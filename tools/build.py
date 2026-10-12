"""Builds index.html from src/app.html + data/data.json (run from the repo root).

The version is 1.<number of the commit this build goes into>, plus the build time
in Turkey time, so the screen shows which update is live.
Optional argument: a path to also write the page without <head> (for the Claude artifact).
--www also writes www/ for the iOS / Android apps: the same page with the fonts bundled
(no internet needed) and only the files the app uses.
"""
import json, os, re, shutil, subprocess, sys
from datetime import datetime, timedelta, timezone
d = json.load(open('data/data.json', encoding='utf-8'))
# every 3x3 block must read as words across and down, all 24 words distinct, each with a clue
for k, ps in d['levels'].items():
    for p in ps:
        allw = []
        for s in p:
            ws = [s[0:3], s[3:6], s[6:9]] + [s[j] + s[3 + j] + s[6 + j] for j in range(3)]
            assert all(w in d['clues'] for w in ws), (k, s)
            allw += ws
        assert len(set(allw)) == 24, (k, p)
# all puzzles (classic arrowwords) from tools/pack_arrow.py, re-checked here
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import arrowgen, dictionary
long_data = json.load(open('data/arrow.json', encoding='utf-8'))
for _set in long_data.values():
    for _p in _set:
        arrowgen.check(_p)
        for _w in _p['words']:
            assert not dictionary.gives_away(_w['answer'], _w['clue']), ('clue gives the answer away', _w)
        _p.pop('share', None)
# Turkish clues for every dictionary word, so Tekrar et can still ask words learned from older puzzle sets
for _v in dictionary._load().values():
    for _x in _v:
        if 2 <= len(_x[0]) <= 8 and _x[0].isalpha():
            d['clues'].setdefault(_x[0], _x[1])
# which-meaning notes for clues: WORD<TAB>tür<TAB>açıklama<TAB>örnek in data/hints-*.tsv; all of them, since
# Tekrar et also asks words learned in earlier versions of the puzzles
import glob
_answers = {w['answer'] for _set in long_data.values() for _p in _set for w in _p['words']}
hints = {}
for _f in sorted(glob.glob('data/hints-*.tsv')):
    for _l in open(_f, encoding='utf-8'):
        _x = _l.rstrip('\n').split('\t')
        if len(_x) == 4:
            assert not re.search(r'(?<![\wçğıöşüÇĞİÖŞÜ])' + _x[0] + r'(?![\wçğıöşüÇĞİÖŞÜ])', _x[2] + ' ' + _x[3], re.I), ('hint gives the answer away', _x)
            hints[_x[0]] = _x[1:]
# words of the day: one per line, tab separated, 6 fields
words = [l.split('\t') for l in open('data/words.tsv', encoding='utf-8').read().strip().split('\n')]
assert all(len(w) == 6 and all(x.strip() for x in w) for w in words), 'words.tsv: every line needs 6 fields'
assert len({w[0] for w in words}) == len(words), 'words.tsv: duplicate word'
assert len(words) % 5 == 0, 'words.tsv: word count must be a multiple of 5'
n = int(subprocess.run(['git', 'rev-list', '--count', 'HEAD'], capture_output=True, text=True).stdout.strip() or 0) + 1
now = datetime.now(timezone(timedelta(hours=3)))
months = ['Oca', 'Şub', 'Mar', 'Nis', 'May', 'Haz', 'Tem', 'Ağu', 'Eyl', 'Eki', 'Kas', 'Ara']
version = {'n': f'1.{n}', 'date': f'{now.day} {months[now.month - 1]} {now.year}, {now:%H:%M}'}
body = (open('src/app.html', encoding='utf-8').read()
        .replace('/*DATA*/{}', json.dumps(d, ensure_ascii=False, separators=(',', ':')))
        .replace("/*VERSION*/{ n: 'geliştirme', date: '' }", json.dumps(version, ensure_ascii=False))
        .replace('/*WOTD*/[]', json.dumps(words, ensure_ascii=False, separators=(',', ':')))
        .replace('/*LONG*/{}', json.dumps(long_data, ensure_ascii=False, separators=(',', ':')))
        .replace('/*HINTS*/{}', json.dumps(hints, ensure_ascii=False, separators=(',', ':'))))
import legacy  # fallbacks for older engines (tools/legacy.py)
body = legacy.apply(body)
args = [x for x in sys.argv[1:] if not x.startswith('--')]
if args:
    open(args[0], 'w', encoding='utf-8').write(body)
head = '<!doctype html>\n<html lang="tr">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<meta name="theme-color" content="#4b3be0">\n<meta name="apple-mobile-web-app-capable" content="yes">\n<meta name="mobile-web-app-capable" content="yes">\n<meta name="apple-mobile-web-app-title" content="Kanca">\n<meta name="apple-mobile-web-app-status-bar-style" content="default">\n<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">\n<link rel="icon" type="image/png" sizes="32x32" href="icons/favicon-32.png">\n<link rel="manifest" href="manifest.webmanifest">\n<style>body{margin:0;font-size:14px}</style>\n'
title_end = body.index('</style>') + len('</style>')
html = head + body[:title_end] + '\n</head>\n<body>\n' + body[title_end:] + '\n</body>\n</html>\n'
open('index.html', 'w', encoding='utf-8').write(html)
print('index.html built, version', version['n'], version['date'])
if '--www' in sys.argv:
    fonts_link = re.search(r'<link rel="preconnect" href="https://fonts.googleapis.com">.*?display=swap">', html, re.S)
    assert fonts_link, 'Google Fonts links not found'
    app_html = html.replace(fonts_link.group(0), '<link rel="stylesheet" href="fonts/fonts.css">')
    shutil.rmtree('www', ignore_errors=True)
    os.makedirs('www')
    open('www/index.html', 'w', encoding='utf-8').write(app_html)
    shutil.copytree('fonts', 'www/fonts')
    shutil.copytree('icons', 'www/icons', ignore=shutil.ignore_patterns('logo-source.html'))
    print('www/ built for the apps:', ', '.join(sorted(os.listdir('www'))))
