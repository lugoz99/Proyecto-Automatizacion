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

        self.animation = QPropertyAnimation(self, b"water_level")
        self.animation.setDuration(900)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)

    def get_water_level(self):
        return self._water_level

    def set_water_level(self, value):
        self._water_level = value
        self.update()

    water_level = pyqtProperty(float, get_water_level, set_water_level)

    def update_water_level(self, target_level, estado, valido):
        self._target_level = target_level
        self.estado = estado
        self.valido = valido

        self.animation.stop()
        self.animation.setStartValue(self._water_level)
        self.animation.setEndValue(target_level)
        self.animation.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()

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

        tank_width = width * 0.70
        tank_height = height * 0.88
        tank_x = (width - tank_width) / 2
        tank_y = (height - tank_height) / 2 + 10

        painter.setPen(QPen(color, 4))
        painter.setBrush(QColor(255, 255, 255))
        painter.drawRect(int(tank_x), int(tank_y), int(tank_width), int(tank_height))

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

        painter.setPen(QPen(QColor(51, 65, 85)))
        painter.setFont(QFont("Segoe UI", 22, QFont.Bold))

        text = f"{self._water_level:.1f}%"
        painter.drawText(0, 0, width, int(tank_y - 5), Qt.AlignCenter, text)
