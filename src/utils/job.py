"""Job is the unit of work flowing through the pipeline."""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Job:
    prompt: str
    seed: int = -1
    image: Any = None
    meta: dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])