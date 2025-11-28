from PyQt5.QtWidgets import QFrame, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt


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
        logo_container = QLabel("💧 TankMonitor")
        logo_container.setStyleSheet(
            """
            color: white;
            font-size: 22px;
            font-weight: bold;
            font-family: 'Segoe UI', Arial;
            padding: 30px 20px;
            background: transparent;
            border-bottom: 1px solid #334155;
        """
        )
        logo_container.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_container)

        # Menu Items
        self.menu_items = []
        self.menu_data = [
            ("📊", "Dashboard"),
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
        for btn in self.menu_items:
            btn.setProperty("active", False)
            self.update_button_style(btn)

        self.menu_items[index].setProperty("active", True)
        self.update_button_style(self.menu_items[index])
        self.current_active = index

        if self.parent_window:
            self.parent_window.change_section(index)
