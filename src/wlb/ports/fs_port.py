from __future__ import annotations

from pathlib import Path
from typing import Protocol


class FsPort(Protocol):
    def find_tp2_files(self, mods_dir: Path) -> list[Path]: ...
    def find_readme(
        self, mod_dir: Path, *, game_lang: str | None = None, mod_name: str | None = None
    ) -> Path | None: ...
