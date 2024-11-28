import asyncio
from config import *
from models import ProcessedData
from sqlmodel import Session



async def procesador(input: str):
    await asyncio.sleep(10)
    
    print(f"Guardando en base de datos: {input}")
    # Guardar en la base de datos
    with Session(ENGINE) as session:
        new_data = ProcessedData(result=input)
        session.add(new_data)
        session.commit()

    return True