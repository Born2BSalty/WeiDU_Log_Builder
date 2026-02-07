from __future__ import annotations

from PySide6.QtWidgets import QFormLayout, QGroupBox

from wlb.ui.widgets.path_picker import PathPicker


def build_tools_section() -> tuple[PathPicker, PathPicker, QGroupBox]:
    box = QGroupBox("Tools")
    form = QFormLayout(box)
    weidu = PathPicker(picker="file")
    installer = PathPicker(picker="file")
    form.addRow("WeiDU.exe:", weidu)
    form.addRow("Mod_Installer.exe:", installer)
    return weidu, installer, box
