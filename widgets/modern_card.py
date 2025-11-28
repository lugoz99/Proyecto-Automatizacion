from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class ModernCard(QFrame):
    def __init__(self, title, value, subtitle="", icon="", color="blue", parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Box)
        self.setLineWidth(0)
        self.setStyleSheet(
            """
            ModernCard {
                background: white;
                border-radius: 16px;
                border: 1px solid #e2e8f0;
            }
            ModernCard:hover {
                border: 2px solid #cbd5e1;
            }
        """
        )
        self.setMinimumHeight(140)

        layout = QVBoxLayout()
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(8)

        header_layout = QHBoxLayout()
        if icon:
            icon_label = QLabel(icon)
            icon_label.setStyleSheet(
                f"""
                color: {self.get_color(color)};
                font-size: 32px;
                background: {self.get_color_light(color)};
                border-radius: 12px;
                padding: 8px;
                min-width: 56px;
                max-width: 56px;
                min-height: 56px;
                max-height: 56px;
            """
            )
            icon_label.setAlignment(Qt.AlignCenter)
            header_layout.addWidget(icon_label)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)

        title_label = QLabel(title)
        title_label.setStyleSheet(
            """
            color: #64748b;
            font-size: 13px;
            font-weight: 600;
            font-family: 'Segoe UI', Arial;
        """
        )
        text_layout.addWidget(title_label)

        self.value_label = QLabel(value)
        self.value_label.setStyleSheet(
            """
            color: #0f172a;
            font-size: 28px;
            font-weight: bold;
            font-family: 'Segoe UI', Arial;
        """
        )
        text_layout.addWidget(self.value_label)

        header_layout.addLayout(text_layout)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        if subtitle:
            self.subtitle_label = QLabel(subtitle)
            self.subtitle_label.setStyleSheet(
                """
                color: #94a3b8;
                font-size: 12px;
                font-family: 'Segoe UI', Arial;
            """
            )
            layout.addWidget(self.subtitle_label)

        self.setLayout(layout)

    def update_value(self, value):
        self.value_label.setText(value)

    def update_subtitle(self, subtitle):
        if hasattr(self, "subtitle_label"):
            self.subtitle_label.setText(subtitle)

    def get_color(self, color):
        colors = {
            "blue": "#3b82f6",
            "green": "#10b981",
            "red": "#ef4444",
            "amber": "#f59e0b",
            "purple": "#8b5cf6",
            "cyan": "#06b6d4",
        }
        return colors.get(color, "#3b82f6")

    def get_color_light(self, color):
        colors = {
            "blue": "#dbeafe",
            "green": "#d1fae5",
            "red": "#fee2e2",
            "amber": "#fef3c7",
            "purple": "#ede9fe",
            "cyan": "#cffafe",
        }
        return colors.get(color, "#dbeafe")
