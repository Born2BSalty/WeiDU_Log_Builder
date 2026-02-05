from __future__ import annotations

from PySide6.QtWidgets import QCheckBox, QComboBox, QFormLayout, QGroupBox, QLabel

from wlb.ui.widgets.path_picker import PathPicker


def build_game_section() -> tuple[QComboBox, QGroupBox]:
    box = QGroupBox("Game Selection")
    form = QFormLayout(box)
    game = QComboBox()
    game.addItems(["BGEE", "BG2EE", "EET"])
    form.addRow("Game Install:", game)
    return game, box


def build_mods_section() -> tuple[PathPicker, QGroupBox]:
    box = QGroupBox("Mods Folder")
    form = QFormLayout(box)
    picker = PathPicker(picker="dir")
    form.addRow("Your Mods Folder:", picker)
    return picker, box


def build_tools_section() -> tuple[PathPicker, PathPicker, QGroupBox]:
    box = QGroupBox("Tools")
    form = QFormLayout(box)
    weidu = PathPicker(picker="file")
    installer = PathPicker(picker="file")
    form.addRow("WeiDU.exe:", weidu)
    form.addRow("Mod_Installer.exe:", installer)
    return weidu, installer, box


def build_bgee_section() -> tuple[PathPicker, PathPicker, PathPicker, QGroupBox, QLabel, QLabel]:
    box = QGroupBox("BGEE Install Paths")
    form = QFormLayout(box)
    game = PathPicker(picker="dir")
    log_folder = PathPicker(picker="dir")
    log_file = PathPicker(picker="file")
    game_label = QLabel("BGEE Game Folder:")
    log_folder_label = QLabel("BGEE WeiDU Log Folder:")
    log_file_label = QLabel("BGEE WeiDU Log File:")
    log_file_label.setVisible(False)
    log_file.setVisible(False)
    form.addRow(game_label, game)
    form.addRow(log_folder_label, log_folder)
    form.addRow(log_file_label, log_file)
    return game, log_folder, log_file, box, log_folder_label, log_file_label


def build_bg2ee_section() -> tuple[PathPicker, PathPicker, PathPicker, QGroupBox, QLabel, QLabel]:
    box = QGroupBox("BG2EE Install Paths")
    form = QFormLayout(box)
    game = PathPicker(picker="dir")
    log_folder = PathPicker(picker="dir")
    log_file = PathPicker(picker="file")
    game_label = QLabel("BG2EE Game Folder:")
    log_folder_label = QLabel("BG2EE WeiDU Log Folder:")
    log_file_label = QLabel("BG2EE WeiDU Log File:")
    log_file_label.setVisible(False)
    log_file.setVisible(False)
    form.addRow(game_label, game)
    form.addRow(log_folder_label, log_folder)
    form.addRow(log_file_label, log_file)
    return game, log_folder, log_file, box, log_folder_label, log_file_label


def build_eet_section() -> tuple[
    PathPicker,
    PathPicker,
    PathPicker,
    PathPicker,
    PathPicker,
    PathPicker,
    QGroupBox,
    QLabel,
    QLabel,
    QLabel,
    QLabel,
]:
    box = QGroupBox("EET Install Paths")
    form = QFormLayout(box)
    bgee_game = PathPicker(picker="dir")
    bgee_log_folder = PathPicker(picker="dir")
    bgee_log_file = PathPicker(picker="file")
    bg2ee_game = PathPicker(picker="dir")
    bg2ee_log_folder = PathPicker(picker="dir")
    bg2ee_log_file = PathPicker(picker="file")
    bgee_game_label = QLabel("BGEE Game Folder:")
    bgee_log_folder_label = QLabel("BGEE WeiDU Log Folder:")
    bgee_log_file_label = QLabel("BGEE WeiDU Fog File:")
    bg2ee_game_label = QLabel("BG2EE Game Folder:")
    bg2ee_log_folder_label = QLabel("BG2EE WeiDU Log Folder:")
    bg2ee_log_file_label = QLabel("BG2EE WeiDU Log File:")
    bgee_log_file_label.setVisible(False)
    bgee_log_file.setVisible(False)
    bg2ee_log_file_label.setVisible(False)
    bg2ee_log_file.setVisible(False)
    form.addRow(bgee_game_label, bgee_game)
    form.addRow(bgee_log_folder_label, bgee_log_folder)
    form.addRow(bgee_log_file_label, bgee_log_file)
    form.addRow(bg2ee_game_label, bg2ee_game)
    form.addRow(bg2ee_log_folder_label, bg2ee_log_folder)
    form.addRow(bg2ee_log_file_label, bg2ee_log_file)
    return (
        bgee_game,
        bgee_log_folder,
        bgee_log_file,
        bg2ee_game,
        bg2ee_log_folder,
        bg2ee_log_file,
        box,
        bgee_log_folder_label,
        bgee_log_file_label,
        bg2ee_log_folder_label,
        bg2ee_log_file_label,
    )


def build_options_section() -> tuple[QGroupBox, QCheckBox, QCheckBox, QCheckBox]:
    box = QGroupBox("Options")
    form = QFormLayout(box)

    logs = QCheckBox("Have WeiDU Logs?")
    logs.setToolTip("If checked, the wizard will read existing WeiDU logs for detection.")
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
    form.addRow("", debug)
    form.addRow("", trace)
    return box, logs, debug, trace
