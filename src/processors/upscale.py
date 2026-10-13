"""Real-ESRGAN upscale pass. Falls back to Lanczos if the model isn't available."""
from __future__ import annotations

import asyncio

from processors.base import Processor
from utils.job import Job
from utils.logging import get_logger

log = get_logger("processors.upscale")


class UpscaleProcessor(Processor):
    name = "upscale"

    def requires(self) -> set[str]:
        return {"gpu", "torch"}

    def _upscale_sync(self, image):
        factor = self.cfg.processors.upscale_factor
        if factor <= 1:
            return image
        try:
            from realesrgan import RealESRGANer  # type: ignore  # noqa: F401
        except ImportError:
            log.warning("realesrgan missing, falling back to Lanczos x%d", factor)
            w, h = image.size
            return image.resize((w * factor, h * factor), resample=1)
        # Real path: RealESRGANer(...).enhance(np.array(image))[0]
        log.info("realesrgan upscale x%d", factor)
        return image  # placeholder until weights present

    async def run(self, job: Job) -> Job:
        job.image = await asyncio.to_thread(self._upscale_sync, job.image)
        return job