"""Programs for the apps-artifacts family: page contracts, linters and models built and checked offline."""
from __future__ import annotations
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup


def _w(work: Path, name: str, text: str) -> Path:
    p = work / name
    p.write_text(text, encoding="utf-8")
    return p


def _lum(hexc: str) -> float:
    h = hexc.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * out[0] + 0.7152 * out[1] + 0.0722 * out[2]


def contrast(a: str, b: str) -> float:
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return round((la + 0.05) / (lb + 0.05), 2)


# ---------------------------------------------------------------- APP-01
ALLOWED_CDN = ("cdnjs.cloudflare.com", "cdn.jsdelivr.net/npm/", "unpkg.com", "cdn.tailwindcss.com", "code.jquery.com")


def artifact_contract(html: str, size_limit=16 * 1024 * 1024) -> list:
    """Return the list of contract violations of one page (empty = publishable)."""
    soup = BeautifulSoup(html, "html.parser")
    bad = []
    title = (soup.title.string or "").strip() if soup.title else ""
    if not 2 <= len(title.split()) <= 4:
        bad.append(f"title words {len(title.split())}")
    css = " ".join(s.get_text() for s in soup.find_all("style"))
    if ":root" not in css:
        bad.append("no :root tokens")
    if ':root:not([data-theme="light"])' not in css.replace("'", '"') or ':root[data-theme="dark"]' not in css.replace("'", '"'):
        bad.append("dark override not guarded")
    if not re.search(r"body\s*{[^}]*background", css):
        bad.append("no body background")
    for s in soup.find_all("script", src=True):
        src = s["src"]
        if not any(h in src for h in ALLOWED_CDN):
            bad.append(f"script host {src}")
        elif not re.search(r"@\d+\.\d+\.\d+", src) and not re.search(r"/\d+\.\d+\.\d+/", src):
            bad.append(f"inexact version {src}")
    if len(html.encode()) > size_limit:
        bad.append("over 16 MB")
    return bad


def app_01(work):
    css = (':root{--bg:#fff;--fg:#111}@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#111;--fg:#eee}}'
           ':root[data-theme="dark"]{--bg:#111;--fg:#eee}body{background:var(--bg);color:var(--fg);padding:0 16px}')
    good = (f'<!doctype html><html><head><title>Sales Weekly Board</title><style>{css}</style>'
            '<script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.3.1/umd/react.production.min.js"></script>'
            '</head><body><p>hi</p></body></html>')
    bad = good.replace("Sales Weekly Board", "My Long Sales Weekly Board Page").replace(
        "cdnjs.cloudflare.com/ajax/libs/react/18.3.1/umd/react.production.min.js", "unpkg.com/react@18")
    _w(work, "good.html", good)
    _w(work, "bad.html", bad)
    vg, vb = artifact_contract(good), artifact_contract(bad)
    big = artifact_contract(good, size_limit=100)
    return [("compliant page has no violations", vg == [], vg),
            ("6-word title rejected", any(v.startswith("title words 6") for v in vb), vb),
            ("react@18 floating version rejected", any("inexact version" in v for v in vb), vb),
            ("size limit enforced", "over 16 MB" in big, big)]


# ---------------------------------------------------------------- APP-02
def storage_choice(item: dict) -> str:
    return "db" if item.get("shared") or item.get("must_persist") else "localStorage"


def unguarded_localstorage(js: str) -> int:
    """Count localStorage uses that are not inside a try { } block."""
    count, depth_try = 0, []
    tokens = re.finditer(r"try\s*{|{|}|localStorage", js)
    for m in tokens:
        t = m.group(0)
        if t.startswith("try"):
            depth_try.append(True)
        elif t == "{":
            depth_try.append(False)
        elif t == "}":
            if depth_try:
                depth_try.pop()
        elif not any(depth_try):
            count += 1
    return count


def app_02(work):
    items = [{"name": "poll votes", "shared": True}, {"name": "sign-ups", "must_persist": True},
             {"name": "collapsed panel"}, {"name": "remembered tab"}]
    plan = {i["name"]: storage_choice(i) for i in items}
    js_ok = "function load(){try{return localStorage.getItem('tab')}catch(e){return null}}"
    js_bad = "function load(){return localStorage.getItem('tab')}"
    _w(work, "storage_plan.json", json.dumps(plan, indent=1))
    return [("shared votes go to db", plan["poll votes"] == "db", plan),
            ("must-persist sign-ups go to db", plan["sign-ups"] == "db", plan),
            ("per-viewer conveniences stay in localStorage",
             plan["collapsed panel"] == plan["remembered tab"] == "localStorage", plan),
            ("guarded localStorage passes", unguarded_localstorage(js_ok) == 0, unguarded_localstorage(js_ok)),
            ("unguarded localStorage caught", unguarded_localstorage(js_bad) == 1, unguarded_localstorage(js_bad))]


# ---------------------------------------------------------------- APP-04
def rtl_dashboard(data: dict) -> str:
    vmax = max(data.values())
    bars = "".join(f'<rect x="{i * 30}" y="{100 - v / vmax * 100:.1f}" width="24" height="{v / vmax * 100:.1f}">'
                   f'<title>{k}: {v}</title></rect>' for i, (k, v) in enumerate(data.items()))
    tiles = "".join(f'<div class="tile"><b>{k}</b><span class="n">{v}</span></div>' for k, v in data.items())
    rows = "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in data.items())
    return ('<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>لوحة المبيعات</title><style>'
            ':root{--bg:#fff;--ink:#111}@media (prefers-color-scheme:dark){:root{--bg:#111;--ink:#eee}}'
            'body{background:var(--bg);color:var(--ink)}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr))}'
            '.n{font-variant-numeric:tabular-nums}</style></head><body>'
            f'<div class="grid">{tiles}</div><svg viewBox="0 0 {len(data) * 30} 100">{bars}</svg>'
            f'<table>{rows}</table></body></html>')


def app_04(work):
    data = {"الرياض": 120, "جدة": 90, "الدمام": 45}
    html = rtl_dashboard(data)
    _w(work, "dashboard.html", html)
    soup = BeautifulSoup(html, "html.parser")
    table = {tr.th.text: int(tr.td.text) for tr in soup.find_all("tr")}
    titles = [t.text for t in soup.find_all("title")][1:]
    tallest = max(soup.find_all("rect"), key=lambda r: float(r["height"]))
    return [("html dir=rtl", soup.html.get("dir") == "rtl", soup.html.get("dir")),
            ("table view equals injected numbers", table == data, table),
            ("one SVG <title> per bar", len(titles) == 3 and titles[0] == "الرياض: 120", titles),
            ("tallest bar is the max value (Riyadh, 100 units)", tallest.title.text.startswith("الرياض")
             and float(tallest["height"]) == 100.0, tallest["height"]),
            ("tiles minmax(150px,1fr) + tabular-nums", "minmax(150px,1fr)" in html and "tabular-nums" in html, "css")]


# ---------------------------------------------------------------- APP-15
def design_smells(html: str) -> list:
    css = html.lower()
    out = []
    grads = re.findall(r"linear-gradient\(([^)]*)\)", css)
    purple = ("#7c3aed", "#8b5cf6", "purple", "#a855f7", "#6d28d9")
    blue = ("#3b82f6", "#2563eb", "blue", "#1d4ed8", "#60a5fa")
    if any(any(p in g for p in purple) and any(b in g for b in blue) for g in grads):
        out.append("purple-to-blue gradient")
    if "blob" in css:
        out.append("decorative blob")
    soup = BeautifulSoup(html, "html.parser")
    if any(c.find_parent(class_="card") for c in soup.find_all(class_="card")):
        out.append("card inside card")
    hues = set()
    flat = re.sub(r"linear-gradient\([^)]*\)", "", css)
    for h in re.findall(r"#([0-9a-f]{6})\b", flat):
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
        mx, mn = max(r, g, b), min(r, g, b)
        if mx - mn < 30:
            continue
        if mx == r:
            hue = (60 * ((g - b) / (mx - mn))) % 360
        elif mx == g:
            hue = 60 * ((b - r) / (mx - mn)) + 120
        else:
            hue = 60 * ((r - g) / (mx - mn)) + 240
        hues.add(int(hue // 30))
    if len(hues) <= 1:
        out.append("one-hue palette")
    hero = soup.find("h1")
    if hero and re.search(r"(unlock|supercharge|revolutioni[sz]e|next[- ]level|the future of)", hero.text.lower()):
        out.append("vague hero copy")
    return out


STATES = ("loading", "empty", "error", "partial", "success", "permission")


def state_matrix_missing(matrix: dict) -> list:
    return [s for s in STATES if not all(matrix.get(s, {}).get(k) for k in ("trigger", "feedback", "next"))]


def app_15(work):
    bad = ('<style>.hero{background:linear-gradient(90deg,#7c3aed,#3b82f6)}.blob{border-radius:50%}'
           'a{color:#2563eb}b{color:#1d4ed8}</style><h1>Unlock the future of work</h1>'
           '<div class="card"><div class="card">x</div></div>')
    good = ('<style>.hero{background:#f5efe6}a{color:#c2410c}b{color:#0f766e}</style>'
            '<h1>Close the month in two days</h1><div class="card">x</div><div class="card">y</div>')
    _w(work, "bad.html", bad)
    _w(work, "good.html", good)
    sb, sg = design_smells(bad), design_smells(good)
    full = {s: {"trigger": "t", "feedback": "f", "next": "n"} for s in STATES}
    partial = dict(full)
    partial.pop("permission")
    partial["error"] = {"trigger": "500", "feedback": "toast"}
    miss = state_matrix_missing(partial)
    _w(work, "state_matrix.json", json.dumps(full, indent=1))
    want = {"purple-to-blue gradient", "decorative blob", "card inside card", "one-hue palette", "vague hero copy"}
    return [("all five planted smells caught", want <= set(sb), sb),
            ("clean page has no smells", sg == [], sg),
            ("matrix has exactly six states", len(STATES) == 6 and state_matrix_missing(full) == [], STATES),
            ("missing 'next' and missing state found", miss == ["error", "permission"], miss)]


# ---------------------------------------------------------------- APP-16
def polish_lint(css: str) -> list:
    out = []
    if re.search(r"transition\s*:\s*all", css):
        out.append("transition: all")
    for prop in re.findall(r"transition\s*:\s*([^;}]*)", css):
        for part in prop.split(","):
            name = part.strip().split()[0] if part.strip() else ""
            if name not in ("transform", "opacity", "all", "none", ""):
                out.append(f"animates {name}")
    m = re.search(r"\.outer{[^}]*border-radius:(\d+)px[^}]*padding:(\d+)px", css)
    n = re.search(r"\.inner{[^}]*border-radius:(\d+)px", css)
    if m and n and int(m.group(1)) != int(n.group(1)) + int(m.group(2)):
        out.append(f"radius {m.group(1)} != {n.group(1)}+{m.group(2)}")
    if "prefers-reduced-motion" not in css:
        out.append("no reduced-motion")
    return out


def app_16(work):
    good = (".outer{border-radius:20px;padding:8px}.inner{border-radius:12px}.btn{transition:transform .15s,opacity .15s}"
            ".btn:active{transform:scale(0.96)}@media (prefers-reduced-motion:reduce){*{transition:none}}")
    bad = (".outer{border-radius:12px;padding:8px}.inner{border-radius:12px}.btn{transition:all .3s}"
           ".x{transition:width .2s}")
    _w(work, "good.css", good)
    _w(work, "bad.css", bad)
    lg, lb = polish_lint(good), polish_lint(bad)
    return [("concentric radius 12+8=20 accepted", lg == [], lg),
            ("equal radii (12 vs 12+8) flagged", "radius 12 != 12+8" in lb, lb),
            ("transition: all flagged", "transition: all" in lb, lb),
            ("width animation flagged", "animates width" in lb, lb),
            ("missing reduced-motion flagged", "no reduced-motion" in lb, lb)]


# ---------------------------------------------------------------- APP-17
def preview(cfg: dict) -> str:
    cols = "1fr" if cfg["layout"] == "stack" else ("1fr 1fr" if cfg["layout"] == "split" else "repeat(3,1fr)")
    return "\n".join([
        "<!doctype html>", "<html><head><style>",
        f"body{{font-family:{cfg['font']};background:{cfg['bg']};color:{cfg['ink']}}}",
        f".g{{display:grid;grid-template-columns:{cols}}}", "</style></head><body>",
        f"<h1>{cfg['title']}</h1>", '<div class="g"><div>a</div><div>b</div><div>c</div></div>', "</body></html>"])


def previews_distinct(cfgs: list, pages: list) -> list:
    bad = []
    for i, p in enumerate(pages):
        if p.count("\n") + 1 >= 100:
            bad.append(f"preview {i} too long")
    for axis in ("layout", "font", "bg"):
        vals = [c[axis] for c in cfgs]
        if len(set(vals)) != len(vals):
            bad.append(f"same {axis}")
    return bad


def app_17(work):
    cfgs = [{"layout": "stack", "font": "Georgia", "bg": "#f6f1e7", "ink": "#222", "title": "A"},
            {"layout": "split", "font": "Space Grotesk", "bg": "#0e1116", "ink": "#eee", "title": "B"},
            {"layout": "grid", "font": "IBM Plex Mono", "bg": "#ffdd00", "ink": "#000", "title": "C"}]
    pages = [preview(c) for c in cfgs]
    for i, p in enumerate(pages):
        _w(work, f"preview_{i}.html", p)
    shades = [dict(cfgs[0], bg=b) for b in ("#f6f1e7", "#f0ebe0", "#ebe5d9")]
    long_page = "\n" * 120
    return [("three previews, all distinct and <100 lines", len(pages) == 3 and previews_distinct(cfgs, pages) == [],
             [p.count("\n") + 1 for p in pages]),
            ("three shades of one idea rejected", "same layout" in previews_distinct(shades, [preview(c) for c in shades]),
             previews_distinct(shades, [preview(c) for c in shades])),
            ("a 121-line preview rejected", "preview 0 too long" in previews_distinct(cfgs, [long_page] + pages[1:]), "121")]


# ---------------------------------------------------------------- APP-18
RUBRIC = {"design": 0.3, "originality": 0.2, "craft": 0.3, "function": 0.2}


def anchor(score: float) -> str:
    return "generic" if score < 4 else "competent" if score < 7 else "distinctive" if score < 9 else "professional"


def rubric_score(s: dict) -> float:
    if set(s) != set(RUBRIC):
        raise ValueError("criteria mismatch")
    return round(sum(RUBRIC[k] * s[k] for k in RUBRIC), 2)


def app_18(work):
    a = rubric_score({"design": 8, "originality": 6, "craft": 9, "function": 7})
    b = rubric_score({"design": 3, "originality": 2, "craft": 3, "function": 7})
    try:
        rubric_score({"design": 8})
        rej = False
    except ValueError:
        rej = True
    _w(work, "rubric.json", json.dumps({"weights": RUBRIC, "a": a, "b": b}))
    return [("weights sum to 1.0", abs(sum(RUBRIC.values()) - 1) < 1e-9, sum(RUBRIC.values())),
            ("8/6/9/7 -> 7.7 distinctive", a == 7.7 and anchor(a) == "distinctive", (a, anchor(a))),
            ("3/2/3/7 -> 3.6 generic (function alone cannot carry it)", b == 3.6 and anchor(b) == "generic", (b, anchor(b))),
            ("incomplete rubric rejected", rej, rej)]


# ---------------------------------------------------------------- APP-19
def finish_gate(page: dict) -> dict:
    res = {"contrast": all(contrast(fg, bg) >= 4.5 for fg, bg in page["text_pairs"]),
           "touch": all(min(w, h) >= 44 for w, h in page["targets"]),
           "reduced_motion": bool(re.search(r"prefers-reduced-motion:\s*reduce\)\s*{[^}]*transform:\s*none", page["css"])),
           "focus_order": page["tab_order"] == sorted(page["tab_order"])}
    res["not_checked"] = ["390x844 render", "1440x900 render"]
    return res


def app_19(work):
    page = {"text_pairs": [("#111111", "#ffffff"), ("#595959", "#ffffff")], "targets": [(44, 44), (120, 48)],
            "css": "@media (prefers-reduced-motion: reduce){*{transform:none!important}}", "tab_order": [1, 2, 3]}
    bad = {"text_pairs": [("#777777", "#ffffff")], "targets": [(32, 32)], "css": "", "tab_order": [1, 3, 2]}
    g, b = finish_gate(page), finish_gate(bad)
    _w(work, "gate.json", json.dumps({"good": g, "bad": b}, indent=1))
    return [("black on white contrast is 21.0", contrast("#000000", "#ffffff") == 21.0, contrast("#000000", "#ffffff")),
            ("#595959 on white passes 4.5 (7.0)", contrast("#595959", "#ffffff") >= 4.5, contrast("#595959", "#ffffff")),
            ("good page passes every gate", all(g[k] for k in ("contrast", "touch", "reduced_motion", "focus_order")), g),
            ("#777 on white (4.48) fails", not b["contrast"] and contrast("#777777", "#ffffff") < 4.5, contrast("#777777", "#ffffff")),
            ("32 px target, missing reduced-motion, bad tab order fail",
             not b["touch"] and not b["reduced_motion"] and not b["focus_order"], b),
            ("unchecked renders recorded", g["not_checked"] == ["390x844 render", "1440x900 render"], g["not_checked"])]


# ---------------------------------------------------------------- APP-24
def second_peak(h: float, e: float) -> float:
    """Ball dropped from h with restitution e: peak after the 2nd bounce = h * e**4 (height scales by e**2 per bounce)."""
    return h * e ** 4


def challenge(target: float, tol: float, lo=0.5, hi=3.0, e=0.8, step=0.01) -> dict:
    best = None
    n = int(round((hi - lo) / step))
    for i in range(n + 1):
        h = lo + i * step
        v = second_peak(h, e)
        if best is None or abs(v - target) < abs(best[1] - target):
            best = (h, v)
    met = abs(best[1] - target) <= tol
    return {"met": met, "value": round(best[1], 4), "setting": round(best[0], 2), "target": target,
            "tolerance": tol, "possible": met}


def app_24(work):
    ok = challenge(0.8192, 0.005)
    no = challenge(2.0, 0.01)
    _w(work, "challenges.json", json.dumps([ok, no], indent=1))
    return [("2 m drop, e=0.8 -> second peak 0.8192 m", abs(second_peak(2.0, 0.8) - 0.8192) < 1e-9, second_peak(2.0, 0.8)),
            ("target 0.8192 reachable at 2.0 m", ok["possible"] and ok["setting"] == 2.0, ok),
            ("target 2.0 m impossible (max 3*0.4096=1.229)", not no["possible"] and abs(no["value"] - 1.2288) < 1e-3, no),
            ("record has the five fields", {"met", "value", "target", "tolerance", "possible"} <= set(ok), sorted(ok))]


# ---------------------------------------------------------------- APP-27
def build_prefs_page() -> str:
    return ('<!doctype html><html><head><style>.loader{position:fixed;inset:0;font-family:"Cairo"}'
            '@media (prefers-reduced-motion: reduce){*{animation:none!important}}body.still *{animation:none!important}'
            'body.projector{font-size:125%;--ink:#000}.sr{position:absolute;left:-9999px}.sr:focus{left:8px}</style></head>'
            '<body><a class="sr" href="#text">تخطَّ إلى النص</a><div class="loader">...</div>'
            '<div id="nogl" hidden><a href="#text">النسخة النصية</a></div><noscript><a href="#text">النسخة النصية</a></noscript>'
            '<script>try{if(localStorage.getItem("still")==="1")document.body.classList.add("still")}catch(e){}'
            'function toggleStill(){document.body.classList.toggle("still");try{localStorage.setItem("still",'
            'document.body.classList.contains("still")?"1":"0")}catch(e){}}</script><main id="text"></main></body></html>')


def prefs_audit(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    js = " ".join(s.get_text() for s in soup.find_all("script"))
    css = " ".join(s.get_text() for s in soup.find_all("style"))
    return {"reduced_motion": "prefers-reduced-motion" in css, "still_class": "body.still" in css,
            "storage_guarded": "localStorage" in js and unguarded_localstorage(js) == 0,
            "projector": "body.projector" in css, "nogl": soup.find(id="nogl") is not None,
            "noscript": soup.find("noscript") is not None,
            "skip_link": bool(soup.select_one("a.sr")) and ".sr:focus" in css,
            "inline_loader": ".loader" in css}


def app_27(work):
    html = build_prefs_page()
    _w(work, "page.html", html)
    a = prefs_audit(html)
    broken = html.replace('try{if(localStorage.getItem("still")==="1")document.body.classList.add("still")}catch(e){}',
                          'if(localStorage.getItem("still")==="1")document.body.classList.add("still");').replace("<noscript>", "<div>").replace("</noscript>", "</div>")
    b = prefs_audit(broken)
    return [("all eight safeguards present", all(a.values()), a),
            ("unguarded localStorage read caught", not b["storage_guarded"], b["storage_guarded"]),
            ("missing <noscript> caught", not b["noscript"], b["noscript"])]


PROGRAMS = {"APP-01": app_01, "APP-02": app_02, "APP-04": app_04, "APP-15": app_15, "APP-16": app_16,
            "APP-17": app_17, "APP-18": app_18, "APP-19": app_19, "APP-24": app_24, "APP-27": app_27}
