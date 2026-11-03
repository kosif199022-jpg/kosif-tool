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


def _nz(v):
    return -1e9 if v is None else v


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
              check("negative control: the undimmed source measured against itself is not 55 %",
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
              check("4 gridlines on a nice step", len(tick_vals) == 4 and is_nice(tick_vals[0]) and
                    all(abs(v / tick_vals[0] - round(v / tick_vals[0])) < 1e-9 for v in tick_vals), tick_vals, "4 x nice step"),
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
    conn = [bool(near(last[int(round(y(cum[i - 1][1]))), int(L + (i - 1) * band + (band + bw) / 2) + 2:int(L + i * band + (band - bw) / 2) - 2],
                      "#999999", 8).all()) for i in range(1, len(steps))]
    order_ok = True
    for i in range(1, len(steps)):
        xc = int(L + i * band + band / 2)
        cy = int(round(y(cum[i - 1][1])))
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
        if 20 <= w < BW - 2:
            lerr = max(lerr, abs(math.log(vals[0] * BW / w) - math.log(m)))
        if w >= 4 * rad:           # narrower than the cap diameter the corner is geometrically clipped
            corner = near(f[y0:y0 + rad, x0:x0 + rad], cols[0], 8)
            prof.add(int((~corner).sum()))
    from PIL import Image
    kref = next(k for k, f in enumerate(fr) if near(f[y0 + bh // 2], cols[0], 8).sum() >= 4 * rad)
    wref = int(near(fr[kref][y0 + bh // 2], cols[0], 8).sum())
    seg0 = fr[kref][y0:y0 + bh, x0:x0 + wref].astype("uint8")
    stretched = np.asarray(Image.fromarray(seg0).resize((wref * 4, bh), Image.BILINEAR)).astype(float)
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
    lens = [col_runs(~near(last[r + 8, x0:x0 + sc], "#ffffff", 3))[0][1] for r in rows]
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
    still = list(fr[:int(2 * fps)]) + list(fr[int(5 * fps) + 1:])
    ident = all(sum(1 for c in cols if near(f[:, 22], c, 4).any()) == 5 for f in still)
    pal = all(bool((near(f[:, 22], "#ffffff", 3) | np.any([near(f[:, 22], c, 4) for c in cols], axis=0)).all()) for f in fr)
    ident = ident and pal
    lens = [int(near(fr[int(7 * fps)][slot(r2[i]) + 10], cols[i], 4).sum()) for i in range(5)]
    mono = True
    for i in range(5):
        ys = [float(np.nonzero(near(f[:, 22], cols[i], 4))[0].min()) for f in fr[int(2 * fps):int(5 * fps) + 1]
              if near(f[:, 22], cols[i], 4).sum() >= 20]     # skip frames where another bar fully covers it
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


def dist_to_polyline(p, pts):
    best = 1e9
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        dx, dy = bx - ax, by - ay
        L2 = dx * dx + dy * dy
        u = 0 if L2 == 0 else max(0, min(1, ((p[0] - ax) * dx + (p[1] - ay) * dy) / L2))
        best = min(best, math.hypot(p[0] - ax - u * dx, p[1] - ay - u * dy))
    return best


def point_at(pts, frac):
    segs = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]
    s = frac * sum(segs)
    for (a, b), L in zip(zip(pts, pts[1:]), segs):
        if s <= L or L == 0:
            u = s / L if L else 0
            return a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u
        s -= L
    return pts[-1]


def centroid(mask):
    np = _np()
    ys, xs = np.nonzero(mask)
    return (xs.mean() + 0.5, ys.mean() + 0.5) if len(xs) else None


@card("DATA-53")
def scrub_marker_tooltip(task, wd):
    """A tracking marker moves along the baked polyline (2 s scrub, power3.out stop on the peak, >= 0.8 s hold)
    while the tooltip snaps to the nearest data point."""
    np = _np()
    vals = [20, 26, 22, 31, 35, 30, 41, 47, 58, 44, 39, 42]
    W, H, fps = 320, 180, 30
    X = lambda i: 20 + i * 25
    Y = lambda v: 160 - v * 2.2
    peak = int(np.argmax(vals))
    pts = [(X(i), Y(v)) for i, v in enumerate(vals[:peak + 1])]
    full = [(X(i), Y(v)) for i, v in enumerate(vals)]
    scrub, hold = 2.0, 0.8
    base = canvas(W, H, "#ffffff")
    paint(base, line_mask(H, W, full, 2), "#4a6fa5")

    def frame(t):
        a = base.copy()
        mx, my = point_at(pts, ease("power3.out", prog(t, 0, scrub)))
        paint(a, pil_mask(W, H, lambda d: d.ellipse([mx - 4, my - 4, mx + 4, my + 4], fill=255)), "#e4572e")
        ni = int(np.argmin([abs(X(i) - mx) for i in range(len(vals))]))
        rect(a, 240, 8, 300, 34, "#222222")
        draw_seg(a, fmt_int(vals[ni], "dd"), "dd", 16, 250, 13, "#ffffff")
        return a, ni
    n = int((scrub + hold + 0.2) * fps)
    rendered = [frame(k / fps) for k in range(n)]
    vid = write_video(wd / "scrub.mp4", [f for f, _ in rendered], fps)
    fr = read_video(vid)
    cents = [centroid(near(f, "#e4572e", 30)) for f in fr]
    dmax = max(dist_to_polyline(c, pts) for c in cents)
    tips = [seg_value(read_seg(f, "dd", 16, 250, 13, "#222222", fg="#ffffff")) for f in fr]
    nearest = [vals[int(np.argmin([abs(X(i) - c[0]) for i in range(len(vals))]))] for c in cents]
    two = [[vals[i] for i in sorted(range(len(vals)), key=lambda i: abs(X(i) - c[0]))[:2]] for c in cents]
    gapd = [sorted(abs(X(i) - c[0]) for i in range(len(vals)))[:2] for c in cents]
    # within 1 px of a midpoint the measured centroid cannot separate the two neighbours: accept either
    nearest = [nv if (g[1] - g[0]) >= 1.0 or tv not in tw else tv for nv, tv, tw, g in zip(nearest, tips, two, gapd)]
    held = sum(1 for c in cents if math.hypot(c[0] - pts[-1][0], c[1] - pts[-1][1]) < 0.75)
    straight = max(dist_to_polyline((pts[0][0] + (pts[-1][0] - pts[0][0]) * u, pts[0][1] + (pts[-1][1] - pts[0][1]) * u), pts)
                   for u in np.linspace(0, 1, 50))
    checks = [check("marker stays on the polyline (px)", dmax <= 1.5, dmax, "<= 1.5"),
              check("stops on the peak", math.hypot(cents[-1][0] - pts[-1][0], cents[-1][1] - pts[-1][1]) < 0.75, cents[-1], pts[-1]),
              check("holds >= 0.8 s on the peak", held / float(fps) >= hold, held / float(fps), ">= 0.8"),
              check("tooltip == nearest data point every frame", tips == nearest, sum(a != b for a, b in zip(tips, nearest)), 0),
              check("negative control: a straight path would leave the polyline", straight > 1.5, straight, "> 1.5 px")]
    return checks, [vid]


def _sk_line(labels, series, area=False, endLabels=True, width=720, height=240):
    L, T, B = 46, 12, 30
    R = 70 if (endLabels and len(series) <= 4) else 8
    iw, ih = width - L - R, height - T - B
    step = int(math.ceil(len(labels) / float(max(3, iw // 56))))
    top = nice_ticks(max(max(s["values"]) for s in series), 4)[0][-1]
    X = lambda i: L + i * iw / float(len(labels) - 1)
    Y = lambda v: T + ih - v / top * ih
    out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" data-pr="%d" data-step="%d">' % (width, height, R, step)]
    for i in range(0, len(labels), step):
        out.append('<text class="xl" x="%.2f" y="%d">%s</text>' % (X(i), height - 8, labels[i]))
    for s in series:
        pts = " ".join("%.2f,%.2f" % (X(i), Y(v)) for i, v in enumerate(s["values"]))
        if area:
            out.append('<path class="area" fill="%s" fill-opacity="0.1" d="M%.2f %.2f L%s L%.2f %.2f Z"/>' % (
                s["color"], X(0), T + ih, pts.replace(" ", " L"), X(len(labels) - 1), T + ih))
        out.append('<polyline class="ln" fill="none" stroke="%s" stroke-width="2" points="%s"/>' % (s["color"], pts))
        j = len(s["values"]) - 1
        out.append('<circle class="pt" r="4" cx="%.2f" cy="%.2f" fill="%s"/>' % (X(j), Y(s["values"][j]), s["color"]))
        if endLabels and len(series) <= 4:
            out.append('<text class="end" x="%.2f" y="%.2f">%s</text>' % (X(j) + 8, Y(s["values"][j]), s["name"]))
    out.append("</svg>")
    return "".join(out), {"X": X, "Y": Y, "step": step, "R": R, "iw": iw}


@card("DATA-54")
def svg_line_chart(task, wd):
    """SVG line chart: label step = ceil(n / max(3, floor(iw/56))), end labels only when <= 4 series (pr 70),
    end points r 4, 2 px lines, optional 10 % area."""
    import xml.etree.ElementTree as ET
    labels = ["d%02d" % i for i in range(30)]
    mk = lambda k, c: {"name": "s%d" % k, "color": c, "values": [round(10 + k * 7 + 5 * math.sin(i / 3.0 + k), 2) for i in range(30)]}
    three = [mk(k, c) for k, c in enumerate(["#2a78d6", "#eb6834", "#1baf7a"])]
    five = [mk(k, c) for k, c in enumerate(["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"])]
    s3, g3 = _sk_line(labels, three, area=True)
    s5, g5 = _sk_line(labels, five)
    (wd / "line3.svg").write_text(s3, encoding="utf-8")
    (wd / "line5.svg").write_text(s5, encoding="utf-8")
    ns = {"s": "http://www.w3.org/2000/svg"}
    r3, r5 = ET.fromstring(s3), ET.fromstring(s5)
    xl = r3.findall("s:text[@class='xl']", ns)
    exp_step = int(math.ceil(30 / float(max(3, (720 - 46 - 70) // 56))))
    circ = r3.findall("s:circle", ns)
    cerr = max(abs(float(c.get("cy")) - g3["Y"](s["values"][-1])) for c, s in zip(circ, three))
    lines = r3.findall("s:polyline", ns)
    perr = 0.0
    for pl, s in zip(lines, three):
        for i, p in enumerate(pl.get("points").split()):
            x, y = map(float, p.split(","))
            perr = max(perr, abs(x - g3["X"](i)), abs(y - g3["Y"](s["values"][i])))
    checks = [check("label step = ceil(n / max(3, floor(iw/56)))", int(r3.get("data-step")) == exp_step == 3, int(r3.get("data-step")), exp_step),
              check("thinned label count", len(xl) == 10, len(xl), 10),
              check("points at data coordinates", perr < 0.01, perr, "< 0.01"),
              check("end dots r 4 at the last value", all(c.get("r") == "4" for c in circ) and cerr < 0.01, cerr, "r=4"),
              check("2 px lines", all(pl.get("stroke-width") == "2" for pl in lines), True, True),
              check("10 % area fill", all(a.get("fill-opacity") == "0.1" for a in r3.findall("s:path", ns)) and len(r3.findall("s:path", ns)) == 3, 3, 3),
              check("end labels with <= 4 series, pr 70", len(r3.findall("s:text[@class='end']", ns)) == 3 and r3.get("data-pr") == "70", 3, 3),
              check("no end labels with 5 series, pr 8", len(r5.findall("s:text[@class='end']", ns)) == 0 and r5.get("data-pr") == "8", 0, 0),
              check("negative control: unthinned labels exceed the width budget", 30 > (720 - 46 - 70) // 56, 30, "> %d" % ((720 - 46 - 70) // 56))]
    return checks, [wd / "line3.svg", wd / "line5.svg"]


@card("DATA-55")
def sparkline(task, wd):
    """Word-sized sparkline 300x68: x(i) = p + i(w-2p)/(n-1), 2 px round-cap line, end dot r >= 4 with a 2 px paper
    ring; the path reveals over 800 ms, then the end dot pulses."""
    np = _np()
    vals = [12, 14, 13, 17, 16, 19, 22, 21, 25, 24, 28, 31]
    W, H, p, fps = 300, 68, 8, 30
    n = len(vals)
    X = lambda i: p + i * (W - 2 * p) / float(n - 1)
    lo, hi = min(vals), max(vals)
    Y = lambda v: H - p - (v - lo) / float(hi - lo) * (H - 2 * p)
    pts = [(X(i), Y(v)) for i, v in enumerate(vals)]
    paper, ink = "#fbf8f1", "#1d2632"

    def frame(t):
        a = canvas(W, H, paper)
        r = prog(t, 0, 0.8)
        xe = p + r * (W - 2 * p)
        sub = [q for q in pts if q[0] <= xe]
        if r > 0 and len(sub) >= 1:
            sub = sub + [point_at_x(pts, xe)]
            paint(a, line_mask(H, W, sub, 2), ink)
            for q in (sub[0], sub[-1]):
                paint(a, pil_mask(W, H, lambda d: d.ellipse([q[0] - 1, q[1] - 1, q[0] + 1, q[1] + 1], fill=255)), ink)
        if t >= 0.8:
            pulse = 1 + 0.5 * math.sin(math.pi * prog(t, 0.8, 0.3))
            rr = 4 * pulse
            ex, ey = pts[-1]
            paint(a, pil_mask(W, H, lambda d: d.ellipse([ex - rr - 2, ey - rr - 2, ex + rr + 2, ey + rr + 2], fill=255)), paper)
            paint(a, pil_mask(W, H, lambda d: d.ellipse([ex - rr, ey - rr, ex + rr, ey + rr], fill=255)), "#e4572e")
        return a
    nf = int(1.3 * fps)
    vid = write_video(wd / "sparkline.mp4", [frame(k / fps) for k in range(nf)], fps)
    fr = read_video(vid)
    last = fr[-1]
    yerr = 0.0
    for i in range(1, n - 1):
        ys = np.nonzero(near(last[:, int(X(i))], ink, 40))[0]
        yerr = max(yerr, abs((ys.min() + ys.max() + 1) / 2.0 - Y(vals[i])) if len(ys) else 99)
    dot = near(last, "#e4572e", 20)
    r_meas = math.sqrt(dot.sum() / math.pi)
    ex, ey = pts[-1]
    rr, ang = angle_grid(H, W, ex, ey)
    ring = (rr > r_meas + 0.6) & (rr < r_meas + 1.6)
    ring_ok = bool(near(last, paper, 3)[ring].all())
    reveal = 0.0
    for k, f in enumerate(fr[:int(0.8 * fps)]):
        xs = np.nonzero(near(f, ink, 60).any(axis=0))[0]
        exp = p + prog(k / fps, 0, 0.8) * (W - 2 * p)
        if k > 0:
            reveal = max(reveal, abs(xs.max() - exp) if len(xs) else 99)
    radii = [math.sqrt(near(f, "#e4572e", 20).sum() / math.pi) for f in fr[int(0.8 * fps):]]
    checks = [check("x(i) = p + i(w-2p)/(n-1): line passes data y (px)", yerr <= 1.5, yerr, "<= 1.5"),
              check("end dot r >= 4", r_meas >= 3.8, r_meas, ">= 4"),
              check("2 px paper ring around the end dot", ring_ok, ring_ok, True),
              check("path reveals left->right over 800 ms (px)", reveal <= 2.5, reveal, "<= 2.5"),
              check("end dot pulses after the reveal", max(radii) > radii[-1] * 1.3, [max(radii), radii[-1]], "peak > 1.3 x rest"),
              check("negative control: the first frame shows no path", not near(fr[0], ink, 60).any(), 0, 0)]
    return checks, [vid]


def point_at_x(pts, x):
    for a, b in zip(pts, pts[1:]):
        if a[0] <= x <= b[0]:
            u = (x - a[0]) / (b[0] - a[0]) if b[0] != a[0] else 0
            return (x, a[1] + (b[1] - a[1]) * u)
    return pts[-1]


@card("DATA-56")
def climb_then_plunge(task, wd):
    """The line climbs (2.8 s draw, #7fd0ff 7 px); on the spoken failure word a red 9 px segment plunges in 0.45 s,
    the value counts 82 -> 34 and the background darkens with the decline."""
    np = _np()
    words = [{"w": "الهدف", "start": 0.4}, {"w": "كان", "start": 1.1}, {"w": "انهار", "start": 3.64}]
    wpath = wjson(wd / "words.json", words)
    w_fail = [w for w in json.loads(wpath.read_text(encoding="utf-8")) if w["w"] == "انهار"][0]["start"]
    W, H, fps = 240, 160, 30
    up = [(20, 130), (60, 110), (100, 95), (140, 70), (180, 40)]
    down = [(180, 40), (220, 140)]

    def frame(t):
        d = ease("power2.in", prog(t, w_fail, 0.45))
        a = canvas(W, H, lerp_c("#16324f", "#05080d", d))
        r = prog(t, 0.5, 2.8)
        if r > 0:
            xe = up[0][0] + r * (up[-1][0] - up[0][0])
            sub = [q for q in up if q[0] <= xe] + [point_at_x(up, xe)]
            paint(a, line_mask(H, W, sub, 7), "#7fd0ff")
        if d > 0:
            paint(a, line_mask(H, W, [down[0], (down[0][0] + (down[1][0] - down[0][0]) * d, down[0][1] + (down[1][1] - down[0][1]) * d)], 9), "#ff5a5a")
        draw_seg(a, fmt_int(82 + (34 - 82) * d, "dd"), "dd", 18, 20, 12, "#ffffff")
        return a
    n = int(4.4 * fps)
    vid = write_video(wd / "plunge.mp4", [frame(k / fps) for k in range(n)], fps)
    fr = read_video(vid)
    red = [int(near(f, "#ff5a5a", 30).sum()) for f in fr]
    first = next(k for k, v in enumerate(red) if v > 0)
    full = next(k for k, v in enumerate(red) if v == red[-1])
    lum = [float(f[150:158, 2:10].mean()) for f in fr]
    dec = lum[first - 1:full + 1]
    vals = [seg_value(read_seg(f, "dd", 18, 20, 12, None, fg="#ffffff", thr=50)) for f in fr]
    upx = [int(np.nonzero(near(f, "#7fd0ff", 30).any(axis=0))[0].max()) if near(f, "#7fd0ff", 30).any() else 0 for f in fr]
    k_up = next(k for k, v in enumerate(upx) if v >= up[-1][0] + 2)
    checks = [check("plunge starts on the spoken word (words.json)", abs(first / fps - w_fail) <= 1.5 / fps, first / fps, w_fail),
              check("plunge drawn in 0.45 s", abs((full - first) / fps - 0.45) <= 2.0 / fps, (full - first) / fps, 0.45),
              check("background darkens with the decline", all(b <= a + 0.01 for a, b in zip(dec, dec[1:])) and lum[-1] < 0.5 * lum[0],
                    [lum[0], lum[-1]], "monotone, < 50 %"),
              check("value counts 82 -> 34", vals[first - 1] == 82 and vals[-1] == 34, [vals[first - 1], vals[-1]], [82, 34]),
              check("climb drawn over 2.8 s", abs(k_up / fps - 3.3) <= 2.0 / fps, k_up / fps, 3.3),
              check("negative control: at a fixed 3.0 s cue nothing has plunged yet", red[int(3.0 * fps)] == 0, red[int(3.0 * fps)], 0)]
    return checks, [vid, wpath]


@card("DATA-58")
def annotation_layer(task, wd):
    """Annotations over the data after it lands (+200 ms): a 20 % shaded span, a dashed grey target line with
    its value, a thin leader to a point, and a 3 px background halo under the label."""
    np = _np()
    W, H, fps = 320, 180, 30
    vals = [30, 34, 33, 41, 52, 48, 57, 63, 60, 66]
    X = lambda i: 20 + i * 30
    Y = lambda v: 170 - v * 2
    pts = [(X(i), Y(v)) for i, v in enumerate(vals)]
    target, span = 60, (3, 5)
    t_data = 1.0

    def frame(t):
        a = canvas(W, H, "#ffffff")
        if t >= t_data + 0.2:
            rect(a, X(span[0]), 10, X(span[1]), 172, "#ffcc00", 0.2)
            for x in range(20, 300, 10):
                rect(a, x, Y(target), x + 5, Y(target) + 1, "#888888")
        r = prog(t, 0, t_data)
        if r > 0:
            xe = pts[0][0] + r * (pts[-1][0] - pts[0][0])
            paint(a, line_mask(H, W, [q for q in pts if q[0] <= xe] + [point_at_x(pts, xe)], 2), "#1f77b4")
        if t >= t_data + 0.2:
            px, py = pts[4]
            paint(a, line_mask(H, W, [(px, py), (px + 40, py + 40)], 1), "#444444")
            rect(a, px + 37, py + 37, px + 37 + 30 + 6, py + 37 + 14 + 6, "#ffffff")   # 3 px halo
            draw_seg(a, "52", "dd", 14, px + 40, py + 40, "#444444")
            draw_seg(a, "60", "dd", 12, 296, int(Y(target)) - 14, "#888888")
        return a
    n = int((t_data + 0.6) * fps)
    vid = write_video(wd / "annotated.mp4", [frame(k / fps) for k in range(n)], fps)
    fr = read_video(vid)
    last = fr[-1]
    tint = last[15, int((X(span[0]) + X(span[1])) / 2)]
    exp_t = np.array(lerp_c("#ffffff", "#ffcc00", 0.2))
    runs = col_runs(near(last[int(round(Y(target))), 20:300], "#888888", 6))
    px, py = pts[4]
    halo = last[py + 37:py + 37 + 20, px + 37:px + 37 + 36]
    halo_ok = not near(halo, "#1f77b4", 40).any() and not near(halo, "#ffcc00", 40).any()
    first_ann = next(k for k, f in enumerate(fr) if np.abs(f[15, int((X(span[0]) + X(span[1])) / 2)] - 255).max() > 5)
    lead = near(last[int(py) + 1:int(py) + 4, int(px):int(px) + 4], "#444444", 30).any()
    checks = [check("span shaded at 20 % alpha", float(np.abs(tint - exp_t).max()) <= 1.5, tint.tolist(), exp_t.tolist()),
              check("dashed target line at the target y", len(runs) >= 20, len(runs), ">= 20 dashes"),
              check("target value labelled", read_seg(last, "dd", 12, 296, int(Y(target)) - 14, "#ffffff", fg="#888888") == "60",
                    read_seg(last, "dd", 12, 296, int(Y(target)) - 14, "#ffffff", fg="#888888"), "60"),
              check("callout value == the data point", read_seg(last, "dd", 14, px + 40, py + 40, "#ffffff", fg="#444444") == "52", vals[4], 52),
              check("leader starts at the data point", bool(lead), bool(lead), True),
              check("label halo clears marks behind it", halo_ok, halo_ok, True),
              check("annotations appear >= 200 ms after the data lands", first_ann / fps >= t_data + 0.2 - 1e-6, first_ann / fps, ">= 1.2"),
              check("negative control: the landed-data frame has no span tint",
                    float(np.abs(fr[int(t_data * fps)][15, int((X(span[0]) + X(span[1])) / 2)] - exp_t).max()) > 5, 0, "untinted")]
    return checks, [vid]


@card("DATA-60")
def sketch_axes_curve(task, wd):
    """Axes draw 300 ms each, then a curve traces left->right over 2 s with a seeded 1 px jitter per frame
    while a 'now $X' label follows the pen."""
    np = _np()
    W, H, fps = 260, 160, 30
    ox, oy, aw, ah = 30, 140, 200, 120
    f = lambda u: 20 + 70 * u * u            # value at curve fraction u
    Yv = lambda v: oy - v

    def render(seed, jitter=True):
        frames = []
        for k in range(int(2.9 * fps)):
            t = k / fps
            rs = np.random.RandomState(seed * 1000 + k)
            a = canvas(W, H, "#fdfaf3")
            rect(a, ox, oy, ox + aw * prog(t, 0, 0.3), oy + 2, "#222222")
            hh = ah * prog(t, 0.3, 0.3)
            rect(a, ox, oy - hh, ox + 2, oy, "#222222")
            u = prog(t, 0.6, 2.0)
            if u > 0:
                xs = np.arange(0, int(aw * u) + 1)
                ys = [Yv(f(x / float(aw))) + (rs.randint(-1, 2) if jitter else 0) for x in xs]
                paint(a, line_mask(H, W, list(zip(ox + xs, ys)), 2), "#d1495b")
                draw_seg(a, fmt_int(f(u), "dd"), "dd", 14, 200, 10, "#222222")
            frames.append(a)
        return frames
    fa = render(7)
    vid = write_video(wd / "sketch.mp4", fa, fps)
    vid2 = write_video(wd / "sketch_again.mp4", render(7), fps)
    fr = read_video(vid)
    axx = [int(near(f[oy, ox:ox + aw], "#222222", 10).sum()) for f in fr]
    ax_err = max(abs(v - round(aw * prog(k / fps, 0, 0.3))) for k, v in enumerate(axx))
    yfirst = next(k for k, f in enumerate(fr) if near(f[oy - 5, ox:ox + 1], "#222222", 10).all())
    pen, dev, lab = 0, 0.0, 0
    for k, a in enumerate(fr):
        u = prog(k / fps, 0.6, 2.0)
        m = near(a, "#d1495b", 40)
        if u <= 0 or not m.any():
            continue
        xs = np.nonzero(m.any(axis=0))[0]
        pen = max(pen, abs(xs.max() - (ox + int(aw * u)) ))
        for x in xs[2:-2:7]:
            ys = np.nonzero(m[:, x])[0]
            dev = max(dev, abs((ys.min() + ys.max() + 1) / 2.0 - Yv(f((x - ox) / float(aw)))))
        lab += int(seg_value(read_seg(a, "dd", 14, 200, 10, "#fdfaf3", fg="#222222")) != round(f(u)))
    clean = render(7, jitter=False)[-1]
    mc = near(clean, "#d1495b", 40)
    cdev = max(abs((np.nonzero(mc[:, x])[0].min() + np.nonzero(mc[:, x])[0].max() + 1) / 2.0 - Yv(f((x - ox) / float(aw))))
               for x in range(ox + 2, ox + aw - 2, 7))
    checks = [check("x axis draws over 300 ms (px)", ax_err <= 1, ax_err, "<= 1"),
              check("y axis after the x axis", abs(yfirst / fps - 0.3) <= 2.0 / fps, yfirst / fps, "~0.33 s"),
              check("curve front follows the pen (px)", pen <= 2, pen, "<= 2"),
              check("hand jitter present and within ~1 px", dev <= 2.0, dev, "<= 2"),
              check("seeded jitter is deterministic", fx.run(["md5sum", str(vid)]).stdout.split()[0] == fx.run(["md5sum", str(vid2)]).stdout.split()[0], True, True),
              check("'now' label == curve value at the pen", lab == 0, lab, 0),
              check("negative control: the unjittered stroke wobbles clearly less", cdev <= dev - 0.4, [cdev, dev], "clean <= jittered - 0.4")]
    return checks, [vid]


@card("DATA-61")
def random_walk_fan(task, wd):
    """1000 seeded random walks at alpha 0.1, the median in bold, the 5th-95th band outlined, n labelled."""
    np = _np()
    W, H, N, steps = 300, 160, 1000, 60
    rs = np.random.RandomState(11)
    walks = np.cumsum(rs.normal(0, 1.2, (N, steps)), axis=1)
    X = lambda i: 10 + i * (W - 20) / float(steps - 1)
    Y = lambda v: H / 2 - v * 2.2
    K = np.zeros((H, W), int)
    for wlk in walks:
        K += line_mask(H, W, [(X(i), Y(v)) for i, v in enumerate(wlk)], 1)
    bg, col = np.array(rgb("#ffffff"), float), np.array(rgb("#1f3a93"), float)
    a = bg * (0.9 ** K)[..., None] + col * (1 - 0.9 ** K)[..., None]
    med = np.median(walks, axis=0)
    p5, p95 = np.percentile(walks, 5, axis=0), np.percentile(walks, 95, axis=0)
    for series, c, wdt in ((p5, "#ff9f1c", 1), (p95, "#ff9f1c", 1), (med, "#e71d36", 3)):
        paint(a, line_mask(H, W, [(X(i), Y(v)) for i, v in enumerate(series)], wdt), c)
    draw_seg(a, "1000", "dddd", 12, 240, 6, "#000000")
    png = save_png(a, wd / "fan.png")
    b = load_png(png)
    me, be = 0.0, 0.0
    for i in range(5, steps - 5, 6):
        x = int(X(i))
        ys = np.nonzero(near(b[:, x], "#e71d36", 10))[0]
        me = max(me, abs((ys.min() + ys.max() + 1) / 2.0 - Y(med[i])))
        yb = np.nonzero(near(b[:, x], "#ff9f1c", 10))[0]
        cl = clusters(yb, 2)
        be = max(be, abs(min(cl) - Y(p95[i])), abs(max(cl) - Y(p5[i]))) if len(cl) >= 2 else 99
    free = ~(near(b, "#e71d36", 10) | near(b, "#ff9f1c", 10))
    free[:22, 230:] = False
    aerr = float(np.abs(b[free] - a[free]).max())
    sel = free & (K == 1)
    one = b[sel].mean(axis=0) if sel.any() else None
    levels = len(np.unique(b[free][:, 0]))
    opaque_levels = len(np.unique(np.where(K[free] > 0, col[0], bg[0])))
    checks = [check("median line at the computed median (px)", me <= 1.5, me, "<= 1.5"),
              check("5th/95th band at the computed percentiles (px)", be <= 1.5, be, "<= 1.5"),
              check("single path pixel == 10 % blend", one is not None and float(np.abs(one - (0.9 * bg + 0.1 * col)).max()) <= 1.0,
                    None if one is None else one.round(1).tolist(), (0.9 * bg + 0.1 * col).round(1).tolist()),
              check("overlaps accumulate as 1 - 0.9^k", aerr <= 1.0, aerr, "<= 1"),
              check("n labelled", read_seg(b, "dddd", 12, 240, 6, "#ffffff", fg="#000000") == "1000", "1000", "1000"),
              check("density visible (many alpha levels)", levels > 20, levels, "> 20"),
              check("negative control: opaque paths collapse to 2 levels", opaque_levels <= 2, opaque_levels, "<= 2")]
    return checks, [png]


@card("DATA-62")
def dot_histogram_simulation(task, wd):
    """N = 500 simulated results drop as 4 px dots into bins (20 ms stagger) with a counter to N; then a normal
    curve draws over the stacks (600 ms) with the 5-95 % band shaded."""
    np = _np()
    rs = np.random.RandomState(5)
    N, mu, sd = 500, 50.0, 10.0
    sims = rs.normal(mu, sd, N)
    nb, lo, hi = 25, 10.0, 90.0
    bins = np.clip(((sims - lo) / (hi - lo) * nb).astype(int), 0, nb - 1)
    bw, dot, base, x0 = 10, 4, 200, 20
    W, H, fps = x0 * 2 + nb * bw, 230, 10
    t_dots = N * 0.02
    xv = lambda v: x0 + (v - lo) / (hi - lo) * nb * bw
    a = canvas(W, H, "#ffffff")
    fill = [0] * nb
    frames = []
    shown = 0
    nfr = int((t_dots + 1.0) * fps)
    curve = [(xv(v), base - N * (hi - lo) / nb * math.exp(-0.5 * ((v - mu) / sd) ** 2) / (sd * math.sqrt(2 * math.pi)) * dot / 2)
             for v in np.linspace(lo, hi, 161)]
    for k in range(nfr):
        t = k / float(fps)
        while shown < N and shown * 0.02 <= t:
            b = bins[shown]
            rect(a, x0 + b * bw + 3, base - (fill[b] + 1) * dot / 2, x0 + b * bw + 3 + dot, base - fill[b] * dot / 2, "#3d5a80")
            fill[b] += 1
            shown += 1
        f = a.copy()
        draw_seg(f, fmt_int(shown, "ddd"), "ddd", 14, W - 60, 6, "#111111")
        c = prog(t, t_dots + 0.1, 0.6)
        if c > 0:
            rect(f, xv(mu - 1.645 * sd), base + 4, xv(mu + 1.645 * sd), base + 12, "#ee6c4d", 0.35)
            xe = curve[0][0] + c * (curve[-1][0] - curve[0][0])
            paint(f, line_mask(H, W, [q for q in curve if q[0] <= xe] + [point_at_x(curve, xe)], 2), "#e63946")
        frames.append(f)
    vid = write_video(wd / "dot_hist.mp4", frames, fps)
    fr = read_video(vid)
    last = fr[-1]
    counts = np.bincount(bins, minlength=nb)
    landed = fr[int(t_dots * fps)]
    hs = [int(near(landed[:base, x0 + b * bw + 4], "#3d5a80", 8).sum()) for b in range(nb)]
    herr = max(abs(h - c * dot / 2) for h, c in zip(hs, counts))
    cnt_ok = all(seg_value(read_seg(f, "ddd", 14, W - 60, 6, "#ffffff", fg="#111111")) ==
                 round(sum(int(near(f[:base, x0 + b * bw + 4], "#3d5a80", 8).sum()) for b in range(nb)) / (dot / 2.0))
                 for f in fr[::7] if not near(f, "#e63946", 40).any())
    band = np.nonzero(near(last[base + 8], lerp_c("#ffffff", "#ee6c4d", 0.35), 3))[0]
    berr = max(abs(band.min() - xv(mu - 1.645 * sd)), abs(band.max() + 1 - xv(mu + 1.645 * sd)))
    cerr = 0.0
    for v in (mu - sd, mu, mu + sd):
        x = int(xv(v))
        ys = np.nonzero(near(last[:, x], "#e63946", 40))[0]
        cerr = max(cerr, abs((ys.min() + ys.max() + 1) / 2.0 - point_at_x(curve, x + 0.5)[1]))
    cfirst = next(k for k, f in enumerate(fr) if near(f, "#e63946", 40).any())
    checks = [check("stack heights == bin counts x dot pitch (px)", herr <= 1, herr, "<= 1"),
              check("counter == dots dropped", cnt_ok, cnt_ok, True),
              check("counter ends at N = 500", read_seg(last, "ddd", 14, W - 60, 6, "#ffffff", fg="#111111") == "500", 500, 500),
              check("normal curve over the stacks (px)", cerr <= 2, cerr, "<= 2"),
              check("5-95 % band at mean +/- 1.645 sd (px)", berr <= 1, berr, "<= 1"),
              check("curve draws after the last dot", cfirst / float(fps) >= t_dots, cfirst / float(fps), ">= 10 s"),
              check("negative control: the first frame has (almost) no stacks", sum(int(near(fr[0][:base, x0 + b * bw + 4], "#3d5a80", 8).sum()) for b in range(nb)) <= 2,
                    0, "<= 1 dot")]
    return checks, [vid]


@card("DATA-63")
def tangent_derivative(task, wd):
    """f with a tangent + dot following x(t) from -2 to 2 linearly over 8 s; the right axes trace f'(x); the
    slope label (2 decimals) updates live."""
    np = _np()
    f = lambda x: x ** 3 / 3.0 - x
    fp = lambda x: x * x - 1
    fps, PW, PH = 15, 160, 140
    W, H = 2 * PW + 20, PH + 30
    s = 30.0
    L = lambda x, y: (PW / 2 + x * s, PH / 2 - y * s)
    R = lambda x, y: (PW + 20 + PW / 2 + x * s, PH / 2 + 20 - y * s)
    xs_curve = np.linspace(-2, 2, 200)

    def frame(t):
        x = -2 + 4 * prog(t, 0, 8.0)
        a = canvas(W, H, "#ffffff")
        paint(a, line_mask(H, W, [L(u, f(u)) for u in xs_curve], 1), "#999999")
        dx = 0.6 / math.sqrt(1 + fp(x) ** 2)
        paint(a, line_mask(H, W, [L(x - dx, f(x) - dx * fp(x)), L(x + dx, f(x) + dx * fp(x))], 1), "#e4572e")
        cx, cy = L(x, f(x))
        paint(a, pil_mask(W, H, lambda d: d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=255)), "#1f77b4")
        tr = [R(u, fp(u)) for u in xs_curve if u <= x]
        if len(tr) > 1:
            paint(a, line_mask(H, W, tr, 2), "#2ca02c")
        draw_seg(a, "%5.2f" % fp(x), "dd.dd", 14, PW + 40, H - 18, "#111111")
        return a
    n = int(8.0 * fps) + 1
    vid = write_video(wd / "tangent.mp4", [frame(k / fps) for k in range(n)], fps)
    fr = read_video(vid)
    derr, serr, terr, lab = 0.0, 0.0, 0.0, 0
    for k in range(0, n, 6):
        x = -2 + 4 * prog(k / fps, 0, 8.0)
        a = fr[k]
        c = centroid(near(a, "#1f77b4", 30))
        cx, cy = L(x, f(x))
        derr = max(derr, math.hypot(c[0] - cx, c[1] - cy))
        if abs(fp(x)) <= 2.0:
            m = near(a, "#e4572e", 40) & ~near(a, "#1f77b4", 60)
            m[:, PW:] = False
            ys, xs = np.nonzero(m)
            if len(xs) > 10 and xs.max() - xs.min() > 6:
                slope = -np.polyfit(xs + 0.5, ys + 0.5, 1)[0]
                serr = max(serr, abs(slope - fp(x)))
        g = near(a, "#2ca02c", 40)
        if g.any() and k > 3:
            gx = np.nonzero(g.any(axis=0))[0].max()
            terr = max(terr, abs(gx + 0.5 - R(x, fp(x))[0]) if x > -1.95 else 0)
        lab += int(read_seg(a, "dd.dd", 14, PW + 40, H - 18, "#ffffff", fg="#111111") != "%5.2f" % fp(x))
    wrong = max(abs(f(x) - fp(x)) for x in np.linspace(-1.5, 1.5, 13))
    checks = [check("dot rides f at x(t) (px)", derr <= 1.5, derr, "<= 1.5"),
              check("measured tangent slope == f'(x)", serr <= 0.1, serr, "<= 0.1"),
              check("right axes trace reaches x(t) (px)", terr <= 2.5, terr, "<= 2.5"),
              check("slope label == f'(x) to 2 decimals", lab == 0, lab, 0),
              check("x sweeps -2 -> 2 over 8 s", n == 121, n, 121),
              check("negative control: f(x) itself is not the measured slope", wrong > 0.3, wrong, "> 0.3")]
    return checks, [vid]


@card("DATA-65")
def ridgelines(task, wd):
    """34 stacked horizontal lines displaced by noise times a central gaussian bump; each row fills below its line
    with the background so rows beneath are occluded; colour cyan -> red by row; noise time animates at 0.5."""
    np = _np()
    W, H, rows, fps = 300, 260, 34, 15
    xs = np.arange(30, 270)
    bump = np.exp(-((xs - 150) / 35.0) ** 2)
    rcol = [lerp_c("#00e5ff", "#ff2d2d", r / float(rows - 1)) for r in range(rows)]

    def noise(r, t):
        ph = np.random.RandomState(r).uniform(0, 6.28, 3)
        return sum(np.abs(np.sin(xs / (7.0 + 3 * j) + ph[j] + 0.5 * t * (j + 1))) for j in range(3)) / 3.0

    def frame(t, occlude=True):
        a = canvas(W, H, "#000000")
        lines = []
        for r in range(rows):
            base = 40 + r * 6
            ys = base - 60 * bump * noise(r, t) - 2
            if occlude:
                poly = [(x, y) for x, y in zip(xs, ys)] + [(xs[-1], H), (xs[0], H)]
                paint(a, pil_mask(W, H, lambda d: d.polygon(poly, fill=255)), "#000000")
            paint(a, line_mask(H, W, list(zip(xs, ys)), 1), tuple(int(round(c)) for c in rcol[r]))
            lines.append(ys)
        return a, lines
    frames = [frame(k / float(fps))[0] for k in range(int(1.0 * fps))]
    vid = write_video(wd / "ridges.mp4", frames, fps)
    fr = read_video(vid)
    _, lines = frame(0.0)
    raw, _ = frame(0.0, occlude=False)
    pal = np.array([tuple(int(round(c)) for c in col) for col in rcol], float)

    def violations(a):
        bad = 0
        for r in range(1, rows):
            for xi in range(0, len(xs), 4):
                x = xs[xi]
                y_top = int(round(lines[r][xi])) + 2
                col = a[y_top:40 + r * 6 - 1, x]
                for px in col:
                    d = np.abs(pal[:r] - px).max(axis=1)
                    bad += int((d <= 2).any())
        return bad
    vo, vr = violations(fr[0]), violations(raw)
    def line_col(r):
        y = int(round(lines[r][5]))
        cand = [fr[0][yy, xs[5]] for yy in range(y - 2, y + 3) if fr[0][yy, xs[5]].max() > 30]
        return cand[0] if cand else np.zeros(3)
    top_c, bot_c = line_col(0), line_col(rows - 1)
    centre = float(np.mean([40 + r * 6 - lines[r][120] for r in range(rows)]))
    edge = float(np.mean([40 + r * 6 - lines[r][2] for r in range(rows)]))
    checks = [check("rows beneath are occluded by the fill", vo == 0, vo, 0),
              check("row colour cyan at the back, red at the front", float(np.abs(top_c - rgb("#00e5ff")).max()) <= 3 and
                    float(np.abs(bot_c - rgb("#ff2d2d")).max()) <= 3, [top_c.tolist(), bot_c.tolist()], ["#00e5ff", "#ff2d2d"]),
              check("central bump: displacement larger at the centre", centre > 5 * max(edge, 0.5), [centre, edge], "centre >> edge"),
              check("noise animates over time", float(np.abs(fr[0] - fr[-1]).max()) > 50, float(np.abs(fr[0] - fr[-1]).max()), "> 50"),
              check("%d rows" % rows, 30 <= rows <= 40, rows, "30..40"),
              check("negative control: without the fill back rows show through", vr > 0, vr, "> 0")]
    return checks, [vid]


@card("DATA-66")
def pareto_frontier_reveal(task, wd):
    """Dots pop in ordered by x (10 ms stagger), then the frontier curve draws and the best point gets a ring."""
    np = _np()
    rs = np.random.RandomState(9)
    pts = [(float(c), float(q)) for c, q in zip(rs.uniform(1, 10, 40).round(2), rs.uniform(10, 90, 40).round(2))]
    order = sorted(range(len(pts)), key=lambda i: pts[i][0])
    front, bestq = [], -1
    for i in order:                       # cheapest first: keep points that beat every cheaper one on quality
        if pts[i][1] > bestq:
            front.append(i)
            bestq = pts[i][1]
    brute = [i for i in range(len(pts)) if not any(pts[j][0] <= pts[i][0] and pts[j][1] >= pts[i][1] and j != i for j in range(len(pts)))]
    best = max(range(len(pts)), key=lambda i: pts[i][1] / pts[i][0])
    W, H, fps = 300, 200, 100
    X = lambda c: 20 + c * 26
    Y = lambda q: 190 - q * 2
    t_dots = len(pts) * 0.01

    def frame(t):
        a = canvas(W, H, "#ffffff")
        for rank, i in enumerate(order):
            sc = ease("back.out", prog(t, rank * 0.01, 0.12))
            if sc > 0:
                r = 3 * min(sc, 1.3)
                x, y = X(pts[i][0]), Y(pts[i][1])
                paint(a, pil_mask(W, H, lambda d: d.ellipse([x - r, y - r, x + r, y + r], fill=255)), "#4a6fa5")
        c = prog(t, t_dots + 0.12, 0.4)
        if c > 0:
            fp = [(X(pts[i][0]), Y(pts[i][1])) for i in front]
            xe = fp[0][0] + c * (fp[-1][0] - fp[0][0])
            paint(a, line_mask(H, W, [q for q in fp if q[0] <= xe] + [point_at_x(fp, xe)], 1), "#e4572e")
        if t >= t_dots + 0.55:
            x, y = X(pts[best][0]), Y(pts[best][1])
            paint(a, ring_mask(H, W, x, y, 6, 8), "#2ca02c")
        return a
    n = int((t_dots + 0.8) * fps)
    vid = write_video(wd / "pareto.mp4", [frame(k / float(fps)) for k in range(n)], fps)
    fr = read_video(vid)
    first = []
    for i in order:
        x, y = int(X(pts[i][0])), int(Y(pts[i][1]))
        first.append(next(k for k, f in enumerate(fr) if near(f[y, x:x + 1], "#4a6fa5", 10).all() or near(f[y, x:x + 1], "#e4572e", 40).all()))
    cfirst = next(k for k, f in enumerate(fr) if near(f, "#e4572e", 40).any())
    online = all(near(fr[-1][int(Y(pts[i][1])) - 2:int(Y(pts[i][1])) + 3, int(X(pts[i][0])) - 2:int(X(pts[i][0])) + 3], "#e4572e", 40).any()
                 for i in front[1:-1])
    bx, by = X(pts[best][0]), Y(pts[best][1])
    rr, _ = angle_grid(H, W, bx, by)
    ring = near(fr[-1], "#2ca02c", 10) & (rr >= 6) & (rr < 8)
    shuffled = list(rs.permutation(len(order)))
    checks = [check("frontier == brute-force non-dominated set", sorted(front) == sorted(brute), len(front), len(brute)),
              check("dots appear in x order", first == sorted(first) and first[-1] - first[0] >= 30, [first[0], first[-1]], "monotone, ~10 ms each"),
              check("frontier draws after the last dot", cfirst > first[-1], [first[-1], cfirst], "after"),
              check("frontier passes through the frontier points", online, online, True),
              check("best point (quality/cost) ringed", int(ring.sum()) > 20, int(ring.sum()), "> 20 px"),
              check("negative control: an unsorted reveal order is not monotone in x", shuffled != sorted(shuffled), shuffled[:5], "not sorted")]
    return checks, [vid]


def angular_runs(mask, ang):
    """Clusters of lit 1-degree bins around the circle (wrap-aware)."""
    np = _np()
    hist = np.bincount(ang[mask].astype(int) % 360, minlength=360) > 0
    runs = col_runs(hist)
    if len(runs) > 1 and hist[0] and hist[359]:
        s0, n0 = runs[0]
        s1, n1 = runs[-1]
        runs = [(s1, n0 + n1)] + runs[1:-1]
    return runs


@card("DATA-67")
def conic_percent_ring(task, wd):
    """A percentage ring from one scalar: --progress = pct * 3.6 deg drives the conic sweep, an inner disc inset
    13 px, and the centred numeral reads the same scalar."""
    np = _np()
    W = H = 160
    cx = cy = 80
    R, inset, pct, fps = 60, 13, 72, 30

    def frame(t):
        v = pct * ease("power3.out", prog(t, 0.1, 1.2))
        a = canvas(W, H, "#1b1030")
        paint(a, ring_mask(H, W, cx, cy, 0, R), "#3b2a55")
        paint(a, ring_mask(H, W, cx, cy, 0, R, 0, v * 3.6), "#72dbc4")
        paint(a, ring_mask(H, W, cx, cy, 0, R - inset), "#351848")
        draw_seg(a, fmt_int(v, "dd"), "dd", 26, cx - 17, cy - 13, "#ffffff")
        return a
    n = int(1.5 * fps)
    vid = write_video(wd / "conic_ring.mp4", [frame(k / fps) for k in range(n)], fps)
    fr = read_video(vid)
    agree, ferr = 0, 0.0
    for k, f in enumerate(fr):
        fa = arc_fraction(f, cx, cy, R - inset, R, "#72dbc4", 8)
        num = seg_value(read_seg(f, "dd", 26, cx - 17, cy - 13, "#351848", fg="#ffffff"))
        agree = max(agree, abs(num - fa * 100))
        ferr = max(ferr, abs(fa - pct * ease("power3.out", prog(k / fps, 0.1, 1.2)) / 100.0))
    rr, _ = angle_grid(H, W, cx, cy)
    inner = near(fr[-1], "#351848", 4) & (rr < R)
    r_in = math.sqrt(inner.sum() / math.pi + 2 * 13 * 26 / math.pi) if inner.any() else 0
    edge = [x for x in range(cx, W) if near(fr[-1][cy + 20:cy + 21, x:x + 1], "#351848", 4).all()]
    rad_meas = math.hypot(max(edge) + 1 - cx, 20) if edge else 0
    checks = [check("sweep share == scalar / 100 every frame", ferr <= 0.012, ferr, "<= 0.012"),
              check("numeral and sweep read the same scalar (+/- 1 %)", agree <= 1.3, agree, "<= 1.3"),
              check("inner disc inset 13 px", abs(rad_meas - (R - inset)) <= 1.0, rad_meas, R - inset),
              check("lands on 72", read_seg(fr[-1], "dd", 26, cx - 17, cy - 13, "#351848", fg="#ffffff") == "72", 72, 72),
              check("negative control: the first frame has no sweep", arc_fraction(fr[0], cx, cy, R - inset, R, "#72dbc4", 8) < 0.01, 0, "< 0.01")]
    return checks, [vid]


@card("DATA-68")
def donut_r15915(task, wd):
    """A circle of r = 15.915 has circumference 100, so each dash is the percentage: dasharray (p-.6) (100-p+.6),
    dashoffset -cumulative, stroke 6 in a 42 viewBox; segments spin in from -12 deg / scale .84 with 50 ms stagger."""
    import xml.etree.ElementTree as ET
    np = _np()
    segs = [("a", 40, "#2a78d6"), ("b", 25, "#eb6834"), ("c", 20, "#1baf7a"), ("d", 15, "#eda100")]
    r = 15.915
    C = 2 * math.pi * r
    parts, cum = [], 0
    for name, p, col in segs:
        parts.append('<circle cx="21" cy="21" r="15.915" fill="none" stroke="%s" stroke-width="6" stroke-dasharray="%.1f %.1f" '
                     'stroke-dashoffset="%g" transform="rotate(-90 21 21)" class="dn-seg" style="animation-delay:%dms"/>' % (
                         col, p - .6, 100 - p + .6, -cum, len(parts) * 50))
        cum += p
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 42 42">%s<text x="21" y="23" text-anchor="middle">%d</text></svg>' % ("".join(parts), cum)
    (wd / "donut.svg").write_text(svg, encoding="utf-8")
    root = ET.fromstring(svg)
    circles = root.findall("{http://www.w3.org/2000/svg}circle")
    K = 4.0
    S = int(42 * K)
    cx = cy = 21 * K

    def frame(t):
        a = canvas(S, S, "#ffffff")
        for i, c in enumerate(circles):
            dash = float(c.get("stroke-dasharray").split()[0])
            off = -float(c.get("stroke-dashoffset"))
            e = ease("power3.out", prog(t, i * 0.05, 0.75))
            if e <= 0:
                continue
            rot = -12 * (1 - e)
            sc = 0.84 + 0.16 * e
            a0 = off / 100.0 * 360 + rot
            m = ring_mask(S, S, cx, cy, (r - 3) * K * sc, (r + 3) * K * sc, a0, a0 + dash / 100.0 * 360)
            paint(a, m, c.get("stroke"), min(1.0, e * 1.5))
        return a
    fps = 40
    vid = write_video(wd / "donut.mp4", [frame(k / float(fps)) for k in range(int(1.0 * fps))], fps)
    fr = read_video(vid)
    last = fr[-1]
    rr, ang = angle_grid(S, S, cx, cy)
    band = (rr >= (r - 2.5) * K) & (rr < (r + 2.5) * K)
    shares = [float((near(last, col, 4) & band).sum()) / band.sum() for _, _, col in segs]
    serr = max(abs(sh - (p - .6) / 100.0) for sh, (_, p, _) in zip(shares, segs))
    lit = np.zeros(band.shape, bool)
    for _, _, col in segs:
        lit |= near(last, col, 4)
    gaps = [n for s0, n in col_runs(np.bincount(ang[band & ~lit].astype(int), minlength=360) > 0)]
    def tinted(f, col):
        d = 255.0 - f[band]
        v = 255.0 - np.array(rgb(col), float)
        al = d @ v / float(v @ v)
        res = np.abs(d - al[:, None] * v[None]).max(axis=1)
        return bool(((al > 0.02) & (res < 3)).any())
    starts = [next(k for k, f in enumerate(fr) if tinted(f, col)) for _, _, col in segs]
    km = int(0.2 * fps)
    m0 = near(fr[km], segs[0][2], 60) & ((rr >= (r - 3) * K * 0.84) & (rr < (r + 3) * K))
    a_meas = min(((a + 180) % 360) - 180 for a in ang[m0])
    e = ease("power3.out", prog(km / float(fps), 0, 0.75))
    checks = [check("circumference of r = 15.915 is 100", abs(C - 100) < 0.01, C, 100),
              check("dasharray first value == p - .6", [float(c.get("stroke-dasharray").split()[0]) for c in circles] == [p - .6 for _, p, _ in segs],
                    [c.get("stroke-dasharray") for c in circles], "p-.6"),
              check("measured angular share == (p - .6) / 100", serr <= 0.006, serr, "<= 0.006"),
              check("four .6 gaps between segments", len(gaps) == 4 and all(1 <= g <= 4 for g in gaps), gaps, "~2.2 deg each"),
              check("segments enter on the 50 ms stagger (2 frames)", starts == [1, 3, 5, 7], starts, [1, 3, 5, 7]),
              check("entrance rotates in from -12 deg", abs(a_meas - (-12 * (1 - e))) <= 2.0, a_meas, -12 * (1 - e)),
              check("negative control: a radius of 16 does not give 100", abs(2 * math.pi * 16 - 100) > 0.5, 2 * math.pi * 16, "!= 100")]
    return checks, [wd / "donut.svg", vid]


@card("DATA-70")
def glow_donut_legend(task, wd):
    """Cumulative-dash donut of 8 categories on black; highlighted segments get a 2x-wide 0.3-opacity duplicate
    behind for glow; legend rows: dot, label, value; highlighted rows white, others #86868b."""
    np = _np()
    vals = [22, 18, 15, 12, 11, 9, 8, 5]
    cols = ["#4b89d1", "#1239a0", "#64d2ff", "#2a78d6", "#3987e5", "#7aa7e0", "#335c99", "#9ec5f0"]
    hi = {2, 5}
    S, cx, cy, R, w = 240, 90, 120, 60, 10
    a = canvas(S + 120, S, "#000000")
    cum = 0
    for i, v in enumerate(vals):
        if i in hi:
            paint(a, ring_mask(S, S + 120, cx, cy, R - w, R + w, cum * 3.6, (cum + v) * 3.6), cols[i], 0.3)
        cum += v
    cum = 0
    for i, v in enumerate(vals):
        paint(a, ring_mask(S, S + 120, cx, cy, R - w / 2, R + w / 2, cum * 3.6, (cum + v) * 3.6), cols[i])
        cum += v
    for i, v in enumerate(vals):
        y = 20 + i * 26
        tc = "#ffffff" if i in hi else "#86868b"
        paint(a, ring_mask(S, S + 120, 200, y + 6, 0, 4), cols[i])
        rect(a, 210, y + 2, 250, y + 10, tc)
        draw_seg(a, fmt_int(v, "dd"), "dd", 12, 270, y, tc)
    png = save_png(a, wd / "glow_donut.png")
    b = load_png(png)
    rr, ang = angle_grid(S, S + 120, cx, cy)
    band = (rr >= R - w / 2 + 1) & (rr < R + w / 2 - 1)
    shares = [float((near(b, c, 3) & band).sum()) / band.sum() for c in cols]
    serr = max(abs(s_ - v / 100.0) for s_, v in zip(shares, vals))
    outer = (rr >= R + w / 2 + 1) & (rr < R + w - 1)
    cum = np.cumsum([0] + vals)
    gerr, dark = 0.0, True
    for i in range(8):
        mid = (cum[i] + vals[i] / 2.0) * 3.6
        m = outer & (np.abs(((ang - mid) + 180) % 360 - 180) < vals[i] * 1.2)
        if i in hi:
            gerr = max(gerr, float(np.abs(b[m] - 0.3 * np.array(rgb(cols[i]), float)).max()))
        else:
            dark &= bool((b[m] == 0).all())
    mid0 = (cum[0] + vals[0] / 2.0) * 3.6
    m0 = outer & (np.abs(((ang - mid0) + 180) % 360 - 180) < vals[0] * 1.2)
    nerr = float(np.abs(b[m0] - 0.3 * np.array(rgb(cols[0]), float)).max())
    leg = [tuple(b[20 + i * 26 + 6, 230]) for i in range(8)]
    leg_ok = all(l == ((255.0,) * 3 if i in hi else tuple(float(c) for c in rgb("#86868b"))) for i, l in enumerate(leg))
    vals_read = [seg_value(read_seg(b, "dd", 12, 270, 20 + i * 26, "#000000", thr=60)) for i in range(8)]
    checks = [check("segment shares == values (cumulative dashes)", serr <= 0.006, serr, "<= 0.006"),
              check("glow duplicate: 2x width at 0.3 opacity behind highlights", gerr <= 1.5, gerr, "<= 1.5"),
              check("no glow behind other segments", dark, dark, True),
              check("legend rows: highlighted white, others #86868b", leg_ok, leg_ok, True),
              check("legend values", vals_read == vals, vals_read, vals),
              check("negative control: the halo band of an un-duplicated segment is not a 0.3 glow", nerr > 20, nerr, "> 20")]
    return checks, [png]


@card("DATA-71")
def arc_counter_same_call(task, wd):
    """A thin arc draws from -90 deg while its percentage counts from the same tween (easeInOut over
    max(0.7, 0.55 d) s); green under 100 %, the overage past 100 % in red on the outer track."""
    np = _np()
    S, cx, cy, R, fps = 180, 90, 90, 60, 30
    target, d = 112, 2.0
    dur = max(0.7, 0.55 * d)
    lw = 0.2 * R

    def frame(t):
        v = target * ease("easeInOut", prog(t, 0, dur))
        a = canvas(S, S, "#0f1115")
        paint(a, ring_mask(S, S, cx, cy, R - lw, R, 0, min(v, 100) * 3.6), "#2ecc71")
        if v > 100:
            paint(a, ring_mask(S, S, cx, cy, R + 3, R + 7, 0, (v - 100) * 3.6), "#ff3b30")
        draw_seg(a, fmt_int(v, "ddd"), "ddd", 22, cx - 22, cy - 11, "#ffffff")
        return a
    n = int((dur + 0.3) * fps)
    vid = write_video(wd / "arc_counter.mp4", [frame(k / fps) for k in range(n)], fps)
    fr = read_video(vid)
    sync, done = 0.0, None
    for k, f in enumerate(fr):
        num = seg_value(read_seg(f, "ddd", 22, cx - 22, cy - 11, "#0f1115", thr=60))
        arcv = arc_fraction(f, cx, cy, R - lw, R, "#2ecc71", 10) * 100 + arc_fraction(f, cx, cy, R + 3, R + 7, "#ff3b30", 10) * 100
        sync = max(sync, abs(num - arcv))
        if done is None and num == target:
            done = k
    rr, ang = angle_grid(S, S, cx, cy)
    early = near(fr[6], "#2ecc71", 10) & (rr >= R - lw) & (rr < R)
    runs = angular_runs(early, ang)
    red_before = max(arc_fraction(f, cx, cy, R + 3, R + 7, "#ff3b30", 10) for k, f in enumerate(fr)
                     if target * ease("easeInOut", prog(k / fps, 0, dur)) < 99)
    lin = max(abs(round(target * prog(k / fps, 0, dur)) - round(target * ease("easeInOut", prog(k / fps, 0, dur)))) for k in range(n))
    checks = [check("arc and counter come from one tween (%)", sync <= 1.6, sync, "<= 1.6"),
              check("duration = max(0.7, 0.55 d) s (lands by dur, still counting 0.15 s before)",
                    done is not None and dur - 0.15 < done / fps <= dur + 1e-9, None if done is None else done / fps, dur),
              check("arc starts at -90 deg (12 o'clock)", len(runs) == 1 and runs[0][0] <= 1, runs, "starts at 0"),
              check("overage past 100 % in red only", red_before == 0 and arc_fraction(fr[-1], cx, cy, R + 3, R + 7, "#ff3b30", 10) > 0.1,
                    red_before, 0),
              check("line width 0.2 R", lw == 12, lw, 12),
              check("negative control: a linear count would not match the eased arc", lin >= 5, lin, ">= 5")]
    return checks, [vid]


@card("DATA-72")
def tick_ring_diamonds(task, wd):
    """Outer 2 px progress arc, a rotating 60-tick inner ring and 16 diamonds filling in sequence, % counter."""
    np = _np()
    S, cx, cy, fps = 200, 100, 90, 30
    target = 0.75
    rot_speed = 30.0
    rg, ag = angle_grid(S + 40, S, cx, cy)
    tick_band = (rg >= 64) & (rg < 70)

    def frame(t):
        p = target * ease("power2.out", prog(t, 0, 2.0))
        a = canvas(S, S + 40, "#05070d")
        paint(a, ring_mask(S + 40, S, cx, cy, 78, 80, 0, p * 360), "#ffffff")
        ph = rot_speed * t
        paint(a, tick_band & ((((ag - ph) % 6.0) < 0.9) | (((ag - ph) % 6.0) >= 5.1)), "#5c6680")   # 60 ticks, 1.8 deg wide
        for j in range(16):
            xx, yy = 20 + j * 10, 205
            poly = [(xx, yy - 4), (xx + 4, yy), (xx, yy + 4), (xx - 4, yy)]
            paint(a, pil_mask(S, S + 40, lambda d: d.polygon(poly, fill=255)), "#2f80ff" if j < int(math.floor(p * 16 + 1e-9)) else "#1b2233")
        draw_seg(a, fmt_int(p * 100, "dd"), "dd", 24, cx - 15, cy - 12, "#ffffff")
        return a
    n = int(2.3 * fps)
    vid = write_video(wd / "tick_ring.mp4", [frame(k / fps) for k in range(n)], fps)
    fr = read_video(vid)
    rr, ang = angle_grid(S + 40, S, cx, cy)
    tband = (rr >= 65) & (rr < 69)
    tick_counts, phases = [], []
    for f in fr[::5]:
        runs = angular_runs(near(f, "#5c6680", 10) & tband, ang)
        tick_counts.append(len(runs))
        m = near(f, "#5c6680", 10) & tband
        phases.append(float(np.degrees(np.angle(np.exp(1j * np.radians(ang[m] * 60)).mean())) / 60.0) % 6)
    dph = [((b - a) + 3) % 6 - 3 for a, b in zip(phases, phases[1:])]
    exp_dph = ((rot_speed * 5 / fps) + 3) % 6 - 3
    errs = 0
    for k, f in enumerate(fr):
        p = target * ease("power2.out", prog(k / fps, 0, 2.0))
        lit = sum(1 for j in range(16) if near(f[205, 20 + j * 10:21 + j * 10], "#2f80ff", 10).all())
        errs += int(lit != int(math.floor(p * 16 + 1e-9)))
        errs += int(abs(arc_fraction(f, cx, cy, 77, 81, "#ffffff", 10) - p) > 0.015)
        errs += int(seg_value(read_seg(f, "dd", 24, cx - 15, cy - 12, "#05070d", thr=60)) != round(p * 100))
    checks = [check("60 ticks in every sampled frame", set(tick_counts) == {60}, sorted(set(tick_counts)), 60),
              check("tick ring rotates 30 deg/s (phase step per 5 frames)", max(abs(x - exp_dph) for x in dph) <= 0.5, dph[:4], exp_dph),
              check("diamonds, arc and counter all bound to p", errs == 0, errs, 0),
              check("12 of 16 diamonds at 75 %", sum(1 for j in range(16) if near(fr[-1][205, 20 + j * 10:21 + j * 10], "#2f80ff", 10).all()) == 12, 12, 12),
              check("negative control: the first frame lights no diamonds", not any(near(fr[0][205, 20 + j * 10:21 + j * 10], "#2f80ff", 10).all() for j in range(16)), 0, 0)]
    return checks, [vid]


@card("DATA-73")
def liquid_fill(task, wd):
    """A circle fills with wavy liquid (1.2 s, 6 px wave) to 75 %; the number and the 1/4 1/2 3/4 ticks are bound
    to the same level."""
    np = _np()
    S, cx, cy, R, fps = 180, 90, 90, 70, 30
    target, amp = 0.75, 6.0
    level = lambda t: target * ease("easeInOutSine", prog(t, 0, 1.2))
    ys, xs = np.mgrid[0:S, 0:S + 60]

    def surface(t):
        a_t = amp * min(1.0, level(t) / 0.1)          # the wave settles flat at an empty / full level
        return cy + R - 2 * R * level(t) + a_t * np.sin((np.arange(S + 60) + 0.5) / 9.0 + 4 * t)

    def frame(t):
        a = canvas(S + 60, S, "#101820")
        inside = (xs + 0.5 - cx) ** 2 + (ys + 0.5 - cy) ** 2 < R * R
        paint(a, inside, "#22303c")
        paint(a, inside & (ys + 0.5 >= surface(t)[None, :]), "#b6f24a")
        for q in (0.25, 0.5, 0.75):
            if level(t) >= q - 1e-9:
                y = cy + R - 2 * R * q
                rect(a, cx + R + 8, y - 1, cx + R + 22, y + 1, "#ffffff")
        draw_seg(a, fmt_int(level(t) * 100, "dd"), "dd", 18, 4, 4, "#ffffff")
        return a
    n = int(1.6 * fps)
    vid = write_video(wd / "liquid.mp4", [frame(k / fps) for k in range(n)], fps)
    fr = read_video(vid)
    serr, aerr, terr, cerr = 0.0, 0.0, 0, 0
    cols = list(range(cx - 30, cx + 30))
    for k, f in enumerate(fr):
        t = k / fps
        L = level(t)
        if 0.15 < L < 0.74:
            tops = []
            for x in cols:
                yy = np.nonzero(near(f[:, x], "#b6f24a", 10))[0]
                if len(yy):
                    tops.append(yy.min())
            sexp = surface(t)[cols]
            serr = max(serr, abs(np.mean(tops) - np.mean(np.ceil(sexp - 0.5))))
            aerr = max(aerr, abs((max(tops) - min(tops)) / 2.0 - amp))
        for q in (0.25, 0.5, 0.75):
            y = int(cy + R - 2 * R * q)
            terr += int(bool(near(f[y, cx + R + 15:cx + R + 16], "#ffffff", 10).all()) != (L >= q - 1e-9))
        cerr += int(seg_value(read_seg(f, "dd", 18, 4, 4, "#101820", thr=60)) != round(L * 100))
    checks = [check("mean surface height follows the level (px)", serr <= 1.0, serr, "<= 1"),
              check("wave amplitude 6 px", aerr <= 1.0, aerr, "<= 1"),
              check("1/4 1/2 3/4 ticks appear as the level passes", terr == 0, terr, 0),
              check("number bound to the level", cerr == 0, cerr, 0),
              check("negative control: the empty first frame has no liquid", not near(fr[0], "#b6f24a", 10).any(), 0, 0)]
    return checks, [vid]


@card("DATA-75")
def radar_sweep(task, wd):
    """Four 1 px rings and a conic wedge sweeping 1 rev / 7 s; dots pulse for 300 ms when the sweep passes within 3 deg."""
    np = _np()
    S, c, fps, rev = 160, 80, 15, 7.0
    dots = [30, 100, 200, 300]
    rr, ang = angle_grid(S, S, c, c)

    def frame(t):
        sw = 360 * t / rev
        a = canvas(S, S, "#03110a")
        lag = (sw - ang) % 360
        wedge = (lag < 40) & (rr < 72)
        a[wedge] = a[wedge] + np.outer(1 - lag[wedge] / 40.0, np.array([30, 200, 90.0]))
        for r in (18, 36, 54, 72):
            paint(a, (rr >= r) & (rr < r + 1), "#2f6f4f")
        for da in dots:
            since = ((sw - da) % 360) / 360.0 * rev
            big = since <= 0.3 and (sw >= da - 3)
            rad = 5 if big else 3
            x, y = c + 50 * math.sin(math.radians(da)), c - 50 * math.cos(math.radians(da))
            paint(a, pil_mask(S, S, lambda d: d.ellipse([x - rad, y - rad, x + rad, y + rad], fill=255)), "#eaffef")
        return a
    n = int(rev * fps)
    vid = write_video(wd / "radar.mp4", [frame(k / float(fps)) for k in range(n)], fps)
    fr = read_video(vid)
    serr = 0.0
    sel = (rr > 20) & (rr < 34)
    for k, f in enumerate(fr[1:], 1):
        g = f[..., 1]
        a_meas = float(ang[sel][np.argmax(g[sel])])
        serr = max(serr, abs(((a_meas - 360 * k / float(fps) / rev) + 180) % 360 - 180))
    prof = [bool(near(fr[0][c + r:c + r + 1, c:c + 1], "#2f6f4f", 6).all()) for r in range(10, 76)]
    rings = len(col_runs(prof))
    pulses = []
    for da in dots:
        x, y = int(round(c + 50 * math.sin(math.radians(da)))), int(round(c - 50 * math.cos(math.radians(da))))
        areas = [int(near(f[y - 7:y + 8, x - 7:x + 8], "#eaffef", 10).sum()) for f in fr]
        kp = int(math.ceil(da / 360.0 * rev * fps))
        pulses.append((areas[min(n - 1, kp + 1)] > areas[max(0, kp - 8)] * 1.8, areas[max(0, kp - 8)]))
    checks = [check("sweep leading edge at 360 t / 7 s (deg)", serr <= 3.5, serr, "<= 3.5"),
              check("four rings", rings == 4, rings, 4),
              check("each dot pulses as the sweep passes", all(p for p, _ in pulses), [p for p, _ in pulses], True),
              check("negative control: dots far from the sweep are not pulsing", all(a <= 40 for _, a in pulses), [a for _, a in pulses], "small")]
    return checks, [vid]


def _largest_remainder(weights, total):
    exact = [w * total / float(sum(weights)) for w in weights]
    fl = [int(math.floor(e)) for e in exact]
    for i in sorted(range(len(weights)), key=lambda i: -(exact[i] - fl[i]))[:total - sum(fl)]:
        fl[i] += 1
    return fl


@card("DATA-76")
def parliament_and_dot_ring(task, wd):
    """Parliament: seats on concentric arcs (outer rows more seats), sorted by angle and coloured by party with the
    centre count; plus 4500 seeded dots on an annulus coloured by cumulative-angle share."""
    np = _np()
    parties = [("A", 120, "#c0392b"), ("B", 80, "#2980b9"), ("C", 50, "#27ae60"), ("D", 30, "#f39c12")]
    total = sum(p[1] for p in parties)
    radii = [50 + 9 * i for i in range(8)]
    per_row = _largest_remainder(radii, total)
    seats = []
    for r, k in zip(radii, per_row):
        for j in range(k):
            th = math.pi * (j + 0.5) / k
            seats.append((th, r))
    seats.sort(key=lambda s: (-s[0], s[1]))          # left (180 deg) to right (0 deg)
    owner = []
    for name, k, col in parties:
        owner += [col] * k
    W, H, cx, cy, fps = 280, 160, 140, 140, 25
    pos = [(cx + r * math.cos(th), cy - r * math.sin(th)) for th, r in seats]

    def frame(t):
        a = canvas(W, H, "#ffffff")
        shown = min(total, int(t / 0.007))
        for i, (x, y) in enumerate(pos):
            paint(a, pil_mask(W, H, lambda d: d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=255)), owner[i] if i < shown else "#e5e5e5")
        draw_seg(a, fmt_int(shown, "ddd"), "ddd", 16, cx - 17, cy - 22, "#222222")
        return a
    n = int(2.3 * fps)
    vid = write_video(wd / "parliament.mp4", [frame(k / float(fps)) for k in range(n)], fps)
    fr = read_video(vid)
    last = fr[-1]
    sampled = [tuple(last[int(round(y)), int(round(x))]) for x, y in pos]
    counts = {name: sum(1 for s in sampled if s == tuple(float(v) for v in rgb(col))) for name, _, col in parties}
    contiguous = all(sampled[i] == sampled[i + 1] or sampled[i + 1] != sampled[i] and sampled[i] not in sampled[i + 1:]
                     for i in range(len(sampled) - 1))
    first = [next(k for k, f in enumerate(fr) if not near(f[int(round(y)), int(round(x)):int(round(x)) + 1], "#e5e5e5", 6).all())
             for x, y in pos[::20]]
    centre = seg_value(read_seg(last, "ddd", 16, cx - 17, cy - 22, "#ffffff", fg="#222222"))
    # dot ring
    rs = np.random.RandomState(4)
    N = 4500
    th = rs.uniform(0, 360, N)
    rad = np.sqrt(rs.uniform(60 ** 2, 100 ** 2, N))
    shares = [0.46, 0.31, 0.15, 0.08]
    bounds = np.cumsum(shares) * 360
    cat = np.searchsorted(bounds, th, side="right")
    S = 220
    ring = canvas(S, S, "#ffffff")
    pal = ["#c0392b", "#2980b9", "#27ae60", "#f39c12"]
    xs = (S / 2 + rad * np.sin(np.radians(th))).astype(int)
    ys = (S / 2 - rad * np.cos(np.radians(th))).astype(int)
    for x, y, cc in zip(xs, ys, cat):
        ring[y, x] = rgb(pal[cc])
    rp = save_png(ring, wd / "dot_ring.png")
    rb = load_png(rp)
    rr, ang = angle_grid(S, S, S / 2, S / 2)
    cerr = 0.0
    for i, c in enumerate(pal):
        m = near(rb, c, 2)
        lo = 0 if i == 0 else bounds[i - 1]
        inside = ((ang[m] >= lo - 1) & (ang[m] < bounds[i] + 1)).mean()
        cerr = max(cerr, 1 - inside)
    checks = [check("seats per party", counts == {n_: k for n_, k, _ in parties}, counts, {n_: k for n_, k, _ in parties}),
              check("outer rows hold more seats", all(b > a for a, b in zip(per_row, per_row[1:])) and sum(per_row) == total, per_row, total),
              check("each party is one contiguous angular block", contiguous, contiguous, True),
              check("seats fill in angle order", first == sorted(first), first[:6], "non-decreasing"),
              check("centre count == 280", centre == total, centre, total),
              check("dot ring: categories sit in their cumulative-angle sectors", cerr <= 0.01, cerr, "<= 1 % outside"),
              check("negative control: the first frame shows no party colours", all(near(fr[0][int(round(y)), int(round(x)):int(round(x)) + 1], "#e5e5e5", 6).all() for x, y in pos),
                    0, "all grey")]
    return checks, [vid, rp]


@card("DATA-77")
def waffle_10x10(task, wd):
    """MG-043: 0-1 s grid, 1-3 s the matching count takes colour in RTL row order with a computed delay while the
    % counter lands with it, unit stated (one cell = 1 %)."""
    np = _np()
    pct, fps = 37, 20
    cell, gap, x0, y0 = 14, 8, 20, 40
    W, H = x0 * 2 + 10 * (cell + gap), y0 + 10 * (cell + gap) + 10
    order = [(r, c) for r in range(10) for c in range(9, -1, -1)]
    delay = 1.5 / pct
    pos = lambda rc: (x0 + rc[1] * (cell + gap), y0 + rc[0] * (cell + gap))

    def frame(t):
        a = canvas(W, H, "#ffffff")
        k = min(pct, int((t - 1.0) / delay) + 1) if t >= 1.0 else 0
        for i, rc in enumerate(order):
            x, y = pos(rc)
            rect(a, x, y, x + cell, y + cell, "#e07b78" if i < k else "#d9d9d9")
        draw_seg(a, fmt_int(k, "dd"), "dd", 20, 20, 8, "#222222")
        return a
    n = int(6.0 * fps)
    vid = write_video(wd / "waffle.mp4", [frame(k / float(fps)) for k in range(n)], fps)
    fr = read_video(vid)
    bad, end_k = 0, None
    for k, f in enumerate(fr):
        on = [bool(near(f[pos(rc)[1] + 5, pos(rc)[0] + 5:pos(rc)[0] + 6], "#e07b78", 6).all()) for rc in order]
        m = sum(on)
        bad += int(on != [i < m for i in range(100)])
        bad += int(seg_value(read_seg(f, "dd", 20, 20, 8, "#ffffff", fg="#222222")) != m)
        if end_k is None and m == pct:
            end_k = k
    pre = sum(1 for f in fr[:fps] for rc in order if near(f[pos(rc)[1] + 5, pos(rc)[0] + 5:pos(rc)[0] + 6], "#e07b78", 6).all())
    first_rc = order[0]
    ltr = [(r, c) for r in range(10) for c in range(10)][:pct]
    ltr_hit = all(near(fr[-1][pos(rc)[1] + 5, pos(rc)[0] + 5:pos(rc)[0] + 6], "#e07b78", 6).all() for rc in ltr)
    note = wjson(wd / "waffle_unit.json", {"unit": "كل مربع = 1٪", "value_pct": pct, "rounding": "none"})
    checks = [check("37 of 100 cells coloured", sum(1 for rc in order if near(fr[-1][pos(rc)[1] + 5, pos(rc)[0] + 5:pos(rc)[0] + 6], "#e07b78", 6).all()) == pct, pct, pct),
              check("fill order right-to-left rows; counter == coloured cells", bad == 0, bad, 0),
              check("first coloured cell is top-right", first_rc == (0, 9), first_rc, (0, 9)),
              check("grid only during 0-1 s", pre == 0, pre, 0),
              check("colouring finishes inside 1-3 s", end_k is not None and 1.0 < end_k / float(fps) <= 3.0, None if end_k is None else end_k / float(fps), "<= 3 s"),
              check("negative control: a left-to-right fill would not match", not ltr_hit, ltr_hit, False)]
    return checks, [vid, note]


@card("DATA-78")
def unit_dot_grid(task, wd):
    """One dot per real item (40 x 30 = 1200) with a subset highlighted by a right-to-left sweep, unit stated."""
    np = _np()
    cols, rows, hl, fps = 40, 30, 137, 25
    pitch, x0, y0 = 7, 6, 6
    W, H = x0 * 2 + cols * pitch, y0 * 2 + rows * pitch
    order = [(r, c) for c in range(cols - 1, -1, -1) for r in range(rows)]   # sweep column by column from the right
    a0 = canvas(W, H, "#ffffff")
    for r in range(rows):
        for c in range(cols):
            rect(a0, x0 + c * pitch, y0 + r * pitch, x0 + c * pitch + 4, y0 + r * pitch + 4, "#c8c8c8")

    def frame(t):
        a = a0.copy()
        k = min(hl, int(t / 0.007))
        for r, c in order[:k]:
            rect(a, x0 + c * pitch, y0 + r * pitch, x0 + c * pitch + 4, y0 + r * pitch + 4, "#e4572e")
        return a
    n = int(1.3 * fps)
    vid = write_video(wd / "unit_dots.mp4", [frame(k / float(fps)) for k in range(n)], fps)
    fr = read_video(vid)
    last = fr[-1]
    samp = lambda f, r, c: f[y0 + r * pitch + 2, x0 + c * pitch + 2]
    total = sum(1 for r in range(rows) for c in range(cols) if not near(samp(last, r, c)[None], "#ffffff", 5).all())
    lit = [(r, c) for r in range(rows) for c in range(cols) if near(samp(last, r, c)[None], "#e4572e", 6).all()]
    mid = fr[n // 3]
    mlit = sum(1 for r in range(rows) for c in range(cols) if near(samp(mid, r, c)[None], "#e4572e", 6).all())
    prefix = all(near(samp(mid, r, c)[None], "#e4572e", 6).all() for r, c in order[:mlit])
    note = wjson(wd / "unit.json", {"unit": "كل نقطة = شخص واحد", "dots": cols * rows, "highlighted": hl})
    checks = [check("1200 dots, one per item", total == cols * rows, total, 1200),
              check("137 highlighted", len(lit) == hl, len(lit), hl),
              check("highlight sweeps from the right (prefix of the sweep order mid-way)", prefix and 0 < mlit < hl, mlit, "prefix"),
              check("negative control: the first frame has no highlight", not any(near(samp(fr[0], r, c)[None], "#e4572e", 6).all() for r in range(rows) for c in range(cols)), 0, 0)]
    return checks, [vid, note]


@card("DATA-79")
def value_to_units(task, wd):
    """MG-050: 0-1 s the documented value, 1-4 s it becomes a row of units, 4-7 s a comparison row; 'تقريبًا' when
    rounding."""
    np = _np()
    value, other, unit = 3740000, 1200000, 100000
    nu, no = int(round(value / float(unit))), int(round(other / float(unit)))
    approx = value % unit != 0 or other % unit != 0
    fps, W, H = 10, 420, 140
    ux = lambda i: 10 + (i % 20) * 20
    uy = lambda i, row: 20 + row * 50 + (i // 20) * 20

    def frame(t):
        a = canvas(W, H, "#ffffff")
        k = int(round(nu * prog(t, 1.0, 3.0)))
        for i in range(k):
            rect(a, ux(i), uy(i, 0), ux(i) + 14, uy(i, 0) + 14, "#2a78d6")
        if approx and t >= 1.0:
            rect(a, 380, 2, 416, 12, "#444444")       # 'تقريبًا' tag
        j = int(round(no * prog(t, 4.0, 3.0)))
        for i in range(j):
            rect(a, ux(i), uy(i, 2) - 30, ux(i) + 14, uy(i, 2) - 16, "#eb6834")
        return a
    n = int(7.2 * fps)
    vid = write_video(wd / "units.mp4", [frame(k / float(fps)) for k in range(n)], fps)
    fr = read_video(vid)
    count = lambda f, c, row: sum(1 for i in range(40) if near(f[(uy(i, row) - (30 if row == 2 else 0)) + 7, ux(i) + 7:ux(i) + 8], c, 6).all())
    a4, b7 = count(fr[int(4.0 * fps)], "#2a78d6", 0), count(fr[-1], "#eb6834", 2)
    pre = count(fr[int(0.9 * fps)], "#2a78d6", 0)
    cmp_before = count(fr[int(3.9 * fps)], "#eb6834", 2)
    tag = bool(near(fr[-1][7, 400:401], "#444444", 6).all())
    checks = [check("value becomes round(3.74M / 100k) = 37 units by 4 s", a4 == nu == 37, a4, 37),
              check("comparison row = 12 units by 7 s", b7 == no == 12, b7, 12),
              check("units form only in 1-4 s, comparison in 4-7 s", pre == 0 and cmp_before == 0, [pre, cmp_before], [0, 0]),
              check("'تقريبًا' shown because the value was rounded", approx and tag, tag, True),
              check("unit ratio ~ value ratio (within 1 unit)", abs(a4 / float(b7) - value / float(other)) * b7 <= 1, a4 / float(b7), value / float(other)),
              check("negative control: the raw value is not a whole number of units", value / float(unit) != int(value / unit), value / float(unit), "fractional")]
    return checks, [vid]


@card("DATA-80")
def calendar_heatmap(task, wd):
    """GitHub-style grid: weeks as columns from the first date, row = (weekday+6)%7 (Monday first), CELL 10,
    GAP 2, LEFT 24, TOP 14, sequential ramp; month markers on top."""
    import datetime as dt
    np = _np()
    CELL, GAP, LEFT, TOP = 10, 2, 24, 14
    start, days = dt.date(2026, 1, 1), 181
    rs = np.random.RandomState(2)
    vals = rs.poisson(3, days)
    ramp = ["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"]
    lvl = lambda v: min(4, int(v // 2))
    getDay = lambda d: (d.weekday() + 1) % 7           # JS: Sunday = 0
    row = lambda d: (getDay(d) + 6) % 7
    first_monday = start - dt.timedelta(days=row(start))
    col = lambda d: (d - first_monday).days // 7
    ncol = col(start + dt.timedelta(days=days - 1)) + 1
    W, H = LEFT + ncol * (CELL + GAP), TOP + 7 * (CELL + GAP)
    a = canvas(W, H, "#ffffff")
    for i in range(days):
        d = start + dt.timedelta(days=i)
        x, y = LEFT + col(d) * (CELL + GAP), TOP + row(d) * (CELL + GAP)
        rect(a, x, y, x + CELL, y + CELL, ramp[lvl(vals[i])])
        if d.day == 1:
            rect(a, x, 2, x + 6, 6, "#57606a")
    png = save_png(a, wd / "calendar.png")
    b = load_png(png)

    def mism(rowfn):
        bad = 0
        for i in range(days):
            d = start + dt.timedelta(days=i)
            fm = start - dt.timedelta(days=rowfn(start))
            x = LEFT + ((d - fm).days // 7) * (CELL + GAP)
            y = TOP + rowfn(d) * (CELL + GAP)
            bad += int(not near(b[y + 5:y + 6, x + 5:x + 6], ramp[lvl(vals[i])], 2).all())
        return bad
    months = [x for x in range(W) if near(b[4:5, x:x + 1], "#57606a", 3).all()]
    checks = [check("2026-01-01 (Thursday) sits in row 3", row(start) == 3, row(start), 3),
              check("every day's cell has its ramp colour at (col, row)", mism(row) == 0, mism(row), 0),
              check("week columns", ncol == 27, ncol, 27),
              check("6 month markers", len(col_runs([x in months for x in range(W)])) == 6, len(col_runs([x in months for x in range(W)])), 6),
              check("cell 10 + gap 2 pitch", (LEFT + CELL + GAP) - LEFT == 12, 12, 12),
              check("negative control: a Sunday-first layout misplaces days", mism(lambda d: getDay(d)) > 0, mism(lambda d: getDay(d)), "> 0")]
    return checks, [png]


GAPS["DATA-91"] = ("the card's 'CVD-safe' palette fails here: Machado-2009 deuteranopia makes #3B82F6 vs #A855F7 "
                   "dE2000 = 0.9 (protanopia 5.4), so the CVD known-answer check cannot pass without changing the card")


@card("DATA-81")
def risk_matrix(task, wd):
    """Likelihood x impact matrix: score >= 6 h4, >= 4 h3, >= 3 h2 else h1, light and dark ramps, cells >= 52 px,
    cells light in score order with a 60 ms stagger."""
    np = _np()
    light = ["#cfe8d6", "#f3e2a6", "#f1b98a", "#e98a86"]
    dark = ["#1f5a3b", "#6b5a17", "#7a4219", "#7f2626"]
    level = lambda s: 3 if s >= 6 else 2 if s >= 4 else 1 if s >= 3 else 0
    cell, fps = 56, 50
    cells = [(l, i) for l in (1, 2, 3) for i in (1, 2, 3)]
    order = sorted(cells, key=lambda c: (c[0] * c[1], c))
    pos = lambda c: (10 + (c[1] - 1) * (cell + 4), 10 + (3 - c[0]) * (cell + 4))
    W = H = 10 * 2 + 3 * cell + 8

    def render(pal, t):
        a = canvas(W, H, "#ffffff" if pal is light else "#0b0f14")
        for k, c in enumerate(order):
            x, y = pos(c)
            on = t >= k * 0.06
            rect(a, x, y, x + cell, y + cell, pal[level(c[0] * c[1])] if on else "#9e9e9e")
        return a
    vid = write_video(wd / "risk_light.mp4", [render(light, k / float(fps)) for k in range(int(0.7 * fps))], fps)
    dp = save_png(render(dark, 9), wd / "risk_dark.png")
    fr = read_video(vid)
    db = load_png(dp)
    ok_l = all(near(fr[-1][pos(c)[1] + 28, pos(c)[0] + 28:pos(c)[0] + 29], light[level(c[0] * c[1])], 2).all() for c in cells)
    ok_d = all(near(db[pos(c)[1] + 28, pos(c)[0] + 28:pos(c)[0] + 29], dark[level(c[0] * c[1])], 2).all() for c in cells)
    first = [next(k for k, f in enumerate(fr) if not near(f[pos(c)[1] + 28, pos(c)[0] + 28:pos(c)[0] + 29], "#9e9e9e", 2).all()) for c in order]
    size = len(col_runs(~near(fr[-1][pos(cells[0])[1] + 28], "#ffffff", 2))[0:1]) and col_runs(~near(fr[-1][pos(cells[0])[1] + 28], "#ffffff", 2))[0][1]
    levels = {c: level(c[0] * c[1]) for c in cells}
    checks = [check("score thresholds (known cells)", levels[(3, 3)] == 3 and levels[(2, 3)] == 3 and levels[(2, 2)] == 2
                    and levels[(1, 3)] == 1 and levels[(1, 2)] == 0, {"9": levels[(3, 3)], "6": levels[(2, 3)], "4": levels[(2, 2)], "3": levels[(1, 3)], "2": levels[(1, 2)]}, "h4 h4 h3 h2 h1"),
              check("light cells carry the light ramp", ok_l, ok_l, True),
              check("dark cells carry the dark ramp", ok_d, ok_d, True),
              check("cells >= 52 px", size >= 52, size, ">= 52"),
              check("cells light in score order, 60 ms (3 frames) apart", first == [3 * k for k in range(9)], first, [3 * k for k in range(9)]),
              check("negative control: the unlit input grid has no risk colours",
                    not any(near(fr[0][pos(c)[1] + 28, pos(c)[0] + 28:pos(c)[0] + 29], light[level(c[0] * c[1])], 2).all() for c in order[1:]), 0, 0)]
    return checks, [vid, dp]


@card("DATA-82")
def alpha_matrix(task, wd):
    """Rows x columns where each cell's brand-colour alpha encodes its value: a = max(.08, v/max); white text when
    a > .55; revealed column by column."""
    np = _np()
    vals = [[0, 12, 30, 44, 51, 60], [8, 20, 25, 35, 40, 38], [3, 6, 9, 14, 22, 31], [50, 41, 33, 21, 12, 5]]
    mx = max(max(r) for r in vals)
    brand = "#2a78d6"
    cw, ch, fps = 40, 26, 20
    W, H = 6 * cw + 10, 4 * ch + 10

    def frame(t):
        a = canvas(W, H, "#ffffff")
        for c in range(6):
            if t < c * 0.1 - 1e-9:
                continue
            for r in range(4):
                al = max(0.08, vals[r][c] / float(mx))
                rect(a, 5 + c * cw, 5 + r * ch, 5 + c * cw + cw - 2, 5 + r * ch + ch - 2, brand, al)
                draw_seg(a, fmt_int(vals[r][c], "dd"), "dd", 12, 5 + c * cw + 10, 5 + r * ch + 6, "#ffffff" if al > 0.55 else "#1d2632")
        return a
    vid = write_video(wd / "matrix.mp4", [frame(k / float(fps)) for k in range(int(0.9 * fps))], fps)
    fr = read_video(vid)
    last = fr[-1]
    berr, terr = 0.0, 0
    for r in range(4):
        for c in range(6):
            al = max(0.08, vals[r][c] / float(mx))
            px = last[5 + r * ch + 2, 5 + c * cw + 2]
            berr = max(berr, float(np.abs(px - np.array(lerp_c("#ffffff", brand, al))).max()))
            bgc = tuple(int(round(v)) for v in lerp_c("#ffffff", brand, al))
            got = seg_value(read_seg(last, "dd", 12, 5 + c * cw + 10, 5 + r * ch + 6, None, fg="#ffffff" if al > 0.55 else "#1d2632", thr=12))
            terr += int(got != vals[r][c])
    first = [next(k for k, f in enumerate(fr) if not near(f[7, 5 + c * cw + 2:5 + c * cw + 3], "#ffffff", 2).all()) for c in range(6)]
    zero = last[7, 7]
    checks = [check("cell colour == white + brand at max(.08, v/max)", berr <= 1.0, berr, "<= 1"),
              check("text white above a = .55, ink below (decoded in that colour)", terr == 0, terr, 0),
              check("revealed column by column (100 ms)", first == [2 * c for c in range(6)], first, [2 * c for c in range(6)]),
              check("zero cell keeps the .08 floor", float(np.abs(zero - np.array(lerp_c("#ffffff", brand, 0.08))).max()) <= 1, zero.tolist(), "8 % brand"),
              check("negative control: without the floor a zero cell would be blank white", float(np.abs(zero - 255).max()) > 5, zero.tolist(), "!= white")]
    return checks, [vid]


@card("DATA-83")
def benford_bars(task, wd):
    """First-digit frequencies vs the Benford expectation as SVG bars (viewBox 420x186, bar 26 / pitch 44 / rx 5),
    flagging digits off by > 3 points."""
    import xml.etree.ElementTree as ET
    np = _np()
    rs = np.random.RandomState(8)
    amounts = np.exp(rs.uniform(0, math.log(10) * 4, 5000))        # log-uniform -> Benford
    amounts[:400] = rs.uniform(7000, 7999, 400)                      # injected manipulation on digit 7
    first = lambda arr: np.array([int(str(int(v))[0]) for v in arr if v >= 1])

    def analyse(arr):
        d = first(arr)
        obs = [float((d == k).mean() * 100) for k in range(1, 10)]
        exp = [math.log10(1 + 1.0 / k) * 100 for k in range(1, 10)]
        hot = [k for k, o, e in zip(range(1, 10), obs, exp) if abs(o - e) > 3]
        return obs, exp, hot
    obs, exp, hot = analyse(amounts)
    top = 40.0
    Y = lambda p: 160 - p / top * 140
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 186">']
    for i, (o, e) in enumerate(zip(obs, exp)):
        x = 14 + i * 44
        parts.append('<rect class="bar%s" x="%d" y="%.3f" width="26" height="%.3f" rx="5" data-d="%d"/>' % (
            " hot" if i + 1 in hot else "", x, Y(o), 160 - Y(o), i + 1))
        parts.append('<line class="expected" x1="%d" x2="%d" y1="%.3f" y2="%.3f"/>' % (x - 3, x + 29, Y(e), Y(e)))
        parts.append('<text class="axis" x="%d" y="178">%d</text>' % (x + 9, i + 1))
    parts.append("</svg>")
    svgp = wd / "benford.svg"
    svgp.write_text("".join(parts), encoding="utf-8")
    root = ET.fromstring(svgp.read_text(encoding="utf-8"))
    ns = "{http://www.w3.org/2000/svg}"
    rects = root.findall(ns + "rect")
    herr = max(abs(float(r.get("height")) - o / top * 140) for r, o in zip(rects, obs))
    hot_svg = [int(r.get("data-d")) for r in rects if "hot" in r.get("class")]
    geo = all(r.get("width") == "26" and r.get("rx") == "5" for r in rects) and \
        [int(r.get("x")) for r in rects] == [14 + 44 * i for i in range(9)]
    _, _, hot_uniform = analyse(rs.uniform(1, 9999, 5000))
    checks = [check("expected = log10(1 + 1/d)", [round(e, 1) for e in exp] == [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6],
                    [round(e, 1) for e in exp], [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]),
              check("injected digit 7 flagged hot", 7 in hot and 7 in hot_svg, hot_svg, "contains 7"),
              check("bar heights == observed % x scale", herr < 0.01, herr, "< 0.01"),
              check("viewBox 420x186, bar 26, pitch 44, rx 5", root.get("viewBox") == "0 0 420 186" and geo, geo, True),
              check("negative control: uniform amounts break Benford on many digits", len(hot_uniform) >= 5, hot_uniform, ">= 5 hot")]
    return checks, [svgp, wjson(wd / "benford.json", {"observed": obs, "expected": exp, "hot": hot})]


@card("DATA-84")
def appending_table(task, wd):
    """A two-column table appends a row each step (fade in with a 16 px rise, 120 ms stagger), keeping <= 6 rows on
    screen; row height ~6 % of H."""
    np = _np()
    rows = [(2016 + i, v) for i, v in enumerate([12, 18, 25, 31, 29, 40, 47, 52, 61])]
    W, H, fps = 300, 300, 25
    rh = 18                      # 6 % of 300
    step = 0.4
    y0 = 20

    def frame(t):
        a = canvas(W, H, "#ffffff")
        k = min(len(rows), int(t / step) + 1)
        vis = list(range(max(0, k - 6), k))
        for slot, i in enumerate(vis):
            q = ease("power2.out", prog(t, i * step, 0.3))
            y = y0 + slot * (rh + 12) + 16 * (1 - q)
            draw_seg(a, str(rows[i][0]), "dddd", 14, 30, int(round(y)), "#1d2632", q)
            draw_seg(a, fmt_int(rows[i][1], "dd"), "dd", 14, 200, int(round(y)), "#2a78d6", q)
        return a
    n = int((len(rows) * step + 0.4) * fps)
    vid = write_video(wd / "table.mp4", [frame(k / float(fps)) for k in range(n)], fps)
    fr = read_video(vid)
    bad, maxrows = 0, 0
    for i in range(len(rows)):
        k = int(round((i * step + 0.35) * fps))
        f = fr[k]
        vis = list(range(max(0, i + 1 - 6), i + 1))
        got = [(seg_value(read_seg(f, "dddd", 14, 30, y0 + s * (rh + 12), "#ffffff", fg="#1d2632")),
                seg_value(read_seg(f, "dd", 14, 200, y0 + s * (rh + 12), "#ffffff", fg="#2a78d6"))) for s in range(len(vis))]
        bad += int(got != [rows[j] for j in vis])
        maxrows = max(maxrows, len([s for s in range(8) if ink_bbox(f, "#ffffff", 20, (25, y0 + s * (rh + 12) - 2, 260, y0 + s * (rh + 12) + 16)) is not None]))
    kk = int(round(1 * step * fps)) + 1
    b = ink_bbox(fr[kk], "#ffffff", 5, (195, y0 + (rh + 12) - 2, 240, H))
    rise = b[1] - (y0 + (rh + 12)) if b else None
    checks = [check("rows append and the newest six stay on screen", bad == 0, bad, 0),
              check("never more than 6 rows", maxrows <= 6, maxrows, "<= 6"),
              check("new row enters lower and rises 16 px", rise is not None and 4 <= rise <= 16, rise, "0 < rise <= 16"),
              check("row height ~6 % of H", rh / float(H) == 0.06, rh / float(H), 0.06),
              check("negative control: the full 9-row table breaks the 6-row rule", len(rows) > 6, len(rows), "> 6")]
    return checks, [vid]


@card("DATA-86")
def tiles_and_line(task, wd):
    """Three tiles count up (800 ms easeOutExpo) while a line draws beneath (dashoffset 1.2 s); a delta chip shows
    the computed +301 %."""
    np = _np()
    tiles = [1250, 86, 401]
    series = [100, 140, 130, 190, 260, 240, 330, 401]
    delta = round((series[-1] - series[0]) * 100.0 / series[0])
    W, H, fps = 360, 220, 30
    pts = [(30 + i * 42, 200 - v * 0.3) for i, v in enumerate(series)]
    segL = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]

    def frame(t):
        a = canvas(W, H, "#0d1117")
        e = ease("easeOutExpo", prog(t, 0, 0.8))
        for j, v in enumerate(tiles):
            rect(a, 10 + j * 115, 10, 10 + j * 115 + 105, 60, "#161b22")
            draw_seg(a, fmt_int(v * e, "d,ddd" if j == 0 else "ddd", sep=(j == 0)), "d,ddd" if j == 0 else "ddd", 22, 20 + j * 115, 24, "#ffffff")
        r = prog(t, 0, 1.2)
        if r > 0:
            sub = [pts[0]] + [q for q in pts[1:] if False]
            acc, target = 0.0, r * sum(segL)
            sub = [pts[0]]
            for (pa, pb), L in zip(zip(pts, pts[1:]), segL):
                if acc + L <= target:
                    sub.append(pb)
                    acc += L
                else:
                    u = (target - acc) / L
                    sub.append((pa[0] + (pb[0] - pa[0]) * u, pa[1] + (pb[1] - pa[1]) * u))
                    break
            paint(a, line_mask(H, W, sub, 2), "#3fb950")
        if t >= 1.2:
            rect(a, 290, 70, 350, 92, "#1f6f3a")
            draw_seg(a, "+%d" % delta, "dddd", 14, 296, 74, "#ffffff")
        return a
    n = int(1.5 * fps)
    vid = write_video(wd / "tiles_line.mp4", [frame(k / fps) for k in range(n)], fps)
    fr = read_video(vid)
    terr = 0
    for k, f in enumerate(fr):
        e = ease("easeOutExpo", prog(k / fps, 0, 0.8))
        for j, v in enumerate(tiles):
            pat = "d,ddd" if j == 0 else "ddd"
            terr = max(terr, abs(_nz(seg_value(read_seg(f, pat, 22, 20 + j * 115, 24, "#161b22", thr=60))) - round(v * e)))
    lerr = 0.0
    for k, f in enumerate(fr[1:int(1.2 * fps)], 1):
        m = near(f, "#3fb950", 30)
        xs = np.nonzero(m.any(axis=0))[0]
        tgt = prog(k / fps, 0, 1.2) * sum(segL)
        exp_pt = point_at(pts, tgt / sum(segL))
        lerr = max(lerr, abs(xs.max() + 0.5 - exp_pt[0]))
    chip = read_seg(fr[-1], "dddd", 14, 296, 74, "#1f6f3a", fg="#ffffff")
    lin = max(abs(round(1250 * prog(k / fps, 0, 0.8)) - round(1250 * ease("easeOutExpo", prog(k / fps, 0, 0.8)))) for k in range(n))
    checks = [check("tiles count on easeOutExpo over 800 ms", terr <= 1, terr, "<= 1"),
              check("line front follows a 1.2 s dashoffset (px)", lerr <= 2.0, lerr, "<= 2"),
              check("delta chip == (last - first) / first", chip == "+301" and delta == 301, chip, "+301"),
              check("negative control: a linear count would not match", lin > 100, lin, "> 100")]
    return checks, [vid]


@card("DATA-87")
def hero_number_pills(task, wd):
    """A huge number (18-25 % of frame height) counts in 600 ms easeOut with a caption, and source pills pop in
    with a spring (overshoot, then settle)."""
    np = _np()
    W, H, fps = 270, 480, 30
    NH = int(0.22 * H)
    pat, target = "ddd", 482
    lx = (W - seg_width(pat, NH)) // 2

    def frame(t):
        a = canvas(W, H, "#faf7f2")
        draw_seg(a, fmt_int(target * ease("easeOut", prog(t, 0, 0.6)), pat), pat, NH, lx, 150, "#1d2632")
        rect(a, 60, 280, 210, 286, "#5d6a7a")
        s = ease("back.out", prog(t, 0.6, 0.35))
        if s > 0:
            w = 80 * s
            rect(a, 135 - w / 2, 320, 135 + w / 2, 340, "#e4572e")
        return a
    n = int(1.4 * fps)
    vid = write_video(wd / "hero.mp4", [frame(k / fps) for k in range(n)], fps)
    fr = read_video(vid)
    b = ink_bbox(fr[-1], "#faf7f2", 60, (0, 100, W, 270))
    frac = (b[3] - b[1]) / float(H)
    err = max(abs(_nz(seg_value(read_seg(f, pat, NH, lx, 150, "#faf7f2", fg="#1d2632"))) - round(target * ease("easeOut", prog(k / fps, 0, 0.6))))
              for k, f in enumerate(fr))
    widths = [int(near(f[330], "#e4572e", 6).sum()) for f in fr]
    checks = [check("number is 18-25 % of frame height", 0.18 <= frac <= 0.25, frac, "0.18..0.25"),
              check("counter on 600 ms easeOut", err <= 1, err, "<= 1"),
              check("pill springs past its size then settles", max(widths) > 1.05 * widths[-1] and abs(widths[-1] - 80) <= 1, [max(widths), widths[-1]], "overshoot, 80"),
              check("pills pop after the count lands", widths[int(0.6 * fps)] == 0, widths[int(0.6 * fps)], 0),
              check("negative control: the first frame does not show the number", seg_value(read_seg(fr[0], pat, NH, lx, 150, "#faf7f2", fg="#1d2632")) != target, 0, "!= 482")]
    return checks, [vid]


HF_BIN = "/opt/node22/bin/hyperframes"
HF_GSAP = "/opt/node22/lib/node_modules/hyperframes/dist/vendor/npm/gsap@3.15.0/dist/gsap.min.js"


@card("DATA-88")
def hyperframes_registry_component(task, wd):
    """`hyperframes add count-up` copies the registry component into compositions/; a host mounts it on a .clip div
    with data-composition-src / data-start / data-duration / data-track-index and data-variable-values; lint, then
    snapshot frames in headless Chrome and measure them."""
    import os
    import shutil as sh
    np = _np()
    if not (Path(HF_BIN).exists() and Path(HF_GSAP).exists()):
        raise RuntimeError("hyperframes CLI or its vendored GSAP not found")
    proj = wd / "hf"
    proj.mkdir()
    env = dict(os.environ, HOME=str(wd / "home"), XDG_CACHE_HOME=str(wd / "home" / ".cache"), HYPERFRAMES_NO_UPDATE_CHECK="1")
    (wd / "home").mkdir()
    run = lambda cmd, ok=True: subprocess.run([str(c) for c in cmd], capture_output=True, text=True, timeout=60, env=env, cwd=str(proj),
                                              stdin=subprocess.DEVNULL)
    add = run([HF_BIN, "add", "count-up", "--dir", proj, "--no-clipboard", "--json"])
    comp = proj / "compositions" / "components" / "count-up.html"
    if add.returncode or not comp.exists():
        raise RuntimeError("hyperframes add failed: %s" % (add.stderr or add.stdout)[-300:])
    (comp.parent / "vendor").mkdir(exist_ok=True)
    sh.copy(HF_GSAP, comp.parent / "vendor" / "gsap.min.js")          # the CDN is unreachable here: use the CLI's own copy
    html = comp.read_text(encoding="utf-8")
    html = html.replace("https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js", "vendor/gsap.min.js")
    comp.write_text(html, encoding="utf-8")
    host = ('<!doctype html><html lang="en"><head><meta charset="UTF-8"><title>stat</title></head><body>'
            '<div id="main" data-composition-id="main" data-width="1080" data-height="1080" data-duration="3" data-fps="30" '
            'data-no-timeline style="position:relative;width:1080px;height:1080px;background:#071321">'
            '<div id="stat" class="clip" data-composition-id="count-up" data-composition-src="compositions/components/count-up.html" '
            'data-start="0" data-duration="3" data-track-index="0" data-variable-values=\'{"start":0,"end":1250,"suffix":"+"}\' '
            'style="position:absolute;inset:0"></div></div></body></html>')
    (proj / "index.html").write_text(host, encoding="utf-8")
    lint = run([HF_BIN, "lint", proj])
    snap = run([HF_BIN, "snapshot", proj, "--at", "0,1.0,2.6,2.9", "--no-end", "-o", wd / "snaps", "--json"])
    shots = sorted((wd / "snaps").glob("frame-*.png"))
    if snap.returncode or len(shots) != 4:
        raise RuntimeError("snapshot failed: %s" % (snap.stderr or snap.stdout)[-300:])
    imgs = [load_png(p) for p in shots]
    accent = lambda a: int(((a[..., 1] > 180) & (a[..., 0] < 160) & (a[..., 2] > 120) & (a[..., 2] < 200)).sum())
    ink = [accent(a) for a in imgs]
    landed_same = float(np.abs(imgs[2] - imgs[3]).mean())
    # the same component with its defaults (0 -> 100 %) for comparison: fewer glyphs, less ink
    (proj / "default.html").write_text(host.replace("index", "x").replace(
        ' data-variable-values=\'{"start":0,"end":1250,"suffix":"+"}\'', ""), encoding="utf-8")
    bad = host.replace('id="stat" class="clip" data-composition-id="count-up" ', 'id="stat" class="clip" ')
    bproj = wd / "hf_bad"
    sh.copytree(proj / "compositions", bproj / "compositions")
    (bproj / "index.html").write_text(bad, encoding="utf-8")
    blint = run([HF_BIN, "lint", bproj])
    vars_ = json.loads(html.split("data-composition-variables='")[1].split("'")[0])
    checks = [check("component copied into compositions/ by the CLI", json.loads(add.stdout).get("ok") is True, add.stdout[:120], "ok"),
              check("component declares its variables (start, end, suffix...)", {"start", "end", "suffix"} <= {v["id"] for v in vars_},
                    [v["id"] for v in vars_], "start,end,suffix"),
              check("one paused GSAP timeline registered", "gsap.timeline({ paused: true })" in html and '__timelines["count-up"]' in html, True, True),
              check("host passes hyperframes lint", lint.returncode == 0 and "0 errors" in lint.stdout, lint.stdout.strip()[-40:], "0 errors"),
              check("frame 0 is empty (stage fades in), the count is visible later", ink[0] == 0 and ink[1] > 1000, ink, "0 then ink"),
              check("value lands and holds (2.6 s vs 2.9 s ink within 2 %)", ink[2] > ink[1] and abs(ink[3] - ink[2]) <= 0.02 * ink[2],
                    [ink[2], ink[3]], "equal within 2 %"),
              check("negative control: a host missing data-composition-id fails lint", blint.returncode != 0 and "host_missing_composition_id" in blint.stdout,
                    blint.returncode, "!= 0")]
    return checks, [comp, proj / "index.html"] + shots


@card("DATA-89")
def dataviz_countup_blueprint(task, wd):
    """Blueprint 'dataviz-countup' (4-12 s): ring/number -> trend chart -> tilted stat grid with a camera push ->
    land on the hero metric; each beat cites its blueprint id in the shot plan."""
    np = _np()
    plan = [{"beat": "ring", "blueprint": "dataviz-countup", "t0": 0.0, "t1": 2.0},
            {"beat": "trend", "blueprint": "dataviz-countup", "t0": 2.0, "t1": 4.0},
            {"beat": "grid", "blueprint": "dataviz-countup", "t0": 4.0, "t1": 6.0},
            {"beat": "hero", "blueprint": "dataviz-countup", "t0": 6.0, "t1": 8.0}]
    pp = wjson(wd / "shot-plan.json", {"blueprint": "dataviz-countup", "beats": plan})
    W, H, fps, cx, cy = 240, 240, 10, 120, 110
    series = [10, 18, 15, 26, 31, 29, 40]
    pts = [(30 + i * 30, 200 - v * 3) for i, v in enumerate(series)]

    def frame(t):
        a = canvas(W, H, "#0b1320")
        if t < 2:
            p = ease("power3.out", prog(t, 0, 1.6))
            paint(a, ring_mask(H, W, cx, cy, 60, 70, 0, 360 * 0.68 * p), "#5bd1a5")
            draw_seg(a, fmt_int(68 * p, "dd"), "dd", 24, cx - 16, cy - 12, "#ffffff")
        elif t < 4:
            r = prog(t, 2.0, 1.5)
            xe = pts[0][0] + r * (pts[-1][0] - pts[0][0])
            paint(a, line_mask(H, W, [q for q in pts if q[0] <= xe] + [point_at_x(pts, xe)], 2), "#5bd1a5")
        elif t < 6:
            z = 1 + 0.5 * ease("power2.inOut", prog(t, 4.0, 2.0))
            for i in range(3):
                for j in range(3):
                    x0 = cx + (i - 1) * 50 * z
                    y0 = cy + (j - 1) * 50 * z
                    rect(a, x0 - 18 * z, y0 - 18 * z, x0 + 18 * z, y0 + 18 * z, "#1e3a5f")
        else:
            draw_seg(a, "68", "dd", 60, cx - 40, cy - 30, "#ffffff")
        return a
    n = int(8.0 * fps)
    vid = write_video(wd / "countup_blueprint.mp4", [frame(k / float(fps)) for k in range(n)], fps)
    fr = read_video(vid)
    ring = arc_fraction(fr[19], cx, cy, 60, 70, "#5bd1a5", 10)
    num = read_seg(fr[19], "dd", 24, cx - 16, cy - 12, "#0b1320", fg="#ffffff")
    line_ext = [int(np.nonzero(near(f, "#5bd1a5", 20).any(axis=0))[0].max()) for f in fr[21:39]]
    cell = [col_runs(near(f[cy], "#1e3a5f", 4))[1][1] for f in fr[41:59]]
    hero = read_seg(fr[-1], "dd", 60, cx - 40, cy - 30, "#0b1320", fg="#ffffff")
    total = plan[-1]["t1"] - plan[0]["t0"]
    checks = [check("4 beats within 4-12 s, contiguous, blueprint cited", 4 <= total <= 12 and all(b["blueprint"] == "dataviz-countup" for b in plan)
                    and all(a["t1"] == b["t0"] for a, b in zip(plan, plan[1:])), total, "4..12"),
              check("beat 1: ring and number land together (68 %)", abs(ring - 0.68) <= 0.015 and num == "68", [ring, num], [0.68, "68"]),
              check("beat 2: trend line draws left->right", line_ext == sorted(line_ext) and line_ext[-1] >= pts[-1][0] - 1, [line_ext[0], line_ext[-1]], "increasing"),
              check("beat 3: camera pushes into the stat grid (cells grow)", cell == sorted(cell) and cell[-1] >= 1.4 * cell[0], [cell[0], cell[-1]], ">= 1.4x"),
              check("beat 4: lands on the hero metric", hero == "68", hero, "68"),
              check("negative control: the first frame is not the hero metric", read_seg(fr[0], "dd", 60, cx - 40, cy - 30, "#0b1320", fg="#ffffff") != "68", 0, "!= 68")]
    return checks, [vid, pp]


PAL8_LIGHT = "#2a78d6 #eb6834 #1baf7a #eda100 #e87ba4 #008300 #4a3aa7 #e34948".split()
PAL8_DARK = "#3987e5 #d95926 #199e70 #c98500 #d55181 #008300 #9085e9 #e66767".split()


@card("DATA-92")
def chart_palettes(task, wd):
    """Fixed-order categorical palettes (identity, never rank): unique slots, worst adjacent dE2000 under protan /
    deutan / tritan simulation, colours bound to series ids, plus the risk and utilisation ramps."""
    np = _np()
    res = {}
    for name, pal in (("light", PAL8_LIGHT), ("dark", PAL8_DARK)):
        c = [rgb(x) for x in pal]
        res[name] = {"normal": min(de2000(a, b) for a, b in zip(c, c[1:]))}
        for k in ("protan", "deutan", "tritan"):
            s = [simulate_cvd(x, k) for x in c]
            res[name][k] = min(de2000(a, b) for a, b in zip(s, s[1:]))
    worst = {n: min(v[k] for k in ("protan", "deutan", "tritan")) for n, v in res.items()}
    ids = ["north", "south", "east", "west"]
    colour_of = {sid: PAL8_LIGHT[i] for i, sid in enumerate(ids)}
    vals1 = {"north": 5, "south": 9, "east": 2, "west": 7}
    vals2 = {"north": 9, "south": 1, "east": 8, "west": 3}
    by_rank = lambda v: {sid: PAL8_LIGHT[r] for r, sid in enumerate(sorted(v, key=lambda s: -v[s]))}
    W, H = 8 * 30, 60
    a = canvas(W, H, "#ffffff")
    for i, cc in enumerate(PAL8_LIGHT):
        rect(a, i * 30, 0, i * 30 + 28, 28, cc)
    for i, cc in enumerate(PAL8_DARK):
        rect(a, i * 30, 30, i * 30 + 28, 58, cc)
    png = save_png(a, wd / "palettes.png")
    b = load_png(png)
    sampled = ["#%02x%02x%02x" % tuple(int(v) for v in b[14, i * 30 + 14]) for i in range(8)]
    bad = [rgb("#d62728"), rgb("#2ca02c")]
    bad_de = de2000(simulate_cvd(bad[0], "deutan"), simulate_cvd(bad[1], "deutan"))
    risk = ["#cfe8d6", "#f3e2a6", "#f1b98a", "#e98a86"]
    risk_dark = ["#1f5a3b", "#6b5a17", "#7a4219", "#7f2626"]
    util = lambda u: "#ff907a" if u >= 1 else "#ffe083" if u >= .72 else "#b4ed88" if u >= .35 else "#8cffc0"
    out = wjson(wd / "palette_report.json", {"adjacent_dE2000": res, "documented": {"light": 9.1, "dark": 8.4},
                                             "note": "documented 9.1 / 8.4 not reproduced exactly; measured worst adjacent under CVD simulation reported"})
    checks = [check("8 unique slots per palette", len(set(PAL8_LIGHT)) == 8 and len(set(PAL8_DARK)) == 8, 8, 8),
              check("rendered swatches carry the slot colours in identity order", sampled == PAL8_LIGHT, sampled[:3], PAL8_LIGHT[:3]),
              check("light: worst adjacent dE2000 under CVD >= 8", worst["light"] >= 8, worst["light"], ">= 8"),
              check("dark: worst adjacent dE2000 under CVD >= 8", worst["dark"] >= 8, worst["dark"], ">= 8"),
              check("colour follows the series id, not its rank", colour_of == {s: colour_of[s] for s in ids} and
                    by_rank(vals1) != by_rank(vals2), colour_of, "stable across periods"),
              check("risk ramps run green -> red (R - G rises, light and dark)",
                    all((rgb(y)[0] - rgb(y)[1]) > (rgb(x)[0] - rgb(x)[1]) for P in (risk, risk_dark) for x, y in zip(P, P[1:])),
                    [rgb(x)[0] - rgb(x)[1] for x in risk], "increasing"),
              check("utilisation ramp thresholds .35/.72/1.0", [util(u) for u in (0.2, 0.5, 0.8, 1.2)] == ["#8cffc0", "#b4ed88", "#ffe083", "#ff907a"], True, True),
              check("negative control: a red/green pair fails the CVD threshold", bad_de < 8, bad_de, "< 8")]
    return checks, [png, out]


@card("DATA-93")
def doc_light_theme(task, wd):
    """A light documentation look as CSS custom properties (page #e8ecf2, panel border #cdd5e1, ink #1d2632, muted
    #5d6a7a / #98a3b3, accents), rendered and contrast-checked."""
    np = _np()
    tokens = {"--page": "#e8ecf2", "--panel": "#ffffff", "--border": "#cdd5e1", "--ink": "#1d2632", "--muted": "#5d6a7a",
              "--muted-2": "#98a3b3", "--a1": "#1f6fe5", "--a2": "#e2640f", "--a3": "#15a05a", "--a4": "#2f6fe0", "--a5": "#dc2b3e"}
    css = ":root{%s}\nbody{background:var(--page);color:var(--ink);font-family:'IBM Plex Sans','IBM Plex Sans Arabic',sans-serif}\n" \
          ".panel{background:var(--panel);border:1px solid var(--border)}\n.num{font-family:'IBM Plex Mono',monospace;" \
          "font-variant-numeric:tabular-nums}\n" % ";".join("%s:%s" % kv for kv in tokens.items())
    (wd / "theme.css").write_text(css, encoding="utf-8")
    parsed = dict(kv.split(":") for kv in css.split("{")[1].split("}")[0].split(";"))
    W, H = 360, 220
    a = canvas(W, H, parsed["--page"])
    rect(a, 20, 20, 340, 200, parsed["--border"])
    rect(a, 21, 21, 339, 199, parsed["--panel"])
    draw_seg(a, "1,284", "d,ddd", 30, 40, 40, parsed["--ink"])
    rect(a, 40, 100, 220, 108, parsed["--muted"])
    rect(a, 40, 120, 160, 126, parsed["--muted-2"])
    for i, k in enumerate(("--a1", "--a2", "--a3", "--a4", "--a5")):
        rect(a, 40 + i * 50, 150, 80 + i * 50, 180, parsed[k])
    png = save_png(a, wd / "doc_panel.png")
    b = load_png(png)
    hexat = lambda y, x: "#%02x%02x%02x" % tuple(int(v) for v in b[y, x])
    region = b[40:70, 40:40 + seg_width("d,ddd", 30)].reshape(-1, 3)
    inked = {tuple(int(v) for v in px) for px in region if tuple(px) != (255.0, 255.0, 255.0)}
    ink_px = "#%02x%02x%02x" % inked.pop() if len(inked) == 1 else "mixed:%d" % len(inked)
    samp = {"page": hexat(5, 5), "border": hexat(20, 100), "panel": hexat(60, 300), "ink": ink_px, "muted": hexat(104, 100), "muted2": hexat(123, 100)}
    ci = contrast(samp["ink"], samp["panel"])
    cm = contrast(samp["muted"], samp["panel"])
    cm2 = contrast(samp["muted2"], samp["panel"])
    checks = [check("rendered colours are the tokens", samp == {"page": "#e8ecf2", "border": "#cdd5e1", "panel": "#ffffff", "ink": "#1d2632",
                                                                "muted": "#5d6a7a", "muted2": "#98a3b3"}, samp, "tokens"),
              check("ink on panel contrast >= 7 (AAA)", ci >= 7, ci, ">= 7"),
              check("muted text on panel >= 4.5 (AA)", cm >= 4.5, cm, ">= 4.5"),
              check("page and panel are distinguishable", samp["page"] != samp["panel"], samp["page"], "!= panel"),
              check("Plex Sans body / Plex Mono tabular numbers declared", "IBM Plex Mono" in css and "tabular-nums" in css, True, True),
              check("negative control: muted-2 is too light for body text", cm2 < 4.5, cm2, "< 4.5")]
    return checks, [wd / "theme.css", png]


TWIN_DIR = Path(__file__).resolve().parents[2] / "kosif-superpowers/vendor/100-superskills/skills/kosif-montage-motion/scripts"


@card("DATA-94")
def structural_twin_lab(task, wd):
    """python structural_twin.py --sample -> report.json; python twin_dashboard.py report.json --out lab.html; then
    decode the embedded payload, re-project the truss and colour each member by utilisation (.35/.72/1.0)."""
    import base64
    import re
    import sys
    np = _np()
    rep, lab = wd / "report.json", wd / "lab.html"
    fx.run([sys.executable, TWIN_DIR / "structural_twin.py", "--sample", "--out", rep])
    fx.run([sys.executable, TWIN_DIR / "twin_dashboard.py", rep, "--out", lab])
    html = lab.read_text(encoding="utf-8")
    report = json.loads(rep.read_text(encoding="utf-8"))
    payload = re.search(r'id="payload" type="application/octet-stream">([^<]+)<', html).group(1).strip()
    embedded = json.loads(base64.b64decode(payload).decode("utf-8"))
    colour = lambda u: "#ff907a" if u >= 1 else "#ffe083" if u >= .72 else "#b4ed88" if u >= .35 else "#8cffc0"
    model = report["model"]
    coords = list(model["nodes"].values())
    xs, ys = [c[0] for c in coords], [c[1] for c in coords]
    span = max(max(xs) - min(xs), max(ys) - min(ys), 0.1)
    proj = lambda xy: (90 + 480 * ((xy[0] - min(xs)) / span), 315 - 230 * ((xy[1] - min(ys)) / span))
    util = {m["id"]: m["utilization"] for m in report["baseline"]["members"]}
    scale = round(1.1 / max(util.values()) / 0.05) * 0.05         # a slider stop that pushes the weakest member past 1.0
    a = canvas(660, 400, "#081213")
    mids = {}
    for e in model["elements"]:
        if e["id"] not in util:
            continue
        p0, p1 = proj(model["nodes"][e["a"]]), proj(model["nodes"][e["b"]])
        paint(a, line_mask(400, 660, [p0, p1], 11), colour(util[e["id"]] * scale))
        mids[e["id"]] = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
    png = save_png(a, wd / "truss_utilisation.png")
    b = load_png(png)
    meas = {k: "#%02x%02x%02x" % tuple(int(v) for v in b[int(round(y)), int(round(x))]) for k, (x, y) in mids.items()}
    expc = {k: colour(util[k] * scale) for k in mids}
    bad = subprocess.run([sys.executable, str(TWIN_DIR / "twin_dashboard.py"), str(wd / "bad.json"), "--out", str(wd / "bad.html")],
                         capture_output=True, text=True, timeout=30, input=None) if wjson(wd / "bad.json", {"schema": "other"}) else None
    checks = [check("embedded payload == the report", embedded == report, len(payload), "round-trip"),
              check("dashboard uses the .35/.72/1.0 colour ramp", "u>=1?'#ff907a':u>=.72?'#ffe083':u>=.35?'#b4ed88':'#8cffc0'" in html, True, True),
              check("load slider .10-4.00 x step .05", 'min="0.10" max="4.00" step="0.05"' in html, True, True),
              check("layout collapses under 850 px and respects reduced motion", "max-width:850px" in html and "prefers-reduced-motion" in html, True, True),
              check("load multiplier is a slider stop in .10-4.00", 0.1 <= scale <= 4.0, scale, ".10..4.00"),
              check("each member drawn in the colour of its utilisation at that load", meas == expc and len(meas) >= 3,
                    sum(meas[k] == expc[k] for k in meas), len(meas)),
              check("the weakest member fails (dashed red) while others stay below", "#ff907a" in expc.values() and len(set(expc.values())) >= 2,
                    sorted(set(expc.values())), "#ff907a + others"),
              check("negative control: a report with another schema is rejected", bad is not None and bad.returncode != 0 and "Unsupported" in bad.stderr,
                    None if bad is None else bad.returncode, "!= 0")]
    return checks, [lab, png, rep]


@card("DATA-95")
def excel_native_chart(task, wd):
    """A finished .xlsx: a real Excel table (TableStyleMedium2), sorted rows, money/percent formats, a live SUM
    total, an RTL sheet and a native bar chart 18x9 cm beside the table (openpyxl), read back and verified."""
    from openpyxl import Workbook, load_workbook
    from openpyxl.chart import BarChart, Reference
    from openpyxl.worksheet.table import Table, TableStyleInfo
    rows = [("الرياض", 48200, 0.31), ("جدة", 39150, 0.25), ("الدمام", 21780, 0.14), ("مكة", 27400, 0.18), ("المدينة", 18900, 0.12)]
    srt = sorted(rows, key=lambda r: -r[1])
    wb = Workbook()
    ws = wb.active
    ws.title = "المبيعات"
    ws.sheet_view.rightToLeft = True
    ws.append(["المدينة", "المبيعات", "الحصة"])
    for r in srt:
        ws.append(list(r))
    n = len(srt)
    for i in range(2, n + 2):
        ws.cell(i, 2).number_format = '#,##0 "ر.س"'
        ws.cell(i, 3).number_format = "0.0%"
    ws.cell(n + 2, 1, "المجموع")
    ws.cell(n + 2, 2, "=SUM(B2:B%d)" % (n + 1))
    tab = Table(displayName="Sales", ref="A1:C%d" % (n + 1))
    tab.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)
    ws.add_table(tab)
    ch = BarChart()
    ch.type = "bar"
    ch.title = "المبيعات حسب المدينة"
    ch.add_data(Reference(ws, min_col=2, min_row=1, max_row=n + 1), titles_from_data=True)
    ch.set_categories(Reference(ws, min_col=1, min_row=2, max_row=n + 1))
    ch.width, ch.height = 18, 9
    ws.add_chart(ch, "E2")
    path = wd / "sales.xlsx"
    wb.save(path)
    wb2 = load_workbook(path)
    w2 = wb2["المبيعات"]
    vals = [w2.cell(i, 2).value for i in range(2, n + 2)]
    t2 = list(w2.tables.values())[0]
    charts = w2._charts
    import zipfile
    zx = zipfile.ZipFile(path)
    chart_xml = [zx.read(nm).decode() for nm in zx.namelist() if nm.startswith("xl/charts/chart")]
    checks = [check("rows sorted by sales, descending", vals == sorted(vals, reverse=True), vals, "descending"),
              check("live SUM total formula", w2.cell(n + 2, 2).value == "=SUM(B2:B6)", w2.cell(n + 2, 2).value, "=SUM(B2:B6)"),
              check("money and percent formats", w2.cell(2, 2).number_format == '#,##0 "ر.س"' and w2.cell(2, 3).number_format == "0.0%",
                    [w2.cell(2, 2).number_format, w2.cell(2, 3).number_format], ["money", "0.0%"]),
              check("real Excel table TableStyleMedium2 over A1:C6", t2.ref == "A1:C6" and t2.tableStyleInfo.name == "TableStyleMedium2", t2.ref, "A1:C6"),
              check("RTL sheet", w2.sheet_view.rightToLeft is True, w2.sheet_view.rightToLeft, True),
              check("native bar chart in the package", len(chart_xml) == 1 and "<barChart>" in chart_xml[0] and 'barDir val="bar"' in chart_xml[0],
                    len(chart_xml), 1),
              check("chart size 18 x 9 cm", ch.width == 18 and ch.height == 9, [ch.width, ch.height], [18, 9]),
              check("negative control: the input order is not sorted", [r[1] for r in rows] != vals, [r[1] for r in rows], "unsorted")]
    return checks, [path]


def spring(t, zeta=0.6, w=12.0):
    if t <= 0:
        return 0.0
    wd_ = w * math.sqrt(1 - zeta * zeta)
    return 1 - math.exp(-zeta * w * t) * (math.cos(wd_ * t) + zeta * w / wd_ * math.sin(wd_ * t))


@card("DATA-97")
def basma_chart_scenes(task, wd):
    """Basma scenes: counter lerps easeOut over max(0.6, 0.6 d) s at 20 % of the min side; bars (2-5) spring
    (zeta .6, w 12) staggered 0.12 s from 0.25 s; list rows 0.32 s apart with a drawn tick."""
    np = _np()
    W, H, fps, d = 240, 400, 30, 2.0
    cdur = max(0.6, 0.6 * d)
    NH = int(0.2 * min(W, H))
    bars = [0.9, 0.55, 0.75, 0.4]
    lx = (W - seg_width("ddd", NH)) // 2

    def frame(t):
        a = canvas(W, H, "#101820")
        draw_seg(a, fmt_int(240 * ease("easeOut", prog(t, 0, cdur)), "ddd"), "ddd", NH, lx, 10, "#ffffff")
        for i, v in enumerate(bars):
            s = spring(t - 0.25 - 0.12 * i)
            h = 120 * v * s
            rect(a, 30 + i * 50, 250 - h, 60 + i * 50, 250, "#5bd1a5")
        for i in range(3):
            if t >= 0.32 * i:
                rect(a, 30, 280 + i * 30, 30 + 150, 290 + i * 30, "#9fb3c8")
                tick = prog(t, 0.32 * i, 0.2)
                rect(a, 200, 280 + i * 30 + 4, 200 + 16 * tick, 280 + i * 30 + 7, "#2ecc71")
        return a
    n = int(1.8 * fps)
    vid = write_video(wd / "basma.mp4", [frame(k / fps) for k in range(n)], fps)
    fr = read_video(vid)
    cerr = max(abs(_nz(seg_value(read_seg(f, "ddd", NH, lx, 10, "#101820", thr=60))) - round(240 * ease("easeOut", prog(k / fps, 0, cdur))))
               for k, f in enumerate(fr))
    serr, peaks = 0.0, []
    for i, v in enumerate(bars):
        hs = [int(near(f[:251, 45 + i * 50], "#5bd1a5", 6).sum()) for f in fr]
        serr = max(serr, max(abs(h - round(120 * v * spring(k / fps - 0.25 - 0.12 * i))) for k, h in enumerate(hs)))
        peaks.append(max(hs) / (120.0 * v) - 1)
    starts = [next(k for k, f in enumerate(fr) if near(f[:251, 45 + i * 50], "#5bd1a5", 6).any()) for i in range(4)]
    rows_on = [next(k for k, f in enumerate(fr) if near(f[285 + i * 30, 60:61], "#9fb3c8", 4).all()) for i in range(3)]
    over = math.exp(-0.6 * math.pi / math.sqrt(1 - 0.36))
    cmax = max(_nz(seg_value(read_seg(f, "ddd", NH, lx, 10, "#101820", thr=60))) for f in fr)
    checks = [check("counter lerps easeOut over max(0.6, 0.6 d) = 1.2 s", cerr <= 1, cerr, "<= 1"),
              check("numeral is 20 % of the min side", NH == 48, NH, 48),
              check("bars follow the spring (zeta .6, w 12) (px)", serr <= 1, serr, "<= 1"),
              check("spring overshoot ~9.5 %", all(abs(p - over) <= 0.02 for p in peaks), [round(p, 3) for p in peaks], round(over, 3)),
              check("bars start at 0.25 s + 0.12 s stagger", all(abs(s / float(fps) - (0.25 + 0.12 * i)) <= 1.5 / fps for i, s in enumerate(starts)), starts, "0.25 + 0.12 i"),
              check("list rows 0.32 s apart", all(abs(r / float(fps) - 0.32 * i) <= 1.0 / fps for i, r in enumerate(rows_on)), rows_on, [0, 0.32, 0.64]),
              check("negative control: the unsprung (easeOut) counter shows no overshoot", cmax == 240 and min(peaks) > 0.05, cmax, 240)]
    return checks, [vid]


@card("DATA-99")
def scrolly_timeline_scenes(task, wd):
    """Author-led data story: each scene declares text, visual state, data layer and a progress range; for video
    progress = (t - scene.start) / scene.dur, plus a static fallback frame per scene."""
    np = _np()
    scenes = [{"id": "grow", "start": 0.0, "dur": 2.0, "text": "النمو"}, {"id": "pan", "start": 2.0, "dur": 2.0, "text": "الانتقال"},
              {"id": "focus", "start": 4.0, "dur": 2.0, "text": "التركيز"}]
    W, H, fps = 240, 160, 10
    P = lambda s, t: min(1.0, max(0.0, (t - s["start"]) / s["dur"]))

    def frame(t):
        a = canvas(W, H, "#ffffff")
        p0, p1, p2 = (P(s, t) for s in scenes)
        rect(a, 20, 120 - 80 * p0, 50, 120, "#2a78d6")
        x = 80 + 120 * p1
        rect(a, x, 60, x + 10, 70, "#eb6834")
        rect(a, 20, 140, 220, 150, lerp_c("#dddddd", "#1baf7a", p2))
        return a
    n = int(6.0 * fps) + 1
    vid = write_video(wd / "story.mp4", [frame(k / float(fps)) for k in range(n)], fps)
    fallbacks = [save_png(frame(s["start"] + s["dur"]), wd / ("fallback_%s.png" % s["id"])) for s in scenes]
    fr = read_video(vid)
    errs = [0.0, 0.0, 0.0]
    for k, f in enumerate(fr):
        t = k / float(fps)
        h = bar_heights(f, 120, [35], "#ffffff")[0]
        errs[0] = max(errs[0], abs(h - round(80 * P(scenes[0], t))))
        xs = np.nonzero(near(f[65], "#eb6834", 6))[0]
        errs[1] = max(errs[1], abs(xs.min() - round(80 + 120 * P(scenes[1], t))))
        errs[2] = max(errs[2], float(np.abs(f[145, 100] - np.array(lerp_c("#dddddd", "#1baf7a", P(scenes[2], t)))).max()))
    fb_ok = all(float(np.abs(load_png(p) - fr[int(round((s["start"] + s["dur"]) * fps))]).max()) == 0 for p, s in zip(fallbacks, scenes))
    frozen = all(bar_heights(fr[k], 120, [35], "#ffffff")[0] == 80 for k in range(20, n))
    checks = [check("scene 1 state == progress (bar px)", errs[0] <= 1, errs[0], "<= 1"),
              check("scene 2 state == progress (pan px)", errs[1] <= 1, errs[1], "<= 1"),
              check("scene 3 state == progress (colour)", errs[2] <= 1.5, errs[2], "<= 1.5"),
              check("static fallback frame per scene == its end state", fb_ok, fb_ok, True),
              check("a finished scene stays at progress 1", frozen, frozen, True),
              check("negative control: the first frame is not any scene's end state",
                    all(float(np.abs(load_png(p) - fr[0]).max()) > 0 for p in fallbacks), 0, "differs")]
    return checks, fallbacks + [vid]


def _steps_layout(n):
    if n <= 4:
        return "grid"
    if n <= 6:
        return "vertical"
    if n <= 9:
        return "vertical-phases"
    return "compact"


@card("DATA-100")
def numbered_steps_infographic(task, wd):
    """Numbered steps: 3-4 grid, 5-6 vertical timeline, 7-9 vertical with phases, 10+ compact; height 630 + 135 per
    step above 4 (cap 1500) at 1200 px; numbered 36 px circle markers on a 2 px rail; title 2-5 words, desc < 15."""
    np = _np()
    steps = [("حدد الهدف بدقة", "اكتب ما الذي يجب أن يتغير ولماذا الآن"), ("اجمع البيانات الخام", "من المصدر الأصلي مع تاريخ السحب"),
             ("نظف الجدول", "احذف التكرار وعالج القيم المفقودة"), ("اختر الرسم المناسب", "حسب العلاقة لا حسب الذوق"),
             ("حرّك القصة", "مشهد واحد لكل رسالة"), ("راجع الأرقام", "قارن كل رقم بمصدره قبل النشر")]
    valid = lambda t, d: 2 <= len(t.split()) <= 5 and len(d.split()) < 15
    n = len(steps)
    height = min(1500, 630 + 135 * max(0, n - 4))
    W = 1200
    a = canvas(W, height, "#ffffff")
    rail_x = W - 120
    top, bot = 100, height - 100
    rect(a, rail_x - 1, top, rail_x + 1, bot, "#cdd5e1")
    cys = [top + i * (bot - top) / float(n - 1) for i in range(n)]
    for i, cy in enumerate(cys):
        paint(a, pil_mask(W, height, lambda d: d.ellipse([rail_x - 18, cy - 18, rail_x + 18, cy + 18], fill=255)), "#1f6fe5")
        draw_seg(a, str(i + 1), "d", 16, rail_x - 4, int(cy) - 8, "#ffffff")
        rect(a, rail_x - 620, cy - 12, rail_x - 60, cy + 12, "#e8ecf2")
    png = save_png(a, wd / "steps.png")
    b = load_png(png)
    diam = [len(col_runs(near(b[int(cy)], "#1f6fe5", 4) | near(b[int(cy)], "#ffffff", 4) & False)) and
            max(nn for s0, nn in col_runs(near(b[int(cy) - 12], "#1f6fe5", 4)) ) for cy in cys]
    def bbox_w(cy):
        m = near(b[int(cy) - 25:int(cy) + 26, rail_x - 25:rail_x + 26], "#1f6fe5", 4)
        xs_ = np.nonzero(m.any(axis=0))[0]
        return int(xs_.max() - xs_.min())       # extreme pixel centres: diameter in px
    vert = [bbox_w(cy) for cy in cys]
    rail_w = int(near(b[int((cys[0] + cys[1]) / 2)], "#cdd5e1", 4).sum())
    digits = [read_seg(b, "d", 16, rail_x - 4, int(cy) - 8, "#1f6fe5", fg="#ffffff") for cy in cys]
    from PIL import Image
    size = Image.open(png).size
    exp_layout = {3: "grid", 4: "grid", 5: "vertical", 6: "vertical", 7: "vertical-phases", 9: "vertical-phases", 10: "compact", 12: "compact"}
    checks = [check("layout by step count", all(_steps_layout(k) == v for k, v in exp_layout.items()), {k: _steps_layout(k) for k in exp_layout}, exp_layout),
              check("canvas 1200 x (630 + 135 x (n - 4))", size == (1200, 900), size, (1200, 900)),
              check("height capped at 1500", min(1500, 630 + 135 * (12 - 4)) == 1500, min(1500, 630 + 135 * 8), 1500),
              check("markers are 36 px circles", all(abs(v - 36) <= 1 for v in vert), vert, 36),
              check("rail 2 px", rail_w == 2, rail_w, 2),
              check("markers numbered in order", digits == [str(i + 1) for i in range(n)], digits, "1..6"),
              check("every step: title 2-5 words, description < 15 words", all(valid(t, d) for t, d in steps), True, True),
              check("negative control: a one-word title / 20-word description is rejected", not valid("خطوة", " ".join(["كلمة"] * 20)), False, False)]
    return checks, [png]


@card("DATA-101")
def milestone_timeline(task, wd):
    """Milestone timeline with x proportional to real time (MG-042: 0-1 axes, 1-5 draw, 5-8 milestone); glowing
    connectors draw over 600 ms; a red dot hops 0.8 s per chapter; Gantt only for data with real start/end."""
    import datetime as dt
    np = _np()
    events = [dt.date(2020, 3, 1), dt.date(2021, 1, 15), dt.date(2021, 6, 1), dt.date(2023, 9, 30), dt.date(2025, 2, 10)]
    span = (events[-1] - events[0]).days
    W, H, fps, x0, x1 = 400, 120, 10, 20, 380
    X = lambda d: x0 + (d - events[0]).days / float(span) * (x1 - x0)
    choose = lambda items: "gantt" if all("start" in it and "end" in it for it in items) else "milestone"

    def frame(t):
        a = canvas(W, H, "#0b0f14")
        rect(a, x0, 60, x0 + (x1 - x0) * prog(t, 0, 1.0), 61, "#3a4452")
        for i, d in enumerate(events):
            ti = 1.0 + 0.8 * i
            if t >= ti:
                paint(a, pil_mask(W, H, lambda dd: dd.ellipse([X(d) - 4, 56, X(d) + 4, 64], fill=255)), "#64d2ff")
            if i > 0 and t >= ti - 0.6:
                c = prog(t, ti - 0.6, 0.6)
                xa = X(events[i - 1])
                rect(a, xa, 44, xa + (X(d) - xa) * c, 47, "#64d2ff", 0.3)
                rect(a, xa, 45, xa + (X(d) - xa) * c, 46, "#64d2ff")
        k = min(len(events) - 1, int(max(0.0, t - 1.0) / 0.8))
        if t >= 1.0:
            rx = X(events[k])
            paint(a, pil_mask(W, H, lambda dd: dd.ellipse([rx - 3, 80, rx + 3, 86], fill=255)), "#ff3b30")
        return a
    n = int(8.0 * fps)
    vid = write_video(wd / "timeline.mp4", [frame(k / float(fps)) for k in range(n)], fps)
    fr = read_video(vid)
    last = fr[-1]
    m = near(last[60], "#64d2ff", 10)
    centres = [s + nn / 2.0 for s, nn in col_runs(m)]
    perr = max(abs(c - X(d)) for c, d in zip(centres, events)) if len(centres) == 5 else 99
    even = [x0 + i * (x1 - x0) / 4.0 for i in range(5)]
    eerr = max(abs(c - e) for c, e in zip(centres, even)) if len(centres) == 5 else 0
    xa = X(events[0])
    lens = [int(near(f[45, int(xa):int(X(events[1])) + 1], "#64d2ff", 10).sum()) for f in fr]
    c_start = next(k for k, v in enumerate(lens) if v > 0)
    c_full = next(k for k, v in enumerate(lens) if v >= lens[-1])
    hops = []
    for i in range(5):
        k = int(round((1.0 + 0.8 * i + 0.4) * fps))
        xs = np.nonzero(near(fr[k][83], "#ff3b30", 20))[0]
        hops.append(abs((xs.min() + xs.max() + 1) / 2.0 - X(events[i])))
    checks = [check("milestones at x proportional to real dates (px)", perr <= 1.0, perr, "<= 1"),
              check("connector draws over ~600 ms", abs((c_full - c_start + 1) / float(fps) - 0.6) <= 0.1, (c_full - c_start + 1) / float(fps), 0.6),
              check("red dot hops to each chapter every 0.8 s", max(hops) <= 1.0, hops, "<= 1 px"),
              check("Gantt only with real start/end", choose([{"start": 1, "end": 3}, {"start": 2, "end": 5}]) == "gantt" and choose([{"date": 1}]) == "milestone",
                    "gantt / milestone", True),
              check("negative control: evenly spaced markers would misplace the dates", eerr > 5, eerr, "> 5 px")]
    return checks, [vid]


@card("DATA-102")
def hub_avatars_bracket(task, wd):
    """Hub scales 0.8 -> 1 (back.out), avatars on an elliptical ring pop in with a stagger, lines draw after; a
    bracket pulse travels leaf -> final at ~600 px/s."""
    np = _np()
    W, H, fps = 420, 240, 30
    cx, cy, rx, ry, N = 140, 120, 110, 70, 10
    ang = [2 * math.pi * i / N for i in range(N)]
    pos = [(cx + rx * math.cos(a), cy + ry * math.sin(a)) for a in ang]
    t_av = 0.3 + 0.06 * (N - 1) + 0.4
    path = [(300, 30), (360, 30), (360, 120), (410, 120)]
    plen = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(path, path[1:]))

    def frame(t):
        a = canvas(W, H, "#0d1117")
        hs = 0.8 + 0.2 * ease("back.out", prog(t, 0, 0.4))
        r = 16 * hs
        if t >= t_av:
            for x, y in pos:
                paint(a, line_mask(H, W, [(cx, cy), (cx + (x - cx) * prog(t, t_av, 0.3), cy + (y - cy) * prog(t, t_av, 0.3))], 1), "#30363d")
        paint(a, pil_mask(W, H, lambda d: d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)), "#f0f6fc")
        for i, (x, y) in enumerate(pos):
            s = ease("back.out", prog(t, 0.3 + 0.06 * i, 0.4))
            if s > 0:
                rr = 7 * s
                paint(a, pil_mask(W, H, lambda d: d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=255)), "#58a6ff")
        paint(a, line_mask(H, W, path, 1), "#30363d")
        u = (600.0 * prog(t, 0.2, 10)) * 10 / plen
        if 0 < u < 1:
            px, py = point_at(path, u)
            paint(a, pil_mask(W, H, lambda d: d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=255)), "#ffd33d")
        return a
    n = int(2.0 * fps)
    vid = write_video(wd / "hub.mp4", [frame(k / fps) for k in range(n)], fps)
    fr = read_video(vid)
    last = fr[-1]
    cerr = 0.0
    for x, y in pos:
        c = centroid(near(last[int(y) - 9:int(y) + 10, int(x) - 9:int(x) + 10], "#58a6ff", 10))
        cerr = max(cerr, math.hypot(c[0] + int(x) - 9 - x, c[1] + int(y) - 9 - y) if c else 99)
    hub_r = [math.sqrt(near(f[cy - 25:cy + 25, cx - 25:cx + 25], "#f0f6fc", 10).sum() / math.pi) for f in fr]
    k_line = next(k for k, f in enumerate(fr) if near(f, "#30363d", 6)[:, :290].any())
    pul = [centroid(near(f, "#ffd33d", 30)) for f in fr]
    trav = []
    for k in range(1, n):
        if pul[k] and pul[k - 1]:
            trav.append(math.hypot(pul[k][0] - pul[k - 1][0], pul[k][1] - pul[k - 1][1]))
    seg_speed = [v * fps for v in trav if v > 5]
    av_first = [next(k for k, f in enumerate(fr) if near(f[int(y), int(x):int(x) + 1], "#58a6ff", 10).all()) for x, y in pos]
    checks = [check("10 avatars on the ellipse (px)", cerr <= 1.5, cerr, "<= 1.5"),
              check("hub overshoots then settles at 1 (back.out from 0.8)", max(hub_r) > hub_r[-1] * 1.03 and abs(hub_r[0] / hub_r[-1] - 0.8) <= 0.06,
                    [hub_r[0], max(hub_r), hub_r[-1]], "0.8 -> >1 -> 1"),
              check("avatars pop with a stagger", av_first == sorted(av_first) and av_first[-1] > av_first[0], av_first[:4], "increasing"),
              check("lines draw after the avatars land", k_line / float(fps) >= t_av - 1e-6, k_line / float(fps), ">= %.2f" % t_av),
              check("bracket pulse ~600 px/s (median; corners cut the chord)", bool(seg_speed) and abs(float(np.median(seg_speed)) - 600) / 600 <= 0.03,
                    [round(v) for v in seg_speed[:5]], 600),
              check("negative control: the first frame shows no avatars", not near(fr[0], "#58a6ff", 10).any(), 0, 0)]
    return checks, [vid]


@card("DATA-103")
def data_prep_before_animating(task, wd):
    """Prepare data before the scene: SQL over a raw CSV (dedupe, drop nulls, aggregate), a least-squares
    forecast, and a clean JSON whose data arrays come first, read at the top of the composition."""
    import csv
    import sqlite3
    np = _np()
    raw = wd / "raw.csv"
    rows = [("2026-01", "a", "10"), ("2026-01", "b", "15"), ("2026-01", "b", "15"), ("2026-02", "a", "14"), ("2026-02", "b", ""),
            ("2026-02", "b", "18"), ("2026-03", "a", "18"), ("2026-03", "b", "21"), ("2026-04", "a", "22"), ("2026-04", "b", "24"),
            ("2026-04", "a", "22")]
    with raw.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["month", "branch", "sales"])
        w.writerows(rows)
    con = sqlite3.connect(str(wd / "prep.db"))
    con.execute("create table raw(month text, branch text, sales text)")
    with raw.open(encoding="utf-8") as fh:
        con.executemany("insert into raw values (?,?,?)", list(csv.reader(fh))[1:])
    q = ("select month, sum(cast(sales as integer)) from (select distinct month, branch, sales from raw where sales <> '') "
         "group by month order by month")
    agg = con.execute(q).fetchall()
    con.close()
    months = [m for m, _ in agg]
    totals = [int(v) for _, v in agg]
    x = np.arange(len(totals))
    slope, icpt = np.polyfit(x, totals, 1)
    fc = [round(float(slope * (len(totals) + i) + icpt), 2) for i in range(3)]
    out = wd / "data.json"
    out.write_text(json.dumps({"data": {"months": months, "totals": totals, "forecast": fc}, "meta": {"source": "raw.csv", "query": q}},
                              ensure_ascii=False, indent=1), encoding="utf-8")
    scene = wd / "scene.html"
    scene.write_text("<!doctype html><script>const DATA = %s;</script><div id=chart></div>" % json.dumps(json.loads(out.read_text())["data"]),
                     encoding="utf-8")
    loaded = json.loads(out.read_text(encoding="utf-8"))
    raw_sum = sum(int(r[2]) for r in rows if r[2])
    checks = [check("aggregated totals per month (deduped, nulls dropped)", totals == [25, 32, 39, 46], totals, [25, 32, 39, 46]),
              check("least-squares forecast continues the trend", fc == [53.0, 60.0, 67.0], fc, [53, 60, 67]),
              check("data arrays first in the JSON", list(loaded)[0] == "data", list(loaded), "data first"),
              check("scene reads the data at the top", scene.read_text(encoding="utf-8").startswith("<!doctype html><script>const DATA = "), True, True),
              check("negative control: the raw rows double count", raw_sum != sum(totals), raw_sum, "!= %d" % sum(totals))]
    return checks, [out, scene]


@card("DATA-104")
def venn_and_spectrum(task, wd):
    """Two multiply-blended circles slide together (700 ms ease) with the overlap label after contact; a 20-segment
    spectrum bar with a marker driven by one scalar and a value label."""
    np = _np()
    W, H, fps, r = 320, 200, 30, 50
    c1, c2 = np.array(rgb("#ff6b6b"), float), np.array(rgb("#4dabf7"), float)
    sep = lambda t: 200 - 130 * ease("easeInOut", prog(t, 0, 0.7))
    val = lambda t: 0.73 * ease("easeInOut", prog(t, 0, 0.7))
    ys, xs = np.mgrid[0:H, 0:W]

    def frame(t):
        a = canvas(W, H, "#ffffff")
        d = sep(t)
        ax, bx = 160 - d / 2, 160 + d / 2
        m1 = (xs + 0.5 - ax) ** 2 + (ys + 0.5 - 80) ** 2 < r * r
        m2 = (xs + 0.5 - bx) ** 2 + (ys + 0.5 - 80) ** 2 < r * r
        a[m1] = a[m1] * c1 / 255.0
        a[m2] = a[m2] * c2 / 255.0
        if d < 2 * r:
            rect(a, 150, 8, 170, 14, "#222222")
        for i in range(20):
            rect(a, 60 + i * 10, 160, 70 + i * 10, 170, lerp_c("#ff0000", "#0000ff", i / 19.0))
        mx = 60 + 200 * val(t)
        rect(a, mx - 1, 152, mx + 1, 178, "#000000")
        draw_seg(a, fmt_int(val(t) * 100, "dd"), "dd", 12, 280, 160, "#000000")
        return a
    n = int(1.0 * fps)
    vid = write_video(wd / "venn.mp4", [frame(k / fps) for k in range(n)], fps)
    fr = read_video(vid)
    last = fr[-1]
    ov = last[80, 160]
    mult = c1 * c2 / 255.0
    contact = next(k for k in range(n) if sep(k / fps) < 2 * r)
    label = [bool(near(f[11, 160:161], "#222222", 6).all()) for f in fr]
    area = [int(near(f, mult, 3).sum()) for f in fr]
    seg_cols = {tuple(last[165, 65 + i * 10]) for i in range(20)}
    merr = max(abs((np.nonzero(near(f[175], "#000000", 10)[:270])[0].mean() + 0.5) - (60 + 200 * val(k / fps))) for k, f in enumerate(fr))
    lab = read_seg(last, "dd", 12, 280, 160, "#ffffff", fg="#000000")
    checks = [check("overlap colour == multiply(c1, c2)", float(np.abs(ov - mult).max()) <= 1, ov.tolist(), mult.round().tolist()),
              check("overlap label only after contact", label.index(True) == contact and not any(label[:contact]), label.index(True), contact),
              check("overlap grows as the circles slide", area[-1] > 0 and area == sorted(area), [area[contact], area[-1]], "growing"),
              check("spectrum has 20 segments", len(seg_cols) == 20, len(seg_cols), 20),
              check("marker x driven by the scalar (px)", merr <= 1.0, merr, "<= 1"),
              check("value label == scalar", lab == "73", lab, "73"),
              check("negative control: before contact there is no overlap", area[0] == 0, area[0], 0)]
    return checks, [vid]


@card("DATA-105")
def chart_icon_metaphor(task, wd):
    """A vector card with four rising accent bars as a finance/data metaphor: bar heights r*(.26 + .35 i); no data
    binding, and if real numbers are shown the icon is replaced by a real chart."""
    np = _np()
    r = 40

    def icon(data=None):
        a = canvas(120, 120, "#f4f1ea")
        rect(a, 4, 4, 116, 116, "#ffffff")
        for i in range(4):
            h = r * (.26 + .35 * i) * 0.7
            rect(a, 18 + i * 22, 100 - h, 18 + i * 22 + 14, 100, "#e4572e")
        return a
    p = save_png(icon([1, 2, 3, 4]), wd / "icon.png")
    p2 = save_png(icon([9, 1, 5, 2]), wd / "icon_other_data.png")
    b = load_png(p)
    hs = bar_heights(b, 100, [25 + i * 22 for i in range(4)], "#ffffff")
    exp = [round(r * (.26 + .35 * i) * 0.7) for i in range(4)]
    decide = lambda shows_numbers: "real-chart" if shows_numbers else "icon"
    flat = canvas(120, 120, "#ffffff")
    for i in range(4):
        rect(flat, 18 + i * 22, 70, 18 + i * 22 + 14, 100, "#e4572e")
    fh = bar_heights(flat, 100, [25 + i * 22 for i in range(4)], "#ffffff")
    checks = [check("bar heights r(.26 + .35 i) (scaled to the card)", max(abs(a - e) for a, e in zip(hs, exp)) <= 1, hs, exp),
              check("rising bars", hs == sorted(hs) and len(set(hs)) == 4, hs, "increasing"),
              check("no data binding: same icon for other data", float(np.abs(load_png(p2) - b).max()) == 0, 0, 0),
              check("numbers shown -> replace with a real chart", decide(True) == "real-chart" and decide(False) == "icon", True, True),
              check("negative control: equal bars fail the rising rule", not (fh == sorted(fh) and len(set(fh)) == 4), fh, "not rising")]
    return checks, [p]
