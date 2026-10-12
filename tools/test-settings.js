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
