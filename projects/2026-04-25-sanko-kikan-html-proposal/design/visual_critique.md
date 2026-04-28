# Visual Critique

## Skill Used

- `deck-visual-critique-rebuilder`

## Current Problems

## 1. Layout balance is weak

- Cover:
  central white box is too plain and large, so it feels like a generic document cover instead of a proposal slide.
- Agenda:
  each item is text-heavy and reads like notes, not like a polished agenda slide.
- Context / proposal:
  cards are mechanically placed and do not create a strong visual hierarchy.
- Demo slides:
  placeholders dominate the page, but the surrounding explanation is too generic to support them.

## 2. Japanese line breaks and text density are poor

- Headlines are long and currently wrapped by width rather than by semantic phrase.
- Some card bodies are too close to paragraph form, which makes them look heavy.
- The same font size strategy is used across slides with very different density, so text blocks do not feel tuned per slide.

## 3. Sidebar system is not visually disciplined enough

- The sidebar itself is conceptually correct, but the red does not feel integrated with the slide body.
- Logo visibility has improved, but the rail still reads like an attached strip rather than a core part of the composition.
- Divider slides and standard slides do not feel like they belong to one tightly controlled system yet.

## 4. Asset treatment is weak

- Icons are barely used or not used where they could add rhythm.
- Existing assets are not orchestrated into a visual language.
- Mock slides feel unfinished because the placeholders are blank boxes with almost no design intent.

## 5. Image2 has not been used where it should be used

- The current HTML implementation is mostly CSS blocks and text.
- That is the main reason the deck feels flat compared with the previous image2-only version.
- The right places for image2 are not body-text slides, but:
  - cover support visual refinement
  - proposal summary decorative/structural figure
  - demo placeholder frames and surrounding visual language
  - future expansion central figure

## Redesign Actions

## A. Tighten the opening system

- Cover should keep the Field X reference composition more literally.
- Agenda should be reduced to cleaner three-row bands with stronger number-to-label contrast.
- Divider slides should have more disciplined title placement and chapter numerals.

## B. Rebuild content slides around stronger hierarchy

- Context:
  cards should feel more like four decision blocks, not four equal memo boxes.
- Proposal:
  stronger lead, more breathing room, clearer priority between Card 1/2 and Card 3/4.
- Message bars:
  should be narrower, cleaner, and less like generic alert boxes.

## C. Redesign placeholders instead of leaving them blank

- Demo slides should use designed screenshot frames with subtle headers, tabs, or UI chrome.
- The frames can remain empty for now, but they should already look intentional.
- Each slide should have a different placeholder composition that previews the eventual screenshot logic.

## D. Use image2 intentionally

- Use image2 to generate:
  - one cover refinement visual guide
  - one proposal-summary visual concept
  - one future-expansion visual concept
  - one demo-placeholder visual language concept
- Then rebuild the HTML to follow those concept images.

## E. Tighten typography and spacing

- Write manual line breaks only at strong phrase boundaries.
- Reduce paragraph feel in cards.
- Use smaller body text where cards are dense, and larger heading contrast where cards are sparse.

## Priority Order

1. Create image2 concept references
2. Rebuild cover / agenda / proposal summary visual rhythm
3. Rebuild demo placeholders with stronger designed frames
4. Rebuild future slide around an image2-backed hub
5. Finalize roadmap and subsidy slide after the new visual system is stable
