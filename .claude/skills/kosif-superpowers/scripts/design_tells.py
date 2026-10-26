#!/usr/bin/env python3
"""Design tells / كاشف علامات التصميم المولّد: a deterministic audit of HTML/CSS for the look every AI page shares.

Models trained on the same templates keep producing the same page: one sans-serif for everything, a purple-to-blue
gradient, cards inside cards, grey text on a coloured panel, an icon tile above every heading, emoji bullets,
everything centred, one radius and one big shadow on every box, "Unlock seamless..." copy, and on Arabic pages a
Latin-only font with no right-to-left direction. This tool finds those patterns with fixed rules (no model, no
network), scores the page out of 100 and says how to fix each hit. Idea from the 30-day GitHub pulse (GP-01:
pbakaus/impeccable, Leonxlnx/taste-skill); the rules and wording are our own.

    python3 scripts/design_tells.py audit page.html [more.html|style.css|folder ...] [--json] [--min 70]
    python3 scripts/design_tells.py rules            # the rule table (id, severity, what, fix)
    python3 scripts/design_tells.py --self-test

Exit codes: 0 = score >= --min (default 70), 3 = REVISE (score below --min), 1 = input error. The score is a
heuristic: a human (or a browser screenshot review) decides. It never edits files.
"""
from __future__ import annotations

import argparse
import colorsys
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

GENERIC_FONTS = {"inter", "roboto", "arial", "helvetica", "helvetica neue", "system-ui", "-apple-system",
                 "segoe ui", "sans-serif", "open sans", "poppins", "montserrat", "blinkmacsystemfont", "ui-sans-serif"}
ARABIC_FONTS = ("cairo", "tajawal", "almarai", "amiri", "noto naskh", "noto kufi", "noto sans arabic", "ibm plex sans arabic",
                "readex", "alexandria", "changa", "el messiri", "lateef", "scheherazade", "rubik", "harmattan", "markazi",
                "reem kufi", "aref ruqaa", "lalezar", "mada", "baloo bhaijaan", "vazirmatn", "kufam", "zain", "thmanyah",
                "dubai", "ge ss", "29lt", "noto sans", "segoe ui", "arial", "tahoma")
HYPE_WORDS = ["unlock", "supercharge", "seamless", "revolutioni", "elevate your", "empower", "next-level", "game-changer",
              "game changer", "cutting-edge", "unleash", "effortless", "transform your", "lorem ipsum", "in today's fast-paced",
              "take your .* to the next level", "all-in-one platform", "harness the power"]
PLACEHOLDER_IMG = re.compile(r"via\.placeholder\.com|placehold\.co|picsum\.photos|source\.unsplash\.com/random|placekitten|dummyimage\.com", re.I)
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿⭐✅✨]")
ARABIC = re.compile("[؀-ۿ]")
NAMED = {"white": "#ffffff", "black": "#000000", "gray": "#808080", "grey": "#808080", "silver": "#c0c0c0",
         "red": "#ff0000", "blue": "#0000ff", "purple": "#800080", "indigo": "#4b0082", "violet": "#ee82ee",
         "navy": "#000080", "teal": "#008080", "green": "#008000", "orange": "#ffa500", "yellow": "#ffff00"}
COLOR_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)|hsla?\([^)]*\)|\b(" + "|".join(NAMED) + r")\b", re.I)

RULES = [
    # id, weight, Arabic, English, fix
    ("DT-01", 8, "خط واحد عام لكل شيء", "one generic sans (Inter/Roboto/system) for every text",
     "pair a characterful display face for headings with a readable text face; set sizes on a scale"),
    ("DT-02", 10, "تدرج بنفسجي إلى أزرق", "purple/indigo-to-blue gradient",
     "derive colour from the brand or subject; one accent, used where the eye should go"),
    ("DT-03", 6, "نص بتدرج لوني في العناوين", "gradient-clipped heading text",
     "solid heading colour; let size, weight and space carry hierarchy"),
    ("DT-04", 10, "بطاقات داخل بطاقات", "cards nested inside cards",
     "flatten: one surface level per region; group with space and dividers, not more boxes"),
    ("DT-05", 8, "نص رمادي فوق خلفية ملونة", "grey text on a coloured background",
     "tint the text from the background hue (same hue, lower or higher lightness) or use white/near-black"),
    ("DT-06", 12, "تباين ضعيف", "text/background contrast below WCAG AA (4.5:1)",
     "raise contrast to >= 4.5:1 for body text, 3:1 for large text"),
    ("DT-07", 8, "أيقونة في مربع فوق كل عنوان", "rounded icon tile above every card heading",
     "drop the decorative tiles, or use one meaningful illustration for the section"),
    ("DT-08", 6, "إيموجي كنقاط أو عناوين", "emoji used as bullets or heading decoration",
     "real icons with a consistent stroke, or plain typographic bullets"),
    ("DT-09", 6, "كل شيء في المنتصف", "almost everything centre-aligned",
     "left-align (right-align in RTL) running text; centre only short display lines"),
    ("DT-10", 4, "نصف قطر واحد لكل شيء", "one border-radius value on every element",
     "define 2-3 radii by role (control, card, pill) or go square where it suits the brand"),
    ("DT-11", 5, "ظلال ثقيلة في كل مكان", "large soft shadows on many elements",
     "keep elevation for things that float (menus, dialogs); use borders or tone for the rest"),
    ("DT-12", 4, "زجاج ضبابي مفرط", "frosted-glass blur used repeatedly",
     "one translucent layer at most, over content that justifies it"),
    ("DT-13", 8, "عبارات تسويقية جاهزة", "stock hype copy (unlock, seamless, supercharge, elevate...)",
     "say what it does for whom with a concrete number or example (TB36 SUCCESs)"),
    ("DT-14", 6, "صور بديلة مؤقتة", "placeholder image services",
     "use real, credited images or a deliberate illustration; never ship placeholders"),
    ("DT-15", 12, "صفحة عربية بخط لاتيني فقط", "Arabic text with a Latin-only font stack",
     "add an Arabic-capable family first in the stack (e.g. IBM Plex Sans Arabic, Noto Naskh Arabic, Cairo)"),
    ("DT-16", 10, "نص عربي بلا اتجاه RTL", "Arabic text without dir=\"rtl\"",
     "set <html lang=\"ar\" dir=\"rtl\"> (or dir on the container) and mirror the layout"),
    ("DT-17", 4, "ظهور متدرج لكل عنصر عند التمرير", "fade-in-on-scroll on everything",
     "animate only what explains change; respect prefers-reduced-motion"),
    ("DT-18", 5, "ألوان مميزة كثيرة", "more than six saturated accent hues",
     "limit the palette: one accent, one or two supporting hues, neutrals"),
    ("DT-19", 3, "بلا احترام لتقليل الحركة", "animations with no prefers-reduced-motion rule",
     "add @media (prefers-reduced-motion: reduce) that turns motion off"),
]
RULE = {r[0]: r for r in RULES}


# ---------------------------------------------------------------- colour helpers

def parse_color(s: str):
    """CSS colour → (r, g, b) 0..255, or None."""
    s = s.strip().lower()
    s = NAMED.get(s, s)
    if s.startswith("#"):
        h = s[1:]
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h[:3])
        if len(h) in (6, 8):
            try:
                return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
            except ValueError:
                return None
        return None
    m = re.match(r"rgba?\(([^)]*)\)", s)
    if m:
        parts = re.split(r"[\s,/]+", m.group(1).strip())
        try:
            vals = [float(p[:-1]) * 2.55 if p.endswith("%") else float(p) for p in parts[:3]]
            return tuple(int(max(0, min(255, v))) for v in vals)
        except ValueError:
            return None
    m = re.match(r"hsla?\(([^)]*)\)", s)
    if m:
        parts = re.split(r"[\s,/]+", m.group(1).strip())
        try:
            h = float(parts[0].replace("deg", "")) / 360
            sat = float(parts[1].rstrip("%")) / 100
            lig = float(parts[2].rstrip("%")) / 100
        except (ValueError, IndexError):
            return None
        r, g, b = colorsys.hls_to_rgb(h % 1, lig, sat)
        return int(r * 255), int(g * 255), int(b * 255)
    return None


def hsl(rgb):
    h, l, s = colorsys.rgb_to_hls(*(c / 255 for c in rgb))
    return h * 360, s, l


def luminance(rgb):
    def ch(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b) -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return round((la + 0.05) / (lb + 0.05), 2)


def is_greyish(rgb) -> bool:
    _, s, l = hsl(rgb)
    return s < 0.12 and 0.3 < l < 0.75


def is_saturated(rgb) -> bool:
    _, s, l = hsl(rgb)
    return s > 0.35 and 0.2 < l < 0.8


# ---------------------------------------------------------------- page model

class Page(HTMLParser):
    """Collects CSS, element classes with nesting, text blocks and attributes."""

    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.css, self.stack, self.texts, self.events = [], [], [], []
        self.html_attrs, self.in_style, self.in_script = {}, False, False
        self.card_nest_max, self.links, self.imgs = 0, [], []
        self.icon_before_heading = 0
        self._last_was_icon = False

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if tag == "html":
            self.html_attrs = a
        if tag == "style":
            self.in_style = True
        if tag == "script":
            self.in_script = True
        if tag == "link" and "stylesheet" in a.get("rel", ""):
            self.links.append(a.get("href", ""))
        if tag == "img":
            self.imgs.append(a.get("src", ""))
        if a.get("style"):
            self.css.append("x{" + a["style"] + "}")
        cls = a.get("class", "").lower()
        is_card = bool(re.search(r"\b[\w-]*card[\w-]*\b|\btile\b|\bpanel\b", cls))
        is_icon = bool(re.search(r"icon|emoji|badge-icon|feature-icon", cls)) or tag == "svg" and "icon" in cls
        if tag in ("h2", "h3", "h4") and self._last_was_icon:
            self.icon_before_heading += 1
        self._last_was_icon = is_icon
        if tag in self.VOID:
            return
        self.stack.append((tag, is_card, a.get("dir", "")))
        depth = sum(1 for _, c, _ in self.stack if c)
        self.card_nest_max = max(self.card_nest_max, depth)
        self.events.append(tag)

    def handle_endtag(self, tag):
        if tag == "style":
            self.in_style = False
        if tag == "script":
            self.in_script = False
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if self.in_style:
            self.css.append(data)
            return
        if self.in_script or not data.strip():
            return
        parent = self.stack[-1][0] if self.stack else ""
        rtl = any(d == "rtl" for _, _, d in self.stack)
        self.texts.append((parent, data.strip(), rtl))


def shadow_blur(value: str) -> float:
    """Largest blur radius (px) in a box-shadow list; rem/em counted as 16px."""
    best = 0.0
    for part in re.split(r",(?![^(]*\))", COLOR_RE.sub(" ", value)):
        toks = re.findall(r"(-?\d*\.?\d+)(px|rem|em)?", part.replace("inset", ""))
        if len(toks) >= 3:
            num, unit = toks[2]
            best = max(best, float(num) * (16 if unit in ("rem", "em") else 1))
    return best


def resolve_vars(css: str) -> str:
    """Substitute var(--x[, fallback]) with the last declared --x value (three passes for nesting)."""
    decl = dict(re.findall(r"(--[\w-]+)\s*:\s*([^;}]+)", css))
    for _ in range(3):
        css = re.sub(r"var\(\s*(--[\w-]+)\s*(?:,\s*([^()]*))?\)",
                     lambda m: decl.get(m.group(1), m.group(2) or "").strip(), css)
    return css


def css_rules(css: str):
    """Yield (selector, {prop: value}) for innermost blocks (media queries flattened)."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    for sel, body in re.findall(r"([^{}]*)\{([^{}]*)\}", css):
        props = {}
        for decl in body.split(";"):
            if ":" in decl:
                k, v = decl.split(":", 1)
                props[k.strip().lower()] = v.strip()
        yield sel.strip(), props


def load_inputs(paths):
    """→ (html_text, css_text, labels). Folders: every *.html / *.css inside (not recursive into node_modules)."""
    html, css, labels = [], [], []
    files = []
    for p in map(Path, paths):
        if p.is_dir():
            files += [f for f in sorted(p.rglob("*")) if f.suffix.lower() in (".html", ".htm", ".css")
                      and "node_modules" not in f.parts][:200]
        elif p.is_file():
            files.append(p)
        else:
            raise FileNotFoundError(str(p))
    for f in files:
        txt = f.read_text(encoding="utf-8", errors="replace")
        labels.append(str(f))
        if f.suffix.lower() == ".css":
            css.append(txt)
        else:
            html.append(txt)
            for href in re.findall(r'<link[^>]+href="([^"]+\.css)"', txt):
                local = (f.parent / href).resolve()
                if local.is_file() and str(local) not in labels:
                    css.append(local.read_text(encoding="utf-8", errors="replace"))
                    labels.append(str(local))
    return "\n".join(html), "\n".join(css), labels


# ---------------------------------------------------------------- audit

def audit_text(html: str, css_extra: str = "") -> dict:
    page = Page()
    page.feed(html)
    css = resolve_vars("\n".join(page.css) + "\n" + css_extra)
    rules = list(css_rules(css))
    hits = []

    def hit(rid, evidence):
        hits.append({"id": rid, "weight": RULE[rid][1], "what_ar": RULE[rid][2], "what": RULE[rid][3],
                     "evidence": evidence, "fix": RULE[rid][4]})

    fams = []
    for _, p in rules:
        for k in ("font-family", "font"):
            if k in p:
                fams.append(p[k].lower())
    families = set()
    for f in fams:
        for name in f.split(","):
            name = name.strip().strip("'\"")
            name = re.sub(r"^.*\d+(px|rem|em|%)\s*(/\s*[\d.]+\w*)?\s*", "", name)  # strip font shorthand sizes
            if name:
                families.add(name)
    named = {f for f in families if f not in ("inherit", "initial", "sans-serif", "serif", "monospace")}
    if (not named and not fams) or (named and named <= GENERIC_FONTS):
        hit("DT-01", "font families: " + (", ".join(sorted(families)) or "none set (browser default)"))

    grads = [p.get("background", "") + " " + p.get("background-image", "") for _, p in rules]
    for g in grads:
        if "gradient" not in g:
            continue
        cols = [parse_color(m.group(0)) for m in COLOR_RE.finditer(g)]
        hues = [hsl(c)[0] for c in cols if c and is_saturated(c)]
        if len(hues) >= 2 and all(195 <= h <= 300 for h in hues) and max(hues) >= 255 and min(hues) <= 245:
            hit("DT-02", g.strip()[:120])
            break
    for sel, p in rules:
        if "text" in p.get("-webkit-background-clip", "") + p.get("background-clip", "") and "gradient" in (
                p.get("background", "") + p.get("background-image", "")):
            hit("DT-03", sel[:80])
            break
    if page.card_nest_max >= 2:
        hit("DT-04", f"card-like elements nested {page.card_nest_max} deep")
    low, grey_on_colour = [], []
    for sel, p in rules:
        fg = parse_color(p.get("color", "")) if p.get("color") else None
        bgv = p.get("background-color") or (p.get("background", "") if "gradient" not in p.get("background", "") else "")
        m = COLOR_RE.search(bgv or "")
        opaque = m and not re.search(r"color-mix|transparent|url\(", bgv) and len(COLOR_RE.findall(bgv)) == 1 \
            and not re.search(r"rgba?\([^)]*[,/]\s*0?\.[0-8]\d*\s*\)|#[0-9a-f]{6}[0-c][0-9a-f]\b|#[0-9a-f]{3}[0-c]\b", bgv, re.I)
        bg = parse_color(m.group(0)) if opaque else None
        if fg and bg:
            if is_greyish(fg) and is_saturated(bg):
                grey_on_colour.append(sel[:60])
            c = contrast(fg, bg)
            if c < 4.5:
                low.append(f"{sel[:50]} {c}:1")
    if grey_on_colour:
        hit("DT-05", "; ".join(grey_on_colour[:4]))
    if low:
        hit("DT-06", "; ".join(low[:4]))
    if page.icon_before_heading >= 3:
        hit("DT-07", f"{page.icon_before_heading} headings directly after an icon element")
    emoji_heads = [t for tag, t, _ in page.texts if tag in ("h1", "h2", "h3", "h4", "li") and EMOJI.match(t)]
    if len(emoji_heads) >= 3:
        hit("DT-08", " | ".join(emoji_heads[:4]))
    aligns = [p.get("text-align") for _, p in rules if "text-align" in p]
    centred = sum(1 for a in aligns if a == "center")
    if centred >= 4 and centred / max(1, len(aligns)) >= 0.7:
        hit("DT-09", f"{centred} of {len(aligns)} text-align declarations are center")
    radii = [p["border-radius"] for _, p in rules if "border-radius" in p]
    if len(radii) >= 6 and len(set(radii)) == 1:
        hit("DT-10", f"border-radius {radii[0]} on {len(radii)} rules")
    big_shadows = [p["box-shadow"] for _, p in rules if "box-shadow" in p and shadow_blur(p["box-shadow"]) >= 20]
    if len(big_shadows) >= 4:
        hit("DT-11", f"{len(big_shadows)} rules with blur >= 20px")
    blurs = [1 for _, p in rules if "blur(" in p.get("backdrop-filter", "") + p.get("-webkit-backdrop-filter", "")]
    if len(blurs) >= 3:
        hit("DT-12", f"backdrop blur on {len(blurs)} rules")
    body_text = " ".join(t for _, t, _ in page.texts).lower()
    hype = [w for w in HYPE_WORDS if re.search(w, body_text)]
    if len(hype) >= 2:
        hit("DT-13", ", ".join(hype[:6]))
    ph = [s for s in page.imgs if PLACEHOLDER_IMG.search(s)] + PLACEHOLDER_IMG.findall(css)
    if ph:
        hit("DT-14", ", ".join(map(str, ph[:3])))
    arabic_chars = len(ARABIC.findall(body_text))
    if arabic_chars >= 20:
        if not any(any(a in f for a in ARABIC_FONTS) for f in families):
            hit("DT-15", "Arabic text, font stack: " + (", ".join(sorted(families)) or "browser default"))
        rtl_html = page.html_attrs.get("dir", "").lower() == "rtl"
        rtl_any = rtl_html or any(r for _, _, r in page.texts) or re.search(r"direction\s*:\s*rtl", css)
        if not rtl_any:
            hit("DT-16", f"{arabic_chars} Arabic letters, no dir=rtl / direction:rtl")
    fades = len(re.findall(r"fade-?in|fadeinup|data-aos|reveal-on-scroll|animate__fadeIn", html + css, re.I))
    if fades >= 5:
        hit("DT-17", f"{fades} fade/reveal hooks")
    hues = set()
    for m in COLOR_RE.finditer(css):
        c = parse_color(m.group(0))
        if c and is_saturated(c):
            hues.add(int(hsl(c)[0] // 20))
    if len(hues) > 6:
        hit("DT-18", f"{len(hues)} distinct saturated hue bands")
    if re.search(r"@keyframes|animation\s*:|transition\s*:", css) and "prefers-reduced-motion" not in css:
        hit("DT-19", "animations/transitions found, no prefers-reduced-motion block")
    score = max(0, 100 - sum(h["weight"] for h in hits))
    return {"score": score, "verdict": None, "hits": hits, "stats": {
        "css_rules": len(rules), "font_families": sorted(families), "text_blocks": len(page.texts),
        "arabic_letters": arabic_chars, "card_nesting": page.card_nest_max}}


def report(res: dict, labels, min_score: int) -> str:
    out = [f"design tells — {', '.join(labels)}", f"score {res['score']}/100 → {res['verdict']} (min {min_score})", ""]
    if not res["hits"]:
        out.append("no tells found. Still look at it in a browser at phone and desktop width.")
    for h in sorted(res["hits"], key=lambda h: -h["weight"]):
        out += [f"[{h['id']}] -{h['weight']}  {h['what']} / {h['what_ar']}", f"    evidence: {h['evidence']}",
                f"    fix: {h['fix']}"]
    return "\n".join(out)


def self_test() -> int:
    slop = """<html><head><style>
    body{font-family:Inter,sans-serif;text-align:center}
    .hero{background:linear-gradient(135deg,#7c3aed,#2563eb)}
    h1{background:linear-gradient(90deg,#8b5cf6,#3b82f6);-webkit-background-clip:text;color:transparent;text-align:center}
    .card{border-radius:16px;box-shadow:0 10px 30px rgba(0,0,0,.2);text-align:center}
    .a{border-radius:16px;box-shadow:0 8px 24px #0003}.b{border-radius:16px;box-shadow:0 8px 40px #0003}
    .c{border-radius:16px;box-shadow:0 8px 40px #0003}.d{border-radius:16px}.e{border-radius:16px}
    .muted{color:#888888;background-color:#2563eb}
    .x{text-align:center}
    .fade-in{animation:f 1s}@keyframes f{from{opacity:0}}
    </style></head><body>
    <div class="card"><div class="card-inner card"><div class="feature-icon">*</div><h3>Fast</h3></div></div>
    <div class="feature-icon">*</div><h3>Secure</h3><div class="feature-icon">*</div><h3>Simple</h3>
    <ul><li>🚀 Speed</li><li>✨ Magic</li><li>✅ Done</li></ul>
    <p>Unlock seamless workflows and supercharge your team.</p>
    <img src="https://via.placeholder.com/300">
    </body></html>"""
    res = audit_text(slop)
    ids = {h["id"] for h in res["hits"]}
    need = {"DT-01", "DT-02", "DT-03", "DT-04", "DT-05", "DT-06", "DT-07", "DT-08", "DT-09", "DT-10", "DT-11",
            "DT-13", "DT-14", "DT-19"}
    ok = need <= ids and res["score"] < 40
    if not ok:
        print("FAIL slop page:", sorted(need - ids), res["score"])
    clean = """<html lang="ar" dir="rtl"><head><style>
    body{font-family:'IBM Plex Sans Arabic','Noto Naskh Arabic',serif;color:#1b1b1b;background-color:#fbf8f2}
    h1{font-family:'Reem Kufi',serif;font-size:3rem}
    .note{color:#5a3e00;background-color:#fff1cc}
    @media (prefers-reduced-motion: reduce){*{animation:none}}
    </style></head><body><h1>مرحبًا بكم في متجر القهوة المختصة</h1>
    <p>نحمّص البن كل صباح في الإسكندرية ونوصله خلال يومين، وكل كيس عليه تاريخ التحميص واسم المزرعة.</p></body></html>"""
    res2 = audit_text(clean)
    if res2["hits"]:
        ok = False
        print("FAIL clean page hits:", [h["id"] for h in res2["hits"]])
    ar_bad = "<html><body style=\"font-family:Inter\"><p>" + "نص عربي طويل بما يكفي لاختبار الاتجاه والخط " * 2 + "</p></body></html>"
    ids3 = {h["id"] for h in audit_text(ar_bad)["hits"]}
    if not {"DT-15", "DT-16"} <= ids3:
        ok = False
        print("FAIL arabic page:", ids3)
    if audit_text("<style>.k{color:#f60;background:color-mix(in srgb,#f60 16%,transparent)}</style>")["hits"] and \
            any(h["id"] == "DT-06" for h in audit_text("<style>.k{color:#f60;background:color-mix(in srgb,#f60 16%,transparent)}</style>")["hits"]):
        ok = False
        print("FAIL translucent background treated as opaque")
    if shadow_blur("0 10px 30px rgba(0,0,0,.2)") != 30 or shadow_blur("inset 0 0 0 1px #000") != 0:
        ok = False
        print("FAIL shadow parse")
    if "Cairo" not in resolve_vars(":root{--f:Cairo, serif} b{font-family:var(--f)}"):
        ok = False
        print("FAIL var resolution")
    if contrast((255, 255, 255), (0, 0, 0)) != 21.0 or parse_color("hsl(240, 100%, 50%)") != (0, 0, 255):
        ok = False
        print("FAIL colour maths")
    print("self-test ok" if ok else "self-test FAILED")
    return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--self-test", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    a = sub.add_parser("audit")
    a.add_argument("paths", nargs="+")
    a.add_argument("--json", action="store_true")
    a.add_argument("--min", type=int, default=70)
    r = sub.add_parser("rules")
    r.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if args.cmd == "rules":
        if args.json:
            print(json.dumps([dict(zip(("id", "weight", "what_ar", "what", "fix"), x)) for x in RULES], ensure_ascii=False, indent=1))
        else:
            for rid, w, ar, en, fix in RULES:
                print(f"{rid}  -{w:<3} {en} / {ar}\n        fix: {fix}")
        return 0
    if args.cmd == "audit":
        try:
            html, css, labels = load_inputs(args.paths)
        except FileNotFoundError as e:
            print(f"not found: {e}", file=sys.stderr)
            return 1
        res = audit_text(html, css)
        res["verdict"] = "PASS" if res["score"] >= args.min else "REVISE"
        res["inputs"] = labels
        print(json.dumps(res, ensure_ascii=False, indent=1) if args.json else report(res, labels, args.min))
        return 0 if res["verdict"] == "PASS" else 3
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
