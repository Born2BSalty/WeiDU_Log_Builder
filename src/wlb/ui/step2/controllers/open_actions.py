from __future__ import annotations

from PySide6.QtCore import QModelIndex, Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QTreeView

from wlb.ui.step2.views.selection_ui import SelectionUi
from wlb.ui.step2.views.view_utils import source_index


def open_tp2(ui: SelectionUi, view: QTreeView) -> None:
    index = source_index(view.currentIndex())
    if not index.isValid():
        ui.details_desc.setPlainText("Select a mod or component first.")
        return
    open_path(ui, index, Qt.ItemDataRole.UserRole + 4, "No TP2 path available.")


def open_readme(ui: SelectionUi, view: QTreeView) -> None:
    index = source_index(view.currentIndex())
    if not index.isValid():
        ui.details_desc.setPlainText("Select a mod or component first.")
        return
    open_path(ui, index, Qt.ItemDataRole.UserRole + 6, "No Readme path available.")


def open_path(
    ui: SelectionUi, index: QModelIndex, role: Qt.ItemDataRole, empty_message: str
) -> None:
    model = index.model()
    if model is None:
        ui.details_desc.setPlainText(empty_message)
        return
    path_value = model.data(index, role)
    if not path_value or path_value == "-":
        ui.details_desc.setPlainText(empty_message)
        return
    QDesktopServices.openUrl(QUrl.fromLocalFile(str(path_value)))
