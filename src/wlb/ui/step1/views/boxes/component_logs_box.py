from __future__ import annotations

from PySide6.QtWidgets import QFormLayout, QGroupBox, QLabel

from wlb.ui.widgets.path_picker import PathPicker


def build_component_logs_section() -> tuple[QGroupBox, PathPicker, QLabel]:
    box = QGroupBox("Component Logs Folder")
    form = QFormLayout(box)
    picker = PathPicker(picker="dir")
    form.addRow("Per‑component logs:", picker)
    note = QLabel("")
    note.setVisible(False)
    form.addRow("", note)
    box.setVisible(False)
    return box, picker, note
