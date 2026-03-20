from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.periom_dx.dataset import load_records, save_records, to_sft_record


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert normalized repository samples into SFT-ready records.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--system-prompt")
    args = parser.parse_args()

    records = load_records(args.input)
    processed = [to_sft_record(record, args.system_prompt) for record in records]
    output_path = save_records(args.output, processed)
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
