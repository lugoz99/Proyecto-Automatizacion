import sys
from PyQt5.QtWidgets import QApplication
from tank_monitor_app import TankMonitorApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = TankMonitorApp()
    window.show()
    sys.exit(app.exec_())
