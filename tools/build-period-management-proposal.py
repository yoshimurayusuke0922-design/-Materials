from __future__ import annotations

import shutil
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projects" / "2026-04-24-period-management-proposal"
REF = ROOT / "reference_slides" / "library" / "period-management-mock" / "slides"
OUT_IMAGES = PROJECT / "generated_backgrounds"
OUT_MOCKS = PROJECT / "source" / "mock_screens"
OUT_PPTX = PROJECT / "proposal_kikan_management_sanko.pptx"
OUT_PPTX_JA = PROJECT / "株式会社三幸_基幹管理システムご提案資料.pptx"

W, H = 1920, 1080
RED = (255, 24, 24)
DARK = (22, 22, 28)
BLACK = (18, 18, 18)
TEXT = (42, 42, 42)
MUTED = (96, 96, 96)
LINE = (222, 222, 222)
BG = (246, 246, 246)
LIGHT_RED = (255, 236, 236)
WHITE = (255, 255, 255)


def font_path() -> str:
    for path in [
        r"C:\Windows\Fonts\YuGothB.ttc",
        r"C:\Windows\Fonts\YuGothR.ttc",
        r"C:\Windows\Fonts\meiryob.ttc",
        r"C:\Windows\Fonts\meiryo.ttc",
        r"C:\Windows\Fonts\msgothic.ttc",
    ]:
        if Path(path).exists():
            return path
    return "arial.ttf"


FONT_PATH = font_path()


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    if bold:
        for candidate in [r"C:\Windows\Fonts\YuGothB.ttc", r"C:\Windows\Fonts\meiryob.ttc"]:
            if Path(candidate).exists():
                return ImageFont.truetype(candidate, size)
    return ImageFont.truetype(FONT_PATH, size)


F = {
    "tiny": font(20),
    "small": font(25),
    "small_b": font(25, True),
    "body": font(30),
    "body_b": font(30, True),
    "mid": font(38, True),
    "large": font(54, True),
    "xl": font(74, True),
    "num": font(178, True),
}


def measure(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont, width: int) -> list[str]:
    lines: list[str] = []
    for raw in text.split("\n"):
        current = ""
        for ch in raw:
            test = current + ch
            if draw.textlength(test, font=fnt) <= width or not current:
                current = test
            else:
                lines.append(current)
                current = ch
        if current:
            lines.append(current)
    return lines


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    fnt: ImageFont.FreeTypeFont,
    width: int,
    fill=BLACK,
    gap: int = 8,
) -> int:
    x, y = xy
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        _, h = measure(draw, line or "あ", fnt)
        y += h + gap
    return y


def rounded(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], radius: int, fill, outline=None, width: int = 1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def base() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (W, H), WHITE)
    return img, ImageDraw.Draw(img)


def footer(draw: ImageDraw.ImageDraw, page: int):
    draw.text((70, 1018), "Copyright @Field X inc. All rights reserved.", font=F["tiny"], fill=(125, 125, 125))
    draw.rectangle((1870, 0, W, H), fill=RED)
    draw.text((1886, 1012), str(page), font=F["small_b"], fill=WHITE)


def title(draw: ImageDraw.ImageDraw, chapter: str, heading: str):
    draw.text((82, 60), chapter, font=F["tiny"], fill=RED)
    draw.text((82, 94), heading, font=F["mid"], fill=BLACK)


def pill(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], label: str, fill=RED, color=WHITE):
    rounded(draw, box, 10, fill)
    tw, th = measure(draw, label, F["small_b"])
    draw.text((box[0] + (box[2] - box[0] - tw) // 2, box[1] + (box[3] - box[1] - th) // 2 - 2), label, font=F["small_b"], fill=color)


def bullets(draw: ImageDraw.ImageDraw, x: int, y: int, items: Iterable[str], width: int, fnt=None, gap: int = 14) -> int:
    fnt = fnt or F["body"]
    for item in items:
        draw.text((x, y + 1), "・", font=fnt, fill=RED)
        y = draw_wrapped(draw, (x + 30, y), item, fnt, width - 30, BLACK, 7) + gap
    return y


def fit_image(path: Path) -> Image.Image:
    source = Image.open(path).convert("RGB")
    img = Image.new("RGB", (W, H), WHITE)
    ratio = min(W / source.width, H / source.height)
    resized = source.resize((int(source.width * ratio), int(source.height * ratio)), Image.LANCZOS)
    img.paste(resized, ((W - resized.width) // 2, (H - resized.height) // 2))
    return img


def cover(page: int):
    img, draw = base()
    # Match the prior deck's opening visual: big red cropped circles and right rail.
    draw.ellipse((-360, -260, 330, 350), fill=RED)
    draw.ellipse((1370, -175, 2260, 720), fill=RED)
    draw.ellipse((-255, 810, 260, 1260), fill=RED)
    draw.text((90, 145), "株式会社三幸　御中", font=F["small"], fill=BLACK)
    draw.text((90, 255), "基幹管理システムの", font=F["xl"], fill=BLACK)
    draw.text((90, 355), "ご提案資料", font=F["xl"], fill=BLACK)
    draw.text((90, 505), "他社コンペ・社内稟議向け / モック改善版のご提案", font=F["mid"], fill=RED)
    draw.text((90, 618), "2026年04月25日", font=F["body_b"], fill=BLACK)
    draw.text((1320, 880), "Field X", font=font(68, True), fill=BLACK)
    footer(draw, page)
    return img


def agenda(page: int):
    img, draw = base()
    draw.text((90, 70), "AGENDA", font=F["tiny"], fill=RED)
    draw.text((90, 105), "目次", font=F["small_b"], fill=BLACK)
    items = [
        ("01", "これまでにお伺いしたこと", "モック確認後の社内稟議・他社比較に必要な前提整理"),
        ("02", "ご提案の要旨・デモンストレーション", "改善版モック、画面別要件、将来のAI活用イメージ"),
        ("03", "今後の進め方のイメージ", "要件定義から開発・現場導入・改善運用までの流れ"),
    ]
    y = 285
    for num, head, body in items:
        draw.text((525, y), num, font=F["large"], fill=RED)
        draw.text((690, y + 9), head, font=F["mid"], fill=RED)
        draw.text((695, y + 70), body, font=F["body"], fill=MUTED)
        y += 185
    footer(draw, page)
    return img


def chapter(page: int, num: str, heading: str):
    img = Image.new("RGB", (W, H), RED)
    draw = ImageDraw.Draw(img)
    draw.text((85, 395), num, font=F["num"], fill=(255, 166, 166))
    draw.text((380, 505), heading, font=F["large"], fill=WHITE)
    draw.text((70, 1018), "Copyright @Field X inc. All rights reserved.", font=F["tiny"], fill=(255, 220, 220))
    draw.text((1886, 1012), str(page), font=F["small_b"], fill=WHITE)
    return img


def card(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], heading: str, body: str):
    rounded(draw, box, 16, BG, (232, 232, 232))
    pill(draw, (box[0] + 22, box[1] + 22, box[2] - 22, box[1] + 78), heading)
    draw_wrapped(draw, (box[0] + 34, box[1] + 112), body, F["small"], box[2] - box[0] - 68, TEXT, 8)


def position_slide(page: int):
    img, draw = base()
    title(draw, "Chapter1", "本資料の位置づけ")
    pill(draw, (95, 202, 830, 265), "今回の目的")
    bullets(draw, 112, 315, [
        "担当者様にご確認いただいたモックを、社内稟議・他社コンペで比較しやすい資料に整理します。",
        "見積書は別途送付予定のため、本資料では開発範囲・機能・進め方・将来展開を中心に説明します。",
        "今回のご意見を反映し、画面単位で要件と機能が分かる改善版モックとして提出します。",
    ], 760, F["body"], 15)
    pill(draw, (980, 202, 1715, 265), "判断いただきたいこと")
    bullets(draw, 998, 315, [
        "基幹管理システムを、既存業務に合わせたカスタム開発で進める妥当性。",
        "初期開発で優先する画面・帳票・ワークフローの範囲。",
        "将来的なAI音声対応、営業支援AI、契約書自動作成、社内FAQ検索への拡張方針。",
    ], 740, F["body"], 15)
    footer(draw, page)
    return img


def heard_slide(page: int):
    img, draw = base()
    title(draw, "Chapter1", "これまでにお伺いしたこと")
    items = [
        ("基幹システム切り替え", "既存システムのサポート終了を見据え、今年中を目途に切り替え検討が必要。"),
        ("現場定着への配慮", "IT活用への慣れに差があるため、日常業務に自然に入る画面設計が重要。"),
        ("日常業務の負荷", "退去修繕対応、契約書作成、請求・インボイス対応などの工数が大きい。"),
        ("データ活用の余地", "顧客・物件・契約・対応履歴を横断して見られる状態を作ることで判断の質を高める。"),
    ]
    xs = [90, 520, 950, 1380]
    for x, (h, b) in zip(xs, items):
        card(draw, (x, 230, x + 365, 760), h, b)
    rounded(draw, (100, 835, 1760, 952), 14, LIGHT_RED, RED, 3)
    draw.text((132, 862), "本提案では、単なる画面開発ではなく「基幹業務の整理」と「今後AIを載せられる土台づくり」を同時に進めます。", font=F["body_b"], fill=BLACK)
    footer(draw, page)
    return img


def proposal_summary(page: int):
    img, draw = base()
    title(draw, "Chapter2", "ご提案の要旨")
    pill(draw, (210, 210, 1710, 285), "基幹管理・期日管理・対応履歴を一体化し、現場の運用負荷を下げる")
    card(draw, (120, 345, 610, 780), "現状の課題感", "基幹システム切り替え、退去修繕・契約書作成・請求対応など、日常業務の負荷が高い。")
    card(draw, (715, 345, 1205, 780), "今回実現すること", "期限、担当、状態、関連書類を一画面で確認できる基幹管理システムを構築する。")
    card(draw, (1310, 345, 1800, 780), "将来拡張", "AI音声対応、営業支援AI、契約書自動作成、社内FAQ検索へ段階的に広げる。")
    rounded(draw, (120, 850, 1800, 952), 14, BG, (230, 230, 230))
    draw.text((155, 878), "モックは今回のご意見を踏まえ、社内稟議時に「何ができるか」が伝わるスクリーンショット資料として作り込みます。", font=F["body_b"], fill=BLACK)
    footer(draw, page)
    return img


def draw_app_shell(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int, heading: str):
    rounded(draw, (x, y, x + w, y + h), 18, WHITE, (216, 216, 216), 2)
    draw.rectangle((x, y, x + 230, y + h), fill=DARK)
    draw.text((x + 32, y + 34), "SANKO", font=F["small_b"], fill=WHITE)
    nav = ["ダッシュボード", "物件管理", "契約管理", "修繕・対応", "書類・検索"]
    for i, label in enumerate(nav):
        yy = y + 110 + i * 62
        draw.rounded_rectangle((x + 24, yy, x + 206, yy + 44), radius=8, fill=RED if i == 0 else (58, 58, 66))
        draw.text((x + 44, yy + 10), label, font=font(19, True), fill=WHITE)
    draw.rectangle((x + 230, y, x + w, y + 78), fill=(252, 252, 252))
    draw.line((x + 230, y + 78, x + w, y + 78), fill=LINE, width=2)
    draw.text((x + 270, y + 27), heading, font=F["small_b"], fill=BLACK)
    return x + 260, y + 105, x + w - 35, y + h - 35


def dashboard_mock(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int):
    cx, cy, rx, by = draw_app_shell(draw, x, y, w, h, "基幹管理ダッシュボード")
    stats = [("本日期限", "12"), ("要確認", "7"), ("遅延リスク", "3"), ("完了", "28"), ("未割当", "4")]
    for i, (label, value) in enumerate(stats):
        bx = cx + i * 170
        rounded(draw, (bx, cy, bx + 148, cy + 88), 12, BG, LINE)
        draw.text((bx + 18, cy + 16), label, font=font(17), fill=MUTED)
        draw.text((bx + 18, cy + 42), value, font=font(34, True), fill=RED if label == "遅延リスク" else BLACK)
    cols = ["退去精算", "修繕対応", "契約更新", "請求確認"]
    for i, col in enumerate(cols):
        bx = cx + i * 220
        rounded(draw, (bx, cy + 126, bx + 198, by), 12, (248, 248, 248), LINE)
        draw.text((bx + 18, cy + 146), col, font=font(20, True), fill=BLACK)
        for j in range(4):
            yy = cy + 190 + j * 82
            rounded(draw, (bx + 16, yy, bx + 182, yy + 60), 8, WHITE, (226, 226, 226))
            draw.rectangle((bx + 16, yy, bx + 22, yy + 60), fill=RED if j == 0 else (180, 180, 180))
            draw.text((bx + 34, yy + 10), f"案件 {i + 1}-{j + 1}", font=font(16, True), fill=BLACK)
            draw.text((bx + 34, yy + 34), "期限 / 担当 / 状態", font=font(13), fill=MUTED)


def detail_mock(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int):
    cx, cy, rx, by = draw_app_shell(draw, x, y, w, h, "物件・契約詳細")
    rounded(draw, (cx, cy, cx + 310, cy + 190), 12, BG, LINE)
    draw.text((cx + 24, cy + 24), "物件情報", font=font(22, True), fill=BLACK)
    for i, line in enumerate(["所在地　東京都〇〇区", "契約状況　更新確認中", "担当者　営業部 A様", "優先度　高"]):
        draw.text((cx + 24, cy + 72 + i * 28), line, font=font(17), fill=TEXT)
    tlx = cx + 405
    draw.line((tlx, cy + 35, tlx, by - 60), fill=(205, 205, 205), width=6)
    steps = [("受付", "問い合わせを自動登録"), ("確認", "担当者が内容確認"), ("承認", "上長承認・通知"), ("完了", "対応履歴として保存")]
    for i, (h1, b1) in enumerate(steps):
        yy = cy + 45 + i * 112
        draw.ellipse((tlx - 20, yy - 20, tlx + 20, yy + 20), fill=RED if i < 3 else (185, 185, 185))
        draw.text((tlx + 45, yy - 29), h1, font=font(23, True), fill=BLACK)
        draw.text((tlx + 45, yy + 6), b1, font=font(18), fill=MUTED)
    panel_x = rx - 335
    rounded(draw, (panel_x, cy, rx, by), 12, BG, LINE)
    draw.text((panel_x + 24, cy + 24), "関連書類 / メモ", font=font(22, True), fill=BLACK)
    for i, line in enumerate(["契約書ドラフト", "見積依頼", "入居者様問い合わせ", "オーナー様報告メモ", "過去対応履歴"]):
        yy = cy + 80 + i * 72
        rounded(draw, (panel_x + 24, yy, rx - 24, yy + 48), 8, WHITE, (226, 226, 226))
        draw.text((panel_x + 44, yy + 13), line, font=font(17, True), fill=BLACK)


def search_mock(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int):
    cx, cy, rx, by = draw_app_shell(draw, x, y, w, h, "社内FAQ・横断検索")
    rounded(draw, (cx, cy, rx, cy + 75), 12, BG, LINE)
    draw.text((cx + 26, cy + 22), "契約更新時の注意点を検索", font=font(24, True), fill=BLACK)
    y0 = cy + 115
    for i, (head, body) in enumerate([
        ("社内FAQ", "更新案内、請求、インボイス対応の社内手順を提示"),
        ("契約書", "関連条文と過去のドラフトを候補表示"),
        ("対応履歴", "類似案件の入居者様対応履歴を要約"),
        ("オーナー報告", "訪問前に物件・収支・過去提案を整理"),
    ]):
        bx = cx + (i % 2) * 430
        byy = y0 + (i // 2) * 190
        rounded(draw, (bx, byy, bx + 390, byy + 145), 12, WHITE, LINE)
        pill(draw, (bx + 22, byy + 18, bx + 180, byy + 58), head, LIGHT_RED, RED)
        draw_wrapped(draw, (bx + 24, byy + 76), body, font(18), 330, TEXT, 6)


def mock_overview(page: int):
    img, draw = base()
    title(draw, "Chapter2", "改善版モックで提示する全体像")
    dashboard_mock(draw, 100, 210, 1360, 735)
    pill(draw, (1500, 230, 1770, 288), "画面で確認できること")
    bullets(draw, 1500, 330, [
        "左サイドバーを残し、実際の運用画面に近い構成で提示",
        "期限・担当・状態を一覧で確認",
        "遅延リスクや要確認案件を強調",
        "稟議用に画面単位で説明可能",
    ], 320, F["small"], 16)
    footer(draw, page)
    return img


def screenshot_dashboard(page: int):
    img, draw = base()
    title(draw, "Chapter2", "スクショ資料1：基幹管理ダッシュボード")
    dashboard_mock(draw, 90, 210, 1450, 735)
    pill(draw, (1580, 230, 1780, 288), "主な機能")
    bullets(draw, 1580, 330, [
        "本日期限・要確認・遅延リスクの可視化",
        "担当者別・案件種別別の絞り込み",
        "期限超過前のアラート表示",
        "対応履歴との連携",
    ], 270, F["small"], 16)
    footer(draw, page)
    return img


def screenshot_detail(page: int):
    img, draw = base()
    title(draw, "Chapter2", "スクショ資料2：物件・契約ごとの進捗管理")
    detail_mock(draw, 90, 210, 1450, 735)
    pill(draw, (1580, 230, 1780, 288), "主な機能")
    bullets(draw, 1580, 330, [
        "物件・契約・対応履歴を一画面で確認",
        "承認・確認・完了までのステータス管理",
        "関連書類やメモの紐づけ",
        "契約書自動作成との連携余地",
    ], 270, F["small"], 16)
    footer(draw, page)
    return img


def screenshot_search(page: int):
    img, draw = base()
    title(draw, "Chapter2", "スクショ資料3：社内FAQ・横断検索")
    search_mock(draw, 90, 210, 1450, 735)
    pill(draw, (1580, 230, 1780, 288), "拡張時の価値")
    bullets(draw, 1580, 330, [
        "社内規程・契約書・過去対応を横断検索",
        "担当者ごとの属人化を軽減",
        "問い合わせ対応や営業準備にAIを活用",
        "基幹データを中心に機能を段階追加",
    ], 270, F["small"], 16)
    footer(draw, page)
    return img


def roadmap(page: int):
    # The user explicitly asked to fully respect this diagram. Reuse the source slide.
    return fit_image(REF / "09.png")


def comparison(page: int):
    img, draw = base()
    title(draw, "Chapter3", "他社比較・社内稟議での判断軸")
    headers = [("判断軸", 90, 335), ("一般的なパッケージ導入", 465, 570), ("Field Xで開発する場合", 1085, 690)]
    for h, x, w in headers:
        pill(draw, (x, 210, x + w, 270), h)
    rows = [
        ("業務適合", "既存機能に業務を寄せる必要がある", "貴社の業務フロー・承認・帳票に合わせて設計"),
        ("現場定着", "画面や操作が合わず利用が限定される可能性", "担当者様の使い方を前提にモックから改善"),
        ("AI拡張", "個別AI連携は追加開発・制約が出やすい", "基幹データを起点にAI音声対応・営業支援AIまで展開"),
        ("社内説明", "導入効果や運用イメージを別途整理する必要", "スクショ資料・要件資料・進め方を一式で提示"),
    ]
    y = 315
    for axis, pkg, fx in rows:
        rounded(draw, (90, y, 425, y + 118), 10, BG, LINE)
        rounded(draw, (465, y, 1035, y + 118), 10, BG, LINE)
        rounded(draw, (1085, y, 1775, y + 118), 10, LIGHT_RED, RED, 2)
        draw.text((118, y + 40), axis, font=F["body_b"], fill=BLACK)
        draw_wrapped(draw, (495, y + 28), pkg, F["small"], 500, TEXT, 6)
        draw_wrapped(draw, (1118, y + 28), fx, F["small"], 615, TEXT, 6)
        y += 138
    footer(draw, page)
    return img


def future_ai(page: int):
    img, draw = base()
    title(draw, "Chapter3", "基幹管理システムを起点に、社内AIへ展開可能")
    # Dense central map with less unused area.
    rounded(draw, (105, 205, 1455, 935), 18, WHITE, LINE, 2)
    dashboard_mock(draw, 135, 245, 690, 610)
    cx, cy = 1120, 550
    draw.ellipse((cx - 145, cy - 78, cx + 145, cy + 78), fill=RED)
    draw.text((cx - 98, cy - 28), "基幹データ\n社内AI基盤", font=font(26, True), fill=WHITE, align="center")
    nodes = [
        ((870, 290), "AI音声対応", "入居者様問い合わせ"),
        ((1185, 290), "営業支援AI", "訪問前ブリーフィング"),
        ((870, 690), "契約書自動作成", "文書作成を省力化"),
        ((1185, 690), "社内FAQ検索", "横断検索・ナレッジ化"),
    ]
    for (nx, ny), h1, b1 in nodes:
        draw.line((cx, cy, nx + 120, ny + 55), fill=LINE, width=4)
        rounded(draw, (nx, ny, nx + 240, ny + 110), 12, BG, LINE)
        draw.text((nx + 22, ny + 24), h1, font=font(22, True), fill=RED)
        draw.text((nx + 22, ny + 65), b1, font=font(16), fill=TEXT)
    pill(draw, (1510, 230, 1780, 288), "展開イメージ")
    bullets(draw, 1510, 330, [
        "入居者様問い合わせの一次対応",
        "オーナー様訪問前の情報整理",
        "契約書・通知文の下書き",
        "社内情報を便利FAQ化",
    ], 320, F["small"], 16)
    footer(draw, page)
    return img


def next_actions(page: int):
    img, draw = base()
    title(draw, "Next", "今後ご提示予定の資料")
    items = [
        ("01", "改善版モック", "今回いただいたご意見を反映し、画面・操作・ステータスの見え方を作り込みます。"),
        ("02", "機能・要件説明資料", "スクリーンショットごとに、必要機能・データ項目・運用イメージを整理します。"),
        ("03", "開発計画", "ご契約後の要件定義、設計、開発、テスト、導入、改善の流れを具体化します。"),
    ]
    y = 250
    for num, h1, b1 in items:
        draw.text((140, y), num, font=F["large"], fill=RED)
        draw.text((285, y + 9), h1, font=F["mid"], fill=BLACK)
        draw_wrapped(draw, (290, y + 72), b1, F["body"], 1220, MUTED, 8)
        y += 210
    rounded(draw, (120, 895, 1760, 972), 14, RED)
    draw.text((150, 916), "まずは、社内稟議・他社比較で使える状態まで、モックと画面別説明資料を整えます。", font=F["body_b"], fill=WHITE)
    footer(draw, page)
    return img


SLIDES = [
    ("基幹管理システム ご提案資料", cover),
    ("目次", agenda),
    ("これまでにお伺いしたこと", lambda p: chapter(p, "01", "これまでにお伺いしたこと")),
    ("本資料の位置づけ", position_slide),
    ("これまでにお伺いしたこと", heard_slide),
    ("ご提案の要旨・デモンストレーション", lambda p: chapter(p, "02", "ご提案の要旨・デモンストレーション")),
    ("ご提案の要旨", proposal_summary),
    ("改善版モックで提示する全体像", mock_overview),
    ("スクショ資料1：基幹管理ダッシュボード", screenshot_dashboard),
    ("スクショ資料2：物件・契約ごとの進捗管理", screenshot_detail),
    ("スクショ資料3：社内FAQ・横断検索", screenshot_search),
    ("今後の進め方のイメージ", lambda p: chapter(p, "03", "今後の進め方のイメージ")),
    ("今後の進め方のイメージ", roadmap),
    ("他社比較・社内稟議での判断軸", comparison),
    ("基幹管理システムを起点に、社内AIへ展開可能", future_ai),
    ("今後ご提示予定の資料", next_actions),
]


def save_slide(img: Image.Image, index: int) -> Path:
    OUT_IMAGES.mkdir(parents=True, exist_ok=True)
    path = OUT_IMAGES / f"slide_{index:02d}.png"
    img.save(path, quality=95)
    return path


def write_markdown(slide_paths: list[Path]):
    requirements = """# Requirements

## Basic

Project name: kikan-management-proposal
Audience: 株式会社三幸 担当者様、社内稟議関係者、他社コンペ比較者
Goal: 基幹管理システムの開発方針、改善版モック、開発・導入の進め方を説明する
Product/service: 基幹管理システム、社内AI基盤
Desired page count: 16
Tone: 法人向け、実務的、稟議に使いやすい

## Notes

- 左サイドバーはモック画面内で維持。
- 冒頭3枚は既存資料のトーンに寄せる。
- 今後の進め方のイメージは参照スライドを優先して使用。
"""
    (PROJECT / "requirements.md").write_text(requirements, encoding="utf-8")

    plan = ["# Slide Plan", ""]
    text = ["# Google Slides Text", "", "PPTX/Googleスライド確認用の原稿です。", ""]
    for i, ((title_text, _), path) in enumerate(zip(SLIDES, slide_paths), start=1):
        plan += [f"## {i:02d}. {title_text}", "", f"Image: generated_backgrounds/{path.name}", ""]
        text += [f"## {i:02d}. {title_text}", "", f"Title: {title_text}", ""]
    (PROJECT / "slide_plan.md").write_text("\n".join(plan), encoding="utf-8")
    (PROJECT / "google_slides_text.md").write_text("\n".join(text), encoding="utf-8")
    log = ["# Generation Log", "", f"Generated at: {datetime.now().isoformat(timespec='seconds')}", ""]
    log += [f"- {p.as_posix()}" for p in slide_paths]
    (PROJECT / "generation_log.md").write_text("\n".join(log), encoding="utf-8")


def rels(entries: list[tuple[str, str, str]]) -> str:
    rows = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">']
    for rid, typ, target in entries:
        rows.append(f'<Relationship Id="{rid}" Type="{typ}" Target="{target}"/>')
    rows.append("</Relationships>")
    return "".join(rows)


def slide_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld><p:spTree>
    <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
    <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
    <p:pic>
      <p:nvPicPr><p:cNvPr id="2" name="slide image"/><p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr>
      <p:blipFill><a:blip r:embed="rId2"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>
      <p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="12192000" cy="6858000"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>
    </p:pic>
  </p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>'''


def write_pptx(slide_paths: list[Path], out_path: Path):
    overrides = "\n".join(
        f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
        for i in range(1, len(slide_paths) + 1)
    )
    content_types = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  <Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
  <Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
  <Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
  {overrides}
</Types>'''
    sld_ids = "".join(f'<p:sldId id="{255+i}" r:id="rId{i+1}"/>' for i in range(1, len(slide_paths) + 1))
    presentation = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>
  <p:sldIdLst>{sld_ids}</p:sldIdLst>
  <p:sldSz cx="12192000" cy="6858000" type="wide"/>
  <p:notesSz cx="6858000" cy="9144000"/>
</p:presentation>'''
    pres_rels = [("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster", "slideMasters/slideMaster1.xml")]
    for i in range(1, len(slide_paths) + 1):
        pres_rels.append((f"rId{i+1}", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide", f"slides/slide{i}.xml"))
    slide_master = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld>
  <p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
  <p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>
  <p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles>
</p:sldMaster>'''
    slide_layout = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank" preserve="1">
  <p:cSld name="Blank"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sldLayout>'''
    theme = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Field X"><a:themeElements>
<a:clrScheme name="Office"><a:dk1><a:srgbClr val="000000"/></a:dk1><a:lt1><a:srgbClr val="FFFFFF"/></a:lt1><a:dk2><a:srgbClr val="1F1F1F"/></a:dk2><a:lt2><a:srgbClr val="F5F5F5"/></a:lt2><a:accent1><a:srgbClr val="FF1818"/></a:accent1><a:accent2><a:srgbClr val="666666"/></a:accent2><a:accent3><a:srgbClr val="E6E6E6"/></a:accent3><a:accent4><a:srgbClr val="BFBFBF"/></a:accent4><a:accent5><a:srgbClr val="7F7F7F"/></a:accent5><a:accent6><a:srgbClr val="D90000"/></a:accent6><a:hlink><a:srgbClr val="0563C1"/></a:hlink><a:folHlink><a:srgbClr val="954F72"/></a:folHlink></a:clrScheme>
<a:fontScheme name="Office"><a:majorFont><a:latin typeface="Yu Gothic"/><a:ea typeface="Yu Gothic"/></a:majorFont><a:minorFont><a:latin typeface="Yu Gothic"/><a:ea typeface="Yu Gothic"/></a:minorFont></a:fontScheme>
<a:fmtScheme name="Office"><a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst><a:lnStyleLst><a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst><a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst><a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst></a:fmtScheme>
</a:themeElements></a:theme>'''
    core = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>基幹管理システム ご提案資料</dc:title><dc:creator>Field X</dc:creator><cp:lastModifiedBy>Field X</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{datetime.utcnow().isoformat(timespec='seconds')}Z</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{datetime.utcnow().isoformat(timespec='seconds')}Z</dcterms:modified>
</cp:coreProperties>'''
    app = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Codex</Application><PresentationFormat>On-screen Show (16:9)</PresentationFormat><Slides>{len(slide_paths)}</Slides>
</Properties>'''
    with zipfile.ZipFile(out_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", rels([
            ("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument", "ppt/presentation.xml"),
            ("rId2", "http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties", "docProps/core.xml"),
            ("rId3", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties", "docProps/app.xml"),
        ]))
        z.writestr("docProps/core.xml", core)
        z.writestr("docProps/app.xml", app)
        z.writestr("ppt/presentation.xml", presentation)
        z.writestr("ppt/_rels/presentation.xml.rels", rels(pres_rels))
        z.writestr("ppt/slideMasters/slideMaster1.xml", slide_master)
        z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", rels([
            ("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout", "../slideLayouts/slideLayout1.xml"),
            ("rId2", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme", "../theme/theme1.xml"),
        ]))
        z.writestr("ppt/slideLayouts/slideLayout1.xml", slide_layout)
        z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", rels([
            ("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster", "../slideMasters/slideMaster1.xml"),
        ]))
        z.writestr("ppt/theme/theme1.xml", theme)
        for i, path in enumerate(slide_paths, start=1):
            z.writestr(f"ppt/slides/slide{i}.xml", slide_xml())
            z.writestr(f"ppt/slides/_rels/slide{i}.xml.rels", rels([
                ("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout", "../slideLayouts/slideLayout1.xml"),
                ("rId2", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image", f"../media/image{i}.png"),
            ]))
            z.write(path, f"ppt/media/image{i}.png")


def main():
    PROJECT.mkdir(parents=True, exist_ok=True)
    OUT_IMAGES.mkdir(parents=True, exist_ok=True)
    OUT_MOCKS.mkdir(parents=True, exist_ok=True)
    for old in OUT_IMAGES.glob("slide_*.png"):
        old.unlink()
    for old in OUT_MOCKS.glob("slide_*.png"):
        old.unlink()
    slide_paths = []
    for index, (_, builder) in enumerate(SLIDES, start=1):
        slide_paths.append(save_slide(builder(index), index))
    for src in slide_paths[7:11]:
        shutil.copy2(src, OUT_MOCKS / src.name)
    write_markdown(slide_paths)
    write_pptx(slide_paths, OUT_PPTX)
    shutil.copy2(OUT_PPTX, OUT_PPTX_JA)
    print(f"Wrote {len(slide_paths)} slide images")
    print(OUT_PPTX_JA)


if __name__ == "__main__":
    main()
