"""wave 3, chunk 08: texture-material and transitions-cuts cards as real programs with known-answer checks.

Engines used here (all local, nothing installed for this module):
  numpy / scipy.ndimage / OpenCV / Pillow (with raqm for shaped Arabic) for the texture and frame math;
  FFmpeg (libx264rgb lossless, xfade) for renders and as the reference the xfade port is compared with;
  the repo's own mimic modules ``scripts/mimic/mm_transitions.py`` (54 xfade ports + 11 phone-editor kinds) and
  ``mm_analyze.py`` (classification by re-synthesis);
  Chromium driven by the globally installed node Playwright (SwiftShader WebGL) for the browser cards: CSS
  @starting-style, ::details-content + interpolate-size, the View Transitions API, raw WebGL GLSL, and three.js
  0.186.1 through the repo's prebuilt ``kit/three-kit.bundle.js`` (window.K3) for CubeCamera, pebbles, terrain and
  road materials.

Every runner builds a seeded fixture inside its work folder, applies the card's method, reads the produced file
back, and measures it against the value the card's own formula predicts. Each carries a negative control: the
same measurement on the untreated input (or the plain hard cut) must fail.
"""
from __future__ import annotations

import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from _harness import card, check, fx

REPO = Path(__file__).resolve().parents[4]
MIMIC = REPO / ".claude/skills/kosif-superpowers/scripts/mimic"
KIT = REPO / ".claude/skills/kosif-superpowers/vendor/100-superskills/skills/kosif-montage-motion/scripts/kit"
FONTS = REPO / ".claude/skills/kosif-superpowers/proofs/_shared/fonts"

GAPS: dict = {
    "TEX-39": "HyperFrames media-treatment shader effects (18 keys) are interpreted by the HyperFrames runtime's "
              "colour-grading pipeline; the card gives no shader maths and a HyperFrames render does not fit in 15 s",
    "TEX-62": "texture-mask-text needs the 66 ambientCG PNG masks shipped with the HyperFrames registry block; the "
              "masks are not present on this machine (the global hyperframes 0.9.8 package does not ship them)",
    "TEX-63": "HyperFrames material shader blocks require a WebGPU-capable Chromium (data-requires-webgpu); only "
              "SwiftShader WebGL is available here",
    "TEX-83": "warm-grain is a HyperFrames example project used as a palette/type reference only; its "
              "sub-compositions are missing locally and `hyperframes init --example` needs the network",
    "TRANS-261": "first/last-frame AI morph needs a paid video-generation API key (Kling image_tail / Together "
                 "frame_images); no spending allowed",
}

W, H = 192, 108


# ============================================================================ helpers
def _rng(seed=7):
    return np.random.default_rng(seed)


def _u8(a):
    return np.clip(np.round(np.asarray(a, dtype=float)), 0, 255).astype(np.uint8)


def _png(path, a):
    Image.fromarray(_u8(a)).save(path)
    return Path(path)


def _load(path, mode="RGB"):
    return np.asarray(Image.open(path).convert(mode)).astype(float)


def _hex(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=float)


def _luma(a):
    a = np.asarray(a, dtype=float)
    return a[..., 0] * .2126 + a[..., 1] * .7152 + a[..., 2] * .0722


def _blur(a, s):
    from scipy.ndimage import gaussian_filter
    a = np.asarray(a, dtype=float)
    if a.ndim == 3:
        return gaussian_filter(a, (s, s, 0))
    return gaussian_filter(a, s)


def _hf(a):
    a = np.asarray(a, dtype=float)
    return float(np.abs(a - _blur(a, 1.5)).mean())


def _vid(path, frames, fps=30):
    """Lossless RGB H.264 (libx264rgb -qp 0) so the read-back equals what was rendered."""
    frames = [_u8(f) for f in frames]
    h, w = frames[0].shape[:2]
    p = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                        "-s", "%dx%d" % (w, h), "-r", str(fps), "-i", "-", "-c:v", "libx264rgb", "-qp", "0",
                        "-preset", "ultrafast", str(path)], input=b"".join(f.tobytes() for f in frames),
                       capture_output=True, timeout=60)
    if p.returncode:
        raise RuntimeError(p.stderr.decode(errors="replace")[-300:])
    return Path(path)


def _rd(path):
    info = fx.probe(path)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    return fx.frames(path, size=(int(v["width"]), int(v["height"])))


def _jw(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
    return Path(path)


def _grid(h=H, w=W):
    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    return xx, yy


def _noise(x, y, seed=1, period=256):
    """Smooth value noise in [-1, 1] (cubic-spline lattice, wraps)."""
    from scipy.ndimage import map_coordinates
    g = _rng(seed).random((period, period)) * 2 - 1
    return map_coordinates(g, [np.asarray(y) % period, np.asarray(x) % period], order=3, mode="grid-wrap")


def _fbm(x, y, octaves=4, seed=1):
    a, s, w = 0.0, 0.0, 1.0
    for i in range(octaves):
        a = a + w * _noise(x * 2 ** i, y * 2 ** i, seed + 31 * i)
        s += w
        w *= .5
    return a / s


def _font(size, bold=True, mono=False):
    for p in (["/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"] if mono else
              ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
               "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]):
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def _text_mask(text, size, shape=(H, W), xy=None, font=None, **kw):
    im = Image.new("L", (shape[1], shape[0]), 0)
    d = ImageDraw.Draw(im)
    f = font or _font(size)
    bb = d.textbbox((0, 0), text, font=f, **kw)
    if xy is None:
        xy = ((shape[1] - (bb[2] - bb[0])) / 2 - bb[0], (shape[0] - (bb[3] - bb[1])) / 2 - bb[1])
    d.text(xy, text, fill=255, font=f, **kw)
    return np.asarray(im).astype(float) / 255.0


def _components(mask):
    from scipy.ndimage import label
    lab, n = label(mask)
    return lab, n


def _phase(a, b):
    import cv2
    (dx, dy), _ = cv2.phaseCorrelate(np.asarray(a, np.float32), np.asarray(b, np.float32))
    return float(dx), float(dy)


def _orient(img, mask=None):
    """Dominant line orientation in degrees (0 = horizontal lines), image y axis pointing down."""
    import cv2
    g = np.asarray(img, np.float32)
    gx = cv2.Sobel(g, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(g, cv2.CV_32F, 0, 1, ksize=3)
    if mask is not None:
        gx, gy = gx[mask], gy[mask]
    jxx, jyy, jxy = float((gx * gx).sum()), float((gy * gy).sum()), float((gx * gy).sum())
    theta = 0.5 * math.degrees(math.atan2(2 * jxy, jxx - jyy))  # gradient direction
    return (theta + 90.0 + 180.0) % 180.0


def _sharp(img):
    import cv2
    return float(cv2.Laplacian(np.asarray(_luma(img), np.float32), cv2.CV_32F).var())


def _softlight(b, s):
    b, s = b / 255.0, s / 255.0
    return ((1 - 2 * s) * b * b + 2 * s * b) * 255.0


def _vignette(h, w, strength, power=2.0):
    xx, yy = _grid(h, w)
    r = np.hypot((xx - (w - 1) / 2) / ((w - 1) / 2), (yy - (h - 1) / 2) / ((h - 1) / 2)) / math.sqrt(2)
    return 1 - strength * np.clip(r, 0, 1) ** power


def _ease_io_cubic(u):
    u = np.clip(u, 0, 1)
    return np.where(u < .5, 4 * u ** 3, 1 - (-2 * u + 2) ** 3 / 2)


def _ease_out_cubic(u):
    u = np.clip(u, 0, 1)
    return 1 - (1 - u) ** 3


def _bez(x1, y1, x2, y2):
    def f(x):
        if x <= 0:
            return 0.0
        if x >= 1:
            return 1.0
        lo, hi = 0.0, 1.0
        for _ in range(50):
            m = (lo + hi) / 2
            cx = 3 * x1 * m * (1 - m) ** 2 + 3 * x2 * m * m * (1 - m) + m ** 3
            lo, hi = (m, hi) if cx < x else (lo, m)
        m = (lo + hi) / 2
        return 3 * y1 * m * (1 - m) ** 2 + 3 * y2 * m * m * (1 - m) + m ** 3
    return f


def _disc_mask(h, w, cx, cy, r, ss=4):
    xx, yy = np.mgrid[0:h * ss, 0:w * ss].astype(float)[::-1]
    yy, xx = np.mgrid[0:h * ss, 0:w * ss].astype(float)
    m = (((xx + .5) / ss - cx) ** 2 + ((yy + .5) / ss - cy) ** 2 <= r * r).astype(float)
    return m.reshape(h, ss, w, ss).mean((1, 3))


def _photo(h=H, w=W, seed=3):
    """Deterministic 'photo': smooth colour field + shapes + texture."""
    xx, yy = _grid(h, w)
    n = _fbm(xx / 18, yy / 18, 3, seed)
    img = np.stack([120 + 80 * np.sin(xx / w * 3 + n), 110 + 70 * np.cos(yy / h * 2.5 - n), 140 + 60 * n], -1)
    img[(xx - w * .33) ** 2 + (yy - h * .5) ** 2 < (h * .22) ** 2] = [235, 200, 60]
    img[int(h * .2):int(h * .8), int(w * .62):int(w * .78)] = [40, 60, 150]
    img += _rng(seed).normal(0, 6, img.shape)
    return np.clip(img, 0, 255)


# ============================================================================ TEXTURE: grain family
def _grain_tile(seed=7, n=192):
    return np.clip(128 + 46 * _rng(seed).normal(0, 1, (n, n)), 0, 255)


def _grain_frame(base, t, tile, opacity=.08, fps_seed=24):
    seed = 1 + int(math.floor(t * fps_seed)) % 97
    dx, dy = (seed * 73856093) % tile.shape[1], (seed * 19349663) % tile.shape[0]
    g = np.roll(tile, (dy, dx), (0, 1))
    reps = (math.ceil(base.shape[0] / g.shape[0]), math.ceil(base.shape[1] / g.shape[1]))
    g = np.tile(g, reps)[:base.shape[0], :base.shape[1]][..., None]
    return base * (1 - opacity) + _softlight(base, g) * opacity


@card("TEX-02")
def frame_seeded_grain(task, wd):
    """seek(t) seeds the grain from the frame number (seed = 1 + floor(t*24) % 97): a 192x192 grey tile translated by
    a hash of the seed, soft-light at 8%; refreshed at 24 Hz yet identical on re-render."""
    xx, yy = _grid()
    base = np.stack([60 + 120 * xx / W, 90 + 60 * yy / H, 140 + 0 * xx], -1)
    tile = _grain_tile()
    f24 = [_grain_frame(base, i / 24, tile) for i in range(24)]
    out = _vid(wd / "grain_24fps.mp4", f24, 24)
    again = [_grain_frame(base, i / 24, tile) for i in range(24)]
    out48 = _vid(wd / "grain_48fps.mp4", [_grain_frame(base, i / 48, tile) for i in range(24)], 48)
    static = _vid(wd / "static_grain.mp4", [_grain_frame(base, 0.0, tile) for i in range(24)], 24)
    F, F48, S = _rd(out), _rd(out48), _rd(static)
    delta = float(np.mean([np.abs(_luma(F[i + 1]) - _luma(F[i])).mean() for i in range(len(F) - 1)]))
    held = max(float(np.abs(F48[2 * k] - F48[2 * k + 1]).max()) for k in range(len(F48) // 2))
    sdelta = float(np.mean([np.abs(_luma(S[i + 1]) - _luma(S[i])).mean() for i in range(len(S) - 1)]))
    same = all(np.array_equal(_u8(a), _u8(b)) for a, b in zip(f24, again))
    return [check("fresh grain every frame: mean frame-to-frame luma delta > 0.5", delta > .5, delta, ">0.5"),
            check("deterministic: re-render of seek(t) is byte-identical", same, same, True),
            check("seed refresh is 24 Hz: at 48 fps frames 2k and 2k+1 identical", held == 0, held, 0),
            check("negative control: a fixed seed (no seek reseed) gives delta <= 0.5", not sdelta > .5, sdelta, "<=0.5")
            ], [out, out48]


@card("TEX-08")
def vintage_film_grade(task, wd):
    """Final pass: warm/violet split-tone, grain .08, 20 dust specks/frame at seeded positions, 0-2 drifting 1 px
    vertical scratches at 30% white, bloom over threshold .8, vignette and projector flicker 1 +/- .03."""
    from scipy.ndimage import median_filter
    xx, yy = _grid()
    n = 24
    src = [np.stack([60 + 170 * xx / W] * 3, -1) for _ in range(n)]
    inp = _vid(wd / "input.mp4", src, 24)
    rng = _rng(11)
    gains = 1 + .03 * rng.uniform(-1, 1, n)
    dust = []
    outf = []
    vig = _vignette(H, W, .35)[..., None]
    for i, f in enumerate(src):
        l = _luma(f)[..., None] / 255
        g = f + (1 - l) * np.array([18, 4, -14]) + l * np.array([6, -10, 16])
        g = g + rng.normal(0, .08 * 255 * .5, (H, W, 1))
        hi = np.clip(_luma(g) / 255 - .8, 0, None)[..., None]
        g = g + _blur(hi, 3) * 255 * 1.5
        pts = [(int(rng.integers(3, W - 3)), int(rng.integers(3, H - 3))) for _ in range(20)]
        for (x, y) in pts:
            r = int(rng.integers(1, 3))
            g[max(0, y - r + 1):y + r, max(0, x - r + 1):x + r] *= .25
        dust.append(pts)
        for s in range(int(rng.integers(0, 3))):
            sx = int((W * (.3 + .4 * s) + 2 * i) % W)
            g[:, sx] = g[:, sx] * .7 + 255 * .3
        outf.append(g * vig * gains[i])
    out = _vid(wd / "vintage.mp4", outf, 24)
    O, I = _rd(out), _rd(inp)

    def measures(F):
        dark, bright = F[:, H // 3:2 * H // 3, 8:W // 4], F[:, H // 3:2 * H // 3, 3 * W // 4:W - 8]
        warm = float((dark[..., 0] - dark[..., 2]).mean())
        violet = float((bright[..., 2] - bright[..., 1]).mean())
        hits = 0
        for k, pts in enumerate(dust):
            L = _luma(F[k])
            med = median_filter(L, 7)
            hits += sum(1 for (x, y) in pts if L[y, x] < med[y, x] - 15)
        dust_rate = hits / (20.0 * len(dust))
        means = np.array([_luma(f[H // 3:2 * H // 3, W // 3:2 * W // 3]).mean() for f in F])
        flick = float(means.std() / means.mean())
        return warm, violet, dust_rate, flick
    wo, vo, do, fo = measures(O)
    wi, vi, di, fi = measures(I)
    crit = lambda w, v, d, f: w > 5 and v > 5 and d > .8 and .004 < f < .05
    return [check("split-tone: shadows warm (R-B > 5)", wo > 5, wo, ">5"),
            check("split-tone: highlights violet (B-G > 5)", vo > 5, vo, ">5"),
            check("dust: >80% of the 20 seeded specks/frame darker than local median", do > .8, do, ">0.8"),
            check("projector flicker: per-frame luma std/mean in (0.004, 0.05)", .004 < fo < .05, fo, "~0.017"),
            check("negative control: untreated clip fails the grade", not crit(wi, vi, di, fi), [wi, vi, di, fi], "fail")
            ], [out]


def _grain_std(F, region):
    y0, y1, x0, x1 = region
    return float(np.mean([_luma(f[y0:y1, x0:x1]).std() for f in F]))


@card("TEX-09")
def warm_black_grain_vignette(task, wd):
    """Warm black #0a0907 ground, per-frame grain 4% and a strong radial vignette that pushes the edges of a red
    scene -35% luminance."""
    base = np.zeros((H, W, 3)) + _hex("#0a0907")
    base[30:78, :] = _hex("#c8302a")
    n = 12
    inp = _vid(wd / "input.mp4", [base] * n)
    rng = _rng(5)
    vig = _vignette(H, W, .55, 1.6)[..., None]
    frames = [np.clip(base + rng.normal(0, .04 * 255, (H, W, 1)), 0, 255) * vig for _ in range(n)]
    out = _vid(wd / "warm_black.mp4", frames)
    O, I = _rd(out), _rd(inp)

    def m(F):
        bg = np.median(F[:, 4:20, W // 2 - 20:W // 2 + 20].reshape(-1, 3), 0)
        edge = float(np.mean([_luma(f[44:64, 0:6]).mean() for f in F]) / np.mean([_luma(f[44:64, W // 2 - 10:W // 2 + 10]).mean() for f in F]))
        gs = _grain_std(F, (48, 60, W // 2 - 12, W // 2 + 12)) / 255
        fresh = float(np.abs(F[1] - F[0]).mean())
        return bg, edge, gs, fresh
    bo, eo, go, fo = m(O)
    bi, ei, gi, fi = m(I)
    ok = lambda e, g, f: e <= .7 and .02 <= g <= .11 and f > 1
    return [check("ground stays warm black #0a0907 (median within 4)", np.abs(bo - _hex("#0a0907")).max() <= 4, bo.tolist(), [10, 9, 7]),
            check("vignette pushes red scene edge >= 30% darker (ratio <= 0.7)", eo <= .7, eo, "<=0.7"),
            check("grain 2-11% std on the flat red", .02 <= go <= .11, go, "0.04"),
            check("grain regenerates every frame (frame delta > 1)", fo > 1, fo, ">1"),
            check("negative control: untreated scene fails", not ok(ei, gi, fi), [ei, gi, fi], "fail")], [out]


@card("TEX-10")
def editorial_paper_grade(task, wd):
    """Cream #efecdd paper with static 3% noise and a 10% vignette, near-black ink and one red accent; the data label
    band is kept clean of texture."""
    base = np.zeros((H, W, 3)) + _hex("#efecdd")
    base[60:64, 20:150] = _hex("#141414")
    base[40:58, 120:150] = _hex("#d62828")
    label = (slice(80, 96), slice(20, 120))
    inp = _vid(wd / "input.mp4", [base] * 4)
    noise = _rng(9).normal(0, .03 * 255, (H, W, 1))
    vig = _vignette(H, W, .10, 2.0)[..., None]
    paper = np.clip(base + noise, 0, 255) * vig
    paper[label] = _hex("#efecdd")
    paper[84:88, 24:100] = _hex("#141414")
    out = _vid(wd / "editorial.mp4", [paper] * 4)
    O, I = _rd(out), _rd(inp)

    def m(F):
        ns = _grain_std(F, (4, 30, 30, 100)) / 255
        static = float(np.abs(F[3] - F[0]).max())
        corner = float(_luma(F[0][0:4, 0:4]).mean() / _luma(F[0][2:30, 80:110]).mean())
        clean = float(_luma(F[0][80:84, 20:120]).std())
        return ns, static, corner, clean
    no, so, co, lo = m(O)
    ni, si, ci, li = m(I)
    return [check("paper noise ~3% (std 1.5-4.5%)", .015 <= no <= .045, no, .03),
            check("noise is static (not boiling): frames identical", so == 0, so, 0),
            check("vignette ~10% at the corner (ratio 0.85-0.95)", .85 <= co <= .95, co, .9),
            check("data label band clean of texture (std ~0)", lo <= .01, lo, 0),
            check("negative control: untreated cream has no paper noise", not (.015 <= ni <= .045), ni, "<0.015")], [out]


def _hud(h, w, k, n):
    m = np.zeros((h, w), bool)
    L = 14
    for (x, y, sx, sy) in [(6, 6, 1, 1), (w - 7, 6, -1, 1), (6, h - 7, 1, -1), (w - 7, h - 7, -1, -1)]:
        xs = sorted([x, x + sx * L])
        ys = sorted([y, y + sy * L])
        m[y, xs[0]:xs[1] + 1] = True
        m[ys[0]:ys[1] + 1, x] = True
    lab = _text_mask("REC 01", 9, (h, w), xy=(24, 8), font=_font(9, mono=True)) > .5
    m |= lab
    mw = 100
    fill = int(round(mw * k / (n - 1)))
    m[h - 14:h - 11, 46:46 + fill] = True
    return m, fill


@card("TEX-11")
def film_grain_hud(task, wd):
    """Per-frame grain 8% under a fixed HUD layer (corner brackets, micro mono label, progress meter); the HUD stays
    crisp outside the grain/camera layer."""
    base = _photo()
    n = 10
    rng = _rng(4)
    frames, inp, fills = [], [], []
    for k in range(n):
        m, fill = _hud(H, W, k, n)
        fills.append(fill)
        g = np.clip(base + rng.normal(0, .08 * 255, (H, W, 1)), 0, 255)
        g[m] = 245
        frames.append(g)
        b = base.copy()
        b[m] = 245
        inp.append(b)
    out = _vid(wd / "grain_hud.mp4", frames)
    pin = _vid(wd / "input.mp4", inp)
    O, I = _rd(out), _rd(pin)
    hud0, _ = _hud(H, W, 0, n)
    corners = np.zeros((H, W), bool)
    corners[6:21, 6:21] = hud0[6:21, 6:21]
    crisp = max(float(np.abs(O[k][corners] - 245).max()) for k in range(n))
    meter = [int((O[k][H - 13, 46:150].mean(-1) > 240).sum()) for k in range(n)]
    gdelta = lambda F: float(np.mean([np.abs(F[k + 1][30:80, 30:150] - F[k][30:80, 30:150]).mean() for k in range(n - 1)]))
    go, gi = gdelta(O), gdelta(I)
    return [check("HUD brackets stay crisp (max deviation 0 from #f5f5f5)", crisp == 0, crisp, 0),
            check("progress meter fill = k/(n-1) of 100 px (+/-1 px)", all(abs(a - b) <= 1 for a, b in zip(meter, fills)), meter, fills),
            check("grain refreshes every frame under the HUD (delta > 3)", go > 3, go, ">3"),
            check("negative control: untreated frames have no grain motion", not gi > 3, gi, "<=3")], [out]


@card("TEX-12")
def grain_glow_title(task, wd):
    """Heavy title filled with noise texture at .5, a 20 px outer glow (blurred copy), scaling in from a single star
    point at the title centre."""
    from scipy.ndimage import binary_dilation, zoom as ndzoom
    full = _text_mask("NOVA", 52)
    xx, yy = _grid()
    tex = 128 + 127 * _fbm(xx / 3, yy / 3, 3, 21)
    bg = np.zeros((H, W, 3)) + [10, 10, 24]
    n = 12
    frames, scales = [], []
    for k in range(n):
        s = max(.02, _ease_out_cubic(k / (n - 1)))
        scales.append(s)
        m = ndzoom(full, s, order=1)
        mm = np.zeros((H, W))
        hh, ww = m.shape
        y0, x0 = (H - hh) // 2, (W - ww) // 2
        mm[y0:y0 + hh, x0:x0 + ww] = m[:H, :W]
        fill = 255 * .5 + tex * .5
        glow = _blur(mm, 20 / 2.5) * 2.2
        f = bg + np.clip(glow, 0, 1)[..., None] * np.array([120, 140, 255]) * .9
        f = f * (1 - mm[..., None]) + (fill[..., None] * np.array([1, .95, .85])) * mm[..., None]
        frames.append(f)
    out = _vid(wd / "title.mp4", frames)
    O = _rd(out)
    plain = bg * (1 - full[..., None]) + 255 * full[..., None]
    pin = _png(wd / "plain_title.png", plain)
    P = _load(pin)

    def m(F):
        inside = full > .9
        ring = binary_dilation(full > .1, iterations=10) & ~binary_dilation(full > .1, iterations=3)
        tex_std = float(_luma(F)[inside].std())
        glow = float(_luma(F)[ring].mean() - _luma(bg).mean())
        return tex_std, glow
    to, go = m(O[-1])
    ti, gi = m(P)
    area = [float((_luma(f) > 150).sum()) for f in O]
    return [check("noise texture fills the letters (inside luma std > 12)", to > 12, to, ">12"),
            check("20 px outer glow lifts the ring 3-10 px outside the letters by > 12", go > 12, go, ">12"),
            check("scale-in from a star point: first-frame bright area < 2% of last", area[0] < .02 * area[-1], [area[0], area[-1]], "<2%"),
            check("letter area grows monotonically", all(b >= a - 1 for a, b in zip(area, area[1:])), area[:4], "monotone"),
            check("negative control: a plain white title has no texture and no glow", not (ti > 12 and gi > 12), [ti, gi], "fail")
            ], [out, pin]


@card("TEX-13")
def static_paper_texture(task, wd):
    """Procedural paper overlay (turbulence at baseFrequency ~.75 tinted to a paper tone) multiplied over the scene at
    7%, same seed every frame so it stays still while the drawing moves."""
    xx, yy = _grid()
    turb = .5 + .5 * _fbm(xx * .75, yy * .75, 4, 13)
    paper = np.stack([turb * 230 + 25, turb * 220 + 25, turb * 195 + 30], -1) / 255
    op = .07
    mult = 1 - op + op * paper
    frames, src = [], []
    for k in range(8):
        f = np.zeros((H, W, 3)) + 235
        f[40:70, 20 + 10 * k:50 + 10 * k] = [200, 60, 50]
        src.append(f)
        frames.append(f * mult)
    out = _vid(wd / "paper.mp4", frames)
    inp = _vid(wd / "input.mp4", src)
    O, I = _rd(out), _rd(inp)

    def m(F, S):
        r = [F[k][5:35] / np.maximum(1, S[k][5:35]) for k in range(len(F))]
        still = max(float(np.abs(r[k] - r[0]).max()) for k in range(len(r)))
        dark = float(1 - np.mean(r[0]))
        tstd = float(np.std(r[0]))
        return still, dark, tstd
    so, do, to = m(O, src)
    si, di, ti = m(I, src)
    return [check("overlay is static: residual identical in every frame (<= 1/235)", so <= 1 / 235 + 1e-6, so, 0),
            check("multiply darkens 3-10% on average", .03 <= do <= .10, do, "0.03-0.10"),
            check("paper texture present (residual std > 0.008)", to > .008, to, ">0.008"),
            check("negative control: untreated scene has no paper residual", not (to > .008 and ti > .008) and not ti > .008, ti, "<=0.008")
            ], [out]


@card("TEX-14")
def watercolour_paper(task, wd):
    """Cream #f3e8cf embossed paper (noise height -> normal-ish emboss, multiplied) over the scene; hills as a wobbly ink
    arc filled with a #c6c7a4 wash, low-frequency darker blotches and 1-2 px edge darkening."""
    from scipy.ndimage import binary_erosion
    xx, yy = _grid()
    hgt = _fbm(xx / 2.5, yy / 2.5, 3, 17)
    gx, gy = np.gradient(hgt)
    shade = np.clip(1 + 1.6 * (-gx - gy) / math.sqrt(2), .85, 1.15)
    paper = _hex("#f3e8cf") * np.ones((H, W, 3))
    ridge = 70 - 18 * np.sin(xx / W * math.pi) + 2.5 * np.sin(xx / 7)
    hill = yy > ridge
    wash = _hex("#c6c7a4") * (1 - .08 * (.5 + .5 * _fbm(xx / 25, yy / 25, 2, 5)))[..., None]
    inner = binary_erosion(hill, iterations=2)
    edge = hill & ~inner
    img = np.where(hill[..., None], wash, paper)
    img[edge] *= .82
    out_a = img * shade[..., None]
    out = _png(wd / "watercolour.png", out_a)
    flat = np.where(hill[..., None], _hex("#c6c7a4"), paper)
    pin = _png(wd / "flat.png", flat)
    O, I = _load(out), _load(pin)

    def m(F):
        pap = np.median(F[~hill & (yy < 30)], 0)
        corr = float(np.corrcoef(_luma(F)[~hill & (yy < 40)], ((-gx - gy))[~hill & (yy < 40)])[0, 1])
        deep = binary_erosion(hill, iterations=8)
        edark = float(_luma(F)[deep].mean() - _luma(F)[edge].mean())
        blot = float(_luma(_blur(F, 3))[deep].std())
        return pap, corr, edark, blot
    po, co, eo, bo = m(O)
    pi, ci, ei, bi = m(I)
    return [check("paper base #f3e8cf (median within 8)", np.abs(po - _hex("#f3e8cf")).max() <= 8, po.tolist(), "#f3e8cf"),
            check("emboss: paper luma correlates with the height-gradient light (r > 0.5)", co > .5, co, ">0.5"),
            check("wash edge darkened 1-2 px (interior - edge luma > 8)", eo > 8, eo, ">8"),
            check("low-frequency blotches in the wash (blurred std > 2)", bo > 2, bo, ">2"),
            check("negative control: flat fill has no emboss/edge/blotch", not (ci > .5 or ei > 8 or bi > 2), [ci, ei, bi], "fail")], [out]


def _pip(x, y, poly):
    """Even-odd ray casting point-in-polygon on arrays."""
    inside = np.zeros(np.shape(x), bool)
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        cond = ((y1 > y) != (y2 > y)) & (x < (x2 - x1) * (y - y1) / ((y2 - y1) + 1e-12) + x1)
        inside ^= cond
    return inside


@card("TEX-15")
def parchment_sand_stipple(task, wd):
    """Radial parchment #ead9b5 -> #c9aa72 with darker edges, faint 1 px fold lines at 8%, and seeded sand dots
    (r .6-1 px, 30%) only inside the desert polygon (point-in-polygon rejects the sea)."""
    xx, yy = _grid()
    r = np.clip(np.hypot((xx - W / 2) / (W / 2), (yy - H / 2) / (H / 2)) / math.sqrt(2), 0, 1)
    ground = _hex("#ead9b5") * (1 - r[..., None]) + _hex("#c9aa72") * r[..., None]
    for fx_ in (W // 3, 2 * W // 3):
        ground[:, fx_] *= .92
    ground[H // 2, :] *= .92
    land = [(20, 15), (110, 10), (150, 40), (120, 95), (40, 90), (15, 55)]
    rng = _rng(19)
    pts = rng.uniform([0, 0], [W, H], (4000, 2))
    keep = _pip(pts[:, 0], pts[:, 1], land)

    def stipple(points):
        im = Image.fromarray(_u8(ground))
        lay = Image.new("L", (W * 4, H * 4), 0)
        d = ImageDraw.Draw(lay)
        for (px, py) in points:
            rr = rng.uniform(.6, 1.0) * 4
            d.ellipse([px * 4 - rr, py * 4 - rr, px * 4 + rr, py * 4 + rr], fill=255)
        a = np.asarray(lay.resize((W, H), Image.BOX)).astype(float)[..., None] / 255 * .3
        return np.asarray(im).astype(float) * (1 - a) + np.array([120, 90, 40]) * a
    out = _png(wd / "parchment.png", stipple(pts[keep]))
    naive = _png(wd / "naive_uniform.png", stipple(pts))
    base = _png(wd / "ground.png", ground)
    O, N, G = _load(out), _load(naive), _load(base)
    sea = ~_pip(xx, yy, land)
    from scipy.ndimage import binary_erosion
    sea_core = binary_erosion(sea, iterations=2)
    land_core = binary_erosion(~sea, iterations=2)
    dot = lambda F: np.abs(F - G).max(-1) > 4
    so, lo = int((dot(O) & sea_core).sum()), int((dot(O) & land_core).sum())
    sn = int((dot(N) & sea_core).sum())
    centre = G[H // 2 - 6:H // 2 - 2, W // 2 + 4:W // 2 + 8].reshape(-1, 3).mean(0)
    return [check("parchment centre colour #ead9b5 (within 6)", np.abs(centre - _hex("#ead9b5")).max() <= 6, centre.tolist(), "#ead9b5"),
            check("edges darker than centre (vignette)", _luma(G[0:3, 0:3]).mean() < _luma(G[H // 2, W // 2 + 5]) - 15, float(_luma(G[0:3, 0:3]).mean()), "darker"),
            check("sand dots inside the desert (> 300 px)", lo > 300, lo, ">300"),
            check("no sand dot pixels in the sea (point-in-polygon)", so == 0, so, 0),
            check("negative control: unrejected uniform stipple puts dots in the sea", not sn == 0, sn, ">0")], [out]


def _scan(h=120, w=120):
    """A 'scanned' hand drawing: dark blob + inner detail on a flat off-white ground."""
    im = Image.new("RGB", (w, h), (238, 236, 228))
    d = ImageDraw.Draw(im)
    d.ellipse([28, 30, 92, 90], fill=(60, 90, 160))
    d.polygon([(60, 12), (75, 34), (45, 34)], fill=(200, 70, 50))
    d.line([(40, 60), (80, 60)], fill=(20, 20, 20), width=3)
    return np.asarray(im).astype(float)


def _sticker(scan, outline=6, shadow_off=2, shadow_a=.2, shadow_blur=4, ground_tol=18):
    corner = scan[0, 0]
    art = (np.abs(scan - corner).max(-1) > ground_tol)
    a = Image.fromarray((art * 255).astype(np.uint8))
    ring = np.asarray(a.filter(ImageFilter.MaxFilter(2 * outline + 1))).astype(float) / 255
    sh = np.roll(np.roll(ring, shadow_off, 0), shadow_off, 1)
    sh = np.asarray(Image.fromarray((sh * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(shadow_blur))).astype(float) / 255 * shadow_a
    rgba = np.zeros(scan.shape[:2] + (4,))
    rgba[..., :3] = 0
    rgba[..., 3] = sh * 255
    white = ring[..., None]
    rgba[..., :3] = rgba[..., :3] * (1 - white) + 255 * .9 * white + 0
    rgba[..., 3] = np.maximum(rgba[..., 3], ring * 255)
    rgba[art, :3] = scan[art]
    rgba[art, 3] = 255
    return rgba, art, ring


@card("TEX-19")
def scanned_sticker(task, wd):
    """Pillow: knock the flat ground out by corner colour, MaxFilter(13) the alpha for a 6 px white outline at 90%,
    and a soft shadow (blurred alpha offset 2 px at 20%) -- a paper sticker."""
    from scipy.ndimage import distance_transform_cdt
    scan = _scan()
    rgba, art, ring = _sticker(scan)
    out = wd / "sticker.png"
    Image.fromarray(_u8(rgba), "RGBA").save(out)
    O = np.asarray(Image.open(out)).astype(float)
    alpha = O[..., 3] > 250
    d = distance_transform_cdt(~art, metric="chessboard")
    width = float(d[alpha & ~art].max())
    rim = O[alpha & ~art][:, :3].mean(0)
    sh = O[..., 3] * ((O[..., 3] < 250) & (O[..., 3] > 0))
    below = float(sh[95:105, 50:70].mean())
    above = float(sh[1:6, 50:70].mean()) if True else 0
    raw = wd / "input_scan.png"
    Image.fromarray(_u8(scan)).convert("RGBA").save(raw)
    raw_alpha = np.asarray(Image.open(raw))[..., 3] > 250
    raw_w = float(d[raw_alpha & ~art].max())
    return [check("outline reaches 6 px beyond the art (MaxFilter 13)", 5.5 <= width <= 7.5, width, 6),
            check("outline is white at 90% (~230)", np.all(np.abs(rim - 229.5) < 3), rim.tolist(), 229.5),
            check("shadow offset down-right: more shadow below than above", below > above + 1, [below, above], "below>above"),
            check("ground knocked out: corners fully transparent", O[0, 0, 3] == 0 and O[-1, -1, 3] < 30, [O[0, 0, 3], O[-1, -1, 3]], 0),
            check("negative control: the untreated scan has no outline", not (5.5 <= raw_w <= 7.5), raw_w, 0)], [out]


@card("TEX-20")
def engraving_cutout(task, wd):
    """Desaturate 100%, halftone the object (dot radius from cell luma), then the sticker recipe: 6 px white border and
    a 12 px blurred shadow at 30% -- archival cut-out."""
    scan = _scan()
    g = _luma(scan)
    h, w = g.shape
    cell = 6
    ht = np.full((h * 4, w * 4), 255.0)
    im = Image.fromarray(ht.astype(np.uint8))
    d = ImageDraw.Draw(im)
    for cy in range(0, h, cell):
        for cx in range(0, w, cell):
            v = g[cy:cy + cell, cx:cx + cell].mean() / 255
            r = (1 - v) ** .5 * cell * .75 * 4
            if r > .4:
                X, Y = (cx + cell / 2) * 4, (cy + cell / 2) * 4
                d.ellipse([X - r, Y - r, X + r, Y + r], fill=0)
    ht = np.asarray(im.resize((w, h), Image.BOX)).astype(float)
    art = np.abs(scan - scan[0, 0]).max(-1) > 18
    grey = np.where(art[..., None], ht[..., None].repeat(3, -1), scan)
    rgba, art2, ring = _sticker(np.where(art[..., None], grey, scan[0, 0]), outline=6, shadow_off=4, shadow_a=.3, shadow_blur=6)
    rgba[art, :3] = ht[art][:, None]
    out = wd / "engraving_cutout.png"
    Image.fromarray(_u8(rgba), "RGBA").save(out)
    O = np.asarray(Image.open(out)).astype(float)
    obj = O[art][:, :3]
    sat = float((obj.max(-1) - obj.min(-1)).max())
    binary = float(((obj[:, 0] < 60) | (obj[:, 0] > 195)).mean())
    corr = float(np.corrcoef(_blur(_luma(O[..., :3]), 3)[art], _blur(g, 3)[art])[0, 1])
    shmax = float(O[..., 3][(O[..., 3] > 0) & (O[..., 3] < 250)].max()) / 255
    s_in = float((scan[art].max(-1) - scan[art].min(-1)).max())
    return [check("object fully desaturated (max channel spread <= 1)", sat <= 1, sat, 0),
            check("halftone is near-binary (>70% of object pixels black/white)", binary > .7, binary, ">0.7"),
            check("dot density follows source luma (blurred r > 0.6)", corr > .6, corr, ">0.6"),
            check("shadow peaks at <= 30% alpha", shmax <= .31, shmax, .3),
            check("negative control: the untreated scan is colourful", not s_in <= 1, s_in, ">1")], [out]


@card("TEX-23")
def paper_cutout_parallax(task, wd):
    """Cream #F6EBD9 paper, muted paper colours, hard paper shadow 0 8px 0 rgba(0,0,0,.18), three depth layers moving
    1 / 0.6 / 0.3 with the camera, and a gentle +/-2 deg sway on the near layer."""
    pal = {"far": _hex("#3B6EA8"), "mid": _hex("#5B8C5A"), "near": _hex("#D96B4A")}
    n = 16
    pan = 40.0
    frames, src = [], []
    for k in range(n):
        cam = pan * k / (n - 1)
        im = Image.new("RGB", (W * 2, H * 2), tuple(int(v) for v in _hex("#F6EBD9")))
        d = ImageDraw.Draw(im)
        sway = 2.0 * math.sin(2 * math.pi * k / n)
        for name, depth, (x, y, ww, hh) in [("far", .3, (40, 20, 40, 30)), ("mid", .6, (100, 40, 36, 30)), ("near", 1.0, (120, 74, 50, 14))]:
            ox = x - cam * depth
            poly = [(ox, y), (ox + ww, y), (ox + ww, y + hh), (ox, y + hh)]
            if name == "near":
                cx, cy = ox + ww / 2, y + hh
                a = math.radians(sway)
                poly = [(cx + (px - cx) * math.cos(a) - (py - cy) * math.sin(a), cy + (px - cx) * math.sin(a) + (py - cy) * math.cos(a)) for px, py in poly]
            sh = Image.new("L", im.size, 0)
            ImageDraw.Draw(sh).polygon([(px * 2, (py + 8) * 2) for px, py in poly], fill=int(255 * .18))
            im = Image.composite(Image.new("RGB", im.size, (0, 0, 0)), im, sh)
            d = ImageDraw.Draw(im)
            d.polygon([(px * 2, py * 2) for px, py in poly], fill=tuple(int(v) for v in pal[name]))
        frames.append(np.asarray(im.resize((W, H), Image.BOX)).astype(float))
    out = _vid(wd / "cutout.mp4", frames)
    O = _rd(out)

    def cx_of(f, col):
        m = np.abs(f - col).max(-1) < 10
        return float(np.nonzero(m)[1].mean()), m

    def angle(m):
        ys, xs = np.nonzero(m)
        xs, ys = xs - xs.mean(), ys - ys.mean()
        return .5 * math.degrees(math.atan2(2 * (xs * ys).mean(), (xs * xs).mean() - (ys * ys).mean()))
    sh = {}
    for name in pal:
        sh[name] = cx_of(O[0], pal[name])[0] - cx_of(O[-1], pal[name])[0]
    ratio = [sh["mid"] / sh["near"], sh["far"] / sh["near"]]
    angs = [abs(angle(cx_of(f, pal["near"])[1])) for f in O]
    sway_amp = max(min(a, abs(90 - a)) for a in angs)
    paper = O[0][2, 2]
    _, nm = cx_of(O[0], pal["near"])
    ys, xs = np.nonzero(nm)
    shadow = O[0][min(H - 1, ys.max() + 5), int(xs.mean())]
    shadow_ratio = float(_luma(shadow) / _luma(paper))
    uni = [1.0, 1.0]
    okr = lambda r: abs(r[0] - .6) < .06 and abs(r[1] - .3) < .06
    return [check("parallax ratios mid/near = 0.6, far/near = 0.3 (+/-0.06)", okr(ratio), ratio, [.6, .3]),
            check("near layer sways about 2 deg (1.2-2.8)", 1.2 <= sway_amp <= 2.8, sway_amp, 2.0),
            check("paper ground #F6EBD9", np.abs(paper - _hex("#F6EBD9")).max() <= 2, paper.tolist(), "#F6EBD9"),
            check("hard paper shadow 8 px below at .18 (luma ratio 0.78-0.86)", .78 <= shadow_ratio <= .86, shadow_ratio, .82),
            check("negative control: layers moving together (1:1:1) fail the depth ratios", not okr(uni), uni, "fail")], [out]


@card("TEX-24")
def stop_motion_jitter(task, wd):
    """Animate on twos (hold = floor(t*12)) with a seeded jitter per held frame: +/-1.5 px and +/-0.6 deg from
    hash(hold, layer), so the set breathes like stop-motion."""
    n, fps = 24, 24

    def jit(hold, layer=1):
        h_ = (hold * 2654435761 + layer * 40503) % 2 ** 32
        r = np.random.default_rng(h_)
        return r.uniform(-1.5, 1.5), r.uniform(-1.5, 1.5), r.uniform(-.6, .6)

    def render(jitter=True, twos=True):
        fr, expect = [], []
        for k in range(n):
            t = k / fps
            hold = math.floor(t * 12) if twos else k
            tt = hold / 12 if twos else t
            x, y = 40 + 100 * tt, 54
            dx, dy, rot = jit(hold) if jitter else (0, 0, 0)
            ss = 4
            im = Image.new("L", (W * ss, H * ss), 0)
            cx, cy = (x + dx) * ss, (y + dy) * ss
            a = math.radians(rot)
            pts = [(-12, -8), (12, -8), (12, 8), (-12, 8)]
            ImageDraw.Draw(im).polygon([(cx + (px * math.cos(a) - py * math.sin(a)) * ss, cy + (px * math.sin(a) + py * math.cos(a)) * ss) for px, py in pts], fill=255)
            m = np.asarray(im.resize((W, H), Image.BOX)).astype(float) / 255
            fr.append(np.stack([40 + 200 * m, 40 + 120 * m, 60 + 30 * m], -1))
            expect.append((x, y))
        return fr, expect
    fr, exp = render()
    out = _vid(wd / "stop_motion.mp4", fr, fps)
    fr2, _ = render()
    smooth, _ = render(jitter=False, twos=False)
    sm = _vid(wd / "input_smooth.mp4", smooth, fps)
    O, S = _rd(out), _rd(sm)

    def cen(f):
        m = np.clip((_luma(f) - _luma(np.array([40., 40, 60]))) / 160, 0, None)
        yy, xx = np.mgrid[0:H, 0:W]
        return float((xx * m).sum() / m.sum()) + .5, float((yy * m).sum() / m.sum()) + .5
    held = max(float(np.abs(O[2 * k] - O[2 * k + 1]).max()) for k in range(n // 2))
    dev = [np.subtract(cen(O[k]), exp[k]) for k in range(0, n, 2)]
    devmax = float(np.abs(dev).max())
    devstd = float(np.std(dev))
    same = all(np.array_equal(_u8(a), _u8(b)) for a, b in zip(fr, fr2))
    held_s = max(float(np.abs(S[2 * k] - S[2 * k + 1]).max()) for k in range(n // 2))
    return [check("on twos: frames 2k and 2k+1 identical", held == 0, held, 0),
            check("jitter within +/-1.6 px of the path", devmax <= 1.6, devmax, "<=1.6"),
            check("jitter present (std > 0.3 px)", devstd > .3, devstd, ">0.3"),
            check("seeded: re-render identical", same, same, True),
            check("negative control: smooth input is not held on twos", not held_s == 0, held_s, ">0")], [out]


def _sphere(h, w, cx, cy, R):
    xx, yy = _grid(h, w)
    dx, dy = (xx - cx) / R, (yy - cy) / R
    r2 = dx * dx + dy * dy
    inside = r2 <= 1
    nz = np.sqrt(np.clip(1 - r2, 0, 1))
    return inside, np.stack([dx, dy, nz], -1)


def _ggx_shade(nrm, inside, rough, light=(-.5, -.6, .62), base=(200, 120, 90), spec=.04):
    L = np.array(light) / np.linalg.norm(light)
    V = np.array([0, 0, 1.0])
    Hh = (L + V) / np.linalg.norm(L + V)
    ndl = np.clip(nrm @ L, 0, 1)
    ndh = np.clip(nrm @ Hh, 0, 1)
    a2 = rough ** 4
    D = a2 / (math.pi * (ndh ** 2 * (a2 - 1) + 1) ** 2)
    specular = D * spec * ndl
    col = np.array(base) * (.12 + .88 * ndl)[..., None] + 255 * np.clip(specular, 0, 4)[..., None] * .25
    return np.where(inside[..., None], col, 20.0)


@card("TEX-25")
def claymation_fingerprint(task, wd):
    """Matte clay (roughness .75, baked top-left key), a 12% multiply fingerprint of concentric ridges (sin of
    distance + noise), and squash scaleY .7 / scaleX 1.3 at the 80 ms impact."""
    hh, ww = 120, 160
    inside, nrm = _sphere(hh, ww, 80, 60, 42)
    clay = _ggx_shade(nrm, inside, .75)
    xx, yy = _grid(hh, ww)
    d = np.hypot(xx - 70, yy - 52) + 3 * _noise(xx / 6, yy / 6, 3)
    ridges = .5 + .5 * np.sin(d * 2 * math.pi / 5.0)
    fp = 1 - .12 * ridges
    tex = clay * np.where(inside[..., None], fp[..., None], 1)
    still = _png(wd / "clay.png", tex)
    plain = _png(wd / "clay_plain.png", clay)
    from scipy.ndimage import zoom as ndzoom
    fps = 30
    frames = []
    for k in range(6):
        t = k / fps
        s = 1 - .3 * math.sin(math.pi * min(1, t / .08)) if t <= .08 else 1.0
        sx, sy = 1 + (1 - s) / .3 * .3, s
        z = ndzoom(inside.astype(float), (sy, sx), order=1)
        canvas = np.zeros((hh, ww))
        zh, zw = z.shape
        y0, x0 = hh - zh - (hh - 102) if zh <= hh else 0, (ww - zw) // 2
        y0 = max(0, 102 - zh)
        canvas[y0:y0 + min(zh, hh - y0), max(0, x0):max(0, x0) + min(zw, ww)] = z[:min(zh, hh - y0), max(0, -x0):max(0, -x0) + min(zw, ww)]
        frames.append(np.stack([canvas * 200 + 20] * 3, -1))
    vid = _vid(wd / "squash.mp4", frames, fps)
    O, P, V = _load(still), _load(plain), _rd(vid)
    q = lambda F: _luma(F)
    lit = q(O) * inside
    tl = float(lit[:60, :80].sum() / max(1, inside[:60, :80].sum()))
    br = float(lit[60:, 80:].sum() / max(1, inside[60:, 80:].sum()))
    inside = inside & (q(P) > 60)
    res = q(O)[inside] / np.maximum(1, q(P)[inside])
    amp = float(1 - res.min())
    dd = d[inside]
    corr = float(np.corrcoef(res, ridges[inside])[0, 1])

    def aspect(f):
        m = _luma(f) > 110
        ys, xs = np.nonzero(m)
        return (ys.max() - ys.min() + 1) / (xs.max() - xs.min() + 1)
    asp = [aspect(f) for f in V]
    res_p = q(P)[inside] / np.maximum(1, q(P)[inside])
    return [check("baked top-left key: top-left quadrant brighter than bottom-right", tl > br + 20, [tl, br], "tl>br"),
            check("fingerprint multiply ~12% (max darkening 0.10-0.13)", .10 <= amp <= .13, amp, .12),
            check("darkening follows the concentric ridge pattern (r < -0.9)", corr < -.9, corr, "<-0.9"),
            check("squash at 80 ms: h/w aspect ~0.7/1.3 = 0.54 (+/-0.06)", abs(min(asp) - .7 / 1.3) < .06, min(asp), .538),
            check("negative control: untextured clay has no ridge residual", not (1 - res_p.min()) >= .10, float(1 - res_p.min()), 0)], [still, vid]


@card("TEX-26")
def crayon_paper_craft(task, wd):
    """Crayon-textured shapes (sun, cloud, hill) filled with a noise-threshold texture and a 3 px dark outline."""
    from scipy.ndimage import binary_erosion
    hh, ww = 120, 180
    xx, yy = _grid(hh, ww)
    shapes = [(((xx - 40) ** 2 + (yy - 35) ** 2) < 22 ** 2, (245, 190, 40)),
              (((xx - 120) ** 2 / 3 + (yy - 30) ** 2) < 14 ** 2, (250, 250, 250)),
              (yy > 90 - 20 * np.sin(xx / ww * math.pi), (90, 170, 70))]
    tex = .5 + .5 * _fbm(xx / 1.2, yy / 4, 3, 33)
    img = np.zeros((hh, ww, 3)) + [150, 205, 240]
    flat = img.copy()
    masks = []
    for m, col in shapes:
        fill = m & (tex > .38)
        img[fill] = col
        flat[m] = col
        ring = m & ~binary_erosion(m, iterations=3)
        img[ring] = [40, 30, 30]
        masks.append((m, ring))
    out = _png(wd / "crayon.png", img)
    pin = _png(wd / "flat.png", flat)
    O, F = _load(out), _load(pin)

    def m(I):
        covs, widths = [], []
        for (mm, ring), (_, col) in zip(masks, shapes):
            core = binary_erosion(mm, iterations=5)
            covs.append(float((np.abs(I[core] - col).max(-1) < 3).mean()))
            dark = (np.abs(I - [40, 30, 30]).max(-1) < 3) & mm
            widths.append(float(dark.sum() / max(1, (mm & ~binary_erosion(mm, iterations=1)).sum())))
        return covs, widths
    co, wo = m(O)
    ci, wi = m(F)
    crit = lambda c, w: all(.4 < v < .92 for v in c) and all(2.4 <= v <= 3.6 for v in w)
    return [check("crayon texture: each shape 40-92% covered (not solid)", all(.4 < v < .92 for v in co), co, "0.4-0.92"),
            check("3 px dark outline (outline area / perimeter 2.4-3.6)", all(2.4 <= v <= 3.6 for v in wo), wo, 3),
            check("negative control: flat fills fail", not crit(ci, wi), [ci, wi], "fail")], [out]


@card("TEX-29")
def halftone_sphere_lambert(task, wd):
    """Dot grid (14 px, rmax 6) whose radius = rmax*max(0, n.L) + .4 for a virtual sphere; #f04a2a on #f6efe3; the
    light orbits at 2 rad/s so shading moves dot by dot."""
    hh, ww, ss = 168, 168, 4
    cx = cy = 84
    R = 70
    grid, rmax = 14, 6

    def frame(t, uniform=False):
        a = 2 * t
        L = np.array([math.cos(a), math.sin(a), .8])
        L /= np.linalg.norm(L)
        im = Image.new("RGB", (ww * ss, hh * ss), (0xf6, 0xef, 0xe3))
        d = ImageDraw.Draw(im)
        expect = {}
        for gy in range(grid // 2, hh, grid):
            for gx in range(grid // 2, ww, grid):
                dx, dy = (gx - cx) / R, (gy - cy) / R
                if dx * dx + dy * dy > 1:
                    continue
                n = np.array([dx, dy, math.sqrt(1 - dx * dx - dy * dy)])
                r = 3.4 if uniform else rmax * max(0.0, float(n @ L)) + .4
                expect[(gx, gy)] = r
                d.ellipse([(gx - r) * ss, (gy - r) * ss, (gx + r) * ss, (gy + r) * ss], fill=(0xf0, 0x4a, 0x2a))
        return np.asarray(im.resize((ww, hh), Image.BOX)).astype(float), expect
    fps = 30
    frs, exps = zip(*[frame(k / fps) for k in range(16)])
    out = _vid(wd / "halftone_sphere.mp4", list(frs), fps)
    O = _rd(out)
    uni, uexp = frame(0, uniform=True)

    def areas(f, ex):
        ink = np.clip((_hex("#f6efe3")[1] - f[..., 1]) / (_hex("#f6efe3")[1] - 0x4a), 0, 1)
        meas, pred = [], []
        for (gx, gy), r in ex.items():
            meas.append(ink[gy - 7:gy + 7, gx - 7:gx + 7].sum())
            pred.append(math.pi * r * r)
        return np.array(meas), np.array(pred)
    m0, p0 = areas(O[0], exps[0])
    corr = float(np.corrcoef(m0, p0)[0, 1])
    slope = float((m0 * p0).sum() / (p0 * p0).sum())

    def light_angle(f, ex):
        m, _ = areas(f, ex)
        keys = list(ex.keys())
        vx = sum(mm * (k[0] - cx) for mm, k in zip(m, keys))
        vy = sum(mm * (k[1] - cy) for mm, k in zip(m, keys))
        return math.atan2(vy, vx)
    a0, a1 = light_angle(O[0], exps[0]), light_angle(O[15], exps[15])
    turn = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
    mu, pu = areas(uni, exps[0])
    cu = float(np.corrcoef(mu, p0)[0, 1]) if mu.std() > 1e-6 else 0.0
    return [check("dot area follows pi*r^2 of the Lambert radius (r > 0.98)", corr > .98, corr, ">0.98"),
            check("measured/predicted area ~1 (0.85-1.15)", .85 <= slope <= 1.15, slope, 1.0),
            check("shading turns with the light: 0.5 s at 2 rad/s = 1.0 rad (+/-0.15)", abs(turn - 1.0) < .15, turn, 1.0),
            check("negative control: a uniform dot grid does not follow Lambert", not cu > .98, cu, "<0.98")], [out]


def _screen(h, w, pitch, angle_deg, radius_fn, ss=3):
    """Render a rotated dot screen; radius_fn(x, y) gives each dot radius. Returns coverage in 0..1 and dot list."""
    im = Image.new("L", (w * ss, h * ss), 0)
    d = ImageDraw.Draw(im)
    a = math.radians(angle_deg)
    ca, sa = math.cos(a), math.sin(a)
    dots = []
    span = int(max(w, h) * 1.5 / pitch) + 2
    for i in range(-span, span):
        for j in range(-span, span):
            x = w / 2 + (i * ca - j * sa) * pitch
            y = h / 2 + (i * sa + j * ca) * pitch
            if -pitch < x < w + pitch and -pitch < y < h + pitch:
                r = radius_fn(x, y)
                dots.append((x, y, r))
                if r > .05:
                    d.ellipse([(x - r) * ss, (y - r) * ss, (x + r) * ss, (y + r) * ss], fill=255)
    return np.asarray(im.resize((w, h), Image.BOX)).astype(float) / 255, dots


@card("TEX-32")
def halftone_ripple_moire(task, wd):
    """Dot screen whose radius r = rmax*(.5 + .5 sin(k d - w t)) rides a radial wave (1 ring / 0.5 s), overprinted
    (multiply) by a second screen rotated 30 deg in another ink: overprint moire."""
    hh, ww, pitch, rmax = 120, 160, 8, 3.6
    lam = 32.0
    k_, om = 2 * math.pi / lam, 2 * math.pi / .5

    def frame(t):
        rf = lambda x, y: rmax * (.5 + .5 * math.sin(k_ * math.hypot(x - ww / 2, y - hh / 2) - om * t))
        c1, d1 = _screen(hh, ww, pitch, 15, rf)
        c2, _ = _screen(hh, ww, pitch, 45, lambda x, y: 1.6)
        cyan, mag = np.array([0, 160, 230]) / 255, np.array([230, 0, 140]) / 255
        img = 255 * (1 - c1[..., None] * (1 - cyan)) * (1 - c2[..., None] * (1 - mag))
        return img, d1
    fps = 32
    frames, dots = zip(*[frame(k / fps) for k in range(8)])
    out = _vid(wd / "ripple.mp4", list(frames), fps)
    O = _rd(out)

    def corr_with(f, t):
        cov1 = np.clip(1 - f[..., 0] / 255, 0, 1)
        meas, pred = [], []
        for (x, y, r) in dots[0]:
            if 6 < x < ww - 6 and 6 < y < hh - 6:
                meas.append(cov1[int(y) - 2:int(y) + 3, int(x) - 2:int(x) + 3].sum())
                pred.append((.5 + .5 * math.sin(k_ * math.hypot(x - ww / 2, y - hh / 2) - om * t)) ** 2)
        return float(np.corrcoef(meas, pred)[0, 1])
    c_now = corr_with(O[0], 0.0)
    c_half = corr_with(O[0], .25)
    c_later = corr_with(O[4], 4 / fps)
    spec = np.abs(np.fft.fftshift(np.fft.fft2(1 - O[0][..., 2] / 255 - (1 - O[0][..., 2] / 255).mean())))
    cyc, cxc = np.array(spec.shape) // 2
    spec[cyc - 3:cyc + 4, cxc - 3:cxc + 4] = 0
    iy, ix = np.unravel_index(np.argmax(spec), spec.shape)
    ang = (math.degrees(math.atan2((iy - cyc) / hh, (ix - cxc) / ww)) + 360) % 90
    flat, _ = _screen(hh, ww, pitch, 15, lambda x, y: rmax / 2)
    flat_img = _png(wd / "input_uniform_screen.png", 255 * (1 - flat[..., None] * (1 - np.array([0, 160, 230]) / 255)))
    flat_corr = float(np.nan_to_num(corr_with(_load(flat_img), 0.0)))
    return [check("ink-1 dot areas follow the radial wave at t (r > 0.85)", c_now > .85, c_now, ">0.85"),
            check("wave moves: half a ring later the pattern is anti-correlated (r < -0.5)", c_half < -.5, c_half, "<-0.5"),
            check("frame at t=0.125 s matches the formula at its own time (r > 0.85)", c_later > .85, c_later, ">0.85"),
            check("second screen (magenta) at 45 deg dominates the blue-channel spectrum", abs(ang - 45) < 6 or abs(ang - 45) > 84, ang, 45),
            check("negative control: an untreated flat plate has no wave correlation", not flat_corr > .85, flat_corr, 0)], [out]


@card("TEX-33")
def halftone_light_bands(task, wd):
    """Diagonal gradient bands at -35 deg filled with a 7 px halftone dot screen at .4 opacity, radially faded towards
    the centre and drifting 8 px/s."""
    hh, ww = 108, 192
    xx, yy = _grid(hh, ww)
    a = math.radians(-35)
    fade = np.clip(np.hypot((xx - ww / 2) / (ww / 2), (yy - hh / 2) / (hh / 2)) - .25, 0, 1) ** 1.2
    bg = np.array([14, 16, 30])

    def frame(t):
        u = (xx * math.cos(a) + yy * math.sin(a)) + 8 * t
        band = .5 + .5 * np.sin(2 * math.pi * u / 48)
        cov, _ = _screen(hh, ww, 7, 0, lambda x, y: 3.2, ss=2)
        lay = cov * band * fade * .4
        return bg + lay[..., None] * (np.array([255, 220, 160]) - bg), u
    fps = 30
    frames = [frame(k / fps)[0] for k in range(31)]
    out = _vid(wd / "bands.mp4", frames, fps)
    O = _rd(out)
    lum = [_blur(_luma(f) - _luma(bg), 3.5) for f in O]
    centre = float(lum[0][hh // 2 - 8:hh // 2 + 8, ww // 2 - 12:ww // 2 + 12].mean())
    corner = float(lum[0][0:20, 0:30].mean())
    sel = fade > .5
    field = lum[0][sel] / fade[sel]
    amps = []
    for deg in range(-90, 90):
        r = math.radians(deg)
        uu = xx[sel] * math.cos(r) + yy[sel] * math.sin(r)
        amps.append(abs(np.sum((field - field.mean()) * np.exp(-2j * math.pi * uu / 48))))
    ang = float(range(-90, 90)[int(np.argmax(amps))])
    best, bt = 1e9, None
    for s in np.arange(4, 12.1, .25):
        sh = (lum[0] - _blur(_luma(frame(s / 8.0)[0]) - _luma(bg), 3.5))
        e = float(np.abs(lum[30] - _blur(_luma(frame(s / 8.0)[0]) - _luma(bg), 3.5)).mean())
        if e < best:
            best, bt = e, s
    flat = _rd(_vid(wd / "input.mp4", [np.zeros((hh, ww, 3)) + bg] * 2))[0]
    fl = _blur(_luma(flat) - _luma(bg), 3.5)
    fc, fk = float(fl[hh // 2 - 8:hh // 2 + 8, ww // 2 - 12:ww // 2 + 12].mean()), float(fl[0:20, 0:30].mean())
    return [check("radial fade: centre glow < 20% of corner", centre < .2 * corner, [centre, corner], "<0.2"),
            check("bands run at -35 deg (matched-filter band normal within +/-4 deg)", abs(ang + 35) <= 4, ang, -35),
            check("drift 8 px/s: best-matching shift after 1 s = 8 px (+/-1)", abs(bt - 8) <= 1, bt, 8),
            check("negative control: the untreated ground fails the fade criterion", not fc < .2 * fk, [fc, fk], "fail")], [out]


@card("TEX-34")
def halftone_macro_image(task, wd):
    """Greyscale photo -> per-cell centre luma -> dot radius (dark = big): the photo becomes a printed poster."""
    src = _photo(120, 160)
    g = _luma(src)
    pin = _png(wd / "grey.png", np.stack([g] * 3, -1))
    cell = 8
    im = Image.new("L", (160 * 4, 120 * 4), 255)
    d = ImageDraw.Draw(im)
    for cy in range(0, 120, cell):
        for cx in range(0, 160, cell):
            v = g[cy + cell // 2, cx + cell // 2] / 255
            r = math.sqrt((1 - v) * cell * cell / math.pi) * 4
            d.ellipse([(cx + 4) * 4 - r, (cy + 4) * 4 - r, (cx + 4) * 4 + r, (cy + 4) * 4 + r], fill=0)
    ht = np.asarray(im.resize((160, 120), Image.BOX)).astype(float)
    out = _png(wd / "halftone.png", np.stack([ht] * 3, -1))
    O, I = _load(out)[..., 0], _load(pin)[..., 0]
    binary = lambda A: float(((A < 40) | (A > 215)).mean())
    cov = [(1 - O[cy:cy + cell, cx:cx + cell] / 255).mean() for cy in range(0, 120, cell) for cx in range(0, 160, cell)]
    dark = [1 - g[cy + 4, cx + 4] / 255 for cy in range(0, 120, cell) for cx in range(0, 160, cell)]
    corr = float(np.corrcoef(cov, dark)[0, 1])
    return [check("print-like: > 75% of pixels pure ink or paper", binary(O) > .75, binary(O), ">0.75"),
            check("cell ink coverage tracks (1 - cell luma) (r > 0.95)", corr > .95, corr, ">0.95"),
            check("negative control: the greyscale photo is continuous-tone", not binary(I) > .75, binary(I), "<0.75")], [out]


BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]])


@card("TEX-35")
def bayer_dither_sky(task, wd):
    """Sky gradient quantised to 4 indigo/purple bands with the 4x4 Bayer rule: v = y/H*(n-1), i = floor(v), pick
    band i+1 when frac(v) > (B[y&3][x&3]+.5)/16; 1-2 px seeded stars twinkle in steps at 4 fps."""
    hh, ww = 96, 128
    pal = np.array([_hex(c) for c in ("#1b1440", "#2f2370", "#5a3a9a", "#8a5ab8")])
    xx, yy = _grid(hh, ww)
    v = yy / hh * (len(pal) - 1)
    i = np.floor(v).astype(int)
    up = (v - i) > (BAYER[yy.astype(int) & 3, xx.astype(int) & 3] + .5) / 16
    idx = np.clip(i + up, 0, len(pal) - 1)
    sky = pal[idx]
    rng = _rng(23)
    stars = [(int(rng.integers(0, ww)), int(rng.integers(0, hh // 2)), int(rng.integers(0, 4))) for _ in range(14)]
    fps = 30
    frames = []
    for k in range(30):
        f = sky.copy()
        step = math.floor(k / fps * 4)
        for (x, y, ph) in stars:
            if (step + ph) % 2 == 0:
                f[y, x] = 255
        frames.append(f)
    out = _vid(wd / "bayer_sky.mp4", frames, fps)
    O = _rd(out)
    starmask = np.zeros((hh, ww), bool)
    for (x, y, _) in stars:
        starmask[y, x] = True
    cols = {tuple(c) for c in O[0][~starmask].reshape(-1, 3).astype(int)}
    exp = pal[idx]
    mism = int((np.abs(O[0] - exp).max(-1) > 0)[~starmask].sum())
    changes = [k for k in range(1, 30) if np.abs(O[k] - O[k - 1]).max() > 0]
    expect_changes = [k for k in range(1, 30) if math.floor(k / fps * 4) != math.floor((k - 1) / fps * 4)]
    smooth = pal[0] * (1 - (yy / hh)[..., None]) + pal[-1] * (yy / hh)[..., None]
    ncol = len({tuple(c) for c in _u8(smooth).reshape(-1, 3)})
    return [check("only the 4 palette colours in the sky", len(cols) <= 4, len(cols), 4),
            check("every pixel follows the Bayer threshold rule (0 mismatches)", mism == 0, mism, 0),
            check("stars change only on 4 fps steps", changes == expect_changes, changes, expect_changes),
            check("negative control: a smooth gradient uses many colours", not ncol <= 4, ncol, ">4")], [out]


@card("TEX-36")
def dither_threshold_sweep(task, wd):
    """1-bit Bayer dither of orange on black filling a region; the threshold animates 0->1 over 600 ms; the Bayer
    matrix is scaled x2 into an 8 px cell and drawn pixelated (no smoothing)."""
    hh, ww = 64, 96
    xx, yy = _grid(hh, ww)
    B2 = np.kron(BAYER, np.ones((2, 2)))
    thr = (B2[yy.astype(int) % 8, xx.astype(int) % 8] + .5) / 16
    region = (xx >= 8) & (xx < 88) & (yy >= 8) & (yy < 56)
    orange = _hex("#ff7a1a")
    fps = 30
    n = 19
    frames, tv = [], []
    for k in range(n):
        t = min(1.0, (k / fps) / .6)
        tv.append(t)
        on = region & (thr < t)
        f = np.zeros((hh, ww, 3))
        f[on] = orange
        frames.append(f)
    out = _vid(wd / "dither_sweep.mp4", frames, fps)
    O = _rd(out)
    covs = [float((np.abs(f - orange).max(-1) < 1)[region].mean()) for f in O]
    err = max(abs(c - t) for c, t in zip(covs, tv))
    cols = {tuple(c) for f in O for c in f.reshape(-1, 3).astype(int)}
    blocks = all(np.array_equal(f[0::2, 0::2], f[1::2, 1::2]) for f in O)
    fade = [np.where(region[..., None], orange * t, 0) for t in tv]
    ncol = len({tuple(c) for f in fade for c in _u8(f).reshape(-1, 3)})
    return [check("coverage tracks the threshold (max error <= 1/16)", err <= 1 / 16 + 1e-9, err, "<=0.0625"),
            check("1-bit: only orange and black", len(cols) == 2, len(cols), 2),
            check("pixelated x2 Bayer: 2x2 blocks uniform", blocks, blocks, True),
            check("sweep completes in 600 ms (frame 18 fully on)", covs[18] == 1.0, covs[18], 1.0),
            check("negative control: a smooth opacity fade is not 1-bit", not ncol == 2, ncol, ">2")], [out]


@card("TEX-37")
def riso_grain_fill(task, wd):
    """Risograph look: a turbulence threshold mask (freq .9) inside flat shapes printed in 2 inks (blue, fluoro pink)
    multiplied on paper, with 2 px / 1 px misregistration of the second ink."""
    hh, ww = 120, 160
    xx, yy = _grid(hh, ww)
    paper = np.array([246, 242, 232.0])
    blue, pink = _hex("#0078bf"), _hex("#ff48b0")
    sh1 = ((xx - 60) ** 2 + (yy - 60) ** 2) < 34 ** 2
    sh2_design = (np.abs(xx - 100) < 30) & (np.abs(yy - 64) < 26)
    reg = (2, 1)
    sh2 = np.roll(np.roll(sh2_design, reg[1], 0), reg[0], 1)
    turb1 = .5 + .5 * _fbm(xx * .9, yy * .9, 3, 41)
    turb2 = .5 + .5 * _fbm(xx * .9 + 50, yy * .9, 3, 43)
    p1 = sh1 & (turb1 > .42)
    p2 = sh2 & (turb2 > .42)
    plate1 = _png(wd / "plate_blue.png", np.where(p1[..., None], 0, 255) * np.ones(3))
    plate2 = _png(wd / "plate_pink.png", np.where(p2[..., None], 0, 255) * np.ones(3))
    img = paper * np.where(p1[..., None], blue / 255, 1) * np.where(p2[..., None], pink / 255, 1)
    out = _png(wd / "riso.png", img)
    O = _load(out)
    P1 = _load(plate1)[..., 0] < 128
    P2 = _load(plate2)[..., 0] < 128
    comp = paper * np.where(P1[..., None], blue / 255, 1) * np.where(P2[..., None], pink / 255, 1)
    cons = float(np.abs(O - comp).max())
    cov1 = float(P1[sh1].mean())
    cov2 = float(P2[sh2].mean())
    import cv2
    dx, dy = _phase(sh2_design.astype(float), _blur(P2.astype(float), 2))
    flat = _png(wd / "input_flat.png", paper * np.where(sh1[..., None], blue / 255, 1))
    flat_cov = float((np.abs(_load(flat) - paper * blue / 255).max(-1) < 2)[sh1].mean())
    return [check("grain: each ink covers 40-90% of its shape", .4 < cov1 < .9 and .4 < cov2 < .9, [cov1, cov2], "0.4-0.9"),
            check("composite = multiply of the two plates on paper (max error <= 1)", cons <= 1, cons, 0),
            check("pink plate misregistered (+2, +1) px from its design (+/-0.5)", abs(dx - 2) < .5 and abs(dy - 1) < .5, [dx, dy], [2, 1]),
            check("negative control: a flat shape fill has full coverage", not (.4 < flat_cov < .9), flat_cov, 1.0)], [out, plate1, plate2]


# ============================================================================ TEXTURE: glass, metal, orbs
def _rounded(h, w, box, rad, ss=4):
    im = Image.new("L", (w * ss, h * ss), 0)
    x0, y0, x1, y1 = box
    ImageDraw.Draw(im).rounded_rectangle([x0 * ss, y0 * ss, x1 * ss, y1 * ss], radius=rad * ss, fill=255)
    return np.asarray(im.resize((w, h), Image.BOX)).astype(float) / 255


def _saturate(img, s):
    l = _luma(img)[..., None]
    return np.clip(l + (img - l) * s, 0, 255)


def _starfield(h, w, seed=29):
    xx, yy = _grid(h, w)
    bg = np.stack([40 + 60 * xx / w, 20 + 30 * yy / h, 90 + 80 * (1 - xx / w)], -1)
    bg += 50 * np.exp(-((xx - w * .3) ** 2 + (yy - h * .4) ** 2) / (2 * (h * .3) ** 2))[..., None] * np.array([1, .3, .6])
    rng = _rng(seed)
    for _ in range(int(h * w / 60)):
        x, y = int(rng.integers(0, w)), int(rng.integers(0, h))
        bg[y, x] = 250
    return np.clip(bg, 0, 255)


@card("TEX-40")
def luxury_glass_cards(task, wd):
    """Frosted glass cards over a live gradient with a star pattern: backdrop blur(22px) saturate(150%), fill
    white .16 -> .035, radius 30, 1 px inset top highlight .45, soft lift shadow; three cards at depths 1/.7/.45
    move in parallax with the camera."""
    hh, ww = 135, 240
    back = _starfield(hh, ww)
    pin = _png(wd / "backdrop.png", back)
    cards = [(1.0, (150, 40, 220, 110)), (.7, (85, 30, 145, 95)), (.45, (20, 45, 75, 105))]

    def frame(cam):
        f = back.copy()
        for depth, (x0, y0, x1, y1) in sorted(cards, key=lambda c: c[0]):
            dx = -cam * depth
            box = (x0 + dx, y0, x1 + dx, y1)
            m = _rounded(hh, ww, box, 14)
            frost = _saturate(_blur(f, 22), 1.5)
            sh = _blur(np.roll(_rounded(hh, ww, box, 14), 8, 0), 6) * .35
            f = f * (1 - sh[..., None])
            yy = np.arange(hh)[:, None] * np.ones((1, ww))
            tint = np.clip(.16 - (.16 - .035) * (yy - y0) / max(1, y1 - y0), .035, .16)[..., None]
            card_ = frost * (1 - tint) + 255 * tint
            top = np.zeros((hh, ww))
            top[int(round(y0)) + 1, int(round(box[0])) + 10:int(round(box[2])) - 10] = .45
            card_ = card_ * (1 - top[..., None]) + 255 * top[..., None]
            f = f * (1 - m[..., None]) + card_ * m[..., None]
        return f
    frames = [frame(c) for c in (0.0, 20.0)]
    out = _vid(wd / "glass_cards.mp4", frames)
    O = _rd(out)
    B = _load(pin)
    x0, y0, x1, y1 = cards[0][1]
    inner = (slice(y0 + 12, y1 - 12), slice(x0 + 12, x1 - 12))
    outside = (slice(5, 30), slice(100, 140))
    hf_in, hf_out = _hf(O[0][inner]), _hf(O[0][outside])
    sat = lambda a: float((a.max(-1) - a.min(-1)).mean())
    s_ratio = sat(O[0][inner]) / max(1e-6, sat(_blur(B, 22)[inner]))
    hl = float(_luma(O[0][y0 + 1, x0 + 14:x1 - 14]).mean() - _luma(O[0][y0 + 4, x0 + 14:x1 - 14]).mean())
    def cx(k, card_):
        x0_, y0_, x1_, _ = card_[1]
        row = _luma(O[k][y0_ + 1]) - _luma(O[k][y0_ + 4])
        lo = int(x0_ - 25)
        cols = np.nonzero(row[max(0, lo):x1_] > 20)[0]
        return float(cols.min() + max(0, lo))
    shifts = [cx(0, c) - cx(1, c) for c in cards]
    ratios = [shifts[1] / shifts[0], shifts[2] / shifts[0]]
    hb = _hf(B[inner]) / max(1e-6, _hf(B[outside]))
    return [check("backdrop blur: high-frequency energy inside the card < 35% of outside", hf_in < .35 * hf_out, [hf_in, hf_out], "<0.35"),
            check("saturate(150%): card chroma > 1.2x the blurred backdrop", s_ratio > 1.2, s_ratio, ">1.2"),
            check("1 px top highlight brighter than 3 px below (+10)", hl > 10, hl, ">10"),
            check("parallax: depth ratios .7 and .45 (+/-0.08)", abs(ratios[0] - .7) < .08 and abs(ratios[1] - .45) < .08, ratios, [.7, .45]),
            check("negative control: the backdrop alone is not frosted (HF ratio >= 0.35)", not hb < .35, hb, ">=0.35")], [out]


@card("TEX-44")
def liquid_glass_control(task, wd):
    """Canvas liquid glass: the body is the backdrop blurred 14 px, a 12 px edge band shows the backdrop magnified
    1.06x about the control centre (slightly blurred) to fake refraction, milky fill, 1 px bright rim, pastel aura."""
    from scipy.ndimage import binary_erosion, affine_transform
    hh, ww = 120, 200
    xx, yy = _grid(hh, ww)
    back = np.stack([128 + 100 * np.sin(xx / 6), 128 + 100 * np.sin(yy / 5 + xx / 17), 128 + 90 * np.cos(xx / 11)], -1)
    pin = _png(wd / "backdrop.png", back)
    box = (40, 30, 160, 90)
    m = _rounded(hh, ww, box, 30) > .5
    band = m & ~binary_erosion(m, iterations=12)
    body = binary_erosion(m, iterations=12)
    cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
    s = 1.06
    mag = np.stack([affine_transform(back[..., c], [1 / s, 1 / s], offset=[cy - cy / s, cx - cx / s], order=1, mode="nearest") for c in range(3)], -1)
    mag = _blur(mag, .8)
    aura = _blur(np.roll(m.astype(float), 6, 0), 10)[..., None] * np.array([200, 170, 255])
    f = back * (1 - .25 * _blur(np.roll(m.astype(float), 6, 0), 10)[..., None]) + .25 * aura
    f = np.where(body[..., None], _blur(back, 14) * .8 + 255 * .2, f)
    f = np.where(band[..., None], mag * .85 + 255 * .15, f)
    rim = m & ~binary_erosion(m, iterations=1)
    f[rim] = f[rim] * .3 + 255 * .7
    out = _png(wd / "liquid_glass.png", f)
    O, B = _load(out), _load(pin)
    inner_band = band & binary_erosion(m, iterations=2)
    plain = _blur(back, .8)

    def corr(a, b):
        hp = lambda z: _luma(z) - _blur(_luma(z), 3)
        return float(np.corrcoef(hp(a)[inner_band], hp(b)[inner_band])[0, 1])
    c_mag, c_plain = corr(O, mag), corr(O, plain)
    i_mag, i_plain = corr(B, mag), corr(B, plain)
    hf_body = _hf(O[body]) if False else float(np.abs(_luma(O) - _blur(_luma(O), 1.5))[binary_erosion(body, iterations=3)].mean())
    hf_back = float(np.abs(_luma(B) - _blur(_luma(B), 1.5))[binary_erosion(body, iterations=3)].mean())
    rimv = float(_luma(O)[rim].mean() - _luma(O)[inner_band].mean())
    return [check("edge band matches the 1.06x magnified backdrop better than the unmagnified one", c_mag > c_plain + .05, [c_mag, c_plain], "mag>plain"),
            check("body blurred 14 px: HF < 20% of the backdrop's", hf_body < .2 * hf_back, [hf_body, hf_back], "<0.2"),
            check("1 px bright rim (+30 over the band)", rimv > 30, rimv, ">30"),
            check("negative control: the raw backdrop band matches the unmagnified version", not (i_mag > i_plain + .05), [i_mag, i_plain], "plain>=mag")], [out]


@card("TEX-45")
def frosted_letters(task, wd):
    """Clip a blurred (30 px) backdrop to the shaped text path, lighten it with a white .25 overlay and add a bright
    1 px top rim at .7; outside the letters the backdrop is untouched. Arabic words are clipped as one shaped word."""
    from scipy.ndimage import binary_erosion
    hh, ww = 120, 240
    back = _starfield(hh, ww, 31)
    pin = _png(wd / "backdrop.png", back)
    m = _text_mask("GLASS", 70, (hh, ww)) > .5
    ar = None
    fp = FONTS / "Lalezar-Regular.ttf"
    if fp.exists():
        f_ar = ImageFont.truetype(str(fp), 40, layout_engine=ImageFont.Layout.RAQM)
        ar = _text_mask("زجاج", 40, (hh, ww), xy=(8, 2), font=f_ar, direction="rtl") > .5
        m = m | ar
    frost = _blur(back, 30) * 1.2
    fill = frost * .75 + 255 * .25
    top = m & ~np.roll(m, 1, 0)
    img = np.where(m[..., None], fill, back)
    img[top] = img[top] * .3 + 255 * .7
    out = _png(wd / "frosted_letters.png", img)
    O, B = _load(out), _load(pin)
    core = binary_erosion(m, iterations=2)
    hf_in = float(np.abs(_luma(O) - _blur(_luma(O), 1.5))[core].mean())
    hf_out = float(np.abs(_luma(B) - _blur(_luma(B), 1.5))[core].mean())
    lighter = float(_luma(O)[core].mean() - _luma(_blur(B, 30))[core].mean())
    lighter_b = float(_luma(B)[core].mean() - _luma(_blur(B, 30))[core].mean())
    far = ~np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))).astype(bool)
    untouched = float(np.abs(O - B)[far].max())
    comps = _components(ar)[1] if ar is not None else 0
    f_basic = ImageFont.truetype(str(fp), 40, layout_engine=ImageFont.Layout.BASIC) if fp.exists() else None
    comps_basic = _components(_text_mask("زجاج", 40, (hh, ww), xy=(8, 2), font=f_basic) > .5)[1] if f_basic else 0
    return [check("letters show a blurred backdrop (HF inside < 25% of the raw backdrop there)", hf_in < .25 * hf_out, [hf_in, hf_out], "<0.25"),
            check("frost lightened (+20% and white .25): inside luma > blurred backdrop + 25", lighter > 25, lighter, ">25"),
            check("backdrop outside the letters untouched (max diff 0)", untouched == 0, untouched, 0),
            check("Arabic word clipped as one shaped word: fewer pieces than unshaped letters", comps < comps_basic, [comps, comps_basic], "shaped<basic"),
            check("negative control: the raw backdrop inside the letters is not lightened frost", not lighter_b > 25, lighter_b, "<=25")], [out]


GOLD = [("#fff4d6", 0), ("#f0d793", 16), ("#c9a24a", 40), ("#8a6424", 56), ("#b88d3a", 68), ("#f2dc9c", 86), ("#fff4d6", 100)]


def _gold_grad(t):
    t = np.clip(t, 0, 1) * 100
    stops = [(p, _hex(c)) for c, p in GOLD]
    out = np.zeros(np.shape(t) + (3,))
    for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
        sel = (t >= p0) & (t <= p1)
        u = ((t - p0) / (p1 - p0))[..., None]
        out[sel] = (c0 * (1 - u) + c1 * u)[sel]
    return out


@card("TEX-47")
def gold_moving_sheen(task, wd):
    """Gold word from four stacked copies: glow (#c9a24a blur 26 at .42), engraved edge (#4a3110, 4 px offset), the
    7-stop 180 deg metal gradient clipped to the text, and a 105 deg masked sheen (#fffaf0) in a +/-9% band sweeping
    across with cubic-bezier(.65,0,.35,1)."""
    hh, ww = 120, 280
    m = _text_mask("GOLD", 80, (hh, ww))
    ys, xs = np.nonzero(m > .5)
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    xx, yy = _grid(hh, ww)
    grad = _gold_grad((yy - y0) / max(1, y1 - y0))
    bg = np.array([18, 14, 10.0])
    ease = _bez(.65, 0, .35, 1)
    a = math.radians(105)
    axis = (xx * math.cos(a - math.pi / 2) + yy * math.sin(a - math.pi / 2))
    amin, amax = axis[m > .5].min(), axis[m > .5].max()
    frames, centres = [], []
    for k in range(10):
        p = ease(k / 9)
        c = -.2 + 1.4 * p
        centres.append(c)
        u = (axis - amin) / (amax - amin)
        band = np.clip(1 - np.abs(u - c) / .09, 0, 1)
        glow = np.clip(_blur(m, 26 / 2.5) * 2.5, 0, 1)[..., None] * .42
        f = bg * (1 - glow) + _hex("#c9a24a") * glow
        edge = np.roll(m, 4, 0)[..., None]
        f = f * (1 - edge) + _hex("#4a3110") * edge
        metal = grad * (1 - band[..., None]) + _hex("#fffaf0") * band[..., None]
        f = f * (1 - m[..., None]) + metal * m[..., None]
        frames.append(f)
    out = _vid(wd / "gold.mp4", frames)
    O = _rd(out)
    rows = {p: int(round(y0 + (y1 - y0) * p / 100)) for _, p in GOLD[1:-1]}
    errs = []
    first = O[0]
    for c, p in GOLD[1:-1]:
        r = rows[p]
        sel = m[r] > .98
        errs.append(float(np.abs(first[r][sel].mean(0) - _hex(c)).max()))
    edge_px = (np.roll(m, 4, 0) > .9) & (m < .02)
    edge_err = float(np.abs(O[0][edge_px].mean(0) - _hex("#4a3110")).max())

    def sheen_pos(f):
        u = (axis - amin) / (amax - amin)
        br = (_luma(f) > 245) & (m > .98)
        return float(u[br].mean()) if br.any() else -1
    pos = [sheen_pos(f) for f in O[3:7]]
    flat = np.where(m[..., None] > .5, _hex("#c9a24a"), bg)
    ferr = [float(np.abs(flat[rows[p]][m[rows[p]] > .98].mean(0) - _hex(c)).max()) for c, p in GOLD[1:-1]]
    return [check("metal gradient hits each inner stop colour on its row (max error <= 14)", max(errs) <= 14, errs, "<=14"),
            check("engraved edge #4a3110 shows 4 px below the letters (error <= 12)", edge_err <= 12, edge_err, "<=12"),
            check("sheen sweeps across along 105 deg (band position increases)", all(b > a_ + .02 for a_, b in zip(pos, pos[1:])) and pos[0] >= 0, pos, "increasing"),
            check("negative control: a flat gold fill misses the stops", not max(ferr) <= 14, ferr, ">14")], [out]


@card("TEX-48")
def glossy_orb(task, wd):
    """Glossy 2D orb from stacked radial gradients: body #5b9bff -> #1239a0, white blurred elliptical specular top-left
    at .6, a #c9f4ff rim light 3 px, a small orange inner hotspot and an outer purple glow."""
    hh, ww, R = 160, 160, 50
    cx = cy = 80
    xx, yy = _grid(hh, ww)
    d = np.hypot(xx - cx, yy - cy)
    disc = np.clip(R + .5 - d, 0, 1)[..., None]
    body = _hex("#5b9bff") * (1 - np.clip(np.hypot(xx - cx + 15, yy - cy + 15) / (R * 1.6), 0, 1))[..., None] + \
        _hex("#1239a0") * np.clip(np.hypot(xx - cx + 15, yy - cy + 15) / (R * 1.6), 0, 1)[..., None]
    rim = np.clip(1 - np.abs(d - (R - 1.5)) / 1.5, 0, 1)[..., None] * .8
    body = body * (1 - rim) + _hex("#c9f4ff") * rim
    spec = _blur((((xx - (cx - 18)) / 16) ** 2 + ((yy - (cy - 22)) / 9) ** 2 < 1).astype(float), 3)[..., None] * .6
    body = body * (1 - spec) + 255 * spec
    hot = _blur((np.hypot(xx - cx - 14, yy - cy - 16) < 5).astype(float), 2)[..., None] * .5
    body = body * (1 - hot) + _hex("#ff9a3c") * hot
    bg = np.array([12, 10, 24.0])
    glow = np.clip(_blur((d < R).astype(float), 8) * 1.4, 0, 1)[..., None] * (d > R)[..., None] * .7
    f = bg * (1 - glow) + _hex("#8a4dff") * glow
    f = f * (1 - disc) + body * disc
    out = _png(wd / "orb.png", f)
    O = _load(out)
    L = _luma(O)
    inside = d < R - 1
    iy, ix = np.unravel_index(np.argmax(np.where(inside, L, 0)), L.shape)
    lower = yy > cy + 10
    rim_l = float(L[(np.abs(d - (R - 1.5)) < 1) & lower].mean())
    in_l = float(L[(np.abs(d - (R - 9)) < 1) & lower].mean())
    g = O[(np.abs(d - (R + 5)) < 1)].mean(0)
    flat = np.where((d < R)[..., None], _hex("#5b9bff"), bg)
    Lf = _luma(flat)
    fy, fx_ = np.unravel_index(np.argmax(np.where(inside, Lf + 1e-3 * (xx + yy), 0)), Lf.shape)
    return [check("specular highlight in the top-left quadrant", ix < cx - 5 and iy < cy - 5, [int(ix), int(iy)], "top-left"),
            check("rim light: edge ring brighter than 8 px inside (lower half, +15)", rim_l > in_l + 15, [rim_l, in_l], "rim>inner"),
            check("outer purple glow just outside the orb (B > R > bg + 20)", g[2] > g[0] > bg[0] + 20, g.tolist(), "purple"),
            check("negative control: a flat disc has no top-left specular", not (fx_ < cx - 5 and fy < cy - 5), [int(fx_), int(fy)], "not top-left")], [out]


@card("TEX-59")
def brick_light_map(task, wd):
    """Seeded procedural brick (rows 24 px, odd rows offset half, 3 px mortar, per-brick tone, fine grain) multiplied
    by a light map at 1/4 res = ambient #1b1f30 + emission blurred 40 px x1.0 + 140 px x1.95; the wall takes the neon
    sign's colour while the mortar stays dark."""
    from scipy.ndimage import zoom as ndzoom
    hh, ww = 192, 320

    def brick(seed=20261016):
        rng = _rng(seed)
        img = np.zeros((hh, ww, 3))
        mortar = np.zeros((hh, ww), bool)
        bw, bh = 48, 24
        for r in range(hh // bh + 1):
            off = (bw // 2) * (r % 2)
            for c in range(-1, ww // bw + 2):
                x0, y0 = c * bw + off, r * bh
                tone = .8 + .35 * rng.random()
                img[y0:y0 + bh, max(0, x0):max(0, x0 + bw)] = np.array([150, 80, 60]) * tone
                mortar[y0:y0 + 3, :] = True
                if 0 <= x0 < ww:
                    mortar[y0:y0 + bh, x0:x0 + 3] = True
        img[mortar] = [40, 38, 36]
        img = img + rng.normal(0, 4, (hh, ww, 1))
        return np.clip(img, 0, 255), mortar
    b, mortar = brick()
    b2, _ = brick()
    emis = np.zeros((hh // 4, ww // 4, 3))
    emis[18:22, 25:55] = _hex("#ff2fd0") / 255 * 3
    lm = _hex("#1b1f30") / 255 + (_blur(emis, 40 / 4 / 2) * 1.0 + _blur(emis, 140 / 4 / 2) * 1.95) * 10
    lm = np.stack([ndzoom(lm[..., c], 4, order=1) for c in range(3)], -1)
    out = _png(wd / "lit_brick.png", b * lm)
    pin = _png(wd / "brick.png", b)
    O, I = _load(out), _load(pin)
    near = np.zeros((hh, ww), bool)
    near[50:110, 80:240] = True
    nb = near & ~mortar
    nm = near & mortar
    hue = lambda A: float(((A[..., 0] + A[..., 2]) / 2 - A[..., 1])[nb].mean())
    mortar_ratio = float(_luma(O)[nm].mean() / _luma(O)[nb].mean())
    far = np.zeros((hh, ww), bool)
    far[160:, 260:] = True
    dark = float(_luma(O)[far & ~mortar].mean() / _luma(I)[far & ~mortar].mean())
    falloff = float(_luma(O)[nb].mean() / max(1e-6, _luma(O)[far & ~mortar].mean()))
    return [check("lit bricks take the magenta sign colour ((R+B)/2 - G > 30)", hue(O) > 30, hue(O), ">30"),
            check("light falls off: bricks near the sign > 3x brighter than the far wall", falloff > 3, falloff, ">3"),
            check("mortar stays darker than the lit bricks (ratio < 0.85)", mortar_ratio < .85, mortar_ratio, "<0.85"),
            check("far wall stays dark (lit/unlit luma ratio < 0.6)", dark < .6, dark, "<0.6"),
            check("seed 20261016 is deterministic", np.array_equal(b, b2), True, True),
            check("negative control: the unlit brick is not magenta", not hue(I) > 30, hue(I), "<=30")], [out]


@card("TEX-61")
def fluid_noise_arabic_word(task, wd):
    """Domain-warped fbm (w = fbm(p/90 + t*.3); v = fbm(p/60 + 2w)) quantised to 3 inks #2f4bff #e8503c #ff7ad9,
    composited destination-in with the whole shaped Arabic word (RTL, Lalezar) so it stays joined; then the mask
    scales 1 -> 12 until the fluid fills the frame."""
    hh, ww = 135, 240
    fp = FONTS / "Lalezar-Regular.ttf"
    font = ImageFont.truetype(str(fp), 80, layout_engine=ImageFont.Layout.RAQM)
    inks = np.array([_hex("#2f4bff"), _hex("#e8503c"), _hex("#ff7ad9")])
    xx, yy = _grid(hh, ww)
    bg = np.array([250, 246, 238.0])

    def fluid(t):
        w_ = _fbm(xx / 90 * 4 + t * .3, yy / 90 * 4, 4, 51)
        v = _fbm(xx / 60 * 4 + 2 * w_, yy / 60 * 4 + 2 * w_, 4, 53)
        q = np.digitize(v, np.quantile(v, [1 / 3, 2 / 3]))
        return inks[q]

    def base_mask(engine=ImageFont.Layout.RAQM):
        f = ImageFont.truetype(str(fp), 80, layout_engine=engine)
        im = Image.new("L", (ww, hh), 0)
        d = ImageDraw.Draw(im)
        kw = {"direction": "rtl"} if engine == ImageFont.Layout.RAQM else {}
        bb = d.textbbox((0, 0), "سائل", font=f, **kw)
        d.text(((ww - (bb[2] - bb[0])) / 2 - bb[0], (hh - (bb[3] - bb[1])) / 2 - bb[1]), "سائل", fill=255, font=f, **kw)
        return np.asarray(im).astype(float) / 255
    from scipy.ndimage import affine_transform, distance_transform_edt
    M0 = base_mask()
    dist = distance_transform_edt(M0 > .5)
    oy, ox = np.unravel_index(np.argmax(dist), dist.shape)

    def word_mask(scale, engine=ImageFont.Layout.RAQM):
        if engine != ImageFont.Layout.RAQM:
            return base_mask(engine)
        if scale == 1:
            return M0
        return np.clip(affine_transform(M0, [1 / scale, 1 / scale], offset=[oy - oy / scale, ox - ox / scale], order=1, mode="constant"), 0, 1)
    frames = []
    scales = [1, 1, 1.5, 3, 6, 12]
    for k, s in enumerate(scales):
        m = word_mask(s)[..., None]
        frames.append(bg * (1 - m) + fluid(k / 10) * m)
    out = _vid(wd / "fluid_word.mp4", frames, 10)
    O = _rd(out)
    m0 = word_mask(1) > .99
    px = O[0][m0]
    dist = np.min(np.abs(px[:, None, :] - inks[None]).max(-1), 1)
    ink_ok = float((dist <= 2).mean())
    shares = [float((np.abs(px - c).max(-1) <= 2).mean()) for c in inks]
    outside = float(np.abs(O[0][word_mask(1) == 0] - bg).max())
    joined = _components(word_mask(1) > .5)[1]
    unshaped = _components(word_mask(1, ImageFont.Layout.BASIC) > .5)[1]
    fill_last = float((np.abs(O[-1] - bg).max(-1) > 3).mean())
    pin = _png(wd / "input_plain_word.png", bg * (1 - M0[..., None]) + np.array([20, 20, 20.0]) * M0[..., None])
    pp = _load(pin)[m0]
    ink_plain = float((np.min(np.abs(pp[:, None, :] - inks[None]).max(-1), 1) <= 2).mean())
    return [check("inside the word only the 3 inks (>= 99% of pixels)", ink_ok >= .99, ink_ok, ">=0.99"),
            check("each ink holds > 15% of the word", min(shares) > .15, shares, ">0.15"),
            check("outside the word untouched (destination-in)", outside == 0, outside, 0),
            check("shaped RTL word stays joined: fewer pieces than unshaped letters", joined < unshaped, [joined, unshaped], "joined<unshaped"),
            check("scaled x12 the fluid fills >= 90% of the frame", fill_last >= .9, fill_last, ">=0.9"),
            check("negative control: the plain black word (no fluid) is not in the 3 inks", not ink_plain >= .99, ink_plain, "<0.99")], [out, pin]


@card("TEX-65")
def painterly_streak_clouds(task, wd):
    """Offline numpy sky: domain-warped fbm (4-5 octaves, warp .3), stretched along x and thresholded into soft
    streaks tinted by the sky gradient and toward the sun, drifting .01 uv/s; plus a purple nebula with seeded stars."""
    hh, ww = 108, 192
    xx, yy = _grid(hh, ww)
    sky = np.stack([60 + 120 * yy / hh, 90 + 70 * yy / hh, 180 - 40 * yy / hh], -1)
    sun = np.array([150.0, 70.0])
    pin = _png(wd / "sky.png", sky)

    def clouds(t, stretch=6.0):
        u = xx / ww + .01 * t
        w_ = _fbm(u * 8 / stretch * 4, yy / hh * 8, 4, 61) * .3
        n = _fbm((u + w_) * 32 / stretch, (yy / hh + w_) * 8, 5, 63)
        c = np.clip((n - .05) / .25, 0, 1) ** 1.5
        warm = np.exp(-np.hypot(xx - sun[0], yy - sun[1]) / 60)[..., None]
        tint = np.array([255, 235, 220]) * (1 - warm) + np.array([255, 170, 110]) * warm
        return sky * (1 - c[..., None] * .8) + tint * c[..., None] * .8, c
    frames, cs = [], []
    for k in range(31):
        f, c = clouds(k / 30 * 10)
        frames.append(f)
        cs.append(c)
    out = _vid(wd / "streak_clouds.mp4", frames, 30)
    O = _rd(out)

    def corr_len(img, axis):
        a = img - img.mean()
        best = 0
        for lag in range(1, 40):
            r = float((a * np.roll(a, lag, axis)).mean() / (a * a).mean())
            if r < .5:
                return lag
            best = lag
        return best
    cl = _luma(O[0]) - _luma(sky)
    lx, ly = corr_len(cl, 1), corr_len(cl, 0)
    cm = cs[0] > .3
    near = cm & (np.hypot(xx - sun[0], yy - sun[1]) < 35)
    farm = cm & (np.hypot(xx - sun[0], yy - sun[1]) > 90)
    warm = float((O[0][..., 0] - O[0][..., 2])[near].mean() - (O[0][..., 0] - O[0][..., 2])[farm].mean())
    dx, _ = _phase(_luma(O[30]) - _luma(sky), _luma(O[0]) - _luma(sky))
    _, iso = clouds(0, stretch=1.0)
    ilx, ily = corr_len(iso, 1), corr_len(iso, 0)
    nebula = np.zeros((hh, ww, 3)) + [20, 8, 40]
    nb = np.clip(.5 + .5 * _fbm(xx / 20, yy / 20, 5, 67), 0, 1)[..., None]
    nebula = nebula * (1 - nb) + np.array([140, 50, 170]) * nb
    rng = _rng(69)
    for _ in range(60):
        nebula[int(rng.integers(0, hh)), int(rng.integers(0, ww))] = 255
    neb = _png(wd / "nebula.png", nebula)
    return [check("streaks are anisotropic: x correlation length > 2x y", lx > 2 * ly, [lx, ly], "x>2y"),
            check("clouds near the sun warmer (R-B +15 over far clouds)", warm > 15, warm, ">15"),
            check("drift .01 uv/s: 10 s later shifted ~0.1*W = 19 px (+/-3)", abs(abs(dx) - 19.2) <= 3, dx, 19.2),
            check("negative control: unstretched fbm is isotropic (fails x>2y)", not ilx > 2 * ily, [ilx, ily], "isotropic")], [out, neb]


@card("TEX-66")
def veined_lava(task, wd):
    """Ridged lava: v = 1 - smoothstep(0, .03, abs(fbm(uv*3 + t*.05))); colour mix(#4a2040, #f0a040, v) plus bloom on
    the veins, slowly scrolling."""
    hh, ww = 108, 192

    def field(t, ridged=True):
        xx, yy = _grid(hh, ww)
        u, v_ = xx / ww * 3 + t * .05, yy / ww * 3
        n = _fbm(u * 6, v_ * 6, 4, 71)
        if not ridged:
            return (n > 0).astype(float)
        x = np.clip(np.abs(n) / .03, 0, 1)
        return 1 - x * x * (3 - 2 * x)

    def frame(t):
        v = field(t)
        col = _hex("#4a2040") * (1 - v[..., None]) + _hex("#f0a040") * v[..., None]
        return np.clip(col + _blur(v, 2)[..., None] * np.array([90, 40, 0]), 0, 255), v
    fps = 30
    frames, vs = zip(*[frame(k / fps * 3) for k in range(31)])
    out = _vid(wd / "lava.mp4", list(frames), fps)
    O = _rd(out)
    v0 = vs[0]
    frac = float((v0 > .5).mean())
    vein = O[0][v0 > .9].mean(0)
    base = np.median(O[0][_blur(v0, 3) < .01], 0)
    dx, _ = _phase(_luma(O[30]), _luma(O[0]))
    expect = ww * .05 * 3 / 3 / 6 * 6
    expect = .05 * 3 * ww / 3
    hv = field(0, ridged=False)
    hfrac = float((hv > .5).mean())
    return [check("thin veins: 2-20% of the floor", .02 < frac < .2, frac, "0.02-0.2"),
            check("veins glow #f0a040 (+ bloom, error <= 45)", np.abs(vein - _hex("#f0a040")).max() <= 45, vein.tolist(), "#f0a040"),
            check("base #4a2040 between veins (error <= 10)", np.abs(base - _hex("#4a2040")).max() <= 10, base.tolist(), "#4a2040"),
            check("scroll .05/s: 3 s later the floor moved %.1f px (+/-1.5)" % expect, abs(abs(dx) - expect) <= 1.5, dx, expect),
            check("negative control: a plain threshold (not abs ridged) covers ~half, not thin veins", not (.02 < hfrac < .2), hfrac, "~0.5")], [out]


@card("TEX-67")
def stroke_painterly(task, wd):
    """Painterly strokes: three stroke sizes oriented along a curl-noise flow field, colour sampled from the underlying
    render, re-seeded at 6 Hz with 1-2 px jitter (on fives at 30 fps)."""
    hh, ww = 108, 192
    src = _photo(hh, ww, 5)
    pin = _png(wd / "render.png", src)
    xx, yy = _grid(hh, ww)
    pot = _fbm(xx / 40, yy / 40, 2, 81)
    gy, gx = np.gradient(pot)
    ang = np.arctan2(-gx, gy)

    def paint(seed):
        rng = _rng(seed)
        im = Image.new("RGB", (ww * 2, hh * 2))
        im.paste(Image.fromarray(_u8(_blur(src, 2))).resize((ww * 2, hh * 2)))
        d = ImageDraw.Draw(im)
        for size, n in ((9, 500), (6, 900), (3, 1400)):
            for _ in range(n):
                x, y = rng.uniform(0, ww), rng.uniform(0, hh)
                jx, jy = rng.uniform(-2, 2, 2)
                a = ang[int(y), int(x)]
                c = tuple(int(v) for v in src[int(y), int(x)])
                L = size * 1.6
                p0 = ((x + jx - L / 2 * math.cos(a)) * 2, (y + jy - L / 2 * math.sin(a)) * 2)
                p1 = ((x + jx + L / 2 * math.cos(a)) * 2, (y + jy + L / 2 * math.sin(a)) * 2)
                d.line([p0, p1], fill=c, width=max(1, int(size * .7)))
        return np.asarray(im.resize((ww, hh), Image.BOX)).astype(float)
    frames = [paint(1000 + (k // 5)) for k in range(15)]
    out = _vid(wd / "painterly.mp4", frames)
    O = _rd(out)
    holds = all(np.array_equal(O[k], O[k - 1]) for k in range(1, 15) if k % 5)
    changes = all(not np.array_equal(O[k], O[k - 1]) for k in (5, 10))
    err = float(np.abs(O[0] - src).mean())
    import cv2

    def flow_agree(img):
        g = _luma(img).astype(np.float32)
        gxx = cv2.Sobel(g, cv2.CV_32F, 1, 0, ksize=3)
        gyy = cv2.Sobel(g, cv2.CV_32F, 0, 1, ksize=3)
        k = 7
        jxx = _blur(gxx * gxx, k)
        jyy = _blur(gyy * gyy, k)
        jxy = _blur(gxx * gyy, k)
        line = .5 * np.arctan2(2 * jxy, jxx - jyy) + math.pi / 2
        diff = np.abs(((line - ang) + math.pi / 2) % math.pi - math.pi / 2)
        return float(np.degrees(diff[10:-10, 10:-10]).mean())
    fo, fi = flow_agree(O[0]), flow_agree(src)
    return [check("held between 6 Hz re-seeds (frames within each 5-frame hold identical)", holds, holds, True),
            check("strokes re-seed every 5 frames (6 Hz)", changes, changes, True),
            check("colours sampled from the render (mean abs error < 28)", err < 28, err, "<28"),
            check("strokes follow the curl-noise flow (mean angle error < 30 deg)", fo < 30, fo, "<30"),
            check("negative control: the unpainted render does not follow the flow", not fi < 30, fi, ">=30")], [out]


@card("TEX-71")
def mesh_gradient_grid(task, wd):
    """Two stacked radial gradients (at 20%/80% .3 and 80%/20% .2, transparent at 50%), a faint 1 px grid every 50 px
    at 3% white, 2% grain against banding, centres drifting slowly."""
    hh, ww = 200, 300
    xx, yy = _grid(hh, ww)
    base = np.array([10, 12, 30.0])

    def frame(t, grain=True, grid=True):
        f = np.zeros((hh, ww, 3)) + base
        for (cx, cy, a, col) in [(.2 + .02 * t, .8, .3, (0, 240, 255)), (.8 - .02 * t, .2, .2, (112, 0, 255))]:
            r = np.hypot((xx / ww - cx), (yy / hh - cy)) / .5
            al = np.clip(1 - r, 0, 1)[..., None] * a
            f = f * (1 - al) + np.array(col) * al
        if grid:
            g = ((xx.astype(int) % 50 == 0) | (yy.astype(int) % 50 == 0))[..., None] * .03
            f = f * (1 - g) + 255 * g
        if grain:
            f = f + _rng(int(t * 10) + 3).normal(0, .02 * 255, (hh, ww, 1))
        return f
    frames = [frame(k / 10) for k in range(10)]
    out = _vid(wd / "mesh_grid.mp4", frames, 10)
    clean = _vid(wd / "input_nograin.mp4", [frame(k / 10, grain=False) for k in range(2)], 10)
    O, C = _rd(out), _rd(clean)
    ref = frame(0, grain=False, grid=False)
    gl = float(np.mean([(_luma(f)[:, 50::50] - _luma(ref)[:, 50::50]).mean() for f in O]))
    expect = float((.03 * (255 - _luma(ref)[:, 50::50])).mean())

    def runs(F):
        row = _u8(F[0][150, 60:140, 0]).astype(int)
        best, cur = 1, 1
        for a, b in zip(row, row[1:]):
            cur = cur + 1 if a == b else 1
            best = max(best, cur)
        return best
    ro, rc = runs(O), runs(C)
    peak = np.unravel_index(np.argmax(O[0][..., 1] - O[0][..., 0] * 0), O[0].shape[:2])
    cyan = _blur(O[0][..., 2] - base[2], 4)
    cy_, cx_ = np.unravel_index(np.argmax(np.where(xx < ww / 2, cyan, 0)), cyan.shape)
    _, dxs = 0, (_blur(_luma(O[9]), 6) - _blur(_luma(O[0]), 6))
    return [check("1 px grid every 50 px lifted by ~3% of (255 - bg) (+/-1)", abs(gl - expect) <= 1, gl, expect),
            check("grain 2% breaks banding: longest flat run on a gradient row <= 6 px", ro <= 6, ro, "<=6"),
            check("cyan radial centred near (20%, 80%)", abs(cx_ / ww - .2) < .06 and abs(cy_ / hh - .8) < .08, [cx_ / ww, cy_ / hh], [.2, .8]),
            check("centres drift between frames", float(np.abs(dxs).mean()) > .2, float(np.abs(dxs).mean()), ">0.2"),
            check("negative control: without grain the gradient bands (run > 6)", not rc <= 6, rc, ">6")], [out]


@card("TEX-75")
def graph_paper_graticule(task, wd):
    """Graph paper: 1 px #1a1a1a lines every 44 px on #090909 with .06 grain; graticule variant: 10x8 dark-green
    #0f2a1a cells at .35 with minor ticks every 1/5 cell on the centre axes, radial vignette."""
    hh, ww = 220, 440
    xx, yy = _grid(hh, ww)
    rng = _rng(91)
    g = np.zeros((hh, ww, 3)) + _hex("#090909")
    lines = (xx.astype(int) % 44 == 0) | (yy.astype(int) % 44 == 0)
    g[lines] = _hex("#1a1a1a")
    g = g + rng.normal(0, .06 * 20, (hh, ww, 1))
    paper = _png(wd / "graph_paper.png", g)
    cw, ch = ww / 10, hh / 8
    gt = np.zeros((hh, ww, 3)) + _hex("#050806")
    vl = np.zeros((hh, ww), bool)
    for i in range(11):
        vl[:, min(ww - 1, int(round(i * cw)))] = True
    for j in range(9):
        vl[min(hh - 1, int(round(j * ch))), :] = True
    for i in range(51):
        x = min(ww - 1, int(round(i * cw / 5)))
        vl[hh // 2 - 3:hh // 2 + 4, x] = True
    for j in range(41):
        y = min(hh - 1, int(round(j * ch / 5)))
        vl[y, ww // 2 - 3:ww // 2 + 4] = True
    col = _hex("#2c8a54")
    gt[vl] = gt[vl] * .65 + col * .35
    gt = gt * _vignette(hh, ww, .5)[..., None]
    grat = _png(wd / "graticule.png", gt)
    P, G = _load(paper), _load(grat)
    colm = _luma(P).mean(0)
    cz = colm - colm.mean()
    ac = [float((cz * np.roll(cz, lag)).sum()) for lag in range(20, 81)]
    period = 20 + int(np.argmax(ac))
    linecol = P[:, ::44][(yy[:, ::44].astype(int) % 44) != 0].mean(0)
    gm = _luma(G)
    lit = gm[30] > np.median(gm[30]) + 3
    nlines = int(np.sum(lit[1:] & ~lit[:-1]) + lit[0])
    ticks = [x for x in range(ww) if gm[hh // 2 + 2, x] > gm[hh // 2 + 2].mean() + 3]
    corner = float(gm[3:12, 3:12].mean())
    blank = np.zeros((hh, ww)) + _luma(_hex("#090909"))
    bz = blank.mean(0) - blank.mean()
    bac = [float((bz * np.roll(bz, lag)).sum()) for lag in range(20, 81)]
    bperiod = 20 + int(np.argmax(bac)) if max(np.abs(bac)) > 1e-9 else 0
    return [check("graph-paper period 44 px from the column spectrum (+/-1)", abs(period - 44) <= 1, period, 44),
            check("lines are #1a1a1a (+/-3)", np.abs(linecol - _hex("#1a1a1a")).max() <= 3, linecol.tolist(), "#1a1a1a"),
            check("graticule has 11 vertical lines (10 cells)", nlines == 11, nlines, 11),
            check("minor ticks every 1/5 cell on the axis (51)", len(ticks) == 51, len(ticks), 51),
            check("negative control: a blank ground has no 44 px period", not abs(bperiod - 44) <= 1, bperiod, "none")], [paper, grat]


@card("TEX-76")
def faint_text_wall(task, wd):
    """Dark ground filled with tiny mono text (9 px) at .08 opacity scrolling 10 px/s under a violet glow; dense variant
    rows alternate direction at 60 px/s; the headline sits on a solid band."""
    hh, ww = 120, 240
    rng = _rng(93)
    rows = ["".join(rng.choice(list("0123456789ABCDEF.:-")) for _ in range(60)) for _ in range(30)]
    tall = Image.new("L", (ww, hh * 3), 0)
    d = ImageDraw.Draw(tall)
    f9 = _font(9, mono=True)
    for i, r in enumerate(rows * 3):
        d.text((2, i * 11), r, fill=255, font=f9)
    T = np.asarray(tall).astype(float) / 255
    bg = np.array([10, 8, 20.0])
    glow = np.exp(-((_grid(hh, ww)[0] - ww / 2) ** 2 + (_grid(hh, ww)[1] - hh / 2) ** 2) / (2 * 50 ** 2))[..., None] * np.array([40, 10, 70])
    fps = 30

    def frame(k, speed=10.0):
        off = int(round(speed * k / fps))
        m = T[off:off + hh] * .08
        f = bg + glow
        f = f * (1 - m[..., None]) + 255 * m[..., None]
        f[50:70] = [30, 20, 50]
        return f
    frames = [frame(k) for k in range(31)]
    out = _vid(wd / "text_wall.mp4", frames, fps)
    O = _rd(out)
    base = bg + glow
    contrast = float((_luma(O[0][0:45]) - _luma(base[0:45])).max())
    tw = lambda f: _luma(f[0:45]) - _luma(base[0:45])
    _, dy = _phase(tw(O[0]), tw(O[30]))
    band_std = float(_luma(O[0][52:68]).std())
    dense = []
    for k in range(4):
        f = np.zeros((hh, ww))
        for r in range(0, hh, 12):
            sgn = 1 if (r // 12) % 2 == 0 else -1
            f[r:r + 12] = np.roll(T[r:r + 12, :], sgn * int(round(60 * k / fps)), 1)
        dense.append(np.stack([f * .08 * 255] * 3, -1) + bg)
    dv = _vid(wd / "text_wall_dense.mp4", dense, fps)
    D = _rd(dv)
    sa, _ = _phase(_luma(D[0][0:12]), _luma(D[3][0:12]))
    sb, _ = _phase(_luma(D[0][12:24]), _luma(D[3][12:24]))
    st = _vid(wd / "input_static.mp4", [frame(0, 0)] * 31, fps)
    S = _rd(st)
    _, sdy = _phase(tw(S[0]), tw(S[30]))
    return [check("text is faint: max lift <= 8% of 255 (+1)", contrast <= .08 * 255 + 1 and contrast > 10, contrast, "<=21.4"),
            check("scrolls 10 px/s: 1 s later shifted 10 px (+/-1)", abs(abs(dy) - 10) <= 1, dy, 10),
            check("headline band solid (std ~0)", band_std <= 1e-6, band_std, 0),
            check("dense rows alternate direction at 60 px/s (+6 / -6 px over 3 frames)", abs(abs(sa) - 6) <= 1 and abs(abs(sb) - 6) <= 1 and sa * sb < 0, [sa, sb], "+-6"),
            check("negative control: a static wall does not scroll", not abs(abs(sdy) - 10) <= 1, sdy, 0)], [out, dv]


@card("TEX-78")
def wet_street_reflections(task, wd):
    """Wet street: gradient #17343f -> #030b16, the hero mirrored in 3 px slices with a sine ripple, a sharp layer plus
    a 16 px blurred layer, and a Fresnel fade .9 -> .25 away from the horizon."""
    hh, ww = 160, 200
    hor = 80
    xx, yy = _grid(hh, ww)
    scene = np.zeros((hh, ww, 3)) + [8, 10, 24]
    scene[30:70, 60:140] = [255, 60, 180]
    scene[40:60, 80:120] = [60, 240, 255]
    street = (_hex("#17343f") * (1 - ((yy - hor) / (hh - hor))[..., None]) + _hex("#030b16") * ((yy - hor) / (hh - hor))[..., None])
    hero = scene[:hor][::-1]
    refl = np.zeros_like(street)
    shifts = []
    for y0 in range(0, hh - hor, 3):
        sh = int(round(2 * math.sin(y0 / 6)))
        shifts.append(sh)
        refl[hor + y0:hor + y0 + 3] = np.roll(hero[y0:y0 + 3], sh, 1)
    refl = .6 * refl + .4 * _blur(refl, 8)
    fres = (.9 - .65 * np.clip((yy - hor) / (hh - hor - 1), 0, 1))[..., None]
    img = scene.copy()
    img[hor:] = (street + fres * refl * .5)[hor:]
    out = _png(wd / "wet_street.png", img)
    plain = scene.copy()
    plain[hor:] = street[hor:]
    pin = _png(wd / "input.png", plain)
    O, I = _load(out), _load(pin)
    mir = _luma(hero)

    def corr(F):
        r = _luma(F[hor:]) - _luma(street[hor:])
        return float(np.corrcoef(r[:40].ravel(), _blur(mir, 3)[:40].ravel())[0, 1]) if r[:40].std() > 0 else 0.0
    co, ci = corr(O), corr(I)
    r = _luma(O[hor:]) - _luma(street[hor:])
    near = float(r[2:8, 80:120].mean() / max(1e-6, _luma(hero)[2:8, 80:120].mean()))
    lift_n = float(r[0:10, 60:140].mean())
    rowsh = []
    for y0 in (0, 3, 6, 9):
        a = _luma(O[hor + y0 + 1, :])
        b = _luma(O[hor + y0 + 2, :])
        rowsh.append(int(np.argmax(np.correlate(a - a.mean(), b - b.mean(), "full")) - (ww - 1)))
    fade_ratio = float(r[60:70, 60:140].mean() / max(1e-6, r[0:10, 60:140].mean()))
    return [check("reflection mirrors the hero (r > 0.6 with the flipped scene)", co > .6, co, ">0.6"),
            check("Fresnel fade: far reflection weaker than near (ratio < 0.6)", fade_ratio < .6, fade_ratio, "<0.6"),
            check("rows inside a 3 px slice share one ripple offset", all(s == 0 for s in rowsh), rowsh, 0),
            check("negative control: a dry street has no mirrored hero", not ci > .6, ci, "<=0.6")], [out]


@card("TEX-79")
def whiteboard_smudges(task, wd):
    """Whiteboard #f6f6f4 with 5 seeded light-grey rounded strokes at .05-.1 opacity, blurred 10 px, static, and an
    inset 40 px inner shadow at .06."""
    hh, ww = 135, 240
    rng = _rng(97)
    lay = Image.new("L", (ww, hh), 0)
    d = ImageDraw.Draw(lay)
    ops = []
    for _ in range(5):
        op = rng.uniform(.05, .1)
        ops.append(op)
        x, y = rng.uniform(40, 200), rng.uniform(30, 105)
        d.line([(x - 30, y), (x + 30, y + rng.uniform(-10, 10))], fill=int(255 * op), width=14, joint="curve")
    sm = np.asarray(lay.filter(ImageFilter.GaussianBlur(10))).astype(float) / 255
    board = np.zeros((hh, ww, 3)) + _hex("#f6f6f4")
    img = board * (1 - sm[..., None]) + 120 * sm[..., None]
    xx, yy = _grid(hh, ww)
    edge = np.minimum.reduce([xx, yy, ww - 1 - xx, hh - 1 - yy])
    inner = .06 * np.clip(1 - edge / 40, 0, 1) ** 2
    img = img * (1 - inner[..., None])
    out = _png(wd / "whiteboard.png", img)
    pin = _png(wd / "board.png", board)
    O, B = _load(out), _load(pin)
    centre = (slice(30, 105), slice(40, 200))
    dark = 1 - _luma(O[centre]) / _luma(B[centre])
    maxd = float(dark.max())
    smooth = float(np.abs(np.diff(_luma(O[centre]), axis=1)).max())
    edge_ratio = float(_luma(O[0:2, 100:140]).mean() / _luma(O[60:62, 100:140]).mean()) if True else 0
    db = 1 - _luma(B[centre]) / _luma(B[centre])
    return [check("smudges darken the board by 2-10% at most", .02 <= maxd <= .10, maxd, "0.02-0.10"),
            check("smudges are soft (max neighbour step <= 2)", smooth <= 2, smooth, "<=2"),
            check("inner border shadow ~6% at the edge (ratio 0.92-0.96)", .92 <= edge_ratio <= .965, edge_ratio, .94),
            check("negative control: the clean board has no smudge", not .02 <= float(db.max()) <= .10, float(db.max()), 0)], [out]


@card("TEX-80")
def chalk_grain_overlay(task, wd):
    """Static full-board chalk overlay: turbulence (baseFrequency ~.9) mapped to board-coloured specks at ~.35 over the
    drawings, without displacing the strokes (no displacement map)."""
    hh, ww = 135, 240
    board = _hex("#2f4a3a")
    img = np.zeros((hh, ww, 3)) + board
    lay = Image.new("L", (ww, hh), 0)
    d = ImageDraw.Draw(lay)
    d.line([(20, 30), (220, 40)], fill=255, width=5)
    d.ellipse([60, 60, 130, 120], outline=255, width=4)
    d.text((150, 70), "A+B", fill=255, font=_font(30))
    stroke = np.asarray(lay).astype(float) / 255
    drawn = img * (1 - stroke[..., None]) + np.array([235, 235, 225]) * stroke[..., None]
    pin = _png(wd / "drawing.png", drawn)
    xx, yy = _grid(hh, ww)
    turb = .5 + .5 * _fbm(xx * .9, yy * .9, 4, 101)
    speck = (turb > .62).astype(float) * .35
    chalk = drawn * (1 - speck[..., None]) + board * speck[..., None]
    out = _png(wd / "chalk.png", chalk)
    O, D = _load(out), _load(pin)
    smask = stroke > .9
    hit = float(((np.abs(O - D).max(-1) > 20) & smask).sum() / smask.sum())
    outside = stroke < .01
    moved = float(np.abs(O - D)[outside].max())
    keep = float(np.corrcoef(_luma(_blur(O, 2)).ravel(), _luma(_blur(D, 2)).ravel())[0, 1])
    hd = float(((np.abs(D - D).max(-1) > 20) & smask).sum() / smask.sum())
    return [check("chalk specks eat 5-45% of the stroke pixels", .05 <= hit <= .45, hit, "0.05-0.45"),
            check("specks are board-coloured: the board itself is unchanged (no displacement)", moved == 0, moved, 0),
            check("strokes keep their geometry (blurred r > 0.95)", keep > .95, keep, ">0.95"),
            check("negative control: the untreated drawing has no specks", not .05 <= hd <= .45, hd, 0)], [out]


@card("TEX-81")
def clipped_hatching(task, wd):
    """Marker scribble fill: a diagonal zigzag at 60 deg with 11 px spacing over the shape bbox, drawn by dash
    progress, clipped to the shape, opacity .55."""
    hh, ww = 140, 200
    xx, yy = _grid(hh, ww)
    shape = ((xx - 100) ** 2 / 70 ** 2 + (yy - 70) ** 2 / 50 ** 2) < 1
    a = math.radians(60)
    dxv, dyv = math.cos(a), -math.sin(a)
    pts = []
    sp = 11
    nx = -dyv, dxv
    for i in range(-20, 21):
        cx0 = 100 + nx[0] * i * sp
        cy0 = 70 + nx[1] * i * sp
        p0 = (cx0 - dxv * 120, cy0 - dyv * 120)
        p1 = (cx0 + dxv * 120, cy0 + dyv * 120)
        pts += [p0, p1] if i % 2 == 0 else [p1, p0]
    seglen = [math.hypot(b[0] - a_[0], b[1] - a_[1]) for a_, b in zip(pts, pts[1:])]
    total = sum(seglen)

    def draw(progress, clip=True):
        im = Image.new("L", (ww * 2, hh * 2), 0)
        d = ImageDraw.Draw(im)
        left = total * progress
        for (p, q), L in zip(zip(pts, pts[1:]), seglen):
            if left <= 0:
                break
            u = min(1, left / L)
            d.line([(p[0] * 2, p[1] * 2), ((p[0] + (q[0] - p[0]) * u) * 2, (p[1] + (q[1] - p[1]) * u) * 2)], fill=255, width=6)
            left -= L
        m = np.asarray(im.resize((ww, hh), Image.BOX)).astype(float) / 255
        if clip:
            m = m * shape
        bg = np.array([250, 250, 246.0])
        return bg * (1 - .55 * m[..., None]) + np.array([30, 80, 200]) * .55 * m[..., None], m
    f_half, m_half = draw(.5)
    f_full, m_full = draw(1.0)
    raw, m_raw = draw(1.0, clip=False)
    out = _vid(wd / "hatching.mp4", [draw(p)[0] for p in np.linspace(0, 1, 10)])
    O = _rd(out)
    bg = np.array([250, 250, 246.0])
    ink = lambda f: np.abs(f - bg).max(-1) > 3
    outside = int((ink(O[-1]) & ~shape).sum())
    alpha = float(((bg - O[-1]) / np.maximum(1, bg - np.array([30, 80, 200])))[..., 2][m_full > .99].mean())
    from scipy.ndimage import binary_erosion
    ang = _orient(_luma(O[-1]), binary_erosion(shape, iterations=6))
    raw_out = int((ink(raw) & ~shape).sum())
    grow = [int(ink(f).sum()) for f in O]
    return [check("no ink outside the shape (clipPath)", outside == 0, outside, 0),
            check("stroke opacity .55 (+/-0.03)", abs(alpha - .55) <= .03, alpha, .55),
            check("hatch lines at 60 deg (orientation 120 in y-down coords, +/-5)", abs(ang - 120) <= 5, ang, 120),
            check("drawn on by dash progress (ink grows monotonically)", all(b >= a_ for a_, b in zip(grow, grow[1:])) and grow[0] == 0, grow, "monotone"),
            check("negative control: the unclipped zigzag inks outside the shape", not raw_out == 0, raw_out, ">0")], [out]


@card("TEX-82")
def doodle_ground_tile_floor(task, wd):
    """Simplest grounds: a repeating 32 px pixel tile drawn as a pattern with smoothing disabled (nearest x2), and
    cloudy paper (low-frequency noise multiply) with a wobbly hand-drawn baseline."""
    hh, ww = 128, 256
    rng = _rng(103)
    pal = np.array([[90, 70, 50], [120, 95, 70], [60, 45, 35], [140, 120, 90]], float)
    tile = pal[rng.integers(0, 4, (16, 16))]
    big = np.kron(tile, np.ones((2, 2, 1)))
    floor = np.tile(big, (hh // 32, ww // 32, 1))
    out_t = _png(wd / "tile_floor.png", floor)
    smooth = np.asarray(Image.fromarray(_u8(np.tile(tile, (hh // 32 + 1, ww // 32 + 1, 1)))).resize((ww + 64, hh + 64), Image.BILINEAR)).astype(float)[:hh, :ww]
    out_s = _png(wd / "input_smoothed.png", smooth)
    xx, yy = _grid(hh, ww)
    paper = np.zeros((hh, ww, 3)) + [245, 240, 228]
    paper *= (1 - .06 * (.5 + .5 * _fbm(xx / 40, yy / 40, 3, 105)))[..., None]
    base = 96 + 2.5 * np.sin(np.arange(ww) / 9) + 1.5 * _noise(np.arange(ww) / 5, np.zeros(ww), 107)
    im = Image.fromarray(_u8(paper))
    ImageDraw.Draw(im).line([(x, base[x]) for x in range(ww)], fill=(40, 40, 40), width=2)
    out_p = im.save(wd / "doodle_paper.png") or (wd / "doodle_paper.png")
    T, S, P = _load(out_t), _load(out_s), _load(out_p)
    periodic = bool(np.array_equal(T[:, :-32], T[:, 32:]) and np.array_equal(T[:-32], T[32:]))
    tcols = {tuple(c) for c in T.reshape(-1, 3).astype(int)}
    scols = {tuple(c) for c in S.reshape(-1, 3).astype(int)}
    blocks = bool(np.array_equal(T[0::2, 0::2], T[1::2, 1::2]))
    ink = _luma(P) < 120
    ys = [np.nonzero(ink[:, x])[0].mean() for x in range(ww) if ink[:, x].any()]
    wob = float(np.std(ys))
    cloud = float(_luma(_blur(P, 6))[10:80].std())
    return [check("tile floor repeats exactly every 32 px", periodic, periodic, True),
            check("smoothing off: only the 4 tile colours", len(tcols) <= 4, len(tcols), 4),
            check("nearest x2 upscale: 2x2 blocks uniform", blocks, blocks, True),
            check("baseline wobbles 0.8-4 px", .8 <= wob <= 4, wob, "0.8-4"),
            check("cloudy paper: low-frequency variation (blurred std > 1)", cloud > 1, cloud, ">1"),
            check("negative control: a smoothed (bilinear) tile adds new colours", not len(scols) <= 4, len(scols), ">4")], [out_t, out_p]


@card("TEX-84")
def one_matte_family(task, wd):
    """Keep one material family: matte roughness .6-.9 for clay/low-poly objects (sample 0x7ee8d2 at .7) and at most
    one glossy hero; the scene is normalised to the family and rendered with a GGX/Schlick shader."""
    scene_in = [{"name": "rock", "roughness": .2}, {"name": "tree", "roughness": .25}, {"name": "hut", "roughness": .7},
                {"name": "bottle", "roughness": .08, "hero": True}]
    fixed = []
    for o in scene_in:
        o2 = dict(o)
        if not o.get("hero"):
            o2["roughness"] = float(min(.9, max(.6, o["roughness"] if o["roughness"] >= .6 else .7)))
        fixed.append(o2)
    _jw(wd / "scene_in.json", scene_in)
    spec_out = _jw(wd / "scene_matte.json", fixed)
    base = tuple(_hex("#7ee8d2"))

    def render(scene):
        tiles = []
        for o in scene:
            inside, nrm = _sphere(80, 80, 40, 40, 34)
            tiles.append(_ggx_shade(nrm, inside, o["roughness"], base=base, spec=.04))
        return np.concatenate(tiles, 1), inside
    img, inside = render(fixed)
    out = _png(wd / "matte_family.png", img)
    raw, _ = render(scene_in)
    pin = _png(wd / "input_mixed.png", raw)
    O, I = _load(out), _load(pin)

    def sharp(F):
        res = []
        for k in range(4):
            L = _luma(F[:, k * 80:(k + 1) * 80])[inside]
            res.append(float(L.max() - np.percentile(L, 90)))
        return res
    so, si = sharp(O), sharp(I)
    rule = lambda sc: sum(1 for o in sc if o.get("hero")) <= 1 and all(.6 <= o["roughness"] <= .9 for o in sc if not o.get("hero"))
    nonhero = [s for s, o in zip(so, fixed) if not o.get("hero")]
    hero = [s for s, o in zip(so, fixed) if o.get("hero")][0]
    gloss_in = sum(1 for s, o in zip(si, scene_in) if not o.get("hero") and s > 40)
    return [check("scene rule: non-hero roughness .6-.9, at most one hero", rule(fixed), [o["roughness"] for o in fixed], "0.6-0.9"),
            check("rendered matte spheres have no sharp highlight (peak - p90 < 40)", max(nonhero) < 40, nonhero, "<40"),
            check("the hero keeps its gloss (peak - p90 > 60)", hero > 60, hero, ">60"),
            check("negative control: the mixed input scene breaks the rule and shows sharp non-hero gloss", not (rule(scene_in) or gloss_in == 0), gloss_in, ">0")], [out, spec_out]


# ============================================================================ TRANSITIONS: mimic engine
def _TR():
    if str(MIMIC) not in sys.path:
        sys.path.insert(0, str(MIMIC))
    import mm_transitions
    return mm_transitions


def _AB(h=H, w=W):
    xx, yy = _grid(h, w)
    A = np.clip(np.stack([xx * 1.3 + 20, yy * 2.2, 60 + 0 * xx], -1) + 40 * (((xx // 10 + yy // 10) % 2) == 0)[..., None] * np.array([1, 0, 0]), 0, 255)
    B = np.stack([30 + 0 * xx, 255 - yy * 2, 100 + xx * .8], -1)
    B[(xx - w / 2) ** 2 + (yy - h / 2) ** 2 < (h * .2) ** 2] = [250, 250, 20]
    return A.astype(np.float32), np.clip(B, 0, 255).astype(np.float32)


def _disc_img(h=H, w=W, r=16, fg=255, bg=10, cx=None, cy=None):
    m = _disc_mask(h, w, w / 2 if cx is None else cx, h / 2 if cy is None else cy, r)
    return (bg + (fg - bg) * m)[..., None].repeat(3, -1).astype(np.float32)


def _radius(f, thr=128):
    return math.sqrt(float((_luma(f) > thr).sum()) / math.pi)


def _seq(kind, A, B, n=21, **prm):
    TR = _TR()
    return [TR.render(kind, A, B, 1.0 - k / (n - 1), **prm) for k in range(n)]


def _seq_out(wd, name, frames, fps=30):
    out = _vid(wd / (name + ".mp4"), frames, fps)
    return out, _rd(out)


def _cut_frames(A, B, n=21):
    return [A if k < n // 2 else B for k in range(n)]


@card("TRANS-01")
def dip_black(task, wd):
    """mm_transitions.render('dipblack', A, B, P, mid=.5): A fades to black by the midpoint, then black to B."""
    A, B = _AB()
    out, O = _seq_out(wd, "dipblack", _seq("dipblack", A, B, mid=.5))
    _, C = _seq_out(wd, "input_cut", _cut_frames(A, B))
    L = [float(_luma(f).mean()) for f in O]
    crit = lambda F: float(_luma(F[10]).mean()) < 2
    return [check("starts on A and ends on B (mean error < 1)", float(np.abs(O[0] - A).mean()) < 1 and float(np.abs(O[-1] - B).mean()) < 1, [float(np.abs(O[0] - A).mean()), float(np.abs(O[-1] - B).mean())], 0),
            check("black at the midpoint (mean luma < 2)", crit(O), L[10], "<2"),
            check("luma falls to the middle then rises (V curve)", all(b <= a + .5 for a, b in zip(L[:11], L[1:11])) and all(b >= a - .5 for a, b in zip(L[10:], L[11:])), L[::5], "V"),
            check("negative control: a hard cut never dips to black", not crit(C), float(_luma(C[10]).mean()), ">2")], [out]


@card("TRANS-02")
def dip_white(task, wd):
    """mm_transitions.render('dipwhite', A, B, P, mid=.5): A fades to white by the midpoint, then white to B."""
    A, B = _AB()
    out, O = _seq_out(wd, "dipwhite", _seq("dipwhite", A, B, mid=.5))
    _, C = _seq_out(wd, "input_cut", _cut_frames(A, B))
    crit = lambda F: float(_luma(F[10]).mean()) > 253
    L = [float(_luma(f).mean()) for f in O]
    return [check("white at the midpoint (mean luma > 253)", crit(O), L[10], ">253"),
            check("luma rises to the middle then falls", L[10] == max(L), L[::5], "peak mid"),
            check("ends exactly on B (mean error < 1)", float(np.abs(O[-1] - B).mean()) < 1, float(np.abs(O[-1] - B).mean()), 0),
            check("negative control: a hard cut never flashes white", not crit(C), float(_luma(C[10]).mean()), "<=253")], [out]


@card("TRANS-03")
def flash_cut(task, wd):
    """mm_transitions.render('flash', A, B, P, peak=.5, width=.25): a white flash over the crossfade, peaking at the
    midpoint and gone beyond +/-width."""
    A, B = _AB()
    out, O = _seq_out(wd, "flash", _seq("flash", A, B, peak=.5, width=.25))
    _, C = _seq_out(wd, "input_cut", _cut_frames(A, B))
    TR = _TR()
    mid = float(_luma(O[10]).mean())
    off = [float(np.abs(O[k] - TR.render("fade", A, B, 1 - k / 20)).mean()) for k in (0, 4, 16, 20)]
    return [check("flash peaks white at q=.5 (mean luma > 250)", mid > 250, mid, ">250"),
            check("outside +/-0.25 the frame is the plain crossfade (error < 1)", max(off) < 1, off, "<1"),
            check("flash ramps: q=.4 brighter than q=.3", _luma(O[8]).mean() > _luma(O[6]).mean() + 20, [float(_luma(O[8]).mean()), float(_luma(O[6]).mean())], "ramp"),
            check("negative control: a hard cut has no white frame", not float(max(_luma(f).mean() for f in C)) > 250, float(max(_luma(f).mean() for f in C)), "<=250")], [out]


@card("TRANS-88")
def blur_cross(task, wd):
    """mm_transitions.render('blurcross', A, B, P, blur=.035): crossfade while both shots blur, sigma = blur*max(h,w)
    * sin(pi q), sharpest at the ends."""
    A, B = _AB()
    out, O = _seq_out(wd, "blurcross", _seq("blurcross", A, B, blur=.035))
    _, C = _seq_out(wd, "input_cut", _cut_frames(A, B))
    s = [_sharp(f) for f in O]
    ref = min(_sharp(A), _sharp(B))
    sc = [_sharp(f) for f in C]
    return [check("midpoint sharpness < 10% of the sharp ends", s[10] < .1 * ref, [s[10], ref], "<0.1"),
            check("ends are untouched (sharpness equal to A and B within 2%)", abs(s[0] - _sharp(A)) / _sharp(A) < .02 and abs(s[-1] - _sharp(B)) / _sharp(B) < .02, [s[0], s[-1]], "sharp"),
            check("blur is symmetric: q=.25 and q=.75 both blurred", s[5] < .5 * _sharp(A) and s[15] < .5 * _sharp(B), [s[5], s[15]], "blurred"),
            check("negative control: a hard cut never loses sharpness", not min(sc) < .1 * ref, min(sc), ">=0.1*ref")], [out]


def _zoom_card(wd, kind, zoom, sign):
    A = _disc_img(r=16)
    B = _disc_img(r=16, fg=200, bg=40)
    TR = _TR()
    qs = [.1, .25, .45]
    frames = [TR.render(kind, A, B, 1 - q, zoom=zoom, blur=.0, xmix=.12) for q in [k / 20 for k in range(21)]]
    blurred = [TR.render(kind, A, B, 1 - q, zoom=zoom, blur=.02, xmix=.12) for q in [k / 20 for k in range(21)]]
    out, O = _seq_out(wd, kind, blurred)
    geo, G = _seq_out(wd, kind + "_geometry", frames)
    meas = [_radius(G[int(round(q * 20))]) for q in qs]
    exp = [16 * (1 + sign * zoom * min(1, q / .5) ** 2) for q in qs]
    s_mid, s_end = _sharp(O[9]), _sharp(O[0])
    _, C = _seq_out(wd, "input_cut", _cut_frames(A, B))
    cut_r = [_radius(C[int(round(q * 20))]) for q in qs]
    crit = lambda m: all(abs(a - b) <= 1.0 for a, b in zip(m, exp))
    return [check("A's disc radius follows 16*(1%+.1f*ease_in(q/.5)) (+/-1 px)" % (sign * zoom), crit(meas), meas, exp),
            check("radial blur near the switch (sharpness at q=.45 < 50% of q=0)", s_mid < .5 * s_end, [s_mid, s_end], "<0.5"),
            check("ends on B", float(np.abs(O[-1] - B).mean()) < 1, float(np.abs(O[-1] - B).mean()), 0),
            check("negative control: a hard cut keeps radius 16", not crit(cut_r), cut_r, 16)], [out, geo]


@card("TRANS-89")
def zoom_blur(task, wd):
    """mm_transitions.render('zoomblur', A, B, P, zoom=.4, blur=.02, xmix=.12): CapCut zoom-in with radial blur."""
    return _zoom_card(wd, "zoomblur", .4, 1)


@card("TRANS-90")
def zoom_blur_out(task, wd):
    """mm_transitions.render('zoomblurout', A, B, P, zoom=.3, blur=.02, xmix=.12): zoom-out with blur."""
    return _zoom_card(wd, "zoomblurout", .3, -1)


def _bar_angle(f):
    ys, xs = np.nonzero(_luma(f) > 128)
    xs, ys = xs - xs.mean(), ys - ys.mean()
    return .5 * math.degrees(math.atan2(2 * (xs * ys).mean(), (xs * xs).mean() - (ys * ys).mean()))


@card("TRANS-91")
def spin(task, wd):
    """mm_transitions.render('spin', A, B, P, deg=90): A rotates deg*u^2 (u = q/.5) with zoom 1+.3u, then B unwinds
    from -deg, with blur peaking at the switch."""
    A = np.zeros((H, W, 3), np.float32) + 10
    A[49:59, 30:162] = 255
    B = A.copy()
    B[..., 0] = np.where(B[..., 0] > 100, 255, 60)
    TR = _TR()
    out, O = _seq_out(wd, "spin", _seq("spin", A, B, deg=90.0))
    a25, a75 = _bar_angle(O[5]), _bar_angle(O[15])
    _, C = _seq_out(wd, "input_cut", _cut_frames(A, B))
    c25 = _bar_angle(C[5])
    return [check("q=.25: A turned 90*(.5)^2 = 22.5 deg (+/-2)", abs(abs(a25) - 22.5) <= 2, a25, 22.5),
            check("q=.75: B turned the opposite way by 22.5 deg (+/-2)", abs(abs(a75) - 22.5) <= 2 and a25 * a75 < 0, a75, -22.5),
            check("ends upright on B (angle ~0)", abs(_bar_angle(O[-1])) < .5, _bar_angle(O[-1]), 0),
            check("negative control: a hard cut does not rotate", not abs(abs(c25) - 22.5) <= 2, c25, 0)], [out]


WHIP = {"whipleft": (-1, 0), "whipright": (1, 0), "whipup": (0, -1), "whipdown": (0, 1)}


def _whip_measure(F, A):
    import cv2
    f = F
    g = _luma(f).astype(np.float32)
    gx = float((cv2.Sobel(g, cv2.CV_32F, 1, 0) ** 2).mean())
    gy = float((cv2.Sobel(g, cv2.CV_32F, 0, 1) ** 2).mean())
    return gx, gy


def _whip_card(wd, kinds):
    rng = _rng(5)
    A = np.kron(rng.random((H // 6, W // 6)) * 255, np.ones((6, 6)))[..., None].repeat(3, -1).astype(np.float32)
    B = np.kron(rng.random((H // 6, W // 6)) * 255, np.ones((6, 6)))[..., None].repeat(3, -1).astype(np.float32) * .6
    checks, outs = [], []
    TR = _TR()
    for kind in kinds:
        dx, dy = WHIP[kind]
        out, O = _seq_out(wd, kind, _seq(kind, A, B, blur=.08))
        outs.append(out)
        gx0, gy0 = _whip_measure(A, A)
        gxm, gym = _whip_measure(O[10], A)
        along = (gxm / gx0) if dx else (gym / gy0)
        across = (gym / gy0) if dx else (gxm / gx0)
        sx, sy = _phase(_luma(A), _luma(O[2]))
        moved = (sx * dx > 2) if dx else (sy * dy > 2)
        checks += [check("%s: motion blur along its axis (along/across gradient ratio < 0.5)" % kind, along < .5 * across, [along, across], "<0.5"),
                   check("%s: A pushed out toward %s (q=.1 shift sign)" % (kind, kind[4:]), moved, [sx, sy], [dx, dy])]
    _, C = _seq_out(wd, "input_cut", _cut_frames(A, B))
    gxm, gym = _whip_measure(C[10], A)
    gx0, gy0 = _whip_measure(A, A)
    checks.append(check("negative control: a hard cut has no directional blur", not (gxm / gx0) < .5 * (gym / gy0), [gxm / gx0, gym / gy0], "isotropic"))
    return checks, outs


@card("TRANS-247")
def whip_family(task, wd):
    """mm_transitions.render('whip<dir>', A, B, P, blur=.08): the matching slide plus a directional motion blur of
    blur*size*sin(pi q), for whipleft/whipright/whipup/whipdown."""
    return _whip_card(wd, list(WHIP))


@card("TRANS-249")
def whip_left(task, wd):
    """mm_transitions.render('whipleft', A, B, P): slide left with horizontal motion blur."""
    return _whip_card(wd, ["whipleft"])


@card("TRANS-250")
def whip_right(task, wd):
    """mm_transitions.render('whipright', A, B, P): slide right with horizontal motion blur."""
    return _whip_card(wd, ["whipright"])


@card("TRANS-251")
def whip_up(task, wd):
    """mm_transitions.render('whipup', A, B, P): slide up with vertical motion blur."""
    return _whip_card(wd, ["whipup"])


@card("TRANS-252")
def whip_down(task, wd):
    """mm_transitions.render('whipdown', A, B, P): slide down with vertical motion blur."""
    return _whip_card(wd, ["whipdown"])


# ---------------------------------------------------------------------------- xfade port vs FFmpeg
def _xfade_vs_ffmpeg(wd, kinds, fps=10, size=(90, 160)):
    hh, ww = size
    A, B = _AB(hh, ww)
    pa, pb = _png(wd / "A.png", A), _png(wd / "B.png", B)
    TR = _TR()
    rows, frames_all = {}, []
    for k in kinds:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-loop", "1", "-framerate", str(fps), "-t", "2", "-i", str(pa), "-loop", "1",
                              "-framerate", str(fps), "-t", "2", "-i", str(pb), "-filter_complex",
                              "[0][1]xfade=transition=%s:duration=1:offset=0.5,format=rgb24" % k, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                             capture_output=True, timeout=30, stdin=subprocess.DEVNULL).stdout
        F = np.frombuffer(raw, np.uint8).reshape(-1, hh, ww, 3).astype(float)
        errs, negs = [], []
        i0, i1 = int(.5 * fps), int(1.5 * fps)
        for i in range(i0, i1 + 1):
            P = 1 - (i / fps - .5)
            R = TR.render(k, A, B, P)
            frames_all.append(R)
            errs.append(float(np.abs(R - F[i]).mean()))
        mid = (i0 + i1) // 2
        rows[k] = {"max_err": max(errs), "neg_err": float(np.abs(A - F[mid]).mean())}
    out = _vid(wd / "xfade_port.mp4", frames_all, fps)
    _jw(wd / "xfade_vs_ffmpeg.json", rows)
    return rows, out


def _xfade_card(wd, kinds, label):
    rows, out = _xfade_vs_ffmpeg(wd, kinds)
    checks = [check("%s: numpy port equals FFmpeg xfade frame by frame (max mean error <= 4)" % k, r["max_err"] <= 4, r["max_err"], "<=4")
              for k, r in rows.items()]
    checks.append(check("negative control: the untreated outgoing shot does not match FFmpeg's midpoint (error > 10)",
                        all(r["neg_err"] > 10 for r in rows.values()), [round(r["neg_err"], 1) for r in rows.values()], ">10"))
    return checks, [out, wd / "xfade_vs_ffmpeg.json"]


for _cid, _kinds, _label in [
        ("TRANS-13", ["fade", "fadeblack", "fadewhite", "fadegrays", "fadefast", "fadeslow", "dissolve", "distance"], "fades"),
        ("TRANS-14", ["wipeleft", "wiperight", "wipeup", "wipedown", "wipetl", "wipetr", "wipebl", "wipebr"], "wipes"),
        ("TRANS-15", ["slideleft", "slideright", "slideup", "slidedown"], "slides"),
        ("TRANS-16", ["smoothleft", "smoothright", "smoothup", "smoothdown"], "smooth wipes"),
        ("TRANS-17", ["circleopen", "circleclose", "circlecrop", "rectcrop", "radial"], "shapes"),
        ("TRANS-18", ["vertopen", "vertclose", "horzopen", "horzclose"], "barn doors"),
        ("TRANS-19", ["diagtl", "diagtr", "diagbl", "diagbr"], "diagonals"),
        ("TRANS-20", ["hlslice", "hrslice", "vuslice", "vdslice"], "slices"),
        ("TRANS-21", ["coverleft", "coverright", "coverup", "coverdown", "revealleft", "revealright", "revealup", "revealdown"], "cover/reveal"),
        ("TRANS-22", ["squeezeh", "squeezev", "zoomin", "pixelize", "hblur"], "stylised")]:
    def _mk(kinds=_kinds, label=_label):
        def run(task, wd):
            return _xfade_card(wd, kinds, label)
        run.__doc__ = "FFmpeg xfade %s (%s) ported 1:1 to numpy in mm_transitions; every frame compared with FFmpeg's own xfade." % (label, ", ".join(kinds))
        return run
    card(_cid)(_mk())


@card("TRANS-248")
def xfade_54_port(task, wd):
    """All 54 xfade kinds of the mm_transitions numpy port, each compared frame by frame with the local FFmpeg
    xfade (6 fps sampling over a 1 s transition)."""
    TR = _TR()
    rows, out = _xfade_vs_ffmpeg(wd, TR.XFADE, fps=6, size=(54, 96))
    good = [k for k, r in rows.items() if r["max_err"] <= 4]
    return [check("54 kinds in the port", len(TR.XFADE) == 54, len(TR.XFADE), 54),
            check("all 54 replay FFmpeg's xfade (max mean error <= 4)", len(good) == 54, len(good), 54),
            check("negative control: the untreated outgoing shot fails against every midpoint", all(r["neg_err"] > 10 for r in rows.values()),
                  min(r["neg_err"] for r in rows.values()), ">10")], [out, wd / "xfade_vs_ffmpeg.json"]


# ---------------------------------------------------------------------------- classification by re-synthesis
def _ref_video(wd, name, kind, fps=25, n_a=20, n_t=12, n_b=20, size=(192, 108)):
    TR = _TR()
    w, h = size
    A, B = _AB(h, w)
    frames = [A] * n_a
    eased = [(.5 - .5 * math.cos(math.pi * (k + 1) / (n_t + 1))) for k in range(n_t)]
    frames += [TR.render(kind, A, B, 1 - q) for q in eased] if kind != "cut" else []
    frames += [B] * n_b
    return _vid(wd / (name + ".mp4"), frames, fps), eased, n_a, A, B


def _classify(ref):
    if str(MIMIC) not in sys.path:
        sys.path.insert(0, str(MIMIC))
    from fractions import Fraction
    import mm_analyze as MA
    info = fx.probe(ref)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    feats = MA.pass_a(str(ref), Fraction(v["r_frame_rate"]), int(v["width"]), int(v["height"]))
    bnds = MA.detect_boundaries(feats, None)
    fit = MA._Fitter(feats, None)
    return [MA.classify(feats, b, None, fitter=fit) for b in bnds]


@card("TRANS-12")
def classify_by_resynthesis(task, wd):
    """mm_analyze classify: each detected transition is identified by re-rendering candidate kinds (PARAM_GRID) and
    fitting their progress curve to the real frames, then replayed with mm_transitions.render(kind, A, B, P)."""
    ref, eased, n_a, A, B = _ref_video(wd, "reference_zoomblur", "zoomblur")
    res = _classify(ref)
    tr = max(res, key=lambda r: r.get("frames", 0)) if res else {"type": "none"}
    R = _rd(ref)
    TR = _TR()
    replay = []
    if tr["type"] not in ("none", "cut"):
        for i, q in enumerate(tr["progress"]):
            replay.append(TR.render(tr["type"], R[tr["ts"] - 1], R[tr["te"]], 1 - q, **tr.get("params", {})))
        err = float(np.mean([np.abs(replay[i] - R[tr["ts"] + i]).mean() for i in range(len(replay))]))
        out = _vid(wd / "replay.mp4", replay, 25)
    else:
        err, out = 99.0, _vid(wd / "replay.mp4", [R[0]], 25)
    _jw(wd / "classification.json", res)
    cut, *_ = _ref_video(wd, "reference_cut", "cut")
    rc = _classify(cut)
    ctypes = [r["type"] for r in rc]
    return [check("transition identified as zoomblur (the kind that made it)", tr["type"] == "zoomblur", tr["type"], "zoomblur"),
            check("span starts at the first transition frame (+/-2)", abs(tr.get("ts", -9) - n_a) <= 2, tr.get("ts"), n_a),
            check("fitted progress is monotone", all(b >= a for a, b in zip(tr.get("progress", [0]), tr.get("progress", [0])[1:])), tr.get("progress", [])[:6], "monotone"),
            check("replay with the fitted kind and curve matches the reference (mean error < 6)", err < 6, err, "<6"),
            check("negative control: a hard-cut reference is not classified as zoomblur", "zoomblur" not in ctypes, ctypes, "cut")], [out, wd / "classification.json"]


@card("TRANS-X13")
def classify_shipped_pipeline(task, wd):
    """The shipped in-repo pipeline: mm_analyze.analyze(ref, work) writes spec.json transitions[{type, params, ts, te,
    progress, confidence, alternatives}] by re-synthesis of 54 xfade + 11 phone kinds over 25 progress samples and a
    monotone DP path."""
    if str(MIMIC) not in sys.path:
        sys.path.insert(0, str(MIMIC))
    import io
    import contextlib
    import mm_analyze as MA
    TR = _TR()
    A, B = _AB(108, 192)
    eased = [(.5 - .5 * math.cos(math.pi * (k + 1) / 11)) for k in range(10)]
    frames = [A] * 30 + [TR.render("dipblack", A, B, 1 - q) for q in eased] + [B] * 30
    C = np.roll(A, 40, 1)[:, ::-1].copy()
    frames += [TR.render("wipeleft", B, C, 1 - q) for q in eased] + [C] * 30
    ref = _vid(wd / "reference.mp4", frames, 25)
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        spec = MA.analyze(str(ref), str(wd / "work"), skip_text=True)
    trs = spec["transitions"]
    types = [t["type"] for t in trs]
    spec_path = wd / "work" / "spec.json"
    ok_ts = len(trs) == 2 and abs(trs[0]["ts"] - 30) <= 2 and abs(trs[1]["ts"] - 70) <= 2
    mono = all(all(b >= a for a, b in zip(t["progress"], t["progress"][1:])) for t in trs)
    fields = all(all(k in t for k in ("type", "params", "ts", "te", "progress", "confidence", "alternatives")) for t in trs)
    cut_ref = _vid(wd / "input_cuts_only.mp4", [A] * 30 + [B] * 30 + [C] * 30, 25)
    naive = [t["type"] for t in _classify(cut_ref)]
    return [check("spec.json lists both transitions with the right kinds (dipblack, wipeleft)", types == ["dipblack", "wipeleft"], types, ["dipblack", "wipeleft"]),
            check("spans start at frames 30 and 70 (+/-2)", ok_ts, [t["ts"] for t in trs], [30, 70]),
            check("measured progress curves are monotone", mono, [t["progress"][:4] for t in trs], "monotone"),
            check("each entry has type, params, ts, te, progress, confidence, alternatives", fields, sorted(trs[0].keys()) if trs else [], "fields"),
            check("negative control: the same shots joined by hard cuts are not read as dipblack/wipeleft", not naive == ["dipblack", "wipeleft"], naive, "cuts")], [spec_path if spec_path.exists() else ref]


# ============================================================================ TRANSITIONS: timing recipes
@card("TRANS-27")
def camera_punch_in(task, wd):
    """Scene cut marked by a camera punch-in: camKeys at t (scale 1.08, rot -1.5 deg) and t+0.2 (scale 1.0), eased
    out, so the cut lands with a quick zoom that snaps back."""
    from scipy.ndimage import affine_transform
    fps, cut = 30, 15
    A = _disc_img(r=12, fg=230, bg=30)
    B = _disc_img(r=16, fg=255, bg=10)

    def cam(img, s):
        cy, cx = (H - 1) / 2, (W - 1) / 2
        return np.stack([affine_transform(img[..., c], [1 / s, 1 / s], offset=[cy - cy / s, cx - cx / s], order=1, mode="nearest") for c in range(3)], -1)
    frames, scales = [], []
    for k in range(30):
        if k < cut:
            frames.append(A)
            scales.append(1.0)
            continue
        u = min(1.0, (k - cut) / fps / .2)
        s = 1.08 - .08 * float(_ease_out_cubic(u))
        scales.append(s)
        frames.append(cam(B, s))
    out, O = _seq_out(wd, "punch_in", frames, fps)
    r_cut, r_end = _radius(O[cut]), _radius(O[cut + 6])
    _, C = _seq_out(wd, "input_cut", [A] * cut + [B] * 15, fps)
    rc = _radius(C[cut])
    return [check("cut frame punched in to 1.08: radius 16*1.08 = 17.3 (+/-0.4)", abs(r_cut - 17.28) <= .4, r_cut, 17.28),
            check("back to 1.0 after 200 ms (6 frames): radius 16 (+/-0.3)", abs(r_end - 16) <= .3, r_end, 16),
            check("scale decreases monotonically through the ramp", all(b <= a + 1e-9 for a, b in zip(scales[cut:], scales[cut + 1:])), scales[cut:cut + 7], "1.08->1.0"),
            check("negative control: a plain cut does not punch in", not abs(rc - 17.28) <= .4, rc, 16)], [out]


@card("TRANS-259")
def scene_fade_edges(task, wd):
    """Remotion starter sceneFade(frame, length, edge=10) = min(progress(frame, 0, edge, easeOutCubic),
    1 - progress(frame, length - edge, edge, easeOutCubic)): every scene fades in and out over 10 frames."""
    length, edge = 40, 10
    prog = lambda f, s, d: float(_ease_out_cubic(min(1.0, max(0.0, (f - s) / d))))
    op = [min(prog(f, 0, edge), 1 - prog(f, length - edge, edge)) for f in range(length)]
    scene = np.zeros((H, W, 3)) + 250
    frames = [scene * o for o in op]
    out, O = _seq_out(wd, "scene_fade", frames, 30)
    meas = [float(_luma(f).mean() / 250) for f in O]
    err = max(abs(a - b) for a, b in zip(meas, op))
    _, C = _seq_out(wd, "input_unfaded", [scene] * length, 30)
    cm = [float(_luma(f).mean() / 250) for f in C]
    cerr = max(abs(a - b) for a, b in zip(cm, op))
    return [check("measured opacity equals sceneFade per frame (max error < 0.01)", err < .01, err, "<0.01"),
            check("fade-in done by frame 10 (opacity 1.0)", abs(meas[10] - 1) < .01, meas[10], 1.0),
            check("easeOutCubic: frame 1 already at 0.27 (+/-0.01)", abs(meas[1] - .271) < .01, meas[1], .271),
            check("negative control: an unfaded scene fails the curve", not cerr < .01, cerr, ">0.01")], [out]


_CURVES = {"linear": lambda u: float(np.clip(u, 0, 1)), "easeInOutCubic": lambda u: float(_ease_io_cubic(u)),
           "easeOutCubic": lambda u: float(_ease_out_cubic(u))}


def _plan_entry(wd, key, dur, curve, where):
    """Declare the key in a PLAN.md transitions table (templates/PLAN.md section 4) and parse it back."""
    tpl = (REPO / "templates/PLAN.md").read_text(encoding="utf-8")
    sec = tpl.index("## 4.")
    rows = "| %s | %d | %s | %s |\n" % (key, dur, curve, where)
    head = tpl[sec:].split("\n")
    table_end = next(i for i, l in enumerate(head) if l.startswith("| |"))
    plan = tpl[:sec] + "\n".join(head[:table_end]) + "\n" + rows + "\n".join(head[table_end + 1:])
    p = wd / "PLAN.md"
    p.write_text(plan, encoding="utf-8")
    txt = p.read_text(encoding="utf-8")
    keys = txt[txt.index("Transition: ") + len("Transition: "):].split("\n")[0].split(" · ")
    part = txt[txt.index("## 4."):txt.index("## 5.")]
    for line in part.splitlines():
        cells = [c.strip() for c in line.strip("|").split("|")]
        if cells and cells[0] == key:
            return {"name": cells[0], "ms": int(cells[1]), "curve": cells[2], "where": cells[3], "vocab": [k.strip() for k in keys]}, p
    raise RuntimeError("PLAN row not parsed")


def _frames_for(ms, fps=30):
    return max(1, int(round(ms / 1000 * fps)))


@card("TRANS-425")
def plan_cut(task, wd):
    """PLAN transition key `cut` (0 ms): declared in the PLAN.md transitions table, then coded in draw() as an
    instant switch from A to B on the cut frame."""
    e, plan = _plan_entry(wd, "cut", 0, "none", "scene 1 -> 2")
    A, B = [np.round(x) for x in _AB()]
    cutf = 12
    frames = [A if k < cutf else B for k in range(24)]
    out, O = _seq_out(wd, "cut", frames)
    isA = [float(np.abs(f - A).max()) == 0 for f in O]
    isB = [float(np.abs(f - B).max()) == 0 for f in O]
    blended = sum(1 for a, b in zip(isA, isB) if not a and not b)
    _, C = _seq_out(wd, "input_held", [A] * 24)
    cB = [float(np.abs(f - B).max()) == 0 for f in C]
    return [check("PLAN row parsed: cut, 0 ms, key in the PLAN vocabulary", e["name"] == "cut" and e["ms"] == 0 and "cut" in e["vocab"], e, "cut 0"),
            check("frames before the cut are exactly A", all(isA[:cutf]), sum(isA[:cutf]), cutf),
            check("from the cut frame on exactly B", all(isB[cutf:]), sum(isB[cutf:]), 24 - cutf),
            check("no blended frame (0 in-between frames)", blended == 0, blended, 0),
            check("negative control: the held input never switches to B", not any(cB), sum(cB), ">0")], [out, plan]


def _edge_x(f, B, A):
    eqB = (np.abs(f - B).max(-1) < 1).mean(0)
    return int((eqB > .98).sum())


@card("TRANS-426")
def plan_wipe(task, wd):
    """PLAN transition key `wipe` (500 ms, easeInOutCubic): the edge of B advances W*ease(t/d) from the left."""
    e, plan = _plan_entry(wd, "wipe", 500, "easeInOutCubic", "scene 2 -> 3")
    A, B = _AB()
    n = _frames_for(e["ms"])
    ease = _CURVES[e["curve"]]
    xs = [int(round(W * ease(k / n))) for k in range(n + 1)]
    frames = []
    for x in xs:
        f = A.copy()
        f[:, :x] = B[:, :x]
        frames.append(f)
    out, O = _seq_out(wd, "wipe", frames)
    meas = [_edge_x(f, B, A) for f in O]
    _, C = _seq_out(wd, "input_held", [A] * (n + 1))
    cm = [_edge_x(f, B, A) for f in C]
    return [check("PLAN row parsed: wipe, 500 ms, easeInOutCubic", (e["ms"], e["curve"]) == (500, "easeInOutCubic"), [e["ms"], e["curve"]], [500, "easeInOutCubic"]),
            check("edge position follows W*easeInOutCubic(t/0.5 s) (+/-1 px)", max(abs(a - b) for a, b in zip(meas, xs)) <= 1, meas[::3], xs[::3]),
            check("15 frames at 30 fps", n == 15, n, 15),
            check("negative control: the held input never wipes", not max(abs(a - b) for a, b in zip(cm, xs)) <= 1, cm[-1], W)], [out, plan]


@card("TRANS-427")
def plan_morph(task, wd):
    """PLAN transition key `morph` (600 ms, easeInOutCubic): the hero circle morphs into a square by easing its corner
    radius 30 -> 0, measured as fill ratio = 1 - (4 - pi) r^2 / s^2."""
    e, plan = _plan_entry(wd, "morph", 600, "easeInOutCubic", "logo -> card")
    n = _frames_for(e["ms"])
    ease = _CURVES[e["curve"]]
    s = 60
    frames, exp = [], []
    for k in range(n + 1):
        r = 30 * (1 - ease(k / n))
        exp.append(1 - (4 - math.pi) * r * r / (s * s))
        m = _rounded(H, W, (66, 24, 66 + s, 24 + s), max(r, .01), ss=8)
        frames.append(np.stack([20 + 220 * m] * 3, -1))
    out, O = _seq_out(wd, "morph", frames)

    def ratio(f):
        m = (_luma(f) - 20) / 220
        return float(m.sum() / (s * s))
    meas = [ratio(f) for f in O]
    err = max(abs(a - b) for a, b in zip(meas, exp))
    _, C = _seq_out(wd, "input_circle", [frames[0]] * (n + 1))
    cerr = max(abs(ratio(f) - b) for f, b in zip(C, exp))
    return [check("fill ratio follows the eased corner radius (max error < 0.01)", err < .01, err, "<0.01"),
            check("starts as a circle (pi/4 = 0.785)", abs(meas[0] - math.pi / 4) < .01, meas[0], .785),
            check("ends as a square (1.0)", abs(meas[-1] - 1) < .01, meas[-1], 1.0),
            check("negative control: the un-morphed circle fails the curve", not cerr < .01, cerr, ">0.01")], [out, plan]


@card("TRANS-428")
def plan_mask_reveal(task, wd):
    """PLAN transition key `mask-reveal` (600 ms, easeOutCubic): B is revealed through a circle whose radius eases from
    0 to the frame diagonal."""
    e, plan = _plan_entry(wd, "mask-reveal", 600, "easeOutCubic", "scene 3 -> 4")
    A, B = _AB()
    n = _frames_for(e["ms"])
    ease = _CURVES[e["curve"]]
    R = math.hypot(W / 2, H / 2)
    rs = [R * ease(k / n) for k in range(n + 1)]
    frames = []
    for r in rs:
        m = _disc_mask(H, W, W / 2, H / 2, r, ss=2)[..., None]
        frames.append(A * (1 - m) + B * m)
    out, O = _seq_out(wd, "mask_reveal", frames)

    def rad(f):
        return math.sqrt(float((np.abs(f - B).max(-1) < 2).sum() - (np.abs(A - B).max(-1) < 2).sum()) / math.pi)
    chk = [(rad(f), r) for f, r in zip(O, rs) if 2 < r < H / 2 - 1]
    err = max(abs(a - b) for a, b in chk)
    _, C = _seq_out(wd, "input_held", [A] * (n + 1))
    cr = [rad(f) for f in C]
    return [check("revealed radius follows R*easeOutCubic(t/0.6 s) while unclipped (+/-1 px)", err <= 1, err, "<=1"),
            check("fully revealed at the end", float(np.abs(O[-1] - B).max()) < 1, float(np.abs(O[-1] - B).max()), 0),
            check("negative control: the held input reveals nothing", not max(cr) > 2, max(cr), 0)], [out, plan]


@card("TRANS-429")
def plan_zoom_through(task, wd):
    """PLAN transition key `zoom-through` (500 ms, easeInOutCubic): the camera flies into A (scale 1 -> 4 about the
    centre) while B fades in over the last 40%."""
    from scipy.ndimage import affine_transform
    e, plan = _plan_entry(wd, "zoom-through", 500, "easeInOutCubic", "chapter break")
    n = _frames_for(e["ms"])
    ease = _CURVES[e["curve"]]
    A = _disc_img(r=10, fg=240, bg=20)
    B = _AB()[1]
    cy, cx = (H - 1) / 2, (W - 1) / 2
    frames, sc = [], []
    for k in range(n + 1):
        u = ease(k / n)
        s = 1 + 3 * u
        sc.append(s)
        z = np.stack([affine_transform(A[..., c], [1 / s, 1 / s], offset=[cy - cy / s, cx - cx / s], order=1, mode="nearest") for c in range(3)], -1)
        a = float(np.clip((k / n - .6) / .4, 0, 1))
        frames.append(z * (1 - a) + B * a)
    out, O = _seq_out(wd, "zoom_through", frames)
    early = [(k, _radius(O[k])) for k in range(n + 1) if k / n <= .6]
    err = max(abs(r - 10 * sc[k]) for k, r in early)
    _, C = _seq_out(wd, "input_held", [A] * (n + 1))
    cerr = max(abs(_radius(C[k]) - 10 * sc[k]) for k, _ in early)
    return [check("A's disc radius grows with the eased camera scale 1 -> 4 (+/-1 px)", err <= 1, err, "<=1"),
            check("ends on B", float(np.abs(O[-1] - B).mean()) < 1, float(np.abs(O[-1] - B).mean()), 0),
            check("negative control: the held input never zooms", not cerr <= 1, cerr, ">1")], [out, plan]


@card("TRANS-430")
def plan_match_cut(task, wd):
    """PLAN transition key `match-cut` (0 ms): the incoming shot's subject is placed where the outgoing subject is on
    the cut frame, so the eye stays put across the cut."""
    e, plan = _plan_entry(wd, "match-cut", 0, "none", "ball -> moon")
    cutf = 12
    xs = [40 + 4 * k for k in range(cutf)]
    hand_off = (xs[-1] + 4, H / 2)

    def shot_a(x):
        return _disc_img(r=12, fg=240, bg=20, cx=x, cy=H / 2)

    def shot_b(pos):
        f = np.zeros((H, W, 3)) + [10, 20, 60]
        m = _disc_mask(H, W, pos[0], pos[1], 14)[..., None]
        return f * (1 - m) + np.array([250, 250, 210]) * m
    frames = [shot_a(x) for x in xs] + [shot_b(hand_off)] * 12
    out, O = _seq_out(wd, "match_cut", frames)
    naive = [shot_a(x) for x in xs] + [shot_b((W / 2, H / 2))] * 12
    _, N = _seq_out(wd, "input_unmatched", naive)

    def cen(f, thr=150):
        m = _luma(f) > thr
        ys, xs_ = np.nonzero(m)
        return float(xs_.mean()) + .5, float(ys.mean()) + .5
    pa = cen(O[cutf - 1])
    pb = cen(O[cutf])
    exp_next = (pa[0] + 4, pa[1])
    d = math.hypot(pb[0] - exp_next[0], pb[1] - exp_next[1])
    nb = cen(N[cutf])
    dn = math.hypot(nb[0] - exp_next[0], nb[1] - exp_next[1])
    jump = float(np.abs(O[cutf] - O[cutf - 1]).mean())
    return [check("PLAN row parsed: match-cut", e["name"] == "match-cut" and "match-cut" in e["vocab"], e["name"], "match-cut"),
            check("incoming subject lands where the outgoing one was heading (<= 1 px)", d <= 1, d, "<=1"),
            check("it is a real cut (big frame change at the cut)", jump > 10, jump, ">10"),
            check("negative control: an unmatched cut moves the subject > 10 px", not dn <= 1, dn, ">1")], [out, plan]


@card("TRANS-431")
def plan_dissolve(task, wd):
    """PLAN transition key `dissolve` (400 ms, linear): frame k = A*(1 - k/n) + B*(k/n); the per-frame mix is
    recovered from the output by least squares."""
    e, plan = _plan_entry(wd, "dissolve", 400, "linear", "scene 4 -> 5")
    A, B = _AB()
    n = _frames_for(e["ms"])
    frames = [A * (1 - _CURVES["linear"](k / n)) + B * _CURVES["linear"](k / n) for k in range(n + 1)]
    out, O = _seq_out(wd, "dissolve", frames)
    d = (B - A).ravel()
    alpha = [float(((f - A).ravel() @ d) / (d @ d)) for f in O]
    err = max(abs(a - k / n) for k, a in enumerate(alpha))
    _, C = _seq_out(wd, "input_cut", [A if k < n / 2 else B for k in range(n + 1)])
    ca = [float(((f - A).ravel() @ d) / (d @ d)) for f in C]
    cerr = max(abs(a - k / n) for k, a in enumerate(ca))
    return [check("recovered mix equals k/n per frame (max error < 0.01)", err < .01, err, "<0.01"),
            check("12 frames at 30 fps for 400 ms", n == 12, n, 12),
            check("negative control: a hard cut fails the dissolve curve", not cerr < .01, cerr, ">0.01")], [out, plan]


def _render_counter(text, size=(28, 110)):
    im = Image.new("RGB", (size[1], size[0]), (20, 20, 20))
    ImageDraw.Draw(im).text((4, 4), text, fill=(255, 255, 255), font=_font(16))
    return np.asarray(im).astype(float)


@card("TRANS-432")
def before_after_wipe(task, wd):
    """Before/after split-screen: a clip-path wipe over 600 ms reveals the after image while a saved-hours counter
    counts 0 -> 120 with the same easing."""
    A, B = _AB()
    n = _frames_for(600)
    ease = _CURVES["easeInOutCubic"]
    frames, exp_x, exp_n = [], [], []
    for k in range(n + 1):
        u = ease(k / n)
        x = int(round(W * u))
        f = A.copy()
        f[:, :x] = B[:, :x]
        val = int(round(120 * u))
        f[H - 30:H - 2, 2:112] = _render_counter("Saved %d h" % val)
        frames.append(f)
        exp_x.append(x)
        exp_n.append(val)
    out, O = _seq_out(wd, "before_after", frames)
    top = slice(0, H - 32)
    meas = [int((np.abs(f[top] - B[top]).max(-1) < 1).mean(0).__gt__(.98).sum()) for f in O]
    counters = [float(np.abs(O[k][H - 30:H - 2, 2:112] - _render_counter("Saved %d h" % exp_n[k])).max()) for k in range(n + 1)]
    _, C = _seq_out(wd, "input_before", [A] * (n + 1))
    cm = [int((np.abs(f[top] - B[top]).max(-1) < 1).mean(0).__gt__(.98).sum()) for f in C]
    return [check("wipe edge follows W*easeInOutCubic over 600 ms (+/-1 px)", max(abs(a - b) for a, b in zip(meas, exp_x)) <= 1, meas[::4], exp_x[::4]),
            check("counter shows the eased saved-hours value on every frame (pixel-exact)", max(counters) == 0, max(counters), 0),
            check("counter ends on 120 h", exp_n[-1] == 120 and counters[-1] == 0, exp_n[-1], 120),
            check("negative control: the before image alone never wipes", not max(abs(a - b) for a, b in zip(cm, exp_x)) <= 1, cm[-1], W)], [out]


@card("TRANS-433")
def sketch_to_real(task, wd):
    """A pencil sketch of the UI (edges of the real screen at the same geometry) crossfades into the real screenshot
    over 400 ms."""
    import cv2
    real = np.zeros((H, W, 3)) + [245, 246, 250]
    real[8:24, 8:184] = [40, 90, 220]
    real[32:80, 8:90] = [255, 255, 255]
    real[32:80, 100:184] = [255, 255, 255]
    real[88:100, 60:132] = [240, 80, 60]
    g = _luma(real).astype(np.uint8)
    edges = cv2.Canny(g, 30, 90) > 0
    sketch = np.where(edges[..., None], [70, 70, 80], [250, 248, 240]).astype(float)
    n = _frames_for(400)
    frames = [sketch * (1 - k / n) + real * (k / n) for k in range(n + 1)]
    out, O = _seq_out(wd, "sketch_to_real", frames)
    se = cv2.Canny(_luma(O[0]).astype(np.uint8), 30, 90) > 0
    from scipy.ndimage import binary_dilation
    re_ = edges
    iou = float((binary_dilation(se, iterations=2) & re_).sum() / max(1, re_.sum()))
    d = (real - sketch).ravel()
    alpha = [float(((f - sketch).ravel() @ d) / (d @ d)) for f in O]
    _, C = _seq_out(wd, "input_cut", [sketch if k < n / 2 else real for k in range(n + 1)])
    ca = [float(((f - sketch).ravel() @ d) / (d @ d)) for f in C]
    step = lambda a: max(abs(y - x) for x, y in zip(a, a[1:]))
    return [check("sketch shares the screenshot's geometry (edge overlap > 0.9)", iou > .9, iou, ">0.9"),
            check("12-frame (400 ms) crossfade: mid mix 0.5 (+/-0.02)", abs(alpha[n // 2] - .5) <= .02, alpha[n // 2], .5),
            check("smooth: no step larger than 1/12 + 0.01", step(alpha) <= 1 / n + .01, step(alpha), 1 / n),
            check("negative control: a hard cut jumps", not step(ca) <= 1 / n + .01, step(ca), ">0.09")], [out]


@card("TRANS-434")
def cut_on_beat(task, wd):
    """Cut on the beat or one frame before, never 2+ frames late: beats are detected from the music track, the edit
    plan snaps every cut to floor(beat*fps), the cuts are found again in the rendered video."""
    fps, rate = 30, 22050
    beats_true = [.5, 1.0, 1.5, 2.0]
    dur = 2.4
    t = np.arange(int(dur * rate)) / rate
    audio = np.zeros_like(t)
    for b in beats_true:
        i = int(b * rate)
        audio[i:i + 600] += np.exp(-np.arange(600) / 120) * np.sin(2 * math.pi * 1200 * np.arange(600) / rate) * .8
    wav = fx.write_wav(wd / "music.wav", audio, rate)
    a, r = fx.read_wav(wav)
    env = np.abs(a[:, 0])
    hop = 256
    e = np.array([env[i:i + hop].sum() for i in range(0, len(env), hop)])
    onset = np.maximum(0, np.diff(e))
    peaks = [i for i in range(1, len(onset) - 1) if onset[i] > onset[i - 1] and onset[i] >= onset[i + 1] and onset[i] > .3 * onset.max()]
    beats = [(p + 1) * hop / r for p in peaks]
    plan = [int(math.floor(b * fps)) for b in beats]
    cols = [(220, 60, 60), (60, 200, 90), (60, 90, 220), (230, 200, 40), (200, 60, 200)]
    nfr = int(dur * fps)

    def render(cuts, name):
        frames, c = [], 0
        for k in range(nfr):
            while c < len(cuts) and k >= cuts[c]:
                c += 1
            frames.append(np.zeros((H, W, 3)) + cols[c])
        v = _vid(wd / (name + "_v.mp4"), frames, fps)
        o = wd / (name + ".mp4")
        fx.ffmpeg("-i", v, "-i", wav, "-c:v", "copy", "-c:a", "aac", "-shortest", o)
        return o
    out = render(plan, "cut_on_beat")
    O = _rd(out)
    found = [k for k in range(1, len(O)) if np.abs(O[k] - O[k - 1]).mean() > 10]
    bf = [b * fps for b in beats_true]
    offs = [f - math.floor(b) for f, b in zip(found, bf)]
    has_audio = any(s["codec_type"] == "audio" for s in fx.probe(out)["streams"])
    late = render([p + 2 for p in plan], "input_late")
    L = _rd(late)
    lf = [k for k in range(1, len(L)) if np.abs(L[k] - L[k - 1]).mean() > 10]
    loffs = [f - math.floor(b) for f, b in zip(lf, bf)]
    return [check("4 beats detected from the music at 0.5 s steps (+/-15 ms)", len(beats) == 4 and max(abs(a_ - b) for a_, b in zip(beats, beats_true)) <= .015, beats, beats_true),
            check("4 cuts found in the rendered video", len(found) == 4, found, [15, 30, 45, 60]),
            check("every cut on the beat or one frame before (offset in {-1, 0})", all(o in (-1, 0) for o in offs) and len(offs) == 4, offs, "0/-1"),
            check("music muxed with the edit", has_audio, has_audio, True),
            check("negative control: cuts 2 frames late violate the rule", not all(o in (-1, 0) for o in loffs), loffs, "+2")], [out]


def _hero_box(f, col):
    m = np.abs(f - col).max(-1) < 3
    if not m.any():
        return None
    ys, xs = np.nonzero(m)
    return (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))


@card("TRANS-435")
def one_shape_never_cut(task, wd):
    """One hero shape survives every transition and changes role button -> card -> screen through morph and scale
    (eased box and corner radius), never cut."""
    col = np.array([255, 120, 40.0])
    keys = [((76, 80, 116, 96), 8), ((46, 20, 146, 90), 12), ((0, 0, W - 1, H - 1), 0)]
    ease = _CURVES["easeInOutCubic"]
    frames = []
    seg = 15
    for i in range(2):
        (b0, r0), (b1, r1) = keys[i], keys[i + 1]
        for k in range(seg):
            u = ease(k / seg)
            box = tuple(a + (b - a) * u for a, b in zip(b0, b1))
            rad = r0 + (r1 - r0) * u
            m = _rounded(H, W, (box[0], box[1], box[2] + 1, box[3] + 1), max(.01, rad)) > .5
            f = np.zeros((H, W, 3)) + [20, 22, 30]
            f[m] = col
            frames.append(f)
    f = np.zeros((H, W, 3)) + col
    frames.append(f)
    out, O = _seq_out(wd, "hero_shape", frames)
    boxes = [_hero_box(f, col) for f in O]
    present = all(b is not None for b in boxes)
    jump = max(max(abs(a - b) for a, b in zip(p, q)) for p, q in zip(boxes, boxes[1:])) if present else 999
    hard = [frames[0]] * 15 + [frames[-1]] * 16
    _, C = _seq_out(wd, "input_hard_cuts", hard)
    cb = [_hero_box(f, col) for f in C]
    cj = max(max(abs(a - b) for a, b in zip(p, q)) for p, q in zip(cb, cb[1:]))
    return [check("the hero shape is on screen in every frame", present, sum(b is not None for b in boxes), len(boxes)),
            check("no edge of the hero jumps more than 12 px between frames (never cut)", jump <= 12, jump, "<=12"),
            check("ends as the full screen", boxes[-1] == (0, 0, W - 1, H - 1), boxes[-1], [0, 0, W - 1, H - 1]),
            check("negative control: hard cuts make the hero jump", not cj <= 12, cj, ">12")], [out]


@card("TRANS-436")
def circle_mask_from_hero(task, wd):
    """Boolean circle mask growing from the hero shape's centre (not the frame centre) over 700 ms ease-in-out,
    revealing the next scene."""
    A, B = _AB()
    hx, hy = 140.0, 70.0
    n = _frames_for(700)
    ease = _CURVES["easeInOutCubic"]
    R = max(math.hypot(hx - x, hy - y) for x in (0, W) for y in (0, H))
    rs = [R * ease(k / n) for k in range(n + 1)]
    frames = []
    for r in rs:
        m = _disc_mask(H, W, hx, hy, r, ss=2)[..., None]
        frames.append(A * (1 - m) + B * m)
    out, O = _seq_out(wd, "circle_reveal", frames)
    base = (np.abs(A - B).max(-1) < 2)
    res = []
    for f, r in zip(O, rs):
        m = (np.abs(f - B).max(-1) < 2) & ~base
        if 3 < r < 30:
            ys, xs = np.nonzero(m)
            res.append((float(xs.mean()) + .5, float(ys.mean()) + .5, math.sqrt(m.sum() / math.pi), r))
    cen_err = max(math.hypot(x - hx, y - hy) for x, y, _, _ in res)
    r_err = max(abs(a - b) for _, _, a, b in res)
    _, C = _seq_out(wd, "input_held", [A] * (n + 1))
    area = int(((np.abs(C[-1] - B).max(-1) < 2) & ~base).sum())
    return [check("the reveal is centred on the hero (<= 1 px)", cen_err <= 1, cen_err, "<=1"),
            check("radius follows R*easeInOutCubic(t/0.7 s) (+/-1 px)", r_err <= 1, r_err, "<=1"),
            check("fully revealed after 700 ms (21 frames)", float(np.abs(O[-1] - B).max()) < 1 and n == 21, n, 21),
            check("negative control: the held input reveals nothing", not area > 0, area, 0)], [out]


@card("TRANS-437")
def screen_push_and_sheet(task, wd):
    """App screen push: the incoming screen travels the full width from inline-end over 470 ms
    cubic-bezier(.2,.8,.2,1), the outgoing one parallaxes 30% and dims 60%; modal sheet up 380 ms
    cubic-bezier(.4,0,.2,1)."""
    out_s = np.zeros((H, W, 3)) + [240, 240, 245]
    out_s[10:30, 10:180] = [60, 60, 200]
    in_s = np.zeros((H, W, 3)) + [30, 160, 120]
    n = _frames_for(470)
    e = _bez(.2, .8, .2, 1)
    frames, xin, dims = [], [], []
    for k in range(n + 1):
        u = e(k / n)
        x_in = int(round(W * (1 - u)))
        x_out = int(round(-.3 * W * u))
        dim = 1 - .6 * u
        f = np.zeros((H, W, 3))
        src = np.roll(out_s, x_out, 1)
        f[:] = src * dim
        f[:, x_in:] = in_s[:, :W - x_in]
        frames.append(f)
        xin.append(x_in)
        dims.append(dim)
    out, O = _seq_out(wd, "push", frames)
    meas = []
    for f in O:
        eq = (np.abs(f - in_s).max(-1) < 1).all(0)
        meas.append(int(np.argmax(eq)) if eq.any() else W)
    dim_m = [float(f[50, 5, 0] / 240) if x > 10 else None for f, x in zip(O, xin)]
    derr = max(abs(a - b) for a, b in zip(dim_m, dims) if a is not None)
    ns = _frames_for(380)
    e2 = _bez(.4, 0, .2, 1)
    sheet_frames, ys = [], []
    for k in range(ns + 1):
        y = int(round(H - 70 * e2(k / ns)))
        f = out_s.copy()
        f[y:] = [255, 255, 255]
        sheet_frames.append(f)
        ys.append(y)
    sh, S = _seq_out(wd, "sheet", sheet_frames)
    sm = [int(np.argmax((np.abs(f - 255).max(-1) < 1).all(1))) if (np.abs(f - 255).max(-1) < 1).all(1).any() else H for f in S]
    _, C = _seq_out(wd, "input_static", [out_s] * (n + 1))
    cm = [int(np.argmax((np.abs(f - in_s).max(-1) < 1).all(0))) if (np.abs(f - in_s).max(-1) < 1).all(0).any() else W for f in C]
    return [check("incoming edge follows W*(1 - bezier(.2,.8,.2,1)) over 470 ms (+/-1 px)", max(abs(a - b) for a, b in zip(meas, xin)) <= 1, meas[::3], xin[::3]),
            check("outgoing screen dims to 40% (dim error < 0.02)", derr < .02, derr, "<0.02"),
            check("sheet rises 70 px with bezier(.4,0,.2,1) in 380 ms (+/-1 px)", max(abs(a - b) for a, b in zip(sm, ys)) <= 1, sm[::3], ys[::3]),
            check("negative control: a static screen never pushes", not max(abs(a - b) for a, b in zip(cm, xin)) <= 1, cm[-1], 0)], [out, sh]


@card("TRANS-438")
def dynamic_photo_masks(task, wd):
    """Feathered wipe with the mask leading the photo: 600 ms cubic-bezier(.65,0,.35,1), feather 1.5% of the width,
    the photo's own slide lagging 75 ms; circle variant r 0 -> full in 450 ms with the inner photo counter-scaling
    1.15 -> 1.00."""
    from scipy.ndimage import affine_transform
    hh, ww, fps = 108, 400, 60
    xx, yy = _grid(hh, ww)
    photo = np.zeros((hh, ww, 3)) + [200, 150, 90]
    bg = np.zeros((hh, ww, 3)) + [15, 15, 25]
    e = _bez(.65, 0, .35, 1)
    feather = .015 * ww
    n = int(.6 * fps) + int(.075 * fps)
    frames, edges, shifts = [], [], []
    for k in range(n + 1):
        t = k / fps
        xm = (ww + feather) * e(t / .6)
        dx = 20 * (1 - e((t - .075) / .6))
        m = np.clip((xm - xx) / feather, 0, 1)[..., None]
        ph = photo.copy()
        mx = int(round(60 + dx))
        ph[48:60, mx:mx + 4] = 255
        frames.append(bg * (1 - m) + ph * m)
        edges.append(xm)
        shifts.append(dx)
    out, O = _seq_out(wd, "feather_wipe", frames, fps)
    k_mid = next(k for k, x in enumerate(edges) if x > ww / 2)
    prof = (_luma(O[k_mid][20]) - _luma(bg[0, 0])) / (_luma(photo[0, 0]) - _luma(bg[0, 0]))
    w1090 = float(np.sum((prof > .1) & (prof < .9)))
    pos = []
    for f in O:
        row = _luma(f[54])
        cand = np.nonzero(row[40:120] > 240)[0]
        pos.append(float(cand.mean() + 40 - 1.5) if len(cand) == 4 else None)
    t_m = next(k for k, x in enumerate(edges) if x >= (ww + feather) / 2) / fps
    valid = [(k / fps, p) for k, p in enumerate(pos) if p is not None]
    t_p = next(t for t, p in valid if p <= 70)
    lead = t_p - t_m
    nc = int(.45 * fps)
    cfr, scales = [], []
    R = math.hypot(ww / 2, hh / 2)
    ring = np.zeros((hh, ww, 3)) + [40, 40, 40]
    ring[_disc_mask(hh, ww, ww / 2, hh / 2, 20) > .5] = [250, 250, 250]
    for k in range(nc + 1):
        u = _CURVES["easeOutCubic"](k / nc)
        s = 1.15 - .15 * u
        scales.append(s)
        cy, cx = (hh - 1) / 2, (ww - 1) / 2
        inner = np.stack([affine_transform(ring[..., c], [1 / s, 1 / s], offset=[cy - cy / s, cx - cx / s], order=1, mode="nearest") for c in range(3)], -1)
        m = _disc_mask(hh, ww, ww / 2, hh / 2, R * u, ss=1)[..., None]
        cfr.append(bg * (1 - m) + inner * m)
    cv, CV = _seq_out(wd, "circle_counter_scale", cfr, fps)
    r_first = _radius(CV[nc // 6])
    r_last = _radius(CV[-1])
    hard = [bg * (xx[..., None] > edges[k]) + photo * (xx[..., None] <= edges[k]) for k in range(n + 1)]
    _, Hd = _seq_out(wd, "input_hard_wipe", hard, fps)
    hp = (_luma(Hd[k_mid][20]) - _luma(bg[0, 0])) / (_luma(photo[0, 0]) - _luma(bg[0, 0]))
    hw = float(np.sum((hp > .1) & (hp < .9)))
    return [check("feather ~1.5% of the width: 10-90% ramp = 0.8 x 6 px (3.5-6.5 px)", 3.5 <= w1090 <= 6.5, w1090, 4.8),
            check("mask leads the photo by 60-90 ms", .055 <= lead <= .095, lead, .075),
            check("circle variant: inner photo counter-scales (mid radius 20*1.15..1.0 > final)", r_first > r_last + .8 and abs(r_last - 20) <= .5, [r_first, r_last], "1.15->1.0"),
            check("negative control: a hard-edged wipe has no feather", not 3.5 <= hw <= 6.5, hw, "<3.5")], [out, cv]


@card("TRANS-439")
def photo_to_graphic_trace(task, wd):
    """Photo-to-graphic: the outline traces the subject over 900 ms easeInOutCubic (dash progress), the photo fades
    out over 300 ms from 700 ms, and the vector fill arrives 150 ms after the trace."""
    fps = 30
    photo = _photo(H, W, 9)
    cx, cy, rx, ry = 96, 54, 50, 34
    pts = [(cx + rx * math.cos(2 * math.pi * i / 400), cy + ry * math.sin(2 * math.pi * i / 400)) for i in range(401)]
    bg = np.array([250, 248, 244.0])
    stroke_col = (10, 10, 10)
    fill_col = np.array([255, 200, 60.0])
    inside = ((_grid()[0] - cx) / rx) ** 2 + ((_grid()[1] - cy) / ry) ** 2 < .92

    def frame(t):
        tr = _CURVES["easeInOutCubic"](t / .9)
        ph = 1 - float(np.clip((t - .7) / .3, 0, 1))
        fl = float(np.clip((t - 1.05) / .2, 0, 1))
        f = bg * (1 - ph) + photo * ph
        f = np.where(inside[..., None], f * (1 - fl) + fill_col * fl, f)
        im = Image.fromarray(_u8(f))
        k = int(round(tr * 400))
        if k >= 2:
            ImageDraw.Draw(im).line(pts[:k], fill=stroke_col, width=2)
        return np.asarray(im).astype(float), tr, ph, fl
    data = [frame(k / fps) for k in range(40)]
    out, O = _seq_out(wd, "trace", [d[0] for d in data], fps)
    total = None
    fracs = []
    for f in O:
        s = (np.abs(f - stroke_col).max(-1) < 3).sum()
        fracs.append(s)
    total = fracs[30]
    meas = [a / total for a in fracs[:28]]
    exp = [d[1] for d in data[:28]]
    terr = max(abs(a - b) for a, b in zip(meas, exp))
    far = ((_grid()[0] - cx) / rx) ** 2 + ((_grid()[1] - cy) / ry) ** 2 > 1.3
    region = far & (np.abs(photo - bg).max(-1) > 20)
    ph_m = []
    for k in (20, 24, 27, 30):
        d = (photo - bg)[region].ravel()
        ph_m.append(float(((O[k] - bg)[region].ravel() @ d) / (d @ d)))
    ph_e = [data[k][2] for k in (20, 24, 27, 30)]
    fill_before = max(float(np.abs(O[k][inside] - fill_col).max(-1).__lt__(3).mean()) for k in range(31))
    fill_after = float((np.abs(O[38][inside] - fill_col).max(-1) < 3).mean())
    _, P = _seq_out(wd, "input_photo", [photo] * 10, fps)
    ps = int((np.abs(P[5] - stroke_col).max(-1) < 3).sum())
    return [check("trace length follows easeInOutCubic over 900 ms (max error < 0.06)", terr < .06, terr, "<0.06"),
            check("photo opacity 1 at 700 ms, then fades to 0 by 1000 ms (+/-0.05)", max(abs(a - b) for a, b in zip(ph_m, ph_e)) < .05, ph_m, ph_e),
            check("no vector fill before 1050 ms, full fill after (>95%)", fill_before < .02 and fill_after > .95, [fill_before, fill_after], [0, 1]),
            check("negative control: the photo alone has no traced outline", not ps > 50, ps, ">50")], [out]


# ============================================================================ browser engines (Chromium + three.js)
_DRIVER = r"""
const {chromium} = require(%(pw)s);
const fs = require('fs');
(async () => {
  const b = await chromium.launch({args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist',
                                           '--allow-file-access-from-files']});
  const pg = await b.newPage({viewport: {width: %(w)d, height: %(h)d}, deviceScaleFactor: 1});
  const errs = [];
  pg.on('pageerror', e => errs.push(String(e)));
  await pg.exposeFunction('__shot', async (name) => { await pg.screenshot({path: %(wd)s + '/' + name + '.png'}); return true; });
  await pg.goto(%(url)s);
  let r;
  try { r = await pg.evaluate(async () => await window.__run()); } catch (e) { r = {error: String(e)}; }
  r.page_errors = errs;
  fs.writeFileSync(%(out)s, JSON.stringify(r));
  await b.close();
})();
"""


def _pw_path():
    for base in [Path(shutil.which("node") or "/usr/bin/node").resolve().parent.parent / "lib/node_modules",
                 Path("/opt/node22/lib/node_modules"), Path("/usr/lib/node_modules"), Path("/usr/local/lib/node_modules")]:
        if (base / "playwright").exists():
            return base / "playwright"
    raise RuntimeError("node playwright not installed")


def _browser(wd, name, html_body, size=(320, 180), timeout=60):
    """Load a page in Chromium (SwiftShader WebGL); window.__run() returns JSON; data:image/png values are saved."""
    import base64
    page = Path(wd) / (name + ".html")
    page.write_text(html_body, encoding="utf-8")
    res = Path(wd) / (name + "_result.json")
    drv = Path(wd) / (name + "_drive.js")
    drv.write_text(_DRIVER % {"pw": json.dumps(str(_pw_path())), "w": size[0], "h": size[1], "wd": json.dumps(str(wd)),
                              "url": json.dumps(page.as_uri()), "out": json.dumps(str(res))}, encoding="utf-8")
    fx.run(["node", drv], timeout=timeout)
    r = json.loads(res.read_text(encoding="utf-8"))
    if r.get("error"):
        raise RuntimeError("page: %s %s" % (r["error"], r.get("page_errors")))
    for k, v in list(r.items()):
        if isinstance(v, str) and v.startswith("data:image/png;base64,"):
            p = Path(wd) / ("%s_%s.png" % (name, k))
            p.write_bytes(base64.b64decode(v.split(",", 1)[1]))
            r[k] = str(p)
    res.write_text(json.dumps(r), encoding="utf-8")
    return r, res


def _k3_page(js, w, h):
    return ("<!doctype html><html><body style='margin:0;background:#000'><canvas id='c' width='%d' height='%d'></canvas>"
            "<script src='%s'></script><script>%s</script></body></html>" % (w, h, (KIT / "three-kit.bundle.js").as_uri(), js))


_THREE_PRE = """
const T = K3.THREE, cv = document.getElementById('c');
const R = new T.WebGLRenderer({canvas: cv, preserveDrawingBuffer: true, antialias: false});
R.setPixelRatio(1); R.setSize(cv.width, cv.height, false);
const shot = () => cv.toDataURL('image/png');
"""


@card("TEX-49")
def chrome_cubecamera(task, wd):
    """three.js (K3.THREE 0.186.1): WebGLCubeRenderTarget(256, HalfFloat, mipmaps) + CubeCamera(.05, 600); the orb is
    MeshStandardMaterial metalness 1 roughness .06 with envMap = the cube; per frame hide orb -> cubeCam.update ->
    show -> render, so it reflects the actual scene live."""
    js = _THREE_PRE + """
window.__run = async () => {
  const out = {};
  for (const useEnv of [true, false]) {
    const scene = new T.Scene();
    const faces = [0xff2020, 0x20ff20, 0xffffff, 0x404040, 0x2040ff, 0xffff20].map(c => new T.MeshBasicMaterial({color: c, side: T.BackSide}));
    scene.add(new T.Mesh(new T.BoxGeometry(20, 20, 20), faces));
    const box = new T.Mesh(new T.BoxGeometry(1.4, 1.4, 1.4), new T.MeshBasicMaterial({color: 0xff00ff})); scene.add(box);
    const rt = new T.WebGLCubeRenderTarget(256, {type: T.HalfFloatType, generateMipmaps: true, minFilter: T.LinearMipmapLinearFilter});
    const cc = new T.CubeCamera(0.05, 600, rt); scene.add(cc);
    const orb = new T.Mesh(new T.SphereGeometry(1, 64, 32), new T.MeshStandardMaterial({metalness: 1, roughness: 0.06, envMap: useEnv ? rt.texture : null}));
    scene.add(orb);
    const cam = new T.PerspectiveCamera(40, cv.width / cv.height, 0.1, 100); cam.position.set(0, 0, 4.5); cam.lookAt(0, 0, 0);
    for (const [k, a] of (useEnv ? [['left', Math.PI * 0.75], ['right', Math.PI * 0.25]] : [['left', Math.PI * 0.75]])) {
      box.position.set(3 * Math.cos(a), 0, 3 * Math.sin(a));
      orb.visible = false; if (useEnv) cc.update(R, scene); orb.visible = true; R.render(scene, cam);
      out[(useEnv ? 'env_' : 'noenv_') + k] = shot();
    }
  }
  return out;
};"""
    r, res = _browser(wd, "cubecam", _k3_page(js, 192, 144), (192, 144))
    E, E2, N = _load(r["env_left"]), _load(r["env_right"]), _load(r["noenv_left"])
    hh, ww = E.shape[:2]
    cx, cy = ww / 2, hh / 2
    rad = hh / 2 * math.tan(math.asin(1 / 4.5)) / math.tan(math.radians(20))
    o = rad * .72

    def px(img, x, y):
        return img[int(y) - 1:int(y) + 2, int(x) - 1:int(x) + 2].reshape(-1, 3).mean(0)
    left, right, centre = px(E, cx - o, cy), px(E, cx + o, cy), px(E, cx, cy)
    disc = _disc_mask(hh, ww, cx, cy, rad * .9, ss=1) > .5
    live = float(np.abs(E[disc] - E2[disc]).mean())
    nl = px(N, cx - o, cy)
    green = lambda c: c[1] > 120 and c[1] > 1.6 * max(c[0], c[2])
    return [check("orb reflects the -x wall on its left (green dominant)", green(left), left.tolist(), "green"),
            check("orb reflects the +x wall on its right (red dominant)", right[0] > 120 and right[0] > 1.6 * max(right[1], right[2]), right.tolist(), "red"),
            check("orb centre reflects the wall behind the camera (+z, blue)", centre[2] > 1.4 * max(centre[0], centre[1]), centre.tolist(), "blue"),
            check("reflection is live: moving the box changes the orb (mean diff > 1)", live > 1, live, ">1"),
            check("negative control: the same orb without the cube envMap shows no green wall", not green(nl), nl.tolist(), "not green")], [Path(r["env_left"]), res]


@card("TEX-92")
def pebbles_and_blades(task, wd):
    """K3.makePebbles({n, region, accept, height, size, flat, clump, seed}) instanced noise-deformed icosahedra in
    4 HSL colour families gathered in drifts, and K3.makeBlades({n, region, tall, width, seed}) tapered swaying reeds,
    run in Chromium and measured from the instance buffers."""
    js = _THREE_PRE + """
window.__run = async () => {
  const reg = [-5, 5, -5, 5], acc = (x, z) => Math.hypot(x, z) < 4.5, h = (x, z) => 0.1 * x;
  const take = (m) => { const P = [], C = []; const mat = new T.Matrix4(), p = new T.Vector3(), q = new T.Quaternion(), s = new T.Vector3(), c = new T.Color();
    for (let i = 0; i < m.count; i++) { m.getMatrixAt(i, mat); mat.decompose(p, q, s); P.push([p.x, p.y, p.z, s.x, s.y, s.z]); m.getColorAt(i, c); const hsl = {}; c.getHSL(hsl); C.push([hsl.h, hsl.s, hsl.l]); } return {P, C}; };
  const peb = K3.makePebbles({n: 2400, region: reg, accept: acc, height: h, size: 0.06, flat: 0.5, clump: 0.55, seed: 31});
  const uni = K3.makePebbles({n: 2400, region: reg, accept: acc, height: h, size: 0.06, flat: 0.5, seed: 31});
  const bl = K3.makeBlades({n: 1500, region: reg, accept: acc, height: h, tall: 0.9, width: 0.02, seed: 17});
  const gp = bl.geometry.attributes.position; const V = []; for (let i = 0; i < gp.count; i++) V.push([gp.getX(i), gp.getY(i), gp.getZ(i)]);
  const pp = peb.geometry.attributes.position; let ymax = 0, xmax = 0; for (let i = 0; i < pp.count; i++) { ymax = Math.max(ymax, Math.abs(pp.getY(i))); xmax = Math.max(xmax, Math.abs(pp.getX(i))); }
  const scene = new T.Scene(); scene.background = new T.Color(0x203040);
  scene.add(new T.HemisphereLight(0xffffff, 0x404040, 2)); const sun = new T.DirectionalLight(0xffffff, 2); sun.position.set(3, 6, 2); scene.add(sun);
  scene.add(peb); scene.add(bl);
  const cam = new T.PerspectiveCamera(45, cv.width / cv.height, 0.05, 100); cam.position.set(0, 6, 6); cam.lookAt(0, 0, 0); R.render(scene, cam);
  return {peb: take(peb), uni: take(uni), blades: {count: bl.count, verts: V}, flat_ratio: ymax / xmax, render: shot()};
};"""
    r, res = _browser(wd, "pebbles", _k3_page(js, 320, 180), (320, 180))
    P = np.array(r["peb"]["P"])
    Cc = np.array(r["peb"]["C"])
    U = np.array(r["uni"]["P"])
    inside = bool((np.hypot(P[:, 0], P[:, 2]) < 4.5).all())
    on_ground = float(np.abs(P[:, 1] - (.1 * P[:, 0] + P[:, 4] * .15)).max())

    def dispersion(Q):
        sel = (np.abs(Q[:, 0]) < 3) & (np.abs(Q[:, 2]) < 3)
        cnt, _, _ = np.histogram2d(Q[sel, 0], Q[sel, 2], bins=8, range=[[-3, 3], [-3, 3]])
        return float(cnt.var() / max(1e-9, cnt.mean()))
    dc, du = dispersion(P), dispersion(U)
    fam = np.where(Cc[:, 1] < .135, np.where(Cc[:, 2] > .6, 3, 0), np.where(Cc[:, 2] < .3, 2, 1))
    shares = [float((fam == i).mean()) for i in range(4)]
    V = np.array(r["blades"]["verts"])
    ys = V[:, 1]
    base_w = np.ptp(V[np.abs(ys - ys.min()) < 1e-6][:, 0])
    top_w = np.ptp(V[np.abs(ys - ys.max()) < 1e-6][:, 0])
    img = _load(r["render"])
    return [check("pebbles placed only where accept() is true and sitting on height(x, z)", inside and on_ground < 1e-4, [inside, on_ground], "inside, on ground"),
            check("water-worn flattening: geometry y extent ~ flat .5 of x extent (0.4-0.65)", .4 <= r["flat_ratio"] <= .65, r["flat_ratio"], .5),
            check("drifts: clumped pebbles over-dispersed (index > 3)", dc > 3, dc, ">3"),
            check("4 colour families near .45/.30/.17/.08 (+/-0.08)", all(abs(a - b) <= .08 for a, b in zip(shares, [.45, .30, .17, .08])), shares, [.45, .30, .17, .08]),
            check("reed blades taper: top width = 8% of base (+/-2%)", abs(top_w / base_w - .08) <= .02, float(top_w / base_w), .08),
            check("blade count 1500 and the frame rendered", r["blades"]["count"] == 1500 and img.std() > 5, [r["blades"]["count"], float(img.std())], 1500),
            check("negative control: without clump the scatter is near-Poisson (index <= 3)", not du > 3, du, "<=3")], [Path(r["render"]), res]


@card("TEX-93")
def pond_terrain_caustics(task, wd):
    """K3.makeTerrain({size 44, seg 320, albedoRepeat 10, normalRepeat 22, normalScale .8, texSize 512}) coloured by
    depth and slope (silt/sand/mud/moss) and K3.addCaustics(material, {time, level 0, strength 3.2, scale 5.5,
    absorb [1.35,.42,1.0], sun}): animated caustics on the bed that absorb red with depth."""
    js = _THREE_PRE + """
const {fbm, smooth, clamp01, lerp} = K3;
const RX = 6.4, RZ = 4.1, rOf = (x, z) => Math.hypot(x / RX, z / RZ);
function height(x, z) { const r = rOf(x, z), n = fbm(x * 0.35 + 3, z * 0.35 + 7, 4), m = fbm(x * 1.8 + 11, z * 1.8 + 2, 3);
  const bowl = -0.92 * Math.pow(clamp01(1 - r * r), 0.65) - 0.04, bank = 0.1 + 0.18 * smooth(1.0, 2.2, r) + 0.12 * n;
  return lerp(bowl + 0.05 * m, bank + 0.03 * m, smooth(0.93, 1.06, r)); }
function groundColour(h, slope, x, z, c) { const n = 0.5 + 0.5 * fbm(x * 0.9 + 5, z * 0.9 + 1, 3), r = rOf(x, z);
  const silt = new T.Color(0x4a4532), sand = new T.Color(0x857a5c), mud = new T.Color(0x2e2a20), moss = new T.Color(0x3d5a26), moss2 = new T.Color(0x5f7a33);
  if (h < -0.02) c.copy(silt).lerp(sand, smooth(-0.5, -0.05, h) * 0.6 + 0.25 * n);
  else c.copy(mud).lerp(moss, smooth(1.0, 1.25, r)).lerp(moss2, n * smooth(1.2, 2, r) * 0.7); }
window.__run = async () => {
  const out = {};
  const sunDir = new T.Vector3(0.4, 1, 0.3).normalize();
  for (const caus of [true, false]) {
    const scene = new T.Scene(); scene.background = new T.Color(0x8fb1d6);
    scene.add(new T.HemisphereLight(0xffe2bf, 0x2d3a22, 1.2)); const sun = new T.DirectionalLight(0xfff0d0, 3); sun.position.copy(sunDir).multiplyScalar(30); scene.add(sun);
    const ground = K3.makeTerrain({height, colour: groundColour, size: 44, seg: 320, albedoRepeat: 10, normalRepeat: 22, normalScale: 0.8, roughness: 0.9, texSize: 512});
    const time = {value: 0};
    if (caus) K3.addCaustics(ground.material, {time, level: 0, strength: 3.2, scale: 5.5, absorb: [1.35, 0.42, 1.0], sun: {value: sunDir.clone()}});
    scene.add(ground);
    if (caus) { const col = ground.geometry.attributes.color, pos = ground.geometry.attributes.position; const deep = [], bank = [];
      for (let i = 0; i < pos.count; i += 7) { const y = pos.getY(i); const c = [col.getX(i), col.getY(i), col.getZ(i)]; if (y < -0.6) deep.push(c); else if (rOf(pos.getX(i), pos.getZ(i)) > 1.6) bank.push(c); }
      out.deep = deep.slice(0, 400); out.bank = bank.slice(0, 400); }
    const cam = new T.PerspectiveCamera(40, cv.width / cv.height, 0.05, 200); cam.position.set(0, 13, 0.01); cam.lookAt(0, 0, 0);
    for (const [k, t] of [['t0', 0], ['t1', 0.7]]) { time.value = t; R.render(scene, cam); out[(caus ? 'c_' : 'n_') + k] = shot(); }
  }
  return out;
};"""
    r, res = _browser(wd, "pond", _k3_page(js, 320, 200), (320, 200), timeout=90)
    C0, C1, N0, N1 = (_load(r[k]) for k in ("c_t0", "c_t1", "n_t0", "n_t1"))
    hh, ww = C0.shape[:2]
    xx, yy = _grid(hh, ww)
    half = 13 * math.tan(math.radians(20))
    wx, wz = (xx - ww / 2) / (hh / 2) * half, (yy - hh / 2) / (hh / 2) * half
    rr = np.hypot(wx / 6.4, wz / 4.1)
    water, deep_px, shallow_px, bank_px = rr < .85, rr < .3, (rr > .6) & (rr < .85), rr > 1.5
    anim = float(np.abs(C0 - C1)[water].mean())
    still_bank = float(np.abs(C0 - C1)[bank_px].mean())
    n_anim = float(np.abs(N0 - N1)[water].mean())
    rg = lambda I, m: float(I[m][:, 0].mean() / max(1, I[m][:, 1].mean()))
    absorb = rg(C0, shallow_px) - rg(C0, deep_px)
    absorb_n = rg(N0, shallow_px) - rg(N0, deep_px)
    lin = lambda c: np.where(c <= .04045, c / 12.92, ((c + .055) / 1.055) ** 2.4)  # THREE.Color stores linear sRGB
    silt, sand = lin(_hex("#4a4532") / 255), lin(_hex("#857a5c") / 255)
    deep = np.array(r["deep"])
    bank = np.array(r["bank"])
    seg = sand - silt
    tt = (deep - silt) @ seg / (seg @ seg)
    resid = float(np.abs(deep - silt - tt[:, None] * seg).max(1).max())
    deep_ok = resid < .02 and float(tt.min()) >= -.01 and float(tt.max()) <= .27
    bank_green = float((bank[:, 1] > bank[:, 0]).mean())
    return [check("bed coloured by depth: deepest vertices lie on silt #4a4532 -> sand with mix <= .25 (noise only)", deep_ok, [resid, float(tt.min()), float(tt.max())], "on segment, t<=0.25"),
            check("bank coloured moss (green > red on > 80% of bank vertices)", bank_green > .8, bank_green, ">0.8"),
            check("caustics animate under water (mean frame diff > 1)", anim > 1, anim, ">1"),
            check("the dry bank is not animated (diff < 0.2)", still_bank < .2, still_bank, "<0.2"),
            check("red absorbed with depth: R/G drops from shallow to deep by > 0.05", absorb > .05, absorb, ">0.05"),
            check("negative control: the bed without addCaustics does not animate", not n_anim > 1, n_anim, "<=1")], [Path(r["c_t0"]), Path(r["c_t1"]), res]


@card("TEX-94")
def wet_asphalt_road(task, wd):
    """Road ribbon from a CatmullRom curve (8 m wide) in MeshStandard 0x15161a roughness .32 (slightly wet, lamps
    glint on it); paint 0xe8e4da emissive 0x6a6658 x.6; dashes .16 x 3 m every 12 m and .14 m edge lines at
    +/-(4 - .35) m."""
    js = _THREE_PRE + """
window.__run = async () => {
  const out = {};
  const curve = new T.CatmullRomCurve3([...Array(12)].map((_, i) => new T.Vector3(3 * Math.sin(i / 4), 0.02, 10 - i * 20)));
  const ribbon = (half, y) => { const N = 400, pos = [], idx = []; for (let i = 0; i <= N; i++) { const u = i / N, p = curve.getPointAt(u), tg = curve.getTangentAt(u); const nx = -tg.z, nz = tg.x, l = Math.hypot(nx, nz);
      pos.push(p.x - half * nx / l, y, p.z - half * nz / l, p.x + half * nx / l, y, p.z + half * nz / l); if (i < N) idx.push(2 * i, 2 * i + 1, 2 * i + 2, 2 * i + 1, 2 * i + 3, 2 * i + 2); }
    const g = new T.BufferGeometry(); g.setAttribute('position', new T.Float32BufferAttribute(pos, 3)); g.setIndex(idx); g.computeVertexNormals(); return g; };
  for (const [tag, rough, emis, lamps] of [['wet', 0.32, 0.6, true], ['dry', 0.9, 0.6, true], ['wet_dark', 0.32, 0.6, false], ['noemis_dark', 0.32, 0.0, false]]) {
    const scene = new T.Scene(); scene.background = new T.Color(0x05070d);
    scene.add(new T.HemisphereLight(0x223355, 0x050505, 0.15));
    const road = new T.Mesh(ribbon(4, 0.02), new T.MeshStandardMaterial({color: 0x15161a, roughness: rough, metalness: 0, side: T.DoubleSide})); scene.add(road);
    const paint = new T.MeshStandardMaterial({color: 0xe8e4da, roughness: 0.5, emissive: 0x6a6658, emissiveIntensity: emis});
    const L = curve.getLength(), nd = Math.floor(L / 12), dash = new T.InstancedMesh(new T.PlaneGeometry(0.16, 3), paint, nd), o = new T.Object3D();
    for (let i = 0; i < nd; i++) { const u = (i * 12 + 1.5) / L, p = curve.getPointAt(u), tg = curve.getTangentAt(u); o.position.set(p.x, 0.05, p.z); o.rotation.set(-Math.PI / 2, 0, Math.atan2(tg.x, -tg.z)); o.updateMatrix(); dash.setMatrixAt(i, o.matrix); }
    scene.add(dash);
    for (const s of [-1, 1]) { const off = (4 - 0.35); const g = ribbon(0.07, 0.04); const m = new T.Mesh(g, paint); const pos = g.attributes.position;
      const base = curve.getSpacedPoints(400); for (let i = 0; i <= 400; i++) { const tg = curve.getTangentAt(i / 400); const nx = -tg.z, nz = tg.x, l = Math.hypot(nx, nz);
        for (const j of [0, 1]) pos.setXYZ(2 * i + j, pos.getX(2 * i + j) + s * off * nx / l, 0.04, pos.getZ(2 * i + j) + s * off * nz / l); } pos.needsUpdate = true; scene.add(m); }
    if (lamps) for (let k = 0; k < 4; k++) { const p = curve.getPointAt(0.06 + k * 0.09); const lt = new T.PointLight(0xffb060, 60, 40, 2); lt.position.set(p.x + 5.5, 6, p.z); scene.add(lt); }
    const cam = new T.PerspectiveCamera(50, cv.width / cv.height, 0.1, 400); const c0 = curve.getPointAt(0.0); cam.position.set(c0.x - 1.5, 1.4, c0.z + 2); cam.lookAt(c0.x, 0.6, c0.z - 30);
    dash.visible = true; R.render(scene, cam); out[tag] = shot();
    dash.visible = false; scene.children.filter(c => c.material === paint).forEach(c => c.visible = false); R.render(scene, cam); out[tag + '_nopaint'] = shot();
    out.dashes = nd; out.length = L;
  }
  return out;
};"""
    r, res = _browser(wd, "road", _k3_page(js, 320, 180), (320, 180), timeout=90)
    I = {k: _load(r[k]) for k in ("wet", "dry", "wet_dark", "noemis_dark", "wet_nopaint", "dry_nopaint", "wet_dark_nopaint", "noemis_dark_nopaint")}
    hh = I["wet"].shape[0]
    road = slice(hh // 2 + 10, hh)

    def glint(img):
        L = _luma(img[road])
        return float(np.percentile(L, 99.5) / max(1, np.median(L)))
    gw, gd = glint(I["wet_nopaint"]), glint(I["dry_nopaint"])
    paint_mask = np.abs(I["wet_dark"] - I["wet_dark_nopaint"]).max(-1) > 6
    pd = float(_luma(I["wet_dark"])[paint_mask].mean()) if paint_mask.any() else 0.0
    asph = float(np.median(_luma(I["wet_dark_nopaint"])[road]))
    pm2 = np.abs(I["noemis_dark"] - I["noemis_dark_nopaint"]).max(-1) > 6
    pn = float(_luma(I["noemis_dark"])[paint_mask].mean()) if paint_mask.any() else 0.0
    return [check("wet asphalt (roughness .32) glints under the lamps: p99.5/median > 4", gw > 4, gw, ">4"),
            check("glint sharper than dry asphalt (roughness .9) by 1.5x", gw > 1.5 * gd, [gw, gd], "wet>1.5 dry"),
            check("retro-reflective paint glows faintly with no lamps (emissive x.6: paint luma > 3x asphalt + 10)", pd > 3 * asph + 10, [pd, asph], ">3x"),
            check("dashes every 12 m along the road", r["dashes"] == int(r["length"] // 12), [r["dashes"], r["length"]], "L/12"),
            check("negative control: the dry (rough) road does not glint like the wet one", not gd > 4 and not (gd > 1.5 * gw), gd, "<=4"),
            check("negative control: paint without emissive stays dark with no lamps", not pn > 3 * asph + 10, pn, "dark")], [Path(r["wet"]), res]


@card("TRANS-97")
def noise_dissolve_render_targets(task, wd):
    """three.js: both scenes rendered offscreen to two WebGLRenderTargets, then a full-screen ShaderMaterial mixes A and
    B by clamp(noise(uv*2.5) + progress*2 - 1, 0, 1) (noise remapped to 0..1 so progress 0 = A, 1 = B)."""
    js = _THREE_PRE + """
window.__run = async () => {
  const w = cv.width, h = cv.height, out = {};
  const mk = (bg, geo, col) => { const s = new T.Scene(); s.background = new T.Color(bg); const m = new T.Mesh(geo, new T.MeshBasicMaterial({color: col})); s.add(m); return s; };
  const sA = mk(0x101830, new T.BoxGeometry(1.4, 1.4, 1.4), 0xff3030), sB = mk(0xe8e0c8, new T.SphereGeometry(1, 48, 24), 0x2050ff);
  const cam = new T.PerspectiveCamera(45, w / h, 0.1, 50); cam.position.set(2, 1.5, 4); cam.lookAt(0, 0, 0);
  const tA = new T.WebGLRenderTarget(w, h), tB = new T.WebGLRenderTarget(w, h);
  R.setRenderTarget(tA); R.render(sA, cam); R.setRenderTarget(tB); R.render(sB, cam); R.setRenderTarget(null);
  const mat = new T.ShaderMaterial({uniforms: {tA: {value: tA.texture}, tB: {value: tB.texture}, progress: {value: 0}, plain: {value: 0}},
    vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }',
    fragmentShader: `varying vec2 vUv; uniform sampler2D tA, tB; uniform float progress, plain;
      float hash(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
      float noise(vec2 p){ vec2 i = floor(p), f = fract(p); vec2 u = f * f * (3.0 - 2.0 * f);
        return mix(mix(hash(i), hash(i + vec2(1, 0)), u.x), mix(hash(i + vec2(0, 1)), hash(i + vec2(1, 1)), u.x), u.y); }
      void main(){ float n = noise(vUv * 2.5 * vec2(1.6, 1.0) * 2.0);
        float m = plain > 0.5 ? progress : clamp(n + progress * 2.0 - 1.0, 0.0, 1.0);
        gl_FragColor = mix(texture2D(tA, vUv), texture2D(tB, vUv), m);
        #include <colorspace_fragment>
      }`});
  const quad = new T.Mesh(new T.PlaneGeometry(2, 2), mat), sc = new T.Scene(); sc.add(quad); const oc = new T.OrthographicCamera(-1, 1, 1, -1, 0, 1);
  for (const [k, p, pl] of [['p0', 0, 0], ['p50', 0.5, 0], ['p100', 1, 0], ['plain50', 0.5, 1]]) { mat.uniforms.progress.value = p; mat.uniforms.plain.value = pl; R.render(sc, oc); out[k] = shot(); }
  R.render(sA, cam); out.A = shot(); R.render(sB, cam); out.B = shot();
  return out;
};"""
    r, res = _browser(wd, "noise_dissolve", _k3_page(js, 256, 144), (256, 144))
    I = {k: _load(r[k]) for k in ("p0", "p50", "p100", "plain50", "A", "B")}
    eA = float(np.abs(I["p0"] - I["A"]).mean())
    eB = float(np.abs(I["p100"] - I["B"]).mean())
    d = (I["B"] - I["A"])
    sel = np.abs(d).sum(-1) > 60

    def mix_map(img):
        m = ((img - I["A"]) * d).sum(-1) / np.maximum(1, (d * d).sum(-1))
        return np.clip(m, 0, 1)
    m = mix_map(I["p50"])[sel]
    frac = float(m.mean())
    spread = float(m.std())
    mm = mix_map(I["p50"])
    coh = float(np.corrcoef(mm[:, :-3][sel[:, :-3]], mm[:, 3:][sel[:, :-3]])[0, 1])
    pl = mix_map(I["plain50"])[sel]
    return [check("progress 0 = scene A render target (mean error < 3, 8-bit target)", eA < 3, eA, "<3"),
            check("progress 1 = scene B render target (mean error < 3, 8-bit target)", eB < 3, eB, "<3"),
            check("progress .5 burns through ~half (B share 0.3-0.7)", .3 <= frac <= .7, frac, .5),
            check("the burn mask is noise-shaped and spatially coherent (std > 0.1, 3 px r > 0.8)", spread > .1 and coh > .8, [spread, coh], ">0.1, >0.8"),
            check("negative control: a plain crossfade at .5 has no noise mask (std <= 0.1)", not float(pl.std()) > .1, float(pl.std()), "<=0.1")], [Path(r["p50"]), res]


@card("TRANS-92")
def glsl_noise_mask_transition(task, wd):
    """The card's stated alternative to @hyperframes/shader-transitions: a hand-written GLSL noise-mask transition on a
    raw WebGL canvas, mix(colorA, colorB, clamp(noise + progress*2 - 1)), compositing two scene textures (drawn
    HTML-canvas scenes uploaded as textures)."""
    page = """<!doctype html><html><body style='margin:0'><canvas id='c' width='256' height='144'></canvas><script>
const W = 256, H = 144;
function scene(bg, fg, text){ const c = document.createElement('canvas'); c.width = W; c.height = H; const g = c.getContext('2d');
  g.fillStyle = bg; g.fillRect(0, 0, W, H); g.fillStyle = fg; g.fillRect(30, 40, 90, 60); g.font = 'bold 28px sans-serif'; g.fillText(text, 140, 85); return c; }
window.__run = async () => {
  const cv = document.getElementById('c'), gl = cv.getContext('webgl', {preserveDrawingBuffer: true});
  const vs = 'attribute vec2 p; varying vec2 uv; void main(){ uv = p * 0.5 + 0.5; uv.y = 1.0 - uv.y; gl_Position = vec4(p, 0.0, 1.0); }';
  const fs = `precision mediump float; varying vec2 uv; uniform sampler2D A, B; uniform float progress;
    float hash(vec2 q){ return fract(sin(dot(q, vec2(12.9898, 78.233))) * 43758.5453); }
    float noise(vec2 q){ vec2 i = floor(q), f = fract(q); vec2 u = f * f * (3.0 - 2.0 * f);
      return mix(mix(hash(i), hash(i + vec2(1, 0)), u.x), mix(hash(i + vec2(0, 1)), hash(i + vec2(1, 1)), u.x), u.y); }
    void main(){ float n = 0.65 * noise(uv * 6.0) + 0.35 * noise(uv * 13.0);
      gl_FragColor = mix(texture2D(A, uv), texture2D(B, uv), clamp(n + progress * 2.0 - 1.0, 0.0, 1.0)); }`;
  const sh = (t, s) => { const o = gl.createShader(t); gl.shaderSource(o, s); gl.compileShader(o); if (!gl.getShaderParameter(o, gl.COMPILE_STATUS)) throw gl.getShaderInfoLog(o); return o; };
  const pr = gl.createProgram(); gl.attachShader(pr, sh(gl.VERTEX_SHADER, vs)); gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, fs)); gl.linkProgram(pr); gl.useProgram(pr);
  const buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
  const loc = gl.getAttribLocation(pr, 'p'); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
  const tex = (unit, img, name) => { const t = gl.createTexture(); gl.activeTexture(gl.TEXTURE0 + unit); gl.bindTexture(gl.TEXTURE_2D, t);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, img); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE); gl.uniform1i(gl.getUniformLocation(pr, name), unit); };
  const a = scene('#14203a', '#ff5a3c', 'A'), b = scene('#f2ead8', '#2f6bff', 'B');
  tex(0, a, 'A'); tex(1, b, 'B');
  const out = {A: a.toDataURL('image/png'), B: b.toDataURL('image/png'), renderer: gl.getParameter(gl.RENDERER)};
  for (const [k, p] of [['p0', 0], ['p25', 0.25], ['p50', 0.5], ['p75', 0.75], ['p100', 1]]) { gl.uniform1f(gl.getUniformLocation(pr, 'progress'), p); gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4); out[k] = cv.toDataURL('image/png'); }
  return out;
};</script></body></html>"""
    r, res = _browser(wd, "glsl_mask", page, (256, 144))
    I = {k: _load(r[k]) for k in ("A", "B", "p0", "p25", "p50", "p75", "p100")}
    eA = float(np.abs(I["p0"] - I["A"]).mean())
    eB = float(np.abs(I["p100"] - I["B"]).mean())
    d = I["B"] - I["A"]
    sel = np.abs(d).sum(-1) > 60
    share = lambda img: float(np.clip(((img - I["A"]) * d).sum(-1) / np.maximum(1, (d * d).sum(-1)), 0, 1)[sel].mean())
    sh = [share(I[k]) for k in ("p0", "p25", "p50", "p75", "p100")]
    mm = np.clip(((I["p50"] - I["A"]) * d).sum(-1) / np.maximum(1, (d * d).sum(-1)), 0, 1)
    coh = float(np.corrcoef(mm[:, :-3][sel[:, :-3]], mm[:, 3:][sel[:, :-3]])[0, 1])
    fade = I["A"] * .5 + I["B"] * .5
    fm = np.clip(((fade - I["A"]) * d).sum(-1) / np.maximum(1, (d * d).sum(-1)), 0, 1)[sel]
    return [check("progress 0 shows scene A and 1 shows scene B (mean error < 2)", eA < 2 and eB < 2, [eA, eB], "<2"),
            check("B share grows monotonically with progress", all(b > a + .05 for a, b in zip(sh, sh[1:])), sh, "monotone"),
            check("noise-shaped, coherent mask at .5 (std > .1, 3 px r > .8)", float(mm[sel].std()) > .1 and coh > .8, [float(mm[sel].std()), coh], ">0.1, >0.8"),
            check("ran on a WebGL context", bool(r.get("renderer")), r.get("renderer"), "WebGL"),
            check("negative control: a plain 50% crossfade has no noise mask", not float(fm.std()) > .1, float(fm.std()), "<=0.1")], [Path(r["p50"]), res]


_VT_CSS = """
body{margin:0;background:#fff;font:14px sans-serif}
#box{position:absolute;width:60px;height:40px}
.a #box{left:20px;top:20px;background:#ff0000}
.b #box{left:20px;top:100px;background:#0000ff}
::view-transition-old(root){animation:150ms linear both vt-fade-out}
::view-transition-new(root){animation:210ms cubic-bezier(0,0,.58,1) both vt-slide-in}
@keyframes vt-fade-out{to{opacity:0}}
@keyframes vt-slide-in{from{transform:translateX(60px)}}
"""


def _vt_measure(wd, name, use_vt, hero=False):
    if hero:
        css = """body{margin:0;background:#fff}#hero{position:absolute;background:#00a000;view-transition-name:hero}
.a #hero{left:20px;top:40px;width:40px;height:40px}.b #hero{left:200px;top:30px;width:120px;height:80px}
::view-transition-group(hero){animation-duration:400ms;animation-timing-function:linear}
::view-transition-old(root),::view-transition-new(root){animation:none}"""
        inner = "<div id='hero'></div>"
    else:
        css, inner = _VT_CSS, "<div id='box'></div>"
    page = """<!doctype html><html><head><style>%s</style></head><body class='a'>%s<script>
window.__run = async () => {
  const flip = () => { document.body.className = 'b'; };
  const out = {supported: !!document.startViewTransition};
  if (%s && document.startViewTransition) {
    const vt = document.startViewTransition(flip); await vt.ready;
    const an = document.getAnimations().filter(a => a.effect && a.effect.pseudoElement);
    out.anims = an.map(a => ({name: a.animationName, pe: a.effect.pseudoElement, dur: a.effect.getTiming().duration}));
    an.forEach(a => a.pause());
    for (const [k, t] of %s) { an.forEach(a => { a.currentTime = t; }); await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))); await window.__shot('%s_' + k); out[k] = '%s_' + k + '.png';
      const de = document.documentElement, go = getComputedStyle(de, '::view-transition-old(root)'), gg = getComputedStyle(de, '::view-transition-group(hero)');
      out[k + '_old_opacity'] = parseFloat(go.opacity); out[k + '_group'] = [gg.width, gg.height]; }
    an.forEach(a => a.finish()); await vt.finished;
  } else {
    flip(); await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
    out.anims = document.getAnimations().map(a => ({name: a.animationName}));
    for (const [k, t] of %s) { await window.__shot('%s_' + k); out[k] = '%s_' + k + '.png'; }
  }
  return out;
};</script></body></html>""" % (css, inner, "true" if use_vt else "false",
                                  json.dumps([["mid", 200]] if hero else [["mid", 75], ["new105", 105]]), name, name,
                                  json.dumps([["mid", 200]] if hero else [["mid", 75], ["new105", 105]]), name, name)
    r, res = _browser(wd, name, page, (360, 180))
    return r, res


def _box_of(img, col, tol=40):
    m = np.abs(img - np.array(col)).max(-1) < tol
    if not m.any():
        return None
    ys, xs = np.nonzero(m)
    return [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]


@card("TRANS-33")
def view_transition_recipes(task, wd):
    """View Transitions recipes in Chromium: document.startViewTransition with ::view-transition-old(root) exit
    fade 150 ms and ::view-transition-new(root) enter slide 60 px over 210 ms ease-out; the animations are paused at
    known times and the frames measured."""
    r, res = _vt_measure(wd, "vt", True)
    durs = sorted(a["dur"] for a in r.get("anims", []) if a.get("pe", "").endswith("(root)"))
    n105 = _load(wd / r["new105"])
    old = r["mid_old_opacity"]
    p75 = 1 - _bez(0, 0, .58, 1)(75 / 210)
    p105 = 1 - _bez(0, 0, .58, 1)(105 / 210)
    bx = _box_of(n105, (0, 0, 255), 60)
    off = (bx[0] - 20) if bx else -99
    rn, _ = _vt_measure(wd, "novt", False)
    nm = _load(wd / rn["mid"])
    nb = _box_of(nm, (0, 0, 255), 60)
    noff = (nb[0] - 20) if nb else -99
    return [check("Chromium supports startViewTransition", r.get("supported") is True, r.get("supported"), True),
            check("old/new pseudo-element animations run 150 ms and 210 ms", durs[:2] == [150, 210], durs, [150, 210]),
            check("old snapshot fades linearly: opacity 0.5 at 75 ms of 150 (+/-0.02)", abs(old - .5) <= .02, old, .5),
            check("new snapshot slides in: offset at 105 ms = 60*(1-ease-out(.5)) = %.1f px (+/-1.5)" % (60 * p105), abs(off - 60 * p105) <= 1.5, off, 60 * p105),
            check("negative control: a plain DOM update has no slide offset", not abs(noff - 60 * p105) <= 1.5, noff, 0)], [wd / r["new105"], res]


@card("TRANS-94")
def view_transition_shared_element(task, wd):
    """View Transitions API shared-element morph: an element with view-transition-name 'hero' morphs from a small box
    to a large one; ::view-transition-group(hero) 400 ms linear, paused at 200 ms and measured."""
    r, res = _vt_measure(wd, "hero", True, hero=True)
    mid = _load(wd / r["mid"])
    bx = _box_of(mid, (0, 160, 0), 50)
    exp = [110, 35, 110 + 80, 35 + 60]
    err = max(abs(a - b) for a, b in zip(bx[:3], exp[:3])) if bx else 999
    gw, gh = (float(v.replace("px", "")) for v in r["mid_group"])
    group = [a for a in r.get("anims", []) if "group(hero)" in a.get("pe", "")]
    rn, _ = _vt_measure(wd, "hero_novt", False, hero=True)
    nb = _box_of(_load(wd / rn["mid"]), (0, 160, 0), 50)
    nerr = max(abs(a - b) for a, b in zip(nb[:3], exp[:3])) if nb else 999
    return [check("a ::view-transition-group(hero) animation of 400 ms exists", any(a["dur"] == 400 for a in group), group, 400),
            check("at 200 ms the hero is halfway in position (left/top/right within 3 px of 110/35/190)", err <= 3, bx, exp),
            check("the group box is halfway in size: 80 x 60 px (+/-1)", abs(gw - 80) <= 1 and abs(gh - 60) <= 1, [gw, gh], [80, 60]),
            check("negative control: without the view transition the hero jumps to the end state", not nerr <= 3, nb, "final box")], [wd / r["mid"], res]


@card("TRANS-35")
def starting_style_entry(task, wd):
    """CSS-only popover entry/exit: [popover] transitions opacity/transform plus display and overlay allow-discrete,
    with @starting-style giving the entry state (opacity 0, scale .95): in 0.2 s ease-out, out 0.15 s ease-in."""
    def page(starting):
        return """<!doctype html><html><head><style>
#p{opacity:1;transform:scale(1);transition:opacity .2s ease-out,transform .2s ease-out,display .2s allow-discrete,overlay .2s allow-discrete;border:0;width:120px;height:60px;background:#222}
#p:not(:popover-open){opacity:0;transform:scale(.95);transition-duration:.15s;transition-timing-function:ease-in}
%s
</style></head><body><div id='p' popover>hi</div><script>
const frame = () => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
window.__run = async () => {
  const p = document.getElementById('p'); const out = {};
  p.showPopover(); await frame();
  let an = p.getAnimations(); out.enter = an.map(a => ({prop: a.transitionProperty, dur: a.effect.getTiming().duration, kf: a.effect.getKeyframes().map(k => k.opacity || k.transform)}));
  an.forEach(a => { a.pause(); a.currentTime = 100; }); await frame();
  out.op_in_100 = parseFloat(getComputedStyle(p).opacity);
  an.forEach(a => a.finish()); await frame();
  p.hidePopover(); await frame();
  an = p.getAnimations(); out.exit = an.map(a => ({prop: a.transitionProperty, dur: a.effect.getTiming().duration}));
  an.forEach(a => { a.pause(); a.currentTime = 75; }); await frame();
  out.display_out_75 = getComputedStyle(p).display; out.op_out_75 = parseFloat(getComputedStyle(p).opacity);
  await window.__shot(%s);
  return out;
};</script></body></html>""" % ("@starting-style{#p:popover-open{opacity:0;transform:scale(.95)}}" if starting else "",
                                 json.dumps("popover_exit" if starting else "popover_nostart"))
    r, res = _browser(wd, "popover", page(True), (240, 160))
    n, nres = _browser(wd, "popover_nostart", page(False), (240, 160))
    ein = {a["prop"]: a for a in r["enter"]}
    eout = {a["prop"]: a for a in r["exit"]}
    exp_in = _bez(.42 * 0, 0, .58, 1)(.5)
    exp_out = 1 - _bez(.42, 0, 1, 1)(.5)
    return [check("entry transitions created from @starting-style: opacity 0 -> 1 and transform, 200 ms", "opacity" in ein and ein["opacity"]["dur"] == 200 and str(ein["opacity"]["kf"][0]) == "0" and "transform" in ein,
                  r["enter"], "opacity 0->1, 200 ms"),
            check("ease-out entry: opacity at 100 ms = %.3f (+/-0.02)" % exp_in, abs(r["op_in_100"] - exp_in) <= .02, r["op_in_100"], exp_in),
            check("exit 150 ms ease-in with display allow-discrete: still displayed at 75 ms", eout.get("opacity", {}).get("dur") == 150 and r["display_out_75"] != "none", [r["exit"], r["display_out_75"]], "block"),
            check("ease-in exit: opacity at 75 ms = %.3f (+/-0.02)" % exp_out, abs(r["op_out_75"] - exp_out) <= .02, r["op_out_75"], exp_out),
            check("negative control: without @starting-style no entry transition is created", not any(a["prop"] == "opacity" for a in n["enter"]), n["enter"], "none")], [res, nres]


@card("TRANS-51")
def details_height_animation(task, wd):
    """Pure-CSS accordion: html{interpolate-size:allow-keywords}; ::details-content transitions block-size 0 -> auto
    (260 ms, measured with linear timing) with content-visibility allow-discrete; the +/- badge rotates 180 deg."""
    def page(interp):
        return """<!doctype html><html><head><style>
%s
details::details-content{block-size:0;overflow:clip;transition:block-size 260ms linear,content-visibility 260ms allow-discrete}
details[open]::details-content{block-size:auto}
summary{height:20px;list-style:none}
.badge{display:inline-block;width:22px;height:22px;transition:transform 260ms cubic-bezier(.34,1.56,.64,1)}
details[open] .badge{transform:rotate(180deg)}
</style></head><body><details id='d'><summary><span class='badge'>+</span></summary><div style='height:100px'>x</div></details><script>
window.__run = async () => {
  const d = document.getElementById('d'), samples = [];
  const h0 = d.getBoundingClientRect().height;
  d.open = true; const t0 = performance.now();
  await new Promise(res => { const step = () => { const t = performance.now() - t0; samples.push([t, d.getBoundingClientRect().height]); if (t < 420) requestAnimationFrame(step); else res(); }; requestAnimationFrame(step); });
  return {h0, samples, badge: getComputedStyle(document.querySelector('.badge')).transform};
};</script></body></html>""" % ("html{interpolate-size:allow-keywords}" if interp else "")
    r, res = _browser(wd, "details", page(True), (240, 200))
    n, nres = _browser(wd, "details_nointerp", page(False), (240, 200))
    h0 = r["h0"]
    full = r["samples"][-1][1]

    def fit(samples):
        best = 1e9
        for off in np.arange(-40, 41, 2):
            errs = [abs(h - (h0 + (full - h0) * min(1, max(0, (t - off) / 260)))) for t, h in samples]
            best = min(best, float(np.sqrt(np.mean(np.square(errs)))))
        return best
    rms, nrms = fit(r["samples"]), fit(n["samples"])
    mids = [h for t, h in r["samples"] if 60 < t < 200]
    m = r["badge"]
    rot = m.startswith("matrix(-1") or m.startswith("matrix(-0.99")
    return [check("opens from the summary height to full content height", full - h0 > 90, [h0, full], "+100 px"),
            check("block-size animates 0 -> auto over 260 ms (RMS error vs linear ramp < 6 px)", rms < 6, rms, "<6"),
            check("intermediate heights observed mid-transition", any(h0 + 10 < h < full - 10 for h in mids), mids[:5], "between"),
            check("badge ends rotated 180 deg", rot, m, "matrix(-1,0,0,-1,...)"),
            check("negative control: without interpolate-size the height jumps (no ramp)", not nrms < 6, nrms, ">=6")], [res, nres]
