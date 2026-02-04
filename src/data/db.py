from dotenv import load_dotenv
import os
import time

from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.exc import OperationalError

from models.cancion import Cancion

load_dotenv()

db_user: str = os.getenv("DB_USER", "quevedo")  
db_password: str = os.getenv("DB_PASSWORD", "1234")
db_server: str = os.getenv("DB_SERVER", "fastapi-db-canciones")
db_port: int = os.getenv("DB_PORT", 5432)
db_name: str = os.getenv("DB_NAME", "cancionesdb")

DATABASE_URL = f"postgresql+psycopg2://{db_user}:{db_password}@{db_server}:{db_port}/{db_name}"
engine = create_engine(os.getenv("DB_URL", DATABASE_URL), echo=True)


def get_session():
    with Session(engine) as session:
        yield session


def init_db(retries: int = 10, delay: int = 2):
    """
    Inicializa la base de datos esperando a que MySQL esté disponible.
    """
    for attempt in range(1, retries + 1):
        try:
            print(f"Intento {attempt}: conectando a MySQL...")
            
            SQLModel.metadata.drop_all(engine)
            SQLModel.metadata.create_all(engine)

            with Session(engine) as session:
                session.add(Cancion(id=1, titulo="Rivers in the desert", artista="Lyn", fecha_lanzamiento="2017-01-17"))
                session.add(Cancion(id=2, titulo="Last surprise", artista="Lyn", fecha_lanzamiento="2017-01-17"))
                session.add(Cancion(id=3, titulo="Bajan", artista="Pescado Rabioso", fecha_lanzamiento="1973-05-07"))
                session.add(Cancion(id=4, titulo="Fermín", artista="Almendra", fecha_lanzamiento="1969-11-30"))
                session.add(Cancion(id=5, titulo="Bubbles", artista="Jenny01", fecha_lanzamiento="2006-04-01"))
                session.commit()

            print("Base de datos inicializada correctamente")
            return

        except OperationalError:
            print(f"MySQL no está listo. Reintentando en {delay} segundos...")
            time.sleep(delay)

    raise Exception("No se pudo conectar a MySQL tras varios intentos")