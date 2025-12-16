from datetime import date
from sqlmodel import Field, SQLModel
from pydantic import BaseModel

class Cancion(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    titulo: str = Field(index=True, max_length=50)
    fecha_estreno: date | None = Field(nullable=True)

# dto classes
class CancionCreate(BaseModel):
    titulo: str
    # fecha de estreno posterior a la fecha actual con Annotated
    fecha_estreno: date | None = None

class CancionUpdate(BaseModel):
    titulo: str | None = None
    fecha_estreno: date | None = None

class CancionResponse(BaseModel):
    id: int
    titulo: str
    fecha_estreno: date | None = None

# mapping functions
def map_cancion_to_response(cancion: Cancion) -> CancionResponse:
    return CancionResponse(
        id=cancion.id,
        titulo=cancion.titulo,
        fecha_estreno=cancion.fecha_estreno
    )

def map_create_to_cancion(cancion_create: CancionCreate) -> Cancion:
    return Cancion(
        titulo=cancion_create.titulo,
        fecha_estreno=cancion_create.fecha_estreno
    )

def map_update_to_cancion(cancion: Cancion, cancion_update: CancionUpdate) -> Cancion:
    if cancion_update.titulo is not None:
        cancion.titulo = cancion_update.titulo
    if cancion_update.fecha_estreno is not None:
        cancion.fecha_estreno = cancion_update.fecha_estreno
    return cancion
