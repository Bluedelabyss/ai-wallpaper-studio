"""Diffusion stage. Backend is pluggable; default is a diffusers SDXL-turbo pipeline.

Gotcha: diffusers >= 0.27 changed `num_inference_steps` semantics for turbo
schedulers — 1-4 steps is the sweet spot, more steps degrades output.
"""
from __future__ import annotations

import asyncio
from typing import Any

from processors.base import Processor
from utils.job import Job
from utils.logging import get_logger

log = get_logger("processors.diffusion")


class DiffusionProcessor(Processor):
    name = "diffusion"

    def __init__(self, cfg) -> None:
        super().__init__(cfg)
        self._pipe: Any = None

    def requires(self) -> set[str]:
        return {"gpu", "torch", "diffusers"}

    def _load(self) -> Any:
        if self._pipe is not None:
            return self._pipe
        from diffusers import AutoPipelineForText2Image  # type: ignore

        model_id = self.cfg.processors.diffusion_model
        log.info("loading diffusion model %s", model_id)
        self._pipe = AutoPipelineForText2Image.from_pretrained(
            model_id, torch_dtype="auto", variant="fp16"
        )
        self._pipe.to("cuda")
        return self._pipe

    def _render_sync(self, prompt: str, seed: int) -> Any:
        pipe = self._load()
        import torch  # type: ignore

        gen = torch.Generator(device="cuda").manual_seed(seed)
        return pipe(
            prompt=prompt,
            num_inference_steps=self.cfg.processors.steps,
            guidance_scale=self.cfg.processors.guidance,
            generator=gen,
        ).images[0]

    async def run(self, job: Job) -> Job:
        seed = job.seed if job.seed >= 0 else 0
        job.image = await asyncio.to_thread(self._render_sync, job.prompt, seed)
        return job