"""KOSIF score — an original soundtrack synthesised on the film's beat grid (numpy only, no samples, no downloads).

Picture and sound read one clock: the score is written in beats, every designed sound sits on a cue the picture
exports (contact frames, 50% pops, settles), and the master is normalised to −14 LUFS when the film is muxed.

    python score.py out.wav --spec score.json [--cues cues.json] [--stems DIR]
    python score.py out.wav --bpm 120 --seconds 15 --key A --mood launch          (a default arrangement)

spec (all times in beats unless the key ends in _s):
{
  "bpm": 120, "seconds": 15, "key": "A", "scale": "minor",
  "sections": [{"from": 0, "to": 8, "kick": "four", "hats": true, "bass": true, "pad": true, "pluck": [0,3,5,7]},
               {"from": 8, "to": 10, "stop": true},
               {"from": 10, "to": 28, "kick": "four", "clap": true, "hats": true, "bass": true, "pad": true, "lead": [7,5,3,0]}],
  "chords": [[0, "i"], [8, "VI"], [16, "III"], [24, "VII"]],
  "drops": [10], "risers": [[6, 10]], "booms": [10], "end_s": 14.2,
  "tape_stops_s": [[6.0, 0.8]], "tape_starts_s": [[7.2, 0.5]]
}
cues: [{"t": 1.25, "type": "click|pop|tick|thump|whoosh|swish|chime|type|boom|riser", "gain": 1.0, "pan": 0}]
"""
from __future__ import annotations

import argparse
import json
import math
import wave
from pathlib import Path

import numpy as np

SR = 48000
NOTE = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
SCALES = {"minor": [0, 2, 3, 5, 7, 8, 10], "major": [0, 2, 4, 5, 7, 9, 11], "dorian": [0, 2, 3, 5, 7, 9, 10], "hijaz": [0, 1, 4, 5, 7, 8, 10],
          "pentatonic": [0, 3, 5, 7, 10], "lydian": [0, 2, 4, 6, 7, 9, 11]}
ROMAN = {"i": 0, "ii": 1, "iii": 2, "iv": 3, "v": 4, "vi": 5, "vii": 6}


def hz(midi: float) -> float:
    return 440.0 * 2 ** ((midi - 69) / 12)


def tt(d: float) -> np.ndarray:
    return np.arange(int(max(d, 0.001) * SR)) / SR


class Rng:
    def __init__(self, seed: int):
        self.r = np.random.default_rng(seed)

    def noise(self, n: int) -> np.ndarray:
        return self.r.standard_normal(n).astype(np.float64)


def onepole_lp(x: np.ndarray, cutoff: float) -> np.ndarray:
    """A gentle low-pass via FFT (zero phase), cheap for whole stems."""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / np.sqrt(1 + (f / max(cutoff, 1)) ** 4)
    return np.fft.irfft(X, len(x))


def bandpass(x: np.ndarray, lo: float, hi: float) -> np.ndarray:
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / np.sqrt(1 + (lo / np.maximum(f, 1)) ** 4) / np.sqrt(1 + (f / hi) ** 4)
    return np.fft.irfft(X, len(x))


# ───────── instruments (mono, peak ~1) ─────────
def kick(rng):
    t = tt(0.45)
    f = 46 + 110 * np.exp(-t / 0.032)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.22)
    y += 0.25 * rng.noise(len(t)) * np.exp(-t / 0.002)
    return np.tanh(1.7 * y)


def clap(rng):
    t = tt(0.35)
    n = bandpass(rng.noise(len(t)), 900, 3200)
    env = sum(np.where(t >= d, np.exp(-(t - d) / 0.007), 0) for d in (0, 0.009, 0.019)) + 0.55 * np.where(t > 0.028, np.exp(-(t - 0.028) / 0.09), 0)
    y = n * env
    return y / (np.abs(y).max() + 1e-9)


def hat(rng, open_=False):
    t = tt(0.22 if open_ else 0.05)
    y = bandpass(rng.noise(len(t)), 6500, 15000) * np.exp(-t / (0.07 if open_ else 0.011))
    return y / (np.abs(y).max() + 1e-9)


def sub(f, dur):
    t = tt(dur)
    y = np.sin(2 * np.pi * f * t) + 0.22 * np.sin(4 * np.pi * f * t)
    a = np.minimum(1, t / 0.006) * np.minimum(1, np.maximum(0, (dur - t) / 0.03))
    return np.tanh(1.2 * y) * a


def pluck(f, dur=0.9, bright=1.0):
    """Karplus-Strong-like additive pluck: decaying partials, brighter attack."""
    t = tt(dur)
    y = np.zeros_like(t)
    for k in range(1, 14):
        if f * k > 14000:
            break
        y += (k ** -0.9) * (1.4 * bright if 2 <= k <= 5 else 1) * np.sin(2 * np.pi * f * k * t) * np.exp(-t * (2.0 + 0.9 * k))
    y *= np.minimum(1, t / 0.002)
    return y / (np.abs(y).max() + 1e-9)


def bell(f, dur=1.8):
    t = tt(dur)
    m = 2.2 * np.exp(-t / 0.45) * np.sin(2 * np.pi * f * 3.5 * t)
    return np.sin(2 * np.pi * f * t + m) * np.exp(-t / (dur * 0.35)) * np.minimum(1, t / 0.002)


def pad(freqs, dur, rng, cutoff=1500):
    t = tt(dur)
    y = np.zeros_like(t)
    for f in freqs:
        for d in (-0.0045, 0.0, 0.0052):
            ph = rng.r.random()
            y += 2 * ((f * (1 + d) * t + ph) % 1) - 1
    y = onepole_lp(y, cutoff)
    a = np.minimum(1, t / 0.6) * np.minimum(1, np.maximum(0, (dur - t) / 0.8))
    return y * a / (np.abs(y).max() + 1e-9)


def riser(dur, rng):
    t = tt(dur)
    n = rng.noise(len(t))
    out = np.zeros_like(t)
    seg = int(0.04 * SR)
    for i in range(0, len(t), seg):
        c = 300 * (9000 / 300) ** (i / len(t))
        out[i:i + seg] = bandpass(n[i:i + seg] if len(n[i:i + seg]) > 8 else np.zeros(8), c * 0.6, c * 1.5)[:len(out[i:i + seg])]
    return out * (t / dur) ** 2.2 / (np.abs(out).max() + 1e-9)


def boom(rng, dur=2.4):
    t = tt(dur)
    y = np.sin(2 * np.pi * np.cumsum(32 + 50 * np.exp(-t / 0.16)) / SR) * np.exp(-t / 0.8)
    y += 0.4 * onepole_lp(rng.noise(len(t)), 700) * np.exp(-t / 0.3)
    return np.tanh(1.8 * y)


# designed SFX: every one is caused by something visible
def sfx(kind: str, rng, root: float):
    if kind == "click":
        t = tt(0.05); y = np.sin(2 * np.pi * 1900 * t) * np.exp(-t * 95) + 0.3 * rng.noise(len(t)) * np.exp(-t * 400)
    elif kind == "tick":
        t = tt(0.04); y = np.sin(2 * np.pi * root * 8 * t) * np.exp(-t * 140)
    elif kind == "pop":
        t = tt(0.16); y = np.sin(2 * np.pi * np.cumsum(500 + 1100 * (t / 0.16)) / SR) * np.exp(-t * 28)
    elif kind == "thump":
        t = tt(0.4); y = np.sin(2 * np.pi * np.cumsum(70 + 90 * np.exp(-t / 0.04)) / SR) * np.exp(-t * 9)
    elif kind == "whoosh":
        t = tt(0.55); n = rng.noise(len(t)); env = np.sin(np.pi * np.minimum(1, t / 0.55)) ** 2
        y = bandpass(n, 400, 5000) * env
    elif kind == "swish":
        t = tt(0.22); n = rng.noise(len(t)); y = bandpass(n, 1500, 9000) * np.sin(np.pi * t / 0.22) ** 3
    elif kind == "chime":
        y = bell(root * 4, 1.2) * 0.8 + bell(root * 6, 1.2) * 0.4
    elif kind == "type":
        t = tt(0.03); y = bandpass(rng.noise(len(t)), 300, 1600) * np.exp(-t * 180)
    elif kind == "boom":
        y = boom(rng)
    elif kind == "riser":
        y = riser(1.5, rng)
    else:
        t = tt(0.05); y = np.zeros_like(t)
    y = np.asarray(y, np.float64)
    # 6 ms cos² tail, no clicks at the buffer end
    k = min(len(y), int(0.006 * SR)); y[-k:] *= np.cos(np.linspace(0, np.pi / 2, k)) ** 2
    return y / (np.abs(y).max() + 1e-9)


class Score:
    BUS = ("kick", "perc", "bass", "music", "fx", "sfx")

    def __init__(self, bpm: float, seconds: float, key: str = "A", scale: str = "minor", seed: int = 7):
        self.bpm, self.beat, self.dur = bpm, 60 / bpm, seconds
        self.N = int((seconds + 0.05) * SR)
        self.bus = {b: np.zeros((2, self.N)) for b in self.BUS}
        self.root = 45 + NOTE.get(key, 9)                     # A2 by default (MIDI)
        self.scale = SCALES.get(scale, SCALES["minor"])
        self.rng = Rng(seed)
        self.cache = {}

    def tb(self, b):
        return b * self.beat

    def deg(self, d: int, octave: int = 0) -> float:
        n = len(self.scale)
        return hz(self.root + 12 * (octave + d // n) + self.scale[d % n])

    def chord(self, roman: str, octave: int = 1):
        d = ROMAN.get(roman.lower(), 0)
        return [self.deg(d, octave), self.deg(d + 2, octave), self.deg(d + 4, octave)]

    def add(self, bus, sig, t, gain=1.0, pan=0.0):
        i = int(t * SR)
        if i >= self.N or len(sig) == 0:
            return
        if i < 0:
            sig, i = sig[-i:], 0
        sig = sig[: self.N - i]
        l, r = math.cos((pan + 1) * math.pi / 4) * 1.414, math.sin((pan + 1) * math.pi / 4) * 1.414
        self.bus[bus][0, i:i + len(sig)] += sig * gain * l
        self.bus[bus][1, i:i + len(sig)] += sig * gain * r

    def at(self, bus, sig, beat, gain=1.0, pan=0.0):
        self.add(bus, sig, self.tb(beat), gain, pan)

    def cached(self, key, fn):
        if key not in self.cache:
            self.cache[key] = fn()
        return self.cache[key]

    # ── arrangement from a spec ──
    def arrange(self, spec: dict):
        chords = spec.get("chords") or [[0, "i"], [8, "VI"], [16, "III"], [24, "VII"]]
        chord_at = lambda b: next((c for s, c in reversed(chords) if b >= s), chords[0][1])
        total = self.dur / self.beat
        for sec in spec.get("sections", []):
            b0, b1 = sec["from"], min(sec["to"], total)
            if sec.get("stop"):
                continue
            b = b0
            while b < b1 - 1e-6:
                bar_pos = (b - b0) % 4
                if sec.get("kick") == "four" or (sec.get("kick") == "half" and bar_pos in (0, 2)):
                    self.at("kick", self.cached("kick", lambda: kick(self.rng)), b, 0.95)
                if sec.get("clap") and int(round(bar_pos)) in (1, 3):
                    self.at("perc", self.cached("clap", lambda: clap(self.rng)), b, 0.5)
                if sec.get("hats"):
                    self.at("perc", self.cached("hat", lambda: hat(self.rng)), b + 0.5, 0.35, 0.3)
                    self.at("perc", self.cached("hat", lambda: hat(self.rng)), b + 0.75, 0.14, -0.3)
                if sec.get("bass"):
                    root = self.chord(chord_at(b), -1)[0] / 2
                    for s in (0, 0.5):
                        if b + s < b1:
                            self.at("bass", sub(root, self.tb(0.42)), b + s, 0.48 if s else 0.36)
                b += 1
            if sec.get("pad"):
                for s, c in chords:
                    e = next((s2 for s2, _ in chords if s2 > s), 1e9)
                    lo, hi = max(s, b0), min(e, b1)
                    if hi > lo:
                        self.at("music", pad(self.chord(c, 0), self.tb(hi - lo) + 0.4, self.rng), lo, 0.22)
            for key in ("pluck", "lead"):
                pat = sec.get(key)
                if pat:
                    step = 0.5 if key == "pluck" else 1.0
                    i, b = 0, b0
                    while b < b1 - 1e-6:
                        d = pat[i % len(pat)]
                        if d is not None:
                            oc = 1 if key == "pluck" else 2
                            self.at("music", pluck(self.deg(ROMAN.get(chord_at(b).lower(), 0) + d, oc), 0.7 if key == "pluck" else 1.1, 1.2 if key == "lead" else 1.0),
                                    b, 0.3 if key == "pluck" else 0.24, -0.25 + 0.5 * (i % 2))
                        i += 1; b += step
        for a, b in spec.get("risers", []):
            self.at("fx", riser(self.tb(b - a), self.rng), a, 0.32)
        for b in spec.get("booms", []):
            self.at("fx", boom(self.rng), b, 0.6)
        if spec.get("end_s"):
            # the lockup resolves: a soft bell on the root, then a tail
            self.add("music", bell(hz(self.root + 24), 2.4), spec["end_s"], 0.4)

    def cues(self, cues: list[dict]):
        root = hz(self.root + 12)
        for c in cues:
            self.add("sfx", sfx(c.get("type", "click"), self.rng, root), float(c["t"]) - (0.12 if c.get("type") == "whoosh" else 0), c.get("gain", 1.0) * 0.6, c.get("pan", 0.0))

    def tape(self, mix: np.ndarray, stops: list, starts: list) -> np.ndarray:
        """Tape-stop: from t0 the playback speed falls to zero over d seconds (pitch and tempo dive together), then dead air;
        tape-start: the speed spins up from zero over d seconds into the next section. stops/starts: [[t0, d], ...]"""
        out = mix.copy()
        for t0, d in stops:
            i0, n = int(t0 * SR), int(d * SR)
            if i0 + n >= self.N:
                continue
            u = np.arange(n) / n
            pos = i0 + np.cumsum((1 - u) ** 1.6)                          # read head slowing to a halt
            for c in range(2):
                out[c, i0:i0 + n] = np.interp(pos, np.arange(self.N), mix[c]) * (1 - u ** 3)
        for t0, d in starts:
            i0, n = int(t0 * SR), int(d * SR)
            if i0 + n >= self.N:
                continue
            u = np.arange(n) / n
            src0 = i0 + n                                                 # the section begins at t0 + d, reached from a standstill
            pos = src0 - np.cumsum((u[::-1]) ** 1.6)[::-1]
            for c in range(2):
                out[c, i0:i0 + n] = np.interp(np.clip(pos, 0, self.N - 1), np.arange(self.N), mix[c]) * np.sqrt(u)
        return out

    def mix(self, path: Path, stems: Path | None = None, silences: list | None = None, stops: list | None = None, starts: list | None = None):
        kick_env = np.abs(self.bus["kick"][0])
        kick_env = onepole_lp(kick_env, 8)
        kick_env /= kick_env.max() + 1e-9
        duck = 1 - 0.55 * np.clip(kick_env * 3, 0, 1)
        for b in ("bass", "music"):
            self.bus[b] *= duck
        sfx_env = onepole_lp(np.abs(self.bus["sfx"][0]), 6); sfx_env /= sfx_env.max() + 1e-9
        self.bus["music"] *= 1 - 0.3 * np.clip(sfx_env * 2, 0, 1)        # music dips ~3 dB under key hits
        gains = {"kick": 0.9, "perc": 0.7, "bass": 0.75, "music": 0.7, "fx": 0.6, "sfx": 0.85}
        mix = sum(v * gains[k] for k, v in self.bus.items())
        # room: a short seeded reverb on music/fx
        irt = tt(1.6)
        ir = np.stack([self.rng.noise(len(irt)), self.rng.noise(len(irt))]) * np.exp(-irt / 0.45)
        ir /= np.sqrt((ir ** 2).sum(1, keepdims=True))
        wet = self.bus["music"] * 0.7 + self.bus["fx"] * 0.6 + self.bus["sfx"] * 0.25
        mix += np.stack([np.convolve(wet[c], ir[c])[: self.N] for c in range(2)]) * 0.35
        for a, b in (silences or []):
            i0, i1 = int(a * SR), int(b * SR)
            mix[:, i0:i1] *= 0.04
        if stops or starts:
            mix = self.tape(mix, stops or [], starts or [])
        mix /= np.abs(mix).max() + 1e-9
        mix = np.tanh(1.3 * mix) / np.tanh(1.3) * 0.89
        k = int(0.01 * SR); mix[:, -k:] *= np.linspace(1, 0, k)
        write_wav(path, mix)
        if stems:
            stems.mkdir(parents=True, exist_ok=True)
            for k2, v in self.bus.items():
                if np.abs(v).max() > 0:
                    write_wav(stems / f"{k2}.wav", v / (np.abs(v).max() + 1e-9) * 0.8)
        return path


def write_wav(path: Path, stereo: np.ndarray):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    data = (np.clip(stereo.T, -1, 1) * 32767).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(data.tobytes())


DEFAULT = {"launch": lambda bars: {"sections": [{"from": 0, "to": 8, "kick": "half", "hats": True, "pad": True, "pluck": [0, None, 2, 4, None, 2, 0, None]},
                                                  {"from": 8, "to": bars * 4 * 0.55, "kick": "four", "clap": True, "hats": True, "bass": True, "pad": True, "pluck": [0, 2, 4, 7, 4, 2]},
                                                  {"from": bars * 4 * 0.55, "to": bars * 4 * 0.55 + 2, "stop": True},
                                                  {"from": bars * 4 * 0.55 + 2, "to": bars * 4 - 2, "kick": "four", "clap": True, "hats": True, "bass": True, "pad": True, "lead": [7, 4, 5, 2]}],
                                     "risers": [[bars * 4 * 0.55 - 2, bars * 4 * 0.55 + 2]], "booms": [bars * 4 * 0.55 + 2]},
           "calm": lambda bars: {"sections": [{"from": 0, "to": bars * 4, "pad": True, "pluck": [0, None, 4, None, 2, None, None, None]}]}}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("out")
    ap.add_argument("--spec"); ap.add_argument("--cues"); ap.add_argument("--stems")
    ap.add_argument("--bpm", type=float, default=120); ap.add_argument("--seconds", type=float, default=15)
    ap.add_argument("--key", default="A"); ap.add_argument("--scale", default="minor"); ap.add_argument("--mood", default="launch")
    ap.add_argument("--seed", type=int, default=7)
    a = ap.parse_args()
    spec = json.loads(Path(a.spec).read_text(encoding="utf-8")) if a.spec else {}
    bpm = spec.get("bpm", a.bpm); secs = spec.get("seconds", a.seconds)
    sc = Score(bpm, secs, spec.get("key", a.key), spec.get("scale", a.scale), spec.get("seed", a.seed))
    if not spec.get("sections"):
        bars = int(secs / (4 * 60 / bpm))
        spec = {**DEFAULT.get(a.mood, DEFAULT["launch"])(bars), **{k: v for k, v in spec.items() if k != "sections"}}
    sc.arrange(spec)
    cues = json.loads(Path(a.cues).read_text(encoding="utf-8")) if a.cues else spec.get("cues", [])
    sc.cues(cues)
    sil = [(s * sc.beat, e * sc.beat) for s, e in ((x["from"], x["to"]) for x in spec.get("sections", []) if x.get("stop"))]
    out = sc.mix(Path(a.out), Path(a.stems) if a.stems else None, sil, spec.get("tape_stops_s"), spec.get("tape_starts_s"))
    print(json.dumps({"file": str(out), "bpm": bpm, "seconds": secs, "cues": len(cues), "beat_s": round(60 / bpm, 4)}))


if __name__ == "__main__":
    main()
