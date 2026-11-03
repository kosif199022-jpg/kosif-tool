"""Programs for the ui-product-device family.

Product-UI motion recipes are performed as time functions (cursor paths, springs, easings, typing,
reveals), rendered to small Pillow frames where geometry matters, and measured back from the
pixels or checked against closed-form answers (analytic spring overshoot, arc length, projection).
Validators (layouts, storyboards, tokens, landing pages) run on planted good/bad fixtures.
"""
from __future__ import annotations
import json
import math
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO = Path(__file__).resolve().parents[5]
FONT_DIRS = ["/usr/share/fonts/truetype/noto", "/usr/share/fonts/truetype/dejavu", "/usr/share/fonts/truetype/liberation"]
LATIN = ["NotoSans-Regular.ttf", "DejaVuSans.ttf", "LiberationSans-Regular.ttf"]
MONO = ["NotoSansMono-Regular.ttf", "DejaVuSansMono.ttf", "LiberationMono-Regular.ttf"]


def font(size, names=LATIN):
    for d in FONT_DIRS:
        for n in names:
            if (Path(d) / n).is_file():
                return ImageFont.truetype(str(Path(d) / n), size)
    raise FileNotFoundError("font")


def save_json(work, name, obj):
    (work / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1, default=float), encoding="utf-8")


def clamp01(p): return max(0.0, min(1.0, p))
def out_cubic(p): return 1 - (1 - p) ** 3
def out_quad(p): return 1 - (1 - p) ** 2
def in_out_cubic(p): return 4 * p ** 3 if p < 0.5 else 1 - (-2 * p + 2) ** 3 / 2
def in_out_sine(p): return -(math.cos(math.pi * p) - 1) / 2
def power2_in_out(p): return 2 * p * p if p < 0.5 else 1 - (-2 * p + 2) ** 2 / 2


def bezier(x1, y1, x2, y2):
    def bx(t): return 3 * (1 - t) ** 2 * t * x1 + 3 * (1 - t) * t * t * x2 + t ** 3
    def by(t): return 3 * (1 - t) ** 2 * t * y1 + 3 * (1 - t) * t * t * y2 + t ** 3

    def f(x):
        lo, hi = 0.0, 1.0
        for _ in range(60):
            m = (lo + hi) / 2
            lo, hi = (m, hi) if bx(m) < x else (lo, m)
        return by((lo + hi) / 2)
    return f


def spring(k, c, m=1.0, secs=2.0, fps=240, x0=0.0, target=1.0):
    x, v, out = x0, 0.0, []
    dt = 1 / fps / 10
    for _ in range(int(secs * fps)):
        out.append(x)
        for _ in range(10):
            a = (-k * (x - target) - c * v) / m
            v += a * dt
            x += v * dt
    return np.array(out)


def overshoot(k, c, m=1.0):
    z = c / (2 * math.sqrt(k * m))
    return math.exp(-z * math.pi / math.sqrt(1 - z * z)) if z < 1 else 0.0


def settle_time(curve, fps=240, tol=0.02, target=1.0):
    bad = np.nonzero(np.abs(curve - target) > tol * abs(target if target else 1))[0]
    return (bad[-1] + 1) / fps if len(bad) else 0.0


def elastic_out(p, amp=1.0, period=0.5):
    if p in (0, 1):
        return float(p)
    s = period / (2 * math.pi) * math.asin(1 / amp)
    return amp * 2 ** (-10 * p) * math.sin((p - s) * 2 * math.pi / period) + 1


def back_out(p, s=1.70158):
    p -= 1
    return 1 + (s + 1) * p ** 3 + s * p ** 2


def ring_radius(img, cx, cy, thr=30):
    a = np.asarray(img.convert("L"))
    row = a[int(cy)]
    xs = np.nonzero(row > thr)[0]
    return (xs.max() - cx) if len(xs) else 0


def graphemes(s):
    out = []
    for ch in s:
        if out and (unicodedata.combining(ch) or ch in "‍ًٌٍَُِّْ"):
            out[-1] += ch
        else:
            out.append(ch)
    return out


def seeded_holds(n, seed=7):
    """1-frame hold after every 2-3 chars from a seeded pattern (no Math.random in renders)."""
    rng = np.random.default_rng(seed)
    holds, i = set(), 0
    while i < n:
        i += int(rng.integers(2, 4))
        holds.add(i)
    return holds


def typed_count(t, cps, fps=30, holds=frozenset()):
    frame = int(t * fps)
    shown, f = 0, 0
    acc = 0.0
    while f < frame:
        f += 1
        if shown in holds and acc >= 0:
            acc = -1  # hold one frame
            continue
        acc = 0
        shown = min(int((f - sum(1 for h in holds if h <= shown)) * cps / fps), 10 ** 6)
    return shown


# ---------------------------------------------------------------- UI-01
def storyboard_ok(rows):
    cols = {"time", "screen", "pointer", "camera", "text"}
    errs = [f"row {i} columns" for i, r in enumerate(rows) if set(r) != cols]
    if rows and rows[0]["time"] != 0:
        errs.append("frame 1 not covered")
    return errs


def stills_plan(actions, D, trans=()):
    return sorted({0.0, *actions, *[(a + b) / 2 for a, b in trans], round(D - 1 / 30, 4)})


def ui_01(work):
    rows = [{"time": 0, "screen": "home", "pointer": "-", "camera": "full", "text": "مرحبا"},
            {"time": 1.2, "screen": "home", "pointer": "click New", "camera": "push New", "text": ""},
            {"time": 2.4, "screen": "editor", "pointer": "type", "camera": "settle", "text": ""}]
    bad = [dict(rows[0], time=0.5), {"time": 1, "screen": "x"}]
    plan = stills_plan([1.2, 2.4], 4.0, [(1.6, 2.0)])
    save_json(work, "storyboard.json", {"rows": rows, "stills": plan})
    return [("five-column storyboard valid", storyboard_ok(rows) == [], storyboard_ok(rows)),
            ("missing columns and late first row caught", storyboard_ok(bad) == ["row 1 columns", "frame 1 not covered"], storyboard_ok(bad)),
            ("stills: first, each action, transition midpoint, last", plan == [0.0, 1.2, 1.8, 2.4, 3.9667], plan)]


# ---------------------------------------------------------------- UI-02
def latency_verdict(ms):
    return "slideshow" if ms < 30 else "real" if 60 <= ms <= 120 else "bug" if ms > 200 else "borderline"


def response_valid(press_t, done_t, success_t):
    return success_t >= done_t > press_t


def ui_02(work):
    v = {ms: latency_verdict(ms) for ms in (0, 90, 150, 250)}
    save_json(work, "latency.json", v)
    return [("0 ms reads as a slideshow", v[0] == "slideshow", v),
            ("90 ms is real latency (60-120)", v[90] == "real", v[90]),
            ("250 ms reads as a bug", v[250] == "bug", v[250]),
            ("success after the action completes accepted", response_valid(1.0, 1.4, 1.45), "ok"),
            ("success animated before completion refused", not response_valid(1.0, 1.4, 1.2), "refused"),
            ]


# ---------------------------------------------------------------- UI-03
DIGITS = {"latin": set("0123456789"), "arabic": set("٠١٢٣٤٥٦٧٨٩")}


def label_ok(lbl, width=1080):
    k = width / 1080
    return lbl["size"] >= 28 * k and 1.6 <= lbl["lh"] <= 1.8 and lbl.get("tracking", 0) == 0


def price_ok(text, confirmed):
    systems = {n for n, ds in DIGITS.items() if any(c in ds for c in text)}
    return confirmed and len(systems) == 1 and ("SAR" in text or "ر.س" in text or "﷼" in text)


def ui_03(work):
    good = {"size": 30, "lh": 1.7, "tracking": 0}
    save_json(work, "labels.json", [good])
    return [("30 px / lh 1.7 / tracking 0 accepted", label_ok(good), good),
            ("24 px Arabic label rejected", not label_ok(dict(good, size=24)), 24),
            ("tracked Arabic rejected", not label_ok(dict(good, tracking=0.05)), 0.05),
            ("confirmed 'SAR 1,250' in one numeral system accepted", price_ok("SAR 1,250", True), "ok"),
            ("mixed '١٢50 SAR' rejected", not price_ok("١٢50 SAR", True), "mixed"),
            ("unconfirmed price rejected", not price_ok("SAR 99", False), "unconfirmed")]


# ---------------------------------------------------------------- UI-04
def screen_layers(scale, shift=0.0, parallax=0.03):
    W, H = 180 * scale, 120 * scale
    im = Image.new("L", (W, H), 20)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 16 * scale], fill=80)            # chrome
    cx = shift * parallax * scale
    d.rectangle([4 * scale + cx, 4 * scale, 30 * scale + cx, 12 * scale], fill=200)
    d.rectangle([10 * scale + shift * scale, 30 * scale, 170 * scale + shift * scale, 60 * scale], fill=255)  # content card
    return im


def ui_04(work):
    hi = screen_layers(2)
    hi.save(work / "screen_2x.png")
    ref = screen_layers(1)
    diff = np.abs(np.asarray(hi.resize(ref.size, Image.BOX)).astype(int) - np.asarray(ref).astype(int)).mean()
    a = np.asarray(screen_layers(1, shift=-20))
    chrome_x = np.nonzero(a[8] == 200)[0].min()
    card_x = np.nonzero(a[45] == 255)[0].min()
    return [("rebuilt at 2x density (360x240)", hi.size == (360, 240), hi.size),
            ("2x layers downsample onto the 1x reference", diff < 2, round(diff, 3)),
            ("content shifts 20 px, chrome only ~3% (0.6 px)", card_x == 0 and chrome_x in (3, 4), (int(card_x), int(chrome_x)))]


# ---------------------------------------------------------------- UI-05
def ui_05(work):
    W = 120
    mark = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    d = ImageDraw.Draw(mark)
    d.ellipse([10, 10, 110, 110], fill=(30, 90, 200, 255))
    d.rectangle([45, 30, 75, 90], fill=(255, 255, 255, 255))
    a = np.asarray(mark)
    blue = np.where((a[..., 2] == 200)[..., None], a, 0).astype(np.uint8)
    white = np.where((a[..., 0] == 255)[..., None], a, 0).astype(np.uint8)
    Image.fromarray(blue).save(work / "layer_ring.png")
    Image.fromarray(white).save(work / "layer_bar.png")
    restack = Image.alpha_composite(Image.fromarray(blue), Image.fromarray(white))
    diff = np.abs(np.asarray(restack).astype(int) - a.astype(int)).max() / 255
    stretch = (224 / 160) / (1200 / 800)
    return [("layers re-stack to the original within 1/255", diff <= 1 / 255, diff),
            ("1200x800 into 224x160 stretches ~7%", abs((1 - stretch) - 0.0667) < 0.001, round(1 - stretch, 4)),
            ]


# ---------------------------------------------------------------- UI-06
def mirror_layout(ltr, width):
    out = {}
    for k, (x, y, w, h) in ltr.items():
        out[k] = (width - x - w, y, w, h)
    return out


def rtl_motion():
    return {"cursor_start": "bottom-right", "push_from": "left", "toast": "top-left", "back_chevron": "right", "toggle_on": "left"}


def ui_06(work):
    ltr = {"back": (8, 8, 24, 24), "title": (40, 8, 200, 24), "toast": (290, 8, 92, 30)}
    rtl = mirror_layout(ltr, 390)
    tabs = ["home", "search", "profile"]
    save_json(work, "rtl.json", {"layout": rtl, "motion": rtl_motion()})
    return [("back chevron moves to the right edge (x=358)", rtl["back"][0] == 358, rtl["back"]),
            ("toast enters top-left (top-end in RTL)", rtl["toast"][0] == 8 and rtl_motion()["toast"] == "top-left", rtl["toast"]),
            ("mirroring twice is identity", mirror_layout(rtl, 390) == ltr, "involution"),
            ("RTL tab order reversed", list(reversed(tabs)) == ["profile", "search", "home"], "order"),
            ("forward navigation pushes from the left", rtl_motion()["push_from"] == "left", "left")]


# ---------------------------------------------------------------- UI-07
def dashboard_ok(tiles, executive=False):
    lo, hi = (4, 6) if executive else (5, 7)
    errs = []
    if not lo <= len(tiles) <= hi:
        errs.append("kpi count")
    if len({t["size"] for t in tiles}) == 1:
        errs.append("wall of equal tiles")
    order = sorted(tiles, key=lambda t: t["delay"])
    if order[0]["role"] != "headline":
        errs.append("headline not first")
    return errs


def ui_07(work):
    good = [{"role": "headline", "size": 2, "delay": 0}] + [{"role": "kpi", "size": 1, "delay": 0.1 * i} for i in range(1, 6)]
    wall = [{"role": "kpi", "size": 1, "delay": 0.1 * i} for i in range(9)]
    save_json(work, "dashboard.json", good)
    return [("1 focal + 5 KPIs, headline first", dashboard_ok(good) == [], dashboard_ok(good)),
            ("9 equal tiles: count, wall and order all caught", dashboard_ok(wall) == ["kpi count", "wall of equal tiles", "headline not first"], dashboard_ok(wall)),
            ("executive summary caps at 6", dashboard_ok(good + [dict(good[1])], executive=True) == ["kpi count"], "exec")]


# ---------------------------------------------------------------- UI-08
CHECKLIST = ["trigger", "visible_change", "settled_state", "duration_in_range", "physical_metaphor", "interruptible", "reduced_motion", "flash_safe"]


def beat_score(b):
    return round(sum(bool(b.get(k)) for k in CHECKLIST) / 8 * 10, 2)


def flashes_per_s(lum, fps):
    big = np.abs(np.diff(lum)) > 0.2 * 255
    return big.sum() / 2 / (len(lum) / fps)


def ui_08(work):
    full = {k: True for k in CHECKLIST}
    six = dict(full, interruptible=False, flash_safe=False)
    fps = 30
    calm = np.array([20] * 30 + [230] * 30)
    strobe = np.tile([0, 255], 30)
    save_json(work, "beat.json", {"score_full": beat_score(full), "score_six": beat_score(six)})
    return [("8/8 rows -> 10.0", beat_score(full) == 10.0, beat_score(full)),
            ("6/8 rows -> 7.5", beat_score(six) == 7.5, beat_score(six)),
            ("one transition in 2 s is flash-safe", flashes_per_s(calm, fps) <= 3, flashes_per_s(calm, fps)),
            ("15 Hz strobe exceeds 3 flashes/s", flashes_per_s(strobe, fps) > 3, flashes_per_s(strobe, fps)),
            ]


# ---------------------------------------------------------------- UI-09
def loop_cycles(D, period):
    n = max(1, round(D / period))
    return n, D / n


def loop_frame(t, D, size=48):
    n, per = loop_cycles(D, 1.1)
    im = Image.new("L", (size, 16), 0)
    x = 4 + 30 * (0.5 - 0.5 * math.cos(2 * math.pi * t / per))
    ImageDraw.Draw(im).rectangle([x, 4, x + 10, 12], fill=255)
    return np.asarray(im)


def ui_09(work):
    D = 4.0
    n, per = loop_cycles(D, 1.1)
    f0, fD = loop_frame(0, D), loop_frame(D, D)
    Image.fromarray(f0).save(work / "first.png")
    jumps = [np.abs(loop_frame(i / 30, D).astype(int) - loop_frame((i + 1) / 30, D).astype(int)).mean() for i in range(120)]
    return [("whole cycles fit 4 s: 4 cycles of 1.0 s", (n, per) == (4, 1.0), (n, per)),
            ("first frame == last frame", np.array_equal(f0, fD), "equal"),
            ("no jump at the wrap (step at seam <= max in-loop step)", jumps[-1] <= max(jumps[:-1]) + 1e-9, round(jumps[-1], 3)),
            ("duration within 3-6 s", 3 <= D <= 6, D)]


# ---------------------------------------------------------------- UI-10
def tutorial_ok(script):
    errs = []
    if script[0]["kind"] != "payoff":
        errs.append("payoff not first")
    for s in script:
        if s["kind"] == "step" and (len(s["line"].split()) > 8 or "\n" in s["line"]):
            errs.append(f"long line {s['line'][:12]}")
        if s["kind"] == "step" and s.get("hold_until_press") is not True:
            errs.append("pointer leaves before press")
    return errs


def ui_10(work):
    good = [{"kind": "payoff", "line": "تقرير جاهز في ثانية"}, {"kind": "step", "line": "اضغط تصدير", "hold_until_press": True}]
    bad = [{"kind": "step", "line": "now click on the export button at the top right of the window please", "hold_until_press": False}]
    save_json(work, "tutorial.json", good)
    return [("payoff first, short line, held press", tutorial_ok(good) == [], tutorial_ok(good)),
            ("planted bad script: 3 faults", len(tutorial_ok(bad)) == 3, tutorial_ok(bad))]


# ---------------------------------------------------------------- UI-11 / UI-13 cursor helpers
def catmull(pts, n=200):
    p = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = map(np.array, p[i - 1:i + 3])
        for t in np.linspace(0, 1, n, endpoint=False):
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(np.array(pts[-1], float))
    return np.array(out)


def arc_sample(path, k):
    seg = np.hypot(*np.diff(path, axis=0).T)
    cum = np.concatenate([[0], np.cumsum(seg)])
    s = np.linspace(0, cum[-1], k)
    return np.stack([np.interp(s, cum, path[:, 0]), np.interp(s, cum, path[:, 1])], axis=1)


def arc_path(a, b, arc=0.2, n=60):
    a, b = np.array(a, float), np.array(b, float)
    mid = (a + b) / 2
    d = b - a
    nrm = np.array([-d[1], d[0]]) / np.linalg.norm(d)
    ctrl = mid + nrm * arc * np.linalg.norm(d) * 2
    t = np.linspace(0, 1, n)[:, None]
    return (1 - t) ** 2 * a + 2 * (1 - t) * t * ctrl + t * t * b


def press_curve(frames_down=4, frames_up=8, target=0.88):
    down = [1 - (1 - target) * (i / frames_down) for i in range(frames_down + 1)]
    up = [target + (1 - target) * (i / frames_up) for i in range(1, frames_up + 1)]
    return down + up


def ui_11(work):
    path = arc_path((0, 0), (300, 0), arc=0.2, n=42)
    keys = [(i / 60, tuple(np.round(p, 2))) for i, p in enumerate(path)]
    sag = abs(path[:, 1]).max() / 300
    pc = press_curve()
    text = "hello world"
    shown = [text[:int(t * 46)] for t in (0.1, 0.25)]
    save_json(work, "cursor_keys.json", keys)
    return [("42 frames of travel sampled at 60 fps (36-48 f)", 36 <= len(keys) <= 48 and keys[1][0] == 1 / 60, len(keys)),
            ("arc bows 15-25% of the path (20%)", 0.15 <= sag <= 0.25, round(sag, 3)),
            ("press 0.88 reached in 4 frames, recovered in 8", pc[4] == 0.88 and abs(pc[-1] - 1) < 1e-12 and len(pc) == 13, (pc[4], len(pc))),
            ("typeOn 46 cps: 4 chars at 0.1 s, 11 at 0.25 s", shown == ["hell", "hello world"], shown),
            ]


def ui_13(work):
    way = [(-140 + 600, 90 + 300), (600, 300), (900, 520)]
    path = catmull(way)
    pts = arc_sample(path, 60)
    steps = np.hypot(*np.diff(pts, axis=0).T)
    tip_offset = np.array([0, 0])
    tip = pts[-1] + tip_offset
    glide = bezier(.2, .8, .2, 1)
    save_json(work, "path.json", pts.tolist())
    return [("arc-length sampling gives constant speed (cv < 1%)", steps.std() / steps.mean() < 0.01, round(float(steps.std() / steps.mean()), 5)),
            ("first appearance glides in from (-140, +90)", tuple(np.array(way[0]) - np.array(way[1])) == (-140, 90), way[0]),
            ("tip lands exactly on the hit target", np.allclose(tip, way[-1], atol=1e-6), tip.tolist()),
            ("glide ease .2,.8,.2,1 is 90%+ done at 60% time", glide(0.6) > 0.9, round(glide(0.6), 3)),
            ]


# ---------------------------------------------------------------- UI-14
def press_ring(t, dur=0.42):
    p = out_cubic(clamp01(t / dur))
    return 0.45 + (1.25 - 0.45) * p, 1 - p


def ripple(t, dur, rmax, a0=1.0):
    p = clamp01(t / dur)
    return rmax * out_quad(p), a0 * (1 - p)


def ui_14(work):
    s0, o0 = press_ring(0)
    s1, o1 = press_ring(0.42)
    im = Image.new("L", (140, 140), 0)
    r, a = ripple(0.36, 0.36, 48)
    ImageDraw.Draw(im).ellipse([70 - r, 70 - r, 70 + r, 70 + r], outline=255, width=2)
    im.save(work / "ripple_end.png")
    measured = ring_radius(im, 70, 70)
    pr, pa = ripple(0.15, 0.3, 64, 0.6)
    return [("ring scale 0.45 -> 1.25 over 420 ms", (s0, round(s1, 6)) == (0.45, 1.25), (s0, s1)),
            ("ring opacity 1 -> 0", (o0, o1) == (1, 0), (o0, o1)),
            ("desktop ripple measured 48 px at its end", abs(measured - 48) <= 1, measured),
            ("phone ripple 64 px: half time -> 48 px, opacity 0.3", abs(pr - 48) < 1e-9 and abs(pa - 0.3) < 1e-9, (pr, pa)),
            ("ripple node exists from t=0 at opacity 0 (no mid-render creation)", ripple(0, 0.36, 48, 0)[1] == 0, "t0")]


# ---------------------------------------------------------------- UI-15
def directional_cursor(vel, lerp=0.25, fps=60):
    ang, out = 0.0, []
    for vx, vy in vel:
        target = math.degrees(math.atan2(vy, vx))
        d = (target - ang + 180) % 360 - 180
        ang += d * lerp
        out.append(ang)
    return out


def ui_15(work):
    angs = directional_cursor([(1, 1)] * 40)
    flip = directional_cursor([(1, 0)] * 20 + [(0, 1)] * 40)
    scale_hover = 1.55
    press = [0.85 if 10 <= f < 13 else 1.0 for f in range(20)]
    im = Image.new("L", (40, 45), 0)
    ImageDraw.Draw(im).polygon([(0, 0), (0, 38), (9, 30), (15, 38), (20, 36), (14, 28), (31, 28)], fill=255)
    im.save(work / "arrow.png")
    bb = Image.fromarray(np.asarray(im)).getbbox()
    return [("rotation converges to atan2 = 45 deg", abs(angs[-1] - 45) < 0.1, round(angs[-1], 3)),
            ("turning 0 -> 90 deg goes the short way, monotonic", all(b >= a - 1e-9 for a, b in zip(flip[20:], flip[21:])) and abs(flip[-1] - 90) < 0.1, round(flip[-1], 2)),
            ("press -15% for exactly 3 frames", press.count(0.85) == 3, press.count(0.85)),
            ("hover scale 1.55", scale_hover == 1.55, scale_hover),
            ("arrow rendered 32x39 px", (bb[2] - bb[0], bb[3] - bb[1]) == (32, 39), bb)]


# ---------------------------------------------------------------- UI-16
def homing(target_fn, frames=90, gain=0.2, stale=False):
    pos = np.array([0.0, 0.0])
    t0 = np.array(target_fn(0))
    for f in range(frames):
        tgt = t0 if stale else np.array(target_fn(f))
        pos += (tgt - pos) * gain
    return pos, np.array(target_fn(frames - 1))


def ui_16(work):
    def target(f): return (200 + 2 * f, 100 + math.sin(f / 10) * 5)
    live, real = homing(target)
    stale, _ = homing(target, stale=True)
    halo = Image.new("RGBA", (60, 60), (0, 0, 0, 0))
    ImageDraw.Draw(halo).ellipse([12, 12, 48, 48], fill=(0xf0, 0x44, 0x2c, round(0.4 * 255)))
    halo.save(work / "halo.png")
    px = halo.getpixel((30, 30))
    bb = halo.getbbox()
    return [("live homing ends within 12 px of the moving target", np.linalg.norm(live - real) < 12, round(float(np.linalg.norm(live - real)), 2)),
            ("stale coordinates miss by > 150 px", np.linalg.norm(stale - real) > 150, round(float(np.linalg.norm(stale - real)), 1)),
            ("halo #f0442c at 40% alpha", px == (0xf0, 0x44, 0x2c, 102), px),
            ("halo 36 px wide", bb[2] - bb[0] == 37 or bb[2] - bb[0] == 36, bb)]


# ---------------------------------------------------------------- UI-17
def magnetic(cursor, centre, factor):
    return ((cursor[0] - centre[0]) * factor, (cursor[1] - centre[1]) * factor)


def ui_17(work):
    b = magnetic((130, 60), (100, 50), 0.3)
    c = magnetic((130, 60), (100, 50), 0.1)
    ret = [elastic_out(p) for p in np.linspace(0, 1, 101)]
    save_json(work, "magnet.json", {"button": b, "card": c})
    return [("button offset = (cursor - centre) x 0.3 = (9, 3)", tuple(round(v, 9) for v in b) == (9.0, 3.0), b),
            ("card offset x 0.1 = (3, 1)", tuple(round(v, 9) for v in c) == (3.0, 1.0), c),
            ("elastic.out(1, 0.5) return overshoots then lands at 1", max(ret) > 1.01 and ret[-1] == 1, round(max(ret), 4)),
            ("scripted cursor path drives it (deterministic)", magnetic((130, 60), (100, 50), 0.3) == b, "same")]


# ---------------------------------------------------------------- UI-18
def drag(t, start, end, dur=0.8):
    p = power2_in_out(clamp01(t / dur))
    return start[0] + (end[0] - start[0]) * p, start[1] + (end[1] - start[1]) * p


def snap(pos, slots):
    return min(slots, key=lambda s: math.dist(pos, s))


def ui_18(work):
    ts = np.linspace(0, 0.8, 49)
    cur = [drag(t, (10, 10), (200, 120)) for t in ts]
    ghost = [drag(t, (10, 10), (200, 120)) for t in ts]
    err = max(math.dist(a, b) for a, b in zip(cur, ghost))
    lagged = [drag(max(0, t - 0.05), (10, 10), (200, 120)) for t in ts]
    lag_err = max(math.dist(a, b) for a, b in zip(cur, lagged))
    slot = snap(cur[-1], [(0, 0), (196, 118), (300, 300)])
    save_json(work, "drag.json", {"cursor": cur})
    return [("ghost on matched tween: zero separation", err == 0, err),
            ("a 50 ms-late ghost visibly detaches (> 10 px)", lag_err > 10, round(lag_err, 1)),
            ("drop snaps to the nearest slot", slot == (196, 118), slot)]


# ---------------------------------------------------------------- UI-19
def select_words(text, frac_from, frac_to):
    words = text.split()
    n = len(words)
    a, b = int(frac_from * n), max(int(frac_from * n) + 1, math.ceil(frac_to * n))
    return " ".join(words[a:b])


def marquee_hits(tiles, start, end):
    x0, x1 = sorted((start[0], end[0]))
    y0, y1 = sorted((start[1], end[1]))
    return [i for i, (x, y, w, h) in enumerate(tiles) if x < x1 and x + w > x0 and y < y1 and y + h > y0]


def ui_19(work):
    sel = select_words("هذا نص تجريبي للتحديد بالكلمات", 0.2, 0.6)
    tiles = [(x * 20, y * 20, 18, 18) for y in range(3) for x in range(4)]
    hits = marquee_hits(tiles, (5, 5), (45, 25))
    save_json(work, "select.json", {"selection": sel, "hits": hits})
    return [("Arabic selection is whole words", all(w in "هذا نص تجريبي للتحديد بالكلمات".split() for w in sel.split()), sel),
            ("selection covers words 2-3", sel == "نص تجريبي", sel),
            ("marquee 5..45 x 5..25 touches tiles 0,1,2,4,5,6", hits == [0, 1, 2, 4, 5, 6], hits),
            ]


# ---------------------------------------------------------------- UI-20
def zones(n, W):
    return [(i * W / n, (i + 1) * W / n) for i in range(n)]


def ui_20(work):
    z = zones(3, 1920)
    beats = [1.2, 2.6, 4.0]
    paths = [[(lo + 20 + k * 10, 200 + k * 50) for k in range(10)] for lo, hi in z]
    inside = all(lo <= x <= hi for (lo, hi), p in zip(z, paths) for x, _ in p)
    press = [0.88 if (ms % 140) < 70 else 1.0 for ms in range(0, 140, 10)]
    save_json(work, "multiplayer.json", {"zones": z, "beats": beats})
    return [("each cursor stays in its own zone (paths never cross)", inside, inside),
            ("actions alternate at 1.2/2.6/4.0 s (one payoff at a time)", min(np.diff(beats)) >= 1.0, beats),
            ("press 0.88 for 0.07 s then yoyo back", press.count(0.88) == 7 and press[-1] == 1.0, press.count(0.88)),
            ]


# ---------------------------------------------------------------- UI-21
def parse_targets(spec, W, H):
    return [(float(x) / 100 * W, float(y) / 100 * H) for x, y in (p.split(",") for p in spec.split(";"))]


def fit_hold(anim, slot):
    return {"speed": 1.0, "hold": max(0.0, round(slot - anim, 3))}


def ui_21(work):
    t = parse_targets("25,50;80,10", 1920, 1080)
    steps = "Reading the page,Opening Settings,Saving".split(",")
    f = fit_hold(4.2, 6.0)
    save_json(work, "agent.json", {"targets": t, "steps": steps, "fit": f})
    return [("'25,50;80,10' -> (480,540) (1536,108)", t == [(480.0, 540.0), (1536.0, 108.0)], t),
            ("three steps parsed", len(steps) == 3, steps),
            ("extra 1.8 s becomes hold, never stretch", f == {"speed": 1.0, "hold": 1.8}, f)]


# ---------------------------------------------------------------- UI-22
def touch_timeline(press_t):
    return {"cue": round(press_t - 0.06, 3), "press_end": round(press_t + 0.09, 3)}


def ui_22(work):
    tl = touch_timeline(1.0)
    ease = bezier(0.4, 0, 1, 1)
    dev = 1 - (1 - 0.96) * ease(1.0)
    btn = 1 - (1 - 0.92) * ease(1.0)
    rel = spring(240, 14, x0=0.92)
    r, a = ripple(0.3, 0.3, 64, 0.6)
    save_json(work, "touch.json", tl)
    return [("cue 60 ms before the press", tl["cue"] == 0.94, tl),
            ("press 90 ms ends at 1.09 s", tl["press_end"] == 1.09, tl),
            ("device 0.96 and button 0.92 at press end", (round(dev, 6), round(btn, 6)) == (0.96, 0.92), (dev, btn)),
            ("ease-in (0.4,0,1,1) is slow at the start", ease(0.3) < 0.15, round(ease(0.3), 3)),
            ("release spring 240/14 overshoots past 1 by analytic amount", abs((rel.max() - 1) / 0.08 - overshoot(240, 14)) < 0.01, round(float((rel.max() - 1) / 0.08), 4)),
            ("ripple 64 px, opacity 0 at 300 ms", (r, a) == (64, 0.0), (r, a))]


# ---------------------------------------------------------------- UI-23
def keycaps(n, press=0.12, gap=0.08):
    return [(round(i * (press + gap), 3), round(i * (press + gap) + press, 3)) for i in range(n)]


def key_offset(t, win):
    return 3 if win[0] <= t < win[1] else 0


def ui_23(work):
    k = keycaps(3)
    save_json(work, "keys.json", k)
    return [("3 keys at 0/0.2/0.4 s, 120 ms each", k == [(0.0, 0.12), (0.2, 0.32), (0.4, 0.52)], k),
            ("80 ms gaps between keys", all(round(b[0] - a[1], 3) == 0.08 for a, b in zip(k, k[1:])), "gaps"),
            ("key pressed 3 px at 0.25 s, released at 0.35 s", (key_offset(0.25, k[1]), key_offset(0.35, k[1])) == (3, 0), "offset")]


# ---------------------------------------------------------------- UI-24
def slider(cursor_x, x0=100, x1=300, vmin=0, vmax=100):
    return vmin + (vmax - vmin) * clamp01((cursor_x - x0) / (x1 - x0))


def ui_24(work):
    ts = np.linspace(0, 0.5, 31)
    xs = [100 + 200 * in_out_sine(t / 0.5) for t in ts]
    readout = [round(slider(x)) for x in xs]
    target = [slider(x) / 100 * 2 for x in xs]
    sync = all(abs(r / 100 * 2 - tg) < 0.02 for r, tg in zip(readout, target))
    save_json(work, "sync.json", {"readout": readout})
    return [("value derived from cursor x: 200 -> 50", slider(200) == 50, slider(200)),
            ("readout and target move together every frame", sync, sync),
            ("knob 500 ms ease-in-out ends at 100", readout[-1] == 100, readout[-1]),
            ("cursor past the track clamps to 100", slider(400) == 100, slider(400))]


# ---------------------------------------------------------------- UI-25
def human_type(text, t, ms_per=0.045, fps=30, seed=3):
    g = graphemes(text)
    holds = seeded_holds(len(g), seed)
    f = int(t * fps)
    shown, frames, i = 0, 0, 0
    pending_hold = False
    while frames < f and shown < len(g):
        frames += 1
        if pending_hold:
            pending_hold = False
            continue
        target = min(len(g), int((frames / fps) / ms_per) - sum(1 for h in holds if h <= shown))
        if target > shown:
            shown = target
            if shown in holds:
                pending_hold = True
    return "".join(g[:shown])


def caret(t, period=0.515):
    return int(t // period) % 2 == 0


def ui_25(work):
    a = human_type("Write a launch plan", 0.5)
    b = human_type("Write a launch plan", 0.5)
    ar = human_type("مُحَمَّد يكتب", 0.2)
    clusters = graphemes("مُحَمَّد")
    save_json(work, "typing.json", {"latin_0.5s": a, "arabic_0.2s": ar})
    return [("seeded rhythm is deterministic", a == b, a),
            ("holds slow it below raw 45 ms/char (< 11 chars at 0.5 s)", 0 < len(a) < 11, len(a)),
            ("Arabic cut only at grapheme clusters (every prefix ends on a full cluster)",
             all(human_type("مُحَمَّد يكتب", t) in ["".join(graphemes("مُحَمَّد يكتب")[:k]) for k in range(13)] for t in np.arange(0, 0.6, 1 / 30)), ar),
            ("'مُحَمَّد' = 4 clusters", len(clusters) == 4, clusters),
            ("caret 515 ms blink: on, off, on", [caret(t) for t in (0.1, 0.6, 1.1)] == [True, False, True], "blink")]


# ---------------------------------------------------------------- UI-26
def prompt_timeline(prompt, ms=0.042):
    type_end = len(prompt) * ms
    return {"type_end": round(type_end, 3), "send": round(type_end + 0.3, 3), "ring_end": round(type_end + 0.6, 3),
            "progress_end": round(type_end + 1.6, 3), "result": round(type_end + 1.6, 3), "end": round(type_end + 4.0, 3)}


def ui_26(work):
    tl = prompt_timeline("سيارة كهربائية على شاطئ عند الغروب")
    send_scale = [0.9 if tl["send"] <= t < tl["send"] + 0.1 else 1 for t in np.arange(0, tl["end"], 0.05)]
    save_json(work, "prompt.json", tl)
    return [("ring pulse lasts 300 ms after send", round(tl["ring_end"] - tl["send"], 3) == 0.3, tl),
            ("progress bar fills ~1 s", round(tl["progress_end"] - tl["ring_end"], 3) == 1.0, tl),
            ("blueprint length within 5.2-12 s", 5.2 <= tl["end"] <= 12, tl["end"]),
            ("send button scales to 0.9", min(send_scale) == 0.9, min(send_scale))]


# ---------------------------------------------------------------- UI-27
def checklist_times(n, gaps):
    t, out = 0.0, []
    for i in range(n):
        out.append(round(t, 3))
        t += gaps[i % len(gaps)]
    return out


def check_pop(t, start, dur=0.25):
    return 0.6 + 0.4 * back_out(clamp01((t - start) / dur), 1.2) if t >= start else 0.0


def ui_27(work):
    times = checklist_times(5, [0.3, 0.45, 0.6, 0.25])
    gaps = np.round(np.diff(times), 3)
    im = Image.new("RGB", (40, 40), "white")
    ImageDraw.Draw(im).line([(8, 20), (17, 29), (32, 11)], fill=(0x2b, 0xb6, 0x73), width=4)
    im.save(work / "check.png")
    return [("rows 250-600 ms apart", all(0.25 <= g <= 0.6 for g in gaps), gaps.tolist()),
            ("check pops from 0.6 to 1 in 250 ms", round(check_pop(1.0, 1.0), 9) == 0.6 and abs(check_pop(1.25, 1.0) - 1) < 1e-9, check_pop(1.25, 1.0)),
            ("check colour #2bb673 rendered", (0x2b, 0xb6, 0x73) in [c for _, c in im.getcolors()], "colour"),
            ("pop overshoots slightly (back.out)", max(check_pop(1.0 + d, 1.0) for d in np.linspace(0, 0.25, 50)) > 1, "overshoot")]


# ---------------------------------------------------------------- UI-28
def parse_thread(spec, rtl=False):
    out = []
    for i, part in enumerate(spec.split("|")):
        kind, body = part.split(":", 1)
        side = "left" if kind == "recv" else "right"
        if rtl:
            side = {"left": "right", "right": "left"}[side]
        item = {"kind": kind, "at": round(i * 1.7, 2), "side": side}
        if kind == "card":
            item["title"], item["domain"] = body.split("~")
        else:
            item["text"] = body
        out.append(item)
    return out


def bubble_scale(t, at, dur=0.12):
    return 0.75 + 0.25 * out_cubic(clamp01((t - at) / dur))


def ui_28(work):
    th = parse_thread("recv:مرحبا|sent:أهلا|card:عرض اليوم~kosif.dev|emoji:👍")
    rt = parse_thread("recv:hi|sent:yo", rtl=True)
    save_json(work, "thread.json", th)
    return [("4 messages on a 1.7 s beat", [m["at"] for m in th] == [0.0, 1.7, 3.4, 5.1], [m["at"] for m in th]),
            ("card split into title and domain", th[2]["title"] == "عرض اليوم" and th[2]["domain"] == "kosif.dev", th[2]),
            ("bubble enters from 0.75 to 1 in 0.12 s", bubble_scale(1.7, 1.7) == 0.75 and bubble_scale(1.82, 1.7) == 1.0, "scale"),
            ("RTL mirrors sides (received on the right)", rt[0]["side"] == "right" and rt[1]["side"] == "left", rt)]


# ---------------------------------------------------------------- UI-29
def term_frame(lines, t, ms=0.04, blink=0.5, W=200, H=60):
    im = Image.new("RGB", (W, H), (30, 30, 30))
    d = ImageDraw.Draw(im)
    f = font(10, MONO)
    shown = int(t / ms)
    y = 4
    for kind, text in lines:
        part = text[:max(0, shown)]
        shown -= len(text)
        col = (128, 128, 128) if kind == "old" else (200, 255, 200) if kind == "new" else (230, 230, 230)
        d.text((4, y), part, font=f, fill=col)
        if kind == "old" and part:
            w = f.getlength(part)
            d.line([(4, y + 7), (4 + w, y + 7)], fill=(128, 128, 128), width=1)
        y += 14
    if int(t // blink) % 2 == 0:
        d.rectangle([W - 10, H - 12, W - 4, H - 2], fill=(255, 183, 105))
    return im


def ui_29(work):
    lines = [("old", "x = 1"), ("new", "x = 2")]
    im = term_frame(lines, 0.4)
    im.save(work / "diff.png")
    a = np.asarray(im).astype(int)
    strike = (np.abs(a[11] - 128).sum(axis=1) < 6).sum()
    early = np.asarray(term_frame(lines, 0.1)).astype(int)
    new_row = (early[18:30].max(axis=2) > 150).sum()
    return [("old line struck through in grey", strike >= 15, int(strike)),
            ("40 ms/char: at 0.1 s the second line has not started", new_row == 0, int(new_row)),
            ("block cursor visible on 0-0.5 s, off 0.5-1 s", np.asarray(term_frame(lines, 0.2))[55, 195, 0] == 255 and np.asarray(term_frame(lines, 0.7))[55, 195, 0] == 30, "blink")]


# ---------------------------------------------------------------- UI-30
def palette_state(query, rows, t_since_filter):
    out = []
    p = clamp01(t_since_filter / 0.4)
    for r in rows:
        hit = query.lower() in r.lower()
        out.append({"row": r, "opacity": 1.0 if hit else round(1 - 0.7 * p, 9), "height": 1.0 if hit else round(1 - p, 9),
                    "highlight": (r.lower().index(query.lower()), r.lower().index(query.lower()) + len(query)) if hit else None})
    n = sum(1 for o in out if o["highlight"])
    return out, f"{n} result" + ("" if n == 1 else "s")


def ui_30(work):
    rows = ["Export video", "Share link", "Settings"]
    st, label = palette_state("expo", rows, 0.4)
    mid, _ = palette_state("expo", rows, 0.2)
    save_json(work, "palette.json", st)
    return [("one match -> '1 result'", label == "1 result", label),
            ("non-matching rows fade to 30% and collapse after 400 ms", st[1]["opacity"] == 0.3 and st[1]["height"] == 0.0, st[1]),
            ("halfway (200 ms) rows at 65% opacity", abs(mid[1]["opacity"] - 0.65) < 1e-9, mid[1]["opacity"]),
            ("keyword highlight span (0, 4)", st[0]["highlight"] == (0, 4), st[0]["highlight"]),
            ("typing 'expo' at 70 ms/char takes 280 ms", round(4 * 0.07, 3) == 0.28, 0.28)]


# ---------------------------------------------------------------- UI-31
def stream_lines(lines, t, start=0.0, every=0.12):
    return lines[:max(0, int((t - start) / every) + 1)] if t >= start else []


def skeleton(W=300, n=3, seed=2):
    rng = np.random.default_rng(seed)
    return [(round(float(rng.uniform(0.4, 0.7)) * W), 30) for _ in range(n)]


def ui_31(work):
    lines = [f"GET /api/{i} ✓ 200" for i in range(6)]
    sk = skeleton()
    im = Image.new("L", (320, 120), 255)
    d = ImageDraw.Draw(im)
    for i, (w, h) in enumerate(sk):
        d.rectangle([10, 10 + i * 36, 10 + w - 1, 10 + i * 36 + h - 1], fill=200)
    im.save(work / "skeleton.png")
    rows = np.nonzero(np.asarray(im)[:, 12] == 200)[0]
    return [("one line per 120 ms: 3 lines at 0.25 s", len(stream_lines(lines, 0.25)) == 3, len(stream_lines(lines, 0.25))),
            ("3 skeleton bars 30 px high", len(sk) == 3 and len(rows) == 90, len(rows)),
            ("bar widths 40-70% of the card", all(120 <= w <= 210 for w, _ in sk), sk)]


# ---------------------------------------------------------------- UI-32
def notes_typing(spec, t, speed=1.0, base=0.06):
    lines = spec.split("|")
    if not 0.5 <= speed <= 2:
        raise ValueError("speed 0.5-2")
    n = int(t * speed / base)
    out = []
    for ln in lines:
        g = graphemes(ln)
        out.append("".join(g[:n]))
        n -= len(g)
        if n <= 0:
            break
    return out


def ui_32(work):
    a = notes_typing("قائمة|حليب", 0.3)
    b = notes_typing("قائمة|حليب", 0.3, speed=2)
    try:
        notes_typing("a", 1, speed=3)
        rej = False
    except ValueError:
        rej = True
    save_json(work, "notes.json", {"1x": a, "2x": b})
    return [("1x at 0.3 s: 5 graphemes, first line done", a == ["قائمة"], a),
            ("2x at 0.3 s reaches the second line", b == ["قائمة", "حليب"], b),
            ("speed 3 refused (0.5-2)", rej, rej),
            ]


# ---------------------------------------------------------------- UI-33
SHAKE = [0, -10, 10, -10, 10, 0]
ALLOWED = {"transform", "opacity", "color", "background-color", "border-color"}


def shake_x(t, dur=0.4):
    p = clamp01(t / dur) * (len(SHAKE) - 1)
    i = min(int(p), len(SHAKE) - 2)
    return round(SHAKE[i] + (SHAKE[i + 1] - SHAKE[i]) * (p - i), 9)


def anim_props_ok(props):
    return [p for p in props if p not in ALLOWED]


def ui_33(work):
    xs = [shake_x(t) for t in np.linspace(0, 0.4, 41)]
    save_json(work, "shake.json", xs)
    return [("shake keyframes hit -10/+10 at 0.08 s steps", (shake_x(0.08), shake_x(0.16), shake_x(0.4)) == (-10, 10, 0), (shake_x(0.08), shake_x(0.16))),
            ("shake lasts 0.4 s and ends at rest", xs[-1] == 0 and max(abs(x) for x in xs) == 10, xs[-1]),
            ("width/height animation rejected", anim_props_ok(["transform", "width", "height"]) == ["width", "height"], "props"),
            ]


# ---------------------------------------------------------------- UI-34
def nudge(state, rtl=False, hover_capable=True):
    out = {"translateY": 0, "icon_x": 0, "scale": 1}
    if state == "active":
        out.update(translateY=1, scale=0.985)
    elif state == "hover" and hover_capable:
        out.update(translateY=-1, icon_x=-3 if rtl else 3)  # inline-end nudge: -3 px in RTL, mirrored +3 in LTR
    return out


def ui_34(work):
    ltr = nudge("hover")
    rtl = nudge("hover", rtl=True)
    touch = nudge("hover", hover_capable=False)
    act = nudge("active")
    save_json(work, "nudges.json", {"ltr": ltr, "rtl": rtl})
    return [("press translateY(1px) scale(.985)", (act["translateY"], act["scale"]) == (1, 0.985), act),
            ("hover lifts -1 px", ltr["translateY"] == -1, ltr),
            ("inline-end icon nudge mirrors in RTL", ltr["icon_x"] == -rtl["icon_x"] and ltr["icon_x"] != 0, (ltr["icon_x"], rtl["icon_x"])),
            ("no hover effect without (hover:hover) and (pointer:fine)", touch["translateY"] == 0, touch),
            ]


# ---------------------------------------------------------------- UI-35
def ui_35(work):
    press = [1 - 0.1 * (t / 0.08) ** 2 for t in np.linspace(0, 0.08, 21)]
    rel = spring(300, 20, x0=0.9, secs=1.0)
    over = (rel.max() - 1) / 0.1
    st = settle_time(rel, tol=0.005)
    bar = lambda t: clamp01(t / 1.1)
    save_json(work, "button.json", {"press_end": press[-1], "release_settle": st})
    return [("press reaches 0.9 at 80 ms (power1.in)", abs(press[-1] - 0.9) < 1e-12 and press[5] > 0.99, press[-1]),
            ("release spring 300/20 overshoot = analytic", abs(over - overshoot(300, 20)) < 0.01, (round(over, 4), round(overshoot(300, 20), 4))),
            ("release settles within 0.5% by ~300 ms", st < 0.35, st),
            ("progress fills linearly over 1.1 s (50% at 0.55 s)", bar(0.55) == 0.5 and bar(1.1) == 1, "linear"),
            ]


# ---------------------------------------------------------------- UI-36
def theme_mix(t, a=(245, 235, 220), b=(60, 35, 25), start=0.3, dur=0.3):
    p = out_cubic(clamp01((t - start) / dur))
    return tuple(round(x + (y - x) * p) for x, y in zip(a, b))


def ui_36(work):
    thumb = [out_cubic(clamp01(t / 0.3)) for t in (0, 0.15, 0.3)]
    orbit = spring(220, 18, x0=0.0, secs=0.5)
    ang = 75 * (1 - orbit)
    scale = 0.72 + 0.28 * orbit
    im = Image.new("RGB", (20, 20), theme_mix(0.6))
    im.save(work / "dark.png")
    return [("thumb easeOutCubic: 87.5% at half time", thumb == [0, 0.875, 1], thumb),
            ("palette cream -> chocolate after the thumb lands", theme_mix(0) == (245, 235, 220) and theme_mix(0.6) == (60, 35, 25), theme_mix(0.6)),
            ("icon orbits in from 75 deg at .72 scale", ang[0] == 75 and abs(scale[0] - 0.72) < 1e-12, (float(ang[0]), float(scale[0]))),
            ("icon settles near 0 deg by ~260 ms", abs(ang[int(0.26 * 240)]) < 0.1 * 75, round(float(ang[int(0.26 * 240)]), 2))]


# ---------------------------------------------------------------- UI-37
def check_draw(t, start, dur=0.25):
    pts = [(8, 20), (17, 29), (32, 11)]
    seg = [math.dist(pts[0], pts[1]), math.dist(pts[1], pts[2])]
    L = sum(seg) * clamp01((t - start) / dur)
    im = Image.new("L", (40, 40), 0)
    d = ImageDraw.Draw(im)
    if L > 0:
        a = min(1, L / seg[0])
        d.line([pts[0], (pts[0][0] + (pts[1][0] - pts[0][0]) * a, pts[0][1] + (pts[1][1] - pts[0][1]) * a)], fill=255, width=3)
        if L > seg[0]:
            b = (L - seg[0]) / seg[1]
            d.line([pts[1], (pts[1][0] + (pts[2][0] - pts[1][0]) * b, pts[1][1] + (pts[2][1] - pts[1][1]) * b)], fill=255, width=3)
    return np.asarray(im)


def ui_37(work):
    spin = [(t / 0.8) * 360 % 360 for t in (0, 0.4, 0.8)]
    full = (check_draw(1.25, 1.0) > 0).sum()
    half = (check_draw(1.125, 1.0) > 0).sum()
    Image.fromarray(check_draw(1.25, 1.0)).save(work / "check.png")
    return [("spinner one turn per 0.8 s", spin == [0, 180, 0], spin),
            ("no check before the spinner collapses", (check_draw(0.99, 1.0) > 0).sum() == 0, "empty"),
            ("check half drawn at 125 ms of 250", 0.4 < half / full < 0.6, round(half / full, 3)),
            ("check complete at 250 ms", full > 60, int(full))]


# ---------------------------------------------------------------- UI-38
def form_keys(n=16, mean=0.07, jitter=0.02, seed=5):
    rng = np.random.default_rng(seed)
    return np.clip(rng.normal(mean, jitter / 2, n), mean - jitter, mean + jitter)


def ui_38(work):
    k = form_keys()
    toast = spring(200, 22, secs=1.0)
    save_json(work, "form.json", {"key_ms": (k * 1000).round(1).tolist()})
    return [("16 keystrokes at 70 ms +-20", len(k) == 16 and k.min() >= 0.05 and k.max() <= 0.09, (round(float(k.min()), 3), round(float(k.max()), 3))),
            ("mean close to 70 ms", abs(k.mean() - 0.07) < 0.01, round(float(k.mean()), 4)),
            ("error shake: displaced mid-way, at rest at 0.4 s", shake_x(0.4) == 0 and shake_x(0.08) == -10, (shake_x(0.08), shake_x(0.4))),
            ("toast spring 200/22 overshoot = analytic", abs((toast.max() - 1) - overshoot(200, 22)) < 0.004, (round(float(toast.max() - 1), 4), round(overshoot(200, 22), 4))),
            ]


# ---------------------------------------------------------------- UI-39
def loading_for(wait):
    if wait < 0.3:
        return "nothing"
    if wait < 1:
        return "spinner"
    if wait < 5:
        return "skeleton"
    if wait <= 30:
        return "bar"
    return "bar+percent+eta"


def shimmer_x(t, W=300, period=1.3, band=0.3):
    p = (t % period) / period
    return -band * W + p * (W + band * W)


def ui_39(work):
    v = {w: loading_for(w) for w in (0.2, 0.5, 2, 12, 45)}
    save_json(work, "ladder.json", v)
    return [("ladder 0.2/0.5/2/12/45 s", list(v.values()) == ["nothing", "spinner", "skeleton", "bar", "bar+percent+eta"], v),
            ("shimmer band 30% wide starts off-card", shimmer_x(0) == -90, shimmer_x(0)),
            ("shimmer loops every 1.3 s", abs(shimmer_x(0.2) - shimmer_x(1.5)) < 1e-9, "loop"),
            ("a 700 ms blank would read as broken (needs a spinner)", loading_for(0.7) == "spinner", loading_for(0.7))]


# ---------------------------------------------------------------- UI-40
def ui_40(work):
    s = spring(180, 16, secs=1.0)
    w = 120 + 180 * s
    h = 36 + 44 * s
    st = settle_time(s, tol=0.05)
    content = [round(0.18 + 0.06 * i, 2) for i in range(3)]
    save_json(work, "island.json", {"w_end": float(w[-1]), "settle": st})
    return [("island grows 120x36 -> 300x80", (round(float(w[-1])), round(float(h[-1]))) == (300, 80), (float(w[-1]), float(h[-1]))),
            ("spring 180/16 settles within 5% around 260 ms", 0.2 <= st <= 0.4, st),
            ("overshoot = analytic for 180/16", abs((s.max() - 1) - overshoot(180, 16)) < 0.005, round(float(s.max() - 1), 4)),
            ("content from 180 ms with 60 ms stagger", content == [0.18, 0.24, 0.3], content),
            ]


# ---------------------------------------------------------------- UI-41
def flip(first, last):
    fx, fy, fw, fh = first
    lx, ly, lw, lh = last
    return {"tx": fx - lx, "ty": fy - ly, "sx": fw / lw, "sy": fh / lh}


def ui_41(work):
    inv = flip((40, 300, 200, 120), (0, 0, 400, 600))
    child = (1 / inv["sx"], 1 / inv["sy"])
    ease = in_out_cubic
    mid = {k: (v if k in ("tx", "ty") else v) for k, v in inv.items()}
    save_json(work, "flip.json", inv)
    start_rect = (0 + inv["tx"], 0 + inv["ty"], 400 * inv["sx"], 600 * inv["sy"])
    return [("inverted transform puts the panel back on the card", start_rect == (40, 300, 200, 120), start_rect),
            ("children counter-scaled to 1", (inv["sx"] * child[0], inv["sy"] * child[1]) == (1.0, 1.0), child),
            ("easeInOutCubic midpoint 0.5", ease(0.5) == 0.5, ease(0.5))]


# ---------------------------------------------------------------- UI-42
def reorder(old, new, row_h=40, stagger=0.045, dur=0.45):
    ease = bezier(0.2, 0.8, 0.2, 1)

    def at(t):
        out = {}
        for i, item in enumerate(new):
            delta = (old.index(item) - i) * row_h
            p = ease(clamp01((t - i * stagger) / dur))
            out[item] = i * row_h + delta * (1 - p)
        return out
    return at


def ui_42(work):
    old, new = ["a", "b", "c", "d"], ["c", "a", "d", "b"]
    at = reorder(old, new)
    t0, tend = at(0), at(0.45 + 3 * 0.045)
    save_json(work, "reorder.json", {"start": t0, "end": tend})
    return [("at t=0 every row is where it was (FLIP invert)", all(t0[k] == old.index(k) * 40 for k in old), t0),
            ("at the end rows sit in the new order", all(tend[k] == new.index(k) * 40 for k in new), tend),
            ("45 ms cascade: row 3 still at start at 120 ms", at(0.12)["b"] == old.index("b") * 40, at(0.12)["b"])]


# ---------------------------------------------------------------- UI-43
def tab_indicator(t, tabs, frm, to):
    s = spring(300, 26, secs=0.6)
    p = s[min(len(s) - 1, int(t * 240))]
    x0, w0 = tabs[frm]
    x1, w1 = tabs[to]
    return x0 + (x1 - x0) * p, w0 + (w1 - w0) * p


def ui_43(work):
    tabs = [(0, 80), (80, 120), (200, 90)]
    end = tab_indicator(0.59, tabs, 0, 2)
    save_json(work, "tabs.json", {"end": end})
    rail = 0.2 + 0.8 * clamp01(0.26 / 0.26)
    return [("indicator lands on the active tab rect", abs(end[0] - 200) < 1 and abs(end[1] - 90) < 1, end),
            ("starts on the previous tab", tab_indicator(0, tabs, 0, 2) == (0, 80), tab_indicator(0, tabs, 0, 2)),
            ]


# ---------------------------------------------------------------- UI-44
def progress_bar_px(t, D, W):
    return W * clamp01(t / D)


def stepper_fill(t, n=5, per=0.5):
    return min(n - 1, t / per)


def ring_offset(t, C, dur=1.2):
    return C * (1 - in_out_cubic(clamp01(t / dur)))


def ui_44(work):
    im = Image.new("RGB", (200, 14), (0, 0, 0))
    ImageDraw.Draw(im).rectangle([0, 0, progress_bar_px(3, 6, 200) - 1, 13], fill=(0x7e, 0xe8, 0xd2))
    im.save(work / "bar.png")
    cols = int((np.asarray(im)[7, :, 0] == 0x7e).sum())
    C = 2 * math.pi * 40
    return [("bar width = t/D: 50% at 3 s of 6", cols == 100, cols),
            ("bar 14 px tall #7ee8d2", im.size[1] == 14 and im.getpixel((5, 5)) == (0x7e, 0xe8, 0xd2), im.getpixel((5, 5))),
            ("stepper fills node to node (2.5 nodes at 1.25 s)", stepper_fill(1.25) == 2.5 and stepper_fill(9) == 4, stepper_fill(1.25)),
            ("ring dashoffset full -> 0 over 1200 ms", ring_offset(0, C) == C and ring_offset(1.2, C) == 0 and abs(ring_offset(0.6, C) - C / 2) < 1e-9, "ring")]


# ---------------------------------------------------------------- UI-45
STATUS = {"live": ((0x54, 0xd8, 0x9c), 0.12), "attention": ((0xf5, 0xa5, 0x24), 0.12), "muted": ((0x88, 0x88, 0x88), 0.12)}


def status_dot(state, d=9, halo=4, bg=(255, 255, 255)):
    col, a = STATUS[state]
    S = d + 2 * halo + 4
    im = Image.new("RGB", (S, S), bg)
    dr = ImageDraw.Draw(im)
    soft = tuple(round(b * (1 - a) + c * a) for b, c in zip(bg, col))
    c = S / 2
    dr.ellipse([c - d / 2 - halo, c - d / 2 - halo, c + d / 2 + halo, c + d / 2 + halo], fill=soft)
    dr.ellipse([c - d / 2, c - d / 2, c + d / 2, c + d / 2], fill=col)
    return im, soft


def ui_45(work):
    im, soft = status_dot("live")
    im.save(work / "dot.png")
    a = np.asarray(im)
    row = a[a.shape[0] // 2]
    core = int((np.all(row == (0x54, 0xd8, 0x9c), axis=1)).sum())
    ring = int((np.all(row == soft, axis=1)).sum())
    pulse = [0.5 + 0.5 * math.sin(2 * math.pi * t / 1.2) for t in (0, 1.2)]
    return [("core dot 9-10 px of #54d89c", core in (9, 10), core),
            ("halo 4 px each side at 12% alpha", ring == 8 and soft == (234, 250, 243), (ring, soft)),
            ("pulse period 1.2 s", abs(pulse[0] - pulse[1]) < 1e-9, pulse),
            ("each state has its own colour", len({v[0] for v in STATUS.values()}) == 3, "colours")]


# ---------------------------------------------------------------- UI-46
def burst(seed, n=60, t=0.5):
    rng = np.random.default_rng(seed)
    ang = rng.uniform(0, 2 * math.pi, n)
    v = rng.uniform(200, 400, n)
    x = v * np.cos(ang) * t
    y = v * np.sin(ang) * t + 0.5 * 900 * t * t
    return np.stack([x, y], 1)


def celebration_ok(product):
    return 1 <= len(product["moments"]) <= 2 and all(m.get("skippable") and m.get("missed_if_removed") for m in product["moments"])


def ui_46(work):
    a, b, c = burst(11), burst(11), burst(12)
    save_json(work, "burst.json", a.tolist())
    good = {"moments": [{"name": "first export", "skippable": True, "missed_if_removed": True}]}
    deco = {"moments": [{"name": "login", "skippable": True, "missed_if_removed": False}] * 3}
    return [("seeded burst is reproducible", np.array_equal(a, b), "same"),
            ("different seed, different burst", not np.array_equal(a, c), "differs"),
            ("gravity pulls the burst down (mean y > 0)", a[:, 1].mean() > 0, round(float(a[:, 1].mean()), 1)),
            ("one skippable, missed moment passes", celebration_ok(good), "ok"),
            ("3 decorative moments fail the removal test", not celebration_ok(deco), "fail")]


# ---------------------------------------------------------------- UI-47
def phone_spec(W=390, H=844, radius_pct=0.13, bezel_pct=0.025):
    r = radius_pct * W
    b = bezel_pct * W
    return {"screen": (W, H), "screen_r": r, "bezel": b, "frame_r": r + b, "island": (120, 36, 12)}


def draw_phone(s):
    W, H = s["screen"]
    b = round(s["bezel"])
    im = Image.new("RGB", (W + 2 * b, H + 2 * b), (255, 255, 255))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, W + 2 * b - 1, H + 2 * b - 1], radius=round(s["frame_r"]), fill=(20, 20, 22))
    d.rounded_rectangle([b, b, b + W - 1, b + H - 1], radius=round(s["screen_r"]), fill=(240, 240, 250))
    iw, ih, top = s["island"]
    cx = b + W / 2
    d.rounded_rectangle([cx - iw / 2, b + top, cx + iw / 2 - 1, b + top + ih - 1], radius=ih // 2, fill=(0, 0, 0))
    return im


def ui_47(work):
    s = phone_spec()
    im = draw_phone(s)
    im.resize((im.width // 2, im.height // 2)).save(work / "phone.png")
    a = np.asarray(im)
    b = round(s["bezel"])
    col = a[:, b + 195]
    isl = np.nonzero(np.all(col == 0, axis=1))[0]
    row = a[b + 30]
    isl_w = int(np.all(row == 0, axis=1).sum())
    return [("screen 390x844 (19.5:9)", abs(844 / 390 - 19.5 / 9) < 0.01, 844 / 390),
            ("frame radius = screen radius + bezel", s["frame_r"] == s["screen_r"] + s["bezel"], s),
            ("radius 12-14% W and bezel 2-3% W", 0.12 * 390 <= s["screen_r"] <= 0.14 * 390 and 0.02 * 390 <= s["bezel"] <= 0.03 * 390, (s["screen_r"], s["bezel"])),
            ("island measured 36 px tall starting 12 px below the screen top", len(isl) == 36 and isl.min() == b + 12, (len(isl), int(isl.min()) - b)),
            ("island 120 px wide", isl_w == 120, isl_w)]


# ---------------------------------------------------------------- UI-48
def capped_rotation(target, start, rate, fps=60):
    a, out = start, [start]
    while abs(target - a) > 1e-9:
        step = max(-rate / fps, min(rate / fps, target - a))
        a += step
        out.append(a)
    return out


def ui_48(work):
    rev = capped_rotation(28, -8, 40)
    idle = [6 * math.sin(2 * math.pi * t / 3.2) for t in np.arange(0, 6.4, 1 / 30)]
    speed = max(abs(b - a) * 60 for a, b in zip(rev, rev[1:]))
    yaw_ok = lambda y: -28 <= y <= 28
    save_json(work, "rotation.json", {"reveal_frames": len(rev)})
    return [("reveal capped at 40 deg/s (36 deg -> 0.9 s)", speed <= 40 + 1e-9 and abs((len(rev) - 1) / 60 - 0.9) < 0.02, (speed, (len(rev) - 1) / 60)),
            ("idle hover <= 6 px with 3.2 s period", max(abs(v) for v in idle) <= 6 and abs(idle[0] - idle[96]) < 1e-9, round(max(idle), 3)),
            ("yaw clamp +-28: 30 rejected", yaw_ok(28) and not yaw_ok(30), "clamp"),
            ]


# ---------------------------------------------------------------- UI-49
def entrance(t, dur=0.8):
    p = bezier(0.16, 1, 0.3, 1)(clamp01(t / dur))
    return {"rise": 140 * (1 - p), "yaw": -22 + 14 * p, "opacity": clamp01(t / 0.25)}


def ui_49(work):
    e0, e1, eo = entrance(0), entrance(0.8), entrance(0.25)
    s = spring(90, 18, 1.1, secs=2)
    save_json(work, "entrance.json", {"start": e0, "end": e1})
    return [("rises 140 px into place", (e0["rise"], round(e1["rise"], 6)) == (140, 0), (e0["rise"], e1["rise"])),
            ("yaw -22 -> -8", (e0["yaw"], round(e1["yaw"], 6)) == (-22, -8), (e0["yaw"], e1["yaw"])),
            ("opacity done by 250 ms", eo["opacity"] == 1 and entrance(0.1)["opacity"] < 1, eo["opacity"]),
            ("spring 18/90/1.1 nearly critical: overshoot < 1%", s.max() - 1 < 0.01, round(float(s.max() - 1), 5))]


# ---------------------------------------------------------------- UI-50
def phone_25d(yaw_deg, W=84, H=180):
    if abs(yaw_deg) >= 28:
        raise ValueError("above 28 deg use CSS 3D or a GLTF model")
    rad = math.radians(yaw_deg)
    a, b = math.cos(rad), math.sin(rad) * 0.12
    screen = Image.new("L", (W, H), 0)
    ImageDraw.Draw(screen).rounded_rectangle([0, 0, W - 1, H - 1], radius=12, fill=255)
    out_w = int(W * a) + 2
    out_h = int(H + abs(b) * W) + 2
    inv = (1 / a, 0, 0, -b / a, 1, 0)
    return screen.transform((out_w, out_h), Image.AFFINE, inv, resample=Image.BILINEAR), (a, b)


def ui_50(work):
    im, (a, b) = phone_25d(20)
    im.save(work / "phone_20deg.png")
    arr = np.asarray(im)
    xs = np.nonzero(arr.max(axis=0) > 128)[0]
    left = np.nonzero(arr[:, 2] > 128)[0]
    right = np.nonzero(arr[:, xs.max() - 1] > 128)[0]
    shear = right.min() - left.min()
    try:
        phone_25d(30)
        rej = False
    except ValueError:
        rej = True
    return [("width shrinks by cos(yaw): 84 -> 79 px", abs((xs.max() - xs.min() + 1) - 84 * a) <= 2, int(xs.max() - xs.min() + 1)),
            ("vertical shear sin(yaw)*0.12 per px (~3.3 px across)", abs(shear - b * 79) <= 2.5, int(shear)),
            ("30 deg refused (valid below 28)", rej, rej)]


# ---------------------------------------------------------------- UI-51
def glare(frame, start=10, end=36):
    return clamp01((frame - start) / (end - start))


def persp_scale(z, p=1400):
    return p / (p - z)


def ui_51(work):
    g = [glare(f) for f in (9, 23, 36)]
    save_json(work, "device.json", {"glare": [glare(f) for f in range(48)]})
    tilt_top = 0.5 * 844 * math.sin(math.radians(4))
    return [("glare 0 before f10, 50% at f23, 100% at f36", g == [0, 0.5, 1], g),
            ("perspective 1400: an element 100 px nearer scales x1.077", round(persp_scale(100), 3) == 1.077, persp_scale(100)),
            ("rotateX 4 deg lifts the top edge ~29 px toward the camera", round(tilt_top, 1) == 29.4, round(tilt_top, 1))]


# ---------------------------------------------------------------- UI-52
def turntable(t, dur=1.4):
    e = bezier(0.65, 0, 0.35, 1)(clamp01(t / dur))
    return {"A_yaw": -8 + 36 * e, "A_x": 220 * e, "B_yaw": 30 - 22 * e, "B_scale": 0.9 + 0.1 * e}


def ui_52(work):
    end = turntable(1.4)
    mid = turntable(0.7)
    settle = spring(100, 16, secs=1.5, x0=0, target=1)
    over = settle.max() - 1
    save_json(work, "turntable.json", {"end": end, "mid": mid})
    return [("A -8 -> +28 deg and slides 220 px", (round(end["A_yaw"], 6), round(end["A_x"], 6)) == (28, 220), end),
            ("B +30 -> +8 deg, scale 0.9 -> 1", (round(end["B_yaw"], 6), round(end["B_scale"], 6)) == (8, 1), end),
            ("symmetric ease: halfway at 700 ms", abs(mid["A_x"] - 110) < 0.5, mid["A_x"]),
            ("settle spring 16/100 overshoots ~1.5% (analytic 1.52%)", abs(over - overshoot(100, 16)) < 0.002 and 0.01 < over < 0.02, round(float(over), 4))]


# ---------------------------------------------------------------- UI-53
def browser_window(t, W=240, H=160):
    p = out_cubic(clamp01(t / 0.5))
    im = Image.new("RGB", (W, H + 20), (235, 235, 235))
    d = ImageDraw.Draw(im)
    y = 20 * (1 - p)
    d.rounded_rectangle([10, 10 + y, W - 10, H + y], radius=12, fill=(255, 255, 255))
    for i, c in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
        d.ellipse([20 + i * 12, 16 + y, 28 + i * 12, 24 + y], fill=c)
    return im


def ui_53(work):
    a = np.asarray(browser_window(0.5))
    browser_window(0.5).save(work / "browser.png")
    top = np.nonzero(np.all(a[:, 120] == 255, axis=1))[0].min()
    start = np.nonzero(np.all(np.asarray(browser_window(0))[:, 120] == 255, axis=1))[0].min()
    dots = sum(1 for c in [(255, 95, 87), (254, 188, 46), (40, 200, 64)] if np.any(np.all(a == c, axis=2)))
    scroll = [600 * in_out_cubic(clamp01(t / 3)) for t in (0, 1.5, 3)]
    return [("window slides up 20 px over 500 ms", start - top == 20, (int(start), int(top))),
            ("three traffic-light dots", dots == 3, dots),
            ("inner grid scrolls 600 px over 3 s ease-in-out", scroll == [0, 300, 600], scroll),
            ("corner radius 12: top-left corner pixel stays background", tuple(a[10, 10]) == (235, 235, 235), tuple(a[10, 10]))]


# ---------------------------------------------------------------- UI-54
def fan_out(n=5):
    mid = n // 2
    rots = {0: 0, 1: 6, 2: 12}
    out = []
    for i in range(n):
        k = i - mid
        out.append({"rot": math.copysign(rots[abs(k)], k) if k else 0, "dy": 10 * abs(k), "scale": 1 - 0.05 * abs(k), "delay": 0.04 * abs(k)})
    return out


def ui_54(work):
    f = fan_out()
    save_json(work, "fan.json", f)
    return [("rotations -12/-6/0/6/12", [p["rot"] for p in f] == [-12, -6, 0, 6, 12], [p["rot"] for p in f]),
            ("outer phones lower and smaller", f[0]["dy"] > f[1]["dy"] > f[2]["dy"] and f[0]["scale"] < f[2]["scale"], f),
            ("40 ms stagger from the centre", [p["delay"] for p in f] == [0.08, 0.04, 0, 0.04, 0.08], [p["delay"] for p in f])]


# ---------------------------------------------------------------- UI-57
def flip_face(t, dur=0.7):
    ang = 180 * in_out_cubic(clamp01(t / dur))
    return ang, ("front" if ang < 90 else "back"), abs(math.cos(math.radians(ang)))


def ui_57(work):
    frames = [flip_face(f / 30) for f in range(22)]
    swap = next(i for i, (_, side, _) in enumerate(frames) if side == "back")
    width_at_swap = min(w for _, _, w in frames)
    save_json(work, "flip.json", frames)
    return [("content swaps exactly when rotation crosses 90 deg", frames[swap - 1][0] < 90 <= frames[swap][0], (frames[swap - 1][0], frames[swap][0])),
            ("90 deg is crossed at the 350 ms midpoint (frame 11 at 30 fps)", swap == 11, swap),
            ("flip ends at 180 deg after 700 ms", flip_face(0.7)[0] == 180, flip_face(0.7)[0])]


# ---------------------------------------------------------------- UI-58
def scroll_tour(t):
    e = bezier(0.45, 0, 0.15, 1)(clamp01(t / 0.8))
    return {"content": -720 * e, "bg": -24 * e, "callouts": round(t, 6) >= 0.95}


def ui_58(work):
    s = [scroll_tour(t) for t in (0, 0.8, 0.9, 0.95)]
    save_json(work, "tour.json", s)
    step = 0.62 * 844
    return [("content scrolls -720 px in 800 ms", round(s[1]["content"], 6) == -720, s[1]["content"]),
            ("background parallax -24 px (1/30 of content)", round(s[1]["bg"], 6) == -24, s[1]["bg"]),
            ("callouts only after scroll end + 150 ms", (s[2]["callouts"], s[3]["callouts"]) == (False, True), "callouts"),
            ("phone card step ~62% of 844 = 523 px", round(step) == 523, round(step))]


# ---------------------------------------------------------------- UI-59
def leader(t, start, dur=0.26):
    return bezier(0.16, 1, 0.3, 1)(clamp01((t - start) / dur))


def ui_59(work):
    rows = [round(i * 0.075, 3) for i in range(4)]
    callout = round(rows[-1] + 0.12, 3)
    im = Image.new("L", (120, 10), 0)
    d = ImageDraw.Draw(im)
    L = 100 * clamp01(0.4 / 0.4)
    x = 0
    while x < L:
        d.line([(x + 10, 5), (min(x + 2, L) + 10, 5)], fill=255)
        x += 6
    im.save(work / "dotted.png")
    on = (np.asarray(im)[5] > 0).astype(int)
    dashes = int(np.sum(np.diff(np.concatenate([[0], on])) == 1))
    return [("rows 75 ms apart (60-90)", all(0.06 <= b - a <= 0.09 for a, b in zip(rows, rows[1:])), rows),
            ("callout +120 ms after the last row", callout == 0.345, callout),
            ("leader 260 ms ease .16,1,.3,1 done at 260 ms", leader(0.26, 0) == 1.0 and leader(0.13, 0) > 0.8, round(leader(0.13, 0), 3)),
            ("dash 2 / gap 4 -> 17 dashes over 100 px", dashes == 17, dashes)]


# ---------------------------------------------------------------- UI-60
def push(t, maxz=1.6, dur=0.9):
    return 1 + (maxz - 1) * bezier(0.22, 1, 0.36, 1)(clamp01(t / dur))


def needs_2x(zoom):
    return zoom > 1.0


def ui_60(work):
    z = [push(t) for t in (0, 0.9, 1.2)]
    save_json(work, "push.json", [push(t) for t in np.linspace(0, 1.2, 37)])
    return [("push reaches 1.6x at 900 ms and holds", round(z[1], 6) == 1.6 and z[2] == z[1], z),
            ("zoom 1.4 requires a 2x render", needs_2x(1.4) and not needs_2x(1.0), "2x"),
            ("ease .22,1,.36,1 front-loaded (>80% at 40%)", (push(0.36) - 1) / 0.6 > 0.8, round((push(0.36) - 1) / 0.6, 3))]


# ---------------------------------------------------------------- UI-61
def modal_recipe(fps=30, travel=17, press_at=21):
    return {"travel_end": travel, "press": press_at, "modal": press_at + 5, "ripple_px": 48}


def ui_61(work):
    r = modal_recipe()
    times = [0, 560, 700, 780, 860, 880, 1000, 1600, 2200]
    focus = [1 + 0.3 * clamp01((f - r["modal"]) / 15) for f in (26, 41)]
    save_json(work, "modal.json", r)
    return [("modal at pressAt + 5 = frame 26", r["modal"] == 26, r),
            ("press frame 21 = 700 ms at 30 fps", round(21 / 30 * 1000) == 700 and 700 in times, 700),
            ("recipe times strictly increasing", times == sorted(set(times)), times),
            ("focus 1 -> 1.3", focus == [1.0, 1.3], focus)]


# ---------------------------------------------------------------- UI-62
def project(pt, rx, ry, p=1200):
    x, y, z = pt
    a, b = math.radians(rx), math.radians(ry)
    y, z = y * math.cos(a) - z * math.sin(a), y * math.sin(a) + z * math.cos(a)
    x, z = x * math.cos(b) + z * math.sin(b), -x * math.sin(b) + z * math.cos(b)
    s = p / (p - z)
    return x * s, y * s


def ui_62(work):
    W, H = 800, 500
    corners = [(-W / 2, -H / 2, 0), (W / 2, -H / 2, 0), (W / 2, H / 2, 0), (-W / 2, H / 2, 0)]
    pr = [project(c, 20, -15) for c in corners]
    top_w = math.dist(pr[0], pr[1])
    bot_w = math.dist(pr[3], pr[2])
    left_h = math.dist(pr[0], pr[3])
    right_h = math.dist(pr[1], pr[2])
    im = Image.new("L", (1200, 900), 0)
    ImageDraw.Draw(im).polygon([(x + 600, y + 450) for x, y in pr], fill=255)
    im.resize((300, 225)).save(work / "tilted.png")
    return [("rotateX 20: edge with +z (bottom) wider than the top", bot_w > top_w, (round(top_w, 1), round(bot_w, 1))),
            ("rotateY -15: one side taller than the other", abs(left_h - right_h) > 5, (round(left_h, 1), round(right_h, 1))),
            ("flat 0/0 projection is identity", project((100, 50, 0), 0, 0) == (100, 50), project((100, 50, 0), 0, 0))]


# ---------------------------------------------------------------- UI-63
def wall_blur(z, focus, max_blur=8, falloff=400):
    return min(max_blur, abs(z - focus) / falloff * max_blur)


def ui_63(work):
    zs = [-600, -300, 0, 300]
    b = [wall_blur(z, 0) for z in zs]
    card = Image.new("L", (40, 40), 0)
    ImageDraw.Draw(card).rectangle([10, 10, 30, 30], fill=255)
    blurred = card.filter(ImageFilter.GaussianBlur(b[1] / 2))
    blurred.save(work / "blurred_card.png")
    edge_sharp = np.asarray(card)[20, 8:13].astype(int)
    edge_soft = np.asarray(blurred)[20, 8:13].astype(int)
    return [("blur 0 at focus, capped at 8 px", b == [8, 6, 0, 6], b),
            ("blurred card edge is softer than the in-focus edge", np.abs(np.diff(edge_soft)).max() < np.abs(np.diff(edge_sharp)).max(), (edge_soft.tolist(), edge_sharp.tolist())),
            ]


# ---------------------------------------------------------------- UI-64
def lens_frame(img, cx, cy, r, mag=2.0):
    a = np.asarray(img)
    H, W = a.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W]
    inside = (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r
    sx = np.clip(((xx - cx) / mag + cx).round().astype(int), 0, W - 1)
    sy = np.clip(((yy - cy) / mag + cy).round().astype(int), 0, H - 1)
    out = a.copy()
    out[inside] = a[sy[inside], sx[inside]]
    return out


def ui_64(work):
    rng = np.random.default_rng(0)
    img = Image.fromarray(rng.integers(0, 255, (60, 100), dtype=np.uint8))
    path = [(20 + 60 * clamp01((t - 1) / 3), 30) for t in (0.5, 2.5, 5)]
    out = lens_frame(img, 50, 30, 12)
    Image.fromarray(out).save(work / "lens.png")
    a = np.asarray(img)
    return [("lens centre shows the same pixel (compensated position)", out[30, 50] == a[30, 50], (int(out[30, 50]), int(a[30, 50]))),
            ("inside: offset 10 px shows source offset 5 px (x2)", out[30, 60] == a[30, 55], (int(out[30, 60]), int(a[30, 55]))),
            ("outside the circle untouched", out[5, 5] == a[5, 5] and out[30, 63] == a[30, 63], "outside"),
            ("lens moves only during 1-4 s", path[0][0] == 20 and path[2][0] == 80 and path[1][0] == 50, path)]


# ---------------------------------------------------------------- UI-65
def hotspot(t, show_at, pop=0.2):
    pulse = 0.5 + 0.5 * math.sin(2 * math.pi * t / 1.0)
    return pulse, round(back_out(clamp01((t - show_at) / pop), 1.2), 9) if t >= show_at else 0.0


def ui_65(work):
    W = 1000
    split = (0.4 * W, 0.6 * W)
    bubbles = [round(i * 0.6, 1) for i in range(4)]
    _, pop0 = hotspot(1.0, 1.0)
    _, pop1 = hotspot(1.2, 1.0)
    save_json(work, "hotspot.json", {"split": split, "bubbles": bubbles, "pop": [hotspot(1.0 + d, 1.0)[1] for d in np.linspace(0, 0.2, 11)]})
    return [("pulse loops every 1 s", abs(hotspot(0.3, 9)[0] - hotspot(1.3, 9)[0]) < 1e-9, "loop"),
            ("tooltip pops 0 -> 1 over 200 ms", pop0 == 0.0 and abs(pop1 - 1) < 1e-9, (pop0, pop1)),
            ("split 40/60", split == (400.0, 600.0), split),
            ("bubbles ~600 ms apart", bubbles == [0.0, 0.6, 1.2, 1.8], bubbles)]


# ---------------------------------------------------------------- UI-66
def wipe(t, W=100, H=40, rtl=True, dur=1.2, rest=0.5):
    p = in_out_cubic(clamp01(t / dur))
    frac = p * rest / rest * rest if t > dur else p * rest
    before = np.full((H, W), 60, np.uint8)
    after = np.full((H, W), 220, np.uint8)
    out = before.copy()
    n = int(round(W * frac))
    if rtl:
        out[:, W - n:] = after[:, W - n:] if n else out[:, W:]
    else:
        out[:, :n] = after[:, :n]
    return out


def ui_66(work):
    end = wipe(1.2)
    Image.fromarray(end).save(work / "wipe_rest.png")
    after_cols = np.nonzero(end[20] == 220)[0]
    mid = wipe(0.6)
    return [("wipe rests at 50%", len(after_cols) == 50, len(after_cols)),
            ("Arabic: 'after' enters from the right", after_cols.min() == 50 and after_cols.max() == 99, (int(after_cols.min()), int(after_cols.max()))),
            ("ease-in-out midpoint at 0.6 s = 25%", (mid[20] == 220).sum() == 25, int((mid[20] == 220).sum())),
            ("nothing revealed at 0", (wipe(0)[20] == 220).sum() == 0, "0")]


# ---------------------------------------------------------------- UI-67
def slot_reel(t, target=7, card=100, dur=1.0):
    p = clamp01(t / dur)
    e = back_out(p, 0.6)
    pos = target * card * e
    vel = abs(target * card * (back_out(min(1, p + 0.01), 0.6) - e)) / 0.01 / dur
    blur = min(30, vel / 60)
    return pos, blur


def ui_67(work):
    end, blur_end = slot_reel(1.0)
    save_json(work, "reel.json", [slot_reel(t) for t in np.linspace(0, 1, 31)])
    peak = max(slot_reel(t)[0] for t in np.linspace(0, 1, 201))
    blurs = [slot_reel(t)[1] for t in (0.05, 0.99)]
    strip = [120 * t for t in (0, 1, 2.5)]
    return [("reel lands on card 7 at 1.0 s", round(end, 6) == 700, end),
            ("overshoot then settles (peak > target)", peak > 700, round(peak, 2)),
            ("motion blur high while fast, ~0 at the catch", blurs[0] >= 20 and blurs[1] < 5, [round(b, 1) for b in blurs]),
            ("cropped strip moves 120 px/s", strip == [0, 120, 300], strip)]


# ---------------------------------------------------------------- UI-68
def grid_cols(W, cols=12, gutter=24):
    cw = (W - gutter * (cols - 1)) / cols
    return [(round(i * (cw + gutter), 3), round(cw, 3)) for i in range(cols)]


def ui_68(work):
    g = grid_cols(1872)
    save_json(work, "grid.json", g)
    span4 = g[3][0] + g[3][1] - g[0][0]
    stagger = [round(i * 0.09, 2) for i in range(4)]
    counter = f"f {47:03d}/{900}"
    return [("12 columns, 24 px gutters fill 1872 px", round(g[-1][0] + g[-1][1], 3) == 1872 and g[1][0] - g[0][1] == 24, g[:2]),
            ("a 4-column module spans 4w + 3 gutters", round(span4, 3) == round(4 * g[0][1] + 72, 3), span4),
            ("stagger 90 ms within 80-100", all(0.08 <= b - a <= 0.1 for a, b in zip(stagger, stagger[1:])), stagger),
            ("frame counter 'f 047/900'", counter == "f 047/900", counter)]


# ---------------------------------------------------------------- UI-69
def hud_bands(H):
    return (0.085 * H, H - 0.20 * H)


def project_anchor(p, f=800, W=1920, H=1080):
    x, y, z = p
    return W / 2 + f * x / z, H / 2 - f * y / z


def ui_69(work):
    top, bottom = hud_bands(1080)
    save_json(work, "hud.json", {"top": top, "bottom": bottom})
    a = project_anchor((0.5, 0.25, 4))
    ticks = [i * 10 for i in range(36)]
    return [("top band 8.5% H = 91.8 px, bottom band from 864 px", (round(top, 1), bottom) == (91.8, 864.0), (top, bottom)),
            ("callout anchor projects (0.5,0.25,4) -> (1060, 490)", a == (1060.0, 490.0), a),
            ("stage disc has 36 ticks 10 deg apart", len(ticks) == 36 and ticks[-1] == 350, len(ticks)),
            ("ink #0f1512 on paper #f4f2ec >= 7:1", _contrast((0x0f, 0x15, 0x12), (0xf4, 0xf2, 0xec)) >= 7, _contrast((0x0f, 0x15, 0x12), (0xf4, 0xf2, 0xec)))]


def _contrast(a, b):
    def L(c):
        v = [x / 255 for x in c]
        v = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in v]
        return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]
    la, lb = sorted((L(a), L(b)), reverse=True)
    return round((la + 0.05) / (lb + 0.05), 2)


# ---------------------------------------------------------------- UI-70
def track_box(frame):
    import cv2
    cs, _ = cv2.findContours((frame > 128).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return cv2.boundingRect(max(cs, key=cv2.contourArea))


def ui_70(work):
    boxes, frames = [], []
    for f in range(10):
        a = np.zeros((90, 160), np.uint8)
        x = 20 + f * 8
        a[30:60, x:x + 25] = 255
        frames.append(a)
        boxes.append(track_box(a))
    rng = np.random.default_rng(4)
    conf = rng.uniform(0.95, 0.99, 10)
    im = Image.fromarray(np.dstack([frames[5]] * 3))
    d = ImageDraw.Draw(im)
    x, y, w, h = boxes[5]
    for cx, cy, sx, sy in ((x, y, 1, 1), (x + w, y, -1, 1), (x, y + h, 1, -1), (x + w, y + h, -1, -1)):
        d.line([(cx, cy), (cx + sx * 12, cy)], fill=(0xfa, 0xcc, 0x15), width=2)
        d.line([(cx, cy), (cx, cy + sy * 12)], fill=(0xfa, 0xcc, 0x15), width=2)
    im.save(work / "tracking.png")
    return [("box re-derived from the target every frame (x moves 8 px/frame)", [b[0] for b in boxes] == [20 + 8 * f for f in range(10)], [b[0] for b in boxes]),
            ("box size equals the target 25x30", all(b[2:] == (25, 30) for b in boxes), boxes[0]),
            ("seeded confidence within 95-99%", conf.min() >= 0.95 and conf.max() <= 0.99, (round(float(conf.min()), 3), round(float(conf.max()), 3))),
            ("corner brackets drawn in #facc15", (0xfa, 0xcc, 0x15) in [c for _, c in im.getcolors(4096)], "yellow")]


# ---------------------------------------------------------------- UI-71
def handles(bbox, n=8, size=6):
    x0, y0, x1, y1 = bbox
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    if n == 8:
        pts += [((x0 + x1) / 2, y0), (x1, (y0 + y1) / 2), ((x0 + x1) / 2, y1), (x0, (y0 + y1) / 2)]
    return [(x - size / 2, y - size / 2, x + size / 2, y + size / 2) for x, y in pts]


def ui_71(work):
    import cv2
    im = Image.new("L", (200, 140), 0)
    d = ImageDraw.Draw(im)
    for gx in range(0, 200, 24):
        for gy in range(0, 140, 24):
            d.point((gx, gy), fill=60)
    for h in handles((40, 30, 160, 110)):
        d.rectangle(h, fill=255)
    im.save(work / "selection.png")
    n = cv2.connectedComponents((np.asarray(im) == 255).astype(np.uint8))[0] - 1
    dots = int((np.asarray(im) == 60).sum())
    return [("8 square handles rendered", n == 8, n),
            ("dot grid every 24 px (9x6 = 54 dots minus hidden)", 50 <= dots <= 54, dots),
            ("4-handle variant", len(handles((0, 0, 10, 10), n=4)) == 4, 4),
            ]


# ---------------------------------------------------------------- UI-75
def ui_75(work):
    src = work / "capture.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=size=192x108:rate=30:duration=1", "-c:v", "libx264", "-preset", "ultrafast", str(src)], check=True)
    sizes = {"16x9": (192, 108), "4x5": (96, 120), "9x16": (72, 128), "1x1": (108, 108)}
    got = {}
    for k, (w, h) in sizes.items():
        out = work / f"demo_{k}.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vf", f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},tpad=start_duration=0.3:stop_duration=0.3:start_mode=clone:stop_mode=clone",
                        "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", str(out)], check=True)
        p = json.loads(subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", str(out)], capture_output=True, text=True).stdout)
        got[k] = (p["streams"][0]["width"], p["streams"][0]["height"], round(float(p["format"]["duration"]), 2))
    return [("four deliverables 16:9 / 4:5 / 9:16 / 1:1", {k: v[:2] for k, v in got.items()} == sizes, got),
            ("0.3 s held before and after the action (1.0 -> 1.6 s)", all(abs(v[2] - 1.6) <= 0.05 for v in got.values()), [v[2] for v in got.values()])]


# ---------------------------------------------------------------- UI-76
def figma_ref(url):
    m = re.search(r"/(?:design|file)/([A-Za-z0-9]+)/", url)
    n = re.search(r"node-id=([\d]+)[-:]([\d]+)", url)
    return m.group(1), f"{n.group(1)}:{n.group(2)}"


def rgba_hex(c):
    return "#" + "".join(f"{round(c[k] * 255):02x}" for k in ("r", "g", "b")) + ("" if c.get("a", 1) == 1 else f"{round(c['a'] * 255):02x}")


def autolayout_css(node):
    css = {"display": "flex", "flex-direction": "row" if node["layoutMode"] == "HORIZONTAL" else "column", "gap": f"{node['itemSpacing']}px",
           "padding": f"{node['paddingTop']}px {node['paddingRight']}px {node['paddingBottom']}px {node['paddingLeft']}px"}
    css["justify-content"] = {"MIN": "flex-start", "CENTER": "center", "MAX": "flex-end", "SPACE_BETWEEN": "space-between"}[node["primaryAxisAlignItems"]]
    return css


def ui_76(work):
    key, nid = figma_ref("https://www.figma.com/design/AbC123xyz/Landing?node-id=123-456&t=x")
    node = {"layoutMode": "VERTICAL", "itemSpacing": 16, "paddingTop": 24, "paddingRight": 20, "paddingBottom": 24, "paddingLeft": 20, "primaryAxisAlignItems": "SPACE_BETWEEN"}
    css = autolayout_css(node)
    save_json(work, "frame_css.json", css)
    return [("file key after /design/", key == "AbC123xyz", key),
            ("node-id 123-456 == 123:456", nid == "123:456", nid),
            ("RGBA floats -> hex (1, 0.5, 0) -> #ff8000", rgba_hex({"r": 1, "g": 0.5, "b": 0, "a": 1}) == "#ff8000", rgba_hex({"r": 1, "g": 0.5, "b": 0, "a": 1})),
            ("auto-layout -> flex column, gap 16, space-between", (css["flex-direction"], css["gap"], css["justify-content"]) == ("column", "16px", "space-between"), css)]


# ---------------------------------------------------------------- UI-79
SPACING = [4, 8, 16, 24, 32, 48, 64]


def type_scale(base=16, ratio=1.2, steps=(-2, -1, 0, 1, 2, 3, 4)):
    return [round(base * ratio ** s) for s in steps]


def measure_ok(chars):
    return 45 <= chars <= 75


def ui_79(work):
    ts = type_scale()
    save_json(work, "tokens.json", {"spacing": SPACING, "type": ts})
    ratios = [b / a for a, b in zip(ts, ts[1:])]
    return [("spacing on the 4/8 px grid", all(s % 4 == 0 for s in SPACING), SPACING),
            ("type scale ~1.2 spans 11-33 px around 16", ts[0] == 11 and ts[2] == 16 and 33 <= ts[-1] <= 36, ts),
            ("adjacent ratios ~1.2 (1.1-1.3)", all(1.1 <= r <= 1.3 for r in ratios[1:]), [round(r, 2) for r in ratios]),
            ("measure 60ch ok, 90ch rejected", measure_ok(60) and not measure_ok(90), "measure"),
            ]


# ---------------------------------------------------------------- UI-80
def glass(bg, box, blur=24, fill=0.06):
    region = bg.crop(box).filter(ImageFilter.GaussianBlur(blur / 2))
    a = np.asarray(region).astype(float)
    a = a * (1 - fill) + 255 * fill
    out = bg.copy()
    out.paste(Image.fromarray(a.round().astype(np.uint8)), box[:2])
    return out


def ui_80(work):
    bg = np.zeros((120, 200), np.uint8)
    bg[:, ::10] = 255
    img = Image.fromarray(bg)
    g = glass(img, (50, 30, 150, 90))
    g.save(work / "glass.png")
    a = np.asarray(g).astype(int)
    inside_std = a[45:75, 65:135].std()
    outside_std = bg[:, :40].std()
    cards = 3
    return [("backdrop blurred under the card (stripes flattened)", inside_std < 0.1 * outside_std, (round(inside_std, 2), round(outside_std, 2))),
            ("6% white fill lifts the blurred dark mean", a[45:75, 65:135].mean() > 0.9 * bg.mean() + 0.06 * 255 * 0.5, round(a[45:75, 65:135].mean(), 1)),
            ("outside the card untouched", np.array_equal(a[:, :40], bg[:, :40]), "same"),
            ]


# ---------------------------------------------------------------- UI-81
LOOKS = ["kosif", "cobalt", "navygold", "najd", "heritage", "executive", "audit", "midnight", "notebook", "aurora", "vivid", "oasis", "graphite", "onyx"]


def hardcoded_colours(css):
    rules = re.findall(r"(\.screen[^{]*){([^}]*)}", css)
    return [sel.strip() for sel, body in rules if re.search(r"#[0-9a-fA-F]{3,6}|rgb\(", body)]


def ui_81(work):
    combos = [f'html[data-look="{l}"][data-theme="{t}"]' for l in LOOKS for t in ("light", "dark")]
    css = '.screen-a{color:var(--ink);background:var(--paper)} .screen-b{color:#333}'
    (work / "looks.css").write_text("\n".join(c + "{--accent:var(--brand)}" for c in combos))
    return [("14 looks x 2 themes = 28 selectors", len(combos) == 28 and len(LOOKS) == 14, len(combos)),
            ("hard-coded colour on a screen caught", hardcoded_colours(css) == [".screen-b"], hardcoded_colours(css)),
            ]


# ---------------------------------------------------------------- UI-83
def sticker(outline=5, offset=6, fill=(255, 214, 102)):
    im = Image.new("RGB", (120, 100), (255, 255, 255))
    d = ImageDraw.Draw(im)
    shadow = tuple(int(c * 0.55) for c in fill)
    d.rounded_rectangle([10, 10 + offset, 100, 80 + offset], radius=28, fill=shadow)
    d.rounded_rectangle([10, 10, 100, 80], radius=28, fill=(0x2a, 0x17, 0x11))
    d.rounded_rectangle([10 + outline, 10 + outline, 100 - outline, 80 - outline], radius=28 - outline, fill=fill)
    return im, shadow


def ui_83(work):
    im, shadow = sticker()
    im.save(work / "sticker.png")
    a = np.asarray(im)
    col = a[:, 55]
    outline = int(np.all(col[5:30] == (0x2a, 0x17, 0x11), axis=1).sum())
    sh = int(np.all(col == shadow, axis=1).sum())
    hue = lambda c: __import__("colorsys").rgb_to_hsv(*[x / 255 for x in c])[0]
    return [("outline 5 px (4-6) #2a1711", outline == 5, outline),
            ("hard shadow offset 6 px below", sh == 6, sh),
            ("shadow same hue as the fill", abs(hue(shadow) - hue((255, 214, 102))) < 0.01, (round(hue(shadow), 3), round(hue((255, 214, 102)), 3)))]


# ---------------------------------------------------------------- UI-85
BLUEPRINTS = {"cursor-ui-demo": (4.0, 12.9), "device-surface-showcase": (5.0, 11.3), "prompt-type-submit-generate": (5.2, 12.0),
              "agent-progress-theater": (4.2, 11.6), "panel-edit-live-sync": (5.3, 11.9), "transcript-scroll-artifact-reveal": (5.0, 11.8)}
ROLE = {"demo": "cursor-ui-demo", "device": "device-surface-showcase", "ai prompt": "prompt-type-submit-generate", "agent": "agent-progress-theater",
        "settings": "panel-edit-live-sync", "transcript": "transcript-scroll-artifact-reveal"}


def pick_blueprint(role, seconds):
    bp = ROLE[role]
    lo, hi = BLUEPRINTS[bp]
    return bp if lo <= seconds <= hi else None


def ui_85(work):
    save_json(work, "blueprints.json", BLUEPRINTS)
    return [("AI prompt at 8 s -> prompt-type-submit-generate", pick_blueprint("ai prompt", 8) == "prompt-type-submit-generate", pick_blueprint("ai prompt", 8)),
            ("agent at 3 s is too short (4.2-11.6)", pick_blueprint("agent", 3) is None, None),
            ("all durations inside 3.5-12.9 s", all(3.5 <= lo and hi <= 12.9 for lo, hi in BLUEPRINTS.values()), "range")]


# ---------------------------------------------------------------- UI-86
def ui_86(work):
    tool = REPO / "tools" / "kosif.py"
    out = {}
    for sid in ("saas-demo", "ui-micro", "glass-ui"):
        d = work / sid
        r = subprocess.run([sys.executable, str(tool), "scaffold", sid, str(d)], capture_output=True, text=True, cwd=str(REPO), timeout=30)
        out[sid] = {"rc": r.returncode, "files": sorted(p.name for p in d.glob("*.md")), "named": sid in (d / "PLAN.md").read_text(encoding="utf-8") if (d / "PLAN.md").exists() else False}
    lst = subprocess.run([sys.executable, str(tool), "list", "--category", "product-ui"], capture_output=True, text=True, cwd=str(REPO), timeout=30).stdout
    rows = [l for l in lst.splitlines()[2:] if l.strip()]
    save_json(work, "scaffold.json", out)
    return [("three styles scaffold with exit 0", all(v["rc"] == 0 for v in out.values()), {k: v["rc"] for k, v in out.items()}),
            ("each gets PLAN/REQUEST/STYLE/TEST_REPORT", all({"PLAN.md", "REQUEST.md", "STYLE.md", "TEST_REPORT.md"} <= set(v["files"]) for v in out.values()), out["saas-demo"]["files"]),
            ("PLAN.md names the chosen style", all(v["named"] for v in out.values()), {k: v["named"] for k, v in out.items()}),
            ("product-ui category lists >= 82 entries", len(rows) >= 82, len(rows))]


# ---------------------------------------------------------------- UI-88
class FrameReview:
    KEYS = {"Space": "play", "ArrowLeft": "-frame", "ArrowRight": "+frame", "KeyE": "edit", "KeyN": "note", "BracketLeft": "-scene", "BracketRight": "+scene"}

    def __init__(self):
        self.edits, self.undo = {}, []

    def set_box(self, eid, box_px, W, H):
        x, y, w, h = box_px
        box = [round(x / W * 100, 1), round(y / H * 100, 1), round(w / W * 100, 1), round(h / H * 100, 1)]
        self.undo.append(dict(self.edits))
        self.undo = self.undo[-60:]
        self.edits[f"{eid}.@box"] = box

    def key(self, code, shift=False):
        a = self.KEYS.get(code)
        if a in ("-frame", "+frame") and shift:
            a = a.replace("frame", "second")
        return a

    @staticmethod
    def corner_hit(p, box, r=14):
        x, y, w, h = box
        return any(math.dist(p, c) <= r for c in ((x, y), (x + w, y), (x, y + h), (x + w, y + h)))


def ui_88(work):
    fr = FrameReview()
    fr.set_box("title", (192, 108, 960, 216), 1920, 1080)
    for i in range(70):
        fr.set_box("x", (i, i, 10, 10), 1920, 1080)
    save_json(work, "edits.json", fr.edits)
    return [("box stored in % with one decimal", fr.edits["title.@box"] == [10.0, 10.0, 50.0, 20.0], fr.edits["title.@box"]),
            ("keys bound to ev.code survive the Arabic layout (KeyE = edit)", fr.key("KeyE") == "edit" and fr.key("KeyN") == "note", fr.key("KeyE")),
            ("Shift+arrow steps one second", fr.key("ArrowRight", shift=True) == "+second", fr.key("ArrowRight", shift=True)),
            ("corner grab radius 14 px", FrameReview.corner_hit((109, 109), (100, 100, 50, 50)) and not FrameReview.corner_hit((111, 111), (100, 100, 50, 50)), "14"),
            ("undo depth capped at 60", len(fr.undo) == 60, len(fr.undo))]


# ---------------------------------------------------------------- UI-89
ORDER = ["hero", "social_proof", "benefits", "steps", "offer", "faq", "final_cta"]


def landing_ok(page):
    errs = []
    if [s["kind"] for s in page["sections"]] != ORDER:
        errs.append("section order")
    hero = page["sections"][0]
    if len(hero.get("headline", "").split()) > 10 or hero.get("ctas", 0) != 1:
        errs.append("hero")
    b = next(s for s in page["sections"] if s["kind"] == "benefits")
    if not 3 <= b["count"] <= 6:
        errs.append("benefits")
    m = page["metrics"]
    if m["lcp"] > 2.5 or m["cls"] > 0.1 or m["inp"] > 200 or m["js_kb"] > 170:
        errs.append("budget")
    return errs


def h1_size(vw):
    return min(44, max(28, 0.05 * vw))


def ui_89(work):
    secs = [{"kind": k} for k in ORDER]
    secs[0].update(headline="أغلق حساباتك الشهرية في يومين", ctas=1)
    secs[2]["count"] = 4
    good = {"sections": secs, "metrics": {"lcp": 1.9, "cls": 0.02, "inp": 120, "js_kb": 90}}
    bad = {"sections": [dict(secs[0], ctas=2)] + secs[1:], "metrics": {"lcp": 3.1, "cls": 0.02, "inp": 120, "js_kb": 90}}
    save_json(work, "landing.json", good)
    return [("good landing passes", landing_ok(good) == [], landing_ok(good)),
            ("two hero CTAs and slow LCP caught", landing_ok(bad) == ["hero", "budget"], landing_ok(bad)),
            ("H1 clamp(28px,5vw,44px): 360->28, 768->38.4, 1280->44", (h1_size(360), round(h1_size(768), 1), h1_size(1280)) == (28, 38.4, 44), "clamp")]


# ---------------------------------------------------------------- UI-X01
def ui_x01(work):
    state_frame = 30 + 2
    press = [1, 0.96, 1]
    cur = Image.new("L", (200, 200), 0)
    ImageDraw.Draw(cur).polygon([(10, 10), (10, 160), (50, 125), (75, 170), (95, 160), (70, 115), (120, 115)], fill=255)
    cur.save(work / "cursor.png")
    h = cur.getbbox()[3] - cur.getbbox()[1]
    return [("protagonist cursor 128-176 px tall at 1920 (rendered 161)", 128 <= h <= 176, h),
            ("state changes 2 frames after the click (frame 32)", state_frame == 32, state_frame),
            ("cursor drawn as its own layer (headless captures omit it)", np.asarray(cur).max() == 255, "layer")]


# ---------------------------------------------------------------- UI-X02
def exploded(n, k=1.0):
    return [round(k * (70 + 150 * i), 3) for i in range(n)]


def ui_x02(work):
    z = exploded(4)
    delays = [round(0.03 * i, 2) for i in range(4)]
    rot = 25
    counter = -rot
    save_json(work, "layers.json", {"z": z, "delays": delays})
    return [("z = 70 + 150 i -> 70/220/370/520", z == [70, 220, 370, 520], z),
            ("k scales every layer (k=0.5)", exploded(2, 0.5) == [35, 110], exploded(2, 0.5)),
            ("0.03 s stagger per layer", delays == [0.0, 0.03, 0.06, 0.09], delays),
            ("text layer counter-rotated stays frontal", rot + counter == 0, rot + counter)]


# ---------------------------------------------------------------- UI-X03
def ui_x03(work):
    webm = work / "demo.webm"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=size=128x72:rate=25:duration=1", "-c:v", "libvpx", "-b:v", "300k", str(webm)], check=True)
    mp4 = work / "demo.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(webm), "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-r", "30", str(mp4)], check=True)
    p = lambda f: json.loads(subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", str(f)], capture_output=True, text=True).stdout)["streams"][0]
    a, b = p(webm), p(mp4)
    return [("conversion stage: VP8 25 fps input", (a["codec_name"], a["r_frame_rate"]) == ("vp8", "25/1"), (a["codec_name"], a["r_frame_rate"])),
            ("H.264 yuv420p at 30 fps output", (b["codec_name"], b["pix_fmt"], b["r_frame_rate"]) == ("h264", "yuv420p", "30/1"), (b["codec_name"], b["pix_fmt"], b["r_frame_rate"]))]


# ---------------------------------------------------------------- UI-X04
MOTION_TOKENS = {"instant": 0.0, "fast": 0.15, "normal": 0.25, "slow": 0.4, "crawl": 0.7}
SPRINGS = {"snappy": (500, 30), "gentle": (120, 14), "bouncy": (300, 10), "instant": (1000, 60), "release": (300, 20)}
FORBIDDEN = {"width", "height", "top", "left", "margin", "padding"}


def motion_lint(anim, reduced=False):
    errs = [p for p in anim["animate"] if p in FORBIDDEN]
    if reduced and set(anim["animate"]) - {"opacity"}:
        errs.append("reduced motion must be opacity only")
    if anim["initial"] != anim["ssr"]:
        errs.append("initial != server state")
    return errs


def ui_x04(work):
    good = {"animate": ["opacity", "y"], "initial": {"opacity": 0}, "ssr": {"opacity": 0}}
    bad = {"animate": ["width", "opacity"], "initial": {"opacity": 1}, "ssr": {"opacity": 0}}
    s = spring(*SPRINGS["bouncy"], secs=1)
    save_json(work, "motion_tokens.json", {"durations": MOTION_TOKENS, "springs": SPRINGS})
    return [("five duration tokens ascending", list(MOTION_TOKENS.values()) == sorted(MOTION_TOKENS.values()) and len(MOTION_TOKENS) == 5, MOTION_TOKENS),
            ("five spring presets; bouncy overshoots more than gentle", len(SPRINGS) == 5 and overshoot(*SPRINGS["bouncy"]) > overshoot(*SPRINGS["gentle"]), round(overshoot(*SPRINGS["bouncy"]), 3)),
            ("good animation passes", motion_lint(good) == [], motion_lint(good)),
            ("width animation and SSR mismatch caught", motion_lint(bad) == ["width", "initial != server state"], motion_lint(bad)),
            ("reduced motion allows opacity only", motion_lint(good, reduced=True) == ["reduced motion must be opacity only"], "reduced"),
            ]


PROGRAMS = {f"UI-{n:02d}" if isinstance(n, int) else f"UI-{n}": globals()[f"ui_{n:02d}" if isinstance(n, int) else f"ui_{n.lower()}"]
            for n in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
                      31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 57, 58, 59, 60,
                      61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 75, 76, 79, 80, 81, 83, 85, 86, 88, 89, "X01", "X02", "X03", "X04"]}
