from sqlalchemy.orm import Session
from database import crud
from inference import MotorInferenciaContable

class AgenteManager:
    def __init__(self):
        self.nombre = "Manager-AI"
        self.motor_inferencia = MotorInferenciaContable()

    def generar_diagnostico_fiscal(self, db: Session, rfc: str, ingresos_acumulados: float) -> dict:
        """
        Analiza la situación actual de un cliente usando el motor de inferencia
        y sus datos de facturación acumulados.
        """
        # Registrar la acción en la bitácora
        crud.registrar_accion_agente(db, agente=self.nombre, accion=f"Generando diagnóstico fiscal para RFC: {rfc}")

        # Buscar al cliente en la base de datos
        cliente = crud.obtener_cliente_por_rfc(db, rfc)
        if not cliente:
            crud.registrar_accion_agente(db, agente=self.nombre, accion=f"Diagnóstico fallido: RFC {rfc} no existe", resultado="Error")
            return {"status": "Error", "mensaje": "El cliente no está registrado en el sistema."}

        # Ejecutar el motor de inferencia experto
        analisis_experto = self.motor_inferencia.evaluar_situacion_cliente(
            regimen=cliente.regimen_fiscal, 
            ingresos_acumulados=ingresos_acumulados
        )

        # Generar una recomendación ejecutiva basada en el resultado del motor
        recomendacion = "Mantener el monitoreo mensual de declaraciones."
        if not analisis_experto.get("apto_para_regimen", True):
            recomendacion = "URGENTE: Agendar cita para cambio de régimen fiscal en el portal del SAT."
        elif "ADVERTENCIA" in analisis_experto.get("alerta_limite", ""):
            recomendacion = "PRECAUCIÓN: Controlar la emisión de facturas este mes o planificar transición."

        return {
            "status": "Éxito",
            "reporte": {
                "cliente": cliente.nombre,
                "rfc": cliente.rfc,
                "regimen_actual": cliente.regimen_fiscal,
                "ingresos_evaluados": ingresos_acumulados,
                "resultado_sistema_experto": analisis_experto,
                "recomendacion_manager": recomendacion
            }
        }