from __future__ import annotations

from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from wlb.domain.models import ModInfo
from wlb.infra.scan.tp2_meta import parse_author, parse_version
from wlb.ports.fs_port import FsPort
from wlb.ports.weidu_port import WeiduPort


class ScanService:
    def __init__(self, fs: FsPort, weidu: WeiduPort, workers: int = 1) -> None:
        self._fs = fs
        self._weidu = weidu
        self._workers = max(1, workers)

    def scan_mods(
        self,
        mods_dir: Path,
        weidu_path: Path,
        game_dir: Path,
        on_progress: Callable[[int, int, str], None] | None = None,
        should_cancel: Callable[[], bool] | None = None,
    ) -> list[ModInfo]:
        tp2_files = self._fs.find_tp2_files(mods_dir)
        grouped = _group_tp2s(tp2_files, mods_dir)
        total = len(grouped)
        mods: list[ModInfo] = []

        def _scan_one(label: str, tp2_paths: list[Path]) -> ModInfo:
            main_tp2 = tp2_paths[0]
            components: list[str] = []
            for path in tp2_paths:
                components.extend(self._weidu.list_components(weidu_path, path, game_dir, mods_dir))
            author = parse_author(main_tp2)
            version = parse_version(main_tp2)
            return ModInfo(
                name=label,
                tp2_path=main_tp2,
                components=components,
                author=author,
                readme_path=None,
                version=version,
            )

        with ThreadPoolExecutor(max_workers=self._workers) as executor:
            futures = {
                executor.submit(_scan_one, label, paths): label for label, paths in grouped.items()
            }
            for done, future in enumerate(as_completed(futures), start=1):
                if should_cancel and should_cancel():
                    break
                path = futures[future]
                mods.append(future.result())
                if on_progress:
                    on_progress(done, total, path)
        return mods

    def scan_readme(self, tp2_path: Path, mod_name: str, game_dir: Path) -> Path | None:
        game_lang = _pick_game_lang(game_dir)
        return self._fs.find_readme(tp2_path.parent, game_lang=game_lang, mod_name=mod_name)


def _pick_game_lang(game_dir: Path) -> str | None:
    lang_root = game_dir / "lang"
    if not lang_root.exists():
        return None
    candidates = [p for p in lang_root.iterdir() if p.is_dir()]
    if not candidates:
        return None
    for pick in ("en_us", "en_gb", "english", "en"):
        for entry in candidates:
            if entry.name.lower() == pick:
                return entry.name.lower()
    return candidates[0].name.lower()


def _mod_label(tp2_path: Path, mods_dir: Path) -> str:
    try:
        rel = tp2_path.resolve().relative_to(mods_dir.resolve())
    except Exception:
        rel = tp2_path
    parts = list(rel.parts)
    if len(parts) >= 2:
        return parts[0]
    return tp2_path.parent.name or tp2_path.stem


def _group_tp2s(tp2_paths: list[Path], mods_dir: Path) -> dict[str, list[Path]]:
    grouped: dict[str, list[Path]] = {}
    for tp2_path in tp2_paths:
        label = _mod_label(tp2_path, mods_dir)
        grouped.setdefault(label, []).append(tp2_path)
    return grouped
