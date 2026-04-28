---
name: deck-polish-reviewer
description: Use when reviewing and polishing a Japanese HTML proposal deck for readability, layout, line breaks, sidebar consistency, icon alignment, screenshot frame sizing, visual hierarchy, and final delivery quality.
---

# Deck Polish Reviewer

## Goal

Catch the small issues that caused repeated manual edits: wording, line breaks, icon drift, sidebar inconsistency, screenshot sizing, and layout balance.

## Inputs

- HTML deck folder, usually `html_deck/` or `out/.../rebuilt_slides/`
- `DECK_MICRO_ADJUSTMENT_RULES.md`
- `DECK_STYLE_SPEC.md`
- `DECK_SIDEBAR_SPEC.md`

## Review Checklist

1. Message and structure
   - Every slide supports the one-message.
   - No unnecessary slide remains.
   - Chapter labels match the structure.
2. Text
   - Japanese line breaks are natural.
   - No orphan character or awkward one-word line.
   - Important text is bold enough.
   - Terms are unified.
3. Layout
   - No right-edge or bottom-edge clipping.
   - Cards align.
   - Red bands and message boxes are centered.
   - Dead space is used for screenshots or content.
4. Icons and images
   - Icon visual center matches the background circle.
   - If an icon is off, move the image first, not the circle.
   - Generated assets are not blurry, cropped, or too small.
5. Sidebar
   - Sidebar chapter text is hidden unless the deck spec says otherwise.
   - Copyright is centered.
   - Page number is consistent.
6. Screenshots
   - Demo screenshot slots are large enough.
   - Slots have documented file paths.
   - Empty slots are visually aligned.

## Output

Create `review/polish_todo.md` with:

- Critical fixes
- Nice-to-have fixes
- CSS selectors or HTML locations to edit
- Follow-up rules to add to `DECK_MICRO_ADJUSTMENT_RULES.md`

