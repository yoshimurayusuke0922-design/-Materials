# Component HTML Assembly

## Purpose

分解済みレイアウト、テキスト、画像部品を使って、編集可能なHTML/CSSへ組み立てる。

## Inputs

- `design/component_layout_spec.md`
- `design/component_manifest.json`
- `content/bullets.md` または原稿
- 画像部品アセット

## Outputs

- `outputs/04_html_drafts/*.html`
- `outputs/05_final/index.html`
- `outputs/05_final/style.css`

## Procedure

1. 先にHTMLの骨格を組む。
2. タイトル、本文、注釈などの意味テキストをHTMLで配置する。
3. 画像部品は限定された場所にだけ差し込む。
4. 共通コンポーネントはCSSクラスで再利用する。
5. PCとスマホで崩れないか確認する。

## Quality Checks

- 本文テキストが画像化されていないか
- コンポーネント名が意味的で再利用可能か
- 装飾画像に依存しすぎていないか
- 改行や余白が自然か

## Failure Cases

- HTMLで再現できる要素まで画像に頼る
- 1スライドごとに別スタイルを増やしすぎる
- スマホ時に重なりが発生する

## Notes

- 画像部品は補助。主役はHTML構造とテキスト。
