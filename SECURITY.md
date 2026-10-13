# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.6.x   | yes       |
| 0.5.x   | security fixes only |
| < 0.5   | no        |

## Reporting a vulnerability

Do **not** open a public issue. Email `security@ai-wallpaper-studio.dev` with a description, repro, and impact. We aim to acknowledge within 72h.

## Threat model notes

`ai-wallpaper-studio` loads model weights from disk and from user-supplied paths. It does **not** sandbox arbitrary Python from config files — treat any `*.toml`/`*.yaml` in `config/` as trusted input. Prompt strings are passed to the local diffusion backend only; no prompt data leaves the machine unless you enable `telemetry.enabled = true`.

## Known non-issues

- Output PNGs are written with user-controlled paths — path traversal in `drivers/file_driver.py` is mitigated by `utils/paths.safe_join`.
- CUDA OOM on 4GB cards with SDXL — expected, not a vuln. Use `--profile=lite`.