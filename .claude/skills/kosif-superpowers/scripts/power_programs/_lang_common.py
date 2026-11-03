"""Shared deterministic helpers for the language group's program modules (ai-generation, prompt-craft,
agent-orchestration, writing-humanizer, arabic-language, voice-tts, web-research, knowledge-graph,
atlas-research).

Helpers are real procedures (text tokenising, Arabic folding, WAV synthesis and measurement,
ffmpeg runs, FFT band energy). Each card's program calls them with its own fixture and its own
parameters and checks known answers. The leading underscore keeps this file out of
power_programs.all_programs().
"""
from __future__ import annotations
import hashlib
import json
import re
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

SCRIPTS = Path(__file__).resolve().parent.parent


def save(work: Path, name: str, obj) -> Path:
    p = Path(work) / name
    p.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(obj, (dict, list)):
        p.write_text(json.dumps(obj, ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
    elif isinstance(obj, bytes):
        p.write_bytes(obj)
    else:
        p.write_text(str(obj), encoding="utf-8")
    return p


def eq(name, got, want, tol=None):
    if tol is None:
        ok = got == want
    else:
        ok = abs(float(got) - float(want)) <= tol
    return (name, bool(ok), f"got={got!r} want={want!r}")


def truth(name, cond, observed=""):
    return (name, bool(cond), str(observed)[:400])


def words(text: str) -> list:
    return re.findall(r"[\w\u0600-\u06FF']+", text.lower())


def sentences(text: str) -> list:
    return [s.strip() for s in re.split(r"(?<=[.!?؟])\s+|\n+", text) if s.strip()]


def jaccard(a, b) -> float:
    a, b = set(a), set(b)
    return len(a & b) / len(a | b) if a | b else 0.0


def sha256(data) -> str:
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


# ---------- Arabic ----------
HARAKAT = re.compile(r"[\u064B-\u0652\u0670\u0640]")
_FOLD = str.maketrans("أإآٱىة", "اااايه")


def norm_ar(s: str) -> str:
    return HARAKAT.sub("", s).translate(_FOLD)


# ---------- audio ----------
SR = 16000


def tone(freq, dur, sr=SR, amp=0.5, phase=0.0):
    t = np.arange(int(round(dur * sr))) / sr
    return amp * np.sin(2 * np.pi * freq * t + phase)


def write_wav(path: Path, x, sr=SR, bits=16):
    x = np.asarray(x, dtype=np.float64)
    if x.ndim == 1:
        x = x[:, None]
    ch = x.shape[1]
    x = np.clip(x, -1, 1)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(ch)
        w.setsampwidth(bits // 8)
        w.setframerate(sr)
        if bits == 16:
            w.writeframes((x * 32767).astype("<i2").tobytes())
        elif bits == 24:
            v = (x * 8388607).astype("<i4")
            b = v.astype("<i4").view(np.uint8).reshape(-1, 4)[:, :3]
            w.writeframes(b.tobytes())
        else:
            raise ValueError(bits)
    return path


def read_wav(path: Path):
    with wave.open(str(path), "rb") as w:
        sr, ch, sw, n = w.getframerate(), w.getnchannels(), w.getsampwidth(), w.getnframes()
        raw = w.readframes(n)
    if sw == 2:
        x = np.frombuffer(raw, "<i2").astype(np.float64) / 32768
    elif sw == 3:
        b = np.frombuffer(raw, np.uint8).reshape(-1, 3)
        v = (b[:, 0].astype(np.int32) | (b[:, 1].astype(np.int32) << 8) | (b[:, 2].astype(np.int32) << 16))
        v = np.where(v >= 1 << 23, v - (1 << 24), v)
        x = v.astype(np.float64) / 8388608
    elif sw == 4:
        x = np.frombuffer(raw, "<i4").astype(np.float64) / 2147483648
    else:
        raise ValueError(sw)
    return x.reshape(-1, ch), sr, sw * 8


def db(x) -> float:
    r = float(np.sqrt(np.mean(np.square(x)))) if len(x) else 0.0
    return 20 * np.log10(max(r, 1e-12))


def peak_db(x) -> float:
    return 20 * np.log10(max(float(np.max(np.abs(x))), 1e-12))


def band_db(x, sr, f, width=0.06):
    """Level (dB) of the spectrum around f (relative bandwidth width)."""
    x = np.asarray(x, dtype=np.float64)
    if x.ndim > 1:
        x = x.mean(axis=1)
    spec = np.abs(np.fft.rfft(x * np.hanning(len(x)))) / len(x)
    freqs = np.fft.rfftfreq(len(x), 1 / sr)
    m = (freqs > f * (1 - width)) & (freqs < f * (1 + width))
    return 20 * np.log10(max(float(np.sqrt(np.sum(spec[m] ** 2))), 1e-12))


def ffmpeg(*args, timeout=30):
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *map(str, args)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if r.returncode:
        raise RuntimeError(f"ffmpeg failed: {r.stderr[-400:]}")
    return r


def ffprobe_duration(path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                        "default=nw=1:nk=1", str(path)], capture_output=True, text=True, timeout=20)
    return float(r.stdout.strip())


def ffprobe_stream(path, sel="a:0") -> dict:
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", sel, "-show_streams", "-of", "json",
                        str(path)], capture_output=True, text=True, timeout=20)
    s = json.loads(r.stdout).get("streams", [])
    return s[0] if s else {}


def loudness(path) -> dict:
    """Integrated loudness and true peak via ffmpeg ebur128."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128=peak=true",
                        "-f", "null", "-"], capture_output=True, text=True, timeout=30)
    tail = r.stderr[r.stderr.rfind("Summary:"):]
    i = re.search(r"I:\s+(-?[\d.]+) LUFS", tail)
    p = re.search(r"Peak:\s+(-?[\d.]+) dBFS", tail)
    return {"I": float(i.group(1)) if i else None, "TP": float(p.group(1)) if p else None}


def run_py(code: str, work: Path, name="snippet.py", timeout=10):
    p = Path(work) / name
    p.write_text(code, encoding="utf-8")
    r = subprocess.run([sys.executable, "-I", str(p)], capture_output=True, text=True, timeout=timeout,
                       cwd=str(work))
    return r
