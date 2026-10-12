"""Rebuilds puzzles in data/arrow.json that hold too few of their level's words (run after pack_arrow.py)."""
import json, os, random, sys
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import arrowgen, dictionary, pack_arrow as P

D = dictionary.load()
d = json.load(open('data/arrow.json', encoding='utf-8'))
level_sets = {'C1': P.uniq(D['c1']), 'C2': P.uniq(D['c2']), 'B1': None, 'B2': None}

def pool_for(key, p):
    if key == 'IELTS':
        t, b = p['topic'], p['band']
        own = [(w, c) for w, c, tt, bb in D['ielts'] if tt == t]
        other = [(w, c) for w, c, tt, bb in D['ielts'] if tt != t and bb == b]
        return P.uniq(own + other), frozenset(w for w, _ in other), {w for w, _ in P.uniq(own + other)}
    lw = P.uniq(P.LEVELS[key][0])
    return lw, frozenset(), {w for w, _ in lw}

def rebuild(job):
    key, i, seed = job
    p = d[key][i]
    lw, sec, lset = pool_for(key, p)
    rng = random.Random(seed)
    fill = P.uniq(P.EASY)
    best = None
    for strict, budget in ((6, 90), (5, 60), (7, 40)):
        q = arrowgen.make(lw, fill, rng, want=0.99, budget=budget, strict=strict, min_long=3, secondary=sec)
        if q:
            n = sum(w['answer'] in lset for w in q['words'])
            if best is None or n > best[0]:
                best = (n, q)
            if n >= 4:
                break
    return key, i, best

if __name__ == '__main__':
    jobs = []
    for key in ('C1', 'C2', 'IELTS'):
        for i, p in enumerate(d[key]):
            _, _, lset = pool_for(key, p)
            if sum(w['answer'] in lset for w in p['words']) < 3:
                jobs.append((key, i, 500 + len(jobs)))
    print('weak puzzles:', len(jobs), file=sys.stderr)
    with Pool(8) as pool:
        for key, i, best in pool.map(rebuild, jobs):
            old = d[key][i]
            _, _, lset = pool_for(key, old)
            had = sum(w['answer'] in lset for w in old['words'])
            if best and best[0] > had:
                arrowgen.check(best[1])
                for k in ('topic', 'band'):
                    if k in old:
                        best[1][k] = old[k]
                d[key][i] = best[1]
                print(key, i, had, '->', best[0], file=sys.stderr)
            else:
                print(key, i, 'kept', had, file=sys.stderr)
    json.dump(d, open('data/arrow.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
