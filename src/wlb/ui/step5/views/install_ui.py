from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtWidgets import QCheckBox, QLineEdit, QPlainTextEdit, QPushButton, QWidget


@dataclass
class InstallUi:
    root: QWidget
    start_button: QPushButton
    cancel_button: QPushButton
    minimal_checkbox: QCheckBox
    io_view: QPlainTextEdit
    input_line: QLineEdit
