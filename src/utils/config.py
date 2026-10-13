"""Loads TOML config, merges optional profile overlay, returns a typed namespace."""
from __future__ import annotations

import tomllib
from pathlib import Path
from types import SimpleNamespace


def _to_ns(d: dict) -> SimpleNamespace:
    return SimpleNamespace(**{k: _to_ns(v) if isinstance(v, dict) else v for k, v in d.items()})


def _merge(base: dict, overlay: dict) -> dict:
    out = dict(base)
    for k, v in overlay.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _merge(out[k], v)
        else:
            out[k] = v
    return out


def load_config(path: str | Path, profile: str | None = None) -> SimpleNamespace:
    p = Path(path)
    data = tomllib.loads(p.read_text(encoding="utf-8"))
    if profile:
        prof = p.parent / "profiles" / f"{profile}.toml"
        if not prof.exists():
            raise FileNotFoundError(f"profile not found: {prof}")
        data = _merge(data, tomllib.loads(prof.read_text(encoding="utf-8")))
    return _to_ns(data)