from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from src.utils.config import ensure_parent, load_yaml, resolve_path


def filter_candidates(
    payload: dict[str, Any],
    diagnosis_label: str,
    patient_flags: list[str],
    min_score: float,
) -> dict[str, Any]:
    flags = {flag for flag in patient_flags if flag and flag != "none"}
    filtered = []
    for candidate in payload.get("candidates", []):
        if candidate.get("diagnosis_label") != diagnosis_label:
            continue
        if float(candidate.get("score", 0.0)) < min_score:
            continue
        contraindications = set(candidate.get("contraindications", []))
        if flags & contraindications:
            continue
        filtered.append(candidate)
    return {
        "query": payload.get("query", {}),
        "patient_flags": sorted(flags),
        "candidates": filtered,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Filter retrieved quality-scheme candidates.")
    parser.add_argument("--config")
    parser.add_argument("--input")
    parser.add_argument("--output")
    parser.add_argument("--diagnosis-label")
    parser.add_argument("--patient-flags", nargs="*", default=None)
    parser.add_argument("--min-score", type=float, default=0.0)
    args = parser.parse_args(argv)

    config = load_yaml(args.config) if args.config else {}
    input_path = args.input or config.get("retrieval_output")
    output_path = args.output or config.get("filtered_output")
    diagnosis_label = args.diagnosis_label or config.get("query", {}).get("diagnosis_label")
    patient_flags = args.patient_flags if args.patient_flags is not None else config.get("patient_flags", [])
    if not input_path or not output_path or not diagnosis_label:
        raise ValueError("Input, output, and diagnosis label are required")

    with resolve_path(input_path).open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    filtered = filter_candidates(payload, diagnosis_label, patient_flags, args.min_score)
    print(json.dumps(filtered, ensure_ascii=False, indent=2))
    output = ensure_parent(output_path)
    with output.open("w", encoding="utf-8") as handle:
        json.dump(filtered, handle, ensure_ascii=False, indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
