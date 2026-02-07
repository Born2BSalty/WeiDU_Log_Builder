from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel

from wlb.ui.step2.models.item_roles import ORDER_ROLE, RAW_ROLE


def ordered_items(model: QStandardItemModel) -> list[str]:
    items: list[tuple[int, str]] = []
    for row in range(model.rowCount()):
        parent = model.item(row)
        if parent is None:
            continue
        for child_row in range(parent.rowCount()):
            child = parent.child(child_row)
            if child is None:
                continue
            if child.checkState() != Qt.CheckState.Checked:
                continue
            order = child.data(ORDER_ROLE)
            raw = child.data(RAW_ROLE) or child.text()
            if isinstance(order, int):
                items.append((order, raw))
    return [raw for _, raw in sorted(items, key=lambda x: x[0])]
