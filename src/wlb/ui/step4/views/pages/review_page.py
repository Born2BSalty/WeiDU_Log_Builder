from __future__ import annotations

from collections.abc import Callable

from PySide6.QtWidgets import QVBoxLayout, QWidget

from wlb.ui.step4.viewmodels.review_viewmodel import ReviewViewModel
from wlb.ui.step4.views.boxes import build_footer_row, build_tabs_panel, build_top_row
from wlb.ui.widgets import PageScaffold


class ReviewPage(PageScaffold):
    def __init__(
        self,
        view_model: ReviewViewModel,
        on_back: Callable[[], None] | None = None,
        on_next: Callable[[], None] | None = None,
    ) -> None:
        super().__init__(
            title="Step 4: Preview & Export",
            subtitle="Review selections before installing.",
        )
        self._view_model = view_model
        self._on_back = on_back
        self._on_next = on_next

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(12)

        top_row, save_button = build_top_row()
        save_button.clicked.connect(self._view_model.save_weidu_log)

        self._tabs, self._bgee_list, self._bg2ee_list = build_tabs_panel()
        self._apply_game_tabs()

        content_layout.addWidget(top_row)
        content_layout.addWidget(self._tabs, 1)
        self.body_layout.addWidget(content)

        button_row, back_button, next_button = build_footer_row()
        back_button.clicked.connect(self._handle_back)
        next_button.clicked.connect(self._handle_next)
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
        self._refresh_lists()

    def _apply_game_tabs(self) -> None:
        game = self._view_model.game()
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

    def _refresh_lists(self) -> None:
        self._bgee_list.clear()
        self._bg2ee_list.clear()
        self._bgee_list.addItems(self._view_model.order_bgee())
        self._bg2ee_list.addItems(self._view_model.order_bg2ee())
