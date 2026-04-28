# Google Slides Generator

This folder contains an editable Google Slides generator for the Sanko core management system proposal.

## Output

- Presentation title: `株式会社三幸_基幹管理システムご提案資料`
- Target Drive folder: `16MBLby8NutejHMjyz9--MQw6Dk-nWHvI`
- Entry point: `createSankoKikanProposal()`

## How To Run

1. Open Google Apps Script with the account that can access the target folder.
2. Paste `Code.gs`.
3. Save the project.
4. Select `createSankoKikanProposal`.
5. Run it and approve the Google-owned Apps Script authorization prompt.

This route is used because the external OAuth/API path was blocked by the Workspace policy. Running the script from Apps Script makes the deck as an editable Google Slides file using native shapes and text.
