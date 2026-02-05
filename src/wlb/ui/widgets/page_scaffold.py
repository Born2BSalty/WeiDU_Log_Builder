from __future__ import annotations

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from wlb.ui.style import metrics


class PageScaffold(QWidget):
    def __init__(self, title: str, subtitle: str | None = None) -> None:
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            metrics.PAGE_MARGIN,
            metrics.PAGE_MARGIN,
            metrics.PAGE_MARGIN,
            metrics.PAGE_MARGIN,
        )
        layout.setSpacing(metrics.SECTION_SPACING)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("PageTitle")
        layout.addWidget(self.title_label)

        if subtitle:
            self.subtitle_label = QLabel(subtitle)
            self.subtitle_label.setObjectName("PageSubtitle")
            layout.addSpacing(metrics.HEADER_BOTTOM_SPACING)
            layout.addWidget(self.subtitle_label)
        else:
            self.subtitle_label = None

        self.body = QWidget()
        self.body_layout = QVBoxLayout(self.body)
        self.body_layout.setSpacing(metrics.SECTION_SPACING)
        layout.addWidget(self.body, 1)

        self.footer = QWidget()
        self.footer_layout = QVBoxLayout(self.footer)
        self.footer_layout.setSpacing(metrics.BUTTON_ROW_SPACING)
        layout.addWidget(self.footer)
