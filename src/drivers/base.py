"""Output driver ABC. Drivers are idempotent — pipeline may retry on IO error."""
from __future__ import annotations

from abc import ABC, abstractmethod

from utils.job import Job


class OutputDriver(ABC):
    name: str = "base"

    def __init__(self, cfg) -> None:
        self.cfg = cfg

    @abstractmethod
    async def deliver(self, image, job: Job) -> None: ...