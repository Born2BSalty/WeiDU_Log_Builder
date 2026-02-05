from __future__ import annotations

from collections.abc import Callable


class SelectionOrderStore:
    def __init__(self) -> None:
        self._bgee: list[str] = []
        self._bg2ee: list[str] = []
        self._listeners: list[Callable[[], None]] = []

    def set_order(self, game: str, items: list[str]) -> None:
        if game == "BG2EE":
            self._bg2ee = items
        else:
            self._bgee = items
        self._notify()

    def get_order(self, game: str) -> list[str]:
        return list(self._bg2ee if game == "BG2EE" else self._bgee)

    def subscribe(self, listener: Callable[[], None]) -> None:
        self._listeners.append(listener)

    def _notify(self) -> None:
        for listener in self._listeners:
            listener()
