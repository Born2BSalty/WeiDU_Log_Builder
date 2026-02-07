from __future__ import annotations

from PySide6.QtWidgets import QTabWidget


def apply_game_tabs(tabs: QTabWidget, game: str) -> None:
    show_bgee = game in ("BGEE", "EET")
    show_bg2ee = game in ("BG2EE", "EET")
    bar = tabs.tabBar()
    bar.setTabVisible(0, show_bgee)
    bar.setTabVisible(1, show_bg2ee)
    bar.updateGeometry()
    bar.adjustSize()
    tabs.updateGeometry()
    if show_bgee:
        tabs.setCurrentIndex(0)
    elif show_bg2ee:
        tabs.setCurrentIndex(1)
