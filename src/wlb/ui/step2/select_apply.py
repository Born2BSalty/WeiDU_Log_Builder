from __future__ import annotations

from pathlib import Path

from wlb.domain.models import ModInfo
from wlb.infra.fs.windows_version import detect_game_version
from wlb.services.settings_service import SettingsService
from wlb.ui.step2.compat_rules import build_issue_map, load_compat_rules
from wlb.ui.step2.select_binding import wire_model
from wlb.ui.step2.select_layout import SelectionUi
from wlb.ui.step2.select_missing import MissingFilesReporter
from wlb.ui.step2.select_models import _display_mod_name, build_mods_model
from wlb.ui.step2.selection_store import SelectionOrderStore


def apply_mods(
    ui: SelectionUi,
    mods: list[ModInfo],
    store: SelectionOrderStore,
    settings: SettingsService,
    reporter: MissingFilesReporter | None = None,
) -> None:
    mods = sorted(mods, key=lambda mod: _display_mod_name(mod.name).lower())
    rules = load_compat_rules(Path("config/compat_rules.yaml"))
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

    mode = settings.game()
    bgee_issues = build_issue_map(mods, rules, "BGEE", bgee_version, mode)
    bg2ee_issues = build_issue_map(mods, rules, "BG2EE", bg2ee_version, mode)
    bgee_model = build_mods_model(mods, bgee_issues)
    bg2ee_model = build_mods_model(mods, bg2ee_issues)
    wire_model(
        ui.bgee_view,
        bgee_model,
        ui.details_desc,
        ui.details_mod_id,
        ui.details_component,
        ui.details_version,
        ui.details_path,
        ui.details_author,
        ui.details_readme,
        ui.details_name,
        store,
        "BGEE",
        reporter.for_item if reporter is not None else None,
    )
    wire_model(
        ui.bg2ee_view,
        bg2ee_model,
        ui.details_desc,
        ui.details_mod_id,
        ui.details_component,
        ui.details_version,
        ui.details_path,
        ui.details_author,
        ui.details_readme,
        ui.details_name,
        store,
        "BG2EE",
        reporter.for_item if reporter is not None else None,
    )
