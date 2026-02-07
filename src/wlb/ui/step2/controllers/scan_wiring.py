from __future__ import annotations

from wlb.services.scan_service import ScanService
from wlb.services.settings_service import SettingsService
from wlb.ui.step2.compat.select_missing import MissingFilesReporter
from wlb.ui.step2.controllers.readme_lookup import ReadmeLookup
from wlb.ui.step2.controllers.scan_flow import ScanFlow
from wlb.ui.step2.models.selection_store import SelectionOrderStore
from wlb.ui.step2.views.selection_ui import SelectionUi


def build_scan_flow(
    ui: SelectionUi,
    settings: SettingsService,
    store: SelectionOrderStore,
    reporter: MissingFilesReporter,
    scan_service: ScanService | None,
    scan_status_label,
) -> tuple[ScanFlow, ReadmeLookup]:
    readme_lookup = ReadmeLookup(
        scan_service,
        lambda _tp2, _readme: None,
        lambda _msg: None,
    )
    scan_flow = ScanFlow(
        ui,
        settings,
        store,
        reporter,
        readme_lookup,
        scan_status_label,
    )
    readme_lookup = ReadmeLookup(
        scan_service,
        scan_flow.apply_readme,
        scan_flow.on_readme_failed,
    )
    scan_flow.set_readme_lookup(readme_lookup)
    return scan_flow, readme_lookup
