from sqlmodel import create_engine, SQLModel, Session
from models.cancion import Cancion

db_user: str = "quevedo"  
db_password: str =  "1234"
db_server: str = "localhost" 
db_port: int = 3306  
db_name: str = "cancionesdb"  

DATABASE_URL = f"mysql+pymysql://{db_user}:{db_password}@{db_server}:{db_port}/{db_name}"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(Cancion(id=1, titulo="Rivers in the desert", artista="Lyn", fecha_lanzamiento="2017-01-17"))
        session.add(Cancion(id=2, titulo="Last surprise", artista="Lyn", fecha_lanzamiento="2017-01-17"))
        session.add(Cancion(id=3, titulo="Bajan", artista="Pescado Rabioso", fecha_lanzamiento="1973-05-07"))
        session.add(Cancion(id=4, titulo="Fermín", artista="Almendra", fecha_lanzamiento="1969-11-30"))
        session.add(Cancion(id=5, titulo="Bubbles", artista="Jenny01", fecha_lanzamiento="2006-04-01"))
        session.commit()