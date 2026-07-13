# models/cocomo2.py — Datos y cálculos COCOMO II Post-Arquitectura
# Extraído de app.py — lógica pura, sin dependencias de Flask

# ═══════════════════════════════════════════
#   CONSTANTES DEL MODELO
# ═══════════════════════════════════════════

FACTORES_ESCALA = [
    {"code": "PREC", "name": "Precedencia",             "vals": [6.20, 4.96, 3.72, 2.48, 1.24, 0.00]},
    {"code": "FLEX", "name": "Flexibilidad desarrollo", "vals": [5.07, 4.05, 3.04, 2.03, 1.01, 0.00]},
    {"code": "RESL", "name": "Arquitectura/resolución", "vals": [7.07, 5.65, 4.24, 2.83, 1.41, 0.00]},
    {"code": "TEAM", "name": "Cohesión del equipo",     "vals": [5.48, 4.38, 3.29, 2.19, 1.10, 0.00]},
    {"code": "PMAT", "name": "Madurez del proceso",     "vals": [7.80, 6.24, 4.68, 3.12, 1.56, 0.00]},
]

MULTIPLICADORES_EM = [
    {"code": "RELY", "name": "Confiabilidad requerida",    "vals": [0.82, 0.92, 1.00, 1.10, 1.26]},
    {"code": "DATA", "name": "Tamaño base de datos",       "vals": [None, 0.90, 1.00, 1.14, 1.28]},
    {"code": "CPLX", "name": "Complejidad",                "vals": [0.73, 0.87, 1.00, 1.17, 1.34, 1.74]},
    {"code": "RUSE", "name": "Reutilización requerida",    "vals": [None, 0.95, 1.00, 1.07, 1.15, 1.24]},
    {"code": "DOCU", "name": "Documentación ciclo vida",   "vals": [0.81, 0.91, 1.00, 1.11, 1.23]},
    {"code": "TIME", "name": "Restricción tiempo CPU",     "vals": [None, None, 1.00, 1.11, 1.29, 1.63]},
    {"code": "STOR", "name": "Restricción almacenamiento", "vals": [None, None, 1.00, 1.05, 1.17, 1.46]},
    {"code": "PVOL", "name": "Volatilidad plataforma",     "vals": [None, 0.87, 1.00, 1.15, 1.30]},
    {"code": "ACAP", "name": "Capacidad analistas",        "vals": [1.42, 1.19, 1.00, 0.85, 0.71]},
    {"code": "PCAP", "name": "Capacidad programadores",    "vals": [1.34, 1.15, 1.00, 0.88, 0.76]},
    {"code": "PCON", "name": "Continuidad personal",       "vals": [1.29, 1.12, 1.00, 0.90, 0.81]},
    {"code": "APEX", "name": "Experiencia aplicación",     "vals": [1.22, 1.10, 1.00, 0.88, 0.81]},
    {"code": "PLEX", "name": "Experiencia plataforma",     "vals": [1.19, 1.09, 1.00, 0.91, 0.85]},
    {"code": "LTEX", "name": "Experiencia lenguaje/herr.", "vals": [1.20, 1.09, 1.00, 0.91, 0.84]},
    {"code": "TOOL", "name": "Uso de herramientas",        "vals": [1.17, 1.09, 1.00, 0.90, 0.78]},
    {"code": "SITE", "name": "Desarrollo multisitio",      "vals": [1.22, 1.09, 1.00, 0.93, 0.86, 0.80]},
    {"code": "SCED", "name": "Compresión calendario",      "vals": [1.43, 1.14, 1.00, 1.00, 1.00]},
]


# ═══════════════════════════════════════════
#   FUNCIÓN DE CÁLCULO
# ═══════════════════════════════════════════

def calcular_cocomo2(kloc, sf_valores, em_valores, costo_hm):
    """Calcula esfuerzo con COCOMO II Post-Arquitectura."""
    A = 2.94
    suma_sf = sum(sf_valores)
    B = 0.91 + 0.01 * suma_sf
    EM = 1.0
    for v in em_valores:
        EM *= v
    esfuerzo = A * (kloc ** B) * EM
    exp_t    = 0.28 + 0.002 * suma_sf
    tiempo   = 3.67 * (esfuerzo ** exp_t)
    personal = esfuerzo / tiempo
    costo    = esfuerzo * costo_hm
    return {
        "esfuerzo": round(esfuerzo, 2),
        "tiempo":   round(tiempo, 2),
        "personal": round(personal, 2),
        "costo":    round(costo, 2),
        "B":        round(B, 4),
        "EM":       round(EM, 4),
        "suma_sf":  round(suma_sf, 2),
    }
