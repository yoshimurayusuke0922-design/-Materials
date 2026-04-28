# Section Plan

## 1. Cover Canvas

- 役割: 表紙としての世界観を作る
- HTML: `main`
- CSS: 背景色、相対配置、16:9比率

## 2. Decorative Shapes

- 役割: 視線誘導とブランドトーンの形成
- HTML: 装飾用 `div`
- CSS: 楕円、円、角丸を使った有機形状
- 備考: 意味要素ではないため `aria-hidden` 扱い

## 3. Recipient Label

- 役割: 誰向けの提案かを明示
- HTML: `header`
- CSS: 左上寄り、本文より小さめ

## 4. Hero Panel

- 役割: タイトル、サブタイトル、提案テーマをまとめる
- HTML: `section > p + h1 + p`
- CSS: 大型白パネル、角丸、シャドウ

## 5. Date

- 役割: 提案日の明示
- HTML: `p`
- CSS: 左下寄りに独立配置

## 6. Brand

- 役割: 提案元の識別
- HTML: `footer > img`
- CSS: 小型白パネルの上にロゴを配置

## PC / Mobile方針

- PC: 画像に近いレイアウトを維持
- Mobile: 宛先 → タイトルパネル → 日付 → ロゴ の順で縦積み
- 装飾は残すが、本文の可読性を最優先
