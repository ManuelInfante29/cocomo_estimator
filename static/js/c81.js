// static/js/c81.js — COCOMO 81 Basico e Intermedio

// ─── HELPER SEMAFORO EAF ───
function colorEAF(eaf, displayId) {
  const el = document.getElementById(displayId);
  if (!el) return;
  el.classList.remove('favorable', 'neutral', 'unfavorable');
  if (eaf < 0.85) el.classList.add('favorable');
  else if (eaf <= 1.15) el.classList.add('neutral');
  else el.classList.add('unfavorable');
}

// ─── MOSTRAR BOTONES DE EXPORTACION ───
function mostrarBotonesExport(panel, hayPdf) {
  const btnExcel = document.getElementById('btn-export-' + panel);
  if (btnExcel) btnExcel.style.display = 'inline-block';
  if (hayPdf) {
    const btnPdf = document.getElementById('btn-pdf-' + panel);
    if (btnPdf) btnPdf.style.display = 'inline-block';
  }
}

// ─── RECALCULAR EAF EN TIEMPO REAL (C81 Intermedio) ───
const C81_DRIVER_CODES = ['RELY','DATA','CPLX','TIME','STOR','VIRT','TURN','ACAP','AEXP','PCAP','VEXP','LEXP','MODP','TOOL','SCED'];

function recalcularEAF() {
  let eaf = 1.0;
  C81_DRIVER_CODES.forEach(code => {
    const el = document.getElementById('c81-' + code);
    if (el) eaf *= parseFloat(el.value);
  });
  eaf = Math.round(eaf * 1000) / 1000;

  const display = document.getElementById('c81-eaf-display');
  if (display) {
    display.textContent = eaf.toFixed(2);
    colorEAF(eaf, 'c81-eaf-display');
  }

  actualizarGaugeEAF(eaf, 'c81-eaf-gauge-fill', 'c81-eaf-gauge-marker');
  return eaf;
}

// ─── COCOMO 81 BASICO ───
let ultimoResultadoC81b = null;

async function calcularC81Basico() {
  showSpinner();
  try {
    const body = {
      kloc:     parseFloat(document.getElementById('c81b-kloc').value),
      modo:     document.getElementById('c81b-modo').value,
      costo_hm: parseFloat(document.getElementById('c81b-costo').value),
    };
    _capturarParams('c81b');

    const res = await fetch('/calcular/c81basico', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    const data = await res.json();
    const r = data.resultado;
    const p = r.params;

    reanimarResultados('results-c81b');

    animateValue(document.getElementById('r-c81b-effort'), r.esfuerzo, 800, '', '');
    animateValue(document.getElementById('r-c81b-time'),   r.tiempo,   800, '', '');
    animateValue(document.getElementById('r-c81b-staff'),  r.personal, 800, '', '');
    document.getElementById('r-c81b-cost').textContent = 'S/. ' + r.costo.toLocaleString();

    renderEtapas('c81b-etapas', data.etapas);

    document.getElementById('c81b-eq').innerHTML = `
      <span class="ec">// COCOMO 81 Basico — EAF = 1 (sin conductores de coste)</span><br>
      <span class="ec">// Modo: ${body.modo} — a=${p.a}, b=${p.b}, c=${p.c}, d=${p.d}</span><br>
      <span class="ev">E</span> = <span class="en">${p.a}</span> x <span class="en">${body.kloc}</span>^<span class="en">${p.b}</span> = <span class="ev">${r.esfuerzo}</span> PM<br>
      <span class="ev">T</span> = <span class="en">${p.c}</span> x <span class="en">${r.esfuerzo}</span>^<span class="en">${p.d}</span> = <span class="ev">${r.tiempo}</span> meses<br>
      <span class="ev">N</span> = ${r.esfuerzo} / ${r.tiempo} = <span class="ev">${r.personal}</span> personas<br>
      <span class="ev">Costo</span> = ${r.esfuerzo} x $${body.costo_hm.toLocaleString()} = <span class="ev">$${r.costo.toLocaleString()}</span>`;

    ultimoResultadoC81b = { body, resultado: r, etapas: data.etapas };
    mostrarBotonesExport('c81b', true);
  } finally {
    hideSpinner();
  }
}

// ─── COCOMO 81 INTERMEDIO ───
let ultimoResultadoC81 = null;

async function calcularC81() {
  showSpinner();
  try {
    // El EAF ya esta actualizado en tiempo real por los listeners
    const eaf = recalcularEAF();

    const kloc = parseFloat(document.getElementById('c81-kloc').value);
    const modo = document.getElementById('c81-modo').value;
    const costo_hm = parseFloat(document.getElementById('c81-costo').value);
    _capturarParams('c81');

    const body = { kloc, modo, eaf, costo_hm };

    const res = await fetch('/calcular/c81', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    const data = await res.json();
    const r = data.resultado;
    const p = r.params;

    reanimarResultados('results-c81');

    animateValue(document.getElementById('r-c81-effort'), r.esfuerzo, 800, '', '');
    animateValue(document.getElementById('r-c81-time'),   r.tiempo,   800, '', '');
    animateValue(document.getElementById('r-c81-staff'),  r.personal, 800, '', '');
    document.getElementById('r-c81-cost').textContent = 'S/. ' + r.costo.toLocaleString();

    renderEtapas('c81-etapas', data.etapas);

    // Recolectar valores de drivers para exportacion
    const valoresDrivers = {};
    C81_DRIVER_CODES.forEach(code => {
      const el = document.getElementById('c81-' + code);
      if (el) {
        valoresDrivers[code] = {
          nombre: el.parentElement.querySelector('.driver-name')?.textContent || code,
          valor: parseFloat(el.value)
        };
      }
    });

    document.getElementById('c81-eq').innerHTML = `
      <span class="ec">// Modo: ${body.modo} — a=${p.a}, b=${p.b}, c=${p.c}, d=${p.d}</span><br>
      <span class="ev">E</span> = <span class="en">${p.a}</span> x <span class="en">${body.kloc}</span>^<span class="en">${p.b}</span> x <span class="en">${eaf}</span> = <span class="ev">${r.esfuerzo}</span> PM<br>
      <span class="ev">T</span> = <span class="en">${p.c}</span> x <span class="en">${r.esfuerzo}</span>^<span class="en">${p.d}</span> = <span class="ev">${r.tiempo}</span> meses<br>
      <span class="ev">N</span> = ${r.esfuerzo} / ${r.tiempo} = <span class="ev">${r.personal}</span> personas<br>
      <span class="ev">Costo</span> = ${r.esfuerzo} x $${body.costo_hm.toLocaleString()} = <span class="ev">$${r.costo.toLocaleString()}</span>`;

    ultimoResultadoC81 = { body, resultado: r, etapas: data.etapas, eaf, valoresDrivers };
    mostrarBotonesExport('c81', true);
  } finally {
    hideSpinner();
  }
}

// ─── LISTENERS: ACTUALIZAR EAF EN TIEMPO REAL ───
// NOTA: No usar DOMContentLoaded — los scripts cargan al final del <body>,
// por lo que DOMContentLoaded ya se disparó y el callback nunca se ejecutaría.
(function() {
  C81_DRIVER_CODES.forEach(code => {
    const el = document.getElementById('c81-' + code);
    if (el) {
      el.addEventListener('change', recalcularEAF);
    }
  });
  // Inicializar el gauge con el EAF por defecto (todos en nominal = 1.0)
  recalcularEAF();
})();
