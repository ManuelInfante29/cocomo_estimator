# models/cocomo81.py — Datos y cálculos COCOMO 81 (Básico e Intermedio)
# Extraído de app.py — lógica pura, sin dependencias de Flask

# ═══════════════════════════════════════════
#   CONSTANTES DEL MODELO
# ═══════════════════════════════════════════

MODOS_C81 = {
    "organico":     {"a": 3.2,  "b": 1.05, "c": 2.5, "d": 0.38},
    "semiacoplado": {"a": 3.0,  "b": 1.12, "c": 2.5, "d": 0.35},
    "empotrado":    {"a": 2.8,  "b": 1.20, "c": 2.5, "d": 0.32},
}

DISTRIBUCION_ETAPAS = {
    "organico": {
        "Requisitos":   (0.08, 0.36),
        "Diseño":       (0.18, 0.36),
        "Codificación": (0.25, 0.18),
        "Pruebas":      (0.26, 0.28),
    },
    "semiacoplado": {
        "Requisitos":   (0.07, 0.33),
        "Diseño":       (0.19, 0.33),
        "Codificación": (0.26, 0.20),
        "Pruebas":      (0.29, 0.30),
    },
    "empotrado": {
        "Requisitos":   (0.06, 0.30),
        "Diseño":       (0.21, 0.34),
        "Codificación": (0.28, 0.20),
        "Pruebas":      (0.30, 0.30),
    },
}

# 15 conductores de coste COCOMO 81
CONDUCTORES_C81 = [
    {"code": "RELY", "name": "Confiabilidad requerida",     "vals": [0.75, 0.88, 1.00, 1.15, 1.40]},
    {"code": "DATA", "name": "Tamaño base de datos",        "vals": [None, 0.94, 1.00, 1.08, 1.16]},
    {"code": "CPLX", "name": "Complejidad del producto",    "vals": [0.70, 0.85, 1.00, 1.15, 1.30, 1.65]},
    {"code": "TIME", "name": "Restricción tiempo CPU",      "vals": [None, None, 1.00, 1.11, 1.30, 1.66]},
    {"code": "STOR", "name": "Restricción almacenamiento",  "vals": [None, None, 1.00, 1.06, 1.21, 1.56]},
    {"code": "VIRT", "name": "Volatilidad máquina virtual", "vals": [None, 0.87, 1.00, 1.15, 1.30]},
    {"code": "TURN", "name": "Tiempo de respuesta",         "vals": [None, 0.87, 1.00, 1.07, 1.15]},
    {"code": "ACAP", "name": "Capacidad analistas",         "vals": [1.46, 1.19, 1.00, 0.86, 0.71]},
    {"code": "AEXP", "name": "Experiencia en aplicación",   "vals": [1.29, 1.13, 1.00, 0.91, 0.82]},
    {"code": "PCAP", "name": "Capacidad programadores",     "vals": [1.42, 1.17, 1.00, 0.86, 0.70]},
    {"code": "VEXP", "name": "Experiencia máq. virtual",    "vals": [1.21, 1.10, 1.00, 0.90]},
    {"code": "LEXP", "name": "Experiencia en lenguaje",     "vals": [1.14, 1.07, 1.00, 0.95]},
    {"code": "MODP", "name": "Prácticas modernas",          "vals": [1.24, 1.10, 1.00, 0.91, 0.82]},
    {"code": "TOOL", "name": "Uso de herramientas SW",      "vals": [1.24, 1.10, 1.00, 0.91, 0.83]},
    {"code": "SCED", "name": "Restricción de calendario",   "vals": [1.23, 1.08, 1.00, 1.04, 1.10]},
]


# ═══════════════════════════════════════════
#   FUNCIONES DE CÁLCULO
# ═══════════════════════════════════════════

def calcular_cocomo81_basico(kloc, modo, costo_hm):
    """Calcula esfuerzo, tiempo, personal y costo con COCOMO 81 Básico (EAF = 1)."""
    p = MODOS_C81[modo]
    esfuerzo = p["a"] * (kloc ** p["b"])   # Sin EAF — siempre vale 1.0
    tiempo   = p["c"] * (esfuerzo ** p["d"])
    personal = esfuerzo / tiempo
    costo    = esfuerzo * costo_hm
    return {
        "esfuerzo": round(esfuerzo, 2),
        "tiempo":   round(tiempo, 2),
        "personal": round(personal, 2),
        "costo":    round(costo, 2),
        "params":   p,
    }


def calcular_cocomo81(kloc, modo, eaf, costo_hm):
    """Calcula esfuerzo, tiempo, personal y costo con COCOMO 81 Intermedio."""
    p = MODOS_C81[modo]
    esfuerzo = p["a"] * (kloc ** p["b"]) * eaf
    tiempo   = p["c"] * (esfuerzo ** p["d"])
    personal = esfuerzo / tiempo
    costo    = esfuerzo * costo_hm
    return {
        "esfuerzo": round(esfuerzo, 2),
        "tiempo":   round(tiempo, 2),
        "personal": round(personal, 2),
        "costo":    round(costo, 2),
        "params":   p,
        "eaf":      round(eaf, 4),
    }


def distribuir_etapas_c81(esfuerzo, tiempo, modo):
    """Distribuye esfuerzo y tiempo entre las 4 etapas del proyecto."""
    dist = DISTRIBUCION_ETAPAS[modo]
    etapas = []
    total_ef = sum(pe for pe, _ in dist.values())
    for nombre, (pe, pt) in dist.items():
        etapas.append({
            "nombre":    nombre,
            "esfuerzo":  round(esfuerzo * pe, 2),
            "tiempo":    round(tiempo * pt, 2),
            "pct":       round(pe / total_ef * 100),
        })
    return etapas
