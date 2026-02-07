from __future__ import annotations

from PySide6.QtCore import QSortFilterProxyModel
from PySide6.QtWidgets import QTreeView


def active_view(bgee_view: QTreeView, bg2ee_view: QTreeView, tab_index: int) -> QTreeView:
    return bgee_view if tab_index == 0 else bg2ee_view


def source_index(index):
    model = index.model()
    if isinstance(model, QSortFilterProxyModel):
        return model.mapToSource(index)
    return index
