from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QPushButton,
    QComboBox,
)
from PyQt5.QtCore import Qt


class ConfiguracionSection(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        title = QLabel("⚙️ Configuración del Sistema")
        title.setStyleSheet(
            """
            font-size: 24px;
            font-weight: bold;
            color: #0f172a;
            margin-bottom: 20px;
        """
        )
        layout.addWidget(title)

        tank_config_frame = QFrame()
        tank_config_frame.setStyleSheet(
            """
            QFrame {
                background: white;
                border-radius: 16px;
                border: 1px solid #e2e8f0;
            }
        """
        )
        tank_layout = QVBoxLayout(tank_config_frame)
        tank_layout.setContentsMargins(24, 20, 24, 20)

        tank_title = QLabel("💧 Configuración del Tanque")
        tank_title.setStyleSheet(
            "font-size: 18px; font-weight: 600; color: #0f172a; margin-bottom: 15px;"
        )
        tank_layout.addWidget(tank_title)

        params_layout = QHBoxLayout()

        height_layout = QVBoxLayout()
        height_label = QLabel("Altura del Tanque (cm):")
        height_label.setStyleSheet(
            "font-size: 13px; color: #64748b; margin-bottom: 5px;"
        )
        height_layout.addWidget(height_label)

        height_value = QLabel("10.0 cm")
        height_value.setStyleSheet("font-size: 16px; font-weight: 600; color: #0f172a;")
        height_layout.addWidget(height_value)
        params_layout.addLayout(height_layout)

        dist_layout = QVBoxLayout()
        dist_label = QLabel("Distancia Sensor (cm):")
        dist_label.setStyleSheet("font-size: 13px; color: #64748b; margin-bottom: 5px;")
        dist_layout.addWidget(dist_label)

        dist_value = QLabel("3.0 cm")
        dist_value.setStyleSheet("font-size: 16px; font-weight: 600; color: #0f172a;")
        dist_layout.addWidget(dist_value)
        params_layout.addLayout(dist_layout)

        params_layout.addStretch()
        tank_layout.addLayout(params_layout)
        layout.addWidget(tank_config_frame)

        alerts_config_frame = QFrame()
        alerts_config_frame.setStyleSheet(
            """
            QFrame {
                background: white;
                border-radius: 16px;
                border: 1px solid #e2e8f0;
            }
        """
        )
        alerts_layout = QVBoxLayout(alerts_config_frame)
        alerts_layout.setContentsMargins(24, 20, 24, 20)

        alerts_title = QLabel("🔔 Configuración de Alertas")
        alerts_title.setStyleSheet(
            "font-size: 18px; font-weight: 600; color: #0f172a; margin-bottom: 15px;"
        )
        alerts_layout.addWidget(alerts_title)

        thresholds_layout = QHBoxLayout()

        low_layout = QVBoxLayout()
        low_label = QLabel("Alerta Nivel Bajo (%):")
        low_label.setStyleSheet("font-size: 13px; color: #64748b; margin-bottom: 5px;")
        low_layout.addWidget(low_label)

        low_combo = QComboBox()
        low_combo.addItems(["15%", "20%", "25%", "30%"])
        low_combo.setCurrentText("20%")
        low_combo.setStyleSheet(
            "padding: 8px 12px; border: 1px solid #e2e8f0; border-radius: 8px;"
        )
        low_layout.addWidget(low_combo)
        thresholds_layout.addLayout(low_layout)

        critical_layout = QVBoxLayout()
        critical_label = QLabel("Alerta Nivel Crítico (%):")
        critical_label.setStyleSheet(
            "font-size: 13px; color: #64748b; margin-bottom: 5px;"
        )
        critical_layout.addWidget(critical_label)

        critical_combo = QComboBox()
        critical_combo.addItems(["5%", "10%", "15%"])
        critical_combo.setCurrentText("10%")
        critical_combo.setStyleSheet(
            "padding: 8px 12px; border: 1px solid #e2e8f0; border-radius: 8px;"
        )
        critical_layout.addWidget(critical_combo)
        thresholds_layout.addLayout(critical_layout)

        thresholds_layout.addStretch()
        alerts_layout.addLayout(thresholds_layout)
        layout.addWidget(alerts_config_frame)

        actions_frame = QFrame()
        actions_frame.setStyleSheet(
            """
            QFrame {
                background: white;
                border-radius: 16px;
                border: 1px solid #e2e8f0;
            }
        """
        )
        actions_layout = QVBoxLayout(actions_frame)
        actions_layout.setContentsMargins(24, 20, 24, 20)

        actions_title = QLabel("🛠️ Acciones del Sistema")
        actions_title.setStyleSheet(
            "font-size: 18px; font-weight: 600; color: #0f172a; margin-bottom: 15px;"
        )
        actions_layout.addWidget(actions_title)

        buttons_layout = QHBoxLayout()

        reconnect_btn = QPushButton("🔄 Reconectar Arduino")
        reconnect_btn.setStyleSheet(
            """
            QPushButton {
                background: #dbeafe;
                color: #1e40af;
                border: 1px solid #93c5fd;
                padding: 12px 20px;
                border-radius: 8px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #bfdbfe;
                border-color: #60a5fa;
            }
        """
        )
        buttons_layout.addWidget(reconnect_btn)

        test_btn = QPushButton("🧪 Test Sensores")
        test_btn.setStyleSheet(
            """
            QPushButton {
                background: #fef3c7;
                color: #d97706;
                border: 1px solid #fcd34d;
                padding: 12px 20px;
                border-radius: 8px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #fde68a;
                border-color: #fbbf24;
            }
        """
        )
        buttons_layout.addWidget(test_btn)

        calibrate_btn = QPushButton("📐 Calibrar Sensores")
        calibrate_btn.setStyleSheet(
            """
            QPushButton {
                background: #dcfce7;
                color: #15803d;
                border: 1px solid #86efac;
                padding: 12px 20px;
                border-radius: 8px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #bbf7d0;
                border-color: #4ade80;
            }
        """
        )
        buttons_layout.addWidget(calibrate_btn)

        actions_layout.addLayout(buttons_layout)
        layout.addWidget(actions_frame)

        layout.addStretch()
