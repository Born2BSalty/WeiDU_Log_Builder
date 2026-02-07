from __future__ import annotations

from PySide6.QtWidgets import QFormLayout, QGroupBox

from wlb.ui.widgets.path_picker import PathPicker


def build_mods_section() -> tuple[PathPicker, QGroupBox]:
    box = QGroupBox("Mods Folder")
    form = QFormLayout(box)
    picker = PathPicker(picker="dir")
    form.addRow("Your Mods Folder:", picker)
    return picker, box
