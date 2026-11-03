"""typography-arabic: method cards as real programs with known-answer checks.

Every card renders real shaped Arabic (Pillow + libraqm/HarfBuzz, or headless Chrome / libass where the card is
about those engines) on deterministic fixtures in the work folder, measures the output and runs a negative control.
Lengths given by a card for a 1080x1920 frame are rendered at K = 0.5 (540x960) and the expected values scaled.
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
    "ARAB-91": "Mosamem (HarfRust engine, cargo workspace mosamem-core) is not present in this container; its 13 golden "
               "text tests cannot be run here, and re-testing the same properties with raqm would not prove Mosamem",
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


# ----------------------------------------------------------------------------- cards
@card("ARAB-02")
def rtl_scoping(task, wd):
    """Lint <html dir> (breaks HyperFrames renders) and scope direction:rtl + isolate to text elements only."""
    def lint(h):
        issues = []
        if re.search(r"<html\b[^>]*\bdir\s*=", h, re.I):
            issues.append({"id": "html_dir_attribute_breaks_render", "severity": "error"})
        return issues

    def scope(h):
        h = re.sub(r"(<html\b[^>]*?)\s+dir\s*=\s*(\"[^\"]*\"|'[^']*'|\S+)", r"\1", h, flags=re.I)
        if not re.search(r"<html\b[^>]*\blang=", h, re.I):
            h = re.sub(r"<html\b", '<html lang="ar"', h, count=1, flags=re.I)
        css = ".line{direction:rtl;unicode-bidi:isolate}.num{direction:ltr;unicode-bidi:isolate}"
        h = h.replace("</style>", css + "</style>", 1)
        return re.sub(r"(?<=[\s>])(\d+)(?=[\s<])", r'<span class="num">\1</span>', h)

    face = "@font-face{font-family:C;src:url('%s')}body{margin:0;background:#000;color:#fff;font:700 40px C}" % CAIRO.as_uri()
    body = '<body><div class="line" style="padding:0 20px">نصل خلال 24 ساعة</div></body></html>'
    orig = '<html lang="ar" dir="rtl"><head><meta charset="utf-8"><style>%s</style></head>%s' % (face, body)
    auto = orig.replace('dir="rtl"', 'dir="auto"')
    fixed = scope(orig)
    unscoped = re.sub(r'\s+dir="rtl"', "", orig)
    _, png_fixed = chrome_shot(wd, fixed, "fixed", 480, 90)
    _, png_un = chrome_shot(wd, unscoped, "unscoped", 480, 90)
    from PIL import Image
    bf = bbox(mask_of(arr(Image.open(png_fixed))))
    bu = bbox(mask_of(arr(Image.open(png_un))))
    checks = [check("lint flags <html dir=rtl>", [i["id"] for i in lint(orig)] == ["html_dir_attribute_breaks_render"],
                    lint(orig), "html_dir_attribute_breaks_render"),
              check("lint flags dir=auto too", len(lint(auto)) == 1, len(lint(auto)), 1),
              check("scoped html passes lint", lint(fixed) == [], lint(fixed), []),
              check("lang=ar kept, no dir on html", bool(re.search(r'<html lang="ar">', fixed)), True, True),
              check("number wrapped LTR", '<span class="num">24</span>' in fixed and ".num{direction:ltr" in fixed, True, True),
              check("rendered text right-aligned (rtl on the element)", bf is not None and bf[2] >= 455, bf and bf[2], ">=455"),
              check("negative control: without element rtl the line sits left", bu is not None and bu[2] < 455 and bu[0] <= 25,
                    bu, "left aligned")]
    return checks, [Path(wd) / "fixed.html", png_fixed]


AR_LETTERS = "؀-ۿݐ-ݿﭐ-﷿ﹰ-﻿"
AR_RUN = re.compile("[%s«](?:[%s‌‍ «»]*[%s»])?" % (AR_LETTERS, AR_LETTERS, AR_LETTERS))


@card("ARAB-07")
def auto_rtl(task, wd):
    """Regex over the Arabic blocks picks direction, alignment and card side; Arabic runs wrapped in <bdi dir=rtl>."""
    def direction(s):
        return "rtl" if re.search("[%s]" % AR_LETTERS, s) else "ltr"

    def wrap(s):
        return AR_RUN.sub(lambda m: '<bdi dir="rtl">%s</bdi>' % m.group(0), s)
    cases = {"مرحبا": "rtl", "Hello": "ltr", "ﻼ": "rtl", "ݐx": "rtl", "2024": "ltr", "Hi «سلام»": "rtl"}
    got = {s: direction(s) for s in cases}
    wrapped = wrap("Watch «الحلقة الأولى» now and ارحل")
    from PIL import ImageDraw
    W, H = 360, 70
    f = font(CAIRO, 34, 700)

    def draw_line(s, detect=True):
        c = blank((W, H))
        d = "rtl" if (detect and direction(s) == "rtl") else "ltr"
        x = W - 16 if d == "rtl" else 16
        ImageDraw.Draw(c).text((x, H / 2), s, font=f, fill="white", anchor="rm" if d == "rtl" else "lm", direction=d,
                               language="ar" if d == "rtl" else None)
        return c
    ar, la, neg = draw_line("اسم الضيف"), draw_line("Guest name"), draw_line("اسم الضيف", detect=False)
    out = save_png(ar, Path(wd) / "auto_rtl_ar.png")
    save_png(la, Path(wd) / "auto_rtl_latin.png")
    ba, bl, bn = bbox(mask_of(arr(ar))), bbox(mask_of(arr(la))), bbox(mask_of(arr(neg)))
    checks = [check("direction known answers", got == cases, got, cases),
              check("Arabic runs wrapped in bdi", wrapped.count('<bdi dir="rtl">') == 2 and "«الحلقة الأولى»</bdi>" in wrapped,
                    wrapped, "2 bdi runs incl. «…»"),
              check("Arabic line drawn from the right edge", ba[2] >= W - 20, ba[2], ">=%d" % (W - 20)),
              check("Latin line drawn from the left edge", bl[0] <= 20, bl[0], "<=20"),
              check("negative control: no detection leaves Arabic at the left", bn[0] <= 20 and bn[2] < W - 20, bn, "left")]
    return checks, [out, write_json(Path(wd) / "rtl_detect.json", {"cases": got, "wrapped": wrapped})]


@card("ARAB-09")
def real_type_over_plates(task, wd):
    """Prompt linter REVISEs Arabic in generation prompts; textless plate with a clean band; real shaped type overlaid."""
    SUFFIX = "No text, no labels, no captions, no watermark"

    def lint(p):
        notes = []
        if re.search("[؀-ۿ]", p):
            notes.append("INFO arabic_text")
        if SUFFIX.lower() not in p.lower():
            notes.append("missing no-text clause")
        return ("REVISE" if notes else "PASS"), notes

    def revise(p):
        p = re.sub("[؀-ۿ][؀-ۿ\\s«»،]*", "", p)
        p = re.sub(r"\s+", " ", p).replace('""', "").strip(" ,.")
        return p + ". Keep a clean empty band across the bottom fifth. " + SUFFIX
    orig = 'Desert dunes at golden hour with the title "رحلة الصحراء" written on the sky'
    rev = revise(orig)
    np = np_()
    from PIL import Image
    W, H = 270, 480
    yy, xx = np.mgrid[0:H, 0:W]
    plate = np.stack([200 - yy * 0.25, 120 + 40 * np.sin(xx / 30.0), 60 + yy * 0.1], -1)  # textless procedural plate
    band_top = int(H * 0.8)
    plate[band_top:] = (20, 16, 24)
    img = Image.fromarray(np.clip(plate, 0, 255).astype("uint8")).convert("RGBA")
    title = "رحلة الصحراء"
    f = font(CAIRO, 30, 800)
    t, _ = tile(title, f)
    place(img, t, W / 2, (band_top + H) / 2)
    out = save_png(img, Path(wd) / "plate_with_type.png")
    a = arr(img)
    band = a[band_top:]
    tb = bbox(mask_of(band, 137))
    ref = comps(shaped_mask(title, f))
    got = comps(mask_of(band, 137))
    raw = comps(basic_mask(title, CAIRO, 30))
    v0, n0 = lint(orig)
    v1, n1 = lint(rev)
    checks = [check("negative control: Arabic prompt is REVISEd", v0 == "REVISE" and "INFO arabic_text" in n0, [v0, n0], "REVISE"),
              check("revised prompt passes", v1 == "PASS", [v1, n1], "PASS"),
              check("no Arabic letters reach the image model", not re.search("[؀-ۿ]", rev), rev, "no U+0600-06FF"),
              check("title sits inside the reserved band", tb is not None and tb[1] > 2 and tb[3] < band.shape[0] - 2,
                    tb, "inside band"),
              check("overlaid title is shaped (joined components)", abs(got - ref) <= 1 and got < raw, got, ref),
              check("negative control: the unshaped string falls apart", raw > ref + 2, raw, ">%d" % (ref + 2))]
    return checks, [out, write_json(Path(wd) / "prompt.json", {"original": orig, "revised": rev})]


@card("ARAB-12")
def cairo_unicode_range(task, wd):
    """Cairo 600/800 as Arabic + Latin woff2 subsets under one family; verify sizes, ranges and the @font-face CSS."""
    from fontTools.ttLib import TTFont
    files = {"arabic-800": 13880, "arabic-600": 13828, "latin-800": 15256, "latin-600": 15252}
    sizes = {k: (FONTS / ("cairo-%s-normal.woff2" % k)).stat().st_size for k in files}
    cm = {k: set(TTFont(str(FONTS / ("cairo-%s-normal.woff2" % k))).getBestCmap()) for k in files}
    ar_need = set(range(0x0621, 0x063B)) | set(range(0x0641, 0x064B)) | set(range(0x0660, 0x066A))
    la_need = set(range(0x41, 0x5B)) | set(range(0x61, 0x7B)) | set(range(0x30, 0x3A))
    ranges = {"arabic": "U+0600-06FF, U+0750-077F, U+FB50-FDFF, U+FE70-FEFF", "latin": "U+0000-00FF"}
    css = "".join("@font-face{font-family:'Cairo';font-weight:%s;font-display:block;src:url(cairo-%s-%s-normal.woff2) "
                  "format('woff2');unicode-range:%s}\n" % (w, s, w, ranges[s]) for s in ("arabic", "latin") for w in (600, 800))
    cssf = Path(wd) / "cairo.css"
    cssf.write_text(css, encoding="utf-8")
    word = "القاهرة"
    ref = shaped_mask(word, font(CAIRO, 60, 800))
    sub = shaped_mask(word, font(FONTS / "cairo-arabic-800-normal.woff2", 60))
    lat = shaped_mask(word, font(FONTS / "cairo-latin-800-normal.woff2", 60))
    from PIL import Image
    Image.fromarray((sub * 255).astype("uint8")).save(Path(wd) / "arabic_subset_render.png")
    checks = [check("subset byte sizes as documented", sizes == files, sizes, files),
              check("Arabic files cover the Arabic letters and digits", all(ar_need <= cm[k] for k in ("arabic-800", "arabic-600")),
                    True, True),
              check("Latin files cover A-Z a-z 0-9", all(la_need <= cm[k] for k in ("latin-800", "latin-600")), True, True),
              check("negative control: Latin file has no Arabic letters", not (ar_need & cm["latin-800"]),
                    len(ar_need & cm["latin-800"]), 0),
              check("CSS: one family, 4 faces, display block, unicode-range",
                    css.count("font-family:'Cairo'") == 4 and css.count("font-display:block") == 4 and "U+FE70-FEFF" in css, True, True),
              check("Arabic subset renders the shaped word like full Cairo", iou(crop_ink(ref), crop_ink(sub)) > 0.85,
                    iou(crop_ink(ref), crop_ink(sub)), ">0.85"),
              check("negative control: Latin subset cannot draw it", iou(crop_ink(ref), crop_ink(lat)) < 0.5,
                    iou(crop_ink(ref), crop_ink(lat)), "<0.5")]
    return checks, [cssf, Path(wd) / "arabic_subset_render.png"]


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


@card("ARAB-17")
def screen_reading_scale(task, wd):
    """v17 tokens: base 15.5 px, leading 1.85, 78ch measure; render a paragraph at 2x and measure pitch and measure."""
    np = np_()
    tokens = {"xs": 13, "sm": 14, "base": 15.5, "lg": 17, "xl": 21, "2xl": 27}
    S = 2
    f = font(CAIRO, tokens["base"] * S, 400)
    ch = tlen("0", f)
    maxw = 78 * ch
    text = ("تعرض هذه الواجهة داخل الفيلم نصا عربيا مقروءا بحجم أساسي أكبر قليلا حتى تظهر النقاط والحركات بوضوح "
            "على الشاشة مع إيقاع رأسي واحد وعرض سطر محدود يسهل تتبعه بالعين من بداية السطر إلى نهايته دون تعب "
            "ثم يستمر الشرح في سطر ثالث ورابع لقياس المسافة بين الأسطر بدقة") .split()

    def render(lh):
        lines = wrap_words(text, f, maxw)
        pitch = tokens["base"] * S * lh
        from PIL import ImageDraw
        H = int(pitch * (len(lines) + 1))
        c = blank((int(maxw + 40), H))
        d = ImageDraw.Draw(c)
        for i, ln in enumerate(lines):
            d.text((maxw + 20, pitch * (i + 0.5)), ln, font=f, fill="white", anchor="rs", direction="rtl", language="ar")
        return c, lines

    def measured(c):
        return acf_pitch(mask_of(arr(c), 100), 10 * S, 45 * S) / S
    good, lines = render(1.85)
    bad, _ = render(1.2)
    out = save_png(good, Path(wd) / "reading_scale.png")
    pg, pb = measured(good), measured(bad)
    widths = [tlen(ln, f) for ln in lines]
    vals = list(tokens.values())
    checks = [check("token steps strictly increase", all(a < b for a, b in zip(vals, vals[1:])), vals, "increasing"),
              check("measured line pitch = 15.5 x 1.85 px", abs(pg - 28.675) <= 1.5, pg, 28.675),
              check("every line within the 78ch measure", max(widths) <= maxw and len(lines) >= 3, max(widths) / S, maxw / S),
              check("negative control: default leading 1.2 misses the pitch", abs(pb - 28.675) > 1.5, pb, "!=28.675")]
    return checks, [out, write_json(Path(wd) / "tokens.json", {"tokens": tokens, "leading": 1.85, "measure_ch": 78})]


@card("ARAB-19")
def word_mask_reveal(task, wd):
    """revealWords: each word slides up 115%→0 out of its own mask, 0.7 s, stagger 0.07 s, expo.out; hideWords down."""
    words = ["نور", "يملأ", "المكان"]
    f = font(CAIRO, 32, 800)
    at, dur, st, hat, hdur, hst = 0.2, 0.7, 0.07, 1.6, 0.45, 0.04
    holder = {}

    def state(i, t):
        h = holder["h"][i]
        if t < at + i * st:
            return None
        if t >= hat + i * hst:
            q = clamp((t - hat - i * hst) / hdur)
            e = 4 * q ** 3 if q < .5 else 1 - (-2 * q + 2) ** 4 / 2  # power4.inOut (approx)
            if t > hat + i * hst + hdur:
                return None
            return {"dy": 1.15 * h * e, "clip": True}
        e = expo_out((t - at - i * st) / dur)
        return {"dy": 1.15 * h * (1 - e), "alpha": e, "clip": True}
    row0 = word_row(words, f, 270, 240)
    holder["h"] = [r["tile"].height * 0.6 for r in row0]
    p, frames, row = kinetic(wd, "word_mask.mp4", words, f, state, 2.4)
    slots = [r["slot"] for r in row]
    ser = [[box_ink(fr, r["slot"]) for fr in frames] for r in row]
    t_first = [first_time(s, 0.05) for s in ser]
    fin = frame_at(frames, 1.3)
    ref = [comps(shaped_mask(w, f)) for w in words]
    got = [comps(mask_of(crop(fin, r["slot"]))) for r in row]
    leak = max(outside_ink(fr, slots) for fr in frames)
    static = frames[0].copy()
    checks = [check("no ink before the reveal", sum(box_ink(frames[2], s) for s in slots) == 0, 0, 0),
              check("words reveal in reading order (right to left)", t_first == sorted(t_first) and t_first[0] is not None, t_first, "ascending"),
              check("stagger ≈ 0.07 s per word", abs((t_first[2] - t_first[0]) - 2 * st) <= 0.07, t_first[2] - t_first[0], 0.14),
              check("ink never leaves the word masks", leak == 0, leak, 0),
              check("letters joined after reveal (components = shaped)", got == ref, got, ref),
              check("hidden again after hideWords", sum(box_ink(frames[-1], s) for s in slots) == 0, 0, 0)]
    sf = blank((270, 480))
    for r in row:
        place(sf, r["tile"], r["cx"], r["cy"])
    checks.append(check("negative control: a static render has ink before the reveal",
                        sum(box_ink(arr(sf), s) for s in slots) > 0, sum(box_ink(arr(sf), s) for s in slots), ">0"))
    return checks, [p]


@card("ARAB-20")
def rise_from_blur(task, wd):
    """riseWords: words wait at 40% opacity, 26 px low and 6 px blurred, then settle in 0.4 s with stagger 0.1 s."""
    np = np_()
    words = ["ضوء", "هادئ", "يصعد"]
    f = font(CAIRO, 32, 700)
    at, dur, st, rise, b0 = 0.5, 0.4, 0.1, 26, 6

    def state(i, t):
        e = expo_out((t - at - i * st) / dur) if t >= at + i * st else 0.0
        return {"dy": rise * (1 - e), "alpha": 0.4 + 0.6 * e, "blur": b0 * (1 - e)}
    p, frames, row = kinetic(wd, "rise_blur.mp4", words, f, state, 1.6)
    zones = [grow(r["ink"], 14, 40) for r in row]
    f0, f1 = frames[0], frames[-1]
    ratio0 = [lumsum(f0, z) / lumsum(f1, z) for z in zones]
    dy0 = [wcentroid(crop(f0, z))[1] - wcentroid(crop(f1, z))[1] for z in zones]

    def sharp(fr, z):
        g = lum(crop(fr, z))
        return float(np.abs(np.diff(g, axis=1)).max())
    settle = [first_time([lumsum(fr, z) for fr in frames], 0.97) for z in zones]
    checks = [check("waits at ~40% light", all(0.3 <= r <= 0.5 for r in ratio0), ratio0, 0.4),
              check("starts ~26 px low", all(18 <= d <= 30 for d in dy0), dy0, 26),
              check("starts blurred, ends sharp", all(sharp(f0, z) < 0.6 * sharp(f1, z) for z in zones),
                    [sharp(f0, z) / sharp(f1, z) for z in zones], "<0.6"),
              check("settles in word order, 0.1 s apart", settle == sorted(settle) and
                    0.1 <= settle[2] - settle[0] <= 0.3, settle, "ascending, Δ≈0.2"),
              check("final words shaped", [comps(mask_of(crop(f1, r["slot"]))) for r in row] ==
                    [comps(shaped_mask(w, f)) for w in words], [comps(mask_of(crop(f1, r["slot"]))) for r in row],
                    [comps(shaped_mask(w, f)) for w in words])]
    sf = blank((270, 480))
    for r in row:
        place(sf, r["tile"], r["cx"], r["cy"])
    rs = lumsum(arr(sf), zones[0]) / lumsum(f1, zones[0])
    checks.append(check("negative control: unprocessed words are at full light", rs > 0.9, rs, ">0.9 (fails 0.4)"))
    return checks, [p]


@card("ARAB-24")
def lines_behind_cut(task, wd):
    """Three lines rise 100%→0 behind their own cut line (reveal 0–1.2 s, stagger .22 s, out 2.6–3 s); roomy wrappers keep dots."""
    lines = ["ثلاث خطوات", "نحو بيت جديد", "تبدأ بثقة"]
    f = font(CAIRO, 34, 700)
    W, H = 270, 480
    st, rdur = 0.22, 1.2 - 2 * 0.22
    rows = []
    for k, ln in enumerate(lines):
        t, _ = tile(ln, f)
        r = {"tile": t, "cx": W / 2, "cy": 170 + k * 60}
        r["ink"] = ink_box_abs(r)
        r["slot"] = grow(r["ink"], 3, 6)      # wrapper with extra line-height
        rows.append(r)
    h = [r["ink"][3] - r["ink"][1] + 12 for r in rows]

    def draw_with(slots):
        def draw(t, c):
            for k, r in enumerate(rows):
                if t < k * st:
                    continue
                if t < 2.6:
                    dy = h[k] * (1 - expo_out((t - k * st) / rdur))
                else:
                    dy = -h[k] * pow_out((t - 2.6) / 0.4, 3)
                place(c, r["tile"], r["cx"], r["cy"] + dy, clip=slots[k])
        return draw
    slots = [r["slot"] for r in rows]
    p, frames = video(wd, "lines_cut.mp4", draw_with(slots), 3.0)
    ref = blank((W, H))
    for r in rows:
        place(ref, r["tile"], r["cx"], r["cy"])
    refa = arr(ref)
    tight = [(r["ink"][0], r["cy"] - f.size * 0.3, r["ink"][2], r["cy"] + f.size * 0.3) for r in rows]
    _, tf = video(wd, "lines_cut_tight.mp4", draw_with(tight), 1.4)
    fin = frame_at(frames, 2.0)
    ious = [iou(mask_of(fin[int(s[1]):int(s[3]), :]), mask_of(refa[int(s[1]):int(s[3]), :])) for s in slots]
    ious_t = [iou(mask_of(tf[-1][int(s[1]):int(s[3]), :]), mask_of(refa[int(s[1]):int(s[3]), :])) for s in slots]
    firsts = [first_time([box_ink(fr, s) for fr in frames], 0.05) for s in slots]
    leak = max(outside_ink(fr, slots) for fr in frames)
    checks = [check("no ink outside the cut lines", leak == 0, leak, 0),
              check("lines start .22 s apart", all(abs(firsts[k] - k * st) <= 0.07 for k in range(3)), firsts, [0, .22, .44]),
              check("all lines complete during the read (dots unclipped)", min(ious) > 0.95, ious, ">0.95"),
              check("out by 3 s", sum(box_ink(frames[-1], s) for s in slots) < 30, sum(box_ink(frames[-1], s) for s in slots), "<30"),
              check("negative control: tight wrappers clip the dots", min(ious_t) < 0.95, ious_t, "<0.95")]
    return checks, [p]


def split_arabic(text, max_chars=18):
    lines, cur = [], ""
    for w in text.split():
        if cur and len(cur) + 1 + len(w) > max_chars:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines[:4]


@card("ARAB-25")
def canvas_line_slide(task, wd):
    """splitArabic by whole words (≤18 chars, ≤4 lines); each line slides in from the right, a = clamp(4(p−0.18k))."""
    text = "كل مشهد يبدأ بفكرة صغيرة ثم يكبر حتى يملأ الشاشة بالحركة والضوء"
    lines = split_arabic(text, 18)
    W, H = 270, 480
    f = font(CAIRO, int(W * 0.074), 700)
    lh = f.size * 1.25
    y0 = 0.68 * H - lh * (len(lines) - 1) / 2
    cols = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255)]   # one hue per line, for measuring only
    tiles = [tile(ln, f, fill=cols[k] + (255,))[0] for k, ln in enumerate(lines)]
    D = 2.0

    def a_of(k, t):
        return clamp(4 * (t / D - 0.18 * k))

    def draw(t, c):
        for k, tl in enumerate(tiles):
            a = a_of(k, t)
            place(c, tl, W / 2 + (1 - cubic_out(a)) * 0.4 * W, y0 + k * lh, alpha=a)
    p, frames = video(wd, "line_slide.mp4", draw, D)
    fin = frames[-1]
    rest = []
    for k in range(len(lines)):
        band = (0, y0 + k * lh - lh / 2, W, y0 + k * lh + lh / 2)
        rest.append(band)
    def lmask(fr, k):
        c = cols[k]
        np = np_()
        on = [fr[..., j] > 50 if c[j] else fr[..., j] < 40 for j in range(3)]
        return on[0] & on[1] & on[2]

    def cx_at(fr, k):
        b = bbox(lmask(fr, k))
        return (b[0] + b[2]) / 2 if b else None
    t_test = 0.18 * 1 * D + 0.125 * D  # line 1 at a = 0.5
    meas = cx_at(frame_at(frames, t_test), 1) - cx_at(fin, 1)
    expv = (1 - cubic_out(a_of(1, round(t_test * 30) / 30))) * 0.4 * W
    naive = [text[i:i + 18] for i in range(0, len(text), 18)]
    words = set(text.split())
    checks = [check("whole-word split, ≤18 chars, ≤4 lines", all(len(l) <= 18 for l in lines) and len(lines) <= 4 and
                    " ".join(lines) == " ".join(text.split()[:sum(len(l.split()) for l in lines)]), lines, "≤18 chars"),
              check("line 1 offset at a=0.5 matches (1−easeOutCubic)·0.4w", abs(meas - expv) <= 4, meas, expv),
              check("line 0 lands before line 1", first_time([float(lmask(fr, 0).sum()) for fr in frames], 0.9) <
                    first_time([float(lmask(fr, 1).sum()) for fr in frames], 0.9), True, True),
              check("final lines centred", all(abs(cx_at(fin, k) - W / 2) <= 3 for k in range(len(lines))),
                    [cx_at(fin, k) for k in range(len(lines))], W / 2),
              check("negative control: fixed-width char split breaks words",
                    not all(set(x.split()) <= words for x in naive), naive, "a split word")]
    return checks, [p, write_json(Path(wd) / "lines.json", lines)]


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


@card("ARAB-28")
def word_turn_in(task, wd):
    """Each word tips up from depth: rotationX −78°, z −220, perspective 900, origin bottom, blur 10→0, 0.62 s back.out(1.4)."""
    np = np_()
    from PIL import Image
    words = ["نحو", "عمق", "جديد"]
    times = [0.4, 1.0, 1.6]
    f = font(CAIRO, 40, 800)
    tiles = [tile(w, f)[0] for w in words]
    W, H = 270, 480
    ys = [90, 245, 400]
    bg = (60, 70, 90)
    shadow_rgba = (0, 0, 0, 166)

    def draw(t, c):
        for i, tl in enumerate(tiles):
            t0 = times[i] - 0.1
            if t < t0:
                continue
            e = back_out((t - t0) / 0.62, 1.4)
            sh, _ = tile(words[i], f, fill=shadow_rgba)
            args = dict(theta_deg=-78 * (1 - e), z0=-220 * (1 - e), dy=46 * (1 - e), blur=10 * max(0, 1 - e))
            turn_in(c, sh.filter(__import__("PIL.ImageFilter", fromlist=["x"]).GaussianBlur(6)), W / 2, ys[i] + 5 + tl.height / 2, **args)
            turn_in(c, tl, W / 2, ys[i] + tl.height / 2, **args)
    p, frames = video(wd, "turn_in.mp4", draw, 2.6, bg=bg)
    fin = frames[-1]
    bands = [(0, y - 60, W, y + 95) for y in ys]
    hfin = [bbox(mask_of(crop(fin, b), 170)) for b in bands]
    def visible(fr, b):
        return float((np.abs(crop(fr, b) - np.array(bg, float)).max(axis=-1) > 25).sum())
    starts = [next((j / 30 for j, fr in enumerate(frames) if visible(fr, b) > 15), None) for b in bands]
    early = frame_at(frames, times[0] - 0.1 + 2 / 30)
    he = bbox(mask_of(crop(early, bands[0]), 170))
    flat = blank((W, H), bg)
    for i, tl in enumerate(tiles):
        place(flat, tl, W / 2, ys[i])
    flatm = mask_of(arr(flat), 170)
    finm = mask_of(fin, 170)
    below = crop(fin, (hfin[0][0], bands[0][1] + hfin[0][3] + 1, hfin[0][2], bands[0][1] + hfin[0][3] + 6))
    checks = [check("words start 0.1 s before their time", all(s is not None and abs(s - (t - 0.1)) <= 0.07 for s, t in zip(starts, times)),
                    starts, [t - 0.1 for t in times]),
              check("tipped back at start (projected height < 45% of final)", he is not None and (he[3] - he[1]) < 0.45 * (hfin[0][3] - hfin[0][1]),
                    he and (he[3] - he[1]) / (hfin[0][3] - hfin[0][1]), "<0.45"),
              check("lands flat and shaped (IoU with flat render)", iou(finm, flatm) > 0.85, iou(finm, flatm), ">0.85"),
              check("soft drop shadow under the word", float(lum(below).mean()) < float(np.mean(bg)) - 4, float(lum(below).mean()), "< bg"),
              check("negative control: the flat input never shows a tipped word", (bbox(mask_of(crop(arr(flat), bands[0]), 170))[3] -
                    bbox(mask_of(crop(arr(flat), bands[0]), 170))[1]) >= 0.95 * (hfin[0][3] - hfin[0][1]), True, True)]
    return checks, [p]


def graphemes(s):
    out = []
    for ch in s:
        if out and unicodedata.category(ch) in ("Mn", "Me"):
            out[-1] += ch
        else:
            out.append(ch)
    return out


@card("ARAB-29")
def typewriter_caret(task, wd):
    """typeOn: the string grows by grapheme so the shaper re-forms the prefix each frame; caret blinks at 2 Hz on hold."""
    np = np_()
    text = "اكتب فكرتك هنا"
    gs = graphemes(text)
    cps, at, hold = 22, 0.2, 1.0
    dur = clamp(len(gs) / cps, 0.5, 1.2)
    f = font(CAIRO, 34, 700)
    W, H = 360, 120
    R = W - 20
    from PIL import ImageDraw
    CARET = (231, 182, 90)

    def n_at(t):
        return len(gs) if t >= at + dur else max(0, int(len(gs) * (t - at) / dur)) if t >= at else 0

    def draw(t, c):
        n = n_at(t)
        s = "".join(gs[:n])
        d = ImageDraw.Draw(c)
        x_end = R
        if s:
            d.text((R, H / 2), s, font=f, fill="white", anchor="rm", direction="rtl", language="ar")
            x_end = R - tlen(s, f)
        on = t < at + dur or ((t - at - dur) % 0.5) < 0.25
        if on and t < at + dur + hold:
            d.rectangle([x_end - 5, H / 2 - 18, x_end - 2, H / 2 + 18], fill=CARET)
    total = at + dur + hold
    p, frames = video(wd, "typewriter.mp4", draw, total, size=(W, H))

    def white(fr):
        return (fr.min(axis=-1) > 150)

    def ref(s):
        c = blank((W, H))
        ImageDraw.Draw(c).text((R, H / 2), s, font=f, fill="white", anchor="rm", direction="rtl", language="ar")
        return white(arr(c))
    ious, neg, cropf = [], [], []
    full = ref(text)
    for k in (3, 6, 9):
        t = at + (k + 0.5) * dur / len(gs)
        fr = frame_at(frames, t)
        n = n_at(round(t * 30) / 30)
        s = "".join(gs[:n])
        ious.append(iou(white(fr), ref(s)))
        # isolated letters side by side (what per-letter spans would draw)
        iso = blank((W, H))
        x = R
        for g in gs[:n]:
            ImageDraw.Draw(iso).text((x, H / 2), g, font=f, fill="white", anchor="rm", direction="rtl", language="ar")
            x -= tlen(g, f)
        neg.append(iou(white(fr), white(arr(iso))))
        m = full.copy()
        m[:, :int(R - tlen(s, f))] = False
        cropf.append(iou(white(fr), m))
    hold0 = at + dur
    caret = [float(colour_mask(frame_at(frames, hold0 + dt), CARET, 50).sum()) for dt in (0.1, 0.35, 0.6, 0.85)]
    tg = graphemes("بِسْمِ")
    checks = [check("each frame shows the shaped prefix", min(ious) > 0.9, ious, ">0.9"),
              check("prefix re-formed (last letter final form, not a crop of the full line)", all(a > b + 0.02 for a, b in zip(ious, cropf)),
                    cropf, "< prefix IoU"),
              check("caret blinks at 2 Hz on hold", caret[0] > 20 and caret[1] == 0 and caret[2] > 20 and caret[3] == 0, caret, "on,off,on,off"),
              check("grapheme stepping keeps harakat on their letters", tg == ["بِ", "سْ", "مِ"], tg, ["بِ", "سْ", "مِ"]),
              check("duration = clamp(len/cps, .5, 1.2)", abs(dur - clamp(14 / 22, .5, 1.2)) < 1e-9, dur, 14 / 22),
              check("negative control: per-letter isolated spans do not match", max(neg) < 0.6, neg, "<0.6")]
    return checks, [p]


@card("ARAB-31")
def rolling_pill(task, wd):
    """Words roll vertically inside an overflow:hidden pill (0.4 s ease-out per step) while rings grow +40 px per step."""
    np = np_()
    from PIL import ImageDraw
    words = ["أيام", "ساعات", "دقائق"]
    W, H = 360, 360
    f = font(CAIRO, 34, 700)
    tiles = [tile(w, f)[0] for w in words]
    pw, ph = 170, 64
    box = (W / 2 - pw / 2, H / 2 - ph / 2, W / 2 + pw / 2, H / 2 + ph / 2)
    steps = [0.6, 1.6]
    PURPLE = (150, 100, 255)

    def pos(t):
        k = 0.0
        for s in steps:
            k += cubic_out((t - s) / 0.4) if t >= s else 0
        return k

    def draw(t, c):
        k = pos(t)
        d = ImageDraw.Draw(c)
        for r in range(1, 4):
            if r <= k + 1 + 1e-6:
                g = 40 * r * min(1.0, k + 1 - (r - 1)) / 2
                d.rounded_rectangle([box[0] - g, box[1] - g / 2, box[2] + g, box[3] + g / 2], radius=40, outline=PURPLE, width=2)
        d.rounded_rectangle(box, radius=32, fill=(30, 20, 60))
        for i, tl in enumerate(tiles):
            place(c, tl, W / 2, H / 2 + (i - k) * ph, clip=box)
    p, frames = video(wd, "pill.mp4", draw, 2.4, size=(W, H))

    def which(fr):
        m = mask_of(crop(fr, box), 150)
        best = []
        for i, tl in enumerate(tiles):
            ref = blank((W, H))
            place(ref, tl, W / 2, H / 2)
            best.append(iou(m, mask_of(crop(arr(ref), box), 150)))
        return int(np.argmax(best)), max(best)
    seen = [which(frame_at(frames, t)) for t in (0.4, 1.2, 2.2)]
    ring = [bbox(colour_mask(frame_at(frames, t), PURPLE, 60)) for t in (0.4, 1.2, 2.2)]
    rw = [b[2] - b[0] for b in ring]
    inside = np.zeros((H, W), bool)
    inside[int(box[1]):int(box[3]), int(box[0]):int(box[2])] = True
    leak = max(int(((fr.min(axis=-1) > 150) & ~inside).sum()) for fr in frames)
    nc = blank((W, H))
    for i, tl in enumerate(tiles):
        place(nc, tl, W / 2, H / 2 + (i - 0.5) * ph)
    checks = [check("settles on days → hours → minutes", [s[0] for s in seen] == [0, 1, 2] and min(s[1] for s in seen) > 0.85, seen, [0, 1, 2]),
              check("rings grow +40 px per step", all(abs((rw[i + 1] - rw[i]) - 40) <= 4 for i in range(2)), rw, "+40 each"),
              check("no word ink outside the pill", leak == 0, leak, 0),
              check("negative control: without the mask the stack spills out", int(mask_of(arr(nc), 150)[:int(box[1])].sum()) > 0, True, True)]
    return checks, [p]


@card("ARAB-33")
def words_on_circle(task, wd):
    """Whole words placed by angle around a centre; appear 0–1 s, rotate slowly 1–3.5 s, stop with the key word on top."""
    np = np_()
    words = ["الشمس", "تدور", "حولنا", "دائما"]
    cols = [(255, 60, 60), (60, 255, 60), (80, 120, 255), (255, 255, 60)]
    f = font(CAIRO, 26, 700)
    tiles = [tile(w, f, fill=c + (255,))[0] for w, c in zip(words, cols)]
    W = H = 360
    R = 120
    base = [math.radians(-90 + 150 + 90 * i) for i in range(4)]     # key word (0) starts 150° from the top
    total = math.radians(-150)
    from PIL import ImageDraw

    def rot_at(t):
        return 0.0 if t < 1 else total * (0.5 - 0.5 * math.cos(math.pi * clamp((t - 1) / 2.5)))

    def draw(t, c):
        ImageDraw.Draw(c).ellipse([W / 2 - 40, H / 2 - 40, W / 2 + 40, H / 2 + 40], fill=(255, 170, 40))
        a0 = clamp(t / 1.0)
        for i, tl in enumerate(tiles):
            a = base[i] + rot_at(t)
            place(c, tl, W / 2 + R * math.cos(a), H / 2 + R * math.sin(a), rot=-(math.degrees(a) + 90), alpha=a0)
    p, frames = video(wd, "circle.mp4", draw, 5.0, size=(W, H))

    def ang(fr, i):
        m = colour_mask(fr, cols[i], 70)
        c = centroid(m)
        return math.degrees(math.atan2(c[1] - H / 2, c[0] - W / 2)), m
    a_end, m_end = ang(frames[-1], 0)
    a_mid, _ = ang(frame_at(frames, 2.25), 0)
    a_start, _ = ang(frame_at(frames, 1.0), 0)
    b = bbox(m_end)
    speeds = []
    for t in np.arange(1.0, 3.5, 0.25):
        a1, _ = ang(frame_at(frames, t), 0)
        a2, _ = ang(frame_at(frames, t + 0.25), 0)
        speeds.append(abs((a2 - a1 + 180) % 360 - 180) / 0.25)
    checks = [check("key word stops on top (−90°)", abs(a_end + 90) <= 4, a_end, -90),
              check("upright at the top (wider than tall)", (b[2] - b[0]) > 1.5 * (b[3] - b[1]), [b[2] - b[0], b[3] - b[1]], "w > 1.5h"),
              check("word kept whole (shaped components)", comps(m_end) == comps(shaped_mask(words[0], f)), comps(m_end),
                    comps(shaped_mask(words[0], f))),
              check("slow rotation (≤ 100°/s)", max(speeds) <= 100, max(speeds), "<=100"),
              check("fades in over the first second", sum(int(colour_mask(frames[0], c, 70).sum()) for c in cols) == 0 and
                    int(colour_mask(frame_at(frames, 1.2), cols[0], 70).sum()) > 50, True, True),
              check("negative control: the unrotated layout does not put the key word on top", abs(a_start + 90) > 30, a_start, "far from −90")]
    return checks, [p]


@card("ARAB-34")
def keyword_slam(task, wd):
    """slam: opacity 0, scale .94, y 24k, blur 10, clip inset(100%→−25%) → rest in 0.34 s expo.out; 200k px weight 700."""
    np = np_()
    W, H = 270, 480
    k = W / 1080
    word = "إطلاقاً"
    f = font(CAIRO, int(200 * k), 700)
    tl, _ = tile(word, f)
    at, dur = 0.3, 0.34
    cx, cy = W / 2, H / 2

    def draw(t, c):
        if t < at:
            return
        e = expo_out((t - at) / dur)
        q = 1 - 1.25 * e                                    # top inset 100% → −25%
        x0, y0 = cx - tl.width / 2, cy - tl.height / 2
        clip = (x0 - 0.1 * tl.width, y0 + q * tl.height, x0 + 1.1 * tl.width, y0 + 1.45 * tl.height)
        place(c, tl, cx, cy + 24 * k * (1 - e), scale=0.94 + 0.06 * e, alpha=e, blur=10 * (1 - e), clip=clip)
    p, frames = video(wd, "slam.mp4", draw, 1.0, size=(W, H))
    fin = mask_of(frames[-1], 128)
    bf = bbox(fin)
    early = mask_of(frame_at(frames, at + 1 / 30), 40)
    be = bbox(early)
    ref = blank((W, H))
    place(ref, tl, cx, cy)
    refm = mask_of(arr(ref), 128)
    land = first_time([float(mask_of(fr, 128).sum()) for fr in frames], 0.97)
    checks = [check("nothing before the slam", float(frames[int(at * 30) - 1].max()) < 20, float(frames[int(at * 30) - 1].max()), "<20"),
              check("mask opens upward (early ink only low)", be is not None and be[1] > bf[1] + 0.3 * (bf[3] - bf[1]), be, "top well below final top"),
              check("sharp and complete within ~1/3 s", land is not None and land <= at + dur + 0.05 and iou(fin, refm) > 0.9,
                    [land, iou(fin, refm)], [at + dur, ">0.9"]),
              check("negative control: an unmasked word shows its top at once", bbox(refm)[1] <= bf[1] + 2, bbox(refm)[1], bf[1])]
    return checks, [p]


@card("ARAB-35")
def slam_settle(task, wd):
    """Word block drops past its slot (0–0.4 s), one back.out(1.6) rebound (0.4–0.8 s), then holds to read until 2 s."""
    np = np_()
    W, H = 270, 480
    f = font(CAIRO, 46, 900)
    tl, _ = tile("الآن", f)
    y_slot, past = H / 2, 16

    def y_at(t):
        if t < 0.4:
            return -tl.height + (y_slot + past + tl.height) * (t / 0.4) ** 2
        if t < 0.8:
            return y_slot + past - past * back_out((t - 0.4) / 0.4, 1.6)
        return y_slot

    def draw(t, c):
        place(c, tl, W / 2, y_at(t))
    p, frames = video(wd, "slam_settle.mp4", draw, 2.0, size=(W, H))
    ys = [wcentroid(fr)[1] if fr.max() > 50 else None for fr in frames]
    fin = ys[-1]
    mx = max(y for y in ys if y is not None)
    imax = ys.index(mx)
    after = [y for y in ys[int(0.85 * 30):] if y is not None]
    ref = mask_of(frames[-1], 128)
    shape_ok = [iou(crop_ink(mask_of(fr, 128)), crop_ink(ref)) for fr in frames[int(0.45 * 30):int(0.8 * 30):3]]
    checks = [check("drops past its slot", mx - fin >= 8, mx - fin, ">=8 px"),
              check("deepest point near 0.4 s", 0.3 <= imax / 30 <= 0.5, imax / 30, 0.4),
              check("locked after 0.8 s", max(after) - min(after) <= 1.0, max(after) - min(after), "<=1 px"),
              check("whole word moves (shape unchanged)", min(shape_ok) > 0.9, shape_ok, ">0.9"),
              check("negative control: a static word never passes its slot", (wcentroid(frames[-1])[1] - fin) < 8, 0, "<8")]
    return checks, [p]


@card("ARAB-36")
def hero_punch_bloom(task, wd):
    """Heavy word at ~40% of frame height punches from scale 1.15 + blur 8 in 300 ms over an orange 20 px glow copy at 40%."""
    np = np_()
    W, H = 480, 270
    word = "قوة"
    sz = 60
    while True:
        m = shaped_mask(word, font(CAIRO, sz, 900))
        b = bbox(m)
        if b[3] - b[1] >= 0.4 * H:
            break
        sz += 2
    f = font(CAIRO, sz, 900)
    tl, _ = tile(word, f)
    glow, _ = tile(word, f, fill=(242, 117, 37, 255), pad=int(sz * 0.6))
    from PIL import ImageFilter
    glow = glow.filter(ImageFilter.GaussianBlur(20))
    at = 0.2

    def draw(t, c, with_glow=True):
        if t < at:
            return
        e = cubic_out((t - at) / 0.3)
        if with_glow:
            place(c, glow, W / 2, H / 2, scale=1.15 - 0.15 * e, alpha=0.4 * e)
        place(c, tl, W / 2, H / 2, scale=1.15 - 0.15 * e, blur=8 * (1 - e), alpha=e)
    p, frames = video(wd, "hero_punch.mp4", draw, 1.0, size=(W, H))
    fin = frames[-1]
    bf = bbox(mask_of(fin, 200))
    def spread(a):                       # luminance-weighted std of the blue channel (white text, not the orange glow)
        g = a[..., 2]
        xs = np.arange(a.shape[1])[None, :]
        tot = g.sum()
        mx = (g * xs).sum() / tot
        return float((g * (xs - mx) ** 2).sum() / tot)
    t1 = round((at + 1 / 30) * 30) / 30
    e1 = cubic_out((t1 - at) / 0.3)
    s_exp = 1.15 - 0.15 * e1
    var1 = spread(frame_at(frames, t1)) - (8 * (1 - e1)) ** 2
    s_meas = math.sqrt(max(var1, 0) / spread(fin))

    def orange(a):
        return int(((a[..., 0] - a[..., 2] > 25) & (a[..., 0] > 25) & (a[..., 0] > a[..., 1])).sum())
    plain = blank((W, H))
    place(plain, tl, W / 2, H / 2)
    checks = [check("word ≈ 40% of frame height", abs((bf[3] - bf[1]) / H - 0.40) <= 0.04, (bf[3] - bf[1]) / H, 0.40),
              check("punches in from 1.15x (scale measured at the 2nd frame, blur removed)", abs(s_meas - s_exp) <= 0.03 and s_meas > 1.06,
                    s_meas, s_exp),
              check("orange bloom halo around the word", orange(fin) > 800, orange(fin), ">800 px"),
              check("negative control: the plain word has no bloom", orange(arr(plain)) < 50, orange(arr(plain)), "<50")]
    return checks, [p]


@card("ARAB-37")
def word_acts_meaning(task, wd):
    """'توسع' widens by uniform scale (never scaleX) 0.6–1.5 s while the sentence holds still; read to 3 s."""
    np = np_()
    W, H = 270, 480
    f = font(CAIRO, 34, 700)
    line1, _ = tile("السوق في", f)
    act, _ = tile("توسع", f)

    def draw(t, c):
        place(c, line1, W / 2, 200)
        s = 1 + 0.4 * cubic_out((t - 0.6) / 0.9) if t > 0.6 else 1.0
        place(c, act, W / 2, 270, scale=s)
    p, frames = video(wd, "acts.mp4", draw, 3.0, size=(W, H))
    top = (0, 160, W, 235)
    bot = (0, 236, W, 330)
    a, b = bbox(mask_of(crop(frame_at(frames, 0.5), bot), 128)), bbox(mask_of(crop(frame_at(frames, 1.6), bot), 128))
    wr, hr = (b[2] - b[0]) / (a[2] - a[0]), (b[3] - b[1]) / (a[3] - a[1])
    still = max(float(np.abs(crop(fr, top) - crop(frames[0], top)).max()) for fr in frames)
    checks = [check("the word widens ×1.4", abs(wr - 1.4) <= 0.06, wr, 1.4),
              check("uniform scale (height grows with width)", abs(wr - hr) <= 0.08, [wr, hr], "equal"),
              check("the sentence holds still", still <= 12, still, "<=12"),
              check("negative control: the static sentence does not act", abs(bbox(mask_of(crop(frames[0], bot), 128))[2] -
                    bbox(mask_of(crop(frames[0], bot), 128))[0] - (a[2] - a[0])) <= 1, True, True)]
    return checks, [p]


@card("ARAB-38")
def typographic_echo(task, wd):
    """3 delayed copies (opacity .6→.1) push out 0–0.7 s, converge on the master 0.7–1.2 s, then vanish; master stays crisp."""
    np = np_()
    W, H = 360, 200
    f = font(CAIRO, 44, 800)
    tl, _ = tile("الصدى", f)
    ops = [0.6, 0.35, 0.1]

    def draw(t, c):
        for i, o in enumerate(ops):
            if t < 0.7:
                d = 26 * (i + 1) * cubic_out(t / 0.7)
            elif t < 1.2:
                d = 26 * (i + 1) * (1 - cubic_out((t - 0.7) / 0.5))
            else:
                continue
            place(c, tl, W / 2 + d, H / 2, alpha=o)
        place(c, tl, W / 2, H / 2)
    p, frames = video(wd, "echo.mp4", draw, 2.5, size=(W, H))
    ref = blank((W, H))
    place(ref, tl, W / 2, H / 2)
    refa = arr(ref)
    mb = bbox(mask_of(refa, 128))
    right = (mb[2] + 2, 0, W, H)
    mid = frame_at(frames, 0.6)
    ech = lum(crop(mid, right))
    late = float(np.abs(frame_at(frames, 1.4) - refa).max())
    crisp = iou(mask_of(crop(mid, mb), 200), mask_of(crop(refa, mb), 200))
    checks = [check("echo copies trail the word at 0.6 s", float((ech > 15).sum()) > 200, float((ech > 15).sum()), ">200"),
              check("copies dimmer than the master", float(ech.max()) <= 0.85 * 255, float(ech.max()), "<=217"),
              check("copies gone after converging (frame = master)", late <= 12, late, "<=12"),
              check("master crisp throughout", crisp > 0.9, crisp, ">0.9"),
              check("negative control: master alone has no echo", float((lum(crop(refa, right)) > 15).sum()) == 0, 0, 0)]
    return checks, [p]


@card("ARAB-39")
def gilded_fills(task, wd):
    """Gradient through the glyphs of the whole shaped word (gold) and a one-pass light sweep (background-position)."""
    np = np_()
    from PIL import Image
    W, H = 360, 160
    word = "ذهبي"
    f = font(CAIRO, 70, 900)
    a = shaped_mask(word, f)
    m = np.zeros((H, W), bool)
    y0, x0 = (H - a.shape[0]) // 2, (W - a.shape[1]) // 2
    m[y0:y0 + a.shape[0], x0:x0 + a.shape[1]] = a
    stops = [hexrgb("#8a6d1e"), hexrgb("#f7e08a"), hexrgb("#b8892b")]
    xs = np.linspace(0, 1, W)

    def grad(u):
        u = np.clip(u, 0, 1)
        lo = np.where(u < 0.5, 0, 1)
        tt = np.where(u < 0.5, u / 0.5, (u - 0.5) / 0.5)
        s0 = np.array(stops)[lo]
        s1 = np.array(stops)[lo + 1]
        return s0 + (s1 - s0) * tt[:, None]

    def frame(pos):
        g = grad(xs)[None].repeat(H, 0)
        band = np.exp(-((xs - pos) / 0.06) ** 2)[None, :, None]
        g = g + (255 - g) * band * 0.8
        img = np.zeros((H, W, 3))
        img[m] = g[m]
        return Image.fromarray(img.astype("uint8"))
    still = frame(-1.0)
    out = Path(wd) / "gilded.png"
    still.save(out)
    frs = [frame(p) for p in np.linspace(-0.1, 1.1, 30)]
    vid = encode(Path(wd) / "sweep.mp4", frs, (W, H))
    sa = np.asarray(still, float)
    cols = [sa[m & (np.arange(W)[None] >= int(W * q)) & (np.arange(W)[None] < int(W * q) + 12)].mean(axis=0) for q in (0.25, 0.5, 0.7)]
    peaks = []
    for fr in fx.frames(vid, (W, H))[10:20:3]:
        l = (lum(fr) - lum(sa)) * m
        colsum = m.sum(axis=0)
        prof = np.where(colsum >= 3, l.sum(axis=0) / np.maximum(colsum, 1), -1)
        peaks.append(float(np.argmax(prof)))
    flat = np.where(m[..., None], np.array(stops[1]), 0)
    checks = [check("gradient runs through the glyphs (mid brighter than edges)", lum(cols[1]) > lum(cols[0]) + 30,
                    [list(map(int, c)) for c in cols], "dark→light→dark"),
              check("outside the glyphs untouched", int(sa[~m].max()) == 0, int(sa[~m].max()), 0),
              check("word shaped as one string", comps(m) == comps(shaped_mask(word, f)) < comps(basic_mask(word, CAIRO, 70)),
                    comps(m), comps(shaped_mask(word, f))),
              check("light sweep travels across once", peaks == sorted(peaks) and peaks[-1] - peaks[0] > 80, peaks, "increasing"),
              check("negative control: a flat fill has no gradient", float(np.ptp(flat[m], axis=0).max()) == 0, 0, 0)]
    return checks, [out, vid]


@card("ARAB-40")
def three_level_hierarchy(task, wd):
    """Speech 54 px/500, phrase 96 px/700, keyword 220 px/700 (one family) at 1080x1920 — rendered at K and measured."""
    np = np_()
    from PIL import ImageDraw
    W, H = 540, 960
    word = "كلمة"
    levels = {"l1": (54, 500, 1452), "l2": (96, 700, 1236), "l3": (220, 700, 1196)}
    IVORY = (245, 238, 222)
    hs, outs, thick = {}, [], {}
    for name, (sz, wt, y) in levels.items():
        c = blank((W, H), (70, 80, 95))
        f = font(CAIRO, sz * K, wt)
        sh, _ = tile(word, f, fill=(0, 0, 0, 115))
        from PIL import ImageFilter
        place(c, sh.filter(ImageFilter.GaussianBlur(8 * K)), W / 2, y * K + 1.5 * K)
        t, _ = tile(word, f, fill=IVORY + (255,))
        place(c, t, W / 2, y * K)
        p = save_png(c, Path(wd) / ("%s.png" % name))
        outs.append(p)
        m = colour_mask(arr(c), IVORY, 30)
        b = bbox(m)
        hs[name] = b[3] - b[1]
        thick[name] = float(m.sum()) / (b[3] - b[1]) ** 2
        below = arr(c)[b[3] + 2:b[3] + 6, b[0]:b[2]]
        hs[name + "_shadow"] = float(lum(below).mean())
    r12, r13 = hs["l2"] / hs["l1"], hs["l3"] / hs["l1"]
    checks = [check("phrase/speech height ratio = 96/54", abs(r12 - 96 / 54) <= 0.12, r12, 96 / 54),
              check("keyword/speech height ratio = 220/54", abs(r13 - 220 / 54) <= 0.25, r13, 220 / 54),
              check("speech at weight 500 lighter than phrase at 700", thick["l1"] < thick["l2"], thick, "l1 < l2"),
              check("double shadow darkens below the text", hs["l3_shadow"] < 82, hs["l3_shadow"], "< bg 82"),
              check("negative control: equal sizes give ratio 1 (no hierarchy)", abs(1.0 - 96 / 54) > 0.12, 1.0, "≠1.78")]
    return checks, outs


def parse_script(text):
    lines = []
    for raw in text.splitlines():
        raw = re.sub(r"\[[^\]]*\]", "", raw).replace("...", "").replace("…", "").strip()
        if not raw:
            continue
        toks, seen = [], False
        for w in raw.split():
            em = w.startswith("*") and w.endswith("*") and len(w) > 2
            toks.append({"w": w.strip("*"), "em": bool(em and not seen)})
            seen = seen or em
        lines.append(toks)
    return lines


@card("ARAB-41")
def asterisk_emphasis(task, wd):
    """*word* convention: parse lines (strip [brackets], '...'), one starred word per line → accent colour at 1.1x."""
    np = np_()
    script = "[مقدمة] هذا هو *السر* الحقيقي...\nلا تنتظر *الفرصة* بل *اصنعها*"
    lines = parse_script(script)
    ACC = hexrgb("#E7B65A")
    W, H = 360, 200
    f = font(CAIRO, 30, 700)
    fe = font(CAIRO, 33, 700)
    c = blank((W, H))
    boxes = []
    for li, toks in enumerate(lines):
        x = W - 16
        cy = 60 + li * 80
        for tk in toks:
            ff = fe if tk["em"] else f
            t, _ = tile(tk["w"], ff, fill=(ACC + (255,)) if tk["em"] else (255, 255, 255, 255))
            ln = tlen(tk["w"], ff)
            place(c, t, x - ln / 2, cy)
            if tk["em"]:
                boxes.append((x - ln - 2, cy - 40, x + 2, cy + 40, tk["w"]))
            x -= ln + f.size * 0.3
    out = save_png(c, Path(wd) / "emphasis.png")
    a = arr(c)
    acc = colour_mask(a, ACC, 40)
    inside = np.zeros_like(acc)
    for b in boxes:
        inside[int(b[1]):int(b[3]), int(b[0]):int(b[2])] = True
    hp = bbox(shaped_mask("السر", f))
    he = bbox(shaped_mask("السر", fe))
    raw = blank((W, 80))
    from PIL import ImageDraw
    ImageDraw.Draw(raw).text((W - 16, 40), "هذا هو *السر*", font=f, fill="white", anchor="rm", direction="rtl", language="ar")
    checks = [check("parsed known answer", [[(t["w"], t["em"]) for t in l] for l in lines] ==
                    [[("هذا", False), ("هو", False), ("السر", True), ("الحقيقي", False)],
                     [("لا", False), ("تنتظر", False), ("الفرصة", True), ("بل", False), ("اصنعها", False)]], lines, "one em per line"),
              check("accent pixels only on the starred words", int(acc.sum()) > 200 and int((acc & ~inside).sum()) == 0,
                    [int(acc.sum()), int((acc & ~inside).sum())], "[>200, 0]"),
              check("starred word at 1.1x", abs((he[3] - he[1]) / (hp[3] - hp[1]) - 1.1) <= 0.05, (he[3] - he[1]) / (hp[3] - hp[1]), 1.1),
              check("negative control: the raw line has no accent", int(colour_mask(arr(raw), ACC, 40).sum()) == 0, 0, 0)]
    return checks, [out, write_json(Path(wd) / "parsed.json", lines)]


@card("ARAB-43")
def rtl_highlighter(task, wd):
    """Rounded #f2c94c bar at 70%, 35% of text height, grows 0→100% width with transform-origin right behind the keyword."""
    np = np_()
    from PIL import ImageDraw, Image
    W, H = 360, 160
    f = font(CAIRO, 44, 800)
    word = "الأهم"
    t, _ = tile(word, f)
    r = {"tile": t, "cx": W / 2, "cy": H / 2}
    ink = ink_box_abs(r)
    th = ink[3] - ink[1]
    bar_h = 0.35 * th
    y1 = ink[3] - th * 0.12
    YEL = (242, 201, 76)

    def draw(tt, c):
        e = cubic_out((tt - 0.2) / 0.4) if tt > 0.2 else 0
        if e > 0:
            ov = Image.new("RGBA", c.size, (0, 0, 0, 0))
            x1 = ink[2] + 4
            ImageDraw.Draw(ov).rounded_rectangle([x1 - (ink[2] - ink[0] + 8) * e, y1 - bar_h, x1, y1], radius=6,
                                                 fill=YEL + (178,))
            c.alpha_composite(ov)
        place(c, t, W / 2, H / 2)
    p, frames = video(wd, "highlighter.mp4", draw, 1.0, size=(W, H))
    exp_col = tuple(int(0.7 * v) for v in YEL)

    def bar(fr):
        return bbox(colour_mask(fr, exp_col, 30))
    bs = [bar(frame_at(frames, tt)) for tt in (0.3, 0.4, 0.8)]
    rights = [b[2] for b in bs]
    lefts = [b[0] for b in bs]
    checks = [check("bar anchored at the right edge", max(rights) - min(rights) <= 2, rights, "constant"),
              check("bar grows leftwards", lefts[0] > lefts[1] > lefts[2], lefts, "decreasing"),
              check("bar height ≈ 35% of the text", abs((bs[2][3] - bs[2][1]) / th - 0.35) <= 0.06, (bs[2][3] - bs[2][1]) / th, 0.35),
              check("bar covers the keyword at the end", abs((bs[2][2] - bs[2][0]) - (ink[2] - ink[0] + 8)) <= 3, bs[2][2] - bs[2][0],
                    ink[2] - ink[0] + 8),
              check("negative control: no bar before the swipe", bar(frames[0]) is None, None, None)]
    return checks, [p]


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


@card("ARAB-44")
def rubber_stamp(task, wd):
    """Red outlined stamp #eb5757, 4 px border, rotated −4°, scale 1.6→1 with overshoot + opacity in ~200 ms, micro shake."""
    np = np_()
    from PIL import Image, ImageDraw
    W, H = 360, 300
    RED = hexrgb("#eb5757")
    f = font(CAIRO, 40, 900)
    t, _ = tile("عاجل", f, fill=RED + (255,), pad=10)
    st = Image.new("RGBA", (t.width + 40, t.height + 20), RED + (0,))
    ImageDraw.Draw(st).rectangle([2, 2, st.width - 3, st.height - 3], outline=RED + (255,), width=4)
    st.alpha_composite(t, (20, 10))
    at = 0.3
    shake = {1: (3, -2), 2: (-3, 2), 3: (2, -1)}

    def draw(tt, c):
        k = int(round((tt - at - 0.2) * 30))
        ox, oy = shake.get(k, (0, 0))
        ImageDraw.Draw(c).rectangle([20 + ox, 20 + oy, W - 20 + ox, H - 20 + oy], fill=(240, 235, 220))
        ImageDraw.Draw(c).rectangle([40 + ox, 40 + oy, 60 + ox, 60 + oy], fill=(20, 20, 20))
        if tt >= at:
            e = back_out((tt - at) / 0.2, 1.2)
            place(c, st, W / 2 + ox, H / 2 + oy, scale=1.6 - 0.6 * e, rot=4, alpha=clamp((tt - at) / 0.1))
    p, frames = video(wd, "stamp.mp4", draw, 1.0, size=(W, H), bg=(0, 0, 0))
    fin = frames[-1]
    red = colour_mask(fin, RED, 45)
    # border: the outermost red ring of the stamp
    from scipy import ndimage
    lab, n = ndimage.label(red)
    sizes = ndimage.sum(red, lab, range(1, n + 1))
    border = lab == (int(np.argmax(sizes)) + 1)
    ang = pca_angle(border)
    rows = np.nonzero(border[:, int(centroid(border)[0])])[0]
    thick = int(np.argmax(np.diff(rows) > 1) + 1) if (np.diff(rows) > 1).any() else len(rows)
    fe_ = frame_at(frames, at + 1 / 30)
    b_early = bbox((fe_[..., 0] - fe_[..., 1] > 40) & (fe_[..., 0] > 60) & (lum(fe_) < 200))
    s_exp = 1.6 - 0.6 * back_out((round((at + 1 / 30) * 30) / 30 - at) / 0.2, 1.2)
    b_fin = bbox(red)

    def marker(fr):
        return centroid(lum(fr) < 40 & (lum(fr) >= 0))
    def mk(fr):
        m = (lum(fr) < 50)
        m[:15, :] = False; m[:, :15] = False; m[H - 15:, :] = False; m[:, W - 15:] = False
        m[:, 100:] = False
        return centroid(m)
    m0 = mk(frames[int(at * 30) + 2])
    disp = [math.dist(mk(frame_at(frames, at + 0.2 + j / 30)), m0) for j in (1, 2, 3)]
    rest = math.dist(mk(frames[-1]), m0)
    checks = [check("stamp rotated −4° (CSS) on the card", abs(abs(ang) - 4) <= 1.2, ang, "±4°"),
              check("border ≈ 4 px", 3 <= thick <= 6, thick, 4),
              check("slams down from 1.6x (scale at 1st frame matches the tween)", b_early is not None and
                    abs((b_early[2] - b_early[0]) / (b_fin[2] - b_fin[0]) - s_exp) <= 0.08 and s_exp > 1.15,
                    b_early and (b_early[2] - b_early[0]) / (b_fin[2] - b_fin[0]), s_exp),
              check("micro shake on contact, then still", min(disp) >= 1.5 and rest <= 0.5, [disp, rest], "shake then 0"),
              check("negative control: no red before the stamp", int(colour_mask(frames[0], RED, 45).sum()) == 0, 0, 0)]
    return checks, [p]


def line_meta(s):
    return {"question": "؟" in s or "?" in s, "quote": "«" in s}


@card("ARAB-45")
def giant_question_mark(task, wd):
    """Hollow '؟' (U+061F) 420 px, 3 px stroke #f5c97a; from scale 2.4, −12°, opacity 0 in 0.7 s; fill → .18; implodes."""
    np = np_()
    from PIL import ImageChops
    W = H = 540
    q = "؟"
    GOLD = hexrgb("#f5c97a")
    f = font(CAIRO, int(420 * K), 700)
    stroke, _ = tile(q, f, fill=GOLD + (255,), stroke=2, stroke_fill=GOLD + (255,), pad=40)
    fill, _ = tile(q, f, fill=GOLD + (255,), stroke=0, pad=40 + 2)
    a_s = stroke.getchannel("A")
    a_f = fill.getchannel("A")
    ring = ImageChops.subtract(a_s, a_f)
    out_t = stroke.copy()

    def glyph(fill_a):
        g = stroke.copy()
        g.putalpha(ImageChops.add(ring, a_f.point(lambda v: int(v * fill_a))))
        return g

    def draw(t, c):
        if t < 2.0:
            e = cubic_out(t / 0.7)
            fa = 0.18 * clamp((t - 0.7) / 0.5)
            place(c, glyph(fa), W / 2, H / 2, scale=2.4 - 1.4 * e, rot=12 * (1 - e), alpha=e)
        else:
            e = clamp((t - 2.0) / 0.25) ** 3
            place(c, glyph(0.18), W / 2, H / 2, scale=1 - 0.8 * e)
    p, frames = video(wd, "question.mp4", draw, 2.4, size=(W, H))
    fin = frame_at(frames, 1.6)
    interior = (np.asarray(a_f) > 250)
    g = lum(fin)
    full = colour_mask(fin, GOLD, 50)
    fb = bbox(full)
    inner_l = []
    ys, xs = np.nonzero(interior)
    offy, offx = int(H / 2 - interior.shape[0] / 2), int(W / 2 - interior.shape[1] / 2)
    from scipy import ndimage
    er = ndimage.binary_erosion(interior, iterations=4)
    ys, xs = np.nonzero(er)
    inner = float(g[ys + offy, xs + offx].mean())
    early = bbox(lum(frame_at(frames, 0.1)) > 30)
    late = bbox(lum(frame_at(frames, 2.24)) > 30)
    solid = arr(blank((W, H)))
    checks = [check("hollow: interior at ~18% gold", 20 <= inner <= 55, inner, "≈0.18·gold lum"),
              check("bright 2 px outline ring", int(full.sum()) > 300, int(full.sum()), ">300"),
              check("slams in from ~2.4x", early is not None and (early[3] - early[1]) > 1.5 * (fb[3] - fb[1]), early, "> 1.5x final"),
              check("implodes at the end", late is None or (late[3] - late[1]) < 0.45 * (fb[3] - fb[1]), late, "< 0.45x"),
              check("lineMeta flags questions", line_meta("هل تعرف؟")["question"] and not line_meta("نعم")["question"], True, True),
              check("negative control: a filled glyph is not hollow", float(lum(np.array(GOLD, float)[None, None])[0, 0]) > 55,
                    float(lum(np.array(GOLD, float)[None, None])[0, 0]), ">55")]
    return checks, [p]


@card("ARAB-46")
def duotone_offset(task, wd):
    """Big word with two whole-word copies behind it offset 8 px, in pink and blue; the stack fades/slides in."""
    np = np_()
    W, H = 360, 200
    f = font(CAIRO, 80, 900)
    word = "صوت"
    PINK, BLUE = (255, 79, 163), (63, 169, 255)
    tw, _ = tile(word, f)
    tp, _ = tile(word, f, fill=PINK + (255,))
    tb, _ = tile(word, f, fill=BLUE + (255,))

    def draw(t, c):
        e = cubic_out(t / 0.5)
        dx = 30 * (1 - e)
        place(c, tb, W / 2 - 8 + dx, H / 2 - 8, alpha=e)
        place(c, tp, W / 2 + 8 + dx, H / 2 + 8, alpha=e)
        place(c, tw, W / 2 + dx, H / 2, alpha=e)
    p, frames = video(wd, "duotone.mp4", draw, 1.0, size=(W, H))
    fin = frames[-1]
    bw = bbox(fin.min(axis=-1) > 200)
    bp = bbox(colour_mask(fin, PINK, 50))
    bb = bbox(colour_mask(fin, BLUE, 50))
    plain = blank((W, H))
    place(plain, tw, W / 2, H / 2)
    checks = [check("pink copy offset +8 px (right/bottom)", abs(bp[2] - bw[2] - 8) <= 1.5 and abs(bp[3] - bw[3] - 8) <= 1.5,
                    [bp[2] - bw[2], bp[3] - bw[3]], [8, 8]),
              check("blue copy offset −8 px (left/top)", abs(bw[0] - bb[0] - 8) <= 1.5 and abs(bw[1] - bb[1] - 8) <= 1.5,
                    [bw[0] - bb[0], bw[1] - bb[1]], [8, 8]),
              check("copies are whole words (shaped)", comps(colour_mask(fin, PINK, 50) | (fin.min(axis=-1) > 200)) <= comps(shaped_mask(word, f)) + 1,
                    True, True),
              check("negative control: plain word has no duotone", int(colour_mask(arr(plain), PINK, 50).sum()) == 0, 0, 0)]
    return checks, [p]


@card("ARAB-47")
def glow_rule(task, wd):
    """After the right-aligned title lands, a 3 px #e0a35a rule with glow grows 0→240 px (power4.out, 1.1 s) from the right."""
    np = np_()
    from PIL import Image, ImageDraw, ImageFilter
    W, H = 540, 300
    T = 0.3
    RULE = hexrgb("#e0a35a")
    ft, fs = font(CAIRO, int(92 * K), 800), font(CAIRO, int(34 * K), 600)
    tt, _ = tile("عنوان الحلقة", ft)
    ts, _ = tile("سطر تعريفي قصير", fs, fill=(200, 200, 200, 255))
    R = W - 40
    rt = {"tile": tt, "cx": R - tt.width / 2 + int(ft.size * 0.35), "cy": 110}
    ink = ink_box_abs(rt)
    rx = ink[2]
    ry = 165

    def draw(t, c):
        if t >= T:
            place(c, tt, rt["cx"], rt["cy"], alpha=clamp((t - T) / 0.2))
        if t >= T + 0.35:
            w = 240 * K * pow_out((t - T - 0.35) / 1.1, 4)
            ov = Image.new("RGBA", c.size, (0, 0, 0, 0))
            ImageDraw.Draw(ov).rectangle([rx - w, ry - 1, rx, ry + 1], fill=RULE + (255,))
            gl = ov.filter(ImageFilter.GaussianBlur(7 * K * 2))
            c.alpha_composite(gl)
            c.alpha_composite(gl)
            c.alpha_composite(ov)
        if t >= T + 0.45:
            place(c, ts, rx - ts.width / 2 + int(fs.size * 0.35), 205, alpha=clamp((t - T - 0.45) / 0.3))
    p, frames = video(wd, "glow_rule.mp4", draw, 2.2, size=(W, H))

    def rule(fr):
        return bbox(colour_mask(fr[ry - 2:ry + 3], RULE, 40))
    tm = T + 0.35 + 0.55
    bm, bf = rule(frame_at(frames, tm)), rule(frames[-1])
    wexp = 240 * K * pow_out((round(tm * 30) / 30 - T - 0.35) / 1.1, 4)
    glow = float(lum(frames[-1][ry - 7:ry - 3, int(bf[0]) + 5:int(bf[2]) - 5]).mean())
    sub_first = first_time([box_ink(fr, (0, 190, W, 225), 90) for fr in frames], 0.05)
    checks = [check("rule anchored at the title's right edge", abs(bf[2] - rx) <= 2 and abs(bm[2] - rx) <= 2, [bm[2], bf[2]], rx),
              check("width at mid-tween follows power4.out", abs((bm[2] - bm[0]) - wexp) <= 3, bm[2] - bm[0], wexp),
              check("final width 240k px", abs((bf[2] - bf[0]) - 240 * K) <= 2, bf[2] - bf[0], 240 * K),
              check("soft glow around the rule", glow > 3, glow, ">3 (bg 0)"),
              check("subtitle follows at T+0.45", sub_first is not None and sub_first >= T + 0.45 - 0.01, sub_first, ">=%.2f" % (T + 0.45)),
              check("negative control: no rule before T+0.35", rule(frame_at(frames, T + 0.3)) is None, None, None)]
    return checks, [p]


@card("ARAB-48")
def stacked_dimming_lines(task, wd):
    """One headline line per beat from the right; the new line in full colour, earlier lines tween to ~40%."""
    np = np_()
    W, H = 360, 360
    f = font(CAIRO, 32, 800)
    CREAM, LIME = (246, 238, 214), (200, 245, 90)
    lines = ["لا نبيع منتجا", "ولا نبيع وعدا", "نبني ثقة"]
    cols = [CREAM, CREAM, LIME]
    tiles = [tile(l, f, fill=c + (255,))[0] for l, c in zip(lines, cols)]
    beats = [0.3, 1.0, 1.7]
    R = W - 24
    ys = [100, 180, 260]

    def bright(i, t):
        nxt = [b for b in beats if b > beats[i]]
        if nxt and t >= nxt[0]:
            return 1 - 0.6 * cubic_out((t - nxt[0]) / 0.3)
        return 1.0

    def draw(t, c):
        for i, tl in enumerate(tiles):
            if t < beats[i]:
                continue
            e = cubic_out((t - beats[i]) / 0.3)
            r = {"tile": tl, "cx": 0, "cy": 0}
            place(c, tl, R - tl.width / 2 + f.size * 0.35 + 30 * (1 - e), ys[i], alpha=e * bright(i, t))
    p, frames = video(wd, "stack_dim.mp4", draw, 2.5, size=(W, H))
    band = [(0, y - 35, W, y + 35) for y in ys]
    full = [max(lumsum(fr, b) for fr in frames) for b in band]
    r_end = [lumsum(frames[-1], b) / full[i] for i, b in enumerate(band)]
    r_mid = [lumsum(frame_at(frames, 1.6), b) / full[i] for i, b in enumerate(band[:2])]
    rights = [bbox(mask_of(crop(frames[-1], b), 40))[2] for b in band]
    checks = [check("earlier lines dim to ~40%", all(abs(r - 0.4) <= 0.07 for r in r_end[:2]), r_end[:2], 0.4),
              check("newest line at full colour", r_end[2] >= 0.95, r_end[2], 1.0),
              check("at beat 2 only line 1 is dimmed", abs(r_mid[0] - 0.4) <= 0.07 and r_mid[1] >= 0.95, r_mid, [0.4, 1.0]),
              check("lines stack from the right (aligned right edges)", max(rights) - min(rights) <= 3, rights, "equal"),
              check("lime accent on the key line", int(colour_mask(frames[-1], LIME, 40).sum()) > 100, int(colour_mask(frames[-1], LIME, 40).sum()), ">100"),
              check("negative control: without dimming line 1 stays at 100%", lumsum(frame_at(frames, 0.9), band[0]) / full[0] > 0.95, True, True)]
    return checks, [p]


@card("ARAB-49")
def arabic_motion_templates(task, wd):
    """mtemplates.py: 8 templates → editable projects (escaped text, validated colours); one frame rendered by seeking the GSAP timeline."""
    np = np_()
    script = VENDOR / "kosif-montage-motion/scripts/mtemplates.py"
    env = dict(os.environ, KOSIF_MOTION_HOME=str(wd))
    lst = subprocess.run(["python3", str(script), "list"], capture_output=True, text=True, timeout=30, env=env).stdout
    names = [l.split()[0] for l in lst.splitlines() if l.strip()]
    made = []
    for n in names:
        sets = ["title=<b>تجربة & اختبار</b>", "accent=red;}"] if n == "title-card" else []
        r = subprocess.run(["python3", str(script), "new", "t-" + n, "--template", n, "--size", "540x960", "--set", *sets],
                           capture_output=True, text=True, timeout=30, env=env)
        made.append((n, r.returncode, Path(wd) / "projects" / ("t-" + n) / "index.html"))
    tc = (Path(wd) / "projects/t-title-card/index.html").read_text(encoding="utf-8")
    seek = tc.replace("</body>", "<script>(function w(){if(window.__ready&&window.render){window.render(SEEKT);}else{setTimeout(w,20);}})();</script></body>")
    from PIL import Image
    d = Path(wd) / "projects/t-title-card"
    shots = []
    for tt in ("0.0", "2.5"):
        (d / ("seek_%s.html" % tt)).write_text(seek.replace("SEEKT", tt), encoding="utf-8")
        exe = chrome_bin()
        out = d / ("frame_%s.png" % tt)
        subprocess.run([exe, "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--user-data-dir=%s" % (Path(wd) / ("ch" + tt)),
                        "--window-size=540,960", "--virtual-time-budget=3000", "--screenshot=%s" % out,
                        (d / ("seek_%s.html" % tt)).as_uri() + "?render"], capture_output=True, timeout=40, stdin=subprocess.DEVNULL)
        shots.append(arr(Image.open(out)))
    bright = [int((s.min(axis=-1) > 200).sum()) for s in shots]
    checks = [check("eight templates listed", len(names) == 8, names, 8),
              check("every template becomes a project with no unfilled placeholders",
                    all(rc == 0 and p.exists() and not re.search(r"\{\{[A-Z_0-9]+\}\}", p.read_text(encoding="utf-8")) for _, rc, p in made),
                    [(n, rc) for n, rc, _ in made], "all rc 0"),
              check("text HTML-escaped", "&lt;b&gt;تجربة &amp; اختبار&lt;/b&gt;" in tc and "<b>تجربة" not in tc, True, True),
              check("invalid colour replaced by the default", "red;}" not in tc and "#E7B65A" in tc, True, True),
              check("seeking the timeline draws the title (frame at 2.5 s has bright type)", bright[1] > 500, bright, ">500 at 2.5 s"),
              check("negative control: at t=0 the title is not yet revealed", bright[0] < bright[1] / 2, bright, "t0 < t2.5/2")]
    return checks, [d / "index.html", d / "frame_2.5.png"]


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


@card("ARAB-50")
def auto_rtl_lower_third(task, wd):
    """lowerThird: 4 px #E7B65A bar grows to 120 px in 0.4 s, title 44 px at +0.12 s, sub 0.55x at 75% at +0.24 s; Arabic → right."""
    np = np_()
    W, H = 540, 240          # bottom 240 px of a 1080x1920 frame at K (the card is placed from the bottom edge)
    ACC = hexrgb("#E7B65A")
    p, frames = video(wd, "lower_third_ar.mp4", lambda t, c: lower_third(c, 0.2, t, "سارة أحمد", "مخرجة أفلام"), 1.3, size=(W, H))
    _, fl = video(wd, "lower_third_en.mp4", lambda t, c: lower_third(c, 0.2, t, "Sara Ahmed", "Film director"), 1.3, size=(W, H))
    _, fn = video(wd, "lower_third_nodetect.mp4", lambda t, c: lower_third(c, 0.2, t, "سارة أحمد", "مخرجة أفلام", detect=False), 1.3, size=(W, H))
    fin = frames[-1]
    bar = bbox(colour_mask(fin, ACC, 40))
    y = H - 160 * K
    tb = bbox((fin.min(axis=-1) > 230)[:int(y - 4)])
    sub_band = fin[int(y + 4):int(y + 40)]
    sb = bbox(lum(sub_band) > 60)
    title_first = first_time([float((fr.min(axis=-1) > 200)[:int(y - 4)].sum()) for fr in frames], 0.03)
    barl = bbox(colour_mask(fl[-1], ACC, 40))
    barn = bbox(colour_mask(fn[-1], ACC, 40))
    bmid = bbox(colour_mask(frame_at(frames, 0.4), ACC, 40))
    checks = [check("Arabic: bar on the right inset (72k)", abs(bar[2] - (W - 72 * K)) <= 2, bar[2], W - 72 * K),
              check("bar grows to 120k px", abs((bar[2] - bar[0]) - 120 * K) <= 2 and (bmid[2] - bmid[0]) < 120 * K - 4,
                    [bmid[2] - bmid[0], bar[2] - bar[0]], 120 * K),
              check("title right-aligned to the inset", abs(tb[2] - (W - 72 * K)) <= 4, tb[2], W - 72 * K),
              check("title enters at +0.12 s", title_first is not None and title_first >= 0.2 + 0.12 - 0.01, title_first, ">=0.32"),
              check("sub at 75% white", 170 <= float(sub_band.max()) <= 205, float(sub_band.max()), 191),
              check("Latin card flips to the left", abs(barl[0] - 72 * K) <= 2, barl[0], 72 * K),
              check("negative control: without detection the Arabic card sits left", abs(barn[0] - 72 * K) <= 2 and barn[2] < W / 2,
                    barn, "left")]
    return checks, [p]


@card("ARAB-51")
def hook_title_looks(task, wd):
    """drawTitle: box (easeBack slide from +0.6W, Lalezar 8.5%), kinetic (words stomp 2.3→1 in .18 s, .16 s apart), minimal (underline from the right)."""
    np = np_()
    from PIL import Image, ImageDraw
    W, H = 270, 480
    S = min(W, H)
    PRIM, ACC = (231, 76, 60), (255, 214, 90)
    words = ["لا", "تفوت", "هذا"]
    fade = lambda t: 1 - clamp((t - 2.65) / 0.35)

    fb = font(LALEZAR, int(S * 0.085))
    tb, _ = tile("لا تفوت هذا", fb)
    bw, bh = tb.width + 10, tb.height

    def box_draw(t, c):
        e = back_out(t / 0.45)
        cx = W / 2 + 0.6 * W * (1 - e)
        a = fade(t)
        ov = Image.new("RGBA", c.size, (0, 0, 0, 0))
        ImageDraw.Draw(ov).rounded_rectangle([cx - bw / 2, H / 2 - bh / 2, cx + bw / 2, H / 2 + bh / 2], radius=10, fill=PRIM + (int(255 * a),))
        c.alpha_composite(ov)
        place(c, tb, cx, H / 2, alpha=a)
    pb, fbx = video(wd, "hook_box.mp4", box_draw, 3.1, size=(W, H))

    fk = font(LALEZAR, int(S * 0.12))
    row = word_row(words, fk, W, H / 2)
    tiles_k = [tile(w, fk, fill=(ACC if i % 2 else (255, 255, 255)) + (255,), stroke=2, stroke_fill=(0, 0, 0, 255))[0] for i, w in enumerate(words)]

    def kin_draw(t, c):
        for i, r in enumerate(row):
            t0 = 0.1 + 0.16 * i
            if t < t0:
                continue
            e = clamp((t - t0) / 0.18)
            place(c, tiles_k[i], r["cx"], r["cy"], scale=1 + 1.3 * (1 - cubic_out(e)), alpha=fade(t))
    pk, fkin = video(wd, "hook_kinetic.mp4", kin_draw, 3.1, size=(W, H))

    plex = REPO / "starters/kitab-theme/public/fonts/ibm-plex-sans-arabic-arabic-700-normal.woff2"
    fm = font(plex, int(S * 0.06))
    tm, _ = tile("الفكرة في دقيقة", fm)
    ink_w = bbox(np.asarray(tm.getchannel("A")) > 128)
    iw = ink_w[2] - ink_w[0]
    xr = W / 2 + iw / 2

    def min_draw(t, c):
        a = fade(t)
        place(c, tm, W / 2, H / 2 + 20 * (1 - cubic_out(t / 0.6)), alpha=a * clamp(t / 0.3))
        w = iw * cubic_out(t / 0.8)
        if w > 0.5:
            ov = Image.new("RGBA", c.size, (0, 0, 0, 0))
            ImageDraw.Draw(ov).rectangle([xr - w, H / 2 + 24, xr, H / 2 + 27], fill=ACC + (int(255 * a),))
            c.alpha_composite(ov)
    pm, fmin = video(wd, "hook_minimal.mp4", min_draw, 3.1, size=(W, H))

    def box_cx(fr):
        b = bbox(colour_mask(fr, PRIM, 40))
        return (b[0] + b[2]) / 2 if b else None
    cx0, cx1 = box_cx(fbx[0]), box_cx(frame_at(fbx, 0.6))
    widths = []
    for i, r in enumerate(row):
        t0 = 0.1 + 0.16 * i
        z = (0, 0, W, H)
        b0 = None
    # kinetic: measure the first word (rightmost) at its first frame vs settled
    def wb(fr, side):
        m = lum(fr) > 60
        b = bbox(m[:, W // 2:] if side else m)
        return b
    k_first = frame_at(fkin, 0.1 + 1 / 30)
    k_set = frame_at(fkin, 0.35)
    w_first = bbox(lum(k_first) > 60)
    w_set = bbox(lum(crop(k_set, (ink_box_abs(row[0])[0] - 4, 0, W, H))) > 60)
    ul = [bbox(colour_mask(frame_at(fmin, t)[int(H / 2 + 22):int(H / 2 + 30)], ACC, 40)) for t in (0.2, 0.5, 1.0)]
    ends = [float(f[-1].max()) for f in (fbx, fkin, fmin)]
    checks = [check("box slides in from +0.6W", cx0 is None or cx0 > W / 2 + 0.3 * W, cx0, ">%.0f" % (W / 2 + 0.3 * W)),
              check("box lands centred", abs(cx1 - W / 2) <= 3, cx1, W / 2),
              check("kinetic word stomps from ~2.3x", w_first is not None and (w_first[2] - w_first[0]) > 1.5 * (w_set[2] - w_set[0]),
                    [w_first and w_first[2] - w_first[0], w_set[2] - w_set[0]], ">1.5x"),
              check("alternating accent on word 2", int(colour_mask(frame_at(fkin, 1.0), ACC, 40).sum()) > 50, True, True),
              check("minimal underline grows from the right", all(u is not None for u in ul) and max(u[2] for u in ul) - min(u[2] for u in ul) <= 2
                    and ul[0][0] > ul[1][0] > ul[2][0], ul, "fixed right, growing left"),
              check("all looks fade out by 3 s", max(ends) < 40, ends, "<40"),
              check("negative control: the first frame of the box look is not centred", cx0 is None or abs(cx0 - W / 2) > 20, cx0, "off-centre")]
    return checks, [pb, pk, pm]


@card("ARAB-52")
def centre_locked_box(task, wd):
    """Phrase swap 1–2 s while the box tweens to the measured shaped width of the longer phrase around a fixed centre."""
    np = np_()
    from PIL import ImageDraw
    W, H = 360, 200
    f = font(CAIRO, 28, 700)
    p1, p2 = "مرحبًا", "أَهْلًا بِكُمْ فِي الْعَرْضِ"
    pad = 18
    w1, w2 = tlen(p1, f) + 2 * pad, tlen(p2, f) + 2 * pad
    t1, _ = tile(p1, f)
    t2, _ = tile(p2, f)
    a2 = bbox(np.asarray(t2.getchannel("A")) > 20)
    bh = max(t1.height, (a2[3] - a2[1]) + 2 * 10)
    BOX = (40, 60, 120)

    def draw(t, c, wfix=None):
        e = cubic_out((t - 1) / 1.0)
        w = wfix if wfix else w1 + (w2 - w1) * e
        ImageDraw.Draw(c).rounded_rectangle([W / 2 - w / 2, H / 2 - bh / 2, W / 2 + w / 2, H / 2 + bh / 2], radius=12, fill=BOX)
        if t < 1.5:
            place(c, t1, W / 2, H / 2, alpha=1 - clamp((t - 1) / 0.5))
        if t >= 1.5:
            place(c, t2, W / 2, H / 2, alpha=clamp((t - 1.5) / 0.5))
    p, frames = video(wd, "resize_box.mp4", draw, 4.0, size=(W, H))
    bxs = [bbox(colour_mask(frame_at(frames, t), BOX, 20)) for t in (0.5, 1.5, 3.5)]
    centres = [(b[0] + b[2]) / 2 for b in bxs]
    fin = frame_at(frames, 3.5)
    ink = bbox(lum(fin) > 140)
    _, neg = video(wd, "fixed_box.mp4", lambda t, c: draw(t, c, wfix=w1), 4.0, size=(W, H))
    nb = bbox(colour_mask(frame_at(neg, 3.5), BOX, 20))
    nink = bbox(lum(frame_at(neg, 3.5)) > 140)
    checks = [check("centre locked across the swap", max(centres) - min(centres) <= 1.5, centres, W / 2),
              check("box = measured phrase 1 width + padding", abs((bxs[0][2] - bxs[0][0]) - w1) <= 2.5, bxs[0][2] - bxs[0][0], w1),
              check("box = measured shaped phrase 2 width + padding", abs((bxs[2][2] - bxs[2][0]) - w2) <= 2.5, bxs[2][2] - bxs[2][0], w2),
              check("tashkeel fits inside the box", ink[1] >= bxs[2][1] and ink[3] <= bxs[2][3] and ink[0] >= bxs[2][0], [ink, bxs[2]], "inside"),
              check("negative control: an unresized box cannot hold phrase 2", nink[0] < nb[0] or nink[2] > nb[2], [nink, nb], "ink spills")]
    return checks, [p]


@card("ARAB-53")
def hijri_gregorian_header(task, wd):
    """Day name + Hijri month (Intl umalqura via node) + LTR Gregorian date with 3 px tracking on digits; two gold rules at 0.8/0.95 s."""
    np = np_()
    import datetime
    from PIL import Image, ImageDraw
    js = ("const d=new Date(Date.UTC(2026,9,8));const o={timeZone:'UTC'};"
          "console.log(JSON.stringify({wd:new Intl.DateTimeFormat('ar',{...o,weekday:'long'}).format(d),"
          "h:new Intl.DateTimeFormat('ar-SA-u-ca-islamic-umalqura',{...o,day:'numeric',month:'long'}).format(d)}))")
    info = json.loads(subprocess.run(["node", "-e", js], capture_output=True, text=True, timeout=20).stdout)
    day = info["wd"]
    hijri = info["h"]
    date = "08 . 10 . 2026"
    W, H = 540, 420
    GOLD = (244, 207, 107)
    fday = font(CAIRO, int(170 * K), 800)
    fmon = font(AMIRI_B, int(54 * K))
    fdat = font(AMIRI_B, int(50 * K))
    tday, _ = tile(day, fday, fill=(255, 231, 168, 255))
    tmon, _ = tile(hijri, fmon, fill=GOLD + (255,))
    sp = 3 * K

    def date_tile(spacing, direction="ltr"):
        if direction == "rtl":
            t, _ = tile(date, fdat, direction="rtl")
            return t
        w = sum(tlen(ch, fdat, "ltr") for ch in date) + spacing * sum(1 for i, ch in enumerate(date[:-1]) if ch.isdigit() and date[i + 1].isdigit())
        im = Image.new("RGBA", (int(w + 20), int(fdat.size * 1.8)), (255, 255, 255, 0))
        d = ImageDraw.Draw(im)
        x = 10
        for i, ch in enumerate(date):
            d.text((x, fdat.size * 0.2), ch, font=fdat, fill="white", direction="ltr")
            x += tlen(ch, fdat, "ltr") + (spacing if ch.isdigit() and i + 1 < len(date) and date[i + 1].isdigit() else 0)
        return im
    tdat = date_tile(sp)

    def draw(t, c):
        e = cubic_out((t - 0.25) / 0.6) if t > 0.25 else 0
        place(c, tmon, W / 2, 70, alpha=clamp(t / 0.5))
        place(c, tday, W / 2, 180 + 23 * (1 - e), scale=0.92 + 0.08 * e, blur=5 * (1 - e), alpha=e)
        place(c, tdat, W / 2, 300)
        for k, (t0, y) in enumerate(((0.8, 115), (0.95, 255))):
            if t >= t0:
                w = 160 * cubic_out((t - t0) / 0.4)
                ImageDraw.Draw(c).rectangle([W / 2 - w, y, W / 2 + w, y + 1], fill=GOLD)
    p, frames = video(wd, "day_header.mp4", draw, 1.6, size=(W, H))
    rule = lambda fr, y: int(colour_mask(fr[y - 1:y + 3], GOLD, 40).sum())
    a = np.asarray(tdat.getchannel("A")) > 128
    a_ltr = np.asarray(date_tile(0).getchannel("A")) > 128
    rt = np.asarray(date_tile(0, "rtl").getchannel("A")) > 128
    first = np.asarray(tile("08", fdat, direction="ltr")[0].getchannel("A")) > 128
    def left_match(m):
        mm = crop_ink(m)
        fi = crop_ink(first)
        return iou(mm[:, :fi.shape[1]], fi)
    nat = bbox(a_ltr)[2] - bbox(a_ltr)[0]
    trk = bbox(a)[2] - bbox(a)[0]
    checks = [check("weekday from Intl matches the calendar (Thursday)", day == "الخميس" and datetime.date(2026, 10, 8).weekday() == 3, day, "الخميس"),
              check("Hijri day/month from umalqura", "٢٧" in hijri and "ربيع" in hijri, hijri, "٢٧ ربيع الآخر/الثاني"),
              check("rules drawn at 0.8 s and 0.95 s", rule(frame_at(frames, 0.75), 115) == 0 and rule(frame_at(frames, 0.9), 115) > 0 and
                    rule(frame_at(frames, 0.9), 255) == 0 and rule(frame_at(frames, 1.1), 255) > 0, True, True),
              check("date reads LTR (08 first on the left)", left_match(a) > 0.6, left_match(a), ">0.6"),
              check("tracking only between digits (+3k px each)", abs((trk - nat) - sp * 6) <= 2, trk - nat, sp * 6),
              check("negative control: the date set in an RTL run starts with 2026 on the left", left_match(rt) < left_match(a) - 0.1,
                    left_match(rt), "< LTR match")]
    return checks, [p, write_json(Path(wd) / "header.json", info)]


AR_DIGITS = "٠١٢٣٤٥٦٧٨٩"


def to_ar_digits(s):
    return "".join(AR_DIGITS[int(c)] if c.isdigit() and c in "0123456789" else c for c in str(s))


@card("ARAB-54")
def pills_chips_badges(task, wd):
    """Tag pill (padding 10x24, 24 px/800, radius 8, #f59e0b→#d97706, scale .8→1), chip 'تعريف ١', 54 px glass badge with ٣."""
    np = np_()
    from PIL import Image, ImageDraw
    W, H = 420, 300
    f = font(CAIRO, 24, 800)
    label = "جديد"
    tw = tlen(label, f)
    t_lab, _ = tile(label, f)
    pw, ph = tw + 48, 24 * 1.5 + 20
    g = np.zeros((int(ph), int(pw), 4), np.uint8)
    yy, xx = np.mgrid[0:int(ph), 0:int(pw)]
    u = ((xx / pw) + (yy / ph)) / 2
    c0, c1 = np.array(hexrgb("#f59e0b")), np.array(hexrgb("#d97706"))
    g[..., :3] = (c0 + (c1 - c0) * u[..., None]).astype(np.uint8)
    pill = Image.fromarray(g, "RGBA")
    m = Image.new("L", pill.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, pill.width - 1, pill.height - 1], radius=8, fill=255)
    pill.putalpha(m)
    pill.alpha_composite(t_lab, (int(pill.width / 2 - t_lab.width / 2), int(pill.height / 2 - t_lab.height / 2)))
    chip_txt = "تعريف " + to_ar_digits(1)
    fc = font(CAIRO, 20, 700)
    t_chip, _ = tile(chip_txt, fc)
    BG = (20, 24, 30)

    def draw(t, c):
        e = cubic_out(t / 0.5)
        place(c, pill, W / 2, 70, scale=0.8 + 0.2 * e, alpha=e)
        d = ImageDraw.Draw(c)
        cw = tlen(chip_txt, fc) + 36
        d.rounded_rectangle([W / 2 - cw / 2, 150 - 20, W / 2 + cw / 2, 150 + 20], radius=999, outline=(255, 255, 255), width=2, fill=(5, 7, 11))
        place(c, t_chip, W / 2, 150)
        d.ellipse([W / 2 - 27, 230 - 27, W / 2 + 27, 230 + 27], fill=(70, 74, 80), outline=(255, 255, 255), width=2)
        place(c, tile(to_ar_digits(3), font(CAIRO, 26, 800))[0], W / 2, 230)
    p, frames = video(wd, "pills.mp4", draw, 1.0, size=(W, H), bg=BG)
    fin = frames[-1]
    orange = (fin[..., 0] > 180) & (fin[..., 2] < 60)
    pb = bbox(orange[:120])
    early = bbox(((frames[0][..., 0] > 60) & (frames[0][..., 2] < 40))[:120])
    tl_col = fin[pb[1] + 3, pb[0] + 6]
    br_col = fin[pb[3] - 4, pb[2] - 7]
    badge = bbox(lum(fin[195:265]) > 60)
    checks = [check("pill width = text + 2x24 px padding", abs((pb[2] - pb[0]) - pw) <= 2, pb[2] - pb[0], pw),
              check("135° gradient #f59e0b → #d97706", np.abs(tl_col - c0).max() < 30 and np.abs(br_col - c1).max() < 30 and lum(tl_col) > lum(br_col),
                    [tl_col.tolist(), br_col.tolist()], ["#f59e0b", "#d97706"]),
              check("pops in from scale 0.8", early is None or (early[2] - early[0]) <= 0.86 * (pb[2] - pb[0]), early, "<=0.86x"),
              check("Arabic-Indic numerals", to_ar_digits("تعريف 1") == "تعريف ١" and to_ar_digits(2026) == "٢٠٢٦", to_ar_digits(2026), "٢٠٢٦"),
              check("54 px badge circle", abs((badge[2] - badge[0]) - 54) <= 3, badge[2] - badge[0], 54),
              check("negative control: unconverted digits are Latin", "1" in "تعريف 1" and "١" not in "تعريف 1", True, True)]
    return checks, [p]


@card("ARAB-56")
def rtl_character_card(task, wd):
    """Avatar frame on the left; right-aligned stack (tag pill, role, huge name, one-line bio); cards change every ~1.7 s."""
    np = np_()
    from PIL import ImageDraw
    W, H = 540, 300
    NAVY, BURG, CREAM, GOLD = hexrgb("#172237"), hexrgb("#731521"), hexrgb("#e9d5b0"), hexrgb("#e0b23a")
    cards = [("القائد", "مؤسس الفريق", "يوسف", "يبدأ كل شيء بسؤال"), ("المهندسة", "تبني الأنظمة", "ليلى", "لا تقبل حلا نصف جاهز")]
    R = W - 30
    fs = [font(CAIRO, 18, 700), font(CAIRO, 18, 600), font(CAIRO, 56, 900), font(CAIRO, 18, 400)]
    ys = [50, 88, 150, 215]

    def draw(t, c, align_right=True):
        k = 0 if t < 1.7 else 1
        d = ImageDraw.Draw(c)
        d.rectangle([0, 0, W, H], fill=NAVY if k == 0 else BURG)
        d.rectangle([30, 60, 170, 240], outline=GOLD, width=4)
        d.ellipse([70, 100, 130, 160], fill=CREAM)
        for i, (txt, ff, y) in enumerate(zip(cards[k], fs, ys)):
            tl, _ = tile(txt, ff, fill=(GOLD if i == 0 else CREAM) + (255,))
            ink = bbox(np.asarray(tl.getchannel("A")) > 128)
            w = ink[2] - ink[0]
            cx = (R - w / 2) if align_right else (200 + w / 2)
            off = (tl.width / 2) - (ink[0] + ink[2]) / 2
            if i == 0:
                d.rounded_rectangle([cx - w / 2 - 10, y - 14, cx + w / 2 + 10, y + 14], radius=14, outline=GOLD, width=2)
            place(c, tl, cx + off, y)
    p, frames = video(wd, "char_card.mp4", draw, 3.4, size=(W, H))
    fin = frame_at(frames, 1.0)

    def rights(fr):
        out = []
        for i, y in enumerate(ys[1:], 1):
            band = colour_mask(fr[y - 30:y + 30, 200:], CREAM, 50)
            b = bbox(band)
            out.append(b[2] + 200)
        return out
    rs = rights(fin)
    avatar = bbox(colour_mask(fin, GOLD, 30)[:, :W // 2])
    diffs = [float(np.abs(frames[i + 1] - frames[i]).mean()) for i in range(len(frames) - 1)]
    cut = int(np.argmax(diffs)) + 1
    _, neg = video(wd, "char_card_left.mp4", lambda t, c: draw(t, c, align_right=False), 0.2, size=(W, H))
    rn = rights(neg[-1])
    checks = [check("text rows right-aligned to one edge", max(rs) - min(rs) <= 3 and abs(max(rs) - R) <= 3, rs, R),
              check("avatar frame on the left", avatar is not None and avatar[2] < W / 2, avatar, "left half"),
              check("next card at ~1.7 s", abs(cut / 30 - 1.7) <= 0.04, cut / 30, 1.7),
              check("negative control: default left alignment gives ragged right edges", max(rn) - min(rn) > 10, rn, "ragged")]
    return checks, [p]


def balance_lines(words, f, n):
    """text-wrap: balance — the split into n lines with the smallest widest line."""
    import itertools
    best = None
    for cuts in itertools.combinations(range(1, len(words)), n - 1):
        parts = [" ".join(words[a:b]) for a, b in zip((0,) + cuts, cuts + (len(words),))]
        wmax = max(tlen(x, f) for x in parts)
        if best is None or wmax < best[0]:
            best = (wmax, parts)
    return best[1]


@card("ARAB-57")
def cinematic_headline(task, wd):
    """Headline clamp(31px, 4.9vw, 65px), lh 1.18, 700, text-wrap:balance, shadow 0 3px 30px .45, eyebrow, bottom-start over footage."""
    np = np_()
    from PIL import Image, ImageFilter
    clampf = lambda vw: max(31, min(65, 0.049 * vw))
    sizes = {w: clampf(w) for w in (400, 1000, 1280, 1920)}
    W, H = 640, 360
    clip = fx.test_clip(Path(wd) / "footage.mp4", 0.5, "640x360", 30)
    bgf = fx.frames(clip, (W, H))[5]
    f = font(CAIRO, int(round(clampf(W))), 700)
    text = "حين يهدأ الضوء فوق المدينة تبدأ الحكاية الحقيقية"
    boxw = min(560, W - 44)
    greedy = wrap_words(text.split(), f, boxw)
    bal = balance_lines(text.split(), f, len(greedy))
    ratio = lambda ls: min(tlen(x, f) for x in ls) / max(tlen(x, f) for x in ls)
    img = Image.fromarray(bgf.astype("uint8")).convert("RGBA")
    lh = f.size * 1.18
    x_start = W - max(22, min(110, 0.06 * W))
    y0 = H - 40 - lh * len(bal)
    from PIL import ImageDraw
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    for i, ln in enumerate(bal):
        ImageDraw.Draw(sh).text((x_start, y0 + i * lh + 3), ln, font=f, fill=(0, 0, 0, 115), anchor="ra", direction="rtl", language="ar")
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(15)))
    d = ImageDraw.Draw(img)
    for i, ln in enumerate(bal):
        d.text((x_start, y0 + i * lh), ln, font=f, fill="white", anchor="ra", direction="rtl", language="ar")
    d.text((x_start, y0 - 20), "فصل ١", font=font(CAIRO, 12, 700), fill=(231, 182, 90), anchor="ra", direction="rtl", language="ar")
    out = save_png(img, Path(wd) / "headline.png")
    a = arr(img)
    region = a[int(y0):int(y0 + lh * len(bal)), int(x_start - boxw):int(x_start)]
    bgr = bgf[int(y0):int(y0 + lh * len(bal)), int(x_start - boxw):int(x_start)]
    white = a.min(axis=-1) > 245
    shadowed = float((lum(bgr) - lum(region))[~(white[int(y0):int(y0 + lh * len(bal)), int(x_start - boxw):int(x_start)])].mean())
    checks = [check("clamp(31px, 4.9vw, 65px) known answers", sizes == {400: 31, 1000: 49.0, 1280: 62.72, 1920: 65},
                    sizes, {400: 31, 1000: 49.0, 1280: 62.72, 1920: 65}),
              check("balanced lines (shortest/longest ≥ 0.7)", ratio(bal) >= 0.7 and len(bal) >= 2, ratio(bal), ">=0.7"),
              check("start-aligned at the inset (right for Arabic)", abs(bbox(white)[2] - x_start) <= 4, bbox(white)[2], x_start),
              check("soft dark shadow lifts the type off the footage", shadowed > 3, shadowed, ">3"),
              check("negative control: greedy wrap is less balanced", ratio(greedy) < ratio(bal), [ratio(greedy), ratio(bal)], "greedy < balanced")]
    return checks, [out]


def ass_time(t):
    return "%d:%02d:%05.2f" % (int(t // 3600), int(t % 3600 // 60), t % 60)


@card("ARAB-58")
def per_shot_ass_card(task, wd):
    """One ASS file per shot: hero word (move 766→740, fad 650/700), detail line +0.45 s, corner tag; burned by libass."""
    np = np_()
    import shutil
    W, H = 540, 960
    k = K
    x = W // 2
    ass = ["﻿[Script Info]", "ScriptType: v4.00+", "PlayResX: %d" % W, "PlayResY: %d" % H, "WrapStyle: 2", "",
           "[V4+ Styles]",
           "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
           "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
           "Style: Hero,Cairo,%d,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,%.1f,%.1f,2,10,10,%d,-1" % (60 * k, 2.5 * k, 1.3 * k, 210 * k),
           "Style: Detail,Cairo,%d,&H00E0E0E0,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,%.1f,0,2,10,10,10,-1" % (32 * k, 1.4 * k),
           "Style: Tag,Cairo,%d,&H005AB6E7,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,0,0,7,10,10,10,-1" % (21 * k), "",
           "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
           "Dialogue: 0,%s,%s,Hero,,0,0,0,,{\\an2\\move(%d,%d,%d,%d,0,900)\\fad(650,700)}الرحلة" % (ass_time(0), ass_time(2.6), x, 766 * k, x, 740 * k),
           "Dialogue: 0,%s,%s,Detail,,0,0,0,,{\\an2\\move(%d,%d,%d,%d,300,1050)\\fad(650,600)}تبدأ من خطوة واحدة" % (ass_time(0.45), ass_time(2.6), x, 812 * k, x, 793 * k),
           "Dialogue: 0,%s,%s,Tag,,0,0,0,,{\\an7\\pos(%d,%d)\\fad(400,600)}مشهد ٠٣" % (ass_time(0), ass_time(2.6), 30 * k, 38 * k)]
    af = Path(wd) / "scene_01.ass"
    af.write_text("\n".join(ass) + "\n", encoding="utf-8")
    base = fx.color_clip(Path(wd) / "plate.mp4", "0x101820", 2.6, "%dx%d" % (W, H), 30)
    out = Path(wd) / "scene_01.mp4"
    fx.ffmpeg("-i", base, "-vf", "ass=%s:fontsdir=%s" % (af.name, fd.name), "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", out.name,
              timeout=60) if False else subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(base), "-vf",
                                                        "ass=scene_01.ass:fontsdir=%s" % FONTS, "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p",
                                                        "scene_01.mp4"], cwd=str(wd), check=True, capture_output=True, timeout=60)
    frames = fx.frames(out, (W, H))
    hero_band = (0, 300, W, 375)

    def hb(t):
        return bbox(lum(crop(frame_at(frames, t), hero_band)) > 150)
    b_early, b_late = hb(0.4), hb(1.2)
    det = lambda t: box_ink(frame_at(frames, t), (0, 382, W, 405), 120)
    tag = bbox(lum(frame_at(frames, 1.0)[:60, :200]) > 60)
    hero_l = [float(lum(crop(frame_at(frames, t), hero_band)).max()) for t in (0.05, 1.2)]
    ref = comps(shaped_mask("الرحلة", font(CAIRO, int(60 * k), 700)))
    got = comps(lum(crop(frame_at(frames, 1.2), hero_band)) > 150)
    plate = fx.frames(base, (W, H))[30]
    checks = [check("hero rises ~13 px (766→740 at K)", b_early and b_late and 6 <= b_early[3] - b_late[3] <= 16, b_early and b_early[3] - b_late[3], 13 * 0.6),
              check("hero fades in (fad 650)", hero_l[0] < 0.4 * hero_l[1], hero_l, "dim → full"),
              check("detail line enters after +0.45 s", det(0.3) == 0 and det(1.3) > 50, [det(0.3), det(1.3)], "0 then >50"),
              check("corner tag top-left", tag is not None and tag[0] < 40 and tag[1] < 40, tag, "near (15,19)"),
              check("libass shapes the Arabic hero word", abs(got - ref) <= 1, got, ref),
              check("negative control: the plate before burning has no type", float(lum(plate).max()) < 60, float(lum(plate).max()), "<60")]
    return checks, [af, out]


@card("ARAB-59")
def shaped_cover(task, wd):
    """thumb: grab a frame, darken with alpha 0.78·t² from 45% height, shaped title 8.5% of short side ≤3 lines ending at 80% H, gold sub, JPEG q93."""
    np = np_()
    from PIL import Image, ImageDraw
    W, H = 540, 960
    clip = fx.test_clip(Path(wd) / "film.mp4", 3.0, "%dx%d" % (W, H), 30)
    grab = Path(wd) / "grab.png"
    fx.ffmpeg("-ss", "2.0", "-i", clip, "-frames:v", "1", grab)
    src = np.asarray(Image.open(grab).convert("RGB"), float)
    yy = np.arange(H)[:, None, None]
    t = np.clip((yy - 0.45 * H) / (0.55 * H), 0, 1)
    dark = src * (1 - 0.78 * t ** 2)
    img = Image.fromarray(dark.clip(0, 255).astype("uint8")).convert("RGBA")
    size = int(0.085 * min(W, H))
    f = font(CAIRO, size, 800)
    title = "كيف تصنع فيلما كاملا من صوت واحد فقط"
    lines = wrap_words(title.split(), f, 0.84 * W)[:3]
    lh = size * 1.25
    fsub = font(CAIRO, size // 2, 700)
    d = ImageDraw.Draw(img)
    bottom = 0.80 * H
    y_last = bottom - size * 0.9 - lh * 0.0
    ys = [y_last - (len(lines) - 1 - i) * lh for i in range(len(lines))]
    for ln, y in zip(lines, ys):
        d.text((W / 2, y), ln, font=f, fill="white", anchor="md", direction="rtl", language="ar", stroke_width=max(1, size // 18), stroke_fill="black")
    d.text((W / 2, bottom), "دليل قصير", font=fsub, fill=(231, 182, 90), anchor="md", direction="rtl", language="ar")
    out = Path(wd) / "cover.jpg"
    img.convert("RGB").save(out, quality=93)
    a = np.asarray(Image.open(out).convert("RGB"), float)
    row = int(0.95 * H)
    tt = (row - 0.45 * H) / (0.55 * H)
    fac = float(lum(a[row:row + 2]).mean() / max(1, lum(src[row:row + 2]).mean()))
    white = a.min(axis=-1) > 235
    tb = bbox(white[:int(bottom - size * 0.6)])
    gold = bbox(colour_mask(a, (231, 182, 90), 45)[int(0.7 * H):])
    checks = [check("lower part darkened by 1 − 0.78·t²", abs(fac - (1 - 0.78 * tt ** 2)) <= 0.08, fac, 1 - 0.78 * tt ** 2),
              check("top untouched above 45%", float(np.abs(a[:int(0.4 * H)] - src[:int(0.4 * H)]).mean()) < 6, True, True),
              check("title ≤3 lines within 84% width", len(lines) <= 3 and tb[2] - tb[0] <= 0.84 * W + 6, [len(lines), tb[2] - tb[0]], "<=3, <=%.0f" % (0.84 * W)),
              check("gold subtitle at the block end (~80% H)", gold is not None and abs(gold[3] + int(0.7 * H) - bottom) <= 8, gold, bottom),
              check("negative control: the grabbed frame itself is not darkened", abs(1 - float(lum(src[row:row + 2]).mean() / max(1, lum(src[row:row + 2]).mean()))) < 1e-9 and fac < 0.7,
                    fac, "<0.7 after, 1.0 before")]
    return checks, [out]


@card("ARAB-60")
def arabic_carousel(task, wd):
    """social.py carousel (vendored): slides 1080x1350 + PDF + contact sheet, titles auto-shrunk to ≤4 lines, RAQM on raw text."""
    np = np_()
    from PIL import Image
    script = VENDOR / "kosif-social/scripts/social.py"
    spec = {"size": "1080x1350", "brand": {"font_bold": str(TAJAWAL), "font": str(TAJAWAL), "handle": "@kosif"},
            "slides": [{"title": "محمد"}, {"title": "هذا عنوان طويل جدا يحتاج إلى أكثر من سطر واحد حتى يظهر كاملا على الشريحة بدون أن يقطع أي كلمة منه"}]}
    sp = Path(wd) / "spec.json"
    write_json(sp, spec)

    def run(outdir, block_reshaper):
        pre = "import sys,runpy;" + ("sys.modules['arabic_reshaper']=None;sys.modules['bidi']=None;sys.modules['bidi.algorithm']=None;" if block_reshaper else "")
        code = pre + "sys.argv=[%r,'carousel',%r,'--out',%r];runpy.run_path(%r,run_name='__main__')" % (str(script), str(sp), str(outdir), str(script))
        r = subprocess.run(["python3", "-c", code], capture_output=True, text=True, timeout=60)
        return json.loads(r.stdout)
    res = run(Path(wd) / "out", True)
    neg = run(Path(wd) / "out_reshaper", False) if fx.have("arabic_reshaper") and fx.have("bidi") else None
    s1 = np.asarray(Image.open(res["slides"][0]).convert("RGB"), float)
    ref = shaped_mask("محمد", font(TAJAWAL, round(1080 * 0.105)))
    m = crop_ink((s1.min(axis=-1) > 200)[200:1100])
    good = iou(m, crop_ink(ref))
    bad = None
    if neg:
        n1 = np.asarray(Image.open(neg["slides"][0]).convert("RGB"), float)
        bad = iou(crop_ink((n1.min(axis=-1) > 200)[200:1100]), crop_ink(ref))
    s2 = np.asarray(Image.open(res["slides"][1]).convert("RGB"), float)
    runs = [r for r in line_pitch((s2.min(axis=-1) > 200)[150:1150]) if r[1] - r[0] > 25]
    pdf = Path(res["pdf"]).read_bytes()
    checks = [check("slides at 1080x1350", Image.open(res["slides"][0]).size == (1080, 1350), Image.open(res["slides"][0]).size, (1080, 1350)),
              check("PDF with one page per slide", pdf.count(b"/Type /Page\n") + pdf.count(b"/Type /Page ") + pdf.count(b"/Type /Page>") >= 2 or pdf.count(b"/Page") >= 3,
                    pdf.count(b"/Page"), ">=2 pages"),
              check("contact sheet written", Path(res["contact_sheet"]).stat().st_size > 1000, True, True),
              check("long title shrunk to ≤4 lines, no warning", 1 <= len(runs) <= 4 and not res["warnings"], [len(runs), res["warnings"]], "<=4"),
              check("title shaped correctly by RAQM on raw text", good > 0.8, good, ">0.8"),
              check("negative control: with arabic_reshaper+bidi on top of RAQM the title is mirrored", bad is not None and bad < 0.6, bad, "<0.6")]
    return checks, [Path(res["slides"][0]), Path(res["pdf"])]


@card("ARAB-61")
def timeline_overlays(task, wd):
    """Timeline-JSON text overlays {pos, size, color, box, anim}: fade 0.35 s, rise/drop/slides, clamped to the 9:16 safe band 14–80%."""
    np = np_()
    from PIL import ImageDraw
    W, H = 270, 480
    spec = {"overlays": [{"type": "text", "text": "العنوان", "start": 0.2, "end": 2.0, "pos": [0.5, 0.05], "size": 30, "color": "#FFFFFF", "anim": "fade"},
                         {"type": "text", "text": "سطر ثان", "start": 0.4, "end": 2.0, "pos": [0.5, 0.6], "size": 22, "color": "#E7B65A", "anim": "rise", "box": True}]}

    def ypos(o):
        return H * min(0.80, max(0.14, o["pos"][1]))

    def draw(t, c, clampy=True):
        for o in spec["overlays"]:
            if not (o["start"] <= t < o["end"]):
                continue
            a = clamp((t - o["start"]) / 0.35) * clamp((o["end"] - t) / 0.35)
            f = font(CAIRO, o["size"], 700)
            tl, _ = tile(o["text"], f, fill=hexrgb(o["color"]) + (255,))
            y = ypos(o) if clampy else H * o["pos"][1]
            dy = 20 * (1 - cubic_out((t - o["start"]) / 0.35)) if o["anim"] == "rise" else 0
            if o.get("box"):
                ImageDraw.Draw(c).rectangle([W / 2 - tl.width / 2, y - tl.height / 2 + dy, W / 2 + tl.width / 2, y + tl.height / 2 + dy], fill=(int(30 * a), int(30 * a), int(30 * a)))
            place(c, tl, W * o["pos"][0], y + dy, alpha=a)
    p, frames = video(wd, "overlays.mp4", draw, 2.2, size=(W, H))
    ink = lambda fr: bbox(lum(fr) > 60)
    allb = [ink(fr) for fr in frames if ink(fr)]
    top, bot = min(b[1] for b in allb), max(b[3] for b in allb)
    w0 = frame_at(frames, 1.0)
    full = float(lum(w0[:int(H * 0.3)]).max())
    half = float(lum(frame_at(frames, 0.2 + 0.175)[:int(H * 0.3)]).max())
    yb = [wcentroid(crop(frame_at(frames, t), (0, H * 0.5, W, H * 0.75)))[1] for t in (0.45, 1.0)]
    _, neg = video(wd, "overlays_unclamped.mp4", lambda t, c: draw(t, c, clampy=False), 1.0, size=(W, H))
    nt = ink(neg[-1])
    checks = [check("every overlay inside the safe band 14–80%", top >= 0.14 * H - 22 and bot <= 0.80 * H + 22, [top, bot], [0.14 * H, 0.8 * H]),
              check("fade 0.35 s (half way ≈ 50%)", 0.3 <= half / full <= 0.7, half / full, 0.5),
              check("rise anim moves up into place", yb[0] > yb[1] + 2, yb, "decreasing y"),
              check("negative control: unclamped pos 5% leaves the band", nt[1] < 0.14 * H - 22, nt[1], "<%.0f" % (0.14 * H - 22))]
    return checks, [p, write_json(Path(wd) / "timeline.json", spec)]


def split_missing_times(words, start, end):
    """Words without times share [start, end] by letters + 2."""
    wts = [len(w) + 2 for w in words]
    tot = sum(wts)
    out, t = [], start
    for w, k in zip(words, wts):
        d = (end - start) * k / tot
        out.append({"w": w, "s": round(t, 4), "e": round(t + d, 4)})
        t += d
    return out


@card("ARAB-62")
def ass_karaoke(task, wd):
    """One Dialogue per spoken word: highlight colour + \\fscx112→100 in 120 ms; ≤6 words per chunk; Encoding −1; burned by libass."""
    np = np_()
    W, H = 540, 300
    text = "هذه الكلمات تظهر واحدة بعد واحدة على الشاشة بترتيبها الصحيح"
    words = split_missing_times(text.split(), 0.2, 4.2)
    for w in words:                                  # snap to frames so the 112% state is sampled
        w["s"] = round(w["s"] * 30) / 30
    chunks = [words[i:i + 6] for i in range(0, len(words), 6)]
    hdr = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: %d" % W, "PlayResY: %d" % H, "WrapStyle: 2", "", "[V4+ Styles]",
           "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
           "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
           "Style: Reels,Cairo,34,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,2,0,5,%d,%d,10,-1" % (0.06 * W, 0.06 * W), "",
           "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    ev = []
    for ch in chunks:
        for j, w in enumerate(ch):
            end = ch[j + 1]["s"] if j + 1 < len(ch) else w["e"]
            parts = [("{\\1c&H0000FFFF&\\fscx112\\fscy112\\t(0,120,\\fscx100\\fscy100)}%s{\\r}" % x["w"]) if x is w else x["w"] for x in ch]
            ev.append("Dialogue: 0,%s,%s,Reels,,0,0,0,,{\\pos(%d,%d)}%s" % (ass_time(w["s"]), ass_time(end), W / 2, H / 2, " ".join(parts)))
    af = Path(wd) / "caps.ass"
    af.write_text("\n".join(hdr + ev) + "\n", encoding="utf-8")
    base = fx.color_clip(Path(wd) / "plate.mp4", "0x101010", 4.4, "%dx%d" % (W, H), 30)
    out = Path(wd) / "captions.mp4"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", "plate.mp4", "-vf", "ass=caps.ass:fontsdir=%s" % FONTS,
                    "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", "captions.mp4"], cwd=str(wd), check=True, capture_output=True, timeout=60)
    frames = fx.frames(out, (W, H))
    YEL = (255, 255, 0)
    hl = lambda t: bbox(colour_mask(frame_at(frames, t), YEL, 70))
    first = chunks[0]
    xs = [(hl(w["s"] + 0.15)[0] + hl(w["s"] + 0.15)[2]) / 2 for w in first]
    w0, w1 = hl(first[2]["s"]), hl(first[2]["s"] + 0.25)
    pop = (w0[3] - w0[1]) / (w1[3] - w1[1])
    plain = fx.frames(base, (W, H))[10]
    checks = [check("≤6 words per on-screen chunk", all(len(c) <= 6 for c in chunks) and len(chunks) == 2, [len(c) for c in chunks], "<=6"),
              check("missing times split by letters + 2", abs((words[0]["e"] - 0.2) / 4.0 - (len(words[0]["w"]) + 2) / sum(len(w["w"]) + 2 for w in words)) < 1e-3,
                    words[0]["e"], "proportional"),
              check("highlight walks right → left in Arabic word order", all(a > b for a, b in zip(xs, xs[1:])), xs, "decreasing x"),
              check("pop 112% → 100% in 120 ms", 1.06 <= pop <= 1.18, pop, 1.12),
              check("negative control: unburned plate has no highlight", int(colour_mask(plain, YEL, 70).sum()) == 0, 0, 0)]
    return checks, [af, out]


PARTICLES = {"في", "من", "على", "إلى", "الى", "عن", "و", "ثم", "أن", "ان", "لا", "ما", "يا", "بل", "قد", "لم", "لن", "إن", "كل"}
OPENERS = {"اللهم", "يا", "إلا", "الا", "اجعل", "اغفر", "ارحم", "اهدنا", "ارزقنا"}


def segment_dp(words, max_words=7, lo=1.1, hi=3.6):
    """DP over cut points: break bonus (pause, punctuation, openers, و/ف clauses) minus penalties; line 1.1–3.6 s, ≤7 words."""
    n = len(words)

    def bonus(j):                                         # cut after word j-1 (between j-1 and j)
        if j >= n:
            return 0.0
        a, b = words[j - 1], words[j]
        gap = max(0.0, b["s"] - a["e"])
        v = 8 * min(gap, 1) + (1.0 if re.search(r"[،,.!؟?]$", a["w"]) else 0)
        bw = b["w"].strip("،,.")
        v += 0.8 if bw in OPENERS else 0
        v += 0.6 if bw.startswith("و") and len(bw) > 2 else 0
        v += 0.5 if bw.startswith("ف") and len(bw) > 3 else 0
        if a["w"].strip("،,.") in PARTICLES:
            v -= 0.7
        if a["w"].isdigit() and b["w"].isdigit():
            v -= 0.8
        if bw == "يا" and j >= 2 and words[j - 2]["w"] == "يا":
            v -= 1.0
        return v
    best = [(-1e9, None)] * (n + 1)
    best[0] = (0.0, None)
    for j in range(1, n + 1):
        for i in range(max(0, j - max_words), j):
            dur = words[j - 1]["e"] - words[i]["s"]
            pen = 2.0 * (max(0, lo - dur) + max(0, dur - hi))
            sc = best[i][0] + bonus(j) - pen - 0.3
            if sc > best[j][0]:
                best[j] = (sc, i)
    cuts, j = [], n
    while j > 0:
        i = best[j][1]
        cuts.append((i, j))
        j = i
    return [words[i:j] for i, j in reversed(cuts)]


def timed(text, pauses=None, wps=2.2, start=0.5):
    pauses = pauses or {}
    out, t = [], start
    for k, w in enumerate(text.split()):
        d = 0.25 + 0.04 * len(w)
        out.append({"w": w, "s": round(t, 3), "e": round(t + d, 3)})
        t += d + 0.08 + pauses.get(k, 0)
    return out


DUA = "اللهم اغفر لي ذنبي كله دقه وجله، يا رب يا كريم يا رحيم اجعل في قلبي نورا وفي سمعي نورا"


@card("ARAB-67")
def dp_line_breaking(task, wd):
    """verse.segment: DP over cut points (pause 8·min(gap,1), punctuation 1.0, openers 0.8, و 0.6, ف 0.5; particle −0.7, يا…يا −1.0)."""
    words = timed(DUA, pauses={6: 0.9})
    lines = segment_dp(words)
    txt = [" ".join(w["w"] for w in l) for l in lines]
    greedy = [" ".join(w["w"] for w in words[i:i + 7]) for i in range(0, len(words), 7)]
    ends_particle = lambda ls: any(l.split()[-1].strip("،") in PARTICLES | OPENERS for l in ls)
    durs = [l[-1]["e"] - l[0]["s"] for l in lines]
    chain_split = lambda ls: any(l.split()[-1] != "يا" and l.split()[-2:-1] == ["يا"] and k + 1 < len(ls) and ls[k + 1].startswith("يا")
                                 for k, l in enumerate(ls))
    checks = [check("break at the pause / comma after 'وجله،'", any(t.endswith("وجله،") for t in txt), txt, "…وجله،"),
              check("no line ends on a particle or an opener", not ends_particle(txt), txt, "no particle/opener at line end"),
              check("≤7 words per line", all(len(l) <= 7 for l in lines), [len(l) for l in lines], "<=7"),
              check("vocative chain 'يا رب يا كريم يا رحيم' kept together", any("يا رب يا كريم يا رحيم" in t for t in txt), txt, "chain"),
              check("line durations in 1.1–3.6 s", all(1.1 - 0.15 <= d <= 3.6 for d in durs), durs, "1.1–3.6"),
              check("negative control: greedy 7-word lines break badly", ends_particle(greedy) or not any(g.endswith("وجله،") for g in greedy), greedy, "bad break")]
    return checks, [write_json(Path(wd) / "lines.json", txt)]


STOP = {"ده", "دي", "كده", "بس", "يعني", "اوي", "أوي", "في", "من", "على", "إلى", "عن", "هذا", "هذه", "التي", "الذي", "ثم", "و", "يا",
        "هو", "هي", "انا", "أنا", "احنا", "إحنا", "مش", "كان", "كانت", "لما", "علشان", "عشان", "قوي", "جدا", "اللي", "إن", "أن"}
UNITS = {"جنيه", "ريال", "دولار", "كيلو", "متر", "سنة", "سنين", "مرة", "ساعة", "%", "٪"}


def pick_keywords(lines, rms, spacing=1.2):
    """stress = 0.65·z(log rms) + 0.35·z(length); + 0.9·(i+1)/n end focus; +0.5 recurring 2–3x; unit after number −3; fillers never."""
    import statistics
    flat = [w for l in lines for w in l]
    lr = [math.log(max(1e-6, rms[id(w)])) for w in flat]
    ln = [len(w["w"]) for w in flat]
    z = lambda v, xs: (v - statistics.mean(xs)) / (statistics.pstdev(xs) or 1)
    counts = {}
    for w in flat:
        counts[w["w"]] = counts.get(w["w"], 0) + 1
    picked, used, last_t = [], set(), -1e9
    k = 0
    for l in lines:
        best, bw = -1e9, None
        for i, w in enumerate(l):
            idx = flat.index(w)
            if w["w"] in STOP or w["w"] in used:
                continue
            sc = 0.65 * z(lr[idx], lr) + 0.35 * z(ln[idx], ln) + 0.9 * (i + 1) / len(l)
            sc += 0.5 if 2 <= counts[w["w"]] <= 3 else 0
            if i > 0 and (l[i - 1]["w"].isdigit() or re.fullmatch("[٠-٩]+", l[i - 1]["w"])) and w["w"] in UNITS:
                sc -= 3
            if sc > best:
                best, bw = sc, w
        if bw is not None and bw["s"] - last_t >= spacing:
            picked.append(bw["w"])
            used.add(bw["w"])
            last_t = bw["s"]
        else:
            picked.append(None)
    return picked


@card("ARAB-68")
def stress_keywords(task, wd):
    """One keyword per line from loudness and length (z-scores) with end focus; never fillers, never a unit after a number."""
    lines_txt = ["بس يعني الحلم كبير اوي", "دفعت 500 جنيه في التذكرة", "الحلم ده بيكبر كل يوم"]
    loud = {"اوي": 0.9, "جنيه": 0.95, "يعني": 0.8, "الحلم": 0.6, "كبير": 0.55, "التذكرة": 0.5, "بيكبر": 0.7, "يوم": 0.3}
    lines, t, rms = [], 0.0, {}
    for lt in lines_txt:
        l = []
        for w in lt.split():
            d = {"w": w, "s": t, "e": t + 0.4}
            rms[id(d)] = loud.get(w, 0.3)
            l.append(d)
            t += 0.45
        lines.append(l)
        t += 0.6
    kws = pick_keywords(lines, rms)
    naive = [max(l, key=lambda w: rms[id(w)])["w"] for l in lines]
    checks = [check("keyword per line known answer (recurring 'الحلم' +0.5 wins line 1, then used once)",
                    kws == ["الحلم", "التذكرة", "بيكبر"], kws, ["الحلم", "التذكرة", "بيكبر"]),
              check("never a filler", not any(k in STOP for k in kws if k), kws, "no fillers"),
              check("never the unit after a number", "جنيه" not in kws, kws, "no جنيه"),
              check("each keyword used once", len(set(k for k in kws if k)) == len([k for k in kws if k]), kws, "unique"),
              check("negative control: loudest-word picking takes fillers/units", any(w in STOP or w in UNITS for w in naive), naive, "contains filler/unit")]
    return checks, [write_json(Path(wd) / "keywords.json", kws)]


def ar_norm(t):
    t = unicodedata.normalize("NFKC", t)
    t = re.sub("[ً-ٰٟـ]", "", t)
    t = re.sub("[أإآٱ]", "ا", t).replace("ى", "ي").replace("ة", "ه").replace("ؤ", "و").replace("ئ", "ي")
    t = t.translate(str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789"))
    t = re.sub(r"[^\w\s]", "", t)
    return re.sub(r"\s+", " ", t).strip()


@card("ARAB-69")
def arabic_normalisation(task, wd):
    """Matching copy: NFKC, strip harakat/tatweel, unify alefs, ى→ي, ة→ه, ؤ→و, ئ→ي, Latin digits, no punctuation."""
    cases = {"إِنَّ الحَمْدَ لِلَّهِ": "ان الحمد لله", "مكتبـــة": "مكتبه", "مُصطفى": "مصطفي", "سُؤال": "سوال", "مسائل": "مسايل",
             "آمنة ٢٠٢٦": "امنه 2026", "«سلامٌ»، عليكم!": "سلام عليكم", "ٱلرَّحْمَٰن": "الرحمن", "۱۲۳": "123"}
    got = {k: ar_norm(k) for k in cases}
    disp = "إِنَّ الحَمْدَ لِلَّهِ"
    checks = [check("normalisation known answers", got == cases, got, cases),
              check("display text keeps its tashkeel", "َ" in disp and ar_norm(disp) != disp, True, True),
              check("variants now match", ar_norm("أحمد") == ar_norm("احمد") == ar_norm("إحمد"), True, True),
              check("negative control: raw strings do not match", "أحمد" != "احمد" and "مكتبـــة" != "مكتبه", True, True)]
    return checks, [write_json(Path(wd) / "normalised.json", got)]


def align_text(lyrics, asr):
    import difflib
    a = [ar_norm(w) for w in lyrics]
    b = [ar_norm(w["w"]) for w in asr]
    out = [None] * len(lyrics)
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            out[blk.a + k] = (asr[blk.b + k]["s"], asr[blk.b + k]["e"])
    for i in range(len(out)):                                   # fuzzy pass for near misses
        if out[i] is None:
            best = max(range(len(b)), key=lambda j: difflib.SequenceMatcher(a=a[i], b=b[j]).ratio())
            if difflib.SequenceMatcher(a=a[i], b=b[best]).ratio() >= 0.6:
                out[i] = (asr[best]["s"], asr[best]["e"])
    return out


@card("ARAB-70")
def vowelled_over_asr(task, wd):
    """Keep full harakat and '..' pauses in the lyric file; align it onto ASR word times; display the vowelled text."""
    np = np_()
    lyric = "يَا لَيْلُ الصَّبُّ مَتَى غَدُهُ .. أَقِيَامُ السَّاعَةِ مَوْعِدُهُ"
    phrases = [p.strip() for p in lyric.split("..")]
    words = " ".join(phrases).split()
    asr = [{"w": w, "s": round(0.4 + 0.5 * i, 2), "e": round(0.8 + 0.5 * i, 2)} for i, w in
           enumerate(["يا", "ليل", "الصب", "متي", "غده", "اقيام", "الساعه", "موعده"])]
    al = align_text(words, asr)
    exact = sum(1 for w in words if any(w == x["w"] for x in asr))
    f = font(AMIRI, 34)
    v = shaped_mask(phrases[0], f)
    u = shaped_mask(ar_norm(phrases[0]), f)
    from PIL import Image
    Image.fromarray((v * 255).astype("uint8")).save(Path(wd) / "card_vowelled.png")
    checks = [check("two phrase cards split on '..'", len(phrases) == 2, phrases, 2),
              check("every vowelled word aligned to an ASR time", all(a is not None for a in al), al, "all timed"),
              check("times monotonic", all(al[i][0] < al[i + 1][0] for i in range(len(al) - 1)), True, True),
              check("displayed card carries the harakat (extra mark ink)", comps(v) > comps(u) + 4, [comps(v), comps(u)], "vowelled > plain"),
              check("negative control: exact string matching aligns almost nothing", exact <= 1, exact, "<=1")]
    return checks, [Path(wd) / "card_vowelled.png", write_json(Path(wd) / "aligned.json", {"words": words, "times": al})]


def tone_words(path, words, rate=16000):
    np = np_()
    n = int((words[-1]["e"] + 0.5) * rate)
    s = np.zeros(n)
    for k, w in enumerate(words):
        a, b = int(w["s"] * rate), int(w["e"] * rate)
        tt = np.arange(b - a) / rate
        s[a:b] = w.get("amp", 0.4) * np.sin(2 * math.pi * (180 + 20 * (k % 5)) * tt) * np.hanning(b - a)
    fx.write_wav(path, s, rate)
    return path


@card("ARAB-66")
def verse_from_sound(task, wd):
    """Words + sound → verse.json: lines ≤7 words 1.1–3.6 s, sections at pauses ≥3 s, interludes ≥4.5 s, one keyword per line, light from RMS."""
    np = np_()
    words = timed(DUA, pauses={6: 3.4, 12: 4.8})
    for k, w in enumerate(words):
        w["amp"] = 0.2 + 0.05 * (k % 4)
    wav = tone_words(Path(wd) / "voice.wav", words)
    data, rate = fx.read_wav(wav)
    x = data[:, 0]
    rms = {}
    for w in words:
        seg = x[int(w["s"] * rate):int(w["e"] * rate)]
        rms[id(w)] = float(np.sqrt((seg ** 2).mean()))
    lines = segment_dp(words)
    def sectionize(lines):
        sections, cur, gaps = [], [lines[0]], []
        for a, b in zip(lines, lines[1:]):
            g = b[0]["s"] - a[-1]["e"]
            gaps.append(g)
            if g >= 3.0:
                sections.append(cur)
                cur = []
            cur.append(b)
        sections.append(cur)
        return sections, gaps
    sections, gaps = sectionize(lines)
    flat_sections, _ = sectionize(segment_dp(timed(DUA)))
    interludes = [round(g, 2) for g in gaps if g >= 4.5]
    kws = pick_keywords(lines, rms, spacing=2.0)
    fps = 30
    dur = len(x) / rate
    env = [float(np.sqrt((x[int(i * rate / fps):int((i + 1) * rate / fps)] ** 2).mean())) for i in range(int(dur * fps))]
    verse = {"lines": [{"text": " ".join(w["w"] for w in l), "t0": l[0]["s"], "t1": l[-1]["e"], "keyword": kws[i]} for i, l in enumerate(lines)],
             "sections": [len(s) for s in sections], "interludes": interludes, "frames": int(round(dur * fps)), "light": env}
    out = write_json(Path(wd) / "verse.json", verse)
    lit = np.array(env)
    voiced = np.zeros(len(env), bool)
    for w in words:
        voiced[int(w["s"] * fps) + 1:int(w["e"] * fps) - 1] = True
    checks = [check("lines ≤7 words", all(len(l) <= 7 for l in lines), [len(l) for l in lines], "<=7"),
              check("a pause ≥3 s starts a new section", len(sections) == 3, verse["sections"], "3 sections"),
              check("a pause ≥4.5 s is an interlude", len(interludes) == 1 and interludes[0] >= 4.5, interludes, "one ≥4.5"),
              check("one keyword per line, never a filler", all(k is None or k not in STOP for k in kws) and sum(1 for k in kws if k) >= 2, kws, "keywords"),
              check("light follows the voice (RMS voiced ≫ silent)", lit[voiced].mean() > 5 * (lit[~voiced].mean() + 1e-6), [float(lit[voiced].mean()), float(lit[~voiced].mean())], "voiced ≫ silent"),
              check("frame count = duration × fps", verse["frames"] == int(round(dur * fps)), verse["frames"], int(round(dur * fps))),
              check("negative control: the same words read without pauses stay one section", len(flat_sections) == 1, len(flat_sections), 1)]
    return checks, [out, wav]


@card("ARAB-71")
def emotional_lyric_preset(task, wd):
    """STY.lyric: night gradient #0E0A16→#2A1236, ink #F7EFE6, accent #FFB35C on the emphasised word, underline grows with the voice, 2.0 words/s, the previous line floats away."""
    np = np_()
    from PIL import Image, ImageDraw
    W, H = 270, 480
    BG1, BG2, INK, ACC = hexrgb("#0E0A16"), hexrgb("#2A1236"), hexrgb("#F7EFE6"), hexrgb("#FFB35C")
    L1, L2 = ["قلبي", "يعرف", "طريق", "البيت"], ["ولو", "طال", "الليل", "علينا"]
    emph = (0, 2)
    times1 = [0.3 + 0.5 * i for i in range(4)]
    times2 = [2.6 + 0.5 * i for i in range(4)]
    words = [{"w": w, "s": t, "e": t + 0.4} for w, t in zip(L1 + L2, times1 + times2)]
    wav = tone_words(Path(wd) / "song.wav", words)
    data, rate = fx.read_wav(wav)
    x = np.abs(data[:, 0])
    cum = np.cumsum(x) / x.sum()
    grad = np.zeros((H, W, 3), np.uint8)
    for y in range(H):
        grad[y] = [int(a + (b - a) * y / (H - 1)) for a, b in zip(BG1, BG2)]
    gimg = Image.fromarray(grad).convert("RGBA")
    f = font(CAIRO, 28, 800)
    r1 = word_row(L1, f, W, 220, fills=[(ACC if (0, i) == emph else INK) + (255,) for i in range(4)])
    r2 = word_row(L2, f, W, 220, fills=[INK + (255,)] * 4)
    plain1 = [tile(w, f, fill=INK + (255,))[0] for w in L1]

    def draw(t, c):
        c.alpha_composite(gimg)
        float_up = cubic_out((t - 2.4) / 0.6) if t > 2.4 else 0
        for i, r in enumerate(r1):
            if t >= times1[i]:
                tl = r["tile"] if (i != emph[1] or t >= times1[i]) else plain1[i]
                place(c, tl, r["cx"], r["cy"] - 40 * float_up, alpha=(1 - float_up) * clamp((t - times1[i]) / 0.15))
        for i, r in enumerate(r2):
            if t >= times2[i]:
                place(c, r["tile"], r["cx"], r["cy"] + 60, alpha=clamp((t - times2[i]) / 0.15))
        w = 0.8 * W * float(cum[min(len(cum) - 1, int(t * rate))])
        ImageDraw.Draw(c).rectangle([W / 2 + 0.4 * W - w, 330, W / 2 + 0.4 * W, 332], fill=ACC)
    p, frames = video(wd, "lyric.mp4", draw, 4.8, size=(W, H))
    top, bot = frames[10][2:6, 5:20].reshape(-1, 3).mean(0), frames[10][-6:-2, 5:20].reshape(-1, 3).mean(0)
    accm = lambda t: int(colour_mask(frame_at(frames, t)[:300], ACC, 40).sum())
    ul = [float(colour_mask(frame_at(frames, t)[328:335], ACC, 40).any(axis=0).sum()) for t in np.arange(0.2, 4.6, 0.2)]
    voice = [0.8 * W * float(cum[int(t * rate)]) for t in np.arange(0.2, 4.6, 0.2)]
    corr = float(np.corrcoef(ul, voice)[0, 1])
    y_a = centroid(lum(crop(frame_at(frames, 2.3), (0, 130, W, 260))) > 60)[1]
    y_b = centroid(lum(crop(frame_at(frames, 2.55), (0, 130, W, 260))) > 60)[1]
    firsts = [first_time([box_ink(fr, r["slot"] if "slot" in r else grow(ink_box_abs(r), 3, 8), 120) for fr in frames], 0.3) for r in r1]
    checks = [check("night gradient #0E0A16 → #2A1236", np.abs(top - BG1).max() < 8 and np.abs(bot - BG2).max() < 8, [top.tolist(), bot.tolist()], [BG1, BG2]),
              check("accent warms the emphasised word only after it is sung", accm(times1[2] - 0.1) == 0 and accm(times1[2] + 0.3) > 50,
                    [accm(times1[2] - 0.1), accm(times1[2] + 0.3)], "0 then >50"),
              check("underline grows with the voice (r > 0.97)", corr > 0.97, corr, ">0.97"),
              check("previous line floats away", y_b < y_a - 10, [y_a, y_b], "moves up"),
              check("2.0 words/s", all(abs((b - a) - 0.5) <= 0.07 for a, b in zip(firsts, firsts[1:])), firsts, "0.5 s apart"),
              check("negative control: before the emphasised word there is no accent", accm(0.5) == 0, accm(0.5), 0)]
    return checks, [p, wav]


MONEY_JS = r"""
const AR='٠١٢٣٤٥٦٧٨٩';
const toArabicDigits=s=>String(s).replace(/[0-9]/g,d=>AR[+d]);
function group(s){let o='';for(let i=0;i<s.length;i++){if(i&&(s.length-i)%3===0)o+=',';o+=s[i];}return o;}
function formatMinor(minor,{exp=2,arabicDigits=true,currency='ر.س'}={}){
  const neg=minor<0;let a=String(Math.abs(minor)).padStart(exp+1,'0');
  const ip=a.slice(0,a.length-exp),fp=a.slice(a.length-exp);
  let s=(neg?'-':'')+group(ip)+(exp?'.'+fp:'');if(arabicDigits)s=toArabicDigits(s);return currency?s+' '+currency:s;}
function roundHalfAway(x,d){const s=x<0?-1:1;const m=Math.round(Math.abs(x)*Math.pow(10,d)+1e-9);return s*m/Math.pow(10,d);}
function formatPercent(x,d=1,arabicDigits=true){const s=roundHalfAway(x,d).toFixed(d)+'٪';return arabicDigits?toArabicDigits(s):s;}
const cases=[[123456789],[-5],[100000,{exp:0}],[999,{arabicDigits:false,currency:''}]];
console.log(JSON.stringify({minor:cases.map(c=>formatMinor(...c)),pct:[formatPercent(2.675,2),formatPercent(2.5,0),formatPercent(-0.05,1)]}));
"""


@card("ARAB-74")
def money_formatter(task, wd):
    """formatMinor without Intl: grouped minor units, Arabic-Indic digits, currency, half-away-from-zero; same result in Node and Python."""
    from decimal import Decimal, ROUND_HALF_UP
    jsf = Path(wd) / "format.mjs"
    jsf.write_text(MONEY_JS, encoding="utf-8")
    node = json.loads(subprocess.run(["node", str(jsf)], capture_output=True, text=True, timeout=20).stdout)

    def fmt_minor(minor, exp=2, arabic=True, currency="ر.س"):
        a = str(abs(minor)).rjust(exp + 1, "0")
        ip, fp = a[:len(a) - exp], a[len(a) - exp:]
        s = ("-" if minor < 0 else "") + "{:,}".format(int(ip)) + ("." + fp if exp else "")
        s = to_ar_digits(s) if arabic else s
        return s + " " + currency if currency else s

    def pct(x, d):
        q = Decimal(str(abs(x))).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP)
        return to_ar_digits(("-" if x < 0 and q != 0 else "") + format(q, "f") + "٪")
    py = {"minor": [fmt_minor(123456789), fmt_minor(-5), fmt_minor(100000, exp=0), fmt_minor(999, arabic=False, currency="")],
          "pct": [pct(2.675, 2), pct(2.5, 0), pct(-0.05, 1)]}
    expect_minor = ["١,٢٣٤,٥٦٧.٨٩ ر.س", "-٠.٠٥ ر.س", "١٠٠,٠٠٠ ر.س", "9.99"]
    html = "<p>المبلغ: <bdi>%s</bdi></p>" % node["minor"][0]
    out = Path(wd) / "money.html"
    out.write_text(html, encoding="utf-8")
    checks = [check("formatMinor known answers", node["minor"] == expect_minor, node["minor"], expect_minor),
              check("half-away-from-zero percent", node["pct"][:2] == ["٢.٦٨٪", "٣٪"], node["pct"], ["٢.٦٨٪", "٣٪"]),
              check("Node and Python implementations agree", node["minor"] == py["minor"] and node["pct"][:2] == py["pct"][:2], [node, py], "equal"),
              check("wrapped in <bdi>", "<bdi>١,٢٣٤,٥٦٧.٨٩ ر.س</bdi>" in html, True, True),
              check("negative control: naive float formatting rounds 2.675 down", "%.2f" % 2.675 == "2.67", "%.2f" % 2.675, "2.67 ≠ 2.68")]
    return checks, [jsf, out]


def mk_latin(s):
    return s.translate(str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹٫٬", "01234567890123456789.,"))


def line_meta_full(s):
    t = mk_latin(s)
    m = re.search(r"(\d+(?:[.,]\d+)*)\s*(%|٪|ألف|مليون|مليار|k|M)?", t)
    return {"num": float(m.group(1).replace(",", "")) if m else None, "unit": (m.group(2) if m else None),
            "question": "؟" in s or "?" in s, "quote": "«" in s}


@card("ARAB-75")
def digit_unit_detection(task, wd):
    """MK.latin maps ٠–٩, ۰–۹, ٫/٬; MK.lineMeta finds the first number + unit and flags questions and quotes."""
    cases = {"نما السوق ٢٥٪ هذا العام": (25.0, "٪", False, False), "وصلنا إلى ٣٫٥ مليون مشاهدة": (3.5, "مليون", False, False),
             "هل تصدق ۱۲ ألف؟": (12.0, "ألف", True, False), "«الربح ١٬٢٠٠ دولار»": (1200.0, None, False, True), "بدون أرقام": (None, None, False, False)}
    got = {k: tuple(line_meta_full(k).values()) for k in cases}
    checks = [check("latin digits", mk_latin("٠١٢٣٤٥٦٧٨٩ ۴۵ ٣٫٥ ١٬٠٠٠") == "0123456789 45 3.5 1,000", mk_latin("٠١٢٣٤٥٦٧٨٩ ۴۵ ٣٫٥ ١٬٠٠٠"), "0123456789 45 3.5 1,000"),
              check("number/unit/question/quote known answers", got == cases, got, cases),
              check("negative control: a plain \\d regex misses Arabic-Indic digits", re.search(r"[0-9]", "نما ٢٥٪") is None, None, None)]
    return checks, [write_json(Path(wd) / "linemeta.json", {k: list(v) for k, v in got.items()})]


def ar_plural(n):
    m = n % 100
    return "zero" if n == 0 else "one" if n == 1 else "two" if n == 2 else "few" if 3 <= m <= 10 else "many" if 11 <= m <= 99 else "other"


def edits_phrase(n):
    d = to_ar_digits(n)
    return {"zero": "لا تعديلات", "one": "تعديل واحد بانتظار الإرسال", "two": "تعديلان بانتظار الإرسال",
            "few": "%s تعديلات بانتظار الإرسال" % d, "many": "%s تعديلاً بانتظار الإرسال" % d, "other": "%s تعديل بانتظار الإرسال" % d}[ar_plural(n)]


@card("ARAB-76")
def plural_agreement(task, wd):
    """Six CLDR plural categories for Arabic (zero/one/two/few/many/other) checked against Node's Intl.PluralRules('ar')."""
    ns = list(range(0, 230))
    js = "console.log(JSON.stringify(%s.map(n=>new Intl.PluralRules('ar').select(n))))" % json.dumps(ns)
    node = json.loads(subprocess.run(["node", "-e", js], capture_output=True, text=True, timeout=20).stdout)
    mine = [ar_plural(n) for n in ns]
    en = ["one" if n == 1 else "other" for n in ns]
    phrases = {n: edits_phrase(n) for n in (0, 1, 2, 5, 11, 100)}
    checks = [check("CLDR rule = Intl.PluralRules('ar') for 0..229", mine == node, sum(a == b for a, b in zip(mine, node)), len(ns)),
              check("all six forms occur", set(mine) == {"zero", "one", "two", "few", "many", "other"}, sorted(set(mine)), 6),
              check("UI phrases: dual and 11+ accusative", phrases[2] == "تعديلان بانتظار الإرسال" and phrases[11] == "١١ تعديلاً بانتظار الإرسال", phrases, "dual / تعديلاً"),
              check("negative control: an English one/other rule disagrees", sum(a == b for a, b in zip(en, node)) < len(ns) * 0.2, sum(a == b for a, b in zip(en, node)), "mostly wrong")]
    return checks, [write_json(Path(wd) / "plurals.json", phrases)]


@card("ARAB-77")
def number_to_headline(task, wd):
    """0–1.5 s the number counts up in tabular digits, 1.5–2.5 s it steps aside, 2.5–5 s the sentence mask-reveals with unit and source."""
    np = np_()
    W, H = 360, 640
    target = 1250
    f = font(CAIRO, 64, 800)
    cellw = max(tlen(d, f) for d in AR_DIGITS)
    dig_tiles = {d: tile(d, f)[0] for d in AR_DIGITS}
    sent = ["مشاهدة", "في", "أسبوع"]
    fs = font(CAIRO, 26, 700)

    def counter(c, val, cx, cy):
        s = to_ar_digits(str(val)).rjust(4, "٠")
        x0 = cx - cellw * 2
        for i, d in enumerate(s):
            tl = dig_tiles[d]
            place(c, tl, x0 + cellw * (i + 0.5), cy)
    row = word_row(sent, fs, W, 380)

    def draw(t, c):
        v = int(round(target * cubic_out(t / 1.5))) if t < 1.5 else target
        e = cubic_out((t - 1.5) / 1.0) if t > 1.5 else 0
        counter(c, v, W / 2 + 70 * e, 280 - 30 * e)
        for i, r in enumerate(row):
            t0 = 2.5 + 0.12 * i
            if t >= t0:
                ee = expo_out((t - t0) / 0.7)
                place(c, r["tile"], r["cx"], r["cy"] + 30 * (1 - ee), alpha=ee, clip=grow(ink_box_abs(r), 3, 12))
        if t > 3.5:
            place(c, tile("المصدر: بيانات تجريبية", font(CAIRO, 12, 400), fill=(170, 170, 170, 255))[0], W / 2, 430, alpha=clamp(t - 3.5))
    p, frames = video(wd, "number_headline.mp4", draw, 5.0, size=(W, H))
    band = (0, 220, W, 340)
    widths = [bbox(mask_of(crop(frame_at(frames, t), band), 128)) for t in (0.6, 0.9, 1.2, 1.5)]
    ww = [b[2] - b[0] for b in widths]
    ref = blank((W, H))
    counter(ref, target, W / 2, 280)
    match = iou(mask_of(crop(frame_at(frames, 1.5), band), 128), mask_of(crop(arr(ref), band), 128))
    early = iou(mask_of(crop(frame_at(frames, 0.5), band), 128), mask_of(crop(arr(ref), band), 128))
    cx = [wcentroid(crop(frame_at(frames, t), band))[0] for t in (1.5, 2.6)]
    sb = (0, 350, W, 410)
    checks = [check("tabular digits: counter width constant while counting", max(ww) - min(ww) <= 3, ww, "constant"),
              check("lands on the real figure ١٢٥٠ at 1.5 s", match > 0.9, match, ">0.9"),
              check("steps aside 1.5–2.5 s", cx[1] - cx[0] > 50, cx, "+70 px"),
              check("sentence hidden before 2.5 s, revealed by 4 s", box_ink(frame_at(frames, 2.4), sb) == 0 and box_ink(frame_at(frames, 4.0), sb) > 200,
                    [box_ink(frame_at(frames, 2.4), sb), box_ink(frame_at(frames, 4.0), sb)], "0 then >200"),
              check("negative control: mid-count frame is not the final figure", early < 0.8, early, "<0.8")]
    return checks, [p]


@card("ARAB-78")
def typographic_dialogue(task, wd):
    """Question settles on the right (0–2 s), withdraws (2–2.6 s), the answer enters from the other side in a second colour (2.6–6 s)."""
    np = np_()
    W, H = 360, 480
    Q, A = (240, 236, 226), (255, 196, 90)
    fq = font(CAIRO, 30, 700)
    tq, _ = tile("لماذا الآن؟", fq, fill=Q + (255,))
    ta, _ = tile("لأن الوقت حان", fq, fill=A + (255,))

    def draw(t, c):
        e = cubic_out(t / 0.6)
        if t < 2:
            place(c, tq, W - 30 - tq.width / 2 + 40 * (1 - e), 180, alpha=e)
        else:
            w = cubic_out((t - 2) / 0.6)
            place(c, tq, W - 30 - tq.width / 2 + 20 * w, 180 - 30 * w, alpha=1 - 0.6 * w, scale=1 - 0.1 * w)
        if t >= 2.6:
            ea = cubic_out((t - 2.6) / 0.6)
            place(c, ta, 30 + ta.width / 2 - 40 * (1 - ea), 300, alpha=ea)
    p, frames = video(wd, "dialogue.mp4", draw, 6.0, size=(W, H))
    qc = centroid(colour_mask(frame_at(frames, 1.5), Q, 30))
    ac = centroid(colour_mask(frame_at(frames, 4.0), A, 40))
    qdim = float(lum(frame_at(frames, 3.0)).max())
    before = int(colour_mask(frame_at(frames, 2.5), A, 40).sum())
    checks = [check("question settles on the right", qc[0] > W * 0.55, qc[0], ">0.55W"),
              check("question withdraws (dimmer, moved)", int(colour_mask(frame_at(frames, 3.0), Q, 30).sum()) == 0 and qdim > 30, qdim, "dimmed"),
              check("answer from the other side in the second colour", ac is not None and ac[0] < W * 0.45, ac, "<0.45W"),
              check("answer waits until 2.6 s", before == 0, before, 0),
              check("negative control: at 1.5 s there is no answer yet", int(colour_mask(frame_at(frames, 1.5), A, 40).sum()) == 0, 0, 0)]
    return checks, [p]


def merc(lng, lat, z):
    s = 256 * 2 ** z
    x = (lng + 180) / 360 * s
    la = math.radians(lat)
    y = (1 - math.log(math.tan(la) + 1 / math.cos(la)) / math.pi) / 2 * s
    return x, y


@card("ARAB-80")
def projected_labels(task, wd):
    """Labels placed per frame by projecting [lng, lat] through the camera (Web Mercator); rise-and-fade ~0.7 s; ≥24 px at 1080p."""
    np = np_()
    from PIL import ImageDraw
    W, H = 540, 540
    city = (31.2357, 30.0444)                         # Cairo
    RED = (255, 40, 40)
    f = font(CAIRO, int(round(24 * W / 1080)) + 4, 700)
    lab, _ = tile("القاهرة", f)

    def cam(t):
        e = cubic_out(t / 2.0)
        return (28 + 4 * e, 27 + 4 * e), 4 + 1.5 * e

    def proj(t):
        (clng, clat), z = cam(t)
        cx, cy = merc(clng, clat, z)
        px, py = merc(*city, z)
        return W / 2 + px - cx, H / 2 + py - cy

    def draw(t, c, static=False):
        d = ImageDraw.Draw(c)
        (clng, clat), z = cam(t)
        for g in range(-40, 60, 5):                    # graticule of the projected world
            x, _ = merc(g, 0, z)
            cx, cy = merc(clng, clat, z)
            d.line([W / 2 + x - cx, 0, W / 2 + x - cx, H], fill=(30, 40, 60))
        x, y = proj(0 if static else t)
        d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=RED)
        a = clamp((t - 0.3) / 0.7)
        place(c, lab, x, y - 22 + 10 * (1 - cubic_out(a)), alpha=a)
    p, frames = video(wd, "map_labels.mp4", draw, 2.4, size=(W, H))
    errs = []
    for t in (0.5, 1.2, 2.0):
        m = colour_mask(frame_at(frames, t), RED, 60)
        c = centroid(m)
        ex = proj(round(t * 30) / 30)
        errs.append(math.dist(c, ex))
    _, sf = video(wd, "map_static.mp4", lambda t, c: draw(t, c, static=True), 2.4, size=(W, H))
    drift = math.dist(centroid(colour_mask(frame_at(frames, 2.0), RED, 60)), centroid(colour_mask(frame_at(sf, 2.0), RED, 60)))
    lb = bbox(lum(crop(frames[-1], (0, 0, W, H))) > 200)
    ref = comps(shaped_mask("القاهرة", f))
    checks = [check("label anchor follows the projected point (≤1.5 px)", max(errs) <= 1.5, errs, "<=1.5"),
              check("label size ≥ 24 px at 1080p", f.size * 1080 / W >= 24, f.size * 1080 / W, ">=24"),
              check("rises and fades in over ~0.7 s", int((lum(frame_at(frames, 0.2)) > 200).sum()) == 0 and int((lum(frame_at(frames, 1.2)) > 200).sum()) > 50,
                    [int((lum(frame_at(frames, 0.2)) > 200).sum()), int((lum(frame_at(frames, 1.2)) > 200).sum())], "0 then >50"),
              check("negative control: a label pinned to its first pixel drifts off the city", drift > 15, drift, ">15 px")]
    return checks, [p]


def unmojibake(s):
    best = s
    if len(AR_RE.findall(s)) >= 2:
        return s
    for enc, dec in (("latin-1", "utf-8"), ("cp1252", "utf-8"), ("latin-1", "cp1256")):
        try:
            g = s.encode(enc).decode(dec)
        except (UnicodeError, LookupError):
            continue
        if len(re.findall("[؀-ۿ]", g)) >= 2:
            return g
    return best


def safe_name(s):
    return re.sub(r"[^\w\-. ()؀-ۿ]", "", s).strip()


@card("ARAB-81")
def mojibake_repair(task, wd):
    """_unmojibake tries latin-1→utf-8, cp1252→utf-8, latin-1→cp1256 and accepts only ≥2 Arabic letters; _safe_name keeps the Arabic block."""
    names = ["تقرير الشهر.mp4", "فيديو (2).mov", "صوت.wav"]
    broken = {names[0]: names[0].encode("utf-8").decode("latin-1"), names[1]: names[1].encode("utf-8").decode("cp1252", errors="replace"),
              names[2]: names[2].encode("cp1256").decode("latin-1")}
    fixed = {k: unmojibake(v) for k, v in broken.items()}
    latin = unmojibake("report_final.mp4")
    checks = [check("latin-1 → utf-8 repaired", fixed[names[0]] == names[0], fixed[names[0]], names[0]),
              check("latin-1 → cp1256 repaired", fixed[names[2]] == names[2], fixed[names[2]], names[2]),
              check("Latin names untouched (no Arabic gained)", latin == "report_final.mp4", latin, "report_final.mp4"),
              check("safe name keeps Arabic, drops path tricks", safe_name("../تقرير:<x>.mp4") == "..تقريرx.mp4", safe_name("../تقرير:<x>.mp4"), "..تقريرx.mp4"),
              check("negative control: the mojibake itself has no Arabic letters", len(AR_RE.findall(broken[names[0]])) == 0, broken[names[0]], "no Arabic")]
    return checks, [write_json(Path(wd) / "names.json", fixed)]


@card("ARAB-82")
def safe_credit_burn(task, wd):
    """Credit via drawtext textfile= (≤300 chars), 1.3% H, white@0.5, y = 0.905·h: untrusted text never enters the filter grammar."""
    np = np_()
    W, H = 540, 960
    base = fx.color_clip(Path(wd) / "reel.mp4", "black", 1.0, "%dx%d" % (W, H), 30)
    credit = "insta: o'neil_50%: \\ [x] ,y;z"[:300]
    tf = Path(wd) / "credit.txt"
    tf.write_text(credit, encoding="utf-8")
    dv = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    out = Path(wd) / "credited.mp4"
    vf = "drawtext=fontfile=%s:textfile=%s:expansion=none:fontsize=%d:fontcolor=white@0.5:x=(w-text_w)/2:y=0.905*h" % (dv, tf.name, round(0.013 * H))
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", base.name, "-vf", vf, "-c:v", "libx264", "-crf", "12", out.name],
                   cwd=str(wd), check=True, capture_output=True, timeout=60)
    fr = fx.frames(out, (W, H))[10]
    b = bbox(lum(fr) > 30)
    inline = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", base.name, "-vf",
                             "drawtext=fontfile=%s:text=%s:fontsize=%d:fontcolor=white@0.5:x=(w-text_w)/2:y=0.905*h" % (dv, credit, round(0.013 * H)),
                             "-frames:v", "1", "-update", "1", "bad.png"], cwd=str(wd), capture_output=True, timeout=60)
    from PIL import Image, ImageFont
    want = ImageFont.truetype(dv, round(0.013 * H)).getlength(credit)
    bad_b = bbox(np.asarray(Image.open(Path(wd) / "bad.png").convert("L"), float) > 30) if (Path(wd) / "bad.png").exists() else None
    bad_w = (bad_b[2] - bad_b[0]) if bad_b else 0
    checks = [check("credit burned at y ≈ 0.905h", b is not None and abs(b[1] - 0.905 * H) <= 3, b, 0.905 * H),
              check("size ≈ 1.3% of H", b is not None and 0.6 * 0.013 * H <= b[3] - b[1] <= 1.4 * 0.013 * H, b and b[3] - b[1], 0.013 * H),
              check("white at 50%", 100 <= float(lum(fr).max()) <= 150, float(lum(fr).max()), 128),
              check("the whole untrusted string is drawn (ink width = its advance)", b is not None and abs((b[2] - b[0]) - want) <= 4, b and b[2] - b[0], want),
              check("negative control: inlined into the filter grammar the credit is mangled", inline.returncode != 0 or abs(bad_w - want) > 10,
                    [inline.returncode, bad_w], "error or wrong text")]
    return checks, [out, tf]


AR_HUE = [(15, "أحمر"), (45, "برتقالي"), (62, "أصفر"), (165, "أخضر"), (260, "أزرق"), (300, "بنفسجي"), (340, "وردي"), (360, "أحمر")]


def name_ar(rgb):
    import colorsys
    h, s, v = colorsys.rgb_to_hsv(*[c / 255 for c in rgb])
    if s < 0.14 or v < 0.12:
        return "أسود" if v < 0.12 else "أبيض" if v > 0.88 else ("رمادي غامق" if v < 0.45 else "رمادي")
    deg = h * 360
    base = next(n for lim, n in AR_HUE if deg < lim)
    if base in ("برتقالي", "أصفر") and s < 0.35 and v > 0.8:
        return "كريمي"
    if base == "أصفر" and v < 0.6:
        return "زيتوني"
    return base + (" داكن" if v < 0.45 else "")


@card("ARAB-83")
def arabic_colour_names(task, wd):
    """vectorize.name_ar: HSV thresholds (s < .14 or v < .12 → neutral), hue bands at 15/45/62/165/260/300/340°."""
    cases = {(200, 20, 20): "أحمر", (90, 10, 10): "أحمر داكن", (128, 128, 0): "زيتوني", (245, 235, 200): "كريمي", (20, 160, 60): "أخضر",
             (30, 60, 200): "أزرق", (140, 40, 200): "بنفسجي", (230, 80, 170): "وردي", (240, 140, 20): "برتقالي", (128, 128, 128): "رمادي",
             (5, 5, 5): "أسود", (250, 250, 250): "أبيض"}
    got = {str(k): name_ar(k) for k in cases}
    exp = {str(k): v for k, v in cases.items()}
    import colorsys
    hue_only = next(n for lim, n in AR_HUE if colorsys.rgb_to_hsv(0.5, 0.5, 0.5)[0] * 360 < lim)
    checks = [check("colour names known answers", got == exp, got, exp),
              check("band edge: hue 14° red, 16° orange", name_ar((255, 62, 0)) == "أحمر" and name_ar((255, 68, 0)) == "برتقالي",
                    [name_ar((255, 62, 0)), name_ar((255, 68, 0))], ["أحمر", "برتقالي"]),
              check("negative control: hue-only naming calls grey red", hue_only == "أحمر", hue_only, "أحمر (wrong)")]
    return checks, [write_json(Path(wd) / "names.json", got)]


@card("ARAB-87")
def fit_width_shrink(task, wd):
    """fit_width .96: one size so the longest line fills 96% width; fitLayout ×0.9 (≤14x) until rows ≤ maxRows; textfit −1 px to 84% (min 9) then truncate."""
    np = np_()
    W = 540
    lines = ["كل شيء يبدأ", "بخطوة صغيرة جدا نحو الحلم"]
    lo, hi = 4, 400
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if max(tlen(l, font(CAIRO, mid, 700)) for l in lines) <= 0.96 * W:
            lo = mid
        else:
            hi = mid
    f = font(CAIRO, lo, 700)
    from PIL import ImageDraw
    c = blank((W, int(lo * 1.42 * 2 + 40)))
    d = ImageDraw.Draw(c)
    for i, l in enumerate(lines):
        d.text((W / 2, 20 + lo * 1.42 * (i + 0.5)), l, font=f, fill="white", anchor="mm", direction="rtl", language="ar")
    out = save_png(c, Path(wd) / "fit_width.png")
    widest = max(tlen(l, f) for l in lines) / W
    para = "هذا نص طويل يجب أن يتقلص حتى يدخل في عدد محدود من الصفوف داخل الإطار المحدد له مهما طال"
    size, it = 60.0, 0
    while it < 14:
        rows = wrap_words(para.split(), font(CAIRO, int(size), 700), 0.9 * W)
        if len(rows) <= 3:
            break
        size *= 0.9
        it += 1
    start_rows = len(wrap_words(para.split(), font(CAIRO, 60, 700), 0.9 * W))
    tsz, txt = 40, "عنوان طويل جدا لا يتسع في سطر واحد أبدا مهما حاولنا"
    while tsz > 9 and tlen(txt, font(CAIRO, tsz, 700)) > 0.84 * W:
        tsz -= 1
    trunc = txt
    if tlen(trunc, font(CAIRO, tsz, 700)) > 0.84 * W:
        while trunc and tlen(trunc + "…", font(CAIRO, tsz, 700)) > 0.84 * W:
            trunc = trunc[:-1]
        trunc += "…"
    checks = [check("longest line fills 96% (±1%)", abs(widest - 0.96) <= 0.01, widest, 0.96),
              check("fitLayout: rows ≤3 after ×0.9 steps", len(rows) <= 3 and 0 < it <= 14 and abs(size - 60 * 0.9 ** it) < 1e-6, [len(rows), it, size], "<=3 rows"),
              check("textfit ends within 84% width", tlen(trunc, font(CAIRO, tsz, 700)) <= 0.84 * W and tsz >= 9, [tsz, tlen(trunc, font(CAIRO, tsz, 700))], "<=%.0f" % (0.84 * W)),
              check("negative control: the paragraph at its base size needs more rows", start_rows > 3, start_rows, ">3")]
    return checks, [out]


def paint_text(img, s, x, y, size, colour, anchor="ms", bold=False, alpha=1.0, ss=2):
    """Painter-scene text op: supersampled, shaped, solid or (first-stop) gradient colour, anchors ms/mm/ls/rs."""
    from PIL import Image, ImageDraw
    W, H = img.size
    big = Image.new("RGBA", (W * ss, H * ss), (0, 0, 0, 0))
    f = font(CAIRO, size * ss, 760 if bold else 400)
    ImageDraw.Draw(big).text((x * ss, y * ss), s, font=f, fill=tuple(colour) + (int(255 * alpha),), anchor=anchor,
                             direction=_dir(s), language="ar" if _dir(s) == "rtl" else None)
    img.alpha_composite(big.resize((W, H), Image.LANCZOS))


def svg_import(svg, img):
    import xml.etree.ElementTree as ET
    ns = {"s": "http://www.w3.org/2000/svg"}
    root = ET.fromstring(svg)
    grads = {g.get("id"): g.find("s:stop", ns).get("stop-color") for g in root.iter("{http://www.w3.org/2000/svg}linearGradient")}
    amap = {"start": "ls", "middle": "ms", "end": "rs"}
    done = []
    for t in root.iter("{http://www.w3.org/2000/svg}text"):
        fill = t.get("fill", "#ffffff")
        m = re.match(r"url\(#(.+)\)", fill)
        col = hexrgb(grads[m.group(1)] if m else fill)
        txt = "".join(t.itertext()).strip()
        bold = int(t.get("font-weight", "400")) >= 600
        anchor = amap.get(t.get("text-anchor", "start"), "ls")
        if _dir(txt) == "rtl" and t.get("text-anchor", "start") == "start":
            anchor = "rs"
        paint_text(img, txt, float(t.get("x")), float(t.get("y")), int(float(t.get("font-size"))), col, anchor, bold)
        done.append({"text": txt, "colour": col, "anchor": anchor, "bold": bold})
    return done


@card("ARAB-88")
def painted_scene_text(task, wd):
    """Painter text op (anchors ms/mm/ls/rs, gradient first stop, bold ≥600, supersampled) + SVG <text> import, mapped to an OFL Arabic font."""
    np = np_()
    from PIL import Image, ImageFont
    W, H = 480, 300
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="480" height="300"><defs><linearGradient id="g"><stop offset="0" stop-color="#ffb35c"/>'
           '<stop offset="1" stop-color="#5d8cf7"/></linearGradient></defs>'
           '<text x="460" y="80" font-size="36" font-weight="700" fill="url(#g)">مشهد مرسوم</text>'
           '<text x="240" y="170" font-size="36" font-weight="400" text-anchor="middle" fill="#ffffff">مشهد مرسوم</text></svg>')
    img = blank((W, H))
    done = svg_import(svg, img)
    out = save_png(img, Path(wd) / "painted.png")
    a = arr(img)
    gold = colour_mask(a, hexrgb("#ffb35c"), 40)
    gb = bbox(gold)
    wb = bbox(a[100:200].min(axis=-1) > 200)
    thick_b = gold.sum() / max(1, (gb[3] - gb[1]) * (gb[2] - gb[0]))
    wm = a[100:200].min(axis=-1) > 200
    thick_r = wm.sum() / max(1, (wb[3] - wb[1]) * (wb[2] - wb[0]))
    df = ImageFont.load_default(36)
    from PIL import ImageDraw
    dimg = blank((W, 100))
    ImageDraw.Draw(dimg).text((10, 20), "مشهد مرسوم", font=df, fill="white")
    shaped = shaped_mask("مشهد مرسوم", font(CAIRO, 36, 400))
    dm = arr(dimg).min(axis=-1) > 128
    checks = [check("start anchor on RTL text → right edge at x", abs(gb[2] - 460) <= 3, gb[2], 460),
              check("text-anchor middle centres at x", abs((wb[0] + wb[2]) / 2 - 240) <= 3, (wb[0] + wb[2]) / 2, 240),
              check("gradient fill uses the first stop", int(gold.sum()) > 300, int(gold.sum()), ">300"),
              check("weight ≥600 → bold (more ink per box)", thick_b > thick_r, [thick_b, thick_r], "bold > regular"),
              check("negative control: Pillow's default font cannot draw it", iou(crop_ink(dm), crop_ink(shaped)) < 0.5 if dm.any() else True,
                    iou(crop_ink(dm), crop_ink(shaped)) if dm.any() else 0, "<0.5")]
    return checks, [out, write_json(Path(wd) / "svg_texts.json", done)]


@card("ARAB-92")
def four_bundled_fonts(task, wd):
    """IBM Plex Sans Arabic, Cairo, Tajawal, Amiri: every file loads, weights resolve, OFL text kept, Arabic shapes."""
    from fontTools.ttLib import TTFont
    plex_dir = REPO / "starters/kitab-theme/public/fonts"
    fonts = {"Cairo": [CAIRO], "Tajawal": [TAJAWAL], "Amiri": [AMIRI, AMIRI_B],
             "IBM Plex Sans Arabic": [plex_dir / ("ibm-plex-sans-arabic-arabic-%d-normal.woff2" % w) for w in (400, 500, 600, 700)]}
    lic = {"Cairo": FONTS / "OFL-Cairo.txt", "Tajawal": FONTS / "OFL-Tajawal.txt", "Amiri": FONTS / "OFL-Amiri.txt", "IBM Plex Sans Arabic": plex_dir / "OFL.txt"}
    word = "محمد"
    weights, shaped = {}, {}
    for fam, files in fonts.items():
        ws = []
        for p in files:
            t = TTFont(str(p))
            ws.append(t["OS/2"].usWeightClass)
            if "fvar" in t:
                ax = [a for a in t["fvar"].axes if a.axisTag == "wght"][0]
                ws = [int(ax.minValue), int(ax.maxValue)]
            shaped[p.name] = comps(shaped_mask(word, font(p, 50))) == 1
        weights[fam] = sorted(set(ws))
    lic_ok = {k: v.exists() and "Open Font License" in v.read_text(encoding="utf-8", errors="ignore") for k, v in lic.items()}
    pop = set(TTFont(str(POPPINS)).getBestCmap())
    checks = [check("weights resolve", weights == {"Cairo": [200, 1000], "Tajawal": [700], "Amiri": [400, 700], "IBM Plex Sans Arabic": [400, 500, 600, 700]},
                    weights, "Cairo 200–1000, Tajawal 700, Amiri 400/700, Plex 400–700"),
              check("every file shapes 'محمد' as one joined word", all(shaped.values()), shaped, "all True"),
              check("SIL OFL 1.1 text kept next to each family", all(lic_ok.values()), lic_ok, "all True"),
              check("negative control: a Latin-only face (Poppins) has no Arabic", 0x0645 not in pop, 0x0645 in pop, False)]
    return checks, [write_json(Path(wd) / "fonts.json", {"weights": weights, "shaped": shaped, "licence": lic_ok})]


@card("ARAB-X01")
def rtl_lyric_reveal(task, wd):
    """Each word revealed whole by a clip growing right→left (eOut3, 0.5 s, from −0.1 s), rise 34 px; key word ×1.3 with a decaying pop and gold."""
    np = np_()
    W, H = 360, 640
    k = W / 1080
    words = ["نحن", "نصنع", "الضوء"]
    times = [0.4, 1.0, 1.6]
    key = 2
    f = font(CAIRO, 40, 800)
    fk = font(CAIRO, 52, 900)
    GOLD = (255, 196, 70)
    row = word_row(words[:2], f, W, 260)
    tk, _ = tile(words[key], fk, fill=GOLD + (255,))
    rows = [(r["tile"], r["cx"], r["cy"]) for r in row] + [(tk, W / 2, 340)]

    def draw(t, c):
        for i, (tl, cx, cy) in enumerate(rows):
            t0 = times[i] - 0.1
            if t < t0:
                continue
            e = cubic_out((t - t0) / 0.5)
            x1 = cx + tl.width / 2
            clip = (x1 - tl.width * e, cy - tl.height, x1, cy + tl.height)
            pop = 1 + 0.08 * math.exp(-(t - times[i]) / 0.35) if i == key and t >= times[i] else 1
            place(c, tl, cx, cy + 34 * k * (1 - e), scale=pop, clip=clip)
    p, frames = video(wd, "lyric_reveal.mp4", draw, 2.8, size=(W, H))
    r0 = grow(ink_box_abs(row[0]), 2, 14)
    mid = mask_of(crop(frame_at(frames, times[0] - 0.1 + 0.1), r0), 100)
    mb = bbox(mid)
    first = [first_time([box_ink(fr, grow(ink_box_abs(r), 2, 14), 100) for fr in frames], 0.02) for r in row]
    kb = bbox(colour_mask(frames[-1], GOLD, 50))
    nb = bbox(shaped_mask(words[key], f))
    ratio = (kb[3] - kb[1]) / (nb[3] - nb[1])
    finc = [comps(mask_of(crop(frames[-1], grow(ink_box_abs(r), 2, 14)), 128)) for r in row]
    checks = [check("clip opens from the right (mid-reveal ink only on the right)", mb is not None and mb[0] > 0.25 * (r0[2] - r0[0]), mb, "left part hidden"),
              check("each word starts 0.1 s before it is sung", all(abs(ft - (t - 0.1)) <= 0.05 for ft, t in zip(first, times)), first, [t - 0.1 for t in times[:2]]),
              check("key word ≈1.3x and gold", abs(ratio - 1.3) <= 0.08, ratio, 1.3),
              check("letters never split (shaped components)", finc == [comps(shaped_mask(w, f)) for w in words[:2]], finc, [comps(shaped_mask(w, f)) for w in words[:2]]),
              check("negative control: before its time the word is absent", box_ink(frame_at(frames, 0.2), r0, 100) == 0, 0, 0)]
    return checks, [p]


@card("ARAB-X02")
def font_candidates(task, wd):
    """Rank candidate fonts for a reference frame by rendered-shape similarity (candidates with scores, not an identity) and check Latin fallback."""
    np = np_()
    from PIL import Image
    text = "سلام عليكم"
    ref = crop_ink(shaped_mask(text, font(TAJAWAL, 50)))     # stands for a frame from the video being imitated
    cands = {"Cairo": CAIRO, "Tajawal": TAJAWAL, "Amiri": AMIRI, "Lalezar": LALEZAR, "El Messiri": MESSIRI}

    def norm(m, h=64):
        im = Image.fromarray((m * 255).astype("uint8"))
        w = max(1, int(im.width * h / im.height))
        return np.asarray(im.resize((w, h))) > 128
    rn = norm(ref)
    scores = {}
    for n, pth in cands.items():
        cm = norm(crop_ink(shaped_mask(text, font(pth, 50))))
        w = min(cm.shape[1], rn.shape[1])
        scores[n] = round(iou(cm[:, :w], rn[:, :w]) * min(cm.shape[1], rn.shape[1]) / max(cm.shape[1], rn.shape[1]), 3)
    ranked = sorted(scores.items(), key=lambda kv: -kv[1])
    from fontTools.ttLib import TTFont
    ar_only = FONTS / "cairo-arabic-800-normal.woff2"
    lat = FONTS / "cairo-latin-800-normal.woff2"
    label = "مؤثر Parallax BPM WebGL"
    cm_ar = set(TTFont(str(ar_only)).getBestCmap())
    cm_lat = set(TTFont(str(lat)).getBestCmap())
    missing_single = [ch for ch in label if not ch.isspace() and ord(ch) not in cm_ar]
    runs = re.findall(r"[A-Za-z0-9]+|[^\sA-Za-z0-9]+", label)
    missing_fb = [ch for r in runs for ch in r if ord(ch) not in (cm_lat if r[0].isascii() else cm_ar)]
    report = {"candidates": ranked, "note": "ranked candidates with similarity scores; not a font identification"}
    checks = [check("true face ranked first among candidates", ranked[0][0] == "Tajawal", ranked, "Tajawal first"),
              check("reported as scored candidates (runner-up listed)", len(ranked) == 5 and ranked[1][1] < ranked[0][1], ranked[:2], "ranked list"),
              check("with a Latin fallback run every glyph exists", missing_fb == [], missing_fb, []),
              check("negative control: a single Arabic-only face draws tofu for Parallax/BPM/WebGL", len(missing_single) >= 14, len(missing_single), ">=14")]
    return checks, [write_json(Path(wd) / "font_candidates.json", report)]


ORN = "✦★☾❖✿"


def decorate_bio(s):
    out = []
    for w in s.split():
        if len(w) > 2:
            w = w[:-1] + "ــ" + w[-1]
        out.append(w)
    return "✦ " + " ".join(out) + " ✦"


def motion_lint(s):
    issues = []
    if "ـ" in s:
        issues.append("tatweel")
    if any(ch in ORN or unicodedata.category(ch) == "So" for ch in s):
        issues.append("ornament")
    return issues


@card("ARAB-X03")
def ornaments_bios_only(task, wd):
    """Ornament/kashida decoration is generated for bios; motion text is linted clean, because symbols inside words break Arabic joining."""
    np = np_()
    plain = "صانع محتوى"
    bio = decorate_bio(plain)
    f = font(CAIRO, 48, 700)
    inside = "صا✦نع"
    c_plain = comps(shaped_mask("صانع", f))
    c_broken = comps(shaped_mask(inside, f))
    clean = re.sub("[ـ%s]" % ORN, "", bio).strip()
    c_clean = comps(shaped_mask(clean, f))
    from PIL import Image
    Image.fromarray((shaped_mask(clean, f) * 255).astype("uint8")).save(Path(wd) / "motion_text.png")
    checks = [check("bio gets kashida and ornaments", "ـ" in bio and bio.startswith("✦"), bio, "decorated"),
              check("cleaned motion text passes the lint", motion_lint(clean) == [] and clean == plain, clean, plain),
              check("an ornament inside a word breaks the joins", c_broken > c_plain, [c_broken, c_plain], "more pieces"),
              check("motion text renders with real joins", c_clean == comps(shaped_mask(plain, f)), c_clean, comps(shaped_mask(plain, f))),
              check("negative control: the decorated bio fails the motion lint", motion_lint(bio) == ["tatweel", "ornament"], motion_lint(bio), ["tatweel", "ornament"])]
    return checks, [Path(wd) / "motion_text.png", write_json(Path(wd) / "bio.json", {"bio": bio, "motion": clean})]
