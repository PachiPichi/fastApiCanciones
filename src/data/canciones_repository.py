from sqlmodel import Session, select
from models.cancion import Cancion

class CancionesRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def get_all_canciones(self) -> list[Cancion]:
        canciones = self.session.exec(select(Cancion)).all()
        return canciones   

    def get_cancion(self, cancion_id: int) -> Cancion:
        cancion = self.session.get(Cancion, cancion_id)
        return cancion

    def create_cancion(self, cancion: Cancion) -> Cancion:
        self.session.add(cancion)
        self.session.commit()
        self.session.refresh(cancion)
        return cancion

    def update_cancion(self, cancion_id: int, cancion_data: dict) -> Cancion:
        cancion = self.get_cancion(cancion_id)
        for key, value in cancion_data.items():
            setattr(cancion, key, value)
        self.session.commit()
        self.session.refresh(cancion)
        return cancion

    def delete_cancion(self, cancion_id: int) -> None:
        cancion = self.get_cancion(cancion_id)
        self.session.delete(cancion)
        self.session.commit()