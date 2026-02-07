from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QPlainTextEdit


@dataclass
class OutputViewState:
    def reset(self) -> None:
        return None


def append_output(
    view: QPlainTextEdit, state: OutputViewState, input_buffer: str, text: str
) -> None:
    _ = state
    doc = view.document()
    end_cursor = QTextCursor(doc)
    end_cursor.movePosition(QTextCursor.End)
    if input_buffer:
        end_cursor.movePosition(
            QTextCursor.Left, QTextCursor.MoveMode.KeepAnchor, len(input_buffer)
        )
        end_cursor.removeSelectedText()
    end_cursor.insertText(text)
    if input_buffer:
        end_cursor.insertText(input_buffer)
