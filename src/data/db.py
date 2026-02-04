from dotenv import load_dotenv
import os
import time

from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.exc import OperationalError

from models.cancion import Cancion

load_dotenv()

# Tomamos la URL completa si está en Render o construimos localmente
db_user: str = os.getenv("DB_USER", "quevedo")  
db_password: str = os.getenv("DB_PASSWORD", "5BqG5wOSbrMgYjZKNbAczXOJrxurLk7f")
db_server: str = os.getenv("DB_SERVER", "localhost")
db_port: int = os.getenv("DB_PORT", 5432)
db_name: str = os.getenv("DB_NAME", "cancionesdb")

DEFAULT_DATABASE_URL = f"postgresql+psycopg2://{db_user}:{db_password}@{db_server}:{db_port}/{db_name}"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)

engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


def init_db(retries: int = 10, delay: int = 3, drop_tables: bool = False):
    """
    Inicializa la base de datos esperando a que PostgreSQL esté disponible.
    drop_tables: si es True, elimina todas las tablas (solo para pruebas locales)
    """
    for attempt in range(1, retries + 1):
        try:
            print(f"[DB] Intento {attempt} de conexión a PostgreSQL...")
            # Intentar conectar
            with engine.connect() as conn:
                print("[DB] Conexión exitosa!")

            # Inicializar tablas
            if drop_tables:
                SQLModel.metadata.drop_all(engine)
            SQLModel.metadata.create_all(engine)

            # Insertar datos iniciales si no existen
            with Session(engine) as session:
                if not session.exec("SELECT 1 FROM cancion LIMIT 1").first():
                    session.add(Cancion(id=1, titulo="Rivers in the desert", artista="Lyn", fecha_lanzamiento="2017-01-17"))
                    session.add(Cancion(id=2, titulo="Last surprise", artista="Lyn", fecha_lanzamiento="2017-01-17"))
                    session.add(Cancion(id=3, titulo="Bajan", artista="Pescado Rabioso", fecha_lanzamiento="1973-05-07"))
                    session.add(Cancion(id=4, titulo="Fermín", artista="Almendra", fecha_lanzamiento="1969-11-30"))
                    session.add(Cancion(id=5, titulo="Bubbles", artista="Jenny01", fecha_lanzamiento="2006-04-01"))
                    session.commit()
                    print("[DB] Datos iniciales insertados")

            print("[DB] Base de datos lista")
            return

        except OperationalError as e:
            print(f"[DB] PostgreSQL no está listo: {e}. Reintentando en {delay} segundos...")
            time.sleep(delay)

    raise Exception("[DB] No se pudo conectar a PostgreSQL tras varios intentos")