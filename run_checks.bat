@echo off
setlocal
cd /d %~dp0

uv run pytest
uv run ruff check src
uv run ruff format src
uv run mypy src/wlb/infra src/wlb/services

endlocal
