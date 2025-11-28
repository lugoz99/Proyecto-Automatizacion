from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QPushButton,
    QComboBox,
    QDateEdit,
    QProgressBar,
    QApplication,
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
import time


class ReportesSection(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        title = QLabel("📊 Generación de Reportes")
        title.setStyleSheet(
            """
            font-size: 24px;
            font-weight: bold;
            color: #0f172a;
            margin-bottom: 20px;
        """
        )
        layout.addWidget(title)

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

        config_title = QLabel("⚙️ Configurar Reporte")
        config_title.setStyleSheet(
            "font-size: 18px; font-weight: 600; color: #0f172a; margin-bottom: 15px;"
        )
        config_layout.addWidget(config_title)

        controls_layout = QHBoxLayout()

        type_layout = QVBoxLayout()
        type_label = QLabel("Tipo de Reporte:")
        type_label.setStyleSheet("font-size: 13px; color: #64748b; margin-bottom: 5px;")
        type_layout.addWidget(type_label)

        self.report_type = QComboBox()
        self.report_type.addItems(
            [
                "📈 Reporte Diario",
                "📊 Reporte Semanal",
                "📋 Reporte Mensual",
                "🔍 Reporte Personalizado",
            ]
        )
        self.report_type.setStyleSheet(
            """
            QComboBox {
                padding: 8px 12px;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                background: white;
                min-width: 200px;
            }
        """
        )
        type_layout.addWidget(self.report_type)
        controls_layout.addLayout(type_layout)

        date_from_layout = QVBoxLayout()
        date_from_label = QLabel("Fecha Desde:")
        date_from_label.setStyleSheet(
            "font-size: 13px; color: #64748b; margin-bottom: 5px;"
        )
        date_from_layout.addWidget(date_from_label)

        self.date_from = QDateEdit()
        self.date_from.setDate(QDate.currentDate().addDays(-7))
        self.date_from.setStyleSheet(
            """
            QDateEdit {
                padding: 8px 12px;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                background: white;
                min-width: 120px;
            }
        """
        )
        date_from_layout.addWidget(self.date_from)
        controls_layout.addLayout(date_from_layout)

        date_to_layout = QVBoxLayout()
        date_to_label = QLabel("Fecha Hasta:")
        date_to_label.setStyleSheet(
            "font-size: 13px; color: #64748b; margin-bottom: 5px;"
        )
        date_to_layout.addWidget(date_to_label)

        self.date_to = QDateEdit()
        self.date_to.setDate(QDate.currentDate())
        self.date_to.setStyleSheet(
            """
            QDateEdit {
                padding: 8px 12px;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                background: white;
                min-width: 120px;
            }
        """
        )
        date_to_layout.addWidget(self.date_to)
        controls_layout.addLayout(date_to_layout)

        controls_layout.addStretch()
        config_layout.addLayout(controls_layout)
        layout.addWidget(config_frame)

        export_frame = QFrame()
        export_frame.setStyleSheet(
            """
            QFrame {
                background: white;
                border-radius: 16px;
                border: 1px solid #e2e8f0;
            }
        """
        )
        export_layout = QVBoxLayout(export_frame)
        export_layout.setContentsMargins(24, 20, 24, 20)

        export_title = QLabel("📤 Formatos de Exportación")
        export_title.setStyleSheet(
            "font-size: 18px; font-weight: 600; color: #0f172a; margin-bottom: 15px;"
        )
        export_layout.addWidget(export_title)

        format_layout = QHBoxLayout()

        formats = [
            {
                "icon": "📄",
                "text": "PDF",
                "color": "#dc2626",
                "bg": "#fef2f2",
                "border": "#fecaca",
            },
            {
                "icon": "📊",
                "text": "Excel",
                "color": "#059669",
                "bg": "#f0fdf4",
                "border": "#bbf7d0",
            },
            {
                "icon": "📋",
                "text": "CSV",
                "color": "#2563eb",
                "bg": "#eff6ff",
                "border": "#bfdbfe",
            },
            {
                "icon": "📈",
                "text": "Gráficos",
                "color": "#7c3aed",
                "bg": "#faf5ff",
                "border": "#ddd6fe",
            },
        ]

        for fmt in formats:
            format_btn = QPushButton(f"{fmt['icon']} {fmt['text']}")
            format_btn.setStyleSheet(
                f"""
                QPushButton {{
                    background: {fmt['bg']};
                    color: {fmt['color']};
                    border: 2px solid {fmt['border']};
                    padding: 15px 20px;
                    border-radius: 12px;
                    font-size: 14px;
                    font-weight: 600;
                    min-width: 120px;
                }}
                QPushButton:hover {{
                    background: {fmt['border']};
                    border-color: {fmt['color']};
                }}
            """
            )
            format_btn.setCursor(Qt.PointingHandCursor)
            format_btn.clicked.connect(
                lambda checked, f=fmt: self.generate_report(f["text"])
            )
            format_layout.addWidget(format_btn)

        export_layout.addLayout(format_layout)
        layout.addWidget(export_frame)

        progress_frame = QFrame()
        progress_frame.setStyleSheet(
            """
            QFrame {
                background: white;
                border-radius: 16px;
                border: 1px solid #e2e8f0;
            }
        """
        )
        progress_layout = QVBoxLayout(progress_frame)
        progress_layout.setContentsMargins(24, 20, 24, 20)

        progress_title = QLabel("🔄 Progreso de Generación")
        progress_title.setStyleSheet(
            "font-size: 18px; font-weight: 600; color: #0f172a; margin-bottom: 15px;"
        )
        progress_layout.addWidget(progress_title)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet(
            """
            QProgressBar {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                background: #f8fafc;
                height: 20px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3b82f6, stop:1 #1d4ed8);
                border-radius: 7px;
            }
        """
        )
        progress_layout.addWidget(self.progress_bar)

        self.progress_label = QLabel("Listo para generar reportes")
        self.progress_label.setStyleSheet(
            "font-size: 13px; color: #64748b; margin-top: 8px;"
        )
        progress_layout.addWidget(self.progress_label)

        layout.addWidget(progress_frame)

        recent_frame = QFrame()
        recent_frame.setStyleSheet(
            """
            QFrame {
                background: white;
                border-radius: 16px;
                border: 1px solid #e2e8f0;
            }
        """
        )
        recent_layout = QVBoxLayout(recent_frame)
        recent_layout.setContentsMargins(24, 20, 24, 20)

        recent_title = QLabel("📁 Reportes Recientes")
        recent_title.setStyleSheet(
            "font-size: 18px; font-weight: 600; color: #0f172a; margin-bottom: 15px;"
        )
        recent_layout.addWidget(recent_title)

        recent_reports = [
            {
                "nombre": "Reporte_Diario_20241205.pdf",
                "fecha": "05/12/2024",
                "tamaño": "2.3 MB",
                "tipo": "PDF",
            },
            {
                "nombre": "Analisis_Semanal_20241201.xlsx",
                "fecha": "01/12/2024",
                "tamaño": "1.8 MB",
                "tipo": "Excel",
            },
            {
                "nombre": "Datos_Crudos_20241128.csv",
                "fecha": "28/11/2024",
                "tamaño": "4.1 MB",
                "tipo": "CSV",
            },
        ]

        for report in recent_reports:
            report_item = self.create_report_item(report)
            recent_layout.addWidget(report_item)

        layout.addWidget(recent_frame)
        layout.addStretch()

    def generate_report(self, format_type):
        self.progress_label.setText(f"Generando reporte en formato {format_type}...")
        self.progress_bar.setValue(0)

        for i in range(101):
            self.progress_bar.setValue(i)
            QApplication.processEvents()
            time.sleep(0.02)

        self.progress_label.setText(f"✅ Reporte {format_type} generado exitosamente")

    def create_report_item(self, report):
        item_frame = QFrame()
        item_frame.setStyleSheet(
            """
            QFrame {
                background: #f8fafc;
                border-radius: 8px;
                padding: 12px 16px;
                border: 1px solid #e2e8f0;
            }
        """
        )

        item_layout = QHBoxLayout(item_frame)

        icon_map = {"PDF": "📄", "Excel": "📊", "CSV": "📋"}
        icon_label = QLabel(icon_map.get(report["tipo"], "📁"))
        icon_label.setStyleSheet("font-size: 16px;")
        item_layout.addWidget(icon_label)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)

        name_label = QLabel(report["nombre"])
        name_label.setStyleSheet("font-size: 14px; font-weight: 500; color: #1f2937;")
        info_layout.addWidget(name_label)

        meta_label = QLabel(
            f"{report['fecha']} • {report['tamaño']} • {report['tipo']}"
        )
        meta_label.setStyleSheet("font-size: 12px; color: #6b7280;")
        info_layout.addWidget(meta_label)

        item_layout.addLayout(info_layout)
        item_layout.addStretch()

        actions_layout = QHBoxLayout()

        download_btn = QPushButton("📥")
        download_btn.setStyleSheet(
            """
            QPushButton {
                background: #dbeafe;
                color: #1e40af;
                border: none;
                padding: 6px 8px;
                border-radius: 4px;
                font-size: 12px;
                min-width: 30px;
            }
            QPushButton:hover {
                background: #bfdbfe;
            }
        """
        )
        download_btn.setCursor(Qt.PointingHandCursor)
        actions_layout.addWidget(download_btn)

        delete_btn = QPushButton("🗑️")
        delete_btn.setStyleSheet(
            """
            QPushButton {
                background: #fef2f2;
                color: #dc2626;
                border: none;
                padding: 6px 8px;
                border-radius: 4px;
                font-size: 12px;
                min-width: 30px;
            }
            QPushButton:hover {
                background: #fee2e2;
            }
        """
        )
        delete_btn.setCursor(Qt.PointingHandCursor)
        actions_layout.addWidget(delete_btn)

        item_layout.addLayout(actions_layout)

        return item_frame
