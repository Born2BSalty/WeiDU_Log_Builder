from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import QEvent, QObject
from PySide6.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSplitter,
    QTabWidget,
    QTextEdit,
    QTreeView,
    QVBoxLayout,
    QWidget,
)

from wlb.ui.step2.selection_store import SelectionOrderStore


@dataclass
class SelectionUi:
    root: QWidget
    search_input: QLineEdit
    scan_button: QPushButton
    cancel_scan_button: QPushButton
    progress_label: QLabel
    tabs: QTabWidget
    bgee_view: QTreeView
    bg2ee_view: QTreeView
    details_box: QGroupBox
    details_desc: QTextEdit
    details_name: QLabel
    details_mod_id: QLabel
    details_component: QLabel
    details_version: QLabel
    details_path: QLabel
    details_author: QLabel
    details_readme: QLabel
    tp2_button: QPushButton
    readme_button: QPushButton


def build_selection_ui(store: SelectionOrderStore) -> SelectionUi:
    container = QWidget()
    layout = QVBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)

    splitter = QSplitter()
    splitter.setChildrenCollapsible(False)

    list_panel = QWidget()
    list_layout = QVBoxLayout(list_panel)
    list_layout.setContentsMargins(0, 0, 0, 0)
    list_title = QLabel("Mods / Components")

    search_row = QWidget()
    search_layout = QHBoxLayout(search_row)
    search_layout.setContentsMargins(0, 0, 0, 0)
    search_input = QLineEdit()
    search_input.setPlaceholderText("Search mods or components...")
    search_layout.addWidget(search_input, 1)

    scan_row = QWidget()
    scan_layout = QHBoxLayout(scan_row)
    scan_layout.setContentsMargins(8, 6, 8, 6)
    scan_layout.setSpacing(8)
    scan_button = QPushButton("Scan Mods Folder")
    cancel_scan_button = QPushButton("Cancel Scan")
    progress_label = QLabel("Idle")
    scan_layout.addWidget(scan_button)
    scan_layout.addWidget(cancel_scan_button)
    scan_layout.addWidget(progress_label)
    scan_layout.addStretch(1)

    tabs = QTabWidget()
    bgee_view = QTreeView()
    bg2ee_view = QTreeView()
    bgee_view.setHeaderHidden(False)
    bg2ee_view.setHeaderHidden(False)
    tabs.addTab(bgee_view, "BGEE")
    tabs.addTab(bg2ee_view, "BG2EE")

    list_layout.addWidget(search_row)
    list_layout.addWidget(scan_row)
    list_layout.addWidget(list_title)
    list_layout.addWidget(tabs)

    details_panel = QWidget()
    details_panel_layout = QVBoxLayout(details_panel)
    details_panel_layout.setContentsMargins(0, 0, 0, 0)

    details_box = QGroupBox("Details")
    details_layout = QVBoxLayout(details_box)
    details_layout.setContentsMargins(8, 8, 8, 8)

    details_name = QLabel("Select an item")
    details_desc = QTextEdit()
    details_desc.setReadOnly(True)
    details_desc.setPlaceholderText("Select an item to view details.")
    details_desc.setMinimumHeight(70)
    details_meta = QWidget()
    details_meta_layout = QFormLayout(details_meta)
    details_mod_id = QLabel("-")
    details_component = QLabel("-")
    details_version = QLabel("-")
    details_path = QLabel("-")
    details_author = QLabel("-")
    details_readme = QLabel("-")
    details_meta_layout.addRow("Mod ID:", details_mod_id)
    details_meta_layout.addRow("Component:", details_component)
    details_meta_layout.addRow("Version:", details_version)
    details_meta_layout.addRow("Location/Path:", details_path)
    details_meta_layout.addRow("Author:", details_author)
    details_meta_layout.addRow("Readme Path:", details_readme)
    details_meta.setVisible(False)

    details_buttons = QWidget()
    details_buttons_layout = QHBoxLayout(details_buttons)
    details_buttons_layout.setContentsMargins(0, 0, 0, 0)
    readme_button = QPushButton("Readme")
    web_button = QPushButton("Web")
    tp2_button = QPushButton("TP2")
    details_buttons_layout.addWidget(readme_button)
    details_buttons_layout.addWidget(web_button)
    details_buttons_layout.addWidget(tp2_button)

    details_layout.addWidget(details_meta)
    details_layout.addWidget(details_buttons)
    details_layout.addWidget(details_desc)
    details_box.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
    details_panel_layout.addStretch(1)
    details_panel_layout.addWidget(details_box)

    splitter.addWidget(list_panel)
    splitter.addWidget(details_panel)
    splitter.setStretchFactor(0, 4)
    splitter.setStretchFactor(1, 2)

    layout.addWidget(splitter)

    _HeightSyncViews(tabs, bgee_view, bg2ee_view, details_box)

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
    )


class _HeightSyncViews(QObject):
    def __init__(
        self,
        tabs: QTabWidget,
        bgee_view: QTreeView,
        bg2ee_view: QTreeView,
        details_box: QGroupBox,
    ) -> None:
        super().__init__(tabs)
        self._tabs = tabs
        self._bgee_view = bgee_view
        self._bg2ee_view = bg2ee_view
        self._details_box = details_box
        self._bgee_view.viewport().installEventFilter(self)
        self._bg2ee_view.viewport().installEventFilter(self)
        self._tabs.currentChanged.connect(self._apply)
        self._apply()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Type.Resize:
            self._apply()
        return False

    def _active_view(self) -> QTreeView:
        return self._bgee_view if self._tabs.currentIndex() == 0 else self._bg2ee_view

    def _apply(self) -> None:
        view = self._active_view()
        height = view.viewport().height()
        self._details_box.setFixedHeight(max(100, height))
