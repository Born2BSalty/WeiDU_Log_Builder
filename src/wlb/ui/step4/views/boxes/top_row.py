from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget


def build_top_row() -> tuple[QWidget, QPushButton]:
    top_row = QWidget()
    top_layout = QHBoxLayout(top_row)
    top_layout.setContentsMargins(0, 0, 0, 0)
    save_button = QPushButton("Save (weidu.log)")
    top_layout.addWidget(save_button)
    top_layout.addStretch(1)
    return top_row, save_button
