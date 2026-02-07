from __future__ import annotations

import re
from collections.abc import Callable

from PySide6.QtCore import QModelIndex, Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QLabel, QTextEdit

from wlb.ui.step2.models.item_roles import ISSUE_ROLE, RAW_ROLE

_COMPONENT_ID_RE = re.compile(r"#\s*\d+\s+#\s*(\d+)")


def apply_details(
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
    issue = item.data(ISSUE_ROLE)

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


def _component_id(display: str, item: QStandardItem) -> str:
    raw = item.data(RAW_ROLE)
    if isinstance(raw, str):
        match = _COMPONENT_ID_RE.search(raw)
        if match:
            return match.group(1)
    return display
