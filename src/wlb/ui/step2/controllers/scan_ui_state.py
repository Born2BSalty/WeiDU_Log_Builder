from __future__ import annotations

from wlb.ui.step2.views.selection_ui import SelectionUi


def set_scanning(ui: SelectionUi) -> None:
    ui.scan_button.setEnabled(False)
    ui.cancel_scan_button.setEnabled(True)
    ui.progress_label.setText("Scanning...")


def set_idle(ui: SelectionUi) -> None:
    ui.scan_button.setEnabled(True)
    ui.cancel_scan_button.setEnabled(False)
