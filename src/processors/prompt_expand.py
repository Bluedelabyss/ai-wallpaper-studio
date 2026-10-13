"""Expands terse prompts into richer ones via a small local template bank.
No network calls — keeps the studio offline-friendly."""
from __future__ import annotations

import random

from processors.base import Processor
from utils.job import Job

STYLE_TAGS = [
    "cinematic lighting", "volumetric fog", "35mm film grain",
    "ultra detailed", "octane render", "soft rim light",
    "moody atmosphere", "hyperreal textures",
]
QUALITY_TAGS = ["8k", "sharp focus", "professional color grading"]


class PromptExpandProcessor(Processor):
    name = "prompt_expand"

    async def run(self, job: Job) -> Job:
        rng = random.Random(job.seed if job.seed >= 0 else None)
        picks = rng.sample(STYLE_TAGS, k=3) + rng.sample(QUALITY_TAGS, k=2)
        job.prompt = f"{job.prompt}, {', '.join(picks)}"
        return job