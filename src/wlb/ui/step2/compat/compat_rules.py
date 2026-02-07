from __future__ import annotations

from wlb.ui.step2.compat.compat_rules_loader import CompatRule, load_compat_rules
from wlb.ui.step2.compat.compat_rules_match import build_issue_map

__all__ = [
    "CompatRule",
    "load_compat_rules",
    "build_issue_map",
]
