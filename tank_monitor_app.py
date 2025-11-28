from datetime import datetime
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QStackedWidget,
    QPushButton,
)
from PyQt5.QtCore import QTimer, Qt
from widgets.sidebar import Sidebar
from sections.dashboard import DashboardSection
from sections.historial import HistorialSection
from sections.configuracion import ConfiguracionSection
from sections.alertas import AlertasSection
from sections.reportes import ReportesSection


class TankMonitorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TankMonitor Pro")
        self.setGeometry(50, 50, 1600, 950)
        self.historical_data = []
        self.current_section = 0
        self.setup_ui()
        self.setup_timers()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar(self)
        main_layout.addWidget(self.sidebar)

        # Main Content
        content_widget = QWidget()
        content_widget.setStyleSheet("background: #f8fafc;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Navbar
        navbar = self.create_navbar()
        content_layout.addWidget(navbar)

        # Stacked Widget for sections
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background: transparent;")

        # Create all sections
        self.dashboard_section = DashboardSection()
        self.historial_section = HistorialSection()
        self.config_section = ConfiguracionSection()
        self.alertas_section = AlertasSection()
        self.reportes_section = ReportesSection()

        self.stacked_widget.addWidget(self.dashboard_section)
        self.stacked_widget.addWidget(self.historial_section)
        self.stacked_widget.addWidget(self.config_section)
        self.stacked_widget.addWidget(self.alertas_section)
        self.stacked_widget.addWidget(self.reportes_section)

        content_layout.addWidget(self.stacked_widget)

        # Footer
        footer = self.create_footer()
        content_layout.addWidget(footer)
        main_layout.addWidget(content_widget)

    def create_navbar(self):
        navbar = QFrame()
        navbar.setStyleSheet(
            "QFrame { background: white; border-bottom: 1px solid #e2e8f0; }"
        )
        navbar.setFixedHeight(70)
        layout = QHBoxLayout(navbar)
        layout.setContentsMargins(30, 0, 30, 0)

        self.navbar_title = QLabel("Panel de Control Principal")
        self.navbar_title.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: #0f172a;"
        )
        layout.addWidget(self.navbar_title)
        layout.addStretch()

        self.time_label = QLabel()
        self.time_label.setStyleSheet(
            "color: #64748b; font-size: 13px; padding: 8px 16px; background: #f1f5f9; border-radius: 8px;"
        )
        layout.addWidget(self.time_label)

        user_btn = QPushButton("👤 Admin")
        user_btn.setStyleSheet(
            "QPushButton { background: #3b82f6; color: white; border: none; padding: 10px 20px; border-radius: 8px; font-size: 13px; font-weight: 600; } QPushButton:hover { background: #2563eb; }"
        )
        user_btn.setCursor(Qt.PointingHandCursor)
        layout.addWidget(user_btn)

        return navbar

    def create_footer(self):
        footer = QFrame()
        footer.setStyleSheet(
            "QFrame { background: white; border-top: 1px solid #e2e8f0; }"
        )
        footer.setFixedHeight(60)
        layout = QHBoxLayout(footer)
        layout.setContentsMargins(30, 0, 30, 0)

        copyright_label = QLabel(
            "© 2024 TankMonitor Pro | Sistema de Gestión y Monitoreo Inteligente de Nivel de Agua en Tanques Remotos"
        )
        copyright_label.setStyleSheet("color: #64748b; font-size: 12px;")
        layout.addWidget(copyright_label)
        layout.addStretch()

        status_label = QLabel(
            "🟢 Sistema Operativo | 📡 Arduino Conectado | 🗄️ MongoDB Activo"
        )
        status_label.setStyleSheet("color: #10b981; font-size: 12px; font-weight: 600;")
        layout.addWidget(status_label)

        return footer

    def setup_timers(self):
        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(1000)
        self.update_time()

    def update_time(self):
        current_time = datetime.now().strftime("%d/%m/%Y  %H:%M:%S")
        self.time_label.setText(f"🕐 {current_time}")

    def change_section(self, index):
        self.stacked_widget.setCurrentIndex(index)
        self.current_section = index
        titles = [
            "Panel de Control Principal",
            "Historial Completo",
            "Configuración del Sistema",
            "Centro de Alertas",
            "Generación de Reportes",
        ]
        self.navbar_title.setText(titles[index])
