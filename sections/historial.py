from datetime import datetime
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
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

from widgets.modern_card import ModernCard


class HistorialSection(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        self.setStyleSheet("border: none;")

        self.historical_data = []
        self.setup_ui()

    def setup_ui(self):
        content = QWidget()
        layout = QVBoxLayout(content)
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

        # History table
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

        # Buttons
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
            }
            QPushButton:hover {
                background: #e2e8f0;
                border-color: #cbd5e1;
            }
        """
        )
        search_btn.setCursor(Qt.PointingHandCursor)
        header_layout.addWidget(search_btn)

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
            }
            QPushButton:hover {
                background: #bfdbfe;
                border-color: #60a5fa;
            }
        """
        )
        export_btn.setCursor(Qt.PointingHandCursor)
        header_layout.addWidget(export_btn)

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
        """
        )
        stats_layout.addWidget(self.historial_error_readings_label)

        stats_layout.addStretch()
        table_layout.addLayout(stats_layout)

        # Table
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(7)
        self.history_table.setHorizontalHeaderLabels(
            ["#", "⏰ Hora", "📏 Nivel", "📊 %", "🎯 Estado", "💧 Sensor", "✓"]
        )

        # Set column widths
        self.history_table.setColumnWidth(0, 50)
        self.history_table.setColumnWidth(1, 120)
        self.history_table.setColumnWidth(2, 100)
        self.history_table.setColumnWidth(3, 80)
        self.history_table.setColumnWidth(4, 120)
        self.history_table.setColumnWidth(5, 100)
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

        self.history_table.setMinimumHeight(450)
        table_layout.addWidget(self.history_table)

        # Pagination
        pagination_layout = QHBoxLayout()
        self.rows_label = QLabel("Mostrando 0 de 0 registros")
        self.rows_label.setStyleSheet("color: #64748b; font-size: 12px;")
        pagination_layout.addWidget(self.rows_label)
        pagination_layout.addStretch()
        table_layout.addLayout(pagination_layout)

        layout.addWidget(table_frame)
        self.setWidget(content)

    def add_reading(self, data):
        timestamp = datetime.now().strftime("%H:%M:%S")
        row_num = self.history_table.rowCount() + 1

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

        self.history_table.insertRow(0)

        for col, value in enumerate(row_data):
            item = QTableWidgetItem(value)
            item.setTextAlignment(Qt.AlignCenter)

            if col == 0:  # Row number
                item.setForeground(QColor(100, 116, 139))
                font = QFont("Segoe UI", 11, QFont.Bold)
                item.setFont(font)

            if col == 4:  # Estado column
                item.setBackground(bg_color)
                font = QFont("Segoe UI", 12, QFont.Bold)
                item.setFont(font)

            if col == 6:  # Valid column
                item.setBackground(valid_color)
                font = QFont("Segoe UI", 14, QFont.Bold)
                item.setFont(font)

            self.history_table.setItem(0, col, item)

        self.history_table.setRowHeight(0, 50)

        # Limit rows
        if self.history_table.rowCount() > 50:
            self.history_table.removeRow(50)

        self.update_stats()

    def update_stats(self):
        total = self.history_table.rowCount()
        valid_count = sum(
            1 for i in range(total) if self.history_table.item(i, 6).text() == "✓"
        )
        error_count = total - valid_count

        self.historial_total_readings_label.setText(f"Total: {total} lecturas")
        self.historial_valid_readings_label.setText(f"Válidas: {valid_count}")
        self.historial_error_readings_label.setText(f"Errores: {error_count}")
        self.rows_label.setText(f"Mostrando {min(total, 50)} de {total} registros")

        # Update cards
        self.hist_total_card.update_value(str(total))
        self.hist_valid_card.update_value(str(valid_count))
        self.hist_error_card.update_value(str(error_count))

        if total > 0:
            percentages = [
                float(self.history_table.item(i, 3).text().rstrip("%"))
                for i in range(total)
            ]
            avg = sum(percentages) / total
            self.hist_avg_card.update_value(f"{avg:.1f}%")
        else:
            self.hist_avg_card.update_value("--")

    def clear_history(self):
        self.history_table.setRowCount(0)
        self.update_stats()
