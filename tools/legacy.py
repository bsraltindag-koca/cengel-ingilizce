"""Fallbacks for older web engines (Chrome / Android WebView 88-110, e.g. Android 9 phones).

The page is written with color-mix(), container-query units (cqw) and dvh. Engines before
Chrome 111 / 105 / 108 drop such declarations, which leaves backgrounds empty and text sizes
wrong. For every declaration that uses one of them, this inserts a plain declaration of the
same property just before it:

  color-mix(in srgb, A p%, B)  ->  the mixed colour, computed here from the theme tokens
  Ncqw                         ->  an approximation from the screen width (a grid cell is
                                    about 1/9.5 of a phone's width)
  dvh                          ->  vh

cqw and dvh fallbacks without var() simply go first: an old engine drops the original as invalid and keeps
the fallback. color-mix(), and anything holding var(), needs more care: an old engine cannot reject it
while parsing, so it would win the cascade and then compute to nothing. Those declarations are
replaced by the fallback and repeated right after their rule inside
@supports (color: color-mix(...)) { ... }, which old engines skip and modern ones apply, in the
same cascade position. Mixes that differ between light and dark get a --legacy-N token in each
theme block.
"""
import re

# feature -> the @supports test that guards declarations using it
SUPPORTS = {
    'color-mix': '(color: color-mix(in srgb, red 50%, blue))',
    'cqw': '(width: 1cqw)',
    'dvh': '(height: 1dvh)',
}
TOKEN = re.compile(r'(--[\w-]+)\s*:\s*([^;]+);')
MIX = re.compile(r'color-mix\(\s*in srgb\s*,\s*([^,()]+(?:\([^()]*\))?)\s+([\d.]+)%\s*,\s*([^()]+?(?:\([^()]*\))?)\s*\)')


def parse_color(v):
    v = v.strip()
    if v == 'transparent':
        return (0, 0, 0, 0.0)
    m = re.fullmatch(r'#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})', v)
    if m:
        h = m.group(1)
        if len(h) == 3:
            h = ''.join(c * 2 for c in h)
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 1.0)
    m = re.fullmatch(r'rgba?\(([^)]*)\)', v)
    if m:
        parts = [p.strip() for p in m.group(1).replace('/', ',').split(',')]
        r, g, b = (float(x) for x in parts[:3])
        a = float(parts[3]) if len(parts) > 3 else 1.0
        return (r, g, b, a)
    return None


def fmt(c):
    r, g, b, a = c
    if a >= 0.999:
        return '#%02x%02x%02x' % (round(r), round(g), round(b))
    return 'rgba(%d, %d, %d, %.3f)' % (round(r), round(g), round(b), a)


def mix(a, p, b):
    # srgb interpolation with premultiplied alpha, as color-mix() does
    pa, pb = p, 1 - p
    alpha = a[3] * pa + b[3] * pb
    if alpha == 0:
        return (0, 0, 0, 0.0)
    ch = [(a[i] * a[3] * pa + b[i] * b[3] * pb) / alpha for i in range(3)]
    return (ch[0], ch[1], ch[2], alpha)


def resolve(expr, tokens, depth=0):
    expr = expr.strip()
    m = re.fullmatch(r'var\((--[\w-]+)\)', expr)
    if m:
        v = tokens.get(m.group(1))
        return resolve(v, tokens, depth + 1) if v is not None and depth < 5 else None
    return parse_color(expr)


def block_tokens(css, opener):
    i = css.find(opener)
    if i < 0:
        return {}
    j = css.index('}', i)
    return dict(TOKEN.findall(css[i:j]))


def add_fallbacks(css):
    light = block_tokens(css, ':root {')
    dark = dict(light, **block_tokens(css, ':root[data-theme="dark"] {'))
    wotd = dict(light, **block_tokens(css, '.wotd {'))
    new_tokens = []  # (name, light, dark)

    def mix_fallback(value, scoped):
        def one(m):
            a, p, b = m.group(1), float(m.group(2)) / 100, m.group(3)
            maps = [wotd] if scoped else [light, dark]
            vals = []
            for t in maps:
                ca, cb = resolve(a, t), resolve(b, t)
                if ca is None or cb is None:
                    return b.strip() if b.strip() != 'transparent' else a.strip()
                vals.append(fmt(mix(ca, p, cb)))
            if len(set(vals)) == 1:
                return vals[0]
            name = '--legacy-%d' % (len(new_tokens) + 1)
            new_tokens.append((name, vals[0], vals[1]))
            return 'var(%s)' % name
        return MIX.sub(one, value)

    def fix_rule(m):
        selector, body = m.group(1), m.group(2)
        if not re.search(r'color-mix|cqw|dvh', body):
            return m.group(0)
        scoped = '.wotd' in selector
        out, modern, needs = [], [], set()
        for decl in re.split(r'(?<=;)', body):
            d = decl.strip()
            pm = re.match(r'([a-z-]+)\s*:\s*(.+?);?$', d, re.S)
            if pm and not d.startswith('--') and re.search(r'color-mix|cqw|dvh', d):
                prop, value = pm.group(1), pm.group(2)
                fb = value
                if 'color-mix' in fb:
                    fb = mix_fallback(fb, scoped)
                fb = re.sub(r'(\d*\.?\d+)cqw', lambda x: 'calc(%s * 0.105vw)' % x.group(1), fb)
                fb = fb.replace('dvh', 'vh')
                # color-mix always, and anything that also holds var(): an old engine would accept
                # it while parsing and then compute it to nothing, so it moves into @supports
                if 'color-mix' not in fb and ('color-mix' in value or 'var(' in value):
                    out.append(' %s: %s;' % (prop, fb))   # the rule keeps only the fallback
                    modern.append(d if d.endswith(';') else d + ';')
                    for feat, test in SUPPORTS.items():
                        if feat in value:
                            needs.add(test)
                    continue
                if 'color-mix' not in fb:
                    out.append(' %s: %s;' % (prop, fb))
            out.append(decl)
        rule = selector + '{' + ''.join(out) + '}'
        if modern:
            rule += ' @supports %s { %s { %s } }' % (' and '.join(sorted(needs)), selector.strip(), ' '.join(modern))
        return rule

    css = re.sub(r'([^{}]+)\{([^{}]*)\}', fix_rule, css)
    if new_tokens:
        light_decl = ' '.join('%s: %s;' % (n, l) for n, l, _ in new_tokens)
        dark_decl = ' '.join('%s: %s;' % (n, d) for n, _, d in new_tokens)
        css = css.replace(':root {', ':root {\n  /* fallbacks for older engines, see tools/legacy.py */\n  ' + light_decl + '\n', 1)
        css = re.sub(r'(:root:not\(\[data-theme="light"\]\) \{)', r'\1 ' + dark_decl.replace('\\', '\\\\'), css, count=1)
        css = css.replace(':root[data-theme="dark"] {', ':root[data-theme="dark"] { ' + dark_decl, 1)
    return css


def apply(html):
    """Runs add_fallbacks on every <style> block of a page (and nothing else)."""
    return re.sub(r'(<style>)(.*?)(</style>)', lambda m: m.group(1) + add_fallbacks(m.group(2)) + m.group(3), html, flags=re.S)
