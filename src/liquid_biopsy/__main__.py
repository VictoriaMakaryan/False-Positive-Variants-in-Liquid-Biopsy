"""CSV interface for the research rules. No row contents are logged."""

import argparse
from pathlib import Path

import pandas as pd

from .triage import classify_variants


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="CSV containing original-scale evidence")
    parser.add_argument("--output", type=Path, required=True, help="New output CSV path")
    args = parser.parse_args()
    try:
        if args.output.exists():
            raise FileExistsError("Output already exists; choose a new output path")
        result = classify_variants(pd.read_csv(args.input))
        with args.output.open("x", encoding="utf-8", newline="") as handle:
            result.to_csv(handle, index=False)
    except (OSError, ValueError, TypeError) as exc:
        parser.exit(2, f"variant-triage: {exc}\n")
    print("Research rules only; not validated for clinical use.")
    print(f"Processed {len(result)} rows.")
    for label in ("AUTO-PASS", "AUTO-REJECT", "MANUAL_REVIEW"):
        print(f"{label}: {(result['final_classification'] == label).sum()}")


if __name__ == "__main__":
    main()
