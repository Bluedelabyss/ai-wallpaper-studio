"""Writes PNG/JPEG to output.target_dir. Uses safe_join to prevent traversal."""
from __future__ import annotations

import asyncio
from pathlib import Path

from drivers.base import OutputDriver
from utils.job import Job
from utils.logging import get_logger
from utils.paths import safe_join

log = get_logger("drivers.file")


class FileDriver(OutputDriver):
    name = "file"

    def _write_sync(self, image, job: Job) -> Path:
        target_dir = Path(self.cfg.target_dir)
        target_dir.mkdir(parents=True, exist_ok=True)
        fmt = self.cfg.format.lower()
        out = safe_join(target_dir, f"{job.id}.{fmt}")
        image.save(out, format=fmt.upper())
        return out

    async def deliver(self, image, job: Job) -> None:
        path = await asyncio.to_thread(self._write_sync, image, job)
        log.info("wrote %s (%s)", path, job.prompt[:48])