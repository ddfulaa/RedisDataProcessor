import os
from sqlmodel import create_engine
# Constantes de configuración
REDIS_HOST = "redis"
REDIS_PORT = 6379
STREAM_NAME = "queue_b"
GROUP_NAME = "writers"
CONSUMER_NAME = os.getenv("CONSUMER_NAME", "writer_default")
IDLE_TIME = 120000  # Tiempo mínimo en ms antes de reclamar un mensaje pendiente
BLOCK_TIME = 5000  # Tiempo de espera en ms para leer nuevos mensajes
QUERY_KEY = b"result"
# Configuración de conexión a SQL Server
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mssql+pyodbc://sa:YourPassword123@sqlserver:1433/yourdb?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
)

ENGINE = create_engine(DATABASE_URL)