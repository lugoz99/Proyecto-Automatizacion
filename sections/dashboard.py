from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QScrollArea,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtChart import QChart, QChartView, QValueAxis, QSplineSeries

from widgets.animated_water import AnimatedWaterWidget
from widgets.modern_card import ModernCard


class DashboardSection(QScrollArea):
    def __init__(self, parent_app=None):
        super().__init__()
        self.parent_app = parent_app
        self.setWidgetResizable(True)
        self.setStyleSheet("border: none;")

        self.historical_data = []
        self.chart_data = []

        self.setup_ui()
        self.setup_chart()

    def setup_ui(self):
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(24)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)

        self.card_nivel = ModernCard(
            "Nivel de Agua", "--", "Esperando datos...", "💧", "blue"
        )
        self.card_porcentaje = ModernCard(
            "Capacidad", "--", "0% del tanque", "📊", "green"
        )
        self.card_humedad = ModernCard("Estado Fugas", "--", "Sin datos", "💦", "cyan")
        self.card_lecturas = ModernCard("Lecturas", "0", "0 errores", "✓", "purple")

        cards_layout.addWidget(self.card_nivel)
        cards_layout.addWidget(self.card_porcentaje)
        cards_layout.addWidget(self.card_humedad)
        cards_layout.addWidget(self.card_lecturas)
        layout.addLayout(cards_layout)

        viz_layout = QHBoxLayout()
        viz_layout.setSpacing(20)

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
            margin-bottom: 10px;
        """
        )
        tank_layout.addWidget(tank_title)

        self.tank_widget = AnimatedWaterWidget()
        tank_layout.addWidget(self.tank_widget, alignment=Qt.AlignCenter)
        viz_layout.addWidget(tank_frame)

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

        chart_title = QLabel("📈 Nivel en Tiempo Real")
        chart_title.setStyleSheet(
            """
            font-size: 16px;
            font-weight: 600;
            color: #0f172a;
            margin-bottom: 10px;
        """
        )
        chart_layout.addWidget(chart_title)

        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setStyleSheet("border: none;")
        chart_layout.addWidget(self.chart_view)
        viz_layout.addWidget(chart_frame)

        layout.addLayout(viz_layout)
        self.setWidget(content)

    def setup_chart(self):
        self.series = QSplineSeries()

        # self.series.setColor(QColor("#3b82f6"))  # Así sí funciona
        pen = self.series.pen()
        pen.setColor(QColor("#3b82f6"))
        pen.setWidth(2)
        self.series.setPen(pen)
        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.legend().hide()
        self.chart.setBackgroundVisible(False)

        self.axis_x = QValueAxis()
        self.axis_x.setLabelFormat("%d s")
        self.axis_x.setRange(0, 30)
        self.axis_x.setTickCount(7)

        self.axis_y = QValueAxis()
        self.axis_y.setLabelFormat("%.0f%%")
        self.axis_y.setRange(0, 100)
        self.axis_y.setTickCount(6)

        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.series.attachAxis(self.axis_x)
        self.series.attachAxis(self.axis_y)

        self.chart_view.setChart(self.chart)

    def update_with_real_data(self, data):
        try:
            if not data:
                return

            # 🔧 VERSIÓN CORREGIDA - Sin duplicados
            nivel = data.get("nivel", 0)
            porcentaje = data.get("porcentaje", 0)
            humedad = data.get("humedad", 0)
            estado = data.get("estado", "--")
            estado_fuga = data.get("estado_fuga", "Sin datos")
            lecturas_ok = data.get("lecturas_ok", 0)
            lecturas_error = data.get("lecturas_error", 0)
            valido = data.get("valido", False)

            # Actualizar cards
            nivel_text = f"{nivel:.1f} cm" if nivel else "--"
            self.card_nivel.update_value(nivel_text)
            self.card_nivel.update_subtitle(f"Estado: {estado}")

            porcentaje_text = f"{porcentaje:.1f}%" if porcentaje else "--"
            self.card_porcentaje.update_value(porcentaje_text)

            self.card_humedad.update_value(str(humedad))
            self.card_humedad.update_subtitle(estado_fuga)

            self.card_lecturas.update_value(str(lecturas_ok))
            self.card_lecturas.update_subtitle(f"{lecturas_error} errores")

            # Actualizar tanque animado
            self.tank_widget.update_water_level(porcentaje, estado, valido)

            # Actualizar gráfico (solo si hay porcentaje)
            if porcentaje:
                self.chart_data.append(porcentaje)
                if len(self.chart_data) > 15:
                    self.chart_data.pop(0)

                self.series.clear()
                for i, value in enumerate(self.chart_data):
                    self.series.append(i * 2, value)

            # Guardar en histórico
            self.historical_data.append(data)

        except Exception as e:
            print(f"❌ Error actualizando dashboard: {e}")
