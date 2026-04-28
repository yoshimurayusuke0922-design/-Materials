# quality_review

## Purpose

生成 HTML を元画像と比較し、欠落、崩れ、改善点を記録する。

## Inputs

- `outputs/04_html_drafts/`
- `outputs/05_final/`
- 解析結果と元画像情報

## Outputs

- `outputs/06_review/comparison_notes.md`
- `outputs/06_review/issues.md`
- `outputs/06_review/improvement_plan.md`
- `outputs/06_review/conversion_report.md`

## Procedure

1. 元画像と HTML を比較する。
2. 情報欠落、見た目の差、改善余地を列挙する。
3. 未解決点と次の改善案を分けて記録する。
4. 最終的な変換レポートをまとめる。

## Quality Checks

- 情報が抜けていない
- HTML がブラウザで表示できる
- レビュー記録が後から読める

## Failure Cases

- 見た目の感想だけで終わる
- 何を再現し、何を再設計したかが分からない

## Notes

- 再現できなかった点は隠さず記録する

