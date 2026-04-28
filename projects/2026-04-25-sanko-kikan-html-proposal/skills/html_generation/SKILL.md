# html_generation

## Purpose

構造化された情報から、編集しやすい HTML/CSS を生成する。

## Inputs

- `outputs/03_structure/` の設計ファイル
- `outputs/02_ocr/text_blocks.json`
- レイアウト解析結果

## Outputs

- `outputs/04_html_drafts/draft_v1.html`
- `outputs/04_html_drafts/draft_v2.html`
- `outputs/05_final/index.html`
- `outputs/05_final/style.css`

## Procedure

1. 見出しや本文を意味のある HTML タグへ落とす。
2. CSS で見た目を整える。
3. まず draft を作り、必要なら改稿する。
4. 最終版を `outputs/05_final/` に出力する。

## Quality Checks

- セマンティック HTML になっている
- PC 表示で読める
- スマホ表示で大きく崩れない
- 画像背景に頼りすぎていない

## Failure Cases

- 画像の見た目だけを追って div を乱立する
- テキストが画像化されて編集不能になる
- 余白や改行が不自然になる

## Notes

- 完全一致より構造化・可読性・編集性を優先する

