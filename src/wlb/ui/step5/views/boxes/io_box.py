from __future__ import annotations

from PySide6.QtWidgets import QGroupBox, QLineEdit, QPlainTextEdit, QVBoxLayout


def build_io_box() -> tuple[QGroupBox, QPlainTextEdit, QLineEdit]:
    io_box = QGroupBox("Interactive Installer")
    io_layout = QVBoxLayout(io_box)
    io_layout.setContentsMargins(8, 8, 8, 8)
    io_layout.setSpacing(8)

    io_view = QPlainTextEdit()
    io_view.setReadOnly(True)
    io_view.setPlaceholderText("WeiDU output and prompts will appear here...")
    io_layout.addWidget(io_view, 1)

    input_line = QLineEdit()
    input_line.setPlaceholderText("Type response here and press Enter…")
    io_layout.addWidget(input_line)

    return io_box, io_view, input_line
