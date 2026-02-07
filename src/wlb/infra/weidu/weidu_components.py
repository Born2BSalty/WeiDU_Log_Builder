from __future__ import annotations

import re
from pathlib import Path, PureWindowsPath

from wlb.ports.process_port import ProcessPort
from wlb.ports.weidu_port import WeiduPort

_COMPONENT_RE = re.compile(r"^\s*(\d+)\s*[:\-]\s*(.+)$")
_TP2_LINE_RE = re.compile(r"^~.*~\s+#\d+\s+#\d+\s+//\s+(.+)$", re.IGNORECASE)
_LANG_RE = re.compile(r"^(\d+)\s*:\s*(.+)$")


class WeiduComponents(WeiduPort):
    def __init__(self, runner: ProcessPort) -> None:
        self._runner = runner

    def list_components(
        self, weidu_path: Path, tp2_path: Path, game_dir: Path, mods_dir: Path
    ) -> list[str]:
        if not weidu_path.exists() or not tp2_path.exists() or not game_dir.exists():
            return []
        lang_idx = _pick_language_index(self._runner, weidu_path, tp2_path, game_dir, mods_dir)
        if lang_idx is None:
            lang_idx = "0"
        result = self._runner.run(
            [
                str(weidu_path),
                "--game",
                str(game_dir),
                "--list-components",
                str(tp2_path),
                lang_idx,
            ],
            cwd=mods_dir,
        )
        if result.returncode != 0:
            return []
        return [_normalize_component(line, mods_dir) for line in _parse_components(result.stdout)]


def _pick_language_index(
    runner: ProcessPort,
    weidu_path: Path,
    tp2_path: Path,
    game_dir: Path,
    mods_dir: Path,
) -> str | None:
    result = runner.run(
        [
            str(weidu_path),
            "--game",
            str(game_dir),
            "--list-languages",
            str(tp2_path),
        ],
        cwd=mods_dir,
    )
    if result.returncode != 0:
        return None
    languages = _parse_languages(result.stdout)
    if not languages:
        return None
    for key in ("english", "en_us", "en"):
        if key in languages:
            return languages[key]
    return languages.get("0")


def _parse_languages(text: str) -> dict[str, str]:
    languages: dict[str, str] = {}
    for line in text.splitlines():
        match = _LANG_RE.match(line.strip())
        if not match:
            continue
        index = match.group(1)
        name = match.group(2).strip().lower()
        languages[name] = index
        if index not in languages:
            languages[index] = index
    return languages


def _parse_components(text: str) -> list[str]:
    components: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if _TP2_LINE_RE.match(stripped):
            components.append(stripped)
            continue
        if _COMPONENT_RE.match(stripped):
            components.append(stripped)
            continue
    return components


def _normalize_component(line: str, mods_dir: Path) -> str:
    match = _TP2_LINE_RE.match(line)
    if not match:
        return line
    end_of_path = line.find("~", 1)
    if end_of_path == -1:
        return line
    raw_path = line[1:end_of_path]
    try:
        rel = Path(raw_path).resolve().relative_to(mods_dir.resolve())
        rel_path = str(PureWindowsPath(rel)).upper()
    except Exception:
        rel_path = str(PureWindowsPath(raw_path)).upper()
    return f"~{rel_path}~{line[end_of_path + 1 :]}".strip()
