from __future__ import annotations

import re
from pathlib import Path

_AUTHOR_RE = re.compile(r"^\s*AUTHOR\s+~([^~]+)~", re.IGNORECASE)
_VERSION_RE = re.compile(r"^\s*VERSION\s+~([^~]+)~", re.IGNORECASE)
_VERSION_QUOTED_RE = re.compile(r"^\s*VERSION\s+\"([^\"]+)\"", re.IGNORECASE)


def parse_author(tp2_path: Path) -> str | None:
    try:
        text = tp2_path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None
    for line in text.splitlines():
        match = _AUTHOR_RE.match(line)
        if match:
            return match.group(1).strip() or None
    return None


def parse_version(tp2_path: Path) -> str | None:
    try:
        text = tp2_path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None
    for line in text.splitlines():
        match = _VERSION_RE.match(line)
        if match:
            return match.group(1).strip() or None
        match = _VERSION_QUOTED_RE.match(line)
        if match:
            return match.group(1).strip() or None
    return None