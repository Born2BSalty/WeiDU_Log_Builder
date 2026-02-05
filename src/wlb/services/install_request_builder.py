from __future__ import annotations

import os
from pathlib import Path

from wlb.services.install_service import InstallRequest
from wlb.services.settings_service import SettingsService
from wlb.ui.step2.selection_store import SelectionOrderStore


class InstallRequestBuilder:
    def __init__(self, settings: SettingsService, store: SelectionOrderStore) -> None:
        self._settings = settings
        self._store = store

    def build(self) -> InstallRequest:
        mods_dir = self._settings.mods_folder()
        installer_path = self._settings.mod_installer_path()
        weidu_path = self._settings.weidu_path()
        game = self._settings.game()
        use_logs = self._settings.has_logs()
        env = self._rust_env()

        if game == "EET":
            argv = [
                installer_path,
                "-e",
                "-1",
                self._settings.bgee_game(),
                "-y",
                self._log_file(
                    self._settings.eet_bgee_log_file(),
                    self._settings.eet_bgee_log_folder(),
                    use_logs,
                ),
                "-2",
                self._settings.bg2ee_game(),
                "-z",
                self._log_file(
                    self._settings.eet_bg2ee_log_file(),
                    self._settings.eet_bg2ee_log_folder(),
                    use_logs,
                ),
                "-w",
                weidu_path,
                "-m",
                mods_dir,
                "-c",
            ]
            return InstallRequest(argv=argv, cwd=Path(mods_dir) if mods_dir else None, env=env)

        if game == "BG2EE":
            argv = [
                installer_path,
                "-n",
                "-w",
                weidu_path,
                "-m",
                mods_dir,
                "-g",
                self._settings.bg2ee_game(),
                "-f",
                self._log_file(
                    self._settings.bg2ee_log_file(), self._settings.bg2ee_log_folder(), use_logs
                ),
                "-c",
            ]
            return InstallRequest(argv=argv, cwd=Path(mods_dir) if mods_dir else None, env=env)

        argv = [
            installer_path,
            "-n",
            "-w",
            weidu_path,
            "-m",
            mods_dir,
            "-g",
            self._settings.bgee_game(),
            "-f",
            self._log_file(
                self._settings.bgee_log_file(), self._settings.bgee_log_folder(), use_logs
            ),
            "-c",
        ]
        return InstallRequest(argv=argv, cwd=Path(mods_dir) if mods_dir else None, env=env)

    @staticmethod
    def _log_file(file_path: str, folder_path: str, use_logs: bool) -> str:
        if use_logs and file_path:
            return file_path
        if folder_path:
            return str(Path(folder_path) / "weidu.log")
        return ""

    def _rust_env(self) -> dict[str, str] | None:
        if self._settings.rust_log_trace():
            env = os.environ.copy()
            env["RUST_LOG"] = "TRACE"
            return env
        if self._settings.rust_log_debug():
            env = os.environ.copy()
            env["RUST_LOG"] = "DEBUG"
            return env
        return None