# app.py — Capa delgada de rutas Flask
# Toda la lógica de negocio está en models/ y utils/

from flask import Flask, render_template, request, jsonify, send_file

from models.cocomo81 import (
    CONDUCTORES_C81,
    calcular_cocomo81_basico,
    calcular_cocomo81,
    distribuir_etapas_c81,
)
from models.cocomo2 import FACTORES_ESCALA, MULTIPLICADORES_EM, calcular_cocomo2
from models.puntos_funcion import TIPOS_FP, LOC_POR_PF, VAF_CARACTERISTICAS, calcular_puntos_funcion
from utils.excel import build_c81basico, build_c81, build_cocomo2, build_fp
from utils.pdf import build_c81basico_pdf, build_c81_pdf, build_cocomo2_pdf, build_fp_pdf

app = Flask(__name__)


# ═══════════════════════════════════════════
#   RUTA PRINCIPAL
# ═══════════════════════════════════════════

@app.route("/")
def index():
    """Página principal — renderiza la plantilla base con todos los paneles."""
    return render_template(
        "base.html",
        conductores=CONDUCTORES_C81,
        factores_escala=FACTORES_ESCALA,
        multiplicadores=MULTIPLICADORES_EM,
        tipos_fp=TIPOS_FP,
        vaf_chars=VAF_CARACTERISTICAS,
        loc_por_pf=LOC_POR_PF,
    )


# ═══════════════════════════════════════════
#   RUTAS DE CÁLCULO
# ═══════════════════════════════════════════

@app.route("/calcular/c81basico", methods=["POST"])
def api_c81_basico():
    data  = request.get_json()
    kloc  = float(data["kloc"])
    modo  = data["modo"]
    costo = float(data.get("costo_hm", 0))
    resultado = calcular_cocomo81_basico(kloc, modo, costo)
    etapas    = distribuir_etapas_c81(resultado["esfuerzo"], resultado["tiempo"], modo)
    return jsonify({"resultado": resultado, "etapas": etapas})


@app.route("/calcular/c81", methods=["POST"])
def api_c81():
    data   = request.get_json()
    kloc   = float(data["kloc"])
    modo   = data["modo"]
    eaf    = float(data["eaf"])
    costo  = float(data.get("costo_hm", 0))
    resultado = calcular_cocomo81(kloc, modo, eaf, costo)
    etapas    = distribuir_etapas_c81(resultado["esfuerzo"], resultado["tiempo"], modo)
    return jsonify({"resultado": resultado, "etapas": etapas})


@app.route("/calcular/c2", methods=["POST"])
def api_c2():
    data      = request.get_json()
    kloc      = float(data["kloc"])
    sf_vals   = [float(v) for v in data["sf_valores"]]
    em_vals   = [float(v) for v in data["em_valores"]]
    costo     = float(data.get("costo_hm", 0))
    resultado = calcular_cocomo2(kloc, sf_vals, em_vals, costo)
    etapas    = distribuir_etapas_c81(resultado["esfuerzo"], resultado["tiempo"], "semiacoplado")
    return jsonify({"resultado": resultado, "etapas": etapas})


@app.route("/calcular/fp", methods=["POST"])
def api_fp():
    data       = request.get_json()
    conteos    = data["conteos"]
    vaf_vals   = data["vaf_valores"]
    loc_por_pf = int(data["loc_por_pf"])
    resultado  = calcular_puntos_funcion(conteos, vaf_vals, loc_por_pf)
    return jsonify(resultado)


# ═══════════════════════════════════════════
#   RUTAS DE EXPORTACIÓN A EXCEL
# ═══════════════════════════════════════════

@app.route("/exportar/c81basico", methods=["POST"])
def exportar_c81basico():
    data = request.get_json()
    buf, filename = build_c81basico(data)
    return send_file(buf, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                     as_attachment=True, download_name=filename)


@app.route("/exportar/c81", methods=["POST"])
def exportar_c81():
    data = request.get_json()
    buf, filename = build_c81(data)
    return send_file(buf, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                     as_attachment=True, download_name=filename)


@app.route("/exportar/c2", methods=["POST"])
def exportar_c2():
    data = request.get_json()
    buf, filename = build_cocomo2(data)
    return send_file(buf, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                     as_attachment=True, download_name=filename)


@app.route("/exportar/fp", methods=["POST"])
def exportar_fp():
    data = request.get_json()
    buf, filename = build_fp(data)
    return send_file(buf, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                     as_attachment=True, download_name=filename)


# ═══════════════════════════════════════════
#   RUTAS DE EXPORTACIÓN A PDF
# ═══════════════════════════════════════════

@app.route("/exportar-pdf/c81basico", methods=["POST"])
def exportar_pdf_c81basico():
    data = request.get_json()
    buf, filename = build_c81basico_pdf(data)
    return send_file(buf, mimetype="application/pdf",
                     as_attachment=True, download_name=filename)


@app.route("/exportar-pdf/c81", methods=["POST"])
def exportar_pdf_c81():
    data = request.get_json()
    buf, filename = build_c81_pdf(data)
    return send_file(buf, mimetype="application/pdf",
                     as_attachment=True, download_name=filename)


@app.route("/exportar-pdf/c2", methods=["POST"])
def exportar_pdf_c2():
    data = request.get_json()
    buf, filename = build_cocomo2_pdf(data)
    return send_file(buf, mimetype="application/pdf",
                     as_attachment=True, download_name=filename)


@app.route("/exportar-pdf/fp", methods=["POST"])
def exportar_pdf_fp():
    data = request.get_json()
    buf, filename = build_fp_pdf(data)
    return send_file(buf, mimetype="application/pdf",
                     as_attachment=True, download_name=filename)


if __name__ == "__main__":
    app.run(debug=True)
