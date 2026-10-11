setTimeout(() => {
  const R = [];
  try {
    const card = document.querySelector('.wotd');
    const sw = (dx) => { card.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true, pointerType: 'touch', clientX: 200, clientY: 300 })); card.dispatchEvent(new PointerEvent('pointerup', { bubbles: true, pointerType: 'touch', clientX: 200 + dx, clientY: 305 })); };
    R.push('start idx=' + wIdx + ' word=' + $('wWord').textContent + ' prevDisabled=' + $('wPrev').disabled + ' dots=' + $('wDots').children.length);
    $('wNext').click(); R.push('next -> idx=' + wIdx + ' word=' + $('wWord').textContent);
    sw(-120); R.push('swipe left -> idx=' + wIdx);
    sw(90); R.push('swipe right -> idx=' + wIdx);
    sw(10); R.push('tiny move (no swipe) -> idx=' + wIdx);
    $('wDots').children[4].click(); R.push('dot 5 -> idx=' + wIdx + ' nextDisabled=' + $('wNext').disabled);
    $('wReveal').click(); R.push('reveal on 5th: open=' + !$('wMeaning').hidden + ' tr=' + $('wTr').textContent);
    $('wPrev').click(); R.push('prev -> idx=' + wIdx + ' open=' + !$('wMeaning').hidden);
    $('wNext').click(); R.push('back to 5th open stays=' + !$('wMeaning').hidden);
    const seen = new Set();
    for (let d = 0; d < 60; d++) { const x = new Date(2026, 0, 1 + d); const n = Math.floor(new Date(dayKey(x) + 'T12:00:00').getTime() / 864e5); const start = (n % 60) * 5; WOTD.slice(start, start + 5).forEach(w => seen.add(w[0])); }
    R.push('distinct words over 60 days=' + seen.size + ' / total ' + WOTD.length);
  } catch (e) { R.push('ERR ' + e.message); }
  const p = document.createElement('pre'); p.id = 'OUT'; p.textContent = R.join('\n'); document.body.appendChild(p);
}, 300);
