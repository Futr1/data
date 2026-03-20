from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from src.perioq_tx.build_index import load_library, normalize_entries
from src.utils.config import ensure_parent, load_yaml, resolve_path


TOKEN_PATTERN = re.compile(r"[a-z0-9_]+", re.IGNORECASE)


def _tokens(text: str) -> set[str]:
    return set(TOKEN_PATTERN.findall((text or "").lower()))


def _load_entries(index_path: str | Path | None, library_path: str | Path | None) -> list[dict[str, Any]]:
    if index_path and resolve_path(index_path).exists():
        with resolve_path(index_path).open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        return data.get("entries", [])
    if library_path:
        return normalize_entries(load_library(library_path))
    raise FileNotFoundError("No index or library path available for retrieval")


def _score(query_tokens: set[str], diagnosis_label: str, entry: dict[str, Any]) -> float:
    title_tokens = _tokens(entry.get("title", ""))
    keyword_tokens = set()
    for keyword in entry.get("keywords", []):
        keyword_tokens |= _tokens(str(keyword))
    step_tokens = set()
    for step in entry.get("recommended_steps", []):
        step_tokens |= _tokens(str(step))

    overlap = len(query_tokens & (title_tokens | keyword_tokens | step_tokens))
    diagnosis_bonus = 5 if entry.get("diagnosis_label") == diagnosis_label else 0
    return float(diagnosis_bonus + overlap)


def retrieve_candidates(
    entries: list[dict[str, Any]],
    diagnosis_label: str,
    query_text: str,
    top_k: int,
) -> dict[str, Any]:
    query_tokens = _tokens(query_text)
    scored = []
    for entry in entries:
        score = _score(query_tokens, diagnosis_label, entry)
        scored.append(
            {
                "scheme_id": entry["scheme_id"],
                "diagnosis_label": entry["diagnosis_label"],
                "title": entry.get("title", ""),
                "score": score,
                "contraindications": entry.get("contraindications", []),
                "recommended_steps": entry.get("recommended_steps", []),
                "follow_up": entry.get("follow_up", []),
                "source": entry.get("source", ""),
            }
        )
    ranked = sorted(scored, key=lambda item: (-item["score"], item["scheme_id"]))[:top_k]
    return {
        "query": {
            "diagnosis_label": diagnosis_label,
            "text": query_text,
        },
        "candidates": ranked,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Retrieve diagnosis-aware quality-scheme candidates.")
    parser.add_argument("--config")
    parser.add_argument("--index")
    parser.add_argument("--library")
    parser.add_argument("--diagnosis-label")
    parser.add_argument("--query")
    parser.add_argument("--top-k", type=int)
    parser.add_argument("--output")
    args = parser.parse_args(argv)

    config = load_yaml(args.config) if args.config else {}
    query_cfg = config.get("query", {})
    entries = _load_entries(args.index or config.get("index_output"), args.library or config.get("library_path"))
    diagnosis_label = args.diagnosis_label or query_cfg.get("diagnosis_label")
    query_text = args.query or query_cfg.get("text")
    top_k = args.top_k or int(config.get("top_k", 3))
    output = args.output or config.get("retrieval_output")
    if not diagnosis_label or not query_text:
        raise ValueError("Diagnosis label and query text are required")

    payload = retrieve_candidates(entries, diagnosis_label, query_text, top_k)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if output:
        output_path = ensure_parent(output)
        with output_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
