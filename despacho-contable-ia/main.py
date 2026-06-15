from fastapi import FastAPI
from api.routes import router as api_router
from database import inicializar_base_de_datos
from config.settings import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    debug=settings.DEBUG
)

# Inicializar la base de datos (crear despacho.db y sus tablas si no existen)
@app.on_event("startup")
def startup_event():
    inicializar_base_de_datos()

# Incluir las rutas de nuestros agentes
app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return {
        "status": "Online",
        "proyecto": settings.PROJECT_NAME,
        "mensaje": "El Backend del Despacho Contable IA está corriendo correctamente."
    }