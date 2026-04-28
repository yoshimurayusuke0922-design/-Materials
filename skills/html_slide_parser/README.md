# html_slide_parser

HTML/CSSで作成されたスライドを読み、スライド単位の構造JSONへ分解する工程です。

## 入力形式

- HTML: `.slide`単位で区切られたスライドHTML
- CSS: スライド幅、高さ、色、カード、余白などを含むCSS
- 既定入力:
  - `out/sanko_html/rebuilt_slides/index.html`
  - `out/sanko_html/rebuilt_slides/styles.css`

## 出力形式

- `analysis/slide_structure.json`
  - スライド枚数
  - 各スライドのタイトル、見出し、本文、箇条書き、カード、図形、画像、背景色
- `analysis/extracted_assets.json`
  - 使用画像一覧
  - 存在確認結果
  - 使用スライド番号

## 実行方法

```powershell
node .\tools\html_slide_parser.js `
  --html .\out\sanko_html\rebuilt_slides\index.html `
  --css .\out\sanko_html\rebuilt_slides\styles.css `
  --out .\analysis
```

## サンプル

```json
{
  "slide_count": 12,
  "slides": [
    {
      "slide_number": 1,
      "source_id": "slide-01-cover",
      "title": "日常業務の効率化と将来的な展望を見据えた..."
    }
  ]
}
```

## エラー時の確認ポイント

- HTMLがUTF-8で読めているか
- `.slide`クラスがスライド単位についているか
- CSSの`:root`に`--slide-w`と`--slide-h`があるか
- `assets/`配下の画像パスがHTMLから見て正しいか

