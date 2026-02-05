from __future__ import annotations

from PySide6.QtWidgets import QFileDialog, QHBoxLayout, QLineEdit, QPushButton, QWidget


class PathPicker(QWidget):
    def __init__(self, picker: str) -> None:
        super().__init__()
        self._picker = picker
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.edit = QLineEdit()
        self.button = QPushButton("Browse")
        self.button.clicked.connect(self._pick_path)

        layout.addWidget(self.edit, 1)
        layout.addWidget(self.button)

    def text(self) -> str:
        return self.edit.text()

    def set_text(self, value: str) -> None:
        self.edit.setText(value)

    def set_picker(self, picker: str) -> None:
        self._picker = picker

    def _pick_path(self) -> None:
        if self._picker == "dir":
            path = QFileDialog.getExistingDirectory()
        else:
            path, _ = QFileDialog.getOpenFileName()
        if path:
            self.edit.setText(path)
