from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.periom_dx import train_grpo, train_sft
from src.perioq_tx import build_index


def main() -> int:
    parser = argparse.ArgumentParser(description="Unified training and indexing entry point.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    sft_parser = subparsers.add_parser("periom-dx-sft")
    sft_parser.add_argument("--config", default="configs/periom_dx_sft.yaml")
    sft_parser.add_argument("--dry-run", action="store_true")

    grpo_parser = subparsers.add_parser("periom-dx-grpo")
    grpo_parser.add_argument("--config", default="configs/periom_dx_grpo.yaml")
    grpo_parser.add_argument("--dry-run", action="store_true")

    index_parser = subparsers.add_parser("perioq-tx-index")
    index_parser.add_argument("--config", default="configs/perioq_tx.yaml")

    args = parser.parse_args()

    if args.command == "periom-dx-sft":
        argv = ["--config", args.config]
        if args.dry_run:
            argv.append("--dry-run")
        return train_sft.main(argv)

    if args.command == "periom-dx-grpo":
        argv = ["--config", args.config]
        if args.dry_run:
            argv.append("--dry-run")
        return train_grpo.main(argv)

    return build_index.main(["--config", args.config])


if __name__ == "__main__":
    raise SystemExit(main())
