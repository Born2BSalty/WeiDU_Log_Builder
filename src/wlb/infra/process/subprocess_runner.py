from __future__ import annotations

import subprocess
from pathlib import Path

from wlb.ports.process_port import ProcessPort, ProcessResult


class SubprocessRunner(ProcessPort):
    def run(self, args: list[str], cwd: Path | None = None) -> ProcessResult:
        proc = subprocess.run(
            args,
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            check=False,
        )
        return ProcessResult(
            stdout=proc.stdout,
            stderr=proc.stderr,
            returncode=proc.returncode,
        )
