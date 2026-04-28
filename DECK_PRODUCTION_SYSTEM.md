# 資料作成システム

このフォルダでは、要件定義書を入力にして、提案資料を再現性高く作る。
要件定義書がまだない場合は、先に方向性から要件定義書を作る。

## 入力モード

### A. 方向性から要件定義書を作る

要件定義書がまだない場合は、`direction.md` に作りたい資料の方向性だけを書く。

```text
projects/<案件名>/direction.md
```

その後、`skills/deck-requirements-builder` で `requirements.md` に変換する。

### B. 要件定義書から資料を作る

要件が整理済みになったら、従来通り `requirements.md` を入力にする。

## 基本フロー

1. `direction.md` に方向性を書く、または `DECK_REQUIREMENTS_TEMPLATE.md` をコピーして案件要件を書く。
2. 方向性だけの場合は `skills/deck-requirements-builder` で `requirements.md` を作る。
3. 生成または手書きした `requirements.md` を資料作成工程に渡す。
4. `skills/deck-production-orchestrator` を使い、工程を分割して進める。
5. 工程ごとに必ず成果物を `projects/<案件名>/` に保存する。
6. 画像生成やイラストは手動生成してもよいが、最終資料ではHTML/CSSと静的アセットで再現する。
7. 最終確認は `DECK_MICRO_ADJUSTMENT_RULES.md` と `DECK_STYLE_SPEC.md` に沿って行う。

## 工程

| 工程 | 使うskill | 主な成果物 |
|---|---|---|
| 0. 方向性から要件化 | `deck-requirements-builder` | `requirements.md`, `intake/assumptions.md` |
| 1. ワンメッセージ | `deck-one-message` | `strategy/one_message.md` |
| 2. サブメッセージ | `deck-submessage-map` | `strategy/submessages.md` |
| 3. スライド構成 | `deck-structure-planner` | `structure/slide_plan.md` |
| 4. 本文作成 | `deck-bullet-writer` | `content/slide_copy.md` |
| 5. デザイン方針 | `deck-design-director` | `design/design_direction.md` |
| 6. HTML静的実装 | `html-proposal-deck-builder` | `html_deck/index.html`, `styles.css` |
| 7. 画像・イラスト | `create-slide-illustration-assets.md` / 必要に応じて画像生成skill | `html_deck/assets/` |
| 8. 微調整レビュー | `deck-polish-reviewer` | `review/polish_todo.md` |
| 9. 出力 | `deck-production-orchestrator` | PDF/PNG/納品HTML |

## 重要ルール

- 方向性しかない場合でも止めない。仮置きした内容を `intake/assumptions.md` に残して進める。
- いきなりHTMLを書かない。必ず要件、ワンメッセージ、サブメッセージ、構成を先に確定する。
- 文章はHTMLテキストとして残す。本文を画像化しない。
- イラストは生成してもよいが、最終配置はCSSで再現する。
- 微調整は感覚で終わらせず、`DECK_MICRO_ADJUSTMENT_RULES.md` に追記して次回使う。
- サイドバーや章表記など、繰り返し使うデザインは `DECK_SIDEBAR_SPEC.md` に固定する。

## Codexへの依頼文

方向性を要件定義書にする場合:

```text
projects/<案件名>/direction.md を入力として、
DECK_REQUIREMENTS_TEMPLATE.md の形式で requirements.md を作ってください。
不明点は仮置きし、仮定は intake/assumptions.md に残してください。
```

要件定義書を直接渡す場合:

```text
projects/<案件名>/requirements.md を入力として、
DECK_PRODUCTION_SYSTEM.md の工程で資料を作ってください。
工程ごとに成果物を保存し、必要なskillがなければ作成または既存skillを提案してください。
最終的にHTML/CSS/静的アセットで再現できる資料として出力してください。
```
