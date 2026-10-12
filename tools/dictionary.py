"""All words with Turkish clues, grouped the way the puzzle levels use them."""
import os, re

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')


def tsv(name):
    p = os.path.join(BASE, 'data', name)
    if not os.path.exists(p):
        return []
    return [l.rstrip('\n').split('\t') for l in open(p, encoding='utf-8') if l.strip()]


def load():
    two = [(w, c) for w, c in tsv('vocab-2.tsv')] + [(w, c) for w, c in tsv('fill-2.tsv') if w != 'YE']
    src = open(os.path.join(BASE, 'tools', 'squares.py'), encoding='utf-8').read()
    three, seen = [], set()
    for part in re.search(r'A1 = """(.*?)"""', src, re.S).group(1).split('|'):
        w, c = part.split(':', 1)
        if c != '-' and len(w) == 3 and w not in seen:
            seen.add(w)
            three.append((w, c))
    three_common = three[:150]
    three += [(w, c) for w, c in tsv('fill-3.tsv') if w not in seen]
    wotd = [(r[0].upper(), r[3]) for r in tsv('words.tsv') if r[0].isalpha()]
    return {
        'two': two, 'three': three, 'three_common': three_common,
        'f4': [(w, c) for w, c in tsv('fill-4.tsv')], 'f5': [(w, c) for w, c in tsv('fill-5.tsv')],
        'wotd': wotd,
        'c1': [(w, c) for w, c in tsv('vocab-c1.tsv')], 'c2': [(w, c) for w, c in tsv('vocab-c2.tsv')],
        'ielts': [tuple(r) for r in tsv('vocab-ielts.tsv')],
    }
