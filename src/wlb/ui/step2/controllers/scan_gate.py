from __future__ import annotations

from pathlib import Path

from wlb.services.settings_service import SettingsService
from wlb.ui.step2.views.selection_ui import SelectionUi


def validate_scan_inputs(
    settings: SettingsService, ui: SelectionUi
) -> tuple[Path, Path, Path] | None:
    mods_dir = settings.mods_folder()
    weidu_path = settings.weidu_path()
    game_dir = settings.bgee_game()
    if not mods_dir:
        ui.details_desc.setPlainText("Set a Mods Folder on Step 1 before scanning.")
        return None
    if not weidu_path:
        ui.details_desc.setPlainText("Set WeiDU.exe path on Step 1 before scanning.")
        return None
    if not game_dir:
        ui.details_desc.setPlainText("Set a game folder on Step 1 before scanning.")
        return None
    return Path(mods_dir), Path(weidu_path), Path(game_dir)
