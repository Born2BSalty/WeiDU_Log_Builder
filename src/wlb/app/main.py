from __future__ import annotations

import sys
import traceback
from contextlib import suppress
from importlib import resources
from pathlib import Path
from threading import excepthook as thread_excepthook

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication

from wlb.ui.wizard_window import WizardWindow


def _load_styles(app: QApplication) -> None:
    try:
        qss_text = resources.files("wlb.ui.style").joinpath("app.qss").read_text(encoding="utf-8")
    except OSError:
        return
    app.setStyleSheet(qss_text)


def main() -> None:
    _install_crash_handlers()
    QCoreApplication.setOrganizationName("WLB")
    QCoreApplication.setApplicationName("WeiDU Wizard")
    app = QApplication(sys.argv)
    _load_styles(app)
    window = WizardWindow()
    window.show()
    app.exec()


def _install_crash_handlers() -> None:
    def _handle_exception(exc_type, exc, tb) -> None:
        _write_crash_log(exc_type, exc, tb)
        sys.__excepthook__(exc_type, exc, tb)

    def _handle_thread_exception(args) -> None:
        _write_crash_log(args.exc_type, args.exc_value, args.exc_traceback)
        thread_excepthook(args)

    sys.excepthook = _handle_exception
    with suppress(Exception):
        import threading

        threading.excepthook = _handle_thread_exception


def _crash_log_path() -> Path:
    return Path.cwd() / "crash.log"


def _write_crash_log(exc_type, exc, tb) -> None:
    log_path = _crash_log_path()
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(_format_crash(exc_type, exc, tb), encoding="utf-8")


def _format_crash(exc_type, exc, tb) -> str:
    lines = [
        "WeiDU Wizard crash log",
        "",
        "Traceback:",
        "".join(traceback.format_exception(exc_type, exc, tb)).strip(),
        "",
    ]
    return "\n".join(lines)
