from __future__ import annotations

from pathlib import Path

from wlb.services.export_service import ExportRequest, ExportService, ExportTarget
from wlb.services.settings_service import SettingsService
from wlb.ui.step2.models.selection_store import SelectionOrderStore


class ReviewViewModel:
    def __init__(
        self,
        settings: SettingsService,
        store: SelectionOrderStore,
        export_service: ExportService,
    ) -> None:
        self._settings = settings
        self._store = store
        self._export_service = export_service

    def game(self) -> str:
        return self._settings.game()

    def order_bgee(self) -> list[str]:
        return self._store.get_order("BGEE")

    def order_bg2ee(self) -> list[str]:
        return self._store.get_order("BG2EE")

    def save_weidu_log(self) -> None:
        game = self._settings.game()
        targets: list[ExportTarget] = []
        if game == "EET":
            bgee_folder = self._settings.eet_bgee_log_folder()
            bg2_folder = self._settings.eet_bg2ee_log_folder()
            if bgee_folder:
                targets.append(
                    ExportTarget(
                        folder=Path(bgee_folder),
                        lines=self._store.get_order("BGEE"),
                    )
                )
            if bg2_folder:
                targets.append(
                    ExportTarget(
                        folder=Path(bg2_folder),
                        lines=self._store.get_order("BG2EE"),
                    )
                )
        elif game == "BG2EE":
            bg2_folder = self._settings.bg2ee_log_folder()
            if bg2_folder:
                targets.append(
                    ExportTarget(
                        folder=Path(bg2_folder),
                        lines=self._store.get_order("BG2EE"),
                    )
                )
        else:
            bgee_folder = self._settings.bgee_log_folder()
            if bgee_folder:
                targets.append(
                    ExportTarget(
                        folder=Path(bgee_folder),
                        lines=self._store.get_order("BGEE"),
                    )
                )
        self._export_service.export(ExportRequest(targets=targets))
