# models/puntos_funcion.py — Datos y cálculos de Puntos de Función (FPA)
# Extraído de app.py — lógica pura, sin dependencias de Flask

# ═══════════════════════════════════════════
#   CONSTANTES DEL MODELO
# ═══════════════════════════════════════════

TIPOS_FP = [
    {"code": "EI",  "name": "Entradas externas",      "pesos": [3, 4,  6]},
    {"code": "EO",  "name": "Salidas externas",       "pesos": [4, 5,  7]},
    {"code": "EQ",  "name": "Consultas externas",     "pesos": [3, 4,  6]},
    {"code": "ILF", "name": "Archivos lógicos int.",  "pesos": [7, 10, 15]},
    {"code": "EIF", "name": "Archivos interfaz ext.", "pesos": [5, 7,  10]},
]

LOC_POR_PF = {
    "Java": 46, "C++": 53, "Python": 40,
    "Visual Basic": 32, "C": 80, "4GL": 20,
}

VAF_CARACTERISTICAS = [
    "Comunicaciones de datos", "Procesamiento distribuido",
    "Rendimiento", "Configuraciones muy utilizadas",
    "Frecuencia de transacciones", "Entrada de datos en línea",
    "Eficiencia del usuario final", "Actualización en línea",
    "Procesamiento complejo", "Reutilización",
    "Facilidad de instalación", "Facilidad de operación",
    "Múltiples sitios", "Facilidad de cambio",
]


# ═══════════════════════════════════════════
#   FUNCIÓN DE CÁLCULO
# ═══════════════════════════════════════════

def calcular_puntos_funcion(conteos, vaf_valores, loc_por_pf):
    """Convierte Puntos de Función a KLOC."""
    pfsa = 0
    for tipo, (simple, medio, complejo) in conteos.items():
        tipo_data = next(t for t in TIPOS_FP if t["code"] == tipo)
        pesos = tipo_data["pesos"]
        pfsa += simple * pesos[0] + medio * pesos[1] + complejo * pesos[2]
    suma_vaf = sum(vaf_valores)
    vaf = round(suma_vaf * 0.01 + 0.65, 4)
    pfa = round(pfsa * vaf)
    kloc = round(pfa * loc_por_pf / 1000, 3)
    return {"pfsa": pfsa, "vaf": vaf, "pfa": pfa, "kloc": kloc}
