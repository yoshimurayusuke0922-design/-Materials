#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const DRIVE_UPLOAD_URL = "https://www.googleapis.com/upload/drive/v3/files";
const DRIVE_API = "https://www.googleapis.com/drive/v3/files";
const TOKEN_URL = "https://oauth2.googleapis.com/token";

function argValue(name, fallback) {
  const index = process.argv.indexOf(name);
  if (index >= 0 && process.argv[index + 1]) return process.argv[index + 1];
  return fallback;
}

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
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
  if (!res.ok) throw new Error(`${options.method || "GET"} ${url} failed: ${res.status} ${JSON.stringify(data)}`);
  return data;
}

async function accessToken() {
  if (process.env.GOOGLE_ACCESS_TOKEN) return process.env.GOOGLE_ACCESS_TOKEN;
  const rcPath = path.join(process.env.USERPROFILE || process.env.HOME || "", ".clasprc.json");
  const rc = JSON.parse(fs.readFileSync(rcPath, "utf8"));
  const token = rc.tokens && rc.tokens.default;
  if (!token) throw new Error("No default clasp token found. Run clasp login first.");
  if (token.access_token && token.expiry_date && token.expiry_date > Date.now() + 60000) return token.access_token;
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
  return data.access_token;
}

async function upload({ pptxPath, name, folderId }) {
  const token = await accessToken();
  const boundary = `codex_${Date.now().toString(16)}`;
  const metadata = {
    name,
    mimeType: "application/vnd.google-apps.presentation",
  };
  if (folderId) metadata.parents = [folderId];
  const file = fs.readFileSync(pptxPath);
  const head = Buffer.from(
    `--${boundary}\r\n` +
      "Content-Type: application/json; charset=UTF-8\r\n\r\n" +
      `${JSON.stringify(metadata)}\r\n` +
      `--${boundary}\r\n` +
      "Content-Type: application/vnd.openxmlformats-officedocument.presentationml.presentation\r\n\r\n",
    "utf8",
  );
  const tail = Buffer.from(`\r\n--${boundary}--\r\n`, "utf8");
  const body = Buffer.concat([head, file, tail]);
  const params = new URLSearchParams({
    uploadType: "multipart",
    supportsAllDrives: "true",
    fields: "id,name,mimeType,webViewLink",
  });
  const data = await fetchJson(`${DRIVE_UPLOAD_URL}?${params}`, {
    method: "POST",
    headers: {
      authorization: `Bearer ${token}`,
      "content-type": `multipart/related; boundary=${boundary}`,
      "content-length": String(body.length),
    },
    body,
  });
  return { token, data };
}

async function exportPdf(token, presentationId, outputPath) {
  const res = await fetch(`${DRIVE_API}/${presentationId}/export?mimeType=application/pdf`, {
    headers: { authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error(`PDF export failed: ${res.status} ${await res.text()}`);
  fs.writeFileSync(outputPath, Buffer.from(await res.arrayBuffer()));
}

async function main() {
  const pptxPath = path.resolve(argValue("--pptx", "output/fallback_editable_from_plan.pptx"));
  const name = argValue("--name", "株式会社三幸 基幹管理システムのご提案 編集可能版");
  const outDir = argValue("--out", "output");
  const folderId = argValue("--folder-id", process.env.GOOGLE_SLIDES_FOLDER_ID || "");
  ensureDir(outDir);
  const { token, data } = await upload({ pptxPath, name, folderId });
  const url = data.webViewLink || `https://docs.google.com/presentation/d/${data.id}/edit`;
  fs.writeFileSync(path.join(outDir, "generated_presentation_id.txt"), `${data.id}\n`, "utf8");
  fs.writeFileSync(path.join(outDir, "generated_presentation_url.txt"), `${url}\n`, "utf8");
  await exportPdf(token, data.id, path.join(outDir, "export_preview.pdf"));
  console.log(JSON.stringify({ id: data.id, url }, null, 2));
}

if (require.main === module) {
  main().catch((error) => {
    ensureDir("logs");
    fs.writeFileSync("logs/errors.md", `# Errors\n\n${error.stack || error.message}\n`, "utf8");
    console.error(error.message);
    process.exit(1);
  });
}

