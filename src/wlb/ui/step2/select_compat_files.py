from __future__ import annotations

import os
import re
from pathlib import Path

_FILE_EXISTS_RE = re.compile(r"\bFILE_EXISTS\b\s*(?:~([^~]+)~|\"([^\"]+)\")", re.IGNORECASE)


def find_missing_files(tp2_paths: list[Path], mods_dir: Path, mod_root: Path) -> list[str]:
    missing: list[str] = []
    seen: set[str] = set()
    for tp2_path in tp2_paths:
        for rel in _extract_file_exists(tp2_path):
            if not rel or rel in seen:
                continue
            seen.add(rel)
            if _exists_in_mods(rel, mods_dir, mod_root):
                continue
            missing.append(rel)
    return missing


def _extract_file_exists(tp2_path: Path) -> list[str]:
    try:
        text = tp2_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []
    matches: list[str] = []
    for line in text.splitlines():
        if "FILE_EXISTS" not in line.upper():
            continue
        for match in _FILE_EXISTS_RE.finditer(line):
            rel = match.group(1) or match.group(2) or ""
            rel = rel.strip()
            if not rel or "%" in rel:
                continue
            matches.append(rel)
    return matches


def _exists_in_mods(rel: str, mods_dir: Path, mod_root: Path) -> bool:
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
