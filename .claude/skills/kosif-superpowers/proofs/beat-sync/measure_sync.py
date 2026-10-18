"""Measure audio-visual sync of the rendered film itself (not of the page's intent).
audio onsets: librosa on the AAC track decoded from the MP4.
visual events: frames where the mean absolute pixel change of the centre band (HUD excluded,
since its playhead moves every frame) rises above a threshold.
usage: python measure_sync.py film.mp4 [out.json]
"""
import json, subprocess, sys
import numpy as np, librosa

mp4 = sys.argv[1]; FPS = 30; SR = 48000; hop = 128
pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', mp4, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
y = np.frombuffer(pcm, np.float32)
env = librosa.onset.onset_strength(y=y, sr=SR, hop_length=hop)
on = librosa.frames_to_time(librosa.onset.onset_detect(onset_envelope=env, sr=SR, hop_length=hop, wait=int(0.08 * SR / hop)), sr=SR, hop_length=hop)

w, h = 270, 150   # centre band y 240..840 of 1080, downscaled 4x
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', mp4, '-vf', f'crop=1080:600:0:240,scale={w}:{h},format=gray', '-f', 'rawvideo', '-'], capture_output=True, check=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(np.float32)
d = np.r_[0, np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2))]
thr = max(0.6, 0.15 * np.median(d[d > 0.6]) if (d > 0.6).any() else 0.6)
events = [f for f in range(1, len(d)) if d[f] > thr and d[f - 1] <= thr]       # rising edges
ev_t = np.array(events) / FPS
pairs = []
for t in on:
    if not len(ev_t): break
    k = int(np.argmin(np.abs(ev_t - t)))
    if abs(ev_t[k] - t) <= 0.1: pairs.append((float(t), float(ev_t[k]), (ev_t[k] - t) * 1000))
offs = np.array([p[2] for p in pairs])
res = {'audio_onsets': len(on), 'visual_events': len(events), 'matched': len(pairs),
       'mean_offset_ms': round(float(offs.mean()), 2), 'mean_abs_offset_ms': round(float(np.abs(offs).mean()), 2),
       'max_abs_offset_ms': round(float(np.abs(offs).max()), 2), 'frame_ms': round(1000 / FPS, 2), 'threshold': round(float(thr), 3),
       'pairs': [{'onset': round(a, 4), 'frame_t': round(b, 4), 'offset_ms': round(c, 1)} for a, b, c in pairs]}
print(json.dumps({k: v for k, v in res.items() if k != 'pairs'}))
if len(sys.argv) > 2: open(sys.argv[2], 'w').write(json.dumps(res, indent=1))
