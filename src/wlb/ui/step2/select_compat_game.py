from __future__ import annotations

import re

_GAME_IS_RE = re.compile(r"\bGAME_IS\s+~([^~]+)~", re.IGNORECASE)
_NOT_GAME_IS_RE = re.compile(r"(?:!GAME_IS|NOT\s+GAME_IS)\s+~([^~]+)~", re.IGNORECASE)


def game_compat_reason(req_text: str, game: str) -> str | None:
    game_lower = game.lower()
    for match in _NOT_GAME_IS_RE.finditer(req_text):
        if _game_in_list(game_lower, match.group(1)):
            return f"NOT GAME_IS excludes {match.group(1)}"
    game_is_matches = [m.group(1) for m in _GAME_IS_RE.finditer(req_text)]
    if game_is_matches and not any(_game_in_list(game_lower, values) for values in game_is_matches):
        return f"GAME_IS excludes {game}"
    return None


def _game_in_list(game: str, values: str) -> bool:
    tokens = [token.strip().lower() for token in values.split()]
    return game.lower() in tokens
