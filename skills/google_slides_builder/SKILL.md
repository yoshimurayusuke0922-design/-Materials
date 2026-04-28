---
name: google-slides-builder
description: Build an editable Google Slides presentation from intermediate/google_slides_plan.json using Google Slides API and Drive API. Use after slide_layout_normalizer when the user needs a real Google Slides URL, editable text boxes, shapes, lines, and image placement.
---

# google_slides_builder

Use `tools/google_slides_builder.js` after `intermediate/google_slides_plan.json` exists. Keep proposal text editable by generating `TEXT_BOX` shapes. Upload local images to Drive and insert them by URL. Do not commit `credentials.json`, `token.json`, `service_account.json`, or `.env`.

Read `README.md` in this folder for the exact inputs, outputs, command, sample, auth setup, and error checks.
