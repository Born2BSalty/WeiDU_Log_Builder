from __future__ import annotations

from PySide6.QtWidgets import QListWidget, QTabWidget


def build_tabs_panel() -> tuple[QTabWidget, QListWidget, QListWidget]:
    tabs = QTabWidget()
    bgee_list = QListWidget()
    bg2ee_list = QListWidget()
    tabs.addTab(bgee_list, "BGEE")
    tabs.addTab(bg2ee_list, "BG2EE")
    return tabs, bgee_list, bg2ee_list
