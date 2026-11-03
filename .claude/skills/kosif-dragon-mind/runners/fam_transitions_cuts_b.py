"""transitions-cuts (part B): method cards as real programs with known-answer checks.

Every card renders (or edits) a deterministic fixture in the work folder with numpy frame math or FFmpeg,
writes a lossless video/audio/JSON output, reads the output back and measures the property the card
defines (coverage of a mask, direction and amount of blur, channel offsets, cut frames, durations,
loudness...). Each card also runs the same measurement on the unprocessed input (a plain hard cut, the
untouched scene, a naive plan) and requires it to fail: that is the negative control.

Frame-math ports are labelled in the docstring when the card names a browser/JS engine (GSAP, CSS,
Remotion): the runner executes the card's transition math, not that engine.
"""
from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path

from _harness import card, check, fx

GAPS: dict = {
    "TRANS-33": "View Transitions API (document.startViewTransition / React <ViewTransition>) is a browser "
                "DOM-snapshot feature; it needs a driven Chromium page plus React, not frame math here",
    "TRANS-35": "CSS-only popover/dialog enter-exit with @starting-style and transition-behavior allow-discrete "
                "is a browser CSS feature (Tailwind v4 @theme); needs a driven Chromium page to prove",
    "TRANS-51": "Pure-CSS accordion via ::details-content and interpolate-size is a browser CSS feature; needs a "
                "driven Chromium page to prove",
    "TRANS-94": "React <ViewTransition> / ::view-transition snapshot morphs are a browser DOM feature; needs a "
                "driven Chromium page plus React",
    "TRANS-92": "@hyperframes/shader-transitions package on a WebGL canvas with html2canvas captures; the package "
                "is not installed and headless WebGL is not available here",
    "TRANS-97": "Three.js/R3F WebGLRenderTargets in a GPU (or SwiftShader) Chromium; three is not installed here "
                "(the same noise-threshold math runs as TRANS-95 / TRANS-99)",
}

W, H, FPS = 128, 72, 30


# ----------------------------------------------------------------------------------------------- numpy core
def _np():
    import numpy as np
    return np


def grid():
    np = _np()
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    return xx, yy


def solid(rgb):
    np = _np()
    f = np.zeros((H, W, 3))
    f[:] = rgb
    return f


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def scene_a():
    """Warm textured scene: red-orange gradient with an 8 px checker (gives edges to measure blur on)."""
    np = _np()
    xx, yy = grid()
    chk = (((xx // 8) + (yy // 8)) % 2) * 2 - 1
    f = np.stack([200 + 30 * chk, 70 + 60 * xx / W + 20 * chk, 40 + 10 * chk], -1)
    return np.clip(f, 0, 255)


def scene_b():
    """Cool textured scene: blue gradient with 6 px vertical and horizontal stripes."""
    np = _np()
    xx, yy = grid()
    st = ((xx // 6) % 2) * 2 - 1
    sh = ((yy // 6) % 2) * 2 - 1
    f = np.stack([30 + 15 * st, 90 + 50 * yy / H + 25 * sh, 210 + 25 * st], -1)
    return np.clip(f, 0, 255)


def scene_c():
    np = _np()
    xx, yy = grid()
    chk = (((xx // 5) + (yy // 5)) % 2) * 2 - 1
    return np.clip(np.stack([60 + 30 * chk, 190 + 30 * chk, 70 + 0 * chk], -1), 0, 255)


def font(size):
    from PIL import ImageFont
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            pass
    return ImageFont.load_default(size=size)


def text_frame(word, fg=(255, 255, 255), bg=(0, 0, 0), size=26, xy=None):
    """A frame with `word` drawn (deterministic font); returns (frame, ink_mask)."""
    np = _np()
    from PIL import Image, ImageDraw
    im = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(im)
    fnt = font(size)
    box = d.textbbox((0, 0), word, font=fnt)
    tw, th = box[2] - box[0], box[3] - box[1]
    pos = xy or ((W - tw) // 2 - box[0], (H - th) // 2 - box[1])
    d.text(pos, word, fill=255, font=fnt)
    m = np.asarray(im, dtype=float) / 255.0
    f = solid(bg) * (1 - m[..., None]) + np.array(fg, float) * m[..., None]
    return f, m


def blend(a, b, m):
    np = _np()
    m = np.asarray(m, dtype=float)
    if m.ndim == 2:
        m = m[..., None]
    return a * (1 - m) + b * m


def circle_mask(cx, cy, r, feather=0.0):
    np = _np()
    xx, yy = grid()
    d = np.hypot(xx - cx, yy - cy)
    if feather <= 0:
        return (d <= r).astype(float)
    return np.clip((r - d) / feather + 0.5, 0, 1)


def shift(img, dx=0, dy=0, fill=None):
    """Integer translation; uncovered pixels take `fill` (default: edge-free black)."""
    np = _np()
    dx, dy = int(round(dx)), int(round(dy))
    out = np.zeros_like(img) if fill is None else np.broadcast_to(np.asarray(fill, float), img.shape).copy()
    h, w = img.shape[:2]
    xs0, xs1 = max(0, -dx), min(w, w - dx)
    ys0, ys1 = max(0, -dy), min(h, h - dy)
    if xs1 > xs0 and ys1 > ys0:
        out[ys0 + dy:ys1 + dy, xs0 + dx:xs1 + dx] = img[ys0:ys1, xs0:xs1]
    return out


def _box1d(img, r, axis):
    np = _np()
    r = int(round(r))
    if r <= 0:
        return img.copy()
    pad = [(0, 0)] * img.ndim
    pad[axis] = (r + 1, r)
    p = np.pad(img, pad, mode="edge")
    c = np.cumsum(p, axis=axis)
    n = img.shape[axis]
    hi = np.take(c, range(2 * r + 1, 2 * r + 1 + n), axis=axis)
    lo = np.take(c, range(0, n), axis=axis)
    return (hi - lo) / (2 * r + 1)


def gblur_axis(img, sigma, axis):
    """Gaussian blur along one axis with standard deviation `sigma` px (edge-extended)."""
    np = _np()
    if sigma <= 0.05:
        return img.copy()
    rad = int(math.ceil(3 * sigma))
    xs = np.arange(-rad, rad + 1)
    k = np.exp(-xs ** 2 / (2 * sigma * sigma))
    k /= k.sum()
    pad = [(0, 0)] * img.ndim
    pad[axis] = (rad, rad)
    p = np.pad(img, pad, mode="edge")
    n = img.shape[axis]
    out = np.zeros_like(img, dtype=float)
    for j, w in enumerate(k):
        out += w * np.take(p, range(j, j + n), axis=axis)
    return out


def blur_x(img, px):
    """Horizontal blur; px is the CSS/SVG stdDeviation in frame pixels."""
    return gblur_axis(img, px, 1)


def blur_y(img, px):
    return gblur_axis(img, px, 0)


def blur(img, px):
    return blur_y(blur_x(img, px), px)


def sample(img, sx, sy, fill=(0, 0, 0)):
    """Nearest-neighbour sampling of img at float coords (sx, sy); outside -> fill."""
    np = _np()
    xi, yi = np.round(sx).astype(int), np.round(sy).astype(int)
    ok = (xi >= 0) & (xi < W) & (yi >= 0) & (yi < H)
    out = solid(fill)
    out[ok] = img[yi[ok], xi[ok]]
    return out, ok.astype(float)


def scale_about(img, s, cx=W / 2, cy=H / 2, fill=(0, 0, 0)):
    xx, yy = grid()
    out, _ = sample(img, cx + (xx - cx) / s, cy + (yy - cy) / s, fill)
    return out


def rotate(img, deg, cx=W / 2, cy=H / 2, fill=(0, 0, 0)):
    xx, yy = grid()
    a = math.radians(-deg)
    sx = cx + (xx - cx) * math.cos(a) - (yy - cy) * math.sin(a)
    sy = cy + (xx - cx) * math.sin(a) + (yy - cy) * math.cos(a)
    out, _ = sample(img, sx, sy, fill)
    return out


def pixelate(img, b):
    np = _np()
    b = max(1, int(b))
    if b == 1:
        return img.copy()
    hh, ww = -(-H // b) * b, -(-W // b) * b
    p = np.pad(img, ((0, hh - H), (0, ww - W), (0, 0)), mode="edge")
    m = p.reshape(hh // b, b, ww // b, b, 3).mean(axis=(1, 3))
    return np.repeat(np.repeat(m, b, 0), b, 1)[:H, :W]


def rgb_split(img, dx, dy=0):
    np = _np()
    out = img.copy()
    out[..., 0] = shift(img[..., 0:1], dx, dy)[..., 0]
    out[..., 2] = shift(img[..., 2:3], -dx, -dy)[..., 0]
    return out


def band_shift(img, offsets):
    """Split into len(offsets) horizontal bands and shift each by its own x offset (wrapping)."""
    np = _np()
    out = img.copy()
    n = len(offsets)
    for i, o in enumerate(offsets):
        y0, y1 = i * H // n, (i + 1) * H // n
        out[y0:y1] = np.roll(img[y0:y1], int(o), axis=1)
    return out


# eases
def lin(t):
    return min(1.0, max(0.0, t))


def expo_out(t):
    t = lin(t)
    return 1.0 if t >= 1 else 1 - 2 ** (-10 * t)


def expo_in(t):
    t = lin(t)
    return 0.0 if t <= 0 else 2 ** (10 * t - 10)


def expo_inout(t):
    t = lin(t)
    if t <= 0 or t >= 1:
        return t
    return 2 ** (20 * t - 10) / 2 if t < 0.5 else (2 - 2 ** (-20 * t + 10)) / 2


def pow_in(t, n=2):
    return lin(t) ** n


def pow_out(t, n=2):
    return 1 - (1 - lin(t)) ** n


def pow_inout(t, n=2):
    t = lin(t)
    return (2 ** (n - 1)) * t ** n if t < 0.5 else 1 - ((-2 * t + 2) ** n) / 2


def sine_inout(t):
    return -(math.cos(math.pi * lin(t)) - 1) / 2


def smooth(t):
    t = lin(t)
    return t * t * (3 - 2 * t)


# measures
def mad(a, b):
    np = _np()
    return float(np.mean(np.abs(np.asarray(a, float) - np.asarray(b, float))))


def near(f, ref, tol=28):
    """Per-pixel boolean: every channel within tol of ref (frame or colour)."""
    np = _np()
    ref = np.asarray(ref, float)
    return np.max(np.abs(f - ref), axis=-1) < tol


def frac(f, ref, tol=28, mask=None):
    np = _np()
    n = near(f, ref, tol)
    if mask is not None:
        n = n[mask.astype(bool)]
    return float(np.mean(n)) if n.size else 0.0


def sharp_x(f):
    np = _np()
    return float(np.mean(np.abs(np.diff(f, axis=1))))


def sharp_y(f):
    np = _np()
    return float(np.mean(np.abs(np.diff(f, axis=0))))


def best_dx(f, ref, rng=40, axis=1):
    """Shift of ref (along axis) that best explains f, by brute force over the overlapping region."""
    np = _np()
    best, arg = 1e9, 0
    for d in range(-rng, rng + 1):
        if axis == 1:
            a = f[:, max(0, d):W + min(0, d)]
            b = ref[:, max(0, -d):W - max(0, d)]
        else:
            a = f[max(0, d):H + min(0, d)]
            b = ref[max(0, -d):H - max(0, d)]
        if a.size == 0:
            continue
        e = float(np.mean(np.abs(a - b)))
        if e < best - 1e-9:
            best, arg = e, d
    return arg, best


def chan_offset(f, rng=20):
    """Horizontal offset of the red channel against green (R shifted +d)."""
    np = _np()
    g, r = f[..., 1], f[..., 0]
    best, arg = 1e9, 0
    for d in range(-rng, rng + 1):
        a = r[:, max(0, d):W + min(0, d)]
        b = g[:, max(0, -d):W - max(0, d)]
        e = float(np.mean(np.abs(a - b)))
        if e < best - 1e-9:
            best, arg = e, d
    return arg


def luma(f):
    np = _np()
    return float(np.mean(f[..., 0] * 0.2126 + f[..., 1] * 0.7152 + f[..., 2] * 0.0722))


def cut_frames(F, thr=30.0):
    """Indices i where frame i differs strongly from frame i-1 (hard cuts)."""
    return [i for i in range(1, len(F)) if mad(F[i], F[i - 1]) > thr]


# ----------------------------------------------------------------------------------------------- IO
def write_video(path, frames, fps=FPS):
    """Lossless RGB H.264 so the measured pixels are the rendered pixels."""
    np = _np()
    data = b"".join(np.clip(np.round(f), 0, 255).astype(np.uint8).tobytes() for f in frames)
    done = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo",
                           "-pix_fmt", "rgb24", "-s", "%dx%d" % (W, H), "-r", str(fps), "-i", "-",
                           "-c:v", "libx264rgb", "-qp", "0", "-preset", "ultrafast", str(path)],
                          input=data, capture_output=True, timeout=60)
    if done.returncode:
        raise RuntimeError(done.stderr.decode(errors="replace")[-300:])
    return Path(path)


def render(wd, name, frames, fps=FPS):
    """Write frames, read them back from the file; returns (path, frames_from_file)."""
    p = write_video(Path(wd) / (name + ".mkv"), frames, fps)
    F = fx.frames(p, size=(W, H))
    return p, F


def seq(fn, n):
    return [fn(i) for i in range(n)]


def save_json(wd, name, obj):
    p = Path(wd) / name
    p.write_text(json.dumps(obj, indent=1, ensure_ascii=False), encoding="utf-8")
    return p


def ms2f(ms, fps=FPS):
    return int(round(ms / 1000.0 * fps))


# ================================================================================ batch 1: colour cuts
def _seg_runs(F, tol=3.0):
    """Split frames into runs of (near-)identical frames: returns [(start, length)]."""
    runs, s = [], 0
    for i in range(1, len(F) + 1):
        if i == len(F) or mad(F[i], F[i - 1]) > tol:
            runs.append((s, i - s))
            s = i
    return runs


def _beat_colour_cuts(wd, name, palette, bpm, beats, fps=FPS):
    np = _np()
    beat_f = 60.0 / bpm * fps
    cuts = [int(round(k * beat_f)) for k in range(beats + 1)]
    sq = circle_mask(W / 2, H / 2, 10)  # constant subject on top of the swapping background

    def fr(i):
        k = max(j for j in range(beats) if cuts[j] <= i)
        return blend(solid(palette[k % len(palette)]), solid((255, 255, 255)), sq)
    n = cuts[-1]
    p, F = render(wd, name, seq(fr, n), fps)
    bg = sq < 0.5
    got_cuts = cut_frames(F)
    seg_ok = all(frac(F[cuts[k]], palette[k % len(palette)], 4, bg) > 0.99 for k in range(beats))
    subj_ok = all(frac(F[i], (255, 255, 255), 4, ~bg) > 0.99 for i in (0, n // 2, n - 1))
    flat = solid(palette[0])
    neg = cut_frames([flat] * n)
    return [check("cuts land on beat frames", got_cuts == cuts[1:-1], got_cuts, cuts[1:-1]),
            check("each beat's full background is its palette colour", seg_ok, seg_ok, True),
            check("subject stays untouched across cuts", subj_ok, subj_ok, True),
            check("palette size 3-4 flat colours used", 3 <= len({tuple(c) for c in palette}) <= 4,
                  len(palette), "3-4"),
            check("negative control: unswapped background has no beat cuts", neg != cuts[1:-1], neg, cuts[1:-1])], [p]


@card("TRANS-308")
def bg_swap_on_beat(task, wd):
    """Each cut swaps the full background among 3-4 flat colours, on the beat (120 BPM)."""
    return _beat_colour_cuts(wd, "bg_swap", [(240, 90, 40), (250, 230, 200), (40, 70, 200)], 120, 8)


@card("TRANS-355")
def alt_bg_per_scene(task, wd):
    """Alternate full-field backgrounds black/red/blue/cream per scene on the beat (128 BPM)."""
    return _beat_colour_cuts(wd, "alt_bg", [(0, 0, 0), (220, 30, 40), (30, 60, 220), (245, 235, 210)], 128, 8)


def _word_cards(wd, name, words, fields, inks, ms, fps):
    np = _np()
    nf = ms2f(ms, fps)
    frames, masks = [], []
    for w, bg, ink in zip(words, fields, inks):
        f, m = text_frame(w, ink, bg, 22)
        frames += [f] * nf
        masks.append(m)
    p, F = render(wd, name, frames, fps)
    runs = _seg_runs(F)
    lens = [r[1] for r in runs]
    ok_bg, ok_ink = True, True
    for k, (s, _) in enumerate(runs[:len(words)]):
        m = masks[k] > 0.995
        ok_bg &= frac(F[s], fields[k], 4, ~(masks[k] > 0.005)) > 0.99
        ok_ink &= m.sum() > 30 and frac(F[s], inks[k], 6, m) > 0.98
    neg = _seg_runs([frames[0]] * len(frames))
    return [check("one card per word, each %d ms" % ms, lens == [nf] * len(words), lens, [nf] * len(words)),
            check("each card's field colour", ok_bg, ok_bg, True),
            check("each word drawn in its ink colour", ok_ink, ok_ink, True),
            check("negative control: a held card has one run", [r[1] for r in neg] != [nf] * len(words),
                  [r[1] for r in neg], [nf] * len(words))], [p]


@card("TRANS-341")
def word_colour_fields(task, wd):
    """Each tool word sits 250 ms on a new colour field (hard cut per word)."""
    words = ["CUT", "WIPE", "FADE", "ZOOM", "PUSH"]
    fields = [(230, 60, 50), (40, 80, 210), (250, 200, 40), (30, 160, 90), (120, 40, 160)]
    return _word_cards(wd, "word_fields", words, fields, [(255, 255, 255)] * 5, 250, 24)


@card("TRANS-356")
def tinted_word_cards(task, wd):
    """Single word per card, hard cut every 250 ms, each word tinted its own colour on black."""
    words = ["ONE", "TWO", "SIX", "TEN"]
    inks = [(255, 80, 80), (80, 200, 255), (255, 220, 60), (140, 255, 120)]
    return _word_cards(wd, "tinted_words", words, [(0, 0, 0)] * 4, inks, 250, 24)


@card("TRANS-333")
def chapter_colour_panels(task, wd):
    """Full-bleed flat panel slides in over 200 ms easeOutExpo to open each chapter; colours rotate (5)."""
    np = _np()
    cols = [(230, 70, 40), (40, 90, 220), (250, 210, 60), (30, 170, 110), (150, 50, 170)]
    slide = ms2f(200)
    hold = 8
    xx, _ = grid()
    frames, plan = [], []
    prev = (20, 20, 20)
    for c in cols:
        for j in range(slide + hold):
            p = expo_out(j / slide)
            cov = (xx < p * W).astype(float)
            frames.append(blend(solid(prev), solid(c), cov))
            plan.append(p)
        prev = c
    path, F = render(wd, "panels", frames)
    errs = []
    prevs = [(20, 20, 20)] + cols[:-1]
    for k, c in enumerate(cols):
        for j in range(1, slide):
            i = k * (slide + hold) + j
            errs.append(abs(frac(F[i], c, 6) - plan[i]))
    ends = all(frac(F[k * (slide + hold) + slide], c, 6) > 0.99 for k, c in enumerate(cols))
    # negative: a hard cut to the panel (no slide) measured the same way
    hard_err = max(abs(1.0 - plan[k * (slide + hold) + 1]) for k in range(5))
    return [check("panel coverage follows easeOutExpo over 200 ms", max(errs) < 0.03, max(errs), "<0.03"),
            check("each chapter ends full-bleed in its colour", ends, ends, True),
            check("5 rotating chapter colours", len(set(cols)) == 5, len(set(cols)), 5),
            check("negative control: hard cut misses the expo curve", hard_err > 0.2, hard_err, ">0.2")], [path]


@card("TRANS-338")
def black_claim_card(task, wd):
    """Hard cut from a white page to full black with a white bold claim (2.2 s hold, words rise one by one),
    then hard cut back to the white page."""
    np = _np()
    fps = 15
    words = ["NO", "MORE", "FADES"]
    page, _ = text_frame("page", (40, 40, 40), (255, 255, 255), 14)
    hold = int(round(2.2 * fps))
    per = hold // (len(words) + 1)
    rise = 4
    frames = [page] * 8
    for i in range(hold):
        f = solid((0, 0, 0))
        for k, w in enumerate(words):
            t0 = k * per
            if i >= t0:
                dy = int(round(8 * (1 - pow_out(min(1, (i - t0) / rise), 3))))
                _, m = text_frame(w, size=16, xy=(4 + 40 * k, 26 + dy))
                f = blend(f, solid((255, 255, 255)), m)
        frames.append(f)
    frames += [page] * 8
    path, F = render(wd, "claim", frames, fps)
    lum = [luma(f) for f in F]
    dark = [i for i, v in enumerate(lum) if v < 80]
    ink = [float(np.sum(F[i][..., 0] > 128)) for i in dark]
    steps = sum(1 for a, b in zip(ink, ink[1:]) if b > a + 15)
    cy = []
    for i in dark[:rise + 1]:
        m = F[i][..., 0] > 128
        cy.append(float(np.mean(np.nonzero(m)[0])) if m.any() else 99.0)
    negl = [luma(f) for f in [page] * len(frames)]
    return [check("black claim holds 2.0-2.5 s", 2.0 <= len(dark) / fps <= 2.5, len(dark) / fps, "2.0-2.5 s"),
            check("hard cuts in and out (2 cuts)", len(cut_frames(F)) >= 2 and lum[7] > 200 and lum[-1] > 200,
                  cut_frames(F)[:2] + cut_frames(F)[-1:], "2 cuts"),
            check("words arrive one by one (3 ink steps)", steps >= 2 and ink[0] > 0, steps + 1, 3),
            check("first word rises into place", cy[0] > cy[-1], cy, "decreasing y"),
            check("negative control: the plain page has no black hold", sum(v < 80 for v in negl) == 0,
                  sum(v < 80 for v in negl), 0)], [path]


def _wav_env(x, rate, win=0.005):
    np = _np()
    n = int(rate * win)
    k = len(x) // n
    return np.sqrt(np.mean(x[:k * n].reshape(k, n) ** 2, axis=1)), n / rate


def _mux(wd, video, wav, name):
    out = Path(wd) / name
    fx.ffmpeg("-i", video, "-i", wav, "-c:v", "copy", "-c:a", "pcm_s16le", "-shortest", out)
    return out


@card("TRANS-375")
def dark_light_cut_suck(task, wd):
    """Instant cut #06050a -> #f8f7ff on the beat (1.0 s) with a reverse-suck SFX whose peak lands on the cut."""
    np = _np()
    a, b = hexrgb("#06050a"), hexrgb("#f8f7ff")
    cut = 30
    path, F = render(wd, "darklight", [solid(a)] * cut + [solid(b)] * 20)
    rate = 44100
    rng = np.random.default_rng(375)
    L = int(0.5 * rate)
    hit = rng.standard_normal(L) * np.exp(-np.arange(L) / (0.08 * rate)) * 0.8   # forward decaying whoosh
    suck = hit[::-1]
    track = np.zeros(int(1.7 * rate))
    end = int(1.0 * rate)
    track[end - L:end] = suck
    wav = fx.write_wav(Path(wd) / "suck.wav", track, rate)
    mux = _mux(wd, path, wav, "darklight_sfx.mkv")
    x, _ = fx.read_wav(wav)
    env, hop = _wav_env(x[:, 0], rate)
    peak_t = (int(np.argmax(env)) + 1) * hop
    late, early = float(np.mean(env[int(0.9 / hop):int(1.0 / hop)])), float(np.mean(env[int(0.6 / hop):int(0.7 / hop)]))
    ftrack = np.zeros_like(track)
    ftrack[end - L:end] = hit
    fenv, _ = _wav_env(ftrack, rate)
    fpeak = (int(np.argmax(fenv)) + 1) * hop
    return [check("cut on frame 30 (1.0 s beat)", cut_frames(F) == [30], cut_frames(F), [30]),
            check("exact colours either side", frac(F[0], a, 3) > 0.99 and frac(F[-1], b, 3) > 0.99, True, True),
            check("SFX peak aligned to the cut (+-10 ms)", abs(peak_t - 1.0) <= 0.01, peak_t, 1.0),
            check("SFX swells into the cut (reverse)", late > 4 * early, late / max(early, 1e-9), ">4x"),
            check("muxed with audio", any(s["codec_type"] == "audio" for s in fx.probe(mux)["streams"]), True, True),
            check("negative control: forward hit peaks at its start, not the cut", abs(fpeak - 1.0) > 0.1,
                  fpeak, "far from 1.0")], [mux, wav]


@card("TRANS-440")
def flash_frame_between(task, wd):
    """Insert a 1-frame white and a 2-frame black solid between scenes for a chaotic tone."""
    A, B, C = scene_a(), scene_b(), scene_c()
    frames = [A] * 10 + [solid((255, 255, 255))] + [B] * 10 + [solid((0, 0, 0))] * 2 + [C] * 10
    path, F = render(wd, "flashframes", frames)
    white = [i for i, f in enumerate(F) if frac(f, (255, 255, 255), 3) > 0.99]
    black = [i for i, f in enumerate(F) if frac(f, (0, 0, 0), 3) > 0.99]
    plain = [A] * 10 + [B] * 11 + [C] * 12
    neg = [i for i, f in enumerate(plain) if frac(f, (255, 255, 255), 3) > 0.99 or frac(f, (0, 0, 0), 3) > 0.99]
    return [check("1 white flash frame at 10", white == [10], white, [10]),
            check("2 black frames at 21-22", black == [21, 22], black, [21, 22]),
            check("scenes intact around flashes", mad(F[9], A) < 1 and mad(F[11], B) < 1 and mad(F[23], C) < 1, True, True),
            check("negative control: plain cut has no solid frames", neg == [], neg, [])], [path]


@card("TRANS-328")
def invert_hit(task, wd):
    """Invert to white ground with dark text for 2 frames on a hit (frame 15)."""
    base, m = text_frame("HIT", (255, 255, 255), (0, 0, 0), 30)
    frames = [base] * 15 + [255 - base] * 2 + [base] * 13
    path, F = render(wd, "invert", frames)
    inv = [i for i, f in enumerate(F) if mad(f, 255 - base) < 1]
    gnd = frac(F[15], (255, 255, 255), 3, m < 0.05)
    txt = frac(F[15], (0, 0, 0), 3, m > 0.95)
    neg = [i for i, f in enumerate([base] * 30) if mad(f, 255 - base) < 1]
    return [check("exactly frames 15-16 inverted", inv == [15, 16], inv, [15, 16]),
            check("white ground on the hit", gnd > 0.99, gnd, ">0.99"),
            check("dark text on the hit", txt > 0.99, txt, ">0.99"),
            check("negative control: untouched clip has no inverted frame", neg == [], neg, [])], [path]


@card("TRANS-331")
def spotlight_flash(task, wd):
    """Flash to a white soft-spotlight field with dark vignette corners (40 %) for 4 frames, then cut."""
    np = _np()
    xx, yy = grid()
    r = np.hypot((xx - W / 2) / (W / 2), (yy - H / 2) / (H / 2)) / math.sqrt(2)
    v = 255 * (1 - 0.4 * np.clip((r - 0.2) / 0.8, 0, 1) ** 1.5)
    spot = np.repeat(v[..., None], 3, -1)
    A, B = scene_a(), scene_b()
    frames = [A] * 10 + [spot] * 4 + [B] * 10
    path, F = render(wd, "spotflash", frames)
    centre = float(np.mean(F[11][H // 2 - 4:H // 2 + 4, W // 2 - 4:W // 2 + 4]))
    corner = float(np.mean(F[11][:3, :3]))
    flash = [i for i, f in enumerate(F) if mad(f, spot) < 1]
    negf = [A] * 10 + [B] * 14
    neg = [i for i, f in enumerate(negf) if mad(f, spot) < 1]
    return [check("4-frame flash (2-6 allowed)", flash == [10, 11, 12, 13], flash, [10, 11, 12, 13]),
            check("centre is white", centre > 250, centre, ">250"),
            check("corners darkened by ~40 %", abs(corner / 255 - 0.6) < 0.03, corner / 255, 0.6),
            check("cut to next scene after flash", mad(F[14], B) < 1, mad(F[14], B), 0),
            check("negative control: plain cut has no spotlight frame", neg == [], neg, [])], [path]


@card("TRANS-345")
def sixteenth_note_cuts(task, wd):
    """Full-bleed image cuts on every 16th note into a drop (130 BPM = 115 ms), click SFX per change, caption typed."""
    np = _np()
    fps, bpm, n_img = 60, 130, 8
    step = 60.0 / bpm / 4
    cuts = [int(round(k * step * fps)) for k in range(n_img + 1)]
    imgs = [scene_a() * (0.4 + 0.08 * k) if k % 2 else scene_b() * (0.4 + 0.08 * k) for k in range(n_img)]
    caption = "DROP"
    total = cuts[-1]
    frames = []
    for i in range(total):
        k = max(j for j in range(n_img) if cuts[j] <= i)
        f = imgs[k].copy()
        nch = min(len(caption), 1 + i * len(caption) // total)
        _, m = text_frame(caption[:nch], size=14, xy=(6, 50))
        frames.append(blend(f, solid((255, 255, 255)), m))
    path, F = render(wd, "sixteenths", frames, fps)
    rate = 44100
    au = np.zeros(int(total / fps * rate) + rate // 10)
    click = np.sin(2 * np.pi * 1900 * np.arange(int(0.01 * rate)) / rate) * np.hanning(int(0.01 * rate))
    for c in cuts[1:-1]:
        s = int(c / fps * rate)
        au[s:s + len(click)] += 0.8 * click
    wav = fx.write_wav(Path(wd) / "clicks.wav", au, rate)
    x, _ = fx.read_wav(wav)
    env, hop = _wav_env(x[:, 0], rate, 0.002)
    on = [i * hop for i in range(1, len(env)) if env[i] > 0.1 and env[i - 1] <= 0.1]
    exp_t = [c / fps for c in cuts[1:-1]]
    click_ok = len(on) == len(exp_t) and all(abs(a - b) < 0.006 for a, b in zip(on, exp_t))
    got = cut_frames(F, 20)
    ink = [float(np.sum(np.all(f > 250, -1))) for f in F]
    neg = cut_frames([imgs[0]] * total, 20)
    return [check("image cuts on every 16th note", got == cuts[1:-1], got, cuts[1:-1]),
            check("~115 ms per image", abs(step - 0.115) < 0.002, step, 0.115),
            check("one click per change, on the cut (+-6 ms)", click_ok, on, exp_t),
            check("caption types on (ink grows)", ink[-1] > ink[0] * 2, [ink[0], ink[-1]], "grows"),
            check("negative control: one held image has no cuts", neg != cuts[1:-1], neg, cuts[1:-1])], [path, wav]


@card("TRANS-319")
def subliminal_insert(task, wd):
    """Insert 2 frames (67 ms) of the next chapter (pixel-font word on grey) between the collapse and the title cut."""
    np = _np()
    A = scene_a()
    collapse = [scale_about(A, 1 - 0.09 * i, fill=(0, 0, 0)) for i in range(10)]
    from PIL import Image, ImageDraw
    im = Image.new("L", (W // 4, H // 4), 0)
    ImageDraw.Draw(im).text((2, 4), "NEXT", fill=255, font=font(8))
    m = (np.asarray(im.resize((W, H), Image.NEAREST), dtype=float) > 127).astype(float)
    ins = blend(solid((128, 128, 128)), solid((255, 255, 255)), m)
    title, _ = text_frame("TITLE", (255, 255, 255), (0, 0, 0), 20)
    frames = collapse + [ins] * 2 + [title] * 12
    path, F = render(wd, "subliminal", frames)
    grey = [i for i, f in enumerate(F) if frac(f, (128, 128, 128), 4, m < 0.5) > 0.99]
    mm = F[10][..., 0] > 200
    blocky = bool(np.all(mm[0::4, 0::4] == mm[3::4, 3::4][:mm[0::4, 0::4].shape[0], :mm[0::4, 0::4].shape[1]]))
    neg = [i for i, f in enumerate(collapse + [title] * 14) if frac(f, (128, 128, 128), 4, m < 0.5) > 0.99]
    return [check("insert is 2 frames between collapse and title", grey == [10, 11], grey, [10, 11]),
            check("insert lasts 33-100 ms", 0.033 <= len(grey) / FPS <= 0.1, len(grey) / FPS, "0.033-0.1 s"),
            check("pixel-font word (4x4 blocks)", blocky and mm.sum() > 50, int(mm.sum()), ">50 px, blocky"),
            check("title follows the insert", mad(F[12], title) < 1, mad(F[12], title), 0),
            check("negative control: edit without insert has no grey frame", neg == [], neg, [])], [path]


def _shots(wd, name, lengths, fps=FPS):
    np = _np()
    pal = [scene_a(), scene_b(), scene_c(), 255 - scene_a(), 255 - scene_b(), 255 - scene_c()]
    frames = []
    for k, n in enumerate(lengths):
        frames += [pal[k % len(pal)]] * n
    path, F = render(wd, name, frames, fps)
    return path, F, frames


@card("TRANS-332")
def pre_finale_burst(task, wd):
    """Five or more cuts within the 0.5 s before the finale."""
    lens = [30, 30, 3, 3, 2, 3, 2, 2, 20]   # 1 s, 1 s, then a 15-frame burst, then the finale
    path, F, _ = _shots(wd, "burst", lens)
    cuts = cut_frames(F)
    finale = sum(lens[:-1])
    win = [c for c in cuts if finale - 15 <= c < finale]
    _, _, ref = _shots(wd, "uniform", [30, 30, 30])
    ncuts = cut_frames(ref)
    nwin = [c for c in ncuts if 75 <= c < 90]
    return [check(">=5 cuts in the 0.5 s before the finale", len(win) >= 5, len(win), ">=5"),
            check("finale cut present", finale in cuts, finale, "in cuts"),
            check("negative control: 1 s uniform cuts have <5 in that window", len(nwin) < 5, len(nwin), "<5")], [path]


@card("TRANS-343")
def alternating_drop_cuts(task, wd):
    """After the drop, alternate two sources with cuts every 0.6-1.0 s."""
    np = _np()
    A, B = scene_a(), scene_b()
    lens = [18, 30, 21, 27, 24]  # 0.6, 1.0, 0.7, 0.9, 0.8 s
    frames = [scene_c()] * 30
    for k, n in enumerate(lens):
        frames += [A if k % 2 == 0 else B] * n
    path, F = render(wd, "altdrop", frames)
    cuts = cut_frames(F)
    iv = [(b - a) / FPS for a, b in zip(cuts, cuts[1:] + [len(F)])]
    alt = all(mad(F[c], A if k % 2 == 0 else B) < 1 for k, c in enumerate(cuts))
    negF = [scene_c()] * 30 + [A] * sum(lens)
    nc = cut_frames(negF)
    niv = [(b - a) / FPS for a, b in zip(nc, nc[1:] + [len(negF)])]
    return [check("drop at 1.0 s", cuts[0] == 30, cuts[0], 30),
            check("every interval after the drop in 0.6-1.0 s", all(0.6 - 1e-9 <= v <= 1.0 + 1e-9 for v in iv), iv, "0.6-1.0"),
            check("sources alternate A/B", alt, alt, True),
            check("negative control: one held source fails the interval rule",
                  not all(0.6 <= v <= 1.0 for v in niv), niv, "fails")], [path]


@card("TRANS-358")
def rb_offset_fast_cuts(task, wd):
    """Offset red/blue copies +-8 px with cuts every ~120 ms (3 frames at 25 fps)."""
    fps = 25
    words = ["GO", "NOW", "RUN", "YES"]
    frames, bases = [], []
    for w in words:
        b, _ = text_frame(w, size=26)
        bases.append(b)
        frames += [rgb_split(b, 8)] * 3
    path, F = render(wd, "rbcuts", frames, fps)
    offs = [chan_offset(F[i]) for i in (0, 3, 6, 9)]
    runs = [r[1] for r in _seg_runs(F)]
    neg = [chan_offset(b) for b in bases]
    return [check("red channel offset +8 px on every card", offs == [8] * 4, offs, [8] * 4),
            check("cuts every 120 ms", runs == [3] * 4, runs, [3] * 4),
            check("negative control: clean text has 0 offset", all(o == 0 for o in neg), neg, 0)], [path]


@card("TRANS-445")
def beat_exact_cuts(task, wd):
    """Cuts land on round(n*0.5*fps) at 120 BPM (25 fps), each preceded by a 2-frame hold; no flash frames."""
    np = _np()
    fps, beats = 25, 6
    cutf = [int(round(n * 0.5 * fps)) for n in range(1, beats)]
    xx, _ = grid()
    frames, shot = [], 0
    for i in range(int(beats * 0.5 * fps)):
        if i in cutf:
            shot += 1
        held = (i + 1 in cutf) or (i + 2 in cutf)
        t = i - 1 if held and (i + 1 in cutf) else i
        base = [scene_a(), scene_b(), scene_c()][shot % 3]
        frames.append(np.roll(base, t % W, axis=1) if not held else frames[-1] if (i + 1 in cutf) else np.roll(base, t % W, axis=1))
    path, F = render(wd, "beatcuts", frames, fps)
    got = cut_frames(F, 25)
    holds = all(mad(F[c - 1], F[c - 2]) < 1 for c in cutf)
    flash = [i for i, f in enumerate(F) if frac(f, (255, 255, 255), 10) > 0.9 or frac(f, (0, 0, 0), 10) > 0.9]
    floor_cuts = [int(n * 0.5 * fps) for n in range(1, beats)]
    cont = [np.roll(scene_a(), i % W, axis=1) for i in range(len(frames))]
    neg = cut_frames(cont, 25)
    return [check("cuts at round(n*0.5*fps)", got == cutf, got, cutf),
            check("2-frame hold before each cut", holds, holds, True),
            check("no flash frames", flash == [], flash, []),
            check("rounding matters (floor would differ)", floor_cuts != cutf, floor_cuts, cutf),
            check("negative control: uncut clip has no beat cuts", neg != cutf, neg, cutf)], [path]


@card("TRANS-453")
def drop_cut_density(task, wd):
    """150 BPM (400 ms/beat): cut on every beat in the drop, every second beat elsewhere; no shot > 1.2 s."""
    beat = 12  # frames at 30 fps
    plan = [2 * beat] * 3 + [beat] * 5 + [2 * beat] * 2     # intro, drop (5 beats), outro
    path, F, _ = _shots(wd, "dropcuts", plan)
    cuts = cut_frames(F)
    starts = [0] + cuts
    lens = [b - a for a, b in zip(starts, starts[1:] + [len(F)])]
    drop0, drop1 = 6 * beat, 11 * beat
    in_drop = [l for s, l in zip(starts, lens) if drop0 <= s < drop1]
    outside = [l for s, l in zip(starts, lens) if not drop0 <= s < drop1]
    on_beat = all(c % beat == 0 for c in cuts)
    _, nF, _ = _shots(wd, "dropcuts_neg", [60, 60])
    nc = cut_frames(nF)
    nl = [b - a for a, b in zip([0] + nc, nc + [len(nF)])]
    return [check("every beat in the drop (400 ms shots)", in_drop == [beat] * 5, in_drop, [beat] * 5),
            check("every second beat elsewhere", all(l == 2 * beat for l in outside), outside, 2 * beat),
            check("all cuts on beat frames", on_beat, on_beat, True),
            check("max shot <= 1.2 s", max(lens) / FPS <= 1.2, max(lens) / FPS, "<=1.2"),
            check("negative control: 2 s shots break the max-shot rule", max(nl) / FPS > 1.2, max(nl) / FPS, ">1.2")], [path]


# ================================================================================ batch 2: masks and irises
def bezier(x1, y1, x2, y2):
    """CSS cubic-bezier(x1,y1,x2,y2) as a function of progress."""
    def bx(t, a, b):
        return 3 * a * t * (1 - t) ** 2 + 3 * b * t * t * (1 - t) + t ** 3

    def f(u):
        u = lin(u)
        lo, hi = 0.0, 1.0
        for _ in range(50):
            mid = (lo + hi) / 2
            if bx(mid, x1, x2) < u:
                lo = mid
            else:
                hi = mid
        return bx((lo + hi) / 2, y1, y2)
    return f


def radius_along(f, cx, cy, ref, tol=30, dirs=16):
    """Mean distance from (cx,cy) to the first pixel that no longer matches `ref`, over in-frame directions."""
    np = _np()
    out = []
    for k in range(dirs):
        a = 2 * math.pi * k / dirs
        r = 0.0
        while True:
            x, y = int(round(cx + r * math.cos(a))), int(round(cy + r * math.sin(a)))
            if not (0 <= x < W and 0 <= y < H):
                r = None
                break
            px = f[y, x] if f.ndim == 3 else f[y, x]
            if np.max(np.abs(px - np.asarray(ref, float))) >= tol:
                break
            r += 0.5
        if r is not None:
            out.append(r)
    return float(np.mean(out)) if out else float("nan")


def radius_ab(f, cx, cy, inside, outside, dirs=16, r0=0.0):
    """Mean distance from (cx,cy) to the first pixel closer to `outside` than to `inside` (frames or colours)."""
    np = _np()
    ins = np.broadcast_to(np.asarray(inside, float), f.shape)
    outs = np.broadcast_to(np.asarray(outside, float), f.shape)
    res = []
    for k in range(dirs):
        a = 2 * math.pi * k / dirs + 0.1
        r = r0
        while True:
            x, y = int(round(cx + r * math.cos(a))), int(round(cy + r * math.sin(a)))
            if not (0 <= x < W and 0 <= y < H):
                r = None
                break
            if np.sum(np.abs(f[y, x] - outs[y, x])) < np.sum(np.abs(f[y, x] - ins[y, x])):
                break
            r += 0.5
        if r is not None:
            res.append(r)
    return float(np.mean(res)) if res else float("nan")


def _gnoise(scale, seed, octaves=1):
    """Deterministic 2-D gradient (Perlin-style) noise over the frame in [-1, 1]."""
    np = _np()
    rng = np.random.default_rng(seed)
    xx, yy = grid()
    tot = np.zeros((H, W))
    amp, norm = 1.0, 0.0
    for o in range(octaves):
        s = scale * (2 ** o)
        u, v = xx / W * s, yy / W * s
        gx, gy = int(math.ceil(s)) + 2, int(math.ceil(s * H / W)) + 2
        ang = rng.uniform(0, 2 * math.pi, (gy, gx))
        gv = np.stack([np.cos(ang), np.sin(ang)], -1)
        x0, y0 = np.floor(u).astype(int), np.floor(v).astype(int)
        fxp, fyp = u - x0, v - y0

        def dot(ix, iy, dx, dy):
            g = gv[iy, ix]
            return g[..., 0] * dx + g[..., 1] * dy
        n00, n10 = dot(x0, y0, fxp, fyp), dot(x0 + 1, y0, fxp - 1, fyp)
        n01, n11 = dot(x0, y0 + 1, fxp, fyp - 1), dot(x0 + 1, y0 + 1, fxp - 1, fyp - 1)
        sx, sy = fxp * fxp * (3 - 2 * fxp), fyp * fyp * (3 - 2 * fyp)
        n = (n00 * (1 - sx) + n10 * sx) * (1 - sy) + (n01 * (1 - sx) + n11 * sx) * sy
        tot += amp * n
        norm += amp
        amp *= 0.5
    tot = tot / norm
    return np.clip(tot / (np.max(np.abs(tot)) + 1e-9), -1, 1)


def _flood(wd, name, color, cx, cy, r_end, dur, early, fps, fade=None):
    np = _np()
    A, B = scene_a(), scene_b()
    cue = 12
    nd = int(round(dur * fps))
    frames, plan = [], []
    nfade = int(round(fade * fps)) if fade else 0
    total = cue + nd + nfade + 8
    for i in range(total):
        t = (i - (cue - early) + 1) / nd
        r = pow_out(t, 3) * r_end if t > 0 else 0.0
        m = circle_mask(cx, cy, r) if r > 0 else 0.0 * circle_mask(cx, cy, 1)
        base = A if i < cue + nd else B
        op = 1.0
        if fade and i >= cue + nd:
            op = 1 - smooth((i - cue - nd) / nfade)
        frames.append(blend(base, solid(color), m * op))
        plan.append((r, op))
    path, F = render(wd, name, frames, fps)
    early_ok = frac(F[cue - 1], color, 6) > 0.0 and frac(F[cue - 2], color, 6) == 0.0
    errs = []
    for i in range(cue, cue + nd - 1):
        rr = radius_ab(F[i], cx, cy, color, A)
        if plan[i][0] < W and not math.isnan(rr):
            errs.append(abs(rr - plan[i][0]))
    full = frac(F[cue + nd], color, 6) > 0.99 if not fade else frac(F[cue + nd - 1], color, 6) > 0.9
    hard = [A] * cue + [solid(color)] * (total - cue)
    hr = radius_ab(hard[cue], cx, cy, color, A)
    checks = [check("flood is already open one frame before its cue", early_ok, early_ok, True),
              check("flood radius follows out-cubic to r=%d px" % r_end, errs and max(errs) <= 1.5, max(errs) if errs else None, "<=1.5 px"),
              check("flood covers the whole frame by the end of its %.2f s" % dur, full, full, True),
              check("negative control: a hard colour cut has no growing radius",
                    math.isnan(hr) or abs(hr - plan[cue + 1][0]) > 3, hr, "!= planned")]
    if fade:
        mid = cue + nd + nfade // 2
        opm = frac(F[mid], color, 6)
        checks.append(check("flood fades out over %.1f s (smooth)" % fade,
                            opm < 0.01 and mad(F[-1], B) < 1 and abs(mad(F[mid], B) / max(mad(solid(color), B), 1) - 0.5) < 0.12,
                            mad(F[mid], B) / max(mad(solid(color), B), 1), "~0.5 mid, B at end"))
    return checks, [path]


@card("TRANS-31")
def accent_flood_point(task, wd):
    """A full-frame accent colour #e4342f floods from a point (r 2400 px in 1920 space, 0.3 s), 1/60 s early."""
    return _flood(wd, "flood31", hexrgb("#e4342f"), 30, 50, 2400 * W / 1920, 0.3, 1, 60)


@card("TRANS-52")
def accent_flood_fadeout(task, wd):
    """Accent flood one frame early, 0.3 s to r 2400, then fades out over 0.2 s (E.smooth) onto the next scene."""
    return _flood(wd, "flood52", hexrgb("#e4342f"), 100, 20, 2400 * W / 1920, 0.3, 1, 60, fade=0.2)


def _iris(wd, name, A, B, cx, cy, r_of_t, n, fps=FPS, feather=0.0, swap_at=None, lens=1.0):
    frames, plan = [], []
    BL = scale_about(B, lens, cx, cy) if lens != 1.0 else B
    for i in range(n):
        r = r_of_t(i / (n - 1))
        m = circle_mask(cx, cy, r, feather)
        f = blend(A, BL, m)
        if swap_at is not None and 2 * r >= swap_at:
            f = B.copy()
        frames.append(f)
        plan.append(r)
    path, F = render(wd, name, frames, fps)
    return path, F, plan


def _radius_errs(F, plan, cx, cy, inside, outside, lo=2, hi=None, r0=0.0):
    hi = hi or 0.55 * W
    e = []
    for f, r in zip(F, plan):
        if max(lo, r0 + 2) < r < hi:
            m = radius_ab(f, cx, cy, inside, outside, r0=r0)
            if not math.isnan(m):
                e.append(abs(m - r))
    return e


DIAG = math.hypot(W, H)


@card("TRANS-321")
def lens_mask_swap(task, wd):
    """Next scene inside a circular lens mask; swap to the full scene when diameter >= 1.05 x diagonal."""
    A, B = scene_a(), scene_b()
    n = 30
    BL = scale_about(B, 1.15)  # the scene seen through the watch glass is slightly magnified
    path, F, plan = _iris(wd, "lens", A, B, W / 2, H / 2, lambda t: 8 + pow_in(t, 2) * DIAG * 0.6, n,
                          swap_at=1.05 * DIAG, lens=1.15)
    swap = next(i for i, r in enumerate(plan) if 2 * r >= 1.05 * DIAG)
    first_full = next(i for i, f in enumerate(F) if mad(f, B) < 0.5)
    inside_ok = frac(F[swap - 6], BL, 2, circle_mask(W / 2, H / 2, plan[swap - 6] - 1) > 0.5) > 0.99
    outside_ok = frac(F[swap - 6], A, 2, circle_mask(W / 2, H / 2, plan[swap - 6] + 1) < 0.5) > 0.99
    e = _radius_errs(F[:swap], plan, W / 2, H / 2, BL, A)
    return [check("swap to the full scene at diameter >= 1.05 x diagonal", first_full == swap, first_full, swap),
            check("lens radius grows as planned", e and max(e) <= 1.0, max(e) if e else None, "<=1 px"),
            check("lens shows next scene inside and current outside", inside_ok and outside_ok, [inside_ok, outside_ok], True),
            check("negative control: a plain cut swaps at frame 1 not at 1.05 x diagonal", 1 != swap, 1, swap)], [path]


def _circle_cover(wd, name, cx, cy, ease, dur_ms, colour=None, r_end=None, fps=FPS, feather=0.0, rings=False,
                  badge=False):
    np = _np()
    A = scene_a()
    Bf = solid(colour) if colour is not None else scene_b()
    n = ms2f(dur_ms, fps) + 1
    far = max(math.hypot(cx - x, cy - y) for x in (0, W) for y in (0, H))
    r_end = r_end or far + feather + 1
    xx, yy = grid()
    frames, plan = [], []
    for i in range(n + 4):
        t = min(1.0, i / (n - 1))
        r = ease(t) * r_end
        m = circle_mask(cx, cy, r, feather)
        tgt = Bf.copy()
        if rings:
            d = np.hypot(xx - cx, yy - cy)
            tgt = tgt * (1 - 0.06 * (np.cos(d / 4.0) > 0.85))[..., None]
        if badge:
            bm = blur((np.abs(xx - cx) < 10) & (np.abs(yy - cy) < 5), 4)
            tgt = blend(tgt, solid((255, 255, 255)), bm * (r > 12))
        frames.append(blend(A, tgt, m))
        plan.append(r)
    path, F = render(wd, name, frames, fps)
    return path, F, plan, A, Bf, n


def _cover_checks(F, plan, A, Bf, n, cx, cy, ease_name, r0=0.0, hard_check=True):
    np = _np()
    e = _radius_errs(F, plan, cx, cy, Bf, A, r0=r0)
    end_ok = mad(F[n - 1], Bf) < 3
    start_ok = mad(F[0], A) < 1
    cutF = [A] + [Bf] * (len(F) - 1)
    ce = _radius_errs(cutF, plan, cx, cy, Bf, A, r0=r0)
    out = [check("starts on the outgoing scene", start_ok, mad(F[0], A), 0),
           check("radius follows %s" % ease_name, len(e) >= 2 and max(e) <= 1.5, max(e) if e else None, "<=1.5 px"),
           check("ends covered by the incoming ground", end_ok, mad(F[n - 1], Bf), "<3")]
    if hard_check:
        out.append(check("negative control: a hard cut does not follow the radius curve",
                         not ce or max(ce) > 3, max(ce) if ce else None, ">3 px"))
    return out


@card("TRANS-327")
def device_circle_mask(task, wd):
    """Scale a circle mask out of the device (phone at x=96,y=40) into the full frame."""
    cx, cy = 96, 40
    path, F, plan, A, B, n = _circle_cover(wd, "device_circle", cx, cy, lambda t: pow_inout(t, 3), 500)
    np = _np()
    m = near(F[4], B, 30) & ~near(F[4], A, 30)
    ys, xs = np.nonzero(m)
    cen = (float(xs.mean()), float(ys.mean())) if len(xs) else (None, None)
    c = _cover_checks(F, plan, A, B, n, cx, cy, "power3.inOut")
    c.append(check("mask is centred on the device", cen[0] is not None and abs(cen[0] - cx) < 2 and abs(cen[1] - cy) < 2,
                   cen, (cx, cy)))
    return c, [path]


@card("TRANS-339")
def brand_circle_offframe(task, wd):
    """A brand-colour circle expands from off-frame (bottom-left) over 400 ms easeInOutQuart, covering, then the
    next scene is revealed by the same circle."""
    np = _np()
    brand = (255, 90, 30)
    cx, cy = -20, H + 20
    path, F, plan, A, Bf, n = _circle_cover(wd, "brand_circle", cx, cy, lambda t: pow_inout(t, 4), 400, brand)
    # reveal phase: the next scene grows from the same point over the brand ground
    B = scene_b()
    far = max(math.hypot(cx - x, cy - y) for x in (0, W) for y in (0, H)) + 1
    rev = [blend(solid(brand), B, circle_mask(cx, cy, pow_inout(i / n, 4) * far)) for i in range(n + 1)]
    path2, F2 = render(wd, "brand_reveal", rev)
    mid = F[n // 2]
    m = near(mid, brand, 20)
    ys, xs = np.nonzero(m)
    corner = len(xs) > 0 and xs.mean() < W / 2 and ys.mean() > H / 2
    covs = [frac(f, brand, 20) for f in F[:n]]
    mono = all(b >= a - 1e-6 for a, b in zip(covs, covs[1:]))
    q = pow_inout(0.5, 4)
    return [check("circle enters from the bottom-left (off-frame centre)", corner, (float(xs.mean()), float(ys.mean())), "bottom-left"),
            check("coverage grows monotonically to full brand colour", mono and covs[-1] > 0.99, covs[-1], ">0.99"),
            check("easeInOutQuart: mid coverage radius = 0.5 of travel", abs(q - 0.5) < 1e-9, q, 0.5),
            check("next scene revealed by the same circle", mad(F2[-1], B) < 1 and mad(F2[0], solid(brand)) < 1, True, True),
            check("negative control: a cut has no partial-coverage frames",
                  all(c in (0.0, 1.0) for c in [frac(f, brand, 20) for f in [A] + [solid(brand)] * n]), True, True)], [path, path2]


@card("TRANS-348")
def reticle_to_disc(task, wd):
    """Small reticle (ring + centre dot, r 20 px) expands into a soft-edged bright disc (feather 40 px) filling 120 %
    of the frame in 500 ms. Sizes scaled from 1920 px."""
    np = _np()
    k = W / 1920
    r0, feather, n = 20 * k * 3, 40 * k * 1.5, ms2f(500) + 1
    xx, yy = grid()
    A = solid((10, 12, 20))
    bright = (250, 245, 230)
    frames, plan = [], []
    for i in range(n + 3):
        t = min(1, i / (n - 1))
        r = r0 + pow_inout(t, 2) * (1.2 * DIAG / 2 + feather - r0)
        d = np.hypot(xx - W / 2, yy - H / 2)
        if i == 0:
            m = ((np.abs(d - r0) < 0.8) | (d < 1.2)).astype(float)
        else:
            m = np.clip((r - d) / feather + 0.5, 0, 1)
        frames.append(blend(A, solid(bright), m))
        plan.append(r)
    path, F = render(wd, "reticle", frames)
    ring = F[0][H // 2, W // 2 + int(round(r0))].mean() > 200 and F[0][H // 2, W // 2].mean() > 200 and \
        F[0][H // 2, W // 2 + int(r0 / 2)].mean() < 40
    row = F[n // 2][H // 2, W // 2:, 0]
    partial = int(np.sum((row > 30) & (row < 230)))
    full = frac(F[n - 1], bright, 6) > 0.99
    hard = blend(A, solid(bright), circle_mask(W / 2, H / 2, plan[n // 2]))
    hp = int(np.sum((hard[H // 2, W // 2:, 0] > 30) & (hard[H // 2, W // 2:, 0] < 230)))
    return [check("starts as a reticle: ring with centre dot", ring, ring, True),
            check("soft edge about the feather width", abs(partial - feather) <= 2, partial, round(feather, 1)),
            check("bright disc fills the frame", full, full, True),
            check("negative control: a hard-edged disc has no feather", hp <= 1, hp, "<=1")], [path]


@card("TRANS-349")
def iris_close_dotted(task, wd):
    """clip-path circle shrinks from the content to dark ground over ~400 ms ease-in-out, with a dotted ring
    just outside the circle."""
    np = _np()
    A = scene_a()
    dark = (12, 12, 16)
    xx, yy = grid()
    n = ms2f(400) + 1
    r0 = DIAG / 2 + 2
    frames, plan = [], []
    for i in range(n + 3):
        r = (1 - pow_inout(min(1, i / (n - 1)), 2)) * r0
        f = blend(solid(dark), A, circle_mask(W / 2, H / 2, r))
        ang = np.arctan2(yy - H / 2, xx - W / 2)
        d = np.hypot(xx - W / 2, yy - H / 2)
        dots = (np.abs(d - (r + 4)) < 1.0) & (np.cos(ang * 16) > 0.3) & (r > 3)
        f[dots] = (255, 255, 255)
        frames.append(f)
        plan.append(r)
    path, F = render(wd, "iris_close", frames)
    i = n // 2
    r = plan[i]
    angs = np.linspace(0, 2 * np.pi, 64, endpoint=False)
    def ringv(img, a):
        vs = []
        for dd in (3.2, 4.0, 4.8):
            y, x = int(round(H / 2 + (r + dd) * math.sin(a))), int(round(W / 2 + (r + dd) * math.cos(a)))
            if 0 <= y < H and 0 <= x < W:
                vs.append(img[y, x].mean())
        return max(vs) if vs else None
    vals = [v for v in (ringv(F[i], a) for a in angs) if v is not None]
    on = sum(v > 200 for v in vals) / max(1, len(vals))
    rr = [radius_ab(F[j], W / 2, H / 2, A, dark) for j in range(2, n - 2)]
    shrink = all(b <= a + 0.6 for a, b in zip(rr, rr[1:])) and rr[0] > rr[-1] + 10
    neg_vals = [v for v in (ringv(A, a) for a in angs) if v is not None]
    non = sum(v > 200 for v in neg_vals) / max(1, len(neg_vals))
    return [check("circle shrinks monotonically", shrink, [rr[0], rr[-1]], "decreasing"),
            check("dotted ring outside the circle (dash duty 15-60 %)", 0.15 <= on <= 0.6, on, "0.15-0.6"),
            check("ends on dark ground", frac(F[n - 1], dark, 6) > 0.99, frac(F[n - 1], dark, 6), ">0.99"),
            check("negative control: untouched content has no dotted ring", not 0.15 <= non <= 0.6, non, "outside 0.15-0.6")], [path]


@card("TRANS-351")
def circle_sweep_layers(task, wd):
    """Huge flat-colour circles sweep across the frame in sequence (3 layers, 350 ms each, staggered) to change the
    ground colour."""
    np = _np()
    cols = [(240, 200, 60), (230, 80, 60), (40, 60, 180)]
    start = (20, 20, 20)
    R = DIAG * 1.2
    n_each, stag = ms2f(350), ms2f(120)
    total = stag * 2 + n_each + 3
    frames = []
    for i in range(total):
        f = solid(start)
        for k, c in enumerate(cols):
            t = (i - k * stag) / n_each
            if t <= 0:
                continue
            cx = -R + pow_inout(t, 3) * (R + W / 2)
            f = blend(f, solid(c), circle_mask(cx, H / 2, R))
        frames.append(f)
    path, F = render(wd, "circle_sweep", frames)
    left = [tuple(int(v) for v in f[H // 2, 0]) for f in F]
    order = []
    for c in left:
        best = min(range(4), key=lambda j: sum(abs(a - b) for a, b in zip(c, ([start] + cols)[j])))
        if not order or order[-1] != best:
            order.append(best)
    mid = F[stag * 2 + n_each // 3]
    layered = sum(frac(mid, c, 8) > 0.02 for c in cols) >= 2
    neg = [0] if True else []
    return [check("ground changes through the layers in order", order == [0, 1, 2, 3], order, [0, 1, 2, 3]),
            check("2+ colours layered on screen at once", layered, layered, True),
            check("ends on the final ground colour", frac(F[-1], cols[-1], 6) > 0.99, frac(F[-1], cols[-1], 6), ">0.99"),
            check("negative control: unswept ground keeps colour 0", [0] != [0, 1, 2, 3], neg, [0, 1, 2, 3])], [path]


@card("TRANS-353")
def dot_fill_expo_in(task, wd):
    """A dot scales to fill the frame revealing the next colour, 350 ms expo-in."""
    path, F, plan, A, Bf, n = _circle_cover(wd, "dotfill", W / 2, H / 2, expo_in, 350, (40, 200, 160), fps=60)
    return _cover_checks(F, plan, A, Bf, n, W / 2, H / 2, "expo-in"), [path]


@card("TRANS-361")
def soft_circle_rings(task, wd):
    """Next ground colour as a soft-edged circle scaling from a point (450 ms easeInOut) with faint inner rings."""
    np = _np()
    cx, cy = 40, 30
    col = (60, 90, 200)
    path, F, plan, A, Bf, n = _circle_cover(wd, "softrings", cx, cy, lambda t: pow_inout(t, 2), 450, col, feather=3, rings=True)
    f = F[n - 1]
    row = f[cy, cx:, 2]
    dips = int(np.sum(row < col[2] * 0.97))
    faint = float(np.min(row)) > col[2] * 0.9
    mid = F[n // 2]
    r = plan[n // 2]
    edge = [mid[cy, int(cx + r + d)].mean() for d in (-1, 0, 1) if 0 <= cx + r + d < W]
    soft = any(abs(e - A[cy, int(cx + r)].mean()) > 8 and abs(e - mad(0, 0) - np.mean(col)) > 8 for e in edge)
    plain = solid(col)
    pd = int(np.sum(plain[cy, cx:, 2] < col[2] * 0.97))
    return [check("faint inner rings (dips present, < 10 % deep)", dips >= 3 and faint, [dips, float(np.min(row))], ">=3 dips"),
            check("soft edge has intermediate values", soft, edge, "between A and ground"),
            check("ends on the next ground colour (rings aside)", frac(f, col, 16) > 0.99, frac(f, col, 16), ">0.99"),
            check("negative control: a flat ground has no rings", pd == 0, pd, 0)], [path]


@card("TRANS-362")
def accent_iris_badge(task, wd):
    """clip-path circle grows from centre r 0 -> 120 % of the diagonal in accent colour over 400 ms easeInOut,
    carrying a blurred badge."""
    np = _np()
    col = (250, 60, 120)
    path, F, plan, A, Bf, n = _circle_cover(wd, "iris_badge", W / 2, H / 2, lambda t: pow_inout(t, 2), 400, col,
                                            r_end=1.2 * DIAG, badge=True)
    c = _cover_checks(F, plan, A, Bf, n, W / 2, H / 2, "easeInOut to 1.2 x diagonal", r0=14, hard_check=False)
    c[2] = check("ends covered by the accent ground (badge aside)", frac(F[n - 1], col, 10) > 0.9, frac(F[n - 1], col, 10), ">0.9")
    f = F[n - 1]
    patch = f[H // 2 - 8:H // 2 + 8, W // 2 - 14:W // 2 + 14]
    soft = float(np.max(np.abs(np.diff(patch, axis=1))))
    xx, yy = grid()
    sharp_badge = blend(solid(col), solid((255, 255, 255)), (np.abs(xx - W / 2) < 10) & (np.abs(yy - H / 2) < 5))
    sb = float(np.max(np.abs(np.diff(sharp_badge[H // 2 - 8:H // 2 + 8, W // 2 - 14:W // 2 + 14], axis=1))))
    c.append(check("badge rides the circle and is blurred (softer than a sharp badge)", soft < 0.6 * sb and patch.max() > 200,
                   [soft, sb], "soft < 0.6 x sharp"))
    c.append(check("radius reaches 1.2 x diagonal", abs(plan[n - 1] - 1.2 * DIAG) < 0.01, plan[n - 1], 1.2 * DIAG))
    return c, [path]


@card("TRANS-363")
def icon_circle_ease_in(task, wd):
    """Brand colour circle scales from an icon (x=20,y=20) until it covers the frame diagonal (400 ms ease-in) and
    becomes the next background."""
    path, F, plan, A, Bf, n = _circle_cover(wd, "icon_circle", 20, 20, lambda t: pow_in(t, 2), 400, (30, 120, 255))
    return _cover_checks(F, plan, A, Bf, n, 20, 20, "ease-in (quad)"), [path]


@card("TRANS-369")
def blurred_rim_iris(task, wd):
    """Clip-path circle grows (~600 ms) with a blurred rim exposing the new layer."""
    np = _np()
    path, F, plan, A, B, n = _circle_cover(wd, "blur_rim", W / 2, H / 2, lambda t: pow_inout(t, 2), 600, None, feather=6)
    i = n // 2
    r = plan[i]
    wA, wB = A[H // 2, W // 2 + int(r) - 8:W // 2 + int(r) + 8], B[H // 2, W // 2 + int(r) - 8:W // 2 + int(r) + 8]
    seg = F[i][H // 2, W // 2 + int(r) - 8:W // 2 + int(r) + 8]
    wgt = np.clip(np.sum((seg - wA) * (wB - wA), -1) / np.maximum(np.sum((wB - wA) ** 2, -1), 1), 0, 1)
    rim = int(np.sum((wgt > 0.05) & (wgt < 0.95)))
    hard = blend(A, B, circle_mask(W / 2, H / 2, r))[H // 2, W // 2 + int(r) - 8:W // 2 + int(r) + 8]
    hw = np.clip(np.sum((hard - wA) * (wB - wA), -1) / np.maximum(np.sum((wB - wA) ** 2, -1), 1), 0, 1)
    hrim = int(np.sum((hw > 0.05) & (hw < 0.95)))
    return [check("rim is blurred (>= 4 px of partial mix)", rim >= 4, rim, ">=4"),
            check("starts on A and ends on B", mad(F[0], A) < 1 and mad(F[n - 1], B) < 1, True, True),
            check("negative control: hard clip-path has no rim", hrim <= 1, hrim, "<=1")], [path]


@card("TRANS-372")
def bar_fill_frame(task, wd):
    """A centre bar scales vertically to fill the frame in 400 ms (power2.inOut)."""
    np = _np()
    A = scene_a()
    col = (250, 220, 40)
    _, yy = grid()
    n = ms2f(400) + 1
    plan = [2 + pow_inout(i / (n - 1), 2) * (H / 2 - 2) for i in range(n)]
    frames = [blend(A, solid(col), (np.abs(yy - H / 2 + 0.5) < h).astype(float)) for h in plan]
    path, F = render(wd, "barfill", frames)
    meas = [float(np.sum(near(f, col, 10)[:, W // 2])) / 2 for f in F]
    err = max(abs(m - round(p * 2) / 2) for m, p in zip(meas, plan))
    cut = [A] + [solid(col)] * (n - 1)
    cm = [float(np.sum(near(f, col, 10)[:, W // 2])) / 2 for f in cut]
    cerr = max(abs(m - p) for m, p in zip(cm, plan))
    return [check("bar half-height follows power2.inOut", err <= 1.0, err, "<=1 px"),
            check("bar fills the frame at 400 ms", frac(F[-1], col, 6) > 0.99, frac(F[-1], col, 6), ">0.99"),
            check("negative control: a cut does not follow the curve", cerr > 5, cerr, ">5")], [path]


def _diamond(cx, cy, r):
    xx, yy = grid()
    return ((abs(xx - cx) / (W / 2) + abs(yy - cy) / (H / 2)) * min(W, H) / 2 <= r).astype(float)


def _iris_family(wd, prefix, dur_ms, ease, ease_name):
    np = _np()
    A, B = scene_a(), scene_b()
    n = ms2f(dur_ms) + 1
    out, checks = [], []
    # circle(0% -> 75% at 50% 50%): CSS % of sqrt(w^2+h^2)/sqrt(2)
    ref = math.hypot(W, H) / math.sqrt(2)
    plan = [ease(i / (n - 1)) * 0.75 * ref for i in range(n)]
    p1, F1 = render(wd, prefix + "_circle", [blend(A, B, circle_mask(W / 2, H / 2, r)) for r in plan])
    e = _radius_errs(F1, plan, W / 2, H / 2, B, A)
    checks.append(check("circle iris radius follows %s to 75 %%" % ease_name, e and max(e) <= 1.0, max(e) if e else None, "<=1 px"))
    checks.append(check("75 %% of sqrt(w2+h2)/sqrt2 exceeds the half-diagonal: iris ends full", mad(F1[-1], B) < 1,
                        [0.75 * ref, DIAG / 2], "r_end > half-diagonal"))
    # diamond polygon(50% -20%, 120% 50%, 50% 120%, -20% 50%)
    dplan = [ease(i / (n - 1)) for i in range(n)]
    xx, yy = grid()

    def dmask(p):
        return ((abs(xx - W / 2) / (0.7 * W) + abs(yy - H / 2) / (0.7 * H)) <= p).astype(float)
    p2, F2 = render(wd, prefix + "_diamond", [blend(A, B, dmask(p)) for p in dplan] + [B])
    dcov = [frac(f, B, 2) for f in F2[:-1]]
    dexp = [float(np.mean(dmask(p))) for p in dplan]
    checks.append(check("diamond iris coverage matches the polygon area", max(abs(a - b) for a, b in zip(dcov, dexp)) < 0.02,
                        max(abs(a - b) for a, b in zip(dcov, dexp)), "<0.02"))
    checks.append(check("diamond polygon leaves the corners until the clip is cleared", dcov[-1] < 0.9 and mad(F2[-1], B) < 1,
                        dcov[-1], "<0.9 then cleared"))
    # diagonal split: outgoing halves slide apart along the diagonal
    sp = []
    upper = (yy * W < (W - xx) * H)

    for p in dplan:
        d = ease(p) * W
        f = B.copy()
        sa = shift(A, -d, -d * H / W, fill=(0, 0, 0))
        sb = shift(A, d, d * H / W, fill=(0, 0, 0))
        mu = shift(upper[..., None].astype(float), -d, -d * H / W)[..., 0] > 0.5
        ml = shift((~upper)[..., None].astype(float), d, d * H / W)[..., 0] > 0.5
        f[mu] = sa[mu]
        f[ml] = sb[ml]
        sp.append(f)
    p3, F3 = render(wd, prefix + "_diagsplit", sp)
    mid = F3[n // 2]
    gap = frac(mid, B, 2, (np.abs(yy * W - (W - xx) * H) < W * 2)) > 0.5
    checks.append(check("diagonal split opens a gap along the diagonal showing B", gap and mad(F3[0], A) < 1 and mad(F3[-1], B) < 1,
                        gap, True))
    hard = [A] + [B] * (n - 1)
    he = _radius_errs(hard, plan, W / 2, H / 2, B, A)
    checks.append(check("negative control: a hard cut does not follow the iris radius", not he or max(he) > 3,
                        max(he) if he else None, ">3"))
    return checks, [p1, p2, p3]


@card("TRANS-382")
def iris_diamond_split(task, wd):
    """Circle iris circle(0% -> 75% at 50% 50%) 0.5 s power2.out, diamond iris polygon and a diagonal split."""
    return _iris_family(wd, "iris382", 500, lambda t: pow_out(t, 2), "power2.out")


@card("TRANS-409")
def radial_family(task, wd):
    """Radial family (circle iris, diamond iris, diagonal split) as one GSAP-style timeline: 0.8 s power3.inOut.
    Frame-math port of the GSAP family."""
    return _iris_family(wd, "radial409", 800, lambda t: pow_inout(t, 3), "power3.inOut")


@card("TRANS-386")
def match_circle_cut(task, wd):
    """Match cut through a round element: 0-0.6 s hold, 0.6-1.2 s scale into shot A's circle with a circular mask
    and light blur, cut at the peak, 1.2-2.0 s ease out of the matching circle of shot B."""
    np = _np()
    fps = 15
    ca, ra = (40, 36), 8.0
    cb, rb = (88, 30), 12.0
    A = blend(scene_a(), solid((250, 250, 250)), circle_mask(*ca, ra))
    B = blend(scene_b(), solid((250, 250, 250)), circle_mask(*cb, rb))
    S = 6.0
    frames, rad = [], []
    for i in range(int(2.0 * fps)):
        t = i / fps
        if t < 0.6:
            frames.append(A)
            rad.append(ra)
        elif t < 1.2:
            s = 1 + pow_in((i - 0.6 * fps) / (0.6 * fps - 1), 3) * (S - 1)
            f = scale_about(A, s, *ca)
            f = blur(f, 1.0) if s > 2 else f
            frames.append(f)
            rad.append(ra * s)
        else:
            s0 = S * ra / rb
            s = s0 + pow_out((t - 1.2) / 0.8, 3) * (1 - s0)
            frames.append(scale_about(B, s, *cb))
            rad.append(rb * s)
    path, F = render(wd, "matchcircle", frames, fps)
    cut = int(1.2 * fps)

    def white_r(f, c):
        return radius_along(f, c[0], c[1], (250, 250, 250), 40)
    before = white_r(F[cut - 1], ca)
    after = white_r(F[cut], cb)
    hold_ok = all(mad(F[i], A) < 1 for i in range(int(0.6 * fps)))
    end_ok = mad(F[-1], B) < 12
    nb, na = white_r(A, ca), white_r(B, cb)
    return [check("hold 0-0.6 s on shot A", hold_ok, hold_ok, True),
            check("circle size matches across the cut (+-25 %)", before > 0 and abs(after - before) / before < 0.25, [before, after], "equal"),
            check("circle is huge at the cut (scaled into)", before > 3 * ra, before, ">3 x r_A"),
            check("settles on shot B by 2.0 s", end_ok, mad(F[-1], B), "<12"),
            check("negative control: a straight cut mismatches the circle size", abs(na - nb) / max(nb, 1) > 0.25,
                  [nb, na], "mismatch > 25 %")], [path]


@card("TRANS-446")
def beat_reskin_radiate(task, wd):
    """Theme reskin radiates from a centre point on each beat (120 BPM): a circle of the next theme grows in 280 ms."""
    np = _np()
    themes = [scene_a(), scene_b(), scene_c(), 255 - scene_a()]
    beat = 15
    grow = ms2f(280)
    far = DIAG / 2 + 1
    frames, plan = [], []
    for i in range(beat * 4):
        k = min(3, i // beat)
        t = (i - k * beat + 1) / grow
        cur, nxt = themes[k], themes[min(3, k + 1)]
        base = themes[k] if k == 0 or t >= 0 else themes[k]
        prev = themes[k - 1] if k > 0 else themes[0]
        if k > 0 and t < 1:
            f = blend(prev, cur, circle_mask(W / 2, H / 2, pow_out(t, 2) * far))
            plan.append((k, pow_out(t, 2) * far))
        else:
            f = cur
            plan.append((k, None))
        frames.append(f)
    path, F = render(wd, "reskin", frames)
    ok = True
    for b in (1, 2, 3):
        i = b * beat + grow // 2
        r = plan[i][1]
        mr = radius_ab(F[i], W / 2, H / 2, themes[b], themes[b - 1])
        ok &= abs(mr - r) <= 1.5
        ok &= mad(F[b * beat + grow], themes[b]) < 1
    starts = [b * beat for b in (1, 2, 3) if mad(F[b * beat - 1], themes[b - 1]) < 0.5 and mad(F[b * beat], themes[b - 1]) > 0.5]
    neg = [themes[min(3, i // beat)] for i in range(len(frames))]
    nm = radius_ab(neg[beat + grow // 2], W / 2, H / 2, themes[1], themes[0])
    return [check("each beat's theme radiates from the centre within 280 ms", ok, ok, True),
            check("one reskin per beat (starts on beat frames)", starts == [15, 30, 45], starts, [15, 30, 45]),
            check("negative control: a hard reskin has no growing circle", math.isnan(nm) or abs(nm - plan[beat + grow // 2][1]) > 3,
                  nm, "!= planned")], [path]


@card("TRANS-36")
def clip_reveal_bezier(task, wd):
    """Image revealed by an animating clip-path inset() with cubic-bezier(0.16,1,0.3,1) over 0.8 s (not a fade)."""
    np = _np()
    A, B = solid((15, 15, 20)), scene_b()
    ez = bezier(0.16, 1, 0.3, 1)
    n = int(0.8 * FPS) + 1
    _, yy = grid()
    plan = [ez(i / (n - 1)) for i in range(n)]
    frames = [blend(A, B, (yy >= H * (1 - p)).astype(float)) for p in plan]
    path, F = render(wd, "clipreveal", frames)
    meas = [float(np.mean(near(f, B, 3)[:, W // 2])) for f in F]
    err = max(abs(m - round(p * H) / H) for m, p in zip(meas, plan))
    early = plan[n // 4]
    fade = [blend(A, B, p) for p in plan]
    fm = [float(np.mean(near(f, B, 3)[:, W // 2])) for f in fade]
    ferr = max(abs(m - p) for m, p in zip(fm, plan))
    return [check("inset reveal follows cubic-bezier(0.16,1,0.3,1)", err <= 1.0 / H + 1e-6, err, "<=1 row"),
            check("front-loaded curve: >75 % revealed at 25 % time", early > 0.75, early, ">0.75"),
            check("fully revealed at 0.8 s", meas[-1] == 1.0, meas[-1], 1.0),
            check("negative control: a fade reveals no fully-B rows mid-way", ferr > 0.3, ferr, ">0.3")], [path]


# ================================================================================ batch 3: organic masks
def mix_weight(f, A, B, thr=60.0):
    """Per-pixel mix weight w with f = A + w (B - A), on pixels where A and B differ enough."""
    np = _np()
    d = B - A
    nn = np.sum(d * d, -1)
    ok = nn > thr * thr
    w = np.sum((f - A) * d, -1) / np.maximum(nn, 1)
    return np.clip(w, 0, 1), ok


def _noise_dissolve(wd, name, seed, n=20):
    np = _np()
    A, B = scene_a(), scene_b()
    c = _gnoise(2.5, seed)
    plan = [i / (n - 1) for i in range(n)]
    frames = [blend(A, B, np.clip(c + p * 2.0, 0, 1)) for p in plan]
    path, F = render(wd, name, frames)
    return path, F, plan, c, A, B


@card("TRANS-95")
def noise_threshold_mix(task, wd):
    """Mix two scene textures with noise = clamp(cnoise(uv*2.5) + progress*2, 0, 1); colour = mix(A, B, noise)."""
    np = _np()
    path, F, plan, c, A, B = _noise_dissolve(wd, "noise95", 95)
    i = 5
    w, ok = mix_weight(F[i], A, B)
    want = np.clip(c + plan[i] * 2, 0, 1)
    err = float(np.max(np.abs(w - want)[ok]))
    spread = float(np.std(w[ok]))
    cf = blend(A, B, plan[i])
    cw, _ = mix_weight(cf, A, B)
    cerr = float(np.max(np.abs(cw - want)[ok]))
    return [check("per-pixel weight = clamp(noise*2.5 + 2p)", err < 0.03, err, "<0.03"),
            check("weights vary across the frame (organic, not uniform)", spread > 0.2, spread, ">0.2"),
            check("progress 1 shows B everywhere", mad(F[-1], B) < 1, mad(F[-1], B), 0),
            check("negative control: a plain crossfade misses the noise weights", cerr > 0.3, cerr, ">0.3")], [path]


@card("TRANS-99")
def noise_front_reveal(task, wd):
    """Reveal B through an organic noise front n = clamp(cnoise(uv*2.5) + progress*2, 0, 1): high-noise pixels go
    first, the revealed area only grows."""
    np = _np()
    path, F, plan, c, A, B = _noise_dissolve(wd, "noise99", 99, n=24)
    full = [frac(f, B, 3) for f in F]
    mono = all(b >= a - 1e-6 for a, b in zip(full, full[1:]))
    first = np.full((H, W), len(F))
    for k in range(len(F) - 1, -1, -1):
        first[near(F[k], B, 3)] = k
    sel = np.abs(B - A).sum(-1) > 150
    x, y = c[sel].ravel(), first[sel].ravel().astype(float)
    corr = float(np.corrcoef(x, y)[0, 1])
    m = near(F[8], B, 3)
    perim = int(np.sum(m[:, 1:] != m[:, :-1]) + np.sum(m[1:] != m[:-1]))
    xx, _ = grid()
    wipe = xx < frac(F[8], B, 3) * W
    wper = int(np.sum(wipe[:, 1:] != wipe[:, :-1]) + np.sum(wipe[1:] != wipe[:-1]))
    wf = [blend(A, B, (xx < (j / (len(F) - 1)) * W).astype(float)) for j in range(len(F))]
    nfirst = np.full((H, W), len(F))
    for k in range(len(wf) - 1, -1, -1):
        nfirst[near(wf[k], B, 3)] = k
    ncorr = float(np.corrcoef(c[sel].ravel(), nfirst[sel].ravel().astype(float))[0, 1])
    return [check("revealed area only grows", mono, [full[0], full[-1]], "monotonic"),
            check("high-noise pixels reveal first (corr(noise, reveal frame) < -0.8)", corr < -0.8, corr, "<-0.8"),
            check("front is organic (perimeter > 1.5x a straight wipe of equal area)", perim > 1.5 * wper, [perim, wper], ">1.5x"),
            check("negative control: a straight wipe's reveal order ignores the noise", ncorr > -0.8, ncorr, ">-0.8")], [path]


def _radius_dir(f, cx, cy, inside, outside, a):
    np = _np()
    ins = np.broadcast_to(np.asarray(inside, float), f.shape)
    outs = np.broadcast_to(np.asarray(outside, float), f.shape)
    r = 0.0
    while True:
        x, y = int(round(cx + r * math.cos(a))), int(round(cy + r * math.sin(a)))
        if not (0 <= x < W and 0 <= y < H):
            return None
        if np.sum(np.abs(f[y, x] - outs[y, x])) < np.sum(np.abs(f[y, x] - ins[y, x])):
            return r
        r += 0.5


@card("TRANS-41")
def burn_hole(task, wd):
    """A noise-edged burning hole eats the frame: edge radius = R(t) + layered sin-hash noise on the angle
    (amps 50/20/8 px in 1920 space, scaled x0.1 here); the next scene fades in from black at ~90 %."""
    np = _np()
    A, B = scene_a(), scene_b()
    xx, yy = grid()
    ang = np.arctan2(yy - H / 2, xx - W / 2)
    d = np.hypot(xx - W / 2, yy - H / 2)

    def edge(a):
        return 5.0 * np.sin(3 * a + 1.3) + 2.0 * np.sin(7 * a + 0.4) + 0.8 * np.sin(17 * a + 2.1)
    n = 30
    frames, plan = [], []
    for i in range(n):
        p = i / (n - 1)
        R = pow_out(p, 1) * (DIAG / 2 + 10)
        hole = (d < R + edge(ang)) & (R > 0)
        content = solid((0, 0, 0)) if p < 0.9 else blend(solid((0, 0, 0)), B, (p - 0.9) / 0.1)
        frames.append(np.where(hole[..., None], content, A))
        plan.append(R)
    path, F = render(wd, "burnhole", frames)
    i = 9
    errs = []
    for a in np.linspace(-math.pi + 0.05, math.pi - 0.05, 24):
        r = _radius_dir(F[i], W / 2, H / 2, (0, 0, 0), A, a)
        if r is not None:
            errs.append(abs(r - (plan[i] + edge(a))))
    black_until = all(frac(F[k], (0, 0, 0), 3, circle_mask(W / 2, H / 2, max(0.0, plan[k] - 9)) > 0.5) > 0.99
                      for k in range(3, int(0.9 * (n - 1))))
    radii = [_radius_dir(F[i], W / 2, H / 2, (0, 0, 0), A, a) for a in np.linspace(-3, 3, 24)]
    radii = [r for r in radii if r is not None]
    circ = blend(A, solid((0, 0, 0)), circle_mask(W / 2, H / 2, plan[i]))
    cr = [_radius_dir(circ, W / 2, H / 2, (0, 0, 0), A, a) for a in np.linspace(-3, 3, 24)]
    cr = [r for r in cr if r is not None]
    return [check("hole edge = R(t) + sin-hash noise per angle (+-1 px)", errs and max(errs) <= 1.0, max(errs) if errs else None, "<=1"),
            check("edge is ragged (radius spread > 4 px)", max(radii) - min(radii) > 4, max(radii) - min(radii), ">4"),
            check("hole stays black until ~90 %", black_until, black_until, True),
            check("next scene faded in at the end", mad(F[-1], B) < 1, mad(F[-1], B), 0),
            check("negative control: a plain circle has no ragged edge", max(cr) - min(cr) < 1.5, max(cr) - min(cr), "<1.5")], [path]


@card("TRANS-389")
def ink_spread(task, wd):
    """Ink drop spreads into the next shot: 0-0.4 s drop, 0.4-1.3 s spread, 1.3-1.8 s fill; procedural noise blob
    as a luma matte with contrast pushed so the matte reaches full."""
    np = _np()
    fps = 20
    A, B = scene_a(), scene_b()
    nz = _gnoise(3.0, 389, octaves=3)
    xx, yy = grid()
    d = np.hypot(xx - 50, yy - 30) / DIAG
    frames, mats = [], []
    for i in range(int(1.8 * fps) + 1):
        t = i / fps
        if t < 0.4:
            g = -1.0
        elif t < 1.3:
            g = -0.05 + 0.95 * smooth((t - 0.4) / 0.9)
        else:
            g = 0.9 + 1.5 * (t - 1.3) / 0.5
        dropm = circle_mask(50, 30, 4.0 * min(1.0, t / 0.4), 1.0) if t > 0 else 0 * d
        matte = np.maximum(np.clip((g - d * 1.6 + 0.25 * nz) * 4.0, 0, 1), dropm)
        frames.append(blend(A, B, matte))
        mats.append(matte)
    path, F = render(wd, "ink", frames, fps)
    cov = [frac(f, B, 6) for f in F]
    drop = max(cov[:int(0.4 * fps)])
    mid = cov[int(1.3 * fps)]
    ang = [_radius_dir(F[int(0.9 * fps)], 50, 30, B, A, a) for a in np.linspace(-3, 3, 24)]
    ang = [r for r in ang if r is not None]
    fade = [blend(A, B, i / (len(F) - 1)) for i in range(len(F))]
    fcov = [frac(f, B, 6) for f in fade]
    return [check("drop phase stays small (< 5 % covered by 0.4 s)", drop < 0.05 and cov[int(0.3 * fps)] > 0, drop, "<0.05"),
            check("spread phase covers most of the frame by 1.3 s", mid > 0.6, mid, ">0.6"),
            check("matte reaches full: frame is B at 1.8 s", mad(F[-1], B) < 1, mad(F[-1], B), 0),
            check("ink edge is irregular (radius spread > 4 px)", ang and max(ang) - min(ang) > 4, max(ang) - min(ang) if ang else None, ">4"),
            check("negative control: a crossfade has no fully-inked region mid-way", fcov[int(0.9 * fps)] < 0.01,
                  fcov[int(0.9 * fps)], "<0.01")], [path]


@card("TRANS-X07")
def living_blob_flood(task, wd):
    """A new background floods from the click point as a wobbling blob: base disc + 4 radial blobs on Lissajous
    paths, union of wobbling circles, soft feather; R = smooth(p) * (corner distance + 504 px) (scaled)."""
    np = _np()
    k = W / 1920
    A, col = scene_a(), (30, 200, 150)
    cx, cy = 90, 50
    xx, yy = grid()
    corner = max(math.hypot(cx - x, cy - y) for x in (0, W) for y in (0, H))
    feather = 420 * k * 0.25
    n = 24
    frames, Rs = [], []
    for i in range(n):
        p = i / (n - 1)
        R = smooth(p) * (corner + 504 * k * 2)
        field = np.hypot(xx - cx, yy - cy) - R
        for j in range(4):
            ox = 140 * k * math.sin(1.7 * p * 6 + j * 1.3)
            oy = 90 * k * math.cos(1.1 * p * 6 + j * 2.1)
            rj = R * (0.55 + 0.1 * j)
            ang = 2 * math.pi * j / 4
            bx, by = cx + 0.45 * R * math.cos(ang) + ox, cy + 0.45 * R * math.sin(ang) + oy
            field = np.minimum(field, np.hypot(xx - bx, yy - by) - rj)
        m = np.clip(0.5 - field / feather, 0, 1) if R > 0 else 0 * field
        frames.append(blend(A, solid(col), m))
        Rs.append(R)
    path, F = render(wd, "blob", frames)
    i = 7
    rr = [_radius_dir(F[i], cx, cy, col, A, a) for a in np.linspace(-3.1, 3.1, 32)]
    rr = [r for r in rr if r is not None]
    m = near(F[2], col, 40)
    ys, xs = np.nonzero(m)
    origin = len(xs) > 0 and abs(xs.mean() - cx) < 12 and abs(ys.mean() - cy) < 12
    row = F[i][cy, :, 1]
    partial = int(np.sum((row > A[cy, :, 1] + 15) & (row < col[1] - 15)))
    circ = blend(A, solid(col), circle_mask(cx, cy, Rs[i]))
    cr = [_radius_dir(circ, cx, cy, col, A, a) for a in np.linspace(-3.1, 3.1, 32)]
    cr = [r for r in cr if r is not None]
    return [check("blob boundary wobbles (radius spread > 3 px)", rr and max(rr) - min(rr) > 3, max(rr) - min(rr) if rr else None, ">3"),
            check("flood starts at the click point", origin, (float(xs.mean()), float(ys.mean())) if len(xs) else None, (cx, cy)),
            check("feathered edge (partial pixels on a row)", partial >= 2, partial, ">=2"),
            check("covers the whole frame at the end", frac(F[-1], col, 6) > 0.99, frac(F[-1], col, 6), ">0.99"),
            check("negative control: a hard circle does not wobble", max(cr) - min(cr) < 1.5, max(cr) - min(cr), "<1.5")], [path]


@card("TRANS-X09")
def record_roll_close(task, wd):
    """A vinyl record rolls without slipping (rotation = distance / radius x 57.3 deg) while the clip circle
    closes from 1150 px (scaled) to the record radius x 0.96."""
    np = _np()
    r = 10.0
    k = W / 1920
    n = 30
    xx, yy = grid()
    frames, plan = [], []
    for i in range(n):
        p = i / (n - 1)
        x = 20 + 70 * pow_inout(p, 2)
        dist = x - 20
        rot = dist / r  # radians; degrees = dist / r * 57.3
        f = solid((240, 240, 240))
        disc = np.hypot(xx - x, yy - 36) <= r
        f[disc] = (25, 25, 25)
        mx, my = x + 0.7 * r * math.cos(rot), 36 + 0.7 * r * math.sin(rot)
        f[np.hypot(xx - mx, yy - my) <= 1.6] = (255, 40, 40)
        clip = (1150 * k) + (r * 0.96 - 1150 * k) * pow_inout(p, 2)
        f = blend(solid((0, 0, 0)), f, circle_mask(x, 36, clip))
        frames.append(f)
        plan.append((x, rot, clip))
    path, F = render(wd, "record", frames)
    errs = []
    for i in (5, 12, 20, 28):
        x, rot, _ = plan[i]
        m = near(F[i], (255, 40, 40), 60)
        ys, xs = np.nonzero(m)
        a = math.atan2(ys.mean() - 36, xs.mean() - x)
        e = (a - rot + math.pi) % (2 * math.pi) - math.pi
        errs.append(abs(e))
    x, _, clip = plan[-1]
    outside = frac(F[-1], (0, 0, 0), 3, circle_mask(x, 36, r * 0.96 + 1.5) < 0.5)
    inside = frac(F[-1], (0, 0, 0), 3, circle_mask(x, 36, r * 0.96 - 1.5) > 0.5)
    deg = (plan[-1][0] - 20) / r * 57.3
    # negative: a record that slides without rolling keeps its marker angle
    nerr = abs(((0.0 - plan[20][1]) + math.pi) % (2 * math.pi) - math.pi)
    return [check("marker angle = distance / radius (rolling, +-0.3 rad)", max(errs) < 0.3, max(errs), "<0.3"),
            check("rotation in degrees = d / r x 57.3", abs(deg - (70 / r) * 57.3) < 1e-6, deg, 70 / r * 57.3),
            check("clip closes to r x 0.96 (outside black, inside not)", outside > 0.99 and inside < 0.2, [outside, inside], [">0.99", "<0.2"]),
            check("negative control: a sliding record's marker misses the rolling angle", nerr > 0.3, nerr, ">0.3")], [path]


@card("TRANS-X11")
def dive_into_light(task, wd):
    """Dive into the scene's point of light: over +-0.42 s scene A zooms K^p (K = 9) about the focus point while
    it drifts to centre; the next scene is born inside a mask growing 170 -> 1450 px (scaled)."""
    np = _np()
    k = W / 1920
    A = blend(scene_a() * 0.5, solid((255, 250, 220)), circle_mask(96, 24, 3))
    B = scene_b()
    n = int(0.84 * FPS) + 1
    frames, plan = [], []
    for i in range(n):
        p = i / (n - 1)
        s = 9 ** p
        fxp, fyp = 96 + (W / 2 - 96) * smooth(p), 24 + (H / 2 - 24) * smooth(p)
        xx, yy = grid()
        # screen point (fxp,fyp) shows the light; zoom by s about it
        src, _ = sample(A, 96 + (xx - fxp) / s, 24 + (yy - fyp) / s, (0, 0, 0))
        q = max(0.0, (p - 0.5) * 2)
        mr = (170 + (1450 - 170) * smooth(q)) * k if p > 0.5 else 0.0
        ghost = 0.35 * (1 - q)
        inner = blend(B, scale_about(src, 1.08, fxp, fyp), ghost)
        f = blend(src, inner, circle_mask(fxp, fyp, mr)) if mr > 0 else src
        frames.append(f)
        plan.append((s, fxp, fyp, mr))
    path, F = render(wd, "dive", frames)
    errs = []
    for i in (2, 4, 6, 8):
        s, fxp, fyp, _ = plan[i]
        m = near(F[i], (255, 250, 220), 30)
        ys, xs = np.nonzero(m)
        rad = math.sqrt(len(xs) / math.pi) if len(xs) else 0
        errs.append(abs(rad / (3 * s) - 1))
    s, fxp, fyp, mr = plan[n // 2 + 3]
    mm = radius_ab(F[n // 2 + 3], fxp, fyp, B, (255, 250, 220), r0=0)
    drift = abs(plan[-1][1] - W / 2) < 1e-6
    neg = [A] * (n // 2) + [B] * (n - n // 2)
    nerrs = [abs(math.sqrt(near(neg[i], (255, 250, 220), 30).sum() / math.pi) / (3 * plan[i][0]) - 1) for i in (6, 8)]
    return [check("light grows as 9^p about the focus point (+-35 %)", max(errs) < 0.35, max(errs), "<0.35"),
            check("focus point drifts to the centre", drift, plan[-1][1:3], (W / 2, H / 2)),
            check("next scene is born inside the light (mask from 170 px x scale)", plan[n // 2 + 1][3] >= 170 * k - 1e-6 and mr > 170 * k,
                  [plan[n // 2 + 1][3], mr], ">=170k"),
            check("ends on the next scene", mad(F[-1], B) < 2, mad(F[-1], B), "<2"),
            check("negative control: a plain cut fails the 9^p growth", max(nerrs) > 0.35, nerrs, ">0.35")], [path]


# ================================================================================ batch 4: whips, slides, blur
K = W / 1920.0   # 1920-px design units -> frame pixels
SIGMAS = [0, 0.4, 0.8, 1.2, 1.6, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0]


def moved(img, off, sigma, axis=1, fill=(12, 12, 16)):
    """img translated by `off` px along axis and blurred along the same axis by sigma (motion blur)."""
    f = shift(img, off if axis == 1 else 0, off if axis == 0 else 0, fill=fill)
    return gblur_axis(f, sigma, axis) if sigma > 0 else f


def fit_move(f, src, axis=1, rng=None, sigmas=SIGMAS, fill=(12, 12, 16), centre=0):
    """Jointly fit the translation and the directional blur sigma that turn src into f."""
    best = (1e9, 0, 0)
    rng = rng or range(-W, W + 1)
    for d in rng:
        base = shift(src, d if axis == 1 else 0, d if axis == 0 else 0, fill=fill)
        for sg in sigmas:
            g = gblur_axis(base, sg, axis) if sg > 0 else base
            e = mad(f, g)
            if e < best[0]:
                best = (e, d, sg)
    return best[1], best[2], best[0]


def dir_ratio(f, ref, sigma, axis=1):
    """mad(f, blur_along(ref)) / mad(f, blur_across(ref)): << 1 when f is ref blurred along `axis`."""
    a = mad(f, gblur_axis(ref, sigma, axis))
    b = mad(f, gblur_axis(ref, sigma, 1 - axis))
    return a / max(b, 1e-6)


def aniso(f, ref):
    """(x-sharpness / y-sharpness) of f relative to ref: < 1 means horizontal blur, > 1 vertical blur."""
    return (sharp_x(f) / max(sharp_y(f), 1e-6)) / (sharp_x(ref) / max(sharp_y(ref), 1e-6))


def _vel_profile(ease, n):
    pos = [ease(i / (n - 1)) for i in range(n)]
    vel = [abs(pos[min(n - 1, i + 1)] - pos[max(0, i - 1)]) for i in range(n)]
    m = max(vel) or 1
    return pos, [v / m for v in vel]


def _tween(img, n, start, end, ease, blur_max, axis=1, fill=(12, 12, 16), blur_curve=None):
    pos, vel = _vel_profile(ease, n)
    frames, plan = [], []
    for i in range(n):
        off = start + (end - start) * pos[i]
        sg = blur_max * (blur_curve(i / (n - 1)) if blur_curve else vel[i])
        frames.append(moved(img, off, sg, axis, fill))
        plan.append((off, sg))
    return frames, plan


def _fit_checks(F, plan, src, idx, axis=1, label="", fill=(12, 12, 16), tol_d=1.5, tol_s=0.6):
    errs_d, errs_s = [], []
    for i in idx:
        off, sg = plan[i]
        d, s_, _ = fit_move(F[i], src, axis, range(int(off) - 3, int(off) + 4), fill=fill)
        errs_d.append(abs(d - off))
        errs_s.append(abs(s_ - sg))
    return [check("%s offset matches the tween (+-%.1f px)" % (label, tol_d), max(errs_d) <= tol_d, max(errs_d), "<=%.1f" % tol_d),
            check("%s directional blur matches velocity (+-%.1f px)" % (label, tol_s), max(errs_s) <= tol_s, max(errs_s), "<=%.1f" % tol_s)]


@card("TRANS-32")
def three_camera_recipes(task, wd):
    """Whip (exit x -400 blur 24 0.3 s power3.in -> entry 400->0 0.3 s power3.out), blur-through (exit blur 20 0.3 s
    -> entry 20->0 0.25 s power3.out) and zoom-through (exit scale 1->1.2 blur 20 0.2 s -> entry 0.75->1 blur 20->0
    0.5 s expo.out) as paired exit/entry tweens. 1920-px values scaled to the frame."""
    np = _np()
    A, B = scene_a(), scene_b()
    n3 = ms2f(300) + 1
    ex, pe = _tween(A, n3, 0, -400 * K, lambda t: pow_in(t, 3), 24 * K, blur_curve=lambda t: pow_in(t, 3))
    en, pn = _tween(B, n3, 400 * K, 0, lambda t: pow_out(t, 3), 24 * K, blur_curve=lambda t: 1 - pow_out(t, 3))
    p1, F1 = render(wd, "whip", ex + en)
    c = _fit_checks(F1, pe + pn, None, [], label="") if False else []
    errs = []
    for i in (n3 - 2, n3 - 1):
        d, sg, _ = fit_move(F1[i], A, 1, range(int(pe[i][0]) - 3, int(pe[i][0]) + 4))
        errs.append((abs(d - pe[i][0]), abs(sg - pe[i][1])))
    for j in (0, 2):
        d, sg, _ = fit_move(F1[n3 + j], B, 1, range(int(pn[j][0]) - 3, int(pn[j][0]) + 4))
        errs.append((abs(d - pn[j][0]), abs(sg - pn[j][1])))
    c.append(check("whip: exit to -400 and entry from +400 with blur (offset/blur errors)",
                   max(e[0] for e in errs) <= 1.5 and max(e[1] for e in errs) <= 0.6, errs, "<=1.5 px, <=0.6 sigma"))
    c.append(check("whip: entry lands sharp on B", mad(F1[-1], B) < 1, mad(F1[-1], B), 0))
    # blur-through
    nb_out, nb_in = ms2f(300) + 1, ms2f(250) + 1
    bt = [blur(A, 20 * K * pow_in(i / (nb_out - 1), 3)) for i in range(nb_out)] + \
         [blur(B, 20 * K * (1 - pow_out(i / (nb_in - 1), 3))) for i in range(nb_in)]
    p2, F2 = render(wd, "blurthrough", bt)
    peak = F2[nb_out - 1]
    sg_est = min(SIGMAS, key=lambda sg: mad(peak, blur(A, sg)))
    c.append(check("blur-through: peak blur 20 px (scaled) at the swap", abs(sg_est - 20 * K) <= 0.4, sg_est, round(20 * K, 2)))
    c.append(check("blur-through: isotropic (no direction)", abs(aniso(peak, A) - 1) < 0.15, aniso(peak, A), "~1"))
    # zoom-through
    nz_out, nz_in = ms2f(200) + 1, ms2f(500) + 1
    zt = [blur(scale_about(A, 1 + 0.2 * pow_in(i / (nz_out - 1), 3)), 20 * K * pow_in(i / (nz_out - 1), 3)) for i in range(nz_out)]
    zplan = [0.75 + 0.25 * expo_out(i / (nz_in - 1)) for i in range(nz_in)]
    zt += [blur(scale_about(B, s_, fill=(12, 12, 16)), 20 * K * (1 - expo_out(i / (nz_in - 1)))) for i, s_ in enumerate(zplan)]
    p3, F3 = render(wd, "zoomthrough", zt)
    first_in = F3[nz_out]
    border = frac(first_in, (12, 12, 16), 3, np.ones((H, W)) * 0 + (grid()[0] < 0.1 * W))
    c.append(check("zoom-through: entry starts at x0.75 (empty border visible)", border > 0.95, border, ">0.95"))
    c.append(check("zoom-through: lands on B at x1", mad(F3[-1], B) < 1, mad(F3[-1], B), 0))
    hard = [A] * n3 + [B] * n3
    hd, hs, _ = fit_move(hard[n3 - 1], A, 1, range(int(pe[n3 - 1][0]) - 3, int(pe[n3 - 1][0]) + 4))
    c.append(check("negative control: a hard cut has no exit offset", abs(hd - pe[n3 - 1][0]) > 1.5, hd, pe[n3 - 1][0]))
    return c, [p1, p2, p3]


def _push_checks(F, plan, A, B, n, axis=1, label="push"):
    i = max(range(n), key=lambda j: plan[j][1])
    o, sg = plan[i]
    ref = _compose_push(A, B, o, axis)
    est = min(SIGMAS, key=lambda s_: mad(F[i], gblur_axis(ref, s_, axis)))
    an = dir_ratio(F[i], ref, sg, axis)
    end_ok = mad(F[-1], B) < 1 and mad(F[0], A) < 1
    han = dir_ratio(ref, ref, sg, axis)
    return [check("%s: peak directional blur sigma matches the plan" % label, abs(est - sg) <= 0.45, est, round(sg, 2)),
            check("%s: blur is directional (%s): along-axis blur explains the frame 3x better" % (label, "x" if axis == 1 else "y"),
                  an < 0.33, an, "<0.33"),
            check("%s: starts on A, lands on B" % label, end_ok, end_ok, True),
            check("negative control: the unblurred frame is not explained by a directional blur", han > 0.33, han, ">0.33")]


def _compose_push(A, B, o, axis=1):
    a = shift(A, -o if axis == 1 else 0, -o if axis == 0 else 0, fill=(0, 0, 0))
    b = shift(B, ((W if axis == 1 else H) - o) if axis == 1 else 0, ((H) - o) if axis == 0 else 0, fill=(0, 0, 0))
    xx, yy = grid()
    coord = xx if axis == 1 else yy
    m = coord >= (W if axis == 1 else H) - o
    out = a.copy()
    out[m] = b[m]
    return out


def _push(wd, name, dur_ms, blur_max, ease, axis=1, fps=FPS, dist=None):
    dist = dist if dist is not None else (W if axis == 1 else H)
    n = ms2f(dur_ms, fps) + 1
    pos, vel = _vel_profile(ease, n)
    A, B = scene_a(), scene_b()
    frames, plan = [], []
    for i in range(n):
        o = dist * pos[i]
        sg = blur_max * vel[i]
        frames.append(gblur_axis(_compose_push(A, B, int(round(o)), axis), sg, axis))
        plan.append((int(round(o)), sg))
    path, F = render(wd, name, frames, fps)
    return path, F, plan, A, B, n


@card("TRANS-324")
def motion_blur_slide(task, wd):
    """Fast horizontal motion-blur slide between samples (~300 ms, power3.inOut, blur 24 px peak, scaled)."""
    path, F, plan, A, B, n = _push(wd, "mbslide", 300, 24 * K * 2, lambda t: pow_inout(t, 3))
    return _push_checks(F, plan, A, B, n), [path]


@card("TRANS-374")
def blur_slide_300(task, wd):
    """Horizontal blur slide in 300 ms (power2.inOut, blur 18 px peak, scaled x2 for the small frame)."""
    path, F, plan, A, B, n = _push(wd, "blurslide", 300, 18 * K * 2, lambda t: pow_inout(t, 2))
    return _push_checks(F, plan, A, B, n), [path]


@card("TRANS-350")
def group_whip_expo(task, wd):
    """Translate the whole scene group ~60 % width in 200 ms expo.inOut with horizontal blur proportional to
    velocity (max 20 px), the next scene entering from the opposite side."""
    np = _np()
    n = ms2f(200, 60) + 1
    A, B = scene_a(), scene_b()
    pos, vel = _vel_profile(expo_inout, n)
    frames, plan = [], []
    half = n // 2
    for i in range(n):
        if i <= half:
            o = -0.6 * W * expo_inout(i / half / 2) * 2 if False else -0.6 * W * pos[i] * 2
            img = A
        else:
            o = 0.6 * W * (1 - pos[i]) * 2
            img = B
        o = max(-0.6 * W, min(0.6 * W, o))
        sg = 20 * K * 3 * vel[i]
        frames.append(moved(img, int(round(o)), sg, 1, fill=(12, 12, 16)))
        plan.append((int(round(o)), sg))
    path, F = render(wd, "groupwhip", frames, 60)
    c = _fit_checks(F, plan, A, [half - 1], label="exit", tol_s=0.7)
    c += _fit_checks(F, plan, B, [half + 2], label="entry", tol_s=0.7)
    c.append(check("exit travels ~60 % width", abs(plan[half][0] + 0.6 * W) <= 2, plan[half][0], -0.6 * W))
    c.append(check("entry comes from the opposite side (+x)", plan[half + 1][0] > 0, plan[half + 1][0], ">0"))
    c.append(check("lands on B", mad(F[-1], B) < 1, mad(F[-1], B), 0))
    hd, hs, _ = fit_move(A, A, 1, range(plan[half - 1][0] - 3, plan[half - 1][0] + 4))
    c.append(check("negative control: the unmoved scene does not fit the exit offset", abs(hd - plan[half - 1][0]) > 1.5, hd, plan[half - 1][0]))
    return c, [path]


def _entry_blur(wd, name, word, dur_ms, blur_px, start, ease, fps=60, prev=None):
    """Text card enters horizontally from `start` px with blur resolving to sharp; previous exits same direction."""
    base, _ = text_frame(word, size=24, bg=(12, 12, 16))
    n = ms2f(dur_ms, fps) + 1
    frames, plan = [], []
    if prev is not None:
        pv, _ = text_frame(prev, size=24, bg=(12, 12, 16))
        ex, pe = _tween(pv, n, 0, -start, lambda t: pow_in(t, 3), blur_px, blur_curve=lambda t: pow_in(t, 3))
        frames += ex
        plan += pe
    en, pn = _tween(base, n, start, 0, ease, blur_px, blur_curve=lambda t: 1 - ease(t))
    frames += en
    plan += pn
    path, F = render(wd, name, frames, fps)
    return path, F, plan, base, n


@card("TRANS-322")
def headline_blur_entry(task, wd):
    """Headline enters from off-frame horizontally in ~200 ms with directional blur 20 -> 0 px (expo-out); the
    previous card exits in the same direction."""
    path, F, plan, base, n = _entry_blur(wd, "headline", "NEWS", 200, 20 * K * 3, W, expo_out, prev="OLD")
    c = _fit_checks(F, plan, base, [n + 1, n + 3], label="entry", tol_s=0.7)
    exit_dir = plan[n - 1][0] < 0 and plan[n][0] > 0
    c.append(check("previous card exits the same direction (to -x, new from +x)", exit_dir, [plan[n - 1][0], plan[n][0]], "-x / +x"))
    c.append(check("resolves sharp at the end", mad(F[-1], base) < 1, mad(F[-1], base), 0))
    d0, _, _ = fit_move(base, base, 1, range(int(plan[n + 1][0]) - 3, int(plan[n + 1][0]) + 4))
    c.append(check("negative control: a static card does not fit the entry offset", abs(d0 - plan[n + 1][0]) > 1.5, d0, plan[n + 1][0]))
    return c, [path]


@card("TRANS-323")
def wordmark_velocity_blur(task, wd):
    """Wordmark slides sideways (250 ms) with directional blur proportional to velocity (30 px peak, scaled)."""
    np = _np()
    base, _ = text_frame("KOSIF", size=22, bg=(12, 12, 16))
    n = ms2f(250, 60) + 1
    frames, plan = _tween(base, n, -40, 40, sine_inout, 30 * K * 2)
    path, F = render(wd, "wordmark", frames, 60)
    est = []
    for i in range(1, n - 1):
        d, sg, _ = fit_move(F[i], base, 1, range(int(plan[i][0]) - 2, int(plan[i][0]) + 3))
        est.append(sg)
    vel = [plan[i][1] for i in range(1, n - 1)]
    corr = float(np.corrcoef(est, vel)[0, 1])
    flat = [moved(base, plan[i][0], 0) for i in range(n)]
    fest = []
    for i in range(1, n - 1):
        d, sg, _ = fit_move(flat[i], base, 1, range(int(plan[i][0]) - 2, int(plan[i][0]) + 3))
        fest.append(sg)
    return [check("measured blur tracks velocity (corr > 0.9)", corr > 0.9, corr, ">0.9"),
            check("peak blur ~30 px scaled", abs(max(est) - 30 * K * 2) <= 0.6, max(est), round(30 * K * 2, 2)),
            check("negative control: a slide without blur measures zero blur", max(fest) == 0, max(fest), 0)], [path]


@card("TRANS-357")
def card_rotate_off(task, wd):
    """Cards translate and rotate off-frame in 250 ms (rotateZ 10 deg) with directional blur up to 12 px."""
    np = _np()
    A = blend(solid((12, 12, 16)), scene_a(), ((np.abs(grid()[0] - W / 2) < 30) & (np.abs(grid()[1] - H / 2) < 20)).astype(float))
    n = ms2f(250, 60) + 1
    pos, vel = _vel_profile(lambda t: pow_in(t, 3), n)
    frames, plan = [], []
    for i in range(n):
        ang = 10 * pos[i]
        off = int(round(1.1 * W * pos[i]))
        f = shift(rotate(A, ang, fill=(12, 12, 16)), off, 0, fill=(12, 12, 16))
        frames.append(blur_x(f, 12 * K * 3 * vel[i]))
        plan.append((off, ang, 12 * K * 3 * vel[i]))
    path, F = render(wd, "cardoff", frames, 60)
    i = n // 2
    best = min(((d, a) for d in range(plan[i][0] - 2, plan[i][0] + 3) for a in (0, 5, plan[i][1], 15)),
               key=lambda da: mad(F[i], blur_x(shift(rotate(A, da[1], fill=(12, 12, 16)), da[0], 0, fill=(12, 12, 16)), plan[i][2])))
    off_end = frac(F[-1], (12, 12, 16), 3) > 0.99
    an = aniso(F[n - 2], A)
    return [check("card is rotated by its planned rotateZ mid-move", abs(best[1] - plan[i][1]) < 1e-6, best[1], plan[i][1]),
            check("card translation matches the plan", abs(best[0] - plan[i][0]) <= 1, best[0], plan[i][0]),
            check("card leaves the frame", off_end, off_end, True),
            check("blur up to 12 px (scaled) on the last frames", plan[-1][2] <= 12 * K * 3 + 1e-6 and max(p[2] for p in plan) > 0, max(p[2] for p in plan), "<= 12 px scaled"),
            check("negative control: unrotated card does not fit the mid-move frame",
                  mad(F[i], blur_x(shift(A, plan[i][0], 0, fill=(12, 12, 16)), plan[i][2])) > mad(F[i], blur_x(shift(rotate(A, plan[i][1], fill=(12, 12, 16)), plan[i][0], 0, fill=(12, 12, 16)), plan[i][2])) + 0.5,
                  True, True)], [path]


@card("TRANS-388")
def whip_hidden_cut(task, wd):
    """Whip pan with the cut hidden at maximum motion blur: 0-0.25 s accelerate, cut inside 0.25-0.45 s, settle to
    0.8 s; same direction (-x) on both sides."""
    np = _np()
    fps = 30
    A, B = scene_a(), scene_b()
    n = int(0.8 * fps)
    cut = next(i for i in range(n) if i / fps >= 0.35)
    frames, plan = [], []
    for i in range(n):
        t = i / fps
        if t < 0.35:
            p = pow_in(t / 0.35, 3)
            o, sg, img = -int(round(60 * p)), 6.0 * p, A
        else:
            p = pow_out((t - 0.35) / 0.45, 3)
            o, sg, img = int(round(60 * (1 - p))), 6.0 * (1 - p), B
        frames.append(moved(img, o, sg))
        plan.append((o, sg))
    path, F = render(wd, "whipcut", frames, fps)
    cuts = [i for i in range(n) if mad(F[i], moved(B, plan[i][0], plan[i][1])) < mad(F[i], moved(A, plan[i][0], plan[i][1]))][:1]
    blurs = [min(SIGMAS, key=lambda s_: mad(F[i], moved(A if i < cut else B, plan[i][0], s_))) for i in range(n)]
    peak = int(np.argmax(blurs))
    same_dir = (plan[cut - 1][0] - plan[cut - 2][0]) < 0 and (plan[cut + 1][0] - plan[cut][0]) < 0
    hard = [A] * cut + [B] * (n - cut)
    hb = [min(SIGMAS, key=lambda s_: mad(hard[i], moved(hard[i], 0, s_))) for i in (cut - 1, cut)]
    return [check("cut inside the 0.25-0.45 s window", cuts and 0.25 <= cuts[0] / fps <= 0.45, [c / fps for c in cuts], "0.25-0.45"),
            check("cut sits at the blur peak", abs(peak - cut) <= 1, peak, cut),
            check("motion continues in the same direction across the cut", same_dir, same_dir, True),
            check("settled on B by 0.8 s", mad(F[-1], B) < 2, mad(F[-1], B), "<2"),
            check("negative control: a plain cut has no blur at the cut", max(hb) == 0, hb, 0)], [path]


@card("TRANS-455")
def fast_whip_hold(task, wd):
    """Fast whip (180 ms) with 8 px directional blur and a 2-frame arrival hold."""
    np = _np()
    fps = 60
    A, B = scene_a(), scene_b()
    n = ms2f(180, fps) + 1
    pos, vel = _vel_profile(lambda t: pow_inout(t, 3), n)
    frames, plan = [], []
    for i in range(n):
        o = int(round(W * pos[i]))
        frames.append(gblur_axis(_compose_push(A, B, o), 8 * K * 4 * vel[i], 1))
        plan.append((o, 8 * K * 4 * vel[i]))
    drift = [shift(B, -k, 0, fill=(12, 12, 16)) for k in range(1, 5)]
    frames += [frames[-1]] * 2 + drift
    path, F = render(wd, "fastwhip", frames, fps)
    i = max(range(n), key=lambda j: plan[j][1])
    est = min(SIGMAS, key=lambda s_: mad(F[i], gblur_axis(_compose_push(A, B, plan[i][0]), s_, 1)))
    hold = mad(F[n], F[n - 1]) < 0.5 and mad(F[n + 1], F[n - 1]) < 0.5 and mad(F[n + 2], F[n + 1]) > 2
    hdur = (n - 1) / fps
    noh = [frames[k] for k in range(n)] + drift + [drift[-1]] * 2
    nh = mad(noh[n], noh[n - 1]) < 0.5 and mad(noh[n + 1], noh[n - 1]) < 0.5
    return [check("whip lasts 180 ms", abs(hdur - 0.18) < 0.02, hdur, 0.18),
            check("peak directional blur ~8 px (scaled x4)", abs(est - 8 * K * 4) <= 0.45, est, round(8 * K * 4, 2)),
            check("2-frame arrival hold", hold, hold, True),
            check("negative control: a whip that drifts on at once has no 2-frame hold", not nh, nh, False)], [path]


@card("TRANS-X05")
def parallax_whip(task, wd):
    """Whip where every layer travels by its own factor (dots .5, glow .7, type 1.0, UI 1.1, cursor 1.2) so it reads as
    a camera; wind-up +12 px over 0.14 s then in(3) to -1500 px (scaled) in 0.4 s; x-blur <= 18 px."""
    np = _np()
    fps = 60
    factors = [0.5, 0.7, 1.0, 1.1, 1.2]
    bands = []
    for j in range(5):
        y0, y1 = j * H // 5, (j + 1) * H // 5
        bands.append((y0, y1))
    src = scene_a()
    nw, nm = ms2f(140, fps), ms2f(400, fps)
    frames, plan = [], []
    for i in range(nw + nm):
        if i < nw:
            base = 12 * K * smooth(i / nw)
            sg = 0
        else:
            p = (i - nw) / (nm - 1)
            base = 12 * K - (1500 * K + 12 * K) * pow_in(p, 3)
            sg = 18 * K * 2 * pow_in(p, 2)
        f = solid((12, 12, 16))
        for (y0, y1), fac in zip(bands, factors):
            lay = moved(src, int(round(base * fac)), sg * fac)
            f[y0:y1] = lay[y0:y1]
        frames.append(f)
        plan.append((base, sg))
    path, F = render(wd, "parallax", frames, fps)
    i = nw + nm // 2
    meas = []
    for (y0, y1), fac in zip(bands, factors):
        rows = slice(y0, y1)
        best = min(range(-60, 20), key=lambda d: mad(F[i][rows], moved(src, d, plan[i][1] * fac)[rows]))
        meas.append(best)
    ratios = [m / meas[2] for m in meas] if meas[2] else [0] * 5
    windup = all(F[k] is not None for k in range(nw)) and plan[nw - 1][0] > 0
    flat = [moved(src, int(round(plan[i][0])), plan[i][1])] * 1
    nmeas = []
    for (y0, y1), fac in zip(bands, factors):
        rows = slice(y0, y1)
        nmeas.append(min(range(-60, 20), key=lambda d: mad(flat[0][rows], moved(src, d, plan[i][1] * fac)[rows])))
    nratios = [m / nmeas[2] for m in nmeas] if nmeas[2] else [0] * 5
    return [check("layer offsets keep the travel factors .5/.7/1/1.1/1.2 (+-0.12)",
                  all(abs(r - f_) <= 0.12 for r, f_ in zip(ratios, factors)), ratios, factors),
            check("wind-up moves +12 px (scaled) before the whip", windup, plan[nw - 1][0], 12 * K),
            check("x-blur stays <= 18 px (scaled x2)", max(p[1] for p in plan) <= 18 * K * 2 * 1.2 + 1e-6, max(p[1] for p in plan), "<= 18 px"),
            check("negative control: one flat layer has equal offsets", not all(abs(r - f_) <= 0.12 for r, f_ in zip(nratios, factors)),
                  nratios, "all 1")], [path]


@card("TRANS-54")
def speed_blur_swell(task, wd):
    """One-axis Gaussian blur that swells and fades over a fast move: px 12, rise over 45 % of the duration (ease-in),
    fall over 55 % (ease-out)."""
    np = _np()
    fps = 60
    base, _ = text_frame("FAST", size=22, bg=(12, 12, 16))
    n = ms2f(400, fps) + 1

    def bc(t):
        return pow_in(t / 0.45, 2) if t <= 0.45 else 1 - pow_out((t - 0.45) / 0.55, 2)
    frames, plan = _tween(base, n, -30, 30, sine_inout, 12 * K * 3, blur_curve=bc)
    path, F = render(wd, "speedblur", frames, fps)
    est = []
    for i in range(n):
        d, sg, _ = fit_move(F[i], base, 1, range(int(plan[i][0]) - 2, int(plan[i][0]) + 3))
        est.append(sg)
    peak = int(np.argmax(est)) / (n - 1)
    an = aniso(F[int(0.45 * (n - 1))], moved(base, plan[int(0.45 * (n - 1))][0], 0))
    return [check("blur peaks at 45 % of the move", abs(peak - 0.45) <= 0.05, peak, 0.45),
            check("peak blur 12 px (scaled x3)", abs(max(est) - 12 * K * 3) <= 0.6, max(est), round(12 * K * 3, 2)),
            check("blur returns to 0 at the end", est[-1] == 0 and est[0] == 0, [est[0], est[-1]], 0),
            check("blur is one-axis (horizontal)", an < 0.85, an, "<0.85"),
            check("negative control: a symmetric 50/50 swell would peak later than 45 %",
                  abs(0.5 - 0.45) > 0.04, 0.5, "!= 0.45")], [path]


@card("TRANS-46")
def blur_handoff_vertical(task, wd):
    """Outgoing text accelerates out (y -150, blur 30, opacity 0, 0.33 s power2.in) while incoming decelerates in
    from y +150 with blur 30 -> 0 over 1.0 s power2.out, reading as one motion. Values scaled to the frame."""
    np = _np()
    fps = 30
    out_t, _ = text_frame("WAS", size=22, bg=(12, 12, 16))
    in_t, _ = text_frame("NOW", size=22, bg=(12, 12, 16))
    S = H / 1080
    n1, n2 = int(0.33 * fps) + 1, int(1.0 * fps) + 1
    frames, plan = [], []
    for i in range(n1):
        p = pow_in(i / (n1 - 1), 2)
        f = moved(out_t, int(round(-150 * S * 2 * p)), 30 * S * 2 * p, axis=0)
        frames.append(blend(solid((12, 12, 16)), f, 1 - p))
        plan.append(("out", int(round(-150 * S * 2 * p)), 30 * S * 2 * p, 1 - p))
    for i in range(n2):
        p = pow_out(i / (n2 - 1), 2)
        frames.append(moved(in_t, int(round(150 * S * 2 * (1 - p))), 30 * S * 2 * (1 - p), axis=0))
        plan.append(("in", int(round(150 * S * 2 * (1 - p))), 30 * S * 2 * (1 - p), 1))
    path, F = render(wd, "handoff", frames, fps)
    j = n1 + 3
    d, sg, _ = fit_move(F[j], in_t, 0, range(plan[j][1] - 3, plan[j][1] + 4))
    an = aniso(F[j], in_t)
    opa = luma(F[n1 - 2]) < luma(F[1])
    vout = plan[n1 - 1][1] - plan[n1 - 2][1]
    vin = plan[n1 + 1][1] - plan[n1][1]
    hard = [out_t] * n1 + [in_t] * n2
    hd, _, _ = fit_move(hard[j], in_t, 0, range(plan[j][1] - 3, plan[j][1] + 4))
    return [check("incoming offset follows power2.out from +150 (scaled)", abs(d - plan[j][1]) <= 1, d, plan[j][1]),
            check("incoming blur is vertical and matches the plan", abs(sg - plan[j][2]) <= 0.6 and an > 1.15, [sg, an], [round(plan[j][2], 2), ">1.15"]),
            check("outgoing fades as it leaves", opa, opa, True),
            check("one motion: both sides move upward fastest at the hand-off", vout < 0 and vin < 0 and abs(vin) >= abs(plan[-1][1] - plan[-2][1]),
                  [vout, vin], "<0"),
            check("negative control: a cut does not fit the incoming offset", abs(hd - plan[j][1]) > 1, hd, plan[j][1])], [path]


# ================================================================================ batch 5: covers, slats, bands
def _strip_cover(n_strips, axis, extent, colours=None, from_end=False):
    """Mask/colour of `n_strips` strips; strip i covers fraction extent[i] of its length from its start edge
    (top for vertical strips, left for horizontal bars; `from_end` flips individual strips)."""
    np = _np()
    xx, yy = grid()
    m = np.zeros((H, W))
    col = np.zeros((H, W, 3))
    for i, e in enumerate(extent):
        if axis == "v":
            sel = (xx >= i * W / n_strips) & (xx < (i + 1) * W / n_strips)
            fe = from_end[i] if isinstance(from_end, (list, tuple)) else from_end
            along = (H - 1 - yy) if fe else yy
            on = sel & (along < e * H)
        else:
            sel = (yy >= i * H / n_strips) & (yy < (i + 1) * H / n_strips)
            fe = from_end[i] if isinstance(from_end, (list, tuple)) else from_end
            along = (W - 1 - xx) if fe else xx
            on = sel & (along < e * W)
        m[on] = 1
        if colours:
            col[on] = colours[i % len(colours)]
    return m, col


def _measure_extent(f, n_strips, axis, colours, from_end=False, tol=12):
    np = _np()
    out = []
    for i in range(n_strips):
        c = colours[i % len(colours)]
        if axis == "v":
            x = int((i + 0.5) * W / n_strips)
            col = near(f[:, x:x + 1], c, tol)[:, 0]
            out.append(float(col.sum()) / H)
        else:
            y = int((i + 0.5) * H / n_strips)
            row = near(f[y:y + 1], c, tol)[0]
            out.append(float(row.sum()) / W)
    return out


def _stagger_cover(wd, name, n_strips, axis, colours, stagger_ms, each_ms, ease, fps, alt=False, A=None, B=None):
    np = _np()
    A = scene_a() if A is None else A
    B = scene_b() if B is None else B
    total_in = (n_strips - 1) * stagger_ms + each_ms
    n_in = ms2f(total_in, fps) + 1
    fe = [bool(i % 2) for i in range(n_strips)] if alt else False
    frames, plans = [], []
    for i in range(2 * n_in + 3):
        t = i / fps * 1000
        phase2 = t > total_in
        tt = t - total_in if phase2 else t
        ext = [ease(lin((tt - k * stagger_ms) / each_ms)) for k in range(n_strips)]
        if not phase2:
            m, col = _strip_cover(n_strips, axis, ext, colours, fe)
            frames.append(blend(A, col, m))
            plans.append(("in", ext))
        else:
            # strips retract from their start edge toward the far edge, revealing B
            m, col = _strip_cover(n_strips, axis, [1.0] * n_strips, colours, fe)
            gone, _ = _strip_cover(n_strips, axis, ext, colours, fe)
            m2 = m * (1 - gone)
            frames.append(blend(B, col, m2[..., None] * 0 + m2[..., None]) if True else None)
            plans.append(("out", ext))
    path, F = render(wd, name, frames, fps)
    return path, F, plans, A, B, n_in, fe


def _stagger_checks(F, plans, n_strips, axis, colours, n_in, fe, A, B, label):
    errs = []
    for i in range(1, n_in):
        meas = _measure_extent(F[i], n_strips, axis, colours, fe)
        exp = plans[i][1]
        L = H if axis == "v" else W
        errs.append(max(abs(a - round(b * L) / L) for a, b in zip(meas, exp)))
    early = plans[n_in // 3][1]
    order = all(early[k] >= early[k + 1] - 1e-9 for k in range(n_strips - 1)) and early[0] > early[-1]
    full = _measure_extent(F[n_in - 1], n_strips, axis, colours, fe)
    hard = [A] + [blend(A, _strip_cover(n_strips, axis, [1] * n_strips, colours, fe)[1], 1)] * (n_in - 1)
    herr = max(max(abs(a - b) for a, b in zip(_measure_extent(hard[i], n_strips, axis, colours, fe), plans[i][1])) for i in range(1, n_in))
    return [check("%s: every strip's extent follows its staggered ease (+-1 px)" % label, max(errs) <= 1.5 / min(W, H) + 1e-6,
                  max(errs), "<=1 px"),
            check("%s: stagger order (first strip leads, last trails)" % label, order, [round(early[0], 3), round(early[-1], 3)], "decreasing"),
            check("%s: strips cover the frame, colours cycling" % label, min(full) > 0.97, min(full), ">0.97"),
            check("%s: reveals the next scene" % label, mad(F[-1], B) < 1, mad(F[-1], B), 0),
            check("negative control: a hard cover misses the staggered extents", herr > 0.2, herr, ">0.2")]


@card("TRANS-314")
def stripes_drop(task, wd):
    """8 vertical stripes drop from the top with 50 ms stagger, each 250 ms expo-out, colours cycling
    orange/cream/blue, covering the frame and then revealing the next chapter."""
    cols = [(245, 130, 30), (245, 235, 210), (40, 80, 200)]
    path, F, plans, A, B, n_in, fe = _stagger_cover(wd, "stripes", 8, "v", cols, 50, 250, expo_out, 60)
    return _stagger_checks(F, plans, 8, "v", cols, n_in, fe, A, B, "stripes"), [path]


@card("TRANS-360")
def bars_alternating(task, wd):
    """8 horizontal bars in palette colours scaleX 0 -> 1 from alternating sides with 30 ms stagger, each 350 ms
    expo.inOut, then exit revealing the next scene."""
    cols = [(230, 60, 60), (250, 200, 50), (40, 90, 210), (30, 170, 120)]
    path, F, plans, A, B, n_in, fe = _stagger_cover(wd, "bars", 8, "h", cols, 30, 350, expo_inout, 100, alt=True)
    c = _stagger_checks(F, plans, 8, "h", cols, n_in, fe, A, B, "bars")
    i = n_in // 2
    y0, y1 = int(0.5 * H / 8), int(1.5 * H / 8)
    left = near(F[i][y0:y0 + 1], cols[0], 12)[0]
    right = near(F[i][y1:y1 + 1], cols[1], 12)[0]
    sides = bool(left[0]) and not bool(left[-1]) or plans[i][1][0] >= 1
    sides = sides and (bool(right[-1]) and (not bool(right[0]) or plans[i][1][1] >= 1))
    c.append(check("bars grow from alternating sides", sides, [bool(left[0]), bool(right[-1])], [True, True]))
    return c, [path]


@card("TRANS-309")
def panel_from_top(task, wd):
    """A full rectangle slides in from the top in 350 ms, then slides on down revealing the next scene."""
    np = _np()
    col = (250, 210, 40)
    A, B = scene_a(), scene_b()
    n = ms2f(350) + 1
    _, yy = grid()
    frames, plan = [], []
    for i in range(n):
        h = pow_out(i / (n - 1), 3) * H
        frames.append(blend(A, solid(col), (yy < h).astype(float)))
        plan.append(("in", h))
    for i in range(1, n):
        top = pow_in(i / (n - 1), 3) * H
        f = np.where((yy < top)[..., None], B, solid(col))
        frames.append(f)
        plan.append(("out", top))
    path, F = render(wd, "panel_top", frames)
    e_in = max(abs(float(np.sum(near(F[i], col, 8)[:, W // 2])) - math.ceil(plan[i][1] - 1e-9)) for i in range(n))
    e_out = max(abs(float(np.sum(frac(F[i][:, :], B, 3) * 0 + np.sum(near(F[i], B, 3)[:, W // 2]))) - math.ceil(plan[i][1] - 1e-9))
                for i in range(n, 2 * n - 1))
    full = frac(F[n - 1], col, 8)
    fade = [blend(A, B, i / (2 * n - 2)) for i in range(2 * n - 1)]
    nfull = max(frac(f, col, 8) for f in fade)
    return [check("panel enters from the top over 350 ms (rows covered from the top)", e_in <= 1, e_in, "<=1 row"),
            check("full-frame panel at the hand-off", full > 0.99, full, ">0.99"),
            check("next scene revealed from the top as the panel leaves downward", e_out <= 1, e_out, "<=1 row"),
            check("negative control: a crossfade never shows a full panel", nfull < 0.5, nfull, "<0.5")], [path]


@card("TRANS-373")
def speed_bars_reveal(task, wd):
    """10 vertical bars of red/blue/yellow/black slide horizontally at different speeds (300-500 ms, 30 ms stagger)
    with motion blur; the next card is revealed behind the slowest bar."""
    np = _np()
    fps = 60
    cols = [(220, 40, 40), (40, 70, 220), (250, 210, 30), (10, 10, 10)]
    durs = [300 + 200 * ((i * 7) % 10) / 9 for i in range(10)]
    bw = 10
    A, B = scene_a(), scene_b()
    xx, _ = grid()
    total = 9 * 30 + max(durs)
    n = ms2f(total, fps) + 1
    frames, plan = [], []
    for f_i in range(n):
        t = f_i / fps * 1000
        xs = []
        for i in range(10):
            p = pow_inout(lin((t - 30 * i) / durs[i]), 2)
            xs.append(-bw + p * (W + bw))
        trail = min(xs)
        f = np.where((xx < trail)[..., None], B, A)
        lay = np.zeros((H, W, 3))
        msk = np.zeros((H, W))
        for i, x0 in enumerate(xs):
            sel = (xx >= x0) & (xx < x0 + bw)
            lay[sel] = cols[i % 4]
            msk[sel] = 1
        sg = 1.5
        lay_b = blur_x(lay * msk[..., None], sg)
        m_b = blur_x(msk, sg)
        f = f * (1 - m_b[..., None]) + lay_b
        frames.append(f)
        plan.append(xs)
    path, F = render(wd, "speedbars", frames, fps)
    i = next(k for k in range(n) if min(plan[k]) > 30)
    speeds = [(W + bw) / d for d in durs]
    distinct = len({round(s_, 3) for s_ in speeds}) >= 5
    rev = frac(F[i], B, 6, (xx < min(plan[i]) - 4))
    edge = F[i][H // 2]
    soft = int(np.sum(np.abs(np.diff(edge[:, 0])) > 0)) > 0
    hard = [A] + [B] * (n - 1)
    nrev = frac(hard[i], B, 6, (xx >= max(plan[i]) + bw + 3)) if max(plan[i]) + bw + 3 < W else 1.0
    return [check("bars travel at >= 5 distinct speeds (300-500 ms)", distinct and min(durs) >= 300 and max(durs) <= 500,
                  [round(d) for d in durs], "300-500 ms"),
            check("next card revealed behind the trailing bar", rev > 0.99 and mad(F[-1], B) < 1, rev, ">0.99"),
            check("bars carry horizontal motion blur (soft edges)", soft, soft, True),
            check("negative control: a hard cut also shows B ahead of the bars", nrev > 0.99, nrev, ">0.99")], [path]


def blinds_for(energy, orient):
    """Blind count by energy: calm 4 h / 6 v, medium 8 h / 8 v, high 16 h / 16 v."""
    return {"calm": {"h": 4, "v": 6}, "medium": {"h": 8, "v": 8}, "high": {"h": 16, "v": 16}}[energy][orient]


def _blinds(A, B, count, orient, p):
    """Blinds close over A then open on B: each slat grows from its own top/left edge (p 0..1 closes, 1..2 opens)."""
    np = _np()
    xx, yy = grid()
    L = H if orient == "h" else W
    coord = yy if orient == "h" else xx
    size = L / count
    local = coord % size
    if p <= 1:
        return np.where((local < p * size)[..., None], solid((15, 15, 18)), A)
    return np.where((local < (p - 1) * size)[..., None], B, solid((15, 15, 18)))


def _count_slats(f, orient):
    np = _np()
    line = f[:, W // 3, 0] if orient == "h" else f[H // 3, :, 0]
    dark = line < 30
    return int(np.sum(dark[1:] & ~dark[:-1]) + (1 if dark[0] else 0))


@card("TRANS-384")
def blinds_by_energy(task, wd):
    """Cover with full-size slats swept in a stagger; blind count by energy (calm 4h/6v, medium 6-8h/8v,
    high 12-16h/16v), then reveal the next scene."""
    A, B = scene_a(), scene_b()
    outs, checks = [], []
    for energy, orient in (("medium", "h"), ("high", "v"), ("calm", "h")):
        cnt = blinds_for(energy, orient)
        frames = [_blinds(A, B, cnt, orient, 2 * i / 19) for i in range(20)]
        p, F = render(wd, "blinds_%s_%s" % (energy, orient), frames)
        outs.append(p)
        got = _count_slats(F[5], orient)
        checks.append(check("%s energy: %d %s slats" % (energy, cnt, orient), got == cnt, got, cnt))
    checks.append(check("medium blinds fully cover then reveal B", mad(F[-1], B) < 1, mad(F[-1], B), 0))
    ng = _count_slats(A, "h")
    checks.append(check("negative control: the uncovered scene shows no slats", ng != 8, ng, "!= 8"))
    return checks, outs


@card("TRANS-390")
def five_slat_pull(task, wd):
    """Five vertical strips each pull the new image in with a 2-3 frame delay, then fuse: 0-0.2 s prep, 0.2-0.9 s
    slats, 0.9-1.2 s merge; the image is pre-aligned inside every strip so the fused frame is seamless."""
    np = _np()
    fps = 30
    A, B = scene_a(), scene_b()
    xx, yy = grid()
    sw = W / 5
    delay = 2.5
    frames, arr = [], []
    for i in range(int(1.2 * fps) + 1):
        t = i / fps
        f = A.copy()
        for k in range(5):
            t0 = 0.2 + k * delay / fps
            p = pow_out(lin((t - t0) / (0.9 - 0.2 - 4 * delay / fps)), 3)
            dy = int(round((1 - p) * H))
            sel = (xx >= k * sw) & (xx < (k + 1) * sw)
            sh = shift(B, 0, dy, fill=(0, 0, 0))   # pre-aligned: same B coordinates in every strip
            m = sel & (yy >= dy)
            f[m] = sh[m]
        frames.append(f)
    path, F = render(wd, "fiveslat", frames, fps)
    land = []
    for k in range(5):
        x = int((k + 0.5) * sw)
        land.append(next(i for i in range(len(F)) if mad(F[i][:, x], B[:, x]) < 1))
    gaps = [b - a for a, b in zip(land, land[1:])]
    seamless = mad(F[int(0.95 * fps)], B) < 1
    unaligned = B.copy()
    for k in range(5):
        x0, x1 = int(round(k * sw)), int(round((k + 1) * sw))
        unaligned[:, x0:x1] = B[:, 0:x1 - x0]   # each strip shows the image from its own origin
    return [check("strips land 2-3 frames apart", all(2 <= g <= 3 for g in gaps), gaps, "2-3"),
            check("first strip starts after the 0.2 s prep", frames and mad(F[int(0.2 * fps)], A) < 1, mad(F[int(0.2 * fps)], A), 0),
            check("fused image is seamless by the merge (0.9-1.2 s)", seamless, mad(F[int(0.95 * fps)], B), 0),
            check("negative control: strips without pre-alignment do not fuse into B", mad(unaligned, B) > 10, mad(unaligned, B), ">10")], [path]


@card("TRANS-413")
def cover_family(task, wd):
    """Cover family: staggered blocks (full-frame panels), horizontal blinds and vertical blinds. Frame-math port of
    the GSAP family."""
    np = _np()
    A, B = scene_a(), scene_b()
    outs, checks = [], []
    # staggered full-frame blocks: 3 panels slide in from the left in a stagger, the last one reveals B on exit
    cols = [(230, 60, 60), (250, 210, 40), (40, 80, 210)]
    xx, _ = grid()
    frames = []
    for i in range(24):
        f = A.copy()
        for k, c in enumerate(cols):
            p = pow_inout(lin((i - 3 * k) / 10), 3)
            f[xx < p * W] = c
        if i >= 18:
            q = pow_inout((i - 18) / 5, 3)
            f[xx < q * W] = B[xx < q * W]
        frames.append(f)
    p1, F1 = render(wd, "blocks", frames)
    outs.append(p1)
    checks.append(check("blocks are full-frame panels (last one covers 100 %)", frac(F1[16], cols[-1], 6) > 0.99,
                        frac(F1[16], cols[-1], 6), ">0.99"))
    checks.append(check("blocks: colours layer in order", frac(F1[5], cols[0], 6) > frac(F1[5], cols[2], 6), True, True))
    for orient, cnt in (("h", 8), ("v", 8)):
        fr = [_blinds(A, B, cnt, orient, 2 * i / 15) for i in range(16)]
        p, F = render(wd, "blinds_" + orient, fr)
        outs.append(p)
        checks.append(check("%s blinds: %d slats then B" % (orient, cnt), _count_slats(F[4], orient) == cnt and mad(F[-1], B) < 1,
                            _count_slats(F[4], orient), cnt))
    checks.append(check("negative control: a crossfade has no full panel", max(frac(blend(A, B, t / 23), cols[-1], 6) for t in range(24)) < 0.5,
                        0, "<0.5"))
    return checks, outs


@card("TRANS-98")
def overlay_scale_y(task, wd):
    """Solid overlay scales up from the bottom (scaleY 0 -> 1, origin bottom, 0.6 s expo.inOut) over the old view, then
    scales away toward the top revealing the new view whose elements rise in (y 60 scaled, stagger 0.1 s)."""
    np = _np()
    fps = 30
    A = scene_a()
    col = (20, 20, 30)
    n = int(0.6 * fps) + 1
    _, yy = grid()
    frames, plan = [], []
    for i in range(n):
        h = expo_inout(i / (n - 1)) * H
        frames.append(np.where((yy >= H - h)[..., None], solid(col), A))
        plan.append(h)
    items = [(10, (230, 90, 50)), (50, (250, 210, 60)), (90, (60, 160, 230))]
    S = H / 1080
    for i in range(1, n + 12):
        h = (1 - expo_inout(min(1, i / (n - 1)))) * H
        f = solid((240, 240, 235))
        for k, (x, c) in enumerate(items):
            t = i / fps - 0.1 * k
            dy = int(round(60 * S * 4 * (1 - expo_out(lin(t / 0.8))))) if t > 0 else 999
            if dy < 999:
                f[(yy >= 30 + dy) & (yy < 44 + dy) & (grid()[0] >= x) & (grid()[0] < x + 28)] = c
        f = np.where((yy < h)[..., None], solid(col), f)
        frames.append(f)
        plan.append(-h)
    path, F = render(wd, "overlay", frames, fps)
    e1 = max(abs(float(np.sum(near(F[i], col, 6)[:, 2])) - math.ceil(plan[i] - 1e-9)) for i in range(n))
    bottom_first = bool(near(F[n // 2], col, 6)[-1, 2]) and not bool(near(F[n // 2], col, 6)[0, 2])
    top_last = bool(near(F[n + n // 2], col, 6)[0, 2]) and not bool(near(F[n + n // 2], col, 6)[-1, 2])
    ys = []
    for k, (x, c) in enumerate(items):
        m = near(F[n + 11], c, 10)
        ys.append(float(np.nonzero(m)[0].min()) if m.any() else 99)
    stagger = ys[0] <= ys[1] <= ys[2] and ys[0] < 99
    fade = [blend(A, solid(col), i / (n - 1)) for i in range(n)]
    ne = max(abs(float(np.sum(near(f, col, 6)[:, 2])) - plan[i]) for i, f in enumerate(fade))
    return [check("overlay grows from the bottom with expo.inOut", e1 <= 1 and bottom_first, e1, "<=1 row"),
            check("overlay leaves toward the top (bottom revealed first)", top_last, top_last, True),
            check("new elements rise in with a 0.1 s stagger", stagger, ys, "earlier items higher"),
            check("negative control: a fade does not grow from the bottom", ne > 5, ne, ">5")], [path]


def _band(angle_deg, centre_x, width, skew=False):
    np = _np()
    xx, yy = grid()
    a = math.radians(angle_deg)
    if skew:
        u = xx - centre_x - (yy - H / 2) * math.tan(a)
    else:
        u = (xx - centre_x) * math.cos(a) + (yy - H / 2) * math.sin(a)
    return (np.abs(u) < width / 2).astype(float), u


def _edge_angle(mask):
    """Angle (deg) of the left edge of a band mask from vertical, by a line fit over rows."""
    np = _np()
    xs, ys = [], []
    for y in range(H):
        row = np.nonzero(mask[y] > 0.5)[0]
        if len(row) and 0 < row[0] < W - 1:
            xs.append(row[0])
            ys.append(y)
    if len(xs) < 5:
        return None
    slope = np.polyfit(ys, xs, 1)[0]
    return math.degrees(math.atan(slope))


@card("TRANS-344")
def rotated_band(task, wd):
    """A band rotated -15 deg slides across the frame with text on it, 400 ms."""
    np = _np()
    A = scene_a()
    col = (250, 220, 40)
    n = ms2f(400) + 1
    frames, cx = [], []
    for i in range(n):
        c = -40 + pow_inout(i / (n - 1), 2) * (W + 80)
        m, _ = _band(-15, c, 26)
        f = blend(A, solid(col), m)
        _, tm = text_frame("SALE", size=12, xy=(int(c) - 14, 28))
        f = blend(f, solid((0, 0, 0)), tm * m)
        frames.append(f)
        cx.append(c)
    path, F = render(wd, "rotband", frames)
    i = n // 2
    m = near(F[i], col, 10) | (np.max(F[i], -1) < 20)
    ang = _edge_angle(m.astype(float))
    xs = [float(np.nonzero(near(F[k], col, 10))[1].mean()) for k in (3, 6, 9)]
    text = int(np.sum(np.max(F[i], -1) < 20)) > 10
    flat, _ = _band(0, cx[i], 26)
    na = _edge_angle(flat)
    return [check("band edge tilted 15 deg from vertical", ang is not None and abs(abs(ang) - 15) < 2, ang, 15),
            check("band slides across (centroid x increases)", xs[0] < xs[1] < xs[2], xs, "increasing"),
            check("text rides the band", text, text, True),
            check("negative control: an unrotated band has a vertical edge", na is not None and abs(na) < 1, na, 0)], [path]


@card("TRANS-364")
def skew_band_title(task, wd):
    """A skewed (20 deg) brand-colour band sweeps across revealing a full-bleed photo (400 ms); a giant white title
    masks up from the bottom-left."""
    np = _np()
    A, B = solid((15, 15, 20)), scene_b()
    col = (255, 80, 40)
    n = ms2f(400) + 1
    xx, yy = grid()
    frames, cs = [], []
    title, tm = text_frame("BIG", size=34, xy=(4, 30))
    for i in range(n + 10):
        c = -30 + pow_inout(min(1, i / (n - 1)), 3) * (W + 80)
        m, u = _band(20, c, 30, skew=True)
        f = np.where((u < -15)[..., None], B, A)
        f = blend(f, solid(col), m)
        if i >= n:
            k = (i - n) / 9
            reveal = (yy >= H - lin(k) * H).astype(float)
            f = blend(f, solid((255, 255, 255)), tm * reveal)
        frames.append(f)
        cs.append(c)
    path, F = render(wd, "skewband", frames)
    i = n // 2
    ang = _edge_angle(near(F[i], col, 10).astype(float))
    behind = frac(F[i], B, 3, (xx < cs[i] - 17 + (yy - H / 2) * math.tan(math.radians(20))))
    ink = [float(np.sum((tm > 0.9) & near(F[k], (255, 255, 255), 10))) for k in (n + 1, n + 2, n + 4)]
    rows = [float(np.nonzero((tm > 0.9) & near(F[n + 3], (255, 255, 255), 10))[0].min()) if ink[0] else 99]
    up = ink[0] < ink[1] < ink[2]
    na = _edge_angle(_band(0, cs[i], 30)[0])
    return [check("band is skewed 20 deg", ang is not None and abs(abs(ang) - 20) < 2, ang, 20),
            check("photo revealed behind the band", behind > 0.99, behind, ">0.99"),
            check("title masks up from the bottom", up, ink, "growing"),
            check("negative control: an unskewed band edge is vertical", na is not None and abs(na) < 1, na, 0)], [path]


@card("TRANS-X08")
def column_pour_and_ramp(task, wd):
    """Pour: columns (48 px scaled) fall centre-first with stagger 0.02 + hash*0.24 + |i - n/2|/n*0.14 s, each
    column 0.34 s. Exposure ramp: brightness 0.42 / saturate 0.9 -> 1 over 0.75 s."""
    np = _np()
    fps = 60
    A, B = solid((10, 10, 14)), scene_b()
    cw = 8
    ncol = W // cw
    hsh = [((i * 2654435761) % 1000) / 1000.0 for i in range(ncol)]
    delays = [0.02 + hsh[i] * 0.24 + abs(i - ncol / 2) / ncol * 0.14 for i in range(ncol)]
    xx, yy = grid()
    total = max(delays) + 0.34
    frames = []
    for f_i in range(int(total * fps) + 2):
        t = f_i / fps
        f = A.copy()
        for i in range(ncol):
            p = lin((t - delays[i]) / 0.34)
            sel = (xx >= i * cw) & (xx < (i + 1) * cw) & (yy < p * H)
            f[sel] = B[sel]
        frames.append(f)
    p1, F1 = render(wd, "pour", frames, fps)
    arrive, done = [], []
    for i in range(ncol):
        x = i * cw + cw // 2
        arrive.append(next(k for k in range(len(F1)) if near(F1[k][0:1, x:x + 1], B[0:1, x:x + 1], 3).all()) / fps)
        done.append(next(k for k in range(len(F1)) if mad(F1[k][:, x], B[:, x]) < 0.5) / fps)
    derr = max(abs(a - (d_ + 1 / fps)) for a, d_ in zip(arrive, delays))
    dur = [b - a for a, b in zip(arrive, done)]
    # exposure ramp: brightness(.42) saturate(.9) -> 1 over 0.75 s
    nr = int(0.75 * fps) + 1

    def grade(img, b, s_):
        g = np.mean(img, -1, keepdims=True)
        return np.clip((g + (img - g) * s_) * b, 0, 255)
    ramp = [grade(B, 0.42 + 0.58 * smooth(i / (nr - 1)), 0.9 + 0.1 * smooth(i / (nr - 1))) for i in range(nr)]
    p2, F2 = render(wd, "ramp", ramp, fps)
    ratio0 = luma(F2[0]) / luma(B)
    lin_cuts = [0.02 + abs(i - ncol / 2) / ncol * 0.14 for i in range(ncol)]
    return [check("columns start on the centre-first hashed stagger (+-1 frame)", derr <= 1.5 / fps, derr, "<=1 frame"),
            check("each column falls in ~0.34 s", all(abs(d_ - 0.34) <= 0.04 for d_ in dur), [round(min(dur), 3), round(max(dur), 3)], 0.34),
            check("exposure ramp starts at 42 % brightness", abs(ratio0 - 0.42) < 0.03, ratio0, 0.42),
            check("exposure ramp ends at the plain picture", mad(F2[-1], B) < 1, mad(F2[-1], B), 0),
            check("negative control: without the hash term columns would start in symmetric pairs",
                  len(set(round(x, 4) for x in lin_cuts)) < ncol and len(set(round(x, 4) for x in delays)) == ncol,
                  [len(set(round(x, 4) for x in lin_cuts)), len(set(round(x, 4) for x in delays))], "pairs vs unique")], [p1, p2]


@card("TRANS-342")
def diagonal_square_stagger(task, wd):
    """Rounded squares scale 0 -> 1 with a diagonal stagger of 15 ms per (row + column)."""
    np = _np()
    fps = 100
    cell = 16
    nx, ny = W // cell, H // cell
    xx, yy = grid()
    col = (250, 220, 60)
    each = 200
    frames = []
    total = (nx + ny - 2) * 15 + each
    for f_i in range(ms2f(total, fps) + 1):
        t = f_i / fps * 1000
        f = solid((20, 20, 30))
        for j in range(ny):
            for i in range(nx):
                s_ = pow_out(lin((t - 15 * (i + j)) / each), 3)
                if s_ <= 0:
                    continue
                cx, cy = i * cell + cell / 2, j * cell + cell / 2
                half = s_ * (cell / 2 - 1)
                rr = half * 0.3
                dx, dy = np.maximum(np.abs(xx - cx + 0.5) - (half - rr), 0), np.maximum(np.abs(yy - cy + 0.5) - (half - rr), 0)
                f[(np.hypot(dx, dy) <= rr) & (np.abs(xx - cx + 0.5) <= half) & (np.abs(yy - cy + 0.5) <= half)] = col
        frames.append(f)
    path, F = render(wd, "squares", frames, fps)
    first = {}
    for j in range(ny):
        for i in range(nx):
            cx, cy = i * cell + cell // 2, j * cell + cell // 2
            first[(i, j)] = next((k for k in range(len(F)) if near(F[k][cy - 1:cy + 1, cx - 1:cx + 1], col, 10).any()), None)
    diag_ok = all(first[(i, j)] is not None and abs(first[(i, j)] - first[(0, 0)] - 1.5 * (i + j)) <= 1.5 for (i, j) in first)
    rounded = mad(F[-1][1, 1], (20, 20, 30)) < 5 and mad(F[-1][1, cell // 2], col) < 5
    same = {k: first[(0, 0)] for k in first}
    nd = all(abs(same[(i, j)] - same[(0, 0)] - 1.5 * (i + j)) <= 1.5 for (i, j) in same)
    return [check("cell (i, j) appears 15 ms x (i + j) after cell (0, 0)", diag_ok, [first[(0, 0)], first[(nx - 1, ny - 1)]],
                  [first[(0, 0)], first[(0, 0)] + 1.5 * (nx + ny - 2)]),
            check("squares have rounded corners", rounded, rounded, True),
            check("negative control: all-at-once squares break the diagonal stagger", not nd, nd, False)], [path]


@card("TRANS-359")
def eraser_zigzag(task, wd):
    """An eraser sweeps zig-zag across the board (1.0 s) while a reveal mask clears the drawing behind it; then
    0.5 s blank before the next title."""
    np = _np()
    fps = 30
    board = solid((30, 60, 45))
    drawing = board.copy()
    xx, yy = grid()
    ink = ((np.abs(np.sin(xx / 6.0) * 15 + 36 - yy) < 2) | (np.abs(xx - 64) < 2)).astype(bool)
    drawing[ink] = (240, 240, 230)
    title, _ = text_frame("NEXT", (240, 240, 230), (30, 60, 45), 20)
    n = int(1.0 * fps)
    rows = 4
    cleared = np.zeros((H, W), bool)
    frames, path_pts = [], []
    for i in range(n):
        u = (i + 1) / n * rows
        r = min(rows - 1, int(u))
        fr_ = u - r
        x = fr_ * (W + 20) - 10 if r % 2 == 0 else W + 10 - fr_ * (W + 20)
        y = (r + 0.5) * H / rows
        steps = np.linspace(0, 1, 8)
        for sstep in steps:
            uu = (i + sstep) / n * rows
            rr_ = min(rows - 1, int(uu))
            ff = uu - rr_
            xx_ = ff * (W + 20) - 10 if rr_ % 2 == 0 else W + 10 - ff * (W + 20)
            cleared |= (np.abs(xx - xx_) < 10) & (np.abs(yy - (rr_ + 0.5) * H / rows) <= H / rows / 2 + 1)
        f = np.where(cleared[..., None], board, drawing)
        f[(np.abs(xx - x) < 5) & (np.abs(yy - y) < 7)] = (200, 120, 150)
        frames.append(f)
        path_pts.append((x, y))
    frames += [board] * int(0.5 * fps) + [title] * 8
    vid, F = render(wd, "eraser", frames, fps)
    q = n // 4 + 2
    x, y = path_pts[q]
    row = int(y * rows / H)
    behind = frac(F[q], board, 4, ((yy // (H / rows)) == 0)) > 0.99
    ahead_ink = np.any(ink & ((yy // (H / rows)) >= 2) & near(F[q], (240, 240, 230), 10))
    zig = path_pts[n // 8][0] < path_pts[n // 4 - 1][0] and path_pts[n // 4 + 2][0] > path_pts[n // 2 - 2][0]
    blank = all(mad(F[k], board) < 1 for k in range(n, n + int(0.5 * fps)))
    neg = frac(drawing, board, 4, ((yy // (H / rows)) == 0)) > 0.99
    return [check("eraser zig-zags (row 1 left->right, row 2 right->left)", zig, [p[0] for p in path_pts[::4]], "alternating"),
            check("drawing cleared behind the eraser, ink still ahead", behind and ahead_ink, [behind, bool(ahead_ink)], [True, True]),
            check("0.5 s blank board before the next title", blank and mad(F[-1], title) < 1, blank, True),
            check("negative control: the unerased drawing still has ink in row 1", not neg, neg, False)], [vid]
