from __future__ import annotations

from PySide6.QtCore import QSettings


class SettingsService:
    def __init__(self, settings: QSettings | None = None) -> None:
        self._settings = settings or QSettings()

    def game(self) -> str:
        return str(self._settings.value("setup/game", "BGEE"))

    def has_logs(self) -> bool:
        return bool(self._settings.value("setup/has_logs", False, type=bool))

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

    def bgee_game(self) -> str:
        return str(self._settings.value("setup/bgee_game", ""))

    def bg2ee_game(self) -> str:
        return str(self._settings.value("setup/bg2ee_game", ""))

    def eet_bgee_game(self) -> str:
        return str(self._settings.value("setup/eet_bgee_game", ""))

    def eet_bg2ee_game(self) -> str:
        return str(self._settings.value("setup/eet_bg2ee_game", ""))

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