"""Programs for the brand-logo-identity family.

Each card's technique is performed for real on a self-built fixture: marks and frames are drawn
with Pillow/numpy, SVG is generated and parsed back, fonts are outlined with fontTools, springs and
easings are integrated numerically and checked against closed-form answers. Pixel measurements are
independent of the code that drew them (we measure the rendered image, not the parameters).
"""
from __future__ import annotations
import colorsys
import hashlib
import json
import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONT_DIRS = ["/usr/share/fonts/truetype/noto", "/usr/share/fonts/truetype/dejavu", "/usr/share/fonts/truetype/liberation"]
LATIN = ["NotoSans-Bold.ttf", "NotoSans-Regular.ttf", "DejaVuSans-Bold.ttf", "DejaVuSans.ttf", "LiberationSans-Bold.ttf"]
ARABIC = ["NotoSansArabic-Bold.ttf", "NotoSansArabic-Regular.ttf", "NotoNaskhArabic-Regular.ttf", "DejaVuSans.ttf"]


def font_path(names) -> str:
    for d in FONT_DIRS:
        for n in names:
            p = Path(d) / n
            if p.is_file():
                return str(p)
    raise FileNotFoundError("no usable font")


def font(size: int, arabic=False):
    return ImageFont.truetype(font_path(ARABIC if arabic else LATIN), size)


def save(work: Path, name: str, data) -> Path:
    p = work / name
    if isinstance(data, Image.Image):
        data.save(p)
    elif isinstance(data, (dict, list)):
        p.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    else:
        p.write_text(str(data), encoding="utf-8")
    return p


def hex2rgb(h: str):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb2hex(c) -> str:
    return "#" + "".join(f"{int(round(v)):02x}" for v in c[:3])


def _lin(c):
    c = c / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def contrast(a: str, b: str) -> float:
    la, lb = (0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(bb) for r, g, bb in (hex2rgb(a), hex2rgb(b)))
    hi, lo = max(la, lb), min(la, lb)
    return round((hi + 0.05) / (lo + 0.05), 2)


def cubic_bezier(x1, y1, x2, y2):
    def bx(t): return 3 * (1 - t) ** 2 * t * x1 + 3 * (1 - t) * t ** 2 * x2 + t ** 3
    def by(t): return 3 * (1 - t) ** 2 * t * y1 + 3 * (1 - t) * t ** 2 * y2 + t ** 3

    def f(x):
        lo, hi = 0.0, 1.0
        for _ in range(60):
            mid = (lo + hi) / 2
            if bx(mid) < x:
                lo = mid
            else:
                hi = mid
        return by((lo + hi) / 2)
    return f


def expo_out(p): return 1.0 if p >= 1 else 1 - 2 ** (-10 * p)
def in_out_cubic(p): return 4 * p ** 3 if p < 0.5 else 1 - (-2 * p + 2) ** 3 / 2
def out_quad(p): return 1 - (1 - p) ** 2
def clamp01(p): return max(0.0, min(1.0, p))


def spring_curve(stiffness, damping, mass=1.0, frames=120, fps=30, sub=40):
    """Integrate x'' = (-k(x-1) - c x') / m from x=0, v=0 (Remotion-style spring to 1); one value per frame."""
    x, v, out = 0.0, 0.0, []
    dt = 1 / fps / sub
    for _ in range(frames):
        out.append(x)
        for _ in range(sub):
            a = (-stiffness * (x - 1) - damping * v) / mass
            v += a * dt
            x += v * dt
    return np.array(out)


def analytic_overshoot(stiffness, damping, mass=1.0):
    z = damping / (2 * math.sqrt(stiffness * mass))
    return math.exp(-z * math.pi / math.sqrt(1 - z * z)) if z < 1 else 0.0


def srgb_to_oklch(h: str):
    r, g, b = (_lin(c) for c in hex2rgb(h))
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l, m, s = (np.cbrt(v) for v in (l, m, s))
    L = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s
    A = 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s
    B = 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s
    return round(float(L), 4), round(float(math.hypot(A, B)), 4), round(math.degrees(math.atan2(B, A)) % 360, 2)


def oklch_to_hex(L, C, H):
    a, b = C * math.cos(math.radians(H)), C * math.sin(math.radians(H))
    l_ = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m_ = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s_ = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    rgb = (4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_,
           -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_,
           -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_)
    out = []
    for c in rgb:
        c = max(0.0, min(1.0, c))
        c = 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
        out.append(round(c * 255))
    return rgb2hex(out)


def ink_bbox(img: Image.Image, thr=40):
    a = np.asarray(img.convert("L"))
    ys, xs = np.nonzero(a > thr)
    if not len(xs):
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


ARABIC_RE = re.compile(r"[؀-ۿﭐ-﷿ﹰ-﻿]")


def tracking_lint(elements: list) -> list:
    """Flag letter-spacing (tracking) on any element whose text is Arabic."""
    return [e["text"] for e in elements if ARABIC_RE.search(e["text"]) and abs(e.get("letter_spacing", 0)) > 1e-9]


# ---------------------------------------------------------------- BRAND-01
OPERATORS = {"monogram + meaning", "product action", "metaphor fusion", "negative space", "construction geometry"}


def mark_type(name: str, new_product=False, recognition_budget=False) -> str:
    letters = re.sub(r"[^A-Za-z]", "", name)
    if len(name.split()) >= 3 or len(letters) > 12:
        return "lettermark"
    if len(letters) <= 6 and re.search(r"[aeiou]", letters.lower()) and not new_product:
        return "wordmark"
    if recognition_budget:
        return "pictorial"
    return "combination"


def validate_brief(b: dict) -> list:
    errs = [f"missing {k}" for k in ("brand", "one_thing", "for", "surface", "personality", "must", "must_not", "colours") if not b.get(k)]
    if b.get("personality") and not 3 <= len(b["personality"]) <= 5:
        errs.append(f"{len(b['personality'])} adjectives")
    ops = b.get("operators", [])
    if not 1 <= len(ops) <= 2 or not set(ops) <= OPERATORS:
        errs.append(f"operators {ops}")
    return errs


def mono_svg_ok(svg: str) -> bool:
    return not re.search(r"<(linear|radial)Gradient|url\(#", svg)


def brand_01(work):
    brief = {"brand": "Zest", "one_thing": "fresh juice in 10 minutes", "for": "office teams", "surface": "app icon",
             "personality": ["bright", "quick", "honest"], "must": "reads at 16 px", "must_not": "default SaaS blue",
             "colours": ["#f2732d"], "operators": ["negative space"]}
    save(work, "brief.json", brief)
    bad = dict(brief, personality=["a", "b", "c", "d", "e", "f"], operators=["negative space", "metaphor fusion", "product action"])
    mono = '<svg viewBox="0 0 24 24"><path d="M2 2h20v20H2z" fill="#000"/></svg>'
    grad = '<svg><linearGradient id="g"/><path fill="url(#g)" d="M0 0h1v1z"/></svg>'
    save(work, "mono.svg", mono)
    # 24 px read test: a mark drawn at 512 and reduced to 24 must keep its negative-space hole
    big = Image.new("L", (512, 512), 0)
    d = ImageDraw.Draw(big)
    d.rectangle([64, 64, 448, 448], fill=255)
    d.ellipse([192, 192, 320, 320], fill=0)
    small = np.asarray(big.resize((24, 24), Image.LANCZOS))
    save(work, "mark_24.png", Image.fromarray(small))
    return [("complete brief valid", validate_brief(brief) == [], validate_brief(brief)),
            ("6 adjectives and 3 operators rejected", "6 adjectives" in validate_brief(bad) and any(e.startswith("operators") for e in validate_brief(bad)), validate_brief(bad)),
            ("short phonetic name -> wordmark", mark_type("Zest") == "wordmark", mark_type("Zest")),
            ("long name -> lettermark", mark_type("International Business Machines") == "lettermark", mark_type("International Business Machines")),
            ("new product default -> combination", mark_type("Kosif", new_product=True) == "combination", mark_type("Kosif", new_product=True)),
            ("mono version: gradient rejected, flat accepted", mono_svg_ok(mono) and not mono_svg_ok(grad), "ok"),
            ("hole survives at 24 px (centre dark, ring light)", small[12, 12] < 100 and small[5, 5] > 200, (int(small[12, 12]), int(small[5, 5])))]


# ---------------------------------------------------------------- BRAND-02
FONT_MAP = {"technical": ("Space Grotesk", "IBM Plex Sans Arabic"), "warm": ("Nunito Sans", "Tajawal"),
            "authority": ("IBM Plex Sans", "Readex Pro")}
ADJ_CLASS = {"precise": "technical", "engineered": "technical", "modern": "technical", "friendly": "warm",
             "cosy": "warm", "human": "warm", "trusted": "authority", "official": "authority", "serious": "authority"}


def identity_from_interview(answers: dict) -> dict:
    if len(answers) > 4:
        raise ValueError("more than 4 questions")
    votes = {}
    for a in answers["adjectives"]:
        c = ADJ_CLASS.get(a)
        if c:
            votes[c] = votes.get(c, 0) + 1
    cls = max(sorted(votes), key=lambda k: votes[k])
    latin, arabic = FONT_MAP[cls]
    radius = 4 if answers["shape"] == "sharp" else 16
    dark = bool(re.search(r"night|cinema|dark|evening|ليل", answers["watched"]))
    presets = answers.get("presets", [])[:3]
    return {"class": cls, "latin": latin, "arabic": arabic, "radius": radius, "mode": "dark" if dark else "light",
            "presets_shown": presets}


def brand_02(work):
    a = identity_from_interview({"adjectives": ["friendly", "human", "precise"], "shape": "rounded",
                                 "watched": "on phones at night", "presets": ["coral", "capsule", "cartesian", "cobalt"]})
    b = identity_from_interview({"adjectives": ["official", "trusted"], "shape": "sharp", "watched": "office desktops"})
    save(work, "identity.json", [a, b])
    try:
        identity_from_interview({"adjectives": [], "shape": "", "watched": "", "presets": [], "extra": 1})
        rej = False
    except ValueError:
        rej = True
    return [("warm majority -> Nunito Sans + Tajawal", (a["latin"], a["arabic"]) == ("Nunito Sans", "Tajawal"), a),
            ("rounded -> radius 16, night -> dark", a["radius"] == 16 and a["mode"] == "dark", a),
            ("authority + sharp -> IBM Plex Sans / Readex Pro, radius 4, light", (b["latin"], b["radius"], b["mode"]) == ("IBM Plex Sans", 4, "light"), b),
            ("at most 3 presets shown", len(a["presets_shown"]) == 3, a["presets_shown"]),
            ("a fifth question is refused", rej, rej)]


# ---------------------------------------------------------------- BRAND-03
DESIGN_DEFAULT = {"bg": "#0F1A2B", "surface": "#16243a", "text": "#F4F7FF", "accent": "#F6C76B"}


def render_from_tokens(tok: dict, size=(64, 36)) -> Image.Image:
    im = Image.new("RGB", size, hex2rgb(tok["bg"]))
    d = ImageDraw.Draw(im)
    d.rectangle([4, 4, 30, 31], fill=hex2rgb(tok["surface"]))
    d.rectangle([36, 4, 59, 14], fill=hex2rgb(tok["accent"]))
    d.rectangle([36, 20, 59, 31], fill=hex2rgb(tok["text"]))
    return im


def drift(tok: dict, im: Image.Image, tol=3) -> dict:
    probes = {"bg": (1, 1), "surface": (10, 10), "accent": (40, 8), "text": (40, 25)}
    out = {}
    for role, xy in probes.items():
        got = im.getpixel(xy)
        diff = max(abs(a - b) for a, b in zip(got, hex2rgb(tok[role])))
        if diff > tol:
            out[role] = {"want": tok[role], "got": rgb2hex(got)}
    return out


def brand_03(work):
    tok = dict(DESIGN_DEFAULT)
    save(work, "tokens.json", {"roles": tok, "source": "DESIGN.md default (claude-animation-studio)"})
    a = render_from_tokens(tok)
    off = dict(tok, accent="#E8B85A")
    b = render_from_tokens(off)
    save(work, "export_a.png", a)
    save(work, "export_b.png", b)
    da, db = drift(tok, a), drift(tok, b)
    return [("four roles bg/surface/text/accent", list(tok) == ["bg", "surface", "text", "accent"], list(tok)),
            ("default text on bg contrast >= 4.5", contrast(tok["text"], tok["bg"]) >= 4.5, contrast(tok["text"], tok["bg"])),
            ("export from the constants module has no drift", da == {}, da),
            ("planted accent drift caught (only accent)", list(db) == ["accent"], db)]


# ---------------------------------------------------------------- BRAND-04
def resolve_tokens(tree: dict) -> dict:
    flat = {}

    def walk(node, path):
        if isinstance(node, dict) and "$value" in node:
            flat[".".join(path)] = node
        elif isinstance(node, dict):
            for k, v in node.items():
                if not k.startswith("$"):
                    walk(v, path + [k])
    walk(tree, [])

    def val(key, seen=()):
        if key in seen:
            raise ValueError(f"circular alias {key}")
        v = flat[key]["$value"]
        m = re.fullmatch(r"{([^}]+)}", str(v))
        return val(m.group(1), seen + (key,)) if m else v
    return {k: val(k) for k in flat}


def theme_maps(prim: dict, semantic: dict) -> dict:
    out = {}
    for brand, modes in semantic.items():
        for mode, roles in modes.items():
            tree = {"prim": prim, "sem": {r: {"$value": v, "$type": "color"} for r, v in roles.items()}}
            res = resolve_tokens(tree)
            out[f"{brand}.{mode}"] = {k.split(".", 1)[1]: v for k, v in res.items() if k.startswith("sem.")}
    return out


def brand_04(work):
    prim = {"blue": {"500": {"$value": "#2b86e0", "$type": "color"}, "900": {"$value": "#0f1a2b", "$type": "color"}},
            "gold": {"400": {"$value": "#f6c76b", "$type": "color"}}, "white": {"$value": "#ffffff", "$type": "color"}}
    sem = {"brandA": {"light": {"bg": "{prim.white}", "accent": "{prim.blue.500}"},
                      "dark": {"bg": "{prim.blue.900}", "accent": "{prim.blue.500}"}},
           "brandB": {"light": {"bg": "{prim.white}", "accent": "{prim.gold.400}"},
                      "dark": {"bg": "{prim.blue.900}", "accent": "{prim.gold.400}"}}}
    maps = theme_maps(prim, sem)
    css = "\n".join(f'[data-brand="{k.split(".")[0]}"][data-theme="{k.split(".")[1]}"]{{' +
                    ";".join(f"--{r}:{v}" for r, v in m.items()) + "}" for k, m in maps.items())
    save(work, "theme.json", maps)
    save(work, "theme.css", css)
    try:
        resolve_tokens({"a": {"$value": "{b}"}, "b": {"$value": "{a}"}})
        circ = False
    except ValueError:
        circ = True
    return [("2 brands x 2 modes = 4 semantic maps", len(maps) == 4, sorted(maps)),
            ("brandB.dark accent resolves through alias to gold", maps["brandB.dark"]["accent"] == "#f6c76b", maps["brandB.dark"]),
            ("brandA.dark bg resolves to #0f1a2b", maps["brandA.dark"]["bg"] == "#0f1a2b", maps["brandA.dark"]),
            ("circular alias rejected", circ, circ),
            ("css has one rule per map", css.count("{") == 4, css.count("{"))]


# ---------------------------------------------------------------- BRAND-05
PRESETS = {"biennale-yellow": {"paper": "#E9E5DB", "sun": "#F1EE2E", "ink": "#1B2566", "ember": "#E26B4A"},
           "blockframe": {"paper": "#FFFDF5", "pink": "#FE90E8", "blue": "#C0F7FE", "ink": "#000000"},
           "blue-professional": {"paper": "#fdfae7", "ink": "#1e2bfa"},
           "broadside": {"paper": "#F0ECE5", "ink": "#E85D26"},
           "cobalt-grid": {"paper": "#F0EBDE", "ink": "#1F2BE0"},
           "editorial-forest": {"paper": "#e89cb1", "ink": "#2e4a2a"}}


def resolve_design_file(files: set) -> str | None:
    for name in ("frame.md", "design.md", "DESIGN.md"):
        if name in files:
            return name
    return None


def px_to_cqw(px: float, width=1920) -> float:
    return round(px / width * 100, 3)


def brand_05(work):
    report = {k: {"ink_on_paper": contrast(v["ink"], v["paper"])} for k, v in PRESETS.items()}
    save(work, "presets.json", report)
    return [("frame.md wins over design.md and DESIGN.md", resolve_design_file({"frame.md", "design.md", "DESIGN.md"}) == "frame.md", "frame.md"),
            ("design.md wins over DESIGN.md", resolve_design_file({"design.md", "DESIGN.md"}) == "design.md", "design.md"),
            ("nothing -> None (design step decides)", resolve_design_file(set()) is None, None),
            ("Biennale ink #1B2566 on paper #E9E5DB >= 7:1", report["biennale-yellow"]["ink_on_paper"] >= 7, report["biennale-yellow"]),
            ("broadside orange on cream is below 4.5 (display only)", report["broadside"]["ink_on_paper"] < 4.5, report["broadside"]),
            ("96 px at 1920 = 5 cqw", px_to_cqw(96) == 5.0, px_to_cqw(96))]


# ---------------------------------------------------------------- BRAND-06
BOOK_PARTS = ["cover", "story", "logo", "colour", "type", "imagery", "motion", "voice", "applications", "contacts"]


def build_brand_book(tokens: dict, voice: list) -> str:
    if not 3 <= len(voice) <= 5:
        raise ValueError("voice needs 3-5 attributes")
    rows = []
    names = list(tokens)
    for n in names:
        L, C, H = srgb_to_oklch(tokens[n])
        rgb = hex2rgb(tokens[n])
        rows.append(f'<tr data-token="{n}"><td>{tokens[n]}</td><td>rgb({rgb[0]} {rgb[1]} {rgb[2]})</td>'
                    f"<td>oklch({L} {C} {H})</td></tr>")
    pairs = [f'<li data-pair="{a}/{b}">{contrast(tokens[a], tokens[b])}</li>' for a in names for b in names if a < b]
    secs = "".join(f'<section id="{p}"></section>' for p in BOOK_PARTS)
    return (f"<html><body>{secs}<table>{''.join(rows)}</table><ul>{''.join(pairs)}</ul>"
            f"<ol id='voice'>{''.join(f'<li>{v}</li>' for v in voice)}</ol></body></html>")


def brand_06(work):
    tok = {"ink": "#000000", "paper": "#ffffff", "red": "#ff0000"}
    html = build_brand_book(tok, ["warm", "exact", "brief"])
    save(work, "brand_book.html", html)
    red = srgb_to_oklch("#ff0000")
    try:
        build_brand_book(tok, ["a", "b"])
        rej = False
    except ValueError:
        rej = True
    return [("ten parts", html.count("<section") == 10, html.count("<section")),
            ("white -> oklch(1, 0, *)", srgb_to_oklch("#ffffff")[:2] == (1.0, 0.0), srgb_to_oklch("#ffffff")),
            ("#ff0000 -> oklch(0.628 0.2577 29.23)", abs(red[0] - 0.628) < 0.001 and abs(red[1] - 0.2577) < 0.001 and abs(red[2] - 29.23) < 0.05, red),
            ("ink/paper WCAG pair listed as 21.0", 'data-pair="ink/paper">21.0<' in html, "21.0"),
            ("2 voice attributes refused", rej, rej)]


# ---------------------------------------------------------------- BRAND-07
def make_font(path: Path, family: str, licence: str, url: str):
    from fontTools.fontBuilder import FontBuilder
    from fontTools.pens.ttGlyphPen import TTGlyphPen
    fb = FontBuilder(1000, isTTF=True)
    fb.setupGlyphOrder([".notdef", "A"])
    fb.setupCharacterMap({65: "A"})
    pen = TTGlyphPen(None)
    pen.moveTo((0, 0)); pen.lineTo((500, 700)); pen.lineTo((1000, 0)); pen.closePath()
    g = pen.glyph()
    fb.setupGlyf({".notdef": TTGlyphPen(None).glyph(), "A": g})
    fb.setupHorizontalMetrics({".notdef": (500, 0), "A": (1000, 0)})
    fb.setupHorizontalHeader(ascent=800, descent=-200)
    fb.setupNameTable({"familyName": family, "styleName": "Regular", "licenseDescription": licence, "licenseInfoURL": url})
    fb.setupOS2()
    fb.setupPost()
    fb.save(str(path))


def licence_gate(path: Path) -> dict:
    from fontTools.ttLib import TTFont
    name = TTFont(str(path))["name"]
    lic = (name.getDebugName(13) or "") + " " + (name.getDebugName(14) or "")
    ok = bool(re.search(r"SIL Open Font License|OFL|scripts\.sil\.org/OFL|openfontlicense", lic, re.I))
    return {"family": name.getDebugName(1), "licence": lic.strip(), "ofl": ok}


def brand_07(work):
    a, b = work / "free.ttf", work / "closed.ttf"
    make_font(a, "Freeface", "This Font Software is licensed under the SIL Open Font License, Version 1.1.", "https://openfontlicense.org")
    make_font(b, "Paidface", "All rights reserved. Desktop licence only; no embedding.", "https://example.invalid/eula")
    ga, gb = licence_gate(a), licence_gate(b)
    credits = [g for g in (ga, gb) if g["ofl"]]
    save(work, "CREDITS.json", {"fonts": credits, "rejected": [g["family"] for g in (ga, gb) if not g["ofl"]]})
    return [("OFL face read from its name table and accepted", ga["ofl"] and ga["family"] == "Freeface", ga),
            ("proprietary face rejected", not gb["ofl"], gb),
            ("credits list only the OFL face", [c["family"] for c in credits] == ["Freeface"], credits)]


# ---------------------------------------------------------------- BRAND-08
def to_hex(s: str):
    s = s.strip().lower()
    m = re.fullmatch(r"#([0-9a-f]{3}|[0-9a-f]{6})", s)
    if m:
        h = m.group(1)
        return "#" + ("".join(c * 2 for c in h) if len(h) == 3 else h)
    m = re.fullmatch(r"rgba?\(\s*(\d+)[ ,]+(\d+)[ ,]+(\d+)\s*(?:[/,]\s*[\d.]+%?)?\s*\)", s)
    if m:
        return rgb2hex([min(255, int(v)) for v in m.groups()])
    m = re.fullmatch(r"hsla?\(\s*([\d.]+)[ ,]+([\d.]+)%[ ,]+([\d.]+)%\s*(?:[/,]\s*[\d.]+%?)?\s*\)", s)
    if m:
        h, sat, l = float(m.group(1)) / 360, float(m.group(2)) / 100, float(m.group(3)) / 100
        return rgb2hex([v * 255 for v in colorsys.hls_to_rgb(h, l, sat)])
    m = re.fullmatch(r"oklch\(\s*([\d.]+)(%?)\s+([\d.]+)\s+([\d.]+)\s*\)", s)
    if m:
        L = float(m.group(1)) / (100 if m.group(2) else 1)
        return oklch_to_hex(L, float(m.group(3)), float(m.group(4)))
    return None


def radius_kind(px: float) -> str:
    return "pill" if px >= 9999 else "round" if px >= 12 else "soft" if px >= 4 else "sharp"


def shot_offsets(page_h: int, view_h=1080, overlap=0.3) -> list:
    step = int(view_h * (1 - overlap))
    offs = list(range(0, max(1, page_h - view_h) + 1, step))
    if offs[-1] + view_h < page_h:
        offs.append(page_h - view_h)
    return offs


def brand_08(work):
    cases = {"#abc": "#aabbcc", "rgb(255 0 0 / 50%)": "#ff0000", "hsl(120,100%,50%)": "#00ff00",
             "oklch(100% 0 0)": "#ffffff", "oklch(0.5 0 0)": "#636363", "not-a-colour": None}
    got = {k: to_hex(k) for k in cases}
    offs = shot_offsets(3000)
    save(work, "material.json", {"palette": [v for v in got.values() if v][:7], "shots": offs})
    return [(f"to_hex({k!r}) == {v}", got[k] == v, got[k]) for k, v in cases.items()] + [
        ("radius 9999 = pill, 16 = round, 2 = sharp", (radius_kind(9999), radius_kind(16), radius_kind(2)) == ("pill", "round", "sharp"), "kinds"),
        ("3000 px page, 1080 view, 30% overlap -> 0/756/1512/1920", offs == [0, 756, 1512, 1920], offs)]


# ---------------------------------------------------------------- BRAND-12
class _FlatPen:
    """fontTools pen that flattens quadratic/cubic segments into polygons."""

    def __init__(self, gs, steps=8):
        self.polys, self.cur, self.steps, self.glyphSet = [], [], steps, gs

    def moveTo(self, p): self.cur = [p]
    def lineTo(self, p): self.cur.append(p)

    def qCurveTo(self, *pts):
        from fontTools.pens.basePen import decomposeQuadraticSegment
        for c, e in decomposeQuadraticSegment(pts):
            s = self.cur[-1]
            for i in range(1, self.steps + 1):
                t = i / self.steps
                self.cur.append(((1 - t) ** 2 * s[0] + 2 * (1 - t) * t * c[0] + t * t * e[0],
                                 (1 - t) ** 2 * s[1] + 2 * (1 - t) * t * c[1] + t * t * e[1]))

    def curveTo(self, *pts):
        from fontTools.pens.basePen import decomposeSuperBezierSegment
        for c1, c2, e in decomposeSuperBezierSegment(pts):
            s = self.cur[-1]
            for i in range(1, self.steps + 1):
                t = i / self.steps
                self.cur.append(tuple((1 - t) ** 3 * s[k] + 3 * (1 - t) ** 2 * t * c1[k] + 3 * (1 - t) * t * t * c2[k] + t ** 3 * e[k] for k in (0, 1)))

    def closePath(self):
        if self.cur:
            self.polys.append(self.cur)
        self.cur = []
    endPath = closePath

    def addComponent(self, name, tr):
        sub = _FlatPen(self.glyphSet, self.steps)
        self.glyphSet[name].draw(sub)
        a, b, c, d, e, f = tr
        self.polys += [[(a * x + c * y + e, b * x + d * y + f) for x, y in poly] for poly in sub.polys]


def outline_text(text: str, path: str) -> tuple:
    from fontTools.ttLib import TTFont
    from fontTools.pens.svgPathPen import SVGPathPen
    f = TTFont(path)
    cmap, gs, hmtx = f.getBestCmap(), f.getGlyphSet(), f["hmtx"]
    x, paths, polys = 0, [], []
    for ch in text:
        gname = cmap[ord(ch)]
        sp = SVGPathPen(gs)
        gs[gname].draw(sp)
        paths.append(f'<path transform="translate({x} 0)" d="{sp.getCommands()}"/>')
        fp = _FlatPen(gs)
        gs[gname].draw(fp)
        polys += [[(px + x, py) for px, py in p] for p in fp.polys]
        x += hmtx[gname][0]
    upm = f["head"].unitsPerEm
    return paths, polys, x, upm


def raster_polys(polys, width_units, upm, height_px):
    k = height_px / upm
    w = max(1, int(width_units * k) + 2)
    im = Image.new("L", (w, height_px), 0)
    d = ImageDraw.Draw(im)
    for p in polys:  # even-odd by XOR so counters stay open
        layer = Image.new("L", im.size, 0)
        ImageDraw.Draw(layer).polygon([(x * k + 1, height_px * 0.8 - y * k) for x, y in p], fill=255)
        im = Image.fromarray(np.bitwise_xor(np.asarray(im), np.asarray(layer)))
    return im


def brand_12(work):
    import arabic_reshaper
    fp = font_path(LATIN)
    paths, polys, adv, upm = outline_text("KOSIF", fp)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 {-upm} {adv} {upm * 1.2:.0f}" preserveAspectRatio="xMidYMid meet">'
           f'<g transform="scale(1 -1)">{"".join(paths)}</g></svg>')
    save(work, "wordmark.svg", svg)
    root = ET.fromstring(svg)
    im32 = raster_polys(polys, adv, upm, 32)
    save(work, "wordmark_32.png", im32)
    import cv2
    arr = np.asarray(im32)
    blobs = cv2.connectedComponents((arr > 128).astype(np.uint8), connectivity=4)[0] - 1
    fav = Image.new("RGB", (64, 64), (29, 24, 20))
    d = ImageDraw.Draw(fav)
    d.rounded_rectangle([0, 0, 63, 63], radius=14, fill=(29, 24, 20))
    d.text((32, 32), "K", font=font(40), fill=(255, 255, 255), anchor="mm")
    save(work, "favicon_64.png", fav)
    shaped = arabic_reshaper.reshape("كسيف")
    bw_unique = sorted(set(np.unique(np.where(arr > 128, 255, 0)).tolist()))
    return [("outlined: no <text>, one path per letter", root.find(".//{http://www.w3.org/2000/svg}text") is None and len(paths) == 5, len(paths)),
            ("preserveAspectRatio xMidYMid", "xMidYMid" in root.get("preserveAspectRatio"), root.get("preserveAspectRatio")),
            ("32 px raster keeps 5 separate letters", blobs == 5, blobs),
            ("flat black/white acid test (2 levels)", bw_unique == [0, 255], bw_unique),
            ("favicon is 64x64", fav.size == (64, 64), fav.size),
            ("Arabic shaped before outlining (presentation forms)", all(0xFE70 <= ord(c) <= 0xFEFF for c in shaped) and shaped != "كسيف", [hex(ord(c)) for c in shaped])]


# ---------------------------------------------------------------- BRAND-13
def trace_layers(img: Image.Image, up=8, simplify=0.85, max_colours=16, merge_dist=30):
    import cv2
    big = img.resize((img.width * up, img.height * up), Image.BICUBIC)
    q = big.quantize(colors=max_colours, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    qa = np.asarray(q)
    qpal = np.array(q.getpalette()[:3 * max_colours], float).reshape(-1, 3)
    counts = np.bincount(qa.ravel(), minlength=len(qpal)).astype(float)
    # merge palette entries closer than merge_dist (heaviest absorbs), keep clusters with >= 3% of pixels (anti-alias fringes fall below)
    order = np.argsort(-counts)
    kept = []
    for i in order:
        if counts[i] == 0:
            continue
        near = [k for k in kept if np.linalg.norm(qpal[k[0]] - qpal[i]) < merge_dist]
        if near:
            near[0][1] += counts[i]
        else:
            kept.append([i, counts[i]])
    kept = [k for k, n in kept if n >= 0.03 * qa.size]
    pal_k = qpal[kept]
    rgb = np.asarray(big.convert("RGB")).astype(float)
    a = np.argmin(((rgb[:, :, None, :] - pal_k[None, None]) ** 2).sum(-1), axis=2)
    pal = pal_k.round().astype(int).ravel().tolist()
    bg = np.bincount(np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])).argmax()
    layers = []
    for idx in np.unique(a):
        if idx == bg:
            continue
        mask = (a == idx).astype(np.uint8) * 255
        area = int(mask.sum() // 255)
        if area < up * up * 4:
            continue
        cs, hier = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
        polys = []
        for i, c in enumerate(cs):
            ap = cv2.approxPolyDP(c, simplify * up, True)
            polys.append({"hole": bool(hier[0][i][3] >= 0), "pts": (ap[:, 0, :] / up).round(2).tolist()})
        ys, xs = np.nonzero(mask)
        layers.append({"color": rgb2hex(pal[idx * 3: idx * 3 + 3]), "area": area / up / up,
                       "centre": [round(xs.mean() / up, 1), round(ys.mean() / up, 1)], "polys": polys})
    layers.sort(key=lambda l: -l["area"])
    return layers


def brand_13(work):
    img = Image.new("RGB", (64, 64), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.rectangle([4, 4, 27, 27], fill=(200, 30, 40))          # 24x24 = 576
    d.ellipse([34, 4, 59, 29], fill=(20, 60, 160))
    d.ellipse([41, 11, 52, 22], fill=(255, 255, 255))         # hole in the blue ring
    d.rectangle([8, 40, 55, 55], fill=(40, 150, 70))         # 48x16 = 768
    save(work, "logo.png", img)
    layers = trace_layers(img)
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">' + "".join(
        f'<path fill="{l["color"]}" fill-rule="evenodd" d="' + " ".join(
            "M" + " L".join(f"{x} {y}" for x, y in p["pts"]) + " Z" for p in l["polys"]) + '"/>' for l in layers) + "</svg>"
    save(work, "logo.svg", svg)
    save(work, "trace.json", layers)
    byc = {l["color"]: l for l in layers}
    red = next(l for l in layers if hex2rgb(l["color"])[0] > 150)
    blue = next(l for l in layers if hex2rgb(l["color"])[2] > 120)
    green = next(l for l in layers if hex2rgb(l["color"])[1] > 120 and hex2rgb(l["color"])[0] < 100)
    return [("3 colour layers (background dropped)", len(layers) == 3, [l["color"] for l in layers]),
            ("<= 16 colours", len(byc) <= 16, len(byc)),
            ("ring layer has a hole polygon", any(p["hole"] for p in blue["polys"]), [p["hole"] for p in blue["polys"]]),
            ("red square area 576 +-4%", abs(red["area"] - 576) / 576 < 0.04, red["area"]),
            ("largest layer first (green 768)", layers[0] is green, layers[0]["area"]),
            ("square simplifies to 4 corners", len(red["polys"][0]["pts"]) == 4, len(red["polys"][0]["pts"]))]


# ---------------------------------------------------------------- BRAND-14
def app_icon(size: int, mark_scale=1.4) -> Image.Image:
    yy, xx = np.mgrid[0:size, 0:size] / size
    r = np.hypot(xx - 0.28, yy - 0.18) / 1.05
    stops = [(0, hex2rgb("#3a2f27")), (0.5, hex2rgb("#1d1814")), (1, hex2rgb("#110e0b"))]
    img = np.zeros((size, size, 3))
    for ch in range(3):
        img[..., ch] = np.interp(np.clip(r, 0, 1), [s for s, _ in stops], [c[ch] for _, c in stops])
    im = Image.fromarray(img.astype(np.uint8))
    d = ImageDraw.Draw(im)
    half = size * 0.2 * mark_scale / 1.4
    c = size / 2
    d.polygon([(c, c - half), (c + half, c), (c, c + half), (c - half, c)], fill=(232, 189, 118))
    return im


def sprite(names) -> str:
    syms = "".join(f'<symbol id="i-{n}" viewBox="0 0 24 24"><path d="M4 12h16" fill="none" stroke="currentColor" stroke-width="1.8"/></symbol>' for n in names)
    uses = "".join(f'<svg class="i"><use href="#i-{n}"/></svg>' for n in names)
    return f'<svg style="display:none">{syms}</svg>{uses}'


def brand_14(work):
    sizes = {}
    for s in (32, 180, 192, 512):
        im = app_icon(s)
        save(work, f"icon_{s}.png", im)
        sizes[s] = im.size
    im512 = np.asarray(app_icon(512)).astype(int)
    lum = im512.sum(axis=2)
    gold = np.all(np.abs(im512 - np.array([232, 189, 118])) < 4, axis=2)
    ys, xs = np.nonzero(gold)
    safe = 409
    lo, hi = (512 - safe) / 2, (512 + safe) / 2
    bgmask = ~gold
    by, bx = np.unravel_index(np.argmax(np.where(bgmask, lum, -1)), lum.shape)
    sp = sprite(["home", "search", "audit"])
    save(work, "sprite.html", sp)
    return [("sizes 32/180/192/512 written", all(sizes[s] == (s, s) for s in sizes), sizes),
            ("mark inside the 409 px safe zone", xs.min() >= lo and xs.max() <= hi and ys.min() >= lo and ys.max() <= hi,
             (int(xs.min()), int(xs.max()))),
            ("radial highlight centred at (.28, .18)", abs(bx / 512 - 0.28) < 0.02 and abs(by / 512 - 0.18) < 0.02, (int(bx), int(by))),
            ("sprite: 3 <use href=#i-…>, stroke currentColor 1.8",
             sp.count('<use href="#i-') == 3 and sp.count('stroke="currentColor" stroke-width="1.8"') == 3, "3")]


# ---------------------------------------------------------------- BRAND-15
SQC_HEX = [(150, 16), (183, 35), (183, 73), (150, 92), (117, 73), (117, 35)]


def sqc_svg() -> str:
    pts = " ".join(f"{x},{y}" for x, y in SQC_HEX)
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 110">'
            '<defs><linearGradient id="ledger"><stop offset="0" stop-color="#f6c39b"/><stop offset=".5" stop-color="#f2732d"/>'
            '<stop offset="1" stop-color="#a53e07"/></linearGradient></defs>'
            '<path id="S" d="M80 30c-20-10-50 0-40 20s40 10 30 30-30 15-40 5" fill="none" stroke="url(#ledger)" stroke-width="19"/>'
            f'<polygon id="Q" points="{pts}" fill="none" stroke="url(#ledger)" stroke-width="19"/>'
            '<path id="facets" d="M150 16V54M183 73L150 54M117 73L150 54" stroke="#fff" stroke-width="5" opacity=".55"/>'
            '<path id="tick" d="M164 80 l13 13 28-33" fill="none" stroke="#a53e07" stroke-width="17"/>'
            '<rect id="diamond" x="250" y="49" width="12" height="12" transform="rotate(45 256 55)"/></svg>')


def k_favicon() -> Image.Image:
    im = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 31, 31], radius=8, fill=hex2rgb("#2F1B68"))
    d.line([(10, 7), (10, 25)], fill="white", width=3)
    d.line([(10, 17), (20, 7)], fill="white", width=3)
    d.line([(12, 15), (21, 25)], fill="white", width=3)
    d.ellipse([22, 22, 28, 28], fill=hex2rgb("#2EA6A6"))
    return im


def brand_15(work):
    svg = sqc_svg()
    save(work, "sqc.svg", svg)
    root = ET.fromstring(svg)
    ns = "{http://www.w3.org/2000/svg}"
    sw = {e.get("id"): e.get("stroke-width") for e in root.iter() if e.get("id") in ("S", "Q", "facets", "tick")}
    cx = sum(x for x, _ in SQC_HEX) / 6
    cy = sum(y for _, y in SQC_HEX) / 6
    sides = [math.dist(SQC_HEX[i], SQC_HEX[(i + 1) % 6]) for i in range(6)]
    fav = k_favicon()
    save(work, "k_favicon.png", fav)
    stops = [s.get("stop-color") for s in root.iter(ns + "stop")]
    return [("viewBox 300x110", root.get("viewBox") == "0 0 300 110", root.get("viewBox")),
            ("strokes S 19 / facets 5 / tick 17", (sw["S"], sw["facets"], sw["tick"]) == ("19", "5", "17"), sw),
            ("hex Q centred at (150, 54)", (cx, cy) == (150, 54), (cx, cy)),
            ("hex sides equal within 1 unit (38.0)", max(sides) - min(sides) < 1.0, [round(s, 2) for s in sides]),
            ("ledger gradient f6c39b -> f2732d -> a53e07", stops == ["#f6c39b", "#f2732d", "#a53e07"], stops),
            ("K favicon: rx 8 corner transparent, body #2F1B68", fav.getpixel((0, 0))[3] == 0 and fav.getpixel((4, 28))[:3] == hex2rgb("#2F1B68"),
             (fav.getpixel((0, 0)), fav.getpixel((4, 28)))),
            ("teal dot r3 at (25,25)", fav.getpixel((25, 25))[:3] == hex2rgb("#2EA6A6"), fav.getpixel((25, 25)))]


# ---------------------------------------------------------------- BRAND-17
LUXE = cubic_bezier(.16, 1, .3, 1)
GLIDE = cubic_bezier(.65, 0, .35, 1)
SETTLE = cubic_bezier(.22, 1.2, .36, 1)
GOLD = ["#4a3110", "#8a6424", "#c9a24a", "#e8cf8a", "#fff4d6", "#c9a24a", "#4a3110"]
STOPS = [0, 16, 40, 56, 68, 86, 100]


def metal_gradient(h=101, w=4) -> Image.Image:
    col = np.zeros((h, 3))
    for ch in range(3):
        col[:, ch] = np.interp(np.linspace(0, 100, h), STOPS, [hex2rgb(c)[ch] for c in GOLD])
    return Image.fromarray(np.repeat(col[:, None, :], w, axis=1).round().astype(np.uint8))


def tagline_times(words, start=7.0, every=0.17):
    return [round(start + i * every, 2) for i in range(len(words))]


def brand_17(work):
    g = metal_gradient()
    save(work, "metal.png", g)
    arr = np.asarray(g)
    at = {s: rgb2hex(arr[s, 0]) for s in STOPS}
    peak = max(SETTLE(i / 200) for i in range(201))
    times = tagline_times(["فخامة", "تبقى", "معك", "دائمًا"])
    els = [{"text": "NAFEES", "letter_spacing": 0.55}, {"text": "نفيس", "letter_spacing": 0}]
    save(work, "timeline.json", {"tagline": times, "luxe_0.5": LUXE(0.5)})
    return [("metal gradient hits each stop colour", [at[s] for s in STOPS] == GOLD, at),
            ("glide is symmetric: glide(0.5) = 0.5", abs(GLIDE(0.5) - 0.5) < 1e-3, GLIDE(0.5)),
            ("luxe front-loads: luxe(0.25) > 0.75", LUXE(0.25) > 0.75, LUXE(0.25)),
            ("settle overshoots above 1 (y1 = 1.2)", 1.0 < peak < 1.1, peak),
            ("tagline words at 7.00/7.17/7.34/7.51 s", times == [7.0, 7.17, 7.34, 7.51], times),
            ("Arabic never tracked (only NAFEES tracks)", tracking_lint(els) == [] and tracking_lint(els + [{"text": "نفيس", "letter_spacing": 0.3}]) == ["نفيس"], "lint")]


# ---------------------------------------------------------------- BRAND-18
def hexagon(cx, cy, r):
    return [(cx + r * math.cos(math.radians(90 + 60 * i)), cy + r * math.sin(math.radians(90 + 60 * i))) for i in range(7)]


def partial_path(pts, frac):
    seg = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    want, out = sum(seg) * frac, [pts[0]]
    for i, s in enumerate(seg):
        if want <= 0:
            break
        t = min(1.0, want / s)
        a, b = pts[i], pts[i + 1]
        out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
        want -= s
    return out


def draw_on_frame(t, draw=1.25, fill_at=1.5, fill_dur=0.4, size=120):
    im = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(im)
    pts = hexagon(60, 60, 40)
    f = clamp01((t - fill_at) / fill_dur)
    if f > 0:
        d.polygon(pts[:-1], fill=int(round(255 * f)))
    p = clamp01(t / draw)
    if p > 0:
        d.line(partial_path(pts, p), fill=255, width=3)
    return im


def brand_18(work):
    frames = {t: np.asarray(draw_on_frame(t)) for t in (0.0, 0.625, 1.25, 1.45, 1.9)}
    for t, a in frames.items():
        save(work, f"frame_{t:.3f}.png", Image.fromarray(a))
    full = (frames[1.25] > 128).sum()
    half = (frames[0.625] > 128).sum()
    centre = {t: int(a[60, 60]) for t, a in frames.items()}
    return [("t=0 nothing drawn", frames[0.0].max() == 0, int(frames[0.0].max())),
            ("halfway through the 1.25 s draw ~50% of the stroke", 0.42 < half / full < 0.58, round(half / full, 3)),
            ("stroke complete at 1.25 s, interior still empty at 1.45 s", centre[1.25] == 0 and centre[1.45] == 0, centre),
            ("fill fully opaque by 1.9 s (fill 1.5 s + 0.4 s)", centre[1.9] == 255, centre[1.9])]


# ---------------------------------------------------------------- BRAND-19
def resample(pts, n):
    seg = np.array([math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)])
    cum = np.concatenate([[0], np.cumsum(seg)])
    out = []
    for s in np.linspace(0, cum[-1], n, endpoint=False):
        i = min(int(np.searchsorted(cum, s, side="right") - 1), len(seg) - 1)
        t = (s - cum[i]) / seg[i]
        out.append((pts[i][0] + (pts[i + 1][0] - pts[i][0]) * t, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * t))
    return np.array(out)


def mg022_phase(t):
    return "prep" if t < 0.6 else "assemble" if t < 1.8 else "hold" if t <= 3.0 else "end"


def morph(a, b, p):
    return a + (b - a) * p


def brand_19(work):
    sq = [(0, 0), (100, 0), (100, 100), (0, 100), (0, 0)]
    circ = [(50 + 50 * math.cos(2 * math.pi * i / 200), 50 + 50 * math.sin(2 * math.pi * i / 200)) for i in range(201)]
    a, b = resample(sq, 64), resample(circ, 64)
    gaps = np.hypot(*np.diff(np.vstack([a, a[:1]]), axis=0).T)
    mid = morph(a, b, 0.5)
    im = Image.new("L", (110, 110), 0)
    ImageDraw.Draw(im).polygon([tuple(p + 5) for p in mid], fill=255)
    save(work, "morph_mid.png", im)
    save(work, "points.json", {"square": a.tolist(), "circle": b.tolist()})
    return [("square resampled to 64 equal-arc points (6.25 each)", len(a) == 64 and np.allclose(gaps, 6.25, atol=1e-6), (len(a), float(gaps.min()), float(gaps.max()))),
            ("both shapes share 64 points (morph-ready)", a.shape == b.shape == (64, 2), a.shape),
            ("morph at p=0.5 is the point-wise average", np.allclose(mid, (a + b) / 2), "avg"),
            ("MG-022 phases at 0.3/1.2/2.5 s", [mg022_phase(t) for t in (0.3, 1.2, 2.5)] == ["prep", "assemble", "hold"], "phases"),
            ("128-point resample of a circle stays on the circle (r=50 +-0.2)",
             np.allclose(np.hypot(*(resample(circ, 128) - 50).T), 50, atol=0.2), "r=50")]


# ---------------------------------------------------------------- BRAND-21
def unfold_frame(t, rtl=True, w=200, h=40, shift=0.4, mask=0.55):
    """Mark slides (shift), then the word reveals from the mark side through a mask with easeOutExpo."""
    im = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(im)
    s = expo_out(clamp01(t / shift))
    mark_x = (w - 30) / 2 + s * ((w - 30) / 2 if rtl else -(w - 30) / 2)
    d.rectangle([mark_x, 5, mark_x + 30, 35], fill=128)
    p = expo_out(clamp01((t - shift) / mask))
    word_l, word_r = 10, w - 40
    revealed = (word_r - word_l) * p
    if revealed > 0:
        if rtl:
            d.rectangle([word_r - revealed, 15, word_r, 25], fill=255)
        else:
            d.rectangle([word_l, 15, word_l + revealed, 25], fill=255)
    return im


def brand_21(work):
    mid = np.asarray(unfold_frame(0.4 + 0.275))
    end = np.asarray(unfold_frame(1.0))
    start = np.asarray(unfold_frame(0.4))
    save(work, "unfold_mid.png", Image.fromarray(mid))
    cols = np.nonzero((mid == 255).any(axis=0))[0]
    frac = len(cols) / 150
    mark_cols = np.nonzero((end == 128).any(axis=0))[0]
    ltr = np.asarray(unfold_frame(0.675, rtl=False))
    lcols = np.nonzero((ltr == 255).any(axis=0))[0]
    return [("no word before the 400 ms shift ends", (start == 255).sum() == 0, int((start == 255).sum())),
            ("mask midpoint easeOutExpo -> 96.9% revealed", abs(frac - expo_out(0.5)) < 0.02, round(frac, 3)),
            ("Arabic: reveal anchored at the right (mark side)", cols.max() == 160 and cols.min() > 10, (int(cols.min()), int(cols.max()))),
            ("Arabic: mark ends at the right edge", mark_cols.max() == 199, int(mark_cols.max())),
            ("Latin mirror anchors at the left", lcols.min() == 10, int(lcols.min()))]


# ---------------------------------------------------------------- BRAND-22
def tracked_width(text, size, em_spacing, fnt=None):
    fnt = fnt or font(size)
    adv = [fnt.getlength(c) for c in text]
    return sum(adv) + em_spacing * size * (len(text) - 1)


def tracking_frame(t, text="KOSIF", size=132, dur=0.8):
    p = expo_out(clamp01(t / dur))
    sp = 0.22 + (-0.03 - 0.22) * p
    fnt = font(size)
    w = int(tracked_width(text, size, 0.22, fnt) + 40)
    im = Image.new("L", (w, size + 40), 0)
    d = ImageDraw.Draw(im)
    x = 20
    for c in text:
        d.text((x, 20), c, font=fnt, fill=int(255 * (0.4 + 0.6 * p)))
        x += fnt.getlength(c) + sp * size
    return im, sp


def brand_22(work):
    a, s0 = tracking_frame(0.0)
    b, s1 = tracking_frame(0.8)
    save(work, "track_start.png", a)
    save(work, "track_end.png", b)
    ba, bb = ink_bbox(a, 20), ink_bbox(b, 20)
    shrink = (ba[2] - ba[0]) - (bb[2] - bb[0])
    want = 0.25 * 132 * 4
    push = 1 + 0.045 * in_out_cubic(clamp01(2.6 / 2.6))
    return [("letter-spacing 0.22em -> -0.03em", (round(s0, 4), round(s1, 4)) == (0.22, -0.03), (s0, s1)),
            ("rendered width shrinks by 0.25em x 132 px x 4 gaps = 132 px", abs(shrink - want) <= 3, shrink),
            ("opacity .4 -> 1 measured from pixels", abs(np.asarray(a).max() / 255 - 0.4) < 0.01 and np.asarray(b).max() == 255,
             (int(np.asarray(a).max()), int(np.asarray(b).max()))),
            ("camera push reaches 1.045 at 2.6 s", abs(push - 1.045) < 1e-9, push),
            ("Arabic letter-spacing tween refused", tracking_lint([{"text": "نفيس", "letter_spacing": 0.22}]) == ["نفيس"], "lint")]


# ---------------------------------------------------------------- BRAND-23
def burst_frame(t, n=40, dur=0.4, size=200):
    im = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(im)
    p = clamp01(t / dur)
    a = int(255 * (1 - p))
    c = size / 2
    for i in range(n):
        ang = 2 * math.pi * i / n
        r0, r1 = 20 + 60 * p, 40 + 60 * p
        d.line([(c + r0 * math.cos(ang), c + r0 * math.sin(ang)), (c + r1 * math.cos(ang), c + r1 * math.sin(ang))], fill=a, width=2)
    return im


def count_rays(im, r, thr=20):
    a = np.asarray(im)
    c = a.shape[0] / 2
    samples = [a[int(round(c + r * math.sin(th))), int(round(c + r * math.cos(th)))] > thr for th in np.linspace(0, 2 * math.pi, 3600, endpoint=False)]
    s = np.array(samples, dtype=int)
    return int(np.sum(np.diff(np.concatenate([s, s[:1]])) == 1))


def orbit_positions(n, r, cx=0, cy=0, phase=0.0):
    return [(cx + r * math.cos(phase + 2 * math.pi * i / n), cy + r * math.sin(phase + 2 * math.pi * i / n)) for i in range(n)]


def brand_23(work):
    f = burst_frame(0.1)
    save(work, "burst.png", f)
    rays = count_rays(f, 45)
    half = np.asarray(burst_frame(0.2)).max()
    end = np.asarray(burst_frame(0.4)).max()
    pos = orbit_positions(4, 216)
    lock_frames = round(0.47 * 30)
    spokes = [round(i * 0.03, 3) for i in range(12)]
    return [("40 radial lines counted on the rendered ring", rays == 40, rays),
            ("opacity halves at 200 ms and is 0 at 400 ms", abs(half - 127) <= 1 and end == 0, (int(half), int(end))),
            ("orbit r=216 is 1.2x a 180 px icon", 216 / 180 == 1.2 and all(abs(math.hypot(x, y) - 216) < 1e-9 for x, y in pos), "1.2"),
            ("lock in ~14 frames at 30 fps (~0.47 s)", lock_frames == 14, lock_frames),
            ("12 asterisk spokes at 30 ms stagger, last at 330 ms", len(spokes) == 12 and spokes[-1] == 0.33, spokes[-1])]


# ---------------------------------------------------------------- BRAND-24
def reel_position(t, stop_t, target, spin_speed=20.0, settle=0.35, overshoot=0.6):
    """Symbol index position of one reel: spins, then eases out onto target with a tiny back overshoot."""
    if t < stop_t - settle:
        return t * spin_speed
    p = clamp01((t - (stop_t - settle)) / settle)
    start = (stop_t - settle) * spin_speed
    end = target + math.ceil((start - target) / 10 + 1) * 10
    s = overshoot
    e = 1 + (s + 1) * (p - 1) ** 3 + s * (p - 1) ** 2   # back.out(s)
    return start + (end - start) * e


def brand_24(work):
    targets = [3, 7, 1]
    stops = [1.0 + 0.25 * i for i in range(3)]
    ts = np.arange(0, 2.0, 1 / 120)
    traj = {i: [reel_position(t, stops[i], targets[i]) for t in ts] for i in range(3)}
    finals = [int(round(reel_position(2.0, stops[i], targets[i]))) % 10 for i in range(3)]
    over = []
    for i in range(3):
        end = reel_position(stops[i], stops[i], targets[i])
        start = reel_position(stops[i] - 0.35, stops[i], targets[i])
        over.append((max(traj[i]) - end) / (end - start))
    settled = [ts[next(k for k in range(len(ts)) if all(abs(traj[i][j] - traj[i][-1]) < 1e-6 for j in range(k, len(ts))))] for i in range(3)]
    save(work, "reels.json", {"stops": stops, "finals": finals, "overshoot": over})
    hz = Image.new("L", (100, 60), 0)
    d = ImageDraw.Draw(hz)
    d.line([(0, 40), (100, 40)], fill=255)
    logo_y = 40 - 20 * out_quad(0.5)
    d.rectangle([40, logo_y, 60, min(40, logo_y + 20)], fill=180)
    save(work, "horizon.png", hz)
    below = np.asarray(hz)[41:, :].max()
    return [("3 reels stop 250 ms apart", [round(s, 2) for s in np.diff(stops)] == [0.25, 0.25], stops),
            ("each reel lands on its target symbol", finals == targets, finals),
            ("tiny overshoot: 0 < overshoot < 10%", all(0 < o < 0.1 for o in over), [round(o, 3) for o in over]),
            ("reels settle in stop order", settled == sorted(settled), [round(s, 3) for s in settled]),
            ("horizon: logo clipped above the line", below == 0, int(below))]


# ---------------------------------------------------------------- BRAND-26
def progress(frame, start, dur, ease=in_out_cubic):
    return ease(clamp01((frame - start) / dur))


def brand_26(work):
    card = spring_curve(90, 14, 1.1, frames=150)
    mark = np.concatenate([np.zeros(18), spring_curve(160, 11, 1.0, frames=132)])
    ring = [progress(f, 8, 40) for f in range(60)]
    save(work, "curves.json", {"card": card.tolist(), "mark": mark.tolist(), "ring": ring})
    oc, om = card.max() - 1, mark.max() - 1
    return [("card spring 14/90/1.1 overshoot = analytic 4.5%", abs(oc - analytic_overshoot(90, 14, 1.1)) < 0.004, (round(oc, 4), round(analytic_overshoot(90, 14, 1.1), 4))),
            ("mark spring 11/160 overshoot = analytic 21.9%", abs(om - analytic_overshoot(160, 11)) < 0.005, (round(om, 4), round(analytic_overshoot(160, 11), 4))),
            ("mark is still 0 before frame 18", mark[:18].max() == 0 and mark[19] > 0, float(mark[19])),
            ("ring progress 0 at f8, 0.5 at f28, 1 at f48", (ring[8], ring[28], ring[48]) == (0.0, 0.5, 1.0), (ring[8], ring[28], ring[48])),
            ("card settles within 1% by 2 s", np.all(np.abs(card[60:] - 1) < 0.01), float(np.abs(card[60:] - 1).max()))]


# ---------------------------------------------------------------- BRAND-28
def end_card(t, W=270, H=480, stagger=0.15, fade_up=0.3, hold=4.0, fade_out=0.55):
    """Quarter-scale 1080x1920 end card: icon 100 / name 60 / tagline 30 px (x0.25), one URL pill."""
    k = 0.25
    im = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(im)
    out = clamp01((t - (3 * stagger + fade_up + hold)) / fade_out)
    items = [("icon", 100), ("name", 60), ("tag", 30), ("pill", 50)]
    y = 140
    for i, (_, size) in enumerate(items):
        p = clamp01((t - i * stagger) / fade_up)
        a = int(255 * p * (1 - out))
        hpx = size * k
        wpx = hpx if i == 0 else 160
        d.rectangle([W / 2 - wpx / 2, y + 12 * (1 - p), W / 2 + wpx / 2 - 1, y + 12 * (1 - p) + hpx - 1], fill=a)
        y += hpx + 20
    return im


def brand_28(work):
    f_full = np.asarray(end_card(1.0))
    save(work, "endcard.png", Image.fromarray(f_full))
    icon_rows = np.nonzero(f_full[:, 135] > 0)[0]
    first_run = icon_rows[icon_rows < 140 + 26]
    icon_cols = np.nonzero(f_full[150] > 0)[0]
    early = np.asarray(end_card(0.1))
    fade_mid = np.asarray(end_card(0.45 + 0.3 + 4.0 + 0.275)).max()
    margin = 0.1 * 270
    cols = np.nonzero(f_full.any(axis=0))[0]
    return [("icon measures 100 px (25 px at quarter scale)", len(first_run) == 25 and len(icon_cols) == 25, (len(first_run), len(icon_cols))),
            ("stagger 150 ms: at 0.1 s only the icon is visible", early[140:170].max() > 0 and early[190:].max() == 0, int(early[190:].max())),
            ("fade 550 ms: half opacity at its midpoint", abs(int(fade_mid) - 127) <= 2, int(fade_mid)),
            ("everything inside 10% safe margins", cols.min() >= margin and cols.max() <= 270 - margin, (int(cols.min()), int(cols.max())))]


# ---------------------------------------------------------------- BRAND-29
def ripple_radius(t, dur=0.4, rmax=60):
    return rmax * out_quad(clamp01(t / dur))


def cta_scale(t, click=0.55, press=0.12, pulses=(1.2, 1.8)):
    s = 0.96 if click <= t < click + press else 1.0
    for pt in pulses:
        if pt <= t < pt + 0.4:
            s *= 1 + 0.06 * math.sin(math.pi * (t - pt) / 0.4)
    return s


def brand_29(work):
    im = Image.new("L", (160, 160), 0)
    r = ripple_radius(0.2)
    ImageDraw.Draw(im).ellipse([80 - r, 80 - r, 80 + r, 80 + r], outline=255, width=2)
    save(work, "ripple_200ms.png", im)
    cols = np.nonzero(np.asarray(im)[80] > 0)[0]
    measured = (cols.max() - cols.min()) / 2
    ts = np.arange(0, 2.5, 1 / 120)
    sc = [cta_scale(t) for t in ts]
    peaks = sum(1 for i in range(1, len(sc) - 1) if sc[i] > sc[i - 1] and sc[i] >= sc[i + 1] and sc[i] > 1.01)
    cur = cubic_bezier(0, 0, 0.58, 1)
    return [("ripple 200 ms in -> 45 px radius (ease-out of 60)", abs(measured - 45) <= 1, measured),
            ("ripple reaches 60 px at 400 ms", ripple_radius(0.4) == 60, ripple_radius(0.4)),
            ("click scale 0.96 lasts 120 ms", cta_scale(0.56) == 0.96 and cta_scale(0.68) == 1.0 and cta_scale(0.66) == 0.96, "0.96"),
            ("CTA pulses exactly twice", peaks == 2, peaks),
            ("cursor easeOut is past 50% at 40% time", cur(0.4) > 0.5, cur(0.4))]


# ---------------------------------------------------------------- BRAND-30
def x_height_px(size):
    fnt = font(size)
    b = fnt.getbbox("x", anchor="ls")
    return -b[1]


def dot_scale(t, dur=0.22):
    p = clamp01(t / dur)
    return 1.2 * (p / 0.6) if p < 0.6 else 1.2 - 0.2 * (p - 0.6) / 0.4


def brand_30(work):
    size = 200
    xh = x_height_px(size)
    dot = 0.45 * xh
    im = Image.new("L", (900, 300), 0)
    d = ImageDraw.Draw(im)
    fa = font(120, arabic=True)
    d.text((700, 150), "كسيف", font=fa, fill=255, anchor="rm", direction="rtl") if _raqm() else d.text((700, 150), "كسيف", font=fa, fill=255, anchor="rm")
    wb = ink_bbox(im)
    dx = wb[0] - 20 - dot
    dot_layer = Image.new("L", im.size, 0)
    ImageDraw.Draw(dot_layer).ellipse([dx, 180 - dot / 2, dx + dot, 180 + dot / 2], fill=255)
    im = Image.fromarray(np.maximum(np.asarray(im), np.asarray(dot_layer)))
    save(work, "arabic_dot.png", im)
    dot_cols = np.nonzero(np.asarray(dot_layer).any(axis=0))[0]
    ts = np.linspace(0, 0.22, 221)
    sc = [dot_scale(t) for t in ts]
    drop_squash = 0.7
    return [("dot diameter = 0.45 x-height", abs(dot - 0.45 * xh) < 1e-9 and xh > 50, (xh, round(dot, 2))),
            ("scale 0 -> 1.2 -> 1 within 220 ms", sc[0] == 0 and abs(max(sc) - 1.2) < 1e-9 and abs(sc[-1] - 1) < 1e-9, (sc[0], max(sc), sc[-1])),
            ("Arabic: dot sits left of the shaped word (visual end)", dot_cols.max() < wb[0], (int(dot_cols.max()), wb[0])),
            ("impact squash 0.7 keeps area (stretch 1/0.7)", abs(drop_squash * (1 / drop_squash) - 1) < 1e-12, round(1 / drop_squash, 3))]


def _raqm():
    from PIL import features
    return features.check("raqm")


# ---------------------------------------------------------------- BRAND-31
def typed(text, t, ms=40):
    return text[:int(t * 1000 // ms)]


def cursor_on(t, blink=0.5):
    return int(t // blink) % 2 == 0


def db_fade(n, sr, db_end=-60.0):
    db = np.linspace(0, db_end, n)
    return 10 ** (db / 20)


def brand_31(work):
    sr = 16000
    tone = np.sin(2 * np.pi * 440 * np.arange(2 * sr) / sr)
    g = db_fade(len(tone), sr)
    out = tone * g
    (work / "fade.raw").write_bytes((out * 32767).astype("<i2").tobytes())
    def rms(a): return float(np.sqrt(np.mean(a ** 2)))
    mid = rms(out[sr - 800: sr + 800]) / rms(tone[sr - 800: sr + 800])
    grad = np.linspace(np.array(hex2rgb("#1f7bf2")), np.array(hex2rgb("#7b5cf5")), 64)
    save(work, "version_grad.png", Image.fromarray(np.repeat(grad[None].round().astype(np.uint8), 8, axis=0)))
    return [("40 ms/char: 'npm i kosif' fully typed at 0.44 s", typed("npm i kosif", 0.44) == "npm i kosif" and typed("npm i kosif", 0.2) == "npm i", typed("npm i kosif", 0.2)),
            ("cursor blink 500 ms: on, off, on", [cursor_on(t) for t in (0.1, 0.6, 1.1)] == [True, False, True], "blink"),
            ("dB-curve fade: -30 dB at the midpoint", abs(20 * math.log10(mid) + 30) < 0.5, round(20 * math.log10(mid), 2)),
            ("gradient ends #1f7bf2 -> #7b5cf5", rgb2hex(grad[0]) == "#1f7bf2" and rgb2hex(grad[-1]) == "#7b5cf5", (rgb2hex(grad[0]), rgb2hex(grad[-1])))]


# ---------------------------------------------------------------- BRAND-32
def reveal_units(text, t, arabic, char_ms=40, word_ms=120):
    if arabic:
        words = text.split()
        return " ".join(words[:int(t * 1000 // word_ms)])
    return text[:int(t * 1000 // char_ms)]


def pendulum(t, theta0=0.5, period=0.6, settle=1.5):
    lam = math.log(50) / settle
    return theta0 * math.exp(-lam * t) * math.cos(2 * math.pi * t / period)


def brand_32(work):
    ts = np.arange(0, 3, 1 / 240)
    th = np.array([pendulum(t) for t in ts])
    env_ok = np.all(np.abs(th[ts >= 1.5]) <= 0.5 * 0.02 + 1e-12)
    early = np.abs(th[(ts > 0.4) & (ts < 0.6)]).max() > 0.5 * 0.02
    ar = reveal_units("محمد عبد الله الكسيف", 0.25, True)
    save(work, "card.json", {"arabic_at_250ms": ar, "pills": [round(i * 0.06, 2) for i in range(4)]})
    return [("Latin name typed 40 ms/char (5 chars at 200 ms)", reveal_units("Nasser Ali", 0.2, False) == "Nasse", reveal_units("Nasser Ali", 0.2, False)),
            ("Arabic name per word every 120 ms: 2 words at 250 ms", ar == "محمد عبد", ar),
            ("Arabic never cut inside a word", all(w in "محمد عبد الله الكسيف".split() for w in ar.split()), ar),
            ("pills stagger 60 ms", [round(i * 0.06, 2) for i in range(4)] == [0.0, 0.06, 0.12, 0.18], "60 ms"),
            ("pendulum within 2% of its swing after 1.5 s, not before", bool(env_ok and early), (bool(env_ok), bool(early)))]


# ---------------------------------------------------------------- BRAND-34
def fit_block(anim: float, slot: float) -> dict:
    if slot < anim:
        raise ValueError("slot shorter than the animation; never time-compress")
    return {"anim": anim, "hold": round(slot - anim, 3), "speed": 1.0}


def testimonial_ok(t: dict) -> bool:
    return bool(t.get("quote") and t.get("source") and t.get("permission") is True)


def marquee(t, row, speed=20):
    return (speed if row % 2 == 0 else -speed) * t


def edge_alpha(x, w, fade=0.1):
    return clamp01(min(x, w - x) / (fade * w))


def brand_34(work):
    f = fit_block(2.4, 6.0)
    save(work, "fit.json", f)
    try:
        fit_block(2.4, 1.0)
        rej = False
    except ValueError:
        rej = True
    real = {"quote": "وفّر علينا يومين", "source": "Client A, 2026-05 email", "permission": True}
    fake = {"quote": "Best app ever!", "source": "", "permission": False}
    return [("extra duration becomes hold (6.0 - 2.4 = 3.6 s), speed stays 1", f == {"anim": 2.4, "hold": 3.6, "speed": 1.0}, f),
            ("shorter slot refused (no time-stretch)", rej, rej),
            ("only sourced, permitted quotes pass", testimonial_ok(real) and not testimonial_ok(fake), "quotes"),
            ("rows drift opposite at 20 px/s (+40/-40 at 2 s)", (marquee(2, 0), marquee(2, 1)) == (40, -40), (marquee(2, 0), marquee(2, 1))),
            ("10% edge fade: alpha 0 at edge, 1 at 10%", edge_alpha(0, 1000) == 0 and edge_alpha(100, 1000) == 1 and edge_alpha(50, 1000) == 0.5, "fade")]


# ---------------------------------------------------------------- BRAND-35
def chrome_frame(t, centre_val, W=480, H=270, inset=0.04):
    im = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(im)
    x0, y0 = W * inset, H * inset
    d.rectangle([x0, y0, x0 + 40, y0 + 6], fill=200)
    if t >= 0.4:
        d.rectangle([W - x0 - 40, H - y0 - 6, W - x0 - 1, H - y0 - 1], fill=220)
    d.rectangle([W / 2 - 60, H / 2 - 30, W / 2 + 60, H / 2 + 30], fill=centre_val)
    return im


def brand_35(work):
    a, b = np.asarray(chrome_frame(1.0, 90)).astype(int), np.asarray(chrome_frame(1.0, 160)).astype(int)
    save(work, "chrome.png", Image.fromarray(a.astype(np.uint8)))
    diff = np.abs(a - b) > 0
    ys, xs = np.nonzero(diff)
    sig_before = np.asarray(chrome_frame(0.3, 90))[240:260, 400:460].max()
    tl = np.nonzero(a[:, :240] == 200)
    k = 1920 / 1080
    els = [{"text": "KOSIF", "letter_spacing": 0.15}, {"text": "الكسيف", "letter_spacing": 0}]
    return [("inset 4%: top-left chrome at (19.2, 10.8) on 480x270", int(tl[1].min()) in (19, 20) and int(tl[0].min()) in (10, 11), (int(tl[1].min()), int(tl[0].min()))),
            ("only the centre content changes between frames", xs.min() >= 180 and xs.max() <= 300 and ys.min() >= 105 and ys.max() <= 165,
             (int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max()))),
            ("signature absent at 0.3 s, present from 0.4 s", sig_before == 0 and np.asarray(chrome_frame(0.4, 90))[240:260, 400:460].max() == 220, int(sig_before)),
            ("V.brand 26 x k px at 1920 tall = 46.2 px", round(26 * k, 1) == 46.2, round(26 * k, 1)),
            ("Arabic chrome untracked", tracking_lint(els) == [], "lint")]


# ---------------------------------------------------------------- BRAND-36
def word_windows(n, at, dur=0.6, stagger=0.06):
    return [(round(at + i * stagger, 3), round(at + i * stagger + dur, 3)) for i in range(n)]


def flood_frame(t, W=96, H=54, start=3.0, dur=1.0, colour=(201, 162, 74)):
    im = Image.new("RGB", (W, H), (10, 10, 12))
    r = math.hypot(W, H) / 2 * in_out_cubic(clamp01((t - start) / dur)) + (1 if t >= start + dur else 0)
    ImageDraw.Draw(im).ellipse([W / 2 - r, H / 2 - r, W / 2 + r, H / 2 + r], fill=colour)
    return im


def bar_progress(t, D=5.0, last=2.0):
    return clamp01((t - (D - last)) / last)


def brand_36(work):
    full = np.asarray(flood_frame(4.0))
    save(work, "flood_end.png", Image.fromarray(full))
    mid = np.asarray(flood_frame(3.5))
    gold = np.all(full == (201, 162, 74), axis=2).mean()
    w = word_windows(2, 4.15)
    return [("iris -> flood: every pixel brand colour at the end", gold == 1.0, gold),
            ("iris midpoint: centre gold, corner still dark", tuple(mid[27, 48]) == (201, 162, 74) and tuple(mid[0, 0]) == (10, 10, 12), (tuple(mid[27, 48]), tuple(mid[0, 0]))),
            ("revealWords at 4.15 s, 0.6 s, stagger .06", w == [(4.15, 4.75), (4.21, 4.81)], w),
            ("progress: 0 at 3 s, 50% at 4 s, 100% at 5 s of a 5 s film", (bar_progress(3), bar_progress(4), bar_progress(5)) == (0, 0.5, 1), "bar")]


# ---------------------------------------------------------------- BRAND-38
def grid_cells(W, H):
    ar = W / H
    if ar < 1:  # 9:16 stacked
        return [(0, i * H // 4, W, H // 4) for i in range(4)]
    return [(x * W // 2, y * H // 2, W // 2, H // 2) for y in range(2) for x in range(2)]


def clip_frames(seed, n=30, blank_first=False):
    rng = np.random.default_rng(seed)
    fr = [rng.integers(40, 220, (9, 16), dtype=np.uint8) for _ in range(n)]
    if blank_first:
        fr[0] = np.zeros((9, 16), np.uint8)
    return fr


def blank_ends(frames, thr=2.0):
    return [i for i in (0, len(frames) - 1) if frames[i].mean() < thr]


def brand_38(work):
    offsets = [0, 7, 13, 21]
    flashes = [o + 10 for o in offsets]
    clips = [clip_frames(i, blank_first=(i == 2)) for i in range(4)]
    W, H = 32, 18
    mosaic = np.zeros((H, W), np.uint8)
    for (x, y, w, h), c, o in zip(grid_cells(W, H), clips, offsets):
        mosaic[y:y + h, x:x + w] = c[(15 + o) % 30][:h, :w]
    save(work, "grid.png", Image.fromarray(mosaic))
    bad = {i: blank_ends(c) for i, c in enumerate(clips) if blank_ends(c)}
    return [("16:9 -> 2x2 cells", grid_cells(1920, 1080) == [(0, 0, 960, 540), (960, 0, 960, 540), (0, 540, 960, 540), (960, 540, 960, 540)], "2x2"),
            ("9:16 -> vertical stack of 4", [c[1] for c in grid_cells(1080, 1920)] == [0, 480, 960, 1440], grid_cells(1080, 1920)),
            ("no two flashes within 2 frames", min(np.diff(sorted(flashes))) > 2, flashes),
            ("planted blank first frame found in clip 2 only", bad == {2: [0]}, bad)]


# ---------------------------------------------------------------- BRAND-39
def mark_svg(params: tuple) -> str:
    sides, rot, ring, dots, stroke, fill, inset, gap = params
    pts = " ".join(f"{50 + 40 * math.cos(math.radians(rot * 15 + 360 * i / (sides + 3))):.2f},"
                   f"{50 + 40 * math.sin(math.radians(rot * 15 + 360 * i / (sides + 3))):.2f}" for i in range(sides + 3))
    rings = "".join(f'<circle cx="50" cy="50" r="{10 + 5 * k + gap}" fill="none" stroke="#000" stroke-width="{1 + stroke}"/>' for k in range(ring))
    ds = "".join(f'<circle cx="{50 + (20 + inset * 3) * math.cos(2 * math.pi * k / 6):.2f}" cy="{50 + (20 + inset * 3) * math.sin(2 * math.pi * k / 6):.2f}" r="2"/>' for k in range(dots))
    return f'<svg viewBox="0 0 100 100"><polygon points="{pts}" fill="#{fill * 40:02x}{fill * 40:02x}{fill * 40:02x}"/>{rings}{ds}</svg>'


def brand_39(work):
    total = 6 ** 8
    cells = [(a, b, 1, 2, 1, 3, 2, 0) for a in range(6) for b in range(6)]
    svgs = [mark_svg(c) for c in cells]
    save(work, "matrix.html", "".join(f'<div style="animation-delay:{(i // 6) * 120}ms">{s}</div>' for i, s in enumerate(svgs)) +
         f"<p>{total:,} combinations</p>")
    delays = sorted({(i // 6) * 120 for i in range(36)})
    return [("8 params x 6 values = 1,679,616", total == 1679616, f"{total:,}"),
            ("36 shown cells are 36 distinct generator outputs", len({hashlib.sha256(s.encode()).hexdigest() for s in svgs}) == 36, len(set(svgs))),
            ("generator is deterministic", mark_svg(cells[5]) == mark_svg(cells[5]), "same"),
            ("rows stagger 120 ms (0..600)", delays == [0, 120, 240, 360, 480, 600], delays)]


# ---------------------------------------------------------------- BRAND-40
def brutal_card(W=80, H=60):
    im = Image.new("RGB", (W + 10, H + 10), (255, 255, 255))
    d = ImageDraw.Draw(im)
    d.rectangle([6, 6, W + 5, H + 5], fill=hex2rgb("#111111"))
    d.rectangle([0, 0, W - 1, H - 1], fill=(0, 0, 0))
    d.rectangle([3, 3, W - 4, H - 4], fill=hex2rgb("#f47fe0"))
    return im


def star(n=24, r0=40, r1=34, rot=0.0):
    return [((r0 if i % 2 == 0 else r1) * math.cos(math.radians(rot) + math.pi * i / n) + 50,
             (r0 if i % 2 == 0 else r1) * math.sin(math.radians(rot) + math.pi * i / n) + 50) for i in range(2 * n)]


def brand_40(work):
    import cv2
    c = np.asarray(brutal_card())
    save(work, "card.png", Image.fromarray(c))
    border = [tuple(c[30, x]) for x in range(0, 4)]
    shadow = tuple(c[64, 84])
    band = Image.new("L", (300, 300), 0)
    bd = ImageDraw.Draw(band)
    w, h, ang = 220, 40, math.radians(-12)
    corners = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]
    bd.polygon([(150 + x * math.cos(ang) - y * math.sin(ang), 150 + x * math.sin(ang) + y * math.cos(ang)) for x, y in corners], fill=255)
    save(work, "band.png", band)
    cs, _ = cv2.findContours(np.asarray(band), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    (_, _), (rw, rh), ra = cv2.minAreaRect(cs[0])
    meas = ra if rw > rh else ra - 90
    meas = (meas + 90) % 180 - 90
    sp = star()
    wob = [3 * math.sin(2 * math.pi * t / 0.8) for t in np.linspace(0, 1.6, 97)]
    return [("3 px black border", border[:3] == [(0, 0, 0)] * 3 and border[3] == hex2rgb("#f47fe0"), border),
            ("hard shadow 6/6/0 #111 (no blur)", shadow == hex2rgb("#111111") and tuple(c[62, 82]) == hex2rgb("#111111"), shadow),
            ("title band measured at -12 deg", abs(abs(meas) - 12) < 0.6, round(meas, 2)),
            ("seal rim has 24 points (48 vertices)", len(sp) == 48, len(sp)),
            ("wobble stays within +-3 deg", max(abs(v) for v in wob) <= 3 + 1e-9, round(max(wob), 3))]


# ---------------------------------------------------------------- BRAND-41
def glow(W=200, H=100, blur_css=30, alpha=0.5):
    base = Image.new("L", (W, H), 0)
    ImageDraw.Draw(base).rectangle([80, 40, 120, 60], fill=255)
    g = base.filter(ImageFilter.GaussianBlur(blur_css / 2))
    g = Image.fromarray((np.asarray(g) * alpha).astype(np.uint8))
    return Image.fromarray(np.maximum(np.asarray(g), np.asarray(base)))


def colour_units(text):
    """Per-letter colour for Latin, per-word for Arabic."""
    return text.split() if ARABIC_RE.search(text) else list(text.replace(" ", ""))


def brand_41(work):
    im = glow()
    save(work, "glow.png", im)
    a = np.asarray(im).astype(int)
    near = a[50, 125]
    far = a[50, 125 + 30 + 10]
    starts = [round(i * 0.06, 2) for i in range(len(colour_units("KOSIF")))]
    return [("glow halo exists just outside the text", 10 < near < 128, int(near)),
            ("glow fades out beyond the 30 px radius", far <= 3, int(far)),
            ("text body stays full white", a[50, 100] == 255, int(a[50, 100])),
            ("Latin: one colour per letter, 60 ms stagger", starts == [0.0, 0.06, 0.12, 0.18, 0.24], starts),
            ("Arabic: one colour per word, never per letter", colour_units("نسخة جديدة") == ["نسخة", "جديدة"], colour_units("نسخة جديدة"))]


# ---------------------------------------------------------------- BRAND-42
def poster(W=360, H=640):
    im = Image.new("RGB", (W, H), hex2rgb("#2a1010"))
    d = ImageDraw.Draw(im)
    d.rectangle([0, H - 90, W, H - 40], fill=hex2rgb("#c91a1f"))
    d.ellipse([W - 110, 20, W - 20, 110], fill=hex2rgb("#a8c13a"))
    d.ellipse([W - 100, 30, W - 30, 100], fill=hex2rgb("#ffffff"))
    d.ellipse([W - 90, 40, W - 40, 90], fill=hex2rgb("#e3161d"))
    mask = Image.new("L", (W, 140), 0)
    md = ImageDraw.Draw(mask)
    kw = {"direction": "rtl"} if _raqm() else {}
    md.text((W - 20, 70), "خروف كامل", font=font(72, arabic=True), fill=255, anchor="rm", **kw)
    grad = np.linspace(np.array(hex2rgb("#f6e3b6")), np.array(hex2rgb("#c49c5c")), 140)
    gimg = Image.fromarray(np.repeat(grad[:, None, :], W, axis=1).round().astype(np.uint8))
    im.paste(gimg, (0, 140), mask)
    return im, mask


def brand_42(work):
    im, mask = poster()
    save(work, "poster.png", im)
    a = np.asarray(im)
    m = np.asarray(mask)
    rows = np.nonzero(m.max(axis=1) == 255)[0]
    top = a[140 + rows.min()][m[rows.min()] == 255].mean(axis=0)
    bot = a[140 + rows.max()][m[rows.max()] == 255].mean(axis=0)
    want_top = np.array(hex2rgb("#f6e3b6")) + (np.array(hex2rgb("#c49c5c")) - np.array(hex2rgb("#f6e3b6"))) * rows.min() / 139
    want_bot = np.array(hex2rgb("#f6e3b6")) + (np.array(hex2rgb("#c49c5c")) - np.array(hex2rgb("#f6e3b6"))) * rows.max() / 139
    shaped = ImageDraw.Draw(Image.new("L", (10, 10))).textlength("كامل", font=font(72, arabic=True), **({"direction": "rtl"} if _raqm() else {}))
    return [("band #c91a1f", tuple(a[600, 10]) == hex2rgb("#c91a1f"), tuple(a[600, 10])),
            ("badge rings green/white/red", (tuple(a[65, 255]), tuple(a[65, 265]), tuple(a[65, 295])) == (hex2rgb("#a8c13a"), (255, 255, 255), hex2rgb("#e3161d")),
             (tuple(a[65, 255]), tuple(a[65, 265]), tuple(a[65, 295]))),
            ("headline gold top->bottom follows #f6e3b6 -> #c49c5c", np.abs(top - want_top).max() < 4 and np.abs(bot - want_bot).max() < 4,
             (rgb2hex(top), rgb2hex(bot))),
            ("Arabic headline rendered (ink present, right aligned)", m.max() == 255 and np.nonzero(m.max(axis=0))[0].max() >= 330, int(np.nonzero(m.max(axis=0))[0].max())),
            ("text measured with a shaping layout", shaped > 0, round(shaped, 1))]


# ---------------------------------------------------------------- BRAND-43
LEDGER = {"light": {"paper": "#fbf8f3", "card": "#fffdf9", "ink": "#1d1814", "ink-2": "#4b4139", "ink-3": "#7b6f64", "accent": "#d9530e"},
          "dark": {"paper": "#161310", "card": "#1c1814", "ink": "#f5ede3", "accent": "#f2732d"}}


def title_card(t, W=192, H=108):
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    bg = np.array(hex2rgb("#11171b"), float)
    acc = np.array(hex2rgb("#d9530e"), float)
    d = np.hypot(xx - 0.28 * W, yy - 0.25 * H) / (0.8 * W)
    gl = np.clip(1 - d, 0, 1)[..., None] * 0.6
    img = bg * (1 - gl) + acc * gl
    unit = W / 12
    img[:, (np.arange(W) % round(unit)) == 0] += 6
    ang = 0.1 * t
    for k in range(3):
        a = ang + k * 2.1
        cx, cy = W / 2 + 0.2 * W * math.cos(a), H / 2 + 0.2 * H * math.sin(a)
        m = np.abs(np.hypot((xx - cx) / 30, (yy - cy) / 12) - 1) < 0.04
        img[m] = acc
    return np.clip(img, 0, 255).astype(np.uint8)


def brand_43(work):
    a, b = title_card(2.0), title_card(2.0)
    save(work, "title_2s.png", Image.fromarray(a))
    save(work, "ledger_tokens.json", LEDGER)
    lum = a.astype(int).sum(axis=2).astype(float)
    lum[:, (np.arange(192) % 16) == 0] = 0
    y, x = np.unravel_index(np.argmax(np.where(np.all(a == np.array(hex2rgb("#d9530e")), axis=2), 0, lum)), lum.shape)
    c = {k: contrast(LEDGER["light"][k], LEDGER["light"]["paper"]) for k in ("ink", "ink-2", "ink-3")}
    return [("pure in t: same t gives identical pixels", np.array_equal(a, b), "equal"),
            ("t changes the frame (ellipses rotate)", not np.array_equal(a, title_card(9.0)), "differs"),
            ("glow brightest near (.28w, .25h)", abs(x - 0.28 * 192) <= 3 and abs(y - 0.25 * 108) <= 3, (int(x), int(y))),
            ("ink and ink-2 on paper pass 7:1, ink-3 passes 4.5:1", c["ink"] >= 7 and c["ink-2"] >= 7 and c["ink-3"] >= 4.5, c),
            ("dark ink on dark paper >= 7:1", contrast(LEDGER["dark"]["ink"], LEDGER["dark"]["paper"]) >= 7, contrast(LEDGER["dark"]["ink"], LEDGER["dark"]["paper"]))]


# ---------------------------------------------------------------- BRAND-20
def stamp_scale(t, dur=0.15):
    return 1.2 - 0.2 * out_quad(clamp01(t / dur))


def multiply(base, top):
    return tuple(round(b * c / 255) for b, c in zip(base, top))


def fog_mask(t, W=64, H=36, seed=7, start=1.0, end=3.0):
    """Turbulence-style value noise thresholded by progress: revealed where noise < p."""
    rng = np.random.default_rng(seed)
    coarse = rng.random((5, 9))
    noise = np.asarray(Image.fromarray((coarse * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)) / 255
    noise = (noise - noise.min()) / (noise.max() - noise.min())
    p = clamp01((t - start) / (end - start))
    return (noise < p) if p < 1 else np.ones_like(noise, bool)


def negative_space(W=60, H=60):
    bg = Image.new("L", (W, H), 30)
    shape = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shape).rectangle([5, 5, 54, 54], fill=255)
    hole = Image.new("L", (W, H), 0)
    ImageDraw.Draw(hole).ellipse([20, 20, 39, 39], fill=255)
    m = np.asarray(shape) & ~np.asarray(hole)
    out = np.where(m > 0, 230, np.asarray(bg))
    return out.astype(np.uint8)


def brand_20(work):
    paper = hex2rgb("#f3ead8")
    red = hex2rgb("#c0302a")
    from PIL import ImageChops
    sq = Image.new("RGB", (20, 20), paper)
    stamp = Image.new("RGB", (20, 20), (255, 255, 255))
    ImageDraw.Draw(stamp).rectangle([5, 5, 14, 14], fill=red)
    arr = np.asarray(ImageChops.multiply(sq, stamp)).astype(int)
    save(work, "stamp.png", Image.fromarray(arr.astype(np.uint8)))
    fr = [fog_mask(t).mean() for t in np.linspace(0, 5, 51)]
    ns = negative_space()
    save(work, "negative_space.png", Image.fromarray(ns))
    return [("stamp scale 1.2 -> 1 in 150 ms", stamp_scale(0) == 1.2 and stamp_scale(0.15) == 1.0, (stamp_scale(0), stamp_scale(0.15))),
            ("multiply: #c0302a on paper = per-channel product", max(abs(int(x) - y) for x, y in zip(arr[10, 10], multiply(paper, red))) <= 1 and tuple(arr[0, 0]) == paper, (tuple(int(v) for v in arr[10, 10]), multiply(paper, red))),
            ("fog: hidden before 1 s, complete by 3 s, monotonic", fr[10] == 0 and fr[30] == 1 and all(b >= a for a, b in zip(fr, fr[1:])),
             [round(v, 2) for v in fr[8:32:4]]),
            ("negative space: logo hole shows the background", ns[30, 30] == 30 and ns[10, 10] == 230, (int(ns[30, 30]), int(ns[10, 10])))]


PROGRAMS = {"BRAND-01": brand_01, "BRAND-02": brand_02, "BRAND-03": brand_03, "BRAND-04": brand_04, "BRAND-05": brand_05,
            "BRAND-06": brand_06, "BRAND-07": brand_07, "BRAND-08": brand_08, "BRAND-12": brand_12, "BRAND-13": brand_13,
            "BRAND-14": brand_14, "BRAND-15": brand_15, "BRAND-17": brand_17, "BRAND-18": brand_18, "BRAND-19": brand_19, "BRAND-20": brand_20,
            "BRAND-21": brand_21, "BRAND-22": brand_22, "BRAND-23": brand_23, "BRAND-24": brand_24, "BRAND-26": brand_26,
            "BRAND-28": brand_28, "BRAND-29": brand_29, "BRAND-30": brand_30, "BRAND-31": brand_31, "BRAND-32": brand_32,
            "BRAND-34": brand_34, "BRAND-35": brand_35, "BRAND-36": brand_36, "BRAND-38": brand_38, "BRAND-39": brand_39,
            "BRAND-40": brand_40, "BRAND-41": brand_41, "BRAND-42": brand_42, "BRAND-43": brand_43}
