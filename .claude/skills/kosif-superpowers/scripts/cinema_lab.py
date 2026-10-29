#!/usr/bin/env python3
"""KOSIF Cinema Lab: cinematography and editing engines for KOSIF Motion, built on FFmpeg + NumPy.

Ideas studied from well-known open-source film tools and rebuilt here in our own code (no code
copied from them; each optional library is used only when it is installed):

  scenes       cut detection like PySceneDetect: FFmpeg's scdet score per frame, a threshold and a
               minimum scene length; --engine pyscenedetect uses the real ContentDetector when
               installed. Writes scenes.json, an optional storyboard contact sheet (Storyboarder
               idea) and OpenTimelineIO / CMX3600 EDL timelines.
  silence-cut  Auto-Editor's core idea: find silences, keep the speech with a margin, snap every cut
               to the frame grid so audio and video stay in sync, render one clean file.
  timeline     any segment plan -> OpenTimelineIO (.otio JSON, read back with the opentimelineio
               package when installed) and a CMX3600 EDL that Kdenlive, Shotcut, Resolve and
               Premiere import.
  grade        OpenColorIO-style colour step: builds portable 33^3 .cube LUTs for named looks (or
               takes yours), applies them with lut3d (tetrahedral) and measures the frame before
               and after. The .cube opens in Resolve, Natron, Kdenlive and OCIO FileTransform.
  stabilize    two-pass vid.stab (deshake fallback); the receipt measures the mean frame-to-frame
               shift (phase correlation) before and after.
  reframe      OpenCV-style tracking for vertical video: follows motion and detail across a wide
               shot, smooths the path like a camera operator (median, two-way ease, speed cap) and
               crops 16:9 to 9:16.
  camera       Motion Canvas / Remotion idea of a programmed camera: push-in, pull-out, pans, tilts
               and ken-burns with ease-in-out on a still or a clip, rendered supersampled.
  review       OpenRV idea of shot review: A/B side-by-side or wipe with labels and burnt-in
               timecode, plus SSIM/PSNR between the two.

Delivery defaults follow the repo's export spec: 1080x1920 for vertical outputs, 30 fps, H.264
CRF 17, yuv420p, +faststart, and the audio stream copied whenever timing is unchanged.
All of it comes from export_profile.py (playbooks/export-standard.md), so it never drifts from the standard. Sources are
never modified, an existing output is kept unless --force, and every command prints a JSON receipt.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
import export_profile as xp  # noqa: E402  (the owner's approved delivery settings)

SCHEMA = "kosif.cinema_lab.receipt.v1"
PLAN_SCHEMA = "kosif.segments.v1"
TIMEOUT = 3600
FPS = xp.FPS
CRF = xp.CRF
VERTICAL = (xp.WIDTH, xp.HEIGHT)
LOOKS = ("teal-orange", "bleach-bypass", "warm-film", "cool-night", "noir", "golden-hour")
MOVES = ("push-in", "pull-out", "pan-left", "pan-right", "tilt-up", "tilt-down", "ken-burns")
FONT_CANDIDATES = ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                   "/usr/share/fonts/dejavu/DejaVuSans.ttf",
                   "/System/Library/Fonts/Supplemental/Arial.ttf",
                   "C:/Windows/Fonts/arial.ttf")


# ---------------------------------------------------------------- helpers

def run(cmd, timeout=TIMEOUT, cwd=None):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                          stdin=subprocess.DEVNULL, timeout=timeout, cwd=cwd)


def need(binary):
    path = shutil.which(binary)
    if not path:
        raise SystemExit(f"{binary} not found on PATH")
    return path


def ff(args, timeout=TIMEOUT, cwd=None):
    p = run([need("ffmpeg"), "-hide_banner", "-nostdin", *args], timeout, cwd)
    if p.returncode:
        raise RuntimeError("ffmpeg failed: " + p.stderr.strip()[-600:])
    return p


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def probe(path):
    p = run([need("ffprobe"), "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)], 120)
    if p.returncode:
        raise ValueError(f"ffprobe could not read {path}: {p.stderr.strip()[-200:]}")
    return json.loads(p.stdout)


def video_stream(info):
    return next((s for s in info.get("streams", []) if s.get("codec_type") == "video"), None)


def audio_stream(info):
    return next((s for s in info.get("streams", []) if s.get("codec_type") == "audio"), None)


def duration_of(info):
    d = info.get("format", {}).get("duration")
    return float(d) if d not in (None, "N/A") else 0.0


def media_summary(path):
    info = probe(path)
    v, a = video_stream(info), audio_stream(info)
    out = {"path": str(path), "duration": round(duration_of(info), 3), "bytes": Path(path).stat().st_size}
    if v:
        rate = v.get("avg_frame_rate") or v.get("r_frame_rate") or "0/1"
        num, _, den = rate.partition("/")
        fps = float(num) / float(den or 1) if float(den or 1) else 0.0
        out.update(width=v.get("width"), height=v.get("height"), fps=round(fps, 3), vcodec=v.get("codec_name"))
    if a:
        out.update(acodec=a.get("codec_name"), sample_rate=int(a.get("sample_rate", 0) or 0))
    return out


def check_paths(src, out, force):
    src, out = Path(src), Path(out)
    if not src.is_file():
        raise SystemExit(f"input not found: {src}")
    if out.exists() and not force:
        raise SystemExit(f"output exists (use --force to replace): {out}")
    if src.resolve() == out.resolve():
        raise SystemExit("output must differ from the input; sources are never modified")
    out.parent.mkdir(parents=True, exist_ok=True)
    return src, out


def even(n):
    n = int(round(n))
    return n - (n % 2)


def parse_size(text, src_w=None, src_h=None):
    if text in (None, "keep"):
        return (even(src_w), even(src_h)) if src_w and src_h else None
    m = re.fullmatch(r"(\d{2,4})x(\d{2,4})", str(text))
    if not m:
        raise SystemExit(f"--size must be WxH or keep, got {text!r}")
    w, h = int(m.group(1)), int(m.group(2))
    if w % 2 or h % 2:
        raise SystemExit("--size needs even numbers")
    return w, h


def encode_args(crf=CRF, fps=FPS):
    """Delivery video settings from export_profile.py (H.264 High, CRF 17, slow, BT.709, faststart)."""
    return [*xp.video_args(crf=crf, fps=fps), *xp.FASTSTART]


def audio_copy_args(info):
    """Copy the user's audio byte for byte when MP4 can hold it, else the AAC 320k/48 kHz floor."""
    a = audio_stream(info)
    if not a:
        return []
    if a.get("codec_name") in xp.MP4_COPY_AUDIO:
        return ["-map", "0:a:0", "-c:a", "copy"]
    return ["-map", "0:a:0", *xp.AAC_FALLBACK]


def font_file():
    for f in FONT_CANDIDATES:
        if Path(f).is_file():
            return f
    p = run(["fc-match", "-f", "%{file}", "sans"], 10) if shutil.which("fc-match") else None
    return p.stdout.strip() if p and p.returncode == 0 and p.stdout.strip() else None


def dt_escape(text):
    return str(text).replace("\\", "\\\\").replace(":", "\\:").replace("'", "\u2019").replace("%", "\\%")


def fmt_time(t):
    m, s = divmod(max(0.0, t), 60)
    return f"{int(m):02d}:{s:05.2f}"


def receipt(cmd, **fields):
    data = {"schema": SCHEMA, "command": cmd, **fields}
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return data


def finish(out, extra=None):
    res = {"output": media_summary(out), "sha256": sha256(out)}
    res.update(extra or {})
    return res


# ---------------------------------------------------------------- frame sampling (NumPy)

def gray_frames(path, fps=6.0, width=160, max_frames=4000):
    """Low-res grayscale frames as a float32 array [n, h, w] plus their times."""
    import numpy as np
    info = probe(path)
    v = video_stream(info)
    if not v:
        raise ValueError("no video stream")
    sw, sh = int(v["width"]), int(v["height"])
    h = max(2, even(width * sh / sw))
    p = subprocess.run([need("ffmpeg"), "-v", "error", "-nostdin", "-i", str(path), "-vf",
                        f"fps={fps},scale={width}:{h}:flags=area,format=gray", "-frames:v", str(max_frames),
                        "-f", "rawvideo", "-"], capture_output=True, timeout=TIMEOUT)
    if p.returncode:
        raise RuntimeError("frame sampling failed: " + p.stderr.decode("utf-8", "replace")[-300:])
    n = len(p.stdout) // (width * h)
    arr = np.frombuffer(p.stdout[: n * width * h], dtype=np.uint8).reshape(n, h, width).astype(np.float32)
    return arr, [i / fps for i in range(n)], (sw, sh)


def phase_shift(a, b):
    """Global translation between two frames by phase correlation (pixels)."""
    import numpy as np
    win = np.outer(np.hanning(a.shape[0]), np.hanning(a.shape[1]))
    fa, fb = np.fft.fft2(a * win), np.fft.fft2(b * win)
    r = fa * np.conj(fb)
    r /= np.abs(r) + 1e-9
    c = np.abs(np.fft.ifft2(r))
    y, x = np.unravel_index(int(np.argmax(c)), c.shape)
    if y > a.shape[0] // 2:
        y -= a.shape[0]
    if x > a.shape[1] // 2:
        x -= a.shape[1]
    return float(math.hypot(x, y))


def jitter(path, fps=15.0):
    """Mean and 95th-percentile frame-to-frame shift at 160 px width."""
    import numpy as np
    frames, _, _ = gray_frames(path, fps=fps, width=160, max_frames=900)
    if len(frames) < 3:
        return {"mean_shift_px": 0.0, "p95_shift_px": 0.0, "frames": int(len(frames))}
    s = np.array([phase_shift(frames[i], frames[i + 1]) for i in range(len(frames) - 1)])
    return {"mean_shift_px": round(float(s.mean()), 3), "p95_shift_px": round(float(np.percentile(s, 95)), 3),
            "frames": int(len(frames)), "at_width": 160}


def frame_stats(path, at=None):
    """Mean luma, mean saturation and mean R,G,B of one frame (rgb24, 256 px wide)."""
    import numpy as np
    info = probe(path)
    t = at if at is not None else duration_of(info) / 2
    v = video_stream(info)
    w = 256
    h = max(2, even(w * int(v["height"]) / int(v["width"])))
    p = subprocess.run([need("ffmpeg"), "-v", "error", "-nostdin", "-ss", f"{t:.3f}", "-i", str(path), "-frames:v", "1",
                        "-vf", f"scale={w}:{h},format=rgb24", "-f", "rawvideo", "-"], capture_output=True, timeout=120)
    if p.returncode or len(p.stdout) < w * h * 3:
        return None
    rgb = np.frombuffer(p.stdout[: w * h * 3], dtype=np.uint8).reshape(h, w, 3).astype(np.float32) / 255
    mx, mn = rgb.max(axis=2), rgb.min(axis=2)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    luma = rgb @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
    return {"t": round(t, 3), "luma": round(float(luma.mean()) * 255, 2), "saturation": round(float(sat.mean()), 4),
            "rgb": [round(float(x) * 255, 2) for x in rgb.reshape(-1, 3).mean(axis=0)]}


# ---------------------------------------------------------------- segment plans and timelines

def normalize_plan(plan):
    if not isinstance(plan, dict) or plan.get("schema") != PLAN_SCHEMA:
        raise ValueError(f"plan must be a {PLAN_SCHEMA} object")
    fps = plan.get("fps", FPS)
    if not isinstance(fps, (int, float)) or not 1 <= fps <= 240:
        raise ValueError("fps must be within 1..240")
    segs = plan.get("segments")
    if not isinstance(segs, list) or not segs:
        raise ValueError("segments must be a nonempty list")
    last = -1.0
    for i, s in enumerate(segs):
        a, b = float(s["start"]), float(s["end"])
        if not (math.isfinite(a) and math.isfinite(b) and 0 <= a < b):
            raise ValueError(f"segment {i} has an invalid range")
        if a < last - 1e-6:
            raise ValueError("segments must be in order and not overlap")
        last = b
    return plan


def tc(frames, fps):
    fps_i = int(round(fps))
    f = int(frames)
    return f"{f // (3600 * fps_i):02d}:{f // (60 * fps_i) % 60:02d}:{f // fps_i % 60:02d}:{f % fps_i:02d}"


def rt(value, rate):
    return {"OTIO_SCHEMA": "RationalTime.1", "rate": float(rate), "value": float(value)}


def to_otio(plan, name="KOSIF timeline"):
    """Write an OpenTimelineIO JSON document without needing the package."""
    plan = normalize_plan(plan)
    fps = float(plan.get("fps", FPS))
    src = Path(plan["source"]).resolve()
    url = src.as_uri()

    def clip(i, s):
        a = round(float(s["start"]) * fps)
        d = max(1, round(float(s["end"]) * fps) - a)
        return {"OTIO_SCHEMA": "Clip.2", "metadata": {"kosif": {"label": s.get("label", "")}},
                "name": s.get("label") or f"{src.stem}_{i + 1:03d}",
                "source_range": {"OTIO_SCHEMA": "TimeRange.1", "start_time": rt(a, fps), "duration": rt(d, fps)},
                "effects": [], "markers": [], "enabled": True,
                "media_references": {"DEFAULT_MEDIA": {"OTIO_SCHEMA": "ExternalReference.1", "metadata": {},
                                                       "name": src.name, "available_range": None,
                                                       "available_image_bounds": None, "target_url": url}},
                "active_media_reference_key": "DEFAULT_MEDIA"}

    def track(kind, label):
        return {"OTIO_SCHEMA": "Track.1", "metadata": {}, "name": label, "source_range": None, "effects": [],
                "markers": [], "enabled": True, "kind": kind,
                "children": [clip(i, s) for i, s in enumerate(plan["segments"])]}

    tracks = [track("Video", "V1")]
    if plan.get("has_audio", True):
        tracks.append(track("Audio", "A1"))
    return {"OTIO_SCHEMA": "Timeline.1", "metadata": {"kosif": {"schema": PLAN_SCHEMA, "made_by": "cinema_lab.py"}},
            "name": name, "global_start_time": rt(0, fps),
            "tracks": {"OTIO_SCHEMA": "Stack.1", "metadata": {}, "name": "tracks", "source_range": None,
                       "effects": [], "markers": [], "enabled": True, "children": tracks}}


def to_edl(plan, title="KOSIF"):
    """CMX3600 EDL: one cut event per segment, record side butted end to end."""
    plan = normalize_plan(plan)
    fps = float(plan.get("fps", FPS))
    reel = re.sub(r"[^A-Za-z0-9]", "", Path(plan["source"]).stem)[:8].upper() or "AX"
    lines = [f"TITLE: {title}", "FCM: NON-DROP FRAME", ""]
    rec = 0
    for i, s in enumerate(plan["segments"], 1):
        a = round(float(s["start"]) * fps)
        b = max(a + 1, round(float(s["end"]) * fps))
        lines.append(f"{i:03d}  {reel:<8} AA/V  C        {tc(a, fps)} {tc(b, fps)} {tc(rec, fps)} {tc(rec + b - a, fps)}")
        lines.append(f"* FROM CLIP NAME: {Path(plan['source']).name}")
        if s.get("label"):
            lines.append(f"* COMMENT: {s['label']}")
        lines.append("")
        rec += b - a
    return "\n".join(lines)


def write_timelines(plan, base):
    base = Path(base)
    otio_path, edl_path = base.with_suffix(".otio"), base.with_suffix(".edl")
    otio_path.write_text(json.dumps(to_otio(plan, base.stem), indent=2), encoding="utf-8")
    edl_path.write_text(to_edl(plan, base.stem), encoding="utf-8")
    res = {"otio": str(otio_path), "edl": str(edl_path), "otio_readback": "opentimelineio not installed"}
    try:
        import opentimelineio as otio  # optional
        tl = otio.adapters.read_from_file(str(otio_path))
        res["otio_readback"] = {"ok": True, "tracks": len(tl.tracks), "clips": len(list(tl.find_clips())),
                                "duration_s": round(tl.duration().to_seconds(), 3), "version": otio.__version__}
    except ImportError:
        pass
    except Exception as exc:  # report, never hide
        res["otio_readback"] = {"ok": False, "error": str(exc)[:200]}
    return res


# ---------------------------------------------------------------- scenes (PySceneDetect idea)

def scdet_scores(path):
    p = ff(["-v", "error", "-i", str(path), "-map", "0:v:0", "-vf", "scdet=threshold=100,metadata=mode=print:file=-",
            "-f", "null", "-"])
    times, scores, t = [], [], None
    for line in p.stdout.splitlines():
        m = re.search(r"pts_time:([0-9.eE+-]+)", line)
        if m:
            t = float(m.group(1))
            continue
        m = re.match(r"lavfi\.scd\.score=([0-9.]+)", line.strip())
        if m and t is not None:
            times.append(t)
            scores.append(float(m.group(1)))
    return times, scores


def pick_cuts(times, scores, threshold, min_len):
    cuts, last = [], 0.0
    for t, s in zip(times, scores):
        if s >= threshold and t - last >= min_len and t > 0:
            cuts.append(t)
            last = t
    return cuts


def cuts_to_segments(cuts, duration):
    edges = [0.0, *[c for c in cuts if 0 < c < duration], duration]
    return [{"start": round(a, 3), "end": round(b, 3), "label": f"scene {i + 1}"}
            for i, (a, b) in enumerate(zip(edges, edges[1:])) if b - a > 1e-3]


def contact_sheet(src, segments, out, cols=4, thumb_w=320):
    font = font_file()
    tmp = Path(tempfile.mkdtemp(prefix="kosif_sheet_"))
    try:
        for i, s in enumerate(segments):
            mid = (s["start"] + s["end"]) / 2
            vf = f"scale={thumb_w}:-2"
            if font:
                label = dt_escape(f"#{i + 1}  {fmt_time(s['start'])}-{fmt_time(s['end'])}")
                vf += (f",drawtext=fontfile='{font}':text='{label}':x=8:y=h-th-8:fontsize=18:fontcolor=white:"
                       "box=1:boxcolor=black@0.6:boxborderw=6")
            ff(["-v", "error", "-ss", f"{mid:.3f}", "-i", str(src), "-frames:v", "1", "-vf", vf, "-y",
                str(tmp / f"t{i:04d}.png")], 120)
        rows = math.ceil(len(segments) / cols)
        th = max(2, even(thumb_w * 9 / 16))
        ff(["-v", "error", "-framerate", "1", "-i", str(tmp / "t%04d.png"), "-vf",
            f"scale={thumb_w}:{th}:force_original_aspect_ratio=decrease,pad={thumb_w}:{th}:(ow-iw)/2:(oh-ih)/2,"
            f"tile={cols}x{rows}:padding=4:margin=4:color=0x111111", "-frames:v", "1", "-y", str(out)], 300)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return str(out)


def cmd_scenes(a):
    src = Path(a.input)
    if not src.is_file():
        raise SystemExit(f"input not found: {src}")
    info = media_summary(src)
    out_dir = Path(a.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    engine = a.engine
    if engine == "auto":
        try:
            import scenedetect  # noqa: F401
            engine = "pyscenedetect"
        except ImportError:
            engine = "ffmpeg"
    detail = {}
    if engine == "pyscenedetect":
        from scenedetect import detect, ContentDetector
        fps = info.get("fps") or FPS
        found = detect(str(src), ContentDetector(threshold=a.threshold if a.threshold is not None else 27.0,
                                                  min_scene_len=max(1, round(a.min_scene * fps))))
        cuts = [round(float(s.seconds if hasattr(s, "seconds") else s.get_seconds()), 3) for s, _ in found][1:]
        import scenedetect as _sd
        detail = {"engine": "pyscenedetect", "version": _sd.__version__, "detector": "ContentDetector"}
    else:
        thr = a.threshold if a.threshold is not None else 6.0
        times, scores = scdet_scores(src)
        cuts = [round(c, 3) for c in pick_cuts(times, scores, thr, a.min_scene)]
        top = sorted(zip(scores, times), reverse=True)[:5]
        detail = {"engine": "ffmpeg-scdet", "threshold": thr, "frames_scored": len(scores),
                  "top_scores": [{"t": round(t, 3), "score": round(s, 2)} for s, t in top]}
    segs = cuts_to_segments(cuts, info["duration"])
    plan = {"schema": PLAN_SCHEMA, "source": str(src.resolve()), "fps": info.get("fps") or FPS,
            "has_audio": "acodec" in info, "kind": "scenes", "segments": segs}
    (out_dir / "scenes.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    extra = {}
    if a.sheet:
        extra["sheet"] = contact_sheet(src, segs, out_dir / "storyboard.jpg", cols=a.cols)
    if a.timeline:
        extra["timeline"] = write_timelines(plan, out_dir / "scenes")
    return receipt("scenes", input=info, detection=detail, cuts=cuts, scenes=len(segs),
                   plan=str(out_dir / "scenes.json"), **extra)


# ---------------------------------------------------------------- silence-cut (Auto-Editor idea)

def silences(path, noise_db, min_silence):
    p = ff(["-v", "info", "-i", str(path), "-map", "0:a:0", "-af", f"silencedetect=noise={noise_db}dB:d={min_silence}",
            "-f", "null", "-"])
    out, start = [], None
    for line in p.stderr.splitlines():
        m = re.search(r"silence_start: ([0-9.eE+-]+)", line)
        if m:
            start = max(0.0, float(m.group(1)))
        m = re.search(r"silence_end: ([0-9.eE+-]+)", line)
        if m and start is not None:
            out.append((start, float(m.group(1))))
            start = None
    if start is not None:
        out.append((start, float("inf")))
    return out


def keep_segments(silent, duration, margin=0.12, min_keep=0.2, fps=FPS):
    """Speech = complement of silence, padded by margin, merged, snapped to the frame grid."""
    keeps, cur = [], 0.0
    for a, b in silent:
        if a > cur:
            keeps.append([cur, a])
        cur = max(cur, b)
    if cur < duration:
        keeps.append([cur, duration])
    padded = []
    for a, b in keeps:
        a, b = max(0.0, a - margin), min(duration, b + margin)
        if padded and a <= padded[-1][1]:
            padded[-1][1] = max(padded[-1][1], b)
        else:
            padded.append([a, b])
    snapped = []
    for a, b in padded:
        fa, fb = math.floor(a * fps + 1e-6), math.ceil(b * fps - 1e-6)
        fb = min(fb, math.floor(duration * fps + 1e-6))
        if (fb - fa) / fps >= min_keep:
            if snapped and fa <= snapped[-1][1]:
                snapped[-1][1] = max(snapped[-1][1], fb)
            else:
                snapped.append([fa, fb])
    return [{"start": round(fa / fps, 4), "end": round(fb / fps, 4), "label": f"keep {i + 1}"}
            for i, (fa, fb) in enumerate(snapped)]


def cut_graph(segs, size=None):
    """trim/atrim + concat graph that keeps only `segs` (frame-snapped). Unlike select/aselect expressions it cuts the
    same way on every FFmpeg version: on FFmpeg 8.0.1 (the CI runner from 29-10-2026) the select graph passed every
    frame through. With size, the video is normalised (fps, fit, pad) before the cut; without it the graph is audio only."""
    n = len(segs)
    parts = []
    if size:
        parts.append(f"[0:v:0]fps={FPS},scale={size[0]}:{size[1]}:force_original_aspect_ratio=decrease,"
                     f"pad={size[0]}:{size[1]}:(ow-iw)/2:(oh-ih)/2,setsar=1,split={n}" + "".join(f"[vs{i}]" for i in range(n)))
    parts.append(f"[0:a:0]aresample=48000,asplit={n}" + "".join(f"[as{i}]" for i in range(n)))
    for i, s in enumerate(segs):
        if size:
            parts.append(f"[vs{i}]trim=start={s['start']:.4f}:end={s['end']:.4f},setpts=PTS-STARTPTS[v{i}]")
        parts.append(f"[as{i}]atrim=start={s['start']:.4f}:end={s['end']:.4f},asetpts=PTS-STARTPTS[a{i}]")
    ins = "".join(f"[v{i}][a{i}]" if size else f"[a{i}]" for i in range(n))
    parts.append(f"{ins}concat=n={n}:v={1 if size else 0}:a=1" + ("[v][a]" if size else "[a]"))
    return ";".join(parts)


def cmd_silence_cut(a):
    src, out = check_paths(a.input, a.output, a.force)
    info = probe(src)
    if not audio_stream(info):
        raise SystemExit("silence-cut needs an audio stream")
    dur = duration_of(info)
    silent = silences(src, a.noise, a.min_silence)
    segs = keep_segments(silent, dur, a.margin, a.min_keep, FPS)
    if not segs:
        raise SystemExit("everything is silent at this threshold; try a lower --noise (e.g. -45)")
    if len(segs) > 600:
        raise SystemExit(f"{len(segs)} segments is too many; raise --min-silence")
    plan = {"schema": PLAN_SCHEMA, "source": str(src.resolve()), "fps": FPS, "has_audio": True,
            "kind": "silence-cut", "segments": segs}
    plan_path = out.with_suffix(".plan.json")
    plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    kept = sum(s["end"] - s["start"] for s in segs)
    extra = {}
    if a.timeline:
        extra["timeline"] = write_timelines(plan, out.with_suffix(""))
    if a.plan_only:
        return receipt("silence-cut", input=media_summary(src), silences=len(silent), segments=len(segs),
                       kept_s=round(kept, 3), removed_s=round(dur - kept, 3), plan=str(plan_path), rendered=False, **extra)
    fd, name = tempfile.mkstemp(prefix="kosif_sc_", suffix=".txt")
    os.close(fd)                             # the graph is written by path below; do not leak the descriptor
    script = Path(name)
    v = video_stream(info)
    try:
        if v:
            size = parse_size(a.size, v.get("width"), v.get("height"))
            script.write_text(cut_graph(segs, size), encoding="utf-8")
            ff(["-v", "error", "-i", str(src), "-filter_complex_script", str(script), "-map", "[v]", "-map", "[a]",
                *encode_args(), *xp.AAC_FALLBACK, "-y", str(out)])
        else:
            script.write_text(cut_graph(segs), encoding="utf-8")
            ff(["-v", "error", "-i", str(src), "-filter_complex_script", str(script), "-map", "[a]",
                *xp.AAC_FALLBACK, "-y", str(out)])
    finally:
        script.unlink(missing_ok=True)
    oi = probe(out)
    vs, as_ = video_stream(oi), audio_stream(oi)
    sync = None
    if vs and as_ and vs.get("duration") and as_.get("duration"):
        sync = round(float(vs["duration"]) - float(as_["duration"]), 4)
    return receipt("silence-cut", input=media_summary(src), silences=len(silent), segments=len(segs),
                   kept_s=round(kept, 3), removed_s=round(dur - kept, 3), plan=str(plan_path), rendered=True,
                   av_duration_gap_s=sync, audio_note="audio re-encoded to AAC 320k/48 kHz (export standard floor) because cutting changes timing",
                   **finish(out), **extra)


# ---------------------------------------------------------------- timeline export

def cmd_timeline(a):
    plan = json.loads(Path(a.plan).read_text(encoding="utf-8"))
    normalize_plan(plan)
    res = write_timelines(plan, Path(a.out))
    return receipt("timeline", plan=a.plan, segments=len(plan["segments"]), **res)


# ---------------------------------------------------------------- grade (OpenColorIO idea)

def _look(name, rgb):
    import numpy as np
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    luma = 0.2126 * r + 0.7152 * g + 0.0722 * b

    def s_curve(x, k):
        return np.clip(x + k * (x - 0.5) * (1 - np.abs(2 * x - 1)), 0, 1)

    def mix(x, y, t):
        return x * (1 - t) + y * t

    if name == "teal-orange":
        sh = np.clip(1 - luma * 2, 0, 1)[..., None]
        hi = np.clip(luma * 2 - 1, 0, 1)[..., None]
        out = rgb + sh * np.array([-0.06, 0.02, 0.07]) + hi * np.array([0.07, 0.02, -0.06])
        out = s_curve(np.clip(out, 0, 1), 0.25)
    elif name == "bleach-bypass":
        out = s_curve(mix(rgb, luma[..., None], 0.55), 0.45)
    elif name == "warm-film":
        out = rgb * np.array([1.06, 1.0, 0.9])
        out = 0.035 + 0.94 * out
        out = (1 - np.exp(-2.2 * out)) / (1 - math.exp(-2.2))  # soft highlight roll-off
        out = s_curve(np.clip(out, 0, 1), 0.12)
    elif name == "cool-night":
        out = rgb * np.array([0.82, 0.92, 1.1]) * 0.88
        out = s_curve(np.clip(mix(out, (luma * 0.88)[..., None] * np.array([0.8, 0.9, 1.1]), 0.35), 0, 1), 0.2)
    elif name == "noir":
        out = s_curve(np.repeat(luma[..., None], 3, axis=-1), 0.6)
    elif name == "golden-hour":
        hi = np.clip(luma, 0, 1)[..., None]
        out = rgb * np.array([1.08, 1.02, 0.86]) + hi * np.array([0.04, 0.02, -0.03])
        out = s_curve(np.clip(out, 0, 1), 0.1)
    else:
        raise SystemExit(f"unknown look {name!r}; choose from {', '.join(LOOKS)}")
    return np.clip(out, 0, 1)


def make_cube(name, strength=1.0, size=33):
    import numpy as np
    if not 0 <= strength <= 1:
        raise SystemExit("--strength must be within 0..1")
    axis = np.linspace(0, 1, size, dtype=np.float64)
    b, g, r = np.meshgrid(axis, axis, axis, indexing="ij")  # red changes fastest in .cube order
    ident = np.stack([r, g, b], axis=-1).reshape(-1, 3)
    graded = _look(name, ident)
    out = ident * (1 - strength) + graded * strength
    lines = [f'TITLE "KOSIF {name} {strength:.2f}"', f"LUT_3D_SIZE {size}", "DOMAIN_MIN 0 0 0", "DOMAIN_MAX 1 1 1"]
    lines += [f"{x:.6f} {y:.6f} {z:.6f}" for x, y, z in out]
    return "\n".join(lines) + "\n"


def read_cube_size(path):
    size, rows = None, 0
    for line in Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
        s = line.strip()
        if s.startswith("LUT_3D_SIZE"):
            size = int(s.split()[1])
        elif s and (s[0].isdigit() or s[0] in "-."):
            rows += 1
    if not size or rows != size ** 3:
        raise SystemExit(f"not a valid 3D .cube LUT (size {size}, {rows} rows)")
    return size


def cmd_grade(a):
    if a.cube_out and not a.input:
        Path(a.cube_out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.cube_out).write_text(make_cube(a.look, a.strength), encoding="utf-8")
        return receipt("grade", look=a.look, strength=a.strength, cube=a.cube_out, size=33,
                       sha256=sha256(a.cube_out), rendered=False)
    if not (a.input and a.output):
        raise SystemExit("grade needs --input and --output (or only --cube-out to export a LUT)")
    src, out = check_paths(a.input, a.output, a.force)
    info = probe(src)
    v = video_stream(info)
    if not v:
        raise SystemExit("grade needs a video stream")
    tmp = Path(tempfile.mkdtemp(prefix="kosif_lut_"))
    try:
        if a.lut:
            read_cube_size(a.lut)
            shutil.copy(a.lut, tmp / "look.cube")
            look = {"lut": str(a.lut)}
        else:
            (tmp / "look.cube").write_text(make_cube(a.look, a.strength), encoding="utf-8")
            look = {"look": a.look, "strength": a.strength}
        if a.cube_out:
            shutil.copy(tmp / "look.cube", a.cube_out)
            look["cube"] = a.cube_out
        size = parse_size(a.size, v.get("width"), v.get("height"))
        vf = (f"lut3d=file=look.cube:interp=tetrahedral,scale={size[0]}:{size[1]}:force_original_aspect_ratio=decrease,"
              f"pad={size[0]}:{size[1]}:(ow-iw)/2:(oh-ih)/2,setsar=1")
        ff(["-v", "error", "-i", str(src.resolve()), "-map", "0:v:0", "-vf", vf, *encode_args(),
            *audio_copy_args(info), "-y", str(out.resolve())], cwd=str(tmp))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    before, after = frame_stats(src), frame_stats(out)
    return receipt("grade", input=media_summary(src), **look, before=before, after=after, **finish(out))


# ---------------------------------------------------------------- stabilize (vid.stab)

def has_filter(name):
    p = run([need("ffmpeg"), "-hide_banner", "-filters"], 30)
    return bool(re.search(rf"\s{re.escape(name)}\s", p.stdout))


def cmd_stabilize(a):
    src, out = check_paths(a.input, a.output, a.force)
    info = probe(src)
    v = video_stream(info)
    if not v:
        raise SystemExit("stabilize needs a video stream")
    size = parse_size(a.size, v.get("width"), v.get("height"))
    fit = f"scale={size[0]}:{size[1]}:force_original_aspect_ratio=decrease,pad={size[0]}:{size[1]}:(ow-iw)/2:(oh-ih)/2,setsar=1"
    tmp = Path(tempfile.mkdtemp(prefix="kosif_stab_"))
    try:
        if has_filter("vidstabdetect") and not a.deshake:
            engine = "vid.stab two-pass"
            ff(["-v", "error", "-i", str(src.resolve()), "-map", "0:v:0", "-vf",
                f"vidstabdetect=shakiness={a.shakiness}:accuracy=15:result=t.trf", "-f", "null", "-"], cwd=str(tmp))
            vf = (f"vidstabtransform=input=t.trf:smoothing={a.smoothing}:optzoom=1:interpol=bicubic,"
                  f"unsharp=5:5:0.6:3:3:0.3,{fit}")
        else:
            engine = "deshake"
            vf = f"deshake=rx=32:ry=32,{fit}"
        ff(["-v", "error", "-i", str(src.resolve()), "-map", "0:v:0", "-vf", vf, *encode_args(),
            *audio_copy_args(info), "-y", str(out.resolve())], cwd=str(tmp))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return receipt("stabilize", engine=engine, input=media_summary(src), shake_before=jitter(src),
                   shake_after=jitter(out), **finish(out))


# ---------------------------------------------------------------- reframe (OpenCV tracking idea)

def subject_path(frames, crop_w_small):
    """Best crop-window left edge per frame (small-frame pixels): motion + detail energy, sliding window."""
    import numpy as np
    n, h, w = frames.shape
    gx = np.abs(np.diff(frames, axis=2, prepend=frames[:, :, :1]))
    gy = np.abs(np.diff(frames, axis=1, prepend=frames[:, :1, :]))
    detail = (gx + gy).sum(axis=1)
    motion = np.zeros((n, w), dtype=np.float32)
    if n > 1:
        motion[1:] = np.abs(np.diff(frames, axis=0)).sum(axis=1)
        motion[0] = motion[1]
    def norm(x):
        return x / (x.max(axis=1, keepdims=True) + 1e-6)
    energy = 1.0 * norm(motion) + 0.35 * norm(detail)
    k = int(crop_w_small)
    csum = np.cumsum(np.pad(energy, ((0, 0), (1, 0))), axis=1)
    window = csum[:, k:] - csum[:, :-k] if k < w else csum[:, -1:]
    centre_bias = 1 - 0.15 * np.abs(np.linspace(-1, 1, window.shape[1]))
    best = np.argmax(window * centre_bias, axis=1)
    cols = np.arange(w, dtype=np.float64)
    lefts = np.empty(n, dtype=np.float64)
    for i, b in enumerate(best):  # centre the crop on the energy centroid inside the best window
        e = energy[i, b: b + k].astype(np.float64)
        c = float((e * cols[b: b + k]).sum() / e.sum()) if e.sum() > 1e-6 else b + k / 2
        lefts[i] = min(max(c - k / 2, 0.0), max(0.0, w - k))
    return lefts


def smooth_path(xs, fps, max_speed, alpha=0.25, median=5):
    import numpy as np
    xs = np.asarray(xs, dtype=np.float64)
    if len(xs) == 0:
        return xs
    r = median // 2
    med = np.array([np.median(xs[max(0, i - r): i + r + 1]) for i in range(len(xs))])
    fwd = med.copy()
    for i in range(1, len(fwd)):
        fwd[i] = fwd[i - 1] + alpha * (med[i] - fwd[i - 1])
    both = fwd.copy()
    for i in range(len(both) - 2, -1, -1):
        both[i] = both[i + 1] + alpha * (fwd[i] - both[i + 1])
    step = max_speed / fps
    out = both.copy()
    for i in range(1, len(out)):
        out[i] = out[i - 1] + max(-step, min(step, out[i] - out[i - 1]))
    return out


def cmd_reframe(a):
    import numpy as np
    src, out = check_paths(a.input, a.output, a.force)
    info = probe(src)
    v = video_stream(info)
    if not v:
        raise SystemExit("reframe needs a video stream")
    tw, th = parse_size(a.size)
    sw, sh = int(v["width"]), int(v["height"])
    crop_w = even(min(sw, sh * tw / th))
    crop_h = even(sh) if crop_w < sw - 2 else even(min(sh, crop_w * th / tw))
    if crop_w >= sw - 2:
        xs_src = np.zeros(1)
        path_note = "source already as narrow as the target; centred fit"
        sample_fps = 1.0
        times = [0.0]
    else:
        sample_fps = a.sample_fps
        frames, times, _ = gray_frames(src, fps=sample_fps, width=160)
        scale = 160 / sw
        left = subject_path(frames, max(2, round(crop_w * scale)))
        cuts = []
        if not a.no_cuts:  # a hard cut re-aims the camera at once instead of panning across it
            st, sc = scdet_scores(src)
            cuts = pick_cuts(st, sc, 6.0, 0.6)
        xs_small = np.empty_like(left)
        edges = [0, *sorted({int(round(c * sample_fps)) for c in cuts if 0 < c * sample_fps < len(left)}), len(left)]
        for lo, hi in zip(edges, edges[1:]):
            if hi > lo:  # max_speed is in source widths per second
                xs_small[lo:hi] = smooth_path(left[lo:hi], sample_fps, a.max_speed * 160)
        xs_src = np.clip(xs_small / scale, 0, sw - crop_w)
        path_note = (f"motion + detail tracking, median + two-way ease + speed cap, "
                     f"re-aimed at {len(edges) - 2} scene cuts")
    y = even((sh - crop_h) / 2)
    dur = duration_of(info)
    tmp = Path(tempfile.mkdtemp(prefix="kosif_rf_"))
    try:
        lines = []
        n_out = max(1, int(dur * FPS))
        ts = np.array(times) if len(times) else np.array([0.0])
        for i in range(n_out):
            t = i / FPS
            x = float(np.interp(t, ts, xs_src)) if len(xs_src) > 1 else float(xs_src[0] if crop_w < sw - 2 else 0)
            lines.append(f"{t:.4f} crop x {int(round(x))};")
        (tmp / "cmds.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
        x0 = int(round(float(xs_src[0]))) if crop_w < sw - 2 else 0
        vf = (f"fps={FPS},sendcmd=f=cmds.txt,crop=w={crop_w}:h={crop_h}:x={x0}:y={y},"
              f"scale={tw}:{th}:flags=lanczos,setsar=1")
        ff(["-v", "error", "-i", str(src.resolve()), "-map", "0:v:0", "-vf", vf, *encode_args(),
            *audio_copy_args(info), "-y", str(out.resolve())], cwd=str(tmp))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    travel = float(np.abs(np.diff(xs_src)).sum()) if len(xs_src) > 1 else 0.0
    path_out = Path(str(out) + ".path.json")
    path_out.write_text(json.dumps({"fps": sample_fps, "crop": [crop_w, crop_h], "y": y,
                                    "x": [round(float(x), 1) for x in xs_src]}), encoding="utf-8")
    return receipt("reframe", input=media_summary(src), crop={"w": crop_w, "h": crop_h, "y": y},
                   tracking=path_note, camera_travel_px=round(travel, 1), path=str(path_out), **finish(out))


# ---------------------------------------------------------------- camera (Motion Canvas / Remotion idea)

EASE = "if(lt(P,0.5),4*P*P*P,1-pow(-2*P+2,3)/2)"


def move_exprs(move, zoom):
    """zoompan z, x, y expressions; E is the eased 0..1 progress."""
    cx, cy, z = "0.5", "0.5", f"{zoom}"
    if move == "push-in":
        z = f"1+({zoom}-1)*E"
    elif move == "pull-out":
        z = f"{zoom}-({zoom}-1)*E"
    elif move == "pan-left":
        cx = "1-E"
    elif move == "pan-right":
        cx = "E"
    elif move == "tilt-up":
        cy = "1-E"
    elif move == "tilt-down":
        cy = "E"
    elif move == "ken-burns":
        z = f"1+({zoom}-1)*E"
        cx, cy = "0.35+0.3*E", "0.6-0.2*E"
    else:
        raise SystemExit(f"unknown move {move!r}; choose from {', '.join(MOVES)}")
    return z, f"(iw-iw/zoom)*({cx})", f"(ih-ih/zoom)*({cy})"


def cmd_camera(a):
    src, out = check_paths(a.input, a.output, a.force)
    if not 1.0 < a.zoom <= 3.0:
        raise SystemExit("--zoom must be within 1..3 (exclusive of 1)")
    info = probe(src)
    v = video_stream(info)
    if not v:
        raise SystemExit("camera needs an image or a video")
    tw, th = parse_size(a.size)
    image_codec = v.get("codec_name") in ("png", "mjpeg", "webp", "bmp", "tiff")
    is_still = duration_of(info) <= 0.05 or (image_codec and int(v.get("nb_frames", "1") or 1) <= 1)
    dur = a.duration if is_still else duration_of(info)
    n = max(2, int(round(dur * FPS)))
    k = a.supersample
    z, x, y = move_exprs(a.move, a.zoom)
    prog = f"min(1,on/{n - 1})"
    ease = EASE.replace("P", prog)
    z, x, y = (e.replace("E", f"({ease})") for e in (z, x, y))
    pre = (f"scale={tw * k}:{th * k}:force_original_aspect_ratio=increase:flags=lanczos,crop={tw * k}:{th * k}")
    zp = f"zoompan=z='{z}':x='{x}':y='{y}':d={n if is_still else 1}:s={tw}x{th}:fps={FPS}"
    args = ["-v", "error", "-i", str(src)]
    args += ["-map", "0:v:0", "-vf", f"{'fps=' + str(FPS) + ',' if not is_still else ''}{pre},{zp},setsar=1{',' + xp.RGB_TO_709 if is_still else ''}",
             "-frames:v", str(n), *encode_args()]
    if not is_still:
        args += audio_copy_args(info)
    ff([*args, "-y", str(out)])
    return receipt("camera", move=a.move, zoom=a.zoom, ease="ease-in-out cubic", still=is_still,
                   frames=n, supersample=k, input=media_summary(src), **finish(out))


# ---------------------------------------------------------------- review (OpenRV idea)

def cmd_review(a):
    for p in (a.a, a.b):
        if not Path(p).is_file():
            raise SystemExit(f"input not found: {p}")
    out = Path(a.output)
    if out.exists() and not a.force:
        raise SystemExit(f"output exists (use --force to replace): {out}")
    out.parent.mkdir(parents=True, exist_ok=True)
    ia, ib = probe(a.a), probe(a.b)
    va = video_stream(ia)
    if not va or not video_stream(ib):
        raise SystemExit("review needs two videos")
    h = even(a.height)
    w = even(h * int(va["width"]) / int(va["height"]))
    font = font_file()

    def label(name, right=False):
        if not font:
            return ""
        x = "w-tw-12" if right else "12"
        return (f",drawtext=fontfile='{font}':text='{dt_escape(name)}':x={x}:y=12:fontsize={max(14, h // 22)}:"
                "fontcolor=white:box=1:boxcolor=black@0.55:boxborderw=6")

    tcode = ""
    if font:
        tcode = (f",drawtext=fontfile='{font}':timecode='00\\:00\\:00\\:00':rate={FPS}:x=(w-tw)/2:y=h-th-12:"
                 f"fontsize={max(14, h // 20)}:fontcolor=white:box=1:boxcolor=black@0.6:boxborderw=6")
    base = f"fps={FPS},scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2,setsar=1"
    if a.mode == "side":
        graph = (f"[0:v]{base}{label(a.label_a)}[l];[1:v]{base}{label(a.label_b)}[r];"
                 f"[l][r]hstack=inputs=2{tcode}[v]")
    else:
        half = even(w / 2)
        graph = (f"[0:v]{base}{label(a.label_a)}[l];[1:v]{base}{label(a.label_b, right=True)},crop={w - half}:{h}:{half}:0[r];"
                 f"[l][r]overlay=x={half}:y=0:shortest=1,drawbox=x={half - 1}:y=0:w=2:h={h}:color=white@0.9:t=fill{tcode}[v]")
    ff(["-v", "error", "-i", str(a.a), "-i", str(a.b), "-filter_complex", graph, "-map", "[v]", "-shortest",
        *encode_args(), "-y", str(out)])
    metrics = None
    if a.metrics:
        p = ff(["-v", "info", "-i", str(a.a), "-i", str(a.b), "-filter_complex",
                f"[0:v]{base}[x];[1:v]{base}[y];[x][y]ssim;[0:v]{base}[p];[1:v]{base}[q];[p][q]psnr",
                "-shortest", "-f", "null", "-"])
        ssim = re.search(r"SSIM .*All:([0-9.]+)", p.stderr)
        psnr = re.search(r"PSNR .*average:([0-9.]+|inf)", p.stderr)
        metrics = {"ssim": float(ssim.group(1)) if ssim else None,
                   "psnr_db": (float(psnr.group(1)) if psnr and psnr.group(1) != "inf" else (math.inf if psnr else None))}
        if metrics["psnr_db"] == math.inf:
            metrics["psnr_db"] = "inf"
    return receipt("review", mode=a.mode, a=media_summary(a.a), b=media_summary(a.b), metrics=metrics, **finish(out))


# ---------------------------------------------------------------- doctor

def cmd_doctor(_a):
    have = {b: bool(shutil.which(b)) for b in ("ffmpeg", "ffprobe")}
    filters = {}
    if have["ffmpeg"]:
        p = run([need("ffmpeg"), "-hide_banner", "-filters"], 30)
        for f in ("scdet", "silencedetect", "lut3d", "vidstabdetect", "vidstabtransform", "deshake", "zoompan",
                  "sendcmd", "drawtext", "ssim", "psnr", "xfade"):
            filters[f] = bool(re.search(rf"\s{f}\s", p.stdout))
    optional = {}
    for mod, pkg in (("numpy", "numpy"), ("scenedetect", "scenedetect[opencv]"), ("cv2", "opencv-python-headless"),
                     ("opentimelineio", "opentimelineio")):
        try:
            m = __import__(mod)
            optional[mod] = {"installed": True, "version": getattr(m, "__version__", "?")}
        except ImportError:
            optional[mod] = {"installed": False, "install": f"pip install {pkg}"}
    return receipt("doctor", binaries=have, filters=filters, python=optional, font=font_file(),
                   defaults={"vertical": f"{VERTICAL[0]}x{VERTICAL[1]}", "fps": FPS, "crf": CRF,
                             "pix_fmt": "yuv420p", "faststart": True, "audio": "copy when timing is unchanged"},
                   looks=list(LOOKS), moves=list(MOVES))


# ---------------------------------------------------------------- CLI

def build_parser():
    ap = argparse.ArgumentParser(prog="cinema_lab.py", description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("doctor", help="check ffmpeg filters, optional libraries and the export defaults")

    s = sub.add_parser("scenes", help="detect cuts -> scenes.json, storyboard sheet, OTIO/EDL")
    s.add_argument("--input", required=True)
    s.add_argument("--out", required=True, help="output folder")
    s.add_argument("--engine", choices=("auto", "ffmpeg", "pyscenedetect"), default="auto")
    s.add_argument("--threshold", type=float, help="ffmpeg scdet score (0..100, default 6) or PySceneDetect (default 27)")
    s.add_argument("--min-scene", type=float, default=0.6, help="shortest scene in seconds")
    s.add_argument("--sheet", action="store_true", help="write storyboard.jpg (one frame per scene)")
    s.add_argument("--cols", type=int, default=4)
    s.add_argument("--timeline", action="store_true", help="also write scenes.otio and scenes.edl")

    c = sub.add_parser("silence-cut", help="remove silences (Auto-Editor style) and render")
    c.add_argument("--input", required=True)
    c.add_argument("--output", required=True)
    c.add_argument("--noise", type=float, default=-35.0, help="silence level in dB")
    c.add_argument("--min-silence", type=float, default=0.45, help="shortest silence to remove, seconds")
    c.add_argument("--margin", type=float, default=0.12, help="speech padding kept on each side, seconds")
    c.add_argument("--min-keep", type=float, default=0.2, help="drop kept pieces shorter than this")
    c.add_argument("--size", default="keep", help="WxH or keep (default keep)")
    c.add_argument("--plan-only", action="store_true", help="write the plan without rendering")
    c.add_argument("--timeline", action="store_true", help="also write .otio and .edl next to the output")
    c.add_argument("--force", action="store_true")

    t = sub.add_parser("timeline", help="segment plan (kosif.segments.v1) -> .otio + .edl")
    t.add_argument("--plan", required=True)
    t.add_argument("--out", required=True, help="output path without extension")

    g = sub.add_parser("grade", help="apply a named look or a .cube LUT; export portable .cube files")
    g.add_argument("--input")
    g.add_argument("--output")
    g.add_argument("--look", choices=LOOKS, default="teal-orange")
    g.add_argument("--strength", type=float, default=0.8)
    g.add_argument("--lut", help="use this .cube instead of a named look")
    g.add_argument("--cube-out", help="also save the LUT here (alone: export the LUT only)")
    g.add_argument("--size", default="keep")
    g.add_argument("--force", action="store_true")

    st = sub.add_parser("stabilize", help="vid.stab two-pass stabilisation with measured shake")
    st.add_argument("--input", required=True)
    st.add_argument("--output", required=True)
    st.add_argument("--shakiness", type=int, default=6, choices=range(1, 11))
    st.add_argument("--smoothing", type=int, default=24)
    st.add_argument("--deshake", action="store_true", help="use the one-pass deshake filter")
    st.add_argument("--size", default="keep")
    st.add_argument("--force", action="store_true")

    r = sub.add_parser("reframe", help="track the subject and crop wide video to vertical")
    r.add_argument("--input", required=True)
    r.add_argument("--output", required=True)
    r.add_argument("--size", default=f"{VERTICAL[0]}x{VERTICAL[1]}")
    r.add_argument("--sample-fps", type=float, default=6.0)
    r.add_argument("--no-cuts", action="store_true", help="do not re-aim the camera at scene cuts")
    r.add_argument("--max-speed", type=float, default=0.35, help="camera speed cap in source widths per second")
    r.add_argument("--force", action="store_true")

    cam = sub.add_parser("camera", help="programmed camera move with easing on a still or a clip")
    cam.add_argument("--input", required=True)
    cam.add_argument("--output", required=True)
    cam.add_argument("--move", choices=MOVES, default="push-in")
    cam.add_argument("--zoom", type=float, default=1.25)
    cam.add_argument("--duration", type=float, default=5.0, help="seconds, for stills")
    cam.add_argument("--size", default=f"{VERTICAL[0]}x{VERTICAL[1]}")
    cam.add_argument("--supersample", type=int, default=3, choices=(1, 2, 3, 4))
    cam.add_argument("--force", action="store_true")

    rv = sub.add_parser("review", help="A/B side-by-side or wipe with timecode, plus SSIM/PSNR")
    rv.add_argument("--a", required=True)
    rv.add_argument("--b", required=True)
    rv.add_argument("--output", required=True)
    rv.add_argument("--mode", choices=("side", "wipe"), default="side")
    rv.add_argument("--label-a", default="A")
    rv.add_argument("--label-b", default="B")
    rv.add_argument("--height", type=int, default=720)
    rv.add_argument("--metrics", action="store_true")
    rv.add_argument("--force", action="store_true")
    return ap


COMMANDS = {"doctor": cmd_doctor, "scenes": cmd_scenes, "silence-cut": cmd_silence_cut, "timeline": cmd_timeline,
            "grade": cmd_grade, "stabilize": cmd_stabilize, "reframe": cmd_reframe, "camera": cmd_camera,
            "review": cmd_review}


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        COMMANDS[args.cmd](args)
    except (RuntimeError, ValueError) as exc:
        print(json.dumps({"schema": SCHEMA, "command": args.cmd, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
