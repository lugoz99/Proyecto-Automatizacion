from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class ReportesSection(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel("📁 Generación de Reportes")
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
            "Exporta reportes en PDF, Excel o CSV con estadísticas detalladas del sistema."
        )
        info.setStyleSheet("font-size: 14px; color: #64748b; padding: 20px;")
        info.setWordWrap(True)
        layout.addWidget(info)
        layout.addStretch()
