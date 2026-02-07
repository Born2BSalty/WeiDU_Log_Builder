from __future__ import annotations

from wlb.ui.step2.views.selection_ui import SelectionUi


def set_scan_started(ui: SelectionUi, scan_status_label) -> None:
    scan_status_label.setText("0/0")
    ui.progress_label.setText("Scanning...")


def set_scan_progress(
    ui: SelectionUi, scan_status_label, current: int, total: int, name: str
) -> None:
    if total > 0:
        scan_status_label.setText(f"{current}/{total}: {name}")
    ui.progress_label.setText("Scanning...")


def set_scan_finished(ui: SelectionUi, scan_status_label) -> None:
    ui.progress_label.setText("Scan complete.")
    scan_status_label.setText("Done")


def set_scan_failed(ui: SelectionUi, scan_status_label, message: str) -> None:
    ui.progress_label.setText("Scan failed.")
    scan_status_label.setText("Failed")
    ui.details_desc.setPlainText(message)


def set_readme_failed(ui: SelectionUi, scan_status_label, message: str) -> None:
    scan_status_label.setText("Readme scan failed")
    ui.details_desc.setPlainText(message)
