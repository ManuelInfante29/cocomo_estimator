# utils/pdf.py - Generacion de archivos PDF para reportes COCOMO

from fpdf import FPDF
from io import BytesIO
from datetime import datetime


class ReportePDF(FPDF):
    """Clase base para reportes PDF con estilo consistente."""

    def __init__(self, titulo):
        super().__init__()
        self.titulo = titulo
        # Auto page break: cuando el contenido excede la pagina, crea una nueva automaticamente
        self.set_auto_page_break(auto=True, margin=18)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(31, 78, 121)
        self.cell(0, 6, self.titulo, align="L")
        self.set_font("Helvetica", "", 7)
        self.set_text_color(128, 128, 128)
        self.cell(0, 6, f"Pag. {self.page_no()}", align="R", new_x="LMARGIN", new_y="NEXT")
        self.line(self.l_margin, self.get_y() + 1, self.w - self.r_margin, self.get_y() + 1)
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(160, 160, 160)
        self.cell(0, 10, f"Generado con COCOMO Estimator - {datetime.now().strftime('%d/%m/%Y %H:%M')}", align="C")

    def titulo_principal(self, texto):
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(31, 78, 121)
        self.cell(0, 10, texto, new_x="LMARGIN", new_y="NEXT", align="L")
        self.ln(2)

    def subtitulo(self, texto):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(90, 95, 112)
        self.cell(0, 5, texto, new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

    def seccion(self, texto):
        # Evitar encabezado huerfano: si quedan menos de 30mm, saltar a nueva pagina
        if self.get_y() > self.h - 40:
            self.add_page()
        self.set_fill_color(31, 78, 121)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 11)
        self.cell(0, 8, f"  {texto}", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

    def fila_dato(self, label, valor, unidad="", destacar=False):
        # Si no hay espacio para esta fila, saltar pagina
        if self.get_y() > self.h - 20:
            self.add_page()
        self.set_font("Helvetica", "B" if destacar else "", 10)
        self.set_text_color(31, 78, 121)
        self.cell(70, 7, label)
        self.set_font("Courier", "B" if destacar else "", 10)
        self.set_text_color(20, 20, 30)
        self.cell(50, 7, str(valor), align="R")
        self.set_font("Helvetica", "", 9)
        self.set_text_color(128, 128, 128)
        self.cell(0, 7, f"  {unidad}", new_x="LMARGIN", new_y="NEXT")

    def fila_tabla(self, cols, anchos=None, cabecera=False):
        if anchos is None:
            anchos = [(self.w - 2 * self.l_margin) // len(cols)] * len(cols)
        # Si no hay espacio para esta fila + 2 filas mas, saltar pagina
        if self.get_y() > self.h - 30:
            self.add_page()
        if cabecera:
            self.set_fill_color(31, 78, 121)
            self.set_text_color(255, 255, 255)
            self.set_font("Helvetica", "B", 9)
        else:
            self.set_fill_color(245, 248, 252)
            self.set_text_color(30, 30, 40)
            self.set_font("Helvetica", "", 9)
        for c, a in zip(cols, anchos):
            self.cell(a, 7, str(c), fill=True, align="C" if cabecera else "L")
        self.ln()

    def tabla_con_encabezado(self, encabezados, filas, anchos=None):
        """Escribe una tabla con encabezados que se repiten en cada nueva pagina."""
        if anchos is None:
            anchos = [(self.w - 2 * self.l_margin) // len(encabezados)] * len(encabezados)
        self.fila_tabla(encabezados, anchos, cabecera=True)
        pagina_anterior = self.page_no()
        for fila in filas:
            if self.page_no() != pagina_anterior:
                self.fila_tabla(encabezados, anchos, cabecera=True)
                pagina_anterior = self.page_no()
            self.fila_tabla(fila, anchos, cabecera=False)

    def linea(self):
        self.set_draw_color(200, 200, 210)
        y = self.get_y()
        self.line(self.l_margin, y, self.w - self.r_margin, y)
        self.ln(3)


def _guardar_bytesio(pdf):
    buf = BytesIO()
    pdf.output(buf)
    buf.seek(0)
    return buf


# ═══════════════════════════════════════════
#   BUILDERS DE PDF POR MODELO
# ═══════════════════════════════════════════

def build_c81basico_pdf(data):
    body = data["body"]
    r = data["resultado"]
    p = r["params"]
    etapas = data["etapas"]

    pdf = ReportePDF("COCOMO 81 - Modelo Basico")
    pdf.add_page()
    pdf.titulo_principal("COCOMO 81 - Modelo Basico")
    pdf.subtitulo(f"Modo: {body['modo'].capitalize()}  |  EAF = 1.0 (fijo)")

    pdf.seccion("Parametros de Entrada")
    pdf.fila_dato("Tamano (KLOC)", body["kloc"])
    pdf.fila_dato("Modo del proyecto", body["modo"].capitalize())
    pdf.fila_dato("Costo hombre-mes", f"${body['costo_hm']:,.2f}")
    pdf.fila_dato("Constantes", f"a={p['a']}  b={p['b']}  c={p['c']}  d={p['d']}")
    pdf.ln(4)

    pdf.seccion("Resultados")
    pdf.fila_dato("Esfuerzo", f"{r['esfuerzo']:.2f}", "persona-mes (PM)", True)
    pdf.fila_dato("Tiempo de desarrollo", f"{r['tiempo']:.2f}", "meses")
    pdf.fila_dato("Personal requerido", f"{r['personal']:.2f}", "personas")
    pdf.fila_dato("Costo total", f"${r['costo']:,.2f}", "USD", True)
    pdf.ln(6)

    pdf.seccion("Distribucion por Etapas")
    ancho = ((pdf.w - 2 * pdf.l_margin) / 4) - 1
    pdf.fila_tabla(["Etapa", "Esfuerzo (PM)", "Tiempo (mes)", "%"], [ancho*1.2, ancho, ancho, ancho*0.6], cabecera=True)
    for e in etapas:
        pdf.fila_tabla([e["nombre"], str(e["esfuerzo"]), str(e["tiempo"]), f"{e['pct']}%"],
                       [ancho*1.2, ancho, ancho, ancho*0.6])

    return _guardar_bytesio(pdf), f"COCOMO81_Basico_{datetime.now().strftime('%Y%m%d')}.pdf"


def build_c81_pdf(data):
    body = data["body"]
    r = data["resultado"]
    p = r["params"]
    etapas = data["etapas"]
    eaf = data["eaf"]
    drivers = data.get("valoresDrivers", {})

    pdf = ReportePDF("COCOMO 81 - Modelo Intermedio")
    pdf.add_page()
    pdf.titulo_principal("COCOMO 81 - Modelo Intermedio")
    pdf.subtitulo(f"Modo: {body['modo'].capitalize()}  |  EAF = {eaf:.4f}")

    pdf.seccion("Parametros de Entrada")
    pdf.fila_dato("Tamano (KLOC)", body["kloc"])
    pdf.fila_dato("Modo del proyecto", body["modo"].capitalize())
    pdf.fila_dato("Costo hombre-mes", f"${body['costo_hm']:,.2f}")
    pdf.fila_dato("Constantes", f"a={p['a']}  b={p['b']}  c={p['c']}  d={p['d']}")
    pdf.ln(4)

    pdf.seccion("Conductores de Coste")
    ancho = ((pdf.w - 2 * pdf.l_margin) / 4) - 1
    pdf.fila_tabla(["Conductor", "Codigo", "Valor", ""], [ancho*1.5, ancho, ancho, ancho*0.5], cabecera=True)
    for code, info in drivers.items():
        pdf.fila_tabla([info.get("nombre", code), code, str(info["valor"]), ""], [ancho*1.5, ancho, ancho, ancho*0.5])
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(31, 78, 121)
    pdf.cell(0, 8, f"EAF TOTAL: {eaf:.4f}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    pdf.seccion("Resultados")
    pdf.fila_dato("Esfuerzo", f"{r['esfuerzo']:.2f}", "persona-mes (PM)", True)
    pdf.fila_dato("Tiempo de desarrollo", f"{r['tiempo']:.2f}", "meses")
    pdf.fila_dato("Personal requerido", f"{r['personal']:.2f}", "personas")
    pdf.fila_dato("Costo total", f"${r['costo']:,.2f}", "USD", True)
    pdf.ln(6)

    pdf.seccion("Distribucion por Etapas")
    ancho = ((pdf.w - 2 * pdf.l_margin) / 4) - 1
    pdf.fila_tabla(["Etapa", "Esfuerzo (PM)", "Tiempo (mes)", "%"], [ancho*1.2, ancho, ancho, ancho*0.6], cabecera=True)
    for e in etapas:
        pdf.fila_tabla([e["nombre"], str(e["esfuerzo"]), str(e["tiempo"]), f"{e['pct']}%"],
                       [ancho*1.2, ancho, ancho, ancho*0.6])

    return _guardar_bytesio(pdf), f"COCOMO81_Intermedio_{datetime.now().strftime('%Y%m%d')}.pdf"


def build_cocomo2_pdf(data):
    body = data["body"]
    r = data["resultado"]
    etapas = data["etapas"]
    B_val = data["B"]
    EM_val = data["EM"]
    sumSF = data["sumSF"]

    pdf = ReportePDF("COCOMO II - Post-Arquitectura")
    pdf.add_page()
    pdf.titulo_principal("COCOMO II - Post-Arquitectura")
    pdf.subtitulo(f"B = {B_val:.4f}  |  EM = {EM_val:.4f}")

    pdf.seccion("Parametros de Entrada")
    pdf.fila_dato("Tamano (KLOC)", body["kloc"])
    pdf.fila_dato("Costo hombre-mes", f"${body['costo_hm']:,.2f}")
    pdf.fila_dato("Suma Factores de Escala", f"{sumSF:.2f}")
    pdf.fila_dato("Exponente B", f"{B_val:.4f}")
    pdf.fila_dato("Producto EM", f"{EM_val:.4f}")
    pdf.ln(2)

    # Factores de Escala (tabla corta, no necesita repeticion de encabezado)
    pdf.seccion("Factores de Escala (SF)")
    sf_names = ["PREC - Precedencia", "FLEX - Flexibilidad", "RESL - Arquitectura/Resolucion", "TEAM - Cohesion equipo", "PMAT - Madurez proceso"]
    sf_anch = ((pdf.w - 2 * pdf.l_margin) / 2) - 1
    sf_filas = [[name, str(val)] for name, val in zip(sf_names, body["sf_valores"])]
    pdf.tabla_con_encabezado(["Factor", "Valor"], sf_filas, [sf_anch*1.3, sf_anch*0.7])
    pdf.ln(2)

    # Multiplicadores de Esfuerzo (17 filas -> puede ocupar 2+ paginas)
    pdf.seccion("Multiplicadores de Esfuerzo (EM)")
    em_names = ["RELY - Confiabilidad", "DATA - Tamano BD", "CPLX - Complejidad", "RUSE - Reutilizacion",
                "DOCU - Documentacion", "TIME - Restriccion CPU", "STOR - Restriccion almacenamiento",
                "PVOL - Volatilidad plataforma", "ACAP - Capacidad analistas", "PCAP - Capacidad programadores",
                "PCON - Continuidad personal", "APEX - Experiencia aplicacion", "PLEX - Experiencia plataforma",
                "LTEX - Experiencia lenguaje", "TOOL - Uso herramientas", "SITE - Multisitio", "SCED - Compresion calendario"]
    em_anch = ((pdf.w - 2 * pdf.l_margin) / 2) - 1
    em_filas = [[name, str(val)] for name, val in zip(em_names, body["em_valores"])]
    pdf.tabla_con_encabezado(["Multiplicador", "Valor"], em_filas, [em_anch*1.3, em_anch*0.7])
    pdf.ln(2)

    pdf.seccion("Resultados")
    pdf.fila_dato("Esfuerzo", f"{r['esfuerzo']:.2f}", "persona-mes (PM)", True)
    pdf.fila_dato("Tiempo de desarrollo (TDEV)", f"{r['tiempo']:.2f}", "meses")
    pdf.fila_dato("Personal requerido", f"{r['personal']:.2f}", "personas")
    pdf.fila_dato("Costo total", f"${r['costo']:,.2f}", "USD", True)
    pdf.ln(2)

    pdf.seccion("Distribucion por Etapas")
    et_anch = ((pdf.w - 2 * pdf.l_margin) / 4) - 1
    et_filas = [[e["nombre"], str(e["esfuerzo"]), str(e["tiempo"]), f"{e['pct']}%"] for e in etapas]
    pdf.tabla_con_encabezado(["Etapa", "Esfuerzo (PM)", "Tiempo (mes)", "%"],
                             et_filas, [et_anch*1.2, et_anch, et_anch, et_anch*0.6])

    return _guardar_bytesio(pdf), f"COCOMO_II_{datetime.now().strftime('%Y%m%d')}.pdf"


def build_fp_pdf(data):
    from models.puntos_funcion import VAF_CARACTERISTICAS

    body = data["body"]
    r = data["resultado"]

    pdf = ReportePDF("Puntos de Funcion (FPA)")
    pdf.add_page()
    pdf.titulo_principal("Puntos de Funcion (FPA)")

    pdf.seccion("Conteo de Componentes")
    ancho = ((pdf.w - 2 * pdf.l_margin) / 4) - 1
    pdf.fila_tabla(["Componente", "Simple", "Medio", "Complejo"], [ancho*1.3, ancho*0.9, ancho*0.9, ancho*0.9], cabecera=True)
    fp_types = ["EI - Entradas externas", "EO - Salidas externas", "EQ - Consultas externas",
                "ILF - Archivos logicos int.", "EIF - Archivos interfaz ext."]
    for name, (s, m, c) in zip(fp_types, body["conteos"].values()):
        pdf.fila_tabla([name, str(s), str(m), str(c)], [ancho*1.3, ancho*0.9, ancho*0.9, ancho*0.9])
    pdf.ln(4)

    pdf.seccion("Factor de Ajuste (VAF)")
    ancho2 = ((pdf.w - 2 * pdf.l_margin) / 2) - 1
    pdf.fila_tabla(["Caracteristica", "Valor"], [ancho2*1.4, ancho2*0.6], cabecera=True)
    for i, val in enumerate(body["vaf_valores"]):
        pdf.fila_tabla([VAF_CARACTERISTICAS[i], str(val)], [ancho2*1.4, ancho2*0.6])
    pdf.ln(6)

    pdf.seccion("Resultados")
    pdf.fila_dato("PF Sin Ajustar (PFSA)", str(r["pfsa"]), "puntos funcion", True)
    pdf.fila_dato("Factor de Ajuste (VAF)", str(r["vaf"]))
    pdf.fila_dato("PF Ajustados (PFA)", str(r["pfa"]), "puntos funcion", True)
    pdf.fila_dato("KLOC estimadas", str(r["kloc"]), "miles de lineas", True)

    return _guardar_bytesio(pdf), f"Puntos_Funcion_{datetime.now().strftime('%Y%m%d')}.pdf"
