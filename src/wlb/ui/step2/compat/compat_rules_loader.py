from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


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
