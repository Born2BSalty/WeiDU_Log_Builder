from __future__ import annotations

import subprocess
import threading
import time
from collections.abc import Callable
from contextlib import suppress
from pathlib import Path

from wlb.ports.install_port import InstallPort


class SubprocessInstaller(InstallPort):
    def __init__(self) -> None:
        self._running = False
        self._process: subprocess.Popen[str] | None = None
        self._lock = threading.Lock()
        self._tail_stop = threading.Event()

    def start(
        self,
        argv: list[str],
        cwd: Path | None,
        env: dict[str, str] | None,
        on_output: Callable[[str], None],
        on_exit: Callable[[int], None],
    ) -> None:
        with self._lock:
            if self._running:
                return
            self._running = True
            self._tail_stop.clear()
        on_output(f"Command: {self._format_command(argv)}")

        def _run() -> None:
            try:
                out_path = (cwd or Path.cwd()) / ".wlb_install_out.txt"
                with out_path.open("w", encoding="utf-8", errors="ignore") as out_file:
                    self._process = subprocess.Popen(
                        argv,
                        cwd=str(cwd) if cwd else None,
                        env=env,
                        stdin=subprocess.PIPE,
                        stdout=out_file,
                        stderr=subprocess.STDOUT,
                        text=True,
                        bufsize=1,
                    )
                    process = self._process
                    on_output(f"Process started (pid {process.pid})")
                    tail_thread = threading.Thread(
                        target=self._tail_file,
                        args=(out_path, on_output, self._tail_stop),
                        daemon=True,
                    )
                    tail_thread.start()
                    returncode = process.wait()
                    self._tail_stop.set()
                    tail_thread.join(timeout=1)
                with suppress(Exception):
                    out_path.unlink()
                on_exit(returncode)
            except Exception as exc:
                on_output(f"Installer failed: {exc}")
                on_exit(1)
            finally:
                with self._lock:
                    self._running = False
                self._process = None

        threading.Thread(target=_run, daemon=True).start()

    def cancel(self) -> None:
        with self._lock:
            proc = self._process
            self._tail_stop.set()
        if proc is None:
            return
        try:
            proc.terminate()
            proc.wait(timeout=5)
        except Exception:
            with suppress(Exception):
                proc.kill()

    def send_input(self, text: str) -> None:
        with self._lock:
            proc = self._process
        if proc is None or proc.stdin is None:
            return
        try:
            proc.stdin.write(text)
            proc.stdin.flush()
        except Exception:
            return

    @staticmethod
    def _format_command(argv: list[str]) -> str:
        def _quote(arg: str) -> str:
            return f'"{arg}"' if " " in arg or "\t" in arg else arg

        return " ".join(_quote(arg) for arg in argv)

    @staticmethod
    def _tail_file(path: Path, on_output: Callable[[str], None], stop: threading.Event) -> None:
        pos = 0
        while not stop.is_set():
            try:
                with path.open("r", encoding="utf-8", errors="ignore") as handle:
                    handle.seek(pos)
                    chunk = handle.read()
                    if chunk:
                        on_output(chunk)
                        pos = handle.tell()
            except FileNotFoundError:
                return
            except Exception:
                time.sleep(0.05)
                continue
            time.sleep(0.05)