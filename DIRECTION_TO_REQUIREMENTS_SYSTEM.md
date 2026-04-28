# 方向性から要件定義書を作るシステム

この入口は、要件定義書を書く前の「作りたい資料の方向性」だけを入力にして、既存の資料作成フローに渡せる `requirements.md` を作るためのものです。

既存のスライド作成工程は `requirements.md` 起点のまま使います。

## 使い方

### 1. 方向性だけで新規案件を作る

```powershell
.\tools\new-deck-from-direction.ps1 -Direction "新規SaaSの提案資料。読み手は中小企業の経営者。紙とExcel管理から脱却し、初回商談で導入イメージを持ってもらう資料にしたい。"
```

スクリプト実行ポリシーで止まる場合:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\new-deck-from-direction.ps1 -Direction "新規SaaSの提案資料。読み手は中小企業の経営者。紙とExcel管理から脱却し、初回商談で導入イメージを持ってもらう資料にしたい。"
```

案件名を指定したい場合は `-Name "client-proposal"` を追加します。

作成される主なファイル:

```text
projects/YYYY-MM-DD-<案件名または自動生成名>/
  direction.md
  requirements.md
  intake/
  source/
```

### 2. Codexに要件定義書化を依頼する

```text
projects/YYYY-MM-DD-client-proposal/direction.md を入力として、
DECK_REQUIREMENTS_TEMPLATE.md の形式で requirements.md を作ってください。
不明点は仮置きし、仮定は intake/assumptions.md に残してください。
```

### 3. 生成された要件定義書を既存フローに渡す

```text
projects/YYYY-MM-DD-client-proposal/requirements.md を入力として、
DECK_PRODUCTION_SYSTEM.md の工程で資料を作ってください。
```

## 内部フロー

1. `direction.md` に方向性を保存する。
2. `skills/deck-requirements-builder` で `requirements.md` に変換する。
3. 仮置き・未確定事項を `intake/assumptions.md` に残す。
4. 生成された `requirements.md` を既存の資料作成工程に渡す。

## 判断基準

- 方向性メモは粗くてよい。
- 未確定情報は止めずに仮置きする。
- 仮置きした内容は必ず `intake/assumptions.md` に残す。
- 数字、金額、納期、法務表現、クライアント固有情報は最終確認対象にする。
- 要件定義書は、スライド構成・本文・デザイン・出力形式を決められる粒度まで具体化する。
