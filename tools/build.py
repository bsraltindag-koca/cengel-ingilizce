"""Builds index.html from src/app.html + data/data.json (run from the repo root)."""
import json
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
body = open('src/app.html', encoding='utf-8').read().replace('/*DATA*/{}', json.dumps(d, ensure_ascii=False, separators=(',', ':')))
head = '<!doctype html>\n<html lang="tr">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<meta name="theme-color" content="#4b3be0">\n<meta name="apple-mobile-web-app-capable" content="yes">\n<meta name="mobile-web-app-capable" content="yes">\n<meta name="apple-mobile-web-app-title" content="Kanca">\n<meta name="apple-mobile-web-app-status-bar-style" content="default">\n<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">\n<link rel="icon" type="image/png" sizes="32x32" href="icons/favicon-32.png">\n<link rel="manifest" href="manifest.webmanifest">\n<style>body{margin:0;font-size:14px}</style>\n'
title_end = body.index('</style>') + len('</style>')
html = head + body[:title_end] + '\n</head>\n<body>\n' + body[title_end:] + '\n</body>\n</html>\n'
open('index.html', 'w', encoding='utf-8').write(html)
print('index.html built')
