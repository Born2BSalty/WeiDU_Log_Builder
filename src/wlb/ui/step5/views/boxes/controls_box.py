from __future__ import annotations

from PySide6.QtWidgets import QCheckBox, QGroupBox, QHBoxLayout, QPushButton


def build_controls_box() -> tuple[QGroupBox, QPushButton, QPushButton, QCheckBox]:
    controls_box = QGroupBox("Installer Controls")
    controls_layout = QHBoxLayout(controls_box)
    controls_layout.setContentsMargins(8, 8, 8, 8)
    start_button = QPushButton("Start Install")
    cancel_button = QPushButton("Cancel")
    minimal_checkbox = QCheckBox("Minimal Output")
    controls_layout.addWidget(start_button)
    controls_layout.addWidget(cancel_button)
    controls_layout.addWidget(minimal_checkbox)
    controls_layout.addStretch(1)
    return controls_box, start_button, cancel_button, minimal_checkbox
