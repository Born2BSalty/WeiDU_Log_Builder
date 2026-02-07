from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from wlb.services.scan_service import ScanService
from wlb.ui.step2.controllers.scan_ui_state import set_idle, set_scanning
from wlb.ui.step2.controllers.scan_worker_runner import start_scan_worker
from wlb.ui.step2.views.select_layout import SelectionUi


class ScanController:
    def __init__(
        self,
        ui: SelectionUi,
        scan_service: ScanService | None,
        on_progress: Callable[[int, int, str], None],
        on_finished: Callable[[list], None],
        on_failed: Callable[[str], None],
        on_cleanup: Callable[[], None],
    ) -> None:
        self._ui = ui
        self._scan_service = scan_service
        self._on_progress = on_progress
        self._on_finished = on_finished
        self._on_failed = on_failed
        self._on_cleanup = on_cleanup
        self._thread = None
        self._worker = None

    def start(self, mods_dir: Path, weidu_path: Path, game_dir: Path) -> None:
        if self._thread is not None:
            return
        if self._scan_service is None:
            self._on_failed("Scan service not available.")
            return
        set_scanning(self._ui)

        self._thread, self._worker = start_scan_worker(
            self._scan_service,
            mods_dir,
            weidu_path,
            game_dir,
            self._on_progress,
            self._on_finished,
            self._on_failed,
            self._cleanup,
        )

    def cancel(self) -> None:
        if self._worker is not None:
            self._worker.cancel()

    def _cleanup(self) -> None:
        set_idle(self._ui)
        self._thread = None
        self._worker = None
        self._on_cleanup()
