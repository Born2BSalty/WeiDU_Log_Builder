from __future__ import annotations

from PySide6.QtCore import QEvent, QObject
from PySide6.QtWidgets import QGroupBox, QTabWidget, QTreeView

from wlb.ui.step2.views.view_utils import active_view


class HeightSyncViews(QObject):
    def __init__(
        self,
        tabs: QTabWidget,
        bgee_view: QTreeView,
        bg2ee_view: QTreeView,
        details_box: QGroupBox,
    ) -> None:
        super().__init__(tabs)
        self._tabs = tabs
        self._bgee_view = bgee_view
        self._bg2ee_view = bg2ee_view
        self._details_box = details_box
        self._bgee_view.viewport().installEventFilter(self)
        self._bg2ee_view.viewport().installEventFilter(self)
        self._tabs.currentChanged.connect(self._apply)
        self._apply()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Type.Resize:
            self._apply()
        return False

    def _active_view(self) -> QTreeView:
        return active_view(self._bgee_view, self._bg2ee_view, self._tabs.currentIndex())

    def _apply(self) -> None:
        view = self._active_view()
        height = view.viewport().height()
        self._details_box.setFixedHeight(max(100, height))
