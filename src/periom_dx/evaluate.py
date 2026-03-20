from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from src.periom_dx.dataset import extract_answer, load_records
from src.utils.config import ensure_parent, resolve_path


def _load_json(path_like: str | Path) -> Any:
    path = resolve_path(path_like)
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def _extract_prediction(item: dict[str, Any]) -> str:
    if "prediction" in item:
        return extract_answer(str(item["prediction"]))
    if "predicted_answer" in item:
        return extract_answer(str(item["predicted_answer"]))
    if "answer" in item:
        return extract_answer(str(item["answer"]))
    if "output" in item and isinstance(item["output"], dict):
        return extract_answer(str(item["output"].get("answer", "")))
    return ""


def _prediction_map(path_like: str | Path) -> dict[str, str]:
    data = _load_json(path_like)
    if not isinstance(data, list):
        raise ValueError("Prediction file must be a JSON list")
    return {str(item["id"]): _extract_prediction(item) for item in data}


def evaluate(predictions_path: str | Path, references_path: str | Path) -> dict[str, Any]:
    predictions = _prediction_map(predictions_path)
    references = {record["id"]: record["target"]["answer"] for record in load_records(references_path)}

    compared = 0
    correct = 0
    missing: list[str] = []
    for record_id, answer in references.items():
        if record_id not in predictions:
            missing.append(record_id)
            continue
        compared += 1
        if predictions[record_id] == answer:
            correct += 1

    accuracy = (correct / compared) if compared else 0.0
    coverage = (compared / len(references)) if references else 0.0
    return {
        "num_references": len(references),
        "num_compared": compared,
        "num_correct": correct,
        "accuracy": round(accuracy, 6),
        "coverage": round(coverage, 6),
        "missing_prediction_ids": missing,
        "scoring_rule": "answer_only",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate PerioM-Dx predictions using answer-only matching.")
    parser.add_argument("--predictions", required=True)
    parser.add_argument("--references", required=True)
    parser.add_argument("--output")
    args = parser.parse_args(argv)

    metrics = evaluate(args.predictions, args.references)
    print(json.dumps(metrics, ensure_ascii=False, indent=2))
    if args.output:
        output_path = ensure_parent(args.output)
        with output_path.open("w", encoding="utf-8") as handle:
            json.dump(metrics, handle, ensure_ascii=False, indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
