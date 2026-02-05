from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QSettings

from wlb.infra.fs.windows_version import detect_game_version
from wlb.ui.step1.setup_sections import SetupSections


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
    sections.logs_checkbox.toggled.connect(lambda value: settings.setValue("setup/has_logs", value))
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
    sections.logs_checkbox.setChecked(settings.value("setup/has_logs", False, type=bool))
    sections.debug_checkbox.setChecked(settings.value("setup/rust_log_debug", False, type=bool))
    sections.trace_checkbox.setChecked(settings.value("setup/rust_log_trace", False, type=bool))


def _set_game_path(settings: QSettings, path_key: str, version_key: str, value: str) -> None:
    settings.setValue(path_key, value)
    version = detect_game_version(Path(value)) if value else None
    if version:
        settings.setValue(version_key, version)
