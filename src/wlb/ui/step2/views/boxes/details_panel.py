from __future__ import annotations

from PySide6.QtWidgets import (
    QGroupBox,
    QLabel,
    QPushButton,
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from wlb.ui.step2.views.boxes.details_buttons import build_details_buttons
from wlb.ui.step2.views.boxes.details_meta import build_details_meta
from wlb.ui.step2.views.boxes.details_panel_layout import apply_details_layout
from wlb.ui.step2.views.boxes.details_text import build_details_text


def build_details_panel() -> tuple[
    QWidget,
    QGroupBox,
    QTextEdit,
    QLabel,
    QLabel,
    QLabel,
    QLabel,
    QLabel,
    QLabel,
    QPushButton,
    QPushButton,
    QPushButton,
]:
    details_panel = QWidget()
    details_panel_layout = QVBoxLayout(details_panel)
    details_panel_layout.setContentsMargins(0, 0, 0, 0)

    details_box = QGroupBox("Details")
    details_layout = QVBoxLayout(details_box)
    details_layout.setContentsMargins(8, 8, 8, 8)

    details_desc, details_name = build_details_text()
    (
        details_meta,
        details_mod_id,
        details_component,
        details_version,
        details_path,
        details_author,
        details_readme,
    ) = build_details_meta()

    details_buttons, readme_button, web_button, tp2_button = build_details_buttons()

    apply_details_layout(details_layout, details_meta, details_buttons, details_desc)
    details_box.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
    details_panel_layout.addStretch(1)
    details_panel_layout.addWidget(details_box)

    return (
        details_panel,
        details_box,
        details_desc,
        details_name,
        details_mod_id,
        details_component,
        details_version,
        details_path,
        details_author,
        details_readme,
        tp2_button,
        readme_button,
        web_button,
    )
