from __future__ import annotations

import html
import shutil
import zipfile
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projects" / "2026-04-24-period-management-proposal"
OUT = PROJECT / "株式会社三幸_基幹管理システムご提案資料_editable.pptx"

EMU = 6350
SLIDE_W = 1920
SLIDE_H = 1080
CX = 12192000
CY = 6858000

RED = "ff1818"
DARK = "15151b"
BLACK = "111111"
TEXT = "333333"
MUTED = "666666"
GRAY = "f5f5f5"
LINE = "dedede"
LIGHT_RED = "ffeaea"
WHITE = "ffffff"


def e(v: int | float) -> int:
    return int(round(v * EMU))


class Deck:
    def __init__(self) -> None:
        self.next_id = 2

    def new_id(self) -> int:
        value = self.next_id
        self.next_id += 1
        return value

    def reset(self) -> None:
        self.next_id = 2


D = Deck()


def esc(value: str) -> str:
    return html.escape(value, quote=False)


def solid(color: str) -> str:
    return f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'


def line_xml(color: str | None, width: int = 1) -> str:
    if color is None:
        return "<a:ln><a:noFill/></a:ln>"
    return f'<a:ln w="{e(width)}">{solid(color)}</a:ln>'


def fill_xml(color: str | None) -> str:
    if color is None:
        return "<a:noFill/>"
    return solid(color)


def tx_body(
    text: str,
    size: int = 24,
    color: str = BLACK,
    bold: bool = False,
    align: str = "l",
    valign: str = "t",
    margin: int = 12,
) -> str:
    b = ' b="1"' if bold else ""
    paragraphs = []
    for raw in text.split("\n"):
        paragraphs.append(
            f'<a:p><a:pPr algn="{align}"/>'
            f'<a:r><a:rPr lang="ja-JP" sz="{size * 100}"{b}>'
            f'{solid(color)}<a:latin typeface="Yu Gothic"/><a:ea typeface="Yu Gothic"/></a:rPr>'
            f"<a:t>{esc(raw)}</a:t></a:r></a:p>"
        )
    anchor = {"t": "t", "m": "ctr", "b": "b"}.get(valign, "t")
    return (
        f'<p:txBody><a:bodyPr wrap="square" anchor="{anchor}" '
        f'lIns="{e(margin)}" tIns="{e(margin)}" rIns="{e(margin)}" bIns="{e(margin)}"/>'
        f"<a:lstStyle/>{''.join(paragraphs)}</p:txBody>"
    )


def shape(
    x: int,
    y: int,
    w: int,
    h: int,
    kind: str = "rect",
    fill: str | None = None,
    line: str | None = None,
    line_w: int = 1,
    text: str | None = None,
    size: int = 24,
    color: str = BLACK,
    bold: bool = False,
    align: str = "l",
    valign: str = "t",
    margin: int = 12,
    name: str = "Shape",
) -> str:
    sid = D.new_id()
    tx = tx_body(text, size, color, bold, align, valign, margin) if text is not None else ""
    return f"""
<p:sp>
  <p:nvSpPr><p:cNvPr id="{sid}" name="{esc(name)} {sid}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="{e(x)}" y="{e(y)}"/><a:ext cx="{e(w)}" cy="{e(h)}"/></a:xfrm>
    <a:prstGeom prst="{kind}"><a:avLst/></a:prstGeom>
    {fill_xml(fill)}
    {line_xml(line, line_w)}
  </p:spPr>
  {tx}
</p:sp>"""


def text_box(x: int, y: int, w: int, h: int, text: str, size=24, color=BLACK, bold=False, align="l", valign="t") -> str:
    return shape(x, y, w, h, "rect", None, None, text=text, size=size, color=color, bold=bold, align=align, valign=valign, margin=2, name="Text")


def footer(page: int) -> list[str]:
    return [
        text_box(70, 1010, 700, 36, "Copyright @Field X inc. All rights reserved.", 14, "888888", True),
        shape(1870, 0, 50, 1080, "rect", RED, None),
        text_box(1878, 1010, 36, 40, str(page), 20, WHITE, True, "c"),
    ]


def title(chapter: str, heading: str) -> list[str]:
    return [
        text_box(82, 58, 220, 28, chapter, 15, RED, True),
        text_box(82, 94, 1150, 58, heading, 30, BLACK, True),
    ]


def dot_grid(x: int, y: int, cols: int, rows: int, gap: int, color: str = "d8d8d8", size: int = 5) -> list[str]:
    shapes: list[str] = []
    for row in range(rows):
        for col in range(cols):
            shapes.append(shape(x + col * gap, y + row * gap, size, size, "ellipse", color, None))
    return shapes


def art_title(chapter_no: str, chapter: str, heading: str, page: int) -> list[str]:
    return [
        shape(0, 0, 138, SLIDE_H, "rect", RED, RED),
        text_box(33, 56, 72, 24, "Chapter", 14, WHITE, True, "c"),
        text_box(18, 96, 102, 70, chapter_no, 56, WHITE, True, "c"),
        shape(33, 188, 72, 5, "rect", WHITE, WHITE),
        text_box(40, 1010, 54, 34, str(page), 22, WHITE, True, "c"),
        shape(185, 74, 150, 14, "rect", RED, RED),
        text_box(185, 112, 1250, 54, heading, 32, BLACK, True),
        text_box(185, 174, 600, 24, chapter, 15, MUTED, True),
        text_box(215, 1018, 700, 30, "Copyright @Field X inc. All rights reserved.", 12, "999999", True),
    ]


def pill(x: int, y: int, w: int, h: int, label: str, fill=RED, color=WHITE) -> str:
    return shape(x, y, w, h, "roundRect", fill, fill, text=label, size=20, color=color, bold=True, align="c", valign="m", margin=6)


def bullet_text(items: list[str]) -> str:
    return "\n".join(f"・{item}" for item in items)


def card(x: int, y: int, w: int, h: int, head: str, body: str) -> list[str]:
    return [
        shape(x, y, w, h, "roundRect", WHITE, LINE),
        shape(x, y, w, 10, "rect", RED, RED),
        text_box(x + 30, y + 36, w - 60, 38, head, 20, BLACK, True),
        shape(x + 30, y + 92, w - 60, 3, "rect", LINE, LINE),
        text_box(x + 30, y + 122, w - 60, h - 145, body, 16, TEXT),
    ]


def feature_card(x: int, y: int, w: int, h: int, marker: str, head: str, body: str) -> list[str]:
    return [
        shape(x, y, w, h, "roundRect", WHITE, LINE),
        shape(x + 32, y + 32, 98, 98, "ellipse", RED, RED),
        text_box(x + 51, y + 62, 60, 36, marker, 28, WHITE, True, "c"),
        text_box(x + 152, y + 40, w - 185, 38, head, 21, BLACK, True),
        shape(x + 32, y + 153, w - 64, 3, "rect", LINE, LINE),
        text_box(x + 38, y + 192, w - 76, h - 215, body, 16, TEXT),
    ]


def check_item(x: int, y: int, head: str, body: str) -> list[str]:
    return [
        shape(x, y, 76, 76, "ellipse", LIGHT_RED, LIGHT_RED),
        text_box(x + 20, y + 14, 36, 30, "✓", 30, RED, True, "c"),
        text_box(x + 98, y + 5, 210, 28, head, 18, BLACK, True),
        text_box(x + 98, y + 45, 210, 34, body, 14, MUTED),
    ]


def insight_bar(x: int, y: int, w: int, h: int, head: str, body: str, actions: list[str]) -> list[str]:
    shapes = [
        shape(x, y, w, h, "roundRect", LIGHT_RED, RED, 2),
        shape(x + 38, y + 32, 110, 110, "ellipse", RED, RED),
        text_box(x + 72, y + 58, 42, 46, "!", 40, WHITE, True, "c"),
        text_box(x + 185, y + 30, 680, 36, head, 23, BLACK, True),
        text_box(x + 185, y + 82, 760, 42, body, 16, MUTED),
    ]
    for i, label in enumerate(actions):
        bx = x + w - 670 + i * 215
        shapes.append(shape(bx, y + 54, 175, 58, "roundRect", "ffd9d9", "ffd9d9", text=label, size=18, color=RED, bold=True, align="c", valign="m"))
    return shapes


def app_shell(x: int, y: int, w: int, h: int, heading: str) -> list[str]:
    shapes = [
        shape(x, y, w, h, "roundRect", WHITE, LINE, 2),
        shape(x, y, 205, h, "rect", DARK, DARK),
        shape(x + 32, y + 34, 42, 42, "ellipse", RED, RED),
        text_box(x + 86, y + 35, 96, 34, "Field X", 22, WHITE, True),
        shape(x + 205, y, w - 205, 84, "rect", "fcfcfc", LINE),
        text_box(x + 245, y + 28, 700, 32, heading, 19, BLACK, True),
        text_box(x + w - 182, y + 30, 95, 24, "担当者", 14, MUTED),
    ]
    nav = ["総合", "物件", "契約", "修繕", "書類", "検索"]
    for i, item in enumerate(nav):
        fill = RED if i == 0 else "2d2f36"
        shapes.append(shape(x + 24, y + 112 + i * 63, 158, 44, "roundRect", fill, fill, text=item, size=15, color=WHITE, bold=True, valign="m", align="c"))
    shapes += [
        shape(x + 32, y + h - 92, 132, 3, "rect", "4c4c53", "4c4c53"),
        shape(x + 36, y + h - 64, 34, 34, "ellipse", "f1f1f1", "f1f1f1"),
        text_box(x + 86, y + h - 60, 80, 22, "設定", 13, "d0d0d0"),
    ]
    return shapes


def dashboard_ui(x: int, y: int, w: int, h: int) -> list[str]:
    shapes = app_shell(x, y, w, h, "基幹管理ダッシュボード")
    cx, cy = x + 248, y + 118
    cw = w - 285
    stats = [("本日期限", "12"), ("要確認", "7"), ("遅延リスク", "3"), ("完了", "28"), ("未割当", "4")]
    for i, (label, value) in enumerate(stats):
        bw = int((cw - 52) / 5)
        bx = cx + i * (bw + 13)
        shapes += [
            shape(bx, cy, bw, 108, "roundRect", WHITE, LINE),
            text_box(bx + 16, cy + 18, bw - 32, 22, label, 13, MUTED, True),
            text_box(bx + 20, cy + 48, 70, 42, value, 31, RED if label == "遅延リスク" else BLACK, True),
            shape(bx + bw - 86, cy + 80, 62, 4, "rect", RED if label == "遅延リスク" else "c9c9c9", None),
        ]
    cols = ["退去精算", "修繕対応", "契約更新", "請求確認", "入居対応"]
    for i, col in enumerate(cols):
        bw = int((cw - 64) / 5)
        bx = cx + i * (bw + 16)
        shapes += [
            shape(bx, cy + 130, bw, 295, "roundRect", "f8f8f8", LINE),
            text_box(bx + 18, cy + 150, bw - 72, 25, col, 15, BLACK, True),
            shape(bx + bw - 48, cy + 148, 32, 26, "roundRect", RED if i == 2 else "b9bcc2", RED if i == 2 else "b9bcc2"),
        ]
        for j in range(3):
            yy = cy + 190 + j * 76
            shapes += [
                shape(bx + 16, yy, bw - 32, 58, "roundRect", WHITE, LINE),
                shape(bx + 16, yy, 7, 58, "rect", RED if j == 0 else "bfbfbf", None),
                text_box(bx + 38, yy + 10, bw - 80, 20, f"案件 {i + 1}-{j + 1}", 12, BLACK, True),
                text_box(bx + 38, yy + 33, bw - 80, 18, "期限 / 担当 / 状態", 9, MUTED),
            ]
    shapes += [
        shape(cx, cy + 455, int(cw * 0.55), 130, "roundRect", WHITE, LINE),
        text_box(cx + 22, cy + 475, 220, 24, "直近対応履歴", 15, BLACK, True),
        shape(cx + int(cw * 0.58), cy + 455, int(cw * 0.42), 130, "roundRect", WHITE, LINE),
        shape(cx + int(cw * 0.63), cy + 488, 70, 70, "ellipse", RED, RED),
        shape(cx + int(cw * 0.645), cy + 506, 36, 36, "ellipse", WHITE, WHITE),
        text_box(cx + int(cw * 0.72), cy + 488, 210, 26, "対応種別の内訳", 15, BLACK, True),
    ]
    for i, label in enumerate(["退去立会い", "見積確認", "契約更新"]):
        yy = cy + 515 + i * 24
        shapes += [
            shape(cx + 24, yy, 12, 12, "ellipse", RED if i == 0 else "a9a9a9", None),
            text_box(cx + 52, yy - 5, 160, 22, label, 12, MUTED),
            shape(cx + 305, yy + 4, 90, 6, "rect", "d7d7d7", None),
            shape(cx + 440, yy + 4, 70, 6, "rect", "d7d7d7", None),
        ]
    return shapes


def detail_ui(x: int, y: int, w: int, h: int) -> list[str]:
    shapes = app_shell(x, y, w, h, "物件・契約詳細")
    cx, cy = x + 260, y + 112
    shapes += [
        shape(cx, cy, 305, 190, "roundRect", GRAY, LINE),
        text_box(cx + 22, cy + 20, 130, 30, "物件情報", 18, BLACK, True),
        text_box(cx + 22, cy + 68, 235, 100, "所在地　東京都〇〇区\n契約状況　更新確認中\n担当者　営業部 A様\n優先度　高", 13, TEXT),
    ]
    tlx = cx + 405
    shapes.append(shape(tlx - 3, cy + 35, 6, 410, "rect", "d1d1d1", None))
    steps = [("受付", "問い合わせを自動登録"), ("確認", "担当者が内容確認"), ("承認", "上長承認・通知"), ("完了", "対応履歴として保存")]
    for i, (h1, b1) in enumerate(steps):
        yy = cy + 50 + i * 106
        shapes += [
            shape(tlx - 18, yy - 18, 36, 36, "ellipse", RED if i < 3 else "bdbdbd", None),
            text_box(tlx + 45, yy - 28, 110, 28, h1, 18, BLACK, True),
            text_box(tlx + 45, yy + 4, 220, 24, b1, 13, MUTED),
        ]
    px = x + w - 360
    shapes += [
        shape(px, cy, 320, h - 150, "roundRect", GRAY, LINE),
        text_box(px + 24, cy + 22, 230, 28, "関連書類 / メモ", 17, BLACK, True),
    ]
    for i, line in enumerate(["契約書ドラフト", "見積依頼", "入居者様問い合わせ", "オーナー様報告メモ", "過去対応履歴"]):
        yy = cy + 78 + i * 66
        shapes += [
            shape(px + 24, yy, 268, 44, "roundRect", WHITE, LINE),
            text_box(px + 42, yy + 11, 210, 20, line, 13, BLACK, True),
        ]
    return shapes


def search_ui(x: int, y: int, w: int, h: int) -> list[str]:
    shapes = app_shell(x, y, w, h, "社内FAQ・横断検索")
    cx, cy = x + 260, y + 112
    shapes += [
        shape(cx, cy, w - 310, 70, "roundRect", GRAY, LINE),
        text_box(cx + 24, cy + 20, 520, 28, "契約更新時の注意点を検索", 19, BLACK, True),
    ]
    cards = [
        ("社内FAQ", "更新案内、請求、インボイス対応の社内手順を提示"),
        ("契約書", "関連条文と過去のドラフトを候補表示"),
        ("対応履歴", "類似案件の入居者様対応履歴を要約"),
        ("オーナー報告", "訪問前に物件・収支・過去提案を整理"),
    ]
    for i, (head, body) in enumerate(cards):
        bx = cx + (i % 2) * 430
        by = cy + 120 + (i // 2) * 180
        shapes += [
            shape(bx, by, 390, 138, "roundRect", WHITE, LINE),
            shape(bx + 22, by + 18, 150, 38, "roundRect", LIGHT_RED, LIGHT_RED, text=head, size=14, color=RED, bold=True, valign="m", align="c"),
            text_box(bx + 24, by + 74, 330, 42, body, 13, TEXT),
        ]
    return shapes


def cover(page: int) -> list[str]:
    return [
        shape(-360, -260, 690, 610, "ellipse", RED, RED),
        shape(1500, -210, 880, 880, "ellipse", RED, RED),
        shape(-255, 810, 515, 450, "ellipse", RED, RED),
        shape(1225, 850, 480, 480, "ellipse", None, RED, 8),
        *dot_grid(1210, 75, 8, 6, 24, "d7d7d7", 6),
        *dot_grid(1645, 855, 8, 4, 20, RED, 6),
        *[shape(1040 + i * 66, 900 - i * 25, 28, 120 + i * 25, "rect", "eeeeee", None) for i in range(8)],
        text_box(90, 145, 300, 40, "株式会社三幸　御中", 20, BLACK, True),
        text_box(90, 255, 960, 88, "基幹管理システムの", 52, BLACK, True),
        text_box(90, 355, 600, 88, "ご提案資料", 52, BLACK, True),
        text_box(90, 505, 1100, 48, "他社コンペ・社内稟議向け / モック改善版のご提案", 28, RED, True),
        shape(90, 645, 865, 90, "roundRect", WHITE, LINE),
        text_box(126, 673, 800, 28, "改善版モック / 画面別要件 / 開発ロードマップ", 20, BLACK, True),
        text_box(90, 590, 260, 36, "2026年04月25日", 22, BLACK, True),
        text_box(1320, 880, 330, 70, "Field X", 48, BLACK, True),
        *footer(page),
    ]


def agenda(page: int) -> list[str]:
    shapes = [text_box(90, 70, 120, 24, "AGENDA", 14, RED, True), text_box(90, 105, 110, 30, "目次", 18, BLACK, True)]
    items = [
        ("01", "これまでにお伺いしたこと", "社内稟議・他社比較に必要な前提整理"),
        ("02", "ご提案の要旨・デモンストレーション", "改善版モック、画面別要件、将来のAI活用"),
        ("03", "今後の進め方のイメージ", "要件定義から開発・現場導入・改善運用まで"),
    ]
    y = 285
    for num, head, body in items:
        shapes += [
            text_box(525, y, 90, 58, num, 40, RED, True),
            text_box(690, y + 9, 650, 42, head, 26, RED, True),
            text_box(695, y + 68, 720, 32, body, 20, MUTED),
        ]
        y += 185
    shapes += footer(page)
    return shapes


def chapter(page: int, num: str, heading: str) -> list[str]:
    return [
        shape(0, 0, SLIDE_W, SLIDE_H, "rect", RED, RED),
        text_box(85, 395, 260, 150, num, 118, "ffa6a6", True),
        text_box(380, 505, 1000, 66, heading, 38, WHITE, True),
        text_box(70, 1018, 700, 36, "Copyright @Field X inc. All rights reserved.", 14, "ffdcdc", True),
        text_box(1880, 1010, 34, 38, str(page), 20, WHITE, True),
    ]


def position_slide(page: int) -> list[str]:
    shapes = [*title("Chapter1", "本資料の位置づけ")]
    shapes += [pill(95, 205, 760, 58, "今回の目的"), pill(965, 205, 760, 58, "判断いただきたいこと")]
    shapes += [
        text_box(112, 315, 780, 210, bullet_text([
            "担当者様に確認いただいたモックを、社内稟議・他社コンペで比較しやすい資料に整理します。",
            "本資料では開発範囲・機能・進め方・将来展開を中心に説明します。",
            "今回のご意見を反映し、画面単位で要件と機能が分かる改善版モックとして提出します。",
        ]), 20, BLACK, True),
        text_box(982, 315, 750, 210, bullet_text([
            "基幹管理システムを、既存業務に合わせたカスタム開発で進める妥当性。",
            "初期開発で優先する画面・帳票・ワークフローの範囲。",
            "将来的なAI音声対応、営業支援AI、契約書自動作成、社内FAQ検索への拡張方針。",
        ]), 20, BLACK, True),
    ]
    bottom = [
        ("提出物", "改善版モック\n画面別要件資料\n開発の進め方"),
        ("社内稟議での使い方", "比較観点を整理\n機能範囲を明確化\n導入後の展開を説明"),
        ("次の確認事項", "優先機能\n権限・帳票\n既存データ移行"),
    ]
    for i, (head, body) in enumerate(bottom):
        x = 115 + i * 560
        shapes += card(x, 700, 500, 245, head, body)
    shapes += footer(page)
    return shapes


def heard_slide(page: int) -> list[str]:
    shapes = [*title("Chapter1", "これまでにお伺いしたこと")]
    cards = [
        ("基幹システム切り替え", "既存システムのサポート終了を見据え、今年中を目途に切り替え検討が必要。"),
        ("現場定着への配慮", "IT活用への慣れに差があるため、日常業務に自然に入る画面設計が重要。"),
        ("日常業務の負荷", "退去修繕対応、契約書作成、請求・インボイス対応などの工数が大きい。"),
        ("データ活用の余地", "顧客・物件・契約・対応履歴を横断して見られる状態を作ることで判断の質を高める。"),
    ]
    for i, (head, body) in enumerate(cards):
        shapes += card(90 + i * 430, 230, 365, 520, head, body)
    shapes += [
        shape(100, 835, 1660, 116, "roundRect", LIGHT_RED, RED, 2),
        text_box(132, 862, 1600, 42, "本提案では、単なる画面開発ではなく「基幹業務の整理」と「今後AIを載せられる土台づくり」を同時に進めます。", 22, BLACK, True),
        *footer(page),
    ]
    return shapes


def proposal_summary(page: int) -> list[str]:
    shapes = [*art_title("02", "Chapter2", "ご提案の要旨", page)]
    shapes += [pill(235, 235, 1490, 65, "基幹管理・期日管理・対応履歴を一体化し、現場の運用負荷を下げる")]
    shapes += feature_card(185, 360, 475, 405, "01", "現状の課題感", "基幹システム切り替え、退去修繕、契約書作成、請求対応など、日常業務の負荷が高い状態です。")
    shapes += feature_card(725, 360, 475, 405, "02", "今回実現すること", "期限、担当、状態、関連書類を一画面で確認できる基幹管理システムとして整理します。")
    shapes += feature_card(1265, 360, 475, 405, "03", "将来拡張", "AI音声対応、営業支援AI、契約書自動作成、社内FAQ検索へ段階的に広げます。")
    shapes += insight_bar(185, 850, 1590, 150, "社内稟議で伝えるポイント", "画面・要件・進め方を一式で見せ、他社比較で判断しやすい資料にします。", ["画面", "要件", "進め方"])
    return shapes


def mock_overview(page: int) -> list[str]:
    shapes = [*art_title("02", "Chapter2", "改善版モックで提示する全体像", page)]
    shapes += dashboard_ui(185, 245, 1290, 705)
    side = [
        ("1", "実運用に近い", "左サイドバーを残し、日常利用を想像しやすくします。"),
        ("2", "稟議で比較しやすい", "期限・担当・状態・リスクを画面単位で説明します。"),
        ("3", "要件化しやすい", "画面から機能・データ項目・運用を確認できます。"),
    ]
    for i, (num, head, body) in enumerate(side):
        y = 255 + i * 235
        shapes += [
            shape(1530, y, 320, 195, "roundRect", WHITE, LINE),
            shape(1562, y + 42, 72, 72, "ellipse", LIGHT_RED, LIGHT_RED),
            text_box(1583, y + 58, 30, 32, num, 26, RED, True, "c"),
            text_box(1655, y + 38, 155, 28, head, 18, RED, True),
            text_box(1655, y + 82, 160, 55, body, 13, MUTED),
        ]
    return shapes


def screenshot_dashboard(page: int) -> list[str]:
    shapes = [*art_title("02", "Chapter2", "スクショ資料1：基幹管理ダッシュボード", page)]
    shapes += dashboard_ui(185, 245, 1320, 705)
    shapes += [
        shape(1550, 260, 300, 690, "roundRect", WHITE, LINE),
        text_box(1590, 298, 180, 30, "主な機能", 22, RED, True),
        *check_item(1585, 380, "期限・リスク", "本日期限と遅延リスクを可視化"),
        *check_item(1585, 540, "絞り込み", "担当者別・案件種別別に確認"),
        *check_item(1585, 700, "履歴連携", "対応履歴と関連書類を紐づけ"),
    ]
    return shapes


def screenshot_detail(page: int) -> list[str]:
    shapes = [*art_title("02", "Chapter2", "スクショ資料2：物件・契約ごとの進捗管理", page)]
    shapes += detail_ui(185, 245, 1320, 705)
    shapes += [
        shape(1550, 260, 300, 690, "roundRect", WHITE, LINE),
        text_box(1590, 298, 180, 30, "主な機能", 22, RED, True),
        *check_item(1585, 380, "一画面管理", "物件・契約・履歴を確認"),
        *check_item(1585, 540, "進捗管理", "承認から完了まで可視化"),
        *check_item(1585, 700, "書類連携", "契約書自動作成へ接続"),
    ]
    return shapes


def screenshot_search(page: int) -> list[str]:
    shapes = [*art_title("02", "Chapter2", "スクショ資料3：社内FAQ・横断検索", page)]
    shapes += search_ui(185, 245, 1320, 705)
    shapes += [
        shape(1550, 260, 300, 690, "roundRect", WHITE, LINE),
        text_box(1590, 298, 180, 30, "拡張時の価値", 22, RED, True),
        *check_item(1585, 380, "横断検索", "契約書・規程・履歴を検索"),
        *check_item(1585, 540, "属人化軽減", "担当者ごとの差を小さくする"),
        *check_item(1585, 700, "AI活用", "問い合わせ・営業準備に展開"),
    ]
    return shapes


def roadmap(page: int) -> list[str]:
    shapes = [*title("Chapter3", "今後の進め方のイメージ")]
    shapes.append(text_box(105, 175, 1700, 52, "繁忙期であると推察されますので、できる限り現場の混乱を避け円滑に進めるため、下記のような流れで進めさせていただければ幸いです。", 21, BLACK, True))
    shapes.append(shape(98, 295, 1760, 748, "roundRect", WHITE, None))
    steps = [("01", "ご契約"), ("02", "進め方の確認"), ("03", "データ移行先の準備"), ("04", "エージェント開発"), ("05", "現場導入"), ("06", "改善")]
    x0, gap = 200, 280
    for i, (num, label) in enumerate(steps):
        x = x0 + i * gap
        shapes += [
            shape(x, 338, 150, 150, "ellipse", WHITE, "d6d6d6", 3),
            shape(x + 14, 352, 122, 122, "ellipse", None, "ff7474", 7),
            text_box(x + 38, 385, 78, 60, num, 38, RED, True, "c"),
        ]
        if i < 5:
            shapes.append(shape(x + 160, 410, 110, 6, "rect", "ff7474", None))
            shapes.append(shape(x + 212, 398, 18, 30, "ellipse", RED, None))
        shapes += [
            shape(x - 75, 510, 270, 70, "rightArrow", RED, RED, text=label, size=18, color=WHITE, bold=True, align="c", valign="m"),
        ]
    bodies = [
        "NDAや個別契約など\n各種ご契約を結ばせて\nいただきます。\n\n※御社フォーマットなどが\nございましたらご都合に\n合わせます。",
        "データ整理の必要可否も含め、\nなるべく現場の従業員の方の\n混乱を起こさないように、\n詳細なプランニングを\nすり合わせます。",
        "データマイグレーションを\n同時並行で実行する場合、\n移行先を先に準備することが\n最重要です。",
        "弊社でエージェントを開発。\n毎週のご報告会を行いながら、\n使用感やUIなどをすり合わせます。",
        "小規模でのテスト運用後、\n本格的に現場導入。\n必要に応じてレクチャーなども\n実施します。",
        "定期的なご報告会を設け、\n細かいアップデートを\n繰り返しながら定着まで\n伴走支援いたします。",
    ]
    for i, body in enumerate(bodies):
        x = 140 + i * 290
        shapes.append(text_box(x, 650, 255, 260, body, 16, BLACK, False))
    shapes += footer(page)
    return shapes


def comparison(page: int) -> list[str]:
    shapes = [*title("Chapter3", "他社比較・社内稟議での判断軸")]
    headers = [("判断軸", 90, 335), ("一般的なパッケージ導入", 465, 570), ("Field Xで開発する場合", 1085, 690)]
    for h, x, w in headers:
        shapes.append(pill(x, 210, w, 58, h))
    rows = [
        ("業務適合", "既存機能に業務を寄せる必要がある", "貴社の業務フロー・承認・帳票に合わせて設計"),
        ("現場定着", "画面や操作が合わず利用が限定される可能性", "担当者様の使い方を前提にモックから改善"),
        ("AI拡張", "個別AI連携は追加開発・制約が出やすい", "基幹データを起点にAI音声対応・営業支援AIまで展開"),
        ("社内説明", "導入効果や運用イメージを別途整理する必要", "スクショ資料・要件資料・進め方を一式で提示"),
    ]
    y = 315
    for axis, pkg, fx in rows:
        shapes += [
            shape(90, y, 335, 118, "roundRect", GRAY, LINE),
            shape(465, y, 570, 118, "roundRect", GRAY, LINE),
            shape(1085, y, 690, 118, "roundRect", LIGHT_RED, RED, 2),
            text_box(118, y + 39, 180, 32, axis, 21, BLACK, True),
            text_box(495, y + 27, 500, 58, pkg, 17, TEXT),
            text_box(1118, y + 27, 615, 58, fx, 17, TEXT),
        ]
        y += 138
    shapes += footer(page)
    return shapes


def future_ai(page: int) -> list[str]:
    shapes = [*title("Chapter3", "基幹管理システムを起点に、社内AIへ展開可能")]
    shapes += [*dashboard_ui(115, 235, 770, 610)]
    shapes += [
        shape(1070, 500, 250, 120, "ellipse", RED, RED, text="基幹データ\n社内AI基盤", size=22, color=WHITE, bold=True, align="c", valign="m"),
    ]
    nodes = [
        (930, 270, "AI音声対応", "入居者様問い合わせ"),
        (1325, 270, "営業支援AI", "訪問前ブリーフィング"),
        (930, 735, "契約書自動作成", "文書作成を省力化"),
        (1325, 735, "社内FAQ検索", "横断検索・ナレッジ化"),
    ]
    for x, y, h, b in nodes:
        shapes += [
            shape(x, y, 285, 112, "roundRect", GRAY, LINE),
            text_box(x + 22, y + 24, 220, 28, h, 18, RED, True),
            text_box(x + 22, y + 65, 220, 22, b, 13, TEXT),
        ]
    shapes += [
        pill(1510, 430, 270, 58, "展開イメージ"),
        text_box(1510, 520, 320, 270, bullet_text(["入居者様問い合わせの一次対応", "オーナー様訪問前の情報整理", "契約書・通知文の下書き", "社内情報を便利FAQ化"]), 18, BLACK, True),
        *footer(page),
    ]
    return shapes


def next_actions(page: int) -> list[str]:
    shapes = [*title("Next", "今後ご提示予定の資料")]
    items = [
        ("01", "改善版モック", "今回いただいたご意見を反映し、画面・操作・ステータスの見え方を作り込みます。"),
        ("02", "機能・要件説明資料", "スクリーンショットごとに、必要機能・データ項目・運用イメージを整理します。"),
        ("03", "開発計画", "ご契約後の要件定義、設計、開発、テスト、導入、改善の流れを具体化します。"),
    ]
    y = 245
    for num, h, b in items:
        shapes += [
            text_box(140, y, 90, 58, num, 40, RED, True),
            text_box(285, y + 8, 560, 42, h, 28, BLACK, True),
            text_box(290, y + 70, 1220, 52, b, 21, MUTED),
        ]
        y += 215
    shapes += [
        shape(120, 895, 1640, 76, "roundRect", RED, RED),
        text_box(150, 916, 1500, 34, "まずは、社内稟議・他社比較で使える状態まで、モックと画面別説明資料を整えます。", 21, WHITE, True),
        *footer(page),
    ]
    return shapes


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


def slide_xml(shapes: list[str]) -> str:
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld><p:spTree>
    <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
    <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
    {''.join(shapes)}
  </p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>'''


def rels(entries: list[tuple[str, str, str]]) -> str:
    rows = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>', '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">']
    for rid, typ, target in entries:
        rows.append(f'<Relationship Id="{rid}" Type="{typ}" Target="{target}"/>')
    rows.append("</Relationships>")
    return "".join(rows)


def write_pptx(out: Path):
    slide_count = len(SLIDES)
    overrides = "\n".join(
        f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
        for i in range(1, slide_count + 1)
    )
    content_types = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  <Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
  <Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
  <Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
  {overrides}
</Types>'''
    sld_ids = "".join(f'<p:sldId id="{255+i}" r:id="rId{i+1}"/>' for i in range(1, slide_count + 1))
    presentation = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>
  <p:sldIdLst>{sld_ids}</p:sldIdLst>
  <p:sldSz cx="{CX}" cy="{CY}" type="wide"/>
  <p:notesSz cx="6858000" cy="9144000"/>
</p:presentation>'''
    pres_rels = [("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster", "slideMasters/slideMaster1.xml")]
    for i in range(1, slide_count + 1):
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
  <Application>Codex</Application><PresentationFormat>On-screen Show (16:9)</PresentationFormat><Slides>{slide_count}</Slides>
</Properties>'''
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as z:
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
        for i, (_, builder) in enumerate(SLIDES, start=1):
            D.reset()
            z.writestr(f"ppt/slides/slide{i}.xml", slide_xml(builder(i)))
            z.writestr(f"ppt/slides/_rels/slide{i}.xml.rels", rels([
                ("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout", "../slideLayouts/slideLayout1.xml"),
            ]))


def write_logs() -> None:
    plan = ["# Editable Slide Plan", ""]
    for i, (title, _) in enumerate(SLIDES, start=1):
        plan.append(f"{i:02d}. {title}")
    (PROJECT / "editable_slide_plan.md").write_text("\n".join(plan), encoding="utf-8")


def main() -> None:
    write_pptx(OUT)
    write_logs()
    print(OUT)


if __name__ == "__main__":
    main()
