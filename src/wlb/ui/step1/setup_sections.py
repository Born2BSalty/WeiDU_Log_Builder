from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtWidgets import QCheckBox, QComboBox, QGroupBox, QLabel

from wlb.ui.step1.setup_section_builders import (
    build_bg2ee_section,
    build_bgee_section,
    build_eet_section,
    build_game_section,
    build_mods_section,
    build_options_section,
    build_tools_section,
)
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
    bgee_box: QGroupBox
    bgee_log_folder_label: QLabel
    bgee_log_file_label: QLabel
    bg2ee_game_picker: PathPicker
    bg2ee_log_folder_picker: PathPicker
    bg2ee_log_file_picker: PathPicker
    bg2ee_box: QGroupBox
    bg2ee_log_folder_label: QLabel
    bg2ee_log_file_label: QLabel
    eet_bgee_game_picker: PathPicker
    eet_bgee_log_folder_picker: PathPicker
    eet_bgee_log_file_picker: PathPicker
    eet_bg2ee_game_picker: PathPicker
    eet_bg2ee_log_folder_picker: PathPicker
    eet_bg2ee_log_file_picker: PathPicker
    eet_box: QGroupBox
    eet_bgee_log_folder_label: QLabel
    eet_bgee_log_file_label: QLabel
    eet_bg2ee_log_folder_label: QLabel
    eet_bg2ee_log_file_label: QLabel
    options_box: QGroupBox
    logs_checkbox: QCheckBox
    debug_checkbox: QCheckBox
    trace_checkbox: QCheckBox


def build_setup_sections() -> SetupSections:
    game_select, game_box = build_game_section()
    mods_picker, mods_box = build_mods_section()
    weidu_picker, mod_installer_picker, tools_box = build_tools_section()
    (
        bgee_game_picker,
        bgee_log_folder_picker,
        bgee_log_file_picker,
        bgee_box,
        bgee_log_folder_label,
        bgee_log_file_label,
    ) = build_bgee_section()
    (
        bg2ee_game_picker,
        bg2ee_log_folder_picker,
        bg2ee_log_file_picker,
        bg2ee_box,
        bg2ee_log_folder_label,
        bg2ee_log_file_label,
    ) = build_bg2ee_section()
    (
        eet_bgee_game_picker,
        eet_bgee_log_folder_picker,
        eet_bgee_log_file_picker,
        eet_bg2ee_game_picker,
        eet_bg2ee_log_folder_picker,
        eet_bg2ee_log_file_picker,
        eet_box,
        eet_bgee_log_folder_label,
        eet_bgee_log_file_label,
        eet_bg2ee_log_folder_label,
        eet_bg2ee_log_file_label,
    ) = build_eet_section()
    options_box, logs_checkbox, debug_checkbox, trace_checkbox = build_options_section()

    return SetupSections(
        game_select=game_select,
        game_box=game_box,
        mods_picker=mods_picker,
        mods_box=mods_box,
        weidu_picker=weidu_picker,
        mod_installer_picker=mod_installer_picker,
        tools_box=tools_box,
        bgee_game_picker=bgee_game_picker,
        bgee_log_folder_picker=bgee_log_folder_picker,
        bgee_log_file_picker=bgee_log_file_picker,
        bgee_box=bgee_box,
        bgee_log_folder_label=bgee_log_folder_label,
        bgee_log_file_label=bgee_log_file_label,
        bg2ee_game_picker=bg2ee_game_picker,
        bg2ee_log_folder_picker=bg2ee_log_folder_picker,
        bg2ee_log_file_picker=bg2ee_log_file_picker,
        bg2ee_box=bg2ee_box,
        bg2ee_log_folder_label=bg2ee_log_folder_label,
        bg2ee_log_file_label=bg2ee_log_file_label,
        eet_bgee_game_picker=eet_bgee_game_picker,
        eet_bgee_log_folder_picker=eet_bgee_log_folder_picker,
        eet_bgee_log_file_picker=eet_bgee_log_file_picker,
        eet_bg2ee_game_picker=eet_bg2ee_game_picker,
        eet_bg2ee_log_folder_picker=eet_bg2ee_log_folder_picker,
        eet_bg2ee_log_file_picker=eet_bg2ee_log_file_picker,
        eet_box=eet_box,
        eet_bgee_log_folder_label=eet_bgee_log_folder_label,
        eet_bgee_log_file_label=eet_bgee_log_file_label,
        eet_bg2ee_log_folder_label=eet_bg2ee_log_folder_label,
        eet_bg2ee_log_file_label=eet_bg2ee_log_file_label,
        options_box=options_box,
        logs_checkbox=logs_checkbox,
        debug_checkbox=debug_checkbox,
        trace_checkbox=trace_checkbox,
    )


def set_log_mode(sections: SetupSections, use_file: bool) -> None:
    _set_log_rows(
        use_file,
        sections.bgee_log_folder_label,
        sections.bgee_log_folder_picker,
        sections.bgee_log_file_label,
        sections.bgee_log_file_picker,
    )
    _set_log_rows(
        use_file,
        sections.bg2ee_log_folder_label,
        sections.bg2ee_log_folder_picker,
        sections.bg2ee_log_file_label,
        sections.bg2ee_log_file_picker,
    )
    _set_log_rows(
        use_file,
        sections.eet_bgee_log_folder_label,
        sections.eet_bgee_log_folder_picker,
        sections.eet_bgee_log_file_label,
        sections.eet_bgee_log_file_picker,
    )
    _set_log_rows(
        use_file,
        sections.eet_bg2ee_log_folder_label,
        sections.eet_bg2ee_log_folder_picker,
        sections.eet_bg2ee_log_file_label,
        sections.eet_bg2ee_log_file_picker,
    )


def _set_log_rows(
    use_file: bool,
    folder_label: QLabel,
    folder_picker: PathPicker,
    file_label: QLabel,
    file_picker: PathPicker,
) -> None:
    folder_label.setVisible(not use_file)
    folder_picker.setVisible(not use_file)
    file_label.setVisible(use_file)
    file_picker.setVisible(use_file)
