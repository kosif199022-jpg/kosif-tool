#!/usr/bin/env python3
"""paperkit: «الورق الحي» Living Paper, a moving paper-cutout diorama style on top of toonkit (way D).

Every layer is drawn with ordinary toonkit calls on its own surface, turned into a paper cutout
(fibre texture, torn edge or white sticker border, gouache wash) and composed with 2.5D parallax,
drop shadows, depth of field, light wrap, bloom, a mood grade and film grain.

    import toonkit as tk, paperkit as pk
    sky  = pk.cutout(*pk.matte(draw_sky), edge=None, gouache=1.0)        # static plates: build once
    hill = pk.cutout(*pk.matte(draw_hills), edge="torn", gouache=1.0, seed=2)
    tp, idx = pk.twos(t)                                                  # characters on twos (12 poses/s)
    chars = pk.cutout(*pk.matte(lambda g: tk.fig(g, "cap", 500, 1500, t=tp)), edge="sticker", boil=idx)
    ch = pk.Chalk(); ch.arrow((300, 600), (520, 820), u); chalk = ch.render(idx)   # self-drawing notebook doodles
    frame = pk.compose([pk.L(sky, 0.0), pk.L(hill, 0.4), pk.L(chars, 1.0, shadow=pk.STICKER_SHADOW, wrap=0.5),
                        pk.L(chalk, 1.0, shadow=None)], cam=(cx, cy, zoom), mood="rain", dof=1.0)
    pk.run(out, D, frame_fn, audio=path, overlay=fn, prepare=fn)   # frame_fn(t, n) -> BGR 1080x1920 uint8

Layers are premultiplied BGRA uint8 canvases of toonkit size (CW x CH = 1.5 x world). `p` is the parallax/depth factor:
0 = infinitely far (sky), 1 = the character plane (follows the camera exactly, never blurred), > 1 = near foreground.
matte() renders a draw function twice (on black and on white) and solves for exact colour and alpha, so toonkit blends,
shades and anti-aliasing all become real transparency. compose() runs at output resolution; cost is about 0.6-1.2 s per
frame on one core, dominated by the per-pose character cutout (cached for the 2-3 frames of each pose).
"""
import math, os, subprocess, sys
import cv2, numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import toonkit as tk  # noqa: E402

W, H, S, CW, CH, FPS = tk.W, tk.H, tk.S, tk.CW, tk.CH, tk.FPS
F32 = np.float32
PAPER = (222, 236, 244)          # warm off-white paper (BGR)
ZMIN = 1.04                      # minimum zoom, leaves a margin so layers can slide (parallax) even in wide shots
STICKER_SHADOW = (16, 22, 13, 0.42)   # dx, dy (output px), blur sigma, strength
PLATE_SHADOW = (8, 12, 10, 0.30)


# ------------------------------------------------------------------ noise and textures (cached)
_C = {}


def noise(shape, scale, seed):
    """Smooth value noise in about [-1, 1]; `scale` = feature size in pixels."""
    k = ("n", shape, scale, seed)
    if k not in _C:
        rng = np.random.default_rng(seed)
        gh, gw = max(2, int(shape[0] / scale) + 3), max(2, int(shape[1] / scale) + 3)
        g = rng.standard_normal((gh, gw)).astype(F32)
        big = cv2.resize(g, (int(gw * scale), int(gh * scale)), interpolation=cv2.INTER_CUBIC)
        n = big[:shape[0], :shape[1]]
        _C[k] = np.ascontiguousarray(n / (float(n.std()) + 1e-6) * 0.5, dtype=F32)
    return _C[k]


def texture():
    """Paper texture for the 1.5x canvas: fine tooth, fibres and soft mottling, a multiplier around 1.0."""
    if "tex" not in _C:
        rng = np.random.default_rng(77)
        fine = cv2.GaussianBlur(rng.standard_normal((CH, CW)).astype(F32), (0, 0), 0.9)
        fine /= fine.std() + 1e-6
        fib = np.zeros((CH, CW), F32)
        for _ in range(16000):
            x, y = rng.uniform(0, CW), rng.uniform(0, CH); a = rng.uniform(0, math.pi); L = rng.uniform(6, 34)
            v = float(rng.choice((-1.0, 1.0)) * rng.uniform(0.4, 1.0))
            cv2.line(fib, (int(x), int(y)), (int(x + L * math.cos(a)), int(y + L * math.sin(a))), v, 1, cv2.LINE_AA)
        fib = cv2.GaussianBlur(fib, (0, 0), 0.6)
        low = noise((CH, CW), 140, 78) + 0.5 * noise((CH, CW), 40, 79)
        _C["tex"] = (1 + 0.030 * fine + 0.055 * fib + 0.035 * low).astype(F32)
    return _C["tex"]


def _disp(idx, amp=1.5, scale=36):
    """Line-boil displacement maps (3-drawing cycle like hand-drawn animation)."""
    k = ("d", idx % 3, amp, scale)
    if k not in _C:
        dx = noise((CH, CW), scale, 300 + idx % 3) * amp * 2; dy = noise((CH, CW), scale, 400 + idx % 3) * amp * 2
        _C[k] = (dx, dy)
    return _C[k]


def prewarm():
    """Build the shared caches once (call before forking render workers)."""
    texture(); chalk_tex()
    for i in range(3): _disp(i)
    for i in range(4): _grain(i)


# ------------------------------------------------------------------ layers
def twos(t, fps=12):
    """Pose time for animation 'on twos': returns (pose_time, pose_index). The camera stays at 30 fps."""
    i = int(math.floor(t * fps + 1e-6)); return i / fps, i


def matte(draw):
    """Draw with toonkit on black and on white, return (premultiplied colour float32 HxWx3, alpha float32 HxW)."""
    gb = tk.G(np.zeros((CH, CW, 3), np.uint8)); draw(gb)
    gw = tk.G(np.full((CH, CW, 3), 255, np.uint8)); draw(gw)
    b = gb.img.astype(F32)
    a = 1.0 - (gw.img.astype(F32) - b).mean(2) / 255.0
    np.clip(a, 0, 1, out=a)
    return b, a


def _bbox(a, pad):
    rows = np.flatnonzero(a.max(1) > 0.004)
    if not len(rows): return None
    cols = np.flatnonzero(a.max(0) > 0.004)
    return (max(0, rows[0] - pad), min(CH, rows[-1] + pad + 1), max(0, cols[0] - pad), min(CW, cols[-1] + pad + 1))


def _blur(x, s):
    if s <= 0.3: return x
    f = max(1, int(s / 3))
    if f == 1: return cv2.GaussianBlur(x, (0, 0), s)
    h, w = x.shape[:2]
    sm = cv2.resize(x, (max(1, w // f), max(1, h // f)), interpolation=cv2.INTER_AREA)
    sm = cv2.GaussianBlur(sm, (0, 0), s / f)
    return cv2.resize(sm, (w, h), interpolation=cv2.INTER_LINEAR)


def _gouache(col, aa, seed, amt, y0, x0):
    """Watercolour/gouache treatment: soft bleed, pigment pooling at shape edges, granulation and wash mottling."""
    h, w = aa.shape
    col = cv2.addWeighted(col, 0.55, cv2.GaussianBlur(col, (0, 0), 1.6), 0.45, 0)
    diff = np.abs(col - cv2.GaussianBlur(col, (0, 0), 7)).sum(2)
    d1 = np.clip(diff / 80.0, 0, 1)
    d2 = np.clip((aa - _blur(aa, 14)) * 2.6, 0, 1)
    L = col.mean(2) / 255.0
    gran = noise((CH, CW), 2.2, seed + 11)[y0:y0 + h, x0:x0 + w]
    wash = noise((CH, CW), 90, seed + 12)[y0:y0 + h, x0:x0 + w]
    k = (1 - amt * (0.20 * d1 + 0.30 * d2)) * (1 + amt * 0.16 * gran * (1.25 - L)) * (1 + amt * 0.09 * wash)
    col = col * k[..., None]
    hue = noise((CH, CW), 160, seed + 13)[y0:y0 + h, x0:x0 + w]
    col[..., 0] *= 1 + amt * 0.05 * hue; col[..., 2] *= 1 - amt * 0.05 * hue      # warm/cool pigment drift
    return col


def cutout(prem, a, edge="torn", seed=0, rim=None, tex=1.0, gouache=0.0, boil=None, boil_amp=1.5, bevel=None):
    """Turn a matte into a paper cutout layer (premultiplied BGRA uint8 canvas).
    edge: None (opaque plate, e.g. sky), "torn" (rough hand-torn edge with a thin white fibre rim),
          "sticker" (smooth scissor-cut white border, for characters and props).
    rim: border width in canvas px (default 4 torn / 14 sticker). gouache: 0..1 watercolour treatment (backgrounds).
    boil: pose index -> tiny hand-drawn wobble (3-drawing cycle). tex: paper texture strength.
    bevel: paper-thickness light (top-left edges lit, bottom-right edges shaded); default 0.5 sticker, 0.35 torn."""
    if bevel is None: bevel = {"torn": 0.35, "sticker": 0.5}.get(edge, 0.0)
    if rim is None: rim = {"torn": 5, "sticker": 14}.get(edge, 0)
    out = np.zeros((CH, CW, 4), np.uint8)
    bb = _bbox(a, int(rim * 2.5 + 16))
    if bb is None: return out
    y0, y1, x0, x1 = bb
    p, aa = prem[y0:y1, x0:x1], a[y0:y1, x0:x1].copy()
    if boil is not None:
        dx, dy = _disp(boil, boil_amp)
        gy, gx = np.mgrid[y0:y1, x0:x1].astype(F32)
        mx, my = (gx - x0 + dx[y0:y1, x0:x1]).astype(F32), (gy - y0 + dy[y0:y1, x0:x1]).astype(F32)
        p = cv2.remap(p, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        aa = cv2.remap(aa, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    # colour, extended outward (normalised convolution) so a torn edge may wander slightly outside the drawing
    safe = np.maximum(aa, 1e-3)[..., None]
    col = p / safe
    if edge == "torn":
        ext = _blur(p, 4) / np.maximum(_blur(aa, 4), 1e-3)[..., None]
        col = np.where((aa > 0.5)[..., None], col, ext)
    if gouache: col = _gouache(col, aa, seed, gouache, y0, x0)
    h, w = aa.shape
    if edge == "torn":
        n1 = noise((CH, CW), 9, seed + 1)[y0:y1, x0:x1] + 0.6 * noise((CH, CW), 2.5, seed + 2)[y0:y1, x0:x1]
        s = _blur(aa, 3.0)
        cm = np.clip((s - 0.55 - 0.22 * n1) * 7 + 0.5, 0, 1) * np.clip(s * 3, 0, 1)
        s2 = _blur(aa, rim * 0.8)
        n2 = noise((CH, CW), 5, seed + 3)[y0:y1, x0:x1] + 0.7 * noise((CH, CW), 1.6, seed + 4)[y0:y1, x0:x1]
        rm = np.clip((s2 - 0.22 - 0.12 * n2) * 9 + 0.5, 0, 1)
    elif edge == "sticker":
        cm = aa
        s2 = _blur(aa, rim * 0.62)
        n2 = noise((CH, CW), 60, seed + 5)[y0:y1, x0:x1]
        rm = np.clip((s2 - 0.10 - 0.025 * n2) * 14 + 0.5, 0, 1)
    else:
        cm = aa; rm = aa
    A = np.maximum(rm, cm)
    T = texture()[y0:y1, x0:x1]
    if tex != 1.0: T = 1 + (T - 1) * tex
    if bevel:
        hgt = _blur(A, 5.0)
        gx = cv2.Sobel(hgt, cv2.CV_32F, 1, 0, ksize=3); gy = cv2.Sobel(hgt, cv2.CV_32F, 0, 1, ksize=3)
        T = T * (1 + bevel * np.clip((gx + gy) * 1.6, -0.5, 0.5))     # light from the top-left
    pr = (col * cm[..., None] + np.array(PAPER, F32) * (A - cm)[..., None]) * T[..., None]
    pr = np.minimum(pr, A[..., None] * 255)
    out[y0:y1, x0:x1, :3] = np.clip(pr, 0, 255).astype(np.uint8)
    out[y0:y1, x0:x1, 3] = np.clip(A * 255, 0, 255).astype(np.uint8)
    return out


def paper(draw, edge="sticker", seed=0, **kw):
    """Shortcut: matte(draw) + cutout(...)."""
    return cutout(*matte(draw), edge=edge, seed=seed, **kw)


def fx(draw, soft=0.0):
    """A plain translucent effects layer (rain, heat lines, flashes): matte only, no paper."""
    b, a = matte(draw)
    if soft: b, a = _blur(b, soft), _blur(a, soft)
    out = np.zeros((CH, CW, 4), np.uint8)
    out[..., :3] = np.clip(b, 0, 255).astype(np.uint8); out[..., 3] = np.clip(a * 255, 0, 255).astype(np.uint8)
    return out


# ------------------------------------------------------------------ chalk: self-drawing notebook doodles
def chalk_tex():
    if "chalk" not in _C:
        n = noise((CH, CW), 1.3, 901) + 0.8 * noise((CH, CW), 4, 902) + 0.5 * noise((CH, CW), 1.0, 903)
        _C["chalk"] = np.clip(0.62 + 0.5 * n, 0.0, 1.0).astype(F32)
    return _C["chalk"]


def _cut(pts, u):
    """First fraction u of a polyline by arc length."""
    if u >= 1: return pts
    if u <= 0 or len(pts) < 2: return pts[:1]
    seg = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]
    tot, goal, acc = sum(seg), sum(seg) * u, 0.0
    out = [pts[0]]
    for (a, b), L in zip(zip(pts, pts[1:]), seg):
        if acc + L >= goal:
            k = (goal - acc) / max(L, 1e-6); out.append((a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k)); return out
        out.append(b); acc += L
    return out


class Chalk:
    """Collect hand-drawn chalk strokes in world coords, each with a draw-on progress u (0..1), then render().
    Strokes wobble like a hand (stable per stroke) plus a tiny boil per pose index."""

    def __init__(self, col=(250, 252, 255), th=9, seed=0):
        self.items, self.col, self.th, self.seed = [], col, th, seed

    def _hand(self, pts, sid, wob=3.0):
        rng = np.random.default_rng(1000 + sid + self.seed)
        ph, f = rng.uniform(0, 6.3, 2), rng.uniform(0.02, 0.05, 2)
        out = []
        for i, (x, y) in enumerate(pts):
            out.append((x + wob * math.sin(i * f[0] * 9 + ph[0]), y + wob * math.cos(i * f[1] * 9 + ph[1])))
        return out

    def path(self, pts, u, th=None, sid=None):
        if u <= 0: return
        sid = len(self.items) if sid is None else sid
        self.items.append((_cut(self._hand(list(pts), sid), min(1.0, u)), th or self.th))

    def line(self, a, b, u, th=None, bend=0.08, sid=None):
        mx, my = (a[0] + b[0]) / 2 - (b[1] - a[1]) * bend, (a[1] + b[1]) / 2 + (b[0] - a[0]) * bend
        self.path(tk.bezier(a, (mx, my), b, 28), u, th, sid)

    def arrow(self, a, b, u, th=None, bend=0.12, head=34):
        """Curved arrow drawn from a to b; the head flicks on in the last 25 % of u."""
        mx, my = (a[0] + b[0]) / 2 - (b[1] - a[1]) * bend, (a[1] + b[1]) / 2 + (b[0] - a[0]) * bend
        pts = tk.bezier(a, (mx, my), b, 28)
        self.path(pts, u / 0.75, th)
        if u > 0.75:
            q = pts[-4]; ang = math.atan2(b[1] - q[1], b[0] - q[0]); k = (u - 0.75) / 0.25
            for s in (1, -1):
                self.path([b, (b[0] - head * math.cos(ang + s * 0.5), b[1] - head * math.sin(ang + s * 0.5))], k, th)

    def circle(self, c, r, u, th=None, start=-100, ry=None, over=40):
        """Loose hand circle with an overshoot, like circling something on a notebook."""
        ry = ry or r
        pts = [(c[0] + r * (1 + 0.05 * math.sin(a * 3)) * math.cos(math.radians(a)), c[1] + ry * (1 + 0.05 * math.sin(a * 3)) * math.sin(math.radians(a)))
               for a in np.linspace(start, start + 360 + over, 60)]
        self.path(pts, u, th)

    def drop(self, c, s, u, th=None):
        pts = [(c[0], c[1] - s)] + [(c[0] + s * 0.62 * math.cos(a), c[1] + s * 0.3 + s * 0.62 * math.sin(a)) for a in np.linspace(-0.2, math.pi + 0.2, 16)] + [(c[0], c[1] - s)]
        self.path(pts, u, th)

    def wave(self, a, b, u, amp=12, n=3, th=None):
        pts = [(a[0] + (b[0] - a[0]) * v, a[1] + (b[1] - a[1]) * v + amp * math.sin(v * n * math.tau)) for v in np.linspace(0, 1, 40)]
        self.path(pts, u, th)

    def star(self, c, r, u, th=None):
        self.path([(c[0] + (r if j % 2 == 0 else r * .42) * math.cos(j * math.pi / 5 - math.pi / 2), c[1] + (r if j % 2 == 0 else r * .42) * math.sin(j * math.pi / 5 - math.pi / 2)) for j in range(11)], u, th)

    def render(self, boil=0):
        """Premultiplied BGRA canvas: broken chalk strokes with a soft dark halo so they read on light skies too."""
        out = np.zeros((CH, CW, 4), np.uint8)
        if not self.items: return out
        rng = np.random.default_rng(5000 + boil % 3)
        m = np.zeros((CH, CW), np.uint8)
        for pts, th in self.items:
            if len(pts) < 2: continue
            j = rng.normal(0, 1.1, (len(pts), 2))
            arr = np.round((np.array(pts) + j) * S).astype(np.int32)
            cv2.polylines(m, [arr], False, 255, max(1, int(th * S)), cv2.LINE_AA)
        bb = _bbox(m.astype(F32), 30)
        if bb is None: return out
        y0, y1, x0, x1 = bb
        mm = m[y0:y1, x0:x1].astype(F32) / 255
        ct = chalk_tex()[y0:y1, x0:x1]
        a = mm * (0.55 + 0.45 * ct) * np.clip(ct * 2.2, 0, 1)
        halo = _blur(mm, 6) * 0.45
        A = np.maximum(a, halo)
        col = np.array(self.col, F32)[None, None] * a[..., None] + np.array((40, 34, 30), F32)[None, None] * (A - a)[..., None]
        out[y0:y1, x0:x1, :3] = np.clip(col, 0, 255).astype(np.uint8)
        out[y0:y1, x0:x1, 3] = np.clip(A * 255, 0, 255).astype(np.uint8)
        return out


# ------------------------------------------------------------------ composition
def L(img, p=1.0, shadow=PLATE_SHADOW, wrap=0.0, soft=0.0, opacity=1.0, focus=False):
    """A layer for compose(): img = BGRA premult canvas, p = depth (0 sky .. 1 characters .. >1 near).
    shadow = (dx, dy, sigma, strength) cast on what is behind, or None. wrap = light-wrap amount (characters ~0.5).
    soft = extra blur in output px. focus=True keeps it sharp whatever the depth of field."""
    return dict(img=img, p=p, shadow=shadow, wrap=wrap, soft=soft, opacity=opacity, focus=focus)


def cam_matrix(cx, cy, z, p):
    """Affine from canvas pixels to screen for a layer of depth p."""
    z = max(ZMIN, z)
    zl = max(1.0, z ** p) * (1 + 0.05 * abs(1 - p)) if p <= 1 else z ** p
    ox, oy = W / 2 + (cx - W / 2) * p, H / 2 + (cy - H / 2) * p
    vw, vh = W / zl, H / zl
    if p <= 1:
        ox = min(max(ox, vw / 2), W - vw / 2); oy = min(max(oy, vh / 2), H - vh / 2)
    x0, y0 = (ox - vw / 2) * S, (oy - vh / 2) * S
    return np.array([[zl / S, 0, -x0 * zl / S], [0, zl / S, -y0 * zl / S]], F32)


def project(pt, cam, p=1.0):
    """World point -> screen point for a layer of depth p."""
    M = cam_matrix(*cam, p); x, y = pt[0] * S, pt[1] * S
    return (M[0, 0] * x + M[0, 2], M[1, 1] * y + M[1, 2])


def _q(x):
    return cv2.resize(x, (W // 4, H // 4), interpolation=cv2.INTER_AREA)


def _up(x):
    return cv2.resize(x, (W, H), interpolation=cv2.INTER_LINEAR)


MOODS = {  # lift (BGR 0..255), gain, gamma, saturation, bloom (threshold, amount, tint BGR), vignette
    "neutral": dict(lift=(6, 6, 8), gain=(252, 252, 255), gamma=(1.0, 1.0, 1.0), sat=1.05, bloom=(0.88, 0.30, (200, 230, 255)), vig=0.22),
    "rain": dict(lift=(30, 20, 14), gain=(246, 240, 234), gamma=(0.94, 1.0, 1.06), sat=0.86, bloom=(0.88, 0.20, (255, 240, 220)), vig=0.30),
    "desert": dict(lift=(14, 14, 20), gain=(226, 244, 255), gamma=(1.14, 1.02, 0.96), sat=1.12, bloom=(0.90, 0.45, (150, 220, 255)), vig=0.24),
    "sunset": dict(lift=(30, 14, 26), gain=(206, 230, 255), gamma=(1.2, 1.05, 0.95), sat=1.1, bloom=(0.86, 0.55, (120, 190, 255)), vig=0.34),
    "dawn": dict(lift=(18, 18, 30), gain=(226, 244, 255), gamma=(1.08, 1.0, 0.94), sat=1.06, bloom=(0.86, 0.55, (140, 210, 255)), vig=0.28),
}


def _lut(mood):
    k = ("lut", mood)
    if k not in _C:
        m = MOODS[mood]; x = np.arange(256, dtype=F32) / 255
        lut = np.stack([m["lift"][c] + (m["gain"][c] - m["lift"][c]) * x ** m["gamma"][c] for c in range(3)], 1)
        _C[k] = np.clip(lut, 0, 255).astype(np.uint8).reshape(256, 1, 3)
    return _C[k]


def _vig(amt):
    k = ("vig", amt)
    if k not in _C:
        yy, xx = np.mgrid[0:H, 0:W].astype(F32)
        d = np.hypot((xx - W / 2) / (W * 0.62), (yy - H * 0.47) / (H * 0.62))
        _C[k] = (1 - amt * np.clip(d - 0.45, 0, 1) ** 1.6)[..., None].astype(F32)
    return _C[k]


def _grain(i):
    k = ("grain", i % 4)
    if k not in _C:
        rng = np.random.default_rng(600 + i % 4)
        g = cv2.GaussianBlur(rng.standard_normal((H, W)).astype(F32), (0, 0), 0.7) * 7.0
        _C[k] = g[..., None]
    return _C[k]


def compose(layers, cam, mood="neutral", dof=0.0, light=None, n=0):
    """Compose layers back to front -> BGR uint8 frame (W x H).
    cam = (cx, cy, zoom) in world units (as toonkit). dof = 0..1.5 depth-of-field strength (close-ups ~1).
    light = (x, y, radius, (B, G, R), amount) screen-space warm key light, or None."""
    cx, cy, z = cam
    out = None
    for Ly in layers:
        img = Ly["img"]
        if img is None: continue
        w = cv2.warpAffine(img, cam_matrix(cx, cy, z, Ly["p"]), (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
        p = Ly["p"]
        sig = Ly["soft"]
        if not Ly["focus"]:
            sig += dof * 20 * (1 - p) if p < 1 else (0.6 + dof) * 26 * (p - 1)
        f = w.astype(F32)
        if sig > 0.8: f = _blur(f, sig)
        if Ly["opacity"] != 1: f *= Ly["opacity"]
        prem, a = f[..., :3], f[..., 3] / 255
        if out is None:
            out = prem + (1 - a)[..., None] * np.array(PAPER, F32); continue
        if Ly["shadow"]:
            dx, dy, sg, amt = Ly["shadow"]
            zz = max(ZMIN, z)
            aq = cv2.warpAffine(_q(a), np.array([[1, 0, dx * zz / 4], [0, 1, dy * zz / 4]], F32), (W // 4, H // 4))
            sh = _up(cv2.GaussianBlur(aq, (0, 0), max(0.6, sg * zz / 4)))
            out *= (1 - amt * sh)[..., None]
        if Ly["wrap"]:
            bq = cv2.GaussianBlur(_q(out), (0, 0), 7)
            aq = cv2.GaussianBlur(_q(a), (0, 0), 2.5)
            k = (Ly["wrap"] * 0.6 * _up(np.clip(1 - aq, 0, 1)) * a)[..., None]
            prem = prem + k * (_up(bq) * a[..., None] - prem)          # background light bleeds over the cutout's edge
        out = out * (1 - a)[..., None] + prem
    m = MOODS[mood]
    lum = out @ np.array([0.114, 0.587, 0.299], F32)
    out = lum[..., None] + m["sat"] * (out - lum[..., None])
    if light:
        lx, ly, lr, lc, la = light
        k = ("lm", int(lx) // 8, int(ly) // 8, int(lr) // 8)
        if k not in _C:
            if len(_C) > 400: [_C.pop(q) for q in [q for q in _C if q[0] == "lm"]]
            yy, xx = np.mgrid[0:H // 4, 0:W // 4].astype(F32)
            _C[k] = _up(np.clip(1 - np.hypot(xx - lx / 4, yy - ly / 4) / (lr / 4), 0, 1) ** 2)
        lm = _C[k]
        out = out * (1 + la * lm[..., None] * (np.array(lc, F32) / 255 - 0.35))
    thr, ba, bt = m["bloom"]
    q = _q(out) / 255
    bl = np.clip(q @ np.array([0.114, 0.587, 0.299], F32) - thr, 0, None) / (1 - thr)
    bl *= bl
    bl = cv2.GaussianBlur(bl, (0, 0), 10) + 0.6 * cv2.GaussianBlur(bl, (0, 0), 28)
    out += _up(bl)[..., None] * (ba * np.array(bt, F32))
    out *= _vig(m["vig"])
    out += _grain(n // 2 if n else 0)
    fr = np.clip(out, 0, 255).astype(np.uint8)
    return cv2.LUT(fr, _lut(mood))


# ------------------------------------------------------------------ run
def _wm(text):
    from PIL import Image, ImageDraw, ImageFont
    im = Image.new("RGBA", (420, 60), (0, 0, 0, 0))
    fp = os.path.join(HERE, "..", "fonts", "Cairo-900.ttf")
    f = ImageFont.truetype(fp, 30) if os.path.exists(fp) else ImageFont.load_default()
    ImageDraw.Draw(im).text((410, 30), text, font=f, fill=(255, 255, 255, 255), anchor="rm", stroke_width=2, stroke_fill=(30, 30, 34, 255))
    return np.asarray(im)[..., [2, 1, 0, 3]].copy()


_JOB = {}


def _render_one(n):
    t = n / FPS
    fr = _JOB["frame"](t, n)
    if _JOB["overlay"]: fr = _JOB["overlay"](fr, t)
    wm = _JOB["wm"]
    if wm is not None:
        a = wm[..., 3:4].astype(F32) / 255 * 0.7; y0, x0 = H - 76, W - 440
        reg = fr[y0:y0 + 60, x0:x0 + 420].astype(F32)
        fr[y0:y0 + 60, x0:x0 + 420] = (reg * (1 - a) + wm[..., :3].astype(F32) * a).astype(np.uint8)
    return fr.tobytes() if _JOB["raw"] else fr


def run(out, D, frame, audio=None, overlay=None, prepare=None, watermark="© Mahmoud Elkosif", workers=None, stills=None):
    """Render: `python3 film.py OUT.mp4` or `python3 film.py OUT --stills 1,5.5` (-> OUT_sheet.jpg, side by side).
    frame(t, n) -> BGR uint8 frame; overlay(frame, t) -> frame in screen space (captions); prepare() builds caches
    before the worker processes fork. Exact frame count via -frames:v; never -shortest."""
    import time
    N = int(round(D * FPS))
    if stills is None and "--stills" in sys.argv:
        stills = [float(v) for v in sys.argv[sys.argv.index("--stills") + 1].split(",")]
    t0 = time.time()
    prewarm()
    if prepare: prepare()
    _JOB.update(frame=frame, overlay=overlay, wm=_wm(watermark) if watermark else None, raw=not stills)
    print(f"paperkit: caches ready in {time.time() - t0:.1f}s", file=sys.stderr)
    if stills:
        ims = []
        for v in stills:
            n = int(round(v * FPS)); fr = _render_one(n); ims.append(fr)
            cv2.imwrite(f"{out}_{v:05.2f}.jpg", fr, [cv2.IMWRITE_JPEG_QUALITY, 92])
        cv2.imwrite(out + "_sheet.jpg", np.hstack([cv2.resize(i, (540, 960), interpolation=cv2.INTER_AREA) for i in ims]), [cv2.IMWRITE_JPEG_QUALITY, 92])
        print(f"paperkit: {len(stills)} stills in {time.time() - t0:.1f}s", file=sys.stderr)
        return
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"]
    if audio: cmd += ["-i", audio, "-map", "0:v", "-map", "1:a", "-c:a", "copy"]
    cmd += ["-c:v", "libx264", "-profile:v", "high", "-crf", "17", "-preset", "slow", "-pix_fmt", "yuv420p", "-vf", "scale=out_color_matrix=bt709:out_range=tv",
            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv", "-movflags", "+faststart", "-frames:v", str(N), out]
    enc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    workers = workers or max(1, (os.cpu_count() or 2) - 1)
    t1 = time.time()
    if workers > 1:
        import multiprocessing as mp
        with mp.get_context("fork").Pool(workers) as pool:
            for i, b in enumerate(pool.imap(_render_one, range(N), chunksize=6)):
                enc.stdin.write(b)
                if i % 30 == 29: print(f"paperkit: frame {i + 1}/{N}  {(time.time() - t1) / (i + 1):.2f}s/frame wall", file=sys.stderr, flush=True)
    else:
        for i in range(N):
            enc.stdin.write(_render_one(i))
            if i % 30 == 29: print(f"paperkit: frame {i + 1}/{N}  {(time.time() - t1) / (i + 1):.2f}s/frame", file=sys.stderr, flush=True)
    enc.stdin.close(); rc = enc.wait()
    print(f"paperkit: done in {time.time() - t0:.0f}s", file=sys.stderr)
    if rc: sys.exit(rc)
