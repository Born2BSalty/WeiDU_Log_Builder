from __future__ import annotations

import re

from wlb.ui.step2.select_compat_deps import mod_is_installed_refs, parse_conflicts, parse_required
from wlb.ui.step2.select_compat_game import game_compat_reason
from wlb.ui.step2.select_compat_types import ModStatus

_BEGIN_RE = re.compile(r"^\s*BEGIN\s+(?:~|@)", re.IGNORECASE)


def split_components(text: str) -> tuple[list[str], list[list[str]]]:
    global_lines: list[str] = []
    components: list[list[str]] = []
    current: list[str] | None = None
    for line in text.splitlines():
        if _BEGIN_RE.match(line):
            current = []
            components.append(current)
        if current is None:
            global_lines.append(line)
        else:
            current.append(line)
    return global_lines, components


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


def norm_tp2_name(raw: str) -> str:
    name = raw.strip().replace("\\", "/")
    name = name.split("/")[-1]
    name = name.lower()
    if name.startswith("setup-"):
        name = name[len("setup-") :]
    if name.startswith("setup_"):
        name = name[len("setup_") :]
    return name
