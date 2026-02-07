from __future__ import annotations

from pathlib import Path
from typing import Protocol


class WeiduPort(Protocol):
    def list_components(
        self, weidu_path: Path, tp2_path: Path, game_dir: Path, mods_dir: Path
    ) -> list[str]: ...
