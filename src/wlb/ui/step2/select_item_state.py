from __future__ import annotations

from PySide6.QtGui import QColor, QStandardItem


def apply_component_state(item: QStandardItem, *, disabled: bool) -> None:
    if disabled:
        item.setCheckable(False)
        item.setForeground(QColor("#808080"))
        return
    item.setCheckable(True)


def apply_header_state(item: QStandardItem, *, disabled: bool) -> None:
    if disabled:
        item.setCheckable(False)
        item.setForeground(QColor("#808080"))
        return
    item.setCheckable(True)
