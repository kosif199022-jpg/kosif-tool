#!/usr/bin/env python3
"""toonkit: small 2D cartoon engine for the «أبو كاب / أبو نضارة» reels (1080x1920, 30 fps).

World units are 1080 x 1920. Everything is drawn on a 1.5x canvas and a camera crops it back to 1080x1920,
so zooming in up to 1.5x stays sharp. Colours are BGR tuples.

    import toonkit as tk
    def bg(g): ...                      # static background, drawn once
    def draw(g, t, n): ...              # everything that moves, every frame
    def cam(t): return (540, 960, 1.0)  # centre x, centre y, zoom (1..1.5); may add tk.shake(...)
    tk.run(out, D, bg, draw, cam, audio)       # or --stills t1,t2 on the command line -> <out>_stills/*.jpg

Characters: tk.fig(g, "cap"|"specs", x, gy, d=+1|-1, **pose) -> anchors dict (head, sh, hip, lh, rh, feet).
Audio: tk.Mix(D) with real effects from ./sfx plus synth helpers; m.save(path) writes a levelled .m4a.
"""
import math, os, subprocess, sys, wave
import cv2, numpy as np

W, H, FPS = 1080, 1920, 30
S = 1.5
CW, CH = int(W * S), int(H * S)
AA = cv2.LINE_AA
HERE = os.path.dirname(os.path.abspath(__file__))
INK = (30, 30, 34)
WHITE = (255, 255, 255)
RED, BLUE = (52, 58, 214), (214, 128, 40)
WATER, ICE = (236, 200, 120), (252, 244, 232)
SKIN = (250, 250, 250)


def sm(u):
    u = min(1.0, max(0.0, u)); return u * u * (3 - 2 * u)


def lerp(a, b, u):
    return a + (b - a) * u


def lerp2(p, q, u):
    return (p[0] + (q[0] - p[0]) * u, p[1] + (q[1] - p[1]) * u)


def out_back(u, s=1.7):
    u = min(1.0, max(0.0, u)) - 1; return u * u * ((s + 1) * u + s) + 1


def out_bounce(u):
    u = min(1.0, max(0.0, u))
    for a, b, c in ((1 / 2.75, 0, 0), (2 / 2.75, 1.5 / 2.75, .75), (2.5 / 2.75, 2.25 / 2.75, .9375), (1, 2.625 / 2.75, .984375)):
        if u < a: return 7.5625 * (u - b) ** 2 + c
    return 1.0


def key(t, keys):
    """Smooth keyframes: keys = [(t, v), ...] with v a number or tuple."""
    if t <= keys[0][0]: return keys[0][1]
    for (t0, a), (t1, b) in zip(keys, keys[1:]):
        if t <= t1:
            u = sm((t - t0) / (t1 - t0))
            return tuple(lerp(x, y, u) for x, y in zip(a, b)) if isinstance(a, (tuple, list)) else lerp(a, b, u)
    return keys[-1][1]


def shake(t, t0, dur=0.4, amp=18):
    """Camera shake offset (dx, dy) decaying after t0."""
    if not (t0 <= t < t0 + dur): return (0.0, 0.0)
    k = 1 - (t - t0) / dur
    return (amp * k * math.sin(t * 95), amp * k * math.cos(t * 83))


def ik(a, b, l1, l2, bend=1):
    d = (b[0] - a[0], b[1] - a[1]); L = min(math.hypot(*d), l1 + l2 - 1e-3); L = max(L, abs(l1 - l2) + 1e-3)
    base = math.atan2(d[1], d[0]); k = math.acos(max(-1, min(1, (l1 * l1 + L * L - l2 * l2) / (2 * l1 * L))))
    return (a[0] + l1 * math.cos(base + bend * k), a[1] + l1 * math.sin(base + bend * k))


class G:
    """Drawing surface in world units."""

    def __init__(self, img=None):
        self.img = img if img is not None else np.zeros((CH, CW, 3), np.uint8)

    @staticmethod
    def P(p):
        return (int(round(p[0] * S)), int(round(p[1] * S)))

    @staticmethod
    def T(th):
        return max(1, int(round(th * S)))

    def line(self, a, b, col=INK, th=8):
        cv2.line(self.img, self.P(a), self.P(b), col, self.T(th), AA)

    def poly(self, pts, col, th=0, closed=True):
        arr = np.round(np.array(pts, np.float64) * S).astype(np.int32)
        if th: cv2.polylines(self.img, [arr], closed, col, self.T(th), AA)
        else: cv2.fillPoly(self.img, [arr], col, AA)

    def shape(self, pts, fill, th=6, ink=INK):
        self.poly(pts, fill); self.poly(pts, ink, th)

    def circle(self, c, r, col, th=0):
        cv2.circle(self.img, self.P(c), max(1, int(round(r * S))), col, -1 if not th else self.T(th), AA)

    def disc(self, c, r, fill, th=6, ink=INK):
        self.circle(c, r, fill); self.circle(c, r, ink, th)

    def ellipse(self, c, axes, col, th=0, ang=0, a0=0, a1=360):
        cv2.ellipse(self.img, self.P(c), (max(1, int(round(axes[0] * S))), max(1, int(round(axes[1] * S)))), ang, a0, a1, col, -1 if not th else self.T(th), AA)

    def oval(self, c, axes, fill, th=6, ang=0, ink=INK):
        self.ellipse(c, axes, fill, 0, ang); self.ellipse(c, axes, ink, th, ang)

    def rect(self, a, b, fill, th=6, ink=INK):
        pts = [a, (b[0], a[1]), b, (a[0], b[1])]; self.poly(pts, fill)
        if th: self.poly(pts, ink, th)

    def capsule(self, a, b, fill, w, ink=INK, edge=5):
        """Thick rounded limb with an ink outline."""
        self.line(a, b, ink, w + 2 * edge); self.line(a, b, fill, w)

    def vgrad(self, y0, y1, top, bot, x0=0, x1=W):
        a, b = int(y0 * S), int(y1 * S)
        k = np.linspace(0, 1, max(1, b - a))[:, None, None]
        self.img[a:b, int(x0 * S):int(x1 * S)] = (np.array(top, np.float32) * (1 - k) + np.array(bot, np.float32) * k).astype(np.uint8)

    def _roi(self, c, r):
        x0, y0 = max(0, int((c[0] - r) * S)), max(0, int((c[1] - r) * S)); x1, y1 = min(CW, int((c[0] + r) * S)), min(CH, int((c[1] + r) * S))
        return (x0, y0, x1, y1) if x1 > x0 and y1 > y0 else None

    def glow(self, c, r, col, amt=0.6):
        """Soft additive light."""
        q = self._roi(c, r)
        if not q or amt <= 0: return
        x0, y0, x1, y1 = q
        yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
        d = np.hypot(xx - c[0] * S, yy - c[1] * S) / (r * S)
        a = (np.clip(1 - d, 0, 1) ** 2 * amt)[..., None]
        reg = self.img[y0:y1, x0:x1].astype(np.float32)
        self.img[y0:y1, x0:x1] = np.clip(reg + np.array(col, np.float32) * a, 0, 255).astype(np.uint8)

    def shade(self, c, rx, ry, amt=0.22):
        """Soft ground shadow."""
        q = self._roi(c, max(rx, ry))
        if not q: return
        x0, y0, x1, y1 = q
        yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
        d = ((xx - c[0] * S) / (rx * S)) ** 2 + ((yy - c[1] * S) / (ry * S)) ** 2
        a = (np.clip(1 - d, 0, 1) ** 0.7 * amt)[..., None]
        self.img[y0:y1, x0:x1] = (self.img[y0:y1, x0:x1].astype(np.float32) * (1 - a)).astype(np.uint8)

    def tint(self, mul):
        """Multiply the whole picture (night, dusk)."""
        self.img[:] = np.clip(self.img.astype(np.float32) * np.array(mul, np.float32), 0, 255).astype(np.uint8)

    def flash(self, amt):
        if amt > 0: self.img[:] = np.clip(self.img.astype(np.float32) + 255 * amt, 0, 255).astype(np.uint8)

    def layer(self):
        """with-less alpha helper: lay = g.layer(); draw on lay; g.blend(lay, 0.5)."""
        return G(self.img.copy())

    def blend(self, lay, amt):
        cv2.addWeighted(lay.img, amt, self.img, 1 - amt, 0, self.img)


# ------------------------------------------------------------------ scenery
def sky(g, top=(236, 200, 150), bot=(250, 232, 200), horizon=1100):
    g.vgrad(0, horizon, top, bot)


def sun(g, c, t=0.0, r=92, col=(120, 226, 255)):
    g.glow(c, r * 4.2, (60, 70, 80), 0.9)
    for i in range(14):
        a = i * math.tau / 14 + t * 0.3
        g.line((c[0] + (r + 18) * math.cos(a), c[1] + (r + 18) * math.sin(a)), (c[0] + (r + 56) * math.cos(a), c[1] + (r + 56) * math.sin(a)), col, 11)
    g.disc(c, r, col, 6, (60, 170, 235)); g.circle((c[0] - r * .28, c[1] - r * .3), r * .34, (190, 244, 255))


def moon(g, c, r=80, skycol=(110, 60, 40)):
    g.glow(c, r * 3.4, (70, 70, 60), 0.7); g.circle(c, r, (236, 244, 250)); g.circle((c[0] + r * .42, c[1] - r * .25), r * .86, skycol)


def stars(g, t, n=60, ymax=900, seed=6, amt=1.0):
    rng = np.random.default_rng(seed)
    for _ in range(n):
        x, y, p = rng.uniform(0, W), rng.uniform(30, ymax), rng.uniform(0, 6.3)
        v = int(255 * amt * (0.45 + 0.55 * math.sin(t * 3 + p) ** 2))
        g.circle((x, y), 3, (v, v, v))


def cloud(g, x, y, s=1.0, col=(255, 252, 250), ink=None):
    blobs = ((-92, 14, 54), (-34, -16, 74), (50, -6, 66), (112, 18, 46))
    if ink:
        for dx, dy, r in blobs: g.circle((x + dx * s, y + dy * s), r * s + 5, ink)
    for dx, dy, r in blobs: g.circle((x + dx * s, y + dy * s), r * s, col)
    g.rect((x - 110 * s, y + 10 * s), (x + 130 * s, y + 50 * s), col, 0)


def hills(g, base, amp, per, col, ph=0.0, bottom=None):
    pts = [(x, base - amp * (0.5 + 0.5 * math.sin(x / per * math.tau + ph)) - 0.35 * amp * math.sin(x / (per * .37) + ph)) for x in range(-20, W + 40, 20)]
    g.poly(pts + [(W + 20, bottom or base + 200), (-20, bottom or base + 200)], col)


def mountains(g, base, peaks, col, cap=(250, 246, 240)):
    """peaks = [(x, y), ...] alternating valley/peak, starting and ending with valleys at the base."""
    g.poly(peaks, col)
    for i in range(1, len(peaks) - 1, 2):
        px, py = peaks[i]; h = 90
        l = (px - h * (px - peaks[i - 1][0]) / max(1, peaks[i - 1][1] - py), py + h); r = (px + h * (peaks[i + 1][0] - px) / max(1, peaks[i + 1][1] - py), py + h)
        g.poly([l, (px, py), r, lerp2((px, py + h * .7), r, .4), (px, py + h * 1.1), lerp2((px, py + h * .7), l, .4)], cap)


def ground(g, y, top=(104, 196, 120), bot=(70, 150, 86), edge=(60, 130, 76)):
    g.vgrad(y, H, top, bot); g.line((-10, y), (W + 10, y), edge, 6)


def tree(g, x, base, s=1.0, leaf=((88, 180, 100), (104, 200, 116)), trunk=(60, 96, 150), sway=0.0):
    g.shape([(x - 36 * s, base), (x - 22 * s, base - 330 * s), (x + 22 * s, base - 330 * s), (x + 36 * s, base)], trunk, 6)
    blobs = ((-150, -380, 130), (150, -380, 130), (0, -480, 165), (-70, -330, 120), (80, -340, 120))
    for dx, dy, r in blobs: g.circle((x + dx * s + sway, base + dy * s), r * s + 6, INK)
    for i, (dx, dy, r) in enumerate(blobs): g.circle((x + dx * s + sway, base + dy * s), r * s, leaf[i % 2])
    g.ellipse((x - 40 * s + sway, base - 470 * s), (60 * s, 36 * s), (150, 226, 160), 6, 0, 200, 320)


def pine(g, x, base, s=1.0, snow=True):
    g.line((x, base), (x, base - 70 * s), (50, 70, 100), 14)
    for j in range(3):
        y = base - 56 * s - j * 58 * s; w = (96 - j * 24) * s
        g.shape([(x - w, y), (x, y - 90 * s), (x + w, y)], (96, 130, 84), 5)
        if snow: g.poly([(x - w * .5, y - 45 * s), (x, y - 90 * s), (x + w * .5, y - 45 * s)], (250, 248, 244))


def grass(g, t, n=34, y0=1360, y1=H - 30, seed=8, col=(56, 126, 70)):
    rng = np.random.default_rng(seed)
    for _ in range(n):
        x, y = rng.uniform(0, W), rng.uniform(y0, y1)
        for a in (-0.5, 0.0, 0.5): g.line((x, y), (x + 28 * math.sin(a + .25 * math.sin(t * 2 + x)), y - 28 * math.cos(a)), col, 5)


def flower(g, x, base, hgt, col, t=0.0, wilt=0.0):
    sway = 6 * math.sin(t * 2 + x * .03) * (1 - wilt); pts = []
    for u in np.linspace(0, 1, 10):
        b = wilt * (u ** 2) * 1.5; pts.append((x + sway * u + hgt * 0.55 * math.sin(b) * u, base - hgt * u * math.cos(b * 0.9)))
    stem = tuple(int(lerp(a, b, wilt)) for a, b in zip((60, 150, 80), (90, 130, 150)))
    g.poly(pts, INK, 12, False); g.poly(pts, stem, 7, False)
    c = pts[-1]; r = 16 + 10 * (1 - wilt); pc = tuple(int(lerp(a, b, wilt)) for a, b in zip(col, (150, 160, 170)))
    pet = [(c[0] + r * math.cos(a * math.tau / 6), c[1] + r * math.sin(a * math.tau / 6) + 10 * wilt) for a in range(6)]
    for q in pet: g.circle(q, r * .62 + 3, INK)
    for q in pet: g.circle(q, r * .62, pc)
    g.circle((c[0], c[1] + 10 * wilt), r * .5, (70, 205, 250) if wilt < 0.5 else (110, 150, 170))


def rain(g, n, heavy=1.0, slant=0.16, col=(240, 236, 230)):
    rng = np.random.default_rng(n * 7919 + 3); lay = g.layer()
    for _ in range(int(240 * heavy)):
        x, y, L = rng.uniform(-60, W), rng.uniform(-40, H), rng.uniform(46, 100)
        lay.line((x, y), (x - L * slant, y + L), col, 3)
    g.blend(lay, 0.38)


def snowfall(g, t, n=80, seed=8):
    rng = np.random.default_rng(seed)
    for _ in range(n):
        x0, y0, s = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(40, 120)
        g.circle(((x0 - 20 * t + 30 * math.sin(t + y0)) % W, (y0 + s * t) % H), s / 26 + 2, WHITE)


def bolt(g, a, b, seed=1, th=14, col=(200, 250, 255)):
    """Lightning from a to b."""
    rng = np.random.default_rng(seed); pts = [a]
    for i in range(1, 9):
        u = i / 9; pts.append((lerp(a[0], b[0], u) + rng.uniform(-60, 60), lerp(a[1], b[1], u)))
    pts.append(b)
    g.poly(pts, (255, 255, 255), th + 14, False); g.poly(pts, col, th, False); g.poly(pts, (255, 255, 255), max(2, th // 3), False)
    return pts


# ------------------------------------------------------------------ effects
def bezier(p0, p1, p2, n=24):
    return [((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * p1[0] + u * u * p2[0], (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * p1[1] + u * u * p2[1]) for u in np.linspace(0, 1, n)]


def stream(g, a, b, t, th=12, col=WATER, sag=0.0):
    """Falling or poured water from a to b (parabolic)."""
    pts = [(lerp(a[0], b[0], u) + 4 * math.sin(u * 9 + t * 14), lerp(a[1], b[1], u * u) + sag * math.sin(u * math.pi)) for u in np.linspace(0, 1, 16)]
    g.poly(pts, INK, th + 8, False); g.poly(pts, col, th, False); g.poly(pts, (255, 250, 236), max(2, th // 3), False)


def splash(g, c, u, n=14, r=160, col=WATER, seed=5):
    """Burst of drops; u = 0..1 progress."""
    if not 0 <= u <= 1: return
    rng = np.random.default_rng(seed)
    for i in range(n):
        a = -math.pi * rng.uniform(0.05, 0.95); v = rng.uniform(0.5, 1.0) * r
        p = (c[0] + v * math.cos(a) * u, c[1] + v * math.sin(a) * u + r * 1.2 * u * u)
        g.disc(p, rng.uniform(7, 16) * (1 - u * .6), col if i % 3 else (255, 250, 236), 3)


def drops(g, c, t, n=4, spread=90, col=(236, 196, 120), rate=1.5):
    """Sweat or drips flying off around a head."""
    for i in range(n):
        ph = (t * rate + i / n) % 1; a = -2.6 + i * (2.2 / max(1, n - 1))
        p = (c[0] + (spread + 36 * ph) * math.cos(a), c[1] + (spread + 36 * ph) * math.sin(a) + 44 * ph * ph)
        g.shape([(p[0] - 9, p[1]), (p[0], p[1] - 22), (p[0] + 9, p[1]), (p[0] + 6, p[1] + 9), (p[0] - 6, p[1] + 9)], col, 3, (150, 110, 40))


def impact(g, c, t, n=7, r=60, col=(60, 214, 255)):
    for i in range(n):
        a = i * math.tau / n + 0.3; k = 1 + 0.2 * math.sin(t * 40 + i)
        g.line((c[0] + r * .4 * math.cos(a), c[1] + r * .4 * math.sin(a)), (c[0] + r * k * math.cos(a), c[1] + r * k * math.sin(a)), INK, 12)
        g.line((c[0] + r * .4 * math.cos(a), c[1] + r * .4 * math.sin(a)), (c[0] + r * k * math.cos(a), c[1] + r * k * math.sin(a)), col, 6)


def star(g, c, r, col=(70, 220, 255), rot=0.0):
    pts = [(c[0] + (r if j % 2 == 0 else r * .45) * math.cos(j * math.pi / 5 - math.pi / 2 + rot), c[1] + (r if j % 2 == 0 else r * .45) * math.sin(j * math.pi / 5 - math.pi / 2 + rot)) for j in range(10)]
    g.shape(pts, col, 4)


def dizzy(g, c, t, n=4, r=110):
    for i in range(n):
        a = t * 5 + i * math.tau / n; star(g, (c[0] + r * math.cos(a), c[1] - 100 + 26 * math.sin(a)), 20, rot=t * 3)


def sparkle(g, c, r, col=WHITE, th=5):
    g.line((c[0] - r, c[1]), (c[0] + r, c[1]), col, th); g.line((c[0], c[1] - r), (c[0], c[1] + r), col, th)


def sparkles(g, c, t, n=6, r=90, size=14, col=WHITE):
    for i in range(n):
        a = i * math.tau / n + t * 3; sparkle(g, (c[0] + r * math.cos(a), c[1] + r * math.sin(a)), size * (0.6 + 0.4 * math.sin(t * 9 + i)), col)


def puff(g, c, u, r=60, col=(236, 232, 228), n=6):
    """Dust or smoke puff expanding and fading, u = 0..1."""
    if not 0 <= u <= 1: return
    lay = g.layer()
    for i in range(n):
        a = i * math.tau / n; lay.circle((c[0] + r * 1.4 * u * math.cos(a), c[1] + r * u * math.sin(a) * .6 - r * .5 * u), r * (0.5 + .5 * u), col)
    g.blend(lay, 0.7 * (1 - u))


def smoke(g, c, t, amt=1.0, h=340, col=(236, 232, 228), n=7):
    lay = g.layer()
    for i in range(n):
        ph = (t * 0.45 + i / n) % 1; lay.circle((c[0] + 30 * math.sin(ph * 7 + i), c[1] - h * ph), 12 + 38 * ph, col)
    g.blend(lay, 0.55 * amt)


def fire(g, c, t, lvl=1.0, w=70, h=220):
    """Flame with its base centre at c."""
    if lvl <= 0: return
    g.glow((c[0], c[1] - h * .4 * lvl), 420 * lvl, (10, 60, 130), 0.55)
    for r, col in ((1.0, (40, 110, 245)), (0.68, (60, 200, 255)), (0.36, (220, 250, 255))):
        hh = h * lvl * r * (1 + 0.10 * math.sin(t * 17 + r * 9)); ww = w * lvl * r; sw = 16 * lvl * math.sin(t * 9 + r * 4)
        pts = [(c[0] - ww * math.cos(u * math.pi / 2) + sw * u, c[1] - hh * u) for u in np.linspace(0, 1, 10)] + [(c[0] + ww * math.cos(u * math.pi / 2) + sw * u, c[1] - hh * u) for u in np.linspace(1, 0, 10)]
        g.poly(pts, col)
        if r == 1.0: g.poly(pts, INK, 5)


def arrow(g, a, b, col=WHITE, th=14, head=30):
    """Chunky outlined arrow (forces, directions)."""
    ang = math.atan2(b[1] - a[1], b[0] - a[0]); L = math.hypot(b[0] - a[0], b[1] - a[1])
    e = (a[0] + (L - head) * math.cos(ang), a[1] + (L - head) * math.sin(ang))
    tip = [b, (e[0] + head * .8 * math.cos(ang + math.pi / 2), e[1] + head * .8 * math.sin(ang + math.pi / 2)), (e[0] + head * .8 * math.cos(ang - math.pi / 2), e[1] + head * .8 * math.sin(ang - math.pi / 2))]
    g.line(a, e, INK, th + 10); g.poly(tip, INK, 10); g.line(a, e, col, th); g.poly(tip, col)


def badge(g, c, ok, u=1.0, r=58):
    """Green tick or red cross popping in (u = 0..1)."""
    k = out_back(u)
    if k <= 0.02: return
    r = r * k; g.disc(c, r, (90, 190, 80) if ok else (70, 70, 230), 7)
    if ok: g.poly([(c[0] - r * .45, c[1]), (c[0] - r * .1, c[1] + r * .38), (c[0] + r * .5, c[1] - r * .35)], WHITE, 12, False)
    else:
        g.line((c[0] - r * .38, c[1] - r * .38), (c[0] + r * .38, c[1] + r * .38), WHITE, 12); g.line((c[0] + r * .38, c[1] - r * .38), (c[0] - r * .38, c[1] + r * .38), WHITE, 12)


def bulb(g, c, u=1.0, t=0.0):
    """Idea light bulb popping in."""
    r = 40 * out_back(u)
    if r < 4: return
    g.glow(c, r * 4, (40, 90, 110), 0.8)
    for i in range(8):
        a = i * math.tau / 8 + t; g.line((c[0] + (r + 14) * math.cos(a), c[1] + (r + 14) * math.sin(a)), (c[0] + (r + 34) * math.cos(a), c[1] + (r + 34) * math.sin(a)), (60, 210, 250), 7)
    g.disc(c, r, (90, 230, 255), 5); g.rect((c[0] - 14, c[1] + r - 4), (c[0] + 14, c[1] + r + 20), (170, 170, 176), 4)


def laugh_marks(g, hc, t, d=1):
    for i in range(3):
        q = (hc[0] - d * (112 + i * 18), hc[1] - 60 + i * 38 + 6 * math.sin(t * 15 + i)); g.line(q, (q[0] - d * 30, q[1] - 12), INK, 6)


def speed_lines(g, c, d=1, n=4, L=90, gap=26):
    for i in range(n): g.line((c[0] - d * 40, c[1] + (i - n / 2) * gap), (c[0] - d * (40 + L * (0.6 + 0.4 * (i % 2))), c[1] + (i - n / 2) * gap), INK, 6)


# ------------------------------------------------------------------ characters
SHIRT = {"cap": (60, 70, 220), "specs": (200, 130, 50)}
SHOE = {"cap": (40, 44, 170), "specs": (150, 90, 30)}


def _face(g, c, r, d, eyes, mouth, brows, look, t):
    e1, e2 = (c[0] + d * r * .10, c[1] - r * .02), (c[0] + d * r * .62, c[1] - r * .02)
    er = r * .21
    for e in (e1, e2):
        if eyes in ("open", "wide", "angry", "sleepy"):
            rr = er * (1.25 if eyes == "wide" else 1.0)
            g.disc(e, rr, WHITE, 4); g.circle((e[0] + look[0] * rr * .45, e[1] + look[1] * rr * .45), rr * (.42 if eyes == "wide" else .5), INK)
            g.circle((e[0] + look[0] * rr * .45 - rr * .15, e[1] + look[1] * rr * .45 - rr * .18), rr * .15, WHITE)
            if eyes == "sleepy": g.ellipse(e, (rr, rr), SKIN, 0, 0, 180, 360); g.line((e[0] - rr, e[1]), (e[0] + rr, e[1]), INK, 5)
        elif eyes == "happy": g.ellipse((e[0], e[1] + er * .3), (er, er * .9), INK, 6, 0, 200, 340)
        elif eyes == "closed": g.ellipse((e[0], e[1] - er * .3), (er, er * .8), INK, 6, 0, 20, 160)
        elif eyes == "squeeze": g.poly([(e[0] - d * er, e[1] - er * .7), (e[0] + d * er * .6, e[1]), (e[0] - d * er, e[1] + er * .7)], INK, 6, False)
    if brows or eyes == "angry":
        b = brows or "down"
        for i, e in enumerate((e1, e2)):
            s = d * (1 if i == 0 else -1)
            if b == "down": g.line((e[0] - s * er * 1.1, e[1] - er * 1.9), (e[0] + s * er * 1.0, e[1] - er * 1.25), INK, 7)
            elif b == "worried": g.line((e[0] - s * er * 1.1, e[1] - er * 1.3), (e[0] + s * er * 1.0, e[1] - er * 1.95), INK, 7)
            else: g.line((e[0] - er, e[1] - er * 1.8), (e[0] + er, e[1] - er * 1.8), INK, 7)
    m = (c[0] + d * r * .36, c[1] + r * .50)
    if mouth == "smile": g.ellipse((m[0], m[1] - r * .12), (r * .34, r * .26), INK, 6, 0, 20, 160)
    elif mouth == "laugh":
        o = r * .05 * math.sin(t * 16)
        g.ellipse((m[0], m[1] - r * .1), (r * .46, r * .36 + o), (50, 36, 70), 0, 0, 0, 180); g.ellipse((m[0], m[1] - r * .1), (r * .46, r * .36 + o), INK, 6, 0, 0, 180)
        g.line((m[0] - r * .46, m[1] - r * .1), (m[0] + r * .46, m[1] - r * .1), INK, 6)
        g.rect((m[0] - r * .36, m[1] - r * .07), (m[0] + r * .36, m[1] + r * .02), WHITE, 0)
        g.ellipse((m[0], m[1] + r * .17 + o * .5), (r * .22, r * .1), (120, 120, 235))
    elif mouth == "o": g.oval(m, (r * .14, r * .18), (50, 36, 70), 5)
    elif mouth == "sad": g.ellipse((m[0], m[1] + r * .16), (r * .3, r * .2), INK, 6, 0, 200, 340)
    elif mouth == "flat": g.line((m[0] - r * .24, m[1]), (m[0] + r * .24, m[1]), INK, 6)
    elif mouth == "wavy": g.poly([(m[0] - r * .34 + k * r * .085, m[1] + r * .07 * math.sin(k * 1.4 + t * 9)) for k in range(9)], INK, 6, False)
    elif mouth == "grit":
        g.rect((m[0] - r * .34, m[1] - r * .12), (m[0] + r * .34, m[1] + r * .12), WHITE, 5)
        for k in range(1, 4): g.line((m[0] - r * .34 + k * r * .17, m[1] - r * .12), (m[0] - r * .34 + k * r * .17, m[1] + r * .12), INK, 3)
    elif mouth == "tongue":
        g.ellipse((m[0], m[1] - r * .1), (r * .3, r * .22), INK, 6, 0, 20, 160); g.oval((m[0] + d * r * .06, m[1] + r * .16), (r * .13, r * .16), (120, 120, 235), 4)


def head(g, who, c, d=1, r=84, eyes="open", mouth="smile", brows=None, look=(0.4, 0.0), blush=0.0, t=0.0, soot=0.0):
    look = (look[0] * d, look[1])
    skin = tuple(int(lerp(a, b, blush)) for a, b in zip(SKIN, (150, 160, 245)))
    skin = tuple(int(lerp(a, b, soot)) for a, b in zip(skin, (74, 70, 70)))
    g.disc(c, r, skin, 7)
    g.ellipse((c[0] - d * r * .25, c[1] + r * .2), (r * .62, r * .62), tuple(int(v * .93) for v in skin), 0, 0, 100 if d > 0 else -10, 190 if d > 0 else 80)
    g.circle(c, r, INK, 7)
    for s in (0.05, 0.72):
        ck = (c[0] + d * r * s, c[1] + r * .22)
        lay_col = tuple(int(lerp(a, b, .5)) for a, b in zip(skin, (170, 170, 250)))
        g.ellipse(ck, (r * .16, r * .09), lay_col)
    if who == "specs":
        for k in range(7):
            a = math.radians((205 if d > 0 else 187) + k * 22)
            p0 = (c[0] + (r - 4) * math.cos(a - .13), c[1] + (r - 4) * math.sin(a - .13)); p1 = (c[0] + (r - 4) * math.cos(a + .13), c[1] + (r - 4) * math.sin(a + .13))
            g.poly([p0, (c[0] + (r + 34) * math.cos(a + .1 * d), c[1] + (r + 34) * math.sin(a + .1 * d)), p1], INK)
        g.ellipse(c, (r, r), INK, 18, 0, 198, 342)
    _face(g, c, r, d, eyes, mouth, brows, (look[0] / d, look[1]) if d else look, t)
    if who == "specs":
        for s in (0.10, 0.62):
            e = (c[0] + d * r * s, c[1] - r * .02); g.circle(e, r * .29, INK, 6); g.ellipse((e[0] - r * .1, e[1] - r * .12), (r * .09, r * .05), WHITE, 0, -40)
        g.line((c[0] + d * r * .36 - 4, c[1] - r * .04), (c[0] + d * r * .36 + 4, c[1] - r * .04), INK, 6); g.line((c[0] - d * r * .19, c[1] - r * .04), (c[0] - d * r * .78, c[1] - r * .16), INK, 6)
    else:
        red, dark = (52, 58, 214), (36, 40, 160)
        g.ellipse((c[0], c[1] - 6), (r + 3, r + 3), red, 0, 0, 206, 334); g.ellipse((c[0], c[1] - 6), (r + 3, r + 3), INK, 7, 0, 206, 334)
        g.ellipse((c[0] - d * r * .2, c[1] - 6), (r * .8, r * .8), dark, 0, 0, 200 if d > 0 else 280, 260 if d > 0 else 340)
        vis = [(c[0] + d * r * .42, c[1] - r * .52), (c[0] + d * (r + 66), c[1] - r * .44), (c[0] + d * (r + 58), c[1] - r * .28), (c[0] + d * r * .62, c[1] - r * .38)]
        g.shape(vis, red, 6); g.line((c[0] - r * .9, c[1] - r * .44), (c[0] + r * .9, c[1] - r * .44), INK, 7)
        g.disc((c[0], c[1] - r - 8), 9, red, 4)


def fig(g, who, x, gy, d=1, t=0.0, k=1.0, lean=0.0, bob=0.0, walk=0.0, ph=None, sit=False, feet=None, lh=None, rh=None,
        eyes="open", mouth="smile", brows=None, look=(0.4, 0.0), blush=0.0, sweat=0, head_dy=0.0, shadow=True, scarf=None, crouch=0.0, soot=0.0):
    """Draw one character standing on ground y=gy at x, facing d (+1 right, -1 left).
    walk: 0..1.3 stride amount (uses ph, default x*0.05). sit: seated on the ground, legs forward.
    lh / rh: world targets for the far / near hand (None = relaxed, swinging while walking).
    crouch: 0..1 lowers the hips (kneel / squat). soot: 0..1 blackened (after a blast). blush: 0..1 red face.
    eyes: open|wide|angry|sleepy|happy|closed|squeeze. mouth: smile|laugh|o|sad|flat|wavy|grit|tongue. brows: None|down|worried|flat.
    Returns anchors in world coords."""
    ph = x * 0.05 if ph is None else ph
    LEG, ARM = 118 * k, 100 * k
    shirt, shoe = SHIRT[who], SHOE[who]
    if soot: shirt = tuple(int(lerp(a, b, soot)) for a, b in zip(shirt, (60, 58, 58)))
    if shadow: g.shade((x, gy + 6), 120 * k, 22 * k)
    if sit:
        hip = (x, gy - 34 * k + bob); f = [(x + d * 230 * k, gy - 6), (x + d * 200 * k, gy - 4)]; kn = [(x + d * 118 * k, gy - 74 * k), (x + d * 108 * k, gy - 44 * k)]
        sh = (x - d * 14 * k + d * lean, hip[1] - 172 * k)
    else:
        hip = (x, gy - (232 - 110 * crouch) * k - abs(math.cos(ph)) * 7 * walk + bob)
        if feet is None:
            f = []
            for sgn in (-1, 1):
                s = 44 * k * math.sin(ph) * sgn * walk
                f.append((x + d * s + (sgn * 16 * k if not walk else 0), gy - 6 - 18 * k * max(0, math.cos(ph) * sgn) * walk))
        else: f = list(feet)
        kn = [ik(hip, (p[0], p[1] - 14), LEG, LEG, -d) for p in f]
        sh = (x + d * lean, hip[1] - 172 * k)
    hc = (sh[0] + d * 10 * k, sh[1] - 92 * k + head_dy)
    A = lambda tgt, i: tgt if tgt is not None else (sh[0] + d * (i * 2 - 1) * (34 + 30 * math.sin(ph) * walk) * k, sh[1] + 182 * k)
    lt, rt = A(lh, 0), A(rh, 1)
    shd = (sh[0], sh[1] + 20 * k)
    # far arm, far leg
    el = ik(shd, lt, ARM, ARM, d if lh is None else -d)
    g.line(shd, el, INK, 12 * k); g.line(el, lt, INK, 12 * k)
    g.line(hip, kn[0], INK, 13 * k); g.line(kn[0], (f[0][0], f[0][1] - 14), INK, 13 * k)
    g.oval((f[0][0] + d * 18 * k, f[0][1] - 10), (36 * k, 16 * k), tuple(int(v * .8) for v in shoe), 5)
    # torso
    g.capsule((hip[0], hip[1] - 4), (sh[0], sh[1] + 16 * k), shirt, 44 * k, edge=5)
    if scarf: g.line((sh[0] - 26 * k, sh[1] + 2), (sh[0] + 26 * k, sh[1] - 2), scarf, 22 * k); g.line((sh[0] - d * 18 * k, sh[1] + 6), (sh[0] - d * 56 * k, sh[1] + 52 * k), scarf, 16 * k)
    # near leg
    g.line(hip, kn[1], INK, 13 * k); g.line(kn[1], (f[1][0], f[1][1] - 14), INK, 13 * k)
    g.oval((f[1][0] + d * 18 * k, f[1][1] - 10), (36 * k, 16 * k), shoe, 5)
    g.disc(lt, 13 * k, SKIN, 5)
    head(g, who, hc, d, 84 * k, eyes, mouth, brows, look, blush, t, soot)
    er = ik(shd, rt, ARM, ARM, d if rh is None else -d)
    g.line(shd, er, INK, 12 * k); g.line(er, rt, INK, 12 * k); g.disc(rt, 13 * k, SKIN, 5)
    if sweat: drops(g, hc, t, sweat, 100 * k)
    return dict(head=hc, sh=shd, hip=hip, lh=lt, rh=rt, feet=f, top=(hc[0], hc[1] - 84 * k))


# ------------------------------------------------------------------ run
def camera_crop(canvas, cx, cy, zoom):
    zoom = max(1.0, min(S, zoom)); vw, vh = W / zoom, H / zoom
    cx = min(max(cx, vw / 2), W - vw / 2); cy = min(max(cy, vh / 2), H - vh / 2)
    x0, y0 = (cx - vw / 2) * S, (cy - vh / 2) * S
    M = np.array([[zoom / S, 0, -x0 * zoom / S], [0, zoom / S, -y0 * zoom / S]], np.float32)
    return cv2.warpAffine(canvas, M, (W, H), flags=cv2.INTER_AREA if zoom < 1.2 else cv2.INTER_LINEAR)


def run(out, D, bg, draw, cam=None, audio=None, watermark="© Mahmoud Elkosif"):
    """Render the film. `python3 film.py OUT.mp4` or `python3 film.py OUT --stills 1,2.5,7`."""
    N = int(round(D * FPS))
    stills = [float(v) for v in sys.argv[sys.argv.index("--stills") + 1].split(",")] if "--stills" in sys.argv else None
    base = G(); bg(base)
    wm = None
    if watermark:
        from PIL import Image, ImageDraw, ImageFont
        im = Image.new("RGBA", (420, 60), (0, 0, 0, 0))
        fp = os.path.join(HERE, "..", "fonts", "Cairo-900.ttf")
        f = ImageFont.truetype(fp, 30) if os.path.exists(fp) else ImageFont.load_default()
        ImageDraw.Draw(im).text((410, 30), watermark, font=f, fill=(255, 255, 255, 255), anchor="rm", stroke_width=2, stroke_fill=(30, 30, 34, 255))
        wm = np.asarray(im)[..., [2, 1, 0, 3]].copy()
    enc = None
    if not stills:
        cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"]
        if audio: cmd += ["-i", audio, "-map", "0:v", "-map", "1:a", "-c:a", "copy"]
        cmd += ["-c:v", "libx264", "-profile:v", "high", "-crf", "17", "-preset", "slow", "-pix_fmt", "yuv420p", "-vf", "scale=out_color_matrix=bt709:out_range=tv",
                "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv", "-movflags", "+faststart", "-frames:v", str(N), out]
        enc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    want = set(int(round(v * FPS)) for v in stills) if stills else None
    for n in range(N):
        if want is not None and n not in want: continue
        t = n / FPS
        g = G(base.img.copy()); draw(g, t, n)
        cx, cy, z = cam(t) if cam else (W / 2, H / 2, 1.0)
        fr = camera_crop(g.img, cx, cy, z)
        if wm is not None:
            a = wm[..., 3:4].astype(np.float32) / 255 * 0.7; y0, x0 = H - 76, W - 440
            reg = fr[y0:y0 + 60, x0:x0 + 420].astype(np.float32)
            fr[y0:y0 + 60, x0:x0 + 420] = (reg * (1 - a) + wm[..., :3].astype(np.float32) * a).astype(np.uint8)
        if stills:
            os.makedirs(out + "_stills", exist_ok=True)
            cv2.imwrite(os.path.join(out + "_stills", f"s_{t:06.2f}.jpg"), cv2.resize(fr, (540, 960), interpolation=cv2.INTER_AREA), [cv2.IMWRITE_JPEG_QUALITY, 88])
        else: enc.stdin.write(fr.tobytes())
    if enc:
        enc.stdin.close(); rc = enc.wait()
        if rc: sys.exit(rc)
    elif stills:
        fs = sorted(os.listdir(out + "_stills")); ims = [cv2.imread(os.path.join(out + "_stills", f)) for f in fs]
        cv2.imwrite(out + "_sheet.jpg", np.hstack(ims))


# ------------------------------------------------------------------ audio
SR = 48000
_cache = {}


def _load(name):
    if name not in _cache:
        p = os.path.join(os.environ.get("TOON_SFX", os.path.join(HERE, "..", "sfx")), name + ".mp3")
        if not os.path.exists(p):  # effect not downloaded: stay silent instead of crashing
            print("toonkit: missing sfx", name, "(see sfx/README.md)", file=sys.stderr); _cache[name] = np.zeros(SR // 10); return _cache[name]
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
        a = np.frombuffer(raw, np.float32).astype(np.float64); pk = np.abs(a).max() or 1.0
        _cache[name] = a / pk
    return _cache[name]


class Mix:
    """Soundtrack builder. Real effects (./sfx/*.mp3, peak-normalised) + synth helpers.
    Effects: laugh_cartoon, laugh_cartoon2, laugh_male, giggle, giggle_kid, rain_light, rain_storm, thunder_close, thunder_mid,
    thunder_impact, explosion, wind_storm, whoosh, pour, splash_big, bubble, bubbles_deep, fill, river, birds_river, drips, pop, clink."""
    N = {"C3": 130.81, "A2": 110.0, "F2": 87.31, "G2": 98.0, "C4": 261.63, "D4": 293.66, "E4": 329.63, "F4": 349.23, "G4": 392.0, "A4": 440.0, "B4": 493.88,
         "C5": 523.25, "D5": 587.33, "E5": 659.25, "G5": 783.99}

    def __init__(self, D, seed=1):
        self.D = D; self.out = np.zeros(int(SR * D)); self.rng = np.random.default_rng(seed)

    def add(self, sig, t):
        i = int(max(0, t) * SR); n = min(len(sig), len(self.out) - i)
        if n > 0: self.out[i:i + n] += sig[:n]

    def sfx(self, name, t, gain=0.6, start=0.0, dur=None, fade=0.08, loop=False, rate=1.0):
        """Place a real effect at time t. dur trims (loop=True repeats it to fill dur); rate changes pitch/speed."""
        a = _load(name)[int(start * SR):]
        if rate != 1.0: a = np.interp(np.arange(0, len(a), rate), np.arange(len(a)), a)
        if dur is not None:
            n = int(dur * SR)
            if loop and len(a) < n: a = np.tile(a, n // len(a) + 1)
            a = a[:n].copy()
        else: a = a.copy()
        f = min(int(fade * SR), len(a) // 2)
        if f > 0: a[:f] *= np.linspace(0, 1, f); a[-f:] *= np.linspace(1, 0, f)
        self.add(a * gain, t)

    def tone(self, t, f, dur, amp=0.2, decay=6.0, f1=None, shape="sine"):
        tt = np.arange(int(SR * dur)) / SR; fr = f if f1 is None else f + (f1 - f) * tt / dur
        s = np.sin(2 * np.pi * np.cumsum(fr * np.ones_like(tt)) / SR)
        if shape == "square": s = np.sign(s)
        self.add(amp * s * np.exp(-decay * tt), t)

    def noise(self, t, dur, amp=0.3, smooth=8, decay=0.0):
        w = self.rng.normal(0, 1, int(SR * dur)); w = np.convolve(w, np.ones(smooth) / smooth, "same") * math.sqrt(smooth)
        tt = np.arange(len(w)) / SR; f = min(len(w) // 2, int(0.01 * SR))
        w[:f] *= np.linspace(0, 1, f); w[-f:] *= np.linspace(1, 0, f)
        self.add(amp * 0.3 * w * np.exp(-decay * tt), t)

    def pluck(self, t, f, dur=0.5, amp=0.3):
        n = int(SR / f); buf = self.rng.uniform(-1, 1, n); y = np.empty(int(SR * dur))
        for i in range(len(y)):
            y[i] = buf[i % n]; buf[i % n] = 0.497 * (buf[i % n] + buf[(i + 1) % n])
        self.add(y * amp * np.linspace(1, 0.2, len(y)), t)

    def tune(self, t0, t1, speed=1.0, gain=1.0, minor=False):
        """Light plucked backing tune between t0 and t1."""
        ch = [("C3", ["C4", "E4", "G4", "E4"]), ("A2", ["A4", "C5", "E4", "C5"]), ("F2", ["F4", "A4", "C5", "A4"]), ("G2", ["G4", "B4", "D5", "B4"])]
        if minor: ch = [("A2", ["A4", "C5", "E4", "C5"]), ("F2", ["F4", "A4", "C5", "A4"]), ("A2", ["E4", "A4", "C5", "A4"]), ("G2", ["G4", "B4", "D5", "B4"])]
        t, k = t0, 0
        while t < t1 - 0.05:
            b, arp = ch[(k // 8) % 4]
            if k % 4 == 0: self.tone(t, self.N[b], 0.45, 0.24 * gain, 5)
            self.pluck(t, self.N[arp[k % 4]], 0.45, 0.22 * gain)
            if k % 8 == 4: self.pluck(t, self.N[arp[1]] * 2, 0.3, 0.1 * gain)
            t += 0.25 / speed; k += 1

    # ready-made cartoon sounds
    def thump(self, t, amp=0.7, f=110): self.tone(t, f, 0.25, amp, 13, f * .55)
    def clang(self, t, amp=0.4): self.tone(t, 1300, 0.14, amp, 20); self.thump(t, amp * 1.4)
    def boing(self, t, amp=0.3): self.tone(t, 260, 0.5, amp, 5, 760)
    def ding(self, t, amp=0.22): self.tone(t, 1568, 0.9, amp, 4); self.tone(t + .08, 2093, 0.9, amp * .7, 4)
    def tada(self, t, amp=0.36):
        for i, n in enumerate(("C4", "E4", "G4", "C5", "E5")): self.pluck(t + i * 0.08, self.N[n], 1.4, amp)
    def rise(self, t, dur, f0=240, f1=1200, amp=0.09):
        tt = np.arange(int(SR * dur)) / SR
        self.add(amp * np.sin(2 * np.pi * np.cumsum(f0 + (f1 - f0) * (tt / dur) ** 1.6) / SR) * np.minimum(1, tt / 0.3) * (0.6 + 0.4 * np.sin(2 * np.pi * 14 * tt)), t)
    def slide_down(self, t, amp=0.18): self.tone(t, 900, 0.6, amp, 1.5, 250)
    def steps(self, t0, t1, every=0.33, amp=0.16):
        t = t0
        while t < t1: self.noise(t, 0.05, amp, 30, 20); t += every
    def chirps(self, t0, t1, every=1.2, amp=0.04):
        t = t0
        while t < t1:
            for i in range(int(self.rng.integers(2, 5))): self.tone(t + i * 0.09, self.rng.uniform(2600, 3600), 0.07, amp, 25, self.rng.uniform(3000, 4200))
            t += every * self.rng.uniform(0.7, 1.3)

    def save(self, path):
        o = self.out.copy(); f = int(SR * 0.4); o[-f:] *= np.linspace(1, 0, f); o = o / (np.abs(o).max() or 1) * 0.85
        tmp = path + ".wav"
        with wave.open(tmp, "wb") as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.stack([o, o], 1) * 32767).astype("<i2").tobytes())
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", "loudnorm=I=-14:TP=-2:LRA=11,alimiter=limit=0.45:level=false:attack=2:release=40,volume=1.5dB",
                        "-ar", str(SR), "-c:a", "aac", "-b:a", "320k", path], check=True)
        os.remove(tmp)
