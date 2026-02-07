from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QAbstractItemView, QListView


class LiveReorderListView(QListView):
    def __init__(self, on_reorder: Callable[[], None]) -> None:
        super().__init__()
        self._on_reorder = on_reorder
        self._drag_row: int | None = None
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setDragDropMode(QAbstractItemView.DragDropMode.DragOnly)
        self.setDefaultDropAction(Qt.DropAction.IgnoreAction)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)

    def dragEnterEvent(self, event) -> None:  # type: ignore[override]
        event.setDropAction(Qt.DropAction.MoveAction)
        event.accept()

    def startDrag(self, supported_actions: Qt.DropActions) -> None:
        index = self.currentIndex()
        self._drag_row = index.row() if index.isValid() else None
        super().startDrag(supported_actions)

    def dragMoveEvent(self, event) -> None:  # type: ignore[override]
        if self._drag_row is None:
            event.setDropAction(Qt.DropAction.MoveAction)
            event.accept()
            return
        pos = event.position().toPoint()
        target = self.indexAt(pos)
        if not target.isValid():
            event.accept()
            return
        target_row = target.row()
        if target_row == self._drag_row:
            event.accept()
            return
        model = self.model()
        if not isinstance(model, QStandardItemModel):
            event.setDropAction(Qt.DropAction.MoveAction)
            event.accept()
            return
        moved = model.takeRow(self._drag_row)
        if not moved:
            event.setDropAction(Qt.DropAction.MoveAction)
            event.accept()
            return
        insert_row = target_row
        if target_row > self._drag_row:
            insert_row -= 1
        model.insertRow(insert_row, moved)
        self._drag_row = insert_row
        self.setCurrentIndex(model.index(insert_row, 0))
        self._on_reorder()
        event.setDropAction(Qt.DropAction.MoveAction)
        event.accept()

    def dropEvent(self, event) -> None:  # type: ignore[override]
        self._drag_row = None
        event.setDropAction(Qt.DropAction.IgnoreAction)
        event.ignore()

    def dragLeaveEvent(self, event) -> None:  # type: ignore[override]
        self._drag_row = None
        super().dragLeaveEvent(event)


def build_reorder_list(model: QStandardItemModel, on_reorder: Callable[[], None]) -> QListView:
    view = LiveReorderListView(on_reorder)
    view.setModel(model)
    return view
