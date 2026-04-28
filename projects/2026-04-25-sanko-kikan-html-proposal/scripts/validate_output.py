from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    required = [
        root / "outputs/05_final/index.html",
        root / "outputs/05_final/style.css",
        root / "outputs/06_review/conversion_report.md",
    ]
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        print("Missing files:")
        for item in missing:
          print(item)
        raise SystemExit(1)
    print("All required final output files exist.")


if __name__ == "__main__":
    main()

