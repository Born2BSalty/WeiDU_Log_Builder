from __future__ import annotations

from wlb.infra.export.weidu_log_writer import WeiduLogWriter
from wlb.infra.fs.local_fs import LocalFs
from wlb.infra.install.terminal_installer import TerminalInstaller
from wlb.infra.process.subprocess_runner import SubprocessRunner
from wlb.infra.weidu.weidu_components import WeiduComponents
from wlb.services.export_service import ExportService
from wlb.services.install_service import InstallService
from wlb.services.scan_service import ScanService
from wlb.services.settings_service import SettingsService


def build_scan_service() -> ScanService:
    return ScanService(LocalFs(), WeiduComponents(SubprocessRunner()), workers=3)


def build_install_service() -> InstallService:
    return InstallService(TerminalInstaller())


def build_export_service() -> ExportService:
    return ExportService(WeiduLogWriter())


def build_settings_service() -> SettingsService:
    return SettingsService()