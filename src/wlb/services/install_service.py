from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from wlb.ports.install_port import InstallPort


@dataclass(frozen=True)
class InstallRequest:
    argv: list[str]
    cwd: Path | None
    env: dict[str, str] | None


class InstallService:
    def __init__(self, installer: InstallPort) -> None:
        self._installer = installer

    def start(
        self,
        request: InstallRequest,
        on_output: Callable[[str], None],
        on_exit: Callable[[int], None],
    ) -> None:
        self._installer.start(request.argv, request.cwd, request.env, on_output, on_exit)

    def send_input(self, text: str) -> None:
        self._installer.send_input(text)

    def cancel(self) -> None:
        self._installer.cancel()