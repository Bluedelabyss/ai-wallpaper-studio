"""Processor registry. Chain order comes from config.processors.chain."""
from __future__ import annotations

from processors.base import Processor
from processors.color_grade import ColorGradeProcessor
from processors.diffusion import DiffusionProcessor
from processors.film_grain import FilmGrainProcessor
from processors.prompt_expand import PromptExpandProcessor
from processors.upscale import UpscaleProcessor

REGISTRY: dict[str, type[Processor]] = {
    "prompt_expand": PromptExpandProcessor,
    "diffusion": DiffusionProcessor,
    "upscale": UpscaleProcessor,
    "color_grade": ColorGradeProcessor,
    "film_grain": FilmGrainProcessor,
}


def build_chain(names: list[str], cfg) -> list[Processor]:
    chain: list[Processor] = []
    for name in names:
        if name not in REGISTRY:
            raise KeyError(f"unknown processor: {name!r} (have: {sorted(REGISTRY)})")
        chain.append(REGISTRY[name](cfg))
    return chain