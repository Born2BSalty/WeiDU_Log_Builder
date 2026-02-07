from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import Signal

from wlb.services.install_service import InstallRequest
from wlb.services.settings_service import SettingsService
from wlb.ui.step5.controllers.input_controller import ConsoleInputController
from wlb.ui.step5.controllers.output_controller import InstallOutputController
from wlb.ui.step5.viewmodels.install_viewmodel import InstallViewModel
from wlb.ui.step5.views.boxes import build_footer_row
from wlb.ui.step5.views.install_layout import build_install_ui
from wlb.ui.widgets import PageScaffold


class InstallPage(PageScaffold):
    install_requested = Signal()
    output = Signal(str)

    def __init__(
        self,
        view_model: InstallViewModel,
        settings: SettingsService,
        on_back: Callable[[], None] | None = None,
    ) -> None:
        super().__init__(
            title="Step 5: Installation & Progress",
            subtitle="Run installation and track progress.",
        )
        self._on_back = on_back
        self._view_model = view_model
        self._settings = settings
        self.output.connect(self._append_output)

        ui = build_install_ui()
        ui.start_button.clicked.connect(self.install_requested.emit)
        ui.cancel_button.clicked.connect(self._on_cancel)
        self.body_layout.addWidget(ui.root)

        button_row, back_button, exit_button = build_footer_row()
        back_button.clicked.connect(self._handle_back)
        exit_button.clicked.connect(self._handle_exit)
        self.footer_layout.addWidget(button_row)

        self._output_controller = InstallOutputController(
            ui.io_view, ui.minimal_checkbox, settings, self._input_buffer
        )
        self._input_controller = ConsoleInputController(
            ui.io_view,
            ui.input_line,
            self._view_model,
            self.output.emit,
            self._output_controller.filter_state,
        )

    def _handle_back(self) -> None:
        if self._on_back is not None:
            self._on_back()

    def _handle_exit(self) -> None:
        self.window().close()

    def _on_cancel(self) -> None:
        self._view_model.cancel()

    def start_install(self, request: InstallRequest) -> None:
        self._output_controller.reset()
        self._input_controller.reset()

        def _on_output(text: str) -> None:
            self.output.emit(text)

        def _on_exit(code: int) -> None:
            self.output.emit(f"\n[EXIT] code {code}\n")
            self._output_controller.close()

        self._view_model.start(request, _on_output, _on_exit)

    def _append_output(self, text: str) -> None:
        self._output_controller.append(text)

    def _input_buffer(self) -> str:
        return self._input_controller.current_buffer()
