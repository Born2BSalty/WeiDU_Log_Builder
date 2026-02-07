from __future__ import annotations

from PySide6.QtWidgets import QLabel, QTextEdit


def build_details_text() -> tuple[QTextEdit, QLabel]:
    details_name = QLabel("Select an item")
    details_desc = QTextEdit()
    details_desc.setReadOnly(True)
    details_desc.setPlaceholderText("Select an item to view details.")
    details_desc.setMinimumHeight(70)
    return details_desc, details_name
