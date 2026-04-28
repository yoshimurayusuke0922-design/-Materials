# Conversion Log

- Checked at: 2026-04-26T14:40:00.706Z
- HTML slide count: 12
- Planned slide count: 12
- Export preview PDF: output/export_preview.pdf
- Missing assets: 7

## Required Checks

- スライド枚数一致: OK
- タイトル欠落: OK
- 本文画像化: OK（plan内の本文・見出し・箇条書きはtext要素）
- 文字サイズ: OK（HTML 1672x941pxからGoogle Slides 720x405ptへ正規化）
- 画像パス: 要確認
- 余白: 要目視確認（CSSグリッド/clip-path/影は近似）
- ブランドカラー: OK（#f80612をbrand.redとして保持）
- テキスト編集性: OK（Google Slides APIのTEXT_BOXで生成）

## Rendering Decisions

- CSSグラデーション、影、clip-path、SVG破線は単純図形へ近似。
- アイコン、ロゴ、生成イラストは画像として配置。
- デモ画面スクリーンショット素材が存在しない場合は白いプレースホルダー枠を残す。
- 旧HTMLには13枚目構成があるが、変換対象のrebuilt_slides/index.htmlは12枚のため12枚として生成。

## Issues

- Missing asset: ./assets/demo_screenshots/demo_1_main.png
- Missing asset: ./assets/demo_screenshots/demo_2_pc.png
- Missing asset: ./assets/demo_screenshots/demo_2_phone.png
- Missing asset: ./assets/demo_screenshots/demo_3_own_listing.png
- Missing asset: ./assets/demo_screenshots/demo_3_partner_listing.png
- Missing asset: ./assets/demo_screenshots/demo_3_response_email.png
- Missing asset: ./assets/demo_screenshots/demo_3_ai_assist.png

## Google Slides Output

- Target Drive folder: `16MBLby8NutejHMjyz9--MQw6Dk-nWHvI`
- Presentation ID: `16X_Fdklq9FkEIslTN3182EbIWNknoeUpFznmbT_bl7c`
- Presentation URL: https://docs.google.com/presentation/d/16X_Fdklq9FkEIslTN3182EbIWNknoeUpFznmbT_bl7c/edit?usp=drivesdk
- Generation route: `google_slides_plan.json` -> editable PPTX fallback -> Drive conversion to Google Slides.
- Direct Slides API route is blocked for the current OAuth project because `slides.googleapis.com` is disabled in project `1072944905499`.
- Export preview PDF: `output/export_preview.pdf`
- Editable PPTX fallback: `output/fallback_editable_from_plan.pptx`
- PPTX slide count check: 12 slides
- PPTX editable text box check: 241 text bodies
