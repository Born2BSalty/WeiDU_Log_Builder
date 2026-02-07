from __future__ import annotations

import re

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


def norm_tp2_name(raw: str) -> str:
    name = raw.strip().replace("\\", "/")
    name = name.split("/")[-1]
    name = name.lower()
    if name.startswith("setup-"):
        name = name[len("setup-") :]
    if name.startswith("setup_"):
        name = name[len("setup_") :]
    return name
