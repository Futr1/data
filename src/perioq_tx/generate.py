from __future__ import annotations

import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path

from src.utils.config import ensure_parent, load_yaml, resolve_path


def generate_xml(filtered_payload: dict, output_path: str | Path) -> Path:
    query = filtered_payload.get("query", {})
    candidates = filtered_payload.get("candidates", [])
    if not candidates:
        raise ValueError("No filtered candidates available for draft generation")

    best = candidates[0]
    root = ET.Element("perioq_tx_draft")
    ET.SubElement(root, "diagnosis_label").text = query.get("diagnosis_label", "")
    ET.SubElement(root, "query_text").text = query.get("text", "")
    ET.SubElement(root, "scheme_id").text = best.get("scheme_id", "")
    ET.SubElement(root, "title").text = best.get("title", "")

    rationale = ET.SubElement(root, "rationale")
    rationale.text = (
        "Diagnosis label matched the curated scheme library and no listed contraindication "
        "was triggered by the provided patient flags."
    )

    steps = ET.SubElement(root, "recommended_steps")
    for step in best.get("recommended_steps", []):
        ET.SubElement(steps, "step").text = str(step)

    follow_up = ET.SubElement(root, "follow_up")
    for item in best.get("follow_up", []):
        ET.SubElement(follow_up, "item").text = str(item)

    tree = ET.ElementTree(root)
    path = ensure_parent(output_path)
    tree.write(path, encoding="utf-8", xml_declaration=True)
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate a constrained XML draft from filtered candidates.")
    parser.add_argument("--config")
    parser.add_argument("--input")
    parser.add_argument("--output")
    args = parser.parse_args(argv)

    config = load_yaml(args.config) if args.config else {}
    input_path = args.input or config.get("filtered_output")
    output_path = args.output or config.get("draft_output")
    if not input_path or not output_path:
        raise ValueError("Input and output paths are required")

    with resolve_path(input_path).open("r", encoding="utf-8") as handle:
        filtered_payload = json.load(handle)
    xml_path = generate_xml(filtered_payload, output_path)
    print(xml_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
