from __future__ import annotations

from wlb.ui.step2.compat.select_compat_types import ModStatus


def format_missing(missing: list[str], status: ModStatus | None) -> list[str]:
    lines: list[str] = []
    ok = "✔"
    warn = "⚠"
    fail = "✖"
    if not missing:
        lines.append(f"{ok} Files: OK")
    else:
        lines.append(f"{fail} Files: Missing ({len(missing)})")
        lines.extend([f"  - {item}" for item in missing])
    if status is None:
        lines.extend(
            [
                f"{warn} Dependencies: Unknown",
                f"{warn} Conflicts: Unknown",
                f"{warn} Requires: Unknown",
            ]
        )
        return lines
    if status.reason:
        lines.append(f"{fail} Compatibility: {status.reason}")
    if status.deps_present:
        lines.append(f"{ok} Dependencies: {', '.join(status.deps_present)}")
    elif status.deps_missing:
        lines.append(f"{fail} Dependencies Missing: {', '.join(status.deps_missing)}")
    else:
        lines.append(f"{ok} Dependencies: None")
    required = sorted({*status.deps_present, *status.deps_missing})
    if required:
        lines.append(f"{ok} Requires: {', '.join(required)}")
    else:
        lines.append(f"{ok} Requires: None")
    if status.conflicts:
        lines.append(f"{fail} Conflicts: {', '.join(status.conflicts)}")
    else:
        lines.append(f"{ok} Conflicts: None")
    return lines
