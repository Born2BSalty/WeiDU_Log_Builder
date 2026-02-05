from __future__ import annotations

import os
import subprocess
import sys
import threading
from collections.abc import Callable
from contextlib import suppress
from pathlib import Path

from wlb.infra.install.subprocess_installer import SubprocessInstaller
from wlb.ports.install_port import InstallPort


class TerminalInstaller(InstallPort):
    def __init__(self) -> None:
        self._fallback = SubprocessInstaller()
        self._process: subprocess.Popen[bytes] | None = None
        self._lock = threading.Lock()
        self._reader_stop = threading.Event()
        self._master_fd: int | None = None

    def start(
        self,
        argv: list[str],
        cwd: Path | None,
        env: dict[str, str] | None,
        on_output: Callable[[str], None],
        on_exit: Callable[[int], None],
    ) -> None:
        if os.name == "nt":
            if not _try_winpty(argv, cwd, env, on_output, on_exit, self._lock):
                self._fallback.start(argv, cwd, env, on_output, on_exit)
            return
        self._start_posix(argv, cwd, env, on_output, on_exit)

    def send_input(self, text: str) -> None:
        if os.name == "nt":
            self._fallback.send_input(text)
            return
        with self._lock:
            master_fd = self._master_fd
        if master_fd is None:
            return
        try:
            os.write(master_fd, text.encode(errors="ignore"))
        except Exception:
            return

    def cancel(self) -> None:
        if os.name == "nt":
            self._fallback.cancel()
            return
        with self._lock:
            proc = self._process
            self._reader_stop.set()
        if proc is None:
            return
        try:
            proc.terminate()
            proc.wait(timeout=5)
        except Exception:
            with suppress(Exception):
                proc.kill()

    def _start_posix(
        self,
        argv: list[str],
        cwd: Path | None,
        env: dict[str, str] | None,
        on_output: Callable[[str], None],
        on_exit: Callable[[int], None],
    ) -> None:
        with self._lock:
            if self._process is not None:
                return
            self._reader_stop.clear()
        if not hasattr(os, "openpty"):
            self._fallback.start(argv, cwd, env, on_output, on_exit)
            return
        master_fd, slave_fd = os.openpty()
        try:
            proc = subprocess.Popen(
                argv,
                cwd=str(cwd) if cwd else None,
                env=env,
                stdin=slave_fd,
                stdout=slave_fd,
                stderr=slave_fd,
                close_fds=True,
            )
        finally:
            with suppress(Exception):
                os.close(slave_fd)
        with self._lock:
            self._process = proc
            self._master_fd = master_fd
        on_output(f"Process started (pid {proc.pid})")
        reader = threading.Thread(target=self._read_loop, args=(master_fd, on_output), daemon=True)
        reader.start()

        def _waiter() -> None:
            code = proc.wait()
            self._reader_stop.set()
            reader.join(timeout=1)
            with self._lock:
                self._process = None
                self._master_fd = None
            on_exit(code)
            with suppress(Exception):
                os.close(master_fd)

        threading.Thread(target=_waiter, daemon=True).start()

    def _read_loop(self, master_fd: int, on_output: Callable[[str], None]) -> None:
        while not self._reader_stop.is_set():
            try:
                data = os.read(master_fd, 4096)
                if not data:
                    break
                on_output(data.decode(errors="ignore"))
            except Exception:
                break


def _try_winpty(
    argv: list[str],
    cwd: Path | None,
    env: dict[str, str] | None,
    on_output: Callable[[str], None],
    on_exit: Callable[[int], None],
    lock: threading.Lock,
) -> bool:
    _ensure_winpty_path()
    try:
        import winpty  # type: ignore
    except Exception:
        return False
    try:
        with lock:
            pass
        proc = winpty.PTYProcess.spawn(
            argv,
            cwd=str(cwd) if cwd else None,
            env=env,
        )
    except Exception:
        return False

    def _reader() -> None:
        try:
            while True:
                chunk = proc.read(4096)
                if not chunk:
                    break
                on_output(chunk)
        except Exception:
            return

    def _waiter() -> None:
        code = proc.wait()
        on_exit(code)

    on_output("Process started (PTY)")
    threading.Thread(target=_reader, daemon=True).start()
    threading.Thread(target=_waiter, daemon=True).start()
    return True


def _ensure_winpty_path() -> None:
    if sys.platform != "win32":
        return
    root = Path(__file__).resolve().parents[4]
    winpty_dir = root / "bin" / "winpty"
    if not winpty_dir.exists():
        return
    os.environ["PATH"] = f"{winpty_dir}{os.pathsep}{os.environ.get('PATH', '')}"
    try:
        os.add_dll_directory(str(winpty_dir))
    except Exception:
        return