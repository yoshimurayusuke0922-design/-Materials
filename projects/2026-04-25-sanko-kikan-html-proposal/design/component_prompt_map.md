# Component Prompt Map

## cover-bg-decorative-horizontal

- Purpose:
  横長表紙の背景装飾のみを部品化する
- Output role:
  HTMLテキストの背面に敷く装飾画像
- Must include:
  - 右側から流れ込む大きな赤い有機形状
  - 上部中央寄りの淡い赤い円形ニュアンス
  - 左下の赤い有機形状
  - 左上から中央にかけてテキストを置ける静かな余白
- Must exclude:
  - タイトル
  - 副題
  - ロゴ
  - 文字全般
  - UIや図表
- Prompt strategy:
  完成スライドを描かせず、横長表紙背景だけに限定する

## HTML overlay text

- Purpose:
  宛先、タイトル、日付、ロゴを編集可能に保つ
- Rendering:
  すべてHTML/CSS
- Constraints:
  画像に文字を焼き込まない
