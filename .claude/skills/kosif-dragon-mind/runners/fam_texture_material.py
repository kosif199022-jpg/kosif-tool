"""texture-material: method cards as real programs with known-answer checks.

Each runner builds a seeded fixture in the work folder, applies the card's method (numpy / PIL /
scipy / OpenCV / ffmpeg) and measures the produced file against the value the card's formula
predicts. Every runner carries a negative control: the same measurement on the unprocessed input
must fail. Shading cards (PBR, plush, gloss) are rendered with a numpy GGX/Schlick shader on an
analytic sphere -- the same BRDF family three.js MeshStandard/PhysicalMaterial use -- not three.js.
"""
import hashlib
import json
import math
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from _harness import card, check, fx

GAPS: dict = {
    "TEX-39": "HyperFrames media-treatment shader effects (18 keys) are interpreted by the HyperFrames runtime in "
              "headless Chrome; the card gives no shader maths and no <15 s render is wired here",
    "TEX-49": "a live CubeCamera reflection needs a WebGL three.js render loop and the demo's assets/main.bundle.js "
              "(not built in this checkout); not reproducible as a measured <15 s program here",
    "TEX-62": "texture-mask-text depends on the 66 ambientCG PNG masks shipped with the HyperFrames registry block; "
              "only the registry JSON is cached locally, the mask images are not present",
    "TEX-63": "HyperFrames material shader blocks need a WebGPU-capable Chromium (data-requires-webgpu); only "
              "SwiftShader WebGL is available here",
    "TEX-83": "warm-grain is a HyperFrames example project used as a style reference only; the local copy lacks "
              "its sub-compositions, so there is no method to execute",
    "TEX-92": "K3.makePebbles/makeBlades are three-kit WebGL instanced-geometry builders; without a WebGL render "
              "there is no measurable output beyond restating parameters",
    "TEX-93": "pond terrain with caustics lives in the three-kit demo whose assets/main.bundle.js is not built; "
              "needs a WebGL render",
    "TEX-94": "wet asphalt road ribbon lives in the three-kit demo whose assets/main.bundle.js is not built; needs "
              "a WebGL render",
}


# ----------------------------------------------------------------- helpers
def _rng(seed=7):
    return np.random.default_rng(seed)


def _save(path, a):
    a = np.clip(np.asarray(a, dtype=float), 0, 255).round().astype(np.uint8)
    Image.fromarray(a).save(path)
    return Path(path)


def _load(path):
    return np.asarray(Image.open(path).convert("RGB")).astype(float)


def _hex(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=float)


def _luma(a):
    return a[..., 0] * .2126 + a[..., 1] * .7152 + a[..., 2] * .0722


def _blur(a, s):
    from scipy.ndimage import gaussian_filter
    a = np.asarray(a, dtype=float)
    if np.ndim(s) == 0:
        s = (s, s)
    return gaussian_filter(a, tuple(s) + ((0,) if a.ndim == 3 else ()))


def _hf(a):
    a = np.asarray(a, dtype=float)
    return float(np.abs(a - _blur(a, 2)).mean())


def _video(path, frames, fps=30):
    frames = [np.clip(np.round(f), 0, 255).astype(np.uint8) for f in frames]
    h, w = frames[0].shape[:2]
    p = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                        "-s", "%dx%d" % (w, h), "-r", str(fps), "-i", "-", "-c:v", "libx264rgb", "-qp", "0",
                        "-pix_fmt", "rgb24", str(path)],
                       input=b"".join(f.tobytes() for f in frames), capture_output=True, timeout=60)
    if p.returncode:
        raise RuntimeError(p.stderr.decode()[-300:])
    return Path(path)


def _smoothstep(e0, e1, x):
    t = np.clip((np.asarray(x, dtype=float) - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def _value_noise(shape, cell, seed, octaves=1, stretch=(1, 1)):
    H, W = shape
    out, amp, tot = np.zeros(shape), 1.0, 0.0
    for o in range(octaves):
        cy, cx = max(1, cell * stretch[1] / 2 ** o), max(1, cell * stretch[0] / 2 ** o)
        g = np.random.default_rng(seed + o).random((int(H / cy) + 3, int(W / cx) + 3))
        y, x = np.mgrid[:H, :W]
        y, x = y / cy, x / cx
        y0, x0 = np.floor(y).astype(int), np.floor(x).astype(int)
        fy, fx_ = _smoothstep(0, 1, y - y0), _smoothstep(0, 1, x - x0)
        v = (g[y0, x0] * (1 - fx_) + g[y0, x0 + 1] * fx_) * (1 - fy) + (g[y0 + 1, x0] * (1 - fx_) + g[y0 + 1, x0 + 1] * fx_) * fy
        out += amp * v
        tot += amp
        amp *= .5
    return out / tot


def _corr_len(a, axis):
    a = a - a.mean()
    for lag in range(1, a.shape[axis] // 2):
        c = (a * np.roll(a, lag, axis=axis)).mean() / (a * a).mean()
        if c < .5:
            return lag
    return a.shape[axis] // 2


def _spectral_slope(img, f_lo, f_hi):
    a = img - img.mean()
    P = np.abs(np.fft.fftshift(np.fft.fft2(a))) ** 2
    H, W = a.shape
    fy = np.fft.fftshift(np.fft.fftfreq(H))[:, None]
    fx_ = np.fft.fftshift(np.fft.fftfreq(W))[None]
    f = np.hypot(fy, fx_)
    bins = np.geomspace(f_lo, f_hi, 12)
    xs, ys = [], []
    for lo, hi in zip(bins[:-1], bins[1:]):
        m = (f >= lo) & (f < hi)
        if m.any():
            xs.append(math.log((lo * hi) ** .5))
            ys.append(math.log(P[m].mean() + 1e-12))
    return float(np.polyfit(xs, ys, 1)[0])


def _prompt_lock(wd, name, block, scenes, forbidden):
    prompts = ["%s\n\nSTYLE LOCK:\n%s" % (s, block) for s in scenes]
    out = wd / ("%s_prompts.json" % name)
    out.write_text(json.dumps({"style_block": block, "prompts": prompts}, ensure_ascii=False, indent=1), "utf-8")
    back = json.loads(out.read_text("utf-8"))["prompts"]
    hashes = {hashlib.sha256(p.split("STYLE LOCK:\n", 1)[1].encode()).hexdigest() if "STYLE LOCK:\n" in p else None
              for p in back}
    raw_has = sum(block in s for s in scenes)
    bad = [w for w in forbidden if any(w.lower() in p.lower() for p in back)]
    return [check("every prompt carries the style block verbatim", all(block in p for p in back), len(back), len(scenes)),
            check("one identical style block hash across prompts", len(hashes) == 1 and None not in hashes, len(hashes), 1),
            check("forbidden words absent", not bad, bad, []),
            check("negative control: raw scene prompts lack the block", raw_has == 0, raw_has, 0)], [out]


def _sphere(n=128):
    yy, xx = (np.mgrid[:n, :n] + .5) / n * 2 - 1
    yy = -yy
    r2 = xx * xx + yy * yy
    inside = r2 < 1
    z = np.sqrt(np.clip(1 - r2, 0, 1))
    N = np.stack([xx, yy, z], -1)
    return N, inside


def _norm(v):
    v = np.asarray(v, dtype=float)
    return v / np.linalg.norm(v, axis=-1, keepdims=True)


def _ggx(N, V, L, base, metal, rough, light=3.0):
    """Cook-Torrance GGX / Smith-Schlick / Fresnel-Schlick, as in three.js MeshStandardMaterial."""
    H = _norm(V + L)
    nl = np.clip((N * L).sum(-1), 0, 1)
    nv = np.clip((N * V).sum(-1), 1e-4, 1)
    nh = np.clip((N * H).sum(-1), 0, 1)
    vh = np.clip((V * H).sum(-1), 0, 1)
    a = max(rough, .02) ** 2
    D = a * a / (math.pi * (nh * nh * (a * a - 1) + 1) ** 2)
    k = a / 2
    G = (nl / (nl * (1 - k) + k)) * (nv / (nv * (1 - k) + k))
    F0 = .04 * (1 - metal) + base * metal
    F = F0 + (1 - F0) * ((1 - vh) ** 5)[..., None]
    spec = (D * G / (4 * nl * nv + 1e-4))[..., None] * F
    diff = base * (1 - metal) / math.pi * (1 - F)
    return (diff + spec) * (nl * light)[..., None], spec * (nl * light)[..., None]


def _to8(lin):
    return np.clip(lin, 0, 1) ** (1 / 2.2) * 255


# ----------------------------------------------------------------- cards
@card("TEX-01")
def stepped_grain(task, wd):
    H, W, fps = 90, 160, 30
    fields = []
    for k in range(6):   # 6 positions, fractal noise (2 octaves, fine), desaturated
        n = .65 * _blur(np.random.default_rng(100 + k).random((H, W)), .6) + .35 * _blur(np.random.default_rng(200 + k).random((H, W)), 1.2)
        fields.append((n - n.min()) / (n.max() - n.min()))
    yy, xx = np.mgrid[:H, :W]
    r = np.hypot((xx - W / 2) / (W / 2), (yy - H / 2) / (H / 2)) / math.sqrt(2)
    vig = 1 - .42 * _smoothstep(.55, 1, r)
    base = np.full((H, W), 205 / 255)

    def soft_light(b, s):   # W3C soft-light, backdrop b, source s
        d = np.where(b <= .25, ((16 * b - 12) * b + 4) * b, np.sqrt(b))
        return np.where(s <= .5, b - (1 - 2 * s) * b * (1 - b), b + (2 * s - 1) * (d - b))

    def frame(t, grain=True):
        k = int(math.floor(t / .1 + 1e-9)) % 6          # 0.6 s loop, steps(1)
        g = fields[k] if grain else np.full((H, W), .5)
        c = base * (1 - .09) + soft_light(base, g) * .09
        return np.stack([c * vig * 255] * 3, -1)
    n = 36
    vid = _video(wd / "grain_stepped.mp4", [frame(i / fps) for i in range(n)], fps)
    v = fx.frames(vid, (W, H))
    changes = [i for i in range(1, n) if np.abs(v[i] - v[i - 1]).max() > 0]
    exp_changes = [i for i in range(1, n) if int(math.floor(i / fps / .1 + 1e-9)) != int(math.floor((i - 1) / fps / .1 + 1e-9))]
    loop = float(np.abs(v[0] - v[18]).max())
    grey = float(np.abs(v[5][..., 0] - v[5][..., 2]).max())
    corner, centre = float(v[0][:6, :6, 0].mean()), float(v[0][40:50, 75:85, 0].mean())
    plate = [frame(i / fps, False) for i in range(6)]
    plate_changes = sum(np.abs(plate[i] - plate[i - 1]).max() > 0 for i in range(1, 6))
    return [check("frames change only at the 0.1 s step boundaries", changes == exp_changes, changes[:6], exp_changes[:6]),
            check("0.6 s loop: frame 0 == frame 18", loop == 0, loop, 0),
            check("grain is desaturated (R == B)", grey == 0, grey, 0),
            check("vignette darkens the corners", corner < centre * .75, [corner, centre], "corner < .75 centre"),
            check("negative control: the plate without grain never changes", plate_changes == 0, int(plate_changes), 0)], [vid]


@card("TEX-03")
def gaussian_grain(task, wd):
    H, W = 180, 320
    yy, xx = np.mgrid[:H, :W]
    src = np.stack([60 + xx / W * 120, 80 + yy / H * 90, 100 + 0 * xx], -1)
    amount, seed = .018, 3
    p_in = _save(wd / "plate.png", src)

    def grain(img, s):
        n = np.random.default_rng(s).normal(0, amount * 255, img.shape[:2])
        return img + n[..., None]          # luminance grain: the same value on every channel
    a = _load(p_in)
    out = _save(wd / "grain.png", grain(a, seed))
    d = _load(out) - a
    std, mean = float(d.std()), float(d.mean())
    lum_only = float(np.abs(d[..., 0] - d[..., 2]).max())
    same = np.array_equal(grain(a, seed), grain(a, seed))
    diff_seed = not np.array_equal(grain(a, seed), grain(a, seed + 1))
    return [check("grain std = amount * 255", abs(std - amount * 255) / (amount * 255) < .06, std, amount * 255),
            check("zero mean", abs(mean) < .1, mean, 0),
            check("luminance grain (same on R and B)", lum_only == 0, lum_only, 0),
            check("seeded: same seed identical, seed=frame differs", same and diff_seed, True, True),
            check("negative control: the plate itself has no fine noise (high-pass std)", float((a - _blur(a, 1)).std()) < 1,
                  float((a - _blur(a, 1)).std()), "<1 vs %.1f" % float((_load(out) - _blur(_load(out), 1)).std()))], [out]


@card("TEX-04")
def ffmpeg_finish(task, wd):
    H, W = 180, 320
    src = np.full((H, W, 3), 110.0)
    src[70:110, 140:180] = 255
    p_in = _save(wd / "graded.png", src)
    bar = int(round((H - W / 2.39) / 2))
    chain = ("split[a][b];[b]gblur=sigma=20[bl];[a][bl]blend=all_mode=screen:all_opacity=0.25,"
             "noise=alls=8:allf=t+u,vignette=PI/5,"
             "drawbox=x=0:y=0:w=iw:h=%d:color=black:t=fill,drawbox=x=0:y=ih-%d:w=iw:h=%d:color=black:t=fill" % (bar, bar, bar))
    fx.ffmpeg("-loop", "1", "-i", str(p_in), "-filter_complex", chain, "-frames:v", "3", str(wd / "finish_%d.png"))
    mp4 = wd / "finish.mp4"
    fx.ffmpeg("-loop", "1", "-t", "2", "-i", str(p_in), "-filter_complex", chain + ",format=yuv420p", "-c:v", "libx264",
              "-crf", "18", str(mp4))
    f1, f2 = _load(wd / "finish_1.png"), _load(wd / "finish_2.png")
    bars = float(max(f1[:bar].mean(), f1[H - bar:].mean()))
    corner = float(f1[bar + 2:bar + 12, 2:12].mean())
    centre = float(f1[60:66, 60:70].mean())
    glow = float(f1[60:66, 150:170].mean()) - float(f1[60:66, 20:40].mean())
    tg = float((f1[50:65, 40:100] - f2[50:65, 40:100]).std())
    inp = _load(p_in)
    return [check("2.39:1 letterbox bars are black (%d px)" % bar, bars < 2, bars, "<2"),
            check("vignette PI/5 darkens the corners", corner < .9 * centre, [corner, centre], "corner < .9 centre"),
            check("screen-blended bloom lifts pixels around the highlight", glow > 3, glow, ">3"),
            check("temporal grain differs frame to frame", tg > 3, tg, ">3"),
            check("negative control: the graded input has no bars", float(inp[:bar].mean()) > 50, float(inp[:bar].mean()), ">50")], \
        [wd / "finish_1.png", mp4]


def _glsl_rand(u, v):
    x = np.sin(u * 12.9898 + v * 78.233) * 43758.5453
    return x - np.floor(x)


@card("TEX-06")
def film_pass(task, wd):
    H, W, fps, intensity = 120, 200, 30, .16
    yy, xx = (np.mgrid[:H, :W] + .5)
    u, v = xx / W, yy / H
    base = np.full((H, W, 3), 100 / 255)

    def frame(n):
        t = n / fps                    # time uniform written from the output frame
        fu, fv = (u + t) % 1, (v + t) % 1
        noise = _glsl_rand(fu, fv)[..., None]
        col = base + base * np.clip(.1 + noise, 0, 1)
        return (base + (col - base) * intensity) * 255
    frames = [frame(n) for n in range(10)]
    vid = _video(wd / "filmpass.mp4", frames, fps)
    vv = fx.frames(vid, (W, H))
    ratio = float(vv[3].mean() / 100)
    expect = 1 + intensity * .595
    seek = np.array_equal(np.round(frame(3)), vv[3])
    moving = float(np.abs(vv[3] - vv[4]).mean())
    return [check("mean gain = 1 + intensity * E[clamp(.1+u,0,1)] = 1.0952", abs(ratio - expect) < .004, ratio, expect),
            check("seekable: re-rendering frame 3 gives the same pixels", seek, seek, True),
            check("grain changes with the frame time", moving > .5, moving, ">0.5"),
            check("negative control: the base plate has gain 1", abs(1.0 - expect) > .004, 1.0, expect)], [vid]


@card("TEX-07")
def grain_edge_ca(task, wd):
    H, W = 500, 1000
    yy, xx = np.mgrid[:H, :W].astype(float)
    src = np.full((H, W), 30.0)
    src[:, ::50] = 255
    src[:, 1::50] = 255
    cx, cy = W / 2, H / 2
    r = np.hypot(xx - cx, yy - cy)
    rmax = math.hypot(cx, cy)
    sh = .002 * W * (r / rmax) ** 2            # 0 at centre, .002 uv at the corners
    dirx = (xx - cx) / np.maximum(r, 1e-6)
    from scipy.ndimage import map_coordinates

    def samp(dx):
        return map_coordinates(src, [yy, xx - dx], order=1, mode="nearest")
    R, G, B = samp(sh * dirx), src, samp(-sh * dirx)
    clean = np.stack([R, G, B], -1)
    g = np.random.default_rng(7).normal(0, .02 * 255, (H, W))[..., None]
    out = _save(wd / "grain_ca.png", clean + g)
    o = _load(out)
    def rb(x0, x1):
        a, b = o[240:260, x0:x1, 2], o[240:260, x0:x1, 0]
        return min(range(-6, 7), key=lambda s: np.mean((np.roll(a, s, axis=1) - b) ** 2))
    centre = rb(450, 550)
    edge = rb(880, 990)
    exp_edge = 2 * .002 * W * ((935 - cx) / rmax) ** 2
    gr = o - np.round(np.clip(clean, 0, 255))
    gstd = float(gr[100:400, 100:900, 1][src[100:400, 100:900] == 30].std())
    mono = float(np.corrcoef(gr[..., 0][src == 30].ravel()[:20000], gr[..., 2][src == 30].ravel()[:20000])[0, 1])
    inp = np.stack([src] * 3, -1)
    neg = min(range(-6, 7), key=lambda s: np.mean((np.roll(inp[240:260, 880:990, 2], s, 1) - inp[240:260, 880:990, 0]) ** 2))
    return [check("no RGB split at the centre", centre == 0, centre, 0),
            check("R-B split near the edge = 2 x .002 W (r/rmax)^2", abs(edge - exp_edge) <= 1, edge, exp_edge),
            check("grain 2% (std ~5.1 levels)", abs(gstd - 5.1) < .6, gstd, 5.1),
            check("grain is monochrome (R/B correlation)", mono > .95, mono, ">0.95"),
            check("negative control: the input has no edge split", neg == 0 and abs(neg - exp_edge) > 1, neg, exp_edge)], [out]


@card("TEX-16")
def paper_collage(task, wd):
    import cv2
    H, W = 270, 480
    rng = _rng(16)
    paper = 228 + 14 * (_value_noise((H, W), 8, 1, 4) - .5)
    canvas = Image.fromarray(np.stack([paper, paper * .97, paper * .9], -1).clip(0, 255).astype(np.uint8)).convert("RGBA")
    cols = [(200, 60, 50), (40, 110, 170), (230, 180, 40)]
    angles = []
    for i, c in enumerate(cols):
        ang = float(rng.uniform(2, 6) * rng.choice([-1, 1]))
        angles.append(ang)
        cut = Image.new("RGBA", (120, 90), c + (255,))
        rot = cut.rotate(ang, expand=True, resample=Image.NEAREST)
        x, y = 40 + i * 140, 80 + (i % 2) * 40
        sh = Image.new("RGBA", rot.size, (0, 0, 0, 0))
        sh.putalpha(Image.fromarray((np.asarray(rot)[..., 3] * .35).astype(np.uint8)))
        sh_arr = np.asarray(sh).astype(float)
        sh_arr[..., 3] = _blur(sh_arr[..., 3], 4)
        canvas.alpha_composite(Image.fromarray(sh_arr.astype(np.uint8)), (x + 4, y + 6))
        canvas.alpha_composite(rot, (x, y))
    out = wd / "collage.png"
    canvas.convert("RGB").save(out)
    o = _load(out)
    meas = []
    for c in cols:
        m = (np.abs(o - c).sum(-1) < 6).astype(np.uint8)
        cnts, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        rect = cv2.minAreaRect(max(cnts, key=cv2.contourArea))
        a = abs(rect[2]) % 90
        meas.append(min(a, 90 - a))
    m0 = (np.abs(o - cols[0]).sum(-1) < 6)
    ys, xs = np.nonzero(m0)
    below = float(o[ys.max() + 3, int(xs.mean()), 0])
    paper_ref = float(o[5:20, 5:20, 0].mean())
    flat = np.zeros((90, 120), np.uint8)
    flat[10:80, 10:110] = 1
    cn, _ = cv2.findContours(flat, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    a0 = cv2.minAreaRect(cn[0])[2] % 90
    return [check("cut-outs rotated 2-6 degrees (measured)", all(1.5 <= m <= 6.5 for m in meas), meas, "2..6"),
            check("measured angles match the applied ones", max(abs(m - abs(a)) for m, a in zip(meas, angles)) < 1, meas, [abs(a) for a in angles]),
            check("soft drop shadow below the cut-out", below < paper_ref - 8, [below, paper_ref], "darker"),
            check("negative control: an unrotated card measures 0 degrees", min(a0, 90 - a0) < 1.5, float(a0), 0)], [out]


@card("TEX-17")
def cutout_board(task, wd):
    W, H, fps = 160, 90, 10
    cuts = [(20, 20, (200, 70, 60)), (90, 18, (60, 130, 200)), (25, 55, (230, 190, 50)), (95, 52, (90, 170, 90))]

    def mg101(t):
        img = np.full((H, W, 3), 225.0)
        for i, (x, y, c) in enumerate(cuts):
            t0 = 1 + i * .75
            p = float(np.clip((t - t0) / .5, 0, 1))
            if p > 0:
                s = int(round(14 * p))
                img[y + 7 - s // 2:y + 7 + (s + 1) // 2, x + 20 - s:x + 20 + s] = c
        return img

    def mg102(t):
        img = np.full((H, W, 3), 225.0)
        img[20:70, 40:120] = (120, 140, 160)
        p = float(np.clip((t - 1) / 1.0, 0, 1))          # tape revealed by a mask 1-2 s
        n = int(round(40 * p))
        img[16:24, 100:100 + n] = img[16:24, 100:100 + n] * .3 + np.array([245, 235, 200]) * .7
        img[24:26, 100:100 + n] *= .92                    # very light tape shadow
        return img
    a = [mg101(i / fps) for i in range(70)]
    b = [mg102(i / fps) for i in range(40)]
    v1, v2 = _video(wd / "mg101.mp4", a, fps), _video(wd / "mg102.mp4", b, fps)
    f1, f2 = fx.frames(v1, (W, H)), fx.frames(v2, (W, H))
    vis = lambda fr: sum(int((np.abs(fr - c).sum(-1) < 6).sum() > 100) for _, _, c in cuts)  # noqa: E731
    d1 = float(fx.probe(v1)["format"]["duration"])
    def tape_cov(fr):
        return float((np.abs(fr[16:24, 100:140] - (fr[30, 30] * 0 + 225) * 1).sum(-1) > 10).mean())
    cov15, cov20 = tape_cov(f2[15]), tape_cov(f2[20])
    shadow = float(f2[30][24, 110, 0] / f2[30][28, 110, 0])
    return [check("MG-101: no cut-outs during the 0-1 s background", vis(f1[5]) == 0, vis(f1[5]), 0),
            check("MG-101: all four cut-outs on the board by 4.5 s", vis(f1[45]) == 4, vis(f1[45]), 4),
            check("MG-101 runs 7 s", abs(d1 - 7) < .15, d1, 7),
            check("MG-102: tape half revealed at 1.5 s, full at 2 s", abs(cov15 - .5) < .06 and cov20 > .97, [cov15, cov20], [.5, 1]),
            check("tape shadow very light (>= 0.9 of paper)", shadow >= .9, shadow, ">=0.9"),
            check("negative control: the t=0 frame does not show the board", vis(f1[0]) != 4, vis(f1[0]), 4)], [v1, v2]


@card("TEX-18")
def paper_tear(task, wd):
    W, H = 640, 360
    rng = _rng(18)
    ys = np.arange(0, H + 12, 12)
    jit = rng.uniform(-13, 13, len(ys))
    ex = W / 2 + jit
    yy, xx = np.mgrid[:H, :W]
    edge_x = np.interp(yy[:, 0], ys, ex)[:, None]
    left0 = xx < edge_x
    right0 = ~left0
    a_scene, b_scene = np.array([230, 220, 200.0]), np.array([30, 60, 120.0])

    def frame(t):
        p = float(_smoothstep(.7, 2.5, t))
        off = 170 * p
        img = np.tile(b_scene, (H, W, 1))
        for mask, sgn in ((left0, -1), (right0, 1)):
            sh = int(round(sgn * off))
            m = np.roll(mask, sh, axis=1)
            if sgn < 0 and sh:
                m[:, W + sh:] = False
            if sgn > 0 and sh:
                m[:, :sh] = False
            img[m] = a_scene
            e = m & ~np.roll(m, -4 * sgn, axis=1) if sh else np.zeros_like(m)
            img[e] = 255   # 4 px white torn edge
        return img
    f0, f1 = frame(0), frame(2.5)
    p0, p1 = _save(wd / "tear_t0.png", f0), _save(wd / "tear_t2_5.png", f1)
    o1 = _load(p1)
    gap = [(np.abs(o1[y] - b_scene).sum(-1) < 6).sum() for y in range(10, H - 10, 20)]
    union_ok = bool((left0 | right0).all() and not (left0 & right0).any())
    spacing = float(np.diff(ys).mean())
    def edge_jitter(mask):   # right boundary of the left half, row by row, relative to the cut line
        xs = np.array([np.nonzero(mask[y])[0].max() + 1 for y in range(H)], float)
        return float(xs.std()), float(np.abs(xs - W / 2).max())
    jstd, jmax = edge_jitter(left0)
    sstd, _ = edge_jitter(xx < W / 2)
    o0 = _load(p0)
    revealed0 = int((np.abs(o0 - b_scene).sum(-1) < 6).sum())
    return [check("both halves share one edge (partition, no gap/overlap at t=0)", union_ok and revealed0 == 0, revealed0, 0),
            check("edge sampled every 12 px", spacing == 12, spacing, 12),
            check("seeded jitter within +-13 px and not smooth (measured edge)", jmax <= 13.5 and jstd > 4, [jmax, jstd], "<=13 / >4"),
            check("halves pulled +-170 px reveal a 340 px slit", all(abs(g - 340) <= 2 for g in gap), [int(min(gap)), int(max(gap))], 340),
            check("white torn edge present", bool((np.abs(o1 - 255).sum(-1) < 3).sum() > 4 * H), int((np.abs(o1 - 255).sum(-1) < 3).sum()), ">4H"),
            check("negative control: a straight cut measured the same way has no jitter", sstd <= 4, sstd, ">4")], [p0, p1]


@card("TEX-21")
def archival_lock(task, wd):
    block = ("Archival scrapbook: sepia newsprint, fine film grain, scan lines, halftone dots, torn photo edges, "
             "brass tacks, red thread between clues, projector flicker; generic stamps only.")
    return _prompt_lock(wd, "vox_history", block, ["Clip %d: 1920s harbour, a map unfolds." % i for i in range(1, 6)],
                        ["coca-cola", "nike", "logo of"])


@card("TEX-22")
def paper_bg_lock(task, wd):
    block = "Flat hand-drawn paper whiteboard background, pencil texture, plain off-white, no depth."
    c, o = _prompt_lock(wd, "stickman", block, ["Shot %d: the stick figure waves." % i for i in range(1, 6)],
                        ["photoreal", "bokeh", "depth of field", "3d render", "cinematic lighting"])
    return c, o


@card("TEX-27")
def wabi_sabi(task, wd):
    rng = _rng(27)
    W, H = 400, 240
    n = 6
    rot = rng.uniform(-2, 2, n)
    rot = np.where(np.abs(rot) < .5, np.sign(rot + 1e-9) * .8, rot)
    widths = 4 * (1 + rng.uniform(-.15, .15, n))
    canvas = Image.new("RGB", (W, H), (240, 232, 215))
    paper = (_value_noise((H, W), 6, 2, 3) - .5) * 16
    arr = np.asarray(canvas).astype(float) + paper[..., None]
    canvas = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    for i in range(n):
        el = Image.new("RGBA", (60, 60), (0, 0, 0, 0))
        d = ImageDraw.Draw(el)
        d.rectangle([10, 10, 50, 50], outline=(60, 50, 40, 255), width=int(round(widths[i])))
        el = el.rotate(rot[i], resample=Image.BICUBIC)
        canvas.paste(el, (20 + i * 62, 30), el)
    # data label: kept clean (no texture, no rotation)
    d = ImageDraw.Draw(canvas)
    d.rectangle([20, 150, 220, 200], fill=(255, 255, 255))
    d.text((30, 160), "42.7%", font=ImageFont.load_default(size=28), fill=(20, 20, 20))
    out = wd / "wabi_sabi.png"
    canvas.save(out)
    ref = Image.new("RGB", (W, H))
    rd = ImageDraw.Draw(ref)
    rd.rectangle([20, 150, 220, 200], fill=(255, 255, 255))
    rd.text((30, 160), "42.7%", font=ImageFont.load_default(size=28), fill=(20, 20, 20))
    o = _load(out)
    label_clean = float(np.abs(o[150:201, 20:221] - np.asarray(ref).astype(float)[150:201, 20:221]).max())
    paper_var = float(o[210:235, 250:390].std())
    (wd / "imperfection.json").write_text(json.dumps({"rotation_deg": rot.tolist(), "stroke": widths.tolist()}), "utf-8")
    return [check("element rotations within +-1-2 degrees, none zero", bool(np.all(np.abs(rot) <= 2) and np.all(np.abs(rot) > .3)), rot.tolist(), "±1..2"),
            check("stroke widths vary within +-15%", bool(np.all(np.abs(widths / 4 - 1) <= .15) and widths.std() > 0), widths.tolist(), "4 ±15%"),
            check("paper texture present", paper_var > 1.5, paper_var, ">1.5"),
            check("data label stays pixel-clean", label_clean == 0, label_clean, 0),
            check("negative control: an untextured canvas has no paper variation", float(np.full((25, 140), 240.0).std()) <= 1.5, 0.0, ">1.5")], \
        [out, wd / "imperfection.json"]


@card("TEX-28")
def corner_knockout(task, wd):
    from scipy.ndimage import label
    H, W = 160, 200
    rng = _rng(28)
    bgc = np.array([40, 120, 200.0])
    img = bgc + rng.normal(0, 6, (H, W, 3))
    yy, xx = np.mgrid[:H, :W]
    subj = np.hypot(yy - 80, xx - 100) < 50
    img[subj] = (210, 60, 50)
    hole = np.hypot(yy - 80, xx - 100) < 12        # bg-coloured but enclosed: must stay
    img[hole] = bgc
    p_in = _save(wd / "scene.png", img)
    a = _load(p_in)
    corners = np.array([a[:4, :4].reshape(-1, 3), a[:4, -4:].reshape(-1, 3), a[-4:, :4].reshape(-1, 3), a[-4:, -4:].reshape(-1, 3)]).reshape(-1, 3).mean(0)
    near = np.linalg.norm(a - corners, axis=-1) <= 34
    lab, _ = label(near)
    seeds = {lab[0, 0], lab[0, -1], lab[-1, 0], lab[-1, -1]} - {0}
    bg = np.isin(lab, list(seeds))
    rgba = np.dstack([a, np.where(bg, 0, 255)])
    out = wd / "knockout.png"
    Image.fromarray(rgba.astype(np.uint8), "RGBA").save(out)
    al = np.asarray(Image.open(out))[..., 3]
    true_bg = ~subj
    acc = float((((al == 0) == true_bg)).mean())
    hole_kept = float((al[hole] == 255).mean())
    inp_alpha = np.asarray(Image.open(p_in).convert("RGBA"))[..., 3]
    return [check("background removed by corner-colour flood (pixel accuracy)", acc > .99, acc, ">0.99"),
            check("enclosed bg-coloured region kept (flood, not global key)", hole_kept == 1, hole_kept, 1),
            check("subject fully opaque", float((al[subj & ~hole] == 255).mean()) == 1, float((al[subj & ~hole] == 255).mean()), 1),
            check("negative control: the input has no transparency", int((inp_alpha == 0).sum()) == 0, int((inp_alpha == 0).sum()), 0)], [out]


@card("TEX-30")
def cmyk_halftone(task, wd):
    H, W, cell, ss = 192, 192, 8, 2
    yy, xx = np.mgrid[:H, :W]
    rgb = np.stack([180 + 50 * np.sin(xx / 40.0), 120 + 60 * np.cos(yy / 30.0), 90 + 0 * xx + 40 * (xx > 96)], -1) / 255
    K = 1 - rgb.max(-1)
    C = (1 - rgb[..., 0] - K) / np.maximum(1 - K, 1e-6)
    M = (1 - rgb[..., 1] - K) / np.maximum(1 - K, 1e-6)
    Y = (1 - rgb[..., 2] - K) / np.maximum(1 - K, 1e-6)
    Y2, X2 = (np.mgrid[:H * ss, :W * ss] + .5) / ss
    from scipy.ndimage import map_coordinates
    planes, covs = {}, {}
    for name, ch, ang in (("C", C, 15), ("M", M, 75), ("Y", Y, 0), ("K", K, 45)):
        a = math.radians(ang)
        u = X2 * math.cos(a) + Y2 * math.sin(a)
        v = -X2 * math.sin(a) + Y2 * math.cos(a)
        best = np.zeros_like(u)
        for du in (-1, 0, 1):          # 3x3 neighbour cells avoid clipped dots
            for dv in (-1, 0, 1):
                cu = (np.floor(u / cell) + .5 + du) * cell
                cv = (np.floor(v / cell) + .5 + dv) * cell
                px = cu * math.cos(a) - cv * math.sin(a)
                py = cu * math.sin(a) + cv * math.cos(a)
                cov = map_coordinates(ch, [np.clip(py, 0, H - 1), np.clip(px, 0, W - 1)], order=1)
                r = cell * np.sqrt(np.clip(cov, 0, 1) / math.pi)
                best = np.maximum(best, (np.hypot(u - cu, v - cv) <= r).astype(float))
        planes[name] = best.reshape(H, ss, W, ss).mean(axis=(1, 3))
        covs[name] = (float(planes[name].mean()), float(ch.mean()))
    out_rgb = np.stack([(1 - planes["C"]) * (1 - planes["K"]), (1 - planes["M"]) * (1 - planes["K"]),
                        (1 - planes["Y"]) * (1 - planes["K"])], -1) * 255
    out = _save(wd / "cmyk_halftone.png", out_rgb)
    kp = _save(wd / "K_plane.png", np.stack([planes["K"] * 255] * 3, -1))
    kb = _load(kp)[..., 0] / 255
    def peak_angle(a):
        F = np.abs(np.fft.fftshift(np.fft.fft2(a - a.mean())))
        cy, cx = H // 2, W // 2
        F[cy - 3:cy + 4, cx - 3:cx + 4] = 0
        py, px = np.unravel_index(np.argmax(F), F.shape)
        return math.degrees(math.atan2(-(py - cy), px - cx)) % 90, float(F.max() / (F.mean() + 1e-9))
    ang, sharp = peak_angle(kb)
    err = max(abs(a - b) for a, b in covs.values())
    ang_in, sharp_in = peak_angle(K)
    return [check("ink coverage per channel matches the source (max abs error)", err < .06, err, "<0.06"),
            check("K screen at 45 degrees (FFT peak)", abs(ang - 45) < 4, ang, 45),
            check("strong periodic screen in the K plate", sharp > 50, sharp, ">50"),
            check("negative control: the continuous-tone K has no 45-degree screen", abs(ang_in - 45) > 4, ang_in, "!= 45")], [out, kp]


@card("TEX-31")
def clipped_halftone(task, wd):
    W, H, s = 320, 200, 1.0
    bg, txt = np.array([250, 245, 235.0]), np.array([30, 40, 90.0])
    img = np.tile(bg, (H, W, 1))
    card_box = (40, 30, 280, 170)
    yy, xx = np.mgrid[:H, :W] + .5
    inside = (xx >= card_box[0]) & (xx < card_box[2]) & (yy >= card_box[1]) & (yy < card_box[3])
    cx = (np.floor(xx / (10 * s)) + .5) * 10 * s
    cy = (np.floor(yy / (10 * s)) + .5) * 10 * s
    sel = ((np.floor(xx / (10 * s)) + np.floor(yy / (10 * s))) % 4 == 0)
    dot = (np.hypot(xx - cx, yy - cy) <= 1.7 * s) & sel & inside       # ctx.clip(card)
    img[dot] = bg * .92 + txt * .08
    out = _save(wd / "halftone_card.png", img)
    o = _load(out)
    lit = np.abs(o - bg).sum(-1) > 0
    outside = int((lit & ~inside).sum())
    col = o[lit][0]
    exp = np.round(bg * .92 + txt * .08)
    cells = {(int(a // 10), int(b // 10)) for a, b in zip(*np.nonzero(lit))}
    diag = all((cx_ + cy_) % 4 == 0 for cy_, cx_ in cells)
    inp = np.tile(bg, (H, W, 1))
    return [check("no dot outside the card clip", outside == 0, outside, 0),
            check("dot colour = 8% of the text colour over the card", float(np.abs(col - exp).max()) <= 1, col.tolist(), exp.tolist()),
            check("dots only in cells with (i+j) % 4 == 0", diag and len(cells) > 50, len(cells), ">50"),
            check("negative control: the plain card has no dots", int((np.abs(inp - bg).sum(-1) > 0).sum()) == 0, 0, ">0")], [out]


@card("TEX-38")
def dot_lattice(task, wd):
    H, W = 180, 320
    hero = np.full((H, W, 3), 18.0)
    yy, xx = np.mgrid[:H, :W] + .5
    dot = (np.hypot((xx % 6) - 3, (yy % 6) - 3) <= .6 + .5)

    def overlay(alpha_hex, opacity):
        a = int(alpha_hex, 16) / 255 * opacity
        return hero + dot[..., None] * (255 - hero) * a
    outs, amps = [], {}
    for name, (ah, op) in {"web_ff16": ("16", .25), "video_ff40": ("40", 1.0)}.items():
        frames = [overlay(ah, op)] * 5
        p = wd / ("lattice_%s.mp4" % name)
        fx.ffmpeg("-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % (W, H), "-r", "10", "-i", "pipe:0",
                  "-c:v", "libx264", "-crf", "23", "-pix_fmt", "yuv420p", str(p)) if False else None
        proc = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                               "-s", "%dx%d" % (W, H), "-r", "10", "-i", "-", "-c:v", "libx264", "-crf", "23",
                               "-pix_fmt", "yuv420p", str(p)], input=b"".join(np.clip(f, 0, 255).astype(np.uint8).tobytes() for f in frames),
                              capture_output=True, timeout=30)
        if proc.returncode:
            raise RuntimeError(proc.stderr.decode()[-200:])
        v = fx.frames(p, (W, H))[2][..., 1]
        F = np.abs(np.fft.rfft(v.mean(0) - v.mean()))
        amps[name] = float(v[dot].mean() - v[~dot].mean())
        amps[name + "_peak6"] = int(np.argmax(F[1:]) + 1)
        outs.append(p)
    flat = hero[..., 1]
    Fh = np.abs(np.fft.rfft(flat.mean(0) - flat.mean()))
    return [check("video strength (#fff40) survives H.264 (dot contrast > 3 levels)", amps["video_ff40"] > 3, amps["video_ff40"], ">3"),
            check("video strength is >= 2.5x the web strength after H.264", amps["video_ff40"] >= 2.5 * amps["web_ff16"],
                  [amps["web_ff16"], amps["video_ff40"]], "video >= 2.5x web"),
            check("lattice period 6 px (FFT peak at W/6)", amps["video_ff40_peak6"] in (53, 54), amps["video_ff40_peak6"], W / 6),
            check("negative control: the bare hero has no lattice", float(Fh.max()) < 1e-6, float(Fh.max()), 0)], outs


def _panel_fixture(H=200, W=320, seed=41):
    rng = _rng(seed)
    yy, xx = np.mgrid[:H, :W]
    bg = np.stack([40 + 30 * np.sin(xx / 7.0), 30 + 25 * np.cos(yy / 5.0), 60 + 30 * np.sin((xx + yy) / 9.0)], -1)
    bg += rng.normal(0, 8, bg.shape)
    return np.clip(bg, 0, 255)


@card("TEX-41")
def frosted_panel(task, wd):
    H, W = 200, 320
    bg = _panel_fixture(H, W)
    x0, y0, x1, y1 = 60, 40, 260, 140
    out = bg.copy()
    # wide ambient shadow 0 24px 80px rgba(0,0,0,.25): offset 24, blur sigma 40
    m = np.zeros((H, W))
    m[y0:y1, x0:x1] = 1
    sh = _blur(np.roll(m, 24, axis=0), 40) * .25
    out = out * (1 - sh[..., None])
    blurred = _blur(bg, 28)
    panel = blurred * .95 + 255 * .05
    out[y0:y1, x0:x1] = panel[y0:y1, x0:x1]
    hgt = y1 - y0
    for y in range(y0, y1):     # 1 px gradient border .12 -> .02 top to bottom
        a = .12 + (.02 - .12) * (y - y0) / (hgt - 1)
        for x in (x0, x1 - 1):
            out[y, x] = out[y, x] * (1 - a) + 255 * a
    out[y0, x0:x1] = out[y0, x0:x1] * 0 + (panel[y0, x0:x1] * (1 - .12) + 255 * .12)
    out[y1 - 1, x0:x1] = panel[y1 - 1, x0:x1] * (1 - .02) + 255 * .02
    p = _save(wd / "frosted.png", out)
    o = _load(p)
    hf_in, hf_out = _hf(bg[y0 + 5:y1 - 5, x0 + 5:x1 - 5]), _hf(o[y0 + 5:y1 - 5, x0 + 5:x1 - 5])
    fill_err = float(np.abs(o[y0 + 5:y1 - 5, x0 + 5:x1 - 5] - np.round(np.clip(blurred * .95 + 12.75, 0, 255))[y0 + 5:y1 - 5, x0 + 5:x1 - 5]).max())
    top_a = float(((o[y0, x0 + 50:x1 - 50] - panel[y0, x0 + 50:x1 - 50]) / (255 - panel[y0, x0 + 50:x1 - 50])).mean())
    bot_a = float(((o[y1 - 1, x0 + 50:x1 - 50] - panel[y1 - 1, x0 + 50:x1 - 50]) / (255 - panel[y1 - 1, x0 + 50:x1 - 50])).mean())
    below = float(o[y1 + 20:y1 + 30, 150:170].mean() / bg[y1 + 20:y1 + 30, 150:170].mean())
    return [check("28 px backdrop blur removes texture inside the panel (HF ratio)", hf_out < .1 * hf_in, hf_out / hf_in, "<0.1"),
            check("5% white fill over the blurred backdrop", fill_err <= 1, fill_err, "<=1"),
            check("top-lit border .12 -> .02", abs(top_a - .12) < .02 and abs(bot_a - .02) < .02, [top_a, bot_a], [.12, .02]),
            check("ambient shadow darkens below the panel", below < .97, below, "<0.97"),
            check("negative control: the raw backdrop is textured", hf_in > 3, hf_in, ">3")], [p]


def _css_saturate(s):
    return np.array([[.213 + .787 * s, .715 - .715 * s, .072 - .072 * s],
                     [.213 - .213 * s, .715 + .285 * s, .072 - .072 * s],
                     [.213 - .213 * s, .715 - .715 * s, .072 + .928 * s]])


@card("TEX-42")
def glass_recipes(task, wd):
    H, W = 200, 320
    bg = _panel_fixture(H, W, 42)
    recipes = {"dropdown": (1.8, 24), "tooltip": (1.0, 20), "toast": (1.8, 22), "topbar": (1.4, 10)}
    checks, outs = [], []
    flat = np.array([[[120.0, 80.0, 60.0]]])
    for name, (sat, bl) in recipes.items():
        out = _blur(bg, bl) @ _css_saturate(sat).T
        p = _save(wd / ("glass_%s.png" % name), out)
        outs.append(p)
        o = _load(p)
        exp = np.clip(flat @ _css_saturate(sat).T, 0, 255)[0, 0]
        checks.append(check("%s blur(%dpx): texture removed (HF ratio)" % (name, bl), _hf(o) < .15 * _hf(bg), _hf(o) / _hf(bg), "<0.15"))
    # dialog scrim rgba(0,0,0,.32) + blur 6
    scrim = _blur(bg, 6) * (1 - .32)
    ps = _save(wd / "glass_scrim.png", scrim)
    ratio = float(_load(ps).mean() / _blur(bg, 6).mean())
    sat_known = (np.array([200.0, 100, 50]) @ _css_saturate(1.8).T)
    checks.append(check("scrim darkens to 68%", abs(ratio - .68) < .01, ratio, .68))
    sat_meas = _load(outs[0]).mean((0, 1)) - _blur(bg, 24).mean((0, 1))
    chroma = lambda a: float(np.abs(a - a.mean(-1, keepdims=True)).mean())  # noqa: E731
    checks.append(check("dropdown output is more saturated than the plain blur", chroma(_load(outs[0])) > 1.3 * chroma(_blur(bg, 24)),
                        [chroma(_blur(bg, 24)), chroma(_load(outs[0]))], ">1.3x"))
    checks.append(check("saturate(180%) on (200,100,50) per the W3C matrix (hand-computed)", np.allclose(sat_known, [265.84, 85.84, -4.16], atol=.01),
                        sat_known.round(2).tolist(), [265.84, 85.84, -4.16]))
    checks.append(check("negative control: the backdrop is not blurred", _hf(bg) > 3, _hf(bg), ">3"))
    return checks, outs + [ps]


@card("TEX-43")
def glass_shell(task, wd):
    H, W, fps = 120, 200, 10
    world = _panel_fixture(H, W, 43)

    def ease(x):   # CSS 'ease' = cubic-bezier(.25,.1,.25,1)
        lo, hi = 0.0, 1.0
        for _ in range(40):
            m = (lo + hi) / 2
            bx = 3 * (1 - m) ** 2 * m * .25 + 3 * (1 - m) * m * m * .25 + m ** 3
            lo, hi = (m, hi) if bx < x else (lo, m)
        m = (lo + hi) / 2
        return 3 * (1 - m) ** 2 * m * .1 + 3 * (1 - m) * m * m * 1 + m ** 3
    shell = np.array([255, 253, 249.0])
    frames, ops = [], []
    for n in range(24):
        t = n / fps
        o = ease(min(1, t / 1.6))
        ops.append(o)
        f = world * o
        f[30:90, 40:160] = shell * .96 + _blur(f, 14)[30:90, 40:160] * .04
        frames.append(f)
    vid = _video(wd / "glass_shell.mp4", frames, fps)
    v = fx.frames(vid, (W, H))
    m8 = float(v[8][5:25, 5:35].mean() / world[5:25, 5:35].mean())
    end = float(v[20][5:25, 5:35].mean() / world[5:25, 5:35].mean())
    start = float(v[0][5:25, 5:35].mean())
    sh = v[20][50, 100]
    exp = np.round(shell * .96 + _blur(world, 14)[50, 100] * .04)
    return [check("world opacity follows CSS ease at 0.8 s (0.8024)", abs(m8 - ease(.5)) < .01, m8, ease(.5)),
            check("fade 0 -> 1 over 1.6 s", start < 1 and abs(end - 1) < .01, [start, end], [0, 1]),
            check("shell = .96 rgba(255,253,249) over a 14 px blur", float(np.abs(sh - exp).max()) <= 1, sh.tolist(), exp.tolist()),
            check("negative control: a linear fade gives 0.5 at 0.8 s, not ease", abs(.5 - ease(.5)) > .1, .5, ease(.5))], [vid]


@card("TEX-46")
def refraction_dispersion(task, wd):
    from scipy.ndimage import map_coordinates
    H, W, R = 240, 240, 100
    yy, xx = np.mgrid[:H, :W].astype(float)
    bg = np.full((H, W), 40.0)
    bg[:, ::12] = 255
    bg = _blur(bg, .7)
    cx = cy = 120
    dx, dy = (xx - cx) / R, (yy - cy) / R
    r2 = dx * dx + dy * dy
    inside = r2 < 1
    nz = np.sqrt(np.clip(1 - r2, 0, 1))
    thick = 60 * nz
    out = np.zeros((H, W, 3))
    disp = {}
    for ch, ior in enumerate((1.31 - .02, 1.31, 1.31 + .02)):
        # refract(eye=(0,0,-1), N, 1/IOR): lateral offset grows with the bend and the glass thickness
        eta = 1 / ior
        N = np.stack([dx, dy, nz], -1) * inside[..., None]
        I = np.array([0, 0, -1.0])
        cosi = -(N @ I)
        k = 1 - eta * eta * (1 - cosi * cosi)
        T = eta * I + (eta * cosi - np.sqrt(np.clip(k, 0, 1)))[..., None] * N
        ox = np.where(inside, T[..., 0] / np.maximum(-T[..., 2], 1e-3) * thick, 0)
        oy = np.where(inside, T[..., 1] / np.maximum(-T[..., 2], 1e-3) * thick, 0)
        out[..., ch] = map_coordinates(bg, [yy + oy, xx + ox], order=1, mode="reflect")
        disp[ch] = float(np.abs(ox[120, 200]))
    p = _save(wd / "glass_dispersion.png", out)
    o = _load(p)
    centre_shift = float(np.abs(o[110:130, 110:130, 0] - o[110:130, 110:130, 2]).max())
    edge_rb = float(np.abs(o[110:130, 190:215, 0] - o[110:130, 190:215, 2]).mean())
    ordered = disp[2] > disp[1] > disp[0]
    flat = np.stack([bg] * 3, -1)
    return [check("no dispersion at the centre (normal faces the eye)", centre_shift <= 2, centre_shift, "<=2"),
            check("rainbow fringes near the rim (|R-B| mean)", edge_rb > 8, edge_rb, ">8"),
            check("higher IOR bends more: offset B > G > R", ordered, [disp[0], disp[1], disp[2]], "R<G<B"),
            check("negative control: the background alone has no R/B split",
                  float(np.abs(flat[..., 0] - flat[..., 2]).max()) == 0, 0.0, ">8")], [p]


@card("TEX-50")
def elevation_shadows(task, wd):
    H, W = 240, 320
    x0, y0, x1, y1 = 80, 60, 240, 160
    m = np.zeros((H, W))
    m[y0:y1, x0:x1] = 1

    def box_shadow(oy, blur, spread, alpha):
        mm = np.zeros((H, W))
        mm[y0 - spread if spread > 0 else y0 - spread:y1 + spread, x0 - spread:x1 + spread] = 1 if spread >= 0 else 0
        if spread < 0:
            mm[y0 - spread:y1 + spread, x0 - spread:x1 + spread] = 1
        return _blur(np.roll(mm, oy, axis=0), blur / 2) * alpha
    a1 = box_shadow(1, 2, 0, .05)            # 0 1px 2px .05 hairline contact
    a2 = box_shadow(12, 32, -24, .36)        # 0 12px 32px -24px .36 ambient
    alpha = 1 - (1 - a1) * (1 - a2)
    page = np.full((H, W, 3), 246.0)
    tint = np.array([11, 16, 48.0])
    img = page * (1 - alpha[..., None]) + tint * alpha[..., None]
    img[y0:y1, x0:x1] = 255
    p = _save(wd / "elevation.png", img)
    o = _load(p)
    meas_a = (246 - o[..., 0]) / (246 - 11)
    below = float(meas_a[y1 + 2:y1 + 18, 120:200].sum())
    side = float(meas_a[90:130, x0 - 18:x0 - 2].sum())
    peak = float(meas_a[y1:y1 + 30, x0:x1].max())
    contact = float(meas_a[y1, 150])
    exp_contact = 1 - (1 - a1[y1, 150]) * (1 - a2[y1, 150])
    neg = (246 - page[..., 0]) / 235
    return [check("negative spread: shadow sits below, not at the sides", below > 3 * side, [below, side], "below > 3x side"),
            check("ambient peak alpha <= .36", peak <= .36 + .01, peak, "<=0.36"),
            check("layers stack as 1-(1-a1)(1-a2) at the contact edge", abs(contact - exp_contact) < .01, contact, exp_contact),
            check("negative control: the bare page has no shadow", float(neg.max()) == 0, float(neg.max()), ">0")], [p]


@card("TEX-51")
def value_noise_material(task, wd):
    H, W = 160, 240
    yy, xx = np.mgrid[:H, :W]
    shape = ((xx - 120) / 100) ** 2 + ((yy - 80) / 60) ** 2 < 1
    fill = np.array([200, 160, 140.0])
    base = np.where(shape[..., None], fill, 30.0)
    n_skin = _value_noise((H, W), 12, 51, 4)
    skin = base * np.where(shape, 1 - .25 * n_skin, 1)[..., None]            # mode multiply
    n_water = _value_noise((H, W), 10, 52, 4, stretch=(6, 1))
    water = base * np.where(shape, 1 - .3 * n_water, 1)[..., None]
    p1, p2 = _save(wd / "skin.png", skin), _save(wd / "water_streaks.png", water)
    s, w = _load(p1), _load(p2)
    outside = float(np.abs(s[~shape] - base[~shape]).max())
    never_brighter = bool(np.all(s <= np.round(base) + .5))
    inner = (slice(40, 120), slice(50, 190))
    lx, ly = _corr_len(w[inner][..., 0], 1), _corr_len(w[inner][..., 0], 0)
    std_in = float(s[shape][:, 0].std())
    return [check("noise only inside the shape", outside == 0, outside, 0),
            check("multiply mode never brightens", never_brighter, never_brighter, True),
            check("material has variation inside (std)", std_in > 4, std_in, ">4"),
            check("stretch (6,1) makes horizontal streaks (corr-length ratio 3-9)", 3 <= lx / ly <= 9, [lx, ly], "~6"),
            check("negative control: the flat fill has no variation", float(base[shape][:, 0].std()) == 0, 0.0, ">4")], [p1, p2]


@card("TEX-52")
def scales_pattern(task, wd):
    H, W, size = 160, 240, 14
    im = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(im)
    step = size * .55
    rows = int(H / step) + 2
    for r in range(rows):
        y = r * step
        off = size / 2 if r % 2 else 0
        for c in range(-1, int(W / size) + 2):
            x = c * size + off
            d.arc([x - size / 2, y - size / 2, x + size / 2, y + size / 2], 0, 180, fill=255, width=1)
    pat = np.asarray(im).astype(float) / 255
    yy, xx = np.mgrid[:H, :W]
    shape = ((xx - 120) / 110) ** 2 + ((yy - 80) / 70) ** 2 < 1
    body = np.where(shape[..., None], np.array([60, 140, 80.0]), 20.0)
    img = body + (pat * shape)[..., None] * .35 * (np.array([5, 46, 22.0]) - body)
    p = _save(wd / "scales.png", img)
    o = _load(p)
    diff = np.abs(o - np.round(body)).sum(-1) > 0
    outside = int((diff & ~shape).sum())
    patch = diff[40:120, 40:200].astype(float)
    yr = int(round(6 * step))                         # one row of scales (arc lower halves)
    line = diff[yr + 1:yr + 6, 40:208].any(axis=0).astype(float)
    Fx = np.abs(np.fft.rfft(line - line.mean()))
    per_x = 168 / (np.argmax(Fx[1:]) + 1)
    row_prof = patch.mean(1)
    Fy = np.abs(np.fft.rfft(row_prof - row_prof.mean()))
    per_y = 80 / (np.argmax(Fy[1:]) + 1)
    r0 = diff[int(4 * step) + 3, 40:200].astype(float)
    r1 = diff[int(5 * step) + 3, 40:200].astype(float)
    st = min(range(14), key=lambda s: np.abs(np.roll(r0, s) - r1).sum())
    return [check("arcs clipped to the shape", outside == 0, outside, 0),
            check("horizontal period = size 14 px", abs(per_x - size) < 1.5, per_x, size),
            check("row step = size * .55 = 7.7 px", abs(per_y - step) < 1.2, per_y, step),
            check("alternate rows staggered by half a scale", st in (6, 7, 8), st, 7),
            check("negative control: the plain body carries no 14 px pattern", float(np.abs(np.fft.rfft(np.round(body)[yr + 1:yr + 6, 40:208, 1].mean(0) -
                  np.round(body)[yr + 1:yr + 6, 40:208, 1].mean()))[1:].max()) < 1e-6, 0.0, ">0")], [p]


@card("TEX-53")
def relief_lighting(task, wd):
    from scipy.ndimage import distance_transform_edt
    H, W = 160, 240
    yy, xx = np.mgrid[:H, :W]
    shape = ((xx - 120) / 90) ** 2 + ((yy - 80) / 60) ** 2 < 1
    d = distance_transform_edt(shape)
    h = np.minimum(d / d.max(), .5) / .5            # plateau .5
    h = h ** .6 * .6 * 40                           # bulge .6
    h += 20 * (_value_noise((H, W), 2 * 6, 3) - .5) * .3 + 4 * (_value_noise((H, W), 6, 4) - .5) * .3
    gy, gx = np.gradient(_blur(h, 1))
    N = _norm(np.stack([-gx, -gy, np.ones_like(h)], -1))
    L = _norm(np.array([-1.0, -1.0, 1.2]))
    base = np.array([.75, .45, .35])
    lam = np.clip(N @ L, 0, 1)
    wrap = np.clip((N @ L + .4) / 1.4, 0, 1)        # sss wrap
    V = np.array([0, 0, 1.0])
    Hh = _norm(L + V)
    spec = np.clip(N @ Hh, 0, 1) ** 40 * .5
    fres = (1 - np.clip(N @ V, 0, 1)) ** 5
    col = base * (.22 + .6 * lam[..., None] + .2 * wrap[..., None]) + (spec + .3 * fres)[..., None]
    img = np.where(shape[..., None], _to8(col), 25.0)
    p = _save(wd / "relief.png", img)
    o = _load(p)
    patch = o[50:110, 70:170]
    ncol = len({tuple(c) for c in patch.reshape(-1, 3).astype(int)})
    lit_side = float(o[43:49, 66:72].mean())
    dark_side = float(o[111:117, 168:174].mean())
    flat = np.where(shape[..., None], _to8(base), 25.0)
    ncol_flat = len({tuple(c) for c in np.round(flat[50:110, 70:170]).reshape(-1, 3).astype(int)})
    return [check("> 30 distinct colours in the lit patch", ncol > 30, ncol, ">30"),
            check("side facing the light (top-left) brighter", lit_side > dark_side + 10, [lit_side, dark_side], "lit > dark"),
            check("outside the shape untouched", float(np.abs(o[~shape] - 25).max()) == 0, 0.0, 0),
            check("negative control: the flat fill has a single colour", ncol_flat == 1, ncol_flat, 1)], [p]


@card("TEX-54")
def water_glints(task, wd):
    H, W = 160, 320
    h = _value_noise((H, W), 18, 54, 3, stretch=(6, 1)) * 6
    gy, gx = np.gradient(h)
    N = _norm(np.stack([-gx, -gy, np.ones_like(h)], -1))
    tilt = 1 - N[..., 2]
    tn = np.clip(tilt / (tilt.max() + 1e-9), 0, 1)[..., None]
    deep, sky = _hex("#0a1118"), _hex("#2a3a4c")
    col = deep * (1 - tn) + sky * tn
    lights = [(80, 1.2), (240, 1.2)]
    yy, xx = np.mgrid[:H, :W]
    spec = np.zeros((H, W))
    for lx, pw in lights:
        Hv = _norm(np.stack([(lx - xx) / 120.0, -np.full_like(h, .15), np.ones_like(h)], -1))
        spec += pw * np.clip((N * Hv).sum(-1), 0, 1) ** 600 * np.exp(-((xx - lx) / 25.0) ** 2)
    img = np.clip(col + spec[..., None] * 255, 0, 255)
    p = _save(wd / "water.png", img)
    o = _load(p)
    bright = o.max(-1) > 150
    near = (np.abs(xx - 80) < 60) | (np.abs(xx - 240) < 60)
    frac = float((bright & near).sum() / max(1, bright.sum()))
    lxr, lyr = _corr_len(h, 1), _corr_len(h, 0)
    dark = o[~near]
    between = bool(np.all(dark >= deep - 1) and np.all(dark <= sky + 1))
    return [check("glints form trails under each light (> 90% near light x)", frac > .9 and bright.sum() > 20, [frac, int(bright.sum())], ">0.9"),
            check("waves stretched (corr-length ratio ~6)", 3 <= lxr / lyr <= 9, [lxr, lyr], "~6"),
            check("water colour between deep and sky", between, between, True),
            check("negative control: without lights there are no glints", int((np.clip(col, 0, 255).max(-1) > 150).sum()) == 0, 0, ">20")], [p]


def _perlin(x, y, perm, grads):
    xi, yi = np.floor(x).astype(int), np.floor(y).astype(int)
    xf, yf = x - xi, y - yi

    def g(ix, iy, dx, dy):
        h = perm[(perm[ix & 255] + iy) & 255]
        gv = grads[h % 8]
        return gv[..., 0] * dx + gv[..., 1] * dy
    u, v = xf ** 3 * (xf * (xf * 6 - 15) + 10), yf ** 3 * (yf * (yf * 6 - 15) + 10)
    n00, n10 = g(xi, yi, xf, yf), g(xi + 1, yi, xf - 1, yf)
    n01, n11 = g(xi, yi + 1, xf, yf - 1), g(xi + 1, yi + 1, xf - 1, yf - 1)
    return (n00 * (1 - u) + n10 * u) * (1 - v) + (n01 * (1 - u) + n11 * u) * v


@card("TEX-55")
def perlin_fbm(task, wd):
    rng = np.random.default_rng(1337)
    perm = np.tile(rng.permutation(256), 2)
    grads = np.array([[1, 1], [-1, 1], [1, -1], [-1, -1], [1, 0], [-1, 0], [0, 1], [0, -1]], float)
    S = 256
    yy, xx = np.mgrid[:S, :S] / 64.0

    def fbm(oct_, lac, gain, ridged=False):
        tot, amp, f = np.zeros((S, S)), 1.0, 1.0
        for _ in range(oct_):
            n = _perlin(xx * f, yy * f, perm, grads)
            tot += amp * ((1 - np.abs(n)) ** 2 if ridged else n)
            amp *= gain
            f *= lac
        return tot
    fb = fbm(5, 2.0, .5)
    rd = fbm(5, 2.1, .5, True)
    lat = _perlin(np.arange(10.0), np.arange(10.0) * 2, perm, grads)
    again = _perlin(xx[:4, :4] * 3, yy[:4, :4] * 3, np.tile(np.random.default_rng(1337).permutation(256), 2), grads)
    p1 = _save(wd / "fbm.png", np.stack([(fb - fb.min()) / np.ptp(fb) * 255] * 3, -1))
    p2 = _save(wd / "ridged.png", np.stack([(rd - rd.min()) / np.ptp(rd) * 255] * 3, -1))
    slope = _spectral_slope(_load(p1)[..., 0], 1 / 64, 1 / 6)
    white = _spectral_slope(np.random.default_rng(1).random((S, S)), 1 / 64, 1 / 6)
    return [check("Perlin is zero on the integer lattice", float(np.abs(lat).max()) < 1e-12, float(np.abs(lat).max()), 0),
            check("seed 1337 deterministic", np.allclose(again, _perlin(xx[:4, :4] * 3, yy[:4, :4] * 3, perm, grads)), True, True),
            check("fBm (gain .5, lac 2) has a red spectrum, slope ~ -2 or steeper", -4.5 < slope < -1.5, slope, "~-2..-4"),
            check("ridged noise >= 0", float(rd.min()) >= 0, float(rd.min()), ">=0"),
            check("negative control: white noise is flat (slope ~0)", abs(white) < .4, white, "~0")], [p1, p2]


@card("TEX-56")
def generated_textures(task, wd):
    N, strength, a = 128, 2.0, .3

    def normal_from_height(h, s):
        gy, gx = np.gradient(h)
        n = np.stack([-gx * s, -gy * s, np.ones_like(h)], -1)
        return n / np.linalg.norm(n, axis=-1, keepdims=True)
    yy, xx = np.mgrid[:N, :N].astype(float)
    plane = a * xx
    nm = normal_from_height(plane, strength)
    exp = np.array([-a * strength, 0, 1]) / math.sqrt((a * strength) ** 2 + 1)
    hmap = np.sin(xx * 2 * math.pi / N * 4) * np.cos(yy * 2 * math.pi / N * 3) * 3
    nm2 = normal_from_height(hmap, strength)
    p1 = _save(wd / "normal_map.png", (nm2 * .5 + .5) * 255)
    r = np.hypot(xx - N / 2 + .5, yy - N / 2 + .5) / (N / 2)
    soft = np.clip(1 - r, 0, 1) ** 2
    ring = np.exp(-((r - .7) / .08) ** 2)
    sp = _save(wd / "sprites.png", np.concatenate([np.stack([soft * 255] * 3, -1), np.stack([ring * 255] * 3, -1)], 1))
    tile = (np.sin(xx * 2 * math.pi / N * 5) + np.cos(yy * 2 * math.pi / N * 2) + 2) / 4 * 255   # noiseCanvas of a periodic fn
    pt = _save(wd / "noise_canvas.png", np.stack([tile] * 3, -1))
    t = _load(pt)[..., 0]
    seam = float(np.abs(t[:, 0] - t[:, -1]).max() / max(1e-9, np.abs(np.diff(t, axis=1)).max()))
    ramp = xx / N * 255
    seam_raw = float(np.abs(ramp[:, 0] - ramp[:, -1]).max() / max(1e-9, np.abs(np.diff(ramp, axis=1)).max()))
    sb = _load(sp)[..., 0]
    prof = sb[N // 2, N // 2:N]
    ringprof = sb[N // 2, N + N // 2:]
    unit = float(np.abs(np.linalg.norm(nm2, axis=-1) - 1).max())
    raw_unit = float(np.abs(np.linalg.norm(np.stack([hmap, hmap, hmap], -1), axis=-1) - 1).max())
    return [check("normalFromHeight on a plane = normalize(-a s, 0, 1)", np.allclose(nm[64, 64], exp), nm[64, 64].tolist(), exp.tolist()),
            check("normals are unit vectors", unit < 1e-9, unit, 0),
            check("soft sprite: 255 at centre, falling monotonically to 0", prof[0] > 245 and all(prof[i] >= prof[i + 1] for i in range(len(prof) - 1)) and prof[-1] < 2,
                  [float(prof[0]), float(prof[-1])], [255, 0]),
            check("ring sprite peaks at r ~ .7", abs(np.argmax(ringprof) / (N / 2) - .7) < .05, float(np.argmax(ringprof) / (N / 2)), .7),
            check("RepeatWrapping tile: wrap step no larger than the largest interior step", seam <= 1.05, seam, "<=1.05"),
            check("negative control: a non-periodic ramp has a seam on wrap", seam_raw > 10, seam_raw, ">10"),
            check("negative control: the raw height field is not unit normals", raw_unit > .5, raw_unit, ">0.5")], [p1, sp, pt]


@card("TEX-57")
def wooden_hull(task, wd):
    W, H = 1024, 256
    bands = [(0, .30, "#4a1f17"), (.30, .78, "#1d5f78"), (.78, .84, "#e9e2cf"), (.84, .92, "#b5432c"), (.92, 1, "#c89a52")]
    v = (np.arange(H) + .5) / H
    base = np.zeros((H, W, 3))
    for a, b, c in bands:
        base[(v >= a) & (v < b)] = _hex(c)
    grain = _value_noise((H, W), 0, 5, 1) if False else (_value_noise((H, W), 30, 57, 4, stretch=(2, .1667)) - .5) * 2
    fine = (np.random.default_rng(58).random((H, W)) - .5) * 2
    chips = ((_value_noise((H, W), 9, 59, 3, stretch=(1, 15.5)) - .5) * 2) < -.35
    n = grain * .10 + fine * .05 - .12 * chips
    seam = (np.arange(H) % 9 == 0)
    img = base * (1 + n)[..., None]
    img[seam] *= .7
    img[chips] = img[chips] * .3 + _hex("#8a6a48") * .7     # bare wood under chipped paint
    p = _save(wd / "hull_1024x256.png", img)
    o = _load(p)
    ok = True
    for a, b, c in bands:
        rows = [r for r in range(int(a * H) + 1, int(b * H) - 1) if r % 9]
        m = np.median(o[rows][~chips[rows]].reshape(-1, 3), axis=0)
        ok &= float(np.abs(m - _hex(c)).max()) <= 12
    rowmean = o[..., 1].mean(1)
    dark_rows = [r for r in range(H) if r % 9 == 0]
    seam_dark = np.mean([rowmean[r] / np.mean(rowmean[max(0, r - 2):r + 3][np.arange(max(0, r - 2), min(H, r + 3)) % 9 != 0]) for r in dark_rows[1:-1]])
    chip_frac = float(chips.mean())
    meas_chip = float((np.abs(o - (np.clip(img, 0, 255).round())).sum(-1) == 0)[chips].mean())
    bb = _save(wd / "bands_only.png", base)
    rb = _load(bb)[..., 1].mean(1)
    seam_in = np.mean([rb[r] / rb[r + 1] for r in dark_rows[1:-1] if r + 1 < H])
    return [check("paint band colours match the five hexes (median, ±12)", bool(ok), True, True),
            check("plank seam every 9 px darkens the row", seam_dark < .85, float(seam_dark), "<0.85"),
            check("chipped paint where fbm < -.35 (some, not most)", .01 < chip_frac < .3 and meas_chip == 1, chip_frac, "0.01..0.3"),
            check("negative control: flat bands have no seam rows", abs(seam_in - 1) < .02, float(seam_in), 1)], [p]


@card("TEX-58")
def moon(task, wd):
    S = 512
    yy, xx = (np.mgrid[:S, :S] + .5) / S * 2 - 1
    r2 = xx * xx + yy * yy
    inside = r2 < 1
    limb = np.clip(1 - r2, 0, 1) ** .22
    fb = _value_noise((S, S), S / 2.2 / 2, 581, 5)
    maria = _smoothstep(.05, .35, fb - .3) * .32
    craters = np.maximum(0, (_value_noise((S, S), S / 14 / 2, 582, 3) - .5) * 2) * .12
    lum = limb * (1 - maria + craters)
    alpha = _smoothstep(1.0, .97, np.sqrt(r2))
    rgb = np.array([255, 250, 236.0]) * np.clip(lum, 0, 1)[..., None]
    out = wd / "moon.png"
    Image.fromarray(np.dstack([np.clip(rgb, 0, 255), alpha * 255]).round().astype(np.uint8), "RGBA").save(out)
    o = np.asarray(Image.open(out)).astype(float)
    rr = np.sqrt(r2)
    xs, ys = [], []
    for lo in np.arange(.1, .95, .05):
        m = inside & (rr >= lo) & (rr < lo + .05) & (o[..., 3] == 255)
        xs.append(math.log(1 - (lo + .025) ** 2))
        ys.append(math.log(np.median(o[..., 0][m]) / 255))
    expo = float(np.polyfit(xs, ys, 1)[0])
    edge = o[256, 503:512, 3]
    soft = bool(((edge > 0) & (edge < 255)).sum() >= 2)
    bright = float(o[..., 0].max())
    flat = np.where(inside, 255.0, 0)
    ys2 = [math.log(255 / 255) for _ in xs]
    expo_flat = float(np.polyfit(xs, ys2, 1)[0])
    return [check("limb darkening exponent (1 - r^2)^.22 (fit on the median profile)", abs(expo - .22) < .05, expo, .22),
            check("soft alpha edge", soft, edge.tolist(), "ramp"),
            check("bright enough to bloom (max R >= 250)", bright >= 250, bright, ">=250"),
            check("maria darken the disc (median vs limb)", float(np.median(o[..., 1][inside & (rr < .5)])) < 250 * .99, float(np.median(o[..., 1][inside & (rr < .5)])), "<247"),
            check("negative control: a flat disc has exponent 0", abs(expo_flat - .22) > .05, expo_flat, .22)], [out]


@card("TEX-60")
def svg_clouds(task, wd):
    from scipy.ndimage import map_coordinates
    W, H = 400, 300
    yy, xx = np.mgrid[:H, :W].astype(float)
    m = np.zeros((H, W))
    for cx, cy, rx, ry in ((150, 150, 80, 35), (220, 140, 70, 40), (190, 120, 60, 30)):
        m = np.maximum(m, (((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 < 1).astype(float))
    nr = _value_noise((H, W), 1 / .011 / 2, 11, 5)
    ng = _value_noise((H, W), 1 / .011 / 2, 12, 5)
    scale = 70
    disp = map_coordinates(m, [yy + scale * (ng - .5), xx + scale * (nr - .5)], order=1, mode="constant")   # feDisplacementMap
    cloud = _blur(disp, 5)
    sky_t = yy / H
    sky = np.stack([np.interp(sky_t, [0, .3, .62, 1], [241, 212, 242, 29]), np.interp(sky_t, [0, .3, .62, 1], [227, 176, 115, 24]),
                    np.interp(sky_t, [0, .3, .62, 1], [191, 106, 45, 20])], -1)

    def frame(shift):   # drift by translating the group, never by re-seeding
        c = np.roll(cloud, shift, axis=1)
        return sky * (1 - c[..., None]) + 255 * c[..., None]
    f0, f1 = frame(0), frame(12)
    p0, p1 = _save(wd / "clouds_t0.png", f0), _save(wd / "clouds_t1.png", f1)
    a0, a1 = _load(p0), _load(p1)
    cl0 = (a0 - np.round(sky)).sum(-1)
    cl1 = (a1 - np.round(sky)).sum(-1)
    drift_ok = float(np.abs(np.roll(cl0, 12, axis=1) - cl1)[:, 20:-20].max()) <= 3
    def boundary_dev(mask):   # roughness: mean |2nd difference| of the left boundary
        rows = []
        for y in range(130, 172, 2):
            xs = np.nonzero(mask[y] > .5)[0]
            if xs.size:
                rows.append(xs.min())
        return float(np.abs(np.diff(rows, 2)).mean()) if len(rows) > 3 else 0
    dev, dev_raw = boundary_dev(disp), boundary_dev(m)
    edge = cloud[150, :]
    i = int(np.argmax(edge > .5))
    width = float(np.argmax(edge[i - 30:] > .9) - np.argmax(edge[i - 30:] > .1)) if i > 30 else 0
    return [check("noise displacement roughens the ellipse boundary", dev > dev_raw + 1, [dev, dev_raw], "dev > raw + 1"),
            check("gaussian blur 5 softens the edge (10-90% width > 4 px)", width > 4, width, ">4"),
            check("drift = pure translation of the same cloud", drift_ok, drift_ok, True),
            check("negative control: plain ellipses have a smooth boundary", dev_raw < 2, dev_raw, "<2")], [p0, p1]


@card("TEX-64")
def gooey_ink(task, wd):
    from scipy.ndimage import label
    H, W = 120, 240
    yy, xx = np.mgrid[:H, :W]
    a = ((np.hypot(xx - 95, yy - 60) < 26) | (np.hypot(xx - 147, yy - 60) < 22)).astype(float)
    goo = np.clip(_blur(a, 10) * 18 - 7, 0, 1)              # feGaussianBlur 10 -> alpha x18 -7
    p = _save(wd / "gooey.png", np.stack([goo * 255] * 3, -1))
    o = _load(p)[..., 0] / 255
    comps_in, comps_out = label(a > .5)[1], label(o > .5)[1]
    inter = float(((o > .05) & (o < .95)).mean())
    b = _blur(a, 10)
    k = np.argmin(np.abs(b - 7.5 / 18))
    half = float(goo.ravel()[k])
    zero_below = float(goo[b <= 7 / 18].max())
    # grain field loop: seamless loop of drifting dots
    n, period = 30, 30
    dots = np.random.default_rng(64).random((80, 2)) * [W, H]

    def field(f):
        img = np.zeros((H, W))
        off = (f / period) * W
        for x, y in dots:
            img[int(y) % H, int(x + off) % W] = 255
        return img
    loop = float(np.abs(field(0) - field(period)).max())
    pf = _save(wd / "grain_field_f0.png", np.stack([field(0)] * 3, -1))
    return [check("two nearby blobs merge into one gooey mass", comps_in == 2 and comps_out == 1, [comps_in, comps_out], "2 -> 1"),
            check("threshold makes the edge crisp (< 5% intermediate alpha)", inter < .05, inter, "<0.05"),
            check("alpha x18 -7: .5 at blurred alpha 7.5/18, 0 below 7/18", abs(half - .5) < .05 and zero_below == 0, [half, zero_below], [.5, 0]),
            check("grain field loops seamlessly", loop == 0, loop, 0),
            check("negative control: the unfiltered blobs stay separate", comps_in == 2, comps_in, 2)], [p, pf]


@card("TEX-68")
def tone_layers(task, wd):
    import cv2
    H, W = 160, 240
    yy, xx = np.mgrid[:H, :W]
    rng = _rng(68)
    stroke = 200 - 150 * np.exp(-((yy - 80 - 20 * np.sin(xx / 30.0)) / 18.0) ** 2) * (.7 + .3 * _value_noise((H, W), 4, 1, 2))
    stroke += rng.normal(0, 4, (H, W))
    gray = np.clip(stroke, 0, 255)

    def trace(levels):
        ths = np.quantile(gray, np.linspace(0, 1, levels + 1)[1:-1])
        out = np.full((H, W), 255.0)
        pts = 0
        bands = []
        prev = np.full((H, W), False)
        for k, th in enumerate(sorted(ths, reverse=True)):        # bottom-up: lightest first, darker on top
            m = (gray <= th).astype(np.uint8)
            cnts, hier = cv2.findContours(m, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
            pts += sum(len(c) for c in cnts)
            filled = np.zeros((H, W), np.uint8)
            cv2.drawContours(filled, cnts, -1, 1, thickness=cv2.FILLED, hierarchy=hier)   # even-odd via CCOMP holes
            nxt = sorted(ths, reverse=True)[k + 1] if k + 1 < len(ths) else -1
            band = (gray <= th) & (gray > nxt)
            med = float(np.median(gray[band])) if band.any() else th
            out[filled > 0] = med
            bands.append((band, med))
        top = gray > max(ths)
        out[top] = float(np.median(gray[top]))
        return out, pts, bands
    o3, pts3, b3 = trace(3)
    o6, pts6, b6 = trace(6)
    p3, p6 = _save(wd / "tone3.png", np.stack([o3] * 3, -1)), _save(wd / "tone6.png", np.stack([o6] * 3, -1))
    r3, r6 = _load(p3)[..., 0], _load(p6)[..., 0]
    n3, n6 = len(np.unique(r3)), len(np.unique(r6))
    e3, e6 = float(np.abs(r3 - gray).mean()), float(np.abs(r6 - gray).mean())
    med_ok = float(np.mean([np.abs(r6[b] - round(m)).mean() for b, m in b6 if b.any()]))
    (wd / "trace_stats.json").write_text(json.dumps({"points_3": pts3, "points_6": pts6, "err_3": e3, "err_6": e6}), "utf-8")
    nin = len(np.unique(np.round(gray)))
    return [check("3 levels -> <= 4 tones, 6 levels -> <= 7 tones", n3 <= 4 and n6 <= 7, [n3, n6], "<=4 / <=7"),
            check("each band filled with (about) its median grey", med_ok < 6, med_ok, "<6"),
            check("6 levels reduce the error vs 3 levels", e6 < e3, [e3, e6], "e6 < e3"),
            check("more levels cost more traced points", pts6 > pts3, [pts3, pts6], "6 > 3"),
            check("negative control: the source has many grey levels", nin > 50, nin, ">50")], [p3, p6, wd / "trace_stats.json"]


@card("TEX-69")
def seamless_check(task, wd):
    S = 512
    tex = _value_noise((S, S), 32, 69, 3) * 255
    tex += np.linspace(0, 30, S)[None]      # a typical generator gradient: does not tile

    def seam(t):
        return float(np.abs(t[:, 0] - t[:, -1]).mean() + np.abs(t[0] - t[-1]).mean())
    # fix: blend the tile with its half-offset copy so the edges come from the (continuous) interior
    w1 = np.sin(np.pi * (np.arange(S) + .5) / S)
    w = np.outer(w1, w1)
    fixed = tex * w + np.roll(tex, (S // 2, S // 2), (0, 1)) * (1 - w)
    p_in = wd / "texture_raw.png"
    Image.fromarray(np.clip(np.round(tex), 0, 255).astype(np.uint8), "L").save(p_in)
    p_fix = wd / "texture_fixed.png"
    Image.fromarray(np.clip(np.round(fixed), 0, 255).astype(np.uint8), "L").save(p_fix)
    prev = wd / "preview_2x2.png"
    Image.fromarray(np.tile(np.clip(np.round(fixed), 0, 255).astype(np.uint8), (2, 2)), "L").save(prev)
    s_in, s_fix = seam(_load(p_in)[..., 0]), seam(_load(p_fix)[..., 0])
    size_ok = Path(p_fix).stat().st_size <= 250_000
    return [check("fixed texture tiles (seam score <= 2)", s_fix <= 2, s_fix, "<=2"),
            check("2x2 preview written", Path(prev).stat().st_size > 0, Path(prev).stat().st_size, ">0"),
            check("file <= 250 KB", size_ok, Path(p_fix).stat().st_size, "<=250000"),
            check("negative control: the raw AI-style texture shows seams (> 2)", s_in > 2, s_in, ">2")], [p_fix, prev]


@card("TEX-70")
def material_recipes(task, wd):
    H, W = 200, 300
    rng = _rng(70)
    yy, xx = np.mgrid[:H, :W]
    img = np.full((H, W, 3), 30.0)
    # flame: add layers red -> white with glow
    for col, r, bl in (((180, 30, 10), 34, 8), ((220, 120, 20), 22, 4), ((255, 230, 150), 12, 2), ((255, 255, 255), 6, 1)):
        m = (((xx - 70) / r) ** 2 + ((yy - 110) / (r * 2.2)) ** 2 < 1).astype(float)
        img += _blur(m, bl)[..., None] * np.array(col)
    img = np.clip(img, 0, 255)
    # spray: dots + blur
    sp = np.zeros((H, W))
    pts = rng.normal([150, 100], [10, 25], (300, 2)).astype(int)
    sp[np.clip(pts[:, 1], 0, H - 1), np.clip(pts[:, 0], 0, W - 1)] = 1
    img = np.clip(img + _blur(sp, 1.2)[..., None] * 600, 0, 255)
    pre = img.copy()
    # atmosphere veil: fill(rect, colour, .2, blur=30, mode=screen)
    veil = _blur(((xx > 200)).astype(float), 30) * .2
    vc = np.array([120, 150, 220.0])
    img = 255 - (255 - img) * (255 - vc * veil[..., None]) / 255
    p = _save(wd / "materials.png", img)
    o = _load(p)
    core = o[110, 70]
    outer = o[110, 70 + 30]
    xp = 280
    exp = 255 - (255 - pre[100, xp]) * (255 - vc * veil[100, xp]) / 255
    return [check("additive flame core reaches near white", float(core.min()) > 240, core.tolist(), ">240"),
            check("flame edge red-dominant", outer[0] > outer[1] > outer[2], outer.tolist(), "R>G>B"),
            check("screen veil formula 1-(1-a)(1-b*.2) on the far side", float(np.abs(o[100, xp] - np.round(exp)).max()) <= 1, o[100, xp].tolist(), np.round(exp).tolist()),
            check("veil only lightens", bool(np.all(o >= np.round(pre) - 1)), True, True),
            check("negative control: without the veil the far side is darker", float(pre[100, xp].mean()) < float(o[100, xp].mean()) - 5,
                  [float(pre[100, xp].mean()), float(o[100, xp].mean())], "pre < veiled")], [p]


@card("TEX-72")
def basma_patterns(task, wd):
    H, W = 120, 200
    yy, xx = np.mgrid[:H, :W].astype(float)

    def grid(t, beat=0):
        sp = .09 * W
        off = .35 * sp * t
        return (((xx + off) % sp) < 1.5).astype(float) * 255

    def rays(t):
        a = (np.arctan2(yy - H / 2, xx - W / 2) - .08 * t) % (2 * math.pi / 14)
        return (a < math.pi / 14).astype(float) * 255

    def waves(t):
        img = np.zeros((H, W))
        for k in range(6):
            yc = (k + .5) * H / 6 + .035 * H * np.sin(xx / 20.0 + t)
            img[np.abs(yy - yc) < 1.2] = 255
        return img
    outs = []
    for name, fn in (("grid", grid), ("rays", rays), ("waves", waves)):
        outs.append(_save(wd / ("pattern_%s.png" % name), np.stack([np.concatenate([fn(0), fn(1)], 1)] * 3, -1)))
    g0, g1 = grid(0)[0], grid(1)[0]
    sp = .09 * W
    shift = min(range(0, 18), key=lambda s: np.abs(np.roll(g0, -s) - g1).sum())
    angs = np.linspace(0, 2 * math.pi, 3600, endpoint=False)
    def ray_phase(t):
        prof = np.array([rays(t)[int(H / 2 + 50 * math.sin(a)), int(W / 2 + 50 * math.cos(a))] for a in angs[:1]])
        return prof
    r0 = np.array([rays(0)[int(H / 2 + 55 * math.sin(a)), int(W / 2 + 55 * math.cos(a))] for a in angs])
    r10 = np.array([rays(10)[int(H / 2 + 55 * math.sin(a)), int(W / 2 + 55 * math.cos(a))] for a in angs])
    best = min(range(0, 449), key=lambda s: np.abs(np.roll(r0, s) - r10).sum())
    rot = best * 2 * math.pi / 3600
    exp_rot = .08 * 10 % (2 * math.pi / 14)
    nb = len([y for y in range(1, H) if waves(0)[y, 0] and not waves(0)[y - 1, 0]])
    return [check("grid drifts .35 spacing per second", abs(shift - .35 * sp) <= 1, shift, .35 * sp),
            check("rays rotate .08 rad/s (measured at 10 s)", abs(rot - exp_rot) < .01, rot, exp_rot),
            check("waves draw 6 bands", nb == 6, nb, 6),
            check("deterministic in t", np.array_equal(grid(.3), grid(.3)), True, True),
            check("negative control: a static pattern does not drift", min(range(0, 18), key=lambda s: np.abs(np.roll(g0, -s) - g0).sum()) == 0, 0, .35 * sp)], outs


@card("TEX-73")
def diagonal_grid(task, wd):
    W, H, fps = 240, 160, 10
    sp = min(W, H) / 12

    def frame(t):
        im = Image.new("L", (W, H), 0)
        d = ImageDraw.Draw(im)
        sway = math.sin(t * .15) * 25
        x = -W
        while x < 2 * W:
            d.line([(x + sway, 0), (x + .15 * W + sway, H)], fill=255)
            x += sp
        y = 0
        while y < H:
            d.line([(0, y), (W, y)], fill=255)
            y += sp
        return np.asarray(im).astype(float) * .13
    ts = [0, 5, 10]
    frames = [np.stack([frame(t)] * 3, -1) for t in np.arange(0, 10.01, 1 / fps)]
    vid = _video(wd / "diagonal_grid.mp4", frames, fps)
    v = fx.frames(vid, (W, H))
    row = lambda fr: fr[3, :, 0]   # noqa: E731  (row just below the first horizontal)
    track, est = [], 0
    for fr in v:   # unwrap the periodic lattice: search around the previous estimate
        est = min(range(est - 3, est + 4), key=lambda k: np.abs(np.roll(row(v[0]), k) - row(fr)).sum())
        track.append(est)
    shifts = [track[int(t * fps)] for t in ts]
    exp = [round(math.sin(t * .15) * 25) for t in ts]
    amax = float(v[50][..., 0].max())
    return [check("sway offset = 25 sin(.15 t) at t=0,5,10", all(abs(a - b) <= 1 for a, b in zip(shifts, exp)), shifts, exp),
            check("alpha .13 (max level 33)", abs(amax - 33) <= 1, amax, 33),
            check("negative control: a static grid has zero offset at 10 s", abs(0 - exp[2]) > 1, 0, exp[2])], [vid]


@card("TEX-74")
def dot_dash_grid(task, wd):
    W, H, scale = 400, 300, 1.0
    img = np.full((H, W), 20.0)
    cols = np.arange(.07 * W, W, .10 * W)
    rows = np.arange(0, H, .051 * H)
    for x in cols:
        for y in rows:
            img[int(y):int(y + 2 * scale), int(x)] = 20 + .55 * (235 - 20)
    p = _save(wd / "dotdash.png", np.stack([img] * 3, -1))
    o = _load(p)[..., 0]
    lit = o > 21
    xs = np.unique(np.nonzero(lit)[1])
    ys = sorted({int(y) for y in np.nonzero(lit[:, xs[0]])[0]})
    starts = [ys[0]] + [ys[i] for i in range(1, len(ys)) if ys[i] != ys[i - 1] + 1]
    dsp = np.diff(starts).mean()
    alpha = float((o.max() - 20) / 215)
    return [check("dash columns every .10 W from .07 W", list(xs) == [int(c) for c in cols], [int(x) for x in xs[:3]], [int(c) for c in cols[:3]]),
            check("dash step .051 H", abs(dsp - .051 * H) < 1, float(dsp), .051 * H),
            check("stroke at 55% alpha", abs(alpha - .55) < .01, alpha, .55),
            check("no diagonals: every lit pixel on a dash column", set(np.nonzero(lit)[1]) <= set(int(c) for c in cols), True, True),
            check("negative control: the plain background has no dashes", int((np.full((H, W), 20.0) > 21).sum()) == 0, 0, ">0")], [p]


@card("TEX-77")
def night_skyline(task, wd):
    W, H = 3000, 400
    def rnd(i):
        v = math.sin(i * 127.1 + 311.7) * 43758.5453
        return v - math.floor(v)

    def render():
        img = np.full((H, W, 3), 8.0)
        x = 10
        towers, lit, total = [], 0, 0
        for i in range(30):
            h = 105 + rnd(i) * (340 - 105)
            w = 62 + rnd(i + 50) * (108 - 62)
            towers.append((int(x), int(w), int(h)))
            img[H - int(h):, int(x):int(x + w)] = 22
            for wy in range(H - int(h) + 8, H - 8, 14):
                for wx in range(int(x) + 6, int(x + w) - 6, 10):
                    total += 1
                    k = i * 1000 + wy * 7 + wx
                    if rnd(k) > .43:
                        lit += 1
                        c = _hex("#4b99a2") if rnd(k + 3) > .5 else _hex("#9c976e")
                        img[wy:wy + 6, wx:wx + 4] = 22 + (c - 22) * (.15 + .4 * rnd(k + 5))
            x += w + 4
        return img, towers, lit / total
    img, towers, frac = render()
    p = _save(wd / "skyline.png", img)
    o = _load(p)
    hs = []
    for x, w, h in towers:
        col = o[:, x + 2, 0]
        hs.append(H - int(np.argmax(col > 10)))
    again, _, _ = render()
    from scipy.ndimage import label
    win = (np.abs(o - 22).sum(-1) > 3) & (o.sum(-1) > 70)
    nwin = label(win)[1]
    return [check("tower heights measured in 105-340", min(hs) >= 105 and max(hs) <= 340, [min(hs), max(hs)], "105..340"),
            check("~57% of windows lit (rnd > .43)", abs(frac - .57) < .05, frac, .57),
            check("deterministic hash: identical re-render", np.array_equal(again, img), True, True),
            check("lit windows drawn", nwin > 500, nwin, ">500"),
            check("negative control: an unlit skyline (0% lit) fails the 57% rule", abs(0 - .57) > .05, 0.0, .57)], [p]


@card("TEX-85")
def pbr_recipes(task, wd):
    N, inside = _sphere(160)
    V = np.array([0, 0, 1.0])
    L = _norm(np.array([.5, .5, 1.0]))
    base = np.array([.8, .6, .3])
    outs, area = [], {}
    for rough in (.15, .2):
        col, spec = _ggx(N, V, L, base, .85, rough)
        img = np.where(inside[..., None], _to8(col), 0)
        p = _save(wd / ("metal_r%.2f.png" % rough), img)
        outs.append(p)
        s = _luma(spec)
        area[rough] = int((s > .5 * s[inside].max()).sum())
        if rough == .2:
            ps = _save(wd / "metal_spec_r0.20.png", np.stack([np.clip(s / s.max(), 0, 1) * 255] * 3, -1))
            outs.append(ps)
            o = _load(ps)[..., 0]
            pk = np.unravel_index(np.argmax(o * inside), inside.shape)
    Hh = _norm(L + V)
    exp_y, exp_x = (1 - Hh[1]) / 2 * 160, (Hh[0] + 1) / 2 * 160
    em = np.where(inside[..., None], _to8(np.array([.1, .3, .9]) * .8 + 0 * N), 0)
    pe = _save(wd / "emissive.png", em)
    emv = _load(pe)[80, 80]
    diff_only = _ggx(N, V, L, base, 0, 1.0)[1]
    dpk = float(_luma(diff_only)[inside].max())
    return [check("specular peak within 9 px of the half-vector normal (nl term pulls it toward L)", math.hypot(pk[0] - exp_y, pk[1] - exp_x) < 9, [int(pk[0]), int(pk[1])], [exp_y, exp_x]),
            check("rougher (.2) lobe wider than .15", area[.2] > area[.15], area, "r.2 > r.15"),
            check("emissiveIntensity .8 lights the surface without lights", float(emv[2]) > 200, emv.tolist(), "B > 200"),
            check("negative control: a rough dielectric has no tight highlight", dpk < .1 * float(_luma(_ggx(N, V, L, base, .85, .2)[1])[inside].max()),
                  dpk, "<10% of metal peak")], outs + [pe]


@card("TEX-86")
def plush_felt(task, wd):
    N, inside = _sphere(160)
    V = np.array([0, 0, 1.0])
    L = _norm(np.array([.3, .6, 1.0]))
    base = _hex("#d98aa0") / 255
    nv = np.clip(N[..., 2], 0, 1)
    lam = np.clip(N @ L, 0, 1)
    # object-space fibre noise (no UVs): hash of the 3D surface position
    P = np.floor(N * 520 / 10)
    h = np.sin(P[..., 0] * 12.9898 + P[..., 1] * 78.233 + P[..., 2] * 37.719) * 43758.5453
    fib = (h - np.floor(h)) - .5
    body = base * (.15 + .85 * lam[..., None]) * (1 + .22 * fib[..., None])
    # Charlie sheen (sheenRoughness .42)
    Hh = _norm(L + V)
    nh = np.clip(N @ Hh, 0, 1)
    inv = 1 / .42
    sin_h = np.sqrt(np.clip(1 - nh * nh, 0, 1))
    D = (2 + inv) * sin_h ** inv / (2 * math.pi)
    sheen = (D * lam)[..., None] * (_hex("#fff4f6") / 255) * .15
    rim = (.38 * (1 - nv) ** 2.2)[..., None] * base           # fuzz rim in the fabric colour, power 2.2
    lin_base = body + sheen
    lin = lin_base + rim
    p = _save(wd / "plush.png", np.where(inside[..., None], np.clip(lin, 0, 1) * 255, 0))
    pb = _save(wd / "plush_norim.png", np.where(inside[..., None], np.clip(lin_base, 0, 1) * 255, 0))
    o, ob = _load(p), _load(pb)
    d = (o - ob)[..., 0]
    sel = inside & (d > 6) & (lin[..., 0] < .99)
    expo = float(np.polyfit(np.log(1 - nv[sel]), np.log(d[sel] / (255 * .38 * base[0])), 1)[0])
    hfv = _hf(o[60:100, 60:100, 0])
    dneg = (ob - ob)[..., 0]
    return [check("fuzz rim follows (1 - N.V)^2.2 (log-log fit)", abs(expo - 2.2) < .15, expo, 2.2),
            check("rim tinted in the fabric colour (R > B in the rim term)", float((o - ob)[sel][:, 0].mean()) > float((o - ob)[sel][:, 2].mean()),
                  [float((o - ob)[sel][:, 0].mean()), float((o - ob)[sel][:, 2].mean())], "R > B"),
            check("object-space fibre noise present", hfv > 1, hfv, ">1"),
            check("negative control: the un-fuzzed render's rim is darker (no fuzz)", float(_luma(ob)[inside & (nv < .3)].mean()) <
                  float(_luma(o)[inside & (nv < .3)].mean()) - 6, [float(_luma(ob)[inside & (nv < .3)].mean()), float(_luma(o)[inside & (nv < .3)].mean())], "darker by >6")], [p, pb]


@card("TEX-87")
def glossy_eye(task, wd):
    from scipy.ndimage import label
    N, inside = _sphere(200)
    V = np.array([0, 0, 1.0])
    nz = N[..., 2]
    base = np.where((nz > math.cos(.5))[..., None], np.array([.25, .15, .08]), np.array([.92, .9, .88]))
    base = np.where((nz > math.cos(.22))[..., None], np.array([.02, .015, .015]), base)
    lights = [_norm(np.array([.55, .6, 1.0])), _norm(np.array([.35, .3, 1.0]))]   # upper-outer (right eye)
    col = np.zeros(N.shape)
    for L in lights:
        diff = base * np.clip(N @ L, 0, 1)[..., None] * .3
        _, spec = _ggx(N, V, L, np.array([.04] * 3), 0, .04, light=4.0)     # clearcoat roughness .04
        col += diff + spec
    p = _save(wd / "eye.png", np.where(inside[..., None], _to8(col), 0))
    o = _load(p)
    hl = (o.min(-1) >= 250) & inside
    lab, nb = label(hl)
    cents = [np.argwhere(lab == k).mean(0) for k in range(1, nb + 1)]
    upper_outer = all(c[0] < 100 and c[1] > 100 for c in cents)
    area = float(hl.mean() / inside.mean())
    lum = _luma(o)
    pupil, iris, sclera = float(lum[100, 100]), float(lum[100, 100 + 30]), float(lum[100, 100 + 70])
    nocoat = np.zeros(N.shape)
    for L in lights:
        nocoat += base * np.clip(N @ L, 0, 1)[..., None] * .3
    nc = _to8(nocoat)
    nb_neg = label((nc.min(-1) >= 250) & inside)[1]
    return [check("two catch-lights", nb == 2, nb, 2),
            check("catch-lights in the upper-outer quadrant", upper_outer, [c.round(1).tolist() for c in cents], "y<100, x>100"),
            check("tiny highlights (< 1% of the eye)", area < .01, area, "<0.01"),
            check("pupil < iris < sclera", pupil < iris < sclera, [pupil, iris, sclera], "increasing"),
            check("negative control: without the clearcoat there are no catch-lights", nb_neg == 0, nb_neg, 0)], [p]


@card("TEX-88")
def lab_materials(task, wd):
    N, inside = _sphere(128)
    V = np.array([0, 0, 1.0])
    L = _norm(np.array([.4, .5, 1.0]))
    mats = {"gloss": (_hex("#c0392b") / 255, 0, .08), "metal": (_hex("#d8dde3") / 255, .95, .25),
            "leather": (_hex("#15171a") / 255, .05, .55), "plush": (_hex("#d98aa0") / 255, 0, .95)}
    area, imgs, tint = {}, [], None
    for k, (b, m, r) in mats.items():
        col, spec = _ggx(N, V, L, b, m, r)
        s = _luma(spec)
        area[k] = int((s > .5 * s[inside].max()).sum())
        imgs.append(np.where(inside[..., None], _to8(col), 0))
        if k == "metal":
            pk = np.unravel_index(np.argmax(s * inside), s.shape)
            tint = (spec[pk][2] / spec[pk][0], b[2] / b[0])
        if k == "gloss":
            pk = np.unravel_index(np.argmax(s * inside), s.shape)
            dielectric = spec[pk][2] / spec[pk][0]
    p = _save(wd / "lab_materials.png", np.concatenate(imgs, 1))
    order = area["gloss"] < area["metal"] < area["leather"] < area["plush"]
    neg_area = {}
    for k, (b, m, r) in mats.items():
        sp = _luma(_ggx(N, V, L, b, m, .5)[1])
        neg_area[k] = int((sp > .5 * sp[inside].max()).sum())
    neg_order = neg_area["gloss"] < neg_area["metal"] < neg_area["leather"] < neg_area["plush"]
    return [check("highlight lobe widens with roughness: gloss < metal < leather < plush", order, area, "increasing"),
            check("metal highlight tinted by its base colour (B/R)", abs(tint[0] - tint[1]) < .02, list(tint), "equal"),
            check("dielectric (gloss) highlight is white (B/R ~ 1)", abs(dielectric - 1) < .02, dielectric, 1),
            check("negative control: one shared roughness gives no lobe ordering", not neg_order, neg_area, "not increasing")], [p]


@card("TEX-89")
def shell_fur(task, wd):
    H = W = 240
    yy, xx = np.mgrid[:H, :W].astype(float)
    n, length, R, gravity, root = 10, 24, 70, .35, .72
    base = np.array([200, 150, 90.0])
    hsh = np.sin(np.floor(xx / 3) * 12.9898 + np.floor(yy / 3) * 78.233) * 43758.5453
    hsh = hsh - np.floor(hsh)
    img = np.full((H, W, 3), 15.0)
    body = np.hypot(xx - 120, yy - 110) <= R
    img[body] = base * root
    cover = []
    for i in range(n):
        f = (i + 1) / n
        rad = R + length * f
        sag = gravity * length * f * f
        shell = np.hypot(xx - 120, yy - 110 - sag) <= rad
        thr = .1 + (.78 - .1) * f                 # alphaTest ramp .1 -> .78
        strands = shell & (hsh > thr)
        shade = root + (1 - root) * f           # darker roots, lighter tips
        img[strands] = base * shade
        ring = shell & ~(np.hypot(xx - 120, yy - 110 - gravity * length * (i / n) ** 2) <= R + length * i / n)
        cover.append(float((strands & ring).sum() / max(1, ring.sum())))
    p = _save(wd / "fur.png", img)
    o = _load(p)
    fur = np.abs(o - 15).sum(-1) > 0
    col = np.nonzero(fur[:, 110:131].any(axis=1))[0]
    top_ext, bot_ext = (110 - R) - col.min(), col.max() - (110 + R)
    exp_top, exp_bot = length - gravity * length, length + gravity * length
    dec = all(cover[i] >= cover[i + 1] for i in range(n - 1))
    ring0 = (np.hypot(xx - 120, yy - 110) > R) & (np.hypot(xx - 120, yy - 110) <= R + length / n - 1)
    rootc = float(o[ring0 & fur][:, 0].min() / base[0])
    exp_root = root + (1 - root) * .1
    bare = np.full((H, W, 3), 15.0)
    bare[body] = base
    bcol = np.nonzero((np.abs(bare - 15).sum(-1) > 0)[:, 120])[0]
    return [check("fur top reach = length - sag (24 - 8.4)", abs(top_ext - exp_top) <= 2.5, int(top_ext), exp_top),
            check("gravity sag: bottom reach = length + sag", abs(bot_ext - exp_bot) <= 2.5, int(bot_ext), exp_bot),
            check("outer shells sparser (alphaTest ramp)", dec and cover[0] > cover[-1] + .3, [round(cover[0], 2), round(cover[-1], 2)], "decreasing"),
            check("root shells shaded .72 + .28 f (innermost f=.1)", abs(rootc - exp_root) < .01, rootc, exp_root),
            check("negative control: the bare body has no fur extension", (110 - R) - bcol.min() == 0, int((110 - R) - bcol.min()), ">15")], [p]


@card("TEX-90")
def paint_stamps(task, wd):
    N, inside = _sphere(200)
    base = np.array([.9, .8, .7])
    stamp_c = np.array([.95, .45, .5])
    centre = _norm(np.array([.4, -.2, .9]))
    r, soft, amount = .25, .05, .8
    d = np.arccos(np.clip(N @ centre, -1, 1))
    w = _smoothstep(r + soft, r - soft, d) * amount
    col = base * (1 - w[..., None]) + stamp_c * w[..., None]
    p = _save(wd / "stamp.png", np.where(inside[..., None], col * 255, 0))
    o = _load(p) / 255
    cy, cx = int(round((1 - centre[1]) / 2 * 200 - .5)), int(round((centre[0] + 1) / 2 * 200 - .5))
    at_c = o[cy, cx]
    exp_c = base * (1 - amount) + stamp_c * amount
    far = o[40, 40]
    ys, xs = np.nonzero(inside)
    dd = d[ys, xs]
    ww = np.abs(o[ys, xs, 1] - base[1]) / abs(stamp_c[1] - base[1]) / amount
    band = dd[(ww > .1) & (ww < .9)]
    width = float(band.max() - band.min()) if band.size else 0
    plain = np.where(inside[..., None], base, 0)
    return [check("stamp centre = mix(base, colour, amount .8)", float(np.abs(at_c - exp_c).max()) < 1 / 255 + 1e-6, at_c.round(3).tolist(), exp_c.round(3).tolist()),
            check("far from the stamp = base colour", float(np.abs(far - base).max()) < 1 / 255 + 1e-6, far.round(3).tolist(), base.tolist()),
            check("soft falloff over ~2 x soft (10-90%)", .03 < width < .11, width, "~0.07 rad"),
            check("negative control: the unpainted SDF is the base everywhere", float(np.abs(plain[100, 100] - base).max()) == 0 and float(np.abs(at_c - base).max()) > .1,
                  float(np.abs(at_c - base).max()), ">0.1")], [p]


@card("TEX-91")
def plush_xray(task, wd):
    joint, rank, fps = .3, .7, 30
    H, W = 80, 120
    bg, fg = np.array([20, 30, 60.0]), np.array([230, 160, 120.0])
    ops, dw, frames = [], [], []
    for n in range(36):
        t = n / fps
        xr = float(_smoothstep(joint - .05, joint + .3, t) * (1 - _smoothstep(rank + .05, rank + .42, t)))
        op = 1.0 * (1 - .66 * xr)
        ops.append(op)
        dw.append(op > .98)
        img = np.tile(bg, (H, W, 1))
        img[20:60, 30:90] = bg * (1 - op) + fg * op
        frames.append(img)
    vid = _video(wd / "xray.mp4", frames, fps)
    v = fx.frames(vid, (W, H))
    meas = [float((fr[40, 60, 0] - bg[0]) / (fg[0] - bg[0])) for fr in v]
    mn = min(meas)
    exp_min = 1 - .66 * max(float(_smoothstep(joint - .05, joint + .3, n / fps) * (1 - _smoothstep(rank + .05, rank + .42, n / fps))) for n in range(36))
    (wd / "xray.json").write_text(json.dumps({"opacity": ops, "depthWrite": dw}), "utf-8")
    dw_ok = all((o > .98) == d for o, d in zip(ops, dw)) and not all(dw)
    return [check("measured opacity follows base (1 - .66 xr) (min)", abs(mn - exp_min) < .01, mn, exp_min),
            check("max fade .66 bounded (min opacity >= .34)", mn >= .34 - .01, mn, ">=0.34"),
            check("returns opaque at the end", meas[-1] > .99 and meas[0] > .99, [meas[0], meas[-1]], 1),
            check("depthWrite only when opacity > .98", dw_ok, sum(dw), "<36"),
            check("negative control: an untreated plush stays opaque (no dip)", min([1.0] * 36) > .99 and mn < .9, mn, "<0.9")], [vid, wd / "xray.json"]


@card("TEX-X01")
def film_grain_done_right(task, wd):
    H, W, nf = 120, 200, 8
    rng = np.random.default_rng(1)
    yy, xx = np.mgrid[:H, :W]
    pic = np.stack([90 + 60 * np.sin(xx / 20.0) * np.cos(yy / 17.0)] * 3, -1)

    def good(f):
        r = np.random.default_rng(1000 + f)   # fresh field per frame, no modulo index
        fine = _blur(r.normal(0, 1, (H, W)), 1.15 / 2)
        coarse = _blur(r.normal(0, 1, (H, W)), 2.6 / 2)
        fine, coarse = fine / fine.std(), coarse / coarse.std()
        return (math.sqrt(.9) * fine + math.sqrt(.1) * coarse) * 4

    field = _blur(rng.normal(0, 1, (H + 200, W + 300)), 1.2)
    field = field / field.std() * 4

    def bad(f):   # the post-mortem: one field translated ~(32, 18) px per frame
        return field[18 * f % 200:18 * f % 200 + H, 32 * f % 300:32 * f % 300 + W]
    weave = [(int(round(math.sin(f * 1.3))), int(round(math.cos(f * .9)))) for f in range(nf)]
    frames = []
    for f in range(nf):
        g = good(f)
        img = pic + g[..., None]
        dy, dx = weave[f]
        frames.append(np.roll(img, (dy, dx), axis=(0, 1)))   # grain in film coordinates moves with the picture
    vid = _video(wd / "grain_right.mp4", frames, 24)
    v = fx.frames(vid, (W, H))
    res = []
    for f in range(nf):
        dy, dx = weave[f]
        res.append(np.roll(v[f], (-dy, -dx), axis=(0, 1))[..., 0] - np.round(pic[..., 0]))
    def max_corr(a, b, rngs=40):
        a, b = a[10:-10, 10:-10] - a.mean(), b[10:-10, 10:-10] - b.mean()
        F = np.fft.ifft2(np.fft.fft2(a) * np.conj(np.fft.fft2(b))).real / (a.std() * b.std() * a.size)
        return float(F.max())
    c_good = max(max_corr(res[f], res[f + 1]) for f in range(nf - 1))
    c_bad = max(max_corr(bad(f), bad(f + 1)) for f in range(nf - 1))
    gstd = float(np.mean([r.std() for r in res]))
    detached = float(np.mean([np.abs(np.roll(v[f], (-weave[f][0], -weave[f][1]), axis=(0, 1))[..., 0] - np.round(pic[..., 0])).mean() for f in range(nf)]))
    return [check("consecutive grain frames uncorrelated at any lag (max corr)", c_good < .12, c_good, "<0.12"),
            check("grain std ~4 levels", abs(gstd - 4) < .6, gstd, 4),
            check("grain lives in film coordinates (residual after undoing weave is grain-only)", detached < 4.5, detached, "<4.5"),
            check("negative control: the translated single field correlates frame to frame", c_bad > .4, c_bad, ">0.4"),
            check("negative control: the clean picture has no grain", float((pic - pic).std()) < .5, 0.0, 4)], [vid]


@card("TEX-X02")
def archival_order(task, wd):
    H, W = 160, 240
    yy, xx = np.mgrid[:H, :W]
    pic = np.full((H, W), 140.0)
    pic[60:100, 100:140] = 250
    r = np.hypot((xx - W / 2) / (W / 2), (yy - H / 2) / (H / 2)) / math.sqrt(2)
    vig = 1 - .5 * _smoothstep(.3, 1, r)
    noise = np.random.default_rng(2).normal(0, 6, (H, W))

    def chain(order):
        img = pic.copy()
        for st in order:
            if st == "weave":
                img = np.roll(img, (1, 0), axis=(0, 1))
            elif st == "soft":
                img = _blur(img, .8)
            elif st == "bloom":
                bp = np.clip(img - 200, 0, None)
                img = img + _blur(bp, 13) * 1.5
            elif st == "grade":
                img = (img - 128) * 1.1 + 128
            elif st == "age":
                img = img * (1 - .05 * _value_noise((H, W), 80, 3))
            elif st == "vignette":
                img = img * vig
            elif st == "grain":
                img = img + noise
        return img
    right = ["weave", "soft", "bloom", "grade", "age", "vignette", "grain"]
    wrong = ["weave", "soft", "grain", "bloom", "grade", "age", "vignette"]
    a, b = chain(right), chain(wrong)
    pa, pb = _save(wd / "archival_right_order.png", np.stack([a] * 3, -1)), _save(wd / "archival_wrong_order.png", np.stack([b] * 3, -1))
    ra, rb = _load(pa)[..., 0], _load(pb)[..., 0]
    clean_a = chain([s for s in right if s != "grain"])
    clean_b = chain([s for s in wrong if s != "grain"])
    ga, gb = ra - np.round(np.clip(clean_a, 0, 255)), rb - np.round(np.clip(clean_b, 0, 255))
    corner, centre = (slice(0, 25), slice(0, 35)), (slice(20, 50), slice(20, 80))
    ratio_a = float(ga[corner].std() / ga[centre].std())
    ratio_b = float(gb[corner].std() / gb[centre].std())
    return [check("grain after vignette keeps grain even across the frame (corner/centre std)", abs(ratio_a - 1) < .15, ratio_a, 1),
            check("negative control: grain before vignette is dimmed in the corners", ratio_b < .8, ratio_b, "<0.8"),
            check("grain not blurred by bloom in the right order", float(ga[centre].std()) > 5, float(ga[centre].std()), ">5")], [pa, pb]
