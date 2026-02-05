from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from PySide6.QtCore import QThread

from wlb.services.scan_service import ScanService
from wlb.ui.step2.select_layout import SelectionUi
from wlb.ui.step2.select_scan_worker import ScanWorker


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
        self._thread: QThread | None = None
        self._worker: ScanWorker | None = None

    def start(self, mods_dir: Path, weidu_path: Path, game_dir: Path) -> None:
        if self._thread is not None:
            return
        if self._scan_service is None:
            self._on_failed("Scan service not available.")
            return
        self._ui.scan_button.setEnabled(False)
        self._ui.cancel_scan_button.setEnabled(True)
        self._ui.progress_label.setText("Scanning...")

        self._thread = QThread()
        self._worker = ScanWorker(self._scan_service, mods_dir, weidu_path, game_dir)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.progress.connect(self._on_progress)
        self._worker.finished.connect(self._on_finished)
        self._worker.failed.connect(self._on_failed)
        self._worker.finished.connect(self._thread.quit)
        self._worker.failed.connect(self._thread.quit)
        self._thread.finished.connect(self._cleanup)
        self._thread.start()

    def cancel(self) -> None:
        if self._worker is not None:
            self._worker.cancel()

    def _cleanup(self) -> None:
        self._ui.scan_button.setEnabled(True)
        self._ui.cancel_scan_button.setEnabled(False)
        self._thread = None
        self._worker = None
        self._on_cleanup()
