from __future__ import annotations

from PySide6.QtWidgets import QCheckBox, QGridLayout, QGroupBox, QHBoxLayout, QSpinBox, QWidget


def build_flags_section(
    dev_mode: bool,
) -> tuple[
    QGroupBox,
    QCheckBox,
    QCheckBox,
    QCheckBox,
    QCheckBox,
    QCheckBox,
    QCheckBox,
    QCheckBox,
    QCheckBox,
    QCheckBox,
    QCheckBox,
    QSpinBox,
]:
    box = QGroupBox("Flags")
    grid = QGridLayout(box)

    pre_eet = QCheckBox("-p New pre‑EET directory")
    pre_eet.setToolTip(
        "Creates a fresh pre‑EET game directory by copying the BGEE game there before "
        "installing (used for a clean pre‑EET stage)."
    )
    new_eet = QCheckBox("-n New EET directory")
    new_eet.setToolTip(
        "Creates a fresh EET game directory by copying the BG2EE game there before installing."
    )
    gen_dir = QCheckBox("-g Generate directory")
    gen_dir.setToolTip(
        "Generic make a new directory, copy the original game into it, then install there."
    )
    skip_installed = QCheckBox("-s Skip installed")
    skip_installed.setToolTip("Uses existing weidu.log to skip components already installed.")
    skip_installed.setChecked(True)
    abort_warnings = QCheckBox("-a Abort on warnings")
    abort_warnings.setToolTip("If WeiDU prints warnings, abort the whole install immediately.")

    weidu_log_mode = QCheckBox("-u WeiDU log mode")
    weidu_log_mode.setToolTip("Choose the WeiDU log flags and optional per-component logs.")

    strict_matching = QCheckBox("-x Strict matching")
    strict_matching.setToolTip(
        "When comparing against weidu.log, it requires exact version + component + subcomponent match."
    )

    download = QCheckBox("--download Missing mods")
    download.setToolTip(
        "If a mod is missing, prompt for a URL and try to download it automatically."
    )
    download.setChecked(True)

    overwrite = QCheckBox("-o Overwrite mod folder")
    overwrite.setToolTip(
        "Force‑copy the mod folder into the game directory even if a folder with that name already "
        "exists. Useful if a previous install left a partial folder."
    )

    tick = QCheckBox("-i Tick (dev)")
    tick.setToolTip(
        "Polling interval in milliseconds for installer output. Lower = more responsive, "
        "higher = less CPU. Default 500."
    )
    tick_input = QSpinBox()
    tick_input.setMinimum(50)
    tick_input.setMaximum(5000)
    tick_input.setValue(500)
    tick_input.setEnabled(False)

    pre_eet.setVisible(False)
    new_eet.setVisible(False)
    gen_dir.setVisible(False)
    tick.setVisible(dev_mode)
    tick_input.setVisible(dev_mode)

    tick.toggled.connect(tick_input.setEnabled)

    rows: list[QWidget] = [
        weidu_log_mode,
        skip_installed,
        pre_eet,
        abort_warnings,
        strict_matching,
        new_eet,
        download,
        overwrite,
        gen_dir,
    ]
    if dev_mode:
        rows.append(_with_spinbox(tick, tick_input))

    columns = 3
    for idx, widget in enumerate(rows):
        row = idx // columns
        col = idx % columns
        grid.addWidget(widget, row, col)

    for col in range(columns):
        grid.setColumnStretch(col, 1)

    return (
        box,
        pre_eet,
        new_eet,
        gen_dir,
        skip_installed,
        abort_warnings,
        weidu_log_mode,
        overwrite,
        strict_matching,
        download,
        tick,
        tick_input,
    )


def _with_spinbox(checkbox: QCheckBox, spinbox: QSpinBox) -> QWidget:
    wrapper = QWidget()
    layout = QHBoxLayout(wrapper)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(checkbox)
    layout.addWidget(spinbox)
    layout.addStretch(1)
    return wrapper
