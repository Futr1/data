from __future__ import annotations

from pathlib import Path

from src.utils.config import repo_root


def legacy_ms_swift_root() -> Path:
    return repo_root() / "multimodal" / "framework" / "ms-swift"


def legacy_r1_v_root() -> Path:
    return repo_root() / "multimodal" / "model" / "R1-V"


def require_dependency(path: Path, label: str) -> Path:
    if not path.exists():
        raise FileNotFoundError(f"{label} not found: {path}")
    return path
