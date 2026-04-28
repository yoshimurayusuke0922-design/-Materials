#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const DEFAULT_HTML = "out/sanko_html/rebuilt_slides/index.html";
const DEFAULT_CSS = "out/sanko_html/rebuilt_slides/styles.css";
const DEFAULT_OUT = "analysis";

const VOID_TAGS = new Set(["area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"]);

function argValue(name, fallback) {
  const index = process.argv.indexOf(name);
  if (index >= 0 && process.argv[index + 1]) return process.argv[index + 1];
  return fallback;
}

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function decodeEntities(value) {
  return String(value)
    .replace(/&nbsp;/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'");
}

function parseAttrs(tagSource) {
  const attrs = {};
  const attrRe = /([\w:-]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+)))?/g;
  let match;
  while ((match = attrRe.exec(tagSource))) {
    const key = match[1];
    if (key === tagSource.split(/\s+/)[0].replace(/^<|\/?>$/g, "")) continue;
    attrs[key] = decodeEntities(match[2] ?? match[3] ?? match[4] ?? "");
  }
  return attrs;
}

function parseHtml(html) {
  const root = { type: "root", tag: "root", attrs: {}, classes: [], children: [] };
  const stack = [root];
  const tokenRe = /<!--[\s\S]*?-->|<!doctype[\s\S]*?>|<\/?[^>]+>|[^<]+/gi;
  let match;
  while ((match = tokenRe.exec(html))) {
    const token = match[0];
    if (!token || token.startsWith("<!--") || /^<!doctype/i.test(token)) continue;
    if (token.startsWith("</")) {
      const closeTag = token.slice(2, -1).trim().toLowerCase();
      while (stack.length > 1) {
        const node = stack.pop();
        if (node.tag === closeTag) break;
      }
      continue;
    }
    if (token.startsWith("<")) {
      const tagMatch = token.match(/^<\s*([^\s/>]+)/);
      if (!tagMatch) continue;
      const tag = tagMatch[1].toLowerCase();
      if (tag === "script" || tag === "style") {
        const end = new RegExp(`<\\/${tag}\\s*>`, "i");
        const rest = html.slice(tokenRe.lastIndex);
        const endMatch = rest.match(end);
        if (endMatch) tokenRe.lastIndex += endMatch.index + endMatch[0].length;
        continue;
      }
      if (tag === "br") {
        stack[stack.length - 1].children.push({ type: "text", text: "\n" });
        continue;
      }
      const attrs = parseAttrs(token);
      const node = {
        type: "element",
        tag,
        attrs,
        classes: (attrs.class || "").split(/\s+/).filter(Boolean),
        children: [],
      };
      stack[stack.length - 1].children.push(node);
      const selfClosing = /\/\s*>$/.test(token) || VOID_TAGS.has(tag);
      if (!selfClosing) stack.push(node);
      continue;
    }
    const text = decodeEntities(token.replace(/\s+/g, " "));
    if (text.trim()) stack[stack.length - 1].children.push({ type: "text", text });
  }
  return root;
}

function textContent(node) {
  if (!node) return "";
  if (node.type === "text") return node.text;
  return (node.children || []).map(textContent).join("").replace(/[ \t]+\n/g, "\n").replace(/\n[ \t]+/g, "\n").replace(/[ \t]{2,}/g, " ").trim();
}

function findAll(node, predicate, acc = []) {
  if (!node) return acc;
  if (predicate(node)) acc.push(node);
  for (const child of node.children || []) findAll(child, predicate, acc);
  return acc;
}

function hasClass(node, className) {
  return (node.classes || []).includes(className);
}

function anyClass(node, regex) {
  return (node.classes || []).some((className) => regex.test(className));
}

function first(node, predicate) {
  return findAll(node, predicate)[0] || null;
}

function parseCssVars(css) {
  const vars = {};
  const rootMatch = css.match(/:root\s*\{([\s\S]*?)\}/);
  if (!rootMatch) return vars;
  const varRe = /--([\w-]+)\s*:\s*([^;]+);/g;
  let match;
  while ((match = varRe.exec(rootMatch[1]))) vars[`--${match[1]}`] = match[2].trim();
  return vars;
}

function parsePxVars(vars) {
  const px = {};
  for (const [key, value] of Object.entries(vars)) {
    const match = String(value).match(/^(-?\d+(?:\.\d+)?)px$/);
    if (match) px[key] = Number(match[1]);
  }
  return px;
}

function extractUrlsFromStyle(style) {
  const urls = [];
  const re = /url\((['"]?)(.*?)\1\)/g;
  let match;
  while ((match = re.exec(style || ""))) urls.push(match[2]);
  return urls;
}

function normalizeAssetPath(src, baseDir) {
  if (!src) return null;
  if (/^https?:\/\//i.test(src)) return src;
  const clean = src.replace(/^\.\//, "");
  return path.normalize(path.join(baseDir, clean));
}

function inferBackground(slide, cssVars) {
  if (hasClass(slide, "divider")) return cssVars["--red"] || "#f80612";
  if (hasClass(slide, "slide-02-agenda")) return "#f7f7f6";
  if (hasClass(slide, "slide-01-cover")) return "#f7f7f6";
  return cssVars["--bg"] || "#f7f7f6";
}

function inferTextRole(node) {
  if (node.tag === "h1") return "title";
  if (node.tag === "h2") return "title";
  if (node.tag === "h3") return "heading";
  if (node.tag === "li") return "bullet";
  if (hasClass(node, "lead")) return "lead";
  if (hasClass(node, "recipient")) return "recipient";
  if (hasClass(node, "cover-date")) return "date";
  if (hasClass(node, "red-band")) return "message";
  if (hasClass(node, "message-bar")) return "message";
  if (hasClass(node, "agenda-no") || hasClass(node, "divider-no")) return "number";
  return "body";
}

function directTextBlocks(slide) {
  const textNodes = findAll(slide, (node) => {
    if (node.type !== "element") return false;
    if (!["h1", "h2", "h3", "p", "li", "strong", "div", "span"].includes(node.tag)) return false;
    if (node.tag === "div" && !anyClass(node, /^(red-band|amount-box|agenda-no|divider-no)$/)) return false;
    if (node.tag === "span" && !anyClass(node, /^(rail-page|rail-copy|rail-chapter|chapter-label)$/)) return false;
    return Boolean(textContent(node));
  });
  return textNodes.map((node) => ({
    tag: node.tag,
    classes: node.classes || [],
    role: inferTextRole(node),
    text: textContent(node),
  }));
}

function extractCards(slide) {
  const cardNodes = findAll(slide, (node) => node.type === "element" && (hasClass(node, "card") || anyClass(node, /-card$/)));
  return cardNodes.map((card) => {
    const heading = first(card, (node) => node.type === "element" && node.tag === "h3");
    const paragraphs = findAll(card, (node) => node.type === "element" && node.tag === "p").map(textContent).filter(Boolean);
    const bullets = findAll(card, (node) => node.type === "element" && node.tag === "li").map(textContent).filter(Boolean);
    const images = findAll(card, (node) => node.type === "element" && node.tag === "img").map((img) => img.attrs.src).filter(Boolean);
    return {
      classes: card.classes || [],
      heading: heading ? textContent(heading) : "",
      paragraphs,
      bullets,
      images,
      text: textContent(card),
    };
  });
}

function extractImages(slide, baseDir) {
  const imageNodes = findAll(slide, (node) => node.type === "element" && node.tag === "img");
  const images = imageNodes.map((img) => {
    const src = img.attrs.src;
    const resolved = normalizeAssetPath(src, baseDir);
    return {
      src,
      resolved,
      classes: img.classes || [],
      alt: img.attrs.alt || "",
      role: anyClass(img, /logo/) ? "logo" : "image",
      exists: resolved ? fs.existsSync(resolved) : false,
    };
  });
  const styled = findAll(slide, (node) => node.type === "element" && node.attrs.style && /url\(/.test(node.attrs.style));
  for (const node of styled) {
    for (const src of extractUrlsFromStyle(node.attrs.style)) {
      const resolved = normalizeAssetPath(src, baseDir);
      images.push({
        src,
        resolved,
        classes: node.classes || [],
        alt: node.attrs["aria-label"] || "",
        role: "css-background-image",
        exists: resolved ? fs.existsSync(resolved) : false,
      });
    }
  }
  return images;
}

function parseSlides(root, css, baseDir) {
  const cssVars = parseCssVars(css);
  const pxVars = parsePxVars(cssVars);
  const sections = findAll(root, (node) => node.type === "element" && node.tag === "section" && hasClass(node, "slide"));
  return {
    source: {
      html_file: DEFAULT_HTML,
      css_file: DEFAULT_CSS,
      slide_width_px: pxVars["--slide-w"] || 1672,
      slide_height_px: pxVars["--slide-h"] || 941,
      rail_width_px: pxVars["--rail"] || 74,
      css_variables: cssVars,
    },
    slide_count: sections.length,
    slides: sections.map((slide, index) => {
      const titleNode = first(slide, (node) => node.type === "element" && ["h1", "h2"].includes(node.tag));
      const images = extractImages(slide, baseDir);
      const shapes = findAll(slide, (node) => node.type === "element" && (hasClass(node, "shape") || hasClass(node, "top-line") || hasClass(node, "red-mark") || hasClass(node, "side-rail"))).map((node) => ({
        tag: node.tag,
        classes: node.classes || [],
      }));
      return {
        slide_number: index + 1,
        source_id: slide.attrs.id || "",
        source_file: slide.attrs["data-source"] || "",
        classes: slide.classes || [],
        background_color: inferBackground(slide, cssVars),
        title: titleNode ? textContent(titleNode) : "",
        headings: findAll(slide, (node) => node.type === "element" && ["h1", "h2", "h3"].includes(node.tag)).map((node) => ({
          level: node.tag,
          classes: node.classes || [],
          text: textContent(node),
        })),
        body: findAll(slide, (node) => node.type === "element" && node.tag === "p").map(textContent).filter(Boolean),
        bullets: findAll(slide, (node) => node.type === "element" && node.tag === "li").map(textContent).filter(Boolean),
        cards: extractCards(slide),
        text_blocks: directTextBlocks(slide),
        shapes,
        images,
        icons: images.filter((image) => /icon|image2_|fieldx/.test(image.src || "")),
        layout_notes: {
          has_rail: hasClass(slide, "with-rail"),
          is_divider: hasClass(slide, "divider"),
          card_count: extractCards(slide).length,
          image_count: images.length,
          missing_image_count: images.filter((image) => !image.exists).length,
        },
      };
    }),
  };
}

function buildExtractedAssets(structure) {
  const seen = new Map();
  for (const slide of structure.slides) {
    for (const image of slide.images) {
      const key = image.resolved || image.src;
      if (!key) continue;
      if (!seen.has(key)) {
        seen.set(key, {
          src: image.src,
          resolved: image.resolved,
          exists: image.exists,
          roles: new Set(),
          used_on_slides: [],
        });
      }
      const item = seen.get(key);
      item.roles.add(image.role);
      item.used_on_slides.push(slide.slide_number);
      item.exists = item.exists || image.exists;
    }
  }
  return {
    asset_count: seen.size,
    missing_asset_count: Array.from(seen.values()).filter((item) => !item.exists).length,
    assets: Array.from(seen.values()).map((item) => ({
      ...item,
      roles: Array.from(item.roles),
      used_on_slides: Array.from(new Set(item.used_on_slides)).sort((a, b) => a - b),
    })),
  };
}

function main() {
  const htmlFile = argValue("--html", DEFAULT_HTML);
  const cssFile = argValue("--css", DEFAULT_CSS);
  const outDir = argValue("--out", DEFAULT_OUT);
  const htmlPath = path.resolve(htmlFile);
  const cssPath = path.resolve(cssFile);
  const baseDir = path.dirname(htmlPath);
  const html = fs.readFileSync(htmlPath, "utf8");
  const css = fs.readFileSync(cssPath, "utf8");
  const root = parseHtml(html);
  const structure = parseSlides(root, css, baseDir);
  structure.source.html_file = path.relative(process.cwd(), htmlPath).replace(/\\/g, "/");
  structure.source.css_file = path.relative(process.cwd(), cssPath).replace(/\\/g, "/");

  ensureDir(outDir);
  fs.writeFileSync(path.join(outDir, "slide_structure.json"), `${JSON.stringify(structure, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(outDir, "extracted_assets.json"), `${JSON.stringify(buildExtractedAssets(structure), null, 2)}\n`, "utf8");
  console.log(`Parsed ${structure.slide_count} slides`);
  console.log(path.join(outDir, "slide_structure.json"));
  console.log(path.join(outDir, "extracted_assets.json"));
}

if (require.main === module) main();

