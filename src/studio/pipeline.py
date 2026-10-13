"""Async pipeline: pulls jobs from queue, runs the processor chain, hands off to driver."""
from __future__ import annotations

import asyncio
from dataclasses import dataclass, field

from drivers.base import OutputDriver
from drivers.registry import build_driver
from processors import build_chain
from utils.config import StudioConfig
from utils.logging import get_logger
from utils.queue import JobQueue

log = get_logger("studio.pipeline")


@dataclass
class PipelineStats:
    pulled: int = 0
    rendered: int = 0
    failed: int = 0
    errors: list[str] = field(default_factory=list)


class Pipeline:
    def __init__(self, cfg: StudioConfig, queue: JobQueue) -> None:
        self.cfg = cfg
        self.queue = queue
        self.chain = build_chain(cfg.processors.chain, cfg)
        self.driver: OutputDriver = build_driver(cfg.output.driver, cfg.output)
        self.stats = PipelineStats()

    async def _worker(self, wid: int) -> None:
        while True:
            job = await self.queue.get()
            if job is None:
                self.queue.task_done()
                return
            try:
                for proc in self.chain:
                    job = await proc.run(job)
                await self.driver.deliver(job.image, job)
                self.stats.rendered += 1
            except Exception as exc:  # keep worker alive; log and continue
                self.stats.failed += 1
                self.stats.errors.append(f"worker={wid} job={job.id}: {exc!r}")
                log.exception("job %s failed", job.id)
            finally:
                self.queue.task_done()

    async def drain(self) -> None:
        workers = [asyncio.create_task(self._worker(i)) for i in range(self.cfg.studio.workers)]
        await self.queue.join()
        for _ in workers:
            await self.queue.put(None)
        await asyncio.gather(*workers)