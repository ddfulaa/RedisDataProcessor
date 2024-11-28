import asyncio
import redis.asyncio as aioredis
from redis.exceptions import ResponseError
from sqlmodel import SQLModel
from brqm import *
from config import *

# Inicialización de la base de datos
def init_db():
    SQLModel.metadata.create_all(ENGINE)

async def process_messages():
    """
    Bucle principal para procesar mensajes de la cola de Redis.
    """
    redis_client = aioredis.Redis(host=REDIS_HOST, port=REDIS_PORT)
    await configurar_grupo(redis_client, STREAM_NAME, GROUP_NAME)

    while True:
        message_id, data = await buscar_mensajes(redis_client, STREAM_NAME, GROUP_NAME, CONSUMER_NAME, IDLE_TIME, BLOCK_TIME)
        if message_id and data:
            await procesar_mensaje(redis_client, message_id, data, STREAM_NAME, GROUP_NAME, QUERY_KEY, 'result', None)
        else:
            logger.debug("No hay mensajes pendientes o nuevos para procesar.")

# Inicializa la base de datos y ejecuta el consumidor
if __name__ == "__main__":
    init_db()
    asyncio.run(process_messages())
