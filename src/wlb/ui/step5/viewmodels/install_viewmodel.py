from __future__ import annotations

from collections.abc import Callable

from wlb.services.install_service import InstallRequest, InstallService


class InstallViewModel:
    def __init__(self, service: InstallService) -> None:
        self._service = service

    def start(
        self,
        request: InstallRequest,
        on_output: Callable[[str], None],
        on_exit: Callable[[int], None],
    ) -> None:
        self._service.start(request, on_output, on_exit)

    def send_input(self, text: str) -> None:
        self._service.send_input(text)

    def cancel(self) -> None:
        self._service.cancel()
