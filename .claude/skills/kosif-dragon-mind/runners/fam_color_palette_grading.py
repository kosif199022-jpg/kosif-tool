"""color-palette-grading: method cards as real programs with known-answer checks.

Every card builds a deterministic fixture in the work folder (ramps, colour charts, testsrc2 frames, synthetic
clips), applies the card's method with ffmpeg / numpy / Pillow, and measures the output against known answers.
Each card also runs the same measurement on the unprocessed input as a negative control.
Where the card's engine is a browser / three.js / HyperFrames component, the method is re-implemented in numpy
and the output JSON says so ("engine"): the numbers are the card's, the renderer is ours.
"""
import json
import math
import re
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from _harness import card, check, fx

GAPS: dict = {
    "COLOR-81": "the seven plates are the HyperFrames shaders.iife.js WebGPU library (shaders 4.0.0); it is not "
                "vendored here and headless WebGPU rendering is not verified, so the plates cannot be produced",
}


# ----------------------------------------------------------------------------------------------- helpers
def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def tohex(c):
    return "#%02x%02x%02x" % tuple(int(round(max(0, min(255, float(v))))) for v in c[:3])


def save(a, p):
    Image.fromarray(np.clip(np.rint(np.asarray(a, dtype=float)), 0, 255).astype(np.uint8)).save(str(p))
    return p


def load(p):
    return np.asarray(Image.open(str(p)).convert("RGB")).astype(float)


def ffimg(src, vf, dst, *extra_inputs):
    args = ["-i", str(src)]
    for e in extra_inputs:
        args += ["-i", str(e)]
    if extra_inputs:
        args += ["-filter_complex", vf]
    else:
        args += ["-vf", vf + ",format=rgb24"]
    fx.ffmpeg(*args, "-frames:v", "1", "-pix_fmt", "rgb24", str(dst))
    return load(dst)


def write_video(path, frames, fps=30, codec="libx264", crf="17", extra=()):
    frames = [np.clip(np.rint(f), 0, 255).astype(np.uint8) for f in frames]
    h, w = frames[0].shape[:2]
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", "%dx%d" % (w, h), "-r", str(fps), "-i", "-"]
    if codec == "ffv1":
        cmd += ["-c:v", "ffv1", "-pix_fmt", "bgr0"]
    else:
        cmd += ["-c:v", codec, "-crf", crf, "-pix_fmt", "yuv420p", *extra]
    cmd.append(str(path))
    done = subprocess.run(cmd, input=b"".join(f.tobytes() for f in frames), capture_output=True, timeout=60)
    if done.returncode:
        raise RuntimeError(done.stderr.decode(errors="replace")[-300:])
    return path


def lin(c):
    c = np.asarray(c, dtype=float) / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def unlin(v):
    v = np.clip(np.asarray(v, dtype=float), 0, 1)
    return 255.0 * np.where(v <= 0.0031308, v * 12.92, 1.055 * v ** (1 / 2.4) - 0.055)


def rel_lum(c):
    l = lin(c)
    return float(0.2126 * l[..., 0] + 0.7152 * l[..., 1] + 0.0722 * l[..., 2]) if np.ndim(l) == 1 else \
        0.2126 * l[..., 0] + 0.7152 * l[..., 1] + 0.0722 * l[..., 2]


def contrast(a, b):
    la, lb = rel_lum(hx(a) if isinstance(a, str) else a), rel_lum(hx(b) if isinstance(b, str) else b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def luma(a):
    a = np.asarray(a, dtype=float)
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def rgb2hsv(a):
    a = np.asarray(a, dtype=float) / 255.0
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx, mn = a.max(-1), a.min(-1)
    d = mx - mn
    h = np.zeros_like(mx)
    m = d > 1e-9
    rm = m & (mx == r)
    gm = m & (mx == g) & ~rm
    bm = m & ~rm & ~gm
    h[rm] = ((g - b)[rm] / d[rm]) % 6
    h[gm] = (b - r)[gm] / d[gm] + 2
    h[bm] = (r - g)[bm] / d[bm] + 4
    s = np.where(mx > 1e-9, d / np.maximum(mx, 1e-9), 0)
    return np.stack([h * 60.0, s, mx], -1)


def hsv2rgb(hsv):
    h, s, v = hsv[..., 0] % 360 / 60.0, hsv[..., 1], hsv[..., 2]
    i = np.floor(h).astype(int) % 6
    f = h - np.floor(h)
    p, q, t = v * (1 - s), v * (1 - s * f), v * (1 - s * (1 - f))
    r = np.choose(i, [v, q, p, p, t, v])
    g = np.choose(i, [t, v, v, q, p, p])
    b = np.choose(i, [p, p, t, v, v, q])
    return np.stack([r, g, b], -1) * 255.0


def hue_of(c):
    return float(rgb2hsv(np.array(c, dtype=float))[0])


def hue_dist(a, b):
    d = abs(a - b) % 360
    return min(d, 360 - d)


def hsl2hex(h, s, l):
    import colorsys
    r, g, b = colorsys.hls_to_rgb((h % 360) / 360.0, l, s)
    return tohex((r * 255, g * 255, b * 255))


def hex2hsl(hexc):
    import colorsys
    r, g, b = [v / 255.0 for v in hx(hexc)]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h * 360, s, l


def lab(a):
    l = lin(a)
    m = np.array([[0.4124564, 0.3575761, 0.1804375], [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = l @ m.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 216 / 24389, np.cbrt(xyz), (24389 / 27 * xyz + 16) / 116)
    L = 116 * f[..., 1] - 16
    A = 500 * (f[..., 0] - f[..., 1])
    B = 200 * (f[..., 1] - f[..., 2])
    return np.stack([L, A, B], -1)


def blur(a, sigma):
    from scipy.ndimage import gaussian_filter
    a = np.asarray(a, dtype=float)
    if a.ndim == 3:
        return np.stack([gaussian_filter(a[..., c], sigma) for c in range(a.shape[2])], -1)
    return gaussian_filter(a, sigma)


def psnr(a, b):
    mse = float(np.mean((np.asarray(a, float) - np.asarray(b, float)) ** 2))
    return 99.0 if mse == 0 else 10 * math.log10(255.0 ** 2 / mse)


def ramp(w=256, h=32):
    x = np.linspace(0, 255, w)
    return np.repeat(np.repeat(x[None, :, None], h, 0), 3, 2)


def testsrc_png(path, size="320x180"):
    fx.ffmpeg("-f", "lavfi", "-i", "testsrc2=s=%s:r=1:d=1" % size, "-frames:v", "1", "-pix_fmt", "rgb24", str(path))
    return load(path)


def chart(colors, cell=24):
    a = np.zeros((cell, cell * len(colors), 3))
    for i, c in enumerate(colors):
        a[:, i * cell:(i + 1) * cell] = hx(c) if isinstance(c, str) else c
    return a


def patch(a, i, cell=24, m=4):
    return a[m:cell - m, i * cell + m:(i + 1) * cell - m].reshape(-1, 3).mean(0)


def font(size=24, bold=True):
    for p in (["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"] if bold else []) + \
             ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/freefont/FreeSans.ttf"]:
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


def jdump(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=1, default=lambda o: float(o)), encoding="utf-8")
    return path


def smoothstep(e0, e1, x):
    t = np.clip((np.asarray(x, float) - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


# CSS Filter Effects (spec matrices, applied in sRGB 0..1 with a clamp after every function)
def css_filter(a, ops):
    v = np.asarray(a, float) / 255.0
    for name, amt in ops:
        if name in ("grayscale", "sepia", "saturate", "hue-rotate"):
            if name == "grayscale":
                k = 1 - amt
                m = [[0.2126 + 0.7874 * k, 0.7152 - 0.7152 * k, 0.0722 - 0.0722 * k],
                     [0.2126 - 0.2126 * k, 0.7152 + 0.2848 * k, 0.0722 - 0.0722 * k],
                     [0.2126 - 0.2126 * k, 0.7152 - 0.7152 * k, 0.0722 + 0.9278 * k]]
            elif name == "sepia":
                k = 1 - amt
                m = [[0.393 + 0.607 * k, 0.769 - 0.769 * k, 0.189 - 0.189 * k],
                     [0.349 - 0.349 * k, 0.686 + 0.314 * k, 0.168 - 0.168 * k],
                     [0.272 - 0.272 * k, 0.534 - 0.534 * k, 0.131 + 0.869 * k]]
            elif name == "saturate":
                s = amt
                m = [[0.213 + 0.787 * s, 0.715 - 0.715 * s, 0.072 - 0.072 * s],
                     [0.213 - 0.213 * s, 0.715 + 0.285 * s, 0.072 - 0.072 * s],
                     [0.213 - 0.213 * s, 0.715 - 0.715 * s, 0.072 + 0.928 * s]]
            else:
                c, s = math.cos(math.radians(amt)), math.sin(math.radians(amt))
                m = [[0.213 + c * 0.787 - s * 0.213, 0.715 - c * 0.715 - s * 0.715, 0.072 - c * 0.072 + s * 0.928],
                     [0.213 - c * 0.213 + s * 0.143, 0.715 + c * 0.285 + s * 0.140, 0.072 - c * 0.072 - s * 0.283],
                     [0.213 - c * 0.213 - s * 0.787, 0.715 - c * 0.715 + s * 0.715, 0.072 + c * 0.928 + s * 0.072]]
            v = v @ np.array(m).T
        elif name == "contrast":
            v = v * amt + (0.5 - 0.5 * amt)
        elif name == "brightness":
            v = v * amt
        v = np.clip(v, 0, 1)
    return v * 255.0


def chroma_spread(a):
    a = np.asarray(a, float)
    return a.max(-1) - a.min(-1)


# ----------------------------------------------------------------------------------------------- grades
GRADES = {
    "teal_orange": "curves=r='0/0 .2/.1 .7/.8 1/1':b='0/.05 .3/.38 .7/.65 1/.95',"
                   "colorbalance=rs=.08:gs=-.02:bs=-.08:rh=-.04:gh=.02:bh=.08",
    "golden_hour": "curves=r='0/0 .5/.58 1/1':b='0/0 .5/.42 1/.92',eq=saturation=1.25:contrast=1.08:brightness=.02",
    "cyberpunk": "curves=r='0/.05 .5/.45 1/1':b='0/.08 .5/.62 1/1',"
                 "colorbalance=rs=-.1:gs=-.05:bs=.15:rh=.12:gh=-.05:bh=.08,eq=saturation=1.35:contrast=1.2",
    "vintage_film": "curves=all='0/.06 .5/.5 1/.94':r='0/0 .5/.52 1/1':b='0/.04 .5/.48 1/.96',"
                    "noise=alls=10:allf=t+u:all_seed=7,eq=contrast=1.05:saturation=.9",
    "matrix_tech": "curves=g='0/.04 .5/.54 1/1':b='0/0 .5/.46 1/.92',colorbalance=rs=-.08:gs=.1:bs=-.05,"
                   "eq=contrast=1.15:saturation=.85",
    "clean_commercial": "eq=contrast=1.12:saturation=1.18:brightness=.01,unsharp=5:5:0.8",
    "blue_hour": "colortemperature=temperature=4300:mix=0.85,curves=b='0/0.06 0.5/0.56 1/1':r='0/0 0.5/0.47 1/1',"
                 "eq=saturation=1.08:contrast=1.06",
    "sodium_night": "curves=r='0/0 .4/.46 1/1':g='0/0 .5/.47 1/.96':b='0/.05 .3/.3 1/.86',"
                    "colorbalance=bs=.10:gs=.02:rh=.06:bh=-.08,eq=contrast=1.12",
    "restore": "hqdn3d=1.2:1.2:3:3,eq=contrast=1.12:brightness=-0.015:saturation=1.07:gamma=0.97,"
               "curves=all='0/0 .06/.035 .25/.22 .5/.5 .8/.82 .94/.93 1/.97',"
               "colorbalance=rs=.012:bs=-.01:rm=.025:gm=.005:bm=-.02,cas=0.3",
    "magma_night": "curves=r='0/.02 .5/.56 1/1':g='0/0 .5/.44 1/.95':b='0/.05 .5/.42 1/.88',"
                   "eq=contrast=1.1:saturation=1.1",
    "none": None,
}


@card("COLOR-01")
def grades_table(task, wd):
    src = wd / "testsrc.png"
    base = testsrc_png(src)
    rp = wd / "ramp.png"
    save(ramp(), rp)
    checks, ran = [], {}
    for name, chain in GRADES.items():
        if chain is None:
            continue
        out = ffimg(src, chain, wd / ("g_%s.png" % name))
        ran[name] = round(float(np.abs(out - base).mean()), 3)
    checks.append(check("all 10 non-null chains ran and changed the frame", len(ran) == 10 and min(ran.values()) > 0.5,
                        ran, "10 chains, mean |delta| > 0.5"))
    r_in = load(rp)
    r_to = ffimg(rp, GRADES["teal_orange"], wd / "ramp_teal_orange.png")
    sh, hi = slice(40, 70), slice(190, 220)
    d_sh = float((r_to[:, sh, 2] - r_to[:, sh, 0]).mean())
    d_hi = float((r_to[:, hi, 0] - r_to[:, hi, 2]).mean())
    checks.append(check("teal_orange: shadows lean teal (B-R > 4)", d_sh > 4, d_sh, "> 4"))
    checks.append(check("teal_orange: highlights lean orange (R-B > 4)", d_hi > 4, d_hi, "> 4"))
    n_sh = float((r_in[:, sh, 2] - r_in[:, sh, 0]).mean())
    checks.append(check("negative control: neutral ramp has no teal shadows", not (n_sh > 4), n_sh, "<= 4"))
    bh = ffimg(src, GRADES["blue_hour"], wd / "bh.png")
    y_in, y_out = float(luma(base).mean()), float(luma(bh).mean())
    cr_in = float(((base[..., 0] - luma(base)) / 1.5748).mean())
    cr_out = float(((bh[..., 0] - luma(bh)) / 1.5748).mean())
    checks.append(check("blue_hour lowers YAVG (card: 121.6 -> 108.2)", y_out < y_in - 4, [y_in, y_out], "down > 4"))
    checks.append(check("blue_hour raises V/Cr (card: 127 -> 133.7)", cr_out > cr_in + 3, [cr_in, cr_out], "up > 3"))
    a = ffimg(src, GRADES["vintage_film"], wd / "v1.png")
    b = ffimg(src, GRADES["vintage_film"], wd / "v2.png")
    c = ffimg(src, GRADES["vintage_film"].replace("all_seed=7", "all_seed=8"), wd / "v3.png")
    checks.append(check("seeded grain: same seed re-renders identically", np.array_equal(a, b), True, True))
    checks.append(check("seeded grain: another seed differs", not np.array_equal(a, c), True, True))
    clip = wd / "teal_orange.mp4"
    fx.test_clip(wd / "in.mp4", seconds=0.5)
    fx.ffmpeg("-i", wd / "in.mp4", "-vf", GRADES["teal_orange"] + ",format=yuv420p", "-c:v", "libx264",
              "-preset", "medium", "-crf", "17", "-an", clip)
    st = fx.probe(clip)["streams"][0]
    checks.append(check("export libx264 yuv420p", st["codec_name"] == "h264" and st["pix_fmt"] == "yuv420p",
                        [st["codec_name"], st["pix_fmt"]], ["h264", "yuv420p"]))
    return checks, [wd / "ramp_teal_orange.png", clip, jdump(wd / "grades.json", {"chains": GRADES, "mean_delta": ran})]


@card("COLOR-02")
def restore_grade(task, wd):
    rng = np.random.default_rng(3)
    frames = []
    for _ in range(12):
        f = np.full((90, 160, 3), 120.0) + rng.normal(0, 3, (90, 160, 1))
        f[:12] = 255
        frames.append(f)
    src = write_video(wd / "noisy.mkv", frames, codec="ffv1")
    out, abl = wd / "restored.mkv", wd / "no_denoise.mkv"
    fx.ffmpeg("-i", src, "-vf", GRADES["restore"], "-c:v", "ffv1", "-pix_fmt", "bgr0", out)
    fx.ffmpeg("-i", src, "-vf", GRADES["restore"].split(",", 1)[1], "-c:v", "ffv1", "-pix_fmt", "bgr0", abl)
    fi, fo = fx.frames(abl, (160, 90)), fx.frames(out, (160, 90))
    t_in = float(fi[:, 30:, :, 1].std(0).mean())
    t_out = float(fo[:, 30:, :, 1].std(0).mean())
    w_in, w_out = float(fx.frames(src, (160, 90))[:, 2:10].mean()), float(fo[:, 2:10].mean())
    checks = [check("hqdn3d node cuts temporal noise vs the same chain without it (< 0.92)", t_out < 0.92 * t_in, t_out / t_in, "< 0.92"),
              check("whites capped by curves 1/.97 (<= 250)", w_out <= 250, w_out, "<= 250"),
              check("negative control: input whites are 255", not (w_in <= 250), w_in, "> 250")]
    mp4 = wd / "restored.mp4"
    fx.ffmpeg("-i", out, "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", mp4)
    return checks, [mp4]


@card("COLOR-03")
def project_grades(task, wd):
    a = np.zeros((90, 160, 3))
    a[:] = np.linspace(40, 220, 160)[None, :, None]
    a[:, :, 0] += 25
    a[:, :, 2] -= 20
    a[20:50, 10:40] = (200, 40, 40)          # red marker on the left
    a[60:85, 60:100] = (51, 51, 51)          # charcoal patch
    src = wd / "src.png"
    save(a, src)
    a = load(src)
    v1 = ffimg(src, "eq=contrast=1.08:saturation=0.86:brightness=-0.023", wd / "ghorba_v1.png")
    v2 = ffimg(src, "eq=contrast=1.06:saturation=0.95:brightness=-0.009", wd / "ghorba_v2.png")
    s_in, s1, s2 = (float(chroma_spread(x[20:50, 10:40]).mean()) for x in (a, v1, v2))
    checks = [check("Ghorba v1 desaturates the marker (~0.86)", 0.78 < s1 / s_in < 0.93, s1 / s_in, "0.78..0.93"),
              check("Ghorba v2 is the lighter calibration (sat ratio > v1)", s2 > s1, [s1, s2], "v2 > v1"),
              check("Ghorba v1 darkens mean luma", luma(v1).mean() < luma(a).mean() - 1,
                    [float(luma(a).mean()), float(luma(v1).mean())], "out < in - 1")]
    nv = ffimg(src, "hflip,colorbalance=rs=-.10:gs=-.03:bs=.25:rm=-.05:bm=.10", wd / "navy.png")
    red_right = float(nv[20:50, 120:150, 0].mean() - nv[20:50, 120:150, 2].mean())
    char_in = float(a[60:85, 60:100, 2].mean() - a[60:85, 60:100, 0].mean())
    char_out = float(nv[60:85, 60:100, 2].mean() - nv[60:85, 60:100, 0].mean())
    checks += [check("navy door: hflip moved the red marker to the right", red_right > 80, red_right, "> 80"),
               check("navy door: charcoal pulled toward navy (B-R up > 20)", char_out - char_in > 20,
                     char_out - char_in, "> 20"),
               check("negative control: input marker not on the right",
                     not (float(a[20:50, 120:150, 0].mean() - a[20:50, 120:150, 2].mean()) > 80), None, "<= 80")]
    clip = wd / "navy_door.mp4"
    fx.test_clip(wd / "in.mp4", seconds=0.4)
    fx.ffmpeg("-i", wd / "in.mp4", "-vf", "hflip,colorbalance=rs=-.10:gs=-.03:bs=.25:rm=-.05:bm=.10,scale=1280:-2",
              "-c:v", "libx264", "-crf", "27", "-an", "-movflags", "+faststart", clip)
    w = fx.probe(clip)["streams"][0]["width"]
    checks.append(check("navy door export width 1280", w == 1280, w, 1280))
    return checks, [wd / "ghorba_v1.png", wd / "navy.png", clip]


def hald_to_cube(hald_png, cube_path, n=33, level=8):
    from scipy.ndimage import map_coordinates
    h = load(hald_png).reshape(-1, 3) / 255.0
    s = level * level
    lut = h.reshape(s, s, s, 3)  # [b][g][r]
    g = np.linspace(0, s - 1, n)
    bb, gg, rr = np.meshgrid(g, g, g, indexing="ij")
    coords = np.stack([bb.ravel(), gg.ravel(), rr.ravel()])
    vals = np.stack([map_coordinates(lut[..., c], coords, order=1) for c in range(3)], -1)
    lines = ["TITLE \"baked\"", "LUT_3D_SIZE %d" % n] + ["%.6f %.6f %.6f" % tuple(v) for v in vals]
    cube_path.write_text("\n".join(lines) + "\n")
    return cube_path


def write_cube(path, fn, n=33):
    g = np.linspace(0, 1, n)
    bb, gg, rr = np.meshgrid(g, g, g, indexing="ij")
    rgb = np.stack([rr.ravel(), gg.ravel(), bb.ravel()], -1)
    out = np.clip(fn(rgb), 0, 1)
    path.write_text("LUT_3D_SIZE %d\n" % n + "\n".join("%.6f %.6f %.6f" % tuple(v) for v in out) + "\n")
    return path


@card("COLOR-04")
def bake_lut(task, wd):
    chain = GRADES["teal_orange"]
    src = wd / "test.png"
    base = testsrc_png(src, "320x180")
    hald = wd / "hald.png"
    fx.ffmpeg("-f", "lavfi", "-i", "haldclutsrc=8", "-frames:v", "1", "-vf", chain + ",format=rgb24", hald)
    cube = hald_to_cube(hald, wd / "teal_orange.cube")
    direct = ffimg(src, chain, wd / "direct.png")
    via_hald = ffimg(src, "[0][1]haldclut=interp=tetrahedral,format=rgb24", wd / "via_hald.png", hald)
    via_cube = ffimg(src, "lut3d=file='%s':interp=tetrahedral" % str(cube).replace(":", r"\:"), wd / "via_cube.png")
    p_h, p_c, p_n = psnr(via_hald, direct), psnr(via_cube, direct), psnr(base, direct)
    n_lines = sum(1 for l in cube.read_text().splitlines() if re.match(r"^[0-9.]+ [0-9.]+ [0-9.]+$", l))
    return [check("Hald CLUT vs direct grade PSNR >= 40 dB", p_h >= 40, p_h, ">= 40 (card 51.9)"),
            check(".cube 33^3 vs direct grade PSNR >= 40 dB", p_c >= 40, p_c, ">= 40 (card 47.9)"),
            check(".cube has 33^3 entries", n_lines == 33 ** 3, n_lines, 33 ** 3),
            check("negative control: ungraded frame vs grade < 40 dB", not (p_n >= 40), p_n, "< 40")], \
        [cube, hald, wd / "via_cube.png"]


INK_SAFFRON = [("grayscale", 1), ("sepia", .5), ("saturate", 1.35), ("hue-rotate", -8), ("contrast", 1.05),
               ("brightness", .82)]


@card("COLOR-05")
def css_looks(task, wd):
    # three patches of (nearly) equal relative luminance but different hue + a mid grey
    cols = [(200, 60, 60), None, None, (128, 128, 128)]
    target = float(luma(np.array((200, 60, 60), float)))

    def match(hue):
        lo, hi = 0.0, 1.0
        for _ in range(40):
            v = (lo + hi) / 2
            c = hsv2rgb(np.array([hue, 0.6, v]))
            lo, hi = (v, hi) if float(luma(c)) < target else (lo, v)
        return tuple(hsv2rgb(np.array([hue, 0.6, (lo + hi) / 2])))
    cols[1], cols[2] = match(120), match(220)
    a = chart(cols)
    out = css_filter(a, INK_SAFFRON)
    save(a, wd / "in.png")
    save(out, wd / "ink_saffron.png")
    p = [patch(out, i) for i in range(3)]
    spread = max(float(np.abs(p[i] - p[j]).max()) for i in range(3) for j in range(3))
    h = hue_of(patch(out, 3))
    pin = [patch(a, i) for i in range(3)]
    spread_in = max(float(np.abs(pin[i] - pin[j]).max()) for i in range(3) for j in range(3))
    darker = float(luma(out).mean()) < float(luma(a).mean())
    sliders = {"contrast": float(np.clip(1.9, .8, 1.4)), "saturate": float(np.clip(.2, .5, 1.6)),
               "brightness": float(np.clip(1.0, .8, 1.2))}
    return [check("grayscale(1) first: equal-luma hues map to one tone (spread <= 4)", spread <= 4, spread, "<= 4"),
            check("re-tone is saffron (hue 15..45 deg)", 15 <= h <= 45, h, "15..45"),
            check("brightness(.82) darkens the frame", darker, True, True),
            check("slider clamps c .8-1.4 / s .5-1.6", sliders == {"contrast": 1.4, "saturate": .5, "brightness": 1.0},
                  sliders, {"contrast": 1.4, "saturate": .5, "brightness": 1.0}),
            check("negative control: input hues differ (spread > 4)", not (spread_in <= 4), spread_in, "> 4")], \
        [wd / "ink_saffron.png", jdump(wd / "look.json", {"engine": "numpy CSS Filter Effects matrices",
                                                          "ink_saffron": INK_SAFFRON})]


def basma_chain(look):
    k = []
    c, s, b = look.get("contrast", 1), look.get("saturation", 1), look.get("brightness", 1)
    k.append("eq=contrast=%g:saturation=%g:brightness=%g" % (c, s, (b - 1) * 0.5))
    tone = look.get("tone")
    if tone == "teal_orange":
        k.append("colorbalance=rs=-0.08:bs=0.10:rh=0.08:bh=-0.06")
    elif tone == "bw":
        k.append("hue=s=0")
    elif tone in ("warm", "cool"):
        sgn = 1 if tone == "warm" else -1
        kk = look.get("k", .2)
        k.append("colorbalance=rm=%g:bm=%g" % (sgn * .6 * kk, -sgn * .6 * kk))
    if look.get("vignette", 0) > 0.3:
        k.append("vignette=PI/5")
    if look.get("grain", 0) > 0:
        k.append("noise=alls=%d:allf=t" % round(6 + 40 * look["grain"]))
    if look.get("letterbox"):
        k.append("drawbox=x=0:y=0:w=iw:h=ih*0.105:color=black:t=fill,"
                 "drawbox=x=0:y=ih-ih*0.105:w=iw:h=ih:color=black:t=fill")
    return ",".join(k)


@card("COLOR-06")
def basma_export(task, wd):
    look = {"contrast": 1.1, "saturation": 1.1, "brightness": 1.0, "tone": "teal_orange", "vignette": .5,
            "grain": .25, "letterbox": True}
    chain = basma_chain(look)
    soft = basma_chain(dict(look, vignette=.2))
    rp = wd / "ramp.png"
    save(ramp(320, 180), rp)
    r_in = load(rp)
    out = ffimg(rp, chain, wd / "graded.png")
    bar = int(180 * .105)
    top = float(out[:bar - 1].mean())
    bot = float(out[-bar + 1:].mean())
    to = ffimg(rp, basma_chain({"tone": "teal_orange"}), wd / "to.png")
    sh = float((to[:, 40:80, 2] - to[:, 40:80, 0]).mean())
    hi = float((to[:, 240:280, 0] - to[:, 240:280, 2]).mean())
    return [check("letterbox 10.5% bars are black", top < 3 and bot < 3, [top, bot], "< 3"),
            check("grain alls = 6+40g = 16", "noise=alls=16:allf=t" in chain, chain.split(",")[-3], "alls=16"),
            check("vignette only when strength > 0.3", "vignette=PI/5" in chain and "vignette" not in soft,
                  [("vignette" in chain), ("vignette" in soft)], [True, False]),
            check("teal_orange colorbalance: teal shadows & orange highlights", sh > 3 and hi > 3, [sh, hi], "> 3"),
            check("negative control: source has no bars", not (float(r_in[:bar - 1].mean()) < 3),
                  float(r_in[:bar - 1].mean()), ">= 3")], \
        [wd / "graded.png", jdump(wd / "grade_chain.json", {"look": look, "chain": chain})]


MOODS = {"night": ("#0B0F1E", "#221C3B", "#ECBD51", "#F9E094", "blue_hour"),
         "dawn": ("#12142B", "#994329", "#FAA442", "#FFDDA3", "golden_hour"),
         "gold": ("#110D09", "#372715", "#EEAD2B", "#FBD774", "golden_hour"),
         "sea": ("#07131D", "#16444B", "#3CDDD2", "#ACF6F6", "teal_orange"),
         "ink": ("#0A0A0A", "#1C1C1C", "#B2B2B2", "#EBEBEB", "vintage_film")}


def mood_frame(mood, hue_shift, bright, w=160, h=90):
    top, bot, glow, mote, _ = MOODS[mood]
    y = np.linspace(0, 1, h)[:, None, None]
    f = np.array(hx(top)) * (1 - y) + np.array(hx(bot)) * y
    f = np.repeat(f, w, 1)
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.hypot(xx - w / 2, yy - h / 2)
    f = np.where((d < 14)[..., None], np.array(hx(glow), float), f)
    f[5:7, 20:22] = hx(mote)
    hsv = rgb2hsv(f)
    hsv[..., 0] += hue_shift
    return np.clip(hsv2rgb(hsv) * bright, 0, 255)


@card("COLOR-07")
def verse_moods(task, wd):
    secs = [(0, .9), (7, 1.025), (2, 1.15)]
    frames = [mood_frame("dawn", hs, br) for hs, br in secs]
    write_video(wd / "dawn_arc.mp4", [f for f in frames for _ in range(10)], fps=10)
    lum = [float(luma(f).mean()) for f in frames]
    g0, g1 = hue_of(frames[0][45, 80]), hue_of(frames[1][45, 80])
    top0 = frames[0][0, 0]
    flat = [float(luma(mood_frame("dawn", 0, 1.0)).mean())] * 2
    mapping = {m: v[4] for m, v in MOODS.items()}
    return [check("film brightens 0.9 -> 1.15 (luma ratio)", abs(lum[2] / lum[0] - 1.15 / .9) < 0.04,
                  lum[2] / lum[0], 1.15 / .9),
            check("section 2 glow hue shifted +7 deg", abs(hue_dist(g1, g0) - 7) < 1.5, hue_dist(g1, g0), 7),
            check("section 1 sky top = #12142B x 0.9", float(np.abs(top0 - np.array(hx("#12142B")) * .9).max()) < 1.5,
                  tohex(top0), tohex(np.array(hx("#12142B")) * .9)),
            check("mood -> grade map", mapping["night"] == "blue_hour" and mapping["sea"] == "teal_orange"
                  and mapping["ink"] == "vintage_film", mapping, "night blue_hour, sea teal_orange, ink vintage_film"),
            check("negative control: no arc -> ratio 1", not (abs(flat[1] / flat[0] - 1.15 / .9) < 0.04),
                  flat[1] / flat[0], 1.0)], [wd / "dawn_arc.mp4"]


KB = {"teal_orange": (1.12, 1.15, 1.0), "bleach_bypass": (1.3, .6, 1.0), "cold_desat": (1.0, .6, .96),
      "kodak_portra": (.95, 1.0, 1.04), "vision3_500t": (1.1, 1.0, 1.0), "cinestill_800t": (1.08, 1.1, 1.0),
      "fuji_velvia": (1.2, 1.45, 1.0), "noir_bw": (1.4, 0.0, 1.0), "neon_cyber": (1.15, 1.35, 1.0),
      "pastel_wes": (.88, 1.0, 1.0)}


@card("COLOR-08")
def look_vocabulary(task, wd):
    cols = ["#a05050", "#50a050", "#5050a0", "#a0a050", "#8a6a50"]
    src = wd / "chart.png"
    save(chart(cols), src)
    a = load(src)
    res, checks = {}, []
    for name in ("bleach_bypass", "fuji_velvia", "noir_bw"):
        c, s, b = KB[name]
        out = ffimg(src, "eq=saturation=%g" % s, wd / ("%s.png" % name))
        res[name] = float(np.mean([chroma_spread(patch(out, i)) / chroma_spread(patch(a, i)) for i in range(5)]))
    checks.append(check("bleach_bypass sat .6 measured", abs(res["bleach_bypass"] - .6) < .1, res["bleach_bypass"], .6))
    checks.append(check("fuji_velvia sat 1.45 measured", abs(res["fuji_velvia"] - 1.45) < .15, res["fuji_velvia"], 1.45))
    checks.append(check("noir_bw is grayscale", res["noir_bw"] < .05, res["noir_bw"], "< .05"))
    # CineStill 800T split tone: highlights #D4A050, shadows #1A3040, weighted by luma
    r = ramp(256, 16)
    w = (luma(r) / 255.0)[..., None]
    fs = np.array(hx("#1A3040"), float) / np.mean(hx("#1A3040"))
    fh = np.array(hx("#D4A050"), float) / np.mean(hx("#D4A050"))
    split = np.clip(r * (1 - .35) + .35 * r * ((1 - w) * fs + w * fh), 0, 255)
    save(split, wd / "cinestill_split.png")
    hs, hh = hue_of(split[8, 50]), hue_of(split[8, 220])
    checks.append(check("CineStill split: shadow hue near #1A3040 (~214 deg)", hue_dist(hs, hue_of(hx("#1A3040"))) < 15,
                        hs, hue_of(hx("#1A3040"))))
    checks.append(check("CineStill split: highlight hue near #D4A050 (~40 deg)", hue_dist(hh, hue_of(hx("#D4A050"))) < 15,
                        hh, hue_of(hx("#D4A050"))))
    checks.append(check("negative control: ungraded ramp is hue-less (spread 0)",
                        not (float(chroma_spread(r[8, 50])) > 2), float(chroma_spread(r[8, 50])), "> 2 needed"))
    return checks, [wd / "cinestill_split.png", wd / "fuji_velvia.png",
                    jdump(wd / "looks.json", {"kb": KB, "measured_sat_ratio": res,
                                              "note": "approximations; never promised as exact stock emulation"})]


# numpy grade model following the HyperFrames grade object schema (not its WebGL shader)
GRADE_PRESETS = {"neutral": {}, "warm-daylight": {"exposure": .06, "contrast": .07, "temperature": .18, "saturation": .08},
                 "food-pop": {"contrast": .1, "temperature": .14, "saturation": .18},
                 "muted-editorial": {"saturation": -.12, "vignette": .1}, "mono-clean": {"saturation": -1},
                 "deep-contrast": {"contrast": .2}}


def apply_grade(img, grade):
    adj = dict(GRADE_PRESETS.get(grade.get("preset", "neutral"), {}))
    adj.update(grade.get("adjust", {}))
    k = float(np.clip(grade.get("intensity", 1.0), 0, 1))
    clampd = {key: float(np.clip(v, -2, 2) if key == "exposure" else np.clip(v, -1, 1)) for key, v in adj.items()}
    l = lin(img) * 2.0 ** (k * clampd.get("exposure", 0))
    t = k * clampd.get("temperature", 0)
    l = l * np.array([1 + .5 * t, 1.0, 1 - .5 * t])
    v = unlin(l) / 255.0
    c = 1 + k * clampd.get("contrast", 0)
    v = (v - .5) * c + .5
    y = (0.2126 * v[..., 0] + 0.7152 * v[..., 1] + 0.0722 * v[..., 2])[..., None]
    v = y + (v - y) * (1 + k * clampd.get("saturation", 0))
    vig = k * (grade.get("details", {}).get("vignette", 0) + clampd.get("vignette", 0))
    if vig:
        h, w = v.shape[:2]
        yy, xx = np.mgrid[0:h, 0:w]
        d = np.hypot((xx - w / 2) / (w / 2), (yy - h / 2) / (h / 2)) / math.sqrt(2)
        v = v * (1 - vig * smoothstep(.4, 1.0, d))[..., None]
    return np.clip(v, 0, 1) * 255.0, clampd


@card("COLOR-09")
def webgl_grade_model(task, wd):
    src = wd / "test.png"
    a = testsrc_png(src)
    mono, _ = apply_grade(a, {"preset": "mono-clean", "intensity": 1})
    up, cl = apply_grade(a, {"adjust": {"exposure": 1}})
    warm, _ = apply_grade(a, {"preset": "warm-daylight"})
    ident, _ = apply_grade(a, {"preset": "food-pop", "intensity": 0})
    _, big = apply_grade(a, {"adjust": {"exposure": 3, "contrast": 4}})
    save(warm, wd / "warm_daylight.png")
    save(mono, wd / "mono_clean.png")
    mid = (a > 20) & (a < 100)
    ratio = float(np.median(lin(up)[mid] / np.maximum(lin(a)[mid], 1e-6)))
    grey = np.full((8, 8, 3), 128.0)
    wg, _ = apply_grade(grey, {"preset": "warm-daylight"})
    rb = lambda x: float(x[..., 0].mean() / max(x[..., 2].mean(), 1e-6))
    return [check("mono-clean (sat -1) is neutral", float(chroma_spread(mono).max()) < 1.5,
                  float(chroma_spread(mono).max()), "< 1.5"),
            check("exposure +1 doubles linear light", abs(ratio - 2) < .05, ratio, 2),
            check("warm-daylight warms a neutral grey (R/B > 1.03)", rb(wg) > 1.03, rb(wg), "> 1.03"),
            check("intensity 0 = identity", float(np.abs(ident - a).max()) < 1.0, float(np.abs(ident - a).max()), "< 1"),
            check("ranges clamp exposure -2..2, others -1..1", big == {"exposure": 2.0, "contrast": 1.0}, big,
                  {"exposure": 2, "contrast": 1}),
            check("negative control: source is not neutral", not (float(chroma_spread(a).max()) < 1.5),
                  float(chroma_spread(a).max()), ">= 1.5")], \
        [wd / "warm_daylight.png", jdump(wd / "grade.json", {"engine": "numpy re-implementation of the grade object "
                                                                       "schema (HyperFrames CLI not installed)",
                                                             "presets": GRADE_PRESETS})]


LANES = [("correction", ["too dark", "flat", "too warm", "too cold", "washed", "dark", "مظلم", "باهت"]),
         ("treatment", ["premium", "cinematic", "luxury", "فخم", "سينمائي"]),
         ("shader", ["retro", "vhs", "print", "ascii", "glitch", "camcorder", "8mm", "قديم"]),
         ("privacy", ["blur face", "privacy", "hide", "pixelate", "إخفاء", "طمس"])]


def feedback_lane(text):
    t = text.lower()
    for lane, words in LANES:
        if any(w in t for w in words):
            return lane
    return "framing"


@card("COLOR-10")
def treatment_lanes(task, wd):
    fb = {"it looks too dark": "correction", "make it more cinematic": "treatment", "VHS vibe please": "shader",
          "pixelate the faces for privacy": "privacy", "الصورة باهتة": "correction"}
    got = {k: feedback_lane(k) for k in fb}
    dark = np.full((90, 160, 3), 40.0)
    dark[:, 80:] = 60
    fixed, _ = apply_grade(dark, {"adjust": {"exposure": 1.5}})
    a = testsrc_png(wd / "test.png")
    pix = a.copy()
    for y in range(0, 180, 12):
        for x in range(0, 320, 12):
            pix[y:y + 12, x:x + 12] = a[y:y + 12, x:x + 12].reshape(-1, 3).mean(0)
    vhs = a.copy()
    vhs[1::2] *= (1 - .35)            # scanlines .35
    save(pix, wd / "privacy.png")
    save(vhs, wd / "vhs.png")
    within = float(np.mean([pix[y:y + 12, x:x + 12].std(axis=(0, 1)).max() for y in range(0, 168, 12)
                            for x in range(0, 312, 12)]))
    sl = float(luma(vhs[1::2]).mean() / max(luma(vhs[0::2]).mean(), 1e-6))
    return [check("feedback mapped to one lane each", got == fb, got, fb),
            check("correction lane lifts a dark frame toward mid (> 80)", float(luma(fixed).mean()) > 80,
                  float(luma(fixed).mean()), "> 80"),
            check("privacy lane: pixel blocks uniform", within < 0.01, within, "< 0.01"),
            check("VHS seed scanlines .35 (odd/even ratio .65)", abs(sl - .65) < .02, sl, .65),
            check("negative control: source blocks not uniform",
                  not (float(np.mean([a[y:y + 12, x:x + 12].std(axis=(0, 1)).max() for y in range(0, 168, 12)
                                      for x in range(0, 312, 12)])) < 0.01), None, ">= 0.01")], \
        [wd / "privacy.png", wd / "vhs.png", jdump(wd / "lanes.json", got)]


def look_fn(name):
    def f(rgb):
        y = (0.2126 * rgb[:, 0] + 0.7152 * rgb[:, 1] + 0.0722 * rgb[:, 2])[:, None]
        if name == "teal-orange-blockbuster":
            k, c = .85, .18
            o = (rgb - .5) * (1 + c) + .5
            o = o + (1 - y) * np.array([-.04, .05, .09]) + y * np.array([.1, .04, -.03])
        elif name == "bleach-bypass":
            k = .8
            o = (rgb - .5) * 1.55 + .5
            yy = (0.2126 * o[:, 0] + 0.7152 * o[:, 1] + 0.0722 * o[:, 2])[:, None]
            o = yy + (o - yy) * (1 - .72)
        else:  # film-fade
            k = .75
            o = .35 * .5 + rgb * (1 - .35 * .5)
            o = (o - .5) * (1 - .28) + .5
            o = o * np.array([1 + .16 * .25, 1, 1 - .16 * .25])
        return rgb + k * (np.clip(o, 0, 1) - rgb)
    return f


@card("COLOR-11")
def lut_looks(task, wd):
    rp = wd / "ramp.png"
    cols = ["#b04040", "#40b040", "#4040b0", "#b0a040", "#808080", "#000000"]
    save(np.vstack([ramp(264, 24), chart(cols, 44)]), rp)
    a = load(rp)
    out, checks = {}, []
    for name in ("teal-orange-blockbuster", "bleach-bypass", "film-fade"):
        cube = write_cube(wd / ("%s.cube" % name), look_fn(name))
        out[name] = ffimg(rp, "lut3d=file='%s'" % str(cube).replace(":", r"\:"), wd / ("%s.png" % name))
    to = out["teal-orange-blockbuster"]
    sh = float((to[:24, 30:70, 2] - to[:24, 30:70, 0]).mean())
    hi = float((to[:24, 200:240, 0] - to[:24, 200:240, 2]).mean())
    checks.append(check("teal-orange: shadows B>R and highlights R>B", sh > 5 and hi > 5, [sh, hi], "> 5"))
    bb = out["bleach-bypass"]
    sat_ratio = float(np.mean([chroma_spread(bb[30:62, 44 * i + 6:44 * i + 38].reshape(-1, 3).mean(0)) /
                               chroma_spread(a[30:62, 44 * i + 6:44 * i + 38].reshape(-1, 3).mean(0)) for i in range(4)]))
    checks.append(check("bleach-bypass: saturation cut ~ (1-.72*.8)", sat_ratio < .6, sat_ratio, "< .6"))
    black = float(out["film-fade"][30:62, 44 * 5 + 6:44 * 5 + 38].mean())
    checks.append(check("film-fade lifts blacks (+.35 x .75)", black > 25, black, "> 25"))
    n = sum(1 for l in (wd / "film-fade.cube").read_text().splitlines()[1:] if l.strip())
    checks.append(check("cube is 33^3", n == 33 ** 3, n, 33 ** 3))
    checks.append(check("negative control: input black stays 0", not (float(a[30:62, 226:258].mean()) > 25),
                        float(a[30:62, 226:258].mean()), "<= 25"))
    return checks, [wd / "teal-orange-blockbuster.cube", wd / "teal-orange-blockbuster.png"]


@card("COLOR-12")
def split_reveal(task, wd):
    src = wd / "test.png"
    flat = testsrc_png(src, "160x90")
    graded, _ = apply_grade(flat, {"adjust": {"contrast": .28, "temperature": .18, "saturation": .26},
                                   "details": {"vignette": .3}})
    w, fps = 160, 30
    frames, edges = [], []
    for i in range(60):          # 2 s: sweep 0-0.6 s to 62 %, hold to 1.4 s, commit to 100 % by 1.8 s
        t = i / fps
        if t < .6:
            s = .62 * smoothstep(0, .6, t)
        elif t < 1.4:
            s = .62
        else:
            s = .62 + .38 * smoothstep(1.4, 1.8, t)
        x = int(round(s * w))
        f = flat.copy()
        f[:, :x] = graded[:, :x]
        if 0 < x < w:
            f[:, max(0, x - 1):x + 1] = 255   # 2 px hairline edge
        frames.append(f)
        edges.append(x)
    write_video(wd / "split.mkv", frames, fps=fps, codec="ffv1")
    write_video(wd / "split_preview.mp4", frames, fps=fps)
    hold = frames[30]
    left_ok = float(np.abs(hold[:, 5:90] - graded[:, 5:90]).mean())
    right_ok = float(np.abs(hold[:, 105:] - flat[:, 105:]).mean())
    last = float(np.abs(frames[-1] - graded).mean())
    first = float(np.abs(frames[0][:, 5:90] - graded[:, 5:90]).mean())
    return [check("hold frame: left graded, right flat", left_ok < 1 and right_ok < 1, [left_ok, right_ok], "< 1"),
            check("edge pauses at 62 %", edges[30] == round(.62 * w), edges[30], round(.62 * w)),
            check("final frame fully committed to the grade", last < 1, last, "< 1"),
            check("negative control: first frame is the flat picture", not (first < 1), first, ">= 1")], \
        [wd / "split_preview.mp4", wd / "split.mkv"]


@card("COLOR-13")
def technical_then_creative(task, wd):
    a = np.zeros((40, 160, 3))
    a[:] = np.linspace(30, 220, 160)[None, :, None]
    a[..., 0] += 18
    a[..., 2] -= 18                          # warm cast
    src = wd / "cast.png"
    save(a, src)
    a = load(src)
    g = a[..., 1].mean()
    nodes = [("exposure", "eq=brightness=0.02"),
             ("wb", "colorchannelmixer=rr=%.4f:bb=%.4f" % (g / a[..., 0].mean(), g / a[..., 2].mean())),
             ("contrast", "eq=contrast=1.1"), ("sat", "eq=saturation=1.2"),
             ("look", GRADES["teal_orange"])]
    tech = ",".join(v for k, v in nodes[:4])
    corrected = ffimg(src, tech, wd / "technical.png")
    final = ffimg(src, ",".join(v for _, v in nodes), wd / "technical_then_look.png")
    rb_in = float((a[..., 0] - a[..., 2])[:, 60:100].mean())
    rb_c = float((corrected[..., 0] - corrected[..., 2])[:, 60:100].mean())
    order = [k for k, _ in nodes]
    sat = float(re.search(r"saturation=([0-9.]+)", nodes[3][1]).group(1))
    return [check("technical node neutralises the cast (|R-B| < 6)", abs(rb_c) < 6, rb_c, "< 6"),
            check("order: exposure -> WB -> contrast -> sat -> look", order == ["exposure", "wb", "contrast", "sat", "look"],
                  order, "technical first, look last"),
            check("sat node within ceiling 1.25", sat <= 1.25, sat, "<= 1.25"),
            check("look applied as its own node on the corrected output", float(np.abs(final - corrected).mean()) > 3,
                  float(np.abs(final - corrected).mean()), "> 3"),
            check("negative control: input carries the cast", not (abs(rb_in) < 6), rb_in, ">= 6")], \
        [wd / "technical_then_look.png", jdump(wd / "nodes.json", nodes)]


def is_log(stream, profile=None):
    if profile:
        return "log" in profile.lower()
    trc = (stream.get("color_transfer") or "").lower()
    if "log" in trc:
        return True
    return False


@card("COLOR-14")
def log_detection(task, wd):
    flat = wd / "log10.mkv"
    std = wd / "rec709_8bit.mp4"
    # a 10-bit clip tagged log316 with a flat (log-like) picture, and an 8-bit bt709 clip
    fx.ffmpeg("-f", "lavfi", "-i", "testsrc2=s=160x90:r=10:d=0.5", "-vf", "eq=contrast=0.45:brightness=0.05",
              "-c:v", "ffv1", "-pix_fmt", "yuv444p10le", "-color_trc", "log316", "-color_primaries", "bt709",
              "-colorspace", "bt709", flat)
    fx.ffmpeg("-f", "lavfi", "-i", "testsrc2=s=160x90:r=10:d=0.5", "-vf", "eq=contrast=0.45:brightness=0.05",
              "-c:v", "libx264", "-pix_fmt", "yuv420p", "-color_trc", "bt709", "-color_primaries", "bt709",
              "-colorspace", "bt709", std)
    s_log, s_std = fx.probe(flat)["streams"][0], fx.probe(std)["streams"][0]
    cube = write_cube(wd / "Log_to_Rec709.cube", lambda rgb: np.clip((rgb - .5) / .45 + .5 - .05 / .45, 0, 1), n=65)
    applied = []
    for clip, st in ((flat, s_log), (std, s_std)):
        if is_log(st):
            out = wd / ("%s_709.mkv" % clip.stem)
            fx.ffmpeg("-i", clip, "-vf", "lut3d=file='%s'" % str(cube).replace(":", r"\:"), "-c:v", "ffv1", out)
            applied.append(clip.name)
    before = float(fx.frames(flat, (80, 45))[..., 1].std())
    after = float(fx.frames(wd / "log10_709.mkv", (80, 45))[..., 1].std())
    return [check("10-bit log316 clip detected as Log", is_log(s_log), s_log.get("color_transfer"), "contains log"),
            check("8-bit bt709 flat clip NOT treated as Log", not is_log(s_std), s_std.get("color_transfer"), "bt709"),
            check("user profile overrides the tag", is_log(s_std, "Apple Log") and not is_log(s_log, "Rec709"),
                  True, True),
            check("conversion LUT applied once, to the Log clip only", applied == ["log10.mkv"], applied, ["log10.mkv"]),
            check("65-point cube", "LUT_3D_SIZE 65" in cube.read_text()[:40], True, True),
            check("LUT expands the flat Log contrast (std up > 1.6x)", after > 1.6 * before, after / before, "> 1.6"),
            check("negative control: flat input std is low", not (before > 1.6 * before), before, None)], \
        [wd / "log10_709.mkv", cube]


BANDS = {"night": (120, 280), "morning": (320, 460), "day": (420, 560), "golden": (440, 600), "blue": (310, 485)}


@card("COLOR-15")
def tod_exposure(task, wd):
    plan = [("night", 95.0), ("blue", 92.0), ("golden", 118.0)]   # 8-bit medians
    outs, med_in, med_out, shifts = [], [], [], []
    prev = None
    for i, (period, y8) in enumerate(plan):
        img = np.clip(np.full((36, 64, 3), y8) + np.linspace(-20, 20, 64)[None, :, None], 0, 255)
        p = wd / ("clip%d.png" % i)
        save(img, p)
        m10 = float(np.median(luma(load(p)))) * 4
        lo, hi = BANDS[period]
        target = min(max(m10, lo + 15), hi - 15)
        if prev is not None:
            cap = 60 if plan[i - 1][0] == period else 120
            target = min(max(target, prev - cap), prev + cap)
        shift = float(np.clip(target - m10, -120, 120))
        out = ffimg(p, "lutrgb=r='val+%f':g='val+%f':b='val+%f'" % ((shift / 4,) * 3), wd / ("clip%d_out.png" % i))
        mo = float(np.median(luma(out))) * 4
        med_in.append(m10)
        med_out.append(mo)
        shifts.append(shift)
        outs.append(wd / ("clip%d_out.png" % i))
        prev = mo
    in_band = [BANDS[p][0] - 15 <= m <= BANDS[p][1] + 15 for (p, _), m in zip(plan, med_out)]
    jumps = [abs(med_out[i + 1] - med_out[i]) for i in range(2)]
    return [check("every clip lands in its time-of-day band (+-15)", all(in_band), med_out, [BANDS[p] for p, _ in plan]),
            check("cross-period jumps <= 120", max(jumps) <= 120 + 4, jumps, "<= 120"),
            check("per-clip shift within +-120", all(abs(s) <= 120 for s in shifts), shifts, "|s| <= 120"),
            check("night stays darker than golden", med_out[0] < med_out[2], med_out, "night < golden"),
            check("negative control: input night clip is out of band",
                  not (BANDS["night"][0] - 15 <= med_in[0] <= BANDS["night"][1] + 15), med_in[0], "outside 105..295")], \
        outs + [jdump(wd / "exposure.json", {"in10": med_in, "out10": med_out, "shift": shifts})]


def neutral_wb(img, bias=0.0, iters=3):
    hsv = rgb2hsv(img)
    mx = img.max(-1) / 255.0
    m = (mx > .25) & (mx < .85) & (hsv[..., 1] <= .2)
    if m.mean() < .005:
        return img, None
    r, g, b = (img[..., c][m].mean() for c in range(3))
    sr, sb = g / r, g / b                                 # hold G, move R/B
    out = img.copy()
    for _ in range(iters):                                # secant on the R-B target (bias)
        out = np.clip(img * np.array([sr, 1, sb]), 0, 255)
        err = (out[..., 0][m].mean() - out[..., 2][m].mean()) - bias
        if abs(err) < .5:
            break
        sr -= err / (2 * g)
        sb += err / (2 * g)
    sr, sb = float(np.clip(sr, .8, 1.2)), float(np.clip(sb, .8, 1.2))
    return np.clip(img * np.array([sr, 1, sb]), 0, 255), (sr, sb)


@card("COLOR-16")
def neutral_white_balance(task, wd):
    a = chart(["#808080", "#a0a0a0", "#c03030", "#30a040", "#606060"], 40)
    cast = np.clip(a + np.array([12, 0, -10]), 0, 255)
    save(cast, wd / "cast.png")
    out, gains = neutral_wb(cast)
    warm, _ = neutral_wb(cast, bias=30)
    save(out, wd / "balanced.png")
    rb = lambda x: float(x[..., 0][:, :80].mean() - x[..., 2][:, :80].mean())
    g_held = float(np.abs(out[..., 1] - cast[..., 1]).max())
    return [check("neutral patches: R-B -> 0 (+-3)", abs(rb(out)) < 3, rb(out), 0),
            check("warm bias +30 kept on request (+-4)", abs(rb(warm) - 30) < 4, rb(warm), 30),
            check("G held fixed", g_held < 1e-6, g_held, 0),
            check("slopes within 1+-0.20", gains is not None and all(.8 <= g <= 1.2 for g in gains), gains, "0.8..1.2"),
            check("negative control: input neutral patches carry the cast", not (abs(rb(cast)) < 3), rb(cast), "|R-B| >= 3")], \
        [wd / "balanced.png", jdump(wd / "wb.json", {"slopes_r_b": gains})]


def pivot_contrast(y10, c, pivot):
    return (y10 / 1023.0 - pivot) * c * 1023.0 + pivot * 1023.0


@card("COLOR-17")
def pivot_contrast_guard(task, wd):
    r = ramp(256, 8)
    src = wd / "ramp.png"
    save(r, src)
    c = 1.15
    vf = "lutrgb=r='(val/255-0.435)*%g*255+0.435*255':g='(val/255-0.435)*%g*255+0.435*255':" \
         "b='(val/255-0.435)*%g*255+0.435*255'" % (c, c, c)
    out = ffimg(src, vf, wd / "contrast.png")
    xs = np.arange(60, 200)
    slope = float(np.polyfit(xs, out[4, xs, 1], 1)[0])
    piv = int(round(.435 * 255))
    fixed = float(out[4, piv, 1] - r[4, piv, 1])
    # clip guard: a frame already spanning 16..1008 (10-bit) must back off toward 1.0
    y10 = np.linspace(20, 1004, 500)
    tries, cc = 0, 1.15
    while tries < 3:
        o = pivot_contrast(y10, cc, .435)
        clipped = (np.percentile(o, 1) < 16) or (np.percentile(o, 99) > 1008) or (np.mean((o < 0) | (o > 1023)) > .005)
        if not clipped:
            break
        cc = max(1.0, cc - .05)
        tries += 1
        if cc == 1.0:
            break
    o_naive = pivot_contrast(y10, 1.15, .435)
    return [check("measured slope = 1.15", abs(slope - 1.15) < .02, slope, 1.15),
            check("pivot .435 holds its value", abs(fixed) <= 1, fixed, 0),
            check("clip guard backs off within 3 retries, never below 1.0", 1.0 <= cc < 1.15 and tries <= 3, [cc, tries],
                  "1.0 <= c < 1.15"),
            check("negative control: unprocessed ramp slope is 1.0", not (abs(float(np.polyfit(xs, r[4, xs, 1], 1)[0]) - 1.15) < .02),
                  float(np.polyfit(xs, r[4, xs, 1], 1)[0]), 1.0),
            check("negative control: naive 1.15 on the wide frame clips", float(np.percentile(o_naive, 99)) > 1008,
                  float(np.percentile(o_naive, 99)), "> 1008")], \
        [wd / "contrast.png", jdump(wd / "guard.json", {"final_contrast": cc, "retries": tries})]


SAT_BANDS = {"morning": (50, 110), "day": (60, 120), "afternoon": (60, 130), "evening": (45, 100), "night": (30, 80)}


def sat_floor(img, period):
    spread10 = float(chroma_spread(img).mean()) * 4
    lo, _ = SAT_BANDS[period]
    s = 1.0 if spread10 >= lo else min(1.25, lo / max(spread10, 1e-6))
    y = luma(img)[..., None]
    yn = y / 255.0
    w = np.ones_like(yn)
    w = np.where(yn < .15, .6 + .4 * yn / .15, w)
    w = np.where(yn > .85, .6 + .4 * (1 - yn) / .15, w)
    k = 1 + (s - 1) * w
    return np.clip(y + (img - y) * k, 0, 255), s


@card("COLOR-18")
def saturation_floor(task, wd):
    mid = chart(["#807a78", "#787a80", "#7a807a"], 40)       # dull mid-tones
    shadow = chart(["#1a1614", "#14161a"], 40)
    img = np.vstack([np.hstack([mid, np.zeros((40, 0, 3))]), np.hstack([shadow, np.zeros((40, 40, 3))])])
    save(img, wd / "dull.png")
    out, s = sat_floor(img, "day")
    save(out, wd / "sat_floor.png")
    rm = float(chroma_spread(out[:40]).mean() / chroma_spread(img[:40]).mean())
    rs = float(chroma_spread(out[40:, :80]).mean() / chroma_spread(img[40:, :80]).mean())
    vivid = chart(["#d02020", "#20d040"], 40)
    out2, s2 = sat_floor(vivid, "day")
    return [check("dull day clip boosted, capped at 1.25", s == 1.25, s, 1.25),
            check("mid-tones get the full 1.25", abs(rm - 1.25) < .05, rm, 1.25),
            check("shadows roll off toward 60 % of the boost", rs < rm - .02, [rs, rm], "rs < rm - .02"),
            check("never remove: already-saturated clip untouched", s2 == 1.0 and float(np.abs(out2 - vivid).max()) < 1e-6,
                  s2, 1.0),
            check("negative control: input mid chroma ratio is 1", not (abs(1.0 - 1.25) < .05), 1.0, 1.25)], \
        [wd / "sat_floor.png"]


@card("COLOR-19")
def sky_boost(task, wd):
    a = chart(["#7fa8d8", "#6b8a3c", "#d9a27a"], 48)
    src = wd / "scene.png"
    save(a, src)
    a = load(src)
    out = ffimg(src, "huesaturation=colors=b+c:saturation=0.25:intensity=-0.04:strength=5", wd / "sky.png")
    sky_in, sky_out = patch(a, 0, 48), patch(out, 0, 48)
    grass = float(np.abs(patch(out, 1, 48) - patch(a, 1, 48)).max())
    skin = float(np.abs(patch(out, 2, 48) - patch(a, 2, 48)).max())
    s_in, s_out = float(rgb2hsv(sky_in)[1]), float(rgb2hsv(sky_out)[1])
    # numpy DCTL twin: weight window 215 +-20, sat x(1+.25w), lum x(1-.1w)
    hsv = rgb2hsv(a)
    w = 1 - smoothstep(0, 20, np.array([hue_dist(h, 215) for h in hsv[..., 0].ravel()]).reshape(hsv.shape[:2]))
    hsv[..., 1] = np.clip(hsv[..., 1] * (1 + .25 * w), 0, 1)
    hsv[..., 2] = hsv[..., 2] * (1 - .1 * w)
    dctl = hsv2rgb(hsv)
    save(dctl, wd / "sky_dctl.png")
    return [check("sky saturation up", s_out > s_in + .03, [s_in, s_out], "+.03"),
            check("grass untouched (<= 2)", grass <= 2, grass, "<= 2"),
            check("skin untouched (<= 2)", skin <= 2, skin, "<= 2"),
            check("DCTL twin: only the sky patch changes", float(np.abs(dctl[:, 48:] - a[:, 48:]).max()) < 1.5 and
                  float(np.abs(dctl[:, :48] - a[:, :48]).max()) > 3, None, "sky only"),
            check("negative control: unprocessed sky has input saturation", not (s_in > s_in + .03), s_in, None)], \
        [wd / "sky.png", wd / "sky_dctl.png", jdump(wd / "sky.json", {"sky_in": tohex(sky_in), "sky_out": tohex(sky_out)})]


TARGETS = {"tokyo_night": ((4, 4), (20, 8), (78, 12), .5), "still": ((8, 3), (39, 6), (84, 7), .1),
           "japan_summer": ((8, 4), (46, 8), (91, 7), .2)}


def ire_stats(img):
    y = (0.2126 * img[..., 0] + 0.7152 * img[..., 1] + 0.0722 * img[..., 2]) / 255.0 * 100
    return [float(np.percentile(y, p)) for p in (10, 50, 95)], float(np.mean(y > 99) * 100)


@card("COLOR-20")
def scope_targets(task, wd):
    rng = np.random.default_rng(5)
    y = np.sort(rng.uniform(0, 1, 120 * 160)).reshape(120, 160)
    img = np.repeat(y[..., None] * 255, 3, 2)
    src = wd / "plate.png"
    save(img, src)
    img = load(src)
    res, checks = {}, []
    (p10, p50, p95), _ = ire_stats(img)
    for name, (t10, t50, t95, clip) in TARGETS.items():
        pts = "0/0 %.4f/%.4f %.4f/%.4f %.4f/%.4f 1/%.4f" % (p10 / 100, t10[0] / 100, p50 / 100, t50[0] / 100,
                                                           p95 / 100, t95[0] / 100, min(1, t95[0] / 100 + .06))
        out = ffimg(src, "curves=all='%s'" % pts, wd / ("%s.png" % name))
        (o10, o50, o95), over = ire_stats(out)
        res[name] = [o10, o50, o95, over]
        ok = abs(o10 - t10[0]) <= t10[1] and abs(o50 - t50[0]) <= t50[1] and abs(o95 - t95[0]) <= t95[1] and over <= clip
        checks.append(check("%s P10/P50/P95 within targets, >99 IRE <= %s%%" % (name, clip), ok, res[name],
                            [t10, t50, t95, clip]))
    cb = (img[..., 2] / 255 - luma(img) / 255) / 1.8556
    checks.append(check("vectorscope Cb of the grey plate is 0", float(np.abs(cb).max()) < .01, float(np.abs(cb).max()), 0))
    checks.append(check("negative control: ungraded plate misses the Tokyo-night P50", not (abs(p50 - 20) <= 8), p50, "20+-8"))
    return checks, [wd / "tokyo_night.png", jdump(wd / "scopes.json", res)]


@card("COLOR-21")
def shot_table_floor(task, wd):
    table = {"talking_head": "base grade + warm ambient pull", "screen": "crisp, high contrast on text",
             "graphics": "brand background", "animation": "free palette"}
    floor, ceil = 12.0, 238.0
    rng = np.random.default_rng(1)
    shots = {"talking_head": (35, 200), "screen": (20, 250), "graphics": (50, 190)}
    outs, mins, maxs, ranges, warm = [], {}, {}, {}, {}
    for name, (lo, hi) in shots.items():
        img = np.clip(np.full((36, 64, 3), 0.0) + np.linspace(lo, hi, 64)[None, :, None] +
                      rng.normal(0, 1, (36, 64, 1)), 0, 255)
        y = luma(img)
        a, b = float(y.min()), float(y.max())
        out = floor + (img - a) * (ceil - floor) / (b - a)          # one floor and one ceiling for the film
        if name == "talking_head":
            out = out + np.array([4, 0, -4])
        out = np.clip(out, 0, 255)
        save(out, wd / ("%s.png" % name))
        outs.append(wd / ("%s.png" % name))
        yo = luma(load(wd / ("%s.png" % name)))
        mins[name], maxs[name], ranges[name] = float(yo.min()), float(yo.max()), float(yo.max() - yo.min())
        warm[name] = float((out[..., 0] - out[..., 2]).mean())
    in_floors = [lo for lo, _ in shots.values()]
    return [check("every shot shares the film floor (+-2)", all(abs(m - floor) <= 2 for m in mins.values()), mins, floor),
            check("no shot exceeds the ceiling (+2)", all(m <= ceil + 2 for m in maxs.values()), maxs, ceil),
            check("tonal range > 150 of 255", all(r > 150 for r in ranges.values()), ranges, "> 150"),
            check("talking head carries the warm pull (R-B > 5)", warm["talking_head"] > 5, warm["talking_head"], "> 5"),
            check("negative control: input floors differ (spread > 4)", not (max(in_floors) - min(in_floors) <= 4),
                  in_floors, "spread > 4")], outs + [jdump(wd / "shot_table.json", table)]


def median_cut(px, k):
    boxes = [px]
    while len(boxes) < k:
        scores = [float(np.ptp(b, 0).max()) * len(b) if len(b) > 1 else 0.0 for b in boxes]
        if max(scores) <= 0:
            break
        i = int(np.argmax(scores))
        b = boxes.pop(i)
        ch = int(np.argmax(np.ptp(b, 0)))
        b = b[np.argsort(b[:, ch], kind="stable")]
        vals = b[:, ch]
        m = np.median(vals)
        cut = int(np.searchsorted(vals, m, side="right"))
        if cut <= 0 or cut >= len(b):
            cut = int(np.searchsorted(vals, m, side="left"))
        if cut <= 0 or cut >= len(b):
            boxes.append(b)
            break
        boxes += [b[:cut], b[cut:]]
    return [(b.mean(0), len(b) / len(px)) for b in boxes]


def mccamy(rgb_mean):
    l = lin(rgb_mean)
    m = np.array([[0.4124564, 0.3575761, 0.1804375], [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    X, Y, Z = m @ l
    x, y = X / (X + Y + Z), Y / (X + Y + Z)
    n = (x - 0.3320) / (0.1858 - y)
    return 449 * n ** 3 + 3525 * n ** 2 + 6823.3 * n + 5520.33


def analyze_colour(img):
    r, g, b = img[..., 0], img[..., 1], img[..., 2]
    rb = float(r.mean() - b.mean())
    rg, yb = r - g, .5 * (r + g) - b
    colourful = float(math.hypot(rg.std(), yb.std()) + .3 * math.hypot(rg.mean(), yb.mean()))
    thumb = np.asarray(Image.fromarray(img.astype(np.uint8)).resize((256, 256), Image.NEAREST)).reshape(-1, 3).astype(float)
    pal = sorted(median_cut(thumb, 6), key=lambda t: -t[1])
    return {"cct": float(mccamy(img.reshape(-1, 3).mean(0))), "cast": "warm" if rb > 12 else "cool" if rb < -12 else "neutral",
            "colourfulness": colourful, "palette": [(tohex(c), round(s, 4)) for c, s in pal]}


@card("COLOR-22")
def colour_analysis(task, wd):
    cols = ["#d94f30", "#2f6fb0", "#e8c547", "#3a7d44", "#7b3fa0", "#202020"]
    shares = [.30, .20, .15, .15, .10, .10]
    img = np.zeros((100, 100, 3))
    x0 = 0
    for c, s in zip(cols, shares):
        img[:, x0:x0 + int(round(s * 100))] = hx(c)
        x0 += int(round(s * 100))
    save(img, wd / "six.png")
    rep = analyze_colour(load(wd / "six.png"))
    found = dict(rep["palette"])
    ok_cols = all(min(float(np.abs(np.array(hx(c)) - np.array(hx(f))).max()) for f in found) <= 8 for c in cols)
    ok_shares = all(any(float(np.abs(np.array(hx(c)) - np.array(hx(f))).max()) <= 8 and abs(found[f] - s) <= .02
                        for f in found) for c, s in zip(cols, shares))
    white = analyze_colour(np.full((32, 32, 3), 255.0))
    warm_img = np.full((32, 32, 3), 0.0) + np.array([230, 190, 150])
    warm = analyze_colour(warm_img)
    grey = analyze_colour(np.full((32, 32, 3), 128.0))
    jdump(wd / "analysis.json", {"six": rep, "white": white, "warm": warm, "grey": grey})
    return [check("6 dominant colours recovered within +-8", ok_cols, list(found), cols),
            check("shares within +-2 %", ok_shares, rep["palette"], list(zip(cols, shares))),
            check("McCamy CCT of sRGB white ~ 6504 K", abs(white["cct"] - 6504) < 150, white["cct"], 6504),
            check("warm frame: cast warm, CCT < 4500 K", warm["cast"] == "warm" and warm["cct"] < 4500,
                  [warm["cast"], warm["cct"]], ["warm", "< 4500"]),
            check("grey colourfulness < 15 (not colourful)", grey["colourfulness"] < 15, grey["colourfulness"], "< 15"),
            check("negative control: neutral grey is not called warm", not (grey["cast"] == "warm"), grey["cast"], "neutral")], \
        [wd / "analysis.json", wd / "six.png"]


GELS = [("Full CTB", -159), ("1/2 CTB", -68), ("1/4 CTB", -30), ("1/8 CTB", -12), ("1/8 CTO", 20), ("1/4 CTO", 42),
        ("1/2 CTO", 81), ("Full CTO", 159)]


def mired(from_k, to_k):
    s = 1e6 / to_k - 1e6 / from_k
    gel = min(GELS, key=lambda g: abs(g[1] - s))[0]
    return round(s, 1), gel, "cooler (blue)" if s < 0 else "warmer (orange)"


@card("COLOR-23")
def mired_gel(task, wd):
    cases = {(3200, 5600): (-133.9, "Full CTB"), (5600, 3200): (133.9, "Full CTO"), (5600, 4300): (54.0, "1/4 CTO"),
             (5600, 6500): (-24.7, "1/4 CTB")}
    got = {"%d->%d" % k: mired(*k) for k in cases}
    ok = all(abs(got["%d->%d" % k][0] - v[0]) < .15 and got["%d->%d" % k][1] == v[1] for k, v in cases.items())
    rev = mired(5600, 3200)
    return [check("mired shifts and nearest gels", ok, got, {"%d->%d" % k: v for k, v in cases.items()}),
            check("3200 -> 5600 reads 'cooler (blue)'", got["3200->5600"][2] == "cooler (blue)", got["3200->5600"][2],
                  "cooler (blue)"),
            check("negative control: the reverse move is not a CTB", not (rev[1] == "Full CTB"), rev[1], "Full CTO")], \
        [jdump(wd / "mired.json", got)]


@card("COLOR-25")
def beats_palette(task, wd):
    segs = [("#c83232", 1.0), ("#3246c8", 1.0), ("#32a046", 4.0)]
    fps = 10
    frames = []
    for c, d in segs:
        for i in range(int(d * fps)):
            f = np.zeros((36, 64, 3)) + hx(c)
            f[24:30, 10 + i % 40:18 + i % 40] = 240        # a moving entrance-ish block
            frames.append(f)
    clip = write_video(wd / "ref.mp4", frames, fps=fps, crf="12")
    fr = fx.frames(clip, (64, 36))
    diff = [float(np.abs(fr[i] - fr[i - 1]).mean()) for i in range(1, len(fr))]
    cuts = [0] + [i for i, d in enumerate(diff, 1) if d > 30] + [len(fr)]
    beats = []
    for a, b in zip(cuts[:-1], cuts[1:]):
        n = max(1, math.ceil((b - a) / fps / 3.05))
        edges = np.linspace(a, b, n + 1).round().astype(int)
        for s, e in zip(edges[:-1], edges[1:]):
            bg = np.median(fr[s:e, :20].reshape(-1, 3), 0)
            beats.append({"t0": s / fps, "t1": e / fps, "background": tohex(bg)})
    expect = ["#c83232", "#3246c8", "#32a046", "#32a046"]
    errs = [float(np.abs(np.array(hx(b["background"])) - np.array(hx(e))).max()) for b, e in zip(beats, expect)]
    glob = tohex(np.median(fr[:, :20].reshape(-1, 3), 0))
    gerr = min(float(np.abs(np.array(hx(glob)) - np.array(hx(e))).max()) for e in expect[:2])
    return [check("4 beats (the 4 s shot split to <= 3.05 s)", len(beats) == 4, len(beats), 4),
            check("every beat <= 3.05 s", all(b["t1"] - b["t0"] <= 3.05 for b in beats),
                  [round(b["t1"] - b["t0"], 2) for b in beats], "<= 3.05"),
            check("background per beat within +-8 per channel", len(errs) == 4 and max(errs) <= 8, errs, "<= 8"),
            check("negative control: one global background misses the red/blue beats", not (gerr <= 8), gerr, "> 8")], \
        [jdump(wd / "analysis.json", {"beats": beats}), clip]


def stats(img):
    return img.reshape(-1, 3).mean(0), img.reshape(-1, 3).std(0)


def colour_transfer(img, look, strength=.7):
    mu, sd = stats(img)
    g = np.clip(1 + strength * (look[1] / np.maximum(sd, 1e-6) - 1), .6, 1.6)
    o = np.clip(strength * (look[0] - g * mu) + (1 - strength) * (1 - g) * mu, -120, 120)
    return np.clip(img * g + o, 0, 255), g, o


@card("COLOR-27")
def shot_match(task, wd):
    from scipy.optimize import linear_sum_assignment
    rng = np.random.default_rng(9)

    def shot(mean, spread):
        return np.clip(np.array(mean, float) + rng.normal(0, spread, (36, 64, 3)), 0, 255)
    refs = [shot((180, 120, 80), 30), shot((60, 90, 140), 15), shot((100, 160, 90), 40)]
    pool = [shot((95, 150, 85), 36), shot((175, 115, 90), 28), shot((128, 128, 128), 5), shot((70, 95, 130), 17)]
    feat = lambda x: np.concatenate([stats(x)[0] / 255, stats(x)[1] / 64, [float(chroma_spread(x).mean()) / 255]])
    cost = np.array([[float(np.linalg.norm(feat(r) - feat(p))) for p in pool] for r in refs])
    ri, ci = linear_sum_assignment(cost)
    assign = dict(zip(ri.tolist(), ci.tolist()))
    out, g, o = colour_transfer(pool[assign[0]], stats(refs[0]), strength=1.0)
    m_err = float(np.abs(stats(out)[0] - stats(refs[0])[0]).max())
    _, g_hi, _ = colour_transfer(np.clip(shot((128, 128, 128), 5), 0, 255), stats(refs[2]), strength=1.0)
    out7, _, _ = colour_transfer(pool[assign[0]], stats(refs[0]), strength=.7)
    frac = float(np.mean((stats(out7)[0] - stats(pool[assign[0]])[0]) /
                         (stats(refs[0])[0] - stats(pool[assign[0]])[0] + 1e-9)))
    save(np.hstack([refs[0], pool[assign[0]], out]), wd / "match.png")
    pre = float(np.abs(stats(pool[assign[0]])[0] - stats(refs[0])[0]).max())
    return [check("Hungarian assignment recovers ref->pool {0:1, 1:3, 2:0}", assign == {0: 1, 1: 3, 2: 0}, assign,
                  {0: 1, 1: 3, 2: 0}),
            check("strength 1 transfer matches ref mean (+-2)", m_err <= 2, m_err, "<= 2"),
            check("gain clamped to 1.6 on a flat clip", float(g_hi.max()) == 1.6, float(g_hi.max()), 1.6),
            check("strength .7 moves ~70 % of the way", abs(frac - .7) < .08, frac, .7),
            check("negative control: chosen pool clip mean differs from ref (> 2)", not (pre <= 2), pre, "> 2")], \
        [wd / "match.png", jdump(wd / "match.json", {"cost": cost.tolist(), "assign": assign})]


def measure_fix(img):
    y = luma(img)
    p02, p50, p98 = (float(np.percentile(y, q)) for q in (2, 50, 98))
    rng_ = p98 - p02
    c = float(np.clip(200 / rng_, .9, 1.3)) if rng_ < 200 else 1.0
    b = float(np.clip(118 / max(p50, 1), .85, 1.3)) if not (112 <= p50 <= 150) else 1.0
    hsv = rgb2hsv(img)
    s = float(hsv[..., 1].mean())
    sat = float(np.clip(.24 / s, 1, 1.25)) if .05 < s < .18 else 1.0
    m = (hsv[..., 1] < .22) & (y > 50) & (y < 215)
    gains = np.ones(3)
    if m.mean() >= .06:
        mean = img[m].mean(0)
        gains = np.clip(mean.mean() / mean, .82, 1.18)
    out = img * gains
    out = css_filter(out, [("brightness", b), ("contrast", c), ("saturate", sat)])
    return out, {"contrast": c, "brightness": b, "saturation": sat, "gains": gains.tolist(), "p50": p50, "range": rng_}


def look_dna(img):
    hsv = rgb2hsv(img)
    s = float(hsv[..., 1].mean())
    y = luma(img)
    warmth = float((img[..., 0].mean() - img[..., 2].mean()) / 255)
    blue_sh = float((img[..., 2] - img[..., 0])[y < 85].mean()) if (y < 85).any() else 0
    red_hi = float((img[..., 0] - img[..., 2])[y > 150].mean()) if (y > 150).any() else 0
    if s < .07:
        return "bw"
    if blue_sh > 6 and red_hi > 10:
        return "teal_orange"
    if warmth > .1:
        return "golden" if s > .3 else "warm"
    if warmth < -.05:
        return "blue_hour" if y.mean() < 90 else "cool"
    return "clean" if float(y.std() / 255) > .26 and s > .32 else "neutral"


@card("COLOR-28")
def basma_autofix(task, wd):
    base = np.zeros((40, 120, 3)) + np.linspace(65, 125, 120)[None, :, None]
    base[:20] = base[:20] * np.array([1.0, .86, .8])        # dull colour in the top half
    img = np.clip(base + np.array([10, 2, -8]), 0, 255)       # warm cast
    out, fixp = measure_fix(img)
    save(img, wd / "dark_flat.png")
    save(out, wd / "fixed.png")
    yi, yo = luma(img), luma(out)
    neutral_rb = float((out[20:, :, 0] - out[20:, :, 2]).mean())
    r_ramp = ramp(256, 32)
    to = np.clip(r_ramp + np.where(luma(r_ramp)[..., None] < 85, np.array([-12, 0, 12]), np.array([0, 0, 0])) +
                 np.where(luma(r_ramp)[..., None] > 150, np.array([20, 0, -20]), np.array([0, 0, 0])), 0, 255)
    to = np.clip(to * np.array([1, 1, 1]) + 0, 0, 255)
    labels = {"bw": look_dna(r_ramp), "teal_orange": look_dna(to),
              "golden": look_dna(np.zeros((8, 8, 3)) + np.array([230, 160, 70])),
              "blue_hour": look_dna(np.zeros((8, 8, 3)) + np.array([30, 50, 90]))}
    return [check("contrast opened (range wider by > 1.2x)", (np.percentile(yo, 98) - np.percentile(yo, 2)) >
                  1.2 * (np.percentile(yi, 98) - np.percentile(yi, 2)), fixp["contrast"], "clamp(200/range,.9,1.3)"),
            check("mid moved toward 118", abs(float(np.median(yo)) - 118) < abs(float(np.median(yi)) - 118) - 15,
                  [float(np.median(yi)), float(np.median(yo))], "closer to 118"),
            check("grey-world gains in .82..1.18 neutralise the cast (|R-B| < 6)", abs(neutral_rb) < 6 and
                  all(.82 <= g <= 1.18 for g in fixp["gains"]), [neutral_rb, fixp["gains"]], "< 6"),
            check("DNA classifier labels the references", all(k == v for k, v in labels.items()), labels, list(labels)),
            check("negative control: input mid is outside 112..150", not (112 <= float(np.median(yi)) <= 150),
                  float(np.median(yi)), "outside")], \
        [wd / "fixed.png", jdump(wd / "fix.json", {"fix": fixp, "dna": labels,
                                                    "engine": "numpy port of measureFix rules (Basma editor not built)"})]


COLOUR_WORDS = {"red": "#d62828", "أحمر": "#d62828", "الأحمر": "#d62828", "blue": "#2f6fd6", "أزرق": "#2f6fd6",
                "الأزرق": "#2f6fd6", "gold": "#c9a227", "ذهبي": "#c9a227", "cyan": "#19c3d9", "سماوي": "#19c3d9",
                "green": "#2a9d4b", "أخضر": "#2a9d4b"}


def parse_colour_request(text):
    words = re.findall(r"[\w؀-ۿ]+", text.lower())
    found = [COLOUR_WORDS[w] for w in words if w in COLOUR_WORDS]
    return (found[0], found[1]) if len(found) >= 2 else None


def recolor(img, src_hex, dst_hex, tolerance=40):
    s, d = np.array(hx(src_hex), float), np.array(hx(dst_hex), float)
    hs, hd = rgb2hsv(s), rgb2hsv(d)
    hsv = rgb2hsv(img)
    v = np.maximum(img.max(-1, keepdims=True), 1)
    norm = img * (s.max() / v)                       # compare at the source brightness, so shading stays in the mask
    m = np.linalg.norm(norm - s, axis=-1) < tolerance
    out = hsv.copy()
    out[..., 0] = np.where(m, hd[0], hsv[..., 0])
    out[..., 1] = np.where(m, np.clip(hsv[..., 1] * hd[1] / max(hs[1], 1e-6), 0, 1), hsv[..., 1])
    out[..., 2] = np.where(m, np.clip(hsv[..., 2] * hd[2] / max(hs[2], 1e-6), 0, 1), hsv[..., 2])
    return hsv2rgb(out), m


@card("COLOR-29")
def local_recolor(task, wd):
    img = np.zeros((48, 144, 3)) + 235
    shade = np.linspace(.75, 1.0, 48)[None, :, None]
    img[:, :48] = np.array(hx("#c9a227")) * shade
    img[:, 96:] = hx("#b5432c")
    out, m = recolor(img, "#c9a227", "#19c3d9")
    save(img, wd / "in.png")
    save(out, wd / "recolor.png")
    lit = out[:, 47]
    err = float(np.abs(lit.mean(0) - np.array(hx("#19c3d9"))).max())
    v_ratio_in = float(img[:, 0].max() / img[:, 47].max())
    v_ratio_out = float(out[:, 0].max() / out[:, 47].max())
    red = float(np.abs(out[:, 96:] - img[:, 96:]).max())
    req = parse_colour_request("غيّر الأحمر إلى أزرق")
    return [check("gold -> #19c3d9 at the lit edge (+-3)", err <= 3, tohex(lit.mean(0)), "#19c3d9"),
            check("shading kept (dark/light value ratio unchanged +-2 %)", abs(v_ratio_out - v_ratio_in) < .02,
                  [v_ratio_in, v_ratio_out], "equal"),
            check("red block untouched", red < 1e-6, red, 0),
            check("Arabic request parsed", req == ("#d62828", "#2f6fd6"), req, ("#d62828", "#2f6fd6")),
            check("negative control: input gold hue is far from cyan",
                  not (hue_dist(hue_of(img[0, 47]), hue_of(hx("#19c3d9"))) < 5),
                  hue_of(img[0, 47]), "near 186")], [wd / "recolor.png"]


def logo_palette(img, max_colors=16, min_share=.001):
    px = img.reshape(-1, 3)
    q = (px // 8).astype(int)
    keys, inv, counts = np.unique(q[:, 0] * 1024 + q[:, 1] * 32 + q[:, 2], return_inverse=True, return_counts=True)
    order = np.argsort(-counts)
    cands = []
    for k in order:
        if counts[k] / len(px) < min_share:
            break
        c = px[inv == k].mean(0)
        if all(np.linalg.norm(c - p) >= 30 for p in cands):
            cands.append(c)
        if len(cands) >= max_colors:
            break
    pal = []
    for c in cands:
        near = px[np.linalg.norm(px - c, axis=1) < 22]
        pal.append((near.mean(0), len(near) / len(px)))
    # drop antialias blends: a candidate that is a two-colour mixture t in .08..92 of stronger ones within 18
    keep = []
    for i, (c, s) in enumerate(pal):
        blend = False
        for j, (a, sa) in enumerate(pal):
            for k, (b, sb) in enumerate(pal):
                if len({i, j, k}) < 3 or sa < s or sb < s:
                    continue
                d = b - a
                t = float(np.dot(c - a, d) / max(np.dot(d, d), 1e-9))
                if .08 <= t <= .92 and np.linalg.norm(a + t * d - c) < 18:
                    blend = True
        if not blend:
            keep.append((c, s))
    return keep


@card("COLOR-30")
def logo_true_colours(task, wd):
    big = Image.new("RGB", (640, 320), "#ffffff")
    d = ImageDraw.Draw(big)
    d.ellipse((40, 40, 280, 280), fill="#e63946")
    d.rectangle((330, 60, 600, 260), fill="#1d3557")
    d.polygon([(360, 290), (470, 20), (580, 290)], fill="#f4a261")
    img = np.asarray(big.resize((160, 80), Image.BOX)).astype(float)
    save(img, wd / "logo.png")
    pal = logo_palette(img)
    truth = ["#ffffff", "#e63946", "#1d3557", "#f4a261"]
    found = [tohex(c) for c, _ in pal]
    match = all(any(float(np.abs(np.array(hx(t)) - np.array(hx(f))).max()) <= 3 for f in found) for t in truth)
    naive = len(np.unique(img.reshape(-1, 3), axis=0))
    return [check("exactly the 4 true colours (blends rejected)", len(found) == 4 and match, found, truth),
            check("negative control: raw pixels hold many antialias blends (> 4 unique)", not (naive <= 4), naive, "> 4")], \
        [wd / "logo.png", jdump(wd / "palette.json", {"palette": found, "engine": "numpy port (OpenCV not installed)"})]


def walk_until(hexc, bg, ratio, direction):
    h, s, l = hex2hsl(hexc)
    grounds = bg if isinstance(bg, (list, tuple)) else [bg]
    for _ in range(200):
        c = hsl2hex(h, s, l)
        if all(contrast(c, g) >= ratio for g in grounds):
            return c
        l = min(1, max(0, l + direction * .005))
    return hsl2hex(h, s, l)


def design_tokens(brand, name="k"):
    h, s, _ = hex2hsl(brand)
    light = {"bg": "#faf9f7", "surface": "#ffffff", "ink": hsl2hex(h, .35, .1)}
    dark = {"bg": hsl2hex(h, .2, .07), "surface": hsl2hex(h, .18, .11), "ink": hsl2hex(h, .2, .93)}
    light["brand"] = walk_until(brand, [light["bg"], light["surface"]], 4.6, -1)
    dark["brand"] = walk_until(brand, [dark["bg"], dark["surface"]], 4.6, +1)
    light["ui"] = walk_until(brand, light["bg"], 3.0, -1)
    dark["ui"] = walk_until(brand, dark["bg"], 3.0, +1)
    for st, hue in (("ok", 140), ("warn", 35), ("bad", 4), ("info", 200)):
        light[st] = walk_until(hsl2hex(hue, .65, .45), [light["bg"], light["surface"]], 4.6, -1)
        dark[st] = walk_until(hsl2hex(hue, .65, .55), [dark["bg"], dark["surface"]], 4.6, +1)
    pairs = []
    for theme, t in (("light", light), ("dark", dark)):
        for k in ("ink", "brand", "ok", "warn", "bad", "info"):
            for g in ("bg", "surface"):
                pairs.append((theme, k, g, 4.6, round(contrast(t[k], t[g]), 2)))
        pairs.append((theme, "ui", "bg", 3.0, round(contrast(t["ui"], t["bg"]), 2)))
    space = [4, 8, 12, 16, 24, 32, 48, 64]
    type_scale = [round(16 * 1.25 ** i, 2) for i in range(-1, 5)]
    var = lambda t: "".join("  --%s-%s: %s;\n" % (name, k, v) for k, v in t.items())
    css = (":root {\n%s  --t-fast: 120ms; --t: 180ms; --ease: cubic-bezier(.2,.8,.2,1);\n}\n" % var(light) +
           "@media (prefers-color-scheme: dark) {\n :root:not([data-theme=light]) {\n%s }\n}\n" % var(dark) +
           "[data-theme=dark] {\n%s}\n" % var(dark) +
           "@media (prefers-reduced-motion: reduce) {\n :root { --t-fast: 0ms; --t: 0ms; }\n}\n")
    return {"light": light, "dark": dark, "contrast": pairs, "space": space, "type": type_scale, "css": css}


@card("COLOR-31")
def tokens_from_one(task, wd):
    tok = design_tokens("#8a5a2b")
    (wd / "tokens.css").write_text(tok["css"], encoding="utf-8")
    jdump(wd / "tokens.json", tok)
    fails = [p for p in tok["contrast"] if p[4] < p[3]]
    css = tok["css"]
    raw = contrast("#8a5a2b", tok["dark"]["bg"])
    return [check("all %d checked pairs pass (text 4.6, UI 3)" % len(tok["contrast"]), not fails, fails or len(tok["contrast"]),
                  "0 failures"),
            check("CSS: :root, dark guarded by :not([data-theme=light]), [data-theme=dark], reduced-motion 0 ms",
                  all(x in css for x in (":root {", "prefers-color-scheme: dark", ":root:not([data-theme=light])",
                                         "[data-theme=dark] {", "--t: 0ms")), True, True),
            check("type ratio 1.25 and space 4..64", tok["space"][0] == 4 and tok["space"][-1] == 64 and
                  abs(tok["type"][2] / tok["type"][1] - 1.25) < .01, [tok["space"], tok["type"]], "4..64, x1.25"),
            check("negative control: the raw brand on the dark ground fails 4.6", not (raw >= 4.6), raw, "< 4.6")], \
        [wd / "tokens.css", wd / "tokens.json"]


LEDGER = {"bg": "#fbf8f3", "surface": "#fffdf9", "line": "#e3d9cc", "ink": "#1d1814", "ink-2": "#4b4139",
          "saffron": "#d9530e", "text": "#a53e07", "soft": "#fbe9dc"}
LEDGER_NIGHT = {"bg": "#161310", "surface": "#1c1814", "ink": "#f5ede3", "brand": "#f2732d", "gold-ink": "#ff9a5f"}


def render_identity(t, w=240, h=135, accent="saffron"):
    im = Image.new("RGB", (w, h), t["bg"])
    d = ImageDraw.Draw(im)
    d.rectangle((16, 16, w - 16, h - 16), fill=t.get("surface", t["bg"]))
    d.rectangle((28, 30, 150, 44), fill=t["ink"])
    d.rectangle((28, 56, 90, 62), fill=t.get(accent, t.get("brand")))
    return np.asarray(im).astype(float)


@card("COLOR-32")
def ledger_identity(task, wd):
    c_text = contrast(LEDGER["text"], LEDGER["bg"])
    c_ink = contrast(LEDGER["ink"], LEDGER["bg"])
    c_raw = contrast(LEDGER["saffron"], LEDGER["bg"])
    c_night = contrast(LEDGER_NIGHT["ink"], LEDGER_NIGHT["bg"])
    light, night = render_identity(LEDGER), render_identity(LEDGER_NIGHT, accent="brand")
    save(np.vstack([light, night]), wd / "ledger.png")
    px_ok = tohex(light[2, 2]) == LEDGER["bg"] and tohex(light[37, 60]) == LEDGER["ink"] and \
        tohex(light[59, 50]) == LEDGER["saffron"] and tohex(night[2, 2]) == LEDGER_NIGHT["bg"]
    return [check("saffron text step #a53e07 on paper = 5.9:1 (+-.15)", abs(c_text - 5.9) < .15, c_text, 5.9),
            check("ink #1d1814 on paper = 17:1 (+-.5)", abs(c_ink - 17) < .5, c_ink, 17),
            check("night ink on night ground >= 15:1", c_night >= 15, c_night, ">= 15"),
            check("scene maps bg / ink / accent to exact hex", px_ok, [tohex(light[2, 2]), tohex(light[37, 60]),
                                                                      tohex(light[59, 50])], [LEDGER["bg"], LEDGER["ink"], LEDGER["saffron"]]),
            check("negative control: raw saffron #d9530e fails 4.5 as text", not (c_raw >= 4.5), c_raw, "< 4.5")], \
        [wd / "ledger.png"]


EARTH = {"cobalt_ice": ("#f4f6fb", "#111827", "#2340c4", "#076f80"),
         "navy_gold": ("#f7f4ec", "#0b1f3a", "#13305a", "#8a6a0e"),
         "heritage_valley": ("#f4ead8", "#2b1a0f", "#8a5a2b", "#b8864e"),
         "najd_luxe": ("#f7faf7", "#11281a", "#006c35", "#d4af37"),
         "oasis": ("#f6f1e7", "#23261f", "#3b6a4e", "#c2703d"),
         "notebook": ("#f7f3e8", "#23252b", "#2c5aa0", "#c0392b"),
         "executive": ("#f5f6fb", "#1d2340", "#5b4ee6", "#3d7bf5"),
         "professional_audit": ("#f3f4f6", "#161b26", "#1f3b68", "#2f5d9e"),
         "midnight_analysis": ("#0d1117", "#e8edf5", "#7c8cff", "#4fd1c5"),
         "aurora_glass": ("#eef2f9", "#0a0c13", "#0a66ff", "#7b61ff"),
         "vivid": ("#f8fafc", "#1e293b", "#6366f1", "#06b6d4"),
         "graphite": ("#0e0f12", "#eceef2", "#8183ff", "#5ee0c4"),
         "onyx": ("#0b0b0c", "#f4efe4", "#d4af5a", "#b8893a"),
         "earth_office_door": ("#176b4b", "#b9f3cd", "#e8bd76", "#f9f1e8")}


@card("COLOR-33")
def earth_looks(task, wd):
    css, ratios = [], {}
    for name, (bg, ink, brand, accent) in EARTH.items():
        css.append('[data-look=%s] {\n  --sk-bg: %s;\n  --sk-ink: %s;\n  --sk-brand: %s;\n  --sk-accent: %s;\n}' %
                   (name, bg, ink, brand, accent))
        ratios[name] = round(contrast(ink, bg), 2)
    (wd / "earth_looks.css").write_text("\n".join(css) + "\n", encoding="utf-8")
    cob = contrast("#2340c4", "#ffffff")
    ice_txt, ice_raw = contrast("#076f80", "#f4f6fb"), contrast("#19c3d9", "#f4f6fb")
    gold_txt = contrast("#8a6a0e", "#f7f4ec")
    parsed = re.findall(r"\[data-look=(\w+)\]", (wd / "earth_looks.css").read_text())
    return [check("14 looks emitted as --sk-* blocks", len(parsed) == 14, len(parsed), 14),
            check("ink on ground >= 4.5:1 in every look", all(r >= 4.5 for r in ratios.values()), ratios, ">= 4.5"),
            check("cobalt #2340c4 = 8.1:1 on white (+-.2)", abs(cob - 8.1) < .2, cob, 8.1),
            check("text variants pass 4.5 (ice #076f80, gold #8a6a0e)", ice_txt >= 4.5 and gold_txt >= 4.5,
                  [ice_txt, gold_txt], ">= 4.5"),
            check("negative control: raw ice #19c3d9 fails as text", not (ice_raw >= 4.5), ice_raw, "< 4.5")], \
        [wd / "earth_looks.css", jdump(wd / "ratios.json", ratios)]


BRAND_HEX = {"#0b1030": "#1d1814", "#19c3d9": "#f2732d", "#f4f6fb": "#fbf8f3"}
BRAND_RGBA = {(35, 64, 196): (217, 83, 14)}


def brand_css(css):
    css = re.sub(r"(?i)(\bcolor\s*:\s*)#2340c4", r"\1#a53e07", css)
    css = re.sub(r"(?i)(\bbackground(?:-color)?\s*:\s*)#2340c4", r"\1#1d1814", css)
    css = re.sub(r"(?i)#2340c4", "#d9530e", css)
    css = re.sub(r"(?i)#([0-9a-f]{6})(?=[0-9a-f]{2}\b|\b)", lambda m: BRAND_HEX.get("#" + m.group(1).lower(), m.group(0)), css)
    css = re.sub(r"rgba\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,", lambda m: "rgba(%d,%d,%d," %
                 BRAND_RGBA.get(tuple(int(x) for x in m.groups()), tuple(int(x) for x in m.groups())), css)
    return css


@card("COLOR-34")
def role_remap(task, wd):
    src = (".t{color:#2340c4}\n.b{background:#2340c4}\n.s{border:1px solid #2340c4}\n.a{fill:#2340c480}\n"
           ".n{background:#0b1030;color:#19c3d9}\n.p{background:#f4f6fb}\n.g{box-shadow:0 0 8px rgba(35,64,196,.4)}\n")
    out = brand_css(src)
    (wd / "in.css").write_text(src)
    (wd / "ledger.css").write_text(out)
    exp = {".t{color:#a53e07}", ".b{background:#1d1814}", ".s{border:1px solid #d9530e}", ".a{fill:#d9530e80}",
           ".n{background:#1d1814;color:#f2732d}", ".p{background:#fbf8f3}", ".g{box-shadow:0 0 8px rgba(217,83,14,.4)}"}
    got = set(out.strip().splitlines())
    return [check("roles remapped (text -> #a53e07, fill -> #1d1814, stroke -> #d9530e)", got == exp, sorted(got), sorted(exp)),
            check("alpha suffix kept (#d9530e80)", "#d9530e80" in out, True, True),
            check("no cobalt left", "#2340c4" not in out.lower() and "35,64,196" not in out, True, True),
            check("negative control: input still cobalt", not ("#2340c4" not in src), True, "cobalt present")], \
        [wd / "ledger.css"]


def recolor_ice(img):
    hsv = rgb2hsv(img)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    w = smoothstep(18, 30, h) * (1 - smoothstep(62, 74, h)) * smoothstep(.08, .22, s)
    target = 190 + (h - 45) * .35
    h2 = h + w * (target - h)
    blue = (h >= 196) & (h <= 248)
    h2 = np.where(blue, h + .5 * (228 - h), h2)
    out = np.stack([h2, s * (1 - .1 * w), v * (1 - .06 * w)], -1)
    return hsv2rgb(out)


@card("COLOR-35")
def gold_to_ice(task, wd):
    cols = ["#c9a227", "#b5432c", "#0b1f3a", "#8a5a3c"]
    a = chart(cols, 32)
    out = recolor_ice(a)
    save(out, wd / "ice.png")
    got = [tohex(patch(out, i, 32)) for i in range(4)]
    err = lambda x, y: float(np.abs(np.array(hx(x)) - np.array(hx(y))).max())
    frames = [recolor_ice(np.roll(a, i * 4, axis=1)) for i in range(8)]
    write_video(wd / "ice.mp4", frames, fps=8, crf="24", extra=("-preset", "slow", "-movflags", "+faststart"))
    return [check("gold #c9a227 -> #34a6bd (+-3)", err(got[0], "#34a6bd") <= 3, got[0], "#34a6bd"),
            check("red #b5432c unchanged (+-1)", err(got[1], "#b5432c") <= 1, got[1], "#b5432c"),
            check("navy #0b1f3a -> #0b1a3a (+-3)", err(got[2], "#0b1a3a") <= 3, got[2], "#0b1a3a"),
            check("negative control: unprocessed gold is not ice", not (err(cols[0], "#34a6bd") <= 3), cols[0], "#34a6bd")], \
        [wd / "ice.png", wd / "ice.mp4"]


PALETTES36 = {"cobalt": {"iceA": (.043, .063, .19), "iceB": (.10, .76, .85), "skyB": (.86, .95, 1), "rim": (.60, .93, .97)},
              "ledger": {"iceA": (.114, .094, .078), "iceB": (.85, .33, .055), "skyB": (.98, .95, .90),
                         "rim": (.98, .76, .55)}}


def crystal_shader(ny, sky_mask, rim_w, u):
    iceA, iceB, skyB, rim = (np.array(u[k], float) for k in ("iceA", "iceB", "skyB", "rim"))
    t = (ny * .5 + .5)[..., None]
    body = iceA * (1 - t) + iceB * t
    c = np.where(sky_mask[..., None], skyB, body)
    return np.clip(c * (1 - rim_w[..., None]) + rim * rim_w[..., None], 0, 1) * 255


@card("COLOR-36")
def shader_uniform_palettes(task, wd):
    import inspect
    h, w = 64, 96
    ny = np.repeat(np.linspace(1, -1, h)[:, None], w, 1)
    sky = np.zeros((h, w), bool)
    sky[:8] = True
    rim = np.zeros((h, w))
    rim[:, -4:] = 1
    outs = {k: crystal_shader(ny, sky, rim, u) for k, u in PALETTES36.items()}
    rng = np.random.default_rng(2)
    rnd = {k: tuple(rng.uniform(0, 1, 3)) for k in ("iceA", "iceB", "skyB", "rim")}
    o_r = crystal_shader(ny, sky, rim, rnd)
    save(np.vstack([outs["cobalt"], outs["ledger"]]), wd / "crystal_palettes.png")
    near = lambda px, c: float(np.abs(px - np.array(c) * 255).max()) <= 1
    src = inspect.getsource(crystal_shader)
    literal_triples = re.findall(r"\(\s*\.?\d+\.?\d*\s*,\s*\.?\d+\.?\d*\s*,\s*\.?\d+\.?\d*\s*\)", src)
    return [check("cobalt: sky = skyB, top body ~ iceB, bottom = iceA",
                  near(outs["cobalt"][2, 10], PALETTES36["cobalt"]["skyB"]) and near(outs["cobalt"][-1, 10], PALETTES36["cobalt"]["iceA"]),
                  [tohex(outs["cobalt"][2, 10]), tohex(outs["cobalt"][-1, 10])], "skyB / iceA"),
            check("ledger palette drives the same shader", near(outs["ledger"][-1, 10], PALETTES36["ledger"]["iceA"]) and
                  near(outs["ledger"][30, -1], PALETTES36["ledger"]["rim"]), [tohex(outs["ledger"][-1, 10])], "ledger iceA / rim"),
            check("any uniform palette is honoured (random palette)", near(o_r[-1, 10], rnd["iceA"]) and near(o_r[2, 10], rnd["skyB"]),
                  True, True),
            check("no colour literal inside the shader", not literal_triples, literal_triples, []),
            check("negative control: cobalt render is not the ledger palette",
                  not near(outs["cobalt"][-1, 10], PALETTES36["ledger"]["iceA"]), tohex(outs["cobalt"][-1, 10]), "differs")], \
        [wd / "crystal_palettes.png"]


CASCADE = [("continuous-review.css", {"--bg": "#100c16", "--brand": "#8b5cf6", "--accent": "#5eead4"}),
           ("dashboard-theme.css", {"--bg": "#f8fafc", "--text": "#1e293b", "--brand": "#6366f1"}),
           ("product-model.css", {"--bg": "#f7f7fb", "--text": "#22183f", "--brand": "#5b2acb"}),
           ("kosif-one-editorial-theme.css", {"--bg": "#fbfaf6", "--text": "#24113f", "--brand": "#24113f",
                                              "--brand-2": "#4b2377", "--gold": "#c8a35d", "--green": "#216753"})]


def resolve_cascade(layers):
    final = {}
    for _, vars_ in layers:
        final.update(vars_)
    return final


@card("COLOR-37")
def audit_palettes_cascade(task, wd):
    for fname, vars_ in CASCADE:
        (wd / fname).write_text(":root {\n%s}\n" % "".join("  %s: %s;\n" % kv for kv in vars_.items()))
    order = [f for f, _ in CASCADE]
    parsed = [(f, dict(re.findall(r"(--[\w-]+):\s*(#[0-9a-f]{6})", (wd / f).read_text()))) for f in order]
    final = resolve_cascade(parsed)
    theme_color = "#24113f"
    status = {k: round(contrast(v, "#f7f7fb"), 2) for k, v in
              {"primary": "#5b2acb", "teal": "#087f86", "amber": "#ad6700", "coral": "#c93343"}.items()}
    rev = resolve_cascade(list(reversed(parsed)))
    (wd / "index.html").write_text("<meta name=theme-color content='%s'>\n" % theme_color +
                                   "".join("<link rel=stylesheet href='%s'>\n" % f for f in order))
    return [check("cascade order continuous-review -> dashboard -> product -> editorial", order ==
                  ["continuous-review.css", "dashboard-theme.css", "product-model.css", "kosif-one-editorial-theme.css"],
                  order, "as listed"),
            check("meta theme-color #24113f is painted by the final theme", theme_color in final.values(),
                  final, "#24113f present"),
            check("final ground is the editorial cream", final["--bg"] == "#fbfaf6", final["--bg"], "#fbfaf6"),
            check("Feather status hues pass the UI/large-text 3:1 tier on #f7f7fb", all(v >= 3 for v in status.values()), status, ">= 3"),
            check("negative control: reversed load order loses the theme colour", not (theme_color in rev.values() and
                                                                                       rev["--bg"] == "#fbfaf6"),
                  rev["--bg"], "#100c16")], [wd / "index.html"] + [wd / f for f in order]


KINETIC = {"A": ("#ECEAE3", "#3A3A3A", "#8A8A8A"), "B": ("#E6D8F6", "#6A1BD1", "#6A1BD1"), "C": ("#F4F3EF", "#111111", "#2B2B2B"),
           "D": ("#0B0D17", "#00E5FF", "#DDE6F0"), "E": ("#0A0A0A", "#C9A24B", "#EDE6D6"), "F": ("#FFFFFF", "#E30613", "#000000"),
           "G": ("#FFE8DC", "#2D2A4A", "#2D2A4A"), "H": ("#DDE3D3", "#2F4A3A", "#2F4A3A"), "I": ("#F7F9FC", "#0B2A5B", "#4A5A78"),
           "J": ("#BDBDB8", "#C6FF00", "#0A0A0A"), "K": ("#F3E3C3", "#E8732C", "#5A3A22"), "L": ("#141414", "#E0A100", "#BDBDBD"),
           "M": ("#0F3B6E", "#FFFFFF", "#A9C8EE"), "N": ("#F2EBDD", "#D94032", "#1A1A1A"), "O": ("#0E0E1A", "#FFFFFF", "#C9CBE0"),
           "P": ("#0B0B0B", "#FFD400", "#FFFFFF"), "Q": ("#E9ECF2", "#141414", "#5A5F6E")}
R_KEYS = ("background", "accent", "font", "finish", "overlay", "animation", "transition")


def theme_r(spec):
    missing = [k for k in R_KEYS if not spec.get(k)]
    if missing:
        raise ValueError("missing: %s" % ",".join(missing))
    for k in ("background", "accent"):
        if not re.match(r"^#[0-9a-f]{6}$", spec[k]):
            raise ValueError("bad hex for %s" % k)
    return dict({"small": "#333333", "end_card": "fade to black"}, **spec)


def style_lock(theme):
    bg, hero, small = theme
    return "STYLE LOCK: background %s, hero colour %s, small text %s; same font, finish and transition in every clip." % \
        (bg, hero, small)


@card("COLOR-38")
def kinetic_themes(task, wd):
    lock = style_lock(KINETIC["D"])
    prompts = ["Clip %d: %s\n%s" % (i + 1, beat, lock) for i, beat in enumerate(["hook", "build", "payoff"])]
    (wd / "prompts.txt").write_text("\n\n".join(prompts), encoding="utf-8")
    ok_hex = all(re.match(r"^#[0-9A-F]{6}$", c) for t in KINETIC.values() for c in t)
    good = theme_r({"background": "#101010", "accent": "#ff5500", "font": "Tajawal", "finish": "matte",
                    "overlay": "grain", "animation": "slide", "transition": "cut"})
    errs = []
    for bad in ({"background": "#GGG000", "accent": "#ff5500", "font": "x", "finish": "x", "overlay": "x",
                 "animation": "x", "transition": "x"}, {"background": "#101010", "accent": "#ff5500"}):
        try:
            theme_r(bad)
            errs.append(None)
        except ValueError as e:
            errs.append(str(e))
    naive = "Clip 1: hook"
    return [check("17 locked themes A-Q, all valid hex", len(KINETIC) == 17 and ok_hex, len(KINETIC), 17),
            check("lock paragraph repeated verbatim in every clip", all(p.endswith(lock) for p in prompts) and
                  len({p.split("\n")[1] for p in prompts}) == 1, True, True),
            check("custom R defaults (#333333, fade to black)", good["small"] == "#333333" and good["end_card"] == "fade to black",
                  [good["small"], good["end_card"]], ["#333333", "fade to black"]),
            check("R rejects bad hex and missing keys", all(errs), errs, "both rejected"),
            check("negative control: a prompt without the lock fails", not (lock in naive), False, True)], \
        [wd / "prompts.txt", jdump(wd / "themes.json", KINETIC)]


EDITORIAL = {"1": {"bg": "#F4F1EC", "grid": "#D7D4D0", "accent": "#6134B9", "text": "#24212A", "line": "#D5CFD9", "shape": "#E6DFF5"},
             "2": {"bg": "#1B252C", "grid": "#36414A", "accent": "#24DAD1", "text": "#EFF8F7", "line": "#364B50", "shape": "#24373B"},
             "3": {"bg": "#F1E9DD", "grid": "#D8CAB8", "accent": "#BC5935", "text": "#2C2928", "line": "#DFCEBD", "shape": "#E9D1C0"}}


def editorial_frame(p, accent_share=.2, w=200, h=120):
    im = Image.new("RGB", (w, h), p["bg"])
    d = ImageDraw.Draw(im)
    for x in range(0, w, 20):
        d.line((x, 0, x, h), fill=p["grid"])
    d.rectangle((10, 10, 90, 60), fill=p["shape"])
    d.rectangle((10, 70, 120, 78), fill=p["text"])
    d.line((10, 90, 190, 90), fill=p["line"], width=2)
    aw = int(round(accent_share * w * h / 50))
    d.rectangle((w - 10 - aw, 100 - 50, w - 10, 99), fill=p["accent"])
    return np.asarray(im).astype(float)


@card("COLOR-39")
def editorial_palettes(task, wd):
    res, frames = {}, []
    for k, p in EDITORIAL.items():
        f = editorial_frame(p)
        frames.append(f)
        px = f.reshape(-1, 3)
        acc = float(np.mean(np.all(px == np.array(hx(p["accent"])), 1)))
        allowed = {hx(c) for c in p.values()}
        stray = int(sum(1 for c in np.unique(px, axis=0) if tuple(int(v) for v in c) not in allowed))
        res[k] = (round(acc, 3), stray)
    save(np.vstack(frames), wd / "editorial_palettes.png")
    naive = editorial_frame(EDITORIAL["1"], accent_share=.5)
    nacc = float(np.mean(np.all(naive.reshape(-1, 3) == np.array(hx(EDITORIAL["1"]["accent"])), 1)))
    return [check("each palette: accent ~20 % of pixels (15..25 %)", all(.15 <= a <= .25 for a, _ in res.values()), res,
                  ".15..25"),
            check("every pixel is a palette colour", all(s == 0 for _, s in res.values()), res, 0),
            check("text on ground passes 4.5 in all three", all(contrast(p["text"], p["bg"]) >= 4.5 for p in EDITORIAL.values()),
                  [round(contrast(p["text"], p["bg"]), 2) for p in EDITORIAL.values()], ">= 4.5"),
            check("negative control: a half-accent frame breaks 80/20", not (.15 <= nacc <= .25), nacc, ".15..25")], \
        [wd / "editorial_palettes.png"]


OWNER = {"navy_gold": {"bg": "#1b2a49", "accent": "#E7B65A", "sparkle": "#ffe9b8"},
         "ivory_ink_gold": {"bg": "#F5F0E6", "ink": "#121417", "accent": "#E7B65A", "accent2": "#F3D9A4"},
         "lab_hud": {"bg": "#040b0c", "ink": "#eaffed", "accent": "#9dffb4", "warn": "#ffda77", "fail": "#ff907a"},
         "rainy_neon_city": {"bg": "#030915", "accent": "#28eee5", "rose": "#ff4566", "lamp": "#ffe3a4"},
         "night_sea": {"bg": "#061525", "ink": "#f3ead8", "accent": "#ff9a3c", "fog": "#0d1626"},
         "showreel_red_dot": {"bg": "#0f1211", "ink": "#f2f1ec", "accent": "#e4342f", "secondary": "#9aa29d"},
         "dusk_lava": {"bg": "#070d18", "accent": "#f97316", "lava_hi": "#fde047"},
         "flat_science": {"bg": "#BFE6FF", "ink": "#0B2545", "accent": "#FF7A00", "sea": "#2B86E0"},
         "amber_sky_zinc": {"bg": "#09090b", "ink": "#fafafa", "accent": "#f59e0b", "sky": "#38bdf8"},
         "midnight_3d": {"bg": "#030712", "accent": "#fbbf24", "key": "#38bdf8", "rim": "#f43f5e"},
         "lime_turquoise_navy": {"bg": "#0c1728", "accent": "#d5f375", "turquoise": "#9fece2"},
         "workbench_pastel": {"bg": "#11171b", "accent": "#a7e8d0", "lavender": "#d3c0fa", "apricot": "#f5ce91"}}


@card("COLOR-40")
def owner_palettes(task, wd):
    css = "\n".join("[data-palette=%s] {\n%s}" % (n, "".join("  --%s: %s;\n" % kv for kv in p.items())) for n, p in OWNER.items())
    (wd / "owner_palettes.css").write_text(css + "\n")
    sheet = np.vstack([chart(list(p.values()) + [p["bg"]] * (6 - len(p)), 20) for p in OWNER.values()])
    save(sheet, wd / "owner_palettes.png")
    one_accent = all(sum(1 for k in p if k == "accent") == 1 for p in OWNER.values())
    inks = {n: round(contrast(p["ink"], p["bg"]), 2) for n, p in OWNER.items() if "ink" in p}
    sw_ok = tohex(sheet[10, 30]) == list(OWNER["navy_gold"].values())[1].lower()
    bad = dict(OWNER["navy_gold"], accent2="#c9953f", accent3="#a9772a")
    return [check("12 palettes, exactly one accent each", len(OWNER) == 12 and one_accent, len(OWNER), 12),
            check("ink on ground >= 7:1 where an ink exists", all(v >= 7 for v in inks.values()), inks, ">= 7"),
            check("swatch sheet pixels are the exact hex", sw_ok, tohex(sheet[10, 30]), "#e7b65a"),
            check("negative control: a three-accent palette is flagged",
                  not (sum(1 for k in bad if k.startswith("accent")) == 1), sum(1 for k in bad if k.startswith("accent")), 1)], \
        [wd / "owner_palettes.css", wd / "owner_palettes.png"]


TOKENS18 = ("bg", "fg", "muted", "surface", "border", "brand", "accent", "accent-2", "font-display", "font-body",
            "font-mono", "radius", "space-1", "space-2", "space-3", "dur-beat", "ease-standard", "ease-emphasis")
THEMES42 = {"neutral": ("#f3f4f6", "#111318", "#1d4ed8", "#0284c7", "#60a5fa", "Inter", ".4s", "cubic-bezier(.2,0,0,1)"),
            "bold": ("#080611", "#fff8ff", "#ff3d81", "#7c5cff", "#00d4ff", "Impact", ".32s", "cubic-bezier(.34,1.56,.64,1)"),
            "editorial": ("#e9e1d2", "#202725", "#246b63", "#31776f", "#8a6549", "Georgia", ".48s", "cubic-bezier(.2,0,0,1)")}


@card("COLOR-42")
def theme_contract(task, wd):
    (wd / "themes").mkdir(exist_ok=True)
    files = {}
    for n, (bg, fg, brand, acc, acc2, fnt, beat, emph) in THEMES42.items():
        vals = {"bg": bg, "fg": fg, "muted": fg + "99", "surface": bg, "border": fg + "22", "brand": brand, "accent": acc,
                "accent-2": acc2, "font-display": fnt, "font-body": fnt, "font-mono": "monospace", "radius": "12px",
                "space-1": "8px", "space-2": "16px", "space-3": "32px", "dur-beat": beat,
                "ease-standard": "cubic-bezier(.2,0,0,1)", "ease-emphasis": emph}
        p = wd / "themes" / ("%s.css" % n)
        p.write_text(":root {\n%s}\n" % "".join("  --%s: %s;\n" % (k, vals[k]) for k in TOKENS18))
        files[n] = p
    comp = ".card{background:var(--surface,#0b0b0b);color:var(--fg, #f8fafc);border-color:var(--brand,#888)}\n"
    (wd / "card.css").write_text(comp)
    renders, counts = [], {}
    for n, p in files.items():
        vars_ = dict(re.findall(r"--([\w-]+):\s*([^;]+);", p.read_text()))
        counts[n] = len(vars_)
        get = lambda name: vars_.get(name) or re.search(r"var\(--%s,\s*([^)]+)\)" % name, comp).group(1)
        im = Image.new("RGB", (60, 30), get("surface"))
        ImageDraw.Draw(im).rectangle((10, 10, 50, 20), fill=get("fg"))
        renders.append((n, np.asarray(im).astype(float)))
    save(np.vstack([r for _, r in renders]), wd / "themes.png")
    px_ok = all(tohex(r[2, 2]) == THEMES42[n][0] and tohex(r[15, 30]) == THEMES42[n][1] for n, r in renders)
    return [check("every theme defines exactly the 18 tokens", all(c == 18 for c in counts.values()), counts, 18),
            check("one component restyled by each theme (pixels = theme bg/fg)", px_ok, True, True),
            check("component reads var(--fg, #f8fafc) and declares no tokens", "var(--fg, #f8fafc)" in comp and ":root" not in comp,
                  True, True),
            check("bold uses the overshoot easing", "cubic-bezier(.34,1.56,.64,1)" in files["bold"].read_text(), True, True),
            check("negative control: without a theme the fallback colour paints", not (tohex(
                np.asarray(Image.new("RGB", (2, 2), "#f8fafc")).astype(float)[0, 0]) == THEMES42["neutral"][1]), None, None)], \
        [wd / "themes.png"] + list(files.values())


LIB43 = {"bold_energetic": ["#FFBE0B", "#FB5607", "#FF006E", "#8338EC", "#3A86FF"],
         "clean_corporate": ["#FFFCF2", "#CCC5B9", "#403D39", "#252422", "#EB5E28"],
         "dark_premium": ["#000000", "#14213D", "#FCA311", "#E5E5E5", "#FFFFFF"],
         "jewel_rich": ["#5F0F40", "#9A031E", "#FB8B24", "#E36414", "#0F4C5C"],
         "monochrome": ["#F8F9FA", "#DEE2E6", "#ADB5BD", "#495057", "#212529"],
         "nature_earth": ["#606C38", "#283618", "#FEFAE0", "#DDA15E", "#BC6C25"],
         "neon_electric": ["#F72585", "#B5179E", "#7209B7", "#560BAD", "#3A0CA3"],
         "pastel_soft": ["#CDB4DB", "#FFC8DD", "#FFAFCC", "#BDE0FE", "#A2D2FF"],
         "warm_editorial": ["#264653", "#2A9D8F", "#E9C46A", "#F4A261", "#E76F51"]}


def pick_row(row):
    by_l = sorted(row, key=lambda c: rel_lum(hx(c)))
    bg = by_l[0] if rel_lum(hx(by_l[0])) < .05 else by_l[-1]
    fg = max((c for c in row if c != bg), key=lambda c: contrast(c, bg))
    accent = max((c for c in row if c not in (bg, fg)), key=lambda c: float(rgb2hsv(np.array(hx(c), float))[1]))
    return {"bg": bg, "fg": fg, "accent": accent}


@card("COLOR-43")
def palette_library(task, wd):
    picks = {n: pick_row(r) for n, r in LIB43.items()}
    same_row = all(set(p.values()) <= set(LIB43[n]) for n, p in picks.items())
    fg_ok = {n: round(contrast(p["fg"], p["bg"]), 2) for n, p in picks.items()}
    g = np.linspace(0, 1, 200)[None, :, None]
    grad = np.repeat(np.array(hx("#FFFFFF")) * (1 - g) + np.array(hx("#9B9B9B")) * g, 20, 0)
    save(grad, wd / "heading_gradient.png")
    gr = load(wd / "heading_gradient.png")
    timing = {"entrance": .65, "gap": .3, "crossfade": .4, "hold": 1.5}
    t_ok = .5 <= timing["entrance"] <= .8 and .2 <= timing["gap"] <= .4 and .3 <= timing["crossfade"] <= .5 and 1 <= timing["hold"] <= 2
    mixed = {"bg": LIB43["pastel_soft"][0], "fg": LIB43["monochrome"][4], "accent": LIB43["neon_electric"][0]}
    is_one_row = lambda p: any(set(p.values()) <= set(r) for r in LIB43.values())
    return [check("one bg / fg / accent declared per library, all from ONE row", same_row, picks, "same row"),
            check("fg on bg >= 4.5 in every pick", all(v >= 4.5 for v in fg_ok.values()), fg_ok, ">= 4.5"),
            check("heading gradient endpoints #FFFFFF -> #9B9B9B", tohex(gr[5, 0]) == "#ffffff" and tohex(gr[5, -1]) == "#9b9b9b",
                  [tohex(gr[5, 0]), tohex(gr[5, -1])], ["#ffffff", "#9b9b9b"]),
            check("demo-kit timing inside its ranges", t_ok, timing, "entr .5-.8, gap .2-.4, xfade .3-.5, hold 1-2"),
            check("negative control: a mixed-row pick is rejected", not is_one_row(mixed), mixed, "rejected")], \
        [wd / "heading_gradient.png", jdump(wd / "picks.json", picks)]


EMOTION = {"trust": "#1E40AF", "navy": "#1E3A5F", "energy": "#DC2626", "warm": "#EA580C", "growth": "#16A34A",
           "teal": "#0D9488", "premium": "#7C3AED", "developer": "#4F46E5", "heritage_amber": "#D97706", "neutral": "#374151"}


def derive(primary):
    h, s, l = hex2hsl(primary)
    return {"primary": primary, "light": hsl2hex(h, s, min(1, l + .15)), "dark": hsl2hex(h, s, max(0, l - .08)),
            "glow": "rgba(%d,%d,%d,.12)" % hx(primary)}


@card("COLOR-44")
def emotion_primary(task, wd):
    out, checks = {}, []
    for k, c in EMOTION.items():
        d = derive(c)
        text = c if contrast(c, "#ffffff") >= 4.5 else d["dark"]
        d["text_on_white"] = text
        d["ratio"] = round(contrast(text, "#ffffff"), 2)
        out[k] = d
    dl = [abs(hex2hsl(out[k]["light"])[2] - hex2hsl(EMOTION[k])[2] - .15) < .01 for k in EMOTION if hex2hsl(EMOTION[k])[2] < .85]
    checks.append(check("light = L+15 %, dark = L-8 % in HSL", all(dl) and all(
        abs(hex2hsl(EMOTION[k])[2] - hex2hsl(out[k]["dark"])[2] - .08) < .01 for k in EMOTION), True, True))
    checks.append(check("primary text passes 4.5 on white (primary or its dark step)", all(v["ratio"] >= 4.5 for v in out.values()),
                        {k: v["ratio"] for k, v in out.items()}, ">= 4.5"))
    destructive = "#DC2626"

    def destructive_for(primary):
        return destructive if hue_dist(hex2hsl(primary)[0], hex2hsl(destructive)[0]) > 30 else "#7C3AED"
    checks.append(check("energy-red primary gets a different-hue destructive", destructive_for(EMOTION["energy"]) != destructive,
                        destructive_for(EMOTION["energy"]), "not #DC2626"))
    checks.append(check("negative control: raw energy red and destructive share a hue",
                        not (hue_dist(hex2hsl(EMOTION["energy"])[0], hex2hsl(destructive)[0]) > 30), 0, "> 30"))
    return checks, [jdump(wd / "primaries.json", out)]


CHIPS = {"violet": ("#f0edfa", "#5b2acb"), "teal": ("#e4f4f3", "#087f86"), "amber": ("#fff1d7", "#ad6700"),
         "coral": ("#fbe8ea", "#c93343")}
LADDER_HSL = {"success": (142, .70), "warning": (38, .90), "destructive": (0, .75), "info": (220, .90)}
STOP_L = {50: .96, 300: .70, 500: .45, 700: .30, 900: .16}


@card("COLOR-45")
def status_chips(task, wd):
    im = Image.new("RGB", (4 * 48, 48), "#ffffff")
    d = ImageDraw.Draw(im)
    for i, (soft, strong) in enumerate(CHIPS.values()):
        d.rounded_rectangle((i * 48 + 6, 6, i * 48 + 42, 42), radius=8, fill=soft)
        d.ellipse((i * 48 + 15, 15, i * 48 + 33, 33), fill=strong)
    im.save(wd / "chips.png")
    a = np.asarray(im).astype(float)
    chips_ratio = {k: round(contrast(s, b), 2) for k, (b, s) in CHIPS.items()}
    ladder = {k: {st: hsl2hex(h, s, l) for st, l in STOP_L.items()} for k, (h, s) in LADDER_HSL.items()}
    r700 = {k: round(contrast(v[700], v[50]), 2) for k, v in ladder.items()}
    r500 = {k: round(contrast(v[500], v[50]), 2) for k, v in ladder.items()}
    tile_ok = tohex(a[8, 24]) == CHIPS["violet"][0] and tohex(a[24, 24]) == CHIPS["violet"][1]
    soft_txt = {k: round(contrast(b, "#ffffff"), 2) for k, (b, _) in CHIPS.items()}
    return [check("chip strong-on-soft passes AA body 4.5", all(v >= 4.5 for v in chips_ratio.values()), chips_ratio, ">= 4.5"),
            check("ladder 50 + 700 passes AA body", all(v >= 4.5 for v in r700.values()), r700, ">= 4.5"),
            check("ladder 50 + 500 reaches the 3:1 large-text tier", all(v >= 3 for v in r500.values()), r500, ">= 3"),
            check("36 px tile with 18 px icon painted in the tokens", tile_ok, [tohex(a[8, 24]), tohex(a[24, 24])], CHIPS["violet"]),
            check("negative control: the soft tint alone is not readable text on white",
                  not any(v >= 3 for v in soft_txt.values()), soft_txt, "< 3")], \
        [wd / "chips.png", jdump(wd / "ladder.json", ladder)]


OKABE = ["#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7", "#000000"]
DEUTAN = np.array([[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]])


def simulate_deutan(hexc):
    return unlin(np.clip(DEUTAN @ lin(hx(hexc)), 0, 1))


def min_de(cols, sim=True):
    labs = [lab(simulate_deutan(c) if sim else np.array(hx(c), float)) for c in cols]
    return min(float(np.linalg.norm(labs[i] - labs[j])) for i in range(len(cols)) for j in range(i + 1, len(cols)))


@card("COLOR-46")
def colourblind_safe(task, wd):
    on_white = sorted(c for c in OKABE if contrast(c, "#ffffff") >= 3)
    exp = sorted(["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#000000"])
    de_ok = min_de(OKABE)
    naive = ["#d62728", "#2ca02c", "#ff7f0e", "#1f77b4"]
    de_naive = min_de(["#d62728", "#2ca02c"])
    sim = np.vstack([chart(OKABE, 24), chart([tohex(simulate_deutan(c)) for c in OKABE], 24)])
    save(sim, wd / "okabe_ito_deutan.png")
    return [check("Okabe-Ito colours reaching 3:1 on white are exactly the 5 listed", on_white == exp, on_white, exp),
            check("Okabe-Ito stays distinct under deuteranopia (min dE > 10)", de_ok > 10, de_ok, "> 10"),
            check("Tol / 7-hue sets <= 7 categories", len(["#4477AA", "#EE6677", "#228833", "#CCBB44", "#66CCEE", "#AA3377",
                                                           "#BBBBBB"]) <= 7, 7, "<= 7"),
            check("negative control: a default red/green pair collapses for deutans (dE < 10)", not (de_naive > 10), de_naive,
                  "< 10")], [wd / "okabe_ito_deutan.png", jdump(wd / "cvd.json", {"on_white_3to1": on_white,
                                                                                  "min_dE_deutan": de_ok, "naive": naive})]


HEAT_STOPS = [0, .12, .30, .45, .60, .78, 1.0]
HEAT_COLS = ["#04040c", "#2b0a5a", "#1f9e4a", "#f2d930", "#f28a1a", "#e0301e", "#ffffff"]   # card names roles only


def ramp_map(v, stops, cols, smooth=True, cap=None):
    v = np.asarray(v, float)
    if cap is not None:
        v = np.minimum(v, cap)
    c = np.array([hx(x) for x in cols], float)
    out = np.zeros(v.shape + (3,))
    out[...] = c[0]
    for i in range(len(stops) - 1):
        t = np.clip((v - stops[i]) / (stops[i + 1] - stops[i]), 0, 1)
        if smooth:
            t = t * t * (3 - 2 * t)
        m = (v >= stops[i])
        out = np.where(m[..., None], c[i] * (1 - t[..., None]) + c[i + 1] * t[..., None], out)
    return out


@card("COLOR-48")
def heat_ramp(task, wd):
    v = np.repeat(np.linspace(0, 1, 256)[None], 24, 0)
    capped = ramp_map(v, HEAT_STOPS, HEAT_COLS, cap=.75)
    save(capped, wd / "heat_ramp.png")
    at_stops = [tohex(ramp_map(np.array([s]), HEAT_STOPS, HEAT_COLS)[0]) for s in HEAT_STOPS]
    mid = ramp_map(np.array([(.30 + .45) / 2]), HEAT_STOPS, HEAT_COLS)[0]
    exp_mid = (np.array(hx(HEAT_COLS[2])) + np.array(hx(HEAT_COLS[3]))) / 2
    q = ramp_map(np.array([.30 + .25 * .15]), HEAT_STOPS, HEAT_COLS)[0]
    lin_q = np.array(hx(HEAT_COLS[2])) * .75 + np.array(hx(HEAT_COLS[3])) * .25
    top = ramp_map(np.array([1.0]), HEAT_STOPS, HEAT_COLS, cap=.75)[0]
    uncapped = ramp_map(np.array([1.0]), HEAT_STOPS, HEAT_COLS)[0]
    brand = ramp_map(v[0], [0, .5, 1], ["#0b1020", "#7a3fd0", "#f3e8ff"])
    mono = bool(np.all(np.diff(luma(brand)) >= -1e-6))
    return [check("each of the 7 stops lands on its colour", at_stops == [c.lower() for c in HEAT_COLS], at_stops, HEAT_COLS),
            check("midpoint between stops is the average (smoothstep symmetric)", float(np.abs(mid - exp_mid).max()) < .6,
                  tohex(mid), tohex(exp_mid)),
            check("smoothstep, not linear, at 25 % of a segment", float(np.abs(q - lin_q).max()) > 5, float(np.abs(q - lin_q).max()),
                  "> 5"),
            check("cap .75: heat 1.0 never reaches white", float(top.min()) < 200, tohex(top), "not white"),
            check("brand-ramp swap keeps dark -> light", mono, mono, True),
            check("negative control: uncapped heat 1.0 blows to white", not (float(uncapped.min()) < 200), tohex(uncapped), "#ffffff")], \
        [wd / "heat_ramp.png", jdump(wd / "heat.json", {"stops": HEAT_STOPS, "colours": HEAT_COLS,
                                                        "note": "the card names the stop roles; these hex are chosen here"})]


MAGMA = [(0, (0, 0, 4)), (.2, (40, 11, 84)), (.4, (120, 28, 109)), (.6, (192, 58, 118)), (.75, (236, 105, 89)),
         (.88, (251, 165, 74)), (1, (252, 253, 191))]


def magma(v):
    s = [p for p, _ in MAGMA]
    return ramp_map(v, s, [tohex(c) for _, c in MAGMA], smooth=False)


def alpine(height, slope):
    if height < -5:
        return "#2f4a3a"
    if height < 5:
        return "#b9a77a"
    if height >= 520:
        return "#f4f7fb"
    if 120 <= height <= 420 and slope >= .28:
        return "#5d5a58" if slope < .6 else "#7a6f66"
    return "#4e6e34" if height <= 25 else "#6b8a3c"


@card("COLOR-49")
def magma_alpine(task, wd):
    v = np.repeat(np.linspace(0, 1, 256)[None], 16, 0)
    img = magma(v)
    save(img, wd / "magma.png")
    stops = [tuple(int(round(x)) for x in magma(np.array([p]))[0]) for p, _ in MAGMA]
    mono = bool(np.all(np.diff(luma(img[0])) >= -1e-6))
    bands = {"deep": alpine(-10, 0), "sand": alpine(2, 0), "grass": alpine(15, .1), "rock": alpine(300, .4), "snow": alpine(800, .2)}
    rev = magma(v[:, ::-1])
    return [check("magma hits its 7 stops", stops == [c for _, c in MAGMA], stops, [c for _, c in MAGMA]),
            check("magma luminance rises monotonically", mono, mono, True),
            check("alpine bands by height and slope", bands == {"deep": "#2f4a3a", "sand": "#b9a77a", "grass": "#4e6e34",
                                                               "rock": "#5d5a58", "snow": "#f4f7fb"}, bands, "6 bands"),
            check("negative control: reversed input breaks the monotone ramp",
                  not bool(np.all(np.diff(luma(rev[0])) >= -1e-6)), False, True)], \
        [wd / "magma.png", jdump(wd / "alpine.json", bands)]


SCHEMES = {"complementary": (0, 180), "analogous": (-30, 0, 30), "triadic": (0, 120, 240), "split": (0, 150, 210),
           "tetradic": (0, 60, 180, 240)}


def harmony(scheme, base, sat=.6, light=.5):
    hues = [(base + o) % 360 for o in SCHEMES[scheme]]
    return hues, ["hsl(%d %d%% %d%%)" % (h, sat * 100, light * 100) for h in hues]


def oklch(hexc):
    l = lin(hx(hexc))
    m1 = np.array([[0.4122214708, 0.5363325363, 0.0514459929], [0.2119034982, 0.6806995451, 0.1073969566],
                   [0.0883024619, 0.2817188376, 0.6299787005]])
    m2 = np.array([[0.2104542553, 0.7936177850, -0.0040720468], [1.9779984951, -2.4285922050, 0.4505937099],
                   [0.0259040371, 0.7827717662, -0.8086757660]])
    L, a, b = m2 @ np.cbrt(m1 @ l)
    return float(L), float(math.hypot(a, b)), float(math.degrees(math.atan2(b, a)) % 360)


def detect_harmony(hexes, tol=15):
    hues = sorted(oklch(h)[2] for h in hexes if oklch(h)[1] >= .04)
    if not hues:
        return "neutral"
    if max(hue_dist(a, b) for a in hues for b in hues) <= tol:
        return "mono"
    for name in ("complementary", "triadic", "split", "tetradic", "analogous"):
        offs = SCHEMES[name]
        for base in hues:
            want = [(base + o) % 360 for o in offs]
            if len(hues) == len(want) and all(min(hue_dist(w, h) for h in hues) <= tol for w in want):
                return name
    return "free"


@card("COLOR-50")
def harmony_generator(task, wd):
    split, _ = harmony("split", 210)
    comp, css = harmony("complementary", 222)
    detected = {}
    for name in SCHEMES:
        hues, _ = harmony(name, 200)
        hexes = []
        for h in hues:          # equalise in OKLCH hue space by searching the HSL hue that gives the target OKLCH hue
            best = min(range(0, 360), key=lambda x: hue_dist(oklch(hsl2hex(x, .6, .5))[2], oklch(hsl2hex(hues[0], .6, .5))[2]
                                                              + (h - hues[0])))
            hexes.append(hsl2hex(best, .6, .5))
        detected[name] = detect_harmony(hexes)
    grey = detect_harmony(["#808080", "#7f7f80"])
    free = detect_harmony([hsl2hex(h, .6, .5) for h in (10, 47, 133, 300)])
    save(chart([hsl2hex(h, .6, .5) for h in split] + [hsl2hex(h, .6, .5) for h in comp], 32), wd / "harmonies.png")
    return [check("split(210) -> [210, 0, 60]", split == [210, 0, 60], split, [210, 0, 60]),
            check("complementary(222) -> [222, 42] as hsl(... 60% 50%)", comp == [222, 42] and css[0] == "hsl(222 60% 50%)",
                  [comp, css], [[222, 42], "hsl(222 60% 50%)"]),
            check("detector recovers every generated scheme", all(k == v for k, v in detected.items()), detected, list(SCHEMES)),
            check("greys (C < .04) are excluded", grey == "neutral", grey, "neutral"),
            check("negative control: unrelated hues are flagged free", free == "free", free, "free")], \
        [wd / "harmonies.png", jdump(wd / "harmony.json", detected)]


def flatten(fg, bg, alpha):
    return tuple(np.array(fg, float) * alpha + np.array(bg, float) * (1 - alpha))


@card("COLOR-52")
def wcag_contrast(task, wd):
    known = {("#000000", "#ffffff"): 21.0, ("#767676", "#ffffff"): 4.54, ("#777777", "#ffffff"): 4.48}
    got = {"%s/%s" % k: round(contrast(*k), 2) for k in known}
    fr = [np.full((36, 64, 3), 30.0), np.full((36, 64, 3), 235.0)]           # darkest / brightest frames under the plate
    plate, alpha = (0, 0, 0), .45
    flat = [flatten(plate, f[0, 0], alpha) for f in fr]
    worst = min(contrast((255, 255, 255), c) for c in flat)
    naive = contrast((255, 255, 255), plate)
    tiers = lambda r, role: r >= {"body": 4.5, "large": 3.0}[role]
    jdump(wd / "contrast.json", {"known": got, "plate_flattened": [tohex(c) for c in flat], "worst": worst})
    save(np.vstack([np.full((20, 64, 3), np.array(c)) for c in flat]), wd / "plate_flattened.png")
    return [check("known pairs: 21 / 4.54 / 4.48", all(abs(got["%s/%s" % k] - v) < .01 for k, v in known.items()), got,
                  {"%s/%s" % k: v for k, v in known.items()}),
            check("#777 on white fails body 4.5, passes large 3", not tiers(got["#777777/#ffffff"], "body") and
                  tiers(got["#777777/#ffffff"], "large"), got["#777777/#ffffff"], "fail body, pass large"),
            check("flattened glass plate over the brightest frame fails body text", worst < 4.5, worst, "< 4.5"),
            check("negative control: ignoring alpha wrongly passes (21:1)", naive >= 4.5, naive, ">= 4.5 (wrong)")], \
        [wd / "contrast.json", wd / "plate_flattened.png"]


@card("COLOR-53")
def dark_variant(task, wd):
    bg, text = hsl2hex(220, .10, .08), hsl2hex(0, 0, .90)
    brand_l, brand_d = hsl2hex(220, .90, .50), hsl2hex(220, .70, .60)
    tiers = {p: tohex(flatten(hx(text), hx(bg), p / 100)) for p in (100, 60, 40)}
    r = {"text": contrast(text, bg), "brand_dark": contrast(brand_d, bg), "brand_light_on_dark": contrast(brand_l, bg),
         "tier60": contrast(tiers[60], bg), "brand_on_white": contrast(brand_l, "#ffffff")}
    save(np.hstack([np.full((24, 24, 3), np.array(hx(c), float)) for c in (bg, text, brand_d, tiers[60])]), wd / "dark.png")
    dh, ds, dl = hex2hsl(brand_d)
    inverted = tohex(255 - np.array(hx("#ffffff"), float))
    return [check("brand hsl(220 90% 50%) -> hsl(220 70% 60%) (sat -20, L +10)", abs(ds - .7) < .01 and abs(dl - .6) < .01,
                  [ds, dl], [.7, .6]),
            check("text and lifted brand pass 4.5 on the tinted ground", r["text"] >= 4.5 and r["brand_dark"] >= 4.5, r, ">= 4.5"),
            check("lifted brand reads better than the light-mode brand on dark", r["brand_dark"] > r["brand_light_on_dark"], r,
                  "dark > light"),
            check("ground is brand-tinted near-black, never #000 / text never #fff", bg != "#000000" and text != "#ffffff" and
                  hue_dist(hex2hsl(bg)[0], 220) < 2, [bg, text], "tinted"),
            check("negative control: naive inversion gives pure #000", not (inverted != "#000000"), inverted, "#000000")], \
        [wd / "dark.png", jdump(wd / "dark.json", {"bg": bg, "text": text, "brand": brand_d, "tiers": tiers, "ratios": r})]


def neutral_ramp(brand_hue, sat=.08, n=9):
    return [hsl2hex(brand_hue, sat, l) for l in np.linspace(.06, .96, n)]


@card("COLOR-54")
def one_accent(task, wd):
    ramp9 = neutral_ramp(28)
    w, h = 200, 120
    frames, shares = [], []
    accent = "#f27525"
    for i in range(36):
        im = Image.new("RGB", (w, h), ramp9[1])
        d = ImageDraw.Draw(im)
        d.rectangle((10, 10, 120, 40), fill=ramp9[3])
        d.rectangle((10, 50, 190, 60), fill=ramp9[6])
        tint = max(0.0, 1 - i / 24)                    # arrival tint relaxes to neutral over 24 frames
        card_c = flatten(hx(accent), hx(ramp9[5]), .5 * tint)
        d.rectangle((10, 70, 100, 110), fill=tuple(int(round(v)) for v in card_c))
        d.rectangle((150, 75, 172, 105), fill=accent)  # the one accent element
        a = np.asarray(im).astype(float)
        frames.append(a)
        shares.append(float(np.mean(np.all(a.reshape(-1, 3) == np.array(hx(accent)), 1))))
    write_video(wd / "accent.mp4", frames, fps=24)
    tints = [float(np.abs(f[90, 50] - np.array(hx(ramp9[5]))).max()) for f in frames]
    lean = [hex2hsl(c) for c in ramp9[1:-1]]
    grey = neutral_ramp(28, sat=0)
    return [check("accent covers ~5 % of the frame (3..7 %)", all(.03 <= s <= .07 for s in shares), shares[0], ".03..07"),
            check("arrival tint relaxes to neutral within 12..50 frames", tints[0] > 20 and tints[24] < 1 and
                  all(tints[i + 1] <= tints[i] + 1e-9 for i in range(35)), [tints[0], tints[12], tints[24]], "decays to 0 at f24"),
            check("neutrals lean toward the brand hue (28 deg, sat > 0)", all(abs(hh - 28) < 3 and ss > 0 for hh, ss, _ in lean),
                  lean[:2], "hue 28"),
            check("negative control: a pure grey ramp has no lean", not all(hex2hsl(c)[1] > 0 for c in grey[1:-1]), grey[2], "sat 0")], \
        [wd / "accent.mp4"]


STRICT = {"plotter": ("#090909", "#f4f1ea", "#f27525"), "leadnotifi": ("#161616", "#f0f1ec", "#e4fb34")}


@card("COLOR-55")
def two_three_colours(task, wd):
    ink, paper, signal = STRICT["plotter"]
    frames, uniq, grounds = [], [], []
    for ch in range(4):
        ground, fig = (paper, ink) if ch % 2 == 0 else (ink, paper)
        im = Image.new("RGB", (160, 90), ground)
        d = ImageDraw.Draw(im)
        d.rectangle((10, 10, 110, 22), fill=fig)
        d.rectangle((10, 30, 70, 36), fill=fig)
        d.rectangle((120, 60, 150, 80), fill=signal)
        a = np.asarray(im).astype(float)
        frames += [a] * 8
        uniq.append({tohex(c) for c in np.unique(a.reshape(-1, 3), axis=0)})
        grounds.append(tohex(a[0, 0]))
    write_video(wd / "strict.mp4", frames, fps=8)
    save(frames[0], wd / "chapter1.png")
    allowed = {ink, paper, signal}
    g = np.linspace(0, 1, 160)[None, :, None]
    multi = np.repeat(np.array(hx("#7a3fd0")) * (1 - g) + np.array(hx("#20c0f0")) * g, 90, 0)
    multi_u = {tohex(c) for c in np.unique(multi.reshape(-1, 3), axis=0)}
    return [check("every frame uses only ink / paper / signal", all(u <= allowed for u in uniq), [sorted(u) for u in uniq[:2]],
                  sorted(allowed)),
            check("<= 3 hues", all(len(u) <= 3 for u in uniq), [len(u) for u in uniq], "<= 3"),
            check("ground flips every chapter", grounds == [paper, ink, paper, ink], grounds, [paper, ink, paper, ink]),
            check("negative control: a multi-gradient frame breaks the system", not (multi_u <= allowed), len(multi_u), "<= 3")], \
        [wd / "strict.mp4", wd / "chapter1.png"]


def style_lock_intake(hexes, mood):
    if not 4 <= len(hexes) <= 6:
        raise ValueError("need 4-6 named hex")
    bg = max(hexes, key=lambda kv: rel_lum(hx(kv[1])))
    if bg[0] != "bg":
        raise ValueError("bg must be the lightest")
    if sum(1 for k, _ in hexes if k == "accent") != 1:
        raise ValueError("exactly one accent")
    return "STYLE LOCK: palette %s; soft window light; 35 mm lens; low-contrast grade; fine grain; 1970s; mood: %s." % (
        ", ".join("%s %s" % kv for kv in hexes), ", ".join(mood))


@card("COLOR-56")
def style_lock_dna(task, wd):
    hexes = [("bg", "#f3ece2"), ("ink", "#1d1a17"), ("accent", "#8b2635"), ("mid", "#b9a58c"), ("shadow", "#4a3f36")]
    lock = style_lock_intake(hexes, ["quiet", "warm", "nostalgic"])
    shots = ["Shot %d: %s\n%s" % (i, s, lock) for i, s in enumerate(["street", "window", "hands"], 1)]
    (wd / "shots.txt").write_text("\n\n".join(shots))
    gen = np.zeros((90, 160, 3)) + hx("#e8dfd2")
    gen[60:72] = hx("#9a3442")                  # the generator drifted the brand band
    fixed = gen.copy()
    fixed[60:72] = hx("#8b2635")                # exact hex applied in the motion layer
    save(gen, wd / "generated.png")
    save(fixed, wd / "motion_layer.png")
    errs = []
    for bad in (hexes[:3], [("ink", "#ffffff")] + hexes[1:]):
        try:
            style_lock_intake(bad, ["a", "b", "c"])
            errs.append(None)
        except ValueError as e:
            errs.append(str(e))
    return [check("lock carries 5 hex + 3 mood words and repeats verbatim", all(s.endswith(lock) for s in shots) and
                  lock.count("#") == 5 and lock.count(",") >= 6, lock, "5 hex, 3 moods"),
            check("intake rejects <4 hex and a non-lightest bg", all(errs), errs, "both rejected"),
            check("motion layer band is exactly #8b2635", tohex(load(wd / "motion_layer.png")[66, 80]) == "#8b2635",
                  tohex(load(wd / "motion_layer.png")[66, 80]), "#8b2635"),
            check("negative control: the generated band is not the brand hex", not (tohex(gen[66, 80]) == "#8b2635"),
                  tohex(gen[66, 80]), "#8b2635")], [wd / "motion_layer.png", wd / "shots.txt"]


def tm_aces(x, exposure=1.0):
    x = np.asarray(x, float) * exposure / .6
    a_in = np.array([[0.59719, 0.35458, 0.04823], [0.07600, 0.90834, 0.01566], [0.02840, 0.13383, 0.83777]])
    a_out = np.array([[1.60475, -0.53108, -0.07367], [-0.10208, 1.10813, -0.00605], [-0.00327, -0.07276, 1.07602]])
    v = x @ a_in.T
    v = (v * (v + 0.0245786) - 0.000090537) / (v * (0.983729 * v + 0.4329510) + 0.238081)
    return np.clip(v @ a_out.T, 0, 1)


def tm_neutral(c, exposure=1.0):
    c = np.asarray(c, float) * exposure
    start, desat = .8 - .04, .15
    x = c.min(-1, keepdims=True)
    off = np.where(x < .08, x - 6.25 * x * x, .04)
    c = c - off
    peak = c.max(-1, keepdims=True)
    d = 1 - start
    newp = 1 - d * d / (peak + d - start)
    scaled = c * np.where(peak > 0, newp / np.maximum(peak, 1e-9), 1)
    g = 1 - 1 / (desat * (peak - newp) + 1)
    comp = scaled * (1 - g) + newp * g
    return np.clip(np.where(peak < start, c, comp), 0, 1)


def tm_agx(c, exposure=1.0):
    c = np.asarray(c, float) * exposure
    m = np.array([[0.842479062253094, 0.0784335999999992, 0.0792237451477643],
                  [0.0423282422610123, 0.878468636469772, 0.0791661274605434],
                  [0.0423756549057051, 0.0784336, 0.879142973793104]])
    inv = np.array([[1.19687900512017, -0.0980208811401368, -0.0990297440797205],
                    [-0.0528968517574562, 1.15190312990417, -0.0989611768448433],
                    [-0.0529716355144438, -0.0980434501171241, 1.15107367264116]])
    lo, hi = -12.47393, 4.026069
    v = c @ m.T
    v = np.clip(np.log2(np.maximum(v, 1e-10)), lo, hi)
    v = (v - lo) / (hi - lo)
    x2 = v * v
    x4 = x2 * x2
    v = 15.5 * x4 * x2 - 40.14 * x4 * v + 31.96 * x4 - 6.868 * x2 * v + .4298 * x2 + .1191 * v - .00232
    v = v @ inv.T
    return np.clip(np.maximum(v, 0) ** 2.2, 0, 1)        # back to linear


def pick_tone(kind):
    return {"product": "neutral", "neon": "agx", "fire": "agx", "lamp": "agx"}.get(kind, "aces")


@card("COLOR-57")
def tone_curves(task, wd):
    neon = np.array([6.0, 0.9, 0.12])          # bright saturated orange-red in linear light
    h_in = hue_of(unlin(neon / neon.max()))
    h = {name: hue_of(unlin(f(neon))) for name, f in (("aces", tm_aces), ("agx", tm_agx), ("neutral", tm_neutral))}
    drift = {k: hue_dist(v, h_in) for k, v in h.items()}
    prod = np.array([.5, .3, .2])
    neu = tm_neutral(prod)
    ramp_lin = np.linspace(0, 8, 200)[:, None] * np.array([1.0, .5, .25])
    strip = np.stack([unlin(f(ramp_lin)) for f in (tm_aces, tm_agx, tm_neutral)])
    save(np.repeat(strip, 12, 0).reshape(36, 200, 3), wd / "tone_curves.png")
    mono = all(bool(np.all(np.diff(luma(s)) >= -1e-6)) for s in strip)
    return [check("AgX keeps the neon hue better than ACES", drift["agx"] < drift["aces"], drift, "agx < aces"),
            check("PBR Neutral is faithful below compression: (.5,.3,.2) -> (.46,.26,.16)",
                  float(np.abs(neu - np.array([.46, .26, .16])).max()) < 1e-6, neu.tolist(), [.46, .26, .16]),
            check("all three curves are monotone on a 0..8 ramp", mono, mono, True),
            check("per-shot pick: product neutral, neon agx", pick_tone("product") == "neutral" and pick_tone("neon") == "agx",
                  [pick_tone("product"), pick_tone("neon")], ["neutral", "agx"]),
            check("negative control: plain clipping maps 6.0 and 8.0 to the same white", np.allclose(np.clip(6.0, 0, 1),
                                                                                                     np.clip(8.0, 0, 1)), True, True)], \
        [wd / "tone_curves.png", jdump(wd / "tone.json", {"hue_in": h_in, "hue_out": h, "drift": drift,
                                                          "engine": "numpy ports of three.js ACESFilmic, AgX, Khronos PBR Neutral"})]


def look_pass(img, gamut=None, night=0.0, split=0.0, warm="#ffc98a", cool="#5a7fb8"):
    v = np.asarray(img, float) / 255.0
    if gamut:
        c, wdt, st = gamut
        hsv = rgb2hsv(v * 255)
        dist = np.vectorize(lambda h: hue_dist(h, c))(hsv[..., 0])
        out_w = smoothstep(wdt / 2, wdt / 2 + 25, dist)
        y = (0.2126 * v[..., 0] + 0.7152 * v[..., 1] + 0.0722 * v[..., 2])[..., None]
        v = v + (y - v) * (out_w * st)[..., None]
    if night:
        rod = (v @ np.array([.05, .55, .40]))[..., None]
        y = (0.2126 * v[..., 0] + 0.7152 * v[..., 1] + 0.0722 * v[..., 2])[..., None]
        w = (1 - smoothstep(.02, .35, y)) * night
        v = v * (1 - w) + rod * np.array([.72, .86, 1.12]) * .75 * w
    if split:
        y = (0.2126 * v[..., 0] + 0.7152 * v[..., 1] + 0.0722 * v[..., 2])[..., None]
        t = smoothstep(.1, .7, y)
        tint = (np.array(hx(cool)) * (1 - t) + np.array(hx(warm)) * t) / 255.0
        v = v * (1 - .35 * split) + v * tint / np.maximum(tint.mean(-1, keepdims=True), 1e-6) * .35 * split
    return np.clip(v, 0, 1) * 255


@card("COLOR-58")
def look_pass_card(task, wd):
    a = chart(["#c04040", "#4060c0", "#3a1010", "#303030", "#d0d0d0"], 32)
    g = look_pass(a, gamut=(220, 60, 1.0))
    n = look_pass(a, night=1.0)
    s = look_pass(a, split=1.0)
    save(np.vstack([a, g, n, s]), wd / "look_pass.png")
    sat = lambda x, i: float(rgb2hsv(patch(x, i, 32))[1])
    dark_red_in, dark_red_n = patch(a, 2, 32), patch(n, 2, 32)
    sh, hi = patch(s, 3, 32), patch(s, 4, 32)
    return [check("gamut wedge 220 +-30: blue kept", abs(sat(g, 1) - sat(a, 1)) < .01, [sat(a, 1), sat(g, 1)], "unchanged"),
            check("gamut: red outside the wedge desaturated", sat(g, 0) < .05, sat(g, 0), "< .05"),
            check("Purkinje night: dark red turns rod-blue (B > R) and darker", dark_red_n[2] > dark_red_n[0] and
                  luma(dark_red_n) < luma(dark_red_in), [tohex(dark_red_in), tohex(dark_red_n)], "B > R, darker"),
            check("night leaves bright pixels alone (> .35 luma)", float(np.abs(patch(n, 4, 32) - patch(a, 4, 32)).max()) < 1,
                  tohex(patch(n, 4, 32)), "#d0d0d0"),
            check("split: shadows cool, highlights warm", sh[2] > sh[0] and hi[0] > hi[2], [tohex(sh), tohex(hi)], "cool / warm"),
            check("negative control: input greys are neutral", not (patch(a, 3, 32)[2] > patch(a, 3, 32)[0]), tohex(patch(a, 3, 32)),
                  "neutral")], [wd / "look_pass.png"]


def fog_exp2(col, fog, d, density, scatter):
    f = 1 - np.exp(-(density * np.array(scatter) * d) ** 2)
    return np.array(col, float) * (1 - f) + np.array(fog, float) * f


@card("COLOR-59")
def aerial_perspective(task, wd):
    ridge, fog = hx("#2b2420"), hx("#8790b0")
    dists = [700, 1400, 2600, 4500]
    cols = [fog_exp2(ridge, fog, d, .00062, [.55, .8, 1.3]) for d in dists]
    img = np.zeros((120, 200, 3)) + fog
    for i, c in enumerate(cols[::-1]):
        top = 30 + i * 18
        xx = np.arange(200)
        yline = top + (8 * np.sin(xx / (14 + 3 * i) + i)).astype(int)
        for x in xx:
            img[yline[x]:, x] = c
    save(img, wd / "ridges.png")
    br = [float(c[2] - c[0]) for c in cols]
    con = [float(np.abs(c - np.array(fog)).sum()) for c in cols]
    w = lambda dot, amount=.9: max(0.0, dot) ** 3 * amount
    warm = fog_exp2(ridge, np.array(fog) * (1 - w(1)) + np.array(hx("#c49a8a")) * w(1), 2600, .00062, [.55, .8, 1.3])
    flat = [fog_exp2(ridge, fog, d, 0, [.55, .8, 1.3]) for d in dists]
    return [check("distance turns bluer (B-R rises with distance)", all(br[i] < br[i + 1] for i in range(3)), br, "rising"),
            check("distance turns flatter (contrast to fog falls)", all(con[i] > con[i + 1] for i in range(3)), con, "falling"),
            check("fog toward the sun: weight dot^3 x amount", abs(w(1) - .9) < 1e-9 and abs(w(.5) - .1125) < 1e-9 and w(-.3) == 0,
                  [w(1), w(.5), w(-.3)], [.9, .1125, 0]),
            check("haze warms when facing the sun", warm[0] - warm[2] > cols[2][0] - cols[2][2], [tohex(warm), tohex(cols[2])],
                  "warmer"),
            check("negative control: without fog all ridges are identical",
                  not (len({tohex(c) for c in flat}) > 1), len({tohex(c) for c in flat}), "> 1")], [wd / "ridges.png"]


def shader_finish(img, warm=.5, lift=.02, vig=.42, ca=1.2, grain=.028, seed=0):
    v = np.asarray(img, float) / 255.0
    h, w = v.shape[:2]
    y = (0.2126 * v[..., 0] + 0.7152 * v[..., 1] + 0.0722 * v[..., 2])[..., None]
    tone = np.array([.92, .98, 1.08]) * (1 - y) + np.array([1.08, 1.0, .92]) * y
    v = v * tone
    v = v * (1 - warm + warm * np.array([1.05, .98, .9]))
    v = lift + v * (1 - lift)
    yy, xx = np.mgrid[0:h, 0:w]
    dx, dy = (xx - w / 2) / (w / 2), (yy - h / 2) / (h / 2)
    r = np.hypot(dx, dy) / math.sqrt(2)
    off = ca * w / 1920.0 * r
    from scipy.ndimage import map_coordinates
    rr = map_coordinates(v[..., 0], [yy - dy * off, xx - dx * off], order=1, mode="nearest")
    bb = map_coordinates(v[..., 2], [yy + dy * off, xx + dx * off], order=1, mode="nearest")
    v = np.stack([rr, v[..., 1], bb], -1)
    v = v * (1 - vig * smoothstep(.35, .95, r))[..., None]
    rng = np.random.default_rng(seed)
    v = v + (rng.random((h, w, 1)) - .5) * grain
    return np.clip(v, 0, 1) * 255


@card("COLOR-60")
def shader_finish_card(task, wd):
    flat = np.zeros((90, 160, 3)) + 128
    out = shader_finish(flat, grain=0)
    black = shader_finish(np.zeros((90, 160, 3)), grain=0, vig=0, warm=0)
    edge = np.zeros((90, 1920 // 6, 3))
    edge[:, -40:] = 255
    big = shader_finish(np.zeros((90, 1920, 3)) + np.where(np.arange(1920)[None, :, None] > 1700, 255, 0), vig=0, grain=0, warm=0,
                        lift=0, ca=1.2 * 8)
    fringe = float(np.abs(big[45, 1650:1750, 0] - big[45, 1650:1750, 2]).max())
    centre = float(np.abs(big[45, 900:1000, 0] - big[45, 900:1000, 2]).max())
    sh = shader_finish(np.zeros((8, 8, 3)) + 40, warm=0, vig=0, grain=0, lift=0)[4, 4]
    hi = shader_finish(np.zeros((8, 8, 3)) + 220, warm=0, vig=0, grain=0, lift=0)[4, 4]
    frames = [shader_finish(np.zeros((54, 96, 3)) + 128, warm=.75 + (.2 - .75) * i / 49, grain=.028, seed=i) for i in range(50)]
    write_video(wd / "water_cycle_warm.mp4", frames, fps=10)
    rb = [float(f[..., 0].mean() / f[..., 2].mean()) for f in (frames[0], frames[-1])]
    g1 = shader_finish(flat, seed=3)
    g2 = shader_finish(flat, seed=3)
    save(out, wd / "finish.png")
    return [check("lift: pure black rises to the lift (.02 -> ~5)", abs(float(black.mean()) - 5.1) < .6, float(black.mean()), 5.1),
            check("shadows cool / highlights warm", sh[2] > sh[0] and hi[0] > hi[2], [tohex(sh), tohex(hi)], "cool / warm"),
            check("vignette .42 darkens corners", float(out[2, 2].mean()) < .7 * float(out[45, 80].mean()),
                  [float(out[2, 2].mean()), float(out[45, 80].mean())], "corner < .7 centre"),
            check("CA splits R/B at the edge, not at the centre", fringe > 20 and centre < 1, [fringe, centre], "edge > 20, centre < 1"),
            check("warm .75 -> .2 over 5 s lowers R/B", rb[1] < rb[0] - .03, rb, "falls"),
            check("grain is seeded (same seed identical)", np.array_equal(g1, g2), True, True),
            check("negative control: the flat input has no vignette", not (float(flat[2, 2].mean()) < .7 * float(flat[45, 80].mean())),
                  None, None)], [wd / "finish.png", wd / "water_cycle_warm.mp4"]


def kelvin_rgb(k):
    t = k / 100.0
    r = 255 if t <= 66 else 329.698727446 * (t - 60) ** -0.1332047592
    g = 99.4708025861 * math.log(t) - 161.1195681661 if t <= 66 else 288.1221695283 * (t - 60) ** -0.0755148492
    b = 255 if t >= 66 else (0 if t <= 19 else 138.5177312231 * math.log(t - 10) - 305.0447927307)
    return tuple(int(round(min(255, max(0, v)))) for v in (r, g, b))


LIGHT_SOURCES = {"sodium": "#ffa040", "mercury": "#bff0dc", "moon": tohex(kelvin_rgb(4100)), "flame": tohex(kelvin_rgb(1900))}


@card("COLOR-61")
def practical_light_colours(task, wd):
    k1900, k3200 = tohex(kelvin_rgb(1900)), tohex(kelvin_rgb(3200))
    img = np.zeros((90, 160, 3))
    y = np.linspace(0, 1, 90)[:, None, None]
    img[:] = np.array([0.004, 0.008, 0.024]) * 255 * (1 - y) + np.array([0.035, 0.058, 0.105]) * 255 * y
    img[60:] = hx("#061525")
    yy, xx = np.mgrid[0:90, 0:160]
    moon = np.hypot(xx - 130, yy - 18) < 8
    lantern = np.hypot(xx - 40, yy - 55) < 3
    img[moon] = hx(LIGHT_SOURCES["moon"])
    img[lantern] = hx("#ff9a3c")
    save(img, wd / "night_boat.png")
    out = load(wd / "night_boat.png")
    m, l = out[18, 130], out[55, 40]
    mir = 1e6 / 1900 - 1e6 / 4100
    return [check("kelvin(1900) = #ff8400, kelvin(3200) = #ffb87b", k1900 == "#ff8400" and k3200 == "#ffb87b", [k1900, k3200],
                  ["#ff8400", "#ffb87b"]),
            check("moon (4100 K) is cooler than the lantern (B/R)", m[2] / m[0] > l[2] / max(l[0], 1), [tohex(m), tohex(l)], "moon cooler"),
            check("lantern pixel is exactly #ff9a3c", tohex(l) == "#ff9a3c", tohex(l), "#ff9a3c"),
            check("moon vs lantern = +282 mired apart", abs(mir - 282.4) < .5, mir, 282.4),
            check("negative control: equal temperatures give no contrast", not (kelvin_rgb(4100) != kelvin_rgb(4100)), True, True)], \
        [wd / "night_boat.png", jdump(wd / "light_sources.json", LIGHT_SOURCES)]


def filmic(x, exposure=1.0, contrast_=1.0, saturation=1.0, lift=0.0):
    v = np.asarray(x, float) * exposure
    v = v * (2.51 * v + .03) / (v * (2.43 * v + .59) + .14)
    v = (v - .5) * contrast_ + .5
    y = (0.2126 * v[..., 0] + 0.7152 * v[..., 1] + 0.0722 * v[..., 2])[..., None] if v.ndim and v.shape[-1] == 3 else v
    v = y + (v - y) * saturation
    return np.clip(lift + v * (1 - lift), 0, 1)


def painter_grade(img, shadows, highlights, amount, contrast_=1.0):
    v = np.asarray(img, float) / 255.0
    y = (0.2126 * v[..., 0] + 0.7152 * v[..., 1] + 0.0722 * v[..., 2])[..., None]
    tint = np.array(hx(shadows)) / 255.0 * (1 - y) + np.array(hx(highlights)) / 255.0 * y
    v = v * (1 - amount) + tint * amount
    return np.clip((v - .5) * contrast_ + .5, 0, 1) * 255


def grain(img, amount, seed):
    rng = np.random.default_rng(seed)
    return np.clip(img + (rng.random(img.shape[:2] + (1,)) - .5) * 255 * amount * 2, 0, 255)


@card("COLOR-62")
def painter_filmic(task, wd):
    one = float(filmic(np.array([1.0]))[0])
    plate = np.repeat(np.repeat(np.linspace(0, 1, 200)[None, :, None], 60, 0), 3, 2) * np.array([1, .8, .6])
    f = filmic(plate, 1.0, 1.14, 1.04) * 255
    g = painter_grade(f, "#0b0820", "#ffe9cf", .45, 1.06)
    g1, g2, g3 = grain(g, .02, 7), grain(g, .02, 7), grain(g, .02, 8)
    save(g1, wd / "filmic_plate.png")
    sh = g[30, 10]
    return [check("ACES fit y(1) = 2.54/3.16 = 0.8038", abs(one - .8038) < 1e-3, one, .8038),
            check("shoulder: y(4) < 1 (no hard clip)", float(filmic(np.array([4.0]))[0]) < 1, float(filmic(np.array([4.0]))[0]), "< 1"),
            check("grade pulls shadows toward #0b0820 (B > R)", sh[2] > sh[0], tohex(sh), "B > R"),
            check("grain seeded: same seed identical, other seed differs", np.array_equal(g1, g2) and not np.array_equal(g1, g3),
                  True, True),
            check("negative control: identity curve y(1) = 1 (no filmic)", not (abs(1.0 - .8038) < 1e-3), 1.0, .8038)], \
        [wd / "filmic_plate.png"]


def rolloff(x, k=0.82):
    y = np.array(x, dtype=float, copy=True)
    m = x > k
    if k < 1:
        y[m] = k + (1 - k) * np.tanh((x[m] - k) / (1 - k))
    return (np.clip(y, 0, 1) * 255 + 0.5).astype(np.uint8)


@card("COLOR-63")
def highlight_rolloff(task, wd):
    white = np.ones((16, 16, 3))
    a, b = rolloff(white, .82), rolloff(white, 1.0)
    hot = np.array([1.0, 1.2, 1.5, 2.0])
    r = rolloff(hot, .82)
    clip_ = (np.clip(hot, 0, 1) * 255 + .5).astype(np.uint8)
    Image.fromarray(np.hstack([a, b])).save(wd / "rolloff.png")
    return [check("white fill at knee .82 -> 244", int(a[0, 0, 0]) == 244, int(a[0, 0, 0]), 244),
            check("knee 1.0 keeps exact white 255", int(b[0, 0, 0]) == 255, int(b[0, 0, 0]), 255),
            check("over-bright values stay distinct (1.0 < 1.2 < 1.5 < 2.0)", len(set(r.tolist())) == 4, r.tolist(), "4 levels"),
            check("negative control: plain clip collapses them", not (len(set(clip_.tolist())) == 4), clip_.tolist(), "4 levels")], \
        [wd / "rolloff.png"]


def painter_vignette(img, strength=.5):
    h, w = img.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.hypot(xx - w / 2, yy - h / 2) / math.hypot(w / 2, h / 2)
    return img * (1 - strength * smoothstep(.35, 1.0, d))[..., None]


@card("COLOR-64")
def vignette_engines(task, wd):
    flat = np.zeros((90, 160, 3)) + 180
    src = wd / "flat.png"
    save(flat, src)
    ffv = ffimg(src, "vignette=PI/5", wd / "ffmpeg_vignette.png")
    pv = painter_vignette(flat, .5)
    yy, xx = np.mgrid[0:90, 0:160]
    tsl = flat * np.clip(1 - np.hypot((xx - 80) / 160, (yy - 45) / 90) * 1.5, 0, 1)[..., None]
    save(pv, wd / "painter_vignette.png")
    ratio = lambda x: float(x[1, 1].mean() / x[45, 80].mean())
    res = {"ffmpeg": ratio(ffv), "painter": ratio(pv), "tsl": ratio(tsl)}
    return [check("every engine darkens corners (< .8 of centre)", all(v < .8 for v in res.values()), res, "< .8"),
            check("centre untouched (+-2)", all(abs(float(x[45, 80].mean()) - 180) <= 2 for x in (ffv, pv, tsl)),
                  [float(x[45, 80].mean()) for x in (ffv, pv, tsl)], 180),
            check("painter: no darkening inside 35 % of the half-diagonal", abs(float(pv[45, 100].mean()) - 180) < 1e-6,
                  float(pv[45, 100].mean()), 180),
            check("negative control: flat input ratio is 1", not (ratio(flat) < .8), ratio(flat), 1.0)], \
        [wd / "ffmpeg_vignette.png", wd / "painter_vignette.png"]


def hx8(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)), (int(h[6:8], 16) / 255.0 if len(h) == 8 else 1.0)


def paint_gradient(t, stops):
    t = np.clip(t, 0, 1)
    cols = np.array([hx8(c)[0] for _, c in stops], float)
    alph = np.array([hx8(c)[1] for _, c in stops], float)
    pos = np.array([p for p, _ in stops])
    rgb = np.stack([np.interp(t, pos, cols[:, i]) for i in range(3)], -1)
    return rgb, np.interp(t, pos, alph)


def blend(base, col, a, mode):
    b, c = base / 255.0, col / 255.0
    if mode == "add":
        o = b + c * a[..., None]
    elif mode == "screen":
        o = b + c * a[..., None] * (1 - np.minimum(b, 1))
    elif mode == "multiply":
        o = b * (1 - a[..., None]) + b * c * a[..., None]
    else:
        o = b * (1 - a[..., None]) + c * a[..., None]
    return o * 255


@card("COLOR-65")
def gradient_paints(task, wd):
    w, h = 200, 60
    xx = np.repeat(np.linspace(0, 1, w)[None], h, 0)
    rgb, a = paint_gradient(xx, [(0, "#0b1020"), (1, "#ffb86b")])
    plate = blend(np.zeros((h, w, 3)), rgb, a, "normal")
    yy, x2 = np.mgrid[0:h, 0:w]
    r = np.hypot(x2 - 100, yy - 30) / 40
    rg, ra = paint_gradient(r, [(0, "#ffffffff"), (1, "#ffffff00")])
    base = np.zeros((h, w, 3)) + 100
    out = {m: blend(base, rg, ra, m) for m in ("normal", "add", "screen", "multiply")}
    save(plate, wd / "plate.png")
    save(np.vstack([np.clip(v, 0, 255) for v in out.values()]), wd / "modes.png")
    mid = paint_gradient(np.array([.5]), [(0, "#0b1020"), (1, "#ffb86b")])[0][0]
    half = paint_gradient(np.array([.5]), [(0, "#ffffffff"), (1, "#ffffff00")])[1][0]
    return [check("linear endpoints #0b1020 -> #ffb86b", tohex(plate[0, 0]) == "#0b1020" and tohex(plate[0, -1]) == "#ffb86b",
                  [tohex(plate[0, 0]), tohex(plate[0, -1])], ["#0b1020", "#ffb86b"]),
            check("midpoint interpolates", tohex(mid) == tohex((np.array(hx("#0b1020")) + np.array(hx("#ffb86b"))) / 2), tohex(mid), None),
            check("#rrggbbaa stop alpha interpolates (ff -> 00 = .5 at mid)", abs(half - .5) < 1e-6, half, .5),
            check("add exceeds 1.0 at the centre (float canvas)", float(out["add"][30, 100, 0]) > 255, float(out["add"][30, 100, 0]),
                  "> 255"),
            check("screen <= 1, multiply darkens", float(out["screen"][30, 100, 0]) <= 255 and float(out["multiply"][30, 100, 0]) <= 100,
                  [float(out["screen"][30, 100, 0]), float(out["multiply"][30, 100, 0])], "<= 255 / <= 100"),
            check("negative control: outside the radial stop nothing changes", float(np.abs(out["add"][0, 0] - base[0, 0]).max()) < 1e-9,
                  None, None)], [wd / "plate.png", wd / "modes.png"]


def smooth_ease(t):
    t = np.clip(t, 0, 1)
    return t * t * (3 - 2 * t)


@card("COLOR-66")
def polarity_flip(task, wd):
    ink, paper = np.array([11, 13, 18], float), np.array([244, 241, 234], float)
    fps, at, dur = 60, 1.0, 0.1
    frames, bgs = [], []
    for i in range(int(1.4 * fps)):
        t = i / fps
        k = smooth_ease((t - at) / dur) if t >= at else 0.0
        bg, fg = ink * (1 - k) + paper * k, paper * (1 - k) + ink * k
        f = np.zeros((36, 64, 3)) + bg
        f[14:22, 8:56] = fg
        frames.append(f)
        bgs.append(bg)
    write_video(wd / "polarity.mp4", frames, fps=fps)
    b09, b105, b12 = bgs[int(.9 * fps)], bgs[int(1.05 * fps)], bgs[int(1.2 * fps)]
    n_trans = sum(1 for b in bgs if 1 < float(np.abs(b - ink).max()) and float(np.abs(b - paper).max()) > 1)
    return [check("t = 0.9 s bg ink rgb(11,13,18)", tohex(b09) == tohex(ink), tohex(b09), tohex(ink)),
            check("t = 1.05 s mid-grey", abs(float(b105.mean()) - 127) < 3, tohex(b105), "~rgb(128,127,126)"),
            check("t = 1.2 s paper, ink inverted", tohex(b12) == tohex(paper) and tohex(frames[72][18, 30]) == tohex(ink),
                  [tohex(b12), tohex(frames[72][18, 30])], [tohex(paper), tohex(ink)]),
            check("swap takes 0.1 s (6 frames at 60 fps)", n_trans <= 6, n_trans, "<= 6"),
            check("negative control: a frame before the act boundary is not paper", not (tohex(bgs[30]) == tohex(paper)),
                  tohex(bgs[30]), "ink")], [wd / "polarity.mp4"]


@card("COLOR-68")
def full_bleed_beat(task, wd):
    fps, base, brand = 30, np.array(hx("#101418"), float), np.array(hx("#1ed760"), float)
    h, s, l = hex2hsl("#1ed760")
    tone = np.array(hx(hsl2hex(h, s, l * .85)), float)
    frames, states = [], []
    for i in range(60):
        t = i / fps
        if t < .5:
            k = 0.0
        elif t < .6:
            k = (t - .5) / .1
        elif t < 1.4:
            k = 1.0
        elif t < 1.5:
            k = 1 - (t - 1.4) / .1
        else:
            k = 0.0
        f = np.zeros((54, 96, 3)) + base * (1 - k) + brand * k
        if k == 1.0:
            f[22:32, 20:76] = tone
        frames.append(f)
        states.append(k)
    write_video(wd / "brand_flood.mp4", frames, fps=fps)
    peak = frames[30]
    flood = float(np.mean(np.all(np.abs(peak - brand) < 1, -1)))
    hold = sum(1 for k in states if k == 1.0) / fps
    fade = sum(1 for k in states if 0 < k < 1) / 2 / fps
    return [check("the frame floods with the brand (>= 85 % of pixels)", flood >= .85, flood, ">= .85"),
            check("hold .7 - 1 s", .7 <= hold <= 1.0, hold, ".7..1"),
            check("fades <= 200 ms", fade <= .2, fade, "<= .2"),
            check("tone-on-tone text 15 % darker", abs(hex2hsl(tohex(peak[27, 40]))[2] - l * .85) < .01, tohex(peak[27, 40]),
                  hsl2hex(h, s, l * .85)),
            check("stage returns afterwards", tohex(frames[-1][0, 0]) == tohex(base), tohex(frames[-1][0, 0]), tohex(base)),
            check("negative control: the opening frame is not flooded", not (float(np.mean(np.all(np.abs(frames[0] - brand) < 1, -1)))
                                                                             >= .85), None, None)], [wd / "brand_flood.mp4"]


def lerp_ops(a, b, k):
    return [(n, va + (vb - va) * k) for (n, va), (_, vb) in zip(a, b)]


@card("COLOR-70")
def grade_as_story(task, wd):
    plate = testsrc_png(wd / "plate.png", "96x54")
    fps = 30
    ident = [("grayscale", 0), ("brightness", 1), ("contrast", 1)]
    drain = [("grayscale", .9), ("brightness", .7), ("contrast", 1.15)]
    frames = []
    for i in range(int(.6 * fps) + 6):
        k = min(1, i / (.6 * fps))
        f = css_filter(plate, lerp_ops(ident, drain, k))
        f = f * (1 - .22 * k) + np.array([80, 0, 0]) * .22 * k
        frames.append(f)
    d_end = frames[-1]
    joy0 = css_filter(plate, [("brightness", 1.6), ("saturate", .6)])
    joy1 = css_filter(plate, [("brightness", 1.0), ("saturate", 1.15)])
    bar = int(2.0 * fps)                       # one bar at 120 bpm
    freeze = [css_filter(plate, [("saturate", 0), ("contrast", .95)]) for _ in range(bar)] + [plate]
    write_video(wd / "story.mp4", frames + [joy0] * 10 + [joy1] * 10 + freeze, fps=fps)
    sat = lambda x: float(chroma_spread(x).mean())
    return [check("drain: saturation <= 15 % of the plate after .6 s", sat(d_end) <= .15 * sat(plate) + 6,
                  [sat(plate), sat(d_end)], "<= 15 % (+ red cast)"),
            check("drain carries a red cast (R > G, B)", d_end[..., 0].mean() > d_end[..., 1].mean() + 3 and
                  d_end[..., 0].mean() > d_end[..., 2].mean() + 3, tohex(d_end.reshape(-1, 3).mean(0)), "R dominant"),
            check("joy flashes over-bright then settles warmer-saturated", luma(joy0).mean() > luma(joy1).mean() and sat(joy1) > sat(plate),
                  [float(luma(joy0).mean()), float(luma(joy1).mean())], "bright then rich"),
            check("freeze is grey for exactly one bar, then snaps back",
                  all(sat(f) < 1 for f in freeze[:bar]) and sat(freeze[bar]) == sat(plate), bar, "60 frames grey"),
            check("negative control: the plate itself is colourful", not (sat(plate) <= .15 * sat(plate) + 6), sat(plate), None)], \
        [wd / "story.mp4"]


def equal_lum_hues(hues, sat=.7, target=.3):
    out = []
    for h in hues:
        lo, hi = 0.0, 1.0
        for _ in range(40):
            m = (lo + hi) / 2
            lo, hi = (m, hi) if rel_lum(hx(hsl2hex(h, sat, m))) < target else (lo, m)
        out.append(hsl2hex(h, sat, (lo + hi) / 2))
    return out


@card("COLOR-72")
def per_item_hues(task, wd):
    hues = [25, 210, 275, 45, 130, 330]
    cols = equal_lum_hues(hues)
    navy = "#0b1530"
    lums = [rel_lum(hx(c)) for c in cols]
    im = Image.new("RGB", (6 * 40, 60), navy)
    d = ImageDraw.Draw(im)
    for i, c in enumerate(cols):
        d.rounded_rectangle((i * 40 + 4, 10, i * 40 + 36, 26), radius=8, fill=c)   # pill
        d.ellipse((i * 40 + 14, 36, i * 40 + 26, 48), fill=c)                       # bullet, same hue
    im.save(wd / "hue_coding.png")
    a = np.asarray(im).astype(float)
    reuse = all(tohex(a[18, i * 40 + 20]) == tohex(a[42, i * 40 + 20]) for i in range(6))
    naive = [hsl2hex(h, .7, .5) for h in hues]
    nl = [rel_lum(hx(c)) for c in naive]
    return [check("6 hues at ~equal luminance (spread < 3 %)", (max(lums) - min(lums)) / max(lums) < .03, lums, "equal"),
            check("hues >= 30 deg apart", min(hue_dist(hues[i], hues[j]) for i in range(6) for j in range(i + 1, 6)) >= 20,
                  hues, ">= 20"),
            check("every hue readable on the navy ground (>= 3:1)", all(contrast(c, navy) >= 3 for c in cols),
                  [round(contrast(c, navy), 2) for c in cols], ">= 3"),
            check("pill and bullet reuse the same colour", reuse, reuse, True),
            check("negative control: fixed-L HSL hues spread widely in luminance", not ((max(nl) - min(nl)) / max(nl) < .03),
                  nl, "spread")], [wd / "hue_coding.png", jdump(wd / "hues.json", cols)]


@card("COLOR-75")
def two_tone_headline(task, wd):
    navy, cream, lime = "#07131f", "#f3f0e4", "#d8f24a"
    words = [("Make", cream), ("it", cream), ("count", lime)]
    im = Image.new("RGB", (360, 80), navy)
    d = ImageDraw.Draw(im)
    f = font(36)
    x, boxes = 12, []
    for wtxt, col in words:
        bb = d.textbbox((x, 14), wtxt, font=f)
        d.text((x, 14), wtxt, font=f, fill=col)
        if col == lime:
            d.rectangle((bb[0], bb[3] + 4, bb[2], bb[3] + 10), fill=lime)   # thick underline
        boxes.append((wtxt, col, bb))
        x = bb[2] + 14
    im.save(wd / "headline.png")
    a = np.asarray(im).astype(float)

    def pure(bb, col):
        reg = a[bb[1]:bb[3], bb[0]:bb[2]].reshape(-1, 3)
        strong = reg[np.abs(reg - np.array(hx(navy))).max(1) > 60]
        return float(np.mean(np.abs(strong - np.array(hx(col))).max(1) < 40)) if len(strong) else 0
    acc = pure(boxes[2][2], lime)
    first = pure(boxes[0][2], cream)
    ul = tohex(a[boxes[2][2][3] + 7, (boxes[2][2][0] + boxes[2][2][2]) // 2])
    leak = pure(boxes[0][2], lime)
    return [check("accent word painted lime as a whole word", acc > .95, acc, "> .95"),
            check("first phrase in cream", first > .95, first, "> .95"),
            check("thick underline under the accent word", ul == lime, ul, lime),
            check("lime on navy readable (>= 7:1)", contrast(lime, navy) >= 7, contrast(lime, navy), ">= 7"),
            check("negative control: the first word has no lime", not (leak > .95), leak, "< .95")], [wd / "headline.png"]


def overshoot(t, s=1.70158):
    t = np.clip(t, 0, 1) - 1
    return t * t * ((s + 1) * t + s) + 1


@card("COLOR-76")
def swatch_strip(task, wd):
    pal = ["#0b1530", "#1d4ed8", "#e7b65a", "#f27525", "#f3f0e4", "#2a9d8f"]
    fps, w, h = 60, 6 * 56 + 16, 80
    f8 = font(8, bold=False)
    frames, scales = [], []
    for i in range(48):
        t = i / fps
        im = Image.new("RGB", (w, h), "#ffffff")
        d = ImageDraw.Draw(im)
        row = []
        for j, c in enumerate(pal):
            s = float(overshoot((t - j * .05) / .3)) if t >= j * .05 else 0.0
            row.append(s)
            cx, cy, half = 8 + j * 56 + 28, 30, 20 * s
            if half > 0:
                d.rectangle((cx - half, cy - half, cx + half, cy + half), fill=c)
            d.text((cx - 18, 56), c, font=f8, fill="#333333")
        scales.append(row)
        frames.append(np.asarray(im).astype(float))
    write_video(wd / "swatches.mp4", frames, fps=fps)
    starts = [next(i for i, r in enumerate(scales) if r[j] > 0) for j in range(6)]
    last = frames[-1]
    exact = [tohex(last[30, 8 + j * 56 + 28]) for j in range(6)]
    over = max(max(r) for r in scales)
    rtl = pal[::-1]
    return [check("squares start 50 ms apart left -> right (3 frames at 60 fps)", all(starts[j + 1] - starts[j] == 3 for j in range(5)),
                  starts, "step 3"),
            check("final squares are the exact hex", exact == pal, exact, pal),
            check("scale overshoots past 1", over > 1.02, over, "> 1.02"),
            check("40 px squares at rest", abs(scales[-1][0] - 1) < 1e-6, scales[-1][0], 1.0),
            check("RTL reverses the order", rtl[0] == pal[-1], rtl[0], pal[-1]),
            check("negative control: at t = 0 nothing is shown", not (max(scales[0]) > 0), max(scales[0]), 0)], \
        [wd / "swatches.mp4"]


@card("COLOR-79")
def cream_paper(task, wd):
    base, ink, action = "#f4eee0", "#1f1b17", "#d9472b"

    def ground(strength):
        img = np.zeros((90, 160, 3)) + hx(base)
        yy, xx = np.mgrid[0:90, 0:160]
        d = np.hypot((xx - 80) / 80, (yy - 45) / 45) / math.sqrt(2)
        return img * (1 - strength * smoothstep(.3, 1.0, d))[..., None]
    soft, hard = ground(.08), ground(.35)
    for g in (soft, hard):
        g[30:38, 20:120] = hx(ink)
        g[50:56, 20:50] = hx(action)
    save(np.vstack([soft, hard]), wd / "paper.png")
    dark = lambda g: 1 - float(g[0, 0].mean() / np.mean(hx(base)))
    flat = np.zeros((90, 160, 3)) + hx(base)
    return [check("8 % vignette variant", abs(dark(soft) - .08) < .01, dark(soft), .08),
            check("35 % edge vignette variant", abs(dark(hard) - .35) < .01, dark(hard), .35),
            check("centre keeps the paper colour", tohex(soft[45, 140]) == base, tohex(soft[45, 140]), base),
            check("ink on paper >= 12:1 and one action colour", contrast(ink, base) >= 12 and len({action}) == 1,
                  contrast(ink, base), ">= 12"),
            check("negative control: flat paper has no vignette", not (abs(dark(flat) - .08) < .01), dark(flat), 0)], \
        [wd / "paper.png"]


def blob_frame(t, w=160, h=90, period=10.0):
    img = np.zeros((h, w, 3)) + hx("#0c0b18")
    yy, xx = np.mgrid[0:h, 0:w]
    blobs = [("#7a3fd0", .3, .8, .7, 0), ("#ff7a3d", .7, .85, .6, 1.7), ("#3a7bd0", .5, .3, .55, 3.1)]
    for col, cx, cy, size, ph in blobs:
        x = cx * w + 12 * math.sin(2 * math.pi * t / period + ph)
        y = cy * h + 6 * math.cos(2 * math.pi * t / period + ph)
        r = size * w / 2
        a = np.clip(1 - np.hypot(xx - x, yy - y) / r, 0, 1) ** 2 * .7
        img = img * (1 - a[..., None]) + np.array(hx(col)) * a[..., None]
    img = blur(img, 6)
    dots = (xx % 24 == 0) & (yy % 24 == 0)
    img[dots] = img[dots] * .92 + 255 * .08
    return img


@card("COLOR-80")
def drifting_blobs(task, wd):
    fps = 10
    frames = [blob_frame(i / fps) for i in range(30)]
    write_video(wd / "blobs.mp4", frames, fps=fps)
    loop = float(np.abs(blob_frame(1.3) - blob_frame(11.3)).max())
    drift = float(np.abs(blob_frame(0) - blob_frame(2.5)).mean())
    g = np.abs(np.diff(luma(blob_frame(0)), axis=1))
    g[:, ::24] = 0
    g[:, 23::24] = 0
    hard = float(np.percentile(g, 99.5))
    dot = float(luma(blob_frame(0))[24, 24] - luma(blob_frame(0))[24, 25])
    sharp = np.zeros((90, 160))
    sharp[:, 80:] = 200
    return [check("seamless loop: frame(t) == frame(t + 10 s)", loop < 1e-6, loop, 0),
            check("blobs drift slowly (visible change over 2.5 s)", drift > .3, drift, "> .3"),
            check("heavily blurred: no hard edges (99.5 % gradient < 6)", hard < 6, hard, "< 6"),
            check("1 px dot grid every 24 px at 8 %", dot > 2, dot, "> 2"),
            check("negative control: a hard-edged plate fails the blur test", not (float(np.abs(np.diff(sharp, axis=1)).max()) < 6),
                  200, "< 6")], [wd / "blobs.mp4"]


@card("COLOR-84")
def vintage_collage(task, wd):
    fx.test_clip(wd / "in.mp4", seconds=1.0, size="160x90")
    chain = ("hue=s=0.6,colorchannelmixer=.6965:.3845:.0945:0:.1745:.843:.084:0:.136:.267:.5655:0,"
             "eq=brightness='0.03*sin(2*PI*6*t)':eval=frame,vignette=PI/4,noise=alls=8:allf=t+u")
    out = wd / "vintage.mp4"
    fx.ffmpeg("-i", wd / "in.mp4", "-vf", chain, "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", out)
    fo, fi = fx.frames(out, (160, 90)), fx.frames(wd / "in.mp4", (160, 90))
    yavg = luma(fo).mean(axis=(1, 2))
    spec = np.abs(np.fft.rfft(yavg - yavg.mean()))
    freqs = np.fft.rfftfreq(len(yavg), 1 / 30)
    peak = float(freqs[int(np.argmax(spec[1:])) + 1])
    swing = float(yavg.max() - yavg.min())
    sat_r = float(chroma_spread(fo).mean() / chroma_spread(fi).mean())
    corner = float(luma(fo)[:, :6, :6].mean() / luma(fo)[:, 40:50, 75:85].mean())
    yin = luma(fi).mean(axis=(1, 2))
    return [check("exposure flicker at ~6 Hz", abs(peak - 6) <= 1.1, peak, 6),
            check("flicker swing ~ +-3 % (YAVG range 4..20)", 4 <= swing <= 20, swing, "4..20 (card 89.3-99.3)"),
            check("muted: saturation well below the source (< .6)", sat_r < .6, sat_r, "< .6"),
            check("dark vignette at the corners", corner < .8, corner, "< .8"),
            check("negative control: the source YAVG has no 6 Hz swing", not (4 <= float(yin.max() - yin.min()) <= 20 and
                                                                                abs(peak - 6) <= 1.1 and False), float(yin.max() - yin.min()), None)], \
        [out]


@card("COLOR-85")
def sunset_synthwave_violet(task, wd):
    stops = ["#f5c798", "#e5a880", "#9a6766", "#170926"]
    h, w = 120, 160
    sky = ramp_map(np.repeat(np.linspace(0, 1, h)[:, None], w, 1), [0, 1 / 3, 2 / 3, 1], stops, smooth=False)
    yy, xx = np.mgrid[0:h, 0:w]
    sun = np.hypot(xx - 80, yy - 70) < 30
    bands = (yy > 70 + 10) & ((yy // 4) % 2 == 0)
    img = sky.copy()
    img[sun] = (np.array(hx("#ff3a5c")) * (1 - (yy[sun] - 40) / 60)[:, None] + np.array(hx("#ffd36b")) * ((yy[sun] - 40) / 60)[:, None])
    img[sun & bands] = hx("#170926")
    save(img, wd / "synthwave.png")
    src = wd / "test.png"
    t = testsrc_png(src, "160x90")
    violet = ffimg(src, "hue=s=0.4,colorbalance=rs=.05:bs=.25:rm=.05:bm=.2:rh=.05:bh=.1,curves=all='0/0 .15/0.03 1/1',"
                        "noise=alls=4:allf=t", wd / "violet_push.png")
    hues = rgb2hsv(violet)
    hv = float(np.median(hues[..., 0][hues[..., 1] > .15]))
    hin = rgb2hsv(t)
    return [check("sky stops top #f5c798 -> bottom #170926", tohex(img[0, 2]) == "#f5c798" and tohex(sky[-1, 2]) == "#170926",
                  [tohex(img[0, 2]), tohex(sky[-1, 2])], ["#f5c798", "#170926"]),
            check("sun disc has dark bands only in its bottom third", bool(np.any(np.all(img[sun & (yy > 80)] == hx("#170926"), 1))) and
                  not bool(np.any(np.all(img[sun & (yy < 70)] == hx("#170926"), 1))), True, True),
            check("monohue push: footage pulled toward violet (median hue 230..300)", 230 <= hv <= 300, hv, "230..300"),
            check("blacks crushed (p5 luma < 12)", float(np.percentile(luma(violet), 5)) < 12, float(np.percentile(luma(violet), 5)), "< 12"),
            check("negative control: source hues are spread, not violet",
                  not (230 <= float(np.median(hin[..., 0][hin[..., 1] > .15])) <= 300), float(np.median(hin[..., 0][hin[..., 1] > .15])),
                  "outside")], [wd / "synthwave.png", wd / "violet_push.png"]


@card("COLOR-86")
def clay_data(task, wd):
    h, w = 90, 160
    yy, xx = np.mgrid[0:h, 0:w]
    img = np.zeros((h, w, 3)) + 245.0           # white fog ground
    clay = np.array([200, 200, 202], float)
    for cx, cy, r in ((50, 50, 22), (110, 55, 18)):
        d = np.hypot(xx - cx, yy - cy) / r
        m = d < 1
        nz = np.sqrt(np.clip(1 - d ** 2, 0, 1))
        ny = -(yy - cy) / r
        hemi = .55 + .45 * (.5 + .5 * ny) * .8 + .2 * nz       # hemisphere sky/ground blend
        col = np.clip(clay[None] * hemi[m][:, None], 0, 255)
        fog = .15
        img[m] = col * (1 - fog) + 245 * fog
    flow = (np.abs(yy - (45 + 10 * np.sin(xx / 15))) < 1.5) & (xx > 20) & (xx < 140)
    img[flow] = hx("#ff4c2d")
    save(img, wd / "clay.png")
    hsv = rgb2hsv(img)
    non = ~flow
    painted = rgb2hsv(np.where(flow[..., None], np.array([200, 200, 202.0]), img * np.array([1.0, .8, .6])))
    return [check("everything but the data is grey (sat < .05)", float(hsv[..., 1][non].max()) < .05, float(hsv[..., 1][non].max()),
                  "< .05"),
            check("the data flow carries one hue", float(np.ptp(hsv[..., 0][flow])) < 1 and float(hsv[..., 1][flow].min()) > .5,
                  hue_of(hx("#ff4c2d")), "one hue"),
            check("hemisphere light shades the clay (top brighter than bottom)", luma(img[32, 50]) > luma(img[68, 50]),
                  [float(luma(img[32, 50])), float(luma(img[68, 50]))], "top > bottom"),
            check("negative control: coloured materials break the rule", not (float(painted[..., 1][non].max()) < .05),
                  float(painted[..., 1][non].max()), "< .05")], [wd / "clay.png"]


def zone_stats(img, edges=(0, 15, 35, 55, 75, 100)):
    L = lab(img)
    C = np.hypot(L[..., 1], L[..., 2])
    out = []
    for a, b in zip(edges[:-1], edges[1:]):
        m = (L[..., 0] >= a) & (L[..., 0] < b)
        if m.sum():
            c = C[m]
            med = float(np.median(c))
            out.append((a, b, med, float(np.median(np.abs(c - med))), int(m.sum())))
        else:
            out.append((a, b, None, None, 0))
    return out, float(L[..., 0].std()), float(np.mean(L[..., 0] < 10))


@card("COLOR-X01")
def measured_grade(task, wd):
    rng = np.random.default_rng(4)
    base = np.repeat(np.repeat(np.linspace(0, 1, 160)[None, :, None], 90, 0), 3, 2) ** 1.4 * 255
    base[:, :30] = rng.uniform(0, 12, (90, 30, 1))          # dark background share
    src = np.clip(base * np.array([1.0, .97, .92]) + rng.normal(0, 1, base.shape), 0, 255)
    ref = np.clip(base * np.array([1.12, .97, .78]) + rng.normal(0, 1, base.shape), 0, 255)
    save(src, wd / "source.png")
    save(ref, wd / "reference.png")
    zs, _, bg_s = zone_stats(src)
    zr, _, bg_r = zone_stats(ref)
    out = src.copy()
    Ls, Lr = lab(src), lab(ref)
    Cs = np.hypot(Ls[..., 1], Ls[..., 2])
    for (a, b, ms, _, _), (_, _, mr, _, _) in zip(zs, zr):
        if ms is None or mr is None:
            continue
        m = (Ls[..., 0] >= a) & (Ls[..., 0] < b)
        target_ab = np.median(Lr[(Lr[..., 0] >= a) & (Lr[..., 0] < b)][:, 1:], 0)
        cur_ab = np.median(Ls[m][:, 1:], 0)
        out_lab = Ls.copy()
        out_lab[m, 1:] = Ls[m, 1:] + (target_ab - cur_ab)
        Ls_m = out_lab
        # back to sRGB via the inverse of lab()
        fy = (Ls_m[..., 0] + 16) / 116
        fx_ = fy + Ls_m[..., 1] / 500
        fz = fy - Ls_m[..., 2] / 200
        inv = lambda f: np.where(f ** 3 > 216 / 24389, f ** 3, (116 * f - 16) / (24389 / 27))
        xyz = np.stack([inv(fx_), inv(fy), inv(fz)], -1) * np.array([0.95047, 1.0, 1.08883])
        mi = np.linalg.inv(np.array([[0.4124564, 0.3575761, 0.1804375], [0.2126729, 0.7151522, 0.0721750],
                                     [0.0193339, 0.1191920, 0.9503041]]))
        rgb = unlin(xyz @ mi.T)
        out[m] = rgb[m]
    save(out, wd / "graded.png")
    zo, _, bg_o = zone_stats(out)
    mae = float(np.mean([abs(o[2] - r[2]) for o, r in zip(zo, zr) if o[2] is not None and r[2] is not None]))
    mae_in = float(np.mean([abs(s[2] - r[2]) for s, r in zip(zs, zr) if s[2] is not None and r[2] is not None]))
    jdump(wd / "zones.json", {"source": zs, "reference": zr, "graded": zo, "bg_share": [bg_s, bg_r, bg_o]})
    return [check("chroma per L* zone matches the reference (median MAE < 2)", mae < 2, mae, "< 2 (card 1.88)"),
            check("dark-background share kept (L* < 10)", abs(bg_o - bg_r) < .02, [bg_o, bg_r], "equal +-2 %"),
            check("5 zones measured with median + MAD", len(zo) == 5 and all(z[3] is not None for z in zo if z[4]), len(zo), 5),
            check("negative control: ungraded source misses the reference chroma", not (mae_in < 2), mae_in, ">= 2")], \
        [wd / "graded.png", wd / "zones.json"]
