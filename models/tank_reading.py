from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TankReading(BaseModel):
    """Modelo de datos para lecturas del tanque"""

    timestamp: datetime = Field(default_factory=datetime.now)
    nivel: Optional[float] = None
    porcentaje: Optional[float] = None
    estado: str
    humedad: int
    estado_fuga: str
    valido: bool
    distancia: Optional[float] = None
    lecturas_ok: int = 0
    lecturas_error: int = 0

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
