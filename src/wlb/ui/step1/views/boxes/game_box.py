from __future__ import annotations

from PySide6.QtWidgets import QComboBox, QFormLayout, QGroupBox


def build_game_section() -> tuple[QComboBox, QGroupBox]:
    box = QGroupBox("Game Selection")
    form = QFormLayout(box)
    game = QComboBox()
    game.addItems(["BGEE", "BG2EE", "EET"])
    form.addRow("Game Install:", game)
    return game, box
