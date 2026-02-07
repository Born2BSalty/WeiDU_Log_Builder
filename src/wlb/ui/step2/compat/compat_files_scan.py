from __future__ import annotations

import os
from pathlib import Path


def exists_in_mods(rel: str, mods_dir: Path, mod_root: Path) -> bool:
    candidate = Path(rel)
    if candidate.is_absolute():
        return candidate.exists()
    if _exists_in_mod_root(mod_root, candidate, max_depth=3):
        return True
    if _exists_in_mod_root(mods_dir, candidate, max_depth=3):
        return True
    return bool((mods_dir / candidate).exists())


def _exists_in_mod_root(mod_root: Path, candidate: Path, max_depth: int) -> bool:
    direct = mod_root / candidate
    if direct.exists():
        return True
    if not mod_root.exists():
        return False
    base_depth = len(mod_root.parts)
    name = candidate.name.lower()
    for root, dirs, files in os.walk(mod_root):
        depth = len(Path(root).parts) - base_depth
        if depth > max_depth:
            dirs[:] = []
            continue
        for filename in files:
            if filename.lower() == name:
                return True
    return False
