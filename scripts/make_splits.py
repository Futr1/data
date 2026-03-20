from __future__ import annotations

import argparse
import csv
import random
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.utils.config import resolve_path


def _write_ids(path: Path, rows: list[dict[str, str]], id_column: str) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=[id_column, "split"])
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create patient-level train/val/test split CSV files.")
    parser.add_argument("--input", required=True, help="CSV file containing patient IDs.")
    parser.add_argument("--id-column", default="patient_id")
    parser.add_argument("--train-ratio", type=float, default=0.7)
    parser.add_argument("--val-ratio", type=float, default=0.2)
    parser.add_argument("--test-ratio", type=float, default=0.1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output-dir", default="metadata/generated_splits")
    args = parser.parse_args()

    total_ratio = args.train_ratio + args.val_ratio + args.test_ratio
    if round(total_ratio, 6) != 1.0:
        raise ValueError("Train, validation, and test ratios must sum to 1.0")

    input_path = resolve_path(args.input)
    output_dir = resolve_path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with input_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        ids = [row[args.id_column] for row in reader]

    rng = random.Random(args.seed)
    rng.shuffle(ids)

    total = len(ids)
    train_cut = int(total * args.train_ratio)
    val_cut = train_cut + int(total * args.val_ratio)

    train_ids = ids[:train_cut]
    val_ids = ids[train_cut:val_cut]
    test_ids = ids[val_cut:]

    _write_ids(
        output_dir / "train_ids.csv",
        [{args.id_column: item, "split": "train"} for item in train_ids],
        args.id_column,
    )
    _write_ids(
        output_dir / "val_ids.csv",
        [{args.id_column: item, "split": "validation"} for item in val_ids],
        args.id_column,
    )
    _write_ids(
        output_dir / "test_ids.csv",
        [{args.id_column: item, "split": "independent_test"} for item in test_ids],
        args.id_column,
    )

    summary_path = output_dir / "split_summary.csv"
    with summary_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["split", "count"])
        writer.writeheader()
        writer.writerows(
            [
                {"split": "train", "count": len(train_ids)},
                {"split": "validation", "count": len(val_ids)},
                {"split": "independent_test", "count": len(test_ids)},
            ]
        )

    print(output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
