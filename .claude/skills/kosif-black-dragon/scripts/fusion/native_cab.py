# -*- coding: utf-8 -*-
"""native_cab.py - Black Dragon port of two ideas from JohnHeibel/ClaudeAnimationBase (MIT).

Written in our own code. Ideas ported:
  1. reads-lint  : the guide's "model the viewer" timing rule. Parses a STORYBOARD.md (logline/world/motif/arc,
                   shots with times and transitions, and per-shot timed "reads") and checks: an event/transition at
                   every seam, reads inside their shot, no overlapping reads, each read long enough for what it
                   shows (small/far/fast/subtle things need longer), no dead stretch without a read, the final read
                   held long enough to land, and no on-screen text.
  2. boil-audit  : the engine's "boil" contract. Linework is reseeded BOIL times a second (default 12 at 24 fps), so
                   pairs of frames inside one boil drawing must match except where something moves. If a moving thing
                   shifts the random stream, still things re-boil every frame (jitter). The audit measures changed
                   pixels within same-boil pairs vs across-boil pairs and flags jitter and frozen stretches.
  Helpers: seed (boil index + FNV-1a boil seed, same maths as boilSeed(key)), todo (resumable frame list:
  missing or < 1000-byte frames), same (determinism check: two renders of the same frames must match).

Usage:
  python -I native_cab.py reads-lint STORYBOARD.md [--fps 24] [--json]
  python -I native_cab.py boil-audit FRAMES_DIR [--fps 24] [--boil 12] [--json]
  python -I native_cab.py seed --times 0,0.5,1.04 --key sky [--boil 12] [--json]
  python -I native_cab.py todo FRAMES_DIR --duration 11 [--fps 24] [--range 0:4] [--json]
  python -I native_cab.py same DIR_A DIR_B [--tol 2] [--json]
  python -I native_cab.py self-test
Exit codes: 0 ok, 3 review (findings), 2 usage/input error.
"""
import argparse
import json
import math
import os
import re
import sys
import tempfile

import numpy as np

try:
    import cv2
except Exception:  # pragma: no cover
    cv2 = None

IMG_EXT = ('.jpg', '.jpeg', '.png')


# ---------------------------------------------------------------- seed / boil index
def fnv1a32(s: str) -> int:
    h = 2166136261
    for ch in s:
        # JS iterates code points but charCodeAt(0) returns the first UTF-16 unit
        cp = ord(ch)
        unit = cp if cp < 0x10000 else 0xD800 + ((cp - 0x10000) >> 10)
        h = ((h ^ unit) * 16777619) & 0xFFFFFFFF
    return h


def boil_index(t: float, boil: int = 12) -> int:
    return math.floor(t * boil)


def boil_seed(key, t: float, boil: int = 12) -> int:
    return fnv1a32(f"{key}|{boil_index(t, boil)}")


def on_twos(t: float) -> float:
    return math.floor(t * 12 + 1e-6) / 12


# ---------------------------------------------------------------- reads-lint
TIME = r"(\d+(?:\.\d+)?)\s*[-–—]\s*(\d+(?:\.\d+)?)"
SHOT_RE = re.compile(r"^\s*([A-Z][A-Za-z0-9]{0,3})\s+" + TIME + r"\s*(\[[^\]]*\])?\s*(.*)$")
READ_RE = re.compile(r"^\s*(?:reads:\s*)?" + TIME + r"\s+(.+)$")
HARD_WORDS = ('small', 'tiny', 'far', 'distant', 'fast', 'quick', 'subtle', 'background', 'corner', 'faint')
TEXT_WORDS = ('caption', 'title card', 'subtitle', 'label', 'sign saying', 'speech bubble', 'lettering',
              'on-screen text', 'text on', 'words on', 'typed', 'written', 'كتابة', 'عنوان', 'لافتة', 'نص على')
FIELDS = ('logline', 'world', 'motif', 'arc')


def parse_storyboard(text: str):
    head = {}
    shots, cur, out_tr = [], None, None
    in_shots = False
    for raw in text.splitlines():
        line = raw.rstrip()
        low = line.strip().lower()
        if not low:
            continue
        m = re.match(r"^\s*(logline|world|motif|clawd's arc|arc|[\w' ]*arc)\s*:\s*(.*)$", line, re.I)
        if m and not in_shots:
            k = m.group(1).lower()
            head['arc' if 'arc' in k else k] = m.group(2).strip()
            continue
        if low.startswith('shots'):
            in_shots = True
            continue
        if not in_shots:
            continue
        if low.startswith('[transition out'):
            out_tr = line.strip()
            continue
        sm = SHOT_RE.match(line)
        if sm and not low.startswith('reads'):
            cur = {'id': sm.group(1), 'start': float(sm.group(2)), 'end': float(sm.group(3)),
                   'transition': (sm.group(4) or '').strip('[] '), 'desc': sm.group(5).strip(), 'reads': []}
            shots.append(cur)
            continue
        rm = READ_RE.match(line)
        if rm and cur is not None:
            cur['reads'].append({'start': float(rm.group(1)), 'end': float(rm.group(2)), 'what': rm.group(3).strip()})
    return head, shots, out_tr


def min_read(what: str, base: float) -> float:
    w = what.lower()
    hard = sum(1 for k in HARD_WORDS if k in w)
    return round(base + 0.2 * hard, 3)


def lint_storyboard(text: str, fps: int = 24, base: float = 0.4, final_hold: float = 1.0, dead: float = 1.0):
    head, shots, out_tr = parse_storyboard(text)
    issues = []

    def add(sev, where, msg):
        issues.append({'severity': sev, 'where': where, 'issue': msg})

    for f in FIELDS:
        if not head.get(f):
            add('warn', 'header', f'missing "{f}" line (plan the whole film first)')
    if not shots:
        add('error', 'shots', 'no shots parsed (format: "A  0.0-3.5  [transition in: iris]  ...")')
    tol = 1.0 / fps
    for i, s in enumerate(shots):
        w = f"shot {s['id']}"
        if s['end'] <= s['start']:
            add('error', w, 'shot ends before it starts')
        if i and abs(s['start'] - shots[i - 1]['end']) > tol:
            add('error', w, f"gap/overlap with previous shot ({shots[i - 1]['end']} -> {s['start']})")
        if not s['transition']:
            add('error', w, 'no [transition] at this seam (every seam gets one; a plain cut only on action)')
        elif re.search(r'\bcut\b', s['transition'].lower()) and not re.search(r'action|smash|match', s['transition'].lower()):
            add('warn', w, 'plain cut: fine only on action or a deliberate smash cut')
        if i == 0 and s['start'] > tol:
            add('warn', w, 'film does not start at 0')
        if not s['reads']:
            add('error', w, 'no reads: list what the viewer must understand, with times')
            continue
        reads = sorted(s['reads'], key=lambda r: r['start'])
        prev_end = s['start']
        for j, r in enumerate(reads):
            rw = f"{w} read {j + 1}"
            dur = r['end'] - r['start']
            if r['start'] < s['start'] - tol or r['end'] > s['end'] + tol:
                add('error', rw, f"read {r['start']}-{r['end']} lies outside shot {s['start']}-{s['end']}")
            need = min_read(r['what'], base)
            if dur + 1e-9 < need:
                add('error', rw, f"{dur:.2f}s ({round(dur * fps)} frames) is too short for '{r['what']}' (needs >= {need}s)")
            if j and r['start'] < reads[j - 1]['end'] - tol:
                add('error', rw, f"overlaps previous read by {reads[j - 1]['end'] - r['start']:.2f}s (one read at a time)")
            if r['start'] - prev_end > dead:
                add('warn', rw, f"{r['start'] - prev_end:.2f}s with nothing to read before it (dead stretch?)")
            if any(k in r['what'].lower() for k in TEXT_WORDS):
                add('error', rw, 'on-screen text: show it, do not write it')
            prev_end = max(prev_end, r['end'])
        if s['end'] - prev_end > dead:
            add('warn', w, f"{s['end'] - prev_end:.2f}s after the last read (pad or cut)")
        if any(k in s['desc'].lower() for k in TEXT_WORDS):
            add('error', w, 'on-screen text in the shot description')
    if shots:
        last = shots[-1]
        if last['reads']:
            lr = max(last['reads'], key=lambda r: r['end'])
            if lr['end'] - lr['start'] < final_hold:
                add('error', f"shot {last['id']}", f"final read lasts {lr['end'] - lr['start']:.2f}s; give it >= {final_hold}s to land")
        if not out_tr:
            add('error', 'end', 'no [transition out: ...] (never just stop)')
    n_err = sum(1 for x in issues if x['severity'] == 'error')
    return {'ok': n_err == 0, 'errors': n_err, 'warnings': len(issues) - n_err,
            'duration': shots[-1]['end'] if shots else 0, 'shots': len(shots),
            'reads': sum(len(s['reads']) for s in shots), 'header': head, 'issues': issues}


# ---------------------------------------------------------------- frames
def list_frames(d):
    fs = sorted(f for f in os.listdir(d) if f.lower().endswith(IMG_EXT))
    return [os.path.join(d, f) for f in fs]


def load_gray(p, width=480):
    data = np.fromfile(p, dtype=np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f'cannot read {p}')
    if img.shape[1] > width:
        h = round(img.shape[0] * width / img.shape[1])
        img = cv2.resize(img, (width, h), interpolation=cv2.INTER_AREA)
    return img.astype(np.int16)


def boil_audit(d, fps=24, boil=12, thr=12, jitter_ratio=0.5, freeze_frac=0.0005):
    if cv2 is None:
        raise RuntimeError('opencv not available')
    frames = list_frames(d)
    if len(frames) < 4:
        raise ValueError('need at least 4 frames')
    same, cross, frozen = [], [], []
    prev = load_gray(frames[0])
    for i in range(1, len(frames)):
        cur = load_gray(frames[i])
        frac = float((np.abs(cur - prev) > thr).mean())
        b0, b1 = boil_index((i - 1) / fps, boil), boil_index(i / fps, boil)
        (same if b0 == b1 else cross).append(frac)
        if frac < freeze_frac:
            frozen.append(i)
        prev = cur
    med_same = float(np.median(same)) if same else None
    med_cross = float(np.median(cross)) if cross else None
    ratio = (med_same / med_cross) if (same and cross and med_cross > 1e-9) else None
    # frozen runs: consecutive identical frames longer than 0.4 s
    runs, start = [], None
    for k in range(1, len(frames)):
        if k in frozen:
            start = k - 1 if start is None else start
        elif start is not None:
            runs.append((start, k - 1)); start = None
    if start is not None:
        runs.append((start, len(frames) - 1))
    runs = [{'from_s': round(a / fps, 3), 'to_s': round(b / fps, 3)} for a, b in runs if (b - a) / fps >= 0.4]
    issues = []
    if ratio is None:
        issues.append('boil rate equals fps (or too few frames): same-boil pairs cannot be tested')
    elif ratio > jitter_ratio:
        issues.append(f'jitter: still things re-boil every frame (same-boil change is {ratio:.2f} of cross-boil change); '
                      'seed each separate element from a stable key plus the boil index')
    if runs:
        issues.append(f'{len(runs)} frozen stretch(es) >= 0.4 s: nothing is ever still')
    return {'ok': not issues, 'frames': len(frames), 'fps': fps, 'boil': boil,
            'same_boil_pairs': len(same), 'cross_boil_pairs': len(cross),
            'median_changed_same_boil': med_same, 'median_changed_cross_boil': med_cross,
            'jitter_ratio': None if ratio is None else round(ratio, 4), 'frozen': runs, 'issues': issues}


def todo_frames(d, duration, fps=24, rng=None, min_bytes=1000):
    a, b = rng if rng else (0, duration)
    first = round(a * fps)
    last = min(math.ceil(duration * fps) - 1, round(b * fps) - 1)
    todo = []
    for i in range(first, last + 1):
        f = os.path.join(d, f'f{i:05d}.jpg')
        if not os.path.exists(f) or os.path.getsize(f) < min_bytes:
            todo.append(i)
    return {'first': first, 'last': last, 'total': last - first + 1, 'todo': len(todo),
            'done': last - first + 1 - len(todo), 'frames': todo}


def same_renders(da, db, tol=2):
    fa = {os.path.basename(p): p for p in list_frames(da)}
    fb = {os.path.basename(p): p for p in list_frames(db)}
    common = sorted(set(fa) & set(fb))
    diffs = []
    for n in common:
        x, y = load_gray(fa[n], 10 ** 6), load_gray(fb[n], 10 ** 6)
        if x.shape != y.shape:
            diffs.append({'frame': n, 'max': 255, 'note': 'size differs'}); continue
        m = int(np.abs(x - y).max())
        if m > tol:
            diffs.append({'frame': n, 'max': m})
    return {'ok': not diffs and bool(common), 'compared': len(common), 'only_a': len(set(fa) - set(fb)),
            'only_b': len(set(fb) - set(fa)), 'differing': diffs[:50], 'n_differing': len(diffs)}


# ---------------------------------------------------------------- self-test
GOOD_SB = """Logline: Clawd wants the kite, but the wind steals it, so Clawd chases it home.
World: windy hill, ochre and sky, cold morning to warm noon.
Motif: the red kite.
Clawd's arc: bored -> surprised -> determined -> happy
Shots:
  A  0.0-3.0  [transition in: iris from paper]  hill, kite tugging · the wind snaps the string · take · slow push
     reads:  0.3-1.2  Clawd holds the kite on the hill
             1.3-2.0  the string snaps
             2.1-2.9  Clawd's surprised take
  B  3.0-6.5  [transition: cut on action]  the chase · Clawd catches the kite · camera follows right
     reads:  3.0-4.2  Clawd runs right after the kite
             4.3-5.0  the jump and catch
             5.0-6.3  Clawd hugs the kite, happy
  [transition out: brush wipe]
"""

BAD_SB = """Logline: x
Shots:
  A  0.0-3.0  []  a sign saying HELLO
     reads:  0.2-0.3  a tiny bird far away in the corner
             0.25-1.0  title card appears
  B  3.0-4.0  [transition: cut]  nothing
     reads:  3.0-3.4  Clawd smiles
"""


def _synth_frames(d, n=48, fps=24, boil=12, buggy=False):
    rng_bg = np.random.default_rng
    for i in range(n):
        t = i / fps
        img = np.full((270, 480, 3), (220, 235, 243), np.uint8)
        b = boil_index(t, boil)
        bg = rng_bg(boil_seed('hills', t, boil) if not buggy else 1000 + i)
        for k in range(12):  # boiling ink lines
            y = 40 + k * 18
            pts = np.array([[x, y + int(bg.integers(-3, 4))] for x in range(0, 480, 24)], np.int32)
            cv2.polylines(img, [pts], False, (51, 34, 43), 2)
        cx = int(60 + 360 * (t / (n / fps)))  # moving prop
        cv2.circle(img, (cx, 200), 18, (87, 119, 217), -1)
        cv2.imencode('.png', img)[1].tofile(os.path.join(d, f'f{i:05d}.png'))
    return b


def self_test():
    results = {}
    # seed maths
    assert fnv1a32('a') == 0xE40C292C, hex(fnv1a32('a'))
    assert boil_index(0.0) == 0 and boil_index(1 / 24) == 0 and boil_index(2 / 24) == 1
    assert boil_seed('sky', 0.0) == boil_seed('sky', 1 / 24) != boil_seed('sky', 2 / 24)
    assert abs(on_twos(0.13) - 1 / 12) < 1e-9
    results['seed'] = {'fnv1a("a")': hex(fnv1a32('a')), 'boilSeed("sky",t=0)': boil_seed('sky', 0.0)}
    # reads-lint
    g = lint_storyboard(GOOD_SB)
    assert g['ok'] and g['shots'] == 2 and g['reads'] == 6, g
    b = lint_storyboard(BAD_SB)
    msgs = ' | '.join(x['issue'] for x in b['issues'])
    for needle in ('no [transition]', 'too short', 'overlaps previous read', 'on-screen text', 'plain cut',
                   'final read', 'transition out', 'missing "world"'):
        assert needle in msgs, (needle, msgs)
    results['reads_lint'] = {'good': {'ok': g['ok'], 'errors': g['errors'], 'warnings': g['warnings']},
                             'bad': {'ok': b['ok'], 'errors': b['errors'], 'warnings': b['warnings']}}
    # boil-audit, todo, same
    with tempfile.TemporaryDirectory() as tmp:
        good, bad, again = (os.path.join(tmp, x) for x in ('good', 'bad', 'again'))
        for p in (good, bad, again):
            os.makedirs(p)
        _synth_frames(good); _synth_frames(bad, buggy=True); _synth_frames(again)
        ga, ba = boil_audit(good), boil_audit(bad)
        assert ga['ok'] and ga['jitter_ratio'] < 0.35, ga
        assert not ba['ok'] and ba['jitter_ratio'] > 0.7, ba
        sm = same_renders(good, again)
        assert sm['ok'] and sm['compared'] == 48, sm
        sd = same_renders(good, bad)
        assert not sd['ok'], sd
        fr = os.path.join(tmp, 'frames'); os.makedirs(fr)
        for i in (0, 1, 3):
            with open(os.path.join(fr, f'f{i:05d}.jpg'), 'wb') as fh:
                fh.write(b'x' * (2000 if i != 3 else 10))
        td = todo_frames(fr, duration=0.25, fps=24)
        assert td['total'] == 6 and td['frames'] == [2, 3, 4, 5], td
        results['boil_audit'] = {'good_ratio': ga['jitter_ratio'], 'buggy_ratio': ba['jitter_ratio']}
        results['same'] = {'identical_renders_ok': sm['ok'], 'different_detected': not sd['ok']}
        results['todo'] = td['frames']
    print(json.dumps({'self_test': 'PASS', **results}, ensure_ascii=False))
    return 0


# ---------------------------------------------------------------- cli
def _emit(obj, as_json, human):
    if as_json:
        print(json.dumps(obj, ensure_ascii=False, indent=1))
    else:
        print(human(obj))


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    sp = ap.add_subparsers(dest='cmd', required=True)
    p = sp.add_parser('reads-lint'); p.add_argument('storyboard'); p.add_argument('--fps', type=int, default=24)
    p.add_argument('--min-read', type=float, default=0.4); p.add_argument('--final-hold', type=float, default=1.0)
    p.add_argument('--dead', type=float, default=1.0); p.add_argument('--json', action='store_true')
    p = sp.add_parser('boil-audit'); p.add_argument('frames'); p.add_argument('--fps', type=int, default=24)
    p.add_argument('--boil', type=int, default=12); p.add_argument('--thr', type=int, default=12)
    p.add_argument('--jitter-ratio', type=float, default=0.5); p.add_argument('--json', action='store_true')
    p = sp.add_parser('seed'); p.add_argument('--times', required=True); p.add_argument('--key', default='frame')
    p.add_argument('--boil', type=int, default=12); p.add_argument('--json', action='store_true')
    p = sp.add_parser('todo'); p.add_argument('frames'); p.add_argument('--duration', type=float, required=True)
    p.add_argument('--fps', type=int, default=24); p.add_argument('--range'); p.add_argument('--json', action='store_true')
    p = sp.add_parser('same'); p.add_argument('a'); p.add_argument('b'); p.add_argument('--tol', type=int, default=2)
    p.add_argument('--json', action='store_true')
    sp.add_parser('self-test')
    a = ap.parse_args(argv)
    try:
        if a.cmd == 'self-test':
            return self_test()
        if a.cmd == 'reads-lint':
            with open(a.storyboard, encoding='utf-8') as fh:
                r = lint_storyboard(fh.read(), a.fps, a.min_read, a.final_hold, a.dead)
            _emit(r, a.json, lambda r: '\n'.join([f"reads-lint: {'OK' if r['ok'] else 'REVIEW'}  {r['shots']} shots, "
                                                  f"{r['reads']} reads, {r['errors']} errors, {r['warnings']} warnings"] +
                                                 [f"  [{x['severity']}] {x['where']}: {x['issue']}" for x in r['issues']]))
            return 0 if r['ok'] else 3
        if a.cmd == 'boil-audit':
            r = boil_audit(a.frames, a.fps, a.boil, a.thr, a.jitter_ratio)
            _emit(r, a.json, lambda r: f"boil-audit: {'OK' if r['ok'] else 'REVIEW'}  jitter_ratio={r['jitter_ratio']}  "
                                       f"frozen={len(r['frozen'])}\n" + '\n'.join('  ' + s for s in r['issues']))
            return 0 if r['ok'] else 3
        if a.cmd == 'seed':
            ts = [float(x) for x in a.times.split(',')]
            r = [{'t': t, 'boil_index': boil_index(t, a.boil), 'on_twos': on_twos(t), 'seed': boil_seed(a.key, t, a.boil)} for t in ts]
            _emit(r, a.json, lambda r: '\n'.join(f"t={x['t']}  boil={x['boil_index']}  seed={x['seed']}" for x in r))
            return 0
        if a.cmd == 'todo':
            rng = tuple(float(x) for x in a.range.split(':')) if a.range else None
            r = todo_frames(a.frames, a.duration, a.fps, rng)
            _emit(r, a.json, lambda r: f"{r['todo']} frames to render ({r['done']} already done)")
            return 0
        if a.cmd == 'same':
            r = same_renders(a.a, a.b, a.tol)
            _emit(r, a.json, lambda r: f"same: {'OK' if r['ok'] else 'DIFFER'}  compared={r['compared']}  differing={r['n_differing']}")
            return 0 if r['ok'] else 3
    except (OSError, ValueError, RuntimeError) as e:
        print(json.dumps({'error': str(e)}) if getattr(a, 'json', False) else f'error: {e}', file=sys.stderr)
        return 2
    return 2


if __name__ == '__main__':
    sys.exit(main())
