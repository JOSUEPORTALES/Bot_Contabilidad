from . import rules

class MotorInferenciaContable:
    def __init__(self):
        self.reglas_regimen = rules.REGLAS_REGIMEN_FISCAL

    def evaluar_situacion_cliente(self, regimen: str, ingresos_acumulados: float) -> dict:
        """Ejecuta el análisis experto sobre la situación del régimen del cliente."""
        regimen_upper = regimen.upper()
        if regimen_upper not in self.reglas_regimen:
            return {
                "estado": "Desconocido",
                "diagnostico": f"El régimen '{regimen}' no está mapeado en las reglas del sistema experto."
            }

        info_regimen = self.reglas_regimen[regimen_upper]
        resultado = {
            "regimen": regimen_upper,
            "descripcion": info_regimen["descripcion"],
            "permite_deducir": info_regimen["permite_deducciones"],
            "consejo": info_regimen["mensaje_alerta"],
            "alerta_limite": "No aplica para este régimen"
        }

        # Aplicar regla específica si es RESICO
        if regimen_upper == "RESICO":
            analisis_limite = rules.validar_monto_resico(ingresos_acumulados)
            resultado["alerta_limite"] = analisis_limite["alerta"]
            resultado["apto_para_regimen"] = analisis_limite["valido"]
        else:
            resultado["apto_para_regimen"] = True

        return resultado

    def auditar_factura(self, monto_total: float, iva_declarado: float) -> dict:
        """Audita matemáticamente si el IVA de una factura fue calculado correctamente."""
        es_correcto = rules.verificar_iva_correcto(monto_total, iva_declarado)
        
        if es_correcto:
            return {
                "resultado": "Aprobada",
                "detalles": "El cálculo del IVA (16%) coincide perfectamente con los estándares de Ley."
            }
        else:
            return {
                "resultado": "Rechazada / Revisión",
                "detalles": "ALERTA: El IVA declarado no coincide con el 16% del monto total. Posible error de captura o tasa diferente."
            }