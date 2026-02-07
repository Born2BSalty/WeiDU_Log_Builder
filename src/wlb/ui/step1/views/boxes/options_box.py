from __future__ import annotations

from PySide6.QtWidgets import QCheckBox, QFormLayout, QGroupBox


def build_options_section() -> tuple[QGroupBox, QCheckBox, QCheckBox, QCheckBox, QCheckBox]:
    box = QGroupBox("Options")
    form = QFormLayout(box)

    logs = QCheckBox("Have WeiDU Logs?")
    logs.setToolTip("If checked, the wizard will read existing WeiDU logs for detection.")
    install_log = QCheckBox("Log Install?")
    install_log.setToolTip("Write installer output to a text file next to the app.")
    debug = QCheckBox("Set RUST_LOG=DEBUG")
    debug.setToolTip(
        "If installs fail or throw errors, enable this and share WSETUP.DEBUG with the mod author."
    )
    trace = QCheckBox("Set RUST_LOG=TRACE")
    trace.setToolTip(
        "Very verbose logging. Use this if DEBUG is not enough, and share "
        "WSETUP.DEBUG with the mod author."
    )

    form.addRow("", logs)
    form.addRow("", install_log)
    form.addRow("", debug)
    form.addRow("", trace)
    return box, logs, install_log, debug, trace
