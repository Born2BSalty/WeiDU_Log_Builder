from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from PySide6.QtWidgets import QWidget

from wlb.services.scan_service import ScanService
from wlb.services.settings_service import SettingsService
from wlb.ui.step2.compat.select_missing import MissingFilesReporter
from wlb.ui.step2.controllers.open_actions import open_readme, open_tp2
from wlb.ui.step2.controllers.page_nav import go_back, go_next
from wlb.ui.step2.controllers.scan_gate import validate_scan_inputs
from wlb.ui.step2.controllers.scan_wiring import build_scan_flow
from wlb.ui.step2.controllers.select_scan import ScanController
from wlb.ui.step2.controllers.select_search import SearchController
from wlb.ui.step2.models.selection_store import SelectionOrderStore
from wlb.ui.step2.views.boxes import build_footer_row
from wlb.ui.step2.views.select_widgets import SelectionUi, build_selection_ui
from wlb.ui.step2.views.tab_visibility import apply_game_tabs
from wlb.ui.step2.views.view_utils import active_view
from wlb.ui.widgets import PageScaffold


class SelectPage(PageScaffold):
    def __init__(
        self,
        store: SelectionOrderStore,
        settings: SettingsService,
        on_back: Callable[[], None] | None = None,
        on_next: Callable[[], None] | None = None,
        scan_service: ScanService | None = None,
    ) -> None:
        super().__init__(
            title="Step 2: Scan & Select Components",
            subtitle="Choose components to install.",
        )
        self._on_back = on_back
        self._on_next = on_next
        self._scan_service = scan_service
        self._store = store
        self._settings = settings
        self._missing_reporter = MissingFilesReporter(settings)
        self.ui: SelectionUi = build_selection_ui(store)
        self._scan_controller = ScanController(
            self.ui,
            scan_service,
            self._on_scan_progress,
            self._on_scan_finished,
            self._on_scan_failed,
            self._cleanup_scan,
        )
        self._search: SearchController | None = None
        self.body_layout.addWidget(self.ui.root)
        self.ui.scan_button.clicked.connect(self._on_scan_clicked)
        self.ui.cancel_scan_button.clicked.connect(self._on_cancel_scan)
        self.ui.tp2_button.clicked.connect(self._on_open_tp2)
        self.ui.readme_button.clicked.connect(self._on_open_readme)
        self._apply_game_tabs()
        self._search = SearchController(
            self.ui.search_input, [self.ui.bgee_view, self.ui.bg2ee_view]
        )

        button_row, self._scan_status, back_button, next_button = build_footer_row()
        back_button.clicked.connect(self._handle_back)
        next_button.clicked.connect(self._handle_next)
        self.footer_layout.addWidget(button_row)

        self._scan_flow, self._readme_lookup = build_scan_flow(
            self.ui,
            self._settings,
            self._store,
            self._missing_reporter,
            scan_service,
            self._scan_status,
        )

    def _handle_back(self) -> None:
        go_back(self._on_back)

    def _handle_next(self) -> None:
        go_next(self._on_next)

    def showEvent(self, event) -> None:  # type: ignore[override]
        super().showEvent(event)
        self._apply_game_tabs()

    def _apply_game_tabs(self) -> None:
        apply_game_tabs(self.ui.tabs, self._settings.game())

    def _on_scan_clicked(self) -> None:
        if self._scan_service is None:
            self.ui.details_desc.setPlainText("Scan service not available.")
            return
        paths = validate_scan_inputs(self._settings, self.ui)
        if paths is None:
            return
        self._start_scan(*paths)

    def _on_cancel_scan(self) -> None:
        self._scan_controller.cancel()
        self.ui.progress_label.setText("Canceling...")

    def _start_scan(self, mods_dir: Path, weidu_path: Path, game_dir: Path) -> None:
        self._scan_flow.start_scan(game_dir)
        self._scan_controller.start(mods_dir, weidu_path, game_dir)

    def _on_scan_progress(self, current: int, total: int, name: str) -> None:
        self._scan_flow.on_progress(current, total, name)

    def _on_scan_finished(self, mods: list) -> None:
        self._scan_flow.on_finished(mods)

    def _on_scan_failed(self, message: str) -> None:
        self._scan_flow.on_failed(message)

    def _cleanup_scan(self) -> None:
        return

    def _on_open_tp2(self) -> None:
        view = self._active_view()
        open_tp2(self.ui, view)

    def _on_open_readme(self) -> None:
        view = self._active_view()
        open_readme(self.ui, view)

    def _active_view(self) -> QWidget:
        return active_view(self.ui.bgee_view, self.ui.bg2ee_view, self.ui.tabs.currentIndex())
