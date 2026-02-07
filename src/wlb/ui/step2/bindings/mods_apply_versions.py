from __future__ import annotations

from pathlib import Path

from wlb.infra.fs.windows_version import detect_game_version
from wlb.services.settings_service import SettingsService


def resolve_game_versions(settings: SettingsService) -> tuple[str | None, str | None]:
    bgee_version = settings.game_version_for("BGEE")
    if not bgee_version:
        game_dir = settings.bgee_game() or settings.eet_bgee_game()
        if game_dir:
            bgee_version = detect_game_version(Path(game_dir))
    bg2ee_version = settings.game_version_for("BG2EE")
    if not bg2ee_version:
        game_dir = settings.bg2ee_game() or settings.eet_bg2ee_game()
        if game_dir:
            bg2ee_version = detect_game_version(Path(game_dir))
    return bgee_version, bg2ee_version
