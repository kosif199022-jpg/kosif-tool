"""Video breakdown for rebuilding: everything that can be MEASURED about a reference film (motion graphics, animation,
product demo, SaaS explainer), across its whole duration, plus the frames Claude must LOOK at to describe the rest.
The method is references/video-breakdown.md; `kmotion omniprompt` turns the filled brief into a generation prompt.

    python scripts/kmotion.py analyze VIDEO [--out DIR] [--max-beat 3.0] [--transcribe]
        → DIR/analysis.json   measured: specs, beats (cuts + motion segments ≤ max-beat s), per-beat palette with hex and
                              share, background colour, brightness, motion energy, global pan, transition guess,
                              audio loudness, tempo, onsets and which beat edges they hit (SFX), optional transcript
          DIR/frames/         3 full-resolution stills per beat (in, mid, out) — read them before writing anything
          DIR/overview.jpg    every beat's mid frame with its time;  DIR/timeline.jpg  a still every 0.5 s
          DIR/brief.json      the breakdown to fill from the frames (composition, camera, subjects, text, type, icons,
                              light, motion, transition, audio per beat; style line, type lock, final frame)
    python scripts/kmotion.py analyze --batch FOLDER [--out DIR]
        measured part only for every video in FOLDER (no frames kept) → DIR/library.json + library.csv: a style library
        (pace, cut rate, palettes, motion energy, loudness) to learn from many references at once
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
FF = shutil.which("ffmpeg") or "ffmpeg"
FP = shutil.which("ffprobe") or "ffprobe"
VIDEO_EXT = {".mp4", ".mov", ".webm", ".mkv", ".m4v", ".avi", ".gif"}


# ───────────────────────── probing and sampling ─────────────────────────
def probe(video: Path) -> dict:
    r = subprocess.run([FP, "-v", "error", "-show_entries", "stream=codec_type,codec_name,width,height,r_frame_rate,avg_frame_rate,sample_rate,channels:format=duration,bit_rate",
                        "-of", "json", str(video)], capture_output=True, text=True, check=True)
    d = json.loads(r.stdout)
    v = next((s for s in d["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in d["streams"] if s["codec_type"] == "audio"), None)
    if not v:
        raise ValueError(f"{video}: no video stream")
    fr = lambda s: (lambda n, dn: float(n) / float(dn or 1))(*s.split("/")) if s and s != "0/0" else 0.0  # noqa: E731
    w, h = int(v["width"]), int(v["height"])
    g = math.gcd(w, h)
    common = {(16, 9): "16:9", (9, 16): "9:16", (1, 1): "1:1", (4, 5): "4:5", (4, 3): "4:3", (21, 9): "21:9", (2, 1): "2:1"}
    ratio = common.get((w // g, h // g)) or min(common.items(), key=lambda kv: abs(kv[0][0] / kv[0][1] - w / h))[1] + " (≈)"
    return {"width": w, "height": h, "aspect": ratio, "fps": round(fr(v.get("avg_frame_rate")) or fr(v.get("r_frame_rate")), 3),
            "duration": round(float(d["format"].get("duration") or 0), 3), "codec": v.get("codec_name"),
            "audio": {"codec": a.get("codec_name"), "rate": int(a.get("sample_rate", 0)), "channels": a.get("channels")} if a else None}


def sample(video: Path, fps: float = 6.0, width: int = 192) -> tuple[np.ndarray, float]:
    """Small RGB frames at `fps` across the whole film: (N, h, w, 3) uint8."""
    info = probe(video)
    h = max(2, int(round(info["height"] * width / info["width"] / 2) * 2))
    r = subprocess.run([FF, "-v", "error", "-i", str(video), "-vf", f"fps={fps},scale={width}:{h}:flags=area", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                       capture_output=True, check=True)
    arr = np.frombuffer(r.stdout, np.uint8)
    n = arr.size // (width * h * 3)
    return arr[: n * width * h * 3].reshape(n, h, width, 3), fps


# ───────────────────────── colour ─────────────────────────
def hexof(c) -> str:
    return "#%02x%02x%02x" % tuple(int(max(0, min(255, round(float(x))))) for x in c)


def palette(px: np.ndarray, k: int = 6, iters: int = 12, seed: int = 3) -> list[dict]:
    """k-means in RGB (numpy, deterministic): the colours that cover the frames, with their share."""
    px = px.reshape(-1, 3).astype(np.float32)
    if len(px) > 20000:
        px = px[np.random.default_rng(seed).choice(len(px), 20000, replace=False)]
    rng = np.random.default_rng(seed)
    cent = px[rng.choice(len(px), min(k, len(px)), replace=False)]
    for _ in range(iters):
        lab = np.argmin(((px[:, None, :] - cent[None]) ** 2).sum(-1), 1)
        for j in range(len(cent)):
            sel = px[lab == j]
            if len(sel):
                cent[j] = sel.mean(0)
    lab = np.argmin(((px[:, None, :] - cent[None]) ** 2).sum(-1), 1)
    share = np.bincount(lab, minlength=len(cent)) / len(lab)
    out = [{"hex": hexof(cent[j]), "share": round(float(share[j]), 3)} for j in np.argsort(-share) if share[j] >= 0.01]
    merged: list[dict] = []                                      # near-duplicates (ΔRGB < 18) are one colour
    for c in out:
        rgb = np.array([int(c["hex"][i:i + 2], 16) for i in (1, 3, 5)])
        hit = next((m for m in merged if np.abs(np.array([int(m["hex"][i:i + 2], 16) for i in (1, 3, 5)]) - rgb).max() < 18), None)
        if hit:
            hit["share"] = round(hit["share"] + c["share"], 3)
        else:
            merged.append(dict(c))
    return merged


def background(fr: np.ndarray) -> str:
    """The most common colour of the frame border (quantised to 8 levels per channel), averaged inside that bin."""
    border = np.concatenate([fr[:, :2].reshape(-1, 3), fr[:, -2:].reshape(-1, 3), fr[:2].reshape(-1, 3), fr[-2:].reshape(-1, 3)]).astype(np.int32)
    q = border // 32
    key = q[:, 0] * 64 + q[:, 1] * 8 + q[:, 2]
    top = np.bincount(key).argmax()
    return hexof(border[key == top].mean(0))


# ───────────────────────── motion ─────────────────────────
def _gray(f: np.ndarray) -> np.ndarray:
    return (f[..., 0] * 0.299 + f[..., 1] * 0.587 + f[..., 2] * 0.114).astype(np.float32)


def shift(a: np.ndarray, b: np.ndarray) -> tuple[float, float, float]:
    """Global translation b relative to a by phase correlation: (dx, dy) in pixels and the peak's confidence."""
    A, B = np.fft.fft2(a - a.mean()), np.fft.fft2(b - b.mean())
    R = A * np.conj(B); R /= np.abs(R) + 1e-9
    c = np.abs(np.fft.ifft2(R))
    y, x = np.unravel_index(np.argmax(c), c.shape)
    h, w = a.shape
    dy, dx = (y if y <= h // 2 else y - h), (x if x <= w // 2 else x - w)
    return -float(dx), -float(dy), float(c.max() / (c.mean() + 1e-9))


def _hist(f: np.ndarray) -> np.ndarray:
    q = (f // 32).reshape(-1, 3).astype(np.int32)
    h = np.bincount(q[:, 0] * 64 + q[:, 1] * 8 + q[:, 2], minlength=512).astype(np.float32)
    return h / h.sum()


def soft_changes(frames: np.ndarray, fps: float, win: float = 0.5, thresh: float = 0.6, gap: float = 1.0) -> list[float]:
    """Scene changes that are not hard cuts (dissolves, dips, wipes): the colour histogram before vs after a moment
    differs a lot (L1 distance in [0, 2]); the local peaks, at least `gap` s apart."""
    k = max(1, int(win * fps)); n = len(frames)
    if n < 2 * k + 2:
        return []
    H = np.stack([_hist(f) for f in frames])
    d = np.zeros(n)
    for i in range(k, n - k):
        d[i] = np.abs(H[max(0, i - k):i].mean(0) - H[i:i + k].mean(0)).sum()
    out = []
    for i in range(1, n - 1):
        if d[i] >= thresh and d[i] == d[max(0, i - int(gap * fps)):i + int(gap * fps) + 1].max():
            out.append(round(i / fps, 3))
    return out


def events(diff: np.ndarray, fps: float, gap: float = 0.6) -> list[float]:
    """Element entrances: where on-screen change rises out of a calm stretch (motion graphics are built from these)."""
    if len(diff) < 4:
        return []
    s = np.convolve(diff, np.ones(3) / 3, mode="same")
    floor = 1.2                                              # mean |Δ| on 0–255 grey: codec noise on a still frame stays well under this
    lo, hi = max(np.percentile(s, 40), floor * 0.5), max(np.percentile(s, 75), s.mean() + 0.5 * s.std(), floor)
    out, calm = [], True
    for i, v in enumerate(s):
        if calm and v > hi and i > 0:
            t = (i - 1) / fps
            if not out or t - out[-1] >= gap:
                out.append(round(t, 3))
            calm = False
        elif v < lo:
            calm = True
    return out


def segment(frames: np.ndarray, fps: float, cuts: list[float], duration: float, max_beat: float = 3.0, min_beat: float = 0.5) -> list[dict]:
    """Beats: hard cuts + soft scene changes + element entrances; beats under min_beat join their neighbour; long
    stretches are split at their calmest moments so no beat is longer than max_beat."""
    g = np.stack([_gray(f) for f in frames]) if len(frames) else np.zeros((0, 1, 1))
    diff = np.concatenate([[0.0], np.abs(np.diff(g, axis=0)).mean((1, 2))]) if len(g) > 1 else np.zeros(len(g))
    ev = events(diff, fps)
    scene_marks = []                                         # a soft change starts where its transition starts moving
    for s in soft_changes(frames, fps):
        if any(abs(s - c) < 0.6 for c in cuts):              # the hard cut already marks this change, exactly
            continue
        pre = [e for e in ev if s - 0.7 <= e <= s]
        scene_marks.append(round(pre[0], 3) if pre else s)
    scene_marks = sorted({*[round(c, 3) for c in cuts], *scene_marks})
    ev = [e for e in ev if not any(abs(e - c) < min_beat for c in scene_marks)]
    marks = sorted({m for m in [*scene_marks, *ev] if min_beat <= m <= duration - min_beat})
    edges = [0.0]
    for m in marks:
        if m - edges[-1] >= min_beat:
            edges.append(m)
        elif m in scene_marks and edges[-1] not in scene_marks and len(edges) > 1:
            edges[-1] = m                                   # a scene change wins over an entrance just before it
    edges.append(round(duration, 3))
    segment.scene_edges = set(scene_marks)
    out = []
    for a, b in zip(edges, edges[1:]):
        parts = [a, b]
        while True:
            longest = max(range(len(parts) - 1), key=lambda i: parts[i + 1] - parts[i])
            s, e = parts[longest], parts[longest + 1]
            if e - s <= max_beat:
                break
            i0, i1 = int((s + min_beat) * fps), int((e - min_beat) * fps)
            if i1 <= i0 + 1:
                break
            j = i0 + int(np.argmin(diff[i0:i1]))           # the calmest moment: where a beat settles
            parts.insert(longest + 1, round(j / fps, 3))
        out += [{"t0": round(p, 3), "t1": round(q, 3)} for p, q in zip(parts, parts[1:]) if q - p >= 0.05]
    return out, diff


def transition_in(frames: np.ndarray, diff: np.ndarray, fps: float, t: float, is_cut: bool) -> str:
    """How the beat starting at t is entered: cut / dip to black / dip to white / crossfade / whip / continuous."""
    if t <= 0:
        lum = _gray(frames[0]).mean() if len(frames) else 0
        return "opens from black" if lum < 14 else ("opens from white" if lum > 240 else "opens on the frame")
    i = int(round(t * fps)); w = int(fps * 0.35)
    win = slice(max(0, i - w), min(len(frames), i + w + 1))
    lum = np.array([_gray(f).mean() for f in frames[win]])
    d = diff[win]
    if len(lum) and lum.min() < 12:
        return "dip to black"
    if len(lum) and lum.max() > 243:
        return "flash / dip to white"
    if is_cut:
        spread = (d > 0.35 * (d.max() + 1e-9)).sum()
        if spread >= 3 and d.max() < 40:
            return "crossfade / dissolve"
        return "hard cut" if spread <= 2 else "whip / fast move cut"
    return "continuous (same shot, the motion carries on)"


# ───────────────────────── audio ─────────────────────────
def audio(video: Path, beats: list[dict], transcribe: bool = False) -> dict | None:
    tmp = Path(tempfile.mkdtemp(prefix="kosif_an_"))
    wav = tmp / "a.wav"
    r = subprocess.run([FF, "-y", "-v", "error", "-i", str(video), "-vn", "-ac", "1", "-ar", "22050", str(wav)], capture_output=True)
    if r.returncode or not wav.exists() or wav.stat().st_size < 2000:
        shutil.rmtree(tmp, ignore_errors=True); return None
    import qa
    rep: dict = {}
    try:
        lo = subprocess.run([FF, "-v", "info", "-i", str(video), "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
        import re
        m = re.findall(r"I:\s+(-?[\d.]+) LUFS", lo); p = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", lo)
        rep["lufs"] = float(m[-1]) if m else None; rep["true_peak"] = float(p[-1]) if p else None
    except Exception:  # noqa: BLE001
        pass
    try:
        b = qa.beats(wav)
        rep["bpm"] = b["bpm"]; hits = b["hits"]
        rep["onsets"] = [round(h, 3) for h in hits][:200]
        edges = [bt["t0"] for bt in beats[1:]]
        rep["onsets_on_beat_edges"] = [e for e in edges if any(abs(h - e) <= 0.08 for h in hits)]
        rep["sfx_alignment"] = round(len(rep["onsets_on_beat_edges"]) / len(edges), 2) if edges else None
    except Exception as e:  # noqa: BLE001
        rep["beats_error"] = str(e)[:200]
    x = np.frombuffer(subprocess.run([FF, "-v", "error", "-i", str(wav), "-f", "s16le", "-"], capture_output=True).stdout, np.int16).astype(np.float32) / 32768
    if len(x):
        env = np.sqrt(np.convolve(x * x, np.ones(2205) / 2205, mode="same"))[::2205]
        rep["silent_share"] = round(float((env < 0.003).mean()), 3)
        for bt in beats:
            seg = env[int(bt["t0"] * 10):max(int(bt["t0"] * 10) + 1, int(bt["t1"] * 10))]
            bt["audio_level_db"] = round(float(20 * np.log10(seg.mean() + 1e-6)), 1) if len(seg) else None
    if transcribe:
        try:
            import transcribe as tr
            words = tr.transcribe(wav, model="small", lang=None)
            rep["transcript"] = [{"t": round(w.get("start", 0), 2), "text": w.get("text", w.get("word", ""))} for w in words][:400]
        except Exception as e:  # noqa: BLE001
            rep["transcript_error"] = str(e)[:200]
    shutil.rmtree(tmp, ignore_errors=True)
    return rep


# ───────────────────────── the breakdown ─────────────────────────
def measure(video: Path, max_beat: float = 3.0, transcribe: bool = False) -> tuple[dict, np.ndarray, float, np.ndarray]:
    info = probe(video)
    frames, fps = sample(video)
    if not info["duration"] and len(frames):                 # browser-recorded WebM carries no duration in its header
        info["duration"] = round(len(frames) / fps, 3)
    try:
        import scenes
        cuts = [s["start"] for s in scenes.detect(video)["scenes"][1:]]
    except Exception:  # noqa: BLE001
        cuts = []
    beats, diff = segment(frames, fps, cuts, info["duration"], max_beat)
    soft = soft_changes(frames, fps)
    W = frames.shape[2] if len(frames) else 1
    for k, bt in enumerate(beats):
        i0, i1 = int(bt["t0"] * fps), max(int(bt["t0"] * fps) + 1, int(bt["t1"] * fps))
        fr = frames[i0:i1] if i1 <= len(frames) else frames[i0:]
        if not len(fr):
            fr = frames[-1:]
        bt["i"] = k + 1
        bt["dur"] = round(bt["t1"] - bt["t0"], 3)
        bt["palette"] = palette(fr)
        bt["background"] = background(fr[len(fr) // 2])
        bt["brightness"] = round(float(np.mean([_gray(f).mean() for f in fr])) / 255, 3)
        hsv_s = [(f.max(-1).astype(np.float32) - f.min(-1)) / (f.max(-1).astype(np.float32) + 1e-6) for f in fr]
        bt["saturation"] = round(float(np.mean(hsv_s)), 3)
        bt["motion_energy"] = round(float(diff[i0 + 1:i1].mean()) if i1 - i0 > 1 else 0.0, 2)
        if len(fr) >= 2:
            sh = [shift(_gray(a), _gray(b)) for a, b in zip(fr[:-1], fr[1:])]
            good = [(dx, dy) for dx, dy, c in sh if c > 6]
            dx = float(np.mean([g[0] for g in good])) if good else 0.0; dy = float(np.mean([g[1] for g in good])) if good else 0.0
            vx, vy = dx * fps / W * 100, dy * fps / W * 100          # % of frame width per second
            bt["pan_pct_per_s"] = [round(vx, 1), round(vy, 1)]
            mag = math.hypot(vx, vy)
            bt["camera_guess"] = "static / locked" if mag < 2 else (("pan right" if vx > 0 else "pan left") if abs(vx) >= abs(vy) else ("tilt down" if vy > 0 else "tilt up")) + f" (~{mag:.0f}% of width/s)"
        hard = any(abs(bt["t0"] - c) < 0.06 for c in cuts)
        if hard:
            bt["in"] = transition_in(frames, diff, fps, bt["t0"], True)
        elif bt["t0"] in getattr(segment, "scene_edges", set()) or any(abs(bt["t0"] - c) < 0.2 for c in soft):
            bt["in"] = "scene change: " + transition_in(frames, diff, fps, bt["t0"], True).replace("hard cut", "fast dissolve")
        elif bt["t0"] <= 0:
            bt["in"] = transition_in(frames, diff, fps, 0, False)
        else:
            bt["in"] = "new element enters (same scene)"
        bt["scene_change"] = hard or bt["in"].startswith("scene change") or bt["t0"] <= 0
    ends = [b["t0"] for b in beats]
    rep = {"file": str(video), **info, "beats": beats, "beat_count": len(beats), "hard_cuts": [round(c, 3) for c in cuts], "soft_scene_changes": soft,
           "scenes": sum(1 for b in beats if b["scene_change"]),
           "cuts_per_10s": round(len(cuts) / max(info["duration"], 0.1) * 10, 2),
           "mean_beat_s": round(float(np.mean([b["dur"] for b in beats])), 2) if beats else None,
           "palette": palette(frames[:: max(1, len(frames) // 60)], k=8) if len(frames) else [],
           "motion_energy_mean": round(float(diff.mean()), 2) if len(diff) else 0.0,
           "pace": None, "beat_starts": ends}
    me, cr = rep["motion_energy_mean"], rep["cuts_per_10s"]
    rep["pace"] = "fast" if (cr >= 4 or (rep["mean_beat_s"] or 9) < 1.2) else "medium" if (cr >= 1.5 or me > 6) else "slow / held"
    rep["audio"] = audio(video, beats, transcribe) if info["audio"] else None
    return rep, frames, fps, diff


def stills(video: Path, rep: dict, out: Path) -> None:
    from PIL import Image, ImageDraw
    fdir = out / "frames"; fdir.mkdir(parents=True, exist_ok=True)
    mids = []
    for bt in rep["beats"]:
        span = bt["t1"] - bt["t0"]
        for tag, t in (("a", bt["t0"] + min(0.12, span * 0.15)), ("b", bt["t0"] + span / 2), ("c", max(bt["t0"], bt["t1"] - min(0.12, span * 0.15)))):
            f = fdir / f"b{bt['i']:02d}{tag}_{t:06.2f}.jpg"
            subprocess.run([FF, "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", str(video), "-frames:v", "1", "-q:v", "2", str(f)], check=True)
            bt.setdefault("frames", []).append(f.relative_to(out).as_posix())
            if tag == "b":
                mids.append((bt, f))
    tw = 360
    ims = []
    for bt, f in mids:
        im = Image.open(f).convert("RGB"); im.thumbnail((tw, tw)); c = Image.new("RGB", (tw, im.height + 26), (17, 17, 17))
        c.paste(im, (0, 26)); ImageDraw.Draw(c).text((6, 6), f"beat {bt['i']}  {bt['t0']:.2f}-{bt['t1']:.2f}s  {bt['in']}", fill=(235, 235, 235)); ims.append(c)
    if ims:
        cols = min(4, len(ims)); rows = math.ceil(len(ims) / cols); hh = max(i.height for i in ims)
        sheet = Image.new("RGB", (cols * (tw + 6), rows * (hh + 6)), (8, 8, 8))
        for k, im in enumerate(ims):
            sheet.paste(im, ((k % cols) * (tw + 6), (k // cols) * (hh + 6)))
        sheet.save(out / "overview.jpg", quality=90)
    n = max(1, math.ceil(rep["duration"] * 2 / 8))
    subprocess.run([FF, "-y", "-v", "error", "-i", str(video), "-vf", f"fps=2,scale=240:-2,tile=8x{n}:padding=3:color=0x111111", "-frames:v", "1", str(out / "timeline.jpg")], check=True)


BEAT_FIELDS = ["composition", "camera", "subjects", "text", "typography", "icons_ui", "lighting_texture", "motion", "transition_out", "audio"]


def brief(rep: dict) -> dict:
    """What Claude fills after looking at the frames — every field required; measured values are prefilled as hints."""
    return {"source": rep["file"], "duration": rep["duration"], "size": f"{rep['width']}x{rep['height']}", "aspect": rep["aspect"], "fps": rep["fps"],
            "style_line": "", "pace": rep["pace"], "recurring_motif": "", "typography_lock": "", "sound_line": "", "final_frame": "",
            "beats": [{"i": b["i"], "t0": b["t0"], "t1": b["t1"], "measured": {"palette": [c["hex"] for c in b["palette"][:5]], "background": b["background"],
                                                                                   "camera_guess": b.get("camera_guess"), "in": b["in"], "energy": b["motion_energy"]},
                       **{f: "" for f in BEAT_FIELDS}} for b in rep["beats"]]}


def analyze(video: Path, out: Path, max_beat: float = 3.0, transcribe: bool = False) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    rep, *_ = measure(video, max_beat, transcribe)
    stills(video, rep, out)
    (out / "analysis.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    bp = out / "brief.json"
    if not bp.exists():
        bp.write_text(json.dumps(brief(rep), ensure_ascii=False, indent=1), encoding="utf-8")
    return {"out": str(out), "duration": rep["duration"], "size": f"{rep['width']}x{rep['height']}", "fps": rep["fps"], "aspect": rep["aspect"],
            "beats": rep["beat_count"], "scenes": rep["scenes"], "hard_cuts": len(rep["hard_cuts"]), "soft_changes": rep["soft_scene_changes"], "pace": rep["pace"], "palette": [c["hex"] for c in rep["palette"][:6]],
            "audio": {k: (rep["audio"] or {}).get(k) for k in ("lufs", "bpm", "sfx_alignment", "silent_share")} if rep["audio"] else None,
            "next": "read overview.jpg, timeline.jpg and frames/ (every beat), fill brief.json, then `kmotion omniprompt brief.json`"}


def batch(folder: Path, out: Path, max_beat: float = 3.0) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    vids = sorted(p for p in folder.rglob("*") if p.suffix.lower() in VIDEO_EXT and p.is_file())
    lib, rows = [], []
    for k, v in enumerate(vids, 1):
        try:
            rep, *_ = measure(v, max_beat)
        except (Exception, SystemExit) as e:  # noqa: BLE001 — one bad file never stops the library
            rows.append({"file": str(v), "error": str(e)[:160]}); print(f"[{k}/{len(vids)}] {v.name}: skipped ({str(e)[:80]})", flush=True); continue
        a = rep["audio"] or {}
        entry = {"file": str(v), "duration": rep["duration"], "size": f"{rep['width']}x{rep['height']}", "aspect": rep["aspect"], "fps": rep["fps"],
                 "beats": rep["beat_count"], "mean_beat_s": rep["mean_beat_s"], "cuts_per_10s": rep["cuts_per_10s"], "pace": rep["pace"],
                 "motion_energy": rep["motion_energy_mean"], "palette": [c["hex"] for c in rep["palette"][:6]], "lufs": a.get("lufs"), "bpm": a.get("bpm"),
                 "sfx_alignment": a.get("sfx_alignment"), "transitions": sorted({b["in"] for b in rep["beats"][1:]})}
        lib.append(entry); rows.append({k2: (";".join(v2) if isinstance(v2, list) else v2) for k2, v2 in entry.items()})
        print(f"[{k}/{len(vids)}] {v.name}: {rep['pace']}, {rep['beat_count']} beats", flush=True)
    (out / "library.json").write_text(json.dumps({"folder": str(folder), "videos": lib}, ensure_ascii=False, indent=1), encoding="utf-8")
    if rows:
        keys = sorted({k for r in rows for k in r})
        with (out / "library.csv").open("w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(rows)
    paces = [e["pace"] for e in lib]
    return {"videos": len(vids), "analysed": len(lib), "failed": len(vids) - len(lib), "out": str(out),
            "pace": {p: paces.count(p) for p in set(paces)}, "median_beat_s": float(np.median([e["mean_beat_s"] for e in lib if e["mean_beat_s"]])) if lib else None}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video", nargs="?"); ap.add_argument("--out"); ap.add_argument("--max-beat", type=float, default=3.0)
    ap.add_argument("--transcribe", action="store_true"); ap.add_argument("--batch", help="a folder of videos")
    a = ap.parse_args()
    if a.batch:
        res = batch(Path(a.batch), Path(a.out or "style-library"), a.max_beat)
    elif a.video:
        v = Path(a.video)
        res = analyze(v, Path(a.out or f"{v.stem}.breakdown"), a.max_beat, a.transcribe)
    else:
        ap.error("give a VIDEO or --batch FOLDER")
    print(json.dumps(res, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
