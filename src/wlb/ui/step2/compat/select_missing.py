from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem

from wlb.services.settings_service import SettingsService
from wlb.ui.step2.compat.select_compat_files import find_missing_files
from wlb.ui.step2.compat.select_compat_types import StatusBundle
from wlb.ui.step2.compat.select_missing_format import format_missing
from wlb.ui.step2.compat.select_missing_status import status_for_item


class MissingFilesReporter:
    def __init__(self, settings: SettingsService) -> None:
        self._settings = settings
        self._cache: dict[str, list[str]] = {}
        self._status_maps: dict[str, dict[Path, StatusBundle]] = {}

    def reset(self) -> None:
        self._cache.clear()
        self._status_maps = {}

    def set_status_maps(self, status_maps: dict[str, dict[Path, StatusBundle]]) -> None:
        self._status_maps = status_maps

    def for_item(self, item: QStandardItem) -> list[str]:
        mods_folder = self._settings.mods_folder()
        tp2_path = item.data(Qt.ItemDataRole.UserRole + 4)
        if not mods_folder or not tp2_path:
            return []
        key = str(tp2_path)
        if key in self._cache:
            status = status_for_item(item, self._status_maps)
            return format_missing(self._cache[key], status)
        mods_dir = Path(mods_folder)
        mod_root = Path(tp2_path).parent
        tp2_paths = list(mod_root.rglob("*.tp2")) if mod_root.exists() else [Path(tp2_path)]
        missing = find_missing_files(tp2_paths, mods_dir, mod_root)
        self._cache[key] = missing
        status = status_for_item(item, self._status_maps)
        return format_missing(missing, status)
