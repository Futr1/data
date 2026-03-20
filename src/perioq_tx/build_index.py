from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from src.utils.config import ensure_parent, load_yaml, resolve_path


def load_library(path_like: str | Path) -> list[dict[str, Any]]:
    path = resolve_path(path_like)
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError(f"Expected a list of quality-scheme entries in {path}")
    return data


def normalize_entries(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for item in entries:
        normalized.append(
            {
                "scheme_id": item["scheme_id"],
                "diagnosis_label": item["diagnosis_label"],
                "title": item.get("title", ""),
                "keywords": item.get("keywords", []),
                "contraindications": item.get("contraindications", []),
                "recommended_steps": item.get("recommended_steps", []),
                "follow_up": item.get("follow_up", []),
                "source": item.get("source", ""),
            }
        )
    return normalized


def build_index(library_path: str | Path, output_path: str | Path) -> Path:
    entries = normalize_entries(load_library(library_path))
    payload = {
        "num_entries": len(entries),
        "entries": entries,
        "diagnosis_labels": sorted({entry["diagnosis_label"] for entry in entries}),
    }
    path = ensure_parent(output_path)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build a normalized quality-scheme index.")
    parser.add_argument("--config")
    parser.add_argument("--library")
    parser.add_argument("--output")
    args = parser.parse_args(argv)

    config = load_yaml(args.config) if args.config else {}
    library_path = args.library or config.get("library_path")
    output_path = args.output or config.get("index_output")
    if not library_path or not output_path:
        raise ValueError("Both library path and output path are required")

    built_path = build_index(library_path, output_path)
    print(built_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
