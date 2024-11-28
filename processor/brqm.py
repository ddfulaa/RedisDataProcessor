# BRQM: Basic Redis Queue Manager
import processor_lib
from redis.exceptions import ResponseError
import logging

# Configuración de logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("BQRM")




async def configurar_grupo(redis_client, stream_name, group_name):
    """
    Configura el grupo de consumidores para la cola si no existe.
    """
    try:
        await redis_client.xgroup_create(stream_name, group_name, id="$", mkstream=True)
        logger.info(f"Grupo {group_name} creado en la cola {stream_name}.")
    except ResponseError as e:
        if "BUSYGROUP" in str(e):
            logger.info(f"Grupo {group_name} ya existe en la cola {stream_name}.")
        else:
            raise


async def reclamar_mensaje_pendiente(redis_client, stream_name, group_name, consumer_name, idle_time):
    """
    Reclama un mensaje pendiente del PEL si existe alguno con tiempo suficiente sin procesar.

    :param redis_client: Cliente Redis.
    :return: Un mensaje pendiente (ID y datos) o None si no hay mensajes pendientes.
    """
    try:
        pending_messages = await redis_client.xautoclaim(
            name=stream_name,
            groupname=group_name,
            consumername=consumer_name,
            min_idle_time=idle_time,
            start_id="0-0",
            count=1
        )
        if pending_messages and pending_messages[1]:
            message_id, data = pending_messages[1][0]
            logger.debug(f"Mensaje pendiente reclamado: {message_id}")
            return message_id, data
    except Exception as e:
        logger.error(f"Error reclamando mensajes pendientes: {e}")
    return None, None


async def leer_mensaje_nuevo(redis_client, stream_name, group_name, consumer_name, block_time):
    """
    Lee un nuevo mensaje de la cola si no hay mensajes pendientes.

    :param redis_client: Cliente Redis.
    :return: Un mensaje nuevo (ID y datos) o None si no hay mensajes nuevos.
    """
    try:
        messages = await redis_client.xreadgroup(
            groupname=group_name,
            consumername=consumer_name,
            streams={stream_name: ">"},
            count=1,
            block=block_time
        )
        if messages:
            stream, entries = messages[0]
            message_id, data = entries[0]
            logger.debug(f"Mensaje nuevo leído: {message_id}")
            return message_id, data
    except Exception as e:
        logger.error(f"Error leyendo mensajes nuevos: {e}")
    return None, None


async def procesar_mensaje(redis_client, message_id, data, input_stream_name, group_name, query_key, answer_key='result', output_stream_name=None):
    """
    Procesa un mensaje de la cola y publica el resultado en la cola de salida.

    :param redis_client: Cliente Redis.
    :param message_id: ID del mensaje procesado.
    :param data: Contenido del mensaje.
    """
    try:
        query = data[query_key].decode("utf-8")
        
        processed_query = await processor_lib.procesador(query)

        if output_stream_name is not None:
            # Publicar resultado en la cola de salida
            await redis_client.xadd(output_stream_name, {answer_key: processed_query})
        
        logger.info(f"Mensaje procesado: {message_id} - {processed_query}")

        # Confirmar mensaje como procesado
        ack = await redis_client.xack(input_stream_name, group_name, message_id)
        if ack:
            await redis_client.incr(f"{input_stream_name}:processed_messages")

            # Eliminar mensaje procesado
            await redis_client.xdel(input_stream_name, message_id)
            logger.info(f"Mensaje eliminado: {message_id}")
        else:
            raise
    except Exception as e:
        # Incrementar contador de mensajes rechazados si hay un error
        await redis_client.incr(f"{input_stream_name}:rejected_messages")
        logger.error(f"Error procesando mensaje {message_id}: {e}")


async def buscar_mensajes(redis_client, stream_name, group_name, consumer_name, idle_time, block_time):
    """
    Busca mensajes para procesar, priorizando mensajes pendientes.
    """
    message_id, data = await reclamar_mensaje_pendiente(redis_client, stream_name, group_name, consumer_name, idle_time)
    if not message_id:
        message_id, data = await leer_mensaje_nuevo(redis_client, stream_name, group_name, consumer_name, block_time)
    return message_id, data