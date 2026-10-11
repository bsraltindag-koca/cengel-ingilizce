// the theme / streak / profile group shows on home, words, stats, settings and level pages
setTimeout(() => {
  const R = [];
  try {
    S.streak = { last: dayKey(), count: 5, best: 5 };
    for (const s of ['home', 'words', 'stats', 'settings']) { show(s); const g = $('s-' + s).querySelector('.right'); R.push(s + ': group=' + !!g + ' streak="' + (g && g.querySelector('.streakv').textContent) + '"'); }
    openLevel('A1'); const g = $('s-level').querySelector('.right'); R.push('level: group=' + !!g + ' streak="' + g.querySelector('.streakv').textContent + '"');
    const before = document.documentElement.classList.contains('is-dark');
    g.querySelector('[data-theme-toggle]').click();
    R.push('theme toggle on level page switched=' + (document.documentElement.classList.contains('is-dark') !== before));
    show('words'); $('s-words').querySelector('.avatar').click(); R.push('profile on words page -> ' + screen);
  } catch (e) { R.push('ERR ' + e.message); }
  const p = document.createElement('pre'); p.id = 'OUT'; p.textContent = R.join('\n'); document.body.appendChild(p);
}, 300);
