from __future__ import annotations

import re
from collections.abc import Callable

from PySide6.QtCore import QModelIndex, QSortFilterProxyModel, Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QLabel, QTextEdit, QTreeView

from wlb.ui.step2.select_filter import ModFilterProxy
from wlb.ui.step2.selection_store import SelectionOrderStore

_ORDER_ROLE = Qt.ItemDataRole.UserRole + 8
_RAW_ROLE = Qt.ItemDataRole.UserRole + 7
_ISSUE_ROLE = Qt.ItemDataRole.UserRole + 11
_COMPONENT_ID_RE = re.compile(r"#\s*\d+\s+#\s*(\d+)")


def wire_model(
    view: QTreeView,
    model: QStandardItemModel,
    details_desc: QTextEdit,
    details_mod_id: QLabel,
    details_component: QLabel,
    details_version: QLabel,
    details_path: QLabel,
    details_author: QLabel,
    details_readme: QLabel,
    details_name: QLabel,
    store: SelectionOrderStore,
    game: str,
    extra_details: Callable[[QStandardItem], list[str]] | None = None,
) -> None:
    tracker = _OrderTracker(store, game)
    model.setProperty("_order_tracker", tracker)
    proxy = ModFilterProxy()
    proxy.setSourceModel(model)
    proxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    proxy.setFilterKeyColumn(0)
    view.setModel(proxy)
    view.setHeaderHidden(True)
    view.selectionModel().currentChanged.connect(
        lambda current, _prev: _apply_details(
            _to_source_index(current),
            details_desc,
            details_mod_id,
            details_component,
            details_version,
            details_path,
            details_author,
            details_readme,
            details_name,
            extra_details,
        )
    )
    model.itemChanged.connect(tracker.on_item_changed)


def _apply_details(
    index: QModelIndex,
    desc_box: QTextEdit,
    mod_id_label: QLabel,
    component_label: QLabel,
    version_label: QLabel,
    path_label: QLabel,
    author_label: QLabel,
    readme_label: QLabel,
    name_label: QLabel,
    extra_details: Callable[[QStandardItem], list[str]] | None,
) -> None:
    if not index.isValid():
        return
    model = index.model()
    if not isinstance(model, QStandardItemModel):
        return
    item = model.itemFromIndex(index)
    if item is None:
        return
    mod_id = item.data(Qt.ItemDataRole.UserRole) or "-"
    component = item.data(Qt.ItemDataRole.UserRole + 1) or "-"
    version = item.data(Qt.ItemDataRole.UserRole + 3) or "-"
    path = item.data(Qt.ItemDataRole.UserRole + 4) or "-"
    author = item.data(Qt.ItemDataRole.UserRole + 5) or "-"
    readme = item.data(Qt.ItemDataRole.UserRole + 6) or "-"
    issue = item.data(_ISSUE_ROLE)

    name_label.setText(item.text())
    mod_id_label.setText(mod_id)
    component_label.setText(_component_id(component, item))
    version_label.setText(version)
    path_label.setText(path)
    author_label.setText(author)
    readme_label.setText(readme)

    lines = [
        f"Mod ID: {mod_id}",
        f"Component: {component}",
        f"Version: {version}",
        f"Location/Path: {path}",
        f"Author: {author}",
        f"Readme Path: {readme}",
    ]
    if issue is not None:
        issue_type = getattr(issue, "issue", "")
        issue_message = getattr(issue, "message", "")
        lines.extend(
            [
                "",
                "Rule:",
                f"Type: {issue_type}",
                issue_message,
            ]
        )
    if extra_details is not None:
        details = extra_details(item)
        if details:
            lines.append("")
            lines.append("Checks:")
            lines.extend(details)
    desc_box.setPlainText("\n".join(lines))


class _OrderTracker:
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
            self._store.set_order(self._game, _ordered_items(model))
            return
        if item.checkState() == Qt.CheckState.Checked:
            if item.data(_ORDER_ROLE) is None:
                item.setData(self._next, _ORDER_ROLE)
                self._next += 1
        else:
            if item.data(_ORDER_ROLE) is not None:
                item.setData(None, _ORDER_ROLE)
        self._store.set_order(self._game, _ordered_items(model))

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
                if child.data(_ORDER_ROLE) is None:
                    child.setData(self._next, _ORDER_ROLE)
                    self._next += 1
            else:
                if child.data(_ORDER_ROLE) is not None:
                    child.setData(None, _ORDER_ROLE)


def _ordered_items(model: QStandardItemModel) -> list[str]:
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
            order = child.data(_ORDER_ROLE)
            raw = child.data(_RAW_ROLE) or child.text()
            if isinstance(order, int):
                items.append((order, raw))
    return [raw for _, raw in sorted(items, key=lambda x: x[0])]


def _to_source_index(index: QModelIndex) -> QModelIndex:
    model = index.model()
    if isinstance(model, QSortFilterProxyModel):
        return model.mapToSource(index)
    return index


def _component_id(display: str, item: QStandardItem) -> str:
    raw = item.data(_RAW_ROLE)
    if isinstance(raw, str):
        match = _COMPONENT_ID_RE.search(raw)
        if match:
            return match.group(1)
    return display
