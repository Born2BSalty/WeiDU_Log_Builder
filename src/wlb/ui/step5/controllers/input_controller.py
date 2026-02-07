from __future__ import annotations

import os
from collections.abc import Callable

from PySide6.QtCore import QObject, Qt
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QLineEdit, QPlainTextEdit

from wlb.ui.step5.controllers.input_sanitize import sanitize_input
from wlb.ui.step5.viewmodels.install_viewmodel import InstallViewModel
from wlb.ui.step5.views.output.output_filter import FilterState


class ConsoleInputController(QObject):
    def __init__(
        self,
        io_view: QPlainTextEdit,
        input_line: QLineEdit,
        view_model: InstallViewModel,
        output: Callable[[str], None],
        filter_state: FilterState,
    ) -> None:
        super().__init__(io_view)
        self._io_view = io_view
        self._input_line = input_line
        self._view_model = view_model
        self._output = output
        self._filter_state = filter_state
        self._input_buffer = ""

        self._input_line.returnPressed.connect(self._send_input_line)
        self._io_view.installEventFilter(self)

    def current_buffer(self) -> str:
        return self._input_buffer

    def reset(self) -> None:
        self._input_buffer = ""
        self._input_line.clear()

    def eventFilter(self, watched, event):  # type: ignore[override]
        if watched is self._io_view and event.type() == event.Type.KeyPress:
            if (event.modifiers() & Qt.KeyboardModifier.ControlModifier) and (
                event.key() in (Qt.Key.Key_C, Qt.Key.Key_A, Qt.Key.Key_V)
            ):
                return False

            key = event.key()
            if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                self._send_buffered_input()
                return True

            if key == Qt.Key.Key_Backspace:
                self._erase_last_char()
                return True

            text = event.text()
            if text:
                self._input_buffer += text
                cursor = self._io_view.textCursor()
                cursor.movePosition(QTextCursor.End)
                cursor.insertText(text)
                return True
        return super().eventFilter(watched, event)

    def _send_input_line(self) -> None:
        text = self._input_line.text()
        clean = sanitize_input(text)
        self._send_input(clean)
        self._input_line.clear()

    def _send_buffered_input(self) -> None:
        if self._input_buffer:
            clean = sanitize_input(self._input_buffer)
            self._send_input(clean)
            self._input_buffer = ""
        else:
            self._send_input("")

    def _send_input(self, text: str) -> None:
        newline = "\r\n" if os.name == "nt" else "\n"
        if text:
            self._view_model.send_input(f"{text}{newline}")
            self._output(f"> {text}\n")
        else:
            self._view_model.send_input(newline)
            self._output(">\n")
        self._filter_state.reset_question()

    def _erase_last_char(self) -> None:
        if not self._input_buffer:
            return
        self._input_buffer = self._input_buffer[:-1]
        cursor = self._io_view.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.movePosition(QTextCursor.Left, QTextCursor.MoveMode.KeepAnchor, 1)
        cursor.removeSelectedText()
