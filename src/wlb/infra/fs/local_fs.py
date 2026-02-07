from __future__ import annotations

import os
from pathlib import Path

from wlb.infra.fs.readme_finder import find_best_readme
from wlb.ports.fs_port import FsPort


class LocalFs(FsPort):
    def find_tp2_files(self, mods_dir: Path) -> list[Path]:
        if not mods_dir.exists():
            return []
        results: list[Path] = []
        mods_root = mods_dir.resolve()
        for root, _dirs, files in os.walk(mods_root):
            current = Path(root)
            for name in files:
                if not name.lower().endswith(".tp2"):
                    continue
                results.append(current / name)
        return results

    def find_readme(
        self, mod_dir: Path, *, game_lang: str | None = None, mod_name: str | None = None
    ) -> Path | None:
        return find_best_readme(mod_dir, game_lang=game_lang, mod_name=mod_name)
