from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from PySide6.QtCore import Qt, QThread
from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QWidget

from wlb.services.scan_service import ScanService
from wlb.ui.step2.controllers.readme_worker_runner import start_readme_worker
from wlb.ui.step2.views.view_utils import source_index
from wlb.ui.step2.workers.readme_scan_worker import ReadmeScanWorker


class ReadmeLookup:
    def __init__(
        self,
        scan_service: ScanService | None,
        apply_readme: Callable[[Path, str], None],
        on_error: Callable[[str], None],
    ) -> None:
        self._scan_service = scan_service
        self._apply_readme = apply_readme
        self._on_error = on_error
        self._thread: QThread | None = None
        self._worker: ReadmeScanWorker | None = None
        self._game_dir: Path | None = None
        self._cache: dict[str, str] = {}
        self._inflight: set[str] = set()
        self._pending: tuple[Path, str, Path] | None = None

    def reset(self, game_dir: Path | None) -> None:
        self._cache.clear()
        self._inflight.clear()
        self._game_dir = game_dir

    def attach(self, view: QWidget) -> None:
        selection = view.selectionModel()
        if selection is None:
            return
        selection.currentChanged.connect(lambda current, _prev: self._maybe_scan_readme(current))

    def _maybe_scan_readme(self, index) -> None:
        index = source_index(index)
        if not index.isValid():
            return
        model = index.model()
        if not isinstance(model, QStandardItemModel):
            return
        item = model.itemFromIndex(index)
        if item is None:
            return
        tp2_path = item.data(Qt.ItemDataRole.UserRole + 4)
        mod_name = item.data(Qt.ItemDataRole.UserRole) or item.text()
        if not tp2_path:
            return
        key = str(tp2_path)
        if key in self._cache:
            return
        existing = item.data(Qt.ItemDataRole.UserRole + 6)
        if existing and existing != "-":
            self._cache[key] = str(existing)
            return
        if key in self._inflight:
            return
        if self._scan_service is None or self._game_dir is None:
            return
        self._start(Path(tp2_path), str(mod_name), self._game_dir)

    def _start(self, tp2_path: Path, mod_name: str, game_dir: Path) -> None:
        if self._thread is not None:
            self._pending = (tp2_path, mod_name, game_dir)
            return
        self._inflight.add(str(tp2_path))
        if self._scan_service is None:
            return
        self._thread, self._worker = start_readme_worker(
            self._scan_service,
            tp2_path,
            mod_name,
            game_dir,
            self._on_found,
            self._on_error,
            self._cleanup,
        )

    def _on_found(self, tp2_path: object, readme: object) -> None:
        key = str(tp2_path)
        readme_value = str(readme) if readme else "-"
        self._cache[key] = readme_value
        self._inflight.discard(key)
        self._apply_readme(Path(key), readme_value)

    def _cleanup(self) -> None:
        self._thread = None
        self._worker = None
        if self._pending is not None:
            tp2_path, mod_name, game_dir = self._pending
            self._pending = None
            self._start(tp2_path, mod_name, game_dir)
