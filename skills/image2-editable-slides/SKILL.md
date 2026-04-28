---
name: image2-editable-slides
description: Use when converting AI-generated slide design concepts or image2 moodboards into editable Google Slides or PPTX decks. Applies when the user wants intermediate design images kept separately, but the final deck must use native slide shapes, text, tables, diagrams, and editable mock UI instead of pasted full-slide images.
---

# Image2 Editable Slides

## Workflow

1. Generate 2-4 concept images only for visual direction.
2. Save concept images under the project, usually `design_concepts/`.
3. Create a concept/check deck for the concepts if the user needs an intermediate artifact.
4. Translate the selected visual language into native slide primitives:
   - text boxes for all real copy
   - rectangles/rounded rectangles for cards, rails, panels, tables
   - circles and simple icons for markers
   - editable lines/arrows for flow and roadmap diagrams
5. Do not paste concept images into the final proposal deck as full-slide backgrounds.
6. Validate the generator or deck file:
   - syntax check Apps Script when used
   - verify PPTX zip integrity when used
   - check slide count and media usage when editability matters

## Design Mapping Rules

- Cover concepts can inform crops, red accents, white space, and faint business motifs.
- Content concepts should become card grids, rail systems, bottom insight bars, and comparison tables.
- Mock UI concepts should become editable app chrome: dark sidebar, top bar, metrics, kanban/status columns, bottom tables, charts, and right-side explanation panels.
- Keep Japanese body copy out of image generation because generated text is unreliable.

## Google Slides Notes

- Prefer Apps Script with `SlidesApp` when direct API access is blocked.
- Put the target folder ID in one constant.
- Provide one entry function that creates and moves the deck to the target folder.
- If OAuth API tools are blocked by Workspace policy, use the user's own Apps Script editor as the first-party execution path.
