"""KOSIF Studio renderer.

A picture here is a *program*: an ordered list of steps made of vector shapes, gradients, light and particles.
`render()` runs that program at any size, so enlarging never loses quality - the picture is simply drawn again,
bigger. Each step also says how a painter would lay it down (sweep, grow, rise, sparkle); the studio uses that to
reveal the changed pixels one by one, so the picture forms as if it were being drawn.

All coordinates are scene units on a 1200 x 800 sheet; `scale` maps them to pixels.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from typing import Callable, Iterator

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W0, H0 = 1200, 800
Pt = tuple[float, float]
Shape = list[list[Pt]]          # a union of polygons, drawn in order; a Hole polygon cuts out what came before


class Hole(list):
    """A polygon that erases (a ring's middle, the inside of a letter). Draw it after the shape it cuts."""


# ── colour and paint ─────────────────────────────────────────────────────────────────────────────────────────
def rgba(c) -> np.ndarray:
    """'#rgb', '#rrggbb', '#rrggbbaa' or a 3/4-tuple of 0..1 floats -> r, g, b, a (0..1)."""
    if isinstance(c, str):
        c = c.strip().lstrip("#")
        if len(c) in (3, 4):
            c = "".join(ch * 2 for ch in c)
        v = [int(c[i:i + 2], 16) / 255 for i in range(0, len(c), 2)]
        return np.array(v + [1.0] * (4 - len(v)), np.float32)
    v = list(np.asarray(c, np.float32))
    return np.array(v + [1.0] * (4 - len(v)), np.float32)


def rgb(c) -> np.ndarray:
    return rgba(c)[:3]


def lin(a: Pt, b: Pt, stops) -> tuple:
    """Linear gradient from a to b; stops = [(0..1, colour), ...]."""
    return ("lin", a, b, stops)


def rad(c: Pt, r: float, stops) -> tuple:
    """Radial gradient around c with radius r."""
    return ("rad", c, r, stops)


# ── geometry ────────────────────────────────────────────────────────────────────────────────────────────────
def catmull(pts, n: int = 10, closed: bool = False) -> list[Pt]:
    """Smooth curve through the points (Catmull-Rom), n samples per segment."""
    P = [tuple(p) for p in pts]
    if len(P) < 2:
        return P
    P = ([P[-1]] + P + [P[0], P[1]]) if closed else ([P[0]] + P + [P[-1]])
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * (2 * p1[j] + (p2[j] - p0[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2
                                    + (3 * p1[j] - p0[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    if not closed:
        out.append(P[-2])
    return out


def _bez(ps: list[Pt], n: int) -> list[Pt]:
    out = []
    for k in range(1, n + 1):
        t = k / n
        q = list(ps)
        while len(q) > 1:
            q = [(a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t) for a, b in zip(q, q[1:])]
        out.append(q[0])
    return out


def path(d: str, n: int = 14) -> Shape:
    """The full SVG path language: M L H V C S Q T A Z, absolute and relative, arcs included.
    Returns one polygon per subpath (open subpaths too; strokes use them, fills close them)."""
    i, L = 0, len(d)

    def skip():
        nonlocal i
        while i < L and (d[i].isspace() or d[i] == ","):
            i += 1

    def number() -> float:
        nonlocal i
        skip()
        m = _NUM.match(d, i)
        if not m:
            raise ValueError(f"path: number expected at {i}: {d[i:i + 12]!r}")
        i = m.end()
        return float(m.group(0))

    def flag() -> int:                      # arc flags may be glued: "a10 10 0 01 5 5"
        nonlocal i
        skip()
        c = d[i]
        i += 1
        return 1 if c == "1" else 0

    def more() -> bool:
        skip()
        return i < L and (d[i].isdigit() or d[i] in "+-.")
    polys: Shape = []
    pts: list[Pt] = []
    cur = start = (0.0, 0.0)
    last_c = last_q = None
    cmd = ""
    while True:
        skip()
        if i >= L:
            break
        if d[i].isalpha():
            cmd = d[i]
            i += 1
        elif not cmd:
            raise ValueError("path must start with a command")
        c, rel = cmd.upper(), cmd.islower()
        ox, oy = cur if rel else (0.0, 0.0)
        if c == "Z":
            if len(pts) > 1:
                polys.append(pts)
            pts, cur, last_c, last_q = [], start, None, None
            continue
        if c == "M":
            if len(pts) > 1:
                polys.append(pts)
            cur = start = (ox + number(), oy + number())
            pts = [cur]
            cmd = "l" if rel else "L"
            last_c = last_q = None
        elif c == "L":
            cur = (ox + number(), oy + number())
            pts.append(cur)
        elif c == "H":
            cur = ((cur[0] if rel else 0) + number(), cur[1])
            pts.append(cur)
        elif c == "V":
            cur = (cur[0], (cur[1] if rel else 0) + number())
            pts.append(cur)
        elif c in "CS":
            if c == "C":
                p1 = (ox + number(), oy + number())
            else:                                            # smooth: mirror the last control point
                p1 = (2 * cur[0] - last_c[0], 2 * cur[1] - last_c[1]) if last_c else cur
            p2, p3 = (ox + number(), oy + number()), (ox + number(), oy + number())
            pts += _bez([cur, p1, p2, p3], n)
            cur, last_c = p3, p2
            last_q = None
            if not more():
                continue
            continue
        elif c in "QT":
            if c == "Q":
                p1 = (ox + number(), oy + number())
            else:
                p1 = (2 * cur[0] - last_q[0], 2 * cur[1] - last_q[1]) if last_q else cur
            p2 = (ox + number(), oy + number())
            pts += _bez([cur, p1, p2], n)
            cur, last_q = p2, p1
            last_c = None
            continue
        elif c == "A":
            rx, ry, phi = number(), number(), number()
            fa, fs = flag(), flag()
            p1 = (ox + number(), oy + number())
            pts += _arc(cur, rx, ry, math.radians(phi), fa, fs, p1)
            cur = p1
        else:
            raise ValueError(f"path: unsupported command {cmd!r}")
        last_c = last_q = None
    if len(pts) > 1:
        polys.append(pts)
    return polys


_NUM = re.compile(r"[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?")


def _arc(p0: Pt, rx: float, ry: float, phi: float, fa: int, fs: int, p1: Pt) -> list[Pt]:
    """SVG elliptical arc (endpoint form) as points, per the SVG spec's centre conversion."""
    if p0 == p1:
        return []
    rx, ry = abs(rx), abs(ry)
    if rx < 1e-9 or ry < 1e-9:
        return [p1]
    co, si = math.cos(phi), math.sin(phi)
    dx, dy = (p0[0] - p1[0]) / 2, (p0[1] - p1[1]) / 2
    x1, y1 = co * dx + si * dy, -si * dx + co * dy
    lam = x1 * x1 / (rx * rx) + y1 * y1 / (ry * ry)
    if lam > 1:
        rx, ry = rx * math.sqrt(lam), ry * math.sqrt(lam)
    num = rx * rx * ry * ry - rx * rx * y1 * y1 - ry * ry * x1 * x1
    den = rx * rx * y1 * y1 + ry * ry * x1 * x1
    k = math.sqrt(max(0.0, num / den)) * (-1 if fa == fs else 1)
    cxp, cyp = k * rx * y1 / ry, -k * ry * x1 / rx
    cx = co * cxp - si * cyp + (p0[0] + p1[0]) / 2
    cy = si * cxp + co * cyp + (p0[1] + p1[1]) / 2

    def ang(ux, uy, vx, vy):
        return math.atan2(ux * vy - uy * vx, ux * vx + uy * vy)
    t1 = ang(1, 0, (x1 - cxp) / rx, (y1 - cyp) / ry)
    dt = ang((x1 - cxp) / rx, (y1 - cyp) / ry, (-x1 - cxp) / rx, (-y1 - cyp) / ry)
    if not fs and dt > 0:
        dt -= 2 * math.pi
    elif fs and dt < 0:
        dt += 2 * math.pi
    n = max(4, int(abs(dt) / (2 * math.pi) * 64))
    out = []
    for j in range(1, n + 1):
        t = t1 + dt * j / n
        out.append((cx + rx * co * math.cos(t) - ry * si * math.sin(t), cy + rx * si * math.cos(t) + ry * co * math.sin(t)))
    out[-1] = p1
    return out


def compound(polys: Shape) -> Shape:
    """Several subpaths filled even-odd as one shape (letters with counters, a ring drawn as two circles)."""
    polys = [p for p in polys if len(p) >= 3]
    if len(polys) < 2:
        return polys
    a = polys[0][0]
    one: list[Pt] = []
    for p in polys:                     # bridge every subpath to one anchor; bridges cancel out under even-odd
        one += list(p) + [p[0], a]
    return [one]


def stroke(polys: Shape, width: float, closed: bool = False) -> Shape:
    """Outline of lines of the given width, round joins and caps (a union of quads and discs)."""
    r = width / 2
    out: Shape = []
    for p in polys:
        q = list(p) + ([p[0]] if closed and len(p) > 2 else [])
        for (x0, y0), (x1, y1) in zip(q, q[1:]):
            dx, dy = x1 - x0, y1 - y0
            dl = math.hypot(dx, dy)
            if dl < 1e-9:
                continue
            nx, ny = -dy / dl * r, dx / dl * r
            out.append([(x0 + nx, y0 + ny), (x1 + nx, y1 + ny), (x1 - nx, y1 - ny), (x0 - nx, y0 - ny)])
        for x, y in q:
            out += ellipse(x, y, r, r, n=12 if r < 3 else 24)
    return out


def poly(pts) -> Shape:
    return [[tuple(p) for p in pts]]


def rect(x, y, w, h) -> Shape:
    return [[(x, y), (x + w, y), (x + w, y + h), (x, y + h)]]


def ellipse(cx, cy, rx, ry=None, rot: float = 0.0, n: int = 48) -> Shape:
    ry = rx if ry is None else ry
    c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    pts = []
    for k in range(n):
        a = 2 * math.pi * k / n
        x, y = rx * math.cos(a), ry * math.sin(a)
        pts.append((cx + x * c - y * s, cy + x * s + y * c))
    return [pts]


def dots(items) -> Shape:
    """[(x, y, r), ...] -> many small discs."""
    out: Shape = []
    for x, y, r in items:
        out += ellipse(x, y, r, r, n=10 if r < 3 else 20)
    return out


def tube(spine, radii, n: int = 8) -> Shape:
    """A limb, tail, horn or flame: a smooth spine with a radius at each spine point. Built as a union of quads and
    discs, so tight bends never punch holes in it."""
    pts = catmull(spine, n)
    m = len(pts)
    r = np.interp(np.linspace(0, len(radii) - 1, m), np.arange(len(radii)), radii)
    L, R = [], []
    for i, (x, y) in enumerate(pts):
        a, b = pts[max(i - 1, 0)], pts[min(i + 1, m - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        d = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / d, dx / d
        L.append((x + nx * r[i], y + ny * r[i]))
        R.append((x - nx * r[i], y - ny * r[i]))
    out: Shape = [[L[i], L[i + 1], R[i + 1], R[i]] for i in range(m - 1)]
    for i in list(range(0, m, max(1, n // 2))) + [m - 1]:
        if r[i] > 0.6:
            out += ellipse(pts[i][0], pts[i][1], r[i], r[i], n=16 if r[i] < 6 else 28)
    return out


def translate(shape: Shape, dx: float, dy: float) -> Shape:
    return [(Hole if isinstance(p, Hole) else list)((x + dx, y + dy) for x, y in p) for p in shape]


def union(*shapes: Shape) -> Shape:
    return [p for s in shapes for p in s]


# ── the canvas the program draws on ─────────────────────────────────────────────────────────────────────────
class Ctx:
    def __init__(self, scale: float, ss: int = 3, paper: str = "#000000"):
        self.scale, self.ss = scale, ss
        self.W, self.H = round(W0 * scale), round(H0 * scale)
        self.canvas = np.empty((self.H, self.W, 3), np.float32)
        self.canvas[:] = rgb(paper)

    def bbox(self, shape: Shape, pad: float):
        xs = [p[0] for q in shape for p in q]
        ys = [p[1] for q in shape for p in q]
        if not xs:
            return None
        s = self.scale
        x0, y0 = max(0, math.floor(min(xs) * s - pad)), max(0, math.floor(min(ys) * s - pad))
        x1, y1 = min(self.W, math.ceil(max(xs) * s + pad) + 1), min(self.H, math.ceil(max(ys) * s + pad) + 1)
        return (x0, y0, x1, y1) if x1 > x0 and y1 > y0 else None

    def mask(self, shape: Shape, box) -> np.ndarray:
        """Antialiased coverage of the shape inside box (supersampled ss x ss, then box-filtered)."""
        x0, y0, x1, y1 = box
        ss, k = self.ss, self.scale * self.ss
        im = Image.new("L", ((x1 - x0) * ss, (y1 - y0) * ss), 0)
        dr = ImageDraw.Draw(im)
        for q in shape:
            if len(q) >= 3:
                dr.polygon([(x * k - x0 * ss, y * k - y0 * ss) for x, y in q], fill=0 if isinstance(q, Hole) else 255)
        if ss > 1:
            im = im.reduce(ss)
        return np.asarray(im, np.float32) / 255

    def paint(self, paint, box) -> np.ndarray:
        """Colour (r, g, b, a) for every pixel of box: a flat colour, or a gradient whose stops may be see-through."""
        if not isinstance(paint, tuple) or isinstance(paint[0], (int, float)):
            return rgba(paint)[None, None, :]
        x0, y0, x1, y1 = box
        s = self.scale
        X, Y = np.meshgrid((np.arange(x0, x1, dtype=np.float32) + .5) / s,
                           (np.arange(y0, y1, dtype=np.float32) + .5) / s)
        if paint[0] == "lin":
            (ax, ay), (bx, by), stops = paint[1], paint[2], paint[3]
            dx, dy = bx - ax, by - ay
            t = ((X - ax) * dx + (Y - ay) * dy) / (dx * dx + dy * dy)
        else:
            (cx, cy), r, stops = paint[1], paint[2], paint[3]
            t = np.hypot(X - cx, Y - cy) / r
        t = np.clip(t, 0, 1)
        pos = [p for p, _ in stops]
        cols = np.array([rgba(c) for _, c in stops])
        return np.stack([np.interp(t, pos, cols[:, j]) for j in range(4)], -1).astype(np.float32)

    def blend(self, box, m: np.ndarray, col: np.ndarray, alpha: float, mode: str):
        x0, y0, x1, y1 = box
        reg = self.canvas[y0:y1, x0:x1]
        if col.shape[-1] == 4:                      # see-through colour or gradient stop
            m = m * col[..., 3]
            col = col[..., :3]
        a = (m * alpha)[..., None]
        if mode == "normal":
            reg *= 1 - a
            reg += col * a
        elif mode == "add":
            reg += col * a
        elif mode == "screen":      # a + b - ab, written so light above 1.0 (glows) is never clipped
            reg += col * a * (1 - np.minimum(reg, 1))
        elif mode == "multiply":
            reg *= 1 - a + a * col
        else:
            raise ValueError(mode)


def _blur(a: np.ndarray, px: float) -> np.ndarray:
    if px < 0.3:
        return a
    im = Image.fromarray(np.clip(a * 255 + .5, 0, 255).astype(np.uint8))
    return np.asarray(im.filter(ImageFilter.GaussianBlur(px)), np.float32) / 255


# ── operations (each returns a function of the canvas) ────────────────────────────────────────────────────
Op = Callable[[Ctx], None]


def fill(shape: Shape, paint, alpha: float = 1.0, blur: float = 0.0, mode: str = "normal") -> Op:
    """Fill a shape with a colour or gradient; blur softens it (scene units), mode = normal/add/screen/multiply."""
    def op(ctx: Ctx):
        bp = blur * ctx.scale
        box = ctx.bbox(shape, 3 * bp + 2)
        if box:
            ctx.blend(box, _blur(ctx.mask(shape, box), bp), ctx.paint(paint, box), alpha, mode)
    return op


def glow(shape: Shape, colour, radius: float, alpha: float = 1.0) -> Op:
    """Light spilling from a shape: an additive, blurred fill."""
    return fill(shape, colour, alpha, radius, "add")


def rim(shape: Shape, toward: Pt, width: float, colour, alpha: float = 1.0, soft: float = 0.6,
        mode: str = "add") -> Op:
    """Rim light: the edge of the shape that faces a light in direction `toward` gets a thin band of its colour."""
    d = math.hypot(*toward) or 1.0
    dx, dy = toward[0] / d * width, toward[1] / d * width
    away = translate(shape, -dx, -dy)

    def op(ctx: Ctx):
        box = ctx.bbox(shape, 2)
        if box:
            m = ctx.mask(shape, box)
            edge = _blur(m * (1 - ctx.mask(away, box)), soft * ctx.scale) * m
            ctx.blend(box, edge, ctx.paint(colour, box), alpha, mode)
    return op


_FONT_FILES = {("sans", False): ["segoeui.ttf", "arial.ttf", "tahoma.ttf"],
               ("sans", True): ["segoeuib.ttf", "arialbd.ttf", "tahomabd.ttf"],
               ("serif", False): ["times.ttf", "georgia.ttf"], ("serif", True): ["timesbd.ttf", "georgiab.ttf"],
               ("mono", False): ["consola.ttf", "cour.ttf"], ("mono", True): ["consolab.ttf", "courbd.ttf"]}


def _font(family: str, size: int, bold: bool):
    import os
    from PIL import ImageFont
    fam = "serif" if "serif" in family and "sans" not in family else "mono" if "mono" in family else "sans"
    for name in _FONT_FILES[(fam, bold)]:
        try:
            return ImageFont.truetype(os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", name), size)
        except OSError:
            continue
    return ImageFont.load_default(size)


def shape_text(s: str) -> str:
    """Arabic letters joined and laid out right to left (Pillow here has no complex-script engine)."""
    if any("֐" <= ch <= "ࣿ" for ch in s):
        try:
            import arabic_reshaper
            from bidi.algorithm import get_display
            return get_display(arabic_reshaper.reshape(s))
        except ImportError:
            pass
    return s


def text(s: str, x: float, y: float, size: float, colour="#000000", anchor: str = "ms", bold: bool = False,
         family: str = "sans", alpha: float = 1.0, mode: str = "normal") -> Op:
    """Text drawn at the render size, so it stays sharp at any scale. anchor like Pillow's: 'ls' left-baseline,
    'ms' middle-baseline, 'rs' right-baseline, 'mm' centred."""
    def op(ctx: Ctx):
        ss = ctx.ss
        f = _font(family, max(1, round(size * ctx.scale * ss)), bold)
        t = shape_text(s)
        X, Y = x * ctx.scale * ss, y * ctx.scale * ss
        l, tp, r, b = f.getbbox(t, anchor=anchor)
        x0, y0 = max(0, math.floor((X + l) / ss) - 2), max(0, math.floor((Y + tp) / ss) - 2)
        x1, y1 = min(ctx.W, math.ceil((X + r) / ss) + 2), min(ctx.H, math.ceil((Y + b) / ss) + 2)
        if x1 <= x0 or y1 <= y0:
            return
        im = Image.new("L", ((x1 - x0) * ss, (y1 - y0) * ss), 0)
        ImageDraw.Draw(im).text((X - x0 * ss, Y - y0 * ss), t, font=f, fill=255, anchor=anchor)
        m = np.asarray(im.reduce(ss) if ss > 1 else im, np.float32) / 255
        box = (x0, y0, x1, y1)
        ctx.blend(box, m, ctx.paint(colour, box), alpha, mode)
    return op


def _value_noise(h: int, w: int, cell: float, seed: int, octaves: int = 4) -> np.ndarray:
    """Smooth random texture in 0..1 (fractal value noise): the base of skin, stone, water and cloud textures."""
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w), np.float32)
    amp, total = 1.0, 0.0
    for o in range(octaves):
        c = max(1.0, cell / (2 ** o))
        gh, gw = int(h / c) + 2, int(w / c) + 2
        g = rng.random((gh, gw), dtype=np.float32)
        im = Image.fromarray((g * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
        out += np.asarray(im, np.float32) / 255 * amp
        total += amp
        amp *= 0.5
    return out / total


def noise(shape: Shape, amount: float = 0.25, cell: float = 24.0, seed: int = 1, mode: str = "multiply",
          colour="#ffffff", octaves: int = 4, stretch: tuple[float, float] = (1.0, 1.0)) -> Op:
    """Texture inside a shape: random light and dark grain the eye reads as a material (skin, rock, water, fog).
    `cell` is the grain size in scene units; `stretch` (sx, sy) elongates it (water streaks, fur); mode multiply
    darkens by up to `amount`, add/screen lightens, normal paints the colour with noisy strength."""
    def op(ctx: Ctx):
        box = ctx.bbox(shape, 2)
        if not box:
            return
        x0, y0, x1, y1 = box
        m = ctx.mask(shape, box)
        n = _value_noise(y1 - y0, x1 - x0, cell * ctx.scale, seed, octaves)
        if stretch != (1.0, 1.0):
            sx, sy = stretch
            big = _value_noise(int((y1 - y0) / sy) + 2, int((x1 - x0) / sx) + 2, cell * ctx.scale, seed, octaves)
            n = np.asarray(Image.fromarray((big * 255).astype(np.uint8)).resize((x1 - x0, y1 - y0), Image.BICUBIC),
                           np.float32) / 255
        n = (n - 0.5) * 2                                   # -1 .. 1
        col = ctx.paint(colour, box)
        if mode == "multiply":
            ctx.blend(box, m, (1 + np.clip(n, -1, 0) * amount)[..., None] * np.ones(3, np.float32), 1.0, "multiply")
        elif mode == "normal":
            ctx.blend(box, m * np.clip(n, 0, 1) * amount, col, 1.0, "normal")
        else:
            ctx.blend(box, m * np.clip(n, 0, 1) * amount, col, 1.0, mode)
    return op


def shade(shape: Shape, light: Pt, lit, dark, core: float = 0.35, soft: float = 0.0) -> Op:
    """Form shading: the side of a shape facing the light point gets `lit`, the far side `dark`, with a smooth
    fall-off between them, which turns a flat silhouette into a rounded body."""
    xs = [p[0] for q in shape for p in q]
    ys = [p[1] for q in shape for p in q]
    if not xs:
        return lambda ctx: None
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    r = max(max(xs) - min(xs), max(ys) - min(ys)) / 2
    lx, ly = light
    d = math.hypot(lx - cx, ly - cy) or 1.0
    hx, hy = cx + (lx - cx) / d * r * core, cy + (ly - cy) / d * r * core
    return fill(shape, rad((hx, hy), r * (1.0 + core), [(0, lit), (1, dark)]), 1.0, soft)


def scales(shape: Shape, size: float = 14.0, colour="#000000", alpha: float = 0.35, width: float = 1.0,
           stagger: bool = True) -> Op:
    """Overlapping arcs clipped to a shape: reptile scales, fish skin, roof tiles."""
    xs = [p[0] for q in shape for p in q]
    ys = [p[1] for q in shape for p in q]
    if not xs:
        return lambda ctx: None
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    arcs = []
    row = 0
    y = y0
    while y < y1 + size:
        x = x0 - (size / 2 if (stagger and row % 2) else 0)
        while x < x1 + size:
            arcs.append([(x + size * .5 * (1 + math.cos(math.pi * (1 - t))), y + size * .45 * math.sin(math.pi * (1 - t)))
                         for t in [k / 8 for k in range(9)]])
            x += size
        y += size * .55
        row += 1
    pattern = stroke(arcs, width)

    def op(ctx: Ctx):
        box = ctx.bbox(shape, 2)
        if not box:
            return
        m = ctx.mask(shape, box) * ctx.mask(pattern, box)
        ctx.blend(box, m, ctx.paint(colour, box), alpha, "normal")
    return op


# ── physically shaded surfaces: a height field under the shape, lit by real light directions ────────────────
Light = tuple  # (x, y, z, colour, strength): z is height above the picture plane, in scene units


def _normals(h: np.ndarray, scale: float) -> np.ndarray:
    """Surface normals of a height field (scene units -> pixels: height is already in pixels)."""
    import cv2
    gx = cv2.Sobel(h, cv2.CV_32F, 1, 0, ksize=3) / 8.0
    gy = cv2.Sobel(h, cv2.CV_32F, 0, 1, ksize=3) / 8.0
    n = np.stack([-gx, -gy, np.ones_like(h)], -1)
    return n / np.linalg.norm(n, axis=-1, keepdims=True)


def _lit(n: np.ndarray, box, ctx, lights, base, ambient, shininess, spec, fresnel, fres_col, sss: float = 0.0,
         sss_col=None, rough: np.ndarray | None = None):
    """Light a normal field. `sss` blurs the diffuse light under the surface (skin, flesh, wax) and tints it;
    `rough` (0..1 per pixel) spreads the highlight where the surface is rough."""
    import cv2
    x0, y0, x1, y1 = box
    s = ctx.scale
    X, Y = np.meshgrid((np.arange(x0, x1, dtype=np.float32) + .5) / s, (np.arange(y0, y1, dtype=np.float32) + .5) / s)
    basec = ctx.paint(base, box)[..., :3]
    diffuse = np.zeros(n.shape, np.float32) + ambient
    specular = np.zeros(n.shape, np.float32)
    V = np.array([0, 0, 1], np.float32)
    for lx, ly, lz, lc, strength in lights:
        L = np.stack([lx - X, ly - Y, np.full_like(X, lz)], -1)
        L /= np.linalg.norm(L, axis=-1, keepdims=True)
        lam = np.clip((n * L).sum(-1), 0, 1)[..., None]
        H = L + V
        H /= np.linalg.norm(H, axis=-1, keepdims=True)
        ndh = np.clip((n * H).sum(-1), 0, 1)[..., None]
        shin = shininess if rough is None else shininess * (1 - 0.85 * rough[..., None])
        sp = ndh ** shin
        c = rgb(lc)[None, None, :] * strength
        diffuse = diffuse + c * lam
        specular = specular + c * sp * spec
    if sss:
        r = max(0.5, sss * s)
        soft = cv2.GaussianBlur(diffuse, (0, 0), r)
        tint = rgb(sss_col)[None, None, :] if sss_col else 1.0
        diffuse = 0.45 * diffuse + 0.55 * soft * tint
    col = basec * diffuse + specular
    if fresnel:
        f = (1 - np.clip(n[..., 2], 0, 1))[..., None] ** 2
        col += rgb(fres_col)[None, None, :] * f * fresnel
    return col


def relief(shape: Shape, lights: list, base="#808080", ambient: float = 0.22, bulge: float = 0.6, plateau: float = 0.5,
           shininess: float = 30.0, spec: float = 0.5, bump: float = 0.0, bump_cell: float = 12.0, seed: int = 1,
           fresnel: float = 0.0, fres_col="#9fb6d8", soft: float = 1.0, bumps: list | None = None, sss: float = 0.0,
           sss_col=None, roughness: float = 0.0, profile: np.ndarray | None = None) -> Op:
    """A shape as a solid body: a height field rises from its edges (rounded sides, a flat top beyond `plateau`),
    optional bumps for skin or rock, and real lights: diffuse falls off with the surface angle, wet highlights
    appear where the surface faces between the light and the eye, Fresnel brightens grazing edges. This is what
    turns a flat silhouette into a lit volume."""
    def op(ctx: Ctx):
        import cv2
        box = ctx.bbox(shape, 3)
        if not box:
            return
        m = ctx.mask(shape, box)
        mb = (m > 0.5).astype(np.uint8)
        d = cv2.distanceTransform(mb, cv2.DIST_L2, 5)
        dmax = max(float(d.max()), 1.0)
        t = np.clip(d / (dmax * plateau), 0, 1)
        h = np.sqrt(1 - (1 - t) ** 2) * dmax * bulge
        if bump:
            h += (_value_noise(*h.shape, bump_cell * ctx.scale, seed, 4) - .5) * bump * ctx.scale * 2
        for k, (amp, cell) in enumerate(bumps or []):             # detail at several scales: folds, pores, grit
            h += (_value_noise(*h.shape, cell * ctx.scale, seed + 7 * (k + 1), 3) - .5) * amp * ctx.scale * 2
        if soft:
            h = cv2.GaussianBlur(h, (0, 0), soft * ctx.scale)
        n = _normals(h, ctx.scale)
        rough = None
        if roughness:
            rough = np.clip(_value_noise(*h.shape, bump_cell * 2 * ctx.scale, seed + 99, 3) * roughness * 1.6, 0, 1).astype(np.float32)
        col = _lit(n, box, ctx, lights, base, ambient, shininess, spec, fresnel, fres_col, sss, sss_col, rough)
        ctx.blend(box, m, np.concatenate([col, np.ones_like(col[..., :1])], -1), 1.0, "normal")
    return op


def water(area: Shape, lights: list, deep="#0a1118", sky="#2a3a4c", cell: float = 18.0, stretch: float = 6.0,
          height: float = 6.0, seed: int = 1, shininess: float = 60.0, spec: float = 1.2, octaves: int = 4) -> Op:
    """A water surface: waves as a stretched noise height field; the colour mixes the deep colour with the sky
    by how much each wave faces up, and every light leaves a trail of glints on the facets that face it."""
    def op(ctx: Ctx):
        import cv2
        box = ctx.bbox(area, 2)
        if not box:
            return
        x0, y0, x1, y1 = box
        m = ctx.mask(area, box)
        big = _value_noise(int((y1 - y0)) + 2, int((x1 - x0) / stretch) + 2, cell * ctx.scale, seed, octaves)
        hgt = np.asarray(Image.fromarray((big * 255).astype(np.uint8)).resize((x1 - x0, y1 - y0), Image.BICUBIC), np.float32) / 255
        hgt = (hgt - .5) * height * ctx.scale
        n = _normals(hgt, ctx.scale)
        up = np.clip(n[..., 2], 0, 1)[..., None]
        base = ctx.paint(deep, box)[..., :3] * (1 - up * .6) + ctx.paint(sky, box)[..., :3] * up * .6
        col = base * .9
        V = np.array([0, 0, 1], np.float32)
        s = ctx.scale
        X, Y = np.meshgrid((np.arange(x0, x1, dtype=np.float32) + .5) / s, (np.arange(y0, y1, dtype=np.float32) + .5) / s)
        for lx, ly, lz, lc, strength in lights:
            L = np.stack([lx - X, ly - Y, np.full_like(X, lz)], -1)
            dist = np.linalg.norm(L, axis=-1, keepdims=True)
            L /= dist
            H = L + V
            H /= np.linalg.norm(H, axis=-1, keepdims=True)
            sp = np.clip((n * H).sum(-1), 0, 1)[..., None] ** shininess
            lam = np.clip((n * L).sum(-1), 0, 1)[..., None]
            c = rgb(lc)[None, None, :] * strength
            col += c * sp * spec + base * c * lam * .5
        ctx.blend(box, m, np.concatenate([col, np.ones_like(col[..., :1])], -1), 1.0, "normal")
    return op


def _blur_canvas(c: np.ndarray, r: float) -> np.ndarray:
    import cv2
    return cv2.GaussianBlur(c, (0, 0), r) if r >= 0.3 else c


def defocus(radius: float, shape: Shape | None = None, soft: float = 30.0) -> Op:
    """Depth of field: everything painted so far goes out of focus by `radius` (scene px). Call it after the
    background steps and before the subject, so the subject stays sharp. With `shape`, only inside it (soft edge)."""
    def op(ctx: Ctx):
        import cv2
        blurred = _blur_canvas(ctx.canvas, radius * ctx.scale)
        if shape is None:
            ctx.canvas[:] = blurred
            return
        box = (0, 0, ctx.W, ctx.H)
        m = cv2.GaussianBlur(ctx.mask(shape, box), (0, 0), max(0.5, soft * ctx.scale))[..., None]
        ctx.canvas[:] = ctx.canvas * (1 - m) + blurred * m
    return op


def motion_blur(shape: Shape, length: float, angle: float = 90.0, mix: float = 1.0) -> Op:
    """Streak what is inside the shape along `angle` (degrees, 90 = downwards) by `length` scene px: rain, spray,
    a wing beat."""
    def op(ctx: Ctx):
        import cv2
        box = ctx.bbox(shape, length * ctx.scale + 2)
        if not box:
            return
        x0, y0, x1, y1 = box
        L = max(3, int(length * ctx.scale) | 1)
        k = np.zeros((L, L), np.float32)
        a = math.radians(angle)
        cx = cy = L // 2
        for t in np.linspace(-L / 2, L / 2, L * 2):
            x, y = int(round(cx + t * math.cos(a))), int(round(cy + t * math.sin(a)))
            if 0 <= x < L and 0 <= y < L:
                k[y, x] = 1
        k /= k.sum()
        reg = ctx.canvas[y0:y1, x0:x1]
        streaked = cv2.filter2D(reg, -1, k, borderType=cv2.BORDER_REFLECT)
        m = ctx.mask(shape, box)[..., None] * mix
        reg[:] = reg * (1 - m) + streaked * m
    return op


def bloom(threshold: float = 0.75, radius: float = 30.0, strength: float = 0.6, tint="#ffffff") -> Op:
    """Highlight bloom: light above `threshold` spills softly into its surroundings, as it does in a lens."""
    def op(ctx: Ctx):
        hi = np.clip(ctx.canvas - threshold, 0, None)
        ctx.canvas += _blur_canvas(hi, radius * ctx.scale) * strength * rgb(tint)[None, None, :]
        ctx.canvas += _blur_canvas(hi, radius * 3 * ctx.scale) * strength * 0.5 * rgb(tint)[None, None, :]
    return op


def flare(centre: Pt, colour="#ffb070", size: float = 120.0, streak: float = 420.0, strength: float = 0.6,
          ghosts: int = 3) -> Op:
    """An anamorphic lens flare from a bright point: a soft core, a horizontal streak, and faint ghost discs mirrored
    through the picture centre."""
    cx, cy = centre
    ops = [glow(ellipse(cx, cy, size * .5, size * .5), colour, size * .6, strength),
           fill(ellipse(cx, cy, streak, size * .09), colour, strength * .45, blur=size * .12, mode="add"),
           fill(ellipse(cx, cy, streak * .55, size * .04), "#ffffff", strength * .5, blur=size * .05, mode="add")]
    for k in range(1, ghosts + 1):
        t = 1 + k * .55
        gx, gy = W0 / 2 + (cx - W0 / 2) * (1 - t), H0 / 2 + (cy - H0 / 2) * (1 - t)
        ops.append(fill(ellipse(gx, gy, size * (.25 + .2 * k), size * (.25 + .2 * k)), colour, strength * .12, blur=size * .1, mode="add"))
    return lambda ctx: [o(ctx) for o in ops]


def chroma(amount: float = 1.5) -> Op:
    """Chromatic fringing: red and blue drift apart toward the frame edges, as in a real lens."""
    def op(ctx: Ctx):
        import cv2
        c = ctx.canvas
        H, W = c.shape[:2]
        cx, cy = W / 2, H / 2
        for ch, k in ((0, 1 + amount * ctx.scale / max(W, H) * 2), (2, 1 - amount * ctx.scale / max(W, H) * 2)):
            M = np.array([[k, 0, cx * (1 - k)], [0, k, cy * (1 - k)]], np.float32)
            c[..., ch] = cv2.warpAffine(c[..., ch], M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return op


def filmic(exposure: float = 1.0, contrast: float = 1.05, saturation: float = 1.0, lift: float = 0.0) -> Op:
    """Filmic tone mapping (ACES-style curve): highlights roll off like film, blacks stay deep, colours stay in
    gamut. Use with ROLLOFF = 1.0 in the scene."""
    def op(ctx: Ctx):
        x = np.clip(ctx.canvas * exposure, 0, None)
        y = (x * (2.51 * x + 0.03)) / (x * (2.43 * x + 0.59) + 0.14)
        lum = (y @ np.array([.2126, .7152, .0722], np.float32))[..., None]
        y = lum + (y - lum) * saturation
        y = (y - 0.5) * contrast + 0.5 + lift
        ctx.canvas[:] = np.clip(y, 0, 1)
    return op


def vignette(strength: float = 0.5) -> Op:
    def op(ctx: Ctx):
        y, x = np.ogrid[:ctx.H, :ctx.W]
        d = np.hypot((x - ctx.W / 2) / (ctx.W / 2), (y - ctx.H / 2) / (ctx.H / 2)) / math.sqrt(2)
        t = np.clip((d - 0.35) / 0.65, 0, 1)
        ctx.canvas *= (1 - strength * t * t * (3 - 2 * t))[..., None].astype(np.float32)
    return op


def grain(amount: float = 0.02, seed: int = 1) -> Op:
    def op(ctx: Ctx):
        ctx.canvas += np.random.default_rng(seed).normal(0, amount, (ctx.H, ctx.W, 1)).astype(np.float32)
    return op


def grade(shadows="#000000", highlights="#ffffff", amount: float = 0.5, contrast: float = 1.0) -> Op:
    """Split toning: lift the shadows toward one colour, tint the highlights toward another; then contrast."""
    def op(ctx: Ctx):
        c = ctx.canvas
        lum = np.clip(c @ np.array([.2126, .7152, .0722], np.float32), 0, 1)[..., None]
        c += rgb(shadows) * (1 - lum) ** 2 * amount
        c *= 1 + (rgb(highlights) - 1) * lum ** 2 * amount
        if contrast != 1.0:
            c[:] = (c - 0.5) * contrast + 0.5
    return op


# ── a step of the picture program ───────────────────────────────────────────────────────────────────────────
@dataclass
class Step:
    label: str                       # what is being drawn (shown while it is drawn)
    ops: list[Op]
    order: str = "sweep"             # sweep | grow | rise | down | sparkle | right | left
    origin: Pt | None = None         # where a 'grow' starts (scene units)
    weight: float = 1.0              # share of drawing time
    meta: dict = field(default_factory=dict)


def to_uint8(c: np.ndarray, rolloff: float = 0.82) -> np.ndarray:
    """Highlights above `rolloff` roll off softly instead of clipping hard (fire and glow stay rich), then 8-bit.
    rolloff=1 keeps every colour exact (logos)."""
    k = rolloff
    x = c if k >= 1 else np.where(c > k, k + (1 - k) * np.tanh((c - k) / (1 - k)), c)
    return (np.clip(x, 0, 1) * 255 + .5).astype(np.uint8)


def render(steps: list[Step], scale: float = 1.0, ss: int = 3, paper: str = "#000000",
           rolloff: float = 0.82) -> Iterator[tuple[int, Step, np.ndarray]]:
    """Run the picture program; yield the finished image after every step."""
    ctx = Ctx(scale, ss, paper)
    for i, st in enumerate(steps):
        for op in st.ops:
            op(ctx)
        yield i, st, to_uint8(ctx.canvas, rolloff)


def render_image(steps: list[Step], scale: float = 1.0, ss: int = 3, rolloff: float = 0.82) -> Image.Image:
    img = None
    for _, _, img in render(steps, scale, ss, rolloff=rolloff):
        pass
    return Image.fromarray(img)


# ── the painter's order: which changed pixel goes down first ────────────────────────────────────────────────
def reveal_order(idx: np.ndarray, W: int, step: Step, scale: float, seed: int = 0) -> np.ndarray:
    """Sort the changed pixels of a step the way a painter would lay them down."""
    rng = np.random.default_rng(seed)
    y, x = idx // W, idx % W
    jitter = rng.random(idx.size).astype(np.float32)
    k = step.order
    if k == "sparkle":
        key = jitter
    elif k == "grow":
        ox, oy = step.origin or (W0 / 2, H0 / 2)
        key = np.hypot(x - ox * scale, y - oy * scale) + jitter * 9 * scale
    elif k == "rise":
        key = -y + jitter * 7 * scale
    elif k == "down":
        key = y + jitter * 7 * scale
    elif k in ("right", "left"):
        key = (x if k == "right" else -x) + jitter * 7 * scale
    else:                                    # sweep: horizontal brush strokes, back and forth
        bh = max(2, round(7 * scale))
        band = y // bh
        xx = np.where(band % 2 == 0, x, W - 1 - x)
        key = band * (W + 64.0) + xx + jitter * 26 * scale
    return idx[np.argsort(key, kind="stable")]
