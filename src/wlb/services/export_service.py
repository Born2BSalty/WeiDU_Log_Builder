from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from wlb.infra.export.weidu_log_writer import WeiduLogWriter


@dataclass(frozen=True)
class ExportTarget:
    folder: Path
    lines: list[str]


@dataclass(frozen=True)
class ExportRequest:
    targets: list[ExportTarget]


class ExportService:
    def __init__(self, writer: WeiduLogWriter) -> None:
        self._writer = writer

    def export(self, request: ExportRequest) -> None:
        for target in request.targets:
            self._writer.write(target.folder, target.lines)
