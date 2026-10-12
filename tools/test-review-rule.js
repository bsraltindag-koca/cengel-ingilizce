// hint attribution: only the selected word counts as hinted; one right review answer clears it
setTimeout(() => {
  const R = [];
  try {
    localStorage.clear(); S.learned = {}; S.review = {};
    const key = k => document.body.dispatchEvent(new KeyboardEvent('keydown', { key: k, bubbles: true }));
    openGame('A2:3');
    const a0 = G.words.find(w => w.dir === 'A' && G.cells[w.cells[0][0]][w.cells[0][1]].D);
    const cross = G.cells[a0.cells[0][0]][a0.cells[0][1]].D;
    pickWord(a0); G.cur = G.cells[a0.cells[0][0]][a0.cells[0][1]]; G.dir = 'A'; hintLetter();
    for (const w of G.words) for (const [r, c] of w.cells) { if (locked(r, c)) continue; G.cur = G.cells[r][c]; G.dir = w.dir; key(G.cells[r][c].sol); }
    R.push('finished=' + !!G.finished);
    R.push('selected word ' + a0.answer + ' hard=' + S.learned[a0.answer].hard + ' | crossing word ' + cross.answer + ' hard=' + S.learned[cross.answer].hard);
    R.push('done screen hinted words=' + G.st.hw.map(i => G.words[i].answer).join(','));
    R.push('needs review before=' + needsReview(a0.answer));
    S.review[a0.answer] = { ok: 1, bad: 0 }; R.push('after one right answer=' + needsReview(a0.answer));
    S.review[a0.answer] = { ok: 1, bad: 2 }; R.push('more wrong than right=' + needsReview(a0.answer));
  } catch (e) { R.push('ERR ' + e.message); }
  const p = document.createElement('pre'); p.id = 'OUT'; p.textContent = R.join('\n'); document.body.appendChild(p);
}, 300);
