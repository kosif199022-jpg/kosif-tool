#!/usr/bin/env python3
"""toonb: scenery and prop helpers shared by films 11-13 (backdrop, drifting clouds, butterflies, fence, rotated props)."""
import math
import numpy as np
import toonkit as tk
from toonkit import INK, WHITE, lerp
import toonx as tx


def backdrop(g, hor, sky=((236, 200, 150), (250, 232, 200)), sun=None, mts=None, hills=(), trees=(), leaf=((88, 180, 100), (104, 200, 116)),
             ground=((104, 196, 120), (70, 150, 86), (60, 130, 76)), suncol=(120, 226, 255)):
    tk.sky(g, sky[0], sky[1], hor)
    if sun: tk.sun(g, (sun[0], sun[1]), 0, sun[2], suncol)
    if mts: tk.mountains(g, hor, mts[0], mts[1], mts[2])
    for base, amp, per, col, ph in hills: tk.hills(g, base, amp, per, col, ph)
    for x, s in trees: tk.tree(g, x, hor + 14, s, leaf)
    tk.ground(g, hor, *ground)


def clouds(g, t, seed=5, n=3, y0=120, y1=420, col=(255, 252, 250), speed=14, s=1.0):
    rng = np.random.default_rng(seed)
    for i in range(n):
        x = (rng.uniform(0, 1400) + t * speed * (1 + i * .4)) % 1400 - 180
        tk.cloud(g, x, lerp(y0, y1, i / max(1, n - 1)), s * (0.85 + 0.2 * i), col)


def butterfly(g, t, seed=1, col=(120, 120, 250), box=(100, 700, 980, 1100)):
    rng = np.random.default_rng(seed); a, b, c, e = rng.uniform(0, 6, 4)
    x = lerp(box[0], box[2], .5 + .5 * math.sin(t * .31 + a) * math.cos(t * .17 + b)); y = lerp(box[1], box[3], .5 + .5 * math.sin(t * .43 + c)) + 14 * math.sin(t * 7 + e)
    wing(g, (x, y), t, col, a)


def wing(g, p, t, col, ph=0.0, rate=14):
    f = abs(math.sin(t * rate + ph))
    for s in (-1, 1): g.oval((p[0] + s * (5 + 11 * f), p[1] - 4), (11 * f + 3, 15), col, 3)
    g.line((p[0], p[1] - 12), (p[0], p[1] + 12), INK, 5)


def fence(g, y, x0=-10, x1=1090, step=90, h=110, col=(150, 190, 226), dark=(110, 150, 196)):
    for yy in (y - h * .7, y - h * .3): g.line((x0, yy), (x1, yy), INK, 20); g.line((x0, yy), (x1, yy), dark, 12)
    for x in range(int(x0) + 30, int(x1), step):
        g.shape([(x - 16, y), (x - 16, y - h + 14), (x, y - h - 6), (x + 16, y - h + 14), (x + 16, y)], col, 5)


def rpoly(c, pts, ang):
    """Local points (relative to c) rotated by ang degrees clockwise -> world points."""
    return [tx.rot((c[0] + x, c[1] + y), c, ang) for x, y in pts]


def flowers(g, t, items, y):
    for x, h, col in items: tk.flower(g, x, y, h, col, t)


def roi_blend(g, x0, y0, x1, y1, col, amt):
    """Blend a flat colour over a rectangle (cheap see-through liquid over legs)."""
    S = tk.S; a, b, c, d = int(x0 * S), int(y0 * S), int(x1 * S), int(y1 * S)
    reg = g.img[b:d, a:c].astype(np.float32)
    g.img[b:d, a:c] = (reg * (1 - amt) + np.array(col, np.float32) * amt).astype(np.uint8)
