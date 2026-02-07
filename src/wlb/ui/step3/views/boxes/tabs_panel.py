from __future__ import annotations

from collections.abc import Callable

from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QListView, QTabWidget

from wlb.ui.step3.views.reorder_list import build_reorder_list


def build_tabs_panel(
    bgee_model: QStandardItemModel,
    bg2ee_model: QStandardItemModel,
    on_bgee_change: Callable[[], None],
    on_bg2ee_change: Callable[[], None],
) -> tuple[QTabWidget, QListView, QListView]:
    tabs = QTabWidget()
    bgee_view = build_reorder_list(bgee_model, on_bgee_change)
    bg2ee_view = build_reorder_list(bg2ee_model, on_bg2ee_change)
    tabs.addTab(bgee_view, "BGEE")
    tabs.addTab(bg2ee_view, "BG2EE")
    return tabs, bgee_view, bg2ee_view
