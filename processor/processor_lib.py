import asyncio
async def procesador(input: str):
    await asyncio.sleep(10)
    return  f"Procesado: {input}"