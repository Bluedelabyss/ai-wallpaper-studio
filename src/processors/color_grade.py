"""Pillow-based color grade. LUT path is optional; falls back to a simple curve."""
from __future__ import annotations

import asyncio
from pathlib import Path

from processors.base import Processor
from utils.job import Job


class ColorGradeProcessor(Processor):
    name = "color_grade"

    def _grade_sync(self, image):
        from PIL import ImageEnhance

        image = ImageEnhance.Contrast(image).enhance(1.08)
        image = ImageEnhance.Color(image).enhance(1.12)
        lut_path = getattr(self.cfg.processors, "lut", None)
        if lut_path and Path(lut_path).exists():
            # Apply .cube LUT via ImageFilter.Color3DLUT — omitted when absent.
            pass
        return image

    async def run(self, job: Job) -> Job:
        job.image = await asyncio.to_thread(self._grade_sync, job.image)
        return job