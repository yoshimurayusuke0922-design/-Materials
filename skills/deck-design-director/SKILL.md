---
name: deck-design-director
description: Use when deciding a deck's visual direction from reference slides and section-specific reference folders. Applies before creating image2 concepts, HTML, PDF, or slide assets.
---

# Deck Design Director

## Goal

Pick the visual system for each section using reference folders.

## Process

1. Read `references_by_section/README.md`.
2. For each section, inspect only the relevant reference folder.
3. Decide:
   - layout pattern
   - color and typography treatment
   - what can be built in HTML/CSS
   - what should be generated as image2 figure or background
4. Use image2 for visual assets when HTML/CSS would be too crude:
   - app mock screens
   - illustration-like diagrams
   - rich hero/background concepts
5. Keep real Japanese copy editable in HTML whenever practical.
6. Store direction in `design/design_direction.md`.

## Guardrails

- Do not use image2 for final body text unless the user explicitly wants image-only output.
- Keep reference slide strengths intact when the user calls them out.
- Avoid one-off design experiments that cannot be repeated across sections.
