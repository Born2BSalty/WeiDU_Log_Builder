from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget


def build_footer_row() -> tuple[QWidget, QPushButton]:
    button_row = QWidget()
    row_layout = QHBoxLayout(button_row)
    row_layout.setContentsMargins(0, 0, 0, 0)

    next_button = QPushButton("Next")
    row_layout.addStretch(1)
    row_layout.addWidget(next_button)

    return button_row, next_button
