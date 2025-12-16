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
        session.add(Cancion(id=1, titulo="The Mandalorian", fecha_estreno="2023-09-10"))
        session.add(Cancion(id=2, titulo="The Simpsons", fecha_estreno="2024-03-20"))
        session.add(Cancion(id=3, titulo="Friends", fecha_estreno="2019-02-22"))
        session.add(Cancion(id=4, titulo="House of dragon", fecha_estreno="2021-10-01"))
        session.add(Cancion(id=5, titulo="Lord of the rings", fecha_estreno="2023-09-10"))
        session.commit()
        #session.refresh_all()