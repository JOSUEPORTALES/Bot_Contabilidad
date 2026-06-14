import os
from pathlib import Path
from pydantic_settings import BaseSettings

# Ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "Despacho Contable AI"
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./database/despacho.db"
    
    # Configuración de LLM (con un valor por defecto seguro)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "mock-key")
    LLM_MODEL: str = "gpt-4o"

    class Config:
        env_file = ".env"
        extra = "ignore"

# Instancia global para importar en todo el proyecto
settings = Settings()