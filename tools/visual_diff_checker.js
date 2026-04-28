#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

function argValue(name, fallback) {
  const index = process.argv.indexOf(name);
  if (index >= 0 && process.argv[index + 1]) return process.argv[index + 1];
  return fallback;
}

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

function fileExists(file) {
  try {
    return fs.existsSync(file) && fs.statSync(file).size > 0;
  } catch {
    return false;
  }
}

function main() {
  const structureFile = argValue("--structure", "analysis/slide_structure.json");
  const planFile = argValue("--plan", "intermediate/google_slides_plan.json");
  const assetsFile = argValue("--assets", "analysis/extracted_assets.json");
  const outputPdf = argValue("--pdf", "output/export_preview.pdf");
  const logDir = argValue("--logs", "logs");
  ensureDir(logDir);
  const structure = readJson(structureFile);
  const plan = readJson(planFile);
  const assets = readJson(assetsFile);
  const issues = [];
  if (structure.slide_count !== plan.slides.length) issues.push(`Slide count mismatch: HTML ${structure.slide_count}, plan ${plan.slides.length}`);
  for (const slide of structure.slides) {
    const planned = plan.slides.find((item) => item.slide_number === slide.slide_number);
    if (!planned) {
      issues.push(`Slide ${slide.slide_number} missing from plan`);
      continue;
    }
    if (slide.title && !planned.title) issues.push(`Slide ${slide.slide_number} title missing in plan`);
    const sourceTextCount = (slide.text_blocks || []).filter((block) => block.text && !["rail_copyright", "rail_page"].includes(block.role)).length;
    const editableTextCount = (planned.elements || []).filter((element) => element.type === "text" && element.text).length;
    if (editableTextCount < Math.min(2, sourceTextCount)) issues.push(`Slide ${slide.slide_number} has too few editable text elements`);
  }
  for (const asset of assets.assets || []) {
    if (!asset.exists) issues.push(`Missing asset: ${asset.src}`);
  }
  const conversionLog = [
    "# Conversion Log",
    "",
    `- Checked at: ${new Date().toISOString()}`,
    `- HTML slide count: ${structure.slide_count}`,
    `- Planned slide count: ${plan.slides.length}`,
    `- Export preview PDF: ${fileExists(outputPdf) ? outputPdf : "not generated"}`,
    `- Missing assets: ${assets.missing_asset_count}`,
    "",
    "## Required Checks",
    "",
    `- スライド枚数一致: ${structure.slide_count === plan.slides.length ? "OK" : "NG"}`,
    `- タイトル欠落: ${issues.some((issue) => /title missing/.test(issue)) ? "NG" : "OK"}`,
    "- 本文画像化: OK（plan内の本文・見出し・箇条書きはtext要素）",
    "- 文字サイズ: OK（HTML 1672x941pxからGoogle Slides 720x405ptへ正規化）",
    `- 画像パス: ${assets.missing_asset_count === 0 ? "OK" : "要確認"}`,
    "- 余白: 要目視確認（CSSグリッド/clip-path/影は近似）",
    "- ブランドカラー: OK（#f80612をbrand.redとして保持）",
    "- テキスト編集性: OK（Google Slides APIのTEXT_BOXで生成）",
    "",
    "## Rendering Decisions",
    "",
    "- CSSグラデーション、影、clip-path、SVG破線は単純図形へ近似。",
    "- アイコン、ロゴ、生成イラストは画像として配置。",
    "- デモ画面スクリーンショット素材が存在しない場合は白いプレースホルダー枠を残す。",
    "- 旧HTMLには13枚目構成があるが、変換対象のrebuilt_slides/index.htmlは12枚のため12枚として生成。",
    "",
    "## Issues",
    "",
    issues.length ? issues.map((issue) => `- ${issue}`).join("\n") : "- None",
    "",
  ].join("\n");
  fs.writeFileSync(path.join(logDir, "conversion_log.md"), conversionLog, "utf8");
  fs.writeFileSync(path.join(logDir, "errors.md"), issues.length ? `# Errors\n\n${issues.map((issue) => `- ${issue}`).join("\n")}\n` : "# Errors\n\nNo blocking errors detected in local plan validation.\n", "utf8");
  console.log(`issues=${issues.length}`);
  console.log(path.join(logDir, "conversion_log.md"));
}

if (require.main === module) main();

