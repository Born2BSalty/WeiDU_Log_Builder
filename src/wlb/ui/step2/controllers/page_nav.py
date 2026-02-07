from __future__ import annotations

from collections.abc import Callable


def go_back(on_back: Callable[[], None] | None) -> None:
    if on_back is not None:
        on_back()


def go_next(on_next: Callable[[], None] | None) -> None:
    if on_next is not None:
        on_next()
