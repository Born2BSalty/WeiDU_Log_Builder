from __future__ import annotations

from PySide6.QtWidgets import QMainWindow, QStackedWidget

from wlb.app.composition_root import (
    build_export_service,
    build_install_service,
    build_scan_service,
    build_settings_service,
)
from wlb.services.install_request_builder import InstallRequestBuilder
from wlb.ui.step1.setup_page import SetupPage
from wlb.ui.step2.select_page import SelectPage
from wlb.ui.step2.selection_store import SelectionOrderStore
from wlb.ui.step3.order_page import OrderPage
from wlb.ui.step4.review_page import ReviewPage
from wlb.ui.step4.review_viewmodel import ReviewViewModel
from wlb.ui.step5.install_page import InstallPage
from wlb.ui.step5.install_viewmodel import InstallViewModel


class WizardWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("WeiDU Wizard")

        self._stack = QStackedWidget()
        self._store = SelectionOrderStore()
        scan_service = build_scan_service()
        install_service = build_install_service()
        export_service = build_export_service()
        settings_service = build_settings_service()
        install_view_model = InstallViewModel(install_service)
        review_view_model = ReviewViewModel(settings_service, self._store, export_service)
        self._install_request_builder = InstallRequestBuilder(settings_service, self._store)
        self._settings = settings_service
        self._setup_page = SetupPage(on_next=self._go_next)
        self._select_page = SelectPage(
            self._store,
            settings_service,
            on_back=self._go_back,
            on_next=self._go_next,
            scan_service=scan_service,
        )
        self._order_page = OrderPage(
            self._store,
            settings_service,
            on_back=self._go_back,
            on_next=self._go_next,
        )
        self._review_page = ReviewPage(
            review_view_model,
            on_back=self._go_back,
            on_next=self._go_next,
        )
        self._install_page = InstallPage(install_view_model, on_back=self._go_back)
        self._install_page.install_requested.connect(self._on_install_requested)

        self._stack.addWidget(self._setup_page)
        self._stack.addWidget(self._select_page)
        self._stack.addWidget(self._order_page)
        self._stack.addWidget(self._review_page)
        self._stack.addWidget(self._install_page)
        self.setCentralWidget(self._stack)
        self.resize(1280, 780)
        self._apply_page_size()

    def _go_next(self) -> None:
        if self._skip_to_install():
            index = self._stack.count() - 1
        else:
            index = min(self._stack.currentIndex() + 1, self._stack.count() - 1)
        self._stack.setCurrentIndex(index)
        self._apply_page_size()

    def _go_back(self) -> None:
        index = 0 if self._skip_to_setup() else max(self._stack.currentIndex() - 1, 0)
        self._stack.setCurrentIndex(index)
        self._apply_page_size()

    def _apply_page_size(self) -> None:
        self.resize(1280, 780)

    def showEvent(self, event) -> None:  # type: ignore[override]
        super().showEvent(event)
        self._apply_page_size()

    def _skip_to_install(self) -> bool:
        if not self._settings.has_logs():
            return False
        return self._stack.currentIndex() in (0, 1, 2, 3)

    def _skip_to_setup(self) -> bool:
        if not self._settings.has_logs():
            return False
        return self._stack.currentIndex() == self._stack.count() - 1

    def _on_install_requested(self) -> None:
        request = self._install_request_builder.build()
        self._stack.setCurrentIndex(self._stack.count() - 1)
        self._apply_page_size()
        self._install_page.start_install(request)
