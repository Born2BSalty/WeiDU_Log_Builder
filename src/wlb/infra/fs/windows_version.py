from __future__ import annotations

import sys
from pathlib import Path
from typing import NamedTuple


class FileVersion(NamedTuple):
    major: int
    minor: int
    build: int
    revision: int


def read_exe_version(exe_path: Path) -> FileVersion | None:
    if sys.platform != "win32":
        return None
    try:
        import ctypes
    except Exception:
        return None
    try:
        size = ctypes.windll.version.GetFileVersionInfoSizeW(str(exe_path), None)
        if size == 0:
            return None
        buf = ctypes.create_string_buffer(size)
        if not ctypes.windll.version.GetFileVersionInfoW(str(exe_path), 0, size, buf):
            return None
        lptr = ctypes.c_void_p()
        lsize = ctypes.c_uint()
        if not ctypes.windll.version.VerQueryValueW(
            buf, "\\", ctypes.byref(lptr), ctypes.byref(lsize)
        ):
            return None

        class VS_FIXEDFILEINFO(ctypes.Structure):
            _fields_ = [
                ("dwSignature", ctypes.c_uint32),
                ("dwStrucVersion", ctypes.c_uint32),
                ("dwFileVersionMS", ctypes.c_uint32),
                ("dwFileVersionLS", ctypes.c_uint32),
                ("dwProductVersionMS", ctypes.c_uint32),
                ("dwProductVersionLS", ctypes.c_uint32),
                ("dwFileFlagsMask", ctypes.c_uint32),
                ("dwFileFlags", ctypes.c_uint32),
                ("dwFileOS", ctypes.c_uint32),
                ("dwFileType", ctypes.c_uint32),
                ("dwFileSubtype", ctypes.c_uint32),
                ("dwFileDateMS", ctypes.c_uint32),
                ("dwFileDateLS", ctypes.c_uint32),
            ]

        if not lptr.value:
            return None
        info = VS_FIXEDFILEINFO.from_address(lptr.value)
        major = info.dwFileVersionMS >> 16
        minor = info.dwFileVersionMS & 0xFFFF
        build = info.dwFileVersionLS >> 16
        revision = info.dwFileVersionLS & 0xFFFF
        return FileVersion(major, minor, build, revision)
    except Exception:
        return None


def detect_game_version(game_dir: Path) -> str | None:
    exe_path = _find_game_exe(game_dir)
    if exe_path is None:
        return None
    version = read_exe_version(exe_path)
    if version is None:
        return None
    return f"{version.major}.{version.minor}.{version.build}.{version.revision}"


def _find_game_exe(game_dir: Path) -> Path | None:
    if not game_dir.exists():
        return None
    preferred = ["Baldur.exe", "BGMain.exe", "Baldur's Gate.exe"]
    for name in preferred:
        candidate = game_dir / name
        if candidate.exists():
            return candidate
    for path in game_dir.glob("*.exe"):
        if path.is_file():
            return path
    return None