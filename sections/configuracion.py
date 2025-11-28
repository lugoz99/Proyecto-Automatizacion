from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt


class ConfiguracionSection(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel("⚙️ Configuración del Sistema")
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

        # Config frame
        config_frame = QFrame()
        config_frame.setStyleSheet(
            """
            QFrame {
                background: white;
                border-radius: 16px;
                border: 1px solid #e2e8f0;
                padding: 24px;
            }
        """
        )
        config_layout = QVBoxLayout(config_frame)

        config_info = QLabel(
            """
            <h3 style="color: #0f172a; margin-bottom: 16px;">🔧 Información del Sistema</h3>
            <p style="margin: 8px 0;"><b>Estado:</b> <span style="color: #10b981;">🟢 Conectado</span></p>
            <p style="margin: 8px 0;"><b>Puerto Arduino:</b> COM5 @ 115200 bauds</p>
            <p style="margin: 8px 0;"><b>Sensor:</b> HC-SR04 Ultrasónico</p>
            <p style="margin: 8px 0;"><b>Base de datos:</b> MongoDB Local</p>
            <p style="margin: 8px 0;"><b>Intervalo de actualización:</b> 2000ms (2 segundos)</p>
            <p style="margin: 8px 0;"><b>Capacidad del tanque:</b> 20 cm (100%)</p>
            <p style="margin: 8px 0;"><b>Umbral de alerta:</b> 20% (Nivel bajo)</p>
        """
        )
        config_info.setStyleSheet("font-size: 14px; color: #475569; line-height: 1.6;")
        config_info.setWordWrap(True)
        config_layout.addWidget(config_info)

        layout.addWidget(config_frame)
        layout.addStretch()
