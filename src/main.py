from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session, select

from models.cancion import Cancion, CancionCreate, CancionResponse,  map_cancion_to_response, map_create_to_cancion
from data.db import init_db, get_session
from data.canciones_repository import CancionesRepository
from routers.api_canciones_router import router as api_canciones_router


import uvicorn


@asynccontextmanager
async def lifespan(application: FastAPI):
    init_db()
    yield


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="src/templates")

app.include_router(api_canciones_router)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/canciones", response_class=HTMLResponse)
async def ver_canciones(request: Request, session: SessionDep):
    repo = CancionesRepository(session)
    canciones = repo.get_all_canciones()
    return templates.TemplateResponse("canciones/canciones.html", {"request": request, "canciones": canciones})

@app.get("/canciones/new", response_class=HTMLResponse)
async def nueva_cancion_form(request: Request):
    """Formulario para añadir una cancion nueva"""
    return templates.TemplateResponse("canciones/cancion_form.html", {
        "request": request,
        "cancion": Cancion()
    })

@app.post("/canciones/new", response_class=HTMLResponse)
async def nueva_cancion(request: Request, session: SessionDep):
    """Crear una nueva cancion desde el formulario"""
    form_data = await request.form()
    titulo = form_data.get("titulo")
    artista = form_data.get("artista")
    fecha_lanzamiento = form_data.get("fecha_lanzamiento") or None

    cancion_create = CancionCreate(
        titulo=titulo,
        artista=artista,
        fecha_lanzamiento=fecha_lanzamiento
    )
    repo = CancionesRepository(session)
    cancion = map_create_to_cancion(cancion_create)
    repo.create_cancion(cancion)
    return RedirectResponse(url="/canciones", status_code=303)


@app.get("/canciones/{cancion_id}", response_class=HTMLResponse)
async def cancion_por_id(cancion_id: int, request: Request,session: SessionDep):
    repo = CancionesRepository(session)
    cancion_encontrada = repo.get_cancion(cancion_id)
    if not cancion_encontrada:
        raise HTTPException(status_code=404, detail="Cancion no encontrada")
    cancion_response = map_cancion_to_response(cancion_encontrada)
    return templates.TemplateResponse("canciones/cancion_detalle.html", {
        "request": request,
        "cancion": cancion_response
    })

# @app.delete("/canciones/{cancion_id}", status_code=204)
# def borrar_cancion(cancion_id: int, session: SessionDep):
#     repo = CancionesRepository(session)
#     cancion_encontrada = repo.get_cancion(cancion_id)
#     if not cancion_encontrada:
#         raise HTTPException(status_code=404, detail="Cancion no encontrada")
#     repo.delete_cancion(cancion_id)
#     return None


# @app.patch("/canciones/{cancion_id}", response_model=Cancion)
# def cambia_cancion(cancion_id: int, cancion: Cancion, session: SessionDep):
#     repo = CancionesRepository(session)
#     cancion_encontrada = repo.get_cancion(cancion_id)
#     if not cancion_encontrada:
#         raise HTTPException(status_code=404, detail="Cancion no encontrada")
#     cancion_data = cancion.model_dump(exclude_unset=True)
#     cancion_encontrada.sqlmodel_update(cancion_data)
#     repo.update_cancion(cancion_encontrada.id, cancion_data)
#     return cancion_encontrada

# @app.put("/canciones", response_model=Cancion)
# def cambia_cancion(cancion: Cancion, session: SessionDep):
#     repo = CancionesRepository(session)
#     cancion_encontrada = repo.get_cancion(cancion.id)
#     if not cancion_encontrada:
#         raise HTTPException(status_code=404, detail="Cancion no encontrada")
#     cancion_data = cancion.model_dump()
#     cancion_encontrada.sqlmodel_update(cancion_data)
#     repo.update_cancion(cancion_encontrada.id, cancion_data)
#     return cancion_encontrada


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=3000, reload=True)