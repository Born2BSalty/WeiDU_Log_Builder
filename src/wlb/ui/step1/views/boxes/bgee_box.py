from __future__ import annotations

from PySide6.QtWidgets import QFormLayout, QGroupBox, QLabel

from wlb.ui.widgets.path_picker import PathPicker


def build_bgee_section() -> tuple[
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
    box = QGroupBox("BGEE Install Paths")
    form = QFormLayout(box)
    game = PathPicker(picker="dir")
    log_folder = PathPicker(picker="dir")
    log_file = PathPicker(picker="file")
    generate_dir = PathPicker(picker="dir")
    game_label = QLabel("BGEE Game Folder:")
    log_folder_label = QLabel("BGEE WeiDU Log Folder:")
    log_file_label = QLabel("BGEE WeiDU Log File:")
    generate_label = QLabel("Generate Directory (-g):")
    generate_summary = QLabel("Installs into a fresh copy at the selected folder.")
    log_file_label.setVisible(False)
    log_file.setVisible(False)
    generate_label.setVisible(False)
    generate_dir.setVisible(False)
    generate_summary.setVisible(False)
    form.addRow(game_label, game)
    form.addRow(log_folder_label, log_folder)
    form.addRow(log_file_label, log_file)
    form.addRow(generate_label, generate_dir)
    form.addRow("", generate_summary)
    return (
        game,
        log_folder,
        log_file,
        generate_dir,
        box,
        log_folder_label,
        log_file_label,
        generate_label,
        generate_summary,
    )
