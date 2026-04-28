# implement-slide

## 目的

ワイヤーフレームとデザインシステムに基づき、編集可能な静的HTML/CSS資料を実装する。

## 入力

- `work/wireframes/`
- `work/design-system.md`
- `work/implementation-choice.md`

## 出力

- `out/sanko_html/rebuilt_slides/index.html`
- `out/sanko_html/rebuilt_slides/styles.css`
- `out/sanko_html/rebuilt_slides/script.js`
- `out/sanko_html/rebuilt_slides/assets/`

## 手順

1. 1画像=1スライドの順序を保つ。
2. 文字はHTMLテキストとして実装する。
3. 共通UIは再利用クラスにまとめる。
4. スライド固有の微調整は画像ファイル名由来のクラスで管理する。
