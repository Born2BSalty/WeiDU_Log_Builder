from __future__ import annotations

import os
from pathlib import Path


def find_best_readme(
    mod_dir: Path, *, game_lang: str | None = None, mod_name: str | None = None
) -> Path | None:
    if not mod_dir.exists():
        return None
    mod_name = (mod_name or mod_dir.name).lower()
    lang = (game_lang or "").lower()
    max_depth = 3
    ext_rank = {".txt": 5, ".md": 4, ".rtf": 3, ".html": 2, ".htm": 2, ".pdf": 1}
    keywords = ("readme", "install", "setup", "howto")
    install_words = ("install", "installation", "setup", "weidu", "component")

    def _iter_files(root: Path) -> list[Path]:
        if not root.exists():
            return []
        files: list[Path] = []
        base_depth = len(root.parts)
        for current, dirs, file_names in os.walk(root):
            depth = len(Path(current).parts) - base_depth
            if depth > max_depth:
                dirs[:] = []
                continue
            for name in file_names:
                files.append(Path(current) / name)
        return files

    def _norm(name: str) -> str:
        return name.lower().replace("-", "_")

    def _lang_match(name: str) -> bool:
        if not lang:
            return False
        return _norm(lang) in _norm(name)

    def _is_french(name: str) -> bool:
        lowered = name.lower()
        return (
            "french" in lowered
            or "francais" in lowered
            or "français" in lowered
            or "fr_" in lowered
        )

    def _score(path: Path, in_docs: bool) -> int:
        name = path.name.lower()
        score = 0
        if "readme" in name:
            score += 50
        for key in keywords:
            if key in name:
                score += 10
        if mod_name and mod_name in name:
            score += 15
        if _lang_match(name):
            score += 12
        if lang and not lang.startswith("fr") and _is_french(name):
            score -= 15
        score += ext_rank.get(path.suffix.lower(), 0)
        if in_docs:
            score += 8
        if path.suffix.lower() in {".txt", ".md", ".rtf", ".html", ".htm"}:
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")[:32768].lower()
                if any(word in text for word in install_words):
                    score += 6
            except Exception:
                return score
        return score

    def _find_lang_dir(root: Path) -> Path | None:
        if not lang:
            return None
        if (root / lang).exists():
            return root / lang
        for entry in root.iterdir() if root.exists() else []:
            if entry.is_dir() and entry.name.lower() == lang:
                return entry
        return None

    docs_dirs = [mod_dir / "docs", mod_dir / "doc"]
    docs_candidates: list[tuple[Path, bool]] = []
    for docs_dir in docs_dirs:
        if not docs_dir.exists():
            continue
        for path in _iter_files(docs_dir):
            if not path.is_file():
                continue
            if path.suffix.lower() not in ext_rank:
                continue
            if path.name.lower() == "readme.txt":
                return path
            if "readme" in path.name.lower():
                docs_candidates.append((path, True))
    if docs_candidates:
        best_docs, _ = max(docs_candidates, key=lambda item: _score(*item))
        return best_docs

    search_dirs: list[Path] = []
    for docs_dir in docs_dirs:
        if docs_dir.exists():
            search_dirs.append(docs_dir)

    lang_dir = _find_lang_dir(mod_dir / "lang")
    if lang_dir:
        search_dirs.append(lang_dir)
    tra_dir = _find_lang_dir(mod_dir / "tra")
    if tra_dir:
        search_dirs.append(tra_dir)
    if lang:
        for entry in mod_dir.iterdir():
            if entry.is_dir() and entry.name.lower() == lang:
                search_dirs.append(entry)
                break
    for extra in (mod_dir / "docs", mod_dir / "doc", mod_dir / "readme"):
        if extra.exists():
            search_dirs.append(extra)
    search_dirs.append(mod_dir)

    candidates: list[tuple[Path, bool, int]] = []
    for index, folder in enumerate(search_dirs):
        in_docs = folder.name.lower() in {"doc", "docs"}
        for path in _iter_files(folder):
            if not path.is_file():
                continue
            if path.suffix.lower() not in ext_rank:
                continue
            if path.name.lower() == "readme.txt":
                return path
            candidates.append((path, in_docs, index))

    if not candidates:
        return None

    def _rank(item: tuple[Path, bool, int]) -> int:
        path, in_docs, order = item
        return _score(path, in_docs) + max(0, 10 - order)

    best_path, _best_docs, _ = max(candidates, key=_rank)
    return best_path
