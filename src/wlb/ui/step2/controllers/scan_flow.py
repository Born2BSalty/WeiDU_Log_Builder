from __future__ import annotations

from pathlib import Path
from typing import Any

from wlb.services.settings_service import SettingsService
from wlb.ui.step2.compat.select_missing import MissingFilesReporter
from wlb.ui.step2.controllers.readme_apply import apply_readme_to_views
from wlb.ui.step2.controllers.readme_lookup import ReadmeLookup
from wlb.ui.step2.controllers.scan_labels import (
    set_readme_failed,
    set_scan_failed,
    set_scan_finished,
    set_scan_progress,
    set_scan_started,
)
from wlb.ui.step2.controllers.scan_status import build_status_maps
from wlb.ui.step2.controllers.tab_views import all_views
from wlb.ui.step2.models.selection_store import SelectionOrderStore
from wlb.ui.step2.views.select_widgets import SelectionUi, apply_mods


class ScanFlow:
    def __init__(
        self,
        ui: SelectionUi,
        settings: SettingsService,
        store: SelectionOrderStore,
        reporter: MissingFilesReporter,
        readme_lookup: ReadmeLookup,
        scan_status_label: Any,
    ) -> None:
        self._ui = ui
        self._settings = settings
        self._store = store
        self._reporter = reporter
        self._readme_lookup = readme_lookup
        self._scan_status_label = scan_status_label
        self._scan_game_dir: Path | None = None

    def set_readme_lookup(self, readme_lookup: ReadmeLookup) -> None:
        self._readme_lookup = readme_lookup

    def start_scan(self, game_dir: Path) -> None:
        self._scan_game_dir = game_dir
        set_scan_started(self._ui, self._scan_status_label)

    def on_progress(self, current: int, total: int, name: str) -> None:
        set_scan_progress(self._ui, self._scan_status_label, current, total, name)

    def on_finished(self, mods: list[Any]) -> None:
        set_scan_finished(self._ui, self._scan_status_label)
        self._readme_lookup.reset(self._scan_game_dir)
        self._reporter.reset()
        mods_dir = Path(self._settings.mods_folder()) if self._settings.mods_folder() else None
        if mods_dir is not None:
            self._reporter.set_status_maps(build_status_maps(mods, mods_dir))
        apply_mods(self._ui, mods, self._store, self._settings, self._reporter)
        for view in all_views(self._ui.bgee_view, self._ui.bg2ee_view):
            self._readme_lookup.attach(view)

    def on_failed(self, message: str) -> None:
        set_scan_failed(self._ui, self._scan_status_label, message)

    def on_readme_failed(self, message: str) -> None:
        set_readme_failed(self._ui, self._scan_status_label, message)

    def apply_readme(self, tp2_path: Path, readme_value: str) -> None:
        apply_readme_to_views(
            all_views(self._ui.bgee_view, self._ui.bg2ee_view),
            tp2_path,
            readme_value,
        )
