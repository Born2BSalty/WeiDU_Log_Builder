from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QWidget

from wlb.ui.step1.views.section_types import SetupSections


def build_top_row(sections: SetupSections) -> QWidget:
    top_row = QWidget()
    top_layout = QHBoxLayout(top_row)
    top_layout.setContentsMargins(0, 0, 0, 0)
    top_layout.addWidget(sections.game_box)
    top_layout.addWidget(sections.options_box)
    top_layout.addWidget(sections.flags_box)
    return top_row
