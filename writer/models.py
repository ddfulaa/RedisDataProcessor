from sqlmodel import SQLModel, Field

# Definición del modelo para SQLModel
class ProcessedData(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    result: str