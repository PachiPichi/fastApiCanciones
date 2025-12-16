from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select

from models.cancion import Cancion, CancionCreate, CancionResponse,  map_cancion_to_response, map_create_to_cancion
from data.db import init_db, get_session
from data.canciones_repository import CancionesRepository


import uvicorn


@asynccontextmanager
async def lifespan(application: FastAPI):
    init_db()
    yield


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI(lifespan=lifespan)


@app.get("/canciones", response_model=list[CancionResponse])
def lista_canciones(session: SessionDep):
    repo = CancionesRepository(session)
    canciones = repo.get_all_canciones()
    return [map_cancion_to_response(cancion) for cancion in canciones]

@app.post("/canciones", response_model=CancionResponse)
def nueva_cancion(cancion_create: CancionCreate, session: SessionDep):
    repo = CancionesRepository(session)
    cancion = map_create_to_cancion(cancion_create)
    cancion_creada = repo.create_cancion(cancion)
    return map_cancion_to_response(cancion_creada)


@app.get("/canciones/{cancion_id}", response_model=CancionResponse)
def cancion_por_id(cancion_id: int, session: SessionDep):
    repo = CancionesRepository(session)
    cancion_encontrada = repo.get_cancion(cancion_id)
    if not cancion_encontrada:
        raise HTTPException(status_code=404, detail="Cancion no encontrada")
    return map_cancion_to_response(cancion_encontrada)

@app.delete("/canciones/{cancion_id}", status_code=204)
def borrar_cancion(cancion_id: int, session: SessionDep):
    repo = CancionesRepository(session)
    cancion_encontrada = repo.get_cancion(cancion_id)
    if not cancion_encontrada:
        raise HTTPException(status_code=404, detail="Cancion no encontrada")
    repo.delete_cancion(cancion_id)
    return None


@app.patch("/canciones/{cancion_id}", response_model=Cancion)
def cambia_cancion(cancion_id: int, cancion: Cancion, session: SessionDep):
    repo = CancionesRepository(session)
    cancion_encontrada = repo.get_cancion(cancion_id)
    if not cancion_encontrada:
        raise HTTPException(status_code=404, detail="Cancion no encontrada")
    cancion_data = cancion.model_dump(exclude_unset=True)
    cancion_encontrada.sqlmodel_update(cancion_data)
    repo.update_cancion(cancion_encontrada.id, cancion_data)
    return cancion_encontrada

@app.put("/canciones", response_model=Cancion)
def cambia_cancion(cancion: Cancion, session: SessionDep):
    repo = CancionesRepository(session)
    cancion_encontrada = repo.get_cancion(cancion.id)
    if not cancion_encontrada:
        raise HTTPException(status_code=404, detail="Cancion no encontrada")
    cancion_data = cancion.model_dump()
    cancion_encontrada.sqlmodel_update(cancion_data)
    repo.update_cancion(cancion_encontrada.id, cancion_data)
    return cancion_encontrada


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=3000, reload=True)