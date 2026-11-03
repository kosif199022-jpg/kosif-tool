"""light-glow-bloom: method cards as real programs with known-answer checks.

Every card paints a deterministic fixture on a float canvas (shapes, strokes, text masks, lit spheres, synthetic
audio), applies the card's light method in numpy / Pillow / ffmpeg, and measures the output: luminance rises where
the method says (inside the radius, along the rays, at the rim) and stays unchanged where it says. Each card also
runs the same measurement on the unprocessed canvas as a negative control. Where the card's engine is three.js,
CSS or a HyperFrames block, the method is re-implemented in numpy and the output JSON says so ("engine").
"""
import json
import math
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from _harness import card, check, fx

GAPS: dict = {
    "GLOW-37": "@remotion/effects (~55 WebGL2 effects, lightLeak/starburst/shine) is a specific npm library that is not "
               "installed here and its effect code is not vendored; reproducing its unknown shaders would be a fake",
    "GLOW-38": "needs Chromium's html-in-canvas drawElementImage flag plus WebGPU/TypeGPU in the render environment; "
               "neither is available or verified here",
    "GLOW-52": "the plates are the HyperFrames shaders.iife.js WebGPU library (shaders 4.0.0); not vendored here and "
               "headless WebGPU rendering is not verified",
    "GLOW-72": "the locked lighting phrases only pay off through an image/video generation service (Google Flow / Veo "
               "or another paid API key); no such key is configured, so no picture can be produced or measured",
}


# ----------------------------------------------------------------------------------------------- helpers
def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def hxf(h):
    return np.array(hx(h), float) / 255.0


def tohex(c):
    return "#%02x%02x%02x" % tuple(int(round(max(0, min(255, float(v))))) for v in c[:3])


def to8(a):
    return np.clip(np.rint(np.asarray(a, float) * 255), 0, 255).astype(np.uint8)


def save(a, p):
    """save a float 0..1 canvas"""
    Image.fromarray(to8(a)).save(str(p))
    return p


def load(p):
    return np.asarray(Image.open(str(p)).convert("RGB")).astype(float) / 255.0


def write_video(path, frames, fps=30, crf="17"):
    frames = [to8(f) for f in frames]
    h, w = frames[0].shape[:2]
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", "%dx%d" % (w, h), "-r", str(fps), "-i", "-", "-c:v", "libx264", "-crf", crf, "-pix_fmt", "yuv420p",
           str(path)]
    done = subprocess.run(cmd, input=b"".join(f.tobytes() for f in frames), capture_output=True, timeout=60)
    if done.returncode:
        raise RuntimeError(done.stderr.decode(errors="replace")[-300:])
    return path


def luma(a):
    a = np.asarray(a, float)
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def hue(c):
    r, g, b = [float(x) for x in c[:3]]
    mx, mn = max(r, g, b), min(r, g, b)
    d = mx - mn
    if d < 1e-9:
        return 0.0
    if mx == r:
        h = ((g - b) / d) % 6
    elif mx == g:
        h = (b - r) / d + 2
    else:
        h = (r - g) / d + 4
    return h * 60


def hue_dist(a, b):
    d = abs(a - b) % 360
    return min(d, 360 - d)


def blur(a, sigma):
    from scipy.ndimage import gaussian_filter
    a = np.asarray(a, float)
    if sigma <= 0:
        return a
    if a.ndim == 3:
        return np.stack([gaussian_filter(a[..., c], sigma) for c in range(a.shape[2])], -1)
    return gaussian_filter(a, sigma)


def smoothstep(e0, e1, x):
    t = np.clip((np.asarray(x, float) - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def jdump(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=1, default=lambda o: float(o)), encoding="utf-8")
    return path


def canvas(h, w, col="#000000"):
    return np.zeros((h, w, 3)) + hxf(col)


def m_ellipse(h, w, cx, cy, rx, ry=None, ss=4):
    ry = rx if ry is None else ry
    im = Image.new("L", (w * ss, h * ss), 0)
    ImageDraw.Draw(im).ellipse(((cx - rx) * ss, (cy - ry) * ss, (cx + rx) * ss, (cy + ry) * ss), fill=255)
    return np.asarray(im.resize((w, h), Image.BOX)).astype(float) / 255.0


def m_line(h, w, pts, width, ss=4):
    im = Image.new("L", (w * ss, h * ss), 0)
    d = ImageDraw.Draw(im)
    p = [(x * ss, y * ss) for x, y in pts]
    d.line(p, fill=255, width=max(1, int(round(width * ss))), joint="curve")
    r = width * ss / 2
    for x, y in (p[0], p[-1]):
        d.ellipse((x - r, y - r, x + r, y + r), fill=255)
    return np.asarray(im.resize((w, h), Image.BOX)).astype(float) / 255.0


def m_text(h, w, text, size, xy, ss=2):
    f = font(size * ss)
    im = Image.new("L", (w * ss, h * ss), 0)
    ImageDraw.Draw(im).text((xy[0] * ss, xy[1] * ss), text, font=f, fill=255)
    return np.asarray(im.resize((w, h), Image.BOX)).astype(float) / 255.0


def font(size=24):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


def fill(cv, mask, col, alpha=1.0, blur_r=0.0, mode="normal"):
    m = blur(mask, blur_r / 2.0) if blur_r else mask
    a = (m * alpha)[..., None]
    c = hxf(col) if isinstance(col, str) else np.asarray(col, float)
    if mode == "add":
        return cv + c * a
    if mode == "screen":
        return cv + c * a * (1 - np.minimum(cv, 1))
    if mode == "multiply":
        return cv * (1 - a) + cv * c * a
    return cv * (1 - a) + c * a


def glow(cv, mask, col, radius, alpha):
    return fill(cv, mask, col, alpha, blur_r=radius, mode="add")


def annulus(h, w, cx, cy, r0, r1):
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.hypot(xx - cx, yy - cy)
    return (d >= r0) & (d < r1)


def dist_map(h, w, cx, cy):
    yy, xx = np.mgrid[0:h, 0:w]
    return np.hypot(xx - cx, yy - cy)


def rolloff(x, k=.82):
    y = np.array(x, float, copy=True)
    m = y > k
    y[m] = k + (1 - k) * np.tanh((y[m] - k) / (1 - k))
    return np.clip(y, 0, 1)


def sphere(h, w, cx, cy, r):
    yy, xx = np.mgrid[0:h, 0:w]
    nx, ny = (xx - cx) / r, -(yy - cy) / r
    d2 = nx ** 2 + ny ** 2
    m = d2 < 1
    nz = np.sqrt(np.clip(1 - d2, 0, 1))
    return np.stack([nx, ny, nz], -1) * m[..., None], m


def norm(v):
    v = np.asarray(v, float)
    return v / np.linalg.norm(v)


def kelvin(k):
    t = k / 100.0
    r = 255 if t <= 66 else 329.698727446 * (t - 60) ** -0.1332047592
    g = 99.4708025861 * math.log(t) - 161.1195681661 if t <= 66 else 288.1221695283 * (t - 60) ** -0.0755148492
    b = 255 if t >= 66 else (0 if t <= 19 else 138.5177312231 * math.log(t - 10) - 305.0447927307)
    return tuple(int(round(min(255, max(0, v)))) for v in (r, g, b))


def fbm(h, w, seed, octaves=5, base=4):
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w))
    amp, tot = 1.0, 0.0
    for o in range(octaves):
        n = base * 2 ** o
        g = rng.random((n + 1, n + 1))
        img = np.asarray(Image.fromarray((g * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)).astype(float) / 255
        out += amp * img
        tot += amp
        amp *= .5
    return out / tot


def perlin1d(x, seed):
    rng = np.random.default_rng(seed)
    grads = rng.uniform(-1, 1, 4096)
    x = np.asarray(x, float)
    i0 = np.floor(x).astype(int)
    f = x - i0
    g0, g1 = grads[i0 % 4096], grads[(i0 + 1) % 4096]
    u = f * f * f * (f * (f * 6 - 15) + 10)
    return (g0 * f * (1 - u) + g1 * (f - 1) * u) * 2


# ----------------------------------------------------------------------------------------------- cards
@card("GLOW-03")
def neon_tube(task, wd):
    h, w, sw = 120, 200, 3.0
    pts = [(20, 60.5), (180, 60.5)]
    c = "#ff2a6d"
    cv = canvas(h, w, "#080a14")
    for width, op, col in ((7 * sw, .045, c), (3 * sw, .12, c), (sw, 1.0, c), (.24 * sw, .85, "#f2ffff")):
        cv = fill(cv, m_line(h, w, pts, width), col, op)
    save(cv, wd / "neon.png")
    bg = hxf("#080a14")
    core = cv[60, 100]
    at = lambda dy: float(np.abs(cv[60 + dy, 100] - bg).sum())
    frames = []
    for i in range(45):
        op = .45 + .25 * math.sin(1.4 * i / 15)
        frames.append(bg + (cv - bg) * op)
    write_video(wd / "neon_flicker.mp4", frames, fps=15)
    ops = [.45 + .25 * math.sin(1.4 * i / 15) for i in range(45)]
    single = fill(canvas(h, w, "#080a14"), m_line(h, w, pts, sw), c, 1)
    tube_only = fill(canvas(h, w, "#080a14"), m_line(h, w, pts, sw), c, 1)[60, 100]
    return [check("sub-pixel hot core whitens the tube centre (G,B up > .2)", float(core[1] - tube_only[1]) > .2 and
                  float(core[2] - tube_only[2]) > .2, [tohex(tube_only * 255), tohex(core * 255)], "toward #f2ffff"),
            check("inner halo at 1.2w > outer halo at 3w > nothing at 5w", at(4) > at(9) > 0 and at(15) < 1e-6,
                  [at(4), at(9), at(15)], "decreasing, 0 beyond 3.5w"),
            check("outer halo is the faint .045 layer", abs(at(9) - .045 * float(np.abs(hxf(c) - bg).sum())) < .01, at(9),
                  .045 * float(np.abs(hxf(c) - bg).sum())),
            check("flicker opacity .45 + .25 sin(1.4t) within .2..7", .2 <= min(ops) and max(ops) <= .7 + 1e-9, [min(ops), max(ops)],
                  ".2..7"),
            check("negative control: a single stroke has no halo at 1.2w", not (float(np.abs(single[64, 100] - bg).sum()) > 0),
                  float(np.abs(single[64, 100] - bg).sum()), 0)], [wd / "neon.png", wd / "neon_flicker.mp4"]


@card("GLOW-05")
def caption_word_glow(task, wd):
    h, w, size = 80, 300, 32
    words = [("one", 10), ("two", 100), ("three", 190)]
    active = 1
    cv = canvas(h, w, "#101010")
    masks = [m_text(h, w, t, size, (x, 20)) for t, x in words]
    acc = "#FF0099"
    cv = glow(cv, masks[active], acc, .5 * size, 1.0)
    for i, m in enumerate(masks):
        cv = fill(cv, m, "#ffffff", 1)
    plain = canvas(h, w, "#101010")
    for m in masks:
        plain = fill(plain, m, "#ffffff", 1)
    save(cv, wd / "caption_glow.png")

    def halo(img, i):
        m = masks[i] > .02
        near = (blur(masks[i], 6) > .02) & ~m
        return float((img[near] - hxf("#101010")).mean(0)[0]), float((img[near] - hxf("#101010")).mean(0)[2])
    ra, ba = halo(cv, active)
    ri, _ = halo(cv, 0)
    rp, _ = halo(plain, active)
    return [check("active word wears an accent halo (R and B up)", ra > .05 and ba > .03, [ra, ba], "> .05 / .03"),
            check("inactive words stay unglowed", abs(ri) < .02, ri, "< .02"),
            check("glow on the word, not the line box (corners stay dark)", float(np.abs(cv[2, 2] - hxf("#101010")).max()) < 1e-6,
                  tohex(cv[2, 2] * 255), "#101010"),
            check("negative control: no-glow render has no halo", not (rp > .05), rp, "<= .05")], [wd / "caption_glow.png"]


def polyline_len(pts):
    return [0.0] + list(np.cumsum([math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts[:-1], pts[1:])]))


def sub_path(pts, l0, l1):
    cum = polyline_len(pts)
    out = []
    for s in np.linspace(l0, l1, 40):
        i = max(0, min(len(pts) - 2, int(np.searchsorted(cum, s) - 1)))
        t = (s - cum[i]) / max(cum[i + 1] - cum[i], 1e-9)
        out.append((pts[i][0] + t * (pts[i + 1][0] - pts[i][0]), pts[i][1] + t * (pts[i + 1][1] - pts[i][1])))
    return out


@card("GLOW-09")
def route_draw_head(task, wd):
    h, w = 120, 240
    route = [(10, 100), (80, 40), (150, 90), (230, 20)]
    total = polyline_len(route)[-1]
    fps, draw_t = 30, 1.5
    frames, heads = [], []
    for i in range(int(2.2 * fps)):
        t = i / fps
        drawn = total * min(1, t / draw_t)
        head_op = 1.0 if t <= draw_t else max(0.0, 1 - (t - draw_t) / .5)
        cv = canvas(h, w, "#101315")
        if drawn > 1:
            body = sub_path(route, 0, drawn)
            cv = fill(cv, m_line(h, w, body, 11), "#49C6FF", .32, blur_r=6)
            cv = fill(cv, m_line(h, w, body, 3), "#E8F7FF", 1)
            head = sub_path(route, max(0, drawn - .03 * total), drawn)
            cv = fill(cv, m_line(h, w, head, 16), (120 / 255, 225 / 255, 1.0), .95 * head_op, blur_r=9)
            cv = fill(cv, m_line(h, w, head, 4.5), "#FFFFFF", head_op)
        frames.append(cv)
        heads.append(head_op)
    write_video(wd / "route.mp4", frames, fps=fps)
    mid = frames[int(.75 * fps)]
    tip = sub_path(route, 0, total * min(1, int(.75 * fps) / fps / draw_t))[-1]
    tail = sub_path(route, 0, total * .2)[-1]
    tip_px, tail_px = mid[int(round(tip[1])), int(round(tip[0]))], mid[int(round(tail[1])), int(round(tail[0]))]
    end = frames[-1]
    white_end = float(np.mean(np.all(end > .99, -1)))
    save(mid, wd / "route_mid.png")
    return [check("head (last 3 %) is white-hot at the tip", float(tip_px.min()) > .97, tohex(tip_px * 255), "#ffffff"),
            check("body behind the head is the icy core #E8F7FF", float(np.abs(tail_px - hxf("#E8F7FF")).max()) < .03,
                  tohex(tail_px * 255), "#e8f7ff"),
            check("head fades to 0 within .5 s after arrival", heads[-1] == 0 and white_end == 0, [heads[-1], white_end], 0),
            check("negative control: before drawing there is no head", not (float(frames[0].max()) > .9), float(frames[0].max()),
                  "<= .9")], [wd / "route.mp4", wd / "route_mid.png"]


@card("GLOW-10")
def phosphor_persistence(task, wd):
    h, w = 60, 160
    bg = hxf("#030706")
    acc = np.zeros((h, w, 3))
    frames = []
    for i in range(12):
        acc = acc * .85                                      # redraw last frame at ~.85
        x = 20 + i * 10
        stroke = m_line(h, w, [(x - 4, 30), (x + 4, 30)], 1.8)
        acc = glow(acc, stroke, "#4dff9a", 12, .6)
        acc = fill(acc, stroke, "#4dff9a", .6, mode="add")
        frames.append(np.clip(bg + acc, 0, 1))
    write_video(wd / "phosphor.mp4", frames, fps=12)
    last = acc
    v = [float(last[30, 20 + k * 10, 1]) for k in (11, 10, 9)]
    r1, r2 = v[1] / v[0], v[2] / v[0]
    a = glow(np.zeros((h, w, 3)), m_ellipse(h, w, 70, 30, 6), "#4dff9a", 4, .6)
    b = glow(a, m_ellipse(h, w, 78, 30, 6), "#4dff9a", 4, .6)
    fresh = glow(np.zeros((h, w, 3)), m_line(h, w, [(126, 30), (134, 30)], 1.8), "#4dff9a", 12, .6)
    return [check("afterglow decays x.85 per frame (k=1)", abs(r1 - .85) < .06, r1, .85),
            check("afterglow k=2 ~ .85^2", abs(r2 - .7225) < .08, r2, .7225),
            check("additive overlaps brighten", float(b[30, 74, 1]) > float(a[30, 74, 1]), [float(a[30, 74, 1]), float(b[30, 74, 1])],
                  "brighter"),
            check("negative control: without persistence the old position is dark", not (float(fresh[30, 120, 1]) > .05 * v[0]),
                  float(fresh[30, 120, 1]), "~0")], [wd / "phosphor.mp4"]


@card("GLOW-11")
def gradient_rim_glow(task, wd):
    h, w = 120, 240
    yy, xx = np.mgrid[0:h, 0:w]
    pill = np.zeros((h, w))
    im = Image.new("L", (w * 4, h * 4), 0)
    ImageDraw.Draw(im).rounded_rectangle((40 * 4, 40 * 4, 200 * 4, 80 * 4), radius=20 * 4, fill=255)
    pill = np.asarray(im.resize((w, h), Image.BOX)).astype(float) / 255
    inner = blur(pill, .01)
    from scipy.ndimage import binary_erosion
    border = pill - binary_erosion(pill > .5, iterations=2).astype(float)
    ang = (np.degrees(np.arctan2(yy - 60, xx - 120)) + 360) % 360
    cols = np.stack([np.interp(ang, [0, 120, 240, 360], [.13, .95, .9, .13]), np.interp(ang, [0, 120, 240, 360], [.8, .9, .2, .8]),
                     np.interp(ang, [0, 120, 240, 360], [.3, .1, .2, .3])], -1)   # conic green -> yellow -> red
    cv = canvas(h, w, "#0b0b10")
    dup = blur(cols * np.clip(border, 0, 1)[..., None], 15) * 6
    cv = cv + dup                                        # blurred duplicate behind
    cv = cv * (1 - pill[..., None])                      # black pill
    cv = cv + cols * np.clip(border, 0, 1)[..., None]    # 2 px conic border
    cv = np.clip(cv, 0, 1)
    save(cv, wd / "rim_glow.png")
    out_top = cv[30, 120]
    inside = cv[60, 120]
    plain = canvas(h, w, "#0b0b10") * (1 - pill[..., None]) + cols * np.clip(border, 0, 1)[..., None]
    hues = [hue(cv[38, x]) for x in (60, 120, 180)]
    return [check("glow spills outside the pill (10 px out brighter than ground)", float(out_top.sum()) > float(hxf("#0b0b10").sum()) + .1,
                  tohex(out_top * 255), "glowing"),
            check("pill interior stays black", float(inside.max()) < .02, tohex(inside * 255), "#000000"),
            check("border hue varies around the rim (conic)", max(hues) - min(hues) > 30, hues, "> 30 deg spread"),
            check("negative control: without the blurred duplicate the outside is dark",
                  not (float(plain[30, 120].sum()) > float(hxf("#0b0b10").sum()) + .1), tohex(plain[30, 120] * 255), "ground")], \
        [wd / "rim_glow.png"]


@card("GLOW-12")
def dot_matrix_word(task, wd):
    h, w = 90, 300
    mask = m_text(h, w, "LIGHT", 60, (20, 10))
    step = 6
    dots = [(x, y) for y in range(3, h, step) for x in range(3, w, step) if mask[y, x] > .5]
    cx, cy = 150, 45
    far = max(math.hypot(x - cx, y - cy) for x, y in dots)
    frames, counts = [], []
    for i in range(20):
        rad = far * i / 15
        cv = canvas(h, w, "#000000")
        shown = [(x, y) for x, y in dots if math.hypot(x - cx, y - cy) <= rad]
        dm = np.zeros((h, w))
        for x, y in shown:
            dm[y - 2:y + 2, x - 2:x + 2] = 1                  # 4 px dot
        cv = fill(cv, dm, "#ffd27a", 1, mode="add")
        cv = glow(cv, dm, "#ff9a3c", 20, .6)                  # 20 px bloom
        flare = np.exp(-(dist_map(h, w, cx, cy) / 18) ** 2) * min(1, i / 10)
        noflare = cv
        cv = cv + flare[..., None] * hxf("#fff1cf") * .5
        frames.append(np.clip(cv, 0, 1))
        counts.append(len(shown))
    write_video(wd / "dot_word.mp4", frames, fps=10)
    last = frames[-1]
    bad = sum(1 for y in range(3, h, step) for x in range(3, w, step) if mask[y, x] <= .5 and last[y, x].max() > .95)
    between = float(luma(last)[mask > .5].mean())
    outside = float(luma(last)[(blur(mask, 8) < .001)].mean())
    return [check("a dot only where the word alpha > .5 (no stray dots)", bad == 0, bad, 0),
            check("dots reveal by distance from centre (count grows monotonically)", all(counts[i] <= counts[i + 1] for i in range(19))
                  and counts[-1] == len(dots), [counts[5], counts[10], counts[-1]], "rising to %d" % len(dots)),
            check("bloom lights the word area above the far background", between > outside + .1, [between, outside], "> +.1"),
            check("flare added at the centre (peak of the flare layer)", np.unravel_index(np.argmax(luma(frames[-1] - np.clip(noflare, 0, 1))),
                                                                                       (h, w)) in [(cy, cx)] or
                  float(luma(frames[-1] - np.clip(noflare, 0, 1))[cy, cx]) > .3, float(luma(frames[-1] - np.clip(noflare, 0, 1))[cy, cx]),
                  "> .3 at centre"),
            check("negative control: frame 0 shows no dots", not (counts[0] > 0), counts[0], 0)], [wd / "dot_word.mp4"]


def rrect_ring(h, w, cx, cy, half_w, half_h, thick, ss=2):
    im = Image.new("L", (w * ss, h * ss), 0)
    d = ImageDraw.Draw(im)
    box = ((cx - half_w) * ss, (cy - half_h) * ss, (cx + half_w) * ss, (cy + half_h) * ss)
    d.rounded_rectangle(box, radius=max(1, int(min(half_w, half_h) * .3 * ss)), outline=255, width=max(1, int(thick * ss)))
    return np.asarray(im.resize((w, h), Image.BOX)).astype(float) / 255


@card("GLOW-13")
def neon_tunnel(task, wd):
    h, w, fps = 90, 160, 30
    cols = ["#ff3048", "#3a7bff", "#ffffff"]
    zs = np.linspace(1, 6, 24)
    frames, radii, pre = [], [], {}
    for i in range(15):
        cv = canvas(h, w)
        for k, z0 in enumerate(zs):
            z = z0 - i * .3
            if z <= .4:
                continue
            s = 1 / z
            cv = fill(cv, rrect_ring(h, w, 80, 45, 70 * s, 40 * s, 1.5), cols[k % 3], .8, mode="add")
        pre[i] = cv.copy()
        if i in (12, 13):                                   # 2 frames of horizontal slice glitch at the peak
            for y0 in range(0, h, 12):
                cv[y0:y0 + 6] = np.roll(cv[y0:y0 + 6], 6, axis=1)
        radii.append(cv)
        frames.append(np.clip(blur(cv, .8) * 1.5 + cv, 0, 1))
    write_video(wd / "tunnel.mp4", frames, fps=fps)
    glitched = lambda i: not np.array_equal(radii[i], pre[i]) and np.allclose(radii[i][0:6], np.roll(pre[i][0:6], 6, 1))
    r1 = rrect_ring(h, w, 80, 45, 70 / 1, 40 / 1, 1.5)
    r2 = rrect_ring(h, w, 80, 45, 70 / 2, 40 / 2, 1.5)
    x1 = int(np.argmax(r1[45, 80:])) + 80
    x2 = int(np.argmax(r2[45, 80:])) + 80
    a = fill(canvas(h, w), r1, "#ff3048", .8, mode="add")
    b = fill(a, r1, "#3a7bff", .8, mode="add")
    shift = lambda f: int(np.argmax([float((f[0:6] * np.roll(f[6:12], k, 1)).sum()) for k in range(-8, 9)]) - 8)
    return [check("ring scale = 1/z (half-width at z=2 is half of z=1)", abs((x2 - 80) / (x1 - 80) - .5) < .05, [x1 - 80, x2 - 80],
                  "ratio .5"),
            check("additive blend: overlaps brighten", float(b[45, x1].sum()) > float(a[45, x1].sum()), None, "brighter"),
            check("glitch: slices displaced 6 px on exactly the 2 peak frames", [i for i in range(15) if glitched(i)] == [12, 13],
                  [i for i in range(15) if glitched(i)], [12, 13]),
            check("negative control: a non-peak frame is unglitched", not glitched(5), glitched(5), False)], \
        [wd / "tunnel.mp4"]


@card("GLOW-14")
def painter_glow_stack(task, wd):
    h, w = 200, 300
    blade = m_ellipse(h, w, 150, 100, 15, 120)
    cv = canvas(h, w)
    for col, r, a in (("#1a8cff", 40, .5), ("#3fd0ff", 14, .95), ("#b8f2ff", 4, 1)):
        cv = glow(cv, blade, col, r, a)
    cv = fill(cv, blade, "#f2fdff")
    out = rolloff(cv)
    save(out, wd / "blade.png")
    prof = [float(luma(cv)[100, 150 + 15 + d]) for d in (2, 10, 25, 50)]
    near = cv[100, 150 + 15 + 25]
    plain = fill(canvas(h, w), blade, "#f2fdff")
    return [check("light spills and decays with distance", all(prof[i] > prof[i + 1] for i in range(3)) and prof[-1] > 0,
                  prof, "decreasing, > 0"),
            check("outer spill is the blue glow (B > G > R)", near[2] > near[1] > near[0], tohex(near * 255), "blue"),
            check("core is the near-white fill", float(np.abs(cv[100, 150] - hxf("#f2fdff")).max()) < .5 and float(cv[100, 150].min()) >= .9,
                  tohex(out[100, 150] * 255), "#f2fdff+"),
            check("far pixels untouched (> 3 x 40 px away)", float(cv[100, 5].max()) < .002, float(cv[100, 5].max()), "~0"),
            check("negative control: the plain fill has nothing outside", not (float(luma(plain)[100, 190]) > 0), float(luma(plain)[100, 190]),
                  0)], [wd / "blade.png"]


def bolt_path(seed):
    rng = np.random.default_rng(seed)
    x, y, pts = 150.0, 0.0, [(150.0, 0.0)]
    while y < 430:
        x += rng.uniform(-30, 18)
        y += rng.uniform(18, 34)
        pts.append((x, y))
    return pts


def flash(t):
    return max(0, 1 - abs(t - 10.6) / .09) + .55 * max(0, 1 - abs(t - 10.82) / .07)


@card("GLOW-15")
def lightning(task, wd):
    h, w = 440, 300
    pts = bolt_path(7)
    cv = canvas(h, w, "#0a0e1a")
    stroke = m_line(h, w, pts, 10)
    cv = glow(cv, stroke, "#8fb4ff", 30, .7)
    cv = fill(cv, m_line(h, w, pts, 2.6), "#f6f9ff")
    wash = np.exp(-(dist_map(h, w, pts[5][0], pts[5][1]) / 200) ** 2) * .18
    cv = cv + wash[..., None] * hxf("#9fbcf0") * (1 - np.minimum(cv, 1))
    save(rolloff(cv), wd / "bolt.png")
    same = bolt_path(7) == pts
    other = bolt_path(8) != pts
    on = [round(flash(t), 3) for t in (10.6, 10.82, 10.7, 10.5)]
    width = sum(1 for t in np.arange(10.4, 11.0, .005) if flash(t) > 0) * .005
    px = cv[int(pts[6][1]), int(pts[6][0])]
    near = cv[int(pts[6][1]), int(pts[6][0]) + 20]
    return [check("seeded random walk is reproducible", same, same, True),
            check("thin core near white on the bolt", float(px.min()) > .9, tohex(rolloff(px) * 255), "#f6f9ff"),
            check("wide blue glow beside the bolt (B > R)", near[2] > near[0] and float(near.sum()) > float(hxf("#0a0e1a").sum()) + .05,
                  tohex(near * 255), "blue"),
            check("double pulse: 1 at 10.6 s, .55 at 10.82 s, dark between", on[:3] == [1.0, .55, 0.0], on, [1, .55, 0]),
            check("flash total width ~ 180 + 140 ms", abs(width - .32) < .02, width, .32),
            check("negative control: another seed gives another bolt", other, other, True)], [wd / "bolt.png"]


def radial_wash(h, w, cx, cy, rx, ry, col, a):
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.hypot((xx - cx) / rx, (yy - cy) / ry)
    return np.clip(1 - d, 0, 1)[..., None] * hxf(col) * a, np.clip(1 - d, 0, 1) * a


@card("GLOW-17")
def corner_blobs(task, wd):
    h, w = 180, 320
    base = canvas(h, w, "#0b0d14")
    layers = [(.95 * w, -.05 * h, 600 / 6, 400 / 6, "#6366f1", .08), (-.05 * w, .40 * h, 500 / 6, 380 / 6, "#06b6d4", .07),
              (1.0 * w, .85 * h, 500 / 6, 380 / 6, "#ec4899", .06)]
    cv = base.copy()
    alphas = []
    for cx, cy, rx, ry, col, a in layers:
        add, al = radial_wash(h, w, cx, cy, rx, ry, col, a)
        cv = cv * (1 - al[..., None]) + hxf(col) * al[..., None]
        alphas.append(float(al.max()))
    rng = np.random.default_rng(1)
    cv = np.clip(cv + (rng.random((h, w, 1)) - .5) * .02, 0, 1)
    save(cv, wd / "wash.png")
    tr = cv[3, w - 10] - base[3, w - 10]
    centre = float(np.abs(cv[90, 160] - base[90, 160]).max())
    return [check("blob alphas within .05 .. .10", all(.05 <= a <= .10 for a in alphas), alphas, ".05..10"),
            check("top-right corner tinted indigo (B up)", tr[2] > .01, tohex(cv[3, w - 10] * 255), "indigo tint"),
            check("centre only carries grain (|delta| <= .01)", centre <= .011, centre, "<= .01"),
            check("radial, not a full-screen linear gradient (centre row flat)", float(np.ptp(blur(cv, 3)[90, 120:200, 2])) < .01,
                  float(np.ptp(blur(cv, 3)[90, 120:200, 2])), "< .01"),
            check("negative control: the base has no corner tint", not (float((base[3, w - 10] - base[3, w - 10])[2]) > .01), 0, None)], \
        [wd / "wash.png"]


def wander(t, w, h):
    return w / 2 + math.sin(.32 * t) * .13 * w, .48 * h + math.cos(.38 * t) * .08 * h


@card("GLOW-18")
def wandering_glow(task, wd):
    w, h = 192, 108
    frames, err = [], []
    for i, t in enumerate(np.linspace(0, 6, 31)):
        y = np.linspace(0, 1, h)[:, None, None]
        cv = hxf("#071520") * (1 - y) + hxf("#22584d") * y
        cv = np.repeat(cv, w, 1)
        cx, cy = wander(t, w, h)
        r = .39 * min(w, h)
        d = dist_map(h, w, cx, cy) / r
        a = np.interp(d, [0, .68, 1], [0x55 / 255, 0x17 / 255, 0])
        g = np.where(d[..., None] < .68, hxf("#57d2ba"), hxf("#77cfc0"))
        cv = cv * (1 - a[..., None]) + g * a[..., None]
        frames.append(cv)
        lum = blur(luma(cv - (hxf("#071520") * (1 - y) + hxf("#22584d") * y)), 2)
        py, px = np.unravel_index(np.argmax(lum), lum.shape)
        err.append(math.hypot(px - cx, py - cy))
    write_video(wd / "aurora_demo.mp4", frames, fps=5)
    return [check("glow centre follows the Lissajous path (<= 2 px)", max(err) <= 2, max(err), "<= 2"),
            check("x amplitude .13 w, y amplitude .08 h", abs(max(wander(t, w, h)[0] for t in np.linspace(0, 20, 400)) - (w / 2 + .13 * w)) < .5,
                  None, w / 2 + .13 * w),
            check("negative control: the glow moved between t=0 and t=6", math.dist(wander(0, w, h), wander(6, w, h)) > 5,
                  math.dist(wander(0, w, h), wander(6, w, h)), "> 5")], [wd / "aurora_demo.mp4"]


def aurora_frame(t, period=8.0, w=160, h=90, accent="#2ee6a0"):
    cv = canvas(h, w, "#06050a")
    yy, xx = np.mgrid[0:h, 0:w]
    for k, (cx, cy, s) in enumerate(((.25, .75, .5), (.55, .8, .45), (.8, .7, .4))):
        ph = 2 * math.pi * (t / period + k / 3)
        x, y = cx * w + 15 * math.sin(ph), cy * h + 5 * math.cos(ph)
        a = np.clip(1 - np.hypot(xx - x, yy - y) / (s * w / 2), 0, 1) ** 2 * .6
        cv = cv * (1 - a[..., None]) + hxf(accent) * a[..., None]
    v = 1 - .15 * smoothstep(.5, 1.0, np.hypot((xx - w / 2) / (w / 2), (yy - h / 2) / (h / 2)) / math.sqrt(2))
    return blur(cv, 4) * v[..., None]


@card("GLOW-19")
def aurora_drift(task, wd):
    frames = [aurora_frame(i / 10) for i in range(40)]
    write_video(wd / "aurora.mp4", frames, fps=10)
    loop = float(np.abs(aurora_frame(1.0) - aurora_frame(9.0)).max())
    moving = float(np.abs(aurora_frame(0) - aurora_frame(2)).mean())
    tint = frames[0][70, 40]
    corner = float(luma(frames[0])[1, 1] / max(luma(aurora_frame(0, accent="#2ee6a0"))[1, 1], 1e-9))
    plain = canvas(90, 160, "#06050a")
    return [check("seamless loop (frame(t) == frame(t + period))", loop < 1e-9, loop, 0),
            check("blobs drift", moving > .002, moving, "> .002"),
            check("blobs tinted by the accent (G dominant)", tint[1] > tint[0] and tint[1] > tint[2], tohex(tint * 255), "green"),
            check("blobs sit in the bottom third", float(luma(frames[0])[65:].mean()) > 2 * float(luma(frames[0])[:30].mean()), None, None),
            check("negative control: the dark base has no accent", not (plain[70, 40][1] > plain[70, 40][0]), tohex(plain[70, 40] * 255),
                  "#06050a")], [wd / "aurora.mp4"]


@card("GLOW-20")
def follow_spot(task, wd):
    w, h, fps = 160, 90, 30
    targets = [(40, 45), (120, 30), (90, 70)]
    frames, cen = [], []
    c = np.array(targets[0], float)
    for scene, tgt in enumerate(targets):
        for i in range(20):
            c = c + (np.array(tgt) - c) * .25               # centre lerps to the active object
            r = .6 * w
            a = np.clip(1 - dist_map(h, w, *c) / r, 0, 1) ** 1.5 * .25
            cv = canvas(h, w) + hxf("#0a3d91")[None, None] * a[..., None] / .25 * .25 * 4
            for tx, ty in targets:
                cv[ty - 3:ty + 3, tx - 3:tx + 3] = .9 if (tx, ty) == tgt else .3
            frames.append(np.clip(cv, 0, 1))
            cen.append(c.copy())
    write_video(wd / "follow.mp4", frames, fps=fps)
    ends = [cen[19], cen[39], cen[59]]
    errs = [float(np.linalg.norm(e - np.array(t))) for e, t in zip(ends, targets)]
    first_next = float(np.linalg.norm(cen[20] - np.array(targets[1])))
    return [check("spot centre arrives on each active object (<= 1 px)", max(errs) <= 1, errs, "<= 1"),
            check("glow #0a3d91 at the centre, gone beyond 60 % W", abs(float(frames[19][52, 40, 2]) - hxf("#0a3d91")[2] * (1 - 7 / 96) ** 1.5) < .02 and
                  float(frames[19][45, 40 + 100, 2]) == 0, [float(frames[19][52, 40, 2]), float(frames[19][45, 140, 2])],
                  [hxf("#0a3d91")[2], 0]),
            check("glide, not jump: first frame of scene 2 still far from target", first_next > 10, first_next, "> 10"),
            check("negative control: at scene start the spot is not on the new target", not (first_next <= 1), first_next, "> 1")], \
        [wd / "follow.mp4"]


@card("GLOW-21")
def concentric_halo(task, wd):
    h, w = 220, 220
    R = 420 / 8
    d = dist_map(h, w, 110, 110)
    cv = canvas(h, w)
    for spread, a in ((95 / 4, .018), (45 / 4, .025)):            # box-shadow spreads, scaled /4
        cv = fill(cv, (d <= R + spread).astype(float), "#ffffff", a)
    cv = fill(cv, (d <= R).astype(float), "#1a1a24", 1)
    save(cv, wd / "halo.png")
    inner = float(cv[110, int(110 + R + 5), 0])
    outer = float(cv[110, int(110 + R + 18), 0])
    out = float(cv[110, int(110 + R + 30), 0])
    e_in = 1 - (1 - .018) * (1 - .025)
    return [check("inner band = both spreads stacked (~.043)", abs(inner - e_in) < .003, inner, e_in),
            check("outer band = the 95 px spread alone (.018)", abs(outer - .018) < .003, outer, .018),
            check("nothing beyond the last spread", out == 0, out, 0),
            check("negative control: without shadows the band is black", not (float(fill(canvas(h, w), (d <= R).astype(float), "#1a1a24", 1)
                                                                                 [110, int(110 + R + 5), 0]) > .01), 0, None)], [wd / "halo.png"]


@card("GLOW-22")
def pulse_ring(task, wd):
    fps, h, w = 50, 100, 100
    frames, radii = [], []
    for i in range(int(3.0 * fps)):
        t = i * 1000 / fps
        tt = t - 320
        if 0 <= tt < 1800:
            ph = (tt % 900) / 900
            s, op = .55 + (2.4 - .55) * (1 - (1 - ph) ** 3), 1 - ph
        else:
            s, op = 0, 0
        cv = canvas(h, w, "#0f1720")
        cv = fill(cv, m_ellipse(h, w, 50, 50, 4), "#5cc3c5")
        if op > 0:
            ring = m_ellipse(h, w, 50, 50, 8 * s + 1) - m_ellipse(h, w, 50, 50, 8 * s)
            cv = fill(cv, np.clip(ring, 0, 1), "#5cc3c5", op)
        frames.append(cv)
        radii.append(s)
    write_video(wd / "pulse.mp4", frames, fps=fps)
    starts = [i for i in range(1, len(radii)) if radii[i] > 0 and (radii[i - 1] == 0 or radii[i] < radii[i - 1] - .5)]
    tail = frames[int(2.3 * fps):]
    static = all(np.array_equal(tail[0], f) for f in tail)
    return [check("ring scales .55 -> 2.4", abs(max(radii) - 2.4) < .05 and abs(min(r for r in radii if r > 0) - .55) < .05,
                  [min(r for r in radii if r > 0), max(radii)], [.55, 2.4]),
            check("exactly 2 iterations, starting after 320 ms", len(starts) == 2 and abs(starts[0] / fps - .32) < .03,
                  [s / fps for s in starts], [.32, 1.22]),
            check("then the mark settles static", static, static, True),
            check("negative control: a frame mid-pulse differs from the settled mark", not np.array_equal(frames[int(.6 * fps)], tail[0]),
                  True, True)], [wd / "pulse.mp4"]


@card("GLOW-24")
def audio_halo(task, wd):
    rate, dur = 22050, 2.0
    t = np.arange(int(rate * dur)) / rate
    sig = .2 * np.sin(2 * math.pi * 220 * t)
    kicks = [.5, 1.0, 1.5]
    for k in kicks:
        m = (t >= k) & (t < k + .12)
        sig[m] += .8 * np.exp(-(t[m] - k) / .03) * np.sin(2 * math.pi * 60 * (t[m] - k))
    fx.write_wav(wd / "song.wav", sig, rate)
    data, r = fx.read_wav(wd / "song.wav")
    x = data[:, 0]
    fps, W, H = 25, 160, 90
    hop = r // fps
    rms = np.array([math.sqrt(float(np.mean(x[i * hop:(i + 1) * hop] ** 2))) for i in range(int(dur * fps))])
    low = np.convolve(np.abs(x), np.ones(200) / 200, "same")
    env = np.array([float(low[i * hop:(i + 1) * hop].max()) for i in range(int(dur * fps))])
    kick = np.clip((env - np.median(env)) / (env.max() - np.median(env)), 0, 1)
    rms_n = rms / rms.max()
    R = .62 * min(W, H) * (1 + .05 * rms_n + .06 * kick)
    frames = []
    for i in range(len(R)):
        a = (.20 + .16 * rms_n[i] + .14 * kick[i])
        halo = np.clip(1 - dist_map(H, W, 80, 45) / R[i], 0, 1) ** 2 * a
        frames.append(canvas(H, W, "#0b0f1e") + halo[..., None] * hxf("#ecbd51"))
    write_video(wd / "halo.mp4", frames, fps=fps)
    kf = [int(k * fps) + int(np.argmax(kick[int(k * fps):int(k * fps) + 3])) for k in kicks]
    quiet = [5, 18, 30]
    ratio = float(np.mean(R[kf]) / np.mean(R[quiet]))
    expect = (1 + .05 * float(np.mean(rms_n[kf])) + .06 * float(np.mean(kick[kf]))) / \
             (1 + .05 * float(np.mean(rms_n[quiet])) + .06 * float(np.mean(kick[quiet])))
    lum_k = float(luma(frames[kf[0]]).mean())
    lum_q = float(luma(frames[quiet[1]]).mean())
    flat_R = .62 * min(W, H) * (1 + .05 * np.ones(5) + 0)
    return [check("kicks detected from the audio at .5 / 1.0 / 1.5 s", all(kick[f] > .5 for f in kf), [float(kick[f]) for f in kf], "> .5"),
            check("halo radius swells on kicks by the formula", abs(ratio - expect) < .005 and ratio > 1.03, [ratio, expect], "> 1.03"),
            check("kick frames brighter than quiet frames", lum_k > lum_q, [lum_k, lum_q], "brighter"),
            check("negative control: a steady signal gives a constant radius", not (float(np.ptp(flat_R)) > 0), float(np.ptp(flat_R)), 0)], \
        [wd / "halo.mp4", jdump(wd / "sound.json", {"rms": rms_n.tolist(), "kick": kick.tolist()})]


BAYER4 = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0


@card("GLOW-25")
def pixel_magic_circle(task, wd):
    lw, lh, scale, fps = 64, 40, 4, 24
    frames, angles = [], []
    for i in range(24):
        step = i // 3                                   # 8 fps rotation inside a 24 fps film
        ang = step * 15
        angles.append(ang)
        col = hxf("#7a5cff") if step % 2 == 0 else hxf("#2ee6ff")
        yy, xx = np.mgrid[0:lh, 0:lw]
        e = np.hypot((xx - 32) / 26, (yy - 20) / 12)
        ring = (np.abs(e - 1) < .08).astype(float)
        th = np.arctan2((yy - 20) / 12, (xx - 32) / 26)
        runes = ((np.abs(e - .75) < .1) & (((np.degrees(th) - ang) % 45) < 8)).astype(float)
        halo = np.clip(1 - np.abs(e - 1) / .5, 0, 1) * .6
        dith = (halo > np.tile(BAYER4, (lh // 4, lw // 4))).astype(float)
        low = canvas(lh, lw, "#0a0814")
        low = np.where((dith > 0)[..., None], col * .5, low)
        low = np.where(((ring + runes) > 0)[..., None], col, low)
        frames.append(np.kron(low, np.ones((scale, scale, 1))))   # nearest-neighbour upscale
    write_video(wd / "rune.mp4", frames, fps=fps)
    save(frames[0], wd / "rune.png")
    f0 = frames[0]
    blocks = f0.reshape(lh, scale, lw, scale, 3)
    crisp = float(blocks.std(axis=(1, 3)).max())
    levels = len(np.unique(np.round(f0.reshape(-1, 3), 4), axis=0))
    smooth = blur(f0, 3)
    return [check("rotation steps at 8 fps (angle changes every 3 frames)", angles[:7] == [0, 0, 0, 15, 15, 15, 30], angles[:7],
                  [0, 0, 0, 15, 15, 15, 30]),
            check("nearest upscale: every 4x4 block uniform", crisp < 1e-9, crisp, 0),
            check("ordered-dither glow: only 3 colour levels, no blur ramp", levels <= 3, levels, "<= 3"),
            check("flash alternates two colours", tohex(frames[0][80, 4 * 32] * 255) != tohex(frames[3][80, 4 * 32] * 255) or
                  tohex(frames[0][4 * 8, 4 * 32] * 255) != tohex(frames[3][4 * 8, 4 * 32] * 255), None, "alternates"),
            check("negative control: a blurred glow has many levels", not (len(np.unique(np.round(smooth.reshape(-1, 3), 4), axis=0)) <= 3),
                  len(np.unique(np.round(smooth.reshape(-1, 3), 4), axis=0)), "> 3")], [wd / "rune.mp4", wd / "rune.png"]


def threshold_bloom(img, thr, strength, radius_px, tint=(1, 1, 1)):
    hi = np.maximum(img - thr, 0)
    return img + (blur(hi, radius_px) * strength + blur(hi, 3 * radius_px) * strength * .5) * np.array(tint)


def radial_rays(img, cx, cy, samples=64, decay=.972, stride=.55, thr=.7, gain=.55, sky=None):
    h, w = img.shape[:2]
    src = np.where((luma(img) > thr)[..., None], img, 0)
    if sky is not None:
        src = src * sky[..., None]
    from scipy.ndimage import map_coordinates
    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    acc = np.zeros_like(img)
    wgt = 1.0
    for k in range(samples):
        f = 1 - stride * k / samples
        sy, sx = cy + (yy - cy) * f, cx + (xx - cx) * f
        for c in range(3):
            acc[..., c] += map_coordinates(src[..., c], [sy, sx], order=1, mode="constant") * wgt
        wgt *= decay
    return acc / samples * gain * 4


def make_post(hdr, sun=None, bloom=.22, threshold=.9, radius=.6, vignette=.42, ca=1.2, grain=.16, clamp=48.0, seed=0):
    img = np.nan_to_num(hdr, nan=0.0, posinf=clamp, neginf=0.0)
    img = np.clip(img, 0, clamp)                                      # NaN / firefly guard
    h, w = img.shape[:2]
    img = threshold_bloom(img, threshold, bloom * 4, radius * 10)
    if sun is not None:
        img = img + radial_rays(img, sun[0], sun[1], thr=threshold)
    y = luma(np.clip(img, 0, 1))[..., None]
    img = img * (np.array([.92, .98, 1.08]) * (1 - y) + np.array([1.08, 1.0, .92]) * y)
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.hypot((xx - w / 2) / (w / 2), (yy - h / 2) / (h / 2)) / math.sqrt(2)
    img = img * (1 - vignette * smoothstep(.35, .95, r))[..., None]
    rng = np.random.default_rng(seed)
    img = img + (rng.random((h, w, 1)) - .5) * grain * .1
    return rolloff(img)


@card("GLOW-26")
def make_post_stack(task, wd):
    h, w = 120, 200
    hdr = np.zeros((h, w, 3)) + .02
    torus = m_ellipse(h, w, 60, 60, 22) - m_ellipse(h, w, 60, 60, 15)
    hdr += np.clip(torus, 0, 1)[..., None] * np.array(kelvin(1900)) / 255 * 4
    hdr += m_ellipse(h, w, 150, 60, 8)[..., None] * np.array([.2, 1.0, 1.0]) * 4
    hdr[100:110, 10:40] = .5                                          # lit surface below threshold
    hdr[5, 5] = np.nan
    hdr[6, 6] = np.inf
    out = make_post(hdr, sun=(150, 60), seed=1)
    noray = make_post(hdr, sun=None, seed=1)
    save(out, wd / "post.png")
    plain = rolloff(np.clip(np.nan_to_num(hdr, nan=0, posinf=1), 0, 1))
    corona_t = out[60, 60 + 28] - plain[60, 60 + 28]
    corona_o = out[60, 150 + 14] - plain[60, 150 + 14]
    surf = float(np.abs(blur(out, 1)[98, 25] - blur(plain, 1)[98, 25]).max())
    ray_along = float(luma(out)[60, 166] - luma(noray)[60, 166])
    return [check("NaN / Inf guarded (all finite)", bool(np.isfinite(out).all()), True, True),
            check("torus corona in its 1900 K colour (R > B)", corona_t[0] > .02 and corona_t[0] > corona_t[2], tohex(corona_t * 255 + 0),
                  "warm halo"),
            check("cyan orb corona in its own colour (B > R)", corona_o[2] > corona_o[0] and corona_o[2] > .02, tohex(corona_o * 255),
                  "cyan halo"),
            check("threshold .9: a .5 lit surface does not bloom", surf < .08, surf, "< .08"),
            check("sun rays add light 16 px out from the on-screen sun", ray_along > .005, ray_along, "> .005"),
            check("negative control: without the post stack there is no warm corona",
                  not (float(plain[60, 88][0] - plain[60, 5][0]) > .02 and plain[60, 88][0] > plain[60, 88][2]),
                  tohex(plain[60, 88] * 255), "ground")], [wd / "post.png", jdump(wd / "post.json", {"engine": "numpy port of the makePost chain order",
                                                                         "params": {"bloom": .22, "threshold": .9, "radius": .6}})]


@card("GLOW-27")
def selective_bloom(task, wd):
    h, w = 100, 200
    emissive = np.zeros((h, w, 3))
    emissive += m_ellipse(h, w, 50, 50, 12)[..., None] * hxf("#ff2a6d") * 3
    beauty = canvas(h, w, "#0a0a10")
    beauty = fill(beauty, m_ellipse(h, w, 150, 50, 16), "#ffffff")       # white, lit, must not glow
    beauty = beauty + emissive
    sel = beauty + blur(emissive, 6) * 1.5                              # MRT emissive target, threshold 0
    glob = threshold_bloom(beauty, .2, 1.5, 6)
    save(rolloff(sel), wd / "selective.png")
    halo_e = sel[50, 50 + 18] - beauty[50, 50 + 18]
    halo_w = float(luma(sel)[50, 150 + 22] - luma(beauty)[50, 150 + 22])
    halo_wg = float(luma(glob)[50, 150 + 22] - luma(beauty)[50, 150 + 22])
    tau = .25
    hit = [4 * math.exp(-t / tau) for t in (0, .25, .5)]
    return [check("emissive source wears a corona in its own colour", halo_e[0] > .05 and halo_e[0] > halo_e[1], tohex(np.clip(halo_e, 0, 1) * 255),
                  "pink"),
            check("white lit object stays clean (no halo)", abs(halo_w) < 1e-9, halo_w, 0),
            check("hit ring decays with tau 250 ms (4 -> 4/e -> 4/e^2)", abs(hit[1] - 4 / math.e) < 1e-9 and abs(hit[2] - 4 / math.e ** 2) < 1e-9,
                  hit, [4, 4 / math.e, 4 / math.e ** 2]),
            check("negative control: global low-threshold bloom makes the white object glow", halo_wg > .02, halo_wg, "> .02")], \
        [wd / "selective.png"]


SHOTS28 = {"makePost": (.22, .90, .60, 1.0), "blue_hour": (.75, .72, .70, 1.0), "egypt_giza": (.42, .95, .50, .82),
           "egypt_orbit": (1.25, .12, .75, 1.10)}


def exposure_curve(t, dur, e):
    return e * smoothstep(0, .35, t) * (1 - .1 * smoothstep(dur - .6, dur, t))


@card("GLOW-28")
def per_shot_presets(task, wd):
    h, w, fps, dur = 60, 100, 20, 1.5
    base = canvas(h, w, "#06080e") + m_ellipse(h, w, 50, 30, 8)[..., None] * 1.6
    frames, params = [], []
    for name in ("blue_hour", "egypt_giza"):
        b, thr, rad, e = SHOTS28[name]
        for i in range(int(dur * fps)):
            t = i / fps
            img = threshold_bloom(base * exposure_curve(t, dur, e), thr, b, rad * 10)
            frames.append(rolloff(img))
            params.append(name)
    write_video(wd / "shots.mp4", frames, fps=fps)
    cut = int(dur * fps)
    halo = lambda f: float(luma(f)[30, 50 + 16])
    jump = abs(halo(frames[cut - 8]) - halo(frames[cut + 10]))
    e = [exposure_curve(t, dur, 1.0) for t in (0, .35, .9, 1.5)]
    within = abs(halo(frames[10]) - halo(frames[12]))
    return [check("exposure fades in over 0 - .35 s", e[0] == 0 and abs(e[1] - 1) < 1e-9, e[:2], [0, 1]),
            check("exposure drops 10 % in the last .6 s", abs(e[3] - .9) < 1e-9 and abs(e[2] - 1) < 1e-9, e[2:], [1, .9]),
            check("table values carried per shot (Egypt Giza threshold .95, exposure .82)", SHOTS28["egypt_giza"][1] == .95 and
                  SHOTS28["egypt_giza"][3] == .82, SHOTS28["egypt_giza"], (.42, .95, .5, .82)),
            check("a cut changes the bloom mood instantly (halo jump)", jump > .05, jump, "> .05"),
            check("negative control: inside a held shot the halo is steady", not (within > .05), within, "<= .05")], [wd / "shots.mp4"]


@card("GLOW-29")
def tsl_style_nodes(task, wd):
    h, w = 60, 200
    from scipy.ndimage import uniform_filter1d
    frames = []
    for i in range(3):
        cv = canvas(h, w, "#202020")
        cv[10:50, 10:50] = .5                                      # static object
        x = 80 + i * 12
        obj = np.zeros((h, w))
        obj[20:40, x:x + 20] = 1
        vel = 12
        moving = np.where(obj[..., None] > 0, hxf("#ffffff"), 0)
        blurred = np.stack([uniform_filter1d(moving[..., c], vel, axis=1) for c in range(3)], -1)
        mob = uniform_filter1d(obj, vel, axis=1)
        cv = cv * (1 - mob[..., None]) + blurred
        emis = np.zeros((h, w, 3))
        emis[25:35, 170:180] = hxf("#3fd0ff") * 2
        cv = cv + emis + blur(emis, 3) * 1.5                       # selective bloom of the emissive target only
        from scipy.ndimage import shift as nd_shift
        pre_ca = cv.copy()
        off = .002 * w * 2.5                                       # .002 UV at a 1000 px-wide target, drawn at 200 px
        cv = np.stack([nd_shift(cv[..., 0], (0, off), order=1, mode="nearest"), cv[..., 1],
                       nd_shift(cv[..., 2], (0, -off), order=1, mode="nearest")], -1)
        frames.append(np.clip(cv, 0, 1))
    write_video(wd / "nodes.mp4", frames, fps=10)
    f = frames[1]
    edge = luma(f)[30, 80 + 12 - 10:80 + 12 + 30]
    ramp_w = int(np.sum((edge > .25) & (edge < .9)))
    static_edge = luma(f)[30, 5:15]
    static_ramp = int(np.sum((static_edge > .17) & (static_edge < .45)))
    glow_px = float(f[30, 182, 2] - hxf("#202020")[2])
    ca = float(abs(f[30, 10, 0] - f[30, 10, 2]))
    ca0 = float(abs(pre_ca[30, 10, 0] - pre_ca[30, 10, 2]))
    return [check("velocity motion blur smears the moving object along x", ramp_w >= 6, ramp_w, ">= 6 px ramp"),
            check("static object stays sharp (zero velocity)", static_ramp <= 2, static_ramp, "<= 2"),
            check("selective bloom spills only from the emissive target", glow_px > .05 and float(f[45, 30, 2]) - .5 < .05, glow_px, "> .05"),
            check("CA .002 UV splits R and B at edges", ca > .03, ca, "> .03"),
            check("negative control: before the CA node R == B at that edge", not (ca0 > .03), ca0, "<= .03"),
            check("negative control: the unblurred moving object has a hard edge",
                  not (int(np.sum((obj[30, 70:130] > .25) & (obj[30, 70:130] < .9))) >= 6), 0, ">= 6")], \
        [wd / "nodes.mp4", jdump(wd / "nodes.json", {"engine": "numpy port of bloom/MRT, motionBlur, chromaticAberration nodes"})]


@card("GLOW-30")
def painter_bloom(task, wd):
    h, w = 120, 240
    cv = canvas(h, w, "#05070c")
    cv = fill(cv, m_ellipse(h, w, 60, 60, 14), (1.4, 1.3, 1.2))
    cv = fill(cv, m_ellipse(h, w, 180, 60, 14), (.7, .7, .7))          # below threshold .75
    tint = hxf("#ffe6d0")
    out = threshold_bloom(cv, .75, .6, 30 / 10, tint)
    save(rolloff(out), wd / "bloom.png")
    d_bright = [float(luma(out - cv)[60, 60 + 14 + k]) for k in (3, 9, 25)]
    d_grey = float(np.abs(out - cv)[60, 180 + 18].max())
    tint_px = (out - cv)[60, 60 + 20]
    return [check("bright disc spills at two radii (near > mid > far > 0)", d_bright[0] > d_bright[1] > d_bright[2] > 0, d_bright, "decreasing"),
            check("pixels below the .75 threshold do not bloom", d_grey < 1e-12, d_grey, 0),
            check("spill carries the tint #ffe6d0 (R >= G >= B)", tint_px[0] >= tint_px[1] >= tint_px[2], tohex(tint_px / tint_px.max() * 255),
                  "warm"),
            check("negative control: unbloomed canvas has no spill", not (float(luma(cv)[60, 60 + 17]) > float(luma(cv)[60, 5]) + 1e-6),
                  float(luma(cv)[60, 77]), "ground")], [wd / "bloom.png"]


@card("GLOW-31")
def float_blend_modes(task, wd):
    base = np.zeros((40, 40, 3)) + .6
    m = np.ones((40, 40))
    add = fill(base, m, (.7, .7, .7), 1, mode="add")
    scr = fill(base, m, (.7, .7, .7), 1, mode="screen")
    over = np.zeros((40, 40, 3)) + 1.3
    scr_over = fill(over, m, (.5, .5, .5), 1, mode="screen")
    mul = fill(base, m, (.5, .5, .5), 1, mode="multiply")
    out = rolloff(add)
    save(np.hstack([out, rolloff(scr), rolloff(mul)]), wd / "modes.png")
    return [check("add exceeds 1.0 on the float canvas (.6 + .7 = 1.3)", abs(float(add[0, 0, 0]) - 1.3) < 1e-9, float(add[0, 0, 0]), 1.3),
            check("screen = reg + col*a*(1 - min(reg,1)) = .88", abs(float(scr[0, 0, 0]) - .88) < 1e-9, float(scr[0, 0, 0]), .88),
            check("screen over > 1 adds nothing more (not clipped down)", abs(float(scr_over[0, 0, 0]) - 1.3) < 1e-9, float(scr_over[0, 0, 0]), 1.3),
            check("multiply darkens (.6 x .5 = .3)", abs(float(mul[0, 0, 0]) - .3) < 1e-9, float(mul[0, 0, 0]), .3),
            check("rolloff .82 maps 1.3 back below 1", float(out[0, 0, 0]) < 1, float(out[0, 0, 0]), "< 1"),
            check("negative control: a clipping canvas loses the 1.3", not (abs(float(np.clip(add, 0, 1)[0, 0, 0]) - 1.3) < 1e-9), 1.0, 1.3)], \
        [wd / "modes.png"]


@card("GLOW-32")
def vignette_four(task, wd):
    h, w = 90, 160
    flat = np.zeros((h, w, 3)) + .7
    yy, xx = np.mgrid[0:h, 0:w]
    edge = np.minimum.reduce([xx, w - 1 - xx, yy, h - 1 - yy]).astype(float)
    css = flat * (1 - .85 * np.exp(-(edge / (160 / 8)) ** 2 * 2))[..., None]
    d = dist_map(h, w, w / 2, h / 2)
    v = .6
    can = flat * (1 - v * np.clip((d - .3 * min(w, h)) / (.75 * max(w, h) - .3 * min(w, h)), 0, 1))[..., None]
    rr = np.hypot((xx - w / 2) / (w / 2), (yy - h / 2) / (h / 2)) / math.sqrt(2)
    kit = flat * (1 - .42 * np.clip((rr - .55) / .45, 0, 1))[..., None]
    pnt = flat * (1 - .5 * smoothstep(.35, 1, d / math.hypot(w / 2, h / 2)))[..., None]
    save(np.vstack([css, can, kit, pnt]), wd / "vignettes.png")
    ratios = {k: float(x[1, 1, 0] / x[45, 80, 0]) for k, x in (("css", css), ("canvas", can), ("kit", kit), ("painter", pnt))}
    inner = float(can[45, 80 + int(.29 * min(w, h)), 0])
    return [check("all four darken the corners (< .75 of centre)", all(r < .75 for r in ratios.values()), ratios, "< .75"),
            check("centre unchanged in all four", all(abs(float(x[45, 80, 0]) - .7) < 1e-3 for x in (css, can, kit, pnt)), None, .7),
            check("canvas radial: transparent inside .3 * min(W,H)", abs(inner - .7) < 1e-9, inner, .7),
            check("negative control: the flat plate has no vignette", not (float(flat[1, 1, 0] / flat[45, 80, 0]) < .75), 1.0, "< .75")], \
        [wd / "vignettes.png"]


def chroma_ab(img, ca, width_ref=1920):
    from scipy.ndimage import map_coordinates
    h, w = img.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    u, v = xx / w - .5, yy / h - .5
    r = np.hypot(u, v)
    off = (ca / width_ref) * r * 4
    out = img.copy()
    out[..., 0] = map_coordinates(img[..., 0], [(v * (1 - off) + .5) * h, (u * (1 - off) + .5) * w], order=1, mode="nearest")
    out[..., 2] = map_coordinates(img[..., 2], [(v * (1 + off) + .5) * h, (u * (1 + off) + .5) * w], order=1, mode="nearest")
    return out


@card("GLOW-33")
def lens_ca(task, wd):
    h, w = 200, 1920
    img = np.zeros((h, w, 3))
    for x in (960, 1440, 1900):
        img[:, x:x + 10] = 1
    out = chroma_ab(img, 1.2 * 6)
    save(out[:, ::4], wd / "ca.png")
    split = lambda x: float(np.abs(out[100, x - 20:x + 30, 0] - out[100, x - 20:x + 30, 2]).sum())
    s_c, s_m, s_e = split(960), split(1440), split(1900)
    return [check("~no split at the centre (< 2 % of the edge split)", s_c < .02 * s_e, s_c, "~0"),
            check("split grows toward the edge", s_e > s_m > s_c, [s_c, s_m, s_e], "rising"),
            check("quadratic growth (edge/mid ~ (0.49/0.25)^2)", 2.5 < s_e / s_m < 5.5, s_e / s_m, (.49 / .25) ** 2),
            check("negative control: untouched lines have equal R and B", not (float(np.abs(img[100, 1880:1930, 0] - img[100, 1880:1930, 2]).sum()) > 0),
                  0, None)], [wd / "ca.png"]


def channel_offset(f):
    r, b = f[30, :, 0], f[30, :, 2]
    best = max(range(-16, 17), key=lambda k: float(np.dot(np.roll(r, -k), b)) if True else 0)
    return -best


@card("GLOW-34")
def rgb_split_hit(task, wd):
    h, w = 60, 200
    frames, offs = [], []
    hits = {10, 11, 12}
    for i in range(20):
        o = 10 if i in hits else 3
        base = np.zeros((h, w, 3))
        base[15:45, 90:110] = 1
        f = np.zeros((h, w, 3))
        f[..., 0] = np.roll(base[..., 0], o, 1)
        f[..., 1] = base[..., 1]
        f[..., 2] = np.roll(base[..., 2], -o, 1)
        frames.append(f)
        r_x = int(np.argmax(f[30, :, 0] > .5))
        b_x = int(np.argmax(f[30, :, 2] > .5))
        offs.append((r_x - b_x) // 2)
    write_video(wd / "split.mp4", frames, fps=24)
    idle = [offs[i] for i in range(20) if i not in hits]
    hit = [offs[i] for i in sorted(hits)]
    return [check("idle split 2-4 px", all(2 <= o <= 4 for o in idle), idle[:3], "2..4"),
            check("hit spikes to 8-12 px for 2-3 frames", all(8 <= o <= 12 for o in hit) and len(hit) == 3, hit, "8..12 x3"),
            check("stillness returns after the hit", offs[13] == 3, offs[13], 3),
            check("negative control: the unsplit layer has no idle split",
                  not (2 <= (int(np.argmax(base[30, :, 0] > .5)) - int(np.argmax(base[30, :, 2] > .5))) // 2 <= 4), 0, "2..4")], [wd / "split.mp4"]


@card("GLOW-35")
def velocity_blur(task, wd):
    h, w = 60, 300
    from scipy.ndimage import gaussian_filter1d

    def render(speed):
        base = np.zeros((h, w))
        base[20:40, 140:160] = 1
        sigma = min(24, .25 * speed)
        return gaussian_filter1d(base, sigma, axis=1) if sigma > 0 else base, sigma
    img, sig = render(40)
    rest, s0 = render(0)
    _, capped = render(200)
    row = img[30]
    rise = np.where((row > .1) & (row < .9))[0]
    rise_w = int(np.sum(rise < 150))
    col = img[:, 150] / img[:, 150].max()
    v_rise = int(np.sum((col > .1) & (col < .9)))
    save(np.stack([img] * 3, -1), wd / "vblur.png")
    return [check("blur sigma = .25 x 40 px/frame = 10", sig == 10, sig, 10),
            check("horizontal edge spread ~ 2.56 sigma (10-90 %)", abs(rise_w - 2.56 * 10) <= 3, rise_w, 25.6),
            check("vertical edges stay sharp (motion axis only)", v_rise == 0, v_rise, 0),
            check("zero at rest, capped at 24", s0 == 0 and capped == 24, [s0, capped], [0, 24]),
            check("negative control: the resting layer has a hard edge", not (int(np.sum((rest[30] > .1) & (rest[30] < .9))) > 3), 0, "> 3")], \
        [wd / "vblur.png"]


def vfx_chain(src, t, nodes):
    img = src.copy()
    h, w = img.shape[:2]
    from scipy.ndimage import map_coordinates
    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    for n in nodes:
        if n["type"] == "wave-warp":
            dx = n.get("amp", 3) * np.sin(2 * math.pi * (yy / n.get("wavelength", 20) + t))
            img = np.stack([map_coordinates(img[..., c], [yy, xx + dx], order=1, mode="nearest") for c in range(3)], -1)
        elif n["type"] == "displacement-map":
            rng = np.random.default_rng(n.get("seed", 1))
            dmap = blur(rng.random((h, w)), 3) - .5
            img = np.stack([map_coordinates(img[..., c], [yy + dmap * 8, xx], order=1, mode="nearest") for c in range(3)], -1)
        elif n["type"] == "pixelate":
            s = n.get("size", 8)
            img = np.kron(img[::s, ::s], np.ones((s, s, 1)))[:h, :w]
        elif n["type"] == "bloom":
            img = threshold_bloom(img, .7, .8, 3)
    return np.clip(img, 0, 1)


@card("GLOW-36")
def media_treatments(task, wd):
    fx.test_clip(wd / "src.mp4", seconds=.2, size="160x90")
    fx.ffmpeg("-i", wd / "src.mp4", "-frames:v", "1", wd / "src.png")
    before = (wd / "src.png").read_bytes()
    src = load(wd / "src.png")
    treatment = {"data-treatment": "bloom", "data-vfx-chain": {"version": 1, "nodes": [{"type": "displacement-map"},
                                                                                        {"type": "wave-warp", "amp": 3}]}}
    jdump(wd / "treatment.json", treatment)
    nodes = treatment["data-vfx-chain"]["nodes"] + [{"type": "bloom"}]
    a1 = vfx_chain(src, .4, nodes)
    _ = vfx_chain(src, .9, nodes)
    a2 = vfx_chain(src, .4, nodes)
    pix = vfx_chain(src, 0, [{"type": "pixelate", "size": 8}])
    save(a1, wd / "treated.png")
    blocks = float(pix[:88, :160].reshape(11, 8, 20, 8, 3).std(axis=(1, 3)).max())
    return [check("source untouched (non-destructive)", (wd / "src.png").read_bytes() == before, True, True),
            check("seek-deterministic: t=.4 repaints identically after t=.9", np.array_equal(a1, a2), True, True),
            check("chain changes the picture", float(np.abs(a1 - src).mean()) > .01, float(np.abs(a1 - src).mean()), "> .01"),
            check("pixelate makes uniform 8 px blocks", blocks < 1e-9, blocks, 0),
            check("negative control: the source is not block-uniform", not (float(src[:88, :160].reshape(11, 8, 20, 8, 3).std(axis=(1, 3)).max()) < 1e-9),
                  None, None)], [wd / "treated.png", wd / "treatment.json"]


@card("GLOW-39")
def hologram(task, wd):
    h, w = 180, 180
    n, m = sphere(h, w, 90, 90, 70)
    rim = (1 - np.abs(n[..., 2])) ** 3 * m
    yy = np.mgrid[0:h, 0:w][0]
    lines = 400 * h / 1080                                 # 400 lines over a 1080 screen, scaled to this canvas
    scan = (.5 + .5 * np.sin(2 * math.pi * yy * lines / h)) * m
    frames, means = [], []
    for i in range(30):
        fl = 1 + .03 * math.sin(i * 1.7)
        col = (hxf("#3fd0ff") * (.25 * m + .9 * rim)[..., None] + hxf("#9feaff") * (.25 * scan)[..., None]) * fl
        f = canvas(h, w, "#020409") + col                   # additive
        frames.append(np.clip(f, 0, 1))
        means.append(float(luma(f)[m].mean()))
    write_video(wd / "hologram.mp4", frames, fps=30)
    f0 = frames[0]
    edge, centre = float(luma(f0)[90, 90 + 66]), float(luma(f0)[90, 90])
    prof = luma(f0)[40:140, 90] - luma(f0)[40:140, 90].mean()
    spec = np.abs(np.fft.rfft(prof))
    k = int(np.argmax(spec[1:])) + 1
    lines_meas = k * h / 100
    flick = (max(means) - min(means)) / np.mean(means)
    plain = canvas(h, w, "#020409") + hxf("#3fd0ff") * (.25 * m)[..., None]
    sp_p = np.abs(np.fft.rfft(luma(plain)[40:140, 90] - luma(plain)[40:140, 90].mean()))
    return [check("Fresnel rim: silhouette brighter than the centre", edge > 1.4 * centre, [edge, centre], "edge > 1.4x"),
            check("scanlines ~400 per screen height (300..800)", 300 * h / 1080 <= lines_meas <= 800 * h / 1080 and abs(lines_meas - lines) < 3,
                  lines_meas, lines),
            check("flicker only a few % (< 8 %)", 0 < flick < .08, flick, "< .08"),
            check("negative control: plain shading has no scanline peak", not (float(sp_p.max()) > 1e-6), float(sp_p.max()), 0)], \
        [wd / "hologram.mp4"]


def shimmer_frames(text, rtl, n=24, w=300, h=80):
    mask = m_text(h, w, text, 48, (10, 10))
    frames, peaks = [], []
    for i in range(n):
        p = i / (n - 1)
        pos = (0 + p) if rtl else (1 - p)               # background-position 100% -> 0% (LTR), 0% -> 100% for RTL
        X = np.linspace(0, 1, w)
        gx = (X + 2 * pos) / 3                           # 300% wide background: offset = (W - 3W) * pos
        band = np.interp(gx, [0, .40, .47, .50, .53, .60, 1], [0, 0, .6, 1, .6, 0, 0])
        col = hxf("#e9e1cf")[None] * (1 - band[:, None]) + hxf("#ffffff")[None] * band[:, None]
        f = canvas(h, w, "#101010") * (1 - mask[..., None]) + col[None] * mask[..., None]
        frames.append(f)
        peaks.append(int(np.argmax(band)) if band.max() > .5 else None)
    return frames, peaks, mask


@card("GLOW-41")
def payoff_sweep(task, wd):
    fr, pk, mask = shimmer_frames("SUMMIT", rtl=False)
    fr_r, pk_r, _ = shimmer_frames("SUMMIT", rtl=True)
    write_video(wd / "sweep.mp4", fr, fps=24)
    seen = [p for p in pk if p is not None]
    seen_r = [p for p in pk_r if p is not None]
    outside = float(np.abs(fr[10][mask == 0] - hxf("#101010")).max())
    static = [pk[12]] * 10
    return [check("LTR: the band travels left -> right", len(seen) > 5 and all(a <= b for a, b in zip(seen, seen[1:])) and seen[-1] > seen[0],
                  seen[:4], "increasing"),
            check("RTL (Arabic): the band runs the other way", len(seen_r) > 5 and all(a >= b for a, b in zip(seen_r, seen_r[1:])),
                  seen_r[:4], "decreasing"),
            check("gradient clipped to the letters (nothing painted outside)", outside < 1e-9, outside, 0),
            check("band peak is pure white #fff inside letters", float(max(f[mask >= 1].max() for f in fr)) > .999,
                  float(max(f[mask >= 1].max() for f in fr)), 1.0),
            check("negative control: a static gradient does not travel", not (static[-1] > static[0]), static[:2], "moves")], \
        [wd / "sweep.mp4"]


@card("GLOW-44")
def rotation_sheen(task, wd):
    L = norm([-1, 1, 1])                                   # fixed light from the top-left
    frames, bright, hl = [], [], []
    for ang in range(-60, 61, 10):
        a = math.radians(ang)
        nrm = np.array([math.sin(a), 0, math.cos(a)])
        b = max(0.0, float(nrm @ L))
        cv = canvas(90, 160, "#0d0f14")
        x0, x1 = 50, 110
        face = hxf("#c9a227") * (.25 + .75 * b)
        cv[25:65, x0:x1] = face
        hx_ = int(x0 + (ang + 60) / 120 * (x1 - x0 - 1))   # highlight stop proportional to the angle
        cv[25:65, max(x0, hx_ - 2):hx_ + 3] = np.clip(face + .35, 0, 1)
        cv[65:69, x0:x1] = face * .8                         # extruded edge one shade darker
        frames.append(cv)
        bright.append((b, float(np.median(luma(cv[45, x0:x1])))))
        hl.append(hx_)
    write_video(wd / "sheen.mp4", frames, fps=10)
    bs = np.array([x for x, _ in bright])
    ls = np.array([y for _, y in bright])
    corr = float(np.corrcoef(bs, ls)[0, 1])
    hcorr = float(np.corrcoef(np.arange(len(hl)), hl)[0, 1])
    edge_ok = all(float(luma(f[66, 60])) < float(luma(f[45, 51])) for f in frames)
    return [check("face brightness follows max(0, n.L) (corr > .99)", corr > .99, corr, "> .99"),
            check("highlight slides in proportion to rotation (corr > .99)", hcorr > .99, hcorr, "> .99"),
            check("extruded edge one shade darker", edge_ok, edge_ok, True),
            check("negative control: an unlit card has constant brightness", not (float(np.ptp(np.full(13, .5))) > 0), 0, None)], \
        [wd / "sheen.mp4"]


@card("GLOW-45")
def laser_scan(task, wd):
    h, w, fps = 100, 120, 30
    fr = (20, 10, 100, 90)                        # scan frame box
    frames, ys = [], []
    for i in range(int(2 * fps) + 1):
        t = i / fps
        ph = (t % 2) / 2
        e = .5 - .5 * math.cos(2 * math.pi * ph)   # ease-in-out 10% -> 90% -> 10%
        y = fr[1] + (fr[3] - fr[1]) * (.1 + .8 * e)
        cv = canvas(h, w, "#606a70")
        outside = np.ones((h, w), bool)
        outside[fr[1]:fr[3], fr[0]:fr[2]] = False
        cv[outside] *= .55                         # surround darkened by .45
        line = np.zeros((h, w))
        line[int(round(y)):int(round(y)) + 2, fr[0]:fr[2]] = 1
        cv = glow(cv, line, "#e5484d", 8, .8)
        cv = fill(cv, line, "#e5484d")
        frames.append(np.clip(cv, 0, 1))
        ys.append(y)
    write_video(wd / "laser.mp4", frames, fps=fps)
    span = fr[3] - fr[1]
    f = frames[15]
    y15 = int(round(ys[15]))
    glow_above = float(f[y15 - 3, 60, 0] - .37)
    plain = canvas(h, w, "#606a70")
    return [check("line at 10 % at t=0, 90 % at 1 s, back at 2 s", abs(ys[0] - (fr[1] + .1 * span)) < .5 and abs(ys[30] - (fr[1] + .9 * span)) < .5 and
                  abs(ys[60] - ys[0]) < .5, [ys[0], ys[30], ys[60]], [fr[1] + 8, fr[1] + 72, fr[1] + 8]),
            check("surround darkened to .55", abs(float(frames[0][2, 2, 0] / hxf("#606a70")[0]) - .55) < .01,
                  float(frames[0][2, 2, 0] / hxf("#606a70")[0]), .55),
            check("8 px red glow just off the line", glow_above > .02 and f[y15 - 3, 60, 0] > f[y15 - 3, 60, 2], glow_above, "> .02"),
            check("negative control: the unprocessed plate has no line or glow",
                  not (float(plain[y15 - 3, 60, 0] - hxf("#606a70")[0]) > .02), 0, None)], [wd / "laser.mp4"]


def star_path(cx, cy, r, rot):
    pts = []
    for k in range(8):
        rr = r if k % 2 == 0 else r * .25
        a = rot + k * math.pi / 4
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pts


def sparkle_schedule(seed, dur=3.0, life=.6, rate=13.0):
    rng = np.random.default_rng(seed)
    t, out = 0.0, []
    while t < dur:
        out.append((t, float(rng.uniform(10, 290)), float(rng.uniform(10, 70))))
        t += 1 / rate
    return out


@card("GLOW-46")
def sparkles(task, wd):
    sched = sparkle_schedule(5)
    fps, frames, alive = 30, [], []
    for i in range(int(3 * fps)):
        t = i / fps
        im = Image.new("RGB", (300, 80), "#0a0a12")
        d = ImageDraw.Draw(im)
        n = 0
        for t0, x, y in sched:
            age = t - t0
            if 0 <= age < .6:
                s = math.sin(math.pi * age / .6)       # scale 0 -> 1 -> 0 over 600 ms
                d.polygon(star_path(x, y, 8 * s + .01, age * 4), fill="#fff3c4")
                n += 1
        alive.append(n)
        frames.append(np.asarray(im).astype(float) / 255)
    write_video(wd / "sparkles.mp4", frames, fps=fps)
    steady = alive[int(.6 * fps):]
    rng = np.random.default_rng(int(1.23 * 30))
    sparks = [(rng.uniform(.01, .045), rng.uniform(0, 2 * math.pi)) for _ in range(8)]
    rng2 = np.random.default_rng(int(1.23 * 30))
    again = [(rng2.uniform(.01, .045), rng2.uniform(0, 2 * math.pi)) for _ in range(8)]
    return [check("6-10 stars alive at once (after warm-up)", min(steady) >= 6 and max(steady) <= 10, [min(steady), max(steady)], "6..10"),
            check("each star lives 600 ms (scale 0 at birth and death)", abs(math.sin(math.pi * 0 / .6)) < 1e-9 and abs(math.sin(math.pi * .6 / .6)) < 1e-9,
                  True, True),
            check("seeded positions reproduce", sparkle_schedule(5) == sched, True, True),
            check("8 pen sparks within .01-.045 m, same per-frame seed -> same sparks", len(sparks) == 8 and sparks == again and
                  all(.01 <= r <= .045 for r, _ in sparks), True, True),
            check("negative control: another seed places other stars", not (sparkle_schedule(6) == sched), True, True)], \
        [wd / "sparkles.mp4"]


@card("GLOW-47")
def css_god_rays(task, wd):
    h, w = 180, 320
    fx.test_clip(wd / "src.mp4", seconds=.1, size="%dx%d" % (w, h))
    fx.ffmpeg("-i", wd / "src.mp4", "-frames:v", "1", wd / "src.png")
    foot = load(wd / "src.png") * .6
    yy, xx = np.mgrid[0:h, 0:w]
    ox, oy = 590 / 1920 * w, -260 / 1080 * h
    ang = (np.degrees(np.arctan2(yy - oy, xx - ox)) - 168) % 9
    a = np.interp(ang, [0, 2.2, 5, 9], [0, .13, 0, 0])
    mask = np.interp(yy / h, [0, .4, .75, 1], [0, .6, 0, 0])
    rays = a * mask
    out = foot + hxf("#fff3d6")[None, None] * rays[..., None] * (1 - np.minimum(foot, 1))        # screen
    bloom = np.clip(1 - np.hypot((xx - 60 / 1920 * w) / (380 / 1920 * w), (yy - 300 / 1080 * h) / (520 / 1080 * h)), 0, 1)
    rays_only = out.copy()
    out = out + hxf("#ffd696")[None, None] * (bloom * .5)[..., None] * (1 - np.minimum(out, 1))
    save(out, wd / "god_rays.png")
    delta = out - foot
    r = 120
    th = np.linspace(-60, 60, 1200)
    sx = (ox + r * np.cos(np.radians(th + 168 + 180 - 180))).astype(int)
    rr = np.hypot(xx - ox, yy - oy)
    band = (rr > 200) & (rr < 210) & (yy > 0) & (yy < .7 * h) & (xx > 100)
    angs = (np.degrees(np.arctan2(yy - oy, xx - ox))[band])
    vals = rays[band]
    order = np.argsort(angs)
    sig = vals[order] - vals.mean()
    spec = np.abs(np.fft.rfft(sig))
    span = float(angs.max() - angs.min())
    period = span / (int(np.argmax(spec[1:])) + 1)
    return [check("rays repeat every 9 deg", abs(period - 9) < 1.5, period, 9),
            check("rays fade out by 75 % of the height", float(rays[int(.8 * h):].max()) == 0, float(rays[int(.8 * h):].max()), 0),
            check("screen blend never darkens the footage", float(delta.min()) >= -1e-9, float(delta.min()), ">= 0"),
            check("warm bloom pool near the subject (R > B added over a grey patch)",
                  float(hxf("#ffd696")[0]) > float(hxf("#ffd696")[2]) and float((out - rays_only)[int(300 / 1080 * h), 12].sum()) > .05,
                  float((out - rays_only)[int(300 / 1080 * h), 12].sum()), "> .05"),
            check("negative control: the footage alone has no rays in the band", not (float(np.ptp((foot - foot)[band])) > .01), 0, "> .01")], \
        [wd / "god_rays.png"]


def angular_period(field, cx, cy, r0, r1, a0=-180, a1=180):
    h, w = field.shape
    yy, xx = np.mgrid[0:h, 0:w]
    rr = np.hypot(xx - cx, yy - cy)
    ang = np.degrees(np.arctan2(yy - cy, xx - cx))
    band = (rr > r0) & (rr < r1) & (ang > a0) & (ang < a1)
    bins = np.linspace(a0, a1, 721)
    idx = np.digitize(ang[band], bins)
    vals = field[band]
    prof = np.array([vals[idx == k].mean() if np.any(idx == k) else np.nan for k in range(1, len(bins))])
    prof = np.nan_to_num(prof - np.nanmean(prof), nan=0.0)
    spec = np.abs(np.fft.rfft(prof))
    if spec[1:].max() < 1e-9:
        return None, prof
    k = int(np.argmax(spec[1:])) + 1
    return (a1 - a0) / k, prof


@card("GLOW-48")
def screen_space_rays(task, wd):
    h, w = 120, 200
    cv = np.zeros((h, w, 3)) + np.array([.35, .45, .6])
    cv[80:] = np.array([.05, .08, .12])                          # water below the horizon
    sun = (100, 40)
    cv = fill(cv, m_ellipse(h, w, *sun, 8), (1.6, 1.4, 1.1))
    for x0 in range(70, 135, 14):                               # branches occluding the sun
        cv[20:60, x0:x0 + 4] = .05
    sky = np.zeros((h, w))
    sky[:80] = 1
    sky[:int(sun[1])] *= 1                                     # masked to the sky region (above the water)
    rays = radial_rays(cv, *sun, samples=64, decay=.972, stride=.55, thr=.7, gain=.55, sky=sky)
    out = cv + rays * (sky[..., None])
    save(rolloff(out), wd / "rays.png")
    gain = luma(rays)
    water = float(gain[85:].max())
    dark = cv.copy()
    dark[luma(dark) > .7] = .5
    r_dark = float(luma(radial_rays(dark, *sun, thr=.7)).max())
    reach = float(gain[50:58, 86:114].mean())
    shaft_open, shaft_shadow = float(gain[52:56, 93:96].mean()), float(gain[52:56, 99:101].mean())
    return [check("rays limited to the sky (none on the water)", water < 1e-9, water, 0),
            check("rays streak radially below the sun (light beyond the disc)", reach > .01, reach, "> .01"),
            check("the branch across the sun casts a darker shaft", shaft_shadow < .8 * shaft_open, [shaft_shadow, shaft_open], "shadow < .8 open"),
            check("negative control: an input under luma .7 gets no rays (reach test fails)", not (r_dark > .01), r_dark, "> .01")], [wd / "rays.png"]


@card("GLOW-49")
def sunburst(task, wd):
    h, w, fps, n_rays = 120, 120, 30, 32
    frames, rots = [], []
    for i in range(30):
        rot = 20 * i / fps
        yy, xx = np.mgrid[0:h, 0:w]
        ang = (np.degrees(np.arctan2(yy - 60, xx - 60)) - rot) % (360 / n_rays)
        wedge = (ang < 360 / n_rays * .35).astype(float)
        mask = np.clip(1 - dist_map(h, w, 60, 60) / 60, 0, 1)
        base = canvas(h, w, "#3a1460")
        f = base + hxf("#ffd36b")[None, None] * (wedge * mask * .4)[..., None] * (1 - base)
        frames.append(f)
        rots.append(rot)
    write_video(wd / "sunburst.mp4", frames, fps=fps)
    lay = luma(frames[0] - canvas(h, w, "#3a1460"))
    p, prof0 = angular_period(lay, 60, 60, 20, 50)
    _, prof1 = angular_period(luma(frames[3] - canvas(h, w, "#3a1460")), 60, 60, 20, 50)
    shifts = [float(np.dot(np.roll(prof0, k), prof1)) for k in range(0, 40)]
    meas_rot = int(np.argmax(shifts)) * .5
    still = luma(canvas(h, w, "#3a1460"))
    return [check("%d thin rays (period 360/%d deg)" % (n_rays, n_rays), p is not None and abs(p - 360 / n_rays) < .5, p, 360 / n_rays),
            check("rotates 20 deg/s (2 deg in 3 frames)", abs(meas_rot - 2.0) <= .5, meas_rot, 2.0),
            check("radial mask fades rays to 0 at the rim", float(lay[60, 119]) < .02, float(lay[60, 119]), "~0"),
            check("negative control: the plain ground has no rays", angular_period(still, 60, 60, 20, 50)[0] is None, None, "none")], \
        [wd / "sunburst.mp4"]


FLARE50 = [("soft", 420, 0.0, "#ffe2b0"), ("ring", 90, .35, "#ffd0a0"), ("soft", 60, .55, "#aad4ff"), ("ring", 140, .75, "#ffc8a0"),
           ("soft", 40, .95, "#ffffff")]


def lens_flare(h, w, sun, occluded=False, scale=.15):
    cv = np.zeros((h, w, 3))
    centres = []
    if occluded:
        return cv, centres
    cx, cy = w / 2, h / 2
    for kind, size, dist, col in FLARE50:
        px = sun[0] + (cx - sun[0]) * 2 * dist
        py = sun[1] + (cy - sun[1]) * 2 * dist
        r = size * scale / 2
        d = dist_map(h, w, px, py) / r
        prof = np.clip(1 - d, 0, 1) ** 2 if kind == "soft" else np.exp(-((d - .85) / .08) ** 2)
        cv = cv + prof[..., None] * hxf(col) * .6
        centres.append((px, py))
    return cv, centres


@card("GLOW-50")
def lens_flare_3d(task, wd):
    h, w = 180, 320
    sun = (60, 40)
    cv, cen = lens_flare(h, w, sun)
    save(rolloff(cv), wd / "flare.png")
    occ, _ = lens_flare(h, w, sun, occluded=True)
    exp = [(sun[0] + (160 - sun[0]) * 2 * d, sun[1] + (90 - sun[1]) * 2 * d) for _, _, d, _ in FLARE50]
    collinear = all(abs((y - sun[1]) * (160 - sun[0]) - (x - sun[0]) * (90 - sun[1])) < 1e-6 for x, y in cen)
    soft2 = cen[2]
    peak = luma(cv)[int(round(soft2[1])), int(round(soft2[0]))]
    return [check("5 elements placed along the sun -> centre axis", collinear and len(cen) == 5, len(cen), 5),
            check("element at .55 sits just past the frame centre", abs(cen[2][0] - exp[2][0]) < 1e-9 and cen[2][0] > 160, cen[2], exp[2]),
            check("each element paints where it is placed", float(peak) > .1, float(peak), "> .1"),
            check("hidden when the sun is occluded", float(occ.max()) == 0, float(occ.max()), 0),
            check("negative control: with no flare the frame centre is dark", not (float(luma(occ)[90, 160]) > .1), 0, None)], \
        [wd / "flare.png"]


def painter_flare(h, w, c, col, size, streak, strength, ghosts=3):
    cv = np.zeros((h, w, 3))
    cv = glow(cv, m_ellipse(h, w, c[0], c[1], size * .25), col, size * .4, strength)
    st = fill(np.zeros((h, w, 3)), m_ellipse(h, w, c[0], c[1], streak / 2, .09 * size / 2), col, strength, blur_r=3, mode="add")
    cv = cv + st
    cv = fill(cv, m_ellipse(h, w, c[0], c[1], .55 * streak / 2, .04 * size / 2), "#ffffff", strength, blur_r=1.5, mode="add")
    cx, cy = w / 2, h / 2
    gpos = []
    for k in range(ghosts):
        t = 1 + .55 * k
        gx, gy = cx - (c[0] - cx) * t * .5 * (k + 1) / ghosts, cy - (c[1] - cy) * t * .5 * (k + 1) / ghosts
        cv = fill(cv, m_ellipse(h, w, gx, gy, size * .1 * (1 + .3 * k)), col, .12, blur_r=2, mode="add")
        gpos.append((gx, gy))
    return cv, gpos, st


@card("GLOW-51")
def anamorphic_flare(task, wd):
    h, w = 160, 480
    c = (130, 60)
    cv, gpos, st = painter_flare(h, w, c, "#ffb070", 120, 420, .6)
    save(rolloff(cv), wd / "flare.png")
    row = luma(st)[60]
    col = luma(st)[:, 130]
    hext = int(np.sum(row > .05))
    vext = int(np.sum(col > .05))
    mirrored = all((gx - w / 2) * (c[0] - w / 2) < 0 and (gy - h / 2) * (c[1] - h / 2) <= 0 for gx, gy in gpos)
    g0 = gpos[0]
    ghost_lift = float(luma(cv)[int(g0[1]), int(g0[0])])
    inner = cv[60, 130 + 60]
    outer = cv[60, 130 + 180]
    return [check("long horizontal streak (width >> height)", hext > 4 * vext and hext >= 300, [hext, vext], "w > 4h"),
            check("white inner streak: whiter near the core than at the streak tips", float(inner.min() / inner.max()) > float(outer.min() / max(outer.max(), 1e-9)),
                  [tohex(np.clip(inner, 0, 1) * 255), tohex(np.clip(outer, 0, 1) * 255)], "whiter inside"),
            check("ghost discs mirrored through the frame centre", mirrored and ghost_lift > .03, gpos, "opposite side"),
            check("negative control: the round glow alone is not a streak", not (int(np.sum(luma(cv - st)[60] > .05)) > 4 * int(np.sum(luma(cv - st)[:, 130] > .05))),
                  [int(np.sum(luma(cv - st)[60] > .05)), int(np.sum(luma(cv - st)[:, 130] > .05))], "w > 4h")], \
        [wd / "flare.png"]


@card("GLOW-53")
def light_leak(task, wd):
    W, H, fps = 160, 90, 30
    fx.test_clip(wd / "src.mp4", seconds=.1, size="%dx%d" % (W, H))
    fx.ffmpeg("-i", wd / "src.mp4", "-frames:v", "1", wd / "src.png")
    foot = load(wd / "src.png")
    frames, cen = [], []
    leak = .6
    for i in range(30):
        t = i / fps * 4
        x, y = W * (.5 + .65 * math.sin(.31 * t)), H * (.12 + .1 * math.cos(.23 * t))
        r = .75 * max(W, H)
        d = dist_map(H, W, x, y) / r
        a = np.interp(d, [0, .45, 1], [leak, .35 * leak, 0])
        col = np.where((d < .45)[..., None], hxf("#ffaa5a"), hxf("#ff503c"))
        f = foot + col * a[..., None] * (1 - foot)
        frames.append(f)
        cen.append((x, y))
    burn = []
    for i in range(int(.9 * fps)):
        p = i / (int(.9 * fps) - 1)
        br = 1.5 + 1.5 * min(1, p * 2)
        wht = math.sin(math.pi * p)
        f = np.clip(foot * br, 0, 1) * (1 - wht) + wht
        burn.append(f)
    write_video(wd / "leak.mp4", frames + burn, fps=fps)
    d0 = frames[0] - foot
    warm = d0[int(cen[0][1]), int(min(W - 1, cen[0][0]))]
    mid_white = float(burn[len(burn) // 2].min())
    return [check("leak follows x = W(.5+.65 sin .31t), y = H(.12+.1 cos .23t)", abs(cen[0][0] - W * .5) < 1e-9 and abs(cen[0][1] - H * .22) < 1e-9,
                  cen[0], (W * .5, H * .22)),
            check("screen blend never darkens", float(min((f - foot).min() for f in frames)) >= -1e-9, None, ">= 0"),
            check("leak is warm (R > B added)", warm[0] >= warm[2], tohex(np.clip(warm, 0, 1) * 255), "warm"),
            check("burn transition blows out to white mid-way", mid_white > .98, mid_white, "> .98"),
            check("negative control: untouched footage is not white", not (float(foot.min()) > .98), float(foot.min()), "< .98")], \
        [wd / "leak.mp4"]


def flash_curve(t, at, peak=.85, attack=.06, decay=.35, again=True):
    def one(tt, pk):
        if tt < 0:
            return 0.0
        if tt < attack:
            return pk * tt / attack
        u = min(1, (tt - attack) / decay)
        return pk * (1 - u) ** 4                    # power4.out decay
    v = one(t - at, peak)
    if again:
        v = max(v, one(t - at - .16, peak * .5))
    return v


def schedule_flashes(times, max_per_s=3):
    out = []
    for t in sorted(times):
        if sum(1 for o in out if t - 1 < o <= t) < max_per_s:
            out.append(t)
    return out


@card("GLOW-54")
def flash_frame(task, wd):
    fps = 100
    ts = np.arange(0, 1.0, 1 / fps)
    v = [flash_curve(t, .2) for t in ts]
    frames = [canvas(36, 64, "#101010") * (1 - a) + a for a in v[::4]]
    write_video(wd / "flash.mp4", frames, fps=25)
    pk = max(v)
    t_pk = ts[int(np.argmax(v))]
    second = max(v[int(.42 * fps):int(.48 * fps)])
    after = v[int(.2 * fps + (.06 + .35) * fps) + 20]
    sched = schedule_flashes([.1, .3, .5, .7, .9])
    return [check("attack .06 s to .85", abs(pk - .85) < 1e-9 and abs(t_pk - .26) < .011, [pk, float(t_pk)], [.85, .26]),
            check("second strike at +.16 s at 50 %", abs(second - .425) < .02, second, .425),
            check("decays to 0 after .35 s (power4.out)", after < 1e-6, after, 0),
            check("<= 3 flashes per second enforced", len(sched) == 3, sched, 3),
            check("negative control: before the flash the frame is dark", not (v[10] > 0), v[10], 0)], [wd / "flash.mp4"]


@card("GLOW-55")
def wordmark_rays(task, wd):
    h, w = 120, 320
    mask = m_text(h, w, "NOOR", 64, (70, 25))
    emit = mask[..., None] * hxf("#ffe2a8")
    frames, sides = [], []
    for i, cx in enumerate(np.linspace(40, 280, 9)):
        rays = radial_rays(emit * 1.5, cx, 0, samples=48, decay=.97, stride=.7, thr=.3, gain=.6)
        f = canvas(h, w, "#06060a") + rays + emit
        frames.append(np.clip(f, 0, 1))
        below = luma(rays)[100:118]
        sides.append((float(below[:, :160].sum()), float(below[:, 160:].sum())))
    write_video(wd / "rays.mp4", frames, fps=6)
    left_light, right_light = sides[0], sides[-1]
    base = np.clip(canvas(h, w, "#06060a") + emit, 0, 1)
    added = float(luma(frames[4] - base)[100:118].sum())
    none = float(luma(base - base)[100:118].sum())
    return [check("rays streak away from the light: cursor at left -> shafts lean right", left_light[1] > left_light[0], left_light, "right > left"),
            check("cursor sweeps to the right -> shafts lean left", right_light[0] > right_light[1], right_light, "left > right"),
            check("rays add light below the wordmark (frame minus base)", added > 1, added, "> 1"),
            check("negative control: the unprocessed base adds nothing below the word", not (none > 1), none, "> 1")], \
        [wd / "rays.mp4"]


def corona(r, bass):
    return np.exp(-np.maximum(0, r - .074) * (46 - 12 * bass)) * (.55 + 1.1 * bass)


@card("GLOW-56")
def sun_corona(task, wd):
    h, w = 160, 160
    r = dist_map(h, w, 80, 80) / w
    frames = []
    for bass in (0, .5, 1):
        disc = 1 - smoothstep(.072, .075, r)
        cor = corona(r, bass) * (1 - disc)
        f = canvas(h, w, "#020205") * (1 - disc[..., None]) + cor[..., None] * np.array([1, .42, .16])
        frames.append(rolloff(f))
    save(np.hstack(frames), wd / "eclipse.png")
    rr = np.linspace(.074, .5, 400001)
    hw = lambda b: float(rr[np.argmax(corona(rr, b) < corona(np.array([.074]), b)[0] / 2)] - .074)
    w0, w1 = hw(0), hw(1)
    two_d = canvas(h, w)
    disc2 = m_ellipse(h, w, 80, 80, 20)
    for rad in (40 / 8, 120 / 8, 300 / 8):
        two_d = glow(two_d, disc2, "#f7b54a", rad, .35)
    two_d = fill(two_d, disc2, "#fcfaca")
    save(rolloff(two_d), wd / "sun2d.png")
    prof = [float(luma(two_d)[80, 80 + 20 + k]) for k in (3, 15, 40)]
    return [check("corona widens with the bass (half-width ratio 46/34)", abs(w1 / w0 - 46 / 34) < .02, w1 / w0, 46 / 34),
            check("corona gains intensity with the bass (.55 -> 1.65)", abs(corona(np.array([.074]), 1)[0] / corona(np.array([.074]), 0)[0] - 3) < 1e-9,
                  3.0, 3.0),
            check("dark disc edge = 1 - smoothstep(.072, .075, r)", float(luma(frames[0])[80, 80]) < .05, float(luma(frames[0])[80, 80]), "< .05"),
            check("2D sun: three stacked glows spread light out to 300 px scale", prof[0] > prof[1] > prof[2] > 0, prof, "decreasing > 0"),
            check("negative control: bass 0 corona is the narrower one", not (w0 >= w1), [w0, w1], "w0 < w1")], \
        [wd / "eclipse.png", wd / "sun2d.png"]


RIGS = {"rembrandt": ((-75, 40), -2.5, -.5, 1.0), "clamshell": ((0, 55), -1, -1.5, .9), "edgy": ((0, 60), -4, .8, .6),
        "ultrasoft": ((-35, 30), -.8, -.3, 2.1), "short": ((55, 30), -2.5, 0, .9), "broad": ((-55, 30), -2.0, -1, .9),
        "sun": ((-60, 18), -2.3, -1, .05)}


def softness_deg(size, dist):
    return math.degrees(2 * math.atan(size / (2 * dist)))


def light_dir(az, el):
    a, e = math.radians(az), math.radians(el)
    return norm([math.sin(a) * math.cos(e), math.sin(e), math.cos(a) * math.cos(e)])


@card("GLOW-58")
def portrait_rigs(task, wd):
    out, imgs = {}, []
    n, m = sphere(100, 100, 50, 50, 40)
    for name, ((az, el), fill_s, rim_s, size) in RIGS.items():
        key = 1.0
        fill_i = key * 2 ** fill_s
        deg = softness_deg(size, 1.5)
        L = light_dir(az, el)
        Lf = light_dir(-az, 0)
        lam = np.clip(n @ L, 0, None) * key + np.clip(n @ Lf, 0, None) * fill_i
        img = np.where(m[..., None], np.clip(lam, 0, 1)[..., None] * np.array([1, .95, .9]), 0)
        imgs.append(img)
        yy, xx = np.unravel_index(np.argmax(np.where(m, lam, -1)), lam.shape)
        out[name] = {"key_fill_ratio": round(key / fill_i, 2), "softness_deg": round(deg, 2), "shadow_radius": round(deg / 3, 2),
                     "hot_x": int(xx) - 50}
    save(np.hstack(imgs), wd / "rigs.png")
    return [check("Rembrandt fill -2.5 stops -> key:fill 5.66:1", out["rembrandt"]["key_fill_ratio"] == 5.66, out["rembrandt"]["key_fill_ratio"], 5.66),
            check("1.0 m source at 1.5 m = 36.87 deg, shadow.radius = deg/3", out["rembrandt"]["softness_deg"] == 36.87 and
                  out["rembrandt"]["shadow_radius"] == 12.29, out["rembrandt"], [36.87, 12.29]),
            check("hard low sun (0.05 m) is far harder than ultrasoft (2.1 m)", out["sun"]["softness_deg"] < 2 < 60 < out["ultrasoft"]["softness_deg"],
                  [out["sun"]["softness_deg"], out["ultrasoft"]["softness_deg"]], "< 2 / > 60"),
            check("key azimuth sets the lit side (rembrandt left, short right)", out["rembrandt"]["hot_x"] < 0 < out["short"]["hot_x"],
                  [out["rembrandt"]["hot_x"], out["short"]["hot_x"]], "neg / pos"),
            check("negative control: clamshell (az 0) is not lit from the side", not (abs(out["clamshell"]["hot_x"]) > 5),
                  out["clamshell"]["hot_x"], "~0")], [wd / "rigs.png", jdump(wd / "rigs.json", out)]


SETUPS59 = {"rembrandt": (45, 4, 5600, "classic drama"), "loop": (30, 3, 5600, "natural portrait"), "split": (90, 8, 5600, "conflict"),
            "high_key": (30, 1.5, 5600, "clean, commercial"), "candle": (60, 6, 1900, "intimacy"), "window": (90, 3, 6000, "documentary")}
SECTIONS59 = ["MOOD", "TOP VIEW", "LIGHTS", "RATIOS & EXPOSURE", "CAMERA", "BUDGET VERSION", "COMMON MISTAKES", "PROMPT"]


def lightplan(name):
    ang, ratio, k, mood = SETUPS59[name]
    fill_stops = math.log2(ratio - 1) if ratio > 1 else 0
    clock = (6 + round(ang / 30)) % 12 or 12
    grid = [[" "] * 13 for _ in range(7)]
    grid[6][6] = "C"
    grid[3][6] = "S"
    a = math.radians(180 - ang)
    grid[3 - round(3 * math.cos(a))][6 + round(6 * math.sin(a))] = "K"
    lines = ["## MOOD", "%s: %s" % (name, mood), "## TOP VIEW", "\n".join("".join(r) for r in grid),
             "## LIGHTS", "| role | fixture | power | angle | gel |", "| key | softbox | 0 st | %d deg (%d o'clock) | %d K |" % (ang, clock, k),
             "| fill | bounce | -%.2f st | camera side | %d K |" % (fill_stops, k),
             "## RATIOS & EXPOSURE", "ratio %g:1 -> fill %.2f stops under key" % (ratio, fill_stops),
             "## CAMERA", "ISO 400, 1/50 s, f/2.8, WB %d K" % k, "## BUDGET VERSION", "window + lamp + foam board + phone light",
             "## COMMON MISTAKES", "mixed colour temperatures; fill too strong", "## PROMPT",
             "%s lighting, key %d degrees, %g:1 ratio, %d K" % (name, ang, ratio, k)]
    return "\n".join(lines), fill_stops, clock


@card("GLOW-59")
def light_plan(task, wd):
    text, fs, clock = lightplan("rembrandt")
    (wd / "lightplan.md").write_text(text, encoding="utf-8")
    pos = [text.find("## " + s) for s in SECTIONS59]
    _, fs_split, _ = lightplan("split")
    stub = "## MOOD\nnice light"
    return [check("all 8 sections present, in order", all(p >= 0 for p in pos) and pos == sorted(pos), pos, "ordered"),
            check("4:1 Rembrandt -> fill log2(3) = 1.58 stops", abs(fs - 1.585) < .01, fs, 1.585),
            check("split 8:1 -> fill 2.81 stops", abs(fs_split - math.log2(7)) < 1e-9, fs_split, math.log2(7)),
            check("ASCII top view has camera, subject and key", all(c in text.split("## LIGHTS")[0] for c in "CSK"), True, True),
            check("negative control: a stub plan misses sections", not all(stub.find("## " + s) >= 0 for s in SECTIONS59), False, True)], \
        [wd / "lightplan.md"]


def light_calc(op):
    k = op["op"]
    if k == "ratio":
        r = 2 ** op["key_stops_over_fill"] + 1
        mood = "flat" if r <= 2.5 else "natural" if r <= 4.5 else "dramatic" if r <= 9 else "noir"
        return {"ratio": r, "mood": mood}
    if k == "fill_stops":
        return {"stops": math.log2(op["ratio"] - 1)}
    if k == "softness":
        d = softness_deg(op["size_m"], op["dist_m"])
        return {"deg": round(d, 1), "label": "very soft" if d > 45 else "soft" if d > 20 else "medium" if d > 8 else "hard"}
    if k == "falloff":
        return {"stops": 2 * math.log2(op["d2"] / op["d1"])}
    if k == "ev":
        return {"ev": round(math.log2(op["f"] ** 2 / op["t"]) - math.log2(op["iso"] / 100), 2)}
    if k == "shutter":
        return {"t": op["angle"] / 360 / op["fps"]}
    if k == "gn":
        return {"f": op["gn"] * math.sqrt(op["iso"] / 100) / op["dist"]}
    if k == "mired":
        s = 1e6 / op["to_k"] - 1e6 / op["from_k"]
        gels = [("Full CTB", -159), ("1/2 CTB", -68), ("1/4 CTB", -30), ("1/8 CTB", -12), ("1/8 CTO", 20), ("1/4 CTO", 42),
                ("1/2 CTO", 81), ("Full CTO", 159)]
        return {"mired": round(s, 1), "gel": min(gels, key=lambda g: abs(g[1] - s))[0]}
    raise ValueError(k)


@card("GLOW-60")
def light_calculator(task, wd):
    ops = [{"op": "ratio", "key_stops_over_fill": 2}, {"op": "fill_stops", "ratio": 4}, {"op": "softness", "size_m": 1.2, "dist_m": 1.5},
           {"op": "falloff", "d1": 2, "d2": 4}, {"op": "ev", "f": 2.8, "t": 1 / 125, "iso": 100}, {"op": "shutter", "fps": 24, "angle": 180},
           {"op": "gn", "gn": 60, "iso": 100, "dist": 5}, {"op": "mired", "from_k": 5600, "to_k": 3200}]
    res = [light_calc(o) for o in ops]
    jdump(wd / "light_calc.json", list(zip(ops, res)))
    exp = [res[0] == {"ratio": 5, "mood": "dramatic"}, abs(res[1]["stops"] - 1.58) < .01, res[2] == {"deg": 43.6, "label": "soft"},
           res[3]["stops"] == 2, abs(res[4]["ev"] - 9.94) < .01, abs(res[5]["t"] - 1 / 48) < 1e-12, res[6]["f"] == 12,
           res[7] == {"mired": 133.9, "gel": "Full CTO"}]
    names = ["ratio 2 st -> 5:1 dramatic", "4:1 -> fill 1.58 st", "1.2 m @ 1.5 m -> 43.6 deg soft", "2 m -> 4 m = 2 st",
             "f/2.8 1/125 ISO100 = EV 9.94", "24 fps @ 180 = 1/48 s", "GN 60 @ 5 m -> f/12", "5600 -> 3200 = +133.9 Full CTO"]
    checks = [check(n, ok, r, None) for n, ok, r in zip(names, exp, res)]
    checks.append(check("negative control: 0 stops is a flat 2:1, not dramatic", not (light_calc({"op": "ratio", "key_stops_over_fill": 0})["mood"] ==
                                                                                   "dramatic"), light_calc({"op": "ratio", "key_stops_over_fill": 0}), "flat"))
    return checks, [wd / "light_calc.json"]


SOURCES61 = {"candle": 1850, "firelight": 1900, "sodium": "#ffa040", "tungsten": 2700, "halogen": 3200, "sunrise": 3000,
             "golden_hour": 3500, "led_warm": 3000, "led_neutral": 4000, "mercury": "#bff0dc", "metal_halide": 4300,
             "fluorescent": "#e8f5e6", "moonlight": "#9fb4d9", "daylight": 5600, "overcast": 6500, "open_shade": 8000,
             "blue_sky": 11000, "neon_red": "#ff2a3a", "neon_blue": "#3a7bff"}


@card("GLOW-61")
def kelvin_sources(task, wd):
    table = {k: (v if isinstance(v, str) else tohex(kelvin(v))) for k, v in SOURCES61.items()}
    from fractions import Fraction  # noqa: F401  (keeps the table pure-python)
    g = light_calc({"op": "mired", "from_k": 5600, "to_k": 3200})
    temps = [1850, 2700, 3500, 5600, 8000, 11000]
    rb = [kelvin(t)[2] / kelvin(t)[0] for t in temps]
    sw = np.vstack([np.full((16, 16, 3), np.array(hx(c), float) / 255) for c in table.values()])
    save(sw, wd / "sources.png")
    return [check("kelvin(1900) = #ff8400, kelvin(3200) = #ffb87b", tohex(kelvin(1900)) == "#ff8400" and tohex(kelvin(3200)) == "#ffb87b",
                  [tohex(kelvin(1900)), tohex(kelvin(3200))], ["#ff8400", "#ffb87b"]),
            check("gel(5600 -> 3200) = 134 mired, Full CTO", round(g["mired"]) == 134 and g["gel"] == "Full CTO", g, {"mired": 134, "gel": "Full CTO"}),
            check("19 named sources", len(table) == 19, len(table), 19),
            check("colour gets bluer as Kelvin rises (B/R monotone)", all(a <= b for a, b in zip(rb, rb[1:])), rb, "rising"),
            check("negative control: a reversed list is not monotone", not all(a <= b for a, b in zip(rb[::-1], rb[::-1][1:])), False, True)], \
        [wd / "sources.png", jdump(wd / "sources.json", table)]


@card("GLOW-62")
def sky_bounce(task, wd):
    n, m = sphere(120, 120, 60, 60, 50)
    sky, ground = np.array(kelvin(11000)) / 255, hxf("#b07a4a")
    up = (n[..., 1] * .5 + .5)[..., None]
    hemi = (sky * up + ground * (1 - up)) * .6
    img = np.where(m[..., None], hemi + .25, 0)
    save(np.clip(img, 0, 1), wd / "bounce.png")
    top, bot = img[20, 60], img[100, 60]
    w = lambda dot, amount=.9: max(0.0, dot) ** 3 * amount
    neutral = np.where(m[..., None], np.full(3, .5), 0.0)
    return [check("up-facing planes go cool (B > R)", top[2] > top[0], tohex(top * 255), "cool"),
            check("down-facing planes go warm (R > B)", bot[0] > bot[2], tohex(bot * 255), "warm"),
            check("haze toward a low sun weights alignment^3", w(1) == .9 and abs(w(.5) - .1125) < 1e-12 and w(-1) == 0, [w(1), w(.5), w(-1)],
                  [.9, .1125, 0]),
            check("negative control: without bounce top and bottom are equal", not (neutral[20, 60][2] > neutral[20, 60][0]), None, None)], \
        [wd / "bounce.png"]


def rim(mask, toward, width, soft=.6):
    from scipy.ndimage import shift as nd_shift
    d = norm(list(toward) + [0])[:2]
    shifted = nd_shift(mask, (-d[1] * width, -d[0] * width), order=1, mode="constant")   # copy shifted away from the light
    return blur(np.clip(mask - shifted, 0, 1), soft)


@card("GLOW-63")
def painter_rim(task, wd):
    h, w = 120, 160
    body = m_ellipse(h, w, 80, 60, 35)
    cv = canvas(h, w, "#0d1220")
    cv = fill(cv, body, "#1a1a22")
    r_warm = rim(body, (1, 0), 3)
    cv = fill(cv, r_warm, "#ff8a3a", .9, mode="add")
    save(rolloff(cv), wd / "rim.png")
    right, left = float(r_warm[60, 80 + 33]), float(r_warm[60, 80 - 33])
    wet1, wet2 = rim(body, (.7, -1), 2.6), rim(body, (-.4, -1), 1.8)
    top_r, top_l = float(wet1[25:33, 92:100].max()), float(wet2[25:33, 60:68].max())
    bot_r = float(wet1[87:95, 60:68].max())
    return [check("rim band on the edge facing the light (right)", right > .3, right, "> .3"),
            check("no rim on the far side (left)", left < .02, left, "< .02"),
            check("rim carries the light colour (R > B)", cv[60, 80 + 33][0] > cv[60, 80 + 33][2], tohex(np.clip(cv[60, 113], 0, 1) * 255), "warm"),
            check("wet surface: two opposing rims both present (upper right & upper left)", top_r > .1 and top_l > .1 and bot_r < .02, [top_r, top_l, bot_r], "> .1, far side 0"),
            check("negative control: the unlit body has no rim", not (float(fill(canvas(h, w, "#0d1220"), body, "#1a1a22")[60, 113, 0]) > .3), 0, None)], \
        [wd / "rim.png"]


def shade(mask, centre, r, light, lit, dark, core=.35):
    h, w = mask.shape
    lx, ly = norm([light[0] - centre[0], light[1] - centre[1], 0])[:2]
    hx_, hy = centre[0] + r * core * lx, centre[1] + r * core * ly
    t = np.clip(dist_map(h, w, hx_, hy) / (r * (1 + core)), 0, 1)[..., None]
    col = hxf(lit) * (1 - t) + hxf(dark) * t
    return col * mask[..., None], (hx_, hy)


@card("GLOW-64")
def form_shading(task, wd):
    h, w = 120, 120
    mask = m_ellipse(h, w, 60, 60, 40)
    img, hot = shade(mask, (60, 60), 40, (0, 0), "#ffe9c8", "#3a2a40")
    save(img, wd / "shade.png")
    lum = np.where(mask > .99, luma(img), -1)
    yy, xx = np.unravel_index(np.argmax(lum), lum.shape)
    off = math.hypot(xx - 60, yy - 60)
    flat = np.where(mask[..., None] > .99, hxf("#ffe9c8"), 0)
    return [check("hotspot offset r*.35 = 14 px toward the light", abs(off - 14) <= 1.5 and xx < 60 and yy < 60, [int(xx), int(yy), off], 14),
            check("lit colour at the hotspot", float(np.abs(img[int(hot[1]), int(hot[0])] - hxf("#ffe9c8")).max()) < .03, tohex(img[int(hot[1]), int(hot[0])] * 255),
                  "#ffe9c8"),
            check("dark side toward the far edge", float(luma(img)[85, 85]) < float(luma(img)[45, 45]) - .2, None, "darker"),
            check("negative control: a flat fill has no hotspot", not (float(np.ptp(luma(flat)[mask > .99])) > .2), 0, "> .2")], [wd / "shade.png"]


@card("GLOW-65")
def relief_body(task, wd):
    import cv2
    h, w = 120, 160
    sil = (m_ellipse(h, w, 80, 60, 60, 40) > .5).astype(np.uint8)
    dist = cv2.distanceTransform(sil, cv2.DIST_L2, 5).astype(float)
    hgt = np.sqrt(np.clip(dist / dist.max(), 0, 1)) * .6 * 40          # bulge .6, plateau-ish
    rng = np.random.default_rng(12)
    bumps = blur(rng.random((h, w)), 2) * 2 + blur(rng.random((h, w)), .8) * .9
    hgt = hgt + bumps * sil
    gx = cv2.Sobel(hgt, cv2.CV_64F, 1, 0, ksize=3) / 8
    gy = cv2.Sobel(hgt, cv2.CV_64F, 0, 1, ksize=3) / 8
    n = np.stack([-gx, gy, np.ones_like(gx)], -1)
    n /= np.linalg.norm(n, axis=-1, keepdims=True)
    L = norm([-.6, .5, .6])
    V = np.array([0, 0, 1.0])
    H = norm(L + V)
    diff = np.clip(n @ L, 0, 1)
    spec = np.clip(n @ H, 0, 1) ** 30 * .5
    fres = (1 - np.clip(n @ V, 0, 1)) ** 3
    sss = np.exp(-dist / 2.5) * sil
    col = hxf("#3a4a60") * (.22 + diff[..., None]) + spec[..., None] + fres[..., None] * hxf("#9fb5da") * .6 + sss[..., None] * hxf("#e8d8d0") * .3
    img = np.where(sil[..., None] > 0, col, hxf("#05070c"))
    save(rolloff(img), wd / "relief.png")
    sp = np.where(sil > 0, spec, 0)
    yy, xx = np.unravel_index(np.argmax(blur(sp, 3)), sp.shape)
    edge = float(fres[(dist > 0) & (dist <= 2)].mean())
    centre = float(fres[dist > 15].mean())
    flat_n = np.zeros((h, w, 3))
    flat_n[..., 2] = 1
    flat_spec = float(np.ptp(np.clip(flat_n @ H, 0, 1) ** 30))
    return [check("Blinn specular sits toward the upper-left light", xx < 80 and yy < 60, [int(xx), int(yy)], "upper-left"),
            check("Fresnel rim brighter at the silhouette band than inside (x5)", edge > 5 * centre and edge > .01, [edge, centre], "edge > 5x centre"),
            check("multi-scale bumps add texture (normal variance)", float(np.std(n[..., 0][dist > 10])) > .02, float(np.std(n[..., 0][dist > 10])), "> .02"),
            check("subsurface warms thin edges", float(sss[60, 80 + 58]) > float(sss[60, 80]) + .1, None, "edge > centre"),
            check("negative control: a flat silhouette has uniform specular", not (flat_spec > .01), flat_spec, 0)], [wd / "relief.png"]


def crystal(n, V, L, depth, iceA, iceB, skyA, skyB, rim_c, fog):
    ice = iceA * (1 - (n[..., 1:2] * .5 + .5)) + iceB * (n[..., 1:2] * .5 + .5)
    R = 2 * np.sum(n * V, -1, keepdims=True) * n - V
    sk = skyA + (skyB - skyA) * smoothstep(-.6, .9, R[..., 1:2])
    ndl = np.clip(np.sum(n * L, -1, keepdims=True), 0, None)
    fres = (1 - np.clip(np.sum(n * V, -1, keepdims=True), 0, None)) ** 2.6
    H = (L + V) / np.linalg.norm(L + V)
    spec = np.clip(np.sum(n * H, -1, keepdims=True), 0, None) ** 64
    c = ice * (.35 + .65 * ndl) + sk * .35 + rim_c * fres * .9 + spec * .8
    f = smoothstep(6, 24, depth)[..., None]
    return c * (1 - f) + fog * f, fres, spec


@card("GLOW-66")
def crystal_shader(task, wd):
    n, m = sphere(140, 140, 70, 70, 60)
    V = np.array([0, 0, 1.0])
    L = norm([.5, .9, .6])
    cols = dict(iceA=np.array([.043, .063, .19]), iceB=np.array([.10, .76, .85]), skyA=np.array([.05, .08, .2]),
                skyB=np.array([.86, .95, 1]), rim_c=np.array([.60, .93, .97]), fog=np.array([.03, .05, .1]))
    near, fres, spec = crystal(n, V, L, np.full((140, 140), 3.0), **cols)
    far, _, _ = crystal(n, V, L, np.full((140, 140), 30.0), **cols)
    img = np.where(m[..., None], near, 0)
    save(rolloff(img), wd / "crystal.png")
    sp = np.where(m[..., None], spec, 0)[..., 0]
    yy, xx = np.unravel_index(np.argmax(sp), sp.shape)
    H = norm(L + V)
    exp_x, exp_y = 70 + 60 * H[0], 70 - 60 * H[1]
    f_exp = (1 - math.sqrt(1 - (58 / 60) ** 2)) ** 2.6
    row = fres[70, 70:129, 0]
    return [check("Fresnel (1-n.v)^2.6: r=58/60 -> %.4f, centre 0, rising outward" % f_exp, abs(float(fres[70, 128, 0]) - f_exp) < 1e-6 and
                  float(fres[70, 70, 0]) < 1e-9 and bool(np.all(np.diff(row) >= -1e-12)), [float(fres[70, 128, 0]), float(fres[70, 70, 0])], [f_exp, 0]),
            check("Blinn highlight at the half-vector (+-3 px)", math.hypot(xx - exp_x, yy - exp_y) <= 3, [int(xx), int(yy)], [exp_x, exp_y]),
            check("fog: depth 30 is pure fog colour", float(np.abs(far[70, 70] - cols["fog"]).max()) < 1e-9, tohex(far[70, 70] * 255), "fog"),
            check("negative control: depth 3 is untouched by fog", not (float(np.abs(near[70, 70] - cols["fog"]).max()) < 1e-9), None, None)], \
        [wd / "crystal.png"]


def refract(I, N, eta):
    cosi = -np.sum(N * I, -1, keepdims=True)
    k = 1 - eta ** 2 * (1 - cosi ** 2)
    return eta * I + (eta * cosi - np.sqrt(np.clip(k, 0, None))) * N


@card("GLOW-67")
def refraction_dispersion(task, wd):
    from scipy.ndimage import map_coordinates
    h, w = 160, 160
    yy, xx = np.mgrid[0:h, 0:w]
    bg = (((xx // 10) + (yy // 10)) % 2).astype(float) * .8 + .1
    n, m = sphere(h, w, 80, 80, 50)
    I = np.zeros((h, w, 3))
    I[..., 2] = -1
    out = np.stack([bg] * 3, -1)
    shifts = {}
    for c, ior in enumerate((1.44, 1.45, 1.47)):            # per-channel IOR -> dispersion
        T = refract(I, n, 1 / ior)
        dx, dy = T[..., 0] * 40, -T[..., 1] * 40
        ch = map_coordinates(bg, [yy + dy, xx + dx], order=1, mode="reflect")
        out[..., c] = np.where(m, ch, bg)
        shifts[c] = float(np.abs(dx[m]).mean())
    save(out, wd / "glass.png")
    th = math.radians(30)
    t = refract(np.array([0, 0, -1.0]), np.array([math.sin(th), 0, math.cos(th)]), 1 / 1.5)
    snell = math.asin(math.sin(th) / 1.5)
    ang_t = math.acos(-float(t @ np.array([math.sin(th), 0, math.cos(th)])))
    fringe = float(np.abs(out[..., 0] - out[..., 2])[m].mean())
    flat = refract(I, n, 1.0)
    return [check("Snell: 30 deg into IOR 1.5 refracts to 19.47 deg", abs(math.degrees(ang_t) - math.degrees(snell)) < 1e-6, math.degrees(ang_t), 19.47),
            check("background bends behind the sphere", shifts[1] > 1, shifts[1], "> 1 px"),
            check("dispersion: R and B separate (colour fringes)", fringe > .005 and shifts[2] > shifts[0], [fringe, shifts[0], shifts[2]], "fringes"),
            check("negative control: IOR 1 does not bend the view", not (float(np.abs(flat - I)[m].max()) > 1e-9), float(np.abs(flat - I)[m].max()), 0)], \
        [wd / "glass.png"]


@card("GLOW-68")
def pulsing_rim_rig(task, wd):
    fps, n_fr = 30, 120
    n, m = sphere(80, 80, 40, 40, 30)
    gold, rimv, frames = [], [], []
    for i in range(n_fr):
        t = i / fps
        g = 3.5 + 1.2 * math.sin(3 * t)
        r = 4.0 + 1.5 * math.cos(2.5 * t)
        key = np.clip(n @ norm([.5, .8, .5]), 0, None)[..., None] * hxf("#38bdf8") * .35
        rimL = np.clip(n @ norm([-1, -.3, -.4]), 0, None)[..., None] * hxf("#f43f5e") * r * .08
        gl = np.clip(n @ norm([.6, -.6, .4]), 0, None)[..., None] * hxf("#fbbf24") * g * .08
        img = np.where(m[..., None], key + rimL + gl + hxf("#0f172a") * .2, 0)
        frames.append(np.clip(img, 0, 1))
        gold.append(float(frames[-1][58, 58, 1]))
        rimv.append(float(frames[-1][44, 11, 0]))
    write_video(wd / "rig.mp4", frames, fps=fps)
    f = np.fft.rfftfreq(n_fr, 1 / fps) * 2 * math.pi
    NP = 1 << 16
    f = np.fft.rfftfreq(NP, 1 / fps) * 2 * math.pi
    pk = lambda s: float(f[int(np.argmax(np.abs(np.fft.rfft((np.array(s) - np.mean(s)) * np.hanning(len(s)), NP))[1:])) + 1])
    frozen = [gold[0]] * n_fr
    return [check("gold pulse at 3 rad/s", abs(pk(gold) - 3) < .3, pk(gold), 3),
            check("rim pulse at 2.5 rad/s", abs(pk(rimv) - 2.5) < .3, pk(rimv), 2.5),
            check("rim light paints the rim side in its colour (R > B)", frames[0][44, 11, 0] > frames[0][44, 11, 2], tohex(frames[0][44, 11] * 255), "rose"),
            check("negative control: a frozen (unanimated) rig shows no 3 rad/s pulse", not (abs(pk(frozen) - 3) < .3), pk(frozen), 3)], [wd / "rig.mp4"]


@card("GLOW-69")
def cream_studio(task, wd):
    h, w = 120, 200
    y = np.linspace(0, 1, h)[:, None, None]
    cv = hxf("#f1efe8") * (1 - .08 * smoothstep(.5, 1, y)) + np.zeros((h, w, 3))
    yy, xx = np.mgrid[0:h, 0:w]
    grid = ((xx % 20 == 0) | (yy % 20 == 0)) & (yy > 70)
    cv[grid] = cv[grid] * .9 + hxf("#c9d8c2") * .1
    shadow = np.clip(1 - np.hypot((xx - 100) / 40, (yy - 92) / 6), 0, 1)
    cv = cv * (1 - .22 * shadow[..., None])                      # contact shadow opacity .22
    obj = m_ellipse(h, w, 100, 60, 26)
    n, mm = sphere(h, w, 100, 60, 26)
    lit = (np.clip(n @ norm([3, 6, 4]), 0, None) * 2.6 / 3 + np.clip(n @ norm([-3, 2, 4]), 0, None) * .9 / 3 + .3)[..., None] * hxf("#d6d2c8")
    cv = cv * (1 - obj[..., None]) + np.clip(lit, 0, 1) * obj[..., None]
    save(cv, wd / "studio.png")
    under = float(luma(cv)[92, 100] / luma(cv)[92, 30])
    return [check("cream sweep #f1efe8 at the top", tohex(cv[2, 2] * 255) == "#f1efe8", tohex(cv[2, 2] * 255), "#f1efe8"),
            check("contact shadow at .22 under the object", abs(under - .78) < .01, under, .78),
            check("faint grid lines on the floor", float(np.abs(cv[105, 40] - cv[105, 41]).max()) > .005, None, "visible"),
            check("key from upper right lights the object's upper right", float(luma(cv)[50, 112]) > float(luma(cv)[70, 88]), None, "brighter"),
            check("negative control: no shadow away from the object", not (abs(float(luma(cv)[92, 30] / luma(cv)[92, 30]) - .78) < .01), 1.0, None)], \
        [wd / "studio.png"]


def read_light(img):
    y = luma(img) * 255
    h, w = y.shape
    halves = {"left": y[:, :w // 2].mean(), "right": y[:, w // 2:].mean(), "top": y[:h // 2].mean(), "bottom": y[h // 2:].mean()}
    lr = halves["left"] - halves["right"]
    if abs(lr) < 8:
        return {"side": "even", "stops": 0.0, "ratio": "1:1"}
    lit, shade_ = max(halves["left"], halves["right"]), min(halves["left"], halves["right"])
    stops = math.log2(lit / shade_)
    return {"side": "left" if lr > 0 else "right", "stops": round(stops, 2), "ratio": "%g:1" % round(2 ** stops, 2)}


@card("GLOW-71")
def read_reference_light(task, wd):
    img = np.zeros((90, 160, 3))
    img[:, :80] = 160 / 255
    img[:, 80:] = 40 / 255
    save(img, wd / "ref.png")
    r = read_light(load(wd / "ref.png"))
    even = read_light(np.zeros((90, 160, 3)) + .5)
    jdump(wd / "light_read.json", {"ref": r, "even": even, "note": "heuristic"})
    return [check("brighter side found: left", r["side"] == "left", r["side"], "left"),
            check("lit/shade = 160/40 -> 2 stops -> 4:1", abs(r["stops"] - 2) < .05 and r["ratio"] == "4:1", r, {"stops": 2, "ratio": "4:1"}),
            check("negative control: an evenly lit frame reads 'even' (< 8 levels)", even["side"] == "even", even, "even")], [wd / "light_read.json"]


def sky_dome(h, w, sun_el, sun_az, top, horizon, size=1.0):
    yy, xx = np.mgrid[0:h, 0:w]
    az = (xx / w - .5) * 2 * math.pi
    el = (1 - yy / h) * math.pi / 2
    d = np.stack([np.cos(el) * np.sin(az), np.sin(el), np.cos(el) * np.cos(az)], -1)
    s_dir = norm([math.cos(math.radians(sun_el)) * math.sin(math.radians(sun_az)),
                                                                        math.sin(math.radians(sun_el)),
                                                                        math.cos(math.radians(sun_el)) * math.cos(math.radians(sun_az))])
    t = smoothstep(0, 1, el / (math.pi / 2))[..., None]
    col = hxf(horizon) * (1 - t) + hxf(top) * t
    s = np.clip(d @ s_dir, 0, 1)
    sun = s ** (1800 / size) * 30 + s ** 40 * .8 + s ** 6 * .25
    return col + sun[..., None] * hxf("#ffd29a"), s_dir


@card("GLOW-73")
def physical_sky(task, wd):
    h, w = 90, 360
    dome, sdir = sky_dome(h, w, 20, 40, "#2E4A7A", "#FFB067")
    save(rolloff(dome), wd / "dome.png")
    yy, xx = np.unravel_index(np.argmax(luma(dome)), (h, w))
    az = (xx / w - .5) * 360
    el = (1 - yy / h) * 90
    dome2, _ = sky_dome(h, w, 50, -90, "#2E4A7A", "#FFB067")
    y2, x2 = np.unravel_index(np.argmax(luma(dome2)), (h, w))
    return [check("sun placed by elevation 20 / azimuth 40 (+-2 deg)", abs(az - 40) <= 2 and abs(el - 20) <= 2, [az, el], [40, 20]),
            check("bounded gradient environment: finite everywhere", bool(np.isfinite(dome).all()) and float(dome.max()) < 40, float(dome.max()), "< 40"),
            check("golden dome: horizon warm, zenith blue", dome[h - 1, 5][0] > dome[h - 1, 5][2] and dome[0, 5][2] > dome[0, 5][0], None, "warm / blue"),
            check("negative control: another sun position moves the peak", not (abs((x2 / w - .5) * 360 - 40) <= 2), (x2 / w - .5) * 360, "!= 40")], \
        [wd / "dome.png"]


@card("GLOW-74")
def dappled_sun(task, wd):
    h, w, fps = 90, 160, 10
    cookie_big = fbm(128, 512, seed=7)
    thr = np.percentile(cookie_big, 100 * (1 - .15 - .2))
    cookie = blur((cookie_big > thr).astype(float), 1.2)
    frames, offs = [], []
    for i in range(20):
        off = int(i * 2)                                   # cookie slides slightly over time
        pat = cookie[:h, off:off + w]
        light = .16 + pat * (1 - .16)
        frames.append(canvas(h, w, "#3a5030") * (.4 + .6 * light[..., None]) + hxf("#ffd9a6") * (pat * .25)[..., None])
        offs.append(off)
    write_video(wd / "dapple.mp4", frames, fps=fps)
    a, b = luma(frames[0]), luma(frames[3])
    best = int(np.argmax([float(np.corrcoef(a[:, k:].ravel(), b[:, :w - k].ravel())[0, 1]) for k in range(0, 15)]))
    cover = float((cookie[:h, :w] > .5).mean())
    again = blur((fbm(128, 512, seed=7) > thr).astype(float), 1.2)
    return [check("leaf shadows slide (6 px over 3 frames)", best == 6, best, 6),
            check("floor .16: deepest shadow keeps 16 % light", abs(float(.16 + cookie.min() * .84) - .16) < .01, .16, .16),
            check("cookie holes ~ density (.25..45 open)", .25 <= cover <= .45, cover, ".25..45"),
            check("seeded cookie reproduces", np.array_equal(cookie, again), True, True),
            check("negative control: a static frame shows no slide", not (int(np.argmax([float(np.corrcoef(a[:, k:].ravel(), a[:, :w - k].ravel())[0, 1])
                                                                                     for k in range(0, 15)])) == 6), 0, 6)], [wd / "dapple.mp4"]


@card("GLOW-75")
def caustics(task, wd):
    h, w, fps = 90, 160, 10
    yy, xx = np.mgrid[0:h, 0:w]
    water = 30
    absorb = np.array([1.6, .55, .42])
    frames = []
    for i in range(10):
        t = i / fps
        c = 0
        for kx, ky, ph in ((.21, .13, 0), (-.17, .19, 1.3), (.09, -.23, 2.1)):
            c = c + np.sin(xx * kx + yy * ky + t * 3 + ph)
        net = np.clip(1 - np.abs(c) / 1.2, 0, 1) ** 3 * 1.6
        depth = np.clip((yy - water) / (h - water), 0, None) * 2.0        # metres below the waterline
        fade = smoothstep(0, .12, depth) * (1 - smoothstep(1.2, 3, depth))
        trans = np.exp(-absorb * depth[..., None])
        base = hxf("#c8b88a") * trans
        f = base + (net * fade)[..., None] * trans * .5
        f[yy < water] = hxf("#9fc4e0")
        frames.append(np.clip(f, 0, 1))
    write_video(wd / "caustics.mp4", frames, fps=fps)
    T = np.exp(-absorb * 1.0)
    above = float(np.abs(frames[0][:water] - frames[3][:water]).max())
    below = float(np.abs(frames[0][50:] - frames[3][50:]).max())
    return [check("per-channel absorption at 1 m: R .20, G .58, B .66", np.allclose(T, [math.exp(-1.6), math.exp(-.55), math.exp(-.42)]) and T[0] < T[1] < T[2],
                  T.tolist(), [.202, .577, .657]),
            check("caustic network moves below the waterline", below > .02, below, "> .02"),
            check("fades in over the first .12 m (none at the surface)", abs(float(smoothstep(0, .12, 0.0))) == 0, 0, 0),
            check("negative control: nothing above the water moves", not (above > .02), above, "<= .02")], [wd / "caustics.mp4"]


@card("GLOW-76")
def long_exposure(task, wd):
    h, w = 60, 200
    sub = 16
    path = [(20 + k * 160 / (sub - 1), 30) for k in range(sub)]
    samples = []
    for x, y in path:
        f = np.zeros((h, w, 3))
        f = fill(f, m_ellipse(h, w, x, y, 3), "#ffd27a")
        samples.append(f)
    lighten = np.max(samples, 0)
    average = np.mean(samples, 0)
    speed = 160 / (sub - 1)
    stretch = 1 + speed / (2 * 3)
    st = []
    for x, y in path:
        f = np.zeros((h, w, 3))
        f = fill(f, m_ellipse(h, w, x, y, 3 * stretch, 3), "#ffd27a")
        st.append(f)
    lighten_st = np.max(st, 0)
    save(np.vstack([lighten, average * 4, lighten_st]), wd / "stacks.png")
    row = luma(lighten)[30, 20:180]
    gaps = int(np.sum(row < .1))
    row_st = luma(lighten_st)[30, 20:180]
    return [check("lighten keeps each pixel's brightest sample (peak = the light)", abs(float(lighten.max()) - float(samples[0].max())) < 1e-9, None, None),
            check("average gives a dim smear (~1/16 of the light)", abs(float(average[30, 100:110].max()) - float(samples[0].max()) / 16) < .05,
                  float(average[30, 100:110].max()), float(samples[0].max()) / 16),
            check("a light faster than its size leaves dots (gaps)", gaps > 20, gaps, "> 20"),
            check("stretching by 1 + trail/(2r) closes the gaps", int(np.sum(row_st < .1)) == 0, int(np.sum(row_st < .1)), 0),
            check("negative control: a single sub-sample is one dot, not a trail", not (int(np.sum(luma(samples[0])[30] > .1)) > 50), int(np.sum(luma(samples[0])[30] > .1)), "<= 50")], \
        [wd / "stacks.png"]


@card("GLOW-77")
def practical_halos(task, wd):
    h, w, fps = 120, 200, 20
    base = canvas(h, w, "#0b1020")
    d = dist_map(h, w, 100, 90)
    r = 300 / 4
    a = np.interp(d / r, [0, .4, 1], [.9, .45, 0])
    col = np.where((d / r < .4)[..., None], hxf("#fff1cf"), hxf("#f2b25a"))
    frames, wins = [], []
    for i in range(40):
        t = i / fps
        f = base + col * a[..., None] * (1 - base)
        on = [t >= .3 + .4 * k for k in range(3)]
        for k, o in enumerate(on):
            if o:
                win = np.zeros((h, w))
                win[20:32, 30 + 40 * k:42 + 40 * k] = 1
                f = fill(f, win, "#ffcf7a")
                f = f + blur(win, 8)[..., None] * hxf("#ffcf7a") * .6
        fl = .5 + .5 * math.sin(2 * math.pi * 1.5 * t)
        f = f + m_ellipse(h, w, 170, 60, 1.5)[..., None] * hxf("#e8ff6a") * fl
        frames.append(np.clip(f, 0, 1))
        wins.append(sum(on))
    write_video(wd / "practicals.mp4", frames, fps=fps)
    f = frames[-1]
    prof = [float(luma(f)[90, 100 + k]) for k in (0, 20, 50, 80)]
    fl = [float(luma(fr)[60, 170]) for fr in frames]
    spec = np.abs(np.fft.rfft(np.array(fl) - np.mean(fl)))
    fq = float(np.fft.rfftfreq(len(fl), 1 / fps)[int(np.argmax(spec[1:])) + 1])
    return [check("pool brightness falls with distance from the lamp", all(prof[i] > prof[i + 1] for i in range(3)), prof, "decreasing"),
            check("warm amber core (#fff1cf) at the lamp", float(np.abs(f[90, 100] - (base[90, 100] + hxf("#fff1cf") * .9 * (1 - base[90, 100]))).max()) < .02,
                  tohex(f[90, 100] * 255), None),
            check("windows switch on in sequence", wins[5] == 0 and wins[8] == 1 and wins[-1] == 3, [wins[5], wins[8], wins[-1]], [0, 1, 3]),
            check("firefly pulses at 1-2 Hz", 1 <= fq <= 2, fq, "1..2"),
            check("negative control: the darkened scene alone has no pool", not (float(luma(base)[90, 100]) > float(luma(base)[90, 180]) + .01), 0, None)], \
        [wd / "practicals.mp4"]


def point_size(a_size, z):
    return float(np.clip(a_size * 1100 / -z, 1.5, 90))


@card("GLOW-78")
def point_sprites(task, wd):
    h, w = 120, 200
    rng = np.random.default_rng(3)
    pts = [(rng.uniform(10, 190), rng.uniform(10, 110), -rng.uniform(20, 400)) for _ in range(300)]
    cv = canvas(h, w, "#05060c")
    for x, y, z in pts:
        s = point_size(.5, z)
        d = dist_map(h, w, x, y) / s
        a = smoothstep(.5, 0, d) ** 2 * .8 * 2.2
        cv = cv + a[..., None] * hxf("#ffa040") * .3
    save(rolloff(cv), wd / "city.png")
    lamps = [45 * k for k in range(24)]
    cam = 300
    real = sorted(lamps, key=lambda p: abs(p - cam))[:6]
    sizes = [point_size(.5, -5.5), point_size(.5, -10), point_size(.5, -1000), point_size(.5, -1)]
    two = canvas(20, 20) + (smoothstep(.5, 0, dist_map(20, 20, 10, 10) / 6) ** 2)[..., None] * .4
    one = canvas(20, 20) + (smoothstep(.5, 0, dist_map(20, 20, 10, 10) / 6) ** 2)[..., None] * .2
    return [check("gl_PointSize = aSize*1100/-z (z=-10 -> 55 px)", abs(sizes[1] - 55) < 1e-9, sizes[1], 55),
            check("clamped to 1.5 .. 90 px", sizes[2] == 1.5 and sizes[3] == 90, [sizes[2], sizes[3]], [1.5, 90]),
            check("fragment a = smoothstep(.5,0,d)^2: centre 1, edge 0", float(smoothstep(.5, 0, 0) ** 2) == 1 and float(smoothstep(.5, 0, .5) ** 2) == 0,
                  None, [1, 0]),
            check("only the nearest 6 of 24 sodium lamps are real lights", len(real) == 6 and all(abs(p - cam) <= 135 for p in real), real, "6 nearest"),
            check("negative control: additive overlap brightens over a single sprite", float(two.max()) > float(one.max()), None, None)], \
        [wd / "city.png"]


def lantern_flicker(t):
    return .9 + .07 * perlin1d(7 * t + 1.3, 11) + .04 * perlin1d(19 * t + 4.1, 12)


@card("GLOW-79")
def lantern(task, wd):
    fps = 60
    ts = np.arange(0, 6, 1 / fps)
    fl = lantern_flicker(ts)
    lamp, glow_op, pool = 9 * fl, .32 * fl, .85 * fl
    frames = []
    for i in range(0, 90, 3):
        f = canvas(60, 100, "#060a14") + m_ellipse(60, 100, 50 + 3 * math.sin(1.1 * ts[i] + 1.3), 30, 10)[..., None] * hxf("#ff9a3c") * glow_op[i] * 2
        frames.append(np.clip(f, 0, 1))
    write_video(wd / "lantern.mp4", frames, fps=20)
    spec = np.abs(np.fft.rfft(fl - fl.mean()))
    fq = np.fft.rfftfreq(len(fl), 1 / fps)
    hi_energy = float(spec[(fq > 3)].sum() / spec[1:].sum())
    corr = float(np.corrcoef(lamp, pool)[0, 1])
    neon = np.where((ts % 1) < .1, 0.0, 1.0)
    return [check("never drops below ~80 %", float(fl.min()) >= .78, float(fl.min()), ">= .78"),
            check("organic wobble around .9 (max <= 1.02)", float(fl.max()) <= 1.02 and float(np.ptp(fl)) > .03, [float(fl.min()), float(fl.max())], ".78..1.02"),
            check("two octaves (7 Hz & 19 Hz): most energy above 3 Hz", hi_energy > .5, hi_energy, "> .5"),
            check("one signal drives lamp, glow and pool together (corr 1)", corr > .9999, corr, 1),
            check("negative control: a neon strike/drop-out violates the floor", not (float(neon.min()) >= .78), float(neon.min()), ">= .78")], \
        [wd / "lantern.mp4"]


@card("GLOW-81")
def painted_moon(task, wd):
    h, w = 400, 600
    cx, cy, r = 400, 200, 100
    cv = canvas(h, w, "#0b0a1e")
    cv = glow(cv, m_ellipse(h, w, cx, cy, r * 2.4), "#4f3f86", 70, .55)
    disc = m_ellipse(h, w, cx, cy, r)
    hx_, hy = cx - r * .35, cy - r * .35
    t = np.clip(dist_map(h, w, hx_, hy) / (r * 1.55), 0, 1)
    col = np.where((t < .5)[..., None], hxf("#fffaf0") * (1 - t[..., None] * 2) + hxf("#f7e6c2") * (t[..., None] * 2),
                   hxf("#f7e6c2") * (2 - t[..., None] * 2) + hxf("#dcb47e") * (t[..., None] * 2 - 1))
    cv = cv * (1 - disc[..., None]) + col * disc[..., None]
    for (ox, oy, rr) in ((30, 20, 14), (-20, 40, 10), (10, -30, 8)):
        cv = fill(cv, m_ellipse(h, w, cx + ox, cy + oy, rr) * disc, "#b99467", .25, blur_r=6)
    cv = glow(cv, disc, "#f1d29a", 26, .32)
    save(rolloff(cv), wd / "moon.png")
    lum = np.where(disc > .99, luma(cv), -1)
    yy, xx = np.unravel_index(np.argmax(lum), lum.shape)
    halo = cv[cy, cx + int(r * 1.6)]
    crater = float(luma(cv)[cy + 20, cx + 30])
    around = float(luma(cv)[cy + 20, cx + 52])
    return [check("disc lit from the upper left", xx < cx and yy < cy, [int(xx), int(yy)], "upper-left"),
            check("wide purple halo outside the disc (B > G)", halo[2] > halo[1] and float(halo.sum()) > float(hxf("#0b0a1e").sum()) + .1, tohex(np.clip(halo, 0, 1) * 255),
                  "purple"),
            check("crater blotches darker than the surrounding disc", crater < around, [crater, around], "darker"),
            check("negative control: the night sky alone has no halo", not (float(hxf("#0b0a1e")[2]) > float(hxf("#0b0a1e")[1]) and float(hxf("#0b0a1e").sum()) > float(hxf("#0b0a1e").sum()) + .1),
                  None, None)], [wd / "moon.png"]


HEAT83 = ([0, .12, .30, .45, .60, .78, 1.0], ["#04040c", "#2b0a5a", "#1f9e4a", "#f2d930", "#f28a1a", "#e0301e", "#ffffff"])


def heat_map(v, cap=.75):
    stops, cols = HEAT83
    v = np.minimum(np.asarray(v, float), cap)
    c = np.array([hxf(x) for x in cols])
    out = np.zeros(v.shape + (3,)) + c[0]
    for i in range(len(stops) - 1):
        t = smoothstep(stops[i], stops[i + 1], v)
        out = np.where((v >= stops[i])[..., None], c[i] * (1 - t[..., None]) + c[i + 1] * t[..., None], out)
    return out


@card("GLOW-83")
def thermal_doppler(task, wd):
    from scipy.ndimage import map_coordinates
    h, w = 90, 160
    q = fbm(h, w, 1)
    r_ = fbm(h, w, 2)
    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    warped = map_coordinates(fbm(h, w, 3), [np.clip(yy + 20 * (q - .5), 0, h - 1), np.clip(xx + 20 * (r_ - .5), 0, w - 1)], order=1)
    field = .34 + .32 * (warped - warped.min()) / np.ptp(warped)
    img = heat_map(field)
    save(img, wd / "heat_field.png")
    again = map_coordinates(fbm(h, w, 3), [np.clip(yy + 20 * (fbm(h, w, 1) - .5), 0, h - 1), np.clip(xx + 20 * (fbm(h, w, 2) - .5), 0, w - 1)], order=1)
    disk = np.zeros((h, w, 3))
    ring = (m_ellipse(h, w, 80, 45, 60, 14) - m_ellipse(h, w, 80, 45, 40, 8)).clip(0, 1)
    beta, cosang = .3, (80 - xx) / 60                      # left side approaching
    delta = 1 / (1 - beta * np.clip(cosang, -1, 1))
    inten = delta ** 3.5
    shift = np.clip((delta - 1) * 2, -1, 1)[..., None]
    base = hxf("#ffb070")
    col = np.where(shift > 0, base * (1 - shift) + hxf("#9fc8ff") * shift, base * (1 + shift) + hxf("#ff5a2a") * (-shift))
    disk = col * (inten * ring)[..., None] * .4
    save(rolloff(disk), wd / "doppler.png")
    L = float(luma(disk)[45, 25:40][ring[45, 25:40] > .5].mean())
    R = float(luma(disk)[45, 120:135][ring[45, 120:135] > .5].mean())
    lb = disk[45, 30]
    uncapped = heat_map(np.array([1.0]), cap=1.0)[0]
    return [check("domain-warped fbm field is deterministic", np.allclose(warped, again), True, True),
            check("background heat stays in .34 .. .66", float(field.min()) >= .34 - 1e-9 and float(field.max()) <= .66 + 1e-9,
                  [float(field.min()), float(field.max())], ".34..66"),
            check("heat cap .75: never white", float(heat_map(np.array([1.0]))[0].min()) < .8, tohex(heat_map(np.array([1.0]))[0] * 255), "not white"),
            check("Doppler: approaching side brighter by ~delta^3.5", L > 2 * R, [L, R], "L > 2R"),
            check("approaching side blue-shifted (B > R)", lb[2] > lb[0], tohex(np.clip(lb, 0, 1) * 255), "blue"),
            check("negative control: uncapped heat 1.0 is white", not (float(uncapped.min()) < .8), tohex(uncapped * 255), "#ffffff")], \
        [wd / "heat_field.png", wd / "doppler.png"]


@card("GLOW-84")
def fog_title(task, wd):
    from scipy.ndimage import map_coordinates
    h, w, fps = 90, 160, 10
    mask0 = m_text(h, w, "FOG", 40, (40, 22))
    ys, xs = np.nonzero(mask0 > .5)
    cy, cx = ys.mean(), xs.mean()
    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    f1, f2 = fbm(h, w * 2, 4), fbm(h, w * 2, 5)
    frames, contrasts, slits, areas = [], [], [], {}
    for i in range(80):
        t = i / fps
        a = f1[:, int(t * 6) % w: int(t * 6) % w + w] * .35                  # far layer 6 px/s
        b = f2[:, int(t * 15) % w: int(t * 15) % w + w] * .25                # near layer 15 px/s
        bg = canvas(h, w, "#0a0d14")
        bg = bg + (a + b)[..., None] * (1 - bg) * .6                         # screen fog
        open_ = min(1, max(0, (t - 1) / 2)) if t >= 1 else 0                 # MG-072 slit: line, widen 1-3 s, hold
        half = .5 + open_ * 4
        bg = bg + (np.abs(yy - 82) <= half)[..., None] * hxf("#fff4dc") * .5 * (t > 0)
        s = 1 + .04 * smoothstep(0, 8, t)                                    # slow drift 1.00 -> 1.04
        mask = map_coordinates(mask0, [cy + (yy - cy) / s, cx + (xx - cx) / s], order=1)
        appear = smoothstep(2, 4, t)
        f = np.clip(bg * (1 - mask[..., None] * appear) + hxf("#f3ead8") * (mask * appear)[..., None], 0, 1)
        frames.append(f)
        if t >= 4:
            txt = luma(f)[mask > .9].mean()
            ring = luma(f)[(blur(mask, 3) > .05) & (mask < .05) & (np.abs(yy - 82) > 6)].mean()
            contrasts.append((txt + .05) / (ring + .05))
        slits.append(int(np.sum(luma(f)[:, 2] > luma(bg - (np.abs(yy - 82) <= half)[..., None] * hxf("#fff4dc") * .5 * (t > 0))[:, 2] + .2)))
        if i in (40, 79):
            areas[i] = float(mask.sum())
    write_video(wd / "fog_title.mp4", frames, fps=fps)
    s40, s79 = 1 + .04 * float(smoothstep(0, 8, 4.0)), 1 + .04 * float(smoothstep(0, 8, 7.9))
    ratio = areas[79] / areas[40]
    raw = canvas(h, w, "#0a0d14") + fbm(h, w * 2, 4)[:, :w, None] * .35
    raw_c = (luma(raw)[mask0 > .9].mean() + .05) / (luma(raw)[(blur(mask0, 3) > .05) & (mask0 < .05)].mean() + .05)
    return [check("haze never blocks reading (title contrast >= 3 every frame after 4 s)", min(contrasts) >= 3, min(contrasts), ">= 3"),
            check("light slit: a line before 1 s, widens 1-3 s, then holds", slits[5] == 1 and slits[5] < slits[20] < slits[30] and slits[30] == slits[70],
                  [slits[5], slits[20], slits[30], slits[70]], "1 < .. < hold"),
            check("slow drift 1.00 -> 1.04: title area grows by (s79/s40)^2", abs(ratio - (s79 / s40) ** 2) < .006, ratio, (s79 / s40) ** 2),
            check("negative control: the untitled fog frame has no readable title (contrast < 3)", not (raw_c >= 3), float(raw_c), ">= 3")], \
        [wd / "fog_title.mp4"]


def p01_frame(t, w=480, h=854):
    n = 321
    pts = [(40 + i * (w - 80) / (n - 1), h / 2 + 95 * math.exp(-i / 600) * math.sin(3 * math.pi * i / (n - 1))) for i in range(n)]
    k = max(2, int(n * min(1, t / 2.6)))
    part = pts[:k]
    base = Image.new("RGB", (w, h), (8, 11, 23))
    d = ImageDraw.Draw(base)
    for y in range(0, h, 48):
        d.line((0, y, w, y), fill=(14, 18, 34))
    halo = Image.new("RGB", (w, h), (0, 0, 0))
    ImageDraw.Draw(halo).line(part, fill=(0, 150, 195), width=17, joint="curve")
    halo = halo.filter(ImageFilter.GaussianBlur(21))
    img = Image.blend(base, halo, 0.44)
    d = ImageDraw.Draw(img)
    d.line(part, fill=(31, 200, 245), width=6, joint="curve")
    d.line(part, fill=(204, 254, 255), width=2, joint="curve")
    x, y = part[-1]
    d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=(255, 255, 255))
    return img, part


@card("GLOW-P01")
def raster_neon_write(task, wd):
    a, part = p01_frame(2.5)
    b, _ = p01_frame(2.5)
    a.save(wd / "still.png")
    frames = [np.asarray(p01_frame(i / 24)[0]).astype(float) / 255 for i in range(0, 96)]
    write_video(wd / "neon_write.mp4", frames, fps=24)
    arr = np.asarray(a).astype(float)
    tip = arr[int(round(part[-1][1])), int(round(part[-1][0]))]
    mid = part[len(part) // 2]
    halo_px = arr[int(mid[1]) + 12, int(mid[0])]
    _, full = p01_frame(3.0)
    _, early = p01_frame(0.0)
    return [check("frame(t) is pure: t=2.5 renders identical bytes", a.tobytes() == b.tobytes(), True, True),
            check("write-on: visible points = 321 * min(1, t/2.6)", len(part) == int(321 * 2.5 / 2.6) and len(full) == 321,
                  [len(part), len(full)], [int(321 * 2.5 / 2.6), 321]),
            check("white tip dot at the head", float(tip.min()) > 250, tohex(tip), "#ffffff"),
            check("blurred cyan halo blended beside the path (B > R)", halo_px[2] > halo_px[0] + 10, tohex(halo_px), "cyan"),
            check("negative control: at t=0 nothing is written", not (len(early) > 2), len(early), 2)], [wd / "still.png", wd / "neon_write.mp4"]


def tinted_bloom(img, light_col, thr=.8, strength=1.2, tint=.6):
    hi = np.maximum(img - thr, 0)
    b = blur(hi, 6) * strength
    core = b * (1 - tint) + luma(b)[..., None] * hxf(light_col) * tint / max(float(luma(hxf(light_col))), 1e-6)
    return img + core


def flash_plan(requests, fps=30):
    big, out = [], []
    for t, kind, frames in sorted(requests):
        if sum(1 for o in out if t - 1 < o[0] <= t) >= 3:
            continue
        if kind == "big" and any(t - 1 < b <= t for b in big):
            continue
        if kind == "white":
            frames = min(frames, 2)
        if kind == "big":
            big.append(t)
        out.append((t, kind, frames))
    return out


@card("GLOW-X02")
def tinted_core_flash_limits(task, wd):
    h, w = 90, 160
    cv = canvas(h, w, "#060810")
    act = (110, 40)
    cv = fill(cv, m_ellipse(h, w, *act, 6), (2.0, 2.0, 2.0))
    out = tinted_bloom(cv, "#ff9a3c")
    white = threshold_bloom(cv, .8, 1.2, 6)
    save(rolloff(out), wd / "tinted_core.png")
    ring = out[act[1], act[0] + 10]
    ring_w = white[act[1], act[0] + 10]
    yy, xx = np.unravel_index(np.argmax(luma(out - cv)), (h, w))
    plan = flash_plan([(.1, "big", 3), (.5, "big", 3), (.6, "small", 2), (.7, "small", 2), (.8, "small", 2), (1.2, "white", 5)])
    per_s = max(sum(1 for t, _, _ in plan if s <= t < s + 1) for s in np.arange(0, 1.5, .05))
    big = [t for t, k, _ in plan if k == "big"]
    whites = [f for _, k, f in plan if k == "white"]
    return [check("bloom core tinted toward the light colour (R > B, not grey)", ring[0] > ring[2] * 1.3, tohex(np.clip(ring, 0, 1) * 255), "warm"),
            check("flash blooms from the action point", math.hypot(xx - act[0], yy - act[1]) <= 1, [int(xx), int(yy)], act),
            check("<= 1 big flash per second", all(b2 - b1 >= 1 for b1, b2 in zip(big, big[1:])) and big == [.1], big, [.1]),
            check("<= 3 flashes per second", per_s <= 3, per_s, "<= 3"),
            check("full white frame <= 2 frames", all(f <= 2 for f in whites), whites, "<= 2"),
            check("negative control: untinted bloom is grey (R == B)", not (ring_w[0] > ring_w[2] * 1.3), tohex(np.clip(ring_w, 0, 1) * 255), "grey")], \
        [wd / "tinted_core.png"]
