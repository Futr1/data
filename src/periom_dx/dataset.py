from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from src.utils.config import ensure_parent, resolve_path


ANSWER_PATTERN = re.compile(r"<answer>\s*(.*?)\s*</answer>", re.DOTALL | re.IGNORECASE)


def extract_answer(text: str) -> str:
    match = ANSWER_PATTERN.search(text or "")
    if match:
        return match.group(1).strip()
    return (text or "").strip()


def _infer_split(record_id: str) -> str:
    lowered = record_id.lower()
    if lowered.startswith("train"):
        return "train"
    if lowered.startswith("val"):
        return "validation"
    if lowered.startswith("test"):
        return "independent_test"
    return "unknown"


def _assistant_content(record: dict[str, Any]) -> str:
    for turn in record.get("conversations", []):
        if turn.get("role") == "assistant":
            return str(turn.get("content", ""))
    return ""


def _user_content(record: dict[str, Any]) -> str:
    for turn in record.get("conversations", []):
        if turn.get("role") == "user":
            return str(turn.get("content", ""))
    return ""


def normalize_record(record: dict[str, Any]) -> dict[str, Any]:
    if "modalities" in record and "target" in record:
        return record

    if "conversations" in record:
        record_id = str(record.get("id", "legacy_sample"))
        image_list = record.get("image") or [""]
        return {
            "id": record_id,
            "split": _infer_split(record_id),
            "patient_id": str(record.get("patient_id", record_id)),
            "modalities": {
                "panoramic_radiograph": image_list[0],
                "structured_ehr": {},
            },
            "question": _user_content(record),
            "target": {
                "thinking": "",
                "answer": extract_answer(_assistant_content(record)),
            },
        }

    raise ValueError("Unsupported record format")


def load_records(path_like: str | Path) -> list[dict[str, Any]]:
    path = resolve_path(path_like)
    with path.open("r", encoding="utf-8-sig") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError(f"Expected list of records in {path}")
    return [normalize_record(item) for item in data]


def save_records(path_like: str | Path, records: list[dict[str, Any]]) -> Path:
    path = ensure_parent(path_like)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(records, handle, ensure_ascii=False, indent=2)
    return path


def _format_ehr(ehr: dict[str, Any]) -> str:
    lines: list[str] = []
    for key, value in ehr.items():
        if isinstance(value, dict):
            pretty = json.dumps(value, ensure_ascii=False, sort_keys=True)
            lines.append(f"- {key}: {pretty}")
        else:
            lines.append(f"- {key}: {value}")
    return "\n".join(lines)


def build_problem_text(record: dict[str, Any]) -> str:
    modalities = record.get("modalities", {})
    ehr = modalities.get("structured_ehr", {})
    sections = [
        f"Panoramic radiograph: {modalities.get('panoramic_radiograph', 'REDACTED')}",
    ]
    if ehr:
        sections.append("Structured EHR:")
        sections.append(_format_ehr(ehr))
    sections.append(f"Question: {record.get('question', '')}")
    return "\n".join(sections)


def to_sft_record(record: dict[str, Any], system_prompt: str | None = None) -> dict[str, Any]:
    answer = record.get("target", {}).get("answer", "").strip()
    thinking = record.get("target", {}).get("thinking", "").strip()
    sft_record: dict[str, Any] = {
        "problem": build_problem_text(record),
        "thinking": f"<think>{thinking}</think>" if thinking else "<think></think>",
        "solution": f"<answer>{answer}</answer>",
        "image": record.get("modalities", {}).get("panoramic_radiograph", ""),
    }
    if system_prompt:
        sft_record["system"] = system_prompt
    return sft_record
