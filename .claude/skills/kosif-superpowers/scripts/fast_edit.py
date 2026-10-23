#!/usr/bin/env python3
"""KOSIF Fast Edit: quick single-file video/audio operations with honest receipts.

Ideas studied from a small user-supplied desktop editor (CapCut Studio Pro 2.0, an
Electron front end over FFmpeg) and rebuilt here in our own code. No code from it is
used. Each command fixes a weakness seen there:

  keyframes      list the video keyframes (a stream copy can only start on one)
  cut            "instant cut": stream copy when the start is on or near a keyframe,
                 otherwise an exact re-encode; the receipt says which and by how much
                 a copy would have drifted, instead of silently starting early
  voice          voice presets (chipmunk, deep, robot, echo, radio, telephone) that
                 read the real sample rate and keep the duration
  brighten       low-light lift + optional denoise, measured before and after
                 (mean luma), and skipped when the clip is already bright
  extract-audio  pull the audio out, bit-exact when the container allows it

Sources are never modified and an existing output is never overwritten unless
--force is given. Every command prints a JSON receipt.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys

SCHEMA = "kosif.fast_edit.receipt.v1"
TIMEOUT = 900

# name -> (pitch factor or None, extra audio filter or None, what it does)
VOICE_PRESETS = {
    "chipmunk": (1.35, None, "higher pitch, same length"),
    "deep": (0.78, None, "lower pitch, same length"),
    "robot": (None, "afftfilt=real='hypot(re,im)':imag='0':win_size=512:overlap=0.75", "flat-phase robotic voice"),
    "echo": (None, "aecho=0.8:0.85:60|120:0.35|0.2", "two-tap echo"),
    "radio": (None, "highpass=f=300,lowpass=f=3400,acompressor=threshold=0.1:ratio=4", "band-limited, compressed broadcast voice"),
    "telephone": (None, "highpass=f=500,lowpass=f=2600,volume=1.3", "narrow phone line"),
}

# mean luma (0..255) above which a clip is not treated as low-light
BRIGHT_ENOUGH = 90.0


# ---------------------------------------------------------------- helpers

def run(cmd, timeout=TIMEOUT):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", stdin=subprocess.DEVNULL, timeout=timeout)


def need(binary):
    path = shutil.which(binary)
    if not path:
        raise SystemExit(f"{binary} not found on PATH")
    return path


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def probe(path):
    p = run([need("ffprobe"), "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)], 60)
    if p.returncode:
        raise ValueError(f"ffprobe could not read {path}: {p.stderr.strip()[-200:]}")
    return json.loads(p.stdout)


def duration_of(info):
    d = info.get("format", {}).get("duration")
    return float(d) if d not in (None, "N/A") else 0.0


def stream(info, kind):
    return next((s for s in info.get("streams", []) if s.get("codec_type") == kind), None)


def check_io(src, out, force):
    src, out = Path(src), Path(out)
    if not src.is_file():
        raise ValueError(f"input not found: {src}")
    if out.resolve() == src.resolve():
        raise ValueError("output must differ from the input; sources are never modified")
    if out.exists() and not force:
        raise ValueError(f"output exists: {out} (use --force to replace it)")
    out.parent.mkdir(parents=True, exist_ok=True)
    return src, out


def ffmpeg(args):
    p = run([need("ffmpeg"), "-hide_banner", "-nostdin", "-loglevel", "error", "-y", *args])
    if p.returncode:
        raise RuntimeError(f"ffmpeg failed: {p.stderr.strip()[-400:]}")


def receipt(command, src, out, **fields):
    info = probe(out)
    body = {"schema": SCHEMA, "command": command, "input": str(src), "output": str(out),
            "output_duration": round(duration_of(info), 3), "output_sha256": sha256(out),
            "streams": [{"type": s.get("codec_type"), "codec": s.get("codec_name"),
                         "duration": round(float(s["duration"]), 3) if s.get("duration") not in (None, "N/A") else None}
                        for s in info.get("streams", [])]}
    body.update(fields)
    return body


# ---------------------------------------------------------------- keyframes / cut

def keyframes(path):
    """Presentation times (seconds) of the video keyframes, ascending."""
    p = run([need("ffprobe"), "-v", "error", "-select_streams", "v:0", "-skip_frame", "nokey",
             "-show_entries", "frame=pts_time,best_effort_timestamp_time", "-of", "json", str(path)], 300)
    if p.returncode:
        raise ValueError(f"ffprobe could not list keyframes: {p.stderr.strip()[-200:]}")
    times = []
    for fr in json.loads(p.stdout or "{}").get("frames", []):
        t = fr.get("pts_time", fr.get("best_effort_timestamp_time"))
        if t not in (None, "N/A"):
            times.append(round(float(t), 6))
    return sorted(set(times))


def plan_cut(kfs, start, end, mode="auto", tolerance=0.1):
    """Decide copy vs exact for [start, end). Pure function, no I/O.

    A stream copy has to begin on a keyframe, so it really starts at the last
    keyframe at or before `start`; `drift` is how much earlier that is.
    """
    if not (math.isfinite(start) and math.isfinite(end)) or start < 0 or end <= start:
        raise ValueError("need 0 <= start < end")
    if mode not in ("auto", "copy", "exact"):
        raise ValueError("mode must be auto, copy or exact")
    before = [k for k in kfs if k <= start + 1e-6]
    anchor = before[-1] if before else (kfs[0] if kfs else 0.0)
    drift = round(max(0.0, start - anchor), 6)
    if mode == "auto":
        chosen = "copy" if kfs and drift <= tolerance else "exact"
    else:
        chosen = mode
    nxt = next((k for k in kfs if k > start + 1e-6), None)
    return {"requested_start": start, "requested_end": end, "mode": chosen, "asked_mode": mode,
            "keyframe_at_or_before": anchor, "next_keyframe": nxt, "copy_drift": drift,
            "tolerance": tolerance,
            "why": ("start is within the tolerance of a keyframe, so a stream copy is exact enough"
                    if chosen == "copy" and mode == "auto" else
                    "start is between keyframes, so it is re-encoded to start exactly"
                    if mode == "auto" else f"{mode} was asked for")}


def cmd_keyframes(a):
    kfs = keyframes(a.input)
    gaps = [round(b - x, 6) for x, b in zip(kfs, kfs[1:])]
    return {"schema": SCHEMA, "command": "keyframes", "input": a.input, "count": len(kfs),
            "keyframes": kfs, "max_gap": max(gaps) if gaps else None}


def cmd_cut(a):
    src, out = check_io(a.input, a.output, a.force)
    info = probe(src)
    total = duration_of(info)
    end = a.end if a.end is not None else total
    if a.start >= total:
        raise ValueError(f"start {a.start} is past the end of the input ({total:.3f}s)")
    end = min(end, total)
    has_video = stream(info, "video") is not None
    kfs = keyframes(src) if has_video else []
    plan = plan_cut(kfs, a.start, end, a.mode, a.tolerance) if has_video else \
        {"requested_start": a.start, "requested_end": end, "mode": "copy", "asked_mode": a.mode,
         "copy_drift": 0.0, "why": "audio only: every packet is a cut point"}
    if plan["mode"] == "copy":
        # input seeking snaps to the keyframe; ask for the keyframe explicitly so the
        # receipt and the file agree. Packet-level copy may also keep a frame or two past
        # the end (B-frame reordering); the receipt's measured durations show it.
        begin = plan.get("keyframe_at_or_before", a.start) if has_video else a.start
        ffmpeg(["-ss", f"{begin:.6f}", "-i", str(src), "-t", f"{end - begin:.6f}", "-map", "0",
                "-c", "copy", str(out)])
        actual_start = begin
    else:
        args = ["-ss", f"{a.start:.6f}", "-i", str(src), "-t", f"{end - a.start:.6f}", "-map", "0:v:0?", "-map", "0:a?"]
        if has_video:
            args += ["-c:v", "libx264", "-preset", a.preset, "-crf", str(a.crf), "-pix_fmt", "yuv420p"]
        args += ["-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)]
        ffmpeg(args)
        actual_start = a.start
    r = receipt("cut", src, out, plan=plan, actual_start=round(actual_start, 6),
                requested_duration=round(end - a.start, 3))
    r["start_error"] = round(actual_start - a.start, 6)
    return r


# ---------------------------------------------------------------- voice

def voice_filter(preset, sample_rate):
    if preset not in VOICE_PRESETS:
        raise ValueError(f"unknown preset {preset}; choose from {', '.join(sorted(VOICE_PRESETS))}")
    if not isinstance(sample_rate, int) or sample_rate < 8000:
        raise ValueError("sample rate must be an integer >= 8000")
    factor, extra, _ = VOICE_PRESETS[preset]
    if factor:
        # resample trick with the real rate, then undo the speed change
        return f"asetrate={round(sample_rate * factor)},aresample={sample_rate},atempo={1 / factor:.6f}"
    return extra


def cmd_voice(a):
    src, out = check_io(a.input, a.output, a.force)
    info = probe(src)
    aud = stream(info, "audio")
    if not aud:
        raise ValueError("input has no audio stream")
    rate = int(aud.get("sample_rate") or 0)
    af = voice_filter(a.preset, rate)
    ext = out.suffix.lower()
    audio_only = ext in (".wav", ".flac", ".mp3", ".m4a", ".aac", ".ogg", ".opus")
    keep_video = bool(stream(info, "video")) and not audio_only
    args = ["-i", str(src)] + (["-map", "0:v:0", "-c:v", "copy"] if keep_video else ["-vn"])
    args += ["-map", "0:a:0", "-af", af, "-ar", str(rate)]
    codec = {".wav": ["-c:a", "pcm_s16le"], ".flac": ["-c:a", "flac"], ".mp3": ["-c:a", "libmp3lame", "-q:a", "2"]}
    args += codec.get(ext, ["-c:a", "aac", "-b:a", "192k"]) + [str(out)]
    ffmpeg(args)
    return receipt("voice", src, out, preset=a.preset, filter=af, sample_rate=rate,
                   input_duration=round(duration_of(info), 3),
                   video="stream-copied" if keep_video else "none")


# ---------------------------------------------------------------- brighten

def mean_luma(path, samples=8):
    """Average Y (0..255) over a few evenly spaced frames."""
    info = probe(path)
    dur = max(duration_of(info), 0.04)
    v = stream(info, "video")
    if not v:
        raise ValueError("input has no video stream")
    vals = []
    for i in range(samples):
        t = dur * (i + 0.5) / samples
        p = subprocess.run([need("ffmpeg"), "-hide_banner", "-nostdin", "-loglevel", "error", "-ss", f"{t:.3f}",
                            "-i", str(path), "-frames:v", "1", "-vf", "scale=160:-2,format=gray", "-f", "rawvideo", "-"],
                           capture_output=True, stdin=subprocess.DEVNULL, timeout=60)
        if p.returncode == 0 and p.stdout:
            vals.append(sum(p.stdout) / len(p.stdout))
    if not vals:
        raise ValueError("could not decode any frame")
    return round(sum(vals) / len(vals), 2)


def brighten_filter(strength=0.6, denoise=False):
    if not (isinstance(strength, (int, float)) and 0.0 < strength <= 1.0):
        raise ValueError("strength must be in (0, 1]")
    lift = 0.10 + 0.25 * strength          # where a mid-dark input (0.25) lands above itself
    mid_out = min(0.95, 0.25 + lift)
    low_out = round(0.04 * strength, 3)
    parts = [f"curves=all='0/{low_out} 0.25/{mid_out:.3f} 1/1'"]
    if denoise:
        parts.append("hqdn3d=1.5:1.5:6:6")
    parts.append("unsharp=5:5:0.4:3:3:0")
    return ",".join(parts)


def cmd_brighten(a):
    src, out = check_io(a.input, a.output, a.force)
    before = mean_luma(src)
    if before >= BRIGHT_ENOUGH and not a.force_lift:
        return {"schema": SCHEMA, "command": "brighten", "input": str(src), "output": None,
                "luma_before": before, "skipped": True,
                "why": f"mean luma {before} is already >= {BRIGHT_ENOUGH}; use --force-lift to brighten anyway"}
    vf = brighten_filter(a.strength, a.denoise)
    ffmpeg(["-i", str(src), "-map", "0:v:0", "-map", "0:a?", "-vf", vf, "-c:v", "libx264", "-preset", a.preset,
            "-crf", str(a.crf), "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", str(out)])
    after = mean_luma(out)
    return receipt("brighten", src, out, filter=vf, luma_before=before, luma_after=after,
                   luma_gain=round(after - before, 2), audio="stream-copied", skipped=False)


# ---------------------------------------------------------------- extract audio

# containers that can hold a given codec without re-encoding
COPY_OK = {".m4a": {"aac", "alac"}, ".aac": {"aac"}, ".mp3": {"mp3"}, ".opus": {"opus"},
           ".ogg": {"vorbis", "opus", "flac"}, ".flac": {"flac"}, ".mka": None}


def cmd_extract_audio(a):
    src, out = check_io(a.input, a.output, a.force)
    info = probe(src)
    aud = stream(info, "audio")
    if not aud:
        raise ValueError("input has no audio stream")
    codec = aud.get("codec_name")
    ext = out.suffix.lower()
    allowed = COPY_OK.get(ext, set())
    copy = ext in COPY_OK and (allowed is None or codec in allowed)
    if copy:
        ffmpeg(["-i", str(src), "-map", "0:a:0", "-vn", "-c:a", "copy", str(out)])
    else:
        enc = {".wav": ["-c:a", "pcm_s16le"], ".flac": ["-c:a", "flac"], ".mp3": ["-c:a", "libmp3lame", "-q:a", "2"],
               ".m4a": ["-c:a", "aac", "-b:a", "192k"], ".aac": ["-c:a", "aac", "-b:a", "192k"],
               ".opus": ["-c:a", "libopus", "-b:a", "128k"], ".ogg": ["-c:a", "libvorbis", "-q:a", "5"]}
        if ext not in enc:
            raise ValueError(f"unsupported audio extension {ext}")
        ffmpeg(["-i", str(src), "-map", "0:a:0", "-vn", *enc[ext], str(out)])
    return receipt("extract-audio", src, out, source_codec=codec, copied=copy,
                   why="bit-exact stream copy" if copy else f"{ext} cannot hold {codec}, re-encoded")


# ---------------------------------------------------------------- cli

def cmd_doctor(_a):
    ff, fp = shutil.which("ffmpeg"), shutil.which("ffprobe")
    return {"schema": SCHEMA, "command": "doctor", "ffmpeg": ff, "ffprobe": fp, "ready": bool(ff and fp),
            "voice_presets": {k: v[2] for k, v in VOICE_PRESETS.items()}}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("doctor", help="check ffmpeg/ffprobe and list voice presets")

    k = sub.add_parser("keyframes", help="list video keyframe times")
    k.add_argument("--input", required=True)

    def io(p):
        p.add_argument("--input", required=True)
        p.add_argument("--output", required=True)
        p.add_argument("--force", action="store_true", help="replace an existing output file")

    def enc(p):
        p.add_argument("--crf", type=int, default=18)
        p.add_argument("--preset", default="medium")

    c = sub.add_parser("cut", help="cut [start, end) by stream copy or exact re-encode")
    io(c); enc(c)
    c.add_argument("--start", type=float, required=True)
    c.add_argument("--end", type=float)
    c.add_argument("--mode", choices=["auto", "copy", "exact"], default="auto")
    c.add_argument("--tolerance", type=float, default=0.1, help="largest copy drift auto accepts (s)")

    v = sub.add_parser("voice", help="apply a voice preset, keeping duration and sample rate")
    io(v)
    v.add_argument("--preset", required=True, choices=sorted(VOICE_PRESETS))

    b = sub.add_parser("brighten", help="lift a low-light clip and measure the gain")
    io(b); enc(b)
    b.add_argument("--strength", type=float, default=0.6)
    b.add_argument("--denoise", action="store_true")
    b.add_argument("--force-lift", action="store_true", help="brighten even when the clip is already bright")

    e = sub.add_parser("extract-audio", help="extract the first audio stream, bit-exact when possible")
    io(e)

    a = ap.parse_args(argv)
    fn = {"doctor": cmd_doctor, "keyframes": cmd_keyframes, "cut": cmd_cut, "voice": cmd_voice,
          "brighten": cmd_brighten, "extract-audio": cmd_extract_audio}[a.cmd]
    try:
        result = fn(a)
    except (ValueError, RuntimeError) as err:
        print(json.dumps({"schema": SCHEMA, "command": a.cmd, "error": str(err)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
