from __future__ import annotations

import re

_REQUIRE_COMPONENT_RE = re.compile(r"REQUIRE_COMPONENT\s+~([^~]+)~", re.IGNORECASE)
_FORBID_COMPONENT_RE = re.compile(r"FORBID_COMPONENT\s+~([^~]+)~", re.IGNORECASE)


def parse_required(text: str, norm: callable) -> set[str]:
    return {norm(m.group(1)) for m in _REQUIRE_COMPONENT_RE.finditer(text)}


def parse_conflicts(text: str, norm: callable) -> set[str]:
    return {norm(m.group(1)) for m in _FORBID_COMPONENT_RE.finditer(text)}


def mod_is_installed_refs(text: str, norm: callable) -> list[tuple[str, bool]]:
    results: list[tuple[str, bool]] = []
    pattern = re.compile(r"(NOT\s+)?MOD_IS_INSTALLED\s+~([^~]+)~", re.IGNORECASE)
    for line in text.splitlines():
        if "MOD_IS_INSTALLED" not in line.upper():
            continue
        for match in pattern.finditer(line):
            name = norm(match.group(2))
            negated = bool(match.group(1))
            results.append((name, negated))
    return results
