from __future__ import annotations

from PySide6.QtWidgets import QVBoxLayout, QWidget


def apply_list_layout(
    layout: QVBoxLayout, search_row: QWidget, scan_row: QWidget, list_title: QWidget, tabs: QWidget
) -> None:
    layout.addWidget(search_row)
    layout.addWidget(scan_row)
    layout.addWidget(list_title)
    layout.addWidget(tabs)
