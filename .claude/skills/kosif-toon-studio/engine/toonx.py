#!/usr/bin/env python3
"""toonx: small helpers shared by films 08-10 (dashed lines, clamped hands, rotated figure, birds, tufts, wavy arrows)."""
import math
import cv2, numpy as np
import toonkit as tk
from toonkit import INK, WHITE, S

KEY = (255, 0, 255)


def unit(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy) or 1.0
    return (dx / L, dy / L)


def dist(a, b):
    return math.hypot(b[0] - a[0], b[1] - a[1])


def along(a, v, L):
    return (a[0] + v[0] * L, a[1] + v[1] * L)


def ang2dir(a):
    r = math.radians(a); return (math.cos(r), math.sin(r))


def dir2ang(v):
    return math.degrees(math.atan2(v[1], v[0]))


def mixdir(a, b, u):
    A, B = dir2ang(a), dir2ang(b); dl = ((B - A + 180) % 360) - 180
    return ang2dir(A + dl * u)


def rot(p, c, ang):
    """Rotate p about c by ang degrees (clockwise on screen)."""
    r = math.radians(ang); co, si = math.cos(r), math.sin(r); dx, dy = p[0] - c[0], p[1] - c[1]
    return (c[0] + co * dx - si * dy, c[1] + si * dx + co * dy)


def dashed(g, a, b, col=WHITE, th=7, dash=26, gap=18, u=1.0, ink=INK):
    L = dist(a, b) * max(0.0, min(1.0, u)); v = unit(a, b); s = 0.0
    while s < L:
        e = min(L, s + dash); p, q = along(a, v, s), along(a, v, e)
        if ink: g.line(p, q, ink, th + 6)
        g.line(p, q, col, th); s += dash + gap


def shoulder(x, gy, d=1, k=1.0, lean=0.0, crouch=0.0, sit=False, bob=0.0):
    if sit: return (x - d * 14 * k + d * lean, gy - 34 * k + bob - 152 * k)
    return (x + d * lean, gy - (232 - 110 * crouch) * k + bob - 152 * k)


def hand(x, gy, tgt, d=1, k=1.0, lean=0.0, crouch=0.0, sit=False, bob=0.0):
    """Clamp a hand target to what the arm can reach (fig stretches the forearm otherwise)."""
    sh = shoulder(x, gy, d, k, lean, crouch, sit, bob); L = dist(sh, tgt); m = 192 * k
    return tgt if L <= m else along(sh, unit(sh, tgt), m)


def birds(g, t, n=3, y=300, seed=2, col=INK, speed=60, s=1.0):
    rng = np.random.default_rng(seed)
    for i in range(n):
        x0, y0, sp = rng.uniform(0, 1300), y + rng.uniform(-90, 90), speed * rng.uniform(0.8, 1.3)
        x = (x0 + sp * t) % 1300 - 110; yy = y0 + 14 * math.sin(t * 1.3 + i)
        f = math.sin(t * 9 + i * 2)
        g.line((x, yy), (x - 24 * s, yy - 8 * s - 12 * s * f), col, 5); g.line((x, yy), (x + 24 * s, yy - 8 * s - 12 * s * f), col, 5)


def tufts(g, t, xs, y, col=(56, 126, 70), h=28):
    for x in xs:
        for a in (-0.5, 0.0, 0.5): g.line((x, y), (x + h * math.sin(a + .25 * math.sin(t * 2 + x)), y - h * math.cos(a)), col, 5)


def wavy_arrow(g, a, b, col=WHITE, th=10, amp=14, waves=3, ph=0.0, head=26):
    v = unit(a, b); nr = (-v[1], v[0]); L = dist(a, b); pts = []
    for u in np.linspace(0, 1, 28):
        w = amp * math.sin(u * waves * math.tau + ph) * (1 - u ** 4); p = along(a, v, (L - head) * u)
        pts.append((p[0] + nr[0] * w, p[1] + nr[1] * w))
    e = pts[-1]; tip = [b, (e[0] + nr[0] * head * .8, e[1] + nr[1] * head * .8), (e[0] - nr[0] * head * .8, e[1] - nr[1] * head * .8)]
    g.poly(pts, INK, th + 8, False); g.poly(tip, INK, 8); g.poly(pts, col, th, False); g.poly(tip, col)


def rfig(g, who, hip, ang, d=1, k=1.0, lh=None, rh=None, feet=None, **kw):
    """A tk.fig rotated by ang degrees (clockwise on screen) about its hip, which is placed at world point `hip`.
    lh / rh / feet are WORLD targets. Returns anchors in world coordinates."""
    n = int(1000 * S); tmp = tk.G(np.empty((n, n, 3), np.uint8)); tmp.img[:] = KEY
    a = math.radians(ang); c, s = math.cos(a), math.sin(a)
    tw = lambda p: (500 + c * (p[0] - hip[0]) + s * (p[1] - hip[1]), 500 - s * (p[0] - hip[0]) + c * (p[1] - hip[1]))
    wt = lambda p: (hip[0] + c * (p[0] - 500) - s * (p[1] - 500), hip[1] + s * (p[0] - 500) + c * (p[1] - 500))
    an = tk.fig(tmp, who, 500, 500 + 232 * k, d, k=k, shadow=False, lh=tw(lh) if lh else None, rh=tw(rh) if rh else None,
                feet=[tw(f) for f in feet] if feet else None, **kw)
    x0, y0 = max(0, int((hip[0] - 520) * S)), max(0, int((hip[1] - 520) * S)); x1, y1 = min(tk.CW, int((hip[0] + 520) * S)), min(tk.CH, int((hip[1] + 520) * S))
    if x1 > x0 and y1 > y0:
        M = np.array([[c, -s, S * hip[0] - c * 500 * S + s * 500 * S - x0], [s, c, S * hip[1] - s * 500 * S - c * 500 * S - y0]], np.float32)
        w = cv2.warpAffine(tmp.img, M, (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=KEY)
        mask = (~((w[..., 1] < 120) & (w[..., 0] > 180) & (w[..., 2] > 180))).astype(np.uint8)
        mask = cv2.erode(mask, np.ones((3, 3), np.uint8), iterations=2) > 0
        g.img[y0:y1, x0:x1][mask] = w[mask]
    out = {}
    for kk, v in an.items(): out[kk] = [wt(p) for p in v] if kk == "feet" else wt(v)
    return out
