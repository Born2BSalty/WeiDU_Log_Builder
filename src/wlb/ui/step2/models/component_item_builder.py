from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem

from wlb.domain.models import ModInfo
from wlb.ui.step2.compat.compat_rules_types import CompatIssue
from wlb.ui.step2.models.display_names import component_version, display_component_name
from wlb.ui.step2.models.item_roles import ISSUE_ROLE, RAW_ROLE
from wlb.ui.step2.models.select_item_state import apply_component_state, issue_disables


def build_component_item(
    mod: ModInfo, mod_name: str, component: str, issue: CompatIssue | None
) -> tuple[QStandardItem, bool]:
    display = display_component_name(component)
    comp_item = QStandardItem(display)
    disabled = _apply_component_data(comp_item, mod, mod_name, component, issue)
    return comp_item, disabled


def _apply_component_data(
    comp_item: QStandardItem,
    mod: ModInfo,
    mod_name: str,
    component: str,
    issue: CompatIssue | None,
) -> bool:
    display = display_component_name(component)
    comp_item.setEditable(False)
    comp_item.setToolTip(display)
    comp_item.setData(mod_name, Qt.ItemDataRole.UserRole)
    comp_item.setData(display, Qt.ItemDataRole.UserRole + 1)
    comp_item.setData(component_version(component, mod.version), Qt.ItemDataRole.UserRole + 3)
    comp_item.setData(str(mod.tp2_path), Qt.ItemDataRole.UserRole + 4)
    comp_item.setData(mod.author or "-", Qt.ItemDataRole.UserRole + 5)
    comp_item.setData(
        str(mod.readme_path) if mod.readme_path else "-", Qt.ItemDataRole.UserRole + 6
    )
    comp_item.setData(component, RAW_ROLE)
    if issue is not None:
        comp_item.setData(issue, ISSUE_ROLE)
    disabled = issue_disables(issue)
    apply_component_state(comp_item, disabled=disabled)
    comp_item.setCheckState(Qt.CheckState.Unchecked)
    comp_item.setData(False, Qt.ItemDataRole.UserRole + 2)
    return disabled
