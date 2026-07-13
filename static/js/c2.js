// static/js/c2.js — COCOMO II Post-Arquitectura

const C2_SF_CODES = ['PREC','FLEX','RESL','TEAM','PMAT'];
const C2_EM_CODES = ['RELY','DATA','CPLX','RUSE','DOCU','TIME','STOR','PVOL','ACAP','PCAP','PCON','APEX','PLEX','LTEX','TOOL','SITE','SCED'];

// ─── RECALCULAR B Y EM EN TIEMPO REAL ───
function recalcularByEM() {
  // Exponente B
  let sumSF = 0;
  C2_SF_CODES.forEach(code => {
    const el = document.getElementById('sf-' + code);
    if (el) sumSF += parseFloat(el.value);
  });
  const B = 0.91 + 0.01 * sumSF;
  const bDisplay = document.getElementById('c2-B-display');
  if (bDisplay) bDisplay.textContent = B.toFixed(3);

  // Producto EM
  let EM = 1.0;
  C2_EM_CODES.forEach(code => {
    const el = document.getElementById('em-' + code);
    if (el) EM *= parseFloat(el.value);
  });
  EM = Math.round(EM * 10000) / 10000;

  const emDisplay = document.getElementById('em-display');
  if (emDisplay) {
    emDisplay.textContent = EM.toFixed(2);
    colorEAF(EM, 'em-display');
  }

  actualizarGaugeEAF(EM, 'em-gauge-fill', 'em-gauge-marker');
  return { B, EM, sumSF };
}

// ─── COCOMO II ───
let ultimoResultadoC2 = null;

async function calcularC2() {
  showSpinner();
  try {
    const { B, EM, sumSF } = recalcularByEM();

    const kloc = parseFloat(document.getElementById('c2-kloc').value);
    const costo_hm = parseFloat(document.getElementById('c2-costo').value);
    _capturarParams('c2');

    const sf_valores = C2_SF_CODES.map(c => parseFloat(document.getElementById('sf-' + c).value));
    const em_valores = C2_EM_CODES.map(c => parseFloat(document.getElementById('em-' + c).value));

    const body = { kloc, sf_valores, em_valores, costo_hm };

    const res  = await fetch('/calcular/c2', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    const data = await res.json();
    const r    = data.resultado;

    reanimarResultados('results-c2');

    animateValue(document.getElementById('r-c2-effort'), r.esfuerzo, 800, '', '');
    animateValue(document.getElementById('r-c2-time'),   r.tiempo,   800, '', '');
    animateValue(document.getElementById('r-c2-staff'),  r.personal, 800, '', '');
    document.getElementById('r-c2-cost').textContent = 'S/. ' + r.costo.toLocaleString();

    renderEtapas('c2-etapas', data.etapas);

    document.getElementById('c2-eq').innerHTML = `
      <span class="ec">// COCOMO II Post-Arquitectura</span><br>
      <span class="ev">B</span> = 0.91 + 0.01 x SF(<span class="en">${r.suma_sf}</span>) = <span class="ev">${r.B}</span><br>
      <span class="ev">E</span> = <span class="en">2.94</span> x <span class="en">${body.kloc}</span>^<span class="ev">${r.B}</span> x <span class="en">${r.EM}</span> = <span class="ev">${r.esfuerzo}</span> PM<br>
      <span class="ev">T</span> = 3.67 x ${r.esfuerzo}^(0.28+0.002x${r.suma_sf}) = <span class="ev">${r.tiempo}</span> meses<br>
      <span class="ev">N</span> = ${r.esfuerzo} / ${r.tiempo} = <span class="ev">${r.personal}</span> personas`;

    ultimoResultadoC2 = { body, resultado: r, etapas: data.etapas, B, EM, sumSF, sfCodes: C2_SF_CODES, emCodes: C2_EM_CODES };
    mostrarBotonesExport('c2', true);
  } finally {
    hideSpinner();
  }
}

// ─── LISTENERS: ACTUALIZAR B Y EM EN TIEMPO REAL ───
// NOTA: No usar DOMContentLoaded — los scripts cargan al final del <body>,
// por lo que DOMContentLoaded ya se disparó y el callback nunca se ejecutaría.
(function() {
  C2_SF_CODES.forEach(code => {
    const el = document.getElementById('sf-' + code);
    if (el) el.addEventListener('change', recalcularByEM);
  });
  C2_EM_CODES.forEach(code => {
    const el = document.getElementById('em-' + code);
    if (el) el.addEventListener('change', recalcularByEM);
  });
  // Inicializar con valores por defecto
  recalcularByEM();
})();
