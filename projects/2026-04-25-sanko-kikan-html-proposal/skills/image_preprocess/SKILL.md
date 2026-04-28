# image_preprocess

## Purpose

画像を HTML 化しやすい状態に整え、前処理結果を保存する。

## Inputs

- `input/original/` 配下の元画像

## Outputs

- `outputs/00_preprocessed/normalized.png`
- `outputs/00_preprocessed/resized.png`
- `outputs/00_preprocessed/preprocess_notes.md`

## Procedure

1. 元画像の有無、サイズ、形式を確認する。
2. 必要に応じてリサイズ、余白調整、コントラスト調整を行う。
3. 元画像を壊さず、前処理後の複製を保存する。
4. 実施した処理をメモに残す。

## Quality Checks

- 前処理後の画像で主要要素が見切れていない
- テキスト領域の視認性が悪化していない
- 元画像との対応関係が追える

## Failure Cases

- 元画像が存在しない
- 解像度が低く、前処理しても文字が読めない
- 余白調整で要素を切ってしまう

## Notes

- 元画像がスレッド添付のみでファイル化されていない場合は、その旨をメモに残す

