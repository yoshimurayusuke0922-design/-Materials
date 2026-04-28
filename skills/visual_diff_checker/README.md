# visual_diff_checker

元HTMLの解析結果と生成計画・PDF出力を照合し、変換精度チェックログを作る工程です。

## 入力形式

- `analysis/slide_structure.json`
- `analysis/extracted_assets.json`
- `intermediate/google_slides_plan.json`
- `output/export_preview.pdf`

## 出力形式

- `logs/conversion_log.md`
- `logs/errors.md`

## 実行方法

```powershell
node .\tools\visual_diff_checker.js `
  --structure .\analysis\slide_structure.json `
  --plan .\intermediate\google_slides_plan.json `
  --assets .\analysis\extracted_assets.json `
  --pdf .\output\export_preview.pdf `
  --logs .\logs
```

## サンプル

```text
issues=0
logs\conversion_log.md
```

## エラー時の確認ポイント

- スライド枚数が一致しているか
- タイトルが欠落していないか
- 本文・見出し・箇条書きが`text`要素として残っているか
- 画像素材が存在しているか
- `output/export_preview.pdf`が生成済みか
- 赤色`#f80612`がbrand.redとして残っているか

