"""SVG -> picture program. Ask any AI to "draw it as SVG", paste the SVG into the studio, and every element becomes
a step the studio paints pixel by pixel. It stays vector, so it renders at any size.

Supported: rect (rounded), circle, ellipse, line, polyline, polygon, path (all commands, arcs too), text/tspan
(Arabic shaped), g/svg/a/use, transforms, fill/stroke/opacity, fill-rule, inline style, <style> rules by tag,
.class and #id, linear and radial gradients (stops may be see-through). Not drawn: filters, masks, clip paths,
patterns, embedded images (their shapes are still drawn without the effect).
"""
from __future__ import annotations

import math
import re
import xml.etree.ElementTree as ET

from render import H0, W0, Step, compound, ellipse, fill, lin, path, rad, rect, stroke, text

NAMED = {"black": "#000000", "white": "#ffffff", "red": "#ff0000", "green": "#008000", "blue": "#0000ff",
         "yellow": "#ffff00", "orange": "#ffa500", "purple": "#800080", "pink": "#ffc0cb", "brown": "#a52a2a",
         "gray": "#808080", "grey": "#808080", "lightgray": "#d3d3d3", "lightgrey": "#d3d3d3", "darkgray": "#a9a9a9",
         "darkgrey": "#a9a9a9", "silver": "#c0c0c0", "gold": "#ffd700", "navy": "#000080", "teal": "#008080",
         "maroon": "#800000", "olive": "#808000", "lime": "#00ff00", "aqua": "#00ffff", "cyan": "#00ffff",
         "magenta": "#ff00ff", "fuchsia": "#ff00ff", "skyblue": "#87ceeb", "lightblue": "#add8e6",
         "darkblue": "#00008b", "darkgreen": "#006400", "lightgreen": "#90ee90", "forestgreen": "#228b22",
         "darkred": "#8b0000", "crimson": "#dc143c", "coral": "#ff7f50", "salmon": "#fa8072", "tomato": "#ff6347",
         "khaki": "#f0e68c", "beige": "#f5f5dc", "ivory": "#fffff0", "tan": "#d2b48c", "chocolate": "#d2691e",
         "sienna": "#a0522d", "violet": "#ee82ee", "indigo": "#4b0082", "turquoise": "#40e0d0", "orchid": "#da70d6",
         "plum": "#dda0dd", "lavender": "#e6e6fa", "midnightblue": "#191970", "steelblue": "#4682b4",
         "royalblue": "#4169e1", "slategray": "#708090", "darkslategray": "#2f4f4f", "goldenrod": "#daa520",
         "darkorange": "#ff8c00", "hotpink": "#ff69b4", "deeppink": "#ff1493", "firebrick": "#b22222",
         "seagreen": "#2e8b57", "mintcream": "#f5fffa", "whitesmoke": "#f5f5f5", "snow": "#fffafa",
         "dodgerblue": "#1e90ff", "deepskyblue": "#00bfff", "lightyellow": "#ffffe0", "wheat": "#f5deb3",
         "peru": "#cd853f", "saddlebrown": "#8b4513", "yellowgreen": "#9acd32", "olivedrab": "#6b8e23",
         "springgreen": "#00ff7f", "limegreen": "#32cd32", "darkviolet": "#9400d3", "slateblue": "#6a5acd",
         "cornflowerblue": "#6495ed", "lightpink": "#ffb6c1", "mistyrose": "#ffe4e1", "honeydew": "#f0fff0"}
SKIP = {"defs", "clipPath", "mask", "pattern", "symbol", "marker", "title", "desc", "metadata", "style", "filter",
        "linearGradient", "radialGradient", "script", "foreignObject", "image"}
NAMES_AR = {"rect": "مستطيل", "circle": "دائرة", "ellipse": "شكل بيضاوي", "line": "خط", "polyline": "خط متعدد",
            "polygon": "مضلع", "path": "مسار", "text": "نص"}
INHERIT = {"fill", "stroke", "stroke-width", "fill-opacity", "stroke-opacity", "fill-rule", "font-size",
           "font-family", "font-weight", "text-anchor", "visibility", "color", "stroke-linejoin", "stroke-linecap"}


def _tag(el) -> str:
    return el.tag.rsplit("}", 1)[-1]


def _num(v, ref: float = 100.0, default: float = 0.0) -> float:
    if v is None:
        return default
    v = str(v).strip()
    m = re.match(r"[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?", v)
    if not m:
        return default
    x = float(m.group(0))
    unit = v[m.end():].strip()
    return x / 100 * ref if unit == "%" else x * 16 if unit in ("em", "rem") else x * 1.333 if unit == "pt" else x


def _nums(v) -> list[float]:
    return [float(t) for t in re.findall(r"[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?", v or "")]


# ── transforms: (a, b, c, d, e, f) maps x, y to a*x + c*y + e, b*x + d*y + f ──────────────────────────────────
def _mul(m, n):
    a, b, c, d, e, f = m
    A, B, C, D, E, F = n
    return (a * A + c * B, b * A + d * B, a * C + c * D, b * C + d * D, a * E + c * F + e, b * E + d * F + f)


def _apply(m, pts):
    return [(m[0] * x + m[2] * y + m[4], m[1] * x + m[3] * y + m[5]) for x, y in pts]


def _scale_of(m) -> float:
    return math.sqrt(abs(m[0] * m[3] - m[1] * m[2])) or 1.0


def _transform(s: str | None):
    m = (1, 0, 0, 1, 0, 0)
    for name, args in re.findall(r"(\w+)\s*\(([^)]*)\)", s or ""):
        v = _nums(args)
        if name == "matrix" and len(v) == 6:
            t = tuple(v)
        elif name == "translate":
            t = (1, 0, 0, 1, v[0], v[1] if len(v) > 1 else 0)
        elif name == "scale":
            t = (v[0], 0, 0, v[1] if len(v) > 1 else v[0], 0, 0)
        elif name == "rotate":
            a = math.radians(v[0])
            t = (math.cos(a), math.sin(a), -math.sin(a), math.cos(a), 0, 0)
            if len(v) == 3:
                t = _mul(_mul((1, 0, 0, 1, v[1], v[2]), t), (1, 0, 0, 1, -v[1], -v[2]))
        elif name == "skewX":
            t = (1, 0, math.tan(math.radians(v[0])), 1, 0, 0)
        elif name == "skewY":
            t = (1, math.tan(math.radians(v[0])), 0, 1, 0, 0)
        else:
            continue
        m = _mul(m, t)
    return m


# ── colours and styles ────────────────────────────────────────────────────────────────────────────────────────
def _colour(v: str | None, current: str = "#000000"):
    """'#rgb', '#rrggbb', rgb()/rgba(), names, currentColor -> '#rrggbbaa', or None for 'none'."""
    if v is None:
        return None
    v = v.strip()
    lv = v.lower()
    if lv in ("none", "transparent", ""):
        return None
    if lv == "currentcolor":
        return _colour(current)
    if lv in NAMED:
        return NAMED[lv] + "ff"
    if v.startswith("#"):
        h = v[1:]
        if len(h) in (3, 4):
            h = "".join(ch * 2 for ch in h)
        return "#" + (h + "ff")[:8] if len(h) in (6, 8) else None
    m = re.match(r"rgba?\(([^)]*)\)", lv)
    if m:
        parts = [p.strip() for p in m.group(1).replace("/", ",").split(",") if p.strip()]
        ch = [round(float(p[:-1]) * 2.55) if p.endswith("%") else round(float(p)) for p in parts[:3]]
        a = parts[3] if len(parts) > 3 else "1"
        a = float(a[:-1]) / 100 if a.endswith("%") else float(a)
        return "#%02x%02x%02x%02x" % (*[max(0, min(255, c)) for c in ch], round(max(0.0, min(1.0, a)) * 255))
    m = re.match(r"hsla?\(([^)]*)\)", lv)
    if m:
        import colorsys
        p = [float(x) for x in re.findall(r"[+-]?\d*\.?\d+", m.group(1))]
        r, g, b = colorsys.hls_to_rgb((p[0] % 360) / 360, p[2] / 100, p[1] / 100)
        a = p[3] if len(p) > 3 else 1
        return "#%02x%02x%02x%02x" % (round(r * 255), round(g * 255), round(b * 255), round(a * 255))
    return None


def _with_alpha(c: str, a: float) -> str:
    base = int(c[7:9], 16) / 255 if len(c) == 9 else 1.0
    return c[:7] + "%02x" % round(max(0.0, min(1.0, base * a)) * 255)


def _css(root) -> list[tuple[str, dict]]:
    rules = []
    for st in root.iter():
        if _tag(st) == "style" and st.text:
            body = re.sub(r"/\*.*?\*/", "", st.text, flags=re.S)
            for sel, decl in re.findall(r"([^{}]+)\{([^}]*)\}", body):
                d = _decls(decl)
                for one in sel.split(","):
                    rules.append((one.strip(), d))
    return rules


def _decls(s: str) -> dict:
    out = {}
    for part in (s or "").split(";"):
        if ":" in part:
            k, v = part.split(":", 1)
            out[k.strip()] = v.replace("!important", "").strip()
    return out


def _matches(sel: str, el) -> bool:
    tag, cls, eid = _tag(el), (el.get("class") or "").split(), el.get("id")
    m = re.fullmatch(r"([a-zA-Z][\w-]*)?((?:[.#][\w-]+)*)", sel)
    if not m:
        return False
    if m.group(1) and m.group(1) != tag:
        return False
    for kind, name in re.findall(r"([.#])([\w-]+)", m.group(2)):
        if (kind == "." and name not in cls) or (kind == "#" and name != eid):
            return False
    return bool(m.group(1) or m.group(2))


# ── the importer ────────────────────────────────────────────────────────────────────────────────────────────
class _Svg:
    def __init__(self, root):
        self.root = root
        self.rules = _css(root)
        self.ids = {el.get("id"): el for el in root.iter() if el.get("id")}
        vb = _nums(root.get("viewBox"))
        if len(vb) == 4 and vb[2] > 0 and vb[3] > 0:
            self.vx, self.vy, self.vw, self.vh = vb
        else:
            self.vx, self.vy = 0.0, 0.0
            self.vw, self.vh = _num(root.get("width"), default=300) or 300, _num(root.get("height"), default=150) or 150
        s = min((W0 - 40) / self.vw, (H0 - 40) / self.vh)
        self.fit = (s, 0, 0, s, (W0 - self.vw * s) / 2 - self.vx * s, (H0 - self.vh * s) / 2 - self.vy * s)
        self.items: list[tuple[str, list, tuple]] = []      # (label, ops, centre)

    def style(self, el, parent: dict) -> dict:
        st = {k: v for k, v in parent.items() if k in INHERIT}
        for k in ("fill", "stroke", "stroke-width", "opacity", "fill-opacity", "stroke-opacity", "fill-rule",
                  "font-size", "font-family", "font-weight", "text-anchor", "display", "visibility", "color",
                  "stop-color", "stop-opacity"):
            if el.get(k) is not None:
                st[k] = el.get(k)
        for sel, d in self.rules:
            if _matches(sel, el):
                st.update(d)
        st.update(_decls(el.get("style")))
        st["_opacity"] = parent.get("_opacity", 1.0) * _num(st.pop("opacity", None), 1, 1.0)
        return st

    def paint(self, v: str | None, st: dict, m, bbox, alpha: float):
        """A fill/stroke value -> render paint (colour '#rrggbbaa' or gradient), or None."""
        if v is None:
            return None
        u = re.match(r"url\(\s*['\"]?#([^)'\"]+)['\"]?\s*\)", v.strip())
        if u:
            g = self.ids.get(u.group(1))
            return self.gradient(g, m, bbox, alpha) if g is not None else None
        c = _colour(v, st.get("color", "#000000"))
        return _with_alpha(c, alpha) if c else None

    def gradient(self, g, m, bbox, alpha):
        chain, el = [], g
        while el is not None and len(chain) < 8:         # href inheritance (stops and attributes)
            chain.append(el)
            ref = el.get("{http://www.w3.org/1999/xlink}href") or el.get("href")
            el = self.ids.get(ref[1:]) if ref and ref.startswith("#") else None

        def attr(k, default=None):
            return next((e.get(k) for e in chain if e.get(k) is not None), default)
        stops = []
        for e in chain:
            ss = [s for s in e if _tag(s) == "stop"]
            if ss:
                for s in ss:
                    sd = {**{k: s.get(k) for k in ("stop-color", "stop-opacity") if s.get(k)}, **_decls(s.get("style"))}
                    c = _colour(sd.get("stop-color", "#000000")) or "#00000000"
                    off = _num(s.get("offset"), 1, 0)
                    stops.append((min(1.0, max(0.0, off)),
                                  _with_alpha(c, _num(sd.get("stop-opacity"), 1, 1.0) * alpha)))
                break
        if not stops:
            return None
        stops.sort(key=lambda t: t[0])
        if len(stops) == 1:
            return stops[0][1]
        user = attr("gradientUnits") == "userSpaceOnUse"
        gm = _mul(m, _transform(attr("gradientTransform")))
        bx0, by0, bx1, by1 = bbox

        def pt(x, y):                                     # gradient coordinates -> scene
            if not user:
                x, y = bx0 + x * (bx1 - bx0), by0 + y * (by1 - by0)
            return _apply(gm, [(x, y)])[0]
        ref = 1.0 if not user else 100.0
        if _tag(chain[0]) == "linearGradient":
            a = pt(_num(attr("x1"), ref * (1 if not user else self.vw / 100), 0),
                   _num(attr("y1"), ref * (1 if not user else self.vh / 100), 0))
            b = pt(_num(attr("x2"), ref * (1 if not user else self.vw / 100), 1 if not user else self.vw),
                   _num(attr("y2"), ref * (1 if not user else self.vh / 100), 0))
            if abs(a[0] - b[0]) + abs(a[1] - b[1]) < 1e-6:
                return stops[-1][1]
            return lin(a, b, stops)
        cx = _num(attr("cx"), 1 if not user else self.vw, .5 if not user else self.vw / 2)
        cy = _num(attr("cy"), 1 if not user else self.vh, .5 if not user else self.vh / 2)
        r = _num(attr("r"), 1 if not user else math.hypot(self.vw, self.vh) / math.sqrt(2), .5)
        c = pt(cx, cy)
        edge = pt(cx + r, cy)
        edge2 = pt(cx, cy + r)
        rr = (math.dist(c, edge) + math.dist(c, edge2)) / 2
        return rad(c, max(rr, 1e-3), stops)

    def walk(self, el, m, parent_style: dict):
        tag = _tag(el)
        if tag in SKIP:
            return
        st = self.style(el, parent_style)
        if st.get("display") == "none":
            return
        m = _mul(m, _transform(el.get("transform")))
        if tag in ("g", "a", "switch") or (tag == "svg" and el is not self.root):
            if tag == "svg" and el is not self.root:
                m = _mul(m, (1, 0, 0, 1, _num(el.get("x")), _num(el.get("y"))))
            for ch in el:
                self.walk(ch, m, st)
            return
        if tag == "svg":
            for ch in el:
                self.walk(ch, m, st)
            return
        if tag == "use":
            ref = el.get("{http://www.w3.org/1999/xlink}href") or el.get("href") or ""
            target = self.ids.get(ref[1:]) if ref.startswith("#") else None
            if target is not None:
                tm = _mul(m, (1, 0, 0, 1, _num(el.get("x")), _num(el.get("y"))))
                if _tag(target) == "symbol":
                    for ch in target:
                        self.walk(ch, tm, st)
                else:
                    self.walk(target, tm, st)
            return
        if st.get("visibility") == "hidden":
            return
        self.shape(el, tag, m, st)

    def shape(self, el, tag, m, st):
        g = lambda k, ref=self.vw: _num(el.get(k), ref)  # noqa: E731
        closed = True
        if tag == "rect":
            x, y, w, h = g("x"), g("y", self.vh), g("width"), g("height", self.vh)
            if w <= 0 or h <= 0:
                return
            rx, ry = el.get("rx"), el.get("ry")
            rx = _num(rx if rx is not None else ry, self.vw)
            ry = _num(ry if ry is not None else el.get("rx"), self.vh)
            rx, ry = min(rx, w / 2), min(ry, h / 2)
            if rx > 0 and ry > 0:
                sub = path(f"M{x + rx} {y} H{x + w - rx} A{rx} {ry} 0 0 1 {x + w} {y + ry} V{y + h - ry} "
                           f"A{rx} {ry} 0 0 1 {x + w - rx} {y + h} H{x + rx} A{rx} {ry} 0 0 1 {x} {y + h - ry} "
                           f"V{y + ry} A{rx} {ry} 0 0 1 {x + rx} {y} Z")
            else:
                sub = rect(x, y, w, h)
        elif tag == "circle":
            r = g("r", math.hypot(self.vw, self.vh) / math.sqrt(2))
            if r <= 0:
                return
            sub = ellipse(g("cx"), g("cy", self.vh), r, r, n=72)
        elif tag == "ellipse":
            rx, ry = g("rx"), g("ry", self.vh)
            if rx <= 0 or ry <= 0:
                return
            sub = ellipse(g("cx"), g("cy", self.vh), rx, ry, n=72)
        elif tag == "line":
            sub, closed = [[(g("x1"), g("y1", self.vh)), (g("x2"), g("y2", self.vh))]], False
        elif tag in ("polyline", "polygon"):
            v = _nums(el.get("points"))
            sub = [list(zip(v[0::2], v[1::2]))]
            closed = tag == "polygon"
        elif tag == "path":
            d = el.get("d") or ""
            try:
                sub = path(d)
            except (ValueError, IndexError):
                return
            closed = "z" in d.lower()
        elif tag == "text":
            self.text(el, m, st)
            return
        else:
            return
        pts = [p for q in sub for p in q]
        if not pts:
            return
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        bbox = (min(xs), min(ys), max(xs), max(ys))
        shape = [_apply(m, q) for q in sub]
        op = st["_opacity"]
        ops = []
        fpaint = self.paint(st.get("fill", "#000000"), st, m, bbox, op * _num(st.get("fill-opacity"), 1, 1.0))
        if fpaint is not None and tag != "line":
            ops.append(fill(compound(shape) if len(shape) > 1 else shape, fpaint))
        spaint = self.paint(st.get("stroke"), st, m, bbox, op * _num(st.get("stroke-opacity"), 1, 1.0))
        sw = _num(st.get("stroke-width"), self.vw, 1.0) * _scale_of(m)
        if spaint is not None and sw > 0:
            ops.append(fill(stroke(shape, sw, closed=closed), spaint))
        if ops:
            sx = [p[0] for q in shape for p in q]
            sy = [p[1] for q in shape for p in q]
            label = el.get("id") or NAMES_AR.get(tag, tag)
            self.items.append((label, ops, ((min(sx) + max(sx)) / 2, (min(sy) + max(sy)) / 2),
                               (max(sx) - min(sx)) * (max(sy) - min(sy))))

    def text(self, el, m, st):
        s = "".join(el.itertext()).strip()
        if not s:
            return
        x, y = _num(el.get("x")), _num(el.get("y"))
        for ch in el:                                  # a first tspan often carries the position
            if _tag(ch) == "tspan" and el.get("x") is None:
                x, y = _num(ch.get("x")), _num(ch.get("y"))
                break
        (X, Y), = _apply(m, [(x, y)])
        size = _num(st.get("font-size"), 16, 16) * _scale_of(m)
        anchor = {"middle": "ms", "end": "rs"}.get(st.get("text-anchor", "start"), "ls")
        bold = str(st.get("font-weight", "")).lower() in ("bold", "bolder", "600", "700", "800", "900")
        paint = self.paint(st.get("fill", "#000000"), st, m, (x, y - size, x + size * len(s) * .6, y),
                           st["_opacity"] * _num(st.get("fill-opacity"), 1, 1.0))
        if paint is None:
            return
        if isinstance(paint, tuple):                   # gradient text: use its first stop
            paint = paint[3][0][1]
        self.items.append((el.get("id") or "نص: " + s[:18], [text(s, X, Y, size, paint, anchor, bold,
                                                                     st.get("font-family", "sans").lower())],
                           (X, Y - size / 3), size * size * len(s)))


def load_svg(source: str, max_steps: int = 160) -> tuple[str, list[Step]]:
    """SVG text -> (title, steps)."""
    root = ET.fromstring(re.sub(r"<!DOCTYPE[^>]*>", "", source.strip(), flags=re.S).encode("utf-8"))
    if _tag(root) != "svg":
        root = next((e for e in root.iter() if _tag(e) == "svg"), None)
        if root is None:
            raise ValueError("no <svg> element found")
    doc = _Svg(root)
    doc.walk(root, doc.fit, {"fill": "#000000"})
    title = next((e.text.strip() for e in root if _tag(e) == "title" and e.text), "SVG")
    vx, vy = _apply(doc.fit, [(doc.vx, doc.vy)])[0]
    vw, vh = doc.vw * doc.fit[0], doc.vh * doc.fit[3]
    steps = [Step("الخلفية", [fill(rect(0, 0, W0, H0), "#1b1822")], "sweep", weight=.5),
             Step("الورقة", [fill(rect(vx, vy, vw, vh), "#ffffff")], "sweep", weight=.6)]
    items = doc.items
    group = max(1, math.ceil(len(items) / max_steps))
    for k in range(0, len(items), group):
        chunk = items[k:k + group]
        ops = [o for it in chunk for o in it[1]]
        label = chunk[0][0] + (f" (+{len(chunk) - 1})" if len(chunk) > 1 else "")
        big = max(it[3] for it in chunk) > 0.45 * vw * vh
        steps.append(Step(label, ops, "sweep" if big else "grow", origin=chunk[0][2], weight=.7 if big else .45))
    return title, steps
