// static/js/nav.js — Navegacion entre paneles y utilidades compartidas

// ─── CONSTANTES DE MODOS ───
const MODOS_PARAMS = {
  organico:     {a:3.2,  b:1.05, c:2.5, d:0.38},
  semiacoplado: {a:3.0,  b:1.12, c:2.5, d:0.35},
  empotrado:    {a:2.8,  b:1.20, c:2.5, d:0.32},
};

// ─── SPINNER ───
function showSpinner() { document.getElementById('spinner').classList.add('active'); }
function hideSpinner() { document.getElementById('spinner').classList.remove('active'); }

// ─── ANIMACION DE CONTADOR ───
function animateValue(el, target, duration, prefix, suffix) {
  if (!el) return;
  const start = 0;
  const startTime = performance.now();
  prefix = prefix || '';
  suffix = suffix || '';

  function update(now) {
    const elapsed = now - startTime;
    const progress = Math.min(elapsed / duration, 1);
    // Easing: cubic-bezier(0.22, 0.61, 0.36, 1)
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = start + (target - start) * eased;
    if (typeof target === 'number' && target % 1 !== 0) {
      el.textContent = prefix + current.toFixed(2) + suffix;
    } else if (target >= 1000) {
      el.textContent = prefix + Math.round(current).toLocaleString() + suffix;
    } else {
      el.textContent = prefix + current.toFixed(2) + suffix;
    }
    if (progress < 1) {
      requestAnimationFrame(update);
    } else {
      el.textContent = prefix + (typeof target === 'string' ? target : target.toLocaleString()) + suffix;
    }
  }
  requestAnimationFrame(update);
}

// ─── ACTUALIZAR GAUGE EAF ───
function actualizarGaugeEAF(eaf, gaugeFillId, gaugeMarkerId) {
  // Mapear EAF (0.7 a 1.6) a posicion 0-100%
  const minEAF = 0.65, maxEAF = 1.65;
  let pct = ((eaf - minEAF) / (maxEAF - minEAF)) * 100;
  pct = Math.max(2, Math.min(98, pct));

  const fill = document.getElementById(gaugeFillId);
  const marker = document.getElementById(gaugeMarkerId);
  if (!fill || !marker) return;

  // Color segun zona
  let color;
  if (eaf < 0.85) color = 'var(--green)';
  else if (eaf <= 1.15) color = 'var(--amber)';
  else color = 'var(--red)';

  fill.style.width = pct + '%';
  fill.style.background = color;
  marker.style.left = pct + '%';
}

// ─── REANIMAR RESULTADOS ───
function reanimarResultados(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;
  // Forzar re-animacion quitando y re-agregando la clase
  container.classList.remove('result-stagger');
  void container.offsetWidth; // force reflow
  container.classList.add('result-stagger');
}

// ─── SINCRONIZAR PARAMETROS ENTRE PANELES ───
let _syncedKloc = 10;
let _syncedCosto = 3000;

function _capturarParams(origen) {
  const klocEl = document.getElementById(origen + '-kloc');
  const costEl = document.getElementById(origen + '-costo');
  if (klocEl) _syncedKloc = parseFloat(klocEl.value) || _syncedKloc;
  if (costEl) _syncedCosto = parseFloat(costEl.value) || _syncedCosto;
}

function _aplicarParams(destino) {
  const klocEl = document.getElementById(destino + '-kloc');
  const costEl = document.getElementById(destino + '-costo');
  if (klocEl) klocEl.value = _syncedKloc;
  if (costEl) costEl.value = _syncedCosto;
}

function showPanel(id) {
  const actual = document.querySelector('.panel.active');
  if (actual) {
    const actualId = actual.id.replace('panel-', '');
    if (actualId !== 'fp') _capturarParams(actualId);
  }

  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  document.getElementById('panel-' + id).classList.add('active');
  const map = { c81b: 0, c81: 1, c2: 2, fp: 3 };
  document.querySelectorAll('.nav-item')[map[id]]?.classList.add('active');

  if (id !== 'fp') _aplicarParams(id);
}

// ─── RENDERIZAR ETAPAS CON BARRAS SVG ───
function renderEtapas(tbodyId, etapas) {
  const tbody = document.getElementById(tbodyId);
  tbody.innerHTML = '';
  const barW = 120, barH = 14, rx = 4;
  const colorEsfuerzo = '#5b9cf5', colorTiempo = '#f59e0b';
  const maxPct = Math.max(...etapas.map(e => e.pct), 1);

  etapas.forEach((e, i) => {
    const efW = Math.max((e.pct / maxPct) * barW, 3);
    const tiempoPct = Math.min(e.tiempo / Math.max(...etapas.map(x => x.tiempo), 0.1) * barW, barW);
    const tW = Math.max(tiempoPct, 3);

    const row = document.createElement('tr');
    row.style.opacity = '0';
    row.style.transform = 'translateX(-8px)';
    row.style.transition = `all 0.3s ease ${i * 0.06}s`;
    row.innerHTML = `
      <td class="phase-name">${e.nombre}</td>
      <td>
        <div class="bar-row">
          <svg class="bar-svg" width="${barW}" height="${barH}">
            <rect x="0" y="1" width="${efW}" height="${barH-2}" rx="${rx}" fill="${colorEsfuerzo}" opacity="0.9"/>
            <rect x="0" y="1" width="${barW}" height="${barH-2}" rx="${rx}" fill="none" stroke="${colorEsfuerzo}" stroke-opacity="0.15" stroke-width="1"/>
          </svg>
          <span class="bar-val">${e.esfuerzo} PM</span>
          <span class="bar-pct">${e.pct}%</span>
        </div>
      </td>
      <td>
        <div class="bar-row">
          <svg class="bar-svg" width="${barW}" height="${barH}">
            <rect x="0" y="1" width="${tW}" height="${barH-2}" rx="${rx}" fill="${colorTiempo}" opacity="0.9"/>
            <rect x="0" y="1" width="${barW}" height="${barH-2}" rx="${rx}" fill="none" stroke="${colorTiempo}" stroke-opacity="0.15" stroke-width="1"/>
          </svg>
          <span class="bar-val">${e.tiempo} mes</span>
        </div>
      </td>`;
    tbody.appendChild(row);

    // Animar entrada
    requestAnimationFrame(() => {
      row.style.opacity = '1';
      row.style.transform = 'translateX(0)';
    });
  });
}

// ─── LISTENER: CONSTANTES DEL MODO BASICO ───
// NOTA: No usar DOMContentLoaded — los scripts cargan al final del <body>
(function() {
  const modoSelect = document.getElementById('c81b-modo');
  if (modoSelect) {
    modoSelect.addEventListener('change', function() {
      const p = MODOS_PARAMS[this.value];
      document.getElementById('c81b-const-a').textContent = p.a;
      document.getElementById('c81b-const-b').textContent = p.b;
      document.getElementById('c81b-const-c').textContent = p.c;
      document.getElementById('c81b-const-d').textContent = p.d;
    });
  }
})();
