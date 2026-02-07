from __future__ import annotations

from PySide6.QtWidgets import QFormLayout, QLabel


def apply_details_meta_rows(
    layout: QFormLayout,
    details_mod_id: QLabel,
    details_component: QLabel,
    details_version: QLabel,
    details_path: QLabel,
    details_author: QLabel,
    details_readme: QLabel,
) -> None:
    layout.addRow("Mod ID:", details_mod_id)
    layout.addRow("Component:", details_component)
    layout.addRow("Version:", details_version)
    layout.addRow("Location/Path:", details_path)
    layout.addRow("Author:", details_author)
    layout.addRow("Readme Path:", details_readme)
