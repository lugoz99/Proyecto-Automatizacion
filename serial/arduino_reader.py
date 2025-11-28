import serial
from datetime import datetime
from PyQt6.QtCore import QThread, pyqtSignal
import re


class ArduinoReader(QThread):
    data_received = pyqtSignal(dict)

    def __init__(self, port="COM5", baudrate=115200):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.running = True
        self.arduino = None

    def run(self):
        try:
            self.arduino = serial.Serial(self.port, self.baudrate, timeout=1)
            print(f"✅ Arduino conectado en {self.port}")
        except Exception as e:
            print(f"❌ Error conectando Arduino: {e}")
            return

        while self.running:
            try:
                if self.arduino and self.arduino.in_waiting > 0:
                    line = (
                        self.arduino.readline().decode("utf-8", errors="ignore").strip()
                    )
                    if line and "Sistema Iniciado" not in line and ":" in line:
                        data = self.parse_line(line)
                        if data:
                            self.data_received.emit(data)
            except Exception as e:
                print(f"❌ Error leyendo Arduino: {e}")
                # Intentar reconectar
                try:
                    self.arduino.close()
                    self.arduino = serial.Serial(self.port, self.baudrate, timeout=1)
                except:
                    pass

    def parse_line(self, line: str) -> dict | None:
        try:
            data = {"timestamp": datetime.now(), "lecturas_ok": 0, "lecturas_error": 0}

            # Parsear cada campo individualmente
            fields = {
                "NIVEL": "nivel",
                "PERC": "porcentaje",
                "ESTADO": "estado",
                "HUM": "humedad",
                "FUGA": "estado_fuga",
                "VALIDO": "valido",
                "DIST": "distancia",
                "OK": "lecturas_ok",
                "ERR": "lecturas_error",
            }

            for field, key in fields.items():
                pattern = f"{field}:([^,]+)"
                match = re.search(pattern, line)
                if match:
                    value = match.group(1).strip()

                    # Conversión de tipos
                    if key in ["nivel", "porcentaje", "distancia"]:
                        data[key] = float(value) if value != "-1" else None
                    elif key in ["humedad", "lecturas_ok", "lecturas_error"]:
                        data[key] = int(value) if value != "-1" else 0
                    elif key == "valido":
                        data[key] = value == "1"
                    else:
                        data[key] = value

            # Validar que tenemos datos mínimos
            if "estado" in data and "humedad" in data:
                # Convertir estados de fuga a más entendibles
                if data.get("estado_fuga"):
                    data["estado_fuga"] = self.convert_fuga_state(data["estado_fuga"])
                return data

            return None

        except Exception as e:
            print(f"❌ Error parseando línea: {e} - Línea: {line}")
            return None

    def convert_fuga_state(self, estado):
        """Convertir estados técnicos a entendibles para usuario"""
        estados = {
            "NoFuga": "✅ SIN FUGAS",
            "FugaMedia": "⚠️ HUMEDAD ALTA",
            "FugaAlta": "🚨 FUGA DETECTADA",
        }
        return estados.get(estado, estado)

    def stop(self):
        self.running = False
        if self.arduino and self.arduino.is_open:
            self.arduino.close()
        self.quit()
        self.wait()
