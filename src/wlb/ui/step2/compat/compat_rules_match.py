from __future__ import annotations

from wlb.domain.models import ModInfo
from wlb.ui.step2.compat.compat_rules_loader import CompatRule
from wlb.ui.step2.compat.compat_rules_matchers import component_id, component_text, match_mod
from wlb.ui.step2.compat.compat_rules_types import CompatIssue
from wlb.ui.step2.compat.compat_rules_version import version_ok


def build_issue_map(
    mods: list[ModInfo],
    rules: list[CompatRule],
    game: str,
    game_version: str | None,
    mode: str | None = None,
) -> dict[tuple[str, int], CompatIssue]:
    issues: dict[tuple[str, int], CompatIssue] = {}
    if not rules:
        return issues
    for mod in mods:
        mod_label = _display_mod_name(mod.name).lower()
        tp2_stem = mod.tp2_path.stem.lower()
        tp2_name = mod.tp2_path.name.lower()
        for idx, component in enumerate(mod.components):
            comp_text = component_text(component)
            comp_id = component_id(component)
            for rule in rules:
                if rule.mode:
                    if mode is None:
                        continue
                    if mode.lower() not in {m.lower() for m in rule.mode}:
                        continue
                if rule.games and game.lower() not in {g.lower() for g in rule.games}:
                    continue
                if rule.min_game_version and not version_ok(game_version, rule.min_game_version):
                    continue
                rule_mod = rule.mod.lower()
                if not match_mod(rule_mod, mod_label, tp2_stem, tp2_name):
                    continue
                if rule.component and rule.component.lower() not in comp_text.lower():
                    continue
                if rule.component_id and rule.component_id != comp_id:
                    continue
                issues[(str(mod.tp2_path), idx)] = CompatIssue(rule.issue, rule.message)
    return issues


def _display_mod_name(name: str) -> str:
    lowered = name.lower()
    if lowered.startswith("setup-"):
        return name[6:]
    if lowered.startswith("setup_"):
        return name[6:]
    return name
