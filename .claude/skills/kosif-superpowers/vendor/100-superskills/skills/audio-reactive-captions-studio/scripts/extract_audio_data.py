#!/usr/bin/env python3
"""يستخرج بيانات صوت حتمية لكل إطار فيديو: RMS و16 حزمة ترددية مطبّعة (الباص أولاً) وBPM ونبضات، إلى JSON يقود الأنيميشن.

usage: python extract_audio_data.py track.mp3 [--fps 30] [--bands 16] [--out audio-data.json]
المخرج: {"fps":30,"totalFrames":N,"bpm":…, "beats":[s…], "frames":[{"time":t,"rms":0-1,"bands":[0-1 …]}]}
يحتاج ffmpeg وnumpy. حمّله في المشهد متزامناً (XHR sync أو مضمّن)؛ لا fetch غير متزامن قبل بناء الخط الزمني.
"""
import argparse
import json
import subprocess
import sys

try:
    import numpy as np
except ImportError:
    sys.exit("numpy غير مثبت: pip install numpy")

SR = 22050


def load(path):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True)
    if r.returncode != 0:
        raise SystemExit(r.stderr.decode(errors="ignore")[-600:])
    return np.frombuffer(r.stdout, dtype=np.float32)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("audio"); ap.add_argument("--fps", type=int, default=30); ap.add_argument("--bands", type=int, default=16); ap.add_argument("--out", default="audio-data.json")
    a = ap.parse_args()
    x = load(a.audio)
    hop = SR // a.fps
    n = len(x) // hop
    win = np.hanning(hop * 2)
    edges = np.geomspace(40, 10000, a.bands + 1)
    freqs = np.fft.rfftfreq(hop * 2, 1 / SR)
    idx = [np.where((freqs >= lo) & (freqs < hi))[0] for lo, hi in zip(edges[:-1], edges[1:])]
    rms = np.zeros(n); bands = np.zeros((n, a.bands)); flux = np.zeros(n); prev = None
    for i in range(n):
        seg = np.concatenate([x[(i - 1) * hop:i * hop] if i else np.zeros(hop), x[i * hop:(i + 1) * hop]])
        if len(seg) < hop * 2:
            seg = np.pad(seg, (0, hop * 2 - len(seg)))
        rms[i] = np.sqrt(np.mean(seg[hop:] ** 2))
        spec = np.abs(np.fft.rfft(seg * win))
        for b, ix in enumerate(idx):
            bands[i, b] = spec[ix].mean() if len(ix) else 0
        if prev is not None:
            d = spec - prev; flux[i] = d[d > 0].sum()
        prev = spec
    rms = rms / (rms.max() or 1)
    bands = bands / (bands.max(axis=0, keepdims=True) + 1e-9)
    flux = flux / (flux.max() or 1)
    # beats: adaptive threshold peaks with min gap 0.25s
    k = max(1, a.fps // 2); peaks, last = [], -10 ** 9
    for i in range(1, n - 1):
        lo, hi = max(0, i - k), min(n, i + k)
        thr = flux[lo:hi].mean() + 0.5 * flux[lo:hi].std()
        if flux[i] > thr and flux[i] >= flux[i - 1] and flux[i] >= flux[i + 1] and i - last >= a.fps // 4:
            peaks.append(i); last = i
    beats = [round(p / a.fps, 3) for p in peaks]
    bpm = None
    if len(beats) > 4:
        g = np.diff(beats); g = g[(g > 0.25) & (g < 2.0)]
        if len(g):
            h, e = np.histogram(g, bins=60, range=(0.25, 2.0)); per = e[h.argmax()] + (e[1] - e[0]) / 2; bpm = 60 / per
            while bpm < 70: bpm *= 2
            while bpm > 180: bpm /= 2
            bpm = round(bpm, 1)
    out = {"fps": a.fps, "totalFrames": n, "duration": round(n / a.fps, 3), "bpm": bpm, "beats": beats,
           "frames": [{"time": round(i / a.fps, 3), "rms": round(float(rms[i]), 3), "bands": [round(float(v), 3) for v in bands[i]]} for i in range(n)]}
    open(a.out, "w", encoding="utf-8").write(json.dumps(out, separators=(",", ":")))
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(json.dumps({"frames": n, "duration": out["duration"], "bpm": bpm, "beats": len(beats), "out": a.out}, ensure_ascii=False))


if __name__ == "__main__":
    main()
