from pymongo import MongoClient
from datetime import datetime, timedelta
import json


class MongoDBManager:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="tank_monitor"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db["lecturas"]

    def save_reading(self, data: dict):
        """Guardar lectura en la base de datos"""
        try:
            doc = data.copy()
            doc["timestamp"] = datetime.now()
            result = self.collection.insert_one(doc)
            return result.inserted_id is not None
        except Exception as e:
            print(f"❌ Error guardando en MongoDB: {e}")
            return False

    def get_recent_readings(self, hours=24, limit=100):
        """Obtener lecturas recientes con filtro de tiempo"""
        try:
            since = datetime.now() - timedelta(hours=hours)
            cursor = (
                self.collection.find({"timestamp": {"$gte": since}})
                .sort("timestamp", -1)
                .limit(limit)
            )
            return list(cursor)
        except Exception as e:
            print(f"❌ Error obteniendo lecturas: {e}")
            return []

    def get_stats(self, hours=24):
        """Obtener estadísticas de las lecturas"""
        try:
            since = datetime.now() - timedelta(hours=hours)

            pipeline = [
                {"$match": {"timestamp": {"$gte": since}}},
                {
                    "$group": {
                        "_id": None,
                        "total_lecturas": {"$sum": 1},
                        "lecturas_validas": {
                            "$sum": {"$cond": [{"$eq": ["$valido", True]}, 1, 0]}
                        },
                        "lecturas_error": {
                            "$sum": {"$cond": [{"$eq": ["$valido", False]}, 1, 0]}
                        },
                        "avg_nivel": {"$avg": "$nivel"},
                        "avg_porcentaje": {"$avg": "$porcentaje"},
                        "min_nivel": {"$min": "$nivel"},
                        "max_nivel": {"$max": "$nivel"},
                        "fugas_detectadas": {
                            "$sum": {
                                "$cond": [
                                    {"$ne": ["$estado_fuga", "✅ SIN FUGAS"]},
                                    1,
                                    0,
                                ]
                            }
                        },
                    }
                },
            ]

            result = list(self.collection.aggregate(pipeline))
            return result[0] if result else {}

        except Exception as e:
            print(f"❌ Error obteniendo estadísticas: {e}")
            return {}

    def close(self):
        """Cerrar conexión a la base de datos"""
        if self.client:
            self.client.close()
