from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    print("Pipeline scaffold is prepared.")
    print(f"Project root: {root}")
    print("Open outputs/05_final/index.html in a browser to review the current result.")


if __name__ == "__main__":
    main()

