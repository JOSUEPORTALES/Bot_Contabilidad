from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

# Esta es la clase base de la cual heredarán todos nuestros modelos
Base = declarative_base()

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    rfc = Column(String(13), unique=True, index=True, nullable=False)
    nombre = Column(String(150), nullable=False)
    regimen_fiscal = Column(String(100), nullable=True)
    correo = Column(String(100), unique=True, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    # Relación con las facturas (Un cliente puede tener muchas facturas)
    facturas = relationship("Factura", back_populates="cliente", cascade="all, delete-orphan")


class Factura(Base):
    __tablename__ = "facturas"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, index=True, nullable=False) # ID único de hacienda
    monto_total = Column(Float, nullable=False)
    iva = Column(Float, default=0.0)
    fecha_emision = Column(DateTime, nullable=False)
    concepto = Column(Text, nullable=True)
    
    # Llave foránea para conectar con el cliente
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    
    # Relación inversa
    cliente = relationship("Cliente", back_populates="facturas")


class BitacoraTarea(Base):
    __tablename__ = "bitacora_tareas"

    id = Column(Integer, primary_key=True, index=True)
    agente_responsable = Column(String(50), nullable=False) # Recepcionista, Supervisor, etc.
    accion_realizada = Column(Text, nullable=False)
    resultado = Column(String(50), default="Éxito") # Éxito, Error, Pendiente
    fecha_registro = Column(DateTime, default=datetime.utcnow)