from __future__ import annotations


def match_mod(rule_mod: str, mod_label: str, tp2_stem: str, tp2_name: str) -> bool:
    if rule_mod in (mod_label, tp2_stem, tp2_name):
        return True
    return rule_mod in mod_label or rule_mod in tp2_stem or rule_mod in tp2_name


def component_text(component: str) -> str:
    return component.strip()


def component_id(component: str) -> str | None:
    parts = component.split("#")
    if len(parts) < 3:
        return None
    comp_id = parts[2].strip().split()[0]
    return comp_id or None
