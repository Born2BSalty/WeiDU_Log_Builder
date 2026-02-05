from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from PySide6.QtCore import QSortFilterProxyModel, Qt, QUrl
from PySide6.QtGui import QDesktopServices, QStandardItemModel
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget

from wlb.services.scan_service import ScanService
from wlb.services.settings_service import SettingsService
from wlb.ui.step2.readme_lookup import ReadmeLookup
from wlb.ui.step2.select_compat import build_status_map
from wlb.ui.step2.select_missing import MissingFilesReporter
from wlb.ui.step2.select_scan import ScanController
from wlb.ui.step2.select_search import SearchController
from wlb.ui.step2.select_widgets import SelectionUi, apply_mods, build_selection_ui
from wlb.ui.step2.selection_store import SelectionOrderStore
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
        self._scan_game_dir: Path | None = None
        self._readme_lookup = ReadmeLookup(
            scan_service,
            self._apply_readme,
            self._on_readme_failed,
        )
        self._pending_readme: tuple[Path, str, Path] | None = None
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

        button_row = QWidget()
        row_layout = QHBoxLayout(button_row)
        row_layout.setContentsMargins(0, 0, 0, 0)

        self._scan_status = QLabel("Idle")

        back_button = QPushButton("Back")
        back_button.clicked.connect(self._handle_back)
        next_button = QPushButton("Next")
        next_button.clicked.connect(self._handle_next)

        row_layout.addWidget(self._scan_status)
        row_layout.addStretch(1)
        row_layout.addWidget(back_button)
        row_layout.addWidget(next_button)
        self.footer_layout.addWidget(button_row)

    def _handle_back(self) -> None:
        if self._on_back is not None:
            self._on_back()

    def _handle_next(self) -> None:
        if self._on_next is not None:
            self._on_next()

    def showEvent(self, event) -> None:  # type: ignore[override]
        super().showEvent(event)
        self._apply_game_tabs()

    def _apply_game_tabs(self) -> None:
        game = self._settings.game()
        show_bgee = game in ("BGEE", "EET")
        show_bg2ee = game in ("BG2EE", "EET")
        bar = self.ui.tabs.tabBar()
        bar.setTabVisible(0, show_bgee)
        bar.setTabVisible(1, show_bg2ee)
        bar.updateGeometry()
        bar.adjustSize()
        self.ui.tabs.updateGeometry()
        if show_bgee:
            self.ui.tabs.setCurrentIndex(0)
        elif show_bg2ee:
            self.ui.tabs.setCurrentIndex(1)

    def _on_scan_clicked(self) -> None:
        mods_dir = self._settings.mods_folder()
        weidu_path = self._settings.weidu_path()
        game_dir = self._settings.bgee_game()
        if not mods_dir:
            self.ui.details_desc.setPlainText("Set a Mods Folder on Step 1 before scanning.")
            return
        if not weidu_path:
            self.ui.details_desc.setPlainText("Set WeiDU.exe path on Step 1 before scanning.")
            return
        if not game_dir:
            self.ui.details_desc.setPlainText("Set a game folder on Step 1 before scanning.")
            return
        if self._scan_service is None:
            self.ui.details_desc.setPlainText("Scan service not available.")
            return
        self._start_scan(Path(mods_dir), Path(weidu_path), Path(game_dir))

    def _on_cancel_scan(self) -> None:
        self._scan_controller.cancel()
        self.ui.progress_label.setText("Canceling...")

    def _start_scan(self, mods_dir: Path, weidu_path: Path, game_dir: Path) -> None:
        self._scan_game_dir = game_dir
        self._scan_status.setText("0/0")
        self._scan_controller.start(mods_dir, weidu_path, game_dir)

    def _on_scan_progress(self, current: int, total: int, name: str) -> None:
        if total > 0:
            self._scan_status.setText(f"{current}/{total}: {name}")
            self.ui.progress_label.setText("Scanning...")
        else:
            self.ui.progress_label.setText("Scanning...")

    def _on_scan_finished(self, mods: list) -> None:
        self.ui.progress_label.setText("Scan complete.")
        self._scan_status.setText("Done")
        self._readme_lookup.reset(self._scan_game_dir)
        self._missing_reporter.reset()
        mods_dir = Path(self._settings.mods_folder()) if self._settings.mods_folder() else None
        if mods_dir is not None:
            bgee_status = build_status_map(mods, mods_dir, "BGEE")
            bg2ee_status = build_status_map(mods, mods_dir, "BG2EE")
            self._missing_reporter.set_status_maps({"BGEE": bgee_status, "BG2EE": bg2ee_status})
        apply_mods(self.ui, mods, self._store, self._settings, self._missing_reporter)
        self._readme_lookup.attach(self.ui.bgee_view)
        self._readme_lookup.attach(self.ui.bg2ee_view)

    def _on_scan_failed(self, message: str) -> None:
        self.ui.progress_label.setText("Scan failed.")
        self._scan_status.setText("Failed")
        self.ui.details_desc.setPlainText(message)

    def _cleanup_scan(self) -> None:
        return

    def _on_open_tp2(self) -> None:
        view = self._active_view()
        index = self._source_index(view.currentIndex())
        if not index.isValid():
            self.ui.details_desc.setPlainText("Select a mod or component first.")
            return
        model = index.model()
        if model is None:
            self.ui.details_desc.setPlainText("No TP2 path available.")
            return
        tp2_path = model.data(index, Qt.ItemDataRole.UserRole + 4)
        if not tp2_path:
            self.ui.details_desc.setPlainText("No TP2 path available.")
            return
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(tp2_path)))

    def _active_view(self) -> QWidget:
        return self.ui.bgee_view if self.ui.tabs.currentIndex() == 0 else self.ui.bg2ee_view

    def _on_open_readme(self) -> None:
        view = self._active_view()
        index = self._source_index(view.currentIndex())
        if not index.isValid():
            self.ui.details_desc.setPlainText("Select a mod or component first.")
            return
        model = index.model()
        if model is None:
            self.ui.details_desc.setPlainText("No Readme path available.")
            return
        readme_path = model.data(index, Qt.ItemDataRole.UserRole + 6)
        if not readme_path or readme_path == "-":
            self.ui.details_desc.setPlainText("No Readme path available.")
            return
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(readme_path)))

    def _on_readme_failed(self, message: str) -> None:
        self._scan_status.setText("Readme scan failed")
        self.ui.details_desc.setPlainText(message)

    def _apply_readme(self, tp2_path: Path, readme_value: str) -> None:
        for view in (self.ui.bgee_view, self.ui.bg2ee_view):
            proxy = view.model()
            source = proxy.sourceModel() if isinstance(proxy, QSortFilterProxyModel) else proxy
            if not isinstance(source, QStandardItemModel):
                continue
            for row in range(source.rowCount()):
                parent = source.item(row)
                if parent is None:
                    continue
                parent_tp2 = parent.data(Qt.ItemDataRole.UserRole + 4)
                if not parent_tp2 or str(parent_tp2) != str(tp2_path):
                    continue
                parent.setData(readme_value, Qt.ItemDataRole.UserRole + 6)
                for child_row in range(parent.rowCount()):
                    child = parent.child(child_row)
                    if child is None:
                        continue
                    child.setData(readme_value, Qt.ItemDataRole.UserRole + 6)
        self._scan_status.setText("Ready")

    @staticmethod
    def _source_index(index):  # type: ignore[no-untyped-def]
        model = index.model()
        if isinstance(model, QSortFilterProxyModel):
            return model.mapToSource(index)
        return index
