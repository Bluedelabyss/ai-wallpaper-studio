"""End-to-end pipeline test with a fake diffusion processor (no GPU)."""
from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest
from PIL import Image

from processors.base import Processor
from studio.pipeline import Pipeline
from utils.job import Job
from utils.queue import JobQueue


class FakeDiffusion(Processor):
    name = "diffusion"

    async def run(self, job: Job) -> Job:
        job.image = Image.new("RGB", (64, 64), (20, 40, 80))
        return job


class FakeDriver:
    def __init__(self, cfg) -> None:
        self.saved: list[Job] = []

    async def deliver(self, image, job: Job) -> None:
        self.saved.append(job)


def _cfg() -> SimpleNamespace:
    return SimpleNamespace(
        studio=SimpleNamespace(workers=2, version="test"),
        processors=SimpleNamespace(chain=["diffusion"], steps=1, guidance=1.0, upscale_factor=1),
        output=SimpleNamespace(driver="file", target_dir="out/", format="png"),
    )


@pytest.mark.asyncio
async def test_pipeline_renders_all_jobs(monkeypatch):
    cfg = _cfg()
    q = JobQueue(maxsize=4)
    await q.put_from_prompt("a neon city at dusk")
    await q.put_from_prompt("a mountain lake at dawn")

    pipe = Pipeline.__new__(Pipeline)
    pipe.cfg = cfg
    pipe.queue = q
    pipe.chain = [FakeDiffusion(cfg)]
    pipe.driver = FakeDriver(cfg.output)
    from studio.pipeline import PipelineStats
    pipe.stats = PipelineStats()

    await pipe.drain()
    assert pipe.stats.rendered == 2
    assert pipe.stats.failed == 0
    assert len(pipe.driver.saved) == 2