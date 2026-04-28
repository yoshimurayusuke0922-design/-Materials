# AI画像生成スライドを編集可能な静的コード資料に再構築する指示書

## 目的

AI画像生成で作った提案資料スライドを、後から編集しやすい静的コードを用いた資料に再構築したい。

この作業の目的は、画像をピクセル単位でそのまま再現することではない。

目的は、画像を参考にしながら、資料としての構造を読み取り、後から人間が編集しやすい静的コードを用いた資料として再設計・再実装することである。

---

## やってほしいこと

`/out/sanko_html/slide_images` にある複数枚のスライド画像を確認し、それぞれを編集可能な静的コード資料として再構築してください。

この作業は「画像をHTMLに変換する」ことではありません。

正しくは、

> 画像を参考にして、編集可能な静的スライド資料として再構築する作業

です。

---

## 入力画像の場所

入力画像は以下のディレクトリにあります。

```text
/out/sanko_html/slide_images
```

このディレクトリ内の画像ファイルを、ファイル名順に読み込んでください。

対象にする拡張子は、原則として以下です。

- `.png`
- `.jpg`
- `.jpeg`
- `.webp`

ただし、作業開始時に実際のファイル一覧を確認し、使用対象にする画像ファイル一覧を `/work/input-files.md` に記録してください。

---

## 前提

`/out/sanko_html/slide_images` に複数枚のスライド画像があります。

各画像は、それぞれ1枚のスライドを表しています。

必ず以下の対応関係を守ってください。

- 1画像 = 1スライド
- 画像ファイル名の並び順 = スライド順
- `01_cover.png` = 1ページ目
- `02_agenda.png` = 2ページ目
- `03_divider_proposal.png` = 3ページ目
- 以降も同様に、実際のファイル名順に対応させる

注意：

- この指示書に書かれていない画像ファイルが存在する場合も、勝手に無視しないでください
- まず実際のファイル一覧を取得し、対象ファイルを確定してください
- 対象外にするファイルがある場合は、その理由を `/work/input-files.md` に記録してください

---

## 最重要ルール

以下は必ず守ってください。

- 1画像 = 1スライドとして扱う
- 複数画像の内容を1枚に統合しない
- 内容を勝手に要約してページ数を減らさない
- ページ数を変更しない
- 入力画像が10枚なら、出力も10スライドにする
- 各スライドの情報量・役割・構成を維持する
- ただし、完全なピクセル再現ではなく、編集しやすい構造化を優先する
- 画像をそのまま1枚の背景画像として貼って終わりにしない
- 文字を画像の中に焼き込んだままにしない
- 全要素を `position: absolute` だけで無理やり並べない
- skillを作るだけで満足せず、実際の成果物生成まで進める

---

## 優先順位

この作業では、以下の優先順位で判断してください。

1. 後から編集しやすいこと
2. 資料として見栄えが良いこと
3. 元画像の雰囲気を維持すること
4. 元画像と完全一致すること

完全一致は最優先ではありません。

元画像に近づけるために編集しづらい実装になるくらいなら、元画像から多少変えても構いません。

---

## 静的コード実装に関する方針

実装方式はHTML/CSSに限定しないでください。

目的は、後から編集しやすい静的コード資料として再構築することです。

作業開始時に、今回の資料に最適な実装方式を選定してください。

候補には、少なくとも以下を含めてください。

- 素のHTML/CSS/JavaScript
- Astro
- React + static export
- Svelte / SvelteKit static
- MDX
- Reveal.js
- Slidev
- SVG中心の実装
- その他、静的に出力できて編集しやすい方式

ただし、技術的に凝ることが目的ではありません。

目的はあくまで、

> 後から人間が編集しやすい静的コード資料を作ること

です。

---

## 実装方式の選定基準

実装方式は以下の基準で選んでください。

1. 後から編集しやすいこと
2. スライドごとに構造を分けやすいこと
3. デザインを共通化しやすいこと
4. 画像・図解・テキストを分離しやすいこと
5. 静的ファイルとして出力できること
6. スクリーンショット化やPDF化がしやすいこと
7. 導入・運用が重すぎないこと
8. CodexやAIエージェントが壊しにくいこと

特に理由がなければ、以下を優先してください。

1. 素のHTML/CSS/JavaScript
2. Astro

React / Next.js / Svelte / Slidev / Reveal.js などは候補に含めてよいですが、今回の用途に対して重すぎる場合は選ばないでください。

---

## 実装方式の選定結果

作業開始時に、実装方式の選定結果を以下に保存してください。

```text
/work/implementation-choice.md
```

記載する内容：

- 選んだ実装方式
- 選んだ理由
- 選ばなかった方式とその理由
- この方式で後から編集しやすい理由
- 編集時に主にどのファイルを触ればよいか

---

## 作業方針

以下の方針で進めてください。

- 画像の完全再現は不要
- 文字は可能な限りHTMLやMarkdownなどのテキストとして起こす
- 背景、カード、見出し、本文、図解、注釈、アイコンを構造化する
- 色・余白・フォントサイズ・角丸・影などは変数または共通設定で管理する
- 絶対配置を最小限にする
- 各スライドを独立して編集できる構造にする
- 共通デザインは共通ファイル・共通コンポーネント・共通クラスで管理する
- スライド固有の調整は、実際のファイル名に対応したクラス名・コンポーネント名・セクション名で分ける
- 後からスライドを増やしやすい構成にする
- 複雑な装飾は必要に応じて `assets` 画像として切り出す
- 各スライドごとに中間成果物を残す

---

## 命名ルール

実際の画像ファイル名を基準に、成果物の名前を決めてください。

例：

```text
01_cover.png
```

に対応する成果物は、以下のように命名してください。

```text
/work/analysis/01_cover.md
/work/wireframes/01_cover.md
/work/previews/01_cover.png
/work/review/01_cover.md
```

実装側でも、可能な限り元ファイル名に対応する名前を使ってください。

例：

- CSSクラス: `.slide-01-cover`
- コンポーネント名: `Slide01Cover`
- セクションID: `slide-01-cover`

ただし、実装方式により命名規則が異なる場合は、その方式に合わせて読みやすく整えてください。

---

## skillに関する方針

各アクションを実行する前に、その作業に対応するskillを必要に応じて作成してください。

skillは、場当たり的な作業を避け、再利用可能な手順として整理するために作成します。

ただし、何でも細かくskill化しすぎないでください。

単なる一度きりの細かすぎる操作ではなく、工程単位で意味のあるskillにしてください。

---

## skill作成ルール

- 各工程に対応するskillを必要に応じて作成する
- skillは再利用可能な単位で作成する
- 各skillの目的、入力、出力、実行手順を明文化する
- 作成したskillは `/skills` 配下に保存する
- 以後の各工程は、対応するskillを参照または使用しながら進める
- 新しい工程が必要になった場合は、その工程用のskillを追加で作成する
- skillの乱立は避け、再利用価値がある場合にのみ作成する
- 最後に、使用したskill一覧と役割を `/work/skills-index.md` にまとめる

---

## 作成すべきskillの例

以下のskillを必要に応じて作成してください。

### `/skills/list-input-images.md`

目的：
入力画像ディレクトリを確認し、対象画像ファイル一覧とスライド順を確定する。

入力：

- `/out/sanko_html/slide_images`

出力：

- `/work/input-files.md`

---

### `/skills/analyze-slide.md`

目的：
スライド画像を見て、タイトル・見出し・本文・図解・注釈・背景・カード・アイコンなどを要素分解する。

入力：

- `/out/sanko_html/slide_images` 内の対象スライド画像

出力：

- `/work/analysis/{元画像ファイル名の拡張子なし}.md`

---

### `/skills/create-wireframe.md`

目的：
要素分解結果をもとに、編集しやすい構造案・ワイヤーフレームを作る。

入力：

- `/work/analysis/{元画像ファイル名の拡張子なし}.md`

出力：

- `/work/wireframes/{元画像ファイル名の拡張子なし}.md`

---

### `/skills/build-design-system.md`

目的：
共通色、余白、タイポグラフィ、カードルール、コンポーネントルールを整理する。

入力：

- 各スライドの分析結果
- 各スライドのワイヤーフレーム

出力：

- `/work/design-system.md`

---

### `/skills/choose-static-implementation.md`

目的：
今回の資料に最適な静的コード実装方式を選定する。

入力：

- 入力画像一覧
- スライド枚数
- デザインの複雑さ
- 編集しやすさの要件
- 出力・運用要件

出力：

- `/work/implementation-choice.md`

---

### `/skills/implement-slide.md`

目的：
ワイヤーフレームとデザインルールをもとに、選定した実装方式で静的コード資料を実装する。

入力：

- `/work/wireframes/`
- `/work/design-system.md`
- `/work/implementation-choice.md`

出力：

- `/out/sanko_html/rebuilt_slides` 配下の成果物一式

---

### `/skills/capture-slide-preview.md`

目的：
実装した各スライドをスクリーンショットとして出力する。

入力：

- `/out/sanko_html/rebuilt_slides` の実装成果物

出力：

- `/work/previews/{元画像ファイル名の拡張子なし}.png`

---

### `/skills/review-slide-diff.md`

目的：
元画像と実装結果を比較し、差分と修正方針を記録する。

入力：

- `/out/sanko_html/slide_images/{元画像ファイル名}`
- `/work/previews/{元画像ファイル名の拡張子なし}.png`

出力：

- `/work/review/{元画像ファイル名の拡張子なし}.md`

---

## 作業ステップ

以下の順番で作業してください。

1. `/out/sanko_html/slide_images` にある画像を確認する
2. 入力画像のファイル一覧を取得する
3. 対象画像の枚数とスライド順を確定し、`/work/input-files.md` に保存する
4. 出力スライド数が入力画像数と一致するように計画する
5. 必要なskillを定義し、`/skills` に作成する
6. 静的コード実装方式を選定し、`/work/implementation-choice.md` に保存する
7. 各画像について、分析skillを使って要素分解メモを `/work/analysis` に保存する
8. 各スライドの構造案を、wireframe skillを使って `/work/wireframes` に保存する
9. 共通デザインルールを、design system skillを使って `/work/design-system.md` にまとめる
10. 選定した実装方式で `/out/sanko_html/rebuilt_slides` に静的コード資料を実装する
11. 実装時は、対応するimplementation skillを使って、再利用可能な構造で作る
12. 1枚ずつスクリーンショットを撮って、元画像と比較する
13. 差分メモを `/work/review` に保存する
14. 差分レビュー用skillを使って、見た目より編集性を優先して修正する
15. 最後に、入力画像数と出力スライド数が一致しているか確認する
16. 使用したskill一覧と、それぞれの役割を `/work/skills-index.md` にまとめる

---

## 推奨ディレクトリ構成

以下の構成を基本としてください。

```text
/out/sanko_html/slide_images
  01_cover.png
  02_agenda.png
  03_divider_proposal.png
  ...

/skills
  list-input-images.md
  analyze-slide.md
  create-wireframe.md
  build-design-system.md
  choose-static-implementation.md
  implement-slide.md
  capture-slide-preview.md
  review-slide-diff.md

/work
  input-files.md
  implementation-choice.md
  design-system.md
  skills-index.md

/work/analysis
  01_cover.md
  02_agenda.md
  03_divider_proposal.md

/work/wireframes
  01_cover.md
  02_agenda.md
  03_divider_proposal.md

/work/previews
  01_cover.png
  02_agenda.png
  03_divider_proposal.png

/work/review
  01_cover.md
  02_agenda.md
  03_divider_proposal.md

/out/sanko_html/rebuilt_slides
  実装方式に応じた成果物一式
```

---

## 出力先

最終成果物は、原則として以下に出力してください。

```text
/out/sanko_html/rebuilt_slides
```

既存の `/out/sanko_html/slide_images` は入力画像ディレクトリなので、上書き・削除・移動しないでください。

---

## 出力形式の例

実装方式によって、`/out/sanko_html/rebuilt_slides` の中身は変えて構いません。

### 素のHTML/CSS/JavaScriptの場合

```text
/out/sanko_html/rebuilt_slides
  index.html
  styles.css
  script.js
  assets/
```

### Astroの場合

```text
/out/sanko_html/rebuilt_slides
  package.json
  astro.config.mjs
  src/
  public/
```

### React + static exportの場合

```text
/out/sanko_html/rebuilt_slides
  package.json
  src/
  public/
  dist または out/
```

### Slidevの場合

```text
/out/sanko_html/rebuilt_slides
  slides.md
  components/
  public/
  package.json
```

### SVG中心の場合

```text
/out/sanko_html/rebuilt_slides
  index.html
  slides/
  assets/
```

---

## 出力ルール

- 入力画像の枚数と同じ数のスライドを作る
- `01_cover.png` は 1ページ目に対応させる
- `02_agenda.png` は 2ページ目に対応させる
- `03_divider_proposal.png` は 3ページ目に対応させる
- それ以降も、実際のファイル名順に対応させる
- スライドの順番はファイル名順にする
- ページ番号やコメントで、どの画像に対応しているか分かるようにする
- 複数スライドの内容を1枚に統合しない
- 各スライドは独立した構造として編集できるようにする
- 実装方式に応じて、スライド単位のコンポーネント、セクション、ページ、Markdownブロックなどに分ける
- ただし、実装ファイルとして1つの `index.html` 内に複数 `section` を並べる構成は許可する
- その場合でも、内容上は必ず1画像=1スライドの対応を守る

---

## 品質確認

実装後、以下を確認してください。

- 入力画像数と出力スライド数が一致しているか
- 各スライドがファイル名順に対応しているか
- 実ファイル名と成果物名の対応が分かるか
- 文字が編集可能なテキストになっているか
- 画像が単なる背景貼り付けになっていないか
- 色、余白、フォントサイズなどが共通管理されているか
- スライドごとの差分修正がしやすいか
- 共通パーツを使い回せる構造になっているか
- 不要に複雑な技術選定になっていないか
- 後から人間が見ても編集箇所が分かるか
- `/out/sanko_html/slide_images` の元画像を破壊していないか

---

## 禁止事項

以下は禁止です。

- `/out/sanko_html/slide_images` の元画像を上書き・削除・移動すること
- 画像をそのまま1枚の背景画像として貼って終わりにすること
- 画像内の文字を編集不能なまま残すこと
- 複数スライドを1枚に統合すること
- ページ数を勝手に減らすこと
- 情報を勝手に要約すること
- 全要素を `position: absolute` だけで無理やり配置すること
- 技術的に凝りすぎて編集しづらくすること
- skillを作るだけで実装を進めないこと
- 実装方式を選んだ理由を記録しないこと

---

## 最後に行うこと

作業完了時に、以下をまとめてください。

1. 入力画像ディレクトリ
2. 入力画像数
3. 対象にした画像ファイル一覧
4. 出力スライド数
5. 出力先ディレクトリ
6. 選んだ実装方式
7. 選んだ理由
8. 作成したskill一覧
9. 主要な編集対象ファイル
10. 各スライドの対応関係
11. 元画像との差分で、意図的に変えた箇所
12. 今後修正する場合の手順

---

## 最終注意

この作業は、画像を静的コードに単純変換する作業ではありません。

画像を参考資料として使いながら、編集しやすい静的コード資料に再設計する作業です。

見た目の完全一致よりも、後から修正できること、構造が分かること、再利用しやすいことを優先してください。
