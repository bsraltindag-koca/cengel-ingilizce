// stats page: activity log, weekly bars, month calendar, records + "Yeni rekor", badges, weak spots
setTimeout(() => {
  const R = [];
  try {
    localStorage.clear();
    S.games = {}; S.done = {}; S.learned = {}; S.review = {}; S.activity = {}; S.rec = {}; S.streak = { last: null, count: 0, best: 0 };
    const key = k => document.body.dispatchEvent(new KeyboardEvent('keydown', { key: k, bubbles: true }));
    const solveAll = () => { for (const w of G.words) for (const [r, c] of w.cells) { if (locked(r, c)) continue; G.cur = G.cells[r][c]; G.dir = w.dir; key(G.cells[r][c].sol); } };
    window.confetti = () => {};
    openGame('A1:0'); G.st.sec = 400; pickWord(G.words[0]); 'ZZZ'.split('').forEach(key); solveAll();
    R.push('puzzle 1: record msg="' + (G.newRecord || '') + '"');
    openGame('A1:1'); G.st.sec = 120; solveAll();
    R.push('puzzle 2 (faster): record msg="' + G.newRecord + '" shown=' + !$('doneRecord').hidden);
    const today = S.activity[dayKey()];
    R.push('activity today: words=' + today.w + ' puzzles=' + today.p + ' | learned=' + Object.keys(S.learned).length);
    show('stats');
    R.push('tiles=' + [...$('statGrid').children].map(t => t.textContent.replace(/\s+/g, ' ').trim()).join(' | '));
    const bars = $('wkBars').children;
    R.push('week bars=' + bars.length + ' today label="' + bars[6].querySelector('.v').textContent + '" sub="' + $('wkSub').textContent + '" tip="' + bars[6].dataset.tip + '"');
    const cells = $('cal').querySelectorAll('.d:not(.pad)');
    const todayCell = $('cal').querySelector('.d.today');
    R.push('calendar days=' + cells.length + ' title=' + $('calTitle').textContent + ' today level=' + todayCell.className + ' sub="' + $('calSub').textContent + '"');
    R.push('records=' + [...$('records').children].map(t => t.querySelector('b').textContent).join(', '));
    R.push('badges=' + $('badgeCount').textContent + ' got=' + badgeList().filter(b => b.got).map(b => b.id).join(','));
    R.push('weak list=' + [...$('weakList').querySelectorAll('.en')].map(e => e.textContent).join(',') + ' acc=' + $('accNum').textContent);
    $('weakGo').click();
    R.push('weak quiz: screen=' + screen + ' questions=' + Q.items.length + ' only weak=' + Q.items.every(it => errCount(it.w) || needsReview(it.w)));
    // a perfect 10 unlocks "Kusursuz tekrar"
    startQuiz(); Q.items.forEach((it, i) => { answer(it.w); if (i < Q.items.length - 1) Q.i++; }); nextQuestion();
    R.push('perfect quiz badge=' + badgeList().find(b => b.id === 'quiz').got);
    show('stats'); R.push('accuracy after quiz=' + $('accNum').textContent + ' (' + $('accSub').textContent + ')');
    show('settings'); $('wipe').click(); $('wipe').click(); show('stats'); R.push('after wipe: tiles=' + [...$('statGrid').children].map(t => t.querySelector('b').textContent).join(',') + ' badges=' + $('badgeCount').textContent);
  } catch (e) { R.push('ERR ' + e.message + ' @ ' + (e.stack || '').split('\n')[1]); }
  const p = document.createElement('pre'); p.id = 'OUT'; p.textContent = R.join('\n'); document.body.appendChild(p);
}, 300);
