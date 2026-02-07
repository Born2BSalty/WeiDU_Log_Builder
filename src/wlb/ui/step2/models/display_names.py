from __future__ import annotations

import re

_TP2_LINE_RE = re.compile(r"^~.*~\s+#\d+\s+#\d+\s+//\s+(.+)$", re.IGNORECASE)
_COMPONENT_RE = re.compile(r"^\s*(\d+)\s*[:\-]\s*(.+)$")
_VERSION_TAIL_RE = re.compile(r":\s*(v?\d[\w.\-]*)\s*$", re.IGNORECASE)


def display_component_name(component: str) -> str:
    line = component.strip()
    tp2_match = _TP2_LINE_RE.match(line)
    if tp2_match:
        return tp2_match.group(1).strip()
    match = _COMPONENT_RE.match(line)
    if match:
        return match.group(2).strip()
    return line


def display_mod_name(name: str) -> str:
    lowered = name.lower()
    if lowered.startswith("setup-"):
        return name[6:]
    if lowered.startswith("setup_"):
        return name[6:]
    return name


def component_version(component: str, fallback: str | None) -> str:
    match = _VERSION_TAIL_RE.search(component.strip())
    if match:
        return match.group(1).strip()
    return fallback or "-"
