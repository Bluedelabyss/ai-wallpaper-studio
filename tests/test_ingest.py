"""Ingest + safe_join tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from ingest.prompt_loader import load_prompts_from_file
from utils.paths import safe_join


def test_prompt_loader_skips_blanks_and_comments(tmp_path: Path):
    f = tmp_path / "p.txt"
    f.write_text("# header\n\nneon city\n  \n# comment\nmountain lake\n", encoding="utf-8")
    assert load_prompts_from_file(f) == ["neon city", "mountain lake"]


def test_safe_join_blocks_traversal(tmp_path: Path):
    with pytest.raises(ValueError):
        safe_join(tmp_path, "..", "etc", "passwd")


def test_safe_join_allows_nested(tmp_path: Path):
    out = safe_join(tmp_path, "sub", "file.png")
    assert out.name == "file.png"
    assert tmp_path.resolve() in out.parents