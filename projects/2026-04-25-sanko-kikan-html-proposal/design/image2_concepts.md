# Image2 Concepts

## Skill Used

- `deck-image2-concept-builder`

## Goal

HTMLだけでは弱くなる部分に対して、image2 の中間成果物を先に作り、それを基準に再実装する。

## Use Image2 For

## 1. Cover refinement concept

- Purpose:
  cover を「普通の資料」ではなく、既存参考資料の延長にある提案表紙へ戻す。
- What stays editable:
  title, subtitle, client name, date.
- What image2 generates:
  red/white composition guide, organic red forms, light background nuance.

## 2. Proposal summary concept

- Purpose:
  05 提案の骨子 を、単なる 4 カード並びではなく、印象の強い提案要旨スライドにする。
- What stays editable:
  lead, card headings, card text, bottom message.
- What image2 generates:
  layout mood, subtle decorative structure, card rhythm, red emphasis treatment.

## 3. Demo placeholder visual system

- Purpose:
  07-09 を「空欄」でもダサく見えない状態にする。
- What stays editable:
  labels, captions, placeholder titles.
- What image2 generates:
  placeholder frame language, faux application chrome, subtle section illustration cues.

## 4. Future expansion concept

- Purpose:
  11 展開イメージ の中央ハブを弱い CSS 図形から脱却させる。
- What stays editable:
  card titles, descriptions, outer labels.
- What image2 generates:
  hub diagram base visual, connecting energy, subtle data-platform feel.

## Prompt Direction

### Shared Prompt Traits

- Japanese B2B proposal slide
- Field X red and white identity
- clean, premium, restrained
- not marketing, not flashy
- high-end business presentation
- real proposal deck, not poster

### Cover Prompt Core

- premium Japanese proposal cover
- red and white organic composition
- large clean title area
- realistic presentation slide aesthetic
- no body text embedded except minimal placeholder-safe composition

### Proposal Summary Prompt Core

- enterprise proposal summary slide
- four claim blocks with strong hierarchy
- clean red accents
- serious Japanese business deck
- elegant spacing and strong compositional balance

### Demo Placeholder Prompt Core

- SaaS dashboard placeholder presentation slide
- designed screenshot frames
- subtle UI chrome
- empty content zones for later screenshot insertion
- editorial quality business presentation design

### Future Prompt Core

- data platform hub and spoke diagram
- Japanese enterprise AI expansion slide
- center hub emphasized
- four surrounding use cases
- restrained red and white, sophisticated, editable-label friendly

## Implementation Rule After Generation

- Do not paste generated image text into final slides.
- Use generated images only as visual reference or as bounded non-text figures.
- Rebuild headings and explanatory text in HTML after the image2 concepts are created.
