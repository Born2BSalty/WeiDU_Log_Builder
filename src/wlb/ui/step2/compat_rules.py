from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from wlb.domain.models import ModInfo
from wlb.ui.step2.compat_rules_types import CompatIssue


@dataclass(frozen=True)
class CompatRule:
    mod: str
    component: str | None
    component_id: str | None
    games: list[str] | None
    mode: list[str] | None
    min_game_version: str | None
    issue: str
    message: str


def load_compat_rules(path: Path) -> list[CompatRule]:
    if not path.exists():
        return []
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    except Exception:
        data = _parse_basic_yaml(path.read_text(encoding="utf-8"))
    rules_raw = data.get("rules", data) if isinstance(data, dict) else data
    rules: list[CompatRule] = []
    if not isinstance(rules_raw, list):
        return []
    for item in rules_raw:
        if not isinstance(item, dict):
            continue
        mod = str(item.get("mod", "")).strip()
        if not mod:
            continue
        issue_value = str(item.get("issue", "") or item.get("kind", "")).strip().lower()
        rules.append(
            CompatRule(
                mod=mod,
                component=_opt_str(item.get("component")),
                component_id=_opt_str(item.get("component_id")),
                games=_opt_games(item.get("games"), item.get("game"), item.get("tab")),
                mode=_opt_games(item.get("mode")),
                min_game_version=_opt_str(
                    item.get("min_game_version"), item.get("min_tab_version")
                ),
                issue=issue_value or "warning",
                message=str(item.get("message", "")).strip() or "Compatibility rule matched.",
            )
        )
    return rules


def build_issue_map(
    mods: list[ModInfo],
    rules: list[CompatRule],
    game: str,
    game_version: str | None,
    mode: str | None = None,
) -> dict[tuple[str, int], CompatIssue]:
    issues: dict[tuple[str, int], CompatIssue] = {}
    if not rules:
        return issues
    for mod in mods:
        mod_label = _display_mod_name(mod.name).lower()
        tp2_stem = mod.tp2_path.stem.lower()
        tp2_name = mod.tp2_path.name.lower()
        for idx, component in enumerate(mod.components):
            comp_text = _component_text(component)
            comp_id = _component_id(component)
            for rule in rules:
                if rule.mode:
                    if mode is None:
                        continue
                    if mode.lower() not in {m.lower() for m in rule.mode}:
                        continue
                if rule.games and game.lower() not in {g.lower() for g in rule.games}:
                    continue
                if rule.min_game_version and not _version_ok(game_version, rule.min_game_version):
                    continue
                rule_mod = rule.mod.lower()
                if not _match_mod(rule_mod, mod_label, tp2_stem, tp2_name):
                    continue
                if rule.component and rule.component.lower() not in comp_text.lower():
                    continue
                if rule.component_id and rule.component_id != comp_id:
                    continue
                issues[(str(mod.tp2_path), idx)] = CompatIssue(rule.issue, rule.message)
    return issues


def _match_mod(rule_mod: str, mod_label: str, tp2_stem: str, tp2_name: str) -> bool:
    if rule_mod in (mod_label, tp2_stem, tp2_name):
        return True
    return rule_mod in mod_label or rule_mod in tp2_stem or rule_mod in tp2_name


def _component_text(component: str) -> str:
    return component.strip()


def _component_id(component: str) -> str | None:
    parts = component.split("#")
    if len(parts) < 3:
        return None
    comp_id = parts[2].strip().split()[0]
    return comp_id or None


def _version_ok(current: str | None, minimum: str) -> bool:
    if not current:
        return False
    return _version_tuple(current) >= _version_tuple(minimum)


def _version_tuple(value: str) -> tuple[int, ...]:
    result: list[int] = []
    for part in value.split("."):
        try:
            result.append(int(part))
        except ValueError:
            break
    return tuple(result)


def _opt_str(*values: object) -> str | None:
    for value in values:
        if value is None:
            continue
        text = str(value).strip()
        if text:
            return text
    return None


def _opt_games(*values: object) -> list[str] | None:
    for value in values:
        if value is None:
            continue
        if isinstance(value, list):
            items = [str(item).strip() for item in value if str(item).strip()]
            return items or None
        text = str(value).strip()
        if text:
            return [text]
    return None


def _parse_basic_yaml(text: str) -> list[dict[str, str]]:
    rules: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("-"):
            current = {}
            rules.append(current)
            line = line[1:].strip()
            if not line:
                continue
        if ":" in line and current is not None:
            key, value = line.split(":", 1)
            current[key.strip()] = value.strip().strip('"').strip("'")
    return rules


def _display_mod_name(name: str) -> str:
    lowered = name.lower()
    if lowered.startswith("setup-"):
        return name[6:]
    if lowered.startswith("setup_"):
        return name[6:]
    return name
