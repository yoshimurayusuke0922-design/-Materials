# Component Layout Spec

## Target

- 対象: 表紙スライド
- レイアウト種別: horizontal_cover
- 比率: 16:9

## Layout Frame

- 背景: 明るいグレー寄りの横長キャンバス
- 主役領域: 左上から中央にかけてのテキストエリア
- 装飾領域: 右端、上中央、左下
- ブランド領域: 最下部中央寄り

## Grid Rule

- 左余白: 約 7%
- 上余白: 約 19%
- タイトル開始位置: 上から 31% 前後
- タイトル幅: 約 64%
- 改行: 最大1回
- 日付: 左下寄り
- ロゴ: 下部中央

## HTML Components

- `cover-client`
- `cover-title`
- `cover-date`
- `cover-brand`

## Image Components

- `cover-bg-decorative-horizontal`
  - 用途: 右側の赤い形状、上部の淡い赤、左下の赤形状をまとめた背景部品
  - テキスト: なし
  - 配置: スライド全面

## Text Rules

- タイトルは意味単位で2行以内
- 改行は `見据えた / 基幹管理システムのご提案` の位置に限定
- 副題は置かない
- 宛先は独立ラベルとして左上に置く
- 日付は独立要素として下部左寄りに置く
- `PROPOSAL` は置かない

## Mobile Rule

- スマホ最適化は不要
- 基本は横長固定レイアウトとして扱う
