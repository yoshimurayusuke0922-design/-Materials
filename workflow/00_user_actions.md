# User Actions

このファイルだけ見れば、あなたがやる操作が分かる状態にしておきます。

## 1. 参考にしたい過去資料を入れる

1. Googleスライドで過去資料を開く。
2. 参考にしたいスライドをPNG画像かPDFで保存する。
3. 新しい参考セットを作る。

```powershell
.\tools\new-reference-set.ps1 -Name "sales-deck-a"
```

4. PNG画像をここに入れる。

```text
reference_slides/library/sales-deck-a/slides/
```

PDFの場合はここに入れる。

```text
reference_slides/library/sales-deck-a/source/original.pdf
```

5. `reference_slides/library/sales-deck-a/metadata.md` に、各スライドの用途をメモする。

## 2. 新しい資料案件を作る

### 方向性だけで始める場合

```powershell
.\tools\new-deck-from-direction.ps1 -Direction "作りたい資料の方向性を書く"
```

スクリプト実行ポリシーで止まる場合:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\new-deck-from-direction.ps1 -Direction "作りたい資料の方向性を書く"
```

案件名を指定したい場合は `-Name "client-proposal"` を追加する。

作成されたフォルダ:

```text
projects/YYYY-MM-DD-<案件名または自動生成名>/
```

次にこちらに依頼してください。

```text
projects/YYYY-MM-DD-client-proposal/direction.md を入力として、
DECK_REQUIREMENTS_TEMPLATE.md の形式で requirements.md を作ってください。
不明点は仮置きし、仮定は intake/assumptions.md に残してください。
```

### 要件定義書から始める場合

```powershell
.\tools\new-deck-project.ps1 -Name "client-proposal"
```

作成されたフォルダ:

```text
projects/YYYY-MM-DD-client-proposal/
```

## 3. 要件を書く

要件から始める場合は、次のファイルを埋める。

```text
projects/YYYY-MM-DD-client-proposal/requirements.md
```

## 4. こちらに依頼する

要件定義書から作る場合は、こう依頼してください。

```text
projects/YYYY-MM-DD-client-proposal/requirements.md を入力として、
DECK_PRODUCTION_SYSTEM.md の工程で資料を作ってください。
```

## 5. Googleスライドで仕上げる

1. `generated_backgrounds/*.png` を各スライドの背景として貼る。
2. `google_slides_text.md` のタイトル・本文・表をGoogleスライド上でテキストボックスとして載せる。
3. 数字、社名、金額、条件はGoogleスライド上で最終確認する。
