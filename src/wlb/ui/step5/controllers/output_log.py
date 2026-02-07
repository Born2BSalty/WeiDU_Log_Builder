from __future__ import annotations

import sys
from pathlib import Path

from wlb.services.settings_service import SettingsService


def default_install_log(settings: SettingsService) -> Path:
    base = _preferred_install_log_dir(settings)
    if base is None:
        base = (
            Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path.cwd()
        )
    return base / "install_log.txt"


def _preferred_install_log_dir(settings: SettingsService) -> Path | None:
    game = settings.game()
    if game == "BGEE":
        if settings.generate_dir_enabled() and settings.bgee_generate_dir():
            return Path(settings.bgee_generate_dir())
        if settings.bgee_game():
            return Path(settings.bgee_game())
    if game == "BG2EE":
        if settings.generate_dir_enabled() and settings.bg2ee_generate_dir():
            return Path(settings.bg2ee_generate_dir())
        if settings.bg2ee_game():
            return Path(settings.bg2ee_game())
    if game == "EET":
        if settings.new_eet_enabled() and settings.eet_new_dir():
            return Path(settings.eet_new_dir())
        if settings.eet_bg2ee_game():
            return Path(settings.eet_bg2ee_game())
        if settings.eet_bgee_game():
            return Path(settings.eet_bgee_game())
    return None
