import sys
import time
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
    QApplication,
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont

from widgets.sidebar import Sidebar
from serial_handler.arduino_reader import ArduinoReader
from database.mongo_manager import MongoDBManager
from sections.dashboard import DashboardSection
from sections.historial import HistorialSection
from sections.configuracion import ConfiguracionSection
from sections.alertas import AlertasSection
from sections.reportes import ReportesSection


class TankMonitorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(
            "Sistema de Gestión y Monitoreo Inteligente de Nivel de Agua"
        )
        self.setGeometry(50, 50, 1600, 950)

        self.serial_reader = None
        self.db_manager = MongoDBManager()
        self.current_section = 0
        self.current_data = None

        # Control de guardado cada 5 minutos
        self.last_save_time = 0
        self.save_interval = 300  # 5 minutos en segundos

        # 🆕 Contador de lecturas para debug
        self.lecturas_recibidas = 0
        self.lecturas_validas = 0

        self.setup_ui()
        self.setup_serial()
        self.setup_timers()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = Sidebar(self)
        main_layout.addWidget(self.sidebar)

        content_widget = QWidget()
        content_widget.setStyleSheet("background: #f8fafc;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        navbar = self.create_navbar()
        content_layout.addWidget(navbar)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background: transparent;")

        self.dashboard_section = DashboardSection(self)
        self.historial_section = HistorialSection(self)
        self.config_section = ConfiguracionSection()
        self.alertas_section = AlertasSection()
        self.reportes_section = ReportesSection()

        self.stacked_widget.addWidget(self.dashboard_section)
        self.stacked_widget.addWidget(self.historial_section)
        self.stacked_widget.addWidget(self.config_section)
        self.stacked_widget.addWidget(self.alertas_section)
        self.stacked_widget.addWidget(self.reportes_section)

        content_layout.addWidget(self.stacked_widget)

        footer = self.create_footer()
        content_layout.addWidget(footer)
        main_layout.addWidget(content_widget)

    def setup_serial(self):
        """Configura la conexión serial con el Arduino"""
        try:
            # 🔧 CAMBIADO: baudrate 115200 → 9600
            self.serial_reader = ArduinoReader(port="COM5", baudrate=9600)
            self.serial_reader.data_received.connect(self.handle_serial_data)
            self.serial_reader.start()
            print("✅ Arduino conectado correctamente en COM5 @ 9600 baud")
        except Exception as e:
            print(f"❌ Error inicializando Arduino: {e}")
            # 🆕 Actualizar UI para mostrar error
            self.connection_status.setText("🔴 Arduino Desconectado")
            self.connection_status.setStyleSheet(
                "color: #ef4444; font-size: 13px; padding: 8px 16px; "
                "background: #fee2e2; border-radius: 8px;"
            )

    def handle_serial_data(self, data):
        """Maneja los datos recibidos del Arduino"""
        try:
            self.current_data = data
            self.lecturas_recibidas += 1

            # 🆕 Verificar si la lectura es válida
            es_valida = data.get("valido", 0) == 1
            if es_valida:
                self.lecturas_validas += 1

            # 🆕 LÓGICA MEJORADA: Guardar solo cada 5 minutos Y si es válida
            current_time = time.time()
            if current_time - self.last_save_time >= self.save_interval:
                if self.db_manager and es_valida:  # Solo guardar si es válida
                    self.db_manager.save_reading(data)
                    self.last_save_time = current_time
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    print(
                        f"💾 [BD] Guardado - {timestamp} | "
                        f"Nivel: {data.get('nivel', 0):.1f}m ({data.get('porcentaje', 0):.0f}%)"
                    )
                elif not es_valida:
                    print(f"⚠️ [BD] Guardado omitido - Lectura inválida")
                    self.last_save_time = current_time  # Resetear timer

            # 🆕 Log cada 10 lecturas
            if self.lecturas_recibidas % 10 == 0:
                tasa_exito = (self.lecturas_validas / self.lecturas_recibidas) * 100
                print(
                    f"📊 Estadísticas: {self.lecturas_validas}/{self.lecturas_recibidas} "
                    f"válidas ({tasa_exito:.1f}%)"
                )

            # La UI siempre se actualiza en tiempo real
            if self.current_section == 0:
                self.dashboard_section.update_with_real_data(data)
            elif self.current_section == 1:
                self.historial_section.add_reading(data)

            # 🆕 Actualizar estado de conexión
            self.update_connection_status(data)

        except Exception as e:
            print(f"❌ Error procesando datos serial: {e}")
            import traceback

            traceback.print_exc()

    def update_connection_status(self, data):
        """Actualiza el indicador de estado de conexión"""
        try:
            es_valida = data.get("valido", 0) == 1

            if es_valida:
                self.connection_status.setText("🟢 Arduino Conectado")
                self.connection_status.setStyleSheet(
                    "color: #10b981; font-size: 13px; padding: 8px 16px; "
                    "background: #f1f5f9; border-radius: 8px;"
                )
                self.system_status.setText(
                    f"🟢 Monitoreo Activo | 📡 Sensor OK | "
                    f"💧 Nivel: {data.get('porcentaje', 0):.0f}%"
                )
            else:
                self.connection_status.setText("⚠️ Sensor Sin Datos")
                self.connection_status.setStyleSheet(
                    "color: #f59e0b; font-size: 13px; padding: 8px 16px; "
                    "background: #fef3c7; border-radius: 8px;"
                )
                self.system_status.setText(
                    "⚠️ Sensor Sin Lectura | 📡 Arduino OK | 💧 Tanque Remoto"
                )
        except Exception as e:
            print(f"Error actualizando estado: {e}")

    def create_navbar(self):
        navbar = QFrame()
        navbar.setStyleSheet(
            "QFrame { background: white; border-bottom: 1px solid #e2e8f0; }"
        )
        navbar.setFixedHeight(70)
        layout = QHBoxLayout(navbar)
        layout.setContentsMargins(30, 0, 30, 0)

        self.navbar_title = QLabel("Monitoreo en Tiempo Real")
        self.navbar_title.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: #0f172a;"
        )
        layout.addWidget(self.navbar_title)
        layout.addStretch()

        self.connection_status = QLabel("🔵 Inicializando...")
        self.connection_status.setStyleSheet(
            "color: #64748b; font-size: 13px; padding: 8px 16px; "
            "background: #f1f5f9; border-radius: 8px;"
        )
        layout.addWidget(self.connection_status)

        self.time_label = QLabel()
        self.time_label.setStyleSheet(
            "color: #64748b; font-size: 13px; padding: 8px 16px; "
            "background: #f1f5f9; border-radius: 8px;"
        )
        layout.addWidget(self.time_label)

        user_btn = QPushButton("👤 Operador")
        user_btn.setStyleSheet(
            """
            QPushButton {
                background: #3b82f6;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #2563eb;
            }
        """
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
            "© 2024 Sistema de Gestión y Monitoreo Inteligente | Tanques Remotos"
        )
        copyright_label.setStyleSheet("color: #64748b; font-size: 12px;")
        layout.addWidget(copyright_label)
        layout.addStretch()

        self.system_status = QLabel("🔵 Inicializando Sistema...")
        self.system_status.setStyleSheet(
            "color: #64748b; font-size: 12px; font-weight: 600;"
        )
        layout.addWidget(self.system_status)

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
            "Monitoreo en Tiempo Real",
            "Historial de Lecturas",
            "Configuración",
            "Alertas del Sistema",
            "Reportes",
        ]
        self.navbar_title.setText(titles[index])

        if index == 1:
            self.historial_section.load_historical_data()

    def closeEvent(self, event):
        """Cierre limpio de la aplicación"""
        print("\n🔌 Cerrando aplicación...")

        if self.serial_reader:
            print("   → Deteniendo lectura serial...")
            self.serial_reader.stop()

        if self.db_manager:
            print("   → Cerrando conexión BD...")
            self.db_manager.close()

        # 🆕 Mostrar estadísticas finales
        if self.lecturas_recibidas > 0:
            tasa_exito = (self.lecturas_validas / self.lecturas_recibidas) * 100
            print(f"\n📊 Resumen de sesión:")
            print(f"   • Lecturas totales: {self.lecturas_recibidas}")
            print(f"   • Lecturas válidas: {self.lecturas_validas} ({tasa_exito:.1f}%)")

        print("✅ Aplicación cerrada correctamente\n")
        event.accept()
