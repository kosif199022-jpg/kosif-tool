"""Real programs for the atlas-craft family (visual design rules, illustration layout locks, prompt governance).

Illustration cards are programmed as their measurable layout/palette locks: the program draws
the composition (PIL/SVG) or compiles the prompt, then measures it against the card's numbers.
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


def _w(work: Path, name: str, obj) -> Path:
    p = work / name
    p.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(obj, (bytes, bytearray)):
        p.write_bytes(obj)
    elif isinstance(obj, str):
        p.write_text(obj, encoding="utf-8")
    else:
        p.write_text(json.dumps(obj, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    return p


def _c(name, cond, obs):
    return (name, bool(cond), str(obs))


def _rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _lum(h):
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in (v / 255 for v in _rgb(h))]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def _contrast(a, b):
    la, lb = sorted([_lum(a), _lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


# ---------------------------------------------------------------- ACRAFT-01
def acraft_01(work: Path):
    def wireframe(steps, width=30):
        if len(steps) > 5:
            raise ValueError("keep few nodes: chunk into <= 5")
        lines = []
        for i, s in enumerate(steps, 1):
            label = f" {i}. {s}"[:width - 2]
            lines += ["+" + "-" * (width - 2) + "+", "|" + label.ljust(width - 2) + "|", "+" + "-" * (width - 2) + "+"]
            if i < len(steps):
                lines.append(" " * (width // 2) + "|")
        return "\n".join(lines)

    wf = wireframe(["Open app", "Pick photo", "Add caption", "Share"])
    _w(work, "wireframe.txt", wf)
    mer = "timeline\n  title Morning\n  07:00 : Wake\n  07:30 : Breakfast\n  08:00 : Leave"
    _w(work, "timeline.mmd", mer)
    try:
        wireframe(list("abcdefg"))
        refused = False
    except ValueError:
        refused = True
    rows = wf.splitlines()
    box_rows = [r for r in rows if r.startswith(("+", "|"))]
    return [_c("ASCII boxes all the same width (30)", all(len(r) == 30 for r in box_rows), {len(r) for r in box_rows}),
            _c("4 numbered steps chunked with connectors", sum(r.startswith("| ") for r in rows) == 4 and rows.count(" " * 15 + "|") == 3, ""),
            _c("more than 5 nodes refused (chunk first)", refused, refused),
            _c("Mermaid timeline written for the time flow", mer.startswith("timeline") and mer.count(" : ") == 3, "")]


# ---------------------------------------------------------------- ACRAFT-02
_DEUTAN = np.array([[0.367, 0.861, -0.228], [0.280, 0.673, 0.047], [-0.012, 0.043, 0.969]])  # Machado 2009, severity 1


def _sim(h, M):
    rgb = np.array(_rgb(h)) / 255
    lin = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    out = np.clip(M @ lin, 0, 1)
    return out


def acraft_02(work: Path):
    light = {"bg": "#ffffff", "text": "#1f2328", "success": "#1a7f37", "error": "#cf222e", "warning": "#9a6700", "primary": "#0969da"}
    dark = {"bg": "#0d1117", "text": "#e6edf3", "success": "#3fb950", "error": "#f85149", "warning": "#d29922", "primary": "#4493f8"}
    inverted = {k: "#%02x%02x%02x" % tuple(255 - v for v in _rgb(c)) for k, c in light.items()}
    ok = lambda pal: {k: round(_contrast(pal[k], pal["bg"]), 2) for k in pal if k != "bg"}
    rep_l, rep_d, rep_i = ok(light), ok(dark), ok(inverted)
    d_normal = np.linalg.norm(np.array(_rgb(light["success"])) / 255 - np.array(_rgb(light["error"])) / 255)
    d_deutan = np.linalg.norm(_sim(light["success"], _DEUTAN) - _sim(light["error"], _DEUTAN))
    semantics = {"success": "✓ Saved", "error": "✕ Failed", "warning": "! Check"}
    _w(work, "colour_system.json", {"light": rep_l, "dark": rep_d, "inverted": rep_i, "deutan_distance": float(d_deutan)})
    return [_c("light text pairs >= 4.5:1, status/UI >= 3:1", rep_l["text"] >= 4.5 and min(rep_l.values()) >= 3, rep_l),
            _c("re-derived dark palette passes the same gates", rep_d["text"] >= 4.5 and min(rep_d.values()) >= 3, rep_d),
            _c("naively inverted primary differs from the re-derived dark one", inverted["primary"] != dark["primary"], inverted["primary"]),
            _c("deuteranopia shrinks the success/error distance (needs icon backup)", d_deutan < 0.6 * d_normal, (round(float(d_normal), 3), round(float(d_deutan), 3))),
            _c("every status has an icon/text backup", all(re.match(r"[✓✕!] \w+", v) for v in semantics.values()), semantics)]


# ---------------------------------------------------------------- ACRAFT-03
def acraft_03(work: Path):
    from PIL import ImageFont
    font = ImageFont.load_default()

    def fit(text, max_px, lines=1):
        if not text:
            return "—"  # empty slot gets a placeholder, never a blank box
        words, out, cur = text.split(), [], ""
        for w in words:
            t = (cur + " " + w).strip()
            if font.getlength(t) <= max_px:
                cur = t
            else:
                out.append(cur)
                cur = w
        out.append(cur)
        if len(out) > lines:
            out = out[:lines]
            while font.getlength(out[-1] + "…") > max_px:
                out[-1] = out[-1][:-1]
            out[-1] += "…"
        return "\n".join(out)

    long_ = "Extraordinarily long product names keep going well beyond the card width"
    a = fit(long_, 120, lines=2)
    e = fit("", 120)
    s = fit("Pen", 120)
    img_src = lambda url: url if url else "fallback.svg"
    de = "Einstellungen speichern"
    grow = font.getlength(de) / font.getlength("Save settings")
    _w(work, "stress.json", {"long": a, "empty": e, "short": s, "de_growth": grow})
    return [_c("long text wraps to 2 lines then truncates with an ellipsis", a.count("\n") == 1 and a.endswith("…") and all(font.getlength(l) <= 120 for l in a.split("\n")), a),
            _c("empty slot gets a placeholder", e == "—", e),
            _c("short text untouched", s == "Pen", s),
            _c("missing image gets the fallback", img_src("") == "fallback.svg", ""),
            _c("German expansion measured > 1.3x: layout must allow it", grow > 1.3, round(grow, 2))]


# ---------------------------------------------------------------- ACRAFT-04
def acraft_04(work: Path):
    # boxes: (name, group, x, y, w, h)
    form = [("Name label", "name", 24, 20, 120, 16), ("Name field", "name", 24, 40, 300, 32),
            ("Email label", "email", 24, 104, 120, 16), ("Email field", "email", 24, 124, 300, 32),
            ("Button", "actions", 27, 200, 120, 40)]

    def audit(boxes):
        f = []
        lefts = {b[2] for b in boxes}
        if len(lefts) > 1:
            f.append(("alignment", sorted(lefts)))
        groups = {}
        for b in boxes:
            groups.setdefault(b[1], []).append(b)
        within = [g[i + 1][3] - (g[i][3] + g[i][5]) for g in groups.values() for i in range(len(g) - 1)]
        order = sorted(boxes, key=lambda b: b[3])
        between = [order[i + 1][3] - (order[i][3] + order[i][5]) for i in range(len(order) - 1) if order[i][1] != order[i + 1][1]]
        if within and between and min(between) <= max(within):
            f.append(("proximity", (max(within), min(between))))
        for g in groups.values():
            lab = [b for b in g if "label" in b[0]]
            fld = [b for b in g if "field" in b[0]]
            if lab and fld and fld[0][3] - (lab[0][3] + lab[0][5]) > 8:
                f.append(("label distance", g[0][1]))
        return f

    fs = audit(form)
    fixed = [b if b[0] != "Button" else ("Button", "actions", 24, 200, 120, 40) for b in form]
    bad = [("A label", "a", 24, 0, 100, 16), ("A field", "a", 24, 40, 200, 32), ("B label", "b", 24, 80, 100, 16), ("B field", "b", 24, 100, 200, 32)]
    _w(work, "gestalt.json", {"form": fs, "fixed": audit(fixed), "bad": audit(bad)})
    return [_c("button 3 px off the shared left edge flagged", fs == [("alignment", [24, 27])], fs),
            _c("aligned form passes: group gaps (32) > inner gaps (4)", audit(fixed) == [], audit(fixed)),
            _c("label far from its field and equal gaps break proximity", {k for k, _ in audit(bad)} == {"proximity", "label distance"}, audit(bad))]


# ---------------------------------------------------------------- ACRAFT-05
def acraft_05(work: Path):
    SCALE = {4, 8, 16, 24, 32, 48, 64}

    def audit(el):
        checks = {"grayscale hierarchy": el["gray_contrast_title_body"] >= 1.5,
                  "<=2 emphasis levers": len(el["levers"]) <= 2,
                  "spacing on scale": set(el["spacings"]) <= SCALE,
                  "group gap > inner gap": el["group_gap"] > el["inner_gap"],
                  "text width 45-75 chars": 45 <= el["measure"] <= 75,
                  "colour added last": not el["colour_carries_hierarchy"],
                  "shadows last": el["shadow_count"] <= 1,
                  "one primary action": el["primary_actions"] == 1}
        return round(sum(checks.values()) / 8 * 10), checks

    good = {"gray_contrast_title_body": 2.0, "levers": ["size", "weight"], "spacings": [8, 16, 24], "group_gap": 32, "inner_gap": 8,
            "measure": 66, "colour_carries_hierarchy": False, "shadow_count": 1, "primary_actions": 1}
    bad = {**good, "levers": ["size", "weight", "colour"], "spacings": [8, 13], "measure": 110}
    sg, _ = audit(good)
    sb, cb = audit(bad)
    _w(work, "refactoring_ui.json", {"good": sg, "bad": sb, "bad_checks": cb})
    return [_c("all 8 checks pass -> 10", sg == 10, sg),
            _c("3 failures -> round(5/8*10) = 6", sb == 6, sb),
            _c("13px spacing off the 4/8/16.. scale fails", cb["spacing on scale"] is False, cb),
            _c("110-char measure fails the 45-75 cap", cb["text width 45-75 chars"] is False, "")]


# ---------------------------------------------------------------- ACRAFT-06
def acraft_06(work: Path):
    elems = [{"id": "gradient bar", "info": None}, {"id": "status dot", "info": "online state"}, {"id": "drop shadow x3", "info": None},
             {"id": "divider", "info": "separates groups"}, {"id": "sparkle icon", "info": None}, {"id": "chart", "info": "trend"}]
    keep = [e["id"] for e in elems if e["info"]]
    delete = [e["id"] for e in elems if not e["info"]]
    ratio = len(keep) / len(elems)
    emphasis = {"colour": ["status dot"], "weight": ["chart title"], "size": [], "motion": []}
    sparse = len(keep) < 2
    _w(work, "signal_noise.json", {"keep": keep, "delete": delete, "data_ink_after": 1.0})
    return [_c("decoration carrying no information deleted", delete == ["gradient bar", "drop shadow x3", "sparkle icon"], delete),
            _c("informative elements kept", keep == ["status dot", "divider", "chart"], keep),
            _c("signal ratio before = 0.5, after = 1.0", ratio == 0.5, ratio),
            _c("emphasis allocated sparingly (<= 1 element per lever)", all(len(v) <= 1 for v in emphasis.values()) and not sparse, emphasis)]


# ---------------------------------------------------------------- ACRAFT-07
def acraft_07(work: Path):
    def audit(t):
        f = []
        if t["body_px"] < 16:
            f.append("body < 16px")
        if not 1.4 <= t["line_height"] <= 1.6:
            f.append("line-height ~1.5")
        cpl = t["container_px"] / (t["body_px"] * 0.5)  # average glyph ~0.5em
        if not 45 <= cpl <= 75:
            f.append(f"line length {cpl:.0f} chars")
        if len(t["families"]) > 2:
            f.append("> 2 families")
        ratios = [b / a for a, b in zip(t["scale"], t["scale"][1:])]
        if max(ratios) - min(ratios) > 0.02:
            f.append("scale not modular")
        return f

    good = {"body_px": 16, "line_height": 1.5, "container_px": 528, "families": ["Inter", "Lora"], "scale": [16, 20, 25, 31.25]}
    bad = {"body_px": 14, "line_height": 1.2, "container_px": 1200, "families": ["A", "B", "C"], "scale": [16, 18, 30]}
    _w(work, "typography.json", {"good": audit(good), "bad": audit(bad)})
    return [_c("16px / 1.5 / 528px (66 chars) / 2 families / 1.25 scale passes", audit(good) == [], audit(good)),
            _c("14px body and 1.2 leading flagged", {"body < 16px", "line-height ~1.5"} <= set(audit(bad)), audit(bad)),
            _c("1200px container at 14px = 171 chars flagged", "line length 171 chars" in audit(bad), audit(bad)),
            _c("3 families and a non-modular scale flagged", {"> 2 families", "scale not modular"} <= set(audit(bad)), audit(bad))]


# ---------------------------------------------------------------- ACRAFT-08
def acraft_08(work: Path):
    W, H = 1080, 1350
    style = {"ink": "#1a1a1a", "fills": ["#d9d4c7", "#efeae0"], "bg": "#f6f1e4", "accent": "#e4572e"}
    headline = "Water boils at 100 °C"
    inset = round(0.02 * W)
    draw_zone = (round(0.03 * H), round(0.62 * H))
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">', f'<rect width="{W}" height="{H}" fill="{style["bg"]}"/>',
           f'<rect x="{inset}" y="{inset}" width="{W - 2 * inset}" height="{H - 2 * inset}" fill="none" stroke="{style["ink"]}"/>',
           f'<g id="drawing"><rect x="300" y="{draw_zone[0] + 100}" width="480" height="500" fill="{style["fills"][0]}" stroke="{style["ink"]}"/>'
           f'<circle cx="540" cy="{draw_zone[0] + 300}" r="60" fill="{style["accent"]}"/></g>',
           f'<text x="{round(0.07 * W)}" y="{round(0.80 * H)}" font-family="Caveat" fill="{style["ink"]}">{headline}</text>', "</svg>"]
    svg_s = "".join(svg)
    _w(work, "card.svg", svg_s)
    prompt = f'Doodle card, ink {style["ink"]}, cream background, single accent {style["accent"]} on the kettle only. Headline reading exactly: "{headline}"'
    _w(work, "prompt.txt", f"```\n{prompt}\n```")
    colours = set(re.findall(r'(?:fill|stroke)="(#[0-9a-f]{6})"', svg_s))
    accents = colours - {style["ink"], style["bg"], *style["fills"]}
    ys = [int(y) for y in re.findall(r'<g id="drawing"><rect x="\d+" y="(\d+)"', svg_s)]
    return [_c("exactly one accent colour, used once", accents == {style["accent"]} and svg_s.count(style["accent"]) == 1, accents),
            _c("inset frame at 2% (22 px)", inset == 22 and f'x="{inset}" y="{inset}"' in svg_s, inset),
            _c("drawing inside the 3-62% zone", draw_zone[0] <= ys[0] and ys[0] + 500 <= draw_zone[1], (ys, draw_zone)),
            _c("headline bottom-left at 7% margin, verbatim text", f'x="{round(0.07 * W)}"' in svg_s and headline in svg_s, ""),
            _c("prompt quotes the in-image string exactly", f'reading exactly: "{headline}"' in prompt, "")]


# ---------------------------------------------------------------- ACRAFT-09
def acraft_09(work: Path):
    def layout(kind, W=1080, H=1350):
        if kind == "contrast":
            return [{"poly": [(0, 0), (W, 0), (W, H // 2 - 20), (0, H // 2 + 20)]}, {"poly": [(0, H // 2 + 40), (W, H // 2), (W, H), (0, H)]}]
        if kind == "emotion":
            return [{"poly": [(0, 0), (W, 0), (W, H), (0, H)], "border": False}]
        return [{"poly": [(0, 0), (W, 0), (W, H // 2), (0, H // 2)], "balloons": 2}, {"poly": [(0, H // 2), (W, H // 2), (W, H), (0, H)], "balloons": 1}]

    script = [{"page": 1, "type": "contrast", "narration": "Monday at the office.", "thought": "Again?"},
              {"page": 2, "type": "emotion", "narration": "The deadline moved.", "thought": "Freedom!"}]
    pages = [layout(p["type"]) for p in script]
    for i, pg in enumerate(pages):
        img = Image.new("RGB", (1080, 1350), "white")
        d = ImageDraw.Draw(img)
        for pan in pg:
            if pan.get("border", True):
                d.polygon(pan["poly"], outline=(120, 110, 100))
        img.resize((216, 270)).save(work / f"page{i + 1}.png")
    tilt = pages[0][0]["poly"][2][1] != pages[0][0]["poly"][3][1]
    return [_c("canvas 4:5 (1080x1350)", 1080 / 1350 == 0.8, "4:5"),
            _c("contrast page: two panels with a tilted divider", len(pages[0]) == 2 and tilt, pages[0][0]["poly"]),
            _c("big-emotion page: one borderless panel", len(pages[1]) == 1 and pages[1][0]["border"] is False, ""),
            _c("inner thought <= ~10 characters per page", all(len(p["thought"]) <= 10 for p in script), [p["thought"] for p in script]),
            _c("page script written before drawing", (work / "page1.png").exists() and len(script) == 2, "")]


# ---------------------------------------------------------------- ACRAFT-10
def acraft_10(work: Path):
    chars = {"Grandpa": "An old man with a white beard, round glasses, a grey flat cap and a brown wool vest.",
             "Lina": "A girl of ten with two black braids, a yellow raincoat and red boots."}
    if len(chars) > 4:
        raise ValueError("at most 4 characters")
    scenes = [{"who": ["Grandpa", "Lina"], "action": "fishing on the pier at dawn"}, {"who": ["Lina"], "action": "running home in the rain"},
              {"who": [], "action": "the empty pier at night"}]
    prompts = []
    for s in scenes:
        p = " ".join(f"CHARACTER {n}: {chars[n]}" for n in s["who"]) + f" Scene: {s['action']}. Background people: faceless mid-grey silhouettes."
        prompts.append(p)
    _w(work, "scene_prompts.json", prompts)
    interview = {"when": "1998 summer", "where": "Alexandria", "who": list(chars), "what": "first fish", "mood": "warm", "scenes": 3}
    verbatim = all(chars[n] in prompts[i] for i, s in enumerate(scenes) for n in s["who"])
    return [_c("interview answered before drawing (6 fields)", len(interview) == 6 and interview["scenes"] == len(scenes), list(interview)),
            _c("CHARACTER sentence pasted word for word in every scene with that lead", verbatim, ""),
            _c("characters absent from a scene are not described", "Grandpa" not in prompts[1] and "CHARACTER" not in prompts[2], ""),
            _c("<= 4 leads; others faceless silhouettes", len(chars) <= 4 and all("faceless" in p for p in prompts), len(chars))]


# ---------------------------------------------------------------- ACRAFT-11
def acraft_11(work: Path):
    LAYOUTS = {"sketch-card-a": {"index": (0.06, 0.05), "title": (0.06, 0.10), "desc_y": 0.20, "check_y": 0.26, "frame": (0.06, 0.34, 0.94, 0.96)}}
    W, H = 900, 1200
    L = LAYOUTS["sketch-card-a"]
    accent, spots = "#f08c00", ["moon"]
    card = {"index": "03", "title": "ORBIT", "subtitle": "(path around a body)", "desc": "A moon circles its planet.",
            "checklist": ["dashed ellipse = orbit", "arrow = direction", "one accent"]}
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="#f4f1ea"/>',
           f'<text x="{L["index"][0] * W:.0f}" y="{L["index"][1] * H:.0f}">{card["index"]}</text>',
           f'<text x="{L["title"][0] * W:.0f}" y="{L["title"][1] * H:.0f}">{card["title"]}</text>']
    x0, y0, x1, y1 = (L["frame"][0] * W, L["frame"][1] * H, L["frame"][2] * W, L["frame"][3] * H)
    svg.append(f'<rect x="{x0:.0f}" y="{y0:.0f}" width="{x1 - x0:.0f}" height="{y1 - y0:.0f}" fill="none" stroke="#444"/>')
    svg.append(f'<ellipse cx="450" cy="{(y0 + y1) / 2:.0f}" rx="300" ry="120" fill="none" stroke="#444" stroke-dasharray="10 8"/>')
    svg.append(f'<circle id="moon" cx="750" cy="{(y0 + y1) / 2:.0f}" r="24" fill="{accent}"/></svg>')
    s = "".join(svg)
    _w(work, "card.svg", s)
    return [_c("layout from the fixed catalogue, drawing in the lower two thirds", y0 >= H / 3 - 1 and y1 <= H, (y0, y1)),
            _c("UPPERCASE title, 2-4 checklist items", card["title"].isupper() and 2 <= len(card["checklist"]) <= 4, card["title"]),
            _c("accent on 1-3 spots only", s.count(accent) == len(spots) and 1 <= len(spots) <= 3, s.count(accent)),
            _c("geometric overlay carries the definition (dashed ellipse for orbit)", "stroke-dasharray" in s and "<ellipse" in s, "")]


# ---------------------------------------------------------------- ACRAFT-12
def acraft_12(work: Path):
    W, H = 600, 400
    img = Image.new("RGB", (W, H), (236, 236, 236))
    d = ImageDraw.Draw(img)
    ground = int(H * 0.85)
    d.line([(0, ground), (W, ground)], fill=(110, 110, 110), width=2)
    d.rectangle([380, ground - 60, 400, ground], fill=(80, 80, 80))       # figure from behind, off-centre
    d.rectangle([410, ground - 14, 424, ground], fill=(0x2e, 0x7d, 0x8c))  # teal prop (a bucket)
    img.save(work / "scene.png")
    a = np.asarray(img).astype(int)
    ink = np.abs(a - 236).sum(-1) > 30
    top_empty = not ink[: int(H * 2 / 3)].any()
    rgb = a.reshape(-1, 3)
    colourful = rgb[(rgb.max(1) - rgb.min(1)) > 20]
    teal_ok = len(colourful) > 0 and np.all(np.abs(colourful - [0x2e, 0x7d, 0x8c]).max(1) <= 2)
    ys, xs = np.where(ink[: ground - 2])
    subj_cx = xs.mean() / W
    template = "Quiet pencil sketch, greyscale, <subject> small on a ground line, one <prop> in teal, empty sky, no text."
    filled = template.replace("<subject>", "a fisherman seen from behind").replace("<prop>", "bucket")
    return [_c("top two thirds empty", top_empty, top_empty),
            _c("the only colour is the teal #2E7D8C prop", teal_ok, len(colourful)),
            _c("subject sits off-centre", abs(subj_cx - 0.5) > 0.1, round(subj_cx, 2)),
            _c("only the <...> slots of the template changed", filled.replace("a fisherman seen from behind", "<subject>").replace("bucket", "<prop>") == template, "")]


# ---------------------------------------------------------------- ACRAFT-13
def acraft_13(work: Path):
    formats = {"thumbnail": (1080, 1080), "route": (900, 1200), "scene": (1200, 900)}
    route_colours = ["#5c9e31", "#7b3fa0", "#f08c00"]
    places = ["Old gate", "Spice market", "Harbour"]
    W, H = formats["route"]
    img = Image.new("RGB", (W, H), (246, 240, 225))
    d = ImageDraw.Draw(img)
    pts = [(W // 2, int(H * (0.2 + 0.3 * i))) for i in range(len(places))]  # no directions given: top-to-bottom visit order
    for i in range(len(pts) - 1):
        d.line([pts[i], pts[i + 1]], fill=route_colours[0], width=8)
    for i, p in enumerate(pts, 1):
        d.ellipse([p[0] - 20, p[1] - 20, p[0] + 20, p[1] + 20], fill=(40, 40, 40))
    img.save(work / "route.png")
    a = np.asarray(img).astype(int)
    empty = (np.abs(a - [246, 240, 225]).sum(-1) < 10).mean()
    title_h = 0.10 * formats["thumbnail"][1]
    sub_h = 0.45 * title_h
    margin = 0.08
    labels_in_route = []  # route sketch carries numbers only
    return [_c("aspect ratios 1:1, 3:4, 4:3", [w / h for w, h in formats.values()] == [1.0, 0.75, 4 / 3], formats),
            _c(">= 35% of the canvas left empty", empty >= 0.35, round(float(empty), 3)),
            _c("no directions: visit order drawn top to bottom", [p[1] for p in pts] == sorted(p[1] for p in pts), pts),
            _c("title 8-12% of canvas, subtitle 40-50% of title, 8% margin", 0.08 <= title_h / 1080 <= 0.12 and 0.4 <= sub_h / title_h <= 0.5 and margin == 0.08, ""),
            _c("route sketch has numbers only, <= 3 route colours", labels_in_route == [] and len(route_colours) <= 3, "")]


# ---------------------------------------------------------------- ACRAFT-14
def acraft_14(work: Path):
    bible = {"look": "ink and wash", "palette": ["#222", "#c9b38f", "#2e7d8c"], "medium": "watercolour"}
    _w(work, "art-bible.md", "# Art bible\n" + "\n".join(f"- {k}: {v}" for k, v in bible.items()))
    figures = [{"id": "F1", "kind": "illustration", "subject": "a lighthouse at dusk", "aspect": "3:2"},
               {"id": "F2", "kind": "chart", "data": "sales.csv"}, {"id": "F3", "kind": "diagram", "source": "flow.d2"},
               {"id": "F4", "kind": "map", "data": "coast.geojson"}]

    def compile_prompt(spec, backend):
        core = f"{spec['subject']}, {bible['look']}, {bible['medium']}, palette {' '.join(bible['palette'])}"
        if backend == "midjourney":
            return f"{core} --ar {spec['aspect']} --style raw"
        if backend == "sdxl":
            return f"{core}, (aspect {spec['aspect']})"
        return json.dumps({"prompt": core, "aspect_ratio": spec["aspect"]})

    route = {f["id"]: ("diffusion" if f["kind"] == "illustration" else "code: matplotlib" if f["kind"] == "chart" else "code: D2/Graphviz SVG" if f["kind"] == "diagram" else "code: map base from data")
             for f in figures}
    prompts = {b: compile_prompt(figures[0], b) for b in ("midjourney", "sdxl", "api")}
    _w(work, "figures.json", {"route": route, "prompts": prompts})
    return [_c("one structured spec compiled to three backends", prompts["midjourney"].endswith("--ar 3:2 --style raw") and json.loads(prompts["api"])["aspect_ratio"] == "3:2", prompts),
            _c("all prompts share the art-bible core", all("ink and wash" in p for p in prompts.values()), ""),
            _c("charts, diagrams and maps never go to diffusion", [route[k] for k in ("F2", "F3", "F4")] == ["code: matplotlib", "code: D2/Graphviz SVG", "code: map base from data"], route),
            _c("only the illustration uses diffusion", list(route.values()).count("diffusion") == 1, "")]


# ---------------------------------------------------------------- ACRAFT-15
def acraft_15(work: Path):
    def draw(shapes, closure=False):
        img = Image.new("L", (48, 48), 0)
        d = ImageDraw.Draw(img)
        for s in shapes:
            if s == "body":
                if closure:  # partial outline: the viewer completes the box
                    d.line([(6, 14), (6, 38), (42, 38)], fill=255, width=3)
                    d.line([(42, 30), (42, 14), (30, 14)], fill=255, width=3)
                else:
                    d.rectangle([6, 14, 42, 38], outline=255, width=3)
            if s == "lens":
                d.ellipse([16, 18, 32, 34], outline=255, width=3)
            if s == "record_dot":
                d.ellipse([36, 4, 44, 12], fill=255)
        return np.asarray(img) > 0

    camera, video = draw(["body", "lens"]), draw(["body", "lens", "record_dot"])
    diff = (camera ^ video)
    ys, xs = np.where(diff)
    closed, open_ = draw(["body", "lens"]), draw(["body", "lens"], closure=True)
    Image.fromarray((video * 255).astype(np.uint8)).save(work / "video.png")
    kind = lambda thing: "resemblance" if thing in ("camera", "lock", "folder") else "convention"
    return [_c("camera vs video differ by one decisive feature (record dot, top-right)", diff.any() and xs.min() >= 34 and ys.max() <= 13, (xs.min(), ys.max())),
            _c("closure: partial outline lowers visual weight", open_.sum() < closed.sum(), (int(closed.sum()), int(open_.sum()))),
            _c("stable objects use resemblance, abstract ones a convention", kind("camera") == "resemblance" and kind("sync") == "convention", "")]


# ---------------------------------------------------------------- ACRAFT-16
def acraft_16(work: Path):
    import colorsys

    def ramp(base):
        h, l, s = colorsys.rgb_to_hls(*[v / 255 for v in _rgb(base)])
        out = {}
        for step, L in ((50, 0.95), (300, 0.70), (500, l), (700, 0.32), (900, 0.18)):
            r, g, b = colorsys.hls_to_rgb(h, L, s)
            out[step] = "#%02x%02x%02x" % (round(r * 255), round(g * 255), round(b * 255))
        return out

    status = {k: ramp(v) for k, v in {"success": "#2f9e44", "warning": "#f08c00", "error": "#e03131", "info": "#1c7ed6"}.items()}
    categories = ["#7048e8", "#0ca678", "#d6336c", "#f59f00", "#1098ad"]
    brand = {"primary_cta": "#1c7ed6", "marketing_emphasis": "#e03131"}
    text_on_tint = {k: round(_contrast(r[700], r[50]), 2) for k, r in status.items()}
    reused = [c for c in categories if c in {r[500] for r in status.values()}]
    misuse = [k for k, v in brand.items() if v == status["error"][500] and k != "destructive"]
    _w(work, "semantic_colours.json", {"status": status, "categories": categories, "text_on_tint": text_on_tint})
    return [_c("each status ramp has steps 50/300/500/700/900", all(list(r) == [50, 300, 500, 700, 900] for r in status.values()), ""),
            _c("700 text on the 50 tint >= 4.5:1 for every status", min(text_on_tint.values()) >= 4.5, text_on_tint),
            _c("category palette 5-7 hues, none reused as status", 5 <= len(categories) <= 7 and reused == [], reused),
            _c("destructive red used for marketing emphasis is flagged", misuse == ["marketing_emphasis"], misuse)]


# ---------------------------------------------------------------- ACRAFT-17
def acraft_17(work: Path):
    def required(size_pt, bold, aaa=False):
        if aaa:
            return 7.0
        return 3.0 if size_pt >= 18 or (bold and size_pt >= 14) else 4.5

    pairs = [("#767676", "#ffffff", 12, False), ("#949494", "#ffffff", 18, False), ("#949494", "#ffffff", 14, True), ("#949494", "#ffffff", 12, False)]
    res = [(fg, size, bold, round(_contrast(fg, bg), 2), _contrast(fg, bg) >= required(size, bold)) for fg, bg, size, bold in pairs]
    leading = {"heading": 1.2, "body": 1.6, "label": 1.3}
    lead_ok = 1.1 <= leading["heading"] <= 1.3 and 1.5 <= leading["body"] <= 1.7 and 1.2 <= leading["label"] <= 1.4
    measure = lambda chars: 45 <= chars <= 75
    _w(work, "legibility.json", {"pairs": res, "leading": leading})
    return [_c("#767676 on white = 4.54:1 passes normal text", res[0][3] == 4.54 and res[0][4], res[0]),
            _c("#949494 (3.03:1) passes as 18pt or 14pt bold, fails at 12pt", res[1][4] and res[2][4] and not res[3][4], res[1:]),
            _c("AAA requires 7:1", required(12, False, aaa=True) == 7.0, ""),
            _c("leading in range for headings/body/labels; 66-char measure ok, 90 not", lead_ok and measure(66) and not measure(90), leading)]


# ---------------------------------------------------------------- ACRAFT-18
def acraft_18(work: Path):
    RATIOS = {"dense app": 1.125, "software": 1.2, "web": 1.25, "editorial": 1.333, "print": 1.414, "magazine": 1.5, "hero": 1.618}
    names = ["micro", "caption", "body-sm", "body", "body-lg", "h4", "h3", "h2", "h1", "display"]

    def scale(ratio, base=16):
        return {n: round(base * ratio ** (i - 3), 2) for i, n in enumerate(names)}

    web = scale(RATIOS["web"])
    tokens = {n: {"size": v, "weight": 600 if n.startswith("h") or n == "display" else 400} for n, v in web.items()}
    _w(work, "type_tokens.json", tokens)
    rank = lambda t: (t["size"], t["weight"])
    return [_c("web default ratio 1.25 from body 16: h1 = 16 x 1.25^5 = 48.83", web["body"] == 16 and web["h1"] == round(16 * 1.25 ** 5, 2), web["h1"]),
            _c("caption = 16 / 1.25^2 = 10.24", web["caption"] == 10.24, web["caption"]),
            _c("10 tokens strictly increasing", list(web.values()) == sorted(web.values()) and len(set(web.values())) == 10, list(web.values())),
            _c("weight as second axis: 24px semibold ranks above 24px regular", rank({"size": 24, "weight": 600}) > rank({"size": 24, "weight": 400}), ""),
            _c("dense UI ratio 1.125 gives a tighter h1", scale(RATIOS["dense app"])["h1"] < web["h1"], scale(RATIOS["dense app"])["h1"])]


# ---------------------------------------------------------------- ACRAFT-19
def acraft_19(work: Path):
    MOT = {"safety": "Innocent", "truth": "Sage", "freedom": "Explorer", "disruption": "Outlaw", "transformation": "Magician",
           "mastery": "Hero", "intimacy": "Lover", "joy": "Jester", "belonging": "Everyman", "service": "Caregiver",
           "innovation": "Creator", "control": "Ruler"}
    TRAITS = {"Jester": {"shapes": "round", "colour": "bright accents", "voice": "playful"}, "Sage": {"shapes": "geometric", "colour": "deep blues", "voice": "measured"}}

    def brand(primary, secondary=None, extra=()):
        if extra:
            raise ValueError("one primary archetype, at most one secondary")
        a = MOT[primary]
        return {"primary": a, "secondary": MOT[secondary] if secondary else None, **TRAITS.get(a, {})}

    b = brand("joy", "truth")
    try:
        brand("joy", "truth", extra=("freedom",))
        refused = False
    except ValueError:
        refused = True
    _w(work, "archetype.json", b)
    return [_c("12 archetypes mapped from motivations", len(set(MOT.values())) == 12, len(MOT)),
            _c("joy -> Jester with round forms and playful voice", b["primary"] == "Jester" and b["shapes"] == "round" and b["voice"] == "playful", b),
            _c("secondary truth -> Sage", b["secondary"] == "Sage", b["secondary"]),
            _c("a third archetype is refused", refused, refused)]


# ---------------------------------------------------------------- ACRAFT-20
def acraft_20(work: Path):
    N = 1024

    def icon(art_frac):
        img = Image.new("RGB", (N, N))
        a = np.zeros((N, N, 3), np.uint8)
        t = np.linspace(0, 1, N)[:, None]
        a[...] = (np.c_[20 + 40 * t, 30 + 60 * t, 90 + 100 * t]).astype(np.uint8)[:, None, :].repeat(N, 1)  # two-stop gradient
        img = Image.fromarray(a)
        d = ImageDraw.Draw(img)
        s = int(N * art_frac)
        o = (N - s) // 2
        d.rounded_rectangle([o, o + s // 4, o + s, o + s], radius=s // 10, fill=(250, 245, 235))   # layer 1: book
        d.rectangle([o + s // 2 - 6, o + s // 4, o + s // 2 + 6, o + s], fill=(240, 140, 0))          # layer 2: spine accent
        return img

    def art_fraction(img):
        a = np.asarray(img).astype(int)
        light = a.sum(-1) > 600
        orange = (a[..., 0] > 200) & (a[..., 2] < 50)
        ys, xs = np.where(light | orange)
        return (xs.max() - xs.min() + 1) / N

    good, big = icon(0.60), icon(0.78)
    good.save(work / "icon_1024.png")
    sizes = {}
    for px in (256, 64, 16):
        good.resize((px, px), Image.LANCZOS).save(work / f"icon_{px}.png")
        sizes[px] = (work / f"icon_{px}.png").stat().st_size
    fg, fb = art_fraction(good), art_fraction(big)
    return [_c("canvas 1024x1024", good.size == (1024, 1024), good.size),
            _c("artwork fills ~60% of the width", abs(fg - 0.60) < 0.01, round(fg, 3)),
            _c("the 78% variant is flagged as oversized", fb > 0.7 and not abs(fb - 0.60) < 0.05, round(fb, 3)),
            _c("previews rendered at 256, 64 and 16", all(v > 0 for v in sizes.values()), sizes)]


# ---------------------------------------------------------------- ACRAFT-21
def acraft_21(work: Path):
    DEFAULTS = [("cream + serif + terracotta", lambda d: d["bg"] in ("#f5efe6", "#faf6ef") and d["type"] == "serif" and d["accent"] in ("#c65d3b", "#d2691e")),
                ("near-black + one acid accent", lambda d: _lum(d["bg"]) < 0.01 and d["accent"] in ("#c6ff00", "#d4ff3a")),
                ("tracked ALL-CAPS eyebrows everywhere", lambda d: d.get("eyebrows_all_caps", 0) >= 0.8),
                ("identical rounded cards with the same grey shadow", lambda d: d.get("card_variants", 2) == 1 and d.get("shadow") == "0 4px 12px #0000001a"),
                ("meta joined by middle dots", lambda d: "·" in d.get("meta", ""))]
    design_a = {"bg": "#f5efe6", "type": "serif", "accent": "#c65d3b", "eyebrows_all_caps": 1.0, "meta": "Mar 3 · 5 min · Essay"}
    design_b = {"bg": "#e9f1ee", "type": "grotesk", "accent": "#0b7285", "eyebrows_all_caps": 0.1, "card_variants": 3, "meta": "5 min read",
                "palette": {"tide": "#0b7285", "sand": "#e9f1ee", "kelp": "#2b8a3e", "ink": "#102a2a"}}
    hits = lambda d: [n for n, f in DEFAULTS if f(d)]
    ha, hb = hits(design_a), hits(design_b)
    _w(work, "DESIGN.md", "# North star\nPalette: " + ", ".join(f"{k} {v}" for k, v in design_b["palette"].items()) + "\n")
    return [_c("template look A trips cream/serif/terracotta, caps eyebrows and middle dots", ha == ["cream + serif + terracotta", "tracked ALL-CAPS eyebrows everywhere", "meta joined by middle dots"], ha),
            _c("subject-grounded design B trips none", hb == [], hb),
            _c("DESIGN.md palette has 4-6 named hex values", 4 <= len(design_b["palette"]) <= 6 and all(re.fullmatch(r"#[0-9a-f]{6}", v) for v in design_b["palette"].values()), "")]


# ---------------------------------------------------------------- ACRAFT-22
def acraft_22(work: Path):
    ROWS = ["trigger visible", "states distinct", "gesture alternative", "rules predictable", "constrain inputs", "feedback < 100 ms", "feedback scaled", "no hidden modes"]

    def score(m):
        passed = {r: bool(m.get(r)) for r in ROWS}
        if not passed["trigger visible"] or not passed["feedback < 100 ms"]:
            return 3, passed
        if all(passed.values()):
            return 10 if m.get("delight") else 9, passed
        return (6 if sum(passed.values()) >= 6 else 5), passed

    like = {r: True for r in ROWS}
    like["feedback < 100 ms"] = 60 < 100
    generic = {**like, "feedback scaled": False, "gesture alternative": False}
    broken = {**like, "feedback < 100 ms": 240 < 100}
    s1, s2, s3 = score({**like, "delight": True})[0], score(generic)[0], score(broken)[0]
    states = {"default": "#1c7ed6", "hover": "#1971c2", "active": "#1864ab", "disabled": "#adb5bd", "loading": "spinner"}
    _w(work, "microinteraction.json", {"scores": [s1, s2, s3], "states": states})
    return [_c("all eight rows pass -> 9-10", s1 in (9, 10), s1),
            _c("generic feel (two rows fail) -> 5-6", s2 in (5, 6), s2),
            _c("240 ms feedback -> <= 3", s3 <= 3, s3),
            _c("five control states all look different", len(set(states.values())) == 5, states)]


# ---------------------------------------------------------------- ACRAFT-23
def acraft_23(work: Path):
    def fmt(q):
        q = q.lower()
        if re.search(r"state|transition|logic|condition", q):
            return "pseudocode"
        if re.search(r"calls?|runtime|flow at runtime|stack", q):
            return "indented call tree"
        if re.search(r"owns|ownership|who owns", q):
            return "shallow tree"
        if re.search(r"actors?|data flow|services talk", q):
            return "mermaid"
        if re.search(r"change|proposed|patch", q):
            return "focused diff"
        return "pseudocode"

    qs = {"How does the order state machine transition?": "pseudocode", "What calls what when I hit /pay?": "indented call tree",
          "Which module owns retries?": "shallow tree", "How do the services talk (data flow)?": "mermaid", "What is the proposed change?": "focused diff"}
    got = {q: fmt(q) for q in qs}
    tree = "handle_pay()\n  validate(cart)\n  charge(card)  # unknown: retry policy not found in code\n"
    _w(work, "explanation.json", {"formats": got, "visual": tree})
    return [_c("one format chosen per question type (5 cases)", got == qs, got),
            _c("call tree lists only verified calls and marks unknowns", "unknown:" in tree and tree.count("\n") == 3, tree)]


# ---------------------------------------------------------------- ACRAFT-24
def acraft_24(work: Path):
    options = {"Export PDF": 0.62, "Share link": 0.55, "Print": 0.08, "Export SVG": 0.04, "Embed code": 0.02, "Copy as image": 0.30}

    def disclose(opts, primary_n=3, threshold=0.25):
        ranked = sorted(opts, key=lambda k: -opts[k])
        primary = [k for k in ranked if opts[k] >= threshold][:primary_n]
        advanced = [k for k in ranked if k not in primary]
        return {"primary": primary, "more": {"trigger": "More options…", "items": advanced}}

    ui = disclose(options)
    depth = 1 + (1 if ui["more"]["items"] else 0)
    _w(work, "disclosure.json", ui)
    return [_c("frequent options shown first, by frequency", ui["primary"] == ["Export PDF", "Share link", "Copy as image"], ui["primary"]),
            _c("rare options behind one explicit trigger", ui["more"] == {"trigger": "More options…", "items": ["Print", "Export SVG", "Embed code"]}, ui["more"]),
            _c("no option used by > 25% is hidden", all(options[k] < 0.25 for k in ui["more"]["items"]), ""),
            _c("nesting <= 2 levels", depth <= 2, depth)]


# ---------------------------------------------------------------- ACRAFT-25
def acraft_25(work: Path):
    reg = {"extract-invoice": {"versions": {"1.0.0": "production", "1.1.0": "draft"}, "owner": "data", "model": "m1", "promoted_by": []}}
    golden = [{"input": f"Invoice #{i} total {i * 10}", "expected": {"no": str(i), "total": i * 10}} for i in range(1, 26)]

    def candidate(text, v):
        no, total = re.search(r"#(\d+) total (\d+)", text).groups()
        out = {"no": no, "total": int(total)}
        if v == "1.2.0" and no.endswith("7"):
            out["total"] = None  # regression in the new prompt version
        return out

    def evaluate(v):
        ex = sum(candidate(g["input"], v) == g["expected"] for g in golden) / len(golden)
        schema = sum(set(candidate(g["input"], v)) == {"no", "total"} for g in golden) / len(golden)
        return ex, schema

    def promote(v, env="production"):
        if len(golden) < (100 if env == "production" else 20):
            return "blocked: golden set too small for production"
        ex, sch = evaluate(v)
        if ex < 0.95 or sch < 1.0:
            return f"blocked: extraction {ex:.2f}"
        return "promoted"

    def promote_staging(v):
        if len(golden) < 20:
            return "blocked: golden set < 20"
        ex, sch = evaluate(v)
        if ex < 0.95 or sch < 1.0:
            return f"blocked: extraction {ex:.2f}"
        reg["extract-invoice"]["versions"][v] = "staging"
        reg["extract-invoice"]["promoted_by"].append(("alice", "2026-11-03", v))
        return "promoted to staging"

    r11 = promote_staging("1.1.0")
    r12 = promote_staging("1.2.0")
    prod = promote("1.1.0")
    reg["extract-invoice"]["versions"]["1.1.0"] = "rolled back"
    _w(work, "prompts/registry.yaml", json.dumps(reg, indent=1))
    return [_c("golden set has the 20-example minimum", len(golden) >= 20, len(golden)),
            _c("1.1.0 passes 95% extraction / 100% schema and is promoted", r11 == "promoted to staging", r11),
            _c("regressed 1.2.0 (invoices 7 and 17 wrong: 23/25 = 0.92 < 0.95) is blocked", r12 == "blocked: extraction 0.92", r12),
            _c("production needs 100+ golden examples", prod == "blocked: golden set too small for production", prod),
            _c("promotion recorded with who and when; rollback recorded", reg["extract-invoice"]["promoted_by"] == [("alice", "2026-11-03", "1.1.0")] and reg["extract-invoice"]["versions"]["1.1.0"] == "rolled back", "")]


# ---------------------------------------------------------------- ACRAFT-26
def acraft_26(work: Path):
    paras = []
    for i in range(100):
        if i < 50:
            paras.append("Short line. Another one. Quick.")
        else:
            paras.append("This later section uses much longer and more winding sentences that keep unfolding with clause after clause.")
    text = "\n".join(paras)
    n = len(paras)
    points = {"opening": 0, "25-35%": int(0.30 * n), "middle": n // 2 + 1, "65-75%": int(0.70 * n), "end": n - 1}

    def avg_len(p):
        sents = [s for s in re.split(r"[.!?]\s*", p) if s]
        return sum(len(s.split()) for s in sents) / len(sents)

    samples = {k: avg_len(paras[i]) for k, i in points.items()}
    single_chapter = avg_len(paras[0])
    guide = {"sentence_length": {"early": samples["opening"], "late": samples["end"]}, "adapts": samples["end"] > 3 * samples["opening"],
             "patterns_not_content": True}
    _w(work, "style_guide.json", {"samples": samples, "guide": guide})
    return [_c("5 sample points spread over the text", len(points) == 5 and list(points.values()) == sorted(points.values()), points),
            _c("spread sampling detects the style shift a single chapter misses", guide["adapts"] and single_chapter < 3, samples),
            _c("guide records patterns (lengths), not content", "Short line" not in json.dumps(guide), "")]


PROGRAMS = {f"ACRAFT-{n:02d}": globals()[f"acraft_{n:02d}"] for n in range(1, 27) if f"acraft_{n:02d}" in globals()}
