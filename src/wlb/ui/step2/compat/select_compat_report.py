from __future__ import annotations

from pathlib import Path

from wlb.domain.models import ModInfo
from wlb.ui.step2.compat.select_compat_types import StatusBundle


def format_status_report(
    mods: list[ModInfo], status_map: dict[Path, StatusBundle], title: str
) -> str:
    lines: list[str] = [f"[{title}]"]
    for mod in mods:
        bundle = status_map.get(mod.tp2_path)
        if bundle is None:
            continue
        header = bundle.header
        lines.append(
            f"MOD {mod.name} :: {mod.tp2_path.name} :: {header.level} :: {header.reason or 'OK'}"
        )
        if header.deps_missing:
            lines.append(f"  deps_missing: {', '.join(header.deps_missing)}")
        if header.deps_present:
            lines.append(f"  deps_present: {', '.join(header.deps_present)}")
        if header.conflicts:
            lines.append(f"  conflicts: {', '.join(header.conflicts)}")
        for idx, component in enumerate(mod.components):
            status = bundle.components[idx] if idx < len(bundle.components) else header
            comp_name = component.strip()
            lines.append(
                f"  COMP {idx:03d} :: {status.level} :: {status.reason or 'OK'} :: {comp_name}"
            )
            if status.deps_missing:
                lines.append(f"    deps_missing: {', '.join(status.deps_missing)}")
            if status.deps_present:
                lines.append(f"    deps_present: {', '.join(status.deps_present)}")
            if status.conflicts:
                lines.append(f"    conflicts: {', '.join(status.conflicts)}")
    lines.append("")
    return "\n".join(lines)
