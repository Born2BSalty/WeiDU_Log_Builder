from __future__ import annotations

from pathlib import Path


class WeiduLogWriter:
    def write(self, folder: Path, lines: list[str]) -> None:
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / "weidu.log"
        content = "\n".join(lines) + ("\n" if lines else "")
        path.write_text(content, encoding="utf-8")
