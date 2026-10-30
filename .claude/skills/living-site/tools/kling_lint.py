#!/usr/bin/env python3
"""kling_lint.py: gate for a Kling 4.0 master prompt before any credit is spent (KOSIF v5.11, A41).

  python3 kling_lint.py prompt.txt [--duration N] [--flash] [--json]
  python3 kling_lint.py plan <seconds>          split a film into blocks of 30 s or less

The prompt follows the A41 master structure (SCENE CONTEXT ... POSITIVE CONSTRAINTS). Every check
below comes from a failure the Kling 4.0 guide or the cinematic-director workflow names.

FAIL (exit 1)
  headers     the labelled blocks are present and in order (blocks of 10 s or less may use the short set)
  duration    3..30 s per generation (3..20 s with --flash)
  timing      ACTION TIMING ranges start at 0, touch end to end, and stop exactly at the duration
  refs        every @Image/@Video/@Element line in ACTIVE REFERENCES has a role; CHARACTER and
              LOCATION lines say what is "not inherited"; a STORYBOARD says "Do not render the storyboard itself."
  limits      Omni Reference: <=10 images, <=5 videos, <=7 elements; Keyframes mode takes images only
  polish      no "flawless", "perfect", "8K", "hyperrealistic", "ultra-detailed", "masterpiece" (plastic skin)
  brands      no camera, lens or film-stock brand names (the model follows visual evidence, not names)
  mood-cam    no mood camera words ("dynamic cinematic camera"): use real moves
  arabic-dlg  no Arabic script in AUDIO (Kling 4.0 lip sync has no Arabic; use English, silence or VO in the edit)
  wide-face   a close-up never uses 24 mm / 84 degrees
warn (never fails)
  negatives   restrictions written as "no X" / "never" / "don't" other than No subtitles / No music:
              the guide says negatives raise errors, rewrite them as positive constraints
  moves       more than 2 camera moves named in one shot
  shot-len    an edited shot longer than 6 s
  headcount   no "Exactly N" head-count lock
Exit 2 on a usage error. It reads text only: it never calls Kling or Higgsfield.
"""
import json
import math
import re
import sys

USAGE = ("usage: python3 kling_lint.py prompt.txt [--duration N] [--flash] [--json]\n"
         "       python3 kling_lint.py plan <seconds>")

FULL = ['SCENE CONTEXT', 'ACTIVE REFERENCES', 'LOCATION MAP', 'FIRST FRAME AND SPATIAL BLOCKING',
        'FORMAT MODE', 'OPTICS', 'CAMERA', 'ACTION TIMING', 'ACTING TASK', 'PHYSICS', 'LIGHTING',
        'AUDIO', 'STYLE', 'QUALITY', 'POSITIVE CONSTRAINTS']
SHORT = ['SCENE CONTEXT', 'ACTIVE REFERENCES', 'ACTION TIMING', 'ACTING TASK', 'AUDIO', 'STYLE',
         'POSITIVE CONSTRAINTS']
POLISH = r'\b(flawless|perfect(?:ly)?|8k|hyper-?realistic|ultra[- ]detailed|masterpiece)\b'
BRANDS = (r'\b(arri|alexa|panavision|cooke|zeiss|kodak|fujifilm|fuji|leica|hasselblad|'
          r'sony venice|red komodo|red v-raptor|canon c\d+|angenieux|atlas orion|vantage hawk|'
          r'portra|cinestill|vision3)\b')
MOOD_CAM = r'\b(dynamic|epic|cinematic|dramatic|immersive|stunning)\s+(camera|camerawork|shot|movement)s?\b'
MOVES = ['locked-off', 'dolly', 'push-in', 'push in', 'pull-back', 'pull back', 'pan', 'tilt', 'tracking',
         'orbit', 'crane', 'handheld', 'gimbal', 'vehicle mount', 'whip', 'zoom', 'rack focus']
NEG_OK = re.compile(r'\b(no subtitles|no background music|no music|do not render the storyboard itself|'
                    r'not inherited|no cuts|no dissolves)\b', re.I)
NEG = re.compile(r"\b(no|never|don't|do not|without|avoid)\b", re.I)
ARABIC = re.compile(r'[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]')
RANGE = re.compile(r'^\s*(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)\s*s\b(.*)$', re.M)


def plan(seconds):
    """Even blocks of whole seconds, none longer than 30 s and none shorter than 3 s."""
    n = max(1, math.ceil(seconds / 30))
    base, extra = divmod(seconds, n)
    sizes = [base + (1 if i < extra else 0) for i in range(n)]
    out, t = [], 0
    for s in sizes:
        out.append((t, t + s))
        t += s
    return out


def sections(text):
    """Header name -> body, for lines that start with a known header in capitals."""
    known = sorted(set(FULL), key=len, reverse=True)
    found, order = {}, []
    lines = text.splitlines()
    cur = None
    for line in lines:
        head = next((h for h in known if line.strip().startswith(h)
                     and (line.strip() == h or not line.strip()[len(h):len(h) + 1].isalpha())), None)
        if head and line.strip().upper().startswith(head):
            cur = head
            order.append(head)
            found.setdefault(head, [])
            rest = line.strip()[len(head):].strip(' :—-')
            if rest:
                found[head].append(rest)
        elif cur:
            found[cur].append(line)
    return {k: '\n'.join(v) for k, v in found.items()}, order


def lint(text, duration=None, flash=False):
    res = []

    def test(name, ok, note='', warn=False):
        res.append({'name': name, 'status': 'ok' if ok else ('warn' if warn else 'FAIL'), 'note': note})

    secs, order = sections(text)

    # duration
    if duration is None:
        m = re.search(r'(\d+(?:\.\d+)?)\s*(?:s|sec|seconds)\b', secs.get('SCENE CONTEXT', ''))
        duration = float(m.group(1)) if m else None
    top = 20 if flash else 30
    test('duration', duration is not None and 3 <= duration <= top,
         f'{duration} s (allowed 3..{top})' if duration is not None else 'no duration in SCENE CONTEXT; pass --duration')

    # headers
    want = SHORT if duration is not None and duration <= 10 and not all(h in order for h in FULL) else FULL
    missing = [h for h in want if h not in order]
    seq = [h for h in order if h in want]
    in_order = seq == sorted(seq, key=want.index)
    test('headers', not missing and in_order,
         ('missing: ' + ', '.join(missing)) if missing else ('' if in_order else 'blocks out of order: ' + ' > '.join(seq)))

    # timing
    timing = secs.get('ACTION TIMING', '')
    ranges = [(float(a), float(b), rest) for a, b, rest in RANGE.findall(timing)]
    note, ok = '', bool(ranges)
    if not ranges:
        note = 'no "0.0-4.0s" ranges in ACTION TIMING'
    else:
        if ranges[0][0] != 0:
            ok, note = False, f'starts at {ranges[0][0]} s, not 0'
        for (a1, b1, _), (a2, b2, _) in zip(ranges, ranges[1:]):
            if abs(b1 - a2) > 1e-6:
                ok, note = False, f'gap or overlap between {b1} s and {a2} s (gaps get filled with shots you did not ask for)'
                break
        if any(b <= a for a, b, _ in ranges):
            ok, note = False, 'a range ends before it starts'
        if ok and duration is not None and abs(ranges[-1][1] - duration) > 1e-6:
            ok, note = False, f'ranges end at {ranges[-1][1]} s but the block is {duration} s'
    test('timing', ok, note or f'{len(ranges)} shots/phases add up to {ranges[-1][1] if ranges else 0} s')

    # refs and limits
    refs = secs.get('ACTIVE REFERENCES', '')
    bad = []
    for line in refs.splitlines():
        m = re.match(r'\s*(@(?:Image|Video|Element)\d+)\s*[—–-]+\s*(.*)', line)
        if not m:
            continue
        tag, body = m.groups()
        role = re.match(r'([A-Z][A-Z /]+?)\s*(?:[—–-]|:|$)', body)
        if not role:
            bad.append(f'{tag} has no ROLE')
            continue
        r = role.group(1).strip()
        if r.startswith(('CHARACTER', 'LOCATION')) and 'not inherited' not in body.lower():
            bad.append(f'{tag} {r} does not say what is not inherited')
        if r.startswith('STORYBOARD') and 'do not render the storyboard itself' not in body.lower():
            bad.append(f'{tag} STORYBOARD lacks "Do not render the storyboard itself."')
    used = {k: set(re.findall(r'@' + k + r'(\d+)', text)) for k in ('Image', 'Video', 'Element')}
    test('refs', not bad, '; '.join(bad) if bad else f"{sum(len(v) for v in used.values())} references with roles")
    over = [f'{k} {len(v)}>{lim}' for k, lim in (('Image', 10), ('Video', 5), ('Element', 7))
            for v in [used[k]] if len(v) > lim]
    keyframes = re.search(r'\bkeyframes?\s+mode\b', text, re.I)
    if keyframes and (used['Video'] or used['Element']):
        over.append('Keyframes mode takes images only; it cannot be combined with Omni references')
    test('limits', not over, '; '.join(over))

    low = text.lower()
    hits = sorted(set(m.group(0) for m in re.finditer(POLISH, low)))
    test('polish', not hits, ', '.join(hits) + ' (use fine film grain, natural skin texture with pores)' if hits else '')
    hits = sorted(set(m.group(0) for m in re.finditer(BRANDS, low)))
    test('brands', not hits, ', '.join(hits) + ' (describe the look instead)' if hits else '')
    hits = sorted(set(m.group(0) for m in re.finditer(MOOD_CAM, low)))
    test('mood-cam', not hits, ', '.join(hits) + ' (name the move: dolly-in, side-tracking, crane up)' if hits else '')
    test('arabic-dlg', not ARABIC.search(secs.get('AUDIO', '')),
         'Arabic script in AUDIO: Kling 4.0 has no Arabic lip sync' if ARABIC.search(secs.get('AUDIO', '')) else '')

    wide = [f'{a}-{b}s' for a, b, rest in ranges
            if re.search(r'close-?up', rest, re.I) and re.search(r'\b(24\s*mm|84\s*°|84 deg)', rest, re.I)]
    test('wide-face', not wide, ('24 mm / 84° on a close-up at ' + ', '.join(wide) + ' (use 50 or 85 mm)') if wide else '')

    # warnings
    negs = []
    for name in ('POSITIVE CONSTRAINTS', 'QUALITY', 'STYLE', 'CAMERA', 'ACTION TIMING', 'LIGHTING', 'PHYSICS'):
        for line in secs.get(name, '').splitlines():
            clean = NEG_OK.sub('', line)
            if NEG.search(clean):
                negs.append(line.strip()[:60])
    test('negatives', not negs, (f'{len(negs)} negative line(s), rewrite as positive constraints: ' + ' | '.join(negs[:3])) if negs else '', warn=True)
    many = []
    for a, b, rest in ranges:
        n = sum(1 for mv in MOVES if re.search(r'\b' + re.escape(mv) + r'\b', rest, re.I))
        if n > 2:
            many.append(f'{a}-{b}s ({n})')
    test('moves', not many, ('more than 2 moves: ' + ', '.join(many)) if many else '', warn=True)
    multi = re.search(r'multi-?shot|hard cuts?', secs.get('FORMAT MODE', ''), re.I)
    long_ = [f'{a}-{b}s' for a, b, _ in ranges if multi and b - a > 6]
    test('shot-len', not long_, ('edited shots over 6 s: ' + ', '.join(long_)) if long_ else '', warn=True)
    head = re.search(r'\bexactly\s+(\w+)\s+(people|person|characters?|men|women)', low)
    test('headcount', head, '' if head else 'no "Exactly N people" lock', warn=True)
    return res


def report(res, as_json):
    passed = all(r['status'] != 'FAIL' for r in res)
    if as_json:
        print(json.dumps({'result': 'PASS' if passed else 'FAIL', 'tests': res}, ensure_ascii=False, indent=1))
    else:
        for r in res:
            print(f"{r['status']:<4} {r['name']}" + (f": {r['note']}" if r['note'] else ''))
        print('PASS' if passed else 'FAIL')
    return 0 if passed else 1


def main(argv):
    if not argv or argv[0] in ('-h', '--help'):
        print(USAGE)
        return 2 if not argv else 0
    if argv[0] == 'plan':
        if len(argv) != 2 or not argv[1].isdigit() or int(argv[1]) < 3:
            print(USAGE, file=sys.stderr)
            return 2
        for i, (a, b) in enumerate(plan(int(argv[1])), 1):
            print(f'block {i}: {a}-{b} s ({b - a} s)')
        return 0
    path, duration, flash, as_json = None, None, False, False
    it = iter(argv)
    for a in it:
        if a == '--duration':
            v = next(it, None)
            try:
                duration = float(v)
            except (TypeError, ValueError):
                print(USAGE, file=sys.stderr)
                return 2
        elif a == '--flash':
            flash = True
        elif a == '--json':
            as_json = True
        elif a.startswith('-') or path:
            print(USAGE, file=sys.stderr)
            return 2
        else:
            path = a
    if not path:
        print(USAGE, file=sys.stderr)
        return 2
    try:
        text = open(path, encoding='utf-8').read()
    except OSError as e:
        print(f'cannot read {path}: {e}', file=sys.stderr)
        return 2
    return report(lint(text, duration, flash), as_json)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
