#!/usr/bin/env python3
"""s82: painted (B6-style) upside-down umbrella film. 9 painted stills -> 20 s motion film."""
import math, os, subprocess, sys
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

HERE = os.environ.get("JOB", os.getcwd())  # job dir holding shots/s0..s8.png; outputs go here
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import toonkit as tk

W, H, FPS, D = 1080, 1920, 30, 20.0
ARCH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fonts", "ArchivoBlack.ttf")
CAIRO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fonts", "Cairo-900.ttf")

# (image, start, end, cam from (zoom, cx, cy) -> to, kind)
SHOTS = [
    ("s0", 0.0, 2.6, (1.30, .62, .42), (1.08, .50, .52), "rain"),
    ("s1", 2.6, 4.6, (1.06, .50, .45), (1.22, .45, .42), "rain_laugh"),
    ("s2", 4.6, 6.8, (1.30, .50, .28), (1.10, .50, .45), "rain"),
    ("s3", 6.8, 8.8, (1.10, .50, .55), (1.26, .45, .35), "rain"),
    ("s8", 8.8, 10.3, (1.02, .50, .60), (1.28, .50, .40), "heat"),
    ("s4", 10.3, 12.6, (1.25, .45, .60), (1.06, .50, .50), "heat"),
    ("s6", 12.6, 14.4, (1.04, .50, .50), (1.24, .45, .45), "heat_shake"),
    ("s5", 14.4, 16.6, (1.24, .45, .55), (1.06, .50, .48), "heat"),
    ("s7", 16.6, 20.0, (1.25, .50, .50), (1.04, .50, .50), "warm"),
]
CAPS = [  # text, t0, t1, y
    ("IT'S RAINING.", 0.15, 1.5, 300),
    ("WHY IS IT UPSIDE DOWN?!", 1.5, 2.6, 300),
    ("HAHAHA", 2.75, 4.5, 1560),
    ("JUST WAIT.", 7.0, 8.7, 1700),
    ("NEXT DAY...", 8.95, 10.2, 960),
    ("50°C", 10.45, 12.5, 300),
    ("WAIT... WHAT?", 12.75, 14.3, 1620),
    ("WHO'S LAUGHING NOW?", 14.55, 16.5, 1720),
    ("SHARING IS SMARTER.", 16.8, 18.4, 300),
]

ease = lambda x: 0.5 - 0.5 * math.cos(math.pi * min(1, max(0, x)))
def out_back(x, s=1.7):
    x = min(1, max(0, x)) - 1; return 1 + (s + 1) * x ** 3 + s * x ** 2

IMG = {}
for s in {s[0] for s in SHOTS}:
    im = Image.open(os.path.join(HERE, "shots", s + ".png")).convert("RGB").resize((W, H), Image.LANCZOS)
    IMG[s] = np.asarray(im)[..., ::-1].copy()

rng = np.random.default_rng(7)
DROPS = rng.uniform(0, 1, (260, 3))  # x, phase, len


def cam(img, z, cx, cy, ang=0.0, dx=0.0, dy=0.0):
    M = cv2.getRotationMatrix2D((cx * W, cy * H), ang, z)
    M[0, 2] += W / 2 - cx * W + dx; M[1, 2] += H / 2 - cy * H + dy
    return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)


def rain(fr, t, k=1.0):
    ov = np.zeros_like(fr)
    for x, ph, ln in DROPS:
        y = ((ph + t * (1.6 + ln)) % 1.0) * (H + 200) - 100
        xx = x * (W + 300) - 150 + (y * 0.12)
        L = 30 + 50 * ln
        cv2.line(ov, (int(xx), int(y)), (int(xx + L * 0.2), int(y + L)), (235, 225, 215), 2, cv2.LINE_AA)
    return cv2.addWeighted(fr, 1.0, ov, 0.35 * k, 0)


def heat(fr, t):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    amp = np.clip((yy - H * 0.45) / (H * 0.55), 0, 1) * 3.0
    mx = xx + amp * np.sin(yy / 23.0 + t * 7.0)
    return cv2.remap(fr, mx, yy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


_fc = {}
def font(p, s):
    if (p, s) not in _fc: _fc[(p, s)] = ImageFont.truetype(p, s)
    return _fc[(p, s)]


def text_rgba(txt, size, fp=ARCH, stroke=9, fill=(255, 255, 255), maxw=980):
    f = font(fp, size)
    bb = ImageDraw.Draw(Image.new("L", (4, 4))).textbbox((0, 0), txt, font=f, stroke_width=stroke)
    if bb[2] - bb[0] > maxw: return text_rgba(txt, int(size * maxw / (bb[2] - bb[0])), fp, stroke, fill, maxw)
    im = Image.new("RGBA", (bb[2] - bb[0] + 40, bb[3] - bb[1] + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text((20 - bb[0] + 6, 20 - bb[1] + 8), txt, font=f, fill=(0, 0, 0, 120), stroke_width=stroke, stroke_fill=(0, 0, 0, 120))
    d.text((20 - bb[0], 20 - bb[1]), txt, font=f, fill=fill + (255,), stroke_width=stroke, stroke_fill=(20, 20, 24, 255))
    return im


def paste(fr, im, cx, cy, sc=1.0, a=1.0):
    if a <= 0.01 or sc <= 0.02: return fr
    if sc != 1.0: im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS)
    L = np.asarray(im).astype(np.float32)
    x0, y0 = int(cx - im.width / 2), int(cy - im.height / 2)
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + im.width), min(H, y0 + im.height)
    if xb <= xa or yb <= ya: return fr
    L = L[ya - y0:yb - y0, xa - x0:xb - x0]; al = L[..., 3:4] / 255 * a
    reg = fr[ya:yb, xa:xb].astype(np.float32)
    fr[ya:yb, xa:xb] = (reg * (1 - al) + L[..., 2::-1] * al).astype(np.uint8)
    return fr


CAPIM = {c[0]: text_rgba(c[0], 104 if c[0] in ("HAHAHA", "50°C") else 82) for c in CAPS}
WM = text_rgba("© Mahmoud Elkosif", 30, CAIRO, 3)
CR1 = text_rgba("مونتاج وإخراج Mahmoud Elkosif", 58, CAIRO, 6)
CR2 = text_rgba("تابعني على فيسبوك", 50, CAIRO, 5, (255, 220, 120))


def frame(t):
    i = max(k for k, s in enumerate(SHOTS) if s[1] <= t + 1e-6)
    name, t0, t1, a, b, kind = SHOTS[i]
    p = ease((t - t0) / (t1 - t0))
    z, cx, cy = (a[j] + (b[j] - a[j]) * p for j in range(3))
    # punch-in on entry
    z *= 1 + 0.06 * max(0, 1 - (t - t0) / 0.25)
    dx = dy = ang = 0.0
    if "laugh" in kind:  # laugh bounce
        dy = 14 * abs(math.sin(t * 15)); ang = 1.2 * math.sin(t * 11)
    if "shake" in kind and t - t0 < 0.6:
        k = 1 - (t - t0) / 0.6; dx = 18 * k * math.sin(t * 70); dy = 12 * k * math.cos(t * 53)
    fr = cam(IMG[name], z, cx, cy, ang, dx, dy)
    if kind.startswith("rain"): fr = rain(fr, t)
    if kind.startswith("heat") and name != "s6": fr = heat(fr, t)
    # whip transition: motion blur + flash in the first 0.12 s
    e = t - t0
    if i > 0 and e < 0.12:
        k = int(60 * (1 - e / 0.12)) | 1
        fr = cv2.filter2D(fr, -1, np.full((1, k), 1 / k, np.float32))
        fr = cv2.addWeighted(fr, 1, np.full_like(fr, 255), 0.35 * (1 - e / 0.12), 0)
    # warm grade at sunset end
    if kind == "warm": fr = cv2.addWeighted(fr, 1, np.full_like(fr, (40, 90, 140)), 0.05, 0)
    for txt, c0, c1, y in CAPS:
        if c0 <= t <= c1:
            s = 0.6 + 0.4 * out_back((t - c0) / 0.28)
            al = min(1, (c1 - t) / 0.15)
            fr = paste(fr, CAPIM[txt], W / 2, y, s, al)
    # end card text
    if t > 18.2:
        k = ease((t - 18.2) / 0.4)
        g = np.clip((np.arange(H) - 1380) / 200, 0, 1)[:, None, None] * 0.6 * k
        fr = (fr * (1 - g)).astype(np.uint8)
        fr = paste(fr, CR1, W / 2, 1520 + 40 * (1 - k), 1, k)
        fr = paste(fr, CR2, W / 2, 1620 + 40 * (1 - k), 1, k)
    fr = paste(fr, WM, W - WM.width / 2 - 24, H - 60, 1, 0.75)
    return fr


def audio(path):
    m = tk.Mix(D)
    m.sfx("rain_storm", 0, 0.5, dur=8.9, loop=True, fade=0.4)
    m.sfx("thunder_mid", 0.1, 0.45)
    m.sfx("laugh_cartoon", 2.6, 0.75, dur=2.0)
    m.sfx("fill", 4.6, 0.5, dur=2.2)
    m.sfx("drips", 6.8, 0.35, dur=2.0)
    m.sfx("whoosh", 8.75, 0.5)
    m.sfx("wind_storm", 8.8, 0.18, dur=7.8, loop=True, fade=0.5)
    m.thump(10.3, 0.5); m.boing(12.6, 0.3)
    m.sfx("bubble", 14.6, 0.5); m.sfx("pour", 14.5, 0.35, dur=1.6)
    m.ding(14.6)
    m.sfx("giggle", 16.8, 0.5, dur=1.8); m.sfx("laugh_male", 17.4, 0.45, dur=2.2)
    m.tune(0.0, 8.8, 1.0, 0.45, minor=True)
    m.tune(8.8, 16.6, 1.15, 0.5)
    m.tune(16.6, 20.0, 1.0, 0.6)
    m.tada(18.2, 0.3)
    for _, t0, *_ in SHOTS[1:]: m.noise(t0 - 0.05, 0.15, 0.25, 3, 18)
    m.save(path)


if __name__ == "__main__":
    out = os.path.join(HERE, sys.argv[1] if len(sys.argv) > 1 else "final.mp4")
    if "--stills" in sys.argv:
        ts = [1.0, 2.2, 3.5, 5.5, 7.8, 9.5, 11.5, 13.2, 15.5, 19.0]
        ims = [cv2.resize(frame(t), (270, 480)) for t in ts]
        cv2.imwrite(os.path.join(HERE, "stills.jpg"), np.vstack([np.hstack(ims[:5]), np.hstack(ims[5:])]))
        sys.exit()
    aud = os.path.join(HERE, "sound.m4a"); audio(aud)
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", aud, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-crf", "17",
           "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
           "-c:a", "copy", "-movflags", "+faststart", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for n in range(int(D * FPS)):
        p.stdin.write(frame(n / FPS).tobytes())
    p.stdin.close(); p.wait(); print("done", out)
