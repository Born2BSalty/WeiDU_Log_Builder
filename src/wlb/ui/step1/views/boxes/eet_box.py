from __future__ import annotations

from PySide6.QtWidgets import QFormLayout, QGroupBox, QLabel

from wlb.ui.widgets.path_picker import PathPicker


def build_eet_section() -> tuple[
    PathPicker,
    PathPicker,
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
    pre_eet_dir = PathPicker(picker="dir")
    new_eet_dir = PathPicker(picker="dir")
    bgee_game_label = QLabel("BGEE Game Folder:")
    bgee_log_folder_label = QLabel("BGEE WeiDU Log Folder:")
    bgee_log_file_label = QLabel("BGEE WeiDU Fog File:")
    bg2ee_game_label = QLabel("BG2EE Game Folder:")
    bg2ee_log_folder_label = QLabel("BG2EE WeiDU Log Folder:")
    bg2ee_log_file_label = QLabel("BG2EE WeiDU Log File:")
    pre_eet_label = QLabel("New Pre‑EET Directory (-p):")
    new_eet_label = QLabel("New EET Directory (-n):")
    pre_eet_summary = QLabel("BGEE stage: installs into a fresh BGEE copy at the selected folder.")
    new_eet_summary = QLabel(
        "EET stage: installs into a fresh BG2EE/EET copy at the selected folder."
    )
    bgee_log_file_label.setVisible(False)
    bgee_log_file.setVisible(False)
    bg2ee_log_file_label.setVisible(False)
    bg2ee_log_file.setVisible(False)
    pre_eet_label.setVisible(False)
    pre_eet_dir.setVisible(False)
    new_eet_label.setVisible(False)
    new_eet_dir.setVisible(False)
    pre_eet_summary.setVisible(False)
    new_eet_summary.setVisible(False)
    form.addRow(bgee_game_label, bgee_game)
    form.addRow(bgee_log_folder_label, bgee_log_folder)
    form.addRow(bgee_log_file_label, bgee_log_file)
    form.addRow(bg2ee_game_label, bg2ee_game)
    form.addRow(bg2ee_log_folder_label, bg2ee_log_folder)
    form.addRow(bg2ee_log_file_label, bg2ee_log_file)
    form.addRow(pre_eet_label, pre_eet_dir)
    form.addRow("", pre_eet_summary)
    form.addRow(new_eet_label, new_eet_dir)
    form.addRow("", new_eet_summary)
    return (
        bgee_game,
        bgee_log_folder,
        bgee_log_file,
        bg2ee_game,
        bg2ee_log_folder,
        bg2ee_log_file,
        pre_eet_dir,
        new_eet_dir,
        box,
        bgee_log_folder_label,
        bgee_log_file_label,
        bg2ee_log_folder_label,
        bg2ee_log_file_label,
        pre_eet_label,
        new_eet_label,
        pre_eet_summary,
        new_eet_summary,
    )
