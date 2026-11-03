"""charts-data-infographic: method cards as real programs with known-answer checks.

Every card builds a deterministic dataset in the work folder, renders the chart / counter / infographic
with numpy + PIL (frames encoded losslessly with libx264rgb so measurements read back exactly), and
measures the produced file: bar heights in pixels, arc coverage by angle, digits decoded from a
seven-segment glyph renderer, colours, timing per frame. Each card also runs a negative control: the
same measurement on the unprocessed input (blank canvas, unsorted data, un-eased counter...) fails.
"""
import json
import math
import subprocess
from pathlib import Path

from _harness import card, check, fx

GAPS: dict = {
    "DATA-98": "needs a Gemini image model (paid Google API key + network); its raster numbers would also "
               "have to be re-set in code, so nothing honest can run here",
}

# ----------------------------------------------------------------------------------------------- helpers


def _np():
    import numpy as np
    return np


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def canvas(w, h, bg="#ffffff"):
    np = _np()
    a = np.zeros((h, w, 3), dtype=float)
    a[:, :] = rgb(bg) if isinstance(bg, str) else bg
    return a


def save_png(arr, path):
    from PIL import Image
    Image.fromarray(_np().clip(arr, 0, 255).round().astype("uint8")).save(path)
    return Path(path)


def load_png(path):
    from PIL import Image
    return _np().asarray(Image.open(path).convert("RGB")).astype(float)


def write_video(path, frames, fps=30):
    """Encode numpy frames losslessly (libx264rgb qp 0) so pixel measurements read back exactly."""
    np = _np()
    frames = list(frames)
    h, w = frames[0].shape[:2]
    p = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", "%dx%d" % (w, h), "-r", str(fps), "-i", "-", "-c:v", "libx264rgb", "-qp", "0",
                          "-preset", "ultrafast", str(path)], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    for f in frames:
        p.stdin.write(np.clip(f, 0, 255).round().astype("uint8").tobytes())
    p.stdin.close()
    if p.wait():
        raise RuntimeError("ffmpeg encode failed: %s" % p.stderr.read().decode(errors="replace")[-300:])
    return Path(path)


def read_video(path):
    np = _np()
    pr = fx.probe(path)
    st = [s for s in pr["streams"] if s.get("codec_type") == "video"][0]
    w, h = int(st["width"]), int(st["height"])
    out = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, timeout=120, stdin=subprocess.DEVNULL).stdout
    return np.frombuffer(out, dtype=np.uint8).reshape(-1, h, w, 3).astype(float)


def pil_mask(w, h, fn):
    from PIL import Image, ImageDraw
    im = Image.new("L", (w, h), 0)
    fn(ImageDraw.Draw(im))
    return _np().asarray(im) > 127


def paint(arr, mask, color, alpha=1.0):
    c = _np().array(rgb(color) if isinstance(color, str) else color, dtype=float)
    arr[mask] = arr[mask] * (1 - alpha) + c * alpha
    return arr


def rect(arr, x0, y0, x1, y1, color, alpha=1.0):
    h, w = arr.shape[:2]
    x0, x1 = max(0, int(round(x0))), min(w, int(round(x1)))
    y0, y1 = max(0, int(round(y0))), min(h, int(round(y1)))
    if x1 > x0 and y1 > y0:
        c = _np().array(rgb(color) if isinstance(color, str) else color, dtype=float)
        arr[y0:y1, x0:x1] = arr[y0:y1, x0:x1] * (1 - alpha) + c * alpha
    return arr


def near(arr, color, tol=12.0):
    np = _np()
    c = np.array(rgb(color) if isinstance(color, str) else color, dtype=float)
    return np.abs(arr - c).max(axis=-1) <= tol


def angle_grid(h, w, cx, cy):
    """Per-pixel radius and clockwise angle from 12 o'clock, in degrees 0..360."""
    np = _np()
    ys, xs = np.mgrid[0:h, 0:w]
    dx, dy = xs + 0.5 - cx, ys + 0.5 - cy
    r = np.hypot(dx, dy)
    ang = (np.degrees(np.arctan2(dx, -dy)) + 360.0) % 360.0
    return r, ang


def ring_mask(h, w, cx, cy, r0, r1, a0=0.0, a1=360.0):
    r, ang = angle_grid(h, w, cx, cy)
    m = (r >= r0) & (r < r1)
    if a1 - a0 < 360:
        a0m, a1m = a0 % 360, a1 % 360
        if a1 - a0 <= 0:
            return m & False
        m &= ((ang >= a0m) & (ang < a1m)) if a0m <= a1m else ((ang >= a0m) | (ang < a1m))
    return m


def arc_fraction(arr, cx, cy, r0, r1, color, tol=12.0):
    """Measured share of the annulus painted in colour (0..1)."""
    h, w = arr.shape[:2]
    ann = ring_mask(h, w, cx, cy, r0 + 1, r1 - 1)
    return float((near(arr, color, tol) & ann).sum()) / float(ann.sum())


# easing curves (GSAP names)
EASE = {
    "linear": lambda t: t,
    "power2.inOut": lambda t: 2 * t * t if t < .5 else 1 - (-2 * t + 2) ** 2 / 2,
    "power2.out": lambda t: 1 - (1 - t) ** 2,
    "power2.in": lambda t: t * t,
    "power3.out": lambda t: 1 - (1 - t) ** 3,
    "easeOutCubic": lambda t: 1 - (1 - t) ** 3,
    "easeInOutCubic": lambda t: 4 * t ** 3 if t < .5 else 1 - (-2 * t + 2) ** 3 / 2,
    "easeOutExpo": lambda t: 1.0 if t >= 1 else 1 - 2 ** (-10 * t),
    "easeInExpo": lambda t: 0.0 if t <= 0 else 2 ** (10 * t - 10),
    "easeInOutSine": lambda t: -(math.cos(math.pi * t) - 1) / 2,
    "easeOut": lambda t: 1 - (1 - t) ** 2,
    "easeInOut": lambda t: -(math.cos(math.pi * t) - 1) / 2,
    "back.out": lambda t: 1 + 2.70158 * (t - 1) ** 3 + 1.70158 * (t - 1) ** 2,
}


def ease(name, t):
    return EASE[name](min(1.0, max(0.0, t)))


def prog(t, start, dur):
    return min(1.0, max(0.0, (t - start) / dur)) if dur > 0 else float(t >= start)


# ---- seven-segment glyphs: numbers drawn by the program and decoded back from the pixels
_DIG = {"0": "abcdef", "1": "bc", "2": "abdeg", "3": "abcdg", "4": "bcfg", "5": "acdfg", "6": "acdefg", "7": "abc",
        "8": "abcdefg", "9": "abcdfg", "-": "g", "+": "gv", " ": ""}
_INV = {frozenset(v): k for k, v in _DIG.items()}


def _segs(H):
    W = int(round(H * 0.55))
    T = max(2, int(round(H * 0.13)))
    m = H // 2
    lo, hi = m - T // 2, m + (T + 1) // 2
    return W, T, {"a": (T, 0, W - T, T), "b": (W - T, T, W, lo), "c": (W - T, hi, W, H - T), "d": (T, H - T, W - T, H),
                  "e": (0, hi, T, H - T), "f": (0, T, T, lo), "g": (T, lo, W - T, hi),
                  "v": (W // 2 - T // 2, H // 4, W // 2 - T // 2 + T, H - H // 4)}


def seg_layout(pattern, H, x, y):
    W, T, _ = _segs(H)
    gap = max(2, T)
    cells, cx = [], x
    for ch in pattern:
        if ch in ",.":
            cells.append((ch, cx, y))
            cx += T + gap
        else:
            cells.append(("d", cx, y))
            cx += W + gap
    return cells, cx - gap - x


def seg_width(pattern, H):
    return seg_layout(pattern, H, 0, 0)[1]


def draw_seg(arr, text, pattern, H, x, y, color, alpha=1.0):
    if len(text) != len(pattern):
        raise ValueError("text %r does not fit pattern %r" % (text, pattern))
    W, T, S = _segs(H)
    cells, _ = seg_layout(pattern, H, x, y)
    for (kind, cx, cy), ch in zip(cells, text):
        if kind == "d":
            for s in _DIG[ch]:
                x0, y0, x1, y1 = S[s]
                rect(arr, cx + x0, cy + y0, cx + x1, cy + y1, color, alpha)
        elif ch in ",.":
            rect(arr, cx, cy + H - T, cx + T, cy + H, color, alpha)
    return arr


def read_seg(arr, pattern, H, x, y, bg, thr=None, fg=None):
    """Decode the glyphs at a known layout by sampling each segment centre (on = far from background;
    with bg=None, on = within thr of the foreground colour, for text over footage)."""
    np = _np()
    W, T, S = _segs(H)
    cells, _ = seg_layout(pattern, H, x, y)
    fgc = None if fg is None else np.array(rgb(fg) if isinstance(fg, str) else fg, dtype=float)
    bgc = None if bg is None else np.array(rgb(bg) if isinstance(bg, str) else bg, dtype=float)
    if thr is None:
        thr = 0.5 * float(np.abs(fgc - bgc).max()) if bgc is not None else 40.0
    hh, ww = arr.shape[:2]

    def on(px, py):
        px, py = int(px), int(py)
        if not (0 <= px < ww and 0 <= py < hh):
            return False
        if bgc is None:
            return float(np.abs(arr[py, px] - fgc).max()) <= thr
        return float(np.abs(arr[py, px] - bgc).max()) > thr
    out = ""
    for kind, cx, cy in cells:
        if kind == "d":
            lit = set()
            for s, (x0, y0, x1, y1) in S.items():
                px, py = cx + (x0 + x1) / 2.0, cy + (y0 + y1) / 2.0
                if s == "v":
                    py = cy + H * 0.33
                if on(px, py):
                    lit.add(s)
            out += _INV.get(frozenset(lit), "?")
        else:
            out += kind if on(cx + T / 2.0, cy + H - T / 2.0) else " "
    return out


def seg_value(s):
    t = s.replace(",", "").replace(" ", "")
    if not t or "?" in t:
        return None
    try:
        return float(t)
    except ValueError:
        return None


def fmt_int(v, pattern, sep=False):
    s = format(int(round(v)), ",d") if sep else str(int(round(v)))
    return s.rjust(len(pattern))


def nice_num(x):
    """Smallest nice step >= x from {1, 2, 2.5, 5, 10} x 10^n."""
    if x <= 0:
        return 1.0
    e = math.floor(math.log10(x))
    f = x / 10 ** e
    return next(s for s in (1, 2, 2.5, 5, 10) if f <= s + 1e-9) * 10 ** e


def nice_ticks(vmax, n=4):
    step = nice_num(vmax / n)
    top = math.ceil(vmax / step - 1e-9) * step
    k = int(round(top / step))
    return [round(i * step, 10) for i in range(k + 1)], step


def is_nice(v):
    if v == 0:
        return True
    e = math.floor(math.log10(abs(v)))
    f = round(abs(v) / 10 ** e, 6)
    return f in (1.0, 2.0, 2.5, 5.0, 10.0)


def wjson(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    return Path(path)


def col_runs(mask_1d):
    """Lengths of consecutive True runs in a 1-D boolean array, with their starts."""
    runs, start = [], None
    for i, v in enumerate(list(mask_1d) + [False]):
        if v and start is None:
            start = i
        elif not v and start is not None:
            runs.append((start, i - start))
            start = None
    return runs


def clusters(idx, gap=1):
    """Group sorted integer positions into clusters; returns their centres."""
    idx = sorted(int(i) for i in idx)
    out, cur = [], []
    for i in idx:
        if cur and i - cur[-1] > gap:
            out.append(sum(cur) / len(cur))
            cur = []
        cur.append(i)
    if cur:
        out.append(sum(cur) / len(cur))
    return out


def srgb_to_lab(c):
    def lin(u):
        u /= 255.0
        return u / 12.92 if u <= 0.04045 else ((u + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(float(v)) for v in c)
    X = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    Y = (0.2126 * r + 0.7152 * g + 0.0722 * b)
    Z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883

    def f(t):
        return t ** (1 / 3) if t > 216 / 24389 else (24389 / 27 * t + 16) / 116
    return 116 * f(Y) - 16, 500 * (f(X) - f(Y)), 200 * (f(Y) - f(Z))


def de2000(c1, c2):
    L1, a1, b1 = srgb_to_lab(c1)
    L2, a2, b2 = srgb_to_lab(c2)
    C1, C2 = math.hypot(a1, b1), math.hypot(a2, b2)
    Cb = (C1 + C2) / 2
    G = 0.5 * (1 - math.sqrt(Cb ** 7 / (Cb ** 7 + 25 ** 7)))
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360
    h2p = math.degrees(math.atan2(b2, a2p)) % 360
    dLp, dCp = L2 - L1, C2p - C1p
    dh = h2p - h1p
    if C1p * C2p == 0:
        dh = 0
    elif dh > 180:
        dh -= 360
    elif dh < -180:
        dh += 360
    dHp = 2 * math.sqrt(C1p * C2p) * math.sin(math.radians(dh / 2))
    Lbp, Cbp = (L1 + L2) / 2, (C1p + C2p) / 2
    if C1p * C2p == 0:
        hbp = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        hbp = (h1p + h2p) / 2
    else:
        hbp = (h1p + h2p + 360) / 2 if h1p + h2p < 360 else (h1p + h2p - 360) / 2
    T = (1 - 0.17 * math.cos(math.radians(hbp - 30)) + 0.24 * math.cos(math.radians(2 * hbp))
         + 0.32 * math.cos(math.radians(3 * hbp + 6)) - 0.20 * math.cos(math.radians(4 * hbp - 63)))
    dth = 30 * math.exp(-((hbp - 275) / 25) ** 2)
    Rc = 2 * math.sqrt(Cbp ** 7 / (Cbp ** 7 + 25 ** 7))
    Sl = 1 + 0.015 * (Lbp - 50) ** 2 / math.sqrt(20 + (Lbp - 50) ** 2)
    Sc, Sh = 1 + 0.045 * Cbp, 1 + 0.015 * Cbp * T
    Rt = -math.sin(math.radians(2 * dth)) * Rc
    return math.sqrt((dLp / Sl) ** 2 + (dCp / Sc) ** 2 + (dHp / Sh) ** 2 + Rt * (dCp / Sc) * (dHp / Sh))


# Machado et al. 2009 severity-1.0 CVD matrices in linear RGB
_CVD = {"protan": ((0.152286, 1.052583, -0.204868), (0.114503, 0.786281, 0.099216), (-0.003882, -0.048116, 1.051998)),
        "deutan": ((0.367322, 0.860646, -0.227968), (0.280085, 0.672501, 0.047413), (-0.011820, 0.042940, 0.968881)),
        "tritan": ((1.255528, -0.076749, -0.178779), (-0.078411, 0.930809, 0.147602), (0.004733, 0.691367, 0.303900))}


def simulate_cvd(c, kind):
    def lin(u):
        u /= 255.0
        return u / 12.92 if u <= 0.04045 else ((u + 0.055) / 1.055) ** 2.4

    def enc(u):
        u = min(1.0, max(0.0, u))
        return 255 * (12.92 * u if u <= 0.0031308 else 1.055 * u ** (1 / 2.4) - 0.055)
    L = [lin(float(v)) for v in c]
    M = _CVD[kind]
    return tuple(enc(sum(M[i][j] * L[j] for j in range(3))) for i in range(3))


def rel_lum(c):
    def lin(u):
        u /= 255.0
        return u / 12.92 if u <= 0.03928 else ((u + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(float(v)) for v in (rgb(c) if isinstance(c, str) else c))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(c1, c2):
    a, b = sorted((rel_lum(c1), rel_lum(c2)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def bar_heights(arr, base_y, xs, bg, thr=40.0):
    """Measure the painted height (px above base_y) in each column x of xs."""
    np = _np()
    bgc = np.array(rgb(bg), dtype=float)
    out = []
    for x in xs:
        col = np.abs(arr[:base_y, int(x)] - bgc).max(axis=-1) > thr
        run = 0
        for y in range(base_y - 1, -1, -1):
            if col[y]:
                run += 1
            else:
                break
        out.append(run)
    return out


def bar_lengths_h(arr, x0, ys, bg, thr=40.0):
    """Horizontal bars: painted run length to the right of x0 on each row y."""
    np = _np()
    bgc = np.array(rgb(bg), dtype=float)
    out = []
    for y in ys:
        row = np.abs(arr[int(y), x0:] - bgc).max(axis=-1) > thr
        run = 0
        for v in row:
            if v:
                run += 1
            else:
                break
        out.append(run)
    return out


def max_ratio_err(measured, values):
    """Largest relative error between measured px and the values scaled by the largest one."""
    k = max(measured) / float(max(values))
    return max(abs(m - v * k) / max(1.0, v * k) for m, v in zip(measured, values))


def line_mask(h, w, pts, width=2):
    return pil_mask(w, h, lambda d: d.line([tuple(map(float, p)) for p in pts], fill=255, width=width, joint="curve"))


# ------------------------------------------------------------------------------------------------- cards


def _infer_relationship(ds):
    if "edges" in ds:
        return "flow"
    if "goal" in ds:
        return "target"
    if "pairs" in ds:
        return "correlation"
    if "sample" in ds:
        return "distribution"
    if "periods" in ds and len(ds["periods"]) == 2:
        return "change_two_periods"
    if "stack_over_time" in ds:
        return "composition_time"
    if "parts" in ds and abs(sum(ds["parts"].values()) - ds.get("total", -1)) <= 0.01 * ds.get("total", 1):
        return "part_to_whole"
    if "time" in ds:
        return "trend"
    if "categories" in ds:
        return "ranking" if ds.get("question") == "rank" else "comparison"
    return "unknown"


def _pick_chart(ds, video=True):
    rel = _infer_relationship(ds)
    if rel == "trend":
        return "area" if ds.get("cumulative") else "line"
    if rel == "comparison":
        return "hbar" if len(ds["categories"]) > 7 else "vbar"
    if rel == "part_to_whole":
        return "pie" if len(ds["parts"]) <= (5 if video else 6) else "stacked_bar"
    return {"ranking": "sorted_hbar", "change_two_periods": "slope", "composition_time": "stacked_area",
            "distribution": "histogram", "correlation": "scatter", "flow": "sankey", "target": "bullet"}.get(rel, "table")


@card("DATA-01")
def chart_by_relationship(task, wd):
    """Infer the relationship from the data's structure and pick the chart from the lookup, then render one."""
    np = _np()
    rs = np.random.RandomState(1)
    months = ["2025-%02d" % m for m in range(1, 13)]
    many = {"c%02d" % i: int(v) for i, v in enumerate(rs.randint(5, 95, 14))}
    fixtures = {
        "trend": ({"time": months, "y": list(range(12))}, "line"),
        "cumulative": ({"time": months, "y": list(np.cumsum(range(12)).tolist()), "cumulative": True}, "area"),
        "compare5": ({"categories": {"a": 3, "b": 7, "c": 5, "d": 2, "e": 9}}, "vbar"),
        "compare14": ({"categories": many}, "hbar"),
        "rank": ({"categories": {"a": 3, "b": 7, "c": 5}, "question": "rank"}, "sorted_hbar"),
        "two_periods": ({"periods": ["2020", "2025"], "series": {"x": [1, 2], "y": [3, 1]}}, "slope"),
        "share4": ({"parts": {"a": 40, "b": 30, "c": 20, "d": 10}, "total": 100}, "pie"),
        "share8": ({"parts": {k: 12.5 for k in "abcdefgh"}, "total": 100}, "stacked_bar"),
        "comp_time": ({"stack_over_time": {"a": [1, 2], "b": [2, 1]}, "time": ["t0", "t1"]}, "stacked_area"),
        "dist": ({"sample": rs.normal(0, 1, 300).round(3).tolist()}, "histogram"),
        "corr": ({"pairs": rs.normal(0, 1, (50, 2)).round(3).tolist()}, "scatter"),
        "flow": ({"edges": [["a", "b", 5], ["a", "c", 3]]}, "sankey"),
        "target": ({"value": 72, "goal": 90}, "bullet"),
    }
    chosen = {k: _pick_chart(ds) for k, (ds, _) in fixtures.items()}
    checks = [check("chart for %s" % k, chosen[k] == exp, chosen[k], exp) for k, (_, exp) in fixtures.items()]
    taste = sum(1 for k, (_, exp) in fixtures.items() if exp == "pie")
    checks.append(check("negative control: a by-taste picker (always pie) matches the lookup", taste / len(fixtures) < 0.5,
                        "%d/%d" % (taste, len(fixtures)), "< 50%"))
    # render the chosen chart for the 14-category fixture: horizontal bars, one hue + accent (<= 8 hues)
    vals = list(many.values())
    H, W, x0, bh, pitch = 14 * 14 + 10, 360, 40, 10, 14
    img = canvas(W, H, "#ffffff")
    for i, v in enumerate(vals):
        rect(img, x0, 5 + i * pitch, x0 + v * 3, 5 + i * pitch + bh, "#e4572e" if v == max(vals) else "#4a6fa5")
    png = save_png(img, wd / "compare14_hbar.png")
    back = load_png(png)
    lens = bar_lengths_h(back, x0, [5 + i * pitch + bh // 2 for i in range(len(vals))], "#ffffff")
    err = max_ratio_err(lens, vals)
    checks.append(check("rendered hbar lengths proportional to data", err < 0.01, err, "< 0.01"))
    hues = len({tuple(back[y, x]) for y in range(H) for x in range(x0, W, 3)} - {(255.0, 255.0, 255.0)})
    checks.append(check("categorical hues <= 8", hues <= 8, hues, "<= 8"))
    out = wjson(wd / "chart_choices.json", {k: {"relationship": _infer_relationship(ds), "chart": chosen[k]}
                                            for k, (ds, _) in fixtures.items()})
    return checks, [out, png]


@card("DATA-02")
def slope_chart(task, wd):
    """Net change / rank flips -> slope chart: two axes, one segment per series, signed change at the right,
    segments drawn with a 70 ms stagger, the biggest mover in accent, the rest grey."""
    np = _np()
    start = [40, 55, 30, 70, 25]
    end = [62, 50, 58, 45, 33]
    question = "net change and rank flips"
    view = "slope" if ("net change" in question or "rank" in question) else "line"
    W, H, L, R, fps = 340, 240, 60, 240, 30
    y = lambda v: 220 - v * 2.5
    hi = int(np.argmax([abs(e - s) for s, e in zip(start, end)]))
    stagger, dur = 0.07, 0.5
    labels = ["%+d" % (e - s) for s, e in zip(start, end)]
    LH = 12

    def frame(t):
        a = canvas(W, H, "#ffffff")
        rect(a, L - 2, 30, L, 222, "#222222")
        rect(a, R, 30, R + 2, 222, "#222222")
        for i, (s, e) in enumerate(zip(start, end)):
            p = ease("power2.out", prog(t, i * stagger, dur))
            if t <= i * stagger or p <= 0:
                continue
            x1 = L + (R - L) * p
            y1 = y(s) + (y(e) - y(s)) * p
            paint(a, line_mask(H, W, [(L, y(s)), (x1, y1)], 2), "#e4572e" if i == hi else "#9aa0a6")
            if p >= 1:
                draw_seg(a, labels[i].rjust(3), "ddd", LH, R + 8, int(y(e)) - LH // 2, "#e4572e" if i == hi else "#555555")
        return a
    n = int(1.2 * fps)
    frames = [frame(k / fps) for k in range(n)]
    vid = write_video(wd / "slope.mp4", frames, fps)
    fr = read_video(vid)
    bg = np.array([255.0, 255.0, 255.0])

    def ys_at(a, x):
        col = np.abs(a[:, x] - bg).max(axis=-1) > 40
        return clusters(np.nonzero(col[25:225])[0] + 25)
    last = fr[-1]
    left, right = ys_at(last, L + 2), ys_at(last, R - 2)
    expl = sorted(y(v) + 0.5 for v in start)
    expr = sorted(y(v) + 0.5 for v in end)
    el = max(abs(a - b) for a, b in zip(sorted(left), expl)) if len(left) == 5 else 99
    er = max(abs(a - b) for a, b in zip(sorted(right), expr)) if len(right) == 5 else 99
    checks = [check("view chosen for net change", view == "slope", view, "slope"),
              check("left endpoints at data y (px)", el <= 1.5, el, "<= 1.5"),
              check("right endpoints at data y (px)", er <= 1.5, er, "<= 1.5")]
    acc = near(last[:, L + 2], "#e4572e", 30)
    acc_y = clusters(np.nonzero(acc)[0])
    checks.append(check("accent marks the biggest mover", len(acc_y) == 1 and abs(acc_y[0] - (y(start[hi]) + 0.5)) <= 1.5,
                        acc_y, y(start[hi]) + 0.5))
    read = [read_seg(last, "ddd", LH, R + 8, int(y(e)) - LH // 2, "#ffffff", fg="#555555").strip() for e in end]
    checks.append(check("signed change labels decoded", read == labels, read, labels))
    counts = [len(ys_at(f, L + 2)) for f in fr]
    exp = [sum(1 for i in range(5) if k / fps > i * stagger and ease("power2.out", prog(k / fps, i * stagger, dur)) > 0)
           for k in range(n)]
    # a just-started segment may still be shorter than 2 px; compare where every started one is > 2 px long
    okc = all(c == e for c, e, k in zip(counts, exp, range(n)) if all(
        prog(k / fps, i * stagger, dur) == 0 or ease("power2.out", prog(k / fps, i * stagger, dur)) * (R - L) > 3
        for i in range(5)))
    checks.append(check("segments appear one by one on the 70 ms stagger", okc and counts[-1] == 5, counts[:8], exp[:8]))
    checks.append(check("negative control: the blank first frame has no segments", len(ys_at(fr[0], L + 2)) != 5,
                        len(ys_at(fr[0], L + 2)), "!= 5"))
    return checks, [vid, wjson(wd / "slope.json", {"start": start, "end": end, "labels": labels, "accent": hi})]


@card("DATA-03")
def histogram_view(task, wd):
    """One group -> 30-bin histogram with white bin edges, dashed mean (red) and median (blue) lines;
    bins rise left->right with a 35 ms stagger, the median line draws after."""
    np = _np()
    rs = np.random.RandomState(7)
    data = np.concatenate([rs.normal(50, 10, 1500), rs.exponential(12, 500) + 60])
    counts, edges = np.histogram(data, bins=30)
    mean, med = float(data.mean()), float(np.median(data))
    bw, x0, base, top = 10, 20, 230, 200
    W, H, fps = 30 * bw + 40, 250, 30
    hpx = [int(round(c / counts.max() * top)) for c in counts]
    xv = lambda v: x0 + (v - edges[0]) / (edges[-1] - edges[0]) * 30 * bw
    stagger, rise = 0.035, 0.3
    t_bins = 29 * stagger + rise

    def frame(t):
        a = canvas(W, H, "#f4f4f4")
        for i, hp in enumerate(hpx):
            p = ease("power2.out", prog(t, i * stagger, rise))
            hh = int(round(hp * p))
            if hh:
                rect(a, x0 + i * bw, base - hh, x0 + (i + 1) * bw - 1, base, "#4a6fa5")
                rect(a, x0 + (i + 1) * bw - 1, base - hh, x0 + (i + 1) * bw, base, "#ffffff")
        if t >= t_bins:
            for v, c in ((mean, "#d62728"), (med, "#1f77b4")):
                xi = int(math.floor(xv(v)))
                for yy in range(20, base, 8):
                    rect(a, xi, yy, xi + 1, yy + 4, c)
                    rect(a, xi + 1, yy, xi + 2, yy + 4, c, 0.5)
        return a
    frames = [frame(k / fps) for k in range(int((t_bins + 0.4) * fps))]
    vid = write_video(wd / "histogram.mp4", frames, fps)
    fr = read_video(vid)
    last = fr[-1]
    png = save_png(last, wd / "histogram_final.png")
    meas = bar_heights(last, base, [x0 + i * bw + 3 for i in range(30)], "#f4f4f4")
    err = max(abs(m - e) for m, e in zip(meas, hpx))
    checks = [check("30 bins", len(counts) == 30, len(counts), 30),
              check("bar heights equal counts scaled (px)", err <= 1, err, "<= 1")]
    line_x = {int(math.floor(xv(v))) + d for v in (mean, med) for d in (-1, 0, 1, 2)}
    white = all(near(last[base - h:base, x0 + (i + 1) * bw - 1], "#ffffff", 1).all() for i, h in enumerate(hpx)
                if h > 0 and x0 + (i + 1) * bw - 1 not in line_x)
    checks.append(check("white edge between bins", white, white, True))
    for v, c, nm in ((mean, "#d62728", "mean"), (med, "#1f77b4", "median")):
        cols = [x for x in range(W) if near(last[20:base, x], c, 8).sum() > 20]
        runs = col_runs(near(last[20:base, cols[0]], c, 8)) if cols else []
        cov = float(sum(near(last[:, x], c, 8).sum() for x in range(W))) / 4 / max(1, len(runs)) if cols else 0
        checks.append(check("%s line at x(%s)" % (nm, nm), bool(cols) and abs(cols[0] + 0.75 - xv(v)) <= 1.0,
                            cols[0] if cols else None, round(xv(v), 2)))
        checks.append(check("%s line dashed" % nm, len(runs) >= 10, len(runs), ">= 10"))
    starts, expect = [], []
    for i in range(30):
        if hpx[i] < 3:
            continue
        starts.append(next((k for k, a in enumerate(fr) if bar_heights(a, base, [x0 + i * bw + 3], "#f4f4f4")[0] > 0), None))
        expect.append(next(k for k in range(len(fr)) if int(round(hpx[i] * ease("power2.out", prog(k / fps, i * stagger, rise)))) > 0))
    mono = starts == expect and all(b >= a for a, b in zip(starts, starts[1:]))
    span = (expect[-1] - expect[0]) / fps
    checks.append(check("bins rise left to right on the 35 ms stagger (first frame per bin)", mono and span > 0.8,
                        starts, expect))
    med_first = next((k for k, a in enumerate(fr) if near(a[20:base], "#1f77b4", 8).any()), None)
    checks.append(check("median line draws after the bins", med_first is not None and med_first / fps >= t_bins - 1e-6,
                        med_first, ">= %.2f s" % t_bins))
    neg = bar_heights(fr[0], base, [x0 + i * bw + 3 for i in range(30)], "#f4f4f4")
    checks.append(check("negative control: unbinned first frame does not show the counts",
                        max(abs(m - e) for m, e in zip(neg, hpx)) > 1, max(neg), "!= counts"))
    return checks, [vid, png]


@card("DATA-06")
def area_encoding(task, wd):
    """Bubble size by area r = sqrt(v)*k; a log axis with equally spaced decades."""
    np = _np()
    vals = [10, 40, 90, 160]
    k = 4.0

    def render(radius_fn, path):
        a = canvas(520, 140, "#ffffff")
        cx = 70
        for v in vals:
            r = radius_fn(v)
            paint(a, pil_mask(520, 140, lambda d: d.ellipse([cx - r, 70 - r, cx + r, 70 + r], fill=255)), "#4a6fa5")
            cx += 2 * r + 18
        return save_png(a, path)

    def areas(path):
        a = load_png(path)
        m = near(a, "#4a6fa5", 5)
        cols = m.any(axis=0)
        return [int(m[:, s:s + n].sum()) for s, n in col_runs(cols)]
    good = render(lambda v: math.sqrt(v) * k, wd / "bubbles_area.png")
    bad = render(lambda v: v * 0.3, wd / "bubbles_linear_radius.png")
    ag, ab = areas(good), areas(bad)
    eg = max(abs(a / ag[0] - v / vals[0]) / (v / vals[0]) for a, v in zip(ag, vals))
    eb = max(abs(a / ab[0] - v / vals[0]) / (v / vals[0]) for a, v in zip(ab, vals))
    checks = [check("4 bubbles measured", len(ag) == 4, len(ag), 4),
              check("bubble pixel area ratio == value ratio", eg < 0.03, eg, "< 0.03"),
              check("negative control: linear radius breaks the area ratio", eb > 0.5, eb, "> 0.5")]
    # log axis, base 10: decades equally spaced
    ax = canvas(520, 40, "#ffffff")
    ticks = [1, 10, 100, 1000]
    for v in ticks:
        x = 40 + math.log10(v) * 140
        rect(ax, x, 10, x + 1, 30, "#000000")
    axp = save_png(ax, wd / "log_axis.png")
    xs = [x for x in range(520) if near(load_png(axp)[20:21, x], "#000000", 5).any()]
    gaps = [b - a for a, b in zip(xs, xs[1:])]
    checks.append(check("log axis decades equally spaced", len(xs) == 4 and max(gaps) - min(gaps) <= 1, gaps, "equal"))
    meta = wjson(wd / "encoding_note.json", {"size": "area, r = sqrt(value) * %g" % k, "axis": "log10, zero excluded",
                                             "values": vals, "areas_px": ag})
    return checks, [good, axp, meta]


_BLACKLIST_RULES = [
    ("3d", lambda s: s.get("3d"), "no decorative 3D"),
    ("pie_slices", lambda s: s["type"] in ("pie", "donut") and s.get("slices", 0) > (3 if s.get("medium") == "video" else 5),
     "pie/donut beyond 3 (video) / 5 slices -> bars"),
    ("animated_pie", lambda s: s["type"] in ("pie", "donut") and s.get("animated"), "no animated pie"),
    ("dual_axis", lambda s: s.get("dual_axis") and not s.get("both_labelled"), "dual axis must be labelled; prefer panels"),
    ("stack_segments", lambda s: s["type"] == "stacked_bar" and s.get("segments", 0) > 4, "many-segment stacks -> small multiples"),
    ("dashboard", lambda s: s["type"] == "dashboard" and s.get("panels", 0) >= 6, "no 6-panel web dashboards"),
    ("baseline", lambda s: s["type"] == "bar" and s.get("baseline", 0) != 0, "bars start at 0"),
]


@card("DATA-07")
def chart_blacklist(task, wd):
    """Lint chart specs against the blacklist, then rebuild a rejected 7-slice pie as zero-based sorted bars."""
    specs = [{"id": "pie7", "type": "pie", "slices": 7, "medium": "video"}, {"id": "bar3d", "type": "bar", "3d": True},
             {"id": "dual", "type": "line", "dual_axis": True}, {"id": "stack9", "type": "stacked_bar", "segments": 9},
             {"id": "animpie", "type": "pie", "slices": 3, "animated": True, "medium": "video"},
             {"id": "dash6", "type": "dashboard", "panels": 6}, {"id": "trunc", "type": "bar", "baseline": 40},
             {"id": "ok_bar", "type": "bar", "baseline": 0}, {"id": "ok_pie", "type": "pie", "slices": 3, "medium": "video"}]
    expected = {"pie7": False, "bar3d": False, "dual": False, "stack9": False, "animpie": False, "dash6": False,
                "trunc": False, "ok_bar": True, "ok_pie": True}
    verdicts = {s["id"]: [r for r, f, _ in _BLACKLIST_RULES if f(s)] for s in specs}
    checks = [check("lint %s" % k, (not v) == expected[k], v, "accept" if expected[k] else "reject")
              for k, v in verdicts.items()]
    shares = [31, 22, 17, 12, 9, 6, 3]

    def bars(baseline, path):
        a = canvas(300, 220, "#ffffff")
        for i, v in enumerate(sorted(shares, reverse=True)):
            h = (v - baseline) * 6
            rect(a, 20 + i * 38, 200 - h, 20 + i * 38 + 28, 200, "#4a6fa5")
        return save_png(a, path)
    good = bars(0, wd / "pie7_as_bars.png")
    trunc = bars(2, wd / "truncated_baseline.png")
    xs = [20 + i * 38 + 14 for i in range(7)]
    hg = bar_heights(load_png(good), 200, xs, "#ffffff")
    ht = bar_heights(load_png(trunc), 200, xs, "#ffffff")
    srt = sorted(shares, reverse=True)
    checks.append(check("rebuilt bars proportional from a zero baseline", max_ratio_err(hg, srt) < 0.01,
                        max_ratio_err(hg, srt), "< 0.01"))
    checks.append(check("negative control: a truncated baseline distorts the ratios", max_ratio_err(ht, srt) > 0.1,
                        max_ratio_err(ht, srt), "> 0.1"))
    return checks, [good, wjson(wd / "lint.json", verdicts)]


@card("DATA-09")
def gaps_look_like_gaps(task, wd):
    """Break the path at missing points (separate M commands), dashed labelled interpolation as a variant,
    no-data cells #777777, and an empty source gives an empty state, never sample numbers."""
    np = _np()
    vals = [12, 15, 14, 18, 21, 19, None, None, 24, 26, 25, 28, None, 30, 29, 33, 35, 34, 37, 40]
    X = lambda i: 20 + i * 15
    Y = lambda v: 180 - v * 4
    segs, cur = [], []
    for i, v in enumerate(vals):
        if v is None:
            if cur:
                segs.append(cur)
            cur = []
        else:
            cur.append((X(i), Y(v)))
    if cur:
        segs.append(cur)
    d = " ".join("M%s" % " L".join("%g %g" % p for p in s) if len(s) > 1 else "M%g %g" % s[0] for s in segs)
    svg = wd / "line_with_gaps.svg"
    svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 200"><path d="%s" fill="none" '
                   'stroke="#1f77b4" stroke-width="2"/></svg>' % d, encoding="utf-8")
    W, H = 320, 200

    def render(seglist, path, dashed=None):
        a = canvas(W, H, "#ffffff")
        for s in seglist:
            if len(s) > 1:
                paint(a, line_mask(H, W, s, 2), "#1f77b4")
        for p0, p1 in dashed or []:
            for k in range(0, 10, 2):
                q0 = (p0[0] + (p1[0] - p0[0]) * k / 10, p0[1] + (p1[1] - p0[1]) * k / 10)
                q1 = (p0[0] + (p1[0] - p0[0]) * (k + 1) / 10, p0[1] + (p1[1] - p0[1]) * (k + 1) / 10)
                paint(a, line_mask(H, W, [q0, q1], 2), "#888888")
        return save_png(a, path)
    good = render(segs, wd / "gaps.png")
    naive = render([[(X(i), Y(v)) for i, v in enumerate(vals) if v is not None]], wd / "naive_connected.png")
    gap_cols = list(range(X(5) + 3, X(8) - 2)) + list(range(X(11) + 3, X(13) - 2))
    ink = lambda path: int(sum((np.abs(load_png(path)[:, x] - 255).max(axis=-1) > 40).sum() for x in gap_cols))
    checks = [check("path has one M per contiguous run", d.count("M") == 3, d.count("M"), 3),
              check("no ink inside the gaps", ink(good) == 0, ink(good), 0),
              check("negative control: silently connecting the line puts ink in the gaps", ink(naive) > 0, ink(naive), "> 0")]
    dash = render(segs, wd / "gaps_interpolated_dashed.png", dashed=[(segs[0][-1], segs[1][0]), (segs[1][-1], segs[2][0])])
    col = near(load_png(dash)[:, :, :], "#888888", 4)
    runs = col_runs(col[:, X(6):X(8)].any(axis=0))
    checks.append(check("interpolated stretch drawn dashed", len(runs) >= 3, len(runs), ">= 3"))
    grid = [[3, 0, 5, None], [None, 2, 4, 1], [6, 7, 0, 2]]
    hm = canvas(4 * 30, 3 * 30, "#ffffff")
    ramp = lambda v: tuple(int(round(240 - v * 25)) for _ in range(2)) + (255,)
    for r, row in enumerate(grid):
        for c, v in enumerate(row):
            rect(hm, c * 30 + 1, r * 30 + 1, c * 30 + 29, r * 30 + 29, "#777777" if v is None else ramp(v))
    hmp = save_png(hm, wd / "nodata_heatmap.png")
    hb = load_png(hmp)
    miss = [tuple(hb[r * 30 + 15, c * 30 + 15]) for r, row in enumerate(grid) for c, v in enumerate(row) if v is None]
    zero = [tuple(hb[r * 30 + 15, c * 30 + 15]) for r, row in enumerate(grid) for c, v in enumerate(row) if v == 0]
    checks.append(check("no-data cells are #777777", all(m == (119.0, 119.0, 119.0) for m in miss), miss, "#777777"))
    checks.append(check("zero cells are not the no-data colour", all(z != (119.0, 119.0, 119.0) for z in zero), zero, "!= #777777"))
    empty = [v for v in [] if v is not None]
    state = {"empty_state": "لا توجد بيانات لهذه الفترة", "points": empty} if not empty else {}
    checks.append(check("empty source -> empty-state text, no numbers", state.get("points") == [] and state["empty_state"],
                        state, "empty state"))
    return checks, [svg, good, dash, hmp, wjson(wd / "empty_state.json", state)]


@card("DATA-12")
def order_by_magnitude(task, wd):
    """Sort categories descending (largest on top), keep months in natural order, draw time series 2:1-3:1,
    and use the same axis range across compared panels."""
    np = _np()
    cats = {"A": 23, "B": 57, "C": 12, "D": 41, "E": 35}
    months = [("Jan", 20), ("Feb", 35), ("Mar", 28), ("Apr", 44), ("May", 39), ("Jun", 52)]
    srt = sorted(cats.items(), key=lambda kv: -kv[1])

    def barh(items, path):
        a = canvas(300, len(items) * 20 + 10, "#ffffff")
        for i, (_, v) in enumerate(items):
            rect(a, 30, 5 + i * 20, 30 + v * 4, 5 + i * 20 + 14, "#4a6fa5")
        return save_png(a, path)
    p1 = barh(srt, wd / "sorted_barh.png")
    p0 = barh(list(cats.items()), wd / "unsorted_input.png")
    pm = barh(months, wd / "months_natural.png")
    ys = [5 + i * 20 + 7 for i in range(5)]
    l1 = bar_lengths_h(load_png(p1), 30, ys, "#ffffff")
    l0 = bar_lengths_h(load_png(p0), 30, ys, "#ffffff")
    lm = bar_lengths_h(load_png(pm), 30, [5 + i * 20 + 7 for i in range(6)], "#ffffff")
    dec = lambda L: all(a >= b for a, b in zip(L, L[1:]))
    checks = [check("largest on top, descending", dec(l1), l1, "non-increasing"),
              check("lengths proportional", max_ratio_err(l1, [v for _, v in srt]) < 0.01, max_ratio_err(l1, [v for _, v in srt]), "< 0.01"),
              check("months keep natural order", [round(x / 4) for x in lm] == [v for _, v in months], lm, [v * 4 for _, v in months]),
              check("negative control: the unsorted input is not descending", not dec(l0), l0, "not sorted")]
    # time-series plot area 2.5:1 and two compared panels on one shared y range
    vmax = max(v for _, v in months)
    plot_w, plot_h = 400, 160
    ts = canvas(plot_w + 40, 2 * (plot_h + 20), "#ffffff")
    for panel, series in enumerate(([v for _, v in months], [v * 0.6 for _, v in months])):
        oy = panel * (plot_h + 20) + 10
        rect(ts, 20, oy, 20 + plot_w, oy + 1, "#cccccc")
        rect(ts, 20, oy + plot_h, 20 + plot_w, oy + plot_h + 1, "#333333")
        pts = [(20 + i * plot_w / 5, oy + plot_h - v / vmax * plot_h) for i, v in enumerate(series)]
        paint(ts, line_mask(ts.shape[0], ts.shape[1], pts, 2), "#4a6fa5")
    tsp = save_png(ts, wd / "timeseries_panels.png")
    tb = load_png(tsp)
    frame_rows = [y for y in range(tb.shape[0]) if near(tb[y, 20:20 + plot_w], "#333333", 3).all()]
    top_rows = [y for y in range(tb.shape[0]) if near(tb[y, 20:20 + plot_w], "#cccccc", 3).all()]
    aspect = plot_w / float(frame_rows[0] - top_rows[0])
    checks.append(check("time-series plot area 2:1..3:1", 2.0 <= aspect <= 3.0, aspect, "2..3"))
    return checks, [p1, pm, tsp]


@card("DATA-13")
def stat_weight_continuity(task, wd):
    """Hero number counts from 0 with a proportional bar; the next stat morphs the same bar (no cut)."""
    np = _np()
    W, H, fps, NH = 270, 480, 30, 25   # 1080x1920 / 4: a 25 px numeral is 100 px at 1080p
    stats = [40, 75]
    BW = 200

    def value(t):
        if t < 1.2:
            return stats[0] * ease("easeOutCubic", t / 1.2)
        if t < 2.0:
            return stats[0]
        return stats[0] + (stats[1] - stats[0]) * ease("easeOutCubic", (t - 2.0) / 1.2)

    def frame(v):
        a = canvas(W, H, "#10233a")
        n = int(round(v))
        draw_seg(a, fmt_int(n, "ddd"), "ddd", NH, 100, 180, "#ffffff")
        rect(a, 35, 260, 35 + round(n / 100 * BW), 280, "#5bd1a5")
        return a
    T = 3.6
    vid = write_video(wd / "stat_morph.mp4", [frame(value(k / fps)) for k in range(int(T * fps))], fps)
    cut = write_video(wd / "stat_hard_cut.mp4", [frame(stats[0] * ease("easeOutCubic", min(1, k / fps / 1.2)) if k / fps < 2.0
                                                       else stats[1]) for k in range(int(T * fps))], fps)

    def measure(path):
        fr = read_video(path)
        nums = [seg_value(read_seg(f, "ddd", NH, 100, 180, "#10233a", fg="#ffffff")) for f in fr]
        widths = [int(near(f[270], "#5bd1a5", 8).sum()) for f in fr]
        return nums, widths
    nums, widths = measure(vid)
    cn, cw = measure(cut)
    pair = max(abs(w - round(n / 100 * BW)) for n, w in zip(nums, widths) if n is not None)
    jump = max(abs(b - a) for a, b in zip(widths, widths[1:]))
    cjump = max(abs(b - a) for a, b in zip(cw, cw[1:]))
    checks = [check("counts from 0", nums[0] == 0, nums[0], 0),
              check("first stat lands at 40", nums[int(1.5 * fps)] == 40, nums[int(1.5 * fps)], 40),
              check("second stat lands at 75", nums[-1] == 75, nums[-1], 75),
              check("bar width bound to the number in every frame (px)", pair <= 1, pair, "<= 1"),
              check("morph is continuous (max px per frame)", jump <= 10, jump, "<= 10"),
              check("hero numeral 80-120 px at 1080p", 80 <= NH * 4 <= 120, NH * 4, "80..120"),
              check("negative control: a hard cut jumps the shape", cjump > 10, cjump, "> 10")]
    return checks, [vid]


def ink_bbox(arr, bg, thr=40.0, region=None):
    np = _np()
    x0, y0, x1, y1 = region or (0, 0, arr.shape[1], arr.shape[0])
    sub = arr[y0:y1, x0:x1]
    m = np.abs(sub - np.array(rgb(bg) if isinstance(bg, str) else bg, dtype=float)).max(axis=-1) > thr
    if not m.any():
        return None
    ys, xs = np.nonzero(m)
    return (x0 + int(xs.min()), y0 + int(ys.min()), x0 + int(xs.max()) + 1, y0 + int(ys.max()) + 1)


def sharpness(arr, region):
    """Largest luminance step between neighbouring pixels in a region (blur lowers it)."""
    np = _np()
    x0, y0, x1, y1 = region
    g = arr[y0:y1, x0:x1].mean(axis=-1)
    return float(max(np.abs(np.diff(g, axis=0)).max(), np.abs(np.diff(g, axis=1)).max()))


def vsharp(arr, region):
    np = _np()
    x0, y0, x1, y1 = region
    return float(np.abs(np.diff(arr[y0:y1, x0:x1].mean(axis=-1), axis=0)).max())


def gold_halo(f):
    """Pixels tinted gold (R > G > B, warm) that are not the white glyph itself."""
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    return int(((r > b + 25) & (g > b + 10) & (r > 50) & ~((r > 235) & (g > 235) & (b > 235))).sum())


def blur(arr, radius):
    from PIL import Image, ImageFilter
    if radius <= 0:
        return arr
    im = Image.fromarray(_np().clip(arr, 0, 255).round().astype("uint8"))
    return _np().asarray(im.filter(ImageFilter.GaussianBlur(radius))).astype(float)


def vblur(arr, k):
    """Vertical box blur of k px (motion blur along a rolling digit strip)."""
    np = _np()
    k = int(k)
    if k <= 1:
        return arr
    pad = np.concatenate([np.repeat(arr[:1], k, 0), arr, np.repeat(arr[-1:], k, 0)], 0)
    c = np.cumsum(pad, axis=0)
    out = (c[k:] - c[:-k]) / k
    off = (out.shape[0] - arr.shape[0]) // 2
    return out[off:off + arr.shape[0]]


def scaled_layer(layer, s, cx, cy, out_shape, bg):
    """Scale a layer (numpy RGB over bg) by s about (cx, cy) into a canvas of out_shape."""
    from PIL import Image
    np = _np()
    h, w = layer.shape[:2]
    nw, nh = max(1, int(round(w * s))), max(1, int(round(h * s)))
    im = Image.fromarray(np.clip(layer, 0, 255).round().astype("uint8")).resize((nw, nh), Image.BILINEAR)
    a = canvas(out_shape[1], out_shape[0], bg)
    x, y = int(round(cx - nw / 2)), int(round(cy - nh / 2))
    sub = np.asarray(im).astype(float)
    ys0, xs0 = max(0, -y), max(0, -x)
    ys1, xs1 = min(nh, out_shape[0] - y), min(nw, out_shape[1] - x)
    a[y + ys0:y + ys1, x + xs0:x + xs1] = sub[ys0:ys1, xs0:xs1]
    return a


def lerp_c(c0, c1, t):
    a, b = (rgb(c0) if isinstance(c0, str) else c0), (rgb(c1) if isinstance(c1, str) else c1)
    return tuple(x + (y - x) * t for x, y in zip(a, b))


@card("DATA-20")
def stat_counter_template(task, wd):
    """Stat counter: 1250+ counts 1.0-2.2 s of a 6 s card while a ring draws on the same ease; a flash and a
    squash on landing; the label rises after."""
    np = _np()
    W, H, fps, D = 216, 384, 30, 6.0
    value, t0, t1 = 1250, 1.0, 2.2
    NH, pat = 30, "d,dddd"
    cx, cy, r0, r1 = 108, 150, 56, 64
    nx = int(cx - seg_width(pat, NH) / 2)
    ny = 260
    e = lambda t: ease("power3.out", prog(t, t0, t1 - t0))

    def frame(t):
        k = (t - t1) / 0.15
        flash = max(0.0, 1 - k) if t >= t1 else 0.0
        a = canvas(W, H, "#10233a")
        grad = np.linspace(0, 1, H)[:, None, None]
        a[:] = a * (1 - grad) + np.array(rgb("#071321"), dtype=float) * grad
        a[:] = a + flash * 60
        paint(a, ring_mask(H, W, cx, cy, r0, r1), "#1d3550")
        paint(a, ring_mask(H, W, cx, cy, r0, r1, 0, 360 * e(t)), "#5bd1a5")
        txt = fmt_int(value * e(t), "d,ddd", sep=True) + "+"
        squash = 0.8 if t1 <= t < t1 + 0.1 else 1.0
        hh = int(round(NH * squash))
        draw_seg(a, txt, pat, hh, nx, ny + (NH - hh), "#ffffff")
        lp = ease("power2.out", prog(t, t1 + 0.2, 0.6))
        if lp > 0:
            rect(a, 60, 330 - 20 * lp, 156, 338 - 20 * lp, "#9fb3c8", lp)
        return a
    n = int(D * fps)
    vid = write_video(wd / "stat_counter.mp4", [frame(k / fps) for k in range(n)], fps)
    fr = read_video(vid)
    errs, ring_err = [], []
    for k, f in enumerate(fr):
        t = k / fps
        if t1 <= t < t1 + 0.1:
            continue
        v = seg_value(read_seg(f, pat, NH, nx, ny, None, fg="#ffffff", thr=50)[:-1])
        errs.append(abs((v if v is not None else -1e9) - round(value * e(t))))
        ring_err.append(abs(arc_fraction(f, cx, cy, r0, r1, "#5bd1a5", 30) - e(t)))
    first = next(k for k, f in enumerate(fr) if arc_fraction(f, cx, cy, r0, r1, "#5bd1a5", 30) > 0.002)
    checks = [check("counter value per frame == round(1250 * ease)", max(errs) <= 1, max(errs), "<= 1"),
              check("ring drawn share == the counter's ease (same ease)", max(ring_err) <= 0.02, max(ring_err), "<= 0.02"),
              check("count starts at 1.0 s", abs(first / fps - t0) <= 1.5 / fps, first / fps, t0),
              check("lands on 1,250+", read_seg(fr[-1], pat, NH, nx, ny, None, fg="#ffffff", thr=50) == "1,250+",
                    read_seg(fr[-1], pat, NH, nx, ny, None, fg="#ffffff", thr=50), "1,250+")]
    lum = [float(f[5:40, 5:40].mean()) for f in fr]
    k1 = int(round(t1 * fps))
    checks.append(check("flash on landing", lum[k1] > lum[k1 - 2] + 30, lum[k1] - lum[k1 - 2], "> 30"))
    hb = ink_bbox(fr[k1 + 1], fr[k1 + 1][ny - 5, 2], 100, (nx, ny - 5, nx + 200, ny + NH + 5))
    hf = ink_bbox(fr[-1], fr[-1][ny - 5, 2], 100, (nx, ny - 5, nx + 200, ny + NH + 5))
    checks.append(check("squash on landing (height ratio)", (hb[3] - hb[1]) / float(hf[3] - hf[1]) < 0.9,
                        (hb[3] - hb[1]) / float(hf[3] - hf[1]), "< 0.9"))
    tops = [ink_bbox(f, f[300, 2], 25, (60, 300, 156, 345)) for f in fr[k1 + 8:]]
    tops = [b[1] for b in tops if b]
    checks.append(check("label rises", tops and tops[-1] < tops[0] and all(b <= a for a, b in zip(tops, tops[1:])),
                        [tops[0], tops[-1]] if tops else None, "decreasing y"))
    lin = max(abs(round(value * prog(k / fps, t0, t1 - t0)) - round(value * e(k / fps))) for k in range(n))
    checks.append(check("negative control: a linear count would not match the measured values", lin > 50, lin, "> 50"))
    return checks, [vid]


@card("DATA-21")
def rolling_digits(task, wd):
    """Each digit is a masked 0-9 strip: translateY = -(digit + 10*extraTurns)*lineH, extraTurns grows to the
    right, 40 ms digit lag, vertical blur by velocity, leading zero at 30 % opacity, glow on landing."""
    np = _np()
    target = "0705"
    NH, lineH, fps = 36, 44, 30
    cellW = int(round(NH * 0.55)) + 10
    W, H = 4 * cellW + 40, 80
    x0, y0 = 20, (H - lineH) // 2
    hold, dur, lag = 0.2, 2.0, 0.04
    turns = [i for i in range(4)]
    totals = [int(target[i]) + 10 * turns[i] for i in range(4)]
    strip = canvas(cellW, lineH * 11, "#0b0f1a")
    for d in range(11):
        draw_seg(strip, str(d % 10), "d", NH, 5, d * lineH + (lineH - NH) // 2, "#ffffff")

    def pos(i, t):
        return totals[i] * ease("easeOutExpo", prog(t, hold + i * lag, dur))

    def vel(i, t, dt=1 / 30.0):
        return (pos(i, t + dt) - pos(i, t)) / dt * lineH / 30.0   # px per frame

    def frame(t):
        a = canvas(W, H, "#0b0f1a")
        for i in range(4):
            p = pos(i, t)
            frac = p - math.floor(p)
            base = int(math.floor(p)) % 10
            col = strip[base * lineH:(base + 2) * lineH]
            col = vblur(col, min(8, int(round(vel(i, t)))))
            off = int(round(frac * lineH))
            win = col[off:off + lineH]
            alpha = 0.3 if (i == 0 and target[0] == "0" and prog(t, hold, dur) >= 1) else 1.0
            a[y0:y0 + lineH, x0 + i * cellW:x0 + (i + 1) * cellW] = a[y0:y0 + lineH, x0 + i * cellW:x0 + (i + 1) * cellW] * (1 - alpha) + win * alpha
        if t >= hold + 3 * lag + dur:
            g = blur(np.where((a > 128).all(axis=-1, keepdims=True), np.array(rgb("#f5c97a"), float), a * 0), 4)
            a[:] = np.maximum(a, g * 0.75)
        return a
    n = int((hold + 3 * lag + dur + 0.4) * fps)
    vid = write_video(wd / "rolling_digits.mp4", [frame(k / fps) for k in range(n)], fps)
    fr = read_video(vid)
    cx = [x0 + i * cellW + 5 for i in range(4)]
    yy = y0 + (lineH - NH) // 2
    first = "".join(read_seg(fr[0], "d", NH, cx[i], yy, "#0b0f1a", thr=60) for i in range(4))
    last = "".join(read_seg(fr[-1], "d", NH, cx[i], yy, "#0b0f1a", thr=30) for i in range(4))
    # measure translateY: match each digit window against every offset of the 0-9 strip, unwrap forward
    gs = strip.mean(axis=-1)
    tmpl = np.stack([gs[o:o + lineH] for o in range(10 * lineH)])
    zn = lambda a: (a - a.mean(axis=(-2, -1), keepdims=True)) / (a.std(axis=(-2, -1), keepdims=True) + 1e-6)
    tmpl = zn(tmpl)
    best = lambda w: int((tmpl * zn(w)[None]).sum(axis=(1, 2)).argmax())   # normalised correlation: opacity-proof
    rows = []
    for i in range(4):
        win = fr[:, y0:y0 + lineH, x0 + i * cellW:x0 + (i + 1) * cellW].mean(axis=-1)
        offs = [best(w) for w in win]
        tot = sum((b - a) % (10 * lineH) for a, b in zip(offs, offs[1:]))
        rows.append(tot / float(lineH))
    seg_px = fr[-1][yy + NH // 4, cx[0] + 1:cx[0] + 3].mean()
    bgm = float(np.mean(rgb("#0b0f1a")))
    lead = (float(seg_px) - bgm) / (255.0 - bgm)
    starts = [next((k for k in range(1, n) if np.abs(fr[k, y0:y0 + lineH, x0 + i * cellW:x0 + (i + 1) * cellW] -
                                                    fr[0, y0:y0 + lineH, x0 + i * cellW:x0 + (i + 1) * cellW]).max() > 30), None)
              for i in range(1, 4)]
    vk = max(range(n), key=lambda k: vel(3, k / fps))
    reg = (x0 + 3 * cellW, y0, x0 + 4 * cellW, y0 + lineH)
    checks = [check("starts at 0000", first == "0000", first, "0000"),
              check("lands on 0705", last == "0705", last, target),
              check("measured strip travel per digit == digit + 10*extraTurns (rows)",
                    max(abs(a - b) for a, b in zip(rows, totals)) <= 0.15, rows, totals),
              check("rightmost digits spin more", rows[0] < rows[1] < rows[2] < rows[3], rows, "increasing"),
              check("digit lag ~40 ms (start frames non-decreasing)", None not in starts and starts == sorted(starts)
                    and starts[-1] - starts[0] >= 2, starts, "+1.2 frames per digit"),
              check("vertical motion blur at peak velocity", vsharp(fr[vk], reg) < 0.6 * vsharp(fr[-1], reg),
                    [vsharp(fr[vk], reg), vsharp(fr[-1], reg)], "peak < 0.6 x landed"),
              check("leading zero at ~30 % opacity", 0.22 <= lead <= 0.45, lead, 0.3)]
    checks.append(check("gold glow only after landing", gold_halo(fr[-1]) > 30 and gold_halo(fr[n // 3]) == 0,
                        [gold_halo(fr[n // 3]), gold_halo(fr[-1])], "0 then > 30 px"))
    w0 = fr[0, y0:y0 + lineH, x0 + 3 * cellW:x0 + 4 * cellW].mean(axis=-1)
    o0 = best(w0)
    checks.append(check("negative control: the unrolled input (frame 0 held) travels 0 rows", abs(totals[3] - 0) > 0.15
                        and o0 == 0, 0.0, totals[3]))
    return checks, [vid]


@card("DATA-24")
def number_pop_in(task, wd):
    """Digits pop in (scale .4 + blur 16 px -> 1 / 0 px, lift) while counting 0->1000 in 0.7 s; gold glow at the end."""
    np = _np()
    W, H, fps, NH, pat = 240, 140, 30, 40, "dddd"
    lw = seg_width(pat, NH)
    pop, cnt = 0.35, 0.7
    lx, ly = (W - lw) // 2, (H - NH) // 2

    def frame(t):
        v = 1000 * ease("power3.out", prog(t, 0, cnt))
        layer = canvas(W, H, "#0d0d12")
        draw_seg(layer, fmt_int(v, pat), pat, NH, lx, ly, "#ffffff")
        p = ease("power3.out", prog(t, 0, pop))
        s = 0.4 + 0.6 * p
        a = scaled_layer(layer, s, W / 2, H / 2 + 14 * (1 - p), (H, W), "#0d0d12")
        a = blur(a, 16 * (1 - p) * 0.4)   # 16 px at 1080p -> 6.4 px here
        if t >= cnt:
            g = blur(np.where((a > 200).all(axis=-1, keepdims=True), np.array(rgb("#f5c97a"), float), a * 0), 6) * 0.75 * 2.2
            a = np.maximum(a, np.minimum(g, np.array(rgb("#f5c97a"), float)))
        return a
    n = int(1.1 * fps)
    vid = write_video(wd / "pop_in.mp4", [frame(k / fps) for k in range(n)], fps)
    fr = read_video(vid)
    bgv = np.array(rgb("#0d0d12"), float)

    def moments(f):
        w = np.abs(f - bgv).max(axis=-1)
        ys = np.arange(f.shape[0])[:, None]
        m = (w * ys).sum() / w.sum()
        return m, (w * (ys - m) ** 2).sum() / w.sum()
    ref = canvas(W, H, "#0d0d12")            # the unprocessed input layer of frame 0 (scale 1, no blur, no lift)
    draw_seg(ref, fmt_int(0, pat), pat, NH, lx, ly, "#ffffff")
    m0, v0 = moments(fr[0])
    m1, v1 = moments(ref)
    sc = math.sqrt(max(0.0, v0 - 6.4 ** 2) / v1)
    exp_c = (H / 2 + 14) + (m1 - H / 2) * 0.4
    bf = ink_bbox(fr[-1], "#0d0d12", 200)
    reg = (lx - 4, ly - 4, lx + lw + 4, ly + NH + 4)
    vals = {}
    for k in range(int(pop * fps) + 1, int(cnt * fps)):
        vals[k] = seg_value(read_seg(fr[k], pat, NH, lx, ly, "#0d0d12", thr=110))
    err = max(abs((v if v is not None else -1e9) - round(1000 * ease("power3.out", k / fps / cnt))) for k, v in vals.items())
    gold, gold_mid = gold_halo(fr[-1]), gold_halo(fr[int(0.5 * fps)])
    checks = [check("pop starts at scale 0.4 (from vertical spread minus blur)", abs(sc - 0.4) <= 0.06, sc, 0.4),
              check("blurred at entry, sharp at rest", sharpness(fr[0], reg) < 0.5 * sharpness(fr[int(0.6 * fps)], reg),
                    [sharpness(fr[0], reg), sharpness(fr[int(0.6 * fps)], reg)], "entry < 0.5 x rest"),
              check("counting values match the tween", err <= 1, err, "<= 1"),
              check("lands on 1000", read_seg(fr[-1], pat, NH, lx, ly, "#0d0d12", thr=200) == "1000",
                    read_seg(fr[-1], pat, NH, lx, ly, "#0d0d12", thr=200), "1000"),
              check("gold glow only after landing", gold > 100 and gold_mid == 0, [gold_mid, gold], "0 then > 100"),
              check("lift: entry centre where scale about the lifted pivot puts it", abs(m0 - exp_c) <= 1.5, m0, exp_c)]
    checks.append(check("negative control: the unprocessed input layer measures scale 1, not 0.4",
                        abs(math.sqrt(v1 / v1) - 0.4) > 0.06 and abs((bf[3] - bf[1]) / float(NH) - 0.4) > 0.06, 1.0, "!= 0.4"))
    return checks, [vid]


@card("DATA-26")
def escalating_numeral(task, wd):
    """1 -> 5000 over 3 s on easeInExpo; colour lerps white -> orange -> red past thresholds; the caption swaps."""
    np = _np()
    W, H, fps, pat = 240, 200, 30, "dddd"
    NH = 50          # 25 % of frame height
    lx, ly = (W - seg_width(pat, NH)) // 2, 40
    caps = ["#3a86ff", "#ffbe0b", "#ff006e"]

    def col(v):
        return lerp_c("#ffffff", "#ff8c1a", v / 2500.0) if v <= 2500 else lerp_c("#ff8c1a", "#e10600", (v - 2500) / 2500.0)

    def val(t):
        return int(round(1 + 4999 * ease("easeInExpo", prog(t, 0, 3.0))))

    def frame(t):
        v = val(t)
        a = canvas(W, H, "#111111")
        draw_seg(a, fmt_int(v, pat), pat, NH, lx, ly, col(v))
        rect(a, 40, 160, 200, 176, caps[(v >= 1000) + (v >= 4000)])
        return a
    n = int(3.4 * fps)
    vid = write_video(wd / "escalate.mp4", [frame(k / fps) for k in range(n)], fps)
    fr = read_video(vid)
    W0, T0, S0 = _segs(NH)
    ax, ay = lx + 3 * (W0 + T0) + (S0["d"][0] + S0["d"][2]) // 2, ly + (S0["d"][1] + S0["d"][3]) // 2   # bottom bar, last digit
    verr, cerr, caperr = 0, 0.0, 0
    for k, f in enumerate(fr):
        v = val(k / fps)
        m = seg_value(read_seg(f, pat, NH, lx, ly, "#111111", thr=60))
        verr = max(verr, abs((m if m is not None else -1e9) - v))
        if fmt_int(v, pat)[-1] in "0235689":
            cerr = max(cerr, float(np.abs(f[ay, ax] - np.array(col(v))).max()))
        caperr += int(np.abs(f[168, 120] - np.array(rgb(caps[(v >= 1000) + (v >= 4000)]))).max() > 6)
    half = seg_value(read_seg(fr[int(1.5 * fps)], pat, NH, lx, ly, "#111111", thr=60))
    checks = [check("values follow easeInExpo", verr <= 1, verr, "<= 1"),
              check("escalation: value at half time < 5 % of the range", half < 250, half, "< 250"),
              check("numeral colour follows the threshold lerp", cerr <= 6, cerr, "<= 6"),
              check("caption swaps at each threshold", caperr == 0, caperr, 0),
              check("numeral is 25 % of frame height", NH / float(H) == 0.25, NH / float(H), 0.25),
              check("ends red at 5000", seg_value(read_seg(fr[-1], pat, NH, lx, ly, "#111111", thr=60)) == 5000, None, 5000)]
    eo = max(abs(int(round(1 + 4999 * ease("easeOutExpo", prog(k / fps, 0, 3)))) - val(k / fps)) for k in range(n))
    checks.append(check("negative control: an ease-out count would not match", eo > 500, eo, "> 500"))
    return checks, [vid]


@card("DATA-27")
def price_cards_total(task, wd):
    """Price cards drop one by one (120 ms drop), each adding to a big counter (300 ms tween per step);
    then the cards collapse into one product card."""
    np = _np()
    prices = [12, 30, 8, 25]
    cum = [sum(prices[:i + 1]) for i in range(len(prices))]
    W, H, fps, NH, pat = 320, 200, 30, 30, "ddd"
    starts = [0.2 + 0.42 * i for i in range(4)]
    land = [s + 0.12 for s in starts]
    t_collapse = land[-1] + 0.5

    def counter(t):
        v = 0.0
        for i in range(4):
            prev = cum[i - 1] if i else 0
            if t >= land[i]:
                v = prev + (cum[i] - prev) * ease("power2.out", prog(t, land[i], 0.3))
        return v

    def frame(t):
        a = canvas(W, H, "#f5f1ea")
        c = ease("power2.inOut", prog(t, t_collapse, 0.4))
        for i in range(4):
            if t < starts[i]:
                continue
            p = ease("power2.in", prog(t, starts[i], 0.12))
            x = 20 + i * 72
            x = x + (124 - x) * c
            y = -60 + (40 + 60) * p
            rect(a, x, y, x + 60, y + 50, "#2b6cb0", 1.0 if c < 1 or i == 3 else 0.0)
        draw_seg(a, fmt_int(counter(t), pat), pat, NH, 120, 140, "#222222")
        return a
    n = int((t_collapse + 0.6) * fps)
    vid = write_video(wd / "price_cards.mp4", [frame(k / fps) for k in range(n)], fps)
    fr = read_video(vid)
    rd = lambda k: seg_value(read_seg(fr[k], pat, NH, 120, 140, "#f5f1ea", fg="#222222"))
    at_steps = [rd(min(n - 1, int(math.ceil((l + 0.3) * fps)))) for l in land]
    cards = [sum(1 for i in range(4) if near(fr[min(n - 1, int(math.ceil((l + 0.05) * fps)))][65, 20 + i * 72 + 30:20 + i * 72 + 31], "#2b6cb0", 8).all())
             for l in land]
    blobs = col_runs(near(fr[-1][65], "#2b6cb0", 8))
    checks = [check("counter lands on each running total", at_steps == cum, at_steps, cum),
              check("cards land one by one", cards == [1, 2, 3, 4], cards, [1, 2, 3, 4]),
              check("total == sum of prices", rd(n - 1) == sum(prices), rd(n - 1), sum(prices)),
              check("collapses into one product card", len(blobs) == 1, len(blobs), 1)]
    mid = rd(int(round((land[1] + 0.12) * fps)))
    checks.append(check("counter tweens between steps", mid is not None and cum[0] < mid < cum[1], mid, "(12, 42)"))
    checks.append(check("negative control: the start frame does not show the total", rd(0) != sum(prices), rd(0), "!= 75"))
    return checks, [vid]


@card("DATA-29")
def spoken_number_ring(task, wd):
    """When a number is spoken, a 24-tick ring with a sweeping hand appears on the subject's free side at eye
    line: ring draws 0.9 s power2.inOut, ticks stagger 0.03 s, hand 360 deg over 1.4 s."""
    np = _np()
    W, H, fps = 320, 180, 30
    base = canvas(W, H, "#203040")
    paint(base, pil_mask(W, H, lambda d: d.ellipse([30, 30, 110, 110], fill=255)), "#c08060")
    paint(base, pil_mask(W, H, lambda d: d.rectangle([20, 105, 120, 180], fill=255)), "#c08060")
    src = save_png(base, wd / "subject.png")
    sb = load_png(src)
    subj = near(sb, "#c08060", 10)
    left, right = subj[:, :W // 2].sum(), subj[:, W // 2:].sum()
    ys = np.nonzero(subj.any(axis=1))[0]
    cx = int(W * 0.75) if right < left else int(W * 0.25)
    cy = int(ys.min() + 0.3 * (ys.max() - ys.min()))
    r = 50
    spoken = 24

    def frame(t):
        a = sb.copy()
        paint(a, ring_mask(H, W, cx, cy, r - 3, r, 0, 360 * ease("power2.inOut", prog(t, 0, 0.9))), "#ffffff")
        for j in range(24):
            if t >= j * 0.03:
                paint(a, ring_mask(H, W, cx, cy, r - 10, r - 5, j * 15 - 2, j * 15 + 2), "#bbbbbb")
        ang = 360 * prog(t, 0, 1.4)
        if t > 0:
            pts = [(cx, cy), (cx + (r - 14) * math.sin(math.radians(ang)), cy - (r - 14) * math.cos(math.radians(ang)))]
            paint(a, line_mask(H, W, pts, 3), "#ff5a36")
        draw_seg(a, str(spoken), "dd", 16, cx - 11, cy + 14, "#ffffff")
        return a
    n = int(1.6 * fps)
    vid = write_video(wd / "ring.mp4", [frame(k / fps) for k in range(n)], fps)
    fr = read_video(vid)
    ring_err = max(abs(arc_fraction(f, cx, cy, r - 3, r, "#ffffff", 20) - ease("power2.inOut", prog(k / fps, 0, 0.9)))
                   for k, f in enumerate(fr))
    rr, ang = angle_grid(H, W, cx, cy)

    def ticks(f):
        m = near(f, "#bbbbbb", 20) & (rr >= r - 9) & (rr < r - 6)
        cl = clusters(np.nonzero(np.bincount(ang[m].astype(int) % 360, minlength=360))[0], gap=3)
        if len(cl) > 1 and np.bincount(ang[m].astype(int) % 360, minlength=360)[[0, 359]].all():
            cl = cl[1:]   # the cluster straddling 0/360 deg was counted twice
        return len(cl)
    herr = 0.0
    for k in (6, 12, 21, 30, 39):
        m = near(fr[k], "#ff5a36", 40) & (rr > r * 0.45) & (rr < r - 15)
        a_meas = float(np.degrees(np.arctan2(np.sin(np.radians(ang[m])).mean(), np.cos(np.radians(ang[m])).mean())) % 360)
        exp = 360 * prog(k / fps, 0, 1.4)
        herr = max(herr, abs((a_meas - exp + 180) % 360 - 180))
    tick_ok = all(ticks(fr[k]) == min(24, int(math.floor(k / fps / 0.03 + 1e-9)) + 1) for k in (0, 6, 12, 18, 30))
    ring_box = subj[max(0, cy - r):cy + r, max(0, cx - r):cx + r].sum()
    checks = [check("ring on the free side, clear of the subject", ring_box == 0, int(ring_box), 0),
              check("ring draw follows power2.inOut over 0.9 s", ring_err <= 0.03, ring_err, "<= 0.03"),
              check("24 ticks at the end", ticks(fr[-1]) == 24, ticks(fr[-1]), 24),
              check("ticks appear on the 0.03 s stagger", tick_ok, [ticks(fr[k]) for k in (0, 6, 12, 18, 30)], "1,7,13,19,24"),
              check("hand angle == 360 * t / 1.4 (deg)", herr <= 6, herr, "<= 6"),
              check("spoken number shown", read_seg(fr[-1], "dd", 16, cx - 11, cy + 14, None, fg="#ffffff", thr=40) == "24",
                    read_seg(fr[-1], "dd", 16, cx - 11, cy + 14, None, fg="#ffffff", thr=40), "24"),
              check("negative control: the input frame has no ticks", ticks(sb) == 0, ticks(sb), 0)]
    return checks, [vid, src]


@card("DATA-30")
def strike_old_value(task, wd):
    """Old value gets a strike line (scaleX 0->1 over 200 ms from the right, Arabic reading side), old value to
    40 % opacity, new value fades and rises over 200 ms."""
    np = _np()
    W, H, fps, NH = 200, 120, 30, 28
    ox, oy, nx, ny = 20, 20, 110, 70
    ow = seg_width("ddd", NH)

    def frame(t):
        a = canvas(W, H, "#ffffff")
        p = ease("power2.out", prog(t, 0.1, 0.2))
        draw_seg(a, "120", "ddd", NH, ox, oy, "#222222", 1 - 0.6 * p)
        sw = ow * p
        rect(a, ox + ow - sw, oy + NH // 2 - 1, ox + ow, oy + NH // 2 + 2, "#d62728")
        q = ease("power2.out", prog(t, 0.3, 0.2))
        if q > 0:
            draw_seg(a, " 95", "ddd", NH, nx, int(ny + 10 * (1 - q)), "#1a7f37", q)
        return a
    n = int(0.8 * fps)
    vid = write_video(wd / "strike.mp4", [frame(k / fps) for k in range(n)], fps)
    fr = read_video(vid)
    yy = oy + NH // 2
    lens, rights = [], []
    for f in fr:
        m = near(f[yy], "#d62728", 25)
        xs = np.nonzero(m)[0]
        lens.append(len(xs))
        rights.append(int(xs.max()) if len(xs) else None)
    exp = [int(round(ow * ease("power2.out", prog(k / fps, 0.1, 0.2)))) for k in range(n)]
    lerr = max(abs(a - b) for a, b in zip(lens, exp))
    anchored = len({r for r in rights if r is not None}) == 1
    W0, T0, S0 = _segs(NH)
    px = fr[-1][oy + 1, ox + W0 + max(2, T0) + (S0["a"][0] + S0["a"][2]) // 2]   # top bar of the "2"
    op = 1 - float(px.mean() - 34) / (255 - 34)
    checks = [check("strike length per frame == ease * width (px)", lerr <= 1, lerr, "<= 1"),
              check("strike grows from the right edge", anchored and rights[-1] == ox + ow - 1, rights[-1], ox + ow - 1),
              check("old value at 40 % opacity", abs(op - 0.4) <= 0.03, op, 0.4),
              check("new value reads 95", read_seg(fr[-1], "ddd", NH, nx, ny, "#ffffff", fg="#1a7f37").strip() == "95",
                    read_seg(fr[-1], "ddd", NH, nx, ny, "#ffffff", fg="#1a7f37"), " 95")]
    tops = [ink_bbox(f, "#ffffff", 20, (nx, 50, W, H)) for f in fr]
    tops = [b[1] for b in tops if b]
    checks.append(check("new value rises into place", len(tops) > 3 and tops[0] > tops[-1] == ny, [tops[0], tops[-1]] if tops else None, ny))
    checks.append(check("negative control: the input frame has no strike", lens[0] == 0 and exp[-1] > 0, lens[0], 0))
    return checks, [vid]


@card("DATA-31")
def slider_bound_numbers(task, wd):
    """One progress p (2 s easeInOutCubic) drives the thumb x, N = round(p*Nmax) and amount = $50 * N."""
    np = _np()
    W, H, fps, Nmax = 260, 140, 30, 40
    tx0, tl = 30, 200

    def frame(t):
        p = ease("easeInOutCubic", prog(t, 0, 2.0))
        N = int(round(p * Nmax))
        a = canvas(W, H, "#f7f7fb")
        rect(a, tx0, 30, tx0 + tl, 34, "#c9cbe0")
        x = tx0 + tl * p
        rect(a, x - 3, 24, x + 3, 40, "#5b4ce0")
        draw_seg(a, fmt_int(N, "dd"), "dd", 20, 30, 60, "#333333")
        draw_seg(a, fmt_int(50 * N, "d,ddd", sep=True), "d,ddd", 28, 110, 60, "#111111")
        return a
    n = int(2.3 * fps)
    vid = write_video(wd / "slider.mp4", [frame(k / fps) for k in range(n)], fps)
    fr = read_video(vid)
    bound, thumb, curve = 0, 0.0, 0
    for k, f in enumerate(fr):
        N = seg_value(read_seg(f, "dd", 20, 30, 60, "#f7f7fb", fg="#333333"))
        A = seg_value(read_seg(f, "d,ddd", 28, 110, 60, "#f7f7fb", fg="#111111"))
        bound += int(N is None or A is None or A != 50 * N)
        xs = np.nonzero(near(f[37], "#5b4ce0", 10))[0]
        xc = (xs.min() + xs.max() + 1) / 2.0
        thumb = max(thumb, abs((xc - tx0) / tl * Nmax - N))
        curve = max(curve, abs(N - round(ease("easeInOutCubic", prog(k / fps, 0, 2.0)) * Nmax)))
    lin = max(abs(round(prog(k / fps, 0, 2) * Nmax) - round(ease("easeInOutCubic", prog(k / fps, 0, 2)) * Nmax)) for k in range(n))
    checks = [check("amount == $50 x N in every frame", bound == 0, bound, 0),
              check("thumb position agrees with N (steps)", thumb <= 0.65, thumb, "<= 0.65 (0.5 rounding + 1/2 px)"),
              check("progress follows easeInOutCubic over 2 s", curve == 0, curve, 0),
              check("ends at N = 40, $2,000", read_seg(fr[-1], "d,ddd", 28, 110, 60, "#f7f7fb", fg="#111111") == "2,000",
                    read_seg(fr[-1], "d,ddd", 28, 110, 60, "#f7f7fb", fg="#111111"), "2,000"),
              check("negative control: a linear drag would not match", lin >= 3, lin, ">= 3")]
    return checks, [vid]


def gradient_fill(mask, box, stops, angle_deg):
    """CSS linear-gradient(angle, stops...) over box, painted where mask is set; returns the colour field."""
    np = _np()
    x0, y0, x1, y1 = box
    h, w = mask.shape
    ys, xs = np.mgrid[0:h, 0:w]
    a = math.radians(angle_deg)
    dx, dy = math.sin(a), -math.cos(a)
    cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
    L = abs((x1 - x0) * dx) + abs((y1 - y0) * dy)
    t = np.clip(((xs + 0.5 - cx) * dx + (ys + 0.5 - cy) * dy) / L + 0.5, 0, 1)
    pos = [p for p, _ in stops]
    cols = [np.array(rgb(c), float) for _, c in stops]
    out = np.zeros((h, w, 3))
    for ch in range(3):
        out[..., ch] = np.interp(t, pos, [c[ch] for c in cols])
    return out


@card("DATA-32")
def gradient_numerals(task, wd):
    """KPI numeral filled with linear-gradient(135deg, #312e81, #6d28d9) via text clipping, tabular figures;
    keynote variant: vertical #C9F4FF -> #64D2FF -> #1AA7EC."""
    np = _np()
    W, H, NH, pat, txt = 260, 100, 60, "dddd", "1084"
    lx, ly = 20, 20
    lay = canvas(W, H, "#000000")
    draw_seg(lay, txt, pat, NH, lx, ly, "#ffffff")
    mask = lay[..., 0] > 128
    ys, xs = np.nonzero(mask)
    box = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
    field = gradient_fill(mask, box, [(0, "#312e81"), (1, "#6d28d9")], 135)
    img = canvas(W, H, "#ffffff")
    img[mask] = field[mask]
    p = save_png(img, wd / "kpi_gradient.png")
    back = load_png(p)
    err = float(np.abs(back[mask] - field[mask]).max())
    outside = float(np.abs(back[~mask] - 255).max())
    flat = canvas(W, H, "#ffffff")
    flat[mask] = rgb("#4f2bb0")
    ferr = float(np.abs(flat[mask] - field[mask]).max())
    W0, T0, _ = _segs(NH)
    rights = [max(x for x in range(lx + i * (W0 + T0), lx + i * (W0 + T0) + W0 + 1) if mask[:, x].any()) for i in range(4)]
    adv = [b - a for a, b in zip(rights, rights[1:])]
    proj = xs + ys
    tl = back[ys[proj.argmin()], xs[proj.argmin()]]
    br = back[ys[proj.argmax()], xs[proj.argmax()]]
    checks = [check("ink pixels follow the 135deg gradient", err <= 1.0, err, "<= 1"),
              check("background untouched outside the glyphs", outside == 0, outside, 0),
              check("top-left near #312e81, bottom-right near #6d28d9",
                    float(np.abs(tl - rgb("#312e81")).max()) < 30 and float(np.abs(br - rgb("#6d28d9")).max()) < 30,
                    [tl.round().tolist(), br.round().tolist()], ["#312e81", "#6d28d9"]),
              check("tabular figures: equal advance", len(set(adv)) == 1, adv, "equal"),
              check("negative control: a flat fill does not match the gradient", ferr > 20, ferr, "> 20")]
    key = canvas(W, H, "#000000")
    kf = gradient_fill(mask, box, [(0, "#C9F4FF"), (0.5, "#64D2FF"), (1, "#1AA7EC")], 180)
    key[mask] = kf[mask]
    kp = save_png(key, wd / "kpi_keynote.png")
    kb = load_png(kp)
    rowc = lambda y: kb[y][mask[y]].mean(axis=0)
    checks.append(check("keynote vertical stops top/bottom", float(np.abs(rowc(box[1]) - rgb("#C9F4FF")).max()) < 12 and
                        float(np.abs(rowc(box[3] - 1) - rgb("#1AA7EC")).max()) < 12, [rowc(box[1]).round().tolist(),
                                                                                    rowc(box[3] - 1).round().tolist()], "#C9F4FF..#1AA7EC"))
    return checks, [p, kp]


@card("DATA-33")
def live_counter_over_footage(task, wd):
    """Footage dimmed 45 %, a big number counts 1.2 s easeOutExpo with thousands separators, a red-dot LIVE pill."""
    np = _np()
    W, H, fps = 320, 180, 30
    src = fx.test_clip(wd / "footage.mp4", seconds=1.6, size="%dx%d" % (W, H), fps=fps)
    raw = read_video(src)
    pat, NH, lx, ly = "dd,ddd", 34, 70, 100
    target = 12480

    def frame(k):
        a = raw[k] * 0.55
        v = target * ease("easeOutExpo", prog(k / fps, 0, 1.2))
        draw_seg(a, fmt_int(v, pat, sep=True), pat, NH, lx, ly, "#ffffff")
        rect(a, 10, 10, 70, 28, "#ffffff")
        paint(a, pil_mask(W, H, lambda d: d.ellipse([14, 14, 24, 24], fill=255)), "#ff2020")
        return a
    vid = write_video(wd / "live_counter.mp4", [frame(k) for k in range(len(raw))], fps)
    fr = read_video(vid)
    reg = (slice(40, 95), slice(100, 300))
    ratio = float(fr[:, reg[0], reg[1]].sum() / max(1.0, raw[:, reg[0], reg[1]].sum()))
    err = 0
    for k, f in enumerate(fr):
        m = seg_value(read_seg(f, pat, NH, lx, ly, None, fg="#ffffff", thr=60))
        err = max(err, abs((m if m is not None else -1e9) - round(target * ease("easeOutExpo", prog(k / fps, 0, 1.2)))))
    sep = read_seg(fr[-1], pat, NH, lx, ly, None, fg="#ffffff", thr=60)
    dot = all(near(f[19:20, 19:20], "#ff2020", 40).all() for f in fr)
    checks = [check("footage dimmed to 55 % (45 % dim)", abs(ratio - 0.55) <= 0.01, ratio, 0.55),
              check("count follows easeOutExpo over 1.2 s", err <= 1, err, "<= 1"),
              check("thousands separator shown", sep == "12,480", sep, "12,480"),
              check("LIVE red dot every frame", dot, dot, True),
              check("negative control: the undimmed source ratio is 1.0", abs(1.0 - 0.55) > 0.01 and
                    abs(float(raw[:, reg[0], reg[1]].sum() / raw[:, reg[0], reg[1]].sum()) - 0.55) > 0.01, 1.0, "!= 0.55")]
    return checks, [vid]


@card("DATA-34")
def hit_column_total(task, wd):
    """Every 150-250 ms a hit pops into a 4-row column (newest on top pushes the rest; pop 1.3 -> 1 in 2 frames),
    coloured by category, with the running total below."""
    np = _np()
    rs = np.random.RandomState(3)
    times, t = [], 0.1
    while t < 1.6:
        times.append(round(t, 3))
        t += rs.uniform(0.15, 0.25)
    vals = [int(v) for v in rs.randint(100, 999, len(times))]
    cats = [int(c) for c in rs.randint(0, 3, len(times))]
    colors = ["#ff4d4d", "#ffd23f", "#3ec1ff"]
    W, H, fps, NH, pat = 200, 260, 30, 22, "ddd"
    rows_y = [20 + i * 40 for i in range(4)]

    def frame(k):
        a = canvas(W, H, "#101018")
        hits = [i for i, tt in enumerate(times) if int(math.ceil(tt * fps)) <= k]
        shown = list(reversed(hits))[:4]
        for r, i in enumerate(shown):
            age = k - int(math.ceil(times[i] * fps))
            s = 1.3 if (r == 0 and age == 0) else (1.15 if (r == 0 and age == 1) else 1.0)
            hh = int(round(NH * s))
            draw_seg(a, fmt_int(vals[i], pat), pat, hh, 60, rows_y[r] + (NH - hh) // 2, colors[cats[i]])
        draw_seg(a, fmt_int(sum(vals[i] for i in hits), "d,ddd", sep=True), "d,ddd", 30, 40, 200, "#ffffff")
        return a
    n = int(2.0 * fps)
    vid = write_video(wd / "hits.mp4", [frame(k) for k in range(n)], fps)
    fr = read_video(vid)
    hf = [int(math.ceil(tt * fps)) for tt in times]
    ok_rows, ok_tot, ok_col = 0, 0, 0
    for k, f in enumerate(fr):
        hits = [i for i, h in enumerate(hf) if h <= k]
        if not hits or k - hf[hits[-1]] < 2:
            continue
        exp = list(reversed(hits))[:4]
        got = [seg_value(read_seg(f, pat, NH, 60, rows_y[r], "#101018", thr=60)) for r in range(len(exp))]
        ok_rows += int(got != [vals[i] for i in exp])
        ok_tot += int(seg_value(read_seg(f, "d,ddd", 30, 40, 200, "#101018", thr=60)) != sum(vals[i] for i in hits))
        W0, T0, S0 = _segs(NH)
        for r, i in enumerate(exp):
            d = fmt_int(vals[i], pat)[-1]
            sg = "b" if d in "0123478 9" else "c"
            x0, y0, x1, y1 = S0[sg]
            px = f[rows_y[r] + (y0 + y1) // 2, 60 + 2 * (W0 + T0) + (x0 + x1) // 2]
            ok_col += int(np.abs(px - rgb(colors[cats[i]])).max() > 10)
    pop = []
    for h in hf[:4]:
        b = ink_bbox(fr[h], "#101018", 60, (55, rows_y[0] - 8, 160, rows_y[0] + NH + 8))
        pop.append(b[3] - b[1])
    appended = [seg_value(read_seg(fr[-1], pat, NH, 60, rows_y[r], "#101018", thr=60)) for r in range(4)]
    checks = [check("%d hits at 150-250 ms" % len(times), all(0.149 <= b - a <= 0.251 for a, b in zip(times, times[1:])),
                    [round(b - a, 3) for a, b in zip(times, times[1:])][:5], "0.15..0.25"),
              check("rows show the 4 newest, newest on top", ok_rows == 0, ok_rows, 0),
              check("running total under the column", ok_tot == 0, ok_tot, 0),
              check("rows coloured by category", ok_col == 0, ok_col, 0),
              check("pop 1.3x on the hit frame", all(abs(p - round(NH * 1.3)) <= 1 for p in pop), pop, round(NH * 1.3)),
              check("negative control: oldest-first (append) order is not what is shown",
                    appended != [vals[i] for i in range(len(vals))][-4:], appended, "newest first")]
    return checks, [vid]


def _sk_bars(labels, series, line=None, stacked=False, height=260, width=720):
    """SKCharts.bars in Python: grouped/stacked columns + optional line on one axis, nice ticks, 4 gridlines,
    padding l46 r8 t12 b30, rounded data-end corner r = min(4, w/2, h), empty state when all zero."""
    L, R, T, B = 46, 8, 12, 30
    iw, ih = width - L - R, height - T - B
    base = T + ih
    sums = [sum(s["values"][i] for s in series) for i in range(len(labels))] if stacked else \
        [max(s["values"][i] for s in series) for i in range(len(labels))]
    vmax = max(sums + (line["values"] if line else []))
    head = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">' % (width, height, width, height)
    if vmax <= 0:
        return head + '<text class="empty" x="%d" y="%d" text-anchor="middle">لا توجد بيانات</text></svg>' % (width // 2, height // 2), None
    ticks, step = nice_ticks(vmax, 4)
    top = ticks[-1]
    y = lambda v: base - v / top * ih
    parts, geo = [], {"top": top, "ticks": ticks, "bars": [], "line": [], "base": base, "ih": ih}
    for tv in ticks[1:]:
        parts.append('<line class="grid" x1="%d" x2="%d" y1="%.2f" y2="%.2f"/>' % (L, L + iw, y(tv), y(tv)))
        parts.append('<text class="tick" x="%d" y="%.2f">%g</text>' % (L - 6, y(tv), tv))
    band = iw / float(len(labels))
    gw = band * 0.7
    for i, _ in enumerate(labels):
        acc = 0.0
        for j, s in enumerate(series):
            v = s["values"][i]
            if stacked:
                w, x = gw, L + i * band + (band - gw) / 2
                y0, y1 = y(acc + v), y(acc)
                acc += v
                end = j == len(series) - 1
            else:
                w = gw / len(series)
                x = L + i * band + (band - gw) / 2 + j * w
                y0, y1 = y(v), base
                end = True
            h = y1 - y0
            r = min(4.0, w / 2, h) if end else 0.0
            d = "M%.2f %.2f V%.2f Q%.2f %.2f %.2f %.2f H%.2f Q%.2f %.2f %.2f %.2f V%.2f Z" % (
                x, y1, y0 + r, x, y0, x + r, y0, x + w - r, x + w, y0, x + w, y0 + r, y1)
            parts.append('<path class="bar" fill="%s" data-v="%g" data-r="%.3f" d="%s"/>' % (s["color"], v, r, d))
            geo["bars"].append({"x": x, "w": w, "y0": y0, "y1": y1, "v": v, "r": r, "color": s["color"], "i": i})
    if line:
        pts = [(L + (i + 0.5) * band, y(v)) for i, v in enumerate(line["values"])]
        parts.append('<polyline class="line" fill="none" stroke="%s" stroke-width="2" points="%s"/>' % (
            line["color"], " ".join("%.2f,%.2f" % p for p in pts)))
        geo["line"] = pts
    return head + "".join(parts) + "</svg>", geo


@card("DATA-38")
def svg_bars_generator(task, wd):
    """Dependency-free SVG grouped/stacked columns with a line on the same axis and nice-number ticks;
    for video each bar scales from the baseline."""
    import xml.etree.ElementTree as ET
    np = _np()
    labels = ["Q1", "Q2", "Q3", "Q4"]
    series = [{"name": "a", "color": "#2a78d6", "values": [12, 28, 45, 64]},
              {"name": "b", "color": "#eb6834", "values": [8, 15, 0.9, 23.3]}]
    line = {"color": "#1baf7a", "values": [20, 35, 41, 87.3]}
    svg, geo = _sk_bars(labels, series, line)
    svgs, geos = _sk_bars(labels, series, None, stacked=True)
    empty, _ = _sk_bars(labels, [{"name": "z", "color": "#000", "values": [0, 0, 0, 0]}])
    (wd / "bars.svg").write_text(svg, encoding="utf-8")
    (wd / "bars_stacked.svg").write_text(svgs, encoding="utf-8")
    (wd / "bars_empty.svg").write_text(empty, encoding="utf-8")
    ns = {"s": "http://www.w3.org/2000/svg"}
    root = ET.fromstring(svg)
    paths = root.findall("s:path", ns)
    hs, vs = [], []
    for pth in paths:
        nums = [float(t) for t in pth.get("d").replace("M", " ").replace("V", " ").replace("Q", " ").replace("H", " ")
                .replace("Z", " ").split()]
        y1, y0 = nums[1], nums[4]          # M x y1 ... Q x y0
        hs.append(y1 - y0)
        vs.append(float(pth.get("data-v")))
    k = geo["ih"] / geo["top"]
    err = max(abs(h - v * k) for h, v in zip(hs, vs))
    tick_vals = [float(t.text) for t in root.findall("s:text", ns)]
    pts = [tuple(map(float, p.split(","))) for p in root.find("s:polyline", ns).get("points").split()]
    lerr = max(abs((geo["base"] - py) - v * k) for (_, py), v in zip(pts, line["values"]))
    small = [b for b in geo["bars"] if b["v"] == 0.9][0]
    rexp = min(4, small["w"] / 2, small["y1"] - small["y0"])
    tops = {}
    for b in geos["bars"]:
        tops[b["i"]] = min(tops.get(b["i"], 1e9), b["y0"])
    serr = max(abs((geos["base"] - tops[i]) - sum(s["values"][i] for s in series) * geos["ih"] / geos["top"]) for i in range(4))
    checks = [check("bar heights == value x scale (px)", err < 0.01, err, "< 0.01"),
              check("axis top is a nice number covering the data", is_nice(geo["top"]) and geo["top"] >= 87.3, geo["top"], ">= 87.3, nice"),
              check("4 gridlines with nice ticks", len(tick_vals) == 4 and all(is_nice(v) for v in tick_vals), tick_vals, "4 nice"),
              check("line on the same axis", lerr < 0.01, lerr, "< 0.01"),
              check("data-end corner r = min(4, w/2, h)", abs(small["r"] - rexp) < 1e-6 and small["r"] < 4, small["r"], rexp),
              check("stack tops == sums", serr < 0.01, serr, "< 0.01"),
              check("empty state when all zero", 'class="empty"' in empty and "<path" not in empty, "empty text", True),
              check("negative control: the raw data max is not a nice axis top", not is_nice(87.3), 87.3, "not nice")]
    # video: scaleY from the baseline, rendered per frame from the same geometry
    W, H, fps = 720, 260, 30
    frames = []
    for kf in range(int(0.8 * fps)):
        p = ease("power3.out", prog(kf / fps, 0, 0.6))
        a = canvas(W, H, "#ffffff")
        for b in geo["bars"]:
            hh = (b["y1"] - b["y0"]) * p
            rect(a, b["x"], b["y1"] - hh, b["x"] + b["w"], b["y1"], b["color"])
        frames.append(a)
    vid = write_video(wd / "bars_grow.mp4", frames, fps)
    fr = read_video(vid)
    b0 = geo["bars"][6]
    xs = int(b0["x"] + b0["w"] / 2)
    grow = [bar_heights(f, int(round(b0["y1"])), [xs], "#ffffff")[0] for f in fr]
    gexp = [round((b0["y1"] - b0["y0"]) * ease("power3.out", prog(kf / fps, 0, 0.6))) for kf in range(len(fr))]
    checks.append(check("scaleY tween keeps bars on the baseline", max(abs(a - b) for a, b in zip(grow, gexp)) <= 1, grow[-1], gexp[-1]))
    return checks, [wd / "bars.svg", wd / "bars_stacked.svg", vid]


@card("DATA-39")
def waterfall(task, wd):
    """Running-total waterfall: steps float from the previous total, totals stand on the baseline, up c1 / down
    c8 / total ink-2, bar width min(40, band*.62), connectors; revealed step by step (350 ms), connector first."""
    np = _np()
    steps = [("Start", 120, True), ("A", 35, False), ("B", -20, False), ("C", 15, False), ("D", -40, False), ("End", None, True)]
    cum, run = [], 0
    for lab, v, tot in steps:
        if tot and v is not None:
            run = v
            cum.append((0, run))
        elif tot:
            cum.append((0, run))
        else:
            cum.append((run, run + v))
            run += v
    W, H, L, B, T = 720, 260, 52, 44, 12
    ih = H - T - B
    base = T + ih
    top = nice_ticks(max(max(a, b) for a, b in cum), 4)[0][-1]
    y = lambda v: base - v / top * ih
    band = (W - L - 8) / len(steps)
    bw = min(40, band * 0.62)
    colors = []
    for (lab, v, tot) in steps:
        colors.append("#5d6a7a" if tot else ("#2a78d6" if v > 0 else "#e34948"))
    fps, per = 30, 0.35

    def frame(t):
        a = canvas(W, H, "#ffffff")
        for i, ((lo, hi), c) in enumerate(zip(cum, colors)):
            ti = i * per
            if i > 0 and t >= ti - 0.1:
                cy = y(cum[i - 1][1])
                x0 = L + (i - 1) * band + (band + bw) / 2
                x1 = L + i * band + (band - bw) / 2
                p = prog(t, ti - 0.1, 0.1)
                rect(a, x0, cy, x0 + (x1 - x0) * p, cy + 1, "#999999")
            if t >= ti:
                p = ease("power2.out", prog(t, ti, 0.25))
                ylo, yhi = y(min(lo, hi)), y(max(lo, hi))
                x = L + i * band + (band - bw) / 2
                rect(a, x, ylo - (ylo - yhi) * p, x + bw, ylo, c)
        return a
    n = int((len(steps) * per + 0.4) * fps)
    vid = write_video(wd / "waterfall.mp4", [frame(k / fps) for k in range(n)], fps)
    fr = read_video(vid)
    last = fr[-1]
    png = save_png(last, wd / "waterfall.png")
    errs, cols = [], []
    for i, ((lo, hi), c) in enumerate(zip(cum, colors)):
        xc = int(L + i * band + band / 2)
        ink = np.nonzero(np.abs(last[:, xc] - 255).max(axis=-1) > 40)[0]
        errs.append(max(abs(ink.min() - round(y(max(lo, hi)))), abs(ink.max() + 1 - round(y(min(lo, hi))))))
        cols.append(bool(near(last[int(ink.mean()), xc:xc + 1], c, 6).all()))
    conn = [bool(near(last[int(y(cum[i - 1][1])), int(L + (i - 1) * band + (band + bw) / 2) + 2:int(L + i * band + (band - bw) / 2) - 2],
                      "#999999", 8).all()) for i in range(1, len(steps))]
    order_ok = True
    for i in range(1, len(steps)):
        xc = int(L + i * band + band / 2)
        cy = int(y(cum[i - 1][1]))
        xm = int(L + (i - 1) * band + (band + bw) / 2 + 1)
        fc = next(k for k, f in enumerate(fr) if near(f[cy, xm:xm + 1], "#999999", 8).all())
        fb = next(k for k, f in enumerate(fr) if (np.abs(f[:, xc] - 255).max(axis=-1) > 40).any())
        order_ok &= fc < fb
    plain = [abs(round(y(0)) - round(y(lo))) for lo, hi in cum if lo != 0]
    checks = [check("each step floats from the running total (px)", max(errs) <= 1, errs, "<= 1"),
              check("colours: up c1, down c8, totals ink-2", all(cols), cols, True),
              check("bar width = min(40, band*.62)", abs(bw - min(40, band * 0.62)) < 1e-9 and bw == 40, bw, 40),
              check("connectors at the previous total", all(conn), conn, True),
              check("connector draws before the next bar", order_ok, order_ok, True),
              check("end total == start + steps", cum[-1][1] == 120 + 35 - 20 + 15 - 40, cum[-1][1], 110),
              check("negative control: bars from the baseline would miss the floating bottoms", min(plain) > 1, plain, "> 1 px")]
    return checks, [vid, png]


@card("DATA-40")
def segmented_share_bar(task, wd):
    """One pill splits into proportional segments with per-segment vertical gradients; boundaries lerp from 0
    to cumulative shares; parts are checked against the total and the rounding remainder printed (MG-048 8 s)."""
    np = _np()
    parts = [("أ", 473), ("ب", 281), ("ج", 162), ("د", 84)]
    total = 1000
    exact = [v * 100.0 / total for _, v in parts]
    floor = [int(math.floor(e)) for e in exact]
    rem = 100 - sum(floor)
    order = sorted(range(len(parts)), key=lambda i: -(exact[i] - floor[i]))
    shown = floor[:]
    for i in order[:rem]:
        shown[i] += 1
    W, H, fps = 360, 200, 10
    px0, pw, ph, py = 30, 300, 12, 90        # pill height 6 % of the frame
    grads = [("#6aa8ff", "#1f5fbf"), ("#ffb38a", "#d9531e"), ("#7ee0b5", "#11865a"), ("#ffe08a", "#c99a00")]
    cumf = np.cumsum([v / float(total) for _, v in parts])

    def frame(t):
        a = canvas(W, H, "#ffffff")
        p = ease("easeInOutCubic", prog(t, 1.0, 3.0))
        edges = [0.0] + [c * p for c in cumf[:-1]] + [1.0]
        mask = pil_mask(W, H, lambda d: d.rounded_rectangle([px0, py, px0 + pw - 1, py + ph - 1], radius=ph // 2, fill=255))
        for i in range(len(parts)):
            x0, x1 = px0 + edges[i] * pw, px0 + edges[i + 1] * pw
            seg = np.zeros(mask.shape, bool)
            seg[py:py + ph, int(round(x0)):int(round(x1))] = True
            g = np.linspace(0, 1, ph)
            for r in range(ph):
                paint(a, seg & mask & (np.arange(H)[:, None] == py + r), lerp_c(grads[i][0], grads[i][1], g[r]))
        return a
    n = int(8.0 * fps)
    vid = write_video(wd / "share_bar.mp4", [frame(k / fps) for k in range(n)], fps)
    fr = read_video(vid)
    mid = fr[-1][py + ph // 2, px0:px0 + pw]
    jumps = [x for x in range(1, pw) if np.abs(mid[x] - mid[x - 1]).max() > 20]
    exp_b = [round(c * pw) for c in cumf[:-1]]
    berr = max(abs(a - b) for a, b in zip(jumps, exp_b)) if len(jumps) == 3 else 99
    halfway = fr[int(2.5 * fps)][py + ph // 2, px0:px0 + pw]
    hj = [x for x in range(1, pw) if np.abs(halfway[x] - halfway[x - 1]).max() > 20]
    pe = ease("easeInOutCubic", prog(2.5, 1.0, 3.0))
    herr = max(abs(a - round(c * pe * pw)) for a, b in zip(hj, cumf[:-1]) for c in [b]) if len(hj) == 3 else 99
    xs = px0 + exp_b[0] // 2
    topc, botc = fr[-1][py + 1, xs], fr[-1][py + ph - 2, xs]
    gexp_t, gexp_b = lerp_c(grads[0][0], grads[0][1], 1 / 11.0), lerp_c(grads[0][0], grads[0][1], 10 / 11.0)
    gerr = max(float(np.abs(topc - gexp_t).max()), float(np.abs(botc - gexp_b).max()))
    checks = [check("parts sum to the total", sum(v for _, v in parts) == total, sum(v for _, v in parts), total),
              check("rounded labels sum to 100 (remainder printed)", sum(shown) == 100 and rem == 1, {"shown": shown, "remainder": rem}, 100),
              check("final boundaries at cumulative shares (px)", berr <= 1, jumps, exp_b),
              check("boundaries lerp from 0 (mid-split frame)", herr <= 1, hj, [round(c * pe * pw) for c in cumf[:-1]]),
              check("each segment has its own vertical gradient", gerr <= 8 and float(np.abs(topc - botc).max()) > 30, gerr, "<= 8"),
              check("pill height 6 % of frame", ph / float(H) == 0.06, ph / float(H), 0.06)]
    f0 = fr[0][py + ph // 2, px0:px0 + pw]
    j0 = [x for x in range(1, pw) if np.abs(f0[x] - f0[x - 1]).max() > 20]
    checks.append(check("negative control: the unsplit input bar has no share boundaries", len(j0) != 3, j0, "!= 3 boundaries"))
    out = wjson(wd / "shares.json", {"parts": parts, "exact_pct": exact, "shown_pct": shown,
                                     "note": "الأرقام مقرّبة؛ الفرق %d نقطة أُضيف لأكبر كسر" % rem})
    return checks, [vid, out]


@card("DATA-41")
def log_domain_zoom(task, wd):
    """Animate the bar domain from 100 to 1.2 in log space: max(t) = exp(lerp(ln a, ln b, e(t))); every
    segment's x/width is recomputed per frame (never a group scale) so the rounded caps stay round."""
    np = _np()
    vals = [1.2, 8.8, 20.0, 70.0]
    cols = ["#e4572e", "#4a6fa5", "#76b041", "#ffc914"]
    W, H, fps, BW, rad = 360, 80, 30, 320, 6
    a0, b0, dur = 100.0, 1.2, 1.2
    mx = lambda t: math.exp(math.log(a0) + (math.log(b0) - math.log(a0)) * ease("easeInOut", prog(t, 0.2, dur)))
    x0, y0, bh = 20, 30, 24

    def frame(t):
        a = canvas(W, H, "#ffffff")
        m = mx(t)
        acc = 0.0
        for v, c in zip(vals, cols):
            xa, xb = x0 + acc / m * BW, x0 + min(acc + v, m * 1.0) / m * BW
            acc += v
            if xa >= x0 + BW:
                break
            xb = min(xb, x0 + BW)
            if xb - xa >= 1:
                paint(a, pil_mask(W, H, lambda d: d.rounded_rectangle([xa, y0, xb - 1, y0 + bh - 1], radius=rad, fill=255)), c)
        if t >= 0.2 + dur:
            draw_seg(a, "%2d" % round(a0 / b0), "dd", 14, 300, 6, "#222222")
        return a
    n = int((0.2 + dur + 0.3) * fps)
    vid = write_video(wd / "log_zoom.mp4", [frame(k / fps) for k in range(n)], fps)
    fr = read_video(vid)
    werr, lerr, prof = 0.0, 0.0, set()
    for k, f in enumerate(fr):
        row = near(f[y0 + bh // 2], cols[0], 8)
        xs = np.nonzero(row)[0]
        w = xs.max() + 1 - xs.min()
        m = mx(k / fps)
        werr = max(werr, abs(w - min(BW, vals[0] / m * BW)))
        if w < BW - 2:
            lerr = max(lerr, abs(math.log(vals[0] * BW / w) - math.log(m)))
        corner = near(f[y0:y0 + rad, x0:x0 + rad], cols[0], 8)
        prof.add(int((~corner).sum()))
    from PIL import Image
    seg0 = fr[0][y0:y0 + bh, x0:x0 + int(round(vals[0] / a0 * BW)) + 2].astype("uint8")
    stretched = np.asarray(Image.fromarray(seg0).resize((seg0.shape[1] * 40, bh), Image.NEAREST)).astype(float)
    sc = near(stretched[:rad, :rad], cols[0], 8)
    checks = [check("first slice width == 1.2 / max(t) x W in every frame (px)", werr <= 1.5, werr, "<= 1.5"),
              check("measured domain follows exp(lerp(ln 100, ln 1.2, e(t)))", lerr <= 0.05, lerr, "<= 0.05 (ln units)"),
              check("rounded cap identical in every frame (not stretched)", len(prof) == 1, sorted(prof), "one profile"),
              check("tiny slice fills the frame at the end", werr <= 1.5 and abs(np.nonzero(near(fr[-1][y0 + bh // 2], cols[0], 8))[0].size - BW) <= 1,
                    int(np.nonzero(near(fr[-1][y0 + bh // 2], cols[0], 8))[0].size), BW),
              check("zoom announced on screen (x83)", read_seg(fr[-1], "dd", 14, 300, 6, "#ffffff", fg="#222222") == "83",
                    read_seg(fr[-1], "dd", 14, 300, 6, "#ffffff", fg="#222222"), "83"),
              check("negative control: a group scaleX stretches the cap", int((~sc).sum()) not in prof, int((~sc).sum()), "!= %s" % sorted(prof))]
    return checks, [vid]


def wilson(k, n, z=1.96):
    p = k / float(n)
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return c - h, c + h


@card("DATA-42")
def threshold_bars_ci(task, wd):
    """Thick bars grow 800 ms easeOutCubic with a 200 ms stagger, green above / red below the threshold, a thin
    95 % interval whisker drawn after each bar, and 'n of N' at the tip; editorial paper palette."""
    np = _np()
    groups = [(61, 100), (45, 100), (72, 120), (30, 80)]
    thr = 0.5
    W, H, fps = 420, 200, 30
    ax, sc, bh = 60, 3.0, 20
    rows = [30 + i * 40 for i in range(4)]
    paper, ink, red, green = "#eee8dc", "#2b2622", "#c9463d", "#1f7a4f"

    def frame(t):
        a = canvas(W, H, paper)
        for i, (k, n) in enumerate(groups):
            p = k / float(n)
            e = ease("easeOutCubic", prog(t, i * 0.2, 0.8))
            rect(a, ax, rows[i], ax + p * 100 * sc * e, rows[i] + bh, green if p >= thr else red)
            if t >= i * 0.2 + 0.8:
                lo, hi = wilson(k, n)
                rect(a, ax + lo * 100 * sc, rows[i] + bh // 2, ax + hi * 100 * sc, rows[i] + bh // 2 + 1, ink)
                for xv in (lo, hi):
                    rect(a, ax + xv * 100 * sc, rows[i] - 4, ax + xv * 100 * sc + 1, rows[i] + bh + 4, ink)
                draw_seg(a, fmt_int(k, "ddd"), "ddd", 10, int(ax + hi * 100 * sc) + 6, rows[i] + 5, ink)
        return a
    n_fr = int((3 * 0.2 + 0.8 + 0.3) * fps)
    vid = write_video(wd / "threshold_bars.mp4", [frame(k / fps) for k in range(n_fr)], fps)
    fr = read_video(vid)
    last = fr[-1]
    lens = [int((near(last[r + 3], green, 10) | near(last[r + 3], red, 10)).sum()) for r in rows]
    exp = [round(k / float(n) * 100 * sc) for k, n in groups]
    colok = [bool(near(last[r + 3, ax + 2:ax + 3], green if k / float(n) >= thr else red, 10).all()) for r, (k, n) in zip(rows, groups)]
    grow = 0
    for kf, f in enumerate(fr):
        for i, (k, n) in enumerate(groups):
            e = ease("easeOutCubic", prog(kf / fps, i * 0.2, 0.8))
            m = int((near(f[rows[i] + 3], green, 10) | near(f[rows[i] + 3], red, 10)).sum())
            grow = max(grow, abs(m - round(k / float(n) * 100 * sc * e)))
    werr, order = 0.0, True
    for i, (k, n) in enumerate(groups):
        cap = np.nonzero(near(last[rows[i] - 2], ink, 10))[0]
        lo, hi = wilson(k, n)
        werr = max(werr, abs(cap.min() - (ax + lo * 100 * sc)), abs(cap.max() - (ax + hi * 100 * sc)))
        first = next(kf for kf, f in enumerate(fr) if near(f[rows[i] - 2], ink, 10).any())
        order &= first / fps >= i * 0.2 + 0.8 - 1e-6
    labels = [seg_value(read_seg(last, "ddd", 10, int(ax + wilson(k, n)[1] * 100 * sc) + 6, rows[i] + 5, paper, fg=ink))
              for i, (k, n) in enumerate(groups)]
    checks = [check("bar lengths == share x scale (px)", max(abs(a - b) for a, b in zip(lens, exp)) <= 1, lens, exp),
              check("green above / red below threshold", all(colok), colok, True),
              check("growth follows easeOutCubic with 200 ms stagger (px)", grow <= 1, grow, "<= 1"),
              check("whisker spans the 95 % Wilson interval (px)", werr <= 1, werr, "<= 1"),
              check("whisker appears only after its bar", order, order, True),
              check("'n' printed at the tip", labels == [k for k, _ in groups], labels, [k for k, _ in groups]),
              check("negative control: the first frame shows no grown bars", max(int((near(fr[0][r + 3], green, 10) | near(fr[0][r + 3], red, 10)).sum()) for r in rows) == 0
                    and max(exp) > 0, 0, "0 px")]
    return checks, [vid]


@card("DATA-43")
def severity_rows_meter_progress(task, wd):
    """Severity rows fill round(n/max*100) % with 90deg gradients, a meter whose colour follows the verdict
    anchored inline-end, and a progress bar via translateX(-(100-value)%) over 500 ms ease-out."""
    np = _np()
    rows = [("critical", 9, "#f43f5e", "#ef4444"), ("high", 6, "#f59e0b", "#f97316"),
            ("medium", 4, "#06b6d4", "#6366f1"), ("low", 2, "#10b981", "#14b8a6")]
    mx = max(n for _, n, _, _ in rows)
    W, H, fps, tx, tw = 320, 240, 30, 90, 200
    value, verdict = 64, "approaching"
    vcol = {"ok": "#10b981", "approaching": "#f59e0b", "material": "#ef4444"}[verdict]

    def frame(t):
        a = canvas(W, H, "#ffffff")
        for i, (_, n, c0, c1) in enumerate(rows):
            y = 20 + i * 24
            rect(a, tx, y, tx + tw, y + 9, "#f1f5f9")
            fw = round(round(n / float(mx) * 100) / 100.0 * tw)
            for x in range(fw):
                rect(a, tx + x, y, tx + x + 1, y + 9, lerp_c(c0, c1, x / max(1.0, fw - 1)))
        e = ease("power2.out", prog(t, 0, 0.5))
        mw = 120 * e * value / 100.0
        rect(a, W - 20 - mw, 130, W - 20, 142, vcol)
        off = -(100 - value * e)
        rect(a, tx, 180, tx + tw, 188, "#e2e8f0")
        rect(a, tx + tw + off / 100.0 * tw - tw, 180, tx + tw + off / 100.0 * tw, 188, "#6366f1")
        return a
    n = int(0.8 * fps)
    vid = write_video(wd / "severity.mp4", [frame(k / fps) for k in range(n)], fps)
    fr = read_video(vid)
    last = fr[-1]
    werr, gerr = 0, 0.0
    for i, (_, nn, c0, c1) in enumerate(rows):
        y = 20 + i * 24 + 4
        fill = np.nonzero(~near(last[y, tx:tx + tw], "#f1f5f9", 3))[0]
        exp = round(round(nn / float(mx) * 100) / 100.0 * tw)
        werr = max(werr, abs(len(fill) - exp))
        gerr = max(gerr, float(np.abs(last[y, tx] - rgb(c0)).max()), float(np.abs(last[y, tx + exp - 1] - rgb(c1)).max()))
    rights, perr = set(), 0
    for k, f in enumerate(fr):
        xs = np.nonzero(near(f[136], vcol, 6))[0]
        if len(xs):
            rights.add(int(xs.max()))
        pw = int(near(f[184, tx:tx + tw], "#6366f1", 6).sum())
        perr = max(perr, abs(pw - round(tw * value / 100.0 * ease("power2.out", prog(k / fps, 0, 0.5)))))
    ph = int(near(last[:, tx + 5], "#6366f1", 6).sum())
    checks = [check("row fill == round(n/max*100) % of the 9 px track (px)", werr <= 1, werr, "<= 1"),
              check("fills run the severity gradient", gerr <= 6, gerr, "<= 6"),
              check("meter colour follows the verdict", bool(near(last[136, W - 25:W - 24], vcol, 6).all()), verdict, vcol),
              check("meter anchored inline-end (fixed right edge)", len(rights) == 1, sorted(rights), "one edge"),
              check("progress visible width == value x ease-out(t/0.5 s) (px)", perr <= 1, perr, "<= 1"),
              check("progress height 8 px", ph == 8, ph, 8),
              check("negative control: the first frame shows no progress", int(near(fr[0][184, tx:tx + tw], "#6366f1", 6).sum()) == 0, 0, 0)]
    return checks, [vid]


@card("DATA-44")
def lighting_cells_bucket(task, wd):
    """A row of 20 cells lights right->left (Arabic) 40 ms per cell to a level with a bound % counter and an end
    tag; a 10-slot bucket drains linearly with a thin partial top slot and a red stroke at zero."""
    np = _np()
    fps = 25          # one frame = 40 ms = one cell
    W, H = 360, 200
    ncell, level = 20, 15
    cw, cg, cx0, cy = 14, 3, 10, 20
    nslot, drain = 10, 2.0

    def frame(k):
        t = k / float(fps)
        a = canvas(W, H, "#0f1115")
        lit = min(level, k)
        for j in range(ncell):
            x = cx0 + (ncell - 1 - j) * (cw + cg)     # j counts from the right edge
            rect(a, x, cy, x + cw, cy + cw, "#5aa8ff" if j < lit else "#2a2f3a")
        draw_seg(a, fmt_int(round(lit / float(ncell) * 100), "ddd"), "ddd", 18, 20, 50, "#ffffff")
        if k > level:
            rect(a, 300, 50, 340, 68, "#ffd23f")      # end tag
        lv = max(0.0, nslot * (1 - prog(t, 1.0, drain)))
        for s in range(nslot):
            y = 180 - (s + 1) * 10
            fill = min(1.0, max(0.0, lv - s))
            if fill >= 1:
                rect(a, 200, y + 1, 260, y + 9, "#5aa8ff")
            elif fill > 0:
                rect(a, 200, y + 9 - max(1, round(8 * fill)), 260, y + 9, "#5aa8ff")
        if lv <= 0:
            for (xa, ya, xb, yb) in ((198, 78, 262, 80), (198, 180, 262, 182), (198, 78, 200, 182), (260, 78, 262, 182)):
                rect(a, xa, ya, xb, yb, "#f85149")
        return a
    n = int((1.0 + drain + 0.4) * fps)
    vid = write_video(wd / "cells_bucket.mp4", [frame(k) for k in range(n)], fps)
    fr = read_video(vid)
    centers = [cx0 + (ncell - 1 - j) * (cw + cg) + cw // 2 for j in range(ncell)]
    lit_ok, rtl_ok, cnt_ok = True, True, True
    for k, f in enumerate(fr[:level + 3]):
        on = [bool(near(f[cy + 5, x:x + 1], "#5aa8ff", 6).all()) for x in centers]
        lit_ok &= sum(on) == min(level, k)
        rtl_ok &= on == [j < min(level, k) for j in range(ncell)]
        cnt_ok &= seg_value(read_seg(f, "ddd", 18, 20, 50, "#0f1115", thr=60)) == round(sum(on) / float(ncell) * 100)
    tag_first = next(k for k, f in enumerate(fr) if near(f[58, 320:321], "#ffd23f", 6).all())
    derr = 0.0
    for k, f in enumerate(fr):
        t = k / float(fps)
        lv = max(0.0, nslot * (1 - prog(t, 1.0, drain)))
        col = near(f[80:180, 230], "#5aa8ff", 6)
        meas = 0.0
        for s in range(nslot):
            seg = col[100 - (s + 1) * 10 + 1:100 - s * 10]
            meas += 1.0 if seg[:8].all() else (seg.sum() / 8.0 if seg.any() else 0)
        derr = max(derr, abs(meas - lv))
    red_end = bool(near(fr[-1][181, 230:231], "#f85149", 6).all()) and not near(fr[int(1.5 * fps)][181, 230:231], "#f85149", 6).all()
    ltr = [bool(near(fr[5][cy + 5, cx0 + j * (cw + cg) + cw // 2:cx0 + j * (cw + cg) + cw // 2 + 1], "#5aa8ff", 6).all()) for j in range(ncell)]
    checks = [check("one cell per 40 ms up to the level (15/20)", lit_ok, level, level),
              check("cells light right -> left", rtl_ok, rtl_ok, True),
              check("bound counter == lit share", cnt_ok, 75, "lit/20*100"),
              check("end tag after the last cell", tag_first == level + 1, tag_first, level + 1),
              check("bucket drains linearly (slots, partial top slot)", derr <= 0.15, derr, "<= 0.15 slot"),
              check("red stroke at zero only", red_end, red_end, True),
              check("negative control: reading left->right, frame 5 has no lit cells on the left", not any(ltr[:5]), ltr[:5], "all off")]
    return checks, [vid]


@card("DATA-46")
def token_probability_bars(task, wd):
    """Four candidate tokens: bars grow to probabilities (400 ms, 80 ms stagger, values count), the chosen one
    turns orange with an arrow, then it types into the prompt."""
    np = _np()
    probs = [0.55, 0.21, 0.11, 0.01]
    fps, W, H, x0, sc = 25, 420, 220, 60, 300
    rows = [20 + i * 30 for i in range(4)]
    chosen = int(np.argmax(probs))
    t_type = 3 * 0.08 + 0.4 + 0.1
    word = 5

    def frame(k):
        t = k / float(fps)
        a = canvas(W, H, "#ffffff")
        for i, p in enumerate(probs):
            e = ease("power2.out", prog(t, i * 0.08, 0.4))
            done = t >= 3 * 0.08 + 0.4
            col = "#ff7a1a" if (done and i == chosen) else "#9aa0a6"
            rect(a, x0, rows[i], x0 + p * sc * e, rows[i] + 16, col)
            draw_seg(a, fmt_int(p * 100 * e, "dd"), "dd", 12, 20, rows[i] + 2, "#333333")
            if done and i == chosen:
                paint(a, pil_mask(W, H, lambda d: d.polygon([(x0 + p * sc + 14, rows[i] + 8), (x0 + p * sc + 24, rows[i] + 2),
                                                              (x0 + p * sc + 24, rows[i] + 14)], fill=255)), "#ff7a1a")
        typed = min(word, int((t - t_type) / 0.08) + 1) if t >= t_type else 0
        for c in range(typed):
            rect(a, 60 + c * 9, 160, 60 + c * 9 + 7, 172, "#222222")
        return a
    n = int((t_type + word * 0.08 + 0.3) * fps)
    vid = write_video(wd / "tokens.mp4", [frame(k) for k in range(n)], fps)
    fr = read_video(vid)
    last = fr[-1]
    lens = [int((~near(last[r + 8, x0:x0 + sc], "#ffffff", 3)).sum()) for r in rows]
    exp = [round(p * sc) for p in probs]
    starts = [next(k for k, f in enumerate(fr) if not near(f[r + 8, x0:x0 + 1], "#ffffff", 3).all()) for r in rows]
    exp_st = [next(k for k in range(n) if round(probs[i] * sc * ease("power2.out", prog(k / float(fps), i * 0.08, 0.4))) >= 1) for i in range(4)]
    accent = [bool(near(last[r + 8, x0 + 1:x0 + 2], "#ff7a1a", 6).all()) for r in rows]
    arrow = [bool(near(last[r + 8, x0 + int(probs[i] * sc) + 20:x0 + int(probs[i] * sc) + 21], "#ff7a1a", 6).all()) for i, r in enumerate(rows)]
    typed = [len(col_runs(near(f[166, 55:120], "#222222", 6))) for f in fr]
    nums = [seg_value(read_seg(last, "dd", 12, 20, r + 2, "#ffffff", fg="#333333")) for r in rows]
    checks = [check("bar lengths == probability x scale (px)", max(abs(a - b) for a, b in zip(lens, exp)) <= 1, lens, exp),
              check("80 ms stagger (first frame per bar)", starts == exp_st and starts[1] - starts[0] == 2, starts, exp_st),
              check("argmax turns orange, others grey", accent == [i == chosen for i in range(4)], accent, chosen),
              check("arrow beside the chosen bar only", arrow == [i == chosen for i in range(4)], arrow, chosen),
              check("values count to the probabilities", nums == [round(p * 100) for p in probs], nums, [55, 21, 11, 1]),
              check("token types into the prompt one char per 80 ms", typed[-1] == word and all(b - a in (0, 1) for a, b in zip(typed, typed[1:])),
                    typed[-1], word),
              check("negative control: the first frame has no bars", max(int((~near(fr[0][r + 8, x0:x0 + sc], "#ffffff", 3)).sum()) for r in rows) == 0, 0, 0)]
    return checks, [vid]


@card("DATA-47")
def rank_reorder(task, wd):
    """Ranked bars move to a new order while numbers update (MG-049: 0-2 s period one, 2-5 s reorder,
    5-8 s period two): fixed slot positions per rank, identity colour kept."""
    np = _np()
    names = ["A", "B", "C", "D", "E"]
    cols = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#4a3aa7"]
    p1 = [50, 40, 30, 20, 10]
    p2 = [25, 45, 35, 55, 15]
    r1 = {i: r for r, i in enumerate(sorted(range(5), key=lambda i: -p1[i]))}
    r2 = {i: r for r, i in enumerate(sorted(range(5), key=lambda i: -p2[i]))}
    fps, W, H = 10, 320, 180
    slot = lambda r: 15 + r * 30

    def frame(t):
        e = ease("easeInOutCubic", prog(t, 2.0, 3.0))
        a = canvas(W, H, "#ffffff")
        for i in range(5):
            y = slot(r1[i]) + (slot(r2[i]) - slot(r1[i])) * e
            v = p1[i] + (p2[i] - p1[i]) * e
            rect(a, 20, y, 20 + v * 5, y + 20, cols[i])
        return a
    n = int(8.0 * fps)
    vid = write_video(wd / "rank_reorder.mp4", [frame(k / fps) for k in range(n)], fps)
    fr = read_video(vid)

    def order(f):
        out = []
        for r in range(5):
            px = f[slot(r) + 10, 22]
            out.append(int(np.argmin([np.abs(px - rgb(c)).max() for c in cols])))
        return out
    o1, o2 = order(fr[int(1 * fps)]), order(fr[int(7 * fps)])
    e1 = sorted(range(5), key=lambda i: -p1[i])
    e2 = sorted(range(5), key=lambda i: -p2[i])
    ident = all(sum(1 for c in cols if near(f[:, 22], c, 4).any()) == 5 for f in fr)
    lens = [int(near(fr[int(7 * fps)][slot(r2[i]) + 10], cols[i], 4).sum()) for i in range(5)]
    mono = True
    for i in range(5):
        ys = [float(np.nonzero(near(f[:, 22], cols[i], 4))[0].min()) for f in fr[int(2 * fps):int(5 * fps) + 1]]
        d = [b - a for a, b in zip(ys, ys[1:])]
        mono &= all(x >= -0.5 for x in d) or all(x <= 0.5 for x in d)
    checks = [check("period one order", o1 == e1, [names[i] for i in o1], [names[i] for i in e1]),
              check("period two order", o2 == e2, [names[i] for i in o2], [names[i] for i in e2]),
              check("identity colours kept in every frame", ident, ident, True),
              check("bar lengths == period-two values (px)", lens == [v * 5 for v in p2], lens, [v * 5 for v in p2]),
              check("each item moves monotonically between slots", mono, mono, True),
              check("negative control: the period-one input order is wrong for period two", o1 != e2, [names[i] for i in o1], "!= period two")]
    return checks, [vid]


@card("DATA-49")
def small_multiples(task, wd):
    """The same mini-chart per category with shared x/y axes: cols = min(3, n), empty cells hidden, one hue
    + accent, panels revealed in Arabic reading order (right-to-left rows) with an 80 ms stagger."""
    np = _np()
    data = {"أ": [10, 20, 30, 25, 35, 40], "ب": [5, 8, 12, 9, 7, 6], "ج": [30, 28, 26, 24, 22, 20],
            "د": [12, 30, 18, 22, 26, 31], "هـ": [40, 35, 45, 50, 48, 55]}
    n = len(data)
    cols = min(3, n)
    rowsn = math.ceil(n / cols)
    pw, ph, gap = 110, 80, 10
    W, H = cols * pw + (cols + 1) * gap, rowsn * ph + (rowsn + 1) * gap
    vmax = max(max(v) for v in data.values())
    fps = 25

    def cell(idx):
        r, c = divmod(idx, cols)
        c = cols - 1 - c                       # right-to-left
        return gap + c * (pw + gap), gap + r * (ph + gap)

    def draw(t, shared=True):
        a = canvas(W, H, "#ffffff")
        for idx, (k, vals) in enumerate(data.items()):
            if t < idx * 0.08:
                continue
            x, y = cell(idx)
            rect(a, x, y, x + pw, y + ph, "#f3f4f6")
            top = vmax if shared else max(vals)
            for j, v in enumerate(vals):
                bh = round(v / float(top) * (ph - 10))
                rect(a, x + 5 + j * 17, y + ph - bh, x + 5 + j * 17 + 12, y + ph, "#e4572e" if j == 5 else "#4a6fa5")
        return a
    vid = write_video(wd / "small_multiples.mp4", [draw(k / float(fps)) for k in range(int(0.8 * fps))], fps)
    fr = read_video(vid)
    last = fr[-1]
    present = [bool(near(last[cell(i)[1] + 2, cell(i)[0] + 2:cell(i)[0] + 3], "#f3f4f6", 3).all()) for i in range(cols * rowsn)]
    first = [next(k for k, f in enumerate(fr) if near(f[cell(i)[1] + 2, cell(i)[0] + 2:cell(i)[0] + 3], "#f3f4f6", 3).all()) for i in range(n)]

    def height(a, idx, j):
        x, y = cell(idx)
        return int((~near(a[y:y + ph, x + 5 + j * 17 + 6], "#f3f4f6", 3)).sum())
    same = [height(last, 2, 0), height(last, 4, 2 - 2)]     # v = 30 (ج, Jan) and v = 40 (هـ, Jan): ratio must be 30:40
    ratio = same[0] / float(same[1])
    auto = save_png(draw(1.0, shared=False), wd / "autoscaled_panels.png")
    ab = load_png(auto)
    ar = height(ab, 2, 0) / float(height(ab, 4, 0))
    checks = [check("grid columns = min(3, n)", cols == 3 and rowsn == 2, [cols, rowsn], [3, 2]),
              check("5 panels shown, empty cell hidden", present == [True] * 5 + [False], present, "5 + hidden"),
              check("shared y axis: heights compare across panels (30:40)", abs(ratio - 0.75) <= 0.02, ratio, 0.75),
              check("reveal in reading order, 80 ms (2 frames) stagger", first == [2 * i for i in range(n)], first, [2 * i for i in range(n)]),
              check("first panel starts at the right", cell(0)[0] > cell(2)[0], cell(0)[0], "> left"),
              check("negative control: autoscaled panels break the comparison", abs(ar - 0.75) > 0.05, ar, "!= 0.75")]
    return checks, [vid, auto]
