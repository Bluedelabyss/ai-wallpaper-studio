"""Load style reference images. Returns raw bytes; decoding happens in the processor."""
from __future__ import annotations

from pathlib import Path

SUPPORTED = {".png", ".jpg", ".jpeg", ".webp"}


def load_references(directory: str | Path) -> dict[str, bytes]:
    d = Path(directory)
    if not d.exists():
        return {}
    refs: dict[str, bytes] = {}
    for f in sorted(d.iterdir()):
        if f.suffix.lower() in SUPPORTED and f.is_file():
            refs[f.stem] = f.read_bytes()
    return refs