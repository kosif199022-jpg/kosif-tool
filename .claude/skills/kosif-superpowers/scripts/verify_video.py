#!/usr/bin/env python3
"""Delivery gate: verify a rendered video against the request and fill TEST_REPORT values.

Checks with ffprobe/ffmpeg (both must be on PATH):
  - container and codecs (H.264 + AAC expected by default)
  - width × height and aspect ratio
  - frame rate and frame count versus the requested duration
  - audio stream presence, channels, sample rate
  - integrated loudness (EBU R128) and true peak, versus a target (default -14 LUFS)
  - optional: the delivered audio duration matches a supplied master audio file (±50 ms)
  - optional: the delivered audio is the untouched source audio (--source-audio): the MD5 of the first
    audio stream's packets (`ffmpeg -i X -map 0:a:0 -c copy -f md5 -`) must equal the source's. AAC is
    hashed through `-bsf:a aac_adtstoasc` on both sides, so a raw ADTS .aac source muxed into MP4/MOV/MKV
    with -c copy (which strips the 7-byte ADTS headers) still matches; other codecs are hashed as they are.
    The deliverable must also carry no other audio stream (an extra track is not covered by the hash).
    When both hold, the source is "preserved": loudness and true peak (measured on that stream) become
    [INFO] "source preserved: … (not normalised by design)" lines that never fail, and so do a sample rate
    under 44.1 kHz ("not resampled") and an MP3 codec ("not re-encoded"; MP3 is the one non-AAC codec
    accepted in a delivery MP4). Any other non-AAC codec (Opus, FLAC, PCM…) still fails: carrying it
    untouched does not make it play everywhere. On a mismatch or an extra stream, every check is scored
    as usual. A -c copy mux keeps the packets identical; any re-encode (even AAC to AAC) or a cut such as
    -shortest dropping the last packet changes them.

Usage:
  python3 tools/verify_video.py film.mp4 --aspect 9:16 --fps 30 --duration 15 [--audio voice.mp3] [--lufs -14] [--json report.json]
  python3 tools/verify_video.py reel.mp4 --aspect 9:16 --fps 30 --duration 15 --source-audio voice.m4a [--json report.json]
Console lines are [PASS], [FAIL] or [INFO]; the summary scores PASS/FAIL only ("N/M checks passed", plus
", K info (not scored)" when there are INFO lines). JSON "checks" entries are {"check", "pass", "value"};
with --source-audio every entry also has "status": "PASS" | "FAIL" | "INFO". Read "status" (or the exit code):
an INFO entry keeps "pass": true so it is never counted as a failure, but it was not scored either.
--source-audio also adds "source_audio": {"md5_match", "video_md5", "source_md5"} (md5_match compares the
first audio stream only; the "one audio stream" check covers the rest).
Exit code 1 when any check fails (INFO never does); 2 when an input cannot be read (missing or unreadable video,
--audio master or --source-audio file, a --source-audio file without an audio stream, unreadable --aspect)
or ffprobe/ffmpeg is missing.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from aspects import ratio_of  # noqa: E402  (any W:H, WxH or name)


class InputError(Exception):
    """An input file ffprobe cannot read; reported as one line, exit 2."""


def probe(path: str) -> dict:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_format", "-show_streams", "-count_frames", "-of", "json", path], capture_output=True, text=True)
    if out.returncode != 0:
        reason = (out.stderr.strip().splitlines() or [f"ffprobe exit status {out.returncode}"])[-1]
        raise InputError(f"cannot read input: {reason if path in reason else f'{path}: {reason}'}")
    try:
        return json.loads(out.stdout)
    except ValueError:
        raise InputError(f"cannot read input: {path}: ffprobe returned no JSON") from None


def packet_md5(path: str, codec: str | None) -> str | None:
    """MD5 of the first audio stream's packets, stream-copied (no decode); None when ffmpeg cannot produce it.
    AAC goes through aac_adtstoasc: it strips ADTS headers (raw .aac, MPEG-TS) the way an MP4/MOV/MKV mux does and
    passes MP4-style AAC through unchanged. Only AAC: the filter refuses every other codec."""
    bsf = ["-bsf:a", "aac_adtstoasc"] if codec == "aac" else []
    out = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-map", "0:a:0", "-c", "copy", *bsf, "-f", "md5", "-"], capture_output=True, text=True)
    m = re.search(r"MD5=([0-9a-f]{32})", out.stdout)
    return m.group(1) if out.returncode == 0 and m else None


def source_md5(path: str) -> str:
    """--source-audio: packet MD5 of a readable file with an audio stream; anything else is an InputError (exit 2)."""
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=codec_name", "-of", "csv=p=0", path], capture_output=True, text=True)
    if out.returncode != 0:
        reason = (out.stderr.strip().splitlines() or [f"ffprobe exit status {out.returncode}"])[-1]
        raise InputError(f"cannot read input: {reason if path in reason else f'{path}: {reason}'}")
    if not out.stdout.strip():
        raise InputError(f"cannot read input: {path}: no audio stream to compare with")
    md5 = packet_md5(path, out.stdout.strip().splitlines()[0].split(",")[0].strip())
    if not md5:
        raise InputError(f"cannot read input: {path}: its audio packets cannot be hashed")
    return md5


def aspect_spec(value: str) -> str:
    """argparse type: keep the user's spelling, reject a spec aspects.py cannot read."""
    try:
        ratio_of(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from None
    return value


def loudness(path: str, stream: str | None = None) -> dict | None:
    """EBU R128 of ffmpeg's default audio stream, or of `stream` (e.g. 0:a:0) when given."""
    pick = ["-map", stream] if stream else []
    try:
        out = subprocess.run(["ffmpeg", "-nostats", "-i", path, *pick, "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    except FileNotFoundError:
        return None
    text = out.stderr
    i = text.rfind("Integrated loudness")
    if i < 0:
        return None
    tail = text[i:]
    li = re.search(r"I:\s*(-?[\d.]+) LUFS", tail)
    lra = re.search(r"LRA:\s*(-?[\d.]+) LU", tail)
    peak = re.search(r"Peak:\s*(-?[\d.]+) dBFS", tail)
    return {"integrated_lufs": float(li.group(1)) if li else None, "lra": float(lra.group(1)) if lra else None, "true_peak_dbfs": float(peak.group(1)) if peak else None}


def frac(s: str) -> float:
    if "/" in s:
        a, b = s.split("/")
        return float(a) / float(b) if float(b) else 0.0
    return float(s)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--aspect", type=aspect_spec, help="any ratio: 9:16, 21:9, 2.35:1, 1920x816, reel, cinema…")
    ap.add_argument("--fps", type=float)
    ap.add_argument("--duration", type=float, help="expected duration in seconds")
    ap.add_argument("--audio", help="master audio file whose duration the video must match")
    ap.add_argument("--lufs", type=float, default=-14.0, help="target integrated loudness (±1.5 LU accepted)")
    ap.add_argument("--no-audio", action="store_true", help="the deliverable is intentionally silent")
    ap.add_argument("--source-audio", help="file (audio or video) whose audio packets the deliverable must carry unchanged (packet MD5, "
                    "ADTS-normalised for AAC) as its only audio stream; when it does, loudness, true peak, a sample rate "
                    "under 44.1 kHz and an MP3 codec are INFO, not normalised by design")
    ap.add_argument("--json", help="write the report as JSON here")
    args = ap.parse_args()
    if args.source_audio and args.no_audio:
        ap.error("--source-audio needs an audio stream; it cannot be combined with --no-audio")
    for tool in ("ffprobe", "ffmpeg"):
        if not shutil.which(tool):
            print(f"{tool} not found on PATH", file=sys.stderr)
            return 2

    try:
        return run_checks(args)
    except InputError as exc:
        print(exc, file=sys.stderr)
        return 2


def run_checks(args: argparse.Namespace) -> int:
    master = probe(args.audio) if args.audio else None  # fail fast on a bad master before the long frame count
    src_md5 = source_md5(args.source_audio) if args.source_audio else None  # likewise for the source audio
    info = probe(args.video)
    v = next((s for s in info["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    checks: list[tuple[str, bool | None, str]] = []  # ok None = INFO: reported, never scored
    report: dict = {"file": args.video}
    if not v:
        print("no video stream", file=sys.stderr)
        return 1
    w, h = int(v["width"]), int(v["height"])
    fps = frac(v.get("avg_frame_rate") or v.get("r_frame_rate") or "0")
    frames = int(v.get("nb_read_frames") or v.get("nb_frames") or 0)
    dur = float(info["format"].get("duration") or 0)
    report.update({"codec": v.get("codec_name"), "width": w, "height": h, "fps": round(fps, 3), "frames": frames, "duration_s": round(dur, 3), "pix_fmt": v.get("pix_fmt")})
    checks.append(("video codec is H.264", v.get("codec_name") == "h264", v.get("codec_name", "?")))
    checks.append(("pixel format is 4:2:0 8-bit (universal playback)", v.get("pix_fmt") in ("yuv420p", "yuvj420p"), v.get("pix_fmt", "?")))
    checks.append(("even dimensions", w % 2 == 0 and h % 2 == 0, f"{w}x{h}"))
    if args.aspect:
        checks.append((f"aspect is {args.aspect}", abs(w / h - ratio_of(args.aspect)) < 0.01, f"{w}x{h} = {w / h:.3f}"))
    if args.fps:
        checks.append((f"frame rate is {args.fps:g}", abs(fps - args.fps) < 0.05, f"{fps:.3f}"))
    if args.duration:
        checks.append((f"duration is {args.duration:g} s (±1 frame)", abs(dur - args.duration) <= (1 / fps if fps else 0.05) + 0.001, f"{dur:.3f} s"))
        if fps:
            checks.append(("frame count matches duration × fps", abs(frames - round(args.duration * fps)) <= 1, f"{frames} frames"))
    if args.no_audio:
        checks.append(("no audio stream (silent deliverable)", a is None, "present" if a else "absent"))
    else:
        checks.append(("audio stream present", a is not None, a.get("codec_name", "?") if a else "absent"))
        source = None
        n_audio = sum(s.get("codec_type") == "audio" for s in info["streams"])
        if src_md5:
            vmd5 = packet_md5(args.video, a.get("codec_name")) if a else None
            source = {"md5_match": vmd5 == src_md5, "video_md5": vmd5, "source_md5": src_md5}
            same = (f"{vmd5} = source" if source["md5_match"] else f"video {vmd5} ≠ source {src_md5}") if vmd5 else \
                ("no audio stream in the video" if not a else "video audio packets cannot be hashed")
        # untouched source audio and nothing beside it: its loudness, peak, low rate or MP3 codec are facts, not targets
        preserved = bool(source and source["md5_match"] and n_audio == 1)

        def scored(ok: bool, value: str, why: str = "not normalised by design") -> tuple[bool | None, str]:
            return (None, f"source preserved: {value} ({why})") if preserved else (ok, value)

        if source and not a:
            checks.append(("audio identical to source (packet MD5)", False, same))
        if a:
            report.update({"audio_codec": a.get("codec_name"), "channels": a.get("channels"), "sample_rate": a.get("sample_rate")})
            codec, rate = a.get("codec_name", "?"), str(a.get("sample_rate"))
            if codec == "mp3":
                checks.append(("audio codec is AAC", *scored(False, codec, "not re-encoded by design")))
            else:
                checks.append(("audio codec is AAC", codec == "aac", codec if codec == "aac" or not preserved else
                               f"{codec}: source preserved, but only AAC or MP3 is accepted for delivery"))
            if int(a.get("sample_rate") or 0) < 44100:
                checks.append(("sample rate ≥ 44.1 kHz", *scored(False, rate, "not resampled by design")))
            else:
                checks.append(("sample rate ≥ 44.1 kHz", True, rate))
            if source:
                checks.append(("audio identical to source (packet MD5)", source["md5_match"], same))
                checks.append(("one audio stream (nothing beside the source)", n_audio == 1, "1 audio stream" if n_audio == 1 else
                               f"{n_audio} audio streams: only the first is compared with the source"))
            lu = loudness(args.video, "0:a:0" if source else None)  # with --source-audio: the stream that was hashed
            if lu:
                report["loudness"] = lu
                if lu.get("integrated_lufs") is not None:
                    checks.append((f"integrated loudness {args.lufs:g} LUFS ±1.5", *scored(abs(lu["integrated_lufs"] - args.lufs) <= 1.5, f"{lu['integrated_lufs']} LUFS")))
                if lu.get("true_peak_dbfs") is not None:
                    checks.append(("true peak ≤ -1 dBFS", *scored(lu["true_peak_dbfs"] <= -1.0, f"{lu['true_peak_dbfs']} dBFS")))
            if master is not None:
                mdur = float(master["format"].get("duration") or 0)
                adur = float(a.get("duration") or dur)
                report["master_audio_s"] = round(mdur, 3)
                checks.append(("delivered audio length matches master (±50 ms)", abs(adur - mdur) <= 0.05, f"{adur:.3f} vs {mdur:.3f}"))
        if source:
            report["source_audio"] = source

    # with --source-audio every entry carries "status"; INFO keeps "pass": true so a consumer counting falsy "pass" never
    # sees it as a failure. Without the flag no INFO can occur and the entries keep their original three keys.
    report["checks"] = [{"check": c, "pass": ok is not False, "value": val, "status": "INFO" if ok is None else "PASS" if ok else "FAIL"}
                        if args.source_audio or ok is None else {"check": c, "pass": ok, "value": val} for c, ok, val in checks]
    width = max(len(c) for c, _, _ in checks)
    for c, ok, val in checks:
        print(f"[{'INFO' if ok is None else 'PASS' if ok else 'FAIL'}] {c.ljust(width)}  {val}")
    failed = [c for c, ok, _ in checks if ok is not None and not ok]
    n_info = sum(ok is None for _, ok, _ in checks)
    print(f"\n{len(checks) - n_info - len(failed)}/{len(checks) - n_info} checks passed" + (f", {n_info} info (not scored)" if n_info else ""))
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=1)
    return 1 if failed else 0


if __name__ == "__main__":
    # UTF-8 is the output contract, including when Windows defaults to cp1256.
    # Capturing callers must decode stdout/stderr as UTF-8.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="backslashreplace")
    sys.exit(main())
