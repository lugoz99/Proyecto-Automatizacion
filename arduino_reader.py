"""
Lector de Arduino con puerto serial
"""

import serial
import time
from datetime import datetime
from config import settings
from models import TankReading


class ArduinoReader:
    """Lector del Arduino"""

    def __init__(self):
        self.port = settings.ARDUINO_PORT
        self.baudrate = settings.ARDUINO_BAUDRATE
        self.arduino = None
        self.connect()

    def connect(self):
        """Conectar al Arduino"""
        try:
            self.arduino = serial.Serial(
                port=self.port, baudrate=self.baudrate, timeout=1
            )
            print(f"✅ Arduino conectado en {self.port}")
            time.sleep(2)
        except Exception as e:
            print(f"❌ Error conectando Arduino: {e}")
            self.arduino = None

    def read_data(self) -> TankReading | None:
        """
        Leer datos del Arduino

        Formato esperado:
        NIVEL:7.5,PERC:75.0,ESTADO:Lleno,HUM:850,FUGA:NoFuga,VALIDO:1,DIST:5.5,OK:100,ERR:2
        """
        if not self.arduino:
            return None

        try:
            if self.arduino.in_waiting > 0:
                line = self.arduino.readline().decode("utf-8", errors="ignore").strip()

                if not line or "Sistema Iniciado" in line:
                    return None

                # Parsear línea
                data = self._parse_line(line)
                if data:
                    return TankReading(**data)

        except Exception as e:
            print(f"❌ Error leyendo Arduino: {e}")
            self.connect()

        return None

    def _parse_line(self, line: str) -> dict | None:
        """Parsear línea del Arduino"""
        try:
            data = {"timestamp": datetime.now(), "lecturas_ok": 0, "lecturas_error": 0}

            # Separar por comas
            parts = line.split(",")

            for part in parts:
                if ":" not in part:
                    continue

                key, value = part.split(":", 1)
                key = key.strip()
                value = value.strip()

                # Parsear cada campo
                if key == "NIVEL":
                    data["nivel"] = float(value) if value != "-1" else None

                elif key == "PERC":
                    data["porcentaje"] = float(value) if value != "-1" else None

                elif key == "ESTADO":
                    data["estado"] = value

                elif key == "HUM":
                    data["humedad"] = int(value) if value != "-1" else 0

                elif key == "FUGA":
                    data["estado_fuga"] = value

                elif key == "VALIDO":
                    data["valido"] = value == "1"

                elif key == "DIST":
                    data["distancia"] = float(value) if value != "-1" else None

                elif key == "OK":
                    data["lecturas_ok"] = int(value)

                elif key == "ERR":
                    data["lecturas_error"] = int(value)

            # Validar campos mínimos
            if "valido" in data and "estado" in data:
                return data

            return None

        except Exception as e:
            print(f"❌ Error parseando línea: {e}")
            return None

    def is_connected(self) -> bool:
        """Verificar conexión"""
        return self.arduino is not None and self.arduino.is_open

    def close(self):
        """Cerrar conexión"""
        if self.arduino:
            self.arduino.close()
            print("🔌 Arduino desconectado")
