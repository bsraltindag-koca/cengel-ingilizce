// mute button on the review screen: stops the spoken word after a right answer and is remembered
setTimeout(() => {
  const R = [];
  try {
    localStorage.clear();
    S.learned = { CAT: { at: '2026-10-01', lv: 'A1', hard: false, miss: 0 }, DOG: { at: '2026-10-01', lv: 'A1', hard: false, miss: 0 }, EGG: { at: '2026-10-01', lv: 'A1', hard: false, miss: 0 }, TEA: { at: '2026-10-01', lv: 'A1', hard: false, miss: 0 }, BUS: { at: '2026-10-01', lv: 'A1', hard: false, miss: 0 } };
    S.review = {}; S.opts.quizMute = false;
    let spoken = 0; const orig = window.speak; window.speak = (...x) => { spoken++; };
    show('words'); startQuiz();
    R.push('button visible=' + !$('qMute').hidden + ' pressed=' + $('qMute').getAttribute('aria-pressed'));
    answer(Q.items[0].w); R.push('right answer, sound on -> spoken=' + spoken);
    $('qMute').click(); R.push('after tap: pressed=' + $('qMute').getAttribute('aria-pressed') + ' label=' + $('qMute').getAttribute('aria-label') + ' saved=' + JSON.parse(localStorage.getItem('cengel-app-v2')).opts.quizMute);
    nextQuestion(); answer(Q.items[1].w); R.push('right answer, muted -> spoken=' + spoken);
    startQuiz(); R.push('new quiz still muted=' + $('qMute').getAttribute('aria-pressed'));
    $('qMute').click(); answer(Q.items[0].w); R.push('unmuted again -> spoken=' + spoken);
    window.speak = orig;
  } catch (e) { R.push('ERR ' + e.message); }
  const p = document.createElement('pre'); p.id = 'OUT'; p.textContent = R.join('\n'); document.body.appendChild(p);
}, 300);
