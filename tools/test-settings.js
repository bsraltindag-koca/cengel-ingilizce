// Ayarlar: sound effects, vibration and read-aloud switches; they really switch the effects off
setTimeout(() => {
  const R = [];
  try {
    let tones = 0, vib = 0;
    const RealAC = window.AudioContext;
    window.AudioContext = function () { const ac = new RealAC(); const mk = ac.createOscillator.bind(ac); ac.createOscillator = () => { tones++; return mk(); }; return ac; };
    AC = null;
    navigator.vibrate = () => { vib++; return true; };
    const key = k => document.body.dispatchEvent(new KeyboardEvent('keydown', { key: k, bubbles: true }));
    show('settings');
    R.push('defaults: sfx=' + $('optSfx').getAttribute('aria-checked') + ' haptic=' + $('optHaptic').getAttribute('aria-checked') + ' speak=' + $('optSpeak').getAttribute('aria-checked'));
    R.push('sections=' + [...document.querySelectorAll('#s-settings .set-h')].map(h => h.textContent).join(' / '));
    openGame('A1:0'); const w = G.words[0];
    tones = 0; vib = 0; for (const [r, c] of w.cells) { G.cur = G.cells[r][c]; G.dir = w.dir; key(G.cells[r][c].sol); }
    R.push('sound on: tones while solving one word=' + tones + ' vibrations=' + vib);
    show('settings'); $('optSfx').click(); $('optHaptic').click();
    R.push('after switching off: sfx=' + S.opts.sfx + ' haptic=' + S.opts.haptic + ' saved=' + JSON.stringify({ s: JSON.parse(localStorage.getItem('cengel-app-v2')).opts.sfx, h: JSON.parse(localStorage.getItem('cengel-app-v2')).opts.haptic }));
    openGame('A1:0'); const w2 = G.words.find(x => !wordSolved(x));
    tones = 0; vib = 0; for (const [r, c] of w2.cells) { if (locked(r, c)) continue; G.cur = G.cells[r][c]; G.dir = w2.dir; key(G.cells[r][c].sol); }
    check();
    R.push('sound off: tones=' + tones + ' vibrations=' + vib);
    show('settings'); $('optSpeak').click(); R.push('read aloud off -> quizMute=' + S.opts.quizMute + ' quiz button pressed=' + $('qMute').getAttribute('aria-pressed'));
    $('qMute').click(); R.push('quiz button back on -> settings switch=' + $('optSpeak').getAttribute('aria-checked'));
  } catch (e) { R.push('ERR ' + e.message + ' @ ' + (e.stack || '').split('\n')[1]); }
  const p = document.createElement('pre'); p.id = 'OUT'; p.textContent = R.join('\n'); document.body.appendChild(p);
}, 300);
// wrong word: fill a word with wrong letters, expect warning sound + vibration + shake
setTimeout(() => {
  const R = [];
  try {
    S.opts.sfx = true; S.opts.haptic = true;
    let tones = 0, vib = 0;
    const RealAC = window.AudioContext;
    window.AudioContext = function () { const ac = new RealAC(); const mk = ac.createOscillator.bind(ac); ac.createOscillator = () => { tones++; return mk(); }; return ac; };
    AC = null; navigator.vibrate = () => { vib++; return true; };
    const key = k => document.body.dispatchEvent(new KeyboardEvent('keydown', { key: k, bubbles: true }));
    openGame('A1:1'); const w = G.words.find(x => !wordSolved(x));
    const open = w.cells.filter(([r, c]) => !locked(r, c));
    open.forEach(([r, c], i) => { G.cur = G.cells[r][c]; G.dir = w.dir; tones = 0; vib = 0; key(G.cells[r][c].sol === 'Q' ? 'Z' : 'Q'); });
    R.push('last letter of a wrong word: tones=' + tones + ' vib=' + vib + ' shaking=' + w.cells.filter(([r, c]) => G.cells[r][c].el.classList.contains('shake')).length + '/' + w.cells.length + ' badMarks=' + Object.values(G.marks).filter(m => m === 'bad').length + ' redWord=' + w.cells.filter(([r, c]) => G.cells[r][c].el.classList.contains('wword')).length + ' afterFix=' + (() => { const [r, c] = open[0]; G.cur = G.cells[r][c]; key('Backspace'); return w.cells.filter(([r, c]) => G.cells[r][c].el.classList.contains('wword')).length; })());
  } catch (e) { R.push('ERR ' + e.message); }
  const p = document.getElementById('OUT'); p.textContent += '\n' + R.join('\n');
}, 900);
