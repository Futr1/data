from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.periom_dx import evaluate as periom_evaluate
from src.perioq_tx import evaluate as perioq_evaluate


def main() -> int:
    parser = argparse.ArgumentParser(description="Unified evaluation entry point.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    dx_parser = subparsers.add_parser("periom-dx")
    dx_parser.add_argument("--predictions", required=True)
    dx_parser.add_argument("--references", required=True)
    dx_parser.add_argument("--output")

    tx_parser = subparsers.add_parser("perioq-tx")
    tx_parser.add_argument("--input", required=True)
    tx_parser.add_argument("--draft-xml")
    tx_parser.add_argument("--top-k", type=int, default=3)
    tx_parser.add_argument("--output")

    args = parser.parse_args()

    if args.command == "periom-dx":
        argv = ["--predictions", args.predictions, "--references", args.references]
        if args.output:
            argv.extend(["--output", args.output])
        return periom_evaluate.main(argv)

    argv = ["--input", args.input, "--top-k", str(args.top_k)]
    if args.draft_xml:
        argv.extend(["--draft-xml", args.draft_xml])
    if args.output:
        argv.extend(["--output", args.output])
    return perioq_evaluate.main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
