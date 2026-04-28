# list-input-images

## 目的

`out/sanko_html/slide_images` にある入力画像を確認し、対象画像ファイル一覧、スライド順、対象外ファイルを記録する。

## 入力

- `out/sanko_html/slide_images`

## 出力

- `work/input-files.md`

## 手順

1. `.png`, `.jpg`, `.jpeg`, `.webp` を対象にファイル名順で並べる。
2. 画像以外のファイルがあれば対象外として理由を記録する。
3. 1画像=1スライドの対応表を作る。
4. 入力画像数と想定出力スライド数を明記する。
