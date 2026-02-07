from __future__ import annotations

from PySide6.QtWidgets import QLabel, QPushButton


def build_footer_widgets() -> tuple[QLabel, QPushButton, QPushButton]:
    scan_status = QLabel("Idle")
    back_button = QPushButton("Back")
    next_button = QPushButton("Next")
    return scan_status, back_button, next_button
