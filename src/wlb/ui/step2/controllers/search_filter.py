from __future__ import annotations

from PySide6.QtCore import QRegularExpression, QSortFilterProxyModel
from PySide6.QtWidgets import QTreeView


def apply_search_filter(text: str, views: list[QTreeView]) -> None:
    regex = QRegularExpression(QRegularExpression.escape(text))
    regex.setPatternOptions(QRegularExpression.PatternOption.CaseInsensitiveOption)
    for view in views:
        model = view.model()
        if not isinstance(model, QSortFilterProxyModel):
            continue
        model.setFilterRegularExpression(regex if text else QRegularExpression())
        if not text:
            view.collapseAll()
