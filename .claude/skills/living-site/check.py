#!/usr/bin/env python3
"""check.py <index.html> : the Living Site gate. Prints each test, then PASS or FAIL (exit 1).

Level 1  a Spline scene is on the page and the shield (or a shield div) keeps the scroll free
Level 2  a scroll film (MotionEngine.Scrub with frames on disk) or a Higgsfield video loop is on the page
Level 3  at least one code-drawn motion piece (data-xray-tool="code") driven by IntersectionObserver
Craft    reduced motion handled, no raw scroll listeners, no hint/pill overlays on 3D, no dashes in copy,
         every local asset exists, real logos only (no placeholder boxes), fictional brands say so,
         Arabic pages never use negative letter-spacing (it breaks letter joining), utf-8 charset declared

KOSIF options:
  --levels 3 | 2,3 | 1,2,3   gate a partial build honestly: skipped levels print "skip", never "ok"
  --levels code,3d,film|all  the same levels by name (USIP v6.0): code = 3, 3d = 1, film = 2
  --json                     machine-readable result (for receipts and CI)
  --strict                   warnings fail too
Warn (USIP v6.0, never fail without --strict): viewport meta, <html lang>, dir="rtl" for Arabic, alt on <img>.
Static checks only: no JavaScript runs, so a real browser pass (phone, desktop, console) is still due.
"""
import html
import json
import os
import re
import sys

USAGE = "usage: python3 check.py page.html [--levels 3|2,3|1,2,3|code,3d,film|all] [--json] [--strict]"
LEVEL_ALIASES = {'1': 1, '2': 2, '3': 3, '3d': 1, 'film': 2, 'code': 3}


def parse_levels(spec):
    out = []
    for part in spec.replace(' ', ',').split(','):
        part = part.strip().lower()
        if not part:
            continue
        if part == 'all':
            out += [1, 2, 3]
        elif part in LEVEL_ALIASES:
            out.append(LEVEL_ALIASES[part])
        else:
            raise ValueError(part)
    if not out:
        raise ValueError('empty')
    return tuple(sorted(set(out)))
ARABIC = re.compile(r'[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]')


def visible_text(src):
    s = re.sub(r'(?is)<(script|style|svg|noscript|template)[^>]*>.*?</\1>', ' ', src)
    s = re.sub(r'(?s)<!--.*?-->', ' ', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    return html.unescape(re.sub(r'\s+', ' ', s))


def tags_with(src, attr):
    """Every opening tag that carries attr, whatever the attribute order."""
    return re.findall(r'<[a-zA-Z][^<>]*\b' + re.escape(attr) + r'=["\'][^<>]*>', src)


def attr(tag, name):
    m = re.search(r'\b' + re.escape(name) + r'=(["\'])(.*?)\1', tag, re.S)
    return m.group(2) if m else None


def is_arabic_page(src, text):
    if re.search(r'<html[^>]*\b(dir=["\']rtl|lang=["\']ar)', src, re.I):
        return True
    letters = re.findall(r'[^\W\d_]', text)
    return bool(letters) and len(ARABIC.findall(text)) / len(letters) > 0.3


def run(path, levels=(1, 2, 3), strict=False):
    src = open(path, encoding='utf-8').read()
    root = os.path.dirname(os.path.abspath(path))
    text = visible_text(src)
    res = []

    def test(name, ok, note=''):
        res.append((bool(ok), name, note))

    # Level 1
    spline = re.findall(r'(?:src|data-src)=["\'](https://(?:my|app|prod)\.spline\.design/[^"\']+)["\']', src)
    scenes = len(set(spline))
    test('L1 live 3D on the page', spline, f'{scenes} Spline scene(s)')
    shield = 'spline-shield.js' in src or re.search(r'class=["\'][^"\']*shield', src) is not None
    test('L1 scroll never trapped (shield present)', not spline or shield)
    pills = r'(?i)(move your cursor|click to play|click to explore|drag to rotate|حرك المؤشر|حرّك المؤشر|اضغط للتشغيل|اسحب للتدوير)'
    test('L1 no hint pills over 3D', not re.search(pills, text) and not re.search(pills, src if spline else ''))
    test('L1 at most two 3D showpieces', scenes <= 2, 'more than two scenes reads as "going crazy"' if scenes > 2 else '')

    # Level 2
    scrub = 'MotionEngine.Scrub' in src
    m = re.search(r'count:\s*(\d+)', src)
    count = int(m.group(1)) if m else 0
    fm = re.search(r"`([\w/.-]*?)\$\{String\(i \+ 1\)\.padStart\((\d)", src)
    frames_ok, frames_note = True, f'count {count}'
    if scrub and fm and count:
        pre, pad = fm.group(1), int(fm.group(2))
        tail = re.search(r"padStart\(\d, '0'\)\}([\w.]+)`", src)
        ext = tail.group(1) if tail else '.jpg'
        missing = [i for i in (1, count) if not os.path.exists(os.path.join(root, f'{pre}{str(i).zfill(pad)}{ext}'))]
        frames_ok = not missing
        if missing:
            frames_note += f', missing frame(s) {missing}'
    elif scrub:
        frames_ok, frames_note = False, 'Scrub found but no frame pattern/count to verify'
    loops = re.findall(r'<video[^>]+src=["\']([^"\']+)["\']', src)
    test('L2 Higgsfield film or living loop', scrub or loops, f'scrub={scrub} loops={len(loops)}')
    test('L2 film frames on disk', frames_ok, frames_note)
    test('L2 film blends frames (smooth slow scroll)', not scrub or re.search(r'blend:\s*true', src))
    hf_tags = [t for t in tags_with(src, 'data-xray-tool') if attr(t, 'data-xray-tool') == 'higgsfield']
    test('L2 tagged as Higgsfield in X-ray', not (scrub or loops) or hf_tags)
    no_cost = [attr(t, 'data-xray') or '?' for t in hf_tags if attr(t, 'data-xray-cost') is None]
    test('L2 every generated piece shows its cost (data-xray-cost)', not no_cost, ', '.join(no_cost[:3]))

    # Level 3
    code_tags = [t for t in tags_with(src, 'data-xray-tool') if attr(t, 'data-xray-tool') == 'code'
                 and not (attr(t, 'data-xray') or '').lower().startswith('spline')]
    test('L3 at least one living code motion piece', code_tags, f'{len(code_tags)} tagged piece(s)')
    test('L3 driven by IntersectionObserver', 'IntersectionObserver' in src)

    # Craft
    test('reduced motion or Off switch handled',
         'prefers-reduced-motion' in src or 'data-motion' in src or 'motion-switch.js' in src)
    raw = [mm.start() for mm in re.finditer(r"""addEventListener\(\s*['"]scroll['"]""", src)]
    bad = [p for p in raw if 'requestAnimationFrame' not in src[p:p + 260] and 'passive' not in src[p:p + 260]]
    test('no raw scroll listeners (rAF-throttled or passive only)', not bad)
    dashes = re.findall(r'.{0,30}[—–].{0,30}', text)
    test('no em or en dashes in visible copy', not dashes, dashes[0] if dashes else '')
    assets = set(re.findall(r'(?:src|href|poster)=["\']((?:img|loops|frames|vendor|assets|film)/[^"\'#?]+)["\']', src))
    missing = sorted(a for a in assets if not os.path.exists(os.path.join(root, a)))
    test('every local asset exists', not missing, ', '.join(missing[:4]))
    test('no placeholder boxes', not re.search(r'(?i)placeholder\.(png|jpg)|via\.placeholder|lorem ipsum', src))
    fictional = re.search(r'(?i)fictional|علامة خيالية|براند خيالي|علامة وهمية', text) is not None
    real = 'data-real-brand' in src
    test('fictional brand says so (or is real)', fictional or real,
         '' if fictional or real else 'add "<Brand> is a fictional brand made for a demo." to the footer, or data-real-brand on <html>')
    test('window.__ready set', '__ready' in src)
    charset = re.search(r'<meta[^>]+charset=["\']?utf-8', src.encode('utf-8')[:1024].decode('utf-8', 'ignore'), re.I)
    test('charset declared (utf-8)', charset,
         '' if charset else 'add <meta charset="utf-8"> in the first 1024 bytes, or Arabic turns to mojibake when served')
    if is_arabic_page(src, text):
        # a hit guarded by an Arabic-script test on the same line (Latin-only tracking) is allowed
        neg = [mm for mm in re.finditer(r"""letter-spacing['"]?\s*[:=,]\s*['"]?\s*-\s*\.?\d""", src)
               if 'u0600' not in src[src.rfind('\n', 0, mm.start()) + 1:mm.start()]]
        test('Arabic: no negative letter-spacing (breaks joining)', not neg,
             f'{len(neg)} hit(s); use line-height, or scope it to Latin text only' if neg else '')

    # Warnings (USIP v6.0): reported, never fail unless --strict
    warns = []
    warns.append((re.search(r'<meta[^>]+name=["\']viewport["\']', src, re.I) is not None, 'viewport meta', ''))
    warns.append((re.search(r'<html[^>]+\blang=["\'][^"\']+', src, re.I) is not None, '<html lang> declared', ''))
    warns.append((not ARABIC.search(text) or re.search(r'<html[^>]+\bdir=["\']rtl', src, re.I) is not None, 'dir="rtl" for Arabic copy', ''))
    imgs = re.findall(r'<img\b[^>]*>', src, re.I)
    no_alt = [t for t in imgs if not re.search(r'\balt\s*=', t, re.I)]
    warns.append((not no_alt, 'alt on every <img>', f'{len(no_alt)} of {len(imgs)} without alt' if no_alt else ''))

    skipped = [r for r in res if r[1][:2] in ('L1', 'L2', 'L3') and int(r[1][1]) not in levels]
    kept = [r for r in res if r not in skipped]
    fails = [n for ok, n, _ in kept if not ok]
    warned = [n for ok, n, _ in warns if not ok]
    if strict:
        fails += warned
    return {'file': path, 'levels': list(levels), 'pass': not fails, 'status': 'PASS' if not fails else 'FAIL',
            'static_only': True,
            'tests': [{'name': n, 'status': 'ok' if ok else 'FAIL', 'note': note} for ok, n, note in kept],
            'warnings': [{'name': n, 'status': 'ok' if ok else 'warn', 'note': note} for ok, n, note in warns],
            'skipped': [n for _, n, _ in skipped], 'fails': fails}


def main(argv):
    args = list(argv)
    levels, as_json, strict = (1, 2, 3), False, False
    if '--json' in args:
        args.remove('--json')
        as_json = True
    if '--strict' in args:
        args.remove('--strict')
        strict = True
    if '--levels' in args:
        i = args.index('--levels')
        try:
            levels = parse_levels(args[i + 1])
        except (IndexError, ValueError):
            print(USAGE)
            return 2
        if not levels or any(l not in (1, 2, 3) for l in levels):
            print('levels must be from 1,2,3\n' + USAGE)
            return 2
        del args[i:i + 2]
    if len(args) != 1 or not os.path.isfile(args[0]):
        print(__doc__ + '\n' + USAGE)
        return 2
    r = run(args[0], levels, strict)
    if as_json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        w = max(len(t['name']) for t in r['tests'] + r['warnings'] + [{'name': n} for n in r['skipped']])
        for n in r['skipped']:
            print(f"  skip  {n.ljust(w)}  level not in this build")
        for t in r['tests']:
            print(f"  {'ok  ' if t['status'] == 'ok' else 'FAIL'}  {t['name'].ljust(w)}  {t['note']}")
        for t in r['warnings']:
            print(f"  {'ok  ' if t['status'] == 'ok' else 'warn'}  {t['name'].ljust(w)}  {t['note']}")
        print('PASS' if r['pass'] else f"FAIL ({len(r['fails'])})")
        print('note: static checks only; browser, console, phone and reduced-motion QA are still to do')
    return 0 if r['pass'] else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
