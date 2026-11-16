#!/usr/bin/env python3
"""01 «قفص الحديد»: thunderstorm. Cap shelters under the only tree and laughs at Specs, who sits in an iron cage in the open.
Lightning hits the cage and runs around the bars (Faraday cage): Specs is fine. It hits the tree: Cap is fried. He joins the cage."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import numpy as np
import os as _o, sys as _s; _s.path.insert(0, _o.path.join(_o.path.dirname(_o.path.abspath(__file__)), "..", "engine"))
import toonkit as tk
from toonkit import sm, key, lerp

D = 20.0
GY = 1320
TREE, CAGE = 250, 770
S1, S2, S3 = 5.2, 9.6, 17.0            # strikes: cage, tree, cage again


def audio(path):
    m = tk.Mix(D)
    m.sfx("rain_storm", 0, 0.34, dur=D, loop=True, fade=0.6)
    m.sfx("wind_storm", 0, 0.16, dur=D, loop=True, fade=1.0)
    m.tune(0.0, 9.4, 0.7, 0.3, minor=True)
    m.sfx("clink", 0.9, 0.3)
    for t in (2.3, 3.7): m.sfx("laugh_cartoon", t, 0.6)
    m.sfx("laugh_male", 7.9, 0.55)
    for t in (S1, S2, S3):
        m.sfx("thunder_close", t, 1.0, dur=4.5, fade=0.02); m.noise(t, 0.35, 1.2, 2, 6); m.tone(t, 90, 0.5, 0.5, 6, 50, "square")
    m.noise(S1 + 0.2, 1.0, 0.3, 3, 3)                       # current crackling round the bars
    m.noise(S2 + 0.3, 1.6, 0.35, 4, 2)                      # sizzle
    m.slide_down(S2 + 1.2); m.sfx("pop", S2 + 2.0, 0.5)     # cough of smoke
    m.steps(12.6, 14.6, 0.36, 0.2)
    for t in (14.8, 15.1, 15.4): m.clang(t, 0.25)           # knocks on the cage
    m.tone(15.9, 300, 0.4, 0.2, 5, 520)                     # door squeak
    m.sfx("giggle", 18.3, 0.6); m.sfx("clink", 18.9, 0.35)
    m.tune(15.6, 19.9, 1.0, 0.5)
    m.save(path)


def bg(g):
    tk.sky(g, (120, 104, 96), (176, 166, 156), 1100)
    tk.hills(g, 1060, 90, 520, (104, 112, 104)); tk.hills(g, 1110, 50, 300, (88, 104, 88), 2.0)
    tk.ground(g, 1100, (84, 132, 92), (56, 96, 66), (50, 90, 60))


def clouds(g, t):
    rng = np.random.default_rng(5)
    for i in range(7):
        x = (rng.uniform(0, 1500) - t * 16 * (1 + i % 3 * .3)) % 1500 - 210; y = rng.uniform(40, 360)
        tk.cloud(g, x, y, 1.5 + 0.3 * (i % 3), (86, 80, 78))


def tree(g, t, burnt):
    leaf = ((60, 62, 60), (72, 74, 72)) if burnt else ((70, 140, 86), (82, 156, 96))
    tk.tree(g, TREE, GY, 1.15, leaf, (40, 44, 50) if burnt else (56, 88, 136), sway=5 * math.sin(t * 3))
    if burnt: tk.smoke(g, (TREE, GY - 640), t, 0.9, 300, (70, 70, 74))


def cage(g, t, lit, door=0.0, front=True):
    x0, x1, top = CAGE - 170, CAGE + 170, GY - 520
    col = (255, 255, 255) if lit > 0.5 else (150, 154, 164)
    bars = [x0 + i * (x1 - x0) / 4 for i in range(5)]
    if not front:                                            # back half: floor and far bars
        g.oval((CAGE, GY + 4), (190, 26), (100, 104, 112), 6)
        return
    if lit > 0:
        g.glow((CAGE, GY - 300), 520, (120, 110, 60), 0.9 * lit)
    for i, bx in enumerate(bars):
        if door > 0 and i == 0: continue                # the door swings open on the left
        g.line((bx, GY), (bx, top), tk.INK, 16); g.line((bx, GY), (bx, top), col, 8)
    if door > 0:
        dx = 110 * math.cos(door * 1.3)
        for bx in (x0 - 0, x0 - dx):
            g.line((bx, GY), (bx, top), tk.INK, 16); g.line((bx, GY), (bx, top), col, 8)
    for y in (top, GY - 260, GY - 6):
        g.line((x0 - 6, y), (x1 + 6, y), tk.INK, 22); g.line((x0 - 6, y), (x1 + 6, y), col, 12)
    g.ellipse((CAGE, top), (176, 110), tk.INK, 22, 0, 180, 360); g.ellipse((CAGE, top), (176, 110), col, 12, 0, 180, 360)
    g.line((CAGE, top - 110), (CAGE, top - 170), tk.INK, 20); g.line((CAGE, top - 110), (CAGE, top - 170), col, 10); g.disc((CAGE, top - 176), 16, col, 6)
    if lit > 0:                                              # current running down the bars into the ground
        for i, bx in enumerate(bars):
            u = (t * 3 + i * .17) % 1; y = lerp(top, GY, u)
            tk.sparkle(g, (bx, y), 26, (200, 250, 255), 7)
        for s in (-1, 1): tk.impact(g, (CAGE + s * 190, GY + 6), t, 5, 46, (200, 250, 255))


def cup(g, c):
    g.shape([(c[0] - 20, c[1] - 22), (c[0] + 20, c[1] - 22), (c[0] + 15, c[1] + 22), (c[0] - 15, c[1] + 22)], (250, 250, 250), 5)
    g.ellipse((c[0] + 24, c[1]), (12, 12), tk.INK, 5, 0, -90, 90)


def draw(g, t, n):
    clouds(g, t)
    for i in range(5):                                       # puddles
        g.ellipse((120 + i * 230, GY + 120 + (i % 2) * 60), (90, 14), (150, 150, 140))
    burnt = t >= S2
    lit1 = max(0, 1 - (t - S1) / 1.3) if t >= S1 else 0
    lit3 = max(0, 1 - (t - S3) / 1.3) if t >= S3 else 0
    lit = max(lit1, lit3)
    tree(g, t, burnt)
    cage(g, t, lit, front=False)

    # ---- Specs, calm in the cage with his tea
    sip = 0.5 - 0.5 * math.cos(t * 1.6)
    a = tk.fig(g, "specs", CAGE + (30 if t >= 16.2 else 0), GY, -1, t, eyes="closed" if sip > 0.6 else "open", mouth="smile",
               rh=(CAGE - 40 + (30 if t >= 16.2 else 0), GY - 330 - 60 * sip), look=(0.6, 0))
    cup(g, (a["rh"][0] - 12, a["rh"][1] - 22))
    if lit > 0.3: tk.sparkles(g, a["head"], t, 5, 120, 14, (200, 250, 255))

    # ---- Cap
    if t < S2:
        scared = S1 <= t < S1 + 1.6
        if scared:
            a = tk.fig(g, "cap", TREE + 150, GY, 1, t, eyes="wide", mouth="o", brows="worried", lean=-30, lh=(TREE + 90, GY - 420), rh=(TREE + 230, GY - 430))
        else:
            a = tk.fig(g, "cap", TREE + 150, GY, 1, t, eyes="squeeze", mouth="laugh", bob=5 * math.sin(t * 15),
                       rh=(TREE + 360 + 10 * math.sin(t * 15), GY - 330 + 8 * math.sin(t * 15)))
            tk.laugh_marks(g, a["head"], t)
    elif t < 12.6:                                           # fried
        j = 6 * math.sin(t * 60) * max(0, 1 - (t - S2) / 1.2)
        a = tk.fig(g, "cap", TREE + 150 + j, GY, 1, t, eyes="wide", mouth="o" if t < S2 + 2 else "wavy", soot=0.9, lh=(TREE + 60, GY - 300), rh=(TREE + 250, GY - 300))
        tk.smoke(g, (a["top"][0], a["top"][1] - 10), t, 0.9, 220, (90, 90, 96))
        if S2 + 1.9 < t < S2 + 2.6: tk.puff(g, (a["head"][0] + 110, a["head"][1] + 40), (t - S2 - 1.9) / 0.7, 50, (80, 80, 86))
    elif t < 16.2:                                           # trudges over and knocks
        x = lerp(TREE + 150, CAGE - 300, sm((t - 12.6) / 2.0))
        knock = 14.7 <= t < 15.7
        a = tk.fig(g, "cap", x, GY, 1, t, walk=1.0 if t < 14.6 else 0, eyes="open", mouth="sad", brows="worried", soot=0.9,
                   rh=(CAGE - 186 + (16 * abs(math.sin(t * 10)) if knock else 0), GY - 330) if knock else None)
        tk.smoke(g, (a["top"][0], a["top"][1] - 10), t, 0.6, 180, (90, 90, 96))
    else:                                                    # inside, safe
        x = lerp(CAGE - 300, CAGE - 80, sm((t - 16.2) / 0.7))
        calm = t > S3 + 1.2
        a = tk.fig(g, "cap", x, GY, 1, t, walk=1.0 if t < 16.9 else 0, eyes="happy" if calm else ("wide" if t >= S3 else "open"),
                   mouth="smile" if calm else ("o" if t >= S3 else "flat"), soot=0.7, lh=(x - 30, GY - 300) if S3 <= t < S3 + 1.2 else None, rh=(x + 50, GY - 300) if S3 <= t < S3 + 1.2 else None)

    cage(g, t, lit, door=sm((t - 15.8) / 0.4) * (1 - sm((t - 17.0) / 0.4)))
    # ---- lightning
    for ts, tgt, seed in ((S1, (CAGE, GY - 700), 3), (S2, (TREE + 20, GY - 720), 8), (S3, (CAGE, GY - 700), 5)):
        if ts <= t < ts + 0.35 and int((t - ts) * 30) % 3 != 1:
            tk.bolt(g, (tgt[0] + 120, -20), tgt, seed, 16)
        if ts <= t < ts + 0.25: g.flash(0.55 * (1 - (t - ts) / 0.25))
    if S2 <= t < S2 + 0.8: tk.impact(g, (TREE + 20, GY - 700), t, 9, 150, (200, 250, 255))
    # ---- verdict badges
    if 12.0 <= t < 15.8:
        tk.badge(g, (TREE, GY - 820), False, (t - 12.0) / 0.35); tk.badge(g, (CAGE, GY - 820), True, (t - 12.5) / 0.35)
    tk.rain(g, n, 0.75)


def cam(t):
    c = key(t, [(0, (CAGE - 20, 1080, 1.45)), (1.4, (CAGE - 20, 1080, 1.45)), (2.6, (540, 960, 1.0)), (4.9, (540, 960, 1.0)), (5.3, (700, 1000, 1.25)),
                (7.2, (540, 960, 1.0)), (9.3, (540, 960, 1.0)), (9.8, (330, 980, 1.35)), (11.9, (360, 1000, 1.3)), (13.0, (540, 960, 1.0)),
                (16.0, (540, 960, 1.0)), (17.2, (720, 1060, 1.3)), (20, (740, 1080, 1.42))])
    dx = dy = 0
    for ts in (S1, S2, S3):
        s = tk.shake(t, ts, 0.5, 22); dx += s[0]; dy += s[1]
    return (c[0] + dx, c[1] + dy, c[2])


if __name__ == "__main__":
    out = sys.argv[1]
    aud = None
    if "--stills" not in sys.argv:
        aud = out.replace(".mp4", ".m4a"); audio(aud)
    tk.run(out, D, bg, draw, cam, aud)
