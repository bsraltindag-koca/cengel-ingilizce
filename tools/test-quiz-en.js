// Tekrar et: after an answer the English of the example sentence appears, with the word in bold
setTimeout(() => {
  const R = [];
  try {
    const ws = ['ABOLISH', 'ACCEPT', 'TICKET', 'WIN', 'BITE'].filter(w => DATA.hints[w]);
    S.learned = {}; ws.forEach(w => S.learned[w] = { at: dayKey(), lv: 'A1', hard: false, miss: 0 });
    startQuiz(ws);
    const before = $('qExEn').hidden;
    let shown = 0, bold = 0;
    for (let i = 0; i < Q.items.length; i++) {
      Q.i = i; renderQuiz();
      if (!$('qExEn').hidden) R.push('visible before answering: ' + Q.items[i].w);
      answer(Q.items[i].w);
      if (!$('qExEn').hidden && $('qExEn').textContent === DATA.hints[Q.items[i].w][3].replace(/\[\[|\]\]/g, '')) shown++;
      if ($('qExEn').querySelector('b')) bold++;
      R.push(Q.items[i].w + ': ' + $('qExEn').innerHTML);
    }
    R.unshift('hidden before=' + before + ' shown after=' + shown + '/' + Q.items.length + ' bold=' + bold + ' withEnglish=' + Object.values(DATA.hints).filter(h => h[3]).length + '/' + Object.keys(DATA.hints).length);
  } catch (e) { R.push('ERR ' + e.message); }
  const p = document.createElement('pre'); p.id = 'OUT'; p.textContent = R.join('\n'); document.body.appendChild(p);
}, 300);
