from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem

from wlb.services.settings_service import SettingsService
from wlb.ui.step2.select_compat_files import find_missing_files
from wlb.ui.step2.select_compat_types import ModStatus, StatusBundle


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
            game = ""
            model = item.model()
            if model is not None:
                game = model.property("_game") or ""
            status_map = self._status_maps.get(str(game), {})
            bundle = status_map.get(Path(tp2_path)) if tp2_path else None
            status = None
            if bundle is not None:
                index = item.data(Qt.ItemDataRole.UserRole + 9)
                if isinstance(index, int) and 0 <= index < len(bundle.components):
                    status = bundle.components[index]
                else:
                    status = bundle.header
            return self._format_missing(self._cache[key], status)
        mods_dir = Path(mods_folder)
        mod_root = Path(tp2_path).parent
        tp2_paths = list(mod_root.rglob("*.tp2")) if mod_root.exists() else [Path(tp2_path)]
        missing = find_missing_files(tp2_paths, mods_dir, mod_root)
        self._cache[key] = missing
        game = ""
        model = item.model()
        if model is not None:
            game = model.property("_game") or ""
        status_map = self._status_maps.get(str(game), {})
        bundle = status_map.get(Path(tp2_path)) if tp2_path else None
        status = None
        if bundle is not None:
            index = item.data(Qt.ItemDataRole.UserRole + 9)
            if isinstance(index, int) and 0 <= index < len(bundle.components):
                status = bundle.components[index]
            else:
                status = bundle.header
        return self._format_missing(missing, status)

    @staticmethod
    def _format_missing(missing: list[str], status: ModStatus | None) -> list[str]:
        lines: list[str] = []
        ok = "✔"
        warn = "⚠"
        fail = "✖"
        if not missing:
            lines.append(f"{ok} Files: OK")
        else:
            lines.append(f"{fail} Files: Missing ({len(missing)})")
            lines.extend([f"  - {item}" for item in missing])
        if status is None:
            lines.extend(
                [
                    f"{warn} Dependencies: Unknown",
                    f"{warn} Conflicts: Unknown",
                    f"{warn} Requires: Unknown",
                ]
            )
            return lines
        if status.reason:
            lines.append(f"{fail} Compatibility: {status.reason}")
        if status.deps_present:
            lines.append(f"{ok} Dependencies: {', '.join(status.deps_present)}")
        elif status.deps_missing:
            lines.append(f"{fail} Dependencies Missing: {', '.join(status.deps_missing)}")
        else:
            lines.append(f"{ok} Dependencies: None")
        required = sorted({*status.deps_present, *status.deps_missing})
        if required:
            lines.append(f"{ok} Requires: {', '.join(required)}")
        else:
            lines.append(f"{ok} Requires: None")
        if status.conflicts:
            lines.append(f"{fail} Conflicts: {', '.join(status.conflicts)}")
        else:
            lines.append(f"{ok} Conflicts: None")
        return lines
