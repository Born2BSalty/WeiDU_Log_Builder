from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QLineEdit, QWidget


def build_search_row() -> tuple[QWidget, QLineEdit]:
    search_row = QWidget()
    search_input = QLineEdit()
    search_input.setPlaceholderText("Search mods or components...")
    search_layout = QHBoxLayout(search_row)
    _apply_search_layout(search_layout, search_input)
    return search_row, search_input


def _apply_search_layout(layout: QHBoxLayout, search_input: QLineEdit) -> None:
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(search_input, 1)
