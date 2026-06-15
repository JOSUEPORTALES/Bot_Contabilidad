# Base de Conocimiento - Reglas Expertas de Contabilidad

REGLAS_REGIMEN_FISCAL = {
    "RESICO": {
        "descripcion": "Régimen Simplificado de Confianza",
        "limite_ingresos": 3500000.0,
        "tasa_isr_max": 2.5,
        "permite_deducciones": False,
        "mensaje_alerta": "Recuerda que en RESICO el ISR se calcula sobre ingresos brutos, no aplican deducciones de gastos para este impuesto."
    },
    "PFAE": {
        "descripcion": "Personas Físicas con Actividades Empresariales y Profesionales",
        "limite_ingresos": None, # Sin límite
        "tasa_isr_max": 35.0,
        "permite_deducciones": True,
        "mensaje_alerta": "En PFAE es vital facturar todos los gastos estrictamente indispensables para deducir ISR."
    }
}

def validar_monto_resico(monto_anual_acumulado: float) -> dict:
    """Verifica si un contribuyente RESICO está en riesgo de salir del régimen."""
    limite = REGLAS_REGIMEN_FISCAL["RESICO"]["limite_ingresos"]
    if monto_anual_acumulado > limite:
        return {
            "valido": False,
            "alerta": "CRÍTICO: El cliente ha excedido el límite de 3.5 millones de RESICO. Debe migrar a PFAE."
        }
    elif monto_anual_acumulado > (limite * 0.85):
        return {
            "valido": True,
            "alerta": "ADVERTENCIA: El cliente ha superado el 85% del límite permitido para RESICO. Monitorear ingresos."
        }
    return {"valido": True, "alerta": "Todo en orden. Los ingresos acumulados están dentro del rango seguro."}

def verificar_iva_correcto(monto_total: float, iva_declarado: float) -> bool:
    """Valida mediante una regla matemática si el IVA corresponde al 16% estándar."""
    # Calculamos el IVA esperado (monto_total incluye IVA, entonces: subtotal = monto / 1.16; iva = subtotal * 0.16)
    subtotal_esperado = monto_total / 1.16
    iva_esperado = subtotal_esperado * 0.16
    
    # Tolerancia de 1 peso por cuestiones de redondeo decimal
    return abs(iva_esperado - iva_declarado) <= 1.0