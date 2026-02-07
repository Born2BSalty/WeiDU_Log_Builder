from __future__ import annotations

from PySide6.QtWidgets import QTreeView


def all_views(bgee_view: QTreeView, bg2ee_view: QTreeView) -> tuple[QTreeView, QTreeView]:
    return bgee_view, bg2ee_view
