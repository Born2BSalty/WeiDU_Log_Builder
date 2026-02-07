from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget


def build_footer_row() -> tuple[QWidget, QPushButton, QPushButton]:
    button_row = QWidget()
    row_layout = QHBoxLayout(button_row)
    row_layout.setContentsMargins(0, 0, 0, 0)

    back_button = QPushButton("Back")
    exit_button = QPushButton("Exit")

    row_layout.addStretch(1)
    row_layout.addWidget(back_button)
    row_layout.addWidget(exit_button)

    return button_row, back_button, exit_button
