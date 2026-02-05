from __future__ import annotations

import re

from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel

from wlb.domain.models import ModInfo
from wlb.ui.step2.compat_rules_types import CompatIssue
from wlb.ui.step2.select_item_state import apply_component_state, apply_header_state

_RAW_ROLE = Qt.ItemDataRole.UserRole + 7
_ISSUE_ROLE = Qt.ItemDataRole.UserRole + 11
_TP2_LINE_RE = re.compile(r"^~.*~\s+#\d+\s+#\d+\s+//\s+(.+)$", re.IGNORECASE)
_COMPONENT_RE = re.compile(r"^\s*(\d+)\s*[:\-]\s*(.+)$")
_VERSION_TAIL_RE = re.compile(r":\s*(v?\d[\w.\-]*)\s*$", re.IGNORECASE)


def build_mods_model(
    mods: list[ModInfo], issues: dict[tuple[str, int], CompatIssue]
) -> QStandardItemModel:
    model = QStandardItemModel()
    model.setHorizontalHeaderLabels(["Mod / Component"])
    for mod in mods:
        mod_name = _display_mod_name(mod.name)
        mod_item = QStandardItem(mod_name)
        mod_item.setEditable(False)
        mod_item.setToolTip(str(mod.tp2_path))
        mod_item.setData(mod_name, Qt.ItemDataRole.UserRole)
        mod_item.setData("-", Qt.ItemDataRole.UserRole + 1)
        mod_item.setData(mod.version or "-", Qt.ItemDataRole.UserRole + 3)
        mod_item.setData(str(mod.tp2_path), Qt.ItemDataRole.UserRole + 4)
        mod_item.setData(mod.author or "-", Qt.ItemDataRole.UserRole + 5)
        mod_item.setData(
            str(mod.readme_path) if mod.readme_path else "-", Qt.ItemDataRole.UserRole + 6
        )
        mod_item.setCheckable(True)
        mod_item.setCheckState(Qt.CheckState.Unchecked)
        mod_item.setData(True, Qt.ItemDataRole.UserRole + 2)

        disabled_children = 0
        for idx, component in enumerate(mod.components):
            display = _display_name(component)
            comp_item = QStandardItem(display)
            comp_item.setEditable(False)
            comp_item.setToolTip(display)
            comp_item.setData(mod_name, Qt.ItemDataRole.UserRole)
            comp_item.setData(display, Qt.ItemDataRole.UserRole + 1)
            comp_item.setData(
                _component_version(component, mod.version), Qt.ItemDataRole.UserRole + 3
            )
            comp_item.setData(str(mod.tp2_path), Qt.ItemDataRole.UserRole + 4)
            comp_item.setData(mod.author or "-", Qt.ItemDataRole.UserRole + 5)
            comp_item.setData(
                str(mod.readme_path) if mod.readme_path else "-", Qt.ItemDataRole.UserRole + 6
            )
            comp_item.setData(component, _RAW_ROLE)
            issue = issues.get((str(mod.tp2_path), idx))
            if issue is not None:
                comp_item.setData(issue, _ISSUE_ROLE)
            disabled = _issue_disables(issue)
            apply_component_state(comp_item, disabled=disabled)
            comp_item.setCheckState(Qt.CheckState.Unchecked)
            comp_item.setData(False, Qt.ItemDataRole.UserRole + 2)
            mod_item.appendRow(comp_item)
            if disabled:
                disabled_children += 1

        if mod_item.rowCount() > 0 and disabled_children == mod_item.rowCount():
            apply_header_state(mod_item, disabled=True)
        model.appendRow(mod_item)
    return model


def _display_name(component: str) -> str:
    line = component.strip()
    tp2_match = _TP2_LINE_RE.match(line)
    if tp2_match:
        return tp2_match.group(1).strip()
    match = _COMPONENT_RE.match(line)
    if match:
        return match.group(2).strip()
    return line


def _display_mod_name(name: str) -> str:
    lowered = name.lower()
    if lowered.startswith("setup-"):
        return name[6:]
    if lowered.startswith("setup_"):
        return name[6:]
    return name


def _component_version(component: str, fallback: str | None) -> str:
    match = _VERSION_TAIL_RE.search(component.strip())
    if match:
        return match.group(1).strip()
    return fallback or "-"


def _issue_disables(issue: CompatIssue | None) -> bool:
    if issue is None:
        return False
    return issue.issue in {"included", "not_needed", "not_compatible"}
