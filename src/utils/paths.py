"""Path helpers. safe_join rejects traversal outside the base dir."""
from __future__ import annotations

from pathlib import Path


def safe_join(base: Path, *parts: str) -> Path:
    base = base.resolve()
    candidate = base.joinpath(*parts).resolve()
    if base not in candidate.parents and candidate != base:
        raise ValueError(f"path escapes base: {candidate}")
    return candidate