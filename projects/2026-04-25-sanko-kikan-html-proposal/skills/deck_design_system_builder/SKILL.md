# Deck Design System Builder

## Purpose

参考資料の見た目ルールを抽出し、左サイドバー、色、文字、カードなどをテンプレ化する。

## Inputs

- 参考スライド画像
- submessages
- slide structure
- bullets

## Outputs

- `design/design.md`
- テンプレ画像
- ページ別 prompt へ流用するルール

## Procedure

1. 参考資料から固定再利用したい要素を抽出する。
2. 左サイドバー、章番号、ページ番号、タイトル位置、カード文法を言語化する。
3. 色、フォントサイズ、余白をトークン化する。
4. そのテンプレだけを表した image を生成する。

## Quality Checks

- 参考資料の文法が再利用できる形で書かれているか
- 色や余白が数値で扱えるか
- 各ページ prompt に転用しやすいか

## Failure Cases

- ページ固有のデザインをテンプレに混ぜる
- 色名だけで終わって数値がない
- テンプレ画像が単なる完成スライドになる

## Notes

- テンプレは資料全体の共通部品として使う。
