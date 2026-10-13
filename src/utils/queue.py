"""Async job queue with helpers to seed from prompt strings or files."""
from __future__ import annotations

import asyncio

from ingest.prompt_loader import load_prompts_from_file
from utils.job import Job


class JobQueue:
    def __init__(self, maxsize: int = 8) -> None:
        self._q: asyncio.Queue[Job | None] = asyncio.Queue(maxsize=maxsize)

    async def put_from_prompt(self, prompt: str, seed: int = -1) -> None:
        await self._q.put(Job(prompt=prompt, seed=seed))

    async def put_from_file(self, path: str) -> int:
        prompts = load_prompts_from_file(path)
        for p in prompts:
            await self._q.put(Job(prompt=p))
        return len(prompts)

    async def get(self) -> Job | None:
        return await self._q.get()

    async def put(self, item: Job | None) -> None:
        await self._q.put(item)

    def task_done(self) -> None:
        self._q.task_done()

    async def join(self) -> None:
        await self._q.join()