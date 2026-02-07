from __future__ import annotations

from PySide6.QtWidgets import QVBoxLayout, QWidget


def apply_details_layout(
    layout: QVBoxLayout, details_meta: QWidget, details_buttons: QWidget, details_desc: QWidget
) -> None:
    layout.addWidget(details_meta)
    layout.addWidget(details_buttons)
    layout.addWidget(details_desc)
