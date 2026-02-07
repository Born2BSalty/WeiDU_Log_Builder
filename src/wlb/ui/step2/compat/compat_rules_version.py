from __future__ import annotations


def version_ok(current: str | None, minimum: str) -> bool:
    if not current:
        return False
    return _version_tuple(current) >= _version_tuple(minimum)


def _version_tuple(value: str) -> tuple[int, ...]:
    result: list[int] = []
    for part in value.split("."):
        try:
            result.append(int(part))
        except ValueError:
            break
    return tuple(result)
