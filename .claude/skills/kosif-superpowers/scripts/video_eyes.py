#!/usr/bin/env python3
"""Video eyes / عيون الفيديو: turn a render into things a text model can read before anyone says "done".

A coding agent cannot watch a video or hear its soundtrack. This tool converts one into evidence it can check:
a contact strip of evenly spaced frames, an onion-skin image that shows the path and easing of a movement, a
per-second motion-energy timeline that flags frozen stretches (a "motion graphic" that is really a slide) and hard
cuts, and per-window loudness with silence and clipping. Idea from the 30-day GitHub pulse (GP-03:
dmtrKovalenko/fframes "your agent cannot watch the video", heygen-com/hyperframes preview loop); code is our own.

    python3 scripts/video_eyes.py strip  film.mp4 --out strip.png [--frames 12] [--cols 4] [--width 320]
    python3 scripts/video_eyes.py onion  film.mp4 --start 1.0 --end 2.0 --out onion.png [--frames 8]
    python3 scripts/video_eyes.py motion film.mp4 [--fps 10] [--freeze 1.5] [--json]
    python3 scripts/video_eyes.py audio  film.mp4 [--window 1.0] [--json]
    python3 scripts/video_eyes.py report film.mp4 --out <dir>      # all four + report.json + REPORT.md
    python3 scripts/video_eyes.py --self-test                       # builds a synthetic clip with ffmpeg

Needs ffmpeg and ffprobe on PATH. Exit codes: 0 ok, 3 = REVIEW (a frozen stretch longer than --freeze, clipping, or
long silence was found), 1 = error. The numbers say where to look; a human still watches the film before delivery.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def need_ffmpeg():
    if not (shutil.which("ffmpeg") and shutil.which("ffprobe")):
        raise RuntimeError("ffmpeg/ffprobe not found on PATH (apt install ffmpeg)")


def probe(path: Path) -> dict:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,width,height,r_frame_rate",
                          "-of", "json", str(path)], capture_output=True, text=True, check=True).stdout
    d = json.loads(out)
    v = next((s for s in d.get("streams", []) if s.get("codec_type") == "video"), {})
    num, _, den = (v.get("r_frame_rate") or "0/1").partition("/")
    fps = float(num) / float(den or 1) if float(den or 1) else 0.0
    return {"duration": float(d.get("format", {}).get("duration") or 0), "width": v.get("width"), "height": v.get("height"),
            "fps": round(fps, 3), "has_audio": any(s.get("codec_type") == "audio" for s in d.get("streams", []))}


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd[:4])}…: {r.stderr.strip()[-400:]}")
    return r


# ---------------------------------------------------------------- strip and onion

def strip(path: Path, out: Path, frames: int = 12, cols: int = 4, width: int = 320) -> dict:
    info = probe(path)
    dur = max(info["duration"], 0.04)
    rows = math.ceil(frames / cols)
    times = [round(dur * (i + 0.5) / frames, 3) for i in range(frames)]
    rate = frames / dur
    run(["ffmpeg", "-v", "error", "-y", "-i", str(path), "-vf",
         f"fps={rate:.6f},scale={width}:-2,tile={cols}x{rows}:padding=4:margin=4:color=0x202020",
         "-frames:v", "1", str(out)])
    return {"image": str(out), "frames": frames, "cols": cols, "times": times,
            "read_as": "left to right, top to bottom; frame i is at times[i] seconds"}


def onion(path: Path, start: float, end: float, out: Path, frames: int = 8, width: int = 640) -> dict:
    if end <= start:
        raise ValueError("--end must be after --start")
    span = end - start
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{start:.3f}", "-t", f"{span:.3f}", "-i", str(path), "-vf",
         f"fps={frames / span:.6f},scale={width}:-2,tmix=frames={frames}", "-frames:v", "1", "-update", "1", str(out)])
    return {"image": str(out), "start": start, "end": end, "frames_blended": frames,
            "read_as": "ghosted copies = positions over time; even spacing = linear, bunched at one end = easing"}


# ---------------------------------------------------------------- motion energy

def gray_frames(path: Path, fps: float, w: int = 64):
    """Yield (t, bytes) of small grayscale frames."""
    info = probe(path)
    h = max(2, int(round(w * (info["height"] or 9) / (info["width"] or 16) / 2) * 2))
    proc = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"fps={fps},scale={w}:{h},format=gray",
                             "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    size, i = w * h, 0
    try:
        while True:
            buf = proc.stdout.read(size)
            if len(buf) < size:
                break
            yield round(i / fps, 3), buf
            i += 1
    finally:
        proc.stdout.close()
        proc.wait()


def motion(path: Path, fps: float = 10.0, freeze: float = 1.5, still: float = 0.6, cut: float = 25.0) -> dict:
    """Per-frame mean absolute difference (0-255). still: below = no visible change; cut: above = hard cut."""
    diffs, prev = [], None
    for t, buf in gray_frames(path, fps):
        if prev is not None:
            diffs.append((t, sum(abs(a - b) for a, b in zip(buf, prev)) / len(buf)))
        prev = buf
    per_sec = {}
    for t, d in diffs:
        per_sec.setdefault(int(t), []).append(d)
    timeline = [{"second": s, "energy": round(sum(v) / len(v), 2), "peak": round(max(v), 2)} for s, v in sorted(per_sec.items())]
    frozen, run_start = [], None
    for t, d in diffs + [(diffs[-1][0] + 1 / fps if diffs else 0, 999)]:
        if d < still and run_start is None:
            run_start = t - 1 / fps
        elif d >= still and run_start is not None:
            if t - run_start >= freeze:
                frozen.append({"from": round(max(0, run_start), 2), "to": round(t - 1 / fps, 2),
                               "seconds": round(t - 1 / fps - run_start, 2)})
            run_start = None
    cuts = [round(t, 2) for t, d in diffs if d >= cut]
    moving = sum(1 for _, d in diffs if d >= still) / max(1, len(diffs))
    return {"fps_sampled": fps, "frames": len(diffs) + 1, "share_moving": round(moving, 3), "timeline": timeline,
            "frozen": frozen, "cuts": cuts, "thresholds": {"still": still, "cut": cut, "freeze_seconds": freeze}}


# ---------------------------------------------------------------- audio

def audio(path: Path, window: float = 1.0, silence_db: float = -50.0, min_silence: float = 1.0) -> dict:
    info = probe(path)
    if not info["has_audio"]:
        return {"has_audio": False}
    r = run(["ffmpeg", "-v", "info", "-nostats", "-i", str(path), "-vn", "-af",
             f"ebur128=peak=true,silencedetect=noise={silence_db}dB:d={min_silence}", "-f", "null", "-"])
    err = r.stderr
    mom = [(float(t), float(m)) for t, m in re.findall(r"t:\s*([\d.]+)\s+TARGET.*?M:\s*(-?[\d.]+|-inf)", err)
           if m != "-inf"]
    windows = {}
    for t, m in mom:
        windows.setdefault(int(t // window), []).append(m)
    per = [{"from": round(k * window, 2), "to": round((k + 1) * window, 2),
            "momentary_lufs": round(10 * math.log10(sum(10 ** (m / 10) for m in v) / len(v)), 1)}
           for k, v in sorted(windows.items())]
    integ = re.search(r"Integrated loudness:\s*I:\s*(-?[\d.]+)", err)
    peak = re.search(r"True peak:\s*Peak:\s*(-?[\d.]+|-inf)", err)
    starts = [float(x) for x in re.findall(r"silence_start:\s*(-?[\d.]+)", err)]
    ends = [float(x) for x in re.findall(r"silence_end:\s*(-?[\d.]+)", err)]
    silences = [{"from": round(max(0, s), 2), "to": round(e, 2), "seconds": round(e - max(0, s), 2)}
                for s, e in zip(starts, ends + [info["duration"]] * (len(starts) - len(ends)))]
    tp = float(peak.group(1)) if peak and peak.group(1) != "-inf" else None
    return {"has_audio": True, "integrated_lufs": float(integ.group(1)) if integ else None, "true_peak_dbtp": tp,
            "clipping_risk": tp is not None and tp > -1.0, "silences": silences, "windows": per}


# ---------------------------------------------------------------- report

def verdict(mot: dict, aud: dict, duration: float) -> list:
    flags = []
    for f in mot.get("frozen", []):
        flags.append(f"frozen {f['seconds']}s at {f['from']}-{f['to']}s: is this a held beat or a static slide?")
    if mot.get("share_moving", 1) < 0.5:
        flags.append(f"only {int(mot['share_moving'] * 100)}% of sampled frames change: motion graphics should move")
    if aud.get("clipping_risk"):
        flags.append(f"true peak {aud['true_peak_dbtp']} dBTP > -1: risk of clipping after platform encoding")
    for s in aud.get("silences", []):
        if s["seconds"] >= 2 and not (s["from"] <= 0.1 or s["to"] >= duration - 0.1):
            flags.append(f"silence {s['seconds']}s at {s['from']}-{s['to']}s inside the film")
    return flags


def report(path: Path, out: Path) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    info = probe(path)
    res = {"input": str(path), "probe": info,
           "strip": strip(path, out / "strip.png"),
           "motion": motion(path)}
    res["audio"] = audio(path)
    mid = info["duration"] / 2
    res["onion"] = onion(path, max(0, mid - 0.5), min(info["duration"], mid + 0.5), out / "onion_mid.png")
    res["flags"] = verdict(res["motion"], res["audio"], info["duration"])
    (out / "report.json").write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    md = [f"# Video eyes — {path.name}", "",
          f"{info['width']}x{info['height']} · {info['fps']} fps · {info['duration']:.2f}s · audio: {info['has_audio']}", "",
          "## Flags", ""] + ([f"- {f}" for f in res["flags"]] or ["- none"]) + [
          "", "## Motion energy per second (0-255 mean change)", "",
          " ".join(f"{t['second']}s:{t['energy']}" for t in res["motion"]["timeline"]), "",
          f"Hard cuts at: {', '.join(map(str, res['motion']['cuts'])) or 'none'}", "",
          "## Audio", ""]
    if res["audio"].get("has_audio"):
        md += [f"Integrated {res['audio']['integrated_lufs']} LUFS · true peak {res['audio']['true_peak_dbtp']} dBTP", "",
               " ".join(f"{w['from']:g}s:{w['momentary_lufs']}" for w in res["audio"]["windows"])]
    else:
        md.append("no audio stream")
    md += ["", "## Images", "", "- `strip.png`: " + res["strip"]["read_as"], "- `onion_mid.png`: " + res["onion"]["read_as"], ""]
    (out / "REPORT.md").write_text("\n".join(md), encoding="utf-8")
    return res


# ---------------------------------------------------------------- self-test

def self_test() -> int:
    need_ffmpeg()
    ok = True
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        clip = td / "t.mp4"
        # 2 s moving test pattern, then 2 s frozen (cloned last frame), audio: 2 s tone then 2 s silence
        run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=size=320x180:rate=25:duration=2",
             "-f", "lavfi", "-i", "sine=frequency=440:duration=2:sample_rate=48000",
             "-filter_complex", "[0:v]tpad=stop_mode=clone:stop_duration=2[v];[1:a]apad=whole_dur=4[a]",
             "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-t", "4", str(clip)])
        m = motion(clip, fps=10, freeze=1.0)
        if not m["frozen"] or m["frozen"][0]["from"] > 2.3 or m["frozen"][0]["seconds"] < 1.5:
            ok = False
            print("FAIL frozen detection", m["frozen"])
        if not (0.3 < m["share_moving"] < 0.7):
            ok = False
            print("FAIL share moving", m["share_moving"])
        a = audio(clip, silence_db=-50, min_silence=1.0)
        if not a["has_audio"] or not a["silences"] or a["integrated_lufs"] is None:
            ok = False
            print("FAIL audio", {k: a.get(k) for k in ("integrated_lufs", "silences")})
        res = report(clip, td / "rep")
        for f in ("strip.png", "onion_mid.png", "report.json", "REPORT.md"):
            if not (td / "rep" / f).is_file():
                ok = False
                print("FAIL missing", f)
        if not any("frozen" in f for f in res["flags"]):
            ok = False
            print("FAIL flags", res["flags"])
    print("self-test ok" if ok else "self-test FAILED")
    return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--self-test", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    s = sub.add_parser("strip")
    s.add_argument("video", type=Path)
    s.add_argument("--out", type=Path, required=True)
    s.add_argument("--frames", type=int, default=12)
    s.add_argument("--cols", type=int, default=4)
    s.add_argument("--width", type=int, default=320)
    o = sub.add_parser("onion")
    o.add_argument("video", type=Path)
    o.add_argument("--start", type=float, required=True)
    o.add_argument("--end", type=float, required=True)
    o.add_argument("--out", type=Path, required=True)
    o.add_argument("--frames", type=int, default=8)
    m = sub.add_parser("motion")
    m.add_argument("video", type=Path)
    m.add_argument("--fps", type=float, default=10.0)
    m.add_argument("--freeze", type=float, default=1.5)
    m.add_argument("--json", action="store_true")
    a = sub.add_parser("audio")
    a.add_argument("video", type=Path)
    a.add_argument("--window", type=float, default=1.0)
    a.add_argument("--json", action="store_true")
    r = sub.add_parser("report")
    r.add_argument("video", type=Path)
    r.add_argument("--out", type=Path, required=True)
    args = ap.parse_args(argv)
    try:
        if args.self_test:
            return self_test()
        need_ffmpeg()
        if args.cmd and not args.video.is_file():
            print(f"not found: {args.video}", file=sys.stderr)
            return 1
        if args.cmd == "strip":
            print(json.dumps(strip(args.video, args.out, args.frames, args.cols, args.width), indent=1))
            return 0
        if args.cmd == "onion":
            print(json.dumps(onion(args.video, args.start, args.end, args.out, args.frames), indent=1))
            return 0
        if args.cmd == "motion":
            res = motion(args.video, args.fps, args.freeze)
            if args.json:
                print(json.dumps(res, indent=1))
            else:
                print(f"moving frames: {int(res['share_moving'] * 100)}%   cuts: {res['cuts'] or 'none'}")
                print("energy/s: " + " ".join(f"{t['second']}s:{t['energy']}" for t in res["timeline"]))
                for f in res["frozen"]:
                    print(f"FROZEN {f['from']}-{f['to']}s ({f['seconds']}s)")
            return 3 if res["frozen"] else 0
        if args.cmd == "audio":
            res = audio(args.video, args.window)
            print(json.dumps(res, indent=1) if args.json else
                  f"integrated {res.get('integrated_lufs')} LUFS, true peak {res.get('true_peak_dbtp')} dBTP, "
                  f"silences {res.get('silences')}")
            return 3 if res.get("clipping_risk") else 0
        if args.cmd == "report":
            res = report(args.video, args.out)
            print(f"wrote {args.out}/REPORT.md, report.json, strip.png, onion_mid.png")
            for f in res["flags"]:
                print("FLAG", f)
            return 3 if res["flags"] else 0
    except (RuntimeError, ValueError, subprocess.CalledProcessError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
