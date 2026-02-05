from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QObject, Signal

from wlb.services.scan_service import ScanService


class ScanWorker(QObject):
    progress = Signal(int, int, str)
    finished = Signal(list)
    failed = Signal(str)

    def __init__(
        self, service: ScanService, mods_dir: Path, weidu_path: Path, game_dir: Path
    ) -> None:
        super().__init__()
        self._service = service
        self._mods_dir = mods_dir
        self._weidu_path = weidu_path
        self._game_dir = game_dir
        self._cancelled = False

    def cancel(self) -> None:
        self._cancelled = True

    def run(self) -> None:
        try:
            mods = self._service.scan_mods(
                self._mods_dir,
                self._weidu_path,
                self._game_dir,
                on_progress=self._on_progress,
                should_cancel=self._should_cancel,
            )
        except Exception as exc:  # pragma: no cover - UI safety net
            self.failed.emit(str(exc))
            return
        self.finished.emit(mods)

    def _on_progress(self, current: int, total: int, name: str) -> None:
        self.progress.emit(current, total, name)

    def _should_cancel(self) -> bool:
        return self._cancelled
