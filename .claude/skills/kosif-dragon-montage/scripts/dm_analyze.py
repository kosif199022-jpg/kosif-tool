#!/usr/bin/env python3
"""Dragon Montage station 1 — «العين الأولى» (the first eye).

Looks at every clip (and an optional music track) and writes analysis.json
(kosif.dm.analysis.v1, see ../CONTRACTS.md):

  probe · loudness (ebur128) · shots (PySceneDetect, fallback ffmpeg scdet) ·
  per-shot quality (sharpness / exposure / shake / score) · faces · motion ·
  colour · one thumbnail per shot · words (faster-whisper + VAD) · silences ·
  RMS energy every 0.5 s · music beats + downbeats (librosa, fallback
  audio_cue_mapper + music_rhythm_engine) · contact sheet.

Every optional dependency that is missing leaves its field empty and is listed
in "missing" — the station never crashes because of it.

Usage:
  dm_analyze.py --job DIR --clip a.mp4 [--clip b.mp4 ...] [--music song.mp3]
                [--no-transcribe] [--whisper-model small] [--language ar]
"""
from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
import sys
import tempfile
import time
import wave
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dm_common as dm  # noqa: E402

STATION = "analyze"
SAMPLE_FPS = 4.0          # frames per second sampled for quality / faces / colour
SAMPLE_W = 480            # width of the sampled frames (and thumbnails)
ENERGY_STEP = 0.5         # seconds between RMS energy points
MIN_SHOT = 0.5            # seconds; shorter detections are merged
LONG_TIMEOUT = 3600       # seconds for whole-file ffmpeg passes; a timeout degrades into `missing`


def r3(x):
    return None if x is None else round(float(x), 3)


def clamp01(x):
    return max(0.0, min(1.0, float(x)))


class Ctx:
    """Collects tools_used / missing for the whole run and writes receipts."""

    def __init__(self, job: Path):
        self.job = job
        self.used: list[str] = []
        self.missing: list[str] = []

    def use(self, name):
        if name not in self.used:
            self.used.append(name)

    def miss(self, name):
        if name not in self.missing:
            self.missing.append(name)

    def receipt(self, tool, argv, rc, seconds, out=None, note=""):
        """Receipt for an in-process step (same line format as dm_common.run)."""
        rec = {"station": STATION, "tool": tool, "argv": [str(a) for a in argv][:40], "rc": rc,
               "seconds": round(seconds, 3), "owner_media": True,
               "sha256_out": dm.sha256(out) if out else None, "stderr_tail": note[-400:]}
        with (self.job / "receipts.jsonl").open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")

    def run(self, tool, argv, **kw):
        kw.setdefault("check", False)
        return dm.run(self.job, STATION, tool, argv, **kw)


def rel(job: Path, p: Path) -> str:
    try:
        return str(p.resolve().relative_to(job))
    except ValueError:
        return str(p.resolve())


# ---------------------------------------------------------------- probe / audio
def probe_clip(ctx: Ctx, path: Path) -> dict:
    res = ctx.run("ffprobe", ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path])
    ctx.use("ffprobe")
    info = json.loads(res.stdout or "{}") if res.returncode == 0 else {}
    streams = info.get("streams", [])
    v = next((s for s in streams if s.get("codec_type") == "video"), {})
    a = next((s for s in streams if s.get("codec_type") == "audio"), None)
    fps = 0.0
    try:
        num, den = (v.get("avg_frame_rate") or v.get("r_frame_rate") or "0/1").split("/")
        fps = float(num) / float(den) if float(den) else 0.0
    except (ValueError, ZeroDivisionError):
        pass
    dur = info.get("format", {}).get("duration") or v.get("duration") or 0
    return {"duration": r3(float(dur)), "width": int(v.get("width") or 0), "height": int(v.get("height") or 0),
            "fps": round(fps, 3), "has_audio": a is not None, "has_video": bool(v)}


def loudness(ctx: Ctx, path: Path):
    res = ctx.run("ffmpeg.ebur128", ["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-vn",
                                     "-af", "ebur128", "-f", "null", "-"], timeout=LONG_TIMEOUT)
    if res.returncode == 124:                       # timed out (dm.run turns TimeoutExpired into rc 124)
        ctx.miss("ffmpeg.ebur128 (timeout)")
        return None
    m = re.findall(r"I:\s+(-?[\d.]+|-inf)\s+LUFS", res.stderr or "")
    if not m or m[-1] == "-inf":
        return None
    ctx.use("ffmpeg.ebur128")
    return round(float(m[-1]), 1)


def silences(ctx: Ctx, path: Path, duration: float) -> list[dict]:
    res = ctx.run("ffmpeg.silencedetect", ["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-vn",
                                           "-af", "silencedetect=noise=-35dB:d=0.5", "-f", "null", "-"],
                  timeout=LONG_TIMEOUT)
    if res.returncode != 0:
        if res.returncode == 124:
            ctx.miss("ffmpeg.silencedetect (timeout)")
        return []
    ctx.use("ffmpeg.silencedetect")
    out, start = [], None
    for line in (res.stderr or "").splitlines():
        m = re.search(r"silence_start:\s*(-?[\d.]+)", line)
        if m:
            start = max(0.0, float(m.group(1)))
        m = re.search(r"silence_end:\s*(-?[\d.]+)", line)
        if m and start is not None:
            out.append({"start": r3(start), "end": r3(float(m.group(1)))})
            start = None
    if start is not None and duration:
        out.append({"start": r3(start), "end": r3(duration)})
    return out


def extract_wav(ctx: Ctx, path: Path, out: Path, sr: int = 16000) -> Path | None:
    res = ctx.run("ffmpeg.extract_audio", ["ffmpeg", "-y", "-v", "error", "-i", path, "-vn", "-ac", "1",
                                           "-ar", str(sr), "-c:a", "pcm_s16le", out], out=out,
                  timeout=LONG_TIMEOUT)
    return out if res.returncode == 0 and out.exists() and out.stat().st_size > 44 else None


def read_wav_mono(path: Path):
    """Returns (samples as list/np array of floats in -1..1, sample_rate)."""
    with wave.open(str(path), "rb") as w:
        sr, n, ch, sw = w.getframerate(), w.getnframes(), w.getnchannels(), w.getsampwidth()
        raw = w.readframes(n)
    try:
        import numpy as np
        data = np.frombuffer(raw, dtype="<i2").astype("float32") / 32768.0
        if ch > 1:
            data = data.reshape(-1, ch).mean(axis=1)
        return data, sr
    except ImportError:
        import array
        a = array.array("h")
        a.frombytes(raw)
        data = [x / 32768.0 for x in a]
        if ch > 1:
            data = [sum(data[i:i + ch]) / ch for i in range(0, len(data), ch)]
        return data, sr


def energy_curve(ctx: Ctx, wav: Path | None) -> list[dict]:
    if not wav:
        return []
    t0 = time.time()
    data, sr = read_wav_mono(wav)
    step = int(sr * ENERGY_STEP)
    out = []
    for i in range(0, len(data), step):
        chunk = data[i:i + step]
        if len(chunk) == 0:
            break
        try:
            rms = float((chunk ** 2).mean() ** 0.5)          # numpy
        except TypeError:
            rms = math.sqrt(sum(x * x for x in chunk) / len(chunk))
        out.append({"t": r3(i / sr), "rms": round(rms, 4)})
    ctx.receipt("rms_energy", ["rms", wav, f"step={ENERGY_STEP}"], 0, time.time() - t0)
    ctx.use("rms_energy")
    return out


# ---------------------------------------------------------------- words
_WHISPER = {}


def transcribe(ctx: Ctx, wav: Path | None, model_name: str, language: str | None) -> list[dict]:
    if not wav:
        return []
    if not dm.have_module("faster_whisper"):
        ctx.miss("faster-whisper")
        return []
    t0 = time.time()
    try:
        from faster_whisper import WhisperModel
        if model_name not in _WHISPER:
            _WHISPER[model_name] = WhisperModel(model_name, device="auto", compute_type="int8")
        model = _WHISPER[model_name]
    except Exception as exc:  # download blocked / no network / bad model
        ctx.miss("faster-whisper-model")
        ctx.receipt("faster-whisper", ["load", model_name], 1, time.time() - t0, note=str(exc))
        return []
    try:
        audio, sr = read_wav_mono(wav)           # 16 kHz mono float32: skips faster-whisper's PyAV decoder
        if sr != 16000 or not hasattr(audio, "dtype"):
            audio = str(wav)
        segs, _info = model.transcribe(audio, language=language or None, word_timestamps=True,
                                       vad_filter=True, beam_size=5)
        words = []
        for s in segs:
            for w in (s.words or []):
                txt = (w.word or "").strip()
                if txt:
                    words.append({"w": txt, "start": r3(w.start), "end": r3(w.end),
                                  "conf": round(float(w.probability or 0.0), 3)})
    except Exception as exc:
        ctx.receipt("faster-whisper", ["transcribe", wav, model_name], 1, time.time() - t0, note=str(exc))
        ctx.miss("faster-whisper-transcribe")
        return []
    ctx.receipt("faster-whisper", ["transcribe", wav, model_name, f"lang={language}", "vad"], 0, time.time() - t0)
    ctx.use("faster-whisper")
    return words


# ---------------------------------------------------------------- shots
def shots_pyscenedetect(ctx: Ctx, path: Path):
    t0 = time.time()
    try:
        from scenedetect import ContentDetector, detect
        scenes = detect(str(path), ContentDetector(threshold=27.0, min_scene_len=15))
    except Exception as exc:
        ctx.receipt("pyscenedetect", ["detect", path, "ContentDetector"], 1, time.time() - t0, note=str(exc))
        return None
    ctx.receipt("pyscenedetect", ["detect", path, "ContentDetector", "threshold=27"], 0, time.time() - t0)
    ctx.use("pyscenedetect")
    return [float(getattr(s[0], "seconds", None) or s[0].get_seconds()) for s in scenes[1:]]   # cut points (start of every scene after the first)


def shots_scdet(ctx: Ctx, path: Path):
    res = ctx.run("ffmpeg.scdet", ["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-an",
                                   "-vf", "scdet=threshold=10", "-f", "null", "-"],
                  timeout=LONG_TIMEOUT)
    if res.returncode != 0:
        if res.returncode == 124:
            ctx.miss("ffmpeg.scdet (timeout)")
        return None
    ctx.use("ffmpeg.scdet")
    return [float(m) for m in re.findall(r"lavfi\.scd\.time:\s*([\d.]+)", res.stderr or "")]


def build_shots(cuts, duration):
    starts = [0.0]
    for c in sorted(c for c in (cuts or []) if 0 < c < duration):
        if c - starts[-1] >= MIN_SHOT and duration - c >= MIN_SHOT:
            starts.append(c)
    return list(zip(starts, starts[1:] + [duration]))


# ---------------------------------------------------------------- frame sampling / quality
def sample_size(info: dict) -> tuple[int, int]:
    w = SAMPLE_W
    h = int(round(info["height"] * w / max(1, info["width"]) / 2) * 2) or 270
    return w, h


def iter_frames(ctx: Ctx, path: Path, info: dict, timeout: float = 1800):
    """Stream SAMPLE_FPS frames at SAMPLE_W wide → yields (t, HxWx3 RGB uint8). One frame in memory at a
    time (an hour of 4 fps 480p frames is ~5.6 GB if collected). A decode past `timeout` is stopped and
    what was read so far is kept; the receipt records it."""
    import numpy as np
    w, h = sample_size(info)
    argv = ["ffmpeg", "-v", "error", "-i", str(path), "-an", "-vf",
            f"fps={SAMPLE_FPS},scale={w}:{h}", "-pix_fmt", "rgb24", "-f", "rawvideo", "-"]
    size = w * h * 3
    t0 = time.time()
    n, note = 0, ""
    with tempfile.TemporaryFile() as err:
        proc = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=err, stdin=subprocess.DEVNULL)
        try:
            while True:
                if time.time() - t0 > timeout:
                    proc.kill()
                    note = f"timeout after {timeout}s ({n} frames kept)"
                    break
                buf = proc.stdout.read(size)
                if not buf or len(buf) < size:
                    break
                yield (n + 0.5) / SAMPLE_FPS, np.frombuffer(buf, dtype=np.uint8).reshape(h, w, 3)
                n += 1
        finally:
            if proc.poll() is None:
                proc.kill()
            proc.stdout.close()
            rc = proc.wait()
            err.seek(0)
            note = note or (err.read().decode("utf-8", "replace") if rc else "")
            ctx.receipt("ffmpeg.sample_frames", argv + [f"frames={n}"], 124 if note.startswith("timeout") else rc,
                        time.time() - t0, note=note)


def sample_frames(ctx: Ctx, path: Path, info: dict):
    """Decode SAMPLE_FPS frames → (times, frames). Collects everything: only for short clips / tests;
    analyze_clip streams with iter_frames + ShotAcc instead."""
    times, frames = [], []
    for t, f in iter_frames(ctx, path, info):
        times.append(t)
        frames.append(f)
    return times, frames


def write_jpg(path: Path, rgb, quality: int = 85) -> bool:
    """cv2.imwrite silently fails on non-ASCII paths on Windows: encode in memory, write with Python."""
    import cv2
    ok, buf = cv2.imencode(".jpg", cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR) if rgb.ndim == 3 else rgb,
                           [cv2.IMWRITE_JPEG_QUALITY, quality])
    if not ok:
        return False
    try:
        Path(path).write_bytes(buf.tobytes())
    except OSError:
        return False
    return True


def read_img(path: Path):
    """cv2.imread twin of write_jpg (BGR array or None) that works with any path."""
    import cv2
    import numpy as np
    try:
        data = np.frombuffer(Path(path).read_bytes(), dtype=np.uint8)
    except OSError:
        return None
    return cv2.imdecode(data, cv2.IMREAD_COLOR) if data.size else None


_FACE = {}


def face_detector():
    """Reuse KMM/faces.py with the YuNet model the doctor manages (data/required_tools.json →
    yunet-face-model: <skill>/models, ~/.cache/kosif/models, KMM/kit/models or $KOSIF_YUNET).
    OpenCV 5 has no Haar cascades; KMM's skin-colour fallback counts hands, so it is not used for a
    face count: without the model faces stay null and the missing model is reported."""
    if "d" not in _FACE:
        _FACE["d"], _FACE["name"] = None, None
        try:
            sys.path.insert(0, str(dm.KMM))
            # vendored files must stay free of __pycache__ (test_superskills checks it)
            _dwb, sys.dont_write_bytecode = sys.dont_write_bytecode, True
            try:
                import faces as kmm_faces  # noqa: E402
            finally:
                sys.dont_write_bytecode = _dwb
            try:
                import dm_doctor
                mp = dm_doctor.model_path("yunet-face-model")
            except Exception:
                mp = None
            if mp and kmm_faces.which() != "yunet":
                kmm_faces.MODEL, kmm_faces._DET = Path(mp), None
            name = kmm_faces.which()
            if name in ("yunet", "haar"):
                _FACE["d"], _FACE["name"] = kmm_faces.detect, name
        except Exception:
            pass
    return _FACE["d"]


def largest_face(boxes, w: int, h: int):
    """(cx, cy, box) of the largest face, normalised to the frame, or None."""
    if not boxes:
        return None
    x, y, bw, bh = max(boxes, key=lambda b: b[2] * b[3])[:4]
    return ((x + bw / 2) / w, (y + bh / 2) / h, [x / w, y / h, bw / w, bh / h])


class ShotAcc:
    """Per-shot metrics fed one frame at a time. Keeps only the running statistics, the previous frame
    and the ≤5 frames used for faces / clipping / the thumbnail (indices from the expected count n)."""

    def __init__(self, n: int):
        self.n = max(1, int(n))
        self.pick = sorted({0, self.n // 4, self.n // 2, (3 * self.n) // 4, self.n - 1})
        self.kept: dict[int, object] = {}
        self.last = None
        self.k = 0
        self.sharp, self.luma, self.diffs, self.shifts, self.sats, self.rgbs = [], [], [], [], [], []
        self.prev = None

    def add(self, f) -> None:
        import cv2
        import numpy as np
        g = cv2.cvtColor(f, cv2.COLOR_RGB2GRAY)
        self.sharp.append(cv2.Laplacian(g, cv2.CV_64F).var())
        self.luma.append(g.mean() / 255.0)
        hsv = cv2.cvtColor(f, cv2.COLOR_RGB2HSV)
        self.sats.append(hsv[..., 1].mean() / 255.0)
        self.rgbs.append(f.reshape(-1, 3).mean(axis=0) / 255.0)
        gf = g.astype("float32")
        if self.prev is not None:
            self.diffs.append(float(np.abs(gf - self.prev).mean()) / 255.0)
            (dx, dy), _ = cv2.phaseCorrelate(self.prev, gf)
            self.shifts.append((dx, dy))
        self.prev = gf
        if self.k in self.pick:
            self.kept[self.k] = f
        self.last = f
        self.k += 1

    def frames(self) -> list:
        """The kept frames in order (the last frame stands in for n-1 when fewer arrived than expected)."""
        out = dict(self.kept)
        if self.last is not None and (self.k - 1) not in out:
            out[self.k - 1] = self.last
        return [out[i] for i in sorted(out)]

    def mid(self):
        fr = self.frames()
        return self.kept.get(self.n // 2) if self.n // 2 in self.kept else (fr[len(fr) // 2] if fr else None)

    def finish(self, ctx: Ctx) -> dict:
        import cv2
        import numpy as np
        sharp, luma, diffs, shifts, sats, rgbs = self.sharp, self.luma, self.diffs, self.shifts, self.sats, self.rgbs
        frames = self.frames()
        lap = float(np.median(sharp)) if sharp else 0.0
        sharpness = lap / (lap + 150.0)                      # 150 ≈ soft/sharp knee at 480px wide
        L = float(np.mean(luma)) if luma else 0.0
        exposure = clamp01(1.0 - abs(L - 0.5) * 2.0)          # 1 = well exposed mid-tones
        clipped = 0.0
        m = self.mid()
        if m is not None:
            g = cv2.cvtColor(m, cv2.COLOR_RGB2GRAY)
            clipped = float(((g < 8) | (g > 247)).mean())
            exposure = clamp01(exposure - 0.5 * clipped)
        shake = 0.0
        if len(shifts) >= 3:
            s = np.array(shifts)
            jerk = np.diff(s, axis=0)                         # camera jitter = change of global translation
            j = float(np.sqrt((jerk ** 2).sum(axis=1)).mean())
            shake = j / (j + 3.0)
        motion = clamp01(float(np.mean(diffs)) * 6.0) if diffs else 0.0
        score = clamp01(0.45 * sharpness + 0.30 * exposure + 0.25 * (1.0 - shake))
        faces, face_c, face_box = None, None, None
        det = face_detector()
        if det is None:
            ctx.miss("yunet-face-model")
        elif frames:
            faces, found = 0, []
            for f in frames:
                boxes = det(f)
                faces = max(faces, len(boxes))
                lf = largest_face(boxes, f.shape[1], f.shape[0])
                if lf:
                    found.append(lf)
            if found:   # median centre of the per-frame largest face → crop anchor for dm_render
                face_c = [r3(float(np.median([f[0] for f in found]))), r3(float(np.median([f[1] for f in found])))]
                face_box = [r3(v) for v in max(found, key=lambda f: f[2][2] * f[2][3])[2]]
            ctx.use(f"kmm.faces.{_FACE['name']}")
        mean_rgb = np.mean(rgbs, axis=0).tolist() if rgbs else [0, 0, 0]
        return {
            "quality": {"sharpness": r3(sharpness), "exposure": r3(exposure), "shake": r3(shake), "score": r3(score),
                        "luma": r3(L), "clipped": r3(clipped)},
            "faces": faces, "face_center": face_c, "faces_box": face_box, "motion_energy": r3(motion),
            "color": {"mean_rgb": [r3(c) for c in mean_rgb], "saturation": r3(np.mean(sats) if sats else 0.0)},
        }


def shot_metrics(ctx: Ctx, frames):
    """Quality/faces/motion/colour for one shot's frames (list of RGB arrays)."""
    acc = ShotAcc(len(frames))
    for f in frames:
        acc.add(f)
    return acc.finish(ctx)


def expected_samples(s: float, e: float) -> int:
    """How many sample times (i+0.5)/SAMPLE_FPS fall in [s, e)."""
    lo = math.ceil(s * SAMPLE_FPS - 0.5 - 1e-9)
    hi = math.ceil(e * SAMPLE_FPS - 0.5 - 1e-9)
    return max(0, hi - max(0, lo))


def ffmpeg_thumb(ctx: Ctx, path: Path, t: float, out: Path):
    ctx.run("ffmpeg.thumb", ["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", path, "-frames:v", "1",
                             "-vf", f"scale={SAMPLE_W}:-2", "-q:v", "4", out], out=out)
    return out.exists()


def contact_sheet(ctx: Ctx, items, out: Path, cols: int = 4):
    """items: list of (label, Path). Writes a grid jpg with OpenCV."""
    import cv2
    import numpy as np
    t0 = time.time()
    tiles = []
    tw = 320
    for label, p in items:
        img = read_img(p)
        if img is None:
            continue
        th = int(img.shape[0] * tw / img.shape[1])
        img = cv2.resize(img, (tw, th))
        cv2.rectangle(img, (0, 0), (tw, 22), (0, 0, 0), -1)
        cv2.putText(img, label, (6, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        tiles.append(img)
    if not tiles:
        return None
    th = max(t.shape[0] for t in tiles)
    tiles = [cv2.copyMakeBorder(t, 0, th - t.shape[0], 0, 0, cv2.BORDER_CONSTANT, value=(20, 20, 20)) for t in tiles]
    while len(tiles) % cols:
        tiles.append(np.full_like(tiles[0], 20))
    rows = [np.hstack(tiles[i:i + cols]) for i in range(0, len(tiles), cols)]
    sheet = np.vstack(rows)
    if not write_jpg(out, sheet[..., ::-1]):         # sheet is BGR; write_jpg takes RGB
        ctx.receipt("opencv.contact_sheet", ["contact_sheet", out], 1, time.time() - t0, note="jpeg write failed")
        return None
    ctx.receipt("opencv.contact_sheet", ["contact_sheet", out, f"tiles={len(items)}"], 0, time.time() - t0, out=out)
    return out


# ---------------------------------------------------------------- clip
def analyze_clip(ctx: Ctx, cid: str, path: Path, adir: Path, args) -> dict:
    info = probe_clip(ctx, path)
    dur = info["duration"] or 0.0
    clip = {"id": cid, "path": str(path), "duration": dur, "width": info["width"], "height": info["height"],
            "fps": info["fps"], "has_audio": info["has_audio"], "loudness_lufs": None,
            "shots": [], "words": [], "silences": [], "energy": []}

    # shots
    cuts = None
    if info["has_video"]:
        if dm.have_module("scenedetect"):
            cuts = shots_pyscenedetect(ctx, path)
        else:
            ctx.miss("pyscenedetect")
        if cuts is None:
            cuts = shots_scdet(ctx, path)
        if cuts is None:
            ctx.miss("shot-detection")
    bounds = build_shots(cuts, dur) if info["has_video"] else []

    # per-shot metrics
    can_cv = dm.have_module("cv2") and dm.have_module("numpy")
    if not can_cv:
        ctx.miss("opencv")
    shots = []
    for i, (s, e) in enumerate(bounds, 1):
        sid = f"{cid}-s{i:03d}"
        shots.append({"id": sid, "start": r3(s), "end": r3(e),
                      "quality": {"sharpness": None, "exposure": None, "shake": None, "score": None},
                      "faces": None, "face_center": None, "faces_box": None, "motion_energy": None,
                      "color": {"mean_rgb": None, "saturation": None},
                      "thumb": None})
    accs: dict[int, ShotAcc] = {}
    if can_cv and bounds:
        cur, done = 0, set()

        def close(k):
            acc = accs.get(k)
            if acc is None or k in done:
                return
            done.add(k)
            shots[k].update(acc.finish(ctx))
            thumb = adir / f"{shots[k]['id']}.jpg"
            m = acc.mid()
            if m is not None and write_jpg(thumb, m):
                shots[k]["thumb"] = rel(ctx.job, thumb)
            accs[k] = None                                 # free the kept frames
        for t, f in iter_frames(ctx, path, info):
            while cur < len(bounds) - 1 and t >= bounds[cur][1]:
                close(cur)
                cur += 1
            if accs.get(cur) is None and cur not in done:
                accs[cur] = ShotAcc(expected_samples(*bounds[cur]))
            accs[cur].add(f)
        for k in list(accs):
            close(k)
        if done:
            ctx.use("opencv.quality")
    for k, (s, e) in enumerate(bounds):
        shot = shots[k]
        thumb = adir / f"{shot['id']}.jpg"
        if not shot["thumb"] and info["has_video"] and ffmpeg_thumb(ctx, path, (s + e) / 2, thumb):
            shot["thumb"] = rel(ctx.job, thumb)
        clip["shots"].append(shot)

    # audio
    if info["has_audio"]:
        clip["loudness_lufs"] = loudness(ctx, path)
        clip["silences"] = silences(ctx, path, dur)
        with tempfile.TemporaryDirectory(prefix="dm_an_") as td:
            wav = extract_wav(ctx, path, Path(td) / f"{cid}.wav")
            clip["energy"] = energy_curve(ctx, wav)
            if not args.no_transcribe:
                clip["words"] = transcribe(ctx, wav, args.whisper_model, args.language)
    return clip


# ---------------------------------------------------------------- music
def downbeats_from(beats, strength=None):
    """Every 4th beat, phase chosen where onset strength is highest."""
    if len(beats) < 4:
        return list(beats[:1])
    best, best_k = -1.0, 0
    for k in range(4):
        sel = range(k, len(beats), 4)
        v = sum(strength[i] for i in sel) / max(1, len(sel)) if strength is not None else (1.0 if k == 0 else 0.0)
        if v > best:
            best, best_k = v, k
    return beats[best_k::4]


def music_librosa(ctx: Ctx, path: Path):
    t0 = time.time()
    try:
        import librosa
        import numpy as np
        y, sr = librosa.load(str(path), sr=22050, mono=True)
        hop = 256
        env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop)
        tempo, frames = librosa.beat.beat_track(onset_envelope=env, sr=sr, hop_length=hop, units="frames")
        frames = np.asarray(frames, dtype=int)
        beats = librosa.frames_to_time(frames, sr=sr, hop_length=hop).tolist()
        if len(beats) >= 4:     # robust tempo: slope of beat time vs index (avoids frame-quantised IBI)
            slope = float(np.polyfit(np.arange(len(beats)), np.array(beats), 1)[0])
            bpm = 60.0 / slope if slope > 0 else float(np.atleast_1d(tempo)[0])
        else:
            bpm = float(np.atleast_1d(tempo)[0]) if len(np.atleast_1d(tempo)) else None
        # strength at each beat = max onset env in a ±2 frame window (strongest onset alignment)
        strength = [float(env[max(0, f - 2):f + 3].max()) if len(env) else 0.0 for f in frames]
        down = downbeats_from(beats, strength)
    except Exception as exc:
        ctx.receipt("librosa.beat_track", ["beat_track", path], 1, time.time() - t0, note=str(exc))
        return None
    ctx.receipt("librosa.beat_track", ["beat_track", path, f"hop={hop}"], 0, time.time() - t0)
    ctx.use("librosa")
    return {"bpm": round(bpm, 2) if bpm else None, "beats": [r3(b) for b in beats],
            "downbeats": [r3(b) for b in down]}


def music_fallback(ctx: Ctx, path: Path):
    acm, mre = dm.SP / "audio_cue_mapper.py", dm.SP / "music_rhythm_engine.py"
    if not (acm.exists() and mre.exists()):
        return None
    with tempfile.TemporaryDirectory(prefix="dm_mu_") as td:
        td = Path(td)
        wav = extract_wav(ctx, path, td / "music.wav", sr=22050)
        if not wav:
            return None
        cues, rh = td / "cues.json", td / "rhythm.json"
        if ctx.run("audio_cue_mapper", dm.py(acm) + [wav, "--out", cues], out=cues).returncode:
            return None
        if ctx.run("music_rhythm_engine", dm.py(mre) + [cues, "--out", rh], out=rh).returncode:
            return None
        data = json.loads(rh.read_text(encoding="utf-8"))
    ctx.use("music_rhythm_engine")
    beats = [r3(b) for b in data.get("estimated_grid_seconds") or []]
    return {"bpm": data.get("candidate_tempo_bpm"), "beats": beats, "downbeats": downbeats_from(beats)}


def analyze_music(ctx: Ctx, path: Path | None) -> dict:
    out = {"path": str(path) if path else None, "bpm": None, "beats": [], "downbeats": []}
    if not path:
        return out
    got = None
    if dm.have_module("librosa"):
        got = music_librosa(ctx, path)
    else:
        ctx.miss("librosa")
    if got is None:
        got = music_fallback(ctx, path)
    if got is None:
        ctx.miss("beat-tracking")
        return out
    out.update(got)
    return out


# ---------------------------------------------------------------- main
def analyze(job: Path, clips: list[Path], music: Path | None, args) -> dict:
    ctx = Ctx(job)
    adir = job / "analysis"
    adir.mkdir(parents=True, exist_ok=True)
    if not dm.have("ffprobe") or not dm.have("ffmpeg"):
        raise SystemExit("ffmpeg/ffprobe are required for station 1 (العين الأولى)")
    result = dm.new("analysis", clips=[], music={}, contact_sheet=None, tools_used=[], missing=[])
    for i, p in enumerate(clips, 1):
        result["clips"].append(analyze_clip(ctx, f"c{i:02d}", p, adir, args))
    result["music"] = analyze_music(ctx, music)
    items = [(s["id"], job / s["thumb"]) for c in result["clips"] for s in c["shots"] if s.get("thumb")]
    if items and dm.have_module("cv2"):
        sheet = contact_sheet(ctx, items, adir / "contact.jpg")
        if sheet:
            result["contact_sheet"] = rel(job, sheet)
            ctx.use("opencv.contact_sheet")
    if args.no_transcribe:
        result["transcribe"] = "skipped (--no-transcribe)"
    result["tools_used"], result["missing"] = ctx.used, ctx.missing
    dm.write(job, "analysis", result)
    return result


def main(argv=None):
    dm.utf8_stdio()
    ap = argparse.ArgumentParser(description="Dragon Montage station 1 — analysis.json")
    ap.add_argument("--job", required=True, help="job folder")
    ap.add_argument("--clip", action="append", required=True, help="input video (repeatable, in order)")
    ap.add_argument("--music", help="optional music track")
    ap.add_argument("--no-transcribe", action="store_true")
    ap.add_argument("--whisper-model", default="small")
    ap.add_argument("--language", default="ar", help="whisper language code, or 'auto'")
    args = ap.parse_args(argv)
    if args.language == "auto":
        args.language = None
    job = dm.job_dir(args.job)
    clips = [Path(c).resolve() for c in args.clip]
    for c in clips:
        if not c.is_file():
            ap.error(f"clip not found: {c}")
    music = Path(args.music).resolve() if args.music else None
    if music and not music.is_file():
        ap.error(f"music not found: {music}")
    res = analyze(job, clips, music, args)
    print(json.dumps({"analysis": str(job / "analysis.json"),
                      "clips": len(res["clips"]),
                      "shots": sum(len(c["shots"]) for c in res["clips"]),
                      "words": sum(len(c["words"]) for c in res["clips"]),
                      "bpm": res["music"]["bpm"], "missing": res["missing"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
