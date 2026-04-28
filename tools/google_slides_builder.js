#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const TOKEN_URL = "https://oauth2.googleapis.com/token";
const SLIDES_API = "https://slides.googleapis.com/v1/presentations";
const DRIVE_API = "https://www.googleapis.com/drive/v3/files";
const DRIVE_UPLOAD_API = "https://www.googleapis.com/upload/drive/v3/files";

function argValue(name, fallback) {
  const index = process.argv.indexOf(name);
  if (index >= 0 && process.argv[index + 1]) return process.argv[index + 1];
  return fallback;
}

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function rgb(hex) {
  const clean = String(hex || "#000000").replace("#", "");
  const value = clean.length === 3 ? clean.split("").map((c) => c + c).join("") : clean.padEnd(6, "0").slice(0, 6);
  return {
    red: parseInt(value.slice(0, 2), 16) / 255,
    green: parseInt(value.slice(2, 4), 16) / 255,
    blue: parseInt(value.slice(4, 6), 16) / 255,
  };
}

function pt(magnitude) {
  return { magnitude: Number(magnitude) || 0, unit: "PT" };
}

function transform(x, y) {
  return {
    scaleX: 1,
    scaleY: 1,
    translateX: Number(x) || 0,
    translateY: Number(y) || 0,
    unit: "PT",
  };
}

function objectId(prefix, slideIndex, elementIndex) {
  return `${prefix}_${slideIndex}_${elementIndex}_${Date.now().toString(36)}`.replace(/[^A-Za-z0-9_]/g, "_").slice(0, 50);
}

async function fetchJson(url, options = {}) {
  const res = await fetch(url, options);
  const text = await res.text();
  let data = {};
  try {
    data = text ? JSON.parse(text) : {};
  } catch {
    data = { raw: text };
  }
  if (!res.ok) {
    throw new Error(`${options.method || "GET"} ${url} failed: ${res.status} ${JSON.stringify(data)}`);
  }
  return data;
}

async function accessTokenFromOAuthFile(tokenPath, credentialsPath) {
  if (!fs.existsSync(tokenPath)) return null;
  const token = JSON.parse(fs.readFileSync(tokenPath, "utf8"));
  if (token.access_token && token.expiry_date && token.expiry_date > Date.now() + 60000) return token.access_token;
  if (!token.refresh_token || !fs.existsSync(credentialsPath)) {
    if (token.access_token) return token.access_token;
    throw new Error(`${tokenPath} exists but cannot refresh it. Provide credentials.json or GOOGLE_ACCESS_TOKEN.`);
  }
  const credentials = JSON.parse(fs.readFileSync(credentialsPath, "utf8"));
  const client = credentials.installed || credentials.web || credentials;
  const body = new URLSearchParams({
    client_id: client.client_id,
    client_secret: client.client_secret,
    refresh_token: token.refresh_token,
    grant_type: "refresh_token",
  });
  const data = await fetchJson(TOKEN_URL, {
    method: "POST",
    headers: { "content-type": "application/x-www-form-urlencoded" },
    body,
  });
  token.access_token = data.access_token;
  token.expiry_date = Date.now() + Number(data.expires_in || 3600) * 1000;
  fs.writeFileSync(tokenPath, `${JSON.stringify(token, null, 2)}\n`, "utf8");
  return token.access_token;
}

async function accessTokenFromClasp() {
  const rcPath = path.join(process.env.USERPROFILE || process.env.HOME || "", ".clasprc.json");
  if (!fs.existsSync(rcPath)) return null;
  const rc = JSON.parse(fs.readFileSync(rcPath, "utf8"));
  const token = rc.tokens && rc.tokens.default;
  if (!token) return null;
  if (token.access_token && token.expiry_date && token.expiry_date > Date.now() + 60000) return token.access_token;
  if (!token.refresh_token || !token.client_id || !token.client_secret) {
    if (token.access_token) return token.access_token;
    return null;
  }
  const body = new URLSearchParams({
    client_id: token.client_id,
    client_secret: token.client_secret,
    refresh_token: token.refresh_token,
    grant_type: "refresh_token",
  });
  const data = await fetchJson(TOKEN_URL, {
    method: "POST",
    headers: { "content-type": "application/x-www-form-urlencoded" },
    body,
  });
  token.access_token = data.access_token;
  token.expiry_date = Date.now() + Number(data.expires_in || 3600) * 1000;
  try {
    fs.writeFileSync(rcPath, `${JSON.stringify(rc, null, 2)}\n`, "utf8");
  } catch {
    // The Codex sandbox may allow reading ~/.clasprc.json but not updating it.
  }
  return token.access_token;
}

async function getAccessToken() {
  if (process.env.GOOGLE_ACCESS_TOKEN) return process.env.GOOGLE_ACCESS_TOKEN;
  const token = await accessTokenFromOAuthFile("token.json", "credentials.json");
  if (token) return token;
  const clasp = await accessTokenFromClasp();
  if (clasp) return clasp;
  throw new Error("No Google OAuth token found. Use GOOGLE_ACCESS_TOKEN, token.json+credentials.json, or run clasp login.");
}

function mimeTypeFor(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  if (ext === ".png") return "image/png";
  if (ext === ".jpg" || ext === ".jpeg") return "image/jpeg";
  if (ext === ".gif") return "image/gif";
  if (ext === ".svg") return "image/svg+xml";
  return "application/octet-stream";
}

async function uploadDriveFile(token, filePath, namePrefix = "codex-slide-asset") {
  const boundary = `codex_${Date.now().toString(16)}_${Math.random().toString(16).slice(2)}`;
  const metadata = {
    name: `${namePrefix}-${path.basename(filePath)}`,
  };
  if (process.env.GOOGLE_SLIDES_ASSET_FOLDER_ID) metadata.parents = [process.env.GOOGLE_SLIDES_ASSET_FOLDER_ID];
  const file = fs.readFileSync(filePath);
  const head = Buffer.from(
    `--${boundary}\r\n` +
      "Content-Type: application/json; charset=UTF-8\r\n\r\n" +
      `${JSON.stringify(metadata)}\r\n` +
      `--${boundary}\r\n` +
      `Content-Type: ${mimeTypeFor(filePath)}\r\n\r\n`,
    "utf8",
  );
  const tail = Buffer.from(`\r\n--${boundary}--\r\n`, "utf8");
  const body = Buffer.concat([head, file, tail]);
  const params = new URLSearchParams({
    uploadType: "multipart",
    supportsAllDrives: "true",
    fields: "id,name",
  });
  const data = await fetchJson(`${DRIVE_UPLOAD_API}?${params}`, {
    method: "POST",
    headers: {
      authorization: `Bearer ${token}`,
      "content-type": `multipart/related; boundary=${boundary}`,
      "content-length": String(body.length),
    },
    body,
  });
  await fetchJson(`${DRIVE_API}/${data.id}/permissions?supportsAllDrives=true`, {
    method: "POST",
    headers: {
      authorization: `Bearer ${token}`,
      "content-type": "application/json",
    },
    body: JSON.stringify({ role: "reader", type: "anyone" }),
  });
  return `https://drive.google.com/uc?export=download&id=${data.id}`;
}

async function resolveImageUrls(token, plan, baseDir, logs) {
  const map = new Map();
  const imageElements = plan.slides.flatMap((slide) => slide.elements.filter((element) => element.type === "image"));
  for (const element of imageElements) {
    if (!element.src || map.has(element.src)) continue;
    if (/^https?:\/\//i.test(element.src)) {
      map.set(element.src, element.src);
      continue;
    }
    const localPath = path.resolve(baseDir, element.src);
    if (!fs.existsSync(localPath)) {
      logs.push(`- Missing image skipped: ${element.src}`);
      map.set(element.src, null);
      continue;
    }
    const url = await uploadDriveFile(token, localPath);
    map.set(element.src, url);
    logs.push(`- Uploaded image asset: ${element.src}`);
  }
  return map;
}

async function createPresentation(token, title) {
  return fetchJson(SLIDES_API, {
    method: "POST",
    headers: {
      authorization: `Bearer ${token}`,
      "content-type": "application/json",
    },
    body: JSON.stringify({ title }),
  });
}

async function movePresentationToFolder(token, presentationId, folderId) {
  if (!folderId) return null;
  const current = await fetchJson(`${DRIVE_API}/${presentationId}?fields=parents&supportsAllDrives=true`, {
    headers: { authorization: `Bearer ${token}` },
  });
  const previousParents = (current.parents || []).join(",");
  const params = new URLSearchParams({
    addParents: folderId,
    supportsAllDrives: "true",
    fields: "id,parents,webViewLink",
  });
  if (previousParents) params.set("removeParents", previousParents);
  return fetchJson(`${DRIVE_API}/${presentationId}?${params}`, {
    method: "PATCH",
    headers: { authorization: `Bearer ${token}` },
  });
}

async function batchUpdate(token, presentationId, requests) {
  if (!requests.length) return {};
  return fetchJson(`${SLIDES_API}/${presentationId}:batchUpdate`, {
    method: "POST",
    headers: {
      authorization: `Bearer ${token}`,
      "content-type": "application/json",
    },
    body: JSON.stringify({ requests }),
  });
}

function shapeType(name) {
  const map = {
    rectangle: "RECTANGLE",
    roundRectangle: "ROUND_RECTANGLE",
    ellipse: "ELLIPSE",
    rightArrow: "RIGHT_ARROW",
    triangle: "TRIANGLE",
  };
  return map[name] || "RECTANGLE";
}

function addShapeRequests(requests, element, pageObjectId, id) {
  requests.push({
    createShape: {
      objectId: id,
      shapeType: shapeType(element.shape),
      elementProperties: {
        pageObjectId,
        size: { width: pt(element.width), height: pt(element.height) },
        transform: transform(element.x, element.y),
      },
    },
  });
  const props = {};
  const fields = [];
  if (element.fill && element.fill !== "transparent") {
    props.shapeBackgroundFill = {
      propertyState: "RENDERED",
      solidFill: { color: { rgbColor: rgb(element.fill) } },
    };
    fields.push("shapeBackgroundFill");
  } else {
    props.shapeBackgroundFill = { propertyState: "NOT_RENDERED" };
    fields.push("shapeBackgroundFill");
  }
  if (element.border && element.border !== "transparent") {
    props.outline = {
      outlineFill: { solidFill: { color: { rgbColor: rgb(element.border) } } },
      weight: pt(element.border_width || 1),
    };
    fields.push("outline");
  } else {
    props.outline = { propertyState: "NOT_RENDERED" };
    fields.push("outline");
  }
  requests.push({
    updateShapeProperties: {
      objectId: id,
      shapeProperties: props,
      fields: fields.join(","),
    },
  });
}

function addTextRequests(requests, element, pageObjectId, id) {
  requests.push({
    createShape: {
      objectId: id,
      shapeType: "TEXT_BOX",
      elementProperties: {
        pageObjectId,
        size: { width: pt(element.width), height: pt(element.height) },
        transform: transform(element.x, element.y),
      },
    },
  });
  if (element.rotation) {
    requests[requests.length - 1].createShape.elementProperties.transform = {
      ...transform(element.x, element.y),
      shearX: 0,
      shearY: 0,
    };
  }
  requests.push({ insertText: { objectId: id, insertionIndex: 0, text: element.text || "" } });
  requests.push({
    updateTextStyle: {
      objectId: id,
      textRange: { type: "ALL" },
      style: {
        fontFamily: element.font_family || "Yu Gothic",
        fontSize: pt(element.font_size || 12),
        bold: Boolean(element.bold),
        foregroundColor: { opaqueColor: { rgbColor: rgb(element.color || "#101214") } },
      },
      fields: "fontFamily,fontSize,bold,foregroundColor",
    },
  });
  const alignMap = { center: "CENTER", right: "END", left: "START" };
  requests.push({
    updateParagraphStyle: {
      objectId: id,
      textRange: { type: "ALL" },
      style: {
        alignment: alignMap[element.align] || "START",
        lineSpacing: 100,
      },
      fields: "alignment,lineSpacing",
    },
  });
  const vMap = { middle: "MIDDLE", center: "MIDDLE", bottom: "BOTTOM", top: "TOP" };
  requests.push({
    updateShapeProperties: {
      objectId: id,
      shapeProperties: {
        contentAlignment: vMap[element.valign] || "TOP",
        shapeBackgroundFill: { propertyState: "NOT_RENDERED" },
        outline: { propertyState: "NOT_RENDERED" },
      },
      fields: "contentAlignment,shapeBackgroundFill,outline",
    },
  });
}

function addLineRequests(requests, element, pageObjectId, id) {
  requests.push({
    createLine: {
      objectId: id,
      lineCategory: "STRAIGHT",
      elementProperties: {
        pageObjectId,
        size: { width: pt(Math.max(0.1, element.x2 - element.x1)), height: pt(Math.max(0.1, element.y2 - element.y1)) },
        transform: transform(element.x1, element.y1),
      },
    },
  });
  requests.push({
    updateLineProperties: {
      objectId: id,
      lineProperties: {
        lineFill: { solidFill: { color: { rgbColor: rgb(element.color || "#f80612") } } },
        weight: pt(element.width || 1),
      },
      fields: "lineFill,weight",
    },
  });
}

function addImageRequests(requests, element, pageObjectId, id, imageUrls) {
  const url = imageUrls.get(element.src);
  if (!url) return;
  requests.push({
    createImage: {
      objectId: id,
      url,
      elementProperties: {
        pageObjectId,
        size: { width: pt(element.width), height: pt(element.height) },
        transform: transform(element.x, element.y),
      },
    },
  });
}

function slideRequests(slide, slideObjectId, slideIndex, imageUrls) {
  const requests = [
    {
      updatePageProperties: {
        objectId: slideObjectId,
        pageProperties: {
          pageBackgroundFill: {
            propertyState: "RENDERED",
            solidFill: { color: { rgbColor: rgb(slide.background || "#ffffff") } },
          },
        },
        fields: "pageBackgroundFill",
      },
    },
  ];
  (slide.elements || []).forEach((element, elementIndex) => {
    const id = objectId(element.type, slideIndex, elementIndex);
    if (element.type === "shape") addShapeRequests(requests, element, slideObjectId, id);
    if (element.type === "text") addTextRequests(requests, element, slideObjectId, id);
    if (element.type === "line") addLineRequests(requests, element, slideObjectId, id);
    if (element.type === "image") addImageRequests(requests, element, slideObjectId, id, imageUrls);
  });
  return requests;
}

async function exportPdf(token, presentationId, outputPath) {
  const res = await fetch(`${DRIVE_API}/${presentationId}/export?mimeType=application/pdf`, {
    headers: { authorization: `Bearer ${token}` },
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`PDF export failed: ${res.status} ${text}`);
  }
  const buffer = Buffer.from(await res.arrayBuffer());
  fs.writeFileSync(outputPath, buffer);
}

async function main() {
  const planFile = argValue("--plan", "intermediate/google_slides_plan.json");
  const outputDir = argValue("--out", "output");
  const logDir = argValue("--logs", "logs");
  const htmlBase = argValue("--asset-base", "out/sanko_html/rebuilt_slides");
  const folderId = argValue("--folder-id", process.env.GOOGLE_SLIDES_FOLDER_ID || "");
  ensureDir(outputDir);
  ensureDir(logDir);
  const logs = [];
  const plan = JSON.parse(fs.readFileSync(planFile, "utf8"));
  const token = await getAccessToken();
  const imageUrls = await resolveImageUrls(token, plan, htmlBase, logs);
  const presentation = await createPresentation(token, plan.title || "Generated presentation");
  const presentationId = presentation.presentationId;
  if (folderId) {
    await movePresentationToFolder(token, presentationId, folderId);
    logs.push(`- Moved presentation to Drive folder: ${folderId}`);
  }
  const firstSlideId = presentation.slides && presentation.slides[0] && presentation.slides[0].objectId;
  const slideIds = plan.slides.map((_, index) => (index === 0 ? firstSlideId : `slide_${String(index + 1).padStart(2, "0")}_${Date.now().toString(36)}`));
  await batchUpdate(
    token,
    presentationId,
    plan.slides.slice(1).map((_, index) => ({
      createSlide: {
        objectId: slideIds[index + 1],
        insertionIndex: index + 1,
        slideLayoutReference: { predefinedLayout: "BLANK" },
      },
    })),
  );
  for (let i = 0; i < plan.slides.length; i += 1) {
    const requests = slideRequests(plan.slides[i], slideIds[i], i + 1, imageUrls);
    await batchUpdate(token, presentationId, requests);
    logs.push(`- Built slide ${i + 1}: ${plan.slides[i].title || plan.slides[i].source_id}`);
  }
  const url = `https://docs.google.com/presentation/d/${presentationId}/edit`;
  fs.writeFileSync(path.join(outputDir, "generated_presentation_id.txt"), `${presentationId}\n`, "utf8");
  fs.writeFileSync(path.join(outputDir, "generated_presentation_url.txt"), `${url}\n`, "utf8");
  await exportPdf(token, presentationId, path.join(outputDir, "export_preview.pdf"));
  fs.appendFileSync(path.join(logDir, "conversion_log.md"), `\n## Google Slides API Build\n\n- Presentation ID: ${presentationId}\n- URL: ${url}\n${logs.join("\n")}\n`, "utf8");
  console.log(url);
}

if (require.main === module) {
  main().catch((error) => {
    ensureDir("logs");
    fs.writeFileSync("logs/errors.md", `# Errors\n\n${error.stack || error.message}\n`, "utf8");
    console.error(error.message);
    process.exit(1);
  });
}
