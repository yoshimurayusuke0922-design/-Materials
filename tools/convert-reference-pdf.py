import argparse
from pathlib import Path

import fitz


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render each PDF page into numbered PNG slide images."
    )
    parser.add_argument("--pdf", required=True, help="Input PDF path")
    parser.add_argument("--out", required=True, help="Output slides directory")
    parser.add_argument("--dpi", type=int, default=180, help="Render DPI")
    parser.add_argument(
        "--prefix",
        default="",
        help="Optional filename prefix, e.g. slide- for slide-01.png",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing PNG files",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    pdf_path = Path(args.pdf).resolve()
    out_dir = Path(args.out).resolve()

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    out_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)
    width = max(2, len(str(len(doc))))
    scale = args.dpi / 72
    matrix = fitz.Matrix(scale, scale)

    written = []
    for index, page in enumerate(doc, start=1):
        filename = f"{args.prefix}{index:0{width}d}.png"
        out_path = out_dir / filename
        if out_path.exists() and not args.overwrite:
            raise FileExistsError(
                f"Refusing to overwrite existing file: {out_path}. "
                "Pass --overwrite to replace it."
            )
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        pix.save(out_path)
        written.append(out_path)

    print(f"Rendered {len(written)} page(s)")
    for path in written:
        print(path)


if __name__ == "__main__":
    main()
