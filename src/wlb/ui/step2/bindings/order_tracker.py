from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem

from wlb.ui.step2.bindings.order_list import ordered_items
from wlb.ui.step2.models.item_roles import ORDER_ROLE
from wlb.ui.step2.models.selection_store import SelectionOrderStore


class OrderTracker:
    def __init__(self, store: SelectionOrderStore, game: str) -> None:
        self._store = store
        self._game = game
        self._next = 1
        self._handling = False

    def on_item_changed(self, item: QStandardItem) -> None:
        if self._handling:
            return
        model = item.model()
        if model is None:
            return
        if item.hasChildren():
            self._handling = True
            self._apply_parent_toggle(item)
            self._handling = False
            self._store.set_order(self._game, ordered_items(model))
            return
        if item.checkState() == Qt.CheckState.Checked:
            if item.data(ORDER_ROLE) is None:
                item.setData(self._next, ORDER_ROLE)
                self._next += 1
        else:
            if item.data(ORDER_ROLE) is not None:
                item.setData(None, ORDER_ROLE)
        self._store.set_order(self._game, ordered_items(model))

    def _apply_parent_toggle(self, parent: QStandardItem) -> None:
        state = parent.checkState()
        for row in range(parent.rowCount()):
            child = parent.child(row)
            if child is None:
                continue
            if not child.isCheckable():
                continue
            if child.checkState() != state:
                child.setCheckState(state)
            if state == Qt.CheckState.Checked:
                if child.data(ORDER_ROLE) is None:
                    child.setData(self._next, ORDER_ROLE)
                    self._next += 1
            else:
                if child.data(ORDER_ROLE) is not None:
                    child.setData(None, ORDER_ROLE)
