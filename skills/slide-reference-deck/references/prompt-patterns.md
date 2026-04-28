# Prompt Patterns

## Slide Background

Use this pattern when generating a background or layout image from reference slides:

```text
Use case: productivity-visual
Asset type: 16:9 Google Slides background / slide layout reference
Primary request: Create a presentation slide background and layout scaffold for <topic>.
Input images: Use the reference image only for layout, spacing, visual hierarchy, palette, and overall tone.
Style/medium: clean modern Japanese business presentation design
Composition/framing: 16:9 landscape, leave clear editable areas for headline, body copy, and data labels
Color palette: <palette>
Text: no readable final copy; use only neutral placeholder blocks where text will be added later
Constraints: keep the slide suitable for Google Slides editing; do not render client names, prices, final claims, or dense tables in the image
Avoid: garbled text, fake logos, unreadable charts, tiny labels, decorative clutter, overly dramatic shadows, watermark
```

## Reference Selection Notes

For each planned slide, record:

```text
Slide:
Purpose:
Reference image(s):
Why this reference fits:
What to copy: layout / hierarchy / palette / visual motif
What not to copy:
Editable text areas:
```

## Generation Log Entry

```text
## YYYY-MM-DD slide NN
Purpose:
Reference image:
Prompt:
Selected output:
Notes:
```
