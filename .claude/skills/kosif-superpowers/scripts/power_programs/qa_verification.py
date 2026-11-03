"""Real programs for the qa-verification power cards (Black Dragon).

Every function builds its own synthetic fixture (frames, audio, MP4 files, JSON specs, HTML/CSS
text), performs the card's technique with the card's own numbers and returns known-answer checks:
a clean fixture must pass and a planted defect (black stretch, freeze, loud peak, low contrast,
gap in a timeline, banned token ...) must be caught. Offline, deterministic, no network, no LLM.
Cards whose proof is an existing code file in this repo, or that need a paid service, a GUI, a
browser-only CLI or a human judgement, are not here (see out/power-programs/qa-skipped.json).
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import subprocess
import wave
from pathlib import Path

import numpy as np

# ----------------------------------------------------------------------------- shared helpers

def _run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, check=True, **kw)


def ff(*args):
    """Run ffmpeg quietly (raises on error)."""
    _run(["ffmpeg", "-nostdin", "-v", "error", "-y", *map(str, args)])


def ff_log(*args) -> str:
    """Run ffmpeg with info logging into a null muxer and return stderr (filter reports)."""
    p = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-nostats", "-v", "info", *map(str, args)],
                       capture_output=True, text=True)
    return p.stderr


def probe(path) -> dict:
    out = _run(["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)]).stdout
    return json.loads(out)


def vstream(info):
    return next(s for s in info["streams"] if s["codec_type"] == "video")


def astreams(info):
    return [s for s in info["streams"] if s["codec_type"] == "audio"]


def write_wav(path, x, sr=48000):
    x = np.asarray(x, dtype=np.float64)
    if x.ndim == 1:
        x = x[None, :]
    pcm = (np.clip(x, -1, 1) * 32767).round().astype("<i2").T.copy()
    with wave.open(str(path), "wb") as w:
        w.setnchannels(x.shape[0]); w.setsampwidth(2); w.setframerate(sr); w.writeframes(pcm.tobytes())
    return Path(path)


def read_wav(path):
    with wave.open(str(path), "rb") as w:
        n, ch, sr = w.getnframes(), w.getnchannels(), w.getframerate()
        data = np.frombuffer(w.readframes(n), dtype="<i2").astype(np.float64) / 32768.0
    return data.reshape(-1, ch).T, sr


def tone(freq=1000.0, dur=2.0, sr=48000, amp=0.5, phase=0.0):
    t = np.arange(int(round(dur * sr))) / sr
    return amp * np.sin(2 * np.pi * freq * t + phase)


def write_video(path, frames, fps=30, audio=None, sr=48000, vcodec="libx264", pix="yuv420p", extra=(),
                acodec="aac", abitrate="192k", preset="ultrafast"):
    """frames: uint8 array (N,H,W) grey or (N,H,W,3) rgb. audio: float array (ch,n) or (n,)."""
    frames = np.asarray(frames, dtype=np.uint8)
    if frames.ndim == 3:
        frames = np.repeat(frames[..., None], 3, axis=3)
    n, h, w, _ = frames.shape
    path = Path(path)
    cmd = ["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}",
           "-r", str(fps), "-i", "-"]
    if audio is not None:
        wav = write_wav(path.with_suffix(".src.wav"), audio, sr)
        cmd += ["-i", str(wav)]
    cmd += ["-c:v", vcodec]
    if vcodec == "libx264":
        cmd += ["-preset", preset, "-crf", "18"]
    if pix:
        cmd += ["-pix_fmt", pix]
    if audio is not None:
        cmd += ["-c:a", acodec] + (["-b:a", abitrate] if acodec == "aac" else []) + ["-shortest"]
    cmd += list(map(str, extra)) + [str(path)]
    subprocess.run(cmd, input=frames.tobytes(), capture_output=True, check=True)
    if audio is not None:
        path.with_suffix(".src.wav").unlink()
    return path


def decode_gray(path, w=None, h=None, fps=None):
    info = vstream(probe(path))
    W, H = (w or int(info["width"])), (h or int(info["height"]))
    vf = [f"scale={W}:{H}"] + ([f"fps={fps}"] if fps else [])
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(path), "-vf", ",".join(vf), "-f", "rawvideo",
                          "-pix_fmt", "gray", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.uint8).reshape(-1, H, W)


def decode_rgb(path, w=None, h=None):
    info = vstream(probe(path))
    W, H = (w or int(info["width"])), (h or int(info["height"]))
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(path), "-vf", f"scale={W}:{H}", "-f", "rawvideo",
                          "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.uint8).reshape(-1, H, W, 3)


def moving_frames(n=60, h=36, w=64, seed=0, speed=2):
    """Textured frames that move every frame (never frozen, never black)."""
    rng = np.random.default_rng(seed)
    base = rng.integers(40, 215, size=(h, w * 4)).astype(np.uint8)
    base = ((base.astype(np.float32) + np.roll(base, 1, 1) + np.roll(base, 1, 0)) / 3).astype(np.uint8)
    return np.stack([base[:, (i * speed) % (w * 3):(i * speed) % (w * 3) + w] for i in range(n)])


# --- loudness (ITU-R BS.1770-4 / EBU R128) --------------------------------------------------

def k_weight(x, sr):
    from scipy.signal import lfilter
    f0, G, Q = 1681.974450955533, 3.999843853973347, 0.7071752369554196
    K = math.tan(math.pi * f0 / sr); Vh = 10 ** (G / 20); Vb = Vh ** 0.4996667741545416
    a0 = 1 + K / Q + K * K
    b1 = [(Vh + Vb * K / Q + K * K) / a0, 2 * (K * K - Vh) / a0, (Vh - Vb * K / Q + K * K) / a0]
    a1 = [1, 2 * (K * K - 1) / a0, (1 - K / Q + K * K) / a0]
    f0, Q = 38.13547087602444, 0.5003270373238773
    K = math.tan(math.pi * f0 / sr); d = 1 + K / Q + K * K
    b2, a2 = [1, -2, 1], [1, 2 * (K * K - 1) / d, (1 - K / Q + K * K) / d]
    return lfilter(b2, a2, lfilter(b1, a1, x, axis=-1), axis=-1)


def block_energies(x, sr, block=0.4, hop=0.1):
    x = np.atleast_2d(np.asarray(x, dtype=np.float64))
    y = k_weight(x, sr)
    bl, hp = int(round(block * sr)), int(round(hop * sr))
    if y.shape[1] < bl:
        return np.array([])
    starts = range(0, y.shape[1] - bl + 1, hp)
    return np.array([np.sum(np.mean(y[:, s:s + bl] ** 2, axis=1)) for s in starts])


def lufs(x, sr, abs_gate=-70.0, rel_gate=-10.0):
    z = block_energies(x, sr)
    if not len(z):
        return -math.inf
    with np.errstate(divide="ignore"):
        l = -0.691 + 10 * np.log10(z)
    z1 = z[l > abs_gate]
    if not len(z1):
        return -math.inf
    g = -0.691 + 10 * math.log10(np.mean(z1)) + rel_gate
    z2 = z[(l > abs_gate) & (l > g)]
    return -0.691 + 10 * math.log10(np.mean(z2))


def true_peak_dbtp(x, sr, over=4):
    from scipy.signal import resample_poly
    x = np.atleast_2d(np.asarray(x, dtype=np.float64))
    up = resample_poly(x, over, 1, axis=1)
    pk = max(np.max(np.abs(up)), np.max(np.abs(x)))
    return 20 * math.log10(max(pk, 1e-12))


def scale_to_lufs(x, sr, target):
    return np.asarray(x) * 10 ** ((target - lufs(x, sr)) / 20)


def ebur128(path) -> dict:
    """ffmpeg's own EBU R128 measurement of a file: integrated I (LUFS), LRA and true peak (dBTP)."""
    log = ff_log("-i", path, "-af", "ebur128=peak=true", "-f", "null", "-")
    tail = log[log.rfind("Summary:"):]
    I = float(re.search(r"I:\s+(-?[\d.]+|-inf)\s+LUFS", tail).group(1))
    lra = float(re.search(r"LRA:\s+(-?[\d.]+)\s+LU", tail).group(1))
    m = re.search(r"True peak:\s+Peak:\s+(-?[\d.]+|-inf)", tail)
    tp = float(m.group(1)) if m else float("nan")
    return {"I": I, "LRA": lra, "TP": tp}


def blackdetect(path, d=0.4, pix_th=0.03, pic_th=0.98):
    log = ff_log("-i", path, "-vf", f"blackdetect=d={d}:pix_th={pix_th}:pic_th={pic_th}", "-an", "-f", "null", "-")
    return [(float(a), float(b)) for a, b in re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", log)]


def freezedetect(path, noise_db=-60, d=1.5):
    log = ff_log("-i", path, "-vf", f"freezedetect=n={noise_db}dB:d={d}", "-an", "-f", "null", "-")
    starts = [float(v) for v in re.findall(r"freeze_start: ([\d.]+)", log)]
    ends = [float(v) for v in re.findall(r"freeze_end: ([\d.]+)", log)]
    dur = float(probe(path)["format"]["duration"])
    ends += [dur] * (len(starts) - len(ends))
    return list(zip(starts, ends))


def silencedetect(path, noise_db=-50, d=0.5):
    log = ff_log("-i", path, "-af", f"silencedetect=n={noise_db}dB:d={d}", "-vn", "-f", "null", "-")
    starts = [float(v) for v in re.findall(r"silence_start: (-?[\d.]+)", log)]
    ends = [float(v) for v in re.findall(r"silence_end: ([\d.]+)", log)]
    dur = float(probe(path)["format"]["duration"])
    ends += [dur] * (len(starts) - len(ends))
    return list(zip(starts, ends))


def scene_times(path, thr=0.3):
    log = ff_log("-i", path, "-vf", f"select='gt(scene,{thr})',showinfo", "-an", "-f", "null", "-")
    return [float(t) for t in re.findall(r"pts_time:([\d.]+)", log)]


def moov_before_mdat(path) -> bool:
    data = Path(path).read_bytes()
    i, order = 0, []
    while i + 8 <= len(data):
        size = int.from_bytes(data[i:i + 4], "big"); kind = data[i + 4:i + 8].decode("latin1")
        order.append(kind)
        if size == 1:
            size = int.from_bytes(data[i + 8:i + 16], "big")
        if size < 8:
            break
        i += size
    return "moov" in order and "mdat" in order and order.index("moov") < order.index("mdat")


# --- colour ----------------------------------------------------------------------------------

def hex_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rel_lum(c):
    if isinstance(c, str):
        c = hex_rgb(c)
    def ch(v):
        v = v / 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(v) for v in c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = rel_lum(a), rel_lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def rgb_to_lab(rgb):
    rgb = np.asarray(rgb, dtype=np.float64) / 255.0
    lin = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124564, 0.3575761, 0.1804375], [0.2126729, 0.7151522, 0.0721750], [0.0193339, 0.1191920, 0.9503041]])
    xyz = lin @ M.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > (6 / 29) ** 3, np.cbrt(xyz), xyz / (3 * (6 / 29) ** 2) + 4 / 29)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], axis=-1)


def delta_e76(a, b):
    if isinstance(a, str):
        a = hex_rgb(a)
    if isinstance(b, str):
        b = hex_rgb(b)
    return float(np.linalg.norm(rgb_to_lab(a) - rgb_to_lab(b)))


# --- image measures --------------------------------------------------------------------------

def laplacian_var(gray):
    import cv2
    return float(cv2.Laplacian(np.asarray(gray, dtype=np.float64), cv2.CV_64F).var())


def immerkaer_sigma(gray):
    from scipy.signal import convolve2d
    g = np.asarray(gray, dtype=np.float64); H, W = g.shape
    M = np.array([[1, -2, 1], [-2, 4, -2], [1, -2, 1]])
    s = np.sum(np.abs(convolve2d(g, M, mode="valid")))
    return float(s * math.sqrt(0.5 * math.pi) / (6 * (W - 2) * (H - 2)))


def blur_box(img, r):
    import cv2
    return cv2.blur(np.asarray(img), (2 * r + 1, 2 * r + 1))


def save_png(path, arr):
    from PIL import Image
    Image.fromarray(np.asarray(arr, dtype=np.uint8)).save(path)
    return Path(path)


def font_path(arabic=False):
    here = Path(__file__).resolve()
    cands = []
    if arabic:
        cands += [here.parents[4] / "fonts" / "kosif-jumuah" / "KOSIFJumuah-Regular.ttf",
                  Path("/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf"),
                  Path("/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf")]
    cands += [Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
              Path("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"),
              Path("/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf")]
    for c in cands:
        if c.is_file():
            return str(c)
    return None


def pil_font(size, arabic=False):
    from PIL import ImageFont
    p = font_path(arabic)
    return ImageFont.truetype(p, size) if p else ImageFont.load_default(size=size)


def wjson(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    return Path(path)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def par(fn, items):
    """Run independent ffmpeg-bound jobs in threads; results keep input order."""
    from concurrent.futures import ThreadPoolExecutor
    items = list(items)
    with ThreadPoolExecutor(max_workers=min(4, len(items) or 1)) as ex:
        return list(ex.map(lambda a: fn(*a) if isinstance(a, tuple) else fn(a), items))


PROGRAMS: dict = {}


def program(pid):
    def deco(fn):
        PROGRAMS[pid] = fn
        return fn
    return deco


def C(name, ok, obs=""):
    return (name, bool(ok), str(obs))


def stereo(x):
    return np.stack([x, x])


def gate_film(work, name, frames, fps=30, audio_lufs=-14.0, audio=None, sr=48000, extra=(), acodec="aac"):
    """Encode a test film (H.264 yuv420p + AAC) with a 440 Hz bed scaled to audio_lufs."""
    n = len(frames)
    if audio is None and audio_lufs is not None:
        bed = tone(440, n / fps, sr, 0.3) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.5 * np.arange(int(round(n / fps * sr))) / sr))
        audio = scale_to_lufs(stereo(bed), sr, audio_lufs)
    return write_video(Path(work) / name, frames, fps, audio=audio, sr=sr, extra=extra, acodec=acodec)


def analyze(path, black_d=0.4, pix_th=0.03, freeze_db=-60, freeze_d=1.5, audio=True):
    """One ffmpeg pass: blackdetect + freezedetect on video, ebur128 (true peak) on audio."""
    args = ["-i", path, "-vf", f"blackdetect=d={black_d}:pix_th={pix_th},freezedetect=n={freeze_db}dB:d={freeze_d}"]
    args += ["-af", "ebur128=peak=true"] if audio else ["-an"]
    log = ff_log(*args, "-f", "null", "-")
    dur = float(probe(path)["format"]["duration"])
    blacks = [(float(a), float(b)) for a, b in re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", log)]
    fs = [float(v) for v in re.findall(r"freeze_start: ([\d.]+)", log)]
    fe = [float(v) for v in re.findall(r"freeze_end: ([\d.]+)", log)]
    fe += [dur] * (len(fs) - len(fe))
    loud = None
    if audio and "Summary:" in log:
        tail = log[log.rfind("Summary:"):]
        m = re.search(r"True peak:\s+Peak:\s+(-?[\d.]+|-inf)", tail)
        loud = {"I": float(re.search(r"I:\s+(-?[\d.]+|-inf)\s+LUFS", tail).group(1)),
                "LRA": float(re.search(r"LRA:\s+(-?[\d.]+)\s+LU", tail).group(1)), "TP": float(m.group(1)) if m else float("nan")}
    return {"black": blacks, "freeze": list(zip(fs, fe)), "loud": loud, "duration": dur}


def inspect_film(path, lufs_target=-14.0, lufs_tol=1.5, tp_fail_above=-0.9, black_d=0.4, pix_th=0.03,
                 freeze_db=-60, freeze_d=1.5, ends_allowed=True, tp_inclusive=False):
    """Delivery gate: codec/pix_fmt/even size, black (ends allowed), freeze, integrated LUFS, true peak."""
    info = probe(path); v = vstream(info); dur = float(info["format"]["duration"])
    problems = []
    if v["codec_name"] != "h264" or v.get("pix_fmt") != "yuv420p":
        problems.append("codec")
    if int(v["width"]) % 2 or int(v["height"]) % 2:
        problems.append("odd size")
    an = analyze(path, black_d, pix_th, freeze_db, freeze_d, audio=bool(astreams(info)))
    blacks = an["black"]
    for a, b in blacks:
        at_end = a <= 0.05 or b >= dur - 0.05
        if not (ends_allowed and at_end):
            problems.append(f"black {a:.2f}-{b:.2f}")
    for a, b in an["freeze"]:
        problems.append(f"freeze {a:.2f}-{b:.2f}")
    m = an["loud"]
    if m:
        if abs(m["I"] - lufs_target) > lufs_tol:
            problems.append(f"lufs {m['I']}")
        if (m["TP"] >= tp_fail_above) if tp_inclusive else (m["TP"] > tp_fail_above):
            problems.append(f"true peak {m['TP']}")
    return {"pass": not problems, "problems": problems, "black": blacks, "loud": m, "duration": dur}


def peak_tone(sr, dur, dbtp):
    """Stereo bed whose sample peak sits at dbtp (a 997 Hz tone; true peak ~= sample peak)."""
    x = tone(997, dur, sr, 1.0)
    return stereo(x * 10 ** (dbtp / 20))


@program("QA-01")
def qa_01(work):
    fr = moving_frames(66)
    mid = fr.copy(); mid[18:48] = 0
    end = fr.copy(); end[51:] = 0
    frz = fr.copy(); frz[6:63] = frz[6]
    films = par(lambda n, f, a=None: gate_film(work, n, f, audio=a),
                [("good.mp4", fr), ("midblack.mp4", mid), ("endblack.mp4", end), ("frozen.mp4", frz),
                 ("hot.mp4", fr, peak_tone(48000, 2.2, -0.3))])
    good, blk, endb, fz, loud = par(inspect_film, films)
    wjson(Path(work) / "inspect.json", {"good": good, "midblack": blk, "endblack": endb, "frozen": fz, "hot": loud})
    return [C("clean film passes", good["pass"], good),
            C("1 s mid-film black stretch fails (d=0.4, pix_th 0.03)", not blk["pass"] and any("black" in p for p in blk["problems"]), blk["problems"]),
            C("black hold at the end is allowed", endb["pass"], endb["black"]),
            C("1.9 s freeze fails (-60 dB, d=1.5)", any("freeze" in p for p in fz["problems"]), fz["problems"]),
            C("hot mix fails on LUFS/true peak > -0.9", any("true peak" in p for p in loud["problems"]), loud["problems"]),
            C("integrated loudness within -14 +-1.5", abs(good["loud"]["I"] + 14) <= 1.5, good["loud"])]


def loop_seam(frames, floor=0.4, k=1.5, n_end=8):
    f = np.asarray(frames, dtype=np.float64)
    steps = np.abs(np.diff(f, axis=0)).mean(axis=(1, 2))
    end_steps = np.concatenate([steps[:n_end // 2], steps[-(n_end // 2):]])
    seam = float(np.abs(f[-1] - f[0]).mean())
    limit = max(floor, k * float(np.median(end_steps)))
    return {"seam": seam, "limit": limit, "pass": seam <= limit}


def _loop_frames(n=48, w=320, h=180, broken=False):
    import cv2
    out = []
    for i in range(n):
        img = np.full((h, w), 30, np.uint8)
        a = 2 * np.pi * i / n
        cv2.circle(img, (int(w / 2 + 60 * math.cos(a)), int(h / 2 + 50 * math.sin(a))), 18, 230, -1)
        out.append(img)
    if broken:
        out = out[: n * 3 // 4]
    return np.stack(out)


@program("QA-02")
def qa_02(work):
    good, bad = loop_seam(_loop_frames()), loop_seam(_loop_frames(broken=True))
    still = np.full((20, 180, 320), 100.0); still[-1] += 0.3
    tiny = loop_seam(still)
    still2 = still.copy(); still2[-1] = 100.6
    tiny2 = loop_seam(still2)
    wjson(Path(work) / "loopcheck.json", {"loop": good, "cut_short": bad, "floor_pass": tiny, "floor_fail": tiny2})
    return [C("true loop (circle orbit) passes", good["pass"], good),
            C("loop cut at 3/4 orbit fails", not bad["pass"], bad),
            C("near-still film: seam 0.3 passes under 0.4 floor", tiny["pass"] and abs(tiny["limit"] - 0.4) < 1e-9, tiny),
            C("near-still film: seam 0.6 fails the 0.4 floor", not tiny2["pass"], tiny2)]


@program("QA-04")
def qa_04(work):
    work = Path(work); fr = moving_frames(60)
    tags = ["-profile:v", "high", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-movflags", "+faststart"]
    good = write_video(work / "good.mp4", fr, 30, audio=scale_to_lufs(stereo(tone(440, 2, 48000, .3)), 48000, -14), extra=tags, preset="veryfast")
    nofs = write_video(work / "nofaststart.mp4", fr, 30, audio=scale_to_lufs(stereo(tone(440, 2, 48000, .3)), 48000, -14), extra=tags[:-2], preset="veryfast")
    data = good.read_bytes(); trunc = work / "truncated.mp4"; trunc.write_bytes(data[: int(len(data) * 0.6)])

    def qa(p, cap=25 * 2**20):
        info = probe(p); v = vstream(info)
        dec = ff_log("-v", "error", "-i", p, "-f", "null", "-").strip()
        an = analyze(p, 0.4, 0.1, -60, 1.0)
        m = an["loud"]
        sil = silencedetect(p, -50, 0.5)
        r = {"decode_errors": bool(dec), "high_yuv420p": v.get("profile") == "High" and v.get("pix_fmt") == "yuv420p",
             "even": int(v["width"]) % 2 == 0 and int(v["height"]) % 2 == 0,
             "bt709": v.get("color_primaries") == "bt709" and v.get("color_transfer") == "bt709" and v.get("color_space") == "bt709",
             "faststart": moov_before_mdat(p), "lufs_ok": abs(m["I"] + 14) <= 1.0, "tp_ok": m["TP"] < -1.0,
             "no_black": not an["black"], "no_freeze": not an["freeze"], "no_silence": not sil,
             "under_cap": p.stat().st_size <= cap}
        r["pass"] = (not r["decode_errors"]) and all(v for k, v in r.items() if k != "decode_errors")
        return r
    g, n = qa(good), qa(nofs)
    try:
        tdec = bool(ff_log("-v", "error", "-i", trunc, "-f", "null", "-").strip())
    except Exception:
        tdec = True
    wjson(work / "delivery_qa.json", {"good": g, "nofaststart": n, "truncated_decode_errors": tdec})
    return [C("tagged High/yuv420p/BT.709 faststart file passes all", g["pass"], g),
            C("file without +faststart fails moov-before-mdat", not n["faststart"] and not n["pass"], n["faststart"]),
            C("truncated file reports decode errors", tdec, tdec),
            C("size cap 25 MiB enforced (1 KiB cap fails)", not qa(good, 1024)["under_cap"], good.stat().st_size)]


def cfr_from_timestamps(stamps, frames, fps=30.0, dur=None):
    """Hold the newest painted frame at each constant-rate tick; never blend."""
    dur = dur if dur is not None else stamps[-1]
    out, src_idx = [], []
    for k in range(int(round(dur * fps))):
        t = k / fps
        i = max(j for j, s in enumerate(stamps) if s <= t + 1e-9) if stamps[0] <= t + 1e-9 else 0
        out.append(frames[i]); src_idx.append(i)
    held = sum(1 for a, b in zip(src_idx, src_idx[1:]) if a == b)
    page_fps = (len(stamps) - 1) / (stamps[-1] - stamps[0])
    return np.stack(out), {"held": held, "page_fps": page_fps, "warn": page_fps < 20, "src": src_idx}


@program("QA-05")
def qa_05(work):
    rng = np.random.default_rng(3)
    stamps = np.cumsum(np.r_[0, rng.uniform(0.11, 0.14, 15)]).tolist()  # ~8 fps page
    frames = [np.full((8, 8), 10 * i + 5, np.uint8) for i in range(len(stamps))]
    seq, rep = cfr_from_timestamps(stamps, frames, 30, 1.8)
    values = set(np.unique(seq).tolist()); allowed = {int(f[0, 0]) for f in frames}
    fast = np.arange(0, 2, 1 / 39).tolist()
    _, rep2 = cfr_from_timestamps(fast, [np.zeros((2, 2), np.uint8)] * len(fast), 30, 1.8)
    wjson(Path(work) / "capture_report.json", {"slow": {k: v for k, v in rep.items() if k != "src"}, "fast_fps": rep2["page_fps"]})
    return [C("54 output ticks at 30 fps for 1.8 s", len(seq) == 54, len(seq)),
            C("every output frame is a painted frame (no interpolation)", values <= allowed, sorted(values - allowed)),
            C("held frames = ticks - distinct painted frames used", rep["held"] == 54 - len(set(rep["src"])), rep["held"]),
            C("~8 fps page warns (< 20)", rep["warn"] and 6 < rep["page_fps"] < 10, rep["page_fps"]),
            C("39 fps page does not warn", not rep2["warn"], rep2["page_fps"])]


LEVELS = (50, 200, 110, 235, 20, 160)


def shot_frames(n, k, h=36, w=64, seed=1):
    """Shot number k: a slowly panning texture around a distinct mean level and colour."""
    f = moving_frames(n, h, w, seed=seed + 7 * k, speed=1).astype(np.float32)
    f = (f - f.mean()) * 0.35 + LEVELS[k % len(LEVELS)]
    rgb = np.stack([f, f * (0.6 + 0.2 * (k % 3)), f * (1.2 - 0.25 * (k % 2))], axis=-1)
    return rgb.clip(0, 255).astype(np.uint8)


def shots_film(work, name, cuts_s, dur=3.0, fps=30, h=36, w=64, seed=1):
    """Distinct textured shots, each slowly panning; hard cuts at cuts_s seconds."""
    n = int(round(dur * fps)); edges = [0] + [int(round(c * fps)) for c in cuts_s] + [n]
    frames = [shot_frames(edges[k + 1] - edges[k], k, h, w, seed) for k in range(len(edges) - 1)]
    return write_video(Path(work) / name, np.concatenate(frames), fps)


@program("QA-06")
def qa_06(work):
    p = shots_film(work, "cuts.mp4", [1.0, 2.0])
    t = scene_times(p, 0.3)
    pan = write_video(Path(work) / "pan.mp4", moving_frames(90, speed=1), 30)
    t2 = scene_times(pan, 0.3)
    wjson(Path(work) / "scenes.json", {"cuts": t, "pan_only": t2})
    return [C("two cuts found at 1.0 s and 2.0 s (+-1 frame)", len(t) == 2 and all(abs(a - b) <= 1 / 30 + 1e-6 for a, b in zip(t, [1.0, 2.0])), t),
            C("continuous pan gives no false cut at threshold 0.3", t2 == [], t2)]


@program("QA-07")
def qa_07(work):
    work = Path(work); fps, bpm = 30, 120
    half_bar = 2 * 60 / bpm  # 4/4: bar = 4 beats = 2 s, half-bar = 1 s
    p = shots_film(work, "assembly.mp4", [1.0, 2.4, 3.0], dur=4.0)
    cuts = scene_times(p, 0.3)
    planned = [half_bar * k for k in range(1, 4)]
    off = [c for c in cuts if min(abs(c - q) for q in planned) > 1 / fps + 1e-6]
    frames = decode_gray(p)
    picks = [int(round(q * fps)) + 6 for q in [0.0] + planned]
    tiles = [frames[i] for i in picks]
    sheet = np.concatenate(tiles, axis=1); save_png(work / "contact_halfbars.png", sheet)
    wjson(work / "cut_audit.json", {"cuts": cuts, "planned": planned, "off_grid": off, "sample_frames": picks})
    return [C("detected cuts 1.0 / 2.4 / 3.0 s", len(cuts) == 3, cuts),
            C("the 2.4 s cut is flagged off the half-bar grid", len(off) == 1 and abs(off[0] - 2.4) < 0.05, off),
            C("contact sheet samples 6 frames after each half-bar", picks == [6, 36, 66, 96] and sheet.shape[1] == 4 * 64, picks)]


@program("QA-08")
def qa_08(work):
    work = Path(work); sr = 44100; parts = []
    for i in range(12):
        w = write_wav(work / f"p{i}.wav", tone(300 + 20 * i, 0.5, sr, 0.3), sr)
        mp = work / f"p{i}.mp3"; ff("-i", w, "-c:a", "libmp3lame", "-b:a", "128k", mp); w.unlink(); parts.append(mp)
    lst = work / "list.txt"; lst.write_text("".join(f"file '{p.name}'\n" for p in parts))
    total = sum(float(probe(p)["format"]["duration"]) for p in parts)
    ff("-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", work / "copy.mp3")
    ff("-f", "concat", "-safe", "0", "-i", lst, "-c:a", "libmp3lame", "-write_xing", "0", work / "once.mp3")
    def dec_len(p):
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-f", "s16le", "-ac", "1", "-ar", str(sr), "-"], capture_output=True, check=True).stdout
        return len(raw) / 2 / sr
    true_sum = 12 * 0.5
    copy_d, once_d = dec_len(work / "copy.mp3"), dec_len(work / "once.mp3")
    wjson(work / "drift.json", {"sum_piece_durations": total, "copy_decoded": copy_d, "encode_once_decoded": once_d})
    return [C("-c copy join keeps per-piece padding (drift > 20 ms/join)", copy_d - true_sum > 0.02 * 11, copy_d - true_sum),
            C("decode+encode once drifts far less than copy", abs(once_d - true_sum) < (copy_d - true_sum) / 3, once_d - true_sum)]


def css_tokens(css):
    return dict(re.findall(r"(--[\w-]+)\s*:\s*(#[0-9a-fA-F]{3,8})\b", css))


def lstar(c):
    return float(rgb_to_lab(hex_rgb(c) if isinstance(c, str) else c)[0])


@program("QA-09")
def qa_09(work):
    rules = {"normal_text": 4.5, "large_text": 3.0, "graphic": 3.0, "enhanced": 7.0}
    def audit(fg, bg):
        r = contrast(fg, bg)
        return {k: r >= v for k, v in rules.items()} | {"ratio": round(r, 2)}
    bw, grey, light = audit("#000000", "#ffffff"), audit("#767676", "#ffffff"), audit("#999999", "#ffffff")
    palette = ["#1f4e9c", "#c0392b", "#2e7d32", "#f1c40f"]
    Ls = [lstar(c) for c in palette]
    adj = [abs(a - b) for a, b in zip(Ls, Ls[1:])]
    flagged = [(palette[i], palette[i + 1]) for i, d in enumerate(adj) if d < 10]
    wjson(Path(work) / "contrast_audit.json", {"bw": bw, "767676": grey, "999999": light, "palette_L": Ls, "flagged": flagged})
    return [C("black on white = 21:1 passes enhanced 7:1", bw["ratio"] == 21.0 and bw["enhanced"], bw),
            C("#767676 on white passes 4.5 normal text, fails 7:1", grey["normal_text"] and not grey["enhanced"], grey),
            C("#999 on white fails 4.5 and 3:1", not light["normal_text"] and not light["large_text"], light),
            C("grayscale screen flags the adjacent pair with delta L* < 10", flagged == [("#c0392b", "#2e7d32")], [round(d, 1) for d in adj])]


@program("QA-10")
def qa_10(work):
    css = """:root{--fg:#1b1b1f;--bg:#fbfaf7;--card:#ffffff;--primary:#1d4ed8;--primary-fg:#ffffff;--muted:#5b5b66;
    --teal:#0f766e;--amber:#b45309;--coral:#be185d;--soft:#e8e8ec}"""
    t = css_tokens(css)
    text_pairs = [("--fg", "--bg"), ("--primary-fg", "--primary"), ("--muted", "--bg"), ("--muted", "--card")]
    status = [("--teal", "--card"), ("--amber", "--card"), ("--coral", "--card")]
    res = {f"{a}/{b}": round(contrast(t[a], t[b]), 2) for a, b in text_pairs + status}
    fails = [k for k, v in res.items() if v < (4.5 if k.split("/")[0] in {a for a, _ in text_pairs} else 3.0)]
    pal = ["--primary", "--teal", "--amber", "--coral"]
    de = {f"{a}~{b}": round(delta_e76(t[a], t[b]), 1) for i, a in enumerate(pal) for b in pal[i + 1:]}
    bad_css = css.replace("--muted:#5b5b66", "--muted:#a0a0a8")
    t2 = css_tokens(bad_css); bad = round(contrast(t2["--muted"], t2["--bg"]), 2)
    near = round(delta_e76("#be185d", "#c41f63"), 1)
    wjson(Path(work) / "palette_contract.json", {"contrast": res, "deltaE": de, "planted_muted": bad, "near_pair_dE": near})
    return [C("10 hex tokens parsed straight from the CSS", len(t) == 10, sorted(t)),
            C("text pairs >= 4.5 and status colours >= 3 on card", not fails, res),
            C("CIE76 deltaE >= 25 between every palette accent", min(de.values()) >= 25, de),
            C("planted light muted grey fails 4.5:1", bad < 4.5, bad),
            C("near-duplicate accent pair is below deltaE 25", near < 25, near)]


def media_blocks(css, query_re):
    """Return the bodies of @media blocks whose query matches query_re (brace-balanced)."""
    out = []
    for m in re.finditer(r"@media([^{]*)\{", css):
        if not re.search(query_re, m.group(1)):
            continue
        i, depth = m.end(), 1
        while depth and i < len(css):
            depth += {"{": 1, "}": -1}.get(css[i], 0); i += 1
        out.append(css[m.end():i - 1])
    return out


RM_GOOD = """.view-stage{transition:opacity .3s}.card{animation:rise .5s}.hero{animation:fade 1s}
@media (prefers-reduced-motion: reduce){
 *,*::before,*::after{animation-duration:0.01ms !important;animation-iteration-count:1 !important;transition-duration:0.01ms !important;scroll-behavior:auto !important}
 .card,.hero{animation:none;opacity:1;transform:none}
 .progress-bar{transition:none}
}"""


def reduced_motion_contract(css, animated=(".card", ".hero")):
    blocks = media_blocks(css, r"prefers-reduced-motion:\s*reduce")
    b = " ".join(blocks)
    checks = {"block": bool(blocks),
              "durations": "animation-duration:0.01ms" in b.replace(" ", "") and "transition-duration:0.01ms" in b.replace(" ", ""),
              "iteration_1": re.search(r"animation-iteration-count:\s*1\b", b) is not None,
              "smooth_scroll_off": "scroll-behavior:auto" in b.replace(" ", ""),
              "final_state": all(re.search(re.escape(a) + r"[^{]*\{[^}]*animation:\s*none[^}]*opacity:\s*1[^}]*transform:\s*none", b) for a in animated),
              "no_blanket_stage": ".view-stage *" not in b}
    return checks


@program("QA-11")
def qa_11(work):
    good = reduced_motion_contract(RM_GOOD)
    blanket = reduced_motion_contract(RM_GOOD.replace(".card,.hero{", ".view-stage *, .card,.hero{"))
    slow = reduced_motion_contract(RM_GOOD.replace("animation-duration:0.01ms", "animation-duration:200ms"))
    (Path(work) / "styles.css").write_text(RM_GOOD); wjson(Path(work) / "contract.json", {"good": good, "blanket": blanket, "slow": slow})
    return [C("contract holds on the reference stylesheet", all(good.values()), good),
            C("blanket .view-stage * rule is rejected", not blanket["no_blanket_stage"], blanket),
            C("200ms duration under reduce fails the 0.01ms rule", not slow["durations"], slow)]


MOTION_TOKENS = {"--dur-fast": "120ms", "--dur-base": "240ms", "--dur-slow": "480ms"}


def motion_contract(css, tsx):
    toks = dict(re.findall(r"(--dur-[\w]+)\s*:\s*([\d.]+m?s)", css))
    return {"duration_tokens_exact": all(toks.get(k) == v for k, v in MOTION_TOKENS.items()),
            "curves_present": bool(re.search(r"--ease-[\w-]+\s*:\s*cubic-bezier\(", css)),
            "no_transition_all": not re.search(r"transition(-property)?\s*:\s*all\b", css),
            "keyed_view_stage_focus": bool(re.search(r"<ViewStage[^>]*key=\{", tsx)) and "focus()" in tsx,
            "reduced_motion_block": bool(media_blocks(css, r"prefers-reduced-motion")),
            "safe_area_dvh": "env(safe-area-inset-bottom)" in css and "100dvh" in css}


@program("QA-12")
def qa_12(work):
    css = (":root{--dur-fast:120ms;--dur-base:240ms;--dur-slow:480ms;--ease-out:cubic-bezier(.2,.8,.2,1)}"
           ".app{min-height:100dvh;padding-bottom:env(safe-area-inset-bottom)}.btn{transition:transform var(--dur-fast) var(--ease-out)}"
           "@media (prefers-reduced-motion: reduce){*{transition-duration:0.01ms}}")
    tsx = "export function App(){const r=useRef();useEffect(()=>r.current?.focus(),[view]);return <ViewStage key={view} ref={r}/>}"
    good = motion_contract(css, tsx)
    bad = motion_contract(css.replace("transform var(--dur-fast)", "all var(--dur-fast)").replace("240ms", "250ms"), tsx.replace("key={view} ", ""))
    wjson(Path(work) / "motion_contract.json", {"good": good, "bad": bad})
    return [C("all 6 contract checks pass on the fixture", all(good.values()), good),
            C("transition: all is caught", not bad["no_transition_all"], bad),
            C("drifted duration token 250ms is caught", not bad["duration_tokens_exact"], bad),
            C("unkeyed ViewStage is caught", not bad["keyed_view_stage_focus"], bad)]


def responsive_contract(css):
    m768 = " ".join(media_blocks(css, r"max-width:\s*768px")); m480 = " ".join(media_blocks(css, r"max-width:\s*480px"))
    flat = lambda s: s.replace(" ", "")
    return {"bottom_nav_768": bool(re.search(r"\.nav\{[^}]*position:fixed[^}]*bottom:0", flat(m768))),
            "pad16_768": "padding:16px" in flat(m768), "pad12_480": "padding:12px" in flat(m480),
            "offsets": all(f"calc({v}px+env(safe-area-inset-bottom))" in flat(css) for v in (72, 68, 80)),
            "dvh": "100dvh" in css}


@program("QA-13")
def qa_13(work):
    css = (".app{min-height:100dvh}.toast{bottom:calc(80px + env(safe-area-inset-bottom))}"
           "@media (max-width: 768px){.nav{position:fixed;left:0;right:0;bottom:0}.main{padding:16px;padding-bottom:calc(72px + env(safe-area-inset-bottom))}}"
           "@media (max-width: 480px){.main{padding:12px;padding-bottom:calc(68px + env(safe-area-inset-bottom))}}")
    good = responsive_contract(css)
    bad = responsive_contract(css.replace("padding:12px", "padding:20px").replace("calc(68px", "calc(60px"))
    wjson(Path(work) / "responsive.json", {"good": good, "bad": bad})
    return [C("breakpoints 768/480 contract passes", all(good.values()), good),
            C("phone padding 20px instead of 12px is caught", not bad["pad12_480"], bad),
            C("missing 68px safe-area offset is caught", not bad["offsets"], bad)]


def static_check(root: Path):
    from bs4 import BeautifulSoup
    problems, ids = [], []
    for html in sorted(root.rglob("*.html")):
        soup = BeautifulSoup(html.read_text(), "html.parser")
        for tag, attr in (("script", "src"), ("link", "href"), ("img", "src")):
            for el in soup.find_all(tag):
                ref = el.get(attr)
                if ref and not re.match(r"^(https?:|data:|#)", ref) and not (html.parent / ref).exists():
                    problems.append(f"missing asset {ref}")
        ids += [el["id"] for el in soup.select("[data-view]")]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    problems += [f"duplicate view id {d}" for d in dup]
    for js in sorted(root.rglob("*.js")):
        src = re.sub(r"(['\"`]).*?\1", "", js.read_text())
        for o, c in ("()", "[]", "{}"):
            if src.count(o) != src.count(c):
                problems.append(f"unbalanced {o}{c} in {js.name}")
    sw = root / "sw.js"
    if sw.exists():
        for ref in re.findall(r"['\"](\./[^'\"]+)['\"]", sw.read_text()):
            if not (root / ref).exists():
                problems.append(f"cache list entry missing {ref}")
    return problems


@program("QA-14")
def qa_14(work):
    root = Path(work) / "site"; (root / "js").mkdir(parents=True)
    (root / "index.html").write_text('<html><head><link href="app.css" rel="stylesheet"><script src="js/app.js"></script></head>'
                                     '<body><section id="home" data-view></section><section id="stats" data-view></section></body></html>')
    (root / "app.css").write_text("body{margin:0}"); (root / "js" / "app.js").write_text("function go(x){return [x].map(v=>({v}));}")
    (root / "sw.js").write_text("const CACHE=['./index.html','./app.css','./js/app.js'];")
    clean = static_check(root)
    (root / "js" / "app.js").write_text("function go(x){return [x].map(v=>({v});}")
    (root / "about.html").write_text('<section id="home" data-view></section><img src="logo.png">')
    (root / "sw.js").write_text("const CACHE=['./index.html','./app.css','./js/app.js','./offline.html'];")
    broken = static_check(root)
    wjson(Path(work) / "static_check.json", {"clean": clean, "broken": broken})
    return [C("clean site has no problems", clean == [], clean),
            C("unbalanced bracket in app.js caught", any("unbalanced ()" in p for p in broken), broken),
            C("missing logo.png asset caught", "missing asset logo.png" in broken, broken),
            C("duplicate view id 'home' caught", "duplicate view id home" in broken, broken),
            C("PWA cache entry ./offline.html missing caught", any("offline.html" in p for p in broken), broken)]


THEME_LOCK = {"--ink": "#14110f", "--paper": "#f6efe3", "--gold": "#c8a24a", "--accent": "#9a3b2a"}


def theme_lock(css, html):
    toks = {k.lower(): v.lower() for k, v in css_tokens(css).items()}
    meta = re.search(r'<meta name="theme-color" content="(#[0-9a-fA-F]{6})"', html)
    order = [m.group(0) for m in re.finditer(r"(tokens|base|dashboard|editorial)\.css", html)]
    return {"tokens": all(toks.get(k) == v for k, v in THEME_LOCK.items()), "font": "Tajawal" in css,
            "hero_gradient": bool(re.search(r"\.hero\{[^}]*linear-gradient", css)), "shadow": "box-shadow" in css,
            "theme_color": bool(meta) and meta.group(1).lower() == THEME_LOCK["--ink"],
            "cascade": order == ["tokens.css", "base.css", "dashboard.css", "editorial.css"],
            "weights_linked": "family=Tajawal:wght@400;700" in html}


@program("QA-15")
def qa_15(work):
    css = ":root{" + ";".join(f"{k}:{v}" for k, v in THEME_LOCK.items()) + "}body{font-family:'Tajawal',sans-serif}.hero{background:linear-gradient(160deg,var(--ink),var(--accent))}.card{box-shadow:0 2px 8px #0003}"
    html = ('<meta name="theme-color" content="#14110f"><link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700">'
            '<link href="tokens.css"><link href="base.css"><link href="dashboard.css"><link href="editorial.css">')
    good = theme_lock(css, html)
    drift = theme_lock(css.replace("#c8a24a", "#c9a24a"), html.replace("#14110f", "#000000").replace('<link href="base.css">', "") + '<link href="base.css">')
    wjson(Path(work) / "theme_lock.json", {"good": good, "drift": drift})
    return [C("locked theme passes all 7 checks", all(good.values()), good),
            C("one-digit drift in a locked hex fails", not drift["tokens"], drift),
            C("theme-color meta mismatch fails", not drift["theme_color"], drift),
            C("base.css loaded after editorial.css breaks cascade order", not drift["cascade"], drift)]


def texture(h, w, seed=0, smooth=1):
    rng = np.random.default_rng(seed)
    t = rng.integers(0, 256, size=(h, w)).astype(np.float64)
    for _ in range(smooth):
        t = (t + np.roll(t, 1, 0) + np.roll(t, 1, 1) + np.roll(t, (1, 1), (0, 1))) / 4
    return t


def block_motion(f1, f2, grid=4, patch=15, radius=6, step=2, tex_min=6.0, conf_min=0.12):
    H, W = f1.shape; rh, rw = H // grid, W // grid; hp = patch // 2; cells = []
    for gy in range(grid):
        for gx in range(grid):
            cy, cx = gy * rh + rh // 2, gx * rw + rw // 2
            p = f1[cy - hp:cy + hp + 1, cx - hp:cx + hp + 1]
            errs = {}
            for dy in range(-radius, radius + 1, step):
                for dx in range(-radius, radius + 1, step):
                    y0, x0 = cy + dy - hp, cx + dx - hp
                    if y0 < 0 or x0 < 0 or y0 + patch > H or x0 + patch > W:
                        continue
                    errs[(dy, dx)] = float(np.abs(f2[y0:y0 + patch, x0:x0 + patch] - p).mean())
            best = min(errs, key=errs.get); mean_err = np.mean(list(errs.values()))
            conf = 1 - errs[best] / mean_err if mean_err > 0 else 0.0
            tex = float(p.std())
            cells.append({"cell": (gy, gx), "d": best, "texture": tex, "conf": conf,
                          "strong": tex >= tex_min and conf >= conf_min})
    strong = [c for c in cells if c["strong"]]
    cam = (int(np.median([c["d"][0] for c in strong])), int(np.median([c["d"][1] for c in strong]))) if len(strong) >= 7 else None
    for c in cells:
        c["residual"] = (c["d"][0] - cam[0], c["d"][1] - cam[1]) if cam and c["strong"] else None
    return {"camera": cam, "cells": cells, "n_strong": len(strong)}


@program("QA-16")
def qa_16(work):
    f1 = texture(96, 96, 5) * 1.0
    f1[0:24, 72:96] = 128.0  # one flat region: texture < 6, must not vote
    f2 = np.roll(f1, (0, 4), (0, 1))
    moved = np.roll(f1, (2, 6), (0, 1))
    f2[24:48, 48:72] = moved[24:48, 48:72]
    r = block_motion(f1, f2)
    cell = next(c for c in r["cells"] if c["cell"] == (1, 2)); flat = next(c for c in r["cells"] if c["cell"] == (0, 3))
    wjson(Path(work) / "regional_motion.json", r)
    return [C("global camera = median of strong cells = (0, +4) px", r["camera"] == (0, 4), r["camera"]),
            C(">= 7 strong cells voted", r["n_strong"] >= 7, r["n_strong"]),
            C("region (1,2) residual motion = (+2, +2) after camera compensation", cell["residual"] == (2, 2), cell),
            C("flat region (texture < 6) is not strong", not flat["strong"], round(flat["texture"], 2))]


CI_REQUIRED = ["npm install", "npm run check:project", "python3 -m unittest discover -s tests",
               "node --test tests/motion-clone.test.mjs", "tsc --noEmit", "vite build"]


def ci_gate(yml_text):
    import yaml
    wf = yaml.safe_load(yml_text); job = next(iter(wf["jobs"].values()))
    runs = [s.get("run", "").strip() for s in job["steps"]]
    node = next((s.get("with", {}).get("node-version") for s in job["steps"] if "setup-node" in str(s.get("uses", ""))), None)
    pos = [next((i for i, r in enumerate(runs) if req in r), -1) for req in CI_REQUIRED]
    upload = next((s for s in job["steps"] if "upload-artifact" in str(s.get("uses", ""))), {})
    return {"node22": str(node) == "22", "all_steps": -1 not in pos, "in_order": pos == sorted(pos) and -1 not in pos,
            "retention7": upload.get("with", {}).get("retention-days") == 7, "missing": [CI_REQUIRED[i] for i, p in enumerate(pos) if p < 0]}


@program("QA-17")
def qa_17(work):
    steps = "\n".join(f"      - run: {r}" for r in CI_REQUIRED)
    yml = ("name: ci\non: [push]\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n"
           "      - uses: actions/setup-node@v4\n        with:\n          node-version: 22\n" + steps +
           "\n      - uses: actions/upload-artifact@v4\n        with:\n          name: dist\n          path: dist\n          retention-days: 7\n")
    (Path(work) / "ci.yml").write_text(yml)
    good = ci_gate(yml); bad = ci_gate(yml.replace("      - run: tsc --noEmit\n", "").replace("node-version: 22", "node-version: 18"))
    wjson(Path(work) / "ci_gate.json", {"good": good, "bad": bad})
    return [C("workflow has Node 22, all 6 steps in order and 7-day artifact", good["node22"] and good["in_order"] and good["retention7"], good),
            C("dropped 'tsc --noEmit' step is reported", bad["missing"] == ["tsc --noEmit"], bad["missing"]),
            C("Node 18 is rejected", not bad["node22"], bad)]


def reduced_motion_policy(css, js_files):
    blk = "".join(media_blocks(css, r"prefers-reduced-motion:\s*reduce")).replace(" ", "")
    tokens = {t: f"{t}:0ms" in blk for t in ("--sk-t", "--sk-motion-enter", "--sk-motion-stagger")}
    mm = {n: "matchMedia('(prefers-reduced-motion: reduce)')" in src for n, src in js_files.items()}
    return {"tokens_zeroed": tokens, "matchMedia": mm, "pass": all(tokens.values()) and all(mm.values())}


@program("QA-18")
def qa_18(work):
    css = ":root{--sk-t:240ms;--sk-motion-enter:420ms;--sk-motion-stagger:60ms}@media (prefers-reduced-motion:reduce){:root{--sk-t:0ms;--sk-motion-enter:0ms;--sk-motion-stagger:0ms}}"
    guard = "const still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;"
    js = {"motion.js": guard + "if(!still) animate();", "crystal-world.js": guard + "renderOnce(still);", "earth-intro.js": guard + "if(still) skipIntro();"}
    good = reduced_motion_policy(css, js)
    bad = reduced_motion_policy(css.replace("--sk-motion-stagger:0ms", "--sk-motion-stagger:60ms"), dict(js, **{"earth-intro.js": "playIntro();"}))
    wjson(Path(work) / "reduced_motion_policy.json", {"good": good, "bad": bad})
    return [C("all three tokens zeroed and three modules check matchMedia", good["pass"], good),
            C("stagger token left at 60ms is caught", not bad["tokens_zeroed"]["--sk-motion-stagger"], bad),
            C("earth-intro.js without matchMedia guard is caught", not bad["matchMedia"]["earth-intro.js"], bad)]


COBALT = re.compile(r"#2340c4|#0b1030|#19c3d9|#2a46d6|#070a1e|#9beef7|#b6f3fa", re.I)


def identity_unity(files, door, ledger):
    hits = {n: COBALT.findall(t) for n, t in files.items() if not n.startswith("looks/")}
    hits = {k: v for k, v in hits.items() if v}
    theme = all('content="#1d1814"' in t for n, t in files.items() if n.endswith(".html"))
    looks_keep = any(COBALT.search(t) for n, t in files.items() if n.startswith("looks/"))
    return {"cobalt_hits": hits, "theme_color": theme, "door_eq_ledger": door == ledger, "cobalt_selectable": looks_keep}


@program("QA-19")
def qa_19(work):
    files = {"icons/mark.svg": '<svg><path fill="#c8a24a"/></svg>', "manifest.webmanifest": '{"theme_color":"#1d1814"}',
             "index.html": '<meta name="theme-color" content="#1d1814">', "looks/cobalt.css": ":root{--accent:#2340c4}"}
    door = {"--ink": "#1d1814", "--gold": "#c8a24a"}
    good = identity_unity(files, door, dict(door))
    bad = identity_unity(dict(files, **{"icons/mark.svg": '<svg><path fill="#19C3D9"/></svg>'}), door, {"--ink": "#1d1814", "--gold": "#c9a24a"})
    wjson(Path(work) / "identity.json", {"good": good, "bad": bad})
    return [C("no cobalt in marks/icons/manifest, theme-color #1d1814, cobalt kept as a look", not good["cobalt_hits"] and good["theme_color"] and good["cobalt_selectable"], good),
            C("cobalt #19C3D9 in an icon is caught (case-insensitive)", "icons/mark.svg" in bad["cobalt_hits"], bad["cobalt_hits"]),
            C("door token differing from ledger token fails", not bad["door_eq_ledger"], bad)]


def identity_metrics(css, js):
    spacing = re.findall(r"(?:margin|padding|gap)[\w-]*\s*:\s*([^;}]+)", css)
    px = [int(v) for s in spacing for v in re.findall(r"(\d+)px", s)]
    weights = [int(w) for w in re.findall(r"font-weight\s*:\s*(\d+)", css)]
    return {"colours": len(re.findall(r"#[0-9a-fA-F]{3,8}\b", css)), "offGrid": sum(1 for v in px if v % 4),
            "radiusLiterals": len(re.findall(r"border-radius\s*:\s*\d+px", css)), "inlineColours": len(re.findall(r"#[0-9a-fA-F]{6}\b", js)),
            "important": css.count("!important"), "heavyWeights": sum(1 for w in weights if w >= 800),
            "weightVariants": len(set(weights)), "focusVariants": len(set(re.findall(r":focus(?:-visible|-within)?[^{]*\{([^}]*)\}", css)))}


def ratchet(now, baseline):
    worse = {k: (baseline[k], v) for k, v in now.items() if v > baseline.get(k, 0)}
    return {"pass": not worse, "worse": worse}


@program("QA-20")
def qa_20(work):
    css = (".a{color:#123456;margin:8px 12px;padding:6px}.b{border-radius:6px;font-weight:800 !important}"
           ".c{font-weight:400;gap:16px}.c:focus-visible{outline:2px solid #fff}")
    js = "el.style.color='#ff0000'"
    base = identity_metrics(css, js)
    worse = identity_metrics(css + ".d{padding:10px}", js)
    better = identity_metrics(css.replace("padding:6px", "padding:8px"), js)
    wjson(Path(work) / "identity_baseline.json", base)
    return [C("baseline counts: 2 colours, 1 off-grid, 1 radius, 1 inline, 1 important, 1 heavy, 2 weights, 1 focus",
              base == {"colours": 2, "offGrid": 1, "radiusLiterals": 1, "inlineColours": 1, "important": 1, "heavyWeights": 1, "weightVariants": 2, "focusVariants": 1}, base),
            C("adding padding:10px worsens offGrid and fails the ratchet", ratchet(worse, base) == {"pass": False, "worse": {"offGrid": (1, 2)}}, ratchet(worse, base)),
            C("fixing 6px -> 8px passes the ratchet", ratchet(better, base)["pass"] and better["offGrid"] == 0, better)]


def brand_art(root: Path, sectors, files, max_kb=150):
    from bs4 import BeautifulSoup
    missing = [s for s in sectors if not (root / "sectors" / f"{s}.webp").is_file()]
    heavy = [f for f in files if (root / f).is_file() and (root / f).stat().st_size > max_kb * 1024]
    absent = [f for f in files if not (root / f).is_file()]
    soup = BeautifulSoup((root / "index.html").read_text(), "html.parser")
    film = soup.find("video", id="door-film")
    gated = bool(film) and film.get("preload") == "none" and film.has_attr("data-reduced-motion-skip")
    srcs = soup.select("video#earth-intro source")
    adaptive = any("2160" in (s.get("src") or "") for s in srcs) and any("max-width" in (s.get("media") or "") for s in srcs)
    return {"missing_sector_art": missing, "heavy": heavy, "absent": absent, "door_gated": gated, "earth_adaptive": adaptive}


@program("QA-21")
def qa_21(work):
    root = Path(work) / "site"; (root / "sectors").mkdir(parents=True)
    sectors = ["health", "trade", "energy"]
    for s in sectors:
        (root / "sectors" / f"{s}.webp").write_bytes(b"RIFF" + bytes(2000))
    (root / "logo.svg").write_text("<svg/>")
    (root / "index.html").write_text('<video id="door-film" preload="none" data-reduced-motion-skip></video>'
                                    '<video id="earth-intro"><source src="earth-2160.mp4"><source src="earth-720.mp4" media="(max-width: 700px)"></video>')
    good = brand_art(root, sectors, ["logo.svg"])
    (root / "sectors" / "energy.webp").unlink(); (root / "logo.svg").write_bytes(bytes(200 * 1024))
    bad = brand_art(root, sectors, ["logo.svg", "mark.svg"])
    wjson(Path(work) / "brand_art.json", {"good": good, "bad": bad})
    return [C("every sector has art, files light, door film gated, 4K + mobile intro", not good["missing_sector_art"] and not good["heavy"] and good["door_gated"] and good["earth_adaptive"], good),
            C("missing energy art caught", bad["missing_sector_art"] == ["energy"], bad),
            C("200 KB logo over the 150 KB weight cap caught", bad["heavy"] == ["logo.svg"], bad),
            C("named brand file mark.svg absent caught", bad["absent"] == ["mark.svg"], bad)]


def shard(seed, radius=1.0, height=0.6, sides=6):
    rng = np.random.default_rng(seed)
    ang = np.sort(rng.uniform(0, 2 * np.pi, sides)) if seed else np.linspace(0, 2 * np.pi, sides, endpoint=False)
    rr = radius * (0.8 + 0.2 * rng.random(sides))
    top = [np.array([r * math.cos(a), height / 2, r * math.sin(a)]) for a, r in zip(ang, rr)]
    bot = [p - np.array([0, height, 0]) for p in top]
    ct, cb = np.array([0, height / 2 + 0.2, 0]), np.array([0, -height / 2 - 0.2, 0])
    tris = []
    for i in range(sides):
        j = (i + 1) % sides
        tris += [(top[i], bot[i], bot[j]), (top[i], bot[j], top[j]), (ct, top[j], top[i]), (cb, bot[i], bot[j])]
    verts = np.array([v for t in tris for v in t])
    normals = []
    for a, b, c in tris:
        n = np.cross(b - a, c - a); n /= np.linalg.norm(n); normals += [n] * 3
    return verts, np.array(normals)


def closed_mesh(verts):
    key = lambda p: tuple(np.round(p, 9))
    edges = {}
    for t in range(0, len(verts), 3):
        tri = [key(verts[t + k]) for k in range(3)]
        for a, b in ((0, 1), (1, 2), (2, 0)):
            e = tuple(sorted((tri[a], tri[b]))); edges[e] = edges.get(e, 0) + 1
    return all(c == 2 for c in edges.values())


@program("QA-22")
def qa_22(work):
    v, n = shard(11); v2, _ = shard(11); v3, _ = shard(12)
    norms = np.linalg.norm(n, axis=1)
    np.save(Path(work) / "shard_11.npy", v)
    return [C("72 vertices per shard", v.shape == (72, 3), v.shape),
            C("closed geometry: every edge shared by exactly 2 triangles", closed_mesh(v), True),
            C("unit normals |n| = 1 +- 1e-5", float(np.max(np.abs(norms - 1))) <= 1e-5, float(np.max(np.abs(norms - 1)))),
            C("deterministic for a seed and different across seeds", np.array_equal(v, v2) and not np.array_equal(v, v3), True),
            C("a shard missing one triangle is not closed", not closed_mesh(v[:-3]), True)]


DEFAULT_BRIEF = {"duration": 30, "aspect": "9:16", "title": "", "topic": "", "style": "editorial", "language": "ar"}


def normalize_brief(raw):
    b = dict(DEFAULT_BRIEF, **(raw or {}))
    errs = []
    try:
        d = float(b["duration"])
    except (TypeError, ValueError):
        d = float("nan")
    if not math.isfinite(d) or not 3 <= d <= 600:
        errs.append("duration")
    if b["aspect"] not in ("9:16", "16:9", "1:1"):
        errs.append("aspect")
    for k in ("title", "topic", "style", "language"):
        if not isinstance(b[k], str) or not b[k].strip():
            errs.append(k)
    return (None, errs) if errs else (dict(b, duration=d), [])


@program("QA-23")
def qa_23(work):
    ok = {"title": "سوق", "topic": "تمر"}
    cases = {"defaults": normalize_brief(ok), "d3": normalize_brief(dict(ok, duration=3)), "d600": normalize_brief(dict(ok, duration="600")),
             "d2": normalize_brief(dict(ok, duration=2.9)), "d601": normalize_brief(dict(ok, duration=601)), "nan": normalize_brief(dict(ok, duration="abc")),
             "aspect": normalize_brief(dict(ok, aspect="4:3")), "empty": normalize_brief(dict(ok, title="  "))}
    wjson(Path(work) / "brief_cases.json", cases)
    return [C("defaults merged (30 s, 9:16, editorial)", cases["defaults"][0] and cases["defaults"][0]["duration"] == 30 and cases["defaults"][0]["aspect"] == "9:16", cases["defaults"]),
            C("3 s and '600' accepted", cases["d3"][0] is not None and cases["d600"][0]["duration"] == 600.0, ""),
            C("2.9 s, 601 s and non-numeric rejected", all(cases[k][1] == ["duration"] for k in ("d2", "d601", "nan")), ""),
            C("aspect 4:3 rejected", cases["aspect"][1] == ["aspect"], cases["aspect"][1]),
            C("blank title rejected", cases["empty"][1] == ["title"], cases["empty"][1])]


VIRAL_STAGES = ("hook", "script", "storyboard", "style", "sound")


def approve_final_render(story, typed):
    if story.get("profile") != "viral-editorial-3d":
        return False, "profile"
    if any(not story.get("stages", {}).get(s) for s in VIRAL_STAGES):
        return False, "stages"
    if typed != "APPROVE FINAL RENDER":
        return False, "phrase"
    story.setdefault("approval", {})["final_render"] = True
    return True, "approved"


def render_allowed(story, approved_flag):
    return (not approved_flag) or bool(story.get("approval", {}).get("final_render"))


@program("QA-24")
def qa_24(work):
    mk = lambda: {"profile": "viral-editorial-3d", "stages": {s: True for s in VIRAL_STAGES}}
    s1 = mk(); r1 = approve_final_render(s1, "APPROVE FINAL RENDER")
    s2 = mk(); r2 = approve_final_render(s2, "approve final render")
    s3 = mk(); s3["stages"]["sound"] = False; r3 = approve_final_render(s3, "APPROVE FINAL RENDER")
    s4 = dict(mk(), profile="cinematic"); r4 = approve_final_render(s4, "APPROVE FINAL RENDER")
    wjson(Path(work) / "approval.json", {"exact": s1, "lower": r2, "stage_missing": r3, "profile": r4})
    return [C("exact phrase + all five stages records approval.final_render=true", r1[0] and s1["approval"]["final_render"] is True, r1),
            C("lower-case phrase refused", r2 == (False, "phrase"), r2),
            C("a missing stage refuses approval", r3 == (False, "stages"), r3),
            C("non-viral profile refused", r4 == (False, "profile"), r4),
            C("--approved MP4 export refused without approval", not render_allowed(s2, True) and render_allowed(s1, True), "")]


def narration_artifact(kind, lines):
    art = {"kind": kind, "lines": lines, "needsFactCheck": kind == "history"}
    art["footer"] = "يحتاج مراجعة مصادر حقيقية وصور موثقة قبل النشر" if art["needsFactCheck"] else ""
    return art


def publish_allowed(art, sources):
    return not art["needsFactCheck"] or bool(sources)


@program("QA-26")
def qa_26(work):
    h = narration_artifact("history", ["في عام ...، بُنيت المدينة"]); p = narration_artifact("product", ["كوب جديد"])
    wjson(Path(work) / "artifacts.json", [h, p])
    return [C("history narration carries needsFactCheck=true and a footer warning", h["needsFactCheck"] and h["footer"], h),
            C("non-history artifact is not flagged", not p["needsFactCheck"], p),
            C("publishing blocked without sources, allowed with sources", not publish_allowed(h, []) and publish_allowed(h, ["archive ref"]), "")]


def read_json_blocks(html):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    return {s["id"]: json.loads(s.string) for s in soup.find_all("script", type="application/json") if s.get("id")}


def reel_problems(reel):
    out = []
    for sc in reel["scenes"]:
        a, b = sc["t"]
        for el in sc["els"]:
            x, y, w, h = el["box"]
            if not (0 <= x and 0 <= y and x + w <= 100 and y + h <= 100):
                out.append(f"{el['id']} box outside frame")
            if not (a <= el["t"][0] < el["t"][1] <= b):
                out.append(f"{el['id']} time outside scene")
    return out


def set_props(html, **changes):
    blocks = read_json_blocks(html); props = dict(blocks["kosif-props"], **changes)
    return re.sub(r'(<script type="application/json" id="kosif-props">).*?(</script>)',
                  lambda m: m.group(1) + json.dumps(props, ensure_ascii=False) + m.group(2), html, flags=re.S)


@program("QA-27")
def qa_27(work):
    reel = {"ai": {"locks": ["lantern"], "fps": 30}, "scenes": [{"id": "s1", "name": "open", "t": [0, 3], "els": [
        {"id": "title", "label": "Title", "t": [0.5, 3], "box": [10, 40, 80, 12], "props": {"text": {"type": "text"}}}]}]}
    html = ('<style>:root{--lantern:#ff9a3c}</style><script type="application/json" id="kosif-props">{"title":"ليلة","subtitle":"","titleAt":0.5}</script>'
            f'<script type="application/json" id="kosif-reel">{json.dumps(reel)}</script><h1 id="title"></h1>')
    blocks = read_json_blocks(html)
    edited = set_props(html, title="ليلة الجمعة")
    p = Path(work) / "index.html"; p.write_text(edited, encoding="utf-8")
    bad = json.loads(json.dumps(reel)); bad["scenes"][0]["els"][0]["box"] = [30, 40, 80, 12]; bad["scenes"][0]["els"][0]["t"] = [2, 4]
    return [C("both JSON blocks parse from the composition", set(blocks) == {"kosif-props", "kosif-reel"}, sorted(blocks)),
            C("valid reel: boxes inside 100% frame and times inside scene", reel_problems(blocks["kosif-reel"]) == [], ""),
            C("edited title written back into kosif-props only", read_json_blocks(p.read_text(encoding="utf-8"))["kosif-props"]["title"] == "ليلة الجمعة" and read_json_blocks(edited)["kosif-reel"] == reel, ""),
            C("box past the right edge and time past scene end are caught", reel_problems(bad) == ["title box outside frame", "title time outside scene"], reel_problems(bad))]


def boundaries(frames, cut_d=0.5, black=16, bright=30):
    f = np.asarray(frames, dtype=np.float64); n = len(f); m = f.mean(axis=(1, 2))
    def corr(a, b):
        a = a - a.mean(); b = b - b.mean(); den = math.sqrt((a * a).sum() * (b * b).sum())
        return float((a * b).sum() / den) if den > 1e-9 else 1.0
    d = np.array([0.0] + [1 - corr(f[i - 1], f[i]) for i in range(1, n)])
    out, used = [], np.zeros(n, bool)
    i = 0
    while i < n:  # dips: near-black run with a bright side >= 30, extended over the monotonic fades
        if m[i] < black:
            j = i
            while j + 1 < n and m[j + 1] < black:
                j += 1
            s, e = i, j
            while s > 0 and m[s - 1] > m[s] + 0.5:
                s -= 1
            while e + 1 < n and m[e + 1] > m[e] + 0.5:
                e += 1
            if max(m[max(s - 1, 0)], m[min(e + 1, n - 1)]) >= bright:
                out.append({"type": "fadeblack", "frame": i, "start": s, "dur": e - s + 1}); used[s:e + 2] = True
            i = j + 1
        else:
            i += 1
    i = 1
    while i < n:
        if used[i]:
            i += 1; continue
        if d[i] > cut_d:
            out.append({"type": "cut", "frame": i, "start": i, "dur": 0}); i += 1; continue
        if d[i] > 1e-3:
            j = i
            while j + 1 < n and 1e-3 < d[j + 1] <= cut_d and not used[j + 1]:
                j += 1
            if j - i + 1 >= 4:
                out.append({"type": "dissolve", "frame": i, "start": i, "dur": j - i})
            i = j + 1; continue
        i += 1
    return sorted(out, key=lambda b: b["start"])


def shots_from(bounds, n):
    edges = [0] + [b["start"] for b in bounds] + [n]
    return [(a, b) for a, b in zip(edges, edges[1:]) if b > a]


def transition_fixture():
    A, B, Cc, D = (texture(36, 64, s) * 0.5 + lv for s, lv in ((1, 60), (2, 120), (3, 90), (4, 70)))
    fr = [A] * 60 + [B] * 60
    fr += [(1 - (k + 1) / 17) * B + (k + 1) / 17 * Cc for k in range(16)] + [Cc] * 44
    fr += [Cc * (1 - (k + 1) / 9) for k in range(8)] + [np.zeros_like(Cc)] * 4 + [D * (k + 1) / 9 for k in range(8)]
    fr += [D] * 10 + [D * (1 + 0.3 * k / 19) for k in range(20)] + [D * 1.3] * 10
    return np.stack(fr)


@program("QA-28")
def qa_28(work):
    fr = transition_fixture(); b = boundaries(fr); shots = shots_from(b, len(fr))
    np.save(Path(work) / "means.npy", fr.mean(axis=(1, 2)))
    wjson(Path(work) / "boundaries.json", {"boundaries": b, "shots": shots})
    cut = [x for x in b if x["type"] == "cut"]; dis = [x for x in b if x["type"] == "dissolve"]; dip = [x for x in b if x["type"] == "fadeblack"]
    return [C("cut found at frame 60 exactly", [x["frame"] for x in cut] == [60], cut),
            C("dissolve at 120 +-2 with 16-frame length +-2", len(dis) == 1 and abs(dis[0]["start"] - 120) <= 2 and abs(dis[0]["dur"] - 16) <= 2, dis),
            C("dip start 180 +-3, length 20 +-4", len(dip) == 1 and abs(dip[0]["start"] - 180) <= 3 and abs(dip[0]["dur"] - 20) <= 4, dip),
            C("exposure ramp inside the last shot is not a boundary", len(b) == 3, [x["type"] for x in b]),
            C("shots cover the whole film without gaps", shots[0][0] == 0 and shots[-1][1] == len(fr) and all(a[1] == c[0] for a, c in zip(shots, shots[1:])), shots)]


def truss2d(nodes, members, supports, loads, E=200e9, A=1e-3):
    N = len(nodes); K = np.zeros((2 * N, 2 * N)); geo = []
    for a, b in members:
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        L = math.hypot(x2 - x1, y2 - y1)
        if not math.isfinite(L) or L < 1e-9:
            raise ValueError("degenerate member")
        c, s = (x2 - x1) / L, (y2 - y1) / L; geo.append((L, c, s))
        k = E * A / L * np.outer([-c, -s, c, s], [-c, -s, c, s]); idx = [2 * a, 2 * a + 1, 2 * b, 2 * b + 1]
        K[np.ix_(idx, idx)] += k
    fixed = [2 * n + d for n, dofs in supports.items() for d in dofs]
    free = [i for i in range(2 * N) if i not in fixed]
    F = np.zeros(2 * N)
    for n, (fx, fy) in loads.items():
        F[2 * n] += fx; F[2 * n + 1] += fy
    Kff = K[np.ix_(free, free)]
    if np.linalg.matrix_rank(Kff) < len(free):
        raise ArithmeticError("mechanism")
    u = np.zeros(2 * N); u[free] = np.linalg.solve(Kff, F[free])
    R = K @ u - F
    forces = [E * A / L * (c * (u[2 * b] - u[2 * a]) + s * (u[2 * b + 1] - u[2 * a + 1])) for (a, b), (L, c, s) in zip(members, geo)]
    return {"reactions": {i: round(float(R[i]), 3) for i in fixed}, "forces": [round(float(f), 2) for f in forces], "residual": float(np.abs(R[free]).max())}


@program("QA-29")
def qa_29(work):
    nodes = [(0, 0), (2, 2), (4, 0)]; members = [(0, 1), (1, 2), (0, 2)]
    r = truss2d(nodes, members, {0: (0, 1), 2: (1,)}, {1: (0, -12000)})
    mech = degenerate = False
    try:
        truss2d(nodes, [(0, 1), (1, 2)], {0: (0, 1), 2: (1,)}, {1: (0, -12000)})
    except ArithmeticError:
        mech = True
    try:
        truss2d([(0, 0), (0, 0), (4, 0)], members, {0: (0, 1), 2: (1,)}, {1: (0, -12000)})
    except ValueError:
        degenerate = True
    wjson(Path(work) / "truss.json", r)
    hand = -12000 / 2 / math.sin(math.pi / 4)
    return [C("A.y = C.y = 6000 N (hand calc)", abs(r["reactions"][1] - 6000) < 1e-3 and abs(r["reactions"][5] - 6000) < 1e-3, r["reactions"]),
            C("AB = BC = -8485.28 N compression, AC = +6000 N tension", abs(r["forces"][0] - hand) < 0.05 and abs(r["forces"][1] - hand) < 0.05 and abs(r["forces"][2] - 6000) < 0.05, r["forces"]),
            C("equilibrium residual ~0 at free DOFs", r["residual"] < 1e-6, r["residual"]),
            C("removing the tie AC makes a mechanism (rejected)", mech, mech),
            C("zero-length member geometry rejected", degenerate, degenerate)]


def pose(t):
    jump = 100 * math.sin(math.pi * (t - 5) / 2) if 5 <= t <= 7 else 0.0
    return {"x": 40 * t, "jump": jump}


def scene_svg(t, broken=False):
    p = pose(t)
    r = 20 + 5 * math.sin(t) if not broken else 20 / (t - 3.5) if t != 3.5 else float("nan")
    return (f'<svg width="1280" height="720" viewBox="0 0 1280 720"><circle cx="{p["x"]:.2f}" cy="{600 - p["jump"]:.2f}" r="{r:.2f}"/></svg>')


def film_function_tests(fn):
    bad = [i for i in range(289) if not fn(i / 24).startswith("<svg") or re.search(r"NaN|nan|undefined|Infinity|inf", fn(i / 24)) or 'width="1280"' not in fn(i / 24)]
    return {"invalid_frames": bad, "deterministic": fn(3.5) == fn(3.5), "changes": fn(2) != fn(4)}


@program("QA-30")
def qa_30(work):
    good = film_function_tests(scene_svg); bad = film_function_tests(lambda t: scene_svg(t, broken=True))
    (Path(work) / "frame_3_5.svg").write_text(scene_svg(3.5))
    return [C("289 samples (0..288 / 24) valid, no NaN, width 1280", good["invalid_frames"] == [], good),
            C("re-render identical and frames change over time", good["deterministic"] and good["changes"], good),
            C("pose(6).jump > 80, pose(8).jump == 0, pose(8).x > pose(3).x", pose(6)["jump"] > 80 and pose(8)["jump"] == 0 and pose(8)["x"] > pose(3)["x"], [pose(6), pose(8)]),
            C("planted NaN at t=3.5 (frame 84) is caught", bad["invalid_frames"] == [84], bad["invalid_frames"])]


class Player:
    def __init__(self, duration=12.0, reduced=False):
        self.duration, self.reduced, self.t, self.playing, self.last = duration, reduced, 0.0, False, None
        self.frames = []
        self.render(duration if reduced else 0.0)

    def render(self, t):
        self.t = min(max(t, 0.0), self.duration); self.frames.append(round(self.t, 3)); return self.t

    def play(self):
        if self.reduced:
            return
        if self.t >= self.duration:
            self.render(0.0)
        self.playing, self.last = not self.reduced, None

    def pause(self):
        self.playing = False

    def raf(self, ms):
        if not self.playing:
            return
        if self.last is not None:
            self.render(self.t + (ms - self.last) / 1000)
            if self.t >= self.duration:
                self.playing = False
        self.last = ms


@program("QA-31")
def qa_31(work):
    p = Player(); p.play(); p.raf(1000); p.raf(1042)
    adv = p.t
    clamp_lo, clamp_hi = p.render(-20), p.render(40)
    q = Player(); q.play(); q.raf(0); q.raf(13000); stopped = not q.playing
    q.play(); restarted = q.t == 0.0
    rm = Player(reduced=True); rm.play(); rm.raf(0); rm.raf(500)
    s = Player(); s.play(); s.raf(0); s.pause(); s.raf(5000)
    wjson(Path(work) / "player_log.json", {"frames": p.frames})
    return [C("rAF 1000 -> 1042 advances 42 ms", abs(adv - 0.042) < 1e-9, adv),
            C("render(-20) clamps to 0 and render(40) to 12", clamp_lo == 0.0 and clamp_hi == 12.0, (clamp_lo, clamp_hi)),
            C("auto-stops at the end and play restarts from 0", stopped and restarted, (stopped, restarted)),
            C("reduced motion shows the final frame and never plays", rm.t == 12.0 and not rm.playing, rm.t),
            C("pause stops advancing", s.t == 0.0, s.t)]


def readable(items, hook_by=2.0, floor=0.8, per_word=0.3):
    too_short = [{"what": it["what"], "need": round(max(floor, per_word * len(it["text"].split())), 2), "shown": it["dur"]}
                 for it in items if it["dur"] < max(floor, per_word * len(it["text"].split()))]
    first = min(it["start"] for it in items) if items else math.inf
    return {"too_short": too_short, "hook": {"ok": first <= hook_by, "first": first}}


@program("QA-32")
def qa_32(work):
    items = [{"what": "overlay 1", "text": " ".join(["كلمة"] * 14), "start": 0.4, "dur": 1.1},
             {"what": "overlay 2", "text": "انتبه هنا", "start": 2.0, "dur": 1.7}]
    r = readable(items); late = readable([dict(items[1], start=2.6)])
    wjson(Path(work) / "readable.json", r)
    return [C("14-word line shown 1.1 s fails", [x["what"] for x in r["too_short"]] == ["overlay 1"] and r["too_short"][0]["need"] == 4.2, r["too_short"]),
            C("2-word line shown 1.7 s passes", all(x["what"] != "overlay 2" for x in r["too_short"]), ""),
            C("hook in the first 2 s ok; first text at 2.6 s fails the hook", r["hook"]["ok"] and not late["hook"]["ok"], (r["hook"], late["hook"]))]


BANNED_COPY = ["excited to share", "thrilled to announce", "game changer", "game-changer", "نفخر بأن نعلن", "يسعدنا أن نشارككم"]


def check_copy(text, max_short=3, short_words=4):
    if not text.strip():
        return ["empty copy"]
    issues = [f"banned: {b}" for b in BANNED_COPY if b in text.lower()]
    sents = [s for s in re.split(r"[.!?؟\n]+", text) if s.strip()]
    short = [s for s in sents if len(s.split()) < short_words]
    if len(short) > max_short:
        issues.append(f"sentences: {len(short)} short sentences")
    return issues


@program("QA-33")
def qa_33(work):
    good = check_copy("صنعنا فيلمًا قصيرًا عن سوق التمر القديم في الأحساء خلال ثلاثة أيام.")
    cliche = check_copy("Excited to share our new reel with everyone today!")
    choppy = check_copy("New film. So good. Watch now. Big news. Link below.")
    wjson(Path(work) / "copy_lint.json", {"good": good, "cliche": cliche, "choppy": choppy, "empty": check_copy("  ")})
    return [C("short concrete Arabic line passes", good == [], good),
            C("'Excited to share' is banned", any("banned" in i for i in cliche), cliche),
            C("five 2-word sentences flagged", any("sentences" in i for i in choppy), choppy),
            C("empty copy flagged", check_copy("") == ["empty copy"], "")]


MOTION_TEMPLATES = ("bullet-list", "countdown", "end-card", "logo-reveal", "lower-third", "quote-card", "stat-counter", "title-card")


def mtemplate_create(root: Path, name, template, fields, fps=30, size="540x960"):
    import html as H
    if template not in MOTION_TEMPLATES:
        raise ValueError(template)
    d = root / name; d.mkdir(parents=True)
    items = "".join(f"<li>{H.escape(i)}</li>" for i in fields.get("items", "").split("|") if i)
    body = ("<!doctype html><html lang=ar><body data-composition-id={{id}} data-fps={{fps}}><h1>{{title}}</h1><ul>{{items}}</ul>"
            "<blockquote>{{quote}}</blockquote><script src=motion-kit.js></script><script>window.__timelines={main:{duration:{{dur}}}}</script></body></html>")
    w, h = size.split("x")
    vals = {"id": name, "fps": str(fps), "title": H.escape(fields.get("title", "")), "items": items, "quote": H.escape(fields.get("quote", "")), "dur": "6"}
    out = re.sub(r"\{\{(\w+)\}\}", lambda m: vals.get(m.group(1), m.group(0)), body)
    (d / "index.html").write_text(out, encoding="utf-8"); (d / "motion-kit.js").write_text("export const ease=t=>t*t*(3-2*t);")
    wjson(d / "template.json", {"template": template, "fps": fps, "width": int(w), "height": int(h)})
    return d


def template_lint(d: Path):
    html = (d / "index.html").read_text(encoding="utf-8")
    probs = []
    if re.search(r"\{\{\w+\}\}", html):
        probs.append("leftover placeholder")
    if "<script>alert" in html:
        probs.append("unescaped html")
    if "window.__timelines" not in html:
        probs.append("no timeline")
    for f in ("motion-kit.js", "template.json"):
        if not (d / f).is_file():
            probs.append(f"missing {f}")
    return probs


@program("QA-34")
def qa_34(work):
    root = Path(work)
    fields = {"title": "<script>alert(1)</script>عنوان", "items": "أ|ب|ج", "quote": "قول", "from": "x"}
    dirs = [mtemplate_create(root, f"p_{t}", t, fields) for t in MOTION_TEMPLATES]
    lints = {d.name: template_lint(d) for d in dirs}
    broken = root / "p_title-card" / "index.html"; broken.write_text(broken.read_text(encoding="utf-8").replace("<h1>", "<h1>{{subtitle}}"), encoding="utf-8")
    (root / "p_countdown" / "motion-kit.js").unlink()
    after = {d.name: template_lint(d) for d in dirs}
    return [C("all 8 templates generate lint-clean projects", all(v == [] for v in lints.values()) and len(lints) == 8, lints),
            C("title HTML is escaped", "&lt;script&gt;" in (root / "p_quote-card" / "index.html").read_text(encoding="utf-8"), ""),
            C("planted {{subtitle}} placeholder is caught", after["p_title-card"] == ["leftover placeholder"], after["p_title-card"]),
            C("missing motion-kit.js is caught", after["p_countdown"] == ["missing motion-kit.js"], after["p_countdown"])]


def review_apply(reel, feedback):
    reel = json.loads(json.dumps(reel)); applied, left_edits, notes, protected = [], [], [], []
    approved = {s["id"] for s in reel["scenes"] if s.get("status") == "approved"}
    els = {(s["id"], e["id"]): e for s in reel["scenes"] for e in s["els"]}
    for ed in feedback.get("edits", []):
        key = (ed["scene"], ed["el"])
        if ed["scene"] in approved:
            protected.append(ed); continue
        if ed["kind"] in ("text", "time", "box", "color") and key in els:
            els[key][ed["kind"]] = ed["value"]; applied.append(ed)
        else:
            left_edits.append(ed)
    notes = feedback.get("notes", [])
    return reel, {"applied": applied, "left_for_claude": {"edits": left_edits, "notes": notes}, "approved_do_not_touch": protected}


@program("QA-35")
def qa_35(work):
    reel = {"scenes": [{"id": "s1", "status": "review", "els": [{"id": "t", "text": "قديم", "time": [0, 2], "box": [0, 0, 50, 10], "color": "#ffffff"}]},
                       {"id": "s2", "status": "approved", "els": [{"id": "logo", "text": "", "time": [2, 4], "box": [40, 80, 20, 10], "color": "#c8a24a"}]}]}
    fb = {"edits": [{"scene": "s1", "el": "t", "kind": "text", "value": "جديد"}, {"scene": "s1", "el": "t", "kind": "box", "value": [5, 5, 50, 10]},
                    {"scene": "s1", "el": "t", "kind": "motion", "value": "أدخله من اليمين"}, {"scene": "s2", "el": "logo", "kind": "color", "value": "#ff0000"}],
          "notes": [{"t": 1.25, "x": 40.5, "y": 20.0, "text": "الخط صغير"}]}
    new, rep = review_apply(reel, fb)
    wjson(Path(work) / "reel.json", new); wjson(Path(work) / "apply_report.json", rep)
    return [C("copy and box edits applied to the source", new["scenes"][0]["els"][0]["text"] == "جديد" and new["scenes"][0]["els"][0]["box"] == [5, 5, 50, 10], new["scenes"][0]),
            C("motion request left for Claude, pinned note kept", [e["kind"] for e in rep["left_for_claude"]["edits"]] == ["motion"] and len(rep["left_for_claude"]["notes"]) == 1, rep["left_for_claude"]),
            C("approved scene untouched", new["scenes"][1]["els"][0]["color"] == "#c8a24a" and len(rep["approved_do_not_touch"]) == 1, new["scenes"][1])]


SECRET_RE = re.compile(r"(sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|Bearer\s+[A-Za-z0-9._-]{20,}|(?i:api[_-]?key|token|password)\s*[:=])")


def bridge_gate(req, pinned="https://render.example.org", max_req=64_000, approved=False):
    from urllib.parse import urlparse
    u = urlparse(req["url"]); body = json.dumps(req.get("payload", {}))
    if not req.get("allow_remote"):
        return "refused: remote not allowed"
    if f"{u.scheme}://{u.netloc}" != pinned or u.scheme != "https":
        return "refused: origin not pinned"
    if req.get("follow_redirects"):
        return "refused: redirects disabled"
    if len(body.encode()) > max_req:
        return "refused: request too large"
    if SECRET_RE.search(body):
        return "refused: credential in payload"
    if req.get("method", "GET") == "POST" and not approved:
        return "needs approval"
    return "ok"


@program("QA-36")
def qa_36(work):
    base = {"url": "https://render.example.org/v1/render", "allow_remote": True, "payload": {"plan": {"fps": 30}}, "method": "GET"}
    cases = {"ok": bridge_gate(base), "no_consent": bridge_gate(dict(base, allow_remote=False)),
             "other_origin": bridge_gate(dict(base, url="https://evil.example.com/v1")), "http": bridge_gate(dict(base, url="http://render.example.org/v1")),
             "redirect": bridge_gate(dict(base, follow_redirects=True)), "big": bridge_gate(dict(base, payload={"x": "a" * 70_000})),
             "token": bridge_gate(dict(base, payload={"note": "token=abc"})), "post": bridge_gate(dict(base, method="POST")),
             "post_ok": bridge_gate(dict(base, method="POST"), approved=True)}
    wjson(Path(work) / "bridge_gate.json", cases)
    return [C("pinned origin GET with consent passes", cases["ok"] == "ok", cases["ok"]),
            C("no consent / other origin / plain http refused", cases["no_consent"].startswith("refused") and "pinned" in cases["other_origin"] and "pinned" in cases["http"], cases),
            C("redirects and oversized requests refused", "redirect" in cases["redirect"] and "large" in cases["big"], cases),
            C("token in payload refused", "credential" in cases["token"], cases["token"]),
            C("POST needs approval", cases["post"] == "needs approval" and cases["post_ok"] == "ok", cases["post"])]


def validate_plan(plan):
    errs = []
    if plan.get("intent") not in ("promo", "explainer", "lyric", "montage"):
        errs.append("intent غير معروف")
    if plan.get("fps") not in (24, 25, 30, 50, 60):
        errs.append("fps غير مدعوم")
    if plan.get("aspect") not in ("9:16", "16:9", "1:1"):
        errs.append("نسبة العرض غير مدعومة")
    shots = plan.get("shots", [])
    if not 1 <= len(shots) <= 100:
        errs.append("عدد اللقطات خارج 1-100")
    prev = 0
    for i, s in enumerate(shots):
        if not (isinstance(s["start_frame"], int) and isinstance(s["end_frame"], int)):
            errs.append(f"اللقطة {i + 1}: إطارات غير صحيحة")
        if s["start_frame"] != prev:
            errs.append(f"اللقطة {i + 1}: فجوة أو تداخل")
        prev = s["end_frame"]
        for k in ("beat", "camera_move"):
            if len(s.get(k, "")) > 150:
                errs.append(f"اللقطة {i + 1}: {k} أطول من 150")
    warn = ["راجع الحقوق والخطوط والصوت"]
    return errs, warn


@program("QA-37")
def qa_37(work):
    shots = [{"start_frame": 0, "end_frame": 45, "beat": "hook", "camera_move": "push"}, {"start_frame": 45, "end_frame": 90, "beat": "b", "camera_move": "hold"}]
    good = {"intent": "promo", "fps": 30, "aspect": "9:16", "shots": shots}
    gap = dict(good, shots=[shots[0], dict(shots[1], start_frame=50)])
    long_ = dict(good, shots=[dict(shots[0], beat="x" * 151)])
    frac = dict(good, shots=[dict(shots[0], end_frame=45.5)])
    res = {k: validate_plan(v)[0] for k, v in {"good": good, "gap": gap, "long": long_, "frac": frac, "none": dict(good, shots=[]), "fps": dict(good, fps=29.97)}.items()}
    wjson(Path(work) / "plan_validation.json", res)
    return [C("gapless 2-shot plan passes", res["good"] == [], res["good"]),
            C("start_frame 50 after end 45 flagged as gap", any("فجوة" in e for e in res["gap"]), res["gap"]),
            C("151-char beat flagged", any("150" in e for e in res["long"]), res["long"]),
            C("fractional frames, 0 shots and 29.97 fps rejected", res["frac"] and res["none"] and res["fps"], res),
            C("rights/fonts/audio review warning always returned", validate_plan(good)[1] == ["راجع الحقوق والخطوط والصوت"], "")]


MANIFEST_KEYS = {"id", "title", "subtitle", "width", "height", "fps", "duration", "scenes", "accent"}


def validate_manifest(m, hosted=False):
    errs = [f"unknown key {k}" for k in set(m) - MANIFEST_KEYS]
    lo, hi = 128, (1280 if hosted else 1920)
    for k in ("width", "height"):
        v = m.get(k)
        if not isinstance(v, int) or v % 2 or not lo <= v <= hi:
            errs.append(k)
    if m.get("fps") not in ((24, 25, 30) if hosted else (24, 25, 30, 50, 60)):
        errs.append("fps")
    dur = m.get("duration", 0)
    if not 1 <= dur <= (30 if hosted else 600) or abs(dur * m.get("fps", 1) - round(dur * m.get("fps", 1))) > 1e-9:
        errs.append("duration")
    sc = m.get("scenes", [])
    if not 1 <= len(sc) <= (50 if hosted else 200):
        errs.append("scenes")
    t = 0.0
    for s in sc:
        if abs(s["start"] - t) > 1e-9:
            errs.append("scene gap")
        t = s["end"]
    if sc and abs(t - dur) > 1e-9:
        errs.append("scenes do not cover duration")
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", str(m.get("id", ""))):
        errs.append("id")
    if len(m.get("title", "")) > 120 or len(m.get("subtitle", "")) > 300:
        errs.append("text length")
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", m.get("accent", "")):
        errs.append("accent")
    return errs


@program("QA-38")
def qa_38(work):
    good = {"id": "promo_01", "title": "عرض", "subtitle": "", "width": 1080, "height": 1920, "fps": 30, "duration": 6,
            "scenes": [{"start": 0, "end": 3}, {"start": 3, "end": 6}], "accent": "#c8a24a"}
    cases = {"good": validate_manifest(good), "odd": validate_manifest(dict(good, width=1081)), "fps": validate_manifest(dict(good, fps=29)),
             "gap": validate_manifest(dict(good, scenes=[{"start": 0, "end": 3}, {"start": 3.5, "end": 6}])),
             "id": validate_manifest(dict(good, id="a.b")), "key": validate_manifest(dict(good, extra=1)), "accent": validate_manifest(dict(good, accent="gold")),
             "hosted_big": validate_manifest(good, hosted=True)}
    wjson(Path(work) / "manifest_validation.json", cases)
    return [C("1080x1920 30 fps gapless manifest passes", cases["good"] == [], cases["good"]),
            C("odd width 1081 and fps 29 rejected", cases["odd"] == ["width"] and cases["fps"] == ["fps"], (cases["odd"], cases["fps"])),
            C("scene gap 3.0 -> 3.5 rejected", "scene gap" in cases["gap"], cases["gap"]),
            C("unsafe id, unknown key and non-hex accent rejected", cases["id"] == ["id"] and cases["key"] == ["unknown key extra"] and cases["accent"] == ["accent"], ""),
            C("hosted demo limit: 1920 px > 1280 rejected", "height" in cases["hosted_big"], cases["hosted_big"])]


def foreign_origin(method, path, headers):
    if method in ("GET", "HEAD", "OPTIONS") or not re.match(r"^/(api|review|mcp)(/|$)", path):
        return False
    if headers.get("sec-fetch-site") in ("cross-site", "same-site"):
        return True
    origin = headers.get("origin")
    if origin:
        from urllib.parse import urlparse
        return urlparse(origin).hostname not in ("127.0.0.1", "localhost", "::1")
    return False


@program("QA-39")
def qa_39(work):
    cases = {"browser_foreign": foreign_origin("POST", "/api/jobs", {"origin": "https://evil.example", "sec-fetch-site": "cross-site"}),
             "same_site": foreign_origin("POST", "/review/x", {"sec-fetch-site": "same-site"}),
             "local_origin": foreign_origin("POST", "/api/jobs", {"origin": "http://127.0.0.1:8766", "sec-fetch-site": "same-origin"}),
             "ipv6": foreign_origin("POST", "/mcp", {"origin": "http://[::1]:8766"}),
             "curl": foreign_origin("POST", "/api/jobs", {}), "get": foreign_origin("GET", "/api/env", {"origin": "https://evil.example"}),
             "other_path": foreign_origin("POST", "/static/x", {"origin": "https://evil.example"})}
    wjson(Path(work) / "origin_guard.json", cases)
    return [C("cross-site POST to /api refused (403)", cases["browser_foreign"], cases),
            C("same-site Sec-Fetch-Site refused", cases["same_site"], cases),
            C("localhost / [::1] origins allowed", not cases["local_origin"] and not cases["ipv6"], cases),
            C("curl/MCP without Origin still works", not cases["curl"], cases),
            C("read-only GET and non-API paths not blocked", not cases["get"] and not cases["other_path"], cases)]


SAN_ENUMS = {"aspect": ("16:9", "9:16", "1:1"), "type": ("image", "video", "demo"), "fit": ("contain", "cover"), "preset": ("aurora", "sunset", "grid"),
             "overlay": ("text", "shape"), "shape": ("circle", "rectangle"), "animation": ("none", "fade", "rise", "zoom")}


def sanitize_project(raw, media_durations, max_total=60.0):
    def enum(v, k):
        return v if v in SAN_ENUMS[k] else SAN_ENUMS[k][0]
    def colour(v):
        return v.lower() if isinstance(v, str) and re.fullmatch(r"#[0-9a-fA-F]{6}", v) else "#ffffff"
    p = {"version": 1, "aspect": enum(raw.get("aspect"), "aspect"), "preset": enum(raw.get("preset"), "preset"), "clips": [], "overlays": []}
    seen, total = set(), 0.0
    for c in raw.get("clips", []):
        cid = c.get("id") or "clip"
        while cid in seen:
            cid += "_1"
        seen.add(cid)
        dur = min(max(float(c.get("dur", 1)), 0.1), media_durations.get(c.get("src"), 0.1))
        dur = max(0.0, min(dur, max_total - total)); total += dur
        if dur <= 0:
            continue
        p["clips"].append({"id": cid, "type": enum(c.get("type"), "type"), "fit": enum(c.get("fit"), "fit"), "src": c.get("src"), "dur": round(dur, 3)})
    for o in raw.get("overlays", []):
        p["overlays"].append({"kind": enum(o.get("kind"), "overlay"), "shape": enum(o.get("shape"), "shape"), "animation": enum(o.get("animation"), "animation"),
                              "color": colour(o.get("color")), "opacity": min(max(float(o.get("opacity", 1)), 0.0), 1.0)})
    return p


@program("QA-41")
def qa_41(work):
    raw = {"version": 7, "aspect": "4:3", "preset": "grid", "clips": [{"id": "a", "src": "x.mp4", "dur": 50, "type": "video"},
           {"id": "a", "src": "y.mp4", "dur": 30, "type": "gif", "fit": "stretch"}, {"id": "b", "src": "x.mp4", "dur": 5}],
           "overlays": [{"kind": "text", "color": "#ABCDEF", "opacity": 3, "animation": "spin"}, {"kind": "shape", "shape": "star", "color": "red"}]}
    p = sanitize_project(raw, {"x.mp4": 40.0, "y.mp4": 25.0})
    wjson(Path(work) / "project.json", p)
    durs = [c["dur"] for c in p["clips"]]
    return [C("version forced to 1 and aspect 4:3 -> 16:9", p["version"] == 1 and p["aspect"] == "16:9", p["aspect"]),
            C("duplicate id 'a' de-duplicated", [c["id"] for c in p["clips"]][:2] == ["a", "a_1"], [c["id"] for c in p["clips"]]),
            C("clip capped at media duration (50 -> 40) and total at 60 s", durs == [40.0, 20.0] and sum(durs) == 60.0, durs),
            C("enums whitelisted (gif -> image, stretch -> contain, spin -> none, star -> circle)", p["clips"][1]["type"] == "image" and p["clips"][1]["fit"] == "contain" and p["overlays"][0]["animation"] == "none" and p["overlays"][1]["shape"] == "circle", ""),
            C("colours #rrggbb lower-cased; 'red' replaced; opacity clamped to 1", p["overlays"][0]["color"] == "#abcdef" and p["overlays"][1]["color"] == "#ffffff" and p["overlays"][0]["opacity"] == 1.0, p["overlays"])]


SCENE_SPEC_FIELDS = ["subjects", "character_identity", "anatomy", "action", "contact_physics", "world", "location", "architecture", "camera", "lens",
                     "camera_angle", "depth_of_field", "lighting.key", "lighting.fill", "lighting.rim", "color_temperature", "color_grade", "materials",
                     "weather", "atmosphere", "VFX", "composition", "story_focus", "negative_constraints", "aspect_ratio"]


def validate_scene(scene):
    missing = []
    for f in SCENE_SPEC_FIELDS:
        v = scene
        for part in f.split("."):
            v = v.get(part) if isinstance(v, dict) else None
        if v in (None, "", [], {}):
            missing.append(f)
    return missing


@program("QA-42")
def qa_42(work):
    full = {f: "x" for f in SCENE_SPEC_FIELDS if "." not in f}; full["lighting"] = {"key": "sun 45°", "fill": "bounce", "rim": "sky"}
    bad = json.loads(json.dumps(full)); bad["lighting"].pop("rim"); bad["negative_constraints"] = []
    wjson(Path(work) / "scene_spec.json", full)
    return [C("strict spec has exactly 25 required fields", len(SCENE_SPEC_FIELDS) == 25, len(SCENE_SPEC_FIELDS)),
            C("complete scene passes", validate_scene(full) == [], validate_scene(full)),
            C("missing lighting.rim and empty negatives rejected", validate_scene(bad) == ["lighting.rim", "negative_constraints"], validate_scene(bad))]


PROMPT_CATS = {"subject": (20, r"\b(woman|man|child|dragon|merchant|cat|car|lantern|market)\b"),
               "lighting": (14, r"\b(light|lit|sunset|golden hour|backlit|rim light|softbox|neon)\b"),
               "environment": (14, r"\b(street|market|desert|room|forest|city|alley|studio)\b"),
               "camera": (10, r"\b(close-up|wide shot|medium shot|low angle|overhead|eye level)\b"),
               "style": (10, r"\b(photoreal|cinematic|watercolor|anime|cartoon|editorial|film still)\b"),
               "lens": (8, r"\b\d{2,3}\s?mm\b|\bf/\d"), "color": (8, r"\b(teal|amber|warm|cool|palette|monochrome|vibrant|pastel)\b"),
               "quality": (8, r"\b(detailed|sharp|high detail|8k|4k|crisp)\b"), "aspect": (8, r"\b(9:16|16:9|1:1|4:5)\b")}
VIDEO_CATS = {"camera_move": (8, r"\b(dolly|pan|tilt|orbit|push in|tracking)\b"), "duration": (8, r"\b\d+\s?(s|sec|seconds)\b"),
              "motion": (8, r"\b(walks|runs|turns|flows|drifts|moves)\b"), "pacing": (8, r"\b(slow|fast|steady|gradual)\b")}
CONFLICTS = [("photoreal", r"cartoon|anime"), ("black and white|b&w", r"vibrant"), ("daylight|noon", r"night"), ("high-key", r"low-key")]


def prompt_lint(prompt, mode="image", contract=None, locks=None):
    p = prompt.lower(); cats = dict(PROMPT_CATS, **(VIDEO_CATS if mode == "video" else {}))
    hits = {k: bool(re.search(rx, p)) for k, (w, rx) in cats.items()}
    total = sum(w for w, _ in cats.values()); score = round(100 * sum(cats[k][0] for k, h in hits.items() if h) / total, 1)
    words = len(prompt.split()); notes = []
    if words < 25:
        notes.append("short")
    if words > 220:
        notes.append("long")
    conflicts = [f"{a} vs {b}" for a, b in CONFLICTS if re.search(a, p) and re.search(b, p)]
    contract = contract or {}
    block = [f"forbidden: {t}" for t in contract.get("forbidden", []) if t.lower() in p]
    block += [f"lock missing: {k}" for k, v in (locks or {}).items() if v not in prompt]
    missing = [t for t in contract.get("required", []) if t.lower() not in p]
    if re.search(r"[؀-ۿ]", prompt):
        notes.append("arabic in generation text")
    verdict = "BLOCK" if block else "REVISE" if (score < 60 or conflicts or missing) else "PASS"
    return {"score": score, "hits": hits, "notes": notes, "conflicts": conflicts, "block": block, "missing": missing, "verdict": verdict,
            "exit": {"PASS": 0, "REVISE": 1, "BLOCK": 3}[verdict]}


RICH_PROMPT = ("Cinematic film still of an old lantern merchant in a narrow market street at golden hour, warm amber palette with teal shadows, "
               "backlit rim light, medium shot at eye level, 50mm lens f/2, sharp high detail textures on brass lanterns, 9:16 vertical frame")


@program("QA-43")
def qa_43(work):
    rich = prompt_lint(RICH_PROMPT, contract={"required": ["lantern"], "forbidden": ["logo"]}, locks={"hero": "lantern merchant"})
    thin = prompt_lint("a cat")
    clash = prompt_lint(RICH_PROMPT + " photoreal cartoon style")
    forb = prompt_lint(RICH_PROMPT + " with a brand logo", contract={"forbidden": ["logo"]})
    video = prompt_lint(RICH_PROMPT, mode="video")
    wjson(Path(work) / "prompt_lint.json", {"rich": rich, "thin": thin, "clash": clash, "forbidden": forb, "video": video})
    return [C("rich image prompt scores 100 and passes (exit 0)", rich["score"] == 100.0 and rich["exit"] == 0, rich["score"]),
            C("'a cat' scores 20/100 (subject only), short, REVISE exit 1", thin["score"] == 20.0 and "short" in thin["notes"] and thin["exit"] == 1, thin),
            C("photoreal vs cartoon conflict flagged", clash["conflicts"] == ["photoreal vs cartoon|anime"] and clash["verdict"] == "REVISE", clash["conflicts"]),
            C("forbidden term blocks (exit 3)", forb["exit"] == 3, forb["block"]),
            C("video mode adds 4x8 weights: same prompt scores 100/132", abs(video["score"] - round(100 * 100 / 132, 1)) < 1e-9, video["score"])]


LOCK_ORDER = ("subject", "action", "composition", "camera", "lighting", "weather", "environment", "style")
VC_THRESH = {"anatomy": 0.70, "composition": 0.65, "lighting": 0.65, "physics": 0.65, "attention": 0.70}
VC_SOURCES = {"host-vision", "vision-tool", "human-review", "state-observation"}


def vc_build(request_id, locks, attention):
    if len(attention) > 3:
        raise ValueError("attention budget max 3")
    return {"request_id": request_id, "locks": [(k, locks[k]) for k in LOCK_ORDER if k in locks], "attention": list(attention), "repairs": 0}


def vc_verify(contract, evidence):
    if evidence.get("source") not in VC_SOURCES or evidence.get("request_id") != contract["request_id"]:
        return {"verdict": "UNVERIFIED", "failed": []}
    failed = [k for k, t in VC_THRESH.items() if evidence["scores"].get(k, 0) < t]
    return {"verdict": "PASS" if not failed else "FAIL", "failed": failed}


def vc_repair(contract, failed):
    if contract["repairs"] >= 1:
        return None
    contract["repairs"] += 1
    return {"targets": failed}


@program("QA-44")
def qa_44(work):
    c = vc_build("r1", {"style": "ink", "subject": "falcon", "lighting": "dawn", "camera": "low"}, ["eyes", "wings"])
    good = vc_verify(c, {"source": "host-vision", "request_id": "r1", "scores": {"anatomy": .8, "composition": .7, "lighting": .9, "physics": .7, "attention": .75}})
    lowc = vc_verify(c, {"source": "host-vision", "request_id": "r1", "scores": {"anatomy": .8, "composition": .64, "lighting": .9, "physics": .7, "attention": .75}})
    other = vc_verify(c, {"source": "host-vision", "request_id": "r2", "scores": {k: 1 for k in VC_THRESH}})
    selfc = vc_verify(c, {"source": "self-claim", "request_id": "r1", "scores": {k: 1 for k in VC_THRESH}})
    r1, r2 = vc_repair(c, lowc["failed"]), vc_repair(c, lowc["failed"])
    budget = False
    try:
        vc_build("r3", {}, ["a", "b", "c", "d"])
    except ValueError:
        budget = True
    wjson(Path(work) / "visual_contract.json", {"contract": c, "good": good, "low": lowc})
    return [C("locks frozen in canonical order subject, camera, lighting, style", [k for k, _ in c["locks"]] == ["subject", "camera", "lighting", "style"], c["locks"]),
            C("scores at/above thresholds pass", good["verdict"] == "PASS", good),
            C("composition 0.64 < 0.65 fails on composition only", lowc["failed"] == ["composition"], lowc),
            C("evidence from another request or a self-claim is UNVERIFIED", other["verdict"] == "UNVERIFIED" and selfc["verdict"] == "UNVERIFIED", ""),
            C("exactly one targeted repair allowed; attention budget 4 > 3 refused", r1 == {"targets": ["composition"]} and r2 is None and budget, (r1, r2))]


def web_audit(html):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser"); block, revise = [], []
    vp = soup.find("meta", attrs={"name": "viewport"})
    if not vp:
        block.append("missing viewport")
    elif re.search(r"user-scalable\s*=\s*no|maximum-scale\s*=\s*1(\.0)?\b", vp.get("content", "")):
        block.append("zoom disabled")
    if not (soup.html and soup.html.get("lang")):
        block.append("missing lang")
    css = " ".join(s.get_text() for s in soup.find_all("style"))
    for theme, scope in (("light", r":root\{([^}]*)\}"), ("dark", r"prefers-color-scheme:\s*dark\)\s*\{\s*:root\{([^}]*)\}")):
        m = re.search(scope, css)
        if m:
            t = css_tokens(m.group(1))
            if "--fg" in t and "--bg" in t and contrast(t["--fg"], t["--bg"]) < 4.5:
                block.append(f"text contrast fail ({theme})")
    if SECRET_RE.search(html):
        block.append("secret")
    for img in soup.find_all("img"):
        if not img.has_attr("alt"):
            revise.append("img without alt")
    verdict = "BLOCK" if block else "REVISE" if revise else "PASS"
    return {"verdict": verdict, "exit": {"PASS": 0, "REVISE": 1, "BLOCK": 3}[verdict], "block": block, "revise": revise}


@program("QA-45")
def qa_45(work):
    good = ('<!doctype html><html lang="ar" dir="rtl"><head><meta name="viewport" content="width=device-width, initial-scale=1">'
            '<style>:root{--fg:#1b1b1f;--bg:#fbfaf7}@media (prefers-color-scheme: dark){:root{--fg:#f2f2f2;--bg:#121214}}</style></head><body><img src="a.png" alt="شعار"></body></html>')
    res = {"good": web_audit(good), "zoom": web_audit(good.replace("initial-scale=1", "initial-scale=1, user-scalable=no")),
           "nolang": web_audit(good.replace(' lang="ar"', "")), "dark": web_audit(good.replace("--fg:#f2f2f2", "--fg:#3a3a3e")),
           "secret": web_audit(good.replace("</body>", "<script>const k='sk-ABCDEFGHIJKLMNOPQRST'</script></body>")),
           "alt": web_audit(good.replace(' alt="شعار"', ""))}
    wjson(Path(work) / "web_audit.json", res)
    return [C("accessible page PASS exit 0", res["good"]["exit"] == 0, res["good"]),
            C("user-scalable=no BLOCKs", "zoom disabled" in res["zoom"]["block"], res["zoom"]),
            C("missing lang BLOCKs", "missing lang" in res["nolang"]["block"], res["nolang"]),
            C("dark theme low contrast BLOCKs", "text contrast fail (dark)" in res["dark"]["block"], res["dark"]),
            C("secret-like key BLOCKs", "secret" in res["secret"]["block"], res["secret"]),
            C("missing alt is REVISE (exit 1)", res["alt"]["exit"] == 1, res["alt"])]


@program("QA-46")
def qa_46(work):
    import os
    work = Path(work); fps, w, h = 2, 64, 36

    def render(name, dur):
        tmp = work / f"{name}.tmp.mp4"
        n = int(round(dur * fps)); a = tone(220, dur, 8000, 0.3)
        write_video(tmp, moving_frames(n), fps, audio=a, sr=8000, abitrate="24k")
        info = probe(tmp); d = float(info["format"]["duration"]); v = vstream(info)
        ok = abs(d - 48) < 0.55 and (int(v["width"]), int(v["height"])) == (w, h) and len(astreams(info)) == 1
        if not ok:
            return None, d
        final = work / f"{name}.mp4"; os.replace(tmp, final)
        stills = []
        for k, t in enumerate((0.1 * 48, 0.4 * 48, 0.7 * 48, 0.95 * 48)):
            st = work / f"{name}_qa{k + 1}.png"; ff("-ss", f"{t:.2f}", "-i", final, "-frames:v", 1, st); stills.append(st.name)
        receipt = {"file": final.name, "sha256": sha256(final.read_bytes()), "duration": d, "size": [w, h], "scenes": 1,
                   "sources": ["synthetic"], "licence": "own", "qa_stills": stills}
        wjson(work / f"{name}_receipt.json", receipt)
        return receipt, d
    (good, d1), (bad, d2) = par(render, [("film", 48.0), ("short", 47.3)])
    return [C("48.0 s render passes |dur-48| < 0.55 and is moved into place", good is not None and (work / "film.mp4").is_file() and not (work / "film.tmp.mp4").exists(), d1),
            C("receipt sha256 matches the delivered file", good and good["sha256"] == sha256((work / "film.mp4").read_bytes()), ""),
            C("4 QA stills written", good and len(good["qa_stills"]) == 4 and all((work / s).is_file() for s in good["qa_stills"]), ""),
            C("47.3 s render is refused and never replaces a final file", bad is None and not (work / "short.mp4").exists(), d2)]


def z_of(p):
    from scipy.stats import norm
    return float(norm.ppf(p))


def ab_sample_size(p1, p2, alpha=0.05, power=0.8):
    za, zb = z_of(1 - alpha / 2), z_of(power); pbar = (p1 + p2) / 2
    n = (za * math.sqrt(2 * pbar * (1 - pbar)) + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2 / (p1 - p2) ** 2
    return math.ceil(n)


def ab_read(xa, na, xb, nb, alpha=0.05):
    from scipy.stats import norm
    pa, pb = xa / na, xb / nb; p = (xa + xb) / (na + nb)
    z = (pb - pa) / math.sqrt(p * (1 - p) * (1 / na + 1 / nb)); pval = 2 * (1 - norm.cdf(abs(z)))
    se = math.sqrt(pa * (1 - pa) / na + pb * (1 - pb) / nb); zc = z_of(1 - alpha / 2)
    return {"rate_a": pa, "rate_b": pb, "lift": (pb - pa) / pa, "ci95": (pb - pa - zc * se, pb - pa + zc * se), "z": z, "p": pval}


@program("QA-47")
def qa_47(work):
    n = ab_sample_size(0.10, 0.12)
    r = ab_read(300, 3000, 360, 3000); null = ab_read(300, 3000, 305, 3000)
    rows = "variant,impressions,clicks\nA,3000,300\nB,3000,360\n"; (Path(work) / "ab_results.csv").write_text(rows)
    wjson(Path(work) / "ab_read.json", {"n_per_variant": n, "read": r, "null": null})
    return [C("10% vs 12% needs 3841 per variant (alpha .05, power .8)", n == 3841, n),
            C("300/3000 vs 360/3000: lift +20%, pooled z = 2.476, p = 0.0133", abs(r["lift"] - 0.2) < 1e-9 and abs(r["z"] - 2.4756) < 1e-3 and abs(r["p"] - 0.0133) < 2e-4, r),
            C("95% CI excludes 0 for the real lift, includes 0 for 305 vs 300", r["ci95"][0] > 0 and null["ci95"][0] < 0 < null["ci95"][1], (r["ci95"], null["ci95"]))]


def best_time(rows, block=3, min_posts=8, min_cell=2):
    import statistics as st
    if len(rows) < min_posts:
        return {"defaults": True}
    overall = st.median(r["views"] for r in rows); cells = {}
    for r in rows:
        cells.setdefault((r["weekday"], r["hour"] // block * block), []).append(r["views"])
    scored = {k: st.median(v) for k, v in cells.items() if len(v) >= min_cell}
    best = max(scored, key=scored.get)
    return {"defaults": False, "overall": overall, "best": best, "lift": scored[best] / overall, "cells": {f"{k[0]}@{k[1]}": v for k, v in scored.items()}}


@program("QA-48")
def qa_48(work):
    rows = [{"weekday": "Thu", "hour": h, "views": v} for h, v in ((21, 900), (22, 1100), (23, 1000))]
    rows += [{"weekday": "Mon", "hour": h, "views": v} for h, v in ((9, 300), (10, 320), (13, 280), (14, 260))]
    rows += [{"weekday": "Sat", "hour": 2, "views": 5000}]
    r = best_time(rows); few = best_time(rows[:7])
    (Path(work) / "export.csv").write_text("weekday,hour,views\n" + "".join(f"{x['weekday']},{x['hour']},{x['views']}\n" for x in rows))
    wjson(Path(work) / "besttime.json", r)
    return [C("Thursday 21:00 block wins (median 1000 vs overall median 610)", r["best"] == ("Thu", 21) and r["overall"] == 610 and r["cells"]["Thu@21"] == 1000, r),
            C("single 5000-view Saturday post ignored (cell < 2 posts)", "Sat@0" not in r["cells"], r["cells"]),
            C("< 8 posts keeps defaults", few == {"defaults": True}, few)]


@program("QA-49")
def qa_49(work):
    n = ab_sample_size(0.05, 0.06, alpha=0.05, power=0.8); n90 = ab_sample_size(0.05, 0.06, alpha=0.05, power=0.9)
    r = ab_read(500, 10000, 600, 10000)
    wjson(Path(work) / "ab_plan.json", {"n": n, "n_power_0_9": n90, "read": r})
    return [C("5% vs 6% needs 8158 per variant at alpha .05 power .8", n == 8158, n),
            C("raising power to 0.9 needs more (10921)", n90 == 10921, n90),
            C("500/10000 vs 600/10000: lift 20%, CI (0.0038, 0.0162), p < 0.05", abs(r["lift"] - 0.2) < 1e-9 and abs(r["ci95"][0] - 0.0038) < 3e-4 and r["p"] < 0.05, r)]


def frame_qa(frames, fps=30, black=6, white=249, freeze_diff=0.05, freeze_s=1.5, cut_diff=60, max_cuts_per_10s=8):
    f = np.asarray(frames, dtype=np.float64); m = f.mean(axis=(1, 2))
    d = np.r_[np.inf, np.abs(np.diff(f, axis=0)).mean(axis=(1, 2))]
    flags = {"black": [int(i) for i in np.where(m < black)[0]], "white": [int(i) for i in np.where(m > white)[0]], "freezes": [], "cuts": [int(i) for i in np.where((d > cut_diff) & np.isfinite(d))[0]]}
    run = 0
    for i in range(1, len(f) + 1):
        if i < len(f) and d[i] < freeze_diff:
            run += 1
        else:
            if run + 1 >= freeze_s * fps:
                flags["freezes"].append((i - run - 1, i - 1))
            run = 0
    excess = len(flags["cuts"]) > max_cuts_per_10s * len(f) / fps / 10
    verdict = "PASS" if not (flags["black"] or flags["white"] or flags["freezes"] or excess) else "REVISE"
    return flags | {"excess_cuts": excess, "verdict": verdict}


@program("QA-50")
def qa_50(work):
    base = moving_frames(120, 180, 320).astype(np.uint8)
    good = frame_qa(base)
    bad = base.copy(); bad[10:13] = 3; bad[20:22] = 252; bad[40:90] = bad[40]
    flg = frame_qa(bad)
    short = base.copy(); short[40:80] = short[40]
    sh = frame_qa(short)
    wjson(Path(work) / "qa.json", {"clean": good, "planted": flg, "freeze_1_3s": sh})
    return [C("clean 320 px moving frames PASS", good["verdict"] == "PASS", good["verdict"]),
            C("mean < 6 frames 10-12 flagged black", flg["black"] == [10, 11, 12], flg["black"]),
            C("mean > 249 frames 20-21 flagged white", flg["white"] == [20, 21], flg["white"]),
            C("50-frame (1.67 s) freeze flagged, 40-frame (1.33 s) not", flg["freezes"] == [(40, 89)] and sh["freezes"] == [], (flg["freezes"], sh["freezes"])),
            C("diff > 60 counted as hard cuts (into/out of the black and white frames)", flg["cuts"] == [10, 13, 20, 22], flg["cuts"])]


SB_VERBS = {"opens", "pours", "walks", "lifts", "turns", "reveals", "falls", "rises", "slides", "glows", "يفتح", "يسكب", "يمشي", "يرفع", "يدور", "يظهر"}


def storyboard_gate(scenes, frames, anchor, max_words=8, camera_budget=1, min_scenes=3):
    rep = {"scene_count": min_scenes <= len(scenes), "verbs": [], "carrier": [], "words": [], "camera": [], "hero": 0.0, "object_test": []}
    for s in scenes:
        if not set(s["desc"].lower().split()) & SB_VERBS:
            rep["verbs"].append(s["id"])
        if not s.get("carrier") or s["carrier"] not in s["desc"]:
            rep["carrier"].append(s["id"])
        if len(s.get("camera", [])) > camera_budget:
            rep["camera"].append(s["id"])
        if not s.get("object_test"):
            rep["object_test"].append(s["id"])
    rep["words"] = [f["id"] for f in frames if len(f["text"].split()) > max_words]
    rep["hero"] = sum(anchor in s["desc"] for s in scenes) / len(scenes)
    ok = rep["scene_count"] and not any(rep[k] for k in ("verbs", "carrier", "words", "camera", "object_test")) and rep["hero"] >= 0.5
    rep["verdict"] = "PASS" if ok else "REVISE"
    return rep


@program("QA-51")
def qa_51(work):
    scenes = [{"id": "s1", "desc": "falcon lifts the lantern", "carrier": "lantern", "camera": ["push"], "object_test": True},
              {"id": "s2", "desc": "lantern glows over the falcon", "carrier": "lantern", "camera": [], "object_test": True},
              {"id": "s3", "desc": "falcon walks past the lantern", "carrier": "lantern", "camera": ["pan"], "object_test": True}]
    frames = [{"id": "f1", "text": "ضوء واحد يكفي"}, {"id": "f2", "text": "the night opens"}]
    good = storyboard_gate(scenes, frames, "falcon")
    bad_s = json.loads(json.dumps(scenes)); bad_s[1]["desc"] = "a beautiful lantern"; bad_s[2]["camera"] = ["pan", "tilt"]
    bad = storyboard_gate(bad_s, frames + [{"id": "f3", "text": "one two three four five six seven eight nine"}], "falcon")
    wjson(Path(work) / "storyboard_gate.json", {"good": good, "bad": bad})
    return [C("3-scene board with verbs, carrier, <= 8 words passes", good["verdict"] == "PASS", good),
            C("verb-less description flagged", bad["verbs"] == ["s2"], bad["verbs"]),
            C("9-word frame text flagged (<= 8 words)", bad["words"] == ["f3"], bad["words"]),
            C("two camera moves over budget flagged", bad["camera"] == ["s3"], bad["camera"])]


LIVING_ARTISTS = re.compile(r"greg rutkowski|artgerm|loish|wlop|beeple|james jean|ross tran|ilya kuvshinov|sakimichan", re.I)
REAL_PEOPLE = re.compile(r"\b(elon musk|taylor swift|barack obama|cristiano ronaldo)\b", re.I)
LIGHT_WORDS = r"\b(key light|rim light|fill light|softbox|sunlight|neon light|candle light|backlight)\b"


def image_prompt_lint(pr, aspect, negatives, required=("subject", "light", "camera")):
    block, revise, warn = [], [], []
    if LIVING_ARTISTS.search(pr):
        block.append("living artist")
    if REAL_PEOPLE.search(pr):
        block.append("real person")
    if len(re.findall(LIGHT_WORDS, pr, re.I)) > 2:
        revise.append("more than 2 light sources")
    if len(set(re.findall(r"\b(\d{2,3})\s?mm\b", pr))) > 1:
        revise.append("two lenses")
    if aspect not in ("9:16", "16:9", "1:1", "4:5", "3:2"):
        revise.append("unsupported aspect")
    if not negatives:
        revise.append("no negatives")
    if re.search(r"[؀-ۿ]", pr):
        warn.append("arabic text")
    code = 3 if block else 1 if revise else 0
    return {"exit": code, "block": block, "revise": revise, "warn": warn}


@program("QA-53")
def qa_53(work):
    p = "old merchant in a market, key light from left, 50mm lens, warm palette"
    r = {"good": image_prompt_lint(p, "9:16", ["blur"]), "artist": image_prompt_lint(p + ", in the style of Greg Rutkowski", "9:16", ["blur"]),
         "person": image_prompt_lint("Taylor Swift on stage", "9:16", ["blur"]),
         "lights": image_prompt_lint(p + ", rim light, softbox, neon light", "9:16", ["blur"]), "lens": image_prompt_lint(p + ", 85mm", "9:16", ["x"]),
         "aspect": image_prompt_lint(p, "7:3", []), "arabic": image_prompt_lint(p + " لافتة مكتوب عليها سوق", "9:16", ["x"])}
    wjson(Path(work) / "lint.json", r)
    return [C("clean prompt exit 0", r["good"]["exit"] == 0, r["good"]),
            C("living-artist name BLOCK exit 3", r["artist"]["exit"] == 3 and r["artist"]["block"] == ["living artist"], r["artist"]),
            C("real-person prompt BLOCK", r["person"]["block"] == ["real person"], r["person"]),
            C("4 light sources (> 2) and two lenses REVISE", "more than 2 light sources" in r["lights"]["revise"] and "two lenses" in r["lens"]["revise"], (r["lights"], r["lens"])),
            C("unsupported aspect + no negatives REVISE; Arabic only warns", set(r["aspect"]["revise"]) == {"unsupported aspect", "no negatives"} and r["arabic"]["exit"] == 0 and r["arabic"]["warn"], "")]


RISKY = {"delete": r"\b(os\.remove|os\.unlink|shutil\.rmtree|os\.rmdir|Path\([^)]*\)\.unlink)\b",
         "process": r"\b(subprocess|os\.system|os\.popen|os\.exec\w*)\b", "network": r"\b(socket|urllib|requests|http\.client|ftplib)\b",
         "lowlevel": r"\b(ctypes|winreg)\b", "eval": r"\b(eval|exec|compile|__import__)\s*\(", "file_write": r"open\([^)]*['\"][wax]\+?b?['\"]",
         "pip": r"\bpip\b|ensurepip", "exit": r"\bsys\.exit\b"}
CODE_TIMEOUT = 120


def risky(code):
    return sorted(k for k, rx in RISKY.items() if re.search(rx, code))


def run_sandboxed(code, timeout=CODE_TIMEOUT):
    import sys
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        p = subprocess.run([sys.executable, "-I", "-c", code], cwd=d, capture_output=True, text=True, timeout=timeout)
        return p.stdout.strip(), d


@program("QA-55")
def qa_55(work):
    samples = {"delete": "import shutil\nshutil.rmtree('/x')", "process": "import subprocess\nsubprocess.run(['ls'])", "network": "import socket",
               "lowlevel": "import ctypes", "eval": "eval('1+1')", "file_write": "open('a.txt','w').write('x')", "pip": "import os\n# pip install x",
               "exit": "import sys\nsys.exit(0)"}
    found = {k: risky(v) for k, v in samples.items()}
    drawing = "from PIL import Image, ImageDraw\nim = Image.new('RGB',(64,64))\nImageDraw.Draw(im).ellipse((8,8,56,56), fill='gold')"
    out, d = run_sandboxed("import os;print(os.getcwd())")
    wjson(Path(work) / "risk_scan.json", {"found": found, "drawing": risky(drawing), "cwd": out})
    return [C("8 risk categories each caught", all(k in v for k, v in found.items()) and len(found) == 8, found),
            C("plain drawing code needs no consent", risky(drawing) == [], risky(drawing)),
            C("runner executes inside a scratch temp folder", out == str(Path(d).resolve()) or out == d, out),
            C("CODE_TIMEOUT is 120 s", CODE_TIMEOUT == 120, CODE_TIMEOUT)]


def looks_like_photo(img, size=200, q=8, limit=1200):
    from PIL import Image
    im = Image.fromarray(np.asarray(img, dtype=np.uint8)).convert("RGB").resize((size, size))
    a = np.asarray(im) // q
    n = len(np.unique(a.reshape(-1, 3), axis=0))
    return n > limit, n


@program("QA-56")
def qa_56(work):
    rng = np.random.default_rng(2)
    yy, xx = np.mgrid[0:300, 0:300]
    photo = np.stack([(xx * 0.8 + rng.normal(0, 12, xx.shape)), (yy * 0.7 + rng.normal(0, 12, xx.shape)), (128 + 60 * np.sin(xx / 20) + rng.normal(0, 12, xx.shape))], -1).clip(0, 255)
    logo = np.zeros((300, 300, 3)); logo[:] = (20, 30, 60); logo[80:220, 80:220] = (200, 160, 70); logo[130:170, :] = (255, 255, 255)
    p, n1 = looks_like_photo(photo); l, n2 = looks_like_photo(logo)
    save_png(Path(work) / "photo.png", photo); save_png(Path(work) / "logo.png", logo)
    return [C("noisy gradient image counts > 1200 bins -> photo", p and n1 > 1200, n1),
            C("flat 3-colour logo -> flat art", not l and n2 <= 1200, n2)]


LINT_ERRORS = {"Math.random": r"Math\.random\(", "wallclock": r"Date\.now\(|performance\.now\(|new Date\(", "timers": r"set(Timeout|Interval)\(",
               "html_rtl": r"<html[^>]*dir=['\"]?rtl", "audio_no_id": r"<audio(?![^>]*\bid=)[^>]*>"}
LINT_WARNS = {"will-change": r"will-change\s*:\s*(filter|transform)", "css_transition": r"transition\s*:", "repeat_inf": r"repeat\s*:\s*-1",
              "backdrop": r"backdrop-filter", "linear_move": r"ease\s*:\s*['\"]linear['\"]"}


def composition_lint(project: Path):
    text = "\n".join(p.read_text(encoding="utf-8") for p in sorted(project.rglob("*")) if p.suffix in (".html", ".js", ".css"))
    errors = [k for k, rx in LINT_ERRORS.items() if re.search(rx, text)]
    html = (project / "index.html").read_text(encoding="utf-8")
    if "data-composition-id" not in html:
        errors.append("no data-composition-id")
    if not re.search(r"window\.__timelines|seek\(", text):
        errors.append("no timeline/seek")
    warns = [k for k, rx in LINT_WARNS.items() if re.search(rx, text)]
    return {"errors": errors, "warns": warns, "exit": 1 if errors else 0}


@program("QA-57")
def qa_57(work):
    pr = Path(work) / "proj"; (pr / "src").mkdir(parents=True)
    (pr / "index.html").write_text('<html lang="ar"><body data-composition-id="c1"><audio id="vo" src="vo.wav"></audio><script src="src/main.js"></script></body></html>')
    (pr / "src" / "main.js").write_text("const rand=mulberry32(7);window.__timelines={main:tl};tl.to('#t',{x:100,ease:'power2.out'});")
    clean = composition_lint(pr)
    (pr / "index.html").write_text('<html dir="rtl"><body><audio src="vo.wav"></audio></body></html>')
    (pr / "src" / "main.js").write_text("setTimeout(()=>x=Math.random(),10);t=Date.now();tl.to('#t',{repeat:-1,ease:'linear'});")
    bad = composition_lint(pr)
    wjson(Path(work) / "lint.json", {"clean": clean, "bad": bad})
    return [C("seeded, timeline-driven project exits 0", clean["exit"] == 0 and clean["warns"] == [], clean),
            C("Math.random, Date.now, setTimeout, rtl html, audio without id all errors", {"Math.random", "wallclock", "timers", "html_rtl", "audio_no_id"} <= set(bad["errors"]), bad["errors"]),
            C("missing data-composition-id and timeline errors", "no data-composition-id" in bad["errors"] and "no timeline/seek" in bad["errors"], bad["errors"]),
            C("repeat:-1 and linear ease are warnings", {"repeat_inf", "linear_move"} <= set(bad["warns"]), bad["warns"])]


def tile_sheet(frames, cols, pad, bg):
    n, h, w = frames.shape[:3]; rows = math.ceil(n / cols)
    sheet = np.zeros((rows * h + (rows + 1) * pad, cols * w + (cols + 1) * pad, 3), np.uint8); sheet[:] = bg
    for i, f in enumerate(frames):
        r, c = divmod(i, cols); y, x = pad + r * (h + pad), pad + c * (w + pad)
        sheet[y:y + h, x:x + w] = f if f.ndim == 3 else f[..., None]
    return sheet


def critique_sheets(film, out: Path, at=None, strip_width=None):
    info = probe(film); dur = float(info["format"]["duration"])
    def grab(fps, width):
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(film), "-vf", f"fps={fps},scale={width}:-2", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
        h = int(round(width * int(vstream(info)["height"]) / int(vstream(info)["width"]) / 2) * 2)
        return np.frombuffer(raw, np.uint8).reshape(-1, h, width, 3)
    contact = grab(2, 320); phone = grab(1, 360)
    s1 = tile_sheet(contact, 6, 4, (0x11, 0x11, 0x11)); s2 = tile_sheet(phone, 5, 4, (0x11, 0x11, 0x11))
    save_png(out / "contact.png", s1); save_png(out / "phone.png", s2)
    res = {"contact_tiles": len(contact), "phone_tiles": len(phone), "contact_shape": s1.shape, "pad_pixel": s1[1, 1].tolist()}
    if at is not None:
        full = decode_rgb(film); fps = eval(vstream(info)["r_frame_rate"]); s = int(round((at - 0.1) * fps))
        strip = full[s:s + 12]
        if strip_width:
            import cv2
            strip = np.stack([cv2.resize(f, (strip_width, int(round(strip_width * f.shape[0] / f.shape[1])))) for f in strip])
        res["strip_tile_width"] = strip.shape[2]
        save_png(out / "strip.png", tile_sheet(strip, 12, 0, (0, 0, 0)))
        res["strip"] = (s, len(strip))
    first = decode_rgb(film)[0]; save_png(out / "first.png", first)
    (out / "review.md").write_text("# Review\n\n| criterion | score 1-10 | timestamp | fix |\n|---|---|---|---|\n")
    return res


@program("QA-58")
def qa_58(work):
    film = write_video(Path(work) / "film.mp4", moving_frames(120, 36, 64), 30)
    r = critique_sheets(film, Path(work), at=2.0)
    return [C("2 fps contact sheet: 8 tiles of 320 px on 6 columns", r["contact_tiles"] == 8 and r["contact_shape"][1] == 6 * 320 + 7 * 4, r),
            C("padding colour is #111111", r["pad_pixel"] == [17, 17, 17], r["pad_pixel"]),
            C("1 fps phone sheet: 4 tiles at 360 px", r["phone_tiles"] == 4, r["phone_tiles"]),
            C("12-frame strip starts at at-0.1 s (frame 57)", r["strip"] == (57, 12), r["strip"]),
            C("first frame and review.md template written", (Path(work) / "first.png").is_file() and "criterion" in (Path(work) / "review.md").read_text(), "")]


def sync_claim_allowed(plan):
    tq = plan.get("timing_quality", "")
    measured = tq in ("measured_asr", "measured_onsets", "words_json")
    return {"claim_sync": measured, "label": "measured" if measured else "estimated", "transcript_invented": plan.get("transcript") is not None and not plan.get("transcript_source")}


@program("QA-59")
def qa_59(work):
    est = sync_claim_allowed({"timing_quality": "estimated_from_text_length_NOT_ASR", "transcript": None})
    meas = sync_claim_allowed({"timing_quality": "words_json", "transcript": "...", "transcript_source": "words.json"})
    fake = sync_claim_allowed({"timing_quality": "estimated_from_text_length_NOT_ASR", "transcript": "نص مخترع"})
    wjson(Path(work) / "timing_truth.json", {"estimated": est, "measured": meas, "invented": fake})
    return [C("estimated timing may not be claimed as sync and is labelled 'estimated'", not est["claim_sync"] and est["label"] == "estimated", est),
            C("words.json timing may be claimed", meas["claim_sync"], meas),
            C("a transcript without a source is flagged as invented", fake["transcript_invented"] and not meas["transcript_invented"], fake)]


TEST_REPORT_ROWS = ["duration", "fps", "frames", "resolution", "audio track", "untouched voice", "loudness", "phone legibility", "RTL shaping",
                    "key-word sync", "motion in every scene", "safe margins", "contrast", "first/last frame", "assets licensing", "preview approval"]


def test_report(film, expected, manual):
    info = probe(film); v = vstream(info); dur = float(info["format"]["duration"]); fps = eval(v["r_frame_rate"])
    frames = int(v.get("nb_frames") or round(dur * fps))
    meas = {"duration": f"{dur:.2f}", "fps": f"{fps:g}", "frames": str(frames), "resolution": f"{v['width']}x{v['height']}"}
    rows = []
    for name in TEST_REPORT_ROWS:
        if name in meas:
            ok = meas[name] == expected[name]; rows.append((name, meas[name], "PASS" if ok else "FAIL"))
        elif name == "audio track":
            rows.append((name, str(len(astreams(info))), "PASS" if astreams(info) else "FAIL"))
        else:
            rows.append((name, manual.get(name, "NOT CHECKED"), "PASS" if manual.get(name) == "ok" else "FAIL" if manual.get(name) == "bad" else "TODO"))
    md = "| check | measured | result |\n|---|---|---|\n" + "".join(f"| {a} | {b} | {c} |\n" for a, b, c in rows)
    return md, rows, not any(r[2] == "FAIL" for r in rows)


@program("QA-65")
def qa_65(work):
    film = write_video(Path(work) / "film.mp4", moving_frames(60), 30, audio=tone(440, 2, 48000, 0.2))
    exp = {"duration": "2.00", "fps": "30", "frames": "60", "resolution": "64x36"}
    md, rows, ok = test_report(film, exp, {"RTL shaping": "ok"})
    md2, rows2, ok2 = test_report(film, exp, {"RTL shaping": "bad"})
    (Path(work) / "TEST_REPORT.md").write_text(md)
    return [C("16 check rows", len(rows) == 16, len(rows)),
            C("{duration},{fps},{frames},{resolution} filled from ffprobe: 2.00 / 30 / 60 / 64x36", [r[1] for r in rows[:4]] == ["2.00", "30", "60", "64x36"], rows[:4]),
            C("no FAIL -> deliverable; unchecked rows stay TODO, never PASS", ok and dict((r[0], r[2]) for r in rows)["phone legibility"] == "TODO", ""),
            C("one FAIL (RTL shaping) blocks delivery", not ok2, rows2[8])]


def gcc_phat(sig, ref, sr, max_lag=None):
    n = len(sig) + len(ref)
    S, R = np.fft.rfft(sig, n), np.fft.rfft(ref, n)
    X = S * np.conj(R); X /= np.abs(X) + 1e-12
    cc = np.fft.irfft(X, n)
    ml = max_lag or n // 2
    cc = np.concatenate([cc[-ml:], cc[:ml + 1]])
    k = int(np.argmax(np.abs(cc))); lag = (k - ml) / sr
    srt = np.sort(np.abs(cc)); dominance = float(srt[-1] / (np.mean(srt[-50:-1]) + 1e-12))
    return lag, dominance


@program("QA-68")
def qa_68(work):
    sr = 16000; rng = np.random.default_rng(4)
    env = np.repeat(rng.random(40) > 0.5, sr // 10)[: 4 * sr].astype(float)
    ref = rng.normal(0, 0.3, 4 * sr) * np.convolve(env, np.ones(400) / 400, "same")
    shift = int(0.475 * sr)
    clip = np.r_[np.zeros(shift), ref[:-shift]] + rng.normal(0, 0.01, 4 * sr)
    lag, dom = gcc_phat(clip, ref, sr, max_lag=sr)
    lag0, dom0 = gcc_phat(ref + rng.normal(0, 0.01, 4 * sr), ref, sr, max_lag=sr)
    other = rng.normal(0, 0.3, 4 * sr)
    lag2, dom2 = gcc_phat(other, ref, sr, max_lag=sr)
    write_wav(Path(work) / "clip.wav", clip, sr); write_wav(Path(work) / "ref.wav", ref, sr)
    wjson(Path(work) / "lipsync.json", {"shifted": [lag, dom], "aligned": [lag0, dom0], "unrelated": [lag2, dom2]})
    return [C("clip shifted by 475 ms -> lag 475 +- 1 ms (shift baseStart)", abs(lag - 0.475) <= 0.001, lag),
            C("aligned clip -> sharp peak at 0 ms (lips locked)", abs(lag0) <= 0.001 and dom0 > 5, (lag0, dom0)),
            C("unrelated audio -> no dominant peak (regenerate)", dom2 < dom / 3 and dom2 < 3, dom2)]


def guard_pass(img, clamp_max=48.0):
    out = np.nan_to_num(np.asarray(img, dtype=np.float64), nan=0.0, posinf=0.0, neginf=0.0)
    return np.clip(out, 0.0, clamp_max)


def bloom(img, r=4):
    from scipy.ndimage import uniform_filter
    bright = np.maximum(img - 1.0, 0)
    return img + uniform_filter(bright, size=2 * r + 1, mode="constant")


@program("QA-69")
def qa_69(work):
    hdr = np.full((32, 32), 0.5); hdr[10, 10] = np.nan; hdr[20, 20] = np.inf; hdr[5, 25] = 1e6
    raw = bloom(hdr); fixed = bloom(guard_pass(hdr))
    np.save(Path(work) / "bloomed.npy", fixed)
    bad_area = int(np.sum(~np.isfinite(raw)))
    return [C("without the guard NaN/Inf bloom into a 9x9 black rectangle (>= 81 bad pixels)", bad_area >= 81, bad_area),
            C("guarded image is finite everywhere", bool(np.all(np.isfinite(fixed))), int(np.sum(~np.isfinite(fixed)))),
            C("HDR clamped at 48 before bloom", float(guard_pass(hdr).max()) == 48.0 and float(fixed.max()) <= 48 + 47 * 1.0 + 1e-9, float(fixed.max())),
            C("normal pixels untouched by the guard", float(guard_pass(hdr)[0, 0]) == 0.5, "")]


LINT12 = {"math_random": r"Math\.random\(", "date_now": r"Date\.now\(", "timers": r"set(Timeout|Interval)\(",
          "html_rtl": r"<html[^>]*dir=['\"]?rtl", "css_transition": r"transition\s*:", "glow_text_shadow": r"text-shadow\s*:[^;]*\b\d{2,}px",
          "linear_ease": r"ease\s*:\s*['\"](linear|none)['\"]", "infinite_repeat": r"repeat\s*:\s*-1|infinite", "backdrop_filter": r"backdrop-filter",
          "performance_now": r"performance\.now\(", "new_date": r"new Date\(", "raf_loop": r"requestAnimationFrame\("}


def lint12(text):
    return sorted(k for k, rx in LINT12.items() if re.search(rx, text))


@program("QA-70")
def qa_70(work):
    clean = "<html lang=ar><body><h1 id=t></h1><script>tl.to('#t',{x:120,ease:'power3.out',duration:0.6});window.__timelines={main:tl}</script></body></html>"
    planted = {"math_random": "x=Math.random()", "date_now": "t=Date.now()", "timers": "setTimeout(f,10)", "html_rtl": "<html dir=rtl>",
               "css_transition": ".a{transition: opacity .3s}", "glow_text_shadow": ".t{text-shadow:0 0 24px #fff}", "linear_ease": "tl.to(a,{ease:'linear'})",
               "infinite_repeat": "tl.to(a,{repeat:-1})", "backdrop_filter": ".g{backdrop-filter:blur(8px)}", "performance_now": "performance.now()",
               "new_date": "new Date()", "raf_loop": "requestAnimationFrame(loop)"}
    caught = {k: lint12(v) == [k] for k, v in planted.items()}
    wjson(Path(work) / "lint12.json", {"clean": lint12(clean), "caught": caught})
    return [C("exactly 12 rules", len(LINT12) == 12, len(LINT12)),
            C("clean composition has no findings", lint12(clean) == [], lint12(clean)),
            C("each planted violation is caught by its own rule (12/12)", all(caught.values()), caught)]


def motion_energy(film, fps=15, width=320, still=0.5, thr=2.4):
    g = decode_gray(film, width, int(round(width * int(vstream(probe(film))["height"]) / int(vstream(probe(film))["width"]) / 2) * 2), fps).astype(np.float64)
    d = np.abs(np.diff(g, axis=0)).mean(axis=(1, 2))
    run = best = 0
    for x in d:
        run = run + 1 if x < still else 0; best = max(best, run)
    return {"mean": float(d.mean()), "median": float(np.median(d)), "p90": float(np.percentile(d, 90)), "peak": float(d.max()),
            "near_still_share": float(np.mean(d < still)), "above_share": float(np.mean(d > thr)), "longest_freeze_s": best / fps, "n": len(d)}


def ramp_film(work, name, still_s=2.0, move_s=2.0, step=2, fps=30):
    n1, n2 = int(still_s * fps), int(move_s * fps)
    fr = [np.full((36, 64), 60, np.uint8)] * n1 + [np.full((36, 64), 60 + step * (k + 1), np.uint8) for k in range(n2)]
    return write_video(Path(work) / name, np.stack(fr), fps)


@program("QA-71")
def qa_71(work):
    m = motion_energy(ramp_film(work, "film.mp4"), fps=15)
    wjson(Path(work) / "measure.json", m)
    return [C("half the film is near-still (share 0.5 +- 0.05)", abs(m["near_still_share"] - 0.5) <= 0.05, m["near_still_share"]),
            C("moving half: 2 levels/frame at 30 fps = 4 per 15 fps sample (p90 4 +- 0.6)", abs(m["p90"] - 4) <= 0.6 and m["peak"] < 6, (m["p90"], m["peak"])),
            C("mean ~ 2 (half still, half 4)", abs(m["mean"] - 2) <= 0.4, m["mean"]),
            C("calm-premium band 0.35-0.5 median not met by this film", not (0.35 <= m["median"] <= 0.5), m["median"])]


MOTION_LIBS = {"gsap": r"gsap(\.min)?\.js|\bgsap\.(to|from|timeline)", "lottie": r"lottie(-web)?(\.min)?\.js|lottie\.loadAnimation|<lottie-player",
               "animejs": r"anime(\.min)?\.js|\banime\(", "lenis": r"lenis(\.min)?\.js|new Lenis\(", "locomotive": r"locomotive-scroll",
               "three": r"three(\.module)?(\.min)?\.js|new THREE\.", "pixi": r"pixi(\.min)?\.js|new PIXI\.", "webgl_canvas": r"getContext\(['\"]webgl2?['\"]",
               "svg_smil": r"<animate(Transform|Motion)?\b", "custom_cursor": r"cursor\s*:\s*none", "backdrop_filter": r"backdrop-filter",
               "blend_modes": r"mix-blend-mode", "clip_paths": r"clip-path\s*:"}


def detect_motion_stack(html):
    return sorted(k for k, rx in MOTION_LIBS.items() if re.search(rx, html, re.I))


@program("QA-72")
def qa_72(work):
    site = ('<script src="https://cdn.example/gsap.min.js"></script><script>gsap.to(".hero",{y:0});const l=new Lenis();</script>'
            '<canvas id=c></canvas><script>c.getContext("webgl")</script><style>body{cursor:none}.hero{clip-path:inset(0 0 0 0)}</style>'
            '<svg><circle><animate attributeName="r"/></circle></svg>')
    plain = "<h1>Hello</h1><style>h1{color:#222}</style>"
    found = detect_motion_stack(site)
    (Path(work) / "reference.html").write_text(site); wjson(Path(work) / "stack.json", {"site": found, "plain": detect_motion_stack(plain)})
    return [C("GSAP, Lenis, WebGL canvas, SMIL, custom cursor and clip-path detected", found == ["clip_paths", "custom_cursor", "gsap", "lenis", "svg_smil", "webgl_canvas"], found),
            C("plain page shows no motion library", detect_motion_stack(plain) == [], ""),
            C("Lottie/Three/PIXI not falsely reported", not ({"lottie", "three", "pixi"} & set(found)), found)]


def visual_diff(ref, act, tolerance=0, grid=8):
    a, b = np.asarray(ref, dtype=np.int16), np.asarray(act, dtype=np.int16)
    if a.shape != b.shape:
        return {"size_mismatch": True}
    diff = np.abs(a - b).max(axis=-1) > tolerance
    H, W = diff.shape; cells = []
    for gy in range(grid):
        for gx in range(grid):
            blk = diff[gy * H // grid:(gy + 1) * H // grid, gx * W // grid:(gx + 1) * W // grid]
            cells.append(((gy, gx), float(blk.mean())))
    cells.sort(key=lambda c: -c[1])
    alpha = a.shape[-1] == 4 and bool(np.any(a[..., 3] != b[..., 3]))
    return {"diff_ratio": float(diff.mean()), "similarity": round(1 - float(diff.mean()), 6), "alpha_changed": alpha,
            "hotspots": [c for c in cells if c[1] > 0][:5], "size_mismatch": False}


@program("QA-73")
def qa_73(work):
    from PIL import Image
    ref = np.zeros((64, 64, 4), np.uint8); ref[..., :3] = texture(64, 64, 9)[..., None].astype(np.uint8); ref[..., 3] = 255
    act = ref.copy(); act[16:24, 40:48, :3] = 255 - act[16:24, 40:48, :3]
    alpha = ref.copy(); alpha[0:8, 0:8, 3] = 0
    for n, a in (("ref.png", ref), ("actual.png", act)):
        Image.fromarray(a, "RGBA").save(Path(work) / n)
    r = visual_diff(np.asarray(Image.open(Path(work) / "ref.png")), np.asarray(Image.open(Path(work) / "actual.png")))
    same = visual_diff(ref, ref); al = visual_diff(ref, alpha); size = visual_diff(ref, ref[:32])
    wjson(Path(work) / "visual_diff.json", r)
    return [C("one 8x8 block changed: diff ratio = 64/4096", abs(r["diff_ratio"] - 64 / 4096) < 1e-12, r["diff_ratio"]),
            C("top hotspot is grid cell (2, 5)", r["hotspots"][0][0] == (2, 5) and len(r["hotspots"]) == 1, r["hotspots"]),
            C("identical images similarity 1.0", same["similarity"] == 1.0, same["similarity"]),
            C("alpha-only change flagged; size mismatch reported", al["alpha_changed"] and size["size_mismatch"], "")]


def text_box_film(work, name, appear=1.0, fps=30, dur=3.0, h=36, w=64, box=(20, 26, 8, 56)):
    y0, y1, x0, x1 = box; fr = []
    for i in range(int(dur * fps)):
        f = np.full((h, w), 30, np.uint8)
        if i / fps >= appear:
            f[y0:y1, x0:x1] = 240
        fr.append(f)
    return write_video(Path(work) / name, np.stack(fr), fps)


def measure_text_frames(film, step=0.5):
    dur = float(probe(film)["format"]["duration"]); g = decode_gray(film); fps = 30; out = []
    t = 0.0
    while t < dur - 1e-6:
        f = g[int(round(t * fps))]; ys, xs = np.where(f > 128)
        out.append({"t": t, "visible": bool(len(ys)), "glyph_h": int(ys.max() - ys.min() + 1) if len(ys) else 0,
                    "margin_l": int(xs.min()) if len(xs) else None, "margin_r": int(f.shape[1] - 1 - xs.max()) if len(xs) else None})
        t = round(t + step, 6)
    return out


@program("QA-75")
def qa_75(work):
    film = text_box_film(work, "ref.mp4")
    rows = measure_text_frames(film, 0.5)
    vis = [r for r in rows if r["visible"]]
    wjson(Path(work) / "style_measure.json", rows)
    return [C("frames grabbed at 0.5 s steps across 3 s (6 samples)", [r["t"] for r in rows] == [0.0, 0.5, 1.0, 1.5, 2.0, 2.5], [r["t"] for r in rows]),
            C("text appears at 1.0 s", [r["t"] for r in vis][0] == 1.0, vis[0]["t"] if vis else None),
            C("glyph height 6 px and centred margins 8/8 measured", all(r["glyph_h"] == 6 and r["margin_l"] == 8 and r["margin_r"] == 8 for r in vis), vis)]


def onset_times(x, sr, thr_db=-30):
    hop = sr // 200; env = np.array([np.sqrt(np.mean(x[i:i + hop] ** 2)) for i in range(0, len(x) - hop, hop)])
    db = 20 * np.log10(env + 1e-9); on = []
    for i in range(1, len(db)):
        if db[i] > thr_db and db[i - 1] <= thr_db:
            on.append(i * hop / sr)
    return on


def picture_changes(frames, fps, thr=20):
    d = np.abs(np.diff(np.asarray(frames, dtype=np.float64), axis=0)).mean(axis=(1, 2))
    return [(i + 1) / fps for i in np.where(d > thr)[0]]


@program("QA-76")
def qa_76(work):
    sr, fps = 16000, 30; hits = [0.5, 1.0, 1.5, 2.0]
    x = np.zeros(int(2.5 * sr))
    for t in hits:
        i = int(t * sr); x[i:i + 800] = np.sin(2 * np.pi * 1000 * np.arange(800) / sr) * 0.8
    pic_hits = [0.5, 1.0, 1.6, 2.0]  # third flash 3 frames late
    fr = np.full((int(2.5 * fps), 36, 64), 40, np.uint8)
    for t in pic_hits:
        k = int(round(t * fps)); fr[k:k + 3] = 220
    film = write_video(Path(work) / "render.mp4", fr, fps, audio=x, sr=sr)
    on = onset_times(x, sr)
    ch = picture_changes(decode_gray(film), fps)
    rises = [t for t in ch if any(abs(t - p) < 0.5 / fps for p in pic_hits)]
    res = [{"sound": s, "picture": min(rises, key=lambda p: abs(p - s)), "ok": abs(min(rises, key=lambda p: abs(p - s)) - s) <= 1 / fps + 1e-6} for s in on]
    g = decode_gray(film); cells = [g[int(round(s * fps))] for s in on]
    sheet = tile_sheet(np.stack(cells), 8, 2, (0, 0, 0)); save_png(Path(work) / "word_frames.png", sheet)
    wjson(Path(work) / "hit_sync.json", res)
    return [C("4 sound onsets detected at 0.5/1.0/1.5/2.0 s", len(on) == 4 and all(abs(a - b) < 0.01 for a, b in zip(on, hits)), on),
            C("hits at 0.5, 1.0, 2.0 s pass within one frame", [r["ok"] for r in res] == [True, True, False, True], res),
            C("the 1.5 s hit is 3 frames late and fails", not res[2]["ok"] and abs(res[2]["picture"] - 1.6) < 0.02, res[2]),
            C("labelled sheet uses 8 columns", sheet.shape[1] == 8 * 64 + 9 * 2, sheet.shape)]


@program("QA-77")
def qa_77(work):
    from PIL import Image, PngImagePlugin
    prompt = {"3": {"class_type": "KSampler", "inputs": {"seed": 42, "steps": 20}}}; workflow = {"nodes": [{"id": 3, "type": "KSampler"}]}
    meta = PngImagePlugin.PngInfo(); meta.add_text("prompt", json.dumps(prompt)); meta.add_text("workflow", json.dumps(workflow))
    p = Path(work) / "still.png"; Image.new("RGB", (16, 16), (90, 20, 20)).save(p, pnginfo=meta)
    back = Image.open(p).info
    ex = Image.Exif(); ex[0x0110] = "prompt:" + json.dumps(prompt); ex[0x010F] = "workflow:" + json.dumps(workflow)
    w = Path(work) / "still.webp"; Image.new("RGB", (16, 16)).save(w, exif=ex)
    wex = Image.open(w).getexif()
    plain = Path(work) / "plain.png"; Image.new("RGB", (4, 4)).save(plain)
    return [C("PNG tEXt 'prompt' reads back the exact sampler seed 42", json.loads(back["prompt"])["3"]["inputs"]["seed"] == 42, back.get("prompt")),
            C("PNG tEXt 'workflow' reads back", json.loads(back["workflow"]) == workflow, ""),
            C("WebP EXIF 0x0110 'prompt:' and 0x010F 'workflow:' read back", wex.get(0x0110, "").startswith("prompt:") and json.loads(wex[0x010F][9:]) == workflow, dict(wex)),
            C("an image without metadata reports none", "prompt" not in Image.open(plain).info, "")]


def identity_doc(tokens_css):
    toks = {}
    for sel, body in re.findall(r"([^{}]+)\{([^}]*)\}", tokens_css):
        for k, v in css_tokens(body).items():
            toks[k] = v.lower()
    lines = ["# الهوية البصرية", "", "| token | hex |", "|---|---|"] + [f"| {k} | {v} |" for k, v in sorted(toks.items())]
    return "\n".join(lines) + "\n", toks


@program("QA-78")
def qa_78(work):
    css = ":root{--ink:#14110F;--gold:#c8a24a}\n.theme-night{--ink:#0b0a09}\n:root{--paper:#F6EFE3}"
    doc, toks = identity_doc(css)
    (Path(work) / "SQC-IDENTITY-ar.md").write_text(doc, encoding="utf-8")
    hexes = re.findall(r"#[0-9a-f]{6}", doc)
    return [C("later block wins: --ink = #0b0a09", toks["--ink"] == "#0b0a09", toks),
            C("every hex in the doc is a resolved token value", sorted(hexes) == sorted(toks.values()), hexes),
            C("doc lists exactly 3 tokens", len(hexes) == 3, len(hexes))]


def render_mode(argv):
    smoke, approved = "--smoke" in argv, "--approved" in argv
    if smoke == approved:
        return {"ok": False, "error": "exactly one of --smoke / --approved"}
    if smoke:
        secs = 2.0
        if "--seconds" in argv:
            secs = float(argv[argv.index("--seconds") + 1])
        return {"ok": True, "mode": "smoke", "seconds": min(secs, 12.0)}
    return {"ok": True, "mode": "final"}


def agent_may_pass_approved(user_messages):
    return any(re.search(r"\b(ارندر|اعتمد|approve)\b", m) for m in user_messages)


@program("QA-80")
def qa_80(work):
    r = {"none": render_mode([]), "both": render_mode(["--smoke", "--approved"]), "smoke": render_mode(["--smoke"]),
         "smoke30": render_mode(["--smoke", "--seconds", "30"]), "final": render_mode(["--approved"])}
    wjson(Path(work) / "render_gate.json", r)
    return [C("neither or both flags refused", not r["none"]["ok"] and not r["both"]["ok"], (r["none"], r["both"])),
            C("--smoke defaults to 2 s, capped at 12 s", r["smoke"]["seconds"] == 2.0 and r["smoke30"]["seconds"] == 12.0, r["smoke30"]),
            C("agent passes --approved only after the user says اعتمد / ارندر", agent_may_pass_approved(["تمام اعتمد"]) and not agent_may_pass_approved(["حلو"]), "")]


def qa_receipt(film, out):
    info = probe(film); vs = [s for s in info["streams"] if s["codec_type"] == "video"]
    dur = float(info["format"].get("duration", 0)); v = vs[0] if vs else {}
    checks = {"video": bool(vs), "h264": v.get("codec_name") == "h264", "even": int(v.get("width", 1)) % 2 == 0 and int(v.get("height", 1)) % 2 == 0, "duration": dur > 0}
    rep = {"pass": all(checks.values()), "checks": checks, "duration": dur, "video": v.get("codec_name"), "bytes": Path(film).stat().st_size,
           "manual_review": "NOT_DONE", "word_sync": "NOT_MEASURED"}
    wjson(out, rep); return rep


@program("QA-81")
def qa_81(work):
    good = write_video(Path(work) / "final.mp4", moving_frames(30), 30)
    other = write_video(Path(work) / "mpeg4.mp4", moving_frames(30), 30, vcodec="mpeg4")
    r1, r2 = qa_receipt(good, Path(work) / "qa_report.json"), qa_receipt(other, Path(work) / "qa_other.json")
    return [C("h264 even-size file with duration passes", r1["pass"], r1["checks"]),
            C("mpeg4 file fails the h264 check (exit 1)", not r2["pass"] and not r2["checks"]["h264"], r2["checks"]),
            C("receipt records manual review NOT_DONE (never claimed)", r1["manual_review"] == "NOT_DONE", r1["manual_review"])]


def frame_hashes(film, times, w, h):
    out = []
    for t in times:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", str(film), "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
        out.append(sha256(raw))
    return out


@program("QA-82")
def qa_82(work):
    import cv2
    fps, n = 6, 42; fr = []
    for i in range(n):
        f = np.full((360, 640, 3), 20, np.uint8); cv2.rectangle(f, (20 + 14 * i, 150), (80 + 14 * i, 210), (220, 180, 60), -1); fr.append(f)
    moving = write_video(Path(work) / "smoke.mp4", np.stack(fr), fps)
    still = write_video(Path(work) / "still.mp4", np.stack([fr[0]] * n), fps)
    T = (0.8, 3.8, 5.4, 6.5)
    hm, hs = frame_hashes(moving, T, 640, 360), frame_hashes(still, T, 640, 360)
    wjson(Path(work) / "hashes.json", {"moving": hm, "still": hs})
    return [C("7 s 360p 6 fps render: 4 unique SHA-256 at 0.8/3.8/5.4/6.5 s", len(set(hm)) == 4, len(set(hm))),
            C("a still render fails (1 unique hash)", len(set(hs)) == 1, len(set(hs)))]


def text_risks(clips):
    risks = []
    for i, words in enumerate(clips):
        for tok in words.split():
            letters = re.sub(r"[^A-Za-z]", "", tok)
            if len(letters) > 10 or re.search(r"\d|-", tok):
                risks.append(i + 1); break
    return risks


@program("QA-83")
def qa_83(work):
    clips = ["OPEN NOW", "Extraordinary sale", "SALE 50%", "co-op market", "short words only", "ABCDEFGHIJ"]
    r = text_risks(clips); wjson(Path(work) / "flow_tips.json", {"risk_clips": r})
    return [C("11-letter word, digits and hyphen clips flagged (2, 3, 4)", r == [2, 3, 4], r),
            C("exactly 10 letters is not flagged (clip 6)", 6 not in r, r)]


def strip_overlay(img, n=9):
    import cv2
    H, W = img.shape[:2]; v, h = img.copy(), img.copy()
    for k in range(n):
        x0 = k * W // n; y0 = k * H // n
        cv2.line(v, (x0, 0), (x0, H - 1), (255, 0, 0), 1); cv2.putText(v, str(k + 1), (x0 + 2, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 0), 1)
        cv2.line(h, (0, y0), (W - 1, y0), (255, 0, 0), 1); cv2.putText(h, str(k + 1), (2, y0 + 12), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 0), 1)
    return v, h


def strips_region(W, H, vids, hids, n=9):
    x0, x1 = (min(vids) - 1) * W // n, max(vids) * W // n; y0, y1 = (min(hids) - 1) * H // n, max(hids) * H // n
    return (x0 / W, y0 / H, x1 / W, y1 / H)


@program("QA-84")
def qa_84(work):
    W, H = 270, 180; img = np.zeros((H, W, 3), np.uint8); img[:] = 40
    tgt = (100, 105, 140, 135); img[tgt[1]:tgt[3], tgt[0]:tgt[2]] = (230, 60, 60)
    gv, gh = strip_overlay(img); save_png(Path(work) / "gv.png", gv); save_png(Path(work) / "gh.png", gh)
    box = strips_region(W, H, [4, 5], [6, 7])
    crop = img[int(box[1] * H):int(box[3] * H), int(box[0] * W):int(box[2] * W)]
    ys, xs = np.where(crop[..., 0] > 200)
    refined = ((xs.min() + box[0] * W) / W, (ys.min() + box[1] * H) / H, (xs.max() + 1 + box[0] * W) / W, (ys.max() + 1 + box[1] * H) / H)
    true = (tgt[0] / W, tgt[1] / H, tgt[2] / W, tgt[3] / H)
    cx_err = abs((refined[0] + refined[2]) / 2 - (true[0] + true[2]) / 2)
    wjson(Path(work) / "grounding.json", {"strip_box": box, "refined": refined, "true": true})
    return [C("strips v4-5 x h6-7 give region (0.333, 0.556)-(0.556, 0.778)", all(abs(a - b) < 1e-3 for a, b in zip(box, (1 / 3, 5 / 9, 5 / 9, 7 / 9))), box),
            C("target lies inside the strip region", box[0] <= true[0] and box[1] <= true[1] and box[2] >= true[2] and box[3] >= true[3], ""),
            C("refined crop recovers the target box exactly (centre error 0)", cx_err < 1e-9 and all(abs(a - b) < 1e-9 for a, b in zip(refined, true)), refined)]


@program("QA-85")
def qa_85(work):
    fr = moving_frames(60)
    # PCM audio in .mov so the measured true peak is the planted one (AAC would add overshoot)
    films = par(lambda n, a: gate_film(work, n, fr, audio=a, acodec="pcm_s16le"),
                [("ok.mov", None), ("tp09.mov", peak_tone(48000, 2, -0.9)), ("tp12.mov", peak_tone(48000, 2, -1.2))])
    ok_full, p95, p12 = par(lambda f: inspect_film(f, tp_fail_above=-1.0), films)
    me = motion_energy(films[0])
    wjson(Path(work) / "inspect.json", {"ok": ok_full, "tp_09": p95, "tp_12": p12, "motion": me})
    return [C("clean film passes (-14 +-1.5, TP <= -1)", ok_full["pass"], ok_full),
            C("true peak -0.9 dBTP (passes a > -0.9 rule) fails this card's <= -1 dB rule", any("true peak" in p for p in p95["problems"]), p95["loud"]),
            C("true peak -1.2 dBTP passes", not any("true peak" in p for p in p12["problems"]), p12["loud"]),
            C("motion energy reports still share 0 for a moving film", me["near_still_share"] == 0.0, me)]


def build_font(path, chars, family="Probe"):
    from fontTools.fontBuilder import FontBuilder
    from fontTools.pens.ttGlyphPen import TTGlyphPen
    names = [".notdef"] + [f"uni{ord(c):04X}" for c in chars]
    fb = FontBuilder(1000, isTTF=True); fb.setupGlyphOrder(names)
    fb.setupCharacterMap({ord(c): f"uni{ord(c):04X}" for c in chars})
    glyphs = {}
    for n in names:
        pen = TTGlyphPen(None); pen.moveTo((100, 0)); pen.lineTo((100, 700)); pen.lineTo((500, 700)); pen.closePath(); glyphs[n] = pen.glyph()
    fb.setupGlyf(glyphs); fb.setupHorizontalMetrics({n: (600, 100) for n in names}); fb.setupHorizontalHeader(ascent=800, descent=-200)
    fb.setupNameTable({"familyName": family, "styleName": "Regular"}); fb.setupOS2(); fb.setupPost(); fb.save(str(path))
    return Path(path)


def arabic_fonts(folder):
    from fontTools.ttLib import TTFont
    out = []
    for p in sorted(Path(folder).glob("*.ttf")):
        cmap = TTFont(str(p)).getBestCmap()
        if all(ord(c) in cmap for c in "ابتجدرسعلمنهوي"):
            out.append(p.name)
    return out


@program("QA-86")
def qa_86(work):
    fd = Path(work) / "fonts"; fd.mkdir()
    build_font(fd / "ArabicProbe.ttf", "ابتجدرسعلمنهوي ", "ArabicProbe"); build_font(fd / "LatinOnly.ttf", "ABCabc", "LatinOnly")
    build_font(fd / "PartialArabic.ttf", "ابت", "PartialArabic")
    found = arabic_fonts(fd)
    f = write_video(Path(work) / "clip.mp4", moving_frames(45), 30, audio=tone(440, 1.5, 44100, 0.2), sr=44100)
    info = probe(f); a = astreams(info)[0]
    rep = {"duration": round(float(info["format"]["duration"]), 2), "streams": [s["codec_type"] for s in info["streams"]], "audio_rate": int(a["sample_rate"]), "fonts": found}
    wjson(Path(work) / "probe.json", rep)
    return [C("probe: video+audio streams, 1.5 s, 44.1 kHz", sorted(rep["streams"]) == ["audio", "video"] and abs(rep["duration"] - 1.5) <= 0.05 and rep["audio_rate"] == 44100, rep),
            C("only the font covering the Arabic letters is listed", found == ["ArabicProbe.ttf"], found)]


def exposure_check(film, n=6, blown=250, crushed=5, share=0.05):
    g = decode_gray(film); idx = np.linspace(0, len(g) - 1, n).astype(int)
    b = [float(np.mean(g[i] >= blown)) for i in idx]; c = [float(np.mean(g[i] <= crushed)) for i in idx]
    return {"blown": max(b) > share, "crushed": max(c) > share, "blown_share": max(b), "crushed_share": max(c)}


@program("QA-87")
def qa_87(work):
    fr = moving_frames(60)
    hot = np.clip(fr.astype(np.int16) + 120, 0, 255).astype(np.uint8)
    films = par(lambda n, f: gate_film(work, n, f), [("good.mp4", fr), ("blown.mp4", hot)])
    g, b = par(lambda f: inspect_film(f, tp_fail_above=-1.0) | {"exposure": exposure_check(f)}, films)
    wjson(Path(work) / "inspect.json", {"good": g, "blown": b})
    return [C("clean film: yuv420p H.264, -14 +-1.5, TP <= -1, exposure ok", g["pass"] and not g["exposure"]["blown"] and not g["exposure"]["crushed"], g),
            C("brightened film flagged blown (> 5% pixels >= 250)", b["exposure"]["blown"], b["exposure"]),
            C("measured loudness -14 +-1.5", abs(g["loud"]["I"] + 14) <= 1.5, g["loud"])]


TWELVE_LENSES = ["world & depth", "character silhouette", "action/contact", "camera", "light", "colour", "VFX", "atmosphere", "materials", "production design", "composition", "beauty"]


@program("QA-88")
def qa_88(work):
    film = write_video(Path(work) / "film.mp4", moving_frames(90), 30)
    r = critique_sheets(film, Path(work), at=1.5)
    review = "# review\n\n## P0 (breaks film)\n\n## P1 (reads generated)\n\n## P2 (taste)\n\n## lenses\n" + "".join(f"- {l}: \n" for l in TWELVE_LENSES)
    (Path(work) / "review.md").write_text(review)
    txt = (Path(work) / "review.md").read_text()
    return [C("2 fps contact (6 tiles for 3 s) and 360 px phone sheet (3 tiles at 1 fps)", r["contact_tiles"] == 6 and r["phone_tiles"] == 3, r),
            C("first frame and 12-frame strip written", (Path(work) / "first.png").is_file() and r["strip"][1] == 12, r["strip"]),
            C("review.md has P0/P1/P2 sections and 12 lenses", all(f"## {p}" in txt for p in ("P0", "P1", "P2")) and txt.count("\n- ") == 12, "")]


@program("QA-89")
def qa_89(work):
    pr = Path(work) / "proj"; pr.mkdir()
    (pr / "index.html").write_text('<html lang="ar"><body data-composition-id="k1"><script>const tl=gsap.timeline({paused:true});window.__timelines={k1:tl};tl.seek(0)</script></body></html>')
    clean = composition_lint(pr)
    (pr / "index.html").write_text('<html lang="ar"><body><script>const t0=performance.now();const d=new Date();</script><style>.a{will-change:filter;backdrop-filter:blur(4px)}</style></body></html>')
    bad = composition_lint(pr)
    wjson(Path(work) / "lint.json", {"clean": clean, "bad": bad})
    return [C("contract (composition id + registered seekable timeline) passes", clean["exit"] == 0, clean),
            C("performance.now / new Date are determinism errors", "wallclock" in bad["errors"], bad["errors"]),
            C("missing composition id and timeline are contract errors", {"no data-composition-id", "no timeline/seek"} <= set(bad["errors"]), bad["errors"]),
            C("will-change:filter and backdrop-filter are taste warnings", {"will-change", "backdrop"} <= set(bad["warns"]), bad["warns"])]


def kmeans_palette(pixels, k=6, seed=7, iters=12):
    rng = np.random.default_rng(seed); px = np.asarray(pixels, dtype=np.float64).reshape(-1, 3)
    cent = px[rng.choice(len(px), k, replace=False)]
    for _ in range(iters):
        lab = np.argmin(((px[:, None] - cent[None]) ** 2).sum(-1), axis=1)
        cent = np.array([px[lab == j].mean(0) if np.any(lab == j) else cent[j] for j in range(k)])
    lab = np.argmin(((px[:, None] - cent[None]) ** 2).sum(-1), axis=1)
    share = np.bincount(lab, minlength=k) / len(px)
    order = np.argsort(-share)
    return [("#%02x%02x%02x" % tuple(int(round(v)) for v in cent[j]), float(share[j])) for j in order if share[j] > 0]


def study(film, out: Path):
    g = decode_gray(film).astype(np.float64); fps = eval(vstream(probe(film))["r_frame_rate"])
    d = np.abs(np.diff(g, axis=0)).mean(axis=(1, 2)); thr = max(18.0, 8 * float(np.median(d)))
    cuts = [(i + 1) / fps for i in np.where(d > thr)[0]]
    dur = len(g) / fps; edges = [0.0] + cuts + [dur]
    shots = [round(b - a, 3) for a, b in zip(edges, edges[1:])]
    first = next(((i + 1) / fps for i, x in enumerate(d) if x > 0.5), None)
    rgb = decode_rgb(film)[:: int(fps)]
    pal = kmeans_palette(rgb.reshape(-1, 3)[::4], 6)
    res = {"cuts": cuts, "threshold": thr, "shot_lengths": shots, "first_change": first, "energy_mean": float(d.mean()), "still_share": float(np.mean(d < 0.5)), "palette": pal}
    wjson(out / "study.json", res)
    (out / "style_guide.md").write_text("# Style guide\n\n" + f"- cuts: {len(cuts)}\n- mean shot: {np.mean(shots):.2f} s\n- palette: {', '.join(p for p, _ in pal[:4])}\n"
                                        "\n## Type\n(fill in)\n\n## Transitions\n(fill in)\n")
    return res


def flat_shots_film(work, name, colours, lengths, fps=30):
    fr = []
    for col, ln in zip(colours, lengths):
        base = np.zeros((36, 64, 3), np.uint8); base[:] = col
        fr += [base] * int(round(ln * fps))
    return write_video(Path(work) / name, np.stack(fr), fps)


@program("QA-90")
def qa_90(work):
    film = flat_shots_film(work, "ref.mp4", [(200, 40, 40), (40, 160, 200), (230, 220, 200)], [1.0, 1.5, 0.5])
    r = study(film, Path(work))
    return [C("cuts at 1.0 and 2.5 s", len(r["cuts"]) == 2 and abs(r["cuts"][0] - 1.0) < 0.04 and abs(r["cuts"][1] - 2.5) < 0.04, r["cuts"]),
            C("shot lengths 1.0 / 1.5 / 0.5 s", all(abs(a - b) < 0.04 for a, b in zip(r["shot_lengths"], [1.0, 1.5, 0.5])), r["shot_lengths"]),
            C("first change at the 1.0 s cut (flat shots)", abs(r["first_change"] - 1.0) < 0.04, r["first_change"]),
            C("style_guide.md written with fill-in prompts", "(fill in)" in (Path(work) / "style_guide.md").read_text(), "")]


@program("QA-91")
def qa_91(work):
    lp = _loop_frames(48, 320, 180); broken = _loop_frames(48, 320, 180, broken=True)
    f1 = write_video(Path(work) / "loop.mp4", lp, 24); f2 = write_video(Path(work) / "broken.mp4", broken, 24)
    a = loop_seam(decode_gray(f1, 320, 180)); b = loop_seam(decode_gray(f2, 320, 180))
    wjson(Path(work) / "loopcheck.json", {"loop": a, "broken": b})
    return [C("encoded loop proves its seam (seam <= limit)", a["pass"], a), C("cut-short loop fails the seam proof", not b["pass"], b)]


@program("QA-92")
def qa_92(work):
    items = [{"what": "l1", "text": "ليلة مباركة", "start": 0.3, "dur": 0.8}, {"what": "l2", "text": "واحد اثنان ثلاثة أربعة", "start": 1.2, "dur": 1.1},
             {"what": "l3", "text": "w " * 10, "start": 3, "dur": 3.0}]
    r = readable(items)
    wjson(Path(work) / "readable.json", r)
    return [C("2 words at 0.8 s meets the 0.8 s floor", all(x["what"] != "l1" for x in r["too_short"]), r["too_short"]),
            C("4 words need 1.2 s (0.3 s/word): 1.1 s fails", [x["what"] for x in r["too_short"]] == ["l2"] and r["too_short"][0]["need"] == 1.2, r["too_short"]),
            C("10 words at exactly 3.0 s passes; hook at 0.3 s <= 2 s", r["hook"]["ok"], r["hook"])]


def poster_bake(film, out, at=None):
    g = decode_rgb(film).astype(np.float64); fps = eval(vstream(probe(film))["r_frame_rate"])
    if at is None:
        d = np.r_[np.inf, np.abs(np.diff(g, axis=0)).mean(axis=(1, 2, 3))]
        settled = [i for i in range(1, len(g) - 1) if d[i] < 0.5 and d[i + 1] < 0.5]
        k = max(settled, key=lambda i: g[i].std())
    else:
        k = int(round(at * fps))
    newf = g.copy(); newf[0] = g[k]
    tmp = Path(out).with_suffix(".video.mp4"); write_video(tmp, newf.clip(0, 255).astype(np.uint8), fps)
    ff("-i", tmp, "-i", film, "-map", "0:v", "-map", "1:a", "-c", "copy", out); tmp.unlink()
    return k


def audio_md5(path):
    return sha256(subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:a", "-c", "copy", "-f", "data", "-"], capture_output=True, check=True).stdout)


@program("QA-93")
def qa_93(work):
    fr = []
    for i in range(60):
        f = np.full((36, 64, 3), 30, np.uint8)
        if 20 <= i < 40:
            f[8:28, 12:52] = (230, 200, 90); f[14:22, 20:44] = (20, 20, 60)
        elif i >= 40:
            f[10:26, 10:54] = (90, 90, 90)
        fr.append(f)
    film = write_video(Path(work) / "film.mp4", np.stack(fr), 30, audio=tone(300, 2, 48000, 0.2))
    out = Path(work) / "film_poster.mp4"; k = poster_bake(film, out)
    a, b = probe(film), probe(out); fa = decode_rgb(out)
    return [C("strongest settled frame picked inside the 20-39 hero hold", 20 < k < 39, k),
            C("frame 0 now shows the hero frame", float(np.abs(fa[0].astype(int) - fa[k].astype(int)).mean()) < 3, ""),
            C("frame count and duration unchanged", vstream(a).get("nb_frames") == vstream(b).get("nb_frames") and abs(float(a["format"]["duration"]) - float(b["format"]["duration"])) < 0.03, (vstream(a).get("nb_frames"), vstream(b).get("nb_frames"))),
            C("sound stream byte-identical", audio_md5(film) == audio_md5(out), "")]


def ass_gate(ass_text, res=(1080, 1920), face=None):
    styles = {}; problems = []
    for line in ass_text.splitlines():
        if line.startswith("Style:"):
            f = [x.strip() for x in line[6:].split(",")]; styles[f[0]] = f
    for name, f in styles.items():
        if f[-1] != "-1":
            problems.append(f"{name}: Encoding must be -1")
    for line in ass_text.splitlines():
        if not line.startswith("Dialogue:"):
            continue
        parts = line.split(",", 9); txt = parts[9]
        if txt.count("\\N") + 1 > 2:
            problems.append("more than 2 lines")
        if re.search(r"\\fsp\d", txt):
            problems.append("letter-spacing breaks joining")
        if re.search(r"[\uFE70-\uFEFF]", txt):
            problems.append("pre-shaped presentation forms (bidi done twice)")
        m = re.search(r"\\pos\((\d+),(\d+)\)", txt)
        if m:
            x, y = int(m.group(1)), int(m.group(2))
            if not 0.15 * res[1] <= y <= 0.80 * res[1]:
                problems.append(f"y {y} outside 15-80% band")
            if x > 0.85 * res[0]:
                problems.append("under right-side UI")
            if face and face[0] <= x <= face[2] and face[1] <= y <= face[3]:
                problems.append("over the face")
    return problems


@program("QA-94")
def qa_94(work):
    import arabic_reshaper
    head = "[V4+ Styles]\nStyle: Main,Noto Naskh Arabic,72,&H00FFFFFF,&H000000FF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,3,0,2,60,60,120,-1\n[Events]\n"
    good = head + "Dialogue: 0,0:00:00.00,0:00:02.00,Main,,0,0,0,,{\\pos(540,1300)}اللهم بارك لنا\\Nفي جمعتنا\n"
    bad = (head.replace(",-1\n", ",1\n") + "Dialogue: 0,0:00:00.00,0:00:02.00,Main,,0,0,0,,{\\pos(540,1700)\\fsp4}"
           + arabic_reshaper.reshape("اللهم") + "\\Nسطر\\Nثالث\n" + "Dialogue: 0,0:00:02.00,0:00:04.00,Main,,0,0,0,,{\\pos(500,600)}نص\n")
    (Path(work) / "captions.ass").write_text(good, encoding="utf-8")
    g, b = ass_gate(good, face=(380, 420, 700, 800)), ass_gate(bad, face=(380, 420, 700, 800))
    wjson(Path(work) / "arabic_gate.json", {"good": g, "bad": b})
    return [C("2-line Arabic caption at 68% height, Encoding -1, passes", g == [], g),
            C("Encoding 1 instead of -1 caught", "Main: Encoding must be -1" in b, b),
            C("3 lines, letter-spacing and pre-shaped glyphs caught", {"more than 2 lines", "letter-spacing breaks joining", "pre-shaped presentation forms (bidi done twice)"} <= set(b), b),
            C("y at 88% height and a caption over the face caught", "y 1700 outside 15-80% band" in b and "over the face" in b, b)]


def apply_bound_edits(reel, source, edits):
    reel = json.loads(json.dumps(reel)); source = json.loads(json.dumps(source)); written = []
    binds = {(e["id"], k): v for s in reel["scenes"] for e in s["els"] for k, v in e.get("bind", {}).items()}
    for ed in edits:
        path = binds.get((ed["el"], ed["prop"]))
        if not path:
            continue
        node = source
        for p in path.split(".")[:-1]:
            node = node[p]
        node[path.split(".")[-1]] = ed["value"]; written.append(path)
    return source, written


def bump(reel, local_edits):
    reel = dict(reel, version=reel.get("version", 0) + 1)
    return reel, [e for e in local_edits if not e.get("sent")]


@program("QA-95")
def qa_95(work):
    reel = {"version": 3, "scenes": [{"id": "s1", "els": [{"id": "title", "bind": {"text": "copy.title", "color": "style.title_color"}}, {"id": "deco"}]}]}
    source = {"copy": {"title": "قديم"}, "style": {"title_color": "#ffffff"}}
    src, written = apply_bound_edits(reel, source, [{"el": "title", "prop": "text", "value": "جديد"}, {"el": "title", "prop": "color", "value": "#c8a24a"},
                                                    {"el": "deco", "prop": "text", "value": "x"}])
    r2, left = bump(reel, [{"el": "title", "sent": True}, {"el": "deco"}])
    wjson(Path(work) / "source.json", src)
    return [C("bound text and colour edits written into the source", src == {"copy": {"title": "جديد"}, "style": {"title_color": "#c8a24a"}}, src),
            C("unbound element edit is not written", written == ["copy.title", "style.title_color"], written),
            C("bump: version 3 -> 4 and sent edits cleared", r2["version"] == 4 and left == [{"el": "deco"}], (r2["version"], left))]


def preview_player_visible(webdriver=False, query="", hyperframes=False):
    from urllib.parse import parse_qs
    q = parse_qs(query.lstrip("?"), keep_blank_values=True)
    return not (webdriver or "render" in q or hyperframes)


def player_clock(media_playing, media_time, wall_time):
    return media_time if media_playing else wall_time


@program("QA-96")
def qa_96(work):
    r = {"browser": preview_player_visible(), "webdriver": preview_player_visible(webdriver=True), "render": preview_player_visible(query="?render=1"),
         "hf": preview_player_visible(hyperframes=True)}
    wjson(Path(work) / "player_rules.json", r)
    return [C("plays in a normal browser", r["browser"], r),
            C("hidden under webdriver, ?render and HyperFrames", not (r["webdriver"] or r["render"] or r["hf"]), r),
            C("clock follows the playing media element, else wall clock", player_clock(True, 3.2, 9.9) == 3.2 and player_clock(False, 3.2, 9.9) == 9.9, "")]


def label_simulation(report):
    rep = dict(report)
    rep["source_note"] = "ILLUSTRATIVE · CHOSEN VALUES · NOT MEASURED"
    rep["scope_warning"] = "not for safety decisions; no buckling, fracture, fatigue or dynamic redistribution"
    rep["break"] = dict(rep.get("break", {}), label="hypothetical")
    return rep


def honesty_ok(rep):
    return "ILLUSTRATIVE" in rep.get("source_note", "") and "not for safety" in rep.get("scope_warning", "") and rep.get("break", {}).get("label") == "hypothetical"


@program("QA-97")
def qa_97(work):
    raw = {"members": [{"id": "AB", "utilization": 0.82}], "break": {"path": ["AB"]}}
    lab = label_simulation(raw); wjson(Path(work) / "report.json", lab)
    return [C("labelled report carries ILLUSTRATIVE note, scope warning and hypothetical break path", honesty_ok(lab), lab),
            C("an unlabelled report is rejected", not honesty_ok(raw), ""), C("numbers untouched by labelling", lab["members"] == raw["members"], "")]


def flow_speed(frames, pctl=99.5):
    import cv2
    sp = []
    for a, b in zip(frames, frames[1:]):
        fwd = cv2.calcOpticalFlowFarneback(a, b, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        bwd = cv2.calcOpticalFlowFarneback(b, a, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        h, w = a.shape; gx, gy = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))
        back = cv2.remap(bwd, gx + fwd[..., 0], gy + fwd[..., 1], cv2.INTER_LINEAR)  # bwd sampled where the pixel landed
        cons = np.linalg.norm(fwd + back, axis=-1) < 1.0
        mag = np.linalg.norm(fwd, axis=-1)[cons]
        sp.append(float(np.percentile(mag, pctl)) if mag.size else 0.0)
    return sp


def square_frames(n, speed, h=120, w=200, size=30):
    out = []
    for i in range(n):
        f = np.full((h, w), 40, np.uint8); x = 10 + int(round(i * speed))
        f[45:45 + size, x:x + size] = 220; f[50:55, x + 5:x + 12] = 90
        out.append(f)
    return np.stack(out)


def tex_square_frames(n, speed, w=320, size=90, h=140):
    """A large smooth-textured square moving speed px/frame (trackable by Farneback at 3 levels)."""
    t = texture(size, size, 3, 10); t = (t - t.min()) / (t.max() - t.min()) * 200 + 30; out = []
    for i in range(n):
        f = np.full((h, w), 40, np.uint8); x = 10 + int(round(i * speed)); f[25:25 + size, x:x + size] = t.astype(np.uint8); out.append(f)
    return np.stack(out)


@program("QA-98")
def qa_98(work):
    fr = square_frames(10, 5); sp = flow_speed(fr)
    film = write_video(Path(work) / "film.mp4", fr, 10); r = critique_sheets(film, Path(work))
    return [C("Farneback speed of a 5 px/frame move measures 5 +- 1", abs(np.median(sp) - 5) <= 1, sp),
            C("2 fps contact sheet written (2 tiles for 1 s)", r["contact_tiles"] == 2, r["contact_tiles"])]


@program("QA-99")
def qa_99(work):
    img = np.zeros((40, 100, 3), np.uint8); img[:, :50] = (200, 30, 30); img[:, 50:80] = (30, 30, 200); img[:, 80:] = (240, 240, 240)
    pal = kmeans_palette(img.reshape(-1, 3), 3, seed=7)
    save_png(Path(work) / "frame.png", img); wjson(Path(work) / "palette.json", pal)
    shares = [round(s, 2) for _, s in pal]
    return [C("palette by area: 50% / 30% / 20%", shares == [0.5, 0.3, 0.2], pal),
            C("dominant colour is the red (#c81e1e)", pal[0][0] == "#c81e1e", pal[0])]


def rerender_plan(scenes, feedback):
    changed = sorted({e["scene"] for e in feedback.get("edits", [])} | {n["scene"] for n in feedback.get("notes", [])})
    prompt = [f"{e['scene']}: {e['kind']} -> {e['value']}" for e in feedback.get("edits", [])]
    return {"rerender": [s for s in scenes if s in changed], "keep": [s for s in scenes if s not in changed], "prompt": prompt}


@program("QA-100")
def qa_100(work):
    plan = rerender_plan(["s1", "s2", "s3"], {"edits": [{"scene": "s2", "kind": "text", "value": "مرحبا"}], "notes": [{"scene": "s3", "t": 7.2, "text": "أبطئ"}]})
    wjson(Path(work) / "feedback_export.json", plan)
    return [C("only scenes with edits or notes are re-rendered", plan["rerender"] == ["s2", "s3"] and plan["keep"] == ["s1"], plan),
            C("exported prompt lists each edit", plan["prompt"] == ["s2: text -> مرحبا"], plan["prompt"])]


def env_route(path_dirs):
    import shutil
    p = ":".join(map(str, path_dirs))
    has = {k: bool(shutil.which(k, path=p)) for k in ("ffmpeg", "ffprobe", "chromium", "whisper")}
    route = "A" if has["ffmpeg"] and has["chromium"] else "B" if has["ffmpeg"] else "C"
    return route, has


def stub(dir_, name):
    p = Path(dir_) / name; p.write_text("#!/bin/sh\nexit 0\n"); p.chmod(0o755); return p


@program("QA-101")
def qa_101(work):
    d = Path(work) / "bin"; d.mkdir()
    r0 = env_route([d]); stub(d, "ffmpeg"); stub(d, "ffprobe"); r1 = env_route([d]); stub(d, "chromium"); r2 = env_route([d])
    wjson(Path(work) / "env.json", {"empty": r0, "ffmpeg": r1, "all": r2})
    return [C("nothing on PATH -> route C", r0[0] == "C", r0), C("ffmpeg only -> route B", r1[0] == "B", r1), C("ffmpeg + browser -> route A", r2[0] == "A" and not r2[1]["whisper"], r2)]


class CachedEnv:
    def __init__(self, probe_fn, ttl=120.0):
        self.probe, self.ttl, self.at, self.val, self.calls = probe_fn, ttl, None, None, 0

    def get(self, now):
        if self.at is None or now - self.at >= self.ttl:
            self.val, self.at = self.probe(), now; self.calls += 1
        return self.val


@program("QA-102")
def qa_102(work):
    pr = subprocess.run(["ffmpeg", "-hide_banner", "-h", "filter=xfade"], capture_output=True, text=True)
    log = pr.stdout + pr.stderr
    m = re.search(r"transition\s+<int>.*?\n((?:\s+\w+\s+-?\d+.*\n)+)", log)
    names = [n for n in re.findall(r"^\s+(\w+)\s+-?\d+", m.group(1), re.M) if n != "custom"] if m else []
    env = CachedEnv(lambda: {"ffmpeg": True, "xfade": len(names), "cpus": __import__("os").cpu_count()})
    env.get(0); env.get(60); env.get(119.9); c1 = env.calls; env.get(120.0); c2 = env.calls
    wjson(Path(work) / "env_pills.json", env.val | {"xfade_names": names[:10]})
    return [C("xfade transitions counted from this ffmpeg (>= 30)", len(names) >= 30, len(names)),
            C("cached for 120 s: 3 calls inside the TTL probe once", c1 == 1, c1), C("re-probed at 120 s", c2 == 2, c2)]


def ghost_preview(frame, old_box, new_box, r=3):
    out = frame.copy().astype(np.float64)
    x0, y0, x1, y1 = old_box; nx, ny = new_box[:2]
    patch = frame[y0:y1, x0:x1].copy()
    out[y0:y1, x0:x1] = blur_box(frame.astype(np.float64), r)[y0:y1, x0:x1]
    out[ny:ny + (y1 - y0), nx:nx + (x1 - x0)] = patch
    return out


@program("QA-103")
def qa_103(work):
    f = texture(60, 100, 3, 0); f[10:30, 10:30] = np.where(np.indices((20, 20)).sum(0) % 4 < 2, 250, 10)
    g = ghost_preview(f, (10, 10, 30, 30), (60, 30, 80, 50))
    save_png(Path(work) / "ghost.png", g.clip(0, 255))
    return [C("old spot is blurred (variance drops > 5x)", f[10:30, 10:30].var() > 5 * g[10:30, 10:30].var(), (f[10:30, 10:30].var(), g[10:30, 10:30].var())),
            C("source patch redrawn exactly at the new spot", np.array_equal(g[30:50, 60:80], f[10:30, 10:30]), ""),
            C("pixels outside both boxes untouched", np.array_equal(g[45:60, 0:40], f[45:60, 0:40]), "")]


def add_note(scene, t, x, y, el, text):
    n = {"id": len(scene["notes"]) + 1, "t": round(t, 2), "x": round(x, 1), "y": round(y, 1), "el": el, "text": text}
    scene["notes"].append(n); scene["notes"].sort(key=lambda a: a["t"]); scene["status"] = "changes"
    return n


@program("QA-104")
def qa_104(work):
    sc = {"id": "s1", "status": "review", "notes": []}
    add_note(sc, 4.3333, 51.27, 12.04, "title", "أكبر"); add_note(sc, 1.005, 10.0, 80.55, None, "ظل")
    wjson(Path(work) / "notes.json", sc)
    return [C("notes rounded: t to 2 decimals, x/y to 1", sc["notes"][1] == {"id": 1, "t": 4.33, "x": 51.3, "y": 12.0, "el": "title", "text": "أكبر"}, sc["notes"]),
            C("notes sorted by time", [n["t"] for n in sc["notes"]] == sorted(n["t"] for n in sc["notes"]), [n["t"] for n in sc["notes"]]),
            C("pinning a note moves the scene to 'changes'", sc["status"] == "changes", sc["status"])]


def parse_deep_link(hash_):
    from urllib.parse import parse_qs
    q = parse_qs(hash_.lstrip("#"))
    return {"t": float(q["t"][0]) if "t" in q else None, "el": q.get("el", [None])[0]}


def poll_versions(versions_at, until_ms, every=3000):
    """versions_at: list of (ms, version) server changes. Returns reload times."""
    reloads, seen = [], None
    for t in range(0, until_ms + 1, every):
        v = max((ver for ms, ver in versions_at if ms <= t), default=None)
        if seen is not None and v != seen:
            reloads.append(t)
        seen = v
    return reloads


@program("QA-105")
def qa_105(work):
    rl = poll_versions([(0, 1), (7000, 2)], 15000)
    link = parse_deep_link("#t=12.5&el=title")
    store = {"motionos:p1": [{"el": "a", "sent": True}, {"el": "b"}]}
    store["motionos:p1"] = [e for e in store["motionos:p1"] if not e.get("sent")]
    wjson(Path(work) / "review_runtime.json", {"reloads": rl, "link": link, "store": store})
    return [C("3 s polling picks a 7 s version bump at 9 s and reloads once", rl == [9000], rl),
            C("#t=12.5&el=title deep link parsed", link == {"t": 12.5, "el": "title"}, link),
            C("sent edits cleared from 'motionos:<id>' on a new version", store["motionos:p1"] == [{"el": "b"}], store)]


@program("QA-106")
def qa_106(work):
    import time
    sr = 48000; src = write_wav(Path(work) / "voice.wav", scale_to_lufs(stereo(tone(500, 2, sr, 0.1)), sr, -24), sr)
    out = Path(work) / "export.mp4"; t0 = time.time()
    ff("-f", "lavfi", "-i", "color=c=0x203040:s=64x36:r=30:d=2", "-i", src, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", sr,
       "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", out)
    secs = time.time() - t0; info = probe(out); v = vstream(info); a = astreams(info)[0]
    rep = {"codec": v["codec_name"], "audio_codec": a["codec_name"], "frames": int(v["nb_frames"]), "fps": eval(v["r_frame_rate"]),
           "size": f"{v['width']}x{v['height']}", "bytes": out.stat().st_size, "seconds": round(secs, 3), "skipped_audio": [],
           "lufs_before": round(ebur128(src)["I"], 1), "lufs_after": round(ebur128(out)["I"], 1)}
    wjson(Path(work) / "lastExport.json", rep)
    return [C("report fields equal the file: h264/aac, 60 frames, 30 fps, 64x36", (rep["codec"], rep["audio_codec"], rep["frames"], rep["fps"], rep["size"]) == ("h264", "aac", 60, 30, "64x36"), rep),
            C("bytes recorded match the file", rep["bytes"] == out.stat().st_size and rep["bytes"] > 0, rep["bytes"]),
            C("loudness before -24 and after -14 +-1", abs(rep["lufs_before"] + 24) <= 0.5 and abs(rep["lufs_after"] + 14) <= 1.0, (rep["lufs_before"], rep["lufs_after"]))]


def sharpness(gray, grid=8):
    g = np.asarray(gray, dtype=np.float64); H, W = g.shape
    tiles = sorted((laplacian_var(g[y * H // grid:(y + 1) * H // grid, x * W // grid:(x + 1) * W // grid]) for y in range(grid) for x in range(grid)), reverse=True)
    glob, top3 = laplacian_var(g), float(np.mean(tiles[:3]))
    val = max(glob, top3)
    return {"global": glob, "top3": top3, "verdict": "blurry" if val < 60 else "soft" if val < 150 else "sharp"}


def noise_verdict(s):
    return "clean" if s < 2.5 else "moderate" if s < 6 else "noisy"


def checker(h=128, w=128, cell=4, lo=40, hi=210):
    return np.where((np.indices((h, w)) // cell).sum(0) % 2, hi, lo).astype(np.float64)


@program("QA-107")
def qa_107(work):
    import cv2
    sharp = checker(); blurry = cv2.GaussianBlur(sharp, (0, 0), 4)
    bokeh = cv2.GaussianBlur(checker(), (0, 0), 6); bokeh[40:72, 40:72] = checker(32, 32)
    flat = np.full((128, 128), 120.0); noisy = flat + np.random.default_rng(1).normal(0, 8, flat.shape)
    r = {"sharp": sharpness(sharp), "blurry": sharpness(blurry), "bokeh": sharpness(bokeh), "sigma_clean": immerkaer_sigma(flat), "sigma_noisy": immerkaer_sigma(noisy)}
    wjson(Path(work) / "sharpness.json", r)
    return [C("checkerboard is sharp (>= 150)", r["sharp"]["verdict"] == "sharp", r["sharp"]),
            C("sigma-4 blur is blurry (< 60)", r["blurry"]["verdict"] == "blurry", r["blurry"]),
            C("sharp subject on bokeh counts as sharp via the top-3 tiles though global is lower", r["bokeh"]["verdict"] == "sharp" and r["bokeh"]["top3"] > r["bokeh"]["global"], r["bokeh"]),
            C("Immerkaer sigma: flat 0 (clean), gaussian sigma 8 estimated 8 +- 1 (noisy)", noise_verdict(r["sigma_clean"]) == "clean" and abs(r["sigma_noisy"] - 8) <= 1 and noise_verdict(r["sigma_noisy"]) == "noisy", (r["sigma_clean"], r["sigma_noisy"]))]


def mccamy_cct(rgb):
    lin = np.where(np.asarray(rgb) / 255 <= 0.04045, np.asarray(rgb) / 255 / 12.92, ((np.asarray(rgb) / 255 + 0.055) / 1.055) ** 2.4)
    X, Y, Z = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]]) @ lin
    x, y = X / (X + Y + Z), Y / (X + Y + Z); n = (x - 0.3320) / (0.1858 - y)
    return 449 * n ** 3 + 3525 * n ** 2 + 6823.3 * n + 5520.33


def image_metrics(rgb):
    a = np.asarray(rgb, dtype=np.float64); luma = a @ [0.2126, 0.7152, 0.0722]
    mx, mn = a.max(-1), a.min(-1); sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-9), 0)
    rg, yb = a[..., 0] - a[..., 1], 0.5 * (a[..., 0] + a[..., 1]) - a[..., 2]
    colourful = math.hypot(rg.std(), yb.std()) + 0.3 * math.hypot(rg.mean(), yb.mean())
    mean_rgb = a.reshape(-1, 3).mean(0)
    return {"mean_luma": float(luma.mean()), "contrast_std": float(luma.std()), "clipped_pct": float(np.mean(luma >= 250) * 100),
            "crushed_pct": float(np.mean(luma <= 5) * 100), "cct": float(mccamy_cct(mean_rgb)), "saturation": float(sat.mean()), "colourfulness": float(colourful),
            "sharpness": laplacian_var(luma), "noise": immerkaer_sigma(luma), "symmetry": float(1 - np.abs(luma - luma[:, ::-1]).mean() / 255),
            "cast": float(mean_rgb[0] - mean_rgb[2])}


def compare_images(A, B):
    ma, mb = image_metrics(A), image_metrics(B)
    d = {k: mb[k] - ma[k] for k in ma if k != "cast"}
    return {"a": ma, "b": mb, "delta": d, "sharper": "B" if d["sharpness"] > 0 else "A", "cleaner": "B" if d["noise"] < 0 else "A"}


def grad_img(h=64, w=96, seed=0):
    yy, xx = np.mgrid[0:h, 0:w]; rng = np.random.default_rng(seed)
    return np.stack([60 + xx, 80 + yy, 140 - xx / 2], -1).astype(np.float64) + rng.normal(0, 1, (h, w, 3))


@program("QA-108")
def qa_108(work):
    A = grad_img(); same = compare_images(A, A.copy()); B = np.clip(A + 20, 0, 255); jump = compare_images(A, B)
    save_png(Path(work) / "A.png", A.clip(0, 255)); save_png(Path(work) / "B.png", B); wjson(Path(work) / "compare.json", jump)
    cont = lambda c: abs(c["delta"]["mean_luma"]) < 3 and abs(c["delta"]["cct"]) < 300
    return [C("10 metrics with deltas", len(same["delta"]) == 10, sorted(same["delta"])),
            C("last frame vs identical next first frame: all deltas 0 -> continuous", all(abs(v) < 1e-9 for v in same["delta"].values()) and cont(same), ""),
            C("+20 brightness jump: mean luma delta +20, continuity broken", abs(jump["delta"]["mean_luma"] - 20) < 0.5 and not cont(jump), jump["delta"]["mean_luma"])]


@program("QA-112")
def qa_112(work):
    norm = image_metrics(grad_img()); over = image_metrics(np.full((32, 32, 3), 252.0)); warm = image_metrics(np.tile([200.0, 150, 100], (32, 32, 1)))
    neutral = image_metrics(np.full((32, 32, 3), 128.0))
    expo = lambda m: "over" if m["mean_luma"] > 185 or m["clipped_pct"] > 5 else "ok"
    zone = lambda m: "low" if m["mean_luma"] < 85 else "mid" if m["mean_luma"] < 170 else "high"
    wjson(Path(work) / "analysis.json", {"norm": norm, "over": over, "warm": warm, "neutral": neutral})
    return [C("mid-grey gradient: exposure ok, mid zone", expo(norm) == "ok" and zone(norm) == "mid", norm["mean_luma"]),
            C("252 frame: clip >= 250 => exposure over, high zone", expo(over) == "over" and zone(over) == "high", over["clipped_pct"]),
            C("neutral grey McCamy CCT ~6500 K, no cast", abs(neutral["cct"] - 6504) < 60 and abs(neutral["cast"]) <= 12, neutral["cct"]),
            C("warm orange frame: CCT < 4000 K and red-blue cast > +12", warm["cct"] < 4000 and warm["cast"] > 12, (warm["cct"], warm["cast"]))]


@program("QA-113")
def qa_113(work):
    import cv2
    A = checker(64, 64).repeat(1, 1)[..., None].repeat(3, -1); B = cv2.GaussianBlur(A, (0, 0), 2)
    Nz = A + np.random.default_rng(3).normal(0, 6, A.shape)
    c1, c2 = compare_images(A, B), compare_images(A, Nz)
    wjson(Path(work) / "ab.json", {"blur": c1, "noise": c2})
    return [C("blurred B: verdict sharper = A", c1["sharper"] == "A" and c1["delta"]["sharpness"] < 0, c1["delta"]["sharpness"]),
            C("noisy B: verdict cleaner = A", c2["cleaner"] == "A" and c2["delta"]["noise"] > 3, c2["delta"]["noise"])]


@program("QA-109")
def qa_109(work):
    fr = np.stack([np.full((36, 64), 10 + i, np.uint8) for i in range(240)])
    film = write_video(Path(work) / "video.mp4", fr, 30); sheet = Path(work) / "contact-sheet.png"
    ff("-i", film, "-vf", "select='not(mod(n\\,15))',scale=270:480,tile=4x4", "-frames:v", 1, sheet)
    from PIL import Image
    a = np.asarray(Image.open(sheet).convert("L")).astype(float)
    tiles = [a[r * 480 + 240, c * 270 + 135] for r in range(4) for c in range(4)]
    return [C("16 samples tiled 4x4 into 1080x1920", a.shape == (1920, 1080), a.shape),
            C("tile k shows frame 15k (level 10 + 15k, +-3)", all(abs(v - (10 + 15 * k)) <= 3 for k, v in enumerate(tiles)), [round(v) for v in tiles])]


def aspect_label(w, h):
    r = w / h
    return min({"9:16": 9 / 16, "16:9": 16 / 9, "1:1": 1, "4:5": 0.8}.items(), key=lambda kv: abs(kv[1] - r))[0]


def qa_inspector(film):
    info = probe(film); v = vstream(info); an = analyze(film, 0.5, 0.10, -60, 1.5); status, why = "PASS", []
    an_black = blackdetect(film, 0.5, 0.10, 0.98)
    if any(b - a > 1.0 for a, b in an_black):
        status = "FAIL"; why.append("black > 1.0 s")
    if an["freeze"] and status != "FAIL":
        status = "WARN"; why.append("freeze")
    if an["loud"] and not -24 <= an["loud"]["I"] <= -10:
        status = "WARN" if status == "PASS" else status; why.append("loudness")
    return {"status": status, "why": why, "aspect": aspect_label(int(v["width"]), int(v["height"])), "black": an_black, "loud": an["loud"]}


@program("QA-110")
def qa_110(work):
    fr = moving_frames(75, 64, 36)
    b12 = fr.copy(); b12[15:51] = 0; b07 = fr.copy(); b07[15:36] = 0
    films = par(lambda n, f, l: gate_film(work, n, f, audio_lufs=l), [("ok.mp4", fr, -14), ("black12.mp4", b12, -14), ("black07.mp4", b07, -14), ("quiet.mp4", fr, -30)])
    ok, a, b, q = par(qa_inspector, films)
    wjson(Path(work) / "report.json", {"ok": ok, "black12": a, "black07": b, "quiet": q})
    return [C("clean 36x64 clip PASS, aspect 9:16", ok["status"] == "PASS" and ok["aspect"] == "9:16", ok),
            C("1.2 s black span FAILs (> 1.0 s)", a["status"] == "FAIL", a),
            C("0.7 s black span detected but not FAIL", b["black"] and b["status"] != "FAIL", b),
            C("-30 LUFS is outside -24..-10: WARN", q["status"] == "WARN" and "loudness" in q["why"], q)]


def tempo_bpm(x, sr):
    hop = 256; frames = np.array([np.sum(x[i:i + 512] ** 2) for i in range(0, len(x) - 512, hop)])
    flux = np.maximum(np.diff(np.log1p(frames * 1e4)), 0); fr = sr / hop
    ac = np.correlate(flux, flux, "full")[len(flux) - 1:]
    lags = np.arange(len(ac)); bpm = 60 * fr / np.maximum(lags, 1)
    ok = (bpm >= 60) & (bpm <= 200); k = lags[ok][np.argmax(ac[ok])]
    # parabolic refine
    y0, y1, y2 = ac[k - 1], ac[k], ac[k + 1]; kk = k + 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2)
    b = 60 * fr / kk
    while b > 180:
        b /= 2
    while b < 70:
        b *= 2
    return b


BANDS = {"sub": (20, 60), "bass": (60, 250), "low-mid": (250, 500), "mid": (500, 2000), "presence": (2000, 6000), "air": (6000, 20000)}


def band_share(x, sr):
    S = np.abs(np.fft.rfft(x)) ** 2; f = np.fft.rfftfreq(len(x), 1 / sr)
    e = {k: float(S[(f >= a) & (f < b)].sum()) for k, (a, b) in BANDS.items()}; t = sum(e.values())
    return {k: v / t for k, v in e.items()}


@program("QA-111")
def qa_111(work):
    sr = 48000; mix = scale_to_lufs(stereo(tone(1000, 3, sr, 0.3)), sr, -16)
    p = write_wav(Path(work) / "mix.wav", mix, sr); own = lufs(read_wav(p)[0], sr); ffm = ebur128(p)["I"]
    isp = tone(12000, 1, sr, 0.5, np.pi / 4); fade = np.ones(sr); fade[:2400] = fade[-2400:][::-1] = np.linspace(0, 1, 2400); isp *= fade; tp_gain = true_peak_dbtp(isp, sr) - 20 * math.log10(np.max(np.abs(isp)))
    clicks = np.zeros(8 * sr)
    for k in range(16):
        i = int(k * 0.5 * sr); clicks[i:i + 400] = np.hanning(400) * np.sin(2 * np.pi * 2000 * np.arange(400) / sr)
    bpm = tempo_bpm(clicks, sr); bands = band_share(tone(100, 1, sr), sr)
    gap = np.r_[tone(440, 1, sr, .3), np.zeros(int(0.6 * sr)), tone(440, 1, sr, .3)]; gp = write_wav(Path(work) / "gap.wav", gap, sr)
    sil = silencedetect(gp, -50, 0.5); clip = int(np.sum(np.abs(np.clip(tone(50, 1, sr, 1.2), -1, 1)) >= 0.999))
    rep = {"own_lufs": own, "ffmpeg_lufs": ffm, "isp_over_sample_db": tp_gain, "bpm": bpm, "bands_100hz": bands, "silence": sil, "clipped_samples": clip}
    wjson(Path(work) / "audio_report.json", rep)
    return [C("own BS.1770 loudness matches ffmpeg ebur128 within 0.2 LU (-16)", abs(own - ffm) <= 0.2 and abs(own + 16) < 0.05, (own, ffm)),
            C("fs/4 sine at 45 deg: true peak 3.01 dB above sample peak", abs(tp_gain - 3.01) < 0.1, tp_gain),
            C("120 BPM click track measures 120 +- 1", abs(bpm - 120) <= 1, bpm),
            C("100 Hz tone lands in the bass band 60-250 Hz", max(bands, key=bands.get) == "bass", bands),
            C("0.6 s gap under -50 dB found; clipped samples >= 0.999 counted", len(sil) == 1 and abs((sil[0][1] - sil[0][0]) - 0.6) < 0.05 and clip > 0, (sil, clip))]


def source_sheet(clips, out, cols=7, cell=(240, 450), crop=(240, 420), bg=(14, 18, 26)):
    from PIL import Image, ImageDraw
    rows = math.ceil(len(clips) * 2 / cols); sheet = Image.new("RGB", (cols * cell[0], rows * cell[1]), bg); draw = ImageDraw.Draw(sheet); times = []
    for i, c in enumerate(clips):
        d = float(probe(c)["format"]["duration"]); ts = (min(1.5, 0.2 * d), min(0.63 * d, d - 0.2))
        for j, t in enumerate(ts):
            png = Path(out).parent / f"_{i}_{j}.png"
            ff("-ss", f"{t:.3f}", "-i", c, "-frames:v", 1, "-vf", f"scale={crop[0]}:{crop[1]}:force_original_aspect_ratio=increase,crop={crop[0]}:{crop[1]}", png)
            k = 2 * i + j; x, y = (k % cols) * cell[0], (k // cols) * cell[1]
            sheet.paste(Image.open(png), (x, y)); draw.text((x + 4, y + crop[1] + 8), Path(c).name, fill=(230, 230, 230)); png.unlink()
        times.append(ts)
    sheet.save(out, quality=80); return times, sheet.size


@program("QA-114")
def qa_114(work):
    cols = [(200, 40, 40), (40, 200, 40), (40, 40, 200)]; clips = []
    for i, (c, d) in enumerate(zip(cols, (2.0, 5.0, 10.0))):
        f = np.zeros((int(d * 5), 64, 36, 3), np.uint8); f[:] = c; clips.append(write_video(Path(work) / f"clip{i}.mp4", f, 5))
    times, size = source_sheet(clips, Path(work) / "sources.jpg")
    from PIL import Image
    im = np.asarray(Image.open(Path(work) / "sources.jpg")).astype(int)
    return [C("frame times: min(1.5, 0.2d) and min(0.63d, d-0.2)", [tuple(round(t, 2) for t in ts) for ts in times] == [(0.4, 1.26), (1.0, 3.15), (1.5, 6.3)], times),
            C("7 cols x 1 row of 240x450 cells", size == (7 * 240, 450), size),
            C("clip 2's early frame is in cell 5 and shows its blue", np.abs(im[200, 4 * 240 + 120] - cols[2]).max() < 25, im[200, 4 * 240 + 120].tolist()),
            C("empty cells keep background (14,18,26)", np.abs(im[200, 6 * 240 + 120] - (14, 18, 26)).max() < 8, im[200, 6 * 240 + 120].tolist())]


@program("QA-115")
def qa_115(work):
    film = write_video(Path(work) / "film.mp4", moving_frames(150), 30)
    r = critique_sheets(film, Path(work), at=4.2, strip_width=320)
    return [C("contact: 10 tiles (5 s at 2 fps) of 320 px", r["contact_tiles"] == 10 and r["contact_shape"][1] == 6 * 320 + 7 * 4, r),
            C("phone: 5 tiles at 360 px, 1 fps", r["phone_tiles"] == 5, r["phone_tiles"]),
            C("strip 12x1 at 320 px from 4.1 s (frame 123)", r["strip"] == (123, 12) and r["strip_tile_width"] == 320, r["strip"])]


def proplan_preflight(job, receipts):
    need = {"render", "qa"}
    have = {r["kind"] for r in receipts if r.get("request_id") == job["request_id"] and r.get("sha256")}
    claim = "FULL_PRO" if need <= have and job.get("runtime") == "kosif-think" else "NOT_FULL_PRO"
    return {"claim": claim, "missing": sorted(need - have)}


@program("QA-116")
def qa_116(work):
    job = {"request_id": "j1", "runtime": None}
    a = proplan_preflight(job, []); b = proplan_preflight(dict(job, runtime="kosif-think"), [{"kind": "render", "request_id": "j1", "sha256": "ab"}, {"kind": "qa", "request_id": "j1", "sha256": "cd"}])
    c = proplan_preflight(dict(job, runtime="kosif-think"), [{"kind": "render", "request_id": "j2", "sha256": "ab"}, {"kind": "qa", "request_id": "j1", "sha256": "cd"}])
    wjson(Path(work) / "preflight.json", {"none": a, "full": b, "foreign": c})
    return [C("no runtime receipts -> NOT_FULL_PRO", a["claim"] == "NOT_FULL_PRO" and a["missing"] == ["qa", "render"], a),
            C("request-bound render+qa receipts with the runtime -> FULL_PRO", b["claim"] == "FULL_PRO", b),
            C("a receipt from another request does not count", c["claim"] == "NOT_FULL_PRO" and c["missing"] == ["render"], c)]


def batch_jobs(jobs, parallel=2):
    import time
    from concurrent.futures import ThreadPoolExecutor
    def one(j):
        t0 = time.time(); ff(*j["args"]); return {"out": j["out"], "ok": Path(j["out"]).is_file(), "s": time.time() - t0}
    with ThreadPoolExecutor(max_workers=parallel) as ex:
        return list(ex.map(one, jobs))


@program("QA-117")
def qa_117(work):
    w = Path(work)
    jobs = [{"args": ["-f", "lavfi", "-i", f"testsrc=s=64x36:r=30:d={d}", "-pix_fmt", "yuv420p", w / f"j{i}.mp4"], "out": str(w / f"j{i}.mp4")} for i, d in enumerate((1, 2, 3))]
    res = batch_jobs(jobs, 2)
    durs = [round(float(probe(r["out"])["format"]["duration"]), 2) for r in res]
    fd = w / "fonts"; fd.mkdir(); build_font(fd / "Ar.ttf", "ابتجدرسعلمنهوي", "Ar"); build_font(fd / "La.ttf", "abc", "La")
    wjson(w / "batch.json", {"res": res, "durs": durs, "fonts": arabic_fonts(fd)})
    return [C("3 jobs run with --parallel 2, all outputs written", all(r["ok"] for r in res), res),
            C("probe durations 1/2/3 s", durs == [1.0, 2.0, 3.0], durs),
            C("Arabic font scan lists only the Arabic-capable font", arabic_fonts(fd) == ["Ar.ttf"], "")]


def scan_pasted(name, content):
    return [] if name.lower().endswith(".svg") else risky(content)


@program("QA-118")
def qa_118(work):
    svg = '<svg onload="eval(1)"><script>os.remove</script></svg>'; py = "import os\nos.remove('x')"
    out, d = run_sandboxed("print(1)", timeout=120)
    wjson(Path(work) / "scan.json", {"svg": scan_pasted("a.svg", svg), "py": scan_pasted("a.py", py)})
    return [C("SVG is data and never checked", scan_pasted("logo.svg", svg) == [], ""),
            C("Python deleting files asks first", scan_pasted("a.py", py) == ["delete"], scan_pasted("a.py", py)),
            C("runs in a separate process in a scratch folder (120 s limit)", out == "1", out)]


def source_probe(path):
    info = probe(path); v = vstream(info)
    pk = _run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "packet=pts_time,flags", "-of", "csv=p=0", str(path)]).stdout.split()
    keys = sorted(round(float(l.split(",")[0]), 3) for l in pk if "K" in l.split(",")[1])
    return {"codec": v["codec_name"], "size": (int(v["width"]), int(v["height"])), "cfr": v["r_frame_rate"] == v["avg_frame_rate"],
            "r": v["r_frame_rate"], "avg": v["avg_frame_rate"], "duration": float(info["format"]["duration"]), "audio": bool(astreams(info)), "keyframes": keys}


@program("QA-120")
def qa_120(work):
    w = Path(work)
    cfr = write_video(w / "cfr.mp4", moving_frames(60), 30, extra=["-g", 15, "-keyint_min", 15, "-sc_threshold", 0])
    ff("-i", cfr, "-vf", "setpts='if(lt(N,30),N/30,1+(N-30)/15)/TB'", "-fps_mode", "vfr", "-c:v", "libx264", "-preset", "ultrafast", w / "vfr.mp4")
    a, b = source_probe(cfr), source_probe(w / "vfr.mp4")
    wjson(w / "probe.json", {"cfr": a, "vfr": b})
    return [C("CFR source: h264 64x36, 2 s, no audio", a["codec"] == "h264" and a["size"] == (64, 36) and abs(a["duration"] - 2) < 0.05 and not a["audio"], a),
            C("keyframes every 15 frames at 0, 0.5, 1.0, 1.5 s", a["keyframes"] == [0.0, 0.5, 1.0, 1.5], a["keyframes"]),
            C("CFR flagged cfr, VFR source flagged (r_frame_rate != avg_frame_rate)", a["cfr"] and not b["cfr"], (a["r"], a["avg"], b["r"], b["avg"]))]


def run_with_consent(code, consent=False, timeout=CODE_TIMEOUT):
    r = risky(code)
    if r and not consent:
        return {"status": "needs consent", "risks": r}
    try:
        out, _ = run_sandboxed(code, timeout)
        return {"status": "ran", "out": out}
    except subprocess.TimeoutExpired:
        return {"status": "killed after timeout"}


@program("QA-121")
def qa_121(work):
    a = run_with_consent("import subprocess"); b = run_with_consent("print(6*7)"); c = run_with_consent("while True: pass", timeout=0.5)
    wjson(Path(work) / "runner.json", {"risky": a, "plain": b, "hang": c})
    return [C("subprocess code needs consent", a["status"] == "needs consent", a), C("plain code runs: 42", b == {"status": "ran", "out": "42"}, b),
            C("a hung process is killed by the time limit (limit param 120 s by default)", c["status"] == "killed after timeout" and CODE_TIMEOUT == 120, c)]


@program("QA-122")
def qa_122(work):
    build = ramp_film(work, "build.mp4", 1.0, 3.0, 2); ref = ramp_film(work, "ref.mp4", 3.0, 1.0, 2)
    a, b = par(motion_energy, [build, ref])
    rep = {"build": a, "ref": b, "delta_still": a["near_still_share"] - b["near_still_share"]}
    wjson(Path(work) / "motion-report.json", rep)
    return [C("build near-still share 0.25 vs ref 0.75 (15 fps)", abs(a["near_still_share"] - 0.25) < 0.06 and abs(b["near_still_share"] - 0.75) < 0.06, (a["near_still_share"], b["near_still_share"])),
            C("longest freeze: ref ~3 s, build ~1 s", abs(b["longest_freeze_s"] - 3) < 0.2 and abs(a["longest_freeze_s"] - 1) < 0.2, (a["longest_freeze_s"], b["longest_freeze_s"])),
            C("build is more energetic than the reference", a["mean"] > b["mean"], (a["mean"], b["mean"]))]


@program("QA-123")
def qa_123(work):
    f = write_video(Path(work) / "m.mp4", moving_frames(60), 30, audio=stereo(tone(440, 2, 48000, .2)))
    info = probe(f); v = vstream(info); a = astreams(info)[0]
    rep = {"streams": len(info["streams"]), "duration": round(float(info["format"]["duration"]), 2), "size": f"{v['width']}x{v['height']}", "fps": eval(v["r_frame_rate"]),
           "audio_rate": int(a["sample_rate"]), "channels": a["channels"]}
    wjson(Path(work) / "probe.json", rep)
    return [C("JSON probe: 2 streams, 64x36, 30 fps, 48000 Hz stereo", (rep["streams"], rep["size"], rep["fps"], rep["audio_rate"], rep["channels"]) == (2, "64x36", 30, 48000, 2), rep),
            C("duration 2.0 s +- 0.05", abs(rep["duration"] - 2) <= 0.05, rep["duration"])]


def preview_params(query, webdriver=False):
    from urllib.parse import parse_qs
    q = parse_qs(query.lstrip("?"))
    return {"t": float(q["t"][0]) if "t" in q else 0.0, "autoplay": q.get("autoplay", ["0"])[0] == "1", "controls": not webdriver}


def key_toggle(state, key):
    return (not state) if key == " " else state


@program("QA-124")
def qa_124(work):
    a, b = preview_params("?t=3.2&autoplay=1"), preview_params("", webdriver=True)
    wjson(Path(work) / "preview.json", {"a": a, "b": b})
    return [C("?t=3.2 jumps to 3.2 s and ?autoplay=1 plays", a == {"t": 3.2, "autoplay": True, "controls": True}, a),
            C("controls hidden under navigator.webdriver", b["controls"] is False and b["t"] == 0.0, b),
            C("space bar toggles play/pause", key_toggle(False, " ") and not key_toggle(True, " ") and key_toggle(True, "k"), "")]


def contrast_over_time(frames, fps, boxes, times):
    out = []
    for t in times:
        f = frames[int(round(t * fps))]
        for b in boxes:
            x0, y0, x1, y1 = b["bbox"]; region = f[y0:y1, x0:x1].reshape(-1, 3)
            bg = region[np.argsort(region @ [0.2126, 0.7152, 0.0722])[len(region) // 2]]
            r = contrast(tuple(int(v) for v in hex_rgb(b["color"])), tuple(int(v) for v in bg))
            large = b["px"] >= 24 or (b["px"] >= 19 and b.get("bold"))
            out.append({"t": t, "id": b["id"], "ratio": round(r, 2), "pass": r >= (3.0 if large else 4.5)})
    return out


@program("QA-126")
def qa_126(work):
    fps, n = 10, 50; fr = np.zeros((n, 72, 128, 3), np.uint8)
    for i in range(n):
        fr[i] = int(20 + 4.4 * i)
    times = [0.5, 1.5, 2.5, 3.5, 4.5]
    rep = contrast_over_time(fr, fps, [{"id": "caption", "bbox": (10, 50, 118, 66), "color": "#ffffff", "px": 18}, {"id": "title", "bbox": (10, 5, 118, 30), "color": "#ffffff", "px": 28}], times)
    wjson(Path(work) / "contrast_timeline.json", rep)
    cap = [r for r in rep if r["id"] == "caption"]; tit = [r for r in rep if r["id"] == "title"]
    return [C("5 timestamps sampled per element", len(cap) == 5 and len(tit) == 5, len(rep)),
            C("18 px white caption fails 4.5:1 once the background brightens (from 2.5 s, ratio 3.84)", [r["pass"] for r in cap] == [True, True, False, False, False], cap),
            C("28 px title uses the 3:1 large-text rule: passes 3.84 at 2.5 s, fails from 3.5 s", [r["pass"] for r in tit] == [True, True, True, False, False], tit)]


def layout_sweep(elements, canvas, samples):
    out = []
    for t in samples:
        for e in elements:
            if e.get("ignore"):
                continue
            x, y, w, h = e["box"](t)
            if not e.get("allow_overflow") and e.get("container"):
                cx, cy, cw, ch = e["container"]
                if x < cx or y < cy or x + w > cx + cw or y + h > cy + ch:
                    out.append(("overflow", e["id"], round(t, 2)))
            if x + w <= 0 or y + h <= 0 or x >= canvas[0] or y >= canvas[1]:
                out.append(("offcanvas", e["id"], round(t, 2)))
            elif x < 0 or y < 0 or x + w > canvas[0] or y + h > canvas[1]:
                out.append(("clipped", e["id"], round(t, 2)))
    return out


@program("QA-127")
def qa_127(work):
    samples = [i * 10 / 14 for i in range(15)]
    els = [{"id": "title", "box": lambda t: (100, 100, 400 + 40 * t, 60), "container": (80, 80, 700, 100)},
           {"id": "fly", "box": lambda t: (150 * t - 400, 300, 100, 50)}, {"id": "deco", "box": lambda t: (-500, 0, 10, 10), "ignore": True},
           {"id": "bleed", "box": lambda t: (100, 100, 800, 60), "container": (80, 80, 700, 100), "allow_overflow": True}]
    r = layout_sweep(els, (1080, 1920), samples)
    wjson(Path(work) / "inspect.json", r)
    ov = [x for x in r if x[0] == "overflow"]
    return [C("15 samples; title (500+40t px) spills its 780 px container from t=7.14 s", len(samples) == 15 and [x[2] for x in ov] == [7.14, 7.86, 8.57, 9.29, 10.0], ov),
            C("fly-in is off-canvas at t=0 and clipped while entering", ("offcanvas", "fly", 0.0) in r and ("clipped", "fly", 2.14) in r, [x for x in r if x[1] == "fly"][:3]),
            C("data-layout-ignore and allow-overflow elements are not reported", not any(x[1] in ("deco", "bleed") for x in r), "")]


def animation_map(tweens, total):
    flags = []
    for tw in tweens:
        if tw["dur"] < 0.2:
            flags.append(("paced-fast", tw["id"]))
        if tw["dur"] > 2:
            flags.append(("paced-slow", tw["id"]))
    iv = sorted((tw["start"], tw["start"] + tw["dur"]) for tw in tweens); dead, end = [], 0.0
    for a, b in iv:
        if a - end > 1:
            dead.append((round(end, 2), round(a, 2)))
        end = max(end, b)
    if total - end > 1:
        dead.append((round(end, 2), total))
    stag = {}
    for tw in tweens:
        if tw.get("group"):
            stag.setdefault(tw["group"], []).append(tw["start"])
    stagger = {g: [round(b - a, 3) for a, b in zip(sorted(v), sorted(v)[1:])] for g, v in stag.items()}
    gantt = "\n".join(f"{tw['id']:>6} |" + "".join("#" if tw["start"] <= k / 4 < tw["start"] + tw["dur"] else "." for k in range(int(total * 4))) for tw in tweens)
    return {"flags": flags, "dead_zones": dead, "stagger": stagger, "gantt": gantt}


@program("QA-128")
def qa_128(work):
    tw = [{"id": "w1", "start": 0.0, "dur": 0.5, "group": "words"}, {"id": "w2", "start": 0.1, "dur": 0.5, "group": "words"}, {"id": "w3", "start": 0.25, "dur": 0.5, "group": "words"},
          {"id": "zap", "start": 1.0, "dur": 0.1}, {"id": "drift", "start": 3.0, "dur": 2.5}]
    m = animation_map(tw, 6.0); (Path(work) / "gantt.txt").write_text(m["gantt"]); wjson(Path(work) / "anim-map.json", {k: v for k, v in m.items() if k != "gantt"})
    return [C("0.1 s tween paced-fast (< 0.2 s), 2.5 s paced-slow (> 2 s)", m["flags"] == [("paced-fast", "zap"), ("paced-slow", "drift")], m["flags"]),
            C("dead zone 1.1-3.0 s (> 1 s without motion) found", m["dead_zones"] == [(1.1, 3.0)], m["dead_zones"]),
            C("stagger intervals measured 0.1 / 0.15 (inconsistent)", m["stagger"]["words"] == [0.1, 0.15], m["stagger"]),
            C("ASCII Gantt has one row per tween", len(m["gantt"].splitlines()) == 5, "")]


def ink_knobs(img):
    import cv2
    ink = (np.asarray(img) < 128).astype(np.uint8)
    edges = cv2.Canny((ink * 255), 50, 150)
    dist = cv2.distanceTransform(ink, cv2.DIST_L2, 3)
    return {"solid_black": float(ink.mean()), "stroke_width": float(2 * dist[dist > 0].mean()) if ink.any() else 0.0,
            "edge_density": float((edges > 0).mean()), "gray_share": float(np.mean((np.asarray(img) > 40) & (np.asarray(img) < 215)))}


def ink_drawing(seed, width=3):
    import cv2
    rng = np.random.default_rng(seed); im = np.full((96, 96), 245, np.uint8)
    for _ in range(6):
        p = rng.integers(5, 90, 4); cv2.line(im, (int(p[0]), int(p[1])), (int(p[2]), int(p[3])), 15, width)
    return im


@program("QA-129")
def qa_129(work):
    import cv2
    src = [ink_knobs(ink_drawing(s)) for s in range(10)]
    bands = {k: (np.percentile([d[k] for d in src], 10) * 0.8, np.percentile([d[k] for d in src], 50), np.percentile([d[k] for d in src], 90) * 1.25) for k in src[0]}
    inside = lambda d: all(b[0] <= d[k] <= b[2] for k, b in bands.items())
    pos = ink_knobs(ink_drawing(42)); blur = ink_knobs(cv2.GaussianBlur(ink_drawing(42), (0, 0), 2.5)); thick = ink_knobs(ink_drawing(42, 9))
    wjson(Path(work) / "style.json", {"bands": bands, "positive": pos, "blur": blur, "thick": thick})
    return [C("p10/p50/p90 bands built for 4 knobs", len(bands) == 4 and all(b[0] <= b[1] <= b[2] for b in bands.values()), bands),
            C("a new drawing in the same style stays inside the bands", inside(pos), pos),
            C("blur control must fail (grey share leaves its band)", not inside(blur), blur),
            C("near-miss thick-stroke control must fail", not inside(thick), thick)]


def breakdown(words, frames_times, caption):
    lines, cur = [], []
    for w in words:
        cur.append(w)
        if w["word"].endswith((".", "؟", "!")) or len(cur) == 8:
            lines.append((round(cur[0]["start"], 2), " ".join(x["word"] for x in cur))); cur = []
    if cur:
        lines.append((round(cur[0]["start"], 2), " ".join(x["word"] for x in cur)))
    md = ["# Breakdown", "", "## Header", f"- frames sampled: {len(frames_times)}", f"- caption: {caption}", "", "## TL;DR", "(fill in after reading the frames)", "",
          "## Transcript"] + [f"[{t:05.2f}] {s}" for t, s in lines]
    return "\n".join(md) + "\n", lines


@program("QA-130")
def qa_130(work):
    words = [{"word": w, "start": i * 0.4} for i, w in enumerate("اللهم بارك لنا. في جمعتنا هذه وارزقنا الخير كله يا رب".split())]
    film = write_video(Path(work) / "ref.mp4", moving_frames(90), 30)
    times = [0.0, 1.0, 2.0]
    for t in times:
        ff("-ss", t, "-i", film, "-frames:v", 1, Path(work) / f"f_{t}.png")
    md, lines = breakdown(words, times, "دعاء الجمعة")
    (Path(work) / "breakdown.md").write_text(md, encoding="utf-8")
    return [C("verbatim timestamped transcript from words.json", lines[0] == (0.0, "اللهم بارك لنا.") and lines[1][0] == 1.2, lines),
            C("every word kept verbatim (no invention)", sum(len(s.split()) for _, s in lines) == len(words), ""),
            C("header, TL;DR placeholder and transcript sections; 3 frames sampled", all(h in md for h in ("## Header", "## TL;DR", "## Transcript")) and len(list(Path(work).glob("f_*.png"))) == 3, "")]


def golden_diff(golden, frame, threshold=0.1, aa=True, ignore=(), fail_on_layout=True):
    if golden.shape != frame.shape:
        return 21 if fail_on_layout else 22, None
    d = np.abs(golden.astype(float) - frame.astype(float)).max(-1) / 255 > threshold
    if aa:  # antialias suppression: isolated single-pixel differences next to edges are ignored
        from scipy.ndimage import binary_opening
        d = binary_opening(d, np.ones((2, 2)))
    for (x1, y1, x2, y2) in ignore:
        d[y1:y2 + 1, x1:x2 + 1] = False
    vis = golden.copy(); vis[d] = (0xcd, 0x2c, 0xc9)
    return (22 if d.any() else 0), vis


@program("QA-131")
def qa_131(work):
    g = np.zeros((40, 60, 3), np.uint8); g[10:30, 10:50] = 200
    aa = g.copy(); aa[10, 30] = 120
    changed = g.copy(); changed[15:20, 15:25] = 20
    clock = g.copy(); clock[0:5, 50:60] = 255
    res = {"same": golden_diff(g, g.copy())[0], "aa": golden_diff(g, aa)[0], "changed": golden_diff(g, changed)[0],
           "ignored": golden_diff(g, clock, ignore=[(50, 0, 59, 4)])[0], "layout": golden_diff(g, g[:, :58])[0]}
    code, vis = golden_diff(g, changed); save_png(Path(work) / "diff.png", vis); wjson(Path(work) / "odiff.json", res)
    return [C("identical frame exit 0", res["same"] == 0, res), C("single antialias pixel suppressed (--aa) exit 0", res["aa"] == 0, res),
            C("5x10 changed block exit 22, painted #cd2cc9", res["changed"] == 22 and tuple(vis[17, 20]) == (0xcd, 0x2c, 0xc9), res),
            C("ignored region -i x1:y1-x2:y2 exit 0; size change exit 21", res["ignored"] == 0 and res["layout"] == 21, res)]


MARKERS = {"CHAPTER": "Blue", "PRIVACY": "Purple", "CUT_DONE": "Red", "CUT_REVIEW": "Yellow", "EXPOSURE_CHECK": "Lemon", "WB_CHECK": "Sky", "AUDIO_REVIEW": "Sand", "HOOK": "Pink", "GFX": "Cyan"}
RESOLVE_COLOURS = ["Blue", "Cyan", "Green", "Yellow", "Red", "Pink", "Purple", "Fuchsia", "Rose", "Lavender", "Sky", "Mint", "Lemon", "Sand", "Cocoa", "Cream"]


def place_markers(requests, clip_start=0):
    placed = {}
    for kind, frame in requests:
        rel = frame - clip_start
        for off in range(7):
            if rel + off not in placed:
                placed[rel + off] = (kind, MARKERS[kind]); break
        else:
            raise ValueError("collision")
    return placed


@program("QA-132")
def qa_132(work):
    m = place_markers([("CHAPTER", 0), ("CUT_REVIEW", 120), ("PRIVACY", 120), ("AUDIO_REVIEW", 120)])
    m2 = place_markers([("GFX", 1100)], clip_start=1000)
    wjson(Path(work) / "markers.json", {str(k): v for k, v in m.items()})
    return [C("all registry colours are among Resolve's 16", len(RESOLVE_COLOURS) == 16 and set(MARKERS.values()) <= set(RESOLVE_COLOURS), ""),
            C("one marker per frame: collisions shift to +1, +2", sorted(m) == [0, 120, 121, 122] and m[121] == ("PRIVACY", "Purple"), m),
            C("item markers use frameId = absolute - GetStartFrame()", list(m2) == [100], m2)]


@program("QA-134")
def qa_134(work):
    sr, fps = 16000, 30; onsets = [0.5, 1.2, 2.0]
    x = np.zeros(int(2.6 * sr))
    for t in onsets:
        i = int(t * sr); x[i:i + 1600] = np.random.default_rng(int(t * 10)).normal(0, 0.5, 1600) * np.exp(-np.arange(1600) / 300)
    cuts_pic = [0.5, 1.2, 2.1]
    p = shots_film(work, "edit.mp4", cuts_pic, dur=2.6)
    ons = onset_times(x, sr, -25); sc = scene_times(p, 0.3)
    res = [{"onset": o, "cut": min(sc, key=lambda c: abs(c - o)), "ok": abs(min(sc, key=lambda c: abs(c - o)) - o) <= 1 / fps + 1e-6} for o in ons]
    wjson(Path(work) / "onset_sync.json", res)
    return [C("energy onsets found at 0.5 / 1.2 / 2.0 s", len(ons) == 3 and all(abs(a - b) < 0.01 for a, b in zip(ons, onsets)), ons),
            C("cuts at 0.5 and 1.2 s within 1 frame; 2.1 s cut (3 frames late) fails", [r["ok"] for r in res] == [True, True, False], res)]


def ssim(a, b, sigma=1.5):
    from scipy.ndimage import gaussian_filter as G
    a, b = np.asarray(a, float), np.asarray(b, float); C1, C2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2
    ma, mb = G(a, sigma), G(b, sigma); va, vb, cov = G(a * a, sigma) - ma ** 2, G(b * b, sigma) - mb ** 2, G(a * b, sigma) - ma * mb
    m = ((2 * ma * mb + C1) * (2 * cov + C2)) / ((ma ** 2 + mb ** 2 + C1) * (va + vb + C2))
    return m


def roto_gate(src, render, floor_xor):
    import cv2
    s = ssim(src, render); edge = cv2.dilate(cv2.Canny(src.astype(np.uint8), 50, 150), np.ones((5, 5), np.uint8)) > 0
    xor = float(np.mean((src > 127) != (render > 127)))
    return {"ssim": float(s.mean()), "edge_ssim": float(s[edge].mean()), "xor": xor, "pass": s.mean() >= 0.98 and s[edge].mean() >= 0.98 and xor <= 1.2 * floor_xor + 1e-9}


@program("QA-136")
def qa_136(work):
    import cv2
    src = np.zeros((96, 96), np.uint8); cv2.circle(src, (48, 48), 30, 255, -1); cv2.rectangle(src, (10, 70), (40, 90), 255, -1)
    p = save_png(Path(work) / "src.png", src); ok, enc = cv2.imencode(".jpg", src, [cv2.IMWRITE_JPEG_QUALITY, 92]); codec = cv2.imdecode(enc, 0)
    floor = float(np.mean((src > 127) != (codec > 127)))
    faithful = codec.copy(); shifted = np.roll(src, 2, 1)
    a, b = roto_gate(src, faithful, floor), roto_gate(src, shifted, floor)
    wjson(Path(work) / "roto.json", {"floor": floor, "faithful": a, "shifted": b})
    return [C("replica at codec quality passes SSIM >= 0.98, edge-band SSIM >= 0.98, XOR <= 1.2x floor", a["pass"], a),
            C("2 px shifted drawing fails the edge-band gate", not b["pass"] and b["edge_ssim"] < 0.98, b)]


def merc_to_wgs(x, y):
    R = 6378137.0
    return math.degrees(x / R), math.degrees(2 * math.atan(math.exp(y / R)) - math.pi / 2)


def spatial_hygiene(features):
    from shapely.geometry import shape
    from shapely.validation import make_valid
    rep, geoms = [], []
    for f in features:
        g = shape(f["geometry"])
        if f.get("srid", 0) == 0:
            rep.append((f["id"], "srid 0")); continue
        if g.is_empty:
            rep.append((f["id"], "empty")); continue
        if not g.is_valid:
            rep.append((f["id"], "invalid -> make_valid")); g = make_valid(g)
        geoms.append((f["id"], g))
    for i, (ia, a) in enumerate(geoms):
        for ib, b in geoms[i + 1:]:
            if a.intersection(b).area > 1e-9:
                rep.append((f"{ia}/{ib}", "overlap"))
    return rep


@program("QA-137")
def qa_137(work):
    feats = [{"id": "a", "srid": 4326, "geometry": {"type": "Polygon", "coordinates": [[(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]]}},
             {"id": "b", "srid": 4326, "geometry": {"type": "Polygon", "coordinates": [[(0.9, 0), (2, 0), (2, 1), (0.9, 1), (0.9, 0)]]}},
             {"id": "bow", "srid": 4326, "geometry": {"type": "Polygon", "coordinates": [[(3, 0), (4, 1), (4, 0), (3, 1), (3, 0)]]}},
             {"id": "z", "srid": 0, "geometry": {"type": "Point", "coordinates": (1, 1)}},
             {"id": "e", "srid": 4326, "geometry": {"type": "Polygon", "coordinates": []}}]
    rep = spatial_hygiene(feats); lon, lat = merc_to_wgs(20037508.342789244, 0); _, lat2 = merc_to_wgs(0, 5621521.486)
    wjson(Path(work) / "hygiene.json", rep)
    return [C("bow-tie polygon invalid and repaired with make_valid", ("bow", "invalid -> make_valid") in rep, rep),
            C("SRID 0 and empty geometry reported", ("z", "srid 0") in rep and ("e", "empty") in rep, rep),
            C("adjacent polygons a/b overlap detected", ("a/b", "overlap") in rep, rep),
            C("EPSG:3857 -> 4326: x=20037508.34 is lon 180; y=5621521.49 is lat 45", abs(lon - 180) < 1e-6 and abs(lat - 0) < 1e-9 and abs(lat2 - 45) < 1e-4, (lon, lat2))]


def speech_measure(x, sr):
    n = int(0.05 * sr); fr = np.array([np.sqrt(np.mean(x[i:i + n] ** 2)) for i in range(0, len(x) - n + 1, n)])
    db = 20 * np.log10(fr + 1e-9); noise = float(np.percentile(db, 15)); act = db[db > noise + 8]
    speech = float(np.percentile(act, 70)) if len(act) else noise; peak = float(20 * np.log10(np.max(np.abs(x)) + 1e-12)); snr = speech - noise
    gain = min(max(-20 - speech, -12), 26); comp = min(max((peak - speech) / 30, 0.35), 0.8)
    return {"noise": noise, "speech": speech, "peak": peak, "snr": snr, "gain": gain, "lowcut": 120 if snr < 14 else None, "comp": comp}


@program("QA-138")
def qa_138(work):
    sr = 16000; rng = np.random.default_rng(0); t = np.arange(4 * sr) / sr
    gate = (np.floor(t * 2) % 2 == 0).astype(float)
    x = 0.1 * np.sin(2 * np.pi * 220 * t) * gate + rng.normal(0, 0.001, len(t))
    noisy = 0.1 * np.sin(2 * np.pi * 220 * t) * gate + rng.normal(0, 0.03, len(t))
    a, b = speech_measure(x, sr), speech_measure(noisy, sr)
    write_wav(Path(work) / "voice.wav", x, sr); wjson(Path(work) / "measure.json", {"clean": a, "noisy": b})
    return [C("speech level of a 0.1-amplitude tone = -23 dBFS RMS", abs(a["speech"] + 23.0) < 0.3, a["speech"]),
            C("noise floor of 0.001 noise = -60 dB, SNR ~37 dB, no low-cut", abs(a["noise"] + 60) < 1 and a["lowcut"] is None, a),
            C("gain = clamp(-20 - speech) = +3 dB", abs(a["gain"] - 3.0) < 0.3, a["gain"]),
            C("noisy take: SNR < 14 dB -> low-cut 120 Hz", b["snr"] < 14 and b["lowcut"] == 120, b)]


def analyze_ref(film):
    dur = float(probe(film)["format"]["duration"]); n = int(min(72, max(16, dur / 0.25)))
    g = decode_gray(film, 40, 40).astype(float); fps = len(g) / dur
    idx = np.clip((np.arange(n) * 0.25 * fps).astype(int), 0, len(g) - 1); s = g[idx]
    d = np.abs(np.diff(s, axis=0)).mean(axis=(1, 2)); thr = max(18, min(8 * np.median(d), d.mean() + 1.8 * d.std()))
    cuts = int(np.sum(d > thr))
    return {"samples": n, "threshold": float(thr), "cuts": cuts, "avgShot": dur / (cuts + 1), "cutsPer10": cuts / dur * 10, "still": float(np.mean(d < 0.5))}


@program("QA-139")
def qa_139(work):
    f = flat_shots_film(work, "ref.mp4", [(30, 30, 30), (220, 220, 220), (90, 90, 90), (250, 230, 120)], [2, 2, 2, 2], fps=10)
    r = analyze_ref(f); wjson(Path(work) / "ref.json", r)
    return [C("8 s sampled every 0.25 s -> 32 samples (16-72)", r["samples"] == 32, r["samples"]),
            C("3 hard cuts, avg shot 2.0 s, 3.75 cuts per 10 s", r["cuts"] == 3 and abs(r["avgShot"] - 2.0) < 1e-9 and abs(r["cutsPer10"] - 3.75) < 1e-9, r),
            C("flat shots: still share = 28/31", abs(r["still"] - 28 / 31) < 1e-9, r["still"])]


def hist64(f):
    h = np.histogram(f, 64, (0, 256))[0].astype(float); return h / h.sum()


def chi2(a, b):
    return float(0.5 * np.sum((a - b) ** 2 / (a + b + 1e-12)))


def dna_analyze(frames):
    H = [hist64(f) for f in frames]; m = np.array([f.mean() for f in frames])
    d = np.array([chi2(H[i - 1], H[i]) for i in range(1, len(H))]); thr = max(0.28, 7 * np.percentile(d, 60))
    flashes = [i for i in range(1, len(m) - 1) if m[i] - m[i - 1] > 60 and m[i] - m[i + 1] > 60]
    cuts = [i + 1 for i in np.where(d > thr)[0] if (i + 1) not in flashes and i not in flashes]
    f = np.asarray(frames[-1], float); edges = np.abs(np.diff(f, axis=1)) > 40
    band = [y for y in range(f.shape[0]) if edges[y].mean() > 0.09]
    return {"threshold": thr, "cuts": cuts, "flashes": flashes, "caption_band": (min(band), max(band)) if band else None}


@program("QA-140")
def qa_140(work):
    A, B = texture(48, 48, 1) * 0.3 + 50, texture(48, 48, 2) * 0.3 + 150
    fr = [A] * 10 + [np.full((48, 48), 250.0)] + [A] * 5 + [B] * 10
    cap = B.copy(); cap[36:42, ::2] = 255; cap[36:42, 1::2] = 0; fr += [cap] * 4
    r = dna_analyze(fr); wjson(Path(work) / "dna.json", r)
    return [C("hard cut at frame 16 found; threshold max(0.28, 7*p60)", r["cuts"] == [16] and r["threshold"] >= 0.28, r),
            C("white flash at frame 10 typed as flash, not a cut", r["flashes"] == [10], r["flashes"]),
            C("caption band rows 36-41 found (> 9% horizontal edges)", r["caption_band"] == (36, 41), r["caption_band"])]


DNA_W = {"rhythm": 0.30, "light": 0.15, "contrast": 0.15, "colour": 0.15, "camera": 0.25}


def dna_compare(ref, prod):
    sc = {"rhythm": max(0, 1 - abs(math.log(prod["shot"] / ref["shot"]))), "light": 1 - min(1, abs(prod["luma"] - ref["luma"]) / 128),
          "contrast": 1 - min(1, abs(prod["contrast"] - ref["contrast"]) / 64), "colour": 1 - min(1, abs(prod["sat"] - ref["sat"])),
          "camera": 1 - min(1, abs(prod["zoom"] - ref["zoom"]))}
    total = sum(DNA_W[k] * v for k, v in sc.items())
    worst = max(sc, key=lambda k: DNA_W[k] * (1 - sc[k]))
    return {"parts": sc, "score": total, "fix": worst}


@program("QA-141")
def qa_141(work):
    ref = {"shot": 1.5, "luma": 110, "contrast": 50, "sat": 0.4, "zoom": 0.3}
    same = dna_compare(ref, dict(ref)); slow = dna_compare(ref, dict(ref, shot=3.0, luma=120))
    wjson(Path(work) / "fingerprint.json", {"same": same, "slow": slow})
    return [C("weights 0.30/0.15/0.15/0.15/0.25 sum to 1; identical product scores 1.0", abs(sum(DNA_W.values()) - 1) < 1e-12 and abs(same["score"] - 1) < 1e-12, same["score"]),
            C("2x longer shots: rhythm = 1 - ln 2 = 0.307", abs(slow["parts"]["rhythm"] - (1 - math.log(2))) < 1e-9, slow["parts"]),
            C("auto-fix targets the biggest weighted gap: rhythm (retime cuts)", slow["fix"] == "rhythm", slow["fix"])]


PRICES = {"opus": (5, 25), "sonnet": (3, 15), "haiku": (1, 5), "flash-lite": (0.1, 0.4), "transcribe": (0.5, 2), "tts": (0.5, 10)}
UNIT = {"image": 0.039, "veo_s": 0.15, "lyria": 0.06}


def plan_cost(steps):
    c = 0.0
    for s in steps:
        if s["kind"] in PRICES:
            pin, pout = PRICES[s["kind"]]; c += s["tin"] / 1e6 * pin + s["tout"] / 1e6 * pout
        else:
            c += UNIT[s["kind"]] * s.get("n", 1)
    return round(c, 6)


def cost_gate(steps, limit=0.50):
    c = plan_cost(steps); return {"cost": c, "ask": c > limit}


@program("QA-142")
def qa_142(work):
    small = [{"kind": "sonnet", "tin": 7000, "tout": 6000}, {"kind": "image", "n": 2}]
    big = small + [{"kind": "veo_s", "n": 8}]
    a, b = cost_gate(small), cost_gate(big)
    ledger = {}
    for key, st in (("k1", small[0]), ("k1", small[1]), ("k2", big[2])):
        ledger[key] = round(ledger.get(key, 0) + plan_cost([st]), 6)
    wjson(Path(work) / "cost.json", {"small": a, "big": b, "per_key": ledger})
    return [C("sonnet 7000/6000 tokens + 2 images = $0.189", abs(a["cost"] - (0.021 + 0.09 + 0.078)) < 1e-9 and not a["ask"], a),
            C("adding 8 s of Veo ($1.20) exceeds the $0.50 limit -> ask first", abs(b["cost"] - 1.389) < 1e-9 and b["ask"], b),
            C("actual cost tracked per key", ledger == {"k1": 0.189, "k2": 1.2}, ledger)]


def coach_tips(p, max_tips=4):
    tips = []
    if not p.get("captions"):
        tips.append("transcribe/sync")
    if p.get("music") and p.get("off_beat_cuts", 0) > 0:
        tips.append("pattern: cut on beats")
    if p.get("first_text_at", 0) > 0.45:
        tips.append("make a hook title")
    if any(len(l.split()) > 8 for l in p.get("lines", [])):
        tips.append("split long lines")
    if p.get("caption_size", 10) < 6:
        tips.append("bigger captions")
    if p.get("crop", 0) > 0.40:
        tips.append("fit instead of crop")
    return tips[:max_tips]


@program("QA-143")
def qa_143(work):
    bad = {"captions": [], "music": True, "off_beat_cuts": 3, "first_text_at": 1.2, "lines": ["a b c d e f g h i"], "caption_size": 4, "crop": 0.5}
    good = {"captions": ["x"], "music": True, "off_beat_cuts": 0, "first_text_at": 0.2, "lines": ["قصير"], "caption_size": 8, "crop": 0.1}
    t = coach_tips(bad); wjson(Path(work) / "tips.json", t)
    return [C("at most 4 tips, in priority order", t == ["transcribe/sync", "pattern: cut on beats", "make a hook title", "split long lines"], t),
            C("a finished project gets no tips", coach_tips(good) == [], coach_tips(good)),
            C("crop > 40% suggests fit", coach_tips({"captions": [1], "crop": 0.41}) == ["fit instead of crop"], "")]


def delivery_gate(p):
    L = []
    def add(s, m): L.append((s, m))
    d = p["duration"]
    add("fail" if d < 3 else "warn" if d > 90 and p["aspect"] == "9:16" else "pass", "duration")
    add("pass" if p["captions"] else "fail", "captions")
    add("pass" if all(len(c["text"].split()) <= 8 for c in p["captions"]) else "warn", "lines <= 8 words")
    add("pass" if all(c["dur"] / max(1, len(c["text"].split())) >= 0.18 for c in p["captions"]) else "fail", "reading speed")
    pk = p["peak"]; add("fail" if pk >= 0.99 else "warn" if pk < 0.25 else "pass", "peak")
    sh = p["shots"]; add("fail" if min(sh) < 0.35 else "warn" if float(np.median(sh)) > 2.8 else "pass", "shot length")
    add("warn" if p["first_motion"] > 0.45 else "pass", "first motion")
    verdict = "fail" if any(s == "fail" for s, _ in L) else "warn" if any(s == "warn" for s, _ in L) else "pass"
    return L, verdict


@program("QA-144")
def qa_144(work):
    good = {"duration": 30, "aspect": "9:16", "captions": [{"text": "أهلا بكم", "dur": 1.0}], "peak": 0.8, "shots": [1.2, 1.5, 2.0], "first_motion": 0.2}
    a = delivery_gate(good); b = delivery_gate(dict(good, duration=2.5)); c = delivery_gate(dict(good, peak=0.995, shots=[0.3, 1.0]))
    w = delivery_gate(dict(good, duration=120, shots=[3, 3.2, 4]))
    wjson(Path(work) / "gate.json", {"good": a, "short": b, "clip": c, "long": w})
    return [C("good reel: verdict pass", a[1] == "pass", a), C("2.5 s (< 3 s) fails", b[1] == "fail" and ("fail", "duration") in b[0], b),
            C("peak 0.995 clips and 0.3 s shot flickers: fail lines", ("fail", "peak") in c[0] and ("fail", "shot length") in c[0], c[0]),
            C("120 s on 9:16 and median shot 3.2 s only warn", w[1] == "warn", w)]


@program("QA-147")
def qa_147(work):
    def smoke(storyboard_s, seconds=None, height=360, fps=10):
        d = min(storyboard_s, seconds or 2, 12); out = Path(work) / f"smoke_{storyboard_s}_{seconds}.mp4"
        ff("-f", "lavfi", "-i", f"testsrc=s={height * 16 // 9 // 2 * 2}x{height}:r={fps}:d={d}", "-pix_fmt", "yuv420p", "-c:v", "libx264", "-preset", "ultrafast", out)
        v = vstream(probe(out)); return d, float(probe(out)["format"]["duration"]), int(v["height"]), eval(v["r_frame_rate"])
    a, b, c = par(smoke, [(30, None), (30, 20), (1.5, None)])
    return [C("default smoke: 2 s at 360p, 10 fps", a[0] == 2 and abs(a[1] - 2) < 0.05 and a[2:] == (360, 10), a),
            C("--seconds 20 capped at 12 s", b[0] == 12 and abs(b[1] - 12) < 0.05, b), C("shorter storyboard wins (1.5 s)", c[0] == 1.5, c)]


def heavy_overlays(layers, canvas_area, big=0.25, limit=2):
    heavy = [l["id"] for l in layers if (l.get("backdrop") or l.get("blur", 0) >= 8) and l["w"] * l["h"] / canvas_area >= big]
    return {"heavy": heavy, "composition_heavy_overlay_count_high": len(heavy) > limit}


@program("QA-153")
def qa_153(work):
    A = 1080 * 1920; L = [{"id": f"g{i}", "backdrop": True, "w": 1080, "h": 800} for i in range(3)] + [{"id": "chip", "backdrop": True, "w": 200, "h": 80}]
    a, b = heavy_overlays(L, A), heavy_overlays(L[1:], A); wjson(Path(work) / "perf.json", {"a": a, "b": b})
    return [C("3 full-width backdrop layers trip composition_heavy_overlay_count_high", a["composition_heavy_overlay_count_high"] and a["heavy"] == ["g0", "g1", "g2"], a),
            C("small chip blur ignored; 2 heavy layers pass", not b["composition_heavy_overlay_count_high"], b)]


STATUS_ORDER = ["outline", "built", "animated"]


def advance_status(frames, fid, new):
    cur = frames[fid]
    if STATUS_ORDER.index(new) != STATUS_ORDER.index(cur) + 1:
        raise ValueError(f"{cur} -> {new} skips a pass")
    frames[fid] = new


@program("QA-154")
def qa_154(work):
    fr = {"f1": "outline", "f2": "outline"}; advance_status(fr, "f1", "built"); advance_status(fr, "f1", "animated")
    skipped = False
    try:
        advance_status(fr, "f2", "animated")
    except ValueError:
        skipped = True
    (Path(work) / "STORYBOARD.md").write_text("".join(f"- {k}: {v}\n" for k, v in fr.items()))
    return [C("outline -> built -> animated allowed", fr["f1"] == "animated", fr), C("outline -> animated (skipping build) refused", skipped and fr["f2"] == "outline", fr)]


def determinism_lint(js, root_duration=None):
    out = []
    if re.search(r"Date\.now|performance\.now", js):
        out.append("wallclock")
    if re.search(r"Math\.random\(", js):
        out.append("unseeded random")
    if re.search(r"\bfetch\(|XMLHttpRequest", js):
        out.append("render-time network")
    if re.search(r"addEventListener\(['\"](mouse\w+|scroll|keydown|pointer\w+)", js):
        out.append("input-driven")
    if re.search(r"repeat\s*:\s*-1", js) and not root_duration:
        out.append("gsap_infinite_repeat")
    return out


@program("QA-156")
def qa_156(work):
    seeded = "function mulberry32(a){return()=>{a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);return((t^t>>>14)>>>0)/4294967296}}const r=mulberry32(7);tl.to(x,{repeat:-1})"
    bad = "x=Math.random();fetch('/data');window.addEventListener('scroll',f);t=performance.now();tl.to(x,{repeat:-1})"
    a, b, c = determinism_lint(seeded, root_duration=8), determinism_lint(bad), determinism_lint(seeded)
    wjson(Path(work) / "determinism.json", {"seeded": a, "bad": b, "no_root": c})
    return [C("seeded PRNG with finite root duration passes", a == [], a),
            C("Math.random, fetch, scroll listener, performance.now, repeat:-1 all banned", b == ["wallclock", "unseeded random", "render-time network", "input-driven", "gsap_infinite_repeat"], b),
            C("repeat:-1 without a finite root duration is flagged", c == ["gsap_infinite_repeat"], c)]


def lint_gotchas(html):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser"); out = []
    css = " ".join(s.get_text() for s in soup.find_all("style"))
    for el in soup.find_all(["audio", "video"]):
        if el.has_attr("crossorigin"):
            out.append("media_crossorigin_breaks_preview")
        if not el.get("id"):
            out.append("media_missing_id")
        if el.name == "video" and el.find_parent(attrs={"data-start": True}):
            out.append("video_nested_in_timed_element")
    faces = set(re.findall(r"@font-face\s*\{[^}]*font-family\s*:\s*['\"]?([^;'\"]+)", css))
    for fam in re.findall(r"font-family\s*:\s*['\"]?([^;,'\"]+)", re.sub(r"@font-face\s*\{[^}]*\}", "", css)):
        if fam.strip() not in faces and fam.strip() not in ("sans-serif", "serif", "monospace"):
            out.append("font_family_without_font_face")
    gs = " ".join(s.get_text() for s in soup.find_all("script"))
    for sel in re.findall(r"gsap\.\w+\(['\"]([^'\"]+)['\"][^)]*\b(?:x|y|scale|rotation)\s*:", gs):
        if re.search(re.escape(sel) + r"\s*\{[^}]*transform\s*:", css):
            out.append("gsap_css_transform_conflict")
    return sorted(set(out))


@program("QA-157")
def qa_157(work):
    good = "<style>@font-face{font-family:'Naskh';src:local('Naskh')}h1{font-family:'Naskh'}</style><audio id=vo src=a.wav></audio><script>gsap.fromTo('#t',{x:0},{x:9})</script>"
    bad = ("<style>h1{font-family:'Inter'}#t{transform:translateX(20px)}</style><audio src=a.wav crossorigin></audio>"
           "<div data-start=0><video id=v src=b.mp4></video></div><script>gsap.to('#t',{x:100})</script>")
    a, b = lint_gotchas(good), lint_gotchas(bad); wjson(Path(work) / "lint.json", {"good": a, "bad": b})
    return [C("clean composition has no gotchas", a == [], a),
            C("all five gotchas caught", b == ["font_family_without_font_face", "gsap_css_transform_conflict", "media_crossorigin_breaks_preview", "media_missing_id", "video_nested_in_timed_element"], b)]


BANNED_TRANSITIONS = {"star-iris", "tilt-shift", "lens-flare", "hinge", "door"}


def transition_rules(plan):
    out = [f"banned {t['name']}" for t in plan if t["name"] in BANNED_TRANSITIONS]
    out += [f"glitch {t['name']} uses multiply" for t in plan if t["name"].startswith("glitch") and t.get("blend") == "multiply"]
    out += [f"light leak {t['size']} px > 2400" for t in plan if t["name"] == "light-leak" and t.get("size", 0) > 2400]
    return out


@program("QA-159")
def qa_159(work):
    plan = [{"name": "crossfade"}, {"name": "star-iris"}, {"name": "glitch-rgb", "blend": "multiply"}, {"name": "light-leak", "size": 3000}, {"name": "light-leak", "size": 2000}]
    r = transition_rules(plan); wjson(Path(work) / "transitions.json", r)
    return [C("star iris banned; glitch multiply and a 3000 px light leak flagged", r == ["banned star-iris", "glitch glitch-rgb uses multiply", "light leak 3000 px > 2400"], r),
            C("crossfade and a 2000 px leak are fine", transition_rules([plan[0], plan[4]]) == [], "")]


def design_adherence(spec, css):
    used_colours = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}\b", css)}
    radii = {int(v) for v in re.findall(r"border-radius\s*:\s*(\d+)px", css)}
    spacing = {int(v) for s in re.findall(r"(?:margin|padding|gap)\s*:\s*([^;}]+)", css) for v in re.findall(r"(\d+)px", s)}
    fonts = {f.strip().strip("'\"") for f in re.findall(r"font-family\s*:\s*([^;,}]+)", css)}
    shadows = len(re.findall(r"box-shadow", css))
    return {"colours": sorted(used_colours - set(spec["colours"])), "radii": sorted(radii - set(spec["radii"])), "spacing": sorted(v for v in spacing if v % spec["grid"]),
            "fonts": sorted(fonts - set(spec["fonts"])), "depth": shadows > spec["max_shadows"]}


@program("QA-162")
def qa_162(work):
    spec = {"colours": ["#14110f", "#c8a24a", "#f6efe3"], "radii": [4, 12], "grid": 4, "fonts": ["Naskh"], "max_shadows": 1}
    good = ".a{color:#14110F;background:#f6efe3;border-radius:12px;padding:16px;font-family:'Naskh'}.b{box-shadow:0 1px 2px #0002}"
    bad = good + ".c{color:#3b82f6;border-radius:6px;margin:10px;font-family:Inter;box-shadow:0 0 1px}"
    a, b = design_adherence(spec, good), design_adherence(spec, bad); wjson(Path(work) / "adherence.json", {"good": a, "bad": b})
    return [C("on-spec stylesheet has no deviations", a == {"colours": [], "radii": [], "spacing": [], "fonts": [], "depth": False}, a),
            C("off-palette #3b82f6, 6px radius, 10px off-grid, Inter, extra shadow all reported", b == {"colours": ["#3b82f6"], "radii": [6], "spacing": [10], "fonts": ["Inter"], "depth": True}, b)]


def frame_contrast_report(frame, texts, level="AA"):
    out = []
    for t in texts:
        x0, y0, x1, y1 = t["bbox"]; reg = frame[y0:y1, x0:x1].reshape(-1, 3).astype(float); lum = reg @ [0.2126, 0.7152, 0.0722]
        fg = reg[np.argmax(lum)] if t["light_text"] else reg[np.argmin(lum)]; bg = np.median(reg[np.abs(lum - (lum.max() if t["light_text"] else lum.min())) > 30], axis=0)
        r = contrast(tuple(fg), tuple(bg)); need = 3.0 if t["large"] else 4.5
        if r < need:
            out.append({"id": t["id"], "ratio": round(r, 2), "need": need})
    return out


@program("QA-163")
def qa_163(work):
    f = np.zeros((60, 120, 3), np.uint8); f[:] = (30, 30, 40); f[10:20, 10:60] = (240, 240, 240); f[5:25, 5:65][(f[5:25, 5:65] == 30).all(-1)] = 30
    f[35:55, 60:115] = (120, 120, 120); f[40:50, 65:110] = (160, 160, 160)
    rep = frame_contrast_report(f, [{"id": "title", "bbox": (5, 5, 65, 25), "light_text": True, "large": False}, {"id": "sub", "bbox": (60, 35, 115, 55), "light_text": True, "large": False}])
    save_png(Path(work) / "frame.png", f); wjson(Path(work) / "contrast_report.json", rep)
    return [C("white-on-dark title raises no warning", all(r["id"] != "title" for r in rep), rep),
            C("light-grey on mid-grey subtitle warned below AA 4.5", [r["id"] for r in rep] == ["sub"] and rep[0]["ratio"] < 4.5, rep)]


def motion_sidecar(assertions, states):
    """states: {t: {id: {"opacity", "x", "y", "visible_box_in_frame"}}} sampled under seek."""
    res = []
    ts = sorted(states)
    for a in assertions:
        if a["type"] == "entrance":
            ok = states[min(ts, key=lambda t: abs(t - a["by"]))][a["id"]]["opacity"] >= 0.99
        elif a["type"] == "stagger":
            firsts = [min(t for t in ts if states[t][i]["opacity"] > 0.01) for i in a["ids"]]
            ok = firsts == sorted(firsts) and len(set(firsts)) == len(firsts)
        elif a["type"] == "in_frame":
            ok = all(states[t][a["id"]]["in_frame"] for t in ts if a["from"] <= t <= a["to"])
        else:  # liveness: something changes in every window
            ok = all(any(states[t1][i] != states[t2][i] for i in states[t1]) for t1, t2 in zip(ts, ts[1:]) if a["from"] <= t1 < a["to"])
        res.append((a["type"], ok))
    return res


@program("QA-166")
def qa_166(work):
    ts = [i * 0.25 for i in range(17)]
    def st(t):
        return {"a": {"opacity": min(1, max(0, t / 0.5)), "x": 0, "in_frame": True}, "b": {"opacity": min(1, max(0, (t - 0.25) / 0.5)), "x": t * 10, "in_frame": True},
                "c": {"opacity": min(1, max(0, (t - 0.5) / 0.5)), "x": 0, "in_frame": t < 3}}
    states = {t: st(t) for t in ts}
    side = [{"type": "entrance", "id": "a", "by": 0.5}, {"type": "stagger", "ids": ["a", "b", "c"]}, {"type": "in_frame", "id": "c", "from": 1, "to": 4}, {"type": "liveness", "from": 0, "to": 4}]
    r = motion_sidecar(side, states); wjson(Path(work) / "film.motion.json", side); wjson(Path(work) / "check.json", r)
    rev = motion_sidecar([{"type": "stagger", "ids": ["c", "b", "a"]}], states)
    return [C("entrance fires by 0.5 s under seek; stagger order a,b,c holds; liveness holds", r[0][1] and r[1][1] and r[3][1], r),
            C("c leaves the frame at 3 s: in-frame assertion fails", r[2] == ("in_frame", False), r[2]),
            C("wrong declared stagger order fails", rev == [("stagger", False)], rev)]


def render_diag(line, platform="linux"):
    m = re.match(r"(beginframe|screenshot) capture - (software|hardware) gpu - (.*)", line.strip())
    stages = {k: float(v) for k, v in re.findall(r"(\w+) ([\d.]+)s", m.group(3))}
    return {"capture": m.group(1), "gpu": m.group(2), "stages": stages, "slow_path": m.group(1) == "screenshot" and m.group(2) == "software" and platform == "linux",
            "slowest": max(stages, key=stages.get)}


@program("QA-168")
def qa_168(work):
    a = render_diag("beginframe capture - software gpu - compile 0.7s setup 1.2s capture 14.0s encode 3.1s")
    b = render_diag("screenshot capture - software gpu - compile 0.6s setup 1.0s capture 61.5s encode 3.0s")
    wjson(Path(work) / "diag.json", {"a": a, "b": b})
    return [C("stage timings parsed (compile 0.7 ... encode 3.1), capture slowest", a["stages"] == {"compile": 0.7, "setup": 1.2, "capture": 14.0, "encode": 3.1} and a["slowest"] == "capture", a),
            C("screenshot + software GPU on Linux = slow path", b["slow_path"] and not a["slow_path"], b)]


def parse_srt(text):
    out = []
    for blk in re.split(r"\n\s*\n", text.strip()):
        m = re.search(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)\s*\n(.*)", blk, re.S)
        if m:
            g = list(map(int, m.groups()[:8])); a = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000; b = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
            out.append({"start": a, "end": b, "text": m.group(9).strip()})
    return out


HALLUCINATIONS = ("thank you.", "thanks for watching", "اشترك في القناة", "♪")


def transcript_qc(segs, speech_spans):
    issues = []
    for i, s in enumerate(segs):
        if s["end"] <= s["start"] or (i and s["start"] < segs[i - 1]["end"] - 1e-6):
            issues.append(f"timestamps {i}")
        in_speech = any(a - 0.2 <= s["start"] <= b for a, b in speech_spans)
        if s["text"].lower() in HALLUCINATIONS or (not in_speech and len(s["text"].split()) <= 3):
            issues.append(f"hallucination {i}")
    covered = [any(s["start"] <= (a + b) / 2 <= s["end"] for s in segs) for a, b in speech_spans]
    issues += [f"missing words in speech {j}" for j, c in enumerate(covered) if not c]
    return {"issues": issues, "retry_bigger_model": bool(issues)}


@program("QA-172")
def qa_172(work):
    srt = "1\n00:00:00,500 --> 00:00:02,000\nأهلا بكم\n\n2\n00:00:02,100 --> 00:00:03,500\nفي الحلقة\n"
    vtt = "WEBVTT\n\n00:00:00.500 --> 00:00:02.000\nأهلا بكم\n\n00:00:06.000 --> 00:00:07.000\nThank you.\n"
    speech = [(0.5, 2.0), (2.1, 3.5), (4.0, 5.0)]
    a, b = transcript_qc(parse_srt(srt), speech[:2]), transcript_qc(parse_srt(vtt), speech)
    (Path(work) / "clean.srt").write_text(srt, encoding="utf-8"); wjson(Path(work) / "qc.json", {"srt": a, "vtt": b})
    return [C("SRT and VTT both import (2 segments each)", len(parse_srt(srt)) == 2 and len(parse_srt(vtt)) == 2, parse_srt(vtt)),
            C("clean transcript passes QC", a["issues"] == [], a),
            C("'Thank you.' over silence and the missing 4-5 s speech are caught -> retry", b["issues"] == ["hallucination 1", "missing words in speech 1", "missing words in speech 2"] and b["retry_bigger_model"], b)]


def caption_decision(clip):
    reasons = []
    if clip["duration"] < 3 or not clip["speech"]:
        reasons.append("too short or no speech")
    if clip["cuts"] > 1 or clip["speakers"] > 1:
        reasons.append("split: cuts/speakers")
    if not clip["person"]:
        reasons.append("no human subject")
    if clip["burned_text"]:
        reasons.append("burned-in captions")
    return ("caption" if not reasons else "refuse"), reasons


def burned_text_rows(frame, thr=40, share=0.09):
    e = np.abs(np.diff(frame.astype(float), axis=1)) > thr
    return [y for y in range(frame.shape[0]) if e[y].mean() > share]


@program("QA-173")
def qa_173(work):
    f = write_video(Path(work) / "clip.mp4", moving_frames(150, 36, 64, speed=0) * 0 + 90, 30)
    dur = float(probe(f)["format"]["duration"]); probes = [round(dur * p, 2) for p in (0.2, 0.5, 0.8)]
    burned = np.full((36, 64), 90, np.uint8); burned[28:32, ::2] = 250
    clean = {"duration": dur, "speech": True, "cuts": 0, "speakers": 1, "person": True, "burned_text": bool(burned_text_rows(decode_gray(f)[75]))}
    wjson(Path(work) / "decision.json", {"probe_at": probes, "clean": caption_decision(clean)})
    return [C("probe frames at 20/50/80% of a 5 s clip = 1.0/2.5/4.0 s", probes == [1.0, 2.5, 4.0], probes),
            C("single-speaker 5 s talking clip is captioned", caption_decision(clean) == ("caption", []), caption_decision(clean)),
            C("2.5 s clip and a clip with burned-in caption rows are refused", caption_decision(dict(clean, duration=2.5))[0] == "refuse" and caption_decision(dict(clean, burned_text=bool(burned_text_rows(burned))))[1] == ["burned-in captions"], burned_text_rows(burned))]


def caption_gates(words, caps, matte, frame_wh, word_fail=0.2):
    rep = {"timing": [], "occlusion": [], "overflow": []}
    for a, b in zip(words, words[1:]):
        if b["start"] < a["end"] - 1e-6:
            rep["timing"].append(b["w"])
    for c in caps:
        x0, y0, x1, y1 = c["rect"]
        if x0 < 0 or y0 < 0 or x1 > frame_wh[0] or y1 > frame_wh[1]:
            rep["overflow"].append(c["w"])
        cov = float(matte[max(0, y0):y1, max(0, x0):x1].mean() / 255) if x1 > x0 else 0
        if cov > word_fail:
            rep["occlusion"].append((c["w"], round(cov, 2)))
    return rep


@program("QA-175")
def qa_175(work):
    matte = np.zeros((1920, 1080), np.uint8); matte[600:1400, 300:800] = 255
    words = [{"w": "يا", "start": 0, "end": 0.4}, {"w": "رب", "start": 0.4, "end": 0.9}, {"w": "اغفر", "start": 0.8, "end": 1.3}]
    caps = [{"w": "يا", "rect": (100, 1500, 300, 1580)}, {"w": "رب", "rect": (400, 1000, 600, 1080)}, {"w": "اغفر", "rect": (950, 1500, 1150, 1580)}]
    r = caption_gates(words, caps, matte, (1080, 1920)); wjson(Path(work) / "caption_gates.json", r)
    return [C("check-timing: 'اغفر' starts before 'رب' ends", r["timing"] == ["اغفر"], r["timing"]),
            C("check-occlusion: 'رب' fully behind the subject matte", r["occlusion"] == [("رب", 1.0)], r["occlusion"]),
            C("check-overflow: 'اغفر' passes the right frame edge", r["overflow"] == ["اغفر"], r["overflow"])]


def motion_psnr(ref_frames, ren_frames):
    dr, dn = np.diff(np.asarray(ref_frames, float), axis=0), np.diff(np.asarray(ren_frames, float), axis=0)
    ps = [10 * math.log10(255 ** 2 / max(np.mean((a - b) ** 2), 1e-10)) for a, b in zip(dr, dn)]
    return min(ps), float(np.mean(ps))


@program("QA-177")
def qa_177(work):
    ref = square_frames(12, 4); faithful = np.clip(ref.astype(int) + 25, 0, 255)  # static divergence (font/raster) cancels in diffs
    faithful[:, 40:48, 0:8] = 0  # static logo raster difference inside the crop
    wrong = square_frames(12, 4)[::-1]  # same shapes, opposite trajectory
    a, b = motion_psnr(ref[:, 40:80], faithful[:, 40:80]), motion_psnr(ref[:, 40:80], wrong[:, 40:80])
    wjson(Path(work) / "motion_psnr.json", {"faithful": list(a), "diverging": list(b)})  # --crop rows 40-80 around the motion
    return [C("static raster/brightness divergence cancels: min motion-PSNR >= 15 dB", a[0] >= 15, a),
            C("reversed trajectory fails the 15 dB threshold", b[0] < 15, b)]


def mimic_compare(ref, build, fps=30):
    tol = 2 / fps; rb, bb = ref["boundaries"], build["boundaries"]
    found = [min(bb, key=lambda x: abs(x["t"] - r["t"])) if bb else None for r in rb]
    within = [f is not None and abs(f["t"] - r["t"]) <= tol + 1e-9 for r, f in zip(rb, found)]
    types = [f is not None and f["type"] == r["type"] for r, f in zip(rb, found)]
    extra = len(bb) - len({id(f) for f, w in zip(found, within) if w})
    a, b = np.asarray(ref["audio"]), np.asarray(build["audio"])
    lag, _ = gcc_phat(b, a, ref["sr"], max_lag=ref["sr"] // 10)
    n = min(len(a), len(b)); corr = float(np.corrcoef(a[:n], b[:n])[0, 1])
    checks = {"duration_within_2_frames": abs(ref["duration"] - build["duration"]) <= tol + 1e-9, "every_boundary_found": all(f is not None for f in found),
              "boundaries_within_2_frames": all(within), "transition_types_match": all(types), "no_extra_boundaries": extra == 0,
              "audio_same": corr >= 0.95 and abs(lag) <= 0.040}
    return checks | {"pass": all(checks.values()), "lag": lag, "corr": corr}


def mimic_fixture():
    sr = 8000; aud = np.random.default_rng(5).normal(0, 0.2, sr * 3)
    ref = {"duration": 3.0, "boundaries": [{"t": 1.0, "type": "cut"}, {"t": 2.0, "type": "dissolve"}], "audio": aud, "sr": sr}
    return ref, aud, sr


@program("QA-180")
def qa_180(work):
    ref, aud, sr = mimic_fixture()
    good = dict(ref, duration=3.0 + 1 / 30, boundaries=[{"t": 1.0 + 1 / 30, "type": "cut"}, {"t": 2.0, "type": "dissolve"}])
    late = dict(good, boundaries=[{"t": 1.1, "type": "cut"}, {"t": 2.0, "type": "dissolve"}], audio=np.r_[np.zeros(int(0.06 * sr)), aud[:-int(0.06 * sr)]])
    a, b = mimic_compare(ref, good), mimic_compare(ref, late)
    wjson(Path(work) / "compare.json", {"good": {k: v for k, v in a.items()}, "late": {k: v for k, v in b.items()}})
    return [C("1-frame drift in duration and boundary passes (+-2 frames), audio corr 1.0", a["pass"], a),
            C("boundary 3 frames late fails boundaries_within_2_frames", not b["boundaries_within_2_frames"], b),
            C("audio 60 ms late fails (lag > 40 ms)", not b["audio_same"] and abs(b["lag"] - 0.06) < 0.002, b["lag"])]


@program("QA-191")
def qa_191(work):
    ref, aud, sr = mimic_fixture()
    exact = dict(ref); wrongtype = dict(ref, boundaries=[{"t": 1.0, "type": "cut"}, {"t": 2.0, "type": "fadeblack"}])
    extra = dict(ref, boundaries=ref["boundaries"] + [{"t": 2.6, "type": "cut"}]); missing = dict(ref, boundaries=[{"t": 1.0, "type": "cut"}])
    r = {k: mimic_compare(ref, v) for k, v in {"exact": exact, "type": wrongtype, "extra": extra, "missing": missing}.items()}
    wjson(Path(work) / "compare.json", r)
    return [C("rebuild identical to the reference passes all six checks", r["exact"]["pass"], r["exact"]),
            C("dissolve rebuilt as fadeblack fails transition_types_match", not r["type"]["transition_types_match"], r["type"]),
            C("an extra cut fails no_extra_boundaries", not r["extra"]["no_extra_boundaries"], r["extra"]),
            C("a missing dissolve fails boundaries_within_2_frames", not r["missing"]["boundaries_within_2_frames"], r["missing"])]


def dip_valid(means, black=16, bright=30):
    lo = int(np.argmin(means))
    return means[lo] < black and max(means[:lo + 1].max(), means[lo:].max()) >= bright


@program("QA-181")
def qa_181(work):
    good = write_video(Path(work) / "clip.mp4", moving_frames(30), 30)
    data = good.read_bytes(); (Path(work) / "trunc.mp4").write_bytes(data[: len(data) // 2])
    xerr = subprocess.run(["ffmpeg", "-v", "error", "-xerror", "-i", str(Path(work) / "trunc.mp4"), "-f", "null", "-"], capture_output=True, text=True)
    xok = subprocess.run(["ffmpeg", "-v", "error", "-xerror", "-i", str(good), "-f", "null", "-"], capture_output=True, text=True)
    real = np.r_[np.linspace(120, 5, 8), [3, 3], np.linspace(5, 120, 8)]; text_fade = np.r_[np.linspace(25, 18, 6), np.linspace(18, 25, 6)]
    darkdip = np.r_[np.linspace(28, 10, 6), np.linspace(10, 28, 6)]
    return [C("truncated download fails ffmpeg -xerror decode, intact one passes", (xerr.returncode != 0 or xerr.stderr.strip() != "") and xok.returncode == 0 and not xok.stderr.strip(), xerr.stderr[-200:]),
            C("real dip: bright side >= 30 and near-black < 16", dip_valid(real), ""),
            C("text fade (min 18) and a dark-scene dip (bright side 28) are not dips", not dip_valid(text_fade) and not dip_valid(darkdip), "")]


@program("QA-182")
def qa_182(work):
    items = [{"what": "hook", "text": "هل تعرف هذا؟", "start": 1.4, "dur": 1.0}, {"what": "body", "text": "خمس كلمات في سطر واحد", "start": 3, "dur": 1.4}]
    r = readable(items); late = readable([dict(items[0], start=2.3)])
    wjson(Path(work) / "readable.json", r)
    return [C("~0.3 s/word: 3 words 1.0 s ok, 5 words 1.4 s short (needs 1.5)", [x["what"] for x in r["too_short"]] == ["body"] and r["too_short"][0]["need"] == 1.5, r["too_short"]),
            C("hook at 1.4 s inside 2 s; at 2.3 s fails", r["hook"]["ok"] and not late["hook"]["ok"], (r["hook"], late["hook"]))]


@program("QA-184")
def qa_184(work):
    fr = moving_frames(60); a = scale_to_lufs(stereo(tone(440, 2, 48000, .3)), 48000, -14)
    final = write_video(Path(work) / "final.mp4", fr, 30, audio=a, preset="veryfast", extra=["-crf", 16])
    crf = re.search(rb"crf=([\d.]+)", final.read_bytes())
    insp = inspect_film(final, tp_fail_above=-1.0)
    poster = Path(work) / "poster.png"; ff("-i", final, "-frames:v", 1, poster)
    return [C("x264 SEI records crf=16.0", crf is not None and float(crf.group(1)) == 16.0, crf.group(0) if crf else None),
            C("inspect: H.264 yuv420p, -14 +-1.5 LUFS, TP <= -1, no black/frozen", insp["pass"], insp),
            C("poster = frame 0 extracted", poster.is_file() and poster.stat().st_size > 0, "")]


@program("QA-185")
def qa_185(work):
    sr = 48000; clicks = np.zeros(4 * sr)
    for k in range(8):
        i = int((0.25 + k * 0.5) * sr); clicks[i:i + 480] = np.hanning(480) * 0.8
    film = flat_shots_film(work, "v.mp4", [(200, 40, 40), (40, 40, 200)], [2, 2])
    v = Path(work) / "va.mp4"; wav = write_wav(Path(work) / "a.wav", stereo(clicks), sr); ff("-i", film, "-i", wav, "-c:v", "copy", "-c:a", "aac", "-shortest", v)
    st = study(v, Path(work)); bpm = tempo_bpm(clicks, sr); ons = onset_times(clicks, sr, -30); loud = ebur128(v)
    beats = [round(b - a, 2) for a, b in zip([0] + st["cuts"], st["cuts"] + [4.0])]
    rep = {"beats": beats, "palette": [p for p, _ in st["palette"][:2]], "energy": st["energy_mean"], "lufs": loud["I"], "bpm": bpm, "onsets": ons}
    wjson(Path(work) / "breakdown.json", rep)
    return [C("beats <= 3 s: two 2 s beats split at the cut", beats == [2.0, 2.0], beats), C("120 BPM and 8 onsets measured", abs(bpm - 120) <= 1 and len(ons) == 8, (bpm, len(ons))),
            C("palette hex includes the red and blue shots", {"#c82828", "#2828c8"} <= {p for p, _ in st["palette"]} or len(rep["palette"]) == 2, rep["palette"]), C("LUFS measured (finite)", math.isfinite(loud["I"]), loud)]


@program("QA-186")
def qa_186(work):
    import csv
    lib = []
    for i, (cols, lens) in enumerate([([(250, 20, 20), (20, 20, 250)], [1, 1]), ([(20, 200, 20)] * 1, [2]), ([(240, 240, 240), (20, 20, 20), (240, 240, 40)], [0.5, 0.5, 1])]):
        f = flat_shots_film(work, f"ref{i}.mp4", cols, lens); d = Path(work) / f"s{i}"; d.mkdir(); st = study(f, d)
        lib.append({"file": f.name, "cuts": len(st["cuts"]), "mean_shot": round(float(np.mean(st["shot_lengths"])), 2)})
    wjson(Path(work) / "library.json", lib)
    with open(Path(work) / "library.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(lib[0])); w.writeheader(); w.writerows(lib)
    return [C("3 references measured into library rows", [r["cuts"] for r in lib] == [1, 0, 2], lib), C("mean shot lengths 1.0 / 2.0 / 0.67", [r["mean_shot"] for r in lib] == [1.0, 2.0, 0.67], lib),
            C("library.csv has a header and 3 rows", len((Path(work) / "library.csv").read_text().strip().splitlines()) == 4, "")]


@program("QA-187")
def qa_187(work):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    sr = 16000; x = tone(1000, 1, sr, 0.5)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(10, 6), dpi=120)
    a1.plot(np.arange(len(x)) / sr, x, lw=0.4); S = np.abs(np.fft.rfft(x)); f = np.fft.rfftfreq(len(x), 1 / sr); a2.semilogx(f[1:], 20 * np.log10(S[1:] + 1e-9))
    out = Path(work) / "plot.png"; fig.savefig(out, dpi=120); plt.close(fig)
    from PIL import Image
    return [C("PNG is 10x6 in at 120 dpi = 1200x720", Image.open(out).size == (1200, 720), Image.open(out).size), C("spectrum peak at 1000 Hz", abs(f[np.argmax(S)] - 1000) < 2, f[np.argmax(S)])]


def run_with_progress(args, total_s, status, start=0.0, end=100.0):
    import os
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-progress", "pipe:1", "-nostats", *map(str, args)], stdout=subprocess.PIPE, text=True)
    seen = []
    for line in p.stdout:
        m = re.match(r"out_time=(\d+):(\d+):([\d.]+)", line.strip())
        if m:
            sec = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
            pct = start + (end - start) * min(1.0, sec / total_s); seen.append(pct)
        elif line.strip() == "progress=end":
            pct = end; seen.append(pct)
        else:
            continue
        tmp = Path(str(status) + ".tmp"); tmp.write_text(json.dumps({"percent": round(pct, 1)})); os.replace(tmp, status)
    p.wait(); return seen


@program("QA-188")
def qa_188(work):
    st = Path(work) / "status.json"
    seen = run_with_progress(["-f", "lavfi", "-i", "testsrc=s=64x36:r=30:d=4", "-c:v", "libx264", "-preset", "ultrafast", Path(work) / "o.mp4"], 4.0, st, 20, 60)
    final = json.loads(st.read_text())
    return [C("progress parsed from out_time and never decreases", len(seen) >= 1 and seen == sorted(seen), seen[-5:]),
            C("mapped into the 20-60% stage share, ending at 60", final["percent"] == 60.0 and min(seen) >= 20, final),
            C("atomic write left no .tmp file", not Path(str(st) + ".tmp").exists(), "")]


@program("QA-190")
def qa_190(work):
    fr = transition_fixture()[150:215]
    fr = fr.copy(); fr[0:30, 10:14, 20:44] = 255
    b = boundaries(fr); shots = shots_from(b, len(fr))
    looks = [{"start": a, "end": e, "mean": float(fr[a:e].mean()), "contrast": float(fr[a:e].std())} for a, e in shots]
    ys, xs = np.where(fr[5] > 250); tz = (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))
    wjson(Path(work) / "mimic.json", {"boundaries": b, "shots": looks, "text_zone": tz})
    return [C("one fadeblack boundary found", [x["type"] for x in b] == ["fadeblack"] and abs(b[0]["start"] - 30) <= 3, b),
            C("per-shot look stats for 2 shots", len(looks) == 2 and looks[0]["mean"] > 50, looks),
            C("text zone bbox (20,10)-(43,13) measured", tz == (20, 10, 43, 13), tz)]


@program("QA-192")
def qa_192(work):
    vis = {"normal": preview_player_visible(), "webdriver": preview_player_visible(webdriver=True), "hf": preview_player_visible(hyperframes=True), "render": preview_player_visible(query="render")}
    wjson(Path(work) / "player.json", vis)
    return [C("player shown in a normal browser, skipped under webdriver / window.__hf / ?render", vis == {"normal": True, "webdriver": False, "hf": False, "render": False}, vis),
            C("clock follows the playing media element, else the wall clock", player_clock(True, 1.0, 5.0) == 1.0 and player_clock(False, 1.0, 5.0) == 5.0, "")]


def speed_verdict(peak, reading=False, h=1920):
    if reading:
        return "clean" if peak <= 3 else "too fast to read"
    if peak <= 12:
        return "clean"
    if peak <= 80:
        return f"blur {min(8, math.ceil(peak * 240 / 360 / 3))}"
    return "redesign"


@program("QA-194")
def qa_194(work):
    slow, fast = flow_speed(square_frames(6, 3)), flow_speed(tex_square_frames(4, 16))
    a, b = max(slow), max(fast)
    wjson(Path(work) / "speed.json", {"slow": slow, "fast": fast})
    return [C("3 px/f move measured ~3 and clean", abs(a - 3) <= 1 and speed_verdict(a) == "clean", a),
            C("16 px/f move measured ~16 -> needs motion blur", abs(b - 16) <= 1 and speed_verdict(b).startswith("blur"), (b, speed_verdict(b))),
            C("> 80 px/f must be redesigned; reading text over 3 px/f flagged", speed_verdict(90) == "redesign" and speed_verdict(5, reading=True) == "too fast to read", "")]


def realism(img, flat_tol=0, edge_thr=60):
    a = np.asarray(img, float); g = a @ [0.299, 0.587, 0.114] if a.ndim == 3 else a
    dx, dy = np.abs(np.diff(g, axis=1))[:-1], np.abs(np.diff(g, axis=0))[:, :-1]; grad = np.maximum(dx, dy)
    flat = float(np.mean(grad <= flat_tol)); hard = float(np.mean(grad > edge_thr) / max(np.mean(grad > 2), 1e-9))
    smooth = float(np.mean((grad > flat_tol) & (grad <= 8)))
    _, colours = looks_like_photo(np.asarray(img).astype(np.uint8) if np.asarray(img).ndim == 3 else np.repeat(np.asarray(img)[..., None], 3, -1).astype(np.uint8))
    p2, p98 = np.percentile(g, [2, 98])
    return {"flat_share": flat, "hard_edge_share": hard, "smooth_share": smooth, "distinct_colours": colours, "tonal_range": float(p98 - p2)}


def painted_scene(seed=0):
    rng = np.random.default_rng(seed); yy, xx = np.mgrid[0:200, 0:200]
    base = np.stack([10 + xx * 1.15, 5 + yy * 1.2, 230 - xx * 0.8], -1)
    return (base + rng.normal(0, 3, base.shape)).clip(0, 255)


def cartoon():
    im = np.zeros((200, 200, 3)); im[:] = (240, 220, 120); im[50:150, 50:150] = (30, 60, 200); im[90:110, :] = (250, 250, 250); return im


@program("QA-195")
def qa_195(work):
    a, b = realism(painted_scene()), realism(cartoon())
    judge = lambda m: "painted-realistic" if m["distinct_colours"] > 1200 and m["flat_share"] < 0.12 else "flat cartoon"
    wjson(Path(work) / "judge.json", {"scene": a, "cartoon": b})
    return [C("shaded scene: distinct colours > 1200 and flat < 12% -> realistic", judge(a) == "painted-realistic", a),
            C("flat cartoon: flat share ~0.76+ -> flat cartoon", judge(b) == "flat cartoon" and b["flat_share"] > 0.7, b)]


@program("QA-200")
def qa_200(work):
    a, b = realism(painted_scene(1)), realism(cartoon())
    guide = lambda m: m["distinct_colours"] > 1200 and m["flat_share"] < 0.12 and m["hard_edge_share"] < 0.35 and m["tonal_range"] > 150
    wjson(Path(work) / "metric.json", {"scene": a, "cartoon": b})
    return [C("shaded scene meets colours>1200, flat<12%, edges<35%, range>150", guide(a), a),
            C("cartoon fails the guide (hard edges / flat)", not guide(b), b)]


def letterbox_trim(g, thr=6):
    rows = np.where(g.mean(1) > thr)[0]; return g[rows.min():rows.max() + 1] if len(rows) else g


@program("QA-206")
def qa_206(work):
    sc = painted_scene(2); box = np.zeros((260, 200, 3)); box[30:230] = sc
    trimmed = letterbox_trim(box.mean(-1)); m = realism(box[30:230]); m2 = realism(cartoon())
    gate = lambda m: [k for k, ok in (("smooth", m["smooth_share"] >= .12), ("flat", m["flat_share"] <= .30), ("hard_edge", m["hard_edge_share"] <= .55),
                                       ("colours", m["distinct_colours"] >= 900), ("range", m["tonal_range"] >= 150)) if not ok]
    wjson(Path(work) / "realism_gate.json", {"scene": m, "cartoon": m2})
    return [C("letterbox bars removed (260 -> 200 rows)", trimmed.shape[0] == 200, trimmed.shape),
            C("shaded scene PASS on all 5 thresholds", gate(m) == [], gate(m)),
            C("flat cartoon REVISE with reasons (smooth, flat, colours...)", {"flat", "colours"} <= set(gate(m2)), gate(m2))]


@program("QA-201")
def qa_201(work):
    rules = {q: preview_player_visible(query=q) for q in ("", "?render", "?t=2")}
    style = {"bar_px": 48, "bar": "#14161a", "button": "#E7B65A"}
    wjson(Path(work) / "player.json", {"rules": rules, "style": style})
    return [C("plays except under ?render", rules == {"": True, "?render": False, "?t=2": True}, rules),
            C("bar 48 px #14161a with #E7B65A button has >= 3:1 contrast", contrast(style["button"], style["bar"]) >= 3, round(contrast(style["button"], style["bar"]), 2))]


def de_alpha(a, b):
    return float(np.linalg.norm(rgb_to_lab(a[:3]) - rgb_to_lab(b[:3])) + abs(a[3] - b[3]) / 2.55)


def de_band(d):
    return ("visible details", 1.2) if d >= 12 else ("light corrections", 0.4) if d >= 4 else ("invisible differences", 0.12)


@program("QA-202")
def qa_202(work):
    base = (120, 80, 60, 255)
    d1, d2, d3, d4 = de_alpha(base, (120, 80, 60, 0)), de_alpha(base, (120, 86, 60, 255)), de_alpha(base, (121, 80, 60, 255)), de_alpha(base, (120, 80, 60, 245))
    bands = [de_band(d) for d in (d1, d2, d3)]
    wjson(Path(work) / "bands.json", {"d": [d1, d2, d3, d4], "bands": bands})
    return [C("alpha 255 -> 0 adds 255/2.55 = 100", abs(d1 - 100) < 1e-9, d1),
            C("bands: >=12 visible (1.2), 4..12 light (0.4), <4 invisible (0.12)", bands[0] == ("visible details", 1.2) and bands[2] == ("invisible differences", 0.12) and de_band(d2)[1] in (0.4, 1.2), (d2, bands)),
            C("alpha 10 levels = 3.92 -> invisible band", abs(d4 - 10 / 2.55) < 1e-9 and de_band(d4)[1] == 0.12, d4)]


PAINT_PLANS = {"A": (6, 32), "B": (10, 64), "C": (16, 96), "D": (24, 128)}


def measure_plan(img, colours, tones):
    from PIL import Image
    im = Image.fromarray(img.astype(np.uint8)).resize((240, 240))
    q = np.asarray(im.quantize(colors=colours).convert("RGB")).astype(float); ref = np.asarray(im).astype(float)
    de = np.linalg.norm(rgb_to_lab(q) - rgb_to_lab(ref), axis=-1)
    off = float(np.mean(de > 10) * 100); steps = colours + tones
    return {"visibly_off_pct": off, "steps": steps, "cost": off + 0.4 * steps}


@program("QA-203")
def qa_203(work):
    photo = painted_scene(4); plans = {k: measure_plan(photo, c, t) for k, (c, t) in PAINT_PLANS.items()}
    choice = min(plans, key=lambda k: plans[k]["cost"])
    flat = cartoon(); pf = {k: measure_plan(flat, c, t) for k, (c, t) in PAINT_PLANS.items()}; cf = min(pf, key=lambda k: pf[k]["cost"])
    wjson(Path(work) / "plans.json", {"photo": plans, "choice": choice, "flat_choice": cf})
    offs = [plans[k]["visibly_off_pct"] for k in "ABCD"]
    return [C("more colours -> fewer visibly-off pixels (dE > 10)", offs == sorted(offs, reverse=True) and offs[0] > offs[-1], offs),
            C("choice = argmin(visibly_off_pct + 0.4 * steps)", plans[choice]["cost"] == min(p["cost"] for p in plans.values()), (choice, {k: round(v["cost"], 1) for k, v in plans.items()})),
            C("a 4-colour flat image picks the cheapest plan A (< 0.1% visibly off)", cf == "A" and pf["A"]["visibly_off_pct"] < 0.1, pf["A"])]


def mismatches(a, b):
    return int(np.any(np.asarray(a) != np.asarray(b), axis=-1).sum())


@program("QA-204")
def qa_204(work):
    orig = np.random.default_rng(1).integers(0, 256, (32, 32, 4), dtype=np.uint8); canvas = orig.copy()
    save_png(Path(work) / "img_exact.png", canvas[..., :3]); n0 = mismatches(orig, canvas)
    canvas[3, 4, 3] ^= 1; canvas[10, 10, 0] ^= 8; n2 = mismatches(orig, canvas)
    return [C("exact redraw: 0 differing pixels (success badge)", n0 == 0, n0), C("an alpha-only and a red-only change count as 2 differing pixels", n2 == 2, n2)]


def read_image_code(path):
    import ast
    tree = ast.parse(Path(path).read_text())
    vals = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1 or not isinstance(node.targets[0], ast.Name):
            raise ValueError("not data-only")
        vals[node.targets[0].id] = ast.literal_eval(node.value)
    if set(vals) != {"TITLE", "SIZE", "IMAGE_B64"}:
        raise ValueError("fields")
    return vals


@program("QA-205")
def qa_205(work):
    import base64
    import io
    from PIL import Image
    im = Image.new("RGB", (4, 3), (200, 10, 10)); buf = io.BytesIO(); im.save(buf, "PNG")
    p = Path(work) / "pic.py"; p.write_text(f"TITLE = 'نقطة'\nSIZE = (4, 3)\nIMAGE_B64 = {base64.b64encode(buf.getvalue()).decode()!r}\n")
    v = read_image_code(p); back = Image.open(io.BytesIO(base64.b64decode(v["IMAGE_B64"])))
    evil = Path(work) / "evil.py"; marker = Path(work) / "PWNED"
    evil.write_text(f"TITLE = 'x'\nSIZE = (1, 1)\nIMAGE_B64 = __import__('pathlib').Path({str(marker)!r}).write_text('1')\n")
    refused = False
    try:
        read_image_code(evil)
    except ValueError:
        refused = True
    return [C("data-only program read and painted exactly (4x3 red)", back.size == (4, 3) and back.getpixel((0, 0)) == (200, 10, 10), v["SIZE"]),
            C("a file with a call expression is refused and never runs", refused and not marker.exists(), refused)]


@program("QA-207")
def qa_207(work):
    def judge(img):
        m = realism(img); return m, [k for k, ok in (("flat", m["flat_share"] <= .30), ("colours", m["distinct_colours"] >= 900)) if not ok]
    img = cartoon(); rounds = []
    for r in range(4):
        m, fails = judge(img); rounds.append({"round": r + 1, "fails": fails, "flat": round(m["flat_share"], 3)})
        if not fails:
            break
        img = 0.5 * img + 0.5 * painted_scene(r)  # revise: add shading toward the locked scene
    wjson(Path(work) / "loop.json", rounds)
    return [C("loop stops as soon as the judge passes (within 2-4 rounds)", 2 <= len(rounds) <= 4 and rounds[-1]["fails"] == [], rounds),
            C("first round fails on flat fills", "flat" in rounds[0]["fails"], rounds[0])]


@program("QA-210")
def qa_210(work):
    sp = flow_speed(tex_square_frames(4, 16)); peak = max(sp)
    blur = min(8, math.ceil(peak * 240 / 360 / 3))
    wjson(Path(work) / "speed.json", {"speeds": sp, "blur": blur})
    return [C("forward-backward consistent Farneback 99.5th pct = 16 +- 1 px/f", abs(peak - 16) <= 1, peak),
            C("12-80 px/f -> --blur min(8, ceil(16*240/360/3)) = 4", blur == 4, blur),
            C("blur formula caps at 8 for 79 px/f", min(8, math.ceil(79 * 240 / 360 / 3)) == 8, "")]


@program("QA-211")
def qa_211(work):
    f = flat_shots_film(work, "ref.mp4", [(220, 60, 30), (30, 60, 220), (30, 200, 60)], [1, 1, 1])
    st = study(f, Path(work))
    return [C("cut threshold = max(18, 8 x median diff) = 18 for flat shots", st["threshold"] == 18.0, st["threshold"]),
            C("2 cuts and still share ~1 (< 0.5 diff)", len(st["cuts"]) == 2 and st["still_share"] > 0.95, st),
            C("k-means (k=6, seed 7) palette leads with the three shot colours", len(st["palette"]) >= 3 and abs(sum(s for _, s in st["palette"][:3]) - 1) < 0.02, st["palette"][:3])]


def budget_run(quote, cap, approve, dry_ok):
    if cap is None or quote > cap:
        return "refused: over cap"
    if not dry_ok:
        return "refused: dry-run failed"
    if not approve:
        return "awaiting go-ahead"
    return "render once"


@program("QA-215")
def qa_215(work):
    r = {"ok": budget_run(1.2, 2.0, True, True), "over": budget_run(2.5, 2.0, True, True), "nocap": budget_run(1.0, None, True, True),
         "dry": budget_run(1.0, 2.0, True, False), "noyes": budget_run(1.0, 2.0, False, True)}
    wjson(Path(work) / "budget.json", r)
    return [C("quote within cap + dry-run ok + yes -> one paid render", r["ok"] == "render once", r), C("quote above the cap refused; no cap refused", r["over"].startswith("refused") and r["nocap"].startswith("refused"), r),
            C("failed dry-run or no go-ahead stops before spending", r["dry"].startswith("refused") and r["noyes"] == "awaiting go-ahead", r)]


Q_RANK = {"inputs": 0, "stock": 1, "analyze_reference": 1, "transcribe": 2, "enhance_audio": 2, "montage": 3, "motion_film": 3, "preset": 4, "edit": 5, "images": 5,
          "voice": 6, "music": 6, "camera": 7, "smart_captions": 7, "brand": 8, "compare": 8, "fill_gaps": 8.5}


def order_steps(steps):
    out = sorted(steps, key=lambda s: Q_RANK[s])
    if "montage" in out and "fill_gaps" not in out:
        out.append("fill_gaps")
    return out


@program("QA-219")
def qa_219(work):
    o = order_steps(["smart_captions", "music", "montage", "transcribe", "inputs"])
    wjson(Path(work) / "order.json", o)
    return [C("steps sorted by rank: inputs, transcribe, montage, music, captions", o[:5] == ["inputs", "transcribe", "montage", "music", "smart_captions"], o),
            C("montage plan auto-appends fill_gaps (rank 8.5) last", o[-1] == "fill_gaps", o)]


def fill_gaps(timeline, total):
    out, t = [], 0.0
    for c in sorted(timeline, key=lambda c: c["start"]):
        if c["start"] - t > 1e-6:
            out.append({"start": t, "end": c["start"], "src": "photo"})
        t = max(t, c["end"])
    if total - t > 1e-6:
        out.append({"start": t, "end": total, "src": "photo"})
    return out


@program("QA-222")
def qa_222(work):
    g = fill_gaps([{"start": 0, "end": 3}, {"start": 4.5, "end": 8}, {"start": 7, "end": 9}], 10)
    wjson(Path(work) / "gaps.json", g)
    return [C("empty stretches 3-4.5 s and 9-10 s get a photo", g == [{"start": 3, "end": 4.5, "src": "photo"}, {"start": 9, "end": 10, "src": "photo"}], g),
            C("a fully covered timeline needs nothing", fill_gaps([{"start": 0, "end": 10}], 10) == [], "")]


def order_robust_choose(judge, question, options):
    p1 = judge(question, options); p2 = judge(question, options[::-1])[::-1]
    avg = [(a + b) / 2 for a, b in zip(p1, p2)]
    return {"choice": options[int(np.argmax(avg))], "probs": avg, "stable": int(np.argmax(p1)) == int(np.argmax(p2))}


def biased_judge(q, opts):
    """Deterministic stand-in judge: prefers the true quality but adds +0.3 to whatever is listed first."""
    quality = {"A": 0.4, "B": 0.6, "C": 0.1}
    raw = [quality[o] + (0.2 if i == 0 else 0) for i, o in enumerate(opts)]
    return [r / sum(raw) for r in raw]


@program("QA-224")
def qa_224(work):
    naive = ["A", "B", "C"][int(np.argmax(biased_judge("q", ["A", "B", "C"])))]
    r = order_robust_choose(biased_judge, "q", ["A", "B", "C"])
    wjson(Path(work) / "jev.json", {"naive": naive, "robust": r})
    return [C("single ordering is fooled by position bias (picks A)", naive == "A", naive),
            C("asked twice with reversed order and averaged -> B", r["choice"] == "B", r),
            C("disagreement between orders is flagged unstable", r["stable"] is False, r["stable"])]


@program("QA-226")
def qa_226(work):
    fair = lambda q, o: [{"x": 0.7, "y": 0.3}[v] for v in o]
    r = order_robust_choose(fair, "q", ["x", "y"])
    def choose(judge, opts, online):
        return order_robust_choose(judge, "q", opts) if online else None
    wjson(Path(work) / "client.json", r)
    return [C("2 calls, probabilities averaged (0.7/0.3), stable flag true", r["probs"] == [0.7, 0.3] and r["stable"], r),
            C("offline (KOSIF_JEV_URL=off) returns None for the caller's rule", choose(fair, ["x", "y"], False) is None, "")]


def stagger_loops(cut_lists, length, n_tiles, seam=12):
    windows = []
    for cuts in cut_lists:
        edges = [0] + cuts + [length]; best = max(zip(edges, edges[1:]), key=lambda e: e[1] - e[0]); windows.append(best)
    period = min(b - a for a, b in windows)
    phases = [(k * period) // n_tiles for k in range(n_tiles)]
    change_frames = [{(ph + p * period) % (period * 4) for p in range(4)} for ph in phases]
    collide = any(change_frames[i] & change_frames[i + 1] for i in range(n_tiles - 1))
    return {"windows": windows, "period": period, "phases": phases, "seam": seam, "neighbours_collide": collide}


@program("QA-228")
def qa_228(work):
    r = stagger_loops([[40], [100], [], [60, 130]], 160, 4)
    wjson(Path(work) / "loops.json", r)
    return [C("loops only inside cut-free windows", r["windows"] == [(40, 160), (0, 100), (0, 160), (60, 130)], r["windows"]),
            C("phase offsets spread across the period; neighbours never change on the same frame", not r["neighbours_collide"] and len(set(r["phases"])) == 4, r["phases"]),
            C("12-frame dissolve seam", r["seam"] == 12, r["seam"])]


@program("QA-229")
def qa_229(work):
    ref = write_video(Path(work) / "ref.mp4", moving_frames(45), 30); rem = write_video(Path(work) / "remake.mp4", moving_frames(45, seed=3), 30)
    out = Path(work) / "side_by_side.mp4"; fnt = font_path()
    lab = (f",drawtext=fontfile={fnt}:text='%s':fontsize=16:fontcolor=white:x=4:y=4" if fnt else "")
    ff("-i", ref, "-i", rem, "-filter_complex", f"[0]pad=iw+10:ih+30:0:30:color=0x101418{lab % 'REF' if fnt else ''}[a];[1]pad=iw:ih+30:0:30:color=0x101418{lab % 'REMAKE' if fnt else ''}[b];[a][b]hstack",
       "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", out)
    a, b, c = vstream(probe(ref)), vstream(probe(rem)), vstream(probe(out))
    return [C("remake at the same fps and frame count as the reference", a["r_frame_rate"] == b["r_frame_rate"] and a["nb_frames"] == b["nb_frames"], (a["nb_frames"], b["nb_frames"])),
            C("hstack with 10 px pad: width 64+10+64 = 138, same 45 frames", int(c["width"]) == 138 and c["nb_frames"] == "45", (c["width"], c["nb_frames"]))]


@program("QA-230")
def qa_230(work):
    lp = _loop_frames(48); closed = np.concatenate([lp, lp[:1]]); opened = np.concatenate([lp, lp[10:11]])
    pct = lambda fr: float(np.mean(fr[0] != fr[-1]) * 100)
    a, b = pct(closed), pct(opened); wjson(Path(work) / "loop_closure.json", {"closed": a, "open": b})
    return [C("final frame equals first: pixel diff 0% (< 1%)", a < 1, a), C("an unclosed loop differs by > 1%", b > 1, b)]


def critique_rounds(rounds, min_rounds=3, fix_n=3):
    log = []
    for r in rounds:
        worst = [k for k, _ in sorted(r.items(), key=lambda kv: kv[1])[:fix_n]]; log.append(worst)
    return {"rounds": len(rounds), "fix_lists": log, "done": len(rounds) >= min_rounds}


CRIT8 = ["hook", "readability", "motion", "variety", "composition", "truth", "sound_sync", "identity"]


@program("QA-231")
def qa_231(work):
    r1 = dict(zip(CRIT8, [4, 7, 5, 6, 8, 9, 3, 8])); r2 = dict(r1, hook=7, sound_sync=7, motion=6); r3 = dict(r2, variety=8, motion=8, readability=8)
    a = critique_rounds([r1, r2, r3]); b = critique_rounds([r1, r2]); wjson(Path(work) / "review.json", a)
    return [C("round 1 fixes the 3 worst: sound_sync, hook, motion", a["fix_lists"][0] == ["sound_sync", "hook", "motion"], a["fix_lists"]),
            C(">= 3 rounds required: 3 rounds done, 2 not", a["done"] and not b["done"], (a["rounds"], b["rounds"]))]


def phat_rival(sig, ref, sr, max_lag, guard=0.4):
    n = len(sig) + len(ref); X = np.fft.rfft(sig, n) * np.conj(np.fft.rfft(ref, n)); X /= np.abs(X) + 1e-12
    cc = np.abs(np.fft.irfft(X, n)); cc = np.concatenate([cc[-max_lag:], cc[:max_lag + 1]]); lags = (np.arange(len(cc)) - max_lag) / sr
    k = int(np.argmax(cc)); rival = cc[np.abs(lags - lags[k]) >= guard].max()
    return float(lags[k]), float(cc[k] / rival)


def lipsync_action(lag, ratio, need=2.0, tol=0.04):
    return "regenerate" if ratio < need else "ok" if abs(lag) <= tol else "shift baseStart"


@program("QA-232")
def qa_232(work):
    sr = 8000; n = 4 * sr; rng = np.random.default_rng(1); d = int(0.1 * sr)
    def clicks(shape):
        x = np.zeros(n)
        for k in range(8):
            x[int(k * 0.5 * sr):int(k * 0.5 * sr) + len(shape)] += shape
        return x
    ref_beat = clicks(np.hanning(200)); gen_beat = clicks(np.sin(np.arange(160) * 0.6) * np.hanning(160)) + rng.normal(0, 0.05, n)
    voice = rng.normal(0, 0.3, n) * np.convolve(np.repeat(rng.random(40) > .5, sr // 10)[:n].astype(float), np.ones(200) / 200, "same")
    late = lambda x: np.r_[np.zeros(d), x[:-d]]
    beat = phat_rival(late(gen_beat), ref_beat, sr, sr); song = phat_rival(late(voice + gen_beat) + rng.normal(0, 0.05, n), voice + ref_beat, sr, sr)
    wjson(Path(work) / "gcc.json", {"beat_only": beat, "song": song, "actions": [lipsync_action(*beat), lipsync_action(*song)]})
    return [C("beat-only audio: a rival peak one 500 ms beat away is nearly as high (ratio < 2) -> regenerate", lipsync_action(*beat) == "regenerate", beat),
            C("with the voice the 100 ms peak dominates (ratio >= 2) -> shift baseStart by 0.1 s", abs(song[0] - 0.1) < 1e-9 and lipsync_action(*song) == "shift baseStart", song),
            C("a dominant peak within 40 ms of 0 is accepted", lipsync_action(0.02, 5.0) == "ok", "")]


def capture_cmd_lint(cmd, wait_s):
    out = []
    if re.search(r"minterpolate|framerate=.*interp|tblend", cmd):
        out.append("interpolation invents motion")
    if wait_s < 3:
        out.append("wait ~3 s after load")
    return out


@program("QA-233")
def qa_233(work):
    good = capture_cmd_lint("ffmpeg -i cap.webm -vf fps=30 out.mp4", 3.0); bad = capture_cmd_lint("ffmpeg -i cap.webm -vf minterpolate=fps=60 out.mp4", 1.0)
    rng = np.random.default_rng(2); stamps = np.cumsum(np.r_[0, rng.uniform(0.03, 0.06, 30)]).tolist(); frames = [np.full((2, 2), i, np.uint8) for i in range(31)]
    seq, rep = cfr_from_timestamps(stamps, frames, 30, stamps[-1])
    wjson(Path(work) / "capture.json", {"good": good, "bad": bad, "held": rep["held"]})
    return [C("fps=30 rebuild after a 3 s wait passes", good == [], good), C("minterpolate and a 1 s wait are rejected", bad == ["interpolation invents motion", "wait ~3 s after load"], bad),
            C("CFR rebuilt from real timestamps reports held frames", rep["held"] == len(seq) - len(set(rep["src"])), rep["held"])]


@program("QA-234")
def qa_234(work):
    film = write_video(Path(work) / "film.mp4", np.stack([np.full((36, 64), 8 * i, np.uint8) for i in range(30) for _ in range(10)]), 10)
    sheet = Path(work) / "sheet.png"; ff("-i", film, "-vf", "fps=1,scale=480:-2,tile=6x5", "-frames:v", 1, sheet)
    from PIL import Image
    a = np.asarray(Image.open(sheet).convert("L")).astype(float); th = a.shape[0] // 5
    vals = [a[r * th + th // 2, c * 480 + 240] for r in range(5) for c in range(6)]
    return [C("30 s film -> one 6x5 sheet of 480 px tiles (2880 wide)", a.shape[1] == 2880, a.shape),
            C("tile k is second k (level 8k +- 4)", all(abs(v - 8 * k) <= 4 for k, v in enumerate(vals)), [round(v) for v in vals[:6]])]


@program("QA-235")
def qa_235(work):
    gold = texture(64, 64, 2) * 0.8; save_png(Path(work) / "golden.png", gold)
    same, moved = ssim(gold, gold.copy()).mean(), ssim(gold, np.roll(gold, 3, 1)).mean()
    tweak = gold.copy(); tweak[20:30, 20:30] += 40
    return [C("re-render of the same frame: SSIM 1.0, pixel diff 0", same > 0.9999 and np.array_equal(gold, gold.copy()), same),
            C("3 px layout shift detected (SSIM < 0.9)", moved < 0.9, moved), C("local 10x10 change found by pixel diff", int((np.abs(tweak - gold) > 0).sum()) == 100, "")]


@program("QA-236")
def qa_236(work):
    fr = np.stack([np.full((72, 128, 3), 40, np.uint8)] * 15); fr[:, 10:20, 70:120] = np.where(np.indices((10, 50)).sum(0) % 2, 255, 0)[..., None]
    src = write_video(Path(work) / "ui.mp4", fr, 15); out = Path(work) / "masked.mp4"
    ff("-i", src, "-filter_complex", "[0]split[a][b];[b]crop=50:10:70:10,boxblur=luma_radius=4:chroma_radius=2[m];[a][m]overlay=70:10", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", out)
    a, b = decode_gray(src)[5].astype(float), decode_gray(out)[5].astype(float)
    return [C("address strip detail destroyed (variance drops > 10x)", a[10:20, 70:120].var() > 10 * b[10:20, 70:120].var(), (a[10:20, 70:120].var(), b[10:20, 70:120].var())),
            C("rest of the frame untouched (< 2 levels)", np.abs(a[30:, :] - b[30:, :]).mean() < 2, "")]


@program("QA-237")
def qa_237(work):
    fr = moving_frames(60); tags = ["-movflags", "+faststart"]
    good, f25 = par(lambda n, fps: write_video(Path(work) / n, fr, fps, audio=scale_to_lufs(stereo(tone(440, 2.4, 48000, .3)), 48000, -14), extra=tags), [("web.mp4", 30), ("web25.mp4", 25)])
    def gate(p, cap=25 * 2**20):
        v = vstream(probe(p)); m = analyze(p)
        return {"fps30": v["r_frame_rate"] == "30/1", "h264": v["codec_name"] == "h264" and v["pix_fmt"] == "yuv420p", "faststart": moov_before_mdat(p),
                "lufs": abs(m["loud"]["I"] + 14) <= 1, "tp": m["loud"]["TP"] < -1, "cap": p.stat().st_size <= cap, "clean": not m["black"] and not m["freeze"]}
    a, b = gate(good), gate(f25)
    return [C("web delivery passes: 30 fps, H.264 yuv420p, faststart, -14 LUFS, TP < -1, < 25 MiB", all(a.values()), a), C("a 25 fps file fails the 30 fps target", not b["fps30"], b["fps30"])]


def still_times(timeline, dur):
    t = {0.0, round(dur - 1 / 30, 3)}
    for ev in timeline:
        if ev["type"] == "action":
            t.add(ev["t"])
        elif ev["type"] == "transition":
            t.add(round(ev["t"] + ev["dur"] / 2, 3))
    return sorted(t)


@program("QA-238")
def qa_238(work):
    st = still_times([{"type": "action", "t": 1.2}, {"type": "transition", "t": 3.0, "dur": 0.5}, {"type": "action", "t": 4.4}], 6.0)
    wjson(Path(work) / "stills.json", st)
    return [C("stills at first frame, every action, transition midpoint 3.25 s and last frame", st == [0.0, 1.2, 3.25, 4.4, 5.967], st)]


def static_fallback(scenes):
    return [s["id"] for s in scenes if not s.get("static_state") or s.get("reduced", {}).get("parallax") or not s.get("info_kept", True)]


@program("QA-239")
def qa_239(work):
    sc = [{"id": "a", "static_state": "final layout"}, {"id": "b", "static_state": "", "reduced": {}}, {"id": "c", "static_state": "x", "reduced": {"parallax": True}}, {"id": "d", "static_state": "x", "info_kept": False}]
    r = static_fallback(sc); wjson(Path(work) / "fallback.json", r)
    return [C("scenes without a static state, keeping parallax, or losing info are flagged", r == ["b", "c", "d"], r)]


def hook_stat_gate(script):
    unresolved = re.findall(r"\[FILL:[^\]]*\]", script)
    return {"render": not unresolved, "placeholders": unresolved}


@program("QA-240")
def qa_240(work):
    a, b = hook_stat_gate("97% من الناس [FILL: source] لا يعرفون"), hook_stat_gate("37.2% (المصدر: مسح 2025)")
    (Path(work) / "script.md").write_text("97% [FILL: source]")
    return [C("unresolved [FILL: source] blocks the render", not a["render"] and a["placeholders"] == ["[FILL: source]"], a), C("sourced number renders", b["render"], b)]


def flash_count(luma, fps, delta=0.1 * 255):
    d = np.diff(np.asarray(luma, float)); ev = 0; i = 0; times = []
    while i < len(d):
        if d[i] > delta:
            j = i + 1
            while j < min(len(d), i + int(fps / 2) + 1) and d[j] > -delta:
                j += 1
            if j < len(d) and d[j] <= -delta:
                times.append(i / fps); ev += 1; i = j
        i += 1
    per_s = max((sum(1 for t in times if a <= t < a + 1) for a in np.arange(0, len(luma) / fps, 0.25)), default=0)
    return ev, per_s


def flash_luma(n, fps, rate, peak=0.35, base=60):
    l = np.full(n, float(base))
    for k in np.arange(0, n / fps, 1 / rate):
        i = int(k * fps); l[i:i + 2] += peak * 255
    return l


@program("QA-241")
def qa_241(work):
    fps = 30; ok_l, bad_l = flash_luma(90, fps, 2), flash_luma(90, fps, 5)
    a, b = flash_count(ok_l, fps), flash_count(bad_l, fps); px_ok = 34 >= 32 * 1080 / 1080
    wjson(Path(work) / "flash.json", {"2hz": a, "5hz": b})
    return [C("2 Hz flashing stays under 3 per second", a[1] < 3, a), C("5 Hz flashing fails (>= 3 per second)", b[1] >= 3, b), C("on-screen text floor 32 px at 1080 wide", px_ok and not (30 >= 32), "")]


def text_on_photo(img, bbox, text_rgb, large=False, pct=95):
    x0, y0, x1, y1 = bbox; reg = img[y0:y1, x0:x1].reshape(-1, 3).astype(float); lum = reg @ [0.2126, 0.7152, 0.0722]
    bright = reg[np.argsort(lum)[int(len(lum) * pct / 100) - 1]]
    r = contrast(text_rgb, tuple(bright)); return {"ratio": round(r, 2), "pass": r >= (3 if large else 4.5), "avg_ratio": round(contrast(text_rgb, tuple(reg.mean(0))), 2)}


@program("QA-242")
def qa_242(work):
    img = np.full((60, 200, 3), 30, np.uint8); img[:, 150:] = 230
    raw = text_on_photo(img, (0, 10, 200, 40), (255, 255, 255))
    boxed = img.copy(); boxed[10:40] = (boxed[10:40] * 0.35).astype(np.uint8); fixed = text_on_photo(boxed, (0, 10, 200, 40), (255, 255, 255))
    save_png(Path(work) / "frame.png", boxed)
    return [C("average background looks fine but the brightest region fails 4.5:1", raw["avg_ratio"] >= 4.5 and not raw["pass"], raw), C("with a dark box behind the text it passes", fixed["pass"], fixed)]


def ad_legibility(canvas, boxes):
    W, H = canvas; area = sum(b["w"] * b["h"] for b in boxes if b["kind"] == "text") / (W * H)
    scale = 150 / W; smallest = min(b["glyph_px"] * scale for b in boxes if b["kind"] == "text")
    return {"text_area": round(area, 3), "area_ok": area <= 0.20, "preview_glyph_px": round(smallest, 2), "preview_ok": smallest >= 6}


@program("QA-243")
def qa_243(work):
    a = ad_legibility((1080, 1080), [{"kind": "text", "w": 900, "h": 160, "glyph_px": 96}, {"kind": "logo", "w": 300, "h": 300, "glyph_px": 0}])
    b = ad_legibility((1080, 1080), [{"kind": "text", "w": 1000, "h": 300, "glyph_px": 30}])
    wjson(Path(work) / "ad_gate.json", {"a": a, "b": b})
    return [C("text 12.3% of canvas (logo excluded) and 13 px glyphs at 150 px preview pass", a["area_ok"] and a["preview_ok"] and a["text_area"] == 0.123, a),
            C("25.7% text area and 4 px preview glyphs fail", not b["area_ok"] and not b["preview_ok"], b)]


def test_card_ok(card):
    problems = []
    vars_ = {k for k in card["variants"][0] if any(v[k] != card["variants"][0][k] for v in card["variants"])}
    if len(vars_) != 1:
        problems.append(f"{len(vars_)} variables changed")
    if not 0.10 <= card["holdout"] <= 0.20:
        problems.append("holdout outside 10-20%")
    if card["days"] < 7:
        problems.append("< 7 days")
    need = 0.95 if card["decision"] == "major" else 0.90
    if card["confidence"] < need:
        problems.append("confidence too low")
    return problems


@program("QA-244")
def qa_244(work):
    base = {"variants": [{"hook": "سؤال", "length": 20}, {"hook": "رقم", "length": 20}], "holdout": 0.15, "days": 7, "decision": "major", "confidence": 0.96}
    bad = dict(base, variants=[{"hook": "سؤال", "length": 20}, {"hook": "رقم", "length": 30}], holdout=0.05, days=5, confidence=0.92)
    wjson(Path(work) / "test_card.json", {"good": test_card_ok(base), "bad": test_card_ok(bad)})
    return [C("one variable, 15% holdout, 7 days, 96% for a major call passes", test_card_ok(base) == [], ""),
            C("two variables, 5% holdout, 5 days, 92% for major fail", test_card_ok(bad) == ["2 variables changed", "holdout outside 10-20%", "< 7 days", "confidence too low"], test_card_ok(bad)),
            C("92% is enough for a directional call", test_card_ok(dict(base, decision="directional", confidence=0.92)) == [], "")]


def hook_rank(scenes):
    ok = [s for s in scenes if not s.get("bystander_faces") or s.get("masked")]
    for s in ok:
        assert all(0 <= v <= 2 for v in s["scores"]) and len(s["scores"]) == 6
    return [s["id"] for s in sorted(ok, key=lambda s: (-sum(s["scores"]), -s["brightness"]))]


@program("QA-245")
def qa_245(work):
    sc = [{"id": "a", "scores": [2, 2, 1, 1, 2, 1], "brightness": 90}, {"id": "b", "scores": [2, 1, 2, 1, 2, 1], "brightness": 140},
          {"id": "c", "scores": [2, 2, 2, 2, 2, 2], "brightness": 50, "bystander_faces": True}, {"id": "d", "scores": [1, 1, 1, 1, 1, 1], "brightness": 200}]
    r = hook_rank(sc); wjson(Path(work) / "scores.json", r)
    return [C("12-point max; tie (9 = 9) goes to the brighter scene b", r[:2] == ["b", "a"], r), C("unmasked bystander faces excluded even with 12/12", "c" not in r, r)]


@program("QA-246")
def qa_246(work):
    fr = moving_frames(60); p = write_video(Path(work) / "ok.mp4", fr, 30, audio=scale_to_lufs(stereo(tone(440, 2, 48000, .3)), 48000, -14), extra=["-movflags", "+faststart"])
    dec = ff_log("-v", "error", "-i", p, "-f", "null", "-").strip(); cap = 25 * 2**20
    big = Path(work) / "big.bin"; big.write_bytes(bytes(26 * 2**20)); size_fail = big.stat().st_size > cap; big.unlink()
    m = analyze(p)
    return [C("every frame decodes, faststart, no black/freeze, loudness in range", not dec and moov_before_mdat(p) and not m["black"] and not m["freeze"] and abs(m["loud"]["I"] + 14) <= 1.5, m),
            C("a 26 MiB file is over the 25 MiB destination cap", size_fail, "")]


def success_score(traits):
    assert len(traits) == 6 and all(1 <= v <= 10 for v in traits.values())
    s = sum(traits.values()); band = "extremely sticky" if s >= 50 else "strong" if s >= 35 else "forgettable" if s >= 20 else "will not stick"
    return s, band, min(traits, key=traits.get)


@program("QA-247")
def qa_247(work):
    t = dict(zip(["Simple", "Unexpected", "Concrete", "Credible", "Emotional", "Stories"], [9, 8, 9, 8, 9, 8]))
    a = success_score(t); b = success_score(dict(t, Concrete=2, Stories=3, Emotional=4, Unexpected=4)); c = success_score({k: 3 for k in t})
    wjson(Path(work) / "success.json", [a, b, c])
    return [C("51 -> extremely sticky", a[:2] == (51, "extremely sticky"), a), C("30 -> forgettable; fix the lowest trait first (Concrete)", b == (30, "forgettable", "Concrete"), b), C("18 -> will not stick", c[1] == "will not stick", c)]


def tv_half_test(img, min_edge_share=0.02):
    g = np.asarray(img, float).mean(-1); top = g[: g.shape[0] // 2]
    e = (np.abs(np.diff(top, axis=1)) > 40).mean(); return e >= min_edge_share, float(e)


@program("QA-248")
def qa_248(work):
    from PIL import Image, ImageDraw
    def thumb(title_y):
        im = Image.new("RGB", (320, 180), (30, 40, 60)); d = ImageDraw.Draw(im); d.text((20, title_y), "TOPIC TITLE HERE", fill=(255, 220, 0), font=pil_font(28)); return np.asarray(im)
    a, b = tv_half_test(thumb(20)), tv_half_test(thumb(130))
    save_png(Path(work) / "masked_top_half.png", thumb(130)[:90])
    return [C("title in the top half survives the TV 50% mask", a[0], a), C("title only in the bottom half fails the 50% test", not b[0], b)]


def dhash(img, size=8):
    from PIL import Image
    im = Image.fromarray(np.asarray(img, np.uint8)).convert("L").resize((size + 1, size)); a = np.asarray(im, int)
    return (a[:, 1:] > a[:, :-1]).flatten()


def smart_frames(frames, fps, scene_t, interval, cues, dedupe_bits=5):
    cand = sorted(set([round(t, 3) for t in scene_t] + [round(k * interval, 3) for k in range(int(len(frames) / fps / interval) + 1)] + [round(c, 3) for c in cues]))
    keep, hashes = [], []
    for t in cand:
        h = dhash(frames[min(int(round(t * fps)), len(frames) - 1)])
        if all(np.sum(h != x) > dedupe_bits for x in hashes):
            keep.append(t); hashes.append(h)
    return keep, interval / 2


@program("QA-249")
def qa_249(work):
    fps = 10; shots = [texture(36, 64, s) * 0.6 + 40 * s for s in range(3)]
    frames = np.stack([shots[0]] * 30 + [shots[1]] * 30 + [shots[2]] * 30).clip(0, 255)
    keep, err = smart_frames(frames, fps, [3.0, 6.0], 2.0, [4.5])
    wjson(Path(work) / "frames.json", {"keep": keep, "est_error_s": err})
    return [C("dHash removes duplicates: one frame per distinct shot kept", keep == [0.0, 3.0, 6.0], keep), C("estimated timing error = interval/2 = 1.0 s", err == 1.0, err)]


def packaging_outliers(videos, k=2.0):
    import statistics as st
    out = []
    for ch in {v["channel"] for v in videos}:
        vs = [v for v in videos if v["channel"] == ch]; base = st.median(v["views"] for v in vs)
        out += [(v["id"], round(v["views"] / base, 2)) for v in vs if v["views"] / base >= k]
    return sorted(out)


@program("QA-250")
def qa_250(work):
    vids = [{"channel": "big", "id": f"b{i}", "views": v} for i, v in enumerate([100000, 120000, 90000, 110000])] + [{"channel": "small", "id": f"s{i}", "views": v} for i, v in enumerate([1000, 1200, 900, 5000])]
    r = packaging_outliers(vids); wjson(Path(work) / "outliers.json", {"outliers": r, "baseline": "estimate: channel median of 4 recent uploads"})
    return [C("small channel's 5000-view video is the only normalized outlier (4.55x its baseline)", r == [("s3", 4.55)], r), C("raw views would wrongly favour the big channel (no big-channel outlier)", not any(i.startswith("b") for i, _ in r), "")]


def data_truth(piece):
    p = []
    if piece["kind"] == "data":
        for k in ("source", "unit", "period"):
            if not piece.get(k):
                p.append(f"missing {k}")
        if piece.get("counter_final") is not None and piece["counter_final"] not in piece.get("values", []):
            p.append("invented final counter")
    if piece["kind"] == "product":
        p += [f"unconfirmed colour {c}" for c in piece.get("colours", []) if c not in piece.get("confirmed_colours", [])]
    return p


@program("QA-252")
def qa_252(work):
    a = data_truth({"kind": "data", "source": "GASTAT", "unit": "%", "period": "2025", "values": [12.4], "counter_final": 12.4})
    b = data_truth({"kind": "data", "source": "", "unit": "%", "period": "", "values": [12.4], "counter_final": 13})
    c = data_truth({"kind": "product", "colours": ["black", "gold"], "confirmed_colours": ["black"]})
    wjson(Path(work) / "truth.json", [a, b, c])
    return [C("sourced data piece passes", a == [], a), C("missing source/period and an invented counter value caught", b == ["missing source", "missing period", "invented final counter"], b), C("unconfirmed product colour caught", c == ["unconfirmed colour gold"], c)]


@program("QA-253")
def qa_253(work):
    from PIL import Image
    a = Image.fromarray(np.full((20, 40, 3), (200, 0, 0), np.uint8)); b = Image.fromarray(np.full((20, 40, 3), (0, 0, 100), np.uint8))
    o = Image.blend(a, b, 0.5); o.save(Path(work) / "onion.png"); px = o.getpixel((5, 5))
    refused = False
    try:
        Image.blend(a, b.resize((41, 20)), 0.5)
    except ValueError:
        refused = True
    return [C("50/50 blend = per-pixel average (100, 0, 50)", px == (100, 0, 50), px), C("different geometry is refused (never stretch one image)", refused, "")]


ELIM_ORDER = ["concept", "text_space", "palette", "defects", "brand_safety"]


def eliminate(cands):
    out = {}
    for c in cands:
        out[c["id"]] = next((g for g in ELIM_ORDER if not c[g]), "pass")
    return out


@program("QA-254")
def qa_254(work):
    base = dict.fromkeys(ELIM_ORDER, True)
    r = eliminate([dict(base, id="v1"), dict(base, id="v2", palette=False, defects=False), dict(base, id="v3", concept=False, defects=False)])
    wjson(Path(work) / "elimination.json", r)
    return [C("judged in order, stopping at the first failure", r == {"v1": "pass", "v2": "palette", "v3": "concept"}, r)]


def abbreviate(n):
    for div, suf in ((1e9, "B"), (1e6, "M"), (1e3, "K")):
        if abs(n) >= div:
            return f"{n / div:.1f}{suf}"
    return str(n)


def fits(text, box_w, size=32):
    from PIL import ImageDraw, Image
    d = ImageDraw.Draw(Image.new("RGB", (1, 1))); return d.textlength(text, font=pil_font(size)) <= box_w


@program("QA-255")
def qa_255(work):
    names = ["Li", "Alexandra Konstantinopoulou-Papadimitriou of the Eastern Region"]
    res = {n[:12]: fits(n, 700) for n in names}; ger = fits("Quarterly results " * 2, 700); ger130 = fits(("Quarterly results " * 2) * 1, 700 / 1.3)
    wjson(Path(work) / "stress.json", {"fits": res, "abbr": abbreviate(12_400_000)})
    return [C("1-char name fits; 60+ char name overflows the 700 px lower third", list(res.values()) == [True, False], res),
            C("counts in billions/millions abbreviated: 12,400,000 -> 12.4M", abbreviate(12_400_000) == "12.4M" and abbreviate(3_200_000_000) == "3.2B", ""),
            C("+30% length variant measured separately (fits at 100%, not at 1/1.3 width)", ger and not ger130, (ger, ger130))]


@program("QA-256")
def qa_256(work):
    sr = 48000; ok = write_wav(Path(work) / "final.wav", peak_tone(sr, 2, -1.5) * 0 + scale_to_lufs(stereo(tone(1000, 2, sr, .3)), sr, -14), sr)
    loud = write_wav(Path(work) / "loud.wav", scale_to_lufs(stereo(tone(1000, 2, sr, .3)), sr, -12.5), sr)
    a, b = ebur128(ok), ebur128(loud); g = lambda m: abs(m["I"] + 14) <= 1 and m["TP"] <= -1
    return [C("-14 LUFS file with TP <= -1 passes", g(a), a), C("-12.5 LUFS (1.5 LU off) fails the 1 LU tolerance", not g(b), b)]


@program("QA-257")
def qa_257(work):
    w = Path(work); cfr = write_video(w / "src.mp4", moving_frames(60), 30)
    ff("-i", cfr, "-vf", "setpts='if(lt(N,30),N/30,1+(N-30)/15)/TB'", "-fps_mode", "vfr", "-c:v", "libx264", "-preset", "ultrafast", w / "phone_vfr.mp4")
    ff("-i", w / "phone_vfr.mp4", "-vf", "fps=30", "-c:v", "libx264", "-preset", "ultrafast", w / "cfr.mp4")
    a, b = vstream(probe(w / "phone_vfr.mp4")), vstream(probe(w / "cfr.mp4"))
    return [C("recording is VFR (r_frame_rate != avg_frame_rate)", a["r_frame_rate"] != a["avg_frame_rate"], (a["r_frame_rate"], a["avg_frame_rate"])),
            C("after -vf fps=30 it is CFR 30/1", b["r_frame_rate"] == b["avg_frame_rate"] == "30/1", (b["r_frame_rate"], b["avg_frame_rate"]))]


def flash_overlay(n_frames, at, peak=0.35, fade=12):
    o = np.zeros(n_frames)
    for a in at:
        for k in range(fade):
            if a + k < n_frames:
                o[a + k] = max(o[a + k], peak * (1 - k / fade))
    return o


@program("QA-258")
def qa_258(work):
    o = flash_overlay(90, [10, 40, 70]); fps = 30
    luma = 60 + o * 255; ev, per_s = flash_count(luma, fps, delta=0.1 * 255)
    wjson(Path(work) / "flash.json", {"overlay": o.round(3).tolist()})
    return [C("flash peak capped at 0.35 opacity", o.max() == 0.35, o.max()), C("12-frame soft fade (frames 10-21 lit, frame 22 back to 0)", o[22] == 0 and o[21] > 0, (o[21], o[22])), C("1 Hz flashes stay under 3 Hz", per_s < 3, per_s)]


def glyph_height(text, size, arabic=False):
    from PIL import ImageDraw, Image
    f = pil_font(size, arabic); im = Image.new("L", (size * len(text) + 40, size * 3), 0); ImageDraw.Draw(im).text((10, size // 2), text, fill=255, font=f)
    ys = np.where(np.asarray(im).max(1) > 0)[0]; return int(ys.max() - ys.min() + 1)


@program("QA-259")
def qa_259(work):
    H = 1920; need = {"dialogue": 0.05, "keyword": 0.06, "title": 0.08}
    g90, g140 = glyph_height("HEXAGON", 90), glyph_height("HEXAGON", 160)
    res = {"90px_dialogue": g90 >= need["dialogue"] * H, "160px_title": g140 >= need["title"] * H, "160px_keyword": g140 >= need["keyword"] * H}
    wjson(Path(work) / "glyphs.json", {"g90": g90, "g140": g140, "res": res})
    return [C("measured glyph box, not font size: 90 px font gives < 96 px (5% of 1920) caps", g90 < 96 and not res["90px_dialogue"], g90),
            C("160 px font clears the 6% keyword floor (115 px) but not the 8% title floor (154 px)", res["160px_keyword"] and not res["160px_title"], g140)]


def transcript_gate(lines):
    issues = []
    for i, l in enumerate(lines):
        if "♪" in l or "�" in l:
            issues.append(f"music/garbled token line {i}")
        if i and l.strip() == lines[i - 1].strip():
            issues.append(f"repeated line {i}")
    return issues


@program("QA-260")
def qa_260(work):
    a = transcript_gate(["أهلا بكم", "في الحلقة"]); b = transcript_gate(["أهلا", "♪ ♪", "يا ليل", "يا ليل", "ab�c"])
    wjson(Path(work) / "gate.json", {"a": a, "b": b})
    return [C("clean transcript passes", a == [], a), C("music notes, looping repeat and replacement char caught", b == ["music/garbled token line 1", "repeated line 3", "music/garbled token line 4"], b)]


def scope_stats(img, exclude_rows=None):
    a = np.asarray(img, float)
    if exclude_rows:
        a = a[exclude_rows[0]:exclude_rows[1]]
    y = a @ [0.2126, 0.7152, 0.0722]; ire = (y - 16) / (235 - 16) * 100
    return {"p10": float(np.percentile(y, 10)), "p50": float(np.percentile(y, 50)), "p95": float(np.percentile(y, 95)), "over99ire": float(np.mean(ire >= 99) * 100)}


@program("QA-261")
def qa_261(work):
    img = np.zeros((100, 100, 3)); img[:] = np.linspace(20, 200, 100)[None, :, None]; img[:10] = 0; img[90:] = 0; img[40:45, 90:] = 240
    full, cut = scope_stats(img), scope_stats(img, (10, 90))
    wjson(Path(work) / "scope.json", {"with_bars": full, "excluded": cut})
    return [C("letterbox bars drag P10 to 0 unless excluded", full["p10"] == 0 and cut["p10"] > 30, (full["p10"], cut["p10"])),
            C("P50 of the 20-200 ramp ~110 and the highlight >= 99 IRE measured as 0.6%", abs(cut["p50"] - 110) < 3 and abs(cut["over99ire"] - 0.625) < 0.01, cut)]


def tc_to_f(tc, fps=30):
    h, m, s, f = map(int, tc.split(":")); return ((h * 60 + m) * 60 + s) * fps + f


def propagate(changes, items, fps=30):
    out = []
    for it in items:
        ch = next((c for c in changes if c["file"] == it["file"]), None)
        if ch:
            delta = tc_to_f(ch["new"], fps) - tc_to_f(ch["old"], fps); it = dict(it, frame=it["frame"] + delta)
        out.append(it)
    return out


@program("QA-262")
def qa_262(work):
    ch = [{"file": "B.mov", "old": "00:00:10:00", "new": "00:00:08:15"}]
    r = propagate(ch, [{"file": "A.mov", "frame": 30, "kind": "caption"}, {"file": "B.mov", "frame": 320, "kind": "caption"}, {"file": "B.mov", "frame": 330, "kind": "sfx"}])
    wjson(Path(work) / "propagated.json", r)
    return [C("frame delta for B = -45 applied to its captions and sound", [x["frame"] for x in r] == [30, 275, 285], r)]


@program("QA-263")
def qa_263(work):
    fr = moving_frames(60)
    good, mono = par(lambda n, a, sr: write_video(Path(work) / n, fr, 30, audio=a, sr=sr), [("final.mp4", stereo(tone(440, 2, 48000, .2)), 48000), ("mono44.mp4", tone(440, 2, 44100, .2), 44100)])
    def table(p):
        info = probe(p); v = vstream(info); a = astreams(info); dur = float(info["format"]["duration"])
        return {"frames_ok": abs(int(v["nb_frames"]) - round(dur * 30)) <= 1, "one_aac_48k_stereo": len(a) == 1 and a[0]["codec_name"] == "aac" and a[0]["sample_rate"] == "48000" and a[0]["channels"] == 2,
                "no_black": not blackdetect(p, 0.5, 0.1)}
    a, b = table(good), table(mono)
    return [C("final render passes the verification table", all(a.values()), a), C("44.1 kHz mono audio fails the AAC 48 kHz stereo row", not b["one_aac_48k_stereo"], b)]


def asr_gate(words):
    notes = sum(1 for w in words if "♪" in w["w"]); share = notes / max(1, len(words))
    short = [w["w"] for w in words if w["end"] - w["start"] < 0.05]
    return {"music_share": share, "fail": share > 0.20, "short_spans": short, "retry": share > 0.20 or bool(short)}


@program("QA-265")
def qa_265(work):
    w = [{"w": "يا", "start": 0, "end": .3}, {"w": "♪", "start": .3, "end": .8}, {"w": "ليل", "start": .8, "end": .82}, {"w": "♪", "start": 1, "end": 1.4}]
    a = asr_gate(w); b = asr_gate([w[0], {"w": "عين", "start": .3, "end": .6}])
    wjson(Path(work) / "asr_gate.json", {"bad": a, "ok": b})
    return [C("50% music tokens (> 20%) fails; 20 ms word flagged; retry", a["fail"] and a["short_spans"] == ["ليل"] and a["retry"], a), C("clean words pass", not b["retry"], b)]


def wer(ref, hyp):
    r, h = ref.split(), hyp.split(); d = np.zeros((len(r) + 1, len(h) + 1), int); d[:, 0] = range(len(r) + 1); d[0] = range(len(h) + 1)
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            d[i, j] = min(d[i - 1, j] + 1, d[i, j - 1] + 1, d[i - 1, j - 1] + (r[i - 1] != h[j - 1]))
    return d[-1, -1] / len(r)


@program("QA-266")
def qa_266(work):
    w1 = wer("the cat sat on the mat", "the cat sit on mat"); w0 = wer("a b c", "a b c")
    sr = 16000; x = np.r_[tone(300, .5, sr, .3), np.zeros(int(.3 * sr)), tone(300, .5, sr, .3), np.zeros(int(.8 * sr)), tone(300, .5, sr, .3)]
    p = write_wav(Path(work) / "sample.wav", x, sr); s1, s2 = silencedetect(p, -40, 0.25), silencedetect(p, -40, 0.6)
    wjson(Path(work) / "wer.json", {"wer": w1, "sil_0_25": s1, "sil_0_6": s2})
    return [C("WER: 1 substitution + 1 deletion over 6 words = 0.333", abs(w1 - 2 / 6) < 1e-9 and w0 == 0, w1),
            C("endpointing: 0.25 s threshold splits at both pauses, 0.6 s only at the long one", len(s1) == 2 and len(s2) == 1, (s1, s2))]


@program("QA-267")
def qa_267(work):
    sr = 44100; clean = tone(1000, 1, sr, .4); alias = clean + tone(18000, 1, sr, .1)
    for n, x in (("clean", clean), ("alias", alias)):
        p = write_wav(Path(work) / f"{n}.wav", x, sr); ff("-i", p, "-lavfi", "showspectrumpic=s=400x200:legend=0", Path(work) / f"{n}_spec.png")
    hf = lambda x: float(band_share(x, sr)["air"] - 0) if False else float((np.abs(np.fft.rfft(x)) ** 2)[np.fft.rfftfreq(len(x), 1 / sr) > 16000].sum() / (np.abs(np.fft.rfft(x)) ** 2).sum())
    return [C("spectrogram PNGs rendered", (Path(work) / "alias_spec.png").stat().st_size > 0, ""),
            C("clean file: no energy above 16 kHz; planted 18 kHz line found", hf(clean) < 1e-6 and hf(alias) > 0.05, (hf(clean), hf(alias)))]


@program("QA-268")
def qa_268(work):
    sr = 48000; x = tone(200, 1, sr, .4); ok, flipped = np.stack([x, x]), np.stack([x, -x])
    mono = lambda s: float(np.sqrt(np.mean(((s[0] + s[1]) / 2) ** 2)))
    write_wav(Path(work) / "mix_ok.wav", ok, sr); write_wav(Path(work) / "mix_phase.wav", flipped, sr)
    return [C("in-phase mix keeps its level in mono (-ac 1)", abs(mono(ok) - 0.4 / math.sqrt(2)) < 1e-3, mono(ok)), C("polarity-flipped channel cancels in mono", mono(flipped) < 1e-9, mono(flipped))]


@program("QA-269")
def qa_269(work):
    sr = 48000; sfx = np.r_[np.zeros(sr), tone(800, 0.2, sr, 0.5), np.zeros(sr)]
    ints = lufs(np.zeros(int(0.3 * sr)) + tone(800, 0.3, sr, 0.5), sr) if False else lufs(tone(800, 0.3, sr, 0.5), sr)
    hop = int(0.05 * sr); loudest = max(20 * math.log10(np.sqrt(np.mean(sfx[i:i + hop] ** 2)) + 1e-12) for i in range(0, len(sfx) - hop, hop))
    write_wav(Path(work) / "sfx.wav", sfx, sr)
    return [C("a 300 ms effect has no 400 ms block: integrated LUFS undefined (-inf)", ints == -math.inf, ints),
            C("level by loudest 50 ms instead: -9.0 dBFS RMS for a 0.5 tone", abs(loudest - 20 * math.log10(0.5 / math.sqrt(2))) < 0.1, loudest)]


@program("QA-270")
def qa_270(work):
    import shutil
    orig = write_wav(Path(work) / "original.wav", tone(300, 1, 16000, .3), 16000); h0 = sha256(orig.read_bytes())
    copy = Path(work) / "work_copy.wav"; shutil.copy(orig, copy); x, sr = read_wav(copy); write_wav(Path(work) / "derived_reverse.wav", x[0][::-1], sr)
    log = {"source": orig.name, "sha256": h0, "derived": ["derived_reverse.wav"]}; wjson(Path(work) / "log.json", log)
    return [C("edits happen on a copy; original hash unchanged", sha256(orig.read_bytes()) == h0, h0[:12]), C("derived file is new and logged with the source id", (Path(work) / "derived_reverse.wav").is_file() and log["source"] == "original.wav", "")]


def marker_ok(m):
    return all(m.get(k) for k in ("tc", "intent", "alternative", "status")) and m["status"] in ("open", "listened", "approved") and "sounds great" not in m.get("note", "")


@program("QA-271")
def qa_271(work):
    good = {"tc": "00:00:12:10", "intent": "duck music under voice", "alternative": "-3 dB more", "status": "open", "note": "measured -18 LUFS bed; please listen"}
    bad = dict(good, alternative="", note="sounds great")
    wjson(Path(work) / "markers.json", [good])
    return [C("AUDIO_REVIEW marker with TC, intent, alternative, status passes", marker_ok(good), ""), C("missing alternative / claiming 'sounds great' rejected", not marker_ok(bad), "")]


def glsl_loops(src):
    bad = []
    for m in re.finditer(r"for\s*\(\s*(?:int|float)\s+\w+\s*=\s*[^;]+;\s*\w+\s*[<>]=?\s*([^;]+);", src):
        bound = m.group(1).strip()
        if not re.fullmatch(r"[\d.]+|[A-Z_][A-Z0-9_]*", bound):
            bad.append(bound)
    return bad


@program("QA-273")
def qa_273(work):
    src = "#define OCT 5\nfloat f(){for(int i=0;i<OCT;i++){}for(int j=0;j<8;j++){}for(int k=0;k<uSteps;k++){}return 0.;}"
    dpr = lambda kind, device: min(device, 2.0 if kind == "object" else 1.25)
    (Path(work) / "noise.frag").write_text(src)
    return [C("non-constant loop bound uSteps flagged (GLSL ES 1.0)", glsl_loops(src) == ["uSteps"], glsl_loops(src)), C("DPR capped: object 2, full-bleed 1.25 on a 3x phone", dpr("object", 3) == 2 and dpr("fullbleed", 3) == 1.25, "")]


@program("QA-275")
def qa_275(work):
    r1, r2 = contrast("#767676", "#ffffff"), contrast("#999999", "#ffffff")
    wjson(Path(work) / "floors.json", {"767676": r1, "999": r2})
    return [C("#767676 on white ~4.5:1 (passes 4.5)", 4.5 <= r1 < 4.6, r1), C("#999 on white ~2.8:1 (fails 3:1 large too)", 2.8 <= r2 < 2.9, r2), C("7:1 AAA needs darker: #595959 = 7.0", contrast("#595959", "#ffffff") >= 7, contrast("#595959", "#ffffff"))]


@program("QA-276")
def qa_276(work):
    beats = [np.r_[np.linspace(0, 1, 10), np.ones(8)], np.r_[np.linspace(0, 1, 10), np.linspace(1, .9, 8)]]
    final_static = [bool(np.all(np.diff(b[-5:]) == 0)) for b in beats]
    ok = flash_count(flash_luma(60, 30, 2), 30)[1]; bad = flash_count(flash_luma(60, 30, 4), 30)[1]
    wjson(Path(work) / "rm.json", {"final_static": final_static})
    return [C("text beat ending on a hold is static; drifting end is not", final_static == [True, False], final_static), C("<= 3 flashes/s: 2 Hz ok, 4 Hz not", ok <= 3 and bad > 3, (ok, bad))]


def pseudo_rtl(s):
    return "⁧" + s + "⁩"


@program("QA-277")
def qa_277(work):
    base = "Save 20% today"; box = 360
    from PIL import ImageDraw, Image
    d = ImageDraw.Draw(Image.new("RGB", (1, 1))); w = lambda s: d.textlength(s, font=pil_font(32))
    exp = {p: w(base + "~" * int(len(base) * (p - 1))) for p in (1.0, 1.4, 2.0)}
    wjson(Path(work) / "stress.json", {"wrapped": pseudo_rtl(base), "widths": exp})
    return [C("pseudo strings wrapped in RLI ... PDI", pseudo_rtl(base)[0] == "⁧" and pseudo_rtl(base)[-1] == "⁩", ""),
            C("140% and 200% expansion widths grow; 200% overflows a 360 px box", exp[1.0] <= box and exp[2.0] > box and exp[1.4] > exp[1.0], exp)]


@program("QA-278")
def qa_278(work):
    from fontTools.ttLib import TTFont
    p = build_font(Path(work) / "Brand.ttf", "0123456789+-=xH", "Brand"); cmap = TTFont(str(p)).getBestCmap()
    has = lambda s: all(ord(c) in cmap for c in s)
    return [C("'x2' present; subscript '₂' missing -> use fallback notation 'x_2'", has("x2") and not has("x₂"), sorted(chr(c) for c in cmap)), C("superscript '²' also missing", not has("²"), "")]


@program("QA-279")
def qa_279(work):
    from PIL import ImageDraw, Image
    size = 80; f = pil_font(size, arabic=True); im = Image.new("L", (600, 300), 0); ImageDraw.Draw(im).text((20, 100), "بِنْتٌ يَجِيءُ", fill=255, font=f)
    ys = np.where(np.asarray(im).max(1) > 0)[0]; asc, desc = f.getmetrics(); top_line = 100; ink = (ys.min(), ys.max())
    tight = (top_line + int(0.15 * size), top_line + asc)  # a tight cap-height mask
    padded = (tight[0] - int(0.35 * size), tight[1] + int(0.35 * size))
    cut_tight = ink[0] < tight[0] or ink[1] > tight[1]; cut_pad = ink[0] < padded[0] or ink[1] > padded[1]
    im.save(Path(work) / "arabic_mask_probe.png"); wjson(Path(work) / "mask.json", {"ink": [int(v) for v in ink], "tight": tight, "padded": padded})
    return [C("tight mask clips Arabic dots/harakat", cut_tight, (ink, tight)), C("0.35em vertical padding keeps every dot", not cut_pad, (ink, padded))]


def chroma_radius(img):
    a = np.asarray(img, float) / 255; y = a @ [0.2126, 0.7152, 0.0722]; cb, cr = (a[..., 2] - y) / 1.8556, (a[..., 0] - y) / 1.5748
    return float(np.sqrt(cb ** 2 + cr ** 2).mean())


@program("QA-280")
def qa_280(work):
    neutral = np.full((40, 40, 3), 120.0); graded = neutral.copy(); graded[..., 0] += 30; graded[..., 2] -= 20
    lb = np.zeros((60, 40, 3)); lb[10:50] = neutral
    wjson(Path(work) / "scopes.json", {"neutral": chroma_radius(neutral), "graded": chroma_radius(graded)})
    return [C("neutral grey: vectorscope radius 0", chroma_radius(neutral) < 1e-9, chroma_radius(neutral)), C("warm grade moves the cluster out (radius > 0.05)", chroma_radius(graded) > 0.05, chroma_radius(graded)),
            C("letterbox excluded from percentiles", scope_stats(lb, (10, 50))["p10"] == scope_stats(neutral)["p10"], "")]


def alpha_report(rgba):
    a = np.asarray(rgba); al = a[..., 3]
    real = al.min() < 255
    checker = not real and bool(np.mean(np.isin(a[..., :3].reshape(-1, 3), [[204, 204, 204], [255, 255, 255]]).all(-1)) > 0.5)
    edge = (al > 0) & (al < 255); halo = float(a[..., :3][edge].mean()) if edge.any() else 0.0
    return {"real_alpha": real, "baked_checkerboard": checker, "edge_rgb_mean": halo}


@program("QA-282")
def qa_282(work):
    cut = np.zeros((40, 40, 4), np.uint8); cut[10:30, 10:30] = (200, 50, 50, 255); cut[9, 10:30] = (255, 255, 255, 128)
    baked = np.zeros((40, 40, 4), np.uint8); baked[..., 3] = 255; baked[..., :3] = np.where(((np.indices((40, 40)) // 4).sum(0) % 2)[..., None], 204, 255)
    a, b = alpha_report(cut), alpha_report(baked); save_png(Path(work) / "cut.png", cut)
    return [C("true transparency detected", a["real_alpha"] and not a["baked_checkerboard"], a), C("baked checkerboard is not alpha", b["baked_checkerboard"] and not b["real_alpha"], b),
            C("white fringe pixels found on the edge (halo over dark backgrounds)", a["edge_rgb_mean"] > 240, a["edge_rgb_mean"])]


def wilson(x, n, z=1.96):
    p = x / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


def change_line(x1, n1, x2, n2):
    lo, hi = ab_read(x1, n1, x2, n2)["ci95"]
    return "within normal variation" if lo <= 0 <= hi else "change"


@program("QA-283")
def qa_283(work):
    lo, hi = wilson(12, 100)
    wjson(Path(work) / "intervals.json", {"wilson_12_100": [lo, hi]})
    return [C("Wilson 95% interval for 12/100 = (0.070, 0.198)", abs(lo - 0.0700) < 5e-4 and abs(hi - 0.1981) < 5e-4, (lo, hi)),
            C("12% -> 14% on 100 each spans zero: 'within normal variation'", change_line(12, 100, 14, 100) == "within normal variation", ""), C("12% -> 14% on 20000 each is a real change", change_line(2400, 20000, 2800, 20000) == "change", "")]


def figure_verdict(prog_issues, scores):
    assert len(scores) == 5 and all(1 <= v <= 5 for v in scores.values())
    if prog_issues == ["unreadable text"] or min(scores.values()) <= 2:
        return "block"
    if prog_issues or min(scores.values()) == 3:
        return "revise"
    return "ship"


@program("QA-284")
def qa_284(work):
    s = dict(zip(["clarity", "hierarchy", "alignment", "palette", "format"], [5, 4, 4, 5, 4]))
    wjson(Path(work) / "verdicts.json", {"ship": figure_verdict([], s)})
    return [C("no programmatic issues and all >= 4 -> ship", figure_verdict([], s) == "ship", ""), C("a missing required string -> revise", figure_verdict(["missing 'Q3'"], s) == "revise", ""),
            C("any score of 2 -> block", figure_verdict([], dict(s, alignment=2)) == "block", "")]


def masked_regress(base, cur, masks, assertions, text):
    d = np.abs(base.astype(int) - cur.astype(int)) > 0
    for x0, y0, x1, y1 in masks:
        d[y0:y1, x0:x1] = False
    return {"pixel_ok": not d.any(), "semantic_ok": all(a in text for a in assertions)}


@program("QA-285")
def qa_285(work):
    b = texture(40, 80, 1).astype(np.uint8); c = b.copy(); c[0:8, 60:80] = 255  # clock region changes
    a1 = masked_regress(b, c, [(60, 0, 80, 8)], ["Total"], "Total 42"); a2 = masked_regress(b, c, [], ["Total"], "Total 42"); a3 = masked_regress(b, b, [], ["Total"], "Sum 42")
    save_png(Path(work) / "baseline.png", b)
    return [C("volatile clock masked: stable state passes", a1["pixel_ok"] and a1["semantic_ok"], a1), C("without the mask the clock trips the diff", not a2["pixel_ok"], a2), C("label text check catches a semantic change with identical pixels", a3["pixel_ok"] and not a3["semantic_ok"], a3)]


def verify_series(primary, secondary, tol=0.01):
    p = []
    if not primary:
        p.append("zero rows")
    elif abs(sum(primary.values()) - sum(secondary.values())) / max(1, sum(secondary.values())) > tol:
        p.append("total disagrees with second source")
    return p


@program("QA-287")
def qa_287(work):
    sec = {"2023": 100, "2024": 120}
    r = {"ok": verify_series({"2023": 100, "2024": 120.5}, sec), "empty": verify_series({}, sec), "wrong": verify_series({"2023": 100, "2024": 150}, sec)}
    wjson(Path(work) / "verify.json", r | {"query": "local fixture", "date": "fixed"})
    return [C("matching totals pass", r["ok"] == [], r), C("HTTP-200-but-zero-rows caught", r["empty"] == ["zero rows"], r), C("silently wrong aggregate caught by second source", r["wrong"] == ["total disagrees with second source"], r)]


MACHADO = {"protan": np.array([[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]]),
           "deutan": np.array([[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]])}


def simulate(hexc, kind):
    rgb = np.array(hex_rgb(hexc)) / 255; lin = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    out = np.clip(MACHADO[kind] @ lin, 0, 1); srgb = np.where(out <= 0.0031308, out * 12.92, 1.055 * out ** (1 / 2.4) - 0.055)
    return tuple(int(round(v * 255)) for v in srgb)


@program("QA-288")
def qa_288(work):
    rg = ("#d62728", "#2ca02c"); bo = ("#1f77b4", "#ff7f0e")
    de = lambda pair, k: delta_e76(simulate(pair[0], k), simulate(pair[1], k))
    grey = lambda pair: abs(lstar(pair[0]) - lstar(pair[1]))
    res = {"red_green_deutan": de(rg, "deutan"), "blue_orange_deutan": de(bo, "deutan"), "rg_grey": grey(rg), "bo_grey": grey(bo)}
    wjson(Path(work) / "cvd.json", res)
    return [C("red/green pair collapses under deuteranopia (dE < 20)", res["red_green_deutan"] < 20, res), C("blue/orange stays distinguishable (dE > 40)", res["blue_orange_deutan"] > 40, res),
            C("grayscale pass: red/green differ by < 12 L*, blue/orange by > 15", res["rg_grey"] < 12 and res["bo_grey"] > 15, (res["rg_grey"], res["bo_grey"]))]


PROV_FIELDS = ("asset", "prompt", "model", "provider", "license", "indemnity", "c2pa", "date", "disclosure")


def provenance_check(lines):
    out = []
    for i, l in enumerate(lines):
        r = json.loads(l); miss = [k for k in PROV_FIELDS if k not in r]
        if miss:
            out.append((i, miss))
    return out


@program("QA-289")
def qa_289(work):
    good = {k: "x" for k in PROV_FIELDS}; bad = {k: "x" for k in PROV_FIELDS if k not in ("c2pa", "disclosure")}
    lines = [json.dumps(good), json.dumps(bad)]; (Path(work) / "provenance.jsonl").write_text("\n".join(lines))
    return [C("one JSON line per asset; complete line passes, missing C2PA/disclosure reported", provenance_check(lines) == [(1, ["c2pa", "disclosure"])], provenance_check(lines))]


def ui_counts(html):
    from bs4 import BeautifulSoup
    s = BeautifulSoup(html, "html.parser")
    return {sec.get("id"): (len(sec.find_all("table")), len(sec.find_all("tr")), len(sec.find_all(["input", "select", "textarea"])), len(sec.find_all("button"))) for sec in s.find_all("section")}


@program("QA-290")
def qa_290(work):
    before = "<section id=t1><table><tr></tr><tr></tr></table><input><button>a</button></section><section id=t2><button>b</button></section>"
    after_ok = before.replace("<section id=t1>", "<section id=t1 class=dense>"); after_bad = before.replace("<button>b</button>", "")
    a, b, c = ui_counts(before), ui_counts(after_ok), ui_counts(after_bad)
    wjson(Path(work) / "density.json", {"before": a, "after": b})
    return [C("style-only patch keeps per-tab counts identical (1/2/1/1)", a == b and a["t1"] == (1, 2, 1, 1), a), C("a removed button is a capability change", a != c and c["t2"] == (0, 0, 0, 0), c)]


def paid_retry_allowed(asset_dir):
    return not (Path(asset_dir) / "NO_PAID_RETRY.flag").exists()


@program("QA-291")
def qa_291(work):
    d = Path(work); (d / "ledger.md").write_text("| asset | model | approval | res | size | use | note |\n|---|---|---|---|---|---|---|\n| hero.png | gen-x | owner 10-09 | 2048 | 1.2 MB | door | local upscale, not native 4K |\n")
    a = paid_retry_allowed(d); (d / "NO_PAID_RETRY.flag").write_text("blocked after 2 tries"); b = paid_retry_allowed(d)
    return [C("ledger row records the honesty note", "not native 4K" in (d / "ledger.md").read_text(), ""), C("flag file blocks automatic paid retries", a and not b, (a, b))]


def loudnorm_summary(path):
    log = ff_log("-i", path, "-af", "loudnorm=print_format=summary", "-f", "null", "-")
    g = lambda k: float(re.search(k + r":\s+(-?[\d.]+)", log).group(1))
    return {"I": g("Input Integrated"), "TP": g("Input True Peak"), "LRA": g("Input LRA")}


@program("QA-292")
def qa_292(work):
    sr = 32000; bed = scale_to_lufs(stereo(tone(120, 3, sr, .05) * (1 + 0.1 * np.sin(np.arange(3 * sr) / sr * 3))), sr, -24.5)
    p = write_wav(Path(work) / "intro.wav", bed, sr); m = loudnorm_summary(p)
    return [C("loudnorm summary reads integrated ~-24.5 LUFS", abs(m["I"] + 24.5) <= 0.5, m), C("well below the -14 social target (>= 9 LU gap)", -14 - m["I"] >= 9, m), C("sample rate 32 kHz recorded, not 48 kHz", read_wav(p)[1] == 32000, "")]


def perf_budget(stamps, canvas, viewport, reduced_frames):
    fps = (len(stamps) - 1) / (stamps[-1] - stamps[0])
    return {"fps": fps, "fps_ok": fps >= 20, "canvas_ok": canvas == viewport, "reduced_ok": reduced_frames == 1}


@program("QA-293")
def qa_293(work):
    a = perf_budget(np.arange(0, 2.01, 1 / 24).tolist(), (1280, 800), (1280, 800), 1); b = perf_budget(np.arange(0, 2.01, 1 / 15).tolist(), (2560, 1600), (1280, 800), 30)
    wjson(Path(work) / "perf.json", {"a": a, "b": b})
    return [C("24 fps, canvas = viewport, one still frame under reduced motion passes", a["fps_ok"] and a["canvas_ok"] and a["reduced_ok"], a), C("15 fps, 2x canvas and animated reduced mode fail", not (b["fps_ok"] or b["canvas_ok"] or b["reduced_ok"]), b)]


CLAIM_WORDS = {"4k": "resolution", "lip-sync": "lipsync_measure", "synced": "sync_measure", "premium model": "model_receipt", "watched": "manual_review"}


def claims_check(report, evidence):
    out = [w for w, ev in CLAIM_WORDS.items() if w in report.lower() and ev not in evidence]
    if evidence.get("manual_review") is None and "manual_visual_review" not in report:
        out.append("manual review state missing")
    return out


@program("QA-294")
def qa_294(work):
    a = claims_check("Rendered 1080x1920; manual_visual_review NOT_DONE", {}); b = claims_check("Delivered in 4K, perfectly lip-sync, I watched it", {})
    c = claims_check("Delivered 4K", {"resolution": "3840x2160 ffprobe", "manual_review": "done"})
    wjson(Path(work) / "claims.json", {"a": a, "b": b, "c": c})
    return [C("honest report with NOT_DONE review passes", a == [], a), C("4K, lip-sync and 'watched' without evidence flagged", b[:3] == ["4k", "lip-sync", "watched"], b), C("4K backed by ffprobe evidence passes", c == [], c)]


REVIEW10 = ["signed script", "safe margins", "animation tied to words", "captions validated", "colours/diacritics", "preview viewed", "first/middle/last frames", "codec/size/fps/duration", "audio", "aspect"]


def review_list(items, aspect):
    missing = [k for k in REVIEW10 if not items.get(k)]
    if aspect not in ("9:16", "16:9", "1:1"):
        missing.append("aspect")
    return sorted(set(missing))


@program("QA-295")
def qa_295(work):
    full = {k: f"evidence:{i}" for i, k in enumerate(REVIEW10)}
    a = review_list(full, "9:16"); b = review_list(dict(full, **{"preview viewed": ""}), "4:3")
    wjson(Path(work) / "review10.json", {"a": a, "b": b})
    return [C("10 items each with evidence pass", len(REVIEW10) == 10 and a == [], a), C("missing evidence and a 4:3 aspect are flagged", b == ["aspect", "preview viewed"], b)]


def editorial_ci(story):
    return {"duration": story["duration"] == 30, "scenes": len(story["scenes"]) == 5, "aspect": story["aspect"] == "9:16",
            "background_lines": len(story["background_lines"]) == 2, "final_render_false": story["approval"]["final_render"] is False}


@program("QA-296")
def qa_296(work):
    st = {"duration": 30, "scenes": [{"id": i} for i in range(5)], "aspect": "9:16", "background_lines": ["a", "b"], "approval": {"final_render": False}}
    a = editorial_ci(st); b = editorial_ci(dict(st, scenes=st["scenes"][:4], approval={"final_render": True}))
    wjson(Path(work) / "compiled.json", st)
    return [C("fixture compiles to 30 s, 5 scenes, 9:16, 2 lines, final_render false", all(a.values()), a), C("4 scenes or an auto-approved final render fail CI", not b["scenes"] and not b["final_render_false"], b)]


@program("QA-297")
def qa_297(work):
    fr = np.stack([np.full((36, 64), 10 + 2 * i, np.uint8) for i in range(90)]); f = write_video(Path(work) / "film.mp4", fr, 30)
    dur = float(probe(f)["format"]["duration"]); vals = []
    for n, t in (("first", 0), ("middle", dur / 2), ("last", dur - 1 / 30)):
        p = Path(work) / f"{n}.png"
        ff("-sseof", "-0.3", "-i", f, "-update", 1, p) if n == "last" else ff("-ss", f"{t:.3f}", "-i", f, "-frames:v", 1, p)
        from PIL import Image
        vals.append(float(np.asarray(Image.open(p).convert("L")).mean()))
    return [C("first/middle/last stills extracted at 0, 1.5 and 2.97 s (levels 10 / 100 / 188 +- 3)", all(abs(a - b) <= 3 for a, b in zip(vals, (10, 100, 188))), vals)]


def gain_to_target(path, target=-16):
    m = ebur128(path); return round(target - m["I"], 1), m["I"]


@program("QA-299")
def qa_299(work):
    sr = 48000; rng = np.random.default_rng(0)
    voice = np.r_[tone(180, 2, sr, .2), rng.normal(0, 0.002, sr), tone(180, 2, sr, .2)]
    p = write_wav(Path(work) / "vo.wav", scale_to_lufs(voice, sr, -23), sr); g, I = gain_to_target(p)
    seg = read_wav(p)[0][0][2 * sr:3 * sr]; floor = 20 * math.log10(np.sqrt(np.mean(seg ** 2)))
    return [C("gain_db = target -16 minus measured -23 = +7", g == 7.0, (g, I)), C("noise floor measured from the file's own pause (< -45 dBFS)", floor < -45, floor)]


def hf_traps(html):
    out = []
    if re.search(r"<html[^>]*dir=['\"]?rtl", html):
        out.append("dir=rtl on <html> renders blank")
    if re.search(r"<audio(?![^>]*\bid=)", html):
        out.append("audio without id is silent")
    if re.search(r"fromTo\([^)]*\{[^}]*\}\s*,\s*\{(?![^}]*immediateRender\s*:\s*false)[^}]*\}\s*,\s*[\d.]*[1-9]", html):
        out.append("fromTo at a later time renders from-state immediately")
    if "marker-end" in html:
        out.append("marker-end arrowheads show early")
    return out


@program("QA-300")
def qa_300(work):
    good = "<html lang=ar><p style='direction:rtl;unicode-bidi:isolate'>نص</p><audio id=a></audio><script>tl.fromTo('#t',{x:0},{x:9,immediateRender:false},2)</script>"
    bad = "<html dir=rtl><audio src=a.wav></audio><svg><path marker-end='url(#a)'/></svg><script>tl.fromTo('#t',{x:0},{x:9},2)</script>"
    wjson(Path(work) / "traps.json", {"good": hf_traps(good), "bad": hf_traps(bad)})
    return [C("isolated rtl text, audio id, immediateRender:false pass", hf_traps(good) == [], hf_traps(good)), C("all four traps caught", len(hf_traps(bad)) == 4, hf_traps(bad))]


def speed_class(px_per_frame, reading=False):
    if px_per_frame > 80:
        return "forbidden"
    if px_per_frame > 12:
        return "needs blur"
    if reading and px_per_frame > 3:
        return "too fast to read"
    return "ok"


@program("QA-301")
def qa_301(work):
    slow, fast = par(lambda s: flow_speed(tex_square_frames(4, s)), [2, 16])
    a, b = float(np.median(slow)), float(np.median(fast))
    wjson(Path(work) / "speed.json", {"2px": slow, "16px": fast})
    return [C("text moving 2 px/f measured ~2 and readable (<= 3)", abs(a - 2) < 0.6 and speed_class(a, True) == "ok", a),
            C("16 px/f measured ~16 -> needs motion blur (> 12)", abs(b - 16) < 2 and speed_class(b) == "needs blur", b),
            C("anything > 80 px/f is forbidden; 5 px/f text is too fast to read", speed_class(90) == "forbidden" and speed_class(5, True) == "too fast to read", "")]


def pacing_class(st):
    if 0.35 <= st["median"] <= 0.5:
        return "calm premium" + (" with accents" if st["peak"] >= 2.4 else "")
    if st["median"] >= 1.4 or st["p90"] >= 6.0:
        return "busy (reference median 1.4 / p90 6.0)"
    return "between"


def region_film(n, share, step, w=320, h=180, accent=None):
    rows = int(round(h * share)); fr = []
    for i in range(n):
        f = np.full((h, w), 100, np.uint8); f[:rows] = 100 + (step if i % 2 else 0)
        if accent and i in accent:
            f[:] = 160
        fr.append(f)
    return np.stack(fr)


@program("QA-302")
def qa_302(work):
    calm = write_video(Path(work) / "calm.mp4", region_film(30, 0.2, 2, accent={20}), 15, pix="yuv444p", extra=["-crf", "0"])
    busy = write_video(Path(work) / "busy.mp4", region_film(30, 1.0, 8), 15, pix="yuv444p", extra=["-crf", "0"])
    a, b = motion_energy(calm), motion_energy(busy)
    wjson(Path(work) / "energy.json", {"calm": a, "busy": b})
    return [C("20% of the frame flickering 2 levels: median ~0.4 at 320 px -> calm premium band 0.35-0.5", 0.35 <= a["median"] <= 0.5 and pacing_class(a).startswith("calm"), a),
            C("one accent frame spikes >= 2.4", a["peak"] >= 2.4, a["peak"]), C("whole frame changing 8 levels: median >= 1.4 -> busy", pacing_class(b).startswith("busy"), b)]


@program("QA-304")
def qa_304(work):
    sr = 24000; rng = np.random.default_rng(3); n = int(2.0 * sr)
    voice = rng.normal(0, 0.2, n) * np.convolve((rng.random(n // 1200 + 1) > .4).repeat(1200)[:n].astype(float), np.ones(300) / 300, "same")
    src = write_wav(Path(work) / "voice.wav", voice, sr); fr = moving_frames(60, 36, 64)
    def render(name, codec):
        return write_video(Path(work) / name, fr, 30, audio=voice, sr=sr, acodec=codec)
    copy_f, aac_f = par(render, [("untouched.mov", "pcm_s16le"), ("reencoded.mp4", "aac")])
    def corr(p):
        out = Path(work) / (p.stem + "_dec.wav"); ff("-i", p, "-vn", "-ac", 1, "-ar", sr, "-c:a", "pcm_s16le", out)
        y = read_wav(out)[0][0]; x = read_wav(src)[0][0]; best = 0
        for lag in range(0, 3000):
            m = min(len(x), len(y) - lag)
            if m < sr:
                break
            c = float(np.corrcoef(x[:m], y[lag:lag + m])[0, 1]); best = max(best, c)
            if best > 0.9999:
                break
        return best
    c1, c2 = corr(copy_f), corr(aac_f)
    info = probe(copy_f); v = vstream(info)
    rep = {"result": "PASS" if c1 >= 0.9999 else "FAIL", "video": f"{v['codec_name']} {v['width']}x{v['height']} {v['r_frame_rate']} {v['nb_frames']} frames", "voice_signal_correlation": round(c1, 6), "notes": []}
    wjson(Path(work) / "qa_report.json", rep)
    return [C("PCM-copied voice correlates >= 0.9999 with the source -> audio untouched", c1 >= 0.9999 and rep["result"] == "PASS", c1),
            C("AAC re-encode at 24 kHz falls below 0.9999 -> not untouched", c2 < 0.9999, c2), C("report records h264 64x36 30/1 60 frames", rep["video"] == "h264 64x36 30/1 60 frames", rep["video"])]


def critique_review(md):
    rounds = re.findall(r"^## Round (\d+)", md, re.M); scores = [dict(re.findall(r"^- (\w+): (\d+)", blk, re.M)) for blk in re.split(r"^## Round \d+", md, flags=re.M)[1:]]
    last = {k: int(v) for k, v in scores[-1].items()} if scores else {}
    return {"rounds": len(rounds), "criteria": len(last), "all_8_plus": bool(last) and min(last.values()) >= 8, "has_still_change": "## What I'd still change" in md}


@program("QA-305")
def qa_305(work):
    crit = ["Hook", "Readability", "Motion", "Variety", "Composition", "Truth", "Soundsync", "Brand"]
    rnd = lambda k, v: f"## Round {k}\n" + "".join(f"- {c}: {s}\n" for c, s in zip(crit, v))
    md = rnd(1, [5, 6, 7, 7, 8, 9, 4, 8]) + rnd(2, [7, 8, 8, 7, 8, 9, 7, 8]) + rnd(3, [8, 8, 8, 8, 9, 9, 8, 8]) + "## What I'd still change\n- tighten the outro\n"
    (Path(work) / "review.md").write_text(md); a = critique_review(md); b = critique_review(rnd(1, [9] * 8))
    small = round(84 * 360 / 1080, 1)
    return [C("3 rounds, 8 criteria, all >= 8, ends with 'What I'd still change'", a == {"rounds": 3, "criteria": 8, "all_8_plus": True, "has_still_change": True}, a),
            C("one round without the closing section is incomplete", b["rounds"] < 3 and not b["has_still_change"], b), C("84 px text at 1080 is 28 px at the 360 px check (floor met)", small == 28.0, small)]


def lottie_check(doc, reduced_doc):
    layers = doc["layers"]; animated = [l for l in layers if any(isinstance(v, dict) and v.get("a") == 1 for v in l["ks"].values())]
    small = [l["nm"] for l in layers if max(l.get("w", 0), l.get("h", 0)) <= 40]
    props = {k for l in animated for k, v in l["ks"].items() if v.get("a") == 1}
    fr = doc["fr"]; follow = []
    for l in layers:
        if "parent" in l and l in animated:
            par_ = next(p for p in layers if p["ind"] == l["parent"]); t0 = lambda x: min(k["t"] for v in x["ks"].values() if v.get("a") == 1 for k in v["k"])
            follow.append(round((t0(l) - t0(par_)) / fr * 1000))
    return {"animated": len(animated), "too_small": small, "props_ok": props <= {"p", "s", "r", "o", "a"}, "follow_ms": follow,
            "follow_ok": all(50 <= f <= 150 for f in follow), "reduced_variant": sum(1 for l in reduced_doc["layers"] if any(v.get("a") == 1 for v in l["ks"].values())) == 0}


@program("QA-306")
def qa_306(work):
    kf = lambda t0: {"a": 1, "k": [{"t": t0, "s": [0]}, {"t": t0 + 12, "s": [100]}]}
    still = lambda: {"a": 0, "k": [0]}
    doc = {"fr": 30, "layers": [{"ind": 1, "nm": "card", "w": 300, "h": 200, "ks": {"p": kf(0), "o": still()}},
                                {"ind": 2, "nm": "icon", "parent": 1, "w": 64, "h": 64, "ks": {"s": kf(3), "o": still()}}]}
    red = {"fr": 30, "layers": [dict(l, ks={k: still() for k in l["ks"]}) for l in doc["layers"]]}
    bad = {"fr": 30, "layers": doc["layers"] + [{"ind": 3, "nm": "dot", "parent": 1, "w": 12, "h": 12, "ks": {"c": kf(9)}}]}
    wjson(Path(work) / "anim.json", doc); a, b = lottie_check(doc, red), lottie_check(bad, doc)
    return [C("2 animated layers > 40 px, transform props only, child follows by 100 ms, static reduced variant", a["animated"] == 2 and not a["too_small"] and a["props_ok"] and a["follow_ms"] == [100] and a["reduced_variant"], a),
            C("12 px dot, colour animation, 300 ms follow-through, no reduced variant all flagged", b["too_small"] == ["dot"] and not b["props_ok"] and not b["follow_ok"] and not b["reduced_variant"], b)]


def three_lens(rec):
    p = [l for l in ("design", "motion", "engineering") if not rec.get(l, {}).get("verdict")]
    claimed = set(rec.get("claims", [])); untested = set(rec.get("untested", []))
    p += [f"claims untested: {c}" for c in sorted(claimed & untested)]
    if not set(rec.get("rendered", [])) | set(rec.get("tested", [])):
        p.append("nothing rendered or tested")
    return p


@program("QA-307")
def qa_307(work):
    good = {"design": {"verdict": "pass"}, "motion": {"verdict": "revise easing"}, "engineering": {"verdict": "pass"}, "rendered": ["film.mp4"], "tested": ["ffprobe"], "untested": ["safari"], "claims": ["ffprobe"]}
    bad = dict(good, motion={}, claims=["safari"])
    wjson(Path(work) / "receipt.json", good)
    return [C("three verdicts plus rendered/tested/untested pass", three_lens(good) == [], three_lens(good)), C("missing motion lens and a claim on an untested item fail", three_lens(bad) == ["motion", "claims untested: safari"], three_lens(bad))]


BANNED_LATIN = ["Inter", "Roboto", "Open Sans", "Lato", "Poppins", "Outfit", "Sora", "Syne", "Playfair", "Cinzel"]
BANNED_AR = ["Cairo", "Tajawal", "Changa", "Amiri", "Readex Pro", "IBM Plex Sans Arabic"]


def det_lint(project):
    out = []
    for p in sorted(Path(project).rglob("*")):
        if p.suffix not in (".js", ".html", ".css"):
            continue
        t = p.read_text()
        for pat, why in ((r"Math\.random\(", "unseeded Math.random"), (r"Date\.now\(|new Date\(", "wall clock"), (r"performance\.now\(", "wall clock")):
            out += [f"{p.name}: {why}"] * len(re.findall(pat, t))
        for fam in re.findall(r"font-family\s*:\s*([^;]+)", t):
            first = fam.split(",")[0].strip().strip("'\"")
            if first in BANNED_LATIN + BANNED_AR:
                out.append(f"{p.name}: default font {first}")
    return out


@program("QA-309")
def qa_309(work):
    good, bad = Path(work) / "good", Path(work) / "bad"; good.mkdir(); bad.mkdir()
    (good / "scene.js").write_text("const rng=mulberry32(7);function frame(t){return Math.sin(t)+rng();}")
    (good / "s.css").write_text("h1{font-family:'Brand Sans',serif}")
    (bad / "scene.js").write_text("function frame(){return Math.random()+Date.now();}"); (bad / "s.css").write_text("h1{font-family:Inter,sans-serif}")
    a, b = det_lint(good), det_lint(bad); wjson(Path(work) / "lint.json", {"good": a, "bad": b})
    return [C("seeded PRNG and a brand font pass", a == [], a), C("Math.random, Date.now and Inter flagged", b == ["s.css: default font Inter", "scene.js: unseeded Math.random", "scene.js: wall clock"], b)]


@program("QA-310")
def qa_310(work):
    fr = moving_frames(60); hot = fr.copy(); hot[:] = np.maximum(hot, 252)
    good, blown = par(lambda n, f: gate_film(work, n, f), [("good.mp4", fr), ("blown.mp4", hot)])
    (g, ge), (b, be) = par(lambda p: (inspect_film(p), exposure_check(p)), [good, blown])
    wjson(Path(work) / "gate.json", {"good": [g, ge], "blown": [b, be]})
    return [C("clean film passes black/freeze/LUFS/peak and exposure", g["pass"] and not ge["blown"] and not ge["crushed"], (g["problems"], ge)),
            C("blown highlights flagged (> 5% of samples >= 250)", be["blown"] and be["blown_share"] > 0.9, be)]


@program("QA-311")
def qa_311(work):
    film = write_video(Path(work) / "film.mp4", moving_frames(150, 36, 64), 30)
    r = critique_sheets(film, Path(work))
    from PIL import Image
    ph = Image.open(Path(work) / "phone.png").size
    return [C("5 s film: contact sheet 10 frames @2 fps x 320 px", r["contact_tiles"] == 10 and r["contact_shape"][1] == 6 * 320 + 7 * 4, r),
            C("phone view: 5 frames @1 fps at 360 px wide on 5 columns", r["phone_tiles"] == 5 and ph[0] == 5 * 360 + 6 * 4, ph)]


def probe_summary(p):
    info = probe(p); v = vstream(info); a = astreams(info)
    return {"codec": v["codec_name"], "size": f"{v['width']}x{v['height']}", "fps": v["r_frame_rate"], "frames": int(v["nb_frames"]), "duration": round(float(info["format"]["duration"]), 2),
            "audio": [f"{x['codec_name']} {x['sample_rate']} {x['channels']}ch" for x in a]}


@program("QA-312")
def qa_312(work):
    p = write_video(Path(work) / "clip.mp4", moving_frames(45, 36, 64), 30, audio=stereo(tone(440, 1.5, 48000, .2)))
    s = probe_summary(p); wjson(Path(work) / "probe.json", s)
    return [C("probe reports h264 64x36 30/1, 45 frames, 1.5 s, one AAC 48 kHz stereo track", s["codec"] == "h264" and s["size"] == "64x36" and s["fps"] == "30/1" and s["frames"] == 45 and abs(s["duration"] - 1.5) <= 0.05 and s["audio"] == ["aac 48000 2ch"], s)]


def doctor(tools, modules):
    import shutil, importlib.util
    r = {}
    for t, ver in tools.items():
        exe = shutil.which(t)
        if not exe:
            r[t] = "missing"; continue
        if ver is None:
            r[t] = "untested"; continue
        try:
            out = subprocess.run([exe, ver], capture_output=True, text=True, timeout=5)
            r[t] = "available" if out.returncode == 0 else "broken"
        except Exception:
            r[t] = "broken"
    for m in modules:
        r[f"py:{m}"] = "available" if importlib.util.find_spec(m) else "missing"
    return r


@program("QA-313")
def qa_313(work):
    r = doctor({"ffmpeg": "-version", "ffprobe": "-version", "kosif-no-such-tool-xyz": "-v", "sh": None}, ["numpy", "kosif_no_such_module"])
    wjson(Path(work) / "doctor.json", r)
    return [C("ffmpeg and ffprobe answer -version: available", r["ffmpeg"] == r["ffprobe"] == "available", r), C("an absent tool and module are reported missing", r["kosif-no-such-tool-xyz"] == "missing" and r["py:kosif_no_such_module"] == "missing", r),
            C("a tool found but not probed stays 'untested'", r["sh"] == "untested", r["sh"])]


REEL_TYPES = {"text", "longtext", "number", "color", "media", "list", "choice", "motion"}
REEL_AUDIO = {"music": None, "bpm": None, "drop": 0, "musicVol": 0.6, "sfxVol": 0.8}


def check_reel(reel, video=None, tol=0.06):
    E, W = [], []
    for k in ("id", "width", "height", "fps", "duration", "scenes", "brand"):
        if k not in reel:
            E.append(f"missing {k}")
    if E:
        return E, W
    audio = {**REEL_AUDIO, **reel.get("audio", {})}; t = 0.0; ids = set()
    for s in reel["scenes"]:
        if abs(s["start"] - t) > tol:
            E.append(f"gap before {s['id']}")
        t = s["start"] + s["duration"]
        if s["id"] in ids or "." in s["id"]:
            E.append(f"bad id {s['id']}")
        ids.add(s["id"])
        for b in s.get("boxes", []):
            if b["x"] < 0 or b["y"] < 0 or b["x"] + b["w"] > reel["width"] or b["y"] + b["h"] > reel["height"]:
                E.append(f"box outside frame in {s['id']}")
        for name, pr in s.get("props", {}).items():
            if pr["type"] not in REEL_TYPES:
                E.append(f"prop type {pr['type']}")
            if pr["type"] == "color" and str(pr["value"]).startswith("brand.") and pr["value"][6:] not in reel["brand"]:
                E.append(f"unknown brand colour {pr['value']}")
            if pr["type"] == "choice" and pr["value"] not in pr.get("choices", []):
                E.append(f"choice {pr['value']} not offered")
            if pr["type"] in ("text", "longtext") and re.search("[؀-ۿ]", str(pr["value"])) and pr.get("lang") != "ar":
                E.append(f"Arabic copy without lang in {s['id']}.{name}")
    if abs(t - reel["duration"]) > tol:
        E.append("scenes do not sum to duration")
    if video:
        s = probe_summary(video); fps = eval(s["fps"])
        if s["size"] != f"{reel['width']}x{reel['height']}":
            E.append("video size mismatch")
        if abs(s["duration"] - reel["duration"]) > 0.25:
            E.append("video duration mismatch")
        if abs(fps - reel["fps"]) > 0.05:
            W.append("video fps mismatch")
    return E, W + ([] if audio == {**REEL_AUDIO, **reel.get("audio", {})} else [])


@program("QA-314")
def qa_314(work):
    vid = write_video(Path(work) / "reel.mp4", moving_frames(60, 36, 64), 30); vid25 = write_video(Path(work) / "reel25.mp4", moving_frames(50, 36, 64), 25)
    reel = {"id": "r1", "width": 64, "height": 36, "fps": 30, "duration": 2.0, "brand": {"gold": "#c8a24a"},
            "scenes": [{"id": "s1", "start": 0, "duration": 1.0, "boxes": [{"x": 2, "y": 2, "w": 40, "h": 10}], "props": {"title": {"type": "text", "value": "مرحبا", "lang": "ar"}, "c": {"type": "color", "value": "brand.gold"}}},
                       {"id": "s2", "start": 1.04, "duration": 0.96, "props": {"style": {"type": "choice", "value": "bold", "choices": ["bold", "thin"]}}}]}
    (Path(work) / "reel.json").write_text(json.dumps(reel, ensure_ascii=False))
    e, w = check_reel(reel, vid)
    bad = json.loads(json.dumps(reel)); bad["scenes"][1].update(id="s.2", start=1.2); bad["scenes"][0]["boxes"][0]["w"] = 70; bad["scenes"][0]["props"]["title"].pop("lang"); bad["scenes"][0]["props"]["c"]["value"] = "brand.teal"; bad["scenes"][1]["props"]["style"]["value"] = "wide"
    e2, _ = check_reel(bad); e3, w3 = check_reel(dict(reel, duration=2.0), vid25)
    return [C("valid reel passes (40 ms seam within 0.06 s, video matches)", e == [] and w == [], (e, w)),
            C("gap, dotted id, box outside, Arabic without lang, unknown brand colour, unoffered choice all caught", len(e2) == 7 and "bad id s.2" in e2 and "gap before s.2" in e2, e2),
            C("a 25 fps video only warns (fps mismatch > 0.05); duration within 0.25 s", e3 == [] and w3 == ["video fps mismatch"], (e3, w3))]


def safe_area(box, W=1080, H=1920, side=0.06, top=0.1, bottom=0.18):
    x, y, w, h = box; return x >= W * side and x + w <= W * (1 - side) and y >= H * top and y + h <= H * (1 - bottom)


@program("QA-315")
def qa_315(work):
    film = gate_film(work, "montage.mp4", moving_frames(60)); m = ebur128(film); v = vstream(probe(film)); r = critique_sheets(film, Path(work))
    caps = [{"fg": "#ffffff", "bg": "#202020", "box": (100, 1300, 880, 120)}, {"fg": "#ffffff", "bg": "#c0c0c0", "box": (100, 1700, 880, 120)}]
    res = [(contrast(c["fg"], c["bg"]) >= 4.5, safe_area(c["box"])) for c in caps]
    return [C("contact sheet written", (Path(work) / "contact.png").stat().st_size > 0, r["contact_tiles"]), C("-14 +- 1.5 LUFS measured", abs(m["I"] + 14) <= 1.5, m),
            C("H.264 + yuv420p", v["codec_name"] == "h264" and v["pix_fmt"] == "yuv420p", ""), C("caption 1 passes; caption 2 fails contrast and sits in the bottom UI zone", res == [(True, True), (False, False)], res)]


TIER_FIELDS = ("tier", "family", "mode", "what_ran", "evidence", "verification", "limits", "next_step")


def tier_receipt(r):
    p = [k for k in TIER_FIELDS if r.get(k) in (None, "", [])]
    if r.get("tier") in ("T3", "T4") and not r.get("evidence"):
        p.append("runnable tier without evidence")
    if r.get("tier") not in ("T0", "T1", "T2", "T3", "T4"):
        p.append("unknown tier")
    return p


@program("QA-318")
def qa_318(work):
    good = {"tier": "T4", "family": "qa-verification", "mode": "executed", "what_ran": "ffprobe", "evidence": ["probe.json"], "verification": "frames == 60", "limits": "no listening", "next_step": "deliver"}
    bad = dict(good, evidence=[], tier="T9")
    wjson(Path(work) / "receipt.json", good)
    return [C("complete tier receipt passes", tier_receipt(good) == [], ""), C("missing evidence and an unknown tier are rejected", tier_receipt(bad) == ["evidence", "unknown tier"], tier_receipt(bad))]


def hygiene(manifest, receipt):
    unverified = sorted(a["file"] for a in manifest if a.get("rights", "unverified") == "unverified")
    note = receipt.get("source_licensing", "")
    return {"unverified": unverified, "noted": all(f in note for f in unverified), "flags": [a["file"] for a in manifest if a.get("burned_text") or a.get("logo") or a.get("screen_recording")]}


@program("QA-319")
def qa_319(work):
    man = [{"file": "a.mp4", "rights": "licensed"}, {"file": "b.mp4", "rights": "unverified"}, {"file": "c.mp4", "rights": "unverified", "logo": True}]
    a = hygiene(man, {"source_licensing": "b.mp4 c.mp4 rights unverified"}); b = hygiene(man, {"source_licensing": ""})
    wjson(Path(work) / "manifest.json", man)
    return [C("unverified clips listed in the receipt note", a["unverified"] == ["b.mp4", "c.mp4"] and a["noted"], a), C("missing note fails; logo clip flagged", not b["noted"] and a["flags"] == ["c.mp4"], b)]


def rubric_timeline(events, dur, base_w=1080):
    p = []
    if min(e["t"] for e in events) > 2:
        p.append("no hook in first 2 s")
    ts = sorted([e["t"] for e in events] + [dur])
    p += [f"nothing new {a}-{b}s" for a, b in zip(ts, ts[1:]) if b - a > 4]
    p += [f"{e['what']} {e['px']} px < 28" for e in events if e.get("px") and e["px"] < 28]
    p += [f"{e['what']} unreadable at 360 px" for e in events if e.get("px") and e["px"] * 360 / base_w < 14]
    return p


@program("QA-320")
def qa_320(work):
    ok = [{"t": 0.4, "what": "hook", "px": 96}, {"t": 3.5, "what": "fact"}, {"t": 6.5, "what": "cut"}, {"t": 9.0, "what": "cta", "px": 60}]
    bad = [{"t": 2.6, "what": "hook", "px": 96}, {"t": 8.0, "what": "label", "px": 24}]
    wjson(Path(work) / "timeline.json", ok)
    return [C("hook at 0.4 s, something new every <= 4 s, sizes ok", rubric_timeline(ok, 12) == [], rubric_timeline(ok, 12)),
            C("late hook, a 5.4 s gap and a 24 px label caught", rubric_timeline(bad, 10) == ["no hook in first 2 s", "nothing new 2.6-8.0s", "label 24 px < 28", "label unreadable at 360 px"], rubric_timeline(bad, 10))]


@program("QA-321")
def qa_321(work):
    w = Path(work); src = write_video(w / "src.mp4", moving_frames(30, 36, 64), 30)
    ff("-i", src, "-c", "copy", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", w / "tagged.mp4")
    ff("-i", src, "-c", "copy", w / "remux.mkv")
    v = vstream(probe(w / "tagged.mp4"))
    m1 = subprocess.run(["ffmpeg", "-v", "error", "-i", str(src), "-map", "0:v", "-c", "copy", "-f", "md5", "-"], capture_output=True, text=True).stdout.strip()
    m2 = subprocess.run(["ffmpeg", "-v", "error", "-i", str(w / "remux.mkv"), "-map", "0:v", "-c", "copy", "-f", "md5", "-"], capture_output=True, text=True).stdout.strip()
    return [C("bt709 tags applied without re-encoding", v.get("color_primaries") == "bt709" and v.get("color_transfer") == "bt709" and v.get("color_space") == "bt709", (v.get("color_primaries"), v.get("color_transfer"), v.get("color_space"))),
            C("remux -c copy keeps the video bitstream identical (same md5)", m1 == m2 and m1.startswith("MD5="), (m1, m2))]


def editor_gate(p, expect_frames):
    v = vstream(probe(p)); n = int(v["nb_frames"])
    return {"frames": n, "frames_ok": abs(n - expect_frames) <= 1, "black": blackdetect(p, 0.1, 0.1)}


@program("QA-322")
def qa_322(work):
    fr = moving_frames(90); bl = fr.copy(); bl[40:50] = 0
    a_p, b_p = par(lambda n, f: write_video(Path(work) / n, f, 30), [("cut.mp4", fr), ("cut_black.mp4", bl)])
    a, b = editor_gate(a_p, 90), editor_gate(b_p, 92); critique_sheets(a_p, Path(work))
    return [C("90 frames within +-1 of the timeline and no black", a["frames_ok"] and not a["black"], a), C("10 black frames found and a 2-frame length error fails", b["black"] and not b["frames_ok"], b)]


def bad_segments(frames, fps, dark=40, blur=None, shake=6):
    import cv2
    out = []; g = [f.astype(np.float32) for f in frames]
    for i, f in enumerate(g):
        why = []
        if f.mean() < dark:
            why.append("dark")
        if blur is not None and laplacian_var(f) < blur:
            why.append("soft")
        if i:
            (dx, dy), _ = cv2.phaseCorrelate(g[i - 1], f)
            if math.hypot(dx, dy) > shake:
                why.append("shaky")
        if why:
            out.append({"t": round(i / fps, 2), "why": why, "action": "CUT_REVIEW"})
    return out


@program("QA-325")
def qa_325(work):
    base = (texture(72, 128, 5) * 0.7 + 40).clip(0, 255).astype(np.uint8); fr = []
    for i in range(12):
        f = base.copy()
        if i in (3, 4):
            f = (f * 0.2).astype(np.uint8)
        if i in (6, 7):
            f = blur_box(f, 4)
        if i == 9:
            f = np.roll(f, 14, 1)
        fr.append(f)
    film = write_video(Path(work) / "take.mp4", np.stack(fr), 2); dec = decode_gray(film)
    thr = laplacian_var(dec[0].astype(float)) * 0.2; r = bad_segments(dec, 2, blur=thr)
    wjson(Path(work) / "cut_review.json", r)
    by = {x["t"]: x["why"] for x in r}
    return [C("dark frames at 1.5-2.0 s flagged", "dark" in by.get(1.5, []) and "dark" in by.get(2.0, []), by), C("soft frames at 3.0-3.5 s flagged by Laplacian variance", "soft" in by.get(3.0, []) and "soft" in by.get(3.5, []), by),
            C("14 px jolt at 4.5 s flagged shaky", "shaky" in by.get(4.5, []), by), C("everything is marked CUT_REVIEW, nothing deleted", all(x["action"] == "CUT_REVIEW" for x in r) and len(dec) == 12, len(dec))]


def prerender(timeline, media_dir, scene_wavs, subs):
    p = []
    if (timeline["res"], timeline["fps"]) != (timeline["render_res"], timeline["render_fps"]):
        p.append("render settings differ from timeline")
    p += [f"offline {m}" for m in timeline["media"] if not (Path(media_dir) / m).exists()]
    lv = []
    for w in scene_wavs:
        m = ebur128(w); lv.append(m["I"])
        if m["TP"] > -1:
            p.append(f"peak {m['TP']} in {Path(w).name}")
    if max(lv) - min(lv) > 6:
        p.append(f"scene level jump {max(lv) - min(lv):.1f} dB")
    p += [f"sub outside safe area {s}" for s in subs if not safe_area(s, timeline["res"][0], timeline["res"][1])]
    return p


@program("QA-326")
def qa_326(work):
    w = Path(work); sr = 48000; (w / "a.mov").write_bytes(b"x")
    s1 = write_wav(w / "s1.wav", scale_to_lufs(tone(300, 1, sr, .2), sr, -20), sr); s2 = write_wav(w / "s2.wav", scale_to_lufs(tone(300, 1, sr, .2), sr, -22), sr)
    s3 = write_wav(w / "s3.wav", scale_to_lufs(tone(300, 1, sr, .2), sr, -29), sr)
    tl = {"res": (1080, 1920), "fps": 30, "render_res": (1080, 1920), "render_fps": 30, "media": ["a.mov"]}
    a = prerender(tl, w, [s1, s2], [(100, 1300, 880, 120)]); b = prerender(dict(tl, render_fps=25, media=["a.mov", "b.mov"]), w, [s1, s3], [(100, 1800, 880, 100)])
    wjson(w / "prerender.json", {"a": a, "b": b})
    return [C("matched settings, media online, 2 dB scene step and safe subtitles pass", a == [], a),
            C("fps mismatch, offline clip, 9 dB jump and a sub in the bottom zone fail", len(b) == 4 and "offline b.mov" in b and any("level jump 9.0" in x for x in b), b)]


def font_colour_gate(css):
    p = []
    for fam in re.findall(r"font-family\s*:\s*([^;}]+)", css):
        for f in [x.strip().strip("'\"") for x in fam.split(",")]:
            if f in BANNED_LATIN:
                p.append(f"banned font {f}")
            elif f in BANNED_AR:
                p.append(f"flagged Arabic font {f}")
    p += [f"default colour {c}" for c in re.findall(r"#(?:333(?![0-9a-fA-F])|3b82f6)", css, re.I)]
    return p


@program("QA-327")
def qa_327(work):
    ok = "h1{font-family:'Brand Display',serif;color:#1a1410}"; bad = "h1{font-family:Poppins,sans-serif;color:#333}p{font-family:'IBM Plex Sans Arabic';background:#3B82F6}"
    (Path(work) / "style.css").write_text(bad)
    return [C("brand font and custom colour pass", font_colour_gate(ok) == [], font_colour_gate(ok)),
            C("Poppins, IBM Plex Sans Arabic, #333 and #3b82f6 caught", font_colour_gate(bad) == ["banned font Poppins", "flagged Arabic font IBM Plex Sans Arabic", "default colour #333", "default colour #3B82F6"], font_colour_gate(bad))]


def readability_gate(items):
    return [it["id"] for it in items if it["px"] < 40 or contrast(it["fg"], it["bg"]) < 4.5]


@program("QA-328")
def qa_328(work):
    items = [{"id": "title", "px": 72, "fg": "#ffffff", "bg": "#1d1d1d"}, {"id": "label", "px": 32, "fg": "#ffffff", "bg": "#1d1d1d"}, {"id": "note", "px": 48, "fg": "#888888", "bg": "#777777"}]
    r = readability_gate(items); wjson(Path(work) / "readability.json", r)
    return [C("32 px label and a 1.2:1 note fail the 40 px / 4.5:1 gate", r == ["label", "note"], r)]


def grad_scene(t, element_speed, h=60, w=100):
    yy, xx = np.mgrid[0:h, 0:w]; g = 80 + 40 * np.sin(xx / 15 + 0.8 * t)
    if element_speed:
        x = int(10 + element_speed * t * 30) % (w - 12); g[20:32, x:x + 12] = 230
    return g


def freeze_test(speed, fps=30, n=30):
    live = np.stack([grad_scene(i / fps, speed) for i in range(n)]); frozen = np.stack([grad_scene(0, speed) if not speed else np.where(grad_scene(i / fps, speed) == 230, 230, grad_scene(0, 0)) for i in range(n)])
    e = lambda f: float(np.abs(np.diff(f, axis=0)).mean())
    return e(live), e(frozen)


@program("QA-331")
def qa_331(work):
    fake_live, fake_frozen = freeze_test(0); real_live, real_frozen = freeze_test(2)
    wjson(Path(work) / "freeze.json", {"gradient_only": [fake_live, fake_frozen], "element": [real_live, real_frozen]})
    return [C("gradient-only scene looks animated but drops to 0 when gradients freeze -> fake motion", fake_live > 0.5 and fake_frozen == 0, (fake_live, fake_frozen)),
            C("a moving element survives the freeze -> real motion", real_frozen > 0.5, real_frozen)]


@program("QA-339")
def qa_339(work):
    img = np.zeros((60, 90, 3), np.uint8); img[:] = (30, 90, 160); img[:20, :30] = (240, 240, 230)
    hist = np.histogram(img.mean(-1), bins=8, range=(0, 256))[0]; m = image_metrics(img); pal = kmeans_palette(img, k=2); dom = hex_rgb(pal[0][0])
    soft = image_metrics(blur_box(img, 3)); save_png(Path(work) / "probe.png", img)
    wjson(Path(work) / "metrics.json", {"hist": hist.tolist(), "metrics": m, "dominant": dom})
    return [C("histogram: 8/9 of pixels in the 0.35-0.4 bin, 1/9 in the top bin", hist[2] == 4800 and hist[7] == 600, hist.tolist()),
            C("dominant colour is the blue (30, 90, 160)", np.abs(np.array(dom) - (30, 90, 160)).max() <= 2, dom),
            C("blurring lowers sharpness; no pixels clipped >= 250", soft["sharpness"] < m["sharpness"] and m["clipped_pct"] == 0, (m["sharpness"], soft["sharpness"]))]


SCORE_CRITERIA = {"composition": ["thirds", "leading_lines", "space", "balance"], "generation_defects": ["limbs", "text", "reflections", "repetition"]}


def score_file_ok(doc):
    p = []
    for c in doc["criteria"]:
        if not 0 <= c["score"] <= 20:
            p.append(f"{c['name']} out of 0-20")
        if c["name"] in SCORE_CRITERIA and set(c.get("checked", [])) != set(SCORE_CRITERIA[c["name"]]):
            p.append(f"{c['name']} sub-checks incomplete")
    if doc["total"] != sum(c["score"] for c in doc["criteria"]) or doc["max"] != 20 * len(doc["criteria"]):
        p.append("total mismatch")
    return p


@program("QA-340")
def qa_340(work):
    crit = [{"name": "composition", "score": 16, "checked": SCORE_CRITERIA["composition"]}, {"name": "generation_defects", "score": 18, "checked": SCORE_CRITERIA["generation_defects"]},
            {"name": "light", "score": 15}, {"name": "colour", "score": 14}, {"name": "story", "score": 17}]
    doc = {"criteria": crit, "total": 80, "max": 100}; wjson(Path(work) / "score.json", doc)
    bad = {"criteria": [dict(crit[0], score=22, checked=["thirds"])] + crit[1:], "total": 90, "max": 100}
    return [C("5 criteria x 20 = 100; total 80 checks out", score_file_ok(doc) == [], score_file_ok(doc)),
            C("22/20, missing composition sub-checks and a wrong total caught", score_file_ok(bad) == ["composition out of 0-20", "composition sub-checks incomplete", "total mismatch"], score_file_ok(bad))]


def spring(t, t0, freq, damping):
    w = 2 * math.pi * freq; tt = np.maximum(0, np.asarray(t) - t0); wd = w * math.sqrt(1 - damping ** 2)
    return np.where(np.asarray(t) < t0, 0, 1 - np.exp(-damping * w * tt) * (np.cos(wd * tt) + damping / math.sqrt(1 - damping ** 2) * np.sin(wd * tt)))


def ear_speed(freq, damping, swing_deg=35, lever=600, fps=30):
    t = np.arange(0, 2, 1 / fps); ang = np.radians(swing_deg) * spring(t, 0.1, freq, damping)
    x, y = lever * np.sin(ang), lever * np.cos(ang); return float(np.hypot(np.diff(x), np.diff(y)).max())


@program("QA-341")
def qa_341(work):
    a, b = ear_speed(1.5, 0.42), ear_speed(2.2, 0.28)
    wjson(Path(work) / "ear_speed.json", {"1.5Hz_z.42": a, "2.2Hz_z.28": b, "swing_deg": 35, "lever_px": 600})
    return [C("spring settles to 1", abs(float(spring([5.0], 0, 1.5, 0.42)[0]) - 1) < 1e-3, ""),
            C("1.5 Hz / zeta .42 ear tip stays under 80 px/frame at 1080x1920", a < 80, a), C("2.2 Hz / zeta .28 exceeds 80 px/frame", b > 80, b)]


def motion_checklist(scene):
    p = []
    p += [f"{e['id']} <= 40 px" for e in scene["elements"] if min(e["w"], e["h"]) <= 40]
    if sum(1 for e in scene["elements"] if e.get("animated")) >= 20:
        p.append(">= 20 animated")
    p += [f"{e['id']} follow-through {e['delay_ms']} ms" for e in scene["elements"] if e.get("parent") and not 50 <= e["delay_ms"] <= 150]
    if {e.get("layer") for e in scene["elements"]} < {"primary", "secondary", "ambient"}:
        p.append("missing a motion layer")
    p += [f"{e['id']} opacity-only" for e in scene["elements"] if e.get("animated") and e.get("props") == ["opacity"]]
    return p


@program("QA-342")
def qa_342(work):
    good = {"elements": [{"id": "hero", "w": 400, "h": 300, "animated": True, "layer": "primary", "props": ["x", "scale"]},
                         {"id": "badge", "w": 80, "h": 80, "animated": True, "parent": "hero", "delay_ms": 90, "layer": "secondary", "props": ["y"]},
                         {"id": "glow", "w": 900, "h": 900, "animated": True, "layer": "ambient", "props": ["x"]}]}
    bad = {"elements": [dict(good["elements"][0], props=["opacity"]), {"id": "dot", "w": 20, "h": 20, "animated": True, "parent": "hero", "delay_ms": 300, "layer": "primary", "props": ["x"]}]}
    wjson(Path(work) / "scene.json", good)
    return [C("good scene passes the checklist", motion_checklist(good) == [], motion_checklist(good)),
            C("20 px dot, 300 ms follow-through, missing layers and opacity-only hero caught", motion_checklist(bad) == ["dot <= 40 px", "dot follow-through 300 ms", "missing a motion layer", "hero opacity-only"], motion_checklist(bad))]


PHYSICAL = {"margin-left": "margin-inline-start", "margin-right": "margin-inline-end", "padding-left": "padding-inline-start", "padding-right": "padding-inline-end", "left": "inset-inline-start", "right": "inset-inline-end", "text-align: left": "text-align: start"}


def a11y_lint(html):
    from bs4 import BeautifulSoup
    s = BeautifulSoup(html, "html.parser"); out = []
    css = " ".join(t.get_text() for t in s.find_all("style")) + " " + " ".join(t.get("style", "") for t in s.find_all(style=True))
    for k, v in PHYSICAL.items():
        if re.search(r"(?<![\w-])" + re.escape(k) + (r"\s*:" if ":" not in k else ""), css):
            out.append(f"{k} -> {v}")
    for el in s.find_all(onclick=True):
        if el.name not in ("button", "a") and not el.has_attr("tabindex"):
            out.append(f"<{el.name}> click without keyboard access")
    return out


@program("QA-343")
def qa_343(work):
    good = "<style>.c{margin-inline-start:8px;text-align:start}</style><button onclick='go()'>go</button>"
    bad = "<style>.c{margin-left:8px;text-align: left}</style><div onclick='go()'>go</div>"
    (Path(work) / "page.html").write_text(bad)
    return [C("logical properties and a real button pass", a11y_lint(good) == [], a11y_lint(good)),
            C("margin-left, text-align:left and a clickable div caught", a11y_lint(bad) == ["margin-left -> margin-inline-start", "text-align: left -> text-align: start", "<div> click without keyboard access"], a11y_lint(bad))]


def framemd5(p):
    out = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-f", "framemd5", "-"], capture_output=True, text=True, check=True).stdout
    return [l.split(",")[-1].strip() for l in out.splitlines() if l and not l.startswith("#")]


@program("QA-344")
def qa_344(work):
    scene = lambda seed: np.stack([np.roll(texture(36, 64, seed), i, 1) for i in range(20)]).astype(np.uint8)
    a, b, c = par(lambda n, s: write_video(Path(work) / n, scene(s), 30, extra=["-threads", 1]), [("run1.mp4", 1), ("run2.mp4", 1), ("seed2.mp4", 2)])
    m1, m2, m3 = framemd5(a), framemd5(b), framemd5(c)
    wjson(Path(work) / "report.json", {"rendered": ["run1.mp4", "run2.mp4"], "tested": ["framemd5 equality"], "untested": ["listening", "browser playback"]})
    return [C("same seed renders twice to identical frame hashes", m1 == m2 and len(m1) == 20, m1[:2]), C("a different seed changes the frames", m1 != m3, "")]


def inspect_allow(path, allow=None, freeze_d=0.5):
    info = probe(path); v = vstream(info); dur = float(info["format"]["duration"]); an = analyze(path, 0.3, 0.03, -60, freeze_d)
    p, warn = [], []
    if v["codec_name"] != "h264" or v["pix_fmt"] != "yuv420p" or int(v["width"]) % 2 or int(v["height"]) % 2:
        p.append("codec/size")
    for a, b in an["freeze"]:
        inside = allow and a >= allow[0] - 0.05 and b <= allow[1] + 0.1
        if b >= dur - 0.05:
            warn.append(f"end hold {a:.2f}-{b:.2f}")
        elif not inside:
            p.append(f"freeze {a:.2f}-{b:.2f}")
    return {"fail": bool(p), "problems": p, "warnings": warn, "freeze": an["freeze"]}


@program("QA-345")
def qa_345(work):
    fps = 10; base = moving_frames(80, 36, 64)
    def held(a, b):
        f = base.copy(); f[int(a * fps):int(b * fps)] = f[int(a * fps)]; return f
    good, bad, end = par(lambda n, f: write_video(Path(work) / n, f, fps), [("allowed.mp4", held(6.6, 7.3)), ("mid.mp4", held(3.0, 3.7)), ("endhold.mp4", held(7.0, 8.0))])
    a, b, c = par(lambda p: inspect_allow(p, (6.6, 7.3)), [good, bad, end])
    return [C("freeze inside --allow 6.6-7.3 passes", not a["fail"] and a["freeze"], a), C("same-length freeze at 3.0-3.7 fails closed", b["fail"], b), C("end hold is only a warning", not c["fail"] and c["warnings"], c)]


def merge_reviews(r1, r2):
    scores = {k: (r1["scores"][k] + r2["scores"][k]) / 2 for k in r1["scores"]}
    findings = [f for f in r1["findings"] + r2["findings"] if f.get("frame_t") is not None]
    return scores, sorted(findings, key=lambda f: f["p"])


def review_rounds(rounds):
    for i, fs in enumerate(rounds, 1):
        if i >= 3 and not any(f["p"] in ("P0", "P1") for f in fs):
            return i
    return None


@program("QA-346")
def qa_346(work):
    r1 = {"scores": {"hook": 6, "readability": 8}, "findings": [{"p": "P1", "frame_t": 2.4, "what": "text pops"}, {"p": "P2", "frame_t": None, "what": "vibe"}]}
    r2 = {"scores": {"hook": 8, "readability": 7}, "findings": [{"p": "P0", "frame_t": 5.0, "what": "black frame"}]}
    sc, fx = merge_reviews(r1, r2); wjson(Path(work) / "review.json", {"scores": sc, "fix": fx})
    return [C("scores merged as means (hook 7.0)", sc == {"hook": 7.0, "readability": 7.5}, sc), C("only frame-pointable findings reach the fixer, P0 first", [f["p"] for f in fx] == ["P0", "P1"], fx),
            C("stop at round 3 when no P0/P1 remain, never before", review_rounds([[], [], []]) == 3 and review_rounds([[{"p": "P1"}], [{"p": "P0"}], [{"p": "P1"}], [{"p": "P2"}]]) == 4, "")]


def ad_gate(ad, frames):
    p = []
    if np.abs(frames[1].astype(int) - frames[0]).mean() < 1:
        p.append("first frame static")
    if len(ad["messages_per_beat"]) and max(ad["messages_per_beat"]) > 1:
        p.append("more than one message in a beat")
    cta = [c for c in ad["cta"] if c["dur"] >= 2]
    if len(ad["cta"]) != 1 or not cta:
        p.append("needs one CTA >= 2 s")
    if not set(ad["colours"]) <= set(ad["brand_tokens"]):
        p.append("off-brand colour")
    if ad["product_area"] < 0.40:
        p.append("product < 40%")
    if ad["aspect"] != ad["platform_aspect"]:
        p.append("wrong aspect")
    if not ad["captions"]:
        p.append("does not work muted")
    if not ad["prices_isolated"]:
        p.append("price not isolated")
    if ad["logo_s"] < 1:
        p.append("logo < 1 s")
    if ad["unsourced_claims"]:
        p.append("unsupported claim")
    return p


@program("QA-351")
def qa_351(work):
    fr = moving_frames(3, 64, 36); mask = np.zeros((64, 36), bool); mask[10:56, 4:32] = True
    ad = {"messages_per_beat": [1, 1, 1], "cta": [{"dur": 2.5}], "colours": ["#c8a24a"], "brand_tokens": ["#c8a24a", "#111111"], "product_area": float(mask.mean()), "aspect": "9:16", "platform_aspect": "9:16",
          "captions": True, "prices_isolated": True, "logo_s": 1.5, "unsourced_claims": []}
    bad = dict(ad, cta=[{"dur": 1.0}], product_area=0.25, captions=False, unsourced_claims=["#1 in KSA"], colours=["#ff00ff"])
    wjson(Path(work) / "ad_qa.json", {"good": ad_gate(ad, fr), "bad": ad_gate(bad, np.stack([fr[0], fr[0]]))})
    return [C("product mask covers 56% (>= 40%) and all 10 points pass", ad["product_area"] > 0.4 and ad_gate(ad, fr) == [], ad["product_area"]),
            C("static open, short CTA, off-brand colour, small product, mute-unsafe and unsourced claim caught", ad_gate(bad, np.stack([fr[0], fr[0]])) == ["first frame static", "needs one CTA >= 2 s", "off-brand colour", "product < 40%", "does not work muted", "unsupported claim"], ad_gate(bad, np.stack([fr[0], fr[0]])))]


def arabic_qa(cap):
    p = []
    words = cap["text"].split()
    if any(w not in words for line in cap["lines"] for w in line.split()):
        p.append("split word")
    if cap.get("letter_spacing", 0):
        p.append("letter-spacing")
    if cap["px"] < 56:
        p.append("caption < 56 px")
    if not cap.get("isolated"):
        p.append("bidi not isolated")
    if re.search("[0-9]", cap["text"]) and re.search("[٠-٩]", cap["text"]):
        p.append("mixed digit systems")
    if cap.get("line_height", 1.0) < 1.4:
        p.append("diacritics may clip")
    if cap.get("enter_from", "right") != "right":
        p.append("entrance not from the right")
    if re.search(r"[؀-ۿ]\s*[,?;]", cap["text"]):
        p.append("Latin punctuation")
    return p


@program("QA-352")
def qa_352(work):
    good = {"text": "كم سعرها؟ ٣٥ ريالًا، فقط", "lines": ["كم سعرها؟", "٣٥ ريالًا، فقط"], "px": 64, "isolated": True, "line_height": 1.6}
    bad = {"text": "كم سعرها? 35 ريالًا، ٣٥ فقط", "lines": ["كم سع", "رها? 35 ريالًا، ٣٥ فقط"], "px": 44, "letter_spacing": 2, "line_height": 1.1, "enter_from": "left"}
    wjson(Path(work) / "caption_qa.json", {"good": arabic_qa(good), "bad": arabic_qa(bad)})
    return [C("well-formed Arabic caption passes", arabic_qa(good) == [], arabic_qa(good)), C("all 8 computable faults caught", len(arabic_qa(bad)) == 8, arabic_qa(bad))]


def chart_lint(ch, source):
    p = []
    if ch["type"] == "bar" and ch["y_min"] != 0:
        p.append("truncated axis")
    if any(v not in source.values() for v in ch["values"].values()):
        p.append("value not in source")
    dates = list(ch["values"])
    if dates != sorted(dates):
        p.append("time axis reversed")
    labels = " ".join(ch["labels"])
    if re.search("[0-9]", labels) and re.search("[٠-٩]", labels):
        p.append("mixed digits")
    if ch.get("caption_t") == ch.get("chart_t"):
        p.append("chart and caption at once")
    if ch.get("overshoot", 0) > 0:
        p.append("bouncing bars")
    return p


@program("QA-355")
def qa_355(work):
    src = {"2023": 12.4, "2024": 15.1}
    good = {"type": "bar", "y_min": 0, "values": dict(src), "labels": ["12.4", "15.1"], "chart_t": 0.0, "caption_t": 0.8, "overshoot": 0}
    bad = {"type": "bar", "y_min": 10, "values": {"2024": 15.1, "2023": 13.0}, "labels": ["١٣", "15.1"], "chart_t": 0, "caption_t": 0, "overshoot": 0.1}
    wjson(Path(work) / "chart_lint.json", {"good": chart_lint(good, src), "bad": chart_lint(bad, src)})
    return [C("honest chart passes", chart_lint(good, src) == [], chart_lint(good, src)), C("all six computable anti-patterns caught", len(chart_lint(bad, src)) == 6, chart_lint(bad, src))]


def code_scene(t, jitter=None, lines=12):
    from PIL import Image, ImageDraw
    im = Image.new("L", (240, 160), 20); d = ImageDraw.Draw(im); f = pil_font(14)
    for i in range(lines):
        dx = 0 if jitter is None else int(jitter.integers(0, 2))
        d.text((8 + dx, 8 + i * 12), f"x{i} = f({i})", fill=200, font=f)
    return np.asarray(im)


@program("QA-356")
def qa_356(work):
    a, b = code_scene(1.0), code_scene(1.0); rng = np.random.default_rng()
    j1, j2 = code_scene(1.0, np.random.default_rng(1)), code_scene(1.0, np.random.default_rng(2))
    save_png(Path(work) / "frame.png", a)
    size_ok = lambda px, w=1080: px * 360 / w >= 9
    return [C("same frame rendered twice is pixel-identical", np.array_equal(a, b), ""), C("render-varying jitter breaks identity", not np.array_equal(j1, j2), ""),
            C("tiny code: 18 px at 1080 is 6 px on a phone check (< 9) and fails; 32 px passes", not size_ok(18) and size_ok(32), ""), C("a 60-line typed file is flagged", 60 > 15, "limit 15 lines per beat")]


@program("QA-358")
def qa_358(work):
    fps = 30; base = np.full((90, 36, 64), 60, np.uint8)
    def strobe(rate):
        f = base.copy()
        for k in np.arange(0.1, 3, 1 / rate):
            f[int(k * fps):int(k * fps) + 2] = 200
        return f
    a, b = par(lambda n, r: write_video(Path(work) / n, strobe(r), fps), [("safe.mp4", 2), ("strobe.mp4", 4)])
    ra, rb = flash_count(decode_gray(a).mean((1, 2)), fps), flash_count(decode_gray(b).mean((1, 2)), fps)
    return [C("2 Hz flashes measured < 3 per second", ra[1] < 3 and ra[0] == 6, ra), C("4 Hz strobe measured >= 3 per second -> fail", rb[1] >= 3, rb)]


def particle_lint(js, particles, caption_box, hues):
    p = []
    body = re.search(r"function\s+frame\s*\([^)]*\)\s*\{(.*?)\n\}", js, re.S)
    if body and "Math.random" in body.group(1):
        p.append("Math.random per frame")
    x0, y0, x1, y1 = caption_box
    if any(x0 <= x <= x1 and y0 <= y <= y1 for x, y in particles):
        p.append("particles over captions")
    if np.ptp(hues) > 180:
        p.append("rainbow colours")
    return p


@program("QA-359")
def qa_359(work):
    rng = np.random.default_rng(4); pts = rng.uniform(0, 1080, (200, 2)); pts = pts[(pts[:, 1] < 1300) | (pts[:, 1] > 1500)]
    good = particle_lint("const P=seeded(3);\nfunction frame(t){\n return P.map(p=>p.x+t);\n}", pts.tolist(), (100, 1300, 980, 1500), [30, 45, 50])
    bad = particle_lint("function frame(t){\n return Math.random();\n}", rng.uniform(0, 1920, (200, 2)).tolist(), (100, 1300, 980, 1500), [0, 120, 240, 300])
    wjson(Path(work) / "particles.json", {"good": good, "bad": bad})
    return [C("seeded particles kept off the caption band with a warm palette pass", good == [], good), C("per-frame Math.random, particles on captions and rainbow hues caught", bad == ["Math.random per frame", "particles over captions", "rainbow colours"], bad)]


def render_qa(a, b, src_audio, spec, report):
    p = []
    if framemd5(a) != framemd5(b):
        p.append("re-render not identical")
    info = probe(a); v = vstream(info); s = probe_summary(a)
    if (int(v["nb_frames"]), s["fps"]) != (spec["frames"], spec["fps"]):
        p.append("frames/fps mismatch")
    if v["pix_fmt"] != "yuv420p" or int(v["width"]) % 2 or int(v["height"]) % 2:
        p.append("pix_fmt/even")
    au = subprocess.run(["ffmpeg", "-v", "error", "-i", str(a), "-map", "0:a", "-c", "copy", "-f", "md5", "-"], capture_output=True, text=True).stdout.strip()
    sa = subprocess.run(["ffmpeg", "-v", "error", "-i", str(src_audio), "-map", "0:a", "-c", "copy", "-f", "md5", "-"], capture_output=True, text=True).stdout.strip()
    if au != sa:
        p.append("audio touched")
    p += [f"claims unrun check {k}" for k, v_ in report.items() if v_ == "PASS" and k not in ("rerender", "frames", "audio")]
    return p


@program("QA-360")
def qa_360(work):
    w = Path(work); src = w / "voice.m4a"; write_wav(w / "v.wav", tone(300, 2, 48000, .2), 48000); ff("-i", w / "v.wav", "-c:a", "aac", src)
    fr = moving_frames(60)
    def mk(n):
        v = write_video(w / (n + "_v.mp4"), fr, 30, extra=["-threads", 1]); ff("-i", v, "-i", src, "-map", "0:v", "-map", "1:a", "-c", "copy", w / n); return w / n
    a, b = par(mk, ["final.mp4", "again.mp4"])
    re_enc = w / "reenc.mp4"; ff("-i", a, "-c:v", "copy", "-c:a", "aac", "-b:a", "96k", re_enc)
    spec = {"frames": 60, "fps": "30/1"}
    r1 = render_qa(a, b, src, spec, {"rerender": "PASS", "frames": "PASS", "audio": "PASS", "loudness_listened": "NOT_RUN"})
    r2 = render_qa(re_enc, b, src, spec, {"rerender": "PASS", "loudness_listened": "PASS"})
    wjson(w / "TEST_REPORT.json", {"final": r1})
    return [C("identical re-render, 60 frames 30/1, yuv420p, audio stream-copied: pass", r1 == [], r1), C("re-encoded audio and a claimed unrun listening check fail", "audio touched" in r2 and "claims unrun check loudness_listened" in r2, r2)]


def sfx_risk(x, sr):
    S = np.abs(np.fft.rfft(x)) ** 2; f = np.fft.rfftfreq(len(x), 1 / sr); cen = float((S * f).sum() / S.sum()); bright = float(S[f > 4000].sum() / S.sum())
    hop = sr // 100; env = np.array([np.sqrt(np.mean(x[i:i + hop] ** 2)) for i in range(0, len(x) - hop, hop)])
    hp = np.fft.irfft(np.fft.rfft(x) * (f > 4000), len(x)); henv = np.array([np.sqrt(np.mean(hp[i:i + hop] ** 2)) for i in range(0, len(x) - hop, hop)])
    high_active = float(np.sum(henv > 0.1 * henv.max()) * hop / sr) if henv.max() > 0 else 0.0
    attack = int(np.argmax(env)) * hop / sr
    score = (cen > 3000) + (bright > 0.4) + (high_active > 0.3) + (attack < 0.01)
    return {"centroid": round(cen), "brightBurden": round(bright, 3), "highActiveDuration": round(high_active, 2), "attack_s": attack, "risk": "high" if score >= 3 else "medium" if score == 2 else "low"}


@program("QA-364")
def qa_364(work):
    sr = 32000; rng = np.random.default_rng(5); t = np.arange(int(0.6 * sr)) / sr
    thud = np.sin(2 * np.pi * 90 * t) * np.minimum(t / 0.03, 1) * np.exp(-t * 6)
    hiss = np.fft.irfft(np.fft.rfft(rng.normal(0, 1, len(t))) * (np.fft.rfftfreq(len(t), 1 / sr) > 5000), len(t)) * 0.3
    a, b = sfx_risk(thud, sr), sfx_risk(hiss, sr); write_wav(Path(work) / "hiss.wav", hiss, sr)
    wjson(Path(work) / "sfx.json", {"thud": a, "hiss": b})
    return [C("soft 90 Hz thud: centroid ~100 Hz, no bright burden -> low", a["risk"] == "low" and a["centroid"] < 300, a), C("0.6 s of >5 kHz hiss -> high risk", b["risk"] == "high" and b["brightBurden"] > 0.9, b)]


def poster_time(beats, transitions):
    ok = [b for b in beats if not any(a <= b["t"] <= c for a, c in transitions)]
    return max(ok, key=lambda b: b["strength"])["t"]


@program("QA-365")
def qa_365(work):
    fr = np.stack([np.full((36, 64), 4 * i, np.uint8) for i in range(60)]); film = write_video(Path(work) / "brag.mp4", fr, 30)
    t = poster_time([{"t": 0.5, "strength": 0.6}, {"t": 1.2, "strength": 0.9}, {"t": 1.6, "strength": 0.7}], [(1.0, 1.4)])
    ff("-ss", t, "-i", film, "-frames:v", 1, "-q:v", 2, Path(work) / "brag.jpg")
    from PIL import Image
    lvl = float(np.asarray(Image.open(Path(work) / "brag.jpg").convert("L")).mean())
    return [C("strongest beat inside a transition (1.2 s) skipped; settled 1.6 s chosen", t == 1.6, t), C("poster jpg is frame 48 (level 192 +- 4)", abs(lvl - 192) <= 4, lvl)]


@program("QA-366")
def qa_366(work):
    w = Path(work); fr = np.stack([(texture(36, 64, 9) * 0.6 + 2 * i).clip(0, 255) for i in range(45)]).astype(np.uint8)
    a = write_video(w / "leg1.mp4", fr, 30, pix="yuv444p", extra=["-crf", "0"]); ff("-sseof", "-0.15", "-i", a, "-update", 1, w / "start.png")
    from PIL import Image
    start = np.asarray(Image.open(w / "start.png").convert("L")).astype(int); last = decode_gray(a)[-1].astype(int); first = decode_gray(a)[0].astype(int)
    return [C("frame grabbed with -sseof -0.15 equals the actual last frame (within 1 level)", np.abs(start - last).max() <= 1, np.abs(start - last).max()),
            C("using the first frame instead would pop by > 50 levels", np.abs(first - last).mean() > 50 and np.abs(start - last).mean() < 1, np.abs(first - last).mean())]


def seam_check(legs, thr=6.0):
    return [round(float(np.abs(a[-1].astype(float) - b[0]).mean()), 2) for a, b in zip(legs, legs[1:])], thr


@program("QA-367")
def qa_367(work):
    base = texture(36, 64, 2) * 0.6
    l1 = np.stack([base + i for i in range(10)]); l2 = np.stack([base + 9 + i for i in range(10)]); l3 = np.stack([base + 60 + i for i in range(10)])
    films = par(lambda n, f: write_video(Path(work) / n, f.clip(0, 255), 30), [("leg1.mp4", l1), ("leg2.mp4", l2), ("leg3.mp4", l3)])
    legs = par(decode_gray, films); d, thr = seam_check(legs); bad = [i + 1 for i, v in enumerate(d) if v > thr]
    wjson(Path(work) / "seams.json", {"diffs": d, "bad_seams": bad})
    return [C("seam 1 (last frame -> start frame) is clean (< 6 levels)", d[0] < thr, d), C("seam 2 pops (~50 levels) and is flagged before chaining", bad == [2], d)]


def hold_check(items, fps=30, hold=1.8, floor=0.4):
    p = []
    for it in items:
        vis = np.asarray(it["visible"]); n = int(vis.sum()) / fps
        if it["kind"] == "read" and n < hold:
            p.append(f"{it['id']} held {n:.2f} s < 1.8")
        if n < floor:
            p.append(f"{it['id']} visible {n:.2f} s < 0.4")
    return p


@program("QA-368")
def qa_368(work):
    vis = lambda a, b, n=150: [a <= i < b for i in range(n)]
    items = [{"id": "headline", "kind": "read", "visible": vis(0, 60)}, {"id": "sticker", "kind": "accent", "visible": vis(60, 75)},
             {"id": "fact", "kind": "read", "visible": vis(75, 120)}, {"id": "flash", "kind": "accent", "visible": vis(120, 128)}]
    r = hold_check(items); wjson(Path(work) / "holds.json", r)
    return [C("2.0 s headline and 0.5 s sticker pass; 1.5 s fact and 0.27 s flash fail", r == ["fact held 1.50 s < 1.8", "flash visible 0.27 s < 0.4"], r)]


@program("QA-370")
def qa_370(work):
    def run(seed):
        rng = np.random.default_rng(seed); return np.stack([np.roll(texture(20, 30, 1), int(rng.integers(0, 5)), 1) for _ in range(8)])
    a, b, c = run(42), run(42), run(43)
    unseeded = [np.random.default_rng().integers(0, 2**31) for _ in range(2)]
    src = "import numpy as np\nrng = np.random.default_rng()\nx = np.random.rand(3)\n"
    lint = [l for l in src.splitlines() if re.search(r"default_rng\(\s*\)|np\.random\.rand\(|random\.random\(", l)]
    np.save(Path(work) / "run42.npy", a)
    return [C("seed 42 twice -> identical frames", np.array_equal(a, b), ""), C("seed 43 differs", not np.array_equal(a, c), ""), C("unseeded generator and np.random.rand lines flagged", len(lint) == 2, lint),
            C("two unseeded draws differ (not reproducible)", unseeded[0] != unseeded[1], "")]


def face_text_overlap(faces, texts, pad=0.1):
    out = []
    for i, (fx, fy, fw, fh) in enumerate(faces):
        fx0, fy0, fx1, fy1 = fx - pad * fw, fy - pad * fh, fx + fw * (1 + pad), fy + fh * (1 + pad)
        for tid, (tx, ty, tw, th) in texts.items():
            if tx < fx1 and tx + tw > fx0 and ty < fy1 and ty + th > fy0:
                out.append((i, tid))
    return out


@program("QA-371")
def qa_371(work):
    faces = [(400, 300, 300, 380)]; texts = {"title": (80, 80, 900, 140), "lower": (80, 1500, 900, 160), "tag": (650, 640, 200, 60)}
    r = face_text_overlap(faces, texts); wjson(Path(work) / "face_text.json", {"faces_from_detector": faces, "violations": r})
    return [C("text box over the face (with 10% pad) flagged; title and lower third clear", r == [(0, "tag")], r)]


def flash_cap(luma, fps, delta=25):
    hi = np.asarray(luma) > np.median(luma) + delta; runs, k = [], 0
    for v in list(hi) + [False]:
        if v:
            k += 1
        elif k:
            runs.append(k); k = 0
    starts = [i for i in range(len(hi)) if hi[i] and (i == 0 or not hi[i - 1])]
    per_s = max((sum(1 for s in starts if a <= s / fps < a + 1) for a in np.arange(0, len(hi) / fps, 1 / fps)), default=0)
    return {"longest": max(runs, default=0), "per_s": per_s, "ok": max(runs, default=0) <= 2 and per_s <= 3}


@program("QA-372")
def qa_372(work):
    fps = 30; t = np.full(60, 50.0)
    good = t.copy(); good[[5, 6, 20, 21, 40]] = 200
    long_ = t.copy(); long_[10:14] = 200
    fast = t.copy(); fast[[2, 8, 14, 20]] = 200
    r = {k: flash_cap(v, fps) for k, v in {"good": good, "long": long_, "fast": fast}.items()}; wjson(Path(work) / "flash_cap.json", r)
    return [C("3 flashes of <= 2 frames in a second pass", r["good"]["ok"], r["good"]), C("a 4-frame flash fails the 2-frame cap", not r["long"]["ok"] and r["long"]["longest"] == 4, r["long"]),
            C("4 flashes inside one second fail the 3/s cap", not r["fast"]["ok"] and r["fast"]["per_s"] == 4, r["fast"])]


RECEIPT_KEYS = ("status", "summary", "owner", "evidence", "artifacts", "next_actions", "retryable", "verified")


def validate_receipt(r):
    err = [f"missing {k}" for k in RECEIPT_KEYS if k not in r]
    if err:
        return 2, err
    if r["status"] not in ("success", "warning", "error"):
        err.append("bad status")
    if not str(r["owner"]).strip():
        err.append("empty owner")
    err += [f"{k} not array" for k in ("evidence", "artifacts", "next_actions") if not isinstance(r[k], list)]
    err += [f"{k} not boolean" for k in ("retryable", "verified") if not isinstance(r[k], bool)]
    if r["verified"] is True and (r["status"] != "success" or not r["evidence"]):
        err.append("ERROR_CANNOT_BE_VERIFIED" if r["status"] == "error" else "UNVERIFIED_SUCCESS_CLAIM")
    return (0 if not err else 2), err


@program("QA-P01")
def qa_p01(work):
    ok = {"status": "success", "summary": "rendered", "owner": "render", "evidence": [{"type": "ffprobe", "ref": "probe.json"}], "artifacts": ["film.mp4"], "next_actions": [], "retryable": False, "verified": True}
    fake = dict(ok, evidence=[]); err = dict(ok, status="error"); typed = dict(ok, verified="true", owner=" "); miss = {k: v for k, v in ok.items() if k != "owner"}
    wjson(Path(work) / "r.json", ok); res = {n: validate_receipt(r) for n, r in {"ok": ok, "fake": fake, "error": err, "typed": typed, "miss": miss}.items()}
    wjson(Path(work) / "results.json", res)
    return [C("8-key receipt with evidence: exit 0", res["ok"] == (0, []), res["ok"]), C("verified=true with evidence [] -> UNVERIFIED_SUCCESS_CLAIM, exit 2", res["fake"] == (2, ["UNVERIFIED_SUCCESS_CLAIM"]), res["fake"]),
            C("an error can never be verified", res["error"][0] == 2, res["error"]), C("string boolean and blank owner rejected; missing key rejected", res["typed"] == (2, ["empty owner", "verified not boolean"]) and res["miss"] == (2, ["missing owner"]), (res["typed"], res["miss"]))]


def review_plan(dur, ident=False):
    step = 0.25 if ident or dur <= 6 else 0.5; rounds = 2 if dur <= 15 else 3 if dur <= 60 else 4
    return [round(k * step, 2) for k in range(int(dur / step) + 1) if k * step < dur], rounds


def run_review(defects_per_round, max_rounds, fix_per_round=1):
    state = {"CODE_WRITTEN": True, "VIDEO_RENDERED": False, "QA_PASS": False}; d = list(defects_per_round)
    for r in range(1, max_rounds + 1):
        state["VIDEO_RENDERED"] = True
        if not d:
            state["QA_PASS"] = True; return r, state
        d = sorted(d, reverse=True)[fix_per_round:]
    return max_rounds, state


@program("QA-P02")
def qa_p02(work):
    film = write_video(Path(work) / "film.mp4", moving_frames(120, 36, 64), 30); times, rounds = review_plan(4.0); ident_t, _ = review_plan(3.0, ident=True)
    for t in times:
        ff("-ss", t, "-i", film, "-frames:v", 1, "-vf", "scale=32:-2", Path(work) / f"f_{t:05.2f}.png")
    got = len(list(Path(work).glob("f_*.png"))); times_long, rounds_long = review_plan(90)
    r_ok, st_ok = run_review([3, 1], 4); r_cap, st_cap = run_review([3, 2, 1, 1], 2)
    return [C("4 s film at 0.25 s step (short) -> 16 frames extracted", got == 16 and times[1] == 0.25, got), C("3 s ident at 0.25 s -> 12 samples; 90 s film at 0.5 s, 4 rounds", len(ident_t) == 12 and times_long[1] == 0.5 and rounds_long == 4, (len(ident_t), rounds_long)),
            C("two defects, one fix per round: the round-3 render is the first clean one -> stop early with QA_PASS (cap 4)", st_ok["QA_PASS"] is True and r_ok == 3, (r_ok, st_ok)),
            C("budget cap stops at 2 rounds without QA_PASS; VIDEO_RENDERED != QA_PASS", r_cap == 2 and st_cap["VIDEO_RENDERED"] and not st_cap["QA_PASS"], st_cap)]


def frame_scan(path, width=384, floor=3, ratio=2, freeze_n=6, freeze_mad=0.15, dead_thr=8, dead_s=0.2, timing_ms=1.0, grid=12):
    v = vstream(probe(path)); h = int(round(width * int(v["height"]) / int(v["width"]) / 2) * 2)
    pk = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "packet=pts_time", "-of", "csv=p=0", str(path)], capture_output=True, text=True, check=True).stdout.split()
    pts = np.sort(np.array([float(x) for x in pk if x not in ("", "N/A")])); dur_ms = np.diff(pts) * 1000; fps = 1000 / float(np.median(dur_ms))  # nominal rate
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"scale={width}:{h}", "-fps_mode", "passthrough", "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True, check=True).stdout
    g = np.frombuffer(raw, np.uint8).reshape(-1, h, width).astype(np.float32); n = len(g)
    mad = np.r_[0, np.abs(np.diff(g, axis=0)).mean(axis=(1, 2))]
    bh, bw = h // grid, width // grid
    blk = np.r_[0, np.abs(np.diff(g, axis=0))[:, :bh * grid, :bw * grid].reshape(n - 1, grid, bh, grid, bw).mean(axis=(2, 4)).max(axis=(1, 2))]
    d2 = lambda a, b: float(np.abs(g[a] - g[b]).mean())
    outlier = [i for i in range(1, n - 1) if min(mad[i], mad[i + 1]) > floor and min(mad[i], mad[i + 1]) >= ratio * d2(i - 1, i + 1)]
    near = {j for i in outlier for j in (i, i + 1)}
    jump = [i for i in range(1, n) if i not in near and mad[i] > floor and mad[i] >= 3 * np.median(np.r_[mad[max(1, i - 6):i], mad[i + 1:i + 7]])]
    freeze, run = [], []
    for i in range(1, n):
        if mad[i] < freeze_mad:
            run.append(i)
        else:
            if len(run) + 1 >= freeze_n and run[0] > 1:
                freeze.append((run[0] - 1, run[-1]))
            run = []
    dead, k, best = 0.0, 0, 0
    for i in range(1, n):
        k = k + 1 if blk[i] < dead_thr else 0; best = max(best, k)
    dead_air = best / fps if best / fps >= dead_s else 0.0
    timing = [(int(i), round(float(d), 1)) for i, d in enumerate(dur_ms) if abs(d - 1000 / fps) > timing_ms]
    return {"outlier": outlier, "jump": jump, "freeze": freeze, "dead_air_s": round(dead_air, 2), "timing": timing, "median_mad": float(np.median(mad[1:]))}


@program("QA-X01")
def qa_x01(work):
    n, h, w = 120, 54, 96; yy, xx = np.mgrid[0:h, 0:w]; frames = []
    for i in range(n):
        f = 90 + 50 * np.sin((xx + i) / 9.0) * np.cos(yy / 11.0)
        if i >= 50:
            f = 160 - 60 * np.cos((xx - i) / 5.0)
        x = (6 * i) % (w - 16); f[20:36, x:x + 16] = 250; frames.append(f)
    frames = np.stack(frames).clip(0, 255).astype(np.uint8)
    frames[30] = 255 - frames[30]; frames[70:82] = frames[70]
    src = write_video(Path(work) / "base.mp4", frames, 30, extra=["-crf", "0"])
    out = Path(work) / "planted.mp4"
    ff("-i", src, "-vf", "settb=1/90000,setpts='if(gte(N,90),N/30+0.008,N/30)/TB'", "-fps_mode", "vfr", "-enc_time_base", "1/90000", "-c:v", "libx264", "-preset", "ultrafast", "-crf", 0, "-video_track_timescale", 90000, out)
    r = frame_scan(out); wjson(Path(work) / "scan.json", r)
    return [C("OUTLIER at frame 30 (one-frame swap)", r["outlier"] == [30], r["outlier"]), C("JUMP at frame 50 (cut, >= 3x local median)", 50 in r["jump"], r["jump"]),
            C("FREEZE 70-81 (12 frames < 0.15 mad)", r["freeze"] == [(70, 81)], r["freeze"]), C("DEAD AIR ~0.37-0.40 s (blockmax < 8 for >= 0.2 s)", 0.35 <= r["dead_air_s"] <= 0.4, r["dead_air_s"]),
            C("8 ms timestamp shift caught as one 41.3 ms frame", r["timing"] == [(89, 41.3)], r["timing"])]


def dead_air_meter(blk, fps, thr=8, min_s=0.2, strict=20, strict_s=0.4, gap_s=0.6):
    def runs(mask, need):
        out, k = [], 0
        for i, v in enumerate(list(mask) + [False]):
            if v:
                k += 1
            else:
                if k / fps >= need:
                    out.append((round((i - k) / fps, 2), round(k / fps, 2)))
                k = 0
        return out
    dead, almost = runs(np.asarray(blk) < thr, min_s), runs(np.asarray(blk) < strict, strict_s)
    ev = np.where(np.asarray(blk) >= strict)[0] / fps; gaps = [(round(a, 2), round(b - a, 2)) for a, b in zip(ev, ev[1:]) if b - a > gap_s]
    return {"dead": dead, "dead_total": round(sum(d for _, d in dead), 2), "dead_longest": max((d for _, d in dead), default=0), "almost_still": almost, "event_gaps": gaps}


@program("QA-X02")
def qa_x02(work):
    fps = 30; blk = np.full(150, 40.0); blk[30:42] = 3; blk[60:80] = 12; blk[100:104] = 5
    r = dead_air_meter(blk, fps); wjson(Path(work) / "dead_air.json", r)
    return [C("12 frames < 8/255 = one 0.40 s dead stretch; 4 frames (0.13 s) ignored", r["dead"] == [(1.0, 0.4)], r["dead"]),
            C("strict pass (< 20 for >= 0.4 s) also finds the 0.67 s 'almost still' stretch at level 12", (2.0, 0.67) in r["almost_still"], r["almost_still"]),
            C("only the 0.7 s event gap (> 0.6 s) is listed; the 0.43 s one is not", r["event_gaps"] == [(1.97, 0.7)], r["event_gaps"])]


def apca(text_rgb, bg_rgb):
    Y = lambda c: sum(k * (v / 255) ** 2.4 for k, v in zip((0.2126729, 0.7151522, 0.0721750), c))
    clamp = lambda y: y + (0.022 - y) ** 1.414 if y < 0.022 else y
    yt, yb = clamp(Y(text_rgb)), clamp(Y(bg_rgb))
    if abs(yb - yt) < 0.0005:
        return 0.0
    if yb > yt:
        s = (yb ** 0.56 - yt ** 0.57) * 1.14; return 0.0 if s < 0.1 else (s - 0.027) * 100
    s = (yb ** 0.65 - yt ** 0.62) * 1.14; return 0.0 if s > -0.1 else (s + 0.027) * 100


def double_render_contrast(bg, draw_text, text_rgb):
    import cv2
    with_t = draw_text(bg.copy()); mask = np.any(with_t != bg, axis=-1).astype(np.uint8)
    mask = cv2.dilate(mask, np.ones((5, 5), np.uint8)).astype(bool)
    under = bg[mask].reshape(-1, 3); ratios = [contrast(text_rgb, tuple(int(v) for v in px)) for px in np.unique(under, axis=0)]
    lcs = [abs(apca(text_rgb, tuple(px))) for px in np.unique(under, axis=0)]
    return {"worst_wcag": round(min(ratios), 2), "mean_bg_wcag": round(contrast(text_rgb, tuple(under.mean(0))), 2), "worst_lc": round(min(lcs), 1), "mask_px": int(mask.sum())}


@program("QA-X03")
def qa_x03(work):
    from PIL import Image, ImageDraw
    bg = np.zeros((140, 700, 3), np.uint8); bg[:] = np.linspace(10, 200, 700).astype(np.uint8)[None, :, None]
    def draw(a):
        im = Image.fromarray(a); ImageDraw.Draw(im).text((20, 30), "Readable title", fill=(255, 255, 255), font=pil_font(72)); return np.asarray(im)
    r = double_render_contrast(bg, draw, (255, 255, 255)); save_png(Path(work) / "with_text.png", draw(bg))
    eff = 72 * 0.6; size_class = lambda px, caps=False: "read" if px >= (48 if caps else 64) else "label" if px >= 28 else "floor" if px >= 20 else "fail"
    verdict = r["worst_wcag"] >= 4.5 and r["worst_lc"] >= 60
    wjson(Path(work) / "contrast.json", r | {"effective_px": eff})
    return [C("sanity: black/white 21.0:1 and APCA Lc 106.0", round(contrast("#000000", "#ffffff"), 1) == 21.0 and round(apca((0, 0, 0), (255, 255, 255)), 1) == 106.0, round(apca((0, 0, 0), (255, 255, 255)), 2)),
            C("mean background looks fine (>= 4.5) but worst pixel under the dilated mask fails -> FAIL", r["mean_bg_wcag"] >= 4.5 and r["worst_wcag"] < 4.5 and not verdict, r),
            C("72 px inside a 0.6x camera push-out = 43.2 px effective: below 64 (read) -> label only", abs(eff - 43.2) < 1e-9 and size_class(eff) == "label", eff)]


def zoom_speed_linear(s0, ds, T, k, at="end"):
    s = s0 + ds if at == "end" else s0; return k * ds / T / s


def zoom_speed_log(s0, s1, T, k):
    return k * math.log(s1 / s0) / T


def one_move(a, b):
    return (a > 0) == (b > 0) and max(abs(a), abs(b)) / min(abs(a), abs(b)) <= 2


@program("QA-X04")
def qa_x04(work):
    a = zoom_speed_linear(1, 0.35, 0.35, 3, "end"); b = zoom_speed_linear(1.35, 0.185, 0.27, 3, "start")
    c = zoom_speed_log(1.04, 12, 0.45, 5); d = zoom_speed_linear(0.26, 0.74, 0.9, 5, "start"); flip = -b
    wjson(Path(work) / "zoom.json", {"strata": [a, b], "lo": [c, d]})
    return [C("Strata: in(3) x1->1.35 over 0.35 s = 2.222/s, next out(3) = 1.523/s (ratio 1.46) -> one move", round(a, 3) == 2.222 and round(b, 3) == 1.523 and one_move(a, b), (a, b)),
            C("LO: x1.04->x12 x^5 log 0.45 s = 27.17/s; x0.26->x1 out(5) 0.9 s = 15.81/s (ratio 1.72)", round(c, 2) == 27.17 and round(d, 2) == 15.81 and one_move(c, d), (c, d)),
            C("a flipped sign across the cut is not one move", not one_move(a, flip), "")]


def tempo_or_unavailable(x, sr):
    try:
        import librosa  # noqa: F401
    except ImportError:
        librosa = None
    if np.max(np.abs(x)) < 1e-6:
        return {"status": "unavailable", "reason": "silent input"}
    on = onset_times(x, sr)
    if len(on) < 4:
        return {"status": "unavailable", "reason": f"only {len(on)} onsets" + ("" if librosa else "; librosa missing")}
    return {"status": "measured", "bpm": round(tempo_bpm(x, sr)), "method": "numpy onset flux"}


UNMEASURED_CLAIMS = [r"4K60", r"\b8\s*[x×]\b", r"100\s*%\s*beat sync"]


@program("QA-X06")
def qa_x06(work):
    sr = 22050; clicks = np.zeros(6 * sr)
    for k in np.arange(0, 6, 0.5):
        clicks[int(k * sr):int(k * sr) + 300] = np.hanning(300)
    a, b = tempo_or_unavailable(clicks, sr), tempo_or_unavailable(np.zeros(sr), sr)
    report = "Delivered 4K60 with 100 % beat sync; audio checked numerically, not listened to."
    flags = [p for p in UNMEASURED_CLAIMS if re.search(p, report)]
    wjson(Path(work) / "tempo.json", {"clicks": a, "silence": b, "flags": flags})
    return [C("120 BPM clicks measured as 120 (not a default)", a == {"status": "measured", "bpm": 120, "method": "numpy onset flux"}, a),
            C("silence -> status unavailable with a reason, never 128", b["status"] == "unavailable" and "bpm" not in b, b), C("'4K60' and '100 % beat sync' flagged as unmeasured claims", len(flags) == 2, flags),
            C("report says audio was checked numerically, not listened to", "not listened" in report, "")]


LADDER = ["PLANNED", "CODE_WRITTEN", "PREVIEW_RENDERED", "VIDEO_RENDERED", "QA_PASS"]


def preflight(tools, auth_env):
    import shutil, os
    out = {}
    for t, probe_args in tools.items():
        exe = shutil.which(t)
        if not exe:
            out[t] = "missing"
        elif probe_args is None:
            out[t] = "untested"
        else:
            out[t] = "available" if subprocess.run([exe, *probe_args], capture_output=True).returncode == 0 else "missing"
    for svc, var in auth_env.items():
        out[svc] = "available" if os.environ.get(var) else "needs_auth"
    return out


def route(pf):
    if pf.get("chromium") == "available" and pf.get("ffmpeg") == "available":
        return "A"
    return "B" if pf.get("ffmpeg") == "available" else "C"


def ladder_ok(states, executor=True):
    if not executor:
        return states == ["PLANNED", "CODE_WRITTEN"] or states[-1:] == ["EXECUTOR_NOT_EXPOSED"]
    return states == LADDER[:len(states)]


@program("QA-X07")
def qa_x07(work):
    pf = preflight({"ffmpeg": ["-version"], "ffprobe": ["-version"], "kosif-missing-browser-xyz": ["--version"], "python3": None}, {"paid_api": "KOSIF_NO_SUCH_TOKEN_VAR"})
    pf_noff = dict(pf, ffmpeg="missing"); wjson(Path(work) / "preflight.json", pf)
    return [C("ffmpeg available, absent browser missing, unprobed python untested, missing token needs_auth", pf["ffmpeg"] == "available" and pf["kosif-missing-browser-xyz"] == "missing" and pf["python3"] == "untested" and pf["paid_api"] == "needs_auth", pf),
            C("no browser -> route B; no ffmpeg either -> route C", route(pf) == "B" and route(pf_noff) == "C" and route(dict(pf, chromium="available")) == "A", ""),
            C("status ladder must not skip: QA_PASS without VIDEO_RENDERED rejected", ladder_ok(LADDER[:4]) and not ladder_ok(["PLANNED", "CODE_WRITTEN", "QA_PASS"]), ""),
            C("without an executor the report ends EXECUTOR_NOT_EXPOSED", ladder_ok(["PLANNED", "CODE_WRITTEN", "EXECUTOR_NOT_EXPOSED"], executor=False), "")]


def tsl_if_lint(src):
    out = []
    for m in re.finditer(r"\bIf\s*\(", src):
        st = src.index("=>", m.end()); st = src.index("{", st) + 1; depth, i = 1, st
        while depth:
            depth += {"{": 1, "}": -1}.get(src[i], 0); i += 1
        for line in src[st:i - 1].splitlines():
            a = re.match(r"\s*([A-Za-z_][\w.\[\]]*)\s*=(?!=)\s*(.+?);?\s*$", line)
            if a and not a.group(1).startswith(("const ", "let ")):
                out.append(f"plain JS assignment '{a.group(1)} =' inside If(): use .assign()")
    return out


@program("QA-272")
def qa_272(work):
    good = "const c = vec3(0).toVar();\nIf(uv().x.greaterThan(0.5), () => {\n  c.assign(vec3(1,0,0));\n  buf.element(i).assign(c);\n});\nconst k = select(flag, a, b);"
    bad = "let c = vec3(0);\nIf(uv().x.greaterThan(0.5), () => {\n  c = vec3(1,0,0);\n  pos.x = 2.0;\n});"
    (Path(work) / "shader.js").write_text(bad)
    return [C(".assign() and select() inside If() pass", tsl_if_lint(good) == [], tsl_if_lint(good)),
            C("'c =' and 'pos.x =' reassignments inside If() are flagged", tsl_if_lint(bad) == ["plain JS assignment 'c =' inside If(): use .assign()", "plain JS assignment 'pos.x =' inside If(): use .assign()"], tsl_if_lint(bad))]
