---
name: slide-layout-normalizer
description: Convert parsed HTML slide structure into intermediate/google_slides_plan.json and intermediate/layout_mapping.json for editable Google Slides generation. Use after html_slide_parser.
---

# slide_layout_normalizer

Use `tools/slide_layout_normalizer.js` after `analysis/slide_structure.json` exists. Keep body copy, headings, bullets, and numeric proposal content as `text` elements. Use images only for logos, icons, illustrations, and screenshot-like visuals.

Read `README.md` in this folder for the exact inputs, outputs, command, sample, and error checks.
