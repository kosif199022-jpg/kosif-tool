#!/usr/bin/env python3
"""KOSIF Style Library: 586 visual styles you can ask for by name, offline.

Joins the 86 paraphrased Futurepedia AI Style Atlas methods (FA-01..FA-86,
data/futurepedia_style_atlas_86.json) with 500 original KOSIF styles in 20 groups
(KS-001..KS-500, data/style_library_500.json). Each style has a name in English and
Arabic, a look, the logic that makes it work, a palette, a texture, a composition
motif and a prompt recipe.

Commands: groups, list, find, describe, prompt (with --mix for a 70/30 fusion),
swatch (one deterministic procedural SVG sample), catalog (every swatch plus an
illustrated HTML page, and with --pdf a PDF through headless Chromium), self-test.

Swatches are original procedural drawings of a style's palette, texture and
composition; they are sketches, not finished artwork, and never copied images.
No network, no paid generator, no third-party media.
"""
import argparse
import hashlib
import html
import json
import math
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
DATA_FA = SKILL / "data" / "futurepedia_style_atlas_86.json"
DATA_KS = SKILL / "data" / "style_library_500.json"
W, H = 480, 320
TEXTURES = ("paper", "grain", "canvas", "none", "vignette", "glow", "scan", "halftone")
FA_GROUP_AR = {"Hand-Drawn": "رسم يدوي", "Painterly": "تصوير زيتي ومائي", "Print": "طباعة",
               "Paper & Craft": "ورق وحِرف", "Illustration": "رسم توضيحي",
               "Art & Design Movements": "حركات فنية وتصميم", "Retro Digital": "رقمي كلاسيكي",
               "Retro UI & Neon": "واجهات قديمة ونيون", "Dimensional": "أبعاد ثلاثية",
               "Light & Imaging": "ضوء وتصوير", "Data & Information": "بيانات ومعلومات",
               "Generative & Type": "توليدي وحروف", "Popular Explainer Looks": "أشكال الشرح الشائعة",
               "Cosmic & Psychedelic": "كوني وسايكيديلك"}
FONT_CANDIDATES = (SKILL.parents[2] / "projects" / "mafatih-al-tharwa" / "src" / "fonts" / "Cairo.ttf",
                   SKILL / "proofs" / "_shared" / "fonts" / "Amiri-Regular.ttf")


# ----------------------------------------------------------------------------- data

def _slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def load():
    """Return {"groups": [...], "styles": [...]} with FA and KS styles in one shape."""
    fa = json.loads(DATA_FA.read_text(encoding="utf-8"))
    ks = json.loads(DATA_KS.read_text(encoding="utf-8"))
    if ks.get("schema") != "kosif.style.library.v1":
        raise ValueError("unexpected style library schema")
    groups, styles = [], []
    seen = []
    for s in fa["styles"]:
        cat = s["category"]
        gid = "fa-" + _slug(cat)
        if gid not in seen:
            seen.append(gid)
            groups.append({"id": gid, "name": "Futurepedia · " + cat, "name_ar": "فيوتشربيديا · " + FA_GROUP_AR.get(cat, cat),
                           "source": "fa"})
        sw = ks["site_swatches"][s["source_style_id"]]
        styles.append({"id": s["id"], "slug": s["slug"], "name": s["name"], "name_ar": sw["name_ar"], "group": gid,
                       "source": "fa", "motif": sw["motif"], "texture": sw["texture"], "palette": _order_palette(s, sw.get("ground")),
                       "look": s["look"], "logic": s["explainer_grammar"], "motion": s["motion"],
                       "summary_ar": s["capability_ar"], "fonts": s.get("fonts", []),
                       "prompt": None, "negative": None})
    for g in ks["groups"]:
        groups.append(dict(g, source="ks"))
    for s in ks["styles"]:
        styles.append(dict(s, source="ks"))
    ids = [s["id"] for s in styles]
    if len(ids) != len(set(ids)) or len(styles) != 586:
        raise ValueError("library must hold 586 distinct styles")
    return {"groups": groups, "styles": styles}


def _lum(hexc):
    r, g, b = (int(hexc[i:i + 2], 16) for i in (1, 3, 5))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _order_palette(s, ground=None):
    """FA palettes are frequency lists: put the ground colour first (reviewed ground, else by tone)."""
    pal = list(dict.fromkeys(s["palette"]))
    if ground:
        pal = [ground] + [c for c in pal if c.upper() != ground.upper()]
    else:
        ground = min(pal, key=_lum) if s.get("tone") == "dark" else max(pal, key=_lum)
    rest = [c for c in pal if c != ground]
    rest.sort(key=lambda c: -abs(_lum(c) - _lum(ground)))
    pal = [ground] + rest
    while len(pal) < 5:
        pal.append(pal[len(pal) % max(1, len(pal) - 1) + 1] if len(pal) > 1 else "#888888")
    return pal[:5]


_AR_MAP = str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ة": "ه", "ى": "ي", "ؤ": "و", "ئ": "ي"})
_DIACRITICS = re.compile("[ً-ْـ]")
ALIASES = {"زخرفة": "ornament", "هندسي": "geometry", "خط": "calligraphy type", "حروف": "letters type",
           "نسيج": "weave textile", "تطريز": "stitch embroidery", "ورق": "paper", "طباعة": "print",
           "ضوء": "light glow", "نيون": "neon glow", "مستقبل": "future", "خيال علمي": "sci-fi future",
           "خريطة": "map", "خرائط": "map", "صوت": "sound", "موسيقى": "music sound", "طعام": "food",
           "حلوى": "candy sweet", "لعبة": "toy", "ألعاب": "toy", "واجهة": "interface ui", "شاشة": "screen",
           "عربي": "arabic", "إسلامي": "islamic", "تراث": "heritage folk", "شعبي": "folk", "صحراء": "desert",
           "بحر": "sea ocean water", "ماء": "water", "سينما": "film cinema", "فيلم": "film", "تصوير": "photo",
           "علمي": "science", "مجهر": "microscope", "طبيعة": "nature", "زمن": "time", "حركة": "motion",
           "توليدي": "generative", "تجريدي": "abstract", "عمارة": "architecture", "معماري": "architecture",
           "زجاج": "glass", "معدن": "metal", "ذهب": "gold", "فضة": "silver", "رمل": "sand", "جليد": "ice",
           "دخان": "smoke", "بكسل": "pixel", "قديم": "vintage retro", "ريترو": "retro", "ألوان مائية": "watercolor",
           "حبر": "ink", "سبورة": "whiteboard chalkboard", "طباشير": "chalk", "بوب": "pop", "صلصال": "clay",
           "مانغا": "manga", "أنمي": "anime kawaii", "فضاء": "space cosmic", "نجوم": "star", "ليل": "night"}


def _norm(text):
    text = _DIACRITICS.sub("", text.casefold().translate(_AR_MAP))
    return re.sub(r"\bال(?=\w{3,})", "", text)


def _words(text):
    return [w for w in re.split(r"[^\w؀-ۿ]+", _norm(text)) if len(w) >= 2]


def resolve(lib, token):
    key = token.strip().casefold()
    if not key:
        raise ValueError("style must not be blank")
    for s in lib["styles"]:
        if key in (s["id"].casefold(), s["slug"], s["name"].casefold()) or token.strip() == s["name_ar"]:
            return s
    hits = find(lib, token, limit=2)
    if hits and (len(hits) == 1 or hits[0][0] > hits[1][0]):
        return hits[0][1]
    raise ValueError("unknown or ambiguous style: %s (try: find)" % token)


def find(lib, query, limit=10, group=None):
    q = query.strip()
    if not q or len(q) > 300:
        raise ValueError("query must be 1-300 characters")
    extra = " ".join(v for k, v in ALIASES.items() if _norm(k) in _norm(q))
    words = _words(q + " " + extra)
    gname = {g["id"]: g["name"] + " " + g["name_ar"] for g in lib["groups"]}
    ranked = []
    for s in lib["styles"]:
        if group and s["group"] != group:
            continue
        name = _norm(s["name"] + " " + s["name_ar"])
        hay = _norm(" ".join([s["id"], s["slug"], s["look"], s["logic"], s["motif"], gname[s["group"]],
                              s.get("summary_ar", "")]))
        score = sum(5 if w in name else 1 for w in words if w in name or w in hay)
        if _norm(q) == _norm(s["name"]) or q == s["name_ar"]:
            score += 50
        if score:
            ranked.append((score, s["id"], s))
    ranked.sort(key=lambda x: (-x[0], x[1]))
    return [(sc, s) for sc, _, s in ranked[:limit]]


# ------------------------------------------------------------------------- prompts

COLOR_NAMES = [("black", (10, 10, 10)), ("charcoal", (45, 45, 45)), ("grey", (128, 128, 128)), ("silver", (192, 192, 192)),
               ("white", (250, 250, 250)), ("cream", (245, 235, 215)), ("sand", (222, 196, 150)), ("ochre", (204, 153, 51)),
               ("gold", (212, 175, 55)), ("yellow", (255, 220, 0)), ("pale yellow", (255, 232, 120)), ("orange", (245, 130, 30)), ("terracotta", (200, 90, 60)),
               ("rust", (165, 75, 35)), ("brown", (110, 70, 40)), ("red", (210, 30, 40)), ("crimson", (150, 20, 40)),
               ("pink", (255, 140, 180)), ("magenta", (240, 0, 160)), ("plum", (110, 40, 90)), ("violet", (130, 60, 200)),
               ("indigo", (45, 40, 110)), ("navy", (15, 30, 70)), ("blue", (40, 100, 210)), ("sky blue", (140, 200, 240)),
               ("cyan", (0, 220, 240)), ("teal", (20, 130, 130)), ("mint", (170, 230, 200)), ("green", (50, 150, 70)),
               ("olive", (110, 120, 50)), ("lime", (150, 230, 40))]


def color_name(hexc):
    r, g, b = (int(hexc[i:i + 2], 16) for i in (1, 3, 5))
    return min(COLOR_NAMES, key=lambda n: (n[1][0] - r) ** 2 * 0.3 + (n[1][1] - g) ** 2 * 0.59 + (n[1][2] - b) ** 2 * 0.11)[0]


def recipe(s):
    if s["prompt"]:
        return s["prompt"]
    names = list(dict.fromkeys(color_name(c) for c in s["palette"]))
    return ("{subject}, rendered in the %s style: %s. Palette: %s. Motion if animated: %s. Keep the logic: %s."
            % (s["name"], s["look"], ", ".join(names), s["motion"], s["logic"]))


def prompt(s, subject, mix=None):
    subject = subject.strip()
    if not 1 <= len(subject) <= 300:
        raise ValueError("subject must have 1-300 characters")
    text = recipe(s).replace("{subject}", subject)
    if mix is not None:
        if mix["id"] == s["id"]:
            raise ValueError("mix needs a different style")
        text += (" Accent (about 30%%, never more than the base): borrow from %s its %s; palette accent %s."
                 % (mix["name"], mix["look"].split(",")[0], color_name(mix["palette"][1])))
    neg = s.get("negative") or "no copied artwork, logos or signatures; keep the medium consistent across the whole frame"
    return {"style": s["id"], "name": s["name"], "name_ar": s["name_ar"], "mix": mix["id"] if mix else None,
            "prompt": text, "negative": neg,
            "use_ar": "الصق البرومنت في مولّد صور أو فيديو، أو استعمل الوصف والمنطق كموجز فني لمشهد موشن أصلي."}


# ---------------------------------------------------------------- procedural swatches

def _f(v):
    s = ("%.1f" % v).rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


class Noise:
    def __init__(self, rng):
        self.v = [rng.random() for _ in range(256)]
        self.p = list(range(256))
        rng.shuffle(self.p)

    def _h(self, x, y):
        return self.v[self.p[(self.p[x & 255] + y) & 255]]

    def __call__(self, x, y):
        xi, yi = math.floor(x), math.floor(y)
        xf, yf = x - xi, y - yi
        u, v = xf * xf * (3 - 2 * xf), yf * yf * (3 - 2 * yf)
        a = self._h(xi, yi) + u * (self._h(xi + 1, yi) - self._h(xi, yi))
        b = self._h(xi, yi + 1) + u * (self._h(xi + 1, yi + 1) - self._h(xi, yi + 1))
        return a + v * (b - a)

    def fbm(self, x, y, octaves=3):
        t, amp, norm = 0.0, 1.0, 0.0
        for _ in range(octaves):
            t += amp * self(x, y)
            norm += amp
            x, y, amp = x * 2.03, y * 2.03, amp * 0.5
        return t / norm


def _poly(points, fill, extra=""):
    return '<polygon points="%s" fill="%s"%s/>' % (" ".join("%s,%s" % (_f(x), _f(y)) for x, y in points), fill, extra)


def _line(points, stroke, width, extra=""):
    return ('<polyline points="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round"%s/>'
            % (" ".join("%s,%s" % (_f(x), _f(y)) for x, y in points), stroke, _f(width), extra))


def _circle(x, y, r, fill, extra=""):
    return '<circle cx="%s" cy="%s" r="%s" fill="%s"%s/>' % (_f(x), _f(y), _f(r), fill, extra)


def _rect(x, y, w, h, fill, extra=""):
    return '<rect x="%s" y="%s" width="%s" height="%s" fill="%s"%s/>' % (_f(x), _f(y), _f(w), _f(h), fill, extra)


def _blob(cx, cy, r, rng, wob=0.3, n=9):
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        rr = r * (1 + wob * (rng.random() - 0.5))
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d = []
    for i in range(n):
        p0, p1 = pts[i], pts[(i + 1) % n]
        mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        if i == 0:
            pm = pts[-1]
            d.append("M%s,%s" % (_f((pm[0] + p0[0]) / 2), _f((pm[1] + p0[1]) / 2)))
        d.append("Q%s,%s %s,%s" % (_f(p0[0]), _f(p0[1]), _f(mx), _f(my)))
    return "".join(d) + "Z"


def m_zellige(r, P, N):
    out, cell = [], r.choice((56, 64, 72))
    for gy in range(-1, H // cell + 2):
        for gx in range(-1, W // cell + 2):
            cx, cy = gx * cell + (cell / 2 if gy % 2 else 0), gy * cell
            rad = cell * 0.48
            pts = []
            for i in range(16):
                a = math.pi * i / 8 + math.pi / 16
                rr = rad if i % 2 == 0 else rad * 0.62
                pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
            out.append(_poly(pts, P[1 + (gx + gy) % 2], ' stroke="%s" stroke-width="2"' % P[0]))
            out.append(_circle(cx, cy, rad * 0.28, P[3], ' stroke="%s" stroke-width="1.5"' % P[0]))
            out.append(_poly([(cx + cell / 2, cy - 6), (cx + cell / 2 + 6, cy), (cx + cell / 2, cy + 6), (cx + cell / 2 - 6, cy)], P[2]))
    return out


def m_lattice(r, P, N):
    out = [_rect(0, 0, W, H, P[1])]
    step = r.choice((26, 32, 40))
    shape = r.choice(("circle", "diamond", "star"))
    for y in range(0, H + step, step):
        for x in range(0, W + step, step):
            ox = step / 2 if (y // step) % 2 else 0
            cx, cy = x + ox, y
            s = step * 0.36
            if shape == "circle":
                out.append(_circle(cx, cy, s, P[0]))
            elif shape == "diamond":
                out.append(_poly([(cx, cy - s), (cx + s, cy), (cx, cy + s), (cx - s, cy)], P[0]))
            else:
                out.append(_poly([(cx + s * math.cos(a * math.pi / 4) * (1 if a % 2 == 0 else 0.45),
                                   cy + s * math.sin(a * math.pi / 4) * (1 if a % 2 == 0 else 0.45)) for a in range(8)], P[0]))
            out.append(_circle(cx, cy, s * 0.25, P[2]))
    out.append('<rect x="0" y="0" width="%d" height="%d" fill="%s" opacity="0.25"/>' % (W, H, P[3]))
    return out


def m_weave(r, P, N):
    out, y = [], 0
    while y < H:
        h = r.choice((10, 16, 24, 40))
        c = P[1 + r.randrange(4)]
        out.append(_rect(0, y, W, h, c))
        if h >= 24:
            k = r.randrange(3)
            for x in range(0, W, h):
                cc = P[1 + (P.index(c) % 4)] if k else P[0]
                if k == 0:
                    out.append(_poly([(x, y + h), (x + h / 2, y), (x + h, y + h)], cc))
                elif k == 1:
                    out.append(_poly([(x + h / 2, y + 3), (x + h - 3, y + h / 2), (x + h / 2, y + h - 3), (x + 3, y + h / 2)], P[0]))
                else:
                    out.append(_rect(x + h / 3, y + h / 3, h / 3, h / 3, P[0]))
        for x in range(0, W, 4):
            out.append(_rect(x, y, 1, h, "#000", ' opacity="0.06"'))
        y += h
    return out


GLYPHS = "ابجدهوزحطيكلمنسعفصقرشتثخذضظغKOSIFSTYLE"


def m_letters(r, P, N):
    out = []
    for i in range(r.choice((3, 4, 5))):
        g = r.choice(GLYPHS)
        size = r.uniform(110, 230)
        x, y = r.uniform(20, W - 80), r.uniform(150, H + 40)
        rot = r.choice((0, 0, -8, 8, -90))
        out.append('<text x="%s" y="%s" font-size="%s" font-weight="900" fill="%s" transform="rotate(%d %s %s)" '
                   'font-family="KLib, Cairo, DejaVu Sans, sans-serif" opacity="%s">%s</text>'
                   % (_f(x), _f(y), _f(size), P[1 + i % 4], rot, _f(x), _f(y), _f(r.uniform(0.75, 1)), html.escape(g)))
    for i in range(6):
        y = r.uniform(20, H - 20)
        out.append(_rect(r.uniform(0, W / 2), y, r.uniform(60, 200), 4, P[1 + i % 4], ' opacity="0.7"'))
    return out


def m_calligraphy(r, P, N):
    out = []
    for stroke in range(r.choice((2, 3))):
        a1, a2, f1, f2 = r.uniform(30, 90), r.uniform(10, 40), r.uniform(1.2, 2.6), r.uniform(2.5, 5)
        ph = r.uniform(0, 6)
        y0 = H * (0.35 + 0.2 * stroke)
        pts = [(x, y0 + a1 * math.sin(f1 * x / W * math.pi * 2 + ph) + a2 * math.sin(f2 * x / W * math.pi * 2))
               for x in range(30, W - 30, 6)]
        nib = r.choice((10, 14, 18))
        col = P[1 + stroke % 4]
        for k in range(-nib, nib + 1, 2):
            dx, dy = k * 0.7, -k * 0.7
            out.append(_line([(x + dx, y + dy) for x, y in pts], col, 2.2))
        for i in range(3):
            x, y = r.uniform(60, W - 60), r.uniform(40, H - 40)
            out.append('<rect x="%s" y="%s" width="12" height="12" fill="%s" transform="rotate(45 %s %s)"/>' % (_f(x), _f(y), P[2], _f(x), _f(y)))
    out.append(_rect(W * 0.18, H * 0.12, 9, H * 0.7, P[1]))
    return out


def m_arches(r, P, N):
    out, cx = [], W / 2
    for i in range(9):
        t = i / 9
        w, h = W * (1 - t * 0.9), H * (1.15 - t * 0.95)
        base = H
        top = base - h
        col = P[1 + i % 2] if r.random() < 0.8 else P[3]
        d = "M%s,%s L%s,%s A%s,%s 0 1,1 %s,%s L%s,%s Z" % (_f(cx - w / 2), _f(base), _f(cx - w / 2), _f(top + w / 2),
                                                             _f(w / 2), _f(w / 2), _f(cx + w / 2), _f(top + w / 2), _f(cx + w / 2), _f(base))
        out.append('<path d="%s" fill="%s"/>' % (d, col))
    out.append(_circle(cx, H * 0.86, 10, P[4]))
    return out


def _voronoi(rng, n, w, h):
    seeds = [(rng.uniform(0, w), rng.uniform(0, h)) for _ in range(n)]
    cells = []
    for i, (sx, sy) in enumerate(seeds):
        poly = [(0, 0), (w, 0), (w, h), (0, h)]
        for j, (tx, ty) in enumerate(seeds):
            if i == j:
                continue
            mx, my, nx, ny = (sx + tx) / 2, (sy + ty) / 2, tx - sx, ty - sy
            res = []
            for k in range(len(poly)):
                p, q = poly[k], poly[(k + 1) % len(poly)]
                dp = (p[0] - mx) * nx + (p[1] - my) * ny
                dq = (q[0] - mx) * nx + (q[1] - my) * ny
                if dp <= 0:
                    res.append(p)
                if (dp < 0) != (dq < 0):
                    t = dp / (dp - dq)
                    res.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
            poly = res
            if not poly:
                break
        cells.append(((sx, sy), poly))
    return cells


def m_cells(r, P, N):
    out = []
    for i, (seed, poly) in enumerate(_voronoi(r, r.choice((22, 34, 48)), W, H)):
        if len(poly) >= 3:
            out.append(_poly(poly, P[1 + r.randrange(4)], ' stroke="%s" stroke-width="%d" stroke-linejoin="round"'
                             % (P[0], r.choice((3, 5)))))
    return out


def _leaf(x, y, ang, ln, wd, fill):
    a = math.radians(ang)
    tx, ty = x + ln * math.cos(a), y + ln * math.sin(a)
    nx, ny = -math.sin(a) * wd, math.cos(a) * wd
    mx, my = (x + tx) / 2, (y + ty) / 2
    return '<path d="M%s,%s Q%s,%s %s,%s Q%s,%s %s,%s Z" fill="%s"/>' % (
        _f(x), _f(y), _f(mx + nx), _f(my + ny), _f(tx), _f(ty), _f(mx - nx), _f(my - ny), _f(x), _f(y), fill)


def _rosette(out, x, y, size, petals, c1, c2):
    for k in range(petals):
        out.append(_leaf(x, y, k * 360 / petals, size, size * 0.34, c1))
    out.append(_circle(x, y, size * 0.3, c2))


def m_botanic(r, P, N):
    out, cx = [], W / 2
    kind = r.randrange(4)
    if kind == 0:
        out.append(_line([(cx, H - 10), (cx, H * 0.3)], P[2], 5))
        for i in range(7):
            y = H - 40 - i * 30
            ln = 70 - i * 6
            out.append(_leaf(cx, y, -30 - i * 4, ln, 14, P[2]))
            out.append(_leaf(cx, y, -150 + i * 4, ln, 14, P[2]))
        _rosette(out, cx, H * 0.28, 52, r.choice((6, 8, 12)), P[1], P[3])
        for i in range(10):
            x, y = r.uniform(20, W - 20), r.uniform(20, H - 20)
            if abs(x - cx) > 110:
                _rosette(out, x, y, 14, 5, P[4] if i % 2 else P[1], P[3])
    elif kind == 1:
        step = r.choice((96, 120))
        for gy in range(0, H + step, step // 2):
            for gx in range(0, W + step, step):
                x = gx + (step / 2 if (gy // (step // 2)) % 2 else 0)
                vine = [(x - step / 2 + t * step / 20, gy + 18 * math.sin(t / 20 * 2 * math.pi)) for t in range(21)]
                out.append(_line(vine, P[2], 3))
                out.append(_leaf(x - step / 4, gy, -60, 30, 9, P[2]))
                out.append(_leaf(x + step / 4, gy, 120, 30, 9, P[2]))
                _rosette(out, x, gy, 22, r.choice((5, 6, 8)), P[1 + (gx // step) % 2 * 2], P[4])
    elif kind == 2:
        R = r.uniform(95, 120)
        for i in range(36):
            a = 2 * math.pi * i / 36
            x, y = cx + R * math.cos(a), H / 2 + R * math.sin(a)
            out.append(_leaf(x, y, math.degrees(a) + 90 + (30 if i % 2 else -30), 34, 10, P[2 + i % 2]))
        _rosette(out, cx, H / 2, 46, 10, P[1], P[4])
        for i in range(6):
            a = 2 * math.pi * i / 6 + 0.3
            _rosette(out, cx + R * math.cos(a), H / 2 + R * math.sin(a), 16, 6, P[1], P[3])
    else:
        for i in range(r.choice((7, 9, 11))):
            x, y = r.uniform(0, W), r.uniform(H * 0.2, H + 40)
            ang = r.uniform(-160, -20)
            out.append(_leaf(x, y, ang, r.uniform(120, 220), r.uniform(28, 46), P[1 + i % 4]))
            a = math.radians(ang)
            out.append(_line([(x, y), (x + 150 * math.cos(a), y + 150 * math.sin(a))], P[0], 1.5, ' opacity="0.5"'))
    return out


def m_guilloche(r, P, N):
    out, cx, cy = [], W / 2, H / 2
    for layer in range(r.choice((3, 4))):
        R, rr, d = r.uniform(110, 150), r.uniform(18, 52), r.uniform(30, 90)
        pts = []
        for i in range(900):
            t = i / 900 * 2 * math.pi * 12
            x = (R - rr) * math.cos(t) + d * math.cos((R - rr) / rr * t)
            y = (R - rr) * math.sin(t) - d * math.sin((R - rr) / rr * t)
            pts.append((cx + x * 1.25, cy + y * 0.95))
        out.append(_line(pts, P[1 + layer % 4], 1.6, ' opacity="0.9"'))
    return out


def m_bricks(r, P, N):
    out, h = [], r.choice((22, 28, 34))
    for row, y in enumerate(range(0, H, h)):
        off = (row % 2) * 30
        col = P[1] if row % 2 else P[3]
        for x in range(-60 + off, W, 60):
            out.append(_rect(x + 2, y + 2, 56, h - 4, col if r.random() > 0.15 else P[2], ' rx="2"'))
    cx = W / 2
    out.append('<path d="M%s,%d L%s,%s A90,90 0 0,1 %s,%s L%s,%d Z" fill="%s"/>' % (
        _f(cx - 90), H, _f(cx - 90), _f(H * 0.55), _f(cx + 90), _f(H * 0.55), _f(cx + 90), H, P[4]))
    return out


def _figure(cx, base, s, fill, pose):
    head = _circle(cx, base - 150 * s, 18 * s, fill)
    body = _poly([(cx - 22 * s, base - 128 * s), (cx + 22 * s, base - 128 * s), (cx + 34 * s, base - 30 * s), (cx - 34 * s, base - 30 * s)], fill)
    la = '<path d="M%s,%s Q%s,%s %s,%s" stroke="%s" stroke-width="%s" fill="none" stroke-linecap="round"/>' % (
        _f(cx - 20 * s), _f(base - 120 * s), _f(cx - 60 * s), _f(base - (150 if pose else 90) * s),
        _f(cx - 50 * s), _f(base - (190 if pose else 60) * s), fill, _f(9 * s))
    ra = '<path d="M%s,%s Q%s,%s %s,%s" stroke="%s" stroke-width="%s" fill="none" stroke-linecap="round"/>' % (
        _f(cx + 20 * s), _f(base - 120 * s), _f(cx + 55 * s), _f(base - 100 * s), _f(cx + 62 * s), _f(base - 70 * s), fill, _f(9 * s))
    legs = _line([(cx - 14 * s, base - 32 * s), (cx - 20 * s, base)], fill, 10 * s) + _line([(cx + 14 * s, base - 32 * s), (cx + 24 * s, base)], fill, 10 * s)
    return head + body + la + ra + legs


def m_figure(r, P, N):
    if r.random() < 0.35:
        cx, hy = W * r.uniform(0.42, 0.58), H * 0.4
        face = r.choice((-1, 1))
        out = [_circle(cx - face * 90, H * 0.32, 80, P[3], ' opacity="0.7"')]
        out.append('<path d="M%s,%d C%s,%s %s,%s %s,%s L%s,%s C%s,%s %s,%s %s,%d Z" fill="%s"/>' % (
            _f(cx - 150), H, _f(cx - 140), _f(H * 0.78), _f(cx - 70), _f(H * 0.74), _f(cx - 26), _f(H * 0.7),
            _f(cx + 26), _f(H * 0.7), _f(cx + 70), _f(H * 0.74), _f(cx + 140), _f(H * 0.78), _f(cx + 150), H, P[2]))
        out.append(_rect(cx - 20, hy + 40, 40, H * 0.32, P[1]))
        out.append('<ellipse cx="%s" cy="%s" rx="46" ry="58" fill="%s"/>' % (_f(cx), _f(hy), P[1]))
        out.append(_poly([(cx + face * 40, hy - 6), (cx + face * 58, hy + 14), (cx + face * 40, hy + 18)], P[1]))
        out.append('<path d="M%s,%s Q%s,%s %s,%s Z" fill="%s"/>' % (_f(cx - 46), _f(hy - 10), _f(cx), _f(hy - 100), _f(cx + 46), _f(hy - 10), P[4]))
        out.append('<ellipse cx="%s" cy="%s" rx="9" ry="4" fill="%s"/>' % (_f(cx + face * 22), _f(hy + 2), P[0]))
        return out
    out = [_circle(W * r.uniform(0.3, 0.7), H * 0.42, r.uniform(80, 120), P[3], ' opacity="0.85"'),
           _rect(0, H * 0.84, W, H * 0.16, P[2])]
    n = r.choice((1, 1, 3, 5))
    for i in range(n):
        s = 1.2 if n == 1 else 0.85
        cx = W / 2 if n == 1 else W * (0.15 + 0.7 * i / (n - 1))
        out.append('<g opacity="%s">%s</g>' % (_f(1 if n == 1 else 0.35 + 0.65 * i / (n - 1)), _figure(cx, H * 0.86, s, P[1], i % 2)))
    return out


def m_ridges(r, P, N):
    out = [_circle(W * r.uniform(0.2, 0.8), H * 0.3, r.uniform(28, 48), P[4])]
    layers = r.choice((4, 5, 6))
    for k in range(layers):
        base = H * (0.35 + 0.65 * (k + 1) / (layers + 1))
        pts = [(0, H)]
        for x in range(0, W + 8, 8):
            pts.append((x, base - 70 * N.fbm(x / 140 + k * 3.1, k * 1.7) + 20))
        pts.append((W, H))
        out.append(_poly(pts, P[1 + k % 4] if k < layers - 1 else P[1]))
    return out


def m_glowfog(r, P, N):
    out = []
    for i in range(r.choice((5, 7, 9))):
        x, y, rad = r.uniform(30, W - 30), r.uniform(30, H - 30), r.uniform(30, 110)
        out.append('<circle cx="%s" cy="%s" r="%s" fill="url(#rg%d)"/>' % (_f(x), _f(y), _f(rad), 1 + i % 4))
    for i in range(40):
        out.append(_circle(r.uniform(0, W), r.uniform(0, H), r.uniform(0.6, 2.4), P[1 + i % 4], ' opacity="0.9"'))
    out.append('<rect x="0" y="%s" width="%d" height="%s" fill="url(#lgfog)"/>' % (_f(H * 0.55), W, _f(H * 0.45)))
    return out


def m_spiral(r, P, N):
    out, cx, cy = [], W / 2 + r.uniform(-40, 40), H / 2
    turns, arms = r.uniform(3, 6), r.choice((1, 2, 3))
    for a in range(arms):
        pts = []
        for i in range(500):
            t = i / 500
            ang = t * turns * 2 * math.pi + a * 2 * math.pi / arms
            rad = 6 + t * 190
            pts.append((cx + rad * math.cos(ang), cy + rad * 0.85 * math.sin(ang)))
        for seg in range(4):
            out.append(_line(pts[seg * 125:(seg + 1) * 125 + 1], P[1 + (seg + a) % 4], 9 - seg))
    out.append(_circle(cx, cy, 10, P[1]))
    return out


def m_triangles(r, P, N):
    out, h = [], r.choice((32, 40, 48))
    for row, y in enumerate(range(0, H + h, h)):
        for i, x in enumerate(range(-h, W + h, h)):
            up = (i + row) % 2 == 0
            pts = [(x, y + h), (x + h / 2, y), (x + h, y + h)] if up else [(x, y), (x + h, y), (x + h / 2, y + h)]
            out.append(_poly(pts, P[1 + (i // 2 + row) % 4] if r.random() > 0.3 else P[0]))
    cx, cy = W / 2, H / 2
    for k in range(4, 0, -1):
        s = 30 * k
        out.append(_poly([(cx, cy - s), (cx + s, cy), (cx, cy + s), (cx - s, cy)], P[k % 4 + 1] if k % 2 else P[0]))
    return out


def m_waves(r, P, N):
    out, n = [], r.choice((6, 9, 12))
    for k in range(n):
        base = H * (k + 1) / (n + 1)
        amp, fr, ph = r.uniform(8, 28), r.uniform(1.5, 4), r.uniform(0, 6)
        pts = [(x, base + amp * math.sin(fr * x / W * 2 * math.pi + ph + k * 0.4)) for x in range(0, W + 6, 6)]
        if k % 2 == 0:
            out.append(_poly(pts + [(W, H), (0, H)], P[1 + k % 4], ' opacity="0.55"'))
        out.append(_line(pts, P[1 + (k + 1) % 4], 3))
    return out


def m_sunburst(r, P, N):
    out, cx, cy = [], W / 2, H * r.choice((0.5, 0.62, 1.0))
    n = r.choice((16, 24, 32))
    for i in range(n):
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 0.5) / n
        out.append(_poly([(cx, cy), (cx + 700 * math.cos(a0), cy + 700 * math.sin(a0)), (cx + 700 * math.cos(a1), cy + 700 * math.sin(a1))],
                         P[1 + i % 2]))
    for k, rad in enumerate((90, 66, 42)):
        out.append(_circle(cx, cy, rad, P[2 + k % 3], ' stroke="%s" stroke-width="3"' % P[0]))
    return out


def m_stitch(r, P, N):
    out, s = [], r.choice((10, 12, 14))
    cols, rows = W // s, H // s
    kind = r.randrange(3)
    for j in range(rows):
        for i in range(cols):
            dx, dy = abs(i - cols / 2), abs(j - rows / 2)
            if kind == 0:
                on = (int(dx + dy) % 6) < 2
            elif kind == 1:
                on = (i % 8 < 4) ^ (j % 8 < 4) and (i + j) % 3 != 0
            else:
                on = (max(dx, dy) % 5) < 1.5 or dx == dy
            if not on:
                continue
            x, y = i * s, j * s
            col = P[1 + (int(dx + dy) // 6) % 4]
            out.append('<path d="M%d,%d L%d,%d M%d,%d L%d,%d" stroke="%s" stroke-width="2.4" stroke-linecap="round"/>'
                       % (x + 2, y + 2, x + s - 2, y + s - 2, x + s - 2, y + 2, x + 2, y + s - 2, col))
    return out


def m_stripes(r, P, N):
    out, ang = [], r.choice((0, 0, 20, -20, 90))
    x = -100
    g = []
    while x < W + 120:
        w = r.choice((8, 14, 24, 40))
        g.append(_rect(x, -200, w, H + 400, P[1 + r.randrange(4)], ' opacity="%s"' % _f(r.uniform(0.6, 1))))
        x += w + r.choice((0, 4, 10))
    out.append('<g transform="rotate(%d %d %d)">%s</g>' % (ang, W // 2, H // 2, "".join(g)))
    return out


def m_paperlayers(r, P, N):
    out, n = [], r.choice((4, 5, 6))
    for k in range(n):
        base = H * (0.2 + 0.8 * k / n)
        pts = [(0, H)] + [(x, base + 26 * math.sin(x / r.uniform(40, 90) + k) + 18 * N(x / 90, k)) for x in range(0, W + 10, 10)] + [(W, H)]
        out.append(_poly(pts, P[1 + k % 4], ' filter="url(#drop)"'))
    out.append(_circle(W * 0.75, H * 0.2, 30, P[4], ' filter="url(#drop)"'))
    return out


def m_dots(r, P, N):
    out, s = [], r.choice((12, 16, 20))
    for y in range(s // 2, H, s):
        for x in range(s // 2, W, s):
            v = N.fbm(x / 120, y / 120)
            rad = s * 0.5 * max(0.12, min(1, (v - 0.25) * 1.8))
            out.append(_circle(x + r.uniform(-2, 2), y + r.uniform(-2, 2), rad, P[1 + int(v * 7) % 4]))
    return out


def m_flow(r, P, N):
    out = []
    for i in range(r.choice((70, 110, 150))):
        x, y = r.uniform(0, W), r.uniform(0, H)
        pts = [(x, y)]
        for _ in range(40):
            a = N.fbm(x / 160, y / 160) * math.pi * 4
            x, y = x + 5 * math.cos(a), y + 5 * math.sin(a)
            pts.append((x, y))
        out.append(_line(pts, P[1 + i % 4], r.choice((1.2, 2, 3)), ' opacity="0.85"'))
    return out


def m_blobs(r, P, N):
    out = []
    for i in range(r.choice((5, 7, 9))):
        cx, cy, rad = r.uniform(40, W - 40), r.uniform(40, H - 40), r.uniform(26, 90)
        out.append('<path d="%s" fill="url(#rg%d)"/>' % (_blob(cx, cy, rad, r, 0.4), 1 + i % 4))
        out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#fff" opacity="0.35"/>' % (
            _f(cx - rad * 0.3), _f(cy - rad * 0.35), _f(rad * 0.25), _f(rad * 0.12)))
    return out


def m_radial(r, P, N):
    out, cx, cy = [], W / 2, H / 2
    kind = r.randrange(4)
    if kind == 0:
        rings = r.choice((8, 12, 16))
        for k in range(rings, 0, -1):
            out.append(_circle(cx, cy, k * 190 / rings, P[1 + k % 4]))
        petals = r.choice((8, 12, 16))
        for i in range(petals):
            out.append(_leaf(cx, cy, i * 360 / petals, 120, 16, P[0] + "aa"))
        out.append(_circle(cx, cy, 18, P[0]))
    elif kind == 1:
        for c in range(r.choice((2, 3))):
            x, y = r.uniform(80, W - 80), r.uniform(60, H - 60)
            for k in range(1, 14):
                out.append(_circle(x, y, k * 16, "none", ' stroke="%s" stroke-width="%s" opacity="%s"'
                                   % (P[1 + c % 4], _f(3.5 - k * 0.2), _f(1 - k / 16))))
    elif kind == 2:
        n = r.choice((10, 14, 20))
        for ring in range(4):
            r0, r1 = 40 + ring * 34, 70 + ring * 34
            for i in range(n):
                a0, a1 = 2 * math.pi * i / n + ring * 0.2, 2 * math.pi * (i + 0.8) / n + ring * 0.2
                out.append(_poly([(cx + r0 * math.cos(a0), cy + r0 * math.sin(a0)), (cx + r1 * math.cos(a0), cy + r1 * math.sin(a0)),
                                  (cx + r1 * math.cos(a1), cy + r1 * math.sin(a1)), (cx + r0 * math.cos(a1), cy + r0 * math.sin(a1))],
                                 P[1 + (i + ring) % 4]))
        out.append(_circle(cx, cy, 30, P[1]))
    else:
        for k in range(6, 0, -1):
            petals = 6 + k * 2
            for i in range(petals):
                out.append(_leaf(cx, cy, i * 360 / petals + k * 9, 22 * k + 10, 7 + k * 2, P[1 + k % 4]))
        out.append(_circle(cx, cy, 14, P[4]))
    return out


def m_shards(r, P, N):
    out, pts = [], [(r.uniform(0, W), r.uniform(0, H)) for _ in range(26)] + [(0, 0), (W, 0), (W, H), (0, H)]
    cx, cy = W * r.uniform(0.3, 0.7), H * r.uniform(0.3, 0.7)
    pts.sort(key=lambda p: math.atan2(p[1] - cy, p[0] - cx))
    for i in range(len(pts)):
        p, q = pts[i], pts[(i + 1) % len(pts)]
        out.append(_poly([(cx, cy), p, q], P[1 + i % 4], ' stroke="%s" stroke-width="1" opacity="%s"' % (P[0], _f(0.55 + 0.45 * ((i * 7) % 5) / 4))))
    return out


def m_contours(r, P, N):
    out = []
    centers = [(r.uniform(60, W - 60), r.uniform(50, H - 50)) for _ in range(r.choice((1, 2, 3)))]
    for cx, cy in centers:
        for k in range(1, 16):
            rad = k * 13
            pts = []
            for i in range(73):
                a = 2 * math.pi * i / 72
                rr = rad * (1 + 0.35 * (N.fbm(math.cos(a) + cx / 50, math.sin(a) + k * 0.15) - 0.5))
                pts.append((cx + rr * math.cos(a) * 1.3, cy + rr * math.sin(a)))
            out.append(_line(pts, P[1 + k % 4], 2.2 if k % 5 == 0 else 1.1))
    return out


def m_glitch(r, P, N):
    out = []
    base = _blob(W / 2, H / 2, 110, r, 0.35)
    for k, c in enumerate((P[1], P[2], P[3])):
        out.append('<path d="%s" fill="%s" opacity="0.7" transform="translate(%d 0)"/>' % (base, c, (k - 1) * 8))
    y = 0
    while y < H:
        h = r.choice((3, 6, 10, 18))
        if r.random() < 0.35:
            out.append(_rect(r.uniform(-60, 60), y, W, h, P[1 + r.randrange(4)], ' opacity="0.6"'))
        y += h + r.choice((2, 8, 20))
    for _ in range(18):
        out.append(_rect(r.uniform(0, W), r.uniform(0, H), r.uniform(8, 60), r.uniform(3, 10), P[4]))
    return out


def m_bars(r, P, N):
    out, n = [], r.choice((16, 24, 32))
    bw = W / n
    for i in range(n):
        h = H * (0.15 + 0.7 * N.fbm(i / 6, 0.5))
        out.append(_rect(i * bw + 2, H - h, bw - 4, h, P[1 + i * 4 // n], ' rx="2"'))
        out.append(_rect(i * bw + 2, H - h - 8, bw - 4, 4, P[4]))
    out.append(_line([(0, H * 0.3)] + [(i * bw + bw / 2, H * (0.55 - 0.3 * N(i / 4, 2))) for i in range(n)], P[4], 2))
    return out


def m_routes(r, P, N):
    out, nodes = [], []
    for k in range(r.choice((3, 4, 5))):
        x, y = r.choice((20, W - 20)), r.uniform(30, H - 30)
        pts = [(x, y)]
        for _ in range(5):
            d = r.choice((0, 45, -45, 90, -90))
            ln = r.uniform(50, 120)
            dx = ln * math.cos(math.radians(d)) * (1 if x < W / 2 else -1)
            x, y = min(W - 10, max(10, x + dx)), min(H - 10, max(10, y + ln * math.sin(math.radians(d)) * 0.6))
            pts.append((x, y))
        out.append(_line(pts, P[1 + k % 4], 8))
        nodes += pts[1:]
    for x, y in nodes:
        out.append(_circle(x, y, 6, P[0], ' stroke="%s" stroke-width="3"' % P[1]))
    return out


def m_ui(r, P, N):
    out, gap = [], 12
    cols = r.choice((2, 3))
    cw = (W - gap * (cols + 1)) / cols
    y = gap
    while y < H - 40:
        x = gap
        rh = r.choice((70, 90, 120))
        for c in range(cols):
            out.append(_rect(x, y, cw, rh, P[1] if (c + int(y)) % 3 else P[2], ' rx="14" filter="url(#drop)"'))
            out.append(_rect(x + 14, y + 16, cw * 0.5, 8, P[3], ' rx="4"'))
            out.append(_rect(x + 14, y + 32, cw * 0.3, 6, P[4], ' rx="3" opacity="0.7"'))
            out.append(_circle(x + cw - 26, y + rh - 26, 12, P[4]))
            x += cw + gap
        y += rh + gap
    return out


def m_iso(r, P, N):
    out, s = [], r.choice((28, 34, 40))
    cells = []
    for gx in range(6):
        for gy in range(6):
            h = r.choice((0, 1, 1, 2, 3))
            for z in range(h):
                cells.append((gx, gy, z))
    cells.sort(key=lambda c: (c[0] + c[1], c[2]))
    ox, oy = W / 2, 70
    for gx, gy, z in cells:
        x = ox + (gx - gy) * s * 0.866
        y = oy + (gx + gy) * s * 0.5 - z * s
        top = [(x, y), (x + s * 0.866, y + s * 0.5), (x, y + s), (x - s * 0.866, y + s * 0.5)]
        left = [(x - s * 0.866, y + s * 0.5), (x, y + s), (x, y + 2 * s), (x - s * 0.866, y + 1.5 * s)]
        right = [(x + s * 0.866, y + s * 0.5), (x, y + s), (x, y + 2 * s), (x + s * 0.866, y + 1.5 * s)]
        c = 1 + (gx * 3 + gy) % 3
        out += [_poly(top, P[c]), _poly(left, P[4]), _poly(right, P[c], ' opacity="0.65"')]
    return out


def m_tree(r, P, N):
    out = []

    def branch(x, y, ang, ln, depth):
        if depth == 0 or ln < 4:
            out.append(_circle(x, y, 3.5, P[1 + depth % 2 + 2]))
            return
        x2, y2 = x + ln * math.cos(ang), y + ln * math.sin(ang)
        out.append(_line([(x, y), (x2, y2)], P[1] if depth > 3 else P[2], max(1, depth * 1.3)))
        spread = r.uniform(0.3, 0.6)
        branch(x2, y2, ang - spread, ln * r.uniform(0.68, 0.8), depth - 1)
        branch(x2, y2, ang + spread, ln * r.uniform(0.68, 0.8), depth - 1)
    for k in range(r.choice((1, 2))):
        branch(W * (0.5 if k == 0 else r.choice((0.2, 0.8))), H, -math.pi / 2 + r.uniform(-0.1, 0.1), r.uniform(60, 80), 8)
    return out


def m_skyline(r, P, N):
    out, x = [_circle(W * 0.78, H * 0.25, 34, P[4])], 0
    for layer in range(2):
        x = -10
        while x < W:
            w, h = r.uniform(26, 64), r.uniform(60, 220) * (0.7 if layer == 0 else 1)
            col = P[2] if layer == 0 else P[1]
            out.append(_rect(x, H - h, w, h, col, ' opacity="%s"' % ("0.6" if layer == 0 else "1")))
            if layer == 1:
                for wy in range(int(H - h) + 10, H - 10, 14):
                    for wx in range(int(x) + 5, int(x + w) - 6, 10):
                        if r.random() < 0.45:
                            out.append(_rect(wx, wy, 5, 7, P[3]))
            x += w + r.uniform(0, 6)
    return out


def _wob(r, pts, amt=1.6):
    return [(x + r.uniform(-amt, amt), y + r.uniform(-amt, amt)) for x, y in pts]


def m_hatch(r, P, N):
    out = []
    kind = r.randrange(3)
    if kind == 0:
        cx, cy, R = W * r.uniform(0.38, 0.62), H * 0.48, r.uniform(85, 110)
        for k in range(2):
            out.append(_line(_wob(r, [(cx + R * math.cos(t / 40 * 2 * math.pi), cy + R * math.sin(t / 40 * 2 * math.pi)) for t in range(42)]), P[1], 2.2))
        for i in range(-int(R), int(R), 7):
            x0 = cx + i
            span = math.sqrt(max(0, R * R - i * i))
            if i > -R * 0.2:
                out.append(_line(_wob(r, [(x0 - span * 0.3, cy + span * 0.1), (x0 + span * 0.3, cy + span)], 0.8), P[2], 1.2))
            if i > R * 0.35:
                out.append(_line(_wob(r, [(x0 + span * 0.3, cy - span * 0.4), (x0 - span * 0.2, cy + span * 0.9)], 0.8), P[2], 1))
        out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="14" fill="%s" opacity="0.35"/>' % (_f(cx + 20), _f(cy + R + 6), _f(R), P[2]))
    elif kind == 1:
        boxes = [(40, 70), (190, 40), (190, 190), (340, 110)]
        for i, (x, y) in enumerate(boxes):
            pts = [(x, y), (x + 100, y), (x + 100, y + 60), (x, y + 60), (x, y)]
            out.append(_line(_wob(r, pts), P[1 + i % 2], 2.6))
            out.append(_line(_wob(r, [(x + 14, y + 24), (x + 80, y + 24)]), P[3], 3))
            out.append(_line(_wob(r, [(x + 14, y + 40), (x + 60, y + 40)]), P[3], 3))
        for (x1, y1), (x2, y2) in ((boxes[0], boxes[1]), (boxes[0], boxes[2]), (boxes[1], boxes[3]), (boxes[2], boxes[3])):
            sx, sy, ex, ey = x1 + 100, y1 + 30, x2, y2 + 30
            out.append(_line(_wob(r, [(sx, sy), ((sx + ex) / 2, (sy + ey) / 2 - 10), (ex - 4, ey)]), P[4], 2.4))
            out.append(_poly([(ex, ey), (ex - 12, ey - 6), (ex - 12, ey + 6)], P[4]))
    else:
        for k in range(4):
            base = H * (0.35 + 0.17 * k)
            pts = [(x, base - 50 * N.fbm(x / 120 + k, k)) for x in range(0, W + 10, 10)]
            out.append(_line(_wob(r, pts, 1), P[1], 2))
            for x in range(0, W, 6):
                y = base - 50 * N.fbm(x / 120 + k, k)
                out.append(_line([(x, y + 3), (x - 8, y + 18 + 10 * k)], P[2 + k % 3], 0.9, ' opacity="0.7"'))
        out.append(_circle(W * 0.8, H * 0.18, 22, "none", ' stroke="%s" stroke-width="2"' % P[3]))
    return out


def m_orbits(r, P, N):
    out, cx, cy = [], W / 2, H / 2
    for k in range(r.choice((4, 5, 6))):
        rx, ry, rot = 40 + k * 32, 16 + k * 14, r.uniform(-30, 30)
        out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="%s" stroke-width="1.6" transform="rotate(%s %s %s)"/>'
                   % (_f(cx), _f(cy), _f(rx), _f(ry), P[1 + k % 4], _f(rot), _f(cx), _f(cy)))
        a = r.uniform(0, 2 * math.pi)
        px, py = rx * math.cos(a), ry * math.sin(a)
        t = math.radians(rot)
        out.append(_circle(cx + px * math.cos(t) - py * math.sin(t), cy + px * math.sin(t) + py * math.cos(t), r.uniform(4, 10), P[1 + (k + 1) % 4]))
    out.append(_circle(cx, cy, 22, "url(#rg1)"))
    return out


def m_wiregrid(r, P, N):
    out, hy = [], H * r.choice((0.42, 0.5))
    out.append(_circle(W / 2, hy, 70, "url(#lgsun)"))
    for i in range(-14, 15):
        out.append(_line([(W / 2 + i * 8, hy), (W / 2 + i * 70, H)], P[1], 1.4))
    y, step = hy, 4
    while y < H:
        out.append(_line([(0, y), (W, y)], P[1], 1.4))
        step *= 1.25
        y += step
    return out


def m_squares(r, P, N):
    out = []
    if r.random() < 0.5:
        cx, cy = W / 2, H / 2 + 10
        for k in range(4):
            s = 280 - k * 62
            out.append(_rect(cx - s / 2, cy - s / 2 + k * 8, s, s, P[1 + k % 4]))
    else:
        def split(x, y, w, h, d):
            if d == 0 or w < 60 or h < 50:
                out.append(_rect(x, y, w, h, P[r.choice((0, 0, 1, 2, 3, 4))], ' stroke="%s" stroke-width="6"' % P[4]))
                return
            if w > h:
                c = r.uniform(0.3, 0.7) * w
                split(x, y, c, h, d - 1)
                split(x + c, y, w - c, h, d - 1)
            else:
                c = r.uniform(0.3, 0.7) * h
                split(x, y, w, c, d - 1)
                split(x, y + c, w, h - c, d - 1)
        split(0, 0, W, H, 4)
    return out


def m_splatter(r, P, N):
    out = []
    for i in range(r.choice((4, 6))):
        cx, cy, rad = r.uniform(40, W - 40), r.uniform(40, H - 40), r.uniform(26, 60)
        col = P[1 + i % 4]
        out.append('<path d="%s" fill="%s"/>' % (_blob(cx, cy, rad, r, 0.8, 12), col))
        for _ in range(14):
            a, d = r.uniform(0, 2 * math.pi), rad * r.uniform(1.1, 2.4)
            out.append(_circle(cx + d * math.cos(a), cy + d * math.sin(a), r.uniform(1.5, 7), col))
    return out


def m_pixels(r, P, N):
    out, s = [], r.choice((16, 20))
    cols, rows = W // s, H // s
    for j in range(rows):
        for i in range(cols):
            v = N.fbm(i / 7, j / 7)
            out.append(_rect(i * s, j * s, s, s, P[min(4, int(v * 5))]))
    sx, sy = cols // 2 - 4, rows // 2 - 4
    for j in range(8):
        for i in range(4):
            if r.random() < 0.55:
                for ii in (i, 7 - i):
                    out.append(_rect((sx + ii) * s, (sy + j) * s, s, s, P[1]))
    return out


def m_washes(r, P, N):
    out = []
    for i in range(r.choice((7, 10, 13))):
        cx, cy, rad = r.uniform(20, W - 20), r.uniform(20, H - 20), r.uniform(40, 120)
        out.append('<path d="%s" fill="%s" fill-opacity="0.35" stroke="%s" stroke-opacity="0.45" stroke-width="2" filter="url(#soft)"/>'
                   % (_blob(cx, cy, rad, r, 0.6, 11), P[1 + i % 4], P[1 + i % 4]))
    return out


def m_caustics(r, P, N):
    out = []
    for seed, poly in _voronoi(r, 40, W, H):
        if len(poly) >= 3:
            out.append(_poly(poly, "none", ' stroke="%s" stroke-width="%s" stroke-linejoin="round" opacity="0.9"' % (P[2], _f(r.uniform(1.5, 4)))))
    return ['<g filter="url(#soft)">%s</g>' % "".join(out)] + out


def m_stars(r, P, N):
    out = []
    for i in range(160):
        out.append(_circle(r.uniform(0, W), r.uniform(0, H), r.choice((0.6, 0.9, 1.3, 2)), P[1 + i % 4] if i % 7 == 0 else "#ffffff",
                           ' opacity="%s"' % _f(r.uniform(0.4, 1))))
    px, py, pr = W * r.uniform(0.3, 0.7), H * r.uniform(0.35, 0.6), r.uniform(46, 70)
    out.append(_circle(px, py, pr, "url(#rg2)"))
    out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="%s" stroke-width="5" transform="rotate(-18 %s %s)"/>'
               % (_f(px), _f(py), _f(pr * 1.8), _f(pr * 0.45), P[3], _f(px), _f(py)))
    out.append(_circle(px + pr * 2.4, py - pr, pr * 0.25, P[4]))
    return out


def m_drips(r, P, N):
    out = []
    for i in range(r.choice((3, 4))):
        x0, w = W * i / 4 + r.uniform(-10, 10), W / 4 + 10
        col = P[1 + i % 4]
        out.append(_rect(x0, 0, w, H * 0.3, col))
        for _ in range(4):
            dx, ln, dw = r.uniform(4, w - 16), r.uniform(30, 190), r.uniform(8, 18)
            out.append('<path d="M%s,%s L%s,%s A%s,%s 0 0,0 %s,%s L%s,%s Z" fill="%s"/>' % (
                _f(x0 + dx), _f(H * 0.29), _f(x0 + dx), _f(H * 0.29 + ln), _f(dw / 2), _f(dw / 2), _f(x0 + dx + dw),
                _f(H * 0.29 + ln), _f(x0 + dx + dw), _f(H * 0.29), col))
    return out


def m_halftone(r, P, N):
    out, s = [], r.choice((10, 12))
    cx, cy = W * r.uniform(0.35, 0.65), H * 0.5
    for y in range(0, H + s, s):
        for x in range(0, W + s, s):
            ox = s / 2 if (y // s) % 2 else 0
            d = math.hypot(x + ox - cx, y - cy)
            rad = s * 0.55 * max(0.08, 1 - d / 240)
            out.append(_circle(x + ox, y, rad, P[1] if d < 150 else P[2]))
    out.append(_rect(0, H * 0.72, W, 12, P[3]))
    return out


MOTIFS = {k[2:]: v for k, v in globals().items() if k.startswith("m_") and callable(v)}


def _defs(P, texture, seed):
    stops = "".join('<radialGradient id="rg%d"><stop offset="0" stop-color="%s" stop-opacity="1"/>'
                    '<stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>' % (i, P[i], P[i]) for i in range(1, 5))
    d = [stops,
         '<linearGradient id="lgfog" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s" stop-opacity="0"/>'
         '<stop offset="1" stop-color="%s" stop-opacity="0.55"/></linearGradient>' % (P[2], P[2]),
         '<linearGradient id="lgsun" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s"/>'
         '<stop offset="1" stop-color="%s"/></linearGradient>' % (P[3], P[2]),
         '<filter id="drop" x="-10%%" y="-10%%" width="120%%" height="130%%"><feDropShadow dx="0" dy="4" stdDeviation="4" flood-opacity="0.35"/></filter>',
         '<filter id="soft"><feGaussianBlur stdDeviation="3"/></filter>',
         '<filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="5" result="b"/>'
         '<feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>',
         '<filter id="noise"><feTurbulence type="fractalNoise" baseFrequency="%s" numOctaves="2" seed="%d"/>'
         '<feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 %s 0"/></filter>'
         % ("0.035" if texture == "paper" else "0.9", seed % 997, "0.55" if texture == "paper" else "0.35"),
         '<pattern id="pcanvas" width="6" height="6" patternUnits="userSpaceOnUse"><path d="M0,3 H6 M3,0 V6" stroke="#000" stroke-opacity="0.08"/></pattern>',
         '<pattern id="pscan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1.6" fill="#000" opacity="0.28"/></pattern>',
         '<pattern id="phalf" width="7" height="7" patternUnits="userSpaceOnUse"><circle cx="3.5" cy="3.5" r="1.4" fill="#000" opacity="0.18"/></pattern>',
         '<radialGradient id="vig"><stop offset="0.55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.6"/></radialGradient>']
    return "<defs>%s</defs>" % "".join(d)


def swatch_svg(s):
    seed = int(hashlib.sha256(s["id"].encode()).hexdigest()[:8], 16)
    rng = random.Random(seed)
    P = list(s["palette"])
    motif = MOTIFS[s["motif"]]
    tex = s["texture"]
    body = "".join(motif(rng, P, Noise(rng)))
    if tex == "glow":
        body = '<g filter="url(#glow)">%s</g>' % body
    over = {"grain": '<rect width="%d" height="%d" filter="url(#noise)" opacity="0.5"/>',
            "paper": '<rect width="%d" height="%d" filter="url(#noise)" opacity="0.35"/>',
            "canvas": '<rect width="%d" height="%d" fill="url(#pcanvas)"/>',
            "scan": '<rect width="%d" height="%d" fill="url(#pscan)"/>',
            "halftone": '<rect width="%d" height="%d" fill="url(#phalf)"/>',
            "vignette": '<rect width="%d" height="%d" fill="url(#vig)" opacity="' + ("0.45" if _lum(P[0]) > 140 else "1") + '"/>'}.get(tex, "")
    over = over % (W, H) if over else ""
    if tex in ("glow", "grain"):
        over += '<rect width="%d" height="%d" fill="url(#vig)" opacity="%s"/>' % (W, H, "0.25" if _lum(P[0]) > 140 else "0.6")
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img" aria-label="%s">'
            '<title>%s · %s</title>%s<rect width="%d" height="%d" fill="%s"/><g>%s</g>%s</svg>'
            % (W, H, W, H, html.escape(s["name"]), s["id"], html.escape(s["name"]), _defs(P, tex, seed), W, H, P[0], body, over))


# ----------------------------------------------------------------------- catalog

CSS = """
@font-face{font-family:KLib;src:url('%(font)s')}
@page{size:A4;margin:12mm 10mm}
*{box-sizing:border-box}body{margin:0;font-family:KLib,'DejaVu Sans',sans-serif;color:#1b1b1f;background:#fff}
.cover{height:265mm;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;
 background:#14121a;color:#f3eee6;page-break-after:always;padding:20mm}
.cover h1{font-size:40pt;margin:0 0 6mm}.cover h2{font-size:18pt;font-weight:400;margin:0 0 10mm;color:#e2b04a}
.cover p{font-size:11pt;max-width:150mm;line-height:1.7;color:#cfc8bd}
.cover .mosaic{display:grid;grid-template-columns:repeat(8,1fr);gap:2mm;width:170mm;margin:8mm 0}
.cover .mosaic img{width:100%%;border-radius:1.5mm;display:block}
.toc{page-break-after:always;padding:6mm 4mm}.toc h2{font-size:18pt}.toc ol{columns:2;font-size:9.5pt;line-height:1.45}.toc li{margin-bottom:2mm;break-inside:avoid}
.group{page-break-before:always}.group:first-of-type{page-break-before:auto}
.gh{display:flex;justify-content:space-between;align-items:baseline;border-bottom:2px solid #1b1b1f;margin:0 0 4mm;padding-bottom:2mm}
.gh h2{margin:0;font-size:16pt}.gh .ar{font-size:16pt;direction:rtl}.gh small{color:#666;font-size:9pt}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:4mm}
.card{break-inside:avoid;page-break-inside:avoid;border:1px solid #e3e0da;border-radius:2.5mm;overflow:hidden;background:#faf9f7}
.card img,.card svg{display:block;width:100%%;height:auto;aspect-ratio:3/2}
.meta{padding:2mm 2.5mm 2.5mm}.id{font:600 7.5pt 'DejaVu Sans Mono',monospace;color:#8a8478}
.en{font-weight:700;font-size:9.5pt;margin-top:.5mm}.arn{direction:rtl;text-align:right;font-size:10.5pt;margin-top:.5mm}
.foot{font-size:7.5pt;color:#777;margin-top:6mm;text-align:center}
"""


def catalog(lib, out_dir, *, only=None, groups=None, title="أطلس أساليب KOSIF", images="svg", font=None):
    out_dir = Path(out_dir)
    sw = out_dir / "swatches"
    sw.mkdir(parents=True, exist_ok=True)
    styles = [s for s in lib["styles"] if (not only or s["source"] == only) and (not groups or s["group"] in groups)]
    gl = [g for g in lib["groups"] if any(s["group"] == g["id"] for s in styles)]
    for s in styles:
        (sw / (s["id"] + ".svg")).write_text(swatch_svg(s), encoding="utf-8")
    ext = "jpg" if images == "jpg" else "svg"
    font_url = ""
    if font:
        shutil.copyfile(font, out_dir / Path(font).name)
        font_url = Path(font).name
    body = []
    picks = [s for s in styles][:: max(1, len(styles) // 32)][:32]
    body.append('<section class="cover"><h1>%s</h1><h2>KOSIF Style Atlas · %d styles</h2><div class="mosaic">%s</div>'
                '<p>كل صفحة فيها مجموعة أساليب: رقم الأسلوب واسمه بالإنجليزي والعربي وصورة لقطة منه. اطلب أي أسلوب بالرقم أو بالاسم، '
                'مثلًا «اعمل لي مشهد بأسلوب KS-042». الصور رسوم إجرائية أصلية تلخّص الألوان والخامة والتكوين، وليست صورًا منسوخة.</p>'
                '<p>FA = 86 أسلوبًا حُلّلت من أطلس Futurepedia وأُعيدت صياغتها · KS = 500 أسلوب أصلي جديد من KOSIF</p></section>'
                % (html.escape(title), len(styles), "".join('<img src="swatches/%s.%s" alt="">' % (s["id"], ext) for s in picks)))
    body.append('<section class="toc"><h2>المجموعات / Groups</h2><ol>%s</ol></section>' % "".join(
        "<li>%s<br><span dir=rtl>%s</span> · %d</li>" % (html.escape(g["name"]), html.escape(g["name_ar"]),
                                                     sum(1 for s in styles if s["group"] == g["id"])) for g in gl))
    for g in gl:
        cards = []
        members = [s for s in styles if s["group"] == g["id"]]
        for s in members:
            cards.append('<div class="card"><img src="swatches/%s.%s" alt="%s"><div class="meta"><div class="id">%s</div>'
                         '<div class="en">%s</div><div class="arn">%s</div></div></div>'
                         % (s["id"], ext, html.escape(s["name"]), s["id"], html.escape(s["name"]), html.escape(s["name_ar"])))
        body.append('<section class="group"><div class="gh"><h2>%s <small>(%d)</small></h2><span class="ar">%s</span></div>'
                    '<div class="grid">%s</div></section>' % (html.escape(g["name"]), len(members), html.escape(g["name_ar"]), "".join(cards)))
    body.append('<div class="foot">python3 .claude/skills/kosif-superpowers/scripts/style_library.py describe &lt;ID&gt; · prompt &lt;ID&gt; --subject "…"</div>')
    page = ('<!doctype html><html lang="ar"><head><meta charset="utf-8"><title>%s</title><style>%s</style></head><body>%s</body></html>'
            % (html.escape(title), CSS % {"font": font_url}, "".join(body)))
    (out_dir / "index.html").write_text(page, encoding="utf-8")
    return out_dir / "index.html", styles


NODE_PDF = r"""
const path = require('path');
const fs = require('fs');
function loadPw() {
  const tries = [() => require.resolve('playwright', { paths: [process.cwd()] }), () => '/opt/node-tools/node_modules/playwright'];
  for (const t of tries) { try { return require(t()); } catch (e) {} }
  throw new Error('playwright not found');
}
(async () => {
  const [dir, pdf, mode] = process.argv.slice(2);
  const { chromium } = loadPw();
  const browser = await chromium.launch();
  const page = await browser.newPage({ deviceScaleFactor: 1.5, viewport: { width: 480, height: 320 } });
  if (mode === 'jpg') {
    const sw = path.join(dir, 'swatches');
    const files = fs.readdirSync(sw).filter(f => f.endsWith('.svg')).sort();
    for (const f of files) {
      await page.setContent('<html><body style="margin:0">' + fs.readFileSync(path.join(sw, f), 'utf8') + '</body></html>');
      await page.locator('svg').first().screenshot({ path: path.join(sw, f.replace(/\.svg$/, '.jpg')), type: 'jpeg', quality: 82 });
    }
  }
  await page.goto('file://' + path.join(dir, 'index.html'), { waitUntil: 'load' });
  await page.pdf({ path: pdf, format: 'A4', printBackground: true, preferCSSPageSize: true });
  await browser.close();
})().catch(e => { console.error(e.message); process.exit(1); });
"""


def render_pdf(out_dir, pdf, images):
    node = shutil.which("node")
    if not node:
        raise RuntimeError("node is required for --pdf (headless Chromium through Playwright)")
    with tempfile.TemporaryDirectory() as tmp:
        js = Path(tmp) / "pdf.cjs"
        js.write_text(NODE_PDF, encoding="utf-8")
        res = subprocess.run([node, str(js), str(Path(out_dir).resolve()), str(Path(pdf).resolve()), images],
                             capture_output=True, text=True, timeout=1800)
    if res.returncode:
        raise RuntimeError("PDF render failed: " + (res.stderr or res.stdout).strip()[:400])
    return Path(pdf)


def default_font():
    for f in FONT_CANDIDATES:
        if f.is_file():
            return str(f)
    return None


# --------------------------------------------------------------------------- CLI

def card_text(lib, s):
    g = next(x for x in lib["groups"] if x["id"] == s["group"])
    lines = ["%s · %s · %s" % (s["id"], s["name"], s["name_ar"]),
             "المجموعة: %s / %s" % (g["name_ar"], g["name"]),
             "الشكل (look): " + s["look"],
             "المنطق (logic): " + s["logic"]]
    if s.get("motion"):
        lines.append("الحركة (motion): " + s["motion"])
    if s.get("summary_ar"):
        lines.append("بالعربي: " + s["summary_ar"])
    lines += ["الألوان: " + " ".join(s["palette"]) + "  (" + ", ".join(dict.fromkeys(color_name(c) for c in s["palette"])) + ")",
              "الملمس: %s · التكوين: %s" % (s["texture"], s["motif"]),
              "البرومنت: " + recipe(s)]
    if s["source"] == "fa":
        lines.append("المصدر: أطلس Futurepedia (وصف معاد صياغته) — للفيلم الكامل: style_atlas_bridge.py brief --style " + s["id"])
    return "\n".join(lines)


def self_test():
    lib = load()
    assert len(lib["styles"]) == 586 and len([g for g in lib["groups"] if g["source"] == "ks"]) == 20
    ks = [s for s in lib["styles"] if s["source"] == "ks"]
    assert [s["id"] for s in ks] == ["KS-%03d" % i for i in range(1, 501)]
    assert len({s["name"].casefold() for s in lib["styles"]}) == 586
    for s in lib["styles"]:
        assert s["motif"] in MOTIFS and s["texture"] in TEXTURES, s["id"]
        assert len(s["palette"]) == 5 and all(re.fullmatch(r"#[0-9A-Fa-f]{6}", c) for c in s["palette"]), s["id"]
    a, b = swatch_svg(ks[0]), swatch_svg(ks[0])
    assert a == b and a.startswith("<svg")
    assert resolve(lib, "KS-001")["name"] == "Zellige Starfield"
    assert resolve(lib, "زليج النجوم")["id"] == "KS-001"
    assert find(lib, "خط عربي نيون")[0][1]["id"] == resolve(lib, "Arabic Neon Script")["id"]
    p = prompt(resolve(lib, "KS-002"), "a reading corner", mix=resolve(lib, "FA-12"))
    assert "a reading corner" in p["prompt"] and "{subject}" not in p["prompt"]
    print("self-test ok: 586 styles, %d motifs, deterministic swatches" % len(MOTIFS))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("groups", help="list the 34 groups (14 Futurepedia families + 20 KOSIF groups)")
    p = sub.add_parser("list", help="list styles")
    p.add_argument("--group")
    p.add_argument("--source", choices=("fa", "ks", "all"), default="all")
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("find", help="rank styles by Arabic or English words")
    p.add_argument("query")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--group")
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("describe", help="print one style card (id, slug, English or Arabic name)")
    p.add_argument("style")
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("prompt", help="fill a style's prompt recipe for a subject")
    p.add_argument("style")
    p.add_argument("--subject", required=True)
    p.add_argument("--mix", help="optional second style as a 30%% accent")
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("swatch", help="write one procedural SVG sample")
    p.add_argument("style")
    p.add_argument("--out", required=True)
    p = sub.add_parser("catalog", help="write every swatch and an illustrated index.html (and a PDF with --pdf)")
    p.add_argument("--out", required=True, help="new or empty output folder")
    p.add_argument("--source", choices=("fa", "ks", "all"), default="all")
    p.add_argument("--group", action="append", help="limit to a group id (repeatable)")
    p.add_argument("--pdf", help="also render this PDF through headless Chromium (node + playwright)")
    p.add_argument("--split-groups", action="store_true", help="with --pdf, also write one PDF per group next to it")
    p.add_argument("--title", default="أطلس أساليب KOSIF")
    sub.add_parser("self-test", help="offline checks of data, search, prompts and swatch determinism")
    a = ap.parse_args(argv)
    if a.cmd == "self-test":
        self_test()
        return 0
    lib = load()
    if a.cmd == "catalog":
        return run_catalog(lib, a)
    if a.cmd == "groups":
        for g in lib["groups"]:
            print("%-28s %3d  %s · %s" % (g["id"], sum(1 for s in lib["styles"] if s["group"] == g["id"]), g["name"], g["name_ar"]))
        return 0
    if a.cmd == "list":
        rows = [s for s in lib["styles"] if (a.source == "all" or s["source"] == a.source) and (not a.group or s["group"] == a.group)]
        if a.json:
            print(json.dumps([{k: s[k] for k in ("id", "name", "name_ar", "group")} for s in rows], ensure_ascii=False, indent=1))
        else:
            for s in rows:
                print("%-7s %-34s %s" % (s["id"], s["name"], s["name_ar"]))
        return 0
    if a.cmd == "find":
        hits = find(lib, a.query, a.limit, a.group)
        if a.json:
            print(json.dumps([{"score": sc, "id": s["id"], "name": s["name"], "name_ar": s["name_ar"]} for sc, s in hits], ensure_ascii=False, indent=1))
        else:
            for sc, s in hits:
                print("%-7s %-34s %s  (%d)" % (s["id"], s["name"], s["name_ar"], sc))
            if not hits:
                print("no match; try other words or: groups")
        return 0 if hits else 1
    s = resolve(lib, a.style)
    if a.cmd == "describe":
        print(json.dumps(s, ensure_ascii=False, indent=1) if a.json else card_text(lib, s))
        return 0
    if a.cmd == "prompt":
        res = prompt(s, a.subject, resolve(lib, a.mix) if a.mix else None)
        print(json.dumps(res, ensure_ascii=False, indent=1) if a.json else res["prompt"] + "\nNegative: " + res["negative"])
        return 0
    if a.cmd == "swatch":
        out = Path(a.out)
        if out.exists():
            raise SystemExit("refusing to overwrite " + str(out))
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(swatch_svg(s), encoding="utf-8")
        print(out)
        return 0
    return 2


def run_catalog(lib, a):
    out = Path(a.out)
    if out.exists() and any(out.iterdir()):
        raise SystemExit("output folder must be new or empty: " + str(out))
    src = None if a.source == "all" else a.source
    font = default_font()
    images = "jpg" if a.pdf else "svg"
    idx, styles = catalog(lib, out, only=src, groups=a.group, title=a.title, images=images, font=font)
    print("catalog: %d styles -> %s" % (len(styles), idx))
    if not a.pdf:
        return 0
    pdf = render_pdf(out, a.pdf, "jpg")
    print("pdf: %s (%.1f MB)" % (pdf, pdf.stat().st_size / 1e6))
    if a.split_groups:
        for g in [g for g in lib["groups"] if any(s["group"] == g["id"] for s in styles)]:
            gout = out / "groups" / g["id"]
            catalog(lib, gout, only=src, groups=[g["id"]], title=g["name_ar"] + " · " + g["name"], images="jpg", font=font)
            for f in (out / "swatches").glob("*.jpg"):
                if (gout / "swatches" / (f.stem + ".svg")).exists():
                    shutil.copyfile(f, gout / "swatches" / f.name)
            gp = render_pdf(gout, Path(a.pdf).parent / ("%s.pdf" % g["id"]), "keep")
            print("pdf: %s (%.1f MB)" % (gp, gp.stat().st_size / 1e6))
    return 0


if __name__ == "__main__":
    sys.exit(main())
