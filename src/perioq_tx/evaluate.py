from __future__ import annotations

import argparse
import json
import math
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from src.utils.config import ensure_parent, resolve_path


def _dcg(rank: int) -> float:
    return 1.0 / math.log2(rank + 1)


def evaluate_retrieval(items: list[dict[str, Any]], top_k: int) -> dict[str, Any]:
    if not items:
        return {"num_queries": 0, "hit_rate_at_k": 0.0, "mrr": 0.0, "ndcg": 0.0}

    hits = 0
    reciprocal_ranks = []
    dcg_scores = []
    counted = 0

    for item in items:
        gold = item.get("gold_scheme_id")
        if not gold:
            continue
        counted += 1
        ranked = [candidate.get("scheme_id") for candidate in item.get("candidates", [])]
        if gold in ranked[:top_k]:
            hits += 1
        if gold in ranked:
            rank = ranked.index(gold) + 1
            reciprocal_ranks.append(1.0 / rank)
            dcg_scores.append(_dcg(rank))
        else:
            reciprocal_ranks.append(0.0)
            dcg_scores.append(0.0)

    if counted == 0:
        return {
            "num_queries": len(items),
            "num_scored_queries": 0,
            "hit_rate_at_k": 0.0,
            "mrr": 0.0,
            "ndcg": 0.0,
        }

    return {
        "num_queries": len(items),
        "num_scored_queries": counted,
        "hit_rate_at_k": round(hits / counted, 6),
        "mrr": round(sum(reciprocal_ranks) / counted, 6),
        "ndcg": round(sum(dcg_scores) / counted, 6),
    }


def evaluate_schema_adherence(xml_path: str | Path | None) -> dict[str, Any]:
    if not xml_path:
        return {"schema_adherence": None}
    root = ET.parse(resolve_path(xml_path)).getroot()
    required = ["diagnosis_label", "scheme_id", "recommended_steps", "follow_up"]
    adherence = all(root.find(name) is not None for name in required)
    return {"schema_adherence": adherence}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate PerioQ-Tx retrieval and draft structure.")
    parser.add_argument("--input", required=True, help="JSON file containing one item or a list of items.")
    parser.add_argument("--draft-xml")
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--output")
    args = parser.parse_args(argv)

    with resolve_path(args.input).open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    items = payload if isinstance(payload, list) else [payload]

    metrics = evaluate_retrieval(items, args.top_k)
    metrics.update(evaluate_schema_adherence(args.draft_xml))
    print(json.dumps(metrics, ensure_ascii=False, indent=2))
    if args.output:
        output = ensure_parent(args.output)
        with output.open("w", encoding="utf-8") as handle:
            json.dump(metrics, handle, ensure_ascii=False, indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
