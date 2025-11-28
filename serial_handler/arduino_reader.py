# ✅ CORRECTO - Importar el módulo serial de PySerial
import serial
from datetime import datetime
from PyQt5.QtCore import QThread, pyqtSignal
import re


class ArduinoReader(QThread):
    data_received = pyqtSignal(dict)

    def __init__(self, port="COM5", baudrate=9600):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.running = True
        self.arduino = None

    def run(self):
        try:
            # ✅ Usar serial.Serial del módulo PySerial
            self.arduino = serial.Serial(self.port, self.baudrate, timeout=1)
            print(f"✅ Arduino conectado en {self.port} @ {self.baudrate} baud")
        except Exception as e:
            print(f"❌ Error conectando Arduino: {e}")
            return

        while self.running:
            try:
                if self.arduino and self.arduino.in_waiting > 0:
                    line = (
                        self.arduino.readline().decode("utf-8", errors="ignore").strip()
                    )

                    if line and self.is_valid_data_line(line):
                        data = self.parse_line(line)
                        if data:
                            self.data_received.emit(data)

            except Exception as e:
                print(f"❌ Error leyendo Arduino: {e}")
                # Intenta reconectar
                try:
                    if self.arduino:
                        self.arduino.close()
                    self.arduino = serial.Serial(self.port, self.baudrate, timeout=1)
                    print("🔄 Reconexión exitosa")
                except Exception as reconnect_error:
                    print(f"❌ Error reconectando: {reconnect_error}")
                    self.msleep(1000)

    def is_valid_data_line(self, line: str) -> bool:
        """Verifica si la línea contiene datos válidos del sensor"""
        if "Sistema Iniciado" in line or "Iniciando" in line:
            return False

        required_fields = ["NIVEL:", "PERC:", "ESTADO:"]
        return all(field in line for field in required_fields)

    def parse_line(self, line: str) -> dict | None:
        try:
            data = {
                "timestamp": datetime.now(),
                "lecturas_ok": 0,
                "lecturas_error": 0,
            }

            fields = {
                "NIVEL": ("nivel", "float"),
                "PERC": ("porcentaje", "float"),
                "ESTADO": ("estado", "str"),
                "HUM": ("humedad", "int"),
                "FUGA": ("estado_fuga", "str"),
                "VALIDO": ("valido", "bool"),
                "DIST": ("distancia", "float"),
                "OK": ("lecturas_ok", "int"),
                "ERR": ("lecturas_error", "int"),
            }

            for field, (key, tipo) in fields.items():
                pattern = f"{field}:([^,]+)"
                match = re.search(pattern, line)

                if match:
                    value = match.group(1).strip()

                    try:
                        if tipo == "float":
                            data[key] = (
                                float(value)
                                if value != "-1.0" and value != "-1"
                                else None
                            )
                        elif tipo == "int":
                            data[key] = int(float(value)) if value != "-1" else 0
                        elif tipo == "bool":
                            data[key] = value == "1" or value == "True"
                        else:
                            data[key] = value
                    except ValueError as e:
                        print(f"⚠️ Error convirtiendo {field}={value}: {e}")
                        if tipo in ["float", "int"]:
                            data[key] = None if tipo == "float" else 0
                        else:
                            data[key] = value

            required_keys = ["nivel", "porcentaje", "estado", "humedad"]
            if all(key in data for key in required_keys):
                if "estado_fuga" in data and data["estado_fuga"]:
                    data["estado_fuga"] = self.convert_fuga_state(data["estado_fuga"])
                return data
            else:
                missing = [k for k in required_keys if k not in data]
                print(f"⚠️ Datos incompletos, faltan: {missing}")
                return None

        except Exception as e:
            print(f"❌ Error parseando línea: {e}")
            print(f"   Línea problemática: {line}")
            return None

    def convert_fuga_state(self, estado: str) -> str:
        estados = {
            "NoFuga": "✅ SIN FUGAS",
            "FugaMedia": "⚠️ HUMEDAD DETECTADA",
            "FugaAlta": "🚨 FUGA ALTA",
        }
        return estados.get(estado, estado)

    def stop(self):
        print("🔌 Deteniendo lectura Arduino...")
        self.running = False

        if self.arduino and self.arduino.is_open:
            self.arduino.close()
            print("✅ Puerto serial cerrado")

        self.quit()
        self.wait()
