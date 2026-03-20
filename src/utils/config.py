from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]


def repo_root() -> Path:
    return REPO_ROOT


def resolve_path(path_like: str | Path, base: str | Path | None = None) -> Path:
    candidate = Path(path_like)
    if candidate.is_absolute():
        return candidate
    anchor = Path(base) if base is not None else REPO_ROOT
    return (anchor / candidate).resolve()


def load_yaml(path_like: str | Path) -> dict[str, Any]:
    path = resolve_path(path_like)
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML config must be a mapping: {path}")
    return data


def ensure_parent(path_like: str | Path) -> Path:
    path = resolve_path(path_like)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path
