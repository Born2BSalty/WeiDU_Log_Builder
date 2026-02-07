from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget

from wlb.ui.step2.views.boxes.scan_widgets import build_scan_widgets


def build_scan_row() -> tuple[QWidget, QPushButton, QPushButton, QLabel]:
    scan_row = QWidget()
    scan_layout = QHBoxLayout(scan_row)
    _apply_scan_layout(scan_layout)
    scan_button, cancel_scan_button, progress_label = build_scan_widgets()
    _apply_scan_widgets(scan_layout, scan_button, cancel_scan_button, progress_label)
    return scan_row, scan_button, cancel_scan_button, progress_label


def _apply_scan_layout(layout: QHBoxLayout) -> None:
    layout.setContentsMargins(8, 6, 8, 6)
    layout.setSpacing(8)


def _apply_scan_widgets(
    layout: QHBoxLayout,
    scan_button: QPushButton,
    cancel_scan_button: QPushButton,
    progress_label: QLabel,
) -> None:
    layout.addWidget(scan_button)
    layout.addWidget(cancel_scan_button)
    layout.addWidget(progress_label)
    layout.addStretch(1)
