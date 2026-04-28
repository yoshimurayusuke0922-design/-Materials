# layout_analysis

## Purpose

画像内のレイアウトを意味単位のブロックへ分解する。

## Inputs

- `outputs/00_preprocessed/` の前処理画像
- 元画像の目視情報

## Outputs

- `outputs/01_analysis/visual_analysis.md`
- `outputs/01_analysis/layout_blocks.json`
- `outputs/01_analysis/detected_elements.json`

## Procedure

1. 画像が何の資料かを特定する。
2. 見出し、本文、図形、ロゴ、背景装飾を洗い出す。
3. ブロックごとに役割、重要度、位置を定義する。
4. HTML 化で再現すべき要素と再設計してよい要素を分ける。

## Quality Checks

- 見出しと本文が分離できている
- 装飾と情報要素が混同されていない
- HTML 設計に使える粒度になっている

## Failure Cases

- 背景装飾を本文要素として誤認する
- 画像全体を 1 ブロックとしてしか捉えられない

## Notes

- 完全一致ではなく、Web として意味のある再構築を優先する

