from datetime import datetime, timedelta
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QScrollArea,
    QComboBox,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

from widgets.modern_card import ModernCard


class HistorialSection(QScrollArea):
    def __init__(self, parent_app=None):
        super().__init__()
        self.parent_app = parent_app
        self.setWidgetResizable(True)
        self.setStyleSheet("border: none;")

        self.historical_data = []
        self.setup_ui()

    def setup_ui(self):
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        title = QLabel("📋 Historial de Lecturas")
        title.setStyleSheet(
            """
            font-size: 24px;
            font-weight: bold;
            color: #0f172a;
            margin-bottom: 10px;
        """
        )
        layout.addWidget(title)

        filters_frame = QFrame()
        filters_frame.setStyleSheet(
            """
            QFrame {
                background: white;
                border-radius: 16px;
                border: 1px solid #e2e8f0;
            }
        """
        )
        filters_layout = QVBoxLayout(filters_frame)
        filters_layout.setContentsMargins(20, 20, 20, 20)

        filters_header = QLabel("🔍 Filtros de Búsqueda")
        filters_header.setStyleSheet(
            "font-size: 16px; font-weight: 600; color: #0f172a; margin-bottom: 15px;"
        )
        filters_layout.addWidget(filters_header)

        controls_layout = QHBoxLayout()

        time_layout = QVBoxLayout()
        time_label = QLabel("Período:")
        time_label.setStyleSheet("font-size: 13px; color: #64748b; margin-bottom: 5px;")
        time_layout.addWidget(time_label)

        self.time_combo = QComboBox()
        self.time_combo.addItems(
            ["Últimas 24 horas", "Últimas 6 horas", "Última hora", "Últimos 7 días"]
        )
        self.time_combo.setStyleSheet(
            """
            QComboBox {
                padding: 8px 12px;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                background: white;
                min-width: 150px;
            }
        """
        )
        self.time_combo.currentIndexChanged.connect(self.load_historical_data)
        time_layout.addWidget(self.time_combo)
        controls_layout.addLayout(time_layout)

        type_layout = QVBoxLayout()
        type_label = QLabel("Tipo:")
        type_label.setStyleSheet("font-size: 13px; color: #64748b; margin-bottom: 5px;")
        type_layout.addWidget(type_label)

        self.type_combo = QComboBox()
        self.type_combo.addItems(
            ["Todas las lecturas", "Solo válidas", "Solo con errores"]
        )
        self.type_combo.setStyleSheet(
            """
            QComboBox {
                padding: 8px 12px;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                background: white;
                min-width: 150px;
            }
        """
        )
        self.type_combo.currentIndexChanged.connect(self.load_historical_data)
        type_layout.addWidget(self.type_combo)
        controls_layout.addLayout(type_layout)

        controls_layout.addStretch()

        buttons_layout = QHBoxLayout()

        refresh_btn = QPushButton("🔄 Actualizar")
        refresh_btn.setStyleSheet(
            """
            QPushButton {
                background: #dbeafe;
                color: #1e40af;
                border: 1px solid #93c5fd;
                padding: 8px 16px;
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
        refresh_btn.clicked.connect(self.load_historical_data)
        buttons_layout.addWidget(refresh_btn)

        export_btn = QPushButton("📥 Exportar CSV")
        export_btn.setStyleSheet(
            """
            QPushButton {
                background: #dcfce7;
                color: #15803d;
                border: 1px solid #86efac;
                padding: 8px 16px;
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
        buttons_layout.addWidget(export_btn)

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
            }
            QPushButton:hover {
                background: #fee2e2;
                border-color: #fca5a5;
            }
        """
        )
        clear_btn.clicked.connect(self.clear_history)
        buttons_layout.addWidget(clear_btn)

        controls_layout.addLayout(buttons_layout)
        filters_layout.addLayout(controls_layout)
        layout.addWidget(filters_frame)

        stats_cards_layout = QHBoxLayout()
        stats_cards_layout.setSpacing(20)

        self.hist_total_card = ModernCard(
            "Total Lecturas", "0", "Período seleccionado", "📊", "blue"
        )
        self.hist_valid_card = ModernCard(
            "Lecturas Válidas", "0", "Sin errores", "✓", "green"
        )
        self.hist_error_card = ModernCard(
            "Lecturas Erróneas", "0", "Con problemas", "✗", "red"
        )
        self.hist_avg_card = ModernCard(
            "Nivel Promedio", "--", "Promedio del período", "📈", "purple"
        )

        stats_cards_layout.addWidget(self.hist_total_card)
        stats_cards_layout.addWidget(self.hist_valid_card)
        stats_cards_layout.addWidget(self.hist_error_card)
        stats_cards_layout.addWidget(self.hist_avg_card)
        layout.addLayout(stats_cards_layout)

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

        table_header = QLabel("📋 Registros de Lecturas")
        table_header.setStyleSheet("font-size: 18px; font-weight: 700; color: #0f172a;")
        table_layout.addWidget(table_header)

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(7)
        self.history_table.setHorizontalHeaderLabels(
            ["#", "⏰ Hora", "📏 Nivel", "📊 %", "🎯 Estado", "💧 Estado Fuga", "✓"]
        )

        self.history_table.setColumnWidth(0, 50)
        self.history_table.setColumnWidth(1, 120)
        self.history_table.setColumnWidth(2, 100)
        self.history_table.setColumnWidth(3, 80)
        self.history_table.setColumnWidth(4, 120)
        self.history_table.setColumnWidth(5, 150)
        self.history_table.setColumnWidth(6, 60)

        self.history_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.history_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.setShowGrid(False)

        self.history_table.setStyleSheet(
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
        """
        )

        self.history_table.setMinimumHeight(400)
        table_layout.addWidget(self.history_table)

        self.pagination_label = QLabel("Mostrando 0 registros")
        self.pagination_label.setStyleSheet("color: #64748b; font-size: 12px;")
        table_layout.addWidget(self.pagination_label)

        layout.addWidget(table_frame)
        self.setWidget(content)

    def load_historical_data(self):
        try:
            if not self.parent_app or not self.parent_app.db_manager:
                return

            time_filter = self.time_combo.currentText()
            hours_map = {
                "Última hora": 1,
                "Últimas 6 horas": 6,
                "Últimas 24 horas": 24,
                "Últimos 7 días": 168,
            }
            hours = hours_map.get(time_filter, 24)

            readings = self.parent_app.db_manager.get_recent_readings(
                hours=hours, limit=200
            )

            type_filter = self.type_combo.currentText()
            if type_filter == "Solo válidas":
                readings = [r for r in readings if r.get("valido", False)]
            elif type_filter == "Solo con errores":
                readings = [r for r in readings if not r.get("valido", True)]

            self.display_readings(readings)
            self.update_stats(readings)

        except Exception as e:
            print(f"❌ Error cargando datos históricos: {e}")

    def display_readings(self, readings):
        self.history_table.setRowCount(0)

        for i, reading in enumerate(reversed(readings)):
            row_pos = self.history_table.rowCount()
            self.history_table.insertRow(row_pos)

            timestamp = reading.get("timestamp", datetime.now())
            if isinstance(timestamp, str):
                timestamp = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            time_str = timestamp.strftime("%H:%M:%S")

            nivel = reading.get("nivel")
            nivel_str = f"{nivel:.1f} cm" if nivel is not None else "N/A"

            porcentaje = reading.get("porcentaje")
            porcentaje_str = f"{porcentaje:.1f}%" if porcentaje is not None else "N/A"

            estado = reading.get("estado", "N/A")
            estado_fuga = reading.get("estado_fuga", "N/A")
            valido = reading.get("valido", False)

            items = [
                QTableWidgetItem(str(i + 1)),
                QTableWidgetItem(time_str),
                QTableWidgetItem(nivel_str),
                QTableWidgetItem(porcentaje_str),
                QTableWidgetItem(estado),
                QTableWidgetItem(estado_fuga),
                QTableWidgetItem("✓" if valido else "✗"),
            ]

            for col, item in enumerate(items):
                item.setTextAlignment(Qt.AlignCenter)

                if col == 4:
                    if estado == "Lleno":
                        item.setBackground(QColor(254, 226, 226))
                    elif estado == "Medio":
                        item.setBackground(QColor(220, 252, 231))
                    elif estado == "Bajo":
                        item.setBackground(QColor(254, 243, 199))
                    elif estado == "MuyBajo":
                        item.setBackground(QColor(254, 226, 226))

                elif col == 6:
                    item.setBackground(
                        QColor(220, 252, 231) if valido else QColor(254, 226, 226)
                    )

                self.history_table.setItem(row_pos, col, item)

        self.pagination_label.setText(f"Mostrando {len(readings)} registros")

    def update_stats(self, readings):
        total = len(readings)
        validas = sum(1 for r in readings if r.get("valido", False))
        errores = total - validas

        niveles = [
            r.get("porcentaje", 0) for r in readings if r.get("porcentaje") is not None
        ]
        promedio = sum(niveles) / len(niveles) if niveles else 0

        self.hist_total_card.update_value(str(total))
        self.hist_valid_card.update_value(str(validas))
        self.hist_error_card.update_value(str(errores))
        self.hist_avg_card.update_value(f"{promedio:.1f}%")

    def add_reading(self, data):
        current_rows = self.history_table.rowCount()
        if current_rows >= 50:
            self.history_table.removeRow(0)

        self.history_table.insertRow(current_rows)

    def export_to_csv(self):
        try:
            from datetime import datetime

            filename = f"lecturas_tanque_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            print(f"📤 Exportando a {filename}...")
        except Exception as e:
            print(f"❌ Error exportando CSV: {e}")

    def clear_history(self):
        self.history_table.setRowCount(0)
        self.hist_total_card.update_value("0")
        self.hist_valid_card.update_value("0")
        self.hist_error_card.update_value("0")
        self.hist_avg_card.update_value("--")
        self.pagination_label.setText("Mostrando 0 registros")
