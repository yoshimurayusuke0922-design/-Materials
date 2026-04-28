# Raster Slide Sidebar Adjustment Notes

## Core Principle

When a raster slide sidebar becomes thinner, do not resize the sidebar crop as an image. That compresses text and makes labels look broken. Treat the sidebar as a layout component:

1. Preserve the slide body pixels.
2. Rebuild the sidebar background at the target width.
3. Re-render every text element for that target width.

## Recommended Process

1. Measure the image and existing sidebar boundary.
2. Decide the target sidebar width. For example, `100px -> 67px` is a two-thirds rail.
3. If the body should move left, crop the slide body from the old boundary and paste it at the new boundary.
4. Build the new rail:
   - sample red pixels from the old rail by row, excluding white text
   - use median row colors to preserve the original gradient
   - draw a subtle right-side separator
5. Re-render typography:
   - chapter label horizontal at the top
   - chapter number as one string, e.g. `03`, not stacked digits
   - copyright text rendered normally, then rotated
   - bottom page number centered
6. Inspect the full-resolution PNG after writing.

## Layout Heuristics For A 67px Left Rail

- Keep at least `6px` side padding for top labels.
- Use `Chapter3` at about `12px` in a bold Gothic font.
- Use `03` at about `44px`; this fits as one line and remains legible.
- Use a short divider line under the chapter number, around `31px` wide.
- Use copyright text at `10-11px`; rotate after rendering so letterforms stay natural.
- Use the bottom page number at `28-30px`.

## Font Choice

On Windows Japanese decks, prefer:

- `C:\Windows\Fonts\YuGothB.ttc` for bold labels and numbers
- `C:\Windows\Fonts\YuGothM.ttc` for regular labels when needed
- `C:\Windows\Fonts\meiryob.ttc` as a fallback

Use the deck's existing font family when known. Do not use a visually unrelated font just because it fits.

## Validation Checklist

- The chapter number is a single line.
- No text appears horizontally squashed.
- Copyright text is readable and does not collide with the bottom page number.
- The rail has the requested width.
- The slide body remains visually unchanged except for any intended left shift.
- The output PNG dimensions match the input dimensions.

## Nearby Raster Text Corrections

When a label or paragraph inside the slide body looks horizontally compressed, do not stretch it. Patch it like a sidebar text element:

1. Sample the local background or red label fill row-by-row.
2. Paint only the affected text area.
3. Re-render the replacement copy with the deck font at normal width.
4. Keep line breaks inside the existing column width.

For Japanese text passed through PowerShell into Python, avoid direct non-ASCII literals in piped scripts because the shell encoding can turn Japanese into `?`. Use a UTF-8 script file, `apply_patch`, or Python Unicode escape strings such as `\u30b7\u30b9\u30c6\u30e0`.
