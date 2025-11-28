from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class AlertasSection(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel("🔔 Centro de Alertas")
        title.setStyleSheet(
            """
            font-size: 24px;
            font-weight: bold;
            color: #0f172a;
            font-family: 'Segoe UI', Arial;
            margin-bottom: 20px;
        """
        )
        layout.addWidget(title)

        info = QLabel(
            "Configuración de notificaciones, alertas de nivel crítico, detección de fugas y más."
        )
        info.setStyleSheet("font-size: 14px; color: #64748b; padding: 20px;")
        info.setWordWrap(True)
        layout.addWidget(info)
        layout.addStretch()
