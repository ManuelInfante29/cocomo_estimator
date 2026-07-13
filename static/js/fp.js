// static/js/fp.js — Puntos de Función (FPA)

let ultimoResultadoFP = null;

async function calcularFP() {
  showSpinner();
  try {
    const fpCodes = ['EI','EO','EQ','ILF','EIF'];
    const conteos = {};
    fpCodes.forEach(c => {
      conteos[c] = [
        parseInt(document.getElementById(`fp-${c}-s`).value)||0,
        parseInt(document.getElementById(`fp-${c}-m`).value)||0,
        parseInt(document.getElementById(`fp-${c}-c`).value)||0,
      ];
    });
    const vaf_valores = Array.from({length:14}, (_,i) => parseInt(document.getElementById(`vaf-${i}`).value)||0);

    const loc_por_pf = parseInt(document.getElementById('fp-lang').value);

    const body = { conteos, vaf_valores, loc_por_pf };

    const res  = await fetch('/calcular/fp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    const r = await res.json();

    document.getElementById('r-fp-pfsa').textContent = r.pfsa;
    document.getElementById('r-fp-vaf').textContent  = r.vaf;
    document.getElementById('r-fp-pfa').textContent  = r.pfa;
    document.getElementById('r-fp-kloc').textContent = r.kloc;

    ultimoResultadoFP = { body, resultado: r, fpCodes };
    mostrarBotonesExport('fp', true);
  } finally {
    hideSpinner();
  }
}

// ─── ENVÍO DE KLOC A OTROS MODELOS ───
function enviarAC81b() {
  const k = document.getElementById('r-fp-kloc').textContent;
  if (k === '—') return alert('Primero calcula los Puntos de Función');
  document.getElementById('c81b-kloc').value = k;
  showPanel('c81b');
}
function enviarAC81() {
  const k = document.getElementById('r-fp-kloc').textContent;
  if (k === '—') return alert('Primero calcula los Puntos de Función');
  document.getElementById('c81-kloc').value = k;
  showPanel('c81');
}
function enviarAC2() {
  const k = document.getElementById('r-fp-kloc').textContent;
  if (k === '—') return alert('Primero calcula los Puntos de Función');
  document.getElementById('c2-kloc').value = k;
  showPanel('c2');
}
