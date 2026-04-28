---
name: slide-sidebar-raster-adjuster
description: Rebuild thin left sidebars in raster slide PNGs without horizontally crushing text. Use when Codex needs to narrow a slide sidebar, fix sidebar typography after a raster/sidebar resize, convert stacked chapter digits like "0" and "3" into one-line "03", or preserve the slide body while re-rendering sidebar labels, copyright text, and page numbers.
---

# Slide Sidebar Raster Adjuster

## Overview

Use this skill for slide PNGs where the slide body should remain raster-identical but the left sidebar needs a new width or typography. Do not scale text horizontally; rebuild the sidebar background and re-render each text element at sizes chosen for the target width.

## Workflow

1. Inspect the current PNG size and estimate:
   - original sidebar width
   - target sidebar width
   - where the slide body starts
   - chapter label, chapter number, copyright text, and page number
2. If the sidebar width is changing, shift the body from the original sidebar boundary to the target sidebar boundary. Fill the newly exposed right edge from the original edge pixels.
3. Rebuild the sidebar as a clean rail:
   - sample red pixels row-by-row from the existing rail when possible
   - draw a simple fallback red gradient when sampling is unreliable
   - add a subtle right divider/shadow
4. Re-render text for the target width:
   - use a one-line chapter number such as `03`, not stacked `0` and `3`
   - center top label and chapter number inside the rail
   - rotate copyright text as text, not as a compressed crop
   - center the page number near the bottom
5. Validate visually at original resolution.

Use the same principle for nearby raster labels in the slide body when a resized image has unnaturally narrow text: erase only the affected label/copy area with local background sampling, then re-render text at normal width.

## Script

Prefer `scripts/adjust_sidebar.py` for deterministic edits:

```powershell
python .\skills\slide-sidebar-raster-adjuster\scripts\adjust_sidebar.py `
  --input .\out\sanko_html\slide_images\12_roadmap_reference.png `
  --output .\out\sanko_html\slide_images\12_roadmap_reference.png `
  --source-rail-width 100 `
  --target-rail-width 67 `
  --chapter-label "Chapter3" `
  --chapter-number "03" `
  --page-number "12"
```

If the slide has already been narrowed and only text needs re-rendering, set `--source-rail-width` equal to `--target-rail-width`.

## Typography Rules

For a 16:9 slide around `1600x900` with a `67px` rail:

- chapter label: `11-12px`, centered
- chapter number: `40-44px`, one line, centered
- copyright: `10-11px`, rotated after rendering
- page number: `28-30px`, centered
- divider lines: keep inside the rail with at least `16px` horizontal padding

Scale sizes proportionally if the rail width differs. Always check that the longest text width fits within the rail before rendering.

## Reference

Read `references/sidebar-raster-adjustment.md` when adapting the method to another deck, a different sidebar orientation, or a different typography system.
