from __future__ import annotations

import os
import re
from pathlib import Path

from wlb.services.install_service import InstallRequest
from wlb.services.settings_service import SettingsService
from wlb.ui.step2.models.selection_store import SelectionOrderStore


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
        extra_flags = self._extra_flags()

        if game == "EET":
            argv = [
                installer_path,
                "eet",
                "--bg1-game-directory",
                self._settings.eet_bgee_game(),
                "--bg1-log-file",
                self._log_file(
                    self._settings.eet_bgee_log_file(),
                    self._settings.eet_bgee_log_folder(),
                    use_logs,
                ),
                "--bg2-game-directory",
                self._settings.eet_bg2ee_game(),
                "--bg2-log-file",
                self._log_file(
                    self._settings.eet_bg2ee_log_file(),
                    self._settings.eet_bg2ee_log_folder(),
                    use_logs,
                ),
                "--weidu-binary",
                weidu_path,
                "--mod-directories",
                mods_dir,
                "--check-last-installed",
            ]
            argv.extend(extra_flags)
            self._add_eet_dirs(argv)
            return InstallRequest(argv=argv, cwd=Path(mods_dir) if mods_dir else None, env=env)

        if game == "BG2EE":
            argv = [
                installer_path,
                "normal",
                "--weidu-binary",
                weidu_path,
                "--mod-directories",
                mods_dir,
                "--game-directory",
                self._settings.bg2ee_game(),
                "--log-file",
                self._log_file(
                    self._settings.bg2ee_log_file(), self._settings.bg2ee_log_folder(), use_logs
                ),
                "--check-last-installed",
            ]
            argv.extend(extra_flags)
            self._add_generate_dir(argv, self._settings.bg2ee_generate_dir())
            return InstallRequest(argv=argv, cwd=Path(mods_dir) if mods_dir else None, env=env)

        argv = [
            installer_path,
            "normal",
            "--weidu-binary",
            weidu_path,
            "--mod-directories",
            mods_dir,
            "--game-directory",
            self._settings.bgee_game(),
            "--log-file",
            self._log_file(
                self._settings.bgee_log_file(), self._settings.bgee_log_folder(), use_logs
            ),
            "--check-last-installed",
        ]
        argv.extend(extra_flags)
        self._add_generate_dir(argv, self._settings.bgee_generate_dir())
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

    def _extra_flags(self) -> list[str]:
        flags: list[str] = []
        if self._settings.custom_depth_enabled():
            flags.extend(["--depth", str(self._settings.depth())])
        flags.extend(["--skip-installed", str(self._settings.skip_installed()).lower()])
        flags.extend(["--abort-on-warnings", str(self._settings.abort_warnings()).lower()])
        flags.extend(["--strict-matching", str(self._settings.strict_matching()).lower()])
        flags.extend(["--download", str(self._settings.download()).lower()])
        flags.extend(["--overwrite", str(self._settings.overwrite()).lower()])
        if self._settings.timeout_enabled():
            flags.extend(["--timeout", str(self._settings.timeout())])
        if self._settings.component_logs():
            folder = self._settings.component_logs_folder()
            if folder:
                folder = self._sanitize_log_folder(folder)
                mode = f"log {folder},logapp,log-extern"
                flags.extend(["--weidu-log-mode", mode])
        if self._settings.tick_enabled():
            flags.extend(["--tick", str(self._settings.tick())])
        return flags

    def _add_generate_dir(self, argv: list[str], path: str) -> None:
        if self._settings.generate_dir_enabled() and path:
            argv.extend(["--generate-directory", path])

    @staticmethod
    def _sanitize_log_folder(folder: str) -> str:
        if " " not in folder:
            return folder
        sanitized = re.sub(r"\s+", "_", folder)
        try:
            Path(sanitized).mkdir(parents=True, exist_ok=True)
        except OSError:
            return folder
        return sanitized

    def _add_eet_dirs(self, argv: list[str]) -> None:
        if self._settings.pre_eet_enabled():
            path = self._settings.eet_pre_dir()
            if path:
                argv.extend(["--new-pre-eet-dir", path])
        if self._settings.new_eet_enabled():
            path = self._settings.eet_new_dir()
            if path:
                argv.extend(["--new-eet-dir", path])
