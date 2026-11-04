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


def centroid(fr, col, tol=None, bg=BG):
    tol = float(np.abs(np.asarray(col) - bg).max()) if tol is None else tol
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
             near("slide wipe: B covers (e x W) columns at the midpoint (blue split widens it by <= amp)", cov, e * W, amp + 1.0),
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
             near("iris radius at open_at + 0.2 s (centre 50%/50%)",
                  float((np.abs(frs[i][int(CY)] - B0[int(CY)]).max(axis=-1) < 2).sum()) / 2, min(r, W / 2), 1.2),
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
    ys = [centroid(f, panel_a)[1] - CY for f in frs]
    st = [ys[i] for i, t in enumerate(ts) if t <= strain]
    inc = np.diff(st)
    yb_meas = [centroid(f, panel_b)[1] - CY for f in frs]
    after = [y for y, t in zip(yb_meas, ts) if t > strain + hold and y == y]
    hold_y = [ys[i] for i, t in enumerate(ts) if strain + 0.01 < t < strain + hold - 0.01]
    return ([check("strain: displacement increments shrink (rising resistance)", bool(np.all(np.diff(np.abs(inc)) < 0.02)),
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
        ys.append(centroid(sub, WORDC)[1] - CY)
    exp = [-dist * off(k, ts[i], True) for k in range(n)]
    return ([check("each word rises on its own clock (staggered 0.06 s)", max(abs(a - b) for a, b in zip(ys, exp)) < 0.4,
                   ys, exp),
             check("word 1 leads word 3", ys[0] < ys[2] - 0.3, ys, "y1 < y3"),
             check("incoming words rest on the axis at the end", abs(centroid(frs[-1], ACCENT)[1] - CY) < 0.3,
                   centroid(frs[-1], ACCENT)[1] - CY, 0.0),
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
    widths = [float(np.ptp(np.nonzero(lum(f).max(axis=0) > 128)[0])) for f in frs]
    w0 = widths[0]
    i = at(ts, 0.4)
    j = at(ts, 0.25)
    sameA = mad(frs[swap_i - 1], mix(solid((10, 20, 60)), solid((255,) * 3), _text_bar(ta, scale(ts[swap_i - 1]),
                                                                                         (255,) * 3)[1])) < 0.5
    sameB = mad(frs[swap_i], mix(solid((10, 20, 60)), solid((255,) * 3), _text_bar(tb, scale(ts[swap_i]), (255,) * 3)[1])) < 0.5
    return ([near("hard swap lands on the speed peak (s)", ts[swap_i], peak_t, 1.0 / fps + 1e-6),
             check("line A until the peak, line B from the peak frame", bool(sameA and sameB), [bool(sameA), bool(sameB)],
                   [True, True]),
             near("scale-down rides the 85% easy-ease curve (width ratio at 0.4 s)", widths[i] / w0, scale(ts[i]), 0.03),
             check("85% easy ease is slow at the start (measured width at 0.25 s vs linear)",
                   widths[j] / w0 > 1 - 0.45 * 0.25 + 0.05, widths[j] / w0, "> %.3f" % (1 - 0.45 * 0.25 + 0.05)),
             neg("width ratio of an unanimated line at 0.4 s", 1.0, scale(ts[i]), 0.03)],
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
    whip_at, t_out, t_in, cap = 0.25, 0.25, 0.25, 0.12 * W
    La = Lb = float(W)          # matched: outgoing end speed 4 La / t_out == incoming start speed 4 Lb / t_in

    def strip_off(t):
        if t < whip_at:
            return "A", -La * p_in(3)(t / t_out)
        return "B", Lb * (1 - p_out(3)(c01((t - whip_at) / t_in)))

    def speed(t):
        if t < whip_at:
            return 4 * La / t_out * (t / t_out) ** 3
        return 4 * Lb / t_in * (1 - c01((t - whip_at) / t_in)) ** 3

    def blen(t):
        return min(cap, speed(t) / 30.0 * 0.5)

    def frame(t):
        which, x = strip_off(t)
        out = sample(A0 if which == "A" else B0, XX - x, YY, fill=(0, 0, 0))
        return hblur(out, blen(t))
    fps = 100
    path, frs, ts = film(wd, "whip_pan_cut", frame, whip_at + t_in, fps)

    def meas(i):
        which, x = strip_off(ts[i])
        m = blen(ts[i]) / 2 + 3
        lo, hi = (m, W + x - m) if which == "A" else (x + m, W - m)
        sel = (XX > lo) & (XX < hi)
        return xshift(frs[i], sel) if sel.sum() > 50 else None
    a_t, a_x, b_t, b_x = [], [], [], []
    for i, t in enumerate(ts):
        v = meas(i)
        if v is None:
            continue
        if t < whip_at and t > 0.12:
            a_t.append(t); a_x.append(v)
        elif t >= whip_at:
            b_t.append(t); b_x.append(v)
    fa = np.array([p_in(3)(t / t_out) for t in a_t])
    La_m = float(-np.dot(fa, a_x) / np.dot(fa, fa))
    fb = np.array([1 - p_out(3)((t - whip_at) / t_in) for t in b_t])
    Lb_m = float(np.dot(fb, b_x) / np.dot(fb, fb))
    va, vb = 4 * La_m / t_out, 4 * Lb_m / t_in
    blur_used = max(blen(t) for t in ts)
    i = at(ts, 0.2)
    return ([near("A whips off on power3.in (fitted travel px)", La_m, La, 2.0),
             near("B catches on power3.out (fitted travel px)", Lb_m, Lb, 2.0),
             near("velocities matched at the cut (incoming / outgoing)", vb / va, 1.0, 0.05),
             check("directional blur is capped (max box length <= cap)", blur_used <= cap + 1e-9, blur_used, "<= %.1f" % cap),
             check("decelerating catch: B settles at rest", mad(frs[-1], B0) < 0.5, mad(frs[-1], B0), "< 0.5"),
             neg("A offset at 0.2 s on the hard cut", xshift(A0, (XX > 30) & (XX < 100)), strip_off(ts[i])[1], 1.0)],
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


@comp_card("TRANS-145", "text_clone_wall")
def _c145(wd):
    rows, t_cover, t_inv, t_clear = 6, 0.8, 0.4, 0.6
    rh = H / rows
    rgb_t, a_t = text_layer("KOSIF KOSIF KOSIF", size=14, color=(20, 20, 20), bg=(255, 255, 255))
    tile = rgb_t
    t_cut = t_cover + t_inv

    def row_x(k, t):
        if t < t_cut:
            return W * (1 - p_out(2)(c01((t - k * 0.08) / (t_cover - 0.08 * (rows - 1)))))
        return -W * p_in(2)(c01((t - t_cut - k * 0.06) / (t_clear - 0.06 * (rows - 1))))

    def frame(t):
        under = A0 if t < t_cut else B0
        out = under.copy()
        rid = np.minimum((YY // rh).astype(int), rows - 1)
        xs = np.array([row_x(k, t) for k in range(rows)])[rid]
        cov = (XX >= xs) & (XX < xs + W)
        wall = sample(tile, XX - xs, YY)
        inv = t_cover <= t < t_cut
        out = np.where(cov[..., None], np.abs(wall - under) if inv else wall, out)
        return out
    T = t_cut + t_clear
    path, frs, ts = film(wd, "clone_wall", frame, T, 40)
    ic = at(ts, t_cover + 0.05)
    covered = float(np.mean(np.abs(frs[ic] - np.abs(tile - A0)).max(axis=-1) < 2))
    ii = at(ts, t_cover + 0.2)
    wall_bg = np.abs(tile - 255).max(axis=-1) < 1
    inv_err = float(np.mean(np.abs(frs[ii][wall_bg] - (255 - A0[wall_bg]))))
    cut_cov = [float(np.mean(np.abs(frs[i] - A0).max(axis=-1) > 2)) for i in range(len(ts)) if abs(ts[i] - t_cut) < 0.03]
    return ([check("word wall covers the whole frame", covered > 0.99, covered, "> 0.99"),
             near("difference blend inverts the scene under the wall", inv_err, 0.0, 1.0),
             check("hard cut A->B happens underneath while covered", mad(frs[0], A0) < 0.5 and mad(frs[-1], B0) < 0.5
                   and min(cut_cov) > 0.95, [mad(frs[0], A0), mad(frs[-1], B0), min(cut_cov)], "A, B, covered at cut"),
             neg("inversion error on the bare scene", float(np.mean(np.abs(A0[wall_bg] - (255 - A0[wall_bg])))), 0.0, 1.0)],
            [path], {"duration": T, "rows": rows})


LIGHT, DARK = np.array([245.0, 245.0, 240.0]), np.array([20.0, 20.0, 24.0])


@comp_card("TRANS-164", "vfx_portal")
def _c164(wd):
    D = 1.0
    rmax = math.hypot(W, H) / 2 + 4

    def frame(t):
        e = p_io(2)(t / D)
        r = rmax * e
        d = np.hypot((XX - CX) * 1.0, (YY - CY) * 1.4)
        out = np.where((d < r)[..., None], solid(DARK), solid(LIGHT))
        rim = np.exp(-((d - r) / 2.0) ** 2) * (0 < e < 1)
        return screen(out, ACCENT * rim[..., None])
    path, frs, ts = film(wd, "portal", frame, D, 30)
    i = at(ts, 0.4)
    r = rmax * p_io(2)(ts[i] / D)
    dark_w = float((np.abs(frs[i][int(CY)] - DARK).max(axis=-1) < 20).sum()) / 2
    dark_h = float((np.abs(frs[i][:, int(CX)] - DARK).max(axis=-1) < 20).sum()) / 2
    rimv = float(frs[i][int(CY), int(CX + r) - 3:int(CX + r) + 4, 2].max())
    return ([check("light panel to dark panel (polarity flips)", lum(frs[0]).mean() > 200 and lum(frs[-1]).mean() < 40,
                   [float(lum(frs[0]).mean()), float(lum(frs[-1]).mean())], "light -> dark"),
             near("portal half-width on the row", dark_w, r - 2, 2.0),
             near("portal is an ellipse (height/width = 1/1.4)", dark_h / max(dark_w, 1e-6), 1 / 1.4, 0.06),
             check("glowing rim at the portal edge", rimv > 250, rimv, "> 250"),
             neg("portal half-width on a hard cut", 0.0, r - 2, 2.0)],
            [path], {"panels": ["light", "dark"], "duration": D})


@comp_card("TRANS-165", "vfx_shatter")
def _c165(wd):
    rng = np.random.default_rng(5)
    n, D = 24, 1.0
    pts = rng.random((n, 2)) * [W, H]
    dist = np.stack([np.hypot(XX - x, YY - y) for x, y in pts])
    lab = dist.argmin(0)
    vel = np.c_[rng.uniform(-40, 40, n), rng.uniform(-30, 10, n)]
    rot = rng.uniform(-1.5, 1.5, n)
    delay = (pts[:, 0] / W) * 0.3

    def frame(t):
        out = B0.copy()
        for k in range(n):
            tk = max(0.0, t - delay[k])
            if tk <= 0:
                dx = dy = th = 0.0
            else:
                dx, dy, th = vel[k, 0] * tk, vel[k, 1] * tk + 0.5 * 400 * tk * tk, rot[k] * tk
            cx_, cy_ = pts[k]
            u, v = XX - cx_ - dx, YY - cy_ - dy
            c, s_ = math.cos(-th), math.sin(-th)
            sx, sy = u * c - v * s_ + cx_, u * s_ + v * c + cy_
            inb = (sx >= 0) & (sx <= W - 1) & (sy >= 0) & (sy <= H - 1)
            si = np.clip(np.rint(sx), 0, W - 1).astype(int)
            sj = np.clip(np.rint(sy), 0, H - 1).astype(int)
            mine = inb & (lab[sj, si] == k)
            out = np.where(mine[..., None], sample(A0, sx, sy), out)
        return out
    path, frs, ts = film(wd, "shatter", frame, D, 20)
    i = at(ts, 0.35)
    fb = [fracb(frs[at(ts, t)]) for t in (0.1, 0.35, 0.7)]
    # rigid shards: for shard 0 pixels still shown as A, the source coords are one rotation+translation of the pixel coords
    sel = (bwt(frs[i]) < 0.5)
    sx_, sy_ = srcx(frs[i]), srcy(frs[i])
    owner = lab[np.clip(np.rint(sy_), 0, H - 1).astype(int), np.clip(np.rint(sx_), 0, W - 1).astype(int)]
    moved = [kk for kk in range(n) if delay[kk] < 0.3]
    k = max(moved, key=lambda kk: int((sel & (owner == kk)).sum()))
    m = sel & (owner == k)
    Amat = np.c_[XX[m], YY[m], np.ones(m.sum())]
    cx_ = np.linalg.lstsq(Amat, sx_[m], rcond=None)
    resid = float(np.sqrt(np.mean((Amat @ cx_[0] - sx_[m]) ** 2))) if m.sum() > 6 else 99.0
    return ([check("starts as the intact panel A", mad(frs[0], A0) < 0.5, mad(frs[0], A0), "< 0.5"),
             check("revealed B grows as shards fall", fb[0] < fb[1] < fb[2], fb, "increasing"),
             check("each shard moves rigidly (affine fit residual px)", resid < 0.6, resid, "< 0.6"),
             check("%d Voronoi shards" % n, len(np.unique(lab)) == n, int(len(np.unique(lab))), n),
             neg("revealed B on the intact panel", fracb(A0), fb[1], 0.0)],
            [path], {"shards": n, "gravity_px_s2": 400})


@comp_card("TRANS-167", "dom_to_texture")
def _c167(wd):
    from PIL import Image
    texA, _ = text_layer("SCENE A", size=24, color=(255, 255, 255), bg=(30, 40, 90))
    texB, _ = text_layer("SCENE B", size=24, color=(20, 20, 20), bg=(240, 200, 60))
    pa, pb = Path(wd) / "u_from.png", Path(wd) / "u_to.png"
    Image.fromarray(texA.astype(np.uint8)).save(pa)
    Image.fromarray(texB.astype(np.uint8)).save(pb)
    u_from = np.asarray(Image.open(pa), float)                 # captured once, reused every frame
    u_to = np.asarray(Image.open(pb), float)
    pf = lambda t: prog(t, 1.0, 2.0, p_io(1))                  # noqa: E731
    path, frs, ts = film(wd, "dom_shader", lambda t: mix(u_from, u_to, pf(t)), 4.0, 10)
    diff = u_to - u_from
    meas = [float(np.sum((f - u_from) * diff) / np.sum(diff * diff)) for f in frs]
    exp = [pf(t) for t in ts]
    lin_ = [c01((t - 1) / 2) for t in ts]
    err = float(np.max(np.abs(np.array(meas) - np.array(exp))))
    err_lin = float(np.max(np.abs(np.array(meas) - np.array(lin_))))
    gl_path, gfrs, gts = film(wd, "dom_glitch", lambda t: sh_glitch(u_from, u_to, pf(t)), 4.0, 10)
    uniq = len(np.unique(gfrs[at(gts, 2.0)][..., 1]))
    return ([check("u_progress per frame follows quadInOut over t = 1..3 s (max error)", err < 0.01, err, "< 0.01"),
             check("textures rasterised once: each frame is mix(u_from, u_to, p)",
                   max(mad(f, mix(u_from, u_to, m)) for f, m in zip(frs, meas)) < 0.6,
                   max(mad(f, mix(u_from, u_to, m)) for f, m in zip(frs, meas)), "< 0.6"),
             check("glitch shader on the same textures quantises to 8 levels at the peak", uniq <= 8, uniq, "<= 8"),
             neg("linear progress against the measured curve (max error)", err_lin, 0.0, 0.01)],
            [path, gl_path, pa, pb], {"uniforms": ["u_from", "u_to", "u_progress", "u_resolution"], "window_s": [1, 3]})


@comp_card("TRANS-168", "clip_path_wipe")
def _c168(wd):
    T0, D = 0.1, 0.5

    def frame(t):
        e = p_out(1)((t - T0) / D)
        return np.where((XX < e * W)[..., None], B0, A0)
    path, frs, ts = film(wd, "clip_wipe", frame, T0 + D + 0.1, 40)
    i = at(ts, T0 + 0.2)
    e = p_out(1)((ts[i] - T0) / D)
    split = np.where((XX < W / 2)[..., None], A0, B0)
    sp = write_video([split] * 10, Path(wd) / "split_screen.mp4", 10)
    sfr = fx.frames(sp, (W, H))[0]
    return ([*ends(frs, A0, B0, name="clip-path wipe"),
             near("polygon edge at +0.2 s (power1.out, 0.5 s overlap)", float(b_width(frs[i])), math.ceil(e * W - 1e-9), 1.0),
             check("split-screen: left half A, right half B", fracb(sfr, XX < W / 2) == 0 and fracb(sfr, XX >= W / 2) == 1,
                   [fracb(sfr, XX < W / 2), fracb(sfr, XX >= W / 2)], [0, 1]),
             neg("polygon edge on the hard cut", float(b_width(A0)), math.ceil(e * W - 1e-9), 1.0)],
            [path, sp], {"overlap_s": D})


def _lane(pts, t):
    ks = sorted(pts)
    return float(np.interp(t, ks, [pts[k] for k in ks]))


def tone_amp(sig, rate, f, t0, t1):
    seg = sig[int(t0 * rate):int(t1 * rate)]
    n = np.arange(len(seg)) / rate
    return float(2 * abs(np.mean(seg * np.exp(-2j * np.pi * f * n))))


@comp_card("TRANS-169", "crossfade_volume_lanes")
def _c169(wd):
    rate, T, startB = 16000, 3.5, 2.5
    t = np.arange(int(T * rate)) / rate
    la = np.array([_lane({0: 1, 2.5: 1, 3: 0}, x) for x in t])
    lb = np.array([_lane({0: 0, 0.5: 1}, x - startB) if x >= startB else 0.0 for x in t])
    sig = 0.4 * la * np.sin(2 * np.pi * 440 * t) + 0.4 * lb * np.sin(2 * np.pi * 660 * t)
    wav = fx.write_wav(Path(wd) / "mix.wav", sig, rate)
    path, frs, ts = film(wd, "crossfade_video", lambda x: mix(A0, B0, c01((x - 2.5) / 0.5)), T, 10)
    out = Path(wd) / "crossfade.mp4"
    fx.ffmpeg("-i", str(path), "-i", str(wav), "-c:v", "copy", "-c:a", "pcm_s16le", "-shortest", str(out.with_suffix(".mov")))
    s2, r2 = fx.read_wav(wav)
    s2 = s2[:, 0]
    aa = tone_amp(s2, r2, 440, 2.70, 2.80) / 0.4
    ab = tone_amp(s2, r2, 660, 2.70, 2.80) / 0.4
    a_end = tone_amp(s2, r2, 440, 3.2, 3.4) / 0.4
    i = at(ts, 2.75)
    return ([near("track A volume at 2.75 s (lane 1 -> 0 over 2.5..3 s)", aa, 0.5, 0.05),
             near("track B volume at 2.75 s (lane 0 -> 1 over its first 0.5 s)", ab, 0.5, 0.05),
             near("track A silent after 3 s", a_end, 0.0, 0.02),
             near("opacity crossfade 0.5 s at 2.5 s (B weight near 2.75 s)", float(bwt(frs[i]).mean()), c01((ts[i] - 2.5) / 0.5), 0.02),
             neg("track A volume at 2.75 s without the envelope", 1.0, 0.5, 0.05)],
            [path, wav, out.with_suffix(".mov")], {"lanes": {"a": {0: 1, 2.5: 1, 3: 0}, "b": {0: 0, 0.5: 1}}, "overlap_s": 0.5})


def _steps(n):
    return lambda x: math.floor(c01(x) * n) / n if x < 1 else 1.0


@comp_card("TRANS-170", "chromatic_glitch_gsap")
def _c170(wd):
    D, q, nsl = 0.6, 1 / 24.0, 6
    el = np.array([240.0, 240.0, 240.0])

    def state(t):
        sx = 1.5 - 0.5 * p_out(4)(t / 0.5)
        k = int(math.floor(t / q + 1e-9))
        env = 1 - c01(k * q / D)                    # envelope also read at the quantised time
        jit = (_h(k, 51) - 0.5) * 2 * 6 * env
        st = _steps(5)(t / 0.5)
        offs = [(_h(j, 52) - 0.5) * 2 * 20 * (1 - st) for j in range(nsl)]
        return sx, jit, offs

    def frame(t):
        sx, jit, offs = state(t)
        img = solid(BG)
        band = np.minimum((YY - (CY - 15)) // 5, nsl - 1).astype(int)
        dx = np.where((YY >= CY - 15) & (YY < CY + 15), np.array(offs)[np.clip(band, 0, nsl - 1)], 0.0)
        a = box(CX + dx, CY, 80 * sx, 30)
        img = mix(img, solid(el), a)
        if abs(jit) > 0.01:
            r = box(CX + dx + jit, CY, 80 * sx, 30)
            img[..., 0] = np.maximum(img[..., 0], 255 * r)
        return img
    path, frs, ts = film(wd, "chromatic_glitch", frame, D + 0.1, 48)
    path2, frs2, _ = film(wd, "chromatic_glitch_rerun", frame, D + 0.1, 48)
    late = [i for i, t in enumerate(ts) if 0.5 <= t < 0.6 - 1e-9]       # stretch and slices done, jitter still live
    pairs_equal = all(np.array_equal(frs[i], frs[i + 1]) for i in late[::2] if i + 1 in late) and \
        not np.array_equal(frs[late[0]], frs[late[2]])
    levels = len({tuple(np.round(state(t)[2], 6)) for t in ts if t < 0.5})
    rest = solid(BG)
    rest = mix(rest, solid(el), box(CX, CY, 80, 30))
    i = at(ts, 0.1)
    wid = float((np.abs(frs[i][int(CY) + 12] - el).max(axis=-1) < 30).sum())
    return ([check("deterministic: re-render is byte-identical", bool(np.array_equal(frs, frs2)), True, True),
             check("jitter held per quantised 1/24 s step (48 fps frame pairs equal, steps differ)", bool(pairs_equal), bool(pairs_equal), True),
             check("slice bands converge on a stepped ease (5 discrete states)", levels == 5, levels, 5),
             check("clean clamped rest after the burst", mad(frs[-1], rest) < 0.3, mad(frs[-1], rest), "< 0.3"),
             near("stretch entrance: scaleX 1.5 -> 1 power4.out at 0.1 s (width px)", wid,
                  round(80 * (1.5 - 0.5 * p_out(4)(ts[i] / 0.5))), 3.0),
             neg("stepped-state count of an unglitched element", 1, 5, 0)],
            [path], {"quantum_s": q, "slices": nsl, "steps": 5})


@comp_card("TRANS-171", "scale_swap")
def _c171(wd):
    t_out, t_in = 0.3, 0.5
    ca, cb = np.array([240.0, 120.0, 60.0]), np.array([80.0, 180.0, 255.0])

    def frame(t):
        img = solid(BG)
        if t < t_out:
            e = p_in(2)(t / t_out)
            return mix(img, solid(ca), box(CX, CY, 40 * (1 - e), 40 * (1 - e)) * (1 - e))
        s = back_out(2.0)((t - t_out) / t_in)
        return mix(img, solid(cb), box(CX, CY, 40 * s, 40 * s))
    path, frs, ts = film(wd, "scale_swap", frame, t_out + t_in + 0.1, 50)
    wb = [float((np.abs(f[int(CY)] - cb).max(axis=-1) < 100).sum()) for f, t in zip(frs, ts) if t >= t_out]
    peak = max(wb) / 40
    xs = np.linspace(0, 1, 2001)
    peak_exp = max(back_out(2.0)(x) for x in xs)
    wa = [float((np.abs(f[int(CY)] - BG).max(axis=-1) > 3).sum()) for f, t in zip(frs, ts) if t < t_out]
    cA, cB = centroid(frs[2], ca), centroid(frs[-1], cb)
    return ([near("entrance overshoot peak = max back.out(2) (scale)", peak, peak_exp, 0.05),
             check("settles at scale 1", abs(wb[-1] - 40) <= 1, wb[-1], 40),
             check("exit shrinks monotonically (power2.in)", all(b <= a for a, b in zip(wa, wa[1:])), wa[:6], "non-increasing"),
             check("shared transform-origin 50% 50%", abs(cA[0] - cB[0]) < 0.3 and abs(cA[1] - cB[1]) < 0.3,
                   [cA[:2], cB[:2]], "same centre"),
             neg("overshoot of a plain scale-in", 1.0, peak_exp, 0.05)],
            [path], {"incoming": "back.out(2)", "outgoing": "power2.in"})


THEMES = [np.array([245.0, 240.0, 230.0]), np.array([20.0, 24.0, 40.0]), np.array([230.0, 60.0, 50.0])]


@comp_card("TRANS-172", "theme_crossfade_anchor")
def _c172(wd):
    md, hold = 0.3, 0.3
    anchor = box(CX, CY, 30, 30)
    anchor_c = np.array([255.0, 200.0, 0.0])

    def theme_w(t):
        w = [1.0, 0.0, 0.0]
        for k in (1, 2):
            t0 = k * (hold + md) - md
            e = p_io(1)((t - t0) / md)
            w = [x * (1 - e) for x in w]
            w[k] += e
        return w

    def frame(t):
        w = theme_w(t)
        bg = sum(wk * solid(c) for wk, c in zip(w, THEMES))
        return mix(bg, solid(anchor_c), anchor)
    T = 3 * (hold + md) - md
    path, frs, ts = film(wd, "theme_morph", frame, T, 40)
    amask = anchor > 0.999
    drift = max(mad(f[amask], frs[0][amask]) for f in frs)
    i = at(ts, hold + md / 2)
    bgm = frs[i][2, 2]
    w = theme_w(ts[i])
    return ([check("anchor never moves or changes (max deviation)", drift < 0.5, drift, "< 0.5"),
             near("theme crossfade mid-point (power2.inOut) background", float(bgm[0]),
                  float(sum(wk * c[0] for wk, c in zip(w, THEMES))), 1.5),
             check("passes through all 3 pre-styled themes", all(mad(frs[at(ts, k * (hold + md) + 0.01)][2, 2], c) < 2
                                                                  for k, c in enumerate(THEMES)), True, True),
             neg("background change with no crossfade", float(THEMES[0][0]), float(sum(wk * c[0] for wk, c in zip(w, THEMES))),
                 1.5)],
            [path], {"themes": 3, "morph_s": md})


# ═════════════════════ motion-kit seams: iris / flood, flashes, dips, band wipes, cut rhythms ═════════════════════
MK_NOTE = "motion-kit easing E.out/E.in taken as power3.out/power3.in (motion-kit.js not loaded here)"
E_OUT, E_IN = p_out(2), p_in(2)


def ray_len(fr, cx, cy, ref=None, tol=3):
    """Run of pixels matching ref (default scene B) from the centre along the longer horizontal direction."""
    ref = B0 if ref is None else ref
    ok = np.abs(fr - ref).max(axis=-1) < tol
    y, x0 = int(round(cy)), int(round(cx))
    right = W - x0 >= x0
    xs = range(x0, W) if right else range(x0, -1, -1)
    n = 0
    for x in xs:
        if not ok[y, x]:
            break
        n += 1
    return float(n), float((W - x0) if right else (x0 + 1))


def r_log(r0, r1, e):
    return math.exp(math.log(r0) + (math.log(r1) - math.log(r0)) * e)


def iris_card(card_id, name, cx, cy, r0, r1, dur, ease, logspace=True, close=False, feather=0.75, ring=None,
              ringc=ACCENT, inside=None, T0=0.1, fps=40, probe_fr=(0.25, 0.5), extra=None, note=MK_NOTE):
    inside = B0 if inside is None else inside

    def radius(u):
        e = ease(u / dur)
        return r_log(r0, r1, e) if logspace else r0 + (r1 - r0) * e

    def frame(t):
        u = round(t - T0, 6)
        if close:
            if u < 0:
                return inside.copy()
            r = radius(dur - u) if u < dur else 0.0
        else:
            if u < 0:
                return A0.copy()
            r = radius(u) if u < dur else 1e4
        m = disc(cx, cy, r, feather) if r > 0 else np.zeros((H, W))
        out = mix(A0, inside, m)
        if ring and 0 < r < 1e4:
            d = np.hypot(XX - cx, YY - cy)
            out = np.where(((d >= r + feather) & (d < r + feather + ring))[..., None], ringc, out)
        return out

    def run(task, wd):
        path, frs, ts = film(wd, name, frame, T0 + dur + 0.1, fps)
        checks = []
        for f in probe_fr:
            i = at(ts, T0 + f * dur)
            u = ts[i] - T0
            r = radius(dur - u) if close else radius(u)
            meas, room = ray_len(frs[i], cx, cy, inside)
            if r + 1 < room:
                checks.append(near("radius at %.0f%% of %.2f s%s" % (f * 100, dur, " (log space)" if logspace else ""),
                                   meas, r, 1.0 + feather))
        if logspace:
            i = at(ts, T0 + probe_fr[0] * dur)
            u = ts[i] - T0
            e = ease((dur - u) / dur if close else u / dur)
            lin_r = r0 + (r1 - r0) * e
            meas = ray_len(frs[i], cx, cy, inside)[0]
            checks.append(check("radius follows log space, not linear (|meas - linear| > 3 px)", abs(meas - lin_r) > 3,
                                [meas, lin_r], "differs"))
        if ring:
            i = at(ts, T0 + probe_fr[0] * dur)
            checks.append(check("ring drawn ahead of the edge", bool((np.abs(frs[i] - ringc).max(axis=-1) < 2).any()), True, True))
        end_ref = A0 if close else inside
        checks.append(check("ends on the %s" % ("hidden state (A)" if close else "revealed scene"),
                            mad(frs[-1], end_ref) < 0.5, mad(frs[-1], end_ref), "< 0.5"))
        i = at(ts, T0 + (probe_fr[0] if close else probe_fr[-1]) * dur)
        u = ts[i] - T0
        r = radius(dur - u) if close else radius(u)
        checks.append(neg("radius on the hard cut", ray_len(A0 if (u < dur / 2) != close else inside, cx, cy, inside)[0],
                          r, 1.0 + feather))
        if extra:
            checks += extra(frs, ts, T0)
        plan = save_plan(wd, name, {"card": card_id, "centre": [cx, cy], "r0": r0, "r1": r1, "dur": dur, "log_space": logspace,
                                    "close": close, "feather": feather, "note": note})
        return checks, [path, plan]
    card(card_id)(run)


iris_card("TRANS-254", "iris_open", CX, CY, 1 * K * 10, 2300 * K, 0.4, E_OUT)
iris_card("TRANS-30", "iris_reveal_close", CX, CY, 1 * K * 10, 2300 * K, 0.4, E_IN, close=True, probe_fr=(0.5, 0.75))
iris_card("TRANS-266", "circle_iris_ring", CX, CY, 0.0, 1.2 * math.hypot(W, H) / 2, 0.45, p_io(2), logspace=False, ring=1.5,
          note="radius 0 -> 120% of the half-diagonal, easeInOutCubic")
iris_card("TRANS-268", "soft_iris_focal", 0.3 * W, 0.6 * H, 0.0, math.hypot(W, H), 0.3, expo_io, logspace=False,
          feather=20 * K, probe_fr=(0.5, 0.6), note="feather 20 css px")
iris_card("TRANS-294", "disc_expand_wipe", 0.7 * W, 0.4 * H, 0.0, math.hypot(W, H), 0.4, p_out(1), logspace=False,
          probe_fr=(0.2, 0.4), note="disc from a point, 400 ms")


def _flood_extra(frs, ts, T0):
    red = hexc("#e4342f")
    return [check("flood colour fills the whole frame at the end", mad(frs[-1], solid(red)) < 0.5, mad(frs[-1], solid(red)), "< 0.5")]


iris_card("TRANS-231", "iris_flood_seam", CX, CY, 1.0, 2300 * K, 0.4, E_OUT, inside=solid("#e4342f"), extra=_flood_extra)
iris_card("TRANS-246", "iris_colour_flood", 0.25 * W, 0.5 * H, 1.0, 2300 * K, 0.3, E_OUT, inside=solid("#e4342f"),
          extra=_flood_extra, probe_fr=(0.2, 0.35))


def _dot_iris(card_id, name, beat=0.3):
    r0, r1, dur = 22 * K, 1150 * K, 0.42

    def frame(t):
        u = round(t - beat, 6)
        if u < 0:
            return mix(A0, solid(ACCENT), disc(CX, CY, r0))
        r = r_log(r0, r1, E_OUT(u / dur)) if u < dur else 1e4
        out = mix(A0, B0, disc(CX, CY, r))
        if u < 0.05:
            out = mix(out, solid(ACCENT), disc(CX, CY, r0))
        return out

    def run(task, wd):
        path, frs, ts = film(wd, name, frame, beat + dur + 0.1, 40)
        i = at(ts, beat + 0.15)
        r = r_log(r0, r1, E_OUT((ts[i] - beat) / dur))
        dot_before = bool((np.abs(frs[at(ts, beat - 0.05)][int(CY), int(CX)] - ACCENT) < 2).all())
        dot_after = bool((np.abs(frs[at(ts, beat + 0.1)] - ACCENT).max(axis=-1) < 2).any())
        checks = [check("travelling dot visible before the drop beat", dot_before, dot_before, True),
                  check("dot hidden 0.05 s after the iris starts", not dot_after, dot_after, False),
                  near("iris radius r0 22 -> r 1150 css px in log space at +0.15 s", ray_len(frs[i], CX, CY)[0], r, 1.0),
                  check("lands on full-bleed footage (scene B)", mad(frs[-1], B0) < 0.5, mad(frs[-1], B0), "< 0.5"),
                  neg("iris radius on a hard cut at the beat", ray_len(A0, CX, CY)[0], r, 1.0)]
        plan = save_plan(wd, name, {"card": card_id, "beat_s": beat, "r0": r0, "r1": r1, "dur": dur, "note": MK_NOTE})
        return checks, [path, plan]
    card(card_id)(run)


_dot_iris("TRANS-236", "iris_from_dot")


def _digit_iris(task, wd):
    from PIL import Image, ImageDraw, ImageFont
    from scipy import ndimage
    im = Image.new("L", (W, H), 0)
    try:
        font = ImageFont.load_default(size=80)
    except TypeError:
        font = ImageFont.load_default()
    ImageDraw.Draw(im).text((W * 0.35, H / 2), "0", fill=255, font=font, anchor="mm")
    glyph = np.asarray(im) > 128
    lab_, n = ndimage.label(~glyph)
    outside = lab_[0, 0]
    holes = [k for k in range(1, n + 1) if k != outside and (lab_ == k).sum() > 10]
    hole = lab_ == holes[0]
    hx, hy = float(XX[hole].mean()), float(YY[hole].mean())
    newc = np.array([30.0, 160.0, 90.0])
    base = np.where(glyph[..., None], np.array([250.0, 250.0, 250.0]), np.array([20.0, 20.0, 30.0]))
    rmax = max(math.hypot(hx - x, hy - y) for x in (0, W) for y in (0, H)) + 2
    T0, dur = 0.1, 0.4

    def frame(t):
        u = round(t - T0, 6)
        if u < 0:
            return base
        r = rmax * p_in(1)(u / dur) if u < dur else 1e4
        out = mix(base, solid(newc), disc(hx, hy, r))
        d = np.hypot(XX - hx, YY - hy)
        return np.where(((d >= r + 0.75) & (d < r + 2.25))[..., None], ACCENT, out) if u < dur else out
    path, frs, ts = film(wd, "digit_iris", frame, T0 + dur + 0.1, 40)
    i = at(ts, T0 + 0.6 * dur)
    m = np.abs(frs[i] - newc).max(axis=-1) < 3
    cxm, cym = float(XX[m].mean()), float(YY[m].mean())
    r = rmax * p_in(1)((ts[i] - T0) / dur)
    checks = [near("iris centre = centroid of the digit's counter (x)", cxm, hx, 0.6),
              near("iris centre = centroid of the digit's counter (y)", cym, hy, 0.6),
              near("disc radius at 60%% (easeIn)", math.sqrt(m.sum() / math.pi), r, 1.0),
              check("accent ring stroke on the disc", bool((np.abs(frs[i] - ACCENT).max(axis=-1) < 2).any()), True, True),
              check("covers the frame with the next scene colour", mad(frs[-1], solid(newc)) < 0.5, mad(frs[-1], solid(newc)),
                    "< 0.5"),
              neg("disc centre if grown from the frame centre (x)", CX, hx, 0.6)]
    plan = save_plan(wd, "digit_iris", {"card": "TRANS-297", "hole_centroid": [hx, hy], "dur": dur})
    return checks, [path, plan]


card("TRANS-297")(_digit_iris)


def _dot_disc(task, wd):
    r_dot, T0, grow, reveal = 1.5, 0.1, 0.4, 0.3
    ring = 1.0

    def frame(t):
        u = round(t - T0, 6)
        if u < grow:
            s = 1 + 29 * p_io(1)(max(u, 0) / grow)
            return mix(A0, solid(ACCENT), disc(CX, CY, r_dot * s))
        R = r_dot * 30
        f = c01((u - grow) / reveal)
        out = mix(A0, solid(ACCENT), disc(CX, CY, R))
        out = mix(out, B0, disc(CX, CY, R - ring) * f)
        return out
    path, frs, ts = film(wd, "dot_to_disc", frame, T0 + grow + reveal + 0.1, 40)
    i = at(ts, T0 + grow / 2)
    s = 1 + 29 * p_io(1)((ts[i] - T0) / grow)
    m = np.abs(frs[i] - ACCENT).max(axis=-1) < 3
    rad = math.sqrt(m.sum() / math.pi)
    last = frs[-1]
    inner = disc(CX, CY, r_dot * 30 - ring - 1) > 0.99
    return ([near("dot scales 1 -> 30 (easeInOut) at 200 ms (radius px)", rad, r_dot * s, 0.8),
             check("disc becomes a circular mask onto the photo", mad(last[inner], B0[inner]) < 0.5, mad(last[inner], B0[inner]),
                   "< 0.5"),
             check("accent ring around the portrait", bool((np.abs(last - ACCENT).max(axis=-1) < 3).any()), True, True),
             neg("dot radius without the scale-up", r_dot, r_dot * s, 0.8)],
            [path, save_plan(wd, "dot_disc", {"card": "TRANS-287", "scale": [1, 30], "ms": 400})])


card("TRANS-287")(_dot_disc)


# ───── flashes ─────
def overlay_alpha(fr, base, colour):
    colour = np.broadcast_to(np.asarray(colour, float), fr.shape)
    den = colour - base
    c = np.argmax(np.abs(den), axis=-1)
    dd = np.take_along_axis(den, c[..., None], -1)[..., 0]
    num = np.take_along_axis(fr - base, c[..., None], -1)[..., 0]
    sel = np.abs(dd) > 150
    return float(np.median(num[sel] / dd[sel])) if sel.any() else float("nan")


def flash_alpha(u, peak, rise, dur, again=None):
    a = 0.0
    if 0 <= u < rise:
        a = peak * u / rise
    elif u >= rise:
        a = peak * (1 - p_out(3)(c01((u - rise) / dur)))
    if again:
        pk2, dt = again
        u2 = u - dt
        if 0 <= u2 < rise:
            a = max(a, pk2 * u2 / rise)
        elif u2 >= rise:
            a = max(a, pk2 * (1 - p_out(3)(c01((u2 - rise) / dur))))
    return a


def flash_card(card_id, name, peak, rise, dur, again=None, colour=(255, 255, 255), at_=0.2, fps=100):
    col = np.asarray(colour, float)

    def frame(t):
        u = round(t - at_, 6)
        base = A0 if u < rise else B0
        return mix(base, solid(col), flash_alpha(u, peak, rise, dur, again))

    def run(task, wd):
        total = at_ + rise + dur + (again[1] if again else 0) + 0.05
        path, frs, ts = film(wd, name, frame, total, fps)
        checks = []
        for u in (rise, rise + 0.1, rise + 0.25):
            i = at(ts, at_ + u)
            uu = round(ts[i] - at_, 6)
            base = A0 if uu < rise else B0
            checks.append(near("flash opacity at +%.2f s" % u, overlay_alpha(frs[i], base, col),
                               flash_alpha(uu, peak, rise, dur, again), 0.02))
        if again:
            i = at(ts, at_ + again[1] + rise)
            checks.append(near("double flicker: second peak %.2f at +%.2f s" % (again[0], again[1]), overlay_alpha(frs[i], B0, col),
                               flash_alpha(ts[i] - at_, peak, rise, dur, again), 0.03))
        checks.append(check("hard change hidden under the flash: A before, B after", mad(frs[0], A0) < 0.5 and mad(frs[-1], B0) < 1,
                            [mad(frs[0], A0), mad(frs[-1], B0)], "< 0.5, < 1"))
        i = at(ts, at_ + rise)
        checks.append(neg("flash opacity on the bare cut", overlay_alpha(B0, B0, col), peak, 0.02))
        plan = save_plan(wd, name, {"card": card_id, "peak": peak, "rise_s": rise, "decay_s": dur, "again": again,
                                    "decay_ease": "power4.out"})
        return checks, [path, plan]
    card(card_id)(run)


flash_card("TRANS-235", "white_flash_accent", 0.6, 0.06, 0.3, again=(0.5, 0.16))
flash_card("TRANS-253", "flash_frame", 0.85, 0.06, 0.35, again=(0.5, 0.16))


def _seams_and_end(task, wd):
    warm = hexc("#fff6e0")
    fl1, end_at, S = 0.3, 1.0, 1.6

    def frame(t):
        base = A0 if t < fl1 + 0.06 else B0
        img = mix(base, solid(warm), flash_alpha(round(t - fl1, 6), 0.9, 0.06, 0.45))
        return mix(img, BLACK, sine_io((t - end_at) / 0.6))
    path, frs, ts = film(wd, "seams_end", frame, S, 50)
    i = at(ts, fl1 + 0.06)
    j = at(ts, end_at + 0.3)
    k = at(ts, fl1 + 0.06 + 0.2)
    return ([near("warm-white flash seals the act change (peak 0.9)", overlay_alpha(frs[i], B0, warm), 0.9, 0.02),
             near("flash decays over 0.45 s (power4.out)", overlay_alpha(frs[k], B0, warm),
                  flash_alpha(ts[k] - fl1, 0.9, 0.06, 0.45), 0.02),
             near("ending fade to black half-way at +0.3 s (smooth)", overlay_alpha(frs[j], B0, (0, 0, 0)), sine_io(0.5), 0.02),
             check("film ends on black", float(frs[-1].max()) < 1, float(frs[-1].max()), "< 1"),
             neg("black on the last frame without the fade", float(B0.max()), 0.0, 1.0)],
            [path, save_plan(wd, "seams_end", {"card": "TRANS-245", "flash": {"peak": 0.9, "dur": 0.45, "color": "#fff6e0"},
                                               "end_fade_s": 0.6})])


card("TRANS-245")(_seams_and_end)


# ───── dips and fades ─────
def _dip_endings(task, wd):
    S = 1.0
    variants = {"premium_dim": (BLACK, lambda t: p_in(1)((t - (S - 0.32)) / 0.32), 1.0),
                "lab_ink": (solid("#0f1512"), lambda t: c01((t - (S - 0.6)) / 0.6), 1.0),
                "bunny_fade": (BLACK, lambda t: 0.85 * c01((t - (S - 0.14)) / 0.14), 0.85)}
    checks, outs = [], []
    for name, (col, af, final) in variants.items():
        path, frs, ts = film(wd, name, lambda t: mix(B0, col, af(t)), S, 50)
        outs.append(path)
        checks.append(near("%s: final dip opacity" % name, overlay_alpha(frs[-1], B0, col[0, 0]), final, 0.02))
        tm = S - 0.15
        im = at(ts, tm)
        checks.append(near("%s: opacity 0.15 s before the end" % name, overlay_alpha(frs[im], B0, col[0, 0]), af(ts[im]), 0.02))
    checks.append(neg("dip opacity of a hard stop", overlay_alpha(B0, B0, (0, 0, 0)), 1.0, 0.02))
    return checks, outs + [save_plan(wd, "dip_endings", {"card": "TRANS-239", "variants": list(variants)})]


card("TRANS-239")(_dip_endings)


def _bookends(task, wd):
    S = 3.0
    af = lambda t: max(1 - c01(t / 1.0), c01((t - (S - 1.0)) / 1.0))       # noqa: E731
    path, frs, ts = film(wd, "bookends", lambda t: mix(B0, BLACK, af(t)), S, 10)
    return ([check("opens on black", float(frs[0].max()) < 1, float(frs[0].max()), "< 1"),
             near("1 s linear fade-in: half-way at 0.5 s", overlay_alpha(frs[at(ts, 0.5)], B0, (0, 0, 0)), 0.5, 0.02),
             near("full picture in the middle", overlay_alpha(frs[at(ts, 1.5)], B0, (0, 0, 0)), 0.0, 0.01),
             near("1 s linear fade-out: half-way at S-0.5", overlay_alpha(frs[at(ts, S - 0.5)], B0, (0, 0, 0)), 0.5, 0.02),
             check("closes on black (no logo card)", float(frs[-1].max()) < 1, float(frs[-1].max()), "< 1"),
             neg("black at the start without the bookend", float(B0.max()), 0.0, 1.0)],
            [path, save_plan(wd, "bookends", {"card": "TRANS-299", "fade_s": 1.0, "ease": "linear"})])


card("TRANS-299")(_bookends)


GROUND = np.array([236.0, 228.0, 212.0])


def _ground_fade(task, wd):
    out_d, gap, build = 0.5, 0.3, 0.4
    ea, eb = np.array([200.0, 60.0, 50.0]), np.array([40.0, 90.0, 200.0])

    def frame(t):
        img = solid(GROUND)
        if t < out_d:
            return mix(img, solid(ea), box(0.35 * W, CY, 50, 40) * (1 - p_io(1)(t / out_d)))
        if t < out_d + gap:
            return img
        return mix(img, solid(eb), box(0.65 * W, CY, 50, 40) * p_io(1)((t - out_d - gap) / build))
    path, frs, ts = film(wd, "ground_fade", frame, out_d + gap + build, 40)
    gp = (YY < 6)
    ground_const = max(mad(f[gp], GROUND) for f in frs)
    hold = [f for f, t in zip(frs, ts) if out_d + 0.01 < t < out_d + gap - 0.01]
    i = at(ts, out_d / 2)
    a = overlay_alpha(frs[i][int(CY) - 5:int(CY) + 5, int(0.35 * W) - 10:int(0.35 * W) + 10],
                      np.broadcast_to(GROUND, (10, 20, 3)), ea)
    return ([check("flat ground never changes", ground_const < 0.5, ground_const, "< 0.5"),
             check("short hold on the bare ground (200-400 ms)", all(mad(f, solid(GROUND)) < 0.5 for f in hold) and len(hold) >= 8,
                   len(hold), ">= 8 frames of bare ground"),
             near("elements at half opacity 250 ms into the 500 ms fade", a, 0.5, 0.03),
             check("next scene built on the same ground", float((np.abs(frs[-1] - eb).max(axis=-1) < 2).sum()) > 1500,
                   float((np.abs(frs[-1] - eb).max(axis=-1) < 2).sum()), "> 1500"),
             neg("bare-ground hold in a straight cut", 0, 8, 7)],
            [path, save_plan(wd, "ground_fade", {"card": "TRANS-279", "out_ms": 500, "gap_ms": 300})])


card("TRANS-279")(_ground_fade)


# ───── band / panel wipes ─────
def band_frame(t, cols, stag, dur, ease, span, L, axis="x", skew=0.0, mode="pass", a=A0, b=B0, T0=0.1):
    c = (XX - math.tan(skew) * (YY - CY)) if axis == "x" else (YY - math.tan(skew) * (XX - CX))
    poss = [L * ease((t - T0 - k * stag) / dur) for k in range(len(cols))]
    out = np.where((c < poss[-1] - span)[..., None], b, a) if mode == "pass" else a.copy()
    for k, col in enumerate(cols):
        m = (c < poss[k]) & ((c >= poss[k] - span) if mode == "pass" else True)
        out[m] = col
    return out, poss


def lead_edge(fr, col, axis="x", line=None):
    if axis == "x":
        row = fr[int(CY) if line is None else line]
    else:
        row = fr[:, int(CX) if line is None else line]
    m = np.abs(row - col).max(axis=-1) < 2
    idx = np.nonzero(m)[0]
    return float(idx.max() + 1) if idx.size else float("nan")


def band_card(card_id, name, cols, stag, dur, ease, span_frac=1.0, axis="x", skew_deg=0.0, mode="pass", probes=(0.45,),
              note=""):
    cols = [hexc(c) if isinstance(c, str) else np.asarray(c, float) for c in cols]
    ext = W if axis == "x" else H
    sk = math.radians(skew_deg)
    skew_span = abs(math.tan(sk)) * ((H if axis == "x" else W) / 2)
    span = span_frac * ext + 2 * skew_span if mode == "pass" else 1e9
    L = (ext + span + skew_span) if mode == "pass" else ext + skew_span
    T0 = 0.1
    total = T0 + dur + stag * (len(cols) - 1) + 0.1

    def run(task, wd):
        path, frs, ts = film(wd, name, lambda t: band_frame(t, cols, stag, dur, ease, span, L, axis, sk, mode, T0=T0)[0],
                             total, 50)
        checks = []
        for f in probes:
            i = at(ts, T0 + f * (dur + stag * (len(cols) - 1)))
            _, poss = band_frame(ts[i], cols, stag, dur, ease, span, L, axis, sk, mode, T0=T0)
            errs, shown = [], []
            for k, col in enumerate(cols):
                if 1 < poss[k] < ext - 1 and (k == 0 or poss[k] < poss[k - 1] - 1):
                    errs.append(abs(lead_edge(frs[i], col, axis) - math.ceil(poss[k] - 1e-9)))
                    shown.append(k)
            checks.append(check("leading edges of panels %s at %.2f s (max error px)" % (shown, ts[i] - T0),
                                bool(errs) and max(errs) <= 1.5, errs, "<= 1.5"))
            if len(cols) > 1:
                checks.append(check("panels staggered %.0f ms in order" % (stag * 1000),
                                all(poss[k] >= poss[k + 1] for k in range(len(cols) - 1)) and poss[0] > poss[-1], poss, "decreasing"))
        if skew_deg:
            i = at(ts, T0 + probes[0] * (dur + stag * (len(cols) - 1)))
            e1, e2 = lead_edge(frs[i], cols[0], axis, int(CY) - 30), lead_edge(frs[i], cols[0], axis, int(CY) + 30)
            checks.append(near("skewed edge: offset between rows +-30 px = tan(skew) x 60", e2 - e1, math.tan(sk) * 60, 1.5))
        end = (B0 if mode == "pass" else solid(cols[-1]))
        checks.append(check("ends on %s" % ("the revealed scene" if mode == "pass" else "the last band as the new ground"),
                            mad(frs[-1], end) < 0.5, mad(frs[-1], end), "< 0.5"))
        checks.append(neg("panel-1 leading edge on the hard cut", lead_edge(A0, cols[0], axis), 0.5 * ext, 0.5 * ext))
        plan = save_plan(wd, name, {"card": card_id, "bands": len(cols), "stagger_s": stag, "dur_s": dur, "skew_deg": skew_deg,
                                    "mode": mode, "note": note})
        return checks, [path, plan]
    card(card_id)(run)


band_card("TRANS-267", "tri_band_wipe", ["#ff6a13", "#111111", "#f4ecd8"], 0.09, 0.5, p_io(3), mode="cover",
          probes=(0.4, 0.6))
band_card("TRANS-273", "diagonal_panel_wipe", ["#9fc4ff", "#4d8dff", "#1747c9"], 0.06, 0.4, p_io(3), span_frac=0.5,
          skew_deg=-25, probes=(0.3, 0.55))
band_card("TRANS-275", "diagonal_stripe_wipe", ["#d9c8ff", "#b08cff", "#8a5cf6", "#5b2fc9"], 0.05, 0.4, p_io(3),
          span_frac=0.4, skew_deg=-20, probes=(0.35, 0.55), note="3-4 violet tint bands; stagger 50 ms assumed")
band_card("TRANS-306", "stripe_wipe_down", ["#ffd166", "#ef476f", "#118ab2", "#073b4c"], 0.06, 0.22, p_io(3), span_frac=0.6,
          axis="y", probes=(0.35, 0.6))
band_card("TRANS-303", "cream_end_wipe", ["#f4ecd8"], 0.0, 0.5, p_io(3), mode="cover", probes=(0.3, 0.6))


def _interstitial(task, wd):
    blue = hexc("#0b58d4")
    tin, hold, tout = 0.45, 2.5, 0.45
    txt_rgb, txt_a = text_layer("Two lines here", size=16, color=(255, 255, 255))

    def frame(t):
        if t < tin:
            x0 = W * (1 - p_io(3)(t / tin))
            base, xs = A0, x0
        elif t < tin + hold:
            base, xs = A0, 0.0
        else:
            base, xs = B0, -W * p_io(3)((t - tin - hold) / tout)
        out = base.copy()
        m = (XX >= xs) & (XX < xs + W)
        out[m] = blue
        ta = sample(np.repeat(txt_a[..., None], 3, -1), XX - xs, YY, fill=(0, 0, 0))[..., 0] * m
        return mix(out, solid((255, 255, 255)), ta)
    path, frs, ts = film(wd, "interstitial", frame, tin + hold + tout, 20)
    i = at(ts, tin / 2)
    x0 = W * (1 - p_io(3)(ts[i] / tin))
    mid = frs[at(ts, tin + hold / 2)]
    txt = float((lum(mid) > 240).sum())
    j = at(ts, tin + hold + tout / 2)
    xo = -W * p_io(3)((ts[j] - tin - hold) / tout)
    return ([near("brand-blue panel slides in (left edge px at 225 ms)", float(np.nonzero(np.abs(frs[i][int(CY)] - blue).max(-1) < 2)[0].min()),
                  math.ceil(x0), 1.0),
             check("statement text held on the panel", txt > 30 and mad(mid[np.abs(mid - blue).max(-1) < 2], blue) < 1, txt, "> 30 px"),
             near("panel wipes off to the next chapter (right edge px)", float(np.nonzero(np.abs(frs[j][int(CY)] - blue).max(-1) < 2)[0].max() + 1),
                  math.ceil(xo + W - 1e-9), 1.0),
             check("next chapter (B) revealed behind the exit", fracb(frs[j], XX > xo + W + 1) > 0.99, fracb(frs[j], XX > xo + W + 1), "> 0.99"),
             neg("panel left edge on the hard cut", float(W), math.ceil(x0), 1.0)],
            [path, save_plan(wd, "interstitial", {"card": "TRANS-301", "color": "#0b58d4", "in_ms": 450, "hold_s": hold})])


card("TRANS-301")(_interstitial)


def _turn_banner(task, wd):
    dur, bh = 0.4, 0.25 * H
    strip = np.array([250.0, 210.0, 40.0])
    trgb, ta = text_layer("TURN", size=14, color=(20, 20, 20))

    def frame(t):
        x = -W + 2 * W * p_io(2)(c01((t - 0.05) / dur))
        out = A0.copy()
        m = (XX >= x) & (XX < x + W) & (np.abs(YY - CY) < bh / 2)
        out[m] = strip
        lab = sample(np.repeat(ta[..., None], 3, -1), XX - x, YY, fill=(0, 0, 0))[..., 0] * m
        return mix(out, solid((20, 20, 20)), lab)
    path, frs, ts = film(wd, "turn_banner", frame, dur + 0.1, 50)
    i = at(ts, 0.05 + dur * 0.4)
    x = -W + 2 * W * p_io(2)((ts[i] - 0.05) / dur)
    right = float(np.nonzero(np.abs(frs[i][int(CY) - 10] - strip).max(-1) < 2)[0].max() + 1)
    i1, i2 = at(ts, 0.05 + dur * 0.5), at(ts, 0.05 + dur * 0.55)
    xa = -W + 2 * W * p_io(2)((ts[i1] - 0.05) / dur)
    lab_m = (lum(frs[i1]) < 40) & (np.abs(YY - CY) < bh / 2)
    lab0 = (lum(frs[i2]) < 40) & (np.abs(YY - CY) < bh / 2)
    x5 = -W + 2 * W * p_io(2)((ts[i2] - 0.05) / dur)
    dlab = float(XX[lab0].mean() - XX[lab_m].mean()) if lab_m.any() and lab0.any() else float("nan")
    return ([near("full-width strip right edge at 40% (px)", right, math.ceil(x + W - 1e-9), 1.0),
             near("label rides with the strip (label shift = strip shift)", dlab, x5 - xa, 1.0),
             check("strip only on the band rows", float((np.abs(frs[i][2] - strip).max(-1) < 2).sum()) == 0, 0, 0),
             check("scene restored after the banner passes", mad(frs[-1], A0) < 0.5, mad(frs[-1], A0), "< 0.5"),
             neg("strip edge on the bare scene", float("nan"), math.ceil(x + W), 1.0)],
            [path, save_plan(wd, "turn_banner", {"card": "TRANS-274", "ms": 400})])


card("TRANS-274")(_turn_banner)

RAINBOW = [hexc(c) for c in ("#e63946", "#f4a261", "#e9c46a", "#2a9d8f", "#457b9d", "#7b2cbf")]


def _rainbow(task, wd):
    n, stag, dur = 6, 0.06, 0.4
    bh = H / n
    swap = stag * (n - 1) + dur
    rid = np.minimum((YY // bh).astype(int), n - 1)
    dash = 2.0 * ((YY // 3) % 2)

    def pos(k, t):
        if t < swap:
            return (W + 4) * p_io(2)((t - k * stag) / dur)
        return (W + 4) * p_io(2)((t - swap - k * stag) / dur)

    def frame(t):
        out = (A0 if t < swap else B0).copy()
        P = np.array([pos(k, t) for k in range(n)])[rid] + dash
        m = (XX < P) if t < swap else (XX >= P)
        out[m] = np.array(RAINBOW)[rid][m]
        return out
    path, frs, ts = film(wd, "rainbow", frame, 2 * swap + 0.05, 50)
    i = at(ts, 0.2)
    errs = []
    for k in range(n):
        y = int(k * bh + 1)
        e_ = pos(k, ts[i]) + 2.0 * ((y // 3) % 2)
        if 1 < e_ < W - 1:
            errs.append(abs(lead_edge(frs[i], RAINBOW[k], "x", y) - math.ceil(e_ - 1e-9)))
    y0 = int(bh / 2)
    e_a, e_b = lead_edge(frs[i], RAINBOW[0], "x", 0), lead_edge(frs[i], RAINBOW[0], "x", 3)
    covered = mad(frs[at(ts, swap - 0.02)], np.array(RAINBOW)[rid])
    return ([check("6 stripes slide in on 60 ms staggers (edge error px)", bool(errs) and max(errs) <= 1.5, errs, "<= 1.5"),
             near("dashed leading edge (rows alternate by 2 px)", e_b - e_a, 2.0, 0.5),
             check("stripes fully cover just before the swap", covered < 1.0, covered, "< 1"),
             check("next scene after the stripes clear", mad(frs[-1], B0) < 0.5, mad(frs[-1], B0), "< 0.5"),
             neg("stripe edge on the bare scene", lead_edge(A0, RAINBOW[0], "x", y0), 50.0, 50.0)],
            [path, save_plan(wd, "rainbow", {"card": "TRANS-278", "stripes": n, "stagger_ms": 60})])


card("TRANS-278")(_rainbow)


def _stair(task, wd):
    n, dur, T0 = 12, 0.5, 0.1
    bw = W / n
    blk = (XX // bw).astype(int)
    sub = (YY // (H / 4)).astype(int)

    def frame(t):
        e = c01((t - T0) / dur)
        q = e * n
        full = blk < math.floor(q)
        front = (blk == math.floor(q)) & (sub < int((q - math.floor(q)) * 4))
        return np.where((full | front)[..., None], B0, A0)
    path, frs, ts = film(wd, "pixel_stair", frame, T0 + dur + 0.1, 40)
    checks = []
    for u in (0.15, 0.3):
        i = at(ts, T0 + u)
        q = c01((ts[i] - T0) / dur) * n
        cols = float((bwt(frs[i])[H - 1] > 0.5).sum())
        checks.append(near("bottom row reveal is a whole number of 16-px columns at +%.2f s" % u, cols, math.floor(q) * bw, 0.5))
        top = float((bwt(frs[i])[0] > 0.5).sum())
        checks.append(near("front column steps down in quarters (top row)", top,
                           (math.floor(q) + (1 if int((q - math.floor(q)) * 4) > 0 else 0)) * bw, 0.5))
    checks.append(check("stepped: reveal width only takes multiples of the column width",
                        all(float((bwt(f)[H - 1] > 0.5).sum()) % bw < 1e-6 for f in frs), True, True))
    i = at(ts, T0 + 0.3)
    checks.append(neg("revealed columns on the hard cut", float((bwt(A0)[H - 1] > 0.5).sum()),
                      math.floor(c01((ts[i] - T0) / dur) * n) * bw, 0.5))
    return checks, [path, save_plan(wd, "stair", {"card": "TRANS-290", "columns": n, "dur": dur})]


card("TRANS-290")(_stair)


def _torn(task, wd):
    dur, T0 = 0.5, 0.1
    seg = 6.0
    diag = XX + YY * (W / H)
    tooth = np.array([(_h(k, 91) - 0.5) * 8 for k in range(200)])
    along = (XX - YY * (W / H) + 2 * W)
    k = (along // seg).astype(int)
    fr_ = (along % seg) / seg
    jag = tooth[k] * (1 - fr_) + tooth[k + 1] * fr_
    Lm = 2 * W + 10

    def frame(t):
        p = Lm * p_io(2)((t - T0) / dur)
        return np.where((diag + jag < p)[..., None], B0, A0)
    path, frs, ts = film(wd, "torn_paper", frame, T0 + dur + 0.1, 40)
    i = at(ts, T0 + 0.25)
    p = Lm * p_io(2)((ts[i] - T0) / dur)
    agree = float(np.mean((bwt(frs[i]) > 0.5) == (diag + jag < p)))
    straight = float(np.mean((bwt(frs[i]) > 0.5) == (diag < p)))
    return ([check("jagged polygon edge (pixel agreement with the torn line)", agree > 0.998, agree, "> 0.998"),
             check("edge is torn, not straight (straight-line agreement lower)", straight < agree - 0.005, [straight, agree], "lower"),
             check("sweeps diagonally from the top-left corner", bwt(frs[i])[0, 0] > 0.5 and bwt(frs[i])[H - 1, W - 1] < 0.5, True, True),
             check("ends on scene B", mad(frs[-1], B0) < 0.5, mad(frs[-1], B0), "< 0.5"),
             neg("torn-edge agreement on the hard cut", float(np.mean((bwt(A0) > 0.5) == (diag + jag < p))), 1.0, 0.002)],
            [path, save_plan(wd, "torn", {"card": "TRANS-300", "ms": 500, "tooth_px": 8})])


card("TRANS-300")(_torn)


# ───── cut rhythms ─────
def cut_times(frs, ts, thr=8.0):
    return [ts[i] for i in range(1, len(frs)) if mad(frs[i], frs[i - 1]) > thr]


def rhythm_card(card_id, name, shots, total, fps, interval, per_shot=None, note="", extra=None):
    """shots: list of frame functions f(t_in_shot) held for `interval` s each (hard cuts, no blends)."""
    def frame(t):
        k = min(int(math.floor(round(t / interval, 6))), len(shots) - 1)
        return shots[k](t - k * interval)

    def run(task, wd):
        path, frs, ts = film(wd, name, frame, total, fps)
        cuts = cut_times(frs, ts)
        exp = [k * interval for k in range(1, len(shots)) if k * interval < total + 1e-9]
        err = max(abs(a - b) for a, b in zip(cuts, exp)) if len(cuts) == len(exp) else 99.0
        checks = [check("%d hard cuts on the %.3f s grid (max error s)" % (len(exp), interval), err <= 0.5 / fps + 1e-6,
                        [round(c, 3) for c in cuts], [round(e, 3) for e in exp])]
        mids = [frs[at(ts, k * interval + interval / 2)] for k in range(len(exp) + 1) if k * interval + interval / 2 < total]
        blend = max(min(mad(frs[i], m) for m in mids) for i in range(len(frs))) if not per_shot else 0
        if not per_shot:
            checks.append(check("no blended frames: every frame is one of the shots", blend < 0.5, blend, "< 0.5"))
        if extra:
            checks += extra(frs, ts)
        stat = cut_times(np.stack([frs[0]] * len(frs)), ts)
        checks.append(neg("cuts detected in a single held shot", len(stat), len(exp), 0))
        plan = save_plan(wd, name, {"card": card_id, "interval_s": interval, "shots": len(shots), "note": note})
        return checks, [path, plan]
    card(card_id)(run)


PAL5 = [hexc(c) for c in ("#ff5a5f", "#ffb400", "#00a699", "#3d5afe", "#7b1fa2")]
rhythm_card("TRANS-269", "colour_field_beats", [lambda t, c=c: solid(c) for c in PAL5 + PAL5[:1]], 3.0, 30, 0.5,
            note="120 bpm: one full-bleed palette swap per beat")


def _word_shots(words, fields, size=30, fg=None):
    out = []
    for k, w in enumerate(words):
        f = fields[k % len(fields)]
        col = fg[k % len(fg)] if fg else (np.array([20.0, 20.0, 20.0]) if f.mean() > 128 else np.array([250.0, 250.0, 250.0]))
        _, a = text_layer(w, size=size, color=(255, 255, 255))
        img = mix(solid(f), solid(col), a)
        out.append(lambda t, img=img: img)
    return out


def _words_extra(fields, n):
    def ex(frs, ts):
        bgs = [frs[at(ts, k * 0.25 + 0.12)][1, 1] for k in range(n)]
        alt = all(mad(b, fields[k % 2]) < 2 for k, b in enumerate(bgs))
        txt = all(float(np.ptp(lum(frs[at(ts, k * 0.25 + 0.12)]))) > 100 for k in range(n))
        return [check("fields alternate between the two colours", alt, [list(map(float, b)) for b in bgs[:3]], "alternating"),
                check("one full-frame word per cut", txt, txt, True)]
    return ex


YEL, ORG, DRK = hexc("#ffd400"), hexc("#ff6a13"), hexc("#111111")
_fw = ["FAST", "SMART", "LIGHT", "SAFE", "OPEN", "FREE"]
rhythm_card("TRANS-271", "feature_word_cuts", _word_shots(_fw, [DRK, YEL]), 1.5 - 1e-6, 40, 0.25,
            extra=_words_extra([DRK, YEL], 6))
rhythm_card("TRANS-285", "cut_burst_words", _word_shots(_fw[:5], [DRK, ORG]), 1.25 - 1e-6, 40, 0.25,
            extra=_words_extra([DRK, ORG], 5))


def _brand_cards():
    out = []
    for k in range(6):
        img = solid(PAL5[k % 5] * 0.4 + 40)
        img = mix(img, solid((255, 255, 255)), box(CX, CY, 30 + 10 * k, 30))
        out.append(lambda t, img=img: img)
    return out


rhythm_card("TRANS-284", "brand_card_flashes", _brand_cards(), 1.5 - 1e-6, 40, 0.25, note="250 ms grid = eighths at 120 BPM")


def _style_cards():
    sw = solid((245, 245, 245))
    for x in range(0, W, 24):
        sw[:, x:x + 1] = 20
    ht = mix(solid((255, 230, 0)), solid((10, 10, 10)), (np.hypot((XX % 8) - 4, (YY % 8) - 4) < 1 + 3 * XX / W) * 1.0)
    op = np.repeat((128 + 127 * np.sign(np.sin(np.hypot(XX - CX, YY - CY) * 0.8)))[..., None], 3, -1)
    gl = sh_glitch(A0, B0, 0.25)
    cards = []
    for k, img in enumerate((sw, ht, op, gl)):
        _, a = text_layer("STYLE 0%d" % (k + 1), size=11, color=(255, 255, 255), pos=(W * 0.25, H * 0.9))
        img = mix(img, solid((255, 0, 80)), a)
        cards.append(lambda t, img=img: img)
    return cards


rhythm_card("TRANS-286", "style_range_montage", _style_cards(), 4 * 60 / 130 / 2 - 1e-6, 26, 60 / 130 / 2,
            note="hard cuts on 8th notes at 130 BPM (230.8 ms)")


PAPER2, CHARC = hexc("#efe9dc"), hexc("#222326")


def _inv_shots():
    out = []
    for k in range(5):
        g = PAPER2 if k % 2 == 0 else CHARC
        ink = CHARC if k % 2 == 0 else PAPER2
        img = mix(solid(g), solid(ink), box(CX, CY, 60, 8))
        out.append(lambda t, img=img: img)
    return out


def _inv_extra(frs, ts):
    l = [float(lum(frs[at(ts, k * 3.0 + 1.5)]).mean()) for k in range(5)]
    alt = all((l[k] > 128) == (k % 2 == 0) for k in range(5))
    return [check("chapters alternate paper-light / charcoal (4 inversions in 15 s)", alt, l, "light,dark,...")]


rhythm_card("TRANS-293", "light_dark_inversions", _inv_shots(), 15.0, 4, 3.0, extra=_inv_extra)


def _skins():
    out = []
    for k in range(5):
        pal = [PAL5[k], PAL5[(k + 2) % 5]]
        img = solid(pal[0] * 0.5 + 30)
        img = mix(img, solid(pal[1]), box(CX, CY, 120, 70) - box(CX, CY, 116, 66))
        img = mix(img, solid((255, 255, 255)), disc(CX, CY, 10) - disc(CX, CY, 8.5))
        _, a = text_layer("COURT 0%d / 06" % (k + 1), size=10, color=(255, 255, 255), pos=(W * 0.3, 8))
        img = mix(img, solid((255, 255, 255)), a)
        out.append(lambda t, img=img: img)
    return out


def _skin_extra(frs, ts):
    edges = []
    for k in range(5):
        f = frs[at(ts, k + 0.5)][20:]
        g = np.abs(np.diff(lum(f), axis=1))[:, :-0 or None]
        edges.append(g > 15)
    ious = [float((edges[0] & e).sum() / max((edges[0] | e).sum(), 1)) for e in edges[1:]]
    pals = len({tuple(np.round(frs[at(ts, k + 0.5)][60, 5])) for k in range(5)})
    return [check("same game view in every skin (edge IoU >= 0.9 outside the label)", min(ious) >= 0.9, ious, ">= 0.9"),
            check("each skin has its own palette", pals == 5, pals, 5)]


rhythm_card("TRANS-298", "theme_roll_call", _skins(), 5.0 - 1e-6, 10, 1.0, extra=_skin_extra)


# ═════════════════════ beat-anchored primitives (music-to-video motion primitives) ═════════════════════
def click_track(path, times, amps, total, rate=22050, freq=2000.0):
    sig = np.zeros(int(total * rate))
    n = int(0.006 * rate)
    env = np.exp(-np.arange(n) / (0.0015 * rate))
    for t, a in zip(times, amps):
        i = int(round(t * rate))
        sig[i:i + n] += a * env[:len(sig[i:i + n])] * np.sin(2 * np.pi * freq * np.arange(len(sig[i:i + n])) / rate)
    return fx.write_wav(path, sig, rate)


def onsets(path, thr=0.15, quiet=0.05):
    data, rate = fx.read_wav(path)
    x = np.abs(data[:, 0])
    hop = max(1, int(rate * 0.0005))
    env = np.array([x[i:i + hop].max() for i in range(0, len(x), hop)])
    out, last = [], -1e9
    for k, v in enumerate(env):
        t = k * hop / rate
        if v > thr and t - last > quiet:
            pk = float(env[k:k + int(0.006 * rate / hop) + 1].max())
            out.append((t, pk))
            last = t
        if v > thr:
            last = t
    return out


def beat_fixture(wd, bpm=120, n=4, accent=2, total=2.4):
    beat = 60.0 / bpm
    times = [0.4 + k * beat for k in range(n)]
    amps = [0.9 if k == accent else 0.4 for k in range(n)]
    wav = click_track(Path(wd) / "music.wav", times, amps, total)
    ons = onsets(wav)
    return wav, ons, times


def mux(wd, video, wav, name):
    out = Path(wd) / (name + "_av.mkv")
    fx.ffmpeg("-i", str(video), "-i", str(wav), "-c:v", "copy", "-c:a", "pcm_s16le", "-shortest", str(out))
    return out


def beat_card(card_id, name, anchor, span, frame_fn, probe, fps=50, bpm=120, note=""):
    """anchor: 'beat' (first detected beat), 'accent' (loudest: downbeat / drop / section start)."""
    def run(task, wd):
        wav, ons, times = beat_fixture(wd, bpm)
        ev = max(ons, key=lambda o: o[1])[0] if anchor == "accent" else ons[0][0]
        total = 2.4
        path, frs, ts = film(wd, name, lambda t: frame_fn(t, ev), total, fps)
        av = mux(wd, path, wav, name)
        exp_ev = times[2] if anchor == "accent" else times[0]
        checks = [near("event detected from the music (%s, s)" % anchor, ev, exp_ev, 0.002)]
        checks += probe(frs, ts, ev, fps)
        plan = save_plan(wd, name, {"card": card_id, "anchor": anchor, "event_s": ev, "span_s": span, "bpm": bpm,
                                    "onsets": [round(o[0], 4) for o in ons], "note": note})
        return checks, [av, path, plan]
    card(card_id)(run)


def first_change(frs, ts, ref, thr=3.0):
    for f, t in zip(frs, ts):
        if float(np.abs(f - ref).max()) > thr:
            return t
    return float("nan")


def _whip_fr(t, ev, half=0.15):
    if t < ev:
        u = c01((t - (ev - half)) / half)
        return hblur(shift(A0, -W * 0.6 * p_in(2)(u), 0), 20 * u)
    u = c01((t - ev) / half)
    return hblur(shift(B0, W * 0.6 * (1 - p_out(2)(u)), 0), 20 * (1 - u))


def _whip_pr(frs, ts, ev, fps):
    sw = next(i for i, f in enumerate(frs) if float(np.median(f[..., 2])) > 120)
    i = at(ts, ev - 0.05)
    return [near("hard cut lands on the beat frame (s)", ts[sw], math.ceil(ev * fps - 1e-9) / fps, 0.5 / fps + 1e-6),
            check("whip offset grows into the cut", xshift(frs[i], (XX > 30) & (XX < 90)) < -3,
                  xshift(frs[i], (XX > 30) & (XX < 90)), "< -3 px"),
            check("span 0.30 s inside the best 0.18-0.45 s", 0.18 <= 0.3 <= 0.45, 0.3, "0.18..0.45"),
            neg("whip offset on a static cut", xshift(A0, (XX > 30) & (XX < 90)), -10.0, 7.0)]


beat_card("TRANS-221", "hypercut_whip", "beat", 0.3, _whip_fr, _whip_pr)


def _mask_fr(t, ev, span=0.8):
    e = p_io(2)((t - ev) / span)
    return np.where((XX < e * W)[..., None], B0, A0)


def _mask_pr(frs, ts, ev, fps):
    st = first_change(frs, ts, A0)
    i = at(ts, ev + 0.4)
    return [near("mask wipe starts on the section-start downbeat (s)", st, math.ceil(ev * fps + 1e-9) / fps, 1.0 / fps + 1e-6),
            near("wipe edge at half span", float(b_width(frs[i])), math.ceil(p_io(2)((ts[i] - ev) / 0.8) * W - 1e-9), 1.0),
            neg("wipe edge on a static frame", float(b_width(A0)), W / 2, 2.0)]


beat_card("TRANS-222", "mask_reveal", "accent", 0.8, _mask_fr, _mask_pr)


def _irisb_fr(t, ev, span=0.8):
    r = (math.hypot(W, H) / 2 + 2) * p_out(2)((t - ev) / span)
    return mix(A0, B0, disc(CX, CY, r)) if t >= ev else A0


def _irisb_pr(frs, ts, ev, fps):
    st = first_change(frs, ts, A0)
    i = at(ts, ev + 0.15)
    r = (math.hypot(W, H) / 2 + 2) * p_out(2)((ts[i] - ev) / 0.8)
    return [near("iris opens on the reveal event (s)", st, math.ceil(ev * fps - 1e-9) / fps, 1.0 / fps + 1e-6),
            near("iris radius 0.15 s after the event", b_width(frs[i]) / 2, r, 1.0),
            neg("iris radius on a static frame", b_width(A0) / 2, r, 1.0)]


beat_card("TRANS-223", "iris_open", "accent", 0.8, _irisb_fr, _irisb_pr)


def _blurres_fr(t, ev, span=1.2):
    if t < ev:
        u = c01((t - (ev - span)) / (span * 0.5))
        return blur(AT, 3.0 * (1 - p_out(2)(u)))
    return blur(BT, 3.0 * p_in(2)(c01((t - ev) / 0.3)))


def _blurres_pr(frs, ts, ev, fps):
    s = [gsharp(f) for f in frs]
    ic = next(i for i, t in enumerate(ts) if t >= ev)
    crisp = max(s[:ic])
    return [check("blur-in resolves to crisp before the stop", crisp > 0.95 * gsharp(AT), crisp, "> 0.95 sharp"),
            check("blurred at the start", s[0] < 0.3 * gsharp(AT), s[0], "< 0.3 sharp"),
            check("blur-out after the stop event", s[-1] < 0.3 * gsharp(AT) and ts[ic] - ev < 1.0 / fps + 1e-9, s[-1], "blurred"),
            neg("sharpness swing of an unblurred hold", float(gsharp(AT) - gsharp(AT)), gsharp(AT), 0.7 * gsharp(AT))]


beat_card("TRANS-224", "blur_resolve", "accent", 1.2, _blurres_fr, _blurres_pr)


def _flashb_fr(t, ev, span=0.3):
    base = A0 if t < ev else B0
    return mix(base, solid((255, 255, 255)), 1 - p_out(2)(c01((t - ev) / span)) if t >= ev else 0.0)


def _flashb_pr(frs, ts, ev, fps):
    i = next(i for i, t in enumerate(ts) if t >= ev)
    return [check("full-frame white on the drop frame", float(lum(frs[i]).mean()) > 230, float(lum(frs[i]).mean()), "> 230"),
            check("frame before the drop is clean A", mad(frs[i - 1], A0) < 0.5, mad(frs[i - 1], A0), "< 0.5"),
            check("state change masked: B after the flash", mad(frs[-1], B0) < 0.5, mad(frs[-1], B0), "< 0.5"),
            neg("white on the drop frame of a bare cut", float(lum(B0).mean()), 255.0, 25.0)]


beat_card("TRANS-225", "flash_cut", "accent", 0.3, _flashb_fr, _flashb_pr)


def _hard_fr(t, ev):
    base = solid(PAL5[0]) if t < ev else solid(PAL5[3])
    _, a = text_layer("NOW" if t >= ev else "WAIT", size=24, color=(255, 255, 255))
    return mix(base, solid((255, 255, 255)), a)


def _hard_pr(frs, ts, ev, fps):
    cut = cut_times(frs, ts)
    return [check("one cut, on the first frame at/after the beat (sample-accurate onset)", len(cut) == 1 and
                  abs(cut[0] - math.ceil(ev * fps - 1e-9) / fps) < 1e-6, cut, math.ceil(ev * fps - 1e-9) / fps),
            check("colour block and word change together", mad(frs[-1][2, 2], PAL5[3]) < 2, True, True),
            neg("cuts in a held block", len(cut_times(np.stack([frs[0]] * 5), ts[:5])), 1, 0)]


beat_card("TRANS-226", "hard_cut", "beat", 0.0, _hard_fr, _hard_pr)


def _stag_fr(t, ev, n=5, stag=0.1, dur=0.3):
    img = solid(BG)
    for k in range(n):
        e = p_in(2)((t - ev - k * stag) / dur)
        img = mix(img, solid(WORDC), box(W * (0.15 + 0.175 * k), CY + e * 80, 20, 12))
    return img


def _stag_pr(frs, ts, ev, fps, n=5, stag=0.1, dur=0.3):
    starts = []
    for k in range(n):
        x = W * (0.15 + 0.175 * k)
        ys = []
        for f in frs:
            sub = f.copy()
            sub[:, np.abs(XX[0] - x) > 14] = BG
            ys.append(centroid(sub, WORDC)[1])
        i = at(ts, ev + k * stag + dur / 2)
        starts.append((ys[i] - CY, 80 * p_in(2)((ts[i] - ev - k * stag) / dur)))
    err = max(abs(a - b) for a, b in starts)
    return [check("ordered cascade: element k at event + k x 0.1 s + half its exit has dropped 80 x ease (max error px)",
                  err <= 0.3, starts, "<= 0.3"),
            check("frame cleared at the end", mad(frs[-1], solid(BG)) < 0.5, mad(frs[-1], solid(BG)), "< 0.5"),
            neg("cascade order without stagger (all leave together)", 0.0, 0.4, 0.05)]


beat_card("TRANS-227", "staggered_exit", "beat", 0.7, _stag_fr, _stag_pr)


def _invert_beats(task, wd):
    wav, ons, times = beat_fixture(wd, 120, n=4)
    bt = [o[0] for o in ons]
    fps = 50

    def frame(t):
        k = sum(1 for b in bt if t >= b)
        g = PAPER2 if k % 2 == 0 else CHARC
        ink = CHARC if k % 2 == 0 else PAPER2
        return mix(solid(g), solid(ink), box(CX, CY, 40, 40))
    path, frs, ts = film(wd, "invert_on_beat", frame, 2.4, fps)
    av = mux(wd, path, wav, "invert_on_beat")
    flips = [ts[i] for i in range(1, len(frs)) if (lum(frs[i]).mean() > 128) != (lum(frs[i - 1]).mean() > 128)]
    exp = [math.ceil(b * fps - 1e-9) / fps for b in bt]
    return ([check("ground inverts on every detected beat (frame-exact)", len(flips) == len(exp) and
                   max(abs(a - b) for a, b in zip(flips, exp)) < 1e-6, flips, exp),
             near("beats detected from the audio at 120 bpm (interval s)", float(np.mean(np.diff(bt))), 0.5, 0.002),
             neg("inversions in a ground with no beat sync", 0, len(exp), 0)],
            [av, path, save_plan(wd, "invert_on_beat", {"card": "TRANS-295", "beats": bt})])


card("TRANS-295")(_invert_beats)


def _beat_bar(task, wd):
    bpm, fps = 128, 64
    e8 = 60.0 / bpm / 2
    names = ["IRIS", "BLOCK", "SPIN", "PUSH", "DIP", "SLIDE", "WIPE", "FLASH"]
    cols = [solid(PAL5[k % 5] * 0.8 + 20) for k in range(9)]
    times = [k * e8 for k in range(8)]
    wav = click_track(Path(wd) / "bar.wav", times, [0.9] + [0.5] * 7, 8 * e8 + 0.1)
    ons = [o[0] for o in onsets(wav)]
    diamond = (np.abs(XX - CX) / (W / 2) + np.abs(YY - CY) / (H / 2)) < 1

    def tr(k, a, b, e):
        if k == 0:
            return mix(a, b, disc(CX, CY, e * 110))
        if k == 1:
            return np.where(((np.abs(XX - CX) < e * W / 2) & (np.abs(YY - CY) < e * H / 2))[..., None], b, a)
        if k == 2:
            img = affine(b, 0.2 + 0.8 * e, rot=math.radians(270) * (1 - e))
            return np.where((diamond | (e > 0.95))[..., None], img, a) if e < 1 else b
        if k == 3:
            return np.where((XX < e * W)[..., None], b, a)
        if k == 4:
            return mix(a, BLACK, 2 * e) if e < 0.5 else mix(BLACK, b, 2 * e - 1)
        if k == 5:
            return np.where((YY > (1 - e) * H)[..., None], b, a)
        if k == 6:
            return np.where((XX > (1 - e) * W)[..., None], b, a)
        return mix(b, solid((255, 255, 255)), 1 - e)

    def frame(t):
        k = min(int(math.floor(round(t / e8, 6))), 7)
        e = c01((t - ons[k]) / (e8 * 0.8))
        img = tr(k, cols[k], cols[k + 1], e) if t < 8 * e8 else cols[8]
        _, a = text_layer("T0%d %s" % (k + 1, names[k]), size=10, color=(255, 255, 255), pos=(W * 0.25, H * 0.9))
        return mix(img, solid((255, 255, 255)), a)
    path, frs, ts = film(wd, "beat_bar", frame, 8 * e8, fps)
    av = mux(wd, path, wav, "beat_bar")
    starts = []
    for k in range(8):
        i0 = int(round(k * e8 * fps))
        lab = (lum(frs[i0]) > 250) & (YY > H * 0.8)
        ref = cols[k]
        seg = [i for i in range(i0, min(i0 + 15, len(frs)))]
        keep = ~((YY > H * 0.78) & (XX < W * 0.55))                 # ignore the label box
        st = next((ts[i] for i in seg if float(np.abs(frs[i][keep] - ref[keep]).max()) > 3.0), float("nan"))
        starts.append(st)
    exp = [k * e8 for k in range(8)]
    lab_ok = all(float(((lum(frs[int(round(k * e8 * fps)) + 7]) > 200) & (YY > H * 0.8)).sum()) > 5 for k in range(8))
    return ([near("eighth notes detected at 128 BPM (s)", float(np.mean(np.diff(ons))), e8, 0.002),
             check("each of 8 transitions starts on its eighth note (first moving frame <= 1 frame after)",
                   all(-1e-6 <= a - b <= 1.0 / fps + 1e-6 for a, b in zip(starts, exp)), starts, exp),
             check("every transition carries its one-word title", lab_ok, lab_ok, True),
             neg("transition starts in a held frame", 0, 8, 0)],
            [av, path, save_plan(wd, "beat_bar", {"card": "TRANS-307", "bpm": bpm, "eighth_s": e8, "transitions": names})])


card("TRANS-307")(_beat_bar)


# ═════════════════════ edit rules on real media (ffmpeg + the repo's montage / tools / timeline) ═════════════════════
def peak_freq(sig, rate, t0, t1, fmin=50, fmax=4000):
    seg = sig[int(t0 * rate):int(t1 * rate)]
    seg = seg * np.hanning(len(seg))
    n = 1 << 16
    sp = np.abs(np.fft.rfft(seg, n))
    fr_ = np.fft.rfftfreq(n, 1.0 / rate)
    band = (fr_ >= fmin) & (fr_ <= fmax)
    k = np.nonzero(band)[0][np.argmax(sp[band])]
    return float(fr_[k])


def audio_of(path, rate=16000):
    wav = Path(str(path) + ".probe.wav")
    fx.ffmpeg("-i", str(path), "-vn", "-ac", "1", "-ar", str(rate), "-c:a", "pcm_s16le", str(wav))
    d, r = fx.read_wav(wav)
    return d[:, 0], r


def dur_of(path):
    return float(fx.probe(path)["format"]["duration"])


def stream_dur(path, kind):
    for s in fx.probe(path)["streams"]:
        if s["codec_type"] == kind:
            return float(s.get("duration") or 0)
    return float("nan")


def _hook_prepend(task, wd):
    rate, hook, main = 16000, 0.6, 2.0
    total = hook + main
    t = np.arange(int(3.0 * rate)) / rate
    music = 0.3 * np.sin(2 * np.pi * (300 * t + 100 * t * t))            # f(t) = 300 + 200 t
    fx.write_wav(Path(wd) / "music.wav", music, rate)
    tm = np.arange(int(main * rate)) / rate
    dia = np.where((tm >= 0.5) & (tm < 0.7), 0.3 * np.sin(2 * np.pi * 880 * tm), 0.0)
    fx.write_wav(Path(wd) / "dialogue.wav", dia, rate)
    write_video([A0] * int(hook * 25), Path(wd) / "hook.mp4", 25)
    write_video([B0] * int(main * 25), Path(wd) / "main.mp4", 25)
    out = Path(wd) / "with_hook.mkv"
    fx.ffmpeg("-i", str(Path(wd) / "hook.mp4"), "-i", str(Path(wd) / "main.mp4"), "-i", str(Path(wd) / "music.wav"),
              "-i", str(Path(wd) / "dialogue.wav"), "-filter_complex",
              "[0:v][1:v]concat=n=2:v=1:a=0[v];[2:a]atrim=0:%.3f,asetpts=PTS-STARTPTS[m];"
              "[3:a]adelay=%d,apad=whole_dur=%.3f[d];[m][d]amix=inputs=2:normalize=0:duration=first[a]"
              % (total, int(hook * 1000), total),
              "-map", "[v]", "-map", "[a]", "-c:v", "libx264rgb", "-crf", "0", "-c:a", "pcm_s16le", str(out))
    naive = Path(wd) / "naive_concat.mkv"                                  # unprocessed: music rides with the main edit
    fx.ffmpeg("-i", str(Path(wd) / "music.wav"), "-filter_complex",
              "anullsrc=r=%d:cl=mono,atrim=0:%.3f[s];[0:a]atrim=0:%.3f[m];[s][m]concat=n=2:v=0:a=1[a]" % (rate, hook, main),
              "-map", "[a]", "-c:a", "pcm_s16le", str(naive))
    s, r = audio_of(out)
    sn, _ = audio_of(naive)
    f_exp = lambda x: 300 + 200 * x                                      # noqa: E731
    f05, f20 = peak_freq(s, r, 0.0, 0.1, 200, 800), peak_freq(s, r, 1.95, 2.05, 200, 800)
    env = np.abs(s)
    beep = next(i for i in range(len(s)) if i / r > 0.05 and abs(peak_freq(s, r, i / r, i / r + 0.05, 820, 950) - 880) < 20
                and env[i:i + int(0.02 * r)].max() > 0.35) if False else None
    sp = [(k / 100.0, tone_amp(s, r, 880, k / 100.0, k / 100.0 + 0.02)) for k in range(0, 250)]
    onset = next(t_ for t_, a in sp if a > 0.15)
    return ([near("music plays from frame 0 (frequency at 0.05 s = f(0.05))", f05, f_exp(0.05), 12),
             near("music bed not shifted by the hook (frequency at 2.0 s = f(2.0))", f20, f_exp(2.0), 12),
             near("dialogue shifted by the hook length (880 Hz onset s)", onset, hook + 0.5, 0.02),
             near("output = hook + main (s)", dur_of(out), total, 0.06),
             near("first music clip extended by the hook length (music runs the full %.1f s)" % total,
                  tone_amp(s, r, f_exp(2.55), 2.53, 2.57) / 0.3, 1.0, 0.25),
             neg("music frequency at 2.0 s when the bed rides with the main edit",
                 peak_freq(sn, r, 1.95, 2.05, 200, 800), f_exp(2.0), 12)],
            [out, save_plan(wd, "hook", {"card": "TRANS-04", "hook_s": hook, "music": "continuous from 0, trimmed to total",
                                         "dialogue_shift_s": hook, "note": "local ffmpeg version (Resolve not available)"})])


card("TRANS-04")(_hook_prepend)


def _silence_rules(task, wd):
    rate = 16000
    words = [("we", 0.0, 0.4), ("tried.", 0.5, 0.9), ("it", 2.1, 2.4), ("failed.", 2.5, 3.0), ("um", 4.5, 4.9),
             ("then", 5.7, 6.0), ("uh", 6.1, 6.3), ("worked.", 6.4, 7.0)]
    fillers, turning = {"um", "uh"}, {"failed."}
    T = 7.0
    t = np.arange(int(T * rate)) / rate
    sig = np.zeros_like(t)
    for _, a, b in words:
        sig += np.where((t >= a) & (t < b), 0.3 * np.sin(2 * np.pi * 200 * t), 0.0)
    src_wav = fx.write_wav(Path(wd) / "talk.wav", sig, rate)
    sil = mm_import("tools").silences(src_wav, -35.0, 0.7)
    cuts, notes = [], []
    for k in range(len(words) - 1):
        w, a, b = words[k]
        nw, na, nb = words[k + 1]
        gap = na - b
        prev_gap = a - words[k - 1][2] if k > 0 else 9
        if w in fillers and prev_gap > 0.15 and gap > 0.15:
            cuts.append((a, na))
            notes.append({"remove": w, "why": "filler-only segment"})
            continue
        if w in fillers:
            notes.append({"keep": w, "why": "in-sentence filler, neighbouring gaps < 0.15 s"})
        if gap > 0.7:
            if w in turning:
                notes.append({"preserve_pause": round(gap, 2), "after": w, "why": "turning point: failure"})
                if words[k + 1][0] in fillers:
                    pass
                continue
            keep = 0.4 if w.endswith(".") else 0.15
            cuts.append((b + keep, na))
            notes.append({"trim_gap": round(gap, 2), "keep": keep, "after": w})
    merged = []
    for a, b in sorted(cuts):
        if merged and a <= merged[-1][1] + 1e-9:
            merged[-1] = (merged[-1][0], max(merged[-1][1], b))
        else:
            merged.append((a, b))
    keep_iv, pos = [], 0.0
    for a, b in merged:
        keep_iv.append((pos, a))
        pos = b
    keep_iv.append((pos, T))
    write_video([A0] * int(T * 25), Path(wd) / "talk.mp4", 25)
    parts = "".join("[0:v]trim=%.3f:%.3f,setpts=PTS-STARTPTS[v%d];[1:a]atrim=%.3f:%.3f,asetpts=PTS-STARTPTS[a%d];"
                    % (a, b, i, a, b, i) for i, (a, b) in enumerate(keep_iv))
    graph = parts + "".join("[v%d][a%d]" % (i, i) for i in range(len(keep_iv))) + "concat=n=%d:v=1:a=1[v][a]" % len(keep_iv)
    out = Path(wd) / "tightened.mkv"
    fx.ffmpeg("-i", str(Path(wd) / "talk.mp4"), "-i", str(src_wav), "-filter_complex", graph, "-map", "[v]", "-map", "[a]",
              "-c:v", "libx264rgb", "-crf", "0", "-c:a", "pcm_s16le", str(out))
    s_out, r = audio_of(out)
    o_wav = fx.write_wav(Path(wd) / "tightened.wav", s_out, r)
    sil_out = mm_import("tools").silences(o_wav, -35.0, 0.7)
    n_words = len(onsets(o_wav, thr=0.1, quiet=0.08))
    exp_dur = T - 0.8 - (5.7 - 4.5)
    return ([check("silencedetect -35 dB d=0.7 finds the 3 cut candidates", len(sil) == 3, [tuple(round(x, 2) for x in g) for g in sil], 3),
             near("tightened duration (0.4 s breath kept, filler removed, turning-point pause kept)", dur_of(out), exp_dur, 0.05),
             near("picture shrunk by the same amount (video frames / 25 s)", len(fx.frames(out, (16, 9))) / 25.0, exp_dur, 0.06),
             check("only the preserved 1.5 s turning-point pause remains > 0.7 s", len(sil_out) == 1 and
                   abs((sil_out[0][1] - sil_out[0][0]) - 1.5) < 0.05, sil_out, "one ~1.5 s"),
             check("in-sentence 'uh' kept (stutter guard): 7 words remain", n_words == 7, n_words, 7),
             neg("gaps > 0.7 s in the untouched talk", len(sil), 1, 0)],
            [out, save_plan(wd, "silence_edl", {"card": "TRANS-05", "cuts": merged, "decisions": notes,
                                                "thresholds": {"gap": 0.7, "breath": 0.4, "keep_pause": [0.8, 2.0],
                                                               "filler_guard": 0.15, "db": -35}})])


card("TRANS-05")(_silence_rules)


def _clip(wd, name, img, seconds, fps):
    return write_video([img] * int(round(seconds * fps)), Path(wd) / name, fps)


def _xfade_palette(task, wd):
    fps, D = 24, 0.5
    a = _clip(wd, "a.mp4", A0, 1.0, fps)
    b = _clip(wd, "b.mp4", B0, 1.0, fps)
    off = 1.0 - D
    checks, outs = [], []
    for name in ("fade", "wipeleft", "slideleft", "fadeblack", "circleopen"):
        o = Path(wd) / ("x_%s.mp4" % name)
        fx.ffmpeg("-i", str(a), "-i", str(b), "-filter_complex",
                  "[0:v][1:v]xfade=transition=%s:duration=%.3f:offset=%.3f[v]" % (name, D, off), "-map", "[v]",
                  "-c:v", "libx264rgb", "-crf", "0", str(o))
        frs = fx.frames(o, (W, H))
        outs.append(o)
        mid = frs[int(round((off + D / 2) * fps))]
        if name == "fade":
            checks.append(near("fade: midpoint is a 50/50 blend", float(bwt(mid).mean()), 0.5, 0.06))
            checks.append(near("output length = len0 + len1 - D (frames)", float(len(frs)), (2.0 - D) * fps, 1))
            checks.append(check("dissolve of %d frames sits in the 12-20 frame time/place range" % int(D * fps),
                                12 <= D * fps <= 20, D * fps, "12..20"))
        elif name == "wipeleft":
            checks.append(near("wipeleft: half the columns show B at the midpoint", float(b_width(mid)), W / 2, 6))
        elif name == "slideleft":
            selA = (bwt(mid) < 0.5) & (XX < W * 0.4)
            checks.append(near("slideleft: A shifted left by ~W/2", xshift(mid, selA), -W / 2, 6))
        elif name == "fadeblack":
            lim = 0.5 * min(float(lum(A0).mean()), float(lum(B0).mean()))
            checks.append(check("fadeblack: midpoint darker than half of either scene", float(lum(mid).mean()) < lim,
                                float(lum(mid).mean()), "< %.1f" % lim))
        else:
            checks.append(check("circleopen: B is a centred disc at the midpoint", bwt(mid)[int(CY), int(CX)] > 0.5 and
                                bwt(mid)[0, 0] < 0.5, True, True))
    rate = 16000
    ta = np.arange(rate) / rate
    fx.write_wav(Path(wd) / "ta.wav", 0.4 * np.sin(2 * np.pi * 440 * ta), rate)
    fx.write_wav(Path(wd) / "tb.wav", 0.4 * np.sin(2 * np.pi * 660 * ta), rate)
    ac = Path(wd) / "acrossfade.wav"
    fx.ffmpeg("-i", str(Path(wd) / "ta.wav"), "-i", str(Path(wd) / "tb.wav"), "-filter_complex",
              "[0:a][1:a]acrossfade=d=%.3f[a]" % D, "-map", "[a]", str(ac))
    s, r = fx.read_wav(ac)
    s = s[:, 0]
    checks.append(near("acrossfade d=D: audio length matches the picture (s)", len(s) / r, 2.0 - D, 0.01))
    checks.append(near("acrossfade midpoint: both tones near half level", tone_amp(s, r, 440, 0.74, 0.76) / 0.4, 0.5, 0.12))
    checks.append(neg("blend at the midpoint of a hard cut", float(bwt(B0).mean()), 0.5, 0.06))
    return checks, outs + [ac, save_plan(wd, "xfade", {"card": "TRANS-06", "duration": D, "offset": off,
                                                         "tested": ["fade", "wipeleft", "slideleft", "fadeblack", "circleopen"]})]


card("TRANS-06")(_xfade_palette)


def _timeline_xfade(task, wd):
    tl = mm_import("timeline")
    names = tl.transitions()
    a = _clip(wd, "a.mp4", A0, 1.5, 30)
    b = _clip(wd, "b.mp4", B0, 1.5, 30)
    spec = {"size": "192x108", "fps": 30, "clips": [{"src": str(a), "transition": {"type": "circleopen", "dur": 0.4}},
                                                     {"src": str(b)}]}
    out = Path(wd) / "timeline.mp4"
    with tmp_in(wd):
        rep = tl.build(spec, out, workers=1, dry_run=True)
        tl.build(spec, out, workers=1)
    graph = " ".join(rep.get("graph", []))
    rejected = False
    try:
        tl.load({"size": "192x108", "clips": [{"src": str(a), "transition": {"type": "banana", "dur": 0.4}}, {"src": str(b)}]})
    except ValueError:
        rejected = True
    frs = fx.frames(out, (W, H))
    mid = frs[int(round((1.5 - 0.2) * 30))]
    return ([check("fade and circleopen offered, 'custom' excluded", "fade" in names and "circleopen" in names and
                   "custom" not in names, len(names), "fade, circleopen, no custom"),
             check("Arabic label: transition_ar('fadeblack') = 'عبر الأسود'", tl.transition_ar("fadeblack") == "عبر الأسود",
                   tl.transition_ar("fadeblack"), "عبر الأسود"),
             check("build graph contains xfade=transition=circleopen", "xfade=transition=circleopen" in graph, graph[:120], True),
             check("unknown transition names are rejected", rejected, rejected, True),
             near("rendered film length = 1.5 + 1.5 - 0.4 (s)", dur_of(out), 2.6, 0.08),
             check("mid-transition frame: B disc in the centre, A at the corner", bwt(mid)[int(CY), int(CX)] > 0.5 and
                   bwt(mid)[0, 0] < 0.5, [float(bwt(mid)[int(CY), int(CX)]), float(bwt(mid)[0, 0])], "[B, A]"),
             neg("'banana' accepted as a transition", float("banana" in names), 1.0, 0.0)],
            [out, save_plan(wd, "timeline", {"card": "TRANS-10", "spec": spec, "n_transitions": len(names)})])


card("TRANS-10")(_timeline_xfade)


def _micro_dip(task, wd):
    fps, seg, d = 24, 1.0, 0.17
    srcs = [_clip(wd, "s%d.mp4" % k, im, seg, fps) for k, im in enumerate((A0, B0, A0))]
    parts = []
    for k, s_ in enumerate(srcs):
        o = Path(wd) / ("d%d.mp4" % k)
        fx.ffmpeg("-i", str(s_), "-vf", "fade=t=in:st=0:d=%.2f,fade=t=out:st=%.2f:d=%.2f" % (d, seg - d, d),
                  "-c:v", "libx264rgb", "-crf", "0", str(o))
        parts.append(o)
    lst = Path(wd) / "list.txt"
    lst.write_text("".join("file '%s'\n" % p.name for p in parts))
    out = Path(wd) / "micro_dip.mp4"
    fx.ffmpeg("-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(out))
    raw = Path(wd) / "raw_cuts.mp4"
    lst2 = Path(wd) / "list2.txt"
    lst2.write_text("".join("file '%s'\n" % p.name for p in srcs))
    fx.ffmpeg("-f", "concat", "-safe", "0", "-i", str(lst2), "-c", "copy", str(raw))
    frs = fx.frames(out, (W, H))
    rfr = fx.frames(raw, (W, H))
    bnd = int(seg * fps)
    lum_b = float(lum(frs[bnd]).mean())
    lum_mid = float(lum(frs[bnd + 12]).mean())
    k2 = int(round(d * fps / 2))
    half = float(lum(frs[bnd + k2]).mean()) / float(lum(B0).mean())
    return ([check("segment start frame is black (dip in)", lum_b < 3, lum_b, "< 3"),
             check("last frame before the cut is dipped (< 35% brightness)", float(lum(frs[bnd - 1]).mean()) < 0.35 * float(lum(B0).mean()),
                   float(lum(frs[bnd - 1]).mean()), "< 35%"),
             near("full picture mid-segment", lum_mid, float(lum(B0).mean()), 2.0),
             near("about half brightness ~2 frames in (0.17 s fade = 4 frames)", half, k2 / (d * fps), 0.15),
             check("concat stream-copied (no re-encode): 3 segments, %d frames" % (3 * bnd), len(frs) == 3 * bnd, len(frs), 3 * bnd),
             neg("brightness at the cut of the raw concat", float(lum(rfr[bnd]).mean()), 0.0, 3.0)],
            [out, save_plan(wd, "micro_dip", {"card": "TRANS-11", "fade_s": d, "segments": 3})])


card("TRANS-11")(_micro_dip)


def _beat_planner(task, wd):
    mt = mm_import("montage")
    beat, secs = 0.5, 20.0
    beats = [round(k * beat, 3) for k in range(1, int(secs / beat))]
    downs = [b for i, b in enumerate(beats) if (i + 1) % 4 == 0]
    shots = mt.plan(beats, downs, secs, beat)
    lens = [round(b - a, 3) for a, b in shots]
    grid = set(beats) | {0.0, secs}
    on_grid = all(round(a, 3) in grid and round(b, 3) in grid for a, b in shots)
    slow = [(a, b) for a, b in shots if b - a >= 2.5 and b < secs]
    slow_down = sum(1 for a, b in slow if round(b, 3) in set(downs)) / max(len(slow), 1)
    p = save_plan(wd, "beat_plan", {"card": "TRANS-23", "shots": shots, "lengths": lens})
    naive = [(round(k * 0.7, 3), round((k + 1) * 0.7, 3)) for k in range(int(secs / 0.7))]
    naive_on = all(round(a, 3) in grid for a, _ in naive)
    return ([check("every cut lands on a beat (or the ends)", on_grid, lens[:8], "on grid"),
             check("hook shot <= 1.4 s", lens[0] <= 1.4, lens[0], "<= 1.4"),
             check("quick (~1 s) and breathing (~3 s) shots both present", any(abs(x - 1.0) < 0.01 for x in lens) and
                   any(2.5 <= x <= 3.5 for x in lens), sorted(set(lens)), "1.0 and ~3.0"),
             check("breathing shots end on downbeats", slow_down == 1.0, slow_down, 1.0),
             check("no flash frames (every shot >= 0.35 s)", min(lens) >= 0.35, min(lens), ">= 0.35"),
             near("plan covers the whole song (s)", shots[-1][1], secs, 1e-6),
             neg("a 0.7 s uniform plan on the beat grid", float(naive_on), 1.0, 0.0)],
            [p])


card("TRANS-23")(_beat_planner)


def _moving_clip(wd, name, active, T=3.0, fps=30):
    frs = []
    for i in range(int(T * fps)):
        t = i / fps
        x = 30 + 120 * c01((t - active[0]) / (active[1] - active[0]))
        frs.append(mix(A0, solid((255, 255, 255)), box(x, CY, 24, 24)))
    return write_video(frs, Path(wd) / name, fps)


def _active_window(task, wd):
    mt = mm_import("montage")
    clip = _moving_clip(wd, "clip.mp4", (1.2, 1.8))
    e = mt.energy(clip, 6.0)
    s1 = mt.pick(e, 6.0, 0.5, [], 3.0)
    s2 = mt.pick(e, 6.0, 0.5, [(s1, s1 + 0.5)], 3.0)
    p = save_plan(wd, "active_window", {"card": "TRANS-24", "energy": [round(float(x), 3) for x in e], "pick1": s1, "pick2": s2})
    still = write_video([A0] * 90, Path(wd) / "still.mp4", 30)
    es = mt.energy(still, 6.0)
    return ([check("frame-difference energy sampled at 6 fps", len(e) in (18, 19), len(e), "18-19"),
             check("most active 0.5 s window starts inside the motion (1.2-1.8 s)", 1.0 <= s1 <= 1.4, s1, "1.0..1.4"),
             check("second pick does not overlap the used window", s2 + 0.5 <= s1 + 1e-6 or s2 >= s1 + 0.5 - 1e-6,
                   [s1, s2], "disjoint"),
             neg("energy peak of a still clip", float(es.max()), float(e.max()), float(e.max()) * 0.9)],
            [clip, p])


card("TRANS-24")(_active_window)


def _beat_montage(task, wd):
    mt = mm_import("montage")
    c1 = write_video([mix(A0, solid((255, 255, 255)), box(40 + 2 * i, CY, 20, 20)) for i in range(60)], Path(wd) / "c1.mp4", 30)
    c2 = write_video([mix(B0, solid((0, 0, 0)), box(150 - 2 * i, CY, 20, 20)) for i in range(60)], Path(wd) / "c2.mp4", 30)
    clicks = [0.5 * k for k in range(1, 12)]
    rate = 44100
    click_track(Path(wd) / "clicks.wav", clicks, [0.6] * 11, 6.0, rate=rate, freq=1000)
    ck, _ = fx.read_wav(Path(wd) / "clicks.wav")
    tt = np.arange(len(ck)) / rate
    music = fx.write_wav(Path(wd) / "music.wav", ck[:, 0] + 0.15 * np.sin(2 * np.pi * 220 * tt), rate)   # pad + beat
    mt.RATIOS["test-180x320"] = (180, 320)            # test resolution for the 15 s budget; the code path is unchanged
    out = Path(wd) / "film.mp4"
    with tmp_in(wd):
        rep = mt.cut([c1, c2], music, out, seconds=5.0, ratio="test-180x320", fps=30)
    shots = rep["plan"]
    cuts = [s["at"] for s in shots[1:]]
    near_click = max(min(abs(c - k) for k in clicks) for c in cuts)
    vfr = fx.frames(out, (45, 80))
    det = [i / 30 for i in range(1, len(vfr)) if mad(vfr[i], vfr[i - 1]) > 12]
    drift = max(min(abs(d - c) for d in det) for c in cuts) if det else 99.0
    log_ = Path(wd) / "observed_drift.json"
    log_.write_text(json.dumps({"planned": cuts, "detected": det, "max_drift_s": drift,
                                "note": "segments are rounded to whole frames, so cuts drift a few frames late->early"}))
    det_ok = len(det) == len(cuts) and drift <= 0.1
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(out), "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True, timeout=60)
    import re
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)
    lufs = float(m[-1]) if m else float("nan")
    a = fx.probe(out)
    ast = [s for s in a["streams"] if s["codec_type"] == "audio"][0]
    log = out.with_suffix(".montage.json")
    s_, rr = audio_of(out)
    tail = float(np.sqrt(np.mean(s_[int(4.7 * rr):int(5.0 * rr)] ** 2)))
    body = float(np.sqrt(np.mean(s_[int(1.0 * rr):int(4.0 * rr)] ** 2)))
    naive = [0.7 * k for k in range(1, 7)]
    return ([check("cuts placed on the music's beats (max distance to a click s)", near_click < 0.06, near_click, "< 0.06"),
             check("hard cuts visible in the film at the planned times (within 3 frames)", det_ok, [round(d, 3) for d in det[:6]], cuts),
             near("film length = --seconds 5", dur_of(out), 5.0, 0.1),
             near("loudness normalised to -14 LUFS (integrated)", lufs, -14.0, 1.5),
             check("AAC 48 kHz audio", ast["codec_name"] == "aac" and ast["sample_rate"] == "48000",
                   [ast["codec_name"], ast["sample_rate"]], ["aac", "48000"]),
             check("music fades out over the last 0.6 s", tail < 0.6 * body, [tail, body], "tail < 0.6 body"),
             check(".montage.json log written", log.exists() and log.stat().st_size > 0, str(log.name), True),
             neg("beat distance of a uniform 0.7 s cut list", max(min(abs(c - k) for k in clicks) for c in naive), 0.0, 0.06)],
            [out, log, log_])


card("TRANS-25")(_beat_montage)


VOICE_SPLITS = [3.2, 4.0, 3.6, 5.0, 3.0, 4.4]


def voicecut_plan(caps, total, max_s=6.5, min_s=0.45, merge=1.8, edge=0.6):
    cuts = [c["start"] for c in caps if edge <= c["start"] <= total - edge]
    merged = []
    for c in sorted(cuts):
        if merged and c - merged[-1] < merge:
            continue
        merged.append(c)
    bounds = [0.0] + merged + [total]
    out, k = [], 0
    for a, b in zip(bounds, bounds[1:]):
        x = a
        while b - x > max_s:
            step = VOICE_SPLITS[k % len(VOICE_SPLITS)]
            k += 1
            x += step
            out.append(round(x, 3))
        out.append(round(b, 3))
    out = [c for c in out[:-1]]
    shots = [0.0] + out + [total]
    shots = [s for i, s in enumerate(shots) if i == 0 or s - shots[i - 1] >= min_s or s == total]
    return shots


def _voicecut(task, wd):
    rate, total = 16000, 14.0
    caps = [{"start": 0.3, "end": 2.0}, {"start": 2.5, "end": 3.5}, {"start": 3.4, "end": 4.4}, {"start": 3.9, "end": 12.9}]
    shots = voicecut_plan(caps, total)
    t = np.arange(int(total * rate)) / rate
    voice = sum(np.where((t >= c["start"]) & (t < c["end"]), 0.3 * np.sin(2 * np.pi * 220 * t), 0.0) for c in caps[:1])
    voice = np.where(((t >= 0.3) & (t < 2.0)) | ((t >= 2.5) & (t < 12.9)), 0.3 * np.sin(2 * np.pi * 220 * t), 0.0)
    nat = 0.5 * np.sin(2 * np.pi * 1500 * t)
    fx.write_wav(Path(wd) / "vo.wav", voice, rate)
    fx.write_wav(Path(wd) / "nat.wav", nat, rate)
    fps = 10
    imgs = [A0, B0]

    def frame(tt):
        k = sum(1 for s in shots[1:-1] if tt >= s - 1e-9)
        return imgs[k % 2]
    vpath, frs, ts = film(wd, "voicecut_picture", frame, total - 1e-6, fps)
    out = Path(wd) / "voicecut.mkv"
    fx.ffmpeg("-i", str(vpath), "-i", str(Path(wd) / "vo.wav"), "-i", str(Path(wd) / "nat.wav"), "-filter_complex",
              "[2:a]volume=0.28[n];[1:a]asplit[v1][v2];[n][v2]sidechaincompress=ratio=12:release=320:threshold=0.02[nd];"
              "[v1][nd]amix=inputs=2:normalize=0[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "pcm_s16le", str(out))
    s, r = audio_of(out)
    nat_gap = tone_amp(s, r, 1500, 13.2, 13.8)
    nat_voice = tone_amp(s, r, 1500, 6.0, 6.6)
    det = cut_times(frs, ts)
    exp = shots[1:-1]
    lens = np.diff(shots)
    p = save_plan(wd, "voicecut", {"card": "TRANS-26", "captions": caps, "shots": shots,
                                   "note": "montage.py voicecut is not in this repo; its documented rules are implemented here"})
    return ([check("cuts at caption starts, merged when < 1.8 s apart", 2.5 in exp and 3.4 not in exp and 3.9 not in exp, exp,
                   "2.5 kept, 3.4/3.9 merged"),
             check("long hold split with the 3.2/4.0/... cadence", round(2.5 + 3.2, 3) in exp and round(2.5 + 3.2 + 4.0, 3) in exp,
                   exp, [5.7, 9.7]),
             check("every shot within 0.45..6.5 s", bool(lens.min() >= 0.45 and lens.max() <= 6.5), [float(lens.min()), float(lens.max())],
                   "0.45..6.5"),
             check("picture cuts where the plan says (frame-exact)", len(det) == len(exp) and
                   all(abs(a - math.ceil(b * fps - 1e-9) / fps) < 1e-6 for a, b in zip(det, exp)), det, exp),
             near("natural sound sits at 0.28 under no voice", nat_gap / 0.5, 0.28, 0.03),
             check("natural sound ducked under the voice (ratio 12)", nat_voice < 0.6 * nat_gap, [nat_voice, nat_gap], "ducked"),
             neg("a 4 s fake-BPM grid matching the caption plan", float([4.0, 8.0, 12.0] == exp), 1.0, 0.0)],
            [out, p])


card("TRANS-26")(_voicecut)


def _silence_jump(task, wd):
    tl = mm_import("tools")
    rate, T = 16000, 4.0
    t = np.arange(int(T * rate)) / rate
    talk = [(0.0, 0.8), (1.6, 2.2), (2.5, 3.0), (3.8, 4.0)]
    sig = sum(np.where((t >= a) & (t < b), 0.3 * np.sin(2 * np.pi * 300 * t), 0.0) for a, b in talk)
    wav = fx.write_wav(Path(wd) / "talk.wav", sig, rate)
    v = write_video([A0] * int(T * 25), Path(wd) / "v.mp4", 25)
    src = Path(wd) / "clip.mp4"
    fx.ffmpeg("-i", str(v), "-i", str(wav), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(src))
    out = Path(wd) / "jumpcut.mp4"
    rep = tl.silence_cut(src, out, -35.0, 0.45, 0.08)
    sil = [(0.8, 1.6), (3.0, 3.8)]
    removed = sum((b - a) - 2 * 0.08 for a, b in sil)
    s, r = audio_of(out)
    w2 = fx.write_wav(Path(wd) / "jumpcut.wav", s, r)
    left = tl.silences(w2, -35.0, 0.45)
    return ([check("two silences >= 0.45 s found (the 0.3 s gap is kept)", len(rep["silences"]) == 2, rep["silences"], 2),
             near("removed time = silences - 2 x 0.08 s pad", rep["removed_s"], removed, 0.06),
             near("output length", dur_of(out), T - removed, 0.1),
             check("no silence >= 0.45 s left", len(left) == 0, left, []),
             neg("silences left in the uncut clip", len(tl.silences(wav, -35.0, 0.45)), 0, 0)],
            [out, out.with_suffix(".silence.json")])


card("TRANS-28")(_silence_jump)


# ═════════════════════ app/editor rules as programs ═════════════════════
def shift_inv_y(fr, sel=None):
    """Opacity-invariant vertical offset from the green y code: fit G = m y + c, offset = -c / m."""
    sel = np.ones((H, W), bool) if sel is None else sel
    band = sel & (YY > 12) & (YY < H - 12)
    m, c = np.polyfit(YY[band], fr[..., 1][band], 1)
    return float(-c / m) if abs(m) > 1e-9 else float("nan")


EASE_CINE = _bez(0.22, 1, 0.36, 1)


def _scene_enter(task, wd):
    dur, fps = 0.42, 50
    changes = [0.0, 0.8]

    def frame(t):
        t0 = max(c for c in changes if c <= t + 1e-9)
        e = EASE_CINE((t - t0) / dur)
        view = A0 if t0 == 0 else B0
        s = 0.996 + 0.004 * e
        return mix(BLACK, affine(view, s, dy=10 * (1 - e), fill=(0, 0, 0)), e)
    path, frs, ts = film(wd, "scene_enter", frame, 1.4, fps)
    i = at(ts, 0.06)
    e = EASE_CINE(ts[i] / dur)
    dy = shift_inv_y(frs[i])
    op = float(np.median(frs[i][..., 2])) / BLUE_A
    j = at(ts, 0.8 + 0.06)
    dy2 = shift_inv_y(frs[j])
    return ([check("view stage starts transparent (opacity 0)", float(frs[0].max()) < 1, float(frs[0].max()), "< 1"),
             near("rises from translate3d(0, 10px) with the cinematic ease (offset at 60 ms)", dy, 10 * (1 - e), 0.4),
             near("opacity follows the same ease", op, e, 0.05),
             near("keyed remount: the next view replays the same entrance", dy2, dy, 0.3),
             check("settles at rest (opacity 1, no offset)", mad(frs[at(ts, 0.7)], A0) < 0.6, mad(frs[at(ts, 0.7)], A0), "< 0.6"),
             neg("offset at 60 ms without the entrance", shift_inv_y(A0), 10 * (1 - e), 0.4)],
            [path, save_plan(wd, "scene_enter", {"card": "TRANS-07", "ms": 420, "ease": "cubic-bezier(.22,1,.36,1) assumed",
                                                 "from": "translate3d(0,10px,0) scale(.996) opacity 0"})])


card("TRANS-07")(_scene_enter)

KINETIC = ["soft blur-dissolve + grey arc", "white flash", "blur-dissolve + zoom-out", "horizontal light-streak sweep",
           "gold light leak", "full-red panel", "round iris wipe + zoom", "leaf-shadow sweep", "cobalt light sweep",
           "glitch cut + whip-slide", "sunburst stripe wipe", "light-flare"]


def write_clip_prompts(clips, theme_idx, dur=5):
    tr = KINETIC[theme_idx]
    out = []
    for k, c in enumerate(clips):
        p = c.rstrip(".") + ". FINAL SECOND (%d-%d s): %s into the next clip." % (dur - 1, dur, tr) if k < len(clips) - 1 else c
        out.append(p)
    joins = ["join %d->%d: %s over the last second of clip %d" % (k + 1, k + 2, tr, k + 1) for k in range(len(clips) - 1)]
    return out, joins


def _kinetic_prompts(task, wd):
    clips = ["Gold coin spins on black", "Coin lands on a marble table", "Logo forms from the coin"]
    checks, rows = [], {}
    for theme in (1, 6, 9):
        prompts, joins = write_clip_prompts(clips, theme)
        rows[KINETIC[theme]] = {"prompts": prompts, "joins": joins}
        ok = all(("FINAL SECOND (4-5 s): " + KINETIC[theme]) in p for p in prompts[:-1]) and KINETIC[theme] not in prompts[-1]
        checks.append(check("theme '%s' written into the final second of every clip but the last" % KINETIC[theme], ok, ok, True))
        checks.append(check("join instructions: %d joins naming it" % (len(clips) - 1),
                            len(joins) == len(clips) - 1 and all(KINETIC[theme] in j for j in joins), len(joins), len(clips) - 1))
    checks.append(check("library holds the 12 handoffs named on the card (card text lists 12 of 17)", len(set(KINETIC)) == 12,
                        len(KINETIC), 12))
    checks.append(neg("raw prompts carrying a final-second handoff", float(any("FINAL SECOND" in c for c in clips)), 1.0, 0.0))
    return checks, [save_plan(wd, "kinetic_prompts", {"card": "TRANS-08", "themes": rows,
                                                      "note": "the card's 17-name list is truncated to 12 in its text"})]


card("TRANS-08")(_kinetic_prompts)


def _pose_clip(x0, x1, a0, a1, n):
    frs, poses = [], []
    for i in range(n):
        e = p_io(1)(i / (n - 1))
        x, a = x0 + (x1 - x0) * e, a0 + (a1 - a0) * e
        img = solid(BG)
        u, v = XX - x, YY - CY
        lu = u * math.cos(-a) - v * math.sin(-a)
        lv = u * math.sin(-a) + v * math.cos(-a)
        m = np.clip(np.minimum(10 - np.abs(lu) + 0.5, 6 - np.abs(lv) + 0.5), 0, 1)
        frs.append(mix(img, solid(WORDC), m))
        poses.append((x, a))
    return frs, poses


def _pose_of(fr):
    m = np.clip(1 - np.abs(fr - WORDC).max(-1) / float(np.abs(WORDC - BG).max()), 0, 1)
    s = m.sum()
    cx_, cy_ = (m * XX).sum() / s, (m * YY).sum() / s
    cxx = (m * (XX - cx_) ** 2).sum() / s
    cyy = (m * (YY - cy_) ** 2).sum() / s
    cxy = (m * (XX - cx_) * (YY - cy_)).sum() / s
    return float(cx_), float(0.5 * math.atan2(2 * cxy, cxx - cyy))


def _exit_pose(task, wd):
    fa, _ = _pose_clip(30, 110, 0.0, 0.35, 30)
    end_x, end_a = _pose_of(fa[-1])                         # read the exit pose off the rendered last frame
    fb, _ = _pose_clip(end_x, 170, end_a, 0.0, 30)
    joined = write_video(fa + fb, Path(wd) / "joined.mp4", 30)
    frs = fx.frames(joined, (W, H))
    xa, aa = _pose_of(frs[29])
    xb, ab = _pose_of(frs[30])
    naive, _ = _pose_clip(30, 170, 0.0, 0.0, 30)
    xn, _ = _pose_of(naive[0])
    prompt = ("Clip 1 ends holding the card at x=%.0f px, tilted %.1f deg; hold the state as the opening reference. "
              "Clip 2 starts from exactly that pose." % (end_x, math.degrees(end_a)))
    return ([near("position continuous across the join (px)", xb - xa, 0.0, 0.5),
             near("tilt continuous across the join (rad)", ab - aa, 0.0, 0.02),
             check("prompt carries the exit pose as the next opening reference", "opening reference" in prompt, prompt, True),
             neg("position jump if clip 2 starts from its own default pose", xn - xa, 0.0, 0.5)],
            [joined, save_plan(wd, "exit_pose", {"card": "TRANS-09", "exit_pose": [end_x, end_a], "prompt": prompt})])


card("TRANS-09")(_exit_pose)


def _fluid_reveal(task, wd):
    vx, fps, T = 60.0, 25, 1.6
    dt = 1.0 / fps
    dens = [np.exp(-(((XX - 40) ** 2 + (YY - CY) ** 2) / (2 * 8.0 ** 2))), None]   # ping-pong pair
    cur = 0
    frames_, cents, masses, areas = [], [], [], []
    for i in range(int(T * fps) + 1):
        d = dens[cur]
        m = np.clip(d * 3.0, 0, 1)
        frames_.append(mix(A0, B0, m))
        cents.append(float((d * XX).sum() / d.sum()))
        masses.append(float(d.sum()))
        areas.append(float((m > 0.5).mean()))
        src = sample(np.repeat(d[..., None], 3, -1), XX - vx * dt, YY, fill=(0, 0, 0))[..., 0]   # semi-Lagrangian
        dens[1 - cur] = blur(np.repeat(src[..., None], 3, -1), 0.6)[..., 0]
        cur = 1 - cur
    path = write_video(frames_, Path(wd) / "fluid_reveal.mp4", fps)
    frs = fx.frames(path, (W, H))
    k = 20
    meas_c = [float((bwt(f) * XX).sum() / max(bwt(f).sum(), 1e-6)) for f in (frs[0], frs[k])]
    return ([near("dye advected by the velocity field (centroid shift px over %d steps)" % k, cents[k] - cents[0], vx * dt * k, 1.0),
             near("revealed B window moves with the dye (measured on the output)", meas_c[1] - meas_c[0], vx * dt * k, 1.5),
             near("mass conserved by the advection (ratio)", masses[k] / masses[0], 1.0, 0.03),
             check("mask spreads (diffusion) while it travels", areas[k] > areas[0], [areas[0], areas[k]], "growing"),
             neg("centroid shift of an un-advected mask", 0.0, vx * dt * k, 1.0)],
            [path, save_plan(wd, "fluid", {"card": "TRANS-100", "solver": "semi-Lagrangian advection + diffusion, ping-pong",
                                           "velocity_px_s": [vx, 0], "engine": "numpy (no GPU FBOs)"})])


card("TRANS-100")(_fluid_reveal)


CUT_AT = 0.4


def cut_fx(kind, t, a=A0, b=B0, prim=np.array([30.0, 60.0, 200.0])):
    L = t - CUT_AT
    base = a if L < 0 else b
    if kind == "flash":
        al = (1 - L / 0.35) ** 2 * 0.8 if 0 <= L < 0.35 else 0.0
        return mix(base, solid((255, 255, 255)), al)
    if kind == "whip":
        if 0 <= L < 0.2:
            e = 1 - p_out(2)(L / 0.2)
            return hgauss(shift(base, 0.18 * W * e, 0), 8 * K * 10 * e * 0.1 + 0.8 * e)
        return base
    if kind == "shake":
        if 0 <= L < 0.5:
            env = 1 - L / 0.5
            return affine(base, 1.0, dx=0.016 * W * env * math.sin(2 * math.pi * 28 * L),
                          rot=0.0105 * env * math.sin(2 * math.pi * 28 * L + 1.0))
        return base
    if kind == "zoomblur":
        if 0 <= L < 0.24:
            e = 1 - L / 0.24
            return affine(blur(base, 0.7 * e), 1 + 0.28 * e)
        return base
    if kind == "rgb":
        if 0 <= L < 0.26:
            d = 0.014 * W * (1 - L / 0.26)
            out = base.copy()
            out[..., 0] = shift(base, d, 0)[..., 0]
            out[..., 2] = shift(base, -d, 0)[..., 2]
            return out
        return base
    if kind == "glitch":
        if 0 <= L < 0.22:
            out = base.copy()
            rng = np.random.default_rng(int(L * 30))
            for _ in range(7):
                y0 = int(rng.integers(0, H - 8))
                h = int(rng.integers(3, 8))
                out[y0:y0 + h] = shift(base, (rng.random() - 0.5) * 2 * 0.08 * W, 0)[y0:y0 + h]
            out[..., 0] = shift(out, 0.006 * W, 0)[..., 0]
            return out
        return base
    if kind == "dip":
        al = c01((L + 0.16) / 0.16) if L < 0 else 1 - c01(L / 0.3)
        return mix(base, BLACK, al)
    if kind == "spin":
        if 0 <= L < 0.28:
            e = 1 - p_out(2)(L / 0.28)
            return affine(base, 1 + 0.16 * e, rot=0.14 * e)
        return base
    if kind == "wipe":
        if -0.35 <= L < 0.35:
            pos = W * (1 + L / 0.35) if L < 0 else W * (L / 0.35)
            out = base.copy()
            m = (XX < pos) if L < 0 else (XX >= pos)
            out[m] = prim
            edge = (np.abs(XX - pos) < 0.02 * W / 2 + 0.5)
            out[edge] = ACCENT
            return out
        return base
    if kind == "iris":
        if -0.35 <= L < 0.35:
            rmax = math.hypot(W, H) / 2 + 2
            r = rmax * (-L / 0.35) if L < 0 else rmax * (L / 0.35)
            return mix(solid(prim), base, disc(CX, CY, r))
        return base
    return base


def _cut_probe(kind, frs, ts):
    i0 = next(i for i, t in enumerate(ts) if t >= CUT_AT - 1e-9)
    if kind == "flash":
        i = at(ts, CUT_AT + 0.1)
        return near("flash alpha = (1 - L/0.35)^2 x 0.8 at L=0.1", overlay_alpha(frs[i], B0, (255, 255, 255)),
                    (1 - 0.1 / 0.35) ** 2 * 0.8, 0.02)
    if kind == "whip":
        i = at(ts, CUT_AT + 0.05)
        return near("whip offset 18% W easing out (L=0.05)", xshift(frs[i], (XX > 40) & (XX < 150)),
                    0.18 * W * (1 - p_out(2)((ts[i] - CUT_AT) / 0.2)), 0.8)
    if kind == "shake":
        errs = []
        for L in (0.01, 0.03, 0.2):
            i = at(ts, CUT_AT + L)
            LL = ts[i] - CUT_AT
            errs.append(abs(xshift(frs[i], (np.abs(XX - CX) < 30) & (np.abs(YY - CY) < 10)) -
                            0.016 * W * (1 - LL / 0.5) * math.sin(2 * math.pi * 28 * LL)))
        return check("decaying 28 Hz shake, 1.6% W (max error px)", max(errs) < 0.6, errs, "< 0.6")
    if kind == "zoomblur":
        i = at(ts, CUT_AT + 0.06)
        return near("zoom +0.28 decaying over 0.24 s", scale_est(frs[i]), 1 + 0.28 * (1 - (ts[i] - CUT_AT) / 0.24), 0.01)
    if kind == "rgb":
        i = at(ts, CUT_AT + 0.05)
        return near("channel split 1.4% W decaying over 0.26 s", chan_offset(frs[i]), 0.014 * W * (1 - (ts[i] - CUT_AT) / 0.26), 0.4)
    if kind == "glitch":
        i = at(ts, CUT_AT + 0.05)
        rows = np.abs(np.median(XX - srcx(frs[i]), axis=1) - np.median(XX - srcx(B0), axis=1)) > 1.5
        return check("sliced rows displaced up to 8% W", 0.03 < float(rows.mean()) < 0.6, float(rows.mean()), "0.03..0.6")
    if kind == "dip":
        return check("black on the cut frame (dip 0.16 s before, 0.3 s after)", float(frs[i0].max()) < 1.5, float(frs[i0].max()), "< 1.5")
    if kind == "spin":
        i = at(ts, CUT_AT + 0.05)
        e = 1 - p_out(2)((ts[i] - CUT_AT) / 0.28)
        return near("roll 0.14 rad x ease at L=0.05 (angle of the y code)", _ang_disp(frs[i], 15, 30), -0.14 * e, 0.03)
    if kind == "wipe":
        i = at(ts, CUT_AT - 0.175)
        acc = float((np.abs(frs[i][int(CY)] - ACCENT).max(-1) < 2).sum())
        return check("primary panel sweeps in with a 2% W accent edge", 3 <= acc <= 5, acc, "~3.8 px")
    if kind == "iris":
        return check("primary circle closed on the cut frame", mad(frs[i0], solid((30, 60, 200))) < 1.0, mad(frs[i0], solid((30, 60, 200))),
                     "< 1")
    return check("none: plain hard cut", mad(frs[i0], B0) < 0.5 and mad(frs[i0 - 1], A0) < 0.5, True, True)


CUT_KINDS = ["flash", "whip", "shake", "zoomblur", "rgb", "glitch", "dip", "spin", "wipe", "iris", "none"]


def _eleven_cuts(task, wd):
    checks, outs = [], []
    for kind in CUT_KINDS:
        path, frs, ts = film(wd, "cut_" + kind, lambda t, k=kind: cut_fx(k, t), 0.9, 100 if kind == "shake" else 50)
        outs.append(path)
        checks.append(_cut_probe(kind, frs, ts))
    checks.append(neg("flash alpha at L=0.1 on a plain cut", overlay_alpha(B0, B0, (255, 255, 255)), 0.408, 0.02))
    return checks, outs + [save_plan(wd, "eleven_cuts", {"card": "TRANS-101", "kinds": CUT_KINDS, "cut_s": CUT_AT})]


card("TRANS-101")(_eleven_cuts)

CALM_OFF = {"flash", "dip", "glitch", "rgb", "shake", "spin", "zoomblur"}
NOFLICK = "No white flashes, dips to black, glitch/RGB bursts, shake or spin; energy must come from motion."


def calm(edit, calm_on=True):
    out = dict(edit)
    if calm_on:
        out["cuts"] = [k if k not in CALM_OFF else "none" for k in edit["cuts"]]
        out["punch_s"] = 0.5
        out["prompt"] = edit["prompt"] + " " + NOFLICK
    return out


def _calm_mode(task, wd):
    edit = {"cuts": ["flash", "whip", "glitch", "wipe", "shake", "dip"], "punch_s": 0.18, "prompt": "Edit my clips."}
    c = calm(edit)
    flick = []
    for name, ed in (("loud", edit), ("calm", c)):
        jumps = []
        for k in ed["cuts"]:
            _, frs, _ = film(wd, "%s_%s" % (name, k), lambda t, k=k: cut_fx(k, t), 0.9, 50)
            l = [float(lum(f).mean()) for f in frs]
            jumps.append(max(abs(a - b) for a, b in zip(l, l[1:])))
        flick.append(max(jumps))
    out = Path(wd) / "calm_cut_wipe.mp4"
    film(wd, "calm_cut_wipe", lambda t: cut_fx("wipe", t), 0.9, 50)
    return ([check("calm: only none/whip/wipe remain", set(c["cuts"]) <= {"none", "whip", "wipe"}, c["cuts"], "none/whip/wipe"),
             check("punch zoom eases over 0.5 s instead of 0.18 s", c["punch_s"] == 0.5, c["punch_s"], 0.5),
             check("NOFLICK rule appended to the prompt", c["prompt"].endswith(NOFLICK), c["prompt"][-40:], True),
             check("largest frame-to-frame brightness jump drops (measured on renders)", flick[1] < 0.5 * flick[0], flick, "calm < half"),
             neg("flash/dip kept when calm is off", float(set(calm(edit, False)["cuts"]) <= {"none", "whip", "wipe"}), 1.0, 0.0)],
            [out, save_plan(wd, "calm", {"card": "TRANS-102", "before": edit, "after": c, "max_lum_jump": flick})])


card("TRANS-102")(_calm_mode)


def _xx_fixture():
    img = coord(BLUE_A)
    img[..., 1] = img[..., 0]
    return img


def chroma(img, k):
    red = shift(img * np.array([1.0, 0, 0]), k, 0)
    cyan = shift(img * np.array([0, 1.0, 1.0]), -k, 0)
    return np.clip(red + cyan, 0, 255)                      # 'lighter' composite


def glitch_slices(img, t, k):
    rng = np.random.default_rng(int(math.floor(t * 30)))
    out = img.copy()
    bands = []
    for _ in range(7):
        h = int(round(rng.uniform(0.015, 0.075) * H))
        y0 = int(rng.integers(0, H - h))
        off = (rng.random() - 0.5) * 2 * 0.08 * W * k
        out[y0:y0 + h] = shift(img, off, 0)[y0:y0 + h]
        bands.append((y0, h, off))
    return out, bands


def _rgb_slice(task, wd):
    X = _xx_fixture()
    kpx = 4.0
    frames_ = [chroma(X, kpx)]
    g1, bands = glitch_slices(X, 0.5, 1.0)
    g2, bands2 = glitch_slices(X, 0.51, 1.0)
    g3, bands3 = glitch_slices(X, 0.54, 1.0)
    frames_ += [g1, g2, g3]
    path = write_video(frames_, Path(wd) / "rgb_slice.mp4", 10)
    frs = fx.frames(path, (W, H))
    inner = (XX > 10) & (XX < W - 10)
    r_off = float(np.median((XX - frs[0][..., 0] * (W - 1) / 255)[inner]))
    g_off = float(np.median((XX - frs[0][..., 1] * (W - 1) / 255)[inner]))
    rowd = np.median(XX - srcx(frs[1]), axis=1)
    disp_rows = int((np.abs(rowd) > 0.5).sum())
    hmin, hmax = min(b[1] for b in bands), max(b[1] for b in bands)
    return ([near("red buffer redrawn +k px", r_off, kpx, 0.3), near("cyan buffer redrawn -k px", g_off, -kpx, 0.3),
             check("7 slice bands, heights 1.5-7.5% H", len(bands) == 7 and hmin >= round(0.015 * H) and hmax <= round(0.075 * H),
                   [hmin, hmax], "2..8 px"),
             check("offsets within +-8% W x k", max(abs(b[2]) for b in bands) <= 0.08 * W, max(abs(b[2]) for b in bands),
                   "<= %.1f" % (0.08 * W)),
             check("rows shifted on the output", disp_rows > 3, disp_rows, "> 3"),
             check("seed floor(t x 30): same within a step, new on the next", bands == bands2 and bands != bands3, True, True),
             neg("red offset on the unsplit frame", float(np.median((XX - X[..., 0] * (W - 1) / 255)[inner])), kpx, 0.3)],
            [path, save_plan(wd, "rgb_slice", {"card": "TRANS-103", "k_px": kpx, "bands": bands})])


card("TRANS-103")(_rgb_slice)


def scene_handover(scenes, adj=0.05):
    out = []
    for i, (a, b) in enumerate(scenes):
        in_cut = a < adj or any(abs(b2 - a) <= adj for j, (a2, b2) in enumerate(scenes) if j != i)
        out_cut = any(abs(a2 - b) <= adj for j, (a2, b2) in enumerate(scenes) if j != i)
        out.append({"start": a, "end": b, "in": "cut" if in_cut else "fade 0.2", "out": "cut" if out_cut else "fade 0.22"})
    return out


def _handover(task, wd):
    scenes = [(0.0, 1.0), (1.0, 2.0), (2.5, 3.5)]
    plan = scene_handover(scenes)
    bg, prim = np.array([20.0, 20.0, 40.0]), np.array([240.0, 120.0, 40.0])
    g = np.clip((XX + YY) / ((W + H) * 0.45), 0, 1)              # 45-degree gradient, primary reached at 45 %
    full = mix(solid(bg), solid(prim), g)
    looks = [mix(full, solid((255, 255, 255)), box(30 + 60 * k, CY, 20, 20)) for k in range(3)]

    def frame(t):
        for k, p in enumerate(plan):
            if p["start"] <= t < p["end"]:
                o = 1.0
                if p["in"] != "cut":
                    o = min(o, c01((t - p["start"]) / 0.2))
                if p["out"] != "cut":
                    o = min(o, c01((p["end"] - t) / 0.22))
                return mix(BLACK, looks[k], o)
        return BLACK
    path, frs, ts = film(wd, "handover", frame, 3.6, 50)
    i1, i0 = at(ts, 1.0), at(ts, 0.98)
    o_out = float(np.median(frs[at(ts, 2.0 - 0.11)][..., 0]) / np.median(looks[1][..., 0]))
    o_in = float(np.median(frs[at(ts, 2.6)][..., 0]) / np.median(looks[2][..., 0]))
    diag = float(np.max(np.abs(full[5, 30] - full[30, 5])))
    return ([check("adjacent scenes hand over with a hard cut at 1.0 s", mad(frs[i0], looks[0]) < 0.5 and mad(frs[i1], looks[1]) < 0.5,
                   [mad(frs[i0], looks[0]), mad(frs[i1], looks[1])], "< 0.5"),
             check("planner: first scene cuts in at film start, isolated scene fades", plan[0]["in"] == "cut" and plan[1]["out"] != "cut"
                   and plan[2]["in"] != "cut", plan, True),
             near("isolated end fades out over 0.22 s (half at -0.11 s)", o_out, 0.5, 0.06),
             near("isolated start fades in over 0.2 s (half at +0.1 s)", o_in, 0.5, 0.06),
             check("full layer paints a 45-degree bg->primary gradient (equal along x+y)", diag < 1.5, diag, "< 1.5"),
             neg("hard cut at the isolated end (opacity half-way)", 1.0, 0.5, 0.06)],
            [path, save_plan(wd, "handover", {"card": "TRANS-104", "plan": plan})])


card("TRANS-104")(_handover)


# ═════════════════════ planners, springs, seams ═════════════════════
ENERGY = {"calm": (0.5, 0.8, "sine/power1", (20, 30)), "medium": (0.3, 0.5, "power2/3", (8, 15)),
          "high": (0.15, 0.3, "power4/expo", (3, 6))}
MOOD_PRIMARY = {"warm": "blur-crossfade", "cold": "push-slide", "editorial": "crossfade", "tech": "glitch",
                "playful": "squeeze", "dramatic": "zoom-through", "premium": "blur-crossfade"}
MOOD_ACCENT = {"warm": ["light-leak"], "tech": ["chromatic-aberration", "zoom-through"], "dramatic": ["color-dip"],
               "editorial": ["push-slide"], "cold": ["blur-crossfade"], "playful": ["elastic-push"], "premium": ["focus-pull"]}


def plan_transitions(n_cuts, energy, mood, related=()):
    lo, hi, ease, blurr = ENERGY[energy]
    prim, acc = MOOD_PRIMARY[mood], MOOD_ACCENT[mood][:2]
    n_prim = int(round(0.65 * n_cuts))
    n_acc = n_cuts - n_prim
    acc_at = {min(n_cuts - 1, int((j + 0.5) * n_cuts / n_acc)) for j in range(n_acc)}
    out = []
    for k in range(n_cuts):
        kind = acc[k % len(acc)] if k in acc_at else prim
        if k == 0:
            d = 0.5
        elif k == n_cuts - 1:
            d = 0.8
        elif k in related:
            d = 0.3
        else:
            d = round((lo + hi) / 2, 3)
        out.append({"cut": k, "type": kind, "dur": d, "ease": ease, "blur_px": blurr})
    return out


def _energy_map(task, wd):
    plan = plan_transitions(12, "medium", "tech", related=(4, 7))
    types = [p["type"] for p in plan]
    share = types.count(MOOD_PRIMARY["tech"]) / len(types)
    mids = [p["dur"] for p in plan[1:-1] if p["cut"] not in (4, 7)]
    sample = [p["type"] for p in plan[:3]]
    checks = [check("primary transition on 60-70% of cuts", 0.6 <= share <= 0.7, share, "0.6..0.7"),
              check("2-3 transition types per video", 2 <= len(set(types)) <= 3, sorted(set(types)), "2..3"),
              check("medium energy: 0.3-0.5 s, power2/3 eases", all(0.3 <= d <= 0.5 for d in mids) and plan[1]["ease"] == "power2/3",
                    mids[:3], "0.3..0.5"),
              check("opening 0.4-0.6 s, related 0.3 s, outro 0.6-1.0 s", 0.4 <= plan[0]["dur"] <= 0.6 and plan[4]["dur"] == 0.3
                    and 0.6 <= plan[-1]["dur"] <= 1.0, [plan[0]["dur"], plan[4]["dur"], plan[-1]["dur"]], True),
              check("blur by energy (medium 8-15 px)", plan[0]["blur_px"] == (8, 15), plan[0]["blur_px"], (8, 15))]
    reel_paths = []
    for k, p in enumerate(plan[:2]):
        if p["type"] in CSS:
            reel_paths.append(run_css(wd, p["type"], "TRANS-218")[1])
    checks.append(check("planned transitions render (first two cuts)", len(reel_paths) == 2, len(reel_paths), 2))
    checks.append(neg("primary share when every cut uses one type", 1.0, 0.65, 0.05))
    return checks, reel_paths + [save_plan(wd, "transition_plan", {"card": "TRANS-218", "plan": plan, "sample": sample})]


card("TRANS-218")(_energy_map)

TEMPLATES = {
    "crossfade": (0.5, "tl.to('__OLD__',{opacity:0,duration:__DUR__},__T__);tl.fromTo('__NEW__',{opacity:0},{opacity:1,duration:__DUR__},__T__);"),
    "blur-crossfade": (0.6, "tl.to('__OLD__',{opacity:0,filter:'blur(10px)',duration:__DUR__},__T__);tl.fromTo('__NEW__',{opacity:0,filter:'blur(10px)'},{opacity:1,filter:'blur(0px)',duration:__DUR__},__T__);"),
    "push-slide": (0.5, "tl.to('__OLD__',{x:-__DX__,duration:__DUR__},__T__);tl.fromTo('__NEW__',{x:__DX__},{x:0,duration:__DUR__},__T__);"),
    "zoom-through": (0.4, "tl.to('__OLD__',{scale:2.5,opacity:0,duration:__DUR__},__T__);tl.fromTo('__NEW__',{scale:0.5,opacity:0},{scale:1,opacity:1,duration:__DUR__},__T__);"),
    "squeeze": (0.4, "tl.to('__OLD__',{scaleX:0,duration:__DUR__},__T__);tl.fromTo('__NEW__',{scaleX:0},{scaleX:1,duration:__DUR__},__T__);"),
}
DIRS = {"LEFT": 1920, "RIGHT": -1920, "UP": 1080, "DOWN": -1080}


def inject(planner_md, energy, starts):
    import re
    out, rows = [], []
    for k, line in enumerate(planner_md.strip().splitlines()):
        m = re.search(r"\*\*Transition:\*\*\s*([a-z-]+)(?:\s+(LEFT|RIGHT|UP|DOWN))?(?:\s+([\d.]+)s)?", line)
        kind = m.group(1) if m else ("zoom-through" if energy[k] == "high" else "blur-crossfade")
        if kind not in TEMPLATES:
            raise ValueError("unknown transition %s" % kind)
        d = min(float(m.group(3)) if m and m.group(3) else TEMPLATES[kind][0], 2.0)
        dx = DIRS.get((m.group(2) if m else None) or "LEFT")
        code = (TEMPLATES[kind][1].replace("__OLD__", "#s%d" % k).replace("__NEW__", "#s%d" % (k + 1))
                .replace("__T__", str(starts[k])).replace("__DUR__", str(d)).replace("__DX__", str(dx)))
        rows.append({"scene": k, "type": kind, "dur": d, "dx": dx})
        out.append(code)
    return "\n".join(out), rows


def _registry_inject(task, wd):
    md = """Scene 1 **Transition:** push-slide LEFT
Scene 2 (no transition named)
Scene 3 **Transition:** crossfade 3.5s
Scene 4 (no transition named)"""
    code, rows = inject(md, ["medium", "high", "medium", "calm"], [2.0, 5.0, 8.0, 11.0])
    js = Path(wd) / "stamped.js"
    js.write_text(code, encoding="utf-8")
    runner = Path(wd) / "run.js"
    runner.write_text("const calls=[];const tl={to:(s,v,t)=>calls.push(['to',s,v,t]),fromTo:(s,a,b,t)=>calls.push(['fromTo',s,a,b,t])};"
                      "eval(require('fs').readFileSync(process.argv[2],'utf8'));console.log(JSON.stringify(calls));")
    r = subprocess.run(["node", str(runner), str(js)], capture_output=True, text=True, timeout=20)
    calls = json.loads(r.stdout) if r.returncode == 0 else []
    leftover = "__" in code
    push = [c for c in calls if c[1] == "#s0"]
    durs = [c[2].get("duration") if c[0] == "to" else c[3].get("duration") for c in calls]
    return ([check("stamped GSAP code runs (node, mocked timeline): 8 tween calls", len(calls) == 8, len(calls), 8),
             check("every placeholder replaced", not leftover, leftover, False),
             check("push-slide LEFT: old x -1920 at T=2.0", bool(push) and push[0][2].get("x") == -1920 and push[0][3] == 2.0,
                   push[:1], "x -1920 at 2.0"),
             check("defaults: zoom-through for high energy, blur-crossfade otherwise", rows[1]["type"] == "zoom-through"
                   and rows[3]["type"] == "blur-crossfade", [r_["type"] for r_ in rows], True),
             check("durations capped at max 2.0 s", max(d for d in durs if d is not None) <= 2.0 and rows[2]["dur"] == 2.0,
                   rows[2]["dur"], 2.0),
             neg("tween calls if the template is not stamped (raw placeholders)", 0, 8, 0)],
            [js, save_plan(wd, "injection", {"card": "TRANS-219", "rows": rows})])


card("TRANS-219")(_registry_inject)


def vel_card(card_id, name, d_out, d_in, travel, blur_px, note):
    tc, fps = 0.4, 100
    T = tc + d_in + 0.05

    def ypos(t):
        if t < tc:
            return -travel * p_in(1)(c01((t - (tc - d_out)) / d_out)), "A"
        return travel * (1 - p_out(1)(c01((t - tc) / d_in))), "B"

    def blur_at(t):
        if t < tc:
            return blur_px * c01((t - (tc - d_out)) / d_out)
        return blur_px * (1 - c01((t - tc) / d_in))

    def texy(blue):
        img = _tex(blue)
        img[..., 0] = YY * 255.0 / (H - 1)                  # red carries the y code here
        return img
    TA, TB = texy(BLUE_A), texy(BLUE_B)

    def frame(t):
        y, w = ypos(t)
        img = TA if w == "A" else TB
        return blur(shift(img, 0, y), blur_at(t))

    def run(task, wd):
        path, frs, ts = film(wd, name, frame, T, fps)
        ys = [float(np.median((YY - f[..., 0] * (H - 1) / 255.0)[(YY > 20) & (YY < H - 20)])) for f in frs]
        v = np.diff(ys) * fps
        ic = next(i for i, t in enumerate(ts) if t >= tc)
        sp = np.abs(v)
        before = sp[ic - 3:ic - 1]
        after = sp[ic:ic + 2]
        out_peak = int(np.argmax(sp[:ic - 1]))
        in_peak = ic + int(np.argmax(sp[ic:]))
        sh = [gsharp(f) for f in frs]
        checks = [check("outgoing speed peaks right before the cut", out_peak >= ic - 3, out_peak, ">= %d" % (ic - 3)),
                  check("incoming speed peaks right after the cut", in_peak <= ic + 2, in_peak, "<= %d" % (ic + 2)),
                  check("same direction across the cut (both move up)", float(np.mean(v[ic - 4:ic - 1])) < 0 and float(np.mean(v[ic + 1:ic + 4])) < 0,
                        [float(np.mean(v[ic - 4:ic - 1])), float(np.mean(v[ic + 1:ic + 4]))], "< 0"),
                  check("blur peaks at the cut (detail at the cut = the minimum, far below the rest frames)",
                        min(sh[ic - 1], sh[ic]) <= min(sh) + 0.3 and min(sh[ic - 1], sh[ic]) < 0.3 * sh[-1],
                        [min(sh[ic - 1], sh[ic]), min(sh), sh[-1]], "min at cut"),
                  near("exit travel (px)", ys[ic - 1], -travel * p_in(1)((ts[ic - 1] - (tc - d_out)) / d_out), 0.5)]
        if abs(d_out - d_in) < 1e-9:
            checks.append(near("matched velocity at the cut (in/out speed ratio)", float(after.mean() / before.mean()), 1.0, 0.2))
        checks.append(neg("speed peak position for a static hard cut", 0.0, 1.0, 0.5))
        return checks, [path, save_plan(wd, name, {"card": card_id, "exit_s": d_out, "enter_s": d_in, "travel_px": travel,
                                                   "blur_px": blur_px, "note": note})]
    card(card_id)(run)


vel_card("TRANS-29", "velocity_matched_cut", 0.33, 1.0, 150 * K, 30 * K,
         "exit y -150 blur 30 0.33 s power2.in; enter 150->0 blur 30->0 1.0 s power2.out (scaled x0.1); fastest moments meet at the cut")
vel_card("TRANS-220", "velocity_matched_transition", 0.3, 0.3, 150 * K, 20 * K,
         "exit y -150 power-in + blur, entry from the matching offset with the mirrored out ease")


def _seams(task, wd):
    fps = 50
    checks, outs = [], []
    # zoom-through forward: scale toward the viewer, hard cut at the blur peak with opacity 0.15
    tc = 0.3

    def zt(t):
        if t < tc:
            e = p_in(2)(t / tc)
            return mix(BLACK, blur(affine(AT, 1 + 2 * e), 2.0 * e), 1 - 0.85 * e)
        e = p_out(2)((t - tc) / 0.3)
        return mix(BLACK, blur(affine(BT, 3 - 2 * e), 2.0 * (1 - e)), 0.15 + 0.85 * e)
    p1, f1, t1 = film(wd, "zoom_through_forward", zt, 0.6, fps)
    ic = at(t1, tc)
    sh = [gsharp(f) for f in f1]
    op = float(np.median(f1[ic][..., 2])) / BLUE_B
    checks += [check("zoom-through: hard cut at the blur peak", int(np.argmin(sh)) in (ic - 1, ic), int(np.argmin(sh)), ic),
               near("zoom-through: opacity 0.15 at the cut", op, 0.15, 0.03),
               check("inverse zoom arrival: scale settles from 3 to 1", abs(scale_est(f1[-1]) - 1) < 0.01, scale_est(f1[-1]), 1.0)]
    outs.append(p1)
    # cut-the-curve between scenes: x 0 -> -230 then +230 -> 0, mirrored eases, same direction
    def ctc(t):
        if t < 0.3:
            return shift(A0, -230 * K * p_in(2)(t / 0.3), 0)
        return shift(B0, 230 * K * (1 - p_out(2)((t - 0.3) / 0.3)), 0)
    p2, f2, t2 = film(wd, "cut_the_curve_scenes", ctc, 0.6, fps)
    sel = (XX > 30) & (XX < W - 30)
    xs = [xshift(f, sel) for f in f2]
    i0 = at(t2, 0.3)
    checks += [near("cut-the-curve: outgoing reaches -230 css px at the cut", xs[i0 - 1], -230 * K * p_in(2)(t2[i0 - 1] / 0.3), 0.5),
               near("cut-the-curve: incoming starts at +230 css px", xs[i0], 230 * K, 0.5),
               check("same direction (both move left)", xs[i0 - 1] < xs[i0 - 3] and xs[i0 + 2] < xs[i0], True, True)]
    outs.append(p2)
    # waterfall: per-word cut-the-curve, staggered
    words = 3

    def wf(t):
        img = solid(BG)
        for k in range(words):
            tk = t - 0.08 * k
            if tk < 0.3:
                x = -23 * p_in(2)(c01(tk / 0.3))
                col = WORDC
            else:
                x = 23 * (1 - p_out(2)(c01((tk - 0.3) / 0.3)))
                col = ACCENT
            img = mix(img, solid(col), box(50 + 45 * k + x, CY, 30, 10))
        return img
    p3, f3, t3 = film(wd, "waterfall_cut", wf, 0.8, fps)
    swaps = []
    for k in range(words):
        sub = [f[:, int(50 + 45 * k - 22):int(50 + 45 * k + 22)] for f in f3]
        swaps.append(next(t for f, t in zip(sub, t3) if (np.abs(f - ACCENT).max(-1) < 3).any()))
    checks.append(check("waterfall: each word cuts on its own beat (staggered 0.08 s)",
                        all(abs((swaps[k] - swaps[0]) - 0.08 * k) <= 1.0 / fps + 1e-6 for k in range(words)), swaps, "0.08 s apart"))
    outs.append(p3)
    checks.append(neg("blur-peak cut on an unzoomed hard cut", float(gsharp(AT) - gsharp(AT)), gsharp(AT), 0.5 * gsharp(AT)))
    return checks, outs + [save_plan(wd, "seams", {"card": "TRANS-228", "travel_css_px": 230, "peak_blur": "text 10, full 20 (scaled)"})]


card("TRANS-228")(_seams)

SPR_FIRM = (300.0, 22.0)            # stiffness, damping (mass 1): an underdamped 'firm' spring


def spring_step(t, k=SPR_FIRM[0], c=SPR_FIRM[1]):
    """Unit step response of a damped spring starting at rest; pure in t."""
    if t <= 0:
        return 0.0
    w0 = math.sqrt(k)
    z = c / (2 * w0)
    wd_ = w0 * math.sqrt(1 - z * z)
    return 1 - math.exp(-z * w0 * t) * (math.cos(wd_ * t) + z * w0 / wd_ * math.sin(wd_ * t))


def track(t, keys):
    v = keys[0][1]
    for (ta, va), (tb, vb) in zip(keys, keys[1:]):
        v += (vb - va) * spring_step(t - tb)
    return v


def _spring_track(task, wd):
    keys = [(0.0, 30.0), (0.3, 120.0), (1.0, 60.0), (1.6, 160.0)]
    ts_ = np.linspace(0, 2.4, 241)
    vals = [track(t, keys) for t in ts_]
    rng = np.random.default_rng(3)
    perm = rng.permutation(len(ts_))
    shuffled = {int(i): track(ts_[i], keys) for i in perm}
    pure = all(abs(shuffled[i] - vals[i]) < 1e-12 for i in range(len(ts_)))
    jumps = max(abs(a - b) for a, b in zip(vals, vals[1:]))
    path, frs, fts = film(wd, "spring_track", lambda t: mix(solid(BG), solid(WORDC), box(track(t, keys) * W / 192, CY, 10, 10)), 2.4, 25)
    xs = [centroid(f, WORDC)[0] for f in frs]
    err = max(abs(x - track(t, keys)) for x, t in zip(xs, fts))
    settle = [abs(track(tb - 0.01, keys) - va) / abs(va) for (ta, va), (tb, vb) in zip(keys, keys[1:]) if tb - ta > 0.5]
    over = max(vals[i] for i in range(len(ts_)) if 0.3 < ts_[i] < 1.0) > 120
    step_jump = max(abs(b - a) for (_, a), (_, b) in zip(keys, keys[1:])) * 0.1
    return ([check("pure in t: evaluating in any order gives the same values", pure, pure, True),
             check("continuous: every retarget starts from rest (max 10 ms jump < 10% of a step)", jumps < step_jump, jumps,
                   "< %.1f" % step_jump),
             check("one spring per change settles near its target before the next key", max(settle) < 0.02, settle, "< 2%"),
             check("firm spring overshoots slightly", over, over, True),
             near("rendered dot follows track(t) (max error px)", err, 0.0, 0.5),
             neg("max 10 ms jump of a step track without springs", 90.0, 0.0, step_jump)],
            [path, save_plan(wd, "spring", {"card": "TRANS-229", "keys": keys, "spring": {"k": SPR_FIRM[0], "c": SPR_FIRM[1]}})])


card("TRANS-229")(_spring_track)


def _rack_focus(task, wd):
    sharp_, soft = AT, blur(AT, 2.0)                          # constant-blur copy computed once
    D = 0.6
    path, frs, ts = film(wd, "rack_focus", lambda t: mix(sharp_, soft, p_io(1)(t / D)), D, 30)
    diff = soft - sharp_
    res = []
    for f in frs:
        a = float(np.sum((f - sharp_) * diff) / np.sum(diff * diff))
        res.append(float(np.abs(f - mix(sharp_, soft, a)).max()))
    anim = blur(AT, 1.0)
    a = float(np.sum((anim - sharp_) * diff) / np.sum(diff * diff))
    return ([check("every frame is a cross-fade of the sharp and one constant-blur copy (max abs residual)", max(res) < 1.5, max(res), "< 1.5"),
             near("mid frame half-way", float(np.sum((frs[at(ts, D / 2)] - sharp_) * diff) / np.sum(diff * diff)), 0.5, 0.03),
             neg("cross-fade residual of an animated (radius 1 px) blur frame", float(np.abs(anim - mix(sharp_, soft, a)).max()), 0.0, 1.5)],
            [path, save_plan(wd, "rack_focus", {"card": "TRANS-230", "blur_px": 2.0, "dur": D})])


card("TRANS-230")(_rack_focus)


def roll_frame(img, ang, persp, origin_bottom=False):
    """rotationX by ang (rad) with perspective; pivot at the centre or the bottom edge."""
    piv = (H - 1) if origin_bottom else CY
    c, s = math.cos(ang), math.sin(ang)
    sy = YY - piv
    den = c * persp + sy * s
    yl = np.where(np.abs(den) > 1e-6, sy * persp / np.where(np.abs(den) > 1e-6, den, 1), 1e9)
    z = yl * s
    xl = (XX - CX) * (persp - z) / persp
    src_y = yl + piv
    ok = (src_y >= -0.5) & (src_y <= H - 0.5) & (np.abs(xl) <= W / 2) & (persp - z > 1) & (c > 0)
    return np.where(ok[..., None], sample(img, xl + CX, src_y, fill=(0, 0, 0)), BG)


def visible_rows(fr):
    m = np.abs(fr - BG).max(-1) > 3
    rows = np.nonzero(m.any(axis=1))[0]
    return (int(rows.min()), int(rows.max())) if rows.size else (0, -1)


def roll_card(card_id, name, frames_done, first_frac, from_deg, persp, origin_bottom, fps=60):
    kexp = math.log(1 - first_frac) / math.log(1 - 1.0 / frames_done)

    def prog_(f):
        return 1 - (1 - min(f, frames_done) / frames_done) ** kexp

    def run(task, wd):
        ts_ = [i / fps for i in range(frames_done + 4)]
        frs_in = [roll_frame(A0, math.radians(from_deg) * (1 - prog_(i)), persp, origin_bottom) for i in range(len(ts_))]
        path = write_video(frs_in, Path(wd) / (name + ".mp4"), fps)
        frs = fx.frames(path, (W, H))
        hs = []
        for f in frs:
            lo, hi = visible_rows(f)
            hs.append(hi - lo + 1)
        ref = []
        for e in np.linspace(0, 1, 201):
            lo, hi = visible_rows(roll_frame(A0, math.radians(from_deg) * (1 - e), persp, origin_bottom))
            ref.append(hi - lo + 1)
        e1 = float(np.linspace(0, 1, 201)[int(np.argmin([abs(r - hs[1]) for r in ref]))])
        checks = [near("front-loaded: about %d%% of the flip in the first frame" % int(first_frac * 100), e1, first_frac, 0.06),
                  check("done in %d frames" % frames_done, mad(frs[frames_done], A0) < 0.5, mad(frs[frames_done], A0), "< 0.5"),
                  check("starts edge-on (rotated %d deg)" % from_deg, hs[0] <= 3, hs[0], "<= 3 rows")]
        if origin_bottom:
            bottoms = [visible_rows(f)[1] for f in frs[1:]]
            checks.append(check("origin 50% 100%: the bottom edge stays put", max(bottoms) - min(bottoms) <= 1, bottoms[:5], "fixed"))
        checks.append(neg("first-frame progress of a linear roll", 1.0 / frames_done, first_frac, 0.06))
        return checks, [path, save_plan(wd, name, {"card": card_id, "frames": frames_done, "first_frame": first_frac,
                                                   "from_deg": from_deg, "perspective": persp})]
    card(card_id)(run)


roll_card("TRANS-232", "roll_flip_seam", 10, 0.35, -90, 1200 * K, False)
roll_card("TRANS-255", "front_loaded_roll", 10, 0.35, -90, 2200 * K, True)


def _polarity(task, wd):
    acts, moves, T = [2.0, 4.0], [1.0, 2.0, 3.3, 4.0], 6.0
    flips = [m for m in moves if any(abs(m - a) < 1e-9 for a in acts)]

    def frame(t):
        k = sum(1 for f in flips if t >= f)
        mv = max([m for m in moves if m <= t] or [0.0])
        x = 40 + 100 * p_out(2)(c01((t - mv) / 0.4)) if mv else 40
        g, ink = (PAPER2, CHARC) if k % 2 == 0 else (CHARC, PAPER2)
        return mix(solid(g), solid(ink), box(x, CY, 20, 20))
    path, frs, ts = film(wd, "polarity", frame, T, 10)
    lum_ = [float(lum(f).mean()) > 128 for f in frs]
    det = [ts[i] for i in range(1, len(frs)) if lum_[i] != lum_[i - 1]]
    return ([check("stage flips only at the act boundaries riding a move", det == flips, det, flips),
             check("moves that are not act boundaries never flip", 1.0 not in det and 3.3 not in det, det, "no 1.0/3.3"),
             neg("flip count if every move flipped", len(moves), len(flips), 0)],
            [path, save_plan(wd, "polarity", {"card": "TRANS-233", "acts": acts, "moves": moves, "flips": flips})])


card("TRANS-233")(_polarity)


def aces(x):
    return np.clip((x * (2.51 * x + 0.03)) / (x * (2.43 * x + 0.59) + 0.14), 0, 1)


def _exposure_fade(task, wd):
    hdr = 0.2 + 1.8 * (XX / W)[..., None] * np.array([1.0, 0.9, 0.7])
    expo = lambda t: 0.95 * (0.12 + 0.88 * smooth(0, 1.1, t))      # noqa: E731
    path, frs, ts = film(wd, "exposure_fade", lambda t: 255 * aces(hdr * expo(t)), 10.0, 5)
    rate = 8000
    tt = np.arange(int(10 * rate)) / rate
    snd = 0.4 * np.sin(2 * np.pi * 300 * tt) * (1 - 0.45 * np.array([smooth(9.4, 10, x) for x in tt]))
    wav = fx.write_wav(Path(wd) / "sound_ground.wav", snd, rate)
    r0 = float(lum(frs[0]).mean()) / float(lum(frs[-1]).mean())
    exp_r = float(lum(255 * aces(hdr * expo(0))).mean()) / float(lum(255 * aces(hdr * expo(10))).mean())
    s, r = fx.read_wav(wav)
    g_end = tone_amp(s[:, 0], r, 300, 9.95, 10.0) / 0.4
    return ([near("first frame = tone-mapped exposure at 12% (brightness ratio)", r0, exp_r, 0.02),
             check("opens dim, never a black overlay (first frame not black)", float(frs[0].max()) > 20, float(frs[0].max()), "> 20"),
             near("full exposure after 1.1 s", mad(frs[at(ts, 1.2)], frs[-1]), 0.0, 0.6),
             near("sound ground fades by x(1 - 0.45) at 10 s", g_end, 0.55, 0.04),
             neg("first-frame brightness ratio of a black overlay fade", 0.0, exp_r, 0.02)],
            [path, wav, save_plan(wd, "exposure", {"card": "TRANS-234", "exposure": "0.95(0.12+0.88 smooth(0,1.1,t))", "tonemap": "ACES fit"})])


card("TRANS-234")(_exposure_fade)


def _letterbox(task, wd):
    S = 8.0
    bar = 70 * H / 1080
    t_open = min(2.4, 0.15 * S)

    def hgt(t):
        if t < S - 1.6 - 0.2:
            return bar * (1 - p_io(3)((t - t_open) / 2.2))
        return bar * p_io(3)((t - (S - 1.8)) / 1.6)

    def frame(t):
        img = A0.copy()
        h = hgt(t)
        img[YY < h] = 0
        img[YY >= H - h] = 0
        return img
    path, frs, ts = film(wd, "letterbox", frame, S, 10)

    def meas(f):
        return float((f[:, int(CX)].max(-1) < 1).sum()) / 2
    checks = []
    for t in (0.5, t_open + 1.1, S - 1.0, S):
        i = at(ts, t)
        checks.append(near("bar height at %.1f s (70 css px, power4.inOut)" % t, meas(frs[i]), math.ceil(hgt(ts[i]) - 1e-9), 1.0))
    checks.append(neg("bar height on the bare frame at 0.5 s", meas(A0), math.ceil(bar), 1.0))
    return checks, [path, save_plan(wd, "letterbox", {"card": "TRANS-240", "open_at": t_open, "open_s": 2.2, "close_s": 1.6})]


card("TRANS-240")(_letterbox)


def _reframe_cut(task, wd):
    ox, oy, tc = 585 * K, 690 * K * (H / 108.0), 0.5

    def scale(t):
        return 1.0 if t < tc else 1.42 + (1.10 - 1.42) * expo_out((t - tc) / 0.6)

    def frame(t):
        return affine(A0, scale(t), cx=ox, cy=oy)
    path, frs, ts = film(wd, "reframe_cut", frame, tc + 0.8, 30)
    ic = at(ts, tc)

    def s_est(f):
        band = (np.abs(YY - oy) < 20) & (XX > 10) & (XX < W - 10)
        return float(np.polyfit(srcx(f)[band], XX[band], 1)[0])
    fixed = float(srcx(frs[ic])[int(round(oy)), int(round(ox))])
    return ([near("before the cut: scale 1", s_est(frs[ic - 1]), 1.0, 0.01),
             near("hard cut sets scale 1.42 at the story turn", s_est(frs[ic]), 1.42, 0.015),
             near("settles toward 1.10 (expo.out, 0.6 s)", s_est(frs[at(ts, tc + 0.3)]), scale(ts[at(ts, tc + 0.3)]), 0.015),
             near("transform origin (585, 690) stays fixed", fixed, ox, 0.8),
             neg("scale on the cut frame without the reframe", s_est(A0), 1.42, 0.015)],
            [path, save_plan(wd, "reframe", {"card": "TRANS-241", "origin_css": [585, 690], "scale": [1.42, 1.10]})])


card("TRANS-241")(_reframe_cut)


def _cut_kick(task, wd):
    cut, fps = 0.4, 50
    cxk, cyk = 0.5 * W, 0.48 * H

    def frame(t):
        base = A0 if t < cut else B0
        amt = c01(1 - abs(t - cut) / 0.16)
        img = np.mean([affine(base, 1.0 / (1 - amt * i / 11 * 0.12), cx=cxk, cy=cyk) for i in range(12)], axis=0) if amt > 0 else base
        fl = c01(1 - abs(t - cut) / 0.1) * 0.55
        g = np.clip(1 - np.hypot(XX - cxk, YY - cyk) / (0.75 * math.hypot(W, H) / 2), 0, 1)
        return mix(img, solid((255, 255, 255)), fl * g)
    path, frs, ts = film(wd, "cut_kick", frame, 0.8, fps)
    i = at(ts, cut + 0.08)
    amt = c01(1 - abs(ts[i] - cut) / 0.16)
    fl = c01(1 - abs(ts[i] - cut) / 0.1) * 0.55
    centre = frs[i][int(round(cyk)), int(round(cxk))]
    base = B0[int(round(cyk)), int(round(cxk))]
    a_c = float((centre[0] - base[0]) / (255 - base[0]))
    j = at(ts, cut + 0.12)
    amt_j = c01(1 - abs(ts[j] - cut) / 0.16)
    exp_s = 1.0 / np.mean([1 - amt_j * k / 11 * 0.12 for k in range(12)])
    band = (np.abs(YY - cyk) < 15) & (XX > 20) & (XX < W - 20)
    s_meas = float(np.polyfit(srcx(frs[j])[band], XX[band], 1)[0])
    return ([near("flash opacity at the centre = (1 - d/0.10) x 0.55 at +0.08 s", a_c, fl, 0.03),
             near("12-tap radial zoom blur strength at +0.12 s (mean tap scale)", s_meas, exp_s, 0.01),
             check("both vanish outside +-0.16 s", mad(frs[at(ts, cut + 0.2)], B0) < 0.5, mad(frs[at(ts, cut + 0.2)], B0), "< 0.5"),
             neg("flash opacity at +0.08 s on a bare cut", 0.0, fl, 0.03)],
            [path, save_plan(wd, "cut_kick", {"card": "TRANS-242", "taps": 12, "window_s": 0.16, "flash_peak": 0.55})])


card("TRANS-242")(_cut_kick)


def _fadeblack_text(task, wd):
    bounds = [2.3, 4.834]
    dur = 23 / 30.0
    shots = [A0, B0, A0]
    lines = ["first line", "second line", "third line"]
    layers = [text_layer(l, size=14, color=(255, 255, 255), pos=(W / 2, H * 0.8))[1] for l in lines]
    text_start = [0.0] + [b - dur / 2 for b in bounds]

    def frame(t):
        k = sum(1 for b in bounds if t >= b)
        dk = [b for b in bounds if abs(t - b) < dur / 2]
        al = 0.0
        if dk:
            al = 1 - abs(t - dk[0]) / (dur / 2)
        img = mix(shots[k], BLACK, al)
        kk = sum(1 for s_ in text_start if t >= s_) - 1
        return mix(img, solid((255, 255, 255)), layers[kk])
    path, frs, ts = film(wd, "fadeblack_text", frame, 5.6, 30)
    i = at(ts, bounds[0])
    pic = frs[i][:int(H * 0.6)]
    txt_mid = float((lum(frs[i])[int(H * 0.7):] > 200).sum())
    j = at(ts, bounds[0] - dur / 2 + 0.05)
    txt2 = float(np.mean(np.abs(frs[j][int(H * 0.7):] - frs[at(ts, 1.0)][int(H * 0.7):]).max(-1) > 50))
    return ([check("shot dips to black at the boundary (picture area)", float(pic.max()) < 3, float(pic.max()), "< 3"),
             check("next line is on screen during the black", txt_mid > 20, txt_mid, "> 20 px"),
             check("next text starts at the start of the dip (line changed by then)", txt2 > 0.005, txt2, "> 0.005"),
             near("dip length 23 frames at 30 fps", dur * 30, 23.0, 0.01),
             neg("text pixels in the black of a plain fade", 0.0, 20.0, 19.0)],
            [path, save_plan(wd, "fadeblack_text", {"card": "TRANS-243", "boundaries": bounds, "dip_s": dur})])


card("TRANS-243")(_fadeblack_text)


def _split_whip(task, wd):
    E_WHIP = p_out(3)
    gold = hexc("#f5c97a")

    def frame(t):
        img = solid(BG)
        er, el = E_WHIP(t / 0.45), E_WHIP((t - 0.06) / 0.45)
        xr = W / 2 + (W / 2) * (1 - er)
        xl = -(W / 2) * (1 - el)
        right = (XX >= xr) & (XX < xr + W / 2)
        left = (XX >= xl) & (XX < xl + W / 2)
        img = np.where(right[..., None], sample(B0, XX - xr + W / 2 - W / 4 + W / 4, YY), img)
        img = np.where(left[..., None], sample(A0, XX - xl, YY), img)
        sh_ = H * p_out(2)(c01(t / 0.5))
        seam = (np.abs(XX - CX) <= 1) & (np.abs(YY - CY) < sh_ / 2)
        img[seam] = gold
        if t > 0.7:
            img = np.where((XX < W / 2)[..., None], img * 0.4, img)
        return img
    path, frs, ts = film(wd, "split_whip", frame, 0.9, 50)
    i = at(ts, 0.2)
    er, el = E_WHIP(ts[i] / 0.45), E_WHIP((ts[i] - 0.06) / 0.45)
    redge = float(np.nonzero(bwt(frs[i])[int(CY) + 10] > 0.5)[0].min())
    seam_h = float((np.abs(frs[i][:, int(CX)] - gold).max(-1) < 2).sum())
    return ([near("right half whips in from its edge (left edge px)", redge, math.ceil(W / 2 + (W / 2) * (1 - er) - 1e-9), 1.0),
             check("left half trails by 60 ms", el < er, [el, er], "left behind"),
             near("gold seam grows scaleY 0 -> 1 in 0.5 s (px)", seam_h, 2 * math.ceil(H * p_out(2)(ts[i] / 0.5) / 2 - 0.5), 2.0),
             check("tint dims one half while the other is named", float(lum(frs[-1])[:, :int(W / 2) - 2].mean()) <
                   0.5 * float(lum(frs[at(ts, 0.6)])[:, :int(W / 2) - 2].mean()), True, True),
             neg("right-half edge without the whip", float(W / 2), math.ceil(W / 2 + (W / 2) * (1 - er) - 1e-9), 1.0)],
            [path, save_plan(wd, "split_whip", {"card": "TRANS-244", "whip_s": 0.45, "offset_ms": 60, "E.whip": "power3.out assumed"})])


card("TRANS-244")(_split_whip)


# ═════════════════════ one-container and UI handoffs ═════════════════════
def _word_plane(task, wd):
    t_in, t_cut, fps = 0.12, 0.3, 50
    plate = np.array([15.0, 15.0, 15.0])
    _, wa = text_layer("KAFIH", size=40, color=(255, 255, 255))

    def frame(t):
        under = affine(A0, 1.0) if t < t_cut else affine(B0, 1.42 + (1.10 - 1.42) * expo_out((t - t_cut) / 0.6))
        e = expo_out((t - t_in) / 0.2) if t >= t_in else 0.0
        if t < t_in:
            return under
        fly = p_io(3)((t - 0.45) / 0.55)
        s = (1.25 + (1 - 1.25) * e) * (1 + (0.36 - 1) * fly)
        dx, dy = 14 * (1 - e), -44 * fly
        plate_a = (1 - fly) * min(1.0, e * 4)
        img = mix(under, solid(plate), plate_a)
        word = affine(np.repeat(wa[..., None], 3, -1), s, dx=dx, dy=dy)[..., 0]
        word = blur(np.repeat(word[..., None], 3, -1), 1.8 * (1 - e))[..., 0]
        return mix(img, solid((255, 255, 255)), word)
    path, frs, ts = film(wd, "word_plane", frame, 1.1, fps)
    ic = at(ts, t_cut)
    covered = [float(np.mean(np.ptp(frs[i], axis=-1) < 4)) for i in (ic - 1, ic)]   # plate + white glyphs are grey; footage is not
    j = at(ts, 0.45 + 0.275)
    _, wy, _ = centroid(frs[j], np.array([255.0, 255, 255]), 60, bg=np.array([0.0, 0, 0]))
    fly = p_io(3)((ts[j] - 0.45) / 0.55)
    return ([check("word plane fills the frame at the cut (plate + glyphs)", min(covered) > 0.98, covered, "> 0.98"),
             check("the cut happens behind it: plate frames identical across the cut", mad(frs[ic - 1], frs[ic]) < 1.0,
                   mad(frs[ic - 1], frs[ic]), "< 1"),
             near("word flies up toward y -440 css px (centroid offset at mid-flight)", wy - CY, -44 * fly, 3.0),
             check("new shot revealed under the departing word", fracb(frs[-1], lum(frs[-1]) < 200) > 0.95,
                   fracb(frs[-1], lum(frs[-1]) < 200), "> 0.95"),
             neg("frame change at the cut without the plane", mad(A0, affine(B0, 1.42)), 0.0, 1.0)],
            [path, save_plan(wd, "word_plane", {"card": "TRANS-237", "in_s": t_in, "cut_s": t_cut,
                                                "note": "latin stand-in word (no Arabic font in PIL default)"})])


card("TRANS-237")(_word_plane)


def _card_rect_mask(cx, cy, w, h, rad):
    qx = np.abs(XX - cx) - (w / 2 - rad)
    qy = np.abs(YY - cy) - (h / 2 - rad)
    d = np.hypot(np.maximum(qx, 0), np.maximum(qy, 0)) + np.minimum(np.maximum(qx, qy), 0) - rad
    return np.clip(0.5 - d, 0, 1)


def container_state(t, t0=0.0):
    u = t - t0
    if u < 0.66:
        e = p_io(2)(u / 0.66)
        return -36 * e, 1 + (0.56 - 1) * e, 44 * K * e
    if u < 0.9:
        return -36, 0.56, 4.4
    e = p_in(2)(c01((u - 0.9) / 0.38))
    return -36 * (1 - e), 0.56 + (0.02 - 0.56) * e, 4.4 + (60 - 4.4) * e


def _container_film(wd, name, iris_first):
    t0 = 0.5 if iris_first else 0.0

    def frame(t):
        img = solid(BG)
        if iris_first and t < t0:
            r = r_log(2.2, 115, E_OUT(t / 0.42)) if t < 0.42 else 1e4
            return mix(img, B0, disc(CX, CY, r))
        dx, s, rad = container_state(t, t0)
        w, h = W * s, H * s
        m = _card_rect_mask(CX + dx, CY, w, h, min(rad, min(w, h) / 2))
        inner = affine(B0, s, dx=dx)
        out = mix(img, inner, m)
        if 0.3 < t - t0 < 1.0:
            for k in range(3):
                e = p_out(2)(c01((t - t0 - 0.3 - 0.12 * k) / 0.3))
                out = mix(out, solid(WORDC), box(150 + 4 * (1 - e), 30 + 22 * k, 40, 8) * e * c01((1.0 - (t - t0)) / 0.1))
        return out
    total = t0 + 1.4
    path, frs, ts = film(wd, name, frame, total, 50)
    left = XX < 125      # the metric boxes live at x >= 128; count the card left of them
    areas = [float(((bwt(f) > 0.5) & left).sum()) for f in frs]
    i_card = at(ts, t0 + 0.8)
    sel = (bwt(frs[i_card]) > 0.5) & (np.abs(XX - (CX - 36)) < W * 0.2) & (np.abs(YY - CY) < H * 0.2)
    s_m = scale_est(frs[i_card], sel) if sel.any() else float("nan")
    def model_area(t):
        dx_, s_, rad_ = container_state(t, t0)
        return float((_card_rect_mask(CX + dx_, CY, W * s_, H * s_, min(rad_, W * s_ / 2, H * s_ / 2)) > 0.5)[left].sum())
    k0 = at(ts, t0 + 0.02)
    jumps = max(abs(a - model_area(t)) / max(model_area(t), 0.01 * W * H) for a, t in zip(areas[k0:], ts[k0:]))
    dx, s, rad = container_state(ts[i_card] - t0)
    x0 = int(math.ceil(CX + dx - W * s / 2))
    y0 = int(math.ceil(CY - H * s / 2))
    corner = bwt(frs[i_card])[y0, x0] < 0.5 and bwt(frs[i_card])[y0 + 4, x0 + 4] > 0.5
    checks = [check("one container, never cut: every frame's card area follows the single-container path (rel err, floor 1% frame)", jumps < 0.05, jumps, "< 0.05"),
              near("footage shrinks into a card at scale 0.56", s_m, 0.56, 0.02),
              check("card corners rounded (44 css px)", bool(corner), bool(corner), True),
              check("metrics slide in beside the card", float((np.abs(frs[i_card] - WORDC).max(-1) < 3).sum()) > 600,
                    float((np.abs(frs[i_card] - WORDC).max(-1) < 3).sum()), "> 600"),
              check("implodes into the dot (area <= 2% x 2% of the frame + 3 px)", areas[-1] <= 0.0004 * W * H + 3, areas[-1],
                    "<= %.1f" % (0.0004 * W * H + 3))]
    if iris_first:
        i = at(ts, 0.2)
        checks.append(near("opens with an iris from the dot (log space, r at 0.2 s)", ray_len(frs[i], CX, CY, B0)[0],
                           r_log(2.2, 115, E_OUT(ts[i] / 0.42)), 1.0))
    checks.append(neg("card scale if the footage were cut to a new card", 1.0, 0.56, 0.02))
    return checks, path


def _footage_card(task, wd):
    c, p = _container_film(wd, "footage_card_implode", False)
    return c, [p, save_plan(wd, "container", {"card": "TRANS-238", "card": {"x": -360, "scale": 0.56, "radius": 44, "s": 0.66},
                                              "implode": {"scale": 0.02, "radius": 600, "s": 0.38}})]


def _showreel(task, wd):
    c, p = _container_film(wd, "iris_card_implode", True)
    return c, [p, save_plan(wd, "showreel", {"card": "TRANS-257", "iris": [22, 1150, 0.42]})]


card("TRANS-238")(_footage_card)
card("TRANS-257")(_showreel)

SHOTS3 = {"establishing": lambda u: (1.0, 0.0, 0.0), "low angle tracking": lambda u: (1.3, -2.0 - 20 * u, 6.0)}


def k3_sequence(items, seconds):
    def seq(t):
        cur = max((it for it in items if it["at"] <= t), key=lambda it: it["at"])
        return cur["shot"], t - cur["at"]
    return seq


def _shot_list(task, wd):
    seq = k3_sequence([{"at": 0, "shot": "establishing"}, {"at": 0.5, "shot": "low angle tracking"}], 1.2)

    def frame(t):
        shot, u = seq(t)
        s, dx, dy = SHOTS3[shot](u)
        return affine(A0, s, dx=dx, dy=dy)
    path, frs, ts = film(wd, "shot_list", frame, 1.2, 20)
    ic = at(ts, 0.5)
    pure = [affine(A0, *SHOTS3["establishing"](0)[:1]), ]
    blended = max(min(mad(f, affine(A0, SHOTS3[seq(t)[0]](seq(t)[1])[0], dx=SHOTS3[seq(t)[0]](seq(t)[1])[1],
                                       dy=SHOTS3[seq(t)[0]](seq(t)[1])[2])), 99) for f, t in zip(frs, ts))
    s_before, s_at = scale_est(frs[ic - 1]), scale_est(frs[ic])
    def anchor(f):   # pixel x where the source column CX now sits (camera position)
        band = (XX > 30) & (XX < W - 30) & (np.abs(YY - CY) < 20)
        a, b = np.polyfit(srcx(f)[band], XX[band], 1)
        return a * CX + b
    xs = [anchor(f) for f in frs[ic:]]
    return ([check("hard cut: scale jumps 1.0 -> 1.3 on the cut frame", abs(s_before - 1) < 0.01 and abs(s_at - 1.3) < 0.01,
                   [s_before, s_at], [1.0, 1.3]),
             check("no crossfades: every frame is exactly one shot's camera", blended < 0.6, blended, "< 0.6"),
             near("the tracking move starts at the cut (x speed px/s)", (xs[-1] - xs[0]) / (ts[-1] - ts[ic]), -20 * 1.0, 3.0),
             neg("scale on the cut frame without the shot list", scale_est(A0), 1.3, 0.01)],
            [path, save_plan(wd, "shot_list", {"card": "TRANS-256", "shots": ["establishing", "low angle tracking"], "cuts": [0.5]})])


card("TRANS-256")(_shot_list)


def keyword_plane(words, cut, keys):
    cands = [w for w in words if -0.8 <= w["t"] - cut <= 0.2]
    best = max(cands, key=lambda w: w["stress"] - 2.5 * abs(w["t"] - cut))
    kept = [k for k in keys if not (-1.2 <= k["t"] - best["t"] <= 0.6)]
    return best, kept


def _keyword(task, wd):
    words = [{"w": "we", "t": 1.0, "stress": 0.2}, {"w": "struggled", "t": 1.5, "stress": 1.0},
             {"w": "fought", "t": 1.9, "stress": 0.9}, {"w": "back", "t": 2.15, "stress": 0.5}, {"w": "hard", "t": 2.6, "stress": 1.4}]
    keys = [{"t": 0.5, "text": "A"}, {"t": 1.2, "text": "B"}, {"t": 2.3, "text": "C"}, {"t": 3.0, "text": "D"}]
    cut = 2.0
    best, kept = keyword_plane(words, cut, keys)
    naive = max(words, key=lambda w: w["stress"])
    _, a = text_layer(best["w"].upper(), size=40, color=(255, 255, 255))
    path, frs, ts = film(wd, "keyword_plane", lambda t: mix(A0 if t < cut else B0, solid((255, 255, 255)),
                                                          a * (abs(t - cut) < 0.2)), 2.6, 10)
    i = at(ts, cut)
    return ([check("strongest word near the cut wins: 'fought' (0.9 - 2.5 x 0.1)", best["w"] == "fought", best["w"], "fought"),
             check("candidates only in -0.8/+0.2 s ('hard' at +0.6 excluded)", "hard" != best["w"], best["w"], "not hard"),
             check("keys within -1.2/+0.6 s of the plane removed", [k["text"] for k in kept] == ["A", "D"], [k["text"] for k in kept],
                   ["A", "D"]),
             check("plane drawn on the cut and absent 0.3 s before", float((lum(frs[i]) > 250).mean()) > 0.03
                   and float((lum(frs[at(ts, cut - 0.3)]) > 250).mean()) == 0.0,
                   [float((lum(frs[i]) > 250).mean()), float((lum(frs[at(ts, cut - 0.3)]) > 250).mean())], "> 0.03 / 0"),
             neg("word chosen by stress alone", float(naive["w"] == best["w"]), 1.0, 0.0)],
            [path, save_plan(wd, "keyword", {"card": "TRANS-258", "chosen": best, "kept_keys": kept})])


card("TRANS-258")(_keyword)


def _poster_under(task, wd):
    leg = 1.0

    def frame(t):
        if t < leg:
            pg = t / leg
            po = c01((pg - 0.5) / 0.4)
            poster = affine(B0, 1 + 0.06 * pg)
            return mix(poster, A0, 1 - po)
        return affine(B0, 1.06 - 0.06 * c01((t - leg) / 0.5))
    path, frs, ts = film(wd, "poster_under", frame, 1.5, 30)
    i = at(ts, 0.75)
    ic = at(ts, leg)
    return ([near("poster fades in over the second half (opacity at 75%)", float(bwt(frs[i]).mean()), c01((ts[i] / leg - 0.5) / 0.4), 0.02),
             near("poster scaled 1 + 0.06 x progress at the end of the leg", scale_inv(frs[ic - 1]), 1 + 0.06 * ts[ic - 1], 0.01),
             check("swap invisible: last leg frame ~ first next-clip frame", mad(frs[ic - 1], frs[ic]) < 1.0, mad(frs[ic - 1], frs[ic]), "< 1"),
             neg("jump at the swap without the poster", mad(A0, affine(B0, 1.06)), 0.0, 1.0)],
            [path, save_plan(wd, "poster", {"card": "TRANS-260", "scale": 1.06})])


card("TRANS-260")(_poster_under)


def _quote_card(task, wd):
    rad = 24 * K * 2
    _, ta = text_layer("quote", size=16, color=(20, 20, 20))

    def st(t):
        veil = 0.7 * c01(t / 0.4) if t < 1.2 else 0.7 * (1 - c01((t - 1.6) / 0.4))
        card_s = p_out(2)(c01((t - 0.4) / 0.35)) if t < 1.4 else 1 - p_in(2)(c01((t - 1.4) / 0.35))
        txt = c01((t - 0.75) / 0.2) if t < 1.2 else 1 - c01((t - 1.2) / 0.2)
        return veil, card_s, txt

    def frame(t):
        veil, cs, txt = st(t)
        img = mix(A0, solid((255, 255, 255)), veil)
        if cs > 0.01:
            m = _card_rect_mask(CX, CY, 120 * cs, 50 * cs, rad * cs)
            img = mix(img, solid((255, 255, 255)), m)
            img = mix(img, solid((20, 20, 20)), ta * txt * (m > 0.99))
        return img
    path, frs, ts = film(wd, "quote_card", frame, 2.1, 20)
    i = at(ts, 0.5)
    corner = frs[at(ts, 1.0)][int(CY - 25), int(CX - 60)]
    tgone = at(ts, 1.4)
    tx = float((lum(frs[tgone]) < 60).sum())
    cs_at = st(ts[tgone])[1]
    return ([near("white veil to ~70% (corner pixel opacity)", overlay_alpha(frs[i][:5, :5], A0[:5, :5], (255, 255, 255)), 0.7, 0.03),
             check("rounded card (corner pixel shows the veil, not the card)", float(corner[2]) < 250 or float(corner[0]) < 250,
                   [float(x) for x in corner], "veil"),
             check("reverse order: text gone before the card shrinks", tx < 3 and cs_at > 0.95, [tx, cs_at], "text 0, card full"),
             check("scene restored at the end", mad(frs[-1], A0) < 0.5, mad(frs[-1], A0), "< 0.5"),
             neg("veil opacity on the bare scene", overlay_alpha(A0[:5, :5], A0[:5, :5], (255, 255, 255)), 0.7, 0.03)],
            [path, save_plan(wd, "quote", {"card": "TRANS-262", "veil_ms": 400, "card_ms": 350, "radius": 24})])


card("TRANS-262")(_quote_card)


def _hole_zoom(task, wd):
    hx, hy, r0 = 0.6 * W, 0.45 * H, 4.0
    k = math.log(40)

    def frame(t):
        s = math.exp(k * c01(t))
        img = affine(A0, s, cx=hx, cy=hy)
        return mix(img, B0, disc(hx, hy, r0 * s))
    path, frs, ts = film(wd, "zoom_hole", frame, 1.0, 30)
    rs = [ray_len(f, hx, hy)[0] for f in frs]
    sel = [i for i, r in enumerate(rs) if 4 < r < W - hx - 2]
    slope = float(np.polyfit([ts[i] for i in sel], np.log([rs[i] for i in sel]), 1)[0])
    return ([near("exponential scale s = e^(k t), 1 -> 40x in 1 s (d ln r / dt)", slope, k, 0.08 * k),
             check("next scene shows through the hole and covers the frame at the end", mad(frs[-1], B0) < 0.5, mad(frs[-1], B0), "< 0.5"),
             near("hole radius = r0 x s at 0.5 s", rs[at(ts, 0.5)], r0 * math.exp(k * 0.5), 1.0),
             neg("growth rate of a static hole", 0.0, k, 0.08 * k)],
            [path, save_plan(wd, "hole", {"card": "TRANS-263", "k": k, "hole": [hx, hy, r0]})])


card("TRANS-263")(_hole_zoom)


def _clouds(task, wd):
    rng = np.random.default_rng(9)
    sprites = [(rng.uniform(0.1, 0.9) * W, rng.uniform(0.15, 0.85) * H, rng.uniform(9, 14)) for _ in range(14)]
    swap = 0.5

    def cover(t):
        g = math.exp(1.6 * min(t, swap))          # clouds rush at the camera: grow g^2, drift outward
        a = np.zeros((H, W))
        for x, y, r in sprites:
            k = 1 + 0.25 * (g - 1)
            a = np.maximum(a, disc(CX + (x - CX) * k, CY + (y - CY) * k, r * g * g, 3.0 * g))
        fade = c01(t / 0.15) if t <= swap else c01(1 - (t - swap) / 0.4)
        return a * fade

    def frame(t):
        base = affine(A0, 1 + 0.6 * t) if t < swap else affine(B0, 1.3 - 0.3 * c01((t - swap) / 0.4))
        return mix(base, solid((255, 255, 255)), cover(t))
    path, frs, ts = film(wd, "cloud_fly", frame, 1.0, 30)
    ic = at(ts, swap)
    cov = float(np.mean(lum(frs[ic]) > 250))
    i_a = at(ts, 0.2)
    sel = cover(ts[i_a]) < 0.004     # measure through the gaps between clouds
    s_a = scale_est(frs[i_a], sel)
    return ([check("clouds cover the frame at the swap (> 90% white)", cov > 0.9, cov, "> 0.9"),
             check("camera change hidden: A visible before, only B after", fracb(frs[i_a], sel) < 0.05 and fracb(frs[-1]) > 0.99,
                   [fracb(frs[i_a], sel), fracb(frs[-1])], "< 0.05 / > 0.99"),
             near("map zooms while the clouds pass (scale of the visible map at 0.2 s)", s_a, 1 + 0.6 * ts[i_a], 0.02),
             check("clouds clear after the swap", float(np.mean(lum(frs[-1]) > 250)) < 0.01, float(np.mean(lum(frs[-1]) > 250)), "< 0.01"),
             neg("white coverage at the swap without clouds", float(np.mean(lum(affine(A0, 1.3)) > 250)), 1.0, 0.1)],
            [path, save_plan(wd, "clouds", {"card": "TRANS-264", "sprites": len(sprites), "swap_s": swap})])


card("TRANS-264")(_clouds)


def _film_strip(task, wd):
    speed, cw, gap = 200 * K, 34.0, 6.0

    def frame(t):
        img = solid((25, 25, 25))
        off = speed * t
        for k in range(-1, 8):
            x = k * (cw + gap) - off % (cw + gap) + 8
            n = k + int(off // (cw + gap))
            img = mix(img, solid(PAL5[n % 5]), box(x + cw / 2, CY, cw, 50))
            for j in range(4):
                img = mix(img, solid((235, 235, 235)), box(x + 4 + j * 9, CY - 31, 4, 4))
        return img
    path, frs, ts = film(wd, "film_strip", frame, 1.0, 20)

    row = int(round(CY - 31))

    def shift_of(f0, f1, maxs=15):
        r0, r1 = lum(f0)[row], lum(f1)[row]
        errs = [float(np.mean(np.abs(r1[:W - 20] - r0[sh:sh + W - 20]))) for sh in range(maxs)]
        return int(np.argmin(errs)), errs
    d, errs = shift_of(frs[0], frs[4])
    vis = sum(1 for k in range(-1, 8) if 0 <= k * (cw + gap) + 8 + cw / 2 <= W)
    return ([near("strip translates at 200 css px/s (sprocket-row shift in 0.2 s, px)", d, speed * 0.2, 1.0),
             check("4-5 frames visible", 4 <= vis <= 5, vis, "4..5"),
             check("cards show successive states (>= 4 distinct palette colours on the middle row)",
                   sum(1 for c in PAL5 if (np.abs(frs[0][int(CY)] - c).max(-1) < 3).any()) >= 4,
                   sum(1 for c in PAL5 if (np.abs(frs[0][int(CY)] - c).max(-1) < 3).any()), ">= 4"),
             neg("strip shift of a still frame", float(shift_of(frs[0], frs[0])[0]), speed * 0.2, 1.0)],
            [path, save_plan(wd, "film_strip", {"card": "TRANS-265", "speed_css_px_s": 200})])


card("TRANS-265")(_film_strip)


def _macro_words(task, wd):
    cuts = [0.0, 0.6, 1.4, 2.0, 2.8]
    scales = [6.0, 8.0, 10.0, 7.0]
    words = ["THIS", "IS", "ONE", "SENTENCE"]
    fields = [PAL5[1], PAL5[2], PAL5[3], PAL5[0]]
    las = [text_layer(w, size=14, color=(255, 255, 255), pos=(W / 2, H * 0.85))[1] for w in words]

    def frame(t):
        k = max(i for i, c in enumerate(cuts[:-1]) if t >= c - 1e-9)
        u = t - cuts[k]
        s = scales[k] * (1 + 0.05 * u)
        img = mix(solid(fields[k]), affine(A0, s), disc(CX, CY, 0.3 * W))
        return mix(img, solid((255, 255, 255)), las[k] * c01(u / 0.1))
    path, frs, ts = film(wd, "macro_words", frame, 2.8 - 1e-6, 40)
    det = cut_times(frs, ts)
    iv = np.diff([0.0] + det)
    sel = disc(CX, CY, 0.2 * W) > 0.99
    s_m = [scale_est(frs[at(ts, c + 0.05)], sel) for c in cuts[:-1]]
    push = scale_est(frs[at(ts, 0.55)], sel) > scale_est(frs[at(ts, 0.05)], sel)
    j = at(ts, 0.6 + 0.05)
    reg = las[1] > 0.99
    a = overlay_alpha(frs[j][reg][None], (affine(A0, scales[1] * (1 + 0.05 * (ts[j] - 0.6))) if True else A0)[reg][None],
                      (255, 255, 255)) if reg.any() else float("nan")
    return ([check("cut every 0.5-1 s", len(det) == 3 and all(0.5 <= x <= 1.0 for x in iv), [float(x) for x in iv], "0.5..1"),
             check("extreme close-ups at 6-10x", all(5.8 <= x <= 10.6 for x in s_m), s_m, "6..10"),
             check("slow push during the shot", push, push, True),
             near("one word per cut, 100 ms fade (alpha at 50 ms)", a, c01((ts[j] - 0.6) / 0.1), 0.08),
             neg("scale of an un-zoomed drawing", scale_est(A0, sel), 8.0, 2.2)],
            [path, save_plan(wd, "macro", {"card": "TRANS-270", "cuts": cuts, "scales": scales})])


card("TRANS-270")(_macro_words)


def _halftone_ring(task, wd):
    cell = 8.0
    ccx, ccy = (XX // cell + 0.5) * cell, (YY // cell + 0.5) * cell
    dc = np.hypot(ccx - CX, ccy - CY)
    D, band = 0.6, 20.0
    Rm = math.hypot(W, H) / 2 + band

    def frame(t):
        R = Rm * p_io(1)(t / D)
        rdot = np.clip((R - dc) / band, 0, 1) * cell * 0.75
        m = (np.hypot(XX - ccx, YY - ccy) < rdot) | (dc < R - band)
        return np.where(m[..., None], B0, A0)
    path, frs, ts = film(wd, "halftone_ring", frame, D, 30)
    i = at(ts, 0.3)
    R = Rm * p_io(1)(ts[i] / D)
    bw = bwt(frs[i]) > 0.5
    inner = float(bw[dc < R - band - 6].mean()) if (dc < R - band - 6).any() else 1.0
    ring = (dc > R - band) & (dc < R)
    near_r = float(bw[ring & (dc < R - band / 2)].mean())
    far_r = float(bw[ring & (dc >= R - band / 2)].mean())
    return ([check("window inside the ring fully open", inner > 0.99, inner, "> 0.99"),
             check("dots shrink with distance across the ring (radial scale gradient)", near_r > far_r, [near_r, far_r], "near > far"),
             check("ends on scene B", mad(frs[-1], B0) < 0.5, mad(frs[-1], B0), "< 0.5"),
             neg("ring gradient on the bare scene", float((bwt(A0) > 0.5)[ring].mean()), 0.5, 0.45)],
            [path, save_plan(wd, "halftone_ring", {"card": "TRANS-272", "cell": cell, "band": band})])


card("TRANS-272")(_halftone_ring)


def _leader(task, wd):
    nums = 3
    fps = 30
    digits = [text_layer(str(n), size=40, color=(30, 30, 30))[1] for n in range(nums, 0, -1)]

    def frame(t):
        if t >= nums:
            return solid((255, 255, 255))
        k = int(t)
        ang = 2 * math.pi * (t - k)
        img = solid((200, 200, 200))
        img[(ANG < ang)] = 140
        ring = np.hypot(XX - CX, YY - CY)
        img[(np.abs(ring - 40) < 0.8) | (np.abs(ring - 34) < 0.8)] = 30
        img[(np.abs(XX - CX) < 0.6) | (np.abs(YY - CY) < 0.6)] = 30
        return mix(img, solid((30, 30, 30)), digits[k])
    path, frs, ts = film(wd, "leader", frame, nums + 2.5 / fps, fps)
    i = at(ts, 1.25)
    sec = (np.hypot(XX - CX, YY - CY) > 10) & (np.hypot(XX - CX, YY - CY) < 30) & (np.abs(XX - CX) > 2) & (np.abs(YY - CY) > 2)
    wedge = (np.abs(frs[i] - 140).max(-1) < 2) & sec
    edge = math.degrees(float(ANG[wedge].max())) if wedge.any() else 0.0
    chg = [ts[j] for j in range(1, len(frs)) if ts[j] < nums and mad(frs[j][:, int(CX) - 12:int(CX) + 12] * 0 + frs[j][int(CY) - 15:int(CY) + 15].mean(), 0) < -1]
    whites = sum(1 for f in frs if float(lum(f).mean()) > 250)
    numeral_change = all(mad(frs[at(ts, k + 0.5)][int(CY) - 15:int(CY) + 15], frs[at(ts, k + 1.5)][int(CY) - 15:int(CY) + 15]) > 1
                         for k in range(nums - 1))
    return ([near("wedge sweeps 360 deg per second (angle at 1.25 s)", edge, 360.0 * (ts[i] - 1), 6.0),
             check("numeral swaps each sweep", numeral_change, numeral_change, True),
             check("ends on a 2-3 frame white flash", 2 <= whites <= 3, whites, "2..3"),
             neg("wedge angle of a still leader", 0.0, 90.0, 6.0)],
            [path, save_plan(wd, "leader", {"card": "TRANS-276", "numbers": nums, "sweep_deg_s": 360})])


card("TRANS-276")(_leader)


def _speed_lines(task, wd):
    D = 0.8
    ang = np.arctan2(YY - CY, XX - CX)
    lines = (np.abs(((ang / (2 * np.pi) * 24) % 1) - 0.5) < 0.08)

    def frame(t):
        e = p_in(2)(t / D)
        img = affine(A0, 1 + 3 * e)
        img = np.where((lines & (np.hypot(XX - CX, YY - CY) > 60 * (1 - e) + 5))[..., None], np.array([40.0, 40, 40]), img)
        return mix(img, solid((255, 255, 255)), c01((e - 0.6) / 0.4))
    path, frs, ts = film(wd, "speed_lines", frame, D, 30)
    i = at(ts, 0.4)
    e = p_in(2)(ts[i] / D)
    sel = np.hypot(XX - CX, YY - CY) < 20
    return ([near("object scales up on an ease-in (scale at 0.4 s)", scale_est(frs[i], sel), 1 + 3 * e, 0.03),
             check("radial lines converge (more line pixels late than early)",
                   float((np.abs(frs[at(ts, 0.6)] - 40).max(-1) < 2).sum()) > float((np.abs(frs[at(ts, 0.2)] - 40).max(-1) < 2).sum()),
                   True, True),
             check("white-out at the end", float(lum(frs[-1]).min()) > 250, float(lum(frs[-1]).min()), "> 250"),
             neg("scale at 0.4 s without the zoom", scale_est(A0, sel), 1 + 3 * e, 0.03)],
            [path, save_plan(wd, "speed_lines", {"card": "TRANS-277", "ms": 800, "ease": "ease-in"})])


card("TRANS-277")(_speed_lines)


# ═════════════════════ FLIP, tiles, dither and chart handoffs ═════════════════════
def bbox_of(fr, col, tol=3):
    m = np.abs(fr - np.asarray(col, float)).max(-1) < tol
    if not m.any():
        return (float("nan"),) * 4
    ys, xs = np.nonzero(m)
    return float(xs.min()), float(xs.max()), float(ys.min()), float(ys.max())


def _flip_grid(task, wd):
    D = 0.8
    ease = p_io(2)
    first = [(48.0, 27.0), (144.0, 27.0), (48.0, 81.0), (144.0, 81.0)]
    gw, gh, pw, ph = 80.0, 44.0, 40.0, 80.0

    def rect(k, t):     # FLIP: last rect = phone, invert to first, play the inverse transform back to identity
        e = ease(t / D)
        (fx0, fy0) = first[k]
        return fx0 + (CX - fx0) * e, fy0 + (CY - fy0) * e, gw + (pw - gw) * e, gh + (ph - gh) * e

    def frame(t):
        img = solid(BG)
        for k in range(4):
            cx, cy, w, h = rect(k, t)
            img = mix(img, solid(PAL5[k]), box(cx, cy, w, h))
        return img
    path, frs, ts = film(wd, "flip_grid_phone", frame, D, 40)
    i = at(ts, 0.4)
    x0, x1, y0, y1 = bbox_of(frs[i], PAL5[3])
    cx, cy, w, h = rect(3, ts[i])
    start_areas = [float((np.abs(frs[0] - PAL5[k]).max(-1) < 3).sum()) for k in range(4)]
    end = [float((np.abs(frs[-1] - PAL5[k]).max(-1) < 3).sum()) for k in range(4)]
    return ([check("starts as a 2x2 grid of windows (each ~80x44 px)", all(abs(a - gw * gh) < 0.06 * gw * gh for a in start_areas),
                   start_areas, gw * gh),
             near("mid-flight window width follows the FLIP ease (px)", x1 - x0 + 1, w, 1.5),
             near("mid-flight window height follows the FLIP ease (px)", y1 - y0 + 1, h, 1.5),
             near("mid-flight window centre x (px)", (x0 + x1) / 2, cx, 1.0),
             check("ends as one phone screen (top window 40x80, others hidden)",
                   abs(end[3] - pw * ph) < 0.06 * pw * ph and sum(end[:3]) == 0, end, [0, 0, 0, pw * ph]),
             neg("phone-rect area of the un-animated grid", float((np.abs(frs[0] - PAL5[3]).max(-1) < 3).sum()), pw * ph, 0.06 * pw * ph)],
            [path, save_plan(wd, "flip", {"card": "TRANS-280", "ms": 800, "grid": first, "phone": [pw, ph]})])


card("TRANS-280")(_flip_grid)

BAYER4 = (np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) + 0.5) / 16.0


def bayer(px=2):
    return BAYER4[(YY // px).astype(int) % 4, (XX // px).astype(int) % 4]


ORANGE = np.array([255.0, 120.0, 0.0])
GREY = np.array([60.0, 60.0, 60.0])


def _seg_toggle(task, wd):
    D, band = 0.3, 20.0
    segs = [(36.0, 96.0), (96.0, 156.0)]          # seg 0 and seg 1 x-ranges (seg 2 = 156..186 stays grey)
    th = bayer(2)
    rows = np.abs(YY - CY) < 12
    in0 = rows & (XX >= segs[0][0]) & (XX < segs[0][1])
    in1 = rows & (XX >= segs[1][0]) & (XX < segs[1][1])
    in2 = rows & (XX >= 156) & (XX < 186)

    def p_at(t):
        xf = segs[0][0] + (segs[1][1] + band - segs[0][0]) * p_io(2)(t / D)
        return np.clip((xf - XX) / band, 0, 1), xf

    def frame(t):
        p, _ = p_at(t)
        img = solid(BG)
        on = (in0 & (th >= p)) | (in1 & (th < p))
        img[in0 | in1 | in2] = GREY
        img[on] = ORANGE
        return img
    path, frs, ts = film(wd, "dither_toggle", frame, D, 50)
    i = at(ts, 0.15)
    p, xf = p_at(ts[i])
    seg = in0 | in1
    f = frs[i]
    binary = float(np.mean((np.abs(f[seg] - ORANGE).max(-1) < 3) | (np.abs(f[seg] - GREY).max(-1) < 3)))
    bandm = seg & (p > 0.05) & (p < 0.95)
    on_exp = (in0 & (th >= p)) | (in1 & (th < p))
    frac = float(np.mean(np.abs(f[bandm] - ORANGE).max(-1) < 3)) if bandm.any() else float("nan")
    frac_exp = float(np.mean(on_exp[bandm])) if bandm.any() else float("nan")
    end1 = float(np.mean(np.abs(frs[-1][in1] - ORANGE).max(-1) < 3))
    end0 = float(np.mean(np.abs(frs[-1][in0] - GREY).max(-1) < 3))
    xfade = mix(solid(GREY), solid(ORANGE), 0.5)[seg]
    neg_bin = float(np.mean((np.abs(xfade - ORANGE).max(-1) < 3) | (np.abs(xfade - GREY).max(-1) < 3)))
    return ([check("starts with segment 0 orange", float(np.mean(np.abs(frs[0][in0] - ORANGE).max(-1) < 3)) == 1.0,
                   float(np.mean(np.abs(frs[0][in0] - ORANGE).max(-1) < 3)), 1.0),
             check("mid-switch pixels are binary (ordered dither, no blended colours)", binary == 1.0, binary, 1.0),
             near("dither density in the wipe band equals the Bayer threshold count", frac, frac_exp, 0.01),
             check("ends with segment 1 orange and segment 0 grey", end1 == 1.0 and end0 == 1.0, [end1, end0], [1, 1]),
             neg("binary-pixel share of a plain 50% crossfade", neg_bin, 1.0, 0.01)],
            [path, save_plan(wd, "toggle", {"card": "TRANS-281", "ms": 300, "band_px": band, "bayer": "4x4, 2 px cells"})])


card("TRANS-281")(_seg_toggle)

TILE_C = (W * 5 / 6, H / 6)


def tile_frame(e, r_screen, grid_alpha=1.0, blur_s=0.0):
    """Camera zoom e (0 = 3x3 grid, 1 = selected tile full-bleed), rendered straight from the sources (one resample)."""
    Z = 1 + 2 * e
    T = (CX + (TILE_C[0] - CX) * e, CY + (TILE_C[1] - CY) * e)
    grid = solid(BG)
    sel = None
    for r in range(3):
        for c in range(3):
            tc = (W * (2 * c + 1) / 6, H * (2 * r + 1) / 6)
            sx, sy = CX + (tc[0] - T[0]) * Z, CY + (tc[1] - T[1]) * Z
            tw, th_ = (W / 3 - 4) * Z, (H / 3 - 4) * Z
            if c == 2 and r == 0:
                tw, th_ = W / 3 * Z + 4 * (Z - 1) / 2, H / 3 * Z + 4 * (Z - 1) / 2    # selected tile grows to full bleed
                sel = (sx, sy, tw, th_)
                continue
            m = _card_rect_mask(sx, sy, tw, th_, min(r_screen, tw / 2, th_ / 2)) * grid_alpha
            grid = mix(grid, affine(A0, Z / 3, dx=sx - CX, dy=sy - CY), m)
    sx, sy, tw, th_ = sel
    m = _card_rect_mask(sx, sy, tw, th_, min(r_screen, tw / 2, th_ / 2))
    out = mix(grid, affine(B0, Z / 3, dx=sx - CX, dy=sy - CY), m)
    return blur(out, blur_s) if blur_s > 0.05 else out


def _whip_tile(task, wd):
    D = 0.5
    ease = p_io(3)

    def st(t):
        e = ease(t / D)
        return e, 12.0 * (1 - e), 20 * K * math.sin(math.pi * c01(t / D))

    def frame(t):
        if t > D:
            return B0.copy()      # full-res clip starts with a matching offset (identity at hand-off)
        e, rad, bl = st(t)
        return tile_frame(e, rad, blur_s=bl)
    path, frs, ts = film(wd, "whip_tile", frame, D + 0.2, 40)
    i1 = at(ts, 0.15)
    e1 = st(ts[i1])[0]
    selm = (bwt(frs[i1]) > 0.98)
    s_m = scale_est(frs[i1], selm & (np.abs(XX - CX) < 50))
    def fit_sigma(j):
        e_, rad_, _ = st(ts[j])
        clean = tile_frame(e_, rad_)
        cands = np.arange(0, 3.01, 0.1)
        return float(cands[int(np.argmin([mad(frs[j], blur(clean, c)) for c in cands]))])
    probes = [at(ts, t) for t in (0.05, 0.12, 0.25)]
    sh = [fit_sigma(j) for j in probes]
    sh_exp = [st(ts[j])[2] for j in probes]
    iD = at(ts, D)
    e_m, rad_m, _ = st(ts[at(ts, 0.3)])
    held = tile_frame(1.0, 12.0)
    return ([near("camera zoom follows the ease (content scale = (1 + 2e)/3 at 0.15 s)", s_m, (1 + 2 * e1) / 3, 0.02),
             check("zoom blur ramps to its 20 css px peak at mid-move (fitted sigma at 0.05/0.12/0.25 s)",
                   all(abs(a - b) <= 0.2 for a, b in zip(sh, sh_exp)) and sh[0] < sh[1] < sh[2], sh, [round(x, 2) for x in sh_exp]),
             check("radius reaches 0 and the last zoom frame equals the full-res clip", mad(frs[iD], B0) < 0.5, mad(frs[iD], B0), "< 0.5"),
             check("hand-off seamless: last zoom frame ~ first clip frame", mad(frs[iD], frs[iD + 1]) < 0.5, mad(frs[iD], frs[iD + 1]), "< 0.5"),
             neg("end frame vs clip if the 12 px radius were kept (corners show the grid)", mad(held, B0), 0.0, 0.05)],
            [path, save_plan(wd, "whip", {"card": "TRANS-282", "ms": 500, "radius_px": [12, 0],
                                          "blur_peak_css_px": 20, "note": "radius in fixture px so the corner is measurable"})])


card("TRANS-282")(_whip_tile)


def _tile_return(task, wd):
    D = 0.6
    ease = p_io(2)

    def frame(t):
        e = 1 - ease(t / D)
        return tile_frame(e, 12.0 * (1 - e), grid_alpha=1 - e)
    path, frs, ts = film(wd, "match_back", frame, D, 40)
    i = at(ts, 0.3)
    e = 1 - ease(ts[i] / D)
    full = tile_frame(e, 12.0 * (1 - e), grid_alpha=1.0)
    none_ = tile_frame(e, 12.0 * (1 - e), grid_alpha=0.0)
    reg = np.abs(full - none_).max(-1) > 30
    a = float(np.sum((frs[i] - none_)[reg] * (full - none_)[reg]) / np.sum((full - none_)[reg] ** 2)) if reg.any() else float("nan")
    x0, x1, y0, y1 = bbox_of(frs[-1], np.array([0, 0, 0]) * 0 + np.nan) if False else (0, 0, 0, 0)
    b = bwt(frs[-1]) > 0.5
    ys, xs = np.nonzero(b)
    bx = (float(xs.min() + xs.max()) / 2, float(ys.min() + ys.max()) / 2, float(xs.max() - xs.min() + 1))
    s_mid = scale_est(frs[i], (bwt(frs[i]) > 0.98) & (np.abs(XX - CX) < 50))
    return ([check("starts as the playing full-bleed clip", mad(frs[0], B0) < 0.5, mad(frs[0], B0), "< 0.5"),
             near("clip scales down on ease-in-out (content scale at 0.3 s)", s_mid, (1 + 2 * e) / 3, 0.02),
             near("grid fades in around it (opacity at 0.3 s, regression)", a, 1 - e, 0.04),
             check("lands in its grid tile (centre and width)", abs(bx[0] - TILE_C[0]) < 1.5 and abs(bx[1] - TILE_C[1]) < 1.5
                   and abs(bx[2] - W / 3) < 2, bx, [TILE_C[0], TILE_C[1], W / 3]),
             neg("grid opacity on the first frame", float(np.sum((frs[0] - none_)[reg] * (full - none_)[reg]) / np.sum((full - none_)[reg] ** 2)),
                 1 - e, 0.04)],
            [path, save_plan(wd, "match_back", {"card": "TRANS-283", "ms": 600, "ease": "inOut(2)"})])


card("TRANS-283")(_tile_return)


def _eink(task, wd):
    D, band, px = 0.4, 0.15 * W, 2
    th = bayer(px)
    old = mix(solid((228, 228, 228)), solid((10, 10, 10)), text_layer("OLD TEXT", size=34)[1])
    new = mix(solid((250, 250, 250)), solid((10, 10, 10)), text_layer("NEW WORDS", size=34)[1])
    diff = np.abs(old - new).max(-1) > 5
    PH = [0.0, 0.37, 0.74, 0.11, 0.48, 0.85, 0.22, 0.59, 0.96, 0.33, 0.7, 0.07, 0.44, 0.81, 0.18, 0.55, 0.92, 0.29, 0.66, 0.03, 0.4]

    def xf(t):
        return -band + (W + 2 * band) * c01(t / D)

    def frame_i(i, t):
        p = np.clip((xf(t) - XX) / band, 0, 1)
        inb_ = (p > 0) & (p < 1)
        thr = (th + PH[i % len(PH)] * inb_) % 1.0
        flk = inb_ & (np.random.default_rng(100 + i).random((H, W)) < 0.4 * (1 - p))   # front pixels flicker, settle as p -> 1
        return np.where(((thr < p) ^ flk)[..., None], new, old)
    fps = 50
    n = int(round(D * fps)) + 1
    path = write_video([frame_i(i, i / fps) for i in range(n)], Path(wd) / "eink_wipe.mp4", fps)
    frs = fx.frames(path, (W, H))
    ts = [i / fps for i in range(n)]
    i = at(ts, 0.2)
    p = np.clip((xf(ts[i]) - XX) / band, 0, 1)
    f = frs[i]
    is_new = np.abs(f - new).max(-1) < 3
    is_old = np.abs(f - old).max(-1) < 3
    behind, ahead, inb = diff & (p >= 1), diff & (p <= 0), diff & (p > 0) & (p < 1)
    flips = 0
    for j in range(5, n - 5):
        pj = np.clip((xf(ts[j]) - XX) / band, 0, 1)
        nj = np.abs(frs[j] - new).max(-1) < 3
        nk = np.abs(frs[j + 1] - new).max(-1) < 3
        flips += int((nj & ~nk & diff & (pj > 0)).sum())
    xfade = mix(old, new, 0.5)
    return ([check("behind the band settled on the new text", float(is_new[behind].mean()) == 1.0, float(is_new[behind].mean()), 1.0),
             check("ahead of the band still the old text", float(is_old[ahead].mean()) == 1.0, float(is_old[ahead].mean()), 1.0),
             check("band pixels are binary old/new (ordered dither)", float((is_new | is_old)[inb].mean()) == 1.0,
                   float((is_new | is_old)[inb].mean()), 1.0),
             near("share of new pixels in the band ~ p + q(1 - 2p), q = 0.4(1 - p)", float(is_new[inb].mean()),
                  float(np.mean(p[inb] + 0.4 * (1 - p[inb]) * (1 - 2 * p[inb]))), 0.05),
             check("pixels flicker back new -> old before settling", flips > 50, flips, "> 50"),
             check("ends fully on the new text", mad(frs[-1], new) < 0.5, mad(frs[-1], new), "< 0.5"),
             neg("binary share of a 50% crossfade in the band", float(((np.abs(xfade - new).max(-1) < 3) | (np.abs(xfade - old).max(-1) < 3))[inb].mean()),
                 1.0, 0.01)],
            [path, save_plan(wd, "eink", {"card": "TRANS-288", "band": "15% frame", "ms": 400, "pixel_px": px})])


card("TRANS-288")(_eink)


def _shared_art(task, wd):
    D1, D2 = 0.6, 0.4
    thumb, hero = (30.0, 22.0, 24.0), (CX, CY, 70.0)
    DET = np.array([235.0, 235.0, 235.0])

    def art_rect(t):
        e = p_out(3)(t / D1)
        x = thumb[0] + (hero[0] - thumb[0]) * e
        y = thumb[1] + (hero[1] - thumb[1]) * e
        sz = thumb[2] + (hero[2] - thumb[2]) * e
        if t > D1:
            x = hero[0] + (60 - hero[0]) * p_out(3)((t - D1) / D2)
        return x, y, sz

    def frame(t):
        x, y, sz = art_rect(t)
        img = solid(BG)
        img = mix(img, affine(A0, sz / W, sy_=sz / H, dx=x - CX, dy=y - CY), box(x, y, sz, sz))
        if t > D1:
            r = p_out(3)((t - D1) / D2)
            for k in range(3):
                img = mix(img, solid(DET), box(140 + 8 * (1 - r), 36 + 14 * k, 50, 6) * r)
        return img
    path, frs, ts = film(wd, "shared_element", frame, D1 + D2, 40)
    i = at(ts, 0.3)
    x, y, sz = art_rect(ts[i])
    m = np.abs(frs[i] - BG).max(-1) > 4
    ys, xs = np.nonzero(m)
    w_m = float(xs.max() - xs.min() + 1)
    inside = box(x, y, sz - 2, sz - 2) > 0.99
    span = (float(srcx(frs[i])[inside].min()), float(srcx(frs[i])[inside].max()))
    det0 = float((np.abs(frs[at(ts, 0.5)] - DET).max(-1) < 3).sum())
    det1 = float((np.abs(frs[-1] - DET).max(-1) < 3).sum())
    me = np.abs(frs[-1] - BG).max(-1) > 4
    me &= XX < 110
    ys2, xs2 = np.nonzero(me)
    return ([near("artwork size follows easeOutQuart at 0.3 s (px)", w_m, sz, 1.5),
             check("same artwork, rescaled (source x spans the whole picture)", span[0] < 0.08 * W and span[1] > 0.92 * W, span, "0..W"),
             near("then slides left to x 60 (centre px)", float(xs2.min() + xs2.max()) / 2, 60.0, 1.0),
             check("details reveal on the right only after the expand", det0 == 0 and det1 > 700, [det0, det1], [0, "> 700"]),
             neg("size at 0.3 s of the unmoved thumbnail", thumb[2], sz, 1.5)],
            [path, save_plan(wd, "shared", {"card": "TRANS-289", "ms": [600, 400], "ease": "easeOutQuart"})])


card("TRANS-289")(_shared_art)


def _light_bar(task, wd):
    D = 0.7
    after = A0.copy()
    before = blur(mix(A0, solid(lum(A0).mean()[None].repeat(3) if False else (128, 128, 128)), 0.7), 2.0)
    for (x, y) in [(150, 30), (120, 80), (170, 70)]:
        before[(np.abs(np.abs(XX - x) - np.abs(YY - y)) < 0.8) & (np.abs(XX - x) < 5)] = (230, 30, 30)
    RED = np.array([230.0, 30.0, 30.0])
    bw, glow = 8 * K, 40 * K

    def xb(t):
        return W * c01(t / D)

    def frame(t):
        x = xb(t)
        img = np.where((XX < x)[..., None], after, before)
        g = np.exp(-0.5 * ((XX - x) / (glow / 2)) ** 2) * 0.6 + box(x, CY, bw, 2 * H)
        return screen(img, solid((255, 255, 240)) * np.clip(g, 0, 1)[..., None])
    path, frs, ts = film(wd, "light_bar", frame, D, 40)
    i = at(ts, 0.35)
    x = xb(ts[i])
    left, right = XX < x - 8, XX > x + 8
    col = lum(frs[i]).mean(0)
    pk = float(np.argmax(col))
    reds = [(np.abs(frs[i] - RED).max(-1) < 30)[XX < x - 8].sum(), (np.abs(frs[i] - RED).max(-1) < 30)[XX > x + 8].sum()]
    return ([check("left of the bar shows the improved 'after'", mad(frs[i][left], after[left]) < 0.6, mad(frs[i][left], after[left]), "< 0.6"),
             check("right of the bar still the grey blurred 'before'", mad(frs[i][right], before[right]) < 0.6, mad(frs[i][right], before[right]), "< 0.6"),
             near("glowing bar sits at the sweep position (brightest column)", pk, x, 1.0),
             check("red X issues only on the not-yet-swept side", reds[0] == 0 and reds[1] > 5, [int(r) for r in reds], [0, "> 5"]),
             check("ends on the 'after' state", mad(frs[-1][:, :W - 8], after[:, :W - 8]) < 0.6, mad(frs[-1][:, :W - 8], after[:, :W - 8]), "< 0.6"),
             neg("left region of the unswept card vs 'after'", mad(before[left], after[left]), 0.0, 0.6)],
            [path, save_plan(wd, "light_bar", {"card": "TRANS-291", "ms": 700, "bar_css_px": 8, "glow_css_px": 40})])


card("TRANS-291")(_light_bar)


def _growth_arrow(task, wd):
    T1, T2 = 1.2, 0.4
    pts = np.array([[20, 90], [50, 80], [80, 84], [110, 60], [140, 50], [170, 22]], float)
    seg = np.hypot(*np.diff(pts, axis=0).T)
    cum = np.concatenate([[0], np.cumsum(seg)])
    LINE, DOT, ARR, AREA = np.array([240.0, 240, 240]), np.array([255.0, 220, 0]), np.array([255.0, 100, 0]), np.array([0.0, 180, 120])
    LOGO = (40.0, 30.0)

    def tip(L):
        k = min(int(np.searchsorted(cum, L, side="right") - 1), len(seg) - 1)
        u = (L - cum[k]) / seg[k]
        p = pts[k] + (pts[k + 1] - pts[k]) * u
        d = (pts[k + 1] - pts[k]) / seg[k]
        return p, d

    def arrow(p, d, size):
        n = np.array([-d[1], d[0]])
        rel = np.stack([XX - p[0], YY - p[1]], -1)
        a, b = rel @ d, rel @ n
        return ((a <= 0) & (a >= -size) & (np.abs(b) <= (a + size) * 0.6)).astype(float)

    def frame(t):
        img = solid(BG)
        L = cum[-1] * p_io(1)(t / T1)
        if t < T1 + T2 or True:
            for k in range(len(seg)):
                if cum[k] >= L:
                    break
                q1 = pts[k] + (pts[k + 1] - pts[k]) * min(1, (L - cum[k]) / seg[k])
                xs = (XX >= pts[k][0]) & (XX <= q1[0])
                yl = pts[k][1] + (pts[k + 1][1] - pts[k][1]) * (XX - pts[k][0]) / (pts[k + 1][0] - pts[k][0])
                under = xs & (YY > yl + 1.5) & (YY < 100)
                img = mix(img, solid(AREA), under * (0.25 + 0.5 * (100 - YY) / 80))
                d = np.abs((XX - pts[k][0]) * (pts[k + 1][1] - pts[k][1]) - (YY - pts[k][1]) * (pts[k + 1][0] - pts[k][0])) / seg[k]
                img = mix(img, solid(LINE), (d < 1.0) & xs)
            for k, c in enumerate(cum):
                if c <= L + 1e-6:
                    img = mix(img, solid(DOT), disc(*pts[k], 2.5))
        p, d = tip(min(L, cum[-1] - 1e-6))
        if t > T1:
            e = p_io(2)((t - T1) / T2)
            p = p + (np.array(LOGO) - p) * e
            img = mix(img, solid((30, 60, 200)), box(LOGO[0] + 14, LOGO[1], 16, 12) * c01((t - T1) / T2))
            return mix(img, solid(ARR), arrow(p, d, 7 + 3 * e))
        return mix(img, solid(ARR), arrow(p, d, 7))
    path, frs, ts = film(wd, "growth_arrow", frame, T1 + T2, 40)
    i = at(ts, 0.6)
    L = cum[-1] * p_io(1)(ts[i] / T1)
    linex = np.nonzero((np.abs(frs[i] - LINE).max(-1) < 3).any(0))[0]
    dots = int(sum(1 for k, c in enumerate(cum) if (np.abs(frs[i][int(pts[k][1]), int(pts[k][0])] - DOT).max() < 3)))
    j = at(ts, T1 + T2 / 2)
    ax, ay, _ = centroid(frs[j], ARR, 40)
    p_end, d_end = tip(cum[-1] - 1e-6)
    e = p_io(2)((ts[j] - T1) / T2)
    ref = arrow(p_end + (np.array(LOGO) - p_end) * e, d_end, 7 + 3 * e)
    rx, ry = float((ref * XX).sum() / ref.sum()), float((ref * YY).sum() / ref.sum())
    ex, ey, _ = centroid(frs[-1], ARR, 40)
    refe = arrow(np.array(LOGO), d_end, 10)
    rex, rey = float((refe * XX).sum() / refe.sum()), float((refe * YY).sum() / refe.sum())
    col = frs[at(ts, T1)][:, 60]
    ar = [float(col[y][1]) for y in (86, 96)]
    return ([near("line drawn to the eased length at 0.6 s (tip x px)", float(linex.max()), tip(L)[0][0], 2.5),
             check("node dots shown for reached months", dots == int((cum <= L + 1e-6).sum()), dots, int((cum <= L + 1e-6).sum())),
             check("gradient area under the line (green brighter near the line)", ar[0] > ar[1] + 5, ar, "upper > lower"),
             near("arrowhead mid-flight on the eased path (centroid x)", ax, rx, 1.0),
             near("arrowhead mid-flight (centroid y)", ay, ry, 1.0),
             check("arrow becomes the logo's arrow", abs(ex - rex) < 1 and abs(ey - rey) < 1, [ex, ey], [rex, rey]),
             neg("arrow position on the chart's last frame vs the logo", math.hypot(*(p_end - np.array(LOGO))), 0.0, 1.0)],
            [path, save_plan(wd, "growth", {"card": "TRANS-292", "chart_s": T1, "fly_s": T2, "points": pts.tolist()})])


card("TRANS-292")(_growth_arrow)


def _blur_dissolve(task, wd):
    D = 0.4
    out_el = mix(solid(BG), A0, box(CX - 30, CY, 70, 50))
    in_el = mix(solid(BG), B0, box(CX + 30, CY, 70, 50))
    ease = p_out(2)
    smax = 12 * K * 2

    def comp(e, so, si):
        a = blur(out_el, so)
        b = blur(in_el, si)
        return a * (1 - e) + b * e

    def frame(t):
        e = ease(t / D)
        return comp(e, smax * e, smax * (1 - e))
    path, frs, ts = film(wd, "blur_dissolve", frame, D, 50)
    i = at(ts, 0.08)
    e = ease(ts[i] / D)
    exp = np.round(comp(e, smax * e, smax * (1 - e)))       # 8-bit like the encoded frame
    sharp0 = np.round(comp(e, 0, 0))
    both = [t for f, t in zip(frs, ts) if 0.05 < float(bwt(f)[np.abs(YY - CY) < 20].max()) < 0.95 or
            (float(bwt(f)[:, :int(CX - 30)].mean()) < 0.5 < float(bwt(f).max()) and 0 < t < D)]
    return ([check("mid frame equals the blur+opacity composite (out 0->12, in 12->0, ease-out cubic)", mad(frs[i], exp) < 0.6,
                   mad(frs[i], exp), "< 0.6"),
             near("sharpness matches the analytic blur composite", sharp(frs[i]), sharp(exp), 0.1 * sharp(exp)),
             check("starts sharp on the outgoing, ends sharp on the incoming", mad(frs[0], out_el) < 0.5 and mad(frs[-1], in_el) < 0.5,
                   [mad(frs[0], out_el), mad(frs[-1], in_el)], "< 0.5"),
             check("overlap spans the 400 ms (both visible on every inner frame)", len(both) >= len(frs) - 2, len(both), ">= %d" % (len(frs) - 2)),
             neg("sharpness of an unblurred crossfade vs the composite", sharp(sharp0), sharp(exp), 0.1 * sharp(exp))],
            [path, save_plan(wd, "blur_dissolve", {"card": "TRANS-296", "blur_css_px": 12, "ms": 400, "ease": "out cubic"})])


card("TRANS-296")(_blur_dissolve)

RC = np.array([128.0, 40.0])
RS = 0.3
BASES = None


def nest(k, s, off, depth=3):
    """Scene k (base k with scene k+1 live in its screen rect) under the map p -> C + off + s (p - C)."""
    bases = [A0, B0, checker(5)]
    img = affine(bases[k % 3], s, dx=off[0], dy=off[1])
    if depth > 0:
        rc = np.array([CX, CY]) + off + s * (RC - np.array([CX, CY]))
        m = _card_rect_mask(rc[0], rc[1], W * RS * s, H * RS * s, 0.0)
        inner = nest(k + 1, s * RS, off + s * (RC - np.array([CX, CY])), depth - 1)
        img = mix(img, inner, m)
    return img


def dive_frame(e, k=0):
    Z = math.exp(math.log(1 / RS) * e)
    g = (Z - 1) / (1 / RS - 1)
    C = np.array([CX, CY])
    off = (RC - C) * (1 - Z) + (C - RC) * g
    return nest(k, Z, off)


def _nested_dive(task, wd):
    D = 1.0
    ease = p_io(2)

    def frame(t):
        if t <= D:
            return dive_frame(ease(t / D))
        if t <= D + 0.1:
            return nest(1, 1.0, np.zeros(2))
        return dive_frame(ease(1 - (t - D - 0.1) / D))      # reverse for the return
    path, frs, ts = film(wd, "nested_dive", frame, 2 * D + 0.1, 30)
    iD = at(ts, D)
    sel0 = _card_rect_mask(RC[0], RC[1], W * RS - 4, H * RS - 4, 0) > 0.99
    s_in = scale_est(frs[0], sel0 & (bwt(frs[0]) > 0.98)) if False else None
    row = int(RC[1]) + 10            # below the grand-child screen
    x0, x1 = (np.nonzero(bwt(frs[0])[row] > 0.5)[0][[0, -1]])
    span = srcx(frs[0])[row, x0 + 2:x1 - 1]
    s_live = float(np.polyfit(span, np.arange(x0 + 2, x1 - 1), 1)[0])
    i = at(ts, 0.5)
    Z = math.exp(math.log(1 / RS) * ease(ts[i] / D))
    return ([near("next scene is live inside the screen rect at scale 0.3", s_live, RS, 0.01),
             check("dive ends with the inner rect filling the frame == next scene", mad(frs[iD], nest(1, 1.0, np.zeros(2))) < 0.5,
                   mad(frs[iD], nest(1, 1.0, np.zeros(2))), "< 0.5"),
             check("swap invisible", mad(frs[iD], frs[iD + 1]) < 0.5, mad(frs[iD], frs[iD + 1]), "< 0.5"),
             check("mid-dive frame equals the zoomed nest (log-space zoom %.2fx)" % Z, mad(frs[i], dive_frame(ease(ts[i] / D))) < 0.5,
                   mad(frs[i], dive_frame(ease(ts[i] / D))), "< 0.5"),
             check("reverse returns to the first scene", mad(frs[-1], frs[0]) < 0.5, mad(frs[-1], frs[0]), "< 0.5"),
             neg("swap jump without the dive", mad(frs[0], nest(1, 1.0, np.zeros(2))), 0.0, 0.5)],
            [path, save_plan(wd, "nested", {"card": "TRANS-302", "rect": RC.tolist(), "rect_scale": RS, "dive_s": D})])


card("TRANS-302")(_nested_dive)


def pixelate(img, b):
    if b <= 1:
        return img.copy()
    ys, xs = (np.arange(H) // b), (np.arange(W) // b)
    out = np.empty_like(img)
    for by in range(ys.max() + 1):
        for bx in range(xs.max() + 1):
            sl = (slice(by * b, (by + 1) * b), slice(bx * b, (bx + 1) * b))
            out[sl] = img[sl].reshape(-1, 3).mean(0)
    return out


def block_size(fr, cands=range(1, 41)):
    best = 1
    for b in cands:
        if np.abs(pixelate(fr, b) - fr).max() < 1.5:
            best = b
    return best


def _mosaic(task, wd):
    D = 0.6

    def bsz(t):
        u = t / (D / 2) if t < D / 2 else (D - t) / (D / 2)
        return int(round(2 + 30 * p_in(2)(u)))

    def frame(t):
        if t >= D - 1e-9:
            return B0.copy()
        return pixelate(A0 if t < D / 2 else B0, bsz(t))
    path, frs, ts = film(wd, "mosaic", frame, D, 20)
    probe = [at(ts, x) for x in (0.1, 0.2, 0.3, 0.45)]
    meas = [block_size(frs[i]) for i in probe]
    expd = [bsz(ts[i]) for i in probe]
    i = probe[1]
    means_ok = mad(frs[i], pixelate(A0, expd[1]))
    return ([check("block size eases 2 -> 32 -> 2 (measured block grid)", meas == expd, meas, expd),
             check("blocks carry the true block means of the frame", means_ok < 0.6, means_ok, "< 0.6"),
             check("A before the peak, B after", fracb(frs[probe[1]]) < 0.05 and fracb(frs[probe[3]]) > 0.95,
                   [fracb(frs[probe[1]]), fracb(frs[probe[3]])], "A / B"),
             check("ends on the clean next scene", mad(frs[-1], B0) < 0.5, mad(frs[-1], B0), "< 0.5"),
             neg("block size of the unprocessed frame", float(block_size(A0, range(1, 9))), float(expd[1]), 0.5)],
            [path, save_plan(wd, "mosaic", {"card": "TRANS-304", "block_px": [2, 32], "ms": 600,
                                            "note": "block sizes in fixture px"})])


card("TRANS-304")(_mosaic)


def _glitch_tiles(task, wd):
    a = text_layer("GLITCH", size=16)[1]
    ys = np.nonzero(a.max(1) > 0.5)[0]
    strip = a[ys.min() - 1:ys.max() + 2]
    hgt, pitch, rows, d = strip.shape[0], 20, 5, 2
    top = int(CY - pitch * rows / 2 + (pitch - hgt) / 2)
    rng = np.random.default_rng(4)
    shifts = rng.integers(-12, 13, size=(40, rows))

    def frame_i(i):
        img = np.zeros((H, W, 3))
        for k in range(rows):
            y = top + k * pitch
            s = int(shifts[i, k])
            for c, o in ((0, d), (1, 0), (2, -d)):
                img[y:y + hgt, :, c] = np.maximum(img[y:y + hgt, :, c], 255 * np.roll(strip, s + o, axis=1))
        return img
    fps, n = 20, 11
    path = write_video([frame_i(i) for i in range(n)], Path(wd) / "glitch_tiles.mp4", fps)
    frs = fx.frames(path, (W, H))

    def best_shift(row, ref, rng_=range(-20, 21)):
        return max(rng_, key=lambda s: float((np.roll(ref, s) * row).sum()))
    ref = strip.max(0)
    errs, offs = [], []
    for i in (2, 7):
        for k in range(rows):
            y = top + k * pitch
            g = frs[i][y:y + hgt, :, 1].max(0) / 255
            r = frs[i][y:y + hgt, :, 0].max(0) / 255
            errs.append(abs(best_shift(g, ref) - int(shifts[i, k])))
            offs.append(best_shift(r, g, range(-6, 7)))
    prof = frs[2][..., 1].max(1) > 128
    nrows = int(np.sum(prof[1:] & ~prof[:-1]))
    moved = [int(shifts[2, k]) != int(shifts[7, k]) for k in range(rows)]
    single = np.zeros((H, W, 3))
    single[top:top + hgt, :, :] = 255 * strip[..., None]
    sg = single[..., 1].max(1) > 128
    return ([check("word repeated in 5 rows", nrows == rows, nrows, rows),
             check("each row's horizontal shift matches the programmed jitter", max(errs) == 0, max(errs), 0),
             check("RGB offset: red channel displaced +2 px from green on every row", all(o == d for o in offs), sorted(set(offs)), d),
             check("rows shift over time", sum(moved) >= 3, sum(moved), ">= 3"),
             neg("row count of the plain word", float(np.sum(sg[1:] & ~sg[:-1])), float(rows), 0.5)],
            [path, save_plan(wd, "glitch", {"card": "TRANS-305", "rows": rows, "rgb_offset_px": d, "jitter_px": 12})])


card("TRANS-305")(_glitch_tiles)
