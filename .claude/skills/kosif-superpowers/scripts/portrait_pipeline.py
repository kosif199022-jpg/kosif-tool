#!/usr/bin/env python3
"""KOSIF Portrait Pipeline: a photo reference becomes a graphite portrait built only from pencil strokes.

The photo is used the way an atelier student uses a sitter: it is measured, never copied. The canvas
starts as blank paper and every mark on it is a generated stroke, so the output contains no photo
pixels (the receipt proves it: `canvas_source = strokes_only`). Stages follow the portrait method
cards PM-01..PM-16 in data/portrait_methods.json:

  measure     face landmarks (MediaPipe, optional) and a body/hair/skin/clothes segmentation give the
              proportional checks a sight-size or Loomis student would make (thirds, eye spacing).
  construct   faint Loomis guides (cranium ball, centre line, brow/nose/chin lines) and a straight-line
              envelope, laid in lightly as the first layer, the way an atelier block-in starts.
  value plan  the reference is reduced to a value map; background is held lighter (focal hierarchy).
  render      four tonal passes of tapered strokes (lay-in, cross-hatch, deep shadow, accents) that
              follow the form's direction field and stop at edges; spacing and length shrink on skin.
  blend       a stump pass softens skin hatching, then fine hatching and accents go back on top.
  edges       lost-and-found contour lines weighted by local contrast and by region (face first).
  lift        a kneaded-eraser pass lifts highlights and catchlights where the value map is light.
  paper       warm paper with tooth; graphite catches the tooth more at light pressure.

Requires numpy + opencv-python-headless (mediapipe and its two model files are optional: without them
a Haar face box and tone-only regions are used). Deterministic for a given --seed. Not a human hand,
not a neural style transfer, not proof of professional quality: it is algorithmic rendering from a
measured construction, and the review command reports what was measured.

  python3 scripts/portrait_pipeline.py draw --photo in.png --out out/portrait [--models DIR] [--scale 1.5]
  python3 scripts/portrait_pipeline.py review --dir out/portrait     # rule-27 gate + value/edge metrics
  python3 scripts/portrait_pipeline.py cards [--id PM-03]            # the method cards
"""
import argparse
import hashlib
import json
import math
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "data" / "portrait_methods.json"
SCHEMA = "kosif.portrait.receipt.v1"

# MediaPipe face-mesh indices used for measurements (canonical 468-point topology).
LM = {"forehead": 10, "chin": 152, "glabella": 9, "nose_tip": 1, "nose_base": 2, "brow_l": 105,
      "brow_r": 334, "eye_l_out": 33, "eye_l_in": 133, "eye_r_in": 362, "eye_r_out": 263,
      "mouth_l": 61, "mouth_r": 291, "lip_top": 13, "lip_bot": 14, "cheek_l": 234, "cheek_r": 454}
FACE_OVAL = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377,
             152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]
EYE_L = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
EYE_R = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
LIPS = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 409, 270, 269, 267, 0, 37, 39, 40, 185]
BROW_L = [70, 63, 105, 66, 107, 55, 65, 52, 53, 46]
BROW_R = [300, 293, 334, 296, 336, 285, 295, 282, 283, 276]
NOSE = [168, 6, 197, 195, 5, 4, 1, 19, 94, 2, 98, 327, 64, 294, 48, 278]

REGIONS = ("background", "hair", "body_skin", "face_skin", "clothes", "other")

# Tonal passes (Speed's mass drawing then Hampton-style build-up): cap = darkest value this pass may
# reach, off = hatch angle added to the form direction, sp = line spacing px, ln = stroke length px,
# w = width px, a = graphite opacity at full pressure, tol = how far tone may drift before a stroke stops.
PASSES = [
    {"name": "lay-in", "cap": 0.30, "off": 0.0, "sp": 2.6, "ln": (22, 70), "w": 1.15, "a": 0.42, "tol": 0.20},
    {"name": "cross-hatch", "cap": 0.55, "off": 58.0, "sp": 2.4, "ln": (18, 60), "w": 1.10, "a": 0.48, "tol": 0.16},
    {"name": "deep-shadow", "cap": 0.78, "off": -38.0, "sp": 2.2, "ln": (14, 48), "w": 1.05, "a": 0.55, "tol": 0.13},
    {"name": "accents", "cap": 0.97, "off": 90.0, "sp": 1.9, "ln": (8, 30), "w": 1.00, "a": 0.62, "tol": 0.10},
]
# Region scaling: length, spacing, width multipliers, default hatch angle (deg), value weight, edge weight.
REGION_STYLE = {
    "background": {"ln": 1.35, "sp": 1.30, "w": 1.05, "ang": 0.0, "val": 0.50, "edge": 0.22, "coh": 0.9,
                   "straight": True, "tol": 1.5, "off": 0.0, "floor": 0.05},
    "hair": {"ln": 0.65, "sp": 0.80, "w": 0.95, "ang": 60.0, "val": 1.00, "edge": 0.55, "coh": 1.0},
    "body_skin": {"ln": 0.55, "sp": 0.80, "w": 0.90, "ang": 50.0, "val": 1.00, "edge": 0.85, "coh": 0.45,
                  "off": 0.3, "amul": 0.8},
    "face_skin": {"ln": 0.60, "sp": 0.72, "w": 0.78, "ang": 50.0, "val": 1.00, "edge": 1.00, "coh": 0.22,
                  "off": 0.3, "amul": 0.8},   # skin: near-parallel layers, lighter touch, no scratchy cross-strokes
    "clothes": {"ln": 1.00, "sp": 1.00, "w": 1.05, "ang": 62.0, "val": 1.00, "edge": 0.50, "coh": 0.55,
                "tol": 1.6},
    "other": {"ln": 0.80, "sp": 0.90, "w": 1.00, "ang": 45.0, "val": 0.90, "edge": 0.60, "coh": 0.8},
}


# Drawing media: paper and pigment colours, stroke width/opacity multipliers, how much the stump blends
# (and where), how far the pigment spreads, and how strongly the paper tooth breaks the stroke.
MEDIUMS = {
    "graphite": {"paper": (244, 238, 226), "ink": (38, 38, 44), "w": 1.0, "a": 1.0, "blend": "skin", "spread": 0.45,
                 "tooth": 1.0, "sheen": 6.0},
    "charcoal": {"paper": (238, 232, 220), "ink": (22, 20, 20), "w": 1.7, "a": 1.15, "blend": "all", "spread": 0.8,
                 "tooth": 1.3, "sheen": 0.0},
    "ink": {"paper": (248, 246, 240), "ink": (14, 14, 18), "w": 0.75, "a": 1.7, "blend": "none", "spread": 0.25,
            "tooth": 0.3, "sheen": 0.0},
    "sepia": {"paper": (243, 233, 212), "ink": (92, 54, 32), "w": 1.0, "a": 1.0, "blend": "skin", "spread": 0.5,
              "tooth": 1.0, "sheen": 0.0},
}
MED = dict(MEDIUMS["graphite"])


def _need():
    try:
        import numpy  # noqa: F401
        import cv2  # noqa: F401
    except ImportError:
        sys.exit("portrait_pipeline needs: pip install numpy opencv-python-headless  (optional: mediapipe)")


# ------------------------------------------------------------------ reference and measurement

def load_reference(path, crop=None):
    """Read the photo; trim phone-screenshot bars (near-black rows) unless an explicit crop is given."""
    import cv2
    import numpy as np
    img = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if img is None:
        raise SystemExit(f"cannot read {path}")
    if crop:
        x0, y0, x1, y1 = crop
        return img[y0:y1, x0:x1], [x0, y0, x1, y1]
    rows = img.mean(axis=(1, 2)) > 35
    best, start, run = (0, img.shape[0]), None, 0
    longest = 0
    for y, ok in enumerate(list(rows) + [False]):
        if ok and start is None:
            start = y
        elif not ok and start is not None:
            if y - start > longest:
                longest, best = y - start, (start, y)
            start = None
    y0, y1 = best
    if longest < img.shape[0] * 0.4:
        y0, y1 = 0, img.shape[0]
    return img[y0:y1], [0, int(y0), int(img.shape[1]), int(y1)]


def measure(img, models=None):
    """Landmarks + region labels. Returns dict with arrays; falls back gracefully without MediaPipe."""
    import cv2
    import numpy as np
    h, w = img.shape[:2]
    out = {"landmarks": None, "labels": None, "engine": []}
    models = Path(models) if models else None
    try:
        import mediapipe as mp
        from mediapipe.tasks import python as mpt
        from mediapipe.tasks.python import vision
        rgb = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        if models and (models / "face_landmarker.task").exists():
            opt = vision.FaceLandmarkerOptions(base_options=mpt.BaseOptions(
                model_asset_path=str(models / "face_landmarker.task")), num_faces=1)
            with vision.FaceLandmarker.create_from_options(opt) as det:
                res = det.detect(rgb)
            if res.face_landmarks:
                out["landmarks"] = np.array([[p.x * w, p.y * h] for p in res.face_landmarks[0]], np.float32)
                out["engine"].append("mediapipe.face_landmarker")
        if models and (models / "selfie_multiclass.tflite").exists():
            opt = vision.ImageSegmenterOptions(base_options=mpt.BaseOptions(
                model_asset_path=str(models / "selfie_multiclass.tflite")), output_category_mask=True)
            with vision.ImageSegmenter.create_from_options(opt) as seg:
                res = seg.segment(rgb)
            out["labels"] = res.category_mask.numpy_view().copy().astype(np.uint8).reshape(h, w)
            out["engine"].append("mediapipe.selfie_multiclass")
    except Exception as exc:  # optional dependency
        out["engine"].append(f"mediapipe unavailable: {type(exc).__name__}: {exc}")
    if out["labels"] is None:
        out["labels"] = np.zeros((h, w), np.uint8)
        casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = [] if casc.empty() else casc.detectMultiScale(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 1.1, 5, minSize=(w // 10, w // 10))
        for (x, y, fw, fh) in faces[:1]:
            cv2.ellipse(out["labels"], (x + fw // 2, y + fh // 2), (fw // 2, int(fh * 0.62)), 0, 0, 360, 3, -1)
            out["engine"].append("opencv.haar_face")
    return out


def scene_regions(img, labels, k=7):
    """Any subject without a person: GrabCut separates subject from surroundings (style), and a colour
    clustering gives the shape boundaries strokes must not cross (the 'big shapes' of a block-in)."""
    import cv2
    import numpy as np
    h, w = img.shape[:2]
    mask = np.zeros((h, w), np.uint8)
    m = max(4, int(min(h, w) * 0.05))
    try:
        bgd, fgd = np.zeros((1, 65), np.float64), np.zeros((1, 65), np.float64)
        small = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        sm = np.zeros(small.shape[:2], np.uint8)
        cv2.grabCut(small, sm, (m // 2, m // 2, small.shape[1] - m, small.shape[0] - m), bgd, fgd, 4,
                    cv2.GC_INIT_WITH_RECT)
        fg = cv2.resize(np.isin(sm, (1, 3)).astype(np.uint8), (w, h), interpolation=cv2.INTER_NEAREST)
    except cv2.error:
        fg = np.zeros((h, w), np.uint8)
    style = np.where(fg > 0, 5, 0).astype(np.uint8)
    lab = cv2.cvtColor(cv2.bilateralFilter(img, 9, 40, 7), cv2.COLOR_BGR2LAB).astype(np.float32)
    lab[..., 0] *= 0.5
    data = cv2.resize(lab, None, fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA).reshape(-1, 3)
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    _, _, centers = cv2.kmeans(data, k, None, crit, 2, cv2.KMEANS_PP_CENTERS)
    d = ((lab.reshape(-1, 1, 3) - centers.reshape(1, -1, 3)) ** 2).sum(-1)
    clusters = cv2.medianBlur(d.argmin(1).reshape(h, w).astype(np.uint8), 7)
    bounds = style.astype(np.int32) * 16 + clusters
    return style, bounds


def proportions(lm):
    """Loomis/atelier proportional checks measured on the landmarks (pixels and ratios)."""
    if lm is None:
        return {"available": False}
    import numpy as np
    P = {k: lm[i] for k, i in LM.items()}
    up = P["chin"] - P["forehead"]
    up = up / (np.linalg.norm(up) + 1e-6)

    def along(a, b):
        return float(np.dot(P[b] - P[a], up))
    brow_y = (P["brow_l"] + P["brow_r"]) / 2
    upper = float(np.dot(brow_y - P["forehead"], up))
    middle = float(np.dot(P["nose_base"] - brow_y, up))
    lower = along("nose_base", "chin")
    eye_w = (np.linalg.norm(P["eye_l_out"] - P["eye_l_in"]) + np.linalg.norm(P["eye_r_out"] - P["eye_r_in"])) / 2
    gap = float(np.linalg.norm(P["eye_r_in"] - P["eye_l_in"]))
    face_w = float(np.linalg.norm(P["cheek_r"] - P["cheek_l"]))
    mouth_w = float(np.linalg.norm(P["mouth_r"] - P["mouth_l"]))
    roll = math.degrees(math.atan2(*(P["eye_r_out"] - P["eye_l_out"])[::-1]))
    return {"available": True,
            "thirds_px": [round(upper, 1), round(middle, 1), round(lower, 1)],
            "thirds_ratio": [round(v / (middle + 1e-6), 3) for v in (upper, middle, lower)],
            "eye_width_px": round(float(eye_w), 1), "eye_gap_over_eye_width": round(float(gap / eye_w), 3),
            "face_width_in_eyes": round(float(face_w / eye_w), 2), "mouth_over_eye_gap": round(mouth_w / gap, 3),
            "head_roll_deg": round(roll, 2),
            "note": "Landmark forehead point sits below the hairline, so the upper third reads short; "
                    "the canonical 1:1:1 is a teaching average, the drawing follows the sitter's measured ratios."}


# ------------------------------------------------------------------ value map and direction field

def value_map(img, labels):
    """Target darkness 0..1 per pixel, with the background held lighter for focal hierarchy."""
    import cv2
    import numpy as np
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    L = lab[..., 0].astype(np.float32) / 255.0
    L = cv2.bilateralFilter(L, 0, 0.06, 3.0)
    clahe = cv2.createCLAHE(clipLimit=1.6, tileGridSize=(8, 8))
    Lc = clahe.apply((L * 255).astype(np.uint8)).astype(np.float32) / 255.0
    skin = np.isin(labels, (2, 3)).astype(np.float32)
    skin = cv2.GaussianBlur(skin, (0, 0), 6)
    L = L * (1 - 0.5 * skin) + Lc * 0.5 * skin           # a little more form contrast on skin
    D = np.clip(1.0 - L, 0, 1) ** 1.12
    D = D * (1 - skin) + (D ** 1.35) * skin              # key the light family of the flesh lighter (Speed, Loomis)
    val = np.ones_like(D)
    for k, name in enumerate(REGIONS):
        val[labels == k] = REGION_STYLE[name]["val"]
    val = cv2.GaussianBlur(val, (0, 0), 4)
    D = D * val
    floor = np.zeros_like(D)
    for k, name in enumerate(REGIONS):
        floor[labels == k] = REGION_STYLE[name].get("floor", 0.0)
    D = np.where(D < floor, D * 0.25, D)                  # lights below the floor stay paper (leave the whites)
    return np.clip(D, 0, 1), L


def direction_field(L, labels, flat_default=False):
    """Hatch orientation: along the isophotes where the form is coherent, a region default elsewhere."""
    import cv2
    import numpy as np
    g = cv2.GaussianBlur(L, (0, 0), 2.0)
    gx = cv2.Sobel(g, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(g, cv2.CV_32F, 0, 1, ksize=3)
    J11 = cv2.GaussianBlur(gx * gx, (0, 0), 9)
    J22 = cv2.GaussianBlur(gy * gy, (0, 0), 9)
    J12 = cv2.GaussianBlur(gx * gy, (0, 0), 9)
    tg = 0.5 * np.arctan2(2 * J12, J11 - J22)
    iso = tg + np.pi / 2
    tr = J11 + J22
    det = np.sqrt((J11 - J22) ** 2 + 4 * J12 ** 2)
    coh = np.where(tr > 1e-8, det / (tr + 1e-8), 0) ** 2
    deflt = np.zeros_like(L)
    cw = np.zeros_like(L)
    for k, name in enumerate(REGIONS):
        m = labels == k
        deflt[m] = math.radians(-REGION_STYLE[name]["ang"])   # image y points down: negative = up-right
        cw[m] = REGION_STYLE[name]["coh"]
    c = np.clip(coh * 1.6, 0, 1) * cw
    if flat_default:     # scenes: flat areas (a clear sky, a smooth wall) take the default angle instead of noise
        c *= np.clip(tr / (np.percentile(tr, 60) + 1e-9), 0, 1)
    vx = c * np.cos(2 * iso) + (1 - c) * np.cos(2 * deflt)
    vy = c * np.sin(2 * iso) + (1 - c) * np.sin(2 * deflt)
    sk = np.isin(labels, (2, 3))
    for sig, m in ((5, ~sk), (11, sk)):                 # skin: broad, calm planes; elsewhere: follow detail
        bx, by = cv2.GaussianBlur(vx, (0, 0), sig), cv2.GaussianBlur(vy, (0, 0), sig)
        vx, vy = np.where(m, bx, vx), np.where(m, by, vy)
    return 0.5 * np.arctan2(vy, vx).astype(np.float32)


# ------------------------------------------------------------------ paper and strokes

def paper_tooth(h, w, rng):
    import cv2
    import numpy as np
    t = np.zeros((h, w), np.float32)
    for s, amp in ((0.7, 0.60), (1.5, 0.30), (4.0, 0.06)):   # fine grain: coarse noise reads as mottled skin
        n = rng.standard_normal((h, w)).astype(np.float32)
        t += amp * cv2.GaussianBlur(n, (0, 0), s)
    fib = cv2.GaussianBlur(rng.standard_normal((h, w)).astype(np.float32), (0, 0), sigmaX=6, sigmaY=0.8)
    t += 0.10 * fib
    t = (t - t.min()) / (t.max() - t.min() + 1e-6)
    return t


class Canvas:
    def __init__(self, h, w, tooth, rng, ss=3):
        import numpy as np
        self.h, self.w, self.ss, self.rng = h, w, ss, rng
        self.ink = np.zeros((h, w), np.float32)     # graphite density actually on the paper
        self.cov = np.zeros((h, w), np.float32)     # local mean darkness the strokes account for
        self.tooth = tooth
        self.strokes = []

    def stroke(self, pts, width, alpha, spacing, layer, taper="both", record=True):
        """Render one tapered pencil stroke (supersampled), deposit graphite through the paper tooth."""
        import cv2
        import numpy as np
        pts = np.asarray(pts, np.float32)
        if len(pts) < 2:
            return
        width, alpha = width * MED["w"], min(alpha * MED["a"], 0.95)
        pad = int(math.ceil(max(width, spacing))) + 2
        x0 = max(int(pts[:, 0].min()) - pad, 0)
        y0 = max(int(pts[:, 1].min()) - pad, 0)
        x1 = min(int(pts[:, 0].max()) + pad + 1, self.w)
        y1 = min(int(pts[:, 1].max()) + pad + 1, self.h)
        if x1 - x0 < 2 or y1 - y0 < 2:
            return
        ss = self.ss
        n = len(pts)
        t = np.linspace(0, 1, n)
        if taper == "both":
            p = np.sin(np.pi * np.clip(t * 0.94 + 0.03, 0, 1)) ** 0.55
        elif taper == "flick":
            p = (1 - t) ** 0.7 * np.clip(t * 6, 0, 1) ** 0.5
        else:
            p = np.ones(n)
        p = np.clip(p * (0.85 + 0.15 * self.rng.random()), 0.05, 1)
        hi = np.zeros(((y1 - y0) * ss, (x1 - x0) * ss), np.uint8)
        q = ((pts - [x0, y0]) * ss * 16).astype(np.int32)
        for i in range(n - 1):
            th = max(1, int(round(width * ss * (0.55 + 0.45 * p[i]))))
            cv2.line(hi, tuple(q[i]), tuple(q[i + 1]), int(255 * p[i]), th, cv2.LINE_AA, shift=4)
        m = cv2.resize(hi, (x1 - x0, y1 - y0), interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0
        tooth = self.tooth[y0:y1, x0:x1]
        k = 0.55 * min(MED["tooth"], 1.0)
        dep = alpha * m * ((1 - k) + k * tooth ** ((1.4 - 0.8 * alpha) * max(MED["tooth"], 1.0)))
        roi = self.ink[y0:y1, x0:x1]
        roi[:] = 1 - (1 - roi) * (1 - dep)
        if spacing:
            lo = np.zeros((y1 - y0, x1 - x0), np.uint8)
            ql = ((pts - [x0, y0]) * 16).astype(np.int32)
            cv2.polylines(lo, [ql], False, 255, max(1, int(round(spacing))), cv2.LINE_AA, shift=4)
            v = min(0.42 * alpha * width / spacing, 0.95)   # 0.42: measured take-up (tooth x taper x pressure width)
            croi = self.cov[y0:y1, x0:x1]
            croi[:] = 1 - (1 - croi) * (1 - v * lo.astype(np.float32) / 255.0)
        if record:
            self.strokes.append((layer, round(width, 2), round(alpha, 3), pts[:: max(1, n // 12)].round(1).tolist()
                                 + [pts[-1].round(1).tolist()]))


def trace(x0, y0, field, off, length, step, labels, tone, tol, cap, cov, rng, hw, straight=False):
    """Follow the direction field both ways from a seed; stop at region changes, tone edges, or filled paper.

    straight=True keeps the seed's angle (snapped to level or plumb when close): architecture is drawn with
    straight strokes, not by following the swirls of a flat wall. Each end overshoots one step, as a hand does,
    so neighbouring regions overlap instead of leaving a paper halo between them.
    """
    h, w = hw
    reg = labels[int(y0), int(x0)]
    t0 = tone[int(y0), int(x0)]
    wob = math.radians(rng.normal(0, 3.0))
    a0 = field[int(y0), int(x0)] + off
    if straight == "free":
        a0 += wob * 0.6
    elif straight:
        for snap in (0.0, math.pi / 2, math.pi, -math.pi / 2):
            if abs((a0 - snap + math.pi) % (2 * math.pi) - math.pi) < math.radians(22):
                a0 = snap
        a0 += wob * 0.4
    halves = []
    for sgn in (1, -1):
        x, y = x0, y0
        pts = []
        pdx = pdy = None
        travelled = 0.0
        while travelled < length / 2:
            a = a0 if straight else field[int(y), int(x)] + off + wob
            dx, dy = math.cos(a), math.sin(a)
            if pdx is not None and dx * pdx + dy * pdy < 0:
                dx, dy = -dx, -dy
            if pdx is None:
                dx, dy = dx * sgn, dy * sgn
            elif dx * pdx + dy * pdy < 0.86:      # sharper than ~30 degrees: lift the pencil
                break
            nx, ny = x + dx * step, y + dy * step
            if not (1 <= nx < w - 1 and 1 <= ny < h - 1):
                break
            ix, iy = int(ny), int(nx)
            if labels[ix, iy] != reg or abs(tone[ix, iy] - t0) > tol or cap[ix, iy] - cov[ix, iy] < -0.06:
                if pdx is not None:
                    pts.append((x + dx * step * 0.8, y + dy * step * 0.8))   # overshoot into the edge
                break
            x, y, pdx, pdy = nx, ny, dx, dy
            travelled += step
            pts.append((x, y))
        halves.append(pts)
    return halves[1][::-1] + [(x0, y0)] + halves[0]


def tonal_pass(cv, P, D, L, labels, field, scale, rng, stats, region_mask=None, cap_scale=1.0, bounds=None):
    import numpy as np
    bounds = labels if bounds is None else bounds
    h, w = D.shape
    cap = np.minimum(D, P["cap"] * cap_scale)
    sp_min = P["sp"] * scale * 0.72
    grid = max(1.0, sp_min * 0.9)
    ys, xs = np.mgrid[0:h:grid, 0:w:grid]
    xs = (xs + rng.random(xs.shape) * grid).ravel()
    ys = (ys + rng.random(ys.shape) * grid).ravel()
    keep = (xs < w - 1) & (ys < h - 1)
    xs, ys = xs[keep], ys[keep]
    off = math.radians(P["off"])
    soft = 0.78          # graphite: many light strokes rather than few inked ones
    count = 0
    for rnd in range(2):
        ix, iy = xs.astype(int), ys.astype(int)
        ok = (cap[iy, ix] - cv.cov[iy, ix]) >= 0.05
        if region_mask is not None:
            ok &= region_mask[iy, ix]
        xs, ys = xs[ok], ys[ok]
        order = rng.permutation(len(xs))
        for x, y in zip(xs[order].tolist(), ys[order].tolist()):
            ix, iy = int(x), int(y)
            r = float(cap[iy, ix] - cv.cov[iy, ix])
            if r < 0.05:
                continue
            st = REGION_STYLE[REGIONS[min(int(labels[iy, ix]), 5)]]
            lo, hi = P["ln"]
            ln = rng.uniform(lo, hi) * st["ln"] * scale
            sp = P["sp"] * st["sp"] * scale
            o = off * st.get("off", 1.0)
            pts = trace(x, y, field, o, ln, 1.6 * scale, bounds, L, P["tol"] * st.get("tol", 1.0), cap, cv.cov, rng,
                        (h, w), straight=st.get("straight", False))
            if len(pts) < 3:
                continue
            a = P["a"] * (0.8 + 0.4 * min(1.0, r / 0.3)) * rng.uniform(0.85, 1.1) * soft * st.get("amul", 1.0)
            cv.stroke(pts, P["w"] * st["w"] * scale * rng.uniform(0.9, 1.1), min(a, 0.9), sp, P["name"],
                      taper="flick" if rng.random() < 0.3 else "both")
            count += 1
    stats[P["name"]] = stats.get(P["name"], 0) + count
    print(f"  pass {P['name']}: {count} strokes", file=sys.stderr, flush=True)


# ------------------------------------------------------------------ construction, edges, blending, lifting

def construction(cv, lm, labels, scale, stats):
    """Loomis guides + envelope, very light: the block-in an atelier drawing starts from."""
    import cv2
    import numpy as np
    n0 = len(cv.strokes)
    lw, la = 0.9 * scale, 0.10
    if lm is not None:
        P = {k: lm[i] for k, i in LM.items()}
        top, chin = P["forehead"], P["chin"]
        axis = chin - top
        axis_u = axis / (np.linalg.norm(axis) + 1e-6)
        perp = np.array([-axis_u[1], axis_u[0]])
        face_w = np.linalg.norm(P["cheek_r"] - P["cheek_l"])
        # cranium ball: centre between brow line and forehead landmark, radius about half the face width
        brow = (P["brow_l"] + P["brow_r"]) / 2
        c = brow - axis_u * face_w * 0.10
        r = face_w * 0.56
        ang = np.linspace(0, 2 * np.pi, 90)
        circle = np.stack([c[0] + r * np.cos(ang), c[1] + r * np.sin(ang)], 1)
        for k in range(0, 90, 30):
            cv.stroke(circle[k:k + 32], lw, la, 0, "construction")
        cv.stroke([top - axis_u * face_w * 0.55, chin + axis_u * face_w * 0.05], lw, la, 0, "construction")
        for key, frac in (("brow", 0.62), ("nose_base", 0.55), ("chin", 0.42)):
            p = brow if key == "brow" else P[key]
            cv.stroke([p - perp * face_w * frac, p + perp * face_w * frac], lw, la * 0.9, 0, "construction")
        eye_y = (P["eye_l_out"] + P["eye_r_out"]) / 2
        cv.stroke([eye_y - perp * face_w * 0.5, eye_y + perp * face_w * 0.5], lw, la * 0.7, 0, "construction")
    person = (labels > 0).astype(np.uint8) * 255
    cnts, _ = cv2.findContours(person, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if cnts:
        big = max(cnts, key=cv2.contourArea)
        env = cv2.approxPolyDP(big, 0.012 * cv2.arcLength(big, True), True)[:, 0, :].astype(np.float32)
        for i in range(len(env)):
            a, b = env[i], env[(i + 1) % len(env)]
            ext = (b - a) * 0.06
            cv.stroke([a - ext, b + ext], lw, la * 0.8, 0, "construction", taper="none")
    stats["construction"] = len(cv.strokes) - n0


def contour_lines(cv, img, L, labels, scale, rng, stats):
    """Lost-and-found edges: line weight follows local contrast and region importance."""
    import cv2
    import numpy as np
    g = cv2.bilateralFilter((L * 255).astype(np.uint8), 0, 18, 3)
    e1 = cv2.Canny(g, 40, 95, L2gradient=True)
    gx = cv2.Sobel(L, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(L, cv2.CV_32F, 0, 1, ksize=3)
    mag = cv2.GaussianBlur(np.sqrt(gx * gx + gy * gy), (0, 0), 1.2)
    cnts, _ = cv2.findContours(e1, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    n0 = len(cv.strokes)
    for c in cnts:
        c = c[:, 0, :].astype(np.float32)
        if len(c) < 10:
            continue
        seg = max(8, int(28 * scale))
        for s in range(0, len(c), seg):
            piece = c[s:s + seg + 2]
            if len(piece) < 6:
                continue
            mid = piece[len(piece) // 2].astype(int)
            reg = REGIONS[min(labels[mid[1], mid[0]], 5)]
            st = REGION_STYLE[reg]
            strength = float(np.clip(mag[mid[1], mid[0]] * 2.2, 0, 1))
            a = 0.55 * st["edge"] * strength
            if a < 0.08 or rng.random() < 0.18 * (1 - st["edge"]):   # lose some edges on purpose
                continue
            k = max(1, len(piece) // 10)
            cv.stroke(piece[::k], (0.75 + 0.5 * strength) * scale * 0.9, a, 0, "edges")
    stats["edges"] = len(cv.strokes) - n0


def stump_blend(cv, labels, amount=0.55, sigma=1.6):
    """Blending stump on skin (charcoal: everywhere; ink: never), keeping the edges of features."""
    import cv2
    import numpy as np
    if MED["blend"] == "none":
        return
    skin = (np.ones(labels.shape, np.float32) * 0.8 if MED["blend"] == "all"
            else np.isin(labels, (2, 3)).astype(np.float32))
    skin = cv2.GaussianBlur(cv2.erode(skin, np.ones((3, 3), np.uint8)), (0, 0), 3) * amount
    soft = cv2.GaussianBlur(cv.ink, (0, 0), sigma)
    cv.ink[:] = cv.ink * (1 - skin) + soft * skin


def lift_highlights(cv, D, L, lm, labels, scale, rng):
    """Kneaded eraser: lift graphite where the value map is lighter than what is on the paper."""
    import cv2
    import numpy as np
    have = cv2.GaussianBlur(cv.ink, (0, 0), 2.0)
    over = np.clip(have - (D + 0.04), 0, 1)
    face = np.isin(labels, (1, 2, 3)).astype(np.float32)
    face = cv2.GaussianBlur(face, (0, 0), 4)
    lift = np.clip(over * 1.4 * face, 0, 0.85)
    cv.ink[:] = cv.ink * (1 - lift)
    if lm is not None:
        for eye in (EYE_L, EYE_R):
            poly = lm[eye].astype(np.int32)
            m = np.zeros(L.shape, np.uint8)
            cv2.fillPoly(m, [poly], 1)
            if m.sum() == 0:
                continue
            Lm = np.where(m > 0, L, 0)
            y, x = np.unravel_index(np.argmax(Lm), L.shape)
            r = max(1.2, 1.4 * scale)
            spot = np.zeros(L.shape, np.float32)
            cv2.circle(spot, (int(x), int(y)), int(math.ceil(r)), 1.0, -1, cv2.LINE_AA)
            spot = cv2.GaussianBlur(spot, (0, 0), 0.6)
            cv.ink[:] = cv.ink * (1 - 0.8 * spot)


def feature_accents(cv, lm, L, labels, scale, rng, stats):
    """Darkest accents a portraitist puts in last: lash line, iris, pupil, nostrils, the line between the lips."""
    import cv2
    import numpy as np
    if lm is None:
        return
    n0 = len(cv.strokes)
    for eye in (EYE_L, EYE_R):
        upper = lm[eye[8:]][::-1]   # inner corner over the top to the outer corner
        upper = np.vstack([lm[eye[8]], lm[eye[9:]], lm[eye[0]]])
        cv.stroke(upper, 1.5 * scale, 0.55, 0, "accents", taper="both")
        cv.stroke(upper + [0, 0.6 * scale], 1.1 * scale, 0.35, 0, "accents", taper="both")
        lower = lm[eye[:9]]
        cv.stroke(lower, 0.8 * scale, 0.18, 0, "accents", taper="both")
    m = lm[LIPS]
    mid = np.vstack([lm[61], lm[78], lm[95], lm[88], lm[178], lm[87], lm[14], lm[317], lm[402], lm[318],
                     lm[324], lm[308], lm[291]])
    cv.stroke(mid, 1.3 * scale, 0.45, 0, "accents", taper="both")
    for nost in ((98, 64, 48), (327, 294, 278)):
        cv.stroke(lm[list(nost)], 1.2 * scale, 0.30, 0, "accents", taper="both")
    stats["feature_accents"] = len(cv.strokes) - n0
    _ = m


# ------------------------------------------------------------------ outputs

def compose(cv, paper_rgb=None, graphite_rgb=None):
    import cv2
    import numpy as np
    paper_rgb, graphite_rgb = paper_rgb or MED["paper"], graphite_rgb or MED["ink"]
    ink = cv2.GaussianBlur(np.clip(cv.ink, 0, 1), (0, 0), MED["spread"])[..., None]   # pigment spreads into the fibre
    paper = np.array(paper_rgb, np.float32)
    shade = (0.965 + 0.035 * cv.tooth)[..., None]
    base = paper * shade
    gr = np.array(graphite_rgb, np.float32)
    out = base * (1 - ink) + gr * ink
    sheen = (ink > 0.75) * MED["sheen"]
    return np.clip(out + sheen, 0, 255).astype(np.uint8)


def write_svg(path, cv, size, figure_parts, title):
    """Editable layered SVG: one <g> per stage, every stroke a path. figure parts carry rule-27 data."""
    w, h = size
    paper = "#%02x%02x%02x" % MED["paper"]
    ink = "#%02x%02x%02x" % MED["ink"]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
           f"<title>{title}</title>", f'<rect width="{w}" height="{h}" fill="{paper}"/>']
    layers = {}
    for layer, width, alpha, pts in cv.strokes:
        layers.setdefault(layer, []).append((width, alpha, pts))
    for layer in ("construction", "lay-in", "cross-hatch", "deep-shadow", "accents", "edges"):
        if layer not in layers:
            continue
        out.append(f'<g id="{layer}" data-stage="{layer}" fill="none" stroke="{ink}" stroke-linecap="round">')
        bins = {}
        for width, alpha, pts in layers[layer]:      # one path per (width, opacity) bin keeps the file small
            k = max(1, len(pts) // 5)
            pts = pts[::k] + ([pts[-1]] if (len(pts) - 1) % k else [])
            d = "M" + "L".join(f"{round(x)} {round(y)}" for x, y in pts)
            bins.setdefault((round(width * 4) / 4, round(alpha * 20) / 20), []).append(d)
        for (width, alpha), ds in sorted(bins.items()):
            out.append(f'<path stroke-width="{width:g}" stroke-opacity="{alpha:g}" d="{"".join(ds)}"/>')
        out.append("</g>")
    if figure_parts:
        out.append('<g id="figure-gate" data-figure="sitter" fill="none" stroke="none" opacity="0">')
        for name, poly, contact in figure_parts:
            d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in poly) + " Z"
            c = f' data-contact="{contact}"' if contact else ""
            out.append(f'<path id="{name}" data-part="{name}"{c} d="{d}" fill="#000"/>')
        out.append("</g>")
    out.append("</svg>")
    Path(path).write_text("\n".join(out), encoding="utf-8")


def figure_parts(labels, lm):
    """Body pieces from the segmentation, for the rule-27 connectivity and contact check."""
    import cv2
    import numpy as np
    parts = []

    def poly(mask, name, contact=None, eps=0.004):
        cnts, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not cnts:
            return
        big = max(cnts, key=cv2.contourArea)
        ap = cv2.approxPolyDP(big, eps * cv2.arcLength(big, True), True)[:, 0, :]
        parts.append((name, ap.tolist(), contact))
    head = np.isin(labels, (1, 3))
    poly(head, "head")
    clothes = labels == 4
    poly(clothes, "torso", "neck")
    skin = labels == 2
    n, comp, st, _ = cv2.connectedComponentsWithStats(skin.astype(np.uint8))
    blobs = sorted(range(1, n), key=lambda i: -st[i, cv2.CC_STAT_AREA])[:3]
    for i in blobs:
        cx = st[i, cv2.CC_STAT_LEFT] + st[i, cv2.CC_STAT_WIDTH] / 2
        cy = st[i, cv2.CC_STAT_TOP] + st[i, cv2.CC_STAT_HEIGHT] / 2
        if lm is not None and cx < lm[234][0]:
            poly(comp == i, "saluting_hand", "head")       # fingertips rest at the brow
        else:
            poly(comp == i, "neck", "torso")
    return parts


def has_person(labels):
    return float((labels > 0).mean()) > 0.02


def draw(args, ref=None, source=None):
    """Draw a photo, or any reference image (an imagined scene rendered by code), from strokes only."""
    _need()
    import cv2
    import numpy as np
    global MED
    t0 = time.time()
    MED = dict(MEDIUMS[getattr(args, "medium", "graphite")])
    rng = np.random.default_rng(args.seed)
    crop = [int(v) for v in args.crop.split(",")] if getattr(args, "crop", None) else None
    if ref is None:
        ref, box = load_reference(args.photo, crop)
    else:
        box = [0, 0, ref.shape[1], ref.shape[0]]
    if args.scale != 1.0:
        ref = cv2.resize(ref, None, fx=args.scale, fy=args.scale, interpolation=cv2.INTER_CUBIC)
    h, w = ref.shape[:2]
    meas = measure(ref, args.models)
    labels, lm = meas["labels"], meas["landmarks"]
    subject = getattr(args, "subject", "auto")
    person = subject == "portrait" or (subject == "auto" and has_person(labels))
    saved = {k: dict(v) for k, v in REGION_STYLE.items()}
    bounds = None
    if not person:
        labels, bounds = scene_regions(ref, labels)
        lm = None
        # a scene is all subject: keep its full value range; strokes follow the form unless told otherwise
        # hatching in short straight strokes at the form's angle reads as a hand; long flowing curves read as a filter
        REGION_STYLE["background"].update(val=0.92, floor=0.0, straight="free", off=1.0, ang=25.0, coh=0.85, ln=0.8)
        REGION_STYLE["other"].update(val=1.0, coh=0.85, straight="free", ln=0.7)
    if getattr(args, "background", "auto") in ("straight", "flow"):
        REGION_STYLE["background"]["straight"] = args.background == "straight"
    try:
        D, L = value_map(ref, labels)
        if not person:   # a designed maquette is often low in contrast: spread it over the full pencil range
            lo, hi = np.percentile(D, [1, 99.5])
            D = (np.clip((D - lo) / max(hi - lo, 1e-3), 0, 1) ** 1.25) * 0.95   # key the lights up, keep the darks
        field = direction_field(L, labels, flat_default=not person)
        cv = Canvas(h, w, paper_tooth(h, w, rng), rng)
        stats = {}
        sc = args.scale
        construction(cv, lm, labels, sc, stats)
        for P in PASSES[:2]:
            tonal_pass(cv, P, D, L, labels, field, sc, rng, stats, bounds=bounds)
        stump_blend(cv, labels, amount=args.blend, sigma=2.2)
        skin = np.isin(labels, (2, 3))
        if skin.any():
            fine = dict(PASSES[1], name="lay-in", sp=1.8, ln=(10, 30), a=0.30, w=0.9, cap=0.5)
            cv.cov[skin] *= 0.6                          # blending lightened the record: let fine hatching rebuild
            tonal_pass(cv, fine, D, L, labels, field, sc, rng, stats, region_mask=skin, bounds=bounds)
        for P in PASSES[2:]:
            tonal_pass(cv, P, D, L, labels, field, sc, rng, stats, bounds=bounds)
        stump_blend(cv, labels, amount=args.blend * 0.5, sigma=1.1)   # second, lighter stump pass knocks back specks
        contour_lines(cv, ref, L, labels, sc, rng, stats)
        feature_accents(cv, lm, L, labels, sc, rng, stats)
        lift_highlights(cv, D, L, lm, labels, sc, rng)
    finally:
        REGION_STYLE.clear()
        REGION_STYLE.update(saved)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    rgb = compose(cv)
    name = args.name
    cv2.imwrite(str(out / f"{name}.png"), cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
    parts = figure_parts(labels, lm) if person else []
    write_svg(out / f"{name}.svg", cv, (w, h), parts, f"{name}: {getattr(args, 'medium', 'graphite')} drawing from strokes")
    # measurement artefacts for review (never shipped as the drawing)
    np.save(out / "_target_darkness.npy", D.astype(np.float16))
    np.save(out / "_labels.npy", labels)
    src_path = Path(source or args.photo)
    rec = {"schema": SCHEMA, "source": str(src_path.name), "source_kind": "imagined" if source else "photo",
           "source_sha256": hashlib.sha256(src_path.read_bytes()).hexdigest(),
           "subject": "portrait" if person else "scene", "medium": getattr(args, "medium", "graphite"),
           "crop_box": box, "scale": sc, "size": [w, h], "seed": args.seed, "engines": meas["engine"],
           "canvas_source": "strokes_only", "photo_pixels_in_output": False,
           "strokes": len(cv.strokes), "strokes_by_stage": stats, "proportions": proportions(lm),
           "methods": (["PM-01", "PM-02", "PM-03", "PM-04", "PM-05", "PM-06", "PM-07", "PM-08", "PM-09", "PM-10",
                        "PM-11", "PM-12", "PM-13", "PM-14"] if person else
                       ["PM-03", "PM-04", "PM-05", "PM-07", "PM-08", "PM-10", "PM-12", "PM-14", "PM-17", "PM-18"]),
           "seconds": round(time.time() - t0, 1), "png": str(out / f"{name}.png"), "svg": str(out / f"{name}.svg"),
           "honesty": "Algorithmic rendering from measured construction and a value map; not a human hand."}
    (out / "receipt.json").write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: rec[k] for k in ("subject", "medium", "strokes", "seconds", "png", "svg")}, ensure_ascii=False))


def rasterize_svg(svg, png, width=None, height=None):
    """Render a Claude-authored SVG scene to PNG with headless Chromium (or rsvg-convert when present)."""
    import re
    import shutil
    import subprocess
    import tempfile
    text = Path(svg).read_text(encoding="utf-8")
    m = re.search(r'viewBox="\s*[-\d.]+[\s,]+[-\d.]+[\s,]+([\d.]+)[\s,]+([\d.]+)', text)
    w = int(width or (float(m.group(1)) if m else 1200))
    h = int(height or (float(m.group(2)) if m else 1600))
    if shutil.which("rsvg-convert"):
        subprocess.run(["rsvg-convert", "-w", str(w), "-h", str(h), "-o", str(png), str(svg)], check=True)
        return
    candidates = [shutil.which(n) for n in ("chromium", "chromium-browser", "google-chrome")]
    candidates += [str(p) for p in Path("/opt/pw-browsers").glob("chromium-*/chrome-linux/chrome")]
    exe = next((c for c in candidates if c and Path(c).exists()), None)
    if not exe:
        raise SystemExit("no SVG rasterizer: install rsvg-convert (librsvg2-bin) or Chromium, or pass --png")
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "scene.html"
        page.write_text(f'<html><body style="margin:0;background:#fff">'
                        f'<img src="file://{Path(svg).resolve()}" width="{w}" height="{h}"></body></html>')
        subprocess.run([exe, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                        "--allow-file-access-from-files", f"--window-size={w},{h + 240}",
                        f"--screenshot={Path(png).resolve()}", f"file://{page}"],
                       check=True, capture_output=True, timeout=120)
    import cv2
    shot = cv2.imread(str(png), cv2.IMREAD_COLOR)        # the window is taller than the scene: crop it exactly
    cv2.imwrite(str(png), shot[:h, :w])


def imagine(args):
    """A scene from imagination: Claude writes it as an SVG (shapes + gradients for light and shadow), it is
    rendered to a tonal reference, and that reference is drawn stroke by stroke like a photo."""
    _need()
    import cv2
    src = Path(args.svg or args.png)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    if args.svg:
        ref_png = out / "_reference.png"
        rasterize_svg(args.svg, ref_png, args.width, args.height)
    else:
        ref_png = src
    ref = cv2.imread(str(ref_png), cv2.IMREAD_COLOR)
    if ref is None:
        raise SystemExit(f"cannot read reference {ref_png}")
    args.photo = str(src)
    return draw(args, ref=ref, source=str(src))


def review(args):
    """Rule-27 gate for portraits: figure connectivity via drawing_methods.review, plus value and edge fidelity."""
    _need()
    import cv2
    import numpy as np
    d = Path(args.dir)
    rec = json.loads((d / "receipt.json").read_text(encoding="utf-8"))
    sys.path.insert(0, str(Path(__file__).parent))
    import drawing_methods as dm
    if rec.get("subject", "portrait") == "portrait":
        gate = dm.review_svg(rec["svg"], tolerance=3.0)
        gate["pass"] = gate.get("status") == "PASS"
    else:   # no body to connect in a scene; the visual review still applies
        gate = {"status": "N/A", "pass": True, "scope": "scene without a figure: rule-27 body gate not applicable"}
    img = cv2.imread(rec["png"], cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255.0
    D = np.load(d / "_target_darkness.npy").astype(np.float32)
    labels = np.load(d / "_labels.npy")
    pr = MEDIUMS.get(rec.get("medium", "graphite"), MEDIUMS["graphite"])["paper"]
    paper = (0.299 * pr[0] + 0.587 * pr[1] + 0.114 * pr[2]) * 0.975 / 255.0
    drawn = np.clip(1 - img / paper, 0, 1)
    checks = []

    def add(cid, ok, observed, method):
        checks.append({"id": cid, "pass": bool(ok), "observed": observed, "method": method})
    for sigma, cid in ((6, "value-masses"), (2, "value-detail")):
        a = cv2.GaussianBlur(drawn, (0, 0), sigma)
        b = cv2.GaussianBlur(D, (0, 0), sigma)
        corr = float(np.corrcoef(a.ravel(), b.ravel())[0, 1])
        add(cid, corr > (0.9 if sigma == 6 else 0.8), {"pearson": round(corr, 3)},
            f"drawn darkness vs value map at blur {sigma}px (squint test)")
    face = labels == 3
    if face.any():
        a = cv2.GaussianBlur(drawn, (0, 0), 1.5)[face]
        b = cv2.GaussianBlur(D, (0, 0), 1.5)[face]
        corr = float(np.corrcoef(a, b)[0, 1])
        add("face-likeness", corr > 0.8, {"pearson": round(corr, 3)}, "face-skin darkness vs value map at 1.5px")
        mae = float(np.abs(cv2.GaussianBlur(drawn, (0, 0), 4) - cv2.GaussianBlur(D, (0, 0), 4))[face].mean())
        add("face-value-error", mae < 0.09, {"mae": round(mae, 3)}, "mean absolute value error on the face")
    full = float(drawn.max())
    lo, hi = np.percentile(drawn, [2, 98])
    add("value-range", hi - lo > 0.6, {"p2": round(float(lo), 3), "p98": round(float(hi), 3)},
        "a full value range from paper white to deep graphite")
    lap = cv2.Laplacian(img, cv2.CV_32F)
    dark = (labels == 4) if (labels == 4).any() else (cv2.GaussianBlur(D, (0, 0), 4) > 0.45)
    tex = float(np.abs(lap)[dark].mean()) if dark.any() else 0.0
    add("stroke-texture", tex > 0.01, {"dark_mass_laplacian": round(tex, 4)},
        "visible pencil texture (not flat fill) on large dark masses")
    add("strokes-only", rec.get("canvas_source") == "strokes_only", rec.get("canvas_source"),
        "receipt: canvas built from paper + strokes only")
    res = {"schema": "kosif.portrait.review.v1", "dir": str(d), "anatomy_gate": gate,
           "checks": checks, "max_darkness": round(full, 3),
           "pass": all(c["pass"] for c in checks) and gate.get("pass", False),
           "limits": "Measures value fidelity, texture and figure connectivity; it does not judge beauty. "
                     "Open the PNG and look at it before claiming anything."}
    (d / "review.json").write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"pass": res["pass"], "anatomy": gate.get("pass"),
                      "checks": {c["id"]: (c["pass"], c["observed"]) for c in checks}}, ensure_ascii=False))
    return 0 if res["pass"] else 1


def cards(args):
    data = json.loads(CARDS.read_text(encoding="utf-8"))
    for c in data["methods"]:
        if args.id and c["id"] != args.id:
            continue
        if args.id:
            print(json.dumps(c, ensure_ascii=False, indent=2))
        else:
            print(f'{c["id"]}  {c["name_en"]} — {c["name_ar"]}  [{", ".join(c["sources"])}]')


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("draw", help="photo (portrait or any subject) -> stroke-built drawing (PNG + layered SVG)")
    d.add_argument("--photo", required=True)
    d.add_argument("--out", required=True)
    d.add_argument("--name", default="portrait")
    d.add_argument("--models", help="dir with face_landmarker.task and selfie_multiclass.tflite (optional)")
    d.add_argument("--crop", help="x0,y0,x1,y1 in source pixels (default: trim screenshot bars)")
    d.add_argument("--scale", type=float, default=1.0)
    d.add_argument("--blend", type=float, default=0.55, help="stump blending on skin, 0..1")
    d.add_argument("--seed", type=int, default=7)
    i = sub.add_parser("imagine", help="draw a scene from imagination: a Claude-authored SVG (or any rendered PNG)")
    src = i.add_mutually_exclusive_group(required=True)
    src.add_argument("--svg", help="scene written as SVG; gradients carry the light and shadow families")
    src.add_argument("--png", help="any rendered reference (3D render, unified_draw output, ...)")
    i.add_argument("--out", required=True)
    i.add_argument("--name", default="drawing")
    i.add_argument("--width", type=int)
    i.add_argument("--height", type=int)
    i.add_argument("--scale", type=float, default=1.0)
    i.add_argument("--blend", type=float, default=0.55)
    i.add_argument("--seed", type=int, default=7)
    for q in (d, i):
        q.add_argument("--medium", choices=sorted(MEDIUMS), default="graphite")
        q.add_argument("--subject", choices=("auto", "portrait", "scene"), default="auto",
                       help="auto: portrait when a person is found, otherwise scene")
        q.add_argument("--background", choices=("auto", "straight", "flow"), default="auto",
                       help="straight = level/plumb strokes for architecture; flow = follow the form")
    i.set_defaults(models=None, crop=None)
    r = sub.add_parser("review", help="rule-27 gate + value/edge fidelity metrics on a drawn portrait")
    r.add_argument("--dir", required=True)
    c = sub.add_parser("cards", help="list or show the portrait method cards")
    c.add_argument("--id")
    a = ap.parse_args(argv)
    return {"draw": draw, "imagine": imagine, "review": review, "cards": cards}[a.cmd](a) or 0


if __name__ == "__main__":
    sys.exit(main())
