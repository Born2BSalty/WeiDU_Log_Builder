from __future__ import annotations

from PySide6.QtWidgets import QTabWidget, QTreeView

from wlb.ui.step2.views.boxes.tabs_views import build_tab_views


def build_tabs_panel() -> tuple[QTabWidget, QTreeView, QTreeView]:
    tabs = QTabWidget()
    bgee_view, bg2ee_view = build_tab_views()
    _apply_tabs(tabs, bgee_view, bg2ee_view)
    return tabs, bgee_view, bg2ee_view


def _apply_tabs(tabs: QTabWidget, bgee_view: QTreeView, bg2ee_view: QTreeView) -> None:
    tabs.addTab(bgee_view, "BGEE")
    tabs.addTab(bg2ee_view, "BG2EE")
