#!/usr/bin/env python3
"""KOSIF App Studio: the photo, design, type, procedural and download features of the analysed desktop apps
(DxO PhotoLab, Capture One, Lightroom/ACDSee, JPEGmini, Affinity Designer, Xara, FontLab, Houdini, Adobe Animate,
IDM, Canva) as one command line that works on the user's real files. Original code on open libraries; no vendor code.

    python scripts/app_studio.py doctor                 # what runs here, what is missing, the install line for it
    python scripts/app_studio.py ops [word]             # every operation with its app, APPX id and requirements
    python scripts/app_studio.py <op> IN [IN…] -o OUT [--set key=value …]
    python scripts/app_studio.py batch <op> IN_DIR -o OUT_DIR [--set …]   # every image in a folder

Examples:
    app_studio.py dehaze city.jpg -o city_clear.jpg --set strength=0.95
    app_studio.py develop raw.jpg -o out.jpg --set wb=grey exposure=0.3 curve=s vibrance=0.25
    app_studio.py jpegmini photo.jpg -o small.jpg --set delta=0.01
    app_studio.py watermark a.jpg -o b.jpg --set text="© KOSIF" opacity=0.4 pos=br
    app_studio.py font-build glyphs_dir -o Brand.ttf --set family="KOSIF Brand" kern="A V -80"
    app_studio.py catalog photos/ -o photos.db ; app_studio.py search photos.db --set q=sunset
    app_studio.py design post.json -o post.png          # Canva-style template: Arabic text, images, shapes, effects
    app_studio.py resize-design post.png -o sizes/ --set sizes=all   # Magic Resize to every platform

Every result prints one JSON line: {"op", "output", "metrics", "verified"}. "verified" is true only when the
operation measured its own postcondition (e.g. SSIM for jpegmini); it never claims more than it measured.
Paths with Arabic or other non-ASCII characters work on Windows (images are read with numpy, not cv2.imread).
"""
import argparse
import hashlib
import importlib
import json
import math
from pathlib import Path
import re
import shutil
import sqlite3
import sys
import threading
import time
import urllib.request

IMG_EXT = (".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".webp")
REQ = {  # requirement id (data/requirements.json) → (python module, pip install line)
    "pip:numpy": ("numpy", "pip install numpy"),
    "pip:opencv": ("cv2", "pip install opencv-python-headless"),
    "pip:pillow": ("PIL", "pip install pillow"),
    "pip:fonttools": ("fontTools", "pip install fonttools"),
    "pip:shapely": ("shapely", "pip install shapely"),
    "pip:segno": ("segno", "pip install segno"),
    "pip:matplotlib": ("matplotlib", "pip install matplotlib"),
    "pip:office": ("pptx", "pip install python-pptx"),
}
# Extras that only some settings of an op need: op → [(python module, pip install line, what needs it)].
# doctor keeps the op "ready" without them but lists the gap under "limited".
OPTIONAL = {
    "font-subset": [("brotli", "pip install brotli", "flavor=woff2")],
}
BASE = ["pip:numpy", "pip:opencv"]
OPS = {}


def op(name, app, appx, requires, ar, en):
    def deco(fn):
        OPS[name] = {"fn": fn, "app": app, "appx": appx, "requires": requires, "ar": ar, "en": en}
        return fn
    return deco


# ------------------------------------------------------------------ io helpers
def np_cv():
    import numpy as np
    import cv2
    return np, cv2


def read(path):
    """BGR uint8 image from any path (cv2.imread cannot open non-ASCII paths on Windows)."""
    np, cv2 = np_cv()
    data = np.fromfile(str(path), dtype=np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError(f"not an image: {path}")
    return img


def write(path, img, quality=95):
    np, cv2 = np_cv()
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    ext = path.suffix.lower() or ".png"
    params = [cv2.IMWRITE_JPEG_QUALITY, int(quality)] if ext in (".jpg", ".jpeg") else []
    ok, buf = cv2.imencode(ext, img, params)
    if not ok:
        raise ValueError(f"cannot encode {ext}")
    buf.tofile(str(path))
    return str(path)


def f(params, key, default):
    v = params.get(key, default)
    return type(default)(v) if default is not None and not isinstance(default, bool) else v


def psnr(a, b):
    np, _ = np_cv()
    mse = np.mean((a.astype(float) - b.astype(float)) ** 2)
    return 99.0 if mse == 0 else float(10 * np.log10(255.0 ** 2 / mse))


def ssim(a, b):
    np, cv2 = np_cv()
    if a.ndim == 3:
        a, b = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY), cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)
    a, b = a.astype(float), b.astype(float)
    c1, c2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2
    g = lambda x: cv2.GaussianBlur(x, (11, 11), 1.5)
    ma, mb = g(a), g(b)
    va, vb, cv = g(a * a) - ma * ma, g(b * b) - mb * mb, g(a * b) - ma * mb
    return float(np.mean(((2 * ma * mb + c1) * (2 * cv + c2)) / ((ma * ma + mb * mb + c1) * (va + vb + c2))))


def res(name, out, metrics=None, verified=False):
    return {"op": name, "output": out, "metrics": metrics or {}, "verified": verified}


# ------------------------------------------------------------------ photo: DxO PhotoLab / Capture One / Lightroom
@op("dehaze", "DxO ClearView", "APPX-31", BASE, "إزالة الضباب", "remove haze (dark-channel prior)")
def dehaze(inp, out, p):
    np, cv2 = np_cv()
    I = read(inp[0]).astype(float) / 255
    k = np.ones((int(f(p, "patch", 15)),) * 2)
    dark = cv2.erode(I.min(axis=2), k)
    n = max(1, dark.size // 1000)
    A = I.reshape(-1, 3)[np.argsort(dark.ravel())[-n:]].max(axis=0)
    t = 1 - f(p, "strength", 0.95) * cv2.erode((I / A).min(axis=2), k)
    t = cv2.blur(t, (31, 31)).clip(f(p, "t0", 0.1), 1)
    J = ((I - A) / t[..., None] + A).clip(0, 1)
    o = (J * 255).astype(np.uint8)
    return res("dehaze", write(out, o), {"contrast_before": float(I.std() * 255), "contrast_after": float(o.std())})


@op("denoise", "DxO Noise (High/Prime)", "APPX-32", BASE, "تقليل الضوضاء", "noise reduction: fast (bilateral) or nlm")
def denoise(inp, out, p):
    _, cv2 = np_cv()
    img = read(inp[0])
    if p.get("method", "nlm") == "fast":
        o = cv2.bilateralFilter(img, 7, f(p, "sigma", 40.0), 7)
    else:
        h = f(p, "h", 10.0)
        o = cv2.fastNlMeansDenoisingColored(img, None, h, h, 7, 21)
    return res("denoise", write(out, o), {"psnr_vs_input": psnr(img, o)})


def order_quad(q):
    np, _ = np_cv()
    s, d = q.sum(1), np.diff(q, axis=1).ravel()
    return np.float32([q[s.argmin()], q[d.argmin()], q[s.argmax()], q[d.argmax()]])


@op("keystone", "DxO Perspective / ViewPoint", "APPX-33", BASE, "تصحيح المنظور", "perspective: auto quad or points=x,y;x,y;x,y;x,y")
def keystone(inp, out, p):
    np, cv2 = np_cv()
    img = read(inp[0])
    h, w = img.shape[:2]
    if p.get("points"):
        quad = np.float32([[float(v) for v in xy.split(",")] for xy in p["points"].split(";")])
    else:   # largest 4-sided contour = the document / facade
        g = cv2.GaussianBlur(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), (5, 5), 0)
        e = cv2.dilate(cv2.Canny(g, 40, 120), None)
        cnts, _ = cv2.findContours(e, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        quad = None
        for c in sorted(cnts, key=cv2.contourArea, reverse=True)[:10]:
            a = cv2.approxPolyDP(c, 0.02 * cv2.arcLength(c, True), True)
            if len(a) == 4 and cv2.contourArea(a) > 0.2 * w * h:
                quad = a.reshape(4, 2).astype(np.float32)
                break
        if quad is None:
            raise ValueError("no quadrilateral found: pass --set points=x,y;x,y;x,y;x,y (TL;TR;BR;BL)")
    q = order_quad(quad)
    W = int(max(np.linalg.norm(q[0] - q[1]), np.linalg.norm(q[3] - q[2])))
    H = int(max(np.linalg.norm(q[0] - q[3]), np.linalg.norm(q[1] - q[2])))
    M = cv2.getPerspectiveTransform(q, np.float32([[0, 0], [W, 0], [W, H], [0, H]]))
    o = cv2.warpPerspective(img, M, (W, H))
    return res("keystone", write(out, o), {"corners": q.round(1).tolist(), "size": [W, H]})


@op("lens", "DxO Distortion, Affinity lens data", "APPX-34", BASE, "تصحيح تشوه العدسة", "undistort with k1 (k2, focal)")
def lens(inp, out, p):
    np, cv2 = np_cv()
    img = read(inp[0])
    h, w = img.shape[:2]
    fc = f(p, "focal", float(w))
    K = np.float32([[fc, 0, w / 2], [0, fc, h / 2], [0, 0, 1]])
    D = np.float32([f(p, "k1", -0.2), f(p, "k2", 0.0), 0, 0, 0])
    return res("lens", write(out, cv2.undistort(img, K, D)), {"k1": float(D[0]), "k2": float(D[1])})


@op("ca", "DxO ChromaticAberration", "APPX-35", BASE, "إزالة الزيغ اللوني", "register R/B to G by radial scale")
def ca(inp, out, p):
    np, cv2 = np_cv()
    img = read(inp[0])
    h, w = img.shape[:2]
    b, g, r = cv2.split(img)
    sc = lambda ch, s: cv2.warpAffine(ch, cv2.getRotationMatrix2D((w / 2, h / 2), 0, s), (w, h), borderMode=cv2.BORDER_REFLECT)
    m = max(8, min(h, w) // 12)
    grad = lambda ch: cv2.magnitude(cv2.Sobel(ch, cv2.CV_32F, 1, 0), cv2.Sobel(ch, cv2.CV_32F, 0, 1))
    gn = lambda ch: (lambda x: x / (x[m:-m, m:-m].mean() + 1e-6))(grad(ch))
    G = gn(g)
    def best(ch):   # edges line up when the channel is scaled right, whatever its brightness
        cands = np.linspace(0.97, 1.03, 121)
        return float(cands[int(np.argmin([np.abs(gn(sc(ch, s)) - G)[m:-m, m:-m].mean() for s in cands]))])
    sr, sb = best(r), best(b)
    return res("ca", write(out, cv2.merge([sc(b, sb), g, sc(r, sr)])), {"scale_r": sr, "scale_b": sb})


def apply_curve(img, name_or_pts):
    np, cv2 = np_cv()
    pts = {"s": [(0, 0), (64, 50), (128, 128), (192, 210), (255, 255)], "linear": [(0, 0), (255, 255)],
           "fade": [(0, 30), (128, 128), (255, 235)], "contrast": [(0, 0), (64, 40), (192, 220), (255, 255)]}.get(name_or_pts)
    if pts is None:
        pts = [tuple(float(v) for v in xy.split(",")) for xy in name_or_pts.split(";")]
    x, y = zip(*pts)
    return cv2.LUT(img, np.interp(np.arange(256), x, y).clip(0, 255).astype(np.uint8))


@op("develop", "DxO WhiteBalance/ToneCurve/HSL, Capture One, Lightroom Basic", "APPX-36", BASE,
    "تطوير: توازن أبيض وتعريض ومنحنى وتشبع", "wb=grey|none, temp, tint, exposure (EV), contrast, curve, saturation, vibrance")
def develop(inp, out, p):
    np, cv2 = np_cv()
    x = read(inp[0]).astype(float)
    if p.get("wb", "none") == "grey":
        m = x.reshape(-1, 3).mean(0)
        x *= m.mean() / m
    t, ti = f(p, "temp", 0.0), f(p, "tint", 0.0)          # −1…1
    x *= [1 - 0.2 * t, 1 + 0.1 * ti, 1 + 0.2 * t]          # BGR
    x *= 2 ** f(p, "exposure", 0.0)
    c = f(p, "contrast", 0.0)
    x = (x - 128) * (1 + c) + 128
    o = x.clip(0, 255).astype(np.uint8)
    if p.get("curve"):
        o = apply_curve(o, p["curve"])
    hsv = cv2.cvtColor(o, cv2.COLOR_BGR2HSV).astype(float)
    sat, vib = f(p, "saturation", 0.0), f(p, "vibrance", 0.0)
    hsv[..., 1] = hsv[..., 1] * (1 + sat) * (1 + vib * (1 - hsv[..., 1] / 255))   # vibrance lifts muted colours most
    o = cv2.cvtColor(hsv.clip(0, 255).astype(np.uint8), cv2.COLOR_HSV2BGR)
    m = o.reshape(-1, 3).mean(0)
    return res("develop", write(out, o), {"channel_means_bgr": m.round(1).tolist()})


@op("grain", "Capture One Film Grain, DxO Grain", "APPX-37", BASE, "حبيبات فيلم", "amount (σ), size")
def grain(inp, out, p):
    np, cv2 = np_cv()
    img = read(inp[0]).astype(np.float32)
    g = np.random.default_rng(int(f(p, "seed", 1))).normal(0, 1, img.shape[:2]).astype(np.float32)
    g = cv2.GaussianBlur(g, (0, 0), f(p, "size", 0.8))
    g = g / (g.std() + 1e-6) * f(p, "amount", 8.0)
    return res("grain", write(out, (img + g[..., None]).clip(0, 255).astype(np.uint8)), {"grain_sigma": f(p, "amount", 8.0)})


@op("vignette", "DxO CreativeVignetting, Lightroom", "APPX-37", BASE, "تعتيم الأطراف", "amount 0..1, start radius")
def vignette(inp, out, p):
    np, _ = np_cv()
    img = read(inp[0]).astype(float)
    h, w = img.shape[:2]
    yy, xx = np.indices((h, w))
    r = np.hypot((xx - w / 2) / (w / 2), (yy - h / 2) / (h / 2))
    v = 1 - f(p, "amount", 0.45) * np.clip(r - f(p, "start", 0.4), 0, None) ** 1.5
    o = (img * v[..., None]).clip(0, 255).astype(np.uint8)
    return res("vignette", write(out, o), {"corner_gain": float(v[0, 0])})


@op("watermark", "DxO Watermark, Lightroom export", "APPX-38", ["pip:pillow"] + BASE, "علامة مائية", "text= or logo=, opacity, pos=br|bl|tr|tl|c, size")
def watermark(inp, out, p):
    from PIL import Image, ImageDraw, ImageFont, features
    import numpy as np
    base = Image.open(inp[0]).convert("RGBA")
    W, H = base.size
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    op_ = f(p, "opacity", 0.4)
    if p.get("logo"):
        logo = Image.open(p["logo"]).convert("RGBA")
        s = f(p, "size", 0.2) * W / logo.width
        logo = logo.resize((max(1, int(logo.width * s)), max(1, int(logo.height * s))))
        logo.putalpha(Image.fromarray((np.array(logo.getchannel("A")) * op_).astype("uint8")))
        mark, box = logo, logo.size
    else:
        text = p.get("text", "© KOSIF")
        size = int(f(p, "size", 0.05) * W) or 12
        font = None
        is_ar = bool(re.search(r"[\u0600-\u06FF]", text))
        if is_ar and not features.check("raqm"):   # no libraqm: shape and reorder ourselves so letters join
            try:
                import arabic_reshaper
                from bidi.algorithm import get_display
                text = get_display(arabic_reshaper.reshape(text))
            except ImportError:
                pass
        bundled = Path(__file__).resolve().parents[1] / "proofs" / "_shared" / "fonts" / "Amiri-Bold.ttf"
        for cand in [p.get("font")] + ([str(bundled)] if is_ar else []) + [r"C:\Windows\Fonts\arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
            if cand and Path(cand).is_file():
                kw = {"layout_engine": ImageFont.Layout.RAQM} if features.check("raqm") else {}
                font = ImageFont.truetype(cand, size, **kw)
                break
        font = font or ImageFont.load_default()
        d = ImageDraw.Draw(layer)
        bb = d.textbbox((0, 0), text, font=font)
        box, mark = (bb[2] - bb[0], bb[3] - bb[1]), None
    m = int(0.03 * W)
    pos = {"br": (W - box[0] - m, H - box[1] - m), "bl": (m, H - box[1] - m), "tr": (W - box[0] - m, m),
           "tl": (m, m), "c": ((W - box[0]) // 2, (H - box[1]) // 2)}[p.get("pos", "br")]
    if mark is not None:
        layer.paste(mark, pos)            # copy RGBA as is: its alpha already carries the opacity
    else:
        ImageDraw.Draw(layer).text(pos, text, font=font, fill=(255, 255, 255, int(255 * op_)))
    o = Image.alpha_composite(base, layer).convert("RGB")
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    o.save(out, quality=95)
    shaping = None
    if re.search(r"[\u0600-\u06FF]", p.get("text", "")):
        shaping = "raqm" if features.check("raqm") else ("arabic-reshaper+bidi" if text != p.get("text") else "none: letters will not join")
    return res("watermark", str(out), {"position": pos, "opacity": op_, "arabic_shaping": shaping})


@op("jpegmini", "JPEGmini", "APPX-39", ["pip:pillow"] + BASE, "ضغط JPEG إدراكي", "smallest quality within delta SSIM of q95")
def jpegmini(inp, out, p):
    import io
    from PIL import Image
    import numpy as np
    src = Image.open(inp[0]).convert("RGB")
    ref_arr = np.array(src)[..., ::-1]
    def enc(q):
        b = io.BytesIO(); src.save(b, "JPEG", quality=q, optimize=True, progressive=True); return b.getvalue()
    score = lambda d: ssim(np.array(Image.open(io.BytesIO(d)).convert("RGB"))[..., ::-1], ref_arr)
    ref = enc(95)
    target = score(ref) - f(p, "delta", 0.01)
    lo, hi, best = int(f(p, "min_q", 30)), 95, 95
    while lo <= hi:
        mid = (lo + hi) // 2
        if score(enc(mid)) >= target:
            best, hi = mid, mid - 1
        else:
            lo = mid + 1
    data = enc(best)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_bytes(data)
    s = score(data)
    orig = Path(inp[0]).stat().st_size
    return res("jpegmini", str(out), {"quality": best, "ssim": round(s, 4), "target": round(target, 4),
                                      "bytes": len(data), "input_bytes": orig, "saved_pct": round(100 - 100 * len(data) / orig, 1)},
               verified=s >= target)


@op("contact-sheet", "Capture One PrintTemplates, Lightroom Print", "APPX-40", ["pip:pillow"], "ورقة تواصل PDF", "cols, rows, page=A4|letter, title")
def contact_sheet(inp, out, p):
    from PIL import Image, ImageDraw
    files = expand(inp)
    cols, rows = int(f(p, "cols", 4)), int(f(p, "rows", 5))
    pw, ph = (2480, 3508) if p.get("page", "A4") == "A4" else (2550, 3300)
    cw, ch = (pw - 200) // cols, (ph - 300) // rows
    pages = []
    for i0 in range(0, len(files), cols * rows):
        pg = Image.new("RGB", (pw, ph), "white")
        d = ImageDraw.Draw(pg)
        d.text((100, 80), p.get("title", ""), fill="black")
        for i, fp in enumerate(files[i0:i0 + cols * rows]):
            t = Image.open(fp).convert("RGB")
            t.thumbnail((cw - 30, ch - 70))
            x, y = 100 + (i % cols) * cw, 200 + (i // cols) * ch
            pg.paste(t, (x, y))
            d.text((x, y + t.height + 8), Path(fp).name[:40], fill="black")
        pages.append(pg)
    if not pages:
        raise ValueError("no images")
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    pages[0].save(out, save_all=True, append_images=pages[1:], resolution=300)
    return res("contact-sheet", str(out), {"images": len(files), "pages": len(pages)})


@op("preset", "Capture One Styles, DxO presets, Lightroom presets", "APPX-41", BASE, "تطبيق إعداد مسبق", "preset=file.json (ops: develop/grain/vignette/curve…)")
def preset(inp, out, p):
    spec = json.loads(Path(p["preset"]).read_text(encoding="utf-8"))
    if spec.get("schema", 1) == 1 and "warmth" in spec:   # v1 files keep opening
        spec = {"schema": 2, "ops": [{"op": "develop", "temp": spec.pop("warmth")}] + spec.get("ops", [])}
    cur, tmp = inp[0], []
    for i, step in enumerate(spec["ops"]):
        name = step.pop("op")
        nxt = str(Path(out).with_name(f".{Path(out).stem}.step{i}.png"))
        OPS[name]["fn"]([cur], nxt, {k: str(v) for k, v in step.items()})
        tmp.append(nxt)
        cur = nxt
    write(out, read(cur))
    for t in tmp:
        Path(t).unlink(missing_ok=True)
    return res("preset", str(out), {"steps": len(spec["ops"]), "schema": spec.get("schema", 1)})


XMP_NS = {"x": "adobe:ns:meta/", "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
          "xmp": "http://ns.adobe.com/xap/1.0/", "dc": "http://purl.org/dc/elements/1.1/"}


def xmp_read(side):
    import xml.etree.ElementTree as ET
    if not Path(side).is_file():
        return {}
    r = ET.parse(side).getroot()
    d = r.find(f".//{{{XMP_NS['rdf']}}}Description")
    return {"rating": int(d.get(f"{{{XMP_NS['xmp']}}}Rating", 0)) if d is not None else 0,
            "label": d.get(f"{{{XMP_NS['xmp']}}}Label", "") if d is not None else "",
            "keywords": [li.text for li in r.iter(f"{{{XMP_NS['rdf']}}}li") if li.text]}


@op("xmp", "Lightroom, ACDSee, DxO Search.Metadata, Affinity libxmp", "APPX-42", [], "ملف XMP جانبي", "rating 0-5, label, keywords=a,b (adds), read=1")
def xmp(inp, out, p):
    import xml.etree.ElementTree as ET
    side = Path(out) if out else Path(inp[0]).with_suffix(".xmp")
    cur = xmp_read(side)
    if p.get("read"):
        return res("xmp", str(side), cur, verified=True)
    for k, v in XMP_NS.items():
        ET.register_namespace(k, v)
    root = ET.Element(f"{{{XMP_NS['x']}}}xmpmeta")
    rdf = ET.SubElement(root, f"{{{XMP_NS['rdf']}}}RDF")
    attrs = {f"{{{XMP_NS['xmp']}}}Rating": str(int(p.get("rating", cur.get("rating", 0)))),
             f"{{{XMP_NS['xmp']}}}Label": p.get("label", cur.get("label", ""))}
    d = ET.SubElement(rdf, f"{{{XMP_NS['rdf']}}}Description", attrs)
    bag = ET.SubElement(ET.SubElement(d, f"{{{XMP_NS['dc']}}}subject"), f"{{{XMP_NS['rdf']}}}Bag")
    kws = list(dict.fromkeys(cur.get("keywords", []) + [k.strip() for k in p.get("keywords", "").split(",") if k.strip()]))
    for k in kws:
        ET.SubElement(bag, f"{{{XMP_NS['rdf']}}}li").text = k
    ET.ElementTree(root).write(side, encoding="utf-8", xml_declaration=True)
    back = xmp_read(side)
    return res("xmp", str(side), back, verified=back["keywords"] == kws)


@op("horizon", "DxO Horizon, Capture One AutoCrop", "APPX-43", BASE, "تقويم الأفق", "auto angle from long lines (or angle=), crop=1")
def horizon(inp, out, p):
    np, cv2 = np_cv()
    img = read(inp[0])
    h, w = img.shape[:2]
    if "angle" in p:
        ang = float(p["angle"])
    else:
        e = cv2.Canny(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 50, 150)
        L = cv2.HoughLinesP(e, 1, np.pi / 720, 100, minLineLength=w // 3, maxLineGap=10)
        angs = [math.degrees(math.atan2(y2 - y1, x2 - x1)) for x1, y1, x2, y2 in (L.reshape(-1, 4) if L is not None else [])]
        angs = [a for a in angs if abs(a) < 20]
        if not angs:
            raise ValueError("no long near-horizontal line: pass --set angle=")
        ang = float(np.median(angs))
    o = cv2.warpAffine(img, cv2.getRotationMatrix2D((w / 2, h / 2), ang, 1.0), (w, h), borderMode=cv2.BORDER_REPLICATE)
    if p.get("crop", "1") == "1":   # largest axis-aligned rectangle inside the rotated frame
        a = math.radians(abs(ang))
        cw = int((w * math.cos(a) - h * math.sin(a)) / math.cos(2 * a)) if abs(math.cos(2 * a)) > 1e-6 else w
        chh = int((h * math.cos(a) - w * math.sin(a)) / math.cos(2 * a)) if abs(math.cos(2 * a)) > 1e-6 else h
        cw, chh = max(1, min(w, cw)), max(1, min(h, chh))
        o = o[(h - chh) // 2:(h + chh) // 2, (w - cw) // 2:(w + cw) // 2]
    return res("horizon", write(out, o), {"angle_deg": round(ang, 2)})


@op("hdr", "DxO Smart Lighting, Lightroom HDR merge", "APPX-50", BASE, "دمج تعريضات HDR", "2+ bracketed images → exposure fusion")
def hdr(inp, out, p):
    np, cv2 = np_cv()
    imgs = [read(x) for x in inp]
    h, w = imgs[0].shape[:2]
    imgs = [cv2.resize(i, (w, h)) for i in imgs]
    if len(imgs) == 1:   # single image: CLAHE on L as "smart lighting"
        lab = cv2.cvtColor(imgs[0], cv2.COLOR_BGR2LAB)
        lab[..., 0] = cv2.createCLAHE(f(p, "clip", 2.0), (8, 8)).apply(lab[..., 0])
        o = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    else:
        cv2.createAlignMTB().process(imgs, imgs)
        o = (cv2.createMergeMertens().process(imgs).clip(0, 1) * 255).astype(np.uint8)
    return res("hdr", write(out, o), {"inputs": len(imgs), "clipped_hi_pct": float((o >= 250).mean() * 100)})


@op("sharpen", "DxO UnsharpMask, Lightroom Detail", "APPX-61", BASE, "توضيح الحدة", "amount, radius, threshold")
def sharpen(inp, out, p):
    np, cv2 = np_cv()
    img = read(inp[0]).astype(float)
    blur = cv2.GaussianBlur(img, (0, 0), f(p, "radius", 1.2))
    diff = img - blur
    mask = np.abs(diff) > f(p, "threshold", 2.0)
    o = (img + f(p, "amount", 0.8) * diff * mask).clip(0, 255).astype(np.uint8)
    return res("sharpen", write(out, o), {"laplacian_var_before": float(cv2.Laplacian(img.astype(np.uint8), cv2.CV_64F).var()),
                                          "laplacian_var_after": float(cv2.Laplacian(o, cv2.CV_64F).var())})


@op("clarity", "DxO Texture/Microcontrast, Lightroom Clarity", "APPX-62", BASE, "وضوح وملمس", "amount (−1..1), radius (large = clarity, small = texture)")
def clarity(inp, out, p):
    np, cv2 = np_cv()
    img = read(inp[0])
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).astype(float)
    L = lab[..., 0].copy()
    base = cv2.bilateralFilter(L.astype(np.float32), 0, 25, f(p, "radius", 20.0))
    lab[..., 0] = (L + f(p, "amount", 0.5) * (L - base)).clip(0, 255)
    o = cv2.cvtColor(lab.astype(np.uint8), cv2.COLOR_LAB2BGR)
    return res("clarity", write(out, o), {"local_contrast_before": float((L - base).std()),
                                          "local_contrast_after": float((lab[..., 0] - base).std())})


HUE_BANDS = {"red": 0, "orange": 15, "yellow": 30, "green": 60, "aqua": 90, "blue": 120, "purple": 140, "magenta": 160}


@op("hsl", "DxO HSL / ColorAccentuation, Lightroom HSL, Capture One Color Editor", "APPX-63", BASE,
    "تحكم لوني لكل نطاق", "band=green hue=+10 sat=-0.5 lum=+0.2 (bands: red orange yellow green aqua blue purple magenta)")
def hsl(inp, out, p):
    np, cv2 = np_cv()
    hls = cv2.cvtColor(read(inp[0]), cv2.COLOR_BGR2HLS).astype(float)
    centre = HUE_BANDS[p.get("band", "green")]
    dist = np.minimum(np.abs(hls[..., 0] - centre), 180 - np.abs(hls[..., 0] - centre))
    wgt = np.clip(1 - dist / 22, 0, 1) * (hls[..., 2] > 20)
    hls[..., 0] = (hls[..., 0] + wgt * f(p, "hue", 0.0)) % 180
    hls[..., 2] = (hls[..., 2] * (1 + wgt * f(p, "sat", 0.0))).clip(0, 255)
    hls[..., 1] = (hls[..., 1] * (1 + wgt * f(p, "lum", 0.0))).clip(0, 255)
    o = cv2.cvtColor(hls.astype(np.uint8), cv2.COLOR_HLS2BGR)
    return res("hsl", write(out, o), {"band": p.get("band", "green"), "pixels_in_band_pct": float((wgt > 0.5).mean() * 100)})


@op("bw", "DxO ChannelMixer, Lightroom B&W, Capture One Black and White", "APPX-64", BASE,
    "أبيض وأسود بخلط القنوات", "r g b weights (default 0.3 0.59 0.11), tone=sepia|none")
def bw(inp, out, p):
    np, cv2 = np_cv()
    img = read(inp[0]).astype(float)
    wr, wg, wb = f(p, "r", 0.3), f(p, "g", 0.59), f(p, "b", 0.11)
    s = wr + wg + wb or 1
    y = (img[..., 2] * wr + img[..., 1] * wg + img[..., 0] * wb) / s
    o = np.repeat(y[..., None], 3, axis=2)
    if p.get("tone") == "sepia":
        o = o * [0.82, 0.95, 1.08]
    return res("bw", write(out, o.clip(0, 255).astype(np.uint8)), {"weights": [wr, wg, wb]})


@op("split-tone", "DxO Toning, Lightroom Color Grading", "APPX-65", BASE, "تلوين الظلال والإضاءات", "shadows=#hex highlights=#hex balance amount")
def split_tone(inp, out, p):
    np, cv2 = np_cv()
    img = read(inp[0]).astype(float)
    hx = lambda s: np.array([int(s.lstrip("#")[i:i + 2], 16) for i in (4, 2, 0)], float)   # → BGR
    sh, hi = hx(p.get("shadows", "#1e5a8c")), hx(p.get("highlights", "#ffb46e"))
    L = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(float) / 255
    bal = f(p, "balance", 0.5)
    ws, wh = np.clip((bal - L) / bal, 0, 1)[..., None], np.clip((L - bal) / (1 - bal), 0, 1)[..., None]
    a = f(p, "amount", 0.25)
    o = img * (1 - a * (ws + wh)) + a * (ws * sh + wh * hi)
    return res("split-tone", write(out, o.clip(0, 255).astype(np.uint8)), {"amount": a})


@op("redeye", "DxO RedEyes", "APPX-66", BASE, "إزالة احمرار العين", "auto (eye detector) or box=x,y,w,h")
def redeye(inp, out, p):
    np, cv2 = np_cv()
    img = read(inp[0])
    if p.get("box"):
        boxes = [tuple(int(v) for v in p["box"].split(","))]
    else:   # compact, saturated red blobs (pupils lit by flash); works without a face model
        b_, g_, r_ = cv2.split(img.astype(np.int32))
        red = ((r_ > 120) & (r_ > 2 * np.maximum(g_, b_))).astype(np.uint8)
        n, _, stats, _ = cv2.connectedComponentsWithStats(red)
        boxes = []
        for x, y, w, h, area in stats[1:]:
            if 12 <= area <= img.shape[0] * img.shape[1] * 0.002 and 0.6 < w / max(h, 1) < 1.6 and area > 0.5 * w * h:
                boxes.append((max(0, x - 2), max(0, y - 2), w + 4, h + 4))
    fixed = 0
    for x, y, w, h in boxes:
        roi = img[y:y + h, x:x + w].astype(float)
        b, g, r = roi[..., 0], roi[..., 1], roi[..., 2]
        mask = (r > 80) & (r > 1.5 * (b + g) / 2)
        mean_bg = (b + g) / 2
        roi[..., 2] = np.where(mask, mean_bg, r)
        img[y:y + h, x:x + w] = roi.astype(np.uint8)
        fixed += int(mask.sum())
    return res("redeye", write(out, img), {"regions": len(boxes), "pixels_fixed": fixed})


@op("repair", "DxO Repair, Lightroom Heal/Remove, Affinity Inpainting", "APPX-67", BASE,
    "إزالة عنصر/ترميم", "mask=mask.png (white = remove) or box=x,y,w,h; method=telea|ns")
def repair(inp, out, p):
    np, cv2 = np_cv()
    img = read(inp[0])
    if p.get("mask"):
        m = cv2.imdecode(np.fromfile(p["mask"], np.uint8), cv2.IMREAD_GRAYSCALE)
        m = (cv2.resize(m, img.shape[1::-1]) > 127).astype(np.uint8) * 255
    else:
        x, y, w, h = (int(v) for v in p["box"].split(","))
        m = np.zeros(img.shape[:2], np.uint8)
        m[y:y + h, x:x + w] = 255
    m = cv2.dilate(m, np.ones((5, 5), np.uint8))
    flag = cv2.INPAINT_NS if p.get("method") == "ns" else cv2.INPAINT_TELEA
    o = cv2.inpaint(img, m, f(p, "radius", 7.0), flag)
    return res("repair", write(out, o), {"masked_pct": float((m > 0).mean() * 100)})


@op("moire", "DxO Moire", "APPX-68", BASE, "إزالة التموج (مواريه)", "FFT notch of periodic peaks; strength")
def moire(inp, out, p):
    np, cv2 = np_cv()
    img = read(inp[0]).astype(np.float32)
    h, w = img.shape[:2]
    out_ch = []
    yy, xx = np.indices((h, w))
    r0 = np.hypot(yy - h / 2, xx - w / 2)
    removed = 0
    for c in cv2.split(img):
        F = np.fft.fftshift(np.fft.fft2(c))
        mag = np.log1p(np.abs(F))
        local = cv2.GaussianBlur(mag, (0, 0), 6)
        peaks = (mag - local > f(p, "strength", 2.5)) & (r0 > min(h, w) * 0.06)
        removed += int(peaks.sum())
        F[cv2.dilate(peaks.astype(np.uint8), np.ones((5, 5))) > 0] = 0
        out_ch.append(np.real(np.fft.ifft2(np.fft.ifftshift(F))))
    o = cv2.merge(out_ch).clip(0, 255).astype(np.uint8)
    return res("moire", write(out, o), {"frequency_peaks_removed": removed})


@op("tilt-shift", "DxO TiltShift", "APPX-69", BASE, "تأثير المجسم (تلت-شيفت)", "center 0..1, band, blur, saturation")
def tilt_shift(inp, out, p):
    np, cv2 = np_cv()
    img = read(inp[0])
    h = img.shape[0]
    blur = cv2.GaussianBlur(img, (0, 0), f(p, "blur", 8.0))
    y = np.arange(h) / h
    m = np.clip((np.abs(y - f(p, "center", 0.55)) - f(p, "band", 0.08)) / 0.2, 0, 1)[:, None, None]
    o = (img * (1 - m) + blur * m).astype(np.uint8)
    hsv = cv2.cvtColor(o, cv2.COLOR_BGR2HSV).astype(float)
    hsv[..., 1] = (hsv[..., 1] * (1 + f(p, "saturation", 0.3))).clip(0, 255)
    return res("tilt-shift", write(out, cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)), {})


@op("bg-blur", "DxO CreativeBlur, Lightroom Lens Blur", "APPX-70", BASE, "تغبيش الخلفية", "auto subject (GrabCut) or box=x,y,w,h; blur")
def bg_blur(inp, out, p):
    np, cv2 = np_cv()
    img = read(inp[0])
    h, w = img.shape[:2]
    rect = tuple(int(v) for v in p["box"].split(",")) if p.get("box") else (int(w * .2), int(h * .1), int(w * .6), int(h * .85))
    mask = np.zeros((h, w), np.uint8)
    cv2.grabCut(img, mask, rect, np.zeros((1, 65)), np.zeros((1, 65)), 4, cv2.GC_INIT_WITH_RECT)
    fg = np.isin(mask, (1, 3)).astype(np.float32)
    fg = cv2.GaussianBlur(fg, (0, 0), 3)[..., None]
    o = (img * fg + cv2.GaussianBlur(img, (0, 0), f(p, "blur", 12.0)) * (1 - fg)).astype(np.uint8)
    return res("bg-blur", write(out, o), {"subject_pct": float((fg > 0.5).mean() * 100)})


@op("crop", "Lightroom/Capture One crop, DxO Crop", "APPX-71", BASE, "قص بنسبة", "aspect=1:1|4:5|9:16|16:9, focus=center|subject")
def crop(inp, out, p):
    np, cv2 = np_cv()
    img = read(inp[0])
    h, w = img.shape[:2]
    a, b = (float(v) for v in p.get("aspect", "1:1").split(":"))
    r = a / b
    cw, ch = (int(h * r), h) if w / h > r else (w, int(w / r))
    cx, cy = w / 2, h / 2
    if p.get("focus") == "subject":   # saliency by spectral residual-free proxy: gradient energy centroid
        g = cv2.GaussianBlur(np.abs(cv2.Laplacian(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), cv2.CV_32F)), (0, 0), 15)
        ys, xs = np.indices(g.shape)
        cx, cy = float((g * xs).sum() / g.sum()), float((g * ys).sum() / g.sum())
    x0 = int(min(max(cx - cw / 2, 0), w - cw))
    y0 = int(min(max(cy - ch / 2, 0), h - ch))
    return res("crop", write(out, img[y0:y0 + ch, x0:x0 + cw]), {"box": [x0, y0, cw, ch]})


@op("resize", "JPEGmini/Lightroom export, ACDSee batch resize", "APPX-72", BASE, "تغيير المقاس", "long=2048 or width= / height=, sharpen=1")
def resize(inp, out, p):
    _, cv2 = np_cv()
    img = read(inp[0])
    h, w = img.shape[:2]
    if "width" in p:
        s = float(p["width"]) / w
    elif "height" in p:
        s = float(p["height"]) / h
    else:
        s = float(p.get("long", 2048)) / max(w, h)
    o = cv2.resize(img, (max(1, round(w * s)), max(1, round(h * s))), interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_LANCZOS4)
    if p.get("sharpen") == "1" and s < 1:
        o = cv2.addWeighted(o, 1.3, cv2.GaussianBlur(o, (0, 0), 0.8), -0.3, 0)
    return res("resize", write(out, o, int(f(p, "quality", 92))), {"size": [o.shape[1], o.shape[0]]})


@op("icc", "Capture One camera profiles, DxO ICC / soft-proof", "APPX-53", ["pip:pillow"], "تحويل ملف اللون", "to=srgb|path.icc, from=path.icc (default: embedded or sRGB)")
def icc(inp, out, p):
    import io
    from PIL import Image, ImageCms
    im = Image.open(inp[0])
    src = ImageCms.ImageCmsProfile(io.BytesIO(im.info["icc_profile"])) if im.info.get("icc_profile") else \
        (ImageCms.getOpenProfile(p["from"]) if p.get("from") else ImageCms.createProfile("sRGB"))
    dst = ImageCms.createProfile("sRGB") if p.get("to", "srgb") == "srgb" else ImageCms.getOpenProfile(p["to"])
    mode = "CMYK" if p.get("to", "").lower().endswith(".icc") and "cmyk" in p.get("to", "").lower() else "RGB"
    o = ImageCms.profileToProfile(im.convert("RGB"), src, dst, outputMode=mode)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    o.save(out)
    return res("icc", str(out), {"mode": o.mode, "had_embedded_profile": bool(im.info.get("icc_profile"))})


@op("auto-tone", "Lightroom Auto, ACDSee Auto Lighting, DxO Smart Lighting", "APPX-73", BASE, "ضبط تلقائي للإضاءة", "clip % for levels")
def auto_tone(inp, out, p):
    np, cv2 = np_cv()
    img = read(inp[0])
    c = f(p, "clip", 0.5)
    o = np.empty_like(img)
    for i in range(3):
        lo, hi = np.percentile(img[..., i], (c, 100 - c))
        o[..., i] = ((img[..., i].astype(float) - lo) * 255 / max(hi - lo, 1)).clip(0, 255)
    return res("auto-tone", write(out, o), {"std_before": float(img.std()), "std_after": float(o.std())})


# ------------------------------------------------------------------ library: ACDSee / Lightroom catalog
def expand(inp):
    files = []
    for x in inp:
        q = Path(x)
        files += sorted(y for y in q.rglob("*") if y.suffix.lower() in IMG_EXT) if q.is_dir() else [q]
    return [str(x) for x in files]


def exif_of(path):
    from PIL import Image, ExifTags
    try:
        ex = Image.open(path).getexif()
    except Exception:
        return {}
    d = {ExifTags.TAGS.get(k, str(k)): v for k, v in ex.items()}
    gps = ex.get_ifd(0x8825) if hasattr(ex, "get_ifd") else {}
    out = {k: str(d[k]) for k in ("DateTime", "Make", "Model", "Software") if k in d}
    if gps and 2 in gps and 4 in gps:
        conv = lambda v, ref: (float(v[0]) + float(v[1]) / 60 + float(v[2]) / 3600) * (-1 if ref in ("S", "W") else 1)
        out["lat"], out["lon"] = conv(gps[2], gps.get(1, "N")), conv(gps[4], gps.get(3, "E"))
    return out


@op("exif", "ACDSee/Lightroom metadata panel", "APPX-74", ["pip:pillow"], "قراءة بيانات الصورة وGPS", "prints EXIF incl. GPS as JSON")
def exif(inp, out, p):
    data = {Path(x).name: exif_of(x) for x in expand(inp)}
    if out:
        Path(out).write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    return res("exif", out, data, verified=True)


def dhash(path, size=8):
    np, cv2 = np_cv()
    g = cv2.resize(cv2.cvtColor(read(path), cv2.COLOR_BGR2GRAY), (size + 1, size), interpolation=cv2.INTER_AREA)
    bits = (g[:, 1:] > g[:, :-1]).ravel()
    return int("".join("1" if b else "0" for b in bits), 2)


@op("dedupe", "ACDSee Duplicate Finder, Lightroom", "APPX-75", BASE, "كشف الصور المكررة والمتشابهة", "threshold (Hamming bits, default 6)")
def dedupe(inp, out, p):
    files = expand(inp)
    hs = {x: dhash(x) for x in files}
    t, groups, seen = int(f(p, "threshold", 6)), [], set()
    for a in files:
        if a in seen:
            continue
        g = [b for b in files if b not in seen and bin(hs[a] ^ hs[b]).count("1") <= t]
        seen.update(g)
        if len(g) > 1:
            groups.append(g)
    if out:
        Path(out).write_text(json.dumps(groups, ensure_ascii=False, indent=1), encoding="utf-8")
    return res("dedupe", out, {"files": len(files), "duplicate_groups": groups})


@op("faces", "ACDSee/Lightroom People, Capture One", "APPX-76", BASE, "كشف الوجوه", "boxes as JSON; draw=1 writes a preview")
def faces(inp, out, p):
    _, cv2 = np_cv()
    img = read(inp[0])
    model = p.get("model") or __import__("os").environ.get("KOSIF_YUNET", "")
    if hasattr(cv2, "CascadeClassifier"):
        casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        boxes = casc.detectMultiScale(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 1.1, 5, minSize=(30, 30))
    elif model and Path(model).is_file():
        det = cv2.FaceDetectorYN.create(model, "", (img.shape[1], img.shape[0]), float(p.get("score", 0.8)))
        _, found = det.detect(img)
        boxes = [] if found is None else [b[:4] for b in found]
    else:
        raise RuntimeError("no face detector in this OpenCV build (5.x removed Haar cascades): pass --set model=face_detection_yunet_2023mar.onnx "
                           "(opencv_zoo, Apache-2.0) or set KOSIF_YUNET, or pip install \"opencv-contrib-python<5\"")
    if out and p.get("draw", "1") == "1":
        for x, y, w, h in boxes:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 220, 255), 2)
        write(out, img)
    return res("faces", out, {"faces": boxes, "count": len(boxes)})


@op("rename", "ACDSee/Lightroom batch rename", "APPX-77", ["pip:pillow"], "إعادة تسمية دفعة", "pattern={date}_{n:04d}{ext} (date from EXIF), dry=1")
def rename(inp, out, p):
    files = expand(inp)
    pat, plan = p.get("pattern", "{date}_{n:04d}{ext}"), []
    for n, x in enumerate(files, 1):
        dt = exif_of(x).get("DateTime", time.strftime("%Y:%m:%d %H:%M:%S", time.localtime(Path(x).stat().st_mtime)))
        date = dt.replace(":", "-").replace(" ", "_")
        new = Path(x).with_name(pat.format(date=date, n=n, ext=Path(x).suffix.lower(), stem=Path(x).stem))
        plan.append([x, str(new)])
    if p.get("dry", "1") != "1":
        for a, b in plan:
            if not Path(b).exists():
                Path(a).rename(b)
    return res("rename", None, {"plan": plan, "applied": p.get("dry", "1") != "1"})


@op("catalog", "Lightroom Catalog, ACDSee database", "APPX-78", ["pip:pillow"] + BASE, "فهرسة مكتبة الصور", "folder → SQLite (path, size, exif, gps, rating, keywords, dhash)")
def catalog(inp, out, p):
    db = sqlite3.connect(out)
    db.execute("CREATE TABLE IF NOT EXISTS photos(path TEXT PRIMARY KEY, bytes INT, width INT, height INT, taken TEXT, camera TEXT,"
               " lat REAL, lon REAL, rating INT, label TEXT, keywords TEXT, dhash TEXT)")
    from PIL import Image
    n = 0
    for x in expand(inp):
        e, xm = exif_of(x), xmp_read(Path(x).with_suffix(".xmp"))
        with Image.open(x) as im:
            W, H = im.size
        db.execute("INSERT OR REPLACE INTO photos VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                   (x, Path(x).stat().st_size, W, H, e.get("DateTime"), " ".join(filter(None, [e.get("Make"), e.get("Model")])),
                    e.get("lat"), e.get("lon"), xm.get("rating", 0), xm.get("label", ""), ",".join(xm.get("keywords", [])),
                    format(dhash(x), "016x")))
        n += 1
    db.commit()
    total = db.execute("SELECT COUNT(*) FROM photos").fetchone()[0]
    db.close()   # Windows keeps an open SQLite file locked
    return res("catalog", str(out), {"indexed": n, "total": total})


@op("search", "Lightroom/ACDSee search and smart collections", "APPX-78", [], "بحث في المكتبة", "q=word, min_rating=, camera=")
def search(inp, out, p):
    db = sqlite3.connect(inp[0])
    q, args = "SELECT path, rating, keywords, taken FROM photos WHERE 1=1", []
    if p.get("q"):
        q += " AND (keywords LIKE ? OR path LIKE ?)"; args += [f"%{p['q']}%"] * 2
    if p.get("min_rating"):
        q += " AND rating >= ?"; args.append(int(p["min_rating"]))
    if p.get("camera"):
        q += " AND camera LIKE ?"; args.append(f"%{p['camera']}%")
    rows = db.execute(q + " ORDER BY taken", args).fetchall()
    db.close()
    return res("search", None, {"hits": [dict(zip(("path", "rating", "keywords", "taken"), r)) for r in rows]}, verified=True)


# ------------------------------------------------------------------ design: Affinity Designer / Xara / Houdini
@op("boolean", "Affinity Designer, Xara, Houdini he_boolean", "APPX-45", ["pip:shapely"], "عمليات بوليانية متجهة",
    "IN = JSON [{\"circle\":[x,y,r]}|{\"rect\":[x,y,w,h]}|{\"poly\":[[x,y],…]}] ; mode=union|difference|intersection|xor ; fill")
def boolean(inp, out, p):
    from shapely.geometry import Point, Polygon, box
    from shapely.ops import unary_union
    shapes = []
    for s in json.loads(Path(inp[0]).read_text(encoding="utf-8")):
        if "circle" in s:
            x, y, r = s["circle"]; shapes.append(Point(x, y).buffer(r, quad_segs=64))
        elif "rect" in s:
            x, y, w, h = s["rect"]; shapes.append(box(x, y, x + w, y + h))
        else:
            shapes.append(Polygon(s["poly"]))
    mode = p.get("mode", "union")
    g = unary_union(shapes) if mode == "union" else shapes[0]
    for s in shapes[1:]:
        if mode != "union":
            g = getattr(g, {"difference": "difference", "intersection": "intersection", "xor": "symmetric_difference"}[mode])(s)
    x0, y0, x1, y1 = g.bounds
    path = g.svg(fill_color=p.get("fill", "#1f6feb"), opacity=1.0)
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {y0} {x1 - x0} {y1 - y0}" width="{x1 - x0:.0f}" height="{y1 - y0:.0f}">{path}</svg>'
    Path(out).write_text(svg, encoding="utf-8")
    return res("boolean", str(out), {"area": round(g.area, 3), "mode": mode}, verified=True)


@op("trace", "Affinity/Xara bitmap to vector", "APPX-79", BASE, "تحويل صورة إلى متجه SVG", "colors=4 (k-means), smooth (epsilon px)")
def trace(inp, out, p):
    np, cv2 = np_cv()
    img = read(inp[0])
    k = int(f(p, "colors", 4))
    Z = img.reshape(-1, 3).astype(np.float32)
    _, lab, cen = cv2.kmeans(Z, k, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0), 3, cv2.KMEANS_PP_CENTERS)
    lab = lab.reshape(img.shape[:2])
    h, w = lab.shape
    parts, n = [], 0
    for i in np.argsort(-np.bincount(lab.ravel(), minlength=k)):     # biggest colour first = background
        m = (lab == i).astype(np.uint8) * 255
        cnts, hier = cv2.findContours(m, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        d = ""
        for c in cnts:
            if cv2.contourArea(c) < f(p, "min_area", 12.0):
                continue
            a = cv2.approxPolyDP(c, f(p, "smooth", 1.2), True).reshape(-1, 2)
            d += "M" + " L".join(f"{x},{y}" for x, y in a) + "Z"
            n += 1
        b, g, r = (int(v) for v in cen[i])
        if d:
            parts.append(f'<path fill="#{r:02x}{g:02x}{b:02x}" fill-rule="evenodd" d="{d}"/>')
    Path(out).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>", encoding="utf-8")
    return res("trace", str(out), {"colors": k, "paths": n, "bytes": Path(out).stat().st_size})


@op("pdf", "Affinity/Xara export, Lightroom/JPEGmini album", "APPX-80", ["pip:pillow"], "صور إلى PDF", "dpi=300")
def pdf(inp, out, p):
    from PIL import Image
    ims = [Image.open(x).convert("RGB") for x in expand(inp)]
    ims[0].save(out, save_all=True, append_images=ims[1:], resolution=f(p, "dpi", 300.0))
    return res("pdf", str(out), {"pages": len(ims)})


@op("scatter", "Houdini Scatter/Copy to Points, Affinity symbols", "APPX-81", BASE, "نثر عناصر إجرائيًا",
    "w h count seed min_dist shape=circle|star size jitter → SVG (Poisson-disc)")
def scatter(inp, out, p):
    np, _ = np_cv()
    W, H, n, rng = f(p, "w", 1080.0), f(p, "h", 1080.0), int(f(p, "count", 200)), np.random.default_rng(int(f(p, "seed", 7)))
    md, pts, tries = f(p, "min_dist", 30.0), [], 0
    while len(pts) < n and tries < n * 60:
        tries += 1
        q = rng.uniform([0, 0], [W, H])
        if all((q[0] - a) ** 2 + (q[1] - b) ** 2 >= md * md for a, b in pts):
            pts.append(q)
    size, el = f(p, "size", 8.0), []
    for x, y in pts:
        s = size * rng.uniform(1 - f(p, "jitter", 0.4), 1 + f(p, "jitter", 0.4))
        if p.get("shape", "circle") == "star":
            pp = " ".join(f"{x + (s if k % 2 == 0 else s / 2.5) * math.cos(math.pi * k / 5 - math.pi / 2):.1f},"
                          f"{y + (s if k % 2 == 0 else s / 2.5) * math.sin(math.pi * k / 5 - math.pi / 2):.1f}" for k in range(10))
            el.append(f'<polygon points="{pp}"/>')
        else:
            el.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{s:.1f}"/>')
    Path(out).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" fill="{p.get("fill", "#f5c542")}">'
                         + "".join(el) + "</svg>", encoding="utf-8")
    dmin = min((math.dist(a, b) for i, a in enumerate(pts) for b in pts[i + 1:]), default=0)
    return res("scatter", str(out), {"points": len(pts), "min_distance": round(dmin, 1)}, verified=dmin >= md - 1e-6)


@op("noise-field", "Houdini Mountain/Noise SOP, VEX noise", "APPX-82", BASE, "حقل ضوضاء إجرائي (أرض/سحب/تموج)",
    "w h scale octaves seed mode=gray|terrain|clouds → PNG (fractal value noise)")
def noise_field(inp, out, p):
    np, cv2 = np_cv()
    W, H, rng = int(f(p, "w", 1024)), int(f(p, "h", 1024)), np.random.default_rng(int(f(p, "seed", 3)))
    acc, amp, tot = np.zeros((H, W), np.float32), 1.0, 0.0
    base = f(p, "scale", 8.0)
    for o in range(int(f(p, "octaves", 5))):
        n = int(base * 2 ** o) + 2
        g = rng.random((n, n)).astype(np.float32)
        acc += amp * cv2.resize(g, (W, H), interpolation=cv2.INTER_CUBIC)
        tot += amp
        amp *= f(p, "persistence", 0.5)
    v = acc / tot
    v = (v - v.min()) / (v.max() - v.min() + 1e-6)
    mode = p.get("mode", "gray")
    if mode == "terrain":
        lut = np.interp(v, [0, .35, .4, .6, .8, 1], [0, 0, 1, 2, 3, 4])
        cols = np.array([[120, 60, 20], [200, 170, 90], [60, 140, 60], [70, 90, 110], [250, 250, 250]], np.float32)
        lo = np.floor(lut).astype(int).clip(0, 3)
        t = (lut - lo)[..., None]
        img = cols[lo] * (1 - t) + cols[lo + 1] * t
    elif mode == "clouds":
        img = np.array([235, 180, 120], np.float32) * (1 - v[..., None]) + 255 * v[..., None]   # sky blue → white (BGR)
    else:
        img = np.dstack([v * 255] * 3)
    return res("noise-field", write(out, img.clip(0, 255).astype(np.uint8)), {"octaves": int(f(p, "octaves", 5))})


@op("lsystem", "Houdini L-System SOP", "APPX-83", [], "نمو نباتي/زخرفي (L-system)", "axiom rules=F:FF+[+F-F-F]-[-F+F+F] iterations angle step → SVG")
def lsystem(inp, out, p):
    s, rules = p.get("axiom", "F"), dict(r.split(":") for r in p.get("rules", "F:FF+[+F-F-F]-[-F+F+F]").split("|"))
    for _ in range(int(f(p, "iterations", 4))):
        s = "".join(rules.get(c, c) for c in s)
        if len(s) > 2_000_000:
            raise ValueError("string too long: lower iterations")
    x, y, a, st, seg = 0.0, 0.0, -90.0, [], []
    ang, step = f(p, "angle", 22.5), f(p, "step", 5.0)
    for c in s:
        if c in "FG":
            nx, ny = x + step * math.cos(math.radians(a)), y + step * math.sin(math.radians(a))
            seg.append((x, y, nx, ny)); x, y = nx, ny
        elif c == "+":
            a += ang
        elif c == "-":
            a -= ang
        elif c == "[":
            st.append((x, y, a))
        elif c == "]":
            x, y, a = st.pop()
    xs = [v for s_ in seg for v in (s_[0], s_[2])]; ys = [v for s_ in seg for v in (s_[1], s_[3])]
    x0, y0, w, h = min(xs) - 5, min(ys) - 5, max(xs) - min(xs) + 10, max(ys) - min(ys) + 10
    d = "".join(f"M{a:.1f} {b:.1f}L{c:.1f} {e:.1f}" for a, b, c, e in seg)
    Path(out).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.1f} {y0:.1f} {w:.1f} {h:.1f}">'
                         f'<path d="{d}" stroke="{p.get("stroke", "#2f7d32")}" stroke-width="1" fill="none"/></svg>', encoding="utf-8")
    return res("lsystem", str(out), {"segments": len(seg)})


@op("chops", "Houdini CHOPs (Lag, Noise, Cycle, Envelope, Spring)", "APPX-46", BASE, "عمليات منحنيات الحركة",
    "IN = keys JSON [[t,v],…] ; fps, lag=τ s, noise=amp, noise_freq, spring=k:damping → JSON curve per frame")
def chops(inp, out, p):
    np, _ = np_cv()
    keys = json.loads(Path(inp[0]).read_text(encoding="utf-8"))
    fps = f(p, "fps", 30.0)
    t = np.arange(0, keys[-1][0] + 1e-9, 1 / fps)
    v = np.interp(t, [k[0] for k in keys], [k[1] for k in keys])
    if "lag" in p:
        a, y = 1 - math.exp(-1 / (float(p["lag"]) * fps)), v.copy()
        for i in range(1, len(y)):
            y[i] = y[i - 1] + a * (v[i] - y[i - 1])
        v = y
    if "spring" in p:   # damped spring follow (overshoot)
        k, c = (float(x) for x in p["spring"].split(":"))
        y, vel = v.copy(), 0.0
        for i in range(1, len(y)):
            vel += (k * (v[i] - y[i - 1]) - c * vel) / fps
            y[i] = y[i - 1] + vel / fps
        v = y
    if "noise" in p:
        rng = np.random.default_rng(int(f(p, "seed", 1)))
        nk = max(2, int(t[-1] * f(p, "noise_freq", 2.0)) + 2)
        v = v + float(p["noise"]) * np.interp(t, np.linspace(0, t[-1], nk), rng.uniform(-1, 1, nk))
    Path(out).write_text(json.dumps({"fps": fps, "values": [round(float(x), 5) for x in v]}), encoding="utf-8")
    return res("chops", str(out), {"frames": len(v)})


# ------------------------------------------------------------------ type: FontLab
@op("font-build", "FontLab 7", "APPX-44", ["pip:fonttools"], "بناء خط من رسومات SVG",
    "IN = folder of SVGs named by character or uniXXXX (e.g. A.svg, uni0628.svg) ; family, upm, kern=\"A V -80;V A -80\", fea=file")
def font_build(inp, out, p):
    from fontTools.fontBuilder import FontBuilder
    from fontTools.pens.ttGlyphPen import TTGlyphPen
    from fontTools.pens.cu2quPen import Cu2QuPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.svgLib.path import parse_path
    from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
    upm = int(f(p, "upm", 1000))
    glyphs, cmap, adv = {}, {}, {}
    empty = TTGlyphPen(None)
    glyphs[".notdef"], glyphs["space"] = empty.glyph(), TTGlyphPen(None).glyph()
    adv[".notdef"], adv["space"] = (upm // 2, 0), (upm // 4, 0)
    cmap[0x20] = "space"
    for svg in sorted(Path(inp[0]).glob("*.svg")):
        stem = svg.stem
        cp = int(stem[3:], 16) if re.fullmatch(r"uni[0-9A-Fa-f]{4,6}", stem) else (ord(stem) if len(stem) == 1 else None)
        if cp is None:
            continue
        name = f"uni{cp:04X}" if not stem.isascii() or not stem.isalnum() or stem.startswith("uni") else stem
        txt = svg.read_text(encoding="utf-8")
        vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', txt).group(1).replace(",", " ").split()] if "viewBox" in txt else [0, 0, upm, upm]
        s = upm / vb[3]
        pen = TTGlyphPen(None)
        tp = TransformPen(Cu2QuPen(pen, 1.0, reverse_direction=True), (s, 0, 0, -s, -vb[0] * s, (vb[1] + vb[3]) * s - upm * 0.2))
        for d in re.findall(r'\sd="([^"]+)"', txt):
            parse_path(d, tp)
        glyphs[name], cmap[cp], adv[name] = pen.glyph(), name, (int(vb[2] * s), 0)
    if len(glyphs) <= 2:
        raise ValueError("no glyph SVGs (name them A.svg or uni0628.svg)")
    fb = FontBuilder(upm, isTTF=True)
    fb.setupGlyphOrder(list(glyphs))
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(adv)
    fb.setupHorizontalHeader(ascent=int(upm * 0.8), descent=-int(upm * 0.2))
    fam = p.get("family", "KOSIF Font")
    fb.setupNameTable({"familyName": fam, "styleName": p.get("style", "Regular")})
    fb.setupOS2(sTypoAscender=int(upm * 0.8), sTypoDescender=-int(upm * 0.2), usWinAscent=upm, usWinDescent=int(upm * 0.25))
    fb.setupPost()
    fea = Path(p["fea"]).read_text(encoding="utf-8") if p.get("fea") else ""
    if p.get("kern"):
        pairs = [x.split() for x in p["kern"].split(";") if x.strip()]
        name_of = lambda c: cmap.get(ord(c), c) if len(c) == 1 else c
        fea += "feature kern {\n" + "".join(f"  pos {name_of(a)} {name_of(b)} {int(v)};\n" for a, b, v in pairs) + "} kern;\n"
    if fea:
        addOpenTypeFeaturesFromString(fb.font, fea)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    fb.save(str(out))
    return res("font-build", str(out), {"glyphs": len(glyphs), "codepoints": len(cmap), "features": bool(fea)})


@op("font-inspect", "FontLab font info / Glyphs panel", "APPX-84", ["pip:fonttools"], "فحص خط", "family/style names, glyph and codepoint counts, Arabic letter coverage, GSUB/GPOS feature tags (e.g. kern), variable flag")
def font_inspect(inp, out, p):
    from fontTools.ttLib import TTFont
    arabic = list(range(0x0621, 0x064B))
    with TTFont(inp[0], lazy=True) as ft:   # closed afterwards: Windows keeps an open font file locked
        cmap = ft.getBestCmap() or {}
        feats = sorted({fr.FeatureTag for fr in ft["GSUB"].table.FeatureList.FeatureRecord}) if "GSUB" in ft else []
        gpos = sorted({fr.FeatureTag for fr in ft["GPOS"].table.FeatureList.FeatureRecord}) if "GPOS" in ft else []
        name = ft["name"].getDebugName
        info = {"family": name(1), "style": name(2), "glyphs": ft["maxp"].numGlyphs, "codepoints": len(cmap),
                "arabic_letters": f"{sum(c in cmap for c in arabic)}/{len(arabic)}", "gsub": feats, "gpos": gpos,
                "variable": "fvar" in ft}
    return res("font-inspect", None, info, verified=True)


@op("font-subset", "FontLab export / web fonts", "APPX-85", ["pip:fonttools"], "تقليص خط للويب", "text= or unicodes=, flavor=woff2|woff (woff2 needs brotli)")
def font_subset(inp, out, p):
    from fontTools import subset
    if p.get("flavor") == "woff2":
        try:
            importlib.import_module("brotli")
        except ImportError:
            raise ImportError("flavor=woff2 needs the brotli package: pip install brotli "
                              "(or use flavor=woff, or no flavor for TTF)") from None
    opts = subset.Options()
    opts.layout_features = ["*"]
    if p.get("flavor"):
        opts.flavor = p["flavor"]
    ft = subset.load_font(inp[0], opts)
    s = subset.Subsetter(opts)
    s.populate(text=p.get("text", ""), unicodes=[int(u, 16) for u in p.get("unicodes", "").split(",") if u])
    s.subset(ft)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    subset.save_font(ft, out, opts)
    ft.close()   # release the source file (Windows locks open files)
    return res("font-subset", str(out), {"bytes_in": Path(inp[0]).stat().st_size, "bytes_out": Path(out).stat().st_size})


# ------------------------------------------------------------------ animation: Adobe Animate
def ease(name, u):
    return {"linear": u, "in": u * u, "out": 1 - (1 - u) ** 2, "inout": u * u * (3 - 2 * u),
            "back": 1 + 2.7 * (u - 1) ** 3 + 1.7 * (u - 1) ** 2}.get(name, u * u * (3 - 2 * u))


@op("tween", "Adobe Animate classic/motion tween + TexturePacker + onion skin", "APPX-49", ["pip:pillow"],
    "حركة متوسطة وورقة رسوم", "IN = sprite PNG ; from=x,y to=x,y frames fps ease=inout|in|out|back w h cols onion=1")
def tween(inp, out, p):
    from PIL import Image
    spr = Image.open(inp[0]).convert("RGBA")
    W, H, n, cols = int(f(p, "w", 640)), int(f(p, "h", 360)), int(f(p, "frames", 24)), int(f(p, "cols", 6))
    a = [float(v) for v in p.get("from", "40,180").split(",")]
    b = [float(v) for v in p.get("to", "600,180").split(",")]
    sheet = Image.new("RGBA", (W * cols, H * math.ceil(n / cols)), (0, 0, 0, 0))
    frames, pos = [], []
    for i in range(n):
        u = ease(p.get("ease", "inout"), i / max(n - 1, 1))
        x, y = a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u
        fr = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        fr.paste(spr, (int(x - spr.width / 2), int(y - spr.height / 2)), spr)
        sheet.paste(fr, ((i % cols) * W, (i // cols) * H))
        frames.append({"x": (i % cols) * W, "y": (i // cols) * H, "w": W, "h": H})
        pos.append([round(x, 2), round(y, 2)])
    outp = Path(out)
    sheet.save(outp)
    outp.with_suffix(".json").write_text(json.dumps({"fps": f(p, "fps", 24.0), "frames": frames, "positions": pos}), encoding="utf-8")
    if p.get("onion") == "1":
        k = n // 2
        on = Image.new("RGBA", (W, H), (255, 255, 255, 255))
        for j, al in ((k - 2, 60), (k - 1, 120), (k, 255)):
            fr = sheet.crop((frames[j]["x"], frames[j]["y"], frames[j]["x"] + W, frames[j]["y"] + H))
            fr.putalpha(fr.getchannel("A").point(lambda v: v * al // 255))
            on = Image.alpha_composite(on, fr)
        on.save(outp.with_name(outp.stem + "_onion.png"))
    return res("tween", str(outp), {"frames": n, "first": pos[0], "last": pos[-1]})


@op("lottie", "Adobe Animate export (Bodymovin/Lottie), Canvas", "APPX-86", [], "تصدير Lottie JSON", "w h fps frames from=x,y to=x,y shape=circle|rect size color ease")
def lottie(inp, out, p):
    W, H, fps, n = int(f(p, "w", 512)), int(f(p, "h", 512)), int(f(p, "fps", 30)), int(f(p, "frames", 60))
    a = [float(v) for v in p.get("from", "100,256").split(",")]
    b = [float(v) for v in p.get("to", "412,256").split(",")]
    sz = f(p, "size", 80.0)
    col = p.get("color", "#e8502e").lstrip("#")
    rgb = [int(col[i:i + 2], 16) / 255 for i in (0, 2, 4)] + [1]
    bez = {"linear": ([0, 0], [1, 1]), "in": ([0.42, 0], [1, 1]), "out": ([0, 0], [0.58, 1])}.get(p.get("ease", "inout"), ([0.42, 0], [0.58, 1]))
    shape = {"ty": "el", "p": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [sz, sz]}} if p.get("shape", "circle") == "circle" else \
        {"ty": "rc", "p": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [sz, sz]}, "r": {"a": 0, "k": 8}}
    anim = {"v": "5.7.4", "fr": fps, "ip": 0, "op": n, "w": W, "h": H, "nm": p.get("name", "KOSIF"), "ddd": 0, "assets": [],
            "layers": [{"ddd": 0, "ind": 1, "ty": 4, "nm": "shape", "sr": 1, "ip": 0, "op": n, "st": 0, "bm": 0,
                        "ks": {"o": {"a": 0, "k": 100}, "r": {"a": 0, "k": 0}, "a": {"a": 0, "k": [0, 0, 0]}, "s": {"a": 0, "k": [100, 100, 100]},
                               "p": {"a": 1, "k": [{"t": 0, "s": a + [0], "o": {"x": [bez[0][0]], "y": [bez[0][1]]}, "i": {"x": [bez[1][0]], "y": [bez[1][1]]}},
                                                   {"t": n - 1, "s": b + [0]}]}},
                        "shapes": [{"ty": "gr", "it": [shape, {"ty": "fl", "c": {"a": 0, "k": rgb}, "o": {"a": 0, "k": 100}},
                                                       {"ty": "tr", "p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]},
                                                        "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}}]}]}]}
    Path(out).write_text(json.dumps(anim), encoding="utf-8")
    return res("lottie", str(out), {"frames": n, "fps": fps})


@op("ik", "Adobe Animate Bone tool (FlashIK), Houdini KineFX", "APPX-87", [], "حل عظمتين (IK)", "l1 l2 target=x,y → joint angles + positions JSON")
def ik(inp, out, p):
    l1, l2 = f(p, "l1", 100.0), f(p, "l2", 80.0)
    tx, ty = (float(v) for v in p.get("target", "120,60").split(","))
    d = min(math.hypot(tx, ty), l1 + l2 - 1e-9)
    c2 = (d * d - l1 * l1 - l2 * l2) / (2 * l1 * l2)
    a2 = math.acos(max(-1, min(1, c2)))
    a1 = math.atan2(ty, tx) - math.atan2(l2 * math.sin(a2), l1 + l2 * math.cos(a2))
    j = (l1 * math.cos(a1), l1 * math.sin(a1))
    e = (j[0] + l2 * math.cos(a1 + a2), j[1] + l2 * math.sin(a1 + a2))
    data = {"shoulder_deg": math.degrees(a1), "elbow_deg": math.degrees(a2), "joint": j, "end": e,
            "reach_error": math.dist(e, (tx, ty))}
    if out:
        Path(out).write_text(json.dumps(data), encoding="utf-8")
    return res("ik", out, data, verified=data["reach_error"] < 1e-6 or math.hypot(tx, ty) > l1 + l2)


# ------------------------------------------------------------------ download: IDM
@op("download", "Internet Download Manager", "APPX-48", [], "تنزيل مجزأ قابل للاستئناف", "IN = URL ; parts=6, sha256= (verify)")
def download(inp, out, p):
    url, n = inp[0], int(f(p, "parts", 6))
    if not url.startswith(("http://", "https://")):
        raise ValueError("http(s) URL required")
    head = urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=30)
    size = int(head.headers.get("Content-Length", 0))
    ranged = head.headers.get("Accept-Ranges", "") == "bytes" and size > 0
    outp = Path(out)
    parts_dir = outp.with_name(outp.name + ".parts")
    parts_dir.mkdir(parents=True, exist_ok=True)
    if not ranged:
        n, bounds = 1, [(0, None)]
    else:
        bounds = [(i * size // n, (i + 1) * size // n - 1) for i in range(n)]
    errors = []

    def fetch(i):
        s, e = bounds[i]
        part = parts_dir / f"{i}.part"
        have = part.stat().st_size if part.exists() else 0
        if e is not None and s + have > e:
            return
        hdr = {"Range": f"bytes={s + have}-{e}"} if e is not None else {}
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=hdr), timeout=60) as r, open(part, "ab" if e is not None else "wb") as o:
                shutil.copyfileobj(r, o, 1 << 16)
        except Exception as exc:   # the .part stays on disk; rerun the same command to resume
            errors.append(f"part {i}: {exc}")
    th = [threading.Thread(target=fetch, args=(i,)) for i in range(n)]
    [t.start() for t in th]
    [t.join() for t in th]
    if errors:
        return res("download", None, {"errors": errors, "resume": "run the same command again"})
    h = hashlib.sha256()
    with open(outp, "wb") as o:
        for i in range(n):
            data = (parts_dir / f"{i}.part").read_bytes()
            o.write(data)
            h.update(data)
    shutil.rmtree(parts_dir, ignore_errors=True)
    got = h.hexdigest()
    ok = (outp.stat().st_size == size if ranged else True) and (got == p["sha256"].lower() if p.get("sha256") else True)
    return res("download", str(outp), {"bytes": outp.stat().st_size, "parts": n, "ranged": ranged, "sha256": got}, verified=ok)


# ------------------------------------------------------------------ design: Canva (evidence: app.asar of Canva 1.126.1)
FONT_DIR = Path(__file__).resolve().parents[1] / "proofs" / "_shared" / "fonts"
FONTS = {"amiri": "Amiri-Regular.ttf", "amiri-bold": "Amiri-Bold.ttf", "cairo": "Cairo[slnt,wght].ttf", "tajawal": "Tajawal-Bold.ttf",
         "reemkufi": "ReemKufi[wght].ttf", "lalezar": "Lalezar-Regular.ttf", "ruqaa": "ArefRuqaa-Regular.ttf", "ruqaa-bold": "ArefRuqaa-Bold.ttf"}
SIZES = {"instagram-post": (1080, 1080), "instagram-portrait": (1080, 1350), "story": (1080, 1920), "reel": (1080, 1920),
         "tiktok": (1080, 1920), "youtube-thumbnail": (1280, 720), "youtube-banner": (2560, 1440), "facebook-post": (1200, 630),
         "facebook-cover": (820, 312), "x-post": (1600, 900), "x-header": (1500, 500), "linkedin-post": (1200, 627),
         "pinterest": (1000, 1500), "whatsapp-status": (1080, 1920), "a4-300dpi": (2480, 3508), "presentation": (1920, 1080)}
AR_RE = re.compile(r"[\u0600-\u06FF]")


def font_path(name):
    if name and Path(name).is_file():
        return str(Path(name))
    f_ = FONTS.get((name or "cairo").lower())
    if f_ and (FONT_DIR / f_).is_file():
        return str(FONT_DIR / f_)
    for c in (r"C:\Windows\Fonts\arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if Path(c).is_file():
            return c
    return None


def shape_text(text, force=False):
    """Return (text to draw, how it was shaped). Pillow+raqm shapes by itself; else arabic-reshaper + bidi.
    force=True reshapes even with raqm (for renderers that never shape, such as matplotlib)."""
    from PIL import features
    if not AR_RE.search(text) or (features.check("raqm") and not force):
        return text, ("raqm" if AR_RE.search(text) else None)
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        return "\n".join(get_display(arabic_reshaper.reshape(line)) for line in text.split("\n")), "arabic-reshaper+bidi"
    except ImportError:
        return text, "none: letters will not join (pip install arabic-reshaper python-bidi)"


_CMAPS = {}


def cover_text(text, fp):
    """Make text drawable in font fp: a missing isolated presentation form becomes its base letter (same shape).
    Returns (text, still_missing)."""
    import unicodedata
    if not fp:
        return text, False
    if fp not in _CMAPS:
        from fontTools.ttLib import TTFont
        try:
            with TTFont(fp, lazy=True, fontNumber=0) as ft:
                _CMAPS[fp] = set(ft.getBestCmap() or {})
        except Exception:
            _CMAPS[fp] = None
    cmap = _CMAPS[fp]
    if cmap is None:
        return text, False
    out, missing = [], False
    for ch in text:
        if ord(ch) in cmap or ch in " \n\t":
            out.append(ch)
            continue
        dec = unicodedata.decomposition(ch)
        if dec.startswith("<isolated>") and int(dec.split()[1], 16) in cmap:
            out.append(chr(int(dec.split()[1], 16)))
            continue
        missing = True
        out.append(ch)
    return "".join(out), missing


def pick_font(text, name):
    """Font path that can draw `text` after shaping; falls back to the bundled Amiri when the chosen font lacks glyphs."""
    fp = font_path(name)
    shaped = shape_text(text)[0]
    _, miss = cover_text(shaped, fp)
    if miss and AR_RE.search(text):
        alt = str(FONT_DIR / FONTS["amiri-bold" if "bold" in str(name).lower() else "amiri"])
        if Path(alt).is_file() and not cover_text(shaped, alt)[1]:
            return alt, True
    return fp, False


def load_font(name, size):
    from PIL import ImageFont, features
    fp = font_path(name)
    if not fp:
        return ImageFont.load_default()
    kw = {"layout_engine": ImageFont.Layout.RAQM} if features.check("raqm") else {}
    return ImageFont.truetype(fp, int(size), **kw)


def hex_rgba(c, alpha=255):
    c = (c or "#000000").lstrip("#")
    if len(c) == 3:
        c = "".join(ch * 2 for ch in c)
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4)) + ((int(c[6:8], 16),) if len(c) == 8 else (alpha,))


def draw_text_block(canvas, el):
    """Text box with wrap, auto-fit, alignment and Canva-style effects: shadow, outline (hollow), glow (neon), echo, lift."""
    from PIL import Image, ImageDraw, ImageFilter
    x, y, w, h = (int(v) for v in el["box"])
    raw = str(el.get("text", ""))
    rtl = bool(AR_RE.search(raw))
    size = int(el.get("size", 0)) or int(h * 0.8)
    fpath, fell_back = pick_font(raw, el.get("font"))
    def layout(sz):
        font = load_font(fpath, sz)
        d = ImageDraw.Draw(Image.new("L", (1, 1)))
        lines = []
        for para in raw.split("\n"):
            words, cur = para.split(" "), ""
            for wd in words:
                trial = (cur + " " + wd).strip()
                if d.textlength(shape_text(trial)[0], font=font) <= w or not cur:
                    cur = trial
                else:
                    lines.append(cur); cur = wd
            lines.append(cur)
        lh = int(sz * float(el.get("line_height", 1.25)))
        return font, lines, lh, max(d.textlength(shape_text(l)[0], font=font) for l in lines), lh * len(lines)
    while True:   # auto-fit: shrink until the block fits its box
        font, lines, lh, tw, th = layout(size)
        if (tw <= w and th <= h) or size <= 8:
            break
        size = int(size * 0.92)
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    color = hex_rgba(el.get("color", "#111111"))
    align = el.get("align", "right" if rtl else "left")
    ty = y + {"top": 0, "middle": (h - th) // 2, "bottom": h - th}[el.get("valign", "middle")]
    how = None
    pos = []
    for i, line in enumerate(lines):
        txt, how = shape_text(line)
        txt = cover_text(txt, fpath)[0]
        lw = d.textlength(txt, font=font)
        tx = {"left": x, "center": x + (w - lw) / 2, "right": x + w - lw}[align]
        pos.append((tx, ty + i * lh, txt))
    fx = el.get("effect", "none")
    def stamp(dx, dy, fill, stroke=0, stroke_fill=None):
        for tx, ty_, txt in pos:
            d.text((tx + dx, ty_ + dy), txt, font=font, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
    if fx in ("shadow", "lift"):
        sh = Image.new("RGBA", canvas.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
        off = max(2, size // 18)
        for tx, ty_, txt in pos:
            sd.text((tx + (off if fx == "shadow" else 0), ty_ + off), txt, font=font, fill=(0, 0, 0, 150 if fx == "shadow" else 110))
        layer = Image.alpha_composite(layer, sh.filter(ImageFilter.GaussianBlur(off if fx == "lift" else off / 2)))
        d = ImageDraw.Draw(layer)
    if fx in ("glow", "neon"):
        gl = Image.new("RGBA", canvas.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(gl)
        for tx, ty_, txt in pos:
            gd.text((tx, ty_), txt, font=font, fill=color[:3] + (255,), stroke_width=max(2, size // 20), stroke_fill=color[:3] + (255,))
        layer = Image.alpha_composite(layer, gl.filter(ImageFilter.GaussianBlur(size / 6)))
        d = ImageDraw.Draw(layer)
    if fx == "echo":
        for k, a in ((3, 60), (2, 110)):
            stamp(k * size / 25, k * size / 25, color[:3] + (a,))
    if fx == "outline":
        stamp(0, 0, (0, 0, 0, 0), max(2, size // 25), color)
    elif fx == "neon":
        stamp(0, 0, (255, 255, 255, 255), max(1, size // 40), color)
    else:
        stamp(0, 0, color, int(el.get("stroke", 0)), hex_rgba(el.get("stroke_color", "#000000")))
    canvas.alpha_composite(layer)
    return {"font_size": size, "lines": len(lines), "shaping": how, "fits": tw <= w and th <= h,
            "font": Path(fpath).name if fpath else None, "font_fallback": fell_back}


def fit_image(path, w, h, fit="cover"):
    from PIL import Image, ImageOps
    im = Image.open(path).convert("RGBA")
    if fit == "contain":
        im = ImageOps.contain(im, (w, h))
        bg = Image.new("RGBA", (w, h), (0, 0, 0, 0)); bg.paste(im, ((w - im.width) // 2, (h - im.height) // 2)); return bg
    return ImageOps.fit(im, (w, h), Image.LANCZOS)


def rounded_mask(w, h, r, shape="rect"):
    from PIL import Image, ImageDraw
    m = Image.new("L", (w, h), 0)
    dr = ImageDraw.Draw(m)
    if shape in ("circle", "ellipse"):
        dr.ellipse([0, 0, w - 1, h - 1], fill=255)
    else:
        dr.rounded_rectangle([0, 0, w - 1, h - 1], radius=int(r), fill=255)
    return m


def gradient(w, h, c1, c2, angle=90):
    np, _ = np_cv()
    from PIL import Image
    a = math.radians(float(angle))
    yy, xx = np.indices((h, w), np.float32)
    t = ((xx - w / 2) * math.cos(a) + (yy - h / 2) * math.sin(a))
    t = (t - t.min()) / (t.max() - t.min() + 1e-6)
    c1, c2 = np.array(hex_rgba(c1), np.float32), np.array(hex_rgba(c2), np.float32)
    return Image.fromarray((c1 * (1 - t[..., None]) + c2 * t[..., None]).astype(np.uint8), "RGBA")


def render_design(spec, base_dir):
    from PIL import Image, ImageDraw
    W, H = SIZES.get(spec.get("size"), None) or (int(spec.get("width", 1080)), int(spec.get("height", 1080)))
    bg = spec.get("background", "#ffffff")
    if isinstance(bg, dict) and bg.get("gradient"):
        canvas = gradient(W, H, *bg["gradient"][:2], bg.get("angle", 90))
    elif isinstance(bg, dict) and bg.get("image"):
        canvas = fit_image(base_dir / bg["image"], W, H)
    else:
        canvas = Image.new("RGBA", (W, H), hex_rgba(bg))
    report = []
    for el in spec.get("elements", []):
        t = el.get("type")
        x, y, w, h = (int(v) for v in el.get("box", [0, 0, W, H]))
        if t == "text":
            report.append({"type": "text", **draw_text_block(canvas, el)})
        elif t == "image":
            im = fit_image(base_dir / el["src"], w, h, el.get("fit", "cover"))
            if el.get("filter") == "duotone":
                im = duotone_pil(im, el.get("dark", "#1b1464"), el.get("light", "#ff6f61"))
            m = rounded_mask(w, h, el.get("radius", 0), el.get("mask", "rect"))
            canvas.paste(im, (x, y), Image.composite(im.getchannel("A"), Image.new("L", (w, h), 0), m))
            report.append({"type": "image", "src": el["src"]})
        elif t in ("rect", "ellipse", "line"):
            layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
            d = ImageDraw.Draw(layer)
            fill = hex_rgba(el.get("fill", "#000000"), int(255 * float(el.get("opacity", 1))))
            if t == "rect":
                d.rounded_rectangle([x, y, x + w, y + h], radius=int(el.get("radius", 0)), fill=fill,
                                    outline=hex_rgba(el["stroke"]) if el.get("stroke") else None, width=int(el.get("stroke_width", 0)))
            elif t == "ellipse":
                d.ellipse([x, y, x + w, y + h], fill=fill)
            else:
                d.line([x, y, x + w, y + h], fill=fill, width=int(el.get("width", 4)))
            canvas.alpha_composite(layer)
            report.append({"type": t})
    return canvas, report


@op("design", "Canva editor (templates, text effects, frames, gradients)", "APPX-88", ["pip:pillow", "pip:numpy"],
    "تصميم من قالب JSON (نصوص عربية وصور وأشكال)", "IN = design.json {size|width,height, background, elements:[text|image|rect|ellipse|line]} → PNG/JPG/PDF")
def design(inp, out, p):
    spec_path = Path(inp[0])
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    canvas, report = render_design(spec, spec_path.parent)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    if str(out).lower().endswith((".jpg", ".jpeg", ".pdf")):
        canvas.convert("RGB").save(out, quality=95, resolution=float(spec.get("dpi", 150)))
    else:
        canvas.save(out)
    texts = [r for r in report if r["type"] == "text"]
    return res("design", str(out), {"size": list(canvas.size), "elements": len(report), "texts": texts},
               verified=all(t["fits"] for t in texts))


@op("resize-design", "Canva Magic Resize", "APPX-89", BASE, "مقاسات متعددة لكل المنصات من تصميم واحد",
    "sizes=instagram-post,story,youtube-thumbnail,… (or all) ; mode=smart|pad-blur|pad-color ; color=#hex → OUT_DIR")
def resize_design(inp, out, p):
    np, cv2 = np_cv()
    img = read(inp[0])
    names = list(SIZES) if p.get("sizes", "all") == "all" else [s.strip() for s in p["sizes"].split(",")]
    outdir = Path(out)
    outdir.mkdir(parents=True, exist_ok=True)
    made = {}
    h, w = img.shape[:2]
    g = cv2.GaussianBlur(np.abs(cv2.Laplacian(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), cv2.CV_32F)), (0, 0), 15)
    ys, xs = np.indices(g.shape)
    cx, cy = float((g * xs).sum() / g.sum()), float((g * ys).sum() / g.sum())
    for n in names:
        W, H = SIZES[n]
        mode = p.get("mode", "smart")
        if mode == "smart" and abs((W / H) / (w / h) - 1) > 0.35:
            mode = "pad-blur"     # very different shape: cropping would cut the design, pad instead
        if mode == "smart":
            s = max(W / w, H / h)
            r = cv2.resize(img, (round(w * s), round(h * s)), interpolation=cv2.INTER_AREA)
            x0 = int(min(max(cx * s - W / 2, 0), r.shape[1] - W)); y0 = int(min(max(cy * s - H / 2, 0), r.shape[0] - H))
            o = r[y0:y0 + H, x0:x0 + W]
        else:
            s = min(W / w, H / h)
            fg = cv2.resize(img, (round(w * s), round(h * s)), interpolation=cv2.INTER_AREA)
            if mode == "pad-color":
                o = np.full((H, W, 3), hex_rgba(p.get("color", "#ffffff"))[2::-1][:3], np.uint8)
            else:
                o = cv2.GaussianBlur(cv2.resize(img, (W, H)), (0, 0), 25)
                o = (o * 0.7).astype(np.uint8)
            yy, xx = (H - fg.shape[0]) // 2, (W - fg.shape[1]) // 2
            o[yy:yy + fg.shape[0], xx:xx + fg.shape[1]] = fg
        made[n] = write(outdir / f"{Path(inp[0]).stem}_{n}.jpg", o)
    ok = all(read(v).shape[1::-1] == SIZES[k] for k, v in made.items())
    return res("resize-design", str(outdir), {"files": made}, verified=ok)


@op("remove-bg", "Canva Background Remover, CapCut", "APPX-14", BASE, "إزالة الخلفية إلى PNG شفاف",
    "box=x,y,w,h around the subject (default: centre 70%) ; feather px → transparent PNG")
def remove_bg(inp, out, p):
    np, cv2 = np_cv()
    img = read(inp[0])
    h, w = img.shape[:2]
    rect = tuple(int(v) for v in p["box"].split(",")) if p.get("box") else (int(w * .15), int(h * .08), int(w * .7), int(h * .88))
    mask = np.zeros((h, w), np.uint8)
    cv2.grabCut(img, mask, rect, np.zeros((1, 65)), np.zeros((1, 65)), int(f(p, "iters", 5)), cv2.GC_INIT_WITH_RECT)
    a = np.isin(mask, (1, 3)).astype(np.uint8) * 255
    n, lab, stats, _ = cv2.connectedComponentsWithStats(a)
    if n > 1:   # keep the largest region only
        a = (lab == 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))).astype(np.uint8) * 255
    fe = f(p, "feather", 2.0)
    if fe > 0:
        a = cv2.GaussianBlur(a, (0, 0), fe)
    o = np.dstack([img, a])
    if not str(out).lower().endswith(".png"):
        out = str(Path(out).with_suffix(".png"))
    write(out, o)
    return res("remove-bg", str(out), {"subject_pct": round(float((a > 127).mean() * 100), 1)})


def duotone_pil(im, dark, light):
    np, _ = np_cv()
    from PIL import Image
    arr = np.asarray(im.convert("RGBA")).astype(np.float32)
    y = (arr[..., 0] * .299 + arr[..., 1] * .587 + arr[..., 2] * .114)[..., None] / 255
    d, l = np.array(hex_rgba(dark)[:3], np.float32), np.array(hex_rgba(light)[:3], np.float32)
    rgb = d * (1 - y) + l * y
    return Image.fromarray(np.dstack([rgb, arr[..., 3:]]).astype(np.uint8), "RGBA")


@op("duotone", "Canva Duotone filter (DUOTONE in app.asar)", "APPX-90", ["pip:pillow", "pip:numpy"], "تأثير اللونين (Duotone)", "dark=#hex light=#hex")
def duotone(inp, out, p):
    from PIL import Image
    o = duotone_pil(Image.open(inp[0]), p.get("dark", "#1b1464"), p.get("light", "#ff6f61"))
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    (o if str(out).lower().endswith(".png") else o.convert("RGB")).save(out)
    return res("duotone", str(out), {"dark": p.get("dark", "#1b1464"), "light": p.get("light", "#ff6f61")})


@op("collage", "Canva grids / Collage", "APPX-91", ["pip:pillow"], "كولاج وشبكات صور",
    "IN = images or folder ; layout=grid|hero|strip ; cols ; size=instagram-post|WxH ; gap ; radius ; bg")
def collage(inp, out, p):
    from PIL import Image
    files = expand(inp)
    if not files:
        raise ValueError("no images")
    sz = p.get("size", "instagram-post")
    W, H = SIZES[sz] if sz in SIZES else tuple(int(v) for v in sz.lower().split("x"))
    gap, rad = int(f(p, "gap", 12)), int(f(p, "radius", 0))
    canvas = Image.new("RGBA", (W, H), hex_rgba(p.get("bg", "#ffffff")))
    lay = p.get("layout", "grid")
    cells = []
    if lay == "hero" and len(files) > 1:   # one big image on top, the rest in a row under it
        top = int((H - 3 * gap) * 0.62)
        cells.append((gap, gap, W - 2 * gap, top))
        k = len(files) - 1
        cw = (W - gap * (k + 1)) / k
        cells += [(int(gap + i * (cw + gap)), 2 * gap + top, int(cw), H - 3 * gap - top) for i in range(k)]
    elif lay == "strip":
        k = len(files)
        cw = (W - gap * (k + 1)) / k
        cells = [(int(gap + i * (cw + gap)), gap, int(cw), H - 2 * gap) for i in range(k)]
    else:
        cols = int(f(p, "cols", math.ceil(math.sqrt(len(files)))))
        rows = math.ceil(len(files) / cols)
        cw, ch = (W - gap * (cols + 1)) / cols, (H - gap * (rows + 1)) / rows
        cells = [(int(gap + (i % cols) * (cw + gap)), int(gap + (i // cols) * (ch + gap)), int(cw), int(ch)) for i in range(len(files))]
    for fpath, (x, y, w, h) in zip(files, cells):
        im = fit_image(fpath, w, h)
        canvas.paste(im, (x, y), rounded_mask(w, h, rad))
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    (canvas if str(out).lower().endswith(".png") else canvas.convert("RGB")).save(out, quality=95)
    return res("collage", str(out), {"images": len(files), "cells": [list(c) for c in cells[:len(files)]], "size": [W, H]})


@op("mockup", "Canva Mockups (PHOTO_TO_MOCKUP, MockupBundle in app.asar)", "APPX-92", BASE, "وضع التصميم داخل صورة واقعية (موك أب)",
    "IN = design, scene photo ; quad=x,y;x,y;x,y;x,y (TL;TR;BR;BL) or auto (largest bright quad) ; shade=0..1")
def mockup(inp, out, p):
    np, cv2 = np_cv()
    des, scene_ = read(inp[0]), read(inp[1])
    H, W = scene_.shape[:2]
    if p.get("quad"):
        q = np.float32([[float(v) for v in xy.split(",")] for xy in p["quad"].split(";")])
    else:   # the screen / poster / paper: largest bright 4-sided region
        g = cv2.cvtColor(scene_, cv2.COLOR_BGR2GRAY)
        _, th = cv2.threshold(g, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        q = None
        for c in sorted(cnts, key=cv2.contourArea, reverse=True)[:5]:
            a = cv2.approxPolyDP(c, 0.02 * cv2.arcLength(c, True), True)
            if len(a) == 4 and cv2.contourArea(a) > 0.03 * W * H:
                q = a.reshape(4, 2).astype(np.float32); break
        if q is None:
            raise ValueError("no target surface found: pass --set quad=x,y;x,y;x,y;x,y")
    q = order_quad(q)
    h, w = des.shape[:2]
    M = cv2.getPerspectiveTransform(np.float32([[0, 0], [w, 0], [w, h], [0, h]]), q)
    warped = cv2.warpPerspective(des, M, (W, H))
    m = cv2.warpPerspective(np.full((h, w), 255, np.uint8), M, (W, H)).astype(np.float32)[..., None] / 255
    shade = f(p, "shade", 0.35)   # keep the scene's light and folds on the design
    lum = cv2.GaussianBlur(cv2.cvtColor(scene_, cv2.COLOR_BGR2GRAY).astype(np.float32), (0, 0), 3)[..., None]
    region = lum[m[..., 0] > 0.5]
    norm = lum / (float(np.median(region)) if region.size else 255.0)
    lit = (warped.astype(np.float32) * ((1 - shade) + shade * norm)).clip(0, 255)
    o = (scene_ * (1 - m) + lit * m).astype(np.uint8)
    return res("mockup", write(out, o), {"quad": q.round(1).tolist()})


@op("qr", "Canva QR code app (vendor QR library in app.asar)", "APPX-93", ["pip:segno", "pip:opencv"], "رمز QR بألوان وشعار",
    "IN = text/URL ; dark=#hex light=#hex scale border logo=path ; error=h when a logo is used → PNG/SVG (decoded back to verify)")
def qr(inp, out, p):
    import segno
    np, cv2 = np_cv()
    data = inp[0]
    err = p.get("error", "h" if p.get("logo") else "m")
    code = segno.make(data, error=err, micro=False)
    kw = {"scale": int(f(p, "scale", 12)), "border": int(f(p, "border", 4)), "dark": p.get("dark", "#000000"), "light": p.get("light", "#ffffff")}
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    if str(out).lower().endswith(".svg"):
        code.save(out, **kw)
        tmp = Path(out).with_suffix(".check.png"); code.save(str(tmp), **kw)
        check_path = tmp
    else:
        code.save(out, **kw)
        check_path = Path(out)
        if p.get("logo"):
            from PIL import Image
            im = Image.open(out).convert("RGBA")
            lg = Image.open(p["logo"]).convert("RGBA")
            s = int(im.width * 0.22)
            lg.thumbnail((s, s))
            pad = Image.new("RGBA", (lg.width + 16, lg.height + 16), hex_rgba(kw["light"]))
            pad.paste(lg, (8, 8), lg)
            im.paste(pad, ((im.width - pad.width) // 2, (im.height - pad.height) // 2))
            im.save(out)
    decoded, _, _ = cv2.QRCodeDetector().detectAndDecode(read(check_path))
    if check_path != Path(out):
        check_path.unlink(missing_ok=True)
    return res("qr", str(out), {"version": code.version, "error": code.error, "decoded": decoded}, verified=decoded == data)


def wcag(c1, c2):
    def lum(c):
        v = [x / 255 for x in c[:3]]
        v = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in v]
        return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]
    a, b = sorted((lum(c1), lum(c2)), reverse=True)
    return (a + 0.05) / (b + 0.05)


@op("palette", "Canva Brand Kit / colour palette from photo", "APPX-94", BASE + ["pip:pillow"], "لوحة ألوان الهوية من شعار أو صورة",
    "colors=5 → JSON (hex, share, best text colour + WCAG contrast) + swatch PNG")
def palette(inp, out, p):
    np, cv2 = np_cv()
    from PIL import Image, ImageDraw
    img = read(inp[0])
    small = cv2.resize(img, (200, int(200 * img.shape[0] / img.shape[1])))
    k = int(f(p, "colors", 5))
    Z = small.reshape(-1, 3).astype(np.float32)
    _, lab, cen = cv2.kmeans(Z, k, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.5), 4, cv2.KMEANS_PP_CENTERS)
    share = np.bincount(lab.ravel(), minlength=k) / lab.size
    cols = []
    for i in np.argsort(-share):
        rgb = tuple(int(v) for v in cen[i][::-1])
        on_white, on_black = wcag(rgb, (255, 255, 255)), wcag(rgb, (0, 0, 0))
        cols.append({"hex": "#%02x%02x%02x" % rgb, "share": round(float(share[i]), 3),
                     "text_on_it": "#ffffff" if on_white >= on_black else "#000000",
                     "contrast": round(max(on_white, on_black), 2), "aa_body_text": max(on_white, on_black) >= 4.5})
    sw = Image.new("RGB", (120 * k, 160), "white")
    d = ImageDraw.Draw(sw)
    for i, c in enumerate(cols):
        d.rectangle([i * 120, 0, i * 120 + 119, 119], fill=c["hex"])
        d.text((i * 120 + 8, 128), c["hex"], fill="black")
    outp = Path(out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    sw.save(outp.with_suffix(".png"))
    outp.with_suffix(".json").write_text(json.dumps(cols, ensure_ascii=False, indent=1), encoding="utf-8")
    return res("palette", str(outp.with_suffix(".json")), {"palette": cols, "swatch": str(outp.with_suffix(".png"))}, verified=True)


@op("chart", "Canva Charts", "APPX-95", ["pip:matplotlib"], "رسم بياني بعناوين عربية",
    "IN = data.json {labels:[…], values:[…]} or CSV label,value ; kind=bar|line|pie|donut ; title ; color ; font → PNG/SVG")
def chart(inp, out, p):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    src = Path(inp[0])
    if src.suffix.lower() == ".json":
        dj = json.loads(src.read_text(encoding="utf-8")); labels, values = dj["labels"], [float(v) for v in dj["values"]]
    else:
        rows = [l.split(",") for l in src.read_text(encoding="utf-8").splitlines() if l.strip()]
        if rows and not re.match(r"^-?[\d.]+$", rows[0][1].strip()):
            rows = rows[1:]
        labels, values = [r[0].strip() for r in rows], [float(r[1]) for r in rows]
    fp, _ = pick_font(" ".join(map(str, labels)) + " " + p.get("title", ""), p.get("font", "cairo"))
    prop = font_manager.FontProperties(fname=fp) if fp else None
    native = tuple(int(x) for x in re.findall(r"\d+", matplotlib.__version__)[:2]) >= (3, 11)   # 3.11+ shapes Arabic itself
    sh = (lambda s: str(s)) if native else (lambda s: cover_text(shape_text(str(s), force=True)[0], fp)[0])
    L = [sh(x) for x in labels]
    fig, ax = plt.subplots(figsize=(float(f(p, "w", 8.0)), float(f(p, "h", 5.0))), dpi=int(f(p, "dpi", 150)))
    color = p.get("color", "#1f6feb")
    kind = p.get("kind", "bar")
    if kind in ("pie", "donut"):
        wedges, texts = ax.pie(values, labels=L, startangle=90, counterclock=False,
                               wedgeprops={"width": 0.45} if kind == "donut" else None, textprops={"fontproperties": prop})
        ax.axis("equal")
    else:
        (ax.bar if kind == "bar" else ax.plot)(range(len(values)), values, color=color, **({"marker": "o", "linewidth": 2.5} if kind == "line" else {}))
        ax.set_xticks(range(len(values)))
        ax.set_xticklabels(L, fontproperties=prop)
        for s_ in ("top", "right"):
            ax.spines[s_].set_visible(False)
        if kind == "bar":
            for i, v in enumerate(values):
                ax.text(i, v, f"{v:g}", ha="center", va="bottom", fontproperties=prop)
    if p.get("title"):
        ax.set_title(sh(p["title"]), fontproperties=prop, fontsize=16)
    fig.tight_layout()
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out)
    plt.close(fig)
    return res("chart", str(out), {"kind": kind, "points": len(values),
                                   "arabic_shaping": ("matplotlib-native" if native else "arabic-reshaper+bidi")
                                   if AR_RE.search(" ".join(map(str, labels)) + p.get("title", "")) else None})


@op("pptx", "Canva Presentations (presentationml export in app.asar)", "APPX-96", ["pip:office", "pip:pillow"], "عرض تقديمي PowerPoint",
    "IN = slide images/designs (PNG/JPG or design.json) in order ; notes=file.txt (one line per slide) → .pptx 16:9")
def pptx(inp, out, p):
    from pptx import Presentation
    from pptx.util import Emu
    files = []
    for x in inp:
        q = Path(x)
        files += sorted(q.glob("*")) if q.is_dir() else [q]
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
    notes = Path(p["notes"]).read_text(encoding="utf-8").splitlines() if p.get("notes") else []
    tmpdir = Path(out).with_suffix(".slides")
    n = 0
    for fp in files:
        if fp.suffix.lower() == ".json":
            tmpdir.mkdir(exist_ok=True)
            spec = json.loads(fp.read_text(encoding="utf-8"))
            spec.setdefault("size", "presentation")
            canvas, _ = render_design(spec, fp.parent)
            img = tmpdir / (fp.stem + ".png"); canvas.save(img)
        elif fp.suffix.lower() in IMG_EXT:
            img = fp
        else:
            continue
        s = prs.slides.add_slide(prs.slide_layouts[6])
        s.shapes.add_picture(str(img), 0, 0, width=prs.slide_width, height=prs.slide_height)
        if n < len(notes):
            s.notes_slide.notes_text_frame.text = notes[n]
        n += 1
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    prs.save(out)
    shutil.rmtree(tmpdir, ignore_errors=True)
    back = len(Presentation(out).slides)
    return res("pptx", str(out), {"slides": back}, verified=back == n)


@op("print-pdf", "Canva Print PDF (bleed, crop marks, CMYK in app.asar)", "APPX-97", ["pip:pillow"], "PDF جاهز للمطبعة: نزيف وعلامات قص وCMYK",
    "IN = design image ; width_mm height_mm (trim) ; bleed_mm=3 ; marks=1 ; cmyk=1 ; dpi=300 ; profile=CMYK.icc (optional, accurate)")
def print_pdf(inp, out, p):
    from PIL import Image, ImageDraw, ImageOps
    dpi = int(f(p, "dpi", 300))
    mm = lambda v: round(float(v) / 25.4 * dpi)
    tw, th = mm(f(p, "width_mm", 210.0)), mm(f(p, "height_mm", 297.0))
    bl = mm(f(p, "bleed_mm", 3.0))
    slug = mm(10) if p.get("marks", "1") == "1" else 0
    art = ImageOps.fit(Image.open(inp[0]).convert("RGB"), (tw + 2 * bl, th + 2 * bl), Image.LANCZOS)   # art covers the bleed
    page = Image.new("RGB", (tw + 2 * bl + 2 * slug, th + 2 * bl + 2 * slug), "white")
    page.paste(art, (slug, slug))
    if slug:
        d = ImageDraw.Draw(page)
        x0, y0, x1, y1 = slug + bl, slug + bl, slug + bl + tw, slug + bl + th
        L, gapm, lw = mm(6), mm(1.5), max(1, mm(0.15))
        for x in (x0, x1):
            d.line([x, 0 + gapm, x, slug - gapm], fill="black", width=lw)
            d.line([x, page.height - slug + gapm, x, page.height - gapm], fill="black", width=lw)
        for y in (y0, y1):
            d.line([gapm, y, slug - gapm, y], fill="black", width=lw)
            d.line([page.width - slug + gapm, y, page.width - gapm, y], fill="black", width=lw)
    mode = "RGB"
    if p.get("cmyk", "1") == "1":
        if p.get("profile"):
            from PIL import ImageCms
            page = ImageCms.profileToProfile(page, ImageCms.createProfile("sRGB"), ImageCms.getOpenProfile(p["profile"]), outputMode="CMYK")
        else:
            page = page.convert("CMYK")   # naive conversion; pass the printer's profile= for accurate colour
        mode = "CMYK"
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    page.save(out, resolution=dpi)
    return res("print-pdf", str(out), {"page_px": list(page.size), "trim_px": [tw, th], "bleed_px": bl, "marks": bool(slug),
                                       "mode": mode, "icc": bool(p.get("profile"))})


@op("text-anim", "Canva text animations (Rise, Typewriter, Fade, Pop)", "APPX-98", ["pip:pillow", "pip:numpy"],
    "تحريك نص عربي إلى GIF أو MP4", "text ; style=rise|typewriter|fade|pop ; size=story|WxH ; font ; color ; bg ; seconds ; fps → .gif or .mp4 (ffmpeg)")
def text_anim(inp, out, p):
    from PIL import Image
    np, _ = np_cv()
    text = p.get("text", inp[0] if inp else "KOSIF")
    sz = p.get("size", "1080x1080")
    W, H = SIZES[sz] if sz in SIZES else tuple(int(v) for v in sz.lower().split("x"))
    fps, secs = int(f(p, "fps", 24)), float(f(p, "seconds", 2.5))
    n = int(fps * secs)
    style = p.get("style", "rise")
    words = text.split(" ")
    frames = []
    for i in range(n):
        u = min(1.0, i / max(1, int(n * 0.6)))
        e = 1 - (1 - u) ** 3
        canvas = Image.new("RGBA", (W, H), hex_rgba(p.get("bg", "#0f172a")))
        shown = text
        alpha, dy, scale = 1.0, 0.0, 1.0
        if style == "typewriter":   # whole words: Arabic letters stay joined
            shown = " ".join(words[:max(1, math.ceil(e * len(words)))])
        elif style == "fade":
            alpha = e
        elif style == "pop":
            scale = 0.6 + 0.4 * (1 + 2.7 * (u - 1) ** 3 + 1.7 * (u - 1) ** 2)
        else:
            dy, alpha = (1 - e) * H * 0.08, e
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        bw_, bh_ = int(W * 0.84 * scale), int(H * 0.3 * scale)
        draw_text_block(layer, {"type": "text", "text": shown, "box": [(W - bw_) // 2, int((H - bh_) // 2 + dy), bw_, bh_],
                                "font": p.get("font", "cairo"), "color": p.get("color", "#ffffff"), "align": "center",
                                "effect": p.get("effect", "none"), "size": int(f(p, "font_size", 0)) * scale if p.get("font_size") else 0})
        if alpha < 1:
            layer.putalpha(layer.getchannel("A").point(lambda v, a=alpha: int(v * a)))
        canvas.alpha_composite(layer)
        frames.append(canvas.convert("RGB"))
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    if str(out).lower().endswith(".mp4"):
        import subprocess
        ff = shutil.which("ffmpeg")
        if not ff:
            raise RuntimeError("MP4 needs ffmpeg on PATH (or write .gif)")
        proc = subprocess.Popen([ff, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps),
                                 "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)], stdin=subprocess.PIPE)
        for fr in frames:
            proc.stdin.write(np.asarray(fr).tobytes())
        proc.stdin.close()
        if proc.wait():
            raise RuntimeError("ffmpeg failed")
    else:
        frames[0].save(out, save_all=True, append_images=frames[1:], duration=int(1000 / fps), loop=0)
    return res("text-anim", str(out), {"frames": n, "fps": fps, "style": style, "size": [W, H]})


# ------------------------------------------------------------------ painting batch: Paint.NET, Photoshop, MS Paint
sys.path.insert(0, str(Path(__file__).resolve().parent))
import app_studio_paint  # noqa: E402

PAINT_BATCH = app_studio_paint.register(globals())


# ------------------------------------------------------------------ cli
def missing(reqs):
    out = []
    for r in reqs:
        mod, pip = REQ.get(r, (None, None))
        if mod:
            try:
                importlib.import_module(mod)
            except Exception:
                out.append({"requirement": r, "install": pip})
    return out


def missing_optional(name):
    out = []
    for mod, pip, needed_for in OPTIONAL.get(name, []):
        try:
            importlib.import_module(mod)
        except Exception:
            out.append({"needed_for": needed_for, "module": mod, "install": pip})
    return out


def doctor():
    rows, runnable = [], 0
    installs = set()
    for name, o in OPS.items():
        miss = missing(o["requires"])
        runnable += not miss
        row = {"op": name, "ready": not miss, "missing": [m["requirement"] for m in miss]}
        opt = missing_optional(name)
        if opt:   # the op runs, but not with these settings until the extra is installed
            row["limited"] = [f"{m['needed_for']} needs {m['module']} ({m['install']})" for m in opt]
        rows.append(row)
        installs.update(m["install"] for m in miss + opt)
    installs = sorted(installs)
    extra = {}
    try:
        from PIL import features
        extra["arabic_text_shaping_raqm"] = bool(features.check("raqm"))
    except Exception:
        extra["arabic_text_shaping_raqm"] = False
    try:
        importlib.import_module("arabic_reshaper"); importlib.import_module("bidi")
        extra["arabic_text_shaping_fallback"] = True
    except Exception:
        extra["arabic_text_shaping_fallback"] = False
        if not extra["arabic_text_shaping_raqm"]:
            installs_hint = "pip install arabic-reshaper python-bidi"
            extra["arabic_install"] = installs_hint
    return {"status": "doctor", "ops": len(OPS), "ready": runnable, "missing_installs": installs, "extras": extra,
            "notes": ["Arabic watermark text: Pillow with libraqm, or else arabic-reshaper + python-bidi (used automatically)",
                      "faces on OpenCV 5.x needs a YuNet model (--set model=… or KOSIF_YUNET); OpenCV 4.x uses Haar cascades",
                      "download needs network access to the URL; all other ops are offline"],
            "rows": rows}


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if argv[0] == "doctor":
        print(json.dumps(doctor(), ensure_ascii=False, indent=1))
        return 0
    if argv[0] == "ops":
        word = argv[1].lower() if len(argv) > 1 else ""
        for n, o in OPS.items():
            line = f"{n:14} {o['appx']:9} {o['app'][:46]:46} {o['en']}"
            if word in (line + o["ar"]).lower():
                print(line + "  |  " + o["ar"])
        return 0
    batch = argv[0] == "batch"
    if batch:
        argv = argv[1:]
    ap = argparse.ArgumentParser(prog="app_studio.py")
    ap.add_argument("op", choices=sorted(OPS))
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("-o", "--out")
    ap.add_argument("--set", nargs="*", default=[], metavar="KEY=VALUE")
    a = ap.parse_args(argv)
    params = dict(kv.split("=", 1) for kv in a.set)
    o = OPS[a.op]
    miss = missing(o["requires"])
    if miss:
        print(json.dumps({"op": a.op, "status": "missing_requirements", "missing": miss}, ensure_ascii=False))
        return 2
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if batch:
        outdir = Path(a.out or "out")
        outdir.mkdir(parents=True, exist_ok=True)
        results = []
        for src in expand(a.inputs):
            try:
                results.append(o["fn"]([src], str(outdir / Path(src).name), dict(params)))
            except Exception as exc:
                results.append({"op": a.op, "input": src, "error": str(exc)[:200]})
        print(json.dumps({"op": a.op, "batch": len(results), "failed": sum("error" in r for r in results), "results": results},
                         ensure_ascii=False))
        return 0
    try:
        r = o["fn"](a.inputs, a.out, params)
    except Exception as exc:
        print(json.dumps({"op": a.op, "status": "error", "error": f"{type(exc).__name__}: {str(exc)[:300]}"}, ensure_ascii=False))
        return 1
    print(json.dumps(r, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
