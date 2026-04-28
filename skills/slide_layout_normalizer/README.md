# slide_layout_normalizer

HTML上の座標・サイズ・意味構造を、GoogleスライドAPIで生成しやすい中間JSONへ変換する工程です。

## 入力形式

- `analysis/slide_structure.json`

## 出力形式

- `intermediate/google_slides_plan.json`
  - `slides[]`
  - `elements[]`
  - `type: text | shape | image | line`
  - Googleスライド座標へ正規化済みの`x`, `y`, `width`, `height`
- `intermediate/layout_mapping.json`
  - HTML pxからGoogle Slides ptへの変換係数
  - 画像化/図形化/テキスト化の判断

## 実行方法

```powershell
node .\tools\slide_layout_normalizer.js `
  --input .\analysis\slide_structure.json `
  --out .\intermediate
```

## サンプル

```json
{
  "slides": [
    {
      "slide_number": 1,
      "background": "#f7f7f6",
      "elements": [
        {
          "type": "text",
          "role": "title",
          "text": "タイトル",
          "x": 32.73,
          "y": 150.64,
          "width": 447.85,
          "height": 77.47,
          "font_size": 24
        }
      ]
    }
  ]
}
```

## エラー時の確認ポイント

- `analysis/slide_structure.json`がJSONとして読めるか
- 対象HTMLが`rebuilt_slides`か旧HTMLか混ざっていないか
- 画像化してよい要素とテキスト化すべき要素が混ざっていないか
- `layout_mapping.json`のsource/targetサイズが想定通りか

