from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSplitter, QVBoxLayout, QWidget

from wlb.ui.step5.views.boxes import build_controls_box, build_io_box
from wlb.ui.step5.views.install_ui import InstallUi


def build_install_ui() -> InstallUi:
    content = QWidget()
    content_layout = QVBoxLayout(content)
    content_layout.setContentsMargins(0, 0, 0, 0)
    content_layout.setSpacing(12)

    controls_box, start_button, cancel_button, minimal_checkbox = build_controls_box()
    io_box, io_view, input_line = build_io_box()

    content_layout.addWidget(controls_box)
    lower_split = QSplitter(Qt.Orientation.Horizontal)
    lower_split.addWidget(io_box)
    content_layout.addWidget(lower_split, 1)

    return InstallUi(
        root=content,
        start_button=start_button,
        cancel_button=cancel_button,
        minimal_checkbox=minimal_checkbox,
        io_view=io_view,
        input_line=input_line,
    )
