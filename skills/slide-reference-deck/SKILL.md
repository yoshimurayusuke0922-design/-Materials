---
name: slide-reference-deck
description: Create Google Slides presentation assets from reference slide images. Use when Codex needs to turn existing deck screenshots, slide PNGs, or PDFs into a reusable reference library, plan a new proposal deck, generate imagegen prompts for editable slide backgrounds, or organize per-project slide production folders.
---

# Slide Reference Deck

## Overview

Use this skill to build a new deck from prior slide images while keeping final copy editable in Google Slides. Treat reference images as layout and visual-direction inputs, not as text sources to reproduce verbatim.

## Workflow

1. Inspect the project root and use the established folders:
   - `reference_slides/library/<reference-set>/slides/`
   - `reference_slides/library/<reference-set>/metadata.md`
   - `projects/<date>-<project-name>/`
   - `workflow/prompts/imagegen_slide_background.md`
2. Ask the user only for missing business inputs that block progress. Prefer using `projects/_template/requirements.md` as the intake format.
3. Index reference slides in `metadata.md` with purpose, layout, visual style, and best-use cases.
4. Create `slide_plan.md` for the new deck. For each slide, choose one or more reference slide images and state why.
5. Use `$imagegen` through the built-in image generation path to create 16:9 background/layout images only.
6. Keep final Japanese copy, numbers, tables, and client-specific details out of generated images unless the user explicitly accepts rasterized text.
7. Save generated background images in `projects/<project>/generated_backgrounds/`.
8. Write editable copy and placement notes in `projects/<project>/google_slides_text.md`.
9. Record each generation attempt in `projects/<project>/generation_log.md`.

## Imagegen Rules

- Load local reference images into context before asking imagegen to use them.
- Use reference images for composition, spacing, hierarchy, palette, and visual tone.
- Generate backgrounds, diagrams, and layout scaffolds. Put exact text into Google Slides later.
- Use `16:9 landscape` and specify `Google Slides background / slide layout reference`.
- Require `no readable text` or only neutral placeholder blocks by default.
- Avoid fake logos, garbled text, dense tables, and final legal or financial claims inside images.
- For each generated asset, copy or move the final file into the project folder before referencing it.

## Output Standard

For each deck project, produce these files:

- `requirements.md`: user/business requirements.
- `slide_plan.md`: slide-by-slide plan and reference mapping.
- `generated_backgrounds/*.png`: imagegen outputs used as slide backgrounds.
- `google_slides_text.md`: exact editable copy and placement notes.
- `generation_log.md`: prompts, reference images, and selected output paths.

## Proposal Deck Fidelity Rules

- Preserve high-value reference layouts instead of redrawing them loosely.
- When the user says a slide should be respected, reuse the reference composition directly and only change content that must change.
- Keep recurring app UI elements, especially the left sidebar/navigation, across all mock screenshots unless the user asks to remove them.
- Avoid awkward Japanese wrapping. Prefer shorter copy, smaller type, wider text boxes, or manual line breaks at phrase boundaries.
- Do not leave large empty mock areas. Expand screenshots, add realistic rows/cards/status blocks, or add supporting panels that clarify requirements.
- For Field X proposal decks, keep the reference deck's opening pattern: cover, agenda, and the first chapter divider should match the prior deck style closely.

## Prompt Templates

Use `references/prompt-patterns.md` for imagegen prompt patterns and negative constraints.

## User Handoff

When reporting back, tell the user only:
- Which folder to place reference files into.
- Which template file to fill next.
- Which generated files are ready to paste into Google Slides.
- Any missing input that blocks the next production step.
