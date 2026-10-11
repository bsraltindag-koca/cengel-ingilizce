window.__errs = [];
window.addEventListener('error', e => __errs.push('onerror: ' + e.message));
setTimeout(() => {
  const R = {}, errs = __errs;
  const key = k => document.body.dispatchEvent(new KeyboardEvent('keydown', { key: k, bubbles: true }));
  const typeWord = w => { for (const [r, c] of w.cells) { G.cur = G.cells[r][c]; G.dir = w.dir; const s = G.cells[r][c].sol; key(s === 'I' ? 'ı' : s.toLowerCase()); } };
  const fresh = id => { delete S.games[id]; delete S.done[id]; };
  let confettiCalls = 0; const oc = window.confetti; window.confetti = () => { confettiCalls++; };
  const origSetTimeout = window.setTimeout;
  // T1: every puzzle solvable, finishes once with full score
  const ids = [];
  for (const L of LEVELS) DATA.levels[L.k].forEach((_, i) => ids.push(`${L.k}:${i}`));
  const base = new Date('2026-10-01T12:00:00');
  for (let d = 0; d < 30; d++) { const x = new Date(base); x.setDate(x.getDate() + d); ids.push('D:' + dayKey(x)); }
  const bad1 = [];
  for (const id of ids) {
    try {
      fresh(id); openGame(id);
      // integrity: 24 clue cells, answers match grid, clues are not empty
      const clueCells = document.querySelectorAll('#grid .cell.clue').length;
      if (clueCells !== 24) bad1.push(id + ' clueCells=' + clueCells);
      G.words.forEach(w => { if (!w.clue || w.clue === w.answer) bad1.push(id + ' noclue ' + w.answer); });
      G.words.filter(w => w.dir === 'A').forEach(typeWord);
      if (!G.finished || G.st.sw.length !== 24) bad1.push(id + ' notFinished sw=' + G.st.sw.length);
      else if (S.done[id].score !== 24 * 35 + 200) bad1.push(id + ' score=' + S.done[id].score);
    } catch (e) { bad1.push(id + ' ERR ' + e.message); }
  }
  R.T1 = { puzzles: ids.length, problems: bad1.slice(0, 10), problemCount: bad1.length };

  // T2: finishing with "Kelime aç" adds the bonus once
  try {
    const id = 'A2:0'; fresh(id); openGame(id);
    const holdA = G.words[0], [hr, hc] = holdA.cells[0];
    for (const w of G.words) for (const [r, c] of w.cells) { if (r === hr && c === hc) continue; G.cur = G.cells[r][c]; G.dir = w.dir; key(G.cells[r][c].sol); }
    const before = G.st.sw.length;
    pickWord(holdA); hintWord();
    R.T2 = { solvedBefore: before, finished: !!G.finished, score: S.done[id] && S.done[id].score, expected: 22 * 35 + 25 + 35 - 40 + 200, stateScore: G.st.score };
  } catch (e) { R.T2 = 'ERR ' + e.message; }

  // T3: typing on a locked square goes to the next open square
  try {
    const id = 'A1:5'; fresh(id); openGame(id);
    const d0 = G.words.find(w => w.dir === 'D'); typeWord(d0);
    const a0 = G.cells[d0.cells[0][0]][d0.cells[0][1]].A;
    G.cur = G.cells[a0.cells[0][0]][a0.cells[0][1]]; G.dir = 'A';
    const want = G.cells[a0.cells[1][0]][a0.cells[1][1]].sol;
    key(want);
    R.T3 = { lockedFirst: locked(...a0.cells[0]), secondNow: val(...a0.cells[1]), want };
  } catch (e) { R.T3 = 'ERR ' + e.message; }

  // T4: random monkey
  let seed = 7; const rnd = n => { seed = (seed * 1103515245 + 12345) % 2147483648; return seed % n; };
  const keys = [...'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'Backspace', 'Delete', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'Tab', ' ', 'Enter', 'ı', 'ş', '1'];
  const inv = [];
  try {
    openGame(ids[rnd(ids.length)]);
    for (let step = 0; step < 4000; step++) {
      const a = rnd(100);
      try {
        if (screen !== 'game') { if (a < 70) openGame(ids[rnd(ids.length)]); else show(['home', 'words', 'stats', 'settings'][rnd(4)]); continue; }
        if (a < 45) key(keys[rnd(keys.length)]);
        else if (a < 60) { const r = rnd(8), c = rnd(8); const cell = G.cells[r][c]; if (cell.sol) tapCell(r, c); else if (G.grid && cell.el.classList.contains('clue')) cell.el.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })); }
        else if (a < 66) hintLetter();
        else if (a < 69) hintWord();
        else if (a < 74) check();
        else if (a < 78) $('nextW').click();
        else if (a < 81) $('prevW').click();
        else if (a < 83) { pause(); $('resume').click(); }
        else if (a < 85) { const b = $('kbd').querySelectorAll('button')[rnd(28)]; b && b.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })); }
        else if (a < 86) show(['home', 'words', 'stats', 'settings', 'play'][rnd(5)]);
        else if (a < 87) { $('sReset').click(); $('sReset').click(); }
        else key(keys[rnd(26)]);
        if (G && screen === 'game') {
          if (G.st.score < 0) inv.push(step + ' negative score');
          if (new Set(G.st.sw).size !== G.st.sw.length) inv.push(step + ' duplicate solved');
          for (const i of G.st.sw) { const w = G.words[i]; if (w.cells.map(([r, c]) => val(r, c)).join('') !== w.answer) inv.push(step + ' solved word wrong ' + w.answer); }
          if (!G.cur || !G.cur.sol) inv.push(step + ' cursor off grid');
        }
      } catch (e) { errs.push('step ' + step + ': ' + e.message); if (errs.length > 15) break; }
    }
  } catch (e) { errs.push('monkey ' + e.message); }
  R.T4 = { invariantProblems: inv.slice(0, 8), invariantCount: inv.length };
  // T5: every screen and level page renders
  try { ['home', 'words', 'stats', 'settings'].forEach(show); LEVELS.forEach(L => openLevel(L.k)); R.T5 = 'ok'; } catch (e) { R.T5 = 'ERR ' + e.message; }
  R.errors = errs.slice(0, 15); R.errorCount = errs.length;
  origSetTimeout(() => { R.confettiCalls = confettiCalls; const p = document.createElement('pre'); p.id = 'OUT'; p.textContent = JSON.stringify(R, null, 1); document.body.appendChild(p); }, 1500);
}, 300);
