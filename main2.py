import sys
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QScrollArea,
    QStackedWidget,
)
from PyQt5.QtCore import (
    QTimer,
    Qt,
    QPropertyAnimation,
    QEasingCurve,
    pyqtProperty,
    QMargins,
)
from PyQt5.QtGui import (
    QFont,
    QPainter,
    QLinearGradient,
    QColor,
    QPen,
    QBrush,
)
from PyQt5.QtChart import (
    QChart,
    QChartView,
    QValueAxis,
    QSplineSeries,
)
import random
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QLinearGradient, QBrush
from PyQt5.QtWidgets import QWidget


class AnimatedWaterWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._water_level = 0
        self._target_level = 0
        self.estado = "SinSensor"
        self.valido = False

        self.setMinimumSize(280, 420)

        # Animación del nivel
        self.animation = QPropertyAnimation(self, b"water_level")
        self.animation.setDuration(900)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)

    # ---------- Propiedad ----------
    def get_water_level(self):
        return self._water_level

    def set_water_level(self, value):
        self._water_level = value
        self.update()

    water_level = pyqtProperty(float, get_water_level, set_water_level)

    # ---------- Actualización ----------
    def update_water_level(self, target_level, estado, valido):
        self._target_level = target_level
        self.estado = estado
        self.valido = valido

        self.animation.stop()
        self.animation.setStartValue(self._water_level)
        self.animation.setEndValue(target_level)
        self.animation.start()

    # ---------- Pintar ----------
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()

        # ------------------ Colores según estado ------------------
        if not self.valido:
            color = QColor(156, 163, 175)
        elif self.estado == "Lleno":
            color = QColor(239, 68, 68)
        elif self.estado == "Medio":
            color = QColor(16, 185, 129)
        elif self.estado == "Bajo":
            color = QColor(245, 158, 11)
        else:
            color = QColor(220, 38, 38)

        # ------------------ Medidas del tanque (rectangular) ------------------
        tank_width = width * 0.70
        tank_height = height * 0.88
        tank_x = (width - tank_width) / 2
        tank_y = (height - tank_height) / 2 + 10

        # ------------------ Tanque cuadrado ------------------
        painter.setPen(QPen(color, 4))
        painter.setBrush(QColor(255, 255, 255))
        painter.drawRect(int(tank_x), int(tank_y), int(tank_width), int(tank_height))

        # ------------------ Agua (rectangular) ------------------
        if self.valido and self._water_level > 0:
            water_height = (self._water_level / 100) * tank_height
            water_y = tank_y + tank_height - water_height

            gradient = QLinearGradient(0, water_y, 0, water_y + water_height)
            gradient.setColorAt(0, QColor(56, 189, 248, 220))
            gradient.setColorAt(1, QColor(14, 165, 233, 255))

            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(gradient))

            painter.drawRect(
                int(tank_x) + 4, int(water_y), int(tank_width) - 8, int(water_height)
            )

        # ------------------ Texto porcentaje ------------------
        painter.setPen(QPen(QColor(51, 65, 85)))
        painter.setFont(QFont("Segoe UI", 22, QFont.Bold))

        text = f"{self._water_level:.1f}%"
        painter.drawText(0, 0, width, int(tank_y - 5), Qt.AlignCenter, text)


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
            f"""
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


class Sidebar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setStyleSheet(
            """
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1e293b, stop:1 #0f172a);
                border-right: 1px solid #334155;
            }
            """
        )
        self.setFixedWidth(260)
        self.current_active = 0
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        # Logo
        logo_container = QWidget()
        logo_container.setStyleSheet("background: transparent; padding: 20px;")
        logo_layout = QVBoxLayout(logo_container)
        logo = QLabel("💧 TankMonitor")
        logo.setStyleSheet(
            """
            color: white;
            font-size: 22px;
            font-weight: bold;
            font-family: 'Segoe UI', Arial;
            padding: 10px;
            """
        )
        logo_layout.addWidget(logo)
        version = QLabel("Versión 2.0 Pro")
        version.setStyleSheet("color: #64748b; font-size: 11px; padding-left: 10px;")
        logo_layout.addWidget(version)
        layout.addWidget(logo_container)
        # Menu Items
        self.menu_items = []
        self.menu_data = [
            ("📊", "Dashboard"),
            ("📈", "Análisis"),
            ("📋", "Historial"),
            ("⚙️", "Configuración"),
            ("🔔", "Alertas"),
            ("📁", "Reportes"),
        ]
        for index, (icon, text) in enumerate(self.menu_data):
            btn = self.create_menu_button(icon, text, index == 0)
            btn.clicked.connect(lambda checked, idx=index: self.switch_section(idx))
            layout.addWidget(btn)
            self.menu_items.append(btn)
        layout.addStretch()
        # Footer info
        footer = QLabel("🟢 Sistema Activo\n📡 Conectado")
        footer.setStyleSheet(
            """
            color: #64748b;
            font-size: 11px;
            padding: 20px;
            border-top: 1px solid #334155;
            """
        )
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)
        self.setLayout(layout)

    def create_menu_button(self, icon, text, active=False):
        btn = QPushButton(f"{icon}  {text}")
        btn.setProperty("active", active)
        self.update_button_style(btn)
        btn.setCursor(Qt.PointingHandCursor)
        return btn

    def update_button_style(self, btn):
        active = btn.property("active")
        btn.setStyleSheet(
            f"""
            QPushButton {{
                text-align: left;
                padding: 16px 24px;
                border: none;
                color: {'#ffffff' if active else '#94a3b8'};
                background: {'#334155' if active else 'transparent'};
                font-size: 14px;
                font-weight: {'600' if active else '500'};
                font-family: 'Segoe UI', Arial;
                border-left: {'4px solid #3b82f6' if active else '4px solid transparent'};
            }}
            QPushButton:hover {{
                background: #334155;
                color: #ffffff;
            }}
            """
        )

    def switch_section(self, index):
        # Deactivate all buttons
        for btn in self.menu_items:
            btn.setProperty("active", False)
            self.update_button_style(btn)
        # Activate clicked button
        self.menu_items[index].setProperty("active", True)
        self.update_button_style(self.menu_items[index])
        self.current_active = index
        # Notify parent window
        if self.parent_window:
            self.parent_window.change_section(index)


class TankMonitorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TankMonitor Pro")
        self.setGeometry(50, 50, 1600, 950)
        self.historical_data = []
        self.chart_data = []
        self.events_timeline = []
        self.daily_readings = []
        self.yesterday_avg = 0
        self.week_avg = 0
        self.current_temperature = 22.0
        self.current_section = 0  # Track active section
        self.setup_ui()
        self.setup_chart()  # Moved after UI setup
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
        # Stacked Widget for different sections
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background: transparent;")
        # Create all sections
        self.dashboard_widget = self.create_dashboard_section()
        self.analisis_widget = self.create_analisis_section()
        self.historial_widget = self.create_historial_section()
        self.config_widget = self.create_config_section()
        self.alertas_widget = self.create_alertas_section()
        self.reportes_widget = self.create_reportes_section()
        self.stacked_widget.addWidget(self.dashboard_widget)
        self.stacked_widget.addWidget(self.analisis_widget)
        self.stacked_widget.addWidget(self.historial_widget)
        self.stacked_widget.addWidget(self.config_widget)
        self.stacked_widget.addWidget(self.alertas_widget)
        self.stacked_widget.addWidget(self.reportes_widget)
        content_layout.addWidget(self.stacked_widget)
        # Footer
        footer = self.create_footer()
        content_layout.addWidget(footer)
        main_layout.addWidget(content_widget)

    def change_section(self, index):
        self.stacked_widget.setCurrentIndex(index)
        self.current_section = index  # Track current section
        # Update navbar title
        titles = [
            "Panel de Control Principal",
            "Análisis de Datos",
            "Historial Completo",
            "Configuración del Sistema",
            "Centro de Alertas",
            "Generación de Reportes",
        ]
        if hasattr(self, "navbar_title"):
            self.navbar_title.setText(titles[index])

    def create_dashboard_section(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(30, 30, 30, 30)
        scroll_layout.setSpacing(24)
        dashboard_content = self.create_dashboard_content()
        scroll_layout.addWidget(dashboard_content)
        scroll.setWidget(scroll_content)
        return scroll

    def create_analisis_section(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 30, 30, 30)
        title = QLabel("📈 Análisis Avanzado de Datos")
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
            "Esta sección mostrará gráficos avanzados, tendencias y análisis predictivo del nivel del tanque."
        )
        info.setStyleSheet("font-size: 14px; color: #64748b; padding: 20px;")
        info.setWordWrap(True)
        layout.addWidget(info)
        layout.addStretch()
        return widget

    def create_historial_section(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        # Title
        title = QLabel("📋 Historial Completo de Lecturas")
        title.setStyleSheet(
            """
            font-size: 24px;
            font-weight: bold;
            color: #0f172a;
            font-family: 'Segoe UI', Arial;
            margin-bottom: 10px;
            """
        )
        layout.addWidget(title)
        # Stats cards row
        stats_cards_layout = QHBoxLayout()
        stats_cards_layout.setSpacing(20)
        self.hist_total_card = ModernCard(
            "Total Lecturas", "0", "Desde inicio", "📊", "blue"
        )
        self.hist_valid_card = ModernCard(
            "Lecturas Válidas", "0", "Sin errores", "✓", "green"
        )
        self.hist_error_card = ModernCard(
            "Lecturas Erróneas", "0", "Con problemas", "✗", "red"
        )
        self.hist_avg_card = ModernCard(
            "Nivel Promedio", "--", "Últimas 50 lecturas", "📈", "purple"
        )
        stats_cards_layout.addWidget(self.hist_total_card)
        stats_cards_layout.addWidget(self.hist_valid_card)
        stats_cards_layout.addWidget(self.hist_error_card)
        stats_cards_layout.addWidget(self.hist_avg_card)
        layout.addLayout(stats_cards_layout)
        # History table with enhanced design
        table_frame = QFrame()
        table_frame.setStyleSheet(
            """
            QFrame {
                background: white;
                border-radius: 16px;
                border: 1px solid #e2e8f0;
            }
            """
        )
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(24, 20, 24, 20)
        table_layout.setSpacing(16)
        # Header with controls
        header_layout = QHBoxLayout()
        table_title = QLabel("📋 Tabla de Registros")
        table_title.setStyleSheet(
            """
            font-size: 18px;
            font-weight: 700;
            color: #0f172a;
            font-family: 'Segoe UI', Arial;
            """
        )
        header_layout.addWidget(table_title)
        header_layout.addStretch()
        # Search button
        search_btn = QPushButton("🔍 Buscar")
        search_btn.setStyleSheet(
            """
            QPushButton {
                background: #f1f5f9;
                color: #475569;
                border: 1px solid #e2e8f0;
                padding: 8px 16px;
                border-radius: 8px;
                font-size: 13px;
                font-weight: 600;
                font-family: 'Segoe UI', Arial;
            }
            QPushButton:hover {
                background: #e2e8f0;
                border-color: #cbd5e1;
            }
            """
        )
        search_btn.setCursor(Qt.PointingHandCursor)
        header_layout.addWidget(search_btn)
        # Export button
        export_btn = QPushButton("📥 Exportar")
        export_btn.setStyleSheet(
            """
            QPushButton {
                background: #dbeafe;
                color: #1e40af;
                border: 1px solid #93c5fd;
                padding: 8px 16px;
                border-radius: 8px;
                font-size: 13px;
                font-weight: 600;
                font-family: 'Segoe UI', Arial;
            }
            QPushButton:hover {
                background: #bfdbfe;
                border-color: #60a5fa;
            }
            """
        )
        export_btn.setCursor(Qt.PointingHandCursor)
        header_layout.addWidget(export_btn)
        # Clear button
        clear_btn = QPushButton("🗑️ Limpiar")
        clear_btn.setStyleSheet(
            """
            QPushButton {
                background: #fef2f2;
                color: #dc2626;
                border: 1px solid #fecaca;
                padding: 8px 16px;
                border-radius: 8px;
                font-size: 13px;
                font-weight: 600;
                font-family: 'Segoe UI', Arial;
            }
            QPushButton:hover {
                background: #fee2e2;
                border-color: #fca5a5;
            }
            """
        )
        clear_btn.setCursor(Qt.PointingHandCursor)
        clear_btn.clicked.connect(self.clear_history)
        header_layout.addWidget(clear_btn)
        table_layout.addLayout(header_layout)
        # Stats row
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(12)
        self.historial_total_readings_label = QLabel("Total: 0 lecturas")
        self.historial_total_readings_label.setStyleSheet(
            """
            background: #eff6ff;
            color: #1e40af;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            font-family: 'Segoe UI', Arial;
            """
        )
        stats_layout.addWidget(self.historial_total_readings_label)
        self.historial_valid_readings_label = QLabel("Válidas: 0")
        self.historial_valid_readings_label.setStyleSheet(
            """
            background: #dcfce7;
            color: #15803d;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            font-family: 'Segoe UI', Arial;
            """
        )
        stats_layout.addWidget(self.historial_valid_readings_label)
        self.historial_error_readings_label = QLabel("Errores: 0")
        self.historial_error_readings_label.setStyleSheet(
            """
            background: #fee2e2;
            color: #991b1b;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            font-family: 'Segoe UI', Arial;
            """
        )
        stats_layout.addWidget(self.historial_error_readings_label)
        stats_layout.addStretch()
        table_layout.addLayout(stats_layout)
        # Enhanced table
        self.historial_history_table = QTableWidget()
        self.historial_history_table.setColumnCount(7)
        self.historial_history_table.setHorizontalHeaderLabels(
            ["#", "⏰ Hora", "📏 Nivel", "📊 %", "🎯 Estado", "💧 Sensor", "✓"]
        )
        # Set column widths
        self.historial_history_table.setColumnWidth(0, 50)
        self.historial_history_table.setColumnWidth(1, 120)
        self.historial_history_table.setColumnWidth(2, 100)
        self.historial_history_table.setColumnWidth(3, 80)
        self.historial_history_table.setColumnWidth(4, 120)
        self.historial_history_table.setColumnWidth(5, 100)
        self.historial_history_table.setColumnWidth(6, 60)
        self.historial_history_table.horizontalHeader().setStretchLastSection(False)
        self.historial_history_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.historial_history_table.setSelectionMode(QTableWidget.SingleSelection)
        self.historial_history_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.historial_history_table.verticalHeader().setVisible(False)
        self.historial_history_table.setShowGrid(False)
        self.historial_history_table.setAlternatingRowColors(False)
        self.historial_history_table.setStyleSheet(
            """
            QTableWidget {
                border: none;
                background: white;
                font-family: 'Segoe UI', Arial;
                font-size: 13px;
                gridline-color: transparent;
            }
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8fafc, stop:1 #f1f5f9);
                color: #475569;
                padding: 14px 10px;
                border: none;
                border-bottom: 2px solid #e2e8f0;
                font-weight: 700;
                font-size: 12px;
                text-align: center;
            }
            QTableWidget::item {
                padding: 12px 10px;
                border-bottom: 1px solid #f1f5f9;
            }
            QTableWidget::item:selected {
                background: #dbeafe;
                color: #1e40af;
            }
            QTableWidget::item:hover {
                background: #f8fafc;
            }
            QScrollBar:vertical {
                border: none;
                background: #f8fafc;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #cbd5e1;
                border-radius: 5px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: #94a3b8;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            """
        )
        self.historial_history_table.setMinimumHeight(450)
        table_layout.addWidget(self.historial_history_table)
        # Pagination controls
        pagination_layout = QHBoxLayout()
        self.historial_rows_label = QLabel("Mostrando 0 de 0 registros")
        self.historial_rows_label.setStyleSheet(
            """
            color: #64748b;
            font-size: 12px;
            font-family: 'Segoe UI', Arial;
            """
        )
        pagination_layout.addWidget(self.historial_rows_label)
        pagination_layout.addStretch()
        table_layout.addLayout(pagination_layout)
        layout.addWidget(table_frame)
        scroll.setWidget(scroll_content)
        return scroll

    def create_config_section(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
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
        # Config cards
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
        return widget

    def create_alertas_section(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
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
        return widget

    def create_reportes_section(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
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
        return widget

    def create_navbar(self):
        navbar = QFrame()
        navbar.setStyleSheet(
            """
            QFrame {
                background: white;
                border-bottom: 1px solid #e2e8f0;
            }
            """
        )
        navbar.setFixedHeight(70)
        layout = QHBoxLayout(navbar)
        layout.setContentsMargins(30, 0, 30, 0)
        self.navbar_title = QLabel("Panel de Control Principal")
        self.navbar_title.setStyleSheet(
            """
            font-size: 20px;
            font-weight: bold;
            color: #0f172a;
            font-family: 'Segoe UI', Arial;
            """
        )
        layout.addWidget(self.navbar_title)
        layout.addStretch()
        # Time
        self.time_label = QLabel()
        self.time_label.setStyleSheet(
            """
            color: #64748b;
            font-size: 13px;
            font-family: 'Segoe UI', Arial;
            padding: 8px 16px;
            background: #f1f5f9;
            border-radius: 8px;
            """
        )
        layout.addWidget(self.time_label)
        # User
        user_btn = QPushButton("👤 Admin")
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
                font-family: 'Segoe UI', Arial;
            }
            QPushButton:hover {
                background: #2563eb;
            }
            """
        )
        user_btn.setCursor(Qt.PointingHandCursor)
        layout.addWidget(user_btn)
        return navbar

    def create_dashboard_content(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(24)
        # Cards row
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)
        self.card_nivel = ModernCard(
            "Nivel de Agua", "--", "Esperando datos...", "💧", "blue"
        )
        self.card_porcentaje = ModernCard(
            "Capacidad", "--", "0% del tanque", "📊", "green"
        )
        self.card_humedad = ModernCard(
            "Sensor Humedad", "--", "Sin fugas", "💦", "cyan"
        )
        self.card_lecturas = ModernCard("Lecturas", "0", "0 errores", "✓", "purple")
        cards_layout.addWidget(self.card_nivel)
        cards_layout.addWidget(self.card_porcentaje)
        cards_layout.addWidget(self.card_humedad)
        cards_layout.addWidget(self.card_lecturas)
        layout.addLayout(cards_layout)
        # Widgets row - Temperatura y Eventos (sin comparativa)

        # Timeline Widget
        timeline_frame = QFrame()
        timeline_frame.setStyleSheet(
            """
            QFrame {
                background: white;
                border-radius: 16px;
                border: 1px solid #e2e8f0;
            }
            """
        )
        timeline_layout = QVBoxLayout(timeline_frame)
        timeline_layout.setContentsMargins(24, 20, 24, 20)
        # Timeline scroll area
        timeline_scroll = QScrollArea()
        timeline_scroll.setWidgetResizable(True)
        timeline_scroll.setStyleSheet(
            """
            QScrollArea {
                border: none;
                background: transparent;
            }
            """
        )
        self.timeline_widget = QWidget()
        self.timeline_layout = QVBoxLayout(self.timeline_widget)
        self.timeline_layout.setSpacing(8)
        self.timeline_layout.setContentsMargins(0, 0, 0, 0)
        # Initial empty state

        self.timeline_layout.addStretch()
        timeline_scroll.setWidget(self.timeline_widget)
        timeline_layout.addWidget(timeline_scroll)
        # Visualization row (Tanque + Gráfica)
        viz_layout = QHBoxLayout()
        viz_layout.setSpacing(20)
        # Tank
        tank_frame = QFrame()
        tank_frame.setStyleSheet(
            """
            QFrame {
                background: white;
                border-radius: 16px;
                border: 1px solid #e2e8f0;
            }
            """
        )
        tank_layout = QVBoxLayout(tank_frame)
        tank_layout.setContentsMargins(24, 20, 24, 20)
        tank_title = QLabel("🎯 Visualización del Tanque")
        tank_title.setStyleSheet(
            """
            font-size: 16px;
            font-weight: 600;
            color: #0f172a;
            font-family: 'Segoe UI', Arial;
            margin-bottom: 10px;
            """
        )
        tank_layout.addWidget(tank_title)
        self.tank_widget = AnimatedWaterWidget()
        tank_layout.addWidget(self.tank_widget, alignment=Qt.AlignCenter)
        viz_layout.addWidget(tank_frame, 35)
        # Chart
        chart_frame = QFrame()
        chart_frame.setStyleSheet(
            """
            QFrame {
                background: white;
                border-radius: 16px;
                border: 1px solid #e2e8f0;
            }
            """
        )
        chart_layout = QVBoxLayout(chart_frame)
        chart_layout.setContentsMargins(24, 20, 24, 20)
        chart_title = QLabel("📈 Nivel en Tiempo Real (últimos 30 segundos)")
        chart_title.setStyleSheet(
            """
            font-size: 16px;
            font-weight: 600;
            color: #0f172a;
            font-family: 'Segoe UI', Arial;
            margin-bottom: 10px;
            """
        )
        chart_layout.addWidget(chart_title)
        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setStyleSheet("border: none;")
        chart_layout.addWidget(self.chart_view)
        viz_layout.addWidget(chart_frame, 65)
        layout.addLayout(viz_layout)
        return container

    def create_footer(self):
        footer = QFrame()
        footer.setStyleSheet(
            """
            QFrame {
                background: white;
                border-top: 1px solid #e2e8f0;
            }
            """
        )
        footer.setFixedHeight(60)
        layout = QHBoxLayout(footer)
        layout.setContentsMargins(30, 0, 30, 0)
        copyright_label = QLabel(
            "© 2024 TankMonitor Pro | Sistema de Monitoreo Industrial"
        )
        copyright_label.setStyleSheet(
            """
            color: #64748b;
            font-size: 12px;
            font-family: 'Segoe UI', Arial;
            """
        )
        layout.addWidget(copyright_label)
        layout.addStretch()
        status_label = QLabel(
            "🟢 Sistema Operativo | 📡 Arduino Conectado | 🗄️ MongoDB Activo"
        )
        status_label.setStyleSheet(
            """
            color: #10b981;
            font-size: 12px;
            font-weight: 600;
            font-family: 'Segoe UI', Arial;
            """
        )
        layout.addWidget(status_label)
        return footer

    def setup_chart(self):
        self.series = QSplineSeries()
        self.series.setColor(QColor(59, 130, 246))
        pen = QPen(QColor(59, 130, 246))
        pen.setWidth(3)
        self.series.setPen(pen)
        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setTitle("")
        self.chart.legend().hide()
        self.chart.setBackgroundVisible(False)
        self.chart.setMargins(QMargins(0, 0, 0, 0))
        self.axis_x = QValueAxis()
        self.axis_x.setLabelFormat("%d s")
        self.axis_x.setTitleText("")
        self.axis_x.setRange(0, 30)
        self.axis_x.setTickCount(7)
        self.axis_x.setLabelsColor(QColor(100, 116, 139))
        self.axis_y = QValueAxis()
        self.axis_y.setLabelFormat("%.0f%%")
        self.axis_y.setTitleText("")
        self.axis_y.setRange(0, 100)
        self.axis_y.setTickCount(6)
        self.axis_y.setLabelsColor(QColor(100, 116, 139))
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.series.attachAxis(self.axis_x)
        self.series.attachAxis(self.axis_y)
        self.chart_view.setChart(self.chart)

    def add_timeline_event(self, message, event_type="info"):
        """Add event to timeline"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        # Remove empty state if exists
        if self.timeline_layout.count() > 0:
            item = self.timeline_layout.itemAt(0)
            if item and item.widget():
                widget = item.widget()
                if "Sin eventos" in widget.text():
                    self.timeline_layout.removeWidget(widget)
                    widget.deleteLater()
        # Color based on type
        if event_type == "warning":
            bg_color = "#fef3c7"
            border_color = "#f59e0b"
            icon = "⚠️"
        elif event_type == "error":
            bg_color = "#fee2e2"
            border_color = "#ef4444"
            icon = "🔴"
        elif event_type == "success":
            bg_color = "#d1fae5"
            border_color = "#10b981"
            icon = "✓"
        else:
            bg_color = "#dbeafe"
            border_color = "#3b82f6"
            icon = "ℹ️"
        event_frame = QFrame()
        event_frame.setStyleSheet(
            f"""
            QFrame {{
                background: {bg_color};
                border-left: 3px solid {border_color};
                border-radius: 6px;
                padding: 8px 12px;
            }}
            """
        )
        event_layout = QHBoxLayout(event_frame)
        event_layout.setContentsMargins(0, 0, 0, 0)
        time_label = QLabel(f"{icon} {timestamp}")
        time_label.setStyleSheet(
            """
            font-size: 11px;
            font-weight: bold;
            color: #475569;
            font-family: 'Segoe UI', Arial;
            """
        )
        event_layout.addWidget(time_label)
        msg_label = QLabel(message)
        msg_label.setStyleSheet(
            """
            font-size: 12px;
            color: #1e293b;
            font-family: 'Segoe UI', Arial;
            """
        )
        event_layout.addWidget(msg_label)
        event_layout.addStretch()
        # Insert at top
        self.timeline_layout.insertWidget(0, event_frame)
        # Keep only last 10 events
        while self.timeline_layout.count() > 11:  # 10 events + stretch
            item = self.timeline_layout.itemAt(10)
            if item and item.widget():
                widget = item.widget()
                self.timeline_layout.removeWidget(widget)
                widget.deleteLater()
        # Store event
        self.events_timeline.append(
            {"time": timestamp, "message": message, "type": event_type}
        )

    def setup_timers(self):
        # Update time
        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(1000)
        self.update_time()
        # Simulate data
        self.data_timer = QTimer()
        self.data_timer.timeout.connect(self.simulate_data)
        self.data_timer.start(2000)

    def update_time(self):
        current_time = datetime.now().strftime("%d/%m/%Y  %H:%M:%S")
        self.time_label.setText(f"🕐 {current_time}")

    def simulate_data(self):
        base_nivel = 8.0
        variation = random.uniform(-2, 3)
        nivel = max(3, min(20, base_nivel + variation))
        porcentaje = ((20 - nivel) / 17) * 100
        porcentaje = max(0, min(100, porcentaje))
        if porcentaje >= 80:
            estado = "Lleno"
        elif porcentaje >= 50:
            estado = "Medio"
        elif porcentaje >= 20:
            estado = "Bajo"
        else:
            estado = "MuyBajo"
        simulated_data = {
            "nivel": nivel,
            "porcentaje": porcentaje,
            "estado": estado,
            "humedad": random.randint(750, 950),
            "estado_fuga": "NoFuga" if random.random() > 0.1 else "FugaPeq",
            "valido": True,
            "lecturas_ok": len(self.historical_data) + 1,
            "lecturas_error": random.randint(0, 5),
        }
        self.update_ui(simulated_data)

    def update_ui(self, data):
        # Update cards
        nivel_text = f"{data['nivel']:.1f} cm"
        self.card_nivel.update_value(nivel_text)
        self.card_nivel.update_subtitle(f"Estado: {data['estado']}")
        porcentaje_text = f"{data['porcentaje']:.1f}%"
        self.card_porcentaje.update_value(porcentaje_text)
        self.card_porcentaje.update_subtitle(
            f"{100 - data['porcentaje']:.0f}% disponible"
        )
        self.card_humedad.update_value(str(data["humedad"]))
        fuga_text = (
            "🟢 Sin Fuga" if data["estado_fuga"] == "NoFuga" else "🟡 Fuga Detectada"
        )
        self.card_humedad.update_subtitle(fuga_text)
        self.card_lecturas.update_value(str(data["lecturas_ok"]))
        self.card_lecturas.update_subtitle(
            f"{data['lecturas_error']} errores detectados"
        )
        # Update tank
        self.tank_widget.update_water_level(
            data["porcentaje"], data["estado"], data["valido"]
        )
        # Update chart
        self.chart_data.append(data["porcentaje"])
        if len(self.chart_data) > 15:
            self.chart_data.pop(0)
        self.series.clear()
        for i, value in enumerate(self.chart_data):
            self.series.append(i * 2, value)
        # Accumulate historical data
        self.historical_data.append(data)
        # Update history (solo en sección de historial)
        if self.current_section == 2:
            self.update_history(data)

    def update_history(self, data):
        # Solo actualizar en sección de historial
        if self.current_section != 2:
            return
        table = self.historial_history_table
        total_label = self.historial_total_readings_label
        valid_label = self.historial_valid_readings_label
        error_label = self.historial_error_readings_label
        rows_label = self.historial_rows_label
        timestamp = datetime.now().strftime("%H:%M:%S")
        # Row number
        row_num = table.rowCount() + 1
        # Status badge
        if data["estado"] == "Lleno":
            estado_badge = "🔴 Lleno"
            bg_color = QColor(254, 226, 226)
        elif data["estado"] == "Medio":
            estado_badge = "🟢 Medio"
            bg_color = QColor(220, 252, 231)
        elif data["estado"] == "Bajo":
            estado_badge = "🟡 Bajo"
            bg_color = QColor(254, 243, 199)
        else:
            estado_badge = "🔴 Muy Bajo"
            bg_color = QColor(254, 226, 226)
        # Valid badge
        valid_badge = "✓" if data["valido"] else "✗"
        valid_color = QColor(220, 252, 231) if data["valido"] else QColor(254, 226, 226)
        row_data = [
            str(row_num),
            timestamp,
            f"{data['nivel']:.1f} cm",
            f"{data['porcentaje']:.0f}%",
            estado_badge,
            str(data["humedad"]),
            valid_badge,
        ]
        table.insertRow(0)
        for col, value in enumerate(row_data):
            item = QTableWidgetItem(value)
            item.setTextAlignment(Qt.AlignCenter)
            # Row number style
            if col == 0:
                item.setForeground(QColor(100, 116, 139))
                font = QFont("Segoe UI", 11, QFont.Bold)
                item.setFont(font)
            # Estado column
            if col == 4:
                item.setBackground(bg_color)
                font = QFont("Segoe UI", 12, QFont.Bold)
                item.setFont(font)
            # Valid column
            if col == 6:
                item.setBackground(valid_color)
                font = QFont("Segoe UI", 14, QFont.Bold)
                item.setFont(font)
            table.setItem(0, col, item)
        # Set row height
        table.setRowHeight(0, 50)
        # Limit rows
        if table.rowCount() > 50:
            table.removeRow(50)
        # Update stats
        total = table.rowCount()
        valid_count = sum(1 for i in range(total) if table.item(i, 6).text() == "✓")
        error_count = total - valid_count
        total_label.setText(f"Total: {total} lecturas")
        valid_label.setText(f"Válidas: {valid_count}")
        error_label.setText(f"Errores: {error_count}")
        rows_label.setText(f"Mostrando {min(total, 50)} de {total} registros")
        # Update historial cards
        self.hist_total_card.update_value(str(total))
        self.hist_valid_card.update_value(str(valid_count))
        self.hist_error_card.update_value(str(error_count))
        if total > 0:
            percentages = [
                float(table.item(i, 3).text().rstrip("%")) for i in range(total)
            ]
            avg = sum(percentages) / total
            self.hist_avg_card.update_value(f"{avg:.1f}%")
        else:
            self.hist_avg_card.update_value("--")

    def clear_history(self):
        # Solo limpiar en sección de historial
        if self.current_section != 2:
            return
        self.historial_history_table.setRowCount(0)
        self.historial_total_readings_label.setText("Total: 0 lecturas")
        self.historial_valid_readings_label.setText("Válidas: 0")
        self.historial_error_readings_label.setText("Errores: 0")
        self.historial_rows_label.setText("Mostrando 0 de 0 registros")
        self.hist_total_card.update_value("0")
        self.hist_valid_card.update_value("0")
        self.hist_error_card.update_value("0")
        self.hist_avg_card.update_value("--")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = TankMonitorApp()
    window.show()
    sys.exit(app.exec_())
