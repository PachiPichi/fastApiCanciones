from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from sqlmodel import Session
from models.cancion import Cancion, CancionCreate, CancionResponse, map_cancion_to_response, map_create_to_cancion

from data.canciones_repository import CancionesRepository
from data.db import get_session

router = APIRouter(prefix="/api/canciones", tags=["canciones"])

SessionDep = Annotated[Session, Depends(get_session)]

@router.get("/", response_model=list[CancionResponse])
async def lista_canciones(session: SessionDep):
    repo = CancionesRepository(session)
    canciones = repo.get_all_canciones()
    return [map_cancion_to_response(cancion) for cancion in canciones]

@router.post("/", response_model=CancionResponse)
async def nueva_cancion(cancion_create: CancionCreate, session: SessionDep):
    repo = CancionesRepository(session)
    cancion = map_create_to_cancion(cancion_create)
    cancion_creada = repo.create_cancion(cancion)
    return map_cancion_to_response(cancion_creada)

@router.get("/{cancion_id}", response_model=CancionResponse)
async def cancion_por_id(cancion_id: int, session: SessionDep):
    repo = CancionesRepository(session)
    cancion_encontrada = repo.get_cancion(cancion_id)
    if not cancion_encontrada:
        raise HTTPException(status_code=404, detail="Cancion no encontrada")
    return map_cancion_to_response(cancion_encontrada)

@router.delete("/{cancion_id}", status_code=204)
async def borrar_cancion(cancion_id: int, session: SessionDep):
    repo = CancionesRepository(session)
    cancion_encontrada = repo.get_cancion(cancion_id)
    if not cancion_encontrada:
        raise HTTPException(status_code=404, detail="Cancion no encontrada")
    repo.delete_cancion(cancion_id)
    return None

@router.patch("/{cancion_id}", response_model=Cancion)
async def cambia_cancion(cancion_id: int, cancion: Cancion, session: SessionDep):
    repo = CancionesRepository(session)
    cancion_encontrada = repo.get_cancion(cancion_id)
    if not cancion_encontrada:
        raise HTTPException(status_code=404, detail="Cancion no encontrada")
    cancion_data = cancion.model_dump(exclude_unset=True)
    cancion_encontrada.sqlmodel_update(cancion_data)
    repo.update_cancion(cancion_encontrada.id, cancion_data)
    return cancion_encontrada

@router.put("/", response_model=Cancion)
async def cambia_cancion(cancion: Cancion, session: SessionDep):
    repo = CancionesRepository(session)
    cancion_encontrada = repo.get_cancion(cancion.id)
    if not cancion_encontrada:
        raise HTTPException(status_code=404, detail="Cancion no encontrada")
    cancion_data = cancion.model_dump(exclude_unset=True)
    cancion_encontrada.sqlmodel_update(cancion_data)
    repo.update_cancion(cancion_encontrada.id, cancion_data)
    return cancion_encontrada