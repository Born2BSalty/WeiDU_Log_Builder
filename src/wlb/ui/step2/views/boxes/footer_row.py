from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget

from wlb.ui.step2.views.boxes.footer_widgets import build_footer_widgets


def build_footer_row() -> tuple[QWidget, QLabel, QPushButton, QPushButton]:
    button_row = QWidget()
    scan_status, back_button, next_button = build_footer_widgets()

    row_layout = QHBoxLayout(button_row)
    _apply_footer_layout(row_layout, scan_status, back_button, next_button)

    return button_row, scan_status, back_button, next_button


def _apply_footer_layout(
    layout: QHBoxLayout,
    scan_status: QLabel,
    back_button: QPushButton,
    next_button: QPushButton,
) -> None:
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(scan_status)
    layout.addStretch(1)
    layout.addWidget(back_button)
    layout.addWidget(next_button)
