// IELTS hub: topic / band modes, group pages, back buttons, two-clue squares, next puzzle inside a group
setTimeout(() => {
  const R = [];
  try {
    localStorage.clear(); S.done = {}; S.games = {}; S.opts.ieltsMode = 'topic';
    show('home'); R.push('home card: ' + $('ieltsSub').textContent + ' | ' + $('ieltsCount').textContent + ' | levels=' + $('levels').children.length);
    $('ieltsGo').click(); R.push('hub screen=' + screen + ' cards=' + $('ieGrid').children.length + ' first=' + $('ieGrid').children[0].querySelector('b').textContent);
    $('ieMode').querySelector('[data-m=band]').click(); R.push('band mode cards=' + [...$('ieGrid').children].map(c => c.querySelector('b').textContent + ' ' + c.querySelector('.cnt').textContent).join(', '));
    $('ieGrid').children[2].click(); R.push('band 7+ page: ' + $('lvTitle').textContent + ' tiles=' + $('tiles').children.length + ' tag1=' + $('tiles').children[0].querySelector('.ttag').textContent);
    $('lvBack').click(); R.push('back -> ' + screen + ' mode kept=' + S.opts.ieltsMode);
    $('ieMode').querySelector('[data-m=topic]').click(); $('ieGrid').children[1].click();
    R.push('topic page: ' + $('lvTitle').textContent + ' tiles=' + $('tiles').children.length + ' bands=' + [...$('tiles').querySelectorAll('.ttag')].map(t => t.textContent).join('/'));
    $('tiles').children[0].click();
    R.push('game: ' + $('gTitle').textContent + ' | ' + $('gSub').textContent + ' | grid cols=' + G.C + ' two-clue squares=' + document.querySelectorAll('#grid .cell.clue.two').length);
    const two = document.querySelector('#grid .cell.clue.two .cp.D');
    if (two) { two.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })); R.push('tap down half -> dir=' + G.dir + ' active=' + two.classList.contains('active')); }
    const key = k => document.body.dispatchEvent(new KeyboardEvent('keydown', { key: k, bubbles: true }));
    window.confetti = () => {};
    for (const w of G.words) for (const [r, c] of w.cells) { if (locked(r, c)) continue; G.cur = G.cells[r][c]; G.dir = w.dir; key(G.cells[r][c].sol); }
    R.push('finished=' + G.finished + ' first=' + S.done[G.id].first + '/' + S.done[G.id].n);
    const before = G.id; renderDone(false); $('doneNext').click(); R.push('next in topic: ' + before + ' -> ' + G.id + ' (' + G.meta.title + ')');
    show('words'); R.push('learned long word clue: ' + Object.keys(S.learned).filter(w => w.length > 3).slice(0, 2).map(w => w.toLowerCase() + '=' + clue(w)).join(', '));
    show('stats'); R.push('stats levels=' + $('lvBars').children.length);
    S.done = {}; for (let i = 0; i < 6; i++) S.done['B2:' + i] = { score: 1, sec: 1, first: 1, hints: 0, n: 24 }; show('home');
    R.push('C1 unlocked after 6 in B2=' + !$('levels').children[4].classList.contains('locked') + ' C2 locked=' + $('levels').children[5].classList.contains('locked'));
  } catch (e) { R.push('ERR ' + e.message + ' @ ' + (e.stack || '').split('\n')[1]); }
  const p = document.createElement('pre'); p.id = 'OUT'; p.textContent = R.join('\n'); document.body.appendChild(p);
}, 300);
