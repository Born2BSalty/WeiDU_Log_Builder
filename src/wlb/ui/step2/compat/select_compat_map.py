from __future__ import annotations

from pathlib import Path

from wlb.domain.models import ModInfo
from wlb.ui.step2.compat.select_compat_parse import eval_block, norm_tp2_name, split_components
from wlb.ui.step2.compat.select_compat_types import ModStatus, StatusBundle, header_status


def build_status_map(mods: list[ModInfo], mods_dir: Path, game: str) -> dict[Path, StatusBundle]:
    tp2_names = {norm_tp2_name(mod.tp2_path.name) for mod in mods}
    return {mod.tp2_path: _mod_status(mod.tp2_path, mods_dir, game, tp2_names) for mod in mods}


def _mod_status(tp2_path: Path, mods_dir: Path, game: str, tp2_names: set[str]) -> StatusBundle:
    try:
        text = tp2_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return StatusBundle(ModStatus("ok", "", [], [], []), [])
    global_lines, component_blocks = split_components(text)
    component_statuses = [eval_block(block, game, tp2_names) for block in component_blocks]
    global_status = eval_block(global_lines, game, tp2_names)
    header = header_status(component_statuses)
    if not component_statuses:
        header = global_status
    elif global_status.level == "red" and header.level != "red":
        header = ModStatus(
            "orange",
            "Compatibility check in TP2 header",
            global_status.deps_missing,
            global_status.deps_present,
            global_status.conflicts,
        )
    return StatusBundle(header, component_statuses)
