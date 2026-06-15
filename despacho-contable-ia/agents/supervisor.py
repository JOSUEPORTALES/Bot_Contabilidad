from sqlalchemy.orm import Session
from database import crud
from inference import MotorInferenciaContable

class AgenteSupervisor:
    def __init__(self):
        self.nombre = "Supervisor-AI"
        self.motor_inferencia = MotorInferenciaContable()

    def auditar_y_registrar_factura(self, db: Session, rfc_cliente: str, uuid: str, monto_total: float, iva_declarado: float, concepto: str) -> dict:
        """
        Recibe una factura, la audita con el motor de inferencia y, si todo
        es correcto, la guarda en la base de datos asociada a su cliente.
        """
        # Registrar el intento en la bitácora
        crud.registrar_accion_agente(db, agente=self.nombre, accion=f"Auditando factura UUID: {uuid} para RFC: {rfc_cliente}")

        # 1. Verificar si el cliente existe en nuestra base de datos
        cliente = crud.obtener_cliente_por_rfc(db, rfc_cliente)
        if not cliente:
            crud.registrar_accion_agente(db, agente=self.nombre, accion=f"Auditoría fallida: Cliente {rfc_cliente} no existe", resultado="Error")
            return {"status": "Error", "mensaje": "No se puede registrar la factura porque el cliente no está dado de alta."}

        # 2. Auditar la factura usando el Motor de Inferencia (Regla del IVA)
        auditoria = self.motor_inferencia.auditar_factura(monto_total, iva_declarado)

        # 3. Guardar la factura en la base de datos
        # Nota: Aunque la factura esté "Rechazada" por auditoría, la guardamos para tener registro de los errores del cliente
        nueva_factura = crud.crear_factura(
            db=db,
            uuid=uuid,
            monto_total=monto_total,
            iva=iva_declarado,
            concepto=concepto,
            cliente_id=cliente.id
        )

        # Actualizar la bitácora con el resultado de la auditoría
        resultado_final = "Éxito" if auditoria["resultado"] == "Aprobada" else "Advertencia"
        crud.registrar_accion_agente(
            db, 
            agente=self.nombre, 
            accion=f"Factura {uuid} procesada. Resultado: {auditoria['resultado']}", 
            resultado=resultado_final
        )

        return {
            "status": "Éxito",
            "auditoria_resultado": auditoria["resultado"],
            "detalles_auditoria": auditoria["detalles"],
            "factura_id": nueva_factura.id
        }