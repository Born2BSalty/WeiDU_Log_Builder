from __future__ import annotations

from PySide6.QtWidgets import QVBoxLayout, QWidget

from wlb.ui.step2.models.selection_store import SelectionOrderStore
from wlb.ui.step2.views.boxes import build_details_panel, build_list_panel
from wlb.ui.step2.views.height_sync import HeightSyncViews
from wlb.ui.step2.views.layout_splitter import build_main_splitter
from wlb.ui.step2.views.selection_ui import SelectionUi


def build_selection_ui(store: SelectionOrderStore) -> SelectionUi:
    container = QWidget()
    layout = QVBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)

    (
        list_panel,
        search_input,
        scan_button,
        cancel_scan_button,
        progress_label,
        tabs,
        bgee_view,
        bg2ee_view,
    ) = build_list_panel()

    (
        details_panel,
        details_box,
        details_desc,
        details_name,
        details_mod_id,
        details_component,
        details_version,
        details_path,
        details_author,
        details_readme,
        tp2_button,
        readme_button,
        web_button,
    ) = build_details_panel()

    splitter = build_main_splitter(list_panel, details_panel)
    layout.addWidget(splitter)

    HeightSyncViews(tabs, bgee_view, bg2ee_view, details_box)

    details_desc.setPlaceholderText("Click Scan Mods Folder to load components.")

    return SelectionUi(
        root=container,
        search_input=search_input,
        scan_button=scan_button,
        cancel_scan_button=cancel_scan_button,
        progress_label=progress_label,
        tabs=tabs,
        bgee_view=bgee_view,
        bg2ee_view=bg2ee_view,
        details_box=details_box,
        details_desc=details_desc,
        details_name=details_name,
        details_mod_id=details_mod_id,
        details_component=details_component,
        details_version=details_version,
        details_path=details_path,
        details_author=details_author,
        details_readme=details_readme,
        tp2_button=tp2_button,
        readme_button=readme_button,
        web_button=web_button,
    )
