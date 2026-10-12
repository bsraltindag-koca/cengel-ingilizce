"""Classic arrowword (çengel bulmaca) generator.

A 9x9 board: the top row and the left column are clue squares, more clue squares sit inside,
and every other square holds a letter. Every run of 2+ letters, across or down, is a word,
and its clue sits in the square just before it (left of an across word, above a down word).
Most letters belong to two words, like a printed çengel bulmaca.

Two steps:
  1. template(): place the inner clue squares with a few rules (every clue square clues
     something, every letter is in a word, word lengths 2-8, few 2-letter words, few letters
     that sit in only one word).
  2. fill(): a constraint solver fills the runs from the dictionary, always trying the
     level's own words first, so the puzzle is mostly made of that level's vocabulary.

    from arrowgen import make
    p = make(level_words, filler_words, rng)   # lists of (WORD, clue)
    # -> {'R': 9, 'C': 9, 'words': [{'dir', 'r', 'c', 'answer', 'clue'}, ...]}
"""
import random
import time

R = C = 9


def runs(black):
    """(dir, r, c, length) for every run of 2+ letter squares."""
    out = []
    for r in range(R):
        c = 0
        while c < C:
            if not black[r][c]:
                s = c
                while c < C and not black[r][c]:
                    c += 1
                if c - s >= 2:
                    out.append(('A', r, s, c - s))
            else:
                c += 1
    for c in range(C):
        r = 0
        while r < R:
            if not black[r][c]:
                s = r
                while r < R and not black[r][c]:
                    r += 1
                if r - s >= 2:
                    out.append(('D', s, c, r - s))
            else:
                r += 1
    return out


def cells(slot):
    d, r, c, n = slot
    return [(r, c + k) if d == 'A' else (r + k, c) for k in range(n)]


def template(rng, max_two=6, max_single=10):
    """Random inner clue squares that pass the rules, or None."""
    black = [[r == 0 or c == 0 for c in range(C)] for r in range(R)]
    cols = list(range(1, C))
    rng.shuffle(cols)
    for r in range(1, R):
        # one or two inner clue squares per row, spread over the columns
        black[r][cols[(r - 1) % len(cols)]] = True
        if rng.random() < 0.55:
            black[r][rng.randint(2, C - 1)] = True
    # keep the bottom-right corner a letter more often than not; it reads better
    sl = runs(black)
    # every inner clue square must clue something (word to its right or below)
    starts = {(r, c - 1) for d, r, c, n in sl if d == 'A'} | {(r - 1, c) for d, r, c, n in sl if d == 'D'}
    for r in range(1, R):
        for c in range(1, C):
            if black[r][c] and (r, c) not in starts:
                return None
    cover = {}
    for s in sl:
        if s[3] > 8:
            return None
        for x in cells(s):
            cover[x] = cover.get(x, 0) + 1
    letters = [(r, c) for r in range(R) for c in range(C) if not black[r][c]]
    if any(x not in cover for x in letters):
        return None
    if sum(1 for s in sl if s[3] == 2) > max_two:
        return None
    if sum(1 for x in letters if cover[x] == 1) > max_single:
        return None
    return black, sl


def fill(sl, by_len, index, rank, rng, deadline, strict=99, level=frozenset()):
    """Fill every slot; candidates are tried in rank order (level words first).
    Slots of length >= strict may only take level words."""
    letter = {}
    used = set()
    chosen = [None] * len(sl)
    cs = [cells(s) for s in sl]

    def cands(i):
        n = sl[i][3]
        pool = by_len.get(n)
        if not pool:
            return []
        res = None
        for k, x in enumerate(cs[i]):
            ch = letter.get(x)
            if ch:
                s = index.get((n, k, ch))
                if not s:
                    return []
                res = s if res is None else res & s
                if not res:
                    return []
        if res is None:
            res = pool
        if n >= strict:
            return [w for w in res if w in level and w not in used]
        return [w for w in res if w not in used]

    def rec():
        if time.time() > deadline:
            return False
        best, bc = None, None
        for i in range(len(sl)):
            if chosen[i] is None:
                c = cands(i)
                if not c:
                    return False
                if best is None or len(c) < len(bc):
                    best, bc = i, c
                    if len(c) == 1:
                        break
        if best is None:
            return True
        bc.sort(key=lambda w: rank[w] + rng.random() * 0.5)
        for w in bc[:12]:
            old = [letter.get(x) for x in cs[best]]
            for x, ch in zip(cs[best], w):
                letter[x] = ch
            chosen[best] = w
            used.add(w)
            if rec():
                return True
            used.discard(w)
            chosen[best] = None
            for x, o in zip(cs[best], old):
                if o is None:
                    del letter[x]
        return False

    return chosen if rec() else None


def make(level_words, filler_words, rng, want=0.5, budget=40.0, per_try=1.2, use=None, strict=99, min_long=0, secondary=frozenset()):
    """Build one puzzle. level_words come first in every choice; filler_words make the
    grid fillable. Returns the best of the fills found within the budget (by share of
    level words), or None."""
    use = use or {}
    clue = {}
    rank = {}
    for w, c in filler_words:
        clue.setdefault(w, c)
        rank[w] = 2.0 + use.get(w, 0) * 0.3
    for w, c in level_words:
        clue[w] = c
        rank[w] = (0.8 if w in secondary else 0.0) + use.get(w, 0) * 0.6
    by_len, index = {}, {}
    for w in clue:
        by_len.setdefault(len(w), set()).add(w)
        for k, ch in enumerate(w):
            index.setdefault((len(w), k, ch), set()).add(w)
    level = frozenset(w for w, _ in level_words)
    start = time.time()
    best = None
    while time.time() - start < budget:
        t = template(rng)
        if not t:
            continue
        black, sl = t
        if min_long and sum(1 for s in sl if s[3] >= strict) < min_long:
            continue
        chosen = fill(sl, by_len, index, rank, rng, time.time() + per_try, strict, level)
        if not chosen:
            continue
        share = sum(w in level for w in chosen) / len(chosen)
        score = share + rng.random() * 0.01
        if best is None or score > best[0]:
            best = (score, sl, chosen)
        if share >= want:
            break
    if not best:
        return None
    _, sl, chosen = best
    words = [{'dir': d, 'r': r, 'c': c, 'answer': w, 'clue': clue[w]} for (d, r, c, n), w in zip(sl, chosen)]
    return {'R': R, 'C': C, 'words': words, 'share': round(best[0], 2)}


def check(p):
    """Independent check: letters agree where words cross, every letter run is a word, each
    word has its clue square right before it, and no word repeats."""
    grid = {}
    for w in p['words']:
        for (r, c), ch in zip(cells((w['dir'], w['r'], w['c'], len(w['answer']))), w['answer']):
            assert grid.get((r, c), ch) == ch, ('letters clash', w)
            grid[(r, c)] = ch
    black = [[(r, c) not in grid for c in range(C)] for r in range(R)]
    got = sorted((d, r, c, n) for d, r, c, n in runs(black))
    want = sorted((w['dir'], w['r'], w['c'], len(w['answer'])) for w in p['words'])
    assert got == want, 'a letter run is not a word'
    for w in p['words']:
        cr, cc = (w['r'], w['c'] - 1) if w['dir'] == 'A' else (w['r'] - 1, w['c'])
        assert black[cr][cc], ('clue square missing', w)
    assert len({w['answer'] for w in p['words']}) == len(p['words']), 'repeated word'
    return True
