#!/usr/bin/env node

const { spawnSync } = require("child_process");

const folderId = process.env.GOOGLE_SLIDES_FOLDER_ID || "16MBLby8NutejHMjyz9--MQw6Dk-nWHvI";

function run(command, args) {
  const result = spawnSync(command, args, { stdio: "inherit", shell: process.platform === "win32" });
  if (result.status !== 0) process.exit(result.status || 1);
}

run("node", ["tools/html_slide_parser.js", "--html", "out/sanko_html/rebuilt_slides/index.html", "--css", "out/sanko_html/rebuilt_slides/styles.css", "--out", "analysis"]);
run("node", ["tools/slide_layout_normalizer.js", "--input", "analysis/slide_structure.json", "--out", "intermediate"]);
run("node", ["tools/google_slides_builder.js", "--plan", "intermediate/google_slides_plan.json", "--out", "output", "--logs", "logs", "--asset-base", "out/sanko_html/rebuilt_slides", "--folder-id", folderId]);
run("node", ["tools/visual_diff_checker.js", "--structure", "analysis/slide_structure.json", "--plan", "intermediate/google_slides_plan.json", "--assets", "analysis/extracted_assets.json", "--pdf", "output/export_preview.pdf", "--logs", "logs"]);
