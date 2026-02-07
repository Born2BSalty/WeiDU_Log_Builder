from __future__ import annotations

from wlb.ui.step2.compat.compat_parse_tokens import norm_tp2_name
from wlb.ui.step2.compat.select_compat_deps import (
    mod_is_installed_refs,
    parse_conflicts,
    parse_required,
)
from wlb.ui.step2.compat.select_compat_game import game_compat_reason
from wlb.ui.step2.compat.select_compat_types import ModStatus


def eval_block(lines: list[str], game: str, tp2_names: set[str]) -> ModStatus:
    text = "\n".join(lines)
    req_lines = [line for line in lines if "REQUIRE_PREDICATE" in line.upper()]
    req_text = "\n".join(req_lines)
    reason = game_compat_reason(req_text, game)
    incompatible = reason is not None

    required = parse_required(text, norm_tp2_name)
    mods_installed = mod_is_installed_refs(req_text, norm_tp2_name)
    required |= {name for name, negated in mods_installed if not negated}
    conflicts = {name for name, negated in mods_installed if negated}
    conflicts |= parse_conflicts(text, norm_tp2_name)

    missing_mods = sorted({name for name in required if name and name not in tp2_names})
    present_mods = sorted({name for name in required if name and name in tp2_names})
    conflict_list = sorted({name for name in conflicts if name})

    if incompatible:
        return ModStatus(
            "red",
            reason or "Incompatible with selected game",
            missing_mods,
            present_mods,
            conflict_list,
        )
    if missing_mods:
        return ModStatus(
            "gray", "Missing required mod(s)", missing_mods, present_mods, conflict_list
        )
    if present_mods or conflict_list:
        return ModStatus(
            "orange",
            "Requires or conflicts with other mod(s)",
            missing_mods,
            present_mods,
            conflict_list,
        )
    return ModStatus("ok", "", missing_mods, present_mods, conflict_list)
