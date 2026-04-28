---
name: deck-requirements-builder
description: Use when converting a rough deck direction brief into a complete proposal requirements document before running the deck production workflow.
---

# Deck Requirements Builder

## Goal

Turn a rough direction brief into `projects/<project>/requirements.md` that is detailed enough for the existing deck production workflow.

## Inputs

- `projects/<project>/direction.md`, or an inline user brief
- `DECK_DIRECTION_TEMPLATE.md`
- `DECK_REQUIREMENTS_TEMPLATE.md`
- source files, reference metadata, or existing notes if available

## Output

- `projects/<project>/requirements.md`
- `projects/<project>/intake/assumptions.md`

## Process

1. Read the direction brief and any source files in `source/`.
2. Infer the deck purpose, audience, desired reader decision, offer, key proof points, constraints, required assets, design direction, and output format.
3. Fill `requirements.md` using the structure in `DECK_REQUIREMENTS_TEMPLATE.md`.
4. If information is missing, make conservative assumptions and mark them as `仮置き`.
5. Put open questions and final-check items in `intake/assumptions.md`; do not block the workflow unless the brief lacks both audience and purpose.
6. Keep the requirements operational: every item should help decide slide structure, copy, visual design, or export.

## Quality Rules

- Do not leave the requirements as vague marketing phrases.
- Translate "方向性" into concrete slide requirements, not a polished deck script.
- Separate facts from assumptions.
- Keep risky claims, numbers, prices, deadlines, legal terms, and client-specific facts in the final-check section unless the source material proves them.
- Prefer the minimum complete deck over an overlong deck.
- Requirements should be ready to pass into `deck-production-orchestrator`.
