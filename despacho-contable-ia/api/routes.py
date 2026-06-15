from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from database import obtener_db
from agents import AgenteRecepcionista, AgenteManager, AgenteSupervisor

router = APIRouter()

# Instanciar a nuestros agentes para que estén listos para jalar
recepcionista = AgenteRecepcionista()
manager = AgenteManager()
supervisor = AgenteSupervisor()

# --- MODELOS DE PETICIÓN (Esquemas de datos) ---
class ClienteCreate(BaseModel):
    rfc: str = Field(..., min_length=12, max_length=13)
    nombre: str
    correo: str
    regimen: str

class DiagnosticoRequest(BaseModel):
    rfc: str
    ingresos_acumulados: float

class FacturaRequest(BaseModel):
    rfc_cliente: str
    uuid: str
    monto_total: float
    iva_declarado: float
    concepto: str


# --- RUTAS DE LA API ---

@router.post("/clientes", summary="Ruta del Agente Recepcionista")
def alta_cliente(cliente: ClienteCreate, db: Session = Depends(obtener_db)):
    resultado = recepcionista.registrar_nuevo_cliente(
        db, rfc=cliente.rfc, nombre=cliente.nombre, correo=cliente.correo, regimen=cliente.regimen
    )
    if resultado["status"] == "Error":
        raise HTTPException(status_code=400, detail=resultado["mensaje"])
    return resultado

@router.post("/diagnostico", summary="Ruta del Agente Manager")
def diagnostico_fiscal(data: DiagnosticoRequest, db: Session = Depends(obtener_db)):
    resultado = manager.generar_diagnostico_fiscal(
        db, rfc=data.rfc, ingresos_acumulados=data.ingresos_acumulados
    )
    if resultado["status"] == "Error":
        raise HTTPException(status_code=404, detail=resultado["mensaje"])
    return resultado

@router.post("/facturas/auditar", summary="Ruta del Agente Supervisor")
def auditar_factura(factura: FacturaRequest, db: Session = Depends(obtener_db)):
    resultado = supervisor.auditar_y_registrar_factura(
        db, 
        rfc_cliente=factura.rfc_cliente, 
        uuid=factura.uuid, 
        monto_total=factura.monto_total, 
        iva_declarado=factura.iva_declarado, 
        concepto=factura.concepto
    )
    if resultado["status"] == "Error":
        raise HTTPException(status_code=400, detail=resultado["mensaje"])
    return resultado