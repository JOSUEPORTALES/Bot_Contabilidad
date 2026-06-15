from sqlalchemy.orm import Session
from . import models
from datetime import datetime

# ==========================================
# OPERACIONES PARA CLIENTES
# ==========================================

def obtener_cliente_por_rfc(db: Session, rfc: str):
    """Busca un cliente en la base de datos usando su RFC."""
    return db.query(models.Cliente).filter(models.Cliente.rfc == rfc.upper()).first()

def obtener_clientes(db: Session, skip: int = 0, limit: int = 100):
    """Trae una lista de los clientes registrados (con límite para no saturar)."""
    return db.query(models.Cliente).offset(skip).limit(limit).all()

def crear_cliente(db: Session, rfc: str, nombre: str, correo: str, regimen_fiscal: str = None):
    """Crea un nuevo cliente en el sistema."""
    nuevo_cliente = models.Cliente(
        rfc=rfc.upper(),
        nombre=nombre,
        correo=correo,
        regimen_fiscal=regimen_fiscal
    )
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    return nuevo_cliente

# ==========================================
# OPERACIONES PARA FACTURAS
# ==========================================

def crear_factura(db: Session, uuid: str, monto_total: float, iva: float, concepto: str, cliente_id: int):
    """Asocia y guarda una nueva factura a un cliente específico."""
    nueva_factura = models.Factura(
        uuid=uuid,
        monto_total=monto_total,
        iva=iva,
        concepto=concepto,
        fecha_emision=datetime.utcnow(),
        cliente_id=cliente_id
    )
    db.add(nueva_factura)
    db.commit()
    db.refresh(nueva_factura)
    return nueva_factura

def obtener_facturas_cliente(db: Session, cliente_id: int):
    """Obtiene todas las facturas que le pertenecen a un cliente."""
    return db.query(models.Factura).filter(models.Factura.cliente_id == cliente_id).all()

# ==========================================
# OPERACIONES PARA LA BITÁCORA DE AGENTES
# ==========================================

def registrar_accion_agente(db: Session, agente: str, accion: str, resultado: str = "Éxito"):
    """Registra en la base de datos qué hizo un agente y si falló o no."""
    nueva_entrada = models.BitacoraTarea(
        agente_responsable=agente,
        accion_realizada=accion,
        resultado=resultado
    )
    db.add(nueva_entrada)
    db.commit()
    db.refresh(nueva_entrada)
    return nueva_entrada