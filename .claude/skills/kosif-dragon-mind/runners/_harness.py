"""Shared harness for Dragon Mind power runners: one real program per method card.

A family module ``runners/fam_<family>.py`` registers one function per card:

    from _harness import card, check, fx

    @card("EASE-03")
    def duration_arithmetic(task, wd):
        ...do the card's method for real, write outputs into wd...
        return [check("total equals clips x length", total == 30, total, 30)], [wd / "plan.json"]

The function returns ``(checks, outputs)``. A card counts as executed only when every check passed
(known-answer checks that would fail if the method had not been applied) and at least one output file
exists and is non-empty. ``GAPS = {"ID": "reason"}`` in a module lists cards that cannot run here.
"""
from __future__ import annotations

import hashlib
import json
import math
import shutil
import subprocess
import wave
from pathlib import Path

REGISTRY: dict = {}


def card(card_id: str):
    def deco(fn):
        if card_id in REGISTRY:
            raise ValueError("duplicate runner for %s" % card_id)
        REGISTRY[card_id] = fn
        return fn
    return deco


def check(name: str, passed, measured=None, expected=None) -> dict:
    return {"check": name, "passed": bool(passed), "measured": _plain(measured), "expected": _plain(expected)}


def _plain(v):
    if v is None or isinstance(v, (bool, int, str)):
        return v
    if isinstance(v, float):
        return round(v, 6)
    if isinstance(v, (list, tuple)):
        return [_plain(x) for x in v]
    if isinstance(v, dict):
        return {str(k): _plain(x) for k, x in v.items()}
    try:
        return round(float(v), 6)
    except (TypeError, ValueError):
        return str(v)


def sha(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class fx:
    """Deterministic fixtures and measurements (ffmpeg, PIL, numpy, wave)."""

    @staticmethod
    def run(cmd: list, timeout: int = 60) -> subprocess.CompletedProcess:
        done = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, timeout=timeout,
                              stdin=subprocess.DEVNULL)
        if done.returncode:
            raise RuntimeError("command failed (%d): %s" % (done.returncode, done.stderr[-400:]))
        return done

    @staticmethod
    def ffmpeg(*args, timeout: int = 60):
        return fx.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args], timeout)

    @staticmethod
    def color_clip(path: Path, color: str = "red", seconds: float = 1.0, size: str = "320x180", fps: int = 30):
        fx.ffmpeg("-f", "lavfi", "-i", "color=c=%s:s=%s:r=%d:d=%s" % (color, size, fps, seconds),
                  "-pix_fmt", "yuv420p", "-c:v", "libx264", "-crf", "12", str(path))
        return Path(path)

    @staticmethod
    def test_clip(path: Path, seconds: float = 1.0, size: str = "320x180", fps: int = 30):
        fx.ffmpeg("-f", "lavfi", "-i", "testsrc2=s=%s:r=%d:d=%s" % (size, fps, seconds),
                  "-pix_fmt", "yuv420p", "-c:v", "libx264", "-crf", "12", str(path))
        return Path(path)

    @staticmethod
    def probe(path: Path) -> dict:
        out = fx.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)]).stdout
        return json.loads(out)

    @staticmethod
    def frames(path: Path, size=(64, 36)):
        """All frames of a video as float numpy arrays (N, H, W, 3) in 0..255, scaled down for measuring."""
        import numpy as np
        w, h = size
        done = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vf", "scale=%d:%d" % (w, h),
                               "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, timeout=120,
                              stdin=subprocess.DEVNULL)
        if done.returncode:
            raise RuntimeError(done.stderr.decode(errors="replace")[-300:])
        return np.frombuffer(done.stdout, dtype=np.uint8).reshape(-1, h, w, 3).astype(float)

    @staticmethod
    def tone(path: Path, freq: float = 440.0, seconds: float = 1.0, rate: int = 44100, amp: float = 0.5):
        n = int(seconds * rate)
        with wave.open(str(path), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(rate)
            w.writeframes(b"".join(int(amp * 32767 * math.sin(2 * math.pi * freq * i / rate)).to_bytes(2, "little", signed=True)
                                   for i in range(n)))
        return Path(path)

    @staticmethod
    def read_wav(path: Path):
        import numpy as np
        with wave.open(str(path), "rb") as w:
            ch, sw, rate, n = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
            data = np.frombuffer(w.readframes(n), dtype={1: np.int8, 2: np.int16, 4: np.int32}[sw]).astype(float)
        data = data.reshape(-1, ch) / float(2 ** (8 * sw - 1))
        return data, rate

    @staticmethod
    def write_wav(path: Path, samples, rate: int = 44100):
        import numpy as np
        a = np.clip(np.asarray(samples, dtype=float), -1, 1)
        if a.ndim == 1:
            a = a[:, None]
        with wave.open(str(path), "wb") as w:
            w.setnchannels(a.shape[1])
            w.setsampwidth(2)
            w.setframerate(rate)
            w.writeframes((a * 32767).astype("<i2").tobytes())
        return Path(path)

    @staticmethod
    def have(module: str) -> bool:
        import importlib.util
        return importlib.util.find_spec(module) is not None

    @staticmethod
    def which(binary: str) -> bool:
        return shutil.which(binary) is not None
