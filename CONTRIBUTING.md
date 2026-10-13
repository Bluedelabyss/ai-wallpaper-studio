# Contributing to ai-wallpaper-studio

Thanks for wanting to push pixels. This repo is a pipeline: **ingest → process → render → output**. Every contribution should slot into one of those four stages.

## Layout

```
src/
  studio/        # entry + orchestration
  ingest/        # prompt / reference / seed loaders
  processors/    # diffusion + upscale + style passes
  drivers/       # output sinks (file, wallpaper-set, slideshow)
  models/        # model registry + weight loaders
  utils/         # job queue, logging, config
config/
tests/
```

## Adding a processor

1. Subclass `processors.base.Processor`.
2. Implement `name`, `requires()`, `run(job) -> Job`.
3. Register in `processors/__init__.py::REGISTRY`.
4. Add a test under `tests/` using a 64x64 dummy tensor — do not hit the GPU in CI.

## Adding an output driver

Subclass `drivers.base.OutputDriver`, implement `deliver(image, job)`. Drivers must be idempotent — the pipeline retries on transient IO errors.

## Style

- `ruff` + `black`, line length 100.
- No blocking calls in `processors/` — everything async-friendly or wrapped in `asyncio.to_thread`.
- Type hints required on public functions.

## PR checklist

- [ ] Tests pass locally (`pytest -q`)
- [ ] No new model weights committed
- [ ] Config keys documented in `config/default.toml`
- [ ] Changelog entry under `## Unreleased`

## Reporting bugs

Include: OS build, GPU + driver, Python version, the exact `job.json` that failed, and the tail of `logs/studio.log`.