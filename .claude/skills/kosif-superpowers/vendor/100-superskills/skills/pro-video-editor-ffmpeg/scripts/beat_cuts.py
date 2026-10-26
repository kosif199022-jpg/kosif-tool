#!/usr/bin/env python3
"""يستخرج طاقة الصوت ونبضاته (onsets) وBPM تقريبياً من أي ملف عبر ffmpeg + numpy، ويقترح نقاط قطع على الإيقاع.

usage: python beat_cuts.py music.mp3 [--every 2] [--min-gap 0.5] [--out beats.json]
--every N يختار كل N نبضة كنقطة قطع (1 = كل نبضة، 2 = كل نبضتين …). المخرج: {bpm, beats_s, cut_points_s, energy_fps}
يحتاج numpy. الطريقة: غلاف طاقة على 100 إطار/ث → فرق طيفي موجب → عتبة متكيفة → ذروات → BPM من التوزيع الزمني للفواصل.
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
HOP = SR // 100  # 100 frames per second


def load_mono(path):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True)
    if r.returncode != 0:
        raise SystemExit(r.stderr.decode(errors="ignore")[-800:])
    return np.frombuffer(r.stdout, dtype=np.float32)


def onset_envelope(x):
    n = len(x) // HOP
    frames = x[: n * HOP].reshape(n, HOP)
    win = np.hanning(HOP * 2)
    spec_prev, flux = None, np.zeros(n)
    for i in range(n):
        seg = np.concatenate([frames[i - 1] if i else np.zeros(HOP), frames[i]]) * win
        spec = np.abs(np.fft.rfft(seg))
        if spec_prev is not None:
            d = spec - spec_prev
            flux[i] = np.sum(d[d > 0])
        spec_prev = spec
    flux = flux / (flux.max() or 1)
    rms = np.sqrt((frames ** 2).mean(axis=1)); rms = rms / (rms.max() or 1)
    return flux, rms


def pick_peaks(flux, min_gap_frames=25):
    k = 50
    pad = np.pad(flux, (k, k), mode="edge")
    thr = np.array([pad[i:i + 2 * k].mean() + 0.6 * pad[i:i + 2 * k].std() for i in range(len(flux))])
    peaks, last = [], -10 ** 9
    for i in range(1, len(flux) - 1):
        if flux[i] > thr[i] and flux[i] >= flux[i - 1] and flux[i] >= flux[i + 1] and i - last >= min_gap_frames:
            peaks.append(i); last = i
    return peaks


def estimate_bpm(beats_s):
    if len(beats_s) < 4:
        return None
    gaps = np.diff(beats_s)
    gaps = gaps[(gaps > 0.25) & (gaps < 2.0)]
    if not len(gaps):
        return None
    hist, edges = np.histogram(gaps, bins=60, range=(0.25, 2.0))
    g = edges[hist.argmax()] + (edges[1] - edges[0]) / 2
    bpm = 60 / g
    while bpm < 70: bpm *= 2
    while bpm > 180: bpm /= 2
    return round(bpm, 1)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("--every", type=int, default=2)
    ap.add_argument("--min-gap", type=float, default=0.5)
    ap.add_argument("--out", default="beats.json")
    a = ap.parse_args()
    x = load_mono(a.audio)
    flux, rms = onset_envelope(x)
    peaks = pick_peaks(flux, int(a.min_gap * 100 * 0.6))
    beats = [round(p / 100, 3) for p in peaks]
    bpm = estimate_bpm(np.array(beats))
    cuts = beats[:: max(1, a.every)]
    # also expose per-video-frame energy at 30fps for animation use
    idx = (np.arange(0, len(rms), 100 / 30)).astype(int)
    energy30 = [round(float(v), 3) for v in rms[idx[idx < len(rms)]]]
    out = {"file": a.audio, "duration_s": round(len(x) / SR, 2), "bpm": bpm, "beats_s": beats, "cut_points_s": cuts,
           "beat_period_s": round(60 / bpm, 3) if bpm else None, "energy_fps": 30, "energy": energy30}
    open(a.out, "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False))
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(json.dumps({k: out[k] for k in ("duration_s", "bpm", "beat_period_s")} | {"beats": len(beats), "cuts": len(cuts), "out": a.out}, ensure_ascii=False))


if __name__ == "__main__":
    main()
