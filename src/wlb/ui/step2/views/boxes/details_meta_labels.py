from __future__ import annotations

from PySide6.QtWidgets import QLabel


def build_details_meta_labels() -> tuple[QLabel, QLabel, QLabel, QLabel, QLabel, QLabel]:
    labels = _build_label_list(6)
    return (
        labels[0],
        labels[1],
        labels[2],
        labels[3],
        labels[4],
        labels[5],
    )


def _build_label_list(count: int) -> list[QLabel]:
    return [QLabel("-") for _ in range(count)]
