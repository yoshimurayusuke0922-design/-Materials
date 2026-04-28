#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const GS_W = 720;
const GS_H = 405;
const HTML_W = 1672;
const HTML_H = 941;
const RED = "#f80612";
const RED_DEEP = "#d9000b";
const RED_SOFT = "#ffe7e8";
const INK = "#101214";
const TEXT = "#2d3338";
const MUTED = "#687079";
const LINE = "#d9dde2";
const BG = "#f7f7f6";
const WHITE = "#ffffff";

function argValue(name, fallback) {
  const index = process.argv.indexOf(name);
  if (index >= 0 && process.argv[index + 1]) return process.argv[index + 1];
  return fallback;
}

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function sx(v) {
  return Math.round((v / HTML_W) * GS_W * 100) / 100;
}

function sy(v) {
  return Math.round((v / HTML_H) * GS_H * 100) / 100;
}

function fsPt(px) {
  return Math.max(6, Math.round((px / HTML_H) * GS_H * 1.12));
}

function text(text, x, y, width, height, options = {}) {
  return {
    type: "text",
    role: options.role || "body",
    text: text || "",
    x: sx(x),
    y: sy(y),
    width: sx(width),
    height: sy(height),
    font_size: options.font_size || fsPt(options.source_font_px || 18),
    bold: options.bold !== false,
    color: options.color || INK,
    align: options.align || "left",
    valign: options.valign || "top",
    font_family: options.font_family || "Yu Gothic",
  };
}

function shape(shapeName, x, y, width, height, options = {}) {
  return {
    type: "shape",
    role: options.role || "shape",
    shape: shapeName || "rectangle",
    x: sx(x),
    y: sy(y),
    width: sx(width),
    height: sy(height),
    fill: options.fill ?? WHITE,
    border: options.border ?? "transparent",
    border_width: options.border_width ?? 1,
    radius: options.radius || 0,
  };
}

function line(x1, y1, x2, y2, options = {}) {
  return {
    type: "line",
    role: options.role || "line",
    x1: sx(x1),
    y1: sy(y1),
    x2: sx(x2),
    y2: sy(y2),
    color: options.color || RED,
    width: options.width || 1.5,
  };
}

function image(src, x, y, width, height, options = {}) {
  return {
    type: "image",
    role: options.role || "image",
    src,
    x: sx(x),
    y: sy(y),
    width: sx(width),
    height: sy(height),
    crop: options.crop || "contain",
  };
}

function sourceRel(src) {
  if (!src) return "";
  return src.replace(/^\.\//, "");
}

function firstText(slide, predicate) {
  const block = (slide.text_blocks || []).find(predicate);
  return block ? block.text : "";
}

function h(slide, level, index = 0) {
  return ((slide.headings || []).filter((item) => item.level === level)[index] || {}).text || "";
}

function cardHeading(slide, index) {
  return (slide.cards[index] || {}).heading || "";
}

function cardBody(slide, index) {
  const card = slide.cards[index] || {};
  const pieces = [];
  if (card.paragraphs) pieces.push(...card.paragraphs);
  if (card.bullets) pieces.push(...card.bullets.map((item) => `• ${item}`));
  return pieces.join("\n");
}

function cardImage(slide, index) {
  const card = slide.cards[index] || {};
  return sourceRel((card.images || [])[0] || "");
}

function rail(elements, chapter, page) {
  elements.push(shape("rectangle", 0, 0, 74, 941, { fill: RED, border: RED, role: "side_rail" }));
  elements.push(text(chapter || "", 0, 90, 74, 36, { source_font_px: 16, color: WHITE, bold: true, align: "center", role: "rail_chapter" }));
  elements.push(text("Copyright @Field X inc.\nAll rights reserved.", -153, 640, 380, 42, { source_font_px: 16, color: WHITE, bold: true, align: "center", role: "rail_copyright" }));
  elements[elements.length - 1].rotation = 90;
  elements.push(text(String(page || ""), 0, 850, 74, 54, { source_font_px: 36, color: WHITE, bold: true, align: "center", role: "rail_page" }));
}

function addTitleBlock(elements, chapter, titleText, x = 130, y = 66, w = 1280, hBox = 78, size = 58) {
  elements.push(text(chapter, x, y - 36, 250, 34, { source_font_px: 28, color: RED, bold: true, role: "chapter_label" }));
  elements.push(text(titleText, x, y, w, hBox, { source_font_px: size, color: INK, bold: true, role: "title" }));
}

function cover(slide) {
  const elements = [];
  const coverTitle = h(slide, "h1").replace(/\n+/g, "\n");
  elements.push(shape("ellipse", 1180, -58, 760, 1060, { fill: RED, border: RED, role: "cover_right_blob" }));
  elements.push(shape("ellipse", -95, 735, 680, 300, { fill: RED, border: RED, role: "cover_bottom_blob" }));
  elements.push(shape("ellipse", 620, -156, 430, 360, { fill: "#ffc9cc", border: "transparent", role: "cover_top_glow" }));
  elements.push(text(firstText(slide, (b) => b.classes.includes("recipient")), 76, 228, 720, 50, { source_font_px: 28, color: INK, bold: true, role: "recipient" }));
  elements.push(text(coverTitle, 76, 350, 1040, 180, { source_font_px: 49, color: INK, bold: true, role: "title" }));
  elements.push(text(firstText(slide, (b) => b.classes.includes("cover-date")), 76, 632, 360, 44, { source_font_px: 27, color: INK, bold: false, role: "date" }));
  const logo = (slide.images || []).find((item) => /fieldx_logo_full/.test(item.src || ""));
  if (logo) elements.push(image(sourceRel(logo.src), 700, 770, 330, 80, { role: "logo" }));
  return { background: BG, elements };
}

function agenda(slide) {
  const elements = [];
  elements.push(shape("rectangle", 0, 0, 1672, 18, { fill: RED, border: RED, role: "top_line" }));
  elements.push(shape("ellipse", 1468, -42, 350, 420, { fill: "#ffd3d5", border: "transparent", role: "corner_glow" }));
  elements.push(shape("ellipse", -138, 760, 470, 310, { fill: RED, border: RED, role: "bottom_blob" }));
  elements.push(text("Contents", 96, 112, 320, 42, { source_font_px: 28, color: RED, bold: true, role: "chapter_label" }));
  elements.push(text(h(slide, "h2"), 96, 160, 600, 80, { source_font_px: 68, color: INK, bold: true, role: "title" }));
  const xs = [138, 568, 998];
  for (let i = 0; i < 3; i += 1) {
    const card = slide.cards[i] || {};
    const x = xs[i];
    elements.push(shape("roundRectangle", x, 385, 392, 455, { fill: WHITE, border: LINE, role: "agenda_card" }));
    elements.push(shape("ellipse", x + 132, 431, 128, 128, { fill: RED, border: RED, role: "agenda_number_circle" }));
    elements.push(text(String(i + 1).padStart(2, "0"), x + 132, 453, 128, 74, { source_font_px: 54, color: WHITE, bold: true, align: "center", role: "agenda_number" }));
    elements.push(shape("rectangle", x + 40, 593, 312, 3, { fill: RED, border: RED, role: "agenda_rule" }));
    elements.push(text(card.heading || "", x + 38, 634, 316, 78, { source_font_px: i === 0 ? 27 : 30, color: INK, bold: true, align: "center", role: "heading" }));
    elements.push(text((card.paragraphs || []).join("\n"), x + 36, 735, 320, 82, { source_font_px: 19, color: TEXT, bold: true, align: "center", role: "body" }));
  }
  return { background: BG, elements };
}

function divider(slide, no, titleY = 488, noX = 190, noY = 300) {
  const elements = [];
  elements.push(text(no, noX, noY, 260, 190, { source_font_px: 218, color: "#ff9ca1", bold: true, role: "divider_number" }));
  elements.push(text(h(slide, "h2"), 445, titleY, 980, 78, { source_font_px: 56, color: WHITE, bold: true, role: "title" }));
  elements.push(shape("rectangle", 445, titleY + 96, no === "03" ? 230 : 72, 4, { fill: WHITE, border: WHITE, role: "divider_rule" }));
  return { background: RED, elements };
}

function proposalSummary(slide) {
  const elements = [];
  rail(elements, "Chapter1", 4);
  elements.push(shape("ellipse", 1460, -92, 330, 330, { fill: "#ffd7d9", border: "transparent", role: "corner_glow" }));
  elements.push(shape("ellipse", 1538, 32, 338, 520, { fill: RED, border: RED, role: "right_blob" }));
  addTitleBlock(elements, "Chapter1", h(slide, "h2"), 130, 66, 980, 80, 58);
  elements.push(shape("roundRectangle", 218, 185, 1238, 64, { fill: RED, border: RED, role: "red_band" }));
  elements.push(text(firstText(slide, (b) => b.classes.includes("red-band")), 240, 197, 1195, 40, { source_font_px: 27, color: WHITE, bold: true, align: "center", role: "message" }));
  const xs = [130, 500, 870, 1240];
  for (let i = 0; i < 4; i += 1) {
    const x = xs[i];
    elements.push(shape("roundRectangle", x, 275, 330, 370, { fill: WHITE, border: LINE, role: "proposal_card" }));
    elements.push(shape("ellipse", x + 111, 294, 108, 108, { fill: RED_SOFT, border: "transparent", role: "icon_circle" }));
    if (cardImage(slide, i)) elements.push(image(cardImage(slide, i), x + 117, 300, 96, 96, { role: "icon" }));
    elements.push(text(cardHeading(slide, i), x + 25, 420, 280, 70, { source_font_px: 24, color: INK, bold: true, align: "center", role: "heading" }));
    elements.push(shape("rectangle", x + 145, 504, 40, 4, { fill: RED, border: RED, role: "short_rule" }));
    elements.push(text(cardBody(slide, i), x + 26, 528, 278, 94, { source_font_px: 15.7, color: TEXT, bold: true, align: "center", role: "body" }));
  }
  elements.push(shape("roundRectangle", 158, 686, 1360, 102, { fill: "#fff3f3", border: RED, border_width: 2, role: "message_bar" }));
  elements.push(shape("ellipse", 208, 698, 78, 78, { fill: RED, border: RED, role: "check_icon" }));
  elements.push(text("✓", 220, 704, 54, 54, { source_font_px: 44, color: WHITE, bold: true, align: "center", role: "check_mark" }));
  elements.push(text(firstText(slide, (b) => b.classes.includes("message-bar")), 340, 704, 1080, 70, { source_font_px: 25, color: INK, bold: true, align: "center", role: "message" }));
  return { background: BG, elements };
}

function demoOne(slide) {
  const elements = [];
  rail(elements, "Chapter2", 6);
  addTitleBlock(elements, "Chapter2", h(slide, "h2"), 122, 56, 1020, 62, 58);
  elements.push(text((slide.body || [])[0] || "", 122, 132, 1080, 42, { source_font_px: 16, color: TEXT, bold: true, role: "lead" }));
  elements.push(shape("roundRectangle", 122, 174, 1050, 620, { fill: WHITE, border: "#cfd4d9", role: "screenshot_placeholder" }));
  const shot = (slide.images || []).find((item) => item.role === "css-background-image");
  if (shot && shot.exists) elements.push(image(sourceRel(shot.src), 142, 194, 1010, 580, { role: "screenshot" }));
  const cards = slide.cards || [];
  for (let i = 0; i < 3; i += 1) {
    const y = 174 + i * 158;
    elements.push(shape("roundRectangle", 1196, y, 330, 140, { fill: WHITE, border: LINE, role: "demo_callout" }));
    const imgSrc = cardImage(slide, i);
    elements.push(shape("ellipse", 1212, y + 27, 86, 86, { fill: RED_SOFT, border: "transparent", role: "icon_circle" }));
    if (imgSrc) elements.push(image(imgSrc, 1216, y + 31, 78, 78, { role: "icon" }));
    elements.push(text((cards[i] || {}).heading || "", 1310, y + 20, 190, 34, { source_font_px: 21, color: RED, bold: true, role: "heading" }));
    elements.push(text(cardBody(slide, i), 1310, y + 62, 190, 55, { source_font_px: 14, color: TEXT, bold: true, role: "body" }));
  }
  elements.push(text((slide.body || []).slice(-1)[0] || "", 960, 855, 560, 26, { source_font_px: 15, color: MUTED, bold: true, role: "note" }));
  return { background: BG, elements };
}

function demoTwo(slide) {
  const elements = [];
  rail(elements, "Chapter2", 7);
  addTitleBlock(elements, "Chapter2", h(slide, "h2"), 122, 56, 1280, 64, 48);
  elements.push(text((slide.body || [])[0] || "", 122, 132, 1180, 42, { source_font_px: 18, color: TEXT, bold: true, role: "lead" }));
  elements.push(shape("roundRectangle", 122, 182, 740, 630, { fill: WHITE, border: "#cfd4d9", border_width: 2, role: "pc_screenshot_placeholder" }));
  elements.push(shape("roundRectangle", 886, 182, 280, 630, { fill: "#fbfbfb", border: "#e7e7e7", border_width: 10, role: "phone_frame" }));
  elements.push(shape("roundRectangle", 932, 182, 118, 28, { fill: "#e7e7e7", border: "#e7e7e7", role: "phone_notch" }));
  elements.push(shape("roundRectangle", 914, 232, 224, 560, { fill: WHITE, border: "#cfd4d9", border_width: 2, role: "phone_inner" }));
  const shots = (slide.images || []).filter((item) => item.role === "css-background-image");
  if (shots[0] && shots[0].exists) elements.push(image(sourceRel(shots[0].src), 142, 202, 700, 590, { role: "pc_screenshot" }));
  if (shots[1] && shots[1].exists) elements.push(image(sourceRel(shots[1].src), 914, 232, 224, 560, { role: "phone_screenshot" }));
  for (let i = 0; i < 3; i += 1) {
    const y = 182 + i * 186;
    elements.push(shape("roundRectangle", 1190, y, 380, 168, { fill: WHITE, border: LINE, role: "feature_row" }));
    const imgSrc = cardImage(slide, i);
    elements.push(shape("ellipse", 1210, y + 41, 86, 86, { fill: RED_SOFT, border: "transparent", role: "icon_circle" }));
    if (imgSrc) elements.push(image(imgSrc, 1214, y + 45, 78, 78, { role: "icon" }));
    elements.push(text(cardHeading(slide, i), 1318, y + 28, 218, 46, { source_font_px: i === 1 ? 19 : 21, color: RED, bold: true, role: "heading" }));
    elements.push(text(cardBody(slide, i), 1318, y + 80, 218, 62, { source_font_px: 14, color: TEXT, bold: true, role: "body" }));
  }
  return { background: BG, elements };
}

function demoThree(slide) {
  const elements = [];
  rail(elements, "Chapter2", 8);
  addTitleBlock(elements, "Chapter2", h(slide, "h2"), 122, 56, 1370, 58, 43);
  elements.push(text((slide.body || [])[0] || "", 122, 126, 1330, 48, { source_font_px: 18, color: TEXT, bold: true, role: "lead" }));
  const xs = [122, 870, 122, 870];
  const ys = [202, 202, 530, 530];
  const shots = (slide.images || []).filter((item) => item.role === "css-background-image");
  for (let i = 0; i < 4; i += 1) {
    const x = xs[i];
    const y = ys[i];
    elements.push(shape("rectangle", x, y, 7, 34, { fill: RED, border: RED, role: "heading_mark" }));
    elements.push(text(((slide.headings || []).filter((item) => item.level === "h3")[i] || {}).text || "", x + 28, y - 4, 650, 42, { source_font_px: i === 3 ? 20.5 : 25, color: INK, bold: true, role: "heading" }));
    elements.push(shape("roundRectangle", x, y + 52, 680, 305, { fill: WHITE, border: "#cfd4d9", role: "screenshot_placeholder" }));
    if (shots[i] && shots[i].exists) elements.push(image(sourceRel(shots[i].src), x + 12, y + 64, 656, 281, { role: "screenshot" }));
  }
  return { background: BG, elements };
}

function future(slide) {
  const elements = [];
  rail(elements, "Chapter3", 10);
  addTitleBlock(elements, "Chapter3", h(slide, "h2"), 130, 56, 1280, 60, 58);
  elements.push(text((slide.body || [])[0] || "", 130, 128, 1300, 54, { source_font_px: 23, color: TEXT, bold: true, role: "lead" }));
  line(560, 275, 690, 370, { color: RED, width: 1.5 });
  const hubImg = (slide.images || []).find((item) => /generated\/17/.test(item.src || ""));
  const cardPositions = [
    [130, 230],
    [1000, 230],
    [130, 550],
    [1000, 550],
  ];
  for (let i = 0; i < 4; i += 1) {
    const [x, y] = cardPositions[i];
    elements.push(shape("roundRectangle", x, y, 474, 132, { fill: WHITE, border: LINE, role: "future_card" }));
    const imgSrc = cardImage(slide, i);
    elements.push(shape("ellipse", x + 24, y + 23, 86, 86, { fill: RED_SOFT, border: "transparent", role: "icon_circle" }));
    if (imgSrc) elements.push(image(imgSrc, x + 28, y + 27, 78, 78, { role: "icon" }));
    elements.push(text(cardHeading(slide, i), x + 135, y + 20, 300, 42, { source_font_px: 24, color: INK, bold: true, role: "heading" }));
    elements.push(shape("rectangle", x + 135, y + 74, 145, 2, { fill: RED, border: RED, role: "card_rule" }));
    elements.push(text(cardBody(slide, i), x + 135, y + 84, 305, 40, { source_font_px: 14.2, color: TEXT, bold: true, role: "body" }));
  }
  elements.push(shape("ellipse", 728, 354, 216, 216, { fill: RED, border: WHITE, border_width: 14, role: "future_hub" }));
  if (hubImg) elements.push(image(sourceRel(hubImg.src), 776, 376, 120, 120, { role: "hub_image" }));
  elements.push(text(firstText(slide, (b) => b.classes.includes("future-hub")) || "基幹データ", 728, 488, 216, 50, { source_font_px: 30, color: WHITE, bold: true, align: "center", role: "hub_label" }));
  elements.push(shape("roundRectangle", 158, 810, 1340, 84, { fill: "#fff3f3", border: RED, border_width: 2, role: "message_bar" }));
  elements.push(text(firstText(slide, (b) => b.classes.includes("message-bar")), 250, 824, 1160, 50, { source_font_px: 22, color: INK, bold: true, align: "center", role: "message" }));
  return { background: BG, elements };
}

function roadmap(slide) {
  const elements = [];
  rail(elements, "Chapter3", 11);
  elements.push(text("Chapter3", 128, 48, 260, 34, { source_font_px: 28, color: RED, bold: true, role: "chapter_label" }));
  elements.push(text(h(slide, "h2"), 128, 88, 720, 60, { source_font_px: 54, color: INK, bold: true, role: "title" }));
  elements.push(text((slide.body || [])[0] || "", 128, 165, 1300, 54, { source_font_px: 21, color: TEXT, bold: true, role: "lead" }));
  elements.push(shape("roundRectangle", 128, 255, 1420, 630, { fill: WHITE, border: "transparent", role: "roadmap_panel" }));
  const labels = ((slide.text_blocks || []).find((b) => b.classes.includes("road-labels")) || {}).text;
  const labelList = labels ? labels.split(/\n|(?<=。)/).filter(Boolean) : ["ご契約", "進め方の確認", "移行先基盤の準備", "システム開発", "現場導入", "改善"];
  const cards = (slide.text_blocks || []).filter((b) => b.classes.includes("road-line")).map((b) => b.text);
  const x0 = 190;
  const gap = 214;
  for (let i = 0; i < 6; i += 1) {
    const x = x0 + i * gap;
    elements.push(shape("ellipse", x, 299, 112, 112, { fill: WHITE, border: "#e8e8e8", border_width: 4, role: "road_number_circle" }));
    elements.push(text(String(i + 1).padStart(2, "0"), x, 326, 112, 56, { source_font_px: 42, color: RED, bold: true, align: "center", role: "road_number" }));
    if (i < 5) elements.push(line(x + 112, 355, x + gap, 355, { color: "#ff7474", width: 2 }));
    elements.push(shape("rightArrow", x - 50, 440, 188, 84, { fill: RED, border: RED, role: "road_label" }));
    elements.push(text(labelList[i] || "", x - 40, 455, 166, 52, { source_font_px: 22, color: WHITE, bold: true, align: "center", role: "heading" }));
    elements.push(shape("roundRectangle", x - 40, 558, 188, 242, { fill: "#fff7f7", border: "#f2cfd2", role: "road_copy_box" }));
    elements.push(shape("rectangle", x - 40, 558, 5, 242, { fill: RED, border: RED, role: "road_copy_accent" }));
    elements.push(text(cards[i] || (slide.body || [])[i + 1] || "", x - 25, 575, 156, 200, { source_font_px: 15.3, color: "#24282c", bold: true, role: "body" }));
  }
  return { background: BG, elements };
}

function subsidy(slide) {
  const elements = [];
  rail(elements, "Chapter3", 12);
  elements.push(text("Chapter3", 126, 58, 250, 34, { source_font_px: 28, color: RED, bold: true, role: "chapter_label" }));
  elements.push(text(h(slide, "h2"), 126, 98, 1300, 62, { source_font_px: 48, color: INK, bold: true, role: "title" }));
  elements.push(text((slide.body || [])[0] || "", 126, 178, 1280, 44, { source_font_px: 22, color: TEXT, bold: true, role: "lead" }));
  const xs = [126, 900];
  for (let i = 0; i < 2; i += 1) {
    const x = xs[i];
    elements.push(shape("roundRectangle", x, 270, 610, 376, { fill: WHITE, border: LINE, role: "subsidy_card" }));
    const imgSrc = cardImage(slide, i);
    elements.push(shape("ellipse", x + 38, 298, 98, 98, { fill: RED_SOFT, border: "transparent", role: "icon_circle" }));
    if (imgSrc) elements.push(image(imgSrc, x + 45, 305, 84, 84, { role: "icon" }));
    elements.push(text(cardHeading(slide, i), x + 158, 292, 390, 82, { source_font_px: 28, color: INK, bold: true, role: "heading" }));
    elements.push(shape("rectangle", x + 36, 414, 538, 4, { fill: RED, border: RED, role: "card_rule" }));
    elements.push(text(cardBody(slide, i), x + 38, 442, 536, 112, { source_font_px: 19.5, color: TEXT, bold: true, role: "body" }));
    if (i === 0) {
      const amount = firstText(slide, (b) => b.classes.includes("amount-box"));
      elements.push(shape("roundRectangle", x + 44, 570, 522, 76, { fill: "#ffe5e6", border: "transparent", role: "amount_box" }));
      elements.push(text(amount, x + 60, 585, 490, 46, { source_font_px: 26, color: RED, bold: true, align: "center", role: "amount" }));
    } else {
      elements.push(shape("roundRectangle", x + 44, 570, 522, 76, { fill: "#ffe5e6", border: "transparent", role: "support_list_box" }));
      elements.push(text((slide.bullets || []).map((item) => `• ${item}`).join("\n"), x + 72, 582, 480, 54, { source_font_px: 18.5, color: INK, bold: true, role: "bullet_list" }));
    }
  }
  elements.push(shape("roundRectangle", 126, 812, 1320, 76, { fill: "#f0f0ef", border: "transparent", role: "note_bar" }));
  elements.push(shape("ellipse", 158, 828, 44, 44, { fill: "#666666", border: "#666666", role: "info_dot" }));
  elements.push(text("i", 158, 826, 44, 44, { source_font_px: 28, color: WHITE, bold: true, align: "center", role: "info" }));
  elements.push(text((slide.body || []).slice(-1)[0] || "", 230, 826, 1140, 46, { source_font_px: 17, color: "#24282c", bold: true, role: "note" }));
  return { background: BG, elements };
}

function fallback(slide) {
  const elements = [];
  if ((slide.classes || []).includes("with-rail")) rail(elements, "", slide.slide_number);
  elements.push(text(slide.title || slide.source_id, 120, 80, 1200, 70, { source_font_px: 48, color: INK, bold: true, role: "title" }));
  elements.push(text((slide.body || []).join("\n\n"), 120, 190, 1200, 560, { source_font_px: 22, color: TEXT, bold: true, role: "body" }));
  return { background: slide.background_color || BG, elements };
}

function buildSlide(slide) {
  const id = slide.source_id || "";
  if (id.includes("slide-01")) return cover(slide);
  if (id.includes("slide-02")) return agenda(slide);
  if (id.includes("slide-03")) return divider(slide, "01", 488, 190, 300);
  if (id.includes("slide-05")) return proposalSummary(slide);
  if (id.includes("slide-06")) return divider(slide, "02", 458, 126, 326);
  if (id.includes("slide-07")) return demoOne(slide);
  if (id.includes("slide-08")) return demoTwo(slide);
  if (id.includes("slide-09")) return demoThree(slide);
  if (id.includes("slide-10")) return divider(slide, "03", 438, 116, 306);
  if (id.includes("slide-11")) return future(slide);
  if (id.includes("slide-12")) return roadmap(slide);
  if (id.includes("slide-13")) return subsidy(slide);
  return fallback(slide);
}

function main() {
  const input = argValue("--input", "analysis/slide_structure.json");
  const outDir = argValue("--out", "intermediate");
  const structure = JSON.parse(fs.readFileSync(input, "utf8"));
  ensureDir(outDir);
  const plan = {
    schema_version: 1,
    title: "株式会社三幸 基幹管理システムのご提案",
    page: {
      width: GS_W,
      height: GS_H,
      unit: "PT",
      source_width_px: structure.source.slide_width_px || HTML_W,
      source_height_px: structure.source.slide_height_px || HTML_H,
    },
    brand: {
      red: RED,
      ink: INK,
      text: TEXT,
      background: BG,
      font_family: "Yu Gothic",
    },
    slides: structure.slides.map((slide) => ({
      slide_number: slide.slide_number,
      source_id: slide.source_id,
      source_file: slide.source_file,
      title: slide.title,
      ...buildSlide(slide),
    })),
  };
  const mapping = {
    source: structure.source,
    target: plan.page,
    scale: {
      x: GS_W / (structure.source.slide_width_px || HTML_W),
      y: GS_H / (structure.source.slide_height_px || HTML_H),
      font_rule: "source CSS px * target_height / source_height * 1.12",
    },
    decisions: [
      "本文・見出し・箇条書き・数値はGoogleスライドのtext要素として再生成する。",
      "カード、帯、サイドレール、区切り線はshape/line要素として再生成する。",
      "アイコン、ロゴ、複雑なイラスト、スクリーンショット枠の画像はimage要素として扱う。",
      "CSSグラデーション、影、clip-path、SVGの細かい破線はGoogleスライドの単純図形に近似する。",
    ],
  };
  fs.writeFileSync(path.join(outDir, "google_slides_plan.json"), `${JSON.stringify(plan, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(outDir, "layout_mapping.json"), `${JSON.stringify(mapping, null, 2)}\n`, "utf8");
  console.log(`Normalized ${plan.slides.length} slides`);
  console.log(path.join(outDir, "google_slides_plan.json"));
  console.log(path.join(outDir, "layout_mapping.json"));
}

if (require.main === module) main();

