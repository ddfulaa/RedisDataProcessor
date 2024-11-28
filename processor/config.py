import os
# Constantes de configuración
REDIS_HOST = "redis"
REDIS_PORT = 6379
STREAM_NAME = "queue_a"
GROUP_NAME = "processors"
CONSUMER_NAME = os.getenv("CONSUMER_NAME", "processor_default")
IDLE_TIME = 120000  # Tiempo mínimo en ms antes de reclamar un mensaje pendiente
BLOCK_TIME = 5000  # Tiempo de espera en ms para leer nuevos mensajes
QUERY_KEY = b"query"