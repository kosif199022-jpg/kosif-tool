#!/usr/bin/env python3
"""KOSIF compositor: real footage + virtual camera + grade + transitions + typography → 1080x1920 60 fps."""
import json, subprocess, sys, math, os
import numpy as np, cv2
C = json.load(open("build/shots.json")); FPS = C["fps"]; OW, OH = C["W"], C["H"]; END = C["duration"]
NF = round(END * FPS); LEAD = 0.4
GRADE = {"S1": dict(exp=0.82,gam=1.25), "S2": dict(exp=0.9,gam=1.1), "S3": dict(exp=0.92,gam=1.05), "S4": dict(exp=1.0,gam=1.0), "S5": dict(exp=0.78,gam=1.35),
         "S6a": dict(exp=0.85,gam=1.25), "S6b": dict(exp=0.72,gam=1.35), "S7": dict(exp=0.72,gam=1.3), "S8": dict(exp=1.05,gam=1.0), "S9": dict(exp=0.9,gam=1.15)}
EASE = {"inOutSine": lambda t: -(math.cos(math.pi * t) - 1) / 2, "outSine": lambda t: math.sin(t * math.pi / 2),
        "smooth": lambda t: t * t * (3 - 2 * t)}

class Shot:
    def __init__(s, d):
        s.d = d; s.path = f"build/shot_{d['id']}.mp4"
        o = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", s.path], capture_output=True, text=True).stdout.split(",")
        s.w, s.h = int(o[0]), int(o[1]); s.proc = None; s.idx = -1; s.frame = None
        s.srcW = None
    def get(s, i):
        if s.proc is None:
            s.proc = subprocess.Popen(["ffmpeg", "-v", "error", "-i", s.path, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
        while s.idx < i:
            b = s.proc.stdout.read(s.w * s.h * 3)
            if len(b) < s.w * s.h * 3: break
            s.frame = np.frombuffer(b, np.uint8).reshape(s.h, s.w, 3); s.idx += 1
        return s.frame
    def render(s, t):
        d = s.d; i = max(0, round((t - d["start"] + LEAD) * FPS)); src = s.get(i)
        cam = d["cam"]; f = (t - d["start"]) / (d["end"] - d["start"]); f = min(1.12, max(-0.12, f))
        e = EASE[cam["ease"]](min(1, max(0, f))) + (f - min(1, max(0, f))) * 0.5   # keep drifting through transitions
        bx, _, bw, bh = d["band"]; scale = s.h / bh   # band may have been rescaled
        z = cam["z0"] + (cam["z1"] - cam["z0"]) * e
        H0 = bh  # full source height
        cx = ((cam["c0"][0] + (cam["c1"][0] - cam["c0"][0]) * e) * d["srcW"] - bx) * scale
        cy = (cam["c0"][1] + (cam["c1"][1] - cam["c0"][1]) * e) * H0 * scale
        ch = s.h / z; cw = ch * 9 / 16
        cx = min(max(cx, cw / 2), s.w - cw / 2); cy = min(max(cy, ch / 2), s.h - ch / 2)
        k = OH / ch
        M = np.float32([[k, 0, OW / 2 - cx * k], [0, k, OH / 2 - cy * k]])
        img = cv2.warpAffine(src, M, (OW, OH), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
        if k > 1.3:  # upscaled source: gentle unsharp to recover edge contrast (no detail is invented)
            bl = cv2.GaussianBlur(img, (0, 0), 1.4); img = cv2.addWeighted(img, 1.35, bl, -0.35, 0)
        return grade(img.astype(np.float32) / 255, GRADE[d["id"]])

def grade(x, g):
    x = np.power(x, g["gam"]) * g["exp"]
    x[..., 2] *= 1.035; x[..., 0] *= 0.94                     # warm (BGR)
    l = x.mean(2, keepdims=True); x = l + (x - l) * 0.92        # slightly calmer saturation
    x = np.clip(x, 0, None); x = x / (1 + 0.18 * x)  * 1.18    # highlight roll-off
    x = 0.012 + x * 0.98                                        # soft lifted blacks
    x = x + 0.12 * (x - 0.5) * (1 - np.abs(2 * x - 1))           # gentle S
    return np.clip(x, 0, 1)

# legibility scrims (static): darker band behind captions, soft top for the header, light vignette
yy = np.linspace(0, 1, OH)[:, None]; xx = np.linspace(-1, 1, OW)[None, :]
cap = np.exp(-((yy * OH - 1000) / 240) ** 2) * 0.48
top = np.exp(-((yy * OH - 440) / 260) ** 2) * 0.30
vig = np.clip((xx ** 2 * 0.5 + ((yy - 0.5) * 2) ** 2 * 0.35) - 0.15, 0, 1) * 0.35
SCRIM = (1 - np.clip(cap + top + vig, 0, 0.65)).astype(np.float32)[..., None]
rng = np.random.default_rng(7); GRAIN = [rng.normal(0, 1, (OH // 2, OW // 2)).astype(np.float32) for _ in range(6)]

def zoom(img, s):
    M = np.float32([[s, 0, OW / 2 * (1 - s)], [0, s, OH / 2 * (1 - s)]])
    return cv2.warpAffine(img, M, (OW, OH), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
def radial(img, s, n=7):
    if s < 0.004: return img
    acc = np.zeros_like(img)
    for j in range(n): acc += zoom(img, 1 + s * j / (n - 1))
    return acc / n
def blur(img, r):
    return img if r < 0.5 else cv2.GaussianBlur(img, (0, 0), r)

def transition(tr, A, B, p):
    ty = tr["type"]; e = EASE["smooth"](p); bell = math.sin(math.pi * p)
    if ty == "dissolve": return A * (1 - e) + B * e
    if ty == "blurdissolve": return blur(A, 10 * bell) * (1 - e) + blur(B, 10 * bell) * e
    if ty == "lightflash":
        m = A * (1 - e) + B * e; fl = bell ** 2 * 0.6
        warm = np.array([0.80, 0.92, 1.0], np.float32)                 # BGR warm white
        return 1 - (1 - m) * (1 - fl * warm)                             # screen blend
    if ty == "dip": return (A * (1 - e) + B * e) * (1 - 0.65 * bell)
    if ty in ("pushblur", "zoomblur"):
        st = 0.05 if ty == "pushblur" else 0.11
        a = radial(zoom(A, 1 + 0.08 * p), st * bell); b = radial(zoom(B, 1.07 - 0.07 * p), st * bell)
        out = a * (1 - e) + b * e
        if ty == "zoomblur": out = 1 - (1 - out) * (1 - 0.18 * bell ** 3)
        return out
    raise ValueError(ty)

def bloom(x):
    hi = np.clip(x - 0.72, 0, 1); hi = cv2.resize(hi, (OW // 4, OH // 4)); hi = cv2.GaussianBlur(hi, (0, 0), 9)
    return np.clip(x + cv2.resize(hi, (OW, OH)) * 0.55, 0, 1)

def frame(i, shots):
    t = i / FPS
    tr = next((r for r in C["transitions"] if r["at"] - 0.55 * r["dur"] <= t < r["at"] + 0.45 * r["dur"]), None)
    if tr:
        k = next(j for j, s in enumerate(C["shots"]) if abs(s["start"] - tr["at"]) < 1e-6)
        p = (t - (tr["at"] - 0.55 * tr["dur"])) / tr["dur"]
        img = transition(tr, shots[k - 1].render(t), shots[k].render(t), p)
    else:
        k = max(j for j, s in enumerate(C["shots"]) if s["start"] <= t + 1e-9); img = shots[k].render(t)
    img = bloom(img) * SCRIM
    g = cv2.resize(GRAIN[i % 6], (OW, OH), interpolation=cv2.INTER_NEAREST)[..., None]
    img = img + g * 0.012 * (1 - img)
    fade = min(1, t / 0.6) * min(1, max(0, (END - t) / 0.4))
    img = img * EASE["inOutSine"](fade)
    ov = cv2.imread(f"build/ov/{i:05d}.png", cv2.IMREAD_UNCHANGED)
    if ov is not None:
        a = ov[..., 3:4].astype(np.float32) / 255; img = img * (1 - a) + ov[..., :3].astype(np.float32) / 255 * a
    return (np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8)

def main():
    for s in C["shots"]:
        s["srcW"] = int(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width", "-of", "csv=p=0", s["src"]], capture_output=True, text=True).stdout)
    if sys.argv[1] == "stills":
        for t in map(float, sys.argv[2:]):
            shots = [Shot(s) for s in C["shots"]]; cv2.imwrite(f"build/still_{t}.png", frame(round(t * FPS), shots))
        return
    out = sys.argv[2]; shots = [Shot(s) for s in C["shots"]]
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{OW}x{OH}", "-r", str(FPS), "-i", "-",
        "-i", "audio/original_audio.m4a", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-profile:v", "high",
        "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-c:a", "copy", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for i in range(NF):
        enc.stdin.write(frame(i, shots).tobytes())
        if i % 120 == 0: print(f"{i}/{NF}", flush=True)
    enc.stdin.close(); enc.wait(); print("done", out)
if __name__ == "__main__": main()
