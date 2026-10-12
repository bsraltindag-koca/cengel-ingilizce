// "?" next to the clue: shows the note for the current word, follows word changes, never the answer
setTimeout(() => {
  const R = [];
  try {
    openGame('A1:0');
    const btn = document.querySelector('.banner [data-hint-toggle]'), box = $('hintBox');
    R.push('button visible=' + !btn.hidden + ' box hidden at start=' + box.hidden);
    btn.click();
    const w1 = curWord();
    R.push('open: ' + w1.clue + ' -> [' + box.querySelector('.tur').textContent + '] ' + box.querySelector('.ac').textContent + ' | ' + box.querySelector('.ex').textContent);
    R.push('answer hidden in note=' + !new RegExp('\\b' + w1.answer + '\\b', 'i').test(box.textContent));
    $('nextW').click(); const w2 = curWord();
    R.push('next word keeps box open=' + !box.hidden + ' now about ' + w2.clue + ': ' + box.querySelector('.ac').textContent);
    btn.click(); R.push('closed=' + box.hidden + ' expanded=' + btn.getAttribute('aria-expanded'));
    btn.click(); $('hintShade').dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })); R.push('tap on dark area closes=' + box.hidden + ' shade hidden=' + $('hintShade').hidden);
    let missing = 0, leaks = 0;
    for (const id of Object.keys(DATA.long).flatMap(k => DATA.long[k].map((_, i) => k === 'IELTS' ? 'IE:' + i : k + ':' + i))) {
      for (const w of meta(id).long.words) { const h = DATA.hints[w.answer]; if (!h) missing++; else if (new RegExp('(^|[^a-zçğıöşü])' + w.answer + '([^a-zçğıöşü]|$)', 'i').test(h[1] + ' ' + h[2])) leaks++; }
    }
    R.push('words without a note=' + missing + ' notes that show the answer=' + leaks);
  } catch (e) { R.push('ERR ' + e.message); }
  const p = document.createElement('pre'); p.id = 'OUT'; p.textContent = R.join('\n'); document.body.appendChild(p);
}, 300);
