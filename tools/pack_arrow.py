"""Builds every puzzle as a classic arrowword into data/arrow.json (run from the repo root).

Levels A1-C2: 12 puzzles each. IELTS: 2 puzzles for every topic x band (36).
Each puzzle prefers its own level's words (see LEVELS below); everyday words fill the rest.
Sets are built in parallel, one process per set.
"""
import json, os, random, sys
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import arrowgen, dictionary

D = dictionary.load()
EASY = D['two'] + D['three'] + D['f4'] + D['f5'] + D['wotd']

def uniq(xs):
    out, seen = [], set()
    for w, c in xs:
        if w not in seen and 2 <= len(w) <= 8:
            seen.add(w); out.append((w, c))
    return out

# level -> (level words, share of level words to aim for, reserve long slots for level words?)
LEVELS = {
    'A1': (D['two'] + D['three_common'] + D['f4'], 0.75, False),
    'A2': (D['three'] + D['f4'] + D['f5'], 0.8, False),
    'B1': (D['f5'] + [x for x in D['wotd'] if 4 <= len(x[0]) <= 8], 0.6, True),
    'B2': ([x for x in D['wotd'] if len(x[0]) >= 5] + D['c1'][:60], 0.45, True),
    'C1': (D['c1'], 0.3, True),
    'C2': (D['c2'], 0.3, True),
}

def one(level_words, fill, rng, want, use, reserve, secondary=frozenset()):
    # long slots (6+, then 7+) reserved for the level's words; if that does not fill in time,
    # the best ordinary fill
    if reserve:
        for strict, budget in ((6, 45), (7, 20)):
            p = arrowgen.make(level_words, fill, rng, want=0.99, budget=budget, use=use, strict=strict, min_long=3, secondary=secondary)
            if p:
                return p
    p = None
    while p is None:
        p = arrowgen.make(level_words, fill, rng, want=want, budget=25, use=use, secondary=secondary)
    return p


def build_set(job):
    key, level_words, want, n, seed, reserve = job[:6]
    secondary = frozenset(job[6]) if len(job) > 6 else frozenset()
    rng = random.Random(seed)
    level_words = uniq(level_words)
    fill = uniq(EASY)
    use, out = {}, []
    for i in range(n):
        p = one(level_words, fill, rng, want, use, reserve, secondary)
        arrowgen.check(p)
        for w in p['words']:
            use[w['answer']] = use.get(w['answer'], 0) + 1
        out.append(p)
        lw = {w for w, _ in level_words}
        print(key, i + 1, len(p['words']), 'words,', sum(w['answer'] in lw for w in p['words']), 'level words', file=sys.stderr, flush=True)
    return key, out

if __name__ == '__main__':
    jobs = [(k, lw, want, 12, 100 + i, res) for i, (k, (lw, want, res)) in enumerate(LEVELS.items())]
    TOPICS = ['egitim', 'cevre', 'saglik', 'teknoloji', 'is', 'toplum']
    BANDS = ['5-6', '6-7', '7+']
    for t in TOPICS:
        for b in BANDS:
            own = [(w, c) for w, c, tt, bb in D['ielts'] if tt == t and bb == b]
            rest = [(w, c) for w, c, tt, bb in D['ielts'] if tt == t and bb != b]
            same_band = [(w, c) for w, c, tt, bb in D['ielts'] if tt != t and bb == b]
            # the topic's words first; same-band words of other topics only help fill long slots
            jobs.append((f'IELTS|{t}|{b}', own + rest + same_band, 0.3, 2, (TOPICS.index(t) * 7 + BANDS.index(b)) * 31 + 7, True, [w for w, _ in same_band]))
    with Pool(min(10, os.cpu_count() or 4)) as pool:
        results = dict(pool.map(build_set, jobs))
    data = {k: results[k] for k in LEVELS}
    data['IELTS'] = []
    for t in TOPICS:
        for b in BANDS:
            for p in results[f'IELTS|{t}|{b}']:
                p['topic'], p['band'] = t, b
                data['IELTS'].append(p)
    json.dump(data, open('data/arrow.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print('done', {k: len(v) for k, v in data.items()}, file=sys.stderr)
