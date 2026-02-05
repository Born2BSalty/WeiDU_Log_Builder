from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget

from wlb.ui.step1.setup_sections import build_setup_sections, set_log_mode
from wlb.ui.step1.setup_settings import load_settings, wire_settings
from wlb.ui.widgets import PageScaffold


class SetupPage(PageScaffold):
    def __init__(self, on_next: Callable[[], None] | None = None) -> None:
        super().__init__(
            title="Step 1: Setup",
            subtitle="Choose your game and mod folder to begin.",
        )
        self._settings = QSettings()
        self._on_next = on_next

        self.sections = build_setup_sections()
        top_row = QWidget()
        top_layout = QHBoxLayout(top_row)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.addWidget(self.sections.game_box)
        top_layout.addWidget(self.sections.options_box)
        self.body_layout.addWidget(top_row)
        self.body_layout.addWidget(self.sections.mods_box)
        self.body_layout.addWidget(self.sections.tools_box)
        self.body_layout.addWidget(self.sections.bgee_box)
        self.body_layout.addWidget(self.sections.bg2ee_box)
        self.body_layout.addWidget(self.sections.eet_box)

        button_row = QWidget()
        row_layout = QHBoxLayout(button_row)
        row_layout.setContentsMargins(0, 0, 0, 0)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self._handle_next)
        row_layout.addStretch(1)
        row_layout.addWidget(self.next_button)
        self.footer_layout.addWidget(button_row)

        self.sections.game_select.currentTextChanged.connect(self._on_game_changed)
        self.sections.logs_checkbox.toggled.connect(self._on_logs_toggled)
        self.sections.debug_checkbox.toggled.connect(self._on_debug_toggled)
        self.sections.trace_checkbox.toggled.connect(self._on_trace_toggled)
        self._on_game_changed(self.sections.game_select.currentText())
        load_settings(self.sections, self._settings)
        wire_settings(self.sections, self._settings)
        self._on_logs_toggled(self.sections.logs_checkbox.isChecked())

    def _on_game_changed(self, game: str) -> None:
        is_bgee = game == "BGEE"
        is_bg2ee = game == "BG2EE"
        is_eet = game == "EET"
        self.sections.bgee_box.setVisible(is_bgee)
        self.sections.bg2ee_box.setVisible(is_bg2ee)
        self.sections.eet_box.setVisible(is_eet)

    def _on_logs_toggled(self, checked: bool) -> None:
        set_log_mode(self.sections, checked)

    def _on_debug_toggled(self, checked: bool) -> None:
        if checked:
            self.sections.trace_checkbox.setChecked(False)

    def _on_trace_toggled(self, checked: bool) -> None:
        if checked:
            self.sections.debug_checkbox.setChecked(False)

    def _handle_next(self) -> None:
        if self._on_next is not None:
            self._on_next()
