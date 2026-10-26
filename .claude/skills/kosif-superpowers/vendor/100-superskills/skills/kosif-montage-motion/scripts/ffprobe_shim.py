"""A stand-in for ffprobe built on ffmpeg alone — for sandboxes that only have an ffmpeg binary (the imageio-ffmpeg
wheel ships ffmpeg without ffprobe, as on claude.ai). It answers the calls this kit makes, in ffprobe's own formats:

    ffprobe -v error [-select_streams a|v|v:0|a:0] -show_entries stream=K,…:format=K,… -of json|csv=p=0|compact FILE
    ffprobe -v error -show_streams -show_format -of json FILE

Fields: format duration/size/format_name; stream index, codec_type, codec_name, profile, pix_fmt, width, height,
r_frame_rate, nb_frames, sample_rate, channels. Durations come from ffmpeg's header (1/100 s); nb_frames is counted
exactly by a stream-copy pass. Anything else is answered as absent, never invented.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from fractions import Fraction

STREAM_KEYS = ["index", "codec_name", "profile", "codec_type", "width", "height", "pix_fmt", "r_frame_rate", "nb_frames", "sample_rate", "channels"]
FORMAT_KEYS = ["filename", "format_name", "duration", "size"]
COMMON_RATES = {23.98: "24000/1001", 23.976: "24000/1001", 29.97: "30000/1001", 59.94: "60000/1001", 47.95: "48000/1001", 119.88: "120000/1001"}


def ffmpeg_exe() -> str:
    exe = os.environ.get("KOSIF_FFMPEG") or shutil.which("ffmpeg")
    if not exe:
        try:
            import imageio_ffmpeg
            exe = imageio_ffmpeg.get_ffmpeg_exe()
        except Exception:  # noqa: BLE001
            exe = None
    if not exe:
        sys.stderr.write("ffprobe_shim: no ffmpeg found (PATH, KOSIF_FFMPEG or imageio-ffmpeg)\n")
        sys.exit(1)
    return exe


def _rate(text: str) -> str | None:
    m = re.search(r"([\d.]+)(k?) fps", text) or re.search(r"([\d.]+)(k?) tbr", text)
    if not m:
        return None
    v = float(m.group(1)) * (1000 if m.group(2) else 1)
    for k, frac in COMMON_RATES.items():
        if abs(v - k) < 0.006:
            return frac
    f = Fraction(v).limit_denominator(1001)
    return f"{f.numerator}/{f.denominator}"


def _channels(text: str) -> int | None:
    for word, n in (("mono", 1), ("stereo", 2), ("2.1", 3), ("quad", 4), ("4.0", 4), ("5.0", 5), ("5.1", 6), ("6.1", 7), ("7.1", 8)):
        if re.search(rf"(?<![\w.]){re.escape(word)}(?![\w.])", text):
            return n
    m = re.search(r"(\d+) channels", text)
    return int(m.group(1)) if m else None


def parse(path: str) -> dict:
    """Header facts from `ffmpeg -i FILE`."""
    r = subprocess.run([ffmpeg_exe(), "-hide_banner", "-nostdin", "-i", path], capture_output=True, text=True, encoding="utf-8", errors="replace")
    err = r.stderr or ""
    if "Invalid data found" in err or "No such file" in err or "Input #0" not in err:
        sys.stderr.write(f"{path}: {err.strip().splitlines()[-1] if err.strip() else 'cannot open'}\n")
        sys.exit(1)
    fmt: dict = {"filename": path}
    m = re.search(r"Input #0, ([^,]+(?:,[^,\s]+)*), from", err)
    if m:
        fmt["format_name"] = m.group(1)
    m = re.search(r"Duration: (\d+):(\d+):(\d+(?:\.\d+)?)", err)
    if m:
        fmt["duration"] = f"{int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3)):.6f}"
    try:
        fmt["size"] = str(os.path.getsize(path))
    except OSError:
        pass
    streams = []
    for line in err.splitlines():
        m = re.match(r"\s*Stream #0:(\d+)(?:\[[^\]]*\])?(?:\([^)]*\))?: (Video|Audio|Subtitle|Data|Attachment): (.*)", line)
        if not m:
            continue
        idx, kind, rest = int(m.group(1)), m.group(2).lower(), m.group(3)
        s: dict = {"index": idx, "codec_type": kind}
        cm = re.match(r"([\w-]+)(?: \(([^)]*)\))?", rest)
        if cm:
            s["codec_name"] = cm.group(1)
            if cm.group(2) and "/" not in cm.group(2):
                s["profile"] = cm.group(2)
        if kind == "video":
            parts = [p.strip() for p in re.split(r",(?![^(]*\))", rest)]
            if len(parts) > 1:
                s["pix_fmt"] = parts[1].split("(")[0].strip()
            wh = re.search(r"(?<!\d)(\d{2,5})x(\d{2,5})(?!\d)", rest)
            if wh:
                s["width"], s["height"] = int(wh.group(1)), int(wh.group(2))
            rate = _rate(rest)
            if rate:
                s["r_frame_rate"] = rate
        elif kind == "audio":
            sr = re.search(r"(\d+) Hz", rest)
            if sr:
                s["sample_rate"] = sr.group(1)
            ch = _channels(rest)
            if ch:
                s["channels"] = ch
            s["r_frame_rate"] = "0/0"
        streams.append(s)
    return {"streams": streams, "format": fmt}


def count_frames(path: str, index: int) -> str | None:
    r = subprocess.run([ffmpeg_exe(), "-hide_banner", "-nostdin", "-i", path, "-map", f"0:{index}", "-c", "copy", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    hits = re.findall(r"frame=\s*(\d+)", r.stderr or "")
    if not hits:   # ffmpeg 6+ prints no frame= line for a stream-copy pass: decode instead
        r = subprocess.run([ffmpeg_exe(), "-hide_banner", "-nostdin", "-i", path, "-map", f"0:{index}", "-f", "null", "-"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        hits = re.findall(r"frame=\s*(\d+)", r.stderr or "")
    return hits[-1] if hits else None


def select(streams: list[dict], spec: str | None) -> list[dict]:
    if not spec:
        return streams
    kind = {"v": "video", "a": "audio", "s": "subtitle", "d": "data"}.get(spec.split(":")[0])
    out = [s for s in streams if kind is None or s["codec_type"] == kind]
    if ":" in spec:
        n = int(spec.split(":")[1])
        out = out[n:n + 1]
    return out


def parse_entries(spec: str) -> dict[str, list[str] | None]:
    """'stream=a,b:format=c' → {'stream': ['a','b'], 'format': ['c']}; a bare section name means all its keys."""
    want: dict[str, list[str] | None] = {}
    for part in spec.split(":"):
        if not part:
            continue
        name, _, keys = part.partition("=")
        want[name] = [k for k in keys.split(",") if k] or None
    return want


def main(argv: list[str]) -> int:
    path, of, sel, entries, show_streams, show_format = None, "default", None, None, False, False
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("-v", "-loglevel"):
            i += 2; continue
        if a == "-select_streams":
            sel = argv[i + 1]; i += 2; continue
        if a == "-show_entries":
            entries = parse_entries(argv[i + 1]); i += 2; continue
        if a in ("-of", "-print_format"):
            of = argv[i + 1]; i += 2; continue
        if a == "-show_streams":
            show_streams = True; i += 1; continue
        if a == "-show_format":
            show_format = True; i += 1; continue
        if a in ("-hide_banner", "-count_frames", "-pretty"):
            i += 1; continue
        if a.startswith("-"):
            i += 1; continue
        path = a; i += 1
    if not path:
        sys.stderr.write("ffprobe_shim: no input file\n"); return 1
    info = parse(path)
    want = entries or {}
    if show_streams:
        want.setdefault("stream", None)
    if show_format:
        want.setdefault("format", None)
    result: dict = {}
    if "stream" in want:
        keys = want["stream"] or STREAM_KEYS
        rows = []
        for s in select(info["streams"], sel):
            if "nb_frames" in keys and s["codec_type"] == "video":
                s["nb_frames"] = count_frames(path, s["index"])
            rows.append({k: s[k] for k in keys if k in s and s[k] is not None})
        result["streams"] = rows
    if "format" in want:
        keys = want["format"] or FORMAT_KEYS
        result["format"] = {k: info["format"][k] for k in keys if k in info["format"]}
    if of.startswith("json"):
        print(json.dumps(result, indent=4))
    elif of.startswith("csv") or of.startswith("default"):
        nokey = "p=0" in of or "nokey=1" in of or of.startswith("csv")
        for s in result.get("streams", []):
            print(",".join(str(v) for v in s.values()) if nokey else "\n".join(f"{k}={v}" for k, v in s.items()))
        if "format" in result:
            f = result["format"]
            print(",".join(str(v) for v in f.values()) if nokey else "\n".join(f"{k}={v}" for k, v in f.items()))
    elif of.startswith("compact"):
        for s in result.get("streams", []):
            print("stream|" + "|".join(f"{k}={v}" for k, v in s.items()))
        if "format" in result:
            print("format|" + "|".join(f"{k}={v}" for k, v in result["format"].items()))
    else:
        print(json.dumps(result, indent=4))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
