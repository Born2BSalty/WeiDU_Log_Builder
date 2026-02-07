from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtWidgets import (
    QGroupBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QTabWidget,
    QTextEdit,
    QTreeView,
    QWidget,
)


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
    web_button: QPushButton
