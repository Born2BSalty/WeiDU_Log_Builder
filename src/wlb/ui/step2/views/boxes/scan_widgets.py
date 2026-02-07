from __future__ import annotations

from PySide6.QtWidgets import QLabel, QPushButton


def build_scan_widgets() -> tuple[QPushButton, QPushButton, QLabel]:
    scan_button = QPushButton("Scan Mods Folder")
    cancel_scan_button = QPushButton("Cancel Scan")
    progress_label = QLabel("Idle")
    return scan_button, cancel_scan_button, progress_label
