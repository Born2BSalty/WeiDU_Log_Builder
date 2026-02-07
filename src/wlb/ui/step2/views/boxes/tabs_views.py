from __future__ import annotations

from PySide6.QtWidgets import QTreeView


def build_tab_views() -> tuple[QTreeView, QTreeView]:
    bgee_view = QTreeView()
    bg2ee_view = QTreeView()
    bgee_view.setHeaderHidden(False)
    bg2ee_view.setHeaderHidden(False)
    return bgee_view, bg2ee_view
