---
name: visual-diff-checker
description: Check local conversion quality for an HTML-to-Google-Slides rebuild by comparing parsed slide structure, generated plan, extracted assets, and exported preview PDF. Use after Google Slides generation or after plan generation for preflight validation.
---

# visual_diff_checker

Use `tools/visual_diff_checker.js` after plan generation and again after Google Slides PDF export. Treat missing screenshot placeholders as known issues unless the deck requires real screenshots.

Read `README.md` in this folder for the exact inputs, outputs, command, sample, and error checks.
