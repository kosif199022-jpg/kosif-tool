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
                     [("لا", False), ("تنتظر", False), ("الفرصة", True), ("اصنعها", False)]], lines, "one em per line"),
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
    b_early = bbox(colour_mask(frame_at(frames, at + 2 / 30), RED, 60))
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
              check("slams from ~1.6x", b_early is not None and (b_early[2] - b_early[0]) > 1.3 * (b_fin[2] - b_fin[0]),
                    b_early and (b_early[2] - b_early[0]) / (b_fin[2] - b_fin[0]), ">1.3"),
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
              check("soft glow around the rule", glow > 8, glow, ">8"),
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
    seek = tc.replace("</body>", "<script>addEventListener('load',()=>{const t=window.__timelines.root;t.seek(%s);});</script></body>")
    from PIL import Image
    d = Path(wd) / "projects/t-title-card"
    shots = []
    for tt in ("0.0", "2.5"):
        (d / ("seek_%s.html" % tt)).write_text(seek % tt, encoding="utf-8")
        exe = chrome_bin()
        out = d / ("frame_%s.png" % tt)
        subprocess.run([exe, "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--user-data-dir=%s" % (Path(wd) / ("ch" + tt)),
                        "--window-size=540,960", "--virtual-time-budget=3000", "--screenshot=%s" % out,
                        (d / ("seek_%s.html" % tt)).as_uri()], capture_output=True, timeout=40, stdin=subprocess.DEVNULL)
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
    W, H = 540, 960
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
