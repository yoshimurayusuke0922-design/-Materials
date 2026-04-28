# google_slides_builder

`intermediate/google_slides_plan.json`からGoogle Slides APIで新規プレゼンを生成する工程です。

## 入力形式

- `intermediate/google_slides_plan.json`
- 画像素材ディレクトリ: `out/sanko_html/rebuilt_slides`
- Google OAuthトークン

## 出力形式

- `output/generated_presentation_url.txt`
- `output/generated_presentation_id.txt`
- `output/export_preview.pdf`
- `logs/conversion_log.md`
- `logs/errors.md`

## 実行方法

```powershell
node .\tools\google_slides_builder.js `
  --plan .\intermediate\google_slides_plan.json `
  --out .\output `
  --logs .\logs `
  --asset-base .\out\sanko_html\rebuilt_slides
```

## 認証

優先順:

1. `GOOGLE_ACCESS_TOKEN`
2. `token.json` + `credentials.json`
3. `%USERPROFILE%\.clasprc.json`

必要な権限:

- Google Slides APIでプレゼンを作成・編集できる権限
- Drive APIで画像アップロード、PDFエクスポート、画像公開リンク作成ができる権限

## サンプル

```text
https://docs.google.com/presentation/d/<presentation-id>/edit
```

## エラー時の確認ポイント

- Google CloudでSlides APIとDrive APIが有効か
- OAuthスコープにSlides/Driveが含まれているか
- `assets/`の画像が存在するか
- Drive上の画像を`anyone with link`で読める設定にできるか
- `output/export_preview.pdf`を書き込めるか

