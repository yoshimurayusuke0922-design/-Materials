const FOLDER_ID = '16MBLby8NutejHMjyz9--MQw6Dk-nWHvI';
const DECK_TITLE = '株式会社三幸_基幹管理システムご提案資料';

const W = 720;
const H = 405;
const RED = '#ff1818';
const DARK = '#15151b';
const BLACK = '#111111';
const TEXT = '#333333';
const MUTED = '#666666';
const GRAY = '#f5f5f5';
const LINE = '#dedede';
const LIGHT_RED = '#ffeaea';
const WHITE = '#ffffff';

function createSankoKikanProposal() {
  const pres = SlidesApp.create(DECK_TITLE);
  const first = pres.getSlides()[0];
  clearSlide(first);

  const builders = [
    cover,
    agenda,
    s => chapter(s, '01', 'これまでにお伺いしたこと'),
    positionSlide,
    heardSlide,
    s => chapter(s, '02', 'ご提案の要旨・デモンストレーション'),
    proposalSummary,
    mockOverview,
    screenshotDashboard,
    screenshotDetail,
    screenshotSearch,
    s => chapter(s, '03', '今後の進め方のイメージ'),
    roadmap,
    comparison,
    futureAi,
    nextActions,
  ];

  builders.forEach((builder, i) => {
    const slide = i === 0 ? first : pres.appendSlide(SlidesApp.PredefinedLayout.BLANK);
    clearSlide(slide);
    builder(slide, i + 1);
  });

  const file = DriveApp.getFileById(pres.getId());
  file.moveTo(DriveApp.getFolderById(FOLDER_ID));

  Logger.log('Created Google Slides: ' + pres.getUrl());
  return pres.getUrl();
}

function clearSlide(slide) {
  slide.getPageElements().forEach(el => el.remove());
  slide.getBackground().setSolidFill(WHITE);
}

function rgb(hex) {
  return hex;
}

function setTextStyle(range, size, color, bold) {
  const style = range.getTextStyle();
  style.setFontFamily('Yu Gothic');
  style.setFontSize(size);
  style.setForegroundColor(color);
  style.setBold(Boolean(bold));
}

function text(slide, x, y, w, h, value, size, color, bold, align) {
  const box = slide.insertTextBox(value, x, y, w, h);
  box.getFill().setTransparent();
  box.getLine().getLineFill().setTransparent();
  const range = box.getText();
  setTextStyle(range, size || 12, color || BLACK, bold);
  if (align) {
    range.getParagraphStyle().setParagraphAlignment(align);
  }
  return box;
}

function rect(slide, x, y, w, h, fill, line, radius) {
  const type = radius ? SlidesApp.ShapeType.ROUND_RECTANGLE : SlidesApp.ShapeType.RECTANGLE;
  const shape = slide.insertShape(type, x, y, w, h);
  if (fill) shape.getFill().setSolidFill(fill); else shape.getFill().setTransparent();
  if (line) shape.getLine().getLineFill().setSolidFill(line); else shape.getLine().getLineFill().setTransparent();
  return shape;
}

function ellipse(slide, x, y, w, h, fill, line) {
  const shape = slide.insertShape(SlidesApp.ShapeType.ELLIPSE, x, y, w, h);
  if (fill) shape.getFill().setSolidFill(fill); else shape.getFill().setTransparent();
  if (line) shape.getLine().getLineFill().setSolidFill(line); else shape.getLine().getLineFill().setTransparent();
  return shape;
}

function arrow(slide, x, y, w, h, fill) {
  const shape = slide.insertShape(SlidesApp.ShapeType.RIGHT_ARROW, x, y, w, h);
  shape.getFill().setSolidFill(fill || RED);
  shape.getLine().getLineFill().setTransparent();
  return shape;
}

function pill(slide, x, y, w, h, label, fill, color) {
  const s = rect(slide, x, y, w, h, fill || RED, fill || RED, true);
  const t = text(slide, x + 4, y + 7, w - 8, h - 10, label, 11, color || WHITE, true, SlidesApp.ParagraphAlignment.CENTER);
  return [s, t];
}

function footer(slide, page) {
  text(slide, 26, 381, 260, 14, 'Copyright @Field X inc. All rights reserved.', 7, '#888888', true);
  rect(slide, 701, 0, 19, 405, RED, RED, false);
  text(slide, 704, 379, 12, 16, String(page), 10, WHITE, true, SlidesApp.ParagraphAlignment.CENTER);
}

function title(slide, chapter, heading) {
  text(slide, 31, 22, 100, 12, chapter, 8, RED, true);
  text(slide, 31, 38, 460, 25, heading, 16, BLACK, true);
}

function dotGrid(slide, x, y, cols, rows, gap, color, size) {
  for (let row = 0; row < rows; row++) {
    for (let col = 0; col < cols; col++) {
      ellipse(slide, x + col * gap, y + row * gap, size || 2, size || 2, color || '#d8d8d8', null);
    }
  }
}

function artTitle(slide, chapterNo, chapter, heading, page) {
  rect(slide, 0, 0, 52, H, RED, RED, false);
  text(slide, 13, 21, 28, 10, 'Chapter', 6, WHITE, true, SlidesApp.ParagraphAlignment.CENTER);
  text(slide, 8, 38, 36, 27, chapterNo, 24, WHITE, true, SlidesApp.ParagraphAlignment.CENTER);
  rect(slide, 12, 72, 28, 2, WHITE, WHITE, false);
  text(slide, 15, 379, 20, 14, String(page), 10, WHITE, true, SlidesApp.ParagraphAlignment.CENTER);
  rect(slide, 70, 28, 58, 6, RED, RED, false);
  text(slide, 70, 43, 470, 23, heading, 16, BLACK, true);
  text(slide, 70, 67, 360, 12, chapter, 7, MUTED, true);
  text(slide, 82, 383, 260, 12, 'Copyright @Field X inc. All rights reserved.', 6, '#999999', true);
}

function featureCard(slide, x, y, w, h, marker, head, body) {
  rect(slide, x, y, w, h, WHITE, LINE, true);
  ellipse(slide, x + 12, y + 13, 38, 38, RED, RED);
  text(slide, x + 17, y + 24, 28, 12, marker, 11, WHITE, true, SlidesApp.ParagraphAlignment.CENTER);
  text(slide, x + 59, y + 16, w - 72, 18, head, 10, BLACK, true);
  rect(slide, x + 14, y + 63, w - 28, 1, LINE, LINE, false);
  text(slide, x + 17, y + 80, w - 34, h - 92, body, 8, TEXT, false);
}

function checkItem(slide, x, y, head, body) {
  ellipse(slide, x, y, 28, 28, LIGHT_RED, LIGHT_RED);
  text(slide, x + 8, y + 5, 14, 12, '✓', 12, RED, true, SlidesApp.ParagraphAlignment.CENTER);
  text(slide, x + 36, y + 2, 76, 12, head, 8, BLACK, true);
  text(slide, x + 36, y + 17, 76, 12, body, 6, MUTED, false);
}

function insightBar(slide, x, y, w, h, head, body, actions) {
  rect(slide, x, y, w, h, LIGHT_RED, RED, true);
  ellipse(slide, x + 14, y + 12, 42, 42, RED, RED);
  text(slide, x + 24, y + 23, 22, 12, '!', 14, WHITE, true, SlidesApp.ParagraphAlignment.CENTER);
  text(slide, x + 69, y + 12, 250, 13, head, 10, BLACK, true);
  text(slide, x + 69, y + 31, 280, 15, body, 7, MUTED, false);
  actions.forEach((label, i) => {
    const bx = x + w - 247 + i * 80;
    rect(slide, bx, y + 21, 66, 22, '#ffd9d9', '#ffd9d9', true);
    text(slide, bx + 3, y + 27, 60, 8, label, 7, RED, true, SlidesApp.ParagraphAlignment.CENTER);
  });
}

function bullets(items) {
  return items.map(v => '・' + v).join('\n');
}

function cover(slide, page) {
  ellipse(slide, -135, -98, 258, 228, RED, RED);
  ellipse(slide, 562, -78, 330, 330, RED, RED);
  ellipse(slide, -96, 304, 193, 169, RED, RED);
  ellipse(slide, 462, 319, 180, 180, null, RED);
  dotGrid(slide, 452, 30, 8, 6, 8, '#d7d7d7', 2);
  dotGrid(slide, 627, 318, 8, 4, 7, RED, 2);
  for (let i = 0; i < 8; i++) {
    rect(slide, 390 + i * 25, 338 - i * 9, 10, 44 + i * 9, '#eeeeee', null, false);
  }
  text(slide, 34, 54, 120, 18, '株式会社三幸　御中', 10, BLACK, true);
  text(slide, 34, 96, 360, 42, '基幹管理システムの', 28, BLACK, true);
  text(slide, 34, 136, 250, 42, 'ご提案資料', 28, BLACK, true);
  text(slide, 34, 190, 430, 24, '他社コンペ・社内稟議向け / モック改善版のご提案', 14, RED, true);
  rect(slide, 34, 246, 325, 34, WHITE, LINE, true);
  text(slide, 48, 256, 300, 10, '改善版モック / 画面別要件 / 開発ロードマップ', 8, BLACK, true);
  text(slide, 34, 232, 120, 18, '2026年04月25日', 11, BLACK, true);
  text(slide, 495, 330, 130, 30, 'Field X', 24, BLACK, true);
  footer(slide, page);
}

function agenda(slide, page) {
  text(slide, 34, 26, 60, 11, 'AGENDA', 7, RED, true);
  text(slide, 34, 39, 55, 15, '目次', 9, BLACK, true);
  const items = [
    ['01', 'これまでにお伺いしたこと', '社内稟議・他社比較に必要な前提整理'],
    ['02', 'ご提案の要旨・デモンストレーション', '改善版モック、画面別要件、将来のAI活用'],
    ['03', '今後の進め方のイメージ', '要件定義から開発・現場導入・改善運用まで'],
  ];
  let y = 108;
  items.forEach(row => {
    text(slide, 197, y, 36, 24, row[0], 20, RED, true);
    text(slide, 258, y + 3, 300, 20, row[1], 13, RED, true);
    text(slide, 261, y + 28, 310, 16, row[2], 10, MUTED, false);
    y += 69;
  });
  footer(slide, page);
}

function chapter(slide, pageLabel, heading, page) {
  rect(slide, 0, 0, W, H, RED, RED, false);
  text(slide, 32, 148, 96, 56, pageLabel, 60, '#ffa6a6', true);
  text(slide, 143, 190, 430, 32, heading, 18, WHITE, true);
  text(slide, 26, 381, 260, 14, 'Copyright @Field X inc. All rights reserved.', 7, '#ffdcdc', true);
}

function card(slide, x, y, w, h, head, body) {
  rect(slide, x, y, w, h, WHITE, LINE, true);
  rect(slide, x, y, w, 4, RED, RED, false);
  text(slide, x + 12, y + 15, w - 24, 16, head, 9, BLACK, true);
  rect(slide, x + 12, y + 40, w - 24, 1, LINE, LINE, false);
  text(slide, x + 12, y + 52, w - 24, h - 58, body, 8, TEXT, false);
}

function positionSlide(slide, page) {
  title(slide, 'Chapter1', '本資料の位置づけ');
  pill(slide, 36, 77, 285, 24, '今回の目的');
  pill(slide, 362, 77, 285, 24, '判断いただきたいこと');
  text(slide, 42, 118, 292, 80, bullets([
    '担当者様に確認いただいたモックを、社内稟議・他社コンペで比較しやすい資料に整理します。',
    '本資料では開発範囲・機能・進め方・将来展開を中心に説明します。',
    '画面単位で要件と機能が分かる改善版モックとして提出します。',
  ]), 9, BLACK, true);
  text(slide, 368, 118, 282, 80, bullets([
    '基幹管理システムを、既存業務に合わせたカスタム開発で進める妥当性。',
    '初期開発で優先する画面・帳票・ワークフローの範囲。',
    'AI音声対応、営業支援AI、契約書自動作成、社内FAQ検索への拡張方針。',
  ]), 9, BLACK, true);
  card(slide, 43, 252, 180, 92, '提出物', '改善版モック\n画面別要件資料\n開発の進め方');
  card(slide, 270, 252, 180, 92, '社内稟議での使い方', '比較観点を整理\n機能範囲を明確化\n導入後の展開を説明');
  card(slide, 497, 252, 180, 92, '次の確認事項', '優先機能\n権限・帳票\n既存データ移行');
  footer(slide, page);
}

function heardSlide(slide, page) {
  title(slide, 'Chapter1', 'これまでにお伺いしたこと');
  const rows = [
    ['基幹システム切り替え', '既存システムのサポート終了を見据え、今年中を目途に切り替え検討が必要。'],
    ['現場定着への配慮', 'IT活用への慣れに差があるため、日常業務に自然に入る画面設計が重要。'],
    ['日常業務の負荷', '退去修繕対応、契約書作成、請求・インボイス対応などの工数が大きい。'],
    ['データ活用の余地', '顧客・物件・契約・対応履歴を横断して見られる状態を作り、判断の質を高める。'],
  ];
  rows.forEach((r, i) => card(slide, 34 + i * 160, 86, 137, 195, r[0], r[1]));
  rect(slide, 38, 312, 622, 44, LIGHT_RED, RED, true);
  text(slide, 50, 323, 590, 16, '単なる画面開発ではなく「基幹業務の整理」と「今後AIを載せられる土台づくり」を同時に進めます。', 10, BLACK, true);
  footer(slide, page);
}

function proposalSummary(slide, page) {
  artTitle(slide, '02', 'Chapter2', 'ご提案の要旨', page);
  pill(slide, 88, 88, 560, 24, '基幹管理・期日管理・対応履歴を一体化し、現場の運用負荷を下げる');
  featureCard(slide, 70, 132, 178, 152, '01', '現状の課題感', '基幹システム切り替え、退去修繕、契約書作成、請求対応など、日常業務の負荷が高い状態です。');
  featureCard(slide, 270, 132, 178, 152, '02', '今回実現すること', '期限、担当、状態、関連書類を一画面で確認できる基幹管理システムとして整理します。');
  featureCard(slide, 470, 132, 178, 152, '03', '将来拡張', 'AI音声対応、営業支援AI、契約書自動作成、社内FAQ検索へ段階的に広げます。');
  insightBar(slide, 70, 316, 608, 56, '社内稟議で伝えるポイント', '画面・要件・進め方を一式で見せ、他社比較で判断しやすい資料にします。', ['画面', '要件', '進め方']);
}

function appShell(slide, x, y, w, h, heading) {
  rect(slide, x, y, w, h, WHITE, LINE, true);
  rect(slide, x, y, 78, h, DARK, DARK, false);
  ellipse(slide, x + 12, y + 13, 16, 16, RED, RED);
  text(slide, x + 33, y + 13, 38, 12, 'Field X', 9, WHITE, true);
  rect(slide, x + 78, y, w - 78, 32, '#fcfcfc', LINE, false);
  text(slide, x + 94, y + 11, 230, 10, heading, 8, BLACK, true);
  text(slide, x + w - 70, y + 11, 44, 9, '担当者', 6, MUTED, false);
  ['総合', '物件', '契約', '修繕', '書類', '検索'].forEach((n, i) => {
    const fill = i === 0 ? RED : '#2d2f36';
    rect(slide, x + 9, y + 43 + i * 24, 60, 17, fill, fill, true);
    text(slide, x + 18, y + 48 + i * 24, 42, 7, n, 6, WHITE, true);
  });
  rect(slide, x + 12, y + h - 36, 50, 1, '#4c4c53', '#4c4c53', false);
  ellipse(slide, x + 13, y + h - 23, 12, 12, '#f1f1f1', '#f1f1f1');
  text(slide, x + 32, y + h - 22, 30, 7, '設定', 5, '#d0d0d0', false);
}

function dashboardUi(slide, x, y, w, h) {
  appShell(slide, x, y, w, h, '基幹管理ダッシュボード');
  const cx = x + 94, cy = y + 45;
  const cw = w - 108;
  [['本日期限', '12'], ['要確認', '7'], ['遅延リスク', '3'], ['完了', '28'], ['未割当', '4']].forEach((r, i) => {
    const bw = (cw - 20) / 5;
    const bx = cx + i * (bw + 5);
    rect(slide, bx, cy, bw, 43, WHITE, LINE, true);
    text(slide, bx + 6, cy + 7, bw - 12, 7, r[0], 6, MUTED, true);
    text(slide, bx + 8, cy + 18, 24, 14, r[1], 13, r[0] === '遅延リスク' ? RED : BLACK, true);
    rect(slide, bx + bw - 32, cy + 31, 24, 1, r[0] === '遅延リスク' ? RED : '#c9c9c9', null, false);
  });
  ['退去精算', '修繕対応', '契約更新', '請求確認', '入居対応'].forEach((col, i) => {
    const bw = (cw - 24) / 5;
    const bx = cx + i * (bw + 6);
    rect(slide, bx, cy + 53, bw, 116, '#f8f8f8', LINE, true);
    text(slide, bx + 7, cy + 61, bw - 20, 8, col, 6, BLACK, true);
    rect(slide, bx + bw - 19, cy + 60, 12, 10, i === 2 ? RED : '#b9bcc2', i === 2 ? RED : '#b9bcc2', true);
    for (let j = 0; j < 3; j++) {
      const yy = cy + 78 + j * 29;
      rect(slide, bx + 6, yy, bw - 12, 22, WHITE, LINE, true);
      rect(slide, bx + 6, yy, 3, 22, j === 0 ? RED : '#bfbfbf', null, false);
      text(slide, bx + 13, yy + 4, bw - 25, 7, `案件 ${i + 1}-${j + 1}`, 5, BLACK, true);
      text(slide, bx + 13, yy + 12, bw - 25, 6, '期限 / 担当 / 状態', 4, MUTED, false);
    }
  });
  rect(slide, cx, cy + 181, cw * 0.55, 50, WHITE, LINE, true);
  text(slide, cx + 9, cy + 189, 100, 7, '直近対応履歴', 6, BLACK, true);
  ['退去立会い', '見積確認', '契約更新'].forEach((r, i) => {
    const yy = cy + 204 + i * 10;
    ellipse(slide, cx + 10, yy, 5, 5, i === 0 ? RED : '#a9a9a9', null);
    text(slide, cx + 20, yy - 2, 76, 6, r, 4, MUTED, false);
    rect(slide, cx + 120, yy, 35, 3, '#d7d7d7', null, false);
    rect(slide, cx + 170, yy, 28, 3, '#d7d7d7', null, false);
  });
  rect(slide, cx + cw * 0.58, cy + 181, cw * 0.42, 50, WHITE, LINE, true);
  ellipse(slide, cx + cw * 0.62, cy + 195, 28, 28, RED, RED);
  ellipse(slide, cx + cw * 0.635, cy + 202, 15, 15, WHITE, WHITE);
  text(slide, cx + cw * 0.72, cy + 195, 85, 8, '対応種別の内訳', 6, BLACK, true);
  ['退去', '契約', '請求'].forEach((r, i) => {
    ellipse(slide, cx + cw * 0.72, cy + 209 + i * 10, 5, 5, i === 0 ? RED : '#b9bcc2', null);
    text(slide, cx + cw * 0.74, cy + 207 + i * 10, 52, 6, r, 4, MUTED, false);
  });
}

function mockOverview(slide, page) {
  artTitle(slide, '02', 'Chapter2', '改善版モックで提示する全体像', page);
  dashboardUi(slide, 68, 92, 484, 264);
  rect(slide, 570, 96, 122, 78, WHITE, LINE, true);
  ellipse(slide, 582, 112, 28, 28, LIGHT_RED, LIGHT_RED);
  text(slide, 591, 119, 10, 10, '1', 10, RED, true, SlidesApp.ParagraphAlignment.CENTER);
  text(slide, 619, 111, 58, 11, '実運用に近い', 8, RED, true);
  text(slide, 619, 128, 58, 21, '左サイドバーを残し、日常利用を想像しやすくします。', 6, MUTED, false);
  rect(slide, 570, 188, 122, 78, WHITE, LINE, true);
  ellipse(slide, 582, 204, 28, 28, LIGHT_RED, LIGHT_RED);
  text(slide, 591, 211, 10, 10, '2', 10, RED, true, SlidesApp.ParagraphAlignment.CENTER);
  text(slide, 619, 203, 58, 11, '稟議で比較しやすい', 8, RED, true);
  text(slide, 619, 220, 58, 21, '期限・担当・状態・リスクを画面単位で説明します。', 6, MUTED, false);
  rect(slide, 570, 280, 122, 76, WHITE, LINE, true);
  ellipse(slide, 582, 296, 28, 28, LIGHT_RED, LIGHT_RED);
  text(slide, 591, 303, 10, 10, '3', 10, RED, true, SlidesApp.ParagraphAlignment.CENTER);
  text(slide, 619, 295, 58, 11, '要件化しやすい', 8, RED, true);
  text(slide, 619, 312, 58, 21, '画面から機能・データ項目・運用を確認できます。', 6, MUTED, false);
}

function screenshotDashboard(slide, page) {
  artTitle(slide, '02', 'Chapter2', 'スクショ資料1：基幹管理ダッシュボード', page);
  dashboardUi(slide, 68, 92, 494, 264);
  rect(slide, 580, 98, 112, 258, WHITE, LINE, true);
  text(slide, 596, 111, 70, 12, '主な機能', 10, RED, true);
  checkItem(slide, 592, 143, '期限・リスク', '本日期限と遅延リスクを可視化');
  checkItem(slide, 592, 201, '絞り込み', '担当者別・案件種別別に確認');
  checkItem(slide, 592, 259, '履歴連携', '対応履歴と関連書類を紐づけ');
}

function detailUi(slide, x, y, w, h) {
  appShell(slide, x, y, w, h, '物件・契約詳細');
  const cx = x + 98, cy = y + 42;
  rect(slide, cx, cy, 114, 70, GRAY, LINE, true);
  text(slide, cx + 8, cy + 8, 52, 10, '物件情報', 8, BLACK, true);
  text(slide, cx + 8, cy + 26, 88, 38, '所在地　東京都〇〇区\n契約状況　更新確認中\n担当者　営業部 A様\n優先度　高', 6, TEXT, false);
  rect(slide, cx + 151, cy + 13, 2, 154, '#d1d1d1', null, false);
  [['受付', '問い合わせを自動登録'], ['確認', '担当者が内容確認'], ['承認', '上長承認・通知'], ['完了', '対応履歴として保存']].forEach((r, i) => {
    const yy = cy + 18 + i * 40;
    ellipse(slide, cx + 145, yy - 6, 14, 14, i < 3 ? RED : '#bdbdbd', null);
    text(slide, cx + 169, yy - 9, 40, 10, r[0], 8, BLACK, true);
    text(slide, cx + 169, yy + 4, 80, 8, r[1], 6, MUTED, false);
  });
  const px = x + w - 135;
  rect(slide, px, cy, 120, h - 56, GRAY, LINE, true);
  text(slide, px + 9, cy + 8, 80, 10, '関連書類 / メモ', 8, BLACK, true);
  ['契約書ドラフト', '見積依頼', '入居者様問い合わせ', 'オーナー様報告メモ', '過去対応履歴'].forEach((r, i) => {
    rect(slide, px + 9, cy + 29 + i * 25, 100, 17, WHITE, LINE, true);
    text(slide, px + 16, cy + 33 + i * 25, 76, 8, r, 6, BLACK, true);
  });
}

function screenshotDetail(slide, page) {
  artTitle(slide, '02', 'Chapter2', 'スクショ資料2：物件・契約ごとの進捗管理', page);
  detailUi(slide, 68, 92, 494, 264);
  rect(slide, 580, 98, 112, 258, WHITE, LINE, true);
  text(slide, 596, 111, 70, 12, '主な機能', 10, RED, true);
  checkItem(slide, 592, 143, '一画面管理', '物件・契約・履歴を確認');
  checkItem(slide, 592, 201, '進捗管理', '承認から完了まで可視化');
  checkItem(slide, 592, 259, '書類連携', '契約書自動作成へ接続');
}

function searchUi(slide, x, y, w, h) {
  appShell(slide, x, y, w, h, '社内FAQ・横断検索');
  const cx = x + 98, cy = y + 42;
  rect(slide, cx, cy, w - 116, 27, GRAY, LINE, true);
  text(slide, cx + 9, cy + 8, 200, 10, '契約更新時の注意点を検索', 8, BLACK, true);
  [['社内FAQ', '更新案内、請求、インボイス対応の社内手順を提示'], ['契約書', '関連条文と過去のドラフトを候補表示'], ['対応履歴', '類似案件の入居者様対応履歴を要約'], ['オーナー報告', '訪問前に物件・収支・過去提案を整理']].forEach((r, i) => {
    const bx = cx + (i % 2) * 161;
    const by = cy + 45 + Math.floor(i / 2) * 68;
    rect(slide, bx, by, 146, 52, WHITE, LINE, true);
    rect(slide, bx + 8, by + 7, 56, 14, LIGHT_RED, LIGHT_RED, true);
    text(slide, bx + 10, by + 10, 48, 6, r[0], 6, RED, true);
    text(slide, bx + 9, by + 28, 124, 15, r[1], 6, TEXT, false);
  });
}

function screenshotSearch(slide, page) {
  artTitle(slide, '02', 'Chapter2', 'スクショ資料3：社内FAQ・横断検索', page);
  searchUi(slide, 68, 92, 494, 264);
  rect(slide, 580, 98, 112, 258, WHITE, LINE, true);
  text(slide, 596, 111, 70, 12, '拡張時の価値', 10, RED, true);
  checkItem(slide, 592, 143, '横断検索', '契約書・規程・履歴を検索');
  checkItem(slide, 592, 201, '属人化軽減', '担当者ごとの差を小さくする');
  checkItem(slide, 592, 259, 'AI活用', '問い合わせ・営業準備に展開');
}

function roadmap(slide, page) {
  title(slide, 'Chapter3', '今後の進め方のイメージ');
  text(slide, 39, 66, 640, 24, '繁忙期であると推察されますので、できる限り現場の混乱を避け円滑に進めるため、下記のような流れで進めさせていただければ幸いです。', 10, BLACK, true);
  rect(slide, 37, 111, 660, 280, WHITE, null, true);
  const steps = [['01', 'ご契約'], ['02', '進め方の確認'], ['03', 'データ移行先の準備'], ['04', 'エージェント開発'], ['05', '現場導入'], ['06', '改善']];
  steps.forEach((s, i) => {
    const x = 75 + i * 105;
    ellipse(slide, x, 126, 56, 56, WHITE, '#d6d6d6');
    ellipse(slide, x + 5, 131, 46, 46, null, '#ff7474');
    text(slide, x + 14, 146, 30, 20, s[0], 18, RED, true, SlidesApp.ParagraphAlignment.CENTER);
    if (i < 5) rect(slide, x + 62, 153, 42, 2, '#ff7474', null, false);
    arrow(slide, x - 28, 190, 101, 34, RED);
    text(slide, x - 15, 199, 70, 13, s[1], 8, WHITE, true, SlidesApp.ParagraphAlignment.CENTER);
  });
  const bodies = [
    'NDAや個別契約など\n各種ご契約を結ばせて\nいただきます。',
    'データ整理の必要可否も含め、\n現場の混乱を起こさないように\n詳細プランをすり合わせます。',
    'データ移行を同時並行で行う場合、\n移行先を先に準備することが\n最重要です。',
    '弊社でエージェントを開発。\n毎週報告しながら使用感やUIを\nすり合わせます。',
    '小規模テスト運用後、\n本格的に現場導入。\n必要に応じてレクチャーします。',
    '定期的なご報告会を設け、\n細かいアップデートを行い\n定着まで伴走します。',
  ];
  bodies.forEach((b, i) => text(slide, 53 + i * 109, 246, 96, 95, b, 7, BLACK, false));
  footer(slide, page);
}

function comparison(slide, page) {
  title(slide, 'Chapter3', '他社比較・社内稟議での判断軸');
  pill(slide, 34, 79, 126, 24, '判断軸');
  pill(slide, 174, 79, 214, 24, '一般的なパッケージ導入');
  pill(slide, 407, 79, 259, 24, 'Field Xで開発する場合');
  const rows = [
    ['業務適合', '既存機能に業務を寄せる必要がある', '貴社の業務フロー・承認・帳票に合わせて設計'],
    ['現場定着', '画面や操作が合わず利用が限定される可能性', '担当者様の使い方を前提にモックから改善'],
    ['AI拡張', '個別AI連携は追加開発・制約が出やすい', '基幹データを起点にAI音声対応・営業支援AIまで展開'],
    ['社内説明', '導入効果や運用イメージを別途整理する必要', 'スクショ資料・要件資料・進め方を一式で提示'],
  ];
  rows.forEach((r, i) => {
    const y = 118 + i * 52;
    rect(slide, 34, y, 126, 44, GRAY, LINE, true);
    rect(slide, 174, y, 214, 44, GRAY, LINE, true);
    rect(slide, 407, y, 259, 44, LIGHT_RED, RED, true);
    text(slide, 44, y + 14, 70, 12, r[0], 10, BLACK, true);
    text(slide, 185, y + 10, 188, 20, r[1], 8, TEXT, false);
    text(slide, 419, y + 10, 230, 20, r[2], 8, TEXT, false);
  });
  footer(slide, page);
}

function futureAi(slide, page) {
  title(slide, 'Chapter3', '基幹管理システムを起点に、社内AIへ展開可能');
  dashboardUi(slide, 43, 88, 288, 229);
  ellipse(slide, 402, 188, 94, 45, RED, RED);
  text(slide, 416, 198, 66, 18, '基幹データ\n社内AI基盤', 9, WHITE, true, SlidesApp.ParagraphAlignment.CENTER);
  [['AI音声対応', '入居者様問い合わせ', 349, 101], ['営業支援AI', '訪問前ブリーフィング', 497, 101], ['契約書自動作成', '文書作成を省力化', 349, 276], ['社内FAQ検索', '横断検索・ナレッジ化', 497, 276]].forEach(r => {
    rect(slide, r[2], r[3], 107, 42, GRAY, LINE, true);
    text(slide, r[2] + 8, r[3] + 9, 82, 10, r[0], 8, RED, true);
    text(slide, r[2] + 8, r[3] + 25, 82, 8, r[1], 6, TEXT, false);
  });
  pill(slide, 566, 161, 101, 24, '展開イメージ');
  text(slide, 566, 195, 120, 100, bullets(['入居者様問い合わせの一次対応', 'オーナー様訪問前の情報整理', '契約書・通知文の下書き', '社内情報を便利FAQ化']), 8, BLACK, true);
  footer(slide, page);
}

function nextActions(slide, page) {
  title(slide, 'Next', '今後ご提示予定の資料');
  [['01', '改善版モック', '今回いただいたご意見を反映し、画面・操作・ステータスの見え方を作り込みます。'], ['02', '機能・要件説明資料', 'スクリーンショットごとに、必要機能・データ項目・運用イメージを整理します。'], ['03', '開発計画', 'ご契約後の要件定義、設計、開発、テスト、導入、改善の流れを具体化します。']].forEach((r, i) => {
    const y = 92 + i * 81;
    text(slide, 53, y, 34, 24, r[0], 20, RED, true);
    text(slide, 107, y + 3, 210, 18, r[1], 14, BLACK, true);
    text(slide, 109, y + 29, 460, 20, r[2], 10, MUTED, false);
  });
  rect(slide, 45, 335, 615, 29, RED, RED, true);
  text(slide, 56, 343, 562, 12, 'まずは、社内稟議・他社比較で使える状態まで、モックと画面別説明資料を整えます。', 10, WHITE, true);
  footer(slide, page);
}
