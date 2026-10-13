"""Maps logical model names to local weight paths + backend hints."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ModelSpec:
    name: str
    backend: str
    weights_dir: Path
    default_steps: int


class ModelRegistry:
    def __init__(self, root: Path = Path("models/weights")) -> None:
        self.root = root
        self._specs: dict[str, ModelSpec] = {
            "sdxl-turbo": ModelSpec("sdxl-turbo", "diffusers", root / "sdxl-turbo", 6),
            "sd15-turbo": ModelSpec("sd15-turbo", "diffusers", root / "sd15-turbo", 4),
        }

    def get(self, name: str) -> ModelSpec:
        if name not in self._specs:
            raise KeyError(f"model {name!r} not registered")
        return self._specs[name]

    def available(self) -> list[str]:
        return [n for n, s in self._specs.items() if s.weights_dir.exists()]