---
name: presentation-art-director
description: Improve business proposal decks, Google Slides, and PPTX presentations. Use when Codex needs stronger slide design, visual hierarchy, spacing correction, editable slide composition, executive proposal polish, mock UI presentation, or redesign of a deck that feels sparse, awkward, or visually weak.
---

# Presentation Art Director

## Overview

Use this skill to turn rough proposal content into polished, executive-ready slides while preserving editability in Google Slides. Prefer native slide text, shapes, tables, and diagrams over flattened images.

## Design Rules

- Preserve strong reference layouts exactly when the user calls them out as good.
- Build editable slides first. Use generated images only for moodboards, decorative backgrounds, or visual references.
- Do not use giant empty white areas. If a slide has unused lower space, add a supporting diagram, decision criteria, next-step cards, or a denser visual system.
- Avoid awkward Japanese line breaks. Use shorter copy, manual phrase breaks, smaller type, or wider text boxes.
- Use a consistent slide grid: 80px side margin, 60px top margin, 60px bottom margin, and 24px/32px gutters.
- Keep proposal decks practical and dense enough for executive scanning. Avoid decorative landing-page layouts.
- For product/mock slides, keep app chrome such as sidebars and top bars visible across screenshots.
- Every slide should answer one of these: why now, what changes, what it looks like, how we proceed, why Field X.

## Visual System

- Base: white and light gray surfaces.
- Accent: Field X red for labels, step arrows, selected states, and warning/risk counts.
- Text: black for headlines, dark gray for body, muted gray for helper notes.
- Cards: small radius, subtle border, no heavy shadow.
- Mock UI: dark left sidebar, light content area, compact cards, realistic status rows.
- Roadmaps: use strong red arrows and numbered circles when matching the reference deck.

## Production Workflow

1. Decide whether the final deck must be editable. If yes, use native slide primitives.
2. Identify reference slides that must be preserved.
3. Create a tighter storyboard with fewer but stronger slides.
4. For each slide, define a primary visual: card grid, mock UI, roadmap, comparison table, or architecture map.
5. Fill lower or side whitespace with useful information, not decoration.
6. Validate at thumbnail size. If the slide is not understandable as a thumbnail, strengthen hierarchy.
7. Validate at full size. Fix awkward wrapping, overlapping text, and low-density areas.

## Imagegen Guidance

- Use imagegen/gpt-image-2 for visual direction, moodboards, background motifs, and high-fidelity mock references.
- Do not use imagegen for final Japanese body text, prices, legal claims, or editable diagrams.
- When using an imagegen concept, translate it back into editable Google Slides shapes and text.
