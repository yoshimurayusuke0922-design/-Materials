---
name: deck-production-orchestrator
description: Use when turning a proposal requirements document into a complete HTML/CSS proposal deck through a staged workflow: one-message, submessages, slide structure, copy, design direction, image assets, static HTML implementation, polish review, and final export.
---

# Deck Production Orchestrator

## Goal

Run the whole proposal deck workflow from a requirements document to a final static HTML deck.

## Required Inputs

- `projects/<project>/requirements.md`
- reference slides or design notes if available
- required logos, screenshots, or generated illustration assets

## Stage Gate

Do not skip stages. Save output files before moving on.

1. One message: use `deck-one-message`.
   - Output: `strategy/one_message.md`
2. Submessages: use `deck-submessage-map`.
   - Output: `strategy/submessages.md`
3. Slide structure: use `deck-structure-planner`.
   - Output: `structure/slide_plan.md`
4. Japanese copy: use `deck-bullet-writer`.
   - Output: `content/slide_copy.md`
5. Visual direction: use `deck-design-director`.
   - Output: `design/design_direction.md`
6. Static HTML deck: use `html-proposal-deck-builder`.
   - Output: `html_deck/index.html`, `html_deck/styles.css`, `html_deck/assets/`
7. Illustration and image assets:
   - Use existing assets first.
   - If AI generation is needed, create prompts and save generated files under `assets/`.
8. Polish review: use `deck-polish-reviewer`.
   - Output: `review/polish_todo.md`
9. Final export:
   - Validate HTML preview.
   - Export PDF/PNG if requested.

## Skill Rule

Before each stage, check whether a suitable skill exists in `skills/` or installed skills.

- If it exists, use it.
- If not, create a small skill for that stage before doing the work.
- Keep skill instructions reusable and short.

## Project Folder Shape

```text
projects/<project>/
  requirements.md
  strategy/
  structure/
  content/
  design/
  html_deck/
  review/
  export/
```

## Quality Rules

Read these files before final polish:

- `DECK_MICRO_ADJUSTMENT_RULES.md`
- `DECK_STYLE_SPEC.md`
- `DECK_SIDEBAR_SPEC.md`
- `DECK_WORKFLOW_CHECKLIST.md`

