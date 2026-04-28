from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "out" / "sanko_html" / "slide_images" / "12_roadmap_reference.png"

W, H = 1672, 941
SCALE = 2
RED = (246, 0, 0)
RED_DARK = (216, 0, 0)
TEXT = (22, 22, 22)
MUTED = (36, 36, 36)


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    paths = {
        "bold": [
            r"C:\Windows\Fonts\YuGothB.ttc",
            r"C:\Windows\Fonts\meiryob.ttc",
            r"C:\Windows\Fonts\BIZ-UDGothicB.ttc",
        ],
        "regular": [
            r"C:\Windows\Fonts\YuGothM.ttc",
            r"C:\Windows\Fonts\meiryo.ttc",
            r"C:\Windows\Fonts\BIZ-UDGothicR.ttc",
        ],
    }
    for candidate in paths[name]:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size * SCALE)
    raise FileNotFoundError(f"No font for {name}")


def xy(value: int | float) -> int:
    return round(value * SCALE)


def box(rect: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    return tuple(xy(v) for v in rect)


def text_center(
    draw: ImageDraw.ImageDraw,
    center: tuple[int, int],
    value: str,
    face: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
    spacing: int = 0,
) -> None:
    bbox = draw.multiline_textbbox((0, 0), value, font=face, spacing=xy(spacing), align="center")
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.multiline_text(
        (xy(center[0]) - tw / 2 - bbox[0], xy(center[1]) - th / 2 - bbox[1]),
        value,
        font=face,
        fill=fill,
        spacing=xy(spacing),
        align="center",
    )


def draw_shadowed_round(
    canvas: Image.Image,
    rect: tuple[int, int, int, int],
    radius: int,
    fill: tuple[int, int, int],
    shadow: int = 18,
) -> None:
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rounded_rectangle(box(rect), radius=xy(radius), fill=(0, 0, 0, 42))
    blurred = layer.filter(ImageFilter.GaussianBlur(xy(shadow)))
    canvas.alpha_composite(blurred, (0, xy(6)))
    ImageDraw.Draw(canvas).rounded_rectangle(box(rect), radius=xy(radius), fill=fill + (255,))


def draw_red_rail(canvas: Image.Image) -> None:
    rail_w = 67
    rail = Image.new("RGBA", (xy(rail_w), xy(H)), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rail)
    for y in range(xy(H)):
        t = y / max(xy(H) - 1, 1)
        r = int(246 * (1 - t) + 222 * t)
        rd.line((0, y, xy(rail_w), y), fill=(r, 0, 0, 255))
    rd.line((xy(rail_w - 1), 0, xy(rail_w - 1), xy(H)), fill=(135, 0, 0, 180), width=xy(2))
    canvas.alpha_composite(rail)

    d = ImageDraw.Draw(canvas)
    text_center(d, (33, 70), "Chapter3", font("bold", 12), (255, 255, 255))
    text_center(d, (33, 126), "03", font("bold", 44), (255, 255, 255))
    d.line((xy(18), xy(162), xy(49), xy(162)), fill=(255, 255, 255), width=xy(3))

    copy = "Copyright @Field X inc.\nAll rights reserved."
    copy_face = font("bold", 26)
    tmp = Image.new("RGBA", (xy(540), xy(96)), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    tb = td.multiline_textbbox((0, 0), copy, font=copy_face, spacing=xy(2), align="left")
    td.multiline_text((xy(4) - tb[0], xy(4) - tb[1]), copy, font=copy_face, fill=(255, 255, 255), spacing=xy(2))
    rotated = tmp.crop(tmp.getbbox()).rotate(270, expand=True, resample=Image.Resampling.BICUBIC)
    canvas.alpha_composite(rotated, (xy((67 - rotated.width / SCALE) / 2), xy(260)))

    d.line((xy(18), xy(837), xy(49), xy(837)), fill=(255, 255, 255), width=xy(3))
    text_center(d, (33, 881), "12", font("bold", 30), (255, 255, 255))


def draw_step_circle(canvas: Image.Image, center: tuple[int, int], num: str) -> None:
    cx, cy = center
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.ellipse(box((cx - 64, cy - 64, cx + 64, cy + 64)), fill=(0, 0, 0, 35))
    blur = layer.filter(ImageFilter.GaussianBlur(xy(8)))
    canvas.alpha_composite(blur, (0, xy(8)))

    d = ImageDraw.Draw(canvas)
    d.ellipse(box((cx - 64, cy - 64, cx + 64, cy + 64)), fill=(252, 252, 252), outline=(228, 228, 228), width=xy(3))
    d.ellipse(box((cx - 54, cy - 54, cx + 54, cy + 54)), outline=(238, 238, 238), width=xy(4))
    d.arc(box((cx - 58, cy - 58, cx + 58, cy + 58)), start=282, end=24, fill=RED, width=xy(6))
    text_center(d, center, num, font("bold", 48), RED)


def draw_dots(canvas: Image.Image, left: int, right: int, y: int) -> None:
    d = ImageDraw.Draw(canvas)
    for x in range(left, right + 1, 16):
        d.ellipse(box((x - 2, y - 2, x + 2, y + 2)), fill=RED)
    d.ellipse(box(((left + right) // 2 - 6, y - 6, (left + right) // 2 + 6, y + 6)), fill=RED)


def draw_arrow(canvas: Image.Image, rect: tuple[int, int, int, int], label: str) -> None:
    x0, y0, x1, y1 = rect
    notch = 36
    point = 34
    pts = [
        (xy(x0), xy(y0)),
        (xy(x1 - point), xy(y0)),
        (xy(x1), xy((y0 + y1) / 2)),
        (xy(x1 - point), xy(y1)),
        (xy(x0), xy(y1)),
        (xy(x0 + notch), xy((y0 + y1) / 2)),
    ]
    d = ImageDraw.Draw(canvas)
    d.polygon(pts, fill=RED)
    d.line((xy(x0 + 8), xy(y0), xy(x1 - point - 6), xy(y0)), fill=(255, 70, 70), width=xy(2))
    text_center(d, ((x0 + x1) // 2 + 6, (y0 + y1) // 2), label, font("bold", 29), (255, 255, 255), spacing=1)


def draw_paragraph(draw: ImageDraw.ImageDraw, x: int, y: int, lines: list[str], size: int = 22, line_h: int = 34) -> None:
    face = font("regular", size)
    for i, line in enumerate(lines):
        draw.text((xy(x), xy(y + i * line_h)), line, font=face, fill=TEXT)


def make_slide() -> Image.Image:
    canvas = Image.new("RGBA", (xy(W), xy(H)), (0, 0, 0, 255))
    d = ImageDraw.Draw(canvas)

    for y in range(xy(H)):
        t = y / max(xy(H) - 1, 1)
        base = int(250 * (1 - t) + 242 * t)
        d.line((0, y, xy(W), y), fill=(base, base, base, 255))

    draw_red_rail(canvas)

    d.text((xy(116), xy(48)), "Chapter3", font=font("bold", 27), fill=RED)
    d.text((xy(116), xy(92)), "今後の進め方", font=font("bold", 54), fill=TEXT)
    d.text(
        (xy(116), xy(184)),
        "繁忙期であると推察されますので、できる限り現場の混乱を避け円滑に進めるため、下記のような流れで進めさせていただければ幸いです",
        font=font("regular", 25),
        fill=MUTED,
    )

    draw_shadowed_round(canvas, (104, 254, 1598, 882), 18, (255, 255, 255), shadow=14)

    centers = [246, 494, 742, 990, 1238, 1486]
    for idx, cx in enumerate(centers, start=1):
        draw_step_circle(canvas, (cx, 356), f"{idx:02d}")
    for left, right in zip([306, 554, 802, 1050, 1298], [434, 682, 930, 1178, 1426]):
        draw_dots(canvas, left, right, 356)

    arrow_y0, arrow_y1 = 455, 537
    arrows = [
        (128, arrow_y0, 398, arrow_y1, "ご契約"),
        (376, arrow_y0, 646, arrow_y1, "進め方の確認"),
        (624, arrow_y0, 894, arrow_y1, "データ移行先\nの準備"),
        (872, arrow_y0, 1142, arrow_y1, "システム\n開発"),
        (1120, arrow_y0, 1390, arrow_y1, "現場導入"),
        (1368, arrow_y0, 1590, arrow_y1, "改善"),
    ]
    for x0, y0, x1, y1, label in arrows:
        draw_arrow(canvas, (x0, y0, x1, y1), label)

    columns = [
        (128, [
            "NDAや個別契約など各",
            "種ご契約を締結させて",
            "いただきます。",
            "",
            "※御社フォーマットなどが",
            "　ございましたら",
            "　ご都合に合わせて",
            "　対応いたします。",
        ]),
        (376, [
            "必要可否も含め、",
            "なるべく現場の従業員",
            "の方の混乱を起こさない",
            "ように、",
            "今後の詳細なプランニ",
            "ングをご提案し、貴社サ",
            "イドとすり合わせます。",
        ]),
        (624, [
            "データマイグレーション",
            "を実行する場合、",
            "移行先を先に準備するこ",
            "とが最重要です。",
            "以後発生するデータを格",
            "納する箱を準備いたしま",
            "す。",
        ]),
        (862, [
            "03と同時並行的に",
            "弊社でシステムを開発",
            "いたします。",
            "毎週のご報告会を行い",
            "ながら使用感やUIなど",
            "をすり合わせながら",
            "開発を進めます。",
        ]),
        (1104, [
            "小規模でのテスト運用",
            "後、本格的に現場導入",
            "をいたします。",
            "必要に応じて現場での",
            "レクチャーなどを実施い",
            "たします。",
        ]),
        (1348, [
            "定期的なご報告会を設",
            "け、細かいアップデート",
            "を繰り返しながら現場で",
            "定着するまで伴走支援",
            "いたします。",
        ]),
    ]
    for x, lines in columns:
        draw_paragraph(d, x, 582, lines, size=20, line_h=33)

    return canvas.resize((W, H), Image.Resampling.LANCZOS).convert("RGB")


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    make_slide().save(OUT)
    print(OUT)
