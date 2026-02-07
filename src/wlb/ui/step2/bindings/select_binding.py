from __future__ import annotations

from collections.abc import Callable

from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QLabel, QTextEdit, QTreeView

from wlb.ui.step2.bindings.details_panel import apply_details
from wlb.ui.step2.bindings.order_tracker import OrderTracker
from wlb.ui.step2.bindings.view_proxy import attach_proxy
from wlb.ui.step2.models.selection_store import SelectionOrderStore
from wlb.ui.step2.views.view_utils import source_index


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
    tracker = OrderTracker(store, game)
    model.setProperty("_order_tracker", tracker)
    attach_proxy(view, model)
    view.selectionModel().currentChanged.connect(
        lambda current, _prev: apply_details(
            source_index(current),
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
