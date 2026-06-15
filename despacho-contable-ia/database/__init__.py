from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import settings
from .models import Base

# 1. Configurar el motor de la base de datos (Engine)
# 'connect_args' solo es necesario para SQLite (permite hilos múltiples)
engine = create_engine(
    settings.DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# 2. Configurar la fábrica de sesiones (SessionLocal)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def inicializar_base_de_datos():
    """Crea todas las tablas en la base de datos si no existen."""
    Base.metadata.create_all(bind=engine)

def obtener_db():
    """Función auxiliar (Dependency) para abrir y cerrar la sesión de BD de forma segura."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()