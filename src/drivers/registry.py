from __future__ import annotations

from drivers.base import OutputDriver
from drivers.file_driver import FileDriver

_DRIVERS: dict[str, type[OutputDriver]] = {
    "file": FileDriver,
}


def build_driver(name: str, cfg) -> OutputDriver:
    if name not in _DRIVERS:
        raise KeyError(f"unknown output driver: {name!r}")
    return _DRIVERS[name](cfg)