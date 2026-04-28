# capture-slide-preview

## 目的

実装したHTMLスライドをChrome headlessでスクリーンショット化し、元画像との確認に使う。

## 入力

- `out/sanko_html/rebuilt_slides/index.html`

## 出力

- `work/previews/{元画像ファイル名の拡張子なし}.png`

## 手順

1. `?slide={番号}` で対象スライドだけを表示する。
2. 1672x941 viewportでスクリーンショットを撮る。
3. ファイル名は元画像の拡張子なしに合わせる。
4. 失敗した場合は理由を `work/review/` に残す。
