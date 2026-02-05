from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class ProcessResult:
    stdout: str
    stderr: str
    returncode: int


class ProcessPort(Protocol):
    def run(self, args: list[str], cwd: Path | None = None) -> ProcessResult: ...