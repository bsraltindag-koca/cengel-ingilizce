// Home card: new words of the day when nothing needs review; the words to review (most mistakes first) when some do
setTimeout(() => {
  const R = [];
  try {
    const ws = Object.keys(DATA.hints).filter(w => w.length > 3).slice(0, 7);
    S.learned = {}; S.review = {};
    ws.forEach(w => S.learned[w] = { at: dayKey(), lv: 'A1', hard: false, miss: 0 });
    show('home');
    R.push('no mistakes: title=' + $('wTitle').textContent + ' first=' + $('wWord').textContent + ' (wotd ' + todaysWords()[0][0] + ') button hidden=' + $('wReview').hidden);
    S.learned[ws[1]] = { ...S.learned[ws[1]], hard: true, miss: 1 };
    S.learned[ws[4]] = { ...S.learned[ws[4]], hard: true, miss: 3 };
    show('home');
    R.push('with mistakes: title=' + $('wTitle').textContent + ' words=' + cardWords().list.map(x => x[0]).join(',') + ' expected=' + [ws[4], ws[1]].map(lowerEn).join(',') + ' dots=' + $('wDots').children.length);
    $('wReveal').click();
    R.push('meaning: ' + $('wTr').textContent + ' | ' + $('wEn').textContent + ' | ' + $('wTrEx').textContent + ' | ' + (DATA.clues[ws[4]] || '') );
    $('wReview').click();
    R.push('button opens quiz: screen=' + screen + ' questions=' + Q.items.length + ' words=' + Q.items.map(x => x.w).sort().join(','));
    Q.items.forEach((it, i) => { Q.i = i; answer(it.w); });
    show('home');
    R.push('after answering right: title=' + $('wTitle').textContent);
  } catch (e) { R.push('ERR ' + e.message + ' ' + (e.stack || '').split('\n')[1]); }
  const p = document.createElement('pre'); p.id = 'OUT'; p.textContent = R.join('\n'); document.body.appendChild(p);
}, 300);
