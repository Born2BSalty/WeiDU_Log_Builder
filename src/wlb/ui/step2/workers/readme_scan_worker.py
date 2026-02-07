from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QObject, Signal

from wlb.services.scan_service import ScanService


class ReadmeScanWorker(QObject):
    finished = Signal(object, object)
    failed = Signal(str)

    def __init__(self, service: ScanService, tp2_path: Path, mod_name: str, game_dir: Path) -> None:
        super().__init__()
        self._service = service
        self._tp2_path = tp2_path
        self._mod_name = mod_name
        self._game_dir = game_dir

    def run(self) -> None:
        try:
            results = self._service.scan_readme(self._tp2_path, self._mod_name, self._game_dir)
        except Exception as exc:  # pragma: no cover - UI safety net
            self.failed.emit(str(exc))
            return
        self.finished.emit(self._tp2_path, results)
