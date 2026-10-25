#!/usr/bin/env python3
"""Build a «الدعاء» (Friday dua) reel from your own clips, text and voice, with the measured reference style.

    python3 styles/dua/kit/build_dua.py project.json [--out reel.mp4] [--preview] [--frames 0:90]

project.json
{
  "clips":   ["shots/01.mp4", "shots/02.jpg", ...],     # one per dua line (video or still); cycled if fewer
  "audio":   "voice.m4a",                               # optional; copied untouched (-c:a copy) when the codec fits MP4
  "date":    "22.08.2025",
  "subtitle":"ليلة جمعة مبـــاركة",                       # optional, default from the style
  "title":   "الأربعاء",                                  # optional: another day's title instead of «الجُمُعَة»
  "lines":   [{"text": "اللَّهُمَّ في ليلة الجمعة", "start": 0.0, "end": 1.68}, ...],   # phrase timings (seconds)
  "asr":     "asr.json",                                # alternative to start/end: faster-whisper segments, one per line
  "duration": 15.4,                                     # optional (default: last end + 0.4)
  "fps": 30,                                            # optional (style default 30)
  "transitions": "reference",                           # or a list: blur_in | mirror_out_blur_in | zoom_out_cut | spin_zoom_blur | cut
  "grade": 0.6                                          # 0..1 strength of the warm low-key grade toward the style means
}

Pipeline (all measured in styles/dua/dua.style.json):
  1. text layers rendered once by layers.cjs (Chromium, real Arabic shaping), then ink-fitted to the measured boxes;
  2. one shot per phrase, cut on the phrase onset; stills get a 3 % slow push-in;
  3. transitions on cuts (blur-in, mirror-out, push-in cut, spin/zoom blur); text never blurs;
  4. text timing: dua line in 0.2 s after its cut (0.17 s fade), out 0.3 s before the next cut (0.15 s fade);
     intro: fade from black 0.6 s, the day number flies in on an arc (0.1→1.1 s); outro: day drifts left, overlay fades;
  5. one H.264 encode (CRF 18, yuv420p) with the voice track copied untouched.
Needs numpy, Pillow, ffmpeg, Node + Playwright (for layers). OpenCV is used for blur when present.
"""
from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

try:
    import cv2  # optional, faster blurs
except ImportError:  # pragma: no cover
    cv2 = None

KIT = Path(__file__).resolve().parent
STYLE = KIT.parent
REPO = STYLE.parents[1]
SPEC = json.loads((STYLE / "dua.style.json").read_text(encoding="utf-8"))
W, H = SPEC["output"]["w"], SPEC["output"]["h"]


# ----------------------------------------------------------------- easing
def ease_out_cubic(x): x = min(max(x, 0.0), 1.0); return 1 - (1 - x) ** 3
def ease_in_out_sine(x): x = min(max(x, 0.0), 1.0); return 0.5 - 0.5 * math.cos(math.pi * x)
def ramp(t, a, b): return 0.0 if t <= a else 1.0 if t >= b else (t - a) / (b - a)


# ----------------------------------------------------------------- project
def load_project(path: Path) -> dict:
    p = json.loads(path.read_text(encoding="utf-8"))
    base = path.parent
    if p.get("asr") and not any("start" in l for l in p.get("lines", [])):
        segs = json.loads((base / p["asr"]).read_text(encoding="utf-8"))["segments"]
        texts = [l["text"] if isinstance(l, dict) else l for l in p.get("lines", [])] or [s["text"] for s in segs]
        p["lines"] = [{"text": texts[i] if i < len(texts) else s["text"], "start": s["start"], "end": s["end"]} for i, s in enumerate(segs)]
    lines = p["lines"]
    if not lines:
        raise SystemExit("project has no lines")
    lines[0]["start"] = 0.0
    p["duration"] = float(p.get("duration") or (lines[-1]["end"] + 0.4))
    p["fps"] = int(p.get("fps") or SPEC["output"]["fps"])
    p["clips"] = [str((base / c).resolve()) for c in p.get("clips", [])]
    if not p["clips"]:
        raise SystemExit("project needs at least one clip (your own or licensed footage / photos)")
    if p.get("audio"):
        p["audio"] = str((base / p["audio"]).resolve())
    p.setdefault("date", "22.08.2025")
    p.setdefault("subtitle", SPEC["layers"]["subtitle_gold"]["text"])
    p.setdefault("transitions", "reference")
    p.setdefault("grade", 0.6)
    return p


# ----------------------------------------------------------------- layers
def render_layers(p: dict, out: Path) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    req = {"date": p["date"], "subtitle": p["subtitle"], "lines": [l["text"] for l in p["lines"]]}
    if p.get("title"):
        req["title_text"] = p["title"]
    (out / "request.json").write_text(json.dumps(req, ensure_ascii=False), encoding="utf-8")
    r = subprocess.run(["node", str(KIT / "layers.cjs"), str(out / "request.json"), str(out)], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("layers.cjs failed:\n" + r.stderr[-2000:])
    meta = json.loads((out / "layers.json").read_text())
    return {k: np.asarray(Image.open(out / v).convert("RGBA")) for k, v in meta["layers"].items()}


def ink_bbox(a: np.ndarray, thr=128):
    ys, xs = np.where(a[..., 3] >= thr)
    return (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1) if len(xs) else None


def place(src: np.ndarray, box, scale: float, anchor_xy, anchor="center") -> np.ndarray:
    """Crop src to box, scale, and paste so that its anchor lands on anchor_xy. Returns a full-frame RGBA."""
    x0, y0, x1, y1 = box
    pad = 12
    x0, y0, x1, y1 = max(0, x0 - pad), max(0, y0 - pad), min(W, x1 + pad), min(H, y1 + pad)
    crop = Image.fromarray(src[y0:y1, x0:x1])
    nw, nh = max(1, round(crop.width * scale)), max(1, round(crop.height * scale))
    crop = crop.resize((nw, nh), Image.LANCZOS)
    ax, ay = anchor_xy
    if anchor == "right":
        ox, oy = ax - (nw - pad * scale), ay - nh / 2
    else:
        ox, oy = ax - nw / 2, ay - nh / 2
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    canvas.alpha_composite(crop, (int(round(ox)), int(round(oy))))
    return np.asarray(canvas)


def fit_layers(raw: dict) -> dict:
    """Fit each layer's real ink box to the box measured on the reference (spec), keeping glyph proportions."""
    L = SPEC["layers"]
    out = {}
    if "title" in raw:
        tb = ink_bbox(raw["title"]); X0, Y0, X1, Y1 = L["title"]["bbox_px"]
        s = math.sqrt(((X1 - X0) / (tb[2] - tb[0])) * ((Y1 - Y0) / (tb[3] - tb[1])))
        out["title"] = place(raw["title"], tb, s, (X1, (Y0 + Y1) / 2), "right")
    # day + rest share one transform (union box) so the date stays one typographic unit
    union = np.maximum(raw["date_day"], raw["date_rest"])
    db = ink_bbox(union); X0, Y0, X1, Y1 = L["date"]["bbox_px"]
    s = (X1 - X0) / (db[2] - db[0])
    for k in ("date_day", "date_rest"):
        out[k] = place(raw[k], db, s, (X1, (Y0 + Y1) / 2), "right")
    gb = ink_bbox(raw["gold"]); X0, Y0, X1, Y1 = L["subtitle_gold"]["bbox_px"]
    s = (X1 - X0) / (gb[2] - gb[0])
    out["gold"] = place(raw["gold"], gb, s, ((X0 + X1) / 2, (Y0 + Y1) / 2))
    # dua lines: one global scale calibrated on the reference ink height of a single line (≈92 px), centred
    singles = [k for k in raw if k.startswith("dua_")]
    hs = [ink_bbox(raw[k])[3] - ink_bbox(raw[k])[1] for k in singles if ink_bbox(raw[k])]
    ref_h = SPEC["layers"]["dua"].get("ink_height_single_px", 92)
    s = ref_h / float(np.median(hs)) if hs else 1.0
    for k in singles:
        b = ink_bbox(raw[k])
        if not b:
            continue
        two = (b[3] - b[1]) > 1.6 * float(np.median(hs))
        cy = SPEC["layers"]["dua"]["two_line_y_center"] if two else SPEC["layers"]["dua"]["single_line_y_center"]
        out[k] = place(raw[k], b, s, (545, cy))
    return out


# ----------------------------------------------------------------- footage
def ffprobe_video(path: str) -> bool:
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=codec_type,nb_frames,duration", "-of", "json", path], capture_output=True, text=True)
    try:
        s = json.loads(r.stdout)["streams"][0]
        return s.get("codec_type") == "video" and not path.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
    except (ValueError, KeyError, IndexError):
        return False


class ShotSource:
    """Frames of one shot at output size: video (cover-fit, looped) or a still with a 3 % slow push-in."""

    def __init__(self, path: str, n: int, fps: int):
        self.n, self.i = n, 0
        self.video = ffprobe_video(path)
        if self.video:
            vf = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={fps}"
            self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-stream_loop", "-1", "-i", path, "-vf", vf, "-frames:v", str(n),
                                       "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
        else:
            im = Image.open(path).convert("RGB")
            r = max(W / im.width, H / im.height) * 1.04
            self.base = im.resize((math.ceil(im.width * r), math.ceil(im.height * r)), Image.LANCZOS)

    def next(self) -> np.ndarray:
        self.i += 1
        if self.video:
            buf = self.p.stdout.read(W * H * 3)
            if len(buf) < W * H * 3:
                buf = getattr(self, "_last", bytes(W * H * 3))
            self._last = buf
            return np.frombuffer(buf, np.uint8).reshape(H, W, 3).copy()
        z = 1.0 + 0.03 * (self.i / max(1, self.n))          # slow push-in
        bw, bh = self.base.size
        cw, ch = W * (bw / (W * 1.04)) / z, H * (bh / (H * 1.04)) / z
        cx, cy = bw / 2, bh / 2
        crop = self.base.crop((int(cx - cw / 2), int(cy - ch / 2), int(cx + cw / 2), int(cy + ch / 2))).resize((W, H), Image.BILINEAR)
        return np.asarray(crop).copy()

    def close(self):
        if self.video:
            self.p.stdout.close(); self.p.wait()


def grade(img: np.ndarray, strength: float, target=None) -> np.ndarray:
    """Warm low-key grade toward the reference footage means (Lab), partial strength."""
    if strength <= 0:
        return img
    t = target or SPEC["palette"]["footage_lab_mean"]
    f = img.astype(np.float32)
    lum = f.mean()
    want = t["L"] * 2.55
    gain = 1 + strength * (want / max(lum, 1) - 1) * 0.6
    f *= gain
    f[..., 0] *= 1 + 0.05 * strength
    f[..., 2] *= 1 - 0.07 * strength
    return np.clip(f, 0, 255).astype(np.uint8)


# ----------------------------------------------------------------- effects
def motion_blur(img: np.ndarray, px: float, angle_deg=0.0) -> np.ndarray:
    k = int(round(px))
    if k < 2:
        return img
    if cv2 is not None:
        kern = np.zeros((k, k), np.float32); kern[k // 2, :] = 1.0 / k
        M = cv2.getRotationMatrix2D((k / 2 - 0.5, k / 2 - 0.5), angle_deg, 1.0)
        kern = cv2.warpAffine(kern, M, (k, k)); kern /= max(kern.sum(), 1e-6)
        return cv2.filter2D(img, -1, kern)
    from PIL import ImageFilter
    return np.asarray(Image.fromarray(img).filter(ImageFilter.BoxBlur(k / 2)))


def zoom_blur(img: np.ndarray, amount: float, spin_deg=0.0, n=8) -> np.ndarray:
    """Radial zoom (and optional spin) blur: average of scaled/rotated copies about the centre."""
    if amount < 0.004 and abs(spin_deg) < 0.2:
        return img
    acc = np.zeros(img.shape, np.float32)
    for i in range(n):
        f = i / (n - 1)
        s, a = 1 + amount * f, spin_deg * f
        if cv2 is not None:
            M = cv2.getRotationMatrix2D((W / 2, H / 2), a, s)
            acc += cv2.warpAffine(img, M, (W, H), borderMode=cv2.BORDER_REFLECT).astype(np.float32)
        else:
            im = Image.fromarray(img).rotate(a, resample=Image.BILINEAR).resize((int(W * s), int(H * s)))
            l, t = (im.width - W) // 2, (im.height - H) // 2
            acc += np.asarray(im.crop((l, t, l + W, t + H))).astype(np.float32)
    return (acc / n).astype(np.uint8)


def mirror_lower(img: np.ndarray, a: float) -> np.ndarray:
    if a <= 0:
        return img
    out = img.copy()
    top = img[: H // 2][::-1]
    out[H // 2:] = (img[H // 2:].astype(np.float32) * (1 - a) + top[: H - H // 2].astype(np.float32) * a).astype(np.uint8)
    return out


def push(img: np.ndarray, s: float) -> np.ndarray:
    if s <= 1.0005:
        return img
    if cv2 is not None:
        M = cv2.getRotationMatrix2D((W / 2, H / 2), 0, s)
        return cv2.warpAffine(img, M, (W, H), borderMode=cv2.BORDER_REFLECT)
    im = Image.fromarray(img).resize((int(W * s), int(H * s)))
    l, t = (im.width - W) // 2, (im.height - H) // 2
    return np.asarray(im.crop((l, t, l + W, t + H)))


def transition_kinds(p, n_cuts):
    seq = SPEC["transitions"]["sequence_reference"]
    if p["transitions"] == "reference":
        return [seq[i % len(seq)] for i in range(n_cuts)]
    return [p["transitions"][i % len(p["transitions"])] for i in range(n_cuts)]


def apply_transition(frame: np.ndarray, kind: str, t_into: float | None, t_before: float | None) -> np.ndarray:
    """t_into: seconds since this shot's cut (incoming side); t_before: seconds until the next cut (outgoing side)."""
    out = frame
    # outgoing side (end of a shot) depends on the NEXT cut's kind (passed in by the caller)
    if t_before is not None:
        k_out, tb = t_before
        if k_out == "mirror_out_blur_in" and tb < 0.3:
            out = mirror_lower(out, ease_out_cubic(1 - tb / 0.3))
        elif k_out == "zoom_out_cut" and tb < 0.1:
            out = push(out, 1 + 0.06 * (1 - tb / 0.1))
        elif k_out == "spin_zoom_blur" and tb < 0.45:
            x = 1 - tb / 0.45
            out = zoom_blur(out, 0.10 * x * x, spin_deg=6 * x * x)
    if t_into is not None:
        k_in, ti = t_into
        if k_in in ("blur_in", "mirror_out_blur_in"):
            d = 0.3 if k_in == "blur_in" else 0.25
            if ti < d:
                out = motion_blur(out, 28 * (1 - ease_out_cubic(ti / d)), angle_deg=8)
        elif k_in == "zoom_out_cut" and ti < 0.15:
            out = motion_blur(out, 12 * (1 - ti / 0.15))
        elif k_in == "spin_zoom_blur" and ti < 0.17:
            x = 1 - ease_out_cubic(ti / 0.17)
            out = zoom_blur(out, 0.12 * x, spin_deg=5 * x)
    return out


# ----------------------------------------------------------------- compositing
def over(dst: np.ndarray, layer: np.ndarray, opacity: float, dx=0, dy=0) -> None:
    if opacity <= 0.003 or layer is None:
        return
    src = layer
    if dx or dy:
        src = np.zeros_like(layer)
        xs0, xd0 = (0, dx) if dx >= 0 else (-dx, 0)
        ys0, yd0 = (0, dy) if dy >= 0 else (-dy, 0)
        w, h = W - abs(dx), H - abs(dy)
        if w <= 0 or h <= 0:
            return
        src[yd0:yd0 + h, xd0:xd0 + w] = layer[ys0:ys0 + h, xs0:xs0 + w]
    a = src[..., 3:4].astype(np.float32) / 255.0 * opacity
    ys = np.where(a[..., 0].max(1) > 0)[0]
    if not len(ys):
        return
    y0, y1 = ys[0], ys[-1] + 1
    d = dst[y0:y1].astype(np.float32)
    dst[y0:y1] = (d * (1 - a[y0:y1]) + src[y0:y1, :, :3].astype(np.float32) * a[y0:y1]).astype(np.uint8)


def build(project: Path, out: Path, preview=False, frames=None) -> dict:
    p = load_project(project)
    fps, T = p["fps"], p["duration"]
    work = out.parent / (out.stem + "_layers")
    raw = render_layers(p, work)
    lay = fit_layers(raw)
    lines = p["lines"]
    cuts = [0.0] + [l["start"] for l in lines[1:]]
    kinds = transition_kinds(p, len(cuts) - 1)
    N = int(round(T * fps))
    f0, f1 = (frames or (0, N))
    shots, k = [], 0
    for i, c in enumerate(cuts):
        end = cuts[i + 1] if i + 1 < len(cuts) else T
        shots.append((c, end, p["clips"][i % len(p["clips"])]))
    # day-number flight: from centre-low (start) into its slot; offsets relative to its fitted position
    db = ink_bbox(lay["date_day"]); dcx, dcy = (db[0] + db[2]) / 2, (db[1] + db[3]) / 2
    sx, sy = 540 - dcx, 1020 - dcy                       # start offset (centre, just above the first dua line)
    cx_, cy_ = sx * 0.55 + 60, sy * 0.25 - 40            # arc control point

    def day_offset(t):
        if t < 0.1:
            return int(sx), int(sy)
        if t < 1.1:
            u = ease_out_cubic((t - 0.1) / 1.0)
            bx = (1 - u) ** 2 * sx + 2 * (1 - u) * u * cx_
            by = (1 - u) ** 2 * sy + 2 * (1 - u) * u * cy_
            return int(round(bx)), int(round(by))
        if t > T - 0.73:
            return int(round(-40 * ease_in_out_sine((t - (T - 0.73)) / 0.35))), 0
        return 0, 0

    scale = 0.5 if preview else 1.0
    ow, oh = int(W * scale) // 2 * 2, int(H * scale) // 2 * 2
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-"]
    audio_note = "none"
    if p.get("audio") and not frames:
        cmd += ["-i", p["audio"], "-map", "0:v", "-map", "1:a"]   # no -ss: keep the AAC priming packet so the stream stays byte-identical
        codec = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=codec_name", "-of", "csv=p=0", p["audio"]], capture_output=True, text=True).stdout.strip()
        if codec in ("aac", "mp3", "alac", "ac3", "opus"):
            cmd += ["-c:a", "copy"]; audio_note = f"{codec} copied untouched"
        else:
            cmd += ["-c:a", "aac", "-b:a", "320k"]; audio_note = f"{codec} → AAC 320k (MP4 cannot carry {codec}; keep your master)"
        cmd += ["-t", f"{T:.3f}"]
    cmd += ["-vf", f"scale={ow}:{oh}" if preview else "null", "-c:v", "libx264", "-crf", str(SPEC["output"]["crf"]), "-preset", "veryfast" if preview else "slow",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)]
    enc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    si = 0
    src = None
    for fi in range(N):
        t = fi / fps
        while si + 1 < len(shots) and t >= shots[si + 1][0]:
            si += 1
            if src:
                src.close()
            src = None
        c0, c1, clip = shots[si]
        if src is None:
            src = ShotSource(clip, max(1, int(round((c1 - c0) * fps)) + 2), fps)
        frame = src.next()
        if not (f0 <= fi < f1):
            continue
        frame = grade(frame, p["grade"])
        k_in = (kinds[si - 1], t - c0) if si > 0 else None
        k_out = (kinds[si], c1 - t) if si < len(kinds) else None
        frame = apply_transition(frame, None, k_in, k_out)
        # global fade from black (intro)
        if t < 0.6:
            frame = (frame.astype(np.float32) * ease_out_cubic(t / 0.6)).astype(np.uint8)
        frame = frame.copy()
        # persistent overlay opacity: intro fade 0.05→0.6, outro fade over the last 0.38 s
        ov = ramp(t, 0.05, 0.6) * (1 - ramp(t, T - 0.38, T - 0.05))
        over(frame, lay.get("title"), ov)
        over(frame, lay["date_rest"], ov)
        ddx, ddy = day_offset(t)
        over(frame, lay["date_day"], ov if t >= 0.1 else ramp(t, 0.0, 0.1) * ov, ddx, ddy)
        over(frame, lay["gold"], ov)
        # dua line of this shot: in 0.2 s after the cut, out 0.3 s before the next cut
        key = f"dua_{si}"
        if key in lay:
            tin = 0.23 if si == 0 else c0 + 0.2
            tout = (c1 - 0.3) if si + 1 < len(shots) else (T - 0.2)
            a = ramp(t, tin, tin + 0.17) * (1 - ramp(t, tout, tout + 0.15))
            if si + 1 == len(shots):
                a *= 1 - ramp(t, T - 0.38, T - 0.05)
            over(frame, lay[key], a)
        enc.stdin.write(frame.tobytes())
    if src:
        src.close()
    enc.stdin.close()
    enc.wait()
    rep = {"out": str(out), "frames": f1 - f0, "fps": fps, "duration_s": round((f1 - f0) / fps, 3), "shots": len(shots),
           "transitions": kinds, "audio": audio_note, "preview": preview}
    (out.with_suffix(".report.json")).write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(rep, ensure_ascii=False))
    return rep


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project"); ap.add_argument("--out", default=None)
    ap.add_argument("--preview", action="store_true", help="half-size, fast encode")
    ap.add_argument("--frames", default=None, help="render only frames a:b (debug)")
    a = ap.parse_args(argv)
    if not shutil.which("ffmpeg") or not shutil.which("node"):
        raise SystemExit("needs ffmpeg and node (+ Playwright) on PATH")
    proj = Path(a.project).resolve()
    out = Path(a.out).resolve() if a.out else proj.with_name("dua_reel.mp4")
    fr = tuple(int(x) for x in a.frames.split(":")) if a.frames else None
    build(proj, out, a.preview, fr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
