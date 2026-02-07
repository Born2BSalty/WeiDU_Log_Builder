from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QSettings

from wlb.infra.fs.windows_version import detect_game_version
from wlb.ui.step1.views.section_types import SetupSections


def wire_settings(sections: SetupSections, settings: QSettings) -> None:
    sections.game_select.currentTextChanged.connect(
        lambda value: settings.setValue("setup/game", value)
    )
    sections.mods_picker.edit.textChanged.connect(
        lambda value: settings.setValue("setup/mods_folder", value)
    )
    sections.weidu_picker.edit.textChanged.connect(
        lambda value: settings.setValue("setup/weidu_path", value)
    )
    sections.mod_installer_picker.edit.textChanged.connect(
        lambda value: settings.setValue("setup/mod_installer_path", value)
    )
    sections.bgee_game_picker.edit.textChanged.connect(
        lambda value: _set_game_path(settings, "setup/bgee_game", "setup/bgee_game_version", value)
    )
    sections.bgee_log_folder_picker.edit.textChanged.connect(
        lambda value: settings.setValue("setup/bgee_log_folder", value)
    )
    sections.bgee_log_file_picker.edit.textChanged.connect(
        lambda value: settings.setValue("setup/bgee_log_file", value)
    )
    sections.bg2ee_game_picker.edit.textChanged.connect(
        lambda value: _set_game_path(
            settings, "setup/bg2ee_game", "setup/bg2ee_game_version", value
        )
    )
    sections.bg2ee_log_folder_picker.edit.textChanged.connect(
        lambda value: settings.setValue("setup/bg2ee_log_folder", value)
    )
    sections.bg2ee_log_file_picker.edit.textChanged.connect(
        lambda value: settings.setValue("setup/bg2ee_log_file", value)
    )
    sections.eet_bgee_game_picker.edit.textChanged.connect(
        lambda value: _set_game_path(
            settings, "setup/eet_bgee_game", "setup/bgee_game_version", value
        )
    )
    sections.eet_bgee_log_folder_picker.edit.textChanged.connect(
        lambda value: settings.setValue("setup/eet_bgee_log_folder", value)
    )
    sections.eet_bgee_log_file_picker.edit.textChanged.connect(
        lambda value: settings.setValue("setup/eet_bgee_log_file", value)
    )
    sections.eet_bg2ee_game_picker.edit.textChanged.connect(
        lambda value: _set_game_path(
            settings, "setup/eet_bg2ee_game", "setup/bg2ee_game_version", value
        )
    )
    sections.eet_bg2ee_log_folder_picker.edit.textChanged.connect(
        lambda value: settings.setValue("setup/eet_bg2ee_log_folder", value)
    )
    sections.eet_bg2ee_log_file_picker.edit.textChanged.connect(
        lambda value: settings.setValue("setup/eet_bg2ee_log_file", value)
    )
    sections.bgee_generate_picker.edit.textChanged.connect(
        lambda value: settings.setValue("setup/bgee_generate_dir", value)
    )
    sections.bg2ee_generate_picker.edit.textChanged.connect(
        lambda value: settings.setValue("setup/bg2ee_generate_dir", value)
    )
    sections.eet_pre_picker.edit.textChanged.connect(
        lambda value: settings.setValue("setup/eet_pre_dir", value)
    )
    sections.eet_new_picker.edit.textChanged.connect(
        lambda value: settings.setValue("setup/eet_new_dir", value)
    )
    sections.logs_checkbox.toggled.connect(lambda value: settings.setValue("setup/has_logs", value))
    sections.install_log_checkbox.toggled.connect(
        lambda value: settings.setValue("setup/log_install", value)
    )
    sections.pre_eet_checkbox.toggled.connect(
        lambda value: settings.setValue("setup/pre_eet_enabled", value)
    )
    sections.new_eet_checkbox.toggled.connect(
        lambda value: settings.setValue("setup/new_eet_enabled", value)
    )
    sections.generate_dir_checkbox.toggled.connect(
        lambda value: settings.setValue("setup/generate_enabled", value)
    )
    sections.custom_depth_checkbox.toggled.connect(
        lambda value: settings.setValue("setup/custom_depth_enabled", value)
    )
    sections.depth_input.valueChanged.connect(lambda value: settings.setValue("setup/depth", value))
    sections.skip_installed_checkbox.toggled.connect(
        lambda value: settings.setValue("setup/skip_installed", value)
    )
    sections.abort_warnings_checkbox.toggled.connect(
        lambda value: settings.setValue("setup/abort_warnings", value)
    )
    sections.timeout_checkbox.toggled.connect(
        lambda value: settings.setValue("setup/timeout_enabled", value)
    )
    sections.timeout_input.valueChanged.connect(
        lambda value: settings.setValue("setup/timeout", value)
    )
    sections.overwrite_checkbox.toggled.connect(
        lambda value: settings.setValue("setup/overwrite", value)
    )
    sections.strict_matching_checkbox.toggled.connect(
        lambda value: settings.setValue("setup/strict_matching", value)
    )
    sections.download_checkbox.toggled.connect(
        lambda value: settings.setValue("setup/download", value)
    )
    sections.per_component_checkbox.toggled.connect(
        lambda value: settings.setValue("setup/component_logs", value)
    )
    sections.component_logs_picker.edit.textChanged.connect(
        lambda value: settings.setValue("setup/component_logs_folder", value)
    )
    sections.tick_checkbox.toggled.connect(
        lambda value: settings.setValue("setup/tick_enabled", value)
    )
    sections.tick_input.valueChanged.connect(lambda value: settings.setValue("setup/tick", value))
    sections.debug_checkbox.toggled.connect(
        lambda value: settings.setValue("setup/rust_log_debug", value)
    )
    sections.trace_checkbox.toggled.connect(
        lambda value: settings.setValue("setup/rust_log_trace", value)
    )


def load_settings(sections: SetupSections, settings: QSettings) -> None:
    sections.game_select.setCurrentText(settings.value("setup/game", "BGEE"))
    sections.mods_picker.set_text(settings.value("setup/mods_folder", ""))
    sections.weidu_picker.set_text(settings.value("setup/weidu_path", ""))
    sections.mod_installer_picker.set_text(settings.value("setup/mod_installer_path", ""))
    sections.bgee_game_picker.set_text(settings.value("setup/bgee_game", ""))
    sections.bgee_log_folder_picker.set_text(settings.value("setup/bgee_log_folder", ""))
    sections.bgee_log_file_picker.set_text(settings.value("setup/bgee_log_file", ""))
    sections.bg2ee_game_picker.set_text(settings.value("setup/bg2ee_game", ""))
    sections.bg2ee_log_folder_picker.set_text(settings.value("setup/bg2ee_log_folder", ""))
    sections.bg2ee_log_file_picker.set_text(settings.value("setup/bg2ee_log_file", ""))
    sections.eet_bgee_game_picker.set_text(settings.value("setup/eet_bgee_game", ""))
    sections.eet_bgee_log_folder_picker.set_text(settings.value("setup/eet_bgee_log_folder", ""))
    sections.eet_bgee_log_file_picker.set_text(settings.value("setup/eet_bgee_log_file", ""))
    sections.eet_bg2ee_game_picker.set_text(settings.value("setup/eet_bg2ee_game", ""))
    sections.eet_bg2ee_log_folder_picker.set_text(settings.value("setup/eet_bg2ee_log_folder", ""))
    sections.eet_bg2ee_log_file_picker.set_text(settings.value("setup/eet_bg2ee_log_file", ""))
    sections.bgee_generate_picker.set_text(settings.value("setup/bgee_generate_dir", ""))
    sections.bg2ee_generate_picker.set_text(settings.value("setup/bg2ee_generate_dir", ""))
    sections.eet_pre_picker.set_text(settings.value("setup/eet_pre_dir", ""))
    sections.eet_new_picker.set_text(settings.value("setup/eet_new_dir", ""))
    sections.logs_checkbox.setChecked(settings.value("setup/has_logs", False, type=bool))
    sections.install_log_checkbox.setChecked(settings.value("setup/log_install", False, type=bool))
    sections.pre_eet_checkbox.setChecked(settings.value("setup/pre_eet_enabled", False, type=bool))
    sections.new_eet_checkbox.setChecked(settings.value("setup/new_eet_enabled", False, type=bool))
    sections.generate_dir_checkbox.setChecked(
        settings.value("setup/generate_enabled", False, type=bool)
    )
    sections.custom_depth_checkbox.setChecked(
        settings.value("setup/custom_depth_enabled", False, type=bool)
    )
    sections.depth_input.setValue(int(settings.value("setup/depth", 5)))
    sections.skip_installed_checkbox.setChecked(
        settings.value("setup/skip_installed", True, type=bool)
    )
    sections.abort_warnings_checkbox.setChecked(
        settings.value("setup/abort_warnings", False, type=bool)
    )
    sections.timeout_checkbox.setChecked(settings.value("setup/timeout_enabled", False, type=bool))
    sections.timeout_input.setValue(int(settings.value("setup/timeout", 3600)))
    sections.overwrite_checkbox.setChecked(settings.value("setup/overwrite", False, type=bool))
    sections.strict_matching_checkbox.setChecked(
        settings.value("setup/strict_matching", False, type=bool)
    )
    sections.download_checkbox.setChecked(settings.value("setup/download", False, type=bool))
    sections.per_component_checkbox.setChecked(
        settings.value("setup/component_logs", False, type=bool)
    )
    sections.component_logs_picker.set_text(settings.value("setup/component_logs_folder", ""))
    sections.tick_checkbox.setChecked(settings.value("setup/tick_enabled", False, type=bool))
    sections.tick_input.setValue(int(settings.value("setup/tick", 500)))
    sections.debug_checkbox.setChecked(settings.value("setup/rust_log_debug", False, type=bool))
    sections.trace_checkbox.setChecked(settings.value("setup/rust_log_trace", False, type=bool))


def _set_game_path(settings: QSettings, path_key: str, version_key: str, value: str) -> None:
    settings.setValue(path_key, value)
    version = detect_game_version(Path(value)) if value else None
    if version:
        settings.setValue(version_key, version)
