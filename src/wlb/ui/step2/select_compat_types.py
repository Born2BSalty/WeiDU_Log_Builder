from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ModStatus:
    level: str
    reason: str
    deps_missing: list[str]
    deps_present: list[str]
    conflicts: list[str]


@dataclass(frozen=True)
class StatusBundle:
    header: ModStatus
    components: list[ModStatus]


def worst_status(statuses: list[ModStatus]) -> ModStatus:
    if not statuses:
        return ModStatus("ok", "", [], [], [])
    order = {"red": 3, "orange": 2, "gray": 1, "ok": 0}
    return max(statuses, key=lambda s: order.get(s.level, 0))


def header_status(statuses: list[ModStatus]) -> ModStatus:
    if not statuses:
        return ModStatus("ok", "", [], [], [])
    reds = [s for s in statuses if s.level == "red"]
    if len(reds) == len(statuses):
        return reds[0]
    if reds:
        return ModStatus("orange", "Some components incompatible", [], [], [])
    return worst_status(statuses)
