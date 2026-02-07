from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from PySide6.QtCore import QThread

from wlb.services.scan_service import ScanService
from wlb.ui.step2.workers.select_scan_worker import ScanWorker


def start_scan_worker(
    scan_service: ScanService,
    mods_dir: Path,
    weidu_path: Path,
    game_dir: Path,
    on_progress: Callable[[int, int, str], None],
    on_finished: Callable[[list], None],
    on_failed: Callable[[str], None],
    on_thread_done: Callable[[], None],
) -> tuple[QThread, ScanWorker]:
    thread = QThread()
    worker = ScanWorker(scan_service, mods_dir, weidu_path, game_dir)
    worker.moveToThread(thread)
    thread.started.connect(worker.run)
    worker.progress.connect(on_progress)
    worker.finished.connect(on_finished)
    worker.failed.connect(on_failed)
    worker.finished.connect(thread.quit)
    worker.failed.connect(thread.quit)
    thread.finished.connect(on_thread_done)
    thread.start()
    return thread, worker
