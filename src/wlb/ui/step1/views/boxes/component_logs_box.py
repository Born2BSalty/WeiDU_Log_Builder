from __future__ import annotations

from PySide6.QtWidgets import QCheckBox, QFormLayout, QGroupBox, QLabel

from wlb.ui.widgets.path_picker import PathPicker


def build_component_logs_section() -> tuple[
    QGroupBox,
    QCheckBox,
    QCheckBox,
    QCheckBox,
    QCheckBox,
    QLabel,
    PathPicker,
    QLabel,
]:
    box = QGroupBox("WeiDU Log Mode")
    form = QFormLayout(box)
    autolog = QCheckBox("autolog")
    autolog.setToolTip("Use WeiDU's autolog mode.")
    autolog.setChecked(True)
    logapp = QCheckBox("logapp")
    logapp.setToolTip("Append to existing WeiDU log instead of overwriting.")
    logapp.setChecked(True)
    logextern = QCheckBox("log-extern")
    logextern.setToolTip("Log output from external commands.")
    logextern.setChecked(True)
    log = QCheckBox("log (per‑component)")
    log.setToolTip("Write one log file per component into the selected folder.")
    picker = PathPicker(picker="dir")
    picker.setVisible(False)
    form.addRow("", autolog)
    form.addRow("", logapp)
    form.addRow("", logextern)
    form.addRow("", log)
    per_component_label = QLabel("Per‑component folder:")
    per_component_label.setVisible(False)
    form.addRow(per_component_label, picker)
    note = QLabel("")
    note.setVisible(False)
    form.addRow("", note)
    box.setVisible(False)
    return box, autolog, logapp, logextern, log, per_component_label, picker, note
