// "En çok hata" sort: puzzle mistakes + review misses, hardest first, with a "N hata" tag
setTimeout(() => {
  const R = [];
  try {
    localStorage.clear();
    S.learned = {
      CAT: { at: '2026-10-01', lv: 'A1', hard: false, miss: 0 },
      DOG: { at: '2026-10-02', lv: 'A1', hard: true, miss: 1 },
      SUN: { at: '2026-10-03', lv: 'A1', hard: true, miss: 0 },
      SEA: { at: '2026-10-04', lv: 'A2', hard: false, miss: 3 },
      RED: { at: null, lv: null, hard: false },            // an older save without a mistake count
    };
    S.review = { CAT: { ok: 0, bad: 2 }, SUN: { ok: 1, bad: 0 } };
    show('words');
    $('wSort').querySelector('[data-s=err]').click();
    R.push('order=' + [...$('wList').querySelectorAll('.en')].map(e => e.textContent).join(','));
    R.push('tags=' + [...$('wList').querySelectorAll('.wrow')].map(r => r.querySelector('.en').textContent + ':' + ([...r.querySelectorAll('.tagc.err')].map(t => t.textContent).join('') || '-')).join(' '));
    R.push('selected=' + $('wSort').querySelector('[aria-checked=true]').textContent);
    $('wSort').querySelector('[data-s=az]').click();
    R.push('A-Z has no hata tags=' + !$('wList').querySelector('.tagc.err'));
  } catch (e) { R.push('ERR ' + e.message); }
  const p = document.createElement('pre'); p.id = 'OUT'; p.textContent = R.join('\n'); document.body.appendChild(p);
}, 300);
