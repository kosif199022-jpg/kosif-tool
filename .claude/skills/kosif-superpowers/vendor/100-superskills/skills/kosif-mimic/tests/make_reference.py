"""Build a synthetic 'Pinterest dua video' with exactly known shots, transitions, text and animation.

    python make_reference.py OUT_DIR [--w 540 --h 960 --fonts DIR]

Writes OUT_DIR/ref.mp4, OUT_DIR/truth.json and OUT_DIR/clips/*.mp4 (the source clips).
Independent of the skill code on purpose: transitions and text are drawn here with plain NumPy/Pillow.
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from synth import GENERATORS  # noqa: E402

FPS = 30

SHOTS = [("clouds", {}), ("bokeh", {}), ("rain", {}), ("sunset", {}), ("blossoms", {}), ("candle", {}),
         ("clouds", {"seed": 11, "hue": (200, 120, 170)})]
# (type, ts, te) in frames — output frames [ts, te) are mixed frames of shot i and i+1
TRANS = [("fade", 70, 85), ("cut", 160, 160), ("fadeblack", 236, 254), ("wipeleft", 318, 330),
         ("zoomblur", 400, 412), ("slideup", 480, 492)]
TOTAL = 570

TEXTS = [
    {"id": 1, "lines": ["اللهم في يوم الجمعة"], "font": "Amiri-Bold.ttf", "in": "fade",
     "t": [12, 27, 96, 108], "out": "fade"},
    {"id": 2, "lines": ["اجعل لنا نورا في قلوبنا", "ونورا في قبورنا"], "font": "Amiri-Bold.ttf", "in": "words",
     "t": [118, 171, 230, 239], "out": "fade", "word_step": 8, "word_fade": 5},
    {"id": 3, "lines": ["يا رب في شهر ربيع الآخر"], "font": "ArefRuqaa-Bold.ttf", "in": "slideup",
     "t": [250, 265, 330, 340], "out": "fade", "dy": 36},
    {"id": 4, "lines": ["اغفر لنا وارحمنا"], "font": "Amiri-Bold.ttf", "in": "pop",
     "t": [352, 364, 430, 439], "out": "fade"},
    {"id": 5, "lines": ["آمين يا رب العالمين"], "font": "Amiri-Bold.ttf", "in": "blur",
     "t": [450, 468, 540, 552], "out": "blur"},
]


def ease_out_cubic(x):
    return 1 - (1 - x) ** 3


def shot_spans():
    spans = []
    for i in range(len(SHOTS)):
        start = 0 if i == 0 else TRANS[i - 1][1]
        end = TOTAL if i == len(SHOTS) - 1 else TRANS[i][2]
        spans.append((start, end))
    return spans


def render_clips(out_dir: Path, w, h):
    gens = []
    spans = shot_spans()
    clip_dir = out_dir / "clips"
    clip_dir.mkdir(parents=True, exist_ok=True)
    for i, ((kind, kw), (a, b)) in enumerate(zip(SHOTS, spans)):
        fn = GENERATORS[kind](w, h, **kw)
        gens.append(fn)
    return gens


def zoom_blur(img, z, sigma):
    h, w = img.shape[:2]
    M = cv2.getRotationMatrix2D((w / 2, h / 2), 0, z)
    out = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT101)
    if sigma > 0.3:
        k = int(sigma * 3) * 2 + 1
        out = cv2.GaussianBlur(out, (k, k), sigma)
    return out


def mix_transition(kind, A, B, j, D):
    q = (j + 1) / (D + 1)  # weight of B
    Af, Bf = A.astype(np.float32), B.astype(np.float32)
    h, w = A.shape[:2]
    if kind == "fade":
        return (Af * (1 - q) + Bf * q)
    if kind == "fadeblack":
        if q < 0.5:
            return Af * (1 - q / 0.5)
        return Bf * ((q - 0.5) / 0.5)
    if kind == "wipeleft":
        x0 = int(w * (1 - q))
        out = Af.copy()
        out[:, x0:] = Bf[:, x0:]
        return out
    if kind == "slideup":
        off = int(round(h * q))
        out = np.empty_like(Af)
        out[: h - off] = Af[off:]
        out[h - off:] = Bf[: off]
        return out
    if kind == "zoomblur":
        if q < 0.5:
            u = q / 0.5
            return zoom_blur(A, 1 + 0.4 * u, 10 * u).astype(np.float32)
        u = (1 - q) / 0.5
        return zoom_blur(B, 1 + 0.4 * u, 10 * u).astype(np.float32)
    raise ValueError(kind)


# ----------------------------------------------------------------------------- text

def line_layers(text, font_path, size, W, H, cx, cy):
    """Full-frame float alpha layers per word for one line centred at (cx, cy).

    The line is shaped as a whole (like an editing app does); word layers are prefix differences,
    so inter-word kerning/overlaps of calligraphic fonts are preserved."""
    font = ImageFont.truetype(font_path, size, layout_engine=ImageFont.Layout.RAQM)
    words = text.split(" ")
    l, t, r, b = font.getbbox(text, anchor="rs", direction="rtl", language="ar")
    ax = cx + (r - l) / 2 - r          # centre the ink box horizontally
    ay = cy + (b - t) / 2 - b          # and vertically
    layers = []
    prev = np.zeros((H, W), np.float32)
    for k in range(1, len(words) + 1):
        im = Image.new("L", (W, H), 0)
        ImageDraw.Draw(im).text((ax, ay), " ".join(words[:k]), font=font, fill=255, anchor="rs",
                                direction="rtl", language="ar")
        cur = np.asarray(im, np.float32) / 255.0
        layers.append(np.clip(cur - prev, 0, 1))
        prev = np.maximum(prev, cur)
    return words, layers


def make_text_assets(W, H, fonts_dir: Path, scale: float):
    assets = []
    for ev in TEXTS:
        size = int(round(42 * scale))
        lines = ev["lines"]
        n = len(lines)
        gap = int(round(58 * scale))
        ys = [H / 2 + (k - (n - 1) / 2) * gap for k in range(n)]
        word_layers = []
        truth_lines = []
        for k, line in enumerate(lines):
            words, layers = line_layers(line, str(fonts_dir / ev["font"]), size, W, H, W / 2, ys[k])
            word_layers += layers
            m = np.max(np.stack(layers), 0) > 0.5
            yy, xx = np.nonzero(m)
            truth_lines.append({"text": line, "bbox": [int(xx.min()), int(yy.min()), int(xx.max()) + 1, int(yy.max()) + 1]})
        assets.append({"ev": ev, "word_layers": word_layers, "size": size, "lines": truth_lines})
    return assets


def text_alpha_at(asset, n):
    ev = asset["ev"]
    a0, a1, b0, b1 = ev["t"]
    wl = asset["word_layers"]
    full = np.max(np.stack(wl), 0)
    if n < a0 or n >= b1:
        return None, None
    params = {"alpha": 1.0, "dy": 0.0, "scale": 1.0, "blur": 0.0}
    layer = full
    if n < a1:
        u = (n - a0) / (a1 - a0)
        kind = ev["in"]
        if kind == "fade":
            params["alpha"] = u
        elif kind == "slideup":
            e = ease_out_cubic(u)
            params["alpha"] = min(1, u * 1.4)
            params["dy"] = ev["dy"] * (1 - e)
        elif kind == "pop":
            params["alpha"] = min(1, u * 2)
            params["scale"] = 0.6 + 0.48 * (u / 0.7) if u < 0.7 else 1.08 - 0.08 * ((u - 0.7) / 0.3)
        elif kind == "blur":
            params["alpha"] = min(1, u * 2)
            params["blur"] = 10 * (1 - u)
        elif kind == "words":
            step, wf = ev["word_step"], ev["word_fade"]
            acc = np.zeros_like(full)
            for k, L in enumerate(wl):
                t0 = a0 + k * step
                aw = np.clip((n - t0 + 1) / wf, 0, 1)
                acc = np.maximum(acc, L * aw)
            layer = acc
    elif n >= b0:
        u = (n - b0 + 1) / (b1 - b0 + 1)
        if ev["out"] == "fade":
            params["alpha"] = 1 - u
        elif ev["out"] == "blur":
            params["alpha"] = 1 - u
            params["blur"] = 8 * u
    return layer, params


def apply_text(frame, asset, n, shadow=(2, 3, 3.0, 0.55)):
    layer, p = text_alpha_at(asset, n)
    if layer is None:
        return frame
    h, w = layer.shape
    L = layer
    if p["scale"] != 1.0 or p["dy"] != 0:
        M = cv2.getRotationMatrix2D((w / 2, h / 2), 0, p["scale"])
        M[1, 2] += p["dy"]
        L = cv2.warpAffine(L, M, (w, h), flags=cv2.INTER_LINEAR)
    if p["blur"] > 0.3:
        k = int(p["blur"] * 3) * 2 + 1
        L = cv2.GaussianBlur(L, (k, k), p["blur"])
    L = L * p["alpha"]
    dx, dy, sb, so = shadow
    S = np.roll(np.roll(L, dy, 0), dx, 1)
    k = int(sb * 3) * 2 + 1
    S = cv2.GaussianBlur(S, (k, k), sb) * so
    f = frame.astype(np.float32)
    f = f * (1 - S[..., None])
    f = f * (1 - L[..., None]) + 255.0 * L[..., None]
    return f


def synth_audio(path: Path, seconds: float, sr=48000):
    t = np.arange(int(seconds * sr)) / sr
    chords = [(220.0, 261.63, 329.63), (174.61, 220.0, 261.63), (196.0, 246.94, 293.66), (164.81, 207.65, 246.94)]
    sig = np.zeros_like(t)
    seg = 4.0
    for i, ch in enumerate(chords * 3):
        a, b = i * seg, (i + 1) * seg + 1.0
        m = (t >= a) & (t < b)
        env = np.clip((t[m] - a) / 0.8, 0, 1) * np.clip((b - t[m]) / 1.2, 0, 1)
        for f in ch:
            sig[m] += env * (np.sin(2 * np.pi * f * t[m]) + 0.3 * np.sin(4 * np.pi * f * t[m])) / 3
    rng = np.random.default_rng(0)
    sig += 0.01 * rng.standard_normal(len(t))
    sig = sig / np.max(np.abs(sig)) * 0.5
    st = np.stack([sig, np.roll(sig, 300)], 1)
    pcm = (st * 32767).astype(np.int16)
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(pcm.tobytes())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--w", type=int, default=540)
    ap.add_argument("--h", type=int, default=960)
    ap.add_argument("--fonts", default=str(Path(__file__).resolve().parent.parent / "assets" / "fonts"))
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    W, H = a.w, a.h
    scale = W / 540
    gens = render_clips(out, W, H)
    spans = shot_spans()
    assets = make_text_assets(W, H, Path(a.fonts), scale)
    # look: 15% darkening, vignette, light grain
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) / math.sqrt(2)
    vig = (1 - 0.45 * np.clip(r, 0, 1) ** 2.2)[..., None]
    rng = np.random.default_rng(5)
    wav = out / "pad.wav"
    synth_audio(wav, TOTAL / FPS + 0.2)
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-framerate", str(FPS),
           "-i", "-", "-i", str(wav), "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out / "ref.mp4")]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for n in range(TOTAL):
        # which shots are active
        frame = None
        for i, (s0, s1) in enumerate(spans):
            pass
        ti = None
        for k, (kind, ts, te) in enumerate(TRANS):
            if ts <= n < te:
                ti = k
                break
        if ti is not None:
            kind, ts, te = TRANS[ti]
            A = gens[ti](n - spans[ti][0])
            B = gens[ti + 1](n - spans[ti + 1][0])
            frame = mix_transition(kind, A, B, n - ts, te - ts)
        else:
            for i, (s0, s1) in enumerate(spans):
                body0 = TRANS[i - 1][2] if i > 0 else 0
                body1 = TRANS[i][1] if i < len(TRANS) else TOTAL
                if body0 <= n < body1:
                    frame = gens[i](n - s0).astype(np.float32)
                    break
        frame = frame * 0.85 * vig
        frame = frame + rng.normal(0, 3.0, frame.shape).astype(np.float32)
        for asset in assets:
            frame = apply_text(frame, asset, n)
        proc.stdin.write(np.clip(frame, 0, 255).astype(np.uint8).tobytes())
    proc.stdin.close()
    proc.wait()
    truth = {
        "w": W, "h": H, "fps": FPS, "frames": TOTAL,
        "shots": [{"kind": k, "start": s0, "end": s1} for (k, _), (s0, s1) in zip(SHOTS, spans)],
        "transitions": [{"type": k, "ts": ts, "te": te} for k, ts, te in TRANS],
        "texts": [{"id": a_["ev"]["id"], "lines": a_["ev"]["lines"], "font": a_["ev"]["font"], "size": a_["size"],
                   "in": a_["ev"]["in"], "out": a_["ev"]["out"], "t": a_["ev"]["t"], "line_boxes": a_["lines"],
                   "color": "#FFFFFF"} for a_ in assets],
        "look": {"darken": 0.15, "vignette": 0.45, "grain_sigma": 3.0},
    }
    (out / "truth.json").write_text(json.dumps(truth, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", out / "ref.mp4")


if __name__ == "__main__":
    main()
