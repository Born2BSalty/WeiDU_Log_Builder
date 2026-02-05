from __future__ import annotations

from PySide6.QtCore import QRegularExpression, QSortFilterProxyModel, QTimer
from PySide6.QtWidgets import QLineEdit, QTreeView


class SearchController:
    def __init__(self, input_field: QLineEdit, views: list[QTreeView]) -> None:
        self._input = input_field
        self._views = views
        self._pending = ""
        self._timer = QTimer(input_field)
        self._timer.setSingleShot(True)
        self._timer.setInterval(200)
        self._timer.timeout.connect(self._apply)
        self._input.textChanged.connect(self._schedule)

    def _schedule(self, text: str) -> None:
        self._pending = text
        self._timer.start()

    def _apply(self) -> None:
        text = self._pending.strip()
        regex = QRegularExpression(QRegularExpression.escape(text))
        regex.setPatternOptions(QRegularExpression.PatternOption.CaseInsensitiveOption)
        for view in self._views:
            model = view.model()
            if not isinstance(model, QSortFilterProxyModel):
                continue
            model.setFilterRegularExpression(regex if text else QRegularExpression())
            if not text:
                view.collapseAll()
