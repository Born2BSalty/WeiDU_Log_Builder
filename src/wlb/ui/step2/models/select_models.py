from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel

from wlb.domain.models import ModInfo
from wlb.ui.step2.compat.compat_rules_types import CompatIssue
from wlb.ui.step2.models.item_builders import build_component_item, build_mod_item
from wlb.ui.step2.models.select_item_state import apply_header_state


def build_mods_model(
    mods: list[ModInfo], issues: dict[tuple[str, int], CompatIssue]
) -> QStandardItemModel:
    model = QStandardItemModel()
    model.setHorizontalHeaderLabels(["Mod / Component"])
    for mod in mods:
        mod_item = build_mod_item(mod)
        mod_name = mod_item.data(Qt.ItemDataRole.UserRole) or mod_item.text()

        disabled_children = 0
        for idx, component in enumerate(mod.components):
            issue = issues.get((str(mod.tp2_path), idx))
            comp_item, disabled = build_component_item(mod, str(mod_name), component, issue)
            mod_item.appendRow(comp_item)
            if disabled:
                disabled_children += 1

        if mod_item.rowCount() > 0 and disabled_children == mod_item.rowCount():
            apply_header_state(mod_item, disabled=True)
        model.appendRow(mod_item)
    return model
