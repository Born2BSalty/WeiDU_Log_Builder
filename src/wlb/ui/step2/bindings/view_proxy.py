from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTreeView

from wlb.ui.step2.models.select_filter import ModFilterProxy


def attach_proxy(view: QTreeView, model) -> ModFilterProxy:
    proxy = ModFilterProxy()
    proxy.setSourceModel(model)
    proxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    proxy.setFilterKeyColumn(0)
    view.setModel(proxy)
    view.setHeaderHidden(True)
    return proxy
