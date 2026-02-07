from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget


def build_details_buttons() -> tuple[QWidget, QPushButton, QPushButton, QPushButton]:
    details_buttons = QWidget()
    readme_button = QPushButton("Readme")
    web_button = QPushButton("Web")
    tp2_button = QPushButton("TP2")
    details_buttons_layout = QHBoxLayout(details_buttons)
    _apply_button_layout(details_buttons_layout, readme_button, web_button, tp2_button)
    return details_buttons, readme_button, web_button, tp2_button


def _apply_button_layout(
    layout: QHBoxLayout,
    readme_button: QPushButton,
    web_button: QPushButton,
    tp2_button: QPushButton,
) -> None:
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(readme_button)
    layout.addWidget(web_button)
    layout.addWidget(tp2_button)
