from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import QTimer
from PySide6.QtGui import QStandardItem, QStandardItemModel

from wlb.services.settings_service import SettingsService
from wlb.ui.step2.models.selection_store import SelectionOrderStore
from wlb.ui.step3.views.boxes import build_footer_row, build_tabs_panel
from wlb.ui.widgets import PageScaffold


class OrderPage(PageScaffold):
    def __init__(
        self,
        store: SelectionOrderStore,
        settings: SettingsService,
        on_back: Callable[[], None] | None = None,
        on_next: Callable[[], None] | None = None,
    ) -> None:
        super().__init__(
            title="Step 3: Reorder Components",
            subtitle="Arrange components into a valid install order.",
        )
        self._store = store
        self._settings = settings
        self._is_reordering = False
        self._on_back = on_back
        self._on_next = on_next

        self._bgee_model = QStandardItemModel()
        self._bg2ee_model = QStandardItemModel()
        self._tabs, self._bgee_view, self._bg2ee_view = build_tabs_panel(
            self._bgee_model,
            self._bg2ee_model,
            lambda: self._sync_from_model("BGEE"),
            lambda: self._sync_from_model("BG2EE"),
        )
        self.body_layout.addWidget(self._tabs)
        self._apply_game_tabs()

        button_row, back_button, next_button = build_footer_row()
        back_button.clicked.connect(self._handle_back)
        next_button.clicked.connect(self._handle_next)
        self.footer_layout.addWidget(button_row)

        self._store.subscribe(self._refresh)
        self._refresh()

    def _refresh(self) -> None:
        if self._is_reordering:
            return
        self._set_items(self._bgee_model, self._store.get_order("BGEE"))
        self._set_items(self._bg2ee_model, self._store.get_order("BG2EE"))

    def _set_items(self, model: QStandardItemModel, items: list[str]) -> None:
        model.clear()
        for text in items:
            item = QStandardItem(text)
            item.setEditable(False)
            model.appendRow(item)

    def _sync_from_model(self, game: str) -> None:
        model = self._bgee_model if game == "BGEE" else self._bg2ee_model
        items = [model.item(row).text() for row in range(model.rowCount()) if model.item(row)]
        self._is_reordering = True
        self._store.set_order(game, items)
        QTimer.singleShot(0, self._end_reorder)

    def _end_reorder(self) -> None:
        self._is_reordering = False

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
        bar = self._tabs.tabBar()
        bar.setTabVisible(0, show_bgee)
        bar.setTabVisible(1, show_bg2ee)
        bar.updateGeometry()
        bar.adjustSize()
        self._tabs.updateGeometry()
        if show_bgee:
            self._tabs.setCurrentIndex(0)
        elif show_bg2ee:
            self._tabs.setCurrentIndex(1)
