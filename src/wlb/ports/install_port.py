from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Protocol


class InstallPort(Protocol):
    def start(
        self,
        argv: list[str],
        cwd: Path | None,
        env: dict[str, str] | None,
        on_output: Callable[[str], None],
        on_exit: Callable[[int], None],
    ) -> None: ...

    def send_input(self, text: str) -> None: ...

    def cancel(self) -> None: ...
