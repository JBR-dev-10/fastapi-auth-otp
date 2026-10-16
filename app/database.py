from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Configuración del motor de SQLite. connect_args es necesario para SQLite en FastAPI (multihilo).
engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Dependencia de FastAPI para obtener una sesión de base de datos por solicitud,
    garantizando su cierre correcto al finalizar.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()