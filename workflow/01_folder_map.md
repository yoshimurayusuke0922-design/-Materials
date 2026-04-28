# Folder Map

```text
資料作成/
  workflow/
    00_user_actions.md
    01_folder_map.md
    prompts/
      direction_to_requirements.md
      imagegen_slide_background.md
    templates/
      direction.md
      requirements.md
      reference_metadata.md
      slide_plan.md
      google_slides_text.md
      generation_log.md
  reference_slides/
    _inbox/
    library/
      <reference-set>/
        slides/
          01_cover.png
          02_problem.png
        metadata.md
  projects/
    _template/
      direction.md
      requirements.md
      slide_plan.md
      google_slides_text.md
      generation_log.md
      generated_backgrounds/
      source/
  tools/
    new-reference-set.ps1
    new-deck-project.ps1
    new-deck-from-direction.ps1
  skills/
    deck-requirements-builder/
    slide-reference-deck/
```

## Roles

- `workflow/`: 手順、テンプレート、プロンプト。
- `reference_slides/_inbox/`: まだ整理前のPDF、PNG、PPTX置き場。
- `reference_slides/library/`: 使える参考スライドだけを整理して置く場所。
- `projects/`: 新しく作る資料ごとの作業フォルダ。
- `tools/`: フォルダ作成を省力化するPowerShell。
- `skills/`: この作業専用のCodex skill。
