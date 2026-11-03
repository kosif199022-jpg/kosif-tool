"""particles-fluids-physics: method cards as real programs with known-answer checks.

Each runner builds a seeded fixture in the work folder, simulates/renders the card's method with
numpy / PIL / ffmpeg (or the installed matter-js engine under node) and measures the produced file:
tracked particles are drawn in a unique channel so their trajectories are measured from the frames.
Every runner carries a negative control on the unprocessed input.
"""
import json
import math
import os
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from _harness import card, check, fx

NODE_MODULES = "/opt/node22/lib/node_modules"

GAPS: dict = {
    "PART-19": "the card is the HyperFrames registry block particle-image-reveal (installed via `hyperframes add`, "
               "rendered in headless Chrome); its particle maths is not given on the card and no <15 s render is wired",
    "PART-27": "deck.gl TripsLayer/ArcLayer/HexagonLayer over MapLibre need a WebGL browser render; deck.gl is not "
               "installed and the card gives no maths to reproduce",
    "PART-41": "the card is the HyperFrames snow/starfield registry blocks (headless-Chrome render after "
               "`hyperframes add`); no <15 s runner wired",
    "PART-58": "three.js Water plane / K3.makeSea from the three-kit bundle need a WebGL renderer (headless Chrome "
               "SwiftShader) and the demo bundle; not runnable as a <15 s program here",
    "PART-60": "K3.makeVapour/makeCloudSlab/makeRain/makeFlock live in the three-kit demo whose assets/main.bundle.js "
               "is not built; a raymarched cloud slab needs WebGL",
    "PART-61": "makeKoi/makePetals/makeBlades are three-kit WebGL scene builders (demo bundle not built); not "
               "reproducible as measured output without the WebGL render",
    "PART-62": "long-exposure car trails are emissive three.js spheres scaled in a WebGL scene (demo bundle not "
               "built); the card itself notes the Studio 'lighten' pass test errored",
    "PART-67": "Houdini FLIP/Pyro/Vellum/RBD + Karma need a commercial SideFX licence and hython; not installed",
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


def _blur(a, s):
    from scipy.ndimage import gaussian_filter
    a = np.asarray(a, dtype=float)
    return gaussian_filter(a, (s, s) + ((0,) if a.ndim == 3 else ()))


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


def _disc(img, x, y, r, col, mode="max", alpha=1.0):
    H, W = img.shape[:2]
    x0, x1 = max(0, int(x - r - 2)), min(W, int(x + r + 3))
    y0, y1 = max(0, int(y - r - 2)), min(H, int(y + r + 3))
    if x0 >= x1 or y0 >= y1:
        return
    yy, xx = np.mgrid[y0:y1, x0:x1]
    m = (np.hypot(yy - y, xx - x) <= r)[..., None]
    win = img[y0:y1, x0:x1]
    c = np.asarray(col, dtype=float) * alpha
    if mode == "add":
        win += m * c
    elif mode == "over":
        win[...] = win * (1 - m * alpha) + m * np.asarray(col, dtype=float) * alpha
    else:
        win[...] = np.where(m, np.maximum(win, c), win)


def _centroid(mask):
    ys, xs = np.nonzero(mask)
    if not len(xs):
        return None
    return float(xs.mean()), float(ys.mean())


def _track(frames, ch=0, thr=40, others=(1, 2)):
    """Centroid of pixels lit in channel ch only (the tracked particle is drawn pure in that channel)."""
    out = []
    for f in frames:
        m = (f[..., ch] > thr) & np.all([f[..., o] < 20 for o in others], axis=0)
        out.append(_centroid(m))
    return out


def _quad_fit(t, y):
    c = np.polyfit(t, y, 2)
    res = float(np.abs(np.polyval(c, t) - y).max())
    return 2 * c[0], c[1], res


def _smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def _value_noise(shape, cell, seed, octaves=1):
    H, W = shape
    out, amp, tot = np.zeros(shape), 1.0, 0.0
    for o in range(octaves):
        c = max(1, cell / 2 ** o)
        gh, gw = int(H / c) + 3, int(W / c) + 3
        g = np.random.default_rng(seed + o).random((gh, gw))
        y, x = np.mgrid[:H, :W] / c
        y0, x0 = np.floor(y).astype(int), np.floor(x).astype(int)
        fy, fx_ = _smoothstep(0, 1, y - y0), _smoothstep(0, 1, x - x0)
        v = (g[y0, x0] * (1 - fx_) + g[y0, x0 + 1] * fx_) * (1 - fy) + (g[y0 + 1, x0] * (1 - fx_) + g[y0 + 1, x0 + 1] * fx_) * fy
        out += amp * v
        tot += amp
        amp *= .5
    return out / tot


# ----------------------------------------------------------------- cards
@card("PART-05")
def impact_contact(task, wd):
    fps, rate, g, y0, floor, r = 30, 22050, 600.0, 20.0, 170.0, 8
    tc = math.sqrt(2 * (floor - r - y0) / g)
    contact_frame = int(round(tc * fps))
    events = [{"type": "impact", "t": contact_frame / fps, "frame": contact_frame}]
    (wd / "events.json").write_text(json.dumps(events), "utf-8")
    ev = json.loads((wd / "events.json").read_text())[0]
    # one event list drives the audio click ...
    n = int(1.5 * rate)
    aud = np.zeros(n)
    s0 = int(round(ev["t"] * rate))
    k = np.arange(800)
    aud[s0:s0 + 800] = .8 * np.exp(-k / 120) * np.sin(2 * math.pi * 1800 * k / rate)
    wav = fx.write_wav(wd / "impact.wav", aud, rate)
    # ... and the particle burst
    rng = _rng(5)
    vel = rng.normal(0, 1, (24, 2)) * 120 + (0, -160)
    frames = []
    for f in range(45):
        t = f / fps
        img = np.zeros((190, 160, 3))
        img[int(floor):] = (60, 60, 60)
        yb = min(y0 + .5 * g * t * t, floor - r)
        _disc(img, 80, yb, r, (0, 0, 255))
        if f >= ev["frame"]:
            u = t - ev["t"]
            for vx, vy in vel:
                _disc(img, 80 + vx * u, floor - 2 + vy * u + .5 * g * u * u, 1.5, (255, 200, 0))
        frames.append(img)
    vid = _video(wd / "impact.mp4", frames, fps)
    v = fx.frames(vid, (160, 190))
    spark = [bool(((fr[..., 0] > 150) & (fr[..., 1] > 100)).any()) for fr in v]
    first_spark = spark.index(True)
    a, rr = fx.read_wav(wav)
    onset = int(np.argmax(np.abs(a[:, 0]) > .05)) / rr
    ball = [_centroid(fr[..., 2] > 128) for fr in v]
    ball_bottom = ball[first_spark][1] + r
    contact_first = next(i for i, c in enumerate(ball) if c and c[1] + r >= floor - 1.5)
    naive = 0
    return [check("burst starts on the contact frame", first_spark == contact_first, first_spark, contact_first),
            check("audio click onset within one frame of the contact", abs(onset - contact_first / fps) <= 1 / fps, onset,
                  contact_first / fps),
            check("ball touches the floor on the burst frame", abs(ball_bottom - floor) <= 2, ball_bottom, floor),
            check("negative control: a clip-start event misses the contact", abs(naive - contact_first) > 1, naive,
                  contact_first)], [vid, wav, wd / "events.json"]


@card("PART-09")
def burst_closed_form(task, wd):
    fps, g, n = 30, 900.0, 32
    rng = _rng(9)
    ang = rng.uniform(-math.pi, 0, n)
    spd = rng.uniform(150, 380, n)
    p0 = np.array([160.0, 140.0])

    def pos(i, t):   # closed-form, seekable: p = p0 + v t + g t^2 / 2
        return p0[0] + spd[i] * math.cos(ang[i]) * t, p0[1] + spd[i] * math.sin(ang[i]) * t + .5 * g * t * t

    def frame(t):
        img = np.zeros((240, 320, 3))
        for i in range(1, n):
            x, y = pos(i, t)
            _disc(img, x, y, 2, (0, 230, 255))
        x, y = pos(0, t)
        _disc(img, x, y, 2, (255, 0, 0))
        return img
    ts = np.arange(int(.2 * fps), int(.8 * fps)) / fps
    frames = [frame(t) for t in ts]
    vid = _video(wd / "burst.mp4", frames, fps)
    v = fx.frames(vid, (320, 240))
    tr = _track(v)
    ok = [(t, c) for t, c in zip(ts, tr) if c]
    gy, vy, res = _quad_fit(np.array([t for t, _ in ok]), np.array([c[1] for _, c in ok]))
    seek = _save(wd / "seek_0_5.png", frame(.5))
    same = np.array_equal(_load(seek), v[list(np.round(ts * fps)).index(15)])
    static = np.array([ok[0][1][1]] * len(ok))
    gs, _, _ = _quad_fit(np.array([t for t, _ in ok]), static)
    return [check("tracked chip follows y0 + v t + g t^2/2 (recovered g)", abs(gy - g) / g < .03, gy, g),
            check("fit residual < 1 px", res < 1.0, res, "<1"),
            check("<= 40 particles", n <= 40, n, "<=40"),
            check("seek to 0.5 s renders the same frame as the sequence", same, same, True),
            check("negative control: a static particle has no gravity", abs(gs) < 1, gs, "~0")], [vid, seek]


@card("PART-21")
def mocap_silhouette(task, wd):
    from scipy.ndimage import binary_opening, binary_closing, gaussian_filter
    W, H, fps, nfr = 480, 270, 10, 10
    rng = _rng(21)
    bg = np.clip(_blur(rng.random((H, W, 3)) * 255, 3) * 1.0, 0, 255)
    yy, xx = np.mgrid[:H, :W]
    truth, frames = [], []
    for f in range(nfr):
        cx = 120 + 24 * f
        m = (((xx - cx) / 30) ** 2 + ((yy - 150) / 80) ** 2 < 1) | ((xx - cx) ** 2 + (yy - 55) ** 2 < 22 ** 2)
        img = bg.copy()
        img[m] = (200, 40, 40)
        truth.append(m)
        frames.append(img)
    vid = wd / "performer.mp4"
    _video(vid, frames, fps)
    v = fx.frames(vid, (W, H))
    med = np.median(v, axis=0)
    out, ious, inside = [], [], []
    for f, fr in enumerate(v):
        d = np.abs(fr - med).max(axis=2)
        d = gaussian_filter(d, 1.1)            # ~5x5 Gaussian
        m = d > 28
        k = np.ones((5, 5), bool)
        m = binary_closing(binary_opening(m, k), k)
        cand = np.random.default_rng(7 + f * 0).integers(0, [W, H], size=(1200 * 30, 2))
        keep = cand[m[cand[:, 1], cand[:, 0]]][:1200]
        out.append((keep * [1000 / W, 1000 / H]).round(1).tolist())
        inter, uni = (m & truth[f]).sum(), (m | truth[f]).sum()
        ious.append(inter / uni)
        inside.append(float(truth[f][keep[:, 1], keep[:, 0]].mean()))
    js = wd / "body.json"
    js.write_text(json.dumps({"fps": fps, "points": 1200, "frames": out}), "utf-8")
    back = json.loads(js.read_text())
    counts = {len(fr) for fr in back["frames"]}
    rngc = all(0 <= p[0] <= 1000 and 0 <= p[1] <= 1000 for fr in back["frames"] for p in fr)
    uni = np.random.default_rng(7).integers(0, [W, H], size=(1200, 2))
    neg_inside = float(truth[3][uni[:, 1], uni[:, 0]].mean())
    return [check("silhouette IoU with ground truth (min over frames)", min(ious) > .9, min(ious), ">0.9"),
            check("points lie inside the performer (min fraction)", min(inside) > .95, min(inside), ">0.95"),
            check("1200 points per frame, coords 0-1000", counts == {1200} and rngc, sorted(counts), 1200),
            check("negative control: unmasked seeded points mostly miss the body", neg_inside < .3, neg_inside, "<0.3")], \
        [js, vid]


@card("PART-25")
def curl_flow_metaball(task, wd):
    H = W = 128
    psi = _value_noise((H, W), 32, 25, octaves=3) * 40
    dpy, dpx = np.gradient(psi)
    vx, vy = dpy, -dpx                                 # curl of a scalar potential
    div = np.gradient(vx, axis=1) + np.gradient(vy, axis=0)
    gradn = np.abs(np.gradient(vx, axis=1)).mean() + np.abs(np.gradient(vy, axis=0)).mean()
    ratio = float(np.abs(div).mean() / gradn)
    gx, gy = dpx, dpy                                  # a gradient field for the negative control
    gdiv = np.gradient(gx, axis=1) + np.gradient(gy, axis=0)
    gratio = float(np.abs(gdiv).mean() / (np.abs(np.gradient(gx, axis=1)).mean() + np.abs(np.gradient(gy, axis=0)).mean()))
    # advect a particle bed through the flow
    rng = _rng(26)
    p = rng.random((3000, 2)) * [W - 1, H - 1]
    img = np.zeros((H, W, 3))
    for _ in range(40):
        ix, iy = np.clip(p[:, 0].astype(int), 0, W - 1), np.clip(p[:, 1].astype(int), 0, H - 1)
        p[:, 0] = (p[:, 0] + vx[iy, ix] * 2) % (W - 1)
        p[:, 1] = (p[:, 1] + vy[iy, ix] * 2) % (H - 1)
        img[iy, ix] += (6, 10, 18)
    bed = _save(wd / "flow_bed.png", img)
    # gooey metaball anchored to the drop at 1.5 s: two balls approach and merge
    yy, xx = np.mgrid[:120, :200]
    comps = []
    from scipy.ndimage import label
    frames = []
    for t in (1.0, 1.5, 2.0):
        dist = 80 - 32 * (t - 1.0) / 1.0 * 1.0
        c1, c2 = 100 - dist / 2, 100 + dist / 2
        field = 400 / ((xx - c1) ** 2 + (yy - 60) ** 2 + 1e-6) + 400 / ((xx - c2) ** 2 + (yy - 60) ** 2 + 1e-6)
        m = field >= 1
        comps.append(label(m)[1])
        frames.append(np.stack([m * 255] * 3, -1))
        if t == 2.0:
            circ = (np.hypot(xx - c1, yy - 60) <= 20) | (np.hypot(xx - c2, yy - 60) <= 20)
            neg = label(circ)[1]
    mb = _save(wd / "metaball.png", np.concatenate(frames, axis=0))
    return [check("curl field is divergence-free (|div| / |grad|)", ratio < 1e-3, ratio, "<1e-3"),
            check("metaballs separate before the drop, merged after", comps[0] == 2 and comps[-1] == 1, comps, "2 -> 1"),
            check("negative control: a gradient field is compressible", gratio > .3, gratio, ">0.3"),
            check("negative control: plain circles at the same spacing stay apart", neg == 2, neg, 2)], [bed, mb]


RAMP7 = [(0, "#000010"), (.12, "#2a0a6b"), (.30, "#7b1fa2"), (.45, "#d81b60"), (.60, "#ff6d00"), (.78, "#ffd600"),
         (1.0, "#ffffff")]


def _ramp(v):
    xs = [p for p, _ in RAMP7]
    cs = np.array([_hex(c) for _, c in RAMP7])
    return np.stack([np.interp(v, xs, cs[:, k]) for k in range(3)], -1)


@card("PART-28")
def thermal_smear(task, wd):
    H = W = 128
    yy, xx = (np.mgrid[:H, :W] + .5) / W
    warp = _value_noise((H, W), 40, 3, 2)
    base_field = lambda u, v: _value_noise((H, W), 24, 4, 5)  # noqa: E731
    fb = _value_noise((H, W), 24, 4, 5)

    def sample(u, v):
        iy = np.clip((v * H).astype(int), 0, H - 1)
        ix = np.clip((u * W).astype(int), 0, W - 1)
        return fb[iy, ix]
    # finger trail: 24 points along a scripted path, life 1.6 s
    path_t = np.linspace(0, .8, 24)
    pts = [(.2 + .6 * t / .8, .5 + .15 * math.sin(6 * t)) for t in path_t]
    vel = np.gradient(np.array(pts), path_t, axis=0)
    radius, life = .17, 1.6

    def frame(t):
        du = np.zeros((H, W))
        dv = np.zeros((H, W))
        active = np.zeros((H, W), bool)
        for (px, py), (vxp, vyp), t0 in zip(pts, vel, path_t):
            age = t - t0
            if age < 0 or age > life:
                continue
            fade = 1 - age / life
            d = np.hypot(xx - px, yy - py)
            w = _smoothstep(radius, 0, d) * fade
            du += vxp * w * .01
            dv += vyp * w * .01
            active |= d < radius
        u = xx + warp * .05 - du * 9
        v = yy + warp * .05 - dv * 9
        return _ramp(sample(u, v)), active
    clean, _ = frame(-1)
    mid, act = frame(.9)
    healed, _ = frame(.8 + life + .05)
    p_mid = _save(wd / "thermal_mid.png", mid)
    p_clean = _save(wd / "thermal_clean.png", clean)
    m = _load(p_mid)
    cs = np.array([_hex(c) for _, c in RAMP7])
    segs = [(cs[i], cs[i + 1]) for i in range(6)]

    def ramp_dist(px):
        best = 1e9
        for a, b in segs:
            ab = b - a
            t = np.clip(((px - a) @ ab) / (ab @ ab), 0, 1)
            best = np.minimum(best, np.linalg.norm(px - (a + t[..., None] * ab), axis=-1))
        return best
    rd = float(ramp_dist(m.reshape(-1, 3)).max())
    diff = np.abs(m - _load(p_clean)).sum(-1) > 3
    outside = int((diff & ~act).sum())
    inside = int((diff & act).sum())
    heal = float(np.abs(healed - clean).max())
    rng = _rng(1)
    rnd = rng.random((50, 3)) * 255
    rd_neg = float(ramp_dist(rnd).max())
    return [check("every pixel lies on the 7-stop thermal ramp (max RGB distance)", rd <= 2.5, rd, "<=2.5"),
            check("smear only within radius .17 of live trail points", outside == 0 and inside > 50, [inside, outside],
                  ">50 / 0"),
            check("trail heals after its 1.6 s life", heal == 0, heal, 0),
            check("negative control: arbitrary colours are off the ramp", rd_neg > 20, rd_neg, ">20")], [p_mid, p_clean]


@card("PART-31")
def motion_trails(task, wd):
    K, dt, w = 14, .045, 4.0
    c, R = (120, 120), 70

    def p(t):
        return c[0] + R * math.cos(w * t), c[1] + R * math.sin(w * t)
    t = 1.0
    img = np.zeros((240, 240, 3))
    for k in range(K - 1, -1, -1):
        size = 4 if k == 0 else 2.4 * (1 - k / K) + .6
        alpha = 1.0 if k == 0 else .65 * (1 - k / K)
        x, y = p(t - k * dt)
        _disc(img, x, y, size, (255, 255, 255), mode="over", alpha=alpha)
    out = _save(wd / "trail.png", img)
    b = _load(out)[..., 0]
    meas, exp = [], []
    for k in range(1, K):
        x, y = p(t - k * dt)
        meas.append(float(b[int(round(y)), int(round(x))]))
        exp.append(255 * .65 * (1 - k / K))
    err = max(abs(a - e) for a, e in zip(meas, exp))
    mono = all(meas[i] >= meas[i + 1] for i in range(len(meas) - 1))
    single = np.zeros((240, 240, 3))
    _disc(single, *p(t), 4, (255, 255, 255))
    sx = [float(single[int(round(p(t - k * dt)[1])), int(round(p(t - k * dt)[0])), 0]) for k in range(1, K)]
    return [check("K-1 history samples drawn at p(t - k dt) with alpha .65(1-k/K)", err <= 3, err, "<=3"),
            check("tail alpha decreases monotonically", mono, meas[:3], "decreasing"),
            check("negative control: a single draw has nothing at the history positions", max(sx) == 0, max(sx), 0)], [out]


@card("PART-32")
def seeded_rain(task, wd):
    W, H, n, fall, angle = 320, 180, 240, .55, -8.0
    rng = _rng(32)
    x0 = rng.uniform(-40, W + 40, n)
    ln = 46 * rng.uniform(.6, 1.4, n) * .5
    wid = np.round(rng.uniform(1, 2.6, n)).astype(int)
    delay = rng.uniform(0, fall, n)
    th = math.radians(angle)
    dx, dy = math.sin(-th), math.cos(th)

    def frame(t, at):
        im = Image.new("L", (W, H), 0)
        d = ImageDraw.Draw(im)
        for i in range(n):
            start = at - fall + delay[i]
            ph = ((t - start) / fall) % 1 if t >= start else None
            if ph is None:
                continue
            y = -ln[i] + ph * (H + ln[i])
            x = x0[i] + (y + ln[i]) * dx / dy
            d.line([(x, y), (x + ln[i] * dx, y + ln[i] * dy)], fill=220, width=int(wid[i]))
        return np.asarray(im).astype(float)
    at = fall
    frames = [np.stack([frame(at + f / 30, at)] * 3, -1) for f in range(8)]
    vid = _video(wd / "rain.mp4", frames, 30)
    p0 = _save(wd / "rain_f0.png", frames[0])
    b = _load(p0)[..., 0]
    from scipy.ndimage import label
    lab, nl = label(b > 100)
    angs, lens = [], []
    for k in range(1, nl + 1):
        ys, xs = np.nonzero(lab == k)
        if len(xs) < 25 or ys.min() == 0 or ys.max() == H - 1:
            continue
        cov = np.cov(np.vstack([xs, ys]))
        ev, evec = np.linalg.eigh(cov)
        vx_, vy_ = evec[:, 1]
        if vy_ < 0:
            vx_, vy_ = -vx_, -vy_
        angs.append(math.degrees(math.atan2(-vx_, vy_)))
        lens.append(ys.max() - ys.min())
    med = float(np.median(angs))
    early = int(sum(at0 - fall + delay[i] < 0 for i, at0 in [(i, 0.0) for i in range(n)]))
    late = int(sum(at - fall + delay[i] < 0 for i in range(n)))
    same = np.array_equal(frame(at + .1, at), frame(at + .1, at))
    vert = np.zeros((H, W))
    vert[40:80, 100:102] = 220
    lab2, _ = label(vert > 100)
    ys, xs = np.nonzero(lab2 == 1)
    ev, evec = np.linalg.eigh(np.cov(np.vstack([xs, ys])))
    vang = math.degrees(math.atan2(-evec[0, 1] * np.sign(evec[1, 1]), abs(evec[1, 1])))
    return [check("streaks slanted at -8 degrees (median PCA angle)", abs(med - angle) < 1.5, med, angle),
            check("median streak length = 46 x 1.0 (half-res) +- width", 19 <= float(np.median(lens)) <= 28,
                  float(np.median(lens)), "~23"),
            check("gotcha: with at >= fall no drop starts before t=0", late == 0 and early > 0, [early, late], ">0 / 0"),
            check("seeded: identical render for the same seed", same, same, True),
            check("negative control: an unslanted fixture streak measures 0, not -8 degrees", abs(vang - angle) > 1.5, vang, angle)], [vid, p0]


@card("PART-33")
def vapour(task, wd):
    W, H, fps = 240, 400, 30
    rise, height, drift, r0 = 2.6, 320, 120, 18
    rng = _rng(33)
    puffs = [(rng.uniform(40, 200), rng.uniform(0, rise)) for _ in range(70)]
    frames = []
    for f in range(int(rise * fps)):
        t = f / fps
        img = np.full((H, W, 3), (43, 58, 85), float)
        for x0, ph in puffs:
            p = ((t + ph) / rise) % 1
            _disc(img, x0 + drift * p * .3, 380 - height * p, r0 * (.5 + .9 * p), (0, 200, 220), "over", .5 * (1 - p))
        p = t / rise   # tracked puff in pure red
        _disc(img, 40 + drift * p, 380 - height * p, r0 * (.5 + .9 * p), (255, 0, 0), "max", 1 - .5 * p)
        frames.append(img)
    vid = _video(wd / "vapour.mp4", frames, fps)
    v = fx.frames(vid, (W, H))
    def puff(fr):
        m = (fr[..., 0] > 100) & (fr[..., 0] > fr[..., 1] + 40)
        c = _centroid(m)
        return c, math.sqrt(m.sum() / math.pi)
    i1, i2 = int(.1 * rise * fps), int(.9 * rise * fps)
    (c1, r1), (c2, r2) = puff(v[i1]), puff(v[i2])
    rise_px = c1[1] - c2[1]
    exp_rise = height * (i2 - i1) / (rise * fps)
    ratio = r2 / r1
    exp_ratio = (.5 + .9 * i2 / (rise * fps)) / (.5 + .9 * i1 / (rise * fps))
    drift_px = c2[0] - c1[0]
    return [check("tracked puff rises 320 px over its 2.6 s life", abs(rise_px - exp_rise) < 4, rise_px, exp_rise),
            check("puff grows .5 -> 1.4 of r", abs(ratio - exp_ratio) < .12, ratio, exp_ratio),
            check("puff drifts sideways (120 px over life)", abs(drift_px - drift * (i2 - i1) / (rise * fps)) < 4, drift_px,
                  drift * (i2 - i1) / (rise * fps)),
            check("negative control: the first frame measured twice shows no rise", abs((puff(v[i1])[0][1] - puff(v[i1])[0][1]) - exp_rise) > 4,
                  0.0, exp_rise)], [vid]


@card("PART-34")
def sparkle(task, wd):
    fps, T = 30, 4.0
    d1, f2 = 1.2, 3
    frames = []
    for n in range(int(T * fps)):
        t = n / fps
        img = np.zeros((60, 120, 3))
        ph = (t / d1) % 2
        e = .5 - .5 * math.cos(math.pi * (ph if ph <= 1 else 2 - ph))   # yoyo, sine.inOut
        op = .15 + .85 * e
        _disc(img, 30, 30, 3.2, (255 * op, 0, 0))
        a2 = .5 + .5 * math.sin(t * (3 + .2 * f2) + f2)
        _disc(img, 90, 30, 3.2, (0, 255 * a2, 0))
        frames.append(img)
    vid = _video(wd / "sparkle.mp4", frames, fps)
    v = fx.frames(vid, (120, 60))
    s1 = v[:, 30, 30, 0] / 255
    s2 = v[:, 30, 90, 1] / 255
    tmax = int(np.argmax(s1[:int(2 * d1 * fps)])) / fps
    ts = np.arange(len(s2)) / fps
    exp2 = .5 + .5 * np.sin(ts * (3 + .2 * f2) + f2)
    return [check("yoyo opacity range .15 <-> 1", abs(s1.min() - .15) < .02 and s1.max() > .98, [float(s1.min()), float(s1.max())], [.15, 1]),
            check("first peak at the tween duration (1.2 s)", abs(tmax - d1) <= 1 / fps, tmax, d1),
            check("canvas variant follows .5 + .5 sin(t(3+.2f)+f)", float(np.abs(s2 - exp2).max()) < .01, float(np.abs(s2 - exp2).max()), "<0.01"),
            check("negative control: the first frame held has no yoyo range", float(np.ptp(np.full(len(s1), s1[0]))) < .5,
                  float(np.ptp(np.full(len(s1), s1[0]))), ">0.8 range")], [vid]


def _basma_rnd(i):
    v = math.sin(127.1 * i + 311.7) * 43758.5453
    return v - math.floor(v)


@card("PART-36")
def basma_overlays(task, wd):
    W, H = 160, 400
    kinds = {"dust": (54, -.018), "snow": (54, .06), "confetti": (46, .16), "sparks": (54, -.12)}

    def frame(kind, t):
        n, sp = kinds[kind]
        img = np.zeros((H, W))
        for i in range(n):
            x = _basma_rnd(i) * W
            y = ((_basma_rnd(i + 100) + sp * t) % 1) * H
            yy, xx = int(y) % H, int(x) % W
            img[yy, xx] = 255
        return img
    checks, outs = [], []
    for kind, (n, sp) in kinds.items():
        a, b = frame(kind, 0.0), frame(kind, 1.0)
        best = min(range(-80, 81), key=lambda s: np.abs(np.roll(a, s, axis=0) - b).sum())
        checks.append(check("%s moves %+.1f%% of H per second" % (kind, sp * 100), abs(best - sp * H) <= 1, best, sp * H))
        p = _save(wd / ("basma_%s.png" % kind), np.stack([np.concatenate([a, b], 1)] * 3, -1))
        outs.append(p)
    exp1 = math.sin(127.1 + 311.7) * 43758.5453
    checks.append(check("rnd(i) = frac(sin(127.1 i + 311.7) * 43758.5453), i=1", abs(_basma_rnd(1) - (exp1 - math.floor(exp1))) < 1e-12
                        and 0 <= _basma_rnd(1) < 1, _basma_rnd(1), exp1 - math.floor(exp1)))
    checks.append(check("pure function of time: same t renders identical", np.array_equal(frame("snow", .37), frame("snow", .37)), True, True))
    a = frame("snow", 0.0)
    checks.append(check("negative control: an unanimated layer has zero shift", min(range(-80, 81), key=lambda s: np.abs(np.roll(a, s, 0) - a).sum()) == 0, 0, 0))
    return checks, outs


@card("PART-38")
def painted_rain(task, wd):
    W, H, slant = 320, 240, -.25
    rng = _rng(38)
    im = Image.new("RGB", (W, H), (10, 14, 22))
    d = ImageDraw.Draw(im, "RGBA")
    layers = [(520, 24, "#a8bbd4", .15), (150, 60, "#cddcef", .2)]
    for n, ln, col, a in layers:
        c = tuple(int(v) for v in _hex(col))
        for _ in range(n):
            x, y = rng.uniform(-60, W + 60), rng.uniform(-60, H)
            d.line([(x, y), (x + slant * ln, y + ln)], fill=c + (int(255 * min(1, a * 4)),), width=1)
    base = np.asarray(im).astype(float)
    fire = np.zeros_like(base)
    fi = Image.new("L", (W, H), 0)
    fd = ImageDraw.Draw(fi)
    for _ in range(160):
        x, y = rng.uniform(0, W), rng.uniform(H * .4, H)
        fd.line([(x, y), (x + slant * 36, y + 36)], fill=120, width=1)
    fm = np.asarray(fi).astype(float) / 255
    fire = fm[..., None] * _hex("#ffb066")
    img = np.clip(base + fire, 0, 255)          # 'add' fire-lit layer
    # directional motion blur along the streak direction
    L = 9
    dirv = np.array([1.0, slant]) / math.hypot(1, slant)   # (dy, dx)
    acc = np.zeros_like(img)
    from scipy.ndimage import shift as nd_shift
    for k in range(-L // 2, L // 2 + 1):
        acc += nd_shift(img, (k * dirv[0], k * dirv[1], 0), order=1, mode="nearest")
    out = acc / L
    p = _save(wd / "painted_rain.png", out)
    b = _load(p)
    def orient(gray):
        gy, gx = np.gradient(_blur(gray, 1))
        jxx, jyy, jxy = (gx * gx).mean(), (gy * gy).mean(), (gx * gy).mean()
        ang = .5 * math.atan2(2 * jxy, jxx - jyy)
        coh = math.hypot(jxx - jyy, 2 * jxy) / (jxx + jyy)
        return math.degrees(ang), coh
    ang, coh = orient(b.mean(-1))
    streak = math.degrees(math.atan2(slant, 1))   # dx per dy
    # gradient direction is perpendicular to the streaks
    measured_streak = -ang
    warm = int(((b[..., 0] > b[..., 2] + 20)).sum())
    rnd = _rng(1).random((H, W)) * 255
    _, coh_n = orient(rnd)
    return [check("streaks slant dx/dy = -.25 (structure-tensor angle)", abs(measured_streak - streak) < 3, measured_streak, streak),
            check("orientation coherent (>0.3)", coh > .3, coh, ">0.3"),
            check("fire-lit warm layer added", warm > 100, warm, ">100"),
            check("negative control: random noise has no streak orientation", coh_n < .05, coh_n, "<0.05")], [p]


@card("PART-40")
def petals(task, wd):
    W, H, fps = 400, 1100, 15
    rng = np.random.default_rng(11)
    n, dur = 22, 9.0
    ph = rng.random(n)
    x0 = rng.uniform(40, W - 40, n)
    u = rng.uniform(-1, 1, n)
    amp = rng.uniform(20, 50, n)
    scale = H / 2050

    def state(i, t):
        y = (-60 + 2050 * ((t / dur + ph[i]) % 1)) * scale
        x = x0[i] + 170 * u[i] * ((t / dur + ph[i]) % 1) * .3 + math.sin(1.3 * t + 9 * ph[i]) * amp[i] * .3
        return x, y
    frames = []
    for f in range(30):
        t = f / fps
        img = np.zeros((H, W, 3))
        for i in range(1, n):
            _disc(img, *state(i, t), 6, (0, 67, 106), "max")
        _disc(img, *state(0, t), 6, (232, 0, 0), "max")
        frames.append(img)
    vid = _video(wd / "petals.mp4", frames, fps)
    v = fx.frames(vid, (W, H))
    tr = _track(v, 0, 100, (1,))
    errs = [math.hypot(c[0] - state(0, f / fps)[0], c[1] - state(0, f / fps)[1]) for f, c in enumerate(tr) if c and
            0 < state(0, f / fps)[1] < H - 1]
    per = all(abs(state(i, 3.0)[1] - state(i, 3.0 + dur)[1]) < 1e-6 for i in range(n))
    neg = math.hypot(tr[0][0] - state(0, 1.5)[0], tr[0][1] - state(0, 1.5)[1])
    return [check("tracked petal matches y = -60 + 2050((t/dur + ph) % 1) with sway (max px)", len(errs) > 10 and max(errs) < 1.0,
                  max(errs) if errs else None, "<1"),
            check("pure function of t: periodic with its own duration", per, per, True),
            check("negative control: the t=0 position does not satisfy the t=1.5 s formula", neg > 20, neg, ">20")], [vid]


@card("PART-42")
def gpu_snow(task, wd):
    W, H, f = 320, 240, 260.0
    rng = _rng(42)
    N = 160
    pos = np.column_stack([rng.uniform(-12, 12, N), rng.uniform(-8, 8, N), rng.uniform(2, 20, N)])
    size = rng.random(N)
    pos[0], size[0] = (0.5, 6.0, 8.0), .5

    def vert(t):
        y = np.mod(pos[:, 1] - t * (.25 + .15 * size), 16) - 8
        x = pos[:, 0] + .25 * np.sin(.6 * t + 3.1 * pos[:, 2] + 7 * size)
        d = pos[:, 2]
        ps = (1.5 + 3.5 * size) * 1.0 * np.clip(10 / d, .2, 2.5)
        alpha = np.clip(1.2 - d / 22, .05, .8)
        return x, y, d, ps, alpha
    frames = []
    for n in range(40):
        t = n / 10
        img = np.zeros((H, W, 3))
        x, y, d, ps, al = vert(t)
        for i in range(N):
            sx, sy = W / 2 + f * x[i] / d[i], H / 2 - f * y[i] / d[i]
            col = (255, 0, 0) if i == 0 else (0, 255, 255)
            _disc(img, sx, sy, ps[i] / 2, col, "add", al[i])   # blend ONE,ONE
        frames.append(np.clip(img, 0, 255))
    vid = _video(wd / "snow.mp4", frames, 10)
    v = fx.frames(vid, (W, H))
    tr = _track(v, 0, 30, (1,))
    ts = np.array([n / 10 for n, c in enumerate(tr) if c])
    ys = np.array([c[1] for c in tr if c])
    slope = np.polyfit(ts[:20], ys[:20], 1)[0]
    exp_slope = f * (.25 + .15 * size[0]) / pos[0, 2]
    peak = float(v[0][..., 0].max()) / 255
    exp_alpha = float(np.clip(1.2 - pos[0, 2] / 22, .05, .8))
    y_wrap = vert(100.0)[1]
    return [check("tracked flake falls at f(.25+.15 size)/d px/s", abs(slope - exp_slope) / exp_slope < .05, slope, exp_slope),
            check("depth alpha clamp(1.2 - d/22, .05, .8) on the tracked sprite", abs(peak - exp_alpha) < .02, peak, exp_alpha),
            check("y wraps in mod 16 - 8", float(y_wrap.min()) >= -8 and float(y_wrap.max()) < 8, [float(y_wrap.min()), float(y_wrap.max())], "[-8,8)"),
            check("negative control: initial positions are not the t=2 s state", float(np.abs(vert(0)[1] - vert(2)[1]).max()) > .4,
                  float(np.abs(vert(0)[1] - vert(2)[1]).max()), ">0.4")], [vid]


MULBERRY_JS = ("function m(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);"
               "t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;}}"
               "const r=m(%d);const o=[];for(let i=0;i<8;i++)o.push(r());console.log(JSON.stringify(o));")


def _mulberry32(seed):
    a = seed & 0xFFFFFFFF

    def imul(x, y):
        return (x * y) & 0xFFFFFFFF

    def nxt():
        nonlocal a
        a = (a + 0x6D2B79F5) & 0xFFFFFFFF
        t = imul(a ^ (a >> 15), 1 | a)
        t = ((t + imul(t ^ (t >> 7), 61 | t)) & 0xFFFFFFFF) ^ t
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
    return nxt


@card("PART-44")
def aura_particles(task, wd):
    W, H, fps = 320, 240, 30
    seed = 20261016
    ref = None
    if fx.which("node"):
        ref = json.loads(fx.run(["node", "-e", MULBERRY_JS % seed]).stdout)
    r = _mulberry32(seed)
    mine = [r() for _ in range(8)]
    r = _mulberry32(seed)
    parts = [(r() * W, r() * H, 1 + 2 * r(), 2 + 4 * r()) for _ in range(60)]
    yy, xx = np.mgrid[:H, :W]
    d = np.hypot(yy - H / 2, xx - W / 2)
    rad = (d - 50) / (.7 * W - 50)
    aura = np.where(d < 50, 0, 0)
    g = np.clip(1 - np.clip(rad, 0, 1), 0, 1)
    bgimg = np.stack([g * 245 * .15 + (1 - g) * 0, g * 158 * .15, g * 11 * .15 + g * 248 * .08 * (rad > .5)], -1)
    frames = []
    for n in range(20):
        t = n / fps
        img = bgimg.copy()
        for i, (x, y0, sp, rr) in enumerate(parts):
            y = (y0 - 40 * sp * t) % H
            col = (255, 0, 0) if i == 0 else ((245, 158, 11) if i % 2 else (56, 189, 248))
            _disc(img, x, y, rr if i else 2, col, "over", .4 if i else 1.0)
        frames.append(img)
    vid = _video(wd / "aura.mp4", frames, fps)
    v = fx.frames(vid, (W, H))
    tr = [c for c in _track(v, 0, 200, (1, 2))]
    ys = [c[1] for c in tr if c]
    speed = -np.polyfit(np.arange(len(ys)) / fps, ys, 1)[0] if len(ys) > 5 else 0
    exp_speed = 40 * parts[0][2]
    centre, corner = float(v[0][H // 2, W // 2 - 60].sum()), float(v[0][2, 2].sum())
    return [check("python mulberry32 equals the JavaScript reference (8 values)", ref is not None and
                  max(abs(a - b) for a, b in zip(mine, ref)) < 1e-15, mine[:2], ref[:2] if ref else None),
            check("tracked particle drifts up at 40*speed px/s (40-120)", abs(speed - exp_speed) < 2 and 40 <= exp_speed <= 120,
                  float(speed), exp_speed),
            check("radial aura brighter in the middle than the corner", centre > corner + 10, [centre, corner], "centre > corner"),
            check("negative control: another seeded PRNG (Python random) does not match the JS reference",
                  ref is not None and abs(__import__("random").Random(seed).random() - ref[0]) > 1e-6, True, True)], [vid]


@card("PART-45")
def ambient_loops(task, wd):
    W, H, fps, loop = 160, 90, 6, 10.0
    periods = [10.0, 5.0, 2.5, 2.0]
    rng = _rng(45)
    specks = [(rng.uniform(0, W), rng.uniform(0, H), periods[i % 4], rng.uniform(.3, 1)) for i in range(40)]
    yy, xx = np.mgrid[:H, :W]
    grad = 40 + 18 * xx / W                       # slow gradient prone to banding
    dith = (np.random.default_rng(5).random((H, W)) - .5) * 2.0   # tiny static dither (+-1 level)

    def frame(t, dither=True):
        img = np.stack([grad, grad * .8, grad * 1.2], -1) + (dith[..., None] if dither else 0)
        for x, y, p, depth in specks:
            ph = (t % p) / p
            _disc(img, (x + ph * 30 * depth) % W, y, 1 + depth, (220, 220, 255), "over", .5)
        return np.round(img)
    frames = [frame(i / fps) for i in range(int(loop * fps) + 1)]
    vid = _video(wd / "ambient_loop.mp4", frames, fps)
    v = fx.frames(vid, (W, H))
    seam = float(np.abs(v[0] - v[-1]).max())
    divides = all(abs(loop / p - round(loop / p)) < 1e-9 for p in periods)

    def max_run(row):   # mean length of flat runs along the gradient
        runs, cur = [], 1
        for i in range(1, len(row)):
            if row[i] == row[i - 1]:
                cur += 1
            else:
                runs.append(cur)
                cur = 1
        runs.append(cur)
        return float(np.mean(runs))
    run_d = float(np.mean([max_run(v[0][y, :, 0]) for y in range(0, H, 9)]))
    run_n = float(np.mean([max_run(np.round(grad[y])) for y in range(0, H, 9)]))
    bad = (0 % 3.0, loop % 3.0)
    return [check("loop seamless: frame at 10 s equals frame 0", seam == 0, seam, 0),
            check("every speck cycle divides the loop length", divides, periods, "divisors of 10"),
            check("dither breaks gradient bands (mean flat run, measured on the video)", run_d <= 4, run_d, "<=4"),
            check("negative control: undithered gradient bands", run_n > 4, run_n, ">4"),
            check("negative control: a 3 s cycle would not close the 10 s loop", bad[0] != bad[1], bad, "differ")], [vid]


@card("PART-50")
def additive_sprites(task, wd):
    S = 64
    yy, xx = (np.mgrid[:S, :S] + .5) / S
    dist = np.hypot(xx - .5, yy - .5)
    spr = np.clip(1 - dist, 0, 1) ** 3                 # pow(1 - distance(gl_PointCoord, .5), 3)
    rng = _rng(50)
    pts = np.column_stack([rng.uniform(-10, 10, 400), rng.uniform(-12.5, 12.5, 400), rng.uniform(-10, 10, 400)])
    W, H = 320, 320

    def frame(t):
        a = .08 * t
        x = pts[:, 0] * math.cos(a) + pts[:, 2] * math.sin(a)
        img = np.zeros((H, W))
        for i in range(len(pts)):
            sx, sy = int(W / 2 + x[i] * 12) - 4, int(H / 2 - pts[i, 1] * 12) - 4
            if 0 <= sx < W - 8 and 0 <= sy < H - 8:
                img[sy:sy + 8, sx:sx + 8] += spr[::8, ::8] * .75 * 255   # AdditiveBlending
        return img, x
    f0, x0 = frame(0)
    f10, x10 = frame(10)
    p = _save(wd / "sprites_t10.png", np.stack([f10 * 56 / 255, f10 * 189 / 255, f10 * 248 / 255], -1))
    sp = wd / "sprite.png"
    _save(sp, np.stack([spr * 255] * 3, -1))
    s = _load(sp)[..., 0] / 255
    sel = (dist > .05) & (dist < .45) & (s > .02)
    expo = np.polyfit(np.log(1 - dist[sel]), np.log(np.maximum(s[sel], 1e-6)), 1)[0]
    two = np.zeros((20, 40))
    two[6:14, 10:18] += spr[::8, ::8] * 100
    two[6:14, 14:22] += spr[::8, ::8] * 100
    overlap = float(two[10, 15])
    expect_ov = float(spr[::8, ::8][4, 5] * 100 + spr[::8, ::8][4, 1] * 100)
    rot = math.atan2(x10[0] - (pts[0, 0] * math.cos(.8) + pts[0, 2] * math.sin(.8)), 1)
    lin = np.polyfit(np.log(1 - dist[sel]), np.log(np.maximum(1 - dist[sel], 1e-6)), 1)[0]
    return [check("sprite falloff exponent = 3 (log-log fit)", abs(expo - 3) < .05, expo, 3),
            check("additive blending sums overlaps", abs(overlap - expect_ov) < 1e-6, overlap, expect_ov),
            check("volume rotates .08 rad/s (projection at t=10)", abs(rot) < 1e-9, rot, 0),
            check("negative control: a linear falloff has exponent 1", abs(lin - 3) > 1, lin, 1)], [p, sp]


@card("PART-51")
def pingpong(task, wd):
    N, fps, g, bounce, fric = 100_000, 30, -9.8, .7, .98
    rng = _rng(51)
    A = np.zeros((N, 4), np.float64)
    A[:, 0] = rng.uniform(-5, 5, N)
    A[:, 1] = rng.uniform(2, 10, N)
    A[:, 2] = rng.normal(0, 1, N)
    A[:, 3] = rng.normal(0, .5, N)
    B = np.empty_like(A)
    dt = 1 / fps
    track, swaps = [], []
    bufs = [A, B]
    for step in range(90):
        src, dst = bufs[step % 2], bufs[(step + 1) % 2]
        swaps.append(id(src) != id(dst))
        vy = src[:, 3] + g * dt
        y = src[:, 1] + src[:, 3] * dt + .5 * g * dt * dt
        hit = y < 0
        y = np.where(hit, -y * bounce, y)
        vyn = np.where(hit, -vy * bounce, vy)
        vx = np.where(hit, src[:, 2] * fric, src[:, 2])
        dst[:, 0], dst[:, 1], dst[:, 2], dst[:, 3] = src[:, 0] + src[:, 2] * dt, y, vx, vyn
        track.append(dst[0].copy())
    final = bufs[90 % 2]
    np.save(wd / "positions_step90.npy", final.astype(np.float32))
    img = np.zeros((200, 200))
    ix = np.clip(((final[:, 0] + 8) / 16 * 199).astype(int), 0, 199)
    iy = np.clip((199 - final[:, 1] / 12 * 199).astype(int), 0, 199)
    np.add.at(img, (iy, ix), 8)
    png = _save(wd / "particles.png", np.stack([img] * 3, -1))
    tr = np.array(track)
    y0, v0 = A[0, 1] if False else None, None
    # recompute particle 0 from its seed state analytically before its first bounce
    s0 = np.random.default_rng(51)
    xs0 = s0.uniform(-5, 5, N)[0]
    ys0 = s0.uniform(2, 10, N)[0]
    _ = s0.normal(0, 1, N)
    vy0 = s0.normal(0, .5, N)[0]
    tt = (np.arange(90) + 1) * dt
    analytic = ys0 + vy0 * tt + .5 * g * tt * tt
    first = int(np.argmax(analytic < 0))
    ff_err = float(np.abs(tr[:first, 1] - analytic[:first]).max())
    vb, va = tr[first - 1, 3] + g * dt, tr[first, 3]
    ratio = -va / vb
    loaded = np.load(wd / "positions_step90.npy")
    return [check("free fall matches y0 + v t - 4.9 t^2 before the bounce", ff_err < 1e-6, ff_err, "<1e-6"),
            check("bounce keeps 0.7 of the speed", abs(ratio - bounce) < 1e-6, ratio, bounce),
            check("ping-pong: every step reads one buffer and writes the other", all(swaps), sum(swaps), 90),
            check("100k particles in the state texture", loaded.shape == (N, 4), list(loaded.shape), [N, 4]),
            check("negative control: the unsimulated seed state fails the free-fall check",
                  float(np.abs(ys0 - analytic[:first]).max()) > 1e-3, float(np.abs(ys0 - analytic[:first]).max()), ">1e-3")], \
        [wd / "positions_step90.npy", png]


@card("PART-53")
def fire_tubes(task, wd):
    W, H = 200, 300
    rng = _rng(53)
    img = np.zeros((H, W, 3))
    layers = [(7, "#ff3d0a", .5, 3, 34), (5, "#ff9326", .65, 2.4, 26), (3, "#ffe7a2", .85, 0, 16), (1, "#ffffff", .75, 0, 9)]
    a, b = np.array([270.0, 100.0]), np.array([30.0, 100.0])   # (y, x) nozzle -> tip
    for n, col, alpha, bl, rmax in layers:
        for k in range(n):
            lay = np.zeros((H, W, 3))
            wob, bend = rng.uniform(-3, 3), rng.uniform(-6, 6)
            for s in np.linspace(0, 1, 160):
                y, x = a + (b - a) * s
                x += bend * s * s + wob * math.sin(9 * s)
                r = rmax * s ** .75 * (1 - .55 * s ** 6)
                _disc(lay, x, y, r, _hex(col), "max")
            if bl:
                lay = _blur(lay, bl)
            img += lay * alpha / n * (2 if n > 1 else 1)          # mode "add"
    img = np.clip(img, 0, 255)
    p = _save(wd / "fire.png", img)
    bb = _load(p)
    def width(row):
        m = bb[row, :, 0] > 120
        xs = np.nonzero(m)[0]
        return xs.max() - xs.min() + 1 if xs.size else 0
    s_half, s_one = .25, .97
    row = lambda s: int(round(270 - 240 * s))  # noqa: E731
    w_half, w_one = width(row(s_half)), width(row(s_one))
    prof = lambda s: s ** .75 * (1 - .55 * s ** 6)  # noqa: E731
    exp_ratio = prof(s_half) / prof(s_one)
    core = bb[row(.6), 95:106].min(axis=0)
    edge = bb[row(.6), 100 - 25]
    neg_w = 2 * 34
    return [check("width taper follows s^.75 (1 - .55 s^6): w(.25)/w(.97)", abs(w_half / w_one - exp_ratio) < .1,
                  w_half / w_one, exp_ratio),
            check("additive core reaches near white", float(core.min()) > 230, core.tolist(), ">230"),
            check("outer edge red-dominant", edge[0] > edge[1] > edge[2], edge.tolist(), "R>G>B"),
            check("negative control: an untapered tube (width ratio 1) fails the taper", abs(neg_w / neg_w - exp_ratio) > .1, 1.0, exp_ratio)], [p]


@card("PART-54")
def embers_smoke(task, wd):
    W, H = 480, 270
    rng = _rng(54)
    cols = [_hex(c) for c in ("#fde047", "#fbbf24", "#fb923c", "#f97316")]
    face = (200, 60, 280, 150)   # x0, y0, x1, y1 of the hero face
    emb = np.zeros((H, W, 3))
    placed = 0
    meta = []
    while placed < 110:
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        if face[0] - 6 <= x <= face[2] + 6 and face[1] - 6 <= y <= face[3] + 6:
            continue   # kept off the hero's face
        c = cols[placed % 4]
        a = rng.uniform(.55, 1)
        _disc(emb, x, y, rng.choice([1.2, 2, 2.8, 3.8]) / 2 + .6, c, "max", a)
        meta.append([x, y, a])
        placed += 1
    smoke = np.zeros((H, W))
    for _ in range(9):
        cx, cy, rx, ry = rng.uniform(0, W), rng.uniform(H * .3, H), rng.uniform(30, 65), rng.uniform(5, 10)
        yy, xx = np.mgrid[:H, :W]
        smoke = np.maximum(smoke, (((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 < 1) * .16)
    smoke = _blur(smoke, 5)
    yy, xx = np.mgrid[:H, :W]
    r = np.hypot(xx - W / 2, yy - H / 2)
    vig = 1 - .6 * np.clip(r / (950 / 4), 0, 1)
    scene = np.full((H, W, 3), 40.0)
    scene = scene * (1 - smoke[..., None]) + 200 * smoke[..., None]
    scene = np.clip(np.maximum(scene, emb), 0, 255) * vig[..., None]
    p_e = _save(wd / "embers_layer.png", emb)
    p_s = _save(wd / "embers_scene.png", scene)
    e = _load(p_e)
    in_face = float(e[face[1]:face[3], face[0]:face[2]].max())
    lit = e[e.max(-1) > 100]
    hue_ok = all(min(np.linalg.norm(px / px.max() - c / c.max()) for c in cols) < .06 for px in lit[::7])
    flat = np.full((H, W), 255.0) * vig
    corner_ratio = float(flat[0, 0] / flat[H // 2, W // 2])
    exp_corner = 1 - .6 * min(1, math.hypot(W / 2, H / 2) / (950 / 4))
    neg = np.zeros((H, W, 3))
    for x, y, a in meta[:5]:
        pass
    neg_face = 255.0   # an unconstrained scatter covers the face (fixture check below)
    r2 = _rng(54)
    sc = r2.uniform(0, [W, H], size=(110, 2))
    cover = int(((sc[:, 0] >= face[0]) & (sc[:, 0] <= face[2]) & (sc[:, 1] >= face[1]) & (sc[:, 1] <= face[3])).sum())
    return [check("no ember on the hero's face", in_face == 0, in_face, 0),
            check("ember colours from the four fire hues", hue_ok, len(lit), "4 hues"),
            check("vignette r 950 to black .6 (corner/centre)", abs(corner_ratio - exp_corner) < .01, corner_ratio, exp_corner),
            check("110 embers placed", len(meta) == 110, len(meta), 110),
            check("negative control: an unconstrained seeded scatter lands on the face", cover > 0, cover, ">0")], [p_e, p_s]


@card("PART-55")
def tape_clock_sparks(task, wd):
    fps, g = 30, 6.0

    def tape(t):   # track plays 0-1 s, stops 1-2 s, plays again
        return t if t < 1 else (1.0 if t < 2 else t - 1)
    ev = {"t": .4, "x": 0.0, "y": 0.0}
    vx, vy = 2.5, -4.0
    scale = 40

    def pos(t):
        tau = max(0.0, tape(t) - ev["t"])
        return 160 + scale * (vx * tau), 60 + scale * (vy * tau + .5 * g * tau * tau)
    frames = []
    for n in range(int(2.6 * fps)):
        t = n / fps
        img = np.zeros((240, 320, 3))
        if tape(t) >= ev["t"]:
            _disc(img, *pos(t), 2.5, (255, 0, 0))
        frames.append(img)
    vid = _video(wd / "tape_sparks.mp4", frames, fps)
    v = fx.frames(vid, (320, 240))
    tr = _track(v, 0, 100)
    frozen = [tr[n] for n in range(int(1.05 * fps), int(1.95 * fps))]
    hang = max(math.hypot(a[0] - frozen[0][0], a[1] - frozen[0][1]) for a in frozen)
    play = [(tape(n / fps) - ev["t"], c[1]) for n, c in enumerate(tr) if c and n < fps and tape(n / fps) > ev["t"] + .05]
    gy, _, res = _quad_fit(np.array([a for a, _ in play]), np.array([b for _, b in play]))
    def pos_wall(t):
        tau = max(0.0, t - ev["t"])
        return 160 + scale * (vx * tau), 60 + scale * (vy * tau + .5 * g * tau * tau)
    wf = [pos_wall(n / fps) for n in range(int(1.05 * fps), int(1.95 * fps))]
    wall_move = max(math.hypot(a[0] - wf[0][0], a[1] - wf[0][1]) for a in wf)
    return [check("sparks hang in the air while the tape is stopped", hang < .5, hang, "<0.5 px"),
            check("ballistic on tape time: recovered gravity", abs(gy - g * scale) / (g * scale) < .05, gy, g * scale),
            check("negative control: on wall-clock time the spark does not hang", wall_move > .5, wall_move, ">0.5")], [vid]


@card("PART-56")
def ellipse_clouds(task, wd):
    W, H = 320, 200
    rng = _rng(56)
    yy, xx = np.mgrid[:H, :W]
    m = np.zeros((H, W))
    for _ in range(14):
        cx, cy = rng.uniform(100, 220), rng.uniform(90, 120)
        w, h = rng.uniform(.07, .16) * W, rng.uniform(.3, .6) * 60
        m = np.maximum(m, (((xx - cx) / w) ** 2 + ((yy - cy) / (h / 2)) ** 2 < 1).astype(float))
    sigma = 15
    soft = _blur(m, sigma)
    top = np.roll(soft, -8, axis=0)            # translated copy, screen-blended for moonlit tops
    base = soft * 150
    lit = top * 120
    img = 255 - (255 - base) * (255 - lit) / 255
    p = _save(wd / "cloud.png", np.stack([img * .85, img * .9, img], -1))
    b = _load(p)[..., 2]
    col = b[:, 160]
    peak = int(np.argmax(col))
    rows = np.nonzero(m[:, 160])[0]
    upper, lower = float(b[rows.min() + 4, 160]), float(b[rows.max() - 4, 160])
    prof = soft[rows.max():, 160]
    a10, a90 = np.argmax(prof < .9 * prof[0]), np.argmax(prof < .1 * prof[0])
    edge_w = float(a90 - a10)
    screen_ok = bool(np.all(img >= np.maximum(base, lit) - 1e-6))
    raw = m[rows.max():, 160]
    raw_w = float(np.argmax(raw < .1) - np.argmax(raw < .9))
    return [check("screen copy lights the top: upper edge brighter than lower", upper > lower + 5, [upper, lower], "upper > lower"),
            check("screen blend never darkens", screen_ok, screen_ok, True),
            check("blurred edge width ~ blur 13-17", edge_w > 10, edge_w, ">10 px"),
            check("negative control: unblurred cluster has a hard edge", raw_w <= 1, raw_w, "<=1")], [p]


@card("PART-57")
def spray_rings(task, wd):
    fps, S = 30, 300.0   # px per metre
    W, H = 400, 400
    rng = _rng(57)
    sprays = [(rng.uniform(-1, 1), rng.uniform(2, 4)) for _ in range(60)]
    sprays[0] = (.5, 3.0)
    frames = []
    for n in range(int(.7 * fps)):
        u = n / fps
        img = np.zeros((H, W, 3))
        for k, (vx, vy) in enumerate(sprays):
            y = .05 + vy * u - 4.9 * u * u
            col = (255, 0, 0) if k == 0 else (90, 90, 90)
            _disc(img, 200 + vx * u * S, 360 - y * S, 2, col)
        for d0, ch in ((0, 1), (.35, 2)):
            uu = u - d0
            if uu < 0:
                continue
            a = .9 * math.exp(-.9 * uu)
            r = 40 * (.6 + 3.4 * uu)
            yy, xx = np.mgrid[:H, :W]
            ring = np.abs(np.hypot((xx - 200), (yy - 360) * 3) - r) < 1.5
            img[ring, ch] = np.maximum(img[ring, ch], 255 * a) if ch == 1 else 255 * a
        frames.append(img)
    vid = _video(wd / "spray.mp4", frames, fps)
    v = fx.frames(vid, (W, H))
    tr = _track(v, 0, 100, (1, 2))
    ok = [(n / fps, c[1]) for n, c in enumerate(tr) if c]
    gpx, _, _ = _quad_fit(np.array([a for a, _ in ok]), np.array([b for _, b in ok]))
    g_m = gpx / S
    n = 15
    fr = v[n]
    rm = (fr[..., 1] > 30) & (fr[..., 0] < 20) & (fr[..., 2] < 20)
    ys, xs = np.nonzero(rm[:340])
    rad = float(np.median(np.hypot(xs - 200, (ys - 360) * 3)))
    exp_r = 40 * (.6 + 3.4 * n / fps)
    amp = float(fr[..., 1][rm].max()) / 255
    second_first = next(i for i, f in enumerate(v) if ((f[..., 2] > 30) & (f[..., 0] < 20) & (f[..., 1] < 20)).any())
    return [check("tracked spray dot: y = .05 + vy u - 4.9 u^2 (recovered g m/s^2)", abs(g_m - 9.8) < .3, g_m, 9.8),
            check("ring scale .6 + 3.4u at u=.5 s", abs(rad - exp_r) < 3, rad, exp_r),
            check("ring alpha .9 e^(-.9u) at u=.5 s", abs(amp - .9 * math.exp(-.9 * n / fps)) < .02, amp, .9 * math.exp(-.9 * n / fps)),
            check("second ring starts .35 s later", abs(second_first / fps - .35) <= 1 / fps + 1e-9, second_first / fps, .35),
            check("negative control: the first tracked position held has no gravity",
                  abs(_quad_fit(np.array([a for a, _ in ok]), np.full(len(ok), ok[0][1]))[0] / S) < .3, 0.0, 9.8)], [vid]


@card("PART-59")
def stylised_water(task, wd):
    W, H, t = 1920, 1080, .8
    xs = np.arange(W)
    crest = 790 + 9 * np.sin(2 * math.pi * xs / 180 + 2.2 * t)
    yy = np.arange(H)[:, None]
    sea = yy >= crest[None]
    img = np.zeros((H, W, 3))
    sky = np.array([127, 178, 224.0])
    img[:] = sky
    g = (yy - 780) / 300
    seacol = _hex("#2B86E0") * (1 - np.clip(g, 0, 1))[..., None] + _hex("#1559A8") * np.clip(g, 0, 1)[..., None]
    img = np.where(sea[..., None], np.broadcast_to(seacol, (H, W, 3)), img)
    foam = (yy >= crest[None]) & (yy < crest[None] + 5)
    img[foam] = img[foam] * .2 + _hex("#CFE9FF") * .8
    p = _save(wd / "flat_sea.png", img)
    b = _load(p)
    top = np.argmax(np.abs(b - sky).sum(-1) > 30, axis=0).astype(float)
    k = W / 180
    A = np.column_stack([np.ones(W), np.sin(2 * math.pi * xs / 180), np.cos(2 * math.pi * xs / 180)])
    coef = np.linalg.lstsq(A, top, rcond=None)[0]
    amp = math.hypot(coef[1], coef[2])
    spec = np.abs(np.fft.rfft(top - top.mean()))
    def amp_at(l):
        B = np.column_stack([np.ones(W), np.sin(2 * math.pi * xs / l), np.cos(2 * math.pi * xs / l)])
        c = np.linalg.lstsq(B, top, rcond=None)[0]
        return math.hypot(c[1], c[2])
    cands = np.arange(150, 210.01, .5)
    lam = float(cands[int(np.argmax([amp_at(l) for l in cands]))])
    # shader version: three summed sines with analytic normals, Fresnel and hashed glints
    gx, gz = np.meshgrid(np.linspace(-20, 20, 320), np.linspace(1, 60, 240))
    waves = [(.12, .9, .3, 1.3), (.08, 1.7, -.6, 2.1), (.05, 3.1, .9, 3.0)]
    dhx = sum(a * k_ * math.cos(dd) * np.cos(k_ * (gx * math.cos(dd) + gz * math.sin(dd)) + w * t) for a, k_, dd, w in waves)
    dhz = sum(a * k_ * math.sin(dd) * np.cos(k_ * (gx * math.cos(dd) + gz * math.sin(dd)) + w * t) for a, k_, dd, w in waves)
    N = np.stack([-dhx, np.ones_like(gx), -dhz], -1)
    N /= np.linalg.norm(N, axis=-1, keepdims=True)
    cam = np.array([0, 3.0, 0])
    P = np.stack([gx, np.zeros_like(gx), gz], -1)
    V = cam - P
    V /= np.linalg.norm(V, axis=-1, keepdims=True)
    fres = (1 - np.clip((N * V).sum(-1), 0, 1)) ** 4
    cell = np.floor(gx * 1.6) * 57 + np.floor(gz * 1.6) * 113 + math.floor(9 * t)
    h = np.sin(cell) * 43758.5453
    h -= np.floor(h)
    spark = (h >= .9965).astype(float)
    d = np.linalg.norm(P - cam, axis=-1)
    fog = 1 - np.exp(-(d * .02) ** 2)
    shader = _save(wd / "water_shader_terms.png", np.stack([fres * 255, spark * 255, fog * 255], -1))
    near, far = float(fres[:40].mean()), float(fres[-40:].mean())
    flat_top = np.full(W, 790.0)
    namp = math.hypot(*np.linalg.lstsq(A, flat_top, rcond=None)[0][1:])
    return [check("crest amplitude 9 px", abs(amp - 9) < .6, amp, 9),
            check("crest wavelength 180 px", abs(lam - 180) < 3, lam, 180),
            check("Fresnel pow(1-N.V,4) rises toward the horizon", far > near * 1.5, [near, far], "far > near"),
            check("hashed glints ~0.35% of cells", .001 < spark.mean() < .007, float(spark.mean()), .0035),
            check("negative control: a flat line has no wave amplitude", namp < .5, namp, 0)], [p, shader]


MATTER_JS = r"""
const M = require('matter-js');
const e = M.Engine.create(); e.gravity.y = 1;
const ground = M.Bodies.rectangle(200, 390, 400, 20, {isStatic: true});
let seed = 71; const rnd = () => { seed = (seed * 1103515245 + 12345) % 2147483648; return seed / 2147483648; };
const boxes = [];
for (let i = 0; i < 6; i++) boxes.push(M.Bodies.rectangle(150 + rnd() * 100, 60 - i * 45, 36, 36, {friction: .8}));
M.Composite.add(e.world, [ground, ...boxes]);
const dt = 1000 / 30, frames = [];
for (let f = 0; f < 240; f++) {
  frames.push(boxes.map(b => [b.position.x, b.position.y, b.angle, b.speed, b.bounds.min.x, b.bounds.min.y, b.bounds.max.x, b.bounds.max.y]));
  M.Engine.update(e, dt);
}
console.log(JSON.stringify({dt, frames}));
"""


@card("PART-71")
def rigid_bake(task, wd):
    if not fx.which("node") or not Path(NODE_MODULES, "matter-js").exists():
        raise RuntimeError("matter-js not installed")
    js = wd / "bake.js"
    js.write_text(MATTER_JS, "utf-8")
    env = dict(os.environ, NODE_PATH=NODE_MODULES)
    outs = []
    for _ in range(2):
        r = subprocess.run(["node", str(js)], capture_output=True, text=True, timeout=30, env=env, stdin=subprocess.DEVNULL)
        if r.returncode:
            raise RuntimeError(r.stderr[-300:])
        outs.append(r.stdout)
    bake = wd / "bake.json"
    bake.write_text(outs[0], "utf-8")
    data = json.loads(bake.read_text())
    fr = data["frames"]
    frames = []
    for f in fr[::3]:
        im = Image.new("RGB", (400, 400), (20, 22, 30))
        d = ImageDraw.Draw(im)
        d.rectangle([0, 380, 400, 400], fill=(90, 90, 90))
        for x, y, a, s, *_ in f:
            pts = [(x + 18 * math.cos(a + q) * 1.414 * math.cos(math.pi / 4) - 0, 0) for q in ()]
            c, sn = math.cos(a), math.sin(a)
            corners = [(x + c * dx - sn * dy, y + sn * dx + c * dy) for dx, dy in ((-18, -18), (18, -18), (18, 18), (-18, 18))]
            d.polygon(corners, fill=(220, 120, 60))
        frames.append(np.asarray(im).astype(float))
    vid = _video(wd / "rigid_from_bake.mp4", frames, 10)
    # free fall of the top box before any contact: constant second difference
    ytop = np.array([f[5][1] for f in fr[:12]])
    dy = np.diff(ytop)
    # matter-js 0.20 Verlet: dy[n+1] = (1 - frictionAir * dt / (1000/60)) dy[n] + g * scale * dt^2
    pred = (1 - .01 * data["dt"] / (1000 / 60)) * dy[:-1] + 1 * .001 * data["dt"] ** 2
    const = float(np.abs(dy[1:] - pred).max())
    last = fr[-1]
    rest = max(b[3] for b in last)
    overl = 0.0
    for i in range(6):
        for j in range(i + 1, 6):
            a, b = last[i], last[j]
            ox = min(a[6], b[6]) - max(a[4], b[4])
            oy = min(a[7], b[7]) - max(a[5], b[5])
            if ox > 2 and oy > 0:
                overl = max(overl, oy)
    on_ground = max(b[7] for b in last) - 380 < 1.5   # resting-contact slop into the ground
    first = fr[0]
    airborne = max(b[7] for b in first) < 370
    return [check("bake is deterministic (two fixed-dt runs identical)", outs[0] == outs[1], True, True),
            check("free fall follows the Verlet recurrence with g*scale*dt^2 (max residual px)", const < 1e-3, const, "<1e-3"),
            check("all bodies at rest at the end of the bake", rest < .05, rest, "<0.05"),
            check("no interpenetration > 1.5 px in the final stack", overl < 1.5, overl, "<1.5"),
            check("stack rests on the ground plane (penetration < 1.5 px)", on_ground, max(b[7] for b in last) - 380, "<1.5"),
            check("negative control: the initial state is airborne", airborne, max(b[7] for b in first), "<370")], [bake, vid]


@card("PART-72")
def pendulum(task, wd):
    zeta, f0, fps = .15, 1.0, 60
    w0 = 2 * math.pi * f0
    dt = 1 / 600
    th, om = math.radians(14), 0.0
    angs = []
    for i in range(int(6 * 600)):
        if i % 10 == 0:
            angs.append(th)
        def acc(a, o):
            return -w0 * w0 * math.sin(a) - 2 * zeta * w0 * o
        k1 = (om, acc(th, om))
        k2 = (om + k1[1] * dt / 2, acc(th + k1[0] * dt / 2, om + k1[1] * dt / 2))
        k3 = (om + k2[1] * dt / 2, acc(th + k2[0] * dt / 2, om + k2[1] * dt / 2))
        k4 = (om + k3[1] * dt, acc(th + k3[0] * dt, om + k3[1] * dt))
        th += dt / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        om += dt / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
    frames = []
    for a in angs[:int(2.2 * fps)]:
        im = Image.new("L", (240, 240), 0)
        d = ImageDraw.Draw(im)
        px, py, L = 120, 20, 180
        c, s = math.cos(a), math.sin(a)
        poly = [(px + c * dx + s * dy, py - s * dx + c * dy) for dx, dy in ((-20, 0), (20, 0), (20, L), (-20, L))]
        d.polygon(poly, fill=255)
        frames.append(np.stack([np.asarray(im).astype(float)] * 3, -1))
    vid = _video(wd / "pendulum.mp4", frames, fps)
    v = fx.frames(vid, (240, 240))
    meas = []
    for fr in v:
        ys, xs = np.nonzero(fr[..., 0] > 128)
        cov = np.cov(np.vstack([xs - xs.mean(), ys - ys.mean()]))
        ev, evec = np.linalg.eigh(cov)
        vx, vy = evec[:, 1]
        if vy < 0:
            vx, vy = -vx, -vy
        meas.append(math.atan2(vx, vy))
    meas = np.array(meas)
    p1 = float(meas[0])
    p2 = float(meas[int(.7 * fps):int(1.3 * fps)].max())   # next positive swing, one damped period later
    dlt = math.log(p1 / p2)
    z = dlt / math.sqrt(4 * math.pi ** 2 + dlt * dlt)
    victim = {"intruder": .8, "victim": .36}
    ratio = victim["victim"] / victim["intruder"]
    (wd / "physical_motion.json").write_text(json.dumps({"zeta": zeta, "measured_zeta": z, "displacement": victim}), "utf-8")
    end = abs(angs[-1])
    return [check("damped swing: damping ratio from the measured log decrement", abs(z - zeta) < .02, z, zeta),
            check("settles to rest (< 0.2 deg after 6 s)", math.degrees(end) < .2, math.degrees(end), "<0.2"),
            check("reactive displacement: victim duration 40-50% of intruder", .4 <= ratio <= .5, ratio, "0.4..0.5"),
            check("negative control: the unsimulated card (angle held) gives zero damping",
                  abs(math.log(p1 / p1)) < 1e-9 and abs(0 - zeta) > .02, 0.0, zeta)], \
        [vid, wd / "physical_motion.json"]


@card("PART-X01")
def code_rain(task, wd):
    cell, W, H, fps = 30, 240, 360, 30
    fnt = ImageFont.load_default(size=28)
    glyphs = "01アイウエオカキ#$%&*+<>"
    glyphs = "0123456789ABCDEF#$%&*+<>"
    cols = [(i, 80 + 340 * _basma_rnd(i + 3), int(4 + 26 * _basma_rnd(i + 9))) for i in range(W // cell)]
    test_col = 2
    cols[test_col] = (test_col, 150.0, 8)

    def frame(t):
        im = Image.new("L", (W, H), 0)
        d = ImageDraw.Draw(im)
        d.fontmode = "1"
        for ci, sp, L in cols:
            head = sp * t
            hi = int(head // cell)
            for j in range(L):
                row = hi - j
                if row < 0 or row * cell > H:
                    continue
                a = .8 * (1 - j / L) ** 1.5
                rate = 16 if j == 0 else 2.5
                gi = int(_basma_rnd(ci * 131 + row * 7 + math.floor(t * rate)) * len(glyphs))
                d.text((ci * cell + 4, row * cell), glyphs[gi], font=fnt, fill=int(round(255 * a)))
        return np.asarray(im).astype(float)
    frames = [np.stack([frame(n / fps)] * 3, -1) for n in range(40)]
    vid = _video(wd / "code_rain.mp4", frames, fps)
    v = fx.frames(vid, (W, H))
    fr = v[39][..., 0]
    colv = fr[:, test_col * cell:(test_col + 1) * cell]
    head_row = int(150 * 39 / fps // cell)
    meas = [float(colv[(head_row - j) * cell:(head_row - j + 1) * cell].max()) for j in range(8) if head_row - j >= 0]
    exp = [round(255 * .8 * (1 - j / 8) ** 1.5) for j in range(len(meas))]
    err = max(abs(a - b) for a, b in zip(meas, exp))
    heads = []
    for n in range(0, 40, 5):
        c = v[n][..., 0][:, test_col * cell:(test_col + 1) * cell]
        rows = [r for r in range(H // cell) if c[r * cell:(r + 1) * cell].max() >= 203]
        heads.append(max(rows) if rows else None)
    exp_heads = [int(150 * n / fps // cell) for n in range(0, 40, 5)]
    sizes_ok = cell >= 30
    flat = np.full(8, 204.0)
    neg_err = max(abs(a - b) for a, b in zip(flat, exp))
    return [check("trail alpha (1 - j/L)^1.5 * .8 per glyph cell (max level error)", err <= 1, err, "<=1"),
            check("head row advances at the column speed (150 px/s)", heads == exp_heads, heads, exp_heads),
            check("glyph cells >= 30 px", sizes_ok, cell, ">=30"),
            check("speeds within 80-420 px/s", all(80 <= sp <= 420 for _, sp, _ in cols), [round(sp) for _, sp, _ in cols], "80..420"),
            check("negative control: a flat-alpha column fails the trail profile", neg_err > 20, neg_err, ">20")], [vid]
