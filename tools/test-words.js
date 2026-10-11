setTimeout(() => {
  const R = [];
  try {
    localStorage.clear();
    // an old save with learned words stored as 1 must still work
    S.learned = { CAT: 1, DOG: 1 }; for (const k of Object.keys(S.learned)) if (typeof S.learned[k] !== 'object') S.learned[k] = { at: null, lv: null, hard: false };
    show('words'); R.push('old save: count=' + $('wCount').textContent + ' quizDisabled=' + $('reviewGo').disabled + ' sub=' + $('reviewSub').textContent);
    // solve one A1 puzzle: one word with a hint, one with a mistake
    const key = k => document.body.dispatchEvent(new KeyboardEvent('keydown', { key: k, bubbles: true }));
    openGame('A1:0');
    pickWord(G.words[0]); 'ZZZ'.split('').forEach(key);
    pickWord(G.words[1]); hintLetter();
    for (const w of G.words.filter(w => w.dir === 'A')) for (const [r, c] of w.cells) { G.cur = G.cells[r][c]; G.dir = 'A'; key(G.cells[r][c].sol); }
    show('words');
    R.push('after puzzle: ' + $('wCount').textContent + ' | total=' + $('sumAll').textContent + ' week=' + $('sumWeek').textContent + ' due=' + $('sumDue').textContent);
    R.push('chips=' + [...$('wChips').children].map(b => b.textContent).join(', '));
    R.push('first row=' + $('wList').children[0].textContent.trim().replace(/\s+/g, ' '));
    $('wChips').querySelector('[data-f=due]').click(); R.push('due filter rows=' + $('wList').querySelectorAll('.wrow').length);
    $('wSort').querySelector('[data-s=az]').click(); $('wChips').querySelector('[data-f=all]').click();
    R.push('A-Z first three=' + [...$('wList').querySelectorAll('.en')].slice(0, 3).map(e => e.textContent).join(','));
    $('wSearch').value = 'kedi'; renderWords(); R.push('search kedi -> ' + [...$('wList').querySelectorAll('.en')].map(e => e.textContent).join(',')); $('wSearch').value = ''; renderWords();
    // quiz
    $('reviewGo').click(); R.push('quiz screen=' + screen + ' q=' + $('qSub').textContent + ' opts=' + $('qOpts').children.length + ' bar=' + $('qBar').children.length);
    const dupOpts = Q.items.some(it => new Set(it.opts).size !== 4 || !it.opts.includes(it.w));
    R.push('every question has 4 different options incl. answer=' + !dupOpts);
    R.push('hard words asked first=' + Q.items.slice(0, 2).every(it => needsReview(it.w)));
    let right = 0;
    Q.items.forEach((it, i) => {
      const pick = i % 3 === 0 ? it.opts.find(o => o !== it.w) : it.w;
      if (i === 1) { key('1'); } else $('qOpts').querySelector(`[data-o="${pick}"]`).click();
      if (Q.items[i].res === 'ok') right++;
      if (i < Q.items.length - 1) $('qNext').click(); else key('Enter');
    });
    R.push('result=' + $('qScore').textContent + ' (counted ' + right + ') done shown=' + !$('qDone').hidden + ' missed rows=' + $('qMiss').children.length);
    R.push('review saved=' + Object.keys(JSON.parse(localStorage.getItem('cengel-app-v2')).review).length);
    show('settings'); $('wipe').click(); $('wipe').click(); show('words'); R.push('after wipe: ' + $('wCount').textContent);
  } catch (e) { R.push('ERR ' + e.message + ' ' + e.stack.split('\n')[1]); }
  const p = document.createElement('pre'); p.id = 'OUT'; p.textContent = R.join('\n'); document.body.appendChild(p);
}, 300);
