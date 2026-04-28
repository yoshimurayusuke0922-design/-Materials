#!/usr/bin/env python
"""Rebuild a thin slide sidebar in a raster PNG without crushing text."""

from __future__ import annotations

import argparse
from pathlib import Path
from statistics import median

from PIL import Image, ImageDraw, ImageFont


def font_path(preferred: str | None = None) -> str:
    candidates = [
        preferred,
        r"C:\Windows\Fonts\YuGothB.ttc",
        r"C:\Windows\Fonts\meiryob.ttc",
        r"C:\Windows\Fonts\BIZ-UDGothicB.ttc",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate
    raise FileNotFoundError("No suitable font found. Pass --font explicitly.")


def centered_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, center_x: float, center_y: float) -> None:
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    draw.text((center_x - width / 2 - bbox[0], center_y - height / 2 - bbox[1]), text, font=font, fill=(255, 255, 255))


def make_canvas(image: Image.Image, source_rail_width: int, target_rail_width: int) -> Image.Image:
    if source_rail_width == target_rail_width:
        return image.copy()

    width, height = image.size
    delta = source_rail_width - target_rail_width
    if delta < 0:
        raise ValueError("This script supports narrowing sidebars. Keep source width >= target width.")
    if source_rail_width >= width or target_rail_width <= 0:
        raise ValueError("Invalid sidebar width for this image.")

    result = Image.new("RGB", (width, height))
    body = image.crop((source_rail_width, 0, width, height))
    result.paste(body, (target_rail_width, 0))

    if delta:
        edge_fill = image.crop((width - delta, 0, width, height))
        result.paste(edge_fill, (width - delta, 0))

    return result


def sampled_rail(image: Image.Image, width: int, height: int) -> Image.Image:
    row_colors: list[tuple[int, int, int]] = []
    sample_width = min(width, image.size[0])
    for y in range(height):
        samples = []
        for x in range(sample_width):
            red, green, blue = image.getpixel((x, y))
            if red > 140 and green < 90 and blue < 90:
                samples.append((red, green, blue))
        if samples:
            row_colors.append(tuple(int(median(channel)) for channel in zip(*samples)))
        else:
            t = y / max(height - 1, 1)
            row_colors.append((int(246 - 18 * t), 0, 0))

    rail = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(rail)
    for y, color in enumerate(row_colors):
        draw.line((0, y, width - 1, y), fill=color)

    for x, alpha in [(width - 3, 0.12), (width - 2, 0.20), (width - 1, 0.34)]:
        if x < 0:
            continue
        for y in range(height):
            base = rail.getpixel((x, y))
            rail.putpixel((x, y), tuple(int(channel * (1 - alpha)) for channel in base))

    return rail


def render_sidebar(image: Image.Image, args: argparse.Namespace) -> Image.Image:
    width, height = image.size
    target = args.target_rail_width
    base_font = font_path(args.font)

    rail = sampled_rail(image, target, height)
    draw = ImageDraw.Draw(rail)

    label_size = args.chapter_label_size or max(9, round(target * 0.18))
    number_size = args.chapter_number_size or max(24, round(target * 0.66))
    copy_size = args.copy_size or max(8, round(target * 0.16))
    page_size = args.page_size or max(18, round(target * 0.45))

    chapter_font = ImageFont.truetype(base_font, label_size)
    number_font = ImageFont.truetype(base_font, number_size)
    copy_font = ImageFont.truetype(base_font, copy_size)
    page_font = ImageFont.truetype(base_font, page_size)

    centered_text(draw, args.chapter_label, chapter_font, target / 2, args.chapter_label_y)
    centered_text(draw, args.chapter_number, number_font, target / 2, args.chapter_number_y)

    line_pad = max(16, round(target * 0.27))
    draw.line((line_pad, args.chapter_line_y, target - line_pad, args.chapter_line_y), fill=(255, 255, 255), width=args.line_width)

    bbox = draw.multiline_textbbox((0, 0), args.copy_text, font=copy_font, spacing=args.copy_spacing)
    copy_img = Image.new("RGBA", (bbox[2] - bbox[0] + 4, bbox[3] - bbox[1] + 4), (0, 0, 0, 0))
    copy_draw = ImageDraw.Draw(copy_img)
    copy_draw.multiline_text((2 - bbox[0], 2 - bbox[1]), args.copy_text, font=copy_font, fill=(255, 255, 255, 255), spacing=args.copy_spacing)
    rotated = copy_img.rotate(270, expand=True, resample=Image.Resampling.BICUBIC)
    rail.paste(rotated.convert("RGB"), ((target - rotated.width) // 2, args.copy_y), rotated)

    draw.line((line_pad, args.page_line_y, target - line_pad, args.page_line_y), fill=(255, 255, 255), width=args.line_width)
    centered_text(draw, args.page_number, page_font, target / 2, args.page_number_y)

    result = image.copy()
    result.paste(rail, (0, 0))
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--source-rail-width", required=True, type=int)
    parser.add_argument("--target-rail-width", required=True, type=int)
    parser.add_argument("--chapter-label", default="Chapter3")
    parser.add_argument("--chapter-number", default="03")
    parser.add_argument("--page-number", default="12")
    parser.add_argument("--copy-text", default="Copyright @Field X inc.\nAll rights reserved.")
    parser.add_argument("--font", default=None)
    parser.add_argument("--chapter-label-size", type=int, default=None)
    parser.add_argument("--chapter-number-size", type=int, default=None)
    parser.add_argument("--copy-size", type=int, default=None)
    parser.add_argument("--page-size", type=int, default=None)
    parser.add_argument("--chapter-label-y", type=int, default=70)
    parser.add_argument("--chapter-number-y", type=int, default=126)
    parser.add_argument("--chapter-line-y", type=int, default=161)
    parser.add_argument("--copy-y", type=int, default=590)
    parser.add_argument("--page-line-y", type=int, default=837)
    parser.add_argument("--page-number-y", type=int, default=880)
    parser.add_argument("--copy-spacing", type=int, default=3)
    parser.add_argument("--line-width", type=int, default=3)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    image = Image.open(args.input).convert("RGB")
    canvas = make_canvas(image, args.source_rail_width, args.target_rail_width)
    result = render_sidebar(canvas, args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.save(args.output)
    print(args.output.resolve())


if __name__ == "__main__":
    main()
