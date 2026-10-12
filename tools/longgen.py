"""Arrowword generator for long words (C1, C2, IELTS).

The A1-B2 puzzles are four 3x3 word squares. Advanced words are 4-8 letters long, so these
puzzles are built differently: words are placed one by one on a 9x9 grid, each crossing a
word already there, each with a free clue square right before its first letter (left of an
across word, above a down word). After every placement all runs of 2+ letters in the grid
are checked: each must be exactly one placed word, so no accidental letter strings appear.
Squares that end up unused stay blank. A clue square may carry one across and one down clue.

    from longgen import generate
    puzzle = generate(pool, rng)   # pool: [(WORD, clue), ...]
    # -> {'R': 9, 'C': 9, 'words': [{'dir': 'A'|'D', 'r', 'c', 'answer', 'clue'}, ...]}
"""
import random

R = C = 9


def cells_of(w, r, c, d):
    return [(r, c + k) if d == 'A' else (r + k, c) for k in range(len(w))]


def clue_pos(r, c, d):
    return (r, c - 1) if d == 'A' else (r - 1, c)


class Board:
    def __init__(self):
        self.letter = {}      # (r, c) -> char
        self.clue = {}        # (r, c) -> set of dirs whose clue sits here
        self.words = []       # (word, r, c, d)

    def runs_ok(self):
        """Every maximal run of 2+ letters, in both directions, is exactly one placed word."""
        starts = {(r, c, d): len(w) for w, r, c, d in self.words}
        for d in 'AD':
            for line in range(R if d == 'A' else C):
                k = 0
                while k < (C if d == 'A' else R):
                    pos = (line, k) if d == 'A' else (k, line)
                    if pos in self.letter:
                        s = k
                        while k < (C if d == 'A' else R) and (((line, k) if d == 'A' else (k, line)) in self.letter):
                            k += 1
                        n = k - s
                        if n >= 2:
                            r, c = (line, s) if d == 'A' else (s, line)
                            if starts.get((r, c, d)) != n:
                                return False
                    else:
                        k += 1
        return True

    def try_place(self, w, r, c, d, need_cross):
        cs = cells_of(w, r, c, d)
        if any(not (0 <= rr < R and 0 <= cc < C) for rr, cc in cs):
            return None
        cp = clue_pos(r, c, d)
        if not (0 <= cp[0] < R and 0 <= cp[1] < C):
            return None
        if cp in self.letter or d in self.clue.get(cp, ()):
            return None
        crosses = 0
        for (rr, cc), ch in zip(cs, w):
            if (rr, cc) in self.clue:
                return None
            have = self.letter.get((rr, cc))
            if have is not None:
                if have != ch:
                    return None
                crosses += 1
        if need_cross and crosses == 0:
            return None
        if crosses == len(w):
            return None
        added = [(p, ch) for p, ch in zip(cs, w) if p not in self.letter]
        for p, ch in added:
            self.letter[p] = ch
        self.clue.setdefault(cp, set()).add(d)
        self.words.append((w, r, c, d))
        if self.runs_ok():
            return crosses, added, cp
        self.undo(added, cp, d)
        return None

    def undo(self, added, cp, d):
        for p, _ in added:
            del self.letter[p]
        self.clue[cp].discard(d)
        if not self.clue[cp]:
            del self.clue[cp]
        self.words.pop()


def build_once(pool, rng, target, fillers=(), max_fill=4):
    """One greedy build. pool = the level's words (preferred), fillers = short easy words that
    may fill gaps (at most max_fill of them)."""
    b = Board()
    order = pool[:]
    rng.shuffle(order)
    first = max(order[:8], key=lambda x: len(x[0]))
    w = first[0]
    d = rng.choice('AD')
    if d == 'A':
        r, c = rng.randint(1, R - 2), rng.randint(1, C - len(w))
    else:
        r, c = rng.randint(1, R - len(w)), rng.randint(1, C - 2)
    if not b.try_place(w, r, c, d, False):
        return b, {}, 0
    clues = {w: first[1]}
    used = {w}
    n_fill = 0
    fill_list = list(fillers)
    while len(b.words) < target:
        best = None
        cands = [(x, False) for x in order if x[0] not in used]
        if n_fill < max_fill:
            rng.shuffle(fill_list)
            cands += [(x, True) for x in fill_list[:80] if x[0] not in used]
        letters = list(b.letter.items())
        for (word, clue), is_fill in cands:
            for (pr, pc), ch in letters:
                for k, wch in enumerate(word):
                    if wch != ch:
                        continue
                    for dd in 'AD':
                        rr, cc = (pr, pc - k) if dd == 'A' else (pr - k, pc)
                        res = b.try_place(word, rr, cc, dd, True)
                        if not res:
                            continue
                        crosses, added, cp = res
                        b.undo(added, cp, dd)
                        # level words first; crossings make the grid tight
                        score = crosses * 4 + len(word) + (0 if is_fill else 6) + rng.random() * 2
                        if best is None or score > best[0]:
                            best = (score, word, clue, rr, cc, dd, is_fill)
        if not best:
            break
        _, word, clue, rr, cc, dd, is_fill = best
        b.try_place(word, rr, cc, dd, True)
        used.add(word); clues[word] = clue
        n_fill += is_fill
    return b, clues, n_fill


def generate(pool, rng=None, tries=30, target=18, min_words=10, fillers=(), max_fill=4):
    """Best of several random builds: most level words, then most words, then most filled squares."""
    rng = rng or random.Random()
    best = None
    for _ in range(tries):
        b, clues, n_fill = build_once(pool, rng, target, fillers, max_fill)
        if len(b.words) < min_words:
            continue
        score = (len(b.words) - n_fill) * 12 + len(b.words) * 4 + len(b.letter)
        if best is None or score > best[0]:
            best = (score, b, clues)
    if not best:
        return None
    _, b, clues = best
    # normalise: reading order, across before down at the same square
    words = sorted(b.words, key=lambda x: (x[1], x[2], x[3]))
    return {'R': R, 'C': C, 'words': [{'dir': d, 'r': r, 'c': c, 'answer': w, 'clue': clues[w]} for w, r, c, d in words]}


def check(p):
    """Independent re-check of a finished puzzle (used by the build)."""
    grid = {}
    clue_dirs = {}
    for w in p['words']:
        for (r, c), ch in zip(cells_of(w['answer'], w['r'], w['c'], w['dir']), w['answer']):
            assert 0 <= r < R and 0 <= c < C, w
            assert grid.get((r, c), ch) == ch, ('letters clash', w)
            grid[(r, c)] = ch
        cp = clue_pos(w['r'], w['c'], w['dir'])
        assert 0 <= cp[0] < R and 0 <= cp[1] < C, ('clue off grid', w)
        assert w['dir'] not in clue_dirs.get(cp, set()), ('two clues same dir', w)
        clue_dirs.setdefault(cp, set()).add(w['dir'])
    for cp in clue_dirs:
        assert cp not in grid, ('clue square holds a letter', cp)
    b = Board()
    b.letter = grid
    b.words = [(w['answer'], w['r'], w['c'], w['dir']) for w in p['words']]
    assert b.runs_ok(), 'stray letter run'
    assert len({w['answer'] for w in p['words']}) == len(p['words']), 'repeated word'
    return True
