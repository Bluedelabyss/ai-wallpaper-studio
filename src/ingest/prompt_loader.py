"""Read newline-separated prompts, one per job. Blank lines and '#' comments skipped."""
from __future__ import annotations

from pathlib import Path


def load_prompts_from_file(path: str | Path) -> list[str]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"prompt file not found: {p}")
    out: list[str] = []
    for raw in p.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        out.append(line)
    return out