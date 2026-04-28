# Design Direction

## Skill Used

- `deck-design-direction-rebuilder`

このデザイン指示は、上記の新規 skill を使う前提で再作成している。

## Overall

- Output format: HTML deck.
- Aspect ratio: 16:9.
- Visual identity: Field X red, white, light gray, black Japanese typography.
- Text policy: explanatory Japanese copy remains editable HTML text.
- Screenshot policy: demo screen slides use empty, fixed placeholder frames for now. Real screenshots will be inserted later without changing the surrounding layout.
- Sidebar rule: cover and full-red divider slides do not use the sidebar. All other slides use the left red sidebar consistently.

## Visual System

### Typography

- Heading style:
  bold Japanese gothic, strong hierarchy, compact line-height.
- Body style:
  short Japanese lines that avoid awkward wrapping.
- Accent style:
  red only for section labels, emphasis bars, chapter cues, and selected keywords.

### Color

- Primary:
  Field X red.
- Background:
  white or very light gray.
- Card:
  white with subtle outline or very soft shadow.
- Divider slides:
  full red with pale oversized chapter numeral.

### Component Rules

- Cards:
  low-radius rounded rectangles, tightly aligned.
- Message bars:
  light red or red outline, not oversized.
- Placeholder frames:
  neutral white or pale gray blocks with subtle dashed outline and short label text.

## Reference Usage

### 00 Cover / Agenda / Divider

- Reference:
  `references_by_section/00_cover_agenda`
- Preserve:
  original Field X proposal identity, strong red/white composition, clean chapter divider feel.

### 01 Context

- Reference:
  `references_by_section/01_context`
- Preserve:
  practical, businesslike card layout with concise text blocks.

### 02 Proposal / Mock

- Reference:
  `references_by_section/02_proposal_mock`
- Preserve:
  strong summary composition from `mock_07_summary.png`.
- Adapt:
  demo slides are placeholder-first for now, not filled with screenshots yet.

### 03 Roadmap / Future

- Reference:
  `references_by_section/03_roadmap_future`
- Preserve:
  roadmap seriousness and future-expansion clarity.

## HTML vs Image Policy

- HTML only:
  cover text, agenda labels, card copy, roadmap labels, future labels, subsidy slide copy.
- Image2 or raster later:
  actual screen images for slides 07-09 if needed.
- Placeholder now:
  all screen areas on slides 07-09.
- Avoid:
  rasterized body text.

## Slide-by-Slide Direction

## 01 Cover

- Layout:
  strongly follow the reference cover composition.
- Keep:
  organic red forms, centered white content block, Field X logo placement.
- Editable text:
  title and subtitle only.
- Sidebar:
  none.

## 02 Agenda

- Layout:
  reference agenda system with three clear agenda items.
- Improve:
  spacing, line breaks, and vertical balance.
- Sidebar:
  present.
- Editable text:
  all text in HTML.

## 03 Divider: 今回のご提案につきまして

- Layout:
  full red divider, pale large chapter numeral, white title.
- Sidebar:
  none.
- Tone:
  neutral and clean, not dramatic.

## 04 現状課題と今回整理すべき論点

- Layout:
  four cards plus one bottom takeaway bar.
- Information hierarchy:
  lead at top, cards in main zone, takeaway bar at bottom.
- Card density:
  each card should fit 2-3 short bullets.
- Sidebar:
  present.

## 05 提案の骨子

- Layout:
  one strong lead at top plus four cards.
- Card weighting:
  Card 1 and Card 2 should feel slightly more foundational.
  Card 3 is usability.
  Card 4 is expansion.
- Sidebar:
  present.
- Icons:
  optional small icons if they support clarity, but not required.

## 06 Divider: デモ画面イメージ

- Layout:
  full red divider matching the chapter system.
- Sidebar:
  none.

## 07 デモ画面イメージ 1

- Layout:
  one large empty screenshot frame with small HTML callouts around it.
- Placeholder treatment:
  a fixed large frame labeled for later screenshot insertion.
- Intended screenshot:
  property, tenant, vacancy, repair, history overview.
- Sidebar:
  present.

## 08 デモ画面イメージ 2

- Layout:
  two or three empty placeholder frames plus short labels.
- Placeholder treatment:
  balanced multi-frame layout that can later hold contract / invoice / mobile screenshots.
- Intended screenshot:
  contract generation, invoice handling, smartphone usage.
- Sidebar:
  present.

## 09 デモ画面イメージ 3

- Layout:
  four-way grid or asymmetrical collage of empty frames.
- Placeholder treatment:
  fixed frame sizes so later image insertion does not break the slide.
- Intended screenshot:
  own-property publishing, other-property publishing, inquiry handling, AI assist.
- Sidebar:
  present.

## 10 Divider: 将来的な展望と今後の進め方

- Layout:
  full red divider.
- Sidebar:
  none.

## 11 展開イメージ

- Layout:
  central hub with four surrounding cards.
- Information hierarchy:
  center first, outer expansion second.
- Implementation choice:
  build in HTML/CSS first. If the center feels weak later, add one image2 background figure behind HTML labels.
- Sidebar:
  present.

## 12 今後の進め方

- Layout:
  strongly respect the existing reference roadmap slide.
- Preserve:
  serious tone, left-to-right process readability, strong step progression.
- Improve:
  alignment, spacing, icon fit, and text density.
- Sidebar:
  present.

## 13 補助金活用について

- Layout:
  calm two-column summary with one short note area below.
- Left:
  subsidy possibility and official-condition summary.
- Right:
  support scope.
- Tone:
  factual, careful, not sales-heavy.
- Sidebar:
  present.

## Implementation Notes

- Build a shared slide shell with:
  - optional sidebar
  - title zone
  - constrained content area
  - stable footer/page number area
- Keep sidebar logo fully visible at all times.
- Demo placeholder frames must have stable aspect ratios and fixed dimensions.
- Use short Japanese labels inside or above placeholders such as `画面イメージ`, `スクリーンショット挿入予定`, `契約 / 請求`, `出稿 / 反響対応`.

## Immediate Next Tasks

1. Update HTML deck to 13 slides.
2. Rebuild agenda, context, and proposal summary to match the new copy.
3. Replace screenshot slides with empty placeholder layouts for 07-09.
4. Rebuild future slide around the central data hub.
5. Rebuild roadmap slide in the reference style.
6. Add the final subsidy slide.
