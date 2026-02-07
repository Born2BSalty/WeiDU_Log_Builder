from __future__ import annotations

from PySide6.QtWidgets import QSplitter, QWidget


def build_main_splitter(list_panel: QWidget, details_panel: QWidget) -> QSplitter:
    splitter = QSplitter()
    splitter.setChildrenCollapsible(False)
    splitter.addWidget(list_panel)
    splitter.addWidget(details_panel)
    splitter.setStretchFactor(0, 4)
    splitter.setStretchFactor(1, 2)
    return splitter
