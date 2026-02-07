from __future__ import annotations

from PySide6.QtGui import QColor, QStandardItem

from wlb.ui.step2.compat.compat_rules_types import CompatIssue


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


def issue_disables(issue: CompatIssue | None) -> bool:
    if issue is None:
        return False
    return issue.issue in {"included", "not_needed", "not_compatible"}
