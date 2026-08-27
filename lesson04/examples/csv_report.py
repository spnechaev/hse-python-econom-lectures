"""Print total sales by category from a CSV file."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def totals_by_category(path: Path) -> dict[str, int]:
    totals: dict[str, int] = {}
    with path.open(encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source)
        for row in reader:
            category = row["category"]
            amount = int(row["amount"])
            totals[category] = totals.get(category, 0) + amount
    return totals


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    for category, total in totals_by_category(args.path).items():
        print(f"{category}: {total}")


if __name__ == "__main__":
    main()
