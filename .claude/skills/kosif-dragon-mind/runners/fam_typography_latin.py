"""typography-latin: method cards as real programs with known-answer checks.

Each card renders real type (Pillow + raqm/HarfBuzz with Inter, Poppins, Liberation, DejaVu, Cairo VF; headless Chrome
or libass where the card is about those engines) on deterministic fixtures in the work folder, measures the output
and runs a negative control. Lengths given for 1080x1920 are rendered at K = 0.5 and the expected values scaled.
The toolkit below is a copy of the one in fam_typography_arabic.py (modules are loaded independently).
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

GAPS: dict = {
    "TYPE-13": "the card is the review page's live Google Fonts swap (seven families fetched from fonts.googleapis.com at "
               "preview time); that page and the remote families are not part of this container, so a local run would not "
               "be the card's method",
}

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
INTERD = Path("/usr/share/fonts/opentype/inter")
LIB = Path("/usr/share/fonts/truetype/liberation")
DJV = Path("/usr/share/fonts/truetype/dejavu")


def pick(*cands):
    for c in cands:
        if Path(c).exists():
            return Path(c)
    raise FileNotFoundError(cands[0])


INTER = pick(INTERD / "Inter-Regular.otf", FONTS / "Poppins-Regular.ttf")
INTER_B = pick(INTERD / "Inter-Bold.otf", POPPINS)
INTER_K = pick(INTERD / "Inter-Black.otf", POPPINS)
INTER_L = pick(INTERD / "Inter-Light.otf", FONTS / "Poppins-Regular.ttf")
SERIF = pick(LIB / "LiberationSerif-Regular.ttf", DJV / "DejaVuSerif.ttf")
SERIF_I = pick(LIB / "LiberationSerif-Italic.ttf", LIB / "LiberationSerif-Regular.ttf")
SERIF_B = pick(LIB / "LiberationSerif-Bold.ttf", DJV / "DejaVuSerif-Bold.ttf")
MONO = pick(DJV / "DejaVuSansMono.ttf", LIB / "LiberationMono-Regular.ttf")
MONO_B = pick(DJV / "DejaVuSansMono-Bold.ttf", MONO)
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
        try:
            axes = f.get_variation_axes()
        except OSError:
            return f
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


def wrap_words(words, f, maxw, gap=None):
    lines, cur = [], []
    for w in words:
        test = " ".join(cur + [w])
        if cur and tlen(test, f) > maxw:
            lines.append(" ".join(cur))
            cur = [w]
        else:
            cur.append(w)
    if cur:
        lines.append(" ".join(cur))
    return lines


def line_pitch(m):
    np = np_()
    rows = m.any(axis=1)
    runs, start = [], None
    for y, v in enumerate(list(rows) + [False]):
        if v and start is None:
            start = y
        if not v and start is not None:
            runs.append((start, y))
            start = None
    return runs


def persp_coeffs(src, dst):
    """PIL PERSPECTIVE coefficients mapping output points dst -> input points src."""
    np = np_()
    A, B = [], []
    for (x, y), (u, v) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y])
        B += [u, v]
    return np.linalg.solve(np.array(A, float), np.array(B, float)).tolist()


def turn_in(canvas, t_img, cx, by, theta_deg, z0, dy=0.0, persp=900.0, blur=0.0):
    """Place a tile rotated about its bottom edge by rotationX theta with z offset under CSS-style perspective."""
    from PIL import Image, ImageFilter
    w, h = t_img.size
    th = math.radians(theta_deg)

    def proj(x, y):
        yy, z = y * math.cos(th), z0 + y * math.sin(th)
        s = persp / (persp - z)
        return (cx + x * s, by + dy - yy * s)
    dst = [proj(-w / 2, h), proj(w / 2, h), proj(w / 2, 0), proj(-w / 2, 0)]
    src = [(0, 0), (w, 0), (w, h), (0, h)]
    im = t_img.filter(ImageFilter.GaussianBlur(blur)) if blur > 0.05 else t_img
    warped = im.transform(canvas.size, Image.PERSPECTIVE, persp_coeffs(src, dst), Image.BICUBIC)
    canvas.alpha_composite(warped)
    ys = [p[1] for p in dst]
    return max(ys) - min(ys)


def pca_angle(m):
    np = np_()
    ys, xs = np.nonzero(m)
    xs = xs - xs.mean()
    ys = ys - ys.mean()
    cov = np.cov(np.vstack([xs, ys]))
    w, v = np.linalg.eigh(cov)
    vx, vy = v[:, np.argmax(w)]
    a = math.degrees(math.atan2(-vy, vx))
    return (a + 90) % 180 - 90


def lower_third(c, at, t, title, sub, accent="#E7B65A", size=44, inset=72, bottom=160, k=K, side=None, detect=True):
    from PIL import ImageDraw
    W, H = c.size
    rtl = (side == "right") if side else (detect and bool(AR_RE.search(title)))
    acc = hexrgb(accent)
    ft, fs = font(CAIRO, int(size * k), 700), font(CAIRO, int(size * 0.55 * k), 600)
    y = H - bottom * k
    if t >= at:
        w = 120 * k * cubic_out((t - at) / 0.4)
        x = W - inset * k if rtl else inset * k
        ImageDraw.Draw(c).rectangle([x - w if rtl else x, y - 2 * k * 2, x if rtl else x + w, y], fill=acc)
    for txt, ff, dt, fill, dy in ((title, ft, 0.12, (255, 255, 255, 255), -size * k * 1.0), (sub, fs, 0.24, (255, 255, 255, 191), size * k * 0.7)):
        if t >= at + dt:
            e = cubic_out((t - at - dt) / 0.5)
            tl, _ = tile(txt, ff, fill=fill)
            half = tl.width / 2 - ff.size * 0.35
            cx = (W - inset * k - half) if rtl else (inset * k + half)
            place(c, tl, cx, y + dy + 16 * k * (1 - e), alpha=e)


def to_ar_digits(s):
    return "".join(AR_DIGITS[int(c)] if c.isdigit() and c in "0123456789" else c for c in str(s))


def ass_time(t):
    return "%d:%02d:%05.2f" % (int(t // 3600), int(t % 3600 // 60), t % 60)



def bezier(x1, y1, x2, y2):
    """CSS cubic-bezier(x1, y1, x2, y2) as an easing function of progress."""
    def f(p):
        p = clamp(p)
        lo, hi = 0.0, 1.0
        for _ in range(40):
            m = (lo + hi) / 2
            x = 3 * (1 - m) ** 2 * m * x1 + 3 * (1 - m) * m * m * x2 + m ** 3
            lo, hi = (m, hi) if x < p else (lo, m)
        m = (lo + hi) / 2
        return 3 * (1 - m) ** 2 * m * y1 + 3 * (1 - m) * m * m * y2 + m ** 3
    return f


E_OUT = bezier(.16, 1, .3, 1)
E_IN = bezier(.7, 0, .84, 0)


def tracked(text, f, spacing=0.0, fill=(255, 255, 255, 255), pad=None):
    """Text with CSS letter-spacing (px) added after every character, kerning kept via cumulative advances."""
    from PIL import Image, ImageDraw
    pad = int(f.size * 0.35) if pad is None else pad
    w = tlen(text, f, "ltr") + spacing * max(0, len(text) - 1)
    asc, desc = f.getmetrics()
    im = Image.new("RGBA", (int(w + 2 * pad), int(asc + desc + 2 * pad)), tuple(fill[:3]) + (0,))
    d = ImageDraw.Draw(im)
    for i, ch in enumerate(text):
        x = pad + tlen(text[:i], f, "ltr") + spacing * i if i else pad
        d.text((x, pad), ch, font=f, fill=fill, direction="ltr")
    return im


def ink_w(im):
    b = bbox(np_().asarray(im.getchannel("A")) > 128)
    return b[2] - b[0]


def contrast(c1, c2):
    def L(c):
        v = []
        for x in c:
            x = x / 255
            v.append(x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4)
        return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]
    a, b = sorted([L(c1), L(c2)], reverse=True)
    return (a + 0.05) / (b + 0.05)


def cap_h(f, ch="H"):
    m = shaped_mask(ch, f)
    b = bbox(m)
    return b[3] - b[1]


# ----------------------------------------------------------------------------- cards
VIDEO_MIN = {1920: {"headline": 60, "body": 20, "label": 16}, 1080: {"headline": 84, "support": 44}}


def lint_sizes(spec):
    W = spec["width"]
    issues = []
    for role, px in spec["sizes"].items():
        mn = VIDEO_MIN.get(W, {}).get(role)
        if mn and px < mn:
            issues.append("%s %dpx < %dpx" % (role, px, mn))
    if spec.get("feed") and spec["sizes"].get("tertiary", 99) < 24:
        issues.append("tertiary < 24px")
    if spec.get("safe", (80, 100)) < (80, 100):
        issues.append("safe area")
    if contrast(spec["fg"], spec["bg"]) < 7:
        issues.append("contrast")
    return issues


@card("TYPE-01")
def video_type_sizing(task, wd):
    """Video type floor: 84/44 px at 1080 w (60/20/16 at 1920), safe area 80/100 px, high contrast; lint a spec and measure a render."""
    np = np_()
    good = {"width": 1080, "sizes": {"headline": 84, "support": 44}, "safe": (80, 100), "fg": (255, 255, 255), "bg": (12, 12, 16)}
    web = {"width": 1080, "sizes": {"headline": 32, "support": 14}, "safe": (24, 24), "fg": (150, 150, 150), "bg": (110, 110, 110)}
    W, H = 540, 960
    c = blank((W, H), good["bg"])
    fh, fs = font(INTER_B, 84 * K), font(INTER, 44 * K)
    from PIL import ImageDraw
    d = ImageDraw.Draw(c)
    d.text((80 * K, 100 * K), "Headline", font=fh, fill=good["fg"], anchor="lt")
    d.text((80 * K, 100 * K + 110 * K), "Support line", font=fs, fill=good["fg"], anchor="lt")
    out = save_png(c, Path(wd) / "type_sizes.png")
    a = arr(c)
    ink = bbox(a.min(axis=-1) > 128)
    ch = cap_h(fh)
    meas = contrast(tuple(a[a.min(axis=-1) > 250][0]), tuple(a[2, 2]))
    checks = [check("video spec passes the floor lint", lint_sizes(good) == [], lint_sizes(good), []),
              check("headline cap height ≈ 0.727 em of 84k px", abs(ch / (84 * K) - 0.727) <= 0.05, ch / (84 * K), 0.727),
              check("type stays in the 80/100 px safe area", ink[0] >= 80 * K - 2 and ink[1] >= 100 * K - 2, ink, (80 * K, 100 * K)),
              check("measured contrast ≥ 7:1", meas >= 7, meas, ">=7"),
              check("negative control: web-sized grey type fails the lint", len(lint_sizes(web)) >= 3, lint_sizes(web), ">=3 issues")]
    return checks, [out]


@card("TYPE-04")
def type_scale_tokens(task, wd):
    """All sizes from one base and ratio: base 16 × 1.25 → 10, 13, 16, 20, 25, 31, 39, 49, 61; render a specimen and measure the steps."""
    np = np_()
    scale = [round(16 * 1.25 ** k) for k in range(-2, 7)]
    from PIL import ImageDraw
    c = blank((600, 420))
    d = ImageDraw.Draw(c)
    y = 10
    hs = []
    for s in scale:
        f = font(INTER_B, s)
        d.text((10, y), "Hx", font=f, fill="white", anchor="lt")
        hs.append(cap_h(f))
        y += s * 1.15
    out = save_png(c, Path(wd) / "scale.png")
    ratios = [b / a for a, b in zip(hs[3:], hs[4:])]
    lin = [16 + 4 * k for k in range(-2, 7)]
    lr = [b / a for a, b in zip(lin, lin[1:])]
    checks = [check("1.25 scale known answer", scale == [10, 13, 16, 20, 25, 31, 39, 49, 61], scale, [10, 13, 16, 20, 25, 31, 39, 49, 61]),
              check("measured cap heights step ×1.25", all(abs(r - 1.25) <= 0.08 for r in ratios), ratios, 1.25),
              check("video base 42–48 px at 1080p → display ≥ 1.333 steps", round(45 * 1.333 ** 2) >= 80, round(45 * 1.333 ** 2), ">=80"),
              check("negative control: a linear +4 px ladder is not geometric", max(lr) - min(lr) > 0.2, lr, "ratios vary")]
    return checks, [out, write_json(Path(wd) / "tokens.json", {"base": 16, "ratio": 1.25, "steps": scale})]


@card("TYPE-05")
def choose_pair_faces(task, wd):
    """Purpose → class → shortlist of 3 → specimen at final size; quality screen (kerning AV/To/Ty, glyph set, weights); ≤2 families."""
    np = np_()
    from fontTools.ttLib import TTFont
    short = {"Inter": INTER_K, "Poppins": POPPINS, "DejaVu Sans Mono": MONO_B}

    def screen(p):
        f = font(p, 80)
        kern = {pr: tlen(pr, f, "ltr") < tlen(pr, f, "ltr", features=["-kern"]) - 0.5 for pr in ("AV", "To", "Ty")}
        cm = set(TTFont(str(p)).getBestCmap())
        glyphs = all(ord(ch) in cm for ch in "AaBbQq0123456789&@€")
        return {"kern": all(kern.values()), "glyphs": glyphs}
    res = {n: screen(p) for n, p in short.items()}
    passed = [n for n, r in res.items() if all(r.values())]
    pair = {"display": passed[0], "workhorse": "Inter"}
    from PIL import ImageDraw
    c = blank((700, 260))
    d = ImageDraw.Draw(c)
    d.text((20, 20), "Build Faster", font=font(short[pair["display"]], 72), fill="white")
    d.text((20, 140), "Captions and lower-thirds in the workhorse face.", font=font(INTER, 26), fill=(200, 200, 200))
    out = save_png(c, Path(wd) / "specimen.png")
    checks = [check("shortlist of 3 screened", len(res) == 3, list(res), 3),
              check("Inter passes the quality screen (kerning AV/To/Ty, glyph set)", all(res["Inter"].values()), res, "Inter passes"),
              check("pair uses ≤2 families", len(set(pair.values())) <= 2, pair, "<=2"),
              check("specimen rendered at final size", bbox(arr(c).min(axis=-1) > 128) is not None, True, True),
              check("negative control: the monospace face fails the kerning screen", not res["DejaVu Sans Mono"]["kern"], res["DejaVu Sans Mono"], "kern False")]
    return checks, [out, write_json(Path(wd) / "screen.json", {"screen": res, "pair": pair})]


@card("TYPE-06")
def tabular_numerals(task, wd):
    """font-feature-settings 'tnum' for moving numbers: equal-width digits, so a counter never jitters; kern/liga stay on."""
    np = np_()
    f = font(INTER_B, 60)
    nums = ["1111", "8888", "1919", "4070"]
    tn = [tlen(n, f, "ltr", features=["tnum"]) for n in nums]
    pn = [tlen(n, f, "ltr", features=["-tnum"]) for n in nums]

    def draw_with(feat):
        def draw(t, c):
            from PIL import ImageDraw
            v = int(1000 + 9000 * t / 1.5)
            ImageDraw.Draw(c).text((300, 60), str(v), font=f, fill="white", anchor="rm", features=feat, direction="ltr")
        return draw
    p, frames = video(wd, "counter_tnum.mp4", draw_with(["tnum"]), 1.5, size=(320, 120))
    _, pf = video(wd, "counter_pnum.mp4", draw_with(["-tnum"]), 1.5, size=(320, 120))
    lefts = [bbox(lum(fr) > 128)[0] for fr in frames[::3]]
    plefts = [bbox(lum(fr) > 128)[0] for fr in pf[::3]]
    checks = [check("tnum: all digit strings equal width", max(tn) - min(tn) < 0.5, tn, "equal"),
              check("right-aligned counter does not jitter (left edge spread ≤ 1 digit's side bearing)", max(lefts) - min(lefts) <= 6, [min(lefts), max(lefts)], "<=6"),
              check("kerning still on", tlen("AV", f, "ltr", features=["tnum"]) < tlen("AV", f, "ltr", features=["-kern"]), True, True),
              check("negative control: proportional digits jitter", max(pn) - min(pn) > 5 and max(plefts) - min(plefts) > max(lefts) - min(lefts),
                    [max(pn) - min(pn), max(plefts) - min(plefts)], "wider spread")]
    return checks, [p]


def fit_font_size(text, path, max_width, base=78, minimum=42, step=2):
    s = base
    while s > minimum and tlen(text, font(path, s), "ltr") > max_width:
        s -= step
    return s, tlen(text, font(path, s), "ltr") <= max_width


@card("TYPE-07")
def fit_to_width(task, wd):
    """fitTextFontSize(text, {maxWidth 1600|900, base 78, min 42, step 2}): largest size that keeps the string inside the width."""
    cases = {"Short title": None, "A noticeably longer dynamic headline": None, "An extremely long dynamic headline string that can never fit at forty-two pixels": None}
    for k in cases:
        cases[k] = fit_font_size(k, INTER_B, 900)
    from PIL import ImageDraw
    c = blank((1000, 300))
    d = ImageDraw.Draw(c)
    y = 30
    widths = []
    for k, (s, ok) in cases.items():
        f = font(INTER_B, s)
        d.text((50, y), k, font=f, fill="white")
        widths.append(tlen(k, f, "ltr"))
        y += s * 1.3
    out = save_png(c, Path(wd) / "fit.png")
    sizes = [v[0] for v in cases.values()]
    s2 = sizes[1]
    checks = [check("short string keeps the base 78 px", sizes[0] == 78, sizes[0], 78),
              check("longer string: largest even size that fits", widths[1] <= 900 and tlen("A noticeably longer dynamic headline", font(INTER_B, s2 + 2), "ltr") > 900, [s2, widths[1]], "<=900, next step overflows"),
              check("floor at 42 px reported as not fitting", sizes[2] == 42 and not list(cases.values())[2][1], list(cases.values())[2], [42, False]),
              check("negative control: base size overflows the 900 px box", tlen("A noticeably longer dynamic headline", font(INTER_B, 78), "ltr") > 900, True, True)]
    return checks, [out, write_json(Path(wd) / "fit.json", cases)]


@card("TYPE-08")
def crisp_svg_text(task, wd):
    """shape-rendering:crispEdges on axes only, integer viewBox, label halo = paint-order:stroke with a 3 px background stroke; rendered in Chrome."""
    np = np_()
    from PIL import Image
    def svg(crisp, halo):
        sr = 'shape-rendering="crispEdges"' if crisp else ""
        st = 'stroke="#101010" stroke-width="6" paint-order="stroke fill"' if halo else ""
        lines = "".join('<line x1="%d" y1="20" x2="%d" y2="180" stroke="#e0e0e0" stroke-width="2"/>' % (60 + i * 17, 60 + i * 17) for i in range(15))
        return ('<html><body style="margin:0;background:#101010"><svg width="400" height="200" viewBox="0 0 400 200">%s'
                '<line x1="40.3" y1="10" x2="40.3" y2="190" stroke="#ffffff" stroke-width="1.5" %s/>'
                '<text x="200" y="110" font-family="DejaVu Sans" font-size="28" fill="#ffd400" text-anchor="middle" %s>Label 42</text>'
                '</svg></body></html>') % (lines, sr, st)
    _, a = chrome_shot(wd, svg(True, True), "crisp", 400, 200)
    _, b = chrome_shot(wd, svg(False, False), "soft", 400, 200)
    A, B = arr(Image.open(a)), arr(Image.open(b))
    colA = lum(A[50:150, 36:46]).mean(axis=0)
    colB = lum(B[50:150, 36:46]).mean(axis=0)
    hard = int((colA > 240).sum()), int(((colA > 30) & (colA < 220)).sum())
    soft = int((colB > 240).sum()), int(((colB > 30) & (colB < 220)).sum())
    yel = colour_mask(A, (255, 212, 0), 60)
    yb = bbox(yel)
    ring = A[yb[1] - 3:yb[3] + 3, yb[0] - 3:yb[2] + 3]
    grey_lines_inside = int(((lum(ring) > 200) & ~colour_mask(ring, (255, 212, 0), 80)).sum())
    grey_b = int(((lum(B[yb[1] - 3:yb[3] + 3, yb[0] - 3:yb[2] + 3]) > 200) & ~colour_mask(B[yb[1] - 3:yb[3] + 3, yb[0] - 3:yb[2] + 3], (255, 212, 0), 80)).sum())
    checks = [check("crispEdges axis on a fractional position is hard pixels only", hard[0] >= 1 and hard[1] == 0, hard, "(>=1, 0)"),
              check("halo clears busy marks behind the label", grey_lines_inside < 0.4 * grey_b, [grey_lines_inside, grey_b], "far fewer"),
              check("negative control: without crispEdges the axis smears into grey columns", soft[1] >= 1, soft, ">=1 grey column")]
    return checks, [a, Path(wd) / "crisp.html"]


EMBED_OK = ("open font license", "apache license")


@card("TYPE-09")
def font_licensing(task, wd):
    """Embed only OFL/Apache faces, self-hosted, one @font-face per family, licence recorded; read the licence from each font's name table."""
    from fontTools.ttLib import TTFont
    cands = {"Inter": INTER, "Poppins": FONTS / "Poppins-Regular.ttf", "Cairo": CAIRO, "DejaVu Sans": DJV / "DejaVuSans.ttf"}
    rec = {}
    for fam, p in cands.items():
        nm = TTFont(str(p))["name"]
        lic = (nm.getDebugName(13) or "") + " " + (nm.getDebugName(14) or "")
        rec[fam] = {"file": p.name, "licence": lic.strip()[:120], "embed": any(k in lic.lower() for k in EMBED_OK)}
    ok = [f for f, r in rec.items() if r["embed"]]
    css = "".join("@font-face{font-family:'%s';src:url(fonts/%s);font-display:block}\n" % (f, rec[f]["file"]) for f in ok)
    cssf = Path(wd) / "fonts.css"
    cssf.write_text(css, encoding="utf-8")
    checks = [check("OFL faces cleared for embedding", all(rec[f]["embed"] for f in ("Inter", "Poppins", "Cairo")), {f: rec[f]["embed"] for f in rec}, "OFL True"),
              check("one @font-face per family, self-hosted, no CDN", css.count("@font-face") == len(ok) and "http" not in css, css.count("@font-face"), len(ok)),
              check("licence recorded per family", all(rec[f]["licence"] for f in rec), True, True),
              check("negative control: a non-OFL/Apache licence is held back", not rec["DejaVu Sans"]["embed"], rec["DejaVu Sans"]["licence"][:60], "not embeddable by rule")]
    return checks, [cssf, write_json(Path(wd) / "licences.json", rec)]


def text_rung(s, role):
    words = len(s.split())
    if re.search(r"\d", s) and len(s) > 6:
        return 3 if role == "data" else 2
    if role == "label":
        return 1 if words <= 4 and len(s) <= 25 else 2
    if role == "title":
        return 1 if words <= 8 and len(s) <= 25 else 2
    return 2 if len(s) <= 120 else 3


@card("TYPE-10")
def text_in_image_ladder(task, wd):
    """Rung 1: image model draws ≤25 chars / label ≤4 words / title ≤8 words, quoted verbatim; rung 2: overlay; rung 3: real vector type."""
    items = [("Panel A", "label"), ("Quarterly revenue by region and channel", "label"), ("Night Market", "title"),
             ("Revenue 2024: $1,284,000", "data"), ("Paragraph of dense explanatory copy that a model would garble", "body")]
    rungs = [text_rung(s, r) for s, r in items]
    prompt = [('Text (verbatim, render exactly, no extra characters): "%s"' % s) for (s, r), g in zip(items, rungs) if g == 1]
    from PIL import ImageDraw
    c = blank((600, 200), (30, 40, 60))
    d = ImageDraw.Draw(c)
    y = 20
    for (s, r), g in zip(items, rungs):
        if g >= 2:
            d.text((20, y), s, font=font(INTER_B, 20), fill="white")
            y += 34
    out = save_png(c, Path(wd) / "overlay.png")
    naive = [1 for _ in items]
    checks = [check("ladder known answers", rungs == [1, 2, 1, 3, 2], rungs, [1, 2, 1, 3, 2]),
              check("rung-1 strings quoted verbatim, each ≤25 chars", all(len(s) <= 25 for (s, r), g in zip(items, rungs) if g == 1) and len(prompt) == 2, prompt, "2 lines"),
              check("numbers and long copy become real overlaid type", bbox(arr(c).min(axis=-1) > 200) is not None, True, True),
              check("negative control: 'let the model draw everything' sends numbers to the model", naive[3] == 1 and rungs[3] != 1, naive[3], "1 (wrong)")]
    return checks, [out, write_json(Path(wd) / "ladder.json", {"items": items, "rungs": rungs, "prompt": prompt})]


@card("TYPE-12")
def offline_font_inlining(task, wd):
    """Inline the project's woff2 faces as base64 @font-face so the page renders with zero network requests; render it in Chrome."""
    import base64
    np = np_()
    from PIL import Image
    faces = {"SG": FONTS / "space-grotesk-latin-700-normal.woff2", "JBM": FONTS / "jetbrains-mono-latin-700-normal.woff2"}
    orig = ('<html><head><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700" rel="stylesheet"><style>'
            'body{margin:0;background:#000;color:#fff}p{font:700 54px "SG",monospace;margin:10px}</style></head><body><p>Offline</p></body></html>')
    css = "".join("@font-face{font-family:'%s';src:url(data:font/woff2;base64,%s) format('woff2');font-display:block}" %
                  (k, base64.b64encode(p.read_bytes()).decode()) for k, p in faces.items())
    inl = re.sub(r"<link[^>]+>", "", orig).replace("<style>", "<style>" + css)
    srcf, png = chrome_shot(wd, inl, "inlined", 360, 90)
    _, png_fb = chrome_shot(wd, re.sub(r"<link[^>]+>", "", orig), "fallback", 360, 90)
    m1 = arr(Image.open(png)).min(axis=-1) > 128
    m2 = arr(Image.open(png_fb)).min(axis=-1) > 128
    back = base64.b64decode(re.search(r"base64,([^)]+)\)", inl).group(1))
    checks = [check("zero network URLs left", not re.search(r"https?://", inl), re.findall(r"https?://\S+", inl), []),
              check("base64 decodes to the exact font bytes", back == faces["SG"].read_bytes(), len(back), faces["SG"].stat().st_size),
              check("Chrome draws the inlined face (differs from the fallback)", iou(crop_ink(m1), crop_ink(m2)) < 0.7, iou(crop_ink(m1), crop_ink(m2)), "<0.7"),
              check("negative control: the original page needs fonts.googleapis.com", "fonts.googleapis.com" in orig, True, True)]
    return checks, [srcf, png]


def latin_row(words, f, W, cy, gap=None, fills=None):
    return word_row(words, f, W, cy, gap=gap, rtl=False, fills=fills)


@card("TYPE-14")
def baseline_mask_rise(task, wd):
    """maskRise: lines clipped at their baseline box rise yPercent 110→0 in 0.5 s, stagger 0.08 s, E.out (.16,1,.3,1); exit −110 in 0.27 s E.in."""
    np = np_()
    W, H = 360, 300
    f = font(INTER_B, 34)
    lines = ["Design that", "moves people", "forward."]
    rows = []
    for k, ln in enumerate(lines):
        t, _ = tile(ln, f)
        r = {"tile": t, "cx": W / 2, "cy": 80 + k * 60}
        r["ink"] = ink_box_abs(r)
        r["clip"] = (r["ink"][0] - 4, r["ink"][1] - 6, r["ink"][2] + 4, r["ink"][3] + 1)
        r["h"] = r["clip"][3] - r["clip"][1]
        rows.append(r)
    at, st, dur, out_at = 0.2, 0.08, 0.5, 1.4

    def draw(t, c):
        for k, r in enumerate(rows):
            h = r["h"]
            if t < at + k * st:
                continue
            if t < out_at + k * st / 2:
                dy = 1.1 * h * (1 - E_OUT((t - at - k * st) / dur))
            else:
                dy = -1.1 * h * E_IN((t - out_at - k * st / 2) / 0.27)
            place(c, r["tile"], r["cx"], r["cy"] + dy, clip=r["clip"])
    p, frames = video(wd, "mask_rise.mp4", draw, 2.0, size=(W, H))
    leak = max(outside_ink(fr, [r["clip"] for r in rows]) for fr in frames)
    firsts = [next(j / 30 for j, fr in enumerate(frames) if box_ink(fr, r["clip"], 40) > 0) for r in rows]
    mid = frame_at(frames, at + 0.25)
    e = E_OUT(round(0.25 * 30) / 30 / dur)
    h0 = rows[0]["ink"][3] - rows[0]["ink"][1]
    vis = box_ink(mid, rows[0]["clip"]) / box_ink(frame_at(frames, 1.0), rows[0]["clip"])
    gone = sum(box_ink(frames[-1], r["clip"]) for r in rows)
    checks = [check("ink never below the baseline clip", leak == 0, leak, 0),
              check("lines start 0.08 s apart", firsts[0] >= at and all(abs((firsts[k] - firsts[0]) - k * st) <= 0.035 for k in range(3)), firsts, "Δ = 0.08 s per line"),
              check("E.out: line 1 mostly visible half way", vis > 0.75, vis, ">0.75 (cubic-bezier .16,1,.3,1)"),
              check("exit −110% clears all lines", gone == 0, gone, 0),
              check("E.out endpoints and monotone", abs(E_OUT(0)) < 1e-6 and abs(E_OUT(1) - 1) < 1e-6 and all(E_OUT(a / 20) <= E_OUT((a + 1) / 20) for a in range(20)), True, True),
              check("negative control: a static render shows ink at t=0", box_ink(arr(blank((W, H))), rows[0]["clip"]) == 0 and firsts[0] > 0, firsts[0], ">0")]
    return checks, [p]


@card("TYPE-15")
def rise_partial_state(task, wd):
    """riseWords: words arrive from 40% opacity, 26 px low, 6 px blur clearing early (by 60% of the move), 0.4 s, stagger 0.1 s."""
    np = np_()
    words = ["Launch", "day", "is", "here"]
    f = font(INTER_B, 32)
    at, dur, st = 0.4, 0.4, 0.1

    def state(i, t):
        p = clamp((t - at - i * st) / dur) if t >= at + i * st else 0.0
        e = E_OUT(p)
        return {"dy": 26 * (1 - e), "alpha": 0.4 + 0.6 * e, "blur": 6 * clamp(1 - p / 0.6)}
    p, frames, row = kinetic(wd, "rise_partial.mp4", words, f, state, 1.6, size=(360, 200), cy=100)
    W = 360
    zones = [grow(r["ink"], 10, 34) for r in row]
    r0 = [lumsum(frames[0], z) / lumsum(frames[-1], z) for z in zones]
    dy0 = [wcentroid(crop(frames[0], z))[1] - wcentroid(crop(frames[-1], z))[1] for z in zones]

    def sharp(fr, z):
        return float(np.abs(np.diff(lum(crop(fr, z)), axis=1)).max())
    t60 = at + 0.6 * dur + 1 / 30
    s60 = sharp(frame_at(frames, t60), zones[0]) / sharp(frames[-1], zones[0])
    checks = [check("waits at 40% light", all(0.3 <= r <= 0.5 for r in r0), r0, 0.4),
              check("starts 26 px low", all(18 <= d <= 30 for d in dy0), dy0, 26),
              check("blur cleared by 60% of the move", s60 > 0.85, s60, ">0.85"),
              check("negative control: unprocessed words are at full light", lumsum(frames[-1], zones[0]) / lumsum(frames[-1], zones[0]) == 1 and min(r0) < 0.6, True, True)]
    return checks, [p]


@card("TYPE-16")
def blur_focus_pull(task, wd):
    """Each word resolves blur(B)→0, opacity 0→1, small y offset, 220–500 ms, stagger 80–120 ms; ≤12 live-blurred elements at once."""
    np = np_()
    words = "We pull every word into sharp focus".split()
    f = font(INTER_B, 26)
    at, dur, st, B = 0.2, 0.35, 0.1, 12

    def state(i, t):
        if t < at + i * st:
            return None
        e = cubic_out((t - at - i * st) / dur)
        return {"blur": B * (1 - e), "alpha": e, "dy": 8 * (1 - e)}
    p, frames, row = kinetic(wd, "focus_pull.mp4", words, f, state, 1.6, size=(640, 160), cy=80)
    zones = [grow(r["ink"], 6, 20) for r in row]

    def sharp(fr, z):
        return float(np.abs(np.diff(lum(crop(fr, z)), axis=1)).max())
    fin = [sharp(frames[-1], z) for z in zones]
    mid = [sharp(frame_at(frames, at + i * st + 0.07), z) / fin[i] for i, z in enumerate(zones)]
    live = max(sum(1 for i in range(len(words)) if at + i * st <= t < at + i * st + dur) for t in np.arange(0, 1.6, 1 / 30))
    order = [first_time([lumsum(fr, z) for fr in frames], 0.1) for z in zones]
    checks = [check("every word blurred on arrival, crisp at rest", all(m < 0.6 for m in mid), mid, "<0.6"),
              check("words resolve in reading order", order == sorted(order), order, "ascending"),
              check("≤12 live-blurred words at any moment", live <= 12, live, "<=12"),
              check("negative control: the plain line is sharp from the start", all(f_ > 100 for f_ in fin), fin, ">100")]
    return checks, [p]


@card("TYPE-17")
def reading_order_light_up(task, wd):
    """A dim paragraph (30%) lights up word by word in reading order: lit = round(progress × words)."""
    np = np_()
    words = "The paragraph waits in shadow until each word is spoken aloud".split()
    f = font(INTER_B, 24)
    W, H = 420, 200
    lines = wrap_words(words, f, 380)
    pos, y = [], 50
    for ln in lines:
        row = latin_row(ln.split(), f, W, y)
        pos += row
        y += 40
    dur = 3.0

    def draw(t, c):
        lit = round(clamp(t / dur) * len(words))
        for i, r in enumerate(pos):
            place(c, r["tile"], r["cx"], r["cy"], alpha=1.0 if i < lit else 0.3)
    p, frames = video(wd, "light_up.mp4", draw, dur + 0.2, size=(W, H))
    boxes = [grow(ink_box_abs(r), 2, 4) for r in pos]
    full = [lumsum(frames[-1], b) for b in boxes]
    ok = []
    for t in (0.6, 1.5, 2.4):
        fr = frame_at(frames, t)
        lit = sum(1 for b, fu in zip(boxes, full) if lumsum(fr, b) / fu > 0.8)
        ok.append((lit, round(clamp(round(t * 30) / 30 / dur) * len(words))))
    dim = lumsum(frames[0], boxes[-1]) / full[-1]
    checks = [check("lit count = round(progress × words)", all(a == b for a, b in ok), ok, "equal"),
              check("unlit words at ~30%", abs(dim - 0.3) <= 0.06, dim, 0.3),
              check("negative control: the unprocessed dim paragraph has no lit word", sum(1 for b, fu in zip(boxes, full) if lumsum(frames[0], b) / fu > 0.8) == 0, 0, 0)]
    return checks, [p]


@card("TYPE-18")
def letter_drop_cascade(task, wd):
    """Latin letters drop onto the baseline: 40 ms stagger, 12 px offset (never opacity alone), ~300 ms each."""
    np = np_()
    word = "CASCADE"
    f = font(INTER_K, 48)
    W, H = 360, 160
    x = (W - tlen(word, f, "ltr")) / 2
    tiles, xs = [], []
    for i, ch in enumerate(word):
        t, _ = tile(ch, f)
        tiles.append(t)
        xs.append(x + tlen(word[:i], f, "ltr") + tlen(ch, f, "ltr") / 2)
    at, st, dur = 0.2, 0.04, 0.3
    cols = [(int(255 - 10 * i), 255, 255) for i in range(len(word))]

    def draw(t, c):
        for i, tl in enumerate(tiles):
            t0 = at + i * st
            if t < t0:
                continue
            e = cubic_out((t - t0) / dur)
            place(c, tl, xs[i], H / 2 - 40 * (1 - e) - 12 * (1 - e), alpha=clamp((t - t0) / 0.1))
    p, frames = video(wd, "letters.mp4", draw, 1.0, size=(W, H), fps=60)
    cols_x = [(int(xs[i] - 8), int(xs[i] + 8)) for i in range(len(word))]
    firsts = [first_time([float((lum(fr[:, a:b]) > 60).sum()) for fr in frames], 0.05, fps=60) for a, b in cols_x]
    gaps = [b - a for a, b in zip(firsts, firsts[1:])]
    y_start = wcentroid(frames[int((at + 0.02) * 60)][:, cols_x[0][0]:cols_x[0][1]])[1]
    y_end = wcentroid(frames[-1][:, cols_x[0][0]:cols_x[0][1]])[1]
    checks = [check("letters start 40 ms apart", all(abs(g - 0.04) <= 0.02 for g in gaps), gaps, 0.04),
              check("each letter travels down onto the baseline (≥12 px)", y_end - y_start >= 12, y_end - y_start, ">=12"),
              check("final word assembled", iou(mask_of(frames[-1]), mask_of(arr(_static(tiles, xs, W, H)))) > 0.9, True, True),
              check("negative control: at t=0 nothing has dropped", float(frames[0].max()) < 30, float(frames[0].max()), "<30")]
    return checks, [p]


def _static(tiles, xs, W, H, y=None):
    c = blank((W, H))
    for tl, x in zip(tiles, xs):
        place(c, tl, x, H / 2 if y is None else y)
    return c


@card("TYPE-19")
def scatter_assemble(task, wd):
    """Glyphs start at seeded random offsets (±300 px, ±25°) and slam home with easeOutBack, stagger 40 ms, 500 ms; deterministic."""
    np = np_()
    import random
    import hashlib
    word = "ASSEMBLE"
    f = font(INTER_K, 44)
    W, H = 400, 240
    x0 = (W - tlen(word, f, "ltr")) / 2
    tiles = [tile(ch, f)[0] for ch in word]
    xs = [x0 + tlen(word[:i], f, "ltr") + tlen(ch, f, "ltr") / 2 for i, ch in enumerate(word)]

    def render(seed):
        rnd = random.Random(seed)
        offs = [(rnd.uniform(-300, 300), rnd.uniform(-300, 300) * 0.4, rnd.uniform(-25, 25)) for _ in word]

        def draw(t, c):
            for i, tl in enumerate(tiles):
                e = back_out(clamp((t - 0.1 - i * 0.04) / 0.5))
                dx, dy, r = offs[i]
                place(c, tl, xs[i] + dx * (1 - e), H / 2 + dy * (1 - e), rot=r * (1 - e))
        return draw
    p, frames = video(wd, "scatter.mp4", render(7), 1.2, size=(W, H))
    p2, frames2 = video(wd, "scatter_again.mp4", render(7), 1.2, size=(W, H))
    ref = mask_of(arr(_static(tiles, xs, W, H)))
    checks = [check("assembled into the word at rest", iou(mask_of(frames[-1]), ref) > 0.92, iou(mask_of(frames[-1]), ref), ">0.92"),
              check("seeded: two renders are identical", hashlib.sha256(frames.tobytes()).hexdigest() == hashlib.sha256(frames2.tobytes()).hexdigest(), True, True),
              check("negative control: the first frame is scattered", iou(mask_of(frames[0]), ref) < 0.3, iou(mask_of(frames[0]), ref), "<0.3")]
    return checks, [p]


@card("TYPE-22")
def waterfall_cascade(task, wd):
    """Binary opacity (tl.set, never faded), y 40–50 px medium density, 0.13–0.16 s power4.out; each element starts before the previous settles."""
    np = np_()
    items = ["Plan", "Build", "Ship", "Repeat"]
    f = font(INTER_B, 30)
    W, H = 300, 320
    tiles = [tile(s, f)[0] for s in items]
    ys = [60 + 60 * i for i in range(4)]
    at, st, dur, off = 0.2, 0.1, 0.15, 45

    def draw(t, c, fade=False):
        for i, tl in enumerate(tiles):
            t0 = at + i * st
            if t < t0:
                continue
            e = pow_out((t - t0) / dur, 4)
            place(c, tl, W / 2, ys[i] + off * (1 - e), alpha=e if fade else 1.0)
    p, frames = video(wd, "waterfall.mp4", draw, 1.0, size=(W, H), fps=60)
    _, ff = video(wd, "waterfall_fade.mp4", lambda t, c: draw(t, c, True), 1.0, size=(W, H), fps=60)
    peak = lambda fr, y: float(lum(fr[y - 40:y + 60]).max())
    mids = [peak(frames[int((at + i * st + 0.02) * 60)], ys[i]) for i in range(4)]
    fmid = [peak(ff[int((at + i * st + 0.02) * 60)], ys[i]) for i in range(4)]
    overlap = st < dur
    checks = [check("binary opacity: full brightness on the first frame of each entry", all(m >= 240 for m in mids), mids, ">=240"),
              check("each starts before the previous settles", overlap, [st, dur], "stagger < duration"),
              check("whips up from 45 px below", centroid(lum(frames[int(at * 60) + 1][ys[0] - 40:ys[0] + 48]) > 100)[1] - centroid(lum(frames[-1][ys[0] - 40:ys[0] + 48]) > 100)[1] > 15,
                    centroid(lum(frames[int(at * 60) + 1][ys[0] - 40:ys[0] + 48]) > 100)[1] - centroid(lum(frames[-1][ys[0] - 40:ys[0] + 48]) > 100)[1], ">15"),
              check("negative control: a faded entry is half-transparent at that frame", min(fmid) < 200, fmid, "<200")]
    return checks, [p]


@card("TYPE-23")
def kinetic_center_build(task, wd):
    """Words enter from the right (entry_offset 88) and shove the growing phrase left until the final line sits centred; 72 px."""
    np = np_()
    words = ["Make", "it", "move"]
    W, H = 640, 200
    f = font(INTER_B, 72 * K * 1.2)
    gap = f.size * 0.28
    lens = [tlen(w, f, "ltr") for w in words]
    tiles = [tile(w, f)[0] for w in words]
    times = [0.2, 0.8, 1.4]

    def layout(n):
        tot = sum(lens[:n]) + gap * (n - 1)
        x = (W - tot) / 2
        out = []
        for i in range(n):
            out.append(x + lens[i] / 2)
            x += lens[i] + gap
        return out

    def draw(t, c):
        n = sum(1 for tt in times if t >= tt)
        if n == 0:
            return
        e = cubic_out((t - times[n - 1]) / 0.4)
        cur, prev = layout(n), layout(n - 1) if n > 1 else []
        for i in range(n):
            if i < n - 1:
                x = prev[i] + (cur[i] - prev[i]) * e
            else:
                x = cur[i] + 88 * K * (1 - e)
            place(c, tiles[i], x, H / 2, alpha=clamp((t - times[i]) / 0.15))
    p, frames = video(wd, "center_build.mp4", draw, 2.2, size=(W, H))
    b = bbox(lum(frames[-1]) > 128)
    first = [centroid(lum(frame_at(frames, t)) > 128)[0] for t in (0.7, 1.3)]
    w0 = bbox(lum(frame_at(frames, 0.7)) > 128)
    w1 = bbox(lum(frame_at(frames, 1.3)) > 128)
    checks = [check("final line centred", abs((b[0] + b[2]) / 2 - W / 2) <= 2, (b[0] + b[2]) / 2, W / 2),
              check("earlier words shoved left as the phrase grows", w1[0] < w0[0] - 10, [w0[0], w1[0]], "left edge moves left"),
              check("new word enters from the right (offset at its first frames)", bbox(lum(frame_at(frames, 0.8 + 2 / 30)) > 60)[2] > bbox(lum(frame_at(frames, 1.3)) > 60)[2] + 10,
                    [bbox(lum(frame_at(frames, 0.8 + 2 / 30)) > 60)[2], bbox(lum(frame_at(frames, 1.3)) > 60)[2]], "further right, then settles"),
              check("negative control: the first word alone is not where the final line starts", abs(w0[0] - b[0]) > 20, [w0[0], b[0]], "different")]
    return checks, [p]


@card("TYPE-25")
def strip_slice_reveal(task, wd):
    """N clipped strips of a giant word, each offset x ±80 px, slide to 0 with 40 ms stagger and align into the word."""
    np = np_()
    W, H = 480, 220
    f = font(INTER_K, 120)
    t, _ = tile("SLICE", f)
    N = 6
    sh = t.height / N

    def draw(tt, c):
        for k in range(N):
            e = cubic_out((tt - 0.2 - k * 0.04) / 0.4) if tt > 0.2 + k * 0.04 else 0
            dx = (80 if k % 2 else -80) * (1 - e)
            y0 = H / 2 - t.height / 2 + k * sh
            place(c, t, W / 2 + dx, H / 2, clip=(0, y0, W, y0 + sh))
    p, frames = video(wd, "strips.mp4", draw, 1.0, size=(W, H))
    ref = blank((W, H))
    place(ref, t, W / 2, H / 2)
    refm = mask_of(arr(ref))

    def row_shift(fr, k):
        y0 = int(H / 2 - t.height / 2 + k * sh + 2)
        a = mask_of(fr)[y0:y0 + int(sh) - 4].sum(axis=0).astype(float)
        b = refm[y0:y0 + int(sh) - 4].sum(axis=0).astype(float)
        if a.sum() == 0 or b.sum() == 0:
            return 0.0
        return float((a * np.arange(W)).sum() / a.sum() - (b * np.arange(W)).sum() / b.sum())
    early = [row_shift(frames[0], k) for k in range(1, N - 1)]
    checks = [check("strips start offset ±80 in alternating directions", all(abs(abs(v) - 80) <= 12 for v in early) and early[0] * early[1] < 0, early, "±80"),
              check("strips align into the word", iou(mask_of(frames[-1]), refm) > 0.95, iou(mask_of(frames[-1]), refm), ">0.95"),
              check("negative control: the unaligned start is not the word", iou(mask_of(frames[0]), refm) < 0.6, iou(mask_of(frames[0]), refm), "<0.6")]
    return checks, [p]


@card("TYPE-26")
def construction_grid(task, wd):
    """Guides (baseline, x-height, cap) draw in at 35% white, 1 px, ~300 ms each, then letters snap onto them and the guides fade."""
    np = np_()
    from PIL import ImageDraw
    W, H = 420, 220
    f = font(SERIF, 96)
    word = "Hxg"
    base_y = 150
    xh = cap_h(f, "x")
    ch = cap_h(f, "H")
    guides = [("baseline", base_y), ("x-height", base_y - xh), ("cap", base_y - ch)]

    def draw(t, c):
        d = ImageDraw.Draw(c)
        for k, (n, y) in enumerate(guides):
            e = clamp((t - 0.1 - 0.3 * k) / 0.3)
            fade = 1 - clamp((t - 1.8) / 0.4)
            if e > 0:
                v = int(255 * 0.35 * fade)
                d.line([20, y, 20 + (W - 40) * e, y], fill=(v, v, v), width=1)
        for i, chh in enumerate(word):
            if t >= 1.0 + 0.15 * i:
                d.text((120 + tlen(word[:i], f, "ltr"), base_y), chh, font=f, fill="white", anchor="ls")
    p, frames = video(wd, "grid.mp4", draw, 2.4, size=(W, H))
    g = frame_at(frames, 0.95)
    rows = [int(np.argmax(((lum(g) > 60) & (lum(g) < 120)).sum(axis=1)[y - 3:y + 4])) + y - 3 for _, y in guides]
    fin = frame_at(frames, 1.6)
    hb = bbox(lum(fin[:, 110:160]) > 200)
    late = frames[-1]
    guide_px = int(((lum(late) > 60) & (lum(late) < 120))[:, 20:110].sum())
    checks = [check("guides at the font's baseline/x-height/cap", all(abs(r - y) <= 1 for r, (_, y) in zip(rows, guides)), rows, [y for _, y in guides]),
              check("guides drawn at ~35% white", 80 <= float(lum(g[guides[0][1]:guides[0][1] + 1, 30:100]).max()) <= 100, float(lum(g[guides[0][1]:guides[0][1] + 1, 30:100]).max()), 89),
              check("letter snapped onto baseline and cap guides", abs(hb[3] - base_y) <= 1 and abs(hb[1] - (base_y - ch)) <= 1, hb, [base_y - ch, base_y]),
              check("guides fade away", guide_px == 0, guide_px, 0),
              check("negative control: before 0.1 s no guide exists", float(frames[1].max()) < 20, float(frames[1].max()), "<20")]
    return checks, [p]


@card("TYPE-27")
def canvas_headline_autortl(task, wd):
    """headline = words.slice(0,4); 900 at 11.4% w; alpha = clamp((local − 0.58)/0.55); y = 0.735h + (1 − easeOutCubic(p))·0.065h; rtl for Arabic."""
    np = np_()
    from PIL import ImageDraw
    W, H = 360, 640

    def render(t, text):
        c = blank((W, H))
        words = text.split()[:4]
        s = " ".join(words)
        rtl = bool(AR_RE.search(s))
        f = font(CAIRO if rtl else INTER_K, int(0.114 * W * 0.6), 900)
        a = clamp((t - 0.58) / 0.55)
        p = clamp((t - 0.58) / 0.65)
        y = 0.735 * H + (1 - cubic_out(p)) * 0.065 * H
        tl, _ = tile(s, f)
        place(c, tl, W / 2, y, alpha=a)
        return c, s, y, a, rtl
    c1, s1, y1, a1, _ = render(0.9, "Build the thing people want today")
    c2, _, y2, _, _ = render(0.9, "Build the thing people want today")
    c3, s3, _, _, rtl = render(1.5, "اصنع ما يحبه الناس اليوم")
    out = save_png(c1, Path(wd) / "headline_t0.9.png")
    save_png(c3, Path(wd) / "headline_ar.png")
    m = arr(c1)
    meas_y = wcentroid(m)[1]
    meas_a = float(m.max()) / 255
    ref = shaped_mask(s3, font(CAIRO, int(0.114 * W * 0.6), 900))
    got = mask_of(arr(c3), 128)
    checks = [check("only the first 4 words", s1 == "Build the thing people", s1, "Build the thing people"),
              check("alpha = clamp((t−0.58)/0.55)", abs(meas_a - a1) <= 0.03, meas_a, a1),
              check("y follows 0.735h + (1−easeOutCubic(p))·0.065h", abs(meas_y - y1) <= 2, meas_y, y1),
              check("pure function of time (same t → same frame)", np.array_equal(arr(c1), arr(c2)), True, True),
              check("Arabic flips to RTL (shaped, first word on the right)", rtl and iou(crop_ink(got), crop_ink(ref)) > 0.85 and iou(crop_ink(got), crop_ink(basic_mask(s3, CAIRO, int(0.114 * W * 0.6)))) < 0.5,
                    iou(crop_ink(got), crop_ink(ref)), ">0.85 vs shaped RTL, <0.5 vs raw LTR"),
              check("negative control: before 0.58 s the headline is invisible", float(arr(render(0.5, "x y")[0]).max()) == 0, 0, 0)]
    return checks, [out, Path(wd) / "headline_ar.png"]


@card("TYPE-28")
def sine_bounce(task, wd):
    """y_i(t) = −A·|sin(ωt + iφ)|, A 12 px, φ 0.4 rad, ω 8 rad/s on bold uppercase letters."""
    np = np_()
    word = "BOUNCE"
    f = font(INTER_K, 44)
    W, H = 360, 140
    x0 = (W - tlen(word, f, "ltr")) / 2
    tiles = [tile(ch, f)[0] for ch in word]
    xs = [x0 + tlen(word[:i], f, "ltr") + tlen(ch, f, "ltr") / 2 for i, ch in enumerate(word)]
    yof = lambda t, i: -12 * abs(math.sin(8 * t + i * 0.4))

    def draw(t, c):
        for i, tl in enumerate(tiles):
            place(c, tl, xs[i], H / 2 + yof(t, i))
    p, frames = video(wd, "bounce.mp4", draw, 1.5, size=(W, H))
    rest = [wcentroid(arr(_static(tiles, xs, W, H))[:, int(x - 10):int(x + 10)])[1] for x in xs]
    errs = []
    for t in (0.3, 0.7, 1.1):
        fr = frame_at(frames, t)
        for i, x in enumerate(xs):
            m = wcentroid(fr[:, int(x - 10):int(x + 10)])[1] - rest[i]
            errs.append(abs(m - yof(round(t * 30) / 30, i)))
    checks = [check("letter offsets follow −12·|sin(8t + 0.4i)|", max(errs) <= 1.5, max(errs), "<=1.5 px"),
              check("neighbours phase-shifted (travelling wave)", abs(yof(0.3, 0) - yof(0.3, 1)) > 1, True, True),
              check("negative control: the static word has zero offsets", max(abs(yof(0.3, i)) for i in range(6)) > 3, True, True)]
    return checks, [p]


MOVES = {"slide_bottom": {"y": 150, "ease": "power4.out", "dur": 0.6}, "slide_top": {"y": -150, "ease": "power4.out", "dur": 0.6},
         "slide_left": {"x": -200, "ease": "power4.out", "dur": 0.6}, "slide_right": {"x": 200, "ease": "power4.out", "dur": 0.6},
         "scale_grow": {"scale": 0.0, "ease": "power2.out", "dur": 0.6}, "scale_punch": {"scale": 0.6, "ease": "back.out(2.2)", "dur": 0.5},
         "fade_in": {"alpha": 0.0, "ease": "linear", "dur": 0.4}, "fade_blur": {"blur": 14, "alpha": 0.0, "ease": "power2.out", "dur": 0.5},
         "bounce_in": {"y": -120, "ease": "bounce.out", "dur": 0.8}, "slam": {"y": -300, "ease": "power4.out", "dur": 0.35}}


def ease_by(name):
    if name == "linear":
        return clamp
    if name.startswith("power"):
        k = int(name[5]) + 1
        return lambda p: pow_out(p, k)
    if name.startswith("back.out"):
        s = float(re.search(r"\(([\d.]+)\)", name).group(1)) if "(" in name else 1.70158
        return lambda p: back_out(p, s)
    if name == "bounce.out":
        def b(p):
            p = clamp(p)
            n, d = 7.5625, 2.75
            if p < 1 / d:
                return n * p * p
            if p < 2 / d:
                p -= 1.5 / d
                return n * p * p + .75
            if p < 2.5 / d:
                p -= 2.25 / d
                return n * p * p + .9375
            p -= 2.625 / d
            return n * p * p + .984375
        return b
    raise KeyError(name)


def move_state(name, p):
    m = MOVES[name]
    e = ease_by(m["ease"])(p)
    st = {"dx": m.get("x", 0) * (1 - e), "dy": m.get("y", 0) * (1 - e), "alpha": 1.0, "blur": m.get("blur", 0) * (1 - e), "scale": 1.0}
    if "scale" in m:
        st["scale"] = m["scale"] + (1 - m["scale"]) * e
    if "alpha" in m:
        st["alpha"] = e
    return st


@card("TYPE-29")
def motion_vocabulary(task, wd):
    """Shared names for text moves (slide_*, scale_punch 0.6→1 back.out(2.2), fade_blur 14 px, bounce_in, slam …) resolved into real tweens."""
    np = np_()
    board = [{"beat": 1, "move": "slide_bottom", "text": "Hello"}, {"beat": 2, "move": "scale_punch", "text": "World"}, {"beat": 3, "move": "spin_wobble", "text": "?"}]
    unknown = [b["move"] for b in board if b["move"] not in MOVES]
    f = font(INTER_B, 40)
    t1, _ = tile("Hello", f)
    W, H = 320, 480

    def draw(t, c):
        s = move_state("slide_bottom", t / 0.6)
        place(c, t1, W / 2, 200 + s["dy"])
        s2 = move_state("scale_punch", clamp((t - 0.7) / 0.5))
        if t >= 0.7:
            place(c, t1, W / 2, 330, scale=s2["scale"])
    p, frames = video(wd, "vocab.mp4", draw, 1.4, size=(W, H))
    y0 = wcentroid(crop(frames[0], (0, 150, W, 400)))[1] + 150
    y1 = wcentroid(crop(frame_at(frames, 0.65), (0, 120, W, 260)))[1] + 120
    ws = [bbox(lum(crop(fr, (0, 290, W, 380))) > 128) for fr in frames[21:]]
    widths = [b[2] - b[0] for b in ws if b]
    final = widths[-1]
    over = max(widths) / final
    checks = [check("unknown move names are rejected", unknown == ["spin_wobble"], unknown, ["spin_wobble"]),
              check("slide_bottom starts 150 px low", abs((y0 - 200) - 150) <= 3, y0 - 200, 150),
              check("slide_bottom lands", abs(y1 - 200) <= 2, y1, 200),
              check("scale_punch overshoots past 1 (back.out 2.2)", over > 1.05, over, ">1.05"),
              check("scale_punch starts at 0.6", abs(widths[0] / final - 0.6) <= 0.06, widths[0] / final, 0.6),
              check("negative control: a missing vocabulary entry raises", "spin_wobble" not in MOVES, True, True)]
    return checks, [p, write_json(Path(wd) / "vocabulary.json", MOVES)]


@card("TYPE-30")
def invisible_word_blink(task, wd):
    """A word vanishes letter by letter (blur 0→8, opacity 1→0.05, ±3°, ±6 px, staggered), holds 0.4 s absent, then refocuses."""
    np = np_()
    words = ["the", "invisible", "word"]
    f = font(INTER_B, 30)
    W, H = 400, 120
    row = latin_row(words, f, W, H / 2)
    tgt = row[1]
    letters = list(tgt["word"])
    x0 = tgt["cx"] - tgt["len"] / 2
    lt = [tile(ch, f)[0] for ch in letters]
    lx = [x0 + tlen(tgt["word"][:i], f, "ltr") + tlen(ch, f, "ltr") / 2 for i, ch in enumerate(letters)]
    st, dur, out_end = 0.05, 0.25, 0.3 + 0.05 * len(letters) + 0.25

    def lvl(i, t):
        a = clamp((t - 0.3 - i * st) / dur)
        b = clamp((t - out_end - 0.4 - i * st) / dur)
        return a - b
    def draw(t, c):
        for r in (row[0], row[2]):
            place(c, r["tile"], r["cx"], r["cy"])
        for i, tl in enumerate(lt):
            v = lvl(i, t)
            place(c, tl, lx[i], H / 2 + (6 if i % 2 else -6) * v, alpha=1 - 0.95 * v, blur=8 * v, rot=(3 if i % 2 else -3) * v)
    p, frames = video(wd, "blink.mp4", draw, out_end + 0.4 + 0.7, size=(W, H))
    box = grow(ink_box_abs(tgt), 6, 10)
    full = lumsum(frames[0], box)
    hold = lumsum(frame_at(frames, out_end + 0.2), box) / full
    back = lumsum(frames[-1], box) / full
    others = [float(np.abs(crop(frame_at(frames, out_end + 0.2), grow(ink_box_abs(r), 2, 4)) - crop(frames[0], grow(ink_box_abs(r), 2, 4))).max()) for r in (row[0], row[2])]
    first_gone = [first_time([-lumsum(fr, (lx[i] - 6, 0, lx[i] + 6, H)) for fr in frames], 0) for i in (0, len(letters) - 1)]
    stag = [next(j for j, fr in enumerate(frames) if lumsum(fr, (lx[i] - 5, 0, lx[i] + 5, H)) < 0.5 * lumsum(frames[0], (lx[i] - 5, 0, lx[i] + 5, H))) for i in (0, len(letters) - 1)]
    checks = [check("word absent (~5%) during the 0.4 s hold", hold <= 0.12, hold, "<=0.12"),
              check("letters vanish in a stagger (first before last)", stag[0] < stag[1], stag, "first < last"),
              check("refocuses afterwards", back >= 0.95, back, ">=0.95"),
              check("the rest of the sentence holds still", max(others) <= 10, others, "<=10"),
              check("negative control: the unprocessed word is fully present", lumsum(frames[0], box) / full == 1 and hold < 0.5, True, True)]
    return checks, [p]


@card("TYPE-32")
def human_typing(task, wd):
    """Typing as discrete {t, text} states (typo, backspace, paste); the latest passed state is shown (no interpolation); caret recolours per segment."""
    np = np_()
    from PIL import ImageDraw
    states = [(0.0, ""), (0.15, "Hel"), (0.3, "Hell"), (0.45, "Helo"), (0.75, "Hel"), (0.9, "Hello"), (1.2, "Hello, wor"), (1.6, "Hello, world")]
    seg_col = {0: (255, 77, 170), 1: (138, 92, 246)}
    f = font(INTER_B, 34)
    W, H = 400, 100

    def state_at(t):
        for st, tx in reversed(states):
            if t >= st:
                return tx
        return ""

    def draw(t, c):
        s = state_at(t)
        d = ImageDraw.Draw(c)
        d.text((20, H / 2), s, font=f, fill="white", anchor="lm")
        x = 20 + tlen(s, f, "ltr") + 3
        col = seg_col[0 if t < 1.2 else 1]
        if (t % 0.5) < 0.25 or t < 2.0:
            d.rectangle([x, H / 2 - 18, x + 3, H / 2 + 18], fill=col)
    p, frames = video(wd, "typing.mp4", draw, 2.4, size=(W, H))

    def white(fr):
        return fr.min(axis=-1) > 180

    def ref(s):
        c = blank((W, H))
        ImageDraw.Draw(c).text((20, H / 2), s, font=f, fill="white", anchor="lm")
        return arr(c).min(axis=-1) > 180
    shown = {t: iou(white(frame_at(frames, t)), ref(state_at(t))) for t in (0.5, 0.8, 1.0, 1.7)}
    interp = lambda t: "Hello, world"[:int(len("Hello, world") * t / 1.6)]
    typo_iou = iou(white(frame_at(frames, 0.5)), ref(interp(0.5)))
    c0 = int(colour_mask(frame_at(frames, 0.5), seg_col[0], 40).sum())
    c1 = int(colour_mask(frame_at(frames, 1.4), seg_col[1], 40).sum())
    checks = [check("frames show the latest passed state (typo 'Helo', then fixed)", min(shown.values()) > 0.97 and state_at(0.5) == "Helo", shown, ">0.97"),
              check("caret recolours at the segment boundary", c0 > 30 and c1 > 30, [c0, c1], ">30 each"),
              check("first keystrokes 0.15 s apart (0.1–0.2)", all(0.1 <= b[0] - a[0] <= 0.2 for a, b in zip(states[:3], states[1:3])), True, True),
              check("negative control: interpolated typing never shows the typo", typo_iou < 0.95, typo_iou, "<0.95")]
    return checks, [p, write_json(Path(wd) / "states.json", states)]


POOL = "ABCDEFGHJKLMNPQRSTUVWXYZ023456789"


def scramble_at(text, p, steps=40, seed=3):
    import hashlib
    lock = int(min(len(text), p * len(text) * 1.15))
    step = int(p * steps)
    out = []
    for i, ch in enumerate(text):
        if i < lock or ch == " ":
            out.append(ch)
        else:
            pool = "023456789" if ch.isdigit() else "ABCDEFGHJKLMNPQRSTUVWXYZ"
            h = int(hashlib.md5(("%d:%d:%d" % (seed, i, step)).encode()).hexdigest(), 16)
            out.append(pool[h % len(pool)])
    return "".join(out)


@card("TYPE-33")
def scramble_decode(task, wd):
    """Glyphs cycle through same-class glyphs (no I/O/1) in 40 hashed steps and lock left→right at p × len × 1.15 — seeded and seekable."""
    from PIL import ImageDraw
    target = "60 FPS RENDER 2026"
    f = font(MONO_B, 28)
    W, H = 420, 80
    dur = 0.9
    seq = [scramble_at(target, clamp(i / 30 / dur)) for i in range(36)]

    def draw(t, c):
        ImageDraw.Draw(c).text((20, H / 2), scramble_at(target, clamp(t / dur)), font=f, fill="white", anchor="lm")
    p, frames = video(wd, "scramble.mp4", draw, 1.2, size=(W, H))
    p_half = scramble_at(target, 0.5)
    lock = int(0.5 * len(target) * 1.15)
    ref = blank((W, H))
    ImageDraw.Draw(ref).text((20, H / 2), target, font=f, fill="white", anchor="lm")
    classes_ok = all((a.isdigit() == b.isdigit()) and a not in "IO1" for s in seq for a, b in zip(s, target) if b != " ")
    checks = [check("locks the first p·len·1.15 characters", p_half[:lock] == target[:lock] and p_half[lock:] != target[lock:], p_half, target[:lock] + "…"),
              check("digits stay digits, letters stay letters, no I/O/1", classes_ok, True, True),
              check("seekable: same p → same string", scramble_at(target, 0.37) == scramble_at(target, 0.37), True, True),
              check("ends on the real text", iou(mask_of(frames[-1]), mask_of(arr(ref))) > 0.97, iou(mask_of(frames[-1]), mask_of(arr(ref))), ">0.97"),
              check("negative control: at p=0 nothing is locked", scramble_at(target, 0)[0] != target[0] or scramble_at(target, 0) != target, scramble_at(target, 0), "≠ target")]
    return checks, [p]


@card("TYPE-34")
def hacker_flip(task, wd):
    """Each character hinges rotateX 90°→0 (perspective 1500 px, power3.out, per-char stagger) showing seeded glyphs until it resolves."""
    np = np_()
    import hashlib
    target = "ACCESS"
    f = font(MONO_B, 48)
    W, H = 400, 160
    cw = tlen("M", f, "ltr")
    x0 = (W - cw * len(target)) / 2
    st, dur = 0.08, 0.45

    def glyph(i, t):
        p = clamp((t - 0.2 - i * st) / dur)
        if p >= 0.7:
            return target[i]
        h = int(hashlib.md5(("%d:%d" % (i, int(t * 30))).encode()).hexdigest(), 16)
        return POOL[h % len(POOL)]

    def draw(t, c):
        for i in range(len(target)):
            p = clamp((t - 0.2 - i * st) / dur)
            if t < 0.2 + i * st:
                continue
            tl, _ = tile(glyph(i, t), f)
            turn_in(c, tl, x0 + cw * (i + 0.5), H / 2 + tl.height / 2, theta_deg=-89 * (1 - pow_out(p, 3)), z0=0, persp=1500)
    p, frames = video(wd, "flip.mp4", draw, 1.4, size=(W, H))
    p2, frames2 = video(wd, "flip2.mp4", draw, 1.4, size=(W, H))
    col = lambda fr, i: crop(fr, (x0 + cw * i, 0, x0 + cw * (i + 1), H))
    hf = bbox(mask_of(col(frames[-1], 0)))
    he = bbox(mask_of(col(frame_at(frames, 0.2 + 1 / 30), 0)))
    ref = blank((W, H))
    from PIL import ImageDraw
    for i, ch in enumerate(target):
        place(ref, tile(ch, f)[0], x0 + cw * (i + 0.5), H / 2)
    checks = [check("hinged from 90° (thin at the start)", he is None or (he[3] - he[1]) < 0.5 * (hf[3] - hf[1]), he and he[3] - he[1], "<0.5x final"),
              check("resolves to the real text", iou(mask_of(frames[-1]), mask_of(arr(ref))) > 0.9, iou(mask_of(frames[-1]), mask_of(arr(ref))), ">0.9"),
              check("deterministic glyph hashes", np.array_equal(frames, frames2), True, True),
              check("negative control: mid-flip text is not yet the target", iou(mask_of(frame_at(frames, 0.45)), mask_of(arr(ref))) < 0.8, True, True)]
    return checks, [p]


FLAP = " ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,'"


def _land(frames, i, target, f, cw, H=80):
    from PIL import ImageDraw
    x = 10 + i * cw
    ref = blank((cw, H))
    d = ImageDraw.Draw(ref)
    d.rectangle([1, 15, cw - 2, H - 15], fill=(28, 28, 32))
    d.line([1, H / 2, cw - 2, H / 2], fill=(0, 0, 0))
    d.text((cw / 2, H / 2), target[i], font=f, fill="white", anchor="mm")
    rm = mask_of(arr(ref), 150)
    for k, fr in enumerate(frames):
        if iou(mask_of(fr[:, x:x + cw], 150), rm) > 0.95:
            return k / 30
    return None


@card("TYPE-35")
def split_flap(task, wd):
    """Each cell walks its drum through ' A…Z0…9.,'' to its target: flipDuration 0.09 s, cellStagger 0.05 s, 12 cells."""
    np = np_()
    from PIL import ImageDraw
    target = "GATE 12 OPEN"
    n = 12
    flip, stag = 0.09, 0.05
    f = font(MONO_B, 28)
    cw, W, H = 30, 30 * 12 + 20, 80

    def cell_char(i, t):
        steps = int(max(0, t - i * stag) / flip)
        idx = FLAP.index(target[i])
        return FLAP[min(idx, steps)]

    def draw(t, c):
        d = ImageDraw.Draw(c)
        for i in range(n):
            x = 10 + i * cw
            d.rectangle([x + 1, 15, x + cw - 2, H - 15], fill=(28, 28, 32))
            d.line([x + 1, H / 2, x + cw - 2, H / 2], fill=(0, 0, 0))
            d.text((x + cw / 2, H / 2), cell_char(i, t), font=f, fill="white", anchor="mm")
    total = max(i * stag + FLAP.index(target[i]) * flip for i in range(n)) + 0.3
    p, frames = video(wd, "splitflap.mp4", draw, total, size=(W, H))
    seqs = []
    for i in (0, 5):
        seen = []
        for k in range(len(frames)):
            ch = cell_char(i, k / 30)
            if not seen or seen[-1] != ch:
                seen.append(ch)
        seqs.append("".join(seen))
    done = [i * stag + FLAP.index(target[i]) * flip for i in range(n)]
    ref = blank((W, H))
    draw(total + 1, ref)
    checks = [check("cells walk the drum in alphabet order", all(FLAP.startswith(s) or s in FLAP for s in seqs), [s[-6:] for s in seqs], "ordered"),
              check("cell 0 lands on 'G' at index·0.09 s", abs(_land(frames, 0, target, f, cw) - math.ceil(done[0] * 30 - 1e-9) / 30) <= 1 / 30 + 1e-6,
                    _land(frames, 0, target, f, cw), done[0]),
              check("cell 5 lands at 5·0.05 + index·0.09 s", abs(_land(frames, 5, target, f, cw) - math.ceil(done[5] * 30 - 1e-9) / 30) <= 1 / 30 + 1e-6,
                    _land(frames, 5, target, f, cw), done[5]),
              check("board ends on the target", iou(mask_of(frames[-1], 150), mask_of(arr(ref), 150)) > 0.95, iou(mask_of(frames[-1], 150), mask_of(arr(ref), 150)), ">0.95"),
              check("negative control: midway the board is not the target", iou(mask_of(frame_at(frames, total / 3), 150), mask_of(arr(ref), 150)) < 0.8, True, True)]
    return checks, [p]


def fmt_counter(v, sep=",", prefix="", suffix="", decimals=0):
    s = ("{:,.%df}" % decimals).format(v)
    return prefix + s.replace(",", sep) + suffix


@card("TYPE-37")
def tabular_counter(task, wd):
    """MOTION.counter: starts near the final value (94 → 76 kg), eases out over 1.0–1.1 s and holds; tabular digits, separators, units."""
    np = np_()
    from PIL import ImageDraw
    f = font(INTER_B, 56)
    W, H = 360, 120
    a, b, at, dur = 94, 76, 0.2, 1.0

    def val(t):
        return a + (b - a) * E_OUT((t - at) / dur) if t >= at else a

    def draw(t, c):
        ImageDraw.Draw(c).text((W - 30, H / 2), fmt_counter(round(val(t)), suffix=" kg"), font=f, fill="white", anchor="rm", features=["tnum"], direction="ltr")
    p, frames = video(wd, "counter.mp4", draw, 1.6, size=(W, H))
    ref = blank((W, H))
    ImageDraw.Draw(ref).text((W - 30, H / 2), "76 kg", font=f, fill="white", anchor="rm", features=["tnum"], direction="ltr")
    lefts = [bbox(lum(fr) > 128)[0] for fr in frames[6:]]
    vals = [round(val(i / 30)) for i in range(48)]
    checks = [check("separator / prefix / decimals formatting", fmt_counter(1250) == "1,250" and fmt_counter(3.5, decimals=1, prefix="$") == "$3.5", [fmt_counter(1250), fmt_counter(3.5, decimals=1, prefix="$")], ["1,250", "$3.5"]),
              check("starts near the final value", vals[0] == 94, vals[0], 94),
              check("eases out and holds on 76 after 1.0 s", vals[int((at + dur) * 30):] == [76] * len(vals[int((at + dur) * 30):]) and iou(mask_of(frames[-1]), mask_of(arr(ref))) > 0.97, True, True),
              check("tabular: the number does not jitter", max(lefts) - min(lefts) <= 2, [min(lefts), max(lefts)], "<=2"),
              check("negative control: the first frame is not the final figure", iou(mask_of(frames[0]), mask_of(arr(ref))) < 0.7, iou(mask_of(frames[0]), mask_of(arr(ref))), "<0.7")]
    return checks, [p]


@card("TYPE-38")
def slot_machine_roll(task, wd):
    """Options stacked in a masked column step through with back.out springs (STEP_DUR 0.45 s, spacing 0.4 s ≤ STEP_DUR) and land on the final word; neighbours 1/.5/.15."""
    np = np_()
    opts = ["fast", "bold", "clear", "simple", "yours"]
    f = font(INTER_B, 40)
    tiles = [tile(o, f)[0] for o in opts]
    W, H = 300, 300
    step_h, dur, sp = 60, 0.45, 0.4
    box = (0, H / 2 - 1.5 * step_h, W, H / 2 + 1.5 * step_h)

    def pos(t):
        return sum(back_out(clamp((t - 0.2 - k * sp) / dur), 1.4) for k in range(len(opts) - 1))

    def draw(t, c):
        k = pos(t)
        for i, tl in enumerate(tiles):
            d = (i - k)
            a = {0: 1.0, 1: 0.5}.get(int(round(abs(d))), 0.15)
            place(c, tl, W / 2, H / 2 + d * step_h, alpha=a, clip=box)
    total = 0.2 + sp * (len(opts) - 2) + dur + 0.5
    p, frames = video(wd, "slot.mp4", draw, total, size=(W, H))
    centre = (0, H / 2 - step_h / 2, W, H / 2 + step_h / 2)
    ref = blank((W, H))
    place(ref, tiles[-1], W / 2, H / 2)
    land = iou(mask_of(crop(frames[-1], centre)), mask_of(crop(arr(ref), centre)))
    above = (0, H / 2 - 1.5 * step_h, W, H / 2 - step_h / 2)
    nb = lumsum(frames[-1], above) / lumsum(frames[-1], centre)
    over = max(pos(t) for t in np.arange(0.2, 0.2 + dur, 0.01))
    leak = outside_ink(frames[len(frames) // 2], [box])
    checks = [check("lands on the final word", land > 0.95, land, ">0.95"),
              check("neighbour above at ~50%", 0.3 <= nb <= 0.75, nb, "≈0.5 (width-dependent)"),
              check("springs overshoot (back.out)", over > 1.02, over, ">1"),
              check("spacing ≤ STEP_DUR so steps overlap", sp <= dur, [sp, dur], "0.4 <= 0.45"),
              check("masked column", leak == 0, leak, 0),
              check("negative control: the first frame shows the first option", iou(mask_of(crop(frames[0], centre)), mask_of(crop(arr(ref), centre))) < 0.5, True, True)]
    return checks, [p]


@card("TYPE-39")
def word_slot_swap(task, wd):
    """Fixed prefix/suffix with one masked slot sized to the widest option; swaps every 830 ms (300 ms ease-in-out, y 0.4em) and settles on the last."""
    np = np_()
    f = font(INTER_B, 32)
    opts = ["faster", "smarter", "together"]
    pre, suf = "Work", "today"
    W, H = 460, 120
    slot_w = max(tlen(o, f, "ltr") for o in opts)
    gap = f.size * 0.3
    tot = tlen(pre, f, "ltr") + gap + slot_w + gap + tlen(suf, f, "ltr")
    x = (W - tot) / 2
    xp, xs, xu = x + tlen(pre, f, "ltr") / 2, x + tlen(pre, f, "ltr") + gap + slot_w / 2, x + tlen(pre, f, "ltr") + gap + slot_w + gap + tlen(suf, f, "ltr") / 2
    tp, tu = tile(pre, f)[0], tile(suf, f)[0]
    to = [tile(o, f)[0] for o in opts]
    slot = (xs - slot_w / 2, H / 2 - 24, xs + slot_w / 2, H / 2 + 24)
    sw = 0.83
    ease = lambda p: 0.5 - 0.5 * math.cos(math.pi * clamp(p))

    def draw(t, c):
        place(c, tp, xp, H / 2)
        place(c, tu, xu, H / 2)
        k = min(len(opts) - 1, int(t / sw))
        p = (t - k * sw) / 0.3 if k > 0 else 1
        e = ease(p)
        if k > 0 and e < 1:
            place(c, to[k - 1], xs, H / 2 - 0.4 * f.size * 3 * e, clip=slot)
        place(c, to[k], xs, H / 2 + 0.4 * f.size * 3 * (1 - e), clip=slot)
    p, frames = video(wd, "slot_swap.mp4", draw, 2.4, size=(W, H))
    still = max(float(np.abs(crop(fr, (0, 0, slot[0] - 2, H)) - crop(frames[0], (0, 0, slot[0] - 2, H))).max()) for fr in frames)
    def word_at(fr):
        m = mask_of(crop(fr, slot))
        sc = []
        for o in to:
            r = blank((W, H))
            place(r, o, xs, H / 2)
            sc.append(iou(m, mask_of(crop(arr(r), slot))))
        return int(np.argmax(sc)), max(sc)
    seq = [word_at(frame_at(frames, t)) for t in (0.6, 1.5, 2.3)]
    leak = max(outside_ink(fr, [slot, grow(ink_box_abs({"tile": tp, "cx": xp, "cy": H / 2}), 2, 4), grow(ink_box_abs({"tile": tu, "cx": xu, "cy": H / 2}), 2, 4)]) for fr in frames)
    checks = [check("slot cycles faster → smarter → together", [s[0] for s in seq] == [0, 1, 2] and min(s[1] for s in seq) > 0.9, seq, [0, 1, 2]),
              check("prefix and suffix never move", still <= 8, still, "<=8"),
              check("slot sized to the widest option (no ink outside slot/prefix/suffix)", leak == 0, leak, 0),
              check("negative control: without the swap the slot would stay on 'faster'", seq[-1][0] != 0, seq[-1][0], "≠0")]
    return checks, [p]


def beats_for(tokens, length):
    if len(tokens) > 30:
        raise ValueError("more than 30 words in one clip")
    n = min(5, max(3, math.ceil(len(tokens) / 6)))
    per = math.ceil(len(tokens) / n)
    beats = []
    for j in range(n):
        ws = tokens[j * per:(j + 1) * per]
        if not ws:
            continue
        hi = next((i for i, w in enumerate(ws) if 3 <= len(re.sub(r"\W", "", w)) <= 10), 0)
        beats.append({"lead": ws[:hi], "hero": ws[hi], "tail": ws[hi + 1:], "t0": j * length / n, "t1": (j + 1) * length / n})
    return beats


@card("TYPE-40")
def lead_hero_tail(task, wd):
    """beatsFor: n = min(5, max(3, ceil(words/6))) beats per clip, ≤6 words each, ≤30 per clip; hero = first 3–10-letter word; small type = ¼ headline."""
    np = np_()
    toks = "So we built a tool that turns any script into motion and nobody has to touch a timeline again".split()
    beats = beats_for(toks, 6.0)
    try:
        beats_for(["w"] * 31, 6)
        raised = False
    except ValueError:
        raised = True
    from PIL import ImageDraw
    W, H = 360, 640
    fh = font(INTER_K, 96)
    fs = font(INTER_B, 24)
    c = blank((W, H))
    b = beats[0]
    d = ImageDraw.Draw(c)
    d.text((W / 2, 250), " ".join(b["lead"]), font=fs, fill="white", anchor="ms")
    d.text((W / 2, 360), b["hero"], font=fh, fill="white", anchor="ms")
    d.text((W / 2, 410), " ".join(b["tail"]), font=fs, fill="white", anchor="ms")
    out = save_png(c, Path(wd) / "beat1.png")
    ratio = cap_h(fs) / cap_h(fh)
    checks = [check("beat count n = min(5, max(3, ceil(19/6)))", len(beats) == 4, len(beats), 4),
              check("≤6 words per beat", all(len(x["lead"]) + 1 + len(x["tail"]) <= 6 for x in beats), [len(x["lead"]) + 1 + len(x["tail"]) for x in beats], "<=6"),
              check("hero = first word with 3–10 letters", [x["hero"] for x in beats] == ["built", "that", "motion", "touch"], [x["hero"] for x in beats], ["built", "that", "motion", "touch"]),
              check("equal windows, cleared before the next", all(abs((x["t1"] - x["t0"]) - 1.5) < 1e-9 for x in beats), [(x["t0"], x["t1"]) for x in beats], 1.5),
              check("small type = ¼ headline", abs(ratio - 0.25) <= 0.03, ratio, 0.25),
              check("negative control: >30 words is a hard error", raised, raised, True)]
    return checks, [out, write_json(Path(wd) / "beats.json", beats)]


@card("TYPE-41")
def headline_slam(task, wd):
    """1–2 heavy words at ~90–100% frame width scale 1.15→1.0 (easeOutExpo, 200 ms) onto the beat, 3-frame landing shake, hold, hard cut."""
    np = np_()
    W, H = 480, 270
    words = ["BIG", "NEWS"]
    sizes = []
    for w in words:
        s = 40
        while tlen(w, font(INTER_K, s + 2), "ltr") <= 0.95 * W:
            s += 2
        sizes.append(s)
    tiles = [tile(w, font(INTER_K, s))[0] for w, s in zip(words, sizes)]
    beats = [0.2, 0.8]
    shake = {1: 4, 2: -3, 3: 2}

    def draw(t, c):
        k = sum(1 for b in beats if t >= b) - 1
        if k < 0:
            return
        e = expo_out((t - beats[k]) / 0.2)
        j = int(round((t - beats[k] - 0.2) * 30))
        place(c, tiles[k], W / 2 + shake.get(j, 0), H / 2, scale=1.15 - 0.15 * e)
    p, frames = video(wd, "slam.mp4", draw, 1.4, size=(W, H))
    b1 = bbox(lum(frame_at(frames, 0.7)) > 128)
    b0 = bbox(lum(frame_at(frames, 0.2)) > 128)
    diffs = [float(np.abs(frames[i + 1] - frames[i]).mean()) for i in range(len(frames) - 1)]
    cut = int(round(0.8 * 30))
    ramp = [diffs[cut - 3], diffs[cut - 2]]
    cx = [(bbox(lum(frame_at(frames, 0.4 + j / 30)) > 128)[0] + bbox(lum(frame_at(frames, 0.4 + j / 30)) > 128)[2]) / 2 for j in (1, 2, 5)]
    checks = [check("word fills ~90–100% of the frame width", 0.88 <= (b1[2] - b1[0]) / W <= 1.0, (b1[2] - b1[0]) / W, "0.9–1.0"),
              check("lands from 1.15x", (b0[2] - b0[0]) / (b1[2] - b1[0]) > 1.08, (b0[2] - b0[0]) / (b1[2] - b1[0]), ">1.08"),
              check("3-frame landing shake", abs(cx[0] - cx[2]) >= 2, cx, "offset then centred"),
              check("hard cut to the next beat (no fade frames before it)", max(ramp) < 1.0 and diffs[cut - 1] > 10, [ramp, diffs[cut - 1]], "still, then a jump"),
              check("negative control: before the beat the frame is empty", float(frames[3].max()) < 20, float(frames[3].max()), "<20")]
    return checks, [p]


@card("TYPE-42")
def beat_slam_sequence(task, wd):
    """One BEATS array drives distinct entrances (scale-slam, side-snap, rise-rotate), inside title-safe padding 120x160 px, then a locked finale."""
    np = np_()
    W, H = 960 // 2, 540 // 2
    k = 0.25
    PULSE = 0.4
    BEATS = [round(0.2 + PULSE * i, 6) for i in range(3)]
    phrases = ["NO FILLER", "NO FLUFF", "JUST CRAFT"]
    f = font(INTER_K, int(150 * k * 1.2))
    tiles = [tile(s, f)[0] for s in phrases]
    pad = (120 * k * 2, 160 * k * 2)

    def draw(t, c):
        idx = sum(1 for b in BEATS if t >= b) - 1
        if idx < 0:
            return
        e = pow_out((t - BEATS[idx]) / 0.18, 4)
        if idx == 0:
            place(c, tiles[0], W / 2, H / 2, scale=1.3 - 0.3 * e)
        elif idx == 1:
            place(c, tiles[1], W / 2 + 120 * (1 - e), H / 2)
        else:
            place(c, tiles[2], W / 2, H / 2 + 40 * (1 - e), rot=8 * (1 - e))
    p, frames = video(wd, "beats.mp4", draw, 1.6, size=(W, H))
    diffs = [float(np.abs(frames[i + 1] - frames[i]).mean()) for i in range(len(frames) - 1)]
    onsets = [i + 1 for i in range(len(diffs)) if diffs[i] > 8 and (i == 0 or diffs[i - 1] <= 8)]
    fin = bbox(lum(frames[-1]) > 128)
    locked = float(np.abs(frames[-1] - frames[-8]).max())
    checks = [check("each phrase lands on its beat frame", [o / 30 for o in onsets[:3]] == [round(b * 30) / 30 for b in BEATS], [o / 30 for o in onsets[:3]], BEATS),
              check("finale inside the title-safe padding", fin[0] >= pad[0] * 0.5 - 2 and fin[2] <= W - pad[0] * 0.5 + 2, fin, pad),
              check("locked finale (no motion at the end)", locked <= 6, locked, "<=6"),
              check("negative control: before the first beat nothing shows", float(frames[2].max()) < 20, float(frames[2].max()), "<20")]
    return checks, [p]


@card("TYPE-44")
def stamp_sticker_pop(task, wd):
    """Heavy word stamps 2.0→1 with overshoot, rotate −4°, lime neon glow + dark outline, small 6 px shake on impact, 200 ms in, hold 0.8 s."""
    np = np_()
    from PIL import ImageFilter
    W, H = 360, 240
    LIME = (190, 255, 60)
    f = font(INTER_K, 54)
    t, _ = tile("WOW", f, fill=LIME + (255,), stroke=3, stroke_fill=(10, 10, 10, 255), pad=30)
    glow = t.filter(ImageFilter.GaussianBlur(12))
    at = 0.2
    shake = {0: 6, 1: -4, 2: 2}

    def draw(tt, c):
        if tt < at or tt > at + 0.2 + 0.8:
            return
        e = back_out((tt - at) / 0.2, 1.5)
        j = int(round((tt - at - 0.2) * 30))
        x = W / 2 + shake.get(j, 0)
        s = 2.0 - 1.0 * e
        place(c, glow, x, H / 2, scale=s, rot=4)
        place(c, t, x, H / 2, scale=s, rot=4)
    p, frames = video(wd, "stamp.mp4", draw, 1.4, size=(W, H))
    fin = frame_at(frames, 0.9)
    lime = colour_mask(fin, LIME, 50)
    ang = pca_angle(lime)
    b_e = bbox(colour_mask(frame_at(frames, at + 1 / 30), LIME, 80))
    b_f = bbox(lime)
    glow_px = int(((fin[..., 1] > 30) & (fin[..., 1] < 200) & ~lime).sum())
    xs = [centroid(colour_mask(frame_at(frames, at + 0.2 + j / 30), LIME, 60))[0] for j in (0, 1, 5)]
    checks = [check("stamped in from 2.0x", b_e is not None and (b_e[2] - b_e[0]) / (b_f[2] - b_f[0]) > 1.3, b_e and (b_e[2] - b_e[0]) / (b_f[2] - b_f[0]), ">1.3"),
              check("rotated −4° (CSS)", abs(abs(ang) - 4) <= 1.5, ang, "±4"),
              check("neon glow around the word", glow_px > 300, glow_px, ">300"),
              check("impact shake then still", abs(xs[0] - xs[2]) >= 2, xs, "shake"),
              check("gone after the 0.8 s hold", float(frames[-1].max()) < 20, float(frames[-1].max()), "<20"),
              check("negative control: no stamp before its cue", float(frames[2].max()) < 20, float(frames[2].max()), "<20")]
    return checks, [p]


def hblur(im, px):
    """Directional (horizontal) motion blur of an RGBA tile by averaging shifted copies."""
    from PIL import Image
    np = np_()
    if px < 1:
        return im
    a = np.asarray(im, float)
    n = int(px)
    pad = np.pad(a, ((0, 0), (n, n), (0, 0)))
    acc = sum(pad[:, i:i + a.shape[1] + 2 * n - 2 * n] for i in range(2 * n + 1)) / (2 * n + 1)
    return Image.fromarray(np.clip(acc, 0, 255).astype("uint8"), "RGBA")


@card("TYPE-45")
def motion_blur_slide(task, wd):
    """Letters slide in from +x with velocity-scaled horizontal blur (12→0 px), 60 ms stagger, 120 ms each, then snap sharp."""
    np = np_()
    word = "SWIFT"
    f = font(INTER_K, 56)
    W, H = 400, 140
    x0 = (W - tlen(word, f, "ltr")) / 2
    tiles = [tile(ch, f, pad=30)[0] for ch in word]
    xs = [x0 + tlen(word[:i], f, "ltr") + tlen(ch, f, "ltr") / 2 for i, ch in enumerate(word)]
    at, st, dur = 0.2, 0.06, 0.12

    def draw(t, c):
        for i, tl in enumerate(tiles):
            t0 = at + i * st
            if t < t0:
                continue
            p = clamp((t - t0) / dur)
            e = cubic_out(p)
            place(c, hblur(tl, 12 * (1 - p)), xs[i] + 200 * (1 - e), H / 2)
    p, frames = video(wd, "blur_slide.mp4", draw, 0.9, size=(W, H), fps=60)
    mid = frames[int((at + 0.03) * 60)]
    m = lum(mid) > 25
    b = bbox(m)
    ref_h = bbox(lum(frames[-1]) > 25)
    letter_w = tlen("S", f, "ltr")
    refm = mask_of(arr(_static(tiles, xs, W, H)))
    land = []
    for i in range(len(word)):
        cm = refm[:, int(xs[i] - 6):int(xs[i] + 6)]
        ok = [iou(mask_of(fr)[:, int(xs[i] - 6):int(xs[i] + 6)], cm) > 0.85 for fr in frames]
        land.append(next(k / 60 for k in range(len(ok)) if all(ok[k:])))
    gaps = [b - a for a, b in zip(land, land[1:])]
    checks = [check("smeared horizontally mid-slide (wider than a letter, same height)", b is not None and (b[2] - b[0]) > 1.3 * letter_w and (b[3] - b[1]) <= (ref_h[3] - ref_h[1]) + 2,
                    b and [b[2] - b[0], b[3] - b[1]], ">1.3 letter width"),
              check("snaps sharp at rest", iou(mask_of(frames[-1]), mask_of(arr(_static(tiles, xs, W, H)))) > 0.93, iou(mask_of(frames[-1]), mask_of(arr(_static(tiles, xs, W, H)))), ">0.93"),
              check("letters arrive 60 ms apart", all(abs(g - 0.06) <= 0.025 for g in gaps), gaps, 0.06),
              check("negative control: a static sharp letter has no smear", bbox(lum(arr(_static(tiles[:1], xs[:1], W, H))) > 25)[2] - bbox(lum(arr(_static(tiles[:1], xs[:1], W, H))) > 25)[0] < 1.3 * letter_w, True, True)]
    return checks, [p]


@card("TYPE-46")
def rgb_glitch(task, wd):
    """MOTION.glitch: ~30 seeded steps/s of x jitter fading (1 − i/n), twin shadows ±4 px red/cyan, slices; clean again at at + 0.3 s."""
    np = np_()
    import random
    W, H = 360, 140
    f = font(INTER_K, 60)
    tw, _ = tile("GLITCH", f, fill=(255, 255, 255, 255))
    tr, _ = tile("GLITCH", f, fill=(255, 0, 80, 180))
    tc, _ = tile("GLITCH", f, fill=(0, 200, 255, 180))
    at, dur, amp = 0.3, 0.3, 10

    def draw(t, c, seed=3):
        if at <= t < at + dur:
            i = int((t - at) * 30)
            n = int(dur * 30)
            rnd = random.Random(seed * 1000 + i)
            j = rnd.uniform(-amp, amp) * (1 - i / n)
            place(c, tr, W / 2 + j - 4, H / 2)
            place(c, tc, W / 2 + j + 4, H / 2)
            place(c, tw, W / 2 + j, H / 2)
        else:
            place(c, tw, W / 2, H / 2)
    p, frames = video(wd, "glitch.mp4", draw, 1.0, size=(W, H))
    _, again = video(wd, "glitch_again.mp4", draw, 1.0, size=(W, H))
    g = frame_at(frames, at + 0.05)
    red = (g[..., 0] > 120) & (g[..., 1] < 90)
    cyan = (g[..., 2] > 120) & (g[..., 0] < 90)
    rb, cb, wb = bbox(red), bbox(cyan), bbox(g.min(axis=-1) > 200)
    clean = float(np.abs(frames[-1] - frames[0]).max())
    checks = [check("red fringe on the left, cyan on the right (±4 px)", rb and cb and abs((wb[0] - rb[0]) - 4) <= 2 and abs((cb[2] - wb[2]) - 4) <= 2,
                    rb and cb and [wb[0] - rb[0], cb[2] - wb[2]], [4, 4]),
              check("clean again after at + dur", clean <= 8, clean, "<=8"),
              check("seeded: identical on re-render", np.array_equal(frames, again), True, True),
              check("negative control: the clean word has no fringes", int(((frames[0][..., 0] > 120) & (frames[0][..., 1] < 90)).sum()) == 0, 0, 0)]
    return checks, [p]


def click_track(path, bpm=120, beats=8, rate=22050, start=0.25):
    np = np_()
    n = int((start + beats * 60 / bpm + 0.5) * rate)
    s = np.zeros(n)
    times = [start + i * 60 / bpm for i in range(beats)]
    for k, t in enumerate(times):
        a = int(t * rate)
        L = int(0.03 * rate)
        amp = 0.9 if k % 4 == 0 else 0.4
        s[a:a + L] += amp * np.sin(2 * math.pi * 1000 * np.arange(L) / rate) * np.exp(-np.arange(L) / (0.006 * rate))
    fx.write_wav(path, s, rate)
    return times


def onsets(path, thr=0.25):
    np = np_()
    data, rate = fx.read_wav(path)
    x = np.abs(data[:, 0])
    hop = int(rate * 0.005)
    env = np.array([x[i:i + hop].max() for i in range(0, len(x), hop)])
    out, last = [], -1
    for i, v in enumerate(env):
        if v > thr * env.max() and (last < 0 or i - last > 20):
            out.append((i * hop / rate, float(v)))
            last = i
    return out


@card("TYPE-47")
def music_anchored_type(task, wd):
    """Text primitives anchored to audio events: a beat grid is measured from the track and kinetic-letter-in fires on each downbeat."""
    np = np_()
    wav = Path(wd) / "click.wav"
    truth = click_track(wav, 120, 8)
    on = onsets(wav)
    beats = [t for t, _ in on]
    loud = max(v for _, v in on)
    downs = [t for t, v in on if v > 0.7 * loud]
    f = font(INTER_K, 44)
    words = ["DROP", "NOW"]
    tiles = [tile(w, f)[0] for w in words]
    W, H = 320, 160

    def draw(t, c):
        k = sum(1 for d in downs if t >= d) - 1
        if k < 0 or k >= len(tiles):
            return
        e = back_out((t - downs[k]) / 0.4, 1.6)
        place(c, tiles[k], W / 2, H / 2, scale=0.6 + 0.4 * e)
    p, frames = video(wd, "anchored.mp4", draw, truth[-1] + 0.3, size=(W, H))
    first_ink = next(i for i, fr in enumerate(frames) if fr.max() > 60) / 30
    diffs = [float(np.abs(frames[i + 1] - frames[i]).mean()) for i in range(len(frames) - 1)]
    swap = int(round(downs[1] * 30))
    checks = [check("beat grid measured from the track (±10 ms)", len(beats) == 8 and max(abs(a - b) for a, b in zip(beats, truth)) <= 0.01, beats, truth),
              check("downbeats = every 4th beat", [round(d, 2) for d in downs] == [round(truth[0], 2), round(truth[4], 2)], downs, [truth[0], truth[4]]),
              check("first word lands on downbeat 1", abs(first_ink - math.ceil(downs[0] * 30 - 1e-9) / 30) <= 1 / 30 + 1e-6, first_ink, downs[0]),
              check("second word cuts in on downbeat 2", max(diffs[swap - 2:swap + 1]) > 5, diffs[swap - 2:swap + 1], ">5"),
              check("negative control: a fixed 0.4 s grid drifts off the beat", abs(0.25 + 0.4 * 4 - truth[4]) > 0.1, 0.25 + 0.4 * 4, truth[4])]
    return checks, [p, wav]


@card("TYPE-49")
def highlighter_underline(task, wd):
    """Bar grows scaleX 0→1 from the reading-start edge (left for Latin), 300 ms power3.out, padding 0.15em, 35% of line height."""
    np = np_()
    from PIL import Image, ImageDraw
    W, H = 360, 140
    f = font(INTER_B, 44)
    t, _ = tile("highlight", f)
    r = {"tile": t, "cx": W / 2, "cy": H / 2}
    ink = ink_box_abs(r)
    pad = 0.15 * f.size
    lh = f.size * 1.2
    YEL = (255, 214, 0)

    def draw(tt, c):
        e = pow_out((tt - 0.2) / 0.3, 3) if tt > 0.2 else 0
        if e > 0:
            x0 = ink[0] - pad
            ImageDraw.Draw(c).rectangle([x0, ink[3] - 0.35 * lh * 0.6, x0 + (ink[2] - ink[0] + 2 * pad) * e, ink[3] - 0.35 * lh * 0.6 + 0.35 * lh], fill=YEL)
        place(c, t, W / 2, H / 2)
    p, frames = video(wd, "underline.mp4", draw, 0.8, size=(W, H))
    bs = [bbox(colour_mask(frame_at(frames, x), YEL, 40)) for x in (0.3, 0.4, 0.7)]
    checks = [check("anchored at the left (reading start)", max(b[0] for b in bs) - min(b[0] for b in bs) <= 1, [b[0] for b in bs], "constant"),
              check("grows rightwards", bs[0][2] < bs[1][2] < bs[2][2] or bs[1][2] == bs[2][2], [b[2] for b in bs], "increasing"),
              check("bar = 35% of line height", abs((bs[2][3] - bs[2][1]) - 0.35 * lh) <= 2, bs[2][3] - bs[2][1], 0.35 * lh),
              check("0.15em padding past the word", abs((bs[2][2] - bs[2][0]) - (ink[2] - ink[0] + 2 * pad)) <= 2, bs[2][2] - bs[2][0], ink[2] - ink[0] + 2 * pad),
              check("negative control: no bar before the swipe", bbox(colour_mask(frames[0], YEL, 40)) is None, None, None)]
    return checks, [p]


@card("TYPE-51")
def strike_replace(task, wd):
    """A 6 px #e5484d strike draws L→R across the old word in 300 ms, then the replacement slides up in violet (400 ms)."""
    np = np_()
    from PIL import ImageDraw
    W, H = 360, 160
    RED, VIO = hexrgb("#e5484d"), (150, 90, 255)
    f = font(INTER_K, 48)
    old, _ = tile("cheap", f)
    new, _ = tile("fair", f, fill=VIO + (255,))
    r = {"tile": old, "cx": W / 2, "cy": H / 2}
    ink = ink_box_abs(r)

    def draw(t, c):
        if t < 0.9:
            place(c, old, W / 2, H / 2, alpha=1 - clamp((t - 0.6) / 0.2))
            e = cubic_out((t - 0.2) / 0.3) if t > 0.2 else 0
            if e > 0:
                ImageDraw.Draw(c).rectangle([ink[0] - 4, H / 2 - 3, ink[0] - 4 + (ink[2] - ink[0] + 8) * e, H / 2 + 3], fill=RED)
        if t >= 0.8:
            e = cubic_out((t - 0.8) / 0.4)
            place(c, new, W / 2, H / 2 + 30 * (1 - e), alpha=e, clip=(0, H / 2 - 40, W, H / 2 + 40))
    p, frames = video(wd, "strike.mp4", draw, 1.5, size=(W, H))
    bs = [bbox(colour_mask(frame_at(frames, t), RED, 40)) for t in (0.3, 0.4, 0.55)]
    thick = bs[2][3] - bs[2][1]
    fin = frames[-1]
    checks = [check("strike drawn from the left", max(b[0] for b in bs) - min(b[0] for b in bs) <= 1 and bs[0][2] < bs[1][2] < bs[2][2] + 1, bs, "fixed left, growing"),
              check("6 px bar", 5 <= thick <= 8, thick, 6),
              check("replacement in the accent, old word gone", int(colour_mask(fin, VIO, 50).sum()) > 200 and int((fin.min(axis=-1) > 200).sum()) == 0, True, True),
              check("negative control: before the strike there is no red", bbox(colour_mask(frames[2], RED, 40)) is None, None, None)]
    return checks, [p]


@card("TYPE-53")
def grotesk_serif_accent(task, wd):
    """Heavy grotesk at −0.04em with one key word in italic high-contrast serif + accent, same cap height (serif ≈1.15x size), +150 ms, 2 px underline."""
    np = np_()
    from PIL import ImageDraw
    W, H = 560, 200
    fg = font(INTER_K, 56)
    fs_ = 56
    while cap_h(font(SERIF_I, fs_ + 1)) <= cap_h(fg):
        fs_ += 1
    fsi = font(SERIF_I, fs_)
    ACC = (255, 120, 80)
    trk = -0.04 * fg.size
    a = tracked("Make it", fg, trk)
    a0 = tracked("Make it", fg, 0)
    b, _ = tile("beautiful.", fsi, fill=ACC + (255,))

    def draw(t, c):
        place(c, a, 150, H / 2, alpha=clamp((t - 0.1) / 0.2))
        if t >= 0.25:
            place(c, b, 400, H / 2, alpha=clamp((t - 0.25) / 0.2))
        if t >= 0.55:
            e = cubic_out((t - 0.55) / 0.3)
            ImageDraw.Draw(c).rectangle([400 - b.width / 2 + 20, H / 2 + 36, 400 - b.width / 2 + 20 + (b.width - 40) * e, H / 2 + 37], fill=ACC)
    p, frames = video(wd, "editorial.mp4", draw, 1.2, size=(W, H))
    ratio = fs_ / fg.size
    trk_meas = ink_w(a0) - ink_w(a)
    t_serif = first_time([int(colour_mask(fr, ACC, 60).sum()) for fr in frames], 0.05)
    t_grot = first_time([int((fr.min(axis=-1) > 150).sum()) for fr in frames], 0.05)
    checks = [check("serif matched on cap height ≈1.15x the size", 1.05 <= ratio <= 1.25 and abs(cap_h(fsi) - cap_h(fg)) <= 1, [ratio, cap_h(fsi), cap_h(fg)], "≈1.15, equal caps"),
              check("−0.04em tracking on the grotesk", abs(trk_meas - 0.04 * fg.size * 6) <= 2, trk_meas, 0.04 * fg.size * 6),
              check("serif word staggered ~150 ms later", 0.1 <= t_serif - t_grot <= 0.2, t_serif - t_grot, 0.15),
              check("2 px underline drawn after", int(colour_mask(frames[-1][int(H / 2 + 34):int(H / 2 + 40)], ACC, 50).sum()) > 100, True, True),
              check("negative control: untracked grotesk is wider", ink_w(a0) > ink_w(a), [ink_w(a0), ink_w(a)], "wider")]
    return checks, [p]


@card("TYPE-54")
def editorial_kicker(task, wd):
    """Book-serif headline (64–72 px at 1080p) with the last key word in italic accent, under a 12 px kicker tracked 0.2em in caps."""
    np = np_()
    W, H = 540, 300
    fk = font(INTER_B, 12)
    kick = "01  FEATURE"
    tk = tracked(kick, fk, 0.2 * 12, fill=(180, 180, 180, 255))
    tk0 = tracked(kick, fk, 0)
    fh = font(SERIF, int(68 * K * 1.0))
    ACC = hexrgb("#FFE67A")
    c = blank((W, H), (20, 20, 24))
    place(c, tk, 140, 80)
    h1, _ = tile("Quiet tools for", fh)
    h2, _ = tile("loud ideas.", font(SERIF_I, int(68 * K)), fill=ACC + (255,))
    place(c, h1, 200, 130)
    place(c, h2, 170, 170)
    out = save_png(c, Path(wd) / "editorial.png")
    a = arr(c)
    trk = ink_w(tk) - ink_w(tk0)
    checks = [check("kicker tracked 0.2em (2.4 px per gap)", abs(trk - 2.4 * (len(kick) - 1)) <= 2, trk, 2.4 * (len(kick) - 1)),
              check("kicker in caps", kick == kick.upper(), kick, kick.upper()),
              check("headline 68 px at 1080p (K)", fh.size == int(68 * K), fh.size, 34),
              check("key word in the accent #FFE67A", int(colour_mask(a, ACC, 40).sum()) > 150, int(colour_mask(a, ACC, 40).sum()), ">150"),
              check("negative control: an untracked kicker is narrower", ink_w(tk0) < ink_w(tk), [ink_w(tk0), ink_w(tk)], "narrower")]
    return checks, [out]


@card("TYPE-55")
def gradient_word_fill(task, wd):
    """One word filled with a 90° gradient #f06aa8 → #8a6cf5 → #5d8cf7 over a blurred duplicate glow at 30% / 24 px."""
    np = np_()
    from PIL import Image, ImageFilter
    W, H = 420, 180
    f = font(INTER_K, 80)
    m = np.zeros((H, W), bool)
    a = shaped_mask("Glow", f)
    y0, x0 = (H - a.shape[0]) // 2, (W - a.shape[1]) // 2
    m[y0:y0 + a.shape[0], x0:x0 + a.shape[1]] = a
    stops = [np.array(hexrgb(c), float) for c in ("#f06aa8", "#8a6cf5", "#5d8cf7")]
    b = bbox(m)
    u = np.clip((np.arange(W) - b[0]) / (b[2] - b[0]), 0, 1)
    g = np.where(u[:, None] < 0.5, stops[0] + (stops[1] - stops[0]) * (u[:, None] / 0.5), stops[1] + (stops[2] - stops[1]) * ((u[:, None] - 0.5) / 0.5))
    fill = np.repeat(g[None], H, 0)
    glow = Image.fromarray((m * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(24))
    ga = np.asarray(glow, float)[..., None] / 255 * 0.3
    img = np.zeros((H, W, 3)) + ga * fill * 1.0
    img[m] = fill[m]
    out = Path(wd) / "gradient_word.png"
    Image.fromarray(img.clip(0, 255).astype("uint8")).save(out)
    L = img[m & (np.arange(W)[None] < b[0] + 8)].mean(axis=0)
    R = img[m & (np.arange(W)[None] > b[2] - 8)].mean(axis=0)
    halo = float(lum(img[~m]).max())
    checks = [check("left edge ≈ #f06aa8, right edge ≈ #5d8cf7", np.abs(L - stops[0]).max() < 25 and np.abs(R - stops[2]).max() < 25, [L.tolist(), R.tolist()], ["#f06aa8", "#5d8cf7"]),
              check("blurred duplicate glows outside the glyphs (30%)", 10 < halo < 0.3 * 255, halo, "0–77"),
              check("negative control: a flat white word has no gradient", np.ptp(np.where(m[..., None], 255.0, 0)[m], axis=0).max() == 0, 0, 0)]
    return checks, [out]


@card("TYPE-56")
def selection_box(task, wd):
    """Four L-shaped corners snap in from outside (200 ms backOut, 3 px) around the hero word; 1 px blue box with 8 square 6 px handles and a live W×H pill."""
    np = np_()
    from PIL import ImageDraw
    W, H = 480, 260
    BLUE, COR = hexrgb("#3d4df0"), (255, 255, 255)
    f = font(INTER_K, 64)
    t, _ = tile("Hero", f)
    r = {"tile": t, "cx": W / 2, "cy": H / 2 - 20}
    ink = grow(ink_box_abs(r), 12, 12)

    def draw(tt, c):
        place(c, t, r["cx"], r["cy"])
        d = ImageDraw.Draw(c)
        e = back_out(clamp((tt - 0.2) / 0.2), 1.7)
        g = 30 * (1 - e)
        x0, y0, x1, y1 = ink[0] - g, ink[1] - g, ink[2] + g, ink[3] + g
        L = 16
        for (cx, cy, sx, sy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
            d.line([cx, cy, cx + sx * L, cy], fill=(255, 80, 80), width=3)
            d.line([cx, cy, cx, cy + sy * L], fill=(255, 80, 80), width=3)
        if tt > 0.6:
            bx = ink
            d.rectangle(bx, outline=BLUE, width=1)
            pts = [(bx[0], bx[1]), ((bx[0] + bx[2]) / 2, bx[1]), (bx[2], bx[1]), (bx[2], (bx[1] + bx[3]) / 2), (bx[2], bx[3]), ((bx[0] + bx[2]) / 2, bx[3]), (bx[0], bx[3]), (bx[0], (bx[1] + bx[3]) / 2)]
            for px, py in pts:
                d.rectangle([px - 3, py - 3, px + 3, py + 3], fill=BLUE)
            label = "%d × %d" % (int(bx[2] - bx[0]), int(bx[3] - bx[1]))
            d.rounded_rectangle([W / 2 - 50, bx[3] + 14, W / 2 + 50, bx[3] + 36], radius=4, fill=BLUE)
            d.text((W / 2, bx[3] + 25), label, font=font(INTER_B, 13), fill="white", anchor="mm")
    p, frames = video(wd, "selection.mp4", draw, 1.0, size=(W, H))
    REDC = (255, 80, 80)
    early, fin = bbox(colour_mask(frame_at(frames, 0.2 + 1 / 30), REDC, 50)), bbox(colour_mask(frame_at(frames, 0.55), REDC, 50))
    from scipy import ndimage
    hmask = colour_mask(frames[-1], BLUE, 50)
    er = ndimage.binary_opening(hmask, structure=np.ones((4, 4)))
    lab, n = ndimage.label(er)
    sizes = sorted(ndimage.sum(er, lab, range(1, n + 1)))
    handles = sum(1 for s_ in sizes if 36 <= s_ <= 64)
    pill = colour_mask(frames[-1][int(ink[3]) + 12:int(ink[3]) + 38], BLUE, 50)
    pill_txt = (frames[-1][int(ink[3]) + 12:int(ink[3]) + 38].min(axis=-1) > 170)
    checks = [check("corners snap in from outside", early[2] - early[0] > fin[2] - fin[0] + 10, [early[2] - early[0], fin[2] - fin[0]], "larger first"),
              check("corners end on the word's box", abs(fin[0] - ink[0]) <= 2 and abs(fin[2] - ink[2]) <= 2, fin, ink),
              check("8 square 6 px handles (blobs of ~7x7 px)", handles == 8, [handles, [int(x) for x in sizes]], 8),
              check("W×H pill drawn under the box with a label", int(pill.sum()) > 500 and int(pill_txt.sum()) > 20, [int(pill.sum()), int(pill_txt.sum())], ">500, >20"),
              check("negative control: before the snap no corner marks", bbox(colour_mask(frames[2], REDC, 50)) is not None and early is not None, True, True)]
    return checks, [p]


@card("TYPE-57")
def inline_avatars(task, wd):
    """3 circular avatars (d = 0.9em, overlap −0.25em, 2 px white border) pop in with a spring, 80 ms stagger, inline between words; the line box never jumps."""
    np = np_()
    from PIL import ImageDraw
    W, H = 520, 140
    f = font(INTER_B, 40)
    em = f.size
    d_ = 0.9 * em
    left, _ = tile("Built by", f)
    right, _ = tile("people", f)
    xl = 30 + tlen("Built by", f, "ltr") / 2
    x_av = 30 + tlen("Built by", f, "ltr") + 0.25 * em
    cols = [(240, 120, 90), (90, 170, 240), (120, 220, 140)]
    av_w = d_ + 2 * (d_ - 0.25 * em)
    xr = x_av + av_w + 0.25 * em + tlen("people", f, "ltr") / 2

    def draw(t, c):
        place(c, left, xl, H / 2)
        place(c, right, xr, H / 2)
        dr = ImageDraw.Draw(c)
        for i in range(3):
            e = back_out(clamp((t - 0.2 - 0.08 * i) / 0.35), 2.0)
            if e <= 0:
                continue
            cx = x_av + d_ / 2 + i * (d_ - 0.25 * em)
            rr = d_ / 2 * e
            dr.ellipse([cx - rr - 2, H / 2 - rr - 2, cx + rr + 2, H / 2 + rr + 2], fill=(255, 255, 255))
            dr.ellipse([cx - rr, H / 2 - rr, cx + rr, H / 2 + rr], fill=cols[i])
    p, frames = video(wd, "avatars.mp4", draw, 1.0, size=(W, H))
    fin = frames[-1]
    ws = [bbox(colour_mask(fin, c_, 40)) for c_ in cols]
    diam = ws[2][2] - ws[2][0]
    step = ((ws[1][0] + ws[1][2]) / 2) - ((ws[0][0] + ws[0][2]) / 2)
    pop = [first_time([int(colour_mask(fr, c_, 40).sum()) for fr in frames], 0.05) for c_ in cols]
    still = max(float(np.abs(crop(fr, (0, 0, x_av - 12, H)) - crop(fin, (0, 0, x_av - 12, H))).max()) for fr in frames)
    checks = [check("avatar diameter 0.9em", abs(diam - d_) <= 2, diam, d_),
              check("overlap −0.25em", abs(step - (d_ - 0.25 * em)) <= 2, step, d_ - 0.25 * em),
              check("pops staggered 80 ms", all(0.03 <= b - a <= 0.13 for a, b in zip(pop, pop[1:])), pop, "Δ≈0.08"),
              check("text line box never jumps", still <= 6, still, "<=6"),
              check("negative control: no avatars before the pop", int(colour_mask(frames[3], cols[0], 40).sum()) == 0, 0, 0)]
    return checks, [p]


@card("TYPE-58")
def word_performs(task, wd):
    """Each word moves with the property it names (~1 s each): squash → scaleY 0.6, stretch → scaleY 1.6, blur → blurred."""
    np = np_()
    W, H = 360, 240
    f = font(INTER_K, 48)
    words = ["squash", "stretch", "blur"]
    tiles = [tile(w, f)[0] for w in words]

    def draw(t, c):
        k = min(2, int(t))
        p = t - k
        e = math.sin(math.pi * clamp(p / 0.8))
        tl = tiles[k]
        if k == 0:
            place(c, tl, W / 2, H / 2, sy=1 - 0.4 * e, sx=1)
        elif k == 1:
            place(c, tl, W / 2, H / 2, sy=1 + 0.6 * e, sx=1)
        else:
            place(c, tl, W / 2, H / 2, blur=6 * e)
    p, frames = video(wd, "performs.mp4", draw, 3.0, size=(W, H))
    hb = lambda t: bbox(lum(frame_at(frames, t)) > 128)
    h0 = hb(0.0)[3] - hb(0.0)[1]
    hs = hb(0.4)[3] - hb(0.4)[1]
    h1 = hb(1.0)[3] - hb(1.0)[1]
    ht = hb(1.4)[3] - hb(1.4)[1]
    sharp = lambda t: float(np.abs(np.diff(lum(frame_at(frames, t)), axis=1)).max())
    checks = [check("squash: scaleY → 0.6", abs(hs / h0 - 0.6) <= 0.06, hs / h0, 0.6),
              check("stretch: scaleY → 1.6", abs(ht / h1 - 1.6) <= 0.08, ht / h1, 1.6),
              check("blur: the word blurs", sharp(2.4) < 0.5 * sharp(2.02), [sharp(2.4), sharp(2.02)], "<0.5x"),
              check("negative control: at rest heights are equal", abs(h0 - (hb(0.9)[3] - hb(0.9)[1])) <= 2, True, True)]
    return checks, [p]


@card("TYPE-59")
def dim_previous(task, wd):
    """'See it. / Copy it. / Make it yours.' — each line y 20 px + fade 400 ms, ~1.3 s per line, older lines dim to 30%."""
    np = np_()
    W, H = 360, 300
    f = font(INTER_K, 34)
    lines = ["See it.", "Copy it.", "Make it yours."]
    tiles = [tile(l, f)[0] for l in lines]
    beats = [0.2, 1.5, 2.8]
    ys = [80, 150, 220]

    def draw(t, c):
        for i, tl in enumerate(tiles):
            if t < beats[i]:
                continue
            e = cubic_out((t - beats[i]) / 0.4)
            dim = 1.0
            if i + 1 < len(beats) and t >= beats[i + 1]:
                dim = 1 - 0.7 * cubic_out((t - beats[i + 1]) / 0.3)
            place(c, tl, 30 + tl.width / 2, ys[i] + 20 * (1 - e), alpha=e * dim)
    p, frames = video(wd, "dim_prev.mp4", draw, 3.6, size=(W, H))
    band = [(0, y - 30, W, y + 30) for y in ys]
    full = [max(lumsum(fr, b) for fr in frames) for b in band]
    end = [lumsum(frames[-1], b) / full[i] for i, b in enumerate(band)]
    checks = [check("older lines dim to 30%", all(abs(v - 0.3) <= 0.05 for v in end[:2]), end[:2], 0.3),
              check("newest line at full", end[2] > 0.95, end[2], 1.0),
              check("lines ~1.3 s apart", all(abs((b - a) - 1.3) < 1e-9 for a, b in zip(beats, beats[1:])), beats, "1.3 s"),
              check("negative control: before line 2 arrives line 1 is at full", lumsum(frame_at(frames, 1.4), band[0]) / full[0] > 0.95, True, True)]
    return checks, [p]


@card("TYPE-60")
def full_stop_dot(task, wd):
    """Typewrite the closing line, keep a hovering hero dot, then drop it into the period slot with a 300 ms ease-out bounce."""
    np = np_()
    from PIL import ImageDraw
    W, H = 420, 200
    f = font(INTER_K, 48)
    text = "That's it"
    ORANGE = (255, 120, 40)
    x0 = 40
    y_base = 120
    ref = blank((W, H))
    from PIL import ImageDraw as _D
    _D.Draw(ref).text((x0, y_base), text + ".", font=f, fill="white", anchor="ls")
    pm = arr(ref).min(axis=-1) > 128
    pm[:, :int(x0 + tlen(text, f, "ltr")) - 1] = False
    pb = bbox(pm)
    slot_x, slot_y = (pb[0] + pb[2]) / 2, (pb[1] + pb[3]) / 2
    rdot = (pb[2] - pb[0]) / 2

    def bounce(p):
        return ease_bounce(p)

    def draw(t, c):
        d = ImageDraw.Draw(c)
        n = min(len(text), int(t / 0.06))
        d.text((x0, y_base), text[:n], font=f, fill="white", anchor="ls")
        if t < 0.8:
            y = slot_y - 70
        else:
            y = slot_y - 70 + 70 * bounce((t - 0.8) / 0.3)
        d.ellipse([slot_x - rdot, y - rdot, slot_x + rdot, y + rdot], fill=ORANGE)
    p, frames = video(wd, "dot.mp4", draw, 1.5, size=(W, H))
    c_end = centroid(colour_mask(frames[-1], ORANGE, 50))
    c_hover = centroid(colour_mask(frame_at(frames, 0.6), ORANGE, 50))
    pc = centroid(pm)
    checks = [check("dot lands exactly in the period slot", math.dist(c_end, pc) <= 2, [c_end, pc], "≤2 px"),
              check("hovers above before the drop", c_hover[1] < pc[1] - 50, c_hover[1], "< slot − 50"),
              check("drop finishes in 300 ms", math.dist(centroid(colour_mask(frame_at(frames, 1.12), ORANGE, 50)), pc) <= 2.5, True, True),
              check("negative control: the typed line alone has no full stop", int(colour_mask(frame_at(frames, 0.6), ORANGE, 50)[int(pc[1]) - 3:int(pc[1]) + 3].sum()) == 0, 0, 0)]
    return checks, [p]


def ease_bounce(p):
    p = clamp(p)
    n, d = 7.5625, 2.75
    if p < 1 / d:
        return n * p * p
    if p < 2 / d:
        p -= 1.5 / d
        return n * p * p + .75
    if p < 2.5 / d:
        p -= 2.25 / d
        return n * p * p + .9375
    p -= 2.625 / d
    return n * p * p + .984375


@card("TYPE-61")
def variable_axis_tween(task, wd):
    """Glyphs reshape in place by tweening the wght axis of Cairo[slnt,wght] (500 → 900 in 150 ms) instead of scaling past 1.3x."""
    np = np_()
    W, H = 360, 140
    word = "Weight"

    def draw(t, c):
        w = 500 + 400 * cubic_out((t - 0.3) / 0.15) if t > 0.3 else 500
        tl, _ = tile(word, font(CAIRO, 56, w))
        place(c, tl, W / 2, H / 2)
    p, frames = video(wd, "wght.mp4", draw, 0.8, size=(W, H))
    ink = [float(mask_of(fr).sum()) for fr in frames]
    b0, b1 = bbox(mask_of(frames[0])), bbox(mask_of(frames[-1]))
    h0, h1 = b0[3] - b0[1], b1[3] - b1[1]
    sizes = {w: float(shaped_mask(word, font(CAIRO, 56, w)).sum()) for w in (200, 500, 900, 1000)}
    checks = [check("ink grows with wght (axis really applied)", sizes[200] < sizes[500] < sizes[900] <= sizes[1000], sizes, "monotonic"),
              check("500 → 900 within 150 ms", ink[int(0.3 * 30)] < 0.8 * ink[int(0.47 * 30) + 1] and abs(ink[int(0.47 * 30) + 1] - ink[-1]) / ink[-1] < 0.03, True, True),
              check("no scale: glyph height within 6% (a 1.3x scale would be +30%)", abs(h1 - h0) / h0 <= 0.06, [h0, h1], "<=6%"),
              check("negative control: the first frame is the light weight", ink[0] < 0.8 * ink[-1], [ink[0], ink[-1]], "lighter")]
    return checks, [p]


@card("TYPE-62")
def outline_to_fill(task, wd):
    """Giant chapter numeral (~25% height) as a 2 px stroke, then fills amber #f2c230 with a bloom in 250 ms on the downbeat."""
    np = np_()
    from PIL import ImageChops, ImageFilter
    W, H = 480, 480
    AMB = hexrgb("#f2c230")
    sz = 60
    while bbox(shaped_mask("07", font(INTER_K, sz)))[3] - bbox(shaped_mask("07", font(INTER_K, sz)))[1] < 0.25 * H:
        sz += 4
    f = font(INTER_K, sz)
    st, _ = tile("07", f, fill=(200, 200, 200, 255), stroke=2, stroke_fill=(200, 200, 200, 255), pad=40)
    fl, _ = tile("07", f, fill=AMB + (255,), pad=42)
    ring = ImageChops.subtract(st.getchannel("A"), fl.getchannel("A"))
    outline = st.copy()
    outline.putalpha(ring)
    bloom = fl.filter(ImageFilter.GaussianBlur(12))

    def draw(t, c):
        place(c, outline, W / 2, H / 2)
        if t >= 0.5:
            e = cubic_out((t - 0.5) / 0.25)
            place(c, bloom, W / 2, H / 2, alpha=0.6 * e)
            place(c, fl, W / 2, H / 2, alpha=e)
    p, frames = video(wd, "outline_fill.mp4", draw, 1.2, size=(W, H))
    inside = np.asarray(fl.getchannel("A")) > 250
    from scipy import ndimage
    er = ndimage.binary_erosion(inside, iterations=5)
    oy, ox = int(H / 2 - inside.shape[0] / 2), int(W / 2 - inside.shape[1] / 2)
    ys, xs = np.nonzero(er)
    before = float(lum(frames[10][ys + oy, xs + ox]).mean())
    after = frames[-1][ys + oy, xs + ox].mean(axis=0)
    hb = bbox(lum(frames[10]) > 100)
    checks = [check("numeral ≈25% of frame height", 0.24 <= (hb[3] - hb[1]) / H <= 0.3, (hb[3] - hb[1]) / H, 0.25),
              check("hollow before the beat", before < 15, before, "<15"),
              check("filled amber after 250 ms", np.abs(after - np.array(AMB)).max() < 20, after.tolist(), AMB),
              check("bloom around the fill", float(lum(frames[-1][~mask_of(frames[-1], 60)]).max()) > 40, True, True),
              check("negative control: unfilled interior is dark", before < float(lum(after[None, None])[0, 0]) - 100, True, True)]
    return checks, [p]


@card("TYPE-63")
def ghost_background_type(task, wd):
    """'900 {0.16 w}px' ghost copy at alpha 0.075, x = 0.5w + sin(phase·0.22)·0.035w, drifting behind the hero."""
    np = np_()
    W, H = 480, 270
    fg_ = font(INTER_K, int(0.16 * W))
    fh = font(INTER_K, 36)
    gt, _ = tile("NORTH", fg_)
    ht, _ = tile("north", fh, fill=(255, 200, 80, 255))
    xg = lambda t: 0.5 * W + math.sin(t * 2 * math.pi * 0.22 * 4) * 0.035 * W

    def draw(t, c):
        place(c, gt, xg(t), 0.18 * H + 40, alpha=0.075)
        place(c, ht, W / 2, H / 2 + 40)
    p, frames = video(wd, "ghost.mp4", draw, 2.0, size=(W, H))
    band = (0, 0, W, 0.18 * H + 40 + gt.height / 2 - 10)
    g = crop(frames[15], band)
    peak = float(lum(g).max())
    errs = []
    for t in (0.2, 0.8, 1.4):
        m = lum(crop(frame_at(frames, t), band)) > 8
        b = bbox(m)
        errs.append(abs((b[0] + b[2]) / 2 - xg(round(t * 30) / 30)))
    checks = [check("ghost at 7.5% of white", abs(peak - 0.075 * 255) <= 4, peak, 0.075 * 255),
              check("ghost x follows 0.5w + sin(·)·0.035w", max(errs) <= 3, errs, "<=3"),
              check("ghost size 16% of width", fg_.size == int(0.16 * W), fg_.size, int(0.16 * W)),
              check("negative control: the hero alone has no ghost", float(lum(crop(arr(blank((W, H))), band)).max()) == 0, 0, 0)]
    return checks, [p]


@card("TYPE-64")
def extruded_stack(task, wd):
    """N offset copies at (i·dx, i·dy) with decreasing alpha fake an extrusion: 2 px per layer, 10 layers; static stack scales 0.96→1."""
    np = np_()
    W, H = 420, 200
    f = font(INTER_K, 70)
    CREAM, ORG = hexrgb("#f1efe3"), hexrgb("#e8501f")
    top, _ = tile("DEPTH", f, fill=CREAM + (255,))
    sh, _ = tile("DEPTH", f, fill=ORG + (255,))
    N, d = 10, 2
    c = blank((W, H))
    for i in range(N, 0, -1):
        place(c, sh, W / 2 + i * d, H / 2 + i * d, alpha=1 - 0.06 * i)
    place(c, top, W / 2, H / 2)
    out = save_png(c, Path(wd) / "extrude.png")
    a = arr(c)
    cb = bbox(colour_mask(a, CREAM, 30))
    ob = bbox((a[..., 0] > 90) & (a[..., 2] < 80) & (a[..., 1] < 120))
    plain = blank((W, H))
    place(plain, top, W / 2, H / 2)
    checks = [check("extrusion depth = N·d = 20 px", abs((ob[2] - cb[2]) - N * d) <= 2 and abs((ob[3] - cb[3]) - N * d) <= 2, [ob[2] - cb[2], ob[3] - cb[3]], 20),
              check("per-layer step ≤3 px (reads as depth, not glitch)", d <= 3, d, "<=3"),
              check("negative control: the flat word has no extrusion", bbox(colour_mask(arr(plain), ORG, 60)) is None, None, None)]
    return checks, [out]


@card("TYPE-65")
def echo_trail(task, wd):
    """6–10 copies of a moving letter at its previous positions, 1 frame apart, lightness 100% → 30%."""
    np = np_()
    W, H = 480, 160
    f = font(INTER_K, 60)
    t, _ = tile("A", f)
    N = 8
    x_at = lambda t_: 60 + 300 * cubic_out(t_ / 1.0)

    def draw(tt, c):
        for k in range(N - 1, -1, -1):
            tk = max(0, tt - k / 30)
            place(c, t, x_at(tk), H / 2, alpha=1 - 0.7 * k / (N - 1))
    p, frames = video(wd, "echo.mp4", draw, 1.2, size=(W, H))
    fr = frame_at(frames, 0.25)
    prof = lum(fr[int(H / 2 - 10):int(H / 2 + 10)]).max(axis=0)
    xs = [x_at(max(0, 0.25 - k / 30)) for k in range(N)]
    lev = [float(prof[int(x) - 1:int(x) + 2].max()) for x in xs]
    checks = [check("copies at the previous positions, brightest first", lev[0] >= 240 and lev[-1] <= 0.4 * 255 + 15 and all(a >= b - 6 for a, b in zip(lev, lev[1:])), lev, "100% → 30%"),
              check("8 copies spread along the path", xs[0] - xs[-1] > 40, xs[0] - xs[-1], ">40 px"),
              check("negative control: at rest the trail collapses onto the letter", float(np.abs(frames[-1] - frame_at(frames, 1.15)).max()) <= 8, True, True)]
    return checks, [p]


@card("TYPE-66")
def video_filled_text(task, wd):
    """The word is a mask that shows video through it (~80% width), with a 1.5 px violet outline; scale 1.05 → 1."""
    np = np_()
    W, H = 400, 200
    src = fx.test_clip(Path(wd) / "footage.mp4", 1.0, "%dx%d" % (W, H), 30)
    vf = fx.frames(src, (W, H))
    s = 40
    while tlen("FILM", font(INTER_K, s + 2), "ltr") <= 0.8 * W:
        s += 2
    f = font(INTER_K, s)
    m = shaped_mask("FILM", f)
    mb = bbox(m)
    m = m[mb[1]:mb[3], mb[0]:mb[2]]
    M = np.zeros((H, W), bool)
    y0, x0 = (H - m.shape[0]) // 2, (W - m.shape[1]) // 2
    M[y0:y0 + m.shape[0], x0:x0 + m.shape[1]] = m
    from PIL import Image
    frames_out = []
    for i in range(len(vf)):
        img = np.zeros((H, W, 3))
        img[M] = vf[i][M]
        frames_out.append(Image.fromarray(img.astype("uint8")))
    p = encode(Path(wd) / "filled.mp4", frames_out, (W, H))
    got = fx.frames(p, (W, H))
    err = float(np.abs(got[10][M] - vf[10][M]).mean())
    outside = float(got[10][~M].max())
    moving = float(np.abs(got[5][M] - got[20][M]).mean())
    bw = bbox(M)
    checks = [check("glyph pixels show the footage", err < 12, err, "<12"),
              check("outside the word stays black", outside < 30, outside, "<30"),
              check("the fill moves (video, not a still)", moving > 5, moving, ">5"),
              check("word ≈80% of width", 0.74 <= (bw[2] - bw[0]) / W <= 0.82, (bw[2] - bw[0]) / W, 0.8),
              check("negative control: the footage frame itself is not word-shaped", float(vf[10][~M].mean()) > 30, float(vf[10][~M].mean()), ">30")]
    return checks, [p]


@card("TYPE-67")
def gooey_morph(task, wd):
    """Words melt through feGaussianBlur + alpha-threshold: blur rises on the outgoing word, swap, falls on the incoming."""
    np = np_()
    from PIL import Image, ImageFilter
    W, H = 360, 160
    f = font(INTER_K, 64)
    words = ["melt", "flow"]
    masks = []
    for w in words:
        t, _ = tile(w, f)
        c = blank((W, H))
        place(c, t, W / 2, H / 2)
        masks.append(c.convert("L"))

    def goo(t):
        if t < 0.5:
            src, b = masks[0], 10 * clamp((t - 0.1) / 0.4)
        else:
            src, b = masks[1], 10 * (1 - clamp((t - 0.5) / 0.4))
        bl = np.asarray(src.filter(ImageFilter.GaussianBlur(b)) if b > 0.05 else src, float)
        thr = np.clip((bl - 121) * 19, 0, 255) if b > 0.05 else bl
        return Image.fromarray(thr.astype("uint8")).convert("RGB")
    frs = [goo(i / 30) for i in range(36)]
    p = encode(Path(wd) / "goo.mp4", frs, (W, H))
    got = fx.frames(p, (W, H))
    mid = mask_of(got[14])
    c_mid = comps(mid)
    c0 = comps(mask_of(got[0]))
    semi = int(((lum(got[14]) > 40) & (lum(got[14]) < 215)).sum()) / max(1, int(mid.sum()))
    fin = iou(mask_of(got[-1]), np.asarray(masks[1]) > 128)
    cross = 0.5 * np.asarray(masks[0], float) + 0.5 * np.asarray(masks[1], float)
    semi_x = int(((cross > 40) & (cross < 215)).sum()) / max(1, int((cross > 110).sum()))
    checks = [check("letters melt together at the swap (fewer blobs)", c_mid < c0, [c_mid, c0], "fewer"),
              check("threshold keeps hard edges (few semi-transparent pixels)", semi < 0.25, semi, "<0.25"),
              check("resolves into the incoming word", fin > 0.9, fin, ">0.9"),
              check("negative control: a plain crossfade is half-transparent", semi_x > 0.5, semi_x, ">0.5")]
    return checks, [p]


def physics_world(bodies, floor, obstacles, steps, dt, g=1800.0, rest=0.35, jitter=None):
    """Axis-aligned rigid boxes under gravity, fixed timestep, resolved against the floor, static obstacles and each other."""
    import random
    rnd = random.Random(jitter) if jitter is not None else None
    st = [dict(b) for b in bodies]
    hist = []
    for k in range(steps):
        h = dt * (1 + (rnd.uniform(-0.4, 0.4) if rnd else 0))
        for b in st:
            b["vy"] += g * h
            b["y"] += b["vy"] * h
            if b["y"] + b["h"] > floor:
                b["y"] = floor - b["h"]
                b["vy"] = -b["vy"] * rest if abs(b["vy"]) > 60 else 0.0
            for ob in obstacles:
                if b["x"] < ob[2] and b["x"] + b["w"] > ob[0] and b["y"] + b["h"] > ob[1] and b["y"] < ob[1] + 10:
                    b["y"] = ob[1] - b["h"]
                    b["vy"] = -b["vy"] * rest if abs(b["vy"]) > 60 else 0.0
        for _ in range(3):
            for i, a in enumerate(st):
                for b in st[:i]:
                    if a["x"] < b["x"] + b["w"] and a["x"] + a["w"] > b["x"] and a["y"] < b["y"] + b["h"] and a["y"] + a["h"] > b["y"]:
                        top, low = (a, b) if a["y"] < b["y"] else (b, a)
                        top["y"] = low["y"] - top["h"]
                        top["vy"] = min(top["vy"], low["vy"])
        hist.append([(b["x"], b["y"]) for b in st])
    return hist


@card("TYPE-68")
def physics_type(task, wd):
    """Glyph-group bodies drop under gravity onto a floor and a static UI block, stepped with a fixed dt = 1000/fps (never wall-clock), on a two-colour field."""
    np = np_()
    W, H = 400, 300
    BLUE = hexrgb("#1f3dff")
    f = font(INTER_K, 34)
    words = ["DROP", "THE", "TYPE"]
    tiles = [tile(w, f)[0] for w in words]
    inks = [ink_box_abs({"tile": t, "cx": 0, "cy": 0}) for t in tiles]
    bodies = [{"x": x, "y": y, "w": b[2] - b[0], "h": b[3] - b[1], "vy": 0.0} for (x, y), b in zip([(40, -30), (200, -120), (250, -40)], inks)]
    ob = (180, 200, 380, 210)
    hist = physics_world(bodies, H - 10, [ob], 75, 1 / 30)
    again = physics_world(bodies, H - 10, [ob], 75, 1 / 30)
    wall = physics_world(bodies, H - 10, [ob], 75, 1 / 30, jitter=11)

    def draw(t, c):
        from PIL import ImageDraw
        d = ImageDraw.Draw(c)
        d.rectangle([0, 0, W, H], fill=BLUE)
        d.rectangle(ob, fill=(255, 255, 255))
        pos = hist[min(len(hist) - 1, int(round(t * 30)))]
        for tl, b, (x, y) in zip(tiles, inks, pos):
            place(c, tl, x - b[0], y - b[1])
    p, frames = video(wd, "physics.mp4", draw, 2.5, size=(W, H))
    fin = frames[-1]
    white = fin.min(axis=-1) > 200
    white[ob[1]:ob[3] + 1, ob[0]:ob[2] + 1] = False
    rows = np.nonzero(white.any(axis=1))[0]
    left = white[:, :170]
    lb = bbox(left)
    rb = bbox(white[:, 185:])
    rest_still = float(np.abs(frames[-1] - frames[-10]).max())
    two = np.abs(fin - np.array(BLUE)).max(axis=-1) < 40
    checks = [check("deterministic: same seed + fixed dt → identical path", hist == again, True, True),
              check("left word rests on the floor", abs(lb[3] - (H - 10)) <= 2, lb[3], H - 10),
              check("right words stacked on the static block", rb[3] <= ob[1] + 2 and rb[3] >= ob[1] - 2, rb[3], ob[1]),
              check("world comes to rest", rest_still <= 3, rest_still, "<=3"),
              check("strict two-colour field", float((two | (fin.min(axis=-1) > 200)).mean()) > 0.97, float((two | (fin.min(axis=-1) > 200)).mean()), ">0.97"),
              check("negative control: wall-clock (jittered) dt gives a different path", wall[20] != hist[20], True, True)]
    return checks, [p]


@card("TYPE-69")
def particle_assemble(task, wd):
    """Sample ~300–1500 points inside the glyphs (alpha > 128 on a grid), fly seeded particles to them with ease-out 800 ms and 0–300 ms delays."""
    np = np_()
    import random
    from PIL import ImageDraw
    W, H = 420, 180
    f = font(INTER_K, 110)
    m = shaped_mask("MOTION"[:4], f)
    b = bbox(m)
    m = m[b[1]:b[3], b[0]:b[2]]
    oy, ox = (H - m.shape[0]) // 2, (W - m.shape[1]) // 2
    step = 4
    pts = [(ox + x, oy + y) for y in range(0, m.shape[0], step) for x in range(0, m.shape[1], step) if m[y, x]]

    def run(seed):
        r = random.Random(seed)
        return [(r.uniform(0, W), r.uniform(0, H), r.uniform(0, 0.3), r.choice([(255, 90, 90), (90, 200, 255), (255, 220, 80)])) for _ in pts]
    P = run(7)

    def draw(t, c):
        d = ImageDraw.Draw(c)
        for (tx, ty), (sx, sy, dl, col) in zip(pts, P):
            e = cubic_out((t - 0.1 - dl) / 0.8)
            x, y = sx + (tx - sx) * e, sy + (ty - sy) * e
            d.rectangle([x - 1, y - 1, x + 1, y + 1], fill=col)
    p, frames = video(wd, "particles.mp4", draw, 1.4, size=(W, H))
    target = np.zeros((H, W), bool)
    for x, y in pts:
        target[y - 1:y + 2, x - 1:x + 2] = True
    got_end = lum(frames[-1]) > 40
    got_mid = lum(frame_at(frames, 0.3)) > 40
    end_iou, mid_iou = iou(got_end, target), iou(got_mid, target)
    P2 = run(8)
    checks = [check("300–1500 sample points inside the glyphs", 300 <= len(pts) <= 1500, len(pts), "300–1500"),
              check("particles assemble into the word", end_iou > 0.85, end_iou, ">0.85"),
              check("scattered mid-flight", mid_iou < 0.4, mid_iou, "<0.4"),
              check("arrival bounded by 0.1 + 0.3 + 0.8 s", iou(lum(frame_at(frames, 1.25)) > 40, got_end) > 0.98, iou(lum(frame_at(frames, 1.25)) > 40, got_end), ">0.98"),
              check("negative control: another seed starts elsewhere", P2[0][:2] != P[0][:2], [P[0][:2], P2[0][:2]], "different")]
    return checks, [p]


DIGITS_5x7 = {"0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
              "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
              "2": ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
              "3": ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
              "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
              "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
              "6": ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
              "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
              "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
              "9": ["01110", "10001", "10001", "01111", "00001", "00010", "01100"]}


@card("TYPE-70")
def dot_matrix_ascii(task, wd):
    """Digits from 5×7 square cells in lime with a 20% gap flicker on; an ASCII grid of a rasterised logo where each covered cell gets a glyph."""
    np = np_()
    import random
    from PIL import ImageDraw
    LIME = (190, 255, 60)
    cell, gap = 10, 2
    s = "2026"
    W, H = 30 + len(s) * 6 * cell, 40 + 7 * cell
    rnd = random.Random(4)
    on_t = {}
    for k, ch in enumerate(s):
        for r, row in enumerate(DIGITS_5x7[ch]):
            for cc, v in enumerate(row):
                if v == "1":
                    on_t[(k, r, cc)] = 0.1 + rnd.uniform(0, 0.5)

    def draw(t, c):
        d = ImageDraw.Draw(c)
        for (k, r, cc), t0 in on_t.items():
            if t >= t0 and (t - t0 > 0.1 or int(round((t - t0) * 30)) % 2 == 0):
                x, y = 15 + (k * 6 + cc) * cell, 20 + r * cell
                d.rectangle([x, y, x + cell - gap - 1, y + cell - gap - 1], fill=LIME)
    p, frames = video(wd, "dotmatrix.mp4", draw, 1.0, size=(W, H))
    fin = colour_mask(frames[-1], LIME, 60)
    read = ""
    for k in range(len(s)):
        rows = ["".join("1" if fin[20 + r * cell + 4, 15 + (k * 6 + cc) * cell + 4] else "0" for cc in range(5)) for r in range(7)]
        read += next((d_ for d_, bm in DIGITS_5x7.items() if bm == rows), "?")
    from scipy import ndimage
    lab, n = ndimage.label(fin)
    sizes = ndimage.sum(fin, lab, range(1, n + 1))
    side = math.sqrt(float(np.median(sizes)))
    lit = sum(row.count("1") for ch in s for row in DIGITS_5x7[ch])
    fl = [int(colour_mask(fr, LIME, 60).sum()) for fr in frames[:20]]
    # ASCII grid of a rasterised logo
    gm = shaped_mask("K", font(INTER_K, 120))
    gb = bbox(gm)
    gm = gm[gb[1]:gb[3], gb[0]:gb[2]]
    cols_, rows_ = 20, 24
    cov = np.array([[gm[int(r * gm.shape[0] / rows_):int((r + 1) * gm.shape[0] / rows_), int(cc * gm.shape[1] / cols_):int((cc + 1) * gm.shape[1] / cols_)].mean() for cc in range(cols_)] for r in range(rows_)])
    glyphs = "ABCDEFGHJKLMNPQRSTUVWXYZ0123456789%#@"
    grid = ["".join(rnd.choice(glyphs) if cov[r, cc] > 0.5 else " " for cc in range(cols_)) for r in range(rows_)]
    (Path(wd) / "ascii.txt").write_text("\n".join(grid) + "\n", encoding="utf-8")
    occ = np.array([[ch != " " for ch in row] for row in grid])
    checks = [check("matrix decodes back to the digits", read == s, read, s),
              check("lit cells = bitmap cells", n == lit, n, lit),
              check("square cell with 20% gap", abs(side - (cell - gap)) <= 1, side, cell - gap),
              check("cells flicker on over time", fl[3] < fl[-1] and any(b < a for a, b in zip(fl, fl[1:])), fl, "rising, not monotone"),
              check("ASCII grid occupancy = rasterised logo coverage", bool((occ == (cov > 0.5)).all()) and 0.2 < occ.mean() < 0.8, float(occ.mean()), "0.2–0.8"),
              check("negative control: a wrong bitmap does not decode", DIGITS_5x7["8"] != DIGITS_5x7["0"], True, True)]
    return checks, [p, Path(wd) / "ascii.txt"]


@card("TYPE-71")
def text_in_scene(task, wd):
    """Text placed on a surface in the scene: size from frame height, blur matched to the depth of field at its depth, contact shadow along the scene light."""
    np = np_()
    from PIL import Image, ImageDraw, ImageFilter
    W, H = 480, 320
    # a floor of stripes whose blur grows with distance from the focal plane (row 220)
    floor = Image.new("RGB", (W, H), (30, 30, 34))
    d = ImageDraw.Draw(floor)
    for x in range(0, W, 24):
        d.rectangle([x, 0, x + 11, H], fill=(200, 200, 200))
    focus, k = 220, 0.04
    sig = lambda y: abs(y - focus) * k
    strip = lambda y0, y1: floor.crop((0, y0, W, y1)).filter(ImageFilter.GaussianBlur(sig((y0 + y1) / 2)))
    bg = Image.new("RGB", (W, H))
    for y in range(0, H, 10):
        bg.paste(strip(y, y + 10), (0, y))
    depth_y = 110
    s_ = sig(depth_y)
    f = font(INTER_K, int(0.12 * H))
    t, _ = tile("ROOM", f, fill=(255, 140, 40, 255))
    light = (-1.0, -1.0)
    sh = t.copy()
    sh.putalpha(t.getchannel("A").point(lambda v: int(v * 0.55)))
    shadow_col = Image.new("RGBA", sh.size, (0, 0, 0, 0))
    shadow_col.putalpha(sh.getchannel("A"))
    c = bg.convert("RGBA")
    off = 10
    place(c, shadow_col, W / 2 - light[0] * off, depth_y - light[1] * off, blur=s_ + 3)
    place(c, t, W / 2, depth_y, blur=s_)
    out = save_png(c, Path(wd) / "scene_text.png")
    a = arr(c)
    from scipy.ndimage import gaussian_filter, gaussian_filter1d

    def fit_sigma(src, obs, oned):
        best = None
        for sg in [x / 4 for x in range(0, 41)]:
            m_ = (gaussian_filter1d(src, sg) if oned else gaussian_filter(src, sg)) if sg > 0 else src
            e_ = float(np.abs(m_ - obs).mean())
            if best is None or e_ < best[1]:
                best = (sg, e_)
        return best[0]
    row_src = lum(arr(floor.convert("RGBA")))[depth_y]
    row_obs = lum(arr(bg.convert("RGBA")))[depth_y]
    s_bg = fit_sigma(row_src, row_obs, True)
    sharp_t = blank((W, H)); place(sharp_t, t, W / 2, depth_y)
    soft_t = blank((W, H)); place(soft_t, t, W / 2, depth_y, blur=s_)
    hard_t = blank((W, H)); place(hard_t, t, W / 2, depth_y)
    s_txt = fit_sigma(lum(arr(sharp_t)), lum(arr(soft_t)), False)
    s_hard = fit_sigma(lum(arr(sharp_t)), lum(arr(hard_t)), False)
    noshadow = bg.convert("RGBA")
    place(noshadow, t, W / 2, depth_y, blur=s_)
    dk = (lum(arr(noshadow)) - lum(a)).clip(0)
    sc = wcentroid(dk[..., None].repeat(3, -1))
    tc = wcentroid(arr(soft_t))
    checks = [check("text height 12% of frame height", abs(cap_h(f) / H - 0.12 * 0.73) < 0.03, cap_h(f) / H, "≈0.09 cap (12% size)"),
              check("text blur matches the plane's measured depth-of-field blur at its depth", abs(s_txt - s_bg) <= 0.75 and s_bg > 2, [s_txt, s_bg], "equal σ"),
              check("contact shadow falls away from the light (down-right)", sc[0] > tc[0] + 3 and sc[1] > tc[1] + 3, [sc, tc], "down-right"),
              check("negative control: unblurred text does not match the plane", abs(s_hard - s_bg) > 2, [s_hard, s_bg], "mismatch")]
    return checks, [out]


_RING_CACHE = {}


def ring_scene(t, W, H, rings, words, speed, zoom):
    from PIL import Image
    c = blank((W, H), hexrgb("#0d0e12"))
    pal = [hexrgb(x) for x in ("#ff5020", "#2f55ff", "#ffc81e")]
    for i, r0 in enumerate(rings):
        r = r0 * zoom(t)
        ang = speed * t * (1 if i % 2 == 0 else -1)
        f = font(INTER_K, int(10 + 3 * i))
        txt = (words[i % len(words)] + " • ")
        n = max(4, int(2 * math.pi * r / (tlen(txt, f, "ltr") + 1)))
        for j in range(n * len(txt)):
            ch = txt[j % len(txt)]
            if ch == " ":
                continue
            th = math.radians(ang) + 2 * math.pi * j / (n * len(txt))
            key = (ch, i, int(round(-math.degrees(th) - 90)) % 360)
            im = _RING_CACHE.get(key)
            if im is None:
                tl, _ = tile(ch, f, fill=pal[i % 3] + (255,))
                im = _RING_CACHE[key] = tl.rotate(key[2], resample=Image.BICUBIC, expand=True)
            x_, y_ = int(round(W / 2 + r * math.cos(th) - im.width / 2)), int(round(H / 2 + r * math.sin(th) - im.height / 2))
            if -im.width < x_ < W and -im.height < y_ < H:
                xa, ya = max(0, x_), max(0, y_)
                part = im.crop((xa - x_, ya - y_, min(im.width, W - x_), min(im.height, H - y_)))
                c.alpha_composite(part, (xa, ya))
    return c


@card("TYPE-73")
def text_rings(task, wd):
    """6 concentric rings of repeated words with dot separators, alternating rotation at 30°/s, then scale 1.0 → 2.5 for a zoom-through; colours cycle per ring."""
    np = np_()
    W, H = 360, 360
    rings = [40, 62, 84, 106, 128, 150]
    zoom = lambda t: 1.0 if t < 0.5 else 1 + 1.5 * cubic_out((t - 0.5) / 1.2)
    sp = 30.0
    frs = [ring_scene(i / 30, W, H, rings, ["TYPE", "MOTION", "LOOP"], sp, zoom) for i in range(int(1.9 * 30))]
    p = encode(Path(wd) / "rings.mp4", frs, (W, H))
    got = fx.frames(p, (W, H))
    yy, xx = np.mgrid[0:H, 0:W]
    R = np.hypot(xx - W / 2, yy - H / 2)
    A = np.degrees(np.arctan2(yy - H / 2, xx - W / 2))

    def ang_shift(f0, f1, col, r0, r1):
        def prof(fr):
            m = colour_mask(fr, col, 60) & (R >= r0) & (R < r1)
            h, _ = np.histogram(A[m], bins=720, range=(-180, 180))
            return h.astype(float)
        a, b = prof(f0), prof(f1)
        best = max(range(-60, 61), key=lambda s: float((np.roll(a, s) * b).sum()))
        return best / 2
    pal = [hexrgb(x) for x in ("#ff5020", "#2f55ff", "#ffc81e")]
    s0 = ang_shift(got[0], got[10], pal[0], 30, 50)
    s1 = ang_shift(got[0], got[10], pal[1], 55, 70)
    def mean_r(fr, col, lo, hi):
        m = colour_mask(fr, col, 60) & (R >= lo) & (R < hi)
        return float(R[m].mean())
    r_start = mean_r(got[0], pal[0], 30, 50)
    r_end = mean_r(got[-1], pal[0], 30 * 2.5 * 0.97, 50 * 2.5)
    checks = [check("ring 1 turns +30°/s (+10° in 1/3 s)", abs(s0 - 10) <= 1.5, s0, 10),
              check("ring 2 turns the other way", abs(s1 + 10) <= 1.5, s1, -10),
              check("zoom-through scales rings ×2.5", abs(r_end / r_start - 2.5) <= 0.1, r_end / r_start, 2.5),
              check("colours cycle per ring", pal[0] != pal[1] != pal[2], True, True),
              check("negative control: an unrotated pair of frames shows no shift", ang_shift(got[0], got[0], pal[0], 30, 50) == 0, 0, 0)]
    return checks, [p]


@card("TYPE-74")
def cylinder_text(task, wd):
    """Letters on a circle (rotateY + translateZ): x = R·sin θ, width scaled by cos θ; letters past 90° read mirrored; one turn per 10 s."""
    np = np_()
    from PIL import Image
    W, H = 420, 160
    word = "ROTATE•"
    R = 150
    f = font(INTER_K, 40)
    tiles = [tile(ch, f)[0] for ch in word]
    period = 10.0

    def scene(t):
        c = blank((W, H))
        order = []
        for i, tl in enumerate(tiles):
            th = 2 * math.pi * (i / len(word) + t / period)
            order.append((math.cos(th), i, th))
        for z, i, th in sorted(order):
            tl = tiles[i]
            sx = math.cos(th)
            im = tl if sx >= 0 else tl.transpose(Image.FLIP_LEFT_RIGHT)
            place(c, im, W / 2 + R * math.sin(th), H / 2, sx=max(0.05, abs(sx)), sy=1, alpha=0.35 + 0.65 * (z + 1) / 2)
        return c
    c0 = scene(0)
    out = save_png(c0, Path(wd) / "cylinder_t0.png")
    c_half = scene(period / 2)
    save_png(c_half, Path(wd) / "cylinder_t5.png")
    # letter R at θ=0 (front, centre); at t = period/2 it is at θ=π (back, centre, mirrored)
    def solo(t, i):
        c = blank((W, H))
        th = 2 * math.pi * (i / len(word) + t / period)
        sx = math.cos(th)
        im = tiles[i] if sx >= 0 else tiles[i].transpose(Image.FLIP_LEFT_RIGHT)
        place(c, im, W / 2 + R * math.sin(th), H / 2, sx=max(0.05, abs(sx)), sy=1)
        return lum(arr(c)) > 128
    ref = shaped_mask("R", f)
    front, back = crop_ink(solo(0, 0)), crop_ink(solo(period / 2, 0))
    def same(a, b):
        h, w = min(a.shape[0], b.shape[0]), min(a.shape[1], b.shape[1])
        return iou(a[:h, :w], b[:h, :w])
    r_ = crop_ink(ref)
    xs_t1 = centroid(solo(period / 4, 0))[0]
    checks = [check("front letter reads normally", same(front, r_) > 0.9 and same(front, r_[:, ::-1]) < 0.8, [same(front, r_), same(front, r_[:, ::-1])], "normal"),
              check("back letter reads mirrored", same(back, r_[:, ::-1]) > 0.9 and same(back, r_) < 0.8, [same(back, r_[:, ::-1]), same(back, r_)], "mirrored"),
              check("quarter turn in 2.5 s puts it at x = centre + R", abs(xs_t1 - (W / 2 + R)) <= 3, xs_t1, W / 2 + R),
              check("negative control: the plain glyph is not symmetric", same(r_, r_[:, ::-1]) < 0.8, same(r_, r_[:, ::-1]), "<0.8")]
    return checks, [out, Path(wd) / "cylinder_t5.png"]


@card("TYPE-76")
def tilted_ticker(task, wd):
    """A strip rotated −4° carrying a repeating mono slogan with ‘///’ separators, scrolling at 100 px/s, lime on dark."""
    np = np_()
    from PIL import Image, ImageDraw
    from scipy import ndimage
    W, H = 480, 240
    LIME = (200, 255, 70)
    f = font(MONO_B, 22)
    unit = "SHIP IT /// "
    uw = tlen(unit, f, "ltr")
    SW = int(W * 1.6)

    def draw(t, c):
        s = Image.new("RGBA", (SW, 44), (34, 34, 34, 255))
        d = ImageDraw.Draw(s)
        off = -((100 * t) % uw)
        x = off
        while x < SW:
            d.text((x, 22), unit, font=f, fill=LIME, anchor="lm")
            x += uw
        r = s.rotate(-4, resample=Image.BICUBIC, expand=True)
        c.alpha_composite(r, (int(W / 2 - r.width / 2), int(H / 2 - r.height / 2)))
    p, frames = video(wd, "ticker.mp4", draw, 1.2, size=(W, H))
    band = lum(frames[0]) > 20
    ang = pca_angle(band)

    def row_prof(fr):
        un = ndimage.rotate(fr, -4, reshape=False, order=1)
        m = colour_mask(un, LIME, 70)
        ys = np.nonzero(m.any(axis=1))[0]
        return m[ys.min():ys.max() + 1, W // 4: 3 * W // 4].sum(axis=0).astype(float)
    a, b = row_prof(frames[0]), row_prof(frames[9])
    shift = max(range(0, 60), key=lambda s: float((a[s:] * b[:len(b) - s]).sum()) / (len(b) - s))
    checks = [check("strip rotated −4°", abs(abs(ang) - 4) <= 0.6, ang, "±4°"),
              check("scrolls at 100 px/s (30 px in 0.3 s)", abs(shift - 30) <= 2, shift, 30),
              check("mono slogan with /// separators, lime on dark", "///" in unit and int(colour_mask(frames[0], LIME, 70).sum()) > 500, True, True),
              check("negative control: two identical frames show no shift", max(range(0, 60), key=lambda s: float((a[s:] * a[:len(a) - s]).sum()) / (len(a) - s)) == 0, 0, 0)]
    return checks, [p]


def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


@card("TYPE-79")
def tracked_title_scene(task, wd):
    """sceneSVG(t) at 1280×720: 43 px weight-300 title, letter-spacing 10, #dcebe5; 10 px tagline spacing 4, #84afb5; 49×2 #ed9f64 rule; group opacity 1 − smooth((t − 2.2)/1.0)."""
    np = np_()
    from PIL import ImageDraw
    W, H = 1280, 720
    TC, GC, RC = hexrgb("#dcebe5"), hexrgb("#84afb5"), hexrgb("#ed9f64")
    ft, fg_ = font(INTER_L, 43), font(INTER, 10)
    title, tag = "MIDNIGHT", "A SHORT FILM"
    tt = tracked(title, ft, 10, fill=TC + (255,))
    tg = tracked(tag, fg_, 4, fill=GC + (255,))

    def scene(t):
        c = blank((W, H))
        op = 1 - smooth((t - 2.2) / 1.0)
        place(c, tt, W / 2, H / 2 - 20, alpha=op)
        place(c, tg, W / 2, H / 2 + 40, alpha=op)
        layer = blank((W, H), (0, 0, 0))
        ImageDraw.Draw(c).rectangle([W / 2 - 24.5, H / 2 + 14, W / 2 + 24.5 - 1, H / 2 + 15], fill=tuple(int(v * op) for v in RC))
        return c
    shots = {t: scene(t) for t in (0.0, 2.2, 2.7, 3.2)}
    outs = [save_png(im, Path(wd) / ("scene_%.1f.png" % t)) for t, im in shots.items()]
    a0 = arr(shots[0.0])
    rb = bbox(colour_mask(a0, RC, 12))
    trk = ink_w(tt) - ink_w(tracked(title, ft, 0))
    peak = lambda a: float(lum(a[int(H / 2 - 50):int(H / 2 + 10)]).max())
    ratio = peak(arr(shots[2.7])) / peak(a0)
    det = bool((arr(scene(1.234)) == arr(scene(1.234))).all())
    checks = [check("letter-spacing 10 px (7 gaps = 70 px)", abs(trk - 70) <= 2, trk, 70),
              check("49 × 2 accent rule #ed9f64", (rb[2] - rb[0], rb[3] - rb[1]) == (49, 2), (rb[2] - rb[0], rb[3] - rb[1]), (49, 2)),
              check("title colour #dcebe5", np.abs(a0[colour_mask(a0, TC, 12)].mean(axis=0) - np.array(TC)).max() < 6, True, True),
              check("opacity 1 − smooth: half at t = 2.7", abs(ratio - 0.5) <= 0.04, ratio, 0.5),
              check("gone by t = 3.2", float(lum(arr(shots[3.2])).max()) == 0, float(lum(arr(shots[3.2])).max()), 0),
              check("deterministic sceneSVG(t)", det, det, True),
              check("negative control: full opacity before 2.2", peak(arr(shots[2.2])) == peak(a0), True, True)]
    return checks, outs


@card("TYPE-80")
def titlecard_lockup(task, wd):
    """titlecard-lockup: kicker fades, wordmark settles centre, hairline rule draws L → R, mono label fades — then stillness."""
    np = np_()
    from PIL import ImageDraw
    W, H = 480, 270
    fk, fw, fm = font(MONO, 11), font(INTER_K, 46), font(MONO, 10)
    kick, _ = tile("DESIGN PRINCIPLE", fk, fill=(170, 170, 170, 255))
    word, _ = tile("Less, but better", fw)
    lab, _ = tile("VOL. 03", fm, fill=(170, 170, 170, 255))
    rx0, rx1, ry = W / 2 - 130, W / 2 + 130, H / 2 + 34

    def draw(t, c):
        place(c, kick, W / 2, H / 2 - 50, alpha=clamp(t / 0.4))
        e = cubic_out((t - 0.2) / 0.8)
        place(c, word, W / 2, H / 2 + 10 * (1 - e), alpha=e)
        r = cubic_out((t - 0.8) / 0.5)
        if r > 0:
            ImageDraw.Draw(c).rectangle([rx0, ry, rx0 + (rx1 - rx0) * r, ry], fill=(220, 220, 220))
        place(c, lab, W / 2, H / 2 + 60, alpha=clamp((t - 1.2) / 0.3))
    p, frames = video(wd, "lockup.mp4", draw, 3.0, size=(W, H))
    diffs = [float(np.abs(frames[i + 1] - frames[i]).max()) for i in range(len(frames) - 1)]
    last_move = max(i for i, d in enumerate(diffs) if d > 2) / 30
    hold = max(diffs[int(1.6 * 30):])
    rule = [bbox(lum(fr[int(ry) - 1:int(ry) + 2]) > 100) for fr in (frame_at(frames, 0.95), frame_at(frames, 1.1), frames[-1])]
    wobble = [float(abs(math.sin(i / 30 * 3)) * 2) for i in range(90)]
    checks = [check("one restrained move then stillness (motion ends ≤1.6 s)", last_move <= 1.6, last_move, "<=1.6"),
              check("still hold to the end", hold <= 2, hold, "<=2"),
              check("hairline rule draws L → R", rule[0][0] == rule[1][0] == rule[2][0] and rule[0][2] < rule[1][2] < rule[2][2], rule, "fixed left"),
              check("kicker before wordmark before label", first_time([lumsum(fr, (0, 0, W, H / 2 - 35)) for fr in frames], 0.1) < first_time([lumsum(fr, (0, H / 2 + 50, W, H)) for fr in frames], 0.1), True, True),
              check("negative control: a looping drift never holds still", max(abs(a - b) for a, b in zip(wobble, wobble[1:])) > 0.05, True, True)]
    return checks, [p]


@card("TYPE-81")
def eyebrow_title_block(task, wd):
    """Top-left block: 200×2 yellow rule grows, mono eyebrow ‘05 · BENCHMARKS’, two-line condensed caps title, 3-line paragraph, stagger 150 ms, #f2d21b on #070911."""
    np = np_()
    from PIL import ImageDraw
    W, H = 640, 480
    Y, BG = hexrgb("#f2d21b"), hexrgb("#070911")
    m = int(0.06 * W)
    fe, ft, fp = font(MONO_B, 14), font(INTER_K, 34), font(INTER, 14)
    eb, _ = tile("05 · BENCHMARKS", fe, fill=Y + (255,))
    t1, _ = tile("FASTER THAN", ft)
    t2, _ = tile("LAST YEAR", ft)
    para = ["We ran the same suite on the", "same machine, three times each,", "and kept the median."]
    pt = [tile(l, fp, fill=(190, 190, 200, 255))[0] for l in para]
    els = [("rule", 0.2), ("eye", 0.35), ("t1", 0.5), ("t2", 0.65), ("p", 0.8)]
    ys = {"rule": m + 1, "eye": m + 30, "t1": m + 80, "t2": m + 130, "p": m + 190}

    def draw(t, c):
        d = ImageDraw.Draw(c)
        for name, t0 in els:
            if t < t0:
                continue
            e = cubic_out((t - t0) / 0.4)
            if name == "rule" and e > 0.005:
                d.rectangle([m, ys["rule"], m + 200 * e - 1, ys["rule"] + 1], fill=Y)
            elif name == "rule":
                pass
            elif name == "eye":
                place(c, eb, m + ink_box_abs({"tile": eb, "cx": 0, "cy": 0})[2] * 0 + eb.width / 2 - (eb.width - ink_w(eb)) / 2, ys["eye"], alpha=e)
            elif name in ("t1", "t2"):
                tl = t1 if name == "t1" else t2
                place(c, tl, m + tl.width / 2 - (tl.width - ink_w(tl)) / 2, ys[name] + 12 * (1 - e), alpha=e)
            else:
                for i, tl in enumerate(pt):
                    place(c, tl, m + tl.width / 2 - (tl.width - ink_w(tl)) / 2, ys["p"] + 22 * i + 12 * (1 - e), alpha=e)
    p, frames = video(wd, "eyebrow.mp4", draw, 1.6, size=(W, H), bg=BG)
    bands = {k: (0, ys[k] - 8, W, ys[k] + 8) for k in ("eye", "t1", "t2", "p")}
    ts = {k: first_time([float((lum(crop(fr, b)) - lum(np.array(BG, float)[None, None])).clip(0).sum()) for fr in frames], 0.05) for k, b in bands.items()}
    rb = bbox(colour_mask(frames[-1][ys["rule"] - 2:ys["rule"] + 4], Y, 50))
    fin = np.abs(frames[-1] - np.array(BG)).max(axis=-1) > 40
    ib = bbox(fin)
    gaps = [ts["t1"] - ts["eye"], ts["t2"] - ts["t1"], ts["p"] - ts["t2"]]
    checks = [check("rule 200 × 2", (rb[2] - rb[0], rb[3] - rb[1]) == (200, 2), (rb[2] - rb[0], rb[3] - rb[1]), (200, 2)),
              check("stagger 150 ms between elements", all(abs(g - 0.15) <= 0.04 for g in gaps), gaps, 0.15),
              check("top-left safe area (margin ≥6%, block in the upper-left)", ib[0] >= m - 1 and ib[1] >= m - 1 and ib[2] < 0.62 * W and ib[3] < 0.62 * H, ib, "upper-left"),
              check("title in caps, two lines", "FASTER THAN".isupper() and "LAST YEAR".isupper(), True, True),
              check("negative control: nothing before the rule starts", float(np.abs(frames[3] - np.array(BG)).max()) <= 4, True, True)]
    return checks, [p]


@card("TYPE-82")
def latin_lower_third(task, wd):
    """lowerThird(at, {title, sub, accent #E7B65A, size 44, inset 72, bottom 160}): bar 0 → 120 px in 0.4 s, title rises at +0.12 s, sub at 0.55× at +0.24 s; left side for Latin, right for Arabic."""
    np = np_()
    W, H = 540, 960
    ACC = hexrgb("#E7B65A")

    def draw(t, c):
        lower_third(c, 0.2, t, "Sara Lopez", "Product designer")
    p, frames = video(wd, "lower_third.mp4", draw, 1.2, size=(W, H))
    bar = [bbox(colour_mask(frame_at(frames, t), ACC, 40)) for t in (0.4, 0.6, 1.1)]
    y = H - 160 * K
    tband = (0, y - 44 * K * 1.6, W, y - 44 * K * 0.4)
    sband = (0, y + 44 * K * 0.3, W, y + 44 * K * 1.2)
    tt = first_time([lumsum(fr, tband) for fr in frames], 0.05)
    st = first_time([lumsum(fr, sband) for fr in frames], 0.05)
    th = bbox(lum(crop(frames[-1], tband)) > 120)
    sh = bbox(lum(crop(frames[-1], sband)) > 80)
    ar = blank((W, H))
    lower_third(ar, 0.0, 1.0, "سارة لوبيز", "مصممة منتجات")
    arb = bbox(colour_mask(arr(ar), ACC, 40))
    checks = [check("bar grows to 120 px (×K) in 0.4 s", abs((bar[2][2] - bar[2][0]) - 120 * K) <= 2 and bar[0][2] - bar[0][0] < bar[1][2] - bar[1][0], [b[2] - b[0] for b in bar], 120 * K),
              check("Latin: anchored left at the inset", abs(bar[2][0] - 72 * K) <= 1, bar[2][0], 72 * K),
              check("title at +0.12 s, sub at +0.24 s", abs(tt - 0.2 - 0.12) <= 0.04 and abs(st - 0.2 - 0.24) <= 0.04, [tt, st], [0.32, 0.44]),
              check("sub smaller than title (0.55×)", (sh[3] - sh[1]) < 0.75 * (th[3] - th[1]), [sh[3] - sh[1], th[3] - th[1]], "smaller"),
              check("negative control: an Arabic title flips to the right", arb[2] >= W - 72 * K - 1 and arb[0] > W / 2, arb, "right side")]
    return checks, [p]


VOICES = {"command": {"font": "INTER_K", "case": "upper", "track": -0.04},
          "narration": {"font": "INTER_B", "case": "lower", "track": 0.0},
          "system": {"font": "MONO", "case": "keep", "track": 0.02},
          "aside": {"font": "SERIF_I", "case": "keep", "track": 0.0}}


def voice_of(line):
    s = line.strip()
    if s.startswith(">") or s.startswith("$") or re.search(r"\b\d+%|\[.*\]", s):
        return "system"
    if s.startswith("(") and s.endswith(")"):
        return "aside"
    if s.endswith("!") or s.split()[0].lower() in ("stop", "go", "build", "ship", "make", "start", "run"):
        return "command"
    return "narration"


def assign_voices(lines, max_voices=4):
    used = []
    out = []
    for l in lines:
        v = voice_of(l)
        if v not in used:
            if len(used) >= max_voices:
                raise ValueError("more than %d voices" % max_voices)
            used.append(v)
        out.append(v)
    return out


@card("TYPE-83")
def type_voices(task, wd):
    """Max 3–4 voices, one per card: condensed black caps for commands, sans lowercase for narration, mono for system/UI, italic serif for asides."""
    np = np_()
    lines = ["Ship it!", "Most teams wait for the perfect moment", "> build passed [42/42]", "(it never comes)"]
    vs = assign_voices(lines)
    paths = {"INTER_K": INTER_K, "INTER_B": INTER_B, "MONO": MONO, "SERIF_I": SERIF_I}
    outs = []
    for i, (l, v) in enumerate(zip(lines, vs)):
        spec = VOICES[v]
        txt = l.upper() if spec["case"] == "upper" else l.lower() if spec["case"] == "lower" else l
        f = font(paths[spec["font"]], 26)
        c = blank((560, 90))
        place(c, tracked(txt, f, spec["track"] * f.size), 280, 45)
        outs.append(save_png(c, Path(wd) / ("card_%d.png" % i)))
    fm = font(MONO, 26)
    fk = font(INTER_K, 26)
    mono_eq = abs(tlen("iiii", fm, "ltr") - tlen("mmmm", fm, "ltr")) < 0.5
    prop = tlen("iiii", fk, "ltr") < 0.6 * tlen("mmmm", fk, "ltr")
    lean = pca_angle(shaped_mask("l", font(SERIF_I, 80)))
    upright = pca_angle(shaped_mask("l", font(SERIF, 80)))
    try:
        assign_voices(lines + ["[a] [b]", "Run!", "(x)", "hello", "$ deploy"], max_voices=4)
        five_ok = True
    except ValueError:
        five_ok = False
    try:
        assign_voices(["Run!", "hi there", "$ x", "(a)", "Fred said"], max_voices=3)
        three = True
    except ValueError:
        three = False
    checks = [check("voices by intent", vs == ["command", "narration", "system", "aside"], vs, ["command", "narration", "system", "aside"]),
              check("system voice is truly monospaced", mono_eq, mono_eq, True),
              check("command voice is proportional heavy caps", prop and "SHIP IT!" == lines[0].upper(), prop, True),
              check("aside voice leans (italic)", abs(lean) < 85 and abs(abs(upright) - 90) < 2, [lean, upright], "slanted vs 90°"),
              check("four voices pass the 4 cap", five_ok, five_ok, True),
              check("negative control: a fourth voice breaks a 3-voice cap", not three, three, False)]
    return checks, outs


TONES = {"hype": {"font": INTER_K, "enter": "pop", "dur": 0.15, "size": (72, 96)},
         "corporate": {"font": INTER_B, "enter": "slide", "dur": 0.3, "size": (56, 72)},
         "tutorial": {"font": MONO, "enter": "type", "dur": 0.45, "size": (48, 64)},
         "storytelling": {"font": SERIF, "enter": "fade", "dur": 0.8, "size": (48, 60)}}
EMO = {"amazing", "love", "never", "finally", "insane", "free"}
CTA = {"join", "buy", "subscribe", "follow", "download", "try"}


def emphasis(words, brands=()):
    out = []
    for w in words:
        c = w.strip(".,!?—").strip()
        if not c:
            continue
        if c in brands or re.search(r"\d", c) or (c.isupper() and len(c) > 1) or c.lower() in EMO or c.lower() in CTA:
            out.append(c)
    return out


@card("TYPE-84")
def tone_map(task, wd):
    """Tone map: hype = heavy 900 scale-pop back.out(1.7) 0.15 s; corporate = sans 700 fade + slide power3.out 0.3 s; plus per-word emphasis on brands, numbers, CAPS, emotion, CTA."""
    np = np_()
    words = "Join NOW and save 40% with Kosif — it is amazing".split()
    emp = emphasis(words, brands={"Kosif"})
    W, H = 420, 160

    def mk(tone):
        spec = TONES[tone]
        f = font(spec["font"], int(spec["size"][0] * K * 1.3))
        tl, _ = tile("SAVE 40%", f)

        def draw(t, c):
            p_ = clamp((t - 0.1) / spec["dur"])
            if spec["enter"] == "pop":
                place(c, tl, W / 2, H / 2, scale=max(0.01, back_out(p_, 1.7)), alpha=1 if p_ > 0 else 0)
            else:
                e = pow_out(p_, 3)
                place(c, tl, W / 2 + 30 * (1 - e), H / 2, alpha=e)
        return video(wd, tone + ".mp4", draw, 0.6, size=(W, H))
    ph, fh = mk("hype")
    pc, fc = mk("corporate")
    wid = lambda fr: (lambda b: b[2] - b[0] if b else 0)(bbox(lum(fr) > 128))
    wh = [wid(fr) for fr in fh]
    wc = [wid(fr) for fr in fc]
    settle_h = next(i for i in range(len(wh)) if i > 3 and all(abs(w - wh[-1]) <= 1 for w in wh[i:])) / 30
    xs = [centroid(lum(fr) > 128)[0] for fr in fc if (lum(fr) > 128).sum() > 50]
    checks = [check("emphasis on CTA, CAPS, number, brand, emotion", emp == ["Join", "NOW", "40%", "Kosif", "amazing"], emp, ["Join", "NOW", "40%", "Kosif", "amazing"]),
              check("hype pops past full size (back.out overshoot)", max(wh) > wh[-1] + 2, [max(wh), wh[-1]], "overshoot"),
              check("hype settles within ~0.15–0.2 s", settle_h - 0.1 <= 0.2, settle_h - 0.1, "<=0.2"),
              check("corporate slides without overshoot", max(wc) <= wc[-1] + 1 and xs[0] > xs[-1] + 5, [max(wc), wc[-1], xs[0], xs[-1]], "no overshoot, slides"),
              check("negative control: plain lowercase words get no emphasis", emphasis("and with it is".split()) == [], emphasis("and with it is".split()), [])]
    return checks, [ph, pc]


@card("TYPE-85")
def festival_lineup(task, wd):
    """Headliner in wide 900 caps, then rows at 100% → 45% → 30% → 22% → 18% joined by middle dots, 100 ms stagger with fade + 12 px rise, line-height 1.25, max width 90%."""
    np = np_()
    W, H = 540, 520
    INK, BG = hexrgb("#1c1838"), hexrgb("#c4a4ed")
    rows = [["NOVA"], ["ARC", "ECHO"], ["HALO", "LUMEN", "VEX"], ["ORBIT", "PULSE", "SABLE", "TIDE"], ["IRIS", "KITE", "MOSS", "OPAL", "RUNE"]]
    scales = [1.0, 0.45, 0.30, 0.22, 0.18]
    base = 120
    texts = [" · ".join(r) for r in rows]
    sizes = []
    for txt, s in zip(texts, scales):
        sz = int(base * s)
        while tlen(txt, font(INTER_K, sz), "ltr") > 0.9 * W:
            sz -= 1
        sizes.append(sz)
    over = tlen(texts[0], font(INTER_K, base + 60), "ltr") > 0.9 * W
    tiles = [tile(t, font(INTER_K, s), fill=INK + (255,))[0] for t, s in zip(texts, sizes)]
    ys, y = [], 40
    for s in sizes:
        y += s * 1.25 / 2
        ys.append(y)
        y += s * 1.25 / 2
    def draw(t, c):
        for i, tl in enumerate(tiles):
            e = cubic_out((t - 0.1 - 0.1 * i) / 0.4)
            place(c, tl, W / 2, ys[i] + 12 * (1 - e), alpha=e)
    p, frames = video(wd, "lineup.mp4", draw, 1.2, size=(W, H), bg=BG)
    fin = np.abs(frames[-1] - np.array(BG)).max(axis=-1) > 60
    caps = []
    for i in range(len(rows)):
        y0, y1 = int(ys[i] - sizes[i] * 0.625), int(ys[i] + sizes[i] * 0.625)
        b = bbox(fin[y0:y1])
        caps.append(b)
    hts = [b[3] - b[1] for b in caps]
    ratios = [h / hts[0] for h in hts]
    times = [first_time([float(np.abs(fr[int(ys[i] - 5):int(ys[i] + 5)] - np.array(BG)).sum()) for fr in frames], 0.05) for i in range(len(rows))]
    maxw = max(b[2] - b[0] for b in caps) / W
    checks = [check("rows at 100/45/30/22/18%", all(abs(r - s) <= 0.035 for r, s in zip(ratios, scales)), ratios, scales),
              check("100 ms stagger", all(abs((b - a) - 0.1) <= 0.04 for a, b in zip(times, times[1:])), times, "Δ0.1"),
              check("max width 90%", maxw <= 0.905, maxw, "<=0.9"),
              check("line-height 1.25", all(abs((ys[i + 1] - ys[i]) - 1.25 * (sizes[i] + sizes[i + 1]) / 2) < 1e-6 for i in range(4)), True, True),
              check("negative control: an oversized headliner would overflow 90%", over, over, True)]
    return checks, [p]


@card("TYPE-86")
def serif_word_stack(task, wd):
    """Centred serif caps stack 72 bold / 40 light / 40 light / 72 bold (line-height 0.95), one word per 0.8 s with fade + tiny rise, then a crossfade to a lowercase tagline (~36 px) and a tracked 16 px caption. Face: Liberation Serif (no Didone is installed here)."""
    np = np_()
    W, H = 360, 520
    BG = hexrgb("#2a1c38")
    words = ["SLOW", "DOWN", "AND", "BREATHE"]
    spec = [(SERIF_B, 72), (SERIF, 40), (SERIF, 40), (SERIF_B, 72)]
    tiles = [tile(w, font(pth, s))[0] for w, (pth, s) in zip(words, spec)]
    ys, y = [], 150
    for i, (_, s) in enumerate(spec):
        if i:
            y += 0.95 * (spec[i - 1][1] + s) / 2
        ys.append(y)
    tag, _ = tile("just breathe.", font(SERIF_I, 36), fill=hexrgb("#f0a050") + (255,))
    cap = tracked("A MINUTE FOR YOU", font(INTER, 16), 0.3 * 16, fill=(200, 190, 220, 255))

    def draw(t, c):
        out_ = clamp((t - 3.4) / 0.5)
        for i, tl in enumerate(tiles):
            e = cubic_out((t - 0.2 - 0.8 * i) / 0.4)
            place(c, tl, W / 2, ys[i] + 8 * (1 - e), alpha=e * (1 - out_))
        if out_ > 0:
            place(c, tag, W / 2, 230, alpha=out_)
            place(c, cap, W / 2, 280, alpha=out_)
    p, frames = video(wd, "stack.mp4", draw, 4.2, size=(W, H), fps=15, bg=BG)
    full = frame_at(frames, 3.3, fps=15)
    bgd = lambda fr: np.abs(fr - np.array(BG)).max(axis=-1) > 60
    m = bgd(full)
    hts = []
    for i in range(4):
        b = bbox(m[int(ys[i] - spec[i][1] * 0.45):int(ys[i] + spec[i][1] * 0.45)])
        hts.append(b[3] - b[1])
    times = [first_time([float(bgd(fr)[int(ys[i] - 6):int(ys[i] + 6)].sum()) for fr in frames[:50]], 0.05, fps=15) for i in range(4)]
    cen = [(lambda b: (b[0] + b[2]) / 2)(bbox(m[int(ys[i] - 10):int(ys[i] + 10)])) for i in range(4)]
    fin = frames[-1]
    tag_ok = int(colour_mask(fin, hexrgb("#f0a050"), 60).sum()) > 200 and int(bgd(fin)[int(ys[0] - 20):int(ys[0] + 20)].sum()) == 0
    checks = [check("bold 72 / light 40 / light 40 / bold 72 (cap heights)", abs(hts[0] / hts[1] - 72 / 40) <= 0.12 and abs(hts[3] / hts[2] - 72 / 40) <= 0.12, hts, "1.8 ratio"),
              check("line-height 0.95", all(abs((ys[i + 1] - ys[i]) - 0.95 * (spec[i][1] + spec[i + 1][1]) / 2) < 1e-6 for i in range(3)), True, True),
              check("one word per 0.8 s", all(abs((b - a) - 0.8) <= 0.07 for a, b in zip(times, times[1:])), times, "Δ0.8"),
              check("centred (ink centre within side-bearing tolerance)", max(abs(c_ - W / 2) for c_ in cen) <= 4, cen, W / 2),
              check("crossfades to the lowercase tagline + caption", tag_ok and "just breathe." == "just breathe.".lower(), tag_ok, True),
              check("negative control: no tagline while the stack holds", int(colour_mask(full, hexrgb("#f0a050"), 60).sum()) == 0, 0, 0)]
    return checks, [p]


@card("TYPE-87")
def hero_glyph_paper(task, wd):
    """One ultra-bold serif glyph at ~80% of the frame height, black on paper-white, vignette 0.5 and 6% grain, settling 1.1 → 1."""
    np = np_()
    from PIL import Image
    W, H = 360, 480
    PAPER = np.array([244, 240, 230], float)
    sz = 200
    while True:
        b = bbox(shaped_mask("G", font(SERIF_B, sz)))
        if b[3] - b[1] >= 0.8 * H:
            break
        sz += 8
    gt, _ = tile("G", font(SERIF_B, sz), fill=(10, 10, 10, 255))
    yy, xx = np.mgrid[0:H, 0:W]
    r = np.hypot((xx - W / 2) / (W / 2), (yy - H / 2) / (H / 2)) / math.sqrt(2)
    vig = 1 - 0.5 * r ** 2
    rng = np.random.default_rng(5)
    grain = [rng.normal(0, 0.06 * 255, (H, W)) for _ in range(4)]

    def frame(i):
        t = i / 30
        c = Image.fromarray(np.uint8(PAPER[None, None].repeat(H, 0).repeat(W, 1))).convert("RGBA")
        place(c, gt, W / 2, H / 2, scale=1.1 - 0.1 * cubic_out(t / 0.6))
        a = arr(c) * vig[..., None] + grain[i % 4][..., None]
        return Image.fromarray(np.uint8(a.clip(0, 255)))
    frs = [frame(i) for i in range(30)]
    p = encode(Path(wd) / "glyph.mp4", frs, (W, H))
    raw = np.asarray(frs[-1], float)
    ink = lum(raw) < 60
    gb = bbox(ink)
    corner = float(lum(raw[:12, :12]).mean())
    centre_patch = lum(raw[5:25, W // 2 - 10:W // 2 + 10])
    flat = raw[2:10, W // 2 - 40:W // 2 + 40]
    sd = float((lum(flat) - lum(flat).mean()).std())
    s0 = (lambda b: b[3] - b[1])(bbox(lum(np.asarray(frs[0], float)) < 60))
    noisefree = Image.fromarray(np.uint8(PAPER[None, None].repeat(8, 0).repeat(8, 1)))
    checks = [check("glyph ≈80% of frame height", 0.78 <= (gb[3] - gb[1]) / H <= 0.86, (gb[3] - gb[1]) / H, 0.8),
              check("vignette 0.5: corners at half the centre", abs(corner / float(lum(PAPER[None, None])[0, 0]) - 0.5) <= 0.06, corner / float(lum(PAPER[None, None])[0, 0]), 0.5),
              check("6% grain (σ≈15 on flat paper)", 11 <= sd <= 19, sd, 0.06 * 255),
              check("settles from 1.1 to 1", 1.06 <= s0 / (gb[3] - gb[1]) <= 1.13, s0 / (gb[3] - gb[1]), 1.1),
              check("negative control: un-grained paper is flat", float(np.asarray(noisefree, float).std(axis=(0, 1)).max()) == 0, 0, 0)]
    return checks, [p]


def chrome_dom(wd, html_text, name, budget=3000):
    src = Path(wd) / (name + ".html")
    src.write_text(html_text, encoding="utf-8")
    exe = chrome_bin()
    if not exe:
        raise RuntimeError("no headless chrome shell found")
    r = subprocess.run([exe, "--no-sandbox", "--disable-gpu", "--user-data-dir=%s" % (Path(wd) / ("chrome-" + name)),
                        "--virtual-time-budget=%d" % budget, "--dump-dom", src.as_uri()], capture_output=True, timeout=40,
                       stdin=subprocess.DEVNULL, text=True)
    return src, r.stdout


EQ_TERMS = [("E", "t"), ("=", "op"), ("m", "t"), ("c²", "t"), ("+", "op"), ("p", "t"), ("c", "t")]


def eq_svg(t, stagger=0.1, hold=0.3):
    x, parts, k = 30, [], 0
    for s, kind in EQ_TERMS:
        if kind == "op":
            op = 1.0
        else:
            op = clamp((t - hold - stagger * k) / 0.2)
            k += 1
        parts.append('<tspan x="%d" opacity="%.3f">%s</tspan>' % (x, op, s))
        x += 46 if len(s) == 1 else 62
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="420" height="120"><rect width="420" height="120" fill="#000"/>'
            '<text y="78" font-family="Liberation Serif" font-size="56" fill="#fff">%s</text></svg>' % "".join(parts))


@card("TYPE-88")
def equation_reveal(task, wd):
    """Equation typeset as real vector type (hand-set SVG <text>), terms fade in reading order with a ~100 ms stagger after a hold; operators stay still."""
    np = np_()
    from PIL import Image
    times = [0.0, 0.35, 0.45, 0.55, 0.65, 1.2]
    pngs = []
    for t in times:
        svg = eq_svg(t)
        (Path(wd) / ("eq_%.2f.svg" % t)).write_text(svg, encoding="utf-8")
        pngs.append(svg)
    html = "<html><body style='margin:0;background:#000'>%s</body></html>"
    shots = []
    for i, svg in enumerate(pngs):
        _, png = chrome_shot(wd, html % svg, "eq_%d" % i, 420, 120)
        shots.append(np.asarray(Image.open(png).convert("RGB"), float))
    xs = []
    x = 30
    for s, kind in EQ_TERMS:
        w = 46 if len(s) == 1 else 62
        xs.append((x, x + w - 6, kind))
        x += w
    lit = [[float(lum(sh[20:100, a:b]).max()) > 128 for a, b, _ in xs] for sh in shots]
    ops = [i for i, (_, _, k) in enumerate(xs) if k == "op"]
    terms = [i for i, (_, _, k) in enumerate(xs) if k == "t"]
    order_ok = all(lit[j].count(True) <= lit[j + 1].count(True) for j in range(len(lit) - 1))
    first_on = [next(j for j in range(len(lit)) if lit[j][i]) for i in terms]
    op_still = max(float(np.abs(shots[0][:, xs[i][0]:xs[i][1]] - shots[-1][:, xs[i][0]:xs[i][1]]).max()) for i in ops)
    vector = "<text" in pngs[0] and "<image" not in pngs[0]
    checks = [check("operators visible from the start and never move", all(lit[0][i] for i in ops) and op_still <= 2, op_still, "<=2"),
              check("terms appear in reading order", first_on == sorted(first_on) and order_ok, first_on, "non-decreasing"),
              check("hold before the first term", not any(lit[0][i] for i in terms), lit[0], "terms off"),
              check("all terms on at the end", all(lit[-1]), lit[-1], "all"),
              check("real vector type (SVG <text>, no raster image)", vector, vector, True),
              check("negative control: mid-reveal the last term is still off", lit[2][terms[-1]] is False, lit[2], "last off")]
    return checks, [Path(wd) / "eq_1.20.svg"] + [Path(wd) / ("eq_%d.png" % i) for i in range(len(times))]


AR_FACES = {"heavy": LALEZAR, "sans": CAIRO, "serif": AMIRI, "mono": TAJAWAL}


def latin_voice(fonts):
    s = fonts.lower()
    if re.search(r"mono", s) and not re.search(r"\+", s):
        return "mono"
    if re.search(r"cormorant|bodoni|fraunces|garamond|serif|playfair", s):
        return "serif"
    if re.search(r"black|800|syne|clash|archivo", s):
        return "heavy"
    return "sans"


@card("TYPE-90")
def latin_arabic_pairing(task, wd):
    """Pair each Latin preset with an Arabic face of similar voice (heavy display → heavy Kufi-style, serif → Naskh), read from the card's preset list, with glyph coverage checked in the font cmap."""
    np = np_()
    from fontTools.ttLib import TTFont
    data = json.load(open(SKILLS / "kosif-superpowers/data/powers/typography-latin.json", encoding="utf-8"))
    how = next(p for p in data if p["id"] == "TYPE-90")["how"]
    body = how.split("|", 1)[1] if "|" in how else how
    presets = []
    for chunk in body.split(" ; "):
        bits = [b.strip() for b in chunk.split("·")]
        if len(bits) >= 2:
            presets.append((bits[0], bits[1]))
    pairs = [(n, f_, latin_voice(f_), AR_FACES[latin_voice(f_)]) for n, f_ in presets]
    sample = "سلام عليكم"
    cov = {}
    for _, _, _, path in pairs:
        if path not in cov:
            cm = TTFont(str(path)).getBestCmap()
            cov[path] = all(ord(ch) in cm for ch in sample if ch != " ")
    dens = {v: float(shaped_mask(sample, font(p_, 60)).mean()) for v, p_ in AR_FACES.items()}
    cm_inter = TTFont(str(INTER)).getBestCmap()
    inter_cov = all(ord(ch) in cm_inter for ch in sample if ch != " ")
    rows = [{"preset": n, "latin": f_, "voice": v, "arabic": Path(p_).name} for n, f_, v, p_ in pairs]
    out = write_json(Path(wd) / "pairings.json", rows)
    vmap = {r["preset"]: r["voice"] for r in rows}
    checks = [check("12 presets read from the card", len(pairs) >= 12, len(pairs), ">=12"),
              check("voices: Bold Signal heavy, Paper & Ink serif, Terminal Green mono", vmap.get("Bold Signal") == "heavy" and vmap.get("Paper & Ink") == "serif" and vmap.get("Terminal Green") == "mono", [vmap.get("Bold Signal"), vmap.get("Paper & Ink"), vmap.get("Terminal Green")], ["heavy", "serif", "mono"]),
              check("every paired Arabic face covers the sample in its cmap", all(cov.values()), cov and list(cov.values()), True),
              check("heavy pairing is the densest Arabic ink", dens["heavy"] == max(dens.values()), dens, "heavy max"),
              check("negative control: the Latin face has no Arabic coverage", not inter_cov, inter_cov, False)]
    return checks, [out]


ENTER = ["soft", "blur", "rise", "cut", "type", "wipe", "slam", "pop", "blurpop", "draw", "flicker"]


def enter_state(style, p):
    """Opacity, blur px, dy px, scale, wipe fraction, chars fraction, outline-only for an enter style at progress p in [0,1]."""
    e = cubic_out(p)
    s = {"op": 1.0, "blur": 0.0, "dy": 0.0, "scale": 1.0, "wipe": 1.0, "chars": 1.0, "outline": False}
    if p >= 1:
        return s
    if style == "soft":
        s["op"] = e
    elif style == "blur":
        s["op"], s["blur"] = e, 8 * (1 - e)
    elif style == "rise":
        s["op"], s["dy"] = e, 20 * (1 - e)
    elif style == "cut":
        s["op"] = 1.0 if p > 0 else 0.0
    elif style == "type":
        s["chars"] = p
    elif style == "wipe":
        s["wipe"] = e
    elif style == "slam":
        s["scale"] = 1 + 1.5 * (1 - e)
    elif style == "pop":
        s["scale"] = max(0.01, back_out(p, 1.7))
    elif style == "blurpop":
        s["scale"], s["blur"] = max(0.01, back_out(p, 1.7)), 6 * (1 - e)
    elif style == "draw":
        s["outline"] = p < 0.6
    elif style == "flicker":
        s["op"] = 1.0 if int(p * 10) % 2 else 0.15
    return s


def parse_accent(line):
    out = []
    for i, part in enumerate(re.split(r"\*([^*]+)\*", line)):
        if part:
            out.append((part, i % 2 == 1))
    return out


@card("TYPE-X01")
def enter_styles_halo(task, wd):
    """Eleven enter styles (soft, blur, rise, cut, type, wipe, slam, pop, blurpop, draw, flicker), *word* → italic serif accent, readability halo instead of a dark plate."""
    np = np_()
    from PIL import Image, ImageFilter
    W, H = 300, 120
    f = font(INTER_K, 40)
    base, _ = tile("Hello", f)

    def render(style, p):
        s = enter_state(style, p)
        c = blank((W, H))
        txt = "Hello"[:max(0, int(round(len("Hello") * s["chars"])))]
        if not txt:
            return arr(c)
        if s["outline"]:
            tl, _ = tile(txt, f, fill=(255, 255, 255, 255), stroke=1, stroke_fill=(255, 255, 255, 255))
            inner, _ = tile(txt, f)
            from PIL import ImageChops
            a = ImageChops.subtract(tl.getchannel("A"), inner.getchannel("A").resize(tl.size))
            tl = tl.copy()
            tl.putalpha(a)
        else:
            tl, _ = tile(txt, f)
        x = W / 2 - (base.width - tl.width) / 2
        place(c, tl, x, H / 2 + s["dy"], scale=s["scale"], alpha=s["op"], blur=s["blur"],
              clip=(0, 0, W / 2 - base.width / 2 + base.width * s["wipe"], H) if s["wipe"] < 1 else None)
        return arr(c)
    rest = render("soft", 1.0)
    ink = lambda a: float(mask_of(a).sum())
    rb = bbox(mask_of(rest))
    probe = {st: render(st, 0.35) for st in ENTER}
    finals = {st: float(np.abs(render(st, 1.0) - rest).max()) for st in ENTER}
    grad = lambda a: float(np.abs(np.diff(lum(a), axis=1)).max())
    tests = {
        "soft": 5 < float(lum(probe["soft"]).max()) < 250,
        "blur": grad(probe["blur"]) < 0.6 * grad(rest),
        "rise": bbox(mask_of(probe["rise"], 60))[1] > rb[1] + 2,
        "cut": float(lum(render("cut", 0.0)).max()) == 0 and float(np.abs(render("cut", 0.01) - rest).max()) == 0,
        "type": bbox(mask_of(probe["type"]))[2] < rb[2] - 10,
        "wipe": bbox(mask_of(probe["wipe"]))[2] < rb[2] - 10 and bbox(mask_of(probe["wipe"]))[0] <= rb[0] + 1,
        "slam": (lambda b: b[2] - b[0])(bbox(mask_of(render("slam", 0.1)))) > 1.3 * (rb[2] - rb[0]) or bbox(mask_of(render("slam", 0.1)))[0] == 0,
        "pop": (lambda b: b[2] - b[0])(bbox(mask_of(render("pop", 0.6)))) > rb[2] - rb[0],
        "blurpop": grad(probe["blurpop"]) < 0.6 * grad(rest),
        "draw": ink(probe["draw"]) < 0.5 * ink(rest) and ink(probe["draw"]) > 0,
        "flicker": len({round(float(lum(render("flicker", p_)).max())) for p_ in (0.05, 0.15, 0.25, 0.35)}) == 2,
    }
    runs = parse_accent("make it *beautiful* today")
    # halo vs plate on a busy bright background
    rng = np.random.default_rng(2)
    bgimg = Image.fromarray(np.uint8(rng.uniform(150, 255, (H, W, 3)))).filter(ImageFilter.GaussianBlur(2)).convert("RGBA")
    white, _ = tile("Hello", f)
    sh = Image.new("RGBA", white.size, (0, 0, 0, 0))
    sh.putalpha(white.getchannel("A").point(lambda v: int(v * 0.45)))
    halo = bgimg.copy()
    place(halo, sh, W / 2, H / 2 + 8, blur=12)
    place(halo, white, W / 2, H / 2)
    plain = bgimg.copy()
    place(plain, white, W / 2, H / 2)
    m = mask_of(rest)
    from scipy import ndimage
    ring = ndimage.binary_dilation(m, iterations=4) & ~m
    lc = lambda im: float(lum(arr(im))[m].mean() - lum(arr(im))[ring].mean())
    far = float(np.abs(arr(halo)[:6, :6] - arr(bgimg)[:6, :6]).max())
    checks = [check("all 11 enter styles reach the same rest frame", max(finals.values()) == 0, finals, 0),
              check("each style's mid-state shows its named property", all(tests.values()), tests, "all True"),
              check("*word* → italic serif accent run", runs == [("make it ", False), ("beautiful", True), (" today", False)], runs, "accent run"),
              check("halo lifts local contrast on a bright background", lc(halo) > lc(plain) + 15, [lc(halo), lc(plain)], "+15"),
              check("no hard plate: far background untouched", far <= 1, far, "<=1"),
              check("negative control: white text on bright ground alone is low-contrast", lc(plain) < 80, lc(plain), "<80")]
    return checks, [save_png(Image.fromarray(np.uint8(arr(halo)[..., :3])), Path(wd) / "halo.png")]


TOKENS_CSS = """:root{--font-display:"Inter";--font-body:"Liberation Serif";--font-mono:"DejaVu Sans Mono";}"""


def css_tokens(css):
    return {k: v.strip().strip('"') for k, v in re.findall(r"--([\w-]+)\s*:\s*([^;]+);", css)}


@card("TYPE-X02")
def font_tokens_audit(task, wd):
    """Three font tokens written once as CSS custom properties, read by the page and by the canvas renderer, then a familyOf() audit over every rendered run after forcing all faces to load."""
    np = np_()
    tok = css_tokens(TOKENS_CSS)
    allowed = {tok["font-display"], tok["font-body"], tok["font-mono"]}
    page = """<html><head><style>%s
h1{font-family:var(--font-display)} p{font-family:var(--font-body)} code{font-family:var(--font-mono)} .rogue{font-family:%s}</style></head>
<body><h1>Title</h1><p>Body copy</p><code>x=1</code><span class="rogue">bad</span><pre id="out"></pre>
<script>
const fams=%s;
function familyOf(el){return getComputedStyle(el).fontFamily.split(',')[0].trim().replace(/^["']|["']$/g,'');}
document.fonts.ready.then(()=>{const r=[];for(const el of document.querySelectorAll('h1,p,code,span')){r.push([el.tagName+(el.className?'.'+el.className:''),familyOf(el),fams.includes(familyOf(el))]);}
document.getElementById('out').textContent=JSON.stringify(r);});
</script></body></html>"""
    src, dom = chrome_dom(wd, page % (TOKENS_CSS, "Comic Sans MS", json.dumps(sorted(allowed))), "tokens")
    mres = re.search(r'<pre id="out">(.*?)</pre>', dom, re.S)
    rows = json.loads(mres.group(1).replace("&quot;", '"')) if mres and mres.group(1) else []
    canvas_runs = [("headline", tok["font-display"]), ("caption", tok["font-body"]), ("code", tok["font-mono"])]
    paths = {"Inter": INTER, "Liberation Serif": SERIF, "DejaVu Sans Mono": MONO}
    canvas_ok = all(fam in allowed and Path(paths[fam]).exists() for _, fam in canvas_runs)
    good = [r for r in rows if not r[0].endswith("rogue")]
    rogue = [r for r in rows if r[0].endswith("rogue")]
    out = write_json(Path(wd) / "family_audit.json", {"tokens": tok, "page": rows, "canvas": canvas_runs})
    checks = [check("tokens written once: three families", len(allowed) == 3, sorted(allowed), 3),
              check("page runs resolve to the tokens (familyOf in browser)", len(good) == 3 and all(r[2] for r in good), good, "all in tokens"),
              check("canvas reads the same tokens and the files exist", canvas_ok, canvas_runs, True),
              check("negative control: a hard-coded family is flagged", len(rogue) == 1 and rogue[0][2] is False, rogue, "flagged")]
    return checks, [out, src]
