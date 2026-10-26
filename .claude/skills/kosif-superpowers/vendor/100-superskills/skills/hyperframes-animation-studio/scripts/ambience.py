"""Deterministic ambience for a film, synthesised with numpy (no samples, no downloads): sea swell, wind, a soft
pad, rain with a thunder roll, and whooshes on the beats you name. Every sound is keyed to seconds, like the picture.

    python ambience.py out.wav --seconds 17 --rain 9.6:12.8 --thunder 10.6 --whoosh 0.6,15.3 --chords 0:A,6:F,12.6:C
"""
from __future__ import annotations

import argparse
import math
import wave
from pathlib import Path

import numpy as np

SR = 44100
NOTE = {"C": 130.81, "D": 146.83, "E": 164.81, "F": 174.61, "G": 196.0, "A": 220.0, "B": 246.94}


def _env(n: int, t0: float, t1: float, fade: float = 0.5) -> np.ndarray:
    t = np.arange(n) / SR
    e = np.clip((t - t0) / max(fade, 1e-3), 0, 1) * np.clip((t1 - t) / max(fade, 1e-3), 0, 1)
    return e


def _lowpass(x: np.ndarray, cutoff: float) -> np.ndarray:
    a = math.exp(-2 * math.pi * cutoff / SR)
    y = np.empty_like(x)
    acc = 0.0
    b = 1 - a
    for i in range(len(x)):                               # one-pole IIR; fine for a few hundred thousand samples
        acc = a * acc + b * x[i]
        y[i] = acc
    return y


def _lowpass_fast(x: np.ndarray, cutoff: float) -> np.ndarray:
    """Same filter through scipy-free vectorisation: cascaded moving averages approximate a gentle low-pass."""
    k = max(1, int(SR / (2 * math.pi * cutoff)))
    y = x
    for _ in range(2):
        y = np.convolve(y, np.ones(k) / k, mode="same")
    return y


def _highpass(x: np.ndarray, cutoff: float) -> np.ndarray:
    return x - _lowpass_fast(x, cutoff)


def birdsong(n: int, t0: float, t1: float, rng, density: float = 1.0) -> np.ndarray:
    """Dawn birds: short seeded FM chirps in phrases, placed left/right in the stereo field."""
    out = np.zeros((n, 2))
    count = int((t1 - t0) * 2.2 * density)
    for _ in range(count):
        start = t0 + rng.random() * (t1 - t0)
        notes = 2 + int(rng.random() * 5)
        pan = rng.random()
        f0 = 2200 + rng.random() * 2600
        for k in range(notes):
            dur = 0.05 + rng.random() * 0.09
            i0 = int((start + k * (dur + 0.03 + rng.random() * 0.05)) * SR)
            m = int(dur * SR)
            if i0 + m >= n:
                break
            tt = np.arange(m) / SR
            sweep = f0 * (1 + 0.35 * rng.random() * np.sin(2 * math.pi * (6 + 10 * rng.random()) * tt + rng.random() * 6))
            env = np.sin(np.pi * tt / dur) ** 1.6
            tone = np.sin(2 * math.pi * np.cumsum(sweep) / SR) * env * (0.07 + 0.06 * rng.random())
            out[i0:i0 + m, 0] += tone * (1 - pan)
            out[i0:i0 + m, 1] += tone * pan
    return out


def synth(seconds: float, rain: list[tuple[float, float]], thunder: list[float], whoosh: list[float],
          chords: list[tuple[float, str]], seed: int = 7, birds: list[tuple[float, float]] | None = None, sea: float = 1.0, drops=None, brook=None) -> np.ndarray:
    n = int(seconds * SR)
    t = np.arange(n) / SR
    rng = np.random.default_rng(seed)
    out = np.zeros((n, 2))
    for t0, t1 in (birds or []):
        out += birdsong(n, t0, t1, rng)
    sea_level = sea
    for ch in range(2):
        noise = rng.standard_normal(n)
        # sea: low rumble with a slow swell
        sea = _lowpass_fast(noise, 320) * (0.55 + 0.45 * np.sin(2 * math.pi * 0.11 * t + ch * 0.9))
        sea = sea / (np.abs(sea).max() + 1e-9) * 0.22 * sea_level
        # wind: a breathing band of air
        wind = _highpass(_lowpass_fast(noise, 1400), 300) * (0.4 + 0.6 * (0.5 + 0.5 * np.sin(2 * math.pi * 0.07 * t + 1.3 + ch)))
        wind = wind / (np.abs(wind).max() + 1e-9) * 0.07
        out[:, ch] += sea + wind
    # pad: slow chords, detuned, with a long attack
    pad = np.zeros(n)
    bounds = [c[0] for c in chords] + [seconds]
    for (t0, name), t1 in zip(chords, bounds[1:]):
        f = NOTE[name.upper()[0]]
        e = _env(n, t0, t1 + 0.8, fade=1.8)
        for mult, amp in ((1, 1.0), (1.5, 0.55), (2, 0.5), (2.5, 0.3), (3, 0.22)):
            for det in (-0.4, 0.3):
                pad += amp * np.sin(2 * math.pi * (f * mult + det) * t + det) * e
    pad = pad / (np.abs(pad).max() + 1e-9) * 0.09
    out[:, 0] += pad
    out[:, 1] += pad * 0.95
    # rain: bright hiss with droplets
    for t0, t1 in rain:
        e = _env(n, t0, t1, fade=0.7)
        hiss = _highpass(rng.standard_normal(n), 2500) * e
        hiss = hiss / (np.abs(hiss).max() + 1e-9) * 0.17
        ticks = np.zeros(n)
        for _ in range(int((t1 - t0) * 90)):
            i = int((t0 + rng.random() * (t1 - t0)) * SR)
            if i + 400 < n:
                ticks[i:i + 400] += np.exp(-np.arange(400) / 90) * rng.random() * 0.3
        out[:, 0] += hiss + ticks * e * 0.6
        out[:, 1] += np.roll(hiss, 311) + np.roll(ticks, 211) * e * 0.6
    # thunder: a brown-noise roll that decays over two seconds
    for t0 in thunder:
        i0 = int(t0 * SR)
        m = min(n - i0, int(2.6 * SR))
        if m <= 0:
            continue
        roll = np.cumsum(rng.standard_normal(m))
        roll = _lowpass_fast(roll - roll.mean(), 120)
        roll = roll / (np.abs(roll).max() + 1e-9) * np.exp(-np.arange(m) / (0.9 * SR)) * 0.5
        out[i0:i0 + m, 0] += roll
        out[i0:i0 + m, 1] += np.roll(roll, 97)
    # whoosh: a band of noise swept up over 0.45 s
    for t0 in whoosh:
        i0 = int(t0 * SR)
        m = min(n - i0, int(0.6 * SR))
        if m <= 0:
            continue
        w = _highpass(_lowpass_fast(rng.standard_normal(m), 3000), 400)
        env = np.sin(np.linspace(0, math.pi, m)) ** 2
        w = w / (np.abs(w).max() + 1e-9) * env * 0.25
        out[i0:i0 + m, 0] += w
        out[i0:i0 + m, 1] += w
    # water plinks: a droplet is a small bubble ringing as it closes — a sine whose pitch rises fast and dies in ~60 ms
    def plink(f0, amp):
        m = int(0.12 * SR); tt = np.arange(m) / SR
        f = f0 * (1 + 0.9 * (1 - np.exp(-tt / 0.012)))
        return np.sin(2 * math.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.045) * amp
    for t0 in (drops or []):
        i0 = int(t0 * SR)
        if i0 >= n:
            continue
        d = plink(900 + rng.random() * 900, 0.16 + rng.random() * 0.1)[: n - i0]
        pan = rng.random()
        out[i0:i0 + len(d), 0] += d * (1 - pan * 0.6); out[i0:i0 + len(d), 1] += d * (0.4 + pan * 0.6)
    for t0, t1 in (brook or []):                         # a trickle: soft band noise and many small plinks
        e = _env(n, t0, t1, fade=1.0)
        b = _highpass(_lowpass_fast(rng.standard_normal(n), 2600), 500) * e
        out[:, 0] += b / (np.abs(b).max() + 1e-9) * 0.05; out[:, 1] += np.roll(b, 523) / (np.abs(b).max() + 1e-9) * 0.05
        for _ in range(int((t1 - t0) * 14)):
            i0 = int((t0 + rng.random() * (t1 - t0)) * SR)
            d = plink(1300 + rng.random() * 1800, 0.05 + rng.random() * 0.05)[: max(0, n - i0)]
            ch = int(rng.random() * 2); out[i0:i0 + len(d), ch] += d
    # final: gentle tail fade and normalisation
    out *= _env(n, 0, seconds, fade=0.4)[:, None]
    out = out / (np.abs(out).max() + 1e-9) * 0.85
    return out


def write_wav(path: str | Path, data: np.ndarray):
    pcm = (np.clip(data, -1, 1) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def _pairs(s: str) -> list[tuple[float, float]]:
    return [tuple(float(v) for v in p.split(":")) for p in s.split(",") if p]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--seconds", type=float, default=10)
    ap.add_argument("--rain", default="", help="t0:t1[,t0:t1]")
    ap.add_argument("--thunder", default="", help="t[,t]")
    ap.add_argument("--whoosh", default="", help="t[,t]")
    ap.add_argument("--chords", default="0:A", help="t:NOTE[,t:NOTE]")
    ap.add_argument("--birds", default="", help="t0:t1[,t0:t1] dawn birdsong")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--sea", type=float, default=1.0, help="sea swell level (0 for a pond or a room)")
    ap.add_argument("--drops", default="", help="t[,t] single water plinks (a petal landing, a fish rising)")
    ap.add_argument("--brook", default="", help="t0:t1[,t0:t1] a trickle of water")
    a = ap.parse_args()
    chords = [(float(p.split(":")[0]), p.split(":")[1]) for p in a.chords.split(",") if p]
    data = synth(a.seconds, _pairs(a.rain), [float(v) for v in a.thunder.split(",") if v],
                 [float(v) for v in a.whoosh.split(",") if v], chords, a.seed, _pairs(a.birds), a.sea,
                 [float(v) for v in a.drops.split(",") if v], _pairs(a.brook))
    write_wav(a.out, data)
    print(a.out, f"{a.seconds}s stereo {SR} Hz")


if __name__ == "__main__":
    main()
