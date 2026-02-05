from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ModInfo:
    name: str
    tp2_path: Path
    components: list[str]
    author: str | None
    readme_path: Path | None
    version: str | None
