from __future__ import annotations

from collections.abc import Callable
from contextlib import suppress
from pathlib import Path

from PySide6.QtWidgets import QCheckBox, QPlainTextEdit

from wlb.services.settings_service import SettingsService
from wlb.ui.step5.controllers.output_log import default_install_log
from wlb.ui.step5.views.output.output_filter import FilterState, filter_output, strip_ansi
from wlb.ui.step5.views.output.output_view import OutputViewState, append_output


class InstallOutputController:
    def __init__(
        self,
        io_view: QPlainTextEdit,
        minimal_checkbox: QCheckBox,
        settings: SettingsService,
        input_buffer: Callable[[], str],
    ) -> None:
        self._io_view = io_view
        self._minimal_checkbox = minimal_checkbox
        self._settings = settings
        self._input_buffer = input_buffer
        self._filter_state = FilterState()
        self._output_state = OutputViewState()
        self._follow_output = True
        self._install_log: Path | None = None
        self._install_log_file = None
        self._io_view.verticalScrollBar().valueChanged.connect(self.on_scroll)

    @property
    def filter_state(self) -> FilterState:
        return self._filter_state

    def reset(self) -> None:
        self._io_view.clear()
        self._filter_state.reset()
        self._output_state.reset()
        self._close_log()
        if self._settings.log_install():
            self._install_log = default_install_log(self._settings)
            self._install_log_file = self._install_log.open("a", encoding="utf-8", errors="ignore")

    def append(self, text: str) -> None:
        text = strip_ansi(text)
        if self._install_log_file is not None:
            with suppress(Exception):
                self._install_log_file.write(text)
                self._install_log_file.flush()

        scrollbar = self._io_view.verticalScrollBar()
        original_value = scrollbar.value()

        if self._minimal_checkbox.isChecked() and "Command:" not in text:
            text = filter_output(self._filter_state, text)
            if not text:
                return

        append_output(self._io_view, self._output_state, self._input_buffer(), text)
        if self._follow_output:
            scrollbar.setValue(scrollbar.maximum())
        else:
            scrollbar.setValue(original_value)

    def close(self) -> None:
        self._close_log()

    def on_scroll(self, value: int) -> None:
        scrollbar = self._io_view.verticalScrollBar()
        self._follow_output = value >= scrollbar.maximum() - 2

    def _close_log(self) -> None:
        if self._install_log_file is not None:
            with suppress(Exception):
                self._install_log_file.close()
        self._install_log_file = None
