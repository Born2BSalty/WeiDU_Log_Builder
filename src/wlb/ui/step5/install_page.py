from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import (
    QCheckBox,
    QGroupBox,
    QHBoxLayout,
    QPlainTextEdit,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from wlb.services.install_service import InstallRequest
from wlb.ui.step5.install_viewmodel import InstallViewModel
from wlb.ui.widgets import PageScaffold


class InstallPage(PageScaffold):
    install_requested = Signal()
    output = Signal(str)

    def __init__(
        self,
        view_model: InstallViewModel,
        on_back: Callable[[], None] | None = None,
    ) -> None:
        super().__init__(
            title="Step 5: Installation & Progress",
            subtitle="Run installation and track progress.",
        )
        self._on_back = on_back
        self._view_model = view_model
        self.output.connect(self._append_output)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(12)

        controls_box = QGroupBox("Installer Controls")
        controls_layout = QHBoxLayout(controls_box)
        controls_layout.setContentsMargins(8, 8, 8, 8)
        start_button = QPushButton("Start Install")
        cancel_button = QPushButton("Cancel")
        self._minimal_checkbox = QCheckBox("Minimal Output")
        start_button.clicked.connect(self.install_requested.emit)
        cancel_button.clicked.connect(self._on_cancel)
        controls_layout.addWidget(start_button)
        controls_layout.addWidget(cancel_button)
        controls_layout.addWidget(self._minimal_checkbox)
        controls_layout.addStretch(1)

        io_box = QGroupBox("Interactive Installer")
        io_layout = QVBoxLayout(io_box)
        io_layout.setContentsMargins(8, 8, 8, 8)
        io_layout.setSpacing(8)

        self._io_view = QPlainTextEdit()
        self._io_view.setReadOnly(False)
        self._io_view.setPlaceholderText("WeiDU output and prompts will appear here...")
        self._output_buffer = ""
        self._capture_question = False
        self._question_lines_left = 0
        self._follow_output = True
        self._io_view.verticalScrollBar().valueChanged.connect(self._on_scroll_changed)
        self._input_buffer = ""
        self._io_view.installEventFilter(self)
        self._capture_warning = False

        io_layout.addWidget(self._io_view, 1)

        content_layout.addWidget(controls_box)
        lower_split = QSplitter(Qt.Orientation.Horizontal)
        lower_split.addWidget(io_box)
        content_layout.addWidget(lower_split, 1)
        self.body_layout.addWidget(content)

        button_row = QWidget()
        row_layout = QHBoxLayout(button_row)
        row_layout.setContentsMargins(0, 0, 0, 0)

        back_button = QPushButton("Back")
        back_button.clicked.connect(self._handle_back)
        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self._handle_exit)

        row_layout.addStretch(1)
        row_layout.addWidget(back_button)
        row_layout.addWidget(exit_button)
        self.footer_layout.addWidget(button_row)

    def _handle_back(self) -> None:
        if self._on_back is not None:
            self._on_back()

    def _handle_exit(self) -> None:
        self.window().close()

    def _on_cancel(self) -> None:
        self._view_model.cancel()

    def start_install(self, request: InstallRequest) -> None:
        self._io_view.clear()
        self._output_buffer = ""
        self._capture_question = False
        self._question_lines_left = 0
        self._capture_warning = False
        self._input_buffer = ""

        def _on_output(text: str) -> None:
            self.output.emit(text)

        def _on_exit(code: int) -> None:
            self.output.emit(f"\n[EXIT] code {code}\n")

        self._view_model.start(request, _on_output, _on_exit)

    def _append_output(self, text: str) -> None:
        scrollbar = self._io_view.verticalScrollBar()
        original_value = scrollbar.value()
        if self._minimal_checkbox.isChecked():
            text = self._filter_output(text)
            if not text:
                return
        doc = self._io_view.document()
        end_cursor = QTextCursor(doc)
        end_cursor.movePosition(QTextCursor.End)
        if self._input_buffer:
            end_cursor.movePosition(
                QTextCursor.Left, QTextCursor.MoveMode.KeepAnchor, len(self._input_buffer)
            )
            end_cursor.removeSelectedText()
        end_cursor.insertText(text)
        if self._input_buffer:
            end_cursor.insertText(self._input_buffer)
        if self._follow_output:
            scrollbar.setValue(scrollbar.maximum())
        else:
            scrollbar.setValue(original_value)

    def _filter_output(self, text: str) -> str:
        self._output_buffer += text
        lines = self._output_buffer.splitlines(keepends=True)
        if lines and not lines[-1].endswith(("\n", "\r")):
            self._output_buffer = lines.pop()
        else:
            self._output_buffer = ""

        kept: list[str] = []
        for line in lines:
            if "Question is" in line:
                self._capture_question = True
                kept.append(line)
                continue
            if self._capture_question:
                kept.append(line)
                continue
            if _is_warning_line(line):
                self._capture_warning = True
                kept.append(line)
                continue
            if self._capture_warning:
                if _is_timestamp_line(line):
                    self._capture_warning = False
                else:
                    kept.append(line)
                    continue
            if _should_keep_line(line):
                kept.append(line)
        return "".join(kept)

    def _on_scroll_changed(self, value: int) -> None:
        scrollbar = self._io_view.verticalScrollBar()
        self._follow_output = value >= scrollbar.maximum() - 2

    def eventFilter(self, watched, event):  # type: ignore[override]
        if watched is self._io_view and event.type() == event.Type.KeyPress:
            if (event.modifiers() & Qt.KeyboardModifier.ControlModifier) and (
                event.key() in (Qt.Key.Key_C, Qt.Key.Key_A, Qt.Key.Key_V)
            ):
                return False
            key = event.key()
            if key == Qt.Key.Key_Return or key == Qt.Key.Key_Enter:
                if self._input_buffer:
                    self._view_model.send_input(f"{self._input_buffer}\n")
                    self.output.emit(f"> {self._input_buffer}\n")
                    self._input_buffer = ""
                else:
                    self._view_model.send_input("\n")
                    self.output.emit(">\n")
                self._capture_question = False
                self._question_lines_left = 0
                return True
            if key == Qt.Key.Key_Backspace:
                if self._input_buffer:
                    self._input_buffer = self._input_buffer[:-1]
                    cursor = self._io_view.textCursor()
                    cursor.movePosition(QTextCursor.End)
                    cursor.movePosition(QTextCursor.Left, QTextCursor.MoveMode.KeepAnchor, 1)
                    cursor.removeSelectedText()
                return True
            text = event.text()
            if text:
                self._input_buffer += text
                cursor = self._io_view.textCursor()
                cursor.movePosition(QTextCursor.End)
                cursor.insertText(text)
                return True
        return super().eventFilter(watched, event)


def _should_keep_line(line: str) -> bool:
    if _is_dot_line(line):
        return False
    keywords = (
        "Beginning",
        "Installed mod",
        "User Input required",
        "Question is",
        "WARNING",
        "WARN",
        "ERROR",
        "[EXIT]",
    )
    return any(word in line for word in keywords)


def _is_warning_line(line: str) -> bool:
    return "WARNING" in line or "WARN" in line


def _is_timestamp_line(line: str) -> bool:
    return line.lstrip().startswith("[20")


def _is_weidu_dots(line: str) -> bool:
    if "mod_installer::weidu" not in line:
        return False
    tail = line.split("mod_installer::weidu]")[-1].strip()
    return tail and all(ch == "." for ch in tail)


def _is_dot_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    return all(ch == "." for ch in stripped)
