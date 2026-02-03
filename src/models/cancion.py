from datetime import date
from sqlmodel import Field, SQLModel
from pydantic import BaseModel

class Cancion(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    titulo: str = Field(index=True, max_length=50)
    artista: str = Field(index=True, max_length=50)
    fecha_lanzamiento: date | None = Field(nullable=True)

# dto classes
class CancionCreate(BaseModel):
    titulo: str
    artista: str
    # fecha de estreno posterior a la fecha actual con Annotated
    fecha_lanzamiento: date | None = None

class CancionUpdate(BaseModel):
    titulo: str | None = None
    artista: str | None = None
    fecha_lanzamiento: date | None = None

class CancionResponse(BaseModel):
    id: int
    titulo: str
    artista: str
    fecha_lanzamiento: date | None = None

# mapping functions
def map_cancion_to_response(cancion: Cancion) -> CancionResponse:
    return CancionResponse(
        id=cancion.id,
        titulo=cancion.titulo,
        artista=cancion.artista,
        fecha_lanzamiento=cancion.fecha_lanzamiento
    )

def map_create_to_cancion(cancion_create: CancionCreate) -> Cancion:
    return Cancion(
        titulo=cancion_create.titulo,
        artista=cancion_create.artista,
        fecha_lanzamiento=cancion_create.fecha_lanzamiento
    )

def map_update_to_cancion(cancion: Cancion, cancion_update: CancionUpdate) -> Cancion:
    if cancion_update.titulo is not None:
        cancion.titulo = cancion_update.titulo
    if cancion_update.artista is not None:
        cancion.artista = cancion_update.artista
    if cancion_update.fecha_lanzamiento is not None:
        cancion.fecha_lanzamiento = cancion_update.fecha_lanzamiento
    return cancion
