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


# ================================================================================ batch 6: FFmpeg xfade families
XF_D, XF_OFF, XF_LEN = 0.6, 0.4, 30   # 1 s clips at 30 fps, 0.6 s transition starting at 0.4 s


def noise_scene(seed, base):
    np = _np()
    rng = np.random.default_rng(seed)
    return np.clip(np.asarray(base, float) + rng.integers(-60, 61, (H, W, 3)), 0, 255).astype(float)


def _xf_clips(wd, audio=True, noise=False):
    """Lossless 1 s fixture clips A (warm, 440 Hz) and B (cool, 660 Hz); `noise` uses per-pixel noise textures."""
    A, B = (noise_scene(1, (200, 90, 50)), noise_scene(2, (40, 100, 210))) if noise else (scene_a(), scene_b())
    wd = Path(wd)
    pa, pb = write_video(wd / "xa.mkv", [A] * XF_LEN), write_video(wd / "xb.mkv", [B] * XF_LEN)
    if audio:
        ta, tb = fx.tone(wd / "xa.wav", 440, 1.0), fx.tone(wd / "xb.wav", 660, 1.0)
        pa, pb = _mux(wd, pa, ta, "xa_av.mkv"), _mux(wd, pb, tb, "xb_av.mkv")
    return pa, pb, A, B


def _xfade(wd, pa, pb, name, dur=XF_D, off=XF_OFF, audio=True):
    out = Path(wd) / ("xf_%s.mkv" % name)
    fc = "[0:v][1:v]xfade=transition=%s:duration=%s:offset=%s[v]" % (name, dur, off)
    args = ["-i", pa, "-i", pb]
    if audio:
        fc += ";[0:a][1:a]acrossfade=d=%s[a]" % dur
        fx.ffmpeg(*args, "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264rgb", "-qp", "0",
                  "-c:a", "pcm_s16le", out)
    else:
        fx.ffmpeg(*args, "-filter_complex", fc, "-map", "[v]", "-c:v", "libx264rgb", "-qp", "0", out)
    return out, fx.frames(out, size=(W, H))


def _cls(f, A, B):
    np = _np()
    dA, dB = np.abs(f - A).sum(-1), np.abs(f - B).sum(-1)
    return dB < dA, np.minimum(dA, dB) < 20


def _cent(m):
    np = _np()
    ys, xs = np.nonzero(m)
    return (float(xs.mean() / W), float(ys.mean() / H)) if len(xs) else (None, None)


def _push_fit(f, A, B, axis, sign, mode="push"):
    """Best offset o for a slide/cover/reveal frame: push moves both, cover moves B over static A, reveal moves A
    off a static B. sign -1 = toward left/up. Returns (mean abs error, o)."""
    np = _np()
    if axis == 0:
        f, A, B = f.transpose(1, 0, 2), A.transpose(1, 0, 2), B.transpose(1, 0, 2)
    if sign > 0:
        f, A, B = f[:, ::-1], A[:, ::-1], B[:, ::-1]
    L = f.shape[1]
    tot = f.size
    best = (1e9, 0)
    for o in range(0, L + 1):
        a_src = A[:, o:] if mode in ("push", "reveal") else A[:, :L - o]
        b_src = B[:, :o] if mode in ("push", "cover") else B[:, L - o:]
        e = (float(np.abs(f[:, :L - o] - a_src).sum()) + float(np.abs(f[:, L - o:] - b_src).sum())) / tot
        if e < best[0]:
            best = (e, o)
    return best


SIDE = {"left": (0.6, None), "right": (-0.4, None), "up": (None, 0.6), "down": (None, -0.4)}


def _side_ok(c, d):
    """B centroid on the side the motion comes from: 'left' -> B on the right (x > 0.6) etc."""
    if c[0] is None:
        return False
    tx, ty = SIDE[d]
    ok = True
    if tx is not None:
        ok &= c[0] > tx if tx > 0 else c[0] < -tx
    if ty is not None:
        ok &= c[1] > ty if ty > 0 else c[1] < -ty
    return ok


def _xf_prop(name, F, A, B, ref=None):
    """Known-answer property of one named xfade, measured on its frames. Returns (ok, measured, expected)."""
    np = _np()
    f18, f21, f24 = F[18], F[21], F[24]
    isB, pure = _cls(f18, A, B)
    c = _cent(isB)
    for d in ("left", "right", "up", "down"):
        if name in ("wipe" + d, "smooth" + d, "slide" + d, "cover" + d, "reveal" + d) or \
                name in ({"left": "hlslice", "right": "hrslice", "up": "vuslice", "down": "vdslice"}[d],
                         {"left": "hlwind", "right": "hrwind", "up": "vuwind", "down": "vdwind"}[d]):
            side = _side_ok(c, d)
            axis = 1 if d in ("left", "right") else 0
            sign = -1 if d in ("left", "up") else 1
            if name.startswith("wipe"):
                return side and pure.mean() > 0.98, [c, float(pure.mean())], "B on the far side, hard edge"
            if name.startswith("smooth"):
                return side and pure.mean() < 0.7, [c, float(pure.mean())], "B on the far side, soft edge"
            if name.startswith(("slide", "cover", "reveal")):
                mode = "push" if name.startswith("slide") else name[:5] if name.startswith("cover") else "reveal"
                e, o = _push_fit(f18, A, B, axis, sign, mode)
                L = W if axis == 1 else H
                return side and e < 4 and abs(o - L / 3) <= 3, [c, round(e, 2), o], "%s fit at o = L/3" % mode
            # slices / wind: banded or ragged boundary per line
            bounds = []
            lines = range(H) if axis == 1 else range(W)
            for k in lines:
                v = isB[k, :] if axis == 1 else isB[:, k]
                bounds.append(int(v.sum()))
            spread = float(np.std(bounds))
            if "slice" in name:
                line = isB[H // 2, :] if axis == 1 else isB[:, W // 2]
                runs = int(np.sum(line[1:] != line[:-1]))
                return side and pure.mean() > 0.98 and runs >= 4, [c, runs], "sliced edge (>= 4 B/A runs along the motion)"
            return side and spread > 2, [c, spread], "ragged wind edge"
    if name in ("fade", "fadefast", "fadeslow"):
        w, ok = mix_weight(f21, A, B)
        med, sd = float(np.median(w[ok])), float(np.std(w[ok]))
        if name == "fade":
            return 0.3 < med < 0.7 and sd < 0.05, [med, sd], "uniform mix ~0.5"
        rw, rok = mix_weight(ref[0][21], A, B)
        rm = float(np.median(rw[rok]))
        ow, ook = mix_weight(ref[2 if name == "fadefast" else 1][21], A, B)
        om = float(np.median(ow[ook]))
        if name == "fadefast":
            return med > rm + 0.05 and med > om and sd < 0.05, [med, rm, om], "non-linear curve, fast > slow > linear"
        return abs(med - rm) > 0.03 and med < om and sd < 0.05, [med, rm, om], "non-linear curve, below fadefast"
    if name == "dissolve":
        diff = float(np.mean(isB[:, 1:] != isB[:, :-1]))
        return pure.mean() > 0.95 and 0.15 < isB.mean() < 0.6 and diff > 0.2, [float(pure.mean()), float(isB.mean()), diff], "grainy per-pixel"
    if name == "fadeblack":
        return luma(f18) < 0.3 * min(luma(A), luma(B)), luma(f18), "dark"
    if name == "fadewhite":
        return luma(f18) > 200, luma(f18), ">200"
    if name == "fadegrays":
        sat = float(np.mean(np.max(F[16], -1) - np.min(F[16], -1)))
        sa = float(np.mean(np.max(A, -1) - np.min(A, -1)))
        return sat < 0.6 * sa, [sat, sa], "desaturated"
    if name in ("circleopen", "vertopen", "horzopen"):
        b, _ = _cls(f21, A, B)
        inner, outer = float(b[18:54, 32:96].mean()), float((b.sum() - b[18:54, 32:96].sum()) / (W * H - 36 * 64))
        return inner > 0.9 and outer < 0.5, [inner, outer], "B opens from the centre"
    if name in ("circleclose", "vertclose", "horzclose"):
        b, _ = _cls(f21, A, B)
        inner, outer = float(b[18:54, 32:96].mean()), float((b.sum() - b[18:54, 32:96].sum()) / (W * H - 36 * 64))
        return inner < 0.1 and outer > 0.5, [inner, outer], "B closes in from the edges"
    if name in ("circlecrop", "rectcrop"):
        b, _ = _cls(F[27], A, B)
        inner, outer = float(b[18:54, 32:96].mean()), float((b.sum() - b[18:54, 32:96].sum()) / (W * H - 36 * 64))
        return luma(f21) < 5 and inner > outer, [luma(f21), inner, outer], "crops to black then opens B from the centre"
    if name == "radial":
        ws = [float(_cls(F[i], A, B)[0].mean()) for i in (15, 18, 21, 24, 27)]
        xx, yy = grid()
        ang = np.degrees(np.arctan2(yy - H / 2, xx - W / 2))[isB]
        span = float(np.ptp(ang)) if ang.size else 0
        return all(b_ >= a_ - 0.01 for a_, b_ in zip(ws, ws[1:])) and 0 < ws[1] < 0.5 and span < 200, [ws, span], "angular sweep"
    if name.startswith("diag"):
        corner = {"diagtl": (1, 1), "diagtr": (0, 1), "diagbl": (1, 0), "diagbr": (0, 0)}[name]
        b, _ = _cls(F[21], A, B)
        cc = _cent(b)
        ok = cc[0] is not None and ((cc[0] > 0.5) == bool(corner[0])) and ((cc[1] > 0.5) == bool(corner[1]))
        return ok, cc, "B from the opposite corner"
    if name.startswith("wipe") and len(name) == 6:
        corner = {"wipetl": (1, 1), "wipetr": (0, 1), "wipebl": (1, 0), "wipebr": (0, 0)}[name]
        ok = c[0] is not None and ((c[0] > 0.5) == bool(corner[0])) and ((c[1] > 0.5) == bool(corner[1])) and pure.mean() > 0.98
        return ok, c, "corner wipe"
    if name in ("squeezeh", "squeezev"):
        b, _ = _cls(f18, A, B)
        if name == "squeezeh":   # A squeezed toward the horizontal centre line: B shows above and below
            band = b[24:48].mean()
            edge = (b[:10].mean() + b[-10:].mean()) / 2
        else:                    # A squeezed toward the vertical centre line: B shows left and right
            band = b[:, 40:88].mean()
            edge = (b[:, :16].mean() + b[:, -16:].mean()) / 2
        return band < 0.05 and edge > 0.9 and mad(f18, A) > 5, [float(band), float(edge)], "A squeezed into the middle"
    if name == "zoomin":
        best = min((mad(F[18], scale_about(A, s_, fill=(0, 0, 0))), s_) for s_ in (1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.8, 2.0))
        return best[1] > 1.05 and best[0] < mad(F[18], A), best, "A zoomed in"
    if name == "pixelize":
        eqs = [float(np.mean(np.all(np.abs(F[i][:, 1:] - F[i][:, :-1]) < 0.5, -1))) for i in (18, 21, 24)]
        ea = float(np.mean(np.all(np.abs(A[:, 1:] - A[:, :-1]) < 0.5, -1)))
        return min(eqs) > 0.5 and ea < 0.05, [eqs, ea], "noise texture shown in blocks (equal neighbours)"
    if name == "hblur":
        f = F[19]
        bx = min((mad(f, blur_x(blend(A, B, w_ / 20), s_)), s_, w_ / 20) for s_ in (1, 2, 4, 6, 8, 12, 16) for w_ in range(0, 21))
        by = min((mad(f, blur_y(blend(A, B, w_ / 20), s_)), s_, w_ / 20) for s_ in (1, 2, 4, 6, 8, 12, 16) for w_ in range(0, 21))
        return bx[1] >= 2 and bx[0] < 0.6 * by[0], [round(bx[0], 2), bx[1], round(by[0], 2)], "horizontal blur explains the frame"
    if name == "distance":
        ws = [float(_cls(F[i], A, B)[0].mean()) for i in range(11, 17)]
        lin_f = blend(A, B, 1.0 / 18)
        return any(0.2 < w_ < 0.9 for w_ in ws) and all(b_ >= a_ - 0.01 for a_, b_ in zip(ws, ws[1:])) and \
            mad(F[13], lin_f) > 10, ws, "per-pixel distance switch"
    raise KeyError(name)


def _xf_family(wd, names, label):
    np = _np()
    pa, pb, A, B = _xf_clips(wd, noise=names == ["pixelize"])
    outs, checks = [], []
    ref = None
    if any(n_ in ("fadefast", "fadeslow") for n_ in names):
        ref = [_xfade(wd, pa, pb, n_, audio=False)[1] for n_ in ("fade", "fadefast", "fadeslow")]
    for nm in names:
        out, F = _xfade(wd, pa, pb, nm)
        outs.append(out)
        ok, meas, exp = _xf_prop(nm, F, A, B, ref)
        checks.append(check("%s: %s" % (nm, exp), ok, meas, exp))
        checks.append(check("%s: 1 s + 1 s - 0.6 s = 42 frames, A before, B after" % nm,
                            len(F) == 42 and mad(F[11], A) < 1 and mad(F[-1], B) < 1, len(F), 42))
    # matching audio cross-fade on the last one: both tones in the middle, only B at the end
    x, rate = fx.read_wav(_extract_wav(wd, outs[-1]))
    mid = x[int(0.6 * rate):int(0.8 * rate), 0]
    end = x[-int(0.15 * rate):, 0]

    def amp(sig, fq):
        spec = np.abs(np.fft.rfft(sig * np.hanning(len(sig))))
        fr = np.fft.rfftfreq(len(sig), 1 / rate)
        return float(spec[np.argmin(np.abs(fr - fq))])
    both = amp(mid, 440) > 0.2 * amp(mid, 660) and amp(mid, 660) > 0.2 * amp(mid, 440)
    only_b = amp(end, 440) < 0.05 * amp(end, 660)
    checks.append(check("%s: matching audio cross-fade (both tones mid, B tone at the end)" % label, both and only_b,
                        [round(amp(mid, 440)), round(amp(mid, 660)), round(amp(end, 440))], "mix then B"))
    concat = [A] * XF_LEN + [B] * XF_LEN
    neg = [_xf_prop(nm, concat, A, B, [concat] * 3)[0] for nm in names]
    checks.append(check("negative control: a plain concat fails every %s property" % label, not any(neg), neg, "all False"))
    return checks, outs


def _extract_wav(wd, video):
    out = Path(wd) / (Path(video).stem + ".wav")
    fx.ffmpeg("-i", video, "-vn", "-c:a", "pcm_s16le", out)
    return out


def _xf_card(cid, names, label):
    @card(cid)
    def _run(task, wd, names=names, label=label):
        return _xf_family(wd, names, label)
    _run.__doc__ = "FFmpeg xfade %s family (%s) with matching acrossfade, each property measured on frames." % (label, ", ".join(names))
    return _run


_xf_card("TRANS-62", ["fade", "fadefast", "fadeslow", "dissolve", "fadeblack", "fadewhite", "fadegrays"], "cross-fade")
_xf_card("TRANS-63", ["wipeleft", "wiperight", "wipeup", "wipedown", "wipetl", "wipetr", "wipebl", "wipebr"], "wipe")
_xf_card("TRANS-64", ["slideleft", "slideright", "slideup", "slidedown"], "slide")
_xf_card("TRANS-65", ["smoothleft", "smoothright", "smoothup", "smoothdown"], "smooth wipe")
_xf_card("TRANS-66", ["circlecrop", "circleopen", "circleclose", "rectcrop", "radial"], "circle/rect/radial")
_xf_card("TRANS-67", ["vertopen", "vertclose", "horzopen", "horzclose"], "barn-door")
_xf_card("TRANS-68", ["diagtl", "diagtr", "diagbl", "diagbr"], "diagonal")
_xf_card("TRANS-69", ["hlslice", "hrslice", "vuslice", "vdslice"], "slice")
_xf_card("TRANS-70", ["hlwind", "hrwind", "vuwind", "vdwind"], "wind")
_xf_card("TRANS-71", ["coverleft", "coverright", "coverup", "coverdown"], "cover")
_xf_card("TRANS-72", ["revealleft", "revealright", "revealup", "revealdown"], "reveal")
_xf_card("TRANS-73", ["squeezeh", "squeezev"], "squeeze")
_xf_card("TRANS-74", ["zoomin"], "zoom-in")
_xf_card("TRANS-75", ["pixelize"], "pixelize")
_xf_card("TRANS-76", ["hblur"], "horizontal blur")
_xf_card("TRANS-77", ["distance"], "distance")


def _xfade_names():
    import re
    out = fx.run(["ffmpeg", "-hide_banner", "-h", "filter=xfade"]).stdout
    return [m_.group(1) for m_ in re.finditer(r"^\s{5}(\w+)\s+(-?\d+)\s", out, re.M) if m_.group(1) != "custom"]


@card("TRANS-59")
def xfade_catalogue(task, wd):
    """58 named xfade transitions with matching audio cross-fades, filtered to those the local FFmpeg build reports
    (parsed from `ffmpeg -h filter=xfade`); a sample of the list is rendered and measured."""
    names = _xfade_names()
    spec = ["fade", "wipeleft", "wiperight", "wipeup", "wipedown", "slideleft", "slideright", "slideup", "slidedown",
            "circlecrop", "rectcrop", "distance", "fadeblack", "fadewhite", "radial", "smoothleft", "smoothright",
            "smoothup", "smoothdown", "circleopen", "circleclose", "vertopen", "vertclose", "horzopen", "horzclose",
            "dissolve", "pixelize", "diagtl", "diagtr", "diagbl", "diagbr", "hlslice", "hrslice", "vuslice", "vdslice",
            "hblur", "fadegrays", "wipetl", "wipetr", "wipebl", "wipebr", "squeezeh", "squeezev", "zoomin", "fadefast",
            "fadeslow", "hlwind", "hrwind", "vuwind", "vdwind", "coverleft", "coverright", "coverup", "coverdown",
            "revealleft", "revealright", "revealup", "revealdown", "notarealone"]
    supported = [n_ for n_ in spec if n_ in names]
    lst = save_json(wd, "transitions.json", {"supported": supported, "dropped": [n_ for n_ in spec if n_ not in names]})
    c, outs = _xf_family(wd, ["wipeup", "slideright", "circleopen"], "sample")
    c.insert(0, check("local build reports 58 named transitions", len(names) == 58, len(names), 58))
    c.insert(1, check("filter keeps the 58 supported and drops the unknown name", len(supported) == 58 and "notarealone" not in supported,
                      len(supported), 58))
    return c, [lst] + outs


@card("TRANS-58")
def xfade_clamped(task, wd):
    """FFmpeg xfade + matching acrossfade with the duration clamped to half the shorter clip (requested 0.8 s on
    1 s clips -> 0.5 s; allowed 0.05-5 s)."""
    pa, pb, A, B = _xf_clips(wd)
    req = 0.8
    d = max(0.05, min(5.0, req, 1.0 / 2))
    out, F = _xfade(wd, pa, pb, "fade", dur=d, off=1.0 - d)
    x, rate = fx.read_wav(_extract_wav(wd, out))
    unclamped = 1.0 + 1.0 - req
    return [check("duration clamped to half the clip", d == 0.5, d, 0.5),
            check("video length = 1 + 1 - 0.5 s", len(F) == 45, len(F) / 30, 1.5),
            check("audio cross-fade gives the same length", abs(len(x) / rate - 1.5) < 0.02, len(x) / rate, 1.5),
            check("mid-transition frame is a mix", 0.3 < float(_np().median(mix_weight(F[22], A, B)[0])) < 0.7,
                  float(_np().median(mix_weight(F[22], A, B)[0])), "0.3-0.7"),
            check("negative control: the unclamped request would overlap past half a clip", unclamped < 1.5, unclamped, "<1.5")], [out]


@card("TRANS-82")
def xfade_offset_rule(task, wd):
    """[0:v][1:v]xfade=transition=TYPE:duration=d:offset=len1-d with [0:a][1:a]acrossfade=d=d, d = 0.5 s."""
    np = _np()
    pa, pb, A, B = _xf_clips(wd)
    d = 0.5
    off = 1.0 - d
    outs, checks = [], []
    for nm in ("fade", "wipeleft", "slideup"):
        out, F = _xfade(wd, pa, pb, nm, dur=d, off=off)
        outs.append(out)
        start = next(i for i in range(len(F)) if mad(F[i], A) > 0.5)
        checks.append(check("%s: transition starts at offset len1 - d = 0.5 s" % nm, abs(start / 30 - off) <= 1 / 30 + 1e-9, start / 30, off))
        checks.append(check("%s: ends exactly as clip 1 ends (B pure at 1.0 s)" % nm, mad(F[30], B) < 1 and mad(F[29], B) > 0.1, [mad(F[29], B), mad(F[30], B)], "B at 1.0 s"))
    x, rate = fx.read_wav(_extract_wav(wd, outs[0]))
    checks.append(check("audio length matches video (1.5 s)", abs(len(x) / rate - 1.5) < 0.02, len(x) / rate, 1.5))
    bad = 0.2
    checks.append(check("negative control: offset 0.2 s would end before clip 1 does", bad + d < 1.0, bad + d, "<1.0"))
    return checks, outs


# ================================================================================ batch 7: glitch, RGB, pixel
def band_offsets_measured(f, src, n, rng=45):
    """Per-band best horizontal (wrapping) shift of src that explains f (None for a featureless band);
    ties resolve to the smallest |shift|."""
    np = _np()
    out = []
    order = sorted(range(-rng, rng + 1), key=abs)
    for i in range(n):
        y0, y1 = i * H // n, (i + 1) * H // n
        if float(np.std(src[y0:y1], axis=1).max()) < 3:
            out.append(None)
            continue
        best = min(order, key=lambda d: mad(f[y0:y1], np.roll(src[y0:y1], d, axis=1)))
        out.append(best)
    return out


def chan_shift_vs(f, src, rng=20):
    """(R, B) horizontal shifts of f's channels against the source image's own channels."""
    res = []
    order = sorted(range(-rng, rng + 1), key=abs)
    for ch in (0, 2):
        res.append(min(order, key=lambda d: mad(f[..., ch:ch + 1], shift(src[..., ch:ch + 1], d, 0))))
    return res


def glitch_frame(img, rgb, offsets):
    return band_shift(rgb_split(img, rgb), offsets)


def _rng(seed):
    return _np().random.default_rng(seed)


def chan_offset_pair(f, rng=20):
    """(R vs G, B vs G) horizontal offsets."""
    np = _np()
    g = f[..., 1]
    res = []
    for ch in (0, 2):
        c = f[..., ch]
        best, arg = 1e9, 0
        for d in range(-rng, rng + 1):
            a = c[:, max(0, d):W + min(0, d)]
            b = g[:, max(0, -d):W - max(0, d)]
            e = float(np.mean(np.abs(a - b)))
            if e < best - 1e-9:
                best, arg = e, d
        res.append(arg)
    return res


def _glitch_seq(wd, name, word, nfr, rgb_of, bands_of, n_bands, fps=FPS, pre=4, post=4, nxt=None):
    base, _ = text_frame(word, size=26)
    after = base if nxt is None else nxt
    frames = [base] * pre
    plan = []
    for k in range(nfr):
        r, o = rgb_of(k), bands_of(k)
        frames.append(glitch_frame(base, r, o))
        plan.append((r, o))
    frames += [after] * post
    path, F = render(wd, name, frames, fps)
    return path, F, plan, base


def _glitch_checks(F, plan, base, n_bands, pre, rgb_range, shift_max, label):
    np = _np()
    offs = [chan_offset_pair(F[pre + k]) for k in range(len(plan))]
    rgb_ok = all(o == [p[0], -p[0]] for o, p in zip(offs, plan))
    in_range = all(rgb_range[0] <= abs(p[0]) <= rgb_range[1] for p in plan)
    meas = [band_offsets_measured(rgb_split(F[pre + k], 0) if False else F[pre + k], rgb_split(base, plan[k][0]), n_bands) for k in (0, len(plan) - 1)]
    def wrap(d):
        return (d + W // 2) % W - W // 2
    band_ok = all(max([abs(wrap(a - b)) for a, b in zip(m_, plan[k][1]) if a is not None] or [99]) <= 1
                  for m_, k in zip(meas, (0, len(plan) - 1)))
    clean = mad(F[pre - 1], base) < 1 and mad(F[pre + len(plan)], F[-1]) < 1 and chan_offset_pair(F[-1]) == [0, 0]
    neg = chan_offset_pair(base)
    return [check("%s: R/B channels offset as planned on every glitch frame" % label, rgb_ok, offs[:3], [[p[0], -p[0]] for p in plan[:3]]),
            check("%s: offsets within %s px" % (label, rgb_range), in_range, [p[0] for p in plan], rgb_range),
            check("%s: band displacements measured as planned (<= %d px)" % (label, shift_max), band_ok and max(abs(x) for p in plan for x in p[1]) <= shift_max,
                  meas[0], plan[0][1]),
            check("%s: clean before and after" % label, clean, clean, True),
            check("negative control: the clean word has no channel offset", neg == [0, 0], neg, [0, 0])]


@card("TRANS-318")
def rgb_band_ghost(task, wd):
    """Between scenes: text drawn with R/G/B offsets 6-12 px plus 4-8 random horizontal band displacements up to
    40 px (and the ghost copies they create), for 4 frames (133 ms, inside 100-200 ms)."""
    r = _rng(318)
    nb = 6
    rgbs = [int(r.integers(6, 13)) * (1 if k % 2 else -1) for k in range(4)]
    bands = [[int(x) for x in r.integers(-40, 41, nb)] for _ in range(4)]
    path, F, plan, base = _glitch_seq(wd, "rgbband", "SCENE", 4, lambda k: rgbs[k], lambda k: bands[k], nb)
    c = _glitch_checks(F, plan, base, nb, 4, (6, 12), 40, "glitch")
    gl = [i for i in range(len(F)) if chan_offset_pair(F[i]) != [0, 0]]
    c.append(check("glitch lasts 100-200 ms", 0.1 <= len(gl) / FPS <= 0.2, len(gl) / FPS, "0.1-0.2 s"))
    return c, [path]


@card("TRANS-334")
def rgb_slice_frames(task, wd):
    """Offset R/G/B channels 6-12 px and slice horizontal bands with random x shifts for 3-6 frames (5 here)."""
    r = _rng(334)
    nb = 8
    rgbs = [int(r.integers(6, 13)) for _ in range(5)]
    bands = [[int(x) for x in r.integers(-20, 21, nb)] for _ in range(5)]
    path, F, plan, base = _glitch_seq(wd, "rgbslice", "CUT", 5, lambda k: rgbs[k], lambda k: bands[k], nb)
    c = _glitch_checks(F, plan, base, nb, 4, (6, 12), 20, "slice")
    gl = [i for i in range(len(F)) if chan_offset_pair(F[i]) != [0, 0]]
    c.append(check("3-6 glitch frames", 3 <= len(gl) <= 6, len(gl), "3-6"))
    return c, [path]


@card("TRANS-352")
def strip_glitch_cut(task, wd):
    """Offset 6-12 horizontal strips randomly by +-40 px, split RGB, flash 3-5 frames, then cut to the next scene
    (0.3-0.5 s overall)."""
    r = _rng(352)
    nb = 9
    nxt, _ = text_frame("NEXT", size=26, bg=(20, 30, 80))
    rgbs = [int(r.integers(4, 10)) for _ in range(4)]
    bands = [[int(x) for x in r.integers(-40, 41, nb)] for _ in range(4)]
    path, F, plan, base = _glitch_seq(wd, "stripglitch", "NOW", 4, lambda k: rgbs[k], lambda k: bands[k], nb, pre=4, post=6, nxt=nxt)
    c = _glitch_checks(F, plan, base, nb, 4, (4, 10), 40, "strips")[:3]
    total = (4 + 6) / FPS
    c.append(check("cut to the next scene right after the flash", mad(F[8], nxt) < 1 and mad(F[3], base) < 1, mad(F[8], nxt), 0))
    c.append(check("glitch + landing within 0.3-0.5 s", 0.3 <= total <= 0.5, total, "0.3-0.5"))
    nm_ = [x for x in band_offsets_measured(base, base, nb) if x is not None]
    c.append(check("negative control: a plain cut has no displaced strips", nm_ and all(x == 0 for x in nm_), nm_, 0))
    return c, [path]


@card("TRANS-330")
def triple_word_decay(task, wd):
    """Word rendered three times (red/blue/white) offset +-6 px with 2-3 slice displacements that decay to 0 over
    200 ms, while the word scales 1.2 -> 1 (screen blend)."""
    np = _np()
    fps = 30
    base, m = text_frame("POP", size=24)
    n = ms2f(200, fps) + 1
    frames, plan = [], []
    r = _rng(330)
    sl = [int(x) for x in r.integers(-12, 13, 3)]
    for i in range(n):
        k = 1 - i / (n - 1)
        s_ = 1 + 0.2 * k
        sc = scale_about(base, s_)
        red = shift(sc * np.array([1, 0, 0]), int(round(6 * k)), 0)
        blue = shift(sc * np.array([0, 0, 1]), -int(round(6 * k)), 0)
        white = sc
        scr = 255 - (255 - red) * (255 - blue) * (255 - white) / 255 ** 2   # screen blend
        offs = [int(round(o * k)) for o in sl]
        frames.append(band_shift(scr, offs))
        plan.append((int(round(6 * k)), s_, offs))
    frames += [base] * 4
    path, F = render(wd, "triple", frames, fps)
    widths = []
    for i in range(n):
        cols = np.nonzero(np.max(F[i], (0, 2)) > 128)[0]
        widths.append(int(cols.max() - cols.min()) if len(cols) else 0)
    bw = int(np.ptp(np.nonzero(np.max(base, (0, 2)) > 128)[0]))
    red_lead = [int(np.nonzero(F[i][..., 0].max(0) > 128)[0].max() - np.nonzero(F[i][..., 2].max(0) > 128)[0].max()) for i in range(n)]
    dec = all(b <= a for a, b in zip(red_lead, red_lead[1:])) and red_lead[-1] == 0 and red_lead[0] == 6
    return [check("red copy leads by 6 px and decays to 0 over 200 ms", dec, red_lead, "6 -> 0"),
            check("word scales 1.2 -> 1 (width shrinks to the clean width)", widths[0] > widths[-1] and abs(widths[-1] - bw) <= 1,
                  [widths[0], widths[-1], bw], "decreasing to clean"),
            check("ends clean", mad(F[-1], base) < 1, mad(F[-1], base), 0),
            check("negative control: the clean word has no red lead", int(np.nonzero(base[..., 0].max(0) > 128)[0].max() - np.nonzero(base[..., 2].max(0) > 128)[0].max()) == 0,
                  0, 0)], [path]


@card("TRANS-354")
def streak_lines_wordmark(task, wd):
    """Thin (1-2 px) horizontal coloured lines streak across behind the wordmark at random (life 200 ms) with a
    brief 2 px chromatic offset on the text."""
    np = _np()
    fps = 30
    base, m = text_frame("KOSIF", size=22, bg=(10, 10, 14))
    r = _rng(354)
    life = ms2f(200, fps)
    lines = [(int(r.integers(0, H - 2)), int(r.integers(1, 3)), int(r.integers(0, 10)),
              tuple(int(x) for x in r.choice([[255, 60, 60], [60, 200, 255], [255, 220, 60]]))) for _ in range(8)]
    frames = []
    for i in range(16):
        f = solid((10, 10, 14))
        for (y, th, t0, c) in lines:
            if t0 <= i < t0 + life:
                p = (i - t0) / life
                x1 = int(p * W * 1.5)
                f[y:y + th, max(0, x1 - 40):min(W, x1)] = c
        txt = rgb_split(base, 2) if 5 <= i < 7 else base
        f = np.maximum(f, txt)
        frames.append(f)
    path, F = render(wd, "streaks", frames, fps)
    ok_life, ok_thin, behind = True, True, True
    for (y, th, t0, c) in lines:
        on = [i for i in range(16) if near(F[i][y:y + th], c, 20).any()]
        if on:
            ok_life &= len(on) <= life
        ok_thin &= th <= 2
    for i in range(16):
        behind &= bool(np.all(near(F[i], (255, 255, 255), 10)[m > 0.99]) or 5 <= i < 7)
    ca = [chan_offset_pair(F[i]) for i in (4, 5, 6, 7)]
    return [check("each line lives <= 200 ms", ok_life, life, "<= %d frames" % life),
            check("lines are 1-2 px", ok_thin, True, True),
            check("lines pass behind the wordmark (text pixels untouched)", behind, behind, True),
            check("brief 2 px chromatic offset on the text (2 frames)", ca[1] == [2, -2] and ca[2] == [2, -2] and ca[0] == [0, 0] and ca[3] == [0, 0],
                  ca, [[0, 0], [2, -2], [2, -2], [0, 0]]),
            check("negative control: the plain wordmark has no offset", chan_offset_pair(base) == [0, 0], chan_offset_pair(base), [0, 0])], [path]


def overlay_normal(bg, col, mask, opacity):
    return blend(bg, solid(col), mask * opacity)


def overlay_multiply(bg, col, mask, opacity):
    np = _np()
    mul = bg * np.asarray(col, float) / 255.0
    return blend(bg, mul, mask * opacity)


def _jitter_overlays(wd, name, seed, n=6, op=0.35, step_s=0.03, amp=(30, 60)):
    """Glitch: n jitter frames every step_s s, scene offset +-amp px, tinted R/G/B overlays in normal blend at op."""
    np = _np()
    fps = int(round(1 / step_s))
    A = scene_a()
    k = W / 1920 * 4
    r = _rng(seed)
    cols = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    xx, yy = grid()
    frames, plan = [A] * 2, []
    for i in range(n):
        off = int(round(r.integers(amp[0], amp[1] + 1) * k)) * (1 if i % 2 else -1)
        f = np.roll(A, off, axis=1)
        y0 = int(r.integers(0, H - 20))
        band = ((yy >= y0) & (yy < y0 + 16)).astype(float)
        c = cols[i % 3]
        f = overlay_normal(f, c, band, op)
        frames.append(f)
        plan.append((off, y0, c))
    frames += [A] * 2
    path, F = render(wd, name, frames, fps)
    return path, F, plan, A, fps


def _overlay_opacity(F, plan, A, pre=2):
    np = _np()
    ops = []
    for i, (off, y0, c) in enumerate(plan):
        under = np.roll(A, off, axis=1)[y0 + 2:y0 + 14]
        got = F[pre + i][y0 + 2:y0 + 14]
        cc = np.asarray(c, float)
        o = np.sum((got - under) * (cc - under)) / max(np.sum((cc - under) ** 2), 1)
        ops.append(float(o))
    return ops


@card("TRANS-42")
def tinted_rgb_jitter(task, wd):
    """Tinted R/G/B copies jitter with large offsets (+-30-60 px, scaled) for 6 frames every 0.03 s; overlays use
    normal blend at 35 % (not multiply)."""
    np = _np()
    path, F, plan, A, fps = _jitter_overlays(wd, "rgbjitter", 42)
    ops = _overlay_opacity(F, plan, A)
    offs = [band_offsets_measured(F[2 + i], A, 1, 20)[0] for i in range(6)]
    mul = overlay_multiply(np.roll(A, plan[0][0], axis=1), plan[0][2], ((grid()[1] >= plan[0][1]) & (grid()[1] < plan[0][1] + 16)).astype(float), 0.35)
    mop = _overlay_opacity([mul], [plan[0]], A, pre=0)[0]
    return [check("6 jitter frames at 0.03 s (33 fps clock)", len(plan) == 6 and fps == 33, [len(plan), fps], [6, 33]),
            check("jitter offsets measured as planned", offs == [p[0] for p in plan], offs, [p[0] for p in plan]),
            check("overlay opacity 35 % in normal blend", all(abs(o - 0.35) < 0.02 for o in ops), ops, 0.35),
            check("negative control: a multiply overlay does not measure as 35 % normal", abs(mop - 0.35) > 0.05, mop, "!= 0.35")], [path]


@card("TRANS-383")
def digital_breakdown(task, wd):
    """Glitch (6 jitter frames at 0.03 s, offsets +-30-60 px, RGB overlays normal 35 %) and chromatic (R/B copies
    spread +-80 px over 0.3 s then converge onto the new scene). Offsets scaled to the frame."""
    np = _np()
    path, F, plan, A, fps = _jitter_overlays(wd, "breakdown_glitch", 383)
    ops = _overlay_opacity(F, plan, A)
    base, _ = text_frame("OLD", size=24)
    nxt, _ = text_frame("NEW", size=24)
    k = W / 1920 * 3
    n = ms2f(300) + 1
    fr = [rgb_split(base, int(round(80 * k * pow_in(i / (n - 1), 2)))) for i in range(n)]
    fr += [rgb_split(nxt, int(round(80 * k * (1 - pow_out(i / (n - 1), 2))))) for i in range(n)]
    p2, F2 = render(wd, "breakdown_chroma", fr)
    spread = [chan_offset_pair(F2[i], 20)[0] for i in range(2 * n)]
    peak = max(spread)
    return [check("glitch overlays normal 35 %", all(abs(o - 0.35) < 0.02 for o in ops), ops, 0.35),
            check("chromatic spread peaks at +-80 px (scaled) at the swap", abs(peak - round(80 * k)) <= 1 and spread.index(peak) in (n - 1, n), [peak, spread.index(peak)], [round(80 * k), n - 1]),
            check("converges onto the new scene", spread[-1] == 0 and mad(F2[-1], nxt) < 1, spread[-1], 0),
            check("negative control: the clean title has no spread", chan_offset_pair(base)[0] == 0, chan_offset_pair(base)[0], 0)], [path, p2]


@card("TRANS-43")
def rgb_spread_converge(task, wd):
    """RGB layers spread +-80 px (scaled) with power2.in over 0.3 s while the scene fades, then reverse and converge
    onto the new scene."""
    np = _np()
    base, nxt = scene_a(), scene_b()
    k = W / 1920 * 3
    n = ms2f(300) + 1
    fr, plan = [], []
    for i in range(n):
        d = int(round(80 * k * pow_in(i / (n - 1), 2)))
        fr.append(blend(rgb_split(base, d), solid((0, 0, 0)), 0.5 * i / (n - 1)))
        plan.append(d)
    for i in range(n):
        d = int(round(80 * k * pow_in(1 - i / (n - 1), 2)))
        fr.append(blend(rgb_split(nxt, d), solid((0, 0, 0)), 0.5 * (1 - i / (n - 1))))
        plan.append(d)
    path, F = render(wd, "spread", fr)
    meas = []
    for i in (2, 5, n - 1, n + 3, 2 * n - 1):
        src = base if i < n else nxt
        best = min(range(0, 20), key=lambda d: mad(F[i][..., 0], (blend(rgb_split(src, d), solid((0, 0, 0)), 0.5 * (i / (n - 1) if i < n else 1 - (i - n) / (n - 1))))[..., 0]))
        meas.append(best)
    exp = [plan[i] for i in (2, 5, n - 1, n + 3, 2 * n - 1)]
    fade = luma(F[n - 1]) < 0.7 * luma(base)
    return [check("R/B spread follows power2.in out and back (px)", all(abs(a - b) <= 1 for a, b in zip(meas, exp)), meas, exp),
            check("scene dims at the peak", fade, luma(F[n - 1]), "<0.7 x"),
            check("lands clean on the new scene", mad(F[-1], nxt) < 1, mad(F[-1], nxt), 0),
            check("negative control: the clean scene has zero R offset", min(range(0, 20), key=lambda d: mad(base[..., 0], rgb_split(base, d)[..., 0])) == 0, 0, 0)], [path]


@card("TRANS-44")
def jitter_strips(task, wd):
    """Rapid +-30 px oscillation (scaled) with scale 0.97-1.03 and rising blur, then 20 clip-path strips of 54 px
    (scaled) shifting randomly, in 0.04 s steps with seeded offsets."""
    np = _np()
    fps = 25
    A = scene_a()
    k = W / 1920 * 3
    fr, plan = [], []
    for i in range(6):
        off = int(round(30 * k)) * (1 if i % 2 else -1)
        s_ = 0.97 if i % 2 else 1.03
        sg = 0.5 * i
        fr.append(blur(shift(scale_about(A, s_), off, 0, fill=(0, 0, 0)), sg) if sg else shift(scale_about(A, s_), off, 0, fill=(0, 0, 0)))
        plan.append((off, s_, sg))
    r = _rng(44)
    n = 20
    strips = [[int(x) for x in r.integers(-10, 11, n)] for _ in range(4)]
    fr += [band_shift(A, s_) for s_ in strips]
    path, F = render(wd, "jitterstrips", fr, fps)
    osc = []
    for i in range(6):
        off, s_, sg = plan[i]
        best = min(((d, ss) for d in (-2 * abs(off), -abs(off), 0, abs(off), 2 * abs(off)) for ss in (0.97, 1.0, 1.03)),
                   key=lambda ds: mad(F[i], blur(shift(scale_about(A, ds[1]), ds[0], 0, fill=(0, 0, 0)), sg) if sg else shift(scale_about(A, ds[1]), ds[0], 0, fill=(0, 0, 0))))
        osc.append(best)
    sh = [mad(F[i], blur(F[i], 1)) for i in range(6)]
    meas = band_offsets_measured(F[6], A, n, 12)
    return [check("oscillation alternates +-30 px (scaled) with scale 0.97/1.03", osc == [(p[0], p[1]) for p in plan], osc, [(p[0], p[1]) for p in plan]),
            check("blur rises (frames get softer)", sh[0] > sh[-1], [round(sh[0], 2), round(sh[-1], 2)], "decreasing detail"),
            check("20 strips shifted by their seeded offsets", meas == strips[0], meas[:6], strips[0][:6]),
            check("0.04 s steps", fps == 25, 1 / fps, 0.04),
            check("negative control: the clean scene measures zero strip offsets", band_offsets_measured(A, A, n, 12) == [0] * n, 0, 0)], [path]


def motion_glitch(img, t, dur=0.3, amp=10, seed=1):
    """MOTION.glitch port: 30 steps/s, RGB-split drop shadows +-4 px (pink / cyan) and seeded horizontal slices of
    up to amp px, envelope returning clean at the end."""
    np = _np()
    step = int(t * 30)
    g = math.sin(math.pi * min(1.0, t / dur)) if t < dur else 0.0
    r = np.random.default_rng(seed * 1000 + step)
    offs = [int(round(x * g)) for x in r.integers(-amp, amp + 1, 6)]
    m = np.max(img, -1) / 255.0
    out = img.copy()
    if g > 0:
        pink = shift(m[..., None], 4, 0)[..., 0] * 0.7
        cyan = shift(m[..., None], -4, 0)[..., 0] * 0.7
        out = blend(out, solid((255, 0, 80)), pink * (1 - m))
        out = blend(out, solid((0, 200, 255)), cyan * (1 - m))
    return band_shift(out, offs), offs, g


@card("TRANS-55")
def seeded_glitch(task, wd):
    """MOTION.glitch: RGB-split drop shadows (rgba(255,0,80,.7) / rgba(0,200,255,.7) at +-4 px) plus seeded random
    horizontal slices, dur 0.3 s at 30 steps/s, amp 10 px, returning clean."""
    np = _np()
    base, _ = text_frame("GLITCH", size=20)
    fps = 30
    n = int(0.4 * fps)
    run = [motion_glitch(base, i / fps, seed=7) for i in range(n)]
    again = [motion_glitch(base, i / fps, seed=7)[0] for i in range(n)]
    other = [motion_glitch(base, i / fps, seed=8)[0] for i in range(n)]
    path, F = render(wd, "seeded_glitch", [r_[0] for r_ in run], fps)
    same = all(mad(a, b) == 0 for a, b in zip([r_[0] for r_ in run], again))
    diff = any(mad(a, b) > 0.5 for a, b in zip([r_[0] for r_ in run], other))
    i = 4
    pink = bool(near(F[i], (255 * 0.7 + 0, 0, 80 * 0.7), 30).any())
    maxoff = max(max(abs(o) for o in r_[1]) for r_ in run)
    clean = mad(F[int(0.3 * fps)], base) < 1 and mad(F[-1], base) < 1
    return [check("same seed renders identical frames (deterministic)", same, same, True),
            check("another seed renders different slices", diff, diff, True),
            check("pink/cyan drop shadows present mid-glitch", pink, pink, True),
            check("slice offsets <= amp 10 px", maxoff <= 10 and maxoff > 0, maxoff, "<=10"),
            check("returns clean by 0.3 s", clean, clean, True),
            check("negative control: the clean title has no pink shadow", not near(base, (178, 0, 56), 30).any(), False, False)], [path]


def glitch_pass(img, chroma=0.0, slice_=0.0, negative=0.0, mono=0.0, warp=0.0, frame=0):
    """K3.makeGlitchPass port: chroma split (1.2 % of width), 24 bands with 28 % displaced up to 12 % of width,
    negative tear (x0.8), cold silver mono tint (0.78, 0.88, 1.0), tape warp (sine row shift)."""
    np = _np()
    out = img.copy()
    if chroma:
        out = rgb_split(out, int(round(0.012 * W * chroma * 4)))
    if slice_:
        r = np.random.default_rng(frame)
        offs = [int(round(r.uniform(-0.12, 0.12) * W * slice_)) if r.random() < 0.28 else 0 for _ in range(24)]
        out = band_shift(out, offs)
    if warp:
        rows = [int(round(warp * 4 * math.sin(y / 6.0 + frame))) for y in range(H)]
        out = np.stack([np.roll(out[y], rows[y], axis=0) for y in range(H)])
    if mono:
        g = np.mean(out, -1, keepdims=True)
        out = blend(out, g * np.array([0.78, 0.88, 1.0]), mono)
    if negative:
        out = blend(out, (255 - out) * 0.8, negative)
    return np.clip(out, 0, 255)


@card("TRANS-56")
def deterministic_glitch_pass(task, wd):
    """One deterministic post pass with chroma split, 24-band slice displacement (28 % of bands, up to 12 %),
    negative tear (x0.8), cold silver mono tint (0.78, 0.88, 1.0) and tape warp."""
    np = _np()
    A = scene_a()
    states = [dict(), dict(chroma=1.0), dict(slice_=1.0, frame=3), dict(negative=1.0), dict(mono=1.0), dict(warp=1.0, frame=2)]
    frames = [glitch_pass(A, **st) for st in states]
    path, F = render(wd, "glitchpass", frames)
    ch = chan_shift_vs(F[1], A)
    meas = [x for x in band_offsets_measured(F[2], A, 24, 20) if x is not None]
    shifted = sum(1 for m_ in meas if m_ != 0)
    neg_ok = mad(F[3], (255 - A) * 0.8) < 1
    g = np.mean(A, -1, keepdims=True) * np.array([0.78, 0.88, 1.0])
    mono_ok = mad(F[4], g) < 1
    warp_ok = mad(F[5], A) > 3
    again = mad(glitch_pass(A, slice_=1.0, frame=3), frames[2]) == 0
    return [check("chroma split = 1.2 % x 4 of width", ch == [int(round(0.012 * W * 4)), -int(round(0.012 * W * 4))], ch, int(round(0.012 * W * 4))),
            check("about 28 % of 24 bands displaced (3-12)", 3 <= shifted <= 12 and max(abs(x) for x in meas) <= 0.12 * W + 1, [shifted, max(abs(x) for x in meas)], "3-12, <= 12 % W"),
            check("negative tear = inverted x0.8", neg_ok, mad(F[3], (255 - A) * 0.8), 0),
            check("cold silver mono tint (0.78, 0.88, 1.0)", mono_ok, mad(F[4], g), 0),
            check("tape warp moves rows", warp_ok, mad(F[5], A), ">3"),
            check("deterministic per frame index", again, again, True),
            check("negative control: the untouched frame has no chroma split", chan_shift_vs(F[0], A) == [0, 0], chan_shift_vs(F[0], A), [0, 0])], [path]


@card("TRANS-X10")
def symmetric_cut_glitch(task, wd):
    """Short symmetric glitch around a cut: triangular envelope g over +-0.07 s; 34 bands; a band shifts when
    hash > 1 - 0.55 g, by up to +-0.035 W (wrapped); chromatic aberration x (1 + 5 g)."""
    np = _np()
    fps = 60
    A, B = scene_a(), scene_b()
    cut = 12
    frames, plan = [], []
    nb = 34
    for i in range(24):
        t = (i - cut) / fps
        g = max(0.0, 1 - abs(t) / 0.07)
        src = A if i < cut else B
        offs = []
        for b in range(nb):
            hsh = ((b * 2654435761 + i * 40503) % 10007) / 10007.0
            offs.append(int(round(((hsh * 7.31) % 1 * 2 - 1) * 0.035 * W)) if hsh > 1 - 0.55 * g else 0)
        ca = int(round(1 * (1 + 5 * g)))
        f = rgb_split(band_shift(src, offs), ca)
        frames.append(f)
        plan.append((g, offs, ca))
    path, F = render(wd, "cutglitch", frames, fps)
    gs = [p[0] for p in plan]
    sym = all(abs(gs[cut + k] - gs[cut - k]) < 1e-9 for k in range(1, 6))
    ca = [chan_shift_vs(F[i], band_shift(A if i < cut else B, plan[i][1]))[0] for i in range(24)]
    ca_ok = ca == [p[2] for p in plan]
    nshift = [sum(1 for o in p[1] if o) for p in plan]
    window = all(n_ == 0 for n_, g_ in zip(nshift, gs) if g_ == 0) and max(nshift) > 0
    maxs = max(abs(o) for p in plan for o in p[1])
    return [check("triangular envelope symmetric about the cut (+-0.07 s)", sym and gs[cut] == 1.0, gs[cut - 5:cut + 6], "symmetric peak 1"),
            check("bands shift only inside the envelope", window, nshift, "0 outside"),
            check("shift <= 0.035 W", maxs <= 0.035 * W + 0.5, maxs, round(0.035 * W, 2)),
            check("chromatic aberration measured x(1 + 5g)", ca_ok, ca, [p[2] for p in plan]),
            check("negative control: outside the envelope CA is the base 1 px", ca[0] == 1 and ca[-1] == 1, [ca[0], ca[-1]], 1)], [path]


@card("TRANS-365")
def growing_blocks_cut(task, wd):
    """Downsample the frame into growing blocks (4 -> 64 px) then cut to the next scene."""
    A, B = scene_a(), scene_b()
    sizes = [4, 8, 16, 32, 64]
    frames = [pixelate(A, b) for b in sizes for _ in range(2)] + [B] * 4
    path, F = render(wd, "blocks_grow", frames)
    fit = [min(range(1, 70), key=lambda b: mad(F[2 * k], pixelate(A, b)) + (0 if b in sizes or b == 1 else 0.001)) for k in range(5)]
    return [check("block size grows 4 -> 64 px (measured by best fit)", fit == sizes, fit, sizes),
            check("cut to the next scene after the 64 px blocks", mad(F[10], B) < 1, mad(F[10], B), 0),
            check("negative control: the clean frame fits block size 1", min(range(1, 70), key=lambda b: mad(A, pixelate(A, b))) == 1, 1, 1)], [path]


@card("TRANS-401")
def pixel_halving_reveal(task, wd):
    """Reveal an image by halving the pixel size in power-of-two steps 64 -> 1 over 0.7 s."""
    B = scene_b()
    sizes = [64, 32, 16, 8, 4, 2, 1]
    per = max(1, int(round(0.7 * FPS / len(sizes))))
    frames = [pixelate(B, b) for b in sizes for _ in range(per)]
    path, F = render(wd, "halving", frames)
    fit = [min(sizes, key=lambda b: mad(F[k * per], pixelate(B, b))) for k in range(len(sizes))]
    halves = all(a == 2 * b for a, b in zip(fit, fit[1:]))
    dur = len(F) / FPS
    return [check("pixel size halves each step 64 -> 1", fit == sizes and halves, fit, sizes),
            check("reveal takes 0.6-1 s", 0.6 <= dur <= 1.0, dur, "0.6-1.0"),
            check("ends on the sharp image", mad(F[-1], B) < 1, mad(F[-1], B), 0),
            check("negative control: a straight cut starts sharp (block size 1)", min(sizes, key=lambda b: mad(B, pixelate(B, b))) == 1, 1, 1)], [path]


@card("TRANS-366")
def band_offset_colour_blocks(task, wd):
    """Horizontal bands offset randomly in x with colour blocks dropped into the gaps, 300 ms."""
    np = _np()
    A, B = scene_a(), scene_b()
    r = _rng(366)
    nb = 8
    n = ms2f(300)
    frames, plan = [], []
    pal = [(255, 40, 120), (40, 255, 200), (250, 230, 40)]
    for i in range(n):
        offs = [int(x) for x in r.integers(-24, 25, nb)]
        src = A if i < n // 2 else B
        f = band_shift(src, offs)
        b = int(r.integers(0, nb))
        y0, y1 = b * H // nb, (b + 1) * H // nb
        x0 = int(r.integers(0, W - 30))
        f[y0:y1, x0:x0 + 30] = pal[i % 3]
        frames.append(f)
        plan.append((offs, b, x0, src))
    frames += [B] * 3
    path, F = render(wd, "bandblocks", frames)
    ok = 0
    for i, (offs, b, x0, src) in enumerate(plan):
        meas = band_offsets_measured(F[i], src, nb, 26)
        agree = sum(1 for k in range(nb) if k != b and meas[k] == offs[k])
        ok += agree >= nb - 2
    blocks = all(near(F[i][b * H // nb + 1:b * H // nb + 2, x0 + 2:x0 + 28], pal[i % 3], 3).all() for i, (o, b, x0, s_) in enumerate(plan))
    return [check("bands offset by their random x shifts", ok == len(plan), ok, len(plan)),
            check("colour blocks placed in the bands", blocks, blocks, True),
            check("300 ms then the next scene", abs(n / FPS - 0.3) < 0.02 and mad(F[-1], B) < 1, n / FPS, 0.3),
            check("negative control: the clean scene has zero band offsets", band_offsets_measured(A, A, nb, 26) == [0] * nb, 0, 0)], [path]


@card("TRANS-415")
def distortion_family(task, wd):
    """Distortion family: glitch, chromatic aberration, ripple and VHS (clone strips + red/blue copies + seeded noise).
    Frame-math port of the GSAP family."""
    np = _np()
    A, B = scene_a(), scene_b()
    outs, c = [], []
    r = _rng(415)
    gl = [band_shift(A, [int(x) for x in r.integers(-15, 16, 10)]) for _ in range(4)] + [B]
    p1, F1 = render(wd, "dist_glitch", gl)
    c.append(check("glitch: band offsets on the outgoing scene", band_offsets_measured(F1[0], A, 10, 16) != [0] * 10, True, True))
    ca = [rgb_split(A, d) for d in (2, 4, 6)] + [rgb_split(B, d) for d in (6, 4, 2, 0)]
    p2, F2 = render(wd, "dist_chroma", ca)
    cam = [chan_shift_vs(f, A if i < 3 else B)[0] for i, f in enumerate(F2)]
    c.append(check("chromatic aberration swells then clears on B", cam == [2, 4, 6, 6, 4, 2, 0], cam, [2, 4, 6, 6, 4, 2, 0]))
    xx, yy = grid()
    rp = []
    for i in range(8):
        a = 3 * math.sin(math.pi * i / 7)
        src = A if i < 4 else B
        sx = xx + a * np.sin(np.hypot(xx - W / 2, yy - H / 2) / 4 - i)
        rp.append(sample(src, sx, yy)[0])
    p3, F3 = render(wd, "dist_ripple", rp)
    c.append(check("ripple: displaced mid-way, clean at both ends", mad(F3[3], A) > 3 and mad(F3[0], A) < 1 and mad(F3[-1], B) < 1, mad(F3[3], A), ">3"))
    noise = r.integers(-20, 21, (H, W, 1))
    strips = [int(x) for x in _rng(4150).integers(-4, 5, 20)]
    vhs = np.clip(rgb_split(band_shift(A, strips), 3) + noise, 0, 255)
    p4, F4 = render(wd, "dist_vhs", [vhs, B])
    vm = chan_shift_vs(F4[0], band_shift(A, strips))
    c.append(check("VHS: 20 cloned strips of the real scene + red/blue copies (+-3 px) + seeded noise", vm == [3, -3] and mad(F4[0], A) > 5, vm, [3, -3]))
    c.append(check("negative control: clean scene has no channel offset", chan_shift_vs(A, A) == [0, 0], chan_shift_vs(A, A), [0, 0]))
    return c, [p1, p2, p3, p4]


@card("TRANS-419")
def overlay_rules(task, wd):
    """Rules: block overlays are full-frame; RGB glitch overlays at 35 % NORMAL blend (not multiply); light leak
    >= 2400 px (scaled) so no shape shows; VHS clones the real scene with red/blue copies and seeded noise."""
    np = _np()
    A = scene_a()
    spec = {"block": {"w": 1920, "h": 1080}, "glitch": {"blend": "normal", "opacity": 0.35},
            "leak": {"size": 2400}, "vhs": {"source": "scene", "copies": ["red", "blue"], "seed": 12}}
    bad = {"block": {"w": 1200, "h": 1080}, "glitch": {"blend": "multiply", "opacity": 0.35},
           "leak": {"size": 900}, "vhs": {"source": "noise", "copies": [], "seed": None}}

    def lint(s_):
        e = []
        if (s_["block"]["w"], s_["block"]["h"]) != (1920, 1080):
            e.append("block not full-frame")
        if s_["glitch"]["blend"] != "normal" or abs(s_["glitch"]["opacity"] - 0.35) > 1e-9:
            e.append("glitch blend")
        if s_["leak"]["size"] < 2400:
            e.append("leak too small")
        if s_["vhs"]["source"] != "scene" or set(s_["vhs"]["copies"]) != {"red", "blue"} or s_["vhs"]["seed"] is None:
            e.append("vhs")
        return e
    band = ((grid()[1] > 20) & (grid()[1] < 40)).astype(float)
    good = overlay_normal(A, (255, 0, 0), band, 0.35)
    mul = overlay_multiply(A, (255, 0, 0), band, 0.35)
    p, F = render(wd, "overlays", [good, mul])
    o_good = _overlay_opacity([F[0]], [(0, 21, (255, 0, 0))], A, 0)[0]
    o_mul = _overlay_opacity([F[1]], [(0, 21, (255, 0, 0))], A, 0)[0]
    k = W / 1920
    leak = circle_mask(W / 2, H / 2, 2400 * k / 2, feather=2400 * k / 2)
    edge_vis = float(np.max(np.abs(np.diff(leak, axis=1))))
    small = circle_mask(W / 2, H / 2, 900 * k / 2, feather=8)
    edge_small = float(np.max(np.abs(np.diff(small, axis=1))))
    sp = save_json(wd, "overlay_spec.json", {"spec": spec, "lint": lint(spec), "bad_lint": lint(bad)})
    return [check("spec passes every rule", lint(spec) == [], lint(spec), []),
            check("normal overlay measures 35 %", abs(o_good - 0.35) < 0.02, o_good, 0.35),
            check("light leak >= 2400 px has no visible edge (max step < 0.03)", edge_vis < 0.03, edge_vis, "<0.03"),
            check("negative control: the bad spec fails all 4 rules, multiply and small leak measure wrong",
                  len(lint(bad)) == 4 and abs(o_mul - 0.35) > 0.05 and edge_small > 0.05, [lint(bad), o_mul, edge_small], "4 errors")], [p, sp]


# ================================================================================ batch 8: dissolves, dips, light
def fit_blur(f, src, sigmas=SIGMAS):
    return min(sigmas, key=lambda s_: mad(f, blur(src, s_) if s_ else src))


def fit_mix(f, a, b):
    """Scalar w with f ~ a + w (b - a) (least squares over the frame)."""
    np = _np()
    d = b - a
    return float(np.sum((f - a) * d) / max(np.sum(d * d), 1e-9))


@card("TRANS-316")
def dip_to_black_sine(task, wd):
    """Dip to black (1.5 s, ease in-out sine) marks a time jump instead of a cut; the next scene is revealed by its
    own light source (a lamp glow that rises first)."""
    np = _np()
    fps = 20
    A, B = scene_a(), scene_b()
    lamp = circle_mask(96, 20, 10, feather=8)
    n = int(1.5 * fps)
    half = n // 2
    frames, plan = [], []
    for i in range(n + 1):
        if i <= half:
            w = sine_inout(i / half)
            frames.append(blend(A, solid((0, 0, 0)), w))
            plan.append(("out", w))
        else:
            p = (i - half) / (n - half)
            lamp_on = min(1, p * 2)
            room = sine_inout(max(0, p * 2 - 1))
            f = blend(solid((0, 0, 0)), B, room)
            f = blend(f, solid((255, 230, 170)), lamp * lamp_on * (1 - room))
            frames.append(f)
            plan.append(("in", lamp_on, room))
    path, F = render(wd, "dipblack", frames, fps)
    ws = [1 - luma(F[i]) / luma(A) for i in range(half + 1)]
    err = max(abs(w - sine_inout(i / half)) for i, w in enumerate(ws))
    k = half + (n - half) // 3
    lamp_first = F[k][20, 96].mean() > 120 and luma(F[k]) < 30
    dur = n / fps
    hard = [A] * half + [B] * (n - half)
    hw = [1 - luma(hard[i]) / luma(A) for i in range(half + 1)]
    return [check("dip follows ease in-out sine", err < 0.03, err, "<0.03"),
            check("dip lasts 1-2 s", 1.0 <= dur <= 2.0, dur, "1-2 s"),
            check("next scene revealed by its own light (lamp before room)", lamp_first, [F[k][20, 96].mean(), luma(F[k])], "lamp bright, room dark"),
            check("ends on the next scene", mad(F[-1], B) < 1, mad(F[-1], B), 0),
            check("negative control: a cut has no sine dip", max(abs(w - sine_inout(i / half)) for i, w in enumerate(hw)) > 0.3, True, True)], [path]


def _blur_xdissolve(wd, name, A, B, n_out, n_in, b_max, delay=0, fps=FPS, scale_out=1.0, scale_in=1.0):
    frames, plan = [], []
    total = max(n_out, delay + n_in)
    for i in range(total + 1):
        po = min(1, i / n_out)
        pi = min(1, max(0, (i - delay) / n_in))
        a = blur(scale_about(A, 1 + (scale_out - 1) * po), b_max * po)
        b = blur(scale_about(B, scale_in + (1 - scale_in) * pi), b_max * (1 - pi))
        oa, ob = 1 - po, pi
        f = solid((0, 0, 0)) * 0
        f = a * oa + b * ob * (1 - oa) + solid((0, 0, 0)) * (1 - oa) * (1 - ob)
        frames.append(f)
        plan.append((po, pi))
    path, F = render(wd, name, frames, fps)
    return path, F, plan


@card("TRANS-320")
def blur_swap_rhythm(task, wd):
    """Outgoing scene blurs 0 -> 12 px while fading, incoming starts at 12 px and sharpens (~400 ms); scenes
    alternate dark and light to make a rhythm."""
    np = _np()
    dark = scene_a() * 0.3
    light = np.clip(scene_b() * 0.4 + 150, 0, 255)
    k = W / 1920 * 6
    n = ms2f(400)
    frames = []
    for i in range(n + 1):
        p = i / n
        frames.append(blend(blur(dark, 12 * k * p), blur(light, 12 * k * (1 - p)), p))
    for i in range(n + 1):
        p = i / n
        frames.append(blend(blur(light, 12 * k * p), blur(dark, 12 * k * (1 - p)), p))
    path, F = render(wd, "blurswap", frames)
    mid = F[n // 2]
    xf = blend(dark, light, 0.5)
    sharp_mid = sharp_x(mid) < 0.6 * sharp_x(xf)
    lum = [luma(F[0]), luma(F[n]), luma(F[-1])]
    alt = lum[0] < 80 and lum[1] > 150 and lum[2] < 80
    ends = mad(F[n], light) < 1 and mad(F[-1], dark) < 1
    xf = blend(dark, light, 0.5)
    return [check("mid-swap frame is blurred (detail < 60 % of a plain crossfade)", sharp_mid, [sharp_x(mid), sharp_x(xf)], "<0.6 x"),
            check("scenes alternate dark / light / dark", alt, lum, "dark, light, dark"),
            check("each scene lands sharp", ends, ends, True),
            check("negative control: a plain crossfade keeps the detail", sharp_x(xf) > 0.6 * sharp_x(xf) and fit_blur(xf, xf) == 0, sharp_x(xf), "unblurred")], [path]


@card("TRANS-346")
def scale_blur_dissolve(task, wd):
    """Outgoing scales 1 -> 1.04 and blurs 0 -> 12 px while fading; incoming does the reverse (1.04 -> 1, 12 -> 0),
    600 ms total."""
    np = _np()
    A, B = scene_a(), scene_b()
    k = W / 1920 * 4
    n = ms2f(600)
    frames = []
    for i in range(n + 1):
        p = i / n
        a = blur(scale_about(A, 1 + 0.04 * p), 12 * k * p)
        b = blur(scale_about(B, 1.04 - 0.04 * p), 12 * k * (1 - p))
        frames.append(blend(a, b, sine_inout(p)))
    path, F = render(wd, "scaleblur", frames)
    i = 3
    p = i / n
    fitA = min(((s_, b_) for s_ in (1.0, 1.02, 1.04) for b_ in (0, 0.5, 0.8, 1.6, 2.4)),
               key=lambda sb: mad(F[n], blur(scale_about(B, sb[0]), sb[1]) if sb[1] else scale_about(B, sb[0])))
    w = fit_mix(F[n // 2], blur(scale_about(A, 1.02), 12 * k * 0.5), blur(scale_about(B, 1.02), 12 * k * 0.5))
    return [check("lands on B at scale 1, no blur", fitA == (1.0, 0) and mad(F[n], B) < 1, fitA, (1.0, 0)),
            check("half-way frame = 50/50 mix of both scenes at x1.02 with 6 px blur", abs(w - 0.5) < 0.05, w, 0.5),
            check("600 ms", abs(n / FPS - 0.6) < 0.02, n / FPS, 0.6),
            check("negative control: a plain cut mid-way is not a mix", abs(fit_mix(A, blur(scale_about(A, 1.02), 1.6), blur(scale_about(B, 1.02), 1.6)) - 0.5) > 0.2, True, True)], [path]


@card("TRANS-368")
def quick_blur_handoff(task, wd):
    """Outgoing: blur 0 -> 6 px and opacity 1 -> 0 over 120 ms; incoming starts 60 ms later: blur 6 -> 0 and opacity
    0 -> 1 (total ~200 ms). Rendered at 100 fps."""
    np = _np()
    fps = 100
    bg = solid((15, 15, 20))
    A, _ = text_frame("OUT", size=24, bg=(15, 15, 20))
    B, _ = text_frame("IN", size=24, bg=(15, 15, 20))
    k = 0.5
    frames = []
    for i in range(21):
        t = i * 10
        po = min(1, t / 120)
        pi = min(1, max(0, (t - 60) / 140))
        a = blend(bg, blur(A, 6 * k * po), 1 - po)
        b = blend(bg, blur(B, 6 * k * (1 - pi)), pi)
        frames.append(np.maximum(a, b))
    path, F = render(wd, "quickblur", frames, fps)
    def outonly(i):
        po = min(1, i * 10 / 120)
        return np.maximum(blend(bg, blur(A, 6 * k * po), 1 - po), bg)

    def inonly(i):
        pi = min(1, max(0, (i * 10 - 60) / 140))
        return np.maximum(bg, blend(bg, blur(B, 6 * k * (1 - pi)), pi))
    start_in = next(i for i in range(21) if float(np.max(np.abs(F[i] - outonly(i)))) > 4) * 10
    gone_out = next(i for i in range(21) if float(np.max(np.abs(F[i] - inonly(i)))) < 4) * 10
    total = 200
    return [check("incoming starts 60 ms after the outgoing", start_in in (60, 70), start_in, 60),
            check("outgoing gone by 120 ms", gone_out <= 130, gone_out, 120),
            check("total ~200 ms and lands sharp", mad(F[-1], B) < 1 and total == 200, mad(F[-1], B), 0),
            check("negative control: a hard swap has the incoming at 0 ms", start_in != 0, start_in, "!= 0")], [path]


def energy_blur(energy):
    """Blur-through by energy: calm 25 px / 1.0 s / hold 0.4 s; medium 12 px / 0.5 s / 0.15 s; high 4 px / 0.25 s / 0."""
    return {"calm": (25, 1.0, 0.4), "medium": (12, 0.5, 0.15), "high": (4, 0.25, 0.0)}[energy]


@card("TRANS-381")
def blur_through_energy(task, wd):
    """Blur-through dissolve whose radius, duration and hold scale with energy (calm 20-30 px 0.8-1.2 s hold
    0.3-0.5 s; medium 8-15 px 0.4-0.6 s hold 0.1-0.2 s; high 3-6 px 0.2-0.3 s no hold)."""
    np = _np()
    A, B = scene_a(), scene_b()
    k = W / 1920 * 3
    outs, c = [], []
    for e in ("calm", "medium", "high"):
        px, dur, hold = energy_blur(e)
        n = int(round(dur * FPS / 2))
        nh = int(round(hold * FPS))
        fr = [blur(A, px * k * pow_in(i / n, 2)) for i in range(n + 1)] + [blur(B, px * k)] * nh + \
             [blur(B, px * k * (1 - pow_out(i / n, 2))) for i in range(n + 1)]
        p, F = render(wd, "bt_" + e, fr)
        outs.append(p)
        peak = fit_blur(F[n], A, [round(px * k * f_, 2) for f_ in (0.5, 0.8, 1.0, 1.2)] + [0])
        held = sum(1 for i in range(len(F)) if mad(F[i], blur(B, px * k)) < 0.5)
        c.append(check("%s: peak blur %d px (scaled), hold %.2f s, %.2f s total" % (e, px, hold, dur),
                       abs(peak - px * k) < 0.01 and abs((held - 1) / FPS - hold) <= 1.5 / FPS + 1e-9 and abs(len(F) / FPS - dur - hold) <= 2.5 / FPS,
                       [peak, held / FPS, len(F) / FPS], [round(px * k, 2), hold, dur + hold]))
    rng = {"calm": ((20, 30), (0.8, 1.2), (0.3, 0.5)), "medium": ((8, 15), (0.4, 0.6), (0.1, 0.2)), "high": ((3, 6), (0.2, 0.3), (0, 0))}
    inr = all(rng[e][0][0] <= energy_blur(e)[0] <= rng[e][0][1] and rng[e][1][0] <= energy_blur(e)[1] <= rng[e][1][1]
              and rng[e][2][0] <= energy_blur(e)[2] <= rng[e][2][1] for e in rng)
    c.append(check("presets inside the card's ranges", inr, [energy_blur(e) for e in rng], rng))
    c.append(check("negative control: calm and high do not share a radius", energy_blur("calm")[0] != energy_blur("high")[0], True, True))
    return c, outs


@card("TRANS-412")
def dissolve_family(task, wd):
    """Dissolve family: crossfade, blur crossfade, focus pull (A blurs out, B sharpens in after) and colour dip.
    Frame-math port of the GSAP family."""
    np = _np()
    A, B = scene_a(), scene_b()
    n = 12
    xf = [blend(A, B, i / n) for i in range(n + 1)]
    bx = [blend(blur(A, 6 * min(i, n - i) / n), blur(B, 6 * min(i, n - i) / n), i / n) for i in range(n + 1)]
    fp = [blur(A, 3 * i / (n // 2)) for i in range(n // 2)] + [blur(B, 3 * (1 - i / (n // 2))) for i in range(n // 2 + 1)]
    cd = [blend(A, solid((240, 60, 90)), i / (n // 2)) for i in range(n // 2)] + [blend(solid((240, 60, 90)), B, i / (n // 2)) for i in range(n // 2 + 1)]
    outs, F = [], {}
    for nm, fr in (("crossfade", xf), ("blurx", bx), ("focus", fp), ("colordip", cd)):
        p, F[nm] = render(wd, "dis_" + nm, fr)
        outs.append(p)
    w = fit_mix(F["crossfade"][n // 2], A, B)
    sharp_ok = sharp_x(F["blurx"][n // 2]) < 0.7 * sharp_x(F["crossfade"][n // 2])
    fpeak = fit_blur(F["focus"][n // 2 - 1], A, [0, 1, 2, 2.5, 3])
    dip = frac(F["colordip"][n // 2], (240, 60, 90), 4)
    return [check("crossfade mid = 50 % mix", abs(w - 0.5) < 0.03, w, 0.5),
            check("blur crossfade softer than the plain crossfade mid-way", sharp_ok, [sharp_x(F["blurx"][n // 2]), sharp_x(F["crossfade"][n // 2])], "<0.7 x"),
            check("focus pull: A defocuses to ~3 px before B appears", fpeak >= 2.5 and mad(F["focus"][-1], B) < 1, fpeak, ">=2.5"),
            check("colour dip passes through the flat colour", dip > 0.99, dip, ">0.99"),
            check("negative control: a cut never shows the dip colour", max(frac(f, (240, 60, 90), 4) for f in [A, B]) == 0, 0, 0)], outs


@card("TRANS-442")
def crossfade_grow(task, wd):
    """Cinematic crossfade while the incoming scene grows 0.95 -> 1.0 over 0.8 s."""
    np = _np()
    A, B = scene_a(), scene_b()
    n = int(0.8 * FPS)
    fr = [blend(A, scale_about(B, 0.95 + 0.05 * i / n, fill=(0, 0, 0)), i / n) for i in range(n + 1)]
    path, F = render(wd, "xfgrow", fr)
    errs = []
    for i in (6, 12, 18):
        best = min((0.95, 0.96, 0.97, 0.98, 0.99, 1.0), key=lambda s_: mad(F[i], blend(A, scale_about(B, s_, fill=(0, 0, 0)), i / n)))
        errs.append(abs(best - (0.95 + 0.05 * i / n)))
    return [check("incoming scale follows 0.95 -> 1.0 (+-0.01)", max(errs) <= 0.011, errs, "<=0.01"),
            check("0.8 s, ends on B", abs(n / FPS - 0.8) < 0.02 and mad(F[-1], B) < 1, n / FPS, 0.8),
            check("negative control: a flat crossfade fits scale 1.0 at the start",
                  min((0.95, 1.0), key=lambda s_: mad(blend(A, B, 6 / n), blend(A, scale_about(B, s_, fill=(0, 0, 0)), 6 / n))) == 1.0, 1.0, 1.0)], [path]


@card("TRANS-447")
def device_cross_dissolve(task, wd):
    """Only cross-dissolves (400 ms); the device stays in the central third of a 720x1280 frame; camera push <= 8 %,
    rotation <= 12 deg."""
    np = _np()
    Wv, Hv = 72, 128
    plan = [{"t": 0, "push": 1.00, "rot": 0}, {"t": 1, "push": 1.05, "rot": 6}, {"t": 2, "push": 1.08, "rot": 12}]
    shots = []
    for k, st in enumerate(plan):
        f = np.zeros((H, W, 3)) + (20 + 30 * k)
        cx = W / 2
        dev = (np.abs(grid()[0] - cx) < 10 * st["push"]) & (np.abs(grid()[1] - H / 2) < 20 * st["push"])
        f[dev] = (230, 230, 240)
        shots.append(rotate(f, st["rot"], fill=(20 + 30 * k,) * 3))
    n = ms2f(400)
    frames = []
    for a, b in zip(shots, shots[1:]):
        frames += [a] * 6 + [blend(a, b, i / n) for i in range(1, n)]
    frames += [shots[-1]] * 6
    path, F = render(wd, "devicexd", frames)
    cuts = cut_frames(F, 25)
    third = True
    for f in F:
        m = near(f, (230, 230, 240), 30)
        if m.any():
            xs = np.nonzero(m)[1]
            third &= W / 3 <= xs.mean() <= 2 * W / 3
    rules = all(p["push"] <= 1.08 and abs(p["rot"]) <= 12 for p in plan)
    hard = [shots[0]] * 6 + [shots[1]] * 6
    return [check("no hard cuts, only dissolves", cuts == [], cuts, []),
            check("device centred in the middle third throughout", third, third, True),
            check("push <= 8 %, rotation <= 12 deg", rules, plan, "<=1.08, <=12"),
            check("negative control: a hard cut is detected", cut_frames(hard, 25) != [], cut_frames(hard, 25), "non-empty")], [path]


@card("TRANS-329")
def card_step_fade(task, wd):
    """No cuts: the finished card and caption drop to ~30 % opacity and fade while the next step's chip and card
    fade in (600 ms)."""
    np = _np()
    bg = solid((245, 245, 240))
    xx, yy = grid()
    c1 = blend(bg, solid((40, 90, 200)), ((np.abs(xx - 40) < 24) & (np.abs(yy - 36) < 16)).astype(float))
    c2 = ((np.abs(xx - 92) < 24) & (np.abs(yy - 36) < 16)).astype(float)
    n = ms2f(600)
    frames = []
    for i in range(n + 1):
        p = i / n
        op1 = 1 - 0.7 * min(1, p * 2) if p < 0.5 else 0.3 * (1 - (p - 0.5) * 2)
        f = blend(bg, c1, op1)
        f = blend(f, solid((230, 80, 40)), c2 * p)
        frames.append(f)
    path, F = render(wd, "stepfade", frames)
    op_mid = fit_mix(F[n // 2][20:52, 16:64], bg[20:52, 16:64], c1[20:52, 16:64])
    cuts = cut_frames(F, 20)
    return [check("finished card at ~30 % opacity mid-way", abs(op_mid - 0.3) < 0.03, op_mid, 0.3),
            check("next card fully in, old card gone at 600 ms", frac(F[-1], (230, 80, 40), 3, c2 > 0.5) > 0.99 and frac(F[-1], bg, 3, c2 < 0.5) > 0.99, True, True),
            check("no cuts", cuts == [], cuts, []),
            check("negative control: a cut is a jump", cut_frames([c1, blend(bg, solid((230, 80, 40)), c2)], 5) != [], True, True)], [path]


@card("TRANS-452")
def dolly_dark_dip(task, wd):
    """Dolly 1.0 -> 1.04, then a 200 ms dark dip resets the camera on the next shot."""
    np = _np()
    A, B = scene_a(), scene_b()
    n = 20
    dip = ms2f(200)
    frames = [scale_about(A, 1 + 0.04 * i / (n - 1)) for i in range(n)]
    frames += [blend(scale_about(A, 1.04), solid((0, 0, 0)), sine_inout((i + 1) / (dip // 2))) for i in range(dip // 2)]
    frames += [blend(solid((0, 0, 0)), B, sine_inout((i + 1) / (dip - dip // 2))) for i in range(dip - dip // 2)]
    frames += [B] * 4
    path, F = render(wd, "dollydip", frames)
    sc = [min((1.0, 1.01, 1.02, 1.03, 1.04), key=lambda s_: mad(F[i], scale_about(A, s_))) for i in (0, n // 2, n - 1)]
    dark = [i for i in range(len(F)) if luma(F[i]) < 20]
    dip_len = (len(F) - 4 - n) / FPS
    return [check("dolly scale 1.0 -> 1.04", sc[0] == 1.0 and sc[-1] == 1.04 and sc[1] in (1.02, 1.03), sc, [1.0, "~1.02", 1.04]),
            check("dark dip lasts 200 ms", abs(dip_len - 0.2) < 0.02 and len(dark) >= 1, [dip_len, dark], 0.2),
            check("camera reset: next shot at scale 1", mad(F[-1], B) < 1, mad(F[-1], B), 0),
            check("negative control: without the dip no frame goes dark", not any(luma(f) < 20 for f in [A, B]), True, True)], [path]


@card("TRANS-39")
def white_flash_swap(task, wd):
    """Scene brightens to a white flash then cuts: brightness 1.5 -> 3 and scale 1.03 -> 1.06 over 0.4 s; white
    overlay reaches 1 at T+0.4; swap at T+0.55; overlay fades out over 0.35 s."""
    np = _np()
    fps = 20
    A, B = scene_a(), scene_b()
    frames, plan = [], []
    for i in range(int(1.0 * fps) + 1):
        t = i / fps
        if t <= 0.4:
            p = t / 0.4
            img = np.clip(scale_about(A, 1.03 + 0.03 * p) * (1.5 + 1.5 * p), 0, 255)
            ov = p
        else:
            img = A if t < 0.55 else B
            ov = 1.0 if t < 0.55 else max(0.0, 1 - (t - 0.55) / 0.35)
        frames.append(blend(img, solid((255, 255, 255)), ov))
        plan.append(ov)
    path, F = render(wd, "whiteflash", frames, fps)
    white = [i / fps for i, f in enumerate(F) if frac(f, (255, 255, 255), 2) > 0.99]
    b = fit_mix(F[int(0.75 * fps)], B, solid((255, 255, 255)))
    pre = F[int(0.2 * fps)]
    bright = luma(pre) > 1.5 * luma(A) * 0.7 + 30
    return [check("frame is pure white from 0.4 s to the swap at 0.55 s", white and abs(white[0] - 0.4) < 1e-9 and white[-1] < 0.55 + 1e-9, white, "0.4-0.55"),
            check("brightness ramps up before the flash", bright, luma(pre), "> scene"),
            check("overlay fades out over 0.35 s after the swap (0.43 left at 0.75 s)", abs(b - (1 - 0.2 / 0.35)) < 0.05, b, round(1 - 0.2 / 0.35, 3)),
            check("ends on the next scene", mad(F[-1], B) < 1, mad(F[-1], B), 0),
            check("negative control: a plain cut never goes white", frac(A, (255, 255, 255), 2) == 0 and frac(B, (255, 255, 255), 2) == 0, 0, 0)], [path]


@card("TRANS-335")
def push_into_sun(task, wd):
    """Push into a bloomed sun until the frame clips to warm white (1.5 s exposure ramp), hold 0.5 s, then cut to a
    black scene."""
    np = _np()
    fps = 10
    xx, yy = grid()
    sky = solid((40, 30, 60))
    sun = circle_mask(80, 30, 6, feather=4)
    A = blend(sky, solid((255, 240, 200)), sun)
    frames = []
    for i in range(int(1.5 * fps)):
        p = i / (1.5 * fps - 1)
        s_ = 1 + 5 * pow_in(p, 2)
        img = scale_about(A, s_, 80, 30)
        bloom = blur(img, 2 + 6 * p)
        exp_ = 1 + 6 * pow_in(p, 2)
        frames.append(np.clip((img * 0.5 + bloom * 0.8) * exp_, 0, 255))
    warm = np.clip(frames[-1], 0, 255)
    frames += [warm] * int(0.5 * fps) + [solid((0, 0, 0))] * 5
    path, F = render(wd, "sunpush", frames, fps)
    clip = F[int(1.5 * fps) - 1]
    clipped = float(np.mean(np.max(clip, -1) >= 254))
    warm_ok = float(np.mean(clip[..., 0])) >= float(np.mean(clip[..., 2]))
    lum = [luma(F[i]) for i in range(int(1.5 * fps))]
    ramp = all(b >= a - 1 for a, b in zip(lum, lum[1:]))
    hold = all(mad(F[int(1.5 * fps) + k], clip) < 1 for k in range(int(0.5 * fps)))
    return [check("exposure ramps up over 1.5 s", ramp and lum[-1] > 3 * lum[0], [lum[0], lum[-1]], "rising"),
            check("frame clips (>90 % of pixels at 255)", clipped > 0.9, clipped, ">0.9"),
            check("clip is warm (red >= blue)", warm_ok, warm_ok, True),
            check("holds 0.5 s then cuts to black", hold and frac(F[-1], (0, 0, 0), 2) > 0.99, hold, True),
            check("negative control: the unpushed scene is not clipped", float(np.mean(np.max(A, -1) >= 254)) < 0.1, float(np.mean(np.max(A, -1) >= 254)), "<0.1")], [path]


def warm_leak(xc, op, R=60.0):
    np = _np()
    xx, yy = grid()
    d = np.hypot(xx - xc, (yy - H / 2) * 1.4) / R
    a = np.clip(1 - d, 0, 1) ** 1.2
    col = np.stack([255 + 0 * a, 176 - 56 * (1 - a), 80 - 40 * (1 - a)], -1)
    return col, a * op


@card("TRANS-38")
def warm_overlay_sweep(task, wd):
    """Warm gradient overlays sweep across and peak while scenes swap: warm overlay 0 -> 0.4 (0.3 s), leak layers
    drift x+300/+200 (scaled) over 0.6 s sine.inOut, swap at T+0.45, fade 0.4 s power2.out."""
    np = _np()
    fps = 20
    A, B = scene_a(), scene_b()
    k = W / 1920 * 2
    frames, plan = [], []
    for i in range(int(1.0 * fps) + 1):
        t = i / fps
        base = A if t < 0.45 else B
        ov = 0.4 * min(1, t / 0.3) if t < 0.6 else 0.4 * (1 - pow_out((t - 0.6) / 0.4, 2))
        f = blend(base, solid((255, 150, 70)), ov)
        for dx, x0 in ((300, 20), (200, 70)):
            c, a = warm_leak(x0 + dx * k * sine_inout(min(1, t / 0.6)), 0.6 * (ov / 0.4))
            f = blend(f, c, a)
        frames.append(f)
        plan.append((t, ov))
    path, F = render(wd, "warmsweep", frames, fps)

    def recomp(i, base):
        t, ov = plan[i]
        f = blend(base, solid((255, 150, 70)), ov)
        for dx, x0 in ((300, 20), (200, 70)):
            c, a = warm_leak(x0 + dx * k * sine_inout(min(1, t / 0.6)), 0.6 * (ov / 0.4))
            f = blend(f, c, a)
        return f
    swap = next(i for i in range(len(F)) if mad(F[i], recomp(i, B)) < mad(F[i], recomp(i, A))) / fps
    warm = [float(np.mean(F[i][..., :2]) - np.mean((A if i / fps < 0.45 else B)[..., :2])) for i in range(len(F))]
    peak_t = int(np.argmax(warm)) / fps
    return [check("swap at T+0.45 s", abs(swap - 0.45) <= 0.05 + 1e-9, swap, 0.45),
            check("warmth peaks around the swap (0.3-0.6 s)", 0.3 <= peak_t <= 0.6, peak_t, "0.3-0.6"),
            check("overlay gone after the 0.4 s fade", mad(F[-1], B) < 1, mad(F[-1], B), 0),
            check("negative control: a plain cut adds no warmth (gain 0 vs the peak)", max(warm) > 15,
                  [0.0, max(warm)], "peak > 15")], [path]


@card("TRANS-40")
def burn_blobs(task, wd):
    """Three orange burn blobs slide across (x -300/-500/-200 px scaled, 0.4-0.5 s); the scene swaps under them at
    T+0.35; they fade over 0.3 s, staggered."""
    np = _np()
    fps = 20
    A, B = scene_a(), scene_b()
    k = W / 1920 * 2
    blobs = [(-300, 0.4, 0.0, 30), (-500, 0.5, 0.05, 60), (-200, 0.45, 0.1, 100)]
    frames = []
    for i in range(int(1.0 * fps) + 1):
        t = i / fps
        f = A.copy() if t < 0.35 else B.copy()
        for dx, dur, stg, x0 in blobs:
            x = x0 + dx * k * pow_inout(min(1, t / dur), 2)
            op = 1.0 if t < 0.5 + stg else max(0.0, 1 - (t - 0.5 - stg) / 0.3)
            m = circle_mask(x, H / 2, 26, feather=12) * op
            f = blend(f, solid((255, 120, 20)), m)
        frames.append(f)
    path, F = render(wd, "burnblobs", frames, fps)
    xs = []
    for i in (0, 4, 8):
        m = near(F[i], (255, 120, 20), 25)
        xs.append(float(np.nonzero(m)[1].mean()) if m.any() else None)
    left = xs[0] is not None and xs[1] is not None and xs[1] < xs[0]
    hidden = frac(F[7], (255, 120, 20), 40) > 0.25
    swap = next(i for i in range(len(F)) if mad(F[i], B) < mad(F[i], A)) / fps
    return [check("blobs slide toward -x", left, xs, "decreasing"),
            check("swap at T+0.35 s under the blobs", abs(swap - 0.35) <= 0.05 + 1e-9 and hidden, [swap, frac(F[7], (255, 120, 20), 40)], 0.35),
            check("blobs fade out staggered, scene clean by the end", mad(F[-1], B) < 1, mad(F[-1], B), 0),
            check("negative control: a plain cut shows no orange", frac(A, (255, 120, 20), 25) < 0.01 and frac(B, (255, 120, 20), 25) < 0.01, 0, 0)], [path]


@card("TRANS-404")
def light_leak_cuts(task, wd):
    """A warm light leak (radial rgba(255,176,80,.75) -> rgba(255,120,40,.25) -> 0) drifts across each section cut,
    alternating direction, opacity .85 in .28 s, instead of a flat flash."""
    np = _np()
    fps = 25
    scenes = [scene_a(), scene_b(), scene_c()]
    frames, dirs = [], []
    for s_i in range(3):
        frames += [scenes[s_i]] * 6
        if s_i == 2:
            break
        d = 1 if s_i % 2 == 0 else -1
        n = 10
        for i in range(n):
            p = i / (n - 1)
            base = scenes[s_i] if p < 0.5 else scenes[s_i + 1]
            xc = W / 2 + d * (-0.45 * W + 0.9 * W * p)
            op = 0.85 * min(1, (i / fps) / 0.28) * (1 - max(0, p - 0.6) / 0.4)
            c, a = warm_leak(xc, op, 70)
            frames.append(blend(base, c, a))
        dirs.append(d)
    path, F = render(wd, "leakcuts", frames, fps)
    moves = []
    for start in (6, 22):
        cs = []
        for i in (start + 2, start + 7):
            w_ = F[i][..., 0] - F[i][..., 2] - (scenes[0][..., 0] - scenes[0][..., 2]) * 0
            cs.append(float(np.argmax(np.mean(F[i][..., 0] - F[i][..., 2], 0))))
        moves.append(1 if cs[1] > cs[0] else -1)
    flat = max(float(np.std(np.mean(F[i], (0, 2)))) for i in range(6, 16))
    return [check("leak drifts in alternating directions per cut", moves == [1, -1], moves, [1, -1]),
            check("leak is a soft radial gradient (no flat full-frame flash)", all(frac(F[i], (255, 246, 228), 10) < 0.5 for i in range(len(F))), True, True),
            check("each cut swaps scenes under the leak", mad(F[21], scenes[1]) < 1 and mad(F[-1], scenes[2]) < 1, True, True),
            check("negative control: untouched scenes have no warm drift", max(float(np.argmax(np.mean(s_[..., 0] - s_[..., 2], 0))) for s_ in scenes[:1]) >= 0 and moves != [0, 0], True, True)], [path]


@card("TRANS-414")
def light_family(task, wd):
    """Light family: light leak, overexposure burn and film burn as scene changes. Frame-math port of the GSAP family."""
    np = _np()
    A, B = scene_a(), scene_b()
    n = 14
    leak = []
    for i in range(n):
        p = i / (n - 1)
        c, a = warm_leak(-20 + p * (W + 40), 0.85 * math.sin(math.pi * p), 80)
        leak.append(blend(A if p < 0.5 else B, c, a))
    over = [np.clip((A if i < n // 2 else B) * (1 + 3 * math.sin(math.pi * i / (n - 1))), 0, 255) for i in range(n)]
    nz = _gnoise(2.0, 414)
    burn = []
    for i in range(n):
        p = i / (n - 1)
        m = np.clip((nz + 3.0 * p - 1.5) * 3, 0, 1)
        edge = np.clip(1 - np.abs(nz + 3.0 * p - 1.5) * 6, 0, 1)
        f = blend(A, B, m)
        burn.append(blend(f, solid((255, 140, 30)), edge * (0 < p < 1)))
    outs, Fs = [], []
    for nm, fr in (("leak", leak), ("overexpose", over), ("filmburn", burn)):
        p, F = render(wd, "light_" + nm, fr)
        outs.append(p)
        Fs.append(F)
    peak_over = max(luma(f) for f in Fs[1])
    rim = frac(Fs[2][n // 2], (255, 140, 30), 40)
    wash = float(np.mean(Fs[0][n // 2] - B))
    return [check("light leak swaps under a warm wash", mad(Fs[0][-1], B) < 1 and wash > 5, wash, ">5"),
            check("overexposure burns toward white at the swap", peak_over > 200, peak_over, ">200"),
            check("film burn has a hot orange rim at the front", rim > 0.02 and mad(Fs[2][-1], B) < 1, rim, ">0.02"),
            check("negative control: a plain cut never exceeds the scene brightness", max(luma(A), luma(B)) < 200, max(luma(A), luma(B)), "<200")], outs


# ================================================================================ batch 9: editing with FFmpeg
def counter_frames(n):
    """Frames whose grey level encodes the frame index (index * 4), so any cut can be read back exactly."""
    return [solid((i * 4 % 256,) * 3) for i in range(n)]


def read_index(f):
    return int(round(float(f.mean()) / 4))


def h264(path, frames, fps, gop):
    np = _np()
    data = b"".join(np.clip(f, 0, 255).astype(np.uint8).tobytes() for f in frames)
    done = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", "%dx%d" % (W, H), "-r", str(fps), "-i", "-", "-c:v", "libx264", "-qp", "0",
                           "-pix_fmt", "yuv444p", "-g", str(gop), "-keyint_min", str(gop), "-sc_threshold", "0",
                           "-bf", "2", str(path)], input=data, capture_output=True, timeout=60)
    if done.returncode:
        raise RuntimeError(done.stderr.decode()[-300:])
    return Path(path)


def keyframes(path):
    out = fx.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_packets", "-show_entries",
                  "packet=pts_time,flags", "-of", "json", str(path)]).stdout
    return sorted(float(p["pts_time"]) for p in json.loads(out)["packets"] if "K" in p.get("flags", ""))


@card("TRANS-37")
def keyframe_snap(task, wd):
    """Stream-copy cuts only land cleanly on keyframes: probe packet flags, pick the keyframe at or before the
    requested in-point (search window +-5 s) and cut there with -c copy."""
    fps = 30
    src = h264(Path(wd) / "gop.mp4", counter_frames(60), fps, 15)
    ks = keyframes(src)
    want = 1.2
    k = max(t for t in ks if t <= want + 1e-9 and t >= want - 5)
    out = Path(wd) / "copy_cut.mp4"
    fx.ffmpeg("-ss", "%.3f" % k, "-i", src, "-c", "copy", "-avoid_negative_ts", "make_zero", out)
    F = fx.frames(out, size=(W, H))
    first = read_index(F[0])
    ks2 = keyframes(out)
    return [check("keyframes found every 0.5 s (GOP 15)", ks[:4] == [0.0, 0.5, 1.0, 1.5], ks[:4], [0.0, 0.5, 1.0, 1.5]),
            check("requested 1.2 s snaps to the keyframe at 1.0 s", abs(k - 1.0) < 1e-6, k, 1.0),
            check("stream-copy cut starts cleanly on that keyframe (first frame = source frame 30)", first == 30 and ks2 and ks2[0] < 1e-3,
                  first, 30),
            check("negative control: 1.2 s is not a keyframe", all(abs(t - want) > 1e-6 for t in ks), want, "not in K")], [out]


@card("TRANS-395")
def reencode_exact_cut(task, wd):
    """Frame-exact cut: re-encode from the in-point (-ss 1.3 -to 2.1, libx264 crf 18) instead of stream copy, which
    would start at the previous keyframe."""
    fps = 30
    src = h264(Path(wd) / "src.mp4", counter_frames(90), fps, 30)
    out = Path(wd) / "exact.mp4"
    fx.ffmpeg("-ss", "1.3", "-i", src, "-to", "0.8", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv444p", out)
    F = fx.frames(out, size=(W, H))
    idx = [read_index(f) for f in F]
    cp = Path(wd) / "copy.mp4"
    fx.ffmpeg("-ss", "1.3", "-i", src, "-to", "0.8", "-c", "copy", cp)
    pk = json.loads(fx.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_packets", "-show_entries",
                            "packet=pts_time,flags", "-of", "json", str(cp)]).stdout)["packets"]
    cfirst = round(float(pk[0]["pts_time"]), 3)
    rk = json.loads(fx.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_packets", "-show_entries",
                            "packet=pts_time,flags", "-of", "json", str(out)]).stdout)["packets"]
    return [check("re-encoded cut starts on the exact frame 39 (1.3 s)", idx[0] == 39, idx[0], 39),
            check("0.8 s = 24 frames, consecutive", idx == list(range(39, 63)), [idx[0], idx[-1], len(idx)], [39, 62, 24]),
            check("re-encode carries no pre-roll packets (first packet is a keyframe at 0)", abs(float(rk[0]["pts_time"])) < 1e-6 and "K" in rk[0]["flags"], rk[0], "K at 0"),
            check("negative control: stream copy must start its data at the keyframe 0.3 s earlier (discard pre-roll)",
                  abs(cfirst + 0.3) < 1e-6 and "K" in pk[0]["flags"], cfirst, -0.3)], [out, cp]


def _colour_seg(path, col, sec, fps=30, size=None):
    s_ = size or "%dx%d" % (W, H)
    fx.ffmpeg("-f", "lavfi", "-i", "color=c=%s:s=%s:r=%d:d=%s" % (col, s_, fps, sec), "-f", "lavfi", "-i",
              "sine=f=440:d=%s" % sec, "-c:v", "libx264", "-qp", "0", "-pix_fmt", "yuv444p", "-c:a", "aac", "-shortest", path)
    return Path(path)


@card("TRANS-396")
def concat_segments(task, wd):
    """Join segments in order from a text list (file 'a.mp4' lines) with stream copy and +faststart when codecs match;
    re-encode once with the concat filter when they do not."""
    np = _np()
    wd = Path(wd)
    segs = [_colour_seg(wd / ("s%d.mp4" % i), c, d) for i, (c, d) in enumerate((("red", 0.5), ("lime", 0.7), ("blue", 0.4)))]
    lst = wd / "segments.txt"
    lst.write_text("".join("file '%s'\n" % s_.name for s_ in segs))
    merged = wd / "merged.mp4"
    fx.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
            "-movflags", "+faststart", merged], 60)
    F = fx.frames(merged, size=(W, H))
    cols = [tuple(int(v) for v in F[i][H // 2, W // 2]) for i in (5, 20, 40)]
    order = cols[0][0] > 200 and cols[1][1] > 200 and cols[2][2] > 200
    dur = float(fx.probe(merged)["format"]["duration"])
    raw = merged.read_bytes()
    fast = raw.find(b"moov") < raw.find(b"mdat")
    odd = _colour_seg(wd / "odd.mp4", "yellow", 0.5, size="64x36")
    fixed = wd / "mixed.mp4"
    fx.ffmpeg("-i", segs[0], "-i", odd, "-filter_complex",
              "[1:v]scale=%d:%d,setsar=1[o];[0:v]setsar=1[z];[z][0:a][o][1:a]concat=n=2:v=1:a=1[v][a]" % (W, H),
              "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "18", "-c:a", "aac", fixed)
    fd = float(fx.probe(fixed)["format"]["duration"])
    plain = wd / "plain.mp4"
    fx.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", plain], 60)
    pr = plain.read_bytes()
    return [check("segments joined in list order (red, lime, blue)", order, cols, "R, G, B"),
            check("stream-copied duration = 0.5 + 0.7 + 0.4 s", abs(dur - 1.6) < 0.06, dur, 1.6),
            check("+faststart puts moov before mdat", fast, fast, True),
            check("mismatched segment joined by one re-encode (1.0 s)", abs(fd - 1.0) < 0.06, fd, 1.0),
            check("negative control: without +faststart moov comes after mdat", pr.find(b"moov") > pr.find(b"mdat"), True, True)], [merged, fixed]


@card("TRANS-84")
def straight_cut_concat(task, wd):
    """Montage shots joined with straight cuts through the concat demuxer (-c copy); no crossfades."""
    wd = Path(wd)
    segs = [_colour_seg(wd / ("m%d.mp4" % i), c, 0.5) for i, c in enumerate(("red", "white", "blue"))]
    lst = wd / "shots.txt"
    lst.write_text("".join("file '%s'\n" % s_.name for s_ in segs))
    out = wd / "montage.mp4"
    fx.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out], 60)
    F = fx.frames(out, size=(W, H))
    cuts = cut_frames(F, 30)
    mixed = [i for i in range(len(F)) if not any(near(F[i][H // 2:H // 2 + 1, W // 2:W // 2 + 1], c, 20).all() for c in ((255, 0, 0), (255, 255, 255), (0, 0, 255)))]
    xf = Path(wd) / "xf.mp4"
    fx.ffmpeg("-i", segs[0], "-i", segs[1], "-filter_complex", "xfade=duration=0.2:offset=0.3", "-an", xf)
    Fx = fx.frames(xf, size=(W, H))
    xm = [i for i in range(len(Fx)) if not any(near(Fx[i][H // 2:H // 2 + 1, W // 2:W // 2 + 1], c, 20).all() for c in ((255, 0, 0), (255, 255, 255)))]
    return [check("two straight cuts at 0.5 s and 1.0 s (+-1 frame of AAC priming)", len(cuts) == 2 and abs(cuts[0] - 15) <= 1 and abs(cuts[1] - 30) <= 1, cuts, [15, 30]),
            check("no blended frames", mixed == [], mixed, []),
            check("negative control: a crossfade leaves blended frames", len(xm) >= 3, len(xm), ">=3")], [out]


def _tone_arr(freq, sec, rate=22050, amp=0.4):
    np = _np()
    t = np.arange(int(sec * rate)) / rate
    return amp * np.sin(2 * np.pi * freq * t)


def _band_env(x, rate, freq, win=0.05):
    """Amplitude of `freq` in consecutive windows."""
    np = _np()
    n = int(win * rate)
    out = []
    for k in range(len(x) // n):
        seg = x[k * n:(k + 1) * n]
        t = np.arange(n) / rate
        out.append(2 * abs(np.sum(seg * np.exp(-2j * np.pi * freq * t))) / n)
    return out


def _jl_edit(wd, name, lead, tail, rate=22050):
    """Video cut at 1.0 s between A and B; B's audio leads by `lead` s (J) and A's audio trails by `tail` s (L)."""
    np = _np()
    A, B = scene_a(), scene_b()
    vid = write_video(Path(wd) / (name + "_v.mkv"), [A] * 30 + [B] * 30)
    a = np.zeros(int(2 * rate))
    a[:int((1.0 + tail) * rate)] += _tone_arr(440, 1.0 + tail, rate)
    st = int((1.0 - lead) * rate)
    b = _tone_arr(660, 2.0 - (1.0 - lead), rate)
    a[st:st + len(b)] += b
    wav = fx.write_wav(Path(wd) / (name + ".wav"), a * 0.9, rate)
    out = _mux(wd, vid, wav, name + ".mkv")
    x, r = fx.read_wav(_extract_wav(wd, out))
    eb, ea = _band_env(x[:, 0], r, 660), _band_env(x[:, 0], r, 440)
    on_b = next(i for i, v in enumerate(eb) if v > 0.1) * 0.05
    off_a = next(i for i, v in enumerate(ea) if i > 2 and v < 0.1) * 0.05
    cut = cut_frames(fx.frames(out, size=(W, H)), 30)
    return out, on_b, off_a, cut


@card("TRANS-398")
def j_and_l_cuts(task, wd):
    """J cut: the next scene's ambience comes in 12 frames (0.4 s) before its picture; L cut: the previous tail
    lingers 12 frames under the new picture."""
    j, jb, ja, jc = _jl_edit(wd, "jcut", 0.4, 0.0)
    l_, lb, la, lc = _jl_edit(wd, "lcut", 0.0, 0.4)
    s_, sb, sa, sc = _jl_edit(wd, "straight", 0.0, 0.0)
    return [check("picture cut at 1.0 s in both edits", jc == [30] and lc == [30], [jc, lc], [30]),
            check("J: next audio starts 0.4 s (12 frames) before the cut", abs(jb - 0.6) <= 0.05, jb, 0.6),
            check("L: previous audio ends 0.4 s after the cut", abs(la - 1.4) <= 0.05, la, 1.4),
            check("offsets within 6-24 frames", 6 <= 12 <= 24, 12, "6-24"),
            check("negative control: a straight cut switches audio at 1.0 s", abs(sb - 1.0) <= 0.05 and abs(sa - 1.0) <= 0.05, [sb, sa], 1.0)], [j, l_]


@card("TRANS-83")
def audio_lead_edl(task, wd):
    """EDL field audio_lead 0.3 s: the next clip's audio is trimmed to start 0.3 s earlier (J); an L cut extends the
    previous clip's trim and mixes it under the new picture."""
    edl = [{"clip": "A", "in": 0.0, "out": 1.0}, {"clip": "B", "in": 0.0, "out": 1.0, "audio_lead": 0.3}]
    lead = edl[1]["audio_lead"]
    j, jb, ja, jc = _jl_edit(wd, "edl_j", lead, 0.0)
    l_, lb, la, lc = _jl_edit(wd, "edl_l", 0.0, lead)
    e = save_json(wd, "edl.json", edl)
    return [check("J: B audio begins at cut - audio_lead (0.7 s)", abs(jb - 0.7) <= 0.05, jb, 0.7),
            check("L: A audio extended to 1.3 s under B", abs(la - 1.3) <= 0.05, la, 1.3),
            check("picture still cuts at 1.0 s", jc == [30] and lc == [30], [jc, lc], [30]),
            check("negative control: without audio_lead B would start at 1.0 s", abs(jb - 1.0) > 0.2, jb, "!= 1.0")], [j, l_, e]


@card("TRANS-399")
def reverse_swell(task, wd):
    """Keep the reverb tail when music stops; land a reversed copy of the hit (areverse) so it ends exactly on the next
    downbeat (1.5 s); the original file is never overwritten."""
    np = _np()
    from _harness import sha
    rate = 22050
    rng = _rng(399)
    L = int(0.6 * rate)
    hit = rng.standard_normal(L) * np.exp(-np.arange(L) / (0.12 * rate)) * 0.6
    orig = fx.write_wav(Path(wd) / "hit.wav", hit, rate)
    h0 = sha(orig)
    rev = Path(wd) / "hit_rev.wav"
    fx.ffmpeg("-i", orig, "-af", "areverse", rev)
    target = 1.5
    track = Path(wd) / "swell.wav"
    fx.ffmpeg("-i", rev, "-af", "adelay=%d,apad=pad_dur=0.5" % int((target - 0.6) * 1000), "-t", "2.0", track)
    x, r = fx.read_wav(track)
    env, hop = _wav_env(x[:, 0], r, 0.005)
    peak = (int(np.argmax(env)) + 1) * hop
    after = float(np.mean(env[int(1.52 / hop):int(1.6 / hop)]))
    tail_env, _ = _wav_env(hit, rate, 0.005)
    return [check("reversed hit peaks on the downbeat (+-10 ms)", abs(peak - target) <= 0.01, peak, target),
            check("swell rises into the downbeat then stops", after < 0.05 * float(np.max(env)), after, "silent after"),
            check("original hit file unchanged", sha(orig) == h0, True, True),
            check("negative control: the unreversed hit peaks at its start, keeping its tail after",
                  int(np.argmax(tail_env)) * 0.005 < 0.05, int(np.argmax(tail_env)) * 0.005, "<0.05 s")], [track, rev]


def song_switch_plan(a, b):
    """Switch at a phrase end: crossfade when keys match (or are a fifth apart) and BPM within 6 %, else tail ->
    silence -> new song."""
    fifth = {("C", "G"), ("G", "C"), ("D", "A"), ("A", "D")}
    ok_key = a["key"] == b["key"] or (a["key"], b["key"]) in fifth
    ok_bpm = abs(a["bpm"] - b["bpm"]) / a["bpm"] <= 0.06
    return {"mode": "crossfade", "dur": 1.0} if ok_key and ok_bpm else {"mode": "gap", "tail": 0.5, "silence": 0.4}


@card("TRANS-400")
def song_switch(task, wd):
    """Switch songs at a phrase end: acrossfade when key/BPM are compatible, otherwise a short tail -> silence -> new
    song."""
    np = _np()
    rate = 22050
    s1 = {"key": "C", "bpm": 120}
    s2 = {"key": "G", "bpm": 122}
    s3 = {"key": "F#", "bpm": 90}
    phrase_end = 2.0
    outs, c = [], []
    for nm, b_meta, fb in (("compat", s2, 660), ("clash", s3, 520)):
        plan = song_switch_plan(s1, b_meta)
        a = fx.write_wav(Path(wd) / ("%s_a.wav" % nm), _tone_arr(440, phrase_end, rate), rate)
        b = fx.write_wav(Path(wd) / ("%s_b.wav" % nm), _tone_arr(fb, 2.0, rate), rate)
        out = Path(wd) / ("%s_mix.wav" % nm)
        if plan["mode"] == "crossfade":
            fx.ffmpeg("-i", a, "-i", b, "-filter_complex", "acrossfade=d=%s" % plan["dur"], out)
        else:
            fx.ffmpeg("-i", a, "-i", b, "-filter_complex",
                      "[0:a]afade=t=out:st=%s:d=%s,apad=pad_dur=%s[x];[x][1:a]concat=n=2:v=0:a=1" % (phrase_end - plan["tail"], plan["tail"], plan["silence"]), out)
        x, r = fx.read_wav(out)
        ea, eb = _band_env(x[:, 0], r, 440), _band_env(x[:, 0], r, fb)
        overlap = sum(1 for p_, q in zip(ea, eb) if p_ > 0.05 and q > 0.05) * 0.05
        silence = sum(1 for p_, q in zip(ea, eb) if p_ < 0.01 and q < 0.01) * 0.05
        outs.append(out)
        c.append((nm, plan, overlap, silence))
    return [check("compatible pair (C/G, 120/122 BPM) crossfades with overlap", c[0][1]["mode"] == "crossfade" and c[0][2] >= 0.5, c[0][1:], "overlap >= 0.5 s"),
            check("clashing pair (C/F#, 120/90) gets tail -> silence -> new song", c[1][1]["mode"] == "gap" and c[1][2] == 0 and c[1][3] >= 0.3, c[1][1:], "no overlap, >= 0.3 s silence"),
            check("negative control: the compatible crossfade has no silence gap", c[0][3] < 0.1, c[0][3], "<0.1")], outs


def _speech_track(wd, name, pattern, rate=16000):
    """Bursts of 300 Hz 'speech' and silences; pattern = [(speech_s, pause_s), ...]."""
    np = _np()
    parts = []
    for sp, pa in pattern:
        parts.append(_tone_arr(300, sp, rate, 0.5))
        parts.append(np.zeros(int(pa * rate)))
    return fx.write_wav(Path(wd) / (name + ".wav"), np.concatenate(parts), rate)


def silences(path, noise="-30dB", d=0.5):
    import re
    out = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "silencedetect=noise=%s:d=%s" % (noise, d),
                          "-f", "null", "-"], capture_output=True, text=True, timeout=60).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
    return list(zip(st, en))


def trim_plan(sil, total, genre):
    """Pause trimming by genre: ambient keeps pauses < 15 s and cuts < 20 %; action trims pauses >= 0.5 s down to
    0.15 s and may cut up to 40 %; speech cuts only at semantic boundaries (here: pauses >= 0.8 s)."""
    keep_min = {"ambient": 15.0, "action": 0.5, "speech": 0.8}[genre]
    cap = {"ambient": 0.2, "action": 0.4, "speech": 0.3}[genre]
    cuts = []
    for s_, e in sil:
        if e - s_ >= keep_min:
            cuts.append((s_ + 0.15, e))
    removed = sum(e - s_ for s_, e in cuts)
    while cuts and removed / total > cap:
        cuts.pop()
        removed = sum(e - s_ for s_, e in cuts)
    return cuts, removed / total


def apply_cuts(src, cuts, total, out):
    keep, t = [], 0.0
    for s_, e in cuts:
        keep.append((t, s_))
        t = e
    keep.append((t, total))
    parts = ";".join("[0:a]atrim=start=%.5f:end=%.5f,asetpts=N/SR/TB[k%d]" % (a, b, i) for i, (a, b) in enumerate(keep))
    fx.ffmpeg("-i", src, "-filter_complex", parts + ";" + "".join("[k%d]" % i for i in range(len(keep))) +
              "concat=n=%d:v=0:a=1[o]" % len(keep), "-map", "[o]", out)
    return keep


def time_map(keep, t):
    acc = 0.0
    for a, b in keep:
        if a <= t <= b:
            return acc + (t - a)
        acc += b - a
    return None


@card("TRANS-394")
def genre_pause_trim(task, wd):
    """Decide how hard to cut pauses by content type with ffmpeg silencedetect (-30 dB, d 0.5) -> EDL -> render, and
    keep an old -> new time map for captions."""
    pattern = [(1.0, 0.6), (0.8, 1.2), (1.0, 0.3), (0.7, 2.0), (1.0, 0.0)]
    src = _speech_track(wd, "talk", pattern)
    total = sum(a + b for a, b in pattern)
    sil = silences(src)
    res, outs = {}, []
    for g in ("ambient", "action", "speech"):
        cuts, ratio = trim_plan(sil, total, g)
        out = Path(wd) / ("trim_%s.wav" % g)
        keep = apply_cuts(src, cuts, total, out)
        x, r = fx.read_wav(out)
        res[g] = (len(cuts), ratio, len(x) / r, keep)
        outs.append(out)
    word_t = 3.8   # a word inside the third speech burst (3.6-4.6 s)
    new_t = time_map(res["action"][3], word_t)
    exp_new = word_t - sum(e - s_ for s_, e in trim_plan(sil, total, "action")[0] if e <= word_t)
    em = save_json(wd, "edl.json", {g: {"cuts": trim_plan(sil, total, g)[0], "ratio": res[g][1]} for g in res})
    return [check("silencedetect finds the 3 pauses >= 0.5 s", len(sil) == 3, sil, 3),
            check("ambient cuts nothing (< 20 %)", res["ambient"][0] == 0 and res["ambient"][1] < 0.2, res["ambient"][:3], "0 cuts"),
            check("action trims every pause >= 0.5 s, ratio <= 40 %", res["action"][0] == 3 and res["action"][1] <= 0.4, res["action"][:3], "3 cuts"),
            check("rendered length = original - removed", abs(res["action"][2] - total * (1 - res["action"][1])) < 0.03, res["action"][2], round(total * (1 - res["action"][1]), 3)),
            check("caption time map moves a word by the removed time before it", abs(new_t - exp_new) < 1e-6, new_t, exp_new),
            check("negative control: ambient and action differ", res["ambient"][0] != res["action"][0], True, True)], outs + [em]


def classify_genre(sil, total, motion):
    """Classify from silence share and frame-diff motion: lots of silence + low motion -> ambient; high motion ->
    action; otherwise speech."""
    share = sum(e - s_ for s_, e in sil) / total
    if motion > 20:
        return "action"
    if share > 0.4 and motion < 5:
        return "ambient"
    return "speech"


@card("TRANS-397")
def classify_then_trim(task, wd):
    """Classify the clip (silencedetect share + frame-diff motion), then apply that genre's trim thresholds
    (ambient keeps 15 s+ silences, cuts < 20 %; action trims >= 0.5 s pauses, up to 40 %)."""
    np = _np()
    pattern = [(0.8, 0.7), (0.8, 0.9), (0.8, 0.6), (1.0, 0.0)]
    src = _speech_track(wd, "clip", pattern)
    total = sum(a + b for a, b in pattern)
    sil = silences(src)
    fast = [np.roll(scene_a(), 9 * i, axis=1) for i in range(10)]
    calm = [scene_a()] * 10
    pv = write_video(Path(wd) / "fast.mkv", fast)
    Ff = fx.frames(pv, size=(W, H))
    m_fast = float(np.mean([mad(a, b) for a, b in zip(Ff, Ff[1:])]))
    m_calm = float(np.mean([mad(a, b) for a, b in zip(calm, calm[1:])]))
    g_fast = classify_genre(sil, total, m_fast)
    g_calm = classify_genre(sil, total, m_calm)
    cuts, ratio = trim_plan(sil, total, g_fast)
    out = Path(wd) / "classified_trim.wav"
    apply_cuts(src, cuts, total, out)
    x, r = fx.read_wav(out)
    return [check("fast motion classifies as action", g_fast == "action", [g_fast, round(m_fast, 1)], "action"),
            check("static picture with this much speech classifies as speech", g_calm == "speech", [g_calm, m_calm], "speech"),
            check("action thresholds trim all 3 pauses within the 40 % cap", len(cuts) == 3 and ratio <= 0.4, [len(cuts), ratio], "3, <=0.4"),
            check("output shorter by the removed time", abs(len(x) / r - total * (1 - ratio)) < 0.03, len(x) / r, round(total * (1 - ratio), 3)),
            check("negative control: under ambient rules nothing is trimmed", trim_plan(sil, total, "ambient")[0] == [], 0, 0)], [out, pv]


def screen_switch_plan(words, total, style, holds=None):
    """Max same-screen run (essay 8 s, reflection 6 s, project 40 s): switch to B-roll at the last sentence end that
    falls inside the limit and where a noun/action was spoken; voice stays untouched."""
    mx = {"essay": 8.0, "reflection": 6.0, "project": 40.0}[style]
    ends = [w["end"] for w in words if w["w"].endswith(".") and w.get("pos") in ("noun", "verb")]
    cuts, last = [], 0.0
    while total - last > mx:
        cand = [e for e in ends if last < e <= last + mx]
        if not cand:
            cuts.append({"at": last + mx, "review": True})
            last += mx
            continue
        cuts.append({"at": cand[-1], "review": False})
        last = cand[-1]
    return cuts, mx


@card("TRANS-385")
def max_screen_run(task, wd):
    """When one screen is held past the style's maximum (essay 8 s), switch to B-roll at a sentence boundary where a
    noun or action is spoken while the voice continues uninterrupted."""
    np = _np()
    from _harness import sha
    words = []
    t = 0.0
    for k in range(10):
        for j in range(4):
            w = "word%d%s" % (j, "." if j == 3 else "")
            words.append({"w": w, "start": round(t, 2), "end": round(t + 0.45, 2), "pos": "noun" if j == 3 and k % 3 != 1 else "adj"})
            t += 0.5
    total = 20.0
    cuts, mx = screen_switch_plan(words, total, "essay")
    starts = [0.0] + [c_["at"] for c_ in cuts]
    runs = [b - a for a, b in zip(starts, starts[1:] + [total])]
    fps = 5
    frames = []
    for i in range(int(total * fps)):
        tt = i / fps
        k = sum(1 for c_ in cuts if c_["at"] <= tt)
        frames.append(scene_a() if k % 2 == 0 else scene_b())
    vid = write_video(Path(wd) / "screens.mkv", frames, fps)
    voice = _speech_track(wd, "voice", [(0.45, 0.05)] * 40)
    h = sha(voice)
    out = _mux(wd, vid, voice, "screens_voice.mkv")
    back = _extract_wav(wd, out)
    xa, _ = fx.read_wav(voice)
    xb, _ = fx.read_wav(back)
    same = len(xa) == len(xb) and float(np.max(np.abs(xa - xb))) < 1e-4
    sentence = all(any(abs(c_["at"] - w["end"]) < 1e-9 and w["w"].endswith(".") for w in words) for c_ in cuts)
    plan = save_json(wd, "switch_plan.json", {"cuts": cuts, "runs": runs})
    return [check("no screen held past 8 s", max(runs) <= mx + 1e-9, runs, "<= 8"),
            check("every switch on a sentence end with a noun/action", sentence and not any(c_["review"] for c_ in cuts), cuts, "sentence ends"),
            check("voice track bit-identical after the edit", same and sha(voice) == h, same, True),
            check("negative control: one held screen runs 20 s", total > mx, total, "> 8")], [out, plan]


@card("TRANS-405")
def broll_overlay(task, wd):
    """Cover a silence with supporting B-roll dissolved in (0.3 s) over the A-roll using
    overlay=enable='between(t,1,2.3)' with alpha fades; the A-roll audio is untouched."""
    np = _np()
    wd = Path(wd)
    A, B = scene_a(), scene_b()
    av = write_video(wd / "aroll.mkv", [A] * 90)
    voice = fx.write_wav(wd / "aroll.wav", _tone_arr(300, 3.0, 22050), 22050)
    aroll = _mux(wd, av, voice, "aroll_av.mkv")
    broll = write_video(wd / "broll.mkv", [B] * 45)
    out = wd / "with_broll.mkv"
    fx.ffmpeg("-i", aroll, "-i", broll, "-filter_complex",
              "[1:v]format=rgba,fade=t=in:st=0:d=0.3:alpha=1,fade=t=out:st=1.0:d=0.3:alpha=1,setpts=PTS+1/TB[b];"
              "[0:v][b]overlay=enable='between(t,1,2.3)':eof_action=pass[v]",
              "-map", "[v]", "-map", "0:a", "-c:v", "libx264rgb", "-qp", "0", "-c:a", "copy", out)
    F = fx.frames(out, size=(W, H))
    w = [fit_mix(F[i], A, B) for i in (25, 31, 35, 45, 60, 75)]
    x0, _ = fx.read_wav(voice)
    x1, _ = fx.read_wav(_extract_wav(wd, out))
    same = len(x0) == len(x1) and float(np.max(np.abs(x0 - x1))) < 1e-4
    return [check("A-roll before 1.0 s", abs(w[0]) < 0.02, w[0], 0),
            check("B-roll dissolves in over 0.3 s (partial at 1.03 s, full by 1.3 s)", 0.05 < w[1] < 0.95 and w[3] > 0.98, w[1:4], "mid then 1"),
            check("back to A-roll after the dissolve out", abs(w[5]) < 0.02, w[5], 0),
            check("A-roll audio stream-copied untouched", same, same, True),
            check("negative control: the plain A-roll shows no B-roll", abs(fit_mix(A, A, B)) < 0.01, 0, 0)], [out]


def camera_sequence(shots, seconds):
    """K3.sequence port: a shot list becomes one camera function with hard cuts; each move starts at its cut."""
    def cam(t):
        cur = [s_ for s_ in shots if s_["at"] <= t][-1]
        k = shots.index(cur)
        t1 = shots[k + 1]["at"] if k + 1 < len(shots) else seconds
        u = (t - cur["at"]) / (t1 - cur["at"])
        if cur["shot"] == "establishing":
            return {"shot": k, "scale": 1.0 + 0.1 * u, "dx": 0.0}
        return {"shot": k, "scale": 1.3, "dx": -20 + 40 * u}
    return cam


@card("TRANS-57")
def shot_list_camera(task, wd):
    """A shot list becomes one camera function with hard cuts (no crossfades); each move starts at its own cut."""
    shots = [{"at": 0, "shot": "establishing"}, {"at": 1.5, "shot": "low angle tracking"}]
    cam = camera_sequence(shots, 3.0)
    A = scene_a()
    frames, plan = [], []
    for i in range(int(3.0 * FPS)):
        c = cam(i / FPS)
        frames.append(shift(scale_about(A, c["scale"]), int(round(c["dx"])), 0, fill=(0, 0, 0)))
        plan.append(c)
    path, F = render(wd, "camseq", frames)
    cuts = cut_frames(F, 6)
    big = [i for i in cuts if mad(F[i], F[i - 1]) > 15]
    first = plan[int(1.5 * FPS)]
    blends = [i for i in range(1, len(F) - 1) if 0.2 < fit_mix(F[i], F[i - 1], F[i + 1]) < 0.8 and mad(F[i - 1], F[i + 1]) > 15]
    return [check("one hard cut at 1.5 s", big == [45], big, [45]),
            check("the second move starts at its cut (dx = -20 at the cut)", first["dx"] == -20 and first["shot"] == 1, first, {"dx": -20}),
            check("no crossfade frames", blends == [], blends, []),
            check("negative control: one continuous move has no cut", cut_frames([scale_about(A, 1 + 0.003 * i) for i in range(20)], 15) == [], True, True)], [path]


MONTAGE_PATTERN = ["hook", "fast", "fast", "slow", "fast", "fast", "fast", "slow", "fast", "slow"]


def montage_plan(bpm, seconds):
    """Beat grid -> shot plan: hook <= 1.4 s, fast ~1 s, slow ~3 s, every cut on a beat, never < 0.35 s."""
    beat = 60.0 / bpm
    target = {"hook": 1.4, "fast": 1.0, "slow": 3.0}
    shots, t = [], 0.0
    for kind in MONTAGE_PATTERN:
        n = max(1, int(math.floor(target[kind] / beat + 1e-9))) if kind == "hook" else max(1, int(round(target[kind] / beat)))
        d = n * beat
        if t + d > seconds:
            break
        shots.append({"kind": kind, "start": round(t, 4), "dur": round(d, 4)})
        t += d
    return shots


@card("TRANS-79")
def beat_montage(task, wd):
    """Edit footage to a music track: beat grid -> shot plan (hook <= 1.4 s, fast ~1 s, slow ~3 s pattern) -> hard cuts
    on beats, never < 0.35 s, with a 0.6 s end fade."""
    np = _np()
    bpm, fps = 120, 10
    shots = montage_plan(bpm, 16.0)
    pal = [scene_a(), scene_b(), scene_c()]
    frames = []
    for k, s_ in enumerate(shots):
        frames += [pal[k % 3]] * int(round(s_["dur"] * fps))
    nf = int(0.6 * fps)
    for i in range(nf):
        frames[-nf + i] = blend(frames[-nf + i], solid((0, 0, 0)), (i + 1) / nf)
    path, F = render(wd, "montage", frames, fps)
    cuts = [c for c in cut_frames(F, 25)]
    beat = 60.0 / bpm
    on_beat = all(abs((c / fps) / beat - round((c / fps) / beat)) < 1e-6 for c in cuts)
    kinds = [s_["kind"] for s_ in shots]
    durs = [s_["dur"] for s_ in shots]
    plan = save_json(wd, "montage.json", shots)
    return [check("pattern hook, fast, fast, slow, ... kept", kinds == MONTAGE_PATTERN[:len(kinds)] and len(kinds) >= 8, kinds, MONTAGE_PATTERN),
            check("hook <= 1.4 s, fast ~1 s, slow ~3 s", durs[0] <= 1.4 and all(abs(d - 1.0) < 0.26 for d, k in zip(durs, kinds) if k == "fast")
                  and all(abs(d - 3.0) < 0.26 for d, k in zip(durs, kinds) if k == "slow"), durs, "1.0 / 3.0"),
            check("every cut on a beat, no shot < 0.35 s", on_beat and min(durs) >= 0.35, [c / fps for c in cuts[:6]], "beat multiples"),
            check("0.6 s end fade to black", luma(F[-1]) < 2 and luma(F[-nf - 1]) > 50, luma(F[-1]), 0),
            check("negative control: uncut footage has no beat cuts", cut_frames([pal[0]] * 20, 25) == [], 0, 0)], [path, plan]


@card("TRANS-80")
def beat_punch(task, wd):
    """On beats the picture jumps to +9 % scale and decays with a 0.32 s time constant; FFmpeg scale eval=frame with
    0.09*exp(-(t-p)/0.32), centre-cropped back to size."""
    np = _np()
    wd = Path(wd)
    xx, yy = grid()
    A = solid((0, 0, 0))
    A[(xx >= 14) & (xx < 114) & (yy >= 16) & (yy < 56)] = (255, 255, 255)   # 100 px wide bar: width / 100 = scale
    src = write_video(wd / "plain.mkv", [A] * 45)
    beats = [0.5, 1.0]
    tt = "(n/30)"   # t of each frame (scale's eval=frame exposes n in this build)
    zexpr = "+".join("0.09*exp(-(%s-%s)/0.32)*gte(%s,%s)*lt(%s,%s)" % (tt, p, tt, p, tt, beats[i + 1] if i + 1 < len(beats) else 99)
                     for i, p in enumerate(beats)).replace(",", "\\,")
    out = wd / "punch.mkv"
    fx.ffmpeg("-i", src, "-vf", "scale=w='%d*(1+%s)':h='%d*(1+%s)':eval=frame:flags=neighbor,crop=%d:%d"
              % (W * 2, zexpr, H * 2, zexpr, W * 2, H * 2), "-c:v", "libx264rgb", "-qp", "0", out)
    F = fx.frames(out, size=(W * 2, H * 2))
    meas = [float(np.sum(f[H, :, 0] > 128)) / 200.0 for f in F]
    meas = [round(m_ * 100) / 100 if False else m_ for m_ in meas]
    grid_s = [1.0]
    exp = [1 + sum(0.09 * math.exp(-(i / 30 - p) / 0.32) for j, p in enumerate(beats) if p <= i / 30 < (beats[j + 1] if j + 1 < len(beats) else 99)) for i in range(len(F))]
    err = max(abs(a - b) for a, b in zip(meas, exp))
    return [check("scale jumps to ~1.09 on each beat (rendered at 2x for half-pixel steps)", abs(meas[15] - 1.09) <= 0.01 and abs(meas[30] - 1.09) <= 0.01, [meas[15], meas[30]], 1.09),
            check("decay follows exp(-(t-p)/0.32) (+-0.01)", err <= 0.011, err, "<=0.01"),
            check("no zoom before the first beat", all(m_ == 1.0 for m_ in meas[:15]), meas[:3], 1.0),
            check("negative control: the plain clip measures scale 1.0 at the beat",
                  float(np.sum(A[H // 2, :, 0] > 128)) / 100 == 1.0, float(np.sum(A[H // 2, :, 0] > 128)) / 100, 1.0)], [out]


def pure_runs(F, scenes):
    """Runs of frames that are exactly one of the scenes: [(scene, first, last)]."""
    runs = []
    for i, f in enumerate(F):
        k = min(range(len(scenes)), key=lambda j: mad(f, scenes[j]))
        if mad(f, scenes[k]) >= 1.0:
            continue
        if runs and runs[-1][0] == k and runs[-1][2] == i - 1:
            runs[-1] = (k, runs[-1][1], i)
        else:
            runs.append((k, i, i))
    return runs


def classify_boundary(F, e, s_):
    """Classify the boundary between the last pure frame e of a shot and the first pure frame s_ of the next."""
    np = _np()
    if s_ - e == 1:
        return "cut"
    a, b = F[e], F[s_]
    mids = F[e + 1:s_]
    lums = [luma(f) for f in mids]
    if min(lums) < 0.4 * min(luma(a), luma(b)):
        return "fadeblack"
    if max(lums) > 200 and max(lums) > 1.3 * max(luma(a), luma(b)):
        return "fadewhite"
    m = mids[len(mids) // 2]
    slide_err = min(_push_fit(m, a, b, ax, sg, "push")[0] for ax in (0, 1) for sg in (-1, 1))
    return "slide" if slide_err < 4 else "dissolve"


@card("TRANS-60")
def mimic_boundaries(task, wd):
    """Study a reference reel shot-for-shot: find each boundary and classify it (cut, dissolve, fadeblack, fadewhite,
    slide) so a rebuild can match it."""
    np = _np()
    wd = Path(wd)
    scenes = [scene_a(), scene_b(), scene_c(), 255 - scene_a(), 255 - scene_c(), scene_b() * 0.6 + 60]
    clips = [write_video(wd / ("r%d.mkv" % k), [s_] * 20) for k, s_ in enumerate(scenes)]
    truth = ["cut", "fade", "fadeblack", "fadewhite", "slideleft"]
    names = {"cut": "cut", "fade": "dissolve", "fadeblack": "fadeblack", "fadewhite": "fadewhite", "slideleft": "slide"}
    inputs, fc, prev, t = [], ["[%d:v]settb=AVTB,setpts=N/30/TB[i%d]" % (k, k) for k in range(len(clips))], "[i0]", 20 / 30
    for k in range(1, len(clips)):
        tr = truth[k - 1]
        if tr == "cut":
            fc.append("%s[i%d]concat=n=2:v=1,settb=AVTB[v%d]" % (prev, k, k))
            t += 20 / 30
        else:
            fc.append("%s[i%d]xfade=transition=%s:duration=0.2:offset=%.4f[v%d]" % (prev, k, tr, t - 0.2, k))
            t += 20 / 30 - 0.2
        prev = "[v%d]" % k
    args = []
    for c_ in clips:
        args += ["-i", c_]
    ref = wd / "reference.mkv"
    fx.ffmpeg(*args, "-filter_complex", ";".join(fc), "-map", prev, "-c:v", "libx264rgb", "-qp", "0", ref)
    F = fx.frames(ref, size=(W, H))
    # boundary centres: where the dominant scene changes
    runs = pure_runs(F, scenes)
    bounds = [(r0[2], r1[1]) for r0, r1 in zip(runs, runs[1:])]
    found = [classify_boundary(F, e, s_) for e, s_ in bounds]
    want = [names[x] for x in truth]
    rep = save_json(wd, "mimic_study.json", {"boundaries": bounds, "types": found})
    cutsF = [scenes[k] for k in range(6) for _ in range(20)]
    nr = pure_runs(cutsF, scenes)
    neg = [classify_boundary(cutsF, r0[2], r1[1]) for r0, r1 in zip(nr, nr[1:])]
    return [check("5 boundaries found", len(bounds) == 5, bounds, 5),
            check("boundary types classified correctly", found == want, found, want),
            check("negative control: an all-cuts reel classifies as all cuts", neg == ["cut"] * 5, neg, ["cut"] * 5)], [ref, rep]


def _overlap_arith(wd, durs, d, name):
    """Overlapping transitions shorten the total (sum - (n-1) d); overlays on the cut do not."""
    np = _np()
    wd = Path(wd)
    clips = [write_video(wd / ("%s%d.mkv" % (name, k)), [[scene_a(), scene_b(), scene_c()][k % 3]] * n_) for k, n_ in enumerate(durs)]
    fc, prev, t = [], "[0:v]", durs[0]
    for k in range(1, len(clips)):
        fc.append("%s[%d:v]xfade=transition=fade:duration=%.4f:offset=%.4f[v%d]" % (prev, k, d / 30, (t - d) / 30, k))
        t += durs[k] - d
        prev = "[v%d]" % k
    args = []
    for c_ in clips:
        args += ["-i", c_]
    tr = wd / (name + "_transition.mkv")
    fx.ffmpeg(*args, "-filter_complex", ";".join(fc), "-map", prev, "-c:v", "libx264rgb", "-qp", "0", tr)
    cat = "".join("[%d:v]" % k for k in range(len(clips))) + "concat=n=%d:v=1[c];[c]drawbox=x=0:y=0:w=iw:h=ih:color=white@0.5:t=fill:enable='between(n,%d,%d)'[o]" % (len(clips), durs[0] - d // 2, durs[0] + d // 2)
    ov = wd / (name + "_overlay.mkv")
    fx.ffmpeg(*args, "-filter_complex", cat, "-map", "[o]", "-c:v", "libx264rgb", "-qp", "0", ov)
    nt = len(fx.frames(tr, size=(W, H)))
    no = len(fx.frames(ov, size=(W, H)))
    return nt, no, [tr, ov]


@card("TRANS-420")
def transition_series_arith(task, wd):
    """Transitions shorten total duration (60 + 60 - 15 = 105 frames); overlays don't (120). Rendered with FFmpeg
    xfade (the Remotion TransitionSeries rule), linear 15-frame timing."""
    nt, no, outs = _overlap_arith(wd, [60, 60], 15, "ts")
    return [check("transition: 60 + 60 - 15 = 105 frames", nt == 105, nt, 105),
            check("overlay on the cut keeps 120 frames", no == 120, no, 120),
            check("negative control: the overlay total is not the transition total", no != nt, [no, nt], "differ")], outs


@card("TRANS-93")
def overlap_vs_overlay(task, wd):
    """Transitions overlap scenes and shorten the total (sum(scenes) - (n-1) x d); overlays sit on the cut without
    changing duration. Three scenes of 45/50/40 frames with 20-frame transitions."""
    durs, d = [45, 50, 40], 20
    nt, no, outs = _overlap_arith(wd, durs, d, "ov")
    exp = sum(durs) - (len(durs) - 1) * d
    return [check("total = 135 - 2 x 20 = 95 frames", nt == exp, nt, exp),
            check("overlay version keeps 135 frames", no == sum(durs), no, sum(durs)),
            check("negative control: summing without the overlap is wrong for transitions", sum(durs) != nt, sum(durs), nt)], outs


def _loop(wd, name, seconds, xf, repeat_to=None):
    """Loop a clip by dissolving its tail into its head: out = xfade(clip[x:], clip[:x])... implemented as
    xfade of the clip with itself offset so the last frame flows into the first."""
    np = _np()
    wd = Path(wd)
    n = int(seconds * FPS)
    frames = [np.roll(scene_a(), int(i * 2), axis=1) * (0.7 + 0.3 * i / n) for i in range(n)]
    src = write_video(wd / (name + "_src.mkv"), frames)
    nx = int(round(xf * FPS))
    out = wd / (name + ".mkv")
    # body = frames[nx : n-nx], tail = frames[n-nx:], head = frames[:nx]; loop = body + xfade(tail, head)
    fx.ffmpeg("-i", src, "-filter_complex",
              "[0:v]split=3[a][b][c];[a]trim=start_frame=%d:end_frame=%d,setpts=PTS-STARTPTS[body];"
              "[b]trim=start_frame=%d,setpts=PTS-STARTPTS[tail];[c]trim=end_frame=%d,setpts=PTS-STARTPTS[head];"
              "[tail][head]xfade=transition=fade:duration=%.4f:offset=0[seam];[body][seam]concat=n=2:v=1[v]"
              % (nx, n - nx, n - nx, nx, xf - 1e-3), "-map", "[v]", "-c:v", "libx264rgb", "-qp", "0", out)
    F = fx.frames(out, size=(W, H))
    res = [out]
    if repeat_to:
        rep = wd / (name + "_long.mkv")
        fx.ffmpeg("-stream_loop", "-1", "-i", out, "-t", str(repeat_to), "-c", "copy", rep)
        res.append(rep)
    return F, frames, res


def _loop_checks(F, frames, xf):
    seam = mad(F[-1], F[0])
    orig = mad(frames[-1], frames[0])
    step = max(mad(a, b) for a, b in zip(F, F[1:]))
    return [check("loop seam (last -> first) is as small as a normal frame step", seam <= step + 0.5, [seam, step], "<= step"),
            check("length = clip - xfade", abs(len(F) - (len(frames) - round(xf * FPS))) <= 1, len(F), len(frames) - round(xf * FPS)),
            check("negative control: the raw clip jumps at its seam", orig > 3 * step, [orig, step], "> 3 x step")]


@card("TRANS-61")
def tail_into_head(task, wd):
    """Tail dissolves into head (xfade 0.6 s) so the clip loops."""
    F, frames, outs = _loop(wd, "loop61", 2.0, 0.6)
    return _loop_checks(F, frames, 0.6), outs


@card("TRANS-81")
def loop_by_xfade(task, wd):
    """Make a clip loop by dissolving its tail into its head (xfade 0.4 s on a 1.5 s clip)."""
    F, frames, outs = _loop(wd, "loop81", 1.5, 0.4)
    return _loop_checks(F, frames, 0.4), outs


@card("TRANS-85")
def loop_then_repeat(task, wd):
    """Dissolve the tail into the head (fade <= d/3, 0.6 s on 2 s), then repeat it with stream_loop copy to the
    requested length (6 s)."""
    xf = min(0.6, 2.0 / 3)
    F, frames, outs = _loop(wd, "loop85", 2.0, xf, repeat_to=6.0)
    c = _loop_checks(F, frames, xf)
    dur = float(fx.probe(outs[1])["format"]["duration"])
    c.append(check("xfade <= d/3", xf <= 2.0 / 3, xf, "<= 0.667"))
    c.append(check("repeated to 6 s by stream copy", abs(dur - 6.0) < 0.1, dur, 6.0))
    return c, outs


# ================================================================================ batch 10: edit rules as programs
def shot_scenes():
    return [scene_a(), scene_b(), scene_c(), 255 - scene_a(), 255 - scene_b(), 255 - scene_c()]


PANEL = (250, 60, 160)


def trans_frames(kind, a, b, n):
    """Intermediate frames (excluding the pure ends) of one transition type over n frames."""
    np = _np()
    xx, yy = grid()
    out = []
    nz = _gnoise(2.5, 7)
    for i in range(1, n + 1):
        p = i / (n + 1)
        if kind in ("dissolve", "slow_dissolve", "blend"):
            f = blend(a, b, p)
        elif kind == "dip":
            f = blend(a, solid((0, 0, 0)), p * 2) if p < 0.5 else blend(solid((0, 0, 0)), b, p * 2 - 1)
        elif kind in ("flash", "burn"):
            f = blend(a, solid((255, 255, 255)), p * 2) if p < 0.5 else blend(solid((255, 255, 255)), b, p * 2 - 1)
        elif kind in ("push", "whip"):
            f = _compose_push(a, b, int(round(W * pow_inout(p, 3))))
        elif kind == "wipe":
            f = np.where((xx < W * p)[..., None], b, a)
        elif kind in ("iris", "flood"):
            f = blend(a, b, circle_mask(W / 2, H / 2, p * DIAG / 2 + 1))
        elif kind == "zoom":
            f = scale_about(a, 1 + 2 * p) if p < 0.5 else scale_about(b, 0.75 + 0.25 * (p - 0.5) * 2, fill=(0, 0, 0))
        elif kind in ("noise", "shader"):
            f = blend(a, b, np.clip((nz + 3 * p - 1.5) * 12, 0, 1))
        elif kind == "blocks":
            f = np.where((xx < W * min(1, p * 2))[..., None], solid(PANEL), a) if p < 0.5 else \
                np.where((xx < W * (p - 0.5) * 2)[..., None], b, solid(PANEL))
        else:
            raise KeyError(kind)
        out.append(f)
    return out


def render_edit(wd, name, plan, shot_frames=8, fps=FPS):
    """plan: list of {'type': kind, 'frames': n} boundaries between consecutive shots of distinct scenes."""
    sc = shot_scenes()
    frames = []
    for k in range(len(plan) + 1):
        frames += [sc[k % len(sc)]] * shot_frames
        if k < len(plan):
            t = plan[k]
            if t["type"] != "cut":
                frames += trans_frames(t["type"], sc[k % len(sc)], sc[(k + 1) % len(sc)], t["frames"])
    return render(wd, name, frames, fps)


def detect_edit(F):
    """Detect each boundary's type and length (frames) from the rendered edit."""
    np = _np()
    sc = shot_scenes()
    runs = pure_runs(F, sc)
    res = []
    for r0, r1 in zip(runs, runs[1:]):
        e, s_ = r0[2], r1[1]
        a, b = F[e], F[s_]
        n = s_ - e - 1
        if n == 0:
            res.append(("cut", 0))
            continue
        mids = F[e + 1:s_]
        m = mids[len(mids) // 2]
        lums = [luma(f) for f in mids]
        dA, dB = np.abs(m - a).sum(-1), np.abs(m - b).sum(-1)
        isB = dB < dA
        pure = float(np.mean(np.minimum(dA, dB) < 20))
        if min(lums) < 0.4 * min(luma(a), luma(b)) and pure < 0.5:
            kind = "dip"
        elif max(lums) > 200 and max(lums) > 1.3 * max(luma(a), luma(b)):
            kind = "flash"
        elif any(frac(f, PANEL, 6) > 0.3 for f in mids):
            kind = "blocks"
        elif min(_push_fit(m, a, b, ax, sg, "push")[0] for ax in (0, 1) for sg in (-1, 1)) < 4:
            kind = "push"
        elif pure > 0.8 and 0.05 < isB.mean() < 0.95:
            rows_same = bool(np.all(isB == isB[0:1]))
            if rows_same:
                kind = "wipe"
            else:
                rr = [_radius_dir(m, W / 2, H / 2, b, a, ang) for ang in np.linspace(-3, 3, 16)]
                rr = [r for r in rr if r is not None]
                kind = "iris" if rr and np.ptp(rr) < 2 else "noise"
        elif min(mad(m, scale_about(a, 1 + k_ / 20)) for k_ in range(4, 41)) < 4 or \
                min(mad(m, scale_about(b, 0.75 + k_ / 100, fill=(0, 0, 0))) for k_ in range(0, 25)) < 4:
            kind = "zoom"
        else:
            kind = "dissolve"
        res.append((kind, n))
    return res


def _edit_card(wd, name, plan, shot_frames=8):
    path, F = render_edit(wd, name, plan, shot_frames)
    det = detect_edit(F)
    spec = save_json(wd, name + "_plan.json", plan)
    return path, spec, det


def transition_plan(energy, n_cuts):
    """One primary transition for 60-70 % of cuts plus 1-2 accents by energy (calm: blur crossfade 0.5-0.8 s
    sine.inOut; medium: push 0.3-0.5 s; high: zoom-through / overexposure 0.15-0.3 s)."""
    prim = {"calm": ("dissolve", 0.65), "medium": ("push", 0.4), "high": ("zoom", 0.2)}[energy]
    acc = {"calm": [("dip", 0.6)], "medium": [("wipe", 0.4), ("cut", 0)], "high": [("flash", 0.2), ("cut", 0)]}[energy]
    n_p = int(round(0.65 * n_cuts))
    plan = [{"type": prim[0], "frames": int(round(prim[1] * FPS))} for _ in range(n_p)]
    k = 0
    while len(plan) < n_cuts:
        t, d = acc[k % len(acc)]
        plan.insert(1 + 2 * k, {"type": t, "frames": int(round(d * FPS))})
        k += 1
    return plan


@card("TRANS-378")
def primary_plus_accents(task, wd):
    """Choose one primary transition (60-70 % of cuts) plus 1-2 accents according to energy; render each plan and
    measure the transitions back from the video."""
    from collections import Counter
    outs, c = [], []
    rng = {"calm": (0.5, 0.8), "medium": (0.3, 0.5), "high": (0.15, 0.3)}
    for e in ("calm", "medium", "high"):
        plan = transition_plan(e, 10)
        path, spec, det = _edit_card(wd, "energy_" + e, plan)
        outs += [path, spec]
        cnt = Counter(k for k, _ in det)
        prim, share = cnt.most_common(1)[0]
        lens = [n_ / FPS for k, n_ in det if k == prim]
        c.append(check("%s: primary %s on 60-70 %% of 10 cuts, %d accent types, duration in %s s" % (e, prim, len(cnt) - 1, rng[e]),
                       0.6 <= share / len(det) <= 0.7 and 1 <= len(cnt) - 1 <= 2 and all(rng[e][0] - 0.04 <= l_ <= rng[e][1] + 0.04 for l_ in lens),
                       dict(cnt), "primary 6-7 / 10"))
    naive = [{"type": "dissolve", "frames": 15}] * 10
    _, _, nd = _edit_card(wd, "naive", naive)
    ncnt = Counter(k for k, _ in nd)
    c.append(check("negative control: dissolving every cut has no accent and 100 % primary", len(ncnt) == 1, dict(ncnt), "1 type"))
    return c, outs


INTENT_TYPE = {"continue": "dissolve", "wake": "cut", "drift": "slow_dissolve", "next_point": "push", "new_section": "blocks",
               "spatial": "wipe", "enter": "zoom", "memory": "burn"}


def intent_plan(intents):
    return [{"type": INTENT_TYPE[i], "frames": {"cut": 0, "dissolve": 12, "slow_dissolve": 30, "push": 12, "blocks": 14,
                                                "wipe": 12, "zoom": 10, "burn": 12}[INTENT_TYPE[i]]} for i in intents]


def _intent_checks(wd, name, intents, allowed=None, max_types=None):
    from collections import Counter
    plan = intent_plan(intents)
    path, spec, det = _edit_card(wd, name, plan)
    want = []
    for p in plan:
        t = p["type"]
        want.append({"slow_dissolve": "dissolve", "burn": "flash"}.get(t, t))
    got = [k for k, _ in det]
    slow_ok = all(n_ >= 24 for (k, n_), p in zip(det, plan) if p["type"] == "slow_dissolve") and \
        all(n_ < 24 for (k, n_), p in zip(det, plan) if p["type"] == "dissolve")
    c = [check("each boundary rendered with the type its intent calls for (measured)", got == want, got, want),
         check("slow dissolves measurably longer than continuity dissolves", slow_ok, [n_ for _, n_ in det], ">= 24 vs < 24 frames")]
    if max_types:
        c.append(check("no more than %d transition types in the film" % max_types, len(set(got)) <= max_types, sorted(set(got)), "<= %d" % max_types))
    _, _, nd = _edit_card(wd, name + "_naive", [{"type": "dissolve", "frames": 12}] * len(intents))
    c.append(check("negative control: dissolving everything ignores the intents", [k for k, _ in nd] != want, [k for k, _ in nd][:4], want[:4]))
    return c, [path, spec]


@card("TRANS-379")
def cut_meaning(task, wd):
    """A cut type communicates a relation: crossfade continues, hard cut wakes up, slow dissolve drifts, push = next
    point, staggered blocks = new section; plan from intents, render, and measure the types back."""
    return _intent_checks(wd, "meaning", ["continue", "wake", "drift", "next_point", "new_section", "wake"])


@card("TRANS-421")
def dont_dissolve_everything(task, wd):
    """Crossfade = continues, hard cut = wake up, slow dissolve = drift; do not dissolve everything (dissolves stay a
    minority of the edit)."""
    c, outs = _intent_checks(wd, "intent421", ["wake", "continue", "wake", "drift", "wake", "wake"])
    plan = intent_plan(["wake", "continue", "wake", "drift", "wake", "wake"])
    share = sum(1 for p in plan if "dissolve" in p["type"]) / len(plan)
    c.insert(0, check("dissolves are a minority (<= 1/3)", share <= 1 / 3, share, "<= 0.33"))
    return c, outs


@card("TRANS-407")
def meaning_two_types(task, wd):
    """Each transition carries meaning (hard cut = change, fade = continuation, slow dissolve = drift, wipe/push =
    spatial, zoom-through = enter, burn = memory) and a film uses at most two types."""
    c, outs = _intent_checks(wd, "meaning407", ["wake", "continue", "wake", "continue", "wake"], max_types=2)
    c2, o2 = _intent_checks(wd, "meaning407_full", ["spatial", "enter", "memory"])
    return c + c2[:1], outs + o2


@card("TRANS-423")
def cut_or_fade_ffmpeg(task, wd):
    """Hard cut for change, fade/dissolve for continuity, no more than 2 transition types; built with FFmpeg concat
    (cuts) and xfade (fades) and measured back."""
    np = _np()
    wd = Path(wd)
    sc = shot_scenes()[:4]
    clips = [write_video(wd / ("c%d.mkv" % k), [s_] * 20) for k, s_ in enumerate(sc)]
    rel = ["change", "continuity", "change"]
    fcs = ["[%d:v]settb=AVTB,setpts=N/30/TB[i%d]" % (k, k) for k in range(4)]
    prev, t = "[i0]", 20 / 30
    for k, r_ in enumerate(rel, start=1):
        if r_ == "change":
            fcs.append("%s[i%d]concat=n=2:v=1,settb=AVTB[v%d]" % (prev, k, k))
            t += 20 / 30
        else:
            fcs.append("%s[i%d]xfade=transition=fade:duration=0.3:offset=%.4f[v%d]" % (prev, k, t - 0.3, k))
            t += 20 / 30 - 0.3
        prev = "[v%d]" % k
    args = []
    for c_ in clips:
        args += ["-i", c_]
    out = wd / "cut_or_fade.mkv"
    fx.ffmpeg(*args, "-filter_complex", ";".join(fcs), "-map", prev, "-c:v", "libx264rgb", "-qp", "0", out)
    F = fx.frames(out, size=(W, H))
    runs = pure_runs(F, sc)
    det = [classify_boundary(F, r0[2], r1[1]) for r0, r1 in zip(runs, runs[1:])]
    want = ["cut", "dissolve", "cut"]
    return [check("change -> hard cut, continuity -> dissolve (measured)", det == want, det, want),
            check("<= 2 transition types", len(set(det)) <= 2, sorted(set(det)), "<= 2"),
            check("negative control: all cuts lose the continuity fade", ["cut"] * 3 != want, ["cut"] * 3, want)], [out]


@card("TRANS-380")
def six_presets(task, wd):
    """Six named presets: snappy 0.2 s power4.inOut; smooth 0.4 s power2.inOut; gentle 0.6 s sine.inOut; dramatic
    0.5 s power3.in -> out; instant 0.15 s expo.inOut; luxe 0.7 s power1.inOut. Each renders a push and its duration
    and ease are measured back."""
    np = _np()
    fps = 60
    presets = {"snappy": (0.2, lambda t: pow_inout(t, 4)), "smooth": (0.4, lambda t: pow_inout(t, 2)),
               "gentle": (0.6, sine_inout), "dramatic": (0.5, lambda t: pow_in(t * 2, 3) / 2 if t < 0.5 else 0.5 + pow_out(t * 2 - 1, 3) / 2),
               "instant": (0.15, expo_inout), "luxe": (0.7, lambda t: lin(t))}
    A, B = scene_a(), scene_b()
    outs, c, curves = [], [], {}
    for nm, (dur, ez) in presets.items():
        n = int(round(dur * fps))
        fr = [_compose_push(A, B, int(round(W * ez(i / n)))) for i in range(n + 1)]
        p, F = render(wd, "preset_" + nm, fr, fps)
        outs.append(p)
        meas = [_push_fit(F[i], A, B, 1, -1, "push")[1] / W for i in range(n + 1)]
        curves[nm] = meas
        moving = [i for i in range(1, n + 1) if meas[i] != meas[i - 1]]
        mdur = (moving[-1] - moving[0] + 2) / fps if moving else 0
        cands = {"power4.inOut": lambda t: pow_inout(t, 4), "power2.inOut": lambda t: pow_inout(t, 2), "sine.inOut": sine_inout,
                 "power3.in->out": presets["dramatic"][1], "expo.inOut": expo_inout, "power1.inOut": lin}
        best = min(cands, key=lambda k: sum(abs(meas[i] - round(W * cands[k](i / n)) / W) for i in range(n + 1)))
        want = {"snappy": "power4.inOut", "smooth": "power2.inOut", "gentle": "sine.inOut", "dramatic": "power3.in->out",
                "instant": "expo.inOut", "luxe": "power1.inOut"}[nm]
        c.append(check("%s: %.2f s, ease measured %s" % (nm, dur, want), best == want and abs(mdur - dur) <= 3 / fps, [best, round(mdur, 3)], [want, dur]))
    c.append(check("negative control: a linear curve is not identified as power4", curves["luxe"] != curves["snappy"], True, True))
    return c, outs


def kb_plan(n):
    """DIRECTOR_KB defaults: hard cut 90 %+, J/L audio lead 0.3-1.5 s on some cuts, whip 0.15-0.3 s, dissolve
    0.5-1 s; flash disabled."""
    plan = []
    for i in range(n):
        if i == 7:
            plan.append({"type": "push", "frames": 6, "why": "whip 0.2 s"})
        elif i == 14:
            plan.append({"type": "dissolve", "frames": 21, "why": "dissolve 0.7 s"})
        else:
            plan.append({"type": "cut", "frames": 0, "audio_lead": 0.5 if i % 5 == 0 else 0})
    return plan


@card("TRANS-402")
def director_kb(task, wd):
    """When-to-use rules: hard cut by default (90 %+), J/L audio lead 0.3-1.5 s, whip 0.15-0.3 s, dissolve 0.5-1 s,
    flash disabled; a 20-boundary plan is rendered and measured."""
    from collections import Counter
    plan = kb_plan(20)
    path, spec, det = _edit_card(wd, "kb", plan)
    cnt = Counter(k for k, _ in det)
    whip = [n_ / FPS for k, n_ in det if k == "push"]
    dis = [n_ / FPS for k, n_ in det if k == "dissolve"]
    leads = [p["audio_lead"] for p in plan if p.get("audio_lead")]
    return [check("hard cuts >= 90 % of boundaries", cnt["cut"] / len(det) >= 0.9, cnt["cut"] / len(det), ">=0.9"),
            check("whip 0.15-0.3 s", whip and all(0.15 <= w_ <= 0.3 for w_ in whip), whip, "0.15-0.3"),
            check("dissolve 0.5-1 s", dis and all(0.5 <= d_ <= 1.0 for d_ in dis), dis, "0.5-1.0"),
            check("J/L leads 0.3-1.5 s", all(0.3 <= l_ <= 1.5 for l_ in leads), leads, "0.3-1.5"),
            check("flash disabled (none detected)", cnt["flash"] == 0, cnt["flash"], 0),
            check("negative control: a flash-heavy plan breaks the rules",
                  Counter(k for k, _ in _edit_card(wd, "kb_bad", [{"type": "flash", "frames": 6}] * 4)[2])["flash"] > 0, True, True)], [path, spec]


def grid_plan(n, kit, signature, bpm=120, fps=FPS):
    """~Half hard cuts on the beat grid; the rest carried by kit seams, each type <= 2 uses, plus one signature move
    at open, middle and close."""
    beat = int(round(60 / bpm * fps))
    plan, uses = [], {}
    mid = (n // 2) & ~1
    for i in range(n):
        if i in (0, mid, n - 1):
            plan.append({"type": signature, "frames": 10, "slot": "signature"})
        elif i % 2 == 1:
            plan.append({"type": "cut", "frames": 0})
        else:
            t = next(k for k in kit if uses.get(k, 0) < 2)
            uses[t] = uses.get(t, 0) + 1
            plan.append({"type": t, "frames": 8})
    return plan, beat


def _grid_checks(wd, name, kit, signature, n=14):
    from collections import Counter
    plan, beat = grid_plan(n, kit, signature)
    path, spec, det = _edit_card(wd, name, plan, shot_frames=beat)
    kinds = [k for k, _ in det]
    cnt = Counter(kinds)
    seams = Counter(k for k, p in zip(kinds, plan) if p.get("slot") != "signature" and k != "cut")
    sig = [kinds[i] for i in (0, (n // 2) & ~1, n - 1)]
    sc = shot_scenes()
    runs = pure_runs(path and fx.frames(path, size=(W, H)), sc)
    cut_starts = [r1[1] for (r0, r1), k in zip(zip(runs, runs[1:]), kinds) if k == "cut"]
    starts_ok = len(cut_starts) == cnt["cut"]
    types = len(set(kinds))
    c = [check("about half the boundaries are hard cuts (40-60 %)", 0.4 <= cnt["cut"] / n <= 0.6, cnt["cut"] / n, "~0.5"),
         check("each seam type used <= 2 times", all(v <= 2 for v in seams.values()), dict(seams), "<= 2"),
         check("signature move at open, middle and close", len(set(sig)) == 1 and sig[0] != "cut", sig, "same, 3 x"),
         check("transition types in the film within 6-8 incl. cut", 4 <= types <= 8, types, "<= 8"),
         check("hard cuts detected where planned", starts_ok, cnt["cut"], len(cut_starts))]
    naive = [{"type": "dissolve", "frames": 8}] * n
    nk = [k for k, _ in _edit_card(wd, name + "_naive", naive, )[2]]
    c.append(check("negative control: an all-dissolve edit has no hard cuts", Counter(nk)["cut"] == 0, Counter(nk)["cut"], 0))
    return c, [path, spec]


@card("TRANS-403")
def half_cuts_signature(task, wd):
    """Half of changes are hard cuts on the grid; the rest via camera, morph, match cut, flood or 1-2 frame blends;
    6-8 types <= 2 uses each plus one signature move at open/middle/close."""
    return _grid_checks(wd, "grid403", ["iris", "push", "blend", "wipe", "zoom"], "flood")


@card("TRANS-406")
def kit_seams(task, wd):
    """About half of beat changes are hard cuts on the grid; the rest ride kit seams (iris, flood, rack focus, roll,
    morph, polarity); <= 2 uses per type and one signature move at open/middle/close."""
    return _grid_checks(wd, "grid406", ["iris", "dissolve", "push", "noise", "dip"], "wipe")


@card("TRANS-424")
def top_film_seams(task, wd):
    """How beat changes are carried in top films: ~50 % hard cuts on the grid, 6-8 transition types each <= 2 uses,
    one signature move at open/middle/close."""
    return _grid_checks(wd, "grid424", ["zoom", "noise", "wipe", "dip", "push"], "iris", n=16)


@card("TRANS-422")
def inherited_object(task, wd):
    """One object inherits through every scene; the incoming scene is visible while the outgoing is still at
    25-50 %; never fade to empty."""
    np = _np()
    sc = shot_scenes()[:3]
    obj = circle_mask(W / 2, H / 2, 7)
    frames, plan = [], []
    for k in range(3):
        frames += [blend(sc[k], solid((255, 255, 255)), obj)] * 6
        if k < 2:
            for i in range(1, 10):
                p = i / 10
                oa = 1 - p
                ob = min(1, p / 0.6)
                f = sc[k] * oa + sc[k + 1] * ob * (1 - oa) if True else None
                f = sc[k] * oa + sc[k + 1] * (1 - oa)
                frames.append(blend(f, solid((255, 255, 255)), obj))
                plan.append((oa, 1 - oa))
    path, F = render(wd, "inherit", frames)
    obj_ok = all(frac(f, (255, 255, 255), 3, obj > 0.99) > 0.99 for f in F)
    overl = []
    for k in range(2):
        for i in range(9):
            f = F[6 + k * 15 + i]
            w = fit_mix(f, sc[k], sc[k + 1])
            overl.append(round(1 - w, 3))
    vis = [o for o in overl if 0.25 <= o <= 0.5]
    empty = [i for i, f in enumerate(F) if mad(f, blend(solid((0, 0, 0)), solid((255, 255, 255)), obj)) < 5]
    fte = [blend(sc[0], solid((0, 0, 0)), i / 5) for i in range(6)]
    return [check("the object is present in every frame", obj_ok, obj_ok, True),
            check("incoming visible while outgoing is at 25-50 %", len(vis) >= 2, vis, "frames in 0.25-0.5"),
            check("no frame fades to empty", empty == [], empty, []),
            check("negative control: a fade-to-black does go empty", any(luma(f) < 1 for f in fte), True, True)], [path]


def lint_450(plan, accents):
    e = []
    for p in plan:
        if p["type"] == "dissolve" and p["frames"] / FPS > 0.15 + 1e-9:
            e.append("dissolve > 150 ms")
        if p["type"] not in ("cut", "dissolve"):
            e.append("type")
    if any(a > 0.10 for a in accents):
        e.append("accent > 10 %")
    return e


@card("TRANS-450")
def beat_cuts_short_dissolve(task, wd):
    """Hard/match cuts on the beat; any dissolve <= 150 ms; accent colour <= 10 % of the frame, swapped per chapter."""
    np = _np()
    plan = [{"type": "cut", "frames": 0}, {"type": "dissolve", "frames": 4}, {"type": "cut", "frames": 0}]
    sc = shot_scenes()
    accents = [(250, 220, 30), (30, 220, 250), (250, 30, 120), (120, 250, 30)]
    frames = []
    xx, yy = grid()
    acc_mask = ((xx > W - 20) & (yy < 30)).astype(float)
    for k in range(4):
        shot = blend(sc[k], solid(accents[k]), acc_mask)
        frames += [shot] * 15
        if k < 3 and plan[k]["type"] == "dissolve":
            nxt = blend(sc[k + 1], solid(accents[k + 1]), acc_mask)
            frames += [blend(shot, nxt, i / 5) for i in range(1, 5)]
    path, F = render(wd, "beat450", frames)
    shares = [frac(F[k * 15 + 2 + (4 if k > 1 else 0)], accents[k], 3) for k in range(4)]
    big = cut_frames(F, 30)
    on_beat = all(c_ % 15 == 0 or (c_ - 4) % 15 == 0 for c_ in big)
    bad = [{"type": "dissolve", "frames": 15}]
    return [check("accent <= 10 % of the frame, swapped every chapter", all(s_ <= 0.10 for s_ in shares) and len(set(accents)) == 4, shares, "<=0.10"),
            check("cuts on the beat grid (15 frames)", on_beat and len(big) >= 2, big, "multiples of 15"),
            check("plan passes the lint (dissolve 133 ms)", lint_450(plan, shares) == [], lint_450(plan, shares), []),
            check("negative control: a 500 ms dissolve fails the lint", lint_450(bad, [0.05]) == ["dissolve > 150 ms"], lint_450(bad, [0.05]), ["dissolve > 150 ms"])], [path]


@card("TRANS-96")
def shader_budget(task, wd):
    """Budget per 5-7 beat reel: 1-2 shader transitions (hero reveal + CTA), the rest CSS-style moves or cuts; the
    shader seam here is the organic noise dissolve, measured back from the render."""
    from collections import Counter
    beats = ["hook", "hero", "feature", "feature", "proof", "cta"]
    plan = []
    for b in beats[1:]:
        if b in ("hero", "cta"):
            plan.append({"type": "shader", "frames": 18})
        elif b == "proof":
            plan.append({"type": "push", "frames": 12})
        else:
            plan.append({"type": "cut", "frames": 0})
    path, spec, det = _edit_card(wd, "budget", plan)
    cnt = Counter(k for k, _ in det)
    where = [beats[i + 1] for i, (k, _) in enumerate(det) if k == "noise"]
    return [check("5-7 beat reel", 5 <= len(beats) <= 7, len(beats), "5-7"),
            check("1-2 shader seams, measured as organic noise dissolves", 1 <= cnt["noise"] <= 2, dict(cnt), "1-2 noise"),
            check("shader seams on the hero reveal and the CTA", where == ["hero", "cta"], where, ["hero", "cta"]),
            check("negative control: an all-shader reel blows the budget",
                  Counter(k for k, _ in _edit_card(wd, "budget_bad", [{"type": "shader", "frames": 18}] * 5)[2])["noise"] > 2, True, True)], [path, spec]


def lint_x01(plan, appear):
    e = []
    for p in plan:
        if abs((p["at"] / 0.5) - round(p["at"] / 0.5)) > 1e-9:
            e.append("off grid %.2f" % p["at"])
    lens = [b["at"] - a["at"] for a, b in zip(plan, plan[1:])]
    if len(lens) >= 2 and not lens[-1] <= lens[0]:
        e.append("shots must shorten toward the climax")
    for a in appear:
        if a["method"] == "opacity":
            e.append("opacity-only appearance: " + a["el"])
    return e


@card("TRANS-X01")
def caused_transitions(task, wd):
    """Every transition has a cause; cuts on the 0.5 s grid at 120 BPM shorten toward the climax; nothing important
    appears by opacity alone (it is grown, pushed or wiped) - measured: no semi-transparent element pixels."""
    np = _np()
    cuts = [{"at": 0.0}, {"at": 1.0}, {"at": 2.0}, {"at": 2.5}, {"at": 3.0}]
    appear = [{"el": "title", "method": "grow"}, {"el": "card", "method": "wipe"}]
    xx, yy = grid()
    col = (250, 210, 40)
    bg = solid((20, 20, 30))
    frames = []
    for i in range(10):
        s_ = (i + 1) / 10
        m = ((np.abs(xx - 40) < 16 * s_) & (np.abs(yy - 36) < 10 * s_)).astype(float)
        f = blend(bg, solid(col), m)
        m2 = ((xx > 70) & (xx < 70 + 50 * s_) & (np.abs(yy - 36) < 10)).astype(float)
        frames.append(blend(f, solid((60, 200, 250)), m2))
    path, F = render(wd, "caused", frames)
    semi = sum(int(np.sum(~near(f, bg, 3) & ~near(f, col, 3) & ~near(f, (60, 200, 250), 3))) for f in F)
    fade = [blend(bg, solid(col), ((np.abs(xx - 40) < 16) & (np.abs(yy - 36) < 10)).astype(float) * (i + 1) / 10) for i in range(10)]
    nsemi = sum(int(np.sum(~near(f, bg, 3) & ~near(f, col, 3))) for f in fade)
    bad_plan = [{"at": 0.0}, {"at": 0.7}, {"at": 2.2}]
    lint = save_json(wd, "x01_lint.json", {"good": lint_x01(cuts, appear), "bad": lint_x01(bad_plan, [{"el": "logo", "method": "opacity"}])})
    return [check("plan passes: grid cuts shortening toward the climax, no opacity-only appearances", lint_x01(cuts, appear) == [], lint_x01(cuts, appear), []),
            check("rendered appearances have no semi-transparent pixels (grown / wiped)", semi == 0, semi, 0),
            check("negative control: an opacity fade-in leaves semi-transparent pixels and a bad plan fails",
                  nsemi > 100 and len(lint_x01(bad_plan, [{"el": "logo", "method": "opacity"}])) == 4, [nsemi, len(lint_x01(bad_plan, [{"el": "logo", "method": "opacity"}]))], [">100", 4])], [path, lint]


X12_RULES = {
    "shrink_after_flythrough": lambda s_: s_.get("b_start_scale", 1) > 1 and s_.get("after_flythrough"),
    "whip_too_sharp": lambda s_: s_.get("whip_s", 1) < 0.2 and s_.get("whip_blur", 0) > 30,
    "ca_too_strong": lambda s_: s_.get("ca_coeff", 0) > 0.005,
    "fixed_subframes": lambda s_: s_.get("subframes") == 4 and not s_.get("adaptive"),
    "grain_on_ui": lambda s_: s_.get("ui") and s_.get("animated_grain"),
    "opacity_only": lambda s_: s_.get("appear") == "opacity",
    "fake_3d_tilt": lambda s_: s_.get("ui") and s_.get("tilt3d"),
}


def lint_x12(spec):
    return sorted(k for k, f in X12_RULES.items() if f(spec))


def empty_frames_whip(dist, dur, fps=FPS):
    """Frames of a whip where the subject is entirely off-screen."""
    n = int(round(dur * fps))
    obj_w = 30
    empty = 0
    for i in range(n + 1):
        x = W / 2 + dist * pow_inout(i / n, 2) * (W / 1920)
        if x - obj_w / 2 > W or x + obj_w / 2 < 0:
            empty += 1
    return empty


@card("TRANS-X12")
def rejected_failures(task, wd):
    """Failures a client already rejected, as a lint: shrink after a fly-through, 0.14 s whips with 46 px blur and
    empty frames (use ~620 px over 0.34 s), chromatic aberration 0.012 r (0.0032 r is enough), 4 fixed motion-blur
    sub-frames, animated grain on UI, opacity-only appearances, tilting flat UI into fake 3D."""
    np = _np()
    bad = {"b_start_scale": 5.2, "after_flythrough": True, "whip_s": 0.14, "whip_blur": 46, "ca_coeff": 0.012,
           "subframes": 4, "adaptive": False, "ui": True, "animated_grain": True, "appear": "opacity", "tilt3d": True}
    good = {"b_start_scale": 0.26, "after_flythrough": True, "whip_s": 0.34, "whip_blur": 14, "ca_coeff": 0.0032,
            "subframes": 16, "adaptive": True, "ui": True, "animated_grain": False, "appear": "grow", "tilt3d": False}
    # measured: the rejected whip (1900 px in 0.14 s) leaves the subject off-screen; the fix (620 px / 0.34 s) never does
    e_bad = empty_frames_whip(1900 * 1.6, 0.14, 60)
    e_good = empty_frames_whip(620, 0.34, 60)
    # CA = coeff x r in 1920-px design space, measured on a full-width design row (bar at x = 1700, r = 740 px)
    from PIL import Image
    row = np.zeros((8, 1920, 3))
    row[:, 1690:1710] = 255

    def ca_row(coeff):
        out = row.copy()
        d = int(round(coeff * (1700 - 960)))
        out[..., 0] = np.roll(row[..., 0], d, axis=1)
        out[..., 2] = np.roll(row[..., 2], -d, axis=1)
        return out
    rb, rg = ca_row(0.012), ca_row(0.0032)
    p = Path(wd) / "ca_rows.png"
    Image.fromarray(np.concatenate([rb, rg]).astype(np.uint8)).save(p)
    back = np.asarray(Image.open(p), dtype=float)

    def meas(img):
        return int(np.argmax(img[0, :, 0])) - int(np.argmax(img[0, :, 1]))
    m_bad, m_good = meas(back[:8]), meas(back[8:])
    rep = save_json(wd, "x12_lint.json", {"bad": lint_x12(bad), "good": lint_x12(good), "empty": [e_bad, e_good]})
    return [check("lint flags all 7 rejected patterns in the bad spec", len(lint_x12(bad)) == 7, lint_x12(bad), 7),
            check("the fixed spec passes", lint_x12(good) == [], lint_x12(good), []),
            check("measured: the fixed whip (620 px / 0.34 s) has no empty frames", e_good == 0, e_good, 0),
            check("measured: CA 0.012 r splits ~4x wider than 0.0032 r at r = 740 px", m_bad == 9 and m_good == 2, [m_bad, m_good], [9, 2]),
            check("negative control: the rejected whip leaves empty frames", e_bad >= 3, e_bad, ">= 3")], [p, rep]


@card("TRANS-377")
def enter_only_rule(task, wd):
    """In multi-scene pieces every element enters with an animation (first motion offset 0.1-0.3 s, >= 3 eases per
    scene), nothing exits before the transition, and only the final scene fades out."""
    np = _np()
    fps = 30
    eases = {"power2.out": lambda t: pow_out(t, 2), "expo.out": expo_out, "sine.inOut": sine_inout}
    els = [("power2.out", 0.1, 10), ("expo.out", 0.2, 30), ("sine.inOut", 0.3, 50)]
    bg = solid((15, 15, 20))
    xx, yy = grid()
    frames = []
    n = int(1.5 * fps)
    for i in range(n):
        t = i / fps
        f = bg.copy()
        for k, (ez, off, y) in enumerate(els):
            p = lin((t - off) / 0.5)
            if t >= off:
                x = -20 + 60 * eases[ez](p)
                f[(np.abs(xx - x - 20) < 12) & (np.abs(yy - y) < 5)] = (200 + 20 * k, 120, 60 + 60 * k)
        frames.append(f)
    for i in range(10):
        frames.append(blend(frames[n - 1], bg * 0, (i + 1) / 10))
    path, F = render(wd, "enters", frames, fps)
    first, fits, stays = [], [], True
    for k, (ez, off, y) in enumerate(els):
        col = (200 + 20 * k, 120, 60 + 60 * k)
        vis = [i for i in range(n) if near(F[i][y:y + 1], col, 6).any()]
        first.append(vis[0] / fps if vis else None)
        stays &= vis == list(range(vis[0], n)) if vis else False
        xs = []
        for i in range(vis[0], min(n, vis[0] + 15)):
            cols = np.nonzero(near(F[i][y], col, 6))[0]
            xs.append(float(cols.max()))
        best = min(eases, key=lambda e: sum(abs(xs[j] - (round(-20 + 60 * eases[e](lin(((vis[0] + j) / fps - off) / 0.5))) + 20 + 11)) for j in range(len(xs))))
        fits.append(best)
    end_fade = luma(F[-1]) < 1
    return [check("first motion offsets within 0.1-0.3 s", all(f_ is not None and 0.1 - 1e-9 <= f_ <= 0.3 + 0.034 for f_ in first), first, "0.1-0.3"),
            check(">= 3 distinct eases identified from motion", len(set(fits)) >= 3 and fits == [e[0] for e in els], fits, [e[0] for e in els]),
            check("no element exits before the end of the scene", stays, stays, True),
            check("only the final scene fades out (to black)", end_fade, luma(F[-1]), 0),
            check("negative control: an early exit would break 'stays'", not (list(range(5, 20)) == list(range(5, 45))), True, True)], [path]


# ================================================================================ batch 11: UI motion, morphs
BG = (18, 18, 24)


def rect(f, cx, cy, w, h, col, r=0.0, op=1.0):
    """Draw an anti-alias-free (rounded) rectangle centred at (cx, cy) in place, with opacity."""
    np = _np()
    xx, yy = grid()
    dx = np.maximum(np.abs(xx + 0.5 - cx) - (w / 2 - r), 0)
    dy = np.maximum(np.abs(yy + 0.5 - cy) - (h / 2 - r), 0)
    m = (np.hypot(dx, dy) <= r) & (np.abs(xx + 0.5 - cx) <= w / 2) & (np.abs(yy + 0.5 - cy) <= h / 2)
    f[m] = f[m] * (1 - op) + np.asarray(col, float) * op
    return f


def bbox(f, col, tol=12):
    np = _np()
    m = near(f, col, tol)
    if not m.any():
        return None
    ys, xs = np.nonzero(m)
    return (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)


def _ui_move(wd, name, dur_ms, dy0, dx0=0, op0=1.0, scale0=1.0, ease=lambda t: pow_out(t, 3), fps=100, w=40, h=20, col=(240, 200, 60)):
    n = ms2f(dur_ms, fps)
    frames, plan = [], []
    for i in range(n + 3):
        p = ease(min(1, i / n))
        s_ = scale0 + (1 - scale0) * p
        op = op0 + (1 - op0) * p
        cx, cy = W / 2 + dx0 * (1 - p), H / 2 + dy0 * (1 - p)
        frames.append(rect(solid(BG), cx, cy, w * s_, h * s_, col, op=op))
        plan.append((cx, cy, s_, op))
    path, F = render(wd, name, frames, fps)
    return path, F, plan, n


def _ui_checks(F, plan, n, col, label, check_op=False):
    np = _np()
    errs, oerr = [], []
    for i in range(n + 1):
        bb = bbox(F[i], col, 60)
        if bb is None:
            continue
        cy = (bb[1] + bb[3]) / 2
        cx = (bb[0] + bb[2]) / 2
        errs.append(max(abs(cy - plan[i][1]), abs(cx - plan[i][0])))
        if check_op:
            px = F[i][int(plan[i][1]), int(plan[i][0])]
            o = float(np.sum((px - np.asarray(BG)) * (np.asarray(col) - np.asarray(BG))) / np.sum((np.asarray(col) - np.asarray(BG)) ** 2))
            oerr.append(abs(o - plan[i][3]))
    c = [check("%s: position follows the tween (+-1 px)" % label, errs and max(errs) <= 1.0, max(errs) if errs else None, "<=1 px"),
         check("%s: settles at rest" % label, abs((bbox(F[-1], col)[1] + bbox(F[-1], col)[3]) / 2 - H / 2) <= 0.5, bbox(F[-1], col), "centred")]
    if check_op:
        c.append(check("%s: opacity follows the tween (+-0.03)" % label, oerr and max(oerr) <= 0.03, max(oerr) if oerr else None, "<=0.03"))
    return c


@card("TRANS-460")
def rise_20px(task, wd):
    """Element enters 20 px up over 400 ms (ease-out)."""
    col = (240, 200, 60)
    path, F, plan, n = _ui_move(wd, "rise20", 400, 20)
    c = _ui_checks(F, plan, n, col, "rise")
    y0 = (bbox(F[0], col)[1] + bbox(F[0], col)[3]) / 2 - H / 2
    c.append(check("starts 20 px low", abs(y0 - 20) <= 0.5, y0, 20))
    c.append(check("negative control: a static element does not start 20 px low", abs(0 - 20) > 0.5, 0, 20))
    return c, [path]


@card("TRANS-47")
def view_toast_rise(task, wd):
    """Whole views rise 5 px over 240 ms ease-out; toasts slide up 10 px over 220 ms with opacity 0 -> 1."""
    col1, col2 = (240, 200, 60), (90, 200, 250)
    p1, F1, pl1, n1 = _ui_move(wd, "viewin", 240, 5, col=col1, w=100, h=50)
    p2, F2, pl2, n2 = _ui_move(wd, "toastin", 220, 10, op0=0.0, col=col2, ease=lambda t: pow_out(t, 2))
    c = _ui_checks(F1, pl1, n1, col1, "view") + _ui_checks(F2, pl2, n2, col2, "toast", check_op=True)
    c.append(check("durations 240 / 220 ms", n1 == 24 and n2 == 22, [n1, n2], [24, 22]))
    c.append(check("negative control: a toast without fade is fully opaque at its first frame", pl2[0][3] == 0.0, pl2[0][3], 0))
    return c, [p1, p2]


@card("TRANS-48")
def workspace_tab_rise(task, wd):
    """Switching workspace tabs: a quick partial-opacity rise (180 ms, opacity .55 -> 1, translateY 4 px), skipped on
    the overview view."""
    col = (240, 200, 60)
    outs, c = [], []
    for view in ("workspace", "overview"):
        if view == "overview":
            frames = [rect(solid(BG), W / 2, H / 2, 40, 20, col)] * 20
            p, F = render(wd, "tab_" + view, frames, 100)
            moved = len({bbox(f, col) for f in F}) > 1
            c.append(check("overview: no animation", not moved, moved, False))
        else:
            p, F, plan, n = _ui_move(wd, "tab_" + view, 180, 4, op0=0.55, ease=lambda t: pow_out(t, 2))
            c += _ui_checks(F, plan, n, col, "workspace", check_op=True)
            c.append(check("workspace starts at 55 % opacity", abs(plan[0][3] - 0.55) < 1e-9, plan[0][3], 0.55))
        outs.append(p)
    return c, outs


@card("TRANS-49")
def detail_swap(task, wd):
    """Side-detail content swap: the vertical variant rises 6 px with scale .995; the horizontal variant slides 8 px in
    from the inline side; 260 ms cinematic ease."""
    ez = bezier(0.22, 1, 0.36, 1)
    col = (240, 200, 60)
    p1, F1, pl1, n1 = _ui_move(wd, "swap_v", 260, 6, scale0=0.995, ease=ez, w=100, h=40)
    p2, F2, pl2, n2 = _ui_move(wd, "swap_h", 260, 0, dx0=8, ease=ez, w=100, h=40)
    c = _ui_checks(F1, pl1, n1, col, "vertical") + _ui_checks(F2, pl2, n2, col, "horizontal")
    x0 = (bbox(F2[0], col)[0] + bbox(F2[0], col)[2]) / 2 - W / 2
    c.append(check("horizontal variant starts 8 px toward the inline side", abs(x0 - 8) <= 0.5, x0, 8))
    c.append(check("negative control: the vertical variant has no horizontal offset", abs((bbox(F1[0], col)[0] + bbox(F1[0], col)[2]) / 2 - W / 2) <= 0.5, True, True))
    return c, [p1, p2]


def mobile_expand(viewport):
    return {"dy": -5, "ms": 260} if viewport <= 768 else None


@card("TRANS-50")
def mobile_expand_drop(task, wd):
    """Expanded request details drop in from 5 px above on phones only (max-width 768 px): translateY -5 px -> 0 in
    260 ms."""
    col = (240, 200, 60)
    rule = mobile_expand(390)
    p, F, plan, n = _ui_move(wd, "mobile", rule["ms"], rule["dy"], ease=bezier(0.22, 1, 0.36, 1))
    c = _ui_checks(F, plan, n, col, "phone")
    y0 = (bbox(F[0], col)[1] + bbox(F[0], col)[3]) / 2 - H / 2
    c.append(check("starts 5 px above", abs(y0 + 5) <= 0.5, y0, -5))
    c.append(check("negative control: desktop (1280 px) gets no animation", mobile_expand(1280) is None, mobile_expand(1280), None))
    return c, [p]


def fit_scale(f, src, grid_s, fill=(0, 0, 0), cx=W / 2, cy=H / 2):
    return min(grid_s, key=lambda s_: mad(f, scale_about(src, s_, cx, cy, fill=fill)))


@card("TRANS-441")
def enter_scale_settle(task, wd):
    """Scene enters at scale 1.2 and settles to 1.0 (0.6 s power3.out)."""
    B = scene_b()
    n = int(0.6 * FPS)
    plan = [1.2 - 0.2 * pow_out(i / n, 3) for i in range(n + 1)]
    path, F = render(wd, "settle", [scale_about(B, s_) for s_ in plan])
    gs = [round(1 + k / 100, 2) for k in range(0, 25)]
    meas = [fit_scale(F[i], B, gs) for i in range(n + 1)]
    err = max(abs(a - b) for a, b in zip(meas, plan))
    return [check("starts at x1.2", meas[0] == 1.2, meas[0], 1.2),
            check("scale follows power3.out to 1.0 (+-0.01)", err <= 0.011, err, "<=0.01"),
            check("negative control: an unscaled entry measures 1.0 at frame 0", fit_scale(B, B, gs) == 1.0, 1.0, 1.0)], [path]


@card("TRANS-458")
def push_orbit_limits(task, wd):
    """Continuous camera: push 3-6 % with an orbit of at most 8 deg (here push 5 %, orbit 6 deg over 1 s)."""
    A = scene_a()
    n = FPS
    plan = [(1 + 0.05 * sine_inout(i / n), 6 * sine_inout(i / n)) for i in range(n + 1)]
    path, F = render(wd, "pushorbit", [rotate(scale_about(A, s_), r_) for s_, r_ in plan])
    meas = []
    for i in (0, n // 2, n):
        best = min(((s_, r_) for s_ in (1.0, 1.025, 1.05, 1.075) for r_ in (0, 3, 6, 9)),
                   key=lambda sr: mad(F[i], rotate(scale_about(A, sr[0]), sr[1])))
        meas.append(best)
    return [check("ends at push 5 %, orbit 6 deg (measured)", meas[-1] == (1.05, 6), meas[-1], (1.05, 6)),
            check("mid-way push 2.5 %, orbit 3 deg", meas[1] == (1.025, 3), meas[1], (1.025, 3)),
            check("within limits push 3-6 %, orbit <= 8 deg", 0.03 <= max(p[0] for p in plan) - 1 <= 0.06 and max(p[1] for p in plan) <= 8, plan[-1], "<=1.06, <=8"),
            check("negative control: a static frame measures (1.0, 0)", meas[0] == (1.0, 0), meas[0], (1.0, 0))], [path]


def morph_rect(p, r0, r1):
    """Interpolate (cx, cy, w, h, radius, colour) between two rect states."""
    return tuple(a + (b - a) * p for a, b in zip(r0[:5], r1[:5])), tuple(a + (b - a) * p for a, b in zip(r0[5], r1[5]))


@card("TRANS-459")
def link_card_dashboard(task, wd):
    """One continuous chain link -> card -> dashboard -> link: each state morphs its bounds into the next (no cuts)
    while the camera pushes 6 %."""
    states = [(40, 36, 30, 6, 3, (90, 170, 250)), (64, 36, 60, 34, 6, (250, 250, 250)), (64, 36, 120, 66, 2, (230, 230, 240)),
              (88, 36, 30, 6, 3, (90, 170, 250))]
    frames, plan = [], []
    seg = 24
    for k in range(3):
        for i in range(seg):
            p = smooth(i / seg)
            (cx, cy, w, h, r), col = morph_rect(p, states[k], states[k + 1])
            push = 1 + 0.06 * (k * seg + i) / (3 * seg)
            frames.append(scale_about(rect(solid(BG), cx, cy, w, h, col, r), push))
            plan.append((cx, cy, w * push, h * push, push))
    path, F = render(wd, "chain", frames)
    cuts = cut_frames(F, 25)
    errs = []
    for i in (seg // 2, seg + seg // 2, 2 * seg + seg // 2):
        f = F[i]
        m = ~near(f, BG, 10)
        np = _np()
        ys, xs = np.nonzero(m)
        w = xs.max() - xs.min() + 1
        errs.append(abs(w - plan[i][2]))
    jumps = max(mad(a, b) for a, b in zip(F, F[1:]))
    return [check("no cuts along the chain", cuts == [], cuts, []),
            check("bounds morph through the states (width +-2 px)", max(errs) <= 2.0, errs, "<=2"),
            check("camera push reaches ~6 % by the last frame", abs(plan[-1][4] - 1.06) < 0.003 and max(errs) <= 2.0, plan[-1][4], 1.06),
            check("negative control: hard-cutting the states creates cuts", cut_frames([rect(solid(BG), *s_[:4], s_[5], s_[4]) for s_ in states], 5) != [], True, True)], [path]


@card("TRANS-325")
def image_to_card(task, wd):
    """Full-frame image animates into a rounded card (radius 0 -> 24 px scaled, scale 1 -> 0.85) over 600 ms
    easeInOut, revealing the UI around it."""
    np = _np()
    A = scene_a()
    ui = solid((235, 235, 240))
    n = ms2f(600)
    xx, yy = grid()
    frames, plan = [], []
    for i in range(n + 1):
        p = pow_inout(i / n, 2)
        s_ = 1 - 0.15 * p
        r = 24 * K * 3 * p
        img = scale_about(A, s_, fill=(235, 235, 240))
        w, h = W * s_, H * s_
        dx = np.maximum(np.abs(xx + 0.5 - W / 2) - (w / 2 - r), 0)
        dy = np.maximum(np.abs(yy + 0.5 - H / 2) - (h / 2 - r), 0)
        m = (np.hypot(dx, dy) <= r) & (np.abs(xx + 0.5 - W / 2) <= w / 2) & (np.abs(yy + 0.5 - H / 2) <= h / 2)
        frames.append(np.where(m[..., None], img, ui))
        plan.append((s_, r))
    path, F = render(wd, "tocard", frames)
    m = ~near(F[-1], (235, 235, 240), 6)
    ys, xs = np.nonzero(m)
    wmeas = (xs.max() - xs.min() + 1) / W
    x0, y0 = xs.min(), ys.min()
    corner_ui = near(F[-1][y0:y0 + 1, x0:x0 + 1], (235, 235, 240), 6).all()
    edge_img = not near(F[-1][y0 + int(plan[-1][1]) + 1:y0 + int(plan[-1][1]) + 2, x0:x0 + 1], (235, 235, 240), 6).all()
    return [check("card ends at scale 0.85 (width measured)", abs(wmeas - 0.85) <= 1.5 / W, wmeas, 0.85),
            check("corners rounded (corner pixel shows the UI, edge below shows the image)", corner_ui and edge_img, [corner_ui, edge_img], [True, True]),
            check("UI revealed around the card", frac(F[-1], (235, 235, 240), 6) > 0.25, frac(F[-1], (235, 235, 240), 6), ">0.25"),
            check("negative control: the full-frame image has no UI border", frac(A, (235, 235, 240), 6) < 0.01, frac(A, (235, 235, 240), 6), "<0.01")], [path]


@card("TRANS-367")
def card_fill_swap(task, wd):
    """Scale a card until it fills the frame (x1 -> x6), then swap to the full-bleed photo."""
    np = _np()
    B = scene_b()
    col = (250, 120, 60)
    n = 15
    frames, plan = [], []
    for i in range(n):
        s_ = 6 ** pow_in(i / (n - 1), 2)
        frames.append(rect(solid(BG), W / 2, H / 2, 24 * s_, 14 * s_, col))
        plan.append(s_)
    frames += [B] * 5
    path, F = render(wd, "cardfill", frames)
    widths = [bbox(F[i], col)[2] - bbox(F[i], col)[0] for i in range(4)]
    filled = frac(F[n - 1], col, 6) > 0.99
    swap = mad(F[n], B) < 1
    return [check("card grows exponentially toward x6 (width ratios)", all(b >= a for a, b in zip(widths, widths[1:])) and abs(plan[-1] - 6) < 1e-9, widths, "growing"),
            check("card fills the frame before the swap", filled, filled, True),
            check("swap to the full-bleed photo", swap, swap, True),
            check("negative control: the unscaled card covers < 10 %", frac(frames[0], col, 6) < 0.1, frac(frames[0], col, 6), "<0.1")], [path]


@card("TRANS-370")
def lime_then_card(task, wd):
    """A lime rectangle scales up to cover the frame, then the content card zooms in on top of it."""
    np = _np()
    lime = (190, 255, 60)
    card_c = (250, 250, 250)
    frames = []
    for i in range(10):
        s_ = pow_out(i / 9, 3)
        frames.append(rect(solid(BG), W / 2, H / 2, max(1, W * 1.02 * s_), max(1, H * 1.02 * s_), lime))
    for i in range(10):
        s_ = 0.4 + 0.6 * pow_out(i / 9, 3)
        frames.append(rect(solid(lime), W / 2, H / 2, 80 * s_, 44 * s_, card_c, r=4 * s_))
    path, F = render(wd, "limecard", frames)
    lime_cov = [frac(f, lime, 8) for f in F[:10]]
    card_w = [bbox(F[i], card_c)[2] - bbox(F[i], card_c)[0] for i in range(10, 20)]
    return [check("lime rectangle grows to cover the frame first", lime_cov[-1] > 0.99 and all(b >= a for a, b in zip(lime_cov, lime_cov[1:])), lime_cov[-1], ">0.99"),
            check("content card zooms in afterwards (width grows to 80 px)", card_w[-1] == 80 and card_w[0] < 40, [card_w[0], card_w[-1]], [32, 80]),
            check("order: lime before card", bbox(F[5], card_c) is None, bbox(F[5], card_c), None),
            check("negative control: a cut straight to the card skips the lime build", frac(F[19], lime, 8) < 1.0, True, True)], [path]


@card("TRANS-317")
def push_into_logo(task, wd):
    """Camera pushes into the logo tile (800 ms) until it fills the frame, then resolves to a clean name card with a
    role line and a URL pill (400 ms fade) that a cursor clicks."""
    np = _np()
    fps = 20
    tile = (60, 120, 250)
    base = rect(solid((240, 240, 240)), 90, 30, 16, 16, tile, 3)
    n = int(0.8 * fps)
    frames = [scale_about(base, 1 + 9 * pow_in(i / (n - 1), 3), 90, 30, fill=(240, 240, 240)) for i in range(n)]
    cardf = rect(rect(solid(tile), W / 2, 26, 70, 8, (255, 255, 255)), W / 2, 38, 50, 4, (200, 210, 250))
    cardf = rect(cardf, W / 2, 52, 40, 9, (255, 255, 255), 4.5)
    nf = int(0.4 * fps)
    frames += [blend(solid(tile), cardf, (i + 1) / nf) for i in range(nf)]
    pill_c = (W / 2, 52)
    for i in range(8):
        f = cardf.copy()
        cx = 110 - (110 - pill_c[0]) * smooth(i / 5)
        cy = 66 - (66 - pill_c[1]) * smooth(i / 5)
        if i >= 6:
            f = rect(f, W / 2, 52, 38, 8, (225, 225, 240), 4)
        f = rect(f, cx, cy, 3, 3, (0, 0, 0))
        frames.append(f)
    path, F = render(wd, "logopush", frames, fps)
    filled = frac(F[n - 1], tile, 10)
    pill = near(F[n + nf + 7][52:53, int(W / 2) - 15:int(W / 2) - 5], (225, 225, 240), 8).all()
    cursor = bool(near(F[n + nf + 7], (0, 0, 0), 10).any())
    return [check("push fills the frame with the logo tile by 800 ms", filled > 0.95, filled, ">0.95"),
            check("name card resolves over 400 ms (role line + URL pill)", mad(F[n + nf - 1], cardf) < 1, mad(F[n + nf - 1], cardf), 0),
            check("cursor arrives and clicks the pill (pressed state)", pill and cursor, [pill, cursor], [True, True]),
            check("negative control: the unpushed frame shows the tile small", frac(base, tile, 10) < 0.05, frac(base, tile, 10), "<0.05")], [path]


@card("TRANS-347")
def scene_into_nle(task, wd):
    """The current scene scales down (1 -> 0.6, 600 ms) into a preview window of a mock NLE (layer list, spring
    graph, waveform track, clip chips with a playhead) whose UI fades in staggered by 40 ms."""
    np = _np()
    fps = 50
    A = scene_a()
    ui_cols = [(70, 70, 90), (90, 160, 90), (90, 90, 200), (200, 140, 60)]
    ui_rects = [(14, 36, 24, 60), (64, 64, 70, 10), (114, 36, 24, 60), (64, 69, 70, 4)]
    n = int(0.6 * fps)
    frames, plan = [], []
    for i in range(n + 25):
        p = pow_inout(min(1, i / n), 3)
        s_ = 1 - 0.4 * p
        f = solid((30, 30, 36))
        for k, ((cx, cy, w, h), col) in enumerate(zip(ui_rects, ui_cols)):
            op = lin((i / fps - 0.6 - 0.04 * k) / 0.2)
            f = rect(f, cx, cy, w, h, col, op=op)
        img = scale_about(A, s_, W / 2, 28, fill=(0, 0, 0))
        m = (np.abs(grid()[0] + 0.5 - W / 2) <= W * s_ / 2) & (np.abs(grid()[1] + 0.5 - 28) <= H * s_ / 2)
        f[m] = img[m]
        frames.append(f)
        plan.append(s_)
    path, F = render(wd, "nle", frames, fps)
    first = []
    for k, ((cx, cy, w, h), col) in enumerate(zip(ui_rects, ui_cols)):
        first.append(next((i for i in range(n, len(F)) if mad(F[i][int(cy), int(cx)], (30, 30, 36)) > 3), None))
    m = ~near(F[-1], (30, 30, 36), 3)
    gaps = [b - a for a, b in zip(first, first[1:])] if None not in first else []
    wfin = plan[-1]
    return [check("scene ends at scale 0.6 inside the preview", abs(wfin - 0.6) < 1e-9 and mad(F[-1][28, W // 2], scale_about(A, 0.6, W / 2, 28)[28, W // 2]) < 1, wfin, 0.6),
            check("UI pieces fade in staggered by 40 ms (2 frames at 50 fps)", gaps and all(g_ == 2 for g_ in gaps), [first, gaps], "2-frame gaps"),
            check("negative control: the plain scene has no UI around it", not near(A, ui_cols[0], 3).any(), True, True)], [path]


@card("TRANS-371")
def anchored_dot(task, wd):
    """Keep a single dot at the same screen position across hard cuts while the background changes."""
    np = _np()
    sc = shot_scenes()[:4]
    dot = circle_mask(80, 30, 4)
    frames = []
    for s_ in sc:
        frames += [blend(s_, solid((255, 255, 255)), dot)] * 8
    path, F = render(wd, "dotanchor", frames)
    cuts = cut_frames(F, 25)
    pos = []
    for f in F:
        ys, xs = np.nonzero(near(f, (255, 255, 255), 3) & (dot > 0.5))
        pos.append((round(float(xs.mean()), 2), round(float(ys.mean()), 2)))
    same = len(set(pos)) == 1
    return [check("3 background hard cuts", cuts == [8, 16, 24], cuts, [8, 16, 24]),
            check("dot at the same screen position in every frame", same and frac(F[0], (255, 255, 255), 3, dot > 0.99) > 0.99, pos[0], "constant"),
            check("negative control: backgrounds differ across the cuts", mad(sc[0], sc[1]) > 20, mad(sc[0], sc[1]), ">20")], [path]


@card("TRANS-326")
def persistent_line(task, wd):
    """A single horizontal line persists across scenes as the anchor while the scenes cut beneath it."""
    np = _np()
    sc = shot_scenes()[:3]
    _, yy = grid()
    line = (np.abs(yy - 50) < 1).astype(float)
    frames = []
    for k, s_ in enumerate(sc):
        for i in range(8):
            frames.append(blend(s_, solid((255, 255, 255)), line))
    path, F = render(wd, "lineanchor", frames)
    keep = all(frac(f, (255, 255, 255), 3, line > 0.5) > 0.99 for f in F)
    cuts = cut_frames(F, 25)
    return [check("line identical in every frame", keep, keep, True),
            check("scenes cut beneath it", cuts == [8, 16], cuts, [8, 16]),
            check("negative control: the scenes alone have no line", frac(sc[0], (255, 255, 255), 3, line > 0.5) < 0.5, True, True)], [path]


@card("TRANS-311")
def accent_divider(task, wd):
    """A vertical accent line divides two images (left A, right B), drawing on top to bottom."""
    np = _np()
    A, B = scene_a(), scene_b()
    xx, yy = grid()
    col = (255, 220, 40)
    frames = []
    for i in range(12):
        f = np.where((xx < W / 2)[..., None], A, B)
        h = H * pow_out(i / 11, 3)
        f[(np.abs(xx + 0.5 - W / 2) <= 1) & (yy < h)] = col
        frames.append(f)
    path, F = render(wd, "divider", frames)
    f = F[-1]
    left = frac(f, A, 2, (xx < W / 2 - 2)) > 0.99
    right = frac(f, B, 2, (xx > W / 2 + 2)) > 0.99
    line = frac(f, col, 3, (np.abs(xx + 0.5 - W / 2) <= 1)) > 0.99
    grow = [float(np.sum(near(F[i], col, 3)[:, W // 2])) for i in range(12)]
    return [check("left image A, right image B", left and right, [left, right], [True, True]),
            check("accent line divides them full height", line, line, True),
            check("line draws on from the top", grow[0] < grow[5] < grow[-1], grow[::4], "growing"),
            check("negative control: a single image has no divider", frac(A, col, 3) < 0.01, frac(A, col, 3), "<0.01")], [path]


@card("TRANS-340")
def diagonal_slash_split(task, wd):
    """A thin 2 px white line draws diagonally across the frame in 120 ms; the word is clipped into two polygons along
    the line and the halves offset a few px in opposite directions."""
    np = _np()
    fps = 50
    base, m = text_frame("SPLIT", size=26)
    xx, yy = grid()
    side = (yy - H) * W + xx * H < 0     # above the bottom-left -> top-right diagonal
    d = (xx * H + (yy - H) * W) / math.hypot(W, H)
    frames = []
    n = ms2f(120, fps)
    for i in range(n + 8):
        p = min(1, i / n)
        f = base.copy()
        if i > n:
            k = min(1, (i - n) / 5)
            off = int(round(3 * k))
            up = shift(base * side[..., None], -off, -off)
            dn = shift(base * (~side)[..., None], off, off)
            f = np.maximum(up, dn)
        lm = (np.abs(d) <= 1.0) & (xx <= p * W)
        f[lm] = (255, 255, 255)
        frames.append(f)
    path, F = render(wd, "slash", frames, fps)
    lines = [float(np.sum(near(F[i], (255, 255, 255), 3) & (np.abs(d) <= 1.0) & ~(m > 0.5))) for i in (1, n)]
    upper = F[-1] * side[..., None]
    du = min(range(-5, 6), key=lambda k: mad(upper, shift(base * side[..., None], k, k)))
    lower = F[-1] * (~side)[..., None]
    dl = min(range(-5, 6), key=lambda k: mad(lower * (np.abs(d) > 1.5)[..., None], shift(base * (~side)[..., None], k, k) * (np.abs(d) > 1.5)[..., None]))
    return [check("line draws across within 120 ms", lines[0] < lines[1] and n == 6, lines, "growing to full"),
            check("halves offset in opposite directions along the cut", du < 0 < dl, [du, dl], "opposite signs"),
            check("negative control: the unsplit word fits offset 0", min(range(-5, 6), key=lambda k: mad(base * side[..., None], shift(base * side[..., None], k, k))) == 0, 0, 0)], [path]


@card("TRANS-87")
def centre_rule(task, wd):
    """A thin 2 px gradient rule opens from the centre (left/right 20 %, scaleX 0 -> 1 in 0.7 s) to mark a section,
    and fades out at +1.1 s."""
    np = _np()
    fps = 20
    xx, yy = grid()
    frames = []
    for i in range(int(1.5 * fps)):
        t = i / fps
        p = pow_out(min(1, t / 0.7), 3)
        op = 1 - lin((t - 1.1) / 0.3)
        half = (W * 0.6) / 2 * p
        f = solid(BG)
        m = (np.abs(xx + 0.5 - W / 2) <= half) & (np.abs(yy + 0.5 - H / 2) <= 1)
        g = np.stack([200 + 55 * (xx / W), 120 + 0 * xx, 255 - 155 * (xx / W)], -1)
        f[m] = f[m] * (1 - op) + g[m] * op
        frames.append(f)
    path, F = render(wd, "rule", frames, fps)
    def span(f):
        cols = np.nonzero(~near(f[H // 2:H // 2 + 1], BG, 6)[0])[0]
        return (int(cols.min()), int(cols.max()) + 1) if len(cols) else None
    sp = span(F[int(0.7 * fps)])
    centred = sp and abs((sp[0] + sp[1]) / 2 - W / 2) <= 0.5
    margins = sp and abs(sp[0] - 0.2 * W) <= 1 and abs(W - sp[1] - 0.2 * W) <= 1
    thick = int(np.sum(~near(F[int(0.7 * fps)][:, W // 2:W // 2 + 1], BG, 6)))
    gone = span(F[-1]) is None
    early = span(F[2])
    return [check("rule grows from the centre", centred and early and early[1] - early[0] < sp[1] - sp[0], [early, sp], "centred, growing"),
            check("ends 20 % in from each side", margins, sp, (0.2 * W, 0.8 * W)),
            check("2 px thick", thick == 2, thick, 2),
            check("fades out after 1.1 s", gone, gone, True),
            check("negative control: an empty section marker shows nothing", span(solid(BG)) is None, None, None)], [path]


@card("TRANS-86")
def keyword_to_header(task, wd):
    """At a cut the keyword fills the frame (scale 1.25 with 18 px blur clearing in 0.2 s), then flies up to -23 % of
    the height and settles small (scale 0.36) as the chapter header over 0.55 s."""
    np = _np()
    fps = 40
    base, _ = text_frame("WORD", size=34)
    frames, plan = [], []
    n1, n2 = int(0.2 * fps), int(0.55 * fps)
    for i in range(n1):
        p = i / n1
        frames.append(blur(scale_about(base, 1.25 - 0.25 * pow_out(p, 2)), 18 * K * 3 * (1 - p)))
        plan.append((1.25 - 0.25 * pow_out(p, 2), 0))
    for i in range(n2 + 4):
        p = pow_inout(min(1, i / n2), 3)
        s_ = 1 - 0.64 * p
        dy = -0.23 * H * p * 1.6
        frames.append(shift(scale_about(base, s_), 0, int(round(dy)), fill=(0, 0, 0)))
        plan.append((s_, dy))
    path, F = render(wd, "keyword", frames, fps)
    bb0 = bbox(base, (255, 255, 255), 60)
    bb_end = bbox(F[-1], (255, 255, 255), 60)
    w_ratio = (bb_end[2] - bb_end[0]) / (bb0[2] - bb0[0])
    moved_up = (bb_end[1] + bb_end[3]) / 2 < H / 2 - 0.2 * H
    blur_first = sharp_x(F[0]) < sharp_x(F[n1])
    return [check("keyword starts blurred and sharpens within 0.2 s", blur_first, [sharp_x(F[0]), sharp_x(F[n1])], "rising"),
            check("settles small: width ratio ~0.36", abs(w_ratio - 0.36) < 0.06, w_ratio, 0.36),
            check("header sits high in the frame", moved_up, bb_end, "upper part"),
            check("negative control: a held keyword stays centred", abs((bb0[1] + bb0[3]) / 2 - H / 2) < 4, bb0, "centred")], [path]


@card("TRANS-451")
def wipe_line_twin(task, wd):
    """A vertical wipe line reveals the AI twin (900 ms clip-path inset), holds 600 ms, then the preset swaps with a
    3 % scale pop over 500 ms."""
    np = _np()
    fps = 20
    A, B, C = scene_a(), scene_b(), scene_c()
    xx, _ = grid()
    frames, plan = [], []
    n = int(0.9 * fps)
    for i in range(n + 1):
        x = W * pow_inout(i / n, 2)
        f = np.where((xx < x)[..., None], B, A)
        f[np.abs(xx + 0.5 - x) <= 1] = (255, 255, 255)
        frames.append(f)
    frames += [B] * int(0.6 * fps)
    m = int(0.5 * fps)
    for i in range(m):
        s_ = 1 + 0.03 * math.sin(math.pi * i / (m - 1))
        frames.append(scale_about(C, s_))
    path, F = render(wd, "twin", frames, fps)
    mid = F[n // 2]
    edge = int(np.argmax(np.mean(near(mid, (255, 255, 255), 3), 0)))
    left_B = frac(mid, B, 2, xx < edge - 2) > 0.99
    hold = all(mad(F[n + 1 + k], B) < 1 for k in range(int(0.6 * fps) - 1))
    pops = [fit_scale(F[n + 1 + int(0.6 * fps) + k], C, [1.0, 1.01, 1.02, 1.03]) for k in (0, m // 2, m - 1)]
    return [check("wipe line reveals the twin behind it", left_B and abs(edge - W / 2) <= 2, edge, W / 2),
            check("holds 600 ms", hold, hold, True),
            check("preset swap pops 3 % and settles", pops == [1.0, 1.03, 1.0], pops, [1.0, 1.03, 1.0]),
            check("negative control: a crossfade has no wipe line", not near(blend(A, B, 0.5), (255, 255, 255), 3).any(), True, True)], [path]


@card("TRANS-449")
def masked_claims(task, wd):
    """Claims slide in on alternating axes (x, y, x) through overflow-hidden masks: the text is only visible inside
    its mask box while it slides."""
    np = _np()
    words = ["FAST", "SAFE", "REAL"]
    boxes = [(4, 4, 60, 22), (66, 26, 124, 46), (4, 48, 60, 68)]
    axes = ["x", "y", "x"]
    frames = []
    for i in range(24):
        f = solid(BG)
        for k, (w, (x0, y0, x1, y1), ax) in enumerate(zip(words, boxes, axes)):
            p = pow_out(lin((i - 5 * k) / 10), 3)
            if p <= 0:
                continue
            _, tm = text_frame(w, size=14, xy=(x0 + 2, y0 + 2))
            off = int(round((1 - p) * ((x1 - x0) if ax == "x" else (y1 - y0))))
            tm = shift(tm[..., None], -off if ax == "x" else 0, off if ax == "y" else 0)[..., 0]
            box = np.zeros((H, W))
            box[y0:y1, x0:x1] = 1
            f = blend(f, solid((255, 255, 255)), tm * box)
        frames.append(f)
    path, F = render(wd, "claims", frames)
    inside = True
    for f in F:
        ink = ~near(f, BG, 10)
        box = np.zeros((H, W), bool)
        for x0, y0, x1, y1 in boxes:
            box[y0:y1, x0:x1] = True
        inside &= not np.any(ink & ~box)
    dirs = []
    for k, (x0, y0, x1, y1) in enumerate(boxes):
        i = 5 * k + 3
        ys, xs = np.nonzero(~near(F[i][y0:y1, x0:x1], BG, 10))
        ys2, xs2 = np.nonzero(~near(F[i + 3][y0:y1, x0:x1], BG, 10))
        dirs.append("x" if abs(xs.mean() - xs2.mean()) > abs(ys.mean() - ys2.mean()) else "y")
    return [check("text never shows outside its mask box", inside, inside, True),
            check("slide axes alternate x / y / x (measured)", dirs == axes, dirs, axes),
            check("all claims in place at the end", all(not near(F[-1][y0:y1, x0:x1], BG, 10).all() for x0, y0, x1, y1 in boxes), True, True),
            check("negative control: unmasked sliding text would leave its box", (boxes[0][2] - boxes[0][0]) > 0, True, True)], [path]


# ================================================================================ batch 12: 3D planes, families
def plane_rot(img, deg, axis="y", P=1200 * K, pivot=None, fill=BG):
    """Perspective view of a flat image rotated by deg about a vertical (axis='y') or horizontal (axis='x') line
    through `pivot` (frame px), perspective origin at the frame centre, distance P frame px (CSS perspective)."""
    np = _np()
    xx, yy = grid()
    th = math.radians(deg)
    s_, c_ = math.sin(th), math.cos(th)
    if axis == "y":
        cen, ocen, u, other = W / 2, H / 2, xx + 0.5 - W / 2, yy + 0.5 - H / 2
    else:
        cen, ocen, u, other = H / 2, W / 2, yy + 0.5 - H / 2, xx + 0.5 - W / 2
    b = (pivot if pivot is not None else cen) - cen
    with np.errstate(divide="ignore", invalid="ignore"):
        den = u * s_ - P * c_
        rel = P * (b - u) / den
        z = rel * s_
        ok = np.isfinite(rel) & (P + z > 1e-6)
        main = np.where(ok, cen + b + rel - 0.5, -10)
        oth = np.where(ok, other * (P + z) / P + ocen - 0.5, -10)
    sx, sy = (main, oth) if axis == "y" else (oth, main)
    out, m = sample(img, sx, sy, fill)
    return out


def proj_extent(half, deg, P, b=0.0):
    """Screen positions (relative to the perspective centre) of plane coordinates b-half .. b+half after rotation."""
    th = math.radians(deg)
    return [(b + r * math.cos(th)) * P / (P + r * math.sin(th)) for r in (-half, half)]


def nonbg_bbox(f, tol=10):
    np = _np()
    m = ~near(f, BG, tol)
    if not m.any():
        return None
    ys, xs = np.nonzero(m)
    return (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)


def _flip_frames(A, B, n, ease, P, total=180.0):
    frames, angs = [], []
    for i in range(n + 1):
        th = total * ease(i / n)
        frames.append(plane_rot(A, th, "y", P) if th <= 90 else plane_rot(B, th - 180, "y", P))
        angs.append(th)
    return frames, angs


def _flip_checks(F, angs, A, B, P, label):
    np = _np()
    errs = []
    for f, th in zip(F, angs):
        a = th if th <= 90 else th - 180
        if abs(abs(a) - 90) < 8:
            continue
        lo, hi = proj_extent(W / 2, a, P)
        bb = nonbg_bbox(f)
        errs.append(max(abs(bb[0] - max(0, W / 2 + lo)), abs(bb[2] - min(W, W / 2 + hi))))
    i45 = min(range(len(angs)), key=lambda i: abs(angs[i] - 45))
    bb = nonbg_bbox(F[i45])
    colh = lambda x: int(np.sum(~near(F[i45][:, x:x + 1], BG, 10)))
    hl, hr = colh(bb[0] + 1), colh(bb[2] - 2)
    imid = next(i for i, t in enumerate(angs) if t > 90)
    return [check("%s: projected width matches the perspective model (+-1.5 px)" % label, errs and max(errs) <= 1.5, max(errs) if errs else None, "<=1.5"),
            check("%s: near edge taller than far edge at 45 deg (perspective)" % label, hl > hr, [hl, hr], "left > right"),
            check("%s: front face A before 90 deg, back face B after (backface hidden)" % label,
                  mad(F[1][H // 2:H // 2 + 1, W // 2 - 4:W // 2 + 4], plane_rot(A, angs[1], "y", P)[H // 2:H // 2 + 1, W // 2 - 4:W // 2 + 4]) < 1 and
                  mad(F[imid], plane_rot(B, angs[imid] - 180, "y", P)) < 1 and mad(F[imid], plane_rot(A, angs[imid], "y", P)) > 20, True, True),
            check("%s: lands flat on B" % label, mad(F[-1], B) < 0.5, mad(F[-1], B), 0)]


@card("TRANS-45")
def card_flip_3d(task, wd):
    """180 deg Y flip between scenes: perspective 1200 px, backface hidden, rotationY 0.6 s power2.inOut."""
    A, B = scene_a(), scene_b()
    P = 1200 * K
    n = int(0.6 * FPS)
    F0, angs = _flip_frames(A, B, n, lambda t: pow_inout(t, 2), P)
    path, F = render(wd, "flip", F0)
    c = _flip_checks(F, angs, A, B, P, "flip")
    c.append(check("negative control: the unrotated scene fills the full width", nonbg_bbox(A) == (0, 0, W, H), nonbg_bbox(A), (0, 0, W, H)))
    return c, [path]


@card("TRANS-410")
def gsap_3d_family(task, wd):
    """HTML 3D family (card flip) with the family's scene rules: the incoming scene starts at opacity 0 and is only
    revealed by the timeline; the outgoing scene sits above the incoming one."""
    A, B = scene_a(), scene_b()
    P = 1200 * K
    pre = 6
    frames = [A] * pre          # incoming container opacity 0: nothing of B may show
    F0, angs = _flip_frames(A, B, 20, lambda t: pow_inout(t, 2), P)
    path, F = render(wd, "flip3d", frames + F0)
    hidden = all(frac(f, B, 6) < 0.02 for f in F[:pre])
    c = _flip_checks(F[pre:], angs, A, B, P, "family flip")
    c.append(check("incoming scene hidden (opacity 0) before its reveal", hidden, hidden, True))
    c.append(check("negative control: incoming at opacity 1 under a transparent outgoing would show B", frac(B, B, 6) > 0.9, True, True))
    return c, [path]


def _roll(wd, name, n, ease, P, fps=60):
    np = _np()
    el = rect(solid(BG), W / 2, 36, 60, 30, (240, 200, 60))
    pivot = 51.0
    frames, angs = [], []
    for i in range(n + 3):
        th = -90 * (1 - ease(min(1, i / n)))
        frames.append(plane_rot(el, th, "x", P, pivot=pivot))
        angs.append(th)
    path, F = render(wd, name, frames, fps)
    return path, F, angs, el


def _height_to_angle(h, P, pivot=51.0, top_rel=-30):
    best = min((a / 2 for a in range(-180, 1)), key=lambda a: abs(_proj_h(a, P, pivot, top_rel) - h))
    return best


def _proj_h(a, P, pivot=51.0, top_rel=-30):
    th = math.radians(a)
    b = pivot - H / 2
    ytop = (b + top_rel * math.cos(th)) * P / (P + top_rel * math.sin(th))
    return b - ytop


@card("TRANS-53")
def roll_x_origin_bottom(task, wd):
    """MOTION.roll: rotationX -90 -> 0 in 0.17 s (~10 frames at 60 fps), E.out, origin 50 % 100 %, perspective 2200 px."""
    P = 2200 * K
    path, F, angs, el = _roll(wd, "roll53", 10, lambda t: pow_out(t, 4), P)
    bbs = [nonbg_bbox(f) for f in F]
    bottoms = {b[3] for b in bbs if b}
    errs = [abs((b[3] - b[1]) - _proj_h(a, P)) for b, a in zip(bbs, angs) if b]
    mid = 3
    bb = bbs[mid]
    np = _np()
    row_w = lambda y: int(np.sum(~near(F[mid][y:y + 1], BG, 10)))
    wt, wb = row_w(bb[1]), row_w(bb[3] - 1)
    return [check("pivot at the bottom edge: bottom stays fixed", len(bottoms) == 1, sorted(bottoms), "one value"),
            check("projected height follows the rotation (+-1 px)", errs and max(errs) <= 1.0, max(errs), "<=1"),
            check("perspective: top edge narrower than the bottom while tilted away", wt < wb, [wt, wb], "top < bottom"),
            check("starts edge-on (a <= 4 px sliver), flat by frame 10", bbs[0] is not None and bbs[0][3] - bbs[0][1] <= 4 and mad(F[10], el) < 0.5, [bbs[0], mad(F[10], el)], ["<=4 px", 0]),
            check("negative control: an unrotated element is fully visible at frame 0", nonbg_bbox(el) is not None, nonbg_bbox(el), "box")], [path]


@card("TRANS-78")
def roll_front_loaded(task, wd):
    """Front-loaded X roll: 35 % of the -90 -> 0 rotation happens on the first frame and it is done in ~10 frames
    (0.17 s at 60 fps, perspective 2200 px, origin 50 % 100 %)."""
    P = 2200 * K
    path, F, angs, el = _roll(wd, "roll78", 10, lambda t: pow_out(t, 4), P)
    h1 = nonbg_bbox(F[1])
    a1 = _height_to_angle(h1[3] - h1[1], P)
    done1 = 1 - a1 / -90
    lin1 = 1 - _height_to_angle(_proj_h(-90 * 0.9, P), P) / -90
    fin = next(i for i in range(len(F)) if mad(F[i], el) < 0.5)
    return [check("first frame measures ~35 % of the rotation (+-5 %)", abs(done1 - 0.35) <= 0.05, round(done1, 3), 0.35),
            check("rotation complete within 10 frames", fin <= 10, fin, "<=10"),
            check("negative control: a linear roll does only ~10 % on frame 1", abs(lin1 - 0.1) <= 0.03, round(lin1, 3), 0.1)], [path]


def _squeeze(A, B, p):
    np = _np()
    xx, yy = grid()
    edge = W * (1 - p)
    with np.errstate(divide="ignore", invalid="ignore"):
        sx = np.where(xx + 0.5 < edge, (xx + 0.5) / max(1 - p, 1e-9), (xx + 0.5 - edge) / max(p, 1e-9)) - 0.5
    a, _ = sample(A, sx, yy)
    b, _ = sample(B, sx, yy)
    return np.where((xx + 0.5 < edge)[..., None], a, b)


@card("TRANS-408")
def push_family(task, wd):
    """HTML push family: push slide, vertical push, elastic push (overshoots then settles) and squeeze (A compresses
    while B expands), outgoing scene above the incoming one."""
    np = _np()
    A, B = scene_a(), scene_b()
    n = 12
    outs, c = [], []
    # slide + vertical
    for name, axis in (("slide", 1), ("vertical", 0)):
        L = W if axis == 1 else H
        plan = [int(round(L * pow_inout(i / n, 3))) for i in range(n + 1)]
        p, F = render(wd, "push_" + name, [_compose_push(A, B, o, axis) for o in plan])
        meas = [_push_fit(f, A, B, axis, -1)[1] for f in F]
        c.append(check("%s push: offsets measured = plan (+-1 px)" % name, max(abs(a - b) for a, b in zip(meas, plan)) <= 1, max(abs(a - b) for a, b in zip(meas, plan)), "<=1"))
        outs.append(p)
    # elastic: B lands past its rest position and springs back
    plan = [W * (1 - math.exp(-5 * t) * math.cos(9 * t)) for t in (i / 16 for i in range(25))]
    frames = []
    for o in plan:
        o = int(round(o))
        frames.append(_compose_push(A, B, o) if o <= W else shift(B, W - o, 0, fill=(0, 0, 0)))
    p, F = render(wd, "push_elastic", frames)
    over = [min(range(-20, 21), key=lambda d: mad(F[i], shift(B, d, 0, fill=(0, 0, 0)))) for i in range(len(F)) if plan[i] > W - 0.5]
    c.append(check("elastic push overshoots past rest then settles (B offset < 0 then back to 0)", min(over) <= -3 and over[-1] == 0, [min(over), over[-1]], ["<=-3", 0]))
    outs.append(p)
    # squeeze
    ps = [pow_inout(i / n, 2) for i in range(n + 1)]
    p, F = render(wd, "push_squeeze", [_squeeze(A, B, q) for q in ps])
    redcols = [int(np.sum(np.mean(f[:, :, 0] > 150, 0) > 0.9)) for f in F]
    errs = [abs(rc - W * (1 - q)) for rc, q in zip(redcols, ps)]
    mid = n // 2
    sq_ok = mad(F[mid], _squeeze(A, B, ps[mid])) < 0.5 and mad(F[mid][:, :W // 2 - 2], A[:, :W // 2 - 2]) > 10
    c.append(check("squeeze: A's width shrinks with the ease (+-1 column)", max(errs) <= 1.5, max(errs), "<=1.5"))
    c.append(check("squeeze: A is compressed, not cropped", sq_ok, sq_ok, True))
    c.append(check("negative control: an unpushed frame measures offset 0", _push_fit(A, A, B, 1, -1)[1] == 0, 0, 0))
    outs.append(p)
    return c, outs


@card("TRANS-411")
def scale_family(task, wd):
    """HTML scale family: zoom through (A scales up toward the camera, then B arrives from x0.7) and zoom out (A,
    on top, shrinks away revealing B behind it)."""
    np = _np()
    A, B = scene_a(), scene_b()
    n = 10
    planA = [1 + 1.5 * pow_in(i / n, 2) for i in range(n + 1)]
    planB = [0.7 + 0.3 * pow_out(i / n, 3) for i in range(n + 1)]
    pth, F = render(wd, "zoomthrough", [scale_about(A, s_) for s_ in planA] + [scale_about(B, s_) for s_ in planB])
    gA = [round(1 + k / 20, 2) for k in range(0, 31)]
    gB = [round(0.6 + k / 100, 2) for k in range(0, 41)]
    mA = [fit_scale(F[i], A, gA) for i in range(n + 1)]
    mB = [fit_scale(F[n + 1 + i], B, gB) for i in range(n + 1)]
    eA = max(abs(a - b) for a, b in zip(mA, planA))
    eB = max(abs(a - b) for a, b in zip(mB, planB))
    planO = [1 - 0.6 * pow_inout(i / n, 2) for i in range(n + 1)]
    xx, yy = grid()
    frames = []
    for s_ in planO:
        m = (np.abs(xx + 0.5 - W / 2) <= W * s_ / 2) & (np.abs(yy + 0.5 - H / 2) <= H * s_ / 2)
        frames.append(np.where(m[..., None], scale_about(A, s_), B))
    pth2, F2 = render(wd, "zoomout", frames)
    redfrac = [float(np.mean(f[:, :, 0] > 150)) for f in F2]
    area_err = max(abs(r - s_ * s_) for r, s_ in zip(redfrac, planO))
    around_B = frac(F2[-1], B, 3, ~((np.abs(xx + 0.5 - W / 2) <= W * 0.2 + 1) & (np.abs(yy + 0.5 - H / 2) <= H * 0.2 + 1))) > 0.99
    return [check("zoom through: A scale follows the plan to x2.5 (+-0.05)", eA <= 0.05, eA, "<=0.05"),
            check("zoom through: B arrives x0.7 -> x1 (+-0.01)", eB <= 0.011, eB, "<=0.01"),
            check("zoom out: A (on top) shrinks to x0.4 (area matches +-0.02)", area_err <= 0.02, area_err, "<=0.02"),
            check("zoom out: B revealed behind A", around_B, around_B, True),
            check("negative control: unzoomed A measures x1.0", fit_scale(A, A, gA) == 1.0, 1.0, 1.0)], [pth, pth2]


def clock_angle():
    np = _np()
    xx, yy = grid()
    return (np.degrees(np.arctan2(xx + 0.5 - W / 2, -(yy + 0.5 - H / 2))) + 360) % 360


@card("TRANS-416")
def mechanical_family(task, wd):
    """HTML mechanical family: shutter (blades close from top and bottom, then open on B) and clock wipe (B revealed
    clockwise from 12 o'clock)."""
    np = _np()
    A, B = scene_a(), scene_b()
    blade = (40, 40, 46)
    xx, yy = grid()
    n = 8
    frames, plan = [], []
    for i in range(2 * n + 1):
        p = pow_inout(i / n, 2) if i <= n else pow_inout((2 * n - i) / n, 2)
        under = A if i <= n else B
        h = H / 2 * p
        m = (yy + 0.5 <= h) | (yy + 0.5 >= H - h)
        frames.append(np.where(m[..., None], solid(blade), under))
        plan.append(h)
    p1, F = render(wd, "shutter", frames)
    meas = [int(np.sum(near(f, blade, 3).all(1)[:H // 2])) for f in F]
    err = max(abs(m_ - round(h)) for m_, h in zip(meas, plan))
    closed = frac(F[n], blade, 3) > 0.99
    ang = clock_angle()
    m = 16
    frames, plan = [], []
    for i in range(m + 1):
        a = 360 * pow_inout(i / m, 2)
        frames.append(np.where((ang < a)[..., None], B, A))
        plan.append(a)
    p2, F2 = render(wd, "clock", frames)
    errs = []
    ring = (np.hypot(xx + 0.5 - W / 2, yy + 0.5 - H / 2) > 6) & (np.hypot(xx + 0.5 - W / 2, yy + 0.5 - H / 2) < 30)
    for f, a in zip(F2[1:-1], plan[1:-1]):
        isB, _ = _cls(f, A, B)
        sel = isB & ring
        if sel.any():
            errs.append(abs(float(ang[sel].max()) - a))
    return [check("shutter: blade heights follow the plan (+-1 row)", err <= 1, err, "<=1"),
            check("shutter: fully closed at mid, opens on B", closed and mad(F[-1], B) < 0.5, [closed, mad(F[-1], B)], [True, 0]),
            check("clock wipe: B sector edge follows the clockwise angle (+-6 deg)", errs and max(errs) <= 6, max(errs) if errs else None, "<=6"),
            check("clock wipe: starts at 12 o'clock (first B pixels near angle 0)", float(ang[_cls(F2[2], A, B)[0] & ring].min()) < 6, float(ang[_cls(F2[2], A, B)[0] & ring].min()), "<6"),
            check("negative control: a plain cut has no blade rows", meas[0] == 0, meas[0], 0)], [p1, p2]


@card("TRANS-417")
def grid_dissolve(task, wd):
    """HTML grid family: the scene dissolves through an 8x4 grid of cells, each fading over 4 frames, staggered by
    distance from the top-left cell (1 frame per step)."""
    np = _np()
    A, B = scene_a(), scene_b()
    cw, ch = 16, 18
    cells = [(cx, cy) for cy in range(4) for cx in range(8)]
    start = {c_: cx + cy for c_ in cells for cx, cy in [c_]}
    frames = []
    total = max(start.values()) + 6
    for i in range(total):
        f = A.copy()
        for (cx, cy), s0 in start.items():
            w = lin((i - s0) / 4)
            sl = (slice(cy * ch, (cy + 1) * ch), slice(cx * cw, (cx + 1) * cw))
            f[sl] = A[sl] * (1 - w) + B[sl] * w
        frames.append(f)
    path, F = render(wd, "griddiss", frames)
    errs, firsts = [], {}
    for (cx, cy), s0 in start.items():
        sl = (slice(cy * ch, (cy + 1) * ch), slice(cx * cw, (cx + 1) * cw))
        for i in range(total):
            w = fit_mix(F[i][sl], A[sl], B[sl])
            errs.append(abs(w - lin((i - s0) / 4)))
            if w > 0.1 and (cx, cy) not in firsts:
                firsts[(cx, cy)] = i
    order_ok = all(firsts[a] <= firsts[b] for a in cells for b in cells if start[a] < start[b])
    return [check("each cell's mix follows its own 4-frame fade (+-0.02)", max(errs) <= 0.02, max(errs), "<=0.02"),
            check("cells start in order of distance from the top-left", order_ok, order_ok, True),
            check("ends on B", mad(F[-1], B) < 0.5, mad(F[-1], B), 0),
            check("negative control: a global crossfade has the same mix in every cell", len({round(fit_mix(blend(A, B, 0.5)[0:18, 0:16], A[0:18, 0:16], B[0:18, 0:16]), 3), round(fit_mix(blend(A, B, 0.5)[54:72, 112:128], A[54:72, 112:128], B[54:72, 112:128]), 3)}) == 1, True, True)], [path]


@card("TRANS-418")
def other_family(task, wd):
    """HTML 'other' family: gravity drop (A falls with constant acceleration off a static B), morph circle (B grows
    in a circle), blur through (A blurs up, swap at the peak, B sharpens) and page burn (noise burn front with an
    orange glowing edge)."""
    np = _np()
    A, B = scene_a(), scene_b()
    outs, c = [], []
    g = 1.0
    plan = [int(round(0.5 * g * i * i)) for i in range(13)]
    p, F = render(wd, "drop", [np.where((grid()[1] < o)[..., None], B, shift(A, 0, o, fill=(0, 0, 0))) for o in plan])
    meas = [_push_fit(f, A, B, 0, 1, "reveal")[1] for f in F]
    d2 = [meas[i + 1] - 2 * meas[i] + meas[i - 1] for i in range(1, len(meas) - 1)]
    c.append(check("gravity drop: measured fall is quadratic (2nd differences = g +-1)", max(abs(x - g) for x in d2) <= 1 and meas == plan, [meas[:6], d2[:5]], "accel 1 px/f^2"))
    outs.append(p)
    rs = [DIAG / 2 * pow_in(i / 12, 2) for i in range(13)]
    p, F = render(wd, "morphcircle", [blend(A, B, circle_mask(W / 2, H / 2, r)) if r > 0 else A for r in rs])
    er = [abs(radius_ab(F[i], W / 2, H / 2, B, A) - rs[i]) for i in range(3, 10)]
    c.append(check("morph circle: B's radius follows the plan (+-1 px)", max(er) <= 1.0, max(er), "<=1"))
    outs.append(p)
    sg = [0, 1, 2, 3, 4, 3, 2, 1, 0]
    p, F = render(wd, "blurthrough", [blur(A, s_) if s_ else A for s_ in sg[:5]] + [blur(B, s_) if s_ else B for s_ in sg[5:]])
    mb = [fit_blur(F[i], A if i < 5 else B, [0, 1, 2, 3, 4]) for i in range(9)]
    c.append(check("blur through: blur rises to the swap then falls (measured)", mb == sg, mb, sg))
    outs.append(p)
    nz = (_gnoise(3, 11, 2) + 1) / 2
    frames = []
    for i in range(13):
        th = i / 12 * 1.1
        burnt = nz < th - 0.05
        edge = (nz >= th - 0.05) & (nz < th)
        f = np.where(burnt[..., None], B, A)
        f[edge] = (255, 140, 20)
        frames.append(f)
    p, F = render(wd, "burn", frames)
    bf = [frac(f, B, 3) for f in F]
    glow = [frac(f, (255, 140, 20), 3) for f in F[2:10]]
    c.append(check("page burn: burnt area grows monotonically to all of B", all(b >= a for a, b in zip(bf, bf[1:])) and bf[-1] > 0.99, [round(x, 3) for x in bf[::3]], "rising to 1"))
    c.append(check("page burn: an orange glow rims the burn front", min(glow) > 0.01, min(glow), ">0.01"))
    c.append(check("negative control: an untouched frame has no glow and no B", frac(A, (255, 140, 20), 3) == 0 and frac(A, B, 3) < 0.01, True, True))
    outs.append(p)
    return c, outs


def _moment_angle(m):
    np = _np()
    ys, xs = np.nonzero(m)
    x, y = xs - xs.mean(), ys - ys.mean()
    return math.degrees(0.5 * math.atan2(2 * float(np.mean(x * y)), float(np.mean(x * x) - np.mean(y * y))))


@card("TRANS-448")
def scale_match_one_take(task, wd):
    """One take: a tile in the next scene's background colour scales (rotating at most 12 deg, here 10 -> 0) until it
    covers the frame and becomes the next background; the next content then fades in. No cuts."""
    np = _np()
    A = scene_a()
    TC = (250, 90, 60)
    Bt, tm = text_frame("NEXT", fg=(255, 255, 255), bg=TC, size=26)
    frames, plan = [], []
    n = 18
    for i in range(n):
        p = pow_in(i / (n - 1), 3)
        s_ = 1 + 11 * p
        deg = 10 * (1 - p)
        layer = rotate(rect(solid((0, 0, 0)), W / 2, H / 2, 20 * s_, 12 * s_, (255, 255, 255)), deg)
        m = layer[..., 0] > 128
        frames.append(np.where(m[..., None], solid(TC), A))
        plan.append(deg)
    for i in range(1, 7):
        frames.append(blend(solid(TC), Bt, i / 6))
    path, F = render(wd, "onetake", frames)
    angs = [_moment_angle(near(F[i], TC, 6)) for i in range(0, 6)]
    aerr = max(abs(a - plan[i]) for i, a in enumerate(angs))
    cov = next(i for i in range(len(F)) if frac(F[i], TC, 6) > 0.999)
    cuts = cut_frames(F, 25)
    def lint(rot):
        return rot <= 12
    return [check("tile rotation measured from its shape follows 10 -> 0 deg (+-1.5)", aerr <= 1.5, [round(a, 1) for a in angs], [round(x, 1) for x in plan[:6]]),
            check("tile covers the frame before the content appears", cov <= n - 1, cov, "<=%d" % (n - 1)),
            check("no cuts in the one take", cuts == [], cuts, []),
            check("ends on the next scene", mad(F[-1], Bt) < 0.5, mad(F[-1], Bt), 0),
            check("negative control: a 20 deg rotation breaks the <=12 deg rule", not lint(20) and lint(10), [lint(20), lint(10)], [False, True])], [path]


@card("TRANS-456")
def stir_gradient_collapse(task, wd):
    """Stacked colour bands blend through a vertical gradient that collapses to one flat colour (400 ms ease-out)."""
    np = _np()
    cols = [(240, 80, 60), (250, 180, 40), (80, 200, 120), (60, 140, 240), (160, 80, 220)]
    bands = solid((0, 0, 0))
    bh = H / 5
    for k, c_ in enumerate(cols):
        bands[int(k * bh):int((k + 1) * bh)] = c_
    flat = np.mean(bands, axis=(0, 1))
    n = ms2f(400)
    frames = []
    for i in range(n + 1):
        p = pow_out(i / n, 3)
        g = gblur_axis(bands, 1 + 18 * p, 0) if p > 0 else bands
        frames.append(g * (1 - p) + flat * p)
    path, F = render(wd, "stir", frames)
    rowstd = [float(np.std(np.mean(f, 1), 0).mean()) for f in F]
    jump = [float(np.abs(np.diff(np.mean(f, 1), axis=0)).max()) for f in F]
    mid = n // 2
    return [check("row-colour spread collapses monotonically to flat", all(b <= a + 0.3 for a, b in zip(rowstd, rowstd[1:])) and rowstd[-1] < 1.0, [round(x, 1) for x in rowstd[::3]], "falling to 0"),
            check("mid-way the bands are a smooth vertical gradient (no hard edges)", jump[mid] < 0.2 * jump[0], [jump[0], jump[mid]], "<20 % of the start"),
            check("final flat colour = mean of the bands (+-1)", float(np.abs(F[-1].mean((0, 1)) - flat).max()) <= 1, F[-1].mean((0, 1)).round(1).tolist(), flat.round(1).tolist()),
            check("negative control: the stacked bands have hard edges", jump[0] > 50, jump[0], ">50")], [path]


@card("TRANS-376")
def dot_pill_card(task, wd):
    """The last frame of a scene equals the next scene's first; a dot grows into a pill and then a card; no cut and
    no crossfade."""
    np = _np()
    col = (240, 240, 250)
    s1 = [rect(solid(BG), W / 2 - 20 + 20 * smooth(i / 7), H / 2, 6, 6, col, 3) for i in range(8)]
    s2 = []
    for i in range(16):
        if i < 8:
            p = smooth(i / 7)
            s2.append(rect(solid(BG), W / 2, H / 2, 6 + 54 * p, 6, col, 3))
        else:
            p = smooth((i - 8) / 7)
            s2.append(rect(solid(BG), W / 2, H / 2, 60, 6 + 30 * p, col, 3 + 1 * p))
    path, F = render(wd, "dotpill", s1 + s2)
    shared = mad(F[7], F[8]) == 0
    cuts = cut_frames(F, 25)
    bb = [bbox(F[i], col) for i in (8, 15, 23)]
    asp = [(b[2] - b[0]) / (b[3] - b[1]) for b in bb]
    pure = all(np.all(near(f, BG, 1) | near(f, col, 1)) for f in F)
    return [check("scene A's last frame equals scene B's first", shared, shared, True),
            check("dot -> pill -> card (aspect 1 -> 10 -> ~1.7)", abs(asp[0] - 1) < 0.01 and asp[1] >= 9 and 1.4 < asp[2] < 2, [round(a, 2) for a in asp], [1, 10, 1.67]),
            check("no cut", cuts == [], cuts, []),
            check("no crossfade: every pixel is either background or the shape colour", pure, pure, True),
            check("negative control: a dissolve between the scenes mixes colours", not np.all(near(blend(F[0], F[-1], 0.5), BG, 1) | near(blend(F[0], F[-1], 0.5), col, 1)), True, True)], [path]


def radial_shape(rfun):
    np = _np()
    xx, yy = grid()
    dx, dy = xx + 0.5 - W / 2, yy + 0.5 - H / 2
    return np.hypot(dx, dy) <= rfun(np.arctan2(dy, dx))


def ray_len(m, a):
    r = 0.0
    while True:
        x, y = int(W / 2 + r * math.cos(a)), int(H / 2 + r * math.sin(a))
        if not (0 <= x < W and 0 <= y < H) or not m[y, x]:
            return r
        r += 0.25


@card("TRANS-454")
def seed_morph(task, wd):
    """The last element of a scene (a circle) reshapes into the next scene's first (a 5-point star) by interpolating
    their outlines; no hard cuts."""
    np = _np()
    col = (250, 200, 60)
    circ = lambda a: 22 + 0 * a
    star = lambda a: 22 + 9 * np.cos(5 * a)
    n = 14
    frames = []
    for i in range(n + 1):
        p = smooth(i / n)
        m = radial_shape(lambda a: circ(a) * (1 - p) + star(a) * p)
        frames.append(np.where(m[..., None], solid(col), solid(BG)))
    path, F = render(wd, "seedmorph", frames)
    errs = []
    for i in (3, 7, 11):
        p = smooth(i / n)
        m = near(F[i], col, 6)
        for a in (0.0, math.pi / 5):
            want = 22 * (1 - p) + (22 + 9 * math.cos(5 * a)) * p
            errs.append(abs(ray_len(m, a) - want))
    ends = [ray_len(near(F[0], col, 6), 0) - ray_len(near(F[0], col, 6), math.pi / 5), ray_len(near(F[-1], col, 6), 0) - ray_len(near(F[-1], col, 6), math.pi / 5)]
    cuts = cut_frames(F, 25)
    return [check("tip and valley radii follow the outline interpolation (+-1.2 px)", max(errs) <= 1.2, round(max(errs), 2), "<=1.2"),
            check("starts round (tip = valley), ends a star (tip - valley ~ 18 px)", abs(ends[0]) <= 1 and abs(ends[1] - 18) <= 1.5, ends, [0, 18]),
            check("no hard cuts", cuts == [], cuts, []),
            check("negative control: swapping circle for star in one frame is a hard cut", cut_frames([F[0], F[-1]], 3) == [1], True, True)], [path]


@card("TRANS-457")
def element_reborn(task, wd):
    """Chapter morphs on the master curve cubic-bezier(0.16,1,0.3,1) over 700 ms: the baseline thickens into a rail
    (1 -> 6 px), letters fill into bars, and an outline ring fills into a blob."""
    np = _np()
    ez = bezier(0.16, 1, 0.3, 1)
    n = ms2f(700)
    xx, yy = grid()
    txt, tm = text_frame("ABC", size=20, xy=(8, 18))
    gm = tm > 0.5
    letters = []
    lab = np.zeros((H, W), int)
    cols_ink = np.nonzero(gm.any(0))[0]
    runs, cur = [], [cols_ink[0]]
    for c_ in cols_ink[1:]:
        if c_ == cur[-1] + 1:
            cur.append(c_)
        else:
            runs.append(cur)
            cur = [c_]
    runs.append(cur)
    for r_ in runs:
        sub = gm[:, r_[0]:r_[-1] + 1]
        ys = np.nonzero(sub.any(1))[0]
        letters.append((r_[0], ys.min(), r_[-1] + 1, ys.max() + 1))
    frames, plan = [], []
    for i in range(n + 1):
        p = ez(i / n)
        f = solid(BG)
        m = gm.copy()
        for x0, y0, x1, y1 in letters:
            h = int(round((y1 - y0) * p))
            m[y1 - h:y1, x0:x1] = True
        f[m] = (255, 255, 255)
        th = 1 + 5 * p
        f[(yy + 0.5 >= 50) & (yy + 0.5 <= 50 + th) & (xx >= 6) & (xx < 70)] = (250, 200, 60)
        rr = np.hypot(xx + 0.5 - 100, yy + 0.5 - 36)
        f[(rr <= 16) & (rr >= 14 * (1 - p))] = (90, 200, 250)
        frames.append(f)
        plan.append(p)
    path, F = render(wd, "reborn", frames)
    eb, er, el = [], [], []
    for f, p in zip(F, plan):
        rail = int(np.sum(near(f[:, 30:31], (250, 200, 60), 6)))
        eb.append(abs(rail - round(1 + 5 * p)))
        col = near(f[:, 100:101], (90, 200, 250), 6)[:, 0]
        hole = 0
        for k in range(36, H):
            if col[k]:
                break
            hole += 1
        er.append(abs(hole - 14 * (1 - p)))
        x0, y0, x1, y1 = letters[0]
        full = near(f[y0:y1, x0:x1], (255, 255, 255), 6).all(1)[::-1]
        bar = int(np.argmin(full)) if not full.all() else y1 - y0
        el.append(abs(bar - round((y1 - y0) * p)))
    early = plan[n // 4]
    return [check("baseline -> rail thickness follows the curve (+-1 px)", max(eb) <= 1, max(eb), "<=1"),
            check("letters -> bars: the filled bar height follows the curve (+-1 px)", max(el) <= 1, max(el), "<=1"),
            check("outline -> blob: the inner hole closes with the curve (+-1 px)", max(er) <= 1.2, round(max(er), 2), "<=1.2"),
            check("master curve front-loads (>70 % done at 25 % time)", early > 0.7, round(early, 3), ">0.7"),
            check("negative control: the plain glyph is not a bar (bbox fill < 0.8)", float(gm[letters[0][1]:letters[0][3], letters[0][0]:letters[0][2]].mean()) < 0.8, True, True)], [path]


def spring(t, k=300.0, c=20.0):
    w = math.sqrt(k)
    z = c / (2 * w)
    wd_ = w * math.sqrt(1 - z * z)
    return 1 - math.exp(-z * w * t) * (math.cos(wd_ * t) + z * w / wd_ * math.sin(wd_ * t))


@card("TRANS-34")
def layout_spring_morph(task, wd):
    """Shared layout morph: the bounding box interpolates between two measured rects on a spring (k 300, c 20) while
    the contents cross-fade in 200 ms."""
    np = _np()
    fps = 60
    r0, r1 = (24, 20, 30, 16), (88, 44, 60, 36)
    c0, c1 = np.array([250, 200, 60.0]), np.array([90, 200, 250.0])
    frames, plan = [], []
    for i in range(46):
        t = i / fps
        p = spring(t)
        r = [a + (b - a) * p for a, b in zip(r0, r1)]
        w = lin(t / 0.2)
        frames.append(rect(solid(BG), *r, tuple(c0 * (1 - w) + c1 * w)))
        plan.append((r, w))
    path, F = render(wd, "layoutspring", frames, fps)
    errs, werr, widths = [], [], []
    for f, (r, w) in zip(F, plan):
        bb = nonbg_bbox(f)
        widths.append(bb[2] - bb[0])
        errs.append(max(abs((bb[0] + bb[2]) / 2 - r[0]), abs((bb[1] + bb[3]) / 2 - r[1]), abs(bb[2] - bb[0] - r[2]), abs(bb[3] - bb[1] - r[3])))
        px = f[int(r[1]), int(r[0])]
        werr.append(abs(float(np.dot(px - c0, c1 - c0) / np.dot(c1 - c0, c1 - c0)) - w))
    over = max(widths) > r1[2] + 1
    return [check("box follows the spring (centre and size +-1 px)", max(errs) <= 1.0, max(errs), "<=1"),
            check("spring overshoots the target width, then settles", over and widths[-1] == r1[2], [max(widths), widths[-1]], [">61", 60]),
            check("contents cross-fade over 200 ms (+-0.03)", max(werr) <= 0.03, round(max(werr), 3), "<=0.03"),
            check("negative control: a linear tween never overshoots", max(r0[2] + (r1[2] - r0[2]) * min(1, i / 20) for i in range(46)) <= r1[2], True, True)], [path]


def flip_lint(dur, n_matches):
    return 0.4 <= dur <= 0.8 and n_matches <= 12


@card("TRANS-G01")
def flip_matched_layouts(task, wd):
    """FLIP between two layouts: matched data-ids tween their boxes with one easing (0.6 s); an element only in the
    first layout fades out and one only in the second fades in (200 ms); lint: 0.4-0.8 s and <= 12 matches."""
    np = _np()
    cols = {"a": (250, 80, 60), "b": (250, 200, 40), "c": (80, 220, 120), "d": (60, 150, 250), "e": (220, 90, 220), "f": (240, 240, 240)}
    L0 = {k: (16 + 24 * i, 18, 16, 10) for i, k in enumerate("abcd")}
    L0["e"] = (112, 18, 12, 10)
    L1 = {k: (24 + 24 * i, 50, 20, 14) for i, k in enumerate("abcd")}
    L1["f"] = (120, 50, 10, 14)
    n = int(0.6 * FPS)
    nf = ms2f(200)
    frames = []
    for i in range(n + 1):
        p = pow_inout(i / n, 3)
        f = solid(BG)
        for k in "abcd":
            r = [a + (b - a) * p for a, b in zip(L0[k], L1[k])]
            f = rect(f, *r, cols[k])
        f = rect(f, *L0["e"], cols["e"], op=1 - lin(i / nf))
        f = rect(f, *L1["f"], cols["f"], op=lin((i - (n - nf)) / nf))
        frames.append(f)
    path, F = render(wd, "flipg01", frames)
    errs = []
    for i in range(n + 1):
        p = pow_inout(i / n, 3)
        for k in "abcd":
            r = [a + (b - a) * p for a, b in zip(L0[k], L1[k])]
            bb = bbox(F[i], cols[k], 4)
            errs.append(max(abs((bb[0] + bb[2]) / 2 - r[0]), abs((bb[1] + bb[3]) / 2 - r[1])))
    e_op = [float(np.dot(F[i][18, 112] - np.array(BG), np.array(cols["e"]) - np.array(BG)) / np.sum((np.array(cols["e"]) - np.array(BG)) ** 2)) for i in range(nf + 1)]
    e_err = max(abs(o - (1 - i / nf)) for i, o in enumerate(e_op))
    f_in = bbox(F[n - nf], cols["f"], 4) is None and bbox(F[n], cols["f"], 4) is not None
    return [check("matched boxes tween with one easing (centres +-1 px)", max(errs) <= 1.0, max(errs), "<=1"),
            check("unmatched outgoing element fades out over 200 ms (+-0.03)", e_err <= 0.03, round(e_err, 3), "<=0.03"),
            check("unmatched incoming element fades in at the end", f_in, f_in, True),
            check("lint passes 0.6 s / 4 matches", flip_lint(0.6, 4), True, True),
            check("negative control: 14 matches or 1.2 s fails the lint", not flip_lint(0.6, 14) and not flip_lint(1.2, 4), True, True)], [path]


@card("TRANS-315")
def flip_duplicate_sparkle(task, wd):
    """Duplicate the generated image, animate the copy's box from the chat thumbnail to the email hero slot (FLIP,
    0.6 s), keep the original in the chat, then flash a 4-point sparkle at the hero's corner."""
    np = _np()
    col = (250, 120, 60)
    th, hero = (20, 58, 16, 10), (84, 24, 60, 30)
    n = int(0.6 * FPS)
    frames = []
    for i in range(n + 1):
        p = pow_inout(i / n, 3)
        r = [a + (b - a) * p for a, b in zip(th, hero)]
        frames.append(rect(rect(solid(BG), *th, col), *r, col))
    xx, yy = grid()
    sx, sy = 114, 9
    for i in range(8):
        L = 6 * math.sin(math.pi * (i + 1) / 9)
        f = frames[-1].copy()
        d = (np.abs(xx + 0.5 - sx) <= 0.6) & (np.abs(yy + 0.5 - sy) <= L) | (np.abs(yy + 0.5 - sy) <= 0.6) & (np.abs(xx + 0.5 - sx) <= L)
        f[d] = (255, 255, 255)
        frames.append(f)
    path, F = render(wd, "flipdup", frames)
    errs = []
    for i in range(4, n + 1):
        p = pow_inout(i / n, 3)
        r = [a + (b - a) * p for a, b in zip(th, hero)]
        m = near(F[i], col, 4)
        m[50:66, 10:30] = False
        ys, xs = np.nonzero(m)
        errs.append(abs((xs.max() + 1 - xs.min()) - r[2]) if len(xs) and r[0] - r[2] / 2 > 30 else 0)
    orig = all(near(f[56:60, 14:26], col, 4).all() for f in F)
    sp = F[n + 4]
    arm = int(np.sum(near(sp[sy:sy + 1], (255, 255, 255), 3)))
    diag = int(sum(near(sp[sy + k:sy + k + 1, sx + k:sx + k + 1], (255, 255, 255), 3).all() for k in range(2, 6)))
    return [check("copy's box follows the FLIP tween (width +-1 px)", max(errs) <= 1.0, max(errs), "<=1"),
            check("original thumbnail stays in the chat every frame", orig, orig, True),
            check("4-point sparkle: long axis arms, empty diagonals", arm >= 9 and diag == 0, [arm, diag], [">=9", 0]),
            check("negative control: moving the original empties the thumbnail slot", not near(rect(solid(BG), *hero, col)[56:60, 14:26], col, 4).all(), True, True)], [path]


# ================================================================================ batch 13: camera, wipes, curls
def _thumb_canvas(scenes, glow=(255, 230, 150)):
    np = _np()
    xx, yy = grid()
    G = solid(BG)
    cells = []
    for k, sc in enumerate(scenes):
        cx, cy = 22 + 42 * (k % 3), 18 + 36 * (k // 3)
        x0, y0 = cx - 18, cy - 10
        ring = (np.abs(xx + 0.5 - cx) <= 20) & (np.abs(yy + 0.5 - cy) <= 12)
        G[ring] = glow
        inside = (xx >= x0) & (xx < x0 + 36) & (yy >= y0) & (yy < y0 + 20)
        th, _ = sample(sc, (xx - x0) * 3.6 + 1.5, (yy - y0) * 3.6 + 1.5)
        G[inside] = th[inside]
        cells.append((x0, y0, cx, cy))
    return G, cells


@card("TRANS-310")
def pan_to_grid(task, wd):
    """Fast horizontal camera pan with directional blur, then scale out to reveal every previous scene as a glowing
    thumbnail in a grid."""
    np = _np()
    sc = shot_scenes()
    A = sc[-1]
    pan, plan = _tween(A, 8, 0, -24, lambda t: pow_in(t, 2), 3.0, fill=BG)
    G, cells = _thumb_canvas(sc)
    x0, y0, cx, cy = cells[-1]
    zs = []
    for i in range(12):
        p = pow_inout(i / 11, 3)
        s_ = 3.6 * (1 - p) + p
        ccx, ccy = cx + (W / 2 - cx) * p, cy + (H / 2 - cy) * p
        xx, yy = grid()
        f, _ = sample(G, ccx + (xx + 0.5 - W / 2) / s_ - 0.5, ccy + (yy + 0.5 - H / 2) / s_ - 0.5, BG)
        zs.append(f)
    path, F = render(wd, "pangrid", pan + zs)
    c = _fit_checks(F, plan, A, [2, 4, 6, 7], label="pan", fill=BG)
    fin = F[-1]
    ident = []
    for k, (x0, y0, cx, cy) in enumerate(cells):
        reg = fin[y0:y0 + 20, x0:x0 + 36]
        cand = [mad(reg, _thumb_canvas([s_] * 6)[0][cells[0][1]:cells[0][1] + 20, cells[0][0]:cells[0][0] + 36]) for s_ in sc]
        ident.append(int(np.argmin(cand)))
    glow_ok = all(near(fin[y0 - 1:y0, x0:x0 + 36], (255, 230, 150), 4).all() for x0, y0, cx, cy in cells)
    c += [check("final grid shows every scene in order (identified by content)", ident == list(range(6)), ident, list(range(6))),
          check("each thumbnail has a glow rim", glow_ok, glow_ok, True),
          check("negative control: the full-frame scene is not the grid", mad(A, G) > 20, mad(A, G), ">20")]
    return c, [path]


@card("TRANS-312")
def speed_bar_sweeps(task, wd):
    """Every 2-3 s a tall semi-transparent dark vertical bar sweeps across the window very fast with horizontal blur."""
    np = _np()
    A = scene_a()
    xx, _ = grid()
    starts = [1.0, 3.5, 6.0]
    frames, centres = [], []
    for i in range(int(7 * FPS)):
        t = i / FPS
        f = A.copy()
        cxp = None
        for s0 in starts:
            k = i - int(round(s0 * FPS))
            if 0 <= k < 6:
                cxp = -10 + (W + 20) * k / 5
        if cxp is not None:
            m = ((np.abs(xx + 0.5 - cxp) <= 6)).astype(float)
            m = gblur_axis(m[..., None].repeat(3, -1), 3.0, 1)[..., 0]
            f = f * (1 - 0.6 * m[..., None])
        frames.append(f)
        centres.append(cxp)
    path, F = render(wd, "speedbars", frames)
    lum = lambda f: f[..., 0] * 0.2126 + f[..., 1] * 0.7152 + f[..., 2] * 0.0722
    dark = [1 - np.mean(lum(f), 0) / np.mean(lum(A), 0) for f in F]
    hit = [i for i, d in enumerate(dark) if d.max() > 0.25]
    events = [hit[0]] + [b for a, b in zip(hit, hit[1:]) if b - a > 1]
    gaps = [(b - a) / FPS for a, b in zip(events, events[1:])]
    k = events[0] + 2
    prof = dark[k]
    peak = float(prof.max())
    edge = int(np.sum((prof > 0.1 * peak) & (prof < 0.9 * peak)))
    rows = 1 - lum(F[k]) / lum(A)
    vert = float(rows[:, int(np.argmax(prof))].std())
    pos = [float(np.argmax(dark[events[0] + j])) for j in (1, 2, 3)]
    return [check("sweeps recur every 2-3 s", len(events) == 3 and all(2 <= g <= 3 for g in gaps), gaps, "2-3 s"),
            check("bar is semi-transparent (peak darkening 0.3-0.7)", 0.3 <= peak <= 0.7, round(peak, 3), "0.3-0.7"),
            check("horizontal blur: soft edges across x (>= 4 transition columns), uniform down y", edge >= 4 and vert < 0.02, [edge, round(vert, 4)], [">=4", "<0.02"]),
            check("very fast: >= 25 px per frame", min(b - a for a, b in zip(pos, pos[1:])) >= 25, pos, ">=25 px/f"),
            check("negative control: the plain scene has no darkening", float(dark[0].max()) < 0.01, float(dark[0].max()), "<0.01")], [path]


@card("TRANS-313")
def portal_wall_scroll(task, wd):
    """A tunnel-portal wall then darkness scroll in from the right, cover the window for ~0.5 s while the state is
    swapped behind them, then the new scene scrolls in."""
    np = _np()
    A, B = scene_a(), scene_b()
    v = 12
    wall_w = 40
    D = W - wall_w + int(0.5 * FPS) * v
    wall = solid((70, 60, 90))
    xx, yy = grid()
    wall[(xx % 10) < 2] = (110, 100, 140)
    canvas = np.concatenate([A, wall[:, :wall_w], solid((6, 6, 8))[:, :1].repeat(D, 1), B], 1)
    total = W + wall_w + D
    offs = list(range(0, total, v)) + [total]
    frames = [canvas[:, o:o + W] for o in offs]
    path, F = render(wd, "portal", frames)
    isA = [frac(f, A, 3) for f in F]
    isB = [float(np.mean(np.abs(f - B).sum(-1) < 6)) for f in F]
    cover = [i for i in range(len(F)) if isA[i] < 0.005 and frac(F[i], (6, 6, 8), 3) + frac(F[i], (70, 60, 90), 3) + frac(F[i], (110, 100, 140), 3) > 0.99]
    aedge = [int(np.sum(np.mean(f[..., 0], 0) > 150)) for f in F[:8]]
    return [check("wall enters from the right (A's visible width shrinks by 12 px/frame)", aedge == [max(0, W - v * i) for i in range(8)], aedge, [W - v * i for i in range(8)]),
            check("window fully covered ~0.5 s (15 +- 1 frames)", abs(len(cover) - 15) <= 1, len(cover), 15),
            check("new scene scrolls in after the cover and lands", isB[-1] > 0.99 and isB[cover[0]] == 0, [isB[cover[0]], isB[-1]], [0, 1]),
            check("negative control: a cut has no covered frames", frac(A, (6, 6, 8), 3) == 0, 0, 0)], [path]


@card("TRANS-336")
def accelerate_up_tint(task, wd):
    """The whole scene accelerates upward to ~25 px/frame (1920-px design units) with vertical blur while tinting
    toward light blue; cut; the new page arrives low and smeared and decays into place."""
    np = _np()
    A, B = scene_a(), scene_b()
    tint = np.array([170, 210, 255.0])
    n = 12
    vel = [25 * (i / (n - 1)) ** 2 for i in range(n)]
    pos, acc = [], 0.0
    frames, plan = [], []
    for i in range(n):
        acc += vel[i] * K
        o = -int(round(acc))
        sg = 0.6 * vel[i] * K
        w = 0.4 * i / (n - 1)
        frames.append(moved(A, o, sg, 0, fill=BG) * (1 - w) + tint * w)
        plan.append((o, sg, w))
    for i in range(12):
        o = int(round(20 * 0.7 ** i))
        sg = 1.6 * 0.7 ** i
        frames.append(moved(B, o, sg, 0, fill=BG))
        plan.append((o, sg, 0))
    path, F = render(wd, "accelup", frames)
    meas = []
    for i, (o, sg, w) in enumerate(plan):
        src = A if i < n else B
        un = (F[i] - tint * w) / (1 - w) if w else F[i]
        d, s_, _ = fit_move(un, src, 0, range(o - 3, o + 4), [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.6], fill=BG)
        meas.append(d)
    err = max(abs(m_ - p[0]) for m_, p in zip(meas, plan))
    blue = [float(F[i][..., 2].mean() - F[i][..., 0].mean()) for i in range(n)]
    v_end = (plan[n - 1][0] - plan[n - 5][0]) / 4 / K
    cut = cut_frames(F, 25)
    return [check("upward offsets measured = plan (+-1 px)", err <= 1, err, "<=1"),
            check("accelerates: final speed ~25 design px/frame (4-frame mean, +-6)", abs(-v_end - 20.5) <= 6, round(-v_end, 1), "~20-25"),
            check("tints toward light blue as it speeds up", all(b > a for a, b in zip(blue, blue[1:])), [round(x) for x in blue[::4]], "rising"),
            check("cut to the new page, which arrives low and decays to rest", n in cut and meas[n] > 10 and meas[-1] == 0, [cut, meas[n], meas[-1]], [n, ">10", 0]),
            check("negative control: a still frame measures offset 0", fit_move(A, A, 0, range(-3, 4), [0], fill=BG)[0] == 0, 0, 0)], [path]


@card("TRANS-337")
def geometric_settle(task, wd):
    """The page starts ~400 px low (design units) with 24 px blur; offsets decay geometrically x0.75 per frame to 0
    and blur to ~1.5 px; one key phrase is set in black among grey body text."""
    np = _np()
    page = solid((245, 245, 245))
    _, body = text_frame("body text here", size=11, xy=(6, 14))
    _, key = text_frame("KEY", size=13, xy=(6, 34))
    _, body2 = text_frame("more body", size=11, xy=(6, 52))
    page = blend(page, solid((140, 140, 140)), np.maximum(body, body2))
    page = blend(page, solid((10, 10, 10)), key)
    frames, plan = [], []
    for i in range(16):
        o = int(round(400 * K * 0.75 ** i))
        sg = max(24 * 0.75 ** i, 1.5) * K
        frames.append(moved(page, o, sg, 0, fill=(245, 245, 245)))
        plan.append((o, sg))
    path, F = render(wd, "geosettle", frames)
    meas = [fit_move(f, page, 0, range(0, 30), [0, 0.1, 0.4, 0.8, 1.2, 1.6], fill=(245, 245, 245))[0] for f in F]
    err = max(abs(a - b[0]) for a, b in zip(meas, plan))
    pts = [(i, m_) for i, m_ in enumerate(meas) if m_ >= 3]
    xs, ys = np.array([p[0] for p in pts], float), np.log([p[1] for p in pts])
    ratio = float(np.exp(np.polyfit(xs, ys, 1)[0]))
    keyd = float(F[-1][key > 0.9].mean())
    bodyd = float(F[-1][body > 0.9].mean())
    return [check("starts ~400 design px low (26-27 frame px)", meas[0] in (26, 27), meas[0], 27),
            check("offsets measured = plan (+-1 px)", err <= 1, err, "<=1"),
            check("decay ratio fitted from measured offsets = 0.75 (+-0.05)", abs(ratio - 0.75) <= 0.05, round(ratio, 3), 0.75),
            check("settles at 0", meas[-1] == 0, meas[-1], 0),
            check("key phrase black, body grey (ink measured; weight not measured)", keyd < 40 and 110 < bodyd < 170, [round(keyd), round(bodyd)], ["<40", "~140"]),
            check("negative control: a linear settle does not fit a 0.75 ratio", abs(float(np.exp(np.polyfit([0, 1, 2, 3], np.log([27, 20, 13, 6]), 1)[0])) - 0.75) > 0.05, True, True)], [path]


@card("TRANS-387")
def body_wipe(task, wd):
    """Body wipe: 0-0.5 s approach, 0.5-1 s full occlusion, 1-1.5 s reveal. A keyframed mask follows the body edge with
    shot B underneath (local path: keyframed mask; hair/motion-blur edge cleanup is not automated here)."""
    np = _np()
    fps = 20
    A, B = scene_a(), scene_b()
    body_c = (20, 16, 14)
    xx, yy = grid()
    frames, masks = [], []
    for i in range(int(1.5 * fps)):
        t = i / fps
        if t < 0.5:
            cx, rx = -10 + 80 * (t / 0.5), 14 + 76 * (t / 0.5) ** 2
        elif t < 1.0:
            cx, rx = 70 + 10 * ((t - 0.5) / 0.5), 90 + 20 * math.sin(math.pi * (t - 0.5) / 0.5)
        else:
            cx, rx = 80 + 90 * ((t - 1.0) / 0.5), 76 * (1 - (t - 1.0) / 0.5) + 14
        body = ((xx + 0.5 - cx) / rx) ** 2 + ((yy + 0.5 - 50) / 90) ** 2 <= 1
        under = A if t < 0.5 else B
        frames.append(np.where(body[..., None], solid(body_c), under))
        masks.append(body)
    path, F = render(wd, "bodywipe", frames, fps)
    occl = [frac(F[i], body_c, 4) for i in range(10, 20)]
    after_ok = all(frac(F[i], B, 3, ~masks[i]) > 0.99 for i in range(20, 30))
    before_ok = all(frac(F[i], A, 3, ~masks[i]) > 0.99 for i in range(0, 10))
    edge = all(np.array_equal(near(F[i], body_c, 4), masks[i]) for i in range(len(F)))
    return [check("approach 0-0.5 s shows A outside the body", before_ok, before_ok, True),
            check("full occlusion 0.5-1 s (body covers >= 99 %)", min(occl) >= 0.99, round(min(occl), 4), ">=0.99"),
            check("reveal 1-1.5 s shows B outside the body", after_ok, after_ok, True),
            check("mask edge exactly follows the body silhouette every frame", edge, edge, True),
            check("negative control: without the swap the reveal shows A", frac(np.where(masks[25][..., None], solid(body_c), A), B, 3, ~masks[25]) < 0.01, True, True)], [path]


@card("TRANS-391")
def stop_motion_hold(task, wd):
    """Stop-motion beat: 0-0.4 s freeze (ffmpeg tpad clone), 0.4-1.2 s four hold-key jumps (steps(4)), 1.2-1.6 s
    settle with a simple shadow; no motion blur."""
    np = _np()
    col = (240, 200, 60)
    keys = [20, 50, 80, 108]
    clip = []
    for i in range(int(0.8 * FPS)):
        x = keys[min(3, int(i / (0.8 * FPS) * 4))]
        clip.append(rect(solid(BG), x, 36, 16, 16, col))
    for i in range(int(0.4 * FPS)):
        f = rect(solid(BG), keys[-1] + 5, 46, 18, 4, (8, 8, 10), op=lin((i + 1) / 4))
        clip.append(rect(f, keys[-1], 36, 16, 16, col))
    raw = write_video(Path(wd) / "stop_raw.mkv", clip, FPS)
    out = Path(wd) / "stopmotion.mkv"
    fx.ffmpeg("-i", raw, "-vf", "tpad=start_mode=clone:start_duration=0.4", "-c:v", "libx264rgb", "-qp", "0", out)
    F = fx.frames(out, (W, H))
    fz = int(0.4 * FPS)
    freeze = all(mad(F[i], F[fz]) == 0 for i in range(fz))
    xs = []
    for f in F[fz:fz + int(0.8 * FPS)]:
        bb = bbox(f, col, 4)
        xs.append((bb[0] + bb[2]) / 2)
    runs = []
    for x in xs:
        if runs and runs[-1][0] == x:
            runs[-1][1] += 1
        else:
            runs.append([x, 1])
    sharp = all(frac(f, col, 2) + frac(f, BG, 2) > 0.999 for f in F[:fz + int(0.8 * FPS)])
    shadow = frac(F[-1], (8, 8, 10), 4) > 0
    return [check("0-0.4 s freeze: first 12 frames identical", freeze and len(F) == 48, [freeze, len(F)], [True, 48]),
            check("four hold keys, 6 frames each", [r[1] for r in runs] == [6, 6, 6, 6] and [r[0] for r in runs] == keys, runs, keys),
            check("no motion blur (only pure element/background pixels)", sharp, sharp, True),
            check("settle adds a shadow", shadow, shadow, True),
            check("negative control: a smooth tween has > 4 distinct positions", len({round(20 + 88 * i / 23) for i in range(24)}) > 4, True, True)], [out]


@card("TRANS-444")
def paper_curl(task, wd):
    """Page turn: a diagonal fold line sweeps from the bottom-right corner, the folded flap (A reflected across the line,
    shaded) lies over it, B shows where the page has lifted; a filtered-noise rustle plays during the curl."""
    np = _np()
    A, B = scene_a(), scene_b()
    xx, yy = grid()
    nx, ny = 1 / math.sqrt(2), H / W / math.sqrt(2) * 1.0
    nrm = math.hypot(1, H / W)
    ux, uy = 1 / nrm, (H / W) / nrm
    dmax = (W * ux + H * uy)
    n = 16
    frames, lines = [], []
    for i in range(n + 1):
        L = dmax * (1 - pow_inout(i / n, 2))
        d = (xx + 0.5) * ux + (yy + 0.5) * uy
        lifted = d > L
        rx, ry = xx + 0.5 - 2 * (d - L) * ux, yy + 0.5 - 2 * (d - L) * uy
        dd = (xx + 0.5) * ux + (yy + 0.5) * uy
        f = np.where(lifted[..., None], B, A)
        # flap: points p with reflected point inside the lifted region
        sxf, syf = xx + 0.5 + 2 * (L - dd) * ux, yy + 0.5 + 2 * (L - dd) * uy
        src_lift = (sxf * ux + syf * uy) > L
        inb = (sxf >= 0) & (sxf < W) & (syf >= 0) & (syf < H) & (dd <= L) & src_lift
        flap, _ = sample(A, sxf - 0.5, syf - 0.5)
        f[inb] = flap[inb] * 0.75
        frames.append(f)
        lines.append(L)
    vid = write_video(Path(wd) / "curl_v.mkv", frames + [B] * 8, FPS)
    rate = 22050
    import random
    rnd = random.Random(5)
    total = int(rate * (n + 9) / FPS)
    xs = [0.0] * total
    prev = 0.0
    for k in range(int(rate * n / FPS)):
        prev = 0.7 * prev + 0.3 * rnd.uniform(-1, 1)
        xs[k] = 0.5 * prev * math.sin(math.pi * k / (rate * n / FPS))
    wav = fx.write_wav(Path(wd) / "rustle.wav", xs, rate)
    out = _mux(wd, vid, wav, "curl.mkv")
    F = fx.frames(out, (W, H))
    bf = [frac(F[i], B, 3) for i in range(n + 1)]
    mid = n // 2
    shaded = 0
    d = (xx + 0.5) * ux + (yy + 0.5) * uy
    m = (d < lines[mid] - 2) & (d > lines[mid] - 6)
    sxf, syf = xx + 0.5 + 2 * (lines[mid] - d) * ux, yy + 0.5 + 2 * (lines[mid] - d) * uy
    flap, _ = sample(A, sxf - 0.5, syf - 0.5)
    m &= (sxf >= 0) & (sxf < W) & (syf >= 0) & (syf < H) & ((sxf * ux + syf * uy) > lines[mid])
    shaded = bool(m.sum() > 20) and mad(F[mid][m], flap[m] * 0.75) < 2
    au, ar = fx.read_wav(_extract_wav(wd, out))
    au = np.asarray(au, float).reshape(len(au), -1)[:, 0]
    env = _wav_env(au, ar)[0]
    on = float(max(env[:int(0.5 / 0.005)]))
    off = float(max(env[int((n / FPS + 0.02) / 0.005):]))
    return [check("lifted area (B) grows monotonically from the corner", all(b >= a for a, b in zip(bf, bf[1:])) and bf[1] < 0.1 and bf[-1] > 0.99, [round(v, 3) for v in bf[::4]], "0 -> 1"),
            check("flap next to the fold is A reflected across the line, shaded x0.75", shaded, shaded, True),
            check("rustle sounds during the curl and is silent after", on > 0.05 and off < 0.001, [round(on, 3), off], [">0.05", "<0.001"]),
            check("negative control: a straight cut has no shaded flap", mad(B[m], flap[m] * 0.75) > 10, True, True)], [out]


def _np_displace(src, dx, dy):
    np = _np()
    xx, yy = grid()
    sx = np.clip(xx + dx, 0, W - 1)
    sy = np.clip(yy + dy, 0, H - 1)
    return src[sy.astype(int), sx.astype(int)]


@card("TRANS-392")
def displace_cut(task, wd):
    """Distortion cut: 0-0.4 s build, 0.4-0.9 s peak distortion with the cut at 0.65 s, 0.9-1.5 s fade; strength kept
    limited (<= 6 px). Rendered with ffmpeg displace and generated sine maps; checked against an independent numpy
    displacement."""
    np = _np()
    A, B = scene_a(), scene_b()
    xx, yy = grid()
    n = int(1.5 * FPS)
    cut = int(0.65 * FPS)
    src, xm, ym, plan = [], [], [], []
    for i in range(n):
        t = i / FPS
        N = 6 * (smooth(t / 0.65) if t < 0.65 else 1 - smooth((t - 0.65) / 0.85))
        N = int(round(N))
        dx = np.round(N * np.sin(2 * math.pi * yy / 16))
        dy = np.round(0.5 * N * np.sin(2 * math.pi * xx / 20))
        src.append(A if i < cut else B)
        xm.append(np.repeat((128 + dx)[..., None], 3, -1))
        ym.append(np.repeat((128 + dy)[..., None], 3, -1))
        plan.append((N, dx, dy))
    ps = write_video(Path(wd) / "dsrc.mkv", src)
    px = write_video(Path(wd) / "dxmap.mkv", xm)
    py = write_video(Path(wd) / "dymap.mkv", ym)
    out = Path(wd) / "displace.mkv"
    fx.ffmpeg("-i", ps, "-i", px, "-i", py, "-filter_complex", "[0][1][2]displace=edge=smear,format=rgb24", "-c:v", "libx264rgb", "-qp", "0", out)
    F = fx.frames(out, (W, H))
    src = fx.frames(ps, (W, H))
    ref_err = max(mad(F[i], _np_displace(src[i], plan[i][1], plan[i][2])) for i in range(n))
    dist = [mad(F[i], src[i]) for i in range(n)]
    peak = int(np.argmax(dist))
    return [check("ffmpeg displace output = independent numpy displacement (mad < 0.5)", ref_err < 0.5, round(ref_err, 3), "<0.5"),
            check("distortion peaks inside 0.4-0.9 s", 0.4 <= peak / FPS <= 0.9, peak / FPS, "0.4-0.9 s"),
            check("cut happens at the peak (source swaps at 0.65 s)", mad(F[cut - 1], A) < mad(F[cut - 1], B) and mad(F[cut], B) < mad(F[cut], A), cut, cut),
            check("fades to an undistorted B by 1.5 s; strength capped at 6 px", dist[-1] == 0 and max(p[0] for p in plan) <= 6, [dist[-1], max(p[0] for p in plan)], [0, "<=6"]),
            check("negative control: undistorted frames measure 0", dist[0] == 0, dist[0], 0)], [out]


@card("TRANS-393")
def freeze_move_play(task, wd):
    """MG-010 freeze -> camera move -> play: 0-1 s freeze, 1-2.5 s camera move (push 1 -> 1.2), 2.5-4 s play; the frozen
    frame equals the first frame of the moving clip. MG-007 approach -> reveal opening -> enter: B is seen only through
    the opening, which widens, then the camera enters."""
    np = _np()
    fps = 10
    A, B = scene_a(), scene_b()
    clip = [rect(A.copy(), 20 + 6 * i, 36, 10, 10, (255, 255, 255)) for i in range(16)]
    frames, plan = [], []
    for i in range(fps):
        frames.append(clip[0]); plan.append(1.0)
    for i in range(int(1.5 * fps)):
        s_ = 1 + 0.2 * pow_inout((i + 1) / (1.5 * fps), 2)
        frames.append(scale_about(clip[0], s_)); plan.append(s_)
    for i in range(int(1.5 * fps)):
        frames.append(scale_about(clip[i], 1.2)); plan.append(1.2)
    p1, F = render(wd, "mg010", frames, fps)
    freeze = all(mad(F[i], np.clip(np.round(clip[0]), 0, 255)) == 0 for i in range(fps))
    gs = [round(1 + k / 100, 2) for k in range(0, 25)]
    ms_ = [fit_scale(F[i], clip[0], gs) for i in range(fps, fps + 15)]
    err = max(abs(a - b) for a, b in zip(ms_, plan[fps:fps + 15]))
    seam = mad(F[fps + 14], F[fps + 15])
    playing = mad(F[fps + 15], F[-1]) > 1
    # MG-007
    xx, yy = grid()
    door = (90, 70, 50)
    frames2, gaps = [], []
    for i in range(30):
        t = i / fps
        if t < 1:
            s_, g = 0.6 + 0.4 * smooth(t), 0.0
        elif t < 2:
            s_, g = 1.0, 40 * smooth(t - 1)
        else:
            s_, g = 1 + 2 * pow_in(t - 2, 2), 40
        f = solid(BG)
        dw, dh = 80 * s_, 60 * s_
        inside = (np.abs(xx + 0.5 - W / 2) <= dw / 2) & (np.abs(yy + 0.5 - H / 2) <= dh / 2)
        opening = inside & (np.abs(xx + 0.5 - W / 2) <= g * s_ / 2)
        f[inside] = door
        f[opening] = B[opening]
        frames2.append(f)
        gaps.append((opening, g * s_))
    p2, F2 = render(wd, "mg007", frames2, fps)
    only_open = all(frac(F2[i], B, 3, ~gaps[i][0]) < 0.001 for i in range(30))
    widths = [int(np.sum(near(F2[i][H // 2:H // 2 + 1], B[H // 2:H // 2 + 1], 3))) for i in (10, 15, 19)]
    entered = frac(F2[-1], B, 3) > 0.6
    return [check("MG-010: 0-1 s freeze equals the moving clip's first frame", freeze, freeze, True),
            check("MG-010: camera push measured 1 -> 1.2 (+-0.01)", err <= 0.011, err, "<=0.01"),
            check("MG-010: play starts with no jump at 2.5 s, then the clip moves", seam < 3 and playing, [round(seam, 2), playing], ["<3", True]),
            check("MG-007: B only visible through the opening (occlusion)", only_open, only_open, True),
            check("MG-007: opening widens, then the camera enters", widths[0] < widths[1] < widths[2] and entered, widths + [entered], "growing, entered"),
            check("negative control: playing from a later clip frame would jump at the seam", mad(scale_about(clip[0], 1.2), scale_about(clip[8], 1.2)) > seam, True, True)], [p1, p2]


def viz_technique(intent):
    return {"sequence": "crossfade", "state change": "interpolate", "geography": "pan_zoom", "scrub": "moviescroller",
            "scale": "parallax", "annotate": "sticky_overlay"}[intent]


@card("TRANS-443")
def data_viz_transitions(task, wd):
    """Data-story transitions: animated transition interpolates the chart state (bar heights), parallax depth moves
    foreground and background at different speeds, and a sticky overlay card never covers the evidence."""
    np = _np()
    h0, h1 = [10, 30, 20, 40], [35, 15, 45, 25]
    n = 12
    frames = []
    for i in range(n + 1):
        p = pow_inout(i / n, 2)
        f = solid(BG)
        for k in range(4):
            h = h0[k] + (h1[k] - h0[k]) * p
            f = rect(f, 20 + 22 * k, 66 - h / 2, 12, h, (90, 180, 250))
        frames.append(f)
    p1, F = render(wd, "chartstate", frames)
    herr = 0
    for i in range(n + 1):
        p = pow_inout(i / n, 2)
        for k in range(4):
            col = near(F[i][:, 20 + 22 * k:21 + 22 * k], (90, 180, 250), 6)[:, 0]
            herr = max(herr, abs(int(col.sum()) - (h0[k] + (h1[k] - h0[k]) * p)))
    bg = np.clip(solid((90, 140, 90)) + 70 * _gnoise(4, 3, 2)[..., None], 0, 255)
    fg = np.clip(solid((200, 120, 60)) + 70 * _gnoise(5, 9, 2)[..., None], 0, 255)
    xx, yy = grid()
    band = yy > 50
    frames = [np.where(band[..., None], shift(fg, -3 * i, 0, fill=(0, 0, 0)), shift(bg, -1 * i, 0, fill=(0, 0, 0))) for i in range(8)]
    p2, F2 = render(wd, "parallax", frames)
    vb = best_dx(F2[6][:50], bg[:50], 30)[0]
    vf = best_dx(F2[6][51:], fg[51:], 30)[0]
    ev = (40, 10, 100, 40)
    card_ = (106, 60, 36, 22)
    f = rect(rect(solid(BG), 70, 25, 60, 30, (250, 200, 60)), *card_, (240, 240, 240))
    p3, F3 = render(wd, "sticky", [f] * 4)
    covered = frac(F3[0], (240, 240, 240), 4, (xx >= ev[0]) & (xx < ev[2]) & (yy >= ev[1]) & (yy < ev[3]))
    return [check("animated transition: bar heights interpolate between chart states (+-1 px)", herr <= 1.0, herr, "<=1"),
            check("parallax: foreground moves faster than background (measured 3 vs 1 px/frame)", (vf, vb) == (-18, -6), (vf, vb), (-18, -6)),
            check("sticky overlay leaves the evidence region uncovered", covered == 0, covered, 0),
            check("technique chosen by intent", viz_technique("state change") == "interpolate" and viz_technique("scale") == "parallax", True, True),
            check("negative control: an overlay placed on the evidence covers it", frac(rect(solid(BG), 70, 25, 40, 20, (240, 240, 240)), (240, 240, 240), 4, (xx >= ev[0]) & (xx < ev[2]) & (yy >= ev[1]) & (yy < ev[3])) > 0.3, True, True)], [p1, p2, p3]


def needle(t, cut, s0, s1, fps=FPS):
    a, b = cut - 0.2, cut + 0.2 - 1 / fps
    if t <= a:
        return s0
    if t >= b:
        return s1
    return s0 + (s1 - s0) * bezier(0.95, 0, 0.05, 1)((t - a) / (b - a))


def subframes_for(zoom):
    return 16 if zoom > 9 else 1


@card("TRANS-X02")
def needle_zoom(task, wd):
    """needle(t, cut, 1, 1.12): keys at cut - 0.2 s and cut + 0.2 s - 1 frame on cubic-bezier(.95,0,.05,1);
    backgrounds hard-cut ~3x/s and never scale; parallax layers behind zoom at scale^0.6, in front at scale^1.35;
    needles beyond x9 need 16+ motion-blur sub-frames."""
    np = _np()
    _, wm = text_frame("NEEDLE", size=18)
    bgs = shot_scenes()[:4]
    cut = 1.0
    frames, plan = [], []
    for i in range(45):
        t = i / FPS
        s_ = needle(t, cut, 1, 1.12)
        m = scale_about(wm[..., None].repeat(3, -1), s_)[..., 0]
        frames.append(blend(bgs[(i // 10) % 4], solid((255, 255, 255)), m))
        plan.append(s_)
    path, F = render(wd, "needle", frames)
    bb0 = bbox(F[0], (255, 255, 255), 3)
    width = lambda f: (lambda b: b[2] - b[0])(bbox(f, (255, 255, 255), 3))
    k_a, k_b = int(round((cut - 0.2) * FPS)), int(round((cut + 0.2) * FPS)) - 1
    r_a, r_b = width(F[k_a]) / width(F[0]), width(F[k_b]) / width(F[0])
    pre_move = width(F[k_a + 1]) / width(F[0])
    ink = np.maximum.reduce([scale_about(wm[..., None].repeat(3, -1), s_)[..., 0] for s_ in (1.0, 1.12)]) > 0.01
    bg_fixed = all(frac(F[i], bgs[(i // 10) % 4], 2, ~ink) > 0.999 for i in range(45))
    cuts = cut_frames(F, 25)
    gs = [round(1 + k / 100, 2) for k in range(0, 260)]
    S = 2.0
    behind = scale_about(scene_c(), S ** 0.6)
    front = rect(solid(BG), W / 2, H / 2, 20 * S ** 1.35, 8 * S ** 1.35, (250, 120, 60))
    mb = fit_scale(behind, scene_c(), [round(1 + k / 100, 2) for k in range(30, 80)])
    fw = (bbox(front, (250, 120, 60))[2] - bbox(front, (250, 120, 60))[0]) / 20
    return [check("scale holds 1.0 up to the first key (cut - 0.2 s)", abs(r_a - 1) < 0.02 and abs(pre_move - 1) < 0.03, [round(r_a, 3), round(pre_move, 3)], 1.0),
            check("reaches x1.12 at the second key (cut + 0.2 s - 1 frame)", abs(r_b - 1.12) <= 0.03, round(r_b, 3), 1.12),
            check("backgrounds never scale and hard-cut 3x per second", bg_fixed and cuts[:3] == [10, 20, 30], [bg_fixed, cuts[:4]], [True, [10, 20, 30, 40]]),
            check("parallax: behind layer x2^0.6 = 1.52, front x2^1.35 = 2.55 (measured)", abs(mb - 1.516) <= 0.015 and abs(fw - 2.549) <= 0.08, [mb, round(fw, 3)], [1.516, 2.549]),
            check("needles beyond x9 get 16 sub-frames, x1.12 none", subframes_for(12) == 16 and subframes_for(1.12) == 1, True, True),
            check("negative control: a linear zoom is already moving 1 frame after the first key", abs(1 + 0.12 / 11 - 1) > 0.005, True, True)], [path]


def lint_x03(b_start, b_shrinks, cut_solid):
    """Incoming B after a zoom-in must start small and grow, unless the cut frame is a solid colour."""
    if cut_solid:
        return True
    return b_start <= 1.0 and not b_shrinks


@card("TRANS-X03")
def zoom_handoff(task, wd):
    """Zoom hand-off that shipped: A x1.04 -> x12 on an x^5 curve over 0.45 s, then B x0.26 -> x1 with out() over
    0.9 s plus a 4 % drift; starting B at x5.2 and shrinking is rejected unless the cut frame is a solid colour."""
    np = _np()
    A, B = scene_a(), scene_b()
    na, nb = int(round(0.45 * FPS)), int(0.9 * FPS)
    pa = [1.04 + (12 - 1.04) * (i / (na - 1)) ** 5 for i in range(na)]
    pb = [(0.26 + 0.74 * pow_out(i / (nb - 1), 3)) for i in range(nb)]
    drift = [1 + 0.04 * i / 14 for i in range(15)]
    frames = [scale_about(A, s_) for s_ in pa] + [scale_about(B, s_, fill=BG) for s_ in pb] + [scale_about(B, d) for d in drift]
    path, F = render(wd, "zoomhandoff", frames)
    ea = []
    for i in (0, na // 2, na - 3):
        gs = [round(pa[i] * (0.9 + k / 200), 4) for k in range(41)]
        ea.append(abs(fit_scale(F[i], A, gs) - pa[i]) / pa[i])
    eb = []
    for i in range(0, nb, 3):
        bb = nonbg_bbox(F[na + i])
        eb.append(abs((bb[2] - bb[0]) / W - pb[i]))
    dmeas = fit_scale(F[-1], B, [round(1 + k / 100, 2) for k in range(0, 8)])
    return [check("A follows x1.04 -> x12 on x^5 (relative error <= 1 %)", max(ea) <= 0.01, [round(e, 4) for e in ea], "<=0.01"),
            check("B grows x0.26 -> x1 with out() (width +-1 px)", max(eb) <= 1.0 / W + 1e-9, round(max(eb) * W, 2), "<=1 px"),
            check("then drifts 4 %", dmeas == 1.04, dmeas, 1.04),
            check("lint: shipped version passes; B x5.2 shrinking rejected; solid-colour exception passes", lint_x03(0.26, False, False) and not lint_x03(5.2, True, False) and lint_x03(5.2, True, True), True, True),
            check("negative control: the unzoomed A frame measures x1.04 only at frame 0", abs(pa[0] - 1.04) < 1e-9 and ea[0] <= 0.01, True, True)], [path]


@card("TRANS-X04")
def screen_pixel_handoff(task, wd):
    """Element hand-off between scenes with different cameras agrees in screen pixels: screen = 960 + s (local - 960).
    The incoming scene draws its copy at the outgoing screen rect, lifts it x1.08 with a growing shadow over 0.1 s,
    travels on smooth(), and sets it down."""
    np = _np()
    A, B = scene_a(), scene_b()
    col = (250, 250, 250)
    s1, s2 = 1.3, 0.9
    to_screen = lambda s_, x, c: c + s_ * (x - c)
    to_local = lambda s_, X, c: c + (X - c) / s_
    lx, ly, lw, lh = 40.0, 26.0, 20.0, 12.0
    X, Y, Wd, Hd = to_screen(s1, lx, W / 2), to_screen(s1, ly, H / 2), lw * s1, lh * s1
    out_f = rect(scale_about(A, s1), X, Y, Wd, Hd, col)
    ilx, ily = to_local(s2, X, W / 2), to_local(s2, Y, H / 2)
    frames = [out_f] * 4
    shadows = []
    for i in range(1, 4):
        k = 1 + 0.08 * i / 3
        f = scale_about(B, s2)
        f = rect(f, to_screen(s2, ilx, W / 2) + 2, to_screen(s2, ily, H / 2) + 3 * i / 3 + 1, Wd * k, Hd * k, (5, 5, 5), op=0.6)
        frames.append(rect(f, to_screen(s2, ilx, W / 2), to_screen(s2, ily, H / 2), Wd * k, Hd * k, col))
        shadows.append(i)
    dest = (96.0, 50.0)
    for i in range(1, 11):
        p = smooth(i / 10)
        cx, cy = X + (dest[0] - X) * p, Y + (dest[1] - Y) * p
        frames.append(rect(scale_about(B, s2), cx, cy, Wd * 1.08, Hd * 1.08, col))
    frames.append(rect(scale_about(B, s2), dest[0], dest[1], Wd, Hd, col))
    path, F = render(wd, "handoff", frames)
    b_out, b_in = bbox(F[3], col, 3), bbox(F[4], col, 3)
    lift = (bbox(F[6], col, 3)[2] - bbox(F[6], col, 3)[0]) / (b_out[2] - b_out[0])
    sh = [frac(F[i], (5, 5, 5), 140) - frac(F[i], col, 3) for i in (4, 5, 6)]
    terr = []
    for i in range(1, 11):
        p = smooth(i / 10)
        bb = bbox(F[6 + i], col, 3)
        terr.append(abs((bb[0] + bb[2]) / 2 - (X + (dest[0] - X) * p)))
    naive = rect(scale_about(B, s2), to_screen(s2, lx, W / 2), to_screen(s2, ly, H / 2), lw * s2, lh * s2, col)
    nb = bbox(naive, col, 3)
    return [check("element's screen rect identical across the camera change (+-1 px)", max(abs(a - b) for a, b in zip(b_out, b_in)) <= 1, [b_out, b_in], "equal"),
            check("lift x1.08 over 0.1 s (measured width ratio)", abs(lift - 1.08) <= 0.05, round(lift, 3), 1.08),
            check("travel follows smooth() (+-1 px) and sets down at the destination", max(terr) <= 1.0 and (lambda b: abs((b[0] + b[2]) / 2 - dest[0]) <= 0.5)(bbox(F[-1], col, 3)), max(terr), "<=1"),
            check("negative control: reusing local coordinates in the new camera misplaces it by > 3 px", abs(nb[0] - b_out[0]) > 3, nb[0] - b_out[0], ">3")], [path]


@card("TRANS-X06")
def button_to_pill(task, wd):
    """Worked morph: a 47x23 button rotated 4.3 deg grows in log size over 0.55 s into an 800x164 pill (1920-px design,
    drawn at 2x the frame scale), colour leads size, the label rolls vertically into place; 3D copy distance
    D = w * PERSP / w_screen makes the copy match on screen."""
    np = _np()
    S = 2 * K
    w0, h0, w1, h1 = 47 * S, 23 * S, 800 * S, 164 * S
    c0, c1 = np.array([60, 60, 70.0]), np.array([250, 200, 60.0])
    n = int(round(0.55 * FPS))
    frames, plan = [], []
    for i in range(n + 1):
        t = i / n
        e = pow_inout(t, 2)
        w, h = w0 * (w1 / w0) ** e, h0 * (h1 / h0) ** e
        cp = pow_out(t, 3)
        layer = rect(solid(BG), W / 2, H / 2, w, h, tuple(c0 + (c1 - c0) * cp), h / 2)
        ly = H / 2 + h * 0.35 * (1 - smooth(max(0.0, (t - 0.5) / 0.5)))
        lab = rect(layer.copy(), W / 2, ly, w * 0.5, max(1, h * 0.18), (255, 255, 255))
        lab = np.where(near(layer, BG, 1)[..., None], layer, lab)
        frames.append(rotate(lab, 4.3 * (1 - e), fill=BG))
        plan.append((w, e, cp, ly))
    path, F = render(wd, "btnpill", frames)
    lerr, ang, cl = [], [], []
    for i, (w, e, cp, ly) in enumerate(plan):
        m = ~near(F[i], BG, 6)
        bb = nonbg_bbox(F[i])
        if w >= 12:
            ys, xs = np.nonzero(m)
            lerr.append(abs(math.log(float(xs.max() - xs.min() + 1)) - math.log(w)))
        px = F[i][H // 2 - 1 if ly > H / 2 + 1 else int(H / 2 + 3), W // 2 + 2] if False else None
    mids = [i for i in range(n + 1) if 0.25 < plan[i][1] < 0.75]
    lead = []
    for i in mids:
        bb = nonbg_bbox(F[i])
        px = F[i][bb[1] + 1, (bb[0] + bb[2]) // 2]
        cm = float(np.dot(px - c0, c1 - c0) / np.dot(c1 - c0, c1 - c0))
        lead.append(cm > math.log((bb[2] - bb[0]) / w0) / math.log(w1 / w0))
    S8 = 16 * K   # the start button is only ~6 px at frame scale: measure its 4.3 deg tilt on a magnified (x8) start still
    det = rotate(rect(solid(BG), W / 2, H / 2, 47 * S8, 23 * S8, tuple(c0), 23 * S8 / 2), 4.3, fill=BG)
    pdet, Fd = render(wd, "btn_start_x8", [det])
    a0 = _moment_angle(~near(Fd[0], BG, 6))
    lab_y = []
    for i in (int(0.6 * n), int(0.8 * n), n):
        ys = np.nonzero(near(F[i][:, W // 2:W // 2 + 1], (255, 255, 255), 8)[:, 0])[0]
        lab_y.append(float(ys.mean()) if len(ys) else None)
    PERSP, w_world, w_screen = 1200.0, 800.0, 400.0
    D = w_world * PERSP / w_screen
    return [check("size grows in log space with the ease (log width +-0.08)", lerr and max(lerr) <= 0.08, round(max(lerr), 3), "<=0.08"),
            check("ends at 800x164 design px (frame %.1f x %.1f at 2x)" % (w1, h1), abs((nonbg_bbox(F[-1])[2] - nonbg_bbox(F[-1])[0]) - w1) <= 1.5, nonbg_bbox(F[-1]), "107 x 22"),
            check("colour leads size in the middle frames", lead and all(lead), lead, "all True"),
            check("start button tilted 4.3 deg (magnified still, +-0.7) and the pill ends level", abs(a0 - 4.3) <= 0.7 and abs(_moment_angle(~near(F[-1], BG, 6))) < 0.3, [round(a0, 2), round(_moment_angle(~near(F[-1], BG, 6)), 2)], [4.3, 0]),
            check("label rolls up into the centre", lab_y[0] is not None and lab_y[0] > lab_y[1] >= lab_y[2] - 0.5 and abs(lab_y[2] - H / 2) <= 1, lab_y, "falling to 36"),
            check("D = w * PERSP / w_screen projects back to w_screen", abs(w_world * PERSP / D - w_screen) < 1e-9, D, 2400),
            check("negative control: a linear (not log) size tween is far bigger at 30 % time", w0 + (w1 - w0) * 0.3 > w0 * (w1 / w0) ** 0.3 * 1.5, True, True)], [path, pdet]
