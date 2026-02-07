from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class FilterState:
    buffer: str = ""
    capture_question: bool = False
    capture_warning: bool = False

    def reset(self) -> None:
        self.buffer = ""
        self.capture_question = False
        self.capture_warning = False

    def reset_question(self) -> None:
        self.capture_question = False


def filter_output(state: FilterState, text: str) -> str:
    state.buffer += text
    lines = state.buffer.splitlines(keepends=True)
    if lines and not lines[-1].endswith(("\n", "\r")):
        state.buffer = lines.pop()
    else:
        state.buffer = ""

    kept: list[str] = []
    for line in lines:
        if "Question is" in line:
            state.capture_question = True
            kept.append(line)
            continue
        if state.capture_question:
            kept.append(line)
            continue
        if _is_warning_line(line):
            state.capture_warning = True
            kept.append(line)
            continue
        if state.capture_warning:
            if _is_timestamp_line(line):
                state.capture_warning = False
            else:
                kept.append(line)
                continue
        if _should_keep_line(line):
            kept.append(line)
    return "".join(kept)


_ANSI_RE = re.compile(r"(?:\x1b\[[0-?]*[ -/]*[@-~]|\x1b\][^\x07]*\x07|\x1b\][^\x1b]*\x1b\\)")


def strip_ansi(text: str) -> str:
    return _ANSI_RE.sub("", text)


def _should_keep_line(line: str) -> bool:
    if _is_dot_line(line):
        return False
    if _has_error_token(line):
        return True
    keywords = (
        "Beginning",
        "Installed mod",
        "User Input required",
        "Question is",
        "WARNING",
        "WARN",
        "[EXIT]",
    )
    return any(word in line for word in keywords)


_ERROR_TOKEN = re.compile(r"(^|\\s|\\]|:)ERROR(\\b|:)")  # avoid ERRORxx.WAV filenames


def _has_error_token(line: str) -> bool:
    return bool(_ERROR_TOKEN.search(line))


def _is_warning_line(line: str) -> bool:
    return "WARNING" in line or "WARN" in line


def _is_timestamp_line(line: str) -> bool:
    return line.lstrip().startswith("[20")


def _is_dot_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    return all(ch == "." for ch in stripped)
