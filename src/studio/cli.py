"""Entry point. Wires config -> job queue -> pipeline -> output driver."""
from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

from studio.pipeline import Pipeline
from utils.config import load_config
from utils.logging import get_logger
from utils.queue import JobQueue

log = get_logger("studio.cli")


def _parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="ai-wallpaper-studio")
    p.add_argument("--config", type=Path, default=Path("config/default.toml"))
    p.add_argument("--profile", default=None, help="config/profile name, e.g. lite")
    p.add_argument("--prompt", default=None, help="single-shot prompt override")
    p.add_argument("--workers", type=int, default=None)
    return p.parse_args(argv)


async def _run(args: argparse.Namespace) -> int:
    cfg = load_config(args.config, profile=args.profile)
    if args.workers:
        cfg.studio.workers = args.workers

    queue = JobQueue(maxsize=cfg.studio.workers * 4)
    pipeline = Pipeline(cfg, queue)

    if args.prompt:
        await queue.put_from_prompt(args.prompt)
    else:
        await queue.put_from_file(cfg.ingest.prompt_file)

    await pipeline.drain()
    log.info("pipeline drained, %d jobs rendered", pipeline.stats.rendered)
    return 0


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv if argv is not None else sys.argv[1:])
    try:
        return asyncio.run(_run(args))
    except KeyboardInterrupt:
        log.warning("interrupted by user")
        return 130