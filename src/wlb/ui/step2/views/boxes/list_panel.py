from __future__ import annotations

from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QPushButton,
    QTabWidget,
    QTreeView,
    QVBoxLayout,
    QWidget,
)

from wlb.ui.step2.views.boxes.list_header import build_list_header
from wlb.ui.step2.views.boxes.list_panel_layout import apply_list_layout
from wlb.ui.step2.views.boxes.scan_row import build_scan_row
from wlb.ui.step2.views.boxes.search_row import build_search_row
from wlb.ui.step2.views.boxes.tabs_panel import build_tabs_panel


def build_list_panel() -> tuple[
    QWidget,
    QLineEdit,
    QPushButton,
    QPushButton,
    QLabel,
    QTabWidget,
    QTreeView,
    QTreeView,
]:
    list_panel = QWidget()
    list_layout = QVBoxLayout(list_panel)
    list_layout.setContentsMargins(0, 0, 0, 0)
    list_title = build_list_header()

    search_row, search_input = build_search_row()
    scan_row, scan_button, cancel_scan_button, progress_label = build_scan_row()
    tabs, bgee_view, bg2ee_view = build_tabs_panel()

    apply_list_layout(list_layout, search_row, scan_row, list_title, tabs)

    return (
        list_panel,
        search_input,
        scan_button,
        cancel_scan_button,
        progress_label,
        tabs,
        bgee_view,
        bg2ee_view,
    )
