from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem

from wlb.ui.step2.compat.select_compat_types import ModStatus, StatusBundle


def status_for_item(
    item: QStandardItem, status_maps: dict[str, dict[Path, StatusBundle]]
) -> ModStatus | None:
    model = item.model()
    game = ""
    if model is not None:
        game = model.property("_game") or ""
    status_map = status_maps.get(str(game), {})
    tp2_path = item.data(Qt.ItemDataRole.UserRole + 4)
    if not tp2_path:
        return None
    bundle = status_map.get(Path(tp2_path))
    if bundle is None:
        return None
    index = item.data(Qt.ItemDataRole.UserRole + 9)
    if isinstance(index, int) and 0 <= index < len(bundle.components):
        return bundle.components[index]
    return bundle.header
