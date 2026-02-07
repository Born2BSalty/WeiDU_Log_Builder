from __future__ import annotations

from PySide6.QtWidgets import QFormLayout, QLabel, QWidget

from wlb.ui.step2.views.boxes.details_meta_labels import build_details_meta_labels
from wlb.ui.step2.views.boxes.details_meta_rows import apply_details_meta_rows


def build_details_meta() -> tuple[
    QWidget,
    QLabel,
    QLabel,
    QLabel,
    QLabel,
    QLabel,
    QLabel,
]:
    details_meta = QWidget()
    details_meta_layout = QFormLayout(details_meta)
    (
        details_mod_id,
        details_component,
        details_version,
        details_path,
        details_author,
        details_readme,
    ) = build_details_meta_labels()
    apply_details_meta_rows(
        details_meta_layout,
        details_mod_id,
        details_component,
        details_version,
        details_path,
        details_author,
        details_readme,
    )
    details_meta.setVisible(False)
    return (
        details_meta,
        details_mod_id,
        details_component,
        details_version,
        details_path,
        details_author,
        details_readme,
    )
