from __future__ import annotations

import os

from PySide6.QtWidgets import QLabel

from wlb.ui.step1.views.section_builders import (
    build_bg2ee_section,
    build_bgee_section,
    build_component_logs_section,
    build_eet_section,
    build_flags_section,
    build_game_section,
    build_mods_section,
    build_options_section,
    build_tools_section,
)
from wlb.ui.step1.views.section_types import SetupSections
from wlb.ui.widgets.path_picker import PathPicker


def build_setup_sections() -> SetupSections:
    game_select, game_box = build_game_section()
    mods_picker, mods_box = build_mods_section()
    weidu_picker, mod_installer_picker, tools_box = build_tools_section()
    (
        bgee_game_picker,
        bgee_log_folder_picker,
        bgee_log_file_picker,
        bgee_generate_picker,
        bgee_box,
        bgee_log_folder_label,
        bgee_log_file_label,
        bgee_generate_label,
        bgee_generate_summary,
    ) = build_bgee_section()
    (
        bg2ee_game_picker,
        bg2ee_log_folder_picker,
        bg2ee_log_file_picker,
        bg2ee_generate_picker,
        bg2ee_box,
        bg2ee_log_folder_label,
        bg2ee_log_file_label,
        bg2ee_generate_label,
        bg2ee_generate_summary,
    ) = build_bg2ee_section()
    (
        eet_bgee_game_picker,
        eet_bgee_log_folder_picker,
        eet_bgee_log_file_picker,
        eet_bg2ee_game_picker,
        eet_bg2ee_log_folder_picker,
        eet_bg2ee_log_file_picker,
        eet_pre_picker,
        eet_new_picker,
        eet_box,
        eet_bgee_log_folder_label,
        eet_bgee_log_file_label,
        eet_bg2ee_log_folder_label,
        eet_bg2ee_log_file_label,
        eet_pre_label,
        eet_new_label,
        eet_pre_summary,
        eet_new_summary,
    ) = build_eet_section()
    (
        options_box,
        logs_checkbox,
        install_log_checkbox,
        debug_checkbox,
        trace_checkbox,
        custom_depth_checkbox,
        depth_input,
        timeout_checkbox,
        timeout_input,
    ) = build_options_section()
    (
        component_logs_box,
        weidu_log_autolog_checkbox,
        weidu_log_logapp_checkbox,
        weidu_log_logextern_checkbox,
        weidu_log_log_checkbox,
        weidu_log_label,
        weidu_log_picker,
        component_logs_note,
    ) = build_component_logs_section()
    dev_mode = os.getenv("WLB_DEV", "") == "1"
    (
        flags_box,
        pre_eet_checkbox,
        new_eet_checkbox,
        generate_dir_checkbox,
        skip_installed_checkbox,
        abort_warnings_checkbox,
        weidu_log_mode_checkbox,
        overwrite_checkbox,
        strict_matching_checkbox,
        download_checkbox,
        tick_checkbox,
        tick_input,
    ) = build_flags_section(dev_mode)

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
        bgee_generate_picker=bgee_generate_picker,
        bgee_box=bgee_box,
        bgee_log_folder_label=bgee_log_folder_label,
        bgee_log_file_label=bgee_log_file_label,
        bgee_generate_label=bgee_generate_label,
        bgee_generate_summary=bgee_generate_summary,
        bg2ee_game_picker=bg2ee_game_picker,
        bg2ee_log_folder_picker=bg2ee_log_folder_picker,
        bg2ee_log_file_picker=bg2ee_log_file_picker,
        bg2ee_generate_picker=bg2ee_generate_picker,
        bg2ee_box=bg2ee_box,
        bg2ee_log_folder_label=bg2ee_log_folder_label,
        bg2ee_log_file_label=bg2ee_log_file_label,
        bg2ee_generate_label=bg2ee_generate_label,
        bg2ee_generate_summary=bg2ee_generate_summary,
        eet_bgee_game_picker=eet_bgee_game_picker,
        eet_bgee_log_folder_picker=eet_bgee_log_folder_picker,
        eet_bgee_log_file_picker=eet_bgee_log_file_picker,
        eet_bg2ee_game_picker=eet_bg2ee_game_picker,
        eet_bg2ee_log_folder_picker=eet_bg2ee_log_folder_picker,
        eet_bg2ee_log_file_picker=eet_bg2ee_log_file_picker,
        eet_pre_picker=eet_pre_picker,
        eet_new_picker=eet_new_picker,
        eet_box=eet_box,
        eet_bgee_log_folder_label=eet_bgee_log_folder_label,
        eet_bgee_log_file_label=eet_bgee_log_file_label,
        eet_bg2ee_log_folder_label=eet_bg2ee_log_folder_label,
        eet_bg2ee_log_file_label=eet_bg2ee_log_file_label,
        eet_pre_label=eet_pre_label,
        eet_new_label=eet_new_label,
        eet_pre_summary=eet_pre_summary,
        eet_new_summary=eet_new_summary,
        options_box=options_box,
        logs_checkbox=logs_checkbox,
        install_log_checkbox=install_log_checkbox,
        debug_checkbox=debug_checkbox,
        trace_checkbox=trace_checkbox,
        custom_depth_checkbox=custom_depth_checkbox,
        depth_input=depth_input,
        timeout_checkbox=timeout_checkbox,
        timeout_input=timeout_input,
        component_logs_box=component_logs_box,
        weidu_log_autolog_checkbox=weidu_log_autolog_checkbox,
        weidu_log_logapp_checkbox=weidu_log_logapp_checkbox,
        weidu_log_logextern_checkbox=weidu_log_logextern_checkbox,
        weidu_log_log_checkbox=weidu_log_log_checkbox,
        weidu_log_label=weidu_log_label,
        weidu_log_picker=weidu_log_picker,
        component_logs_note=component_logs_note,
        flags_box=flags_box,
        pre_eet_checkbox=pre_eet_checkbox,
        new_eet_checkbox=new_eet_checkbox,
        generate_dir_checkbox=generate_dir_checkbox,
        skip_installed_checkbox=skip_installed_checkbox,
        abort_warnings_checkbox=abort_warnings_checkbox,
        weidu_log_mode_checkbox=weidu_log_mode_checkbox,
        overwrite_checkbox=overwrite_checkbox,
        strict_matching_checkbox=strict_matching_checkbox,
        download_checkbox=download_checkbox,
        tick_checkbox=tick_checkbox,
        tick_input=tick_input,
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
