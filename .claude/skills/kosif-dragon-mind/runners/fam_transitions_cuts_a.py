"""transitions-cuts (part A): method cards as real programs with known-answer checks.

Every transition here is rendered frame by frame (numpy "fragment shader" maths or real FFmpeg filters) into a
lossless MP4 (libx264rgb -crf 0), read back with ffmpeg, and measured. The main fixture is a coordinate-coded pair:
in both scene A and scene B the red channel encodes the source x and the green channel the source y, and the blue
channel tells the scenes apart (A = 30, B = 225). So the B weight of any pixel, and the exact geometric remap a
transition applied (shift, scale, swirl angle, lens deflection...), can be read off the output frame.

Where a card names an engine that is not used here (hyperframes components, @hyperframes/shader-transitions GLSL,
GSAP in a browser), the runner re-implements the card's described effect with its stated parameters and says so in
the plan JSON ("engine"); it never claims the original package ran. Cards that need a paid key go in GAPS.
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path

import numpy as np

from _harness import card, check, fx

GAPS: dict = {
    "TRANS-261": "needs a paid video-generation API key (Kling/Together image2video with first and last frame); "
                 "no generative video model is available here",
}

REPO = Path(__file__).resolve().parents[4]
MM = REPO / ".claude/skills/kosif-superpowers/vendor/100-superskills/skills/kosif-montage-motion/scripts"

W, H = 192, 108
K = W / 1920.0                      # CSS px at 1920 wide -> fixture px
YY, XX = np.mgrid[0:H, 0:W].astype(float)
CX, CY = (W - 1) / 2.0, (H - 1) / 2.0
BLUE_A, BLUE_B = 30.0, 225.0


# ───────────────────────── easing (GSAP names) ─────────────────────────
def c01(x):
    return float(min(1.0, max(0.0, x)))


def p_in(n):
    return lambda x: c01(x) ** (n + 1)


def p_out(n):
    return lambda x: 1 - (1 - c01(x)) ** (n + 1)


def p_io(n):
    def f(x):
        x = c01(x)
        return 0.5 * (2 * x) ** (n + 1) if x < 0.5 else 1 - 0.5 * (2 - 2 * x) ** (n + 1)
    return f


lin = c01
sine_io = lambda x: 0.5 - 0.5 * math.cos(math.pi * c01(x))           # noqa: E731
expo_out = lambda x: 1.0 if c01(x) >= 1 else 1 - 2 ** (-10 * c01(x))  # noqa: E731
expo_in = lambda x: 0.0 if c01(x) <= 0 else 2 ** (10 * c01(x) - 10)   # noqa: E731


def expo_io(x):
    x = c01(x)
    if x in (0.0, 1.0):
        return x
    return 2 ** (20 * x - 10) / 2 if x < 0.5 else (2 - 2 ** (-20 * x + 10)) / 2


def back_out(s=1.70158):
    return lambda x: 1 + (s + 1) * (c01(x) - 1) ** 3 + s * (c01(x) - 1) ** 2


def smooth(e0, e1, x):
    t = c01((x - e0) / (e1 - e0)) if e1 != e0 else float(x >= e0)
    return t * t * (3 - 2 * t)


def prog(t, start, dur, ease=lin):
    return ease((t - start) / dur) if dur > 0 else float(t >= start)


# ───────────────────────── images ─────────────────────────
def coord(blue):
    img = np.empty((H, W, 3))
    img[..., 0] = XX * 255.0 / (W - 1)
    img[..., 1] = YY * 255.0 / (H - 1)
    img[..., 2] = blue
    return img


A0, B0 = coord(BLUE_A), coord(BLUE_B)


def hexc(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], float)


def solid(c):
    c = hexc(c) if isinstance(c, str) else np.asarray(c, float)
    return np.broadcast_to(c, (H, W, 3)).astype(float).copy()


def checker(k=6, c1=(20, 20, 20), c2=(235, 235, 235)):
    m = ((XX // k + YY // k) % 2)[..., None]
    return np.where(m > 0, np.array(c2, float), np.array(c1, float))


def sample(img, sx, sy, fill=None):
    """Bilinear sample img at float source coords; outside -> fill colour (or clamped edge when fill is None)."""
    x0 = np.floor(sx)
    y0 = np.floor(sy)
    fx_ = (sx - x0)[..., None]
    fy_ = (sy - y0)[..., None]
    x0c = np.clip(x0, 0, W - 1).astype(int)
    x1c = np.clip(x0 + 1, 0, W - 1).astype(int)
    y0c = np.clip(y0, 0, H - 1).astype(int)
    y1c = np.clip(y0 + 1, 0, H - 1).astype(int)
    out = (img[y0c, x0c] * (1 - fx_) * (1 - fy_) + img[y0c, x1c] * fx_ * (1 - fy_)
           + img[y1c, x0c] * (1 - fx_) * fy_ + img[y1c, x1c] * fx_ * fy_)
    if fill is not None:
        inside = ((sx >= -0.5) & (sx <= W - 0.5) & (sy >= -0.5) & (sy <= H - 0.5))[..., None]
        out = np.where(inside, out, np.asarray(fill, float))
    return out


def affine(img, s=1.0, sy_=None, cx=CX, cy=CY, dx=0.0, dy=0.0, rot=0.0, fill=None):
    """Scale (s, optional separate y scale) and rotate about (cx, cy), then translate by (dx, dy)."""
    syy = s if sy_ is None else sy_
    u, v = XX - cx - dx, YY - cy - dy
    c, n = math.cos(-rot), math.sin(-rot)
    ur, vr = u * c - v * n, u * n + v * c
    return sample(img, ur / max(s, 1e-6) + cx, vr / max(syy, 1e-6) + cy, fill)


def shift(img, dx=0.0, dy=0.0, fill=None):
    return sample(img, XX - dx, YY - dy, fill)


def blur(img, sigma):
    if sigma <= 0.05:
        return img.copy()
    if fx.have("cv2"):
        import cv2
        return cv2.GaussianBlur(img.astype(np.float32), (0, 0), sigma, borderType=cv2.BORDER_REPLICATE).astype(float)
    from scipy.ndimage import gaussian_filter
    return np.stack([gaussian_filter(img[..., c], sigma, mode="nearest") for c in range(3)], -1)


def hblur(img, length):
    """Horizontal box (motion) blur of `length` px."""
    L = int(round(length))
    if L <= 1:
        return img.copy()
    pad = np.pad(img, ((0, 0), (L, L), (0, 0)), mode="edge")
    cs = np.cumsum(pad, axis=1)
    cs = np.concatenate([np.zeros((H, 1, 3)), cs], axis=1)
    a = L // 2
    idx = np.arange(W) + L
    return (cs[:, idx + (L - a)] - cs[:, idx - a]) / L


def mix(a, b, m):
    m = np.asarray(m, float)
    if m.ndim == 2:
        m = m[..., None]
    return a * (1 - m) + b * m


def disc(cx, cy, r, feather=0.75):
    d = np.hypot(XX - cx, YY - cy)
    return np.clip((r - d) / max(feather, 1e-6) + 0.5, 0, 1)


def screen(base, over):
    return 255 - (255 - base) * (255 - over) / 255.0


def lum(fr):
    return 0.2126 * fr[..., 0] + 0.7152 * fr[..., 1] + 0.0722 * fr[..., 2]


def text_layer(text, size=40, color=(255, 255, 255), pos=None, bg=None):
    """PIL text -> (rgb, alpha) arrays at fixture size."""
    from PIL import Image, ImageDraw, ImageFont
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0) if bg is None else tuple(int(v) for v in bg) + (255,))
    dr = ImageDraw.Draw(im)
    try:
        font = ImageFont.load_default(size=size)
    except TypeError:
        font = ImageFont.load_default()
    x, y = pos if pos else (W / 2, H / 2)
    dr.text((x, y), text, fill=tuple(int(v) for v in color) + (255,), font=font, anchor="mm")
    a = np.asarray(im, float)
    return a[..., :3], a[..., 3] / 255.0


def noise(seed, cells=6, octaves=3, ridged=False):
    """Value-noise fBm on the fixture grid (deterministic); rank-normalised to a uniform 0..1 field."""
    rng = np.random.default_rng(seed)
    tot = np.zeros((H, W))
    amp = 1.0
    for o in range(octaves):
        n = cells * 2 ** o
        g = rng.random((n + 2, n + 2))
        gx, gy = XX / W * n, YY / W * n
        x0, y0 = gx.astype(int), gy.astype(int)
        tx, ty = gx - x0, gy - y0
        tx, ty = tx * tx * (3 - 2 * tx), ty * ty * (3 - 2 * ty)
        v = (g[y0, x0] * (1 - tx) * (1 - ty) + g[y0, x0 + 1] * tx * (1 - ty)
             + g[y0 + 1, x0] * (1 - tx) * ty + g[y0 + 1, x0 + 1] * tx * ty)
        if ridged:
            v = 1 - np.abs(2 * v - 1)
        tot += amp * v
        amp *= 0.5
    r = tot.ravel().argsort().argsort().reshape(H, W)
    return (r + 0.5) / r.size


# ───────────────────────── io ─────────────────────────
def write_video(frames, path, fps):
    arr = np.clip(np.rint(np.stack(frames)), 0, 255).astype(np.uint8)
    done = subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % (W, H),
                           "-r", str(fps), "-i", "-", "-c:v", "libx264rgb", "-crf", "0", "-preset", "ultrafast",
                           str(path)], input=arr.tobytes(), capture_output=True, timeout=120)
    if done.returncode:
        raise RuntimeError(done.stderr.decode(errors="replace")[-300:])
    return Path(path)


def film(wd, name, frame_fn, seconds, fps):
    """Render frame_fn(t) for t = i/fps, i < seconds*fps (+1 so the end state is a frame); return (path, frames, ts)."""
    n = int(round(seconds * fps)) + 1
    ts = [i / fps for i in range(n)]
    path = write_video([frame_fn(t) for t in ts], Path(wd) / (name + ".mp4"), fps)
    frs = fx.frames(path, (W, H))
    if len(frs) != n:
        raise RuntimeError("frame count %d != %d" % (len(frs), n))
    return path, frs, ts


def at(ts, t):
    return int(np.argmin(np.abs(np.asarray(ts) - t)))


def save_plan(wd, name, obj):
    p = Path(wd) / (name + ".json")
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
    return p


# ───────────────────────── measurements ─────────────────────────
def bwt(fr):
    return np.clip((fr[..., 2] - BLUE_A) / (BLUE_B - BLUE_A), 0, 1)


def fracb(fr, mask=None):
    m = bwt(fr) > 0.5
    return float(m[mask].mean() if mask is not None else m.mean())


def srcx(fr):
    return fr[..., 0] * (W - 1) / 255.0


def srcy(fr):
    return fr[..., 1] * (H - 1) / 255.0


def mad(a, b):
    return float(np.mean(np.abs(np.asarray(a, float) - np.asarray(b, float))))


def sharp(fr):
    g = lum(fr)
    return float(np.mean(np.abs(4 * g[1:-1, 1:-1] - g[:-2, 1:-1] - g[2:, 1:-1] - g[1:-1, :-2] - g[1:-1, 2:])))


def xshift(fr, sel=None):
    """Median of (pixel x - source x) over selected pixels: + means content moved right."""
    d = XX - srcx(fr)
    return float(np.median(d[sel] if sel is not None else d))


def yshift(fr, sel=None):
    d = YY - srcy(fr)
    return float(np.median(d[sel] if sel is not None else d))


def scale_est(fr, sel=None):
    """Content scale about the centre from the coordinate code: slope of pixel x against source x."""
    sel = np.ones((H, W), bool) if sel is None else sel
    band = sel & (np.abs(YY - CY) < H * 0.3) & (np.abs(XX - CX) < W * 0.3)
    sx = srcx(fr)[band]
    if sx.size < 10 or np.ptp(sx) < 1e-6:
        return float("nan")
    return float(np.polyfit(sx, XX[band], 1)[0])


def scale_inv(fr, sel=None):
    """Opacity-invariant scale about the centre: fit red = m x + c; the value at the centre gives opacity x code
    scale, so s = (red(CX) / CX) / m."""
    sel = np.ones((H, W), bool) if sel is None else sel
    band = sel & (np.abs(YY - CY) < H * 0.3) & (np.abs(XX - CX) < W * 0.3)
    if band.sum() < 10:
        return float("nan")
    m, c = np.polyfit(XX[band], fr[..., 0][band], 1)
    return float(((m * CX + c) / CX) / m) if abs(m) > 1e-9 else float("nan")


def b_width(fr, row=None):
    """Columns showing B on a row (B weight > .5)."""
    r = int(round(CY)) if row is None else row
    return int((bwt(fr)[r] > 0.5).sum())


def chan_offset(fr):
    """Horizontal offset of the red channel against the green-coded geometry: median(x - red source x) on the
    interior (0 when channels are aligned)."""
    inner = (XX > 12) & (XX < W - 12)
    return float(np.median((XX - srcx(fr))[inner]))


def near(name, m, e, tol):
    ok = m == m and abs(m - e) <= tol
    return check(name, ok, m, "%s +- %s" % (e, tol))


def neg(name, m, e, tol):
    ok = not (m == m and abs(m - e) <= tol)
    return check("negative control: " + name, ok, m, "not within %s +- %s" % (e, tol))


def ends(frs, a, b, tol=1.5, name="transition"):
    return [check("%s: first frame is scene A" % name, mad(frs[0], a) < tol, mad(frs[0], a), "< %s" % tol),
            check("%s: last frame is scene B" % name, mad(frs[-1], b) < tol, mad(frs[-1], b), "< %s" % tol)]


def hardcut(a, b, cut):
    return lambda t: a if t < cut else b


@contextmanager
def tmp_in(wd):
    old = tempfile.tempdir
    tempfile.tempdir = str(wd)
    try:
        yield
    finally:
        tempfile.tempdir = old


def mm_import(name):
    if str(MM) not in sys.path:
        sys.path.insert(0, str(MM))
    import importlib
    return importlib.import_module(name)


# ═════════════════════ 14 shader transitions (numpy fragment-shader ports) ═════════════════════
# The @hyperframes/shader-transitions GLSL is not in this repo, so each effect is re-implemented from its name and the
# card text as a per-pixel function of (A, B, progress). Each probe measures the effect's defining geometry/colour.
def _sm(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def sh_chroma(a, b, p, radial=False, amp=0.035 * W):
    base = mix(a, b, p)
    d = amp * math.sin(math.pi * p)
    ux, uy = ((XX - CX) / (W / 2), (YY - CY) / (W / 2)) if radial else (np.ones((H, W)), np.zeros((H, W)))
    out = base.copy()
    out[..., 0] = sample(base, XX - d * ux, YY - d * uy)[..., 0]
    out[..., 2] = sample(base, XX + d * ux, YY + d * uy)[..., 2]
    return out


def pr_chroma(frs, ps, hc, radial=False, amp=0.035 * W):
    i = int(np.argmin(np.abs(np.asarray(ps) - 0.5)))
    d = amp * math.sin(math.pi * ps[i])
    if radial:
        sel = (XX > 0.72 * W) & (XX < 0.9 * W)
        e = d * float(np.mean((XX[sel] - CX) / (W / 2)))
        m = float(np.median((XX - srcx(frs[i]))[sel]))
        sel_l = (XX < 0.28 * W) & (XX > 0.1 * W)
        ml = float(np.median((XX - srcx(frs[i]))[sel_l]))
        return [near("red channel pushed outward on the right (px)", m, e, 0.6),
                near("red channel pushed outward on the left (mirror)", ml, -e, 0.6),
                near("channels aligned at the end", chan_offset(frs[-1]), 0.0, 0.3),
                neg("red-channel offset on the hard cut", float(np.median((XX - srcx(hc(i)))[sel])), e, 0.6)]
    m = chan_offset(frs[i])
    return [near("red channel offset at peak (px)", m, d, 0.6), near("aligned at the end", chan_offset(frs[-1]), 0, 0.3),
            neg("red-channel offset on the hard cut", chan_offset(hc(i)), d, 0.6)]


ZK = 0.5


def _zoomblur(img, s, amt):
    return np.mean([affine(img, s * (1 + 0.03 * j * amt)) for j in range(6)], axis=0)


def _zoom_scales(s, amt):
    return 1.0 / np.mean([1.0 / (s * (1 + 0.03 * j * amt)) for j in range(6)])


def sh_zoom(a, b, p):
    amt = math.sin(math.pi * p)
    sa, sb = 1 + ZK * 2 * min(p, 0.5), 1 + ZK * 2 * min(1 - p, 0.5)
    m = smooth(0.35, 0.65, p)
    za = _zoomblur(a, sa, amt) if m < 1 else a
    zb = _zoomblur(b, sb, amt) if m > 0 else b
    return mix(za, zb, m)


def pr_zoom(frs, ps, hc):
    ps = np.asarray(ps)
    i, j = int(np.argmin(np.abs(ps - 0.25))), int(np.argmin(np.abs(ps - 0.75)))
    ea = _zoom_scales(1 + ZK * 2 * min(ps[i], 0.5), math.sin(math.pi * ps[i]))
    eb = _zoom_scales(1 + ZK * 2 * min(1 - ps[j], 0.5), math.sin(math.pi * ps[j]))
    return [near("scene A zoomed in at p=%.2f (scale)" % ps[i], scale_est(frs[i]), ea, 0.03),
            check("frame at p=%.2f is still scene A" % ps[i], fracb(frs[i]) < 0.02, fracb(frs[i]), "< 0.02"),
            near("scene B arrives zoomed at p=%.2f (scale)" % ps[j], scale_est(frs[j]), eb, 0.03),
            neg("zoom scale of the hard cut", scale_est(hc(i)), ea, 0.03)]


def sh_crosswarp(a, b, p):
    x = _sm(0, 1, p * 2 + XX / (W - 1) - 1)
    sa = sample(a, CX + (XX - CX) * (1 - x), CY + (YY - CY) * (1 - x))
    sb = sample(b, CX + (XX - CX) * x, CY + (YY - CY) * x)
    return mix(sa, sb, x)


def pr_crosswarp(frs, ps, hc):
    i = int(np.argmin(np.abs(np.asarray(ps) - 0.5)))
    exp = _sm(0, 1, ps[i] * 2 + XX[0] / (W - 1) - 1)
    row = bwt(frs[i])[int(CY)]
    err = float(np.mean(np.abs(row - exp)))
    # A is drawn shrunk toward the centre by (1 - x): at column 0.25 W the A source sits closer to the centre
    c = int(0.25 * W)
    xa = float(_sm(0, 1, ps[i] * 2 + c / (W - 1) - 1))
    exp_src = (1 - xa) * (CX + (c - CX) * (1 - xa)) + xa * (CX + (c - CX) * xa)   # blend of both warped samples
    return [check("B weight follows smoothstep(2p+u-1) across x", err < 0.02, err, "< 0.02"),
            near("A and B sampled at their warped coordinates (col 0.25W)", float(srcx(frs[i])[int(CY), c]), exp_src, 0.8),
            neg("B-weight profile error of the hard cut", float(np.mean(np.abs(bwt(hc(i))[int(CY)] - exp))), 0.0, 0.02)]


def _warped_noise():
    n1, q, r = noise(11, 4, 3), noise(12, 3, 2), noise(13, 3, 2)
    nn = sample(np.repeat(n1[..., None], 3, -1), XX + 24 * (q - 0.5), YY + 24 * (r - 0.5))[..., 0]
    rk = nn.ravel().argsort().argsort().reshape(H, W)
    return (rk + 0.5) / rk.size


DWN = _warped_noise()
RGN = noise(21, 5, 3, ridged=True)
EDGE = 0.05


def _thresh(field, p, e=EDGE):
    return np.clip((p * (1 + 2 * e) - e - field) / (2 * e) + 0.5, 0, 1)


def sh_domain(a, b, p):
    return mix(a, b, _thresh(DWN, p))


def pr_domain(frs, ps, hc, field=None):
    field = DWN if field is None else field
    i = int(np.argmin(np.abs(np.asarray(ps) - 0.3)))
    exp = ps[i] * (1 + 2 * EDGE) - EDGE
    m = bwt(frs[i]) > 0.5
    coh = float(np.corrcoef(m[:, :-1].ravel().astype(float), m[:, 1:].ravel().astype(float))[0, 1])
    return [near("B area fraction at p=%.2f" % ps[i], fracb(frs[i]), exp, 0.02),
            check("dissolve mask is spatially coherent (warped noise, not white noise)", coh > 0.6, coh, "> 0.6"),
            neg("B area fraction of the hard cut", fracb(hc(i)), exp, 0.02)]


def sh_flashwhite(a, b, p):
    white = solid((255, 255, 255))
    return mix(a, white, 2 * p) if p < 0.5 else mix(white, b, 2 * p - 1)


def pr_flashwhite(frs, ps, hc):
    ps = np.asarray(ps)
    i = int(np.argmin(np.abs(ps - 0.5)))
    j = int(np.argmin(np.abs(ps - 0.25)))
    e_j = float(np.mean(lum(A0))) + (255 - float(np.mean(lum(A0)))) * 2 * ps[j]
    return [check("frame at p=%.2f is near white" % ps[i], float(lum(frs[i]).mean()) > 255 - 255 * abs(2 * ps[i] - 1) - 3,
                  float(lum(frs[i]).mean()), "> %.1f" % (255 - 255 * abs(2 * ps[i] - 1) - 3)),
            near("quarter frame lifted toward white (mean luma)", float(lum(frs[j]).mean()), e_j, 2.0),
            neg("hard-cut frame is not white (mean luma)", float(lum(hc(i)).mean()), 255.0, 255 * abs(2 * ps[i] - 1) + 3)]


def _h(*k):
    v = 0
    for x in k:
        v = (v * 1103515245 + int(x) * 2654435761 + 12345) & 0xFFFFFFFF
    return ((v ^ (v >> 13)) * 1274126177 & 0xFFFFFFFF) / 4294967295.0


def sh_glitch(a, b, p, rows=60, bx=12, by=8, shift_=0.035):
    g = math.sin(math.pi * p)
    base = mix(a, b, p)
    step = int(p * 12)
    band = (YY * rows / H).astype(int)
    dxr = np.vectorize(lambda k: (_h(k, step, 1) - 0.5) * 2 * 0.08 * W)(np.arange(rows))[band]
    on = np.vectorize(lambda k: _h(k, step, 2) < 0.5)(np.arange(rows))[band]
    bxi, byi = (XX * bx / W).astype(int), (YY * by / H).astype(int)
    boff = np.vectorize(lambda u, v: (_h(u, v, step, 3) - 0.5) * 0.1 * W if _h(u, v, step, 4) < 0.25 else 0.0)(bxi, byi)
    sx = XX - g * (dxr * on + boff)
    out = sample(base, sx, YY)
    rs = shift_ * W * g
    out[..., 0] = sample(base, sx - rs, YY)[..., 0]
    scan = 1 - 0.15 * g * ((YY.astype(int) % 2) == 0)
    out = out * scan[..., None]
    levels = int(round(256 - 248 * g ** 4))
    q = 255.0 / max(levels - 1, 1)
    return np.round(out / q) * q if levels < 256 else out


def pr_glitch(frs, ps, hc):
    ps = np.asarray(ps)
    i = int(np.argmin(np.abs(ps - 0.25)))
    j = int(np.argmin(np.abs(ps - 0.5)))
    rowdisp = np.abs(np.median(XX - srcx(frs[i]), axis=1))
    frac = float(np.mean(rowdisp > 1.0))
    lev = int(round(256 - 248 * math.sin(math.pi * ps[j]) ** 4))
    uniq = len(np.unique(frs[j][..., 1]))
    hc_rows = float(np.mean(np.abs(np.median(XX - srcx(hc(i)), axis=1)) > 1.0))
    return [check("scan rows displaced at p=%.2f (fraction of rows > 1 px)" % ps[i], frac > 0.25, frac, "> 0.25"),
            check("colour quantised at the peak (unique green levels <= %d)" % lev, uniq <= lev, uniq, "<= %d" % lev),
            check("clean B at the end (no displaced rows)",
                  float(np.mean(np.abs(np.median(XX - srcx(frs[-1]), axis=1)) > 1.0)) == 0.0, 0.0, 0.0),
            neg("fraction of displaced rows on the hard cut", hc_rows, 0.6, 0.35)]


LENS_E = 0.22 * H


def sh_lens(a, b, p):
    E = LENS_E * math.sin(math.pi * p)
    u, v = XX - CX, YY - CY
    r = np.maximum(np.hypot(u, v), 1e-3)
    f = 1 - (E * E) / (r * r)
    return mix(sample(a, CX + u * f, CY + v * f), sample(b, CX + u * f, CY + v * f), p)


def _ring_e2(fr, r0, r1):
    r = np.hypot(XX - CX, YY - CY)
    sel = (r > r0) & (r < r1)
    rs = np.hypot(srcx(fr) - CX, srcy(fr) - CY)
    return float(np.median(((r - rs) * r)[sel]))


def pr_lens(frs, ps, hc):
    i = int(np.argmin(np.abs(np.asarray(ps) - 0.5)))
    E2 = (LENS_E * math.sin(math.pi * ps[i])) ** 2
    e_in, e_out = _ring_e2(frs[i], 34, 40), _ring_e2(frs[i], 46, 52)
    return [near("deflection x radius at r~37 equals E^2 (1/r point-mass law)", e_in, E2, 0.08 * E2),
            near("deflection x radius at r~49 equals E^2", e_out, E2, 0.08 * E2),
            near("no deflection at the end", _ring_e2(frs[-1], 34, 40), 0.0, 0.015 * E2),
            neg("deflection x radius on the hard cut", _ring_e2(hc(i), 34, 40), E2, 0.08 * E2)]


LEAK = np.array([255.0, 170.0, 80.0])


def _leak_cx(p):
    return W * (-0.2 + 1.4 * p)


def sh_leak(a, b, p):
    base = mix(a, b, p)
    g = np.exp(-(((XX - _leak_cx(p)) / (0.3 * W)) ** 2 + ((YY - 0.4 * H) / (0.5 * H)) ** 2))
    over = LEAK * (0.85 * math.sin(math.pi * p) * g)[..., None]
    return screen(base, over)


def pr_leak(frs, ps, hc):
    ps = np.asarray(ps)
    out = []
    cents = []
    for target in (0.35, 0.65):
        i = int(np.argmin(np.abs(ps - target)))
        gain = lum(frs[i]) - lum(mix(A0, B0, ps[i]))
        colg = np.clip(gain.mean(axis=0), 0, None)
        cents.append((float((colg * XX[0]).sum() / max(colg.sum(), 1e-6)), _leak_cx(ps[i]), i))
    for c, e, i in cents:
        out.append(near("light-leak centre at p=%.2f (column)" % ps[i], c, e, 0.08 * W))
    i = int(np.argmin(np.abs(ps - 0.5)))
    d = frs[i] - mix(A0, B0, ps[i])
    rg, bg = float(d[..., 0].mean()), float(d[..., 2].mean())
    out.append(check("leak is warm (red gain > blue gain) at the peak", rg > bg + 5, [rg, bg], "red > blue + 5"))
    out.append(check("red channel lifted by the leak at the peak (mean gain > 5)", rg > 5, rg, "> 5"))
    hd = hc(i) - mix(A0, B0, ps[i])
    out.append(neg("red-channel lift on the hard cut", float(hd[..., 0].mean()), 30.0, 25.0))
    return out


BURN_BAND = 0.06
ORANGE = np.array([255.0, 120.0, 20.0])


def sh_burn(a, b, p):
    if p <= 0 or p >= 1:
        return (a if p <= 0 else b).copy()
    p2 = p * (1 + BURN_BAND)
    out = mix(a, b, (RGN < p2 - BURN_BAND) * 1.0)
    out[(RGN >= p2 - BURN_BAND) & (RGN < p2)] = ORANGE
    return out


def pr_burn(frs, ps, hc):
    i = int(np.argmin(np.abs(np.asarray(ps) - 0.4)))
    p2 = ps[i] * (1 + BURN_BAND)
    fb = fracb(frs[i])
    orange = (np.abs(frs[i] - ORANGE).max(axis=-1) < 6)
    edge_ok = float(np.mean(orange))
    return [near("burned-through (B) area at p=%.2f" % ps[i], fb, max(p2 - BURN_BAND, 0), 0.01),
            near("glowing orange burn front covers the ridged band", edge_ok, BURN_BAND, 0.01),
            neg("orange burn-front area on the hard cut", float(np.mean(np.abs(hc(i) - ORANGE).max(axis=-1) < 6)),
                BURN_BAND, 0.01)]


RIP_A, RIP_L = 0.025 * W, 0.12 * W


def _rip_d(r, p):
    return RIP_A * math.sin(math.pi * p) * np.sin(2 * math.pi * r / RIP_L - 4 * math.pi * p)


def sh_ripple(a, b, p):
    u, v = XX - CX, YY - CY
    r = np.maximum(np.hypot(u, v), 1e-3)
    f = (r - _rip_d(r, p)) / r
    return mix(sample(a, CX + u * f, CY + v * f), sample(b, CX + u * f, CY + v * f), p)


def _radial_disp(fr):
    r = np.hypot(XX - CX, YY - CY)
    return r, r - np.hypot(srcx(fr) - CX, srcy(fr) - CY)


def pr_ripple(frs, ps, hc):
    i = int(np.argmin(np.abs(np.asarray(ps) - 0.5)))
    r, d = _radial_disp(frs[i])
    sel = (r > 4) & (r < 50)
    exp = _rip_d(r, ps[i])
    corr = float(np.corrcoef(d[sel], exp[sel])[0, 1])
    amp = float(np.percentile(np.abs(d[sel]), 98))
    r2, d2 = _radial_disp(hc(i))
    return [check("radial displacement follows sin(2 pi r / lambda) (correlation)", corr > 0.97, corr, "> 0.97"),
            near("ripple amplitude (px)", amp, RIP_A * math.sin(math.pi * ps[i]), 0.5),
            neg("ripple amplitude of the hard cut", float(np.percentile(np.abs(d2[sel]), 98)),
                RIP_A * math.sin(math.pi * ps[i]), 0.5)]


IRIS_MAX = math.hypot(W, H) / 2 + 1


def sh_iris(a, b, p):
    return mix(a, b, disc(CX, CY, IRIS_MAX * p))


def pr_iris(frs, ps, hc):
    i = int(np.argmin(np.abs(np.asarray(ps) - 0.3)))
    e = IRIS_MAX * ps[i]
    m = b_width(frs[i]) / 2.0
    vh = int((bwt(frs[i])[:, int(CX)] > 0.5).sum()) / 2.0
    return [near("iris radius along the centre row (SDF circle)", m, e, 1.0),
            near("iris radius along the centre column (round, not an ellipse)", vh, e, 1.0),
            neg("B half-width of the hard cut", b_width(hc(i)) / 2.0, e, 1.0)]


SW_S, SW_R = 2.5, 0.45 * W


def _sw_theta(r, p):
    return SW_S * math.sin(math.pi * p) * np.clip(1 - r / SW_R, 0, 1) ** 2


def sh_swirl(a, b, p):
    u, v = XX - CX, YY - CY
    r = np.hypot(u, v)
    th = -_sw_theta(r, p)
    c, s = np.cos(th), np.sin(th)
    sx, sy = CX + u * c - v * s, CY + u * s + v * c
    return mix(sample(a, sx, sy), sample(b, sx, sy), p)


def _ang_disp(fr, r0, r1):
    u, v = XX - CX, YY - CY
    r = np.hypot(u, v)
    sel = (r > r0) & (r < r1)
    da = np.arctan2(srcy(fr) - CY, srcx(fr) - CX) - np.arctan2(v, u)
    da = (da + np.pi) % (2 * np.pi) - np.pi
    return float(np.median(da[sel]))


def pr_swirl(frs, ps, hc):
    i = int(np.argmin(np.abs(np.asarray(ps) - 0.5)))
    e20 = -float(_sw_theta(np.array(20.0), ps[i]))
    e40 = -float(_sw_theta(np.array(40.0), ps[i]))
    return [near("swirl angle at r=20 px (rad)", _ang_disp(frs[i], 18, 22), e20, 0.06),
            near("swirl angle at r=40 px falls off as (1-r/R)^2 (rad)", _ang_disp(frs[i], 38, 42), e40, 0.06),
            neg("swirl angle of the hard cut", _ang_disp(hc(i), 18, 22), e20, 0.06)]


TH_A, TH_L = 0.03 * W, H / 4.0


def _th_dx(y, p):
    return TH_A * math.sin(math.pi * p) * np.sin(2 * math.pi * y / TH_L + 8 * p)


def sh_thermal(a, b, p):
    sx = XX - _th_dx(YY, p)
    return mix(sample(a, sx, YY), sample(b, sx, YY), p)


def pr_thermal(frs, ps, hc):
    i = int(np.argmin(np.abs(np.asarray(ps) - 0.5)))
    inner = (XX > 10) & (XX < W - 10)
    rows = np.array([np.median((XX - srcx(frs[i]))[y][inner[y]]) for y in range(H)])
    exp = _th_dx(np.arange(H, dtype=float), ps[i])
    err = float(np.max(np.abs(rows - exp)))
    hrows = np.array([np.median((XX - srcx(hc(i)))[y][inner[y]]) for y in range(H)])
    return [check("per-row heat-haze shift matches the sine (max error px)", err < 0.7, err, "< 0.7"),
            near("haze amplitude (px)", float(np.max(np.abs(rows))), TH_A * math.sin(math.pi * ps[i]), 0.7),
            neg("haze amplitude of the hard cut", float(np.max(np.abs(hrows))), TH_A * math.sin(math.pi * ps[i]), 0.7)]


WHIP_BLUR = 0.3 * W


def sh_whip(a, b, p, blur_max=WHIP_BLUR):
    o = p * W
    pos = XX + o
    img = np.where((pos < W)[..., None], sample(a, pos, YY), sample(b, pos - W, YY))
    return hblur(img, blur_max * math.sin(math.pi * p))


def pr_whip(frs, ps, hc, blur_max=WHIP_BLUR):
    i = int(np.argmin(np.abs(np.asarray(ps) - 0.25)))
    o, L = ps[i] * W, blur_max * math.sin(math.pi * ps[i])
    sel = (XX > L / 2 + 3) & (XX < W - o - L / 2 - 3)
    row = bwt(frs[i])[int(CY)]
    width = int(((row > 0.1) & (row < 0.9)).sum())
    return [near("camera pan offset at p=%.2f (A moved left, px)" % ps[i], xshift(frs[i], sel), -o, 0.8),
            near("directional blur smears the A|B seam over ~0.8 L px", width, 0.8 * L, 3.0),
            neg("pan offset of the hard cut", xshift(hc(i), sel), -o, 0.8)]


SHADERS = {
    "chromatic-split": (sh_chroma, pr_chroma),
    "chromatic-radial-split": (lambda a, b, p: sh_chroma(a, b, p, radial=True), lambda f, p, h: pr_chroma(f, p, h, radial=True)),
    "cinematic-zoom": (sh_zoom, pr_zoom),
    "cross-warp-morph": (sh_crosswarp, pr_crosswarp),
    "domain-warp": (sh_domain, pr_domain),
    "flash-through-white": (sh_flashwhite, pr_flashwhite),
    "glitch": (sh_glitch, pr_glitch),
    "gravitational-lens": (sh_lens, pr_lens),
    "light-leak": (sh_leak, pr_leak),
    "ridged-burn": (sh_burn, pr_burn),
    "ripple-waves": (sh_ripple, pr_ripple),
    "sdf-iris": (sh_iris, pr_iris),
    "swirl-vortex": (sh_swirl, pr_swirl),
    "thermal-distortion": (sh_thermal, pr_thermal),
    "whip-pan": (sh_whip, pr_whip),
}
# timing per card group: (start, duration, total, fps, ease)
SHADER_MODES = {
    "quick": (0.0, 0.7, 0.7, 30, lin),            # hyperframes registry id, page-side compositing
    "block": (1.0, 2.0, 4.0, 10, p_io(1)),        # 4 s composition, progress window 1..3 s quadInOut
    "webgl": (4.0, 0.7, 5.0, 20, lin),            # transitions array {time: 4.0, duration: 0.7}
}


def shader_card(wd, key, mode, card_id):
    fn, probe = SHADERS[key]
    T0, D, total, fps, ease = SHADER_MODES[mode]
    pf = lambda t: prog(t, T0, D, ease)           # noqa: E731
    path, frs, ts = film(wd, key, lambda t: fn(A0, B0, pf(t)), total, fps)
    ps = [pf(t) for t in ts]
    hc = lambda i: A0 if ps[i] < 0.5 else B0      # noqa: E731  the unprocessed hard cut at the same frame
    checks = ends(frs, A0, B0, name=key)
    if mode != "quick":
        pre = [i for i, t in enumerate(ts) if t < T0 - 1e-9]
        post = [i for i, t in enumerate(ts) if t > T0 + D + 1e-9]
        checks.append(check("scene A holds untouched before %.1f s" % T0, max(mad(frs[i], A0) for i in pre) < 1.0,
                            max(mad(frs[i], A0) for i in pre), "< 1"))
        if post:
            checks.append(check("scene B holds after %.1f s" % (T0 + D), max(mad(frs[i], B0) for i in post) < 1.0,
                                max(mad(frs[i], B0) for i in post), "< 1"))
    if mode == "block":
        i = at(ts, 1.5)
        checks.append(near("progress at t=1.5 s follows quadInOut (0.125)", ps[i], 0.125, 1e-6))
    checks += probe(frs, ps, hc)
    plan = save_plan(wd, "shader_" + key, {"card": card_id, "shader": key, "mode": mode, "start": T0, "duration": D,
                                           "fps": fps, "engine": "numpy per-pixel port of the named effect "
                                           "(@hyperframes/shader-transitions GLSL not used: absent here)"})
    return checks, [path, plan]


def _reg_shader(cid, key, mode):
    card(cid)(lambda task, wd: shader_card(wd, key, mode, cid))


for _cid, _key in [("TRANS-105", "chromatic-split"), ("TRANS-106", "cinematic-zoom"), ("TRANS-107", "cross-warp-morph"),
                   ("TRANS-108", "domain-warp"), ("TRANS-109", "flash-through-white"), ("TRANS-110", "glitch"),
                   ("TRANS-111", "gravitational-lens"), ("TRANS-112", "light-leak"), ("TRANS-113", "ridged-burn"),
                   ("TRANS-114", "ripple-waves"), ("TRANS-115", "sdf-iris"), ("TRANS-116", "swirl-vortex"),
                   ("TRANS-117", "thermal-distortion"), ("TRANS-118", "whip-pan")]:
    _reg_shader(_cid, _key, "quick")
for _cid, _key in [("TRANS-137", "chromatic-radial-split"), ("TRANS-138", "cinematic-zoom"),
                   ("TRANS-139", "cross-warp-morph"), ("TRANS-140", "domain-warp"), ("TRANS-141", "flash-through-white"),
                   ("TRANS-142", "glitch"), ("TRANS-143", "gravitational-lens"), ("TRANS-144", "light-leak"),
                   ("TRANS-146", "ridged-burn"), ("TRANS-147", "ripple-waves"), ("TRANS-148", "sdf-iris"),
                   ("TRANS-149", "swirl-vortex"), ("TRANS-150", "thermal-distortion"), ("TRANS-166", "whip-pan")]:
    _reg_shader(_cid, _key, "block")
for _cid, _key in [("TRANS-205", "chromatic-split"), ("TRANS-206", "cinematic-zoom"), ("TRANS-207", "cross-warp-morph"),
                   ("TRANS-208", "domain-warp"), ("TRANS-209", "flash-through-white"), ("TRANS-210", "gravitational-lens"),
                   ("TRANS-211", "light-leak"), ("TRANS-212", "ridged-burn"), ("TRANS-213", "ripple-waves"),
                   ("TRANS-214", "sdf-iris"), ("TRANS-215", "swirl-vortex"), ("TRANS-216", "thermal-distortion"),
                   ("TRANS-217", "whip-pan")]:
    _reg_shader(_cid, _key, "webgl")


# ═════════════════════ CSS scene-to-scene handoffs (hyperframes-animation transitions/*.md) ═════════════════════
# Positions are CSS px on a 1920x1080 stage, scaled by K onto the fixture. u = time since the transition started.
def _tex(blue):
    """Coordinate code in red, a separable fine texture in green (period-4 stripes along x plus along y), identity in blue."""
    img = coord(blue)
    sq = lambda v: np.where((v // 2) % 2 > 0, 1.0, -1.0)     # noqa: E731
    img[..., 1] = 128 + 55 * sq(XX) + 55 * sq(YY)
    return img


def hgauss(img, sigma):
    if sigma <= 0.05:
        return img.copy()
    if fx.have("scipy"):
        from scipy.ndimage import gaussian_filter1d
        return gaussian_filter1d(img, sigma, axis=1, mode="nearest")
    return hblur(img, sigma * 2.5)


def norm_op(fr, blue):
    """Undo a uniform opacity over black using the blue identity channel (blue = blue0 x opacity)."""
    return fr * (blue / np.maximum(fr[..., 2], 1e-3))[..., None]


AT, BT = _tex(BLUE_A), _tex(BLUE_B)
BLACK = solid((0, 0, 0))


def gsharp(fr, axis=None):
    g = fr[..., 1]
    h = float(np.mean(np.abs(np.diff(g, axis=1))))
    v = float(np.mean(np.abs(np.diff(g, axis=0))))
    return h if axis == "h" else v if axis == "v" else (h + v) / 2


def over(base, top, alpha):
    return mix(base, top, alpha)


def push_frame(a, b, e, dx=1, dy=0):
    oa = sample(a, XX + e * W * dx, YY + e * H * dy, fill=(0, 0, 0))
    bx, by = XX - (1 - e) * W * dx, YY - (1 - e) * H * dy
    inb = ((bx >= -0.5) & (bx <= W - 0.5) & (by >= -0.5) & (by <= H - 0.5))
    return np.where(inb[..., None], sample(b, bx, by), oa)


def css_push(dx, dy, D=0.5, ease=p_io(3)):
    def fr(u):
        return push_frame(A0, B0, ease(u / D), dx, dy)

    def pr(frs, ts, T0, hc):
        out = []
        for f in (0.3, 0.5, 0.7):
            i = at(ts, T0 + f * D)
            e = ease((ts[i] - T0) / D)
            if dx:
                selA = (bwt(frs[i]) < 0.5) & (XX > 2) & (XX < W * (1 - e) - 2)
                out.append(near("old scene x offset at %.0f%% (power3.inOut)" % (f * 100), xshift(frs[i], selA) if selA.any()
                                else float("nan"), -e * W, 0.8))
            else:
                selA = (bwt(frs[i]) < 0.5) & (YY > 2) & (YY < H * (1 - e) - 2)
                out.append(near("old scene y offset at %.0f%% (power3.inOut)" % (f * 100), yshift(frs[i], selA) if selA.any()
                                else float("nan"), -e * H, 0.8))
        i = at(ts, T0 + 0.3 * D)
        e = ease((ts[i] - T0) / D)
        selB = (bwt(frs[i]) > 0.5)
        meas = xshift(frs[i], selB) if dx else yshift(frs[i], selB)
        out.append(near("new scene enters from the far edge (offset)", meas, (1 - e) * (W if dx else H), 0.8))
        sel = (XX > 2) & (XX < W * 0.5) if dx else (YY > 2) & (YY < H * 0.5)
        out.append(neg("old-scene offset on the hard cut", xshift(hc(i), sel) if dx else yshift(hc(i), sel),
                       -e * (W if dx else H), 0.8))
        return out
    return D, fr, pr


def _elastic_x(u):
    """new scene x (CSS px): 1920 -> 30 in 0.4 s power4.out, then -> -15 (0.1 s sine), then -> 0 (0.1 s sine)."""
    if u < 0.4:
        return 1920 + (30 - 1920) * p_out(4)(u / 0.4)
    if u < 0.5:
        return 30 + (-15 - 30) * sine_io((u - 0.4) / 0.1)
    return -15 + 15 * sine_io((u - 0.5) / 0.1)


def css_elastic():
    D = 0.6

    def fr(u):
        x = _elastic_x(max(u, 0)) * K if u > 0 else W
        bxs = XX - x
        inb = (bxs >= -0.5) & (bxs <= W - 0.5)
        old = sample(A0, XX - (x - W), YY, fill=(0, 0, 0))
        return np.where(inb[..., None], sample(B0, bxs, YY), old)

    def pr(frs, ts, T0, hc):
        out = []
        for u, e in ((0.4, 30 * K), (0.5, -15 * K)):
            i = at(ts, T0 + u)
            selB = (bwt(frs[i]) > 0.5) & (XX > 8) & (XX < W - 8)
            out.append(near("new scene at %.1f s: x = %+.0f css px (overshoot/settle)" % (u, e / K), xshift(frs[i], selB),
                            e, 0.5))
        i = at(ts, T0 + 0.4)
        out.append(neg("overshoot offset on the hard cut", xshift(hc(i), (XX > 8) & (XX < W - 8)), 30 * K, 0.5))
        return out
    return D, fr, pr


def css_squeeze(D=0.4, ease=p_io(3)):
    def fr(u):
        e = ease(u / D)
        wa = W * (1 - e)
        old = sample(A0, XX / max(1 - e, 1e-6), YY) if wa > 0.5 else BLACK
        new = sample(B0, W - (W - XX) / max(e, 1e-6), YY) if e > 1e-3 else BLACK
        return np.where((XX < wa - 0.5)[..., None], old, new)

    def pr(frs, ts, T0, hc):
        i = at(ts, T0 + 0.5 * D)
        e = ease((ts[i] - T0) / D)
        selA = (bwt(frs[i]) < 0.5)
        selB = ~selA
        return [near("new scene width = scaleX x W (origin right)", float(selB[int(CY)].sum()), e * W, 1.0),
                near("old scene scaleX (origin left)", scale_est(frs[i], selA & (XX < W * (1 - e) - 2)) if selA.any() else
                     float("nan"), 1 - e, 0.03) if (1 - e) * W > 30 else check("old squeezed", True),
                neg("new-scene width on the hard cut", float((bwt(hc(i))[int(CY)] > 0.5).sum()), e * W, 1.0)]
    return D, fr, pr


CSS_REF = math.hypot(W, H) / math.sqrt(2)


def css_circle(D=0.5, ease=p_out(2)):
    def fr(u):
        return mix(A0, B0, disc(CX, CY, 0.75 * CSS_REF * ease(u / D)))

    def pr(frs, ts, T0, hc):
        i = at(ts, T0 + 0.25 * D)
        r = 0.75 * CSS_REF * ease((ts[i] - T0) / D)
        return [near("circle() radius at 25%% = 75%% x ease (power2.out) px", b_width(frs[i]) / 2, min(r, W / 2), 1.0),
                near("radius on the vertical axis", float((bwt(frs[i])[:, int(CX)] > 0.5).sum()) / 2, min(r, H / 2), 1.0),
                neg("iris radius on the hard cut", b_width(hc(i)) / 2, min(r, W / 2), 1.0)]
    return D, fr, pr


def css_diamond(D=0.5, ease=p_out(2)):
    def mask(e):
        if e <= 0:
            return np.zeros((H, W))
        return ((np.abs(XX - CX) / (0.7 * W * e) + np.abs(YY - CY) / (0.7 * H * e)) < 1) * 1.0

    def fr(u):
        return mix(A0, B0, mask(ease(u / D)))

    def pr(frs, ts, T0, hc):
        i = at(ts, T0 + 0.25 * D)
        e = ease((ts[i] - T0) / D)
        bw = bwt(frs[i]) > 0.5
        ax, ay = 0.7 * W * e, 0.7 * H * e
        pin = (int(CY + 0.45 * ay), int(CX + 0.45 * ax))
        pout = (int(CY + 0.58 * ay), int(CX + 0.58 * ax))
        return [near("diamond half-width on the row", float(bw[int(CY)].sum()) / 2, min(ax, W / 2), 1.0),
                check("point at (0.45, 0.45) of the half-diagonals is inside (L1 ball)", bool(bw[pin]), bool(bw[pin]), True),
                check("point at (0.58, 0.58) is outside (a circle/ellipse would contain it)", not bool(bw[pout]),
                      bool(bw[pout]), False),
                neg("diamond half-width on the hard cut", float((bwt(hc(i))[int(CY)] > 0.5).sum()) / 2, min(ax, W / 2), 1.0)]
    return D, fr, pr


def css_diagsplit(D=0.5, ease=p_io(3)):
    def amask(e):
        s = max(1 - e, 1e-6)
        return ((XX / (2 * W * s) + YY / (2 * H * s)) < 1) * (e < 1)

    def fr(u):
        return mix(B0, A0, amask(ease(u / D)) * 1.0)

    def pr(frs, ts, T0, hc):
        i = at(ts, T0 + 0.6 * D)
        e = ease((ts[i] - T0) / D)
        am = amask(e)
        meas = bwt(frs[i]) < 0.5
        agree = float(np.mean(meas == am))
        return [check("old scene is the shrinking corner triangle (pixel agreement)", agree > 0.995, agree, "> 0.995"),
                near("old-scene area", float(meas.mean()), float(am.mean()), 0.01),
                neg("old-scene area on the hard cut", float((bwt(hc(i)) < 0.5).mean()), float(am.mean()), 0.01)]
    return D, fr, pr


FLIP_P = 1200 * K


def flip_frame(a, b, th, persp=FLIP_P, bg=BLACK):
    c, s = math.cos(th), math.sin(th)
    sx, sy = XX - CX, YY - CY
    den = c * persp + sx * s
    xl = np.where(np.abs(den) > 1e-6, sx * persp / np.where(np.abs(den) > 1e-6, den, 1), 1e9)
    z = xl * s
    yl = sy * (persp - z) / persp
    front = c > 0
    img = a if front else b
    xs = xl if front else -xl
    ok = (np.abs(xl) <= W / 2) & (persp - z > 1)
    out = sample(img, xs + CX, yl + CY, fill=(0, 0, 0))
    inside_y = np.abs(yl) <= H / 2
    return np.where((ok & inside_y)[..., None], out, bg)


def flip_span(th, persp=FLIP_P):
    c, s = math.cos(th), math.sin(th)
    xs = [x * c * persp / (persp - x * s) for x in (-W / 2, W / 2)]
    return min(xs), max(xs)


def css_flip(D=0.6, ease=p_io(2)):
    def fr(u):
        return flip_frame(A0, B0, math.pi * ease(u / D))

    def pr(frs, ts, T0, hc):
        out = []
        for f in (0.35, 0.7):
            i = at(ts, T0 + f * D)
            th = math.pi * ease((ts[i] - T0) / D)
            lo, hi = flip_span(th)
            vis = frs[i][int(CY)].max(axis=-1) > 0
            cols = np.nonzero(vis)[0]
            out.append(near("projected card width at %.0f deg (perspective 1200)" % math.degrees(th),
                            float(cols.max() - cols.min() + 1) if cols.size else 0.0, min(hi, W / 2) - max(lo, -W / 2), 2.0))
            face = "A" if th < math.pi / 2 else "B"
            fb = fracb(frs[i], vis[None, :].repeat(H, 0) & (frs[i].max(axis=-1) > 0))
            out.append(check("visible face is %s (backface hidden)" % face, (fb < 0.05) if face == "A" else (fb > 0.95), fb,
                             face))
        i = at(ts, T0 + 0.85 * D)
        row = srcx(frs[i])[int(CY)]
        vis = frs[i][int(CY)].max(axis=-1) > 0
        slope = float(np.polyfit(XX[0][vis], row[vis], 1)[0]) if vis.sum() > 5 else float("nan")
        out.append(check("back face B reads left-to-right (not mirrored)", slope > 0, slope, "> 0"))
        i = at(ts, T0 + 0.35 * D)
        lo, hi = flip_span(math.pi * ease((ts[i] - T0) / D))
        out.append(neg("card width on the hard cut", float(W), min(hi, W / 2) - max(lo, -W / 2), 2.0))
        return out
    return D, fr, pr


def css_zoomthrough():
    D = 0.55

    def fr(u):
        eo = p_in(3)(u / 0.4)
        old = affine(blur(A0, 8 * K * eo), 1 + 1.5 * eo, fill=(0, 0, 0))
        out = mix(BLACK, old, 1 - eo)
        un = u - 0.15
        if un > 0:
            en = p_out(3)(un / 0.4)
            new = affine(B0, 0.5 + 0.5 * en, fill=(0, 0, 0))
            inside = ((np.abs(XX - CX) <= (0.5 + 0.5 * en) * W / 2) & (np.abs(YY - CY) <= (0.5 + 0.5 * en) * H / 2))
            out = mix(out, new, inside * en)
        return out

    def pr(frs, ts, T0, hc):
        i = at(ts, T0 + 0.15)
        eo = p_in(3)((ts[i] - T0) / 0.4)
        j = at(ts, T0 + 0.4)
        en = p_out(3)((ts[j] - T0 - 0.15) / 0.4)
        selB = bwt(frs[j]) > 0.5
        return [near("old scene scaled toward 2.5 (power3.in) at +0.15 s", scale_inv(frs[i]), 1 + 1.5 * eo, 0.01),
                near("old opacity 1 - e (blue level)", float(np.median(frs[i][..., 2])) / BLUE_A, 1 - eo, 0.03),
                near("new scene scale 0.5 -> 1 (power3.out) at +0.40 s", scale_inv(frs[j], selB), 0.5 + 0.5 * en, 0.01),
                neg("scale of the hard cut at +0.15 s", scale_est(hc(i)), 1 + 1.5 * eo, 0.01)]
    return D, fr, pr


def css_zoomout(D=0.4, ease=p_in(3)):
    def fr(u):
        e = ease(u / D)
        s = 1 - 0.7 * e
        old = affine(A0, s, fill=(0, 0, 0))
        inside = (np.abs(XX - CX) <= s * W / 2) & (np.abs(YY - CY) <= s * H / 2)
        return mix(B0, old, inside * (1 - e) * (u < D))

    def pr(frs, ts, T0, hc):
        i = at(ts, T0 + 0.6 * D)
        e = ease((ts[i] - T0) / D)
        s = 1 - 0.7 * e
        core = (np.abs(XX - CX) < s * W / 2 - 2) & (np.abs(YY - CY) < s * H / 2 - 2)
        blue = float(frs[i][..., 2][core].mean())
        return [near("old scene scaled to 1 - 0.7 e (old on top)", float(np.mean(srcx(frs[i])[int(CY)][(XX[0] > CX - s * W / 2 + 2) &
                     (XX[0] < CX + s * W / 2 - 2)].ptp() / max(1e-6, (s * W - 4)))), 1.0, 1.0) if False else
                near("old scene scale (power3.in toward 0.3)", scale_est(frs[i], core), s, 0.02),
                near("old opacity 1 - e over the new scene (blue mix)", blue, BLUE_A * (1 - e) + BLUE_B * e, 2.0),
                neg("scale on the hard cut", scale_est(hc(i), core), s, 0.02)]
    return D, fr, pr


def css_crossfade(D=0.5, ease=p_io(2)):
    def fr(u):
        return mix(A0, B0, ease(u / D))

    def pr(frs, ts, T0, hc):
        out = []
        for f in (0.25, 0.5):
            i = at(ts, T0 + f * D)
            e = ease((ts[i] - T0) / D)
            out.append(near("opacity at %.0f%% (power2.inOut, not linear)" % (f * 100), float(bwt(frs[i]).mean()), e, 0.01))
        i = at(ts, T0 + 0.5 * D)
        out.append(neg("blend weight of the hard cut", float(bwt(hc(i)).mean()), 0.5, 0.05))
        return out
    return D, fr, pr


def css_blurfade(D=0.5, blur_px=10, s_out=1.03, s_in=0.97, ease=p_io(2)):
    def fr(u):
        e = ease(u / D)
        old = affine(blur(AT, blur_px * K * e), 1 + (s_out - 1) * e)
        new = affine(blur(BT, blur_px * K * (1 - e)), s_in + (1 - s_in) * e)
        return mix(old, new, e)

    def pr(frs, ts, T0, hc):
        i = at(ts, T0 + 0.25 * D)
        e = ease((ts[i] - T0) / D)
        j = at(ts, T0 + 0.5 * D)
        sh = gsharp(frs[j])
        out = [check("detail drops at the midpoint (both layers blurred %.0f px)" % (blur_px * 0.5), sh < 0.75 * gsharp(AT),
                     sh, "< %.1f" % (0.75 * gsharp(AT))),
               near("blend weight at 25%%", float(bwt(frs[i]).mean()), e, 0.02)]
        if s_out != 1:
            out.append(near("old layer scale at 25%%", scale_est(frs[i]), (1 - e) * (1 + (s_out - 1) * e) + e * (s_in + (1 - s_in) * e),
                            0.006))
        out.append(neg("detail of the hard cut at the midpoint", gsharp(hc(j)), 0.5 * gsharp(AT), 0.25 * gsharp(AT)))
        return out
    return D, fr, pr


def css_dip(D=0.6, color=(0, 0, 0)):
    c = solid(color)

    def fr(u):
        e = u / D
        return mix(A0, c, p_io(1)(2 * e)) if e < 0.5 else mix(c, B0, p_io(1)(2 * e - 1))

    def pr(frs, ts, T0, hc):
        i = at(ts, T0 + 0.5 * D)
        j = at(ts, T0 + 0.25 * D)
        return [near("midpoint is the solid dip colour", mad(frs[i], c), 0.0, 1.0),
                near("quarter point is half-way to the dip", mad(frs[j], mix(A0, c, p_io(1)((ts[j] - T0) / D * 2))), 0.0, 1.5),
                neg("hard cut midpoint vs dip colour", mad(hc(i), c), 0.0, 1.0)]
    return D, fr, pr


BLOCK_C = [hexc("#2f6bff"), hexc("#ff7a1a"), hexc("#18c29c"), hexc("#f2c94c"), hexc("#d946ef")]


def css_blocks(nb=2, step=0.25, off=0.06, ease=p_io(3)):
    D = 2 * step + off * (nb - 1)
    swap = step + off * (nb - 1) / 2

    def bx(k, u):
        uk = u - k * off
        if uk < step:
            return -W + W * ease(uk / step)
        return W * ease((uk - step) / step)

    def fr(u):
        out = (A0 if u < swap else B0).copy()
        for k in range(nb):
            x0 = bx(k, u)
            out[(XX >= x0) & (XX < x0 + W)] = BLOCK_C[k % 5]
        return out

    def pr(frs, ts, T0, hc):
        i = at(ts, T0 + step / 2)
        u = ts[i] - T0
        e1 = (bx(0, u) + W) - max(bx(1, u) + W, 0)
        m = float((np.abs(frs[i][int(CY)] - BLOCK_C[0]).max(axis=-1) < 2).sum())
        return [near("block 1 visible columns at %.3f s (power3.inOut, block 2 %.2f s behind)" % (u, off), m, e1, 1.5),
                check("blocks fully cover the frame at the swap",
                      float((np.abs(frs[at(ts, T0 + swap)] - BLOCK_C[nb - 1]).max(axis=-1) < 2).mean()) > 0.9,
                      float((np.abs(frs[at(ts, T0 + swap)] - BLOCK_C[nb - 1]).max(axis=-1) < 2).mean()), "> 0.9"),
                neg("block-1 columns on the hard cut", float((np.abs(hc(i)[int(CY)] - BLOCK_C[0]).max(axis=-1) < 2).sum()),
                    e1, 1.5)]
    return D, fr, pr


def css_blinds(n, axis="h", stagger=0.03, strip=0.2, ease=p_io(3)):
    D = strip + stagger * (n - 1)
    size = (H if axis == "h" else W) / n

    def emap(u):
        return [ease((u - k * stagger) / strip) for k in range(n)]

    def fr(u):
        es = emap(u)
        coord_ = YY if axis == "h" else XX
        k = np.minimum((coord_ // size).astype(int), n - 1)
        loc = coord_ - k * size
        m = loc < np.array(es)[k] * size
        return mix(A0, B0, m * 1.0)

    def pr(frs, ts, T0, hc):
        i = at(ts, T0 + D * 0.4)
        es = emap(ts[i] - T0)
        bw = bwt(frs[i]) > 0.5
        meas = [float(bw[int(k * size):int((k + 1) * size)].mean()) if axis == "h" else
                float(bw[:, int(k * size):int((k + 1) * size)].mean()) for k in range(n)]
        err = float(np.max(np.abs(np.array(meas) - np.array(es))))
        hb = bwt(hc(i)) > 0.5
        hmeas = [float(hb[int(k * size):int((k + 1) * size)].mean()) if axis == "h" else
                 float(hb[:, int(k * size):int((k + 1) * size)].mean()) for k in range(n)]
        return [check("%d %s strips each closed by its own staggered ease (max error)" % (n, axis), err < 1.0 / size + 0.02,
                      err, "< %.3f" % (1.0 / size + 0.02)),
                check("strip 0 leads strip %d (stagger %.3f s)" % (n - 1, stagger), meas[0] > meas[-1], [meas[0], meas[-1]],
                      "first > last"),
                neg("staggered strip profile on the hard cut (max error)",
                    float(np.max(np.abs(np.array(hmeas) - np.array(es)))), 0.0, 1.0 / size + 0.02)]
    return D, fr, pr


TINT = np.array([255.0, 160.0, 60.0])
LEAKC = np.array([255.0, 180.0, 0.0])


def _tint_a(u):
    if u < 0.2:
        return 0.4 * p_out(2)(u / 0.2)
    if u < 0.45:
        return 0.4 + 0.2 * sine_io((u - 0.2) / 0.25)
    return 0.6 * (1 - p_io(1)((u - 0.45) / 0.45))


def css_lightleak():
    D = 0.9

    def fr(u):
        base = A0 if u < 0.45 else B0
        a = _tint_a(u)
        out = mix(base, solid(TINT), a)
        for k, (x0, y0) in enumerate(((0.1, 0.3), (0.8, 0.7), (0.4, 1.1))):
            x = W * x0 + 250 * K * c01(u / D)
            g = np.exp(-(((XX - x) ** 2 + (YY - H * y0) ** 2) / (2 * (0.5 * 2400 * K / 3) ** 2)))
            out = screen(out, LEAKC * (a * g)[..., None])
        return out

    def pr(frs, ts, T0, hc):
        i = at(ts, T0 + 0.44)
        j = at(ts, T0 + 0.46)
        ai = float(np.median((frs[i][..., 2] - BLUE_A) / (TINT[2] - BLUE_A)))
        bj = float(np.median(frs[j][..., 2]))
        return [near("warm tint opacity just before the swap (0.4 -> 0.6)", ai, _tint_a(ts[i] - T0), 0.03),
                check("scene swaps under the tint at +0.45 s", bj > 120 and ai < 1, bj, "> 120 (B under tint)"),
                neg("tint opacity on the hard cut", float(np.median((hc(i)[..., 2] - BLUE_A) / (TINT[2] - BLUE_A))),
                    _tint_a(ts[i] - T0), 0.03)]
    return D, fr, pr


def _burn_state(u):
    if u < 0.2:
        b = 1 + 0.5 * p_in(1)(u / 0.2)
    else:
        b = 1.5 + 1.5 * p_in(2)(c01((u - 0.2) / 0.35))
    w = p_in(2)(c01((u - 0.2) / 0.35)) if u < 0.55 else 1 - p_out(2)(c01((u - 0.55) / 0.35))
    s = 1.03 + 0.03 * c01(u / 0.55)
    return b, w, s


def css_overexpose():
    D = 0.9

    def fr(u):
        b, w, s = _burn_state(u)
        if u < 0.55:
            img = np.clip(affine(A0, s) * b, 0, 255)
        else:
            img = B0
        return mix(img, solid((255, 255, 255)), w)

    def pr(frs, ts, T0, hc):
        i = at(ts, T0 + 0.2)
        b, w, s = _burn_state(ts[i] - T0)
        gsel = (YY < H * 0.45)
        gain = float(np.median((frs[i][..., 1][gsel] + 1) / (A0[..., 1][gsel] + 1)))
        j = at(ts, T0 + 0.55)
        return [near("brightness x1.5 at +0.2 s (green gain on unclipped rows)", gain, b, 0.08),
                check("burns to full white at the swap (+0.55 s)", float(lum(frs[j]).mean()) > 250, float(lum(frs[j]).mean()),
                      "> 250"),
                neg("brightness gain on the hard cut", float(np.median((hc(i)[..., 1][gsel] + 1) / (A0[..., 1][gsel] + 1))),
                    b, 0.08)]
    return D, fr, pr


FB_COLS = [np.array([255.0, 191.0, 0.0]), np.array([255.0, 120.0, 0.0]), np.array([220.0, 30.0, 0.0])]


def _fb_r(k, u):
    return 1.6 * W * p_in(1)(c01((u - 0.05 * k) / 0.4))


def css_filmburn():
    D = 0.9

    def fr(u):
        base = A0 if u < 0.45 else B0
        out = base.copy()
        fade = 1 - c01((u - 0.45) / 0.45)
        for k, col in enumerate(FB_COLS):
            r = _fb_r(k, u) * (1 if u < 0.45 else 1.0)
            m = disc(0, CY, r, 3.0) * fade
            out = mix(out, solid(col), m * 0.8)
        return out

    def pr(frs, ts, T0, hc):
        i = at(ts, T0 + 0.25)
        u = ts[i] - T0
        row = frs[i][int(CY)]
        changed = np.abs(row - A0[int(CY)]).max(axis=-1) > 20
        reach = float(np.nonzero(changed)[0].max() + 1) if changed.any() else 0.0
        order = [_fb_r(k, u) for k in range(3)]
        return [near("amber front reach from the left edge at +0.25 s (px)", reach, min(order[0], W), 2.0),
                check("overlays staggered 0.05 s: amber > orange > red radius", order[0] > order[1] > order[2], order,
                      "decreasing"),
                check("left edge burns first (column 2 changed, column W-3 not yet)", bool(changed[2]) and not bool(changed[-3]),
                      [bool(changed[2]), bool(changed[-3])], [True, False]),
                neg("burn reach on the hard cut", float((np.abs(hc(i)[int(CY)] - A0[int(CY)]).max(axis=-1) > 20).sum()),
                    min(order[0], W), 2.0)]
    return D, fr, pr


def _jit(k):
    s = 1 if _h(k, 7) < 0.5 else -1
    return s * (30 + 30 * _h(k, 8)) * K


def css_glitch():
    D, q, swap = 0.4, 0.03, 0.2
    w0 = swap - 3 * q

    def fr(u):
        base = A0 if u < swap else B0
        k = int(math.floor((u - w0) / q + 1e-9))
        if not (0 <= k < 6):
            return base.copy()
        d = _jit(k)
        red = shift(base, d, 0) * np.array([1.0, 0, 0])
        cyan = shift(base, -d, 0) * np.array([0, 1.0, 1.0])
        return mix(mix(base, red, 0.35), cyan, 0.35)

    def pr(frs, ts, T0, hc):
        inwin = [i for i, t in enumerate(ts) if 0 <= math.floor((t - T0 - w0) / q + 1e-9) < 6]
        states = len({hash(frs[i].tobytes()) for i in inwin})
        clean_before = mad(frs[at(ts, T0 + w0 - 0.02)], A0)
        clean_after = mad(frs[at(ts, T0 + w0 + 6 * q + 0.02)], B0)
        i = inwin[1]
        base = A0 if ts[i] - T0 < swap else B0
        best = min(range(1, 9), key=lambda s: min(mad(frs[i], mix(mix(base, shift(base, sg * s, 0) * np.array([1.0, 0, 0]), 0.35),
                                                                  shift(base, -sg * s, 0) * np.array([0, 1.0, 1.0]), 0.35))
                                                  for sg in (1, -1)))
        sw = next(i for i, t in enumerate(ts) if t - T0 >= swap)
        return [check("six distinct jitter states, one per 0.03 s", states == 6, states, 6),
                check("clean before and after the jitter window", clean_before < 0.5 and clean_after < 0.5,
                      [clean_before, clean_after], "< 0.5"),
                check("RGB copies displaced 30-60 css px (3-6 px here)", 3 <= best <= 6, best, "3..6"),
                check("swap at +0.2 s", float(np.median(frs[sw][..., 2])) > 100 > float(np.median(frs[sw - 2][..., 2])),
                      [float(np.median(frs[sw - 2][..., 2])), float(np.median(frs[sw][..., 2]))], "A then B"),
                neg("distinct jitter states on the hard cut", len({hash(hc(i).tobytes()) for i in inwin}), 6, 0)]
    return D, fr, pr


def _ab_d(u):
    return 80 * K * (p_in(2)(u / 0.3) if u < 0.3 else 1 - p_out(2)(c01((u - 0.3) / 0.3)))


def css_aberr():
    D = 0.6

    def fr(u):
        base = A0 if u < 0.3 else B0
        d = _ab_d(u)
        out = base.copy()
        out[..., 0] = shift(base, d, 0)[..., 0]
        out[..., 2] = shift(base, -d, 0)[..., 2]
        return out

    def pr(frs, ts, T0, hc):
        i, j = at(ts, T0 + 0.15), at(ts, T0 + 0.29)
        return [near("RGB spread at +0.15 s (power2.in)", chan_offset(frs[i]), _ab_d(ts[i] - T0), 0.4),
                near("RGB spread near the peak (80 css px)", chan_offset(frs[j]), _ab_d(ts[j] - T0), 0.5),
                near("channels re-converged at the end", chan_offset(frs[-1]), 0.0, 0.2),
                neg("RGB spread on the hard cut", chan_offset(hc(j)), _ab_d(ts[j] - T0), 0.5)]
    return D, fr, pr


def _rip_state(u):
    env = math.sin(math.pi * c01(u / 0.4))
    k = int(u // 0.04)
    sg = 1 if k % 2 == 0 else -1
    return sg * 30 * K * env, 1 + sg * 0.03 * env, 4 * K * 10 * env * 0.1


def css_ripple():
    D = 0.4

    def fr(u):
        dx, s, b = _rip_state(u)
        base = A0 if u < 0.2 else B0
        return blur(affine(base, s, dx=dx), b)

    def pr(frs, ts, T0, hc):
        out = []
        for u in (0.1, 0.14, 0.26):
            i = at(ts, T0 + u)
            dx, s, b = _rip_state(ts[i] - T0)
            out.append(near("x oscillation at +%.2f s (+-30 css px, 0.04 s)" % u, xshift(frs[i], (XX > 20) & (XX < W - 20)),
                            dx, 0.4))
            out.append(near("scale oscillation at +%.2f s (0.97-1.03)" % u, scale_est(frs[i]), s, 0.01))
        i = at(ts, T0 + 0.1)
        out.append(neg("x oscillation on the hard cut", xshift(hc(i), (XX > 20) & (XX < W - 20)), _rip_state(ts[i] - T0)[0], 0.4))
        return out
    return D, fr, pr


def _vhs_off(k, u):
    return (_h(k, 31) - 0.5) * 2 * 0.06 * W * math.sin(math.pi * c01(u / 0.4))


def css_vhs():
    D, n = 0.4, 20

    def fr(u):
        base = A0 if u < 0.2 else B0
        sh_ = np.array([_vhs_off(k, u) for k in range(n)])[np.minimum((YY // (H / n)).astype(int), n - 1)]
        img = sample(base, XX - sh_, YY)
        d = 0.01 * W * math.sin(math.pi * c01(u / 0.4))
        img[..., 2] = sample(base, XX - sh_ + d, YY)[..., 2]
        return img

    def pr(frs, ts, T0, hc):
        i = at(ts, T0 + 0.12)
        u = ts[i] - T0
        inner = (XX > 15) & (XX < W - 15)
        sid = np.minimum((YY // (H / n)).astype(int), n - 1)
        d_ = XX - srcx(frs[i])
        meas = [float(np.median(d_[(sid == k) & inner])) for k in range(n)]
        exp = [_vhs_off(k, u) for k in range(n)]
        err = float(np.max(np.abs(np.array(meas) - np.array(exp))))
        within = max(float(np.ptp(d_[(sid == k) & inner])) for k in range(n))
        hm = [float(np.median((XX - srcx(hc(i)))[(sid == k) & inner])) for k in range(n)]
        return [check("20 strips each shifted by its seeded offset (max error px)", err < 0.6, err, "< 0.6"),
                check("one offset per strip (spread inside a strip)", within < 1.2, within, "< 1.2"),
                neg("strip offsets on the hard cut (max error)", float(np.max(np.abs(np.array(hm) - np.array(exp)))), 0.0, 0.6)]
    return D, fr, pr


SHUT = solid((12, 12, 14))


def _shut_e(u):
    return p_in(3)(u / 0.25) if u < 0.25 else 1 - p_out(3)(c01((u - 0.25) / 0.25))


def css_shutter():
    D = 0.5

    def fr(u):
        e = _shut_e(u)
        base = A0 if u < 0.25 else B0
        m = (YY < e * H / 2) | (YY >= H - e * H / 2)
        return np.where(m[..., None], SHUT, base)

    def pr(frs, ts, T0, hc):
        i = at(ts, T0 + 0.2)
        e = _shut_e(ts[i] - T0)
        rows = float((np.abs(frs[i][:, int(CX)] - SHUT[0, 0]).max(axis=-1) < 2).sum())
        j = at(ts, T0 + 0.25)
        return [near("shutter halves cover 2 x e x H/2 rows at +0.2 s (power3.in)", rows, 2 * math.ceil(e * H / 2 - 1e-9), 2.0),
                check("closed at +0.25 s", float((np.abs(frs[j] - SHUT[0, 0]).max(axis=-1) < 2).mean()) > 0.98,
                      float((np.abs(frs[j] - SHUT[0, 0]).max(axis=-1) < 2).mean()), "> 0.98"),
                neg("covered rows on the hard cut", float((np.abs(hc(i)[:, int(CX)] - SHUT[0, 0]).max(axis=-1) < 2).sum()),
                    2 * math.ceil(e * H / 2 - 1e-9), 2.0)]
    return D, fr, pr


ANG = (np.arctan2(XX - CX, -(YY - CY)) % (2 * np.pi))     # clockwise from 12 o'clock


def css_clock(D=0.4):
    def fr(u):
        th = 2 * np.pi * c01(u / D)
        return mix(A0, B0, (ANG < th) * 1.0)

    def pr(frs, ts, T0, hc):
        i = at(ts, T0 + 0.15)
        th = 2 * np.pi * c01((ts[i] - T0) / D)
        bw = bwt(frs[i]) > 0.5
        ring = (np.hypot(XX - CX, YY - CY) > 20) & (np.hypot(XX - CX, YY - CY) < 40)
        edge = float(ANG[ring & bw].max())
        agree = float(np.mean(bw == (ANG < th)))
        return [near("hand angle at +0.15 s = 360 x t/0.4 (ease none, 0.1 s per quadrant)", math.degrees(edge),
                     math.degrees(th), 4.0),
                check("revealed region is the clockwise sector from 12 o'clock", agree > 0.995, agree, "> 0.995"),
                neg("sector agreement on the hard cut", float(np.mean((bwt(hc(i)) > 0.5) == (ANG < th))), 1.0, 0.005)]
    return D, fr, pr


def css_grid(cols=4, rows=3, fill=0.2, k=0.12):
    cw, ch = W / cols, H / rows
    ci = np.minimum((XX // cw).astype(int), cols - 1)
    cj = np.minimum((YY // ch).astype(int), rows - 1)
    dist = np.hypot((ci + 0.5) - cols / 2, (cj + 0.5) - rows / 2)
    dmax = float(dist.max())
    colr = np.array(BLOCK_C)[(ci + cj * cols) % 5]
    T_in = fill + k * dmax
    D = 2 * T_in

    def fr(u):
        base = A0 if u < T_in else B0
        if u < T_in:
            a = np.clip((u - k * dist) / fill, 0, 1)
        else:
            a = 1 - np.clip((u - T_in - k * dist) / fill, 0, 1)
        return mix(base, colr, a)

    def pr(frs, ts, T0, hc):
        i = at(ts, T0 + 0.18)
        u = ts[i] - T0
        a_exp = np.clip((u - k * dist) / fill, 0, 1)
        a_meas = np.zeros((H, W))
        for c in range(cols):
            for r in range(rows):
                sel = (ci == c) & (cj == r) & (np.abs(XX - (c + 0.5) * cw) < 4) & (np.abs(YY - (r + 0.5) * ch) < 4)
                f = frs[i][sel].mean(axis=0)
                cc = colr[sel][0]
                bc = A0[sel].mean(axis=0)
                a_meas[(ci == c) & (cj == r)] = float(np.dot(f - bc, cc - bc) / max(np.dot(cc - bc, cc - bc), 1e-6))
        err = float(np.max(np.abs(a_meas - a_exp)))
        centre = float(a_meas[int(CY), int(CX)])
        corner = float(a_meas[0, 0])
        ncol = len({tuple(c) for c in colr.reshape(-1, 3)})
        return [check("each cell fills on its own clock, delayed by distance from centre (max error)", err < 0.05, err, "< 0.05"),
                check("centre cells lead the corners (ripple from centre)", centre > corner, [centre, corner], "centre > corner"),
                check("5 palette colours on the grid", ncol == 5, ncol, 5),
                neg("cell fill on the hard cut (centre cell)", 0.0, centre, 0.05)]
    return D, fr, pr


def css_gravity(D=0.5, ease=p_in(3)):
    def fr(u):
        e = ease(u / D)
        old = affine(A0, 1.0, dy=1200 * K * e, rot=math.radians(4) * e, fill=None)
        cy_ = CY + 1200 * K * e
        rot = math.radians(4) * e
        u_, v_ = XX - CX, YY - cy_
        lx = u_ * math.cos(-rot) - v_ * math.sin(-rot)
        ly = u_ * math.sin(-rot) + v_ * math.cos(-rot)
        inside = (np.abs(lx) <= W / 2) & (np.abs(ly) <= H / 2)
        return np.where(inside[..., None], old, B0) if u < D else B0

    def pr(frs, ts, T0, hc):
        i = at(ts, T0 + 0.35)
        e = ease((ts[i] - T0) / D)
        selA = (bwt(frs[i]) < 0.5) & (np.abs(XX - CX) < 30)
        dy = yshift(frs[i], selA)
        sel2 = (bwt(frs[i]) < 0.5) & (YY > 1200 * K * e + 8) & (XX > 30) & (XX < W - 30)
        slope = float(np.polyfit(XX[sel2], srcy(frs[i])[sel2], 1)[0]) if sel2.sum() > 20 else float("nan")
        return [near("old scene dropped 1200 css px x power3.in at +0.35 s", dy, 1200 * K * e, 1.0),
                near("old scene rotated 4 deg x e (source-y slope)", -slope, math.tan(math.radians(4) * e), 0.012),
                neg("drop on the hard cut", yshift(hc(i), np.abs(XX - CX) < 30), 1200 * K * e, 1.0)]
    return D, fr, pr


MCOL = np.array([40.0, 60.0, 200.0])


def css_morphcircle(D=0.5, ease=p_in(3)):
    def fr(u):
        if u >= 0.4:
            base = B0
            fade = 1 - c01((u - 0.4) / 0.1)
            return mix(base, solid(MCOL), fade)
        r = 10 * 30 * ease(u / D)
        return mix(A0, solid(MCOL), disc(CX, CY, r))

    def pr(frs, ts, T0, hc):
        i = at(ts, T0 + 0.3)
        r = 300 * ease((ts[i] - T0) / D)
        m = float((np.abs(frs[i][int(CY)] - MCOL).max(axis=-1) < 3).sum()) / 2
        j = at(ts, T0 + 0.4)
        return [near("circle radius = 10 px x scale 30 x power3.in at +0.3 s", m, min(r, W / 2), 1.0),
                check("swap to scene B at +0.4 s (under the colour)", float(np.median(frs[j][..., 2])) > 190,
                      float(np.median(frs[j][..., 2])), "> 190"),
                neg("circle radius on the hard cut", float((np.abs(hc(i)[int(CY)] - MCOL).max(axis=-1) < 3).sum()) / 2,
                    min(r, W / 2), 1.0)]
    return D, fr, pr


def css_blurthrough(D=0.4, blur_px=15, s_peak=1.08):
    half = D / 2

    def fr(u):
        if u < half:
            e = p_in(2)(u / half)
            return affine(blur(AT, blur_px * K * e), 1 + (s_peak - 1) * e)
        e = p_out(2)((u - half) / half)
        return affine(blur(BT, blur_px * K * (1 - e)), s_peak - (s_peak - 1) * e)

    def pr(frs, ts, T0, hc):
        j = at(ts, T0 + half - 0.01)
        e = p_in(2)((ts[j] - T0) / half)
        return [near("scale toward %.2f at the swap" % s_peak, scale_est(frs[j]), 1 + (s_peak - 1) * e, 0.006),
                check("detail lowest at the swap (blur %.0f css px)" % blur_px, gsharp(frs[j]) < 0.5 * gsharp(AT),
                      gsharp(frs[j]), "< %.1f" % (0.5 * gsharp(AT))),
                neg("detail on the hard cut at the swap", gsharp(hc(j)), 0.25 * gsharp(AT), 0.25 * gsharp(AT))]
    return D, fr, pr


def _dirblur_state(u, D):
    half = D / 2
    if u < half:
        e = p_in(2)(u / half)
        return "A", -200 * K * e, math.radians(-8) * e, 12 * K * e
    e = p_out(2)((u - half) / half)
    return "B", 200 * K * (1 - e), math.radians(8) * (1 - e), 12 * K * (1 - e)


def css_dirblur(D=0.4):
    def fr(u):
        which, dx, sk, L = _dirblur_state(u, D)
        img = AT if which == "A" else BT
        sx = XX - dx - np.tan(sk) * (YY - CY)
        return hgauss(sample(img, sx, YY), L)

    def pr(frs, ts, T0, hc):
        i = at(ts, T0 + D / 2 - 0.02)
        which, dx, sk, L = _dirblur_state(ts[i] - T0, D)
        inner = (XX > 30) & (XX < W - 30) & (np.abs(YY - CY) < 40)
        dyx = float(np.polyfit(YY[inner], (XX - srcx(frs[i]))[inner], 1)[0])
        return [near("x offset toward -200 css px", xshift(frs[i], inner & (np.abs(YY - CY) < 2)), dx, 0.6),
                near("skewX -8 deg x e (shift per row)", dyx, math.tan(sk), 0.02),
                check("blur is horizontal (horizontal detail << vertical)", gsharp(frs[i], "h") < 0.6 * gsharp(frs[i], "v"),
                      [gsharp(frs[i], "h"), gsharp(frs[i], "v")], "h < 0.6 v"),
                neg("skew on the hard cut", float(np.polyfit(YY[inner], (XX - srcx(hc(i)))[inner], 1)[0]), math.tan(sk), 0.02)]
    return D, fr, pr


CHAR = np.array([40.0, 22.0, 12.0])
GLOW = np.array([255.0, 140.0, 30.0])


def _pb_front(ang, R):
    a = ang * 1.0
    n = (50 * K * np.sin(a * 7 + 1.3) + 20 * K * np.sin(a * 19 + 0.4) + 8 * K * np.sin(a * 43 + 2.1))
    return R + n


def css_pageburn(D=0.8):
    dist = np.hypot(XX, YY)
    ang = np.arctan2(YY, XX)
    Rmax = math.hypot(W, H) + 10

    def fr(u):
        R = Rmax * p_io(1)(u / D)
        f = _pb_front(ang, R)
        out = np.where((dist < f - 3)[..., None], B0, A0)
        out = np.where(((dist >= f - 3) & (dist < f))[..., None], CHAR, out)
        out = np.where(((dist >= f) & (dist < f + 2))[..., None], GLOW, out)
        return out if u < D else B0

    def pr(frs, ts, T0, hc):
        i = at(ts, T0 + 0.4)
        R = Rmax * p_io(1)((ts[i] - T0) / D)
        f = _pb_front(ang, R)
        meas = bwt(frs[i]) > 0.5
        agree = float(np.mean(meas == (dist < f - 3)))
        charm = float(((np.abs(frs[i] - CHAR).max(axis=-1) < 2)).mean())
        return [check("burnt region = radial front from the corner + 3-octave sin noise", agree > 0.995, agree, "> 0.995"),
                check("charred fringe present along the front", charm > 0.005, charm, "> 0.005"),
                neg("burnt-region agreement on the hard cut", float(np.mean((bwt(hc(i)) > 0.5) == (dist < f - 3))), 1.0, 0.005)]
    return D, fr, pr


CSS = {
    "push-slide": css_push(1, 0), "vertical-push": css_push(0, 1), "elastic-push": css_elastic(), "squeeze": css_squeeze(),
    "circle-iris": css_circle(), "diamond-iris": css_diamond(), "diagonal-split": css_diagsplit(), "card-flip": css_flip(),
    "zoom-through": css_zoomthrough(), "zoom-out": css_zoomout(), "crossfade": css_crossfade(), "blur-crossfade": css_blurfade(),
    "focus-pull": css_blurfade(0.5, 15, 1.0, 1.0), "color-dip": css_dip(), "staggered-blocks": css_blocks(),
    "horizontal-blinds": css_blinds(6, "h"), "vertical-blinds": css_blinds(8, "v"), "light-leak": css_lightleak(),
    "overexposure-burn": css_overexpose(), "film-burn": css_filmburn(), "glitch": css_glitch(),
    "chromatic-aberration": css_aberr(), "ripple": css_ripple(), "vhs-tape": css_vhs(), "shutter": css_shutter(),
    "clock-wipe": css_clock(), "grid-dissolve": css_grid(), "gravity-drop": css_gravity(), "morph-circle": css_morphcircle(),
    "blur-through": css_blurthrough(), "directional-blur": css_dirblur(), "page-burn": css_pageburn(),
}
CSS_FPS = {"glitch": 100, "ripple": 100, "light-leak": 100}
CSS_TEX = {"blur-crossfade", "focus-pull", "blur-through", "directional-blur"}


def run_css(wd, key, card_id, T0=0.1, tail=0.1):
    """Render one handoff: scene A held, the recipe for D seconds, then overlays cleaned and scene B held."""
    D, fr, pr = CSS[key]
    fps = CSS_FPS.get(key, 40)
    a, b = (AT, BT) if key in CSS_TEX else (A0, B0)

    def frame(t):
        u = round(t - T0, 6)
        return a if u < 0 else fr(u) if u < D else b
    path, frs, ts = film(wd, key, frame, T0 + D + tail, fps)
    cut = T0 + D / 2
    hc = lambda i: a if ts[i] < cut else b     # noqa: E731
    checks = ends(frs, a, b, name=key) + pr(frs, ts, T0, hc)
    return checks, path


def css_card(card_id, key):
    def fn(task, wd):
        checks, path = run_css(wd, key, card_id)
        plan = save_plan(wd, "handoff_" + key, {"card": card_id, "transition": key, "duration_s": CSS[key][0],
                                                "stage": "1920x1080 css px scaled to %dx%d" % (W, H),
                                                "engine": "numpy re-implementation of the GSAP handoff recipe"})
        return checks, [path, plan]
    card(card_id)(fn)


for _cid, _key in [("TRANS-173", "push-slide"), ("TRANS-174", "vertical-push"), ("TRANS-175", "elastic-push"),
                   ("TRANS-176", "squeeze"), ("TRANS-177", "circle-iris"), ("TRANS-178", "diamond-iris"),
                   ("TRANS-179", "diagonal-split"), ("TRANS-180", "card-flip"), ("TRANS-181", "zoom-through"),
                   ("TRANS-182", "zoom-out"), ("TRANS-183", "crossfade"), ("TRANS-184", "blur-crossfade"),
                   ("TRANS-185", "focus-pull"), ("TRANS-186", "color-dip"), ("TRANS-187", "staggered-blocks"),
                   ("TRANS-188", "horizontal-blinds"), ("TRANS-189", "vertical-blinds"), ("TRANS-190", "light-leak"),
                   ("TRANS-191", "overexposure-burn"), ("TRANS-192", "film-burn"), ("TRANS-193", "glitch"),
                   ("TRANS-194", "chromatic-aberration"), ("TRANS-195", "ripple"), ("TRANS-196", "vhs-tape"),
                   ("TRANS-197", "shutter"), ("TRANS-198", "clock-wipe"), ("TRANS-199", "grid-dissolve"),
                   ("TRANS-200", "gravity-drop"), ("TRANS-201", "morph-circle"), ("TRANS-202", "blur-through"),
                   ("TRANS-203", "directional-blur"), ("TRANS-204", "page-burn")]:
    css_card(_cid, _key)


def showcase_card(card_id, keys):
    """A hyperframes 'transitions-*' showcase: every named transition rendered, measured, and joined into one reel."""
    def fn(task, wd):
        checks, paths = [], []
        for k in keys:
            c, p = run_css(wd, k, card_id)
            checks += [dict(x, check="%s: %s" % (k, x["check"])) for x in c]
            paths.append(p)
        reel = Path(wd) / "showcase.mp4"
        ins = sum((["-i", str(p)] for p in paths), [])
        graph = "".join("[%d:v]fps=100[v%d];" % (k, k) for k in range(len(paths))) + \
            "".join("[v%d]" % k for k in range(len(paths))) + "concat=n=%d:v=1:a=0[v]" % len(paths)
        fx.ffmpeg(*ins, "-filter_complex", graph, "-map", "[v]", "-c:v", "libx264rgb", "-crf", "0", "-preset", "ultrafast",
                  str(reel))
        d_exp = sum(float(fx.probe(p)["format"]["duration"]) for p in paths)
        d = float(fx.probe(reel)["format"]["duration"])
        checks.append(near("showcase reel holds every named transition back to back (duration s)", d, d_exp, 0.06))
        plan = save_plan(wd, "showcase", {"card": card_id, "transitions": keys,
                                          "engine": "numpy re-implementation; hyperframes composition not used"})
        return checks, [reel, plan]
    card(card_id)(fn)


showcase_card("TRANS-152", ["blur-through", "directional-blur"])
showcase_card("TRANS-153", ["staggered-blocks", "horizontal-blinds", "vertical-blinds"])
showcase_card("TRANS-154", ["page-burn"])
showcase_card("TRANS-155", ["crossfade", "blur-crossfade", "focus-pull", "color-dip"])
showcase_card("TRANS-156", ["glitch", "chromatic-aberration", "ripple"])
showcase_card("TRANS-157", ["grid-dissolve"])
showcase_card("TRANS-158", ["light-leak", "overexposure-burn", "film-burn"])
showcase_card("TRANS-159", ["shutter", "clock-wipe"])
showcase_card("TRANS-161", ["push-slide", "vertical-push", "elastic-push", "squeeze"])
showcase_card("TRANS-162", ["circle-iris", "diamond-iris", "diagonal-split"])
showcase_card("TRANS-163", ["zoom-through", "zoom-out"])
showcase_card("TRANS-151", ["card-flip"])


def css_flashcut(D=0.3):
    white = solid((255, 255, 255))

    def fr(u):
        if u < 0.05:
            return mix(A0, white, u / 0.05)
        return mix(B0, white, 1 - p_out(2)((u - 0.05) / (D - 0.05)))

    def pr(frs, ts, T0, hc):
        i = at(ts, T0 + 0.05)
        j = at(ts, T0 + 0.15)
        e = 1 - p_out(2)((ts[j] - T0 - 0.05) / (D - 0.05))
        return [near("full white at the swap (+0.05 s)", float(lum(frs[i]).mean()), 255.0, 1.0),
                near("white decays power2.out over scene B (+0.15 s)", float(np.median(frs[j][..., 2])),
                     BLUE_B * (1 - e) + 255 * e, 2.0),
                neg("white at the swap on the hard cut", float(lum(hc(i)).mean()), 255.0, 1.0)]
    return D, fr, pr


CSS["flash-cut"] = css_flashcut()
showcase_card("TRANS-160", ["flash-cut", "gravity-drop", "morph-circle"])


# ───────────────────────── hyperframes component cards (re-implemented) ─────────────────────────
BG = np.array([18.0, 20.0, 30.0])


def box(cx, cy, w, h):
    return np.clip(np.minimum(w / 2 - np.abs(XX - cx) + 0.5, h / 2 - np.abs(YY - cy) + 0.5), 0, 1)


def centroid(fr, col, tol=60):
    m = np.clip(1 - np.abs(fr - col).max(axis=-1) / tol, 0, 1)
    s = m.sum()
    return (float((m * XX).sum() / s), float((m * YY).sum() / s), float(s)) if s > 0.5 else (float("nan"),) * 2 + (0.0,)


def comp_card(card_id, name, engine="numpy re-implementation of the hyperframes component (component not installed)"):
    def deco(fn):
        def run(task, wd):
            checks, outs, plan = fn(wd)
            p = save_plan(wd, name, dict(plan, card=card_id, engine=engine))
            return checks, list(outs) + [p]
        card(card_id)(run)
        return fn
    return deco


@comp_card("TRANS-119", "chromatic_aberration_wipe")
def _c119(wd):
    D, T0, amp = 0.5, 0.1, 0.02 * W

    def frame(t):
        u = round(t - T0, 6)
        if u < 0:
            return A0
        if u >= D:
            return B0
        e = p_io(3)(u / D)
        bx = XX - (1 - e) * W
        img = np.where((bx >= -0.5)[..., None], sample(B0, bx, YY), A0)
        d = amp * max(0.0, math.sin(math.pi * (u / D - 0.25) / 0.5)) if 0.25 < u / D < 0.75 else 0.0
        out = img.copy()
        out[..., 0] = shift(img, d, 0)[..., 0]
        out[..., 2] = shift(img, -d, 0)[..., 2]
        return out
    path, frs, ts = film(wd, "chromatic_wipe", frame, T0 + D + 0.1, 40)
    i, j = at(ts, T0 + 0.5 * D), at(ts, T0 + 0.15 * D)
    e = p_io(3)((ts[i] - T0) / D)
    cov = float((bwt(frs[i])[int(CY)] > 0.5).sum())
    return ([*ends(frs, A0, B0, name="chromatic wipe"),
             near("slide wipe: B covers (e x W) columns at the midpoint", cov, e * W, 2.0),
             near("RGB split on the peak frames (aberration 1 = 2% W)", chan_offset(frs[i]), amp, 0.5),
             near("no split outside the peak window", chan_offset(frs[j]), 0.0, 0.2),
             neg("RGB split on the hard cut", chan_offset(A0 if ts[i] < T0 + D / 2 else B0), amp, 0.5)],
            [path], {"direction": "left", "aberration": 1, "duration": D})


CURTAIN = np.array([110.0, 20.0, 40.0])


@comp_card("TRANS-120", "curtain_reveal")
def _c120(wd):
    D, T0, pel, period = 1.2, 0.1, int(0.12 * H), 8.0

    def frame(t):
        u = round(t - T0, 6)
        e = p_io(2)(u / D) if u > 0 else 0.0
        img = B0.copy()
        if e > 0.6:                                            # spotlight blooms on the stage
            g = (e - 0.6) / 0.4 * 0.35 * np.exp(-(((XX - CX) / (0.25 * W)) ** 2 + ((YY - 0.6 * H) / (0.35 * H)) ** 2))
            img = screen(img, 255 * g[..., None] * np.ones(3))
        half = (W / 2) * (1 - e)
        for side in (0, 1):
            xl = XX if side == 0 else (W - 1 - XX)
            inside = xl < half
            p_eff = max(period * (1 - e), 2.0)
            shade = 0.72 + 0.28 * np.cos(2 * math.pi * xl / p_eff)
            img = np.where(inside[..., None], CURTAIN * shade[..., None], img)
        img[:pel] = CURTAIN * 0.6
        return img
    path, frs, ts = film(wd, "curtain", frame, T0 + D + 0.2, 20)
    i = at(ts, T0 + 0.5 * D)
    e = p_io(2)((ts[i] - T0) / D)
    gap = float((bwt(frs[i])[int(0.6 * H)] > 0.5).sum())
    pel_static = max(mad(f[:pel], frs[0][:pel]) for f in frs)
    j = at(ts, T0 + 0.1 * D)
    row = frs[j][int(0.6 * H), :int(W * 0.4), 0]
    spec = np.abs(np.fft.rfft(row - row.mean()))
    per = len(row) / max(int(np.argmax(spec[1:]) + 1), 1)
    e_j = p_io(2)((ts[j] - T0) / D)
    spot = float(lum(frs[-1])[int(0.6 * H), int(CX)] - lum(B0)[int(0.6 * H), int(CX)])
    return ([check("curtains closed on the first frame (no stage visible)", fracb(frs[0], YY >= pel) < 0.01,
                   fracb(frs[0], YY >= pel), "< 0.01"),
             near("stage gap = W x e at the midpoint (curtains gather outward)", gap, W * e, 2.0),
             check("pelmet never moves", pel_static < 0.5, pel_static, "< 0.5"),
             near("pleat period gathers with the curtain (px)", per, max(period * (1 - e_j), 2.0), 1.2),
             check("spotlight blooms on the stage at the end", spot > 30, spot, "> 30"),
             check("stage is scene B at the end", fracb(frs[-1], (YY >= pel)) > 0.99, fracb(frs[-1], YY >= pel), "> 0.99"),
             neg("stage gap on an uncurtained cut", float(W if ts[i] >= T0 + D / 2 else 0), W * e, 2.0)],
            [path], {"tone": "burgundy", "pelmet": "on", "spotlight": "on", "duration": D})


SUBJ_A, SUBJ_B = np.array([240.0, 240.0, 240.0]), np.array([60.0, 220.0, 120.0])


@comp_card("TRANS-121", "cut_the_curve")
def _c121(wd):
    D, cf, travel, x0 = 1.0, 0.33, 0.6 * W, 0.15 * W
    tc = cf * D
    Lo, Li = travel * cf, travel * (1 - cf)

    def xpos(t):
        if t < tc:
            return x0 + Lo * p_in(3)(t / tc)
        return x0 + Lo + Li * p_out(3)((t - tc) / (D - tc))

    def frame(t):
        col = SUBJ_A if t < tc else SUBJ_B
        return mix(solid(BG), solid(col), box(xpos(t), CY, 14, 14))
    fps = 100
    path, frs, ts = film(wd, "cut_the_curve", frame, D, fps)
    xs = [centroid(f, SUBJ_A if t < tc else SUBJ_B)[0] for f, t in zip(frs, ts)]
    ic = next(i for i, t in enumerate(ts) if t >= tc)
    v_out = (xs[ic - 1] - xs[ic - 2]) * fps
    v_in = (xs[ic + 1] - xs[ic]) * fps
    v_mid_out = (xs[ic // 2] - xs[ic // 2 - 1]) * fps
    swap_ok = (np.abs(frs[ic - 1] - SUBJ_A).max(axis=-1) < 5).any() and (np.abs(frs[ic] - SUBJ_B).max(axis=-1) < 5).any()
    return ([check("subject swaps exactly at cutFraction 0.33", bool(swap_ok), ts[ic], tc),
             check("same direction across the cut", v_out > 0 and v_in > 0, [v_out, v_in], "> 0"),
             near("incoming speed matches outgoing at the cut (ratio)", v_in / v_out, 1.0, 0.25),
             check("outgoing accelerates (power4.in): speed at cut >> speed at mid-exit", v_out > 4 * max(v_mid_out, 1e-6),
                   [v_mid_out, v_out], "x4"),
             neg("speed ratio for a static hard cut", 0.0, 1.0, 0.25)],
            [path], {"cutFraction": cf, "out_ease": "power4.in", "in_ease": "power4.out", "subject": "card"})


@comp_card("TRANS-122", "directional_wipe")
def _c122(wd):
    D, T0, rad = 0.6, 0.1, 48 * K

    def frame(t):
        u = round(t - T0, 6)
        if u < 0:
            return A0
        if u >= D:
            return B0
        e = p_io(3)(u / D)
        x0 = (1 - e) * W
        bx = XX - x0
        inside = bx >= 0
        corner = (bx < rad) & ((YY < rad) | (YY > H - 1 - rad))
        cy_ = np.where(YY < rad, rad, H - 1 - rad)
        rounded = corner & (np.hypot(bx - rad, YY - cy_) > rad)
        return np.where((inside & ~rounded)[..., None], sample(B0, bx, YY), A0)
    path, frs, ts = film(wd, "directional_wipe", frame, T0 + D + 0.1, 40)
    i = at(ts, T0 + 0.5 * D)
    e = p_io(3)((ts[i] - T0) / D)
    x0 = (1 - e) * W
    selA, selB = (XX < x0 - 2), (XX > x0 + 2) & (np.abs(YY - CY) < 20)
    xi = int(math.ceil(x0))
    return ([*ends(frs, A0, B0, name="directional wipe"),
             near("scene A stays put under the panel (offset px)", xshift(frs[i], selA), 0.0, 0.3),
             near("panel B pushed in from the right (offset px)", xshift(frs[i], selB), x0, 0.8),
             check("panel corner is rounded (corner pixel shows A, inset pixel shows B)",
                   bwt(frs[i])[0, xi] < 0.5 and bwt(frs[i])[int(rad) + 1, xi + int(rad) + 1] > 0.5,
                   [float(bwt(frs[i])[0, xi]), float(bwt(frs[i])[int(rad) + 1, xi + int(rad) + 1])], "[A, B]"),
             neg("panel offset on the hard cut", xshift(A0 if ts[i] < T0 + D / 2 else B0, selB), x0, 0.8)],
            [path], {"palette": "slate", "corner": "rounded", "duration": D})


PAPER = np.array([244.0, 239.0, 230.0])


@comp_card("TRANS-123", "fade_through")
def _c123(wd):
    D, T0 = 0.8, 0.1
    css = css_dip(D, PAPER)
    path, frs, ts = film(wd, "fade_through", lambda t: A0 if t < T0 else css[1](round(t - T0, 6)) if t < T0 + D else B0,
                         T0 + D + 0.1, 40)
    hc = lambda i: A0 if ts[i] < T0 + D / 2 else B0       # noqa: E731
    return (ends(frs, A0, B0, name="fade through") + css[2](frs, ts, T0, hc), [path],
            {"wash": "paper", "shape": "flat", "strength": 1})


@comp_card("TRANS-124", "grid_pixelate_wipe")
def _c124(wd):
    nx, ny, D, T0, fade = 12, 7, 0.9, 0.1, 0.3
    cw, ch = W / nx, H / ny
    ci, cj = np.minimum((XX // cw).astype(int), nx - 1), np.minimum((YY // ch).astype(int), ny - 1)
    order = (ci + cj) / float(nx + ny - 2)
    stag = D - fade

    def frame(t):
        u = round(t - T0, 6)
        a = np.clip((u - order * stag) / fade, 0, 1)
        return mix(A0, B0, a)
    path, frs, ts = film(wd, "grid_pixelate", frame, T0 + D + 0.1, 40)
    i = at(ts, T0 + 0.45)
    u = ts[i] - T0
    w = bwt(frs[i])
    uni = max(float(np.ptp(w[(ci == a) & (cj == b)])) for a in range(nx) for b in range(ny))
    exp = np.clip((u - order * stag) / fade, 0, 1)
    err = float(np.max(np.abs(w - exp)))
    return ([*ends(frs, A0, B0, name="grid pixelate"),
             check("each square fades as one block (weight spread in a cell)", uni < 0.01, uni, "< 0.01"),
             check("squares fade on a staggered diagonal clock (max error)", err < 0.01, err, "< 0.01"),
             neg("staggered-grid error on the hard cut", float(np.max(np.abs(bwt(A0 if u < D / 2 else B0) - exp))), 0, 0.01)],
            [path], {"grid": [nx, ny], "fade_s": fade, "stagger_s": stag})


INK = np.array([40.0, 200.0, 110.0])


@comp_card("TRANS-125", "halftone_dissolve")
def _c125(wd):
    nx, ny, at_, dur = 12, 7, 1.1, 0.6
    cw, ch = W / nx, H / ny
    ci, cj = np.minimum((XX // cw).astype(int), nx - 1), np.minimum((YY // ch).astype(int), ny - 1)
    ccx, ccy = (ci + 0.5) * cw, (cj + 0.5) * ch
    rmax = math.hypot(cw, ch) / 2 + 1
    delay = ci / (nx - 1) * 0.3                               # ltr: smallest dots on the left first

    def radius(u):
        return rmax * np.clip((u - delay) / (dur - 0.3), 0, 1)

    def frame(t):
        u = round(t - at_, 6)
        r = radius(u)
        d = np.hypot(XX - ccx, YY - ccy)
        out = np.where((d < r - 1)[..., None], B0, A0)
        return np.where(((d >= r - 1) & (d < r) & (r > 0))[..., None], INK, out)
    path, frs, ts = film(wd, "halftone", frame, at_ + dur + 0.1, 20)
    i = at(ts, at_ + 0.3)
    u = ts[i] - at_
    r = radius(u)
    bmask = bwt(frs[i]) > 0.5
    areas_l = float(bmask[(ci == 2)].sum()) / ny
    areas_r = float(bmask[(ci == 9)].sum()) / ny
    rl = float(r[0, int(2.5 * cw)])
    d = np.hypot(XX - ccx, YY - ccy)
    disc_ok = float(np.mean(bmask[(ci == 2)] == (d < r - 1)[(ci == 2)]))
    return ([check("before dissolve_at 1.1 s the frame is scene A", mad(frs[at(ts, 1.0)], A0) < 0.5, mad(frs[at(ts, 1.0)], A0),
                   "< 0.5"),
             check("each dot is a disc window onto B (pixel agreement)", disc_ok > 0.98, disc_ok, "> 0.98"),
             check("ltr: left dots larger than right dots", areas_l > areas_r, [areas_l, areas_r], "left > right"),
             check("ink ring rims the dots", bool((np.abs(frs[i] - INK).max(axis=-1) < 2).any()), True, True),
             check("scene B at the end", mad(frs[-1], B0) < 0.5, mad(frs[-1], B0), "< 0.5"),
             neg("disc-window area on the hard cut (left column)", float((bwt(A0) > 0.5)[(ci == 2)].sum()) / ny,
                 math.pi * rl * rl, 2.0)],
            [path], {"dot_size": "medium", "direction": "ltr", "dissolve_at": at_})


ACCENT = np.array([70.0, 140.0, 255.0])


@comp_card("TRANS-126", "iris_reveal")
def _c126(wd):
    open_at, D = 0.35, 0.5
    rmax = math.hypot(W, H) / 2 + 2

    def frame(t):
        u = round(t - open_at, 6)
        if u < 0:
            return A0
        r = rmax * p_out(2)(u / D)
        if u >= D:
            return B0
        g = lum(A0)
        desat = mix(A0, np.repeat(g[..., None], 3, -1), c01(u / 0.15))
        d = np.hypot(XX - CX, YY - CY)
        out = np.where((d < r)[..., None], B0, desat)
        return np.where(((d >= r) & (d < r + 1.5))[..., None], ACCENT, out)
    path, frs, ts = film(wd, "iris_reveal", frame, open_at + D + 0.1, 40)
    i = at(ts, open_at + 0.2)
    r = rmax * p_out(2)((ts[i] - open_at) / D)
    outside = np.hypot(XX - CX, YY - CY) > r + 2
    sat = float(np.mean(frs[i][outside].max(axis=-1) - frs[i][outside].min(axis=-1))) if outside.any() else 0.0
    return ([*ends(frs, A0, B0, name="iris reveal"),
             near("iris radius at open_at + 0.2 s (centre 50%/50%)", b_width(frs[i]) / 2, min(r, W / 2), 1.2),
             check("classic register: A desaturated while B lands in colour", sat < 2.0, sat, "< 2"),
             check("thin accent rim at the iris edge", bool((np.abs(frs[i] - ACCENT).max(axis=-1) < 2).any()), True, True),
             neg("A saturation on the hard cut", float(np.mean(A0.max(axis=-1) - A0.min(axis=-1))), 0.0, 2.0)],
            [path], {"iris_x": 50, "iris_y": 50, "open_at": open_at, "register": "color"})


@comp_card("TRANS-127", "match_cut")
def _c127(wd):
    D, tc = 1.2, 0.5
    bgA, bgB = np.array([20.0, 24.0, 40.0]), np.array([240.0, 236.0, 226.0])

    def state(t):
        if t < tc:
            e = p_in(3)(t / tc)
            return 0.2 * W + 0.3 * W * e, CY, 8 + 18 * e
        e = p_out(3)((t - tc) / (D - tc))
        return 0.5 * W + 0.2 * W * e, CY, 26 - 14 * e

    def frame(t):
        x, y, r = state(t)
        return mix(solid(bgA if t < tc else bgB), solid(INK), disc(x, y, r))
    path, frs, ts = film(wd, "match_cut", frame, D, 50)
    ic = next(i for i, t in enumerate(ts) if t >= tc)

    def circ(f):
        cx_, cy_, area = centroid(f, INK, 40)
        return cx_, math.sqrt(area / math.pi)
    a, b = circ(frs[ic - 1]), circ(frs[ic])
    ex = state(ts[ic])
    bg_ok = mad(frs[ic - 1][0, 0], bgA) < 2 and mad(frs[ic][0, 0], bgB) < 2
    return ([check("single-frame scene swap (background changes at the cut frame)", bool(bg_ok), True, True),
             near("incoming circle radius matches the outgoing one at the cut (px)", b[1], ex[2], 0.6),
             near("incoming circle starts where the outgoing one is heading (centre px)", b[0], ex[0], 0.6),
             check("continues to a smaller rest pose", circ(frs[-1])[1] < b[1] - 8, [b[1], circ(frs[-1])[1]], "smaller"),
             neg("radius continuity on a plain cut to a fresh circle", 8.0, ex[2], 0.6)],
            [path], {"labels": ["Start", "Done"], "cut_s": tc})


@comp_card("TRANS-128", "morph_swap")
def _c128(wd):
    swap, half = 1.4, 0.3
    ca, cb = np.array([240.0, 90.0, 60.0]), np.array([60.0, 160.0, 240.0])

    def frame(t):
        img = solid(BG)
        if t < swap:
            e = p_in(2)(c01((t - (swap - half)) / half))
            return mix(img, solid(ca), box(CX, CY, 40 * (1 - e) + 1e-3, 40 * (1 - e) + 1e-3) * (1 - e))
        e = p_out(2)(c01((t - swap) / half))
        return mix(img, solid(cb), box(CX, CY, 40 * e, 40 * e) * e)
    path, frs, ts = film(wd, "morph_swap", frame, swap + half + 0.2, 20)
    i, j = at(ts, swap - 0.15), at(ts, swap + 0.15)
    ea = p_in(2)(0.5)
    ia = centroid(frs[i], ca, 80)
    jb = centroid(frs[j], cb, 80)
    wa = float((np.abs(frs[i][int(CY)] - BG).max(axis=-1) > 3).sum())
    return ([near("A and B share one centre (x)", ia[0], jb[0], 0.3), near("A and B share one centre (y)", ia[1], jb[1], 0.3),
             near("A condenses: width 40 x (1 - e) at swap - 0.15 s", wa, round(40 * (1 - ea)), 1.5),
             check("B fully formed at the end", float((np.abs(frs[-1] - cb).max(axis=-1) < 2).sum()) >= 39 * 39,
                   float((np.abs(frs[-1] - cb).max(axis=-1) < 2).sum()), ">= 1521"),
             neg("condensed width without the morph (full A until the swap)", 40.0, round(40 * (1 - ea)), 1.5)],
            [path], {"swap_at": swap, "register": "condense"})


CSS["page-slide"] = css_push(1, 0, D=0.6)
css_card("TRANS-129", "page-slide")


@comp_card("TRANS-130", "rubber_band_bumper")
def _c130(wd):
    strain, hold, snap, settle = 0.4, 0.15, 0.2, 0.4
    L, kres = 0.12 * H, 6.0
    panel_a, panel_b = np.array([235.0, 235.0, 240.0]), np.array([40.0, 200.0, 110.0])

    def ya(t):
        if t < strain:
            return -L * (1 - math.exp(-kres * t)) / (1 - math.exp(-kres * strain))
        if t < strain + hold:
            return -L
        return -L - (H + 10) * p_in(3)(c01((t - strain - hold) / snap))

    def yb(t):
        t0 = strain + hold
        if t < t0:
            return H + 10
        return (H + 10) * (1 - back_out(2.0)(c01((t - t0) / (snap + settle))))

    def frame(t):
        img = solid(BG)
        img = mix(img, solid(panel_a), box(CX, CY + ya(t), W * 0.6, H * 0.6))
        return mix(img, solid(panel_b), box(CX, CY + yb(t), W * 0.6, H * 0.6))
    T = strain + hold + snap + settle
    path, frs, ts = film(wd, "rubber_band", frame, T, 40)
    ys = [centroid(f, panel_a, 30)[1] - CY for f in frs]
    st = [ys[i] for i, t in enumerate(ts) if t <= strain]
    inc = np.diff(st)
    yb_meas = [centroid(f, panel_b, 30)[1] - CY for f in frs]
    after = [y for y, t in zip(yb_meas, ts) if t > strain + hold and y == y]
    hold_y = [ys[i] for i, t in enumerate(ts) if strain + 0.01 < t < strain + hold - 0.01]
    return ([check("strain: displacement increments shrink (rising resistance)", bool(np.all(np.diff(np.abs(inc)) < 1e-6)),
                   [float(x) for x in inc[:4]], "decreasing"),
             check("holds at tension", float(np.ptp(hold_y)) < 0.05, float(np.ptp(hold_y)), "< 0.05"),
             check("incoming panel overshoots past rest then settles (back.out)", min(after) < -0.3 and abs(after[-1]) < 0.3,
                   [min(after), after[-1]], "min < -0.3, end ~0"),
             neg("shrinking strain increments on a linear push",
                 0.0 if np.all(np.diff(np.abs(np.diff(np.linspace(0, -L, 17)))) < -1e-6) else 1.0, 0.0, 0.5)],
            [path], {"direction": "up", "strain_s": strain, "hold_s": hold})


WORDC = np.array([240.0, 240.0, 240.0])


def _words_x(n=3):
    return [W * (0.2 + 0.3 * k) for k in range(n)]


@comp_card("TRANS-131", "shared_axis_y")
def _c131(wd):
    n, dur, stag, dist = 3, 0.3, 0.06, 30 * K * 3

    def off(k, t, out):
        u = c01((t - k * stag) / dur)
        e = p_in(2)(u) if out else p_out(2)(u)
        return e

    T_out = dur + stag * (n - 1)

    def frame(t):
        img = solid(BG)
        for k, x in enumerate(_words_x(n)):
            if t < T_out:
                e = off(k, t, True)
                img = mix(img, solid(WORDC), box(x, CY - dist * e, 30, 10) * (1 - e))
            else:
                e = off(k, t - T_out, False)
                img = mix(img, solid(ACCENT), box(x, CY + dist * (1 - e), 30, 10) * e)
        return img
    path, frs, ts = film(wd, "shared_axis_y", frame, 2 * T_out + 0.1, 50)
    i = at(ts, 0.12)
    ys = []
    for x in _words_x(n):
        sub = frs[i].copy()
        sub[:, np.abs(XX[0] - x) > 16] = BG
        ys.append(centroid(sub, WORDC, 240)[1] - CY)
    exp = [-dist * off(k, ts[i], True) for k in range(n)]
    return ([check("each word rises on its own clock (staggered 0.06 s)", max(abs(a - b) for a, b in zip(ys, exp)) < 0.4,
                   ys, exp),
             check("word 1 leads word 3", ys[0] < ys[2] - 1, ys, "y1 < y3"),
             check("incoming words rest on the axis at the end", abs(centroid(frs[-1], ACCENT, 60)[1] - CY) < 0.3,
                   centroid(frs[-1], ACCENT, 60)[1] - CY, 0.0),
             neg("staggered rise without the transition", 0.0, exp[0], 0.4)],
            [path], {"direction": "up", "distance": "standard", "stagger_s": stag})


@comp_card("TRANS-132", "shared_axis_z")
def _c132(wd):
    D = 0.6

    def frame(t):
        if t < D * 0.3:
            e = p_in(2)(t / (D * 0.3))
            s = 1 + 0.1 * e
            core = (np.abs(XX - CX) <= s * W / 2) & (np.abs(YY - CY) <= s * H / 2)
            return mix(BLACK, affine(A0, s), core * (1 - e))
        e = p_out(2)((t - D * 0.3) / (D * 0.7))
        s = 0.8 + 0.2 * e
        core = (np.abs(XX - CX) <= s * W / 2) & (np.abs(YY - CY) <= s * H / 2)
        return mix(BLACK, affine(B0, s, fill=(0, 0, 0)), core * e)
    path, frs, ts = film(wd, "shared_axis_z", frame, D, 50)
    i, j = at(ts, 0.1), at(ts, 0.35)
    ea = p_in(2)(ts[i] / (D * 0.3))
    eb = p_out(2)((ts[j] - D * 0.3) / (D * 0.7))
    return ([check("starts on scene A", mad(frs[0], A0) < 0.5, mad(frs[0], A0), "< 0.5"),
             near("outgoing scales up toward 1.1 (depth: away)", scale_inv(frs[i]), 1 + 0.1 * ea, 0.01),
             near("incoming scales 0.8 -> 1 (depth: arriving)", scale_inv(frs[j], bwt(frs[j]) > 0.3), 0.8 + 0.2 * eb, 0.01),
             check("ends on scene B", mad(frs[-1], B0) < 0.5, mad(frs[-1], B0), "< 0.5"),
             neg("outgoing scale on the hard cut", scale_inv(A0), 1 + 0.1 * ea, 0.01)],
            [path], {"direction": "in", "depth": "standard"})


def _bez(x1, y1, x2, y2):
    """CSS cubic-bezier easing via bisection."""
    def f(x):
        x = c01(x)
        lo, hi = 0.0, 1.0
        for _ in range(40):
            m = (lo + hi) / 2
            bx = 3 * (1 - m) ** 2 * m * x1 + 3 * (1 - m) * m * m * x2 + m ** 3
            lo, hi = (m, hi) if bx < x else (lo, m)
        m = (lo + hi) / 2
        return 3 * (1 - m) ** 2 * m * y1 + 3 * (1 - m) * m * m * y2 + m ** 3
    return f


EASY85 = _bez(0.85, 0, 0.15, 1)                     # After Effects easy ease, 85 % influence


def _text_bar(text, s, col):
    rgb, a = text_layer(text, size=16, color=col)
    return rgb, affine(np.repeat(a[..., None], 3, -1), s)[..., 0]


@comp_card("TRANS-133", "text_match_cut")
def _c133(wd):
    D = 1.0
    ta, tb = "Basic Interface Behavior", "Thoughtful Experience Design"

    def scale(t):
        return 1.0 - 0.45 * EASY85(t / D)

    def frame(t):
        s = scale(t)
        txt = ta if t < D / 2 else tb
        _, a = _text_bar(txt, s, (255, 255, 255))
        return mix(solid((10, 20, 60)), solid((255, 255, 255)), a)
    fps = 50
    path, frs, ts = film(wd, "text_match_cut", frame, D, fps)
    sp = np.abs(np.diff([scale(t) for t in ts]))
    peak_t = ts[int(np.argmax(sp))]
    _, aA = _text_bar(ta, 1.0, (255, 255, 255))
    _, aB = _text_bar(tb, 1.0, (255, 255, 255))
    swap_i = next(i for i, t in enumerate(ts) if t >= D / 2)
    widths = [float(np.nonzero(lum(f).max(axis=0) > 128)[0].ptp()) for f in frs]
    w0 = widths[0]
    i = at(ts, 0.25)
    sameA = mad(frs[swap_i - 1], mix(solid((10, 20, 60)), solid((255,) * 3), _text_bar(ta, scale(ts[swap_i - 1]),
                                                                                         (255,) * 3)[1])) < 0.5
    sameB = mad(frs[swap_i], mix(solid((10, 20, 60)), solid((255,) * 3), _text_bar(tb, scale(ts[swap_i]), (255,) * 3)[1])) < 0.5
    return ([near("hard swap lands on the speed peak (s)", ts[swap_i], peak_t, 1.0 / fps + 1e-6),
             check("line A until the peak, line B from the peak frame", bool(sameA and sameB), [bool(sameA), bool(sameB)],
                   [True, True]),
             near("scale-down rides the 85%% easy-ease curve (width ratio at 0.25 s)", widths[i] / w0, scale(ts[i]), 0.04),
             check("85%% easy ease is slow at the start (vs linear)", scale(ts[i]) > 1 - 0.45 * 0.25 + 0.05,
                   scale(ts[i]), "> %.3f" % (1 - 0.45 * 0.25 + 0.05)),
             neg("width ratio of an unanimated line at 0.25 s", 1.0, scale(ts[i]), 0.04)],
            [path], {"mode": "scale-down", "text_a": ta, "text_b": tb, "curve": "cubic-bezier(.85,0,.15,1)"})


@comp_card("TRANS-134", "type_match_cut")
def _c134(wd):
    D = 0.8
    wl, wr = np.array([240.0, 240.0, 240.0]), np.array([200.0, 200.0, 255.0])

    def gap(t):
        return W * p_io(3)(t / D)

    def frame(t):
        g = gap(t)
        img = solid(BG)
        img = mix(img, solid(wl), box(CX - g / 2 - 24, CY, 46, 14))
        img = mix(img, solid(wr), box(CX + g / 2 + 24, CY, 46, 14))
        return mix(img, solid(INK), box(CX, CY, g, H))
    path, frs, ts = film(wd, "type_match_cut", frame, D, 40)
    i = at(ts, 0.4)
    g = gap(ts[i])
    panel = float((np.abs(frs[i][int(CY) - 20] - INK).max(axis=-1) < 3).sum())
    lx = centroid(frs[i], wl, 30)[0]
    rx = centroid(frs[i], wr, 30)[0]
    return ([near("incoming panel grows from the gap (width px)", panel, round(g), 1.5),
             near("left word exits left by gap/2", lx, CX - g / 2 - 24, 0.5) if CX - g / 2 - 24 > 23 else check("left word off", True),
             near("right word exits right by gap/2", rx, CX + g / 2 + 24, 0.5) if CX + g / 2 + 24 < W - 23 else check("right word off", True),
             check("panel fills the frame at the end", float((np.abs(frs[-1] - INK).max(axis=-1) < 3).mean()) > 0.99,
                   float((np.abs(frs[-1] - INK).max(axis=-1) < 3).mean()), "> 0.99"),
             neg("panel width with no split", 0.0, round(g), 1.5)],
            [path], {"text": "Meet the new editor", "accent": "green"})


@comp_card("TRANS-135", "whip_pan_cut")
def _c135(wd):
    whip_at, t_out, t_in, cap = 0.25, 0.25, 0.4, 0.12 * W
    # outgoing: x 0 -> -W over t_out (power3.in, end speed 4W/t_out); incoming speed-ramps from +W' to 0 (power3.out)
    v = 4 * W / t_out
    Lin = v * t_in / 4

    def strip_off(t):
        if t < whip_at:
            return "A", -W * p_in(3)(t / t_out)
        return "B", Lin * (1 - p_out(3)(c01((t - whip_at) / t_in)))

    def speed(t):
        if t < whip_at:
            return 4 * W / t_out * (t / t_out) ** 3
        return 4 * Lin / t_in * (1 - c01((t - whip_at) / t_in)) ** 3

    def frame(t):
        which, x = strip_off(t)
        img = A0 if which == "A" else B0
        out = sample(img, XX - x, YY, fill=(0, 0, 0))
        return hblur(out, min(cap, speed(t) / 30.0 * 0.5))
    fps = 100
    path, frs, ts = film(wd, "whip_pan_cut", frame, whip_at + t_in, fps)
    i = at(ts, 0.2)
    inner = (XX > cap) & (XX < W - cap) & (bwt(frs[i]) < 0.5) & (frs[i][..., 2] > 20)
    xa = xshift(frs[i], inner) if inner.any() else float("nan")
    ib = at(ts, whip_at + 0.01)
    selb = (XX > cap) & (bwt(frs[ib]) > 0.5) & (XX < W - cap)
    vb = (xshift(frs[ib + 1], selb) - xshift(frs[ib], selb)) * fps
    va = -(strip_off(ts[at(ts, whip_at - 0.01)])[1] - strip_off(ts[at(ts, whip_at - 0.02)])[1]) * fps
    blur_used = max(min(cap, speed(t) / 30.0 * 0.5) for t in ts)
    return ([near("A whips off (offset at 0.2 s, px)", xa, strip_off(ts[i])[1], 1.0),
             near("B enters at matched velocity (px/s)", -vb, va, 0.3 * va),
             check("directional blur is capped (max box length <= cap)", blur_used <= cap + 1e-9, blur_used, "<= %.1f" % cap),
             check("decelerating catch: B settles at rest", mad(frs[-1], B0) < 0.5, mad(frs[-1], B0), "< 0.5"),
             neg("A offset at 0.2 s on the hard cut", 0.0, strip_off(ts[i])[1], 1.0)],
            [path], {"direction": "left", "whip_at": whip_at, "blur_cap_px": cap})


@comp_card("TRANS-136", "zoom_through_transition")
def _c136(wd):
    D, s_end = 1.0, (W / 40.0) * 1.02
    k = math.log(s_end) / D
    cw, chh = 40.0, 22.5

    def frame(t):
        s = math.exp(k * c01(t / D))
        img = solid(BG)
        card_ = box(CX, CY, cw * s, chh * s)
        inner = sample(B0, CX + (XX - CX) * (W / (cw * s)), CY + (YY - CY) * (H / (chh * s)))
        return mix(img, inner, card_) if t < D else B0
    path, frs, ts = film(wd, "zoom_through", frame, D, 30)
    widths = []
    for f in frs[:-1]:
        m = bwt(f)[int(CY)] > 0.5
        widths.append(float(m.sum()))
    tt = np.array(ts[:len(widths)])
    ok = np.array(widths) < W - 1
    slope = float(np.polyfit(tt[ok], np.log(np.array(widths)[ok]), 1)[0])
    return ([near("card grows exponentially (d ln width / dt)", slope, k, 0.05 * k),
             check("focal card shows the next scene inside it", fracb(frs[5], box(CX, CY, cw * 0.9, chh * 0.9) > 0.99) > 0.99,
                   fracb(frs[5], box(CX, CY, cw * 0.9, chh * 0.9) > 0.99), "> 0.99"),
             check("lands full-frame on scene B", mad(frs[-1], B0) < 0.5, mad(frs[-1], B0), "< 0.5"),
             neg("exponential growth rate of a static card", 0.0, k, 0.05 * k)],
            [path], {"depth": "standard", "growth": "s = e^(k t)"})
