from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QScrollArea,
    QPushButton,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor


class AlertasSection(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        self.setStyleSheet("border: none;")
        self.setup_ui()

    def setup_ui(self):
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        title = QLabel("🔔 Centro de Alertas")
        title.setStyleSheet(
            """
            font-size: 24px;
            font-weight: bold;
            color: #0f172a;
            margin-bottom: 20px;
        """
        )
        layout.addWidget(title)

        active_alerts_frame = QFrame()
        active_alerts_frame.setStyleSheet(
            """
            QFrame {
                background: white;
                border-radius: 16px;
                border: 1px solid #e2e8f0;
            }
        """
        )
        active_layout = QVBoxLayout(active_alerts_frame)
        active_layout.setContentsMargins(24, 20, 24, 20)

        active_title = QLabel("🚨 Alertas Activas")
        active_title.setStyleSheet(
            "font-size: 18px; font-weight: 600; color: #0f172a; margin-bottom: 15px;"
        )
        active_layout.addWidget(active_title)

        self.alerts_container = QVBoxLayout()
        self.alerts_container.setSpacing(10)

        sample_alerts = [
            {
                "tipo": "warning",
                "mensaje": "Nivel del tanque bajo (25%)",
                "timestamp": "14:30:22",
            },
            {
                "tipo": "info",
                "mensaje": "Sensor reconectado exitosamente",
                "timestamp": "14:25:10",
            },
        ]

        for alert in sample_alerts:
            alert_widget = self.create_alert_widget(
                alert["tipo"], alert["mensaje"], alert["timestamp"]
            )
            self.alerts_container.addWidget(alert_widget)

        no_alerts_label = QLabel("✅ No hay alertas críticas activas")
        no_alerts_label.setStyleSheet(
            """
            color: #059669;
            font-size: 14px;
            font-weight: 500;
            padding: 20px;
            text-align: center;
            background: #d1fae5;
            border-radius: 8px;
            border: 1px solid #a7f3d0;
        """
        )
        self.alerts_container.addWidget(no_alerts_label)

        active_layout.addLayout(self.alerts_container)
        layout.addWidget(active_alerts_frame)

        history_frame = QFrame()
        history_frame.setStyleSheet(
            """
            QFrame {
                background: white;
                border-radius: 16px;
                border: 1px solid #e2e8f0;
            }
        """
        )
        history_layout = QVBoxLayout(history_frame)
        history_layout.setContentsMargins(24, 20, 24, 20)

        history_title = QLabel("📋 Historial de Alertas (Últimas 24h)")
        history_title.setStyleSheet(
            "font-size: 18px; font-weight: 600; color: #0f172a; margin-bottom: 15px;"
        )
        history_layout.addWidget(history_title)

        stats_layout = QHBoxLayout()

        stats_cards = [
            {"valor": "3", "texto": "Alertas Totales", "color": "blue"},
            {"valor": "1", "texto": "Críticas", "color": "red"},
            {"valor": "2", "texto": "Advertencias", "color": "amber"},
            {"valor": "0", "texto": "Informativas", "color": "green"},
        ]

        for stat in stats_cards:
            stat_frame = QFrame()
            stat_frame.setStyleSheet(
                f"""
                QFrame {{
                    background: white;
                    border-radius: 12px;
                    border: 2px solid #e2e8f0;
                    padding: 15px;
                }}
            """
            )
            stat_layout = QVBoxLayout(stat_frame)

            valor_label = QLabel(stat["valor"])
            valor_label.setStyleSheet(
                f"""
                font-size: 24px;
                font-weight: bold;
                color: #0f172a;
                text-align: center;
            """
            )
            stat_layout.addWidget(valor_label)

            texto_label = QLabel(stat["texto"])
            texto_label.setStyleSheet(
                """
                font-size: 12px;
                color: #64748b;
                text-align: center;
            """
            )
            stat_layout.addWidget(texto_label)

            stats_layout.addWidget(stat_frame)

        history_layout.addLayout(stats_layout)

        history_list_layout = QVBoxLayout()
        history_list_layout.setSpacing(8)

        sample_history = [
            {
                "tipo": "warning",
                "mensaje": "Nivel bajo detectado: 22%",
                "timestamp": "14:30:22",
                "leida": True,
            },
            {
                "tipo": "info",
                "mensaje": "Sistema iniciado correctamente",
                "timestamp": "14:00:00",
                "leida": True,
            },
            {
                "tipo": "error",
                "mensaje": "Pérdida de conexión con sensor",
                "timestamp": "13:45:15",
                "leida": True,
            },
            {
                "tipo": "success",
                "mensaje": "Conexión restaurada",
                "timestamp": "13:50:30",
                "leida": True,
            },
        ]

        for alert in sample_history:
            history_item = self.create_history_item(
                alert["tipo"], alert["mensaje"], alert["timestamp"], alert["leida"]
            )
            history_list_layout.addWidget(history_item)

        history_layout.addLayout(history_list_layout)
        layout.addWidget(history_frame)

        config_frame = QFrame()
        config_frame.setStyleSheet(
            """
            QFrame {
                background: white;
                border-radius: 16px;
                border: 1px solid #e2e8f0;
            }
        """
        )
        config_layout = QVBoxLayout(config_frame)
        config_layout.setContentsMargins(24, 20, 24, 20)

        config_title = QLabel("⚙️ Configuración de Notificaciones")
        config_title.setStyleSheet(
            "font-size: 18px; font-weight: 600; color: #0f172a; margin-bottom: 15px;"
        )
        config_layout.addWidget(config_title)

        options_layout = QVBoxLayout()
        options_layout.setSpacing(12)

        notification_options = [
            "🔔 Alertas de nivel crítico (< 15%)",
            "⚠️ Alertas de nivel bajo (< 30%)",
            "🚨 Alertas de fugas detectadas",
            "📡 Alertas de desconexión de sensores",
            "💾 Alertas de error en base de datos",
        ]

        for option in notification_options:
            option_frame = QFrame()
            option_frame.setStyleSheet(
                """
                QFrame {
                    background: #f8fafc;
                    border-radius: 8px;
                    padding: 12px 16px;
                    border: 1px solid #e2e8f0;
                }
            """
            )
            option_layout = QHBoxLayout(option_frame)

            option_label = QLabel(option)
            option_label.setStyleSheet("font-size: 14px; color: #374151;")
            option_layout.addWidget(option_label)
            option_layout.addStretch()

            toggle_btn = QPushButton("Activado")
            toggle_btn.setStyleSheet(
                """
                QPushButton {
                    background: #10b981;
                    color: white;
                    border: none;
                    padding: 6px 12px;
                    border-radius: 6px;
                    font-size: 11px;
                    font-weight: 600;
                    min-width: 60px;
                }
                QPushButton:hover {
                    background: #059669;
                }
            """
            )
            toggle_btn.setCursor(Qt.PointingHandCursor)
            option_layout.addWidget(toggle_btn)

            options_layout.addWidget(option_frame)

        config_layout.addLayout(options_layout)
        layout.addWidget(config_frame)

        self.setWidget(content)

    def create_alert_widget(self, tipo, mensaje, timestamp):
        alert_frame = QFrame()

        colors = {
            "error": {"bg": "#fef2f2", "border": "#fecaca", "icon": "🔴"},
            "warning": {"bg": "#fffbeb", "border": "#fed7aa", "icon": "🟡"},
            "info": {"bg": "#eff6ff", "border": "#bfdbfe", "icon": "🔵"},
            "success": {"bg": "#f0fdf4", "border": "#bbf7d0", "icon": "🟢"},
        }

        config = colors.get(tipo, colors["info"])

        alert_frame.setStyleSheet(
            f"""
            QFrame {{
                background: {config['bg']};
                border-left: 4px solid {config['border']};
                border-radius: 8px;
                padding: 12px 16px;
            }}
        """
        )

        alert_layout = QHBoxLayout(alert_frame)

        icon_label = QLabel(config["icon"])
        icon_label.setStyleSheet("font-size: 16px;")
        alert_layout.addWidget(icon_label)

        message_label = QLabel(mensaje)
        message_label.setStyleSheet(
            "font-size: 14px; font-weight: 500; color: #1f2937;"
        )
        alert_layout.addWidget(message_label)

        alert_layout.addStretch()

        time_label = QLabel(timestamp)
        time_label.setStyleSheet("font-size: 12px; color: #6b7280;")
        alert_layout.addWidget(time_label)

        action_btn = QPushButton("Resolver")
        action_btn.setStyleSheet(
            """
            QPushButton {
                background: #3b82f6;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 11px;
                font-weight: 500;
                margin-left: 8px;
            }
            QPushButton:hover {
                background: #2563eb;
            }
        """
        )
        action_btn.setCursor(Qt.PointingHandCursor)
        alert_layout.addWidget(action_btn)

        return alert_frame

    def create_history_item(self, tipo, mensaje, timestamp, leida):
        item_frame = QFrame()
        item_frame.setStyleSheet(
            """
            QFrame {
                background: #f8fafc;
                border-radius: 6px;
                padding: 10px 12px;
                border: 1px solid #e2e8f0;
            }
        """
        )

        item_layout = QHBoxLayout(item_frame)

        status_icon = QLabel("✓" if leida else "●")
        status_icon.setStyleSheet(
            f"""
            font-size: 14px;
            color: {'#10b981' if leida else '#3b82f6'};
            font-weight: bold;
        """
        )
        item_layout.addWidget(status_icon)

        message_label = QLabel(mensaje)
        message_label.setStyleSheet("font-size: 13px; color: #374151;")
        item_layout.addWidget(message_label)

        item_layout.addStretch()

        time_label = QLabel(timestamp)
        time_label.setStyleSheet("font-size: 11px; color: #6b7280;")
        item_layout.addWidget(time_label)

        return item_frame
