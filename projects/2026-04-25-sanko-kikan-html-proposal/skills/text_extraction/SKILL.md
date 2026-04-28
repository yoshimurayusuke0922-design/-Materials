# text_extraction

## Purpose

画像内テキストを抽出し、OCR 由来の崩れを整えて意味単位に整理する。

## Inputs

- 元画像または前処理画像
- 目視確認結果

## Outputs

- `outputs/02_ocr/raw_ocr.txt`
- `outputs/02_ocr/cleaned_text.md`
- `outputs/02_ocr/text_blocks.json`

## Procedure

1. テキストを抽出する。
2. OCR の改行崩れ、誤字、順番崩れを直す。
3. タイトル、サブタイトル、本文などに分ける。
4. JSON 化して HTML 生成に渡せる状態にする。

## Quality Checks

- 主要テキストが欠けていない
- 改行位置が意味単位になっている
- cleaned_text と text_blocks の内容が一致している

## Failure Cases

- OCR で文字が抜ける
- 背景装飾を文字として誤認する
- 複数行テキストの順序が崩れる

## Notes

- OCR が不安定な場合は目視補正を優先する

