"""KOSIF tools — the fast, everyday edits around a film or a clip. FFmpeg does the heavy lifting; frames stream, nothing
is written to disk twice. Every command is one line from `kmotion`.

    python tools.py silence  CLIP --out cut.mp4 [--threshold -35] [--min 0.45] [--pad 0.08]     jump-cut the silences out of a talking clip
    python tools.py aspect   CLIP --to 9:16 [--mode smart|crop|blur] --out v.mp4                 reframe: face-aware crop, centre crop, or blurred pad
    python tools.py trim     CLIP --from 3.2 --to 9.8 --out part.mp4                             frame-accurate cut
    python tools.py concat   A.mp4 B.mp4 ... --out all.mp4 [--size 1080x1920] [--fps 30]        join clips (different sizes are fitted)
    python tools.py loop     CLIP --out loop.mp4 [--seconds 30] [--xfade 0.6]                    a seamless loop (tail dissolves into head)
    python tools.py stabilize CLIP --out steady.mp4 [--strength 10]                               vidstab two-pass, or deshake when vidstab is absent
    python tools.py export   FILM --out DIR [--aspects 9:16,1:1,16:9] [--poster 2.0] [--gif] [--webp]   every delivery variant at once
    python tools.py thumb    FILM --out cover.jpg [--at 2.0] [--text "عنوان"] [--size 1080x1920]   a poster frame with an Arabic title
    python tools.py probe    FILE                                                                 streams, duration, fps, loudness
    python tools.py batch    jobs.json [--parallel 2]                                             several kmotion jobs side by side
    python tools.py fonts                                                                         which Arabic-capable fonts this machine has

Conventions: yuv420p H.264 (crf 18, preset medium) + 48 kHz AAC on every MP4; nothing fabricated; the source's audio
is kept unless the command says otherwise.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

FF = shutil.which("ffmpeg") or "ffmpeg"
FP = shutil.which("ffprobe") or "ffprobe"
V = ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
A = ["-c:a", "aac", "-b:a", "192k", "-ar", "48000"]
RATIOS = {"9:16": (1080, 1920), "16:9": (1920, 1080), "1:1": (1080, 1080), "4:5": (1080, 1350), "4:3": (1440, 1080), "21:9": (2520, 1080)}


def _run(cmd: list[str], capture: bool = True) -> subprocess.CompletedProcess:
    r = subprocess.run(cmd, capture_output=capture, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise RuntimeError((r.stderr or "")[-1500:])
    return r


def probe(p: Path) -> dict:
    j = json.loads(_run([FP, "-v", "error", "-show_entries", "stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels:format=duration,size",
                         "-of", "json", str(p)]).stdout)
    v = next((s for s in j["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in j["streams"] if s["codec_type"] == "audio"), None)
    out = {"file": str(p), "duration": float(j["format"].get("duration", 0) or 0), "mb": round(int(j["format"].get("size", 0)) / 1e6, 2),
           "video": None, "audio": None}
    if v:
        num, den = (v.get("r_frame_rate") or "30/1").split("/")
        out["video"] = {"codec": v.get("codec_name"), "w": int(v.get("width", 0)), "h": int(v.get("height", 0)), "fps": round(float(num) / float(den or 1), 3)}
    if a:
        out["audio"] = {"codec": a.get("codec_name"), "sr": int(a.get("sample_rate", 0)), "ch": int(a.get("channels", 0))}
    return out


def _has_filter(name: str) -> bool:
    r = subprocess.run([FF, "-hide_banner", "-filters"], capture_output=True, text=True)
    return bool(re.search(rf"\s{name}\s", r.stdout))


def _even(v: float) -> int:
    return max(2, int(round(v / 2)) * 2)


# ───────────────────────── fonts ─────────────────────────
_FONT_DIRS = ["C:/Windows/Fonts", "/usr/share/fonts", "/usr/local/share/fonts", str(Path.home() / ".fonts"), str(Path.home() / ".local/share/fonts"),
              "/Library/Fonts", "/System/Library/Fonts", "/System/Library/Fonts/Supplemental", str(Path.home() / "Library/Fonts"), str(HERE / "kit" / "fonts")]
_ARABIC = ["NotoNaskhArabic", "NotoSansArabic", "NotoKufiArabic", "Cairo", "Tajawal", "Almarai", "Amiri", "Scheherazade", "KacstOne", "DejaVuSans",
           "segoeui", "arial", "tahoma", "GeezaPro", "Geeza"]


def fonts(arabic: bool = True) -> list[Path]:
    """Font files on this machine that can set Arabic (by family name), most complete first."""
    found: list[Path] = []
    for d in _FONT_DIRS:
        dp = Path(d)
        if not dp.exists():
            continue
        for f in dp.rglob("*"):
            if f.suffix.lower() in (".ttf", ".otf", ".ttc"):
                found.append(f)
    names = _ARABIC if arabic else ["segoeui", "arial", "DejaVuSans", "NotoSans", "Helvetica"]
    ranked = []
    for n in names:
        ranked += sorted(f for f in found if n.lower() in f.stem.lower().replace("-", "").replace("_", "") and "mono" not in f.stem.lower())
    return list(dict.fromkeys(ranked))


def font_path(arabic: bool = True) -> Path | None:
    fs = fonts(arabic)
    return fs[0] if fs else None


def _ff_path(p: Path) -> str:
    """A path inside an FFmpeg filter string (colons and backslashes escaped)."""
    return p.as_posix().replace("\\", "/").replace(":", "\\:").replace("'", "\\'")


# ───────────────────────── silence ─────────────────────────
def silences(src: Path, threshold: float = -35.0, min_len: float = 0.45) -> list[tuple[float, float]]:
    r = subprocess.run([FF, "-v", "info", "-i", str(src), "-af", f"silencedetect=n={threshold}dB:d={min_len}", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    starts = [float(m) for m in re.findall(r"silence_start: ([\d.]+)", r.stderr)]
    ends = [float(m) for m in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
    return list(zip(starts, ends))


def silence_cut(src: Path, out: Path, threshold: float = -35.0, min_len: float = 0.45, pad: float = 0.08, report: bool = True) -> dict:
    """Remove the pauses of a talking clip (a jump-cut edit). Every silence longer than min_len (below threshold dBFS)
    is cut, keeping `pad` seconds of air on each side so words never clip. Picture and sound are cut together,
    frame-accurate, in one FFmpeg pass."""
    info = probe(src)
    dur = info["duration"]
    sil = silences(src, threshold, min_len)
    keep, pos = [], 0.0
    for a, b in sil:
        a2, b2 = a + pad, b - pad
        if a2 > pos + 0.05:
            keep.append((pos, a2))
        pos = max(pos, b2)
    if dur - pos > 0.05:
        keep.append((pos, dur))
    if not keep:
        keep = [(0.0, dur)]
    has_audio = info["audio"] is not None
    parts, labels = [], []
    for i, (a, b) in enumerate(keep):
        parts.append(f"[0:v]trim=start={a:.3f}:end={b:.3f},setpts=PTS-STARTPTS[v{i}]")
        if has_audio:
            parts.append(f"[0:a]atrim=start={a:.3f}:end={b:.3f},asetpts=PTS-STARTPTS[a{i}]")
        labels.append(f"[v{i}]" + (f"[a{i}]" if has_audio else ""))
    graph = ";".join(parts) + f";{''.join(labels)}concat=n={len(keep)}:v=1:a={1 if has_audio else 0}[v]" + ("[a]" if has_audio else "")
    maps = ["-map", "[v]"] + (["-map", "[a]"] if has_audio else [])
    out.parent.mkdir(parents=True, exist_ok=True)
    _run([FF, "-y", "-v", "error", "-i", str(src), "-filter_complex", graph, *maps, *V, *(A if has_audio else []), str(out)])
    kept = sum(b - a for a, b in keep)
    rep = {"file": str(out), "source_s": round(dur, 2), "kept_s": round(kept, 2), "removed_s": round(dur - kept, 2),
           "cuts": len(keep) - 1, "silences": [(round(a, 2), round(b, 2)) for a, b in sil]}
    if report:
        out.with_suffix(".silence.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    return rep


# ───────────────────────── aspect / reframe ─────────────────────────
def _attention_centre(src: Path, samples: int = 24) -> tuple[float | None, float | None]:
    """Where the eye goes when there is no face: the centroid of motion energy (frame differences) across the clip,
    which follows the subject that moves — a speaker's gestures, a walking person, a product being turned."""
    import numpy as np
    info = probe(src)
    w, h = info["video"]["w"], info["video"]["h"]
    sw = 160
    sh = _even(h * sw / w)
    step = max(0.15, info["duration"] / samples)
    p = subprocess.Popen([FF, "-v", "error", "-i", str(src), "-vf", f"fps=1/{step},scale={sw}:{sh}", "-f", "rawvideo", "-pix_fmt", "gray", "-"],
                         stdout=subprocess.PIPE)
    prev, acc = None, np.zeros((sh, sw), np.float32)
    while True:
        buf = p.stdout.read(sw * sh)
        if len(buf) < sw * sh:
            break
        g = np.frombuffer(buf, np.uint8).reshape(sh, sw).astype(np.float32)
        if prev is not None:
            acc += np.abs(g - prev)
        prev = g
    p.wait()
    if acc.sum() < 1e-3:
        return None, None
    ys, xs = np.mgrid[0:sh, 0:sw]
    tot = acc.sum()
    return float((xs * acc).sum() / tot / sw), float((ys * acc).sum() / tot / sh)


def _face_centre(src: Path, samples: int = 24) -> tuple[float | None, float | None]:
    """Where the faces are, as a share of the frame (x, y), from a few frames across the clip (OpenCV Haar, when this
    OpenCV build carries objdetect); otherwise the motion centroid (`_attention_centre`)."""
    try:
        import cv2
        import numpy as np
        casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        if casc.empty():
            raise AttributeError("no cascade")
    except (ImportError, AttributeError):
        return _attention_centre(src, samples)
    info = probe(src)
    w, h = info["video"]["w"], info["video"]["h"]
    sw = 480
    sh = _even(h * sw / w)
    step = max(0.2, info["duration"] / samples)
    p = subprocess.Popen([FF, "-v", "error", "-i", str(src), "-vf", f"fps=1/{step},scale={sw}:{sh}", "-f", "rawvideo", "-pix_fmt", "gray", "-"],
                         stdout=subprocess.PIPE)
    xs, ys, ws = [], [], []
    while True:
        buf = p.stdout.read(sw * sh)
        if len(buf) < sw * sh:
            break
        g = np.frombuffer(buf, np.uint8).reshape(sh, sw)
        for (x, y, fw, fh) in casc.detectMultiScale(g, 1.15, 5, minSize=(28, 28)):
            xs.append((x + fw / 2) / sw); ys.append((y + fh / 2) / sh); ws.append(fw)
    p.wait()
    if not xs:
        return _attention_centre(src, samples)
    wts = np.asarray(ws, np.float32)
    return float(np.average(xs, weights=wts)), float(np.average(ys, weights=wts))


def aspect(src: Path, out: Path, to: str = "9:16", mode: str = "smart", size: tuple[int, int] | None = None) -> dict:
    """Reframe a clip to another aspect. smart: crop around the faces (centre crop when there are none); crop: centre
    crop; blur: the whole picture fitted inside, over a blurred, darkened copy of itself filling the frame."""
    W, H = size or RATIOS[to]
    info = probe(src)
    sw, sh = info["video"]["w"], info["video"]["h"]
    cx = cy = 0.5
    used = mode
    if mode == "smart":
        fx, fy = _face_centre(src)
        if fx is None:
            used = "centre"
        else:
            cx, cy = fx, fy
    if mode == "blur":
        vf = (f"split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},gblur=sigma=40,eq=brightness=-0.12:saturation=0.85[bg];"
              f"[b]scale={W}:{H}:force_original_aspect_ratio=decrease:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,format=yuv420p")
    else:
        scale = max(W / sw, H / sh)
        tw, th = _even(sw * scale), _even(sh * scale)
        x = int(min(max(0, cx * tw - W / 2), tw - W)); y = int(min(max(0, cy * th - H / 2), th - H))
        vf = f"scale={tw}:{th}:flags=lanczos,crop={W}:{H}:{x}:{y},format=yuv420p"
    out.parent.mkdir(parents=True, exist_ok=True)
    _run([FF, "-y", "-v", "error", "-i", str(src), "-vf", vf, *V, "-c:a", "copy", str(out)])
    return {"file": str(out), "size": f"{W}x{H}", "mode": used, "centre": (round(cx, 3), round(cy, 3))}


# ───────────────────────── trim / concat / loop / stabilize ─────────────────────────
def trim(src: Path, out: Path, start: float, end: float | None) -> dict:
    args = [FF, "-y", "-v", "error", "-ss", f"{start:.3f}", "-i", str(src)]
    if end is not None:
        args += ["-t", f"{max(0.0, end - start):.3f}"]
    out.parent.mkdir(parents=True, exist_ok=True)
    _run([*args, *V, *A, str(out)])
    return {"file": str(out), "from": start, "to": end, "duration": probe(out)["duration"]}


def concat(clips: list[Path], out: Path, size: tuple[int, int] | None = None, fps: int = 30) -> dict:
    """Join clips in order. Sizes and rates are unified (fit inside, letterboxed with black); clips without sound get
    silence so the audio track never breaks."""
    infos = [probe(c) for c in clips]
    if size is None:
        size = (infos[0]["video"]["w"], infos[0]["video"]["h"])
    W, H = size
    args = [FF, "-y", "-v", "error"]
    parts, labels = [], []
    for i, (c, inf) in enumerate(zip(clips, infos)):
        args += ["-i", str(c)]
        parts.append(f"[{i}:v]scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps={fps},format=yuv420p[v{i}]")
        if inf["audio"]:
            parts.append(f"[{i}:a]aformat=sample_rates=48000:channel_layouts=stereo,asetpts=PTS-STARTPTS[a{i}]")
        else:
            parts.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{inf['duration']:.3f}[a{i}]")
        labels.append(f"[v{i}][a{i}]")
    graph = ";".join(parts) + f";{''.join(labels)}concat=n={len(clips)}:v=1:a=1[v][a]"
    out.parent.mkdir(parents=True, exist_ok=True)
    _run([*args, "-filter_complex", graph, "-map", "[v]", "-map", "[a]", *V, *A, str(out)])
    return {"file": str(out), "clips": len(clips), "size": f"{W}x{H}", "duration": round(probe(out)["duration"], 2)}


def loop(src: Path, out: Path, seconds: float | None = None, xfade: float = 0.6) -> dict:
    """A seamless loop: the last `xfade` seconds dissolve into the first, then the unit repeats to `seconds`."""
    info = probe(src)
    d = info["duration"]
    x = min(xfade, d / 3)
    unit = d - x
    reps = max(1, math.ceil((seconds or unit) / unit))
    has_a = info["audio"] is not None
    # unit: [0, d-x) with the tail [d-x, d) blended over the head
    g = (f"[0:v]split[s0][s1];[s0]trim=0:{unit:.3f},setpts=PTS-STARTPTS[head];[s1]trim={unit:.3f}:{d:.3f},setpts=PTS-STARTPTS[tail];"
         f"[head][tail]xfade=transition=fade:duration={x:.3f}:offset=0[u]")
    # xfade with offset 0 blends the tail over the start of head: a loop that closes on itself
    if has_a:
        g += (f";[0:a]asplit[t0][t1];[t0]atrim=0:{unit:.3f},asetpts=PTS-STARTPTS[ah];[t1]atrim={unit:.3f}:{d:.3f},asetpts=PTS-STARTPTS[at];"
              f"[ah][at]acrossfade=d={x:.3f}:c1=tri:c2=tri[ua]")
    tmp = Path(tempfile.mkdtemp(prefix="kosif_loop_")) / "unit.mp4"
    maps = ["-map", "[u]"] + (["-map", "[ua]"] if has_a else [])
    _run([FF, "-y", "-v", "error", "-i", str(src), "-filter_complex", g, *maps, *V, *(A if has_a else []), str(tmp)])
    out.parent.mkdir(parents=True, exist_ok=True)
    _run([FF, "-y", "-v", "error", "-stream_loop", str(reps - 1), "-i", str(tmp), "-c", "copy", "-t", f"{(seconds or unit):.3f}", "-movflags", "+faststart", str(out)])
    shutil.rmtree(tmp.parent, ignore_errors=True)
    return {"file": str(out), "unit_s": round(unit, 2), "repeats": reps, "duration": round(probe(out)["duration"], 2)}


def stabilize(src: Path, out: Path, strength: int = 10) -> dict:
    out.parent.mkdir(parents=True, exist_ok=True)
    if _has_filter("vidstabdetect"):
        trf = Path(tempfile.mkdtemp(prefix="kosif_stab_")) / "t.trf"
        _run([FF, "-y", "-v", "error", "-i", str(src), "-vf", f"vidstabdetect=shakiness={min(10, strength)}:accuracy=15:result='{_ff_path(trf)}'", "-f", "null", "-"])
        _run([FF, "-y", "-v", "error", "-i", str(src), "-vf", f"vidstabtransform=input='{_ff_path(trf)}':zoom=0:smoothing={strength * 2}:optzoom=1,unsharp=5:5:0.5,format=yuv420p",
              *V, "-c:a", "copy", str(out)])
        shutil.rmtree(trf.parent, ignore_errors=True)
        return {"file": str(out), "method": "vidstab (2-pass)"}
    _run([FF, "-y", "-v", "error", "-i", str(src), "-vf", f"deshake=rx=32:ry=32:edge=mirror:blocksize=8,format=yuv420p", *V, "-c:a", "copy", str(out)])
    return {"file": str(out), "method": "deshake (vidstab not built into this ffmpeg)"}


# ───────────────────────── export / thumb ─────────────────────────
def thumb(src: Path, out: Path, at: float = 2.0, text: str | None = None, size: tuple[int, int] | None = None, sub: str | None = None) -> dict:
    """A poster frame: the frame at `at`, optionally reframed, darkened toward the bottom, with an Arabic title set in
    a real Arabic font (shaped and ordered by arabic_reshaper + python-bidi when they are installed)."""
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
    import numpy as np
    info = probe(src)
    w, h = info["video"]["w"], info["video"]["h"]
    raw = subprocess.run([FF, "-v", "error", "-ss", f"{at:.3f}", "-i", str(src), "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True).stdout
    im = Image.frombytes("RGB", (w, h), raw[:w * h * 3])
    if size:
        W, H = size
        s = max(W / w, H / h)
        im = im.resize((_even(w * s), _even(h * s)), Image.LANCZOS)
        x, y = (im.width - W) // 2, (im.height - H) // 2
        im = im.crop((x, y, x + W, y + H))
    W, H = im.size
    font_used = None
    if text:
        grad = Image.new("L", (1, H))
        for yy in range(H):
            t = max(0.0, (yy / H - 0.45) / 0.55)
            grad.putpixel((0, yy), int(255 * 0.78 * t * t))
        im = Image.composite(Image.new("RGB", im.size, (0, 0, 0)), im, grad.resize(im.size))
        fp = font_path(arabic=any("\u0600" <= ch <= "\u06ff" for ch in text))
        font_used = str(fp) if fp else None
        fs = round(min(W, H) * 0.085)
        font = ImageFont.truetype(str(fp), fs) if fp else ImageFont.load_default(fs)
        try:
            import arabic_reshaper
            from bidi.algorithm import get_display
            shaped = get_display(arabic_reshaper.reshape(text))
        except ImportError:
            shaped = text
        lines = _wrap(shaped, font, W * 0.84, ImageDraw.Draw(im))
        dr = ImageDraw.Draw(im)
        y = H * 0.80 - fs * 1.25 * len(lines)
        for ln in lines:
            dr.text((W / 2, y), ln, font=font, fill=(255, 255, 255), anchor="ma", stroke_width=max(2, fs // 18), stroke_fill=(0, 0, 0))
            y += fs * 1.25
        if sub:
            sf = ImageFont.truetype(str(fp), round(fs * 0.5)) if fp else ImageFont.load_default(round(fs * 0.5))
            dr.text((W / 2, y + fs * 0.1), sub, font=sf, fill=(231, 182, 90), anchor="ma")
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, quality=93)
    return {"file": str(out), "size": f"{W}x{H}", "at": at, "font": font_used}


def _wrap(text: str, font, max_w: float, dr) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for w in words:
        cand = (cur + " " + w).strip()
        if dr.textlength(cand, font=font) <= max_w or not cur:
            cur = cand
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines[:3]


def export(src: Path, out_dir: Path, aspects: list[str] | None = None, poster_at: float = 2.0, gif: bool = False, webp: bool = False,
           title: str | None = None, mode: str = "smart", parallel: int = 2) -> dict:
    """Everything a delivery needs from one master: a variant per aspect (face-aware reframe), a poster JPG (with the
    title when given), and optional GIF/WebP previews. Variants render side by side."""
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = src.stem
    info = probe(src)
    w, h = info["video"]["w"], info["video"]["h"]
    own = f"{w}:{h}"
    aspects = aspects or ["9:16", "1:1", "16:9"]
    rep = {"source": str(src), "variants": {}, "poster": None}
    jobs = []
    for a in aspects:
        W, H = RATIOS[a]
        if abs(W / H - w / h) < 0.01:
            dst = out_dir / f"{stem}_{a.replace(':', 'x')}.mp4"
            shutil.copy2(src, dst)
            rep["variants"][a] = {"file": str(dst), "mode": "copy"}
            continue
        jobs.append((a, out_dir / f"{stem}_{a.replace(':', 'x')}.mp4"))
    with ThreadPoolExecutor(max(1, parallel)) as ex:
        for a, r in zip([j[0] for j in jobs], ex.map(lambda j: aspect(src, j[1], j[0], mode), jobs)):
            rep["variants"][a] = r
    poster = out_dir / f"{stem}_poster.jpg"
    rep["poster"] = thumb(src, poster, poster_at, title)
    if gif:
        g = out_dir / f"{stem}.gif"
        _run([FF, "-y", "-v", "error", "-i", str(src), "-vf", "fps=12,scale=480:-2:flags=lanczos,split[a][b];[a]palettegen=max_colors=160[p];[b][p]paletteuse=dither=bayer:bayer_scale=4",
              "-t", "8", str(g)])
        rep["gif"] = str(g)
    if webp:
        wp = out_dir / f"{stem}.webp"
        _run([FF, "-y", "-v", "error", "-i", str(src), "-vf", "fps=15,scale=540:-2:flags=lanczos", "-loop", "0", "-q:v", "70", "-t", "8", str(wp)])
        rep["webp"] = str(wp)
    (out_dir / f"{stem}.export.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    return rep


# ───────────────────────── batch ─────────────────────────
def batch(jobs_file: Path, parallel: int = 2) -> dict:
    """jobs.json: [{"cmd": "render", "args": ["projects/a", "--draft"]}, {"cmd": "grade", "args": ["x.mp4", "--preset", "blue_hour"]}]
    Each job is `python kmotion.py CMD ARGS…` in its own process; `parallel` of them run at once."""
    jobs = json.loads(Path(jobs_file).read_text(encoding="utf-8"))
    km = HERE / "kmotion.py"

    def one(j: dict) -> dict:
        cmd = [sys.executable, str(km), j["cmd"], *[str(a) for a in j.get("args", [])]]
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", env={**os.environ, "KOSIF_WORKERS": "1"})
        return {"cmd": j["cmd"], "args": j.get("args", []), "ok": r.returncode == 0, "out": (r.stdout or "")[-600:], "err": (r.stderr or "")[-400:]}
    with ThreadPoolExecutor(max(1, parallel)) as ex:
        results = list(ex.map(one, jobs))
    rep = {"jobs": len(jobs), "ok": sum(r["ok"] for r in results), "results": results}
    Path(jobs_file).with_suffix(".report.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    return rep


# ───────────────────────── CLI ─────────────────────────
def _size(s: str | None):
    return tuple(int(v) for v in s.lower().split("x")) if s else None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("silence"); p.add_argument("clip"); p.add_argument("--out", required=True); p.add_argument("--threshold", type=float, default=-35.0)
    p.add_argument("--min", dest="min_len", type=float, default=0.45); p.add_argument("--pad", type=float, default=0.08)
    p = sub.add_parser("aspect"); p.add_argument("clip"); p.add_argument("--to", default="9:16", choices=list(RATIOS)); p.add_argument("--mode", default="smart", choices=["smart", "crop", "blur"])
    p.add_argument("--out", required=True); p.add_argument("--size")
    p = sub.add_parser("trim"); p.add_argument("clip"); p.add_argument("--from", dest="start", type=float, default=0.0); p.add_argument("--to", dest="end", type=float); p.add_argument("--out", required=True)
    p = sub.add_parser("concat"); p.add_argument("clips", nargs="+"); p.add_argument("--out", required=True); p.add_argument("--size"); p.add_argument("--fps", type=int, default=30)
    p = sub.add_parser("loop"); p.add_argument("clip"); p.add_argument("--out", required=True); p.add_argument("--seconds", type=float); p.add_argument("--xfade", type=float, default=0.6)
    p = sub.add_parser("stabilize"); p.add_argument("clip"); p.add_argument("--out", required=True); p.add_argument("--strength", type=int, default=10)
    p = sub.add_parser("export"); p.add_argument("film"); p.add_argument("--out", required=True); p.add_argument("--aspects", default="9:16,1:1,16:9")
    p.add_argument("--poster", type=float, default=2.0); p.add_argument("--gif", action="store_true"); p.add_argument("--webp", action="store_true")
    p.add_argument("--title"); p.add_argument("--mode", default="smart", choices=["smart", "crop", "blur"]); p.add_argument("--parallel", type=int, default=2)
    p = sub.add_parser("thumb"); p.add_argument("film"); p.add_argument("--out", required=True); p.add_argument("--at", type=float, default=2.0)
    p.add_argument("--text"); p.add_argument("--sub"); p.add_argument("--size")
    p = sub.add_parser("probe"); p.add_argument("file")
    p = sub.add_parser("batch"); p.add_argument("jobs"); p.add_argument("--parallel", type=int, default=2)
    sub.add_parser("fonts")
    a = ap.parse_args()
    if a.cmd == "silence":
        rep = silence_cut(Path(a.clip), Path(a.out), a.threshold, a.min_len, a.pad)
    elif a.cmd == "aspect":
        rep = aspect(Path(a.clip), Path(a.out), a.to, a.mode, _size(a.size))
    elif a.cmd == "trim":
        rep = trim(Path(a.clip), Path(a.out), a.start, a.end)
    elif a.cmd == "concat":
        rep = concat([Path(c) for c in a.clips], Path(a.out), _size(a.size), a.fps)
    elif a.cmd == "loop":
        rep = loop(Path(a.clip), Path(a.out), a.seconds, a.xfade)
    elif a.cmd == "stabilize":
        rep = stabilize(Path(a.clip), Path(a.out), a.strength)
    elif a.cmd == "export":
        rep = export(Path(a.film), Path(a.out), [x.strip() for x in a.aspects.split(",") if x.strip()], a.poster, a.gif, a.webp, a.title, a.mode, a.parallel)
    elif a.cmd == "thumb":
        rep = thumb(Path(a.film), Path(a.out), a.at, a.text, _size(a.size), a.sub)
    elif a.cmd == "probe":
        rep = probe(Path(a.file))
    elif a.cmd == "batch":
        rep = batch(Path(a.jobs), a.parallel)
    else:
        rep = {"arabic_fonts": [str(f) for f in fonts(True)][:8], "latin_fonts": [str(f) for f in fonts(False)][:4]}
    print(json.dumps(rep, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
