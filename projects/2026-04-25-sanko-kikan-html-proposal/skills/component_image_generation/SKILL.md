# Component Image Generation

## Purpose

image生成をスライド全体ではなく、装飾・図・UIフレームなどの部品単位で行う。

## Inputs

- `design/component_layout_spec.md`
- `design/component_manifest.json`
- 参考画像

## Outputs

- `design/component_prompt_map.md`
- `design/component_asset_plan.md`
- 生成した各部品の保存先メモ

## Procedure

1. 画像生成対象を装飾、図解、UIフレーム、背景ニュアンスに限定する。
2. 各部品ごとに役割、サイズ、透明背景要否、禁止事項を定義する。
3. テキスト入り画像を避ける。
4. 1部品ずつ生成し、命名規則に沿って保存する。
5. HTMLで重ねる前提で、部品の境界が自然か確認する。

## Quality Checks

- 画像部品に本文テキストが入っていないか
- 透明背景や矩形切り出し前提が明確か
- 同じカードやフレームを複数回使い回せるか
- スライド全体の一発生成に戻っていないか

## Failure Cases

- 全ページをそのまま画像生成してしまう
- 画像内に見出しや本文まで焼き込んでしまう
- 部品サイズがHTML配置に合っていない

## Notes

- image生成は「完成物生成」ではなく「部品生成」に使う。
