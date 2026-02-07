from __future__ import annotations

from pathlib import Path

from wlb.domain.models import ModInfo
from wlb.ui.step2.compat.select_compat import build_status_map
from wlb.ui.step2.compat.select_compat_types import StatusBundle


def build_status_maps(mods: list[ModInfo], mods_dir: Path) -> dict[str, dict[Path, StatusBundle]]:
    return {
        "BGEE": build_status_map(mods, mods_dir, "BGEE"),
        "BG2EE": build_status_map(mods, mods_dir, "BG2EE"),
    }
