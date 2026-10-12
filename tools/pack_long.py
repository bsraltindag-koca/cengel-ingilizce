"""Builds the long-word puzzles (C1, C2, IELTS) into data/long.json.

C1 / C2: 12 puzzles each from data/vocab-c1.tsv / vocab-c2.tsv.
IELTS:   for every topic x band, 2 puzzles from data/vocab-ielts.tsv. The band's own words
         come first; the topic's other words help fill when a band alone is too small.
Short 3-letter words from data/data.json may fill gaps (at most a few per puzzle).
Words used less so far are preferred, so the same word rarely repeats across a set.
Run from the repo root: python3 tools/pack_long.py
"""
import json, random, sys, os
from collections import Counter
sys.path.insert(0, os.path.dirname(__file__))
import longgen

def tsv(path):
    return [l.rstrip('\n').split('\t') for l in open(path, encoding='utf-8') if l.strip()]

fillers = list(json.load(open('data/data.json', encoding='utf-8'))['clues'].items())
rng = random.Random(2026)

def make_set(pool, n, label, extra=()):
    use = Counter(); out = []
    for i in range(n):
        fresh = sorted(pool, key=lambda x: (use[x[0]], rng.random()))[:max(28, len(pool) // 2)]
        p = None
        for attempt in range(4):
            p = longgen.generate(fresh + [x for x in extra if x[0] not in {f[0] for f in fresh}][:10], rng, tries=30, target=18, min_words=10, fillers=fillers, max_fill=6)
            if p: break
        assert p, (label, i)
        longgen.check(p)
        for w in p['words']: use[w['answer']] += 1
        out.append(p)
        print(label, i + 1, len(p['words']), 'words', file=sys.stderr, flush=True)
    return out

data = {}
for lv in ('C1', 'C2'):
    pool = [(w, c) for w, c in tsv(f'data/vocab-{lv.lower()}.tsv')]
    data[lv] = make_set(pool, 12, lv)

rows = tsv('data/vocab-ielts.tsv')
TOPICS = ['egitim', 'cevre', 'saglik', 'teknoloji', 'is', 'toplum']
BANDS = ['5-6', '6-7', '7+']
ielts = []
for t in TOPICS:
    for b in BANDS:
        own = [(w, c) for w, c, tt, bb in rows if tt == t and bb == b]
        rest = [(w, c) for w, c, tt, bb in rows if tt == t and bb != b]
        for p in make_set(own + rest[:12], 2, f'IELTS {t} {b}'):
            p['topic'], p['band'] = t, b
            ielts.append(p)
data['IELTS'] = ielts
json.dump(data, open('data/long.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('done', {k: len(v) for k, v in data.items()}, file=sys.stderr)
