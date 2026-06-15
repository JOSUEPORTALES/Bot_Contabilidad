from sqlalchemy.orm import Session
from database import crud
from inference import MotorInferenciaContable

class AgenteRecepcionista:
    def __init__(self):
        self.nombre = "Recepcionista-AI"
        self.motor_inferencia = MotorInferenciaContable()

    def registrar_nuevo_cliente(self, db: Session, rfc: str, nombre: str, correo: str, regimen: str) -> dict:
        """Recibe los datos de un cliente, los valida y los guarda en la base de datos."""
        # Registrar la acción del agente en la bitácora
        crud.registrar_accion_agente(db, agente=self.nombre, accion=f"Intento de registro de cliente con RFC: {rfc}")

        # Validar si el cliente ya existe
        cliente_existente = crud.obtener_cliente_por_rfc(db, rfc)
        if cliente_existente:
            crud.registrar_accion_agente(db, agente=self.nombre, accion=f"Registro fallido: RFC {rfc} duplicado", resultado="Error")
            return {"status": "Error", "mensaje": "El RFC ya se encuentra registrado en el sistema."}

        # Validar sintaxis básica de RFC mexicano (longitud)
        if len(rfc) not in [12, 13]:
            crud.registrar_accion_agente(db, agente=self.nombre, accion=f"Registro fallido: RFC {rfc} inválido", resultado="Error")
            return {"status": "Error", "mensaje": "El RFC introducido no tiene una longitud válida (debe ser de 12 o 13 caracteres)."}

        # Guardar en base de datos si pasa las validaciones
        nuevo_cliente = crud.crear_cliente(db, rfc=rfc, nombre=nombre, correo=correo, regimen_fiscal=regimen)
        
        # Evaluar de inmediato su situación con el motor de inferencia para darle la bienvenida
        analisis_inicial = self.motor_inferencia.evaluar_situacion_cliente(regimen, ingresos_acumulados=0.0)

        return {
            "status": "Éxito",
            "mensaje": f"Cliente '{nombre}' registrado correctamente.",
            "datos_cliente": {
                "id": nuevo_cliente.id,
                "rfc": nuevo_cliente.rfc,
                "regimen": nuevo_cliente.regimen_fiscal
            },
            "diagnostico_inicial": analisis_inicial
        }