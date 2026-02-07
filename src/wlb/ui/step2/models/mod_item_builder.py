from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem

from wlb.domain.models import ModInfo
from wlb.ui.step2.models.display_names import display_mod_name


def build_mod_item(mod: ModInfo) -> QStandardItem:
    mod_name = display_mod_name(mod.name)
    mod_item = QStandardItem(mod_name)
    _apply_mod_item_data(mod_item, mod, mod_name)
    return mod_item


def _apply_mod_item_data(mod_item: QStandardItem, mod: ModInfo, mod_name: str) -> None:
    mod_item.setEditable(False)
    mod_item.setToolTip(str(mod.tp2_path))
    mod_item.setData(mod_name, Qt.ItemDataRole.UserRole)
    mod_item.setData("-", Qt.ItemDataRole.UserRole + 1)
    mod_item.setData(mod.version or "-", Qt.ItemDataRole.UserRole + 3)
    mod_item.setData(str(mod.tp2_path), Qt.ItemDataRole.UserRole + 4)
    mod_item.setData(mod.author or "-", Qt.ItemDataRole.UserRole + 5)
    mod_item.setData(str(mod.readme_path) if mod.readme_path else "-", Qt.ItemDataRole.UserRole + 6)
    mod_item.setCheckable(True)
    mod_item.setCheckState(Qt.CheckState.Unchecked)
    mod_item.setData(True, Qt.ItemDataRole.UserRole + 2)
