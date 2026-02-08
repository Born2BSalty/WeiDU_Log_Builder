from __future__ import annotations

import re
from collections.abc import Callable

from PySide6.QtCore import QSettings

from wlb.ui.step1.controllers.settings import load_settings, wire_settings
from wlb.ui.step1.views.boxes import build_footer_row, build_top_row
from wlb.ui.step1.views.sections import build_setup_sections, set_log_mode
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
        top_row = build_top_row(self.sections)
        self.body_layout.addWidget(top_row)
        self.body_layout.addWidget(self.sections.mods_box)
        self.body_layout.addWidget(self.sections.component_logs_box)
        self.body_layout.addWidget(self.sections.tools_box)
        self.body_layout.addWidget(self.sections.bgee_box)
        self.body_layout.addWidget(self.sections.bg2ee_box)
        self.body_layout.addWidget(self.sections.eet_box)

        button_row, self.next_button = build_footer_row()
        self.next_button.clicked.connect(self._handle_next)
        self.footer_layout.addWidget(button_row)

        self.sections.game_select.currentTextChanged.connect(self._on_game_changed)
        self.sections.logs_checkbox.toggled.connect(self._on_logs_toggled)
        self.sections.debug_checkbox.toggled.connect(self._on_debug_toggled)
        self.sections.trace_checkbox.toggled.connect(self._on_trace_toggled)
        self.sections.weidu_log_mode_checkbox.toggled.connect(self._on_log_mode_toggled)
        self.sections.weidu_log_log_checkbox.toggled.connect(self._on_per_component_toggled)
        self.sections.weidu_log_picker.edit.textChanged.connect(
            self._on_component_logs_path_changed
        )
        self.sections.generate_dir_checkbox.toggled.connect(self._on_generate_dir_toggled)
        self.sections.pre_eet_checkbox.toggled.connect(self._on_pre_eet_toggled)
        self.sections.new_eet_checkbox.toggled.connect(self._on_new_eet_toggled)
        self._on_game_changed(self.sections.game_select.currentText())
        load_settings(self.sections, self._settings)
        wire_settings(self.sections, self._settings)
        self._on_logs_toggled(self.sections.logs_checkbox.isChecked())
        self._on_log_mode_toggled(self.sections.weidu_log_mode_checkbox.isChecked())
        self._on_per_component_toggled(self.sections.weidu_log_log_checkbox.isChecked())
        self._on_generate_dir_toggled(self.sections.generate_dir_checkbox.isChecked())
        self._on_pre_eet_toggled(self.sections.pre_eet_checkbox.isChecked())
        self._on_new_eet_toggled(self.sections.new_eet_checkbox.isChecked())

    def _on_game_changed(self, game: str) -> None:
        is_bgee = game == "BGEE"
        is_bg2ee = game == "BG2EE"
        is_eet = game == "EET"
        self.sections.bgee_box.setVisible(is_bgee)
        self.sections.bg2ee_box.setVisible(is_bg2ee)
        self.sections.eet_box.setVisible(is_eet)
        self.sections.pre_eet_checkbox.setVisible(is_eet)
        self.sections.new_eet_checkbox.setVisible(is_eet)
        self.sections.generate_dir_checkbox.setVisible(is_bgee or is_bg2ee)
        self._on_generate_dir_toggled(self.sections.generate_dir_checkbox.isChecked())
        self._on_pre_eet_toggled(self.sections.pre_eet_checkbox.isChecked())
        self._on_new_eet_toggled(self.sections.new_eet_checkbox.isChecked())

    def _on_logs_toggled(self, checked: bool) -> None:
        set_log_mode(self.sections, checked)

    def _on_debug_toggled(self, checked: bool) -> None:
        if checked:
            self.sections.trace_checkbox.setChecked(False)

    def _on_trace_toggled(self, checked: bool) -> None:
        if checked:
            self.sections.debug_checkbox.setChecked(False)

    def _on_log_mode_toggled(self, checked: bool) -> None:
        self.sections.component_logs_box.setVisible(checked)
        if not checked:
            self.sections.component_logs_note.setVisible(False)
            self.sections.weidu_log_label.setVisible(False)
            self.sections.weidu_log_picker.setVisible(False)
        else:
            self._on_per_component_toggled(self.sections.weidu_log_log_checkbox.isChecked())

    def _on_per_component_toggled(self, checked: bool) -> None:
        self.sections.weidu_log_label.setVisible(checked)
        self.sections.weidu_log_picker.setVisible(checked)
        if not checked:
            self.sections.component_logs_note.setVisible(False)

    def _on_component_logs_path_changed(self, text: str) -> None:
        if not self.sections.weidu_log_log_checkbox.isChecked():
            self.sections.component_logs_note.setVisible(False)
            return
        if " " not in text:
            self.sections.component_logs_note.setVisible(False)
            return
        sanitized = re.sub(r"\s+", "_", text)
        self.sections.component_logs_note.setText(f"Logs will be written to: {sanitized}")
        self.sections.component_logs_note.setVisible(True)

    def _on_generate_dir_toggled(self, checked: bool) -> None:
        self.sections.bgee_generate_label.setVisible(checked)
        self.sections.bgee_generate_picker.setVisible(checked)
        self.sections.bgee_generate_summary.setVisible(checked)
        self.sections.bg2ee_generate_label.setVisible(checked)
        self.sections.bg2ee_generate_picker.setVisible(checked)
        self.sections.bg2ee_generate_summary.setVisible(checked)

    def _on_pre_eet_toggled(self, checked: bool) -> None:
        self.sections.eet_pre_label.setVisible(checked)
        self.sections.eet_pre_picker.setVisible(checked)
        self.sections.eet_pre_summary.setVisible(checked)

    def _on_new_eet_toggled(self, checked: bool) -> None:
        self.sections.eet_new_label.setVisible(checked)
        self.sections.eet_new_picker.setVisible(checked)
        self.sections.eet_new_summary.setVisible(checked)

    def _handle_next(self) -> None:
        if self._on_next is not None:
            self._on_next()
