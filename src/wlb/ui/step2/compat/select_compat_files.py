from __future__ import annotations

import re
from pathlib import Path

from wlb.ui.step2.compat.compat_files_scan import exists_in_mods

_FILE_EXISTS_RE = re.compile(r"\bFILE_EXISTS\b\s*(?:~([^~]+)~|\"([^\"]+)\")", re.IGNORECASE)


def find_missing_files(tp2_paths: list[Path], mods_dir: Path, mod_root: Path) -> list[str]:
    missing: list[str] = []
    seen: set[str] = set()
    for tp2_path in tp2_paths:
        for rel in _extract_file_exists(tp2_path):
            if not rel or rel in seen:
                continue
            seen.add(rel)
            if exists_in_mods(rel, mods_dir, mod_root):
                continue
            missing.append(rel)
    return missing


def _extract_file_exists(tp2_path: Path) -> list[str]:
    try:
        text = tp2_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []
    return _find_file_exists_lines(text.splitlines())


def _find_file_exists_lines(lines: list[str]) -> list[str]:
    matches: list[str] = []
    for line in lines:
        if "FILE_EXISTS" not in line.upper():
            continue
        for match in _FILE_EXISTS_RE.finditer(line):
            rel = match.group(1) or match.group(2) or ""
            rel = rel.strip()
            if not rel or "%" in rel:
                continue
            matches.append(rel)
    return matches
