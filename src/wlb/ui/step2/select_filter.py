from __future__ import annotations

from PySide6.QtCore import QRegularExpression, QSortFilterProxyModel


class ModFilterProxy(QSortFilterProxyModel):
    def filterAcceptsRow(self, source_row: int, source_parent) -> bool:  # type: ignore[override]
        regex = self.filterRegularExpression()
        if not regex.pattern():
            return True
        model = self.sourceModel()
        if model is None:
            return False
        index = model.index(source_row, 0, source_parent)
        if not index.isValid():
            return False
        text = model.data(index, self.filterRole())
        if _matches(regex, text):
            return True
        if not source_parent.isValid():
            for row in range(model.rowCount(index)):
                child = model.index(row, 0, index)
                child_text = model.data(child, self.filterRole())
                if _matches(regex, child_text):
                    return True
            return False
        parent_text = model.data(source_parent, self.filterRole())
        return _matches(regex, parent_text)


def _matches(regex: QRegularExpression, text: object) -> bool:
    if not text:
        return False
    return regex.match(str(text)).hasMatch()
