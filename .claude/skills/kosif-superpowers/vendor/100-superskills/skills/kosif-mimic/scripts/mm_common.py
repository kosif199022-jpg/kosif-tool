"""Shared helpers for the mimic skill: ffmpeg discovery, probing, process running, JSON I/O, timing.

Everything here is standard library only, so the other modules can import it on any machine.
"""
from __future__ import annotations

import json
import math
import os
import re
import shutil
import subprocess
import sys
import time
from fractions import Fraction
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
ASSETS = SKILL_ROOT / "assets"
VERBOSE = os.environ.get("MIMIC_QUIET") != "1"


def log(*parts):
    if VERBOSE:
        print("[mimic]", *parts, file=sys.stderr, flush=True)


def die(msg: str, code: int = 2):
    print(f"[mimic] ERROR: {msg}", file=sys.stderr, flush=True)
    raise SystemExit(code)


# --------------------------------------------------------------------------- binaries

def _candidates(name: str):
    env = os.environ.get(name.upper())
    if env:
        yield env
    found = shutil.which(name)
    if found:
        yield found
    for d in (Path.home() / "kosif-motion" / "bin", Path("/usr/local/bin"), Path("/usr/bin")):
        for ext in ("", ".exe"):
            p = d / f"{name}{ext}"
            if p.exists():
                yield str(p)
    if name == "ffmpeg":
        try:
            import imageio_ffmpeg  # type: ignore
            yield imageio_ffmpeg.get_ffmpeg_exe()
        except Exception:
            pass


_BIN_CACHE: dict[str, str | None] = {}


def which(name: str) -> str | None:
    if name not in _BIN_CACHE:
        _BIN_CACHE[name] = next(iter(_candidates(name)), None)
    return _BIN_CACHE[name]


def ffmpeg() -> str:
    exe = which("ffmpeg")
    if not exe:
        die("ffmpeg was not found. Install it (or set FFMPEG=/path/to/ffmpeg).")
    return exe


def run(cmd: list[str], check: bool = True, capture: bool = True, timeout: float | None = None,
        quiet: bool = False) -> subprocess.CompletedProcess:
    if not quiet:
        log("run:", " ".join(_short(c) for c in cmd[:14]) + (" …" if len(cmd) > 14 else ""))
    proc = subprocess.run(cmd, stdout=subprocess.PIPE if capture else None,
                          stderr=subprocess.PIPE if capture else None, timeout=timeout)
    if check and proc.returncode != 0:
        tail = (proc.stderr or b"").decode("utf-8", "replace")[-2500:]
        raise RuntimeError(f"command failed ({proc.returncode}): {' '.join(cmd[:8])} …\n{tail}")
    return proc


def _short(s: str, n: int = 90) -> str:
    s = str(s)
    return s if len(s) <= n else s[: n - 1] + "…"


# --------------------------------------------------------------------------- probing

def parse_rate(s: str | None) -> Fraction | None:
    if not s or s in ("0/0", "N/A"):
        return None
    try:
        if "/" in s:
            a, b = s.split("/", 1)
            if int(b) == 0:
                return None
            return Fraction(int(a), int(b))
        return Fraction(s).limit_denominator(1001)
    except Exception:
        return None


def nice_fps(fr: Fraction | None) -> Fraction:
    """Snap a measured frame rate to the usual broadcast/phone values."""
    if not fr or fr <= 0:
        return Fraction(30)
    common = [Fraction(24000, 1001), Fraction(24), Fraction(25), Fraction(30000, 1001), Fraction(30),
              Fraction(48), Fraction(50), Fraction(60000, 1001), Fraction(60), Fraction(15), Fraction(12)]
    best = min(common, key=lambda c: abs(float(c) - float(fr)))
    if abs(float(best) - float(fr)) / float(best) < 0.004:
        return best
    return fr.limit_denominator(1001)


def probe(path: str | Path) -> dict:
    """Return {'w','h','fps'(Fraction),'duration','frames','has_audio','audio':{...},'rotation'}."""
    path = str(path)
    fp = which("ffprobe")
    info: dict = {"path": path}
    if fp:
        out = run([fp, "-v", "error", "-print_format", "json", "-show_streams", "-show_format", path],
                  quiet=True).stdout.decode("utf-8", "replace")
        data = json.loads(out or "{}")
        vs = [s for s in data.get("streams", []) if s.get("codec_type") == "video"
              and not (s.get("disposition") or {}).get("attached_pic")]
        aus = [s for s in data.get("streams", []) if s.get("codec_type") == "audio"]
        fmt = data.get("format", {})
        if vs:
            v = vs[0]
            w, h = int(v.get("width", 0)), int(v.get("height", 0))
            rot = 0
            try:
                rot = int(float((v.get("tags") or {}).get("rotate", 0)))
            except Exception:
                rot = 0
            for sd in v.get("side_data_list", []) or []:
                if "rotation" in sd:
                    try:
                        rot = int(float(sd["rotation"]))
                    except Exception:
                        pass
            if abs(rot) % 180 == 90:
                w, h = h, w
            fps = parse_rate(v.get("avg_frame_rate")) or parse_rate(v.get("r_frame_rate"))
            info.update(w=w, h=h, rotation=rot, fps=nice_fps(fps), codec=v.get("codec_name"),
                        pix_fmt=v.get("pix_fmt"), vbitrate=_int(v.get("bit_rate")),
                        nb_frames=_int(v.get("nb_frames")))
            vdur = _float(v.get("duration"))
        else:
            info.update(w=0, h=0, fps=Fraction(30), rotation=0)
            vdur = None
        info["duration"] = vdur or _float(fmt.get("duration")) or 0.0
        info["format_duration"] = _float(fmt.get("duration")) or info["duration"]
        info["has_audio"] = bool(aus)
        if aus:
            a = aus[0]
            info["audio"] = {"codec": a.get("codec_name"), "sr": _int(a.get("sample_rate")),
                             "channels": _int(a.get("channels")), "bitrate": _int(a.get("bit_rate")),
                             "duration": _float(a.get("duration"))}
        return info
    # Fallback: parse `ffmpeg -i` banner.
    proc = subprocess.run([ffmpeg(), "-hide_banner", "-i", path], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    txt = proc.stderr.decode("utf-8", "replace")
    m = re.search(r"Duration:\s*(\d+):(\d+):([\d.]+)", txt)
    info["duration"] = (int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))) if m else 0.0
    info["format_duration"] = info["duration"]
    m = re.search(r"Video:.*?(\d{2,5})x(\d{2,5})", txt)
    info["w"], info["h"] = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
    m = re.search(r"([\d.]+) fps", txt)
    info["fps"] = nice_fps(Fraction(m.group(1)).limit_denominator(1001) if m else None)
    m = re.search(r"rotate\s*:\s*(-?\d+)", txt) or re.search(r"rotation of (-?[\d.]+)", txt)
    rot = int(float(m.group(1))) if m else 0
    if abs(rot) % 180 == 90:
        info["w"], info["h"] = info["h"], info["w"]
    info["rotation"] = rot
    am = re.search(r"Audio:\s*(\w+)[^,]*,\s*(\d+) Hz", txt)
    info["has_audio"] = bool(am)
    if am:
        info["audio"] = {"codec": am.group(1), "sr": int(am.group(2))}
    return info


def _int(v):
    try:
        return int(v)
    except Exception:
        return None


def _float(v):
    try:
        f = float(v)
        return f if math.isfinite(f) else None
    except Exception:
        return None


# --------------------------------------------------------------------------- time helpers

def fps_str(fps: Fraction) -> str:
    return f"{fps.numerator}/{fps.denominator}"


def t2f(t: float, fps: Fraction) -> int:
    """Seconds → nearest frame index."""
    return int(round(t * float(fps)))


def f2t(n: int, fps: Fraction) -> float:
    return float(n / fps)


def tc(t: float) -> str:
    """Seconds → m:ss.cc (for humans)."""
    if t is None:
        return "-"
    m = int(t // 60)
    return f"{m}:{t - 60 * m:05.2f}"


# --------------------------------------------------------------------------- json

class _Enc(json.JSONEncoder):
    def default(self, o):
        try:
            import numpy as np  # noqa
            if isinstance(o, (np.integer,)):
                return int(o)
            if isinstance(o, (np.floating,)):
                return round(float(o), 5)
            if isinstance(o, np.ndarray):
                return o.tolist()
            if isinstance(o, np.bool_):
                return bool(o)
        except Exception:
            pass
        if isinstance(o, Fraction):
            return fps_str(o)
        if isinstance(o, Path):
            return str(o)
        return super().default(o)


def save_json(path: str | Path, data, indent: int = 1):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=indent, cls=_Enc), encoding="utf-8")
    tmp.replace(path)


def load_json(path: str | Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def rnd(x, n=3):
    try:
        return round(float(x), n)
    except Exception:
        return x


# --------------------------------------------------------------------------- arabic text helpers

HARAKAT = re.compile("[ؐ-ًؚ-ٰٟۖ-ۭـ]")


def strip_harakat(s: str) -> str:
    return HARAKAT.sub("", s)


def has_arabic(s: str) -> bool:
    return any("؀" <= ch <= "ۿ" or "ݐ" <= ch <= "ݿ" or "ﭐ" <= ch <= "ﻼ" for ch in s)


def is_ltr_word(w: str) -> bool:
    letters = [c for c in w if c.isalpha() or c.isdigit()]
    return bool(letters) and not has_arabic(w)


class Timer:
    def __init__(self, label: str):
        self.label = label

    def __enter__(self):
        self.t0 = time.time()
        return self

    def __exit__(self, *exc):
        log(f"{self.label}: {time.time() - self.t0:.1f}s")


def ensure_dir(p: str | Path) -> Path:
    p = Path(p)
    p.mkdir(parents=True, exist_ok=True)
    return p


def work_paths(work: str | Path) -> dict[str, Path]:
    w = Path(work)
    return {
        "root": w, "spec": w / "spec.json", "frames": w / "frames", "sheets": w / "sheets",
        "text": w / "text", "audio": w / "audio", "cand": w / "candidates", "build": w / "build",
        "cache": w / "cache", "report": w / "report",
    }
