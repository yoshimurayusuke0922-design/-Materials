---
name: html-proposal-deck-builder
description: Use when producing a proposal deck as HTML/CSS instead of Google Slides. Applies when the output should be browser-previewable, iterated through visual feedback, optionally printed/exported to PDF, and may include image2 assets while keeping text editable in HTML.
---

# HTML Proposal Deck Builder

## Goal

Build a deck as HTML sections that can be previewed in a browser and exported to PDF.

## Output

- `html_deck/index.html`
- `html_deck/styles.css`
- `html_deck/assets/`
- optional `html_deck/README.md`

## Process

1. Read strategy, content, structure, and design files.
2. Use one `<section class="slide">` per slide.
3. Keep headings and real copy as HTML text.
4. Use image2 assets only for:
   - mock UI screenshots
   - decorative backgrounds
   - complex diagrams where CSS would look weak
5. Use CSS print rules:
   - 16:9 slide size
   - `page-break-after: always`
   - no browser default margins
6. Validate in browser with screenshots where possible.

## HTML Rules

- Do not put long body text into images.
- Use stable CSS dimensions to avoid layout shifts.
- Avoid visible instructions or meta explanations in the deck.
- Keep Japanese line lengths controlled with deliberate widths and shorter copy.
