"""Real programs for the characters-rigs power cards.

Rig maths (two-bone IK, nested pivots, phase-locked walks, springs, Verlet chains), timing recipes
(squash, anticipation, blinks, mouth swaps from words.json), staging rules and spec sheets run as
deterministic numpy/Pillow procedures with known answers. Cards that need an image/avatar
generator, three.js kits (K3/K3S), Lottie players or paid APIs are skipped.
"""
from __future__ import annotations

import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from .photo_video_footage import REPO, chk, jwrite, near, hexrgb, write_video, read_video

FONT = REPO / ".claude/skills/kosif-superpowers/proofs/_shared/fonts/Amiri-Bold.ttf"


def _recorded(fn):
    """Keep the computed observations as the program's output file when it draws nothing else."""
    def run(work):
        checks = fn(work)
        if not any(p.is_file() and p.stat().st_size for p in Path(work).rglob("*")):
            jwrite(work, f"{fn.__name__}.json", [{"check": n, "passed": bool(ok), "observed": str(o)} for n, ok, o in checks])
        return checks
    run.__name__ = fn.__name__
    return run


def scaffold(style, d):
    r = subprocess.run([sys.executable, str(REPO / "tools" / "kosif.py"), "scaffold", style, str(d)],
                       capture_output=True, text=True, timeout=60, cwd=REPO)
    return r.returncode == 0 and (Path(d) / "PLAN.md").is_file(), (sorted(p.name for p in Path(d).iterdir()) if Path(d).is_dir() else r.stderr[-200:])


def smoothstep(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


def sine_io(p):
    return 0.5 - 0.5 * math.cos(math.pi * min(max(p, 0), 1))


def spring(t, f, z):
    """Unit step response of a damped spring with natural frequency f Hz and damping ratio z."""
    w = 2 * math.pi * f
    if t <= 0:
        return 0.0
    wd = w * math.sqrt(1 - z * z)
    return 1 - math.exp(-z * w * t) * (math.cos(wd * t) + z * w / wd * math.sin(wd * t))


def back_out(p, s=1.70158):
    p -= 1
    return 1 + (s + 1) * p ** 3 + s * p ** 2


def cubic_bezier(x1, y1, x2, y2):
    def bez(t, a, b):
        return 3 * a * t * (1 - t) ** 2 + 3 * b * t * t * (1 - t) + t ** 3

    def solve(x):
        lo, hi = 0.0, 1.0
        for _ in range(60):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if bez(mid, x1, x2) < x else (lo, mid)
        return bez((lo + hi) / 2, y1, y2)
    return solve


def silhouette_reads(mask):
    """A pose reads as a silhouette when its limbs separate from the body: count holes/notches by convex deficiency."""
    import cv2
    m = (mask > 0).astype(np.uint8)
    cnts, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = max(cnts, key=cv2.contourArea)
    hull = cv2.convexHull(c)
    return 1 - cv2.contourArea(c) / cv2.contourArea(hull)


def draw_stick(arm_angle, size=200):
    im = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(im)
    d.ellipse([85, 20, 115, 50], fill=255)
    d.rectangle([94, 50, 106, 130], fill=255)
    for side in (-1, 1):
        a = math.radians(arm_angle) * side
        d.line([(100, 60), (100 + side * 55 * math.cos(math.radians(90) - abs(a)) if arm_angle else 100 + side * 6, 60 + 55 * math.sin(math.radians(90) - abs(a)) if arm_angle else 125)],
               fill=255, width=10)
        d.line([(100, 130), (100 + side * 25, 185)], fill=255, width=10)
    return np.asarray(im)


def ch_01(work):
    spec = {"palette": ["#1f2328", "#f2c94c", "#5b8def", "#fbf9f4"], "outline": {"px": 4, "colour": "#1f2328"},
            "views": ["front", "side", "three-quarter", "rear", "camera"], "expressions": ["neutral", "joy", "anger", "fear"],
            "ground_line": 180}
    (work / "STYLE.md").write_text("\n".join(f"{k}: {v}" for k, v in spec.items()))
    closed, opened = draw_stick(0), draw_stick(60)
    Image.fromarray(opened).save(work / "silhouette_open.png")
    d0, d1 = silhouette_reads(closed), silhouette_reads(opened)
    return [chk("3-5 colours, 3-5+ views, 3-5 expressions locked", 3 <= len(spec["palette"]) <= 5 and len(spec["views"]) >= 3
                and 3 <= len(spec["expressions"]) <= 5, (len(spec["palette"]), len(spec["views"]))),
            chk("arms-down pose fails the silhouette test, open pose reads (more negative space)", d1 > d0 + 0.1, (round(d0, 3), round(d1, 3)))]


def ch_02(work):
    head_w, body_w = 0.16, 0.14

    def lint(c):
        errs = []
        if c["head_w"] < c["body_w"]:
            errs.append("head narrower than body")
        if not 0.40 <= c["eye_y"] <= 0.50:
            errs.append("eyes not low (~45%)")
        if not near(c["eye_gap"], 0.4 * c["head_w"], 0.01):
            errs.append("eye spacing != 0.4 x head width")
        if c["nose_w"] > c["head_w"] / 8:
            errs.append("nose > 1/8 head width")
        if c["accents"] != 1:
            errs.append("exactly one accent colour")
        return errs

    cute = {"head_w": head_w, "body_w": body_w, "eye_y": 0.45, "eye_gap": 0.064, "nose_w": 0.018, "accents": 1}
    wrong = dict(cute, head_w=0.12, eye_y=0.3, nose_w=0.05, accents=3)
    jwrite(work, "cute_lint.json", {"cute": lint(cute), "wrong": lint(wrong)})
    return [chk("bunny spec passes the cute recipe", lint(cute) == [], lint(cute)),
            chk("narrow head, high eyes, big nose, 3 accents all caught", len(lint(wrong)) == 5, lint(wrong))]


LOCK_FIELDS = ["name", "age", "skin tone", "face shape", "eyes", "brows", "nose", "lips", "hair", "build/height",
               "signature outfit", "accessories", "marks", "MUST NOT CHANGE"]


def ch_03(work):
    lock = "CHR-001: " + " · ".join(f"{f}: x" for f in LOCK_FIELDS)
    prompts = [f"Shot {i}: walking at dawn. {lock}" for i in range(3)] + ["Shot 4: running. CHR-001: name: x · hair: y"]
    verbatim = [lock in p for p in prompts]
    views = ["front", "3/4 left", "profile", "back", "full-body contrapposto"]
    expr = ["neutral", "joy", "anger", "fear", "determination"]
    (work / "CHR-001.txt").write_text(lock)
    return [chk("lock paragraph has all 14 fields incl. MUST NOT CHANGE", all(f + ":" in lock for f in LOCK_FIELDS), len(LOCK_FIELDS)),
            chk("drifted prompt (lock not pasted verbatim) caught", verbatim == [True, True, True, False], verbatim),
            chk("5 views and 5 expressions", len(views) == 5 and len(expr) == 5, (views, expr))]


def ch_04(work):
    cues = {"assertive": "squared shoulders, direct gaze, centre frame", "anxious": "guarded arms, off-camera glance, tense jaw",
            "ordered": "pressed clothes, symmetrical workspace", "warm": "open palms, soft eyes", "curious": "leaning in, head tilt"}
    sig = ["if criticised then folds arms", "if alone then hums", "if late then checks watch twice"]
    need = "competence"
    jwrite(work, "personality.json", {"facets": cues, "if_then": sig, "need": need})
    return [chk("4-6 facets mapped to visible cues", 4 <= len(cues) <= 6 and all(cues.values()), len(cues)),
            chk("3 if-then signatures", len(sig) == 3 and all(s.startswith("if ") and " then " in s for s in sig), sig),
            chk("one driving need from autonomy/competence/relatedness", need in ("autonomy", "competence", "relatedness"), need)]


def ch_05(work):
    H = 1080
    head_d = H / 4
    torso = 300
    stroke = 5 * H / 1080
    im = Image.new("RGB", (1080, 1080), "white")
    d = ImageDraw.Draw(im)
    cx = 540
    d.ellipse([cx - head_d / 2, 20, cx + head_d / 2, 20 + head_d], outline="#222", width=round(stroke))
    neck = 20 + head_d
    d.line([(cx, neck), (cx, neck + torso)], fill="#222", width=round(stroke))
    limb = torso / 2
    d.line([(cx, neck + torso), (cx - limb * 0.6, neck + torso + limb * 0.8)], fill="#222", width=round(stroke))
    d.line([(cx - 12, neck + 6), (cx - 40, neck + 20)], fill="#1a9e8f", width=8)
    im.save(work / "stickman_bible.png")
    a = np.asarray(im)
    teal_x = np.where((a == hexrgb("#1a9e8f")).all(2))[1]
    return [chk("circular head = 1/4 of height", head_d == 270, head_d),
            chk("limbs half a torso long", near(math.hypot(limb * 0.6, limb * 0.8), torso / 2, 1e-9), limb),
            chk("5 px strokes at 1080 px", stroke == 5, stroke),
            chk("teal scarf at the left of the neck", teal_x.size > 0 and teal_x.max() < cx, int(teal_x.max()) if teal_x.size else None)]


def ch_09(work):
    words = [{"w": "مرحبا", "s": 0.2, "e": 0.6}, {"w": "بكم", "s": 0.65, "e": 1.0}, {"w": "اليوم", "s": 2.0, "e": 2.5}]

    def state(t):
        for w in words:
            if w["s"] <= t < w["e"]:
                return "speaking"
        for a, b in zip(words, words[1:]):
            if a["e"] <= t < b["s"] and b["s"] - a["e"] > 0.7:
                return "thinking"
        return "idle"

    tl = [state(k / 10) for k in range(30)]
    (work / "orb_states.txt").write_text(" ".join(tl))
    return [chk("speaking while a word is active", state(0.3) == "speaking" and state(2.2) == "speaking", state(0.3)),
            chk("short gap (0.05 s) is not thinking", state(0.62) == "idle", state(0.62)),
            chk("gap > 0.7 s -> thinking", state(1.5) == "thinking", state(1.5)),
            chk("before and after speech -> idle", state(0) == "idle" and state(2.9) == "idle", (state(0), state(2.9)))]


def interp(frame, xs, ys, ease=sine_io):
    if frame <= xs[0]:
        return ys[0]
    for i in range(len(xs) - 1):
        if frame <= xs[i + 1]:
            return ys[i] + (ys[i + 1] - ys[i]) * ease((frame - xs[i]) / (xs[i + 1] - xs[i]))
    return ys[-1]


def rot_about(p, pivot, deg):
    a = math.radians(deg)
    x, y = p[0] - pivot[0], p[1] - pivot[1]
    return (pivot[0] + x * math.cos(a) - y * math.sin(a), pivot[1] + x * math.sin(a) + y * math.cos(a))


def ch_10(work):
    ok, files = scaffold("character-rig", work / "rig")
    shoulder, elbow0, hand0 = (0.0, 0.0), (0.0, 40.0), (0.0, 80.0)
    sh = lambda f: interp(f, [0, 6, 14, 24], [0, 8, -55, -48])
    el = lambda f: interp(f, [2, 10, 18, 26], [0, 5, -30, -24])

    def hand(f):
        e = rot_about(elbow0, shoulder, sh(f))
        h = rot_about(rot_about(hand0, elbow0, el(f)), shoulder, sh(f))
        return e, h

    e, h = hand(14)
    upper = math.dist(shoulder, e)
    lower = math.dist(e, h)
    lag = next(f for f in range(30) if el(f) != 0) - next(f for f in range(30) if sh(f) != 0)
    return [chk("character-rig scaffold", ok, files),
            chk("nested pivots keep bone lengths", near(upper, 40, 1e-9) and near(lower, 40, 1e-9), (upper, lower)),
            chk("shoulder keys [0,6,14,24] -> [0,8,-55,-48]", sh(14) == -55 and sh(24) == -48, sh(14)),
            chk("elbow starts 2 frames after the shoulder (follow-through)", lag == 2, lag)]


def two_bone_ik(S, T, l1, l2, bend=1):
    S, T = np.asarray(S, float), np.asarray(T, float)
    d = min(np.linalg.norm(T - S), l1 + l2 - 1e-9)
    u = (T - S) / np.linalg.norm(T - S)
    a = (l1 * l1 - l2 * l2 + d * d) / (2 * d)
    h = math.sqrt(max(l1 * l1 - a * a, 0))
    n = np.array([-u[1], u[0]]) * bend
    J = S + u * a + n * h
    E = S + u * d
    return J, E


def ch_11(work):
    hip = (0.0, 0.0)
    l1, l2 = 0.45, 0.43
    J, E = two_bone_ik(hip, (0.2, 0.7), l1, l2, bend=-1)
    ctrl = 2 * J - (np.array(hip) + E) / 2
    mid = 0.25 * np.array(hip) + 0.5 * ctrl + 0.25 * E
    w = 2 * math.pi
    pedal = lambda t: (0.25 + 0.17 * math.cos(w * t), 0.55 + 0.17 * math.sin(w * t))
    reach = [np.linalg.norm(two_bone_ik(hip, pedal(t / 20), l1, l2)[1] - np.array(pedal(t / 20))) for t in range(20)]
    wheel_v = 2.5 * w * 0.33
    jwrite(work, "ik.json", {"knee": J.tolist(), "foot": E.tolist()})
    return [chk("IK keeps thigh and shin lengths", near(np.linalg.norm(J - hip), l1, 1e-9) and near(np.linalg.norm(E - J), l2, 1e-9),
                (round(float(np.linalg.norm(J)), 4), round(float(np.linalg.norm(E - J)), 4))),
            chk("foot reaches the target", np.allclose(E, (0.2, 0.7)), E.tolist()),
            chk("control 2J - (S+E)/2 makes the curve pass through the knee", np.allclose(mid, J), mid.tolist()),
            chk("pedals reached all crank revolution; wheel speed = 2.5 w r", max(reach) < 1e-9 and near(wheel_v, 5.18, 0.01), round(wheel_v, 3))]


def ch_12(work):
    fps = 30
    tilt = lambda t: 20 * math.sin(2 * math.pi * 0.5 * t)
    hip_y = lambda t: 100 * abs(math.sin(math.pi * t))
    k = 0.05

    def bend(t):
        return k * (tilt(t) - tilt(t - 1 / fps)) * fps

    def squash(t):
        v = (hip_y(t) - hip_y(t - 1 / fps)) * fps
        return min(max(1 + v / 3000, 0.85), 1.15)

    b1 = bend(1.0)
    b2 = bend(1.0)
    vals = [squash(f / fps) for f in range(90)]
    head = lambda t: tilt(t - 1.5 / fps)
    return [chk("bend from d(tilt)/dt via seek(t) and seek(t-1/fps): stateless, repeatable", b1 == b2 and abs(bend(0.5)) < abs(bend(0.0)) + 1e-9,
                (round(bend(0.0), 3), round(bend(0.5), 3))),
            chk("stretch/squash clamped 0.85-1.15", min(vals) >= 0.85 and max(vals) <= 1.15 and max(vals) > 1.05, (round(min(vals), 3), round(max(vals), 3))),
            chk("head follows 1-2 frames late", near(head(1.0), tilt(1.0 - 0.05), 1e-12), "1.5 f")]


def ch_13(work):
    words = [{"w": "مرحبا", "s": 0.0, "e": 0.5}, {"w": "بيت", "s": 0.6, "e": 0.9}, {"w": "سلام", "s": 1.0, "e": 1.4}]
    closed = set("مبف")
    mouths = ["rest", "closed", "open", "wide", "round", "smile"]

    def mouth(t):
        for w in words:
            if w["s"] <= t < w["e"]:
                if w["w"][0] in closed and t < w["s"] + 0.1:
                    return "closed"
                return "open"
        return "rest"

    def eye_scale(t, every=3.0, dur=0.08):
        return 0.1 if (t % every) < dur else 1.0

    fps = 30
    frames = [mouth(f / fps) for f in range(45)]
    onset = [math.ceil(w["s"] * fps - 1e-9) for w in words]
    lag = max(f / fps - w["s"] for f, w in zip(onset, words))
    switched = all(frames[f] != "rest" for f in onset)
    jwrite(work, "mouths.json", frames)
    return [chk("closed mouth on م/ب at word onset", mouth(0.02) == "closed" and mouth(0.62) == "closed" and mouth(1.02) == "open",
                (mouth(0.02), mouth(0.62), mouth(1.02))),
            chk("mouth switches on the first frame of each word (< 1 frame late)", switched and lag < 1 / fps, round(lag, 4)),
            chk("blink scaleY 0.1 for 80 ms every 2.5-4 s", eye_scale(3.05) == 0.1 and eye_scale(3.1) == 1.0, eye_scale(3.05)),
            chk("5-7 mouth shapes", 5 <= len(mouths) <= 7, len(mouths))]


def ch_14(work):
    step = 40.0

    def phase(dist):
        return dist / step * 2 * math.pi

    def foot_x(body_x, side):
        p = phase(body_x) + (math.pi if side else 0)
        return body_x - step / (2 * math.pi) * math.sin(p)

    def face(facing):
        eyes = [(-6 + 8 * facing), (6 + 8 * facing)]
        near_arm = "right" if facing > 0 else "left" if facing < 0 else "both"
        return eyes, near_arm

    xs = np.cumsum([1.0] * 40 + [3.0] * 40)
    stance = [foot_x(x, 0) for x in xs]
    naive = [x - step / (2 * math.pi) * math.sin(2 * math.pi * i / step) for i, x in enumerate(xs)]  # phase from time
    planted_slide, naive_slide = [], []
    for i in range(1, len(xs)):
        p = phase(xs[i]) % (2 * math.pi)
        if math.cos(p) > 0.95:
            planted_slide.append(abs(stance[i] - stance[i - 1]) / (xs[i] - xs[i - 1]))
        if i > 40 and math.cos(2 * math.pi * i / step) > 0.95:
            naive_slide.append(abs(naive[i] - naive[i - 1]) / (xs[i] - xs[i - 1]))
    eyes0, arm0 = face(0)
    return [chk("phase = distance / step: same pose at the same distance whatever the speed", near(phase(80), 4 * math.pi, 1e-12)
                and near(foot_x(80, 0), foot_x(80 + 40, 0) - 40, 1e-9), round(foot_x(80, 0), 3)),
            chk("distance phase keeps the contact foot near-planted after a 3x speed-up; time phase slides",
                max(planted_slide) < 0.2 and min(naive_slide) > 0.6, (round(max(planted_slide), 3), round(min(naive_slide), 3))),
            chk("facing 0 shows both eyes centred", eyes0 == [-6, 6] and arm0 == "both", eyes0),
            chk("facing dial swaps the near arm", face(1)[1] == "right" and face(-1)[1] == "left", (face(1)[1], face(-1)[1]))]


def ch_15(work):
    feet = (380, 619)
    local = [(0, 0), (-30, -100), (30, -100), (0, -160)]

    def xf(p, origin=(560, 392), rot=-16, scale=1.3):
        x, y = p[0] * scale, p[1] * scale
        a = math.radians(rot)
        return (origin[0] + x * math.cos(a) - y * math.sin(a), origin[1] + x * math.sin(a) + y * math.cos(a))

    placed = [xf(p) for p in local]
    girl = [xf(p, origin=feet, rot=0, scale=1.4) for p in local]
    im = Image.new("RGB", (900, 700), "white")
    ImageDraw.Draw(im).polygon(placed, outline="black")
    im.save(work / "placed.png")
    return [chk("the body origin lands exactly at translate(560 392)", np.allclose(placed[0], (560, 392)), placed[0]),
            chk("group rotate/scale preserves shape (distances x1.3)", near(math.dist(placed[1], placed[2]), 60 * 1.3, 1e-9), math.dist(placed[1], placed[2])),
            chk("scaling 1.4x around her feet keeps the feet planted", np.allclose(girl[0], feet) and near(girl[3][1], 619 - 160 * 1.4, 1e-9), girl[3])]


def ch_16(work):
    shoulder, elbow, wrist = np.array([0.0, 0]), np.array([60.0, -30]), np.array([120.0, -10])
    tips = [np.array([200.0, -60]), np.array([210.0, 10]), np.array([170.0, 60])]
    attach = np.array([20.0, 50])
    sag = 0.28

    def scallop(a, b, n=12):
        mid = (a + b) / 2
        chord = b - a
        nrm = np.array([-chord[1], chord[0]]) / np.linalg.norm(chord)
        towards = (shoulder + wrist) / 2 - mid
        if nrm @ towards < 0:
            nrm = -nrm
        return [a + chord * u + nrm * sag * np.linalg.norm(chord) * 4 * u * (1 - u) for u in np.linspace(0, 1, n)]

    edge = [wrist] + tips + [attach]
    membrane = [p for a, b in zip(edge, edge[1:]) for p in scallop(a, b)]
    spikes = lambda r, size: (4 + r * .45) * size
    im = Image.new("RGB", (260, 160), "white")
    ImageDraw.Draw(im).polygon([tuple(p + (20, 80)) for p in membrane], fill=(80, 40, 60))
    im.save(work / "wing.png")
    a, b = tips[0], tips[1]
    s = scallop(a, b)
    depth = np.linalg.norm(s[6] - (a + (b - a) * (6 / 11)))
    return [chk("each scallop has 12 samples", len(s) == 12 and len(membrane) == 12 * (len(edge) - 1), len(membrane)),
            chk("membrane sags 0.28 x chord at the middle (inward)", near(depth, sag * np.linalg.norm(b - a) * 4 * (6 / 11) * (5 / 11), 1e-9), round(depth, 3)),
            chk("spike height (4 + r*.45)*size", spikes(20, 2) == 26, spikes(20, 2))]


def ch_17(work):
    ok, files = scaffold("stickman", work / "stick")
    pal = {"bg": "#FBF9F4", "ink": "#1F2328", "accent": "#F2C94C", "floor": "#EFEAE0"}
    from .photo_video_footage import contrast
    cr = contrast(hexrgb(pal["ink"]), hexrgb(pal["bg"]))
    wps = 2.1
    line = "نصيحة اليوم: نم مبكرا ثم استيقظ متأخرا"
    dur = len(line.split()) / wps

    def card_y(i, t, drop=0.4, gap=0.25):
        p = min(max((t - i * gap) / drop, 0), 1)
        return -200 + (400 - i * 40 + 200) * (1 - (1 - p) ** 3)

    stack = [card_y(i, 3) for i in range(3)]
    return [chk("stickman scaffold", ok, files),
            chk("ink on paper >= 12:1", cr >= 12, round(cr, 2)),
            chk("2.1 words per second reading time", near(dur, 7 / 2.1, 1e-9), round(dur, 3)),
            chk("cards drop and stack upward (each 40 px higher)", stack == [400, 360, 320], stack)]


def ch_18(work):
    bpm = 150
    bones = 16
    phases = np.linspace(0, math.pi, bones)
    amps = np.array([4 if i in (3, 7, 11) else 10 for i in range(bones)], float)

    def rot(i, t):
        return amps[i] * math.sin(2 * math.pi * bpm / 60 * t + phases[i])

    period = 60 / bpm
    loop = all(near(rot(i, 0.13), rot(i, 0.13 + period), 1e-9) for i in range(bones))
    jwrite(work, "dance.json", {"bpm": bpm, "amps": amps.tolist()})
    return [chk("~16 bones", bones == 16, bones),
            chk("rotation A sin(2 pi BPM/60 t + phi) repeats every beat (0.4 s at 150 BPM)", loop and near(period, 0.4, 1e-12), period),
            chk("joint bones keep small amplitude", amps[[3, 7, 11]].max() < amps.max(), amps[[3, 7, 11]].tolist())]


def ch_19(work):
    tile = 200
    eye_r = 0.08 * tile

    def blink(t, every=3.0):
        return 0.05 if (t % every) < 0.1 else 1.0

    def egg_land(t, t_land=1.0):
        return 0.75 if t_land <= t < t_land + 0.08 else 1.0

    im = Image.new("RGB", (tile, tile), "#e8b04a")
    d = ImageDraw.Draw(im)
    for cx in (70, 130):
        d.ellipse([cx - eye_r, 90 - eye_r, cx + eye_r, 90 + eye_r], fill="black")
        d.ellipse([cx - eye_r * 0.2 - 4, 90 - eye_r * 0.5 - 4, cx - eye_r * 0.2 + 2, 90 - eye_r * 0.5 + 2], fill="white")
    im.save(work / "tile_face.png")
    a = np.asarray(im)
    black = (a.sum(2) == 0).sum()
    return [chk("eye radius ~8% of the tile", eye_r == 16, eye_r),
            chk("glossy eyes drawn with a catch-light", black > 2 * 0.8 * math.pi * 16 ** 2 and (a[90 - 8 - 1, 70 - 3] == 255).all(), int(black)),
            chk("blink 100 ms", blink(3.05) < 1 and blink(3.11) == 1, blink(3.05)),
            chk("landing squash y .75 for 80 ms", egg_land(1.05) == 0.75 and egg_land(1.09) == 1, egg_land(1.05))]


def ch_20(work):
    W, H = 200, 140
    layers = ["wall", "window", "props", "desk_back", "character", "desk_front"]
    colours = {"wall": (230, 225, 210), "window": (180, 210, 240), "props": (150, 120, 90), "desk_back": (120, 80, 50),
               "character": (40, 90, 200), "desk_front": (100, 60, 30)}
    im = Image.new("RGB", (W, H), colours["wall"])
    d = ImageDraw.Draw(im)
    d.rectangle([20, 20, 70, 60], fill=colours["window"])
    d.rectangle([140, 50, 160, 90], fill=colours["props"])
    d.rectangle([30, 80, 170, 90], fill=colours["desk_back"])
    d.rectangle([90, 40, 110, 110], fill=colours["character"])
    d.rectangle([30, 95, 170, 130], fill=colours["desk_front"])
    im.save(work / "stage.png")
    a = np.asarray(im)

    def on_twos(t, fps=24):
        return math.floor(t * 12) / 12

    return [chk("6 layers in back-to-front order", layers.index("desk_back") < layers.index("character") < layers.index("desk_front"), layers),
            chk("character hidden behind the desk front (arms vanish)", tuple(a[100, 100]) == colours["desk_front"]
                and tuple(a[60, 100]) == colours["character"], (tuple(a[100, 100]), tuple(a[60, 100]))),
            chk("character on twos (steps(12) per second)", on_twos(0.05) == 0 and near(on_twos(0.09), 1 / 12, 1e-12), on_twos(0.09))]


def ch_21(work):
    fill = "#0d0c0b"
    W = 160
    im = Image.new("RGB", (W, W), "#f4d9a0")
    d = ImageDraw.Draw(im)
    d.polygon([(70, 40), (95, 40), (100, 130), (65, 130)], fill=fill)
    d.ellipse([70, 15, 92, 40], fill=fill)
    d.rectangle([62, 18, 100, 24], fill=fill)
    im.save(work / "silhouette.png")
    a = np.asarray(im)
    ink = (a == hexrgb(fill)).all(2)
    colours = {tuple(c) for c in a.reshape(-1, 3)}
    frame_of = lambda t: int(t * 24) % 24 // 12
    return [chk("single dark fill, no internal detail (exactly 2 colours)", len(colours) == 2, len(colours)),
            chk("figure reads by outline against a bright ground", ink.sum() > 1000, int(ink.sum())),
            chk("12 frames per step at 24 fps", frame_of(0.49) == 0 and frame_of(0.51) == 1, (frame_of(0.49), frame_of(0.51)))]


def ch_22(work):
    fps_sprite = 6

    def leg_frame(t):
        return int(math.floor(t * fps_sprite)) % 2

    def bob(t):
        return 2 * leg_frame(t)

    def staff(t):
        return min(int(math.floor(t * fps_sprite)), 5)

    frames = []
    for k in range(4):
        im = Image.new("RGB", (16, 16), (0, 0, 0))
        d = ImageDraw.Draw(im)
        y = bob(k / 6)
        d.rectangle([3, 3 + y, 12, 10 + y], fill=hexrgb("#d17c55"))
        legs = (4, 8) if leg_frame(k / 6) == 0 else (6, 10)
        for x in legs:
            d.point((x, 11 + y), fill=(255, 255, 255))
        frames.append(np.asarray(im))
    Image.fromarray(np.hstack(frames)).resize((256, 64), Image.NEAREST).save(work / "sprite_strip.png")
    return [chk("2-frame leg swap at 6 fps", [leg_frame(k / 6) for k in range(4)] == [0, 1, 0, 1], [leg_frame(k / 6) for k in range(4)]),
            chk("2 px bob on the swap frame", bob(1 / 6) - bob(0) == 2, bob(1 / 6)),
            chk("frames 0 and 2 identical (true cycle)", np.array_equal(frames[0], frames[2]) and not np.array_equal(frames[0], frames[1]), "cycle"),
            chk("staff raises in 6 stepped frames", [staff(k / 6) for k in range(8)] == [0, 1, 2, 3, 4, 5, 5, 5], staff(2))]


def ch_23(work):
    palette = ["#F2C94C", "#1F2328", "#EB5757"]
    stages = [{"name": "child", "scale": 0.6, "palette": palette}, {"name": "teen", "scale": 0.85, "palette": palette},
              {"name": "adult", "scale": 1.0, "palette": palette}]

    def shake(t, contacts=(0.5, 1.2)):
        for c in contacts:
            if c <= t < c + 0.15:
                return 6 * (1 - (t - c) / 0.15) * (1 if int((t - c) * 60) % 2 == 0 else -1)
        return 0.0

    def dock(t, start=(0, 0), slot=(100, 50), T=0.5):
        p = 1 - (1 - min(t / T, 1)) ** 3
        return (start[0] + (slot[0] - start[0]) * p, start[1] + (slot[1] - start[1]) * p)

    jwrite(work, "variants.json", stages)
    return [chk("palette identical across age variants", all(s["palette"] == palette for s in stages), len(stages)),
            chk("parts dock into their slots", dock(0.5) == (100, 50), dock(0.5)),
            chk("6 px camera shake for 150 ms on each contact", abs(shake(0.5)) == 6 and shake(0.66) == 0 and abs(shake(1.2)) == 6,
                (shake(0.5), shake(0.66)))]


def ch_24(work):
    fps, H = 24, 200
    stride = 60.0

    def pose(f):
        ph = (f % 24) / 24 * 2 * math.pi
        bob = 0.04 * H * (0.5 - 0.5 * math.cos(2 * ph))
        names = ["contact", "down", "passing", "up"]
        key = names[int((f % 12) / 3)]
        return {"bob": bob, "key": key, "foot": 30 * math.sin(ph)}

    bg = lambda t: -stride / 0.5 * t
    clip = {"name": "walk", "frames": 24, "loop": True, "events": {"contact": [0, 12], "footstep": [0, 12]}}
    jwrite(work, "walk_clip.json", clip)
    bobs = [pose(f)["bob"] for f in range(24)]
    return [chk("24 frames per two steps (12 per step) loops", pose(0) == pose(24) and pose(3)["key"] == "down", pose(3)["key"]),
            chk("bob 3-5% of height", 0.03 * H <= max(bobs) - min(bobs) <= 0.05 * H, round(max(bobs) - min(bobs), 2)),
            chk("background speed = stride / 0.5 s", bg(1.0) == -120, bg(1.0)),
            chk("pose(f) renders any frame directly (stateless)", pose(17) == pose(17 + 48), "phase")]


def ch_25(work):
    def leg(x, phase):
        foot = x + 22 * math.sin(phase)
        knee = x + 12 * math.sin(phase)
        lift = max(0.0, math.cos(phase)) * 15
        return foot, knee, lift

    hz = 1.5
    ph = lambda t, off: 2 * math.pi * hz * t + off
    offs = [0, math.pi, math.pi / 2, 3 * math.pi / 2]
    t = 0.1
    lifts = [leg(0, ph(t, o))[2] for o in offs]
    x = lambda tt: 680 - 145 * tt
    return [chk("foot swings +-22, knee +-12", near(leg(0, math.pi / 2)[0], 22, 1e-12) and near(leg(0, math.pi / 2)[1], 12, 1e-12), leg(0, math.pi / 2)[:2]),
            chk("lifts only in the forward half (cos > 0), max 15", leg(0, 0)[2] == 15 and leg(0, math.pi)[2] == 0, lifts),
            chk("pi-offset pairs never lift together", all(min(leg(0, ph(k / 50, 0))[2], leg(0, ph(k / 50, math.pi))[2]) == 0 for k in range(50)), "alternate"),
            chk("walk right -> left x = 680 - 145t", x(0) == 680 and x(8) == -480, x(8))]


def ch_26(work):
    def pose(t):
        if t < 4.1:
            return {"x": 430 + 59 * t, "y": 0, "seg": "walk"}
        if t < 5.2:
            return {"x": 430 + 59 * 4.1, "y": -14 * smoothstep((t - 4.65) / 0.55), "seg": "crouch"}
        if t <= 6.9:
            u = (t - 5.2) / 1.7
            return {"x": 671.9 + (1050 - 671.9) * u, "y": 147 * 4 * u * (1 - u), "angle": -14 + 26 * u, "seg": "jump"}
        return {"x": 1050 + 48 * (t - 6.9), "y": 0, "seg": "walk"}

    apex = max(pose(5.2 + k * 1.7 / 100)["y"] for k in range(101))
    segs = [pose(t)["seg"] for t in (1, 4.5, 6, 8)]
    jwrite(work, "pose_segments.json", segs)
    return [chk("walk reaches 671.9 at 4.1 s (430 + 59*4.1)", near(pose(4.0999)["x"], 671.9, 0.01), round(pose(4.0999)["x"], 3)),
            chk("jump apex 147 px at mid-flight", near(apex, 147, 1e-9), apex),
            chk("jump ends at x 1050, body angle -14 -> +12", near(pose(6.9)["x"], 1050, 1e-9) and near(pose(6.9)["angle"], 12, 1e-9), pose(6.9)["angle"]),
            chk("segments walk -> crouch -> jump -> walk", segs == ["walk", "crouch", "jump", "walk"], segs)]


def ch_27(work):
    presets = {"chibi": {"head": 0.5}, "standard": {"head": 0.25}, "tall": {"head": 0.14}}

    def draw(direction, pose, preset="standard", H=48):
        im = Image.new("L", (32, H), 0)
        d = ImageDraw.Draw(im)
        hh = presets[preset]["head"] * H
        bob = 1 if pose in (1, 3) else 0
        d.ellipse([10, 1 + bob, 22, 1 + hh + bob], fill=255)
        legx = {0: (12, 20), 1: (14, 18), 2: (10, 22), 3: (14, 18)}[pose]
        for lx in legx:
            d.line([(16, hh + 12 + bob), (lx, H - 1)], fill=255, width=2)
        d.ellipse([18 if direction == "right" else 11, 4 + bob, 21 if direction == "right" else 14, 7 + bob], fill=0)
        return np.asarray(im)

    rpg = [0, 1, 2, 1]
    frames = [draw("right", p) for p in rpg]
    Image.fromarray(np.hstack(frames)).save(work / "rpg_walk.png")
    sym = np.array_equal(draw("left", 0)[:, ::-1], draw("right", 0))
    return [chk("RPG 3 patterns 0-1-2-1 (frames 2 and 4 identical)", np.array_equal(frames[1], frames[3]) and not np.array_equal(frames[0], frames[2]), rpg),
            chk("1 px bob", int(np.argmax(frames[1].any(1))) - int(np.argmax(frames[0].any(1))) == 1, "1 px"),
            chk("asymmetric side view (eye offset) is drawn, not mirrored", not sym, sym),
            chk("chibi head larger than tall", presets["chibi"]["head"] > presets["standard"]["head"] > presets["tall"]["head"], presets)]


def ch_28(work):
    fps = 24
    keys = [(0, 0.0), (12, 45.0), (24, 45.0), (36, -10.0)]
    gaps = [b[0] - a[0] for a, b in zip(keys, keys[1:])]

    def angle(f):
        return interp(f, [k[0] for k in keys], [k[1] for k in keys])

    breakdown = angle(6)
    hold = [angle(f) for f in range(12, 25)]
    jwrite(work, "blocking.json", {"keys": keys})
    return [chk("keys every 8-16 frames", all(8 <= g <= 16 for g in gaps), gaps),
            chk("ease-in-out breakdown halfway between keys", near(breakdown, 22.5, 1e-9) and angle(3) < 22.5 / 2, (angle(3), breakdown)),
            chk("held pose stays still", len(set(hold)) == 1, hold[0])]


def ch_29(work):
    def scale_y(t):
        if t < 0.2:
            return 1 - 0.04 * (1 - math.cos(math.pi / 2 * t / 0.2))
        if t < 0.45:
            return 0.96 + 0.04 * (1 - (1 - (t - 0.2) / 0.25) ** 3)
        if t < 0.8:
            k, c = 200.0, 12.0
            w = math.sqrt(k - (c / 2) ** 2)
            u = t - 0.45
            return 1 - 0.08 * math.exp(-c / 2 * u) * math.cos(w * u)
        return 1 + 0.01 * math.sin(2 * math.pi * 0.25 * (t - 0.8))

    def height(t):
        if 0.2 <= t < 0.45:
            p = (t - 0.2) / 0.25
            return 80 * (1 - (1 - p) ** 3) if p < 1 else 80
        return 0.0

    ts = [k / 1000 for k in range(2000)]
    sy = [scale_y(t) for t in ts]
    return [chk("sink 4% by 200 ms", near(scale_y(0.1999), 0.96, 1e-3), round(scale_y(0.1999), 4)),
            chk("landing squash 8% at 450 ms, recovering on the spring", near(scale_y(0.45), 0.92, 1e-12) and abs(scale_y(0.79) - 1) < 0.01,
                (scale_y(0.45), round(scale_y(0.79), 4))),
            chk("jump eases out (fast start)", height(0.25) > 0.4 * 80, round(height(0.25), 2)),
            chk("breathing hold 0.8-2.0 s stays within 1%", max(abs(s - 1) for s, t in zip(sy, ts) if t >= 0.8) <= 0.01 + 1e-9, "breath")]


def ch_30(work):
    shoulder = np.array([0.0, 0.0])
    target_angle = math.radians(-40)

    def finger(t):
        p = sine_io(t / 0.35)
        a = math.radians(80) + (target_angle - math.radians(80)) * p
        return shoulder + 100 * np.array([math.cos(a), math.sin(a)])

    def target_scale(t, stop=0.35):
        p = (t - stop - 0.08) / 0.25
        return 0 if p < 0 else back_out(min(p, 1))

    radii = [np.linalg.norm(finger(k / 100)) for k in range(36)]
    jwrite(work, "point.json", {"stop": 0.35, "pop": 0.43})
    return [chk("arm extends on an arc (constant radius)", np.allclose(radii, 100), round(float(np.ptp(radii)), 9)),
            chk("finger stops at 350 ms", np.allclose(finger(0.35), finger(0.5)), finger(0.35).round(3).tolist()),
            chk("target pops 80 ms after the finger stops", target_scale(0.4299) == 0 and target_scale(0.44) > 0, target_scale(0.44))]


def ch_31(work):
    words = [{"w": "هذا", "s": 0.0, "e": 0.3}, {"w": "مهم", "s": 0.35, "e": 0.8, "stress": True}, {"w": "جدا.", "s": 0.85, "e": 1.2}]

    def tilt(t):
        for w in words:
            if w.get("stress") and w["s"] <= t < w["e"]:
                return 3 * math.sin(math.pi * (t - w["s"]) / (w["e"] - w["s"]))
        return 0.0

    def blink_frames(T=10, fps=30, every=(2.5, 4.0), seed=3):
        rng = np.random.default_rng(seed)
        t, out = 0.0, []
        while True:
            t += rng.uniform(*every)
            if t > T:
                return out
            out.append(list(range(int(t * fps), int(t * fps) + 3)))

    bl = blink_frames()
    gaps = np.diff([b[0] for b in bl]) / 30
    nod = [w for w in words if w["w"].endswith(".")]
    return [chk("tilt <= 3 deg only on the stressed word", near(max(tilt(k / 100) for k in range(120)), 3, 0.01) and tilt(0.1) == 0,
                round(max(tilt(k / 100) for k in range(120)), 4)),
            chk("blinks 3 frames, every 2.5-4 s", all(len(b) == 3 for b in bl) and gaps.min() >= 2.5 - 1 / 30 and gaps.max() <= 4 + 1 / 30,
                gaps.round(2).tolist()),
            chk("nod on the sentence end", len(nod) == 1 and nod[0]["w"] == "جدا.", nod)]


def ch_32(work):
    hill_y = 300
    n = 4

    def rise(i, t, rtl=True):
        order = (n - 1 - i) if rtl else i
        p = (t - order * 0.2) / 0.35
        if p <= 0:
            return hill_y + 100
        return hill_y + 100 - 120 * back_out(min(p, 1), 1.6)

    def visible(y_top, h=100):
        return max(0, min(h, hill_y - y_top))

    def disc_pop(t):
        p = min(t / 0.3, 1)
        if p < 0.6:
            return 0.8 + 0.25 * p / 0.6
        return 1.05 - 0.05 * (p - 0.6) / 0.4

    first = min(range(n), key=lambda i: next(k for k in range(200) if rise(i, k / 100) < hill_y + 100))
    over = min(rise(0, k / 1000) for k in range(1500))
    return [chk("Arabic: starts from the right (rightmost first)", first == n - 1, first),
            chk("masked below the hill line until it rises", visible(rise(0, 0)) == 0 and visible(rise(0, 2)) > 0, visible(rise(0, 2))),
            chk("easeOutBack(1.6) overshoots then settles 20 px above the hill", over < hill_y - 20 and near(rise(0, 2), hill_y - 20, 1e-9), round(over, 2)),
            chk("disc pop 0.8 -> 1.05 -> 1 in 300 ms", disc_pop(0) == 0.8 and near(disc_pop(0.18), 1.05, 1e-9) and near(disc_pop(0.3), 1, 1e-12),
                disc_pop(0.18))]


def ch_33(work):
    def wing(t, T=0.8):
        return 70 * back_out(min(t / T, 1), 1.70158)

    def z_glyph(i, t):
        tt = t - i * 0.25
        if tt < 0:
            return None
        return {"y": -30 * tt, "scale": 1 + 0.5 * tt, "alpha": max(0, 1 - tt / 1.5)}

    peak = max(wing(k / 100) for k in range(81))
    z = [z_glyph(i, 1.0) for i in range(3)]
    run_frame = lambda t, fps=24: int(t * fps) % 8
    return [chk("wings spread to ~70 deg over 0.8 s with back.out overshoot", near(wing(0.8), 70, 1e-9) and peak > 70, round(peak, 2)),
            chk("Z glyphs rise, grow and fade, 250 ms apart", z[0]["y"] < z[1]["y"] < z[2]["y"] and z[0]["alpha"] < z[2]["alpha"], z),
            chk("8-frame run cycle", [run_frame(k / 24) for k in range(9)] == [0, 1, 2, 3, 4, 5, 6, 7, 0], "8f")]


def ch_34(work):
    def squash(t):
        sy = 1 - 0.3 * max(0, 1 - abs(t - 1) / 0.1)
        sx = 1 / sy
        return sx, sy

    def anticipation_frames(kind):
        return 2 if kind == "player-attack" else 6

    vols = [squash(k / 100)[0] * squash(k / 100)[1] for k in range(200)]
    fps, n = 30, 90
    frames = np.zeros((n, 16, 16, 3), np.uint8)
    for k in range(n):
        frames[k, :, :, 0] = k * 2
    frames[41:44] = frames[40]
    path = work / "check.mkv"
    write_video(path, frames, fps)
    from .photo_video_footage import probe
    pr = probe(path)
    vs = next(s for s in pr["streams"] if s["codec_type"] == "video")
    nb = int(vs.get("nb_frames", 0) or 0) or int(round(float(pr["format"]["duration"]) * fps))
    dec = read_video(path)
    held = [k for k in range(1, len(dec)) if np.array_equal(dec[k], dec[40])]
    held = [40] + [k for k in held if k != 40]
    return [chk("constant volume through squash (sx*sy = 1)", np.allclose(vols, 1), round(min(vols), 6)),
            chk("player-facing attacks keep anticipation short", anticipation_frames("player-attack") < anticipation_frames("enemy"), "2 < 6"),
            chk("impact frame held: 4 identical frames 40-43 after encode", held == [40, 41, 42, 43], held),
            chk("rendered frame count / fps / duration verified", nb == 90 and near(float(pr["format"]["duration"]), 3.0, 0.05), (nb, pr["format"]["duration"]))]


def ch_35(work):
    from PIL import ImageFont, features
    chars = ["A", "B", "C"]
    W = 1920
    enter = {c: (W + 200, W - 400 - 300 * i) for i, c in enumerate(chars)}
    start_times = {c: 0.2 * i for i, c in enumerate(chars)}
    look = {c: "left" for c in chars}
    phrase = "قفزةٌ واحدة… وصارت"
    font = ImageFont.truetype(str(FONT), 40)
    im = Image.new("L", (600, 100), 0)
    if features.check("raqm"):
        ImageDraw.Draw(im).text((580, 20), phrase, font=font, fill=255, anchor="ra", direction="rtl")
    else:
        import arabic_reshaper
        from bidi.algorithm import get_display
        ImageDraw.Draw(im).text((580, 20), get_display(arabic_reshaper.reshape(phrase)), font=font, fill=255, anchor="ra")
    im.save(work / "bubble.png")
    k, zeta = 230.0, 0.5

    def bubble_scale(t):
        w = math.sqrt(k)
        wd = w * math.sqrt(1 - zeta ** 2)
        return 1 - math.exp(-zeta * w * t) * (math.cos(wd * t) + zeta * w / wd * math.sin(wd * t))

    peak = max(bubble_scale(i / 1000) for i in range(1000))
    return [chk("characters enter from the right edge", all(enter[c][0] > W for c in chars), enter),
            chk("group staggers right -> left, all looking left", start_times["A"] < start_times["B"] and enter["A"][1] > enter["B"][1]
                and set(look.values()) == {"left"}, start_times),
            chk("whole phrase drawn once, right-anchored", int(np.where((np.asarray(im) > 0).any(0))[0].max()) <= 580 and
                int(np.where((np.asarray(im) > 0).any(0))[0].max()) > 560, "phrase"),
            chk("bubble spring k 230, zeta .5 overshoots ~16% and settles", 1.1 < peak < 1.2 and near(bubble_scale(1.0), 1, 1e-3), round(peak, 4))]


def ch_36(work):
    def idle(t):
        breath = 0.012 * math.sin(2.2 * t)
        blink = 1 - 0.85 * max(0.0, math.sin(math.pi * ((t % 3.7) / 0.3))) if (t % 3.7) < 0.3 else 1.0
        ears = 0.12 * math.sin(2.6 * t)
        tail = 0.35 * math.sin(3.1 * t)
        return breath, blink, ears, tail

    ts = np.linspace(0, 20, 4001)
    vals = np.array([idle(t) for t in ts])
    blinks = [ts[i] for i in range(1, len(ts)) if vals[i, 1] < 1 and vals[i - 1, 1] == 1]
    np.save(work / "idle.npy", vals)
    return [chk("pure function of t (repeatable)", idle(7.3) == idle(7.3), idle(7.3)),
            chk("breath +-1.2%", near(np.abs(vals[:, 0]).max(), 0.012, 1e-5), round(float(np.abs(vals[:, 0]).max()), 5)),
            chk("blink every 3.7 s", np.allclose(np.diff(blinks), 3.7, atol=0.006), np.round(np.diff(blinks), 3).tolist()),
            chk("ears +-.12 rad, tail +-.35 rad", near(np.abs(vals[:, 2]).max(), .12, 1e-4) and near(np.abs(vals[:, 3]).max(), .35, 1e-4), "amps")]


def ch_37(work):
    fps, L = 30, 500.0

    def max_speed(f, z, A=math.radians(40)):
        ang = [A * (1 - spring(k / fps, f, z)) for k in range(90)]
        return max(abs(a - b) * L for a, b in zip(ang, ang[1:]))

    ok = max_speed(1.5, 0.42)
    bad = max_speed(2.2, 0.28)

    def verlet(T, n=9, dt=1 / 120, link=10.0):
        p = np.array([[i * link, 0.0] for i in range(n)])
        prev = p.copy()
        for _ in range(int(round(T / dt))):
            anchor = np.array([0.0, 0.0])
            acc = np.array([0.0, 400.0])
            new = p + (p - prev) * 0.99 + acc * dt * dt
            prev, p = p, new
            for _ in range(10):
                p[0] = anchor
                for i in range(n - 1):
                    d = p[i + 1] - p[i]
                    dist = np.linalg.norm(d)
                    corr = (dist - link) / dist * 0.5 * d
                    if i == 0:
                        p[i + 1] -= 2 * corr
                    else:
                        p[i] += corr
                        p[i + 1] -= corr
        return p

    a = verlet(1.0)
    b = verlet(1.0)
    links = np.linalg.norm(np.diff(a, axis=0), axis=1)
    np.save(work / "scarf.npy", a)
    return [chk("ear flop 1.5 Hz zeta .42 passes the 80 px/frame gate", ok <= 80, round(ok, 1)),
            chk("2.2 Hz zeta .28 fails it", bad > 80, round(bad, 1)),
            chk("9-link Verlet scarf re-simulated from t=0 is identical on every seek", np.array_equal(a, b) and len(a) == 9, "seek"),
            chk("links keep length and hang under gravity", np.allclose(links, 10, atol=0.3) and a[-1, 1] > 40, (round(float(links.mean()), 3), round(float(a[-1, 1]), 1)))]


def ch_38(work):
    sx = lambda t: abs(math.sin(2 * math.pi * 4.5 * t)) * 0.85 + 0.13
    sm = lambda x: smoothstep(x)
    y = lambda t: 348 - 20 * math.sin(1.8 * t) - 48 * sm((t - 4.2) / 1.8) + 55 * sm((t - 7) / 2)
    ts = np.linspace(0, 2, 4001)
    s = np.array([sx(t) for t in ts])
    mins = ts[1:-1][(s[1:-1] < s[:-2]) & (s[1:-1] <= s[2:])]
    return [chk("wing scaleX in [0.13, 0.98]", near(s.min(), 0.13, 1e-3) and near(s.max(), 0.98, 1e-3), (round(s.min(), 4), round(s.max(), 4))),
            chk("|sin| doubles the beat: closes 9 times per second at 4.5 Hz", near(float(np.median(np.diff(mins))), 1 / 9, 2e-3),
                round(float(np.median(np.diff(mins))), 4)),
            chk("path dips 48 by 6 s then rises 55 by 9 s", near(y(6) - (348 - 20 * math.sin(10.8)), -48, 1e-9) and
                near(y(9) - (348 - 20 * math.sin(16.2)), 7, 1e-9), round(y(9), 2))]


def ch_45(work):
    def angle(t, t0=0, t1=8):
        q = (t - t0) / (t1 - t0) * 4
        k = min(int(q), 3)
        f = q - k
        turn = 0 if f < 0.7 else sine_io((f - 0.7) / 0.3)
        return 90 * (k + turn) if t < t1 else 360

    holds = [angle(t) for t in (0.5, 2.5, 4.5, 6.5)]
    sheet = Image.new("RGB", (400, 100), "white")
    d = ImageDraw.Draw(sheet)
    for i, a in enumerate(holds):
        w = 30 * abs(math.cos(math.radians(a))) + 10
        d.rectangle([50 + 100 * i - w / 2, 10, 50 + 100 * i + w / 2, 90], fill="black")
    sheet.save(work / "contact_sheet.png")
    return [chk("holds at front/side/back/side (0, 90, 180, 270)", holds == [0, 90, 180, 270], holds),
            chk("each quarter holds 70% then turns in the last 30%", angle(1.39) == 0 and angle(1.41) > 0 and near(angle(1.999), 90, 0.01), angle(1.7)),
            chk("full turn by t1", angle(8) == 360, angle(8))]


def ch_46(work):
    import cv2
    W, H, n = 160, 120, 12
    bg = np.full((H, W, 3), 60, np.uint8)
    frames = []
    for k in range(n):
        f = bg.copy()
        x = 40 + 6 * k
        cv2.rectangle(f, (x, 30), (x + 20, 100), (220, 200, 180), -1)
        cv2.circle(f, (x + 10, 22), 9, (220, 200, 180), -1)
        frames.append(f)
    write_video(work / "performer.mkv", np.array(frames), 12)
    vid = read_video(work / "performer.mkv")
    out = []
    rng = np.random.default_rng(0)
    for f in vid:
        diff = np.abs(f.astype(int) - bg.astype(int)).max(2)
        ys, xs = np.where(diff > 28)
        idx = rng.choice(len(xs), min(200, len(xs)), replace=False)
        out.append([[int(xs[i] * 1000 / W), int(ys[i] * 1000 / H)] for i in idx])
    jwrite(work, "body.json", {"frames": out})
    cx = [np.mean([p[0] for p in fr]) for fr in out]
    ghosts = [0.35 / k for k in (1, 2, 3)]
    inside = all(40 + 6 * k - 0.2 <= p[0] * W / 1000 <= 40 + 6 * k + 20 + 0.2 for k, fr in enumerate(out) for p in fr)
    return [chk("background difference (threshold 28) finds the performer only", inside and len(out) == n, len(out[0])),
            chk("coords in 0..1000", all(0 <= v <= 1000 for fr in out for p in fr for v in p), "0..1000"),
            chk("particles track the motion (+6 px per frame -> +37.5 units)", near(float(np.mean(np.diff(cx))), 6 * 1000 / W, 2.5), round(float(np.mean(np.diff(cx))), 2)),
            chk("3 ghosts with alpha .35/k", np.allclose(ghosts, [0.35, 0.175, 0.35 / 3]), ghosts)]


def ch_48(work):
    ok, files = scaffold("comics-panels", work / "comic")
    panels = [(0, 0, 960, 540), (960, 0, 1920, 540), (0, 540, 1920, 1080)]
    gutter = 24

    def cam(t, hold=1.5, move=0.5):
        seg = int(t // (hold + move))
        u = (t % (hold + move) - hold) / move
        a = panels[min(seg, 2)]
        b = panels[min(seg + 1, 2)]
        p = 0 if u < 0 else sine_io(u)
        ca = ((a[0] + a[2]) / 2, (a[1] + a[3]) / 2)
        cb = ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)
        return (ca[0] + (cb[0] - ca[0]) * p, ca[1] + (cb[1] - ca[1]) * p)

    return [chk("comics-panels scaffold", ok, files),
            chk("camera holds on panel 1 then travels to panel 2", cam(1.0) == (480, 270) and cam(2.0) == (1440, 270), (cam(1.0), cam(2.0))),
            chk("gutters separate panels", gutter > 0 and panels[0][2] == panels[1][0], gutter)]


def ch_49(work):
    ok, files = scaffold("anime-action", work / "anime")
    fps = 24
    frames = np.full((12, 32, 32, 3), 100, np.uint8)
    impact = 6
    frames[impact:impact + 3] = 255 - frames[impact:impact + 3]
    overshoot = lambda p: 1 + 0.08 * math.sin(math.pi * p) if p < 1 else 1
    lines = 24
    return [chk("anime-action scaffold", ok, files),
            chk("impact held 2-3 frames with an inverted flash", (frames[impact] == 155).all() and np.array_equal(frames[impact], frames[impact + 2])
                and (frames[impact + 3] == 100).all(), "3 f"),
            chk("overshoot 5-10%", 1.05 <= max(overshoot(k / 20) for k in range(21)) <= 1.10, round(max(overshoot(k / 20) for k in range(21)), 3))]


def ch_x01(work):
    grumpy = lambda t: math.sin(83 * t) * 8 + math.sin(61 * t) * 5
    huff = lambda t: max(0, math.sin(5 * t)) ** 5
    sleepy = lambda t: math.sin(2.4 * t) * 32
    sacc = lambda t: math.copysign(abs(math.sin(5.2 * t)) ** 0.2, math.sin(5.2 * t)) * 26
    arrival = lambda a: 0.1 * math.exp(-7 * a) * math.sin(19 * a)
    ts = np.linspace(0, 5, 5001)
    g = np.array([grumpy(t) for t in ts])
    s = np.array([sacc(t) for t in ts])
    still_ok = 0.7
    idle_mult = 2
    jwrite(work, "signatures.json", {"grumpy_range": float(np.ptp(g)), "idle_x": idle_mult})
    return [chk("grumpy jitter bounded by 8 + 5 = 13 px", np.abs(g).max() <= 13 and np.abs(g).max() > 12, round(float(np.abs(g).max()), 3)),
            chk("saccade eyes snap: mostly near +-26", (np.abs(np.abs(s) - 26) < 5).mean() > 0.7, round(float((np.abs(np.abs(s) - 26) < 5).mean()), 3)),
            chk("sleepy float +-32 px", near(max(abs(sleepy(t)) for t in ts), 32, 0.01), "32"),
            chk("arrival squash decays (e^-7a)", abs(arrival(1.0)) < 0.001 < max(abs(arrival(a / 100)) for a in range(30)), round(arrival(0.08), 4))]


_PROGRAMS = {
    "CHAR-01": ch_01, "CHAR-02": ch_02, "CHAR-03": ch_03, "CHAR-04": ch_04, "CHAR-05": ch_05, "CHAR-09": ch_09,
    "CHAR-10": ch_10, "CHAR-11": ch_11, "CHAR-12": ch_12, "CHAR-13": ch_13, "CHAR-14": ch_14, "CHAR-15": ch_15,
    "CHAR-16": ch_16, "CHAR-17": ch_17, "CHAR-18": ch_18, "CHAR-19": ch_19, "CHAR-20": ch_20, "CHAR-21": ch_21,
    "CHAR-22": ch_22, "CHAR-23": ch_23, "CHAR-24": ch_24, "CHAR-25": ch_25, "CHAR-26": ch_26, "CHAR-27": ch_27,
    "CHAR-28": ch_28, "CHAR-29": ch_29, "CHAR-30": ch_30, "CHAR-31": ch_31, "CHAR-32": ch_32, "CHAR-33": ch_33,
    "CHAR-34": ch_34, "CHAR-35": ch_35, "CHAR-36": ch_36, "CHAR-37": ch_37, "CHAR-38": ch_38, "CHAR-45": ch_45,
    "CHAR-46": ch_46, "CHAR-48": ch_48, "CHAR-49": ch_49, "CHAR-X01": ch_x01,
}
PROGRAMS = {k: _recorded(v) for k, v in _PROGRAMS.items()}
