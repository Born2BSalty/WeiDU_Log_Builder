from __future__ import annotations

from PySide6.QtWidgets import QCheckBox, QGridLayout, QGroupBox, QSpinBox


def build_flags_section(
    dev_mode: bool,
) -> tuple[
    QGroupBox,
    QCheckBox,
    QCheckBox,
    QCheckBox,
    QCheckBox,
    QSpinBox,
    QCheckBox,
    QCheckBox,
    QCheckBox,
    QSpinBox,
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

    custom_depth = QCheckBox("-d Custom scan depth")
    custom_depth.setToolTip(
        "How deep to scan mod folders for TP2s. Higher = slower, but finds mods buried in subfolders."
    )
    depth_input = QSpinBox()
    depth_input.setMinimum(1)
    depth_input.setMaximum(10)
    depth_input.setValue(5)
    depth_input.setEnabled(False)

    strict_matching = QCheckBox("-x Strict matching")
    strict_matching.setToolTip(
        "When comparing against weidu.log, it requires exact version + component + subcomponent match."
    )

    download = QCheckBox("--download Missing mods")
    download.setToolTip(
        "If a mod is missing, prompt for a URL and try to download it automatically."
    )

    overwrite = QCheckBox("-o Overwrite mod folder")
    overwrite.setToolTip(
        "Force‑copy the mod folder into the game directory even if a folder with that name already "
        "exists. Useful if a previous install left a partial folder."
    )

    timeout = QCheckBox("-t Timeout")
    timeout.setToolTip(
        "Maximum time per mod before the installer stops it. Default is 3600 (1 hour). "
        "Useful if a mod hangs."
    )
    timeout_input = QSpinBox()
    timeout_input.setMinimum(30)
    timeout_input.setMaximum(86400)
    timeout_input.setValue(3600)
    timeout_input.setEnabled(False)

    per_component = QCheckBox("-u Per‑component logs")
    per_component.setToolTip("Write one log file per component into the selected folder.")

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

    custom_depth.toggled.connect(depth_input.setEnabled)
    timeout.toggled.connect(timeout_input.setEnabled)
    tick.toggled.connect(tick_input.setEnabled)

    rows: list[tuple[QCheckBox, QSpinBox | None]] = [
        (pre_eet, None),
        (new_eet, None),
        (gen_dir, None),
        (skip_installed, None),
        (abort_warnings, None),
        (custom_depth, depth_input),
        (strict_matching, None),
        (download, None),
        (overwrite, None),
        (timeout, timeout_input),
        (per_component, None),
    ]
    if dev_mode:
        rows.append((tick, tick_input))

    row = 0
    col = 0
    for checkbox, extra in rows:
        grid.addWidget(checkbox, row, col)
        if extra is not None:
            grid.addWidget(extra, row, col + 1)
        if col == 0:
            col = 2
        else:
            col = 0
            row += 1

    grid.setColumnStretch(0, 1)
    grid.setColumnStretch(1, 0)
    grid.setColumnStretch(2, 1)
    grid.setColumnStretch(3, 0)

    return (
        box,
        pre_eet,
        new_eet,
        gen_dir,
        custom_depth,
        depth_input,
        skip_installed,
        abort_warnings,
        timeout,
        timeout_input,
        overwrite,
        strict_matching,
        download,
        per_component,
        tick,
        tick_input,
    )
