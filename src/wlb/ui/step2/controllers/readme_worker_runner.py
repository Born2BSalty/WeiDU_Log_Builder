from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from PySide6.QtCore import QThread

from wlb.services.scan_service import ScanService
from wlb.ui.step2.workers.readme_scan_worker import ReadmeScanWorker


def start_readme_worker(
    scan_service: ScanService,
    tp2_path: Path,
    mod_name: str,
    game_dir: Path,
    on_found: Callable[[object, object], None],
    on_error: Callable[[str], None],
    on_cleanup: Callable[[], None],
) -> tuple[QThread, ReadmeScanWorker]:
    thread = QThread()
    worker = ReadmeScanWorker(scan_service, tp2_path, mod_name, game_dir)
    worker.moveToThread(thread)
    thread.started.connect(worker.run)
    worker.finished.connect(on_found)
    worker.failed.connect(on_error)
    worker.finished.connect(thread.quit)
    worker.failed.connect(thread.quit)
    thread.finished.connect(on_cleanup)
    thread.start()
    return thread, worker
