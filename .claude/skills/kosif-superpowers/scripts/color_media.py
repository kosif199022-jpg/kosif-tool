#!/usr/bin/env python3
"""KOSIF colour media: the portrait pipeline's measurement and stroke engine, in coloured pencil, oil
(brush) and watercolour.

The reference is measured exactly as for graphite (landmarks, regions, direction field), and the canvas
again starts blank. What changes is the pigment model and the order of work each medium is taught in:

  colored-pencil  a 30-pencil set; layered light to dark in hatched passes. Each stroke picks the pencil
                  whose layer moves the paper's local colour closest to the reference (wax layers glaze
                  over each other, so blue over yellow reads green); burnishing on skin, dark edges last.
  oil             a toned ground, then brushes from large to small (Hertzmann's coarse-to-fine painterly
                  rendering): each stroke takes one mixed colour, follows the form, ends dry; bristle
                  streaks, impasto relief lit from the upper left and the canvas weave come from the
                  stroke record, not from the photo.
  watercolor      a light pencil underdrawing, then transparent washes light to dark (a soft wet-in-wet
                  wash, flat shape washes, then darks), with edge darkening, granulation in the paper
                  tooth and the whites left as paper.

No photo pixel is copied: every colour on the canvas is a pencil from the set, a brush-load colour
sampled from a blurred reference (the painter's mixed colour), or a wash flattened over a whole shape.
Used through portrait_pipeline.py (`--medium colored-pencil|oil|watercolor`) or directly:

  python3 scripts/color_media.py draw --photo in.png --out out/x --medium oil [--models DIR]
"""
import hashlib
import json
import math
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import portrait_pipeline as pp  # noqa: E402

COLOR_MEDIA = ("colored-pencil", "oil", "watercolor")

# A generic 30-pencil set (names describe the colour, not a brand), sRGB 0..255.
PENCILS = [
    ("white", (250, 250, 246)), ("cream", (246, 232, 196)), ("lemon yellow", (247, 226, 76)),
    ("canary yellow", (245, 196, 40)), ("orange", (240, 130, 40)), ("vermilion", (222, 72, 44)),
    ("scarlet lake", (196, 40, 48)), ("crimson", (150, 26, 46)), ("rose pink", (232, 140, 160)),
    ("magenta", (176, 46, 120)), ("violet", (104, 62, 140)), ("ultramarine", (48, 58, 150)),
    ("cobalt blue", (52, 102, 176)), ("sky blue", (130, 180, 220)), ("indigo", (36, 42, 74)),
    ("turquoise", (40, 150, 160)), ("emerald green", (30, 130, 84)), ("sap green", (92, 128, 50)),
    ("olive green", (110, 110, 54)), ("yellow ochre", (200, 150, 70)), ("raw sienna", (186, 120, 60)),
    ("burnt sienna", (150, 74, 44)), ("burnt umber", (96, 62, 44)), ("sepia", (70, 50, 40)),
    ("peach", (240, 190, 160)), ("light flesh", (236, 204, 178)), ("terracotta", (190, 104, 80)),
    ("warm grey", (150, 140, 130)), ("cool grey", (124, 132, 140)), ("black", (28, 28, 32)),
]
NEUTRAL = {"warm grey", "cool grey", "black"}

PENCIL_PASSES = [   # light to dark, the way a coloured-pencil drawing is layered
    {"name": "layer-1", "off": 0.0, "sp": 3.4, "ln": (24, 70), "w": 1.6, "a": 0.50, "tol": 0.20},
    {"name": "layer-2", "off": 58.0, "sp": 3.0, "ln": (18, 60), "w": 1.5, "a": 0.58, "tol": 0.16},
    {"name": "layer-3", "off": -38.0, "sp": 2.6, "ln": (14, 46), "w": 1.35, "a": 0.65, "tol": 0.13},
    {"name": "layer-4", "off": 90.0, "sp": 2.2, "ln": (8, 30), "w": 1.2, "a": 0.70, "tol": 0.10},
]

DETAIL_PASS = {"name": "detail", "off": 20.0, "sp": 1.5, "ln": (5, 18), "w": 0.8, "a": 0.62, "tol": 0.07,
               "blur": 0.8}
PAPER = {"colored-pencil": (247, 244, 236), "oil": (176, 146, 112), "watercolor": (250, 249, 244)}


def srgb_to_oklab(c):
    """c: (..., 3) sRGB in 0..1 -> OKLab (Ottosson 2020)."""
    import numpy as np
    c = np.asarray(c, np.float32)
    lin = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    M1 = np.array([[0.4122214708, 0.5363325363, 0.0514459929], [0.2119034982, 0.6806995451, 0.1073969566],
                   [0.0883024619, 0.2817188376, 0.6299787005]], np.float32)
    M2 = np.array([[0.2104542553, 0.7936177850, -0.0040720468], [1.9779984951, -2.4285922050, 0.4505937099],
                   [0.0259040371, 0.7827717662, -0.8086757660]], np.float32)
    lms = np.cbrt(np.maximum(lin @ M1.T, 0))
    return lms @ M2.T


def _target(ref):
    import cv2
    import numpy as np
    rgb = cv2.cvtColor(cv2.bilateralFilter(ref, 0, 10, 1.5), cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
    return rgb


def _focus(labels, lm, L, person):
    """Where the finest tools work (focal hierarchy, PM-06): the face and the subject's strongest edges."""
    import cv2
    import numpy as np
    h, w = L.shape
    m = np.zeros((h, w), np.uint8)
    if person:
        m |= (labels == 3).astype(np.uint8)
        if lm is not None:     # brows, eyes and hairline belong to the face even where segmentation says hair
            x0, y0 = lm.min(0).astype(int)
            x1, y1 = lm.max(0).astype(int)
            pad = int(0.08 * (x1 - x0))
            m[max(0, y0 - 3 * pad):y1 + pad, max(0, x0 - pad):x1 + pad] |= np.isin(
                labels[max(0, y0 - 3 * pad):y1 + pad, max(0, x0 - pad):x1 + pad], (1, 2, 3)).astype(np.uint8)
    g = cv2.GaussianBlur(L, (0, 0), 1.0)
    mag = np.hypot(cv2.Sobel(g, cv2.CV_32F, 1, 0, ksize=3), cv2.Sobel(g, cv2.CV_32F, 0, 1, ksize=3))
    subject = labels > 0 if person else np.ones((h, w), bool)
    m |= ((mag > np.percentile(mag[subject], 92)) & subject).astype(np.uint8)
    return cv2.dilate(m, np.ones((5, 5), np.uint8)) > 0


def _colour_bounds(T, labels, k=12):
    """Colour shapes strokes must not cross: kmeans in OKLab, per region."""
    import cv2
    import numpy as np
    h, w = labels.shape
    lab = srgb_to_oklab(cv2.resize(T, (max(1, w // 4), max(1, h // 4)), interpolation=cv2.INTER_AREA))
    data = lab.reshape(-1, 3).astype(np.float32) * [1.0, 2.0, 2.0]
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1e-3)
    _, _, centers = cv2.kmeans(data.astype(np.float32), k, None, crit, 2, cv2.KMEANS_PP_CENTERS)
    full = (srgb_to_oklab(T) * [1.0, 2.0, 2.0]).reshape(-1, 1, 3)
    cl = ((full - centers.reshape(1, -1, 3)) ** 2).sum(-1).argmin(1).reshape(h, w).astype(np.uint8)
    cl = cv2.medianBlur(cl, 7)
    return labels.astype(np.int32) * 16 + cl


# ------------------------------------------------------------------ coloured pencil

class PencilCanvas:
    """Paper as RGB; each stroke lays a pencil's wax through the tooth (part glaze, part cover)."""

    def __init__(self, h, w, tooth, rng, paper, ss=3):
        import numpy as np
        self.h, self.w, self.ss, self.rng, self.tooth = h, w, ss, rng, tooth
        base = np.array(paper, np.float32) / 255.0
        self.rgb = (base * (0.965 + 0.035 * tooth)[..., None]).astype(np.float32)
        self.pal = np.array([c for _, c in PENCILS], np.float32) / 255.0
        self.pal_lab = srgb_to_oklab(self.pal)
        self.T = self.T_lab = None
        self.strokes = []
        self.glaze = 0.62        # share of a layer that multiplies (transparent wax) vs covers

    def choose(self, x, y, v, darken=1.0, penalty=0.012, hue_lock=False):
        """Pencil whose layer at coverage v moves the local colour closest to the (darkened) target."""
        import numpy as np
        r = 2
        c = self.rgb[max(0, y - r):y + r + 1, max(0, x - r):x + r + 1].reshape(-1, 3).mean(0)
        t = self.T_lab[y, x].copy()
        t[0] *= darken
        cand = c * (1 - v) + v * (self.glaze * c * self.pal + (1 - self.glaze) * self.pal)
        d = np.sqrt(((srgb_to_oklab(cand) - t) ** 2 * [1.0, 1.6, 1.6]).sum(1))
        chroma = float(np.hypot(t[1], t[2]))
        if chroma > 0.03:     # colourists build darks from colour; greys and black only for neutral areas
            d[[i for i, (n, _) in enumerate(PENCILS) if n in NEUTRAL]] += penalty
        if chroma > 0.03:   # stay near the local hue: brown darks on skin, not a blue cast (edges: strictly)
            ph = np.arctan2(self.pal_lab[:, 2], self.pal_lab[:, 1])
            dh = np.abs((ph - math.atan2(t[2], t[1]) + np.pi) % (2 * np.pi) - np.pi)
            col = np.hypot(self.pal_lab[:, 1], self.pal_lab[:, 2]) > 0.03
            d += col * 0.035 * dh / np.pi
            if hue_lock:
                d[(dh > math.radians(45)) & col] += 1.0
        now = float(np.sqrt(((srgb_to_oklab(c) - t) ** 2 * [1.0, 1.6, 1.6]).sum()))
        i = int(d.argmin())
        return i, now - float(d[i])

    def stroke(self, pts, width, alpha, spacing, layer, taper="both", record=True, pencil=None):
        import numpy as np
        pts = np.asarray(pts, np.float32)
        if len(pts) < 2:
            return
        if pencil is None:   # edges and accents: the pencil nearest a darker version of the local colour
            mx, my = pts[len(pts) // 2].astype(int)
            mx, my = min(max(mx, 0), self.w - 1), min(max(my, 0), self.h - 1)
            if layer == "construction":
                pencil = [n for n, _ in PENCILS].index("yellow ochre")
            else:
                pencil, _ = self.choose(mx, my, 0.9, darken=0.72, penalty=0.004, hue_lock=True)
                local = self.rgb[max(0, my - 2):my + 3, max(0, mx - 2):mx + 3].reshape(-1, 3).mean(0)
                if self.pal_lab[pencil][0] >= srgb_to_oklab(local)[0] - 0.02:
                    return                       # an edge line is only ever darker than what is on the paper
        got = pp.stroke_mask(pts, width, spacing, (self.h, self.w), self.rng, self.ss, taper)
        if got is None:
            return
        m, (x0, y0, x1, y1) = got
        tooth = self.tooth[y0:y1, x0:x1]
        dep = (min(alpha, 0.95) * m * (0.45 + 0.55 * tooth ** (1.4 - 0.8 * alpha)))[..., None]
        p = self.pal[pencil]
        roi = self.rgb[y0:y1, x0:x1]
        roi[:] = roi * (1 - dep) + dep * (self.glaze * roi * p + (1 - self.glaze) * p)
        if record:
            n = len(pts)
            self.strokes.append((layer, round(width, 2), round(alpha, 3), pencil,
                                 pts[:: max(1, n // 12)].round(1).tolist() + [pts[-1].round(1).tolist()]))


def _need_map(cv, scale, sigma=1.6):
    import cv2
    import numpy as np
    blur = cv2.GaussianBlur(cv.rgb, (0, 0), sigma * scale)
    d = np.sqrt(((srgb_to_oklab(blur) - cv.T_lab) ** 2 * [1.0, 1.6, 1.6]).sum(-1))
    return ((d - 0.05) * 4.0).astype(np.float32)


def pencil_pass(cv, P, L, labels, bounds, field, scale, rng, stats, region_mask=None):
    import cv2
    import numpy as np
    h, w = L.shape
    passcov = np.zeros((h, w), np.float32)    # where this pass has already laid a hatch line
    grid = max(1.0, P["sp"] * scale * 0.72 * 0.9)
    ys, xs = np.mgrid[0:h:grid, 0:w:grid]
    xs = (xs + rng.random(xs.shape) * grid).ravel()
    ys = (ys + rng.random(ys.shape) * grid).ravel()
    keep = (xs < w - 1) & (ys < h - 1)
    xs, ys = xs[keep], ys[keep]
    off = math.radians(P["off"])
    count = 0
    for rnd in range(2):
        need = _need_map(cv, scale, P.get("blur", 1.6))
        if rnd:
            passcov[:] = 0                   # second round: a second layer in the same direction where still needed
        ix, iy = xs.astype(int), ys.astype(int)
        ok = (need[iy, ix] > 0) & (passcov[iy, ix] < 0.5)
        if region_mask is not None:
            ok &= region_mask[iy, ix]
        xs, ys = xs[ok], ys[ok]
        order = rng.permutation(len(xs))
        for x, y in zip(xs[order].tolist(), ys[order].tolist()):
            ix, iy = int(x), int(y)
            if passcov[iy, ix] >= 0.5:
                continue
            st = pp.REGION_STYLE[pp.REGIONS[min(int(labels[iy, ix]), 5)]]
            sp = P["sp"] * st["sp"] * scale
            width = P["w"] * st["w"] * scale * rng.uniform(0.9, 1.1)
            a = min(P["a"] * rng.uniform(0.85, 1.1) * st.get("amul", 1.0), 0.9)
            v = min(0.42 * a * width / sp, 0.95)
            pencil, gain = cv.choose(ix, iy, v)
            if gain < 0.008:
                continue
            ln = rng.uniform(*P["ln"]) * st["ln"] * scale
            pts = pp.trace(x, y, field, off * st.get("off", 1.0), ln, 1.6 * scale, bounds, L,
                           P["tol"] * st.get("tol", 1.0), need, passcov, rng, (h, w),
                           straight=st.get("straight", False))
            if len(pts) < 3:
                continue
            cv.stroke(pts, width, a, sp, P["name"], taper="flick" if rng.random() < 0.3 else "both", pencil=pencil)
            q = (np.asarray(pts) * 16).astype(np.int32)
            cv2.polylines(passcov, [q], False, 1.0, max(1, int(round(sp))), cv2.LINE_8, shift=4)
            count += 1
    stats[P["name"]] = stats.get(P["name"], 0) + count
    print(f"  pass {P['name']}: {count} strokes", file=sys.stderr, flush=True)


def burnish(cv, labels, amount):
    """Colourless blender / burnishing on skin: the wax is pressed into the tooth and the hatching melts."""
    import cv2
    import numpy as np
    skin = np.isin(labels, (2, 3)).astype(np.float32)
    if amount <= 0 or not skin.any():
        return
    m = cv2.GaussianBlur(cv2.erode(skin, np.ones((3, 3), np.uint8)), (0, 0), 3)[..., None] * amount
    soft = cv2.GaussianBlur(cv.rgb, (0, 0), 1.3)
    cv.rgb[:] = cv.rgb * (1 - m) + soft * m


def draw_pencil(ref, meas, person, args, stats, rng):
    import cv2
    import numpy as np
    h, w = ref.shape[:2]
    sc = args.scale
    labels, lm = meas["labels"], meas["landmarks"]
    T = _target(ref)
    L = cv2.cvtColor(ref, cv2.COLOR_BGR2LAB)[..., 0].astype(np.float32) / 255.0
    L = cv2.bilateralFilter(L, 0, 0.06, 3.0)
    bounds = _colour_bounds(T, labels)
    field = pp.direction_field(L, labels, flat_default=not person)
    cv = PencilCanvas(h, w, pp.paper_tooth(h, w, rng), rng, PAPER["colored-pencil"])
    cv.T, cv.T_lab = T, srgb_to_oklab(T)
    pp.construction(cv, lm, labels, sc, stats)
    for P in PENCIL_PASSES[:2]:
        pencil_pass(cv, P, L, labels, bounds, field, sc, rng, stats)
    burnish(cv, labels, args.blend * 0.8)
    for P in PENCIL_PASSES[2:]:
        pencil_pass(cv, P, L, labels, bounds, field, sc, rng, stats)
    burnish(cv, labels, args.blend * 0.35)
    # a sharp pencil last, on the face and the strongest edges only: crisp features, loose surroundings
    pencil_pass(cv, DETAIL_PASS, L, labels, bounds, field, sc, rng, stats, region_mask=_focus(labels, lm, L, person))
    pp.contour_lines(cv, ref, L, labels, sc, rng, stats)
    pp.feature_accents(cv, lm, L, labels, sc, rng, stats)
    if lm is not None:      # white pencil catchlights
        white = 0
        for eye in (pp.EYE_L, pp.EYE_R):
            c = lm[eye].mean(0)
            cv.stroke([c + [-0.6 * sc, -1.2 * sc], c + [0.4 * sc, -1.4 * sc]], 1.4 * sc, 0.8, 0, "accents",
                      taper="none", pencil=white)
    rgb = cv2.GaussianBlur(cv.rgb, (0, 0), 0.35)
    return np.clip(rgb * 255, 0, 255).astype(np.uint8), cv


# ------------------------------------------------------------------ oil (brush)

def _brush_stroke(img, height, x, y, R, colour, ref_blur, field, rng, max_len=14, min_len=3):
    """One Hertzmann stroke: follow the form, stop when the reference no longer matches the brush colour."""
    import cv2
    import numpy as np
    h, w = field.shape
    pts = [(x, y)]
    px = py = None
    for i in range(max_len):
        a = float(field[int(y), int(x)])
        dx, dy = math.cos(a), math.sin(a)
        if px is not None:
            if dx * px + dy * py < 0:
                dx, dy = -dx, -dy
            dx, dy = 0.6 * dx + 0.4 * px, 0.6 * dy + 0.4 * py      # brush inertia (curvature filter)
            nrm = math.hypot(dx, dy) + 1e-9
            dx, dy = dx / nrm, dy / nrm
        elif rng.random() < 0.5:
            dx, dy = -dx, -dy
        nx, ny = x + dx * R, y + dy * R
        if not (0 <= nx < w and 0 <= ny < h):
            break
        if i >= min_len:
            rc = ref_blur[int(ny), int(nx)]
            if np.abs(rc - colour).sum() > np.abs(rc - img[int(ny), int(nx)]).sum():
                break
        x, y, px, py = nx, ny, dx, dy
        pts.append((x, y))
    pts = np.array(pts, np.float32)
    if len(pts) < 2:
        pts = np.vstack([pts, pts + [R * 0.5, 0]])
    pad = int(R * 1.6) + 3
    x0, y0 = max(int(pts[:, 0].min()) - pad, 0), max(int(pts[:, 1].min()) - pad, 0)
    x1, y1 = min(int(pts[:, 0].max()) + pad + 1, w), min(int(pts[:, 1].max()) + pad + 1, h)
    if x1 - x0 < 2 or y1 - y0 < 2:
        return 0
    ss = 2
    n = len(pts)
    # a full body of paint under the bristles, then each bristle drags its own streak along the stroke
    body = np.zeros(((y1 - y0) * ss, (x1 - x0) * ss), np.uint8)
    brist = np.zeros_like(body)
    q = (pts - [x0, y0]) * ss
    tang = np.gradient(pts, axis=0) if n > 2 else np.repeat(pts[1:] - pts[:1], 2, 0)
    nrm = np.stack([-tang[:, 1], tang[:, 0]], 1) / (np.linalg.norm(tang, axis=1, keepdims=True) + 1e-9)
    dry = rng.uniform(0.3, 0.7)
    nb = int(np.clip(R * 0.9, 4, 14))
    for i in range(n - 1):
        t = i / max(n - 2, 1)
        paint = 1.0 - dry * t ** 1.5                        # the brush runs out of paint towards the end
        th = max(1, int(round(1.7 * R * ss)))
        a, b = (q[i] * 16).astype(np.int32), (q[i + 1] * 16).astype(np.int32)
        cv2.line(body, tuple(a), tuple(b), int(255 * max(paint - 0.25, 0)), th, cv2.LINE_AA, shift=4)
    load = rng.uniform(0.55, 1.0, nb)
    offs = (np.linspace(-0.92, 0.92, nb) + rng.normal(0, 0.06, nb)) * R
    bth = max(1, int(round(2.0 * R * ss / nb * 1.15)))
    for j in range(nb):
        line = (q + nrm * offs[j] * ss) * 16
        for i in range(n - 1):
            t = i / max(n - 2, 1)
            v = load[j] * (1.0 - dry * t ** 1.5)
            if v < 0.5:                                     # this bristle has run dry: a gap in the stroke
                continue
            cv2.line(brist, tuple(line[i].astype(np.int32)), tuple(line[i + 1].astype(np.int32)), int(255 * v), bth,
                     cv2.LINE_AA, shift=4)
    m = cv2.resize(np.maximum(body, brist), (x1 - x0, y1 - y0), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
    s = cv2.resize(brist, (x1 - x0, y1 - y0), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
    alpha = np.clip(m * 1.35, 0, 1)
    jitter = colour * (1 + rng.normal(0, 0.03))
    col = jitter[None, None, :] * (0.95 + 0.08 * s[..., None])
    roi = img[y0:y1, x0:x1]
    roi[:] = roi * (1 - alpha[..., None]) + col * alpha[..., None]
    hr = height[y0:y1, x0:x1]
    hr[:] = hr * (1 - alpha) + alpha * (0.35 + 0.65 * s) * min(1.0, R / 6.0)
    return 1


def draw_oil(ref, meas, person, args, stats, rng):
    import cv2
    import numpy as np
    h, w = ref.shape[:2]
    labels, lm = meas["labels"], meas["landmarks"]
    T = _target(ref)
    L = cv2.cvtColor(ref, cv2.COLOR_BGR2LAB)[..., 0].astype(np.float32) / 255.0
    field = pp.direction_field(L, labels, flat_default=True)
    ground = np.array(PAPER["oil"], np.float32) / 255.0
    img = np.ones((h, w, 3), np.float32) * ground
    height = np.zeros((h, w), np.float32)
    base = max(h, w)
    radii = [base / 48, base / 96, base / 190, base / 380]
    focus = _focus(labels, lm, L, person)
    radii += [base / 640, base / 950, base / 1500]      # small brushes: the face and the strongest edges only
    for li, R in enumerate(radii):
        R = max(1.4, R)
        ref_blur = cv2.GaussianBlur(T, (0, 0), max(0.6, R * 0.5))
        diff = np.abs(img - ref_blur).sum(-1)
        if li == 0:
            diff[:] = 1.0                                       # the first layer covers the whole ground
        g = max(1, int(R))
        thr = 0.10 if li < 4 else 0.08
        seeds = []
        for yy in range(0, h, g):
            for xx in range(0, w, g):
                cell = diff[yy:yy + g, xx:xx + g]
                if li >= 4 and not focus[min(yy + g // 2, h - 1), min(xx + g // 2, w - 1)]:
                    continue
                if cell.mean() > thr:
                    j = int(cell.argmax())
                    seeds.append((xx + j % cell.shape[1], yy + j // cell.shape[1]))
        order = rng.permutation(len(seeds))
        n = 0
        for k in order:
            x, y = seeds[k]
            n += _brush_stroke(img, height, float(x), float(y), R, ref_blur[y, x].copy(), ref_blur, field, rng)
        stats[f"brush-{li + 1} r{R:.1f}"] = n
        print(f"  brush {li + 1} (r {R:.1f}px): {n} strokes", file=sys.stderr, flush=True)
    # impasto relief lit from the upper left, and the canvas weave where paint is thin
    hb = cv2.GaussianBlur(height, (0, 0), 1.3)
    gx = cv2.Sobel(hb, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(hb, cv2.CV_32F, 0, 1, ksize=3)
    light = np.clip((gx + gy) * 0.6, -0.05, 0.05)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    weave = 0.5 + 0.25 * (np.sin(xx * 1.9) + np.sin(yy * 1.9))
    thin = np.clip(1 - height * 2.5, 0, 1)
    img = img * (1 + light[..., None]) * (1 - 0.05 * thin * (1 - weave))[..., None]
    spec = np.clip(light - 0.05, 0, 1) * 1.5
    img = img + spec[..., None]
    return np.clip(img * 255, 0, 255).astype(np.uint8), None


# ------------------------------------------------------------------ watercolour

def _wobble(mask_labels, rng, amp=2.0, sig=6.0):
    """Hand-laid wash edges: displace a label map with smooth noise."""
    import cv2
    import numpy as np
    h, w = mask_labels.shape
    dx = cv2.GaussianBlur(rng.standard_normal((h, w)).astype(np.float32), (0, 0), sig)
    dy = cv2.GaussianBlur(rng.standard_normal((h, w)).astype(np.float32), (0, 0), sig)
    dx *= amp / (dx.std() + 1e-6)
    dy *= amp / (dy.std() + 1e-6)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    return cv2.remap(mask_labels, xx + dx, yy + dy, cv2.INTER_NEAREST, borderMode=cv2.BORDER_REPLICATE)


def _flat_wash(resid, seg, tooth, rng, edge=0.35, gran=0.6, keep_light=0.97):
    """One wash: each shape gets one flat transmittance (the mean the shape needs), darker at its edges
    where pigment collects as the wash dries, and granulating into the paper tooth."""
    import cv2
    import numpy as np
    n = int(seg.max()) + 1
    sums = np.bincount(seg.ravel(), weights=resid.ravel(), minlength=n)
    cnt = np.bincount(seg.ravel(), minlength=n)
    mean = sums / np.maximum(cnt, 1)
    g = mean[seg].astype(np.float32)
    g = np.where(g > keep_light, 1.0, g)                  # nearly white shapes are left as paper
    border = np.zeros(seg.shape, np.uint8)
    border[:, 1:] |= (seg[:, 1:] != seg[:, :-1]).astype(np.uint8)
    border[1:, :] |= (seg[1:, :] != seg[:-1, :]).astype(np.uint8)
    dist = cv2.distanceTransform(1 - border, cv2.DIST_L2, 3)
    od = -np.log(np.clip(g, 1e-3, 1))                     # optical density of the wash
    od *= 1 + edge * np.exp(-dist / 2.5)
    od *= 1 + gran * (0.5 - tooth)
    return np.exp(-od).astype(np.float32)


def _segments(img_rgb, k, rng, wobble=2.0, down=2):
    import cv2
    import numpy as np
    h, w = img_rgb.shape[:2]
    small = cv2.resize((img_rgb * 255).astype(np.uint8), (max(1, w // down), max(1, h // down)),
                       interpolation=cv2.INTER_AREA)
    ms = cv2.pyrMeanShiftFiltering(small, 8, 18).astype(np.float32) / 255.0
    lab = srgb_to_oklab(ms).reshape(-1, 3) * [1.0, 1.5, 1.5]
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1e-3)
    _, lab_k, _ = cv2.kmeans(lab.astype(np.float32), k, None, crit, 2, cv2.KMEANS_PP_CENTERS)
    q = lab_k.reshape(small.shape[:2]).astype(np.uint8)
    q = cv2.medianBlur(q, 5)
    # connected pieces of each colour cluster become separate shapes
    seg = np.zeros(q.shape, np.int32)
    nxt = 0
    for c in range(k):
        m = (q == c).astype(np.uint8)
        nc, cc = cv2.connectedComponents(m, connectivity=4)
        seg[m > 0] = cc[m > 0] + nxt
        nxt += nc
    seg = cv2.resize(seg.astype(np.float32), (w, h), interpolation=cv2.INTER_NEAREST).astype(np.int32)
    return _wobble(seg.astype(np.float32), rng, amp=wobble).astype(np.int32)


def draw_watercolor(ref, meas, person, args, stats, rng):
    import cv2
    import numpy as np
    h, w = ref.shape[:2]
    sc = args.scale
    labels, lm = meas["labels"], meas["landmarks"]
    T = _target(ref)
    paper = np.array(PAPER["watercolor"], np.float32) / 255.0
    tooth = pp.paper_tooth(h, w, rng)
    tooth = cv2.GaussianBlur(tooth, (0, 0), 1.2)
    tooth = (tooth - tooth.min()) / (tooth.max() - tooth.min() + 1e-6)
    Tt = np.clip(T / paper, 0.02, 1.0)
    # 1. pencil underdrawing (graphite, light), kept under the washes
    L = cv2.cvtColor(ref, cv2.COLOR_BGR2LAB)[..., 0].astype(np.float32) / 255.0
    gcv = pp.Canvas(h, w, tooth, rng)
    pp.MED = dict(pp.MEDIUMS["graphite"])
    pp.construction(gcv, lm, labels, sc, stats)
    pp.contour_lines(gcv, ref, L, labels, sc, rng, stats)
    focus = _focus(labels, lm, L, person)
    fsoft = cv2.GaussianBlur(focus.astype(np.float32), (0, 0), 4)
    under = 1 - (0.42 + 0.2 * fsoft) * np.clip(gcv.ink, 0, 1)
    # 2. wet-in-wet: one soft wash that never goes darker than the lightest local value it covers
    dark = 1 - Tt
    soft = cv2.GaussianBlur(cv2.erode(dark, np.ones((int(9 * sc) | 1,) * 2, np.uint8)), (0, 0), max(h, w) / 90)
    g1 = np.clip(1 - 0.85 * soft, 0, 1)
    g1 = np.exp(np.log(np.clip(g1, 1e-3, 1)) * (1 + 0.35 * (0.5 - tooth))[..., None])
    stats["wash-1 wet-in-wet"] = 1
    # 3. shape washes (hard edges), then 4. darks on smaller shapes
    resid = np.clip(Tt / g1, 0, 1)
    seg2 = _segments(np.clip(T, 0, 1), 14, rng, wobble=2.2 * sc)
    g2 = np.stack([_flat_wash(resid[..., c] ** 0.85, seg2, tooth, rng) for c in range(3)], -1)
    stats["wash-2 shapes"] = int(seg2.max()) + 1
    resid = np.clip(Tt / (g1 * g2), 0, 1)
    fine = cv2.GaussianBlur(resid, (0, 0), 1.2 * sc)
    seg3 = _segments(np.clip(fine, 0, 1), 18, rng, wobble=1.2 * sc)
    g3 = np.stack([_flat_wash(fine[..., c], seg3, tooth, rng, edge=0.45, keep_light=0.92) for c in range(3)], -1)
    stats["wash-3 darks"] = int(seg3.max()) + 1
    # 5. last glaze: the darkest accents, again flat per (small) shape
    resid = np.clip(Tt / (g1 * g2 * g3), 0, 1)
    seg4 = _segments(np.clip(cv2.GaussianBlur(resid, (0, 0), 0.8 * sc), 0, 1), 24, rng, wobble=0.8 * sc)
    g4 = np.stack([_flat_wash(resid[..., c], seg4, tooth, rng, edge=0.5, keep_light=0.9) for c in range(3)], -1)
    stats["wash-4 accents"] = int(seg4.max()) + 1
    # 6. a small brush on the face and the strongest edges: crisp little shapes, the rest stays loose
    resid = np.clip(Tt / (g1 * g2 * g3 * g4), 0, 1)
    seg5 = _segments(np.clip(cv2.GaussianBlur(resid, (0, 0), 0.6), 0, 1), 32, rng, wobble=0.4 * sc, down=1)
    g5 = np.stack([_flat_wash(resid[..., c], seg5, tooth, rng, edge=0.4, keep_light=0.95) for c in range(3)], -1)
    g5 = np.exp(np.log(np.clip(g5, 1e-3, 1)) * fsoft[..., None])
    stats["wash-5 detail"] = int(seg5.max()) + 1
    glaze = g1 * g2 * g3 * g4 * g5
    if person:   # vignette: the background is washed lighter and left unfinished towards the paper's edges
        bg = cv2.GaussianBlur((labels == 0).astype(np.float32), (0, 0), 6)
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        edge = np.minimum.reduce([xx, yy, w - 1 - xx, h - 1 - yy]) / (0.09 * min(h, w))
        n = cv2.GaussianBlur(rng.standard_normal((h, w)).astype(np.float32), (0, 0), 0.03 * min(h, w))
        edge = np.clip(edge + 0.35 * n / (n.std() + 1e-6), 0, 1)
        strength = (1 - bg) + bg * 0.75 * edge             # optical density multiplier
        glaze = np.exp(np.log(np.clip(glaze, 1e-3, 1)) * strength[..., None])
    out = paper * (0.975 + 0.025 * tooth)[..., None] * glaze * under[..., None]
    out = cv2.GaussianBlur(out, (0, 0), 0.3)        # the paper's fibre softens every edge a little
    return np.clip(out * 255, 0, 255).astype(np.uint8), None


# ------------------------------------------------------------------ outputs

def write_pencil_svg(path, cv, size, figure_parts, title):
    w, h = size
    paper = "#%02x%02x%02x" % PAPER["colored-pencil"]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
           f"<title>{title}</title>", f'<rect width="{w}" height="{h}" fill="{paper}"/>']
    layers = {}
    for layer, width, alpha, pencil, pts in cv.strokes:
        layers.setdefault(layer, []).append((width, alpha, pencil, pts))
    for layer in ["construction"] + [P["name"] for P in PENCIL_PASSES] + ["detail", "accents", "edges"]:
        if layer not in layers:
            continue
        out.append(f'<g id="{layer}" data-stage="{layer}" fill="none" stroke-linecap="round">')
        bins = {}
        for width, alpha, pencil, pts in layers[layer]:
            k = max(1, len(pts) // 5)
            pts = pts[::k] + ([pts[-1]] if (len(pts) - 1) % k else [])
            d = "M" + "L".join(f"{round(x)} {round(y)}" for x, y in pts)
            bins.setdefault((pencil, round(width * 4) / 4, round(alpha * 10) / 10), []).append(d)
        for (pencil, width, alpha), ds in sorted(bins.items()):
            name, rgb = PENCILS[pencil]
            out.append(f'<path data-pencil="{name}" stroke="#%02x%02x%02x" stroke-width="{width:g}" '
                       f'stroke-opacity="{alpha:g}" d="{"".join(ds)}"/>' % rgb)
        out.append("</g>")
    if figure_parts:
        out.append('<g id="figure-gate" data-figure="sitter" fill="none" stroke="none" opacity="0">')
        for name, poly, contact in figure_parts:
            d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in poly) + " Z"
            c = f' data-contact="{contact}"' if contact else ""
            out.append(f'<path id="{name}" data-part="{name}"{c} d="{d}" fill="#000"/>')
        out.append("</g>")
    out.append("</svg>")
    Path(path).write_text("\n".join(out), encoding="utf-8")


def draw(args, ref=None, source=None):
    """Same contract as portrait_pipeline.draw, for the colour media."""
    pp._need()
    import cv2
    import numpy as np
    t0 = time.time()
    medium = args.medium
    rng = np.random.default_rng(args.seed)
    crop = [int(v) for v in args.crop.split(",")] if getattr(args, "crop", None) else None
    if ref is None:
        ref, box = pp.load_reference(args.photo, crop)
    else:
        box = [0, 0, ref.shape[1], ref.shape[0]]
    if args.scale != 1.0:
        ref = cv2.resize(ref, None, fx=args.scale, fy=args.scale, interpolation=cv2.INTER_CUBIC)
    h, w = ref.shape[:2]
    meas = pp.measure(ref, args.models)
    subject = getattr(args, "subject", "auto")
    person = subject == "portrait" or (subject == "auto" and pp.has_person(meas["labels"]))
    if not person:
        meas["labels"], _ = pp.scene_regions(ref, meas["labels"])
        meas["landmarks"] = None
    stats = {}
    fn = {"colored-pencil": draw_pencil, "oil": draw_oil, "watercolor": draw_watercolor}[medium]
    saved = {k: dict(v) for k, v in pp.REGION_STYLE.items()}
    try:
        if not person:
            pp.REGION_STYLE["background"].update(val=0.92, floor=0.0, straight="free", off=1.0, ang=25.0, coh=0.85,
                                                 ln=0.8)
            pp.REGION_STYLE["other"].update(val=1.0, coh=0.85, straight="free", ln=0.7)
        rgb, cv = fn(ref, meas, person, args, stats, rng)
    finally:
        pp.REGION_STYLE.clear()
        pp.REGION_STYLE.update(saved)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    name = args.name
    cv2.imwrite(str(out / f"{name}.png"), cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
    labels, lm = meas["labels"], meas["landmarks"]
    parts = pp.figure_parts(labels, lm) if person else []
    svg = None
    if cv is not None:
        svg = out / f"{name}.svg"
        write_pencil_svg(svg, cv, (w, h), parts, f"{name}: coloured pencil drawing from strokes")
    else:     # painted media: the figure gate travels in a small SVG beside the PNG
        svg = out / f"{name}.svg"
        Path(svg).write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" '
            f'height="{h}" viewBox="0 0 {w} {h}"><title>{name}: {medium}</title>'
            f'<image href="{name}.png" width="{w}" height="{h}"/>'
            + ('<g id="figure-gate" data-figure="sitter" fill="none" stroke="none" opacity="0">'
               + "".join(f'<path id="{n}" data-part="{n}"' + (f' data-contact="{c}"' if c else "")
                         + ' d="M' + " L".join(f"{x:.1f} {y:.1f}" for x, y in poly) + ' Z" fill="#000"/>'
                         for n, poly, c in parts) + "</g>" if parts else "")
            + "</svg>", encoding="utf-8")
    # colour media aim at the reference's own values (no graphite keying): darkness = 1 - lightness
    D = 1.0 - cv2.cvtColor(cv2.bilateralFilter(ref, 0, 18, 3), cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0
    np.save(out / "_target_darkness.npy", D.astype(np.float16))
    np.save(out / "_labels.npy", labels)
    np.save(out / "_target_colour.npy", cv2.resize(_target(ref), (max(1, w // 4), max(1, h // 4)),
                                                   interpolation=cv2.INTER_AREA).astype(np.float16))
    src_path = Path(source or args.photo)
    strokes = len(cv.strokes) if cv is not None else sum(v for k, v in stats.items() if k.startswith("brush"))
    canvas = {"colored-pencil": "strokes_only", "oil": "brush_strokes_only",
              "watercolor": "washes_and_strokes"}[medium]
    rec = {"schema": pp.SCHEMA, "source": src_path.name, "source_kind": "imagined" if source else "photo",
           "source_sha256": hashlib.sha256(src_path.read_bytes()).hexdigest(),
           "subject": "portrait" if person else "scene", "medium": medium, "crop_box": box, "scale": args.scale,
           "size": [w, h], "seed": args.seed, "engines": meas["engine"], "canvas_source": canvas,
           "photo_pixels_in_output": False, "strokes": int(strokes), "strokes_by_stage": stats,
           "palette": [n for n, _ in PENCILS] if medium == "colored-pencil" else None,
           "proportions": pp.proportions(lm),
           "methods": {"colored-pencil": ["PM-01", "PM-02", "PM-07", "PM-08", "PM-10", "PM-11", "PM-19", "PM-20"],
                       "oil": ["PM-04", "PM-06", "PM-21", "PM-22"],
                       "watercolor": ["PM-03", "PM-10", "PM-23", "PM-24"]}[medium],
           "seconds": round(time.time() - t0, 1), "png": str(out / f"{name}.png"), "svg": str(svg),
           "honesty": {"colored-pencil": "Every mark is a generated stroke of one of 30 named pencils.",
                       "oil": "Every mark is a generated brush stroke; each stroke's colour is sampled from a "
                              "blurred reference (the mixed colour), relief and weave are simulated.",
                       "watercolor": "Washes are flat per shape (the mean the shape needs) plus a pencil "
                                     "underdrawing; edges, granulation and whites are simulated."}[medium]
           + " Algorithmic rendering, not a human hand."}
    (out / "receipt.json").write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: rec[k] for k in ("subject", "medium", "strokes", "seconds", "png", "svg")}, ensure_ascii=False))


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("draw")
    d.add_argument("--photo", required=True)
    d.add_argument("--out", required=True)
    d.add_argument("--name", default="painting")
    d.add_argument("--models")
    d.add_argument("--crop")
    d.add_argument("--scale", type=float, default=1.0)
    d.add_argument("--blend", type=float, default=0.55)
    d.add_argument("--seed", type=int, default=7)
    d.add_argument("--medium", choices=COLOR_MEDIA, default="colored-pencil")
    d.add_argument("--subject", choices=("auto", "portrait", "scene"), default="auto")
    sub.add_parser("palette")
    a = ap.parse_args(argv)
    if a.cmd == "palette":
        for n, c in PENCILS:
            print(f"{n:16s} #%02x%02x%02x" % c)
        return 0
    return draw(a) or 0


if __name__ == "__main__":
    sys.exit(main())
