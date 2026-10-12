// Tekrar et: the question card shows the word's meaning note, and the note never holds the English answer
setTimeout(() => {
  const R = [];
  try {
    const ws = Object.keys(DATA.hints).slice(0, 6);
    S.learned = {}; ws.forEach(w => S.learned[w] = { at: dayKey(), lv: 'A1', hard: false, miss: 0 });
    startQuiz();
    let shown = 0, leaks = 0;
    for (let i = 0; i < Q.items.length; i++) {
      const it = Q.items[i];
      if (!$('qNote').hidden && $('qNote').querySelector('.ac').textContent === DATA.hints[it.w][1]) shown++;
      if (new RegExp('(^|[^\\wçğıöşü])' + it.w + '([^\\wçğıöşü]|$)', 'i').test($('qNote').textContent)) leaks++;
      answer(it.w); nextQuestion();
    }
    R.push('questions=' + Q.items.length + ' noteShown=' + shown + ' leaks=' + leaks);
  } catch (e) { R.push('ERR ' + e.message); }
  const p = document.createElement('pre'); p.id = 'OUT'; p.textContent = R.join('\n'); document.body.appendChild(p);
}, 300);
