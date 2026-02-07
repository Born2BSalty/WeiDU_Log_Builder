from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtWidgets import QCheckBox, QComboBox, QGroupBox, QLabel, QSpinBox

from wlb.ui.widgets.path_picker import PathPicker


@dataclass
class SetupSections:
    game_select: QComboBox
    game_box: QGroupBox
    mods_picker: PathPicker
    mods_box: QGroupBox
    weidu_picker: PathPicker
    mod_installer_picker: PathPicker
    tools_box: QGroupBox
    bgee_game_picker: PathPicker
    bgee_log_folder_picker: PathPicker
    bgee_log_file_picker: PathPicker
    bgee_generate_picker: PathPicker
    bgee_box: QGroupBox
    bgee_log_folder_label: QLabel
    bgee_log_file_label: QLabel
    bgee_generate_label: QLabel
    bgee_generate_summary: QLabel
    bg2ee_game_picker: PathPicker
    bg2ee_log_folder_picker: PathPicker
    bg2ee_log_file_picker: PathPicker
    bg2ee_generate_picker: PathPicker
    bg2ee_box: QGroupBox
    bg2ee_log_folder_label: QLabel
    bg2ee_log_file_label: QLabel
    bg2ee_generate_label: QLabel
    bg2ee_generate_summary: QLabel
    eet_bgee_game_picker: PathPicker
    eet_bgee_log_folder_picker: PathPicker
    eet_bgee_log_file_picker: PathPicker
    eet_bg2ee_game_picker: PathPicker
    eet_bg2ee_log_folder_picker: PathPicker
    eet_bg2ee_log_file_picker: PathPicker
    eet_pre_picker: PathPicker
    eet_new_picker: PathPicker
    eet_box: QGroupBox
    eet_bgee_log_folder_label: QLabel
    eet_bgee_log_file_label: QLabel
    eet_bg2ee_log_folder_label: QLabel
    eet_bg2ee_log_file_label: QLabel
    eet_pre_label: QLabel
    eet_new_label: QLabel
    eet_pre_summary: QLabel
    eet_new_summary: QLabel
    options_box: QGroupBox
    logs_checkbox: QCheckBox
    install_log_checkbox: QCheckBox
    debug_checkbox: QCheckBox
    trace_checkbox: QCheckBox
    component_logs_box: QGroupBox
    component_logs_picker: PathPicker
    component_logs_note: QLabel
    flags_box: QGroupBox
    pre_eet_checkbox: QCheckBox
    new_eet_checkbox: QCheckBox
    generate_dir_checkbox: QCheckBox
    custom_depth_checkbox: QCheckBox
    depth_input: QSpinBox
    skip_installed_checkbox: QCheckBox
    abort_warnings_checkbox: QCheckBox
    timeout_checkbox: QCheckBox
    timeout_input: QSpinBox
    overwrite_checkbox: QCheckBox
    strict_matching_checkbox: QCheckBox
    download_checkbox: QCheckBox
    per_component_checkbox: QCheckBox
    tick_checkbox: QCheckBox
    tick_input: QSpinBox
