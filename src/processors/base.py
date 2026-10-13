"""Processor ABC. Every stage mutates and returns the Job."""
from __future__ import annotations

from abc import ABC, abstractmethod

from utils.job import Job


class Processor(ABC):
    name: str = "base"

    def __init__(self, cfg) -> None:
        self.cfg = cfg

    def requires(self) -> set[str]:
        """Capability tags this processor needs, e.g. {'gpu', 'torch'}."""
        return set()

    @abstractmethod
    async def run(self, job: Job) -> Job: ...