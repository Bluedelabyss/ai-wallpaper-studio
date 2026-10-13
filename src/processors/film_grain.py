"""Overlays procedural film grain. Deterministic per-job via seed."""
from __future__ import annotations

import asyncio
import random

from processors.base import Processor
from utils.job import Job


class FilmGrainProcessor(Processor):
    name = "film_grain"

    def _grain_sync(self, image):
        from PIL import Image, ImageDraw

        rng = random.Random(self.cfg.studio.version)
        w, h = image.size
        overlay = Image.new("L", (w, h), 0)
        draw = ImageDraw.Draw(overlay)
        density = (w * h) // 800
        for _ in range(density):
            x, y = rng.randrange(w), rng.randrange(h)
            draw.point((x, y), fill=rng.randrange(0, 40))
        return Image.composite(image, Image.new("RGB", (w, h), (0, 0, 0)), overlay.point(lambda v: v))

    async def run(self, job: Job) -> Job:
        job.image = await asyncio.to_thread(self._grain_sync, job.image)
        return job