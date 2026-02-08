from __future__ import annotations

from typing import Any

from PySide6.QtCore import QSettings


class SettingsService:
    def __init__(self, settings: QSettings | None = None) -> None:
        self._settings = settings or QSettings()

    def _int_value(self, key: str, default: int) -> int:
        value: Any = self._settings.value(key, default)
        if isinstance(value, int):
            return value
        if isinstance(value, float):
            return int(value)
        if isinstance(value, str):
            try:
                return int(value)
            except ValueError:
                return default
        return default

    def game(self) -> str:
        return str(self._settings.value("setup/game", "BGEE"))

    def has_logs(self) -> bool:
        return bool(self._settings.value("setup/has_logs", False, type=bool))

    def log_install(self) -> bool:
        return bool(self._settings.value("setup/log_install", False, type=bool))

    def mods_folder(self) -> str:
        return str(self._settings.value("setup/mods_folder", ""))

    def weidu_path(self) -> str:
        return str(self._settings.value("setup/weidu_path", ""))

    def mod_installer_path(self) -> str:
        return str(self._settings.value("setup/mod_installer_path", ""))

    def bgee_game_version(self) -> str | None:
        value = self._settings.value("setup/bgee_game_version", "")
        text = str(value).strip()
        return text or None

    def bg2ee_game_version(self) -> str | None:
        value = self._settings.value("setup/bg2ee_game_version", "")
        text = str(value).strip()
        return text or None

    def game_version_for(self, game: str) -> str | None:
        if game == "BGEE":
            return self.bgee_game_version()
        if game == "BG2EE":
            return self.bg2ee_game_version()
        if game == "EET":
            return self.bgee_game_version()
        return None

    def rust_log_debug(self) -> bool:
        return bool(self._settings.value("setup/rust_log_debug", False, type=bool))

    def rust_log_trace(self) -> bool:
        return bool(self._settings.value("setup/rust_log_trace", False, type=bool))

    def weidu_log_mode_enabled(self) -> bool:
        return bool(self._settings.value("setup/weidu_log_mode_enabled", False, type=bool))

    def weidu_log_autolog(self) -> bool:
        return bool(self._settings.value("setup/weidu_log_autolog", True, type=bool))

    def weidu_log_logapp(self) -> bool:
        return bool(self._settings.value("setup/weidu_log_logapp", True, type=bool))

    def weidu_log_logextern(self) -> bool:
        return bool(self._settings.value("setup/weidu_log_logextern", True, type=bool))

    def weidu_log_log(self) -> bool:
        return bool(self._settings.value("setup/weidu_log_log", False, type=bool))

    def weidu_log_folder(self) -> str:
        return str(self._settings.value("setup/weidu_log_folder", ""))

    def pre_eet_enabled(self) -> bool:
        return bool(self._settings.value("setup/pre_eet_enabled", False, type=bool))

    def new_eet_enabled(self) -> bool:
        return bool(self._settings.value("setup/new_eet_enabled", False, type=bool))

    def generate_dir_enabled(self) -> bool:
        return bool(self._settings.value("setup/generate_enabled", False, type=bool))

    def custom_depth_enabled(self) -> bool:
        return bool(self._settings.value("setup/custom_depth_enabled", False, type=bool))

    def depth(self) -> int:
        return self._int_value("setup/depth", 5)

    def skip_installed(self) -> bool:
        return bool(self._settings.value("setup/skip_installed", True, type=bool))

    def abort_warnings(self) -> bool:
        return bool(self._settings.value("setup/abort_warnings", False, type=bool))

    def timeout_enabled(self) -> bool:
        return bool(self._settings.value("setup/timeout_enabled", False, type=bool))

    def timeout(self) -> int:
        return self._int_value("setup/timeout", 3600)

    def overwrite(self) -> bool:
        return bool(self._settings.value("setup/overwrite", False, type=bool))

    def strict_matching(self) -> bool:
        return bool(self._settings.value("setup/strict_matching", False, type=bool))

    def download(self) -> bool:
        return bool(self._settings.value("setup/download", True, type=bool))

    def tick_enabled(self) -> bool:
        return bool(self._settings.value("setup/tick_enabled", False, type=bool))

    def tick(self) -> int:
        return self._int_value("setup/tick", 500)

    def bgee_game(self) -> str:
        return str(self._settings.value("setup/bgee_game", ""))

    def bg2ee_game(self) -> str:
        return str(self._settings.value("setup/bg2ee_game", ""))

    def eet_bgee_game(self) -> str:
        return str(self._settings.value("setup/eet_bgee_game", ""))

    def eet_bg2ee_game(self) -> str:
        return str(self._settings.value("setup/eet_bg2ee_game", ""))

    def bgee_generate_dir(self) -> str:
        return str(self._settings.value("setup/bgee_generate_dir", ""))

    def bg2ee_generate_dir(self) -> str:
        return str(self._settings.value("setup/bg2ee_generate_dir", ""))

    def eet_pre_dir(self) -> str:
        return str(self._settings.value("setup/eet_pre_dir", ""))

    def eet_new_dir(self) -> str:
        return str(self._settings.value("setup/eet_new_dir", ""))

    def bgee_log_folder(self) -> str:
        return str(self._settings.value("setup/bgee_log_folder", ""))

    def bg2ee_log_folder(self) -> str:
        return str(self._settings.value("setup/bg2ee_log_folder", ""))

    def eet_bgee_log_folder(self) -> str:
        return str(self._settings.value("setup/eet_bgee_log_folder", ""))

    def eet_bg2ee_log_folder(self) -> str:
        return str(self._settings.value("setup/eet_bg2ee_log_folder", ""))

    def bgee_log_file(self) -> str:
        return str(self._settings.value("setup/bgee_log_file", ""))

    def bg2ee_log_file(self) -> str:
        return str(self._settings.value("setup/bg2ee_log_file", ""))

    def eet_bgee_log_file(self) -> str:
        return str(self._settings.value("setup/eet_bgee_log_file", ""))

    def eet_bg2ee_log_file(self) -> str:
        return str(self._settings.value("setup/eet_bg2ee_log_file", ""))
