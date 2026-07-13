// static/js/api.js — Helpers de fetch, exportación a Excel y PDF

// ─── EXPORTAR A EXCEL ───
function exportarExcel(modelo) {
  let payload = null;
  if (modelo === 'c81basico' && typeof ultimoResultadoC81b !== 'undefined') {
    payload = ultimoResultadoC81b;
  } else if (modelo === 'c81' && typeof ultimoResultadoC81 !== 'undefined') {
    payload = ultimoResultadoC81;
  } else if (modelo === 'c2' && typeof ultimoResultadoC2 !== 'undefined') {
    payload = ultimoResultadoC2;
  } else if (modelo === 'fp' && typeof ultimoResultadoFP !== 'undefined') {
    payload = ultimoResultadoFP;
  }
  if (!payload) return alert('Primero debes calcular los resultados.');

  fetch('/exportar/' + modelo, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  .then(res => res.blob())
  .then(blob => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    const nombres = { c81basico: 'COCOMO81_Basico', c81: 'COCOMO81_Intermedio', c2: 'COCOMO_II', fp: 'Puntos_Funcion' };
    a.download = nombres[modelo] + '_' + new Date().toISOString().slice(0,10) + '.xlsx';
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  })
  .catch(() => alert('Error al generar el archivo Excel.'));
}

// ─── EXPORTAR A PDF ───
function exportarPDF(modelo) {
  let payload = null;
  if (modelo === 'c81basico' && typeof ultimoResultadoC81b !== 'undefined') {
    payload = ultimoResultadoC81b;
  } else if (modelo === 'c81' && typeof ultimoResultadoC81 !== 'undefined') {
    payload = ultimoResultadoC81;
  } else if (modelo === 'c2' && typeof ultimoResultadoC2 !== 'undefined') {
    payload = ultimoResultadoC2;
  } else if (modelo === 'fp' && typeof ultimoResultadoFP !== 'undefined') {
    payload = ultimoResultadoFP;
  }
  if (!payload) return alert('Primero debes calcular los resultados.');

  fetch('/exportar-pdf/' + modelo, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  .then(res => res.blob())
  .then(blob => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    const nombres = { c81basico: 'COCOMO81_Basico', c81: 'COCOMO81_Intermedio', c2: 'COCOMO_II', fp: 'Puntos_Funcion' };
    a.download = nombres[modelo] + '_' + new Date().toISOString().slice(0,10) + '.pdf';
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  })
  .catch(() => alert('Error al generar el archivo PDF.'));
}
