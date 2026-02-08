from __future__ import annotations

import sys
from pathlib import Path

from wlb.domain.models import ModInfo
from wlb.services.settings_service import SettingsService
from wlb.ui.step2.bindings.mods_apply_versions import resolve_game_versions
from wlb.ui.step2.compat.compat_rules import build_issue_map, load_compat_rules
from wlb.ui.step2.models.select_models import build_mods_model


def build_game_models(mods: list[ModInfo], settings: SettingsService) -> tuple[object, object]:
    rules = load_compat_rules(_compat_rules_path())
    bgee_version, bg2ee_version = resolve_game_versions(settings)
    mode = settings.game()
    bgee_issues = build_issue_map(mods, rules, "BGEE", bgee_version, mode)
    bg2ee_issues = build_issue_map(mods, rules, "BG2EE", bg2ee_version, mode)
    return build_mods_model(mods, bgee_issues), build_mods_model(mods, bg2ee_issues)


def _compat_rules_path() -> Path:
    if getattr(sys, "frozen", False):
        base = Path(sys.executable).resolve().parent
        return base / "_internal" / "config" / "compat_rules.yaml"
    here = Path(__file__).resolve()
    for parent in here.parents:
        direct = parent / "config" / "compat_rules.yaml"
        if direct.exists():
            return direct
        dev = parent / "dev" / "config" / "compat_rules.yaml"
        if dev.exists():
            return dev
    return here.parents[4] / "config" / "compat_rules.yaml"
