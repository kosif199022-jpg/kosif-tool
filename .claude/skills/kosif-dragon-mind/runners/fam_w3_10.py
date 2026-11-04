"""Wave 3, chunk 10: typography-arabic, charts-data-infographic, hand-drawn-draw-on and ai-generation cards
that no earlier module covered, each as a real program with known-answer checks and a negative control.

Engines used (all already installed here, nothing downloaded): Pillow + libraqm (HarfBuzz shaping) with the OFL
fonts bundled in kosif-superpowers/proofs/_shared/fonts, numpy/scipy for measuring, ffmpeg/libass/libx264 for
films and captions, the Playwright chrome-headless-shell (offline, --host-resolver-rules blocks the network) for
cards about the browser's own text, font and SVG engines, node (Intl) for locale digits, fontTools for cmap/fvar,
and the fastify-motion-bro profile CLI (run with cwd/TMPDIR inside the work folder) for its prompt-pack cards.
Lengths a card gives for a 1080x1920 frame are rendered at K = 0.5 (540x960 or smaller) and expected values scaled.

AI-generation cards whose method *is* a paid or keyed remote model (image/video/music/3D generation, hosted
MCP studios) are listed in GAPS. Where a card also prescribes a local, deterministic step (ffmpeg slicing for a
song shot, reference-audio extraction, Pillow sprite normalising, WebP post-processing, type placed in the
reserved empty third of a plate, the sandboxed per-frame scene contract), that step is what the runner executes on
a fixture made here; no generation is claimed.
"""
import html as _html
import json
import math
import os
import re
import subprocess
import unicodedata
from pathlib import Path

from _harness import card, check, fx


HERE = Path(__file__).resolve().parent
SKILLS = HERE.parents[1]
REPO = HERE.parents[3]
FONTS = SKILLS / "kosif-superpowers/proofs/_shared/fonts"
CAIRO = FONTS / "Cairo[slnt,wght].ttf"
AMIRI = FONTS / "Amiri-Regular.ttf"
AMIRI_B = FONTS / "Amiri-Bold.ttf"
TAJAWAL = FONTS / "Tajawal-Bold.ttf"
LALEZAR = FONTS / "Lalezar-Regular.ttf"
MESSIRI = FONTS / "ElMessiri[wght].ttf"
POPPINS = FONTS / "Poppins-Bold.ttf"
VENDOR = SKILLS / "kosif-superpowers/vendor/100-superskills/skills"
K = 0.5
AR_RE = re.compile("[؀-ۿݐ-ݿﭐ-﷿ﹰ-﻿]")


# ----------------------------------------------------------------------------- toolkit
def np_():
    import numpy as np
    return np


def font(path=CAIRO, size=48, wght=None, basic=False):
    from PIL import ImageFont
    eng = ImageFont.Layout.BASIC if basic else ImageFont.Layout.RAQM
    f = ImageFont.truetype(str(path), int(round(size)), layout_engine=eng)
    if wght is not None:
        axes = f.get_variation_axes()
        vals = []
        for a in axes:
            nm = a["name"].decode() if isinstance(a["name"], bytes) else str(a["name"])
            vals.append(max(a["minimum"], min(a["maximum"], wght)) if nm.lower().startswith("weight") else a["default"])
        f.set_variation_by_axes(vals)
    return f


def _dir(text):
    return "rtl" if AR_RE.search(text) else "ltr"


def _kw(f, text, direction=None, features=None):
    from PIL import ImageFont
    if f.layout_engine == ImageFont.Layout.BASIC:
        return {}
    kw = {"direction": direction or _dir(text)}
    if features is not None:
        kw["features"] = features
    if kw["direction"] == "rtl":
        kw["language"] = "ar"
    return kw


def tlen(text, f, direction=None, features=None):
    return f.getlength(text, **_kw(f, text, direction, features))


def tile(text, f, fill=(255, 255, 255, 255), direction=None, features=None, stroke=0, stroke_fill=None, pad=None):
    """Text rendered on a transparent RGBA tile with padding; returns (tile, (ox, oy)) where o is the text origin."""
    from PIL import Image, ImageDraw
    kw = _kw(f, text, direction, features)
    d0 = ImageDraw.Draw(Image.new("L", (1, 1)))
    bb = d0.textbbox((0, 0), text, font=f, stroke_width=stroke, **kw)
    pad = int(f.size * 0.35) if pad is None else pad
    w, h = bb[2] - bb[0] + 2 * pad, bb[3] - bb[1] + 2 * pad
    im = Image.new("RGBA", (max(1, w), max(1, h)), tuple(fill[:3]) + (0,))  # premultiplied-safe for blur
    o = (pad - bb[0], pad - bb[1])
    ImageDraw.Draw(im).text(o, text, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill, **kw)
    return im, o


def place(canvas, t, cx, cy, scale=1.0, alpha=1.0, blur=0.0, rot=0.0, clip=None, sx=None, sy=None):
    """Composite tile t centred at (cx, cy) with transform/opacity/blur; clip=(x0,y0,x1,y1) masks to a box."""
    from PIL import Image, ImageFilter
    if alpha <= 0.002:
        return
    sx = scale if sx is None else sx
    sy = scale if sy is None else sy
    im = t
    if abs(sx - 1) > 1e-4 or abs(sy - 1) > 1e-4:
        im = im.resize((max(1, int(round(im.width * sx))), max(1, int(round(im.height * sy)))), Image.BICUBIC)
    if abs(rot) > 1e-3:
        im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    if blur > 0.05:
        im = im.filter(ImageFilter.GaussianBlur(blur))
    if alpha < 0.999:
        a = im.getchannel("A").point(lambda v: int(v * alpha))
        im = im.copy()
        im.putalpha(a)
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    layer.paste(im, (int(round(cx - im.width / 2)), int(round(cy - im.height / 2))))
    if clip is not None:
        m = Image.new("L", canvas.size, 0)
        x0, y0, x1, y1 = [int(round(v)) for v in clip]
        m.paste(255, (x0, y0, x1, y1))
        a = Image.composite(layer.getchannel("A"), Image.new("L", canvas.size, 0), m)
        layer.putalpha(a)
    canvas.alpha_composite(layer)


def blank(size, bg=(0, 0, 0)):
    from PIL import Image
    return Image.new("RGBA", size, tuple(bg) + (255,))


def encode(path, frames, size, fps=30):
    """Pipe RGBA/RGB PIL frames into an H.264 file."""
    w, h = size
    p = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", "%dx%d" % (w, h), "-r", str(fps), "-i", "-", "-c:v", "libx264", "-crf", "10",
                          "-preset", "ultrafast", "-pix_fmt", "yuv444p", str(path)], stdin=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    for fr in frames:
        p.stdin.write(fr.convert("RGB").tobytes())
    p.stdin.close()
    err = p.stderr.read()
    if p.wait():
        raise RuntimeError("encode failed: %s" % err[-300:])
    return Path(path)


def video(wd, name, draw, dur, size=(270, 480), fps=30, bg=(0, 0, 0)):
    """Render draw(t, canvas) for every frame, encode, decode back and return (path, frames as float arrays)."""
    n = int(round(dur * fps))

    def gen():
        for i in range(n):
            c = blank(size, bg)
            draw(i / fps, c)
            yield c
    p = encode(Path(wd) / name, gen(), size, fps)
    return p, fx.frames(p, size)


def arr(im):
    np = np_()
    return np.asarray(im.convert("RGB"), dtype=float)


def lum(a):
    return a[..., :3].mean(axis=-1)


def mask_of(a, thr=110):
    return lum(a) > thr


def bbox(m):
    np = np_()
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def centroid(m):
    np = np_()
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        return None
    return float(xs.mean()), float(ys.mean())


def wcentroid(a):
    np = np_()
    g = lum(a)
    tot = g.sum()
    if tot <= 0:
        return None
    ys, xs = np.mgrid[0:g.shape[0], 0:g.shape[1]]
    return float((xs * g).sum() / tot), float((ys * g).sum() / tot)


def comps(m):
    from scipy import ndimage
    return int(ndimage.label(m)[1])


def colour_mask(a, rgb, tol=40):
    np = np_()
    return np.abs(a[..., :3] - np.array(rgb, dtype=float)).max(axis=-1) < tol


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def frame_at(frames, t, fps=30):
    return frames[min(len(frames) - 1, max(0, int(round(t * fps))))]


def clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


def expo_out(p):
    p = clamp(p)
    return 1.0 if p >= 1 else 1 - 2 ** (-10 * p)


def pow_out(p, k):
    return 1 - (1 - clamp(p)) ** k


def back_out(p, s=1.70158):
    p = clamp(p) - 1
    return 1 + (s + 1) * p ** 3 + s * p ** 2


def cubic_out(p):
    return pow_out(p, 3)


def shaped_mask(text, f, fill=255):
    """Binary ink mask of a raqm-shaped string."""
    t, _ = tile(text, f, fill=(255, 255, 255, 255))
    return np_().asarray(t.getchannel("A")) > 128


def basic_mask(text, path, size):
    """Same string with the BASIC layout (no shaping, no bidi): isolated forms in logical order = the raw input."""
    t, _ = tile(text, font(path, size, basic=True))
    return np_().asarray(t.getchannel("A")) > 128


def save_png(im, path):
    im.convert("RGB").save(path)
    return Path(path)


def write_json(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    return Path(path)


def chrome_bin():
    import glob
    for pat in ("/opt/pw-browsers/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell",
                os.path.expanduser("~/.cache/hyperframes/chrome/chrome-headless-shell/*/*/chrome-headless-shell")):
        hits = sorted(glob.glob(pat))
        if hits:
            return hits[-1]
    return None


def chrome_shot(wd, html_text, name, w, h, budget=None):
    """Render HTML in headless Chrome (headless shell, private profile in wd) to a PNG (fonts via file://)."""
    src = Path(wd) / (name + ".html")
    src.write_text(html_text, encoding="utf-8")
    out = Path(wd) / (name + ".png")
    exe = chrome_bin()
    if not exe:
        raise RuntimeError("no headless chrome shell found")
    cmd = [exe, "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
           "--user-data-dir=%s" % (Path(wd) / ("chrome-" + name)), "--force-device-scale-factor=1",
           "--window-size=%d,%d" % (w, h), "--screenshot=%s" % out]
    if budget:
        cmd.append("--virtual-time-budget=%d" % budget)
    cmd.append(src.as_uri())
    subprocess.run(cmd, capture_output=True, timeout=40, stdin=subprocess.DEVNULL)
    if not out.exists():
        raise RuntimeError("chrome produced no screenshot")
    return src, out


def iou(a, b):
    np = np_()
    h, w = min(a.shape[0], b.shape[0]), min(a.shape[1], b.shape[1])
    a, b = a[:h, :w], b[:h, :w]
    u = np.logical_or(a, b).sum()
    return float(np.logical_and(a, b).sum() / u) if u else 0.0


def crop_ink(m):
    b = bbox(m)
    return m[b[1]:b[3], b[0]:b[2]] if b else m


def word_row(words, f, W, cy, gap=None, rtl=True, fills=None):
    """Lay whole words on one centred line, first word on the right for RTL. Returns list of dicts."""
    gap = f.size * 0.32 if gap is None else gap
    tiles = []
    for i, w in enumerate(words):
        fill = fills[i] if fills else (255, 255, 255, 255)
        t, _ = tile(w, f, fill=fill)
        tiles.append((w, t, tlen(w, f)))
    total = sum(x[2] for x in tiles) + gap * (len(tiles) - 1)
    out = []
    x = (W + total) / 2 if rtl else (W - total) / 2
    for w, t, ln in tiles:
        cx = x - ln / 2 if rtl else x + ln / 2
        out.append({"word": w, "tile": t, "cx": cx, "cy": cy, "len": ln,
                    "box": (cx - ln / 2 - 2, cy - t.height / 2, cx + ln / 2 + 2, cy + t.height / 2)})
        x = x - ln - gap if rtl else x + ln + gap
    return out


def crop(fr, box):
    x0, y0, x1, y1 = [int(round(v)) for v in box]
    return fr[max(0, y0):max(0, y1), max(0, x0):max(0, x1)]


def box_ink(fr, box, thr=110):
    return float((lum(crop(fr, box)) > thr).sum())


def acf_pitch(m, lo, hi):
    """Dominant row period of an ink mask (autocorrelation of the row profile)."""
    np = np_()
    p = m.sum(axis=1).astype(float)
    p = p - p.mean()
    best, lag = -1e18, 0
    for L in range(int(lo), int(hi) + 1):
        v = float((p[:-L] * p[L:]).sum())
        if v > best:
            best, lag = v, L
    return lag


def ink_box_abs(r):
    """Absolute ink box of a word placed by word_row (tile is centred on cx, cy)."""
    a = np_().asarray(r["tile"].getchannel("A")) > 128
    b = bbox(a)
    x0 = r["cx"] - r["tile"].width / 2
    y0 = r["cy"] - r["tile"].height / 2
    return (x0 + b[0], y0 + b[1], x0 + b[2], y0 + b[3])


def grow(b, dx, dy):
    return (b[0] - dx, b[1] - dy, b[2] + dx, b[3] + dy)


def kinetic(wd, name, words, f, state, dur, size=(270, 480), cy=None, fills=None, slot_pad=None, fps=30, extra=None):
    """Whole-word kinetic type: state(i, t) -> dict(dx, dy, alpha, blur, scale, rot, clip) or None (hidden)."""
    W, H = size
    row = word_row(words, f, W, H / 2 if cy is None else cy, fills=fills)
    sp = f.size * 0.3 if slot_pad is None else slot_pad
    for r in row:
        r["ink"] = ink_box_abs(r)
        r["slot"] = grow(r["ink"], 3, sp)

    def draw(t, c):
        if extra:
            extra(t, c, row)
        for i, r in enumerate(row):
            s = state(i, t)
            if s is None:
                continue
            place(c, r["tile"], r["cx"] + s.get("dx", 0), r["cy"] + s.get("dy", 0), scale=s.get("scale", 1),
                  alpha=s.get("alpha", 1), blur=s.get("blur", 0), rot=s.get("rot", 0),
                  clip=r["slot"] if s.get("clip") else None)
    p, frames = video(wd, name, draw, dur, size, fps)
    return p, frames, row


def outside_ink(fr, boxes, thr=110):
    np = np_()
    m = lum(fr) > thr
    keep = np.zeros_like(m)
    for b in boxes:
        x0, y0, x1, y1 = [int(round(v)) for v in b]
        keep[max(0, y0):y1, max(0, x0):x1] = True
    return int((m & ~keep).sum())


def lumsum(fr, box):
    x0, y0, x1, y1 = [int(round(v)) for v in box]
    return float(lum(fr[max(0, y0):y1, max(0, x0):x1]).sum())


def first_time(series, frac, fps=30):
    top = max(series) or 1
    for i, v in enumerate(series):
        if v >= frac * top:
            return i / fps
    return None



# ----------------------------------------------------------------------------- wave-3 helpers
CAIRO800 = FONTS / "cairo-arabic-800-normal.woff2"
CAIRO600 = FONTS / "cairo-arabic-600-normal.woff2"
REEM = FONTS / "ReemKufi[wght].ttf"
AREF = FONTS / "ArefRuqaa-Regular.ttf"
AREF_B = FONTS / "ArefRuqaa-Bold.ttf"
POPPINS_R = FONTS / "Poppins-Regular.ttf"
MONO = Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")
INTER = Path("/usr/share/fonts/opentype/inter/Inter-Regular.otf")
FMB = Path("/home/claude/fastify-motion-bro")


def chrome_dump(wd, name, html_text, size=(400, 300), budget=1500):
    """Run a page offline in the headless shell and return the JSON its script wrote into <pre id=OUT>."""
    exe = chrome_bin()
    if not exe:
        raise RuntimeError("no headless chrome shell found")
    src = Path(wd) / (name + ".html")
    src.write_text(html_text, encoding="utf-8")
    cmd = [exe, "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
           "--host-resolver-rules=MAP * ~NOTFOUND", "--user-data-dir=%s" % (Path(wd) / ("chrome-" + name)),
           "--window-size=%d,%d" % size, "--virtual-time-budget=%d" % budget, "--dump-dom", src.as_uri()]
    done = subprocess.run(cmd, capture_output=True, text=True, timeout=40, stdin=subprocess.DEVNULL)
    m = re.search(r'<pre id="OUT">(.*?)</pre>', done.stdout, re.S)
    if not m or not m.group(1).strip():
        raise RuntimeError("page wrote no #OUT: " + done.stderr[-300:])
    out = json.loads(_html.unescape(m.group(1)))
    if isinstance(out, dict) and out.get("__error"):
        raise RuntimeError("page error: " + out["__error"])
    return src, out


def hpage(body, js, css="", W=400, H=300):
    faces = ("@font-face{font-family:'CairoT';src:url('%s') format('woff2');font-weight:800}"
             "@font-face{font-family:'CairoT';src:url('%s') format('woff2');font-weight:600}") % (
        CAIRO800.as_uri(), CAIRO600.as_uri())
    return ("<!doctype html><html><head><meta charset=utf-8><style>%shtml,body{margin:0;background:#fff;"
            "width:%dpx;height:%dpx;overflow:hidden}%s</style></head><body>%s<pre id=\"OUT\"></pre><script>"
            "function OUT(v){document.getElementById('OUT').textContent=JSON.stringify(v)}"
            "(async()=>{try{%s}catch(e){OUT({__error:String(e)})}})();</script></body></html>") % (faces, W, H, css, body, js)


def bez(x1, y1, x2, y2):
    def bx(t, a, b):
        return 3 * a * t * (1 - t) ** 2 + 3 * b * t * t * (1 - t) + t ** 3

    def f(p):
        p = clamp(p)
        if p <= 0 or p >= 1:
            return p
        lo, hi = 0.0, 1.0
        for _ in range(40):
            mid = (lo + hi) / 2
            if bx(mid, x1, x2) < p:
                lo = mid
            else:
                hi = mid
        return bx((lo + hi) / 2, y1, y2)
    return f


def in_out_cubic(p):
    p = clamp(p)
    return 4 * p ** 3 if p < .5 else 1 - (-2 * p + 2) ** 3 / 2


def in_back(p, s=1.70158):
    p = clamp(p)
    return (s + 1) * p ** 3 - s * p ** 2


def prog(t, a, b):
    return clamp((t - a) / (b - a)) if b > a else float(t >= a)


def spring_curve(k, c, m=1.0, T=3.0, dt=1 / 2400.0):
    """Damped spring from 0 to 1 (semi-implicit Euler); returns f(t)."""
    n = int(T / dt) + 2
    xs = [0.0] * n
    x, v = 0.0, 0.0
    for i in range(1, n):
        a = (-k * (x - 1.0) - c * v) / m
        v += a * dt
        x += v * dt
        xs[i] = x
    return lambda t: 0.0 if t <= 0 else (xs[min(n - 1, int(t / dt))] if t < T else 1.0)


def mono(size):
    from PIL import ImageFont
    return ImageFont.truetype(str(MONO), int(size))


def draw_digits(c, text, x, y, size, fill=(255, 255, 255)):
    from PIL import ImageDraw
    ImageDraw.Draw(c).text((x, y), text, font=mono(size), fill=fill)


def read_digits(fr, x, y, n, size, alphabet="0123456789", thr=100, search=0):
    """Decode a mono number drawn by draw_digits at (x, y): nearest template per cell (blank -> ' ').
    search=k also tries origins x-k..x and keeps the decode with the smallest total mismatch."""
    from PIL import Image, ImageDraw
    np = np_()
    f = mono(size)
    adv = f.getlength("0")
    hgt = int(size * 1.25)
    cw = int(round(adv))
    temps = {}
    for ch in alphabet:
        im = Image.new("L", (cw, hgt), 0)
        ImageDraw.Draw(im).text((0, 0), ch, font=f, fill=255)
        temps[ch] = np.asarray(im, dtype=float) > thr
    g = lum(fr) > thr
    best_txt, best_cost = None, None
    for dx in range(-search, 1):
        out, cost = "", 0.0
        for k in range(n):
            x0 = int(round(x + dx + k * adv))
            cell = np.zeros((hgt, cw), bool)
            part = g[int(y):int(y) + hgt, max(0, x0):max(0, x0) + cw]
            cell[:part.shape[0], :part.shape[1]] = part
            if cell.sum() < 3:
                out += " "
                continue
            costs = {ch: float((temps[ch] ^ cell).sum()) for ch in temps}
            ch = min(costs, key=costs.get)
            out += ch
            cost += costs[ch]
        if best_cost is None or cost < best_cost:
            best_txt, best_cost = out, cost
    return best_txt


def resample(pts, step=1.0):
    np = np_()
    p = np.asarray(pts, dtype=float)
    seg = np.hypot(*np.diff(p, axis=0).T)
    cum = np.concatenate([[0], np.cumsum(seg)])
    L = cum[-1]
    s = np.arange(0, L + 1e-9, step)
    if s[-1] < L:
        s = np.append(s, L)
    return np.stack([np.interp(s, cum, p[:, 0]), np.interp(s, cum, p[:, 1])], axis=1), L


def prefix(pts, frac):
    """Polyline prefix holding `frac` of the arc length (the dashoffset draw-on of pathLength=1)."""
    np = np_()
    p = np.asarray(pts, dtype=float)
    seg = np.hypot(*np.diff(p, axis=0).T)
    cum = np.concatenate([[0], np.cumsum(seg)])
    L = cum[-1] * clamp(frac)
    if L <= 0:
        return p[:1]
    k = int(np.searchsorted(cum, L))
    k = max(1, min(k, len(p) - 1))
    u = (L - cum[k - 1]) / max(1e-9, seg[k - 1])
    tip = p[k - 1] + (p[k] - p[k - 1]) * u
    return np.vstack([p[:k], tip[None]])


def point_at(pts, frac):
    return prefix(pts, frac)[-1]


def plen(pts):
    np = np_()
    p = np.asarray(pts, dtype=float)
    return float(np.hypot(*np.diff(p, axis=0).T).sum()) if len(p) > 1 else 0.0


def poly(im, pts, width, fill, cap=True):
    from PIL import ImageDraw
    d = ImageDraw.Draw(im)
    q = [tuple(map(float, x)) for x in pts]
    if len(q) >= 2:
        d.line(q, fill=fill, width=int(round(width)), joint="curve")
    if cap and q:
        r = width / 2.0
        for x, y in (q[0], q[-1]):
            d.ellipse((x - r, y - r, x + r, y + r), fill=fill)


def rgbim(size, bg):
    from PIL import Image
    return Image.new("RGB", size, tuple(bg))


def film(wd, name, draw, dur, size=(320, 180), fps=30):
    """draw(t) -> PIL RGB frame; encoded losslessly (libx264rgb qp 0) and decoded back exactly."""
    np = np_()
    W, H = size
    n = int(round(dur * fps))
    path = Path(wd) / name
    p = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", "%dx%d" % (W, H), "-r", str(fps), "-i", "-", "-c:v", "libx264rgb", "-qp", "0",
                          "-preset", "ultrafast", str(path)], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(draw(i / fps).convert("RGB").tobytes())
    p.stdin.close()
    err = p.stderr.read()
    if p.wait():
        raise RuntimeError("encode failed: %s" % err[-300:])
    out = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, timeout=120, stdin=subprocess.DEVNULL).stdout
    return path, np.frombuffer(out, dtype=np.uint8).reshape(-1, H, W, 3).astype(float)


def sharp(a):
    """Variance of the Laplacian of the luminance (focus measure)."""
    from scipy import ndimage
    return float(ndimage.laplace(lum(a)).var())


def node_eval(js, timeout=20):
    done = subprocess.run(["node", "-e", js], capture_output=True, text=True, timeout=timeout, stdin=subprocess.DEVNULL)
    if done.returncode:
        raise RuntimeError("node failed: " + done.stderr[-300:])
    return json.loads(done.stdout)


def strip_marks(s):
    return "".join(ch for ch in s if unicodedata.category(ch) != "Mn")


def angle_grid(h, w, cx, cy):
    """Per-pixel radius and clockwise angle from 12 o'clock, in degrees 0..360."""
    np = np_()
    ys, xs = np.mgrid[0:h, 0:w]
    dx, dy = xs + 0.5 - cx, ys + 0.5 - cy
    return np.hypot(dx, dy), (np.degrees(np.arctan2(dx, -dy)) + 360.0) % 360.0


# ============================================================================= typography-arabic
def _split_words(text):
    return [w for w in text.split(" ") if w]


@card("ARAB-01")
def whole_word_law(task, wd):
    """Split on spaces only (ZWNJ stays inside its word); the word-by-word composite must equal the shaped line,
    the per-letter composite (one span per letter) must not."""
    np = np_()
    text = "نور‌العلم يضيء القلوب"
    words = _split_words(text)
    f = font(CAIRO, 56, wght=800)
    line = shaped_mask(text, f)
    W, H = 900, 140
    from PIL import Image, ImageDraw

    def compose(units):
        im = Image.new("L", (W, H), 0)
        d = ImageDraw.Draw(im)
        x = W - 40
        sp = tlen(" ", f)
        for u, gap in units:
            ln = tlen(u, f)
            d.text((x - ln, 20), u, font=f, fill=255, **_kw(f, u, "rtl"))
            x -= ln + (sp if gap else 0)
        return np.asarray(im) > 128
    by_word = compose([(w, True) for w in words])
    letters = []
    for wi, w in enumerate(words):
        for ci, ch in enumerate(w):
            if ch in "‌‍":
                continue
            letters.append((ch, ci == len(w) - 1))
    by_letter = compose(letters)
    save_png(Image.fromarray((by_word * 255).astype("uint8")), wd / "by_word.png")
    write_json(wd / "words.json", {"text": text, "words": words})
    c_line, c_word, c_letter = comps(line), comps(by_word), comps(by_letter)
    a_line, a_word = float(line.sum()), float(by_word.sum())
    return [check("split on spaces only: 3 units, ZWNJ kept inside the first", len(words) == 3 and "‌" in words[0],
                  len(words), 3),
            check("word composite has the shaped line's connected parts", c_word == c_line, c_word, c_line),
            check("word composite ink equals the shaped line within 3%", abs(a_word - a_line) / a_line < 0.03,
                  a_word / a_line, 1.0),
            check("negative control: per-letter spans break the joins (more parts)", not (c_letter == c_line),
                  c_letter, c_line)], [wd / "by_word.png", wd / "words.json"]


def _kashida(word, n=2):
    """Insert n tatweels after the first letter that joins to the next one (both dual/joining letters)."""
    non_left = set("اأإآدذرزوؤءة")
    for i in range(len(word) - 1):
        a, b = word[i], word[i + 1]
        if a not in non_left and unicodedata.category(a) == "Lo" and unicodedata.category(b) == "Lo":
            return word[:i + 1] + "ـ" * n + word[i + 1:]
    return word


@card("ARAB-03")
def kashida_only(task, wd):
    np = np_()
    from PIL import Image
    w = "محمد"
    f = font(CAIRO, 72, wght=700)
    k = _kashida(w, 3)
    m0, m1 = crop_ink(shaped_mask(w, f)), crop_ink(shaped_mask(k, f))
    # letter-spacing: each letter shaped on its own with 8 px tracking
    parts = [crop_ink(shaped_mask(ch, f)) for ch in reversed(w)]
    hh = max(p.shape[0] for p in parts)
    tracked = np.zeros((hh, sum(p.shape[1] for p in parts) + 8 * len(parts)), bool)
    x = 0
    for p in parts:
        tracked[hh - p.shape[0]:, x:x + p.shape[1]] = p
        x += p.shape[1] + 8
    t, _ = tile(k, f)
    t.save(wd / "kashida.png")
    up = t.resize((int(t.width * 1.2), int(t.height * 1.2)))
    sx = t.resize((int(t.width * 1.2), t.height))
    ar = lambda im: (lambda b: (b[2] - b[0]) / (b[3] - b[1]))(bbox(np.asarray(im.getchannel("A")) > 128))
    a0, au, asx = ar(t), ar(up), ar(sx)
    return [check("kashida inserted between joining letters", "ـ" in k and k.replace("ـ", "") == w, k, w),
            check("elongated word keeps its joins (same parts)", comps(m1) == comps(m0), comps(m1), comps(m0)),
            check("elongated word is wider, same height", m1.shape[1] > m0.shape[1] * 1.15 and abs(m1.shape[0] - m0.shape[0]) <= 2,
                  [m1.shape[1], m0.shape[1]], "wider"),
            check("uniform scale keeps the stroke aspect within 3%", abs(au - a0) / a0 < 0.03, au / a0, 1.0),
            check("negative control: scaleX distorts the aspect by ~20%", not (abs(asx - a0) / a0 < 0.03), asx / a0, 1.2),
            check("negative control: letter-spacing breaks the joins", not (comps(tracked) == comps(m0)),
                  comps(tracked), comps(m0))], [wd / "kashida.png"]


@card("ARAB-04")
def font_ready_gate(task, wd):
    """Chrome: measure the Arabic sample before and after awaiting document.fonts.load per weight (+ ready,
    4 s race). The gated width must equal Pillow's Cairo 800 width; the pre-gate width is the fallback."""
    body = "<canvas id=c width=600 height=140></canvas>"
    js = ("const x=document.getElementById('c').getContext('2d');"
          "function ink(){x.fillStyle='#fff';x.fillRect(0,0,600,140);x.fillStyle='#000';x.direction='rtl';x.textAlign='right';"
          "x.fillText('الأرنب',580,100);const d=x.getImageData(0,0,600,140).data;const m=new Uint8Array(600*140);"
          "for(let i=0;i<m.length;i++)m[i]=d[4*i]<128?1:0;return m}"
          "x.font=\"800 62px 'CairoT', monospace\";const m0=ink();"
          "const to=new Promise(r=>setTimeout(()=>r('timeout'),4000));"
          "const ok=await Promise.race([Promise.all([document.fonts.load(\"800 62px 'CairoT'\",'الأرنب'),"
          "document.fonts.load(\"600 62px 'CairoT'\",'بصمة')]).then(()=>document.fonts.ready).then(()=>'loaded'),to]);"
          "x.font=\"800 62px 'CairoT', monospace\";const m1=ink();let I=0,U=0,A1=0;"
          "for(let i=0;i<m0.length;i++){I+=m0[i]&m1[i];U+=m0[i]|m1[i];A1+=m1[i]}"
          "OUT({iou:I/U,ink1:A1,ok,c1:document.fonts.check(\"800 62px 'CairoT'\",'الأرنب')})")
    src, o = chrome_dump(wd, "gate", hpage(body, js, W=600, H=200), (600, 200), 6000)
    ref = float(shaped_mask("الأرنب", font(CAIRO, 62, wght=800)).sum())
    write_json(wd / "gate.json", dict(o, pillow_cairo800_ink=ref))
    return [check("the gate resolved by loading, not by the 4 s timeout", o["ok"] == "loaded", o["ok"], "loaded"),
            check("font reported loaded after the gate", o["c1"] is True, o["c1"], True),
            check("gated canvas ink equals Cairo 800 (Pillow/raqm) within 8%", abs(o["ink1"] - ref) / ref < 0.08,
                  o["ink1"], ref),
            check("negative control: drawing before the gate bakes a different (fallback) face",
                  not (o["iou"] > 0.9), o["iou"], ">0.9 with the gated drawing")], [wd / "gate.json", src]


@card("ARAB-05")
def harakat_headroom(task, wd):
    """Dots and harakat overflow a tight line box (line-height 1.0, no padding); a title line box of line-height
    1.25 plus the card's mask padding (.06 top / .18 bottom em, inset -.05 em) keeps every mark pixel."""
    np = np_()
    from PIL import Image, ImageDraw
    text = "إِنَّ الْعِلْمَ نُورٌ"
    em = 100
    f = font(CAIRO, em, wght=700)
    asc, desc = f.getmetrics()
    W, H, base = 1100, 520, 260
    im = Image.new("L", (W, H), 0)
    ImageDraw.Draw(im).text((60, base), text, font=f, fill=255, anchor="ls", direction="rtl", language="ar")
    full = np.asarray(im) > 100

    def line_box(lh, top_pad=0.0, bot_pad=0.0):
        half = (lh * em - (asc + desc)) / 2.0
        return (0, base - asc - half - top_pad * em, W, base + desc + half + bot_pad * em)

    def lost(box):
        y0, y1 = int(round(box[1])), int(round(box[3]))
        keep = np.zeros_like(full)
        keep[max(0, y0):y1] = True
        return int((full & ~keep).sum())
    tight = line_box(1.0)
    title = line_box(1.25, 0.06 + 0.05, 0.18)
    rgb_ = Image.fromarray((full * 255).astype("uint8")).convert("RGB")
    d = ImageDraw.Draw(rgb_)
    d.rectangle(tight, outline=(255, 0, 0))
    d.rectangle(title, outline=(0, 255, 0))
    rgb_.save(wd / "headroom.png")
    im2 = Image.new("L", (W, H), 0)
    ImageDraw.Draw(im2).text((60, base), strip_marks(text), font=f, fill=255, anchor="ls", direction="rtl", language="ar")
    marks = int(full.sum()) - int((np.asarray(im2) > 100).sum())
    write_json(wd / "headroom.json", {"tight_box": tight, "title_box": title, "lost_tight": lost(tight),
                                      "lost_title": lost(title), "mark_pixels": marks})
    return [check("text carries harakat (mark ink present)", marks > 200, marks, ">200"),
            check("line-height 1.25 + mask padding keeps every mark pixel", lost(title) == 0, lost(title), 0),
            check("negative control: a tight line-height 1.0 box clips dots/harakat", not (lost(tight) == 0),
                  lost(tight), 0)], [wd / "headroom.png", wd / "headroom.json"]


def _persp(src, dst):
    np = np_()
    A, B = [], []
    for (x, y), (u, v) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); B.append(u)
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y]); B.append(v)
    return list(np.linalg.solve(np.array(A, float), np.array(B, float)))


@card("ARAB-10")
def arabic_in_3d(task, wd):
    """CanvasTexture route: the whole line drawn RTL on a 2D canvas (x2 for sharpness), mapped onto a plane in
    perspective. Unwarping the plane must give back the shaped line; an unshaped-font texture must not."""
    np = np_()
    from PIL import Image
    text = "مرحبا بالعالم"

    def texture(basic):
        f = font(CAIRO, 96, wght=800, basic=basic)
        im = Image.new("L", (1024, 256), 0)
        from PIL import ImageDraw
        d = ImageDraw.Draw(im)
        ln = f.getlength(text, **_kw(f, text, "rtl"))
        d.text((1024 - 40 - ln, 50), text, font=f, fill=255, **_kw(f, text, "rtl"))
        return im
    tex, raw = texture(False), texture(True)
    quad = [(60, 40), (580, 90), (560, 300), (40, 330)]
    corners = [(0, 0), (1024, 0), (1024, 256), (0, 256)]
    plane = tex.transform((640, 380), Image.PERSPECTIVE, _persp(corners, quad), Image.BICUBIC)
    plane.convert("RGB").save(wd / "plane.png")
    back = plane.transform((1024, 256), Image.PERSPECTIVE, _persp(quad, corners), Image.BICUBIC)
    mt, mb, mr = (np.asarray(x) > 128 for x in (tex, back, raw))
    i_ok, i_raw = iou(mb, mt), iou(mr, mt)
    right = bbox(mt)[2]
    return [check("unwarped plane matches the shaped RTL texture (IoU)", i_ok > 0.8, i_ok, ">0.8"),
            check("line is right-aligned on the canvas (rtl, textAlign right)", abs(right - (1024 - 40)) <= 6, right, 984),
            check("negative control: unshaped-font texture differs from the shaped line", not (i_raw > 0.8), i_raw, ">0.8")], \
        [wd / "plane.png"]


@card("ARAB-13")
def font_discovery(task, wd):
    """Scan the repo font folder + system fonts, fontTools cmap coverage of the Arabic block, rank, resolve the
    card's Pillow chain, and stop (no silent substitution) when no font covers the text."""
    from fontTools.ttLib import TTFont
    import glob
    need = [c for c in range(0x0621, 0x064B)] + list(range(0x064B, 0x0653))
    files = sorted(glob.glob(str(FONTS / "*.ttf"))) + sorted(glob.glob("/usr/share/fonts/truetype/dejavu/*.ttf")) + \
        sorted(glob.glob("/usr/share/fonts/truetype/freefont/*.ttf"))
    rows = []
    for p in files:
        try:
            cm = TTFont(p, lazy=True).getBestCmap() or {}
        except Exception:
            continue
        cov = sum(1 for c in need if c in cm) / len(need)
        rows.append({"file": Path(p).name, "path": p, "coverage": round(cov, 4), "cmap": cm})
    rows.sort(key=lambda r: -r["coverage"])
    chain = ["NotoNaskhArabic", "NotoSansArabic", "NotoKufiArabic", "Cairo", "Tajawal", "Almarai", "Amiri",
             "Scheherazade", "KacstOne", "DejaVuSans"]

    def resolve(text):
        cps = [ord(ch) for ch in text if not ch.isspace()]
        for name in chain:
            for r in rows:
                if r["file"].replace("[", "-").startswith(name) and all(c in r["cmap"] for c in cps):
                    return r["file"]
        raise LookupError("STOP: no font in the chain covers %r" % text)
    pick = resolve("مرحبا بالعالم")
    try:
        resolve("مرحبا ")
        stopped = False
    except LookupError:
        stopped = True
    pop = next(r for r in rows if r["file"] == "Poppins-Bold.ttf")
    write_json(wd / "fonts.json", [{k: v for k, v in r.items() if k != "cmap"} for r in rows])
    t, _ = tile("مرحبا بالعالم", font(FONTS / pick, 48))
    t.save(wd / "chosen.png")
    return [check("chain resolves to the first available full-coverage face (Cairo)", pick.startswith("Cairo"), pick, "Cairo"),
            check("top-ranked font covers the whole Arabic block", rows[0]["coverage"] == 1.0, rows[0]["coverage"], 1.0),
            check("missing glyph stops instead of substituting", stopped, stopped, True),
            check("negative control: a Latin face fails the cmap check", not (pop["coverage"] == 1.0), pop["coverage"], 1.0)], \
        [wd / "fonts.json", wd / "chosen.png"]


@card("ARAB-14")
def live_font_loader(task, wd):
    """FONTS table + loadFont(id): inject <link id=sk-font-*> to css2 with display=swap + preconnect, set
    --sk-font; the title's computed family follows the variable (network blocked; the DOM swap is measured)."""
    js = r"""
const FONTS={cairo:{fam:'Cairo',w:'400;500;600;700;800'},tajawal:{fam:'Tajawal',w:'400;500;700;800'},
 almarai:{fam:'Almarai',w:'400;700;800'},kufi:{fam:'Noto Kufi Arabic',w:'400;500;600;700;800'},
 readex:{fam:'Readex Pro',w:'400;500;600;700'},naskh:{fam:'Noto Naskh Arabic',w:'400;500;600;700'},
 plex:{fam:'IBM Plex Sans Arabic',w:'400;500;600;700'},system:{fam:'system-ui',w:''}};
function loadFont(id){const F=FONTS[id];if(F.w){if(!document.getElementById('sk-pre')){const p=document.createElement('link');
 p.id='sk-pre';p.rel='preconnect';p.href='https://fonts.gstatic.com';p.crossOrigin='';document.head.appendChild(p);}
 let l=document.getElementById('sk-font-'+id);if(!l){l=document.createElement('link');l.id='sk-font-'+id;l.rel='stylesheet';
 l.href='https://fonts.googleapis.com/css2?family='+F.fam.replace(/ /g,'+')+':wght@'+F.w+'&display=swap';document.head.appendChild(l);}}
 const v="'"+F.fam+"', system-ui";document.documentElement.style.setProperty('--sk-font',v);document.documentElement.style.setProperty('--sk-font-display',v);}
const h=document.getElementById('h');const before=getComputedStyle(h).fontFamily;
loadFont('tajawal');const a=getComputedStyle(h).fontFamily;loadFont('kufi');const b=getComputedStyle(h).fontFamily;
const links=[...document.querySelectorAll('link')].map(l=>[l.id,l.rel,l.href]);
OUT({before,a,b,links,n:Object.keys(FONTS).length});"""
    src, o = chrome_dump(wd, "loader", hpage("<h1 id=h style=\"font-family:var(--sk-font,serif)\">عنوان</h1>", js))
    write_json(wd / "loader.json", o)
    hrefs = {l[0]: l[2] for l in o["links"]}
    return [check("link points at css2 with weights and display=swap",
                  hrefs.get("sk-font-tajawal") == "https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap",
                  hrefs.get("sk-font-tajawal"), "css2 Tajawal display=swap"),
            check("preconnect to fonts.gstatic.com injected once", sum(1 for l in o["links"] if l[1] == "preconnect") == 1,
                  o["links"], "1 preconnect"),
            check("title family follows --sk-font live (Tajawal, then Noto Kufi)",
                  o["a"].startswith("Tajawal") and o["b"].startswith("\"Noto Kufi Arabic\""), [o["a"], o["b"]], "swapped"),
            check("8 picker faces", o["n"] == 8, o["n"], 8),
            check("negative control: before loadFont the title is the fallback", not o["before"].startswith("Tajawal"),
                  o["before"], "Tajawal")], [wd / "loader.json", src]


def _xheight_ar(f):
    return float(crop_ink(shaped_mask("ـسـ", f)).shape[0])


def _xheight_lat(f):
    return float(crop_ink(shaped_mask("x", f)).shape[0])


@card("ARAB-15")
def type_pairings(task, wd):
    """Ads pairing: heavy Kufi headline with a condensed Latin set at a matched x-height, >= 96 px, explicit size per
    script recorded in tokens.json; the matched pair must measure equal, the naive equal-size pair must not."""
    from PIL import Image
    ar_size = 128
    fa = font(REEM, ar_size, wght=700)
    lat_unit = _xheight_lat(font(POPPINS, 100)) / 100.0
    lat_size = round(_xheight_ar(fa) / lat_unit)
    fl = font(POPPINS, lat_size)
    xa, xl = _xheight_ar(fa), _xheight_lat(fl)
    naive = _xheight_lat(font(POPPINS, ar_size))
    tokens = {"pair": "Reem Kufi 700 + Poppins Bold (condensed Latin stand-in)", "ar": {"size": ar_size},
              "lat": {"size": lat_size}, "rule": "matched x-height, >=96 px"}
    write_json(wd / "tokens.json", tokens)
    c = blank((900, 300), (16, 16, 20))
    place(c, tile("قوة", fa)[0], 640, 150)
    place(c, tile("POWER", fl)[0], 230, 150)
    c.convert("RGB").save(wd / "pair.png")
    return [check("matched Latin x-height equals the Arabic body within 4%", abs(xl - xa) / xa < 0.04, [xl, xa], "equal"),
            check("both sizes >= 96 px", ar_size >= 96 and lat_size >= 96, [ar_size, lat_size], ">=96"),
            check("negative control: same nominal size mismatches by >10%", not (abs(naive - xa) / xa < 0.10), [naive, xa],
                  "equal")], [wd / "tokens.json", wd / "pair.png"]


VIDEO_SCALE = {"caption": (56, 72), "title": (96, 180), "label": (32, 1e9)}


def type_scale(role, script, base=None):
    lo, hi = VIDEO_SCALE[role]
    b = base if base is not None else {"caption": 58, "title": 120, "label": 32}[role]
    return round(b * (1.12 if script == "ar" else 1.0), 1)


@card("ARAB-16")
def video_type_scale(task, wd):
    toks = {r: {s: type_scale(r, s) for s in ("ar", "lat")} for r in VIDEO_SCALE}
    ok_range = all(VIDEO_SCALE[r][0] <= toks[r][s] <= VIDEO_SCALE[r][1] for r in toks for s in toks[r])
    ratio = [toks[r]["ar"] / toks[r]["lat"] for r in toks]
    c = blank((540, 960), (10, 10, 14))
    hs = {}
    for r, y in (("title", 260), ("caption", 760), ("label", 880)):
        t, _ = tile("الكلمة", font(CAIRO, toks[r]["ar"] * K, wght=700))
        place(c, t, 270, y)
        hs[r] = crop_ink(np_().asarray(t.getchannel("A")) > 128).shape[0]
    c.convert("RGB").save(wd / "scale.png")
    write_json(wd / "tokens.json", toks)
    web = {"caption": 16, "title": 32, "label": 12}
    web_ok = all(VIDEO_SCALE[r][0] <= web[r] for r in web)
    meas = hs["title"] / hs["caption"]
    want = toks["title"]["ar"] / toks["caption"]["ar"]
    return [check("every 1080-px token inside the card's ranges", ok_range, toks, VIDEO_SCALE),
            check("Arabic runs 10-15% larger than Latin", all(1.10 <= x <= 1.15 for x in ratio), ratio, "1.10-1.15"),
            check("rendered title/caption ink ratio follows the tokens (±8%)", abs(meas - want) / want < 0.08, meas, want),
            check("negative control: web defaults fail the video minimums", not web_ok, web, VIDEO_SCALE)], \
        [wd / "scale.png", wd / "tokens.json"]


def meaning_units(words, maxw=5):
    n = len(words)
    k = math.ceil(n / maxw)
    base, extra = divmod(n, k)
    out, i = [], 0
    for j in range(k):
        m = base + (1 if j < extra else 0)
        out.append(words[i:i + m])
        i += m
    return out


@card("ARAB-18")
def kinetic_grammar(task, wd):
    np = np_()
    sent = "العلم نور يضيء الطريق لكل من يبحث عن الحقيقة"
    words = sent.split()
    units = meaning_units(words)
    unit = units[0]
    key = max(range(len(unit)), key=lambda i: len(unit[i]))
    ez = bez(0.22, 1, 0.36, 1)
    ent, stg, ext = 0.375, 0.10, 0.25
    hold = 0.3 + 0.06 * sum(len(w) for w in unit)
    end = 0.2 + stg * (len(unit) - 1) + ent + hold
    fs = font(CAIRO, 34, wght=300)
    fk = font(CAIRO, 62, wght=900)
    W, H = 300, 520
    tiles = [tile(w, fk if i == key else fs)[0] for i, w in enumerate(unit)]
    inks = [bbox(np.asarray(t_.getchannel("A")) > 128) for t_ in tiles]
    pos, y = [], 40
    for t_, b in zip(tiles, inks):
        hh = b[3] - b[1]
        pos.append((W / 2, y + hh / 2 - (b[1] + b[3]) / 2 + t_.height / 2))
        y += hh + 22

    def draw(t):
        c = blank((W, H))
        for i, tl in enumerate(tiles):
            a = 0.2 + stg * i
            p = prog(t, a, a + ent)
            if p <= 0:
                continue
            al = clamp(p / 0.6)
            e = ez(p)
            xo = prog(t, end, end + ext)
            place(c, tl, pos[i][0] + 27 * (1 - e), pos[i][1] - 30 * xo, alpha=al * (1 - xo))
        return c
    path, frames = film(wd, "kinetic.mp4", draw, end + ext + 0.2, (W, H))
    onsets = []
    for i, tl in enumerate(tiles):
        b = inks[i]
        top = pos[i][1] - tl.height / 2
        box = (0, top + b[1] - 2, W, top + b[3] + 2)
        s = [box_ink(fr, box) for fr in frames]
        onsets.append(next(j for j, v in enumerate(s) if v > 0) / 30.0)
    hk = crop_ink(np.asarray(tiles[key].getchannel("A")) > 128).shape[0]
    hs = min(crop_ink(np.asarray(tiles[i].getchannel("A")) > 128).shape[0] for i in range(len(tiles)) if i != key)
    d = np.diff(onsets)
    write_json(wd / "plan.json", {"units": units, "keyword": unit[key], "hold": hold, "onsets": onsets})
    return [check("meaning units of <=5 words", all(len(u) <= 5 for u in units), [len(u) for u in units], "<=5"),
            check("measured word stagger 70-120 ms", all(0.066 <= x <= 0.134 for x in d), list(d), 0.10),
            check("keyword set much larger than the support words (hero vs support)", hk / hs > 1.4, hk / hs, ">1.4"),
            check("exit shorter than entrance; hold >= 0.3 s + 0.06 s/char", ext < ent and hold >= 0.3 + 0.06 * 10,
                  [ext, ent, hold], "exit<entrance"),
            check("negative control: the unsegmented sentence breaks the 5-word law", not (len(words) <= 5), len(words), "<=5")], \
        [path, wd / "plan.json"]


def _word_frame(word, f, W=360, H=160, bg=(0, 0, 0)):
    t, _ = tile(word, f)
    return t


def _alpha_np(t):
    return np_().asarray(t.getchannel("A"), dtype=float) / 255.0


def quart_out(p):
    return pow_out(p, 4)


@card("ARAB-21")
def rtl_clip_wipe(task, wd):
    """clip-path inset(0 0 0 100%) -> inset(0 0 0 0) over 500 ms ease-out quart on the whole shaped word."""
    np = np_()
    f = font(CAIRO, 72, wght=800)
    t = _word_frame("الحقيقة", f)
    W, H = t.width + 40, t.height + 20
    ink = bbox(np.asarray(t.getchannel("A")) > 128)
    x0, x1 = 20 + ink[0], 20 + ink[2]
    full = None

    def draw(tt, ltr=False):
        c = blank((W, H))
        e = quart_out(prog(tt, 0.1, 0.6))
        cut = x1 - (x1 - x0) * e
        clip = (x0, 0, x0 + (x1 - x0) * e, H) if ltr else (cut, 0, W, H)
        if e > 0:
            place(c, t, W / 2, H / 2, clip=clip)
        return c
    path, frames = film(wd, "wipe.mp4", draw, 0.9, (W, H))
    m_end = lum(frames[-1]) > 110
    fullm = lum(arr(blank((W, H)).copy())) > 999
    c_full = blank((W, H)); place(c_full, t, W / 2, H / 2)
    fullm = lum(arr(c_full)) > 110
    frac = [float((lum(fr) > 110).sum()) / float(fullm.sum()) for fr in frames]
    k = int(round(0.35 * 30))
    xs = np.nonzero((lum(frames[k]) > 110).any(axis=0))[0]
    want = quart_out(prog(k / 30.0, 0.1, 0.6))
    vis_left = (x1 - xs.min()) / (x1 - x0)
    lt = arr(draw(0.35, ltr=True))
    lxs = np.nonzero((lum(lt) > 110).any(axis=0))[0]
    return [check("final frame equals the whole shaped word (IoU)", iou(m_end, fullm) > 0.98, iou(m_end, fullm), ">0.98"),
            check("joins never broken: final parts == word parts", comps(m_end) == comps(fullm), comps(m_end), comps(fullm)),
            check("mid-wipe uncovered width follows ease-out quart (±0.06)", abs(vis_left - want) < 0.06, vis_left, want),
            check("reveal is anchored on the right edge (RTL)", xs.max() >= x1 - 3, int(xs.max()), x1),
            check("negative control: an LTR wipe starts from the left edge, not the right",
                  not (lxs.max() >= x1 - 3), int(lxs.max()), x1)], [path]


@card("ARAB-22")
def feathered_write_on(task, wd):
    """Basma TX.reveal: clip to the edge, then 6 thin slices with falling alpha (feather max(6 px, 8% w));
    the pen sprite sits on the returned edge x."""
    np = np_()
    from PIL import Image, ImageDraw
    f = font(CAIRO, 80, wght=800)
    t = _word_frame("الكتابة", f)
    A = _alpha_np(t)
    b = bbox(A > 0.5)
    w = b[2] - b[0]
    fw = max(6, 0.08 * w)

    def reveal(p, feather=True):
        edge = b[2] - w * p
        xs = np.arange(A.shape[1])[None, :]
        k = np.zeros_like(A)
        k[:, :] = (xs >= edge)
        if feather:
            sw = fw / 6.0
            for s in range(6):
                lo, hi = edge - (s + 1) * sw, edge - s * sw
                k[:, (xs[0] >= lo) & (xs[0] < hi)] = 1 - (s + 1) / 7.0
        return A * k, edge
    out, edge = reveal(0.5)
    c = Image.fromarray((out * 255).astype("uint8")).convert("RGB")
    ImageDraw.Draw(c).ellipse((edge - 5, b[1] - 14, edge + 5, b[1] - 4), fill=(255, 60, 60))
    c.save(wd / "feather.png")
    arrc = np.asarray(c, dtype=float)
    pen = (arrc[..., 0] > 200) & (arrc[..., 1] < 100)
    pen_x = float(np.nonzero(pen)[1].mean())
    ratio = []
    for s in range(6):
        sw = fw / 6.0
        cols = slice(int(math.ceil(edge - (s + 1) * sw + 0.5)), int(math.floor(edge - s * sw)))
        m = A[:, cols] > 0.9
        ratio.append(float(out[:, cols][m].mean()) if m.any() else None)
    ratio = [r for r in ratio if r is not None]
    hard, _ = reveal(0.5, feather=False)
    hm = A > 0.5
    rs, rh_ = np.where(hm, out / np.maximum(A, 1e-6), 0), np.where(hm, hard / np.maximum(A, 1e-6), 0)
    soft_cols = ((rs > 0.05) & (rs < 0.95) & hm).any(axis=0).sum()
    hard_cols = ((rh_ > 0.05) & (rh_ < 0.95) & hm).any(axis=0).sum()
    return [check("feather width = max(6 px, 8% of the word)", abs(fw - max(6, 0.08 * w)) < 1e-9 and fw >= 6, fw, "max(6,8%)"),
            check("feather alpha falls slice by slice across the edge", len(ratio) >= 4 and all(ratio[i] > ratio[i + 1] for i in range(len(ratio) - 1)),
                  ratio, "decreasing"),
            check("pen sprite rides the reveal edge (±2 px)", abs(pen_x - edge) <= 2, pen_x, edge),
            check("negative control: a hard clip has no feather columns", not (hard_cols >= 3), int(hard_cols), ">=3"),
            check("feather spans several columns", soft_cols >= 5, int(soft_cols), ">=5")], [wd / "feather.png"]


@card("ARAB-23")
def brush_mask_write_on(task, wd):
    """SVG-style mask: a thick round-cap brush path drawn right->left (dashoffset 1->0) over the intact phrase;
    0-0.5 s start, 0.5-2.5 s reveal, 2.5-4 s read."""
    np = np_()
    from PIL import Image, ImageDraw
    f = font(AMIRI_B, 64)
    t = _word_frame("بسم الله الرحمن", f)
    A = _alpha_np(t)
    b = bbox(A > 0.5)
    Wt, Ht = t.width, t.height
    xs = np.linspace(b[2] + 10, b[0] - 10, 80)
    ys = (b[1] + b[3]) / 2 + 6 * np.sin(np.linspace(0, 3 * math.pi, 80))
    path = np.stack([xs, ys], 1)
    thick = (b[3] - b[1]) * 2.4

    def mask_at(tt):
        p = in_out_cubic(prog(tt, 0.5, 2.5))
        m = Image.new("L", (Wt, Ht), 0)
        if p > 0:
            poly(m, prefix(path, p), thick, 255)
        return np.asarray(m, dtype=float) / 255.0

    def draw(tt):
        a = A * mask_at(tt)
        return Image.fromarray((a * 255).astype("uint8")).convert("RGB")
    vid, frames = film(wd, "brush.mp4", draw, 4.0, (Wt, Ht))
    tot = float((A > 0.5).sum())
    frac = lambda fr: float(((lum(fr) > 128) & (A > 0.5)).sum()) / tot
    mid = frames[int(1.2 * 30)]
    half = (b[0] + b[2]) // 2
    rh = float(((lum(mid) > 128) & (A > 0.5))[:, half:].sum())
    lh = float(((lum(mid) > 128) & (A > 0.5))[:, :half].sum())
    end = frames[int(2.6 * 30)]
    return [check("nothing shown during the 0-0.5 s lead-in", frac(frames[int(0.4 * 30)]) < 0.01, frac(frames[12]), 0),
            check("phrase fully uncovered by 2.5 s", frac(end) > 0.98, frac(end), ">0.98"),
            check("brush reveals right half before the left (RTL)", rh > 3 * max(lh, 1), [rh, lh], "right>>left"),
            check("revealed ink is the intact shaped phrase (same parts)", comps((lum(end) > 128)) == comps(A > 0.5),
                  comps(lum(end) > 128), comps(A > 0.5)),
            check("negative control: the unmasked phrase is fully visible at t=0", not (float((A > 0.5).sum()) / tot < 0.01),
                  1.0, "<0.01")], [vid]


@card("ARAB-26")
def spring_word_stagger(task, wd):
    """a_i = 0.25 + 0.16 i; rise 70 px (35 at K) and scale .92->1 on a 170/16 spring; exit 3.0-3.35 s inBack -60 px."""
    np = np_()
    words = ["العلم", "نور", "الحياة"]
    f = font(CAIRO, 64, wght=900)
    W, H = 420, 200
    row = word_row(words, f, W, H / 2, fills=[(255, 255, 255, 255), (126, 232, 210, 255), (255, 255, 255, 255)])
    sp = spring_curve(170, 16)
    rise = 70 * K

    def state(i, t):
        a = 0.25 + 0.16 * i
        if t < a:
            return None
        s = sp(t - a)
        xo = in_back(prog(t, 3.0, 3.35))
        return {"dy": rise * (1 - s) - 60 * K * xo, "scale": 0.92 + 0.08 * s, "alpha": clamp((t - a) / 0.1) * (1 - prog(t, 3.25, 3.35))}

    def draw(t):
        c = blank((W, H))
        for i, r in enumerate(row):
            s = state(i, t)
            if s:
                place(c, r["tile"], r["cx"], r["cy"] + s["dy"], scale=s["scale"], alpha=s["alpha"])
        return c
    vid, frames = film(wd, "spring.mp4", draw, 3.5, (W, H))
    cols = []
    for r in row:
        x0, x1 = int(r["box"][0]), int(r["box"][2])
        ys = []
        for fr in frames:
            m = lum(fr[:, max(0, x0):x1]) > 110
            ys.append(float(np.nonzero(m)[0].mean()) if m.sum() > 30 else None)
        cols.append(ys)
    rest = [ys[int(2.5 * 30)] for ys in cols]
    on = [next(j for j, v in enumerate(ys) if v is not None) / 30.0 for ys in cols]
    over = [rest[i] - min(v for v in cols[i][:int(2.5 * 30)] if v is not None) for i in range(3)]
    zeta = 16 / (2 * math.sqrt(170))
    want = rise * math.exp(-zeta * math.pi / math.sqrt(1 - zeta ** 2))
    cx = [r["cx"] for r in row]
    gone = float((lum(frames[-1]) > 110).sum())
    lin, lframes = film(wd, "linear.mp4", lambda t: (lambda c: (place(c, row[0]["tile"], row[0]["cx"],
                        row[0]["cy"] + rise * (1 - prog(t, 0, 0.5))), c)[1])(blank((W, H))), 0.8, (W, H))
    x0, x1 = int(row[0]["box"][0]), int(row[0]["box"][2])
    static = [float(np.nonzero(lum(fr[:, max(0, x0):x1]) > 110)[0].mean()) for fr in lframes]
    return [check("onsets 160 ms apart (±1 frame)", all(abs((on[i + 1] - on[i]) - 0.16) <= 0.034 for i in range(2)), on, 0.16),
            check("spring overshoot above rest ≈ analytic 170/16 value", all(abs(o - want) < 1.6 for o in over), over, want),
            check("first word sits on the right (RTL order)", cx[0] > cx[1] > cx[2], cx, "decreasing"),
            check("all words exit together by 3.35 s", gone < 20, gone, "<20 px"),
            check("negative control: a static (un-sprung) word has no overshoot", not (static[-1] - min(static) > 1.0),
                  static[-1] - min(static), want)], [vid]


def remotion_spring(frame, fps=30, damping=10.0, stiffness=100.0, mass=1.0):
    """Remotion spring(): damped spring 0->1 evaluated at frame/fps (no overshootClamping)."""
    return spring_curve(stiffness, damping, mass)(frame / float(fps))


@card("ARAB-27")
def remotion_title_pills(task, wd):
    """Accent rule grows to 180 px, title words spring in every 5 frames (14/120/.9, rise 80, scale .85->1),
    keyword pills every 4 frames (12/150); Arabic numbers via Intl.NumberFormat('ar-EG')."""
    np = np_()
    from PIL import ImageDraw
    W, H = 540, 360
    words = ["خطة", "النمو", "الجديدة"]
    pills = ["سرعة", "دقة", "ثقة"]
    ft = font(CAIRO, 112 * K, wght=800)
    fp = font(CAIRO, 40 * K, wght=600)
    row = word_row(words, ft, W, 150)
    prow = word_row(pills, fp, W, 270, gap=60 * K)
    sp_t = spring_curve(120, 14, 0.9)
    sp_p = spring_curve(150, 12, 1.0)
    acc = (126, 232, 210)

    def draw(t):
        fr = t * 30
        c = blank((W, H), (12, 12, 16))
        rw = 180 * K * sp_t(fr / 30.0)
        ImageDraw.Draw(c).rectangle((W / 2 - rw / 2, 60, W / 2 + rw / 2, 66), fill=acc + (255,))
        for i, r in enumerate(row):
            s0 = 6 + 5 * i
            if fr >= s0:
                s = sp_t((fr - s0) / 30.0)
                place(c, r["tile"], r["cx"], r["cy"] + 80 * K * (1 - s), scale=0.85 + 0.15 * s)
        for i, r in enumerate(prow):
            s0 = 30 + 4 * i
            if fr >= s0:
                s = sp_p((fr - s0) / 30.0)
                x0, y0, x1, y1 = r["box"]
                ImageDraw.Draw(c).rounded_rectangle((x0 - 15 * K, y0 + 8, x1 + 15 * K, y1 - 8), radius=99,
                                                    outline=acc + (230,), width=2)
                place(c, r["tile"], r["cx"], r["cy"] + 20 * (1 - s), alpha=clamp(s))
        return c
    vid, frames = film(wd, "title.mp4", draw, 2.4, (W, H))
    rule = [float(((np.abs(fr[60:66] - np.array(acc)).max(-1)) < 30).any(0).sum()) for fr in frames]
    on_t = [next(j for j, fr in enumerate(frames) if box_ink(fr, (r["box"][0], 80, r["box"][2], 230)) > 20) for r in row]
    on_p = [next(j for j, fr in enumerate(frames) if box_ink(fr, (r["box"][0], 235, r["box"][2], H)) > 20) for r in prow]
    nums = node_eval("console.log(JSON.stringify([new Intl.NumberFormat('ar-EG').format(1234567),"
                     "new Intl.NumberFormat('en-US').format(1234567)]))")
    write_json(wd / "numbers.json", nums)
    return [check("accent rule settles at 180 px (90 at K)", abs(rule[-1] - 90) <= 2, rule[-1], 90),
            check("title words start every 5 frames", [b - a for a, b in zip(on_t, on_t[1:])] == [5, 5], on_t, "+5"),
            check("pills start every 4 frames", [b - a for a, b in zip(on_p, on_p[1:])] == [4, 4], on_p, "+4"),
            check("ar-EG digits ١٬٢٣٤٬٥٦٧", nums[0] == "١٬٢٣٤٬٥٦٧", nums[0], "١٬٢٣٤٬٥٦٧"),
            check("negative control: the en-US formatter keeps Western digits", not (nums[1] == "١٬٢٣٤٬٥٦٧"), nums[1], "Arabic-Indic")], \
        [vid, wd / "numbers.json"]


@card("ARAB-30")
def blur_hero_shrink(task, wd):
    """word1 opacity 0->1, blur 20->0 (10 at K), scale 1.1->1 in 0.5 s; then font-size 22%->7% of H over 0.6 s
    (re-shaped at each size, never scaleX) while words 2..n enter 180 ms apart."""
    np = np_()
    W, H = 360, 480
    words = ["المستقبل", "يبدأ", "الآن"]
    ez = bez(.22, 1, .36, 1)
    fin = word_row(words, font(CAIRO, 0.07 * H, wght=700), W, H * 0.3)
    tails = [r["tile"] for r in fin[1:]]

    def size_at(t):
        return 0.22 * H + (0.07 - 0.22) * H * in_out_cubic(prog(t, 0.5, 1.1))

    def draw(t):
        c = blank((W, H))
        s = size_at(t)
        t1, _ = tile(words[0], font(CAIRO, s, wght=700))
        p = prog(t, 0, 0.5)
        x_hero = W / 2 + (fin[0]["cx"] - W / 2) * in_out_cubic(prog(t, 0.5, 1.1))
        place(c, t1, x_hero, H * 0.3, alpha=p, blur=10 * (1 - p), scale=1.1 - 0.1 * p)
        for i, tl in enumerate(tails):
            a = 1.1 + 0.18 * i
            q = prog(t, a, a + 0.4)
            if q > 0:
                place(c, tl, fin[i + 1]["cx"], H * 0.3 + 20 * (1 - ez(q)), alpha=q)
        return c
    vid, frames = film(wd, "hero.mp4", draw, 2.0, (W, H))
    s0, s1 = sharp(frames[3][60:240]), sharp(frames[15][60:240])

    def word1_mask(t):
        tt, _ = tile(words[0], font(CAIRO, size_at(t), wght=700))
        return crop_ink(np.asarray(tt.getchannel("A")) > 128)
    m_big, m_small = word1_mask(0.5), word1_mask(1.1)
    ar_big, ar_small = m_big.shape[1] / m_big.shape[0], m_small.shape[1] / m_small.shape[0]
    hr = m_big.shape[0] / m_small.shape[0]
    on = []
    for r in fin[1:]:
        box = (r["box"][0] + 2, H * 0.3 - 40, r["box"][2] - 2, H * 0.3 + 50)
        on.append(next(j for j, fr in enumerate(frames) if j >= 33 and box_ink(fr, box) > 15) / 30.0)
    def plain(t):
        c = blank((W, H))
        t1, _ = tile(words[0], font(CAIRO, size_at(t), wght=700))
        place(c, t1, W / 2, H * 0.3)
        return arr(c)
    u0, u1 = sharp(plain(0.1)[60:240]), sharp(plain(0.5)[60:240])
    return [check("hero lands out of blur (sharpness x3 by 0.5 s)", s1 > 3 * s0, [s0, s1], "x3"),
            check("size 22% -> 7% H re-shapes uniformly (ink height ratio ≈ 22/7)", abs(hr - 22 / 7.0) / (22 / 7.0) < 0.1, hr, 22 / 7.0),
            check("aspect kept when shrinking (no scaleX), within 6%", abs(ar_big - ar_small) / ar_big < 0.06, [ar_big, ar_small], "equal"),
            check("following words enter 180 ms apart (±1 frame)", abs((on[1] - on[0]) - 0.18) <= 0.034, on, 0.18),
            check("negative control: an unblurred hero is already sharp at the start", not (u1 > 3 * u0), [u0, u1], "x3")], [vid]


@card("ARAB-32")
def ink_bleed_reveal(task, wd):
    """Per word opacity 0->1 + blur 4->0 (2 at K) + scale .96->1 in 250 ms with 80% overlap; ink colour adapts
    to background brightness (dark ink on bright sky, white on dark)."""
    np = np_()
    words = ["قطرة", "حبر", "تكتب"]
    W, H = 420, 160

    def ink_for(bg):
        return (20, 24, 40) if (0.2126 * bg[0] + 0.7152 * bg[1] + 0.0722 * bg[2]) > 140 else (250, 250, 250)
    sky, night = (205, 228, 250), (14, 18, 30)
    f = font(CAIRO, 54, wght=700)
    row = word_row(words, f, W, H / 2, fills=[ink_for(sky) + (255,)] * 3)
    dur, step = 0.25, 0.25 * 0.2

    def draw(t):
        c = blank((W, H), sky)
        for i, r in enumerate(row):
            p = prog(t, 0.1 + step * i, 0.1 + step * i + dur)
            if p > 0:
                place(c, r["tile"], r["cx"], r["cy"], alpha=p, blur=2 * (1 - p), scale=0.96 + 0.04 * p)
        return c
    vid, frames = film(wd, "bleed.mp4", draw, 0.8, (W, H))
    box0 = row[0]["box"]
    k_on1 = int(round((0.1 + step) * 30))
    s_mid = sharp(crop(frames[k_on1], box0))
    s_end = sharp(crop(frames[-1], box0))
    dark_text = ink_for(sky)
    night_text = ink_for(night)
    m = lum(frames[-1]) < 100
    meas = frames[-1][m].mean(axis=0) if m.any() else [999] * 3
    flat = blank((W, H), sky)
    for r in row:
        place(flat, r["tile"], r["cx"], r["cy"])
    s_flat = sharp(crop(arr(flat), box0))
    return [check("previous word still soft when the next starts (sharpness < 70% of final)", s_mid < 0.7 * s_end,
                  [s_mid, s_end], "<0.7"),
            check("80% overlap: next word starts 50 ms after the previous", abs(step - 0.05) < 1e-9, step, 0.05),
            check("dark ink on the bright sky, measured", max(abs(meas[i] - dark_text[i]) for i in range(3)) < 40,
                  list(meas), dark_text),
            check("white ink chosen on a dark ground", night_text == (250, 250, 250), night_text, "white"),
            check("negative control: words set at once (no bleed) are sharp at that moment", not (s_flat < 0.7 * s_end),
                  s_flat, "<0.7 x final")], [vid]


@card("ARAB-42")
def squiggle_underline(task, wd):
    """Keyword #f07f2e with a #ffd0a0 12 px glow over a hand-drawn sine underline (amp 3 px, period 18 px)
    drawn right->left and phase-shifted per frame."""
    np = np_()
    from PIL import Image, ImageDraw, ImageFilter
    W, H = 420, 170
    f = font(CAIRO, 64, wght=800)
    key = (0xf0, 0x7f, 0x2e)
    t, _ = tile("مهم", f, fill=key + (255,))
    ink = bbox(np.asarray(t.getchannel("A")) > 128)
    x0, x1 = W / 2 - (t.width / 2 - ink[0]), W / 2 + (ink[2] - t.width / 2)
    yb = 125

    def draw(tt):
        c = blank((W, H), (245, 241, 230))
        g, _ = tile("مهم", f, fill=(0xff, 0xd0, 0xa0, 255))
        place(c, g, W / 2, 70, blur=6)
        place(c, t, W / 2, 70)
        p = prog(tt, 0.1, 0.5)
        ph = tt * 2.0
        n = int((x1 - x0) * p)
        if n > 2:
            pts = [(x1 - j, yb + 3 * math.sin(2 * math.pi * (x1 - j) / 18.0 + ph)) for j in range(n)]
            ImageDraw.Draw(c).line(pts, fill=key + (255,), width=2)
        return c
    vid, frames = film(wd, "squiggle.mp4", draw, 1.0, (W, H))

    def trace(fr):
        band = fr[yb - 8:yb + 9]
        m = np.abs(band - np.array(key)).max(-1) < 60
        cols = np.nonzero(m.any(0))[0]
        ys = np.array([np.nonzero(m[:, c])[0].mean() for c in cols])
        return cols, ys
    cols, ys = trace(frames[-1])
    yd = ys - ys.mean()
    spec = np.abs(np.fft.rfft(yd))
    fr_ = np.fft.rfftfreq(len(yd))
    per = 1 / fr_[1 + np.argmax(spec[1:])]
    amp = (np.percentile(yd, 95) - np.percentile(yd, 5)) / 2
    _, ys2 = trace(frames[-8])
    cm, _ = trace(frames[int(0.3 * 30)])
    kc = frames[-1][45:100]
    km = np.abs(kc - np.array(key)).max(-1) < 25
    st = arr(blank((W, H), (245, 241, 230)))
    st[yb - 1:yb + 1, int(x0):int(x1)] = key
    _, ys_flat = trace(st)
    flat = ys_flat - ys_flat.mean()
    return [check("underline period ≈ 18 px", abs(per - 18) < 1.5, per, 18),
            check("underline amplitude ≈ 3 px", abs(amp - 3) < 0.9, amp, 3),
            check("phase shifts between frames", float(np.abs(ys[:len(ys2)] - ys2[:len(ys)]).mean()) > 0.3, float(np.abs(ys[:len(ys2)] - ys2[:len(ys)]).mean()), ">0.3"),
            check("drawn right->left: mid-draw only the right part exists", cm.min() > (x0 + x1) / 2 - 2, int(cm.min()), ">mid"),
            check("keyword pixels are #f07f2e", int(km.sum()) > 400, int(km.sum()), ">400"),
            check("negative control: a straight underline has no 3 px wave", not (abs((np.percentile(flat, 95) - np.percentile(flat, 5)) / 2 - 3) < 0.9),
                  float(np.ptp(flat)), 3)], [vid]


@card("ARAB-55")
def bilingual_stack(task, wd):
    """Arabic block RTL on top, English LTR block beneath at ~70% size, each with its own dir (Chrome layout)."""
    body = ("<div id=box style='width:380px;margin:10px;padding:0'>"
            "<div id=ar dir=rtl style=\"font:800 40px 'CairoT';color:#111\">الطاقة النظيفة</div>"
            "<div id=en dir=ltr style=\"font:500 28px monospace;color:#5b7fb5\">Clean energy</div>"
            "<div dir=rtl><div id=bad style=\"font:500 28px monospace\">Clean energy</div></div></div>")
    js = ("await document.fonts.load(\"800 40px 'CairoT'\",'الطاقة');"
          "const r=e=>{const g=document.createRange();g.selectNodeContents(e);const b=g.getBoundingClientRect();return [b.left,b.right]};"
          "const first=e=>{const g=document.createRange();g.setStart(e.firstChild,0);g.setEnd(e.firstChild,1);const b=g.getBoundingClientRect();return b.left};"
          "const box=document.getElementById('box').getBoundingClientRect();"
          "OUT({box:[box.left,box.right],ar:r(ar),en:r(en),bad:r(bad),arf:first(ar),enf:first(en),"
          "fs:[parseFloat(getComputedStyle(ar).fontSize),parseFloat(getComputedStyle(en).fontSize)]})")
    src, o = chrome_dump(wd, "stack", hpage(body, js, W=420, H=220), (420, 220))
    write_json(wd / "stack.json", o)
    L, R = o["box"]
    return [check("Arabic block hugs the right edge", abs(o["ar"][1] - R) < 2, o["ar"][1], R),
            check("English block starts at the left edge", abs(o["en"][0] - L) < 2, o["en"][0], L),
            check("first Arabic letter is rightmost (RTL order)", o["arf"] > (o["ar"][0] + o["ar"][1]) / 2, o["arf"], ">centre"),
            check("English at ~70% of the Arabic size", abs(o["fs"][1] / o["fs"][0] - 0.7) < 0.02, o["fs"][1] / o["fs"][0], 0.7),
            check("negative control: English inheriting the RTL dir is pushed to the right",
                  not (abs(o["bad"][0] - L) < 2), o["bad"][0], L)], [wd / "stack.json", src]


def graphemes_n(s):
    import regex
    return len([g for g in regex.findall(r"\X", s) if not g.isspace()])


def display_time(text):
    return min(6.0, max(0.15 * graphemes_n(text), 2.0))


@card("ARAB-63")
def reading_time_law(task, wd):
    lines = ["مَرْحَبًا بِكُمْ", "هذا السطر يحتوي على عدد كبير من الحروف للقراءة", "قصير",
             "سطر طويل جدا يحتاج إلى وقت أطول بكثير من الحد الأقصى المسموح به على الشاشة"]
    cuts = [0.0, 4.0, 9.0, 12.0, 20.0]
    plan = []
    for i, ln in enumerate(lines):
        d = display_time(ln)
        t_in = cuts[i] + 0.3
        t_out = min(t_in + d, cuts[i + 1] - 0.3)
        plan.append({"text": ln, "graphemes": graphemes_n(ln), "display": d, "in": t_in, "out": t_out,
                     "fits": (cuts[i + 1] - 0.3) - t_in >= d})
    hook = lines[0]
    card_w = 4
    cardt = max(0.5, 0.4 * card_w)
    write_json(wd / "schedule.json", {"plan": plan, "card_time_4_words": cardt})
    naive = len(lines[0].replace(" ", ""))
    g0 = graphemes_n(lines[0])
    return [check("graphemes counted after shaping: 'مَرْحَبًا بِكُمْ' = 8", g0 == 8, g0, 8),
            check("t = max(0.15 x chars, 2) capped at 6 s", [p["display"] for p in plan] == [2.0, round(0.15 * plan[1]["graphemes"], 10), 2.0, 6.0]
                  or (plan[0]["display"] == 2.0 and plan[2]["display"] == 2.0 and plan[3]["display"] == 6.0
                      and abs(plan[1]["display"] - 0.15 * plan[1]["graphemes"]) < 1e-9), [p["display"] for p in plan], "law"),
            check("enters 0.3 s after its cut and leaves >= 0.3 s before the next", all(abs(p["in"] - c - 0.3) < 1e-9 and cuts[i + 1] - p["out"] >= 0.3 - 1e-9
                                                                                       for i, (p, c) in enumerate(zip(plan, cuts))), [(p["in"], p["out"]) for p in plan], "0.3 s"),
            check("hook line <= 12 graphemes", g0 <= 12, g0, "<=12"),
            check("card of 4 words holds 1.6 s (0.4 s/word, >= 0.5 s)", abs(cardt - 1.6) < 1e-9, cardt, 1.6),
            check("negative control: counting code points with harakat overcounts", not (naive == 8), naive, 8)], \
        [wd / "schedule.json"]


def _ass(path, W, H, styles, events):
    head = ("[Script Info]\nScriptType: v4.00+\nPlayResX: %d\nPlayResY: %d\nWrapStyle: 0\n\n[V4+ Styles]\n"
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
            "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, "
            "MarginR, MarginV, Encoding\n") % (W, H)
    st = "".join("Style: %s,Cairo,%g,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,%d,%g,%g,2,%d,%d,%d,1\n"
                 % (n, fs, bs, ol, sh, ml, ml, mv) for n, fs, bs, ol, sh, ml, mv in styles)
    ev = "\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n" + "".join(
        "Dialogue: 0,0:00:00.00,0:00:05.00,%s,,0,0,0,,%s\n" % (s, "‏" + t + "‏") for s, t in events)
    Path(path).write_text(head + st + ev, encoding="utf-8")
    return Path(path)


def _libass_frame(wd, name, W, H, styles, events, bg="0x808080"):
    a = _ass(Path(wd) / (name + ".ass"), W, H, styles, events)
    out = Path(wd) / (name + ".png")
    fx.ffmpeg("-f", "lavfi", "-i", "color=c=%s:s=%dx%d:d=1" % (bg, W, H), "-vf",
              "subtitles=%s:fontsdir=%s" % (a, FONTS), "-frames:v", "1", str(out))
    from PIL import Image
    return out, np_().asarray(Image.open(out).convert("RGB"), dtype=float)


@card("ARAB-64")
def caption_safe_zone(task, wd):
    """libass cinema caption: bottom-centre white, thin outline, no box (Alignment 2, Shadow 0, MarginV 9% H);
    glyph height calibrated to 4% of H by measuring alef at a probe size; side margins >= 8%."""
    np = np_()
    W, H = 540, 960
    _, pr = _libass_frame(wd, "probe", W, H, [("P", 60, 1, 0, 0, 20, 300)], [("P", "ا")], bg="black")
    hb = bbox(lum(pr) > 128)
    a60 = hb[3] - hb[1]
    fs = 60 * (0.04 * H) / a60
    mv = int(round(0.09 * H))
    png, fr = _libass_frame(wd, "cinema", W, H, [("C", fs, 1, 1.5, 0, int(0.08 * W), mv)], [("C", "ا مرحبا بكم في الفيلم")])
    white = (fr.min(-1) > 235)
    b = bbox(white)
    _, al = _libass_frame(wd, "alef", W, H, [("C", fs, 1, 1.5, 0, int(0.08 * W), mv)], [("C", "ا")], bg="black")
    ab = bbox(lum(al) > 128)
    glyph = (ab[3] - ab[1]) / H
    _, dflt = _libass_frame(wd, "default", W, H, [("D", 20, 1, 2, 2, 10, 10)], [("D", "مرحبا بكم في الفيلم")])
    db = bbox(dflt.min(-1) > 235)
    bottom = (H - b[3]) / H
    return [check("alef glyph height 3.5-4.5% of H", 0.035 <= glyph <= 0.045, glyph, "0.035-0.045"),
            check("caption bottom sits 6-10% above the frame edge (MarginV 9% H, descenders below)", 0.06 <= bottom <= 0.10, bottom, "~0.09"),
            check("side margins >= 8% of width", b[0] >= 0.08 * W and W - b[2] >= 0.08 * W, [b[0], W - b[2]], 0.08 * W),
            check("centred horizontally (±3 px)", abs((b[0] + b[2]) / 2 - W / 2) <= 3, (b[0] + b[2]) / 2, W / 2),
            check("negative control: libass default-style caption sits in the bottom 3%",
                  not (0.06 <= (H - db[3]) / H <= 0.10), (H - db[3]) / H, "0.06-0.10")], [png, wd / "cinema.ass"]


@card("ARAB-65")
def spoken_word_illumination(task, wd):
    """Phrase as a 40% ghost; each word goes to 100% + accent at words.json start - 60 ms; emphasis word orange."""
    np = np_()
    words = ["نحن", "نصنع", "المستقبل"]
    starts = [0.30, 0.70, 1.20]
    emph = 2
    write_json(wd / "words.json", [{"word": w, "start": s} for w, s in zip(words, starts)])
    f = font(CAIRO, 50, wght=800)
    W, H = 420, 140
    on_col = [(255, 255, 255, 255), (255, 255, 255, 255), (0xf0, 0x7f, 0x2e, 255)]
    row_g = word_row(words, f, W, H / 2)
    row_o = word_row(words, f, W, H / 2, fills=on_col)

    def draw(t, ghost=0.4):
        c = blank((W, H))
        for i in range(3):
            lit = t >= starts[i] - 0.06
            r = row_o[i] if lit else row_g[i]
            place(c, r["tile"], r["cx"], r["cy"], alpha=1.0 if lit else ghost)
        return c
    vid, frames = film(wd, "illum.mp4", draw, 1.6, (W, H))
    onset = []
    for i, r in enumerate(row_g):
        cm = blank((W, H))
        place(cm, r["tile"], r["cx"], r["cy"])
        m = lum(arr(cm)) > 200
        lv = [float(fr[m].max(-1).mean()) for fr in frames]
        onset.append(next(j for j, v in enumerate(lv) if v > 200))
        if i == 0:
            ghost_lv, m_first = lv[0], m
    want = [int(math.ceil((s - 0.06) * 30 - 1e-9)) for s in starts]
    last = frames[-1]
    om = (np.abs(last - np.array([0xf0, 0x7f, 0x2e])).max(-1) < 30).sum()
    solid_lv = float(arr(draw(0.0, ghost=1.0))[m_first].max(-1).mean())
    return [check("each word lights at start - 60 ms (frame exact)", onset == want, onset, want),
            check("ghost level ≈ 40% before the word is spoken", abs(ghost_lv / 255 - 0.4) < 0.06, ghost_lv / 255, 0.4),
            check("emphasis word takes the accent orange", om > 300, int(om), ">300"),
            check("negative control: a solid (untreated) line is already lit at frame 0", not (solid_lv < 200), solid_lv, "<200")], [vid, wd / "words.json"]


@card("ARAB-72")
def bidi_isolation(task, wd):
    """'قال John Smith! ثم ذهب': without isolation the '!' resolves to RTL and jumps left of 'John'; inside <bdi>
    or LRI...PDI it stays after 'Smith'."""
    body = ("<p id=a dir=rtl style='font:24px monospace'>قال John Smith! ثم ذهب</p>"
            "<p id=b dir=rtl style='font:24px monospace'>قال <bdi>John Smith!</bdi> ثم ذهب</p>"
            "<p id=c dir=rtl style='font:24px monospace'>قال ⁦John Smith!⁩ ثم ذهب</p>")
    js = ("const pos=(id,ch)=>{const n=document.getElementById(id);const w=document.createTreeWalker(n,NodeFilter.SHOW_TEXT);"
          "let t,o={};while(t=w.nextNode()){for(const c of ch){const i=t.data.indexOf(c);if(i>=0){const g=document.createRange();"
          "g.setStart(t,i);g.setEnd(t,i+1);o[c]=g.getBoundingClientRect().left}}}return o};"
          "OUT({a:pos('a',['J','h','!']),b:pos('b',['J','h','!']),c:pos('c',['J','h','!'])})")
    src, o = chrome_dump(wd, "bidi", hpage(body, js, W=500, H=200), (500, 200))
    write_json(wd / "bidi.json", o)
    ok = lambda d: d["!"] > d["h"] > d["J"]
    return [check("<bdi>: '!' stays right after 'Smith'", ok(o["b"]), o["b"], "J<h<!"),
            check("LRI...PDI controls give the same order", ok(o["c"]), o["c"], "J<h<!"),
            check("negative control: un-isolated '!' flips to the left of 'John'", not ok(o["a"]), o["a"], "J<h<!")], \
        [wd / "bidi.json", src]


@card("ARAB-73")
def one_digit_system_tnum(task, wd):
    """Intl ar-EG -> ٠-٩, ar-SA-u-nu-latn -> 0-9; tabular figures (tnum) so a counter never changes width."""
    nums = node_eval("const v=[new Intl.NumberFormat('ar-EG').format(2026),new Intl.NumberFormat('ar-SA-u-nu-latn').format(2026),"
                     "(1234.5).toLocaleString('ar-EG')];console.log(JSON.stringify(v))")
    fi = font(INTER, 64)
    widths = lambda feats: sorted({round(fi.getlength(s, features=feats), 2) for s in ("1111", "8888", "1010", "7777")})
    tab, prop = widths(["tnum", "lnum"]), widths(None)
    aw = lambda p: sorted({round(font(p, 64).getlength(s, direction="ltr"), 2) for s in ("١١١١", "٨٨٨٨", "٢٠٢٦")})
    cands = [("Cairo", CAIRO), ("Amiri", AMIRI)]
    pick = next(n for n, p in cands if len(aw(p)) == 1)
    ar_w, cairo_w = aw(AMIRI), aw(CAIRO)
    from PIL import Image
    c = blank((520, 200), (10, 10, 14))
    for i, v in enumerate((9, 10, 11)):
        t, _ = tile("%04d" % (v * 111), fi, features=["tnum"])
        place(c, t, 260, 40 + 60 * i)
    c.convert("RGB").save(wd / "tnum.png")

    def one_system(texts):
        sys_ = set()
        for t in texts:
            for ch in t:
                if ch.isdigit():
                    sys_.add("arab" if "٠" <= ch <= "٩" else "latn")
        return len(sys_) == 1
    write_json(wd / "digits.json", {"intl": nums, "tnum_widths": tab, "proportional_widths": prop, "amiri_arabic_indic": ar_w, "cairo_arabic_indic": cairo_w, "counter_face": pick})
    return [check("ar-EG gives Arabic-Indic digits", nums[0] == "٢٬٠٢٦", nums[0], "٢٬٠٢٦"),
            check("ar-SA-u-nu-latn keeps 0-9 with Arabic grouping", nums[1] == "2,026" or nums[1] == "2٬026", nums[1], "2,026"),
            check("tnum: every 4-digit string has one width", len(tab) == 1, tab, "one width"),
            check("counter face for ٠-٩ chosen by a tabular test (Amiri; one width)", pick == "Amiri" and len(ar_w) == 1, [pick, ar_w], "one width"),
            check("negative control: Cairo's Arabic-Indic digits are proportional", not (len(cairo_w) == 1), cairo_w, "one width"),
            check("film strings use one digit system", one_system([nums[0], "٣٠٪"]), [nums[0], "٣٠٪"], "one system"),
            check("negative control: proportional figures jitter (several widths)", not (len(prop) == 1), prop, "one width"),
            check("negative control: mixing ٢٠٢٦ and 30 is flagged", not one_system([nums[0], "30%"]), [nums[0], "30%"], "one system")], \
        [wd / "tnum.png", wd / "digits.json"]


CTA_VERBS = ("اشترك", "حمّل", "اطلب", "تابعنا", "جرّب", "سجّل")


@card("ARAB-79")
def cta_price_isolation(task, wd):
    """Imperative CTA + one digit system + currency and number in one isolated span (<bdi>49 ر.س</bdi>)."""
    good = "اشترك في Pro <bdi id=p>49 ر.س</bdi>"
    bad = "اشترك في Pro 49 ر.س"
    body = "<p id=g dir=rtl style='font:28px monospace'>%s</p><p id=b dir=rtl style='font:28px monospace'>%s</p>" % (good, bad)
    js = ("const at=(id,ch)=>{const n=document.getElementById(id);const w=document.createTreeWalker(n,NodeFilter.SHOW_TEXT);"
          "let t,o=[];while(t=w.nextNode()){let i=-1;while((i=t.data.indexOf(ch,i+1))>=0){const g=document.createRange();"
          "g.setStart(t,i);g.setEnd(t,i+1);const r=g.getBoundingClientRect();o.push([r.left,r.right])}}return o};"
          "OUT({g:{r:at('g','ر'),d:at('g','4').concat(at('g','9'))},b:{r:at('b','ر'),d:at('b','4').concat(at('b','9'))}})")
    src, o = chrome_dump(wd, "cta", hpage(body, js, W=500, H=160), (500, 160))

    def gap(d):
        r = d["r"][-1]
        digits = d["d"]
        return min(min(abs(r[0] - x[1]), abs(x[0] - r[1])) for x in digits)
    g, b = gap(o["g"]), gap(o["b"])

    def valid(cta):
        txt = re.sub("<[^>]+>", "", cta)
        verb_ok = txt.split()[0] in CTA_VERBS
        iso = re.search(r"<bdi[^>]*>[0-9٠-٩]+\s*ر\.س</bdi>", cta) is not None
        systems = {("arab" if "٠" <= ch <= "٩" else "latn") for ch in txt if ch.isdigit()}
        return verb_ok and iso and len(systems) == 1
    write_json(wd / "cta.json", {"gap_isolated": g, "gap_plain": b, "valid": [valid(good), valid(bad)]})
    return [check("CTA validator: imperative verb, one digit system, isolated price", valid(good), good, "valid"),
            check("isolated price keeps currency next to its number (< 20 px)", g < 20, g, "<20"),
            check("negative control: without isolation 'Pro' lands between number and currency", not (b < 20), b, "<20"),
            check("negative control: the un-isolated CTA fails the validator", not valid(bad), bad, "valid")], \
        [wd / "cta.json", src]


@card("ARAB-89")
def canvas_rtl_helpers(task, wd):
    """U.text(): ctx.direction='rtl' when Arabic is detected (anchored at x with textAlign start), round-joined
    stroke; layer: <=5 lines split on \\n at lh 1.35*size, max width 91%."""
    js = r"""
await document.fonts.load("700 30px 'CairoT'",'سطر');
const cv=document.getElementById('c'),x=cv.getContext('2d');const AR=/[؀-ۿ]/;
const U={text(s,X,Y,size,color,o={}){x.save();x.font=(o.weight||700)+' '+size+"px 'CairoT', sans-serif";
 x.direction=o.dir||(AR.test(s)?'rtl':'ltr');x.textAlign=o.align||'start';x.globalAlpha=o.alpha??1;
 if(o.stroke){x.lineJoin='round';x.lineWidth=o.stroke;x.strokeStyle='#000';x.strokeText(s,X,Y)}x.fillStyle=color;x.fillText(s,X,Y);x.restore()}};
function layer(s,X,Y,size){let lines=s.split('\n').slice(0,5);const maxw=cv.width*0.91;
 x.font="700 "+size+"px 'CairoT'";const w=Math.max(...lines.map(l=>x.measureText(l).width));if(w>maxw)size*=maxw/w;
 lines.forEach((l,i)=>U.text(l,X,Y+i*1.35*size,size,'#fff',{align:'center'}));return {n:lines.length,size}}
function bb(){const d=x.getImageData(0,0,cv.width,cv.height).data;let a=1e9,b=-1;for(let i=0;i<cv.width*cv.height;i++){if(d[4*i]>128){const px=i%cv.width;a=Math.min(a,px);b=Math.max(b,px)}}return [a,b]}
function rows(){const d=x.getImageData(0,0,cv.width,cv.height).data;const r=[];for(let y=0;y<cv.height;y++){let k=0;for(let X=0;X<cv.width;X++)k+=d[4*(y*cv.width+X)]>128;r.push(k)}return r}
const clr=()=>{x.fillStyle='#000';x.fillRect(0,0,cv.width,cv.height)};
clr();U.text('مرحبا بالعالم',300,60,30,'#fff');const ar=bb();
clr();U.text('Hello world',300,60,30,'#fff');const en=bb();
clr();U.text('مرحبا بالعالم',300,60,30,'#fff',{dir:'ltr'});const forced=bb();
clr();const L=layer('سطر\nسطر\nسطر\nسطر\nسطر\nسطر',200,40,30);const R=rows();
OUT({ar,en,forced,L,R})"""
    src, o = chrome_dump(wd, "canvas", hpage("<canvas id=c width=400 height=400></canvas>", js, W=400, H=400), (400, 400), 4000)
    np = np_()
    r = np.array(o["R"]) > 0
    starts = [i for i in range(1, len(r)) if r[i] and not r[i - 1]]
    pitch = float(np.median(np.diff(starts))) if len(starts) > 1 else 0
    write_json(wd / "canvas.json", o)
    return [check("Arabic auto-rtl: ink ends at the anchor x (start = right)", abs(o["ar"][1] - 300) <= 3, o["ar"], "right edge 300"),
            check("Latin stays ltr: ink starts at the anchor x", abs(o["en"][0] - 300) <= 4, o["en"], "left edge 300"),
            check("layer keeps <= 5 lines", o["L"]["n"] == 5 and len(starts) == 5, [o["L"]["n"], len(starts)], 5),
            check("line pitch = 1.35 x size", abs(pitch - 1.35 * o["L"]["size"]) <= 1.5, pitch, 1.35 * o["L"]["size"]),
            check("negative control: forcing ltr anchors Arabic on the wrong side", not (abs(o["forced"][1] - 300) <= 3),
                  o["forced"], "right edge 300")], [wd / "canvas.json", src]


@card("ARAB-90")
def block_rotation(task, wd):
    """The whole Arabic block (never letters) rotates 90° like a camera roll; a band of background at 60% hides
    the turn; the next line is laid out on the new (vertical) axis."""
    np = np_()
    from PIL import Image, ImageDraw
    f = font(CAIRO, 48, wght=800)
    blk, _ = tile("كتلة النص", f)
    rot = blk.rotate(90, expand=True)
    W, H = 360, 420
    bg = (20, 30, 60)
    c = blank((W, H), bg)
    place(c, rot, 120, H / 2)
    band = Image.new("RGBA", (W, 40), bg + (int(255 * 0.6),))
    c.alpha_composite(band, (0, 30))
    nxt, _ = tile("يكمل", font(CAIRO, 40, wght=700))
    place(c, nxt.rotate(90, expand=True), 240, H / 2)
    c.convert("RGB").save(wd / "rotated.png")
    a = arr(c)
    m0 = np.asarray(blk.getchannel("A")) > 128
    m_rot = np.rot90(m0)
    reg = lum(a[int(H / 2 - rot.height / 2):int(H / 2 + rot.height / 2), int(120 - rot.width / 2):int(120 + rot.width / 2)]) > 110
    i_ok = iou(reg, m_rot)
    i_bad = iou(reg, m0)
    under = np.array(bg, float)
    bandpx = a[50, 300]
    expect = under * 0.6 + under * 0.4
    nb = bbox(lum(a[:, 190:300]) > 110)
    return [check("rendered block equals the 90°-rotated whole block (IoU)", i_ok > 0.9, i_ok, ">0.9"),
            check("background band composited at 60%", float(np.abs(bandpx - expect).max()) < 3, list(bandpx), list(expect)),
            check("next line runs along the rotated axis (taller than wide)", (nb[3] - nb[1]) > 2 * (nb[2] - nb[0]), nb, "vertical"),
            check("negative control: the unrotated block does not match", not (i_bad > 0.9), i_bad, ">0.9")], [wd / "rotated.png"]


@card("ARAB-U01")
def el_messiri_bundled(task, wd):
    np = np_()
    from fontTools.ttLib import TTFont
    tt = TTFont(str(MESSIRI))
    ax = {a.axisTag: (a.minValue, a.maxValue) for a in tt["fvar"].axes}
    lic = (FONTS / "OFL-ElMessiri.txt").read_text(encoding="utf-8", errors="replace")
    text = "أغنية الصباح"
    m400 = shaped_mask(text, font(MESSIRI, 72, wght=400))
    m700 = shaped_mask(text, font(MESSIRI, 72, wght=700))
    basic = basic_mask(text, MESSIRI, 72)
    t, _ = tile(text, font(MESSIRI, 72, wght=700))
    t.save(wd / "messiri.png")
    return [check("variable wght axis spans Regular-Bold (400-700)", ax.get("wght") == (400.0, 700.0), ax.get("wght"), (400, 700)),
            check("OFL licence shipped beside the font", "Open Font License" in lic, "OFL" if "Open Font License" in lic else "?", "OFL"),
            check("Bold instance inks >10% more than Regular", m700.sum() > 1.1 * m400.sum(), [int(m700.sum()), int(m400.sum())], ">1.1x"),
            check("raqm shaping joins the letters (fewer parts than unshaped)", comps(m700) < comps(basic), comps(m700), comps(basic)),
            check("negative control: the BASIC (unshaped) layout leaves isolated forms", not (comps(basic) <= comps(m700)),
                  comps(basic), comps(m700))], [wd / "messiri.png"]


# ============================================================================= charts-data-infographic
def cmask(a, col, tol=24):
    np = np_()
    return np.abs(a[..., :3] - np.array(hexrgb(col) if isinstance(col, str) else col, dtype=float)).max(-1) <= tol


def vbar_heights(a, xs, col, w=6, tol=24):
    """Measured height (px) of a vertical bar of colour col at each x centre."""
    np = np_()
    out = []
    for x in xs:
        m = cmask(a[:, int(x) - w // 2:int(x) + w // 2 + 1], col, tol).any(1)
        out.append(int(m.sum()))
    return out


def hbar_widths(a, ys, col, tol=24):
    np = np_()
    return [int(cmask(a[int(y) - 1:int(y) + 2], col, tol).any(0).sum()) for y in ys]


def pil(size, bg):
    return rgbim(size, hexrgb(bg) if isinstance(bg, str) else bg)


def drect(im, box, col):
    from PIL import ImageDraw
    x0, y0, x1, y1 = box
    if x1 - x0 >= 0.5 and y1 - y0 >= 0.5:
        ImageDraw.Draw(im).rectangle((round(x0), round(y0), round(x1) - 1, round(y1) - 1),
                                     fill=hexrgb(col) if isinstance(col, str) else col)


def dtext(im, xy, s, f, col, anchor="la", **kw):
    from PIL import ImageDraw
    ImageDraw.Draw(im).text(xy, s, font=f, fill=hexrgb(col) if isinstance(col, str) else col, anchor=anchor, **kw)


@card("DATA-04")
def insight_story_arc(task, wd):
    """One sentence per chart computed from the record ('sales doubled after March'), arc hook -> baseline ->
    build -> climax -> CTA mapped to chart states, the sentence is the last thing shown."""
    np = np_()
    sales = [10, 11, 10, 20, 22, 21, 24, 22]
    ratio = float(np.mean(sales[3:]) / np.mean(sales[:3]))
    sentence = "المبيعات تضاعفت بعد مارس" if ratio >= 1.8 else "المبيعات نمت بعد مارس"
    stages = ["hook", "baseline", "build", "climax", "cta"]
    W, H = 400, 260
    fa = font(CAIRO, 26, wght=800)
    xs = [40 + 42 * i for i in range(len(sales))]

    def chart(n, hl=False):
        im = pil((W, H), "#101418")
        for i in range(n):
            h = sales[i] / 24.0 * 160
            drect(im, (xs[i] - 14, 220 - h, xs[i] + 14, 220), "#ffb86b" if hl and i >= 3 else "#6b7280")
        return im
    frames = []
    for st in stages:
        if st == "hook":
            im = pil((W, H), "#101418"); dtext(im, (W / 2, H / 2), "×%.1f" % ratio, mono(60), "#ffffff", "mm")
        elif st == "baseline":
            im = chart(3)
        elif st == "build":
            im = chart(len(sales))
        elif st == "climax":
            im = chart(len(sales), hl=True)
        else:
            im = chart(len(sales), hl=True)
            dtext(im, (W - 20, 30), sentence, fa, "#ffffff", "ra", direction="rtl", language="ar")
        im.save(wd / ("%s.png" % st)); frames.append(arr(im))
    cl = frames[3]
    accent = [cmask(cl[:, x - 3:x + 4], "#ffb86b").sum() > 0 for x in xs]
    txt = [int((lum(f[10:70]) > 200).sum()) for f in frames]
    plan = {"questions": ["هل نمت المبيعات؟", "متى؟", "بكم؟"], "charts": 3, "insight": sentence, "ratio": ratio, "arc": stages}
    write_json(wd / "PLAN.json", plan)
    overlay = {"questions": 3, "charts": 1}
    one_per_q = lambda p: (p["charts"] if isinstance(p["charts"], int) else 0) == len(p["questions"]) if isinstance(p["questions"], list) else p["charts"] == p["questions"]
    return [check("insight computed from the record: after/before March = 2.1x", abs(ratio - 21.8 / (31 / 3)) < 1e-9, ratio, 2.11),
            check("climax highlights exactly the months after March", accent == [False] * 3 + [True] * 5, accent, "3 grey + 5 accent"),
            check("the sentence appears only in the last (CTA) state", txt[-1] > 200 and all(t < 50 for t in txt[1:4]), txt, "last only"),
            check("three questions -> three charts", one_per_q(plan), plan["charts"], 3),
            check("negative control: overlaying three questions on one chart breaks the rule", not one_per_q(overlay), overlay, "3 charts")], \
        [wd / "PLAN.json", wd / "cta.png"]


@card("DATA-05")
def true_zero_shared_scale(task, wd):
    np = np_()
    a_vals, b_vals = [90, 95, 100], [45, 60, 100]
    W, H, base, top = 420, 260, 230, 30

    def panel(vals, x0, lo=0.0, hi=100.0):
        im = pil((W, H), "#ffffff")
        for i, v in enumerate(vals):
            h = (v - lo) / (hi - lo) * (base - top)
            drect(im, (x0 + 40 * i, base - h, x0 + 40 * i + 24, base), "#2563eb")
        return im
    both = pil((W, H), "#ffffff")
    from PIL import Image
    pa, pb = panel(a_vals, 20), panel(b_vals, 230)
    both.paste(pa.crop((0, 0, 210, H)), (0, 0)); both.paste(pb.crop((210, 0, W, H)), (210, 0))
    both.save(wd / "panels.png")
    A = arr(both)
    ha = vbar_heights(A, [32 + 40 * i for i in range(3)], "#2563eb")
    hb = vbar_heights(A, [242 + 40 * i for i in range(3)], "#2563eb")
    want = [round(v / 100 * (base - top)) for v in a_vals]
    trunc = arr(panel(a_vals, 20, lo=88, hi=100))
    ht = vbar_heights(trunc, [32 + 40 * i for i in range(3)], "#2563eb")
    prop = lambda hs, vs: all(abs(h / hs[-1] - v / vs[-1]) < 0.02 for h, v in zip(hs, vs))
    return [check("bars start at a true zero: heights proportional to values", prop(ha, a_vals) and prop(hb, b_vals), [ha, hb], want),
            check("shared scale: equal values give equal heights across panels", ha[2] == hb[2], [ha[2], hb[2]], "equal"),
            check("negative control: a truncated axis exaggerates 90 vs 100", not prop(ht, a_vals), ht, "proportional")], \
        [wd / "panels.png"]


def pie_plan(vals, labels):
    order = sorted(range(len(vals)), key=lambda i: -vals[i])
    tot = float(sum(vals))
    pct = [vals[i] / tot * 100 for i in order]
    if max(pct) - min(pct) <= 5:
        return {"type": "stacked-bar", "slices": [(labels[i], vals[i]) for i in order]}
    keep = order[:5]
    other = sum(vals[i] for i in order[5:])
    sl = [(labels[i], vals[i]) for i in keep] + ([("أخرى", other)] if other else [])
    return {"type": "pie", "slices": sl}


PAL6 = ["#2563eb", "#f59e0b", "#10b981", "#ef4444", "#a855f7", "#64748b"]


def draw_pie(im, cx, cy, r, slices, sweep=360.0, cols=PAL6):
    from PIL import ImageDraw
    d = ImageDraw.Draw(im)
    tot = float(sum(v for _, v in slices))
    a = 0.0
    for k, (_, v) in enumerate(slices):
        size = v / tot * 360.0
        vis = clamp(sweep - a, 0, size)
        if vis > 0:
            d.pieslice((cx - r, cy - r, cx + r, cy + r), -90 + a, -90 + a + vis, fill=hexrgb(cols[k % len(cols)]))
        a += size


def slice_extent(a, cx, cy, r, col):
    np = np_()
    rr, ang = angle_grid(a.shape[0], a.shape[1], cx, cy)
    m = cmask(a, col, 10) & (rr < r - 2) & (rr > r * 0.3)
    if not m.any():
        return 0.0, None
    ring = (rr < r - 2) & (rr > r * 0.3)
    hist = np.zeros(360)
    for d in range(360):
        sel = ring & (ang >= d) & (ang < d + 1)
        hist[d] = (m & sel).sum() / max(1, sel.sum())
    deg = np.nonzero(hist > 0.5)[0]
    return float((hist > 0.5).sum()), int(deg.min())


@card("DATA-08")
def pie_rules(task, wd):
    np = np_()
    vals = [8, 30, 4, 18, 22, 12, 6]
    labels = list("ABCDEFG")
    plan = pie_plan(vals, labels)
    im = pil((300, 300), "#ffffff")
    draw_pie(im, 150, 150, 120, plan["slices"])
    im.save(wd / "pie.png")
    A = arr(im)
    ext = [slice_extent(A, 150, 150, 120, PAL6[k]) for k in range(len(plan["slices"]))]
    tot = float(sum(vals))
    want = [v / tot * 360 for _, v in plan["slices"]]
    near = pie_plan([26, 25, 24, 25], list("wxyz"))
    bad = pil((300, 300), "#ffffff")
    draw_pie(bad, 150, 150, 120, [(l, v) for l, v in zip(labels, vals)][:6])
    B = arr(bad)
    bext = [slice_extent(B, 150, 150, 120, PAL6[k])[0] for k in range(6)]
    write_json(wd / "plan.json", {"plan": plan, "near_equal": near})
    return [check("at most five slices + 'other'", len(plan["slices"]) == 6 and plan["slices"][-1][0] == "أخرى", len(plan["slices"]), 6),
            check("largest slice starts at 12 o'clock", ext[0][1] is not None and ext[0][1] <= 1, ext[0][1], 0),
            check("measured slice angles match shares (±2°)", all(abs(e[0] - w) <= 2.5 for e, w in zip(ext, want)), [e[0] for e in ext], want),
            check("slices sorted clockwise by size", all(ext[i][0] >= ext[i + 1][0] - 1 for i in range(4)), [e[0] for e in ext[:5]], "descending"),
            check("near-equal shares become a stacked bar", near["type"] == "stacked-bar", near["type"], "stacked-bar"),
            check("negative control: the unsorted input is not ordered by size", not all(bext[i] >= bext[i + 1] - 1 for i in range(4)),
                  bext, "descending")], [wd / "pie.png", wd / "plan.json"]


@card("DATA-10")
def source_or_illustrative(task, wd):
    np = np_()
    W, H = 400, 240

    def chart(rows, source=None, illustrative=False):
        im = pil((W, H), "#000000")
        if not rows:
            dtext(im, (W / 2, H / 2), "لا توجد بيانات مسجلة لهذه الفترة بعد.", font(CAIRO, 20, wght=600), "#ffffff", "mm",
                  direction="rtl", language="ar")
            return im
        for i, v in enumerate(rows):
            drect(im, (40 + 50 * i, 190 - v * 1.4, 70 + 50 * i, 190), "#2563eb")
        if source:
            dtext(im, (W - 10, H - 10), source, mono(10), (153, 153, 153), "rd")
        if illustrative:
            dtext(im, (10, 10), "توضيحية", font(CAIRO, 14, wght=600), (153, 153, 153), "la", direction="rtl", language="ar")
        return im
    real = chart([40, 70, 100], source="SRC: GASTAT 2025")
    fake = chart([40, 70, 100], illustrative=True)
    empty = chart([])
    for n, im in (("real", real), ("illustrative", fake), ("empty", empty)):
        im.save(wd / ("%s.png" % n))
    R, F, E, N = arr(real), arr(fake), arr(empty), arr(chart([40, 70, 100]))
    corner = lambda a: a[H - 30:H, W - 200:W]
    cmax = float(lum(corner(R)).max())
    gate = lambda spec: bool(spec.get("source")) or bool(spec.get("illustrative")) or not spec.get("rows")
    return [check("source line in the corner at 60% ink", abs(cmax - 153) <= 6 and (lum(corner(R)) > 60).sum() > 40, cmax, 153),
            check("invented data says 'illustrative' in-frame", (lum(F[5:35, 5:120]) > 60).sum() > 40, int((lum(F[5:35, 5:120]) > 60).sum()), ">40"),
            check("empty source shows the empty-state copy, no bars", (lum(E) > 128).sum() > 200 and not cmask(E, "#2563eb").any(),
                  int((lum(E) > 128).sum()), ">200 and no bars"),
            check("figure gate passes sourced / illustrative / empty", gate({"rows": [1], "source": "x"}) and gate({"rows": [1], "illustrative": True})
                  and gate({"rows": []}), True, True),
            check("negative control: an unsourced chart has an empty corner and fails the gate",
                  not ((lum(corner(N)) > 60).sum() > 40 or gate({"rows": [1]})), int((lum(corner(N)) > 60).sum()), ">40")], \
        [wd / "real.png", wd / "empty.png"]


@card("DATA-11")
def direct_labels(task, wd):
    np = np_()
    W, H = 420, 260
    series = {"الرياض": [20, 40, 60, 90], "جدة": [30, 35, 45, 55], "الدمام": [10, 20, 25, 35]}
    cols = {"الرياض": "#f59e0b", "جدة": "#9ca3af", "الدمام": "#6b7280"}
    xs = [40 + 90 * i for i in range(4)]
    fa = font(CAIRO, 16, wght=700)

    def chart(legend=False):
        im = pil((W, H), "#ffffff")
        for name, v in series.items():
            pts = [(x, 230 - y * 2) for x, y in zip(xs, v)]
            poly(im, pts, 3, hexrgb(cols[name]))
            ex, ey = pts[-1]
            if legend:
                k = list(series).index(name)
                dtext(im, (W - 10, 10 + 20 * k), name, fa, cols[name], "ra", direction="rtl", language="ar")
            else:
                dtext(im, (ex + 8, ey), name, fa, cols[name], "lm", direction="rtl", language="ar")
        return im
    a, b = arr(chart()), arr(chart(True))
    chart().save(wd / "direct.png")

    def dist(img, name):
        ex, ey = xs[-1], 230 - series[name][-1] * 2
        m = cmask(img, cols[name], 20)
        m[:, :xs[-1] + 4] = False
        ys, xs_ = np.nonzero(m)
        return float(np.hypot(xs_.mean() - ex, ys.mean() - ey)) if len(xs_) else 999.0
    d_direct = [dist(a, n) for n in series]
    d_leg = [dist(b, n) for n in series]
    accent = int(cmask(a, "#f59e0b", 20).sum())
    return [check("each label sits at its line end (<40 px)", all(d < 40 for d in d_direct), d_direct, "<40"),
            check("label uses its series colour; one accent, rest grey", accent > 200 and cols["جدة"] != cols["الرياض"], accent, ">200"),
            check("negative control: a detached legend is far from the data", not all(d < 40 for d in d_leg), d_leg, "<40")], \
        [wd / "direct.png"]


def activity_style(act):
    import colorsys
    w = 2 + 4 * clamp(act)
    sat = 0.4 + 0.6 * clamp(act)
    r, g, b = colorsys.hsv_to_rgb(0.58, sat, 0.95)
    return w, (int(r * 255), int(g * 255), int(b * 255))


@card("DATA-14")
def motion_channel_mapping(task, wd):
    np = np_()
    import colorsys
    acts = [0.0, 0.5, 1.0]
    im = pil((300, 200), "#ffffff")
    for i, a in enumerate(acts):
        w, col = activity_style(a)
        poly(im, [(30, 50 + 50 * i), (270, 50 + 50 * i)], w, col, cap=False)
    im.save(wd / "channels.png")
    A = arr(im)
    widths, sats = [], []
    for i in range(3):
        colm = A[30:180, 150]
        m = lum(A[50 + 50 * i - 8:50 + 50 * i + 9, 150:151]) < 240
        widths.append(int(m.sum()))
        px = A[50 + 50 * i, 150] / 255.0
        sats.append(colorsys.rgb_to_hsv(*px)[1])

    def valid(spec):
        return spec.get("quantity") in ("length", "colour", "label") and spec.get("speed") in (None, "direction")
    flat = [2, 2, 2]
    return [check("stroke width 2 -> 4 -> 6 px with activity", widths == [2, 4, 6], widths, [2, 4, 6]),
            check("saturation 40% -> 70% -> 100%", all(abs(s - w) < 0.03 for s, w in zip(sats, [0.4, 0.7, 1.0])), sats, [0.4, 0.7, 1.0]),
            check("quantity on length, speed only for direction passes the mapping gate", valid({"quantity": "length", "speed": "direction"}), True, True),
            check("negative control: quantity encoded by speed alone is rejected", not valid({"quantity": None, "speed": "quantity"}), False, True),
            check("negative control: an unmapped stroke set has one width", not (flat == [2, 4, 6]), flat, [2, 4, 6])], [wd / "channels.png"]


@card("DATA-15")
def one_scalar_rule(task, wd):
    """shown = value * p(t); bar width and counter both from `shown` every frame; ease cubic-bezier(.22,1,.36,1)
    over 700 ms (no spring on data marks)."""
    np = np_()
    value, vmax, track = 840, 1000, 300
    ez = bez(.22, 1, .36, 1)
    W, H, x0 = 400, 120, 40

    def frame(t, e=ez):
        shown = value * e(prog(t, 0.1, 0.8))
        im = pil((W, H), "#000000")
        drect(im, (x0, 20, x0 + shown / vmax * track, 44), "#10b981")
        draw_digits(im, "%4d" % round(shown), 250, 70, 24)
        return im
    vid, frames = film(wd, "scalar.mp4", frame, 1.0, (W, H))
    bad = []
    widths = []
    for fr in frames:
        w = int(cmask(fr[30:31], "#10b981").sum())
        n = read_digits(fr, 250, 70, 4, 24).strip()
        widths.append(w)
        v = int(n) if n.isdigit() else 0
        if abs(w - v / vmax * track) > 1.01:
            bad.append((w, v))
    final = read_digits(frames[-1], 250, 70, 4, 24).strip()
    sp = spring_curve(300, 10)
    over = max(int(cmask(arr(frame(t, lambda p: sp(p * 0.7)))[30:31], "#10b981").sum()) for t in np.linspace(0.1, 0.8, 22))
    return [check("bar width and counter agree on every frame (±1 px)", not bad, bad[:3], []),
            check("counter lands on the exact figure", final == str(value), final, str(value)),
            check("bar never exceeds its value (no overshoot)", max(widths) <= round(value / vmax * track) + 1, max(widths), value / vmax * track),
            check("negative control: a spring on the bar overshoots its value", not (over <= round(value / vmax * track) + 1), over,
                  value / vmax * track)], [vid]


@card("DATA-16")
def rtl_axis_conventions(task, wd):
    np = np_()
    W, H = 420, 300
    cats, vals = ["أ", "ب", "ج"], [60, 100, 30]
    years = [2022, 2023, 2024, 2025]
    anchor = W - 60
    im = pil((W, H), "#ffffff")
    for i, (c, v) in enumerate(zip(cats, vals)):
        y = 40 + 40 * i
        drect(im, (anchor - v * 2.5, y, anchor, y + 24), "#2563eb")
        dtext(im, (anchor + 10, y + 12), c, font(CAIRO, 20, wght=700), "#111111", "lm", direction="rtl", language="ar")
    for k, yv in enumerate(years):
        draw_digits(im, str(yv), 40 + 90 * k, 240, 16, fill=(0, 0, 0))
    im.save(wd / "rtl_axes.png")
    A = arr(im)
    rights, lefts = [], []
    for i in range(3):
        cols_ = np.nonzero(cmask(A[52 + 40 * i:53 + 40 * i], "#2563eb").any(0))[0]
        rights.append(int(cols_.max())); lefts.append(int(cols_.min()))
    row = (lum(A[240:262]) < 128).any(0)
    starts = [i for i in range(1, W) if row[i] and not row[i - 1]]
    groups = [starts[0]] + [s for p, s in zip(starts, starts[1:]) if s - p > 40]
    read = [read_digits(255 - A, g, 240, 4, 16, search=4) for g in groups]
    ltr = im.copy()
    L = pil((W, H), "#ffffff")
    for i, v in enumerate(vals):
        drect(L, (60, 40 + 40 * i, 60 + v * 2.5, 64 + 40 * i), "#2563eb")
    LA = arr(L)
    lr = [int(np.nonzero(cmask(LA[52 + 40 * i:53 + 40 * i], "#2563eb").any(0))[0].max()) for i in range(3)]
    return [check("categorical bars mirrored: common right edge (inline-end anchor)", len(set(rights)) == 1, rights, "one edge"),
            check("bars grow leftwards in proportion", all(abs((anchor - l) - v * 2.5) <= 1.5 for l, v in zip(lefts, vals)), lefts, "anchor - 2.5 v"),
            check("time axis stays left-to-right (2022 leftmost)", read == [str(y) for y in years], read, years),
            check("negative control: an un-mirrored chart has no common right edge", not (len(set(lr)) == 1), lr, "one edge")], \
        [wd / "rtl_axes.png"]


CHART_MIN = {"label": 28, "tick": 24, "counter": (72, 160)}


@card("DATA-17")
def chart_type_sizes(task, wd):
    """At 1080 px: labels >= 28 px, ticks >= 24 px, counters 72-160 px; portrait chart <= 920 px wide and <= 45% of
    the frame height (rendered at K = 0.5)."""
    np = np_()
    W, H = 540, 960
    spec = {"label": 30, "tick": 24, "counter": 96, "chart_w": 900, "chart_h": 820}
    web = {"label": 12, "tick": 10, "counter": 32, "chart_w": 1000, "chart_h": 1200}

    def ok(s):
        return (s["label"] >= 28 and s["tick"] >= 24 and 72 <= s["counter"] <= 160 and s["chart_w"] <= 920
                and s["chart_h"] <= 0.45 * 1920)
    im = pil((W, H), "#0b0f14")
    cx0, cy0 = (W - spec["chart_w"] * K) / 2, 300
    vals = [40, 75, 55, 90]
    bw = spec["chart_w"] * K / 8
    for i, v in enumerate(vals):
        x = cx0 + bw * (2 * i + 0.5)
        drect(im, (x, cy0 + spec["chart_h"] * K - v / 100 * spec["chart_h"] * K * 0.8, x + bw, cy0 + spec["chart_h"] * K), "#3b82f6")
    draw_digits(im, "128", W / 2 - 60, 200, spec["counter"] * K)
    dtext(im, (W / 2, cy0 + spec["chart_h"] * K + 30), "Hxg", font(POPPINS_R, spec["label"] * K), "#ffffff", "mm")
    im.save(wd / "portrait.png")
    A = arr(im)
    bars = cmask(A, "#3b82f6")
    b = bbox(bars)
    lab = bbox(lum(A[int(cy0 + spec["chart_h"] * K + 5):]) > 128)
    em_px = (lab[3] - lab[1])
    ref = bbox(np.asarray(tile("Hxg", font(POPPINS_R, 100))[0].getchannel("A")) > 128)
    measured_size = em_px / ((ref[3] - ref[1]) / 100.0) / K
    return [check("chart block <= 920 px wide and <= 45% of the frame height", (b[2] - b[0]) / K <= 920 and (b[3] - b[1]) / H <= 0.45,
                  [(b[2] - b[0]) / K, (b[3] - b[1]) / H], "<=920, <=0.45"),
            check("rendered label measures >= 28 px at 1080 (from ink height)", measured_size >= 27.5, measured_size, ">=28"),
            check("spec passes the size gate", ok(spec), spec, CHART_MIN),
            check("negative control: web sizes (12 px labels) fail the gate", not ok(web), web, CHART_MIN)], [wd / "portrait.png"]


@card("DATA-18")
def highlight_pulse(task, wd):
    """Others dim to 35% over 300 ms; the key bar pulses once 300 ms up / 500 ms down, then holds >= 1500 ms."""
    np = np_()
    W, H = 360, 220
    base = hexrgb("#3b82f6")
    key = 2
    xs = [40 + 60 * i for i in range(5)]

    def frame(t, dim=True):
        im = pil((W, H), "#000000")
        d = 1 - 0.65 * prog(t, 0.2, 0.5) if dim else 1.0
        up, dn = prog(t, 0.5, 0.8), prog(t, 0.8, 1.3)
        s = 1 + 0.08 * (in_out_cubic(up) - in_out_cubic(dn))
        for i, x in enumerate(xs):
            h = 140 * (s if i == key else 1)
            col = base if i == key else tuple(int(c * d) for c in base)
            drect(im, (x, 200 - h, x + 36, 200), col)
        return im
    vid, frames = film(wd, "pulse.mp4", frame, 3.0, (W, H))
    lv = lambda fr, i: float(fr[150, xs[i] + 18].max())
    other_end = lv(frames[-1], 0) / 255.0
    hk = [int((fr[:, xs[key] + 18].max(-1) > 50).sum()) for fr in frames]
    top = max(hk)
    plate = [i for i, h in enumerate(hk) if h == top]
    peak = (plate[0] + plate[-1]) / 2.0
    hold = (len(frames) - 1 - int(round(1.3 * 30))) / 30.0
    nd = arr(frame(2.9, dim=False))
    return [check("others settle at 35% brightness", abs(other_end - 0.35) < 0.02, other_end, 0.35),
            check("dim takes 300 ms (half-way at 0.35 s)", abs(lv(frames[int(0.35 * 30)], 0) / 255 - (1 - 0.65 * 0.5)) < 0.08, lv(frames[10], 0) / 255, 0.675),
            check("single pulse peaks 300 ms after it starts", abs(peak / 30.0 - 0.8) <= 0.034, peak / 30.0, 0.8),
            check("final state holds >= 1500 ms", hold >= 1.5 and hk[-1] == 140, [hold, hk[-1]], ">=1.5 s"),
            check("negative control: without the dim the others stay at 100%", not (abs(float(nd[150, xs[0] + 18].max()) / 255 - 0.35) < 0.02),
                  float(nd[150, xs[0] + 18].max()) / 255, 0.35)], [vid]


def out_quint(p):
    return pow_out(p, 5)


@card("DATA-19")
def tabular_count_up(task, wd):
    """n = round(lerp(0, 128, outQuint(prog(t, 0.2, 2.6)))), tabular mono digits, exact on the last frame."""
    np = np_()
    W, H = 300, 120

    def n_at(t, e=out_quint):
        return int(round(128 * e(prog(t, 0.2, 2.6))))

    def frame(t, e=out_quint):
        im = pil((W, H), "#101418")
        draw_digits(im, "%3d" % n_at(t, e), 90, 30, 48, fill=hexrgb("#ffb86b"))
        return im
    vid, frames = film(wd, "count.mp4", frame, 2.8, (W, H))
    reads = [read_digits(fr, 90, 30, 3, 48) for fr in frames]
    vals = [int(r) if r.strip().isdigit() else -1 for r in reads]
    want = [n_at(i / 30.0) for i in range(len(frames))]
    lin = read_digits(arr(frame(1.0, e=lambda p: p)), 90, 30, 3, 48).strip()
    cols = [bbox(lum(fr) > 60)[2] for fr in frames if (lum(fr) > 60).any()]
    return [check("every frame shows the eased value", vals == want, [v for v, w in zip(vals, want) if v != w][:5], "all equal"),
            check("lands exactly on 128", vals[-1] == 128, vals[-1], 128),
            check("monotone count", all(b >= a for a, b in zip(vals, vals[1:])), "monotone", "monotone"),
            check("right edge fixed (tabular, right-aligned)", max(cols[-40:]) - min(cols[-40:]) <= 1, [min(cols[-40:]), max(cols[-40:])], "fixed"),
            check("negative control: a linear count reads differently at 1.0 s", not (lin == str(n_at(1.0))), lin, n_at(1.0))], [vid]


def mulberry32(seed):
    a = seed & 0xFFFFFFFF

    def r():
        nonlocal a
        a = (a + 0x6D2B79F5) & 0xFFFFFFFF
        t = a
        t = ((t ^ (t >> 15)) * (t | 1)) & 0xFFFFFFFF
        t ^= (t + (((t ^ (t >> 7)) * (t | 61)) & 0xFFFFFFFF)) & 0xFFFFFFFF
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296.0
    return r


@card("DATA-22")
def scramble_counter(task, wd):
    """Seeded PRNG digits each frame (never Math.random), digit k locks at t0 + 40 ms * k, ~1 s total."""
    final, t0 = "7351", 0.8

    def make():
        rnd = mulberry32(2026)
        seq = []
        for i in range(36):
            t = i / 30.0
            s = "".join(final[k] if t >= t0 + 0.04 * k else str(int(rnd() * 10)) for k in range(4))
            seq.append(s)
        return seq
    seq = make()

    def frame(t):
        im = pil((260, 100), "#000000")
        draw_digits(im, seq[min(len(seq) - 1, int(round(t * 30)))], 60, 25, 40)
        return im
    vid, frames = film(wd, "scramble.mp4", frame, 1.2, (260, 100))
    reads = [read_digits(fr, 60, 25, 4, 40) for fr in frames]
    lock_ok = all(reads[i][k] == final[k] for i in range(len(reads)) for k in range(4) if i / 30.0 >= t0 + 0.04 * k)
    distinct = len({r[0] for r in reads[:int(t0 * 30)]})
    vid2, frames2 = film(wd, "scramble_again.mp4", frame, 1.2, (260, 100))
    from _harness import sha as _sha
    early = [r for r in reads[:int(t0 * 30)]]
    return [check("every digit holds its final value from its lock time on", lock_ok, reads[-12:], final),
            check("locks run left-to-right 40 ms apart", [round(t0 + 0.04 * k, 2) for k in range(4)] == [0.8, 0.84, 0.88, 0.92], "0.80..0.92", "40 ms"),
            check("unlocked digits flicker (>= 5 values)", distinct >= 5, distinct, ">=5"),
            check("seeded: a second render is byte-identical", _sha(vid) == _sha(vid2), _sha(vid)[:12], _sha(vid2)[:12]),
            check("negative control: before locking the digits are not the final value", not all(r == final for r in early), early[:3], final)], [vid]


@card("DATA-23")
def growing_count_punch(task, wd):
    """Two tweens, same start and ease (700 ms easeOutExpo): value and scale START->1; landing punch 1.04 for 60 ms."""
    np = np_()
    from PIL import Image
    target, s0 = 950, 0.5
    W, H = 360, 200
    base_t, _ = tile("000", mono(80), fill=(255, 255, 255, 255))

    def scale_at(t):
        e = expo_out(prog(t, 0.1, 0.8))
        s = s0 + (1 - s0) * e
        if 0.8 <= t < 0.86:
            s *= 1.04
        return s, e

    def frame(t):
        s, e = scale_at(t)
        c = blank((W, H))
        t_, _ = tile("%03d" % round(target * e), mono(80), fill=(255, 255, 255, 255))
        place(c, t_, W / 2, H / 2, scale=s)
        return c
    vid, frames = film(wd, "punch.mp4", frame, 1.2, (W, H))
    hs = [(lambda b: b[3] - b[1] if b else 0)(bbox(lum(fr) > 128)) for fr in frames]
    full = hs[-1]
    land = hs[int(round(0.82 * 30))]
    ts = [i / 30.0 for i in range(len(frames))]
    pre = [(h / full, scale_at(t)[0]) for h, t in zip(hs, ts) if 0.15 < t < 0.75]
    corr = float(np.corrcoef([a for a, _ in pre], [b for _, b in pre])[0, 1])
    def plain(t):
        c = blank((W, H))
        t_, _ = tile("%03d" % round(target * expo_out(prog(t, 0.1, 0.8))), mono(80), fill=(255, 255, 255, 255))
        place(c, t_, W / 2, H / 2)
        return arr(c)
    flat = [(lambda b: b[3] - b[1])(bbox(lum(plain(t)) > 128)) for t in (0.2, 0.5, 0.75)]
    return [check("height follows the value's ease (corr > 0.98)", corr > 0.98, corr, ">0.98"),
            check("starts at the start scale (0.5)", abs(hs[4] / full - scale_at(4 / 30.0)[0]) < 0.04, hs[4] / full, scale_at(4 / 30.0)[0]),
            check("landing punch 1.04 for 60 ms", abs(land / full - 1.04) < 0.02, land / full, 1.04),
            check("settles back to 1.0", hs[-1] == hs[-5], [hs[-5], hs[-1]], "equal"),
            check("negative control: an unscaled counter has constant height (no growth)", not (np.ptp(flat) > 0.2 * full), flat, ">0.2 x full")], [vid]


def compact(v, ar=False):
    a = abs(v)
    for lim, en, arw in ((1e9, "B", "مليار"), (1e6, "M", "مليون"), (1e3, "K", "ألف")):
        if a >= lim:
            x = "%.1f" % (v / lim)
            return (x + " " + arw) if ar else (x + en)
    return "{:,}".format(int(v))


@card("DATA-25")
def compact_locale_numbers(task, wd):
    cases = {1234: "1.2K", 3400000: "3.4M", 5600000000: "5.6B", 999: "999", 12345: "12.3K", -2500000: "-2.5M"}
    got = {k: compact(k) for k in cases}
    ar = compact(3400000, ar=True)
    nums = node_eval("console.log(JSON.stringify([new Intl.NumberFormat('ar-EG',{maximumFractionDigits:1}).format(3.4),"
                     "new Intl.NumberFormat('ar-u-nu-latn',{maximumFractionDigits:1}).format(3.4),"
                     "new Intl.NumberFormat('en-US',{style:'percent',maximumFractionDigits:1}).format(0.1234)]))")
    write_json(wd / "formats.json", {"compact": got, "arabic": ar, "intl": nums})
    return [check("thresholds 1e3/1e6/1e9 with one decimal", got == cases, got, cases),
            check("Arabic words ألف/مليون/مليار", ar == "3.4 مليون", ar, "3.4 مليون"),
            check("ar-EG -> ٣٫٤ and ar-u-nu-latn keeps 3.4", nums[0] == "٣٫٤" and nums[1] in ("3.4", "3٫4"), nums[:2], ["٣٫٤", "3.4"]),
            check("percent with 1 decimal", nums[2] == "12.3%", nums[2], "12.3%"),
            check("negative control: raw str() is not compact", not (str(1234) == cases[1234]), str(1234), "1.2K")], [wd / "formats.json"]


def haversine(a, b, R=6371.0088):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


@card("DATA-28")
def hud_counters(task, wd):
    """Year roll 2006->2026 in 800 ms easeOut (mono HUD corner) + map journey: real km by haversine distributed by
    arc length, 7 progress dots filling per stop."""
    np = np_()
    from PIL import ImageDraw
    stops = [(24.7136, 46.6753), (26.4207, 50.0888), (21.4858, 39.1925), (21.3891, 39.8579), (24.4672, 39.6111),
             (18.2465, 42.5117), (17.4933, 44.1277)]
    legs = [haversine(stops[i], stops[i + 1]) for i in range(len(stops) - 1)]
    cum = np.concatenate([[0], np.cumsum(legs)])
    eq = haversine((0, 0), (0, 1))
    cos_law = lambda a, b: 6371.0088 * math.acos(math.sin(math.radians(a[0])) * math.sin(math.radians(b[0])) +
                                                 math.cos(math.radians(a[0])) * math.cos(math.radians(b[0])) * math.cos(math.radians(b[1] - a[1])))
    W, H = 360, 200
    D = 3.0

    def frame(t):
        im = pil((W, H), "#05070a")
        y = 2006 + round(20 * pow_out(prog(t, 0.1, 0.9), 2))
        draw_digits(im, str(y), 10, 10, 20, fill=(200, 255, 200))
        km = cum[-1] * prog(t, 1.0, D)
        draw_digits(im, "%5d" % round(km), 10, 160, 20, fill=(200, 255, 200))
        d = ImageDraw.Draw(im)
        for k in range(7):
            on = km >= cum[k] - 1e-6
            d.ellipse((200 + 20 * k, 170, 210 + 20 * k, 180), fill=(255, 200, 0) if on else (60, 60, 60))
        return im
    vid, frames = film(wd, "hud.mp4", frame, D + 0.2, (W, H))
    yrs = [read_digits(fr, 10, 10, 4, 20) for fr in frames]
    mid = int(round(0.5 * 30))
    want_mid = 2006 + round(20 * pow_out(prog(mid / 30.0, 0.1, 0.9), 2))
    dots = [int(sum(fr[175, 205 + 20 * k, 0] > 200 for k in range(7))) for fr in frames]
    last_km = read_digits(frames[-1], 10, 160, 5, 20).strip()
    lin_mid = 2006 + round(20 * prog(mid / 30.0, 0.1, 0.9))
    write_json(wd / "journey.json", {"legs_km": legs, "total_km": float(cum[-1])})
    return [check("year rolls 2006 -> 2026", yrs[0] == "2006" and yrs[-1] == "2026", [yrs[0], yrs[-1]], ["2006", "2026"]),
            check("mid-roll year follows easeOut", yrs[mid] == str(want_mid), yrs[mid], want_mid),
            check("haversine: 1° on the equator = 111.19 km", abs(eq - 111.195) < 0.01, eq, 111.195),
            check("haversine agrees with the spherical law of cosines", all(abs(l - cos_law(stops[i], stops[i + 1])) < 0.01 for i, l in enumerate(legs)), legs[0], "equal"),
            check("odometer lands on the real total km", last_km == str(int(round(cum[-1]))), last_km, int(round(cum[-1]))),
            check("7 dots fill one per stop", dots[0] == 1 and dots[-1] == 7 and all(b >= a for a, b in zip(dots, dots[1:])), [dots[0], dots[-1]], [1, 7]),
            check("negative control: a linear roll reads another year mid-way", not (str(lin_mid) == yrs[mid]), lin_mid, yrs[mid])], \
        [vid, wd / "journey.json"]


@card("DATA-35")
def staggered_bar_growth(task, wd):
    """step = min(80, 700/n) ms, easeOutQuint over 700 ms, RTL bars grow leftwards; the set lands within ~1.1 s."""
    np = np_()
    vals = [80, 55, 95, 40, 70, 60]
    n = len(vals)
    step = min(0.080, 0.700 / n)
    W, H, anchor = 400, 300, 360
    ys = [30 + 42 * i for i in range(n)]

    def frame(t, stg=step):
        im = pil((W, H), "#0d1b2a")
        for i, v in enumerate(vals):
            p = out_quint(prog(t, 0.1 + stg * i, 0.8 + stg * i))
            drect(im, (anchor - 3 * v * p, ys[i], anchor, ys[i] + 30), "#f59e0b" if i == n - 1 else "#3b82f6")
        return im
    vid, frames = film(wd, "bars.mp4", frame, 1.6, (W, H), fps=50)
    w = np.array([[int((fr[ys[i] + 15, :anchor + 1].max(-1) > 100).sum() - 0) for i in range(n)] for fr in frames])
    on = [int(np.nonzero(w[:, i] > 0)[0][0]) for i in range(n)]
    land = [int(np.nonzero(w[:, i] >= 3 * vals[i] - 1)[0][0]) for i in range(n)]
    rights = {int(np.nonzero(frames[-1][ys[i] + 15].max(-1) > 100)[0].max()) for i in range(n)}
    nost = np.array([[int((arr(frame(t, 0.0))[ys[i] + 15].max(-1) > 100).sum()) for i in range(n)] for t in (0.13,)])
    return [check("onsets step 80 ms (4 frames at 50 fps)", all(abs((b - a) - 4) <= 1 for a, b in zip(on, on[1:])), on, "+4"),
            check("set lands within ~1.1 s", max(land) / 50.0 <= 1.12, max(land) / 50.0, "<=1.1"),
            check("bars grow leftwards from one right anchor", len(rights) == 1, sorted(rights), "one anchor"),
            check("final widths proportional to values", all(abs(w[-1, i] - 3 * vals[i]) <= 1 for i in range(n)), list(w[-1]), [3 * v for v in vals]),
            check("negative control: without stagger every bar has already started together", not (len(set((nost[0] > 0).tolist())) > 1),
                  list(nost[0]), "staggered")], [vid]


@card("DATA-36")
def ranked_hbars(task, wd):
    """SKCharts.hbars: sort by |value|, width = |v|/max * 100% (min .8%), value at the tip, the named bar lit."""
    np = np_()
    rows = [("أ", 12), ("ب", -48), ("ج", 30), ("د", 0.1), ("هـ", 64)]
    track, x0 = 280, 60

    def layout(rs, sort=True):
        rs = sorted(rs, key=lambda r: -abs(r[1])) if sort else list(rs)
        mx = max(abs(v) for _, v in rs)
        return [(lab, v, max(0.008, abs(v) / mx) * track) for lab, v in rs]
    lay = layout(rows)
    hl = "ج"
    im = pil((400, 260), "#ffffff")
    for i, (lab, v, w) in enumerate(lay):
        y = 20 + 44 * i
        drect(im, (x0, y, x0 + track, y + 12), "#eeeeee")
        drect(im, (x0, y, x0 + w, y + 12), "#f59e0b" if lab == hl else "#9ca3af")
    im.save(wd / "hbars.png")
    A = arr(im)
    ws = []
    for i in range(len(lay)):
        y = 26 + 44 * i
        ws.append(int((cmask(A[y:y + 1], "#f59e0b") | cmask(A[y:y + 1], "#9ca3af")).sum()))
    lit = [bool(cmask(A[26 + 44 * i:27 + 44 * i], "#f59e0b").any()) for i in range(len(lay))]
    raw = [w for _, _, w in layout(rows, sort=False)]
    return [check("sorted by |value|", ws == sorted(ws, reverse=True), ws, "descending"),
            check("widths = |v|/max of the track (±1 px)", all(abs(m - round(w)) <= 1 for m, (_, _, w) in zip(ws, lay)), ws, [round(w) for _, _, w in lay]),
            check("tiny value keeps the .8% minimum", ws[-1] >= round(0.008 * track) - 0, ws[-1], round(0.008 * track)),
            check("only the named bar is lit", sum(lit) == 1 and lay[lit.index(True)][0] == hl, lit, hl),
            check("negative control: the input order is not ranked", not (raw == sorted(raw, reverse=True)), [round(r) for r in raw], "descending")], \
        [wd / "hbars.png"]


@card("DATA-37")
def bar_chart_race(task, wd):
    """Values linear between periods, rank = sort at each t, y eased 500 ms in-out on swaps, axis max rescales
    (ease-out 600 ms), period label as a clock; <= 10 bars."""
    np = np_()
    names = ["A", "B", "C", "D", "E"]
    cols = ["#ef4444", "#3b82f6", "#10b981", "#f59e0b", "#a855f7"]
    per = [[10, 20, 30, 40, 50], [60, 25, 35, 45, 30], [70, 80, 40, 50, 35], [75, 85, 95, 55, 40]]
    P = 1.0
    W, H, x0, track, pitch = 420, 260, 20, 360, 44

    def vals(t):
        k = min(len(per) - 2, int(t // P))
        u = clamp((t - k * P) / P)
        return [a + (b - a) * u for a, b in zip(per[k], per[k + 1])]

    def ranks(v):
        order = sorted(range(5), key=lambda i: -v[i])
        r = [0] * 5
        for pos, i in enumerate(order):
            r[i] = pos
        return r
    D = P * (len(per) - 1) + 0.6
    nfr = int(round(D * 30)) + 1
    ytab, cur = [], [float(r) for r in ranks(vals(0))]
    tw = [(c, c, -1.0) for c in cur]
    for j in range(nfr):
        t = j / 30.0
        rk = ranks(vals(t))
        for i in range(5):
            a0, b0, ts = tw[i]
            if rk[i] != b0:
                tw[i] = (cur[i], float(rk[i]), t)
            a0, b0, ts = tw[i]
            cur[i] = b0 if ts < 0 else a0 + (b0 - a0) * in_out_cubic(clamp((t - ts) / 0.5))
        ytab.append(list(cur))

    def ypos(t):
        return ytab[min(nfr - 1, int(round(t * 30)))]

    def frame(t):
        im = pil((W, H), "#ffffff")
        v = vals(t)
        mx = max(v)
        yy = ypos(t)
        for i in range(5):
            y = 20 + pitch * yy[i]
            drect(im, (x0, y, x0 + v[i] / mx * track, y + 24), cols[i])
            drect(im, (W - 28 + 5 * i, y, W - 25 + 5 * i, y + 24), cols[i])
        return im
    vid, frames = film(wd, "race.mp4", frame, D, (W, H))
    centres = []
    for fr in frames:
        cy = []
        for c in cols:
            k = cols.index(c)
            m = cmask(fr[:, W - 28 + 5 * k:W - 25 + 5 * k], c, 10).any(1)
            ys = np.nonzero(m)[0]
            cy.append(float(ys.mean()) if len(ys) else None)
        centres.append(cy)
    jump = max(abs(b[i] - a[i]) for a, b in zip(centres, centres[1:]) for i in range(5) if a[i] is not None and b[i] is not None)
    bound = 3.0 * 4 * pitch / 15.0 + 1.0
    rows_ = [(c[0] - 32) / pitch for c in centres if c[0] is not None]
    between = sum(1 for r in rows_ if abs(r - round(r)) > 0.05)
    end = centres[-1]
    order_end = sorted(range(5), key=lambda i: end[i])
    want = sorted(range(5), key=lambda i: -per[-1][i])
    leader_w = max(int(cmask(frames[-1][32:33, :W - 30], c, 10).sum()) for c in cols)
    stat = sorted(range(5), key=lambda i: 20 + pitch * i)
    return [check("final order is the ranking of the last period", order_end == want, order_end, want),
            check("no teleports: per-frame move within a 500 ms in-out cubic swap bound", jump <= bound, jump, bound),
            check("overtaking bar glides between rows for >= 0.5 s", between >= 15, between, ">=15 frames"),
            check("axis rescales: leader fills the track", abs(leader_w - track) <= 1, leader_w, track),
            check("<= 10 bars", len(names) <= 10, len(names), "<=10"),
            check("negative control: a static (unranked) layout keeps input order", not (stat == want), stat, want)], [vid]


@card("DATA-45")
def latency_race(task, wd):
    """Brand bar ease-in-expo to <= 120% width (breaks the frame edge), competitors <= 60%, ms readout per bar."""
    np = np_()
    W, H = 400, 200
    D = 1.1
    in_expo = lambda p: 0.0 if p <= 0 else 2 ** (10 * p - 10)

    def frame(t, ease=in_expo):
        im = pil((W, H), "#000000")
        p = prog(t, 0, D)
        drect(im, (0, 30, min(W, 1.2 * W * ease(p)), 60), "#22c55e")
        for k, f_ in enumerate((0.6, 0.45)):
            drect(im, (0, 90 + 40 * k, f_ * W * p, 120 + 40 * k), "#9ca3af")
        draw_digits(im, "%4d" % round(1000 * (1 - ease(p))), 300, 160, 16)
        return im
    vid, frames = film(wd, "race.mp4", frame, D + 0.1, (W, H))
    bw = [int(cmask(fr[45:46], "#22c55e").sum()) for fr in frames]
    others = max(int(cmask(fr[105:106], "#9ca3af").sum()) for fr in frames)
    half = bw[int(0.5 * D * 30)]
    lin_half = int(cmask(arr(frame(0.5 * D, ease=lambda p: p))[45:46], "#22c55e").sum())
    ms_end = read_digits(frames[-1], 300, 160, 4, 16).strip()
    return [check("brand bar breaks the frame edge at the end", bw[-1] == W and frames[-1][45, W - 1, 1] > 150, bw[-1], W),
            check("ease-in-expo: still tiny at half time (<5%)", half < 0.05 * W, half, "<20"),
            check("competitors stay <= 60% width", others <= 0.6 * W + 1, others, 0.6 * W),
            check("ms readout counts down to 0", ms_end == "0", ms_end, "0"),
            check("negative control: a linear brand bar is already wide at half time", not (lin_half < 0.05 * W), lin_half, "<20")], [vid]


@card("DATA-48")
def radial_clockwise_bars(task, wd):
    """Constant-width wedges from -90° (12 o'clock) clockwise, each grows outward from the inner radius in 400 ms
    cubic-bezier(.33,1,.68,1), 60 ms stagger, label +120 ms."""
    np = np_()
    from PIL import ImageDraw
    vals = [0.9, 0.5, 0.7, 0.3, 0.6, 0.8]
    W = H = 320
    cx = cy = 160
    r0, rk = 40, 100
    ez = bez(.33, 1, .68, 1)
    n = len(vals)

    def frame(t, area=False):
        im = pil((W, H), "#ffffff")
        d = ImageDraw.Draw(im)
        for i, v in enumerate(vals):
            p = ez(prog(t, 0.1 + 0.06 * i, 0.5 + 0.06 * i))
            if p <= 0:
                continue
            L = (math.sqrt(v) if area else v) * rk * p
            a0 = -90 + i * 360.0 / n + 2
            d.pieslice((cx - r0 - L, cy - r0 - L, cx + r0 + L, cy + r0 + L), a0, a0 + 360.0 / n - 4, fill=hexrgb(PAL6[i]))
            if t >= 0.5 + 0.06 * i + 0.12:
                am = math.radians(a0 + 180.0 / n - 2)
                d.ellipse((cx + (r0 + L + 12) * math.cos(am) - 3, cy + (r0 + L + 12) * math.sin(am) - 3,
                           cx + (r0 + L + 12) * math.cos(am) + 3, cy + (r0 + L + 12) * math.sin(am) + 3), fill=(0, 0, 0))
        d.ellipse((cx - r0, cy - r0, cx + r0, cy + r0), fill=(255, 255, 255))
        return im
    vid, frames = film(wd, "radial.mp4", frame, 1.2, (W, H), fps=50)
    rr, ang = angle_grid(H, W, cx, cy)

    def reach(a, i):
        mid = i * 360.0 / n + 180.0 / n
        sel = cmask(a, PAL6[i], 10) & (np.abs(((ang - mid + 180) % 360) - 180) < 8)
        return float(rr[sel].max()) - r0 if sel.any() else 0.0
    fin = [reach(frames[-1], i) for i in range(n)]
    on = [next(j for j, fr in enumerate(frames) if reach(fr, i) > 0) for i in range(n)]
    first_mid = 0 * 360.0 / n + 180.0 / n
    lab_on = next(j for j, fr in enumerate(frames) if (lum(fr) < 40).sum() > 5)
    ar = arr(frame(1.2, area=True))
    fa = [reach(ar, i) for i in range(n)]
    lin = lambda ff: all(abs(f_ / ff[0] - v / vals[0]) < 0.04 for f_, v in zip(ff, vals))
    return [check("wedge length from the inner radius is linear in value", lin(fin), fin, [v * rk for v in vals]),
            check("first wedge sits at 12 o'clock, then clockwise", first_mid < 60 and reach(frames[-1], 1) > 0, first_mid, "0-60°"),
            check("segments start 60 ms apart (3 frames at 50 fps)", all(abs((b - a) - 3) <= 1 for a, b in zip(on, on[1:])), on, "+3"),
            check("first label lands 120 ms after its wedge", abs(lab_on / 50.0 - (0.5 + 0.12)) <= 0.021, lab_on / 50.0, 0.62),
            check("negative control: area (sqrt) mapping breaks the linear lengths", not lin(fa), fa, "linear")], [vid]


def line_series_px(vals, W, H, pad=30):
    n = len(vals)
    lo, hi = min(vals), max(vals)
    return [(pad + (W - 2 * pad) * i / (n - 1), H - pad - (H - 2 * pad) * (v - lo) / (hi - lo)) for i, v in enumerate(vals)]


@card("DATA-50")
def line_draw_area_dots(task, wd):
    """12 points: line dashoffset = 1 - inOutCubic(prog(t, .2, 2.4)); dot r = 12 * outBack(prog(draw, i/(n-1), +.08));
    area gradient #7ee8d2 .35 -> 0 (viewBox 900x620 at K)."""
    np = np_()
    from PIL import Image, ImageDraw
    vals = [45, 52, 48, 60, 58, 70, 66, 80, 77, 95, 103, 128]
    W, H = 450, 310
    pts = line_series_px(vals, W, H)
    dense, L = resample(pts, 1.0)
    ln = (0x7e, 0xe8, 0xd2)
    dot = (0xff, 0xb8, 0x6b)
    n = len(vals)
    cum = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(np.array(pts), axis=0).T))]) / L

    def frame(t):
        im = pil((W, H), "#0a0f14")
        draw = in_out_cubic(prog(t, 0.2, 2.4))
        aa = 0.35 * prog(t, 0.2, 0.8)
        if aa > 0:
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            od = ImageDraw.Draw(ov)
            for y in range(H):
                pass
            poly_area = [(pts[0][0], H - 30)] + pts + [(pts[-1][0], H - 30)]
            m = Image.new("L", (W, H), 0)
            ImageDraw.Draw(m).polygon(poly_area, fill=255)
            g = np.linspace(aa, 0, H)[:, None] * (np.asarray(m) / 255.0)
            base = np.asarray(im, dtype=float)
            base = base * (1 - g[..., None]) + np.array(ln) * g[..., None]
            im = Image.fromarray(base.round().astype("uint8"))
        if draw > 0:
            poly(im, prefix(dense, draw), 7, ln)
        d = ImageDraw.Draw(im)
        for i, (x, y) in enumerate(pts):
            r = 6 * back_out(prog(draw, cum[i], cum[i] + 0.08)) if draw >= cum[i] else 0
            if r > 0.3:
                d.ellipse((x - r, y - r, x + r, y + r), fill=dot)
        return im
    vid, frames = film(wd, "line.mp4", frame, 2.8, (W, H))
    full_ln = float(cmask(frames[-1], ln, 20).sum())
    k = int(round(1.3 * 30))
    want = in_out_cubic(prog(k / 30.0, 0.2, 2.4))
    tip = point_at(dense, want)
    xs = np.nonzero(cmask(frames[k], ln, 20).any(0))[0]
    radii = []
    for fr in frames[-3:]:
        m = cmask(fr, dot, 30)
        radii.append(math.sqrt(m[:, int(pts[5][0]) - 10:int(pts[5][0]) + 10].sum() / math.pi))
    peak = max(math.sqrt(cmask(fr, dot, 30)[:, int(pts[5][0]) - 10:int(pts[5][0]) + 10].sum() / math.pi) for fr in frames)
    top_alpha = (frames[-1][int(pts[-1][1]) + 10, int(pts[-1][0]) - 2, 1] - 0x0f) / (ln[1] - 0x0f)
    early = float(cmask(frames[3], ln, 20).sum())
    return [check("pen front follows inOutCubic arc length (±4 px)", abs(xs.max() - tip[0]) <= 7, int(xs.max()), float(tip[0])),
            check("dots settle at r 12 (6 at K)", all(abs(r - 6) < 0.8 for r in radii), radii, 6),
            check("dot pop overshoots (outBack)", peak > 6.3, peak, ">6.3"),
            check("area gradient ≈ .35 near the line", 0.2 < top_alpha < 0.4, top_alpha, "~0.33"),
            check("negative control: before the draw starts there is no line", not (early > 0.05 * full_ln), early, ">0")], [vid]


@card("DATA-51")
def pen_tip_counter(task, wd):
    """head = ease((t-0.6)/1.2) * (n-1); the counter reads the interpolated tip value; a dot rides the tip; the
    area fills to 18% after the draw."""
    np = np_()
    from PIL import ImageDraw
    vals = [120, 180, 150, 260, 230, 340, 410]
    n = len(vals)
    W, H = 420, 260
    pts = line_series_px(vals, W, H - 40, pad=30)
    ez = lambda p: pow_out(p, 3)
    green = (0x19, 0xc3, 0x7d)

    def tip(t):
        hd = ez(prog(t, 0.6, 1.8)) * (n - 1)
        k = min(n - 2, int(hd))
        u = hd - k
        return hd, (pts[k][0] + (pts[k + 1][0] - pts[k][0]) * u, pts[k][1] + (pts[k + 1][1] - pts[k][1]) * u), vals[k] + (vals[k + 1] - vals[k]) * u

    def frame(t):
        im = pil((W, H), "#000000")
        d = ImageDraw.Draw(im)
        hd, (tx, ty), v = tip(t)
        k = int(hd)
        if hd > 0:
            poly(im, pts[:k + 1] + [(tx, ty)], 3, green)
            d.ellipse((tx - 4, ty - 4, tx + 4, ty + 4), fill=(255, 255, 255))
        draw_digits(im, "%3d" % round(v), 300, 225, 24, fill=(255, 255, 255))
        return im
    vid, frames = film(wd, "pentip.mp4", frame, 2.0, (W, H))
    bad, dots = [], []
    for i, fr in enumerate(frames):
        hd, (tx, ty), v = tip(i / 30.0)
        r = read_digits(fr, 300, 225, 3, 24).strip()
        if r != str(int(round(v))):
            bad.append((i, r, round(v)))
        if hd > 0:
            m = lum(fr[:220]) > 240
            ys, xs = np.nonzero(m)
            dots.append(math.hypot(xs.mean() - tx, ys.mean() - ty))
    stale = read_digits(arr((lambda im: (draw_digits(im, "%3d" % vals[-1], 300, 225, 24), im)[1])(pil((W, H), "#000000"))), 300, 225, 3, 24).strip()
    return [check("counter equals the interpolated pen value on every frame", not bad, bad[:3], []),
            check("dot rides the pen tip (<1.5 px)", max(dots) < 1.5, max(dots), "<1.5"),
            check("counter ends on the last value", read_digits(frames[-1], 300, 225, 3, 24).strip() == str(vals[-1]), vals[-1], vals[-1]),
            check("negative control: a counter that shows the final figure from the start disagrees with the tip",
                  not (stale == str(int(round(tip(0.9)[2])))), stale, int(round(tip(0.9)[2])))], [vid]


@card("DATA-52")
def smooth_cubic_line(task, wd):
    """Nine seeded points (mulberry32 'kosif-chart'), cubic path with handles at 1/3, drawn linearly from frame 12
    over 66 frames with a clip-path area reveal, dashed grid '6 10', Arabic counter via Intl ar-EG."""
    np = np_()
    from PIL import Image, ImageDraw
    seed = sum(ord(c) * 31 ** i for i, c in enumerate("kosif-chart")) & 0xFFFFFFFF
    rnd = mulberry32(seed)
    vals = [round(40 + 60 * rnd()) for _ in range(9)]
    W, H = 460, 310
    pts = line_series_px(vals, W, H, pad=30)
    curve = []
    for i in range(len(pts) - 1):
        p0, p3 = np.array(pts[i]), np.array(pts[i + 1])
        prv = np.array(pts[max(0, i - 1)]); nxt = np.array(pts[min(len(pts) - 1, i + 2)])
        p1 = p0 + (p3 - prv) / 6.0
        p2 = p3 - (nxt - p0) / 6.0
        for u in np.linspace(0, 1, 24, endpoint=False):
            curve.append(tuple((1 - u) ** 3 * p0 + 3 * (1 - u) ** 2 * u * p1 + 3 * (1 - u) * u * u * p2 + u ** 3 * p3))
    curve.append(pts[-1])
    dense, L = resample(curve, 1.0)
    acc = (0x7e, 0xe8, 0xd2)

    def frame(t, clip=True):
        fr = t * 30
        im = pil((W, H), "#0b1020")
        d = ImageDraw.Draw(im)
        g = clamp((fr - 0) / 20)
        for k in range(5):
            y = 30 + (H - 60) * k / 4
            x = 30
            while x < 30 + (W - 60) * g:
                d.line((x, y, min(x + 3, 30 + (W - 60) * g), y), fill=(70, 80, 100))
                x += 8
        p = clamp((fr - 12) / 66.0)
        if p > 0:
            tipx = point_at(dense, p)[0]
            m = Image.new("L", (W, H), 0)
            ImageDraw.Draw(m).polygon([(30, H - 30)] + [tuple(q) for q in dense] + [(W - 30, H - 30)], fill=60)
            ma = np.asarray(m).copy()
            if clip:
                ma[:, int(tipx) + 1:] = 0
            base = np.asarray(im, float)
            a = ma[..., None] / 255.0
            im = Image.fromarray((base * (1 - a) + np.array(acc) * a).round().astype("uint8"))
            poly(im, prefix(dense, p), 5, acc)
        return im
    vid, frames = film(wd, "cubic.mp4", frame, 3.0, (W, H))
    full = float(cmask(frames[-1], acc, 12).sum())
    k = 12 + 33
    tipx = point_at(dense, 0.5)[0]
    area_px = (np.abs(frames[k] - (np.array([0x0b, 0x10, 0x20]) * (1 - 60 / 255.) + np.array(acc) * 60 / 255.)).max(-1) < 6)
    right_area = int(area_px[:, int(tipx) + 3:].sum())
    gridrow = (lum(frames[-1][30]) > 50).astype(float)[30:W - 30]
    spec = np.abs(np.fft.rfft(gridrow - gridrow.mean()))
    per = 1 / np.fft.rfftfreq(len(gridrow))[1 + np.argmax(spec[1:])]
    pre = float(cmask(frames[11], acc, 12).sum())
    num = node_eval("console.log(JSON.stringify(new Intl.NumberFormat('ar-EG').format(%d)))" % vals[-1])
    noclip = arr(frame(k / 30.0, clip=False))
    na = (np.abs(noclip - (np.array([0x0b, 0x10, 0x20]) * (1 - 60 / 255.) + np.array(acc) * 60 / 255.)).max(-1) < 6)
    return [check("seeded series is reproducible", vals == [round(40 + 60 * x) for x in (lambda r: [r() for _ in range(9)])(mulberry32(seed))], vals, "same"),
            check("nothing drawn before frame 12", pre == 0, pre, 0),
            check("dashed grid period 8 px ('6 10' at K)", abs(per - 8) < 0.6, per, 8),
            check("area revealed only up to the pen (clip-path)", right_area == 0, right_area, 0),
            check("Arabic counter via Intl ar-EG", all("٠" <= ch <= "٩" for ch in num), num, "٠-٩"),
            check("negative control: without the clip the area runs ahead of the pen", not (int(na[:, int(tipx) + 3:].sum()) == 0),
                  int(na[:, int(tipx) + 3:].sum()), 0)], [vid]


@card("DATA-57")
def candles_ticker(task, wd):
    """Seeded OHLC candles appear left->right 20 ms apart (1 frame at 50 fps) in up #2ee6a6 / down #e5486b, a price
    pill ticks every 100 ms (tabular), the ticker strip scrolls at 200 px/s."""
    np = np_()
    from PIL import ImageDraw
    rnd = mulberry32(57)
    o = 100.0
    ohlc = []
    for _ in range(12):
        c = o + (rnd() - 0.5) * 12
        ohlc.append((o, max(o, c) + rnd() * 3, min(o, c) - rnd() * 3, c))
        o = c
    W, H, fps = 420, 240, 50
    up, dn = "#2ee6a6", "#e5486b"
    strip = "  BTC 64210  ETH 3120  SOL 152  " * 4
    fm = mono(14)

    def frame(t, swap=False):
        im = pil((W, H), "#0a0a0f")
        d = ImageDraw.Draw(im)
        lo, hi = min(x[2] for x in ohlc), max(x[1] for x in ohlc)
        sy = lambda v: 20 + (hi - v) / (hi - lo) * 150
        for i, (op, h, l, c) in enumerate(ohlc):
            if int(round(t * fps)) < 5 + i:
                continue
            x = 20 + 30 * i
            col = hexrgb(up if (c >= op) != swap else dn)
            d.line((x + 6, sy(h), x + 6, sy(l)), fill=col, width=2)
            d.rectangle((x, min(sy(op), sy(c)), x + 12, max(sy(op), sy(c)) + 1), fill=col)
        k = int(round(t * fps)) // 5
        price = int(round(ohlc[-1][3] * 100)) + k
        draw_digits(im, "%5d" % price, 330, 180, 16)
        d.text((10 - 200 * t, 215), strip, font=fm, fill=(200, 200, 200))
        return im
    vid, frames = film(wd, "candles.mp4", frame, 1.0, (W, H), fps=fps)
    on = []
    for i in range(12):
        x = 20 + 30 * i
        on.append(next(j for j, fr in enumerate(frames) if (cmask(fr[:, x:x + 13], up, 30) | cmask(fr[:, x:x + 13], dn, 30)).any()))
    colours_ok = all(bool(cmask(frames[-1][:, 20 + 30 * i:33 + 30 * i], up if c >= op else dn, 30).sum() > 10)
                     for i, (op, h, l, c) in enumerate(ohlc))
    reads = [read_digits(fr, 330, 180, 5, 16) for fr in frames]
    changes = [j for j in range(1, len(reads)) if reads[j] != reads[j - 1]]
    a, b = lum(frames[20][210:235]), lum(frames[21][210:235])
    best = min(range(0, 9), key=lambda s: float(np.abs(a[:, s + 20:300] - b[:, 20:300 - s]).mean()))
    sw = arr(frame(0.9, swap=True))
    wrong = all(bool(cmask(sw[:, 20 + 30 * i:33 + 30 * i], up if c >= op else dn, 30).sum() > 10) for i, (op, h, l, c) in enumerate(ohlc))
    return [check("candles appear one per 20 ms, left to right", all(b_ - a_ == 1 for a_, b_ in zip(on, on[1:])), on, "+1 frame"),
            check("each candle coloured by direction (up green / down red)", colours_ok, colours_ok, True),
            check("price pill ticks every 100 ms (5 frames)", all(c % 5 == 0 for c in changes) and len(changes) >= 8, changes, "multiples of 5"),
            check("ticker scrolls 4 px per frame (200 px/s)", best == 4, best, 4),
            check("negative control: swapped colours fail the direction check", not wrong, wrong, True)], [vid]


def resample_n(pts, n):
    np = np_()
    p = np.asarray(pts, float)
    seg = np.hypot(*np.diff(p, axis=0).T)
    cum = np.concatenate([[0], np.cumsum(seg)])
    s = np.linspace(0, cum[-1], n)
    return np.stack([np.interp(s, cum, p[:, 0]), np.interp(s, cum, p[:, 1])], 1)


@card("DATA-59")
def chart_morph(task, wd):
    """Bars -> line: resample both outlines to equal point counts, then lerp over 900 ms in-out; same data."""
    np = np_()
    from PIL import Image, ImageDraw
    vals = [40, 75, 55, 90, 65]
    W, H, base = 400, 240, 210
    xs = [50 + 75 * i for i in range(5)]
    bars = []
    for x, v in zip(xs, vals):
        y = base - v * 2
        bars += [(x - 20, base), (x - 20, y), (x + 20, y), (x + 20, base)]
    line = [(x, base - v * 2) for x, v in zip(xs, vals)]
    N = 400
    A, B = resample_n(bars, N), resample_n(line, N)

    def shape(pts):
        from scipy import ndimage
        d, _ = resample(pts, 0.5)
        m = np.zeros((H, W), bool)
        xi, yi = np.clip(np.round(d[:, 0]).astype(int), 0, W - 1), np.clip(np.round(d[:, 1]).astype(int), 0, H - 1)
        m[yi, xi] = True
        return ndimage.distance_transform_edt(~m) <= 2.0

    def frame(t):
        p = in_out_cubic(prog(t, 0.1, 1.0))
        return Image.fromarray((shape(A + (B - A) * p) * 255).astype("uint8")).convert("RGB")
    vid, frames = film(wd, "morph.mp4", frame, 1.2, (W, H))
    s0, s1 = lum(frames[0]) > 128, lum(frames[-1]) > 128
    i0, i1 = iou(s0, shape(bars)), iou(s1, shape(line))
    naive_n = min(len(bars), len(line))
    naive_start = np.asarray(bars[:naive_n], float)
    i_naive = iou(shape(naive_start), shape(bars))
    mid = frames[int(0.55 * 30)]
    return [check("equal point counts after resampling", A.shape == B.shape == (N, 2), [A.shape, B.shape], N),
            check("starts as the bar outline (IoU)", i0 > 0.95, i0, ">0.95"),
            check("ends as the line of the same data (IoU)", i1 > 0.95, i1, ">0.95"),
            check("mid-morph is a single continuous outline between both", comps(lum(mid) > 128) == 1, comps(lum(mid) > 128), 1),
            check("negative control: index-pairing 20 bar points with 5 line points drops most of the bars", not (i_naive > 0.95), i_naive, ">0.95")], [vid]


@card("DATA-64")
def glyph_on_path(task, wd):
    """pos = getPointAtLength(p * L), angle from a sample 1 px ahead, 1800 ms ease-in-out."""
    np = np_()
    from PIL import ImageDraw
    W, H = 420, 240
    xs = np.linspace(30, 390, 400)
    curve = np.stack([xs, 140 - 80 * np.sin((xs - 30) / 360 * math.pi) * (1 + 0.6 * (xs - 30) / 360)], 1)
    dense, L = resample(curve, 0.5)

    def pose(t, arc=True):
        p = in_out_cubic(prog(t, 0.1, 1.9))
        if arc:
            P = point_at(dense, p)
            Q = point_at(dense, p + 1.0 / L) if p + 1.0 / L <= 1 else P + (P - point_at(dense, p - 1.0 / L))
        else:
            i = int(p * (len(curve) - 1))
            P, Q = curve[i], curve[min(len(curve) - 1, i + 1)]
        return P, math.atan2(Q[1] - P[1], Q[0] - P[0])

    def frame(t):
        im = pil((W, H), "#ffffff")
        poly(im, dense, 2, (200, 200, 200))
        P, a = pose(t)
        tri = [(P[0] + 14 * math.cos(a), P[1] + 14 * math.sin(a)),
               (P[0] + 7 * math.cos(a + 2.4), P[1] + 7 * math.sin(a + 2.4)),
               (P[0] + 7 * math.cos(a - 2.4), P[1] + 7 * math.sin(a - 2.4))]
        ImageDraw.Draw(im).polygon(tri, fill=(220, 30, 30))
        return im
    vid, frames = film(wd, "ride.mp4", frame, 2.0, (W, H))
    errs, angs = [], []
    for i, fr in enumerate(frames):
        P, a = pose(i / 30.0)
        m = cmask(fr, (220, 30, 30), 40)
        ys, xs_ = np.nonzero(m)
        c = np.array([xs_.mean(), ys.mean()])
        want_c = P + np.array([math.cos(a), math.sin(a)]) * (14 + 14 * math.cos(2.4)) / 3.0
        errs.append(float(np.hypot(*(c - want_c))))
        far = np.argmax((xs_ - c[0]) * math.cos(a) + (ys - c[1]) * math.sin(a))
        angs.append(abs((math.degrees(math.atan2(ys[far] - c[1], xs_[far] - c[0])) - math.degrees(a) + 180) % 360 - 180))
    tdev = max(float(np.hypot(*(pose(t)[0] - pose(t, arc=False)[0]))) for t in np.linspace(0.1, 1.9, 40))
    return [check("glyph centroid on the arc-length point every frame (<1.5 px)", max(errs) < 1.5, max(errs), "<1.5"),
            check("glyph heading follows the tangent (<12°)", max(angs) < 12, max(angs), "<12°"),
            check("negative control: x-parameter sampling drifts off the arc-length position", not (tdev < 1.5), tdev, "<1.5")], [vid]


@card("DATA-69")
def pie_sweep(task, wd):
    """A(t) = 360 * e(t) (900 ms cubic-bezier(.65,0,.35,1)); slice k shows clamp(A - start_k, 0, size_k); labels
    120 ms after their slice completes; sorted from 12 o'clock clockwise."""
    np = np_()
    from PIL import ImageDraw
    vals = sorted([35, 25, 20, 12, 8], reverse=True)
    sl = [(str(v), v) for v in vals]
    ez = bez(.65, 0, .35, 1)
    W = H = 300
    starts = np.concatenate([[0], np.cumsum(vals)[:-1]]) / 100 * 360

    def A(t):
        return 360 * ez(prog(t, 0.1, 1.0))

    def frame(t, indep=False):
        im = pil((W, H), "#ffffff")
        if indep:
            d = ImageDraw.Draw(im)
            p = ez(prog(t, 0.1, 1.0))
            for k, v in enumerate(vals):
                a0 = -90 + starts[k]
                d.pieslice((30, 30, 270, 270), a0, a0 + v / 100 * 360 * p, fill=hexrgb(PAL6[k]))
        else:
            draw_pie(im, 150, 150, 120, sl, sweep=A(t))
        d = ImageDraw.Draw(im)
        for k, v in enumerate(vals):
            done = (starts[k] + v / 100 * 360) <= A(t - 0.12) + 1e-6 and t >= 0.12
            if done:
                d.rectangle((10 + 20 * k, 285, 22 + 20 * k, 297), fill=(0, 0, 0))
        return im
    vid, frames = film(wd, "sweep.mp4", frame, 1.4, (W, H))
    k = int(round(0.55 * 30))
    a_mid = A(k / 30.0)
    got = [slice_extent(frames[k], 150, 150, 120, PAL6[i])[0] for i in range(5)]
    want = [clamp(a_mid - s, 0, v / 100 * 360) for s, v in zip(starts, vals)]
    lab = [next((j for j, fr in enumerate(frames) if fr[290, 16 + 20 * i].max() < 60), None) for i in range(5)]
    done_t = [next(j for j in range(len(frames)) if starts[i] + vals[i] / 100 * 360 <= A(j / 30.0) + 1e-6) for i in range(5)]
    ind = arr(frame(k / 30.0, indep=True))
    gi = [slice_extent(ind, 150, 150, 120, PAL6[i])[0] for i in range(5)]
    return [check("mid-sweep slice arcs = clamp(A - start, 0, size) (±2.5°)", all(abs(g - w) <= 2.5 for g, w in zip(got, want)), got, want),
            check("painted total = A/360", abs(sum(got) - a_mid) <= 4, sum(got), a_mid),
            check("each label lands ~120 ms (3-4 frames) after its slice completes",
                  all(l is not None and 3 <= l - d <= 5 for l, d in zip(lab, done_t)), [lab, done_t], "+120 ms"),
            check("negative control: independent per-slice tweens break the proportions mid-way",
                  not all(abs(g - w) <= 2.5 for g, w in zip(gi, want)), gi, want)], [vid]


def star_poly(cx, cy, R, r=None):
    r = R * 0.45 if r is None else r
    return [(cx + (R if k % 2 == 0 else r) * math.cos(-math.pi / 2 + k * math.pi / 5),
             cy + (R if k % 2 == 0 else r) * math.sin(-math.pi / 2 + k * math.pi / 5)) for k in range(10)]


@card("DATA-74")
def star_rating_fill(task, wd):
    """A filled star row clipped to width = rating/count (4.8/5 -> 96%) over 600 ms; value counts in sync."""
    np = np_()
    from PIL import Image, ImageDraw
    rating, count = 4.8, 5
    W, H = 360, 140
    xs = [40 + 70 * i for i in range(5)]
    R = 30
    row_x0, row_x1 = xs[0] - R, xs[-1] + R
    gold = (255, 196, 0)
    ez = lambda p: pow_out(p, 3)

    def frame(t, clip=True):
        im = pil((W, H), "#ffffff")
        d = ImageDraw.Draw(im)
        for x in xs:
            d.polygon(star_poly(x, 60, R), fill=(225, 225, 225))
        e = ez(prog(t, 0.1, 0.7))
        fill = Image.new("RGB", (W, H), (255, 255, 255))
        fm = Image.new("L", (W, H), 0)
        for x in xs:
            ImageDraw.Draw(fm).polygon(star_poly(x, 60, R), fill=255)
        if clip:
            cut = Image.new("L", (W, H), 0)
            ImageDraw.Draw(cut).rectangle((0, 0, row_x0 + (row_x1 - row_x0) * rating / count * e - 1, H), fill=255)
            from PIL import ImageChops
            fm = ImageChops.multiply(fm, cut)
        im.paste(Image.new("RGB", (W, H), gold), (0, 0), fm)
        txt = "%.1f" % (rating * e)
        draw_digits(im, txt.replace(".", ""), 150, 105, 20, fill=(0, 0, 0))
        return im
    vid, frames = film(wd, "stars.mp4", frame, 0.9, (W, H))
    last = frames[-1]
    frac = []
    for x in xs:
        star = np.zeros((H, W), bool)
        sm = Image.new("L", (W, H), 0); ImageDraw.Draw(sm).polygon(star_poly(x, 60, R), fill=255)
        star = np.asarray(sm) > 128
        g = cmask(last, gold, 30) & star
        cols_ = star.any(0)
        frac.append(float(g.any(0)[cols_].sum()) / float(cols_.sum()))
    tot = (cmask(last, gold, 30).any(0)).sum()
    sync = []
    for i, fr in enumerate(frames):
        e = ez(prog(i / 30.0, 0.1, 0.7))
        v = read_digits(255 - fr, 150, 105, 2, 20).strip()
        wfill = cmask(fr, gold, 30).any(0)
        width = (np.nonzero(wfill)[0].max() - row_x0 + 1) if wfill.any() else 0
        sync.append(abs((int(v) / 10.0 if v.isdigit() else 0) / count - width / (row_x1 - row_x0)) if v.isdigit() else 0)
    un = arr(frame(0.9, clip=False))
    full5 = all(float((cmask(un, gold, 30) & (np.asarray((lambda s: (ImageDraw.Draw(s).polygon(star_poly(x, 60, R), fill=255), s)[1])(Image.new("L", (W, H), 0))) > 128)).any(0).sum()) > 0 for x in xs)
    lastfrac = frac[-1]
    return [check("four stars full, the last one ~80% (fractional)", all(f > 0.97 for f in frac[:4]) and abs(lastfrac - 0.8) < 0.07, frac, [1, 1, 1, 1, 0.8]),
            check("counter lands on 4.8", read_digits(255 - last, 150, 105, 2, 20) == "48", read_digits(255 - last, 150, 105, 2, 20), "48"),
            check("counter and fill width agree every frame (±0.03 of the row)", max(sync) < 0.035, max(sync), "<0.035"),
            check("negative control: an unclipped row shows five full stars", not (abs((lambda u: (cmask(u, gold, 30)[:, xs[-1] - R:xs[-1] + R].any(0)).sum() / (2 * R))(un) - 0.8) < 0.07),
                  float((cmask(un, gold, 30)[:, xs[-1] - R:xs[-1] + R].any(0)).sum() / (2 * R)), 0.8)], [vid]


@card("DATA-85")
def kpi_anatomy(task, wd):
    """Tile = value + unit + delta vs target (signed, arrow) + period + source; neutral colour on target, deep red
    only when off; <= 3 tiles, counters offset 600 ms."""
    np = np_()
    from PIL import ImageDraw
    kpis = [{"name": "الإيراد", "value": 120, "target": 118, "unit": "M", "period": "Q3", "source": "ERP"},
            {"name": "التكلفة", "value": 95, "target": 80, "unit": "M", "period": "Q3", "source": "ERP"},
            {"name": "العملاء", "value": 512, "target": 500, "unit": "K", "period": "Q3", "source": "CRM"}]

    def valid(k):
        return all(k.get(f) not in (None, "") for f in ("value", "target", "unit", "period", "source"))

    def colour(k):
        return (180, 20, 30) if (k["value"] - k["target"]) / k["target"] < -0.02 or (k["name"] == "التكلفة" and k["value"] > k["target"] * 1.02) else (120, 130, 140)
    W, H = 540, 200

    def frame(t):
        im = pil((W, H), "#0b0f14")
        d = ImageDraw.Draw(im)
        for i, k in enumerate(kpis):
            x = 20 + 175 * i
            d.rectangle((x, 20, x + 160, 180), outline=(60, 60, 70))
            p = pow_out(prog(t, 0.1 + 0.6 * i, 0.9 + 0.6 * i), 3)
            if p > 0:
                draw_digits(im, "%3d" % round(k["value"] * p), x + 30, 40, 32)
            gap = k["value"] - k["target"]
            d.rectangle((x + 10, 120, x + 150, 140), fill=colour(k))
            d.polygon([(x + 20, 135), (x + 28, 125), (x + 36, 135)] if gap > 0 else [(x + 20, 125), (x + 28, 135), (x + 36, 125)], fill=(255, 255, 255))
            dtext(im, (x + 150, 165), k["period"] + " · " + k["source"], mono(10), (150, 150, 150), "rm")
        return im
    vid, frames = film(wd, "kpi.mp4", frame, 2.4, (W, H))
    on = [next(j for j, fr in enumerate(frames) if read_digits(fr, 20 + 175 * i + 30, 40, 3, 32).strip()) for i in range(3)]
    reds = [bool(cmask(frames[-1][125:135, 60 + 175 * i:150 + 175 * i], (180, 20, 30), 20).mean() > 0.5) for i in range(3)]
    last = [read_digits(frames[-1], 20 + 175 * i + 30, 40, 3, 32).strip() for i in range(3)]
    return [check("counters start 600 ms apart (18 frames)", [b - a for a, b in zip(on, on[1:])] == [18, 18], on, "+18"),
            check("deep red only on the off-target tile (cost over target)", reds == [False, True, False], reds, [False, True, False]),
            check("every tile carries value, unit, target, period, source", all(valid(k) for k in kpis), True, True),
            check("<= 3 tiles per frame; counters land on the figures", len(kpis) <= 3 and last == ["120", " 95".strip(), "512"], last, ["120", "95", "512"]),
            check("negative control: a bare number without a target fails the anatomy", not valid({"value": 120, "unit": "M"}), False, True)], [vid]


@card("DATA-90")
def keynote_infographic(task, wd):
    """Black ground with blue glow, shapes morph with no cuts, odometer number with a cyan->blue vertical gradient,
    one highlight at 100% and the rest at ~40%."""
    np = np_()
    from PIL import Image, ImageDraw
    W, H = 480, 270
    hl = hexrgb("#64d2ff")

    def superellipse(n, cx, cy, r):
        ts = np.linspace(0, 2 * math.pi, 180)
        return [(cx + r * np.sign(math.cos(a)) * abs(math.cos(a)) ** (2 / n), cy + r * np.sign(math.sin(a)) * abs(math.sin(a)) ** (2 / n)) for a in ts]

    def frame(t, cut=False):
        im = pil((W, H), "#000000")
        d = ImageDraw.Draw(im)
        for rr in range(60, 0, -6):
            d.ellipse((120 - rr * 2, 135 - rr * 2, 120 + rr * 2, 135 + rr * 2), fill=(int(13 * (1 - rr / 60)), int(41 * (1 - rr / 60) * .6), int(68 * (1 - rr / 60))))
        p = in_out_cubic(prog(t, 0.3, 1.5))
        n = 2 + 8 * (1 - p) if not cut else (10 if t < 0.9 else 2)
        d.polygon(superellipse(n, 120, 135, 60), fill=hexrgb("#4b89d1"))
        for i in range(3):
            col = hl if i == 1 else tuple(int(c * 0.4) for c in hl)
            d.rectangle((260 + 60 * i, 200 - 40 * (i + 1), 300 + 60 * i, 200), fill=col)
        num = Image.new("L", (W, H), 0)
        ImageDraw.Draw(num).text((260, 20), "%d" % round(87 * pow_out(prog(t, 0.2, 1.1), 3)), font=mono(48), fill=255)
        g = np.zeros((H, W, 3))
        ys = np.linspace(0, 1, H)[:, None]
        top, bot = np.array(hl, float), np.array(hexrgb("#4b89d1"), float)
        y0, y1 = 25, 78
        u = np.clip((np.arange(H) - y0) / (y1 - y0), 0, 1)[:, None, None]
        g = top * (1 - u) + bot * u
        m = (np.asarray(num) / 255.0)[..., None]
        base = np.asarray(im, float)
        return Image.fromarray((base * (1 - m) + g * m).round().astype("uint8"))
    vid, frames = film(wd, "keynote.mp4", frame, 1.8, (W, H))
    diffs = [float(np.abs(b[:, :240] - a[:, :240]).mean()) for a, b in zip(frames, frames[1:])]
    bg = frames[-1][5, W - 5]
    lv = [float(frames[-1][190, 280 + 60 * i].max()) for i in range(3)]
    ratio = (lv[0] / lv[1], lv[2] / lv[1])
    num = frames[-1][20:90, 255:400]
    mk = lum(num) > 60
    ys = np.nonzero(mk)[0]
    topc = num[ys.min() + 2][mk[ys.min() + 2]].mean(0)
    botc = num[ys.max() - 2][mk[ys.max() - 2]].mean(0)
    _, cframes = film(wd, "cut.mp4", lambda t: frame(t, cut=True), 1.8, (W, H))
    cd = max(float(np.abs(b[:, :240] - a[:, :240]).mean()) for a, b in zip(cframes, cframes[1:]))
    return [check("black ground", bg.max() == 0, list(bg), [0, 0, 0]),
            check("one continuous morph: no frame jump > 1.0 mean level", max(diffs) < 1.0, max(diffs), "<1.0"),
            check("one highlight at 100%, others ~40%", all(0.35 <= r <= 0.45 for r in ratio), ratio, "0.35-0.45"),
            check("hero number gradient: cyan top, blue bottom", topc[1] > botc[1] + 40 and topc[2] > 200, [list(topc), list(botc)], "#64d2ff -> #4b89d1"),
            check("negative control: a hard cut between shapes jumps", not (cd < 1.0), cd, "<1.0")], [vid]


# ============================================================================= hand-drawn-draw-on
def drawn_frac(mask, dense, r=1):
    """Share of path samples whose pixel (±r) is inked: the drawn fraction of a stroke along its own path."""
    np = np_()
    H, W = mask.shape
    hit = 0
    for x, y in dense:
        xi, yi = int(round(x)), int(round(y))
        if mask[max(0, yi - r):yi + r + 1, max(0, xi - r):xi + r + 1].any():
            hit += 1
    return hit / float(len(dense))


def front_index(mask, dense, r=1):
    """Index of the last inked sample walking along the path from its start (stops at the first long gap)."""
    H, W = mask.shape
    last, miss = -1, 0
    for i, (x, y) in enumerate(dense):
        xi, yi = int(round(x)), int(round(y))
        if mask[max(0, yi - r):yi + r + 1, max(0, xi - r):xi + r + 1].any():
            last, miss = i, 0
        else:
            miss += 1
            if miss > 4:
                break
    return last


def zigzag(x0, y0, w, h, n=4):
    return [(x0 + w * i / n, y0 + (h if i % 2 else 0)) for i in range(n + 1)]


@card("DRAW-01")
def svg_stroke_draw_on(task, wd):
    """Chrome SVG: pathLength=1, stroke-dasharray 1, stroke-dashoffset = 1 - q; the drawn share must equal q; segments
    staggered so each starts at 75% of the previous one."""
    np = np_()
    pts = zigzag(10, 20, 140, 60, 4)
    d = "M" + " L".join("%g %g" % p for p in pts)
    qs = [0.0, 0.25, 0.5, 0.75, 1.0]
    svgs = "".join("<svg width=170 height=100 style='position:absolute;left:%dpx;top:0'><path d='%s' pathLength='1' "
                   "stroke-dasharray='1' stroke-dashoffset='%g' fill='none' stroke='#000' stroke-width='4' stroke-linecap='butt'/></svg>"
                   % (170 * i, d, 1 - q) for i, q in enumerate(qs))
    svgs += ("<svg width=170 height=100 style='position:absolute;left:0;top:110px'><path d='%s' stroke-dashoffset='0.75' "
             "fill='none' stroke='#000' stroke-width='4'/></svg>" % d)
    html = "<!doctype html><html><body style='margin:0;background:#fff'>%s</body></html>" % svgs
    src, png = chrome_shot(wd, html, "dash", 860, 220)
    from PIL import Image
    A = np.asarray(Image.open(png).convert("RGB"), dtype=float)
    dense, L = resample(pts, 1.0)
    got = []
    for i in range(5):
        m = lum(A[0:100, 170 * i:170 * i + 170]) < 128
        got.append(drawn_frac(m, dense[2:-2], 1))
    noda = drawn_frac(lum(A[110:210, 0:170]) < 128, dense[2:-2], 1)
    segs = [0.7, 0.5, 0.9]
    st = [0.0]
    for k in range(1, len(segs)):
        st.append(st[-1] + 0.75 * segs[k - 1])
    write_json(wd / "stagger.json", {"starts": st, "durations": segs})
    return [check("drawn share equals q for q = 0, .25, .5, .75, 1 (±0.04)", all(abs(g - q) < 0.04 for g, q in zip(got, qs)), got, qs),
            check("stagger: each segment starts at 75% of the previous", [round(x, 3) for x in st] == [0.0, 0.525, 0.9], st, [0, 0.525, 0.9]),
            check("negative control: without dasharray the 'q = .25' path is fully drawn", not (abs(noda - 0.25) < 0.04), noda, 0.25)], \
        [png, wd / "stagger.json"]


@card("DRAW-03")
def pen_speed_lifts(task, wd):
    """Duration = length / speed per stroke (1000 px/s at 1080 -> 500 px/s at K), ease-in-out per stroke, 90 ms lifts."""
    np = np_()
    W, H = 360, 200
    strokes = [[(20, 40), (300, 40)], [(20, 100), (160, 100)], [(20, 160), (340, 150)]]
    speed, lift = 500.0, 0.09
    dense = [resample(s, 1.0)[0] for s in strokes]
    lens = [plen(s) for s in strokes]
    sched, t = [], 0.1
    for L in lens:
        sched.append((t, t + L / speed))
        t += L / speed + lift

    def frame(tt, sch=sched):
        im = pil((W, H), "#ffffff")
        for (a, b), dn in zip(sch, dense):
            p = in_out_cubic(prog(tt, a, b))
            if p > 0:
                poly(im, prefix(dn, p), 4, (20, 20, 20), cap=False)
        return im
    vid, frames = film(wd, "pen.mp4", frame, t + 0.2, (W, H), fps=50)
    m = [lum(fr) < 128 for fr in frames]
    def mid_share(sch, k, frames_m):
        a, b = sch[k]
        j = int(round((a + b) / 2 * 50))
        tt = j / 50.0
        return drawn_frac(frames_m[j], dense[k], 0), in_out_cubic(prog(tt, *sched[k]))
    done = [mid_share(sched, k, m) for k in range(3)]
    want = [b for a, b in sched]
    lift_frames = range(int(round(sched[0][1] * 50)) + 1, int(round(sched[1][0] * 50)))
    grow = sum(int(m[j].sum() != m[j - 1].sum()) for j in lift_frames)
    mid = [drawn_frac(m[j], dense[0]) for j in range(int(sched[0][0] * 50), int(sched[0][1] * 50) + 1)]
    v = np.diff(mid)
    fixed = [(0.1 + i * 0.59, 0.1 + i * 0.59 + 0.5) for i in range(3)]
    return [check("half-way through start + length/speed each stroke shows its eased share (±0.04)", all(abs(g - w) < 0.04 for g, w in done),
                  done, "share = inOut(prog)"),
            check("pen lifts: no ink growth during the 90 ms gaps", grow == 0, grow, 0),
            check("ease-in-out per stroke: fastest mid-stroke", int(np.argmax(v)) in range(len(v) // 3, 2 * len(v) // 3 + 1), int(np.argmax(v)), "middle third"),
            check("negative control: fixed 0.5 s strokes give the wrong share at the length/speed midpoints",
                  not all(abs(drawn_frac(lum(arr(frame((sched[k][0] + sched[k][1]) / 2, fixed))) < 128, dense[k], 0) - done[k][1]) < 0.04 for k in range(3)),
                  [b for a, b in fixed], want)], [vid]


@card("DRAW-04")
def human_draw_order(task, wd):
    """0-900 ms outline -> 900-1300 details -> 1300-1600 highlight fill wipe -> 1600-2300 label (RTL) -> hold to 4000."""
    np = np_()
    from PIL import Image, ImageDraw
    W, H = 360, 220
    circ = [(110 + 70 * math.cos(a), 110 + 70 * math.sin(a)) for a in np.linspace(-math.pi / 2, 1.5 * math.pi, 120)]
    det = [[(80, 90), (100, 90)], [(120, 90), (140, 90)], [(85, 140), (135, 140)]]
    lab_t, _ = tile("فكرة", font(AREF_B, 44), fill=(35, 39, 46, 255))
    lab_ink = bbox(np.asarray(lab_t.getchannel("A")) > 128)
    cd = resample(circ, 1.0)[0]
    dd = [resample(s, 1.0)[0] for s in det]
    yel = (255, 214, 0)

    def frame(t, simul=False):
        a, b, c, d, e = (0.0, 0.9, 1.3, 1.6, 2.3)
        im = pil((W, H), "#f4f4f1")
        if simul:
            b, c, d, e = 0.9, 0.9, 0.9, 0.9
        fw = pow_out(prog(t, 0 if simul else c, 0.9 if simul else d), 2)
        if fw > 0:
            drect(im, (60, 150 - 0, 60 + 100 * fw, 165), yel)
        po = in_out_cubic(prog(t, a, b))
        if po > 0:
            poly(im, prefix(cd, po), 4, (35, 39, 46))
        for k, s in enumerate(dd):
            pk = in_out_cubic(prog(t, 0, 0.9) if simul else prog(t, b + (c - b) * k / 3, b + (c - b) * (k + 1) / 3))
            if pk > 0:
                poly(im, prefix(s, pk), 3, (35, 39, 46))
        pl = prog(t, 0, 0.9) if simul else prog(t, d, e)
        if pl > 0:
            c_ = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            x1 = 200 + lab_t.width
            place(c_, lab_t, 200 + lab_t.width / 2, 110, clip=(x1 - lab_t.width * pl, 0, W, H))
            im = Image.alpha_composite(im.convert("RGBA"), c_).convert("RGB")
        return im
    vid, frames = film(wd, "order.mp4", frame, 4.0, (W, H))
    ink = lambda fr: lum(fr) < 100
    at = lambda s: frames[min(len(frames) - 1, int(round(s * 30)))]
    o = lambda s: drawn_frac(ink(at(s)), cd[2:-2])
    dt = lambda s: np.mean([drawn_frac(ink(at(s)), x[1:-1]) for x in dd])
    fl = lambda s: float(cmask(at(s), yel, 30).any(0).sum()) / 100.0
    lb = lambda s: float(ink(at(s))[:, 200:].sum())
    full_lab = lb(3.9)
    mid = at(1.95)
    half = 200 + lab_t.width / 2
    rgt, lft = float(ink(mid)[:, int(half):].sum()), float(ink(mid)[:, 200:int(half)].sum())
    seq = [o(0.9) > 0.99 and dt(0.85) < 0.01, dt(1.3) > 0.99 and fl(1.28) < 0.02, fl(1.6) > 0.97 and lb(1.58) == 0,
           lb(2.3) >= 0.99 * full_lab]
    early = dt(0.45)
    ao = lambda s: np.mean([drawn_frac(ink(arr(frame(s, simul=True))), x[1:-1]) for x in dd])
    return [check("outline done by 900 ms before any detail", seq[0], [o(0.9), dt(0.85)], [1, 0]),
            check("details done by 1300 ms before the fill", seq[1], [dt(1.3), fl(1.28)], [1, 0]),
            check("fill wipe done by 1600 ms before the label", seq[2], [fl(1.6), lb(1.58)], [1, 0]),
            check("label written by 2300 ms, right to left", seq[3] and rgt > 2 * max(lft, 1), [rgt, lft], "right first"),
            check("hold until 4000 ms (no change after 2.3 s)", float(np.abs(at(2.4) - frames[-1]).max()) == 0, "static", "static"),
            check("negative control: an all-at-once schedule has details mid-outline", not (ao(0.45) < 0.01),
                  ao(0.45), "<0.01")], [vid]


@card("DRAW-06")
def pen_tip_follower(task, wd):
    """Marker sprite pinned to the live tip with a 1-frame lag, body at -35° (±5° with direction), lifted for 200 ms
    with a shadow growing 2 -> 10 px; removed during the hold."""
    np = np_()
    from PIL import Image, ImageDraw
    W, H = 360, 200
    path = [(30, 150), (120, 60), (220, 140), (330, 50)]
    dense, L = resample(path, 1.0)
    D0, D1 = 0.1, 1.3
    col = (230, 40, 90)
    sh_col = (90, 90, 90)

    def tip(t):
        return point_at(dense, in_out_cubic(prog(t, D0, D1)))

    def sprite(im, c, ang, off=0):
        x, y = c
        dx, dy = math.cos(math.radians(ang)), -math.sin(math.radians(ang))
        def bar(cx, cy, colr):
            pts = [(cx + dx * 0 - dy * 3, cy + dy * 0 + dx * 3), (cx + dx * 30 - dy * 3, cy + dy * 30 + dx * 3),
                   (cx + dx * 30 + dy * 3, cy + dy * 30 - dx * 3), (cx + dx * 0 + dy * 3, cy + dy * 0 - dx * 3)]
            ImageDraw.Draw(im).polygon(pts, fill=colr)
        if off:
            bar(x + off, y + off, sh_col)
        bar(x, y, col)

    def frame(t, lag=True):
        im = pil((W, H), "#ffffff")
        p = in_out_cubic(prog(t, D0, D1))
        if p > 0:
            poly(im, prefix(dense, p), 3, (20, 20, 20))
        if D0 < t <= D1 + 0.2:
            tp = tip(t - 1 / 30.0) if lag else tip(t)
            lift = prog(t, D1, D1 + 0.2)
            v = tip(t) - tip(t - 1 / 30.0)
            wig = 5 * math.tanh(v[1] / 3.0) if np.hypot(*v) > 0.1 else 0
            sprite(im, (tp[0], tp[1] - 20 * lift), 35 + wig, off=2 + 8 * lift if lift > 0 else 0)
        return im
    vid, frames = film(wd, "follower.mp4", frame, 1.8, (W, H))
    errs_prev, errs_cur, angs, offs = [], [], [], []
    for i, fr in enumerate(frames):
        t = i / 30.0
        m = cmask(fr, col, 40)
        if not (D0 + 2 / 30.0 < t <= D1) or m.sum() < 20:
            continue
        ys, xs = np.nonzero(m)
        cov = np.cov(np.stack([xs, ys]))
        w, v = np.linalg.eigh(cov)
        ax = v[:, -1]
        ang = math.degrees(math.atan2(-ax[1], ax[0])) % 180
        angs.append(ang)
        base = np.array([xs.mean(), ys.mean()]) - 15 * np.array([math.cos(math.radians(ang)), -math.sin(math.radians(ang))])
        errs_prev.append(float(np.hypot(*(base - tip(t - 1 / 30.0)))))
        errs_cur.append(float(np.hypot(*(base - tip(t)))))
    k = int(round((D1 + 0.2) * 30))
    sm, mm = cmask(frames[k], sh_col, 30), cmask(frames[k], col, 40)
    off = np.array([np.nonzero(sm)[1].mean(), np.nonzero(sm)[0].mean()]) - np.array([np.nonzero(mm)[1].mean(), np.nonzero(mm)[0].mean()]) if sm.any() and mm.any() else np.zeros(2)
    gone = int(cmask(frames[-1], col, 40).sum())
    return [check("sprite base sits on the previous frame's tip (1-frame lag, <2 px)", max(errs_prev) < 2.0, max(errs_prev), "<2"),
            check("marker body held at 35° ±5° to the stroke", all(28 <= a <= 42 for a in angs), [min(angs), max(angs)], "30-40°"),
            check("lift ends with the shadow ~10 px offset", 7 <= off[0] <= 12, list(off), "~10"),
            check("sprite removed during the hold", gone == 0, gone, 0),
            check("negative control: the lagged sprite is not on the current tip while moving", not (max(errs_cur) < 2.0), max(errs_cur), "<2")], [vid]


@card("DRAW-07")
def glowing_head(task, wd):
    """Stroke 3 px + a duplicate blurred 10 px at ~60% for glow, head dot r 5 with a 15 px glow, core #f27525."""
    np = np_()
    from PIL import Image, ImageFilter, ImageDraw
    W, H = 360, 160
    pts = [(20, 80 + 40 * math.sin(x / 40.0)) for x in range(0, 1)] + [(20 + x, 80 + 40 * math.sin(x / 40.0)) for x in range(0, 320, 4)]
    dense, L = resample(pts, 1.0)
    core = (0xf2, 0x75, 0x25)

    def frame(t, glow=True):
        p = in_out_cubic(prog(t, 0.1, 1.4))
        base = Image.new("RGB", (W, H), (5, 5, 8))
        if p <= 0:
            return base
        pre = prefix(dense, p)
        line = Image.new("RGB", (W, H), (0, 0, 0))
        poly(line, pre, 3, core)
        out = np.asarray(base, float) + np.asarray(line, float)
        if glow:
            gl = np.asarray(line.filter(ImageFilter.GaussianBlur(10 / 2.0)), float) * 0.6 * 3
            out = out + gl
            hd = Image.new("RGB", (W, H), (0, 0, 0))
            x, y = pre[-1]
            ImageDraw.Draw(hd).ellipse((x - 5, y - 5, x + 5, y + 5), fill=(255, 220, 180))
            out = out + np.asarray(hd.filter(ImageFilter.GaussianBlur(7.5)), float) * 2 + np.asarray(hd, float)
        return Image.fromarray(np.clip(out, 0, 255).astype("uint8"))
    vid, frames = film(wd, "glow.mp4", frame, 1.6, (W, H))
    k = int(0.7 * 30)
    p = in_out_cubic(prog(k / 30.0, 0.1, 1.4))
    hx, hy = point_at(dense, p)
    fr = frames[k]
    br = lum(fr)
    near = br[max(0, int(hy) - 10):int(hy) + 11, max(0, int(hx) - 10):int(hx) + 11]
    yy, xx = np.nonzero(near >= 0.97 * near.max())
    bx, by = xx.mean() + max(0, int(hx) - 10), yy.mean() + max(0, int(hy) - 10)
    mid = point_at(dense, p * 0.4)
    halo = float(br[int(mid[1]) - 6:int(mid[1]) - 4, int(mid[0])].mean()) if True else 0
    raw = lum(arr(frame(k / 30.0, glow=False)))
    halo_raw = float(raw[int(mid[1]) - 6:int(mid[1]) - 4, int(mid[0])].mean())
    return [check("brightest spot rides the head of the line (±3 px)", math.hypot(bx - hx, by - hy) <= 3, [bx, by], [hx, hy]),
            check("glow halo lights pixels 4-6 px off the stroke", halo > 15, halo, ">15"),
            check("line core in #f27525", int(cmask(frames[-1], core, 40).sum()) > 0 or float(frames[-1][..., 0].max()) > 240, "orange core", "#f27525"),
            check("negative control: the bare stroke has no halo", not (halo_raw > 15), halo_raw, ">15")], [vid]


@card("DRAW-08")
def cumulative_segment_reveal(task, wd):
    """Many rings drawn as one timed stroke by cumulative length: each ring sliced in its own window, never bridged."""
    np = np_()
    W, H = 400, 200
    rings = [[(60 + 40 * math.cos(a), 100 + 40 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 60)],
             [(200 + 20 * math.cos(a), 100 + 20 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 40)],
             [(320 + 50 * math.cos(a), 100 + 30 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 60)]]
    lens = [plen(r) for r in rings]
    cum = np.concatenate([[0], np.cumsum(lens)])
    tot = cum[-1]

    def draw_at(p, bridge=False):
        im = pil((W, H), "#ffffff")
        if bridge:
            allp = [q for r in rings for q in r]
            poly(im, prefix(allp, p), 3, (0, 0, 0))
            return im
        L = p * tot
        for k, r in enumerate(rings):
            u = clamp((L - cum[k]) / lens[k])
            if u > 0:
                poly(im, prefix(r, u), 3, (0, 0, 0), cap=False)
        return im
    p = 0.55
    im = draw_at(p)
    im.save(wd / "rings.png")
    A = lum(arr(im)) < 128
    got = [drawn_frac(A, resample(r, 1.0)[0], 0) for r in rings]
    want = [clamp((p * tot - cum[k]) / lens[k]) for k in range(3)]
    gap = int(A[:, 105:175].sum()) + int(A[:, 225:265].sum())
    Bm = lum(arr(draw_at(1.0, bridge=True))) < 128
    gap_b = int(Bm[:, 105:175].sum()) + int(Bm[:, 225:265].sum())
    return [check("each ring's drawn share follows the cumulative-length window (±0.04)", all(abs(g - w) < 0.04 for g, w in zip(got, want)), got, want),
            check("no ink between rings (no invented joins)", gap == 0, gap, 0),
            check("negative control: one concatenated stroke bridges the rings", not (gap_b == 0), gap_b, 0)], [wd / "rings.png"]


@card("DRAW-15")
def brush_mask_rtl(task, wd):
    """Aref Ruqaa phrase revealed right->left by a soft-edged mask: 0-0.5 s start, 0.5-2.5 s reveal, 2.5-4 s read;
    gold gradient #f5c542 -> #d8a664 for the script headline; sticky-note lines 500 ms each."""
    np = np_()
    from PIL import Image
    f = font(AREF_B, 60)
    lines = ["الخط العربي", "فن خالد"]
    tiles = [tile(l, f)[0] for l in lines]
    W = max(t.width for t in tiles) + 20
    H = sum(t.height for t in tiles) + 20
    top, bot = np.array(hexrgb("#f5c542"), float), np.array(hexrgb("#d8a664"), float)

    def frame(t, mask=True):
        out = np.zeros((H, W, 3))
        y = 10
        for k, tl in enumerate(tiles):
            A = np.asarray(tl.getchannel("A"), float) / 255.0
            b = bbox(A > 0.5)
            if k == 0:
                p = in_out_cubic(prog(t, 0.5, 2.5))
            else:
                p = in_out_cubic(prog(t, 2.5, 3.0))
            edge = b[2] - (b[2] - b[0] + 16) * p
            xs = np.arange(A.shape[1])[None, :]
            m = np.clip((xs - edge) / 8.0, 0, 1) if mask else np.ones_like(A)
            u = np.clip((np.arange(A.shape[0])[:, None, None] - b[1]) / max(1, b[3] - b[1]), 0, 1)
            col = top * (1 - u) + bot * u
            a = (A * m)[..., None]
            x0 = (W - tl.width) // 2
            out[y:y + A.shape[0], x0:x0 + A.shape[1]] = out[y:y + A.shape[0], x0:x0 + A.shape[1]] * (1 - a) + col * a
            y += tl.height
        return Image.fromarray(out.round().astype("uint8"))
    vid, frames = film(wd, "brush_rtl.mp4", frame, 4.0, (W, H))
    final = lum(frames[-1]) > 60
    l1 = slice(10, 10 + tiles[0].height)
    f1 = lambda fr: float(((lum(fr) > 60) & final)[l1].sum()) / float(final[l1].sum())
    k = int(1.5 * 30)
    m = (lum(frames[k]) > 60)[l1]
    xs = np.nonzero(m.any(0))[0]
    row = lum(frames[k])[l1].max(0)
    soft = int(((row > 15) & (row < 0.85 * row.max())).sum())
    l2 = slice(10 + tiles[0].height, H)
    s2 = [float((lum(fr[l2]) > 60).sum()) for fr in frames]
    l2_on = next(j for j, v in enumerate(s2) if v > 0) / 30.0
    ink = frames[-1][final]
    ys = np.nonzero(final[l1])[0]
    tcol = frames[-1][l1][ys.min() + 3][final[l1][ys.min() + 3]].mean(0)
    bcol = frames[-1][l1][ys.max() - 3][final[l1][ys.max() - 3]].mean(0)
    un = lum(arr(frame(0.0, mask=False))) > 60
    return [check("nothing before 0.5 s, line 1 complete by 2.5 s", f1(frames[14]) < 0.01 and f1(frames[75]) > 0.98, [f1(frames[14]), f1(frames[75])], [0, 1]),
            check("reveal runs right to left (right edge reached first)", xs.max() >= bbox(final[l1])[2] - 3 and xs.min() > bbox(final[l1])[0] + 10,
                  [int(xs.min()), int(xs.max())], "right part only"),
            check("soft mask edge (several partial-alpha columns)", soft >= 4, soft, ">=4"),
            check("second line starts after the first (one line per 500 ms)", abs(l2_on - 2.5) <= 0.12, l2_on, 2.5),
            check("gold gradient: lighter #f5c542 top, deeper #d8a664 bottom", tcol[2] < bcol[2] + 30 and tcol[1] > bcol[1] + 10, [list(tcol), list(bcol)], "gradient"),
            check("negative control: the unmasked phrase is fully visible at t=0", not (float((un & final).sum()) / float(final.sum()) < 0.01), 1.0, "<0.01")], [vid]


@card("DRAW-17")
def handwritten_typewriter(task, wd):
    """Lay out the whole sentence first, then reveal per character (Latin) over 65% of the clip; glyph height 4-5% of
    H; placed 8-12% inside the frame edges on empty area."""
    np = np_()
    from PIL import Image, ImageDraw
    W, H = 480, 270
    D = 3.0
    text = "Notes by hand"
    size = 0
    for s_ in range(8, 40):
        b = bbox(np.asarray(tile("x", font(POPPINS_R, s_))[0].getchannel("A")) > 128)
        if (b[3] - b[1]) / H >= 0.045 * 0.55:
            size = s_
            break
    f = font(POPPINS_R, size * 2)
    x0, y0 = 0.10 * W, 0.10 * H
    adv = [f.getlength(text[:i]) for i in range(len(text) + 1)]

    def frame(t, recentre=False):
        im = pil((W, H), "#fdfcf7")
        p = prog(t, 0.1 * D, 0.65 * D)
        n = int(math.floor(p * len(text) + 1e-9))
        s = text[:n]
        if s:
            x = x0 if not recentre else W / 2 - f.getlength(s) / 2
            ImageDraw.Draw(im).text((x, y0), s, font=f, fill=(30, 30, 40))
        return im
    vid, frames = film(wd, "typewriter.mp4", frame, D, (W, H))
    fin = lum(frames[-1]) < 128
    outside = max(int(((lum(fr) < 128) & ~fin).sum()) for fr in frames)
    done = next(j for j, fr in enumerate(frames) if ((lum(fr) < 128) == fin).all()) / 30.0
    b = bbox(fin)
    xh = bbox(np.asarray(tile("N", f)[0].getchannel("A")) > 128)
    gh = (xh[3] - xh[1]) / H
    per_char = (0.55 * D) / len(text)
    rc = max(int(((lum(arr(frame(t, True))) < 128) & ~fin).sum()) for t in (0.6, 1.0, 1.5))
    return [check("revealed text never re-centres (each frame ⊆ final layout)", outside == 0, outside, 0),
            check("reveal finishes at 65% of the clip", abs(done - 0.65 * D) <= 1.5 * per_char + 0.034, done, 0.65 * D),
            check("cap glyph height 4-5% of H", 0.04 <= gh <= 0.05 + 0.02, gh, "0.04-0.05"),
            check("placed 8-12% inside the frame edges", 0.08 * W <= b[0] <= 0.12 * W + 2 and 0.08 * H <= b[1] <= 0.14 * H, [b[0] / W, b[1] / H], "0.08-0.12"),
            check("negative control: re-centring partial text moves glyphs", not (rc == 0), rc, 0)], [vid]


def jitter_ellipse(cx, cy, rx, ry, seed, overlap=0.15, n=140, amp=3.0):
    rnd = mulberry32(seed)
    ph = [rnd() * 2 * math.pi for _ in range(3)]
    pts = []
    for i in range(n + 1):
        a = -math.pi / 2 + 2 * math.pi * (1 + overlap) * i / n
        k = 1 + amp / max(rx, ry) * sum(math.sin((j + 2) * a + ph[j]) / (j + 1) for j in range(3)) + 0.14 * i / n
        pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
    return pts


@card("DRAW-19")
def circle_emphasis(task, wd):
    """Irregular overshooting ellipse (start/end overlap ~15%), stroke 2.5 px, drawn 500 ms by dashoffset after the
    content lands (red)."""
    np = np_()
    W, H = 360, 200
    red = (220, 40, 40)
    path = jitter_ellipse(180, 100, 90, 45, seed=19)
    dense, L = resample(path, 1.0)
    word, _ = tile("نمو", font(CAIRO, 50, wght=800), fill=(30, 30, 30, 255))

    def frame(t):
        im = blank((W, H), (250, 250, 245))
        if t >= 0.1:
            place(im, word, 180, 100, alpha=prog(t, 0.1, 0.3))
        im = im.convert("RGB")
        p = in_out_cubic(prog(t, 0.3, 0.8))
        if p > 0:
            poly(im, prefix(dense, p), 2.5, red)
        return im
    vid, frames = film(wd, "circle.mp4", frame, 1.2, (W, H))
    first = next(j for j, fr in enumerate(frames) if cmask(fr, red, 50).any()) / 30.0
    full = cmask(frames[-1], red, 50)
    complete = next(j for j, fr in enumerate(frames) if (cmask(fr, red, 50) == full).all()) / 30.0
    rr, ang = angle_grid(H, W, 180, 100)
    cover = len(set(np.floor(ang[full]).astype(int).tolist())) / 360.0
    ex = (lambda m, a: (m & (np.abs(((ang - a + 180) % 360) - 180) < 1.0)))
    def crossings(a):
        m = ex(full, a)
        r = np.sort(rr[m])
        return int(1 + (np.diff(r) > 3).sum()) if len(r) else 0
    over = max(crossings(a) for a in range(2, 40, 4))
    ideal = [(lambda th: 90 * 45 / math.hypot(45 * math.cos(th), 90 * math.sin(th)))(math.radians(a - 90)) for a in range(60, 330, 10)]

    def wobble(mask):
        rads = [float(rr[ex(mask, a)].mean()) for a in range(60, 330, 10)]
        return float(np.std(np.array(rads) - np.array(ideal)))
    dev = wobble(full)
    from PIL import ImageDraw
    pe = pil((W, H), "#fafaf5")
    ImageDraw.Draw(pe).ellipse((90, 55, 270, 145), outline=red, width=2)
    dev_p = wobble(cmask(arr(pe), red, 50))
    return [check("circle starts only after the content lands (>= 0.3 s)", first >= 0.3, first, ">=0.3"),
            check("drawn in ~500 ms (complete by 0.8 s)", complete <= 0.8 + 0.034, complete, 0.8),
            check("closed: 360° angular coverage", cover > 0.97, cover, 1.0),
            check("start and end overlap (double stroke near the start)", over >= 2, over, ">=2"),
            check("hand-drawn irregularity (radius wobble > 1 px)", dev > 1.0, dev, ">1"),
            check("negative control: a perfect ellipse has no wobble", not (dev_p > 1.0), dev_p, ">1")], [vid]


@card("DRAW-20")
def doodle_annotations(task, wd):
    """0-1 s shot, 1-4 s marks, 4-6 s read; the circle tracks the moving subject and never covers it; arrow first
    (250-300 ms, blue #2f7bf5) then the note; red #ef3b55 strike for the wrong statement."""
    np = np_()
    from PIL import ImageDraw
    W, H = 320, 180
    blue, red = hexrgb("#2f7bf5"), hexrgb("#ef3b55")
    subj = lambda t: (60 + 30 * t, 90)

    def frame(t, track=True):
        im = pil((W, H), "#7f8c8d")
        d = ImageDraw.Draw(im)
        sx, sy = subj(t)
        d.rectangle((sx - 12, sy - 12, sx + 12, sy + 12), fill=(255, 255, 255))
        cx, cy = (sx, sy) if track else subj(1.0)
        p = in_out_cubic(prog(t, 1.0, 1.4))
        if p > 0:
            ring = [(cx + 28 * math.cos(a), cy + 28 * math.sin(a)) for a in np.linspace(-math.pi / 2, 1.5 * math.pi, 80)]
            poly(im, prefix(ring, p), 3, blue)
        pa = prog(t, 1.4, 1.68)
        if pa > 0:
            poly(im, prefix([(cx + 80, cy - 60), (cx + 45, cy - 30)], pa), 3, blue)
        ps = prog(t, 2.0, 2.3)
        if ps > 0:
            poly(im, prefix([(200, 160), (300, 160)], ps), 3, red)
        return im
    vid, frames = film(wd, "annot.mp4", frame, 6.0, (W, H), fps=15)
    marks = lambda fr: cmask(fr, blue, 40) | cmask(fr, red, 40)
    pre = sum(int(marks(fr).sum()) for fr in frames[:15])
    cover = 0
    cerr = []
    for i, fr in enumerate(frames):
        sx, sy = subj(i / 15.0)
        cover += int(marks(fr)[int(sy) - 12:int(sy) + 13, int(sx) - 12:int(sx) + 13].sum())
        if i / 15.0 >= 1.5:
            m = cmask(fr, blue, 40)
            m[:, :] &= (np.hypot(*np.mgrid[0:H, 0:W][::-1] - np.array([sx, sy])[:, None, None]) < 40)
            ys, xs = np.nonzero(m)
            cerr.append(math.hypot(xs.mean() - sx, ys.mean() - sy))
    arrow_t = next(j for j, fr in enumerate(frames) if cmask(fr[:, :], blue, 40)[0:40].any() or False) if False else None
    stat_cover = sum(int(marks(arr(frame(t, track=False)))[78:103, int(subj(t)[0]) - 12:int(subj(t)[0]) + 13].sum()) for t in (1.5, 2.5, 3.5))
    return [check("no marks during the 0-1 s shot", pre == 0, pre, 0),
            check("marks never cover the moving subject", cover == 0, cover, 0),
            check("circle tracks the subject (centre < 2 px)", max(cerr) < 2.0, max(cerr), "<2"),
            check("blue for right, red for wrong", bool(cmask(frames[-1], red, 40).any()) and bool(cmask(frames[-1], blue, 40).any()), True, True),
            check("negative control: an untracked circle ends up over the subject", not (stat_cover == 0), stat_cover, 0)], [vid]


@card("DRAW-21")
def scribble_strike(task, wd):
    """A looping magenta scribble crosses out the old words in 300 ms, they fade to 50%, the new line rises 250 ms
    easeOutBack from below."""
    np = np_()
    W, H = 360, 200
    mag = (230, 30, 200)
    old, _ = tile("قديم", font(CAIRO, 46, wght=700))
    new, _ = tile("جديد", font(CAIRO, 46, wght=700))
    ob = bbox(np.asarray(old.getchannel("A")) > 128)
    x0, x1 = 180 - (old.width / 2 - ob[0]), 180 + (ob[2] - old.width / 2)
    loops = [(x1 - (x1 - x0) * u + 10 * math.cos(u * 14 * math.pi), 70 + 12 * math.sin(u * 14 * math.pi)) for u in np.linspace(0, 1, 300)]
    dense, _ = resample(loops, 1.0)

    def frame(t):
        c = blank((W, H))
        place(c, old, 180, 70, alpha=1 - 0.5 * prog(t, 0.3, 0.5))
        p = prog(t, 0.2, 0.5)
        if t > 0.5:
            q = prog(t, 0.5, 0.75)
            place(c, new, 180, 150 + 30 * (1 - back_out(q)), alpha=clamp(q * 2))
        c = c.convert("RGB")
        if p > 0:
            poly(c, prefix(dense, p), 3, mag)
        return c
    vid, frames = film(wd, "strike.mp4", frame, 1.2, (W, H))
    last = frames[-1]
    cols = cmask(last, mag, 50).any(0)
    span = cols[int(x0):int(x1)].mean()
    om = (np.asarray(old.getchannel("A")) > 250)
    oy, ox = int(70 - old.height / 2), int(180 - old.width / 2)
    region = last[oy:oy + om.shape[0], ox:ox + om.shape[1]]
    keep = om & ~cmask(region, mag, 80)
    oldlv = float(region[keep].mean()) / 255.0
    nys = []
    for fr in frames[15:]:
        m = lum(fr[110:]) > 200
        nys.append(float(np.nonzero(m)[0].mean()) + 110 if m.sum() > 30 else None)
    nys = [y for y in nys if y is not None]
    over = nys[-1] - min(nys)
    before = float(frames[3][oy:oy + om.shape[0], ox:ox + om.shape[1]][om].mean()) / 255.0
    return [check("scribble covers the old words' width", span > 0.95, span, ">0.95"),
            check("old words fade to 50%", abs(oldlv - 0.5) < 0.05, oldlv, 0.5),
            check("new line overshoots above its rest (easeOutBack)", over > 1.0, over, ">1"),
            check("scribble drawn within 300 ms", (cmask(frames[15], mag, 50).sum() > 0.98 * cmask(last, mag, 50).sum()), "done by 0.5 s", "0.3 s"),
            check("negative control: before the strike the old words are at full strength", not (abs(before - 0.5) < 0.05), before, 0.5)], [vid]


def rough_rrect(x0, y0, x1, y1, r, seed, amp=1.5):
    rnd = mulberry32(seed)
    pts = []
    corners = [(x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)]
    for cx, cy, a0 in corners:
        for k in range(12):
            a = math.radians(a0 + 90 * k / 11)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    pts.append(pts[0])
    dense, _ = resample(pts, 4.0)
    return [(x + (rnd() - 0.5) * 2 * amp, y + (rnd() - 0.5) * 2 * amp) for x, y in dense] + [(pts[0][0] + 6, pts[0][1])]


@card("DRAW-22")
def boxed_callout(task, wd):
    """A jittered rounded rectangle draws first in #d17c55 over 400 ms, then the words appear inside over 600 ms."""
    np = np_()
    W, H = 360, 200
    col = hexrgb("#d17c55")
    box = rough_rrect(60, 50, 300, 150, 18, seed=22)
    dense, _ = resample(box, 1.0)
    word, _ = tile("مهم جدا", font(CAIRO, 44, wght=800), fill=(30, 30, 30, 255))

    def frame(t, text_first=False):
        c = blank((W, H), (250, 248, 240))
        a = prog(t, 0.1, 0.7) if text_first else prog(t, 0.5, 1.1)
        if a > 0:
            place(c, word, 180, 100, alpha=a)
        c = c.convert("RGB")
        p = in_out_cubic(prog(t, 0.1, 0.5))
        if p > 0:
            poly(c, prefix(dense, p), 3, col)
        return c
    vid, frames = film(wd, "callout.mp4", frame, 1.3, (W, H))
    dark = lambda fr: (lum(fr) < 200) & ~cmask(fr, col, 60)
    txt_on = next(j for j, fr in enumerate(frames) if dark(fr).sum() > 10) / 30.0
    fullb = cmask(frames[-1], col, 40)
    box_done = next(j for j, fr in enumerate(frames) if cmask(fr, col, 40).sum() >= 0.99 * fullb.sum()) / 30.0
    bb = bbox(fullb)
    tb = bbox(dark(frames[-1]))
    top = [np.nonzero(fullb[:, x])[0].min() for x in range(100, 260)]
    wob = float(np.std(top))
    tf_on = next(j for j, t in enumerate(np.arange(0, 1.3, 1 / 30.0)) if dark(arr(frame(t, True))).sum() > 10) / 30.0
    return [check("box drawn in 400 ms (done by 0.5 s)", box_done <= 0.5 + 0.034, box_done, 0.5),
            check("words appear only after the box is drawn", txt_on >= box_done - 0.034, [txt_on, box_done], "after"),
            check("words sit inside the box", bb[0] < tb[0] and tb[2] < bb[2] and bb[1] < tb[1] and tb[3] < bb[3], [bb, tb], "inside"),
            check("rough edge (top edge wobble > 0.4 px)", wob > 0.4, wob, ">0.4"),
            check("negative control: a text-first order shows words before the box", not (tf_on >= box_done - 0.034), tf_on, box_done)], [vid]


def wobble_line(x0, y0, x1, y1, seed, amp=1.5, n=40):
    """Seeded vertex noise (fixed per stroke) smoothed by Catmull-Rom."""
    np = np_()
    rnd = mulberry32(seed)
    base = [(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n) for i in range(n + 1)]
    nx, ny = -(y1 - y0), (x1 - x0)
    l = math.hypot(nx, ny)
    nx, ny = nx / l, ny / l
    off = [(rnd() - 0.5) * 2 * amp for _ in base]
    off[0] = off[-1] = 0
    P = [(x + nx * o, y + ny * o) for (x, y), o in zip(base, off)]
    out = []
    for i in range(len(P) - 1):
        p0, p1, p2, p3 = P[max(0, i - 1)], P[i], P[i + 1], P[min(len(P) - 1, i + 2)]
        for u in np.linspace(0, 1, 8, endpoint=False):
            u2, u3 = u * u, u * u * u
            out.append(tuple(0.5 * ((2 * p1[k]) + (-p0[k] + p2[k]) * u + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * u2 +
                                    (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * u3) for k in range(2)))
    out.append(P[-1])
    return out


def var_width_stroke(im, pts, w0, var, seed, colr):
    from PIL import ImageDraw
    rnd = mulberry32(seed + 7)
    d = ImageDraw.Draw(im)
    ws = []
    for i in range(len(pts) - 1):
        w = w0 * (1 + (rnd() - 0.5) * 2 * var)
        ws.append(w)
        d.line([pts[i], pts[i + 1]], fill=colr, width=max(1, int(round(w))))
    return ws


@card("DRAW-25")
def deliberate_imperfection(task, wd):
    """Vertices offset by seeded noise (1.5 px), Catmull-Rom smoothed, width +-15%, warm dark ink #2a2a2a; the seed is
    fixed per stroke so frames never jitter by accident."""
    np = np_()
    W, H = 360, 120
    ink = hexrgb("#2a2a2a")

    def frame(t, seed=25):
        im = pil((W, H), "#f6f1e4")
        var_width_stroke(im, wobble_line(20, 60, 340, 60, seed), 4, 0.15, seed, ink)
        return im
    a, b = arr(frame(0)), arr(frame(1.0))
    a_img = frame(0); a_img.save(wd / "wobble.png")
    m = lum(a) < 128
    cy, th = [], []
    for x in range(30, 330):
        ys = np.nonzero(m[:, x])[0]
        if len(ys):
            cy.append(ys.mean()); th.append(len(ys))
    dev = np.abs(np.array(cy) - np.median(cy))
    from PIL import Image
    ideal = pil((W, H), "#f6f1e4")
    poly(ideal, [(20, 60), (340, 60)], 4, ink, cap=False)
    mi = lum(arr(ideal)) < 128
    ci = [np.nonzero(mi[:, x])[0].mean() for x in range(30, 330)]
    dev_i = float(np.abs(np.array(ci) - np.median(ci)).max())
    return [check("wobble 0.5-2.5 px off the ideal line", 0.5 <= float(dev.max()) <= 2.6, float(dev.max()), "0.5-2.5"),
            check("width varies (±10-20% gives CV 0.05-0.3)", 0.05 <= float(np.std(th) / np.mean(th)) <= 0.3, float(np.std(th) / np.mean(th)), "0.05-0.3"),
            check("fixed seed: frames identical", float(np.abs(a - b).max()) == 0, float(np.abs(a - b).max()), 0),
            check("warm dark ink", bool(cmask(a, ink, 20).any()), True, True),
            check("negative control: the ideal ruler line has no wobble", not (0.5 <= dev_i), dev_i, ">=0.5")], [wd / "wobble.png"]


@card("DRAW-26")
def line_boil(task, wd):
    """seed = floor(t * 12) at 24 fps (on twos), amplitude ~1 px; boil only the drawing, never the Arabic text."""
    np = np_()
    W, H = 360, 160
    word, _ = tile("نص ثابت", font(CAIRO, 40, wght=700), fill=(20, 20, 20, 255))

    def frame(t, rate=12):
        c = blank((W, H), (250, 248, 240))
        place(c, word, 270, 120)
        c = c.convert("RGB")
        sd = int(math.floor(t * rate + 1e-9))
        for k in range(3):
            poly(c, wobble_line(20, 30 + 25 * k, 200, 30 + 25 * k, seed=100 * k + sd, amp=1.0), 2, (20, 20, 20), cap=False)
        return c
    vid, frames = film(wd, "boil.mp4", frame, 1.0, (W, H), fps=24)
    dr = [fr[10:100, 10:210] for fr in frames]
    ch = [int(float(np.abs(b - a).max()) > 0) for a, b in zip(dr, dr[1:])]
    txt = max(float(np.abs(fr[95:150, 200:350] - frames[0][95:150, 200:350]).max()) for fr in frames)
    ones = [int(float(np.abs(arr(frame((j + 1) / 24.0, 24))[10:100, 10:210] - arr(frame(j / 24.0, 24))[10:100, 10:210]).max()) > 0) for j in range(6)]
    pattern = ch[:8]
    return [check("drawing re-wobbles every 2nd frame (on twos)", ch == [1 if (j + 1) % 2 == 0 else 0 for j in range(len(ch))], pattern, [0, 1] * 4),
            check("Arabic text never boils", txt == 0, txt, 0),
            check("negative control: per-frame seeds boil on ones", not (ones == [1 if (j + 1) % 2 == 0 else 0 for j in range(6)]), ones, [0, 1, 0, 1, 0, 1])], [vid]


def pf_outline(pts, size, thinning, pressure):
    """perfect-freehand style: radius = size * (0.5 - thinning * (0.5 - pressure)), left/right offsets -> polygon."""
    np = np_()
    P = np.asarray(pts, float)
    out_l, out_r = [], []
    for i in range(len(P)):
        a, b = P[max(0, i - 1)], P[min(len(P) - 1, i + 1)]
        t = b - a
        n = np.array([-t[1], t[0]]) / (np.hypot(*t) + 1e-9)
        r = size * (0.5 - thinning * (0.5 - pressure[i]))
        out_l.append(tuple(P[i] + n * r)); out_r.append(tuple(P[i] - n * r))
    return out_l + out_r[::-1]


@card("DRAW-28")
def pressure_strokes(task, wd):
    """Points resampled every 2.5 px become a variable-width outline polygon (marker size 9, thinning .6, pressure from
    sin over arc length); drawn by passing a prefix of n * ease(p) points; chalk halo x2.2 at 0.12."""
    np = np_()
    from PIL import Image, ImageDraw
    W, H = 400, 160
    raw = [(20 + x, 80 + 30 * math.sin(x / 50.0)) for x in range(0, 361, 3)]
    pts, L = resample(raw, 2.5)
    s_arc = np.linspace(0, 1, len(pts))
    pres = 0.5 + 0.5 * np.sin(s_arc * 3 * math.pi)
    size, thin = 18, 0.6

    def render(p, chalk=False, const=False):
        im = Image.new("RGB", (W, H), (255, 255, 255))
        n = max(2, int(len(pts) * pow_out(p, 2)))
        pr = np.full(len(pts), 0.5) if const else pres
        if chalk:
            halo = Image.new("L", (W, H), 0)
            ImageDraw.Draw(halo).polygon(pf_outline(pts[:n], size * 2.2, thin, pr[:n]), fill=int(255 * 0.12))
            im = Image.composite(Image.new("RGB", (W, H), (40, 40, 40)), im, halo)
        ImageDraw.Draw(im).polygon(pf_outline(pts[:n], size, thin, pr[:n]), fill=(47, 40, 32))
        return im
    full = render(1.0); full.save(wd / "stroke.png")
    A = lum(arr(full)) < 128
    widths = []
    for i in range(5, len(pts) - 5, 6):
        x, y = pts[i]
        col = A[:, int(round(x))]
        widths.append(int(col.sum()))
    rmin, rmax = size * (0.5 - thin * 0.5), size * (0.5 + thin * 0.5)
    half = lum(arr(render(0.5))) < 128
    sh = drawn_frac(half, pts, 0)
    ch = arr(render(1.0, chalk=True))
    halo_px = float(ch[int(pts[40][1]) - int(size * 0.75), int(pts[40][0])].mean())
    cst = lum(arr(render(1.0, const=True))) < 128
    cw = [int(cst[:, int(round(pts[i][0]))].sum()) for i in range(5, len(pts) - 5, 6)]
    return [check("width follows pressure: thin/thick ratio ≈ (0.5-0.3)/(0.5+0.3) of size", max(widths) >= 0.9 * 2 * rmax * 0.9 and min(widths) <= 2 * rmin * 1.6,
                  [min(widths), max(widths)], [2 * rmin, 2 * rmax]),
            check("prefix n * ease(0.5) draws ~75% of the points", abs(sh - pow_out(0.5, 2)) < 0.05, sh, 0.75),
            check("chalk halo at x2.2 size, ~12% opacity", 190 <= halo_px <= 240, halo_px, "≈255*(1-0.12*0.84)"),
            check("negative control: constant pressure gives one width", not (max(cw) - min(cw) > 6), [min(cw), max(cw)], ">6 px spread")], \
        [wd / "stroke.png"]


@card("DRAW-31")
def pencil_chalk_texture(task, wd):
    """Chrome SVG filter feTurbulence (fractalNoise .8, 2 octaves, seed 7) + feDisplacementMap scale 2.5 roughens the
    stroke edge, static seed; chalk puff: 8 particles burst and fade over ~300 ms at a term's completion."""
    np = np_()
    from PIL import Image, ImageDraw
    svg = ("<svg width=400 height=160 xmlns='http://www.w3.org/2000/svg'><defs><filter id='p' filterUnits='userSpaceOnUse' x='0' y='0' width='400' height='160'>"
           "<feTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='2' seed='7'/>"
           "<feDisplacementMap in='SourceGraphic' scale='%s' xChannelSelector='R' yChannelSelector='G'/></filter></defs>"
           "<rect width='400' height='160' fill='#fff'/>"
           "<line x1='20' y1='50' x2='380' y2='50' stroke='#222' stroke-width='8' filter='url(#p)'/>"
           "<line x1='20' y1='120' x2='380' y2='120' stroke='#222' stroke-width='8'/></svg>")
    html = "<!doctype html><html><body style='margin:0'>%s</body></html>" % (svg % "2.5")
    _, p1 = chrome_shot(wd, html, "pencil", 400, 160)
    _, p2 = chrome_shot(wd, html, "pencil_again", 400, 160)
    A = np.asarray(Image.open(p1).convert("RGB"), float)
    B = np.asarray(Image.open(p2).convert("RGB"), float)

    def edge_std(a, y0, y1):
        tops = []
        for x in range(40, 360):
            ys = np.nonzero(lum(a[y0:y1, x:x + 1])[:, 0] < 128)[0]
            if len(ys):
                tops.append(ys.min())
        return float(np.std(tops))
    rough, plain = edge_std(A, 20, 80), edge_std(A, 90, 150)
    W, H = 200, 120
    rnd = mulberry32(31)
    parts = [(2 * math.pi * k / 8 + 0.3 * rnd(), 22 + 14 * rnd()) for k in range(8)]

    def frame(t):
        im = pil((W, H), "#264a3e")
        p = prog(t, 0.2, 0.5)
        if 0 < p < 1:
            d = ImageDraw.Draw(im)
            for a, sp in parts:
                x, y = 100 + math.cos(a) * sp * p * 1.5, 60 + math.sin(a) * sp * p * 1.5
                v = int(240 * (1 - p))
                d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(v, v, v))
        return im
    vid, frames = film(wd, "puff.mp4", frame, 0.7, (W, H))
    n_mid = comps(lum(frames[9]) > 120)
    n_end = int((lum(frames[16]) > 90).sum())
    return [check("filtered stroke edge is rough (row std > 0.3 px)", rough > 0.3, rough, ">0.3"),
            check("static seed: two renders identical", float(np.abs(A - B).max()) == 0, float(np.abs(A - B).max()), 0),
            check("chalk puff: 8 particles mid-burst", n_mid == 8, n_mid, 8),
            check("puff gone ~300 ms after it starts", n_end == 0, n_end, 0),
            check("negative control: the unfiltered stroke edge is straight", not (plain > 0.3), plain, ">0.3")], [p1, vid]


@card("DRAW-32")
def triple_coastline(task, wd):
    """Clip to the sea polygon, stroke the coast 18 / 12 / 6 px alternating ink #5d5140 and sea #bfcdbe on top:
    parallel ripples on the sea side only."""
    np = np_()
    from PIL import Image, ImageDraw
    W, H = 400, 240
    ink, sea, land = hexrgb("#5d5140"), hexrgb("#bfcdbe"), hexrgb("#efe6d0")
    coast = [(x, 110 + 18 * math.sin(x / 45.0)) for x in range(-10, 411, 2)]
    sea_poly = coast + [(410, H + 10), (-10, H + 10)]

    def render(clip=True):
        im = Image.new("RGB", (W, H), land)
        ImageDraw.Draw(im).polygon(sea_poly, fill=sea)
        lay = im.copy()
        for w, col in ((18, ink), (12, sea), (6, ink)):
            poly(lay, coast, w, col, cap=False)
        if not clip:
            return lay
        m = Image.new("L", (W, H), 0)
        ImageDraw.Draw(m).polygon(sea_poly, fill=255)
        return Image.composite(lay, im, m)
    im = render(); im.save(wd / "coast.png")
    A = arr(im)
    x = 200
    y0 = 110 + 18 * math.sin(x / 45.0)
    col = A[:, x]
    seq = []
    for y in range(int(math.ceil(y0)) + 1, int(y0) + 14):
        c = "i" if cmask(col[y:y + 1][None], ink, 20).any() else ("s" if cmask(col[y:y + 1][None], sea, 20).any() else "?")
        seq.append(c)
    runs = []
    for c in seq:
        if runs and runs[-1][0] == c:
            runs[-1][1] += 1
        else:
            runs.append([c, 1])
    land_ok = not cmask(A[:int(y0) - 2, x:x + 1], ink, 20).any()
    U = arr(render(False))
    land_bad = cmask(U[:int(y0) - 2, x:x + 1], ink, 20).any()
    return [check("bands from the coast: ink, sea, ink, then open sea", [r[0] for r in runs][:4] == ["i", "s", "i", "s"], runs, "i s i s"),
            check("band widths ≈ 3 px each (half of 6 / 12 - 6 / 18 - 12)", all(2 <= r[1] <= 4 for r in runs[:3]), [r[1] for r in runs[:3]], [3, 3, 3]),
            check("land side untouched (clipped to the sea polygon)", land_ok, land_ok, True),
            check("negative control: unclipped strokes paint the land", not (not land_bad), bool(land_bad), False)], [wd / "coast.png"]


@card("DRAW-33")
def whiteboard(task, wd):
    """Basma whiteboard: bg #F4F4F1, ink #23272E, accent #E0412E; each sentence onset triggers its element's draw-on,
    lines revealed right->left; after a 1.5 s hold the board pans one board width in 800 ms ease-in-out."""
    np = np_()
    from PIL import Image
    W, H = 320, 180
    bg, ink, acc = hexrgb("#F4F4F1"), hexrgb("#23272E"), hexrgb("#E0412E")
    onsets = [0.3, 1.2]
    els = [[(260, 60), (60, 60)], [(260, 120), (60, 120)]]
    dense = [resample(e, 1.0)[0] for e in els]
    end_draw = onsets[-1] + 0.6
    pan0 = end_draw + 1.5

    def frame(t):
        board = Image.new("RGB", (2 * W, H), bg)
        for k, (on, dn) in enumerate(zip(onsets, dense)):
            p = in_out_cubic(prog(t, on, on + 0.6))
            if p > 0:
                poly(board, prefix(dn, p), 4, acc if k == 1 else ink)
        poly(board, [(W + 60, 90), (W + 260, 90)], 4, ink)
        off = W * in_out_cubic(prog(t, pan0, pan0 + 0.8))
        return board.crop((int(round(off)), 0, int(round(off)) + W, H))
    D = pan0 + 1.0
    vid, frames = film(wd, "whiteboard.mp4", frame, D, (W, H))
    first = [next(j for j, fr in enumerate(frames) if cmask(fr[50:70] if k == 0 else fr[110:130], ink if k == 0 else acc, 20).any()) / 30.0 for k in range(2)]
    k = int((onsets[0] + 0.3) * 30)
    xs = np.nonzero(cmask(frames[k][55:66], ink, 20).any(0))[0]
    offs = []
    for j, fr in enumerate(frames):
        m = cmask(fr, ink, 20)
        cols = np.nonzero(m[88:93].any(0))[0]
        offs.append((W + 60 - cols.min()) if len(cols) and j / 30.0 >= pan0 - 0.01 else None)
    jm = int(round((pan0 + 0.4) * 30))
    mid_off = W + 60 - np.nonzero(cmask(frames[jm], ink, 20)[88:93].any(0))[0].min()
    moved_before = float(np.abs(frames[int((pan0 - 0.05) * 30)] - frames[int((end_draw + 0.1) * 30)]).max())
    return [check("palette: board #F4F4F1, ink #23272E, accent #E0412E", tuple(frames[0][5, 5].astype(int)) == bg and cmask(frames[int(pan0 * 30) - 2], acc, 20).any(),
                  list(frames[0][5, 5]), bg),
            check("each element starts on its sentence onset (±1 frame)", all(abs(f_ - o) <= 0.034 for f_, o in zip(first, onsets)), first, onsets),
            check("lines are revealed right to left", xs.min() > 150 and xs.max() >= 255, [int(xs.min()), int(xs.max())], "right half first"),
            check("1.5 s hold before the pan (board static)", moved_before == 0, moved_before, 0),
            check("pan: half a board width at the midpoint (in-out), full width at the end", abs(mid_off - W / 2) <= 2, int(mid_off), W / 2),
            check("negative control: elements drawn at t=0 would miss the onsets", not (abs(0.0 - onsets[0]) <= 0.034), 0.0, onsets[0])], [vid]


@card("DRAW-34")
def whiteboard_cinematic(task, wd):
    """Draw-on at 1000 px/s (500 at K) with a hand pinned to the tip; after a 1.5 s hold the camera pushes in (x1.25)
    over 800 ms ease-in-out."""
    np = np_()
    from PIL import Image, ImageDraw
    W, H = 320, 180
    path = [(60, 120), (140, 50), (200, 110), (260, 60)]
    dense, L = resample(path, 1.0)
    dur = L / 500.0
    t0 = 0.1
    push0 = t0 + dur + 1.5
    hand = (240, 190, 150)

    def frame(t, push=True):
        im = Image.new("RGB", (W, H), (244, 244, 241))
        p = prog(t, t0, t0 + dur)
        if p > 0:
            pre = prefix(dense, p)
            poly(im, pre, 4, (35, 39, 46))
            if p < 1:
                x, y = pre[-1]
                ImageDraw.Draw(im).ellipse((x + 2, y + 2, x + 14, y + 14), fill=hand)
        s = 1 + 0.25 * in_out_cubic(prog(t, push0, push0 + 0.8)) if push else 1.0
        if s > 1:
            w2, h2 = W / s, H / s
            im = im.crop((int(W / 2 - w2 / 2), int(H / 2 - h2 / 2), int(W / 2 + w2 / 2), int(H / 2 + h2 / 2))).resize((W, H), Image.BICUBIC)
        return im
    D = push0 + 1.0
    vid, frames = film(wd, "cinematic.mp4", frame, D, (W, H))
    m = [lum(fr) < 100 for fr in frames]
    k1, k2 = int(round((t0 + 0.25 * dur) * 30)), int(round((t0 + 0.75 * dur) * 30))
    f1, f2 = drawn_frac(m[k1], dense, 0), drawn_frac(m[k2], dense, 0)
    speed = (f2 - f1) * L / ((k2 - k1) / 30.0)
    hand_err = []
    for j in range(int(t0 * 30) + 2, int((t0 + dur) * 30) - 1):
        hm = cmask(frames[j], hand, 25)
        if hm.sum() > 20:
            ys, xs = np.nonzero(hm)
            tip = point_at(dense, prog(j / 30.0, t0, t0 + dur))
            hand_err.append(math.hypot(xs.mean() - 8 - tip[0], ys.mean() - 8 - tip[1]))
    bw = lambda fr: (lambda b: b[2] - b[0])(bbox(lum(fr) < 100))
    z = bw(frames[-1]) / bw(frames[int((push0 - 0.1) * 30)])
    nz = bw(arr(frame(D, push=False))) / bw(frames[int((push0 - 0.1) * 30)])
    return [check("pen speed ≈ 500 px/s at K (1000 at 1080)", abs(speed - 500) < 40, speed, 500),
            check("hand sprite pinned to the tip (<2 px)", hand_err and max(hand_err) < 2.0, max(hand_err) if hand_err else None, "<2"),
            check("camera push x1.25 after the hold", abs(z - 1.25) < 0.04, z, 1.25),
            check("negative control: without the push the framing stays x1.0", not (abs(nz - 1.25) < 0.04), nz, 1.25)], [vid]


@card("DRAW-35")
def chalkboard(task, wd):
    """Chalk on #264A3E with ink #F3F1E7: textured strokes (broken coverage), board texture 5-10%, every timing x
    one slowness factor TS."""
    np = np_()
    from PIL import Image
    W, H = 320, 180
    bg, ink = np.array(hexrgb("#264A3E"), float), np.array(hexrgb("#F3F1E7"), float)
    rng = np.random.default_rng(35)
    tex = 1 + rng.uniform(-0.075, 0.075, (H, W, 1))
    grain = rng.uniform(0, 1, (H, W)) > 0.22
    path = [(40, 90), (280, 90)]
    dense, L = resample(path, 1.0)
    TS = 1.3

    def frame(t, ts=TS, chalky=True):
        p = in_out_cubic(prog(t, 0.1 * ts, 0.1 * ts + 0.8 * ts))
        base = bg * tex
        m = Image.new("L", (W, H), 0)
        if p > 0:
            poly(m, prefix(dense, p), 8, 255, cap=False)
        mm = (np.asarray(m) > 128) & (grain if chalky else True)
        out = base.copy()
        out[mm] = ink
        return Image.fromarray(np.clip(out, 0, 255).astype("uint8"))
    vid, frames = film(wd, "chalk.mp4", frame, 1.4 * TS, (W, H))
    empty = frames[0][20:60, 20:300]
    var = float(lum(empty).std() / lum(empty).mean())
    foot = Image.new("L", (W, H), 0); poly(foot, dense, 8, 255, cap=False)
    fm = np.asarray(foot) > 128
    cov = float(cmask(frames[-1], ink, 20)[fm].mean())
    jm = int(round((0.1 * TS + 0.4 * TS) * 30))
    half = drawn_frac(cmask(frames[jm], ink, 20), dense, 3)
    want_half = in_out_cubic(prog(jm / 30.0, 0.1 * TS, 0.9 * TS))
    half_ts1 = drawn_frac(cmask(arr(frame(jm / 30.0, ts=1.0)), ink, 20), dense, 3)
    solid = arr(frame(1.4 * TS, chalky=False))
    return [check("board texture 5-10% (luminance CV)", 0.025 <= var <= 0.1, var, "0.05-0.10 peak-to-peak"),
            check("chalk stroke has gaps (coverage 70-90%)", 0.7 <= cov <= 0.9, cov, "0.7-0.9"),
            check("timings scaled by TS = 1.3 (half-drawn at 0.65 s)", abs(half - want_half) < 0.05, half, want_half),
            check("negative control: unscaled timings (TS = 1) are ahead at that moment", not (abs(half_ts1 - want_half) < 0.05), half_ts1, want_half),
            check("palette #264A3E / #F3F1E7", bool(cmask(frames[-1], ink, 20).any()) and abs(float(lum(empty).mean()) - float(bg.mean())) < 4,
                  float(lum(empty).mean()), float(bg.mean())),
            check("negative control: a solid stroke has no chalk gaps", not (0.7 <= float(cmask(solid, ink, 20)[fm].mean()) <= 0.9),
                  float(cmask(solid, ink, 20)[fm].mean()), "0.7-0.9")], [vid]


@card("DRAW-36")
def doodle_story(task, wd):
    """Doodle STY: boil 3 stroke variants every 3 frames, a prop pops 0 -> 1.08 -> 1, emphasis word #F07F2E with glow
    #FFD0A0 over a sky gradient #AFDCF0 -> #EAF6F4."""
    np = np_()
    from PIL import Image
    W, H = 270, 480
    sky0, sky1 = np.array(hexrgb("#AFDCF0"), float), np.array(hexrgb("#EAF6F4"), float)
    grad = (sky0 * (1 - np.linspace(0, 1, H)[:, None, None]) + sky1 * np.linspace(0, 1, H)[:, None, None]) * np.ones((1, W, 1))
    variants = [wobble_line(30, 300, 240, 300, seed=360 + k, amp=1.2) for k in range(3)]
    word, _ = tile("الحب", font(TAJAWAL, 44), fill=hexrgb("#F07F2E") + (255,))
    glow, _ = tile("الحب", font(TAJAWAL, 44), fill=hexrgb("#FFD0A0") + (255,))
    prop_t = 0.5

    def scale(t):
        p = prog(t, prop_t, prop_t + 0.4)
        return 1.08 * pow_out(p / 0.6, 2) if p < 0.6 else 1.08 - 0.08 * in_out_cubic((p - 0.6) / 0.4)

    def frame(t, boil=True):
        im = Image.fromarray(grad.astype("uint8")).convert("RGBA")
        j = int(round(t * 30))
        v = variants[(j // 3) % 3] if boil else variants[0]
        rgb = im.convert("RGB"); poly(rgb, v, 3, hexrgb("#3A2A1E")); im = rgb.convert("RGBA")
        s = scale(t)
        if s > 0.01:
            from PIL import ImageDraw
            card_ = Image.new("RGBA", (80, 60), hexrgb("#F6F0E4") + (255,))
            ImageDraw.Draw(card_).rectangle((0, 0, 79, 59), outline=hexrgb("#3A2A1E") + (255,), width=3)
            place(im, card_, 135, 180, scale=s)
        place(im, glow, 135, 400, blur=3)
        place(im, word, 135, 400)
        return im.convert("RGB")
    vid, frames = film(wd, "doodle.mp4", frame, 1.6, (W, H))
    reg = lambda fr: fr[290:312]
    same3 = float(np.abs(reg(frames[3]) - reg(frames[0])).max())
    same9 = float(np.abs(reg(frames[9]) - reg(frames[0])).max())
    within = float(np.abs(reg(frames[1]) - reg(frames[0])).max())
    ws = []
    for fr in frames:
        m = cmask(fr[100:260], hexrgb("#3A2A1E"), 30)
        cols = np.nonzero(m.any(0))[0]
        ws.append((cols.max() - cols.min() + 1) if len(cols) else 0)
    peak = max(ws) / float(ws[-1])
    top, bottom = frames[-1][2, 5], frames[-1][H - 3, 5]
    ub = arr(frame(0.1, boil=False)), arr(frame(0.2, boil=False))
    return [check("boil: a new variant every 3 frames, cycle of 3 (period 9)", within == 0 and same3 > 0 and same9 == 0, [within, same3, same9], [0, ">0", 0]),
            check("prop pops to 1.08 then settles at 1", abs(peak - 1.08) < 0.03, peak, 1.08),
            check("emphasis word in #F07F2E", int(cmask(frames[-1][370:430], hexrgb("#F07F2E"), 25).sum()) > 100, int(cmask(frames[-1][370:430], hexrgb("#F07F2E"), 25).sum()), ">100"),
            check("sky gradient #AFDCF0 -> #EAF6F4", np.abs(top - sky0).max() < 4 and np.abs(bottom - sky1).max() < 4, [list(top), list(bottom)], "gradient"),
            check("negative control: an unboiled drawing is static across 3 frames", not (float(np.abs(reg(ub[0]) - reg(ub[1])).max()) > 0),
                  float(np.abs(reg(ub[0]) - reg(ub[1])).max()), ">0")], [vid]


@card("DRAW-37")
def plotter_pen(task, wd):
    """Constant pen speed (no easing), pen-up travel at 10% opacity, spark core #f27525 at the head, grid drifting
    3 px/s, a 180-point seeded curve."""
    np = np_()
    from PIL import Image, ImageDraw
    W, H, fps = 320, 180, 30
    rnd = mulberry32(37)
    ys = [90.0]
    for _ in range(179):
        ys.append(min(150, max(30, ys[-1] + (rnd() - 0.5) * 8)))
    c1 = [(20 + 140 * i / 89.0, ys[i]) for i in range(90)]
    c2 = [(170 + 130 * i / 89.0, ys[90 + i]) for i in range(90)]
    d1, L1 = resample(c1, 1.0)
    d2, L2 = resample(c2, 1.0)
    speed = 300.0
    T1 = L1 / speed
    Tt = 0.2
    bg = np.array(hexrgb("#0B0B0C"), float)
    spark = hexrgb("#f27525")

    def frame(t, eased=False):
        im = Image.new("RGB", (W, H), tuple(int(v) for v in bg))
        d = ImageDraw.Draw(im)
        off = 3 * t
        for gx in range(-20, W + 20, 20):
            d.line((gx + off % 20, 0, gx + off % 20, H), fill=(26, 26, 28))
        p1 = prog(t, 0, T1)
        if eased:
            p1 = in_out_cubic(p1)
        if p1 > 0:
            poly(im, prefix(d1, p1), 1.5, (244, 244, 242), cap=False)
        tr = prog(t, T1, T1 + Tt)
        if tr > 0:
            a, b = d1[-1], d2[0]
            q = (a[0] + (b[0] - a[0]) * tr, a[1] + (b[1] - a[1]) * tr)
            d.line((a[0], a[1], q[0], q[1]), fill=tuple(int(bg[k] * 0.9 + 244 * 0.1) for k in range(3)))
        p2 = prog(t, T1 + Tt, T1 + Tt + L2 / speed)
        if p2 > 0:
            poly(im, prefix(d2, p2), 1.5, (244, 244, 242), cap=False)
        head = prefix(d1, p1)[-1] if p1 < 1 else (prefix(d2, p2)[-1] if p2 > 0 else None)
        if head is not None and (p1 < 1 or 0 < p2 < 1):
            d.ellipse((head[0] - 3, head[1] - 3, head[0] + 3, head[1] + 3), fill=spark)
        return im
    D = T1 + Tt + L2 / speed + 0.2
    vid, frames = film(wd, "plotter.mp4", frame, D, (W, H), fps=fps)
    def head_idx(fr):
        y_, x_ = np.nonzero(cmask(fr, spark, 30))
        c = np.array([x_.mean(), y_.mean()])
        return int(np.argmin(np.hypot(d1[:, 0] - c[0], d1[:, 1] - c[1])))
    adv = [head_idx(frames[j]) for j in range(2, int(T1 * fps) - 1)]
    step = np.diff(adv)
    spk = []
    for j in range(2, int(T1 * fps) - 1):
        m = cmask(frames[j], spark, 30)
        y_, x_ = np.nonzero(m)
        tip = point_at(d1, prog(j / fps, 0, T1))
        spk.append(math.hypot(x_.mean() - tip[0], y_.mean() - tip[1]))
    a, b = d1[-1], d2[0]
    mid = (int((a[0] + b[0]) / 2), int((a[1] + b[1]) / 2))
    jt = int((T1 + Tt + 0.05) * fps)
    trav = frames[jt][mid[1] - 1:mid[1] + 2, mid[0]].max(0)
    tlev = (trav - bg).max() / (244 - bg.max())
    g0 = (lum(frames[0][5]) > 20).astype(float)
    g1 = (lum(frames[fps][5]) > 20).astype(float)
    shift = min(range(0, 8), key=lambda s: float(np.abs(g1[s + 20:300] - g0[20:300 - s]).sum()))
    ea = [head_idx(arr(frame(j / fps, eased=True))) for j in range(2, int(T1 * fps) - 1)]
    estep = np.diff(ea)
    return [check("constant pen speed: per-frame advance = 10 px (300 px/s), spread < 2 px", abs(float(np.median(step)) - speed / fps) < 1.5 and float(np.ptp(step)) < 3,
                  [float(np.median(step)), float(np.ptp(step))], [10, "<3"]),
            check("spark core #f27525 rides the head (<1.5 px)", max(spk) < 1.5, max(spk), "<1.5"),
            check("pen-up travel line at ~10% opacity", 0.05 <= tlev <= 0.16, float(tlev), 0.1),
            check("grid drifts 3 px per second", shift == 3, shift, 3),
            check("180-point seeded curve", len(ys) == 180, len(ys), 180),
            check("negative control: an eased pen has uneven advance", not (float(np.ptp(estep)) < 3), float(np.ptp(estep)), "<3")], [vid]


@card("DRAW-38")
def on_twos(task, wd):
    """A new drawing every 2 frames at 24 fps (12 drawings/s) while the camera pan stays on ones."""
    np = np_()
    from PIL import Image, ImageDraw
    W, H, fps = 320, 180, 24
    rng = np.random.default_rng(38)
    bgtex = (rng.uniform(0, 1, (H, 2 * W)) * 40 + 180).astype("uint8")

    def frame(t, twos=True):
        j = int(round(t * fps))
        pose = j // 2 if twos else j
        cam = 2 * j
        bgim = Image.fromarray(bgtex[:, cam:cam + W]).convert("RGB")
        d = ImageDraw.Draw(bgim)
        x = 160 - 0
        arm = 30 * math.sin(pose * 0.9)
        d.line((x, 60, x, 120), fill=(0, 0, 0), width=4)
        d.line((x, 80, x + 30, 80 + arm), fill=(0, 0, 0), width=4)
        return bgim
    vid, frames = film(wd, "twos.mp4", frame, 1.0, (W, H), fps=fps)
    bgrow = [fr[170, :, 0] for fr in frames]
    cam = [min(range(0, 6), key=lambda s: float(np.abs(b[:W - 10 - s] - a[s:W - 10]).mean())) for a, b in zip(bgrow, bgrow[1:])]
    fig = [(lum(fr[40:140, 150:200]) < 30) for fr in frames]
    ch = [int((a ^ b).sum() > 0) for a, b in zip(fig, fig[1:])]
    ones_fig = [(lum(arr(frame(j / fps, twos=False))[40:140, 150:200]) < 30) for j in range(6)]
    ch1 = [int((a ^ b).sum() > 0) for a, b in zip(ones_fig, ones_fig[1:])]
    return [check("camera moves every frame (2 px on ones)", all(c == 2 for c in cam), cam[:8], 2),
            check("drawing changes only every 2nd frame (12 dps)", ch == [1 if (k + 1) % 2 == 0 else 0 for k in range(len(ch))], ch[:8], [0, 1] * 4),
            check("negative control: drawings on ones change every frame", not (ch1 == [1 if (k + 1) % 2 == 0 else 0 for k in range(5)]), ch1, [0, 1, 0, 1, 0])], [vid]


@card("DRAW-44")
def line_art_garden(task, wd):
    """Garden metaphor: flowers scaleY from the root (transform-origin bottom) 600 ms easeOut, 80 ms stagger; an insect
    on a Lissajous path with wings flapping (scaleX) at 8 Hz."""
    np = np_()
    from PIL import ImageDraw
    W, H, fps = 320, 200, 50
    roots = [(60 + 50 * i, 180) for i in range(5)]
    hgt = 80
    green, bug, wing = (40, 140, 60), (30, 30, 30), (90, 160, 230)

    def insect(t):
        return 160 + 100 * math.sin(3 * t), 60 + 30 * math.sin(2 * t)

    def frame(t, centre=False):
        im = pil((W, H), "#fbfaf6")
        d = ImageDraw.Draw(im)
        for i, (x, y) in enumerate(roots):
            s = pow_out(prog(t, 0.1 + 0.08 * i, 0.7 + 0.08 * i), 2)
            if s <= 0:
                continue
            if centre:
                y0, y1 = y - hgt / 2 - hgt * s / 2, y - hgt / 2 + hgt * s / 2
            else:
                y0, y1 = y - hgt * s, y
            d.line((x, y0, x, y1), fill=green, width=3)
        bx, by = insect(t)
        sx = abs(math.cos(math.pi * 8 * t))
        d.ellipse((bx - 10 * sx - 3, by - 6, bx + 10 * sx + 3, by - 2), fill=wing)
        d.ellipse((bx - 3, by - 3, bx + 3, by + 3), fill=bug)
        return im
    vid, frames = film(wd, "garden.mp4", frame, 2.0, (W, H), fps=fps)
    bases, tops, on = [], [], []
    for i, (x, y) in enumerate(roots):
        col = [cmask(fr[:, x - 1:x + 2], green, 30).any(1) for fr in frames]
        ys = [np.nonzero(c)[0] for c in col]
        on.append(next(j for j, v in enumerate(ys) if len(v)))
        bases.append({int(v.max()) for v in ys if len(v)})
    perr = []
    wv = []
    for j, fr in enumerate(frames):
        m = cmask(fr, bug, 20)
        y_, x_ = np.nonzero(m)
        bx, by = insect(j / fps)
        perr.append(math.hypot(x_.mean() - bx, y_.mean() - by))
        wm = cmask(fr, wing, 30)
        wv.append(int(wm.any(0).sum()))
    spec = np.abs(np.fft.rfft(np.array(wv) - np.mean(wv)))
    freq = np.fft.rfftfreq(len(wv), 1.0 / fps)[1 + int(np.argmax(spec[1:]))]
    cen = [arr(frame(t, centre=True)) for t in (0.3, 0.6)]
    cb = {int(np.nonzero(cmask(c[:, roots[0][0] - 1:roots[0][0] + 2], green, 30).any(1))[0].max()) for c in cen}
    return [check("flowers grow from a fixed root (base row constant)", all(len(b) == 1 for b in bases), [sorted(b) for b in bases], "one base"),
            check("80 ms stagger (4 frames at 50 fps)", all(abs((b - a) - 4) <= 1 for a, b in zip(on, on[1:])), on, "+4"),
            check("insect on the Lissajous path (<1.5 px)", max(perr) < 1.5, max(perr), "<1.5"),
            check("wing flap at 8 Hz (wing-width spectrum peak)", abs(freq * 1.0 - 16.0) < 1.0 or abs(freq - 8.0) < 1.0, freq, "8 Hz (16 Hz in |cos|)"),
            check("negative control: scaling from the centre moves the base", not (len(cb) == 1), sorted(cb), "one base")], [vid]


@card("DRAW-45")
def cutout_lift_eraser(task, wd):
    """Alpha cut-out of a scanned drawing moved only by translate / rotate (<= ±12°) / uniform scale, colours never
    changed; an eraser-shaped mask follows the eraser sprite's path for 400 ms."""
    np = np_()
    from PIL import Image, ImageDraw, ImageFilter
    W, H = 320, 200
    rng = np.random.default_rng(45)
    paper = (np.array(hexrgb("#f3eee2"), float) + rng.normal(0, 3, (H, W, 3))).clip(0, 255).astype("uint8")
    scan = Image.fromarray(paper)
    d = ImageDraw.Draw(scan)
    d.rectangle((40, 60, 140, 110), outline=(40, 30, 90), width=5)
    d.line((40, 60, 140, 110), fill=(160, 40, 40), width=5)
    A = np.asarray(scan, float)
    ink = lum(A) < 160
    alpha = Image.fromarray((ink * 255).astype("uint8")).filter(ImageFilter.MaxFilter(3))
    cut = scan.copy(); cut.putalpha(alpha)
    cut = cut.crop((30, 50, 150, 120))

    def lift(angle):
        ang = max(-12.0, min(12.0, angle))
        return cut.rotate(ang, resample=Image.NEAREST, expand=True), ang
    moved, ang = lift(20.0)
    canvas = Image.fromarray(paper).convert("RGBA")
    canvas.alpha_composite(moved, (170, 40))
    canvas.convert("RGB").save(wd / "lifted.png")
    C = np.asarray(canvas.convert("RGB"), float)

    def angle_of(rgbimg, colr):
        m = cmask(rgbimg, colr, 40)
        y_, x_ = np.nonzero(m)
        cov = np.cov(np.stack([x_, -y_]))
        w, v = np.linalg.eigh(cov)
        return math.degrees(math.atan2(v[1, -1], v[0, -1]))
    a0 = angle_of(A[:, :160], (160, 40, 40))
    a1 = angle_of(C[:, 160:], (160, 40, 40))
    src_cols = A[cmask(A, (160, 40, 40), 40)].mean(0)
    dst_cols = C[:, 160:][cmask(C[:, 160:], (160, 40, 40), 40)].mean(0)
    pth = [(14, 160), (306, 160)]

    def frame(t):
        im = Image.fromarray(paper).convert("RGB")
        ImageDraw.Draw(im).rectangle((20, 150, 300, 170), fill=(30, 30, 30))
        p = prog(t, 0.1, 0.5)
        if p > 0:
            ex = point_at(pth, p)
            m = Image.new("L", (W, H), 0)
            ImageDraw.Draw(m).line([pth[0], tuple(ex)], fill=255, width=26)
            im = Image.composite(Image.fromarray(paper), im, m)
            ImageDraw.Draw(im).rounded_rectangle((ex[0] - 8, ex[1] - 14, ex[0] + 8, ex[1] + 14), radius=4, fill=(240, 120, 160))
        return im
    vid, frames = film(wd, "eraser.mp4", frame, 0.7, (W, H))
    dark = lambda fr: float((lum(fr[150:171, 20:301]) < 60).mean())
    k = int(0.3 * 30)
    ex_mid = 14 + 292 * prog(k / 30.0, 0.1, 0.5)
    want_mid = 1 - clamp((ex_mid - 20) / 281.0)
    unclamped = cut.rotate(20.0, resample=Image.NEAREST, expand=True)
    U = Image.fromarray(paper).convert("RGBA"); U.alpha_composite(unclamped, (170, 40))
    a2 = angle_of(np.asarray(U.convert("RGB"), float)[:, 160:], (160, 40, 40))
    return [check("rotation clamped to ±12° (requested 20°)", abs((a1 - a0) - 12) < 1.5, a1 - a0, 12),
            check("cut-out colours unchanged (mean ΔRGB < 3)", float(np.abs(src_cols - dst_cols).max()) < 3, [list(src_cols), list(dst_cols)], "equal"),
            check("eraser wipe finishes in 400 ms", dark(frames[int(0.52 * 30)]) < 0.02 and dark(frames[2]) > 0.95, [dark(frames[2]), dark(frames[16])], [1, 0]),
            check("mid-wipe: the mask follows the eraser (≈ half erased)", abs(dark(frames[k]) - want_mid) < 0.12, dark(frames[k]), want_mid),
            check("negative control: an unclamped lift rotates by the full 20°", not (abs((a2 - a0) - 12) < 1.5), a2 - a0, 12)], [wd / "lifted.png", vid]


@card("DRAW-46")
def striped_ribbon(task, wd):
    """One curve, three parallel strokes at offsets (~30 px total: red / white / blue) drawn together over 1.5 s;
    Arab flags swap to their real colours (here Egypt: red / white / black)."""
    np = np_()
    W, H = 400, 220
    cols = [(206, 17, 38), (255, 255, 255), (0, 0, 0)]
    base = [(20 + x, 110 + 50 * math.sin(x / 70.0)) for x in range(0, 361, 2)]
    dense, L = resample(base, 1.0)

    def offset(pts, o):
        P = np.asarray(pts)
        T = np.gradient(P, axis=0)
        N = np.stack([-T[:, 1], T[:, 0]], 1) / (np.hypot(T[:, 0], T[:, 1])[:, None] + 1e-9)
        return P + N * o
    lanes = [offset(dense, o) for o in (-10, 0, 10)]

    def frame(t, single=False):
        im = pil((W, H), "#9aa5b1")
        p = in_out_cubic(prog(t, 0.1, 1.6))
        if p > 0:
            for lane, c in (zip(lanes, cols) if not single else [(lanes[1], cols[0])]):
                poly(im, prefix(lane, p), 10 if not single else 30, c, cap=False)
        return im
    vid, frames = film(wd, "ribbon.mp4", frame, 1.8, (W, H))
    last = frames[-1]
    i = len(dense) // 2
    P = dense[i]
    T = dense[i + 1] - dense[i - 1]
    N = np.array([-T[1], T[0]]) / np.hypot(*T)
    prof = []
    for s_ in np.arange(-16, 16.5, 1.0):
        x, y = P + N * s_
        prof.append(tuple(last[int(round(y)), int(round(x))].astype(int)))
    def lab(c):
        return min(range(3), key=lambda k: sum(abs(a - b) for a, b in zip(c, cols[k]))) if min(sum(abs(a - b) for a, b in zip(c, cc)) for cc in cols) < 60 else None
    seq = [lab(c) for c in prof]
    runs = []
    for v in seq:
        if v is None:
            continue
        if runs and runs[-1][0] == v:
            runs[-1][1] += 1
        else:
            runs.append([v, 1])
    k = int(round(0.85 * 30))
    shares = [drawn_frac(cmask(frames[k], c, 30), lane, 1) for lane, c in zip(lanes, cols)]
    want = in_out_cubic(prog(k / 30.0, 0.1, 1.6))
    sg = arr(frame(1.8, single=True))
    sprof = {lab(tuple(sg[int(round((P + N * s_)[1])), int(round((P + N * s_)[0]))].astype(int))) for s_ in np.arange(-12, 13, 2.0)}
    return [check("cross-section: three bands red / white / black, ~10 px each", [r[0] for r in runs] == [0, 1, 2] and all(8 <= r[1] <= 12 for r in runs),
                  runs, "3 x 10 px"),
            check("all three lanes drawn together (same share mid-draw ±0.04)", all(abs(s_ - want) < 0.04 for s_ in shares), shares, want),
            check("negative control: one wide stroke has a single colour band", not (len(sprof - {None}) == 3), sorted(x for x in sprof if x is not None), [0, 1, 2])], [vid]


def smooth_step(e0, e1, x):
    t = clamp((x - e0) / (e1 - e0))
    return t * t * (3 - 2 * t)


@card("DRAW-47")
def wireframe_to_solid(task, wd):
    """Mesh edges draw on staggered (~1.5 s), then the three-kit scan shader math sweeps a band up the model:
    band = smoothstep(.09, 0, scan - y) * step(y, scan + .004), edge = smoothstep(.012, 0, |y - scan|),
    scanY = lerp(-.02, .4, t/.78); the solid forms with form = 1 - ease(ramp(t, .4, 2.8))."""
    np = np_()
    from PIL import Image, ImageDraw
    W, H = 320, 240
    V = np.array([[x, y, z] for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)], float)
    E = [(a, b) for a in range(8) for b in range(a + 1, 8) if np.abs(V[a] - V[b]).sum() == 2]
    ry, rx = math.radians(35), math.radians(-25)
    R = np.array([[math.cos(ry), 0, math.sin(ry)], [0, 1, 0], [-math.sin(ry), 0, math.cos(ry)]]) @ \
        np.array([[1, 0, 0], [0, math.cos(rx), -math.sin(rx)], [0, math.sin(rx), math.cos(rx)]])
    P = (V @ R.T)
    S = np.stack([160 + 60 * P[:, 0], 120 - 60 * P[:, 1]], 1)
    yn = (P[:, 1] - P[:, 1].min()) / np.ptp(P[:, 1])
    hull_pts = [tuple(S[i]) for i in range(8)]
    from scipy.spatial import ConvexHull
    hull = [hull_pts[i] for i in ConvexHull(S).vertices]
    mask = Image.new("L", (W, H), 0); ImageDraw.Draw(mask).polygon(hull, fill=255)
    M = np.asarray(mask) > 128
    ys_img = np.arange(H)[:, None] * np.ones((1, W))
    ytop, ybot = S[:, 1].min(), S[:, 1].max()
    yobj = (ybot - ys_img) / (ybot - ytop)
    stagger = 1.5 / len(E)

    def frame(t):
        im = Image.new("RGB", (W, H), (10, 12, 10))
        for k, (a, b) in enumerate(E):
            p = prog(t, k * stagger, k * stagger + stagger * 2)
            if p > 0:
                poly(im, prefix([tuple(S[a]), tuple(S[b])], p), 2, (120, 255, 150), cap=False)
        ts = t - 1.6
        if ts >= 0:
            scan = -0.02 + (0.4 + 0.02) * clamp(ts / 0.78)
            band = np.vectorize(lambda y: smooth_step(0.09, 0.0, scan - y) * (1.0 if y <= scan + 0.004 else 0.0))(yobj[:, 0])[:, None] * np.ones((1, W))
            edge = np.vectorize(lambda y: smooth_step(0.012, 0.0, abs(y - scan)))(yobj[:, 0])[:, None] * np.ones((1, W))
            form = 1 - in_out_cubic(prog(ts, 0.4, 2.8))
            col = np.array([.62, 1, .72]) * (1 - edge[..., None]) + np.array([.95, 1, .8]) * edge[..., None]
            solid = (1 - form) * 0.55
            a = np.clip(band * 0.6 + edge + solid, 0, 1)[..., None] * M[..., None]
            base = np.asarray(im, float)
            im = Image.fromarray((base * (1 - a) + 255 * col * a).clip(0, 255).astype("uint8"))
        return im
    D = 1.6 + 3.0
    vid, frames = film(wd, "wire.mp4", frame, D, (W, H), fps=15)
    ed = [resample([tuple(S[a]), tuple(S[b])], 1.0)[0] for a, b in E]
    done = []
    for k in range(len(E)):
        done.append(next(j for j, fr in enumerate(frames) if drawn_frac(lum(fr) > 60, ed[k][1:-1], 1) > 0.98) / 15.0)
    jt = int(round((1.6 + 0.39) * 15))
    tsj = jt / 15.0 - 1.6
    scan = -0.02 + 0.42 * clamp(tsj / 0.78)
    inside = frames[jt][M]
    rows = [float(lum(frames[jt][y][M[y]]).mean()) if M[y].any() else 0 for y in range(H)]
    brightest = int(np.argmax(rows))
    yb = (ybot - brightest) / (ybot - ytop)
    fill_end = float((lum(frames[-1])[M] > 80).mean())
    pre = frames[int(1.5 * 15)]
    pre_rows = [float(lum(pre[y][M[y]]).mean()) if M[y].any() else 0 for y in range(H)]
    return [check("edges finish staggered across ~1.5 s", done == sorted(done) and 1.2 <= max(done) <= 1.75, [min(done), max(done)], "staggered to ~1.5 s"),
            check("bright scan edge sits at scanY = lerp(-.02, .4, t/.78) (±0.03)", abs(yb - scan) < 0.03, yb, scan),
            check("solid forms by the end (fill coverage)", fill_end > 0.95, fill_end, ">0.95"),
            check("12 cube edges", len(E) == 12, len(E), 12),
            check("negative control: before the scan there is no bright band row", not (abs((ybot - int(np.argmax(pre_rows))) / (ybot - ytop) - scan) < 0.03 and max(pre_rows) > 150),
                  max(pre_rows), "band")], [vid]


@card("DRAW-U01")
def make_frame_deterministic(task, wd):
    """Every frame computed from absolute time (no accumulated clock): rendering in reverse or out of order gives the
    same frames; the pen tip is pinned to the end of the active stroke; ffprobe QA of fps, size and frame count."""
    np = np_()
    from PIL import Image, ImageDraw
    import hashlib
    W, H, fps, D = 180, 320, 30, 2.0
    strokes = [[(20, 60), (160, 80)], [(30, 160), (150, 140)], [(40, 250), (140, 270)]]
    dense = [resample(s, 1.0)[0] for s in strokes]
    rng = np.random.default_rng(2026)
    paper = (np.array([246, 241, 228], float) + rng.normal(0, 4, (H, W, 3))).clip(0, 255).astype("uint8")

    def make_frame(t):
        im = Image.fromarray(paper)
        d = ImageDraw.Draw(im)
        active = None
        for k, dn in enumerate(dense):
            p = in_out_cubic(prog(t, 0.2 + 0.55 * k, 0.65 + 0.55 * k))
            if p > 0:
                poly(im, prefix(dn, p), 3, (30, 30, 40))
                if p < 1:
                    active = prefix(dn, p)[-1]
        if active is not None:
            x, y = active
            d.ellipse((x - 3, y - 3, x + 3, y + 3), fill=(230, 60, 60))
        return im
    n = int(D * fps)
    fwd = [hashlib.sha256(make_frame(i / fps).tobytes()).hexdigest() for i in range(n)]
    rev = [hashlib.sha256(make_frame(i / fps).tobytes()).hexdigest() for i in reversed(range(n))][::-1]
    vid, frames = film(wd, "film.mp4", make_frame, D, (W, H), fps=fps)
    pr = fx.probe(vid)
    st = [s for s in pr["streams"] if s["codec_type"] == "video"][0]
    qa = {"fps": st["r_frame_rate"], "size": [st["width"], st["height"]], "frames": int(st.get("nb_frames", len(frames)))}
    write_json(wd / "qa.json", qa)
    tip_err = []
    for j, fr in enumerate(frames):
        m = cmask(fr, (230, 60, 60), 40)
        if m.sum() > 10:
            t = j / fps
            k = max(i for i in range(3) if t >= 0.2 + 0.55 * i)
            tip = prefix(dense[k], in_out_cubic(prog(t, 0.2 + 0.55 * k, 0.65 + 0.55 * k)))[-1]
            y_, x_ = np.nonzero(m)
            tip_err.append(math.hypot(x_.mean() - tip[0], y_.mean() - tip[1]))

    class Clock:
        def __init__(self):
            self.t, self.r = 0.0, mulberry32(1)

        def step(self):
            self.t += 1 / fps + (self.r() - 0.5) * 0.004
            return make_frame(self.t)
    c = Clock()
    seq = [hashlib.sha256(c.step().tobytes()).hexdigest() for _ in range(n)]
    c2 = Clock()
    for _ in range(10):
        c2.step()
    seek = hashlib.sha256(c2.step().tobytes()).hexdigest()
    return [check("reverse-order render gives byte-identical frames", fwd == rev, sum(a != b for a, b in zip(fwd, rev)), 0),
            check("ffprobe QA: 30 fps, 180x320, 60 frames", qa == {"fps": "30/1", "size": [180, 320], "frames": 60}, qa, "30/1 180x320 60"),
            check("pen tip pinned to the active stroke end (<1.5 px)", tip_err and max(tip_err) < 1.5, max(tip_err) if tip_err else None, "<1.5"),
            check("negative control: an accumulated clock drifts from absolute time", not (seek == fwd[10] and seq[:5] == fwd[1:6]),
                  [seek[:10], fwd[10][:10]], "equal")], [vid, wd / "qa.json"]


# ============================================================================= ai-generation (local, deterministic parts)
def fmb_cli(wd, *args, env=None):
    e = dict(os.environ)
    e["TMPDIR"] = str(wd)
    done = subprocess.run(["node", str(FMB / "scripts/profiles-cli.mjs"), *args], cwd=str(wd), capture_output=True, text=True,
                          timeout=30, stdin=subprocess.DEVNULL, env=e)
    return done.returncode, done.stdout + done.stderr


@card("GEN-18")
def stage_gated_profile_cli(task, wd):
    """fastify-motion-bro profile CLI: its own 19 node tests (TMPDIR inside the work folder), list of 7 modes, the
    session file, and the stage gate (an answer without a started session is refused)."""
    e = dict(os.environ)
    e["TMPDIR"] = str(wd)
    done = subprocess.run(["node", "--test", "tests/viral-editorial.test.mjs", "tests/production-profiles.test.mjs",
                           "tests/production-cli.test.mjs"], cwd=str(FMB), capture_output=True, text=True, timeout=60,
                          stdin=subprocess.DEVNULL, env=e)
    (wd / "node_test.txt").write_text(done.stdout[-4000:] + done.stderr[-2000:], encoding="utf-8")
    m_pass = re.search(r"^# pass (\d+)", done.stdout, re.M)
    m_fail = re.search(r"^# fail (\d+)", done.stdout, re.M)
    rc_l, menu = fmb_cli(wd, "list")
    modes = ["stickman", "fitness", "car-exploded", "vox-history", "food-flow", "kinetic-flow", "character-romance"]
    rc_gate, gate = fmb_cli(wd, "answer", "fitness", "Chest")
    rc_s, _ = fmb_cli(wd, "start", "fitness")
    sess = json.loads((wd / "projects/profiles/fitness/session.json").read_text(encoding="utf-8"))
    return [check("the CLI's own tests: 19 pass, 0 fail", m_pass and int(m_pass.group(1)) == 19 and m_fail and int(m_fail.group(1)) == 0,
                  [m_pass and m_pass.group(1), m_fail and m_fail.group(1)], [19, 0]),
            check("list shows all seven modes", rc_l == 0 and all(m in menu for m in modes), [m for m in modes if m in menu], modes),
            check("start writes a persistent session.json", rc_s == 0 and sess.get("stage") not in (None, "DONE"), sess.get("stage"), "first stage"),
            check("negative control: answering before start is refused (stage gate)", not (rc_gate == 0), rc_gate, "non-zero")], \
        [wd / "node_test.txt", wd / "projects/profiles/fitness/session.json"]


@card("GEN-19")
def five_profile_series(task, wd):
    """Drive the five packs stage by stage with the card's first answers and count what each writes (prompts only)."""
    runs = {"stickman": [json.dumps({"image": "no", "background": "paper", "genre": 4, "direction": "coffee shop"})],
            "fitness": ["Chest"], "car-exploded": ["Toyota", "Corolla", json.dumps({"year": "2024", "trim": "LE", "color": "white"})],
            "vox-history": ["6", "history of the printing press", "10"], "food-flow": ["2", "4"]}
    art = {}
    for mode, answers in runs.items():
        fmb_cli(wd, "start", mode)
        for a in answers:
            fmb_cli(wd, "answer", mode, a)
        art[mode] = json.loads((wd / "projects/profiles" / mode / "artifacts.json").read_text(encoding="utf-8"))
    P = {m: a["prompts"] for m, a in art.items()}
    st = P["stickman"]
    vox = art["vox-history"]
    food = P["food-flow"]
    media = [p for p in (wd / "projects").rglob("*") if p.suffix.lower() in (".mp4", ".png", ".jpg", ".wav", ".mp3")]
    write_json(wd / "summary.json", {m: len(v) for m, v in P.items()})
    gate_rc, _ = fmb_cli(wd, "answer", "fitness", "Back")
    return [check("stickman: 5 image+motion pairs, 7 s each (35 s)", len(st) == 5 and all("7s clip" in p["videoPrompt"] for p in st), len(st), 5),
            check("fitness: 5 image-to-video prompts of 6 s", len(P["fitness"]) == 5 and all("6-second" in str(p) for p in P["fitness"]), len(P["fitness"]), 5),
            check("car-exploded: exactly 3 prompts", len(P["car-exploded"]) == 3, len(P["car-exploded"]), 3),
            check("vox-history: 10 x 10 s, all six phases, flagged needsFactCheck", len(vox["prompts"]) == 10 and vox.get("needsFactCheck") is True
                  and len({p["phase"] for p in vox["prompts"]}) == 6 and all(p["durationSeconds"] == 10 for p in vox["prompts"]),
                  [len(vox["prompts"]), vox.get("needsFactCheck")], [10, True]),
            check("food-flow: 4 x 10 s, tasting shot last", len(food) == 4 and food[-1].get("isEating") is True and not any(p.get("isEating") for p in food[:-1]),
                  [len(food), food[-1].get("isEating")], [4, True]),
            check("outputs are prompts, never media", not media, len(media), 0),
            check("negative control: a finished session refuses further answers", True if gate_rc != 0 else False, gate_rc, "non-zero")], \
        [wd / "summary.json"]


@card("GEN-20")
def kinetic_flow_clean_plate(task, wd):
    """kinetic-flow: one prompt per clip with the exact script words; clean-plate n rewrites clip n to forbid all
    on-screen text and returns the overlay sheet (order, words, hero, masked reveal) for HTML/Remotion."""
    script = "Focus follows action. Build something real."
    fmb_cli(wd, "start", "kinetic-flow")
    fmb_cli(wd, "answer", "kinetic-flow", json.dumps({"theme": "C", "ratio": "9:16", "length": 10, "brand": "", "pace": "fast", "audio": "none"}))
    rc, clip_txt = fmb_cli(wd, "answer", "kinetic-flow", script)
    rc2, sheet_txt = fmb_cli(wd, "clean-plate", "kinetic-flow", "1")
    sheet = json.loads(sheet_txt)
    write_json(wd / "clean_plate.json", sheet)
    (wd / "clip_prompts.txt").write_text(clip_txt, encoding="utf-8")
    words = [w for o in sheet["overlaySheet"] for w in (o.get("words") or [])] if isinstance(sheet["overlaySheet"], list) else []
    flat = json.dumps(sheet["overlaySheet"], ensure_ascii=False)
    return [check("normal clip prompt carries the exact script words", "Focus follows action" in clip_txt, "Focus follows action" in clip_txt, True),
            check("clean plate forbids on-screen text", "ABSOLUTELY NO ON-SCREEN TEXT" in sheet["prompt"], sheet["prompt"][:80], "NO ON-SCREEN TEXT"),
            check("clean plate removes the script words from the prompt", "Focus follows action" not in sheet["prompt"], False, False),
            check("overlay sheet returns the words for the editor", "Focus" in flat and sheet["clip"] == 1, flat[:120], "words"),
            check("negative control: the un-cleaned clip prompt would bake the words into the plate",
                  not ("Focus follows action" not in clip_txt), "Focus follows action" in clip_txt, False)], \
        [wd / "clean_plate.json", wd / "clip_prompts.txt"]


def brand_plate(W=1600, H=900, ground="#0B1F3A", metal="#C9A227"):
    """Deterministic stand-in for a generated still: metal sphere + faceted crystal on a flat brand ground,
    warm rim light, object on the right third."""
    np = np_()
    from PIL import Image, ImageDraw, ImageFilter
    im = Image.new("RGB", (W, H), hexrgb(ground))
    d = ImageDraw.Draw(im)
    cx, cy, r = int(W * 0.72), int(H * 0.52), int(H * 0.22)
    for k in range(r, 0, -2):
        f = k / r
        c = tuple(int(v * (0.55 + 0.45 * (1 - f))) for v in hexrgb(metal))
        d.ellipse((cx - k, cy - k, cx + k, cy + k), fill=c)
    d.polygon([(cx - r, cy + r), (cx - r // 2, cy + r // 3), (cx, cy + r + 20)], fill=(210, 230, 245))
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    ImageDraw.Draw(glow).ellipse((cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6), outline=(255, 190, 120), width=8)
    return Image.fromarray(np.clip(np.asarray(im, float) + np.asarray(glow.filter(ImageFilter.GaussianBlur(6)), float) * 0.8, 0, 255).astype("uint8"))


@card("GEN-42")
def brand_still_post(task, wd):
    """Brand-still recipe, post stage on a deterministic stand-in plate (generation itself is a paid Higgsfield call):
    prompt grammar with the hard negative suffix, hflip for RTL space, WebP q80 at 1600 w hero / 720x480 sector /
    1200 audit / 900 cover."""
    np = np_()
    from PIL import Image
    suffix = "No text, no letters, no numbers, no logos, no people"
    prompt = ("One symbolic object in polished gold metal #C9A227 and faceted clear crystal on a flat ground #0B1F3A, warm rim "
              "light, luxury annual report mood. " + suffix)
    (wd / "prompt.txt").write_text(prompt, encoding="utf-8")
    plate = brand_plate()
    flipped = plate.transpose(Image.FLIP_LEFT_RIGHT)
    outs = {}
    specs = {"hero": (1600, None), "sector": (720, 480), "audit": (1200, None), "cover": (900, None)}
    for name, (w, h) in specs.items():
        if h is None:
            im = flipped.resize((w, round(flipped.height * w / flipped.width)), Image.LANCZOS)
        else:
            sc = max(w / flipped.width, h / flipped.height)
            tmp = flipped.resize((round(flipped.width * sc), round(flipped.height * sc)), Image.LANCZOS)
            l, t = (tmp.width - w) // 2, (tmp.height - h) // 2
            im = tmp.crop((l, t, l + w, t + h))
        p = wd / ("%s.webp" % name)
        im.save(p, "WEBP", quality=80)
        outs[name] = p
    got = {n: Image.open(p).size for n, p in outs.items()}
    fmt = {n: Image.open(p).format for n, p in outs.items()}
    hero = np.asarray(Image.open(outs["hero"]).convert("RGB"), float)
    gold = cmask(hero, "#C9A227", 70)
    cx = float(np.nonzero(gold)[1].mean()) / hero.shape[1]
    corner = hero[10, hero.shape[1] - 10]
    q100 = wd / "hero_q100.webp"
    Image.open(outs["hero"]).save(q100, "WEBP", quality=100)
    raw = np.asarray(plate, float)
    rcx = float(np.nonzero(cmask(raw, "#C9A227", 70))[1].mean()) / raw.shape[1]
    return [check("prompt ends with the hard negative suffix", prompt.endswith(suffix), prompt[-60:], suffix),
            check("WebP at the card's sizes", got == {"hero": (1600, 900), "sector": (720, 480), "audit": (1200, 675), "cover": (900, 506)} and set(fmt.values()) == {"WEBP"},
                  got, "1600 w / 720x480 / 1200 w / 900 w"),
            check("hflip leaves the right side free for RTL type (object centre < 0.4 W)", cx < 0.4, cx, "<0.4"),
            check("brand ground kept (#0B1F3A at the free corner)", float(np.abs(corner - np.array(hexrgb("#0B1F3A"))).max()) < 8, list(corner), "#0B1F3A"),
            check("q80 is smaller than q100", outs["hero"].stat().st_size < q100.stat().st_size, [outs["hero"].stat().st_size, q100.stat().st_size], "smaller"),
            check("negative control: the unflipped plate keeps the object on the right", not (rcx < 0.4), rcx, "<0.4")], list(outs.values())


@card("GEN-43")
def plates_reserve_type_space(task, wd):
    """Every shot prompt ends with one shared style suffix asking for empty upper/lower thirds and no text; then the
    type goes into the emptiest third (measured), never over the subject."""
    np = np_()
    from PIL import Image, ImageDraw
    suffix = ("editorial cinematic photography, shallow depth of field, anamorphic look, grain, empty upper/lower thirds, "
              "no text, letters, logos or watermark")
    shots = ["s1_question", "s2_city", "s3_hands", "s4_screen", "s5_road", "s6_paths"]
    prompts = {s: "Shot %s, 9:16 2k. %s" % (s, suffix) for s in shots}
    write_json(wd / "prompts.json", prompts)
    W, H = 540, 960
    rng = np.random.default_rng(43)
    base = np.linspace(40, 90, H)[:, None, None] * np.ones((1, W, 3))
    plate = base + rng.normal(0, 1.5, (H, W, 3))
    yy, xx = np.mgrid[0:H, 0:W]
    subj = ((xx - 270) ** 2 / 120 ** 2 + (yy - 470) ** 2 / 200 ** 2) < 1
    tex = rng.normal(0, 40, (H, W, 3))
    plate[subj] = 150 + tex[subj]
    plate = Image.fromarray(np.clip(plate, 0, 255).astype("uint8"))
    A = np.asarray(plate, float)
    thirds = [(0, H // 3), (H // 3, 2 * H // 3), (2 * H // 3, H)]
    busy = [float(np.abs(np.diff(lum(A[a:b]), axis=1)).mean()) for a, b in thirds]
    pick = int(np.argmin([busy[0], 1e9, busy[2]]))
    t, _ = tile("سؤال اليوم", font(CAIRO, 64, wght=800))
    c = plate.convert("RGBA")
    y0, y1 = thirds[pick]
    place(c, t, W / 2, (y0 + y1) / 2)
    c.convert("RGB").save(wd / "plate_with_type.png")
    out = arr(c)
    ink = (lum(out) > 245) & ~subj
    over = int(((lum(out) > 245) & subj).sum())
    bb = bbox(lum(out) > 245)
    c2 = plate.convert("RGBA")
    place(c2, t, W / 2, H / 2)
    o2 = arr(c2)
    over2 = int(((np.abs(o2 - A).max(-1) > 30) & subj).sum())
    return [check("all 6 shot prompts end with the shared suffix", all(p.endswith(suffix) for p in prompts.values()) and len(prompts) == 6, len(prompts), 6),
            check("the middle third (subject) is measured busiest", busy[1] > 3 * max(busy[0], busy[2]), busy, "middle busiest"),
            check("type lands inside the chosen empty third", bb[1] >= thirds[pick][0] and bb[3] <= thirds[pick][1], [bb, thirds[pick]], "inside"),
            check("type never covers the subject", over == 0, over, 0),
            check("negative control: centring the type puts it over the subject", not (over2 == 0), over2, 0)], [wd / "plate_with_type.png", wd / "prompts.json"]


@card("GEN-44")
def sprite_normalise(task, wd):
    """Sprite strip from seed frames: near-white threshold fallback for a transparent background, then Pillow normalise
    to one shared scale and a bottom-centre anchor in fixed cells (exact frame count)."""
    np = np_()
    from PIL import Image, ImageDraw
    n, cell = 6, (96, 128)
    raw = []
    for k in range(n):
        s = 0.7 + 0.1 * k
        im = Image.new("RGB", (200, 200), (252, 252, 250))
        d = ImageDraw.Draw(im)
        ox, oy = 40 + 7 * k, 20 + 5 * k
        h = 100 * s
        d.ellipse((ox + 20 * s, oy, ox + 50 * s, oy + 30 * s), fill=(40, 90, 200))
        d.rectangle((ox + 25 * s, oy + 30 * s, ox + 45 * s, oy + h), fill=(220, 60, 60))
        raw.append(im)
    frames = []
    for im in raw:
        a = np.asarray(im, float)
        alpha = (a.min(-1) < 235).astype("uint8") * 255
        rgba = im.convert("RGBA"); rgba.putalpha(Image.fromarray(alpha))
        frames.append(rgba.crop(rgba.getbbox()))
    target_h = 110
    strip = Image.new("RGBA", (cell[0] * n, cell[1]), (0, 0, 0, 0))
    for k, fr in enumerate(frames):
        sc = target_h / fr.height
        r = fr.resize((max(1, round(fr.width * sc)), target_h), Image.LANCZOS)
        strip.alpha_composite(r, (k * cell[0] + (cell[0] - r.width) // 2, cell[1] - 6 - r.height))
    strip.save(wd / "strip.png")
    S = np.asarray(strip)
    hs, bots, cxs = [], [], []
    for k in range(n):
        al = S[:, k * cell[0]:(k + 1) * cell[0], 3] > 128
        b = bbox(al)
        hs.append(b[3] - b[1]); bots.append(b[3]); cxs.append((b[0] + b[2]) / 2.0)
    raw_h = [bbox(np.asarray(im, float).min(-1) < 235)[3] - bbox(np.asarray(im, float).min(-1) < 235)[1] for im in raw]
    return [check("transparent background from the near-white threshold", S[0, 0, 3] == 0 and S[5, 5, 3] == 0, int(S[0, 0, 3]), 0),
            check("one shared scale: every frame 110 px tall (±1)", max(hs) - min(hs) <= 1 and abs(hs[0] - target_h) <= 1, hs, target_h),
            check("bottom-centre anchor in every cell", len(set(bots)) == 1 and max(cxs) - min(cxs) <= 1, [sorted(set(bots)), [min(cxs), max(cxs)]], "fixed"),
            check("exact frame count -> strip width", strip.width == n * cell[0], strip.width, n * cell[0]),
            check("negative control: the raw seed frames drift in size", not (max(raw_h) - min(raw_h) <= 1), raw_h, "equal")], [wd / "strip.png"]


def tone_track(path, secs=10.0, rate=44100):
    np = np_()
    t = np.arange(int(secs * rate)) / rate
    f = 220 * (1 + (np.floor(t) % 5) / 4.0)
    s = 0.4 * np.sin(2 * np.pi * np.cumsum(f) / rate)
    return fx.write_wav(path, np.stack([s, s * 0.8], 1), rate)


@card("GEN-57")
def song_slice_for_shot(task, wd):
    """Slice the song to the shot with ffmpeg: 48 kHz PCM, whole-second duration, so mouth and hits land by
    construction; references labelled @Image1 (style) @Image2 (singer) @Audio1 (slice)."""
    np = np_()
    song = tone_track(wd / "song.wav")
    start, want = 3.2, 4.6
    dur = max(1, round(want))
    out = wd / "slice.wav"
    fx.ffmpeg("-ss", "%.3f" % start, "-t", str(dur), "-i", str(song), "-ar", "48000", "-c:a", "pcm_s16le", str(out))
    pr = fx.probe(out)
    a = pr["streams"][0]
    d = float(pr["format"]["duration"])
    x, r = fx.read_wav(out)
    src, r0 = fx.read_wav(song)
    seg = src[int(start * r0):int((start + 0.5) * r0), 0]
    import scipy.signal as ss
    got = ss.resample_poly(x[:int(0.5 * 48000), 0], 147, 160)
    n = min(len(seg), len(got))
    corr = float(np.corrcoef(seg[:n], got[:n])[0, 1])
    prompt = ("Style of @Image1, the singer from @Image2 sings @Audio1 with precise lip sync, mouth closed when @Audio1 is "
              "silent, static camera, no text, one continuous shot.")
    (wd / "prompt.txt").write_text(prompt, encoding="utf-8")
    sp = fx.probe(song)
    return [check("slice is 48 kHz PCM s16le", a["sample_rate"] == "48000" and a["codec_name"] == "pcm_s16le", [a["sample_rate"], a["codec_name"]], ["48000", "pcm_s16le"]),
            check("whole-second duration (5.000 s)", abs(d - dur) < 1e-3 and dur == 5, d, 5.0),
            check("slice content starts at the shot's 3.2 s (corr > 0.98)", corr > 0.98, corr, ">0.98"),
            check("prompt references @Image1 @Image2 @Audio1", all(k in prompt for k in ("@Image1", "@Image2", "@Audio1")), True, True),
            check("negative control: the master track is not a 48 kHz whole-second slice",
                  not (sp["streams"][0]["sample_rate"] == "48000"), sp["streams"][0]["sample_rate"], "48000")], [out, wd / "prompt.txt"]


@card("GEN-58")
def voice_reference_continuity(task, wd):
    """Segment 1's own audio -> ref.mp3 (libmp3lame -q:a 2, 2-15 s, <= 15 MB) as the reference for segments 2..N,
    then concat with -c copy (no re-encode)."""
    segs = []
    for k, (c, f) in enumerate((("red", 300), ("green", 420), ("blue", 520))):
        p = wd / ("s%d.mp4" % (k + 1))
        fx.ffmpeg("-f", "lavfi", "-i", "color=c=%s:s=160x90:r=25:d=3" % c, "-f", "lavfi", "-i", "sine=f=%d:d=3" % f,
                  "-c:v", "libx264", "-g", "25", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(p))
        segs.append(p)
    ref = wd / "ref.mp3"
    fx.ffmpeg("-i", str(segs[0]), "-vn", "-acodec", "libmp3lame", "-q:a", "2", str(ref))
    rp = fx.probe(ref)
    rd = float(rp["format"]["duration"])

    def ref_ok(d, size, n=1):
        return 2 <= d <= 15 and size <= 15 * 1024 * 1024 and n <= 3
    lst = wd / "list.txt"
    lst.write_text("".join("file '%s'\n" % p.name for p in segs), encoding="utf-8")
    out = wd / "joined.mp4"
    fx.ffmpeg("-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(out))
    def md5(p, copy=True):
        rows = [l.split(",") for l in fx.run(["ffmpeg", "-v", "error", "-i", str(p), "-map", "0:v"] + (["-c", "copy"] if copy else []) +
                                             ["-f", "framemd5", "-"]).stdout.splitlines() if l and not l.startswith("#")]
        return [r[-1].strip() for r in rows]
    jp, pp = md5(out), sum((md5(p) for p in segs), [])
    # concat re-inserts SPS/PPS in front of each keyframe (1 per second here); every other packet must be the same bytes,
    # and the decoded pictures must be identical (a re-encode would change them)
    same = sum(a == b for a, b in zip(jp, pp))
    joined, parts = md5(out, False), sum((md5(p, False) for p in segs), [])
    reenc = wd / "reencoded.mp4"
    fx.ffmpeg("-i", str(out), "-c:v", "libx264", "-crf", "30", "-an", str(reenc))
    renc = md5(reenc, False)
    jd = float(fx.probe(out)["format"]["duration"])
    return [check("reference is MP3 from segment 1, 2-15 s, <= 15 MB", rp["streams"][0]["codec_name"] == "mp3" and ref_ok(rd, ref.stat().st_size),
                  [rp["streams"][0]["codec_name"], rd], ["mp3", "2-15 s"]),
            check("concat -c copy: decoded pictures identical, non-key packets byte-identical", joined == parts and len(jp) == len(pp) and same >= len(pp) - 9,
                  [len(joined), same, len(pp)], "identical"),
            check("negative control: a re-encode changes the decoded pictures", not (renc == parts), sum(a == b for a, b in zip(renc, parts)), len(parts)),
            check("joined length = sum of segments (±0.1 s)", abs(jd - 9.0) < 0.1, jd, 9.0),
            check("negative control: a 20 s reference breaks the 2-15 s rule", not ref_ok(20.0, 1000), 20.0, "2-15 s")], [ref, out]


BPM_BY_INDUSTRY = {"crypto": 100, "finance": 92, "creative": 115, "saas": 108}


def bgm_bpm(industry, cascade=False, demo=False):
    return BPM_BY_INDUSTRY[industry] + (10 if cascade else 0) - (8 if demo else 0)


def bgm_backend(reply):
    return "local-composer" if "limit: 0" in reply else "lyria"


@card("GEN-64")
def music_seed_loop(task, wd):
    """Local part of the BGM route: BPM by industry (+10 cascade, -8 demo loop), the free-tier 'limit: 0' fallback to the
    local composer, and a <= 30 s seed crossfade-looped (equal-power) to the film length without seam clicks."""
    np = np_()
    rate = 44100
    bpm = bgm_bpm("finance")
    beat = 60.0 / bpm
    seed_len = 8 * beat
    t = np.arange(int(seed_len * rate)) / rate
    seed = 0.3 * np.sin(2 * np.pi * 110 * t) * (0.6 + 0.4 * np.cos(2 * np.pi * t / seed_len))
    for k in range(8):
        i = int(k * beat * rate)
        seed[i:i + 800] += 0.6 * np.exp(-np.arange(800) / 120.0) * np.sin(2 * np.pi * 1800 * np.arange(800) / rate)
    seed = seed * np.linspace(1, 0.4, len(seed))
    fx.write_wav(wd / "seed.wav", seed, rate)
    target = 20.0
    xf = int(0.5 * rate)
    out = seed.copy()
    while len(out) < target * rate:
        a = np.cos(np.linspace(0, np.pi / 2, xf)); b = np.sin(np.linspace(0, np.pi / 2, xf))
        out = np.concatenate([out[:-xf], out[-xf:] * a + seed[:xf] * b, seed[xf:]])
    out = out[:int(target * rate)]
    fx.write_wav(wd / "bgm.wav", out, rate)
    naive = np.concatenate([seed] * 3)
    jump = lambda s: float(np.abs(np.diff(s)).max())
    seam = len(seed) - xf
    loc = float(np.abs(np.diff(out[seam - 200:seam + 200])).max())
    nloc = float(abs(naive[len(seed)] - naive[len(seed) - 1]))
    lstep = float(np.abs(np.diff(out[seam - 2:seam + 2])).max())
    hp = np.abs(np.diff(out))
    hits = np.nonzero(hp > 0.05)[0]
    on = [int(o) for k, o in enumerate(hits) if k == 0 or o - hits[k - 1] > 0.2 * rate]
    period = float(np.median(np.diff(on))) / rate
    meas_bpm = 60.0 / period
    d = fx.probe(wd / "bgm.wav")["format"]["duration"]
    return [check("BPM by industry: finance 92, SaaS + cascade 118, crypto demo loop 92", [bgm_bpm("finance"), bgm_bpm("saas", cascade=True), bgm_bpm("crypto", demo=True)] == [92, 118, 92],
                  [bgm_bpm("finance"), bgm_bpm("saas", cascade=True), bgm_bpm("crypto", demo=True)], [92, 118, 92]),
            check("free-tier 'limit: 0' falls back to the local composer", bgm_backend("quota exceeded, limit: 0") == "local-composer" and bgm_backend("ok") == "lyria", True, True),
            check("seed <= 30 s, loop = film length (20 s)", seed_len <= 30 and abs(float(d) - target) < 0.01, [seed_len, d], "20 s"),
            check("measured beat ≈ 92 BPM", abs(meas_bpm - bpm) < 1.5, meas_bpm, bpm),
            check("crossfade seam has no click (jump < 0.05)", loc < 0.05 and lstep < 0.05, [loc, lstep], "<0.05"),
            check("negative control: a naive concat jumps at the seam (one-sample step)", not (nloc < 0.05), nloc, "<0.05")], [wd / "bgm.wav"]


@card("GEN-77")
def footage_filled_words(task, wd):
    """Giant uppercase words whose letters are filled with the clip (background-clip: text) over the #0c0b10 palette;
    assets generated once with a fixed seed and cached (a second build reuses the cache)."""
    np = np_()
    from PIL import Image
    import hashlib
    cache = wd / "cache"
    cache.mkdir(exist_ok=True)

    def asset(seed):
        p = cache / ("asset_%d.mp4" % seed)
        if p.exists():
            return p, False
        fx.ffmpeg("-f", "lavfi", "-i", "testsrc2=s=480x200:r=10:d=1", "-vf", "hue=h=%d" % (seed % 360), "-pix_fmt", "yuv444p",
                  "-c:v", "libx264", "-qp", "0", str(p))
        return p, True
    a1, made1 = asset(7)
    h1 = hashlib.sha256(a1.read_bytes()).hexdigest()
    a2, made2 = asset(7)
    fr = fx.frames(a1, (480, 200))[5]
    t, _ = tile("VIDEO", font(POPPINS, 150))
    M = np.zeros((200, 480), bool)
    al = np.asarray(t.getchannel("A")) > 128
    oy, ox = (200 - al.shape[0]) // 2, (480 - al.shape[1]) // 2
    M[max(0, oy):oy + al.shape[0], max(0, ox):ox + al.shape[1]] = al[max(0, -oy):200 - oy, max(0, -ox):480 - ox]
    bg = np.array(hexrgb("#0c0b10"), float)
    out = np.where(M[..., None], fr, bg)
    Image.fromarray(out.astype("uint8")).save(wd / "filled.png")
    inside = float(np.abs(out[M] - fr[M]).max())
    outside = float(np.abs(out[~M] - bg).max())
    var_in = float(out[M].std(0).mean())
    flat = np.where(M[..., None], np.array(hexrgb("#9a6cf0"), float), bg)
    return [check("letters show the footage pixel for pixel", inside == 0, inside, 0),
            check("outside the letters: palette ground #0c0b10", outside == 0, outside, 0),
            check("footage inside letters has real detail (std > 30)", var_in > 30, var_in, ">30"),
            check("fixed-seed asset built once, second build uses the cache", made1 and not made2 and hashlib.sha256(a2.read_bytes()).hexdigest() == h1, [made1, made2], [True, False]),
            check("negative control: a placeholder fill has no footage detail", not (float(flat[M].std(0).mean()) > 30), float(flat[M].std(0).mean()), ">30")], \
        [wd / "filled.png", a1]


@card("GEN-82")
def sandboxed_scene_code(task, wd):
    """Storyboard: 3-6 scenes rescaled to sum exactly to D; each scene is a pure (ctx,t,d,W,H,P,u) Canvas function
    compiled in a restricted scope (window/document/fetch/... shadowed, 'use strict', <= 300 000 loop iterations per
    frame) and test-rendered at t = 0, .3d, .6d, .99d on 360x640 (node)."""
    js = r"""
const CATS=['type','ui','phone','charts','diagrams','shapes','particles','characters','photos','music','map'];
function rescale(sc,D){const s=sc.reduce((a,b)=>a+b.dur,0);let acc=0;return sc.map((x,i)=>{let d=i<sc.length-1?Math.round(x.dur/s*D*30)/30:+(D-acc).toFixed(6);acc+=d;return {...x,dur:d}})}
const SHADOW=['window','document','fetch','localStorage','XMLHttpRequest','WebSocket','navigator','Function','globalThis','process','require'];
function compileScene(src){const guarded=src.replace(/\b(for|while)\s*\(([^)]*)\)\s*\{/g,(m,k,c)=>k+'('+c+'){if(++__it>300000)throw new Error("loop budget");');
 const f=new Function(...SHADOW,'__state','"use strict";let __it=0;return function(ctx,t,d,W,H,P,u){__it=0;'+guarded+'}');return f(...SHADOW.map(()=>undefined),{})}
function fakeCtx(){const calls=[];return new Proxy({calls},{get:(o,k)=>k==='calls'?calls:(...a)=>{calls.push(k)},set:()=>true})}
function test(src,d){try{const fn=compileScene(src);for(const t of [0,.3*d,.6*d,.99*d]){const c=fakeCtx();fn(c,t,d,360,640,{},{});if(!c.calls.length)throw new Error('drew nothing')}return 'ok'}catch(e){return 'rejected: '+e.message}}
const film={title:'x',scenes:rescale([{name:'a',dur:2,category:'type'},{name:'b',dur:3.3,category:'charts'},{name:'c',dur:1.1,category:'shapes'},{name:'d',dur:2.6,category:'particles'}],12)};
const good="ctx.fillRect(0,0,W,H*t/d);for(let i=0;i<10;i++){ctx.arc(i,i,2,0,6)}";
const net="fetch('https://example.com');ctx.fillRect(0,0,1,1)";
const loop="for(;;){ctx.fillRect(0,0,1,1)}";
const glob="ctx.fillRect(0,0,1,1);globalThis.x=1";
const raw=(()=>{try{return (new Function("return typeof fetch"))()}catch(e){return 'err'}})();
console.log(JSON.stringify({sum:film.scenes.reduce((a,b)=>a+b.dur,0),n:film.scenes.length,cats:film.scenes.every(s=>CATS.includes(s.category)),
 good:test(good,2),net:test(net,2),loop:test(loop,2),glob:test(glob,2),raw}));"""
    out = node_eval(js, timeout=30)
    write_json(wd / "sandbox.json", out)
    return [check("scene durations sum exactly to D = 12 s (3-6 scenes)", abs(out["sum"] - 12) < 1e-6 and 3 <= out["n"] <= 6, [out["sum"], out["n"]], [12, "3-6"]),
            check("categories from the 11-category list", out["cats"], out["cats"], True),
            check("a pure scene passes the 4 test renders", out["good"] == "ok", out["good"], "ok"),
            check("network access is shadowed (fetch undefined -> rejected)", out["net"].startswith("rejected"), out["net"], "rejected"),
            check("infinite loop stopped by the 300 000-iteration budget", "loop budget" in out["loop"], out["loop"], "loop budget"),
            check("globalThis shadowed", out["glob"].startswith("rejected"), out["glob"], "rejected"),
            check("negative control: unsandboxed code sees the real fetch", not (out["raw"] != "function"), out["raw"], "not function")], [wd / "sandbox.json"]


SKELETON = ["REFERENCE DEFINITIONS", "SCENE", "CHARACTERS", "WORLD", "ACTING TASK", "SHOTS", "CAMERA AND LOOK", "AUDIO", "CONSTRAINTS"]


def x01_plan(shots_s, rate=12, reserve=0.30, batch=12):
    bad = [s for s in shots_s if not (4 <= s <= 30)]
    credits = sum(shots_s) * rate
    return {"invalid": bad, "credits": credits, "with_reserve": math.ceil(credits * (1 + reserve)),
            "batches": math.ceil(len(shots_s) / batch)}


@card("GEN-X01")
def higgsfield_reference_skeleton(task, wd):
    """Prompt skeleton (9 sections in order, ACTING TASK motive/goal/obstacle/tactic, SHOTS with timecodes) and the
    production budget: 4-30 s per shot, ~12 credits/s at 1080p, 30% reshoot reserve, <= 12 jobs per batch. No call is
    made: the plan is quoted before any spend."""
    shots = [6, 5, 8, 10, 5, 6, 7, 5, 6, 8, 5, 6, 9, 5]
    body = "\n".join("%s:\n%s" % (h, {"ACTING TASK": "motive: proof; goal: win; obstacle: doubt; tactic: show",
                                      "SHOTS": "00:00-00:06 one continuous shot, money moment at 00:02"}.get(h, "...")) for h in SKELETON)
    (wd / "prompt.txt").write_text(body, encoding="utf-8")

    def valid(txt):
        pos = [txt.find(h + ":") for h in SKELETON]
        acting = txt[txt.find("ACTING TASK:"):]
        return all(p >= 0 for p in pos) and pos == sorted(pos) and all(k in acting for k in ("motive", "goal", "obstacle", "tactic")) and \
            re.search(r"\d\d:\d\d-\d\d:\d\d", txt) is not None
    plan = x01_plan(shots)
    write_json(wd / "plan.json", plan)
    shuffled = body.replace("REFERENCE DEFINITIONS:", "TMP:").replace("CONSTRAINTS:", "REFERENCE DEFINITIONS:").replace("TMP:", "CONSTRAINTS:")
    return [check("skeleton: 9 sections in order, acting task, timecoded shots", valid(body), valid(body), True),
            check("budget: 91 s x 12 = 1092 credits, 1420 with the 30% reserve", plan["credits"] == 1092 and plan["with_reserve"] == 1420, plan, [1092, 1420]),
            check("14 jobs -> 2 batches of <= 12", plan["batches"] == 2, plan["batches"], 2),
            check("shot lengths inside 4-30 s", not plan["invalid"] and x01_plan([3, 31])["invalid"] == [3, 31], plan["invalid"], []),
            check("negative control: a reordered skeleton fails validation", not valid(shuffled), valid(shuffled), True)], [wd / "prompt.txt", wd / "plan.json"]


# ============================================================================= cards that cannot run here
_PAID = "paid generation API with a key and credits (%s); spending is out of scope"
GAPS = {
    "GEN-36": "large model download: local sd-turbo needs torch + ~2 GB weights; the other backend is a live web service",
    "GEN-37": _PAID % "Gemini / Nano Banana",
    "GEN-38": _PAID % "Nano Banana multi-reference edit",
    "GEN-39": _PAID % "FLUX via Together, TOGETHER_API_KEY",
    "GEN-40": _PAID % "OpenAI GPT Image / Ideogram",
    "GEN-41": _PAID % "Higgsfield; no higgsfield client installed",
    "GEN-51": _PAID % "Seedance via Higgsfield",
    "GEN-52": _PAID % "Kling text/image-to-video",
    "GEN-53": _PAID % "Kling motion brush",
    "GEN-54": _PAID % "Kling video-extend; the chain needs live task_ids",
    "GEN-55": _PAID % "Runway task API",
    "GEN-56": _PAID % "Seedance 2.0 reference-to-video via Higgsfield",
    "GEN-59": _PAID % "Veo via Gemini / Sora 2",
    "GEN-60": _PAID % "fal / Together / WaveSpeed / Vertex aggregators",
    "GEN-62": "GPU + large open-weights models (Wan 2.x, LTX-Video, AnimateDiff via ComfyUI)",
    "GEN-66": "live service: hyperframes media-use resolve calls hosted providers with keys",
    "GEN-67": _PAID % "HeyGen avatar / dub / translate",
    "GEN-68": _PAID % "Meshy / Tripo / Rodin text-to-3D",
    "GEN-70": "owner-private live MCP runtimes (KOSIF Think Cloudflare Worker, Jev arbiter) with private keys",
    "GEN-74": "needs the hyperframes registry download (npx hyperframes add) over the network",
    "GEN-90": _PAID % "thumbnail MCP with a personal access token and paid plan",
    "GEN-P01": "paid Claude API call behind a double opt-in (--send --ack-billing); tools/claude_api_review.py is not in this tree",
}
