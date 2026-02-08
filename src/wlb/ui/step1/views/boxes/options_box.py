from __future__ import annotations

from PySide6.QtWidgets import (
    QCheckBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QSpinBox,
    QWidget,
)


def build_options_section() -> tuple[
    QGroupBox,
    QCheckBox,
    QCheckBox,
    QCheckBox,
    QCheckBox,
    QCheckBox,
    QSpinBox,
    QCheckBox,
    QSpinBox,
]:
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

    custom_depth = QCheckBox("Custom scan depth")
    custom_depth.setToolTip(
        "How deep to scan mod folders for TP2s. Higher = slower, but finds mods buried in subfolders."
    )
    depth_input = QSpinBox()
    depth_input.setMinimum(1)
    depth_input.setMaximum(10)
    depth_input.setValue(5)
    depth_input.setEnabled(False)
    custom_depth.toggled.connect(depth_input.setEnabled)
    depth_row = _with_spinbox(custom_depth, depth_input)

    timeout = QCheckBox("Timeout per mod")
    timeout.setToolTip(
        "Maximum time per mod before the installer stops it. Default is 3600 (1 hour). "
        "Useful if a mod hangs."
    )
    timeout_input = QSpinBox()
    timeout_input.setMinimum(30)
    timeout_input.setMaximum(86400)
    timeout_input.setValue(3600)
    timeout_input.setEnabled(False)
    timeout.toggled.connect(timeout_input.setEnabled)
    timeout_row = _with_spinbox(timeout, timeout_input)

    form.addRow("", logs)
    form.addRow("", install_log)
    form.addRow("", debug)
    form.addRow("", trace)
    form.addRow("", depth_row)
    form.addRow("", timeout_row)
    return (
        box,
        logs,
        install_log,
        debug,
        trace,
        custom_depth,
        depth_input,
        timeout,
        timeout_input,
    )


def _with_spinbox(checkbox: QCheckBox, spinbox: QSpinBox) -> QWidget:
    wrapper = QWidget()
    layout = QHBoxLayout(wrapper)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(checkbox)
    layout.addWidget(spinbox)
    layout.addStretch(1)
    return wrapper
