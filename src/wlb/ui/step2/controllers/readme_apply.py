from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QSortFilterProxyModel, Qt
from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QTreeView


def apply_readme_to_views(views: tuple[QTreeView, ...], tp2_path: Path, readme: str) -> None:
    for view in views:
        proxy = view.model()
        source = proxy.sourceModel() if isinstance(proxy, QSortFilterProxyModel) else proxy
        if not isinstance(source, QStandardItemModel):
            continue
        _apply_readme_to_model(source, tp2_path, readme)


def _apply_readme_to_model(model: QStandardItemModel, tp2_path: Path, readme: str) -> None:
    for row in range(model.rowCount()):
        parent = model.item(row)
        if parent is None:
            continue
        parent_tp2 = parent.data(Qt.ItemDataRole.UserRole + 4)
        if not parent_tp2 or str(parent_tp2) != str(tp2_path):
            continue
        parent.setData(readme, Qt.ItemDataRole.UserRole + 6)
        for child_row in range(parent.rowCount()):
            child = parent.child(child_row)
            if child is None:
                continue
            child.setData(readme, Qt.ItemDataRole.UserRole + 6)
