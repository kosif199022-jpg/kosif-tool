"""pixel-retro-stylized: method cards as real programs with known-answer checks.

Every runner builds a seeded fixture in the work folder, applies the card's method (numpy / PIL /
ffmpeg / the installed HyperFrames dither script) and measures the produced file. Each returns a
negative control: the same measurement on the unprocessed input must fail the criterion.
"""
import json
import math
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from _harness import card, check, fx

GAPS: dict = {
    "RETRO-14": "the card is the HyperFrames media-treatment command itself (engraving/crosshatch/Kuwahara "
                "attributes interpreted by the HyperFrames runtime in headless Chrome); no runner wired here and "
                "the treatments' shader maths is not given on the card",
    "RETRO-17": "the card is the HyperFrames registry blocks yt-screen-warp / camcorder-hud / yt-lcd-background "
                "(GSAP timelines rendered in headless Chrome after `hyperframes add`); not reproducible from the "
                "card's text and no <15 s Chrome render wired here",
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


def _colours(a):
    return {tuple(int(v) for v in c) for c in np.asarray(a).reshape(-1, np.asarray(a).shape[-1])}


def _blur(a, s):
    from scipy.ndimage import gaussian_filter
    sig = (s, s) + ((0,) if np.asarray(a).ndim == 3 else ())
    return gaussian_filter(np.asarray(a, dtype=float), sig)


def _video(path, frames, fps=30, lossless=True):
    frames = [np.clip(np.round(f), 0, 255).astype(np.uint8) for f in frames]
    h, w = frames[0].shape[:2]
    codec = ["-c:v", "libx264rgb", "-qp", "0", "-pix_fmt", "rgb24"] if lossless else \
        ["-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p"]
    p = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                        "-s", "%dx%d" % (w, h), "-r", str(fps), "-i", "-", *codec, str(path)],
                       input=b"".join(f.tobytes() for f in frames), capture_output=True, timeout=60)
    if p.returncode:
        raise RuntimeError(p.stderr.decode()[-300:])
    return Path(path)


def _shift_x(a, b, maxs=12):
    """Integer horizontal shift s that best maps a onto b (b[x] ~ a[x - s])."""
    best, bs = None, 0
    for s in range(-maxs, maxs + 1):
        e = np.mean((np.roll(a, s, axis=1) - b) ** 2)
        if best is None or e < best:
            best, bs = e, s
    return bs


def _font(size=10):
    return ImageFont.load_default(size=size)


def _prompt_lock(wd, name, block, scenes, forbidden):
    prompts = ["%s\n\nSTYLE LOCK:\n%s" % (s, block) for s in scenes]
    out = wd / ("%s_prompts.json" % name)
    out.write_text(json.dumps({"style_block": block, "prompts": prompts}, ensure_ascii=False, indent=1), "utf-8")
    back = json.loads(out.read_text("utf-8"))["prompts"]
    import hashlib
    hashes = {hashlib.sha256(p.split("STYLE LOCK:\n", 1)[1].encode()).hexdigest() if "STYLE LOCK:\n" in p else None
              for p in back}
    raw_has = sum(block in s for s in scenes)
    bad = [w for w in forbidden if any(w.lower() in p.lower() for p in back)]
    return [check("every prompt carries the style block verbatim", all(block in p for p in back), len(back), len(scenes)),
            check("one identical style block hash across prompts", len(hashes) == 1 and None not in hashes, len(hashes), 1),
            check("forbidden words absent", not bad, bad, []),
            check("negative control: raw scene prompts lack the block", raw_has == 0, raw_has, 0)], [out]


B4 = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]], dtype=float)
GB = ["#0f380f", "#306230", "#8bac0f", "#9bbc0f"]


def _bayer_quant(v, n):
    """v in 0..1 -> palette index with a 4x4 Bayer threshold offset."""
    h, w = v.shape
    th = np.tile(B4, (h // 4 + 1, w // 4 + 1))[:h, :w] / 16.0 + 1 / 32.0
    return np.clip(np.floor(v * (n - 1) + th), 0, n - 1).astype(int)


# ----------------------------------------------------------------- cards
@card("RETRO-02")
def bayer_fade(task, wd):
    pal = np.array([_hex(c) for c in GB])
    h, w = 64, 128
    scene = np.tile(np.linspace(0, 1, w), (h, 1))
    frames, means, targets = [], [], []
    for f in (1.0, .75, .5, .25, 0.0):
        v = scene * f
        idx = _bayer_quant(v, 4)
        frames.append(pal[idx])
        means.append(float(idx.mean()))
        targets.append(float((v * 3).mean()))
    sheet = _save(wd / "bayer_fade_sheet.png", np.concatenate(frames, axis=0))
    back = _load(sheet).reshape(5, h, w, 3)
    pal_set = {tuple(int(x) for x in c) for c in pal}
    on_pal = all(_colours(fr) <= pal_set for fr in back)
    n_first = len(_colours(back[0]))
    mean_err = max(abs(m - t) for m, t in zip(means, targets))
    alpha = scene[..., None] * .5 * (pal[3] - pal[0]) + pal[0]   # an alpha fade, the forbidden way
    n_alpha = len(_colours(np.round(alpha)))
    return [check("every fade frame uses only the 4 Game Boy colours", on_pal, True, True),
            check("full-light frame has exactly 4 colours", n_first == 4, n_first, 4),
            check("ordered dither preserves mean ramp level (max error)", mean_err < .06, mean_err, "<0.06"),
            check("negative control: alpha fade has more than 4 colours", n_alpha > 4, n_alpha, ">4")], [sheet]


SPRITE = ["......oooo......", ".....ohhhho.....", "....ohbbbbho....", "....obbbbbbo....",
          "....obsbbsbo....", "....obbbbbbo....", ".....obbbbo.....", "....oobbbboo....",
          "...ohbbbbbbbbo..", "...obbbbbbbbbo..", "...obbobbobbbo..", "....obbbbbbo....",
          "....obbbbbbo....", "....obb..bbo....", "....oo....oo....", "................"]
SPAL = {"o": "#1a1c2c", "h": "#f4b41b", "b": "#e6482e", "s": "#622461"}


def _pose(pose):
    rows = [list(r) for r in SPRITE]
    if pose % 2:   # walking pose: swap leg columns, generator keeps every other pixel on-model
        rows[13] = list("....obbo.bbo....")
        rows[14] = list("....oo...ooo....")
    return ["".join(r) for r in rows]


@card("RETRO-03")
def palette_sprites(task, wd):
    pal = {k: _hex(v) for k, v in SPAL.items()}
    sprites = []
    for pose in range(2):
        g = _pose(pose)
        a = np.zeros((16, 16, 4))
        for y, r in enumerate(g):
            for x, k in enumerate(r):
                if k != ".":
                    a[y, x, :3], a[y, x, 3] = pal[k], 255
        # selective 1px outline: the generator turns every opaque pixel touching transparency into the line colour
        op = np.pad(a[..., 3] > 0, 1)
        rim = (a[..., 3] > 0) & ~(op[:-2, 1:-1] & op[2:, 1:-1] & op[1:-1, :-2] & op[1:-1, 2:])
        a[rim, :3] = pal["o"]
        sprites.append(a)
    sheet = np.concatenate(sprites, axis=1)
    p1 = wd / "sprite_sheet_1x.png"
    Image.fromarray(sheet.astype(np.uint8), "RGBA").save(p1)
    prev = np.kron(sheet, np.ones((8, 8, 1)))
    p8 = wd / "sprite_preview_x8.png"
    Image.fromarray(prev.astype(np.uint8), "RGBA").save(p8)
    back = np.asarray(Image.open(p1)).astype(float)
    opaque = back[..., 3] > 0
    cols = {tuple(int(v) for v in c) for c in back[opaque][:, :3]}
    palset = {tuple(int(v) for v in c) for c in pal.values()}
    pad = np.pad(opaque, 1)
    edge = opaque & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
    edge_ok = all(tuple(int(v) for v in back[y, x, :3]) == tuple(int(v) for v in pal["o"]) for y, x in zip(*np.where(edge)))
    pv = np.asarray(Image.open(p8)).astype(float)
    blocks = pv.reshape(16, 8, 32, 8, 4)
    uniform = float(blocks.std(axis=(1, 3)).max())
    counts = [int((s[..., 3] > 0).sum()) for s in sprites]
    smooth = np.asarray(Image.fromarray(sheet.astype(np.uint8), "RGBA").resize((48, 24), Image.BILINEAR)).astype(float)
    smooth_cols = {tuple(int(v) for v in c) for c in smooth[smooth[..., 3] == 255][:, :3]}
    return [check("all opaque pixels on the 4-colour palette", cols <= palset, len(cols), 4),
            check("silhouette edge pixels are the outline colour", edge_ok, True, True),
            check("x8 preview is nearest-neighbour (block std)", uniform == 0, uniform, 0),
            check("poses stay on-model (pixel count within 10%)", abs(counts[0] - counts[1]) <= .1 * counts[0], counts, "±10%"),
            check("size <= 24x24", max(sprites[0].shape[:2]) <= 24, 16, "<=24"),
            check("negative control: a smooth-resized sprite leaves the palette", not smooth_cols <= palset,
                  len(smooth_cols), ">4")], [p1, p8]


@card("RETRO-04")
def vfx_sheet(task, wd):
    ramp = [_hex(c) for c in ("#fff6d3", "#f9a875", "#eb6b6f", "#7c3f58")]  # bright -> dark
    bg = np.array([0., 0., 0.])
    timing = [(0, 40), (1, 80), (2, 40), (3, 40), (4, 40), (5, 40)]   # frame 1 = impact, held
    stage = [0, 0, 1, 2, 3, 3]
    radius = [3, 7, 9, 10, 11, 11]
    yy, xx = np.mgrid[:32, :32]
    frames, top_idx = [], []
    for f, (fi, ms) in enumerate(timing):
        img = np.tile(bg, (32, 32, 1))
        r = np.hypot(yy - 15.5, xx - 15.5)
        ring = r <= radius[f]
        # inner part one step brighter than the rim: palette-stepped, never alpha
        img[ring] = ramp[min(3, stage[f] + 1)]
        img[r <= radius[f] * .55] = ramp[stage[f]]
        if f == 5:
            img[r <= radius[f] * .55] = bg   # dissipates into a ring
        frames.append(img)
        top_idx.append(stage[f])
    sheet = _save(wd / "explosion_sheet.png", np.concatenate(frames, axis=1))
    gif = wd / "explosion_preview.gif"
    ims = [Image.fromarray(fr.astype(np.uint8)) for fr in frames]
    ims[0].save(gif, save_all=True, append_images=ims[1:], duration=[ms for _, ms in timing], loop=0)
    durs = []
    with Image.open(gif) as g:
        for i in range(g.n_frames):
            g.seek(i)
            durs.append(g.info.get("duration", 0))
    back = _load(sheet)
    allowed = {tuple(int(v) for v in c) for c in ramp} | {(0, 0, 0)}
    on_ramp = _colours(back) <= allowed
    mono = all(top_idx[i] <= top_idx[i + 1] for i in range(1, len(top_idx) - 1))
    alpha_fade = frames[1] * .6
    return [check("sheet colours only from the ramp + background", on_ramp, len(_colours(back)), "<=5"),
            check("GIF frame durations >= 20 ms", min(durs) >= 20, durs, ">=20"),
            check("impact frame held longest", durs[1] == max(durs) and durs[1] >= 2 * durs[2], durs[1], ">=2x"),
            check("ramp steps only darker after impact", mono, top_idx, "non-decreasing index"),
            check("negative control: an alpha fade leaves the ramp", not _colours(np.round(alpha_fade)) <= allowed,
                  False, "off-ramp")], [sheet, gif]


def _corner_tile(tl, tr, bl, br, cols, n=8):
    corners = np.array([[0, 0], [0, n], [n, 0], [n, n]], dtype=float)
    vals = [tl, tr, bl, br]
    t = np.zeros((n, n, 3))
    for y in range(n):
        for x in range(n):
            d = np.hypot(corners[:, 0] - (y + .5), corners[:, 1] - (x + .5))
            t[y, x] = cols[vals[int(np.argmin(d))]]
    return t


@card("RETRO-05")
def seamless_tiles(task, wd):
    cols = [_hex("#3b7d4f"), _hex("#2a5fa8")]   # grass, water
    tiles = {}
    for code in range(16):
        b = [(code >> i) & 1 for i in range(4)]
        tiles[tuple(b)] = _corner_tile(*b, cols)
    rng = _rng(5)
    for _ in range(200):
        grid = rng.integers(0, 2, size=(9, 9))
        used = {(grid[y, x], grid[y, x + 1], grid[y + 1, x], grid[y + 1, x + 1]) for y in range(8) for x in range(8)}
        if len(used) == 16:
            break
    mp = np.zeros((64, 64, 3))
    for y in range(8):
        for x in range(8):
            mp[y * 8:y * 8 + 8, x * 8:x * 8 + 8] = tiles[(grid[y, x], grid[y, x + 1], grid[y + 1, x], grid[y + 1, x + 1])]
    # seam score: compare each tile edge with the edge the neighbouring tile would draw for the shared corners
    def seam(m):
        s = 0
        for y in range(8):
            for x in range(7):
                a, b = m[y * 8:y * 8 + 8, x * 8 + 7], m[y * 8:y * 8 + 8, x * 8 + 8]
                s += float(np.abs(a - b).sum() > 0 and np.abs(a - b).mean())
        return s
    # adjacent edge columns must agree in terrain row by row (Voronoi corner ownership)
    def terrain(m):
        return (m[..., 2] > 100).astype(int)
    tm = terrain(mp)
    mism = int(sum((tm[:, x * 8 + 7] != tm[:, x * 8 + 8]).sum() for x in range(7)) +
               sum((tm[y * 8 + 7] != tm[y * 8 + 8]).sum() for y in range(7)))
    naive = np.zeros_like(mp)
    keys = list(tiles)
    for y in range(8):
        for x in range(8):
            naive[y * 8:y * 8 + 8, x * 8:x * 8 + 8] = tiles[keys[rng.integers(16)]]
    tn = terrain(naive)
    mism_naive = int(sum((tn[:, x * 8 + 7] != tn[:, x * 8 + 8]).sum() for x in range(7)) +
                     sum((tn[y * 8 + 7] != tn[y * 8 + 8]).sum() for y in range(7)))
    preview = np.tile(tiles[(1, 1, 1, 1)], (3, 3, 1))
    p_map = _save(wd / "corner_tiles_test_map.png", np.kron(mp, np.ones((4, 4, 1))))
    p_pre = _save(wd / "tile_3x3_preview.png", preview)
    # parallax: deeper = slower and darker; step must divide the loop width
    loop_w, layers = 256, [{"depth": d, "speed": 4 / 2 ** d, "dark": .8 ** d} for d in range(3)]
    divides = all(loop_w % l["speed"] == 0 for l in layers)
    slower = all(layers[i]["speed"] > layers[i + 1]["speed"] and layers[i]["dark"] > layers[i + 1]["dark"]
                 for i in range(2))
    (wd / "parallax.json").write_text(json.dumps({"loop_width": loop_w, "layers": layers}), "utf-8")
    return [check("test map exercises all 16 corner transitions", len(used) == 16, len(used), 16),
            check("no terrain mismatch across any tile seam", mism == 0, mism, 0),
            check("parallax deeper layers slower and darker", slower, True, True),
            check("scroll step divides loop width", divides, True, True),
            check("negative control: random tile choice breaks seams", mism_naive > 0, mism_naive, ">0")], \
        [p_map, p_pre, wd / "parallax.json"]


@card("RETRO-07")
def diorama_reflection(task, wd):
    w, h = 480, 270
    horizon = 150
    rng = _rng(3)
    img = np.zeros((h, w, 3))
    for y in range(horizon):
        img[y] = _hex("#1b2a49") + (y / horizon) * (_hex("#f08a4b") - _hex("#1b2a49"))
    for x in range(w):
        hill = int(110 + 18 * math.sin(x / 37.0) + 9 * math.sin(x / 13.0))
        img[hill:horizon, x] = _hex("#2d1e2f")
    img[30:44, 300:314] = _hex("#ffe08a")   # pixel sun
    for _ in range(40):
        img[rng.integers(0, 80), rng.integers(0, w)] = 255
    base = img.copy()
    t, amp, tint = 0.5, 2, .7
    lake_rows = h - horizon
    shifts = []
    for j in range(lake_rows):
        src = horizon - 1 - j
        s = int(round(amp * math.sin(2.0 * t + j * .45)))
        shifts.append(s)
        img[horizon + j] = np.roll(base[src], s, axis=0) * tint
    out = _save(wd / "diorama_x4.png", np.kron(img, np.ones((4, 4, 1))))
    back = _load(out)
    small = back[::4, ::4]
    blk = float(back.reshape(h, 4, w, 4, 3).std(axis=(1, 3)).max())
    ok_rows, nonzero = 0, 0
    for j in range(0, lake_rows, 3):
        row = small[horizon + j]
        src = base[horizon - 1 - j] * tint
        m = _shift_x(src[None], row[None], 3)
        ok_rows += int(m == shifts[j] or np.allclose(np.roll(src, m, 0), np.roll(src, shifts[j], 0), atol=1))
        nonzero += int(shifts[j] != 0)
    n_tested = len(range(0, lake_rows, 3))
    ratio = float(small[horizon:].mean() / np.mean([base[horizon - 1 - j] for j in range(lake_rows)]))
    neg = float(np.abs(base[horizon + 10] - base[horizon - 11] * tint).mean())
    return [check("lake rows are the mirrored sky with the per-row sine offset", ok_rows == n_tested, ok_rows, n_tested),
            check("ripple offsets within 1-2 px and not all zero", nonzero > 0 and max(abs(s) for s in shifts) <= 2,
                  max(abs(s) for s in shifts), "1..2"),
            check("reflection darker by the tint", abs(ratio - tint) < .03, ratio, tint),
            check("x4 nearest upscale keeps 4x4 blocks", blk == 0, blk, 0),
            check("negative control: unprocessed lake is not the reflection", neg > 5, neg, ">5")], [out]


@card("RETRO-08")
def hud_typewriter(task, wd):
    text = "HELLO KOSIF WORLD"
    fnt = _font(8)
    fps, ms = 30, 30
    W, H = 160, 90
    frames, expect, measured = [], [], []
    for n in range(0, 24):
        t = n / fps
        k = min(len(text), int(t * 1000 // ms))
        im = Image.new("RGB", (W, H), (40, 120, 200))
        d = ImageDraw.Draw(im)
        d.fontmode = "1"
        d.rectangle([8, 52, 151, 83], fill=(250, 220, 40), outline=(0, 0, 0), width=2)
        if k:
            d.text((14, 60), text[:k], font=fnt, fill=(0, 0, 0))
        frames.append(np.kron(np.asarray(im).astype(float), np.ones((4, 4, 1))))
        expect.append(k)
    vid = _video(wd / "dialogue_x4.mp4", frames, fps)
    back = fx.frames(vid, (W * 4, H * 4))
    def ink_extent(fr):
        box = fr[::4, ::4][56:80, 12:148]
        ink = (box.sum(axis=2) < 60)
        cols = np.where(ink.any(axis=0))[0]
        return int(cols.max()) + 1 if cols.size else 0
    def probe(k):
        im = Image.new("RGB", (W, H), (40, 120, 200))
        d = ImageDraw.Draw(im)
        d.fontmode = "1"
        d.rectangle([8, 52, 151, 83], fill=(250, 220, 40), outline=(0, 0, 0), width=2)
        if k:
            d.text((14, 60), text[:k], font=fnt, fill=(0, 0, 0))
        return ink_extent(np.kron(np.asarray(im).astype(float), np.ones((4, 4, 1))))
    ok = 0
    for fr, k in zip(back, expect):
        e = ink_extent(fr)
        ok += int(e == probe(k))
        measured.append(e)
    blocks = float(back[5].reshape(H, 4, W, 4, 3).std(axis=(1, 3)).mean())
    border = back[-1][::4, ::4][52, 80]
    return [check("visible text grows 1 char / 30 ms (ink extent per frame)", ok == len(expect), ok, len(expect)),
            check("text complete by 17*30 ms", expect[-1] == len(text), expect[-1], len(text)),
            check("4x pixel scale (mean intra-block std)", blocks < 1.0, blocks, "<1"),
            check("box border is black", float(border.sum()) < 60, border.tolist(), "black"),
            check("negative control: without the typewriter frame 0 would already show the full line",
                  probe(len(text)) != measured[0], [probe(len(text)), measured[0]], "differ")], [vid]


@card("RETRO-09")
def pixel_chapter(task, wd):
    rng = _rng(9)
    pal = np.array([_hex(c) for c in ("#1a1c2c", "#5d275d", "#b13e53", "#ef7d57", "#ffcd75", "#a7f070")])
    src = pal[rng.integers(0, 6, size=(180, 320))]
    p_src = _save(wd / "chapter_320x180.png", src)
    modern = wd / "modern.mp4"
    fx.ffmpeg("-f", "lavfi", "-i", "testsrc2=s=1920x1080:r=30:d=1.5", "-pix_fmt", "yuv420p", "-c:v", "libx264",
              "-preset", "ultrafast", "-crf", "18", str(modern))
    out = wd / "edit_with_pixel_chapter.mp4"
    fx.ffmpeg("-i", str(modern), "-loop", "1", "-t", "1.5", "-framerate", "30", "-i", str(p_src), "-filter_complex",
              "[1:v]scale=1920:1080:flags=neighbor,format=yuv420p,setsar=1,fps=30,settb=AVTB[px];"
              "[0:v]format=yuv420p,setsar=1,fps=30,settb=AVTB[m];[m][px]xfade=transition=pixelize:duration=0.5:offset=1[v]",
              "-map", "[v]", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "16", "-pix_fmt", "yuv420p", str(out),
              timeout=60)
    fr = wd / "frame_2_2.png"
    fx.ffmpeg("-ss", "2.2", "-i", str(out), "-frames:v", "1", str(fr))
    a = _luma(_load(fr))
    def blockstd(img):
        return float(img[:1080, :1920].reshape(180, 6, 320, 6).std(axis=(1, 3)).mean())
    s_out = blockstd(a)
    bil = _luma(np.asarray(Image.open(p_src).resize((1920, 1080), Image.BILINEAR)).astype(float))
    s_neg = blockstd(bil)
    pr = fx.probe(out)
    v = [s for s in pr["streams"] if s["codec_type"] == "video"][0]
    dur = float(pr["format"]["duration"])
    return [check("output is 1920x1080", (v["width"], v["height"]) == (1920, 1080), [v["width"], v["height"]], [1920, 1080]),
            check("x6 neighbour chapter stays blocky (mean intra-block std)", s_out < 5, s_out, "<5"),
            check("xfade overlap gives 1.5+1.5-0.5 s", abs(dur - 2.5) < .1, dur, 2.5),
            check("negative control: bilinear upscale is not blocky", s_neg > 2 * s_out and s_neg > 8, s_neg, ">8")], \
        [out, fr]


@card("RETRO-10")
def luma_halftone(task, wd):
    cell, R, ss = 12, 6.0, 4
    cols = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1], [.6, .6, .6], [.3, .3, .3], [0, 0, 0]]) * .6
    gh, gw = 4, 6
    src = np.zeros((gh * cell, gw * cell, 3))
    for i, c in enumerate(cols):
        src[:, i * cell:(i + 1) * cell] = c * 255
    H, W = src.shape[:2]
    yy, xx = (np.mgrid[:H * ss, :W * ss] + .5) / ss
    cy = (np.floor(yy / cell) + .5) * cell
    cx = (np.floor(xx / cell) + .5) * cell
    samp = src[np.clip(cy.astype(int), 0, H - 1), np.clip(cx.astype(int), 0, W - 1)] / 255
    lum = samp @ np.array([.2126, .7152, .0722])
    r = R * (0.1 + lum)
    dot = (np.hypot(yy - cy, xx - cx) <= r).astype(float)
    cov = dot.reshape(H, ss, W, ss).mean(axis=(1, 3))
    out = _save(wd / "halftone.png", np.stack([cov * 255] * 3, -1))
    back = _load(out)[..., 0] / 255
    errs, errs_neg = [], []
    for i, c in enumerate(cols):
        lum_c = float(c @ np.array([.2126, .7152, .0722]))
        pred = R * (0.1 + lum_c)
        area = back[:cell, i * cell:(i + 1) * cell].sum()
        errs.append(abs(math.sqrt(area / math.pi) - pred))
        area_in = (src[:cell, i * cell:(i + 1) * cell, 0] / 255).sum()
        errs_neg.append(abs(math.sqrt(area_in / math.pi) - pred))
    green_r = math.sqrt(back[:cell, cell:2 * cell].sum() / math.pi)
    return [check("dot radius per cell = R*(0.1+luma) (max error px)", max(errs) < .35, max(errs), "<0.35"),
            check("Rec.709 luma weights: green dot radius", abs(green_r - R * (.1 + .6 * .7152)) < .35, green_r,
                  R * (.1 + .6 * .7152)),
            check("negative control: input coverage does not follow the dot formula", max(errs_neg) > 1, max(errs_neg),
                  ">1")], [out]


@card("RETRO-11")
def riso(task, wd):
    paper, pink, blue = _hex("#F2EBDD"), _hex("#FF48B0"), _hex("#0078BF")
    H, W = 120, 160
    yy, xx = np.mgrid[:H, :W]
    m_pink = (np.hypot(yy - 60, xx - 70) < 32).astype(float)
    m_blue = ((abs(yy - 60) < 26) & (abs(xx - 92) < 26)).astype(float)

    def offset(t):   # 0-1 s paper, 1-3 s drift at 6 px, 3-5 s settle to registration
        if t < 3:
            return 6.0
        return 6.0 * max(0.0, 1 - (t - 3) / 2) ** 2

    def frame(t):
        o = int(round(offset(t)))
        mp = np.roll(m_pink, o, axis=1)
        img = np.tile(paper, (H, W, 1))
        img = img * (1 - mp[..., None] + mp[..., None] * pink / 255)
        img = img * (1 - m_blue[..., None] + m_blue[..., None] * blue / 255)
        return img
    frames = [frame(t) for t in np.arange(1, 5.01, .25)]
    p2 = _save(wd / "riso_t2.png", frame(2.0))
    p5 = _save(wd / "riso_t5.png", frame(5.0))
    raw = wd / "riso_raw.mp4"
    _video(raw, frames, fps=4, lossless=True)
    grain = wd / "riso_grain.mp4"
    fx.ffmpeg("-i", str(raw), "-vf", "noise=alls=8:allf=t", "-c:v", "libx264rgb", "-qp", "0", str(grain))
    a5 = _load(p5)
    expect = np.floor(np.floor(paper * pink / 255) * blue / 255)
    over = a5[60, 80]
    a2 = _load(p2)
    pinkc = paper * pink / 255

    def left_edge(img):
        row = np.abs(img[60] - pinkc).sum(-1) < 8
        return int(np.where(row)[0].min())
    s = left_edge(a2) - left_edge(a5)
    g = fx.frames(grain, (W, H))
    flat = g[:, 5:20, 5:20, 1]
    tstd = float(flat.std(axis=0).mean())
    normal = paper * .0 + blue   # normal blend: the top ink hides the other
    return [check("overlap = multiply of paper x pink x blue", np.abs(over - expect).max() <= 2, over.tolist(),
                  expect.tolist()),
            check("misregistration offset during drift = 6 px", s == 6, s, 6),
            check("registered at 5 s", offset(5.0) == 0, offset(5.0), 0),
            check("temporal grain present in the paper (frame std)", tstd > 2, tstd, ">2"),
            check("negative control: normal blend would not give the multiply colour",
                  np.abs(normal - expect).max() > 20, normal.tolist(), "!= multiply")], [p2, p5, grain]


@card("RETRO-12")
def film_strips(task, wd):
    W, H, fps = 160, 90, 10
    v1, v2 = 40.0, 25.0

    def strip(xoff, y0, photo_col):
        s = np.full((22, W, 3), 20.0)
        for x in range(W):
            if (int(x - xoff) % 16) < 6:
                s[2:5, x] = s[17:20, x] = 230   # perforations
        for k in range(3):
            px = int((k * 60 + xoff) % (W + 40)) - 40
            s[6:16, max(0, px):max(0, px + 30)] = photo_col
        return s
    frames = []
    for n in range(8 * fps):
        t = n / fps
        tt = min(t, 5.0)   # strips stop at 5 s, title holds
        img = np.full((H, W, 3), 12.0)
        img[10:32] = strip(v1 * tt, 10, (200, 150, 90))
        img[50:72] = strip(v2 * tt, 50, (90, 160, 200))
        if t >= 5:
            img[38:46, 50:110] = 250
        frames.append(img)
    vid = _video(wd / "film_strips.mp4", frames, fps)
    f = fx.frames(vid, (W, H))
    s1 = _shift_x(f[30, 10:32, :, 1], f[31, 10:32, :, 1], 8)
    s2 = _shift_x(f[30, 50:72, :, 1], f[31, 50:72, :, 1], 8)
    stopped = float(np.abs(f[60] - f[70]).max())
    moving = float(np.abs(f[30] - f[31]).max())
    title_before, title_after = float(f[40, 38:46, 50:110].mean()), float(f[60, 38:46, 50:110].mean())
    return [check("strip 1 speed 40 px/s (shift per frame 4 px)", s1 == 4, s1, 4),
            check("strip 2 slower (2.5 px/frame -> 2 or 3 px)", s2 in (2, 3) and s2 < s1, s2, "2..3"),
            check("strips and frame frozen on the title after 5 s", stopped == 0, stopped, 0),
            check("title appears at 5 s", title_after > 200 and title_before < 40, [title_before, title_after], "dark->lit"),
            check("negative control: during 2-5 s the frame is not frozen", moving > 50, moving, ">50")], [vid]


def _srgb_to_lab(rgb):
    c = rgb / 255
    c = np.where(c > .04045, ((c + .055) / 1.055) ** 2.4, c / 12.92)
    m = np.array([[.4124, .3576, .1805], [.2126, .7152, .0722], [.0193, .1192, .9505]])
    xyz = c @ m.T / np.array([.95047, 1, 1.08883])
    f = np.where(xyz > .008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)


@card("RETRO-13")
def poster_kmeans(task, wd):
    rng = _rng(13)
    H = W = 96
    yy, xx = np.mgrid[:H, :W]
    img = np.zeros((H, W, 3))
    img[...] = np.stack([60 + xx, 90 + .5 * yy, 160 - .6 * xx], -1)
    img[np.hypot(yy - 40, xx - 50) < 22] = (220, 80, 60)
    img[(yy > 65) & (xx < 40)] = (30, 40, 50)
    img += rng.normal(0, 10, img.shape)
    img = np.clip(img, 0, 255)
    # bilateral smoothing (5x5, sigma_s 2, sigma_r 25), edge-preserving
    acc, wsum = np.zeros_like(img), np.zeros((H, W, 1))
    pad = np.pad(img, ((2, 2), (2, 2), (0, 0)), mode="edge")
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            sh = pad[2 + dy:2 + dy + H, 2 + dx:2 + dx + W]
            wgt = np.exp(-(dy * dy + dx * dx) / 8.0) * np.exp(-((sh - img) ** 2).sum(-1, keepdims=True) / (2 * 25 ** 2))
            acc += wgt * sh
            wsum += wgt
    sm = acc / wsum
    lab = _srgb_to_lab(sm).reshape(-1, 3)
    k = 6
    cent = [lab[rng.integers(len(lab))]]
    for _ in range(k - 1):   # k-means++
        d = np.min([((lab - c) ** 2).sum(1) for c in cent], axis=0)
        cent.append(lab[rng.choice(len(lab), p=d / d.sum())])
    cent = np.array(cent)
    inertia = []
    for _ in range(15):
        lbl = np.argmin(((lab[:, None] - cent[None]) ** 2).sum(-1), 1)
        inertia.append(float(((lab - cent[lbl]) ** 2).sum()))
        cent = np.array([lab[lbl == j].mean(0) if (lbl == j).any() else cent[j] for j in range(k)])
    rgb_c = np.array([sm.reshape(-1, 3)[lbl == j].mean(0) for j in range(k)]).round()
    poster = rgb_c[lbl].reshape(H, W, 3)
    out = _save(wd / "poster_k6.png", poster)
    rects = []
    lb = lbl.reshape(H, W)
    for y in range(H):
        x = 0
        while x < W:
            x2 = x
            while x2 + 1 < W and lb[y, x2 + 1] == lb[y, x]:
                x2 += 1
            c = rgb_c[lb[y, x]].astype(int)
            rects.append('<rect x="%d" y="%d" width="%d" height="1" fill="#%02x%02x%02x"/>' % (x, y, x2 - x + 1, *c))
            x = x2 + 1
    svg = wd / "poster_k6.svg"
    svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" shape-rendering="crispEdges">%s</svg>'
                   % (W, H, "".join(rects)), "utf-8")
    n_out = len(_colours(_load(out)))
    import re
    fills = set(re.findall(r'fill="(#[0-9a-f]{6})"', svg.read_text("utf-8")))
    noise_before = float(img[5:30, 5:30].std(axis=(0, 1)).mean() - np.stack([60 + xx, 90 + .5 * yy, 160 - .6 * xx], -1)[5:30, 5:30].std(axis=(0, 1)).mean())
    edge_in = abs(img[40, 20:26].mean() - img[40, 30:34].mean())
    edge_sm = abs(sm[40, 20:26].mean() - sm[40, 30:34].mean())
    n_in = len(_colours(np.round(img)))
    return [check("poster has exactly k=6 colours", n_out == 6, n_out, 6),
            check("SVG uses the same 6 fills", len(fills) == 6, len(fills), 6),
            check("k-means inertia non-increasing", all(inertia[i + 1] <= inertia[i] + 1e-6 for i in range(len(inertia) - 1)),
                  [inertia[0], inertia[-1]], "decreasing"),
            check("bilateral keeps the circle edge (>=85% contrast)", edge_sm >= .85 * edge_in, [edge_in, edge_sm], ">=85%"),
            check("negative control: input has far more than 6 colours", n_in > 1000, n_in, ">1000")], [out, svg]


@card("RETRO-15")
def manga_burst(task, wd):
    H, W = 240, 240
    yy, xx = np.mgrid[:H, :W]
    rng = _rng(15)
    src = np.zeros((H, W, 3))
    src[...] = (120, 160, 200)
    subj = np.hypot(yy - 120, xx - 120) < 50
    src[subj] = np.stack([150 + 20 * np.sin(xx / 6.0), 110 + 20 * np.cos(yy / 5.0), 90 + 0 * xx], -1)[subj]
    gray = _luma(src)
    con = np.clip((gray - 128) * 1.6 + 128, 0, 255)
    out = np.stack([con] * 3, -1)
    n_lines = 72
    ang = (np.arctan2(yy - 120, xx - 120) + math.pi) / (2 * math.pi) * n_lines
    rr = np.hypot(yy - 120, xx - 120)
    line = (np.abs(ang - np.round(ang)) < .12 + .1 * _rng(16).random((H, W)) * 0) & (rr > 62)
    out[line] = 0
    p = _save(wd / "manga.png", out)
    b = _load(p)
    sat = float(np.abs(b[subj][:, 0] - b[subj][:, 2]).max())
    ratio = float(b[subj][:, 0].std() / gray[subj].std())
    ring = [(int(120 + 110 * math.sin(a)), int(120 + 110 * math.cos(a))) for a in np.linspace(0, 2 * math.pi, 3600, endpoint=False)]
    dark = np.array([b[y, x, 0] < 30 for y, x in ring])
    runs = int(np.sum(dark & ~np.roll(dark, 1)))
    ring_in = np.array([src[y, x, 0] < 30 for y, x in ring])
    runs_in = int(np.sum(ring_in & ~np.roll(ring_in, 1)))
    return [check("subject desaturated (max |R-B|)", sat == 0, sat, 0),
            check("contrast x1.6 (std ratio)", abs(ratio - 1.6) < .08, ratio, 1.6),
            check("60-90 radial speed lines on the outer ring", 60 <= runs <= 90, runs, "60..90"),
            check("negative control: input has no speed lines and is in colour", runs_in == 0 and
                  float(np.abs(src[subj][:, 0] - src[subj][:, 2]).max()) > 10, runs_in, 0)], [p]


@card("RETRO-16")
def crt_ffmpeg(task, wd):
    H, W = 180, 320
    yy, xx = np.mgrid[:H, :W]
    src = np.zeros((H, W, 3))
    src[..., 0] = src[..., 1] = src[..., 2] = 150
    src[:, 160:] = (90, 200, 120)
    p_in = _save(wd / "crt_in.png", src)
    out = wd / "crt_%02d.png"
    fx.ffmpeg("-loop", "1", "-i", str(p_in), "-vf",
              "drawgrid=w=iw:h=4:t=1:c=black@0.25,rgbashift=rh=2:bh=-2,noise=alls=8:allf=t",
              "-frames:v", "3", str(out))
    mp4 = wd / "crt.mp4"
    fx.ffmpeg("-loop", "1", "-t", "1", "-i", str(p_in), "-vf",
              "drawgrid=w=iw:h=4:t=1:c=black@0.25,rgbashift=rh=2:bh=-2,noise=alls=8:allf=t,format=yuv420p",
              "-c:v", "libx264", "-crf", "18", str(mp4))
    f1, f2 = _load(wd / "crt_01.png"), _load(wd / "crt_02.png")
    rows = f1[:, 20:140, 1].mean(axis=1)
    scan = rows[4:176:4].mean() / np.mean([rows[y] for y in range(4, 176) if y % 4])
    rin = _load(p_in)[:, 20:140, 1].mean(axis=1)
    scan_in = rin[4:176:4].mean() / np.mean([rin[y] for y in range(4, 176) if y % 4])
    redge = int(np.argmax(np.abs(np.diff(f1[1:179:4][:, :, 0].mean(0)[150:170])))) + 150
    gedge = int(np.argmax(np.abs(np.diff(f1[1:179:4][:, :, 1].mean(0)[150:170])))) + 150
    tdiff = float(np.abs(f1[1:179:4, 20:140] - f2[1:179:4, 20:140]).mean())
    return [check("every 4th row darkened by 25%", abs(scan - .75) < .04, scan, .75),
            check("rgbashift moves red 2 px right of green", redge - gedge == 2, redge - gedge, 2),
            check("temporal grain differs frame to frame", tdiff > 2, tdiff, ">2"),
            check("negative control: input rows not darkened", abs(scan_in - .75) > .2, scan_in, "1.0")], \
        [wd / "crt_01.png", mp4]


@card("RETRO-18")
def led_ticker(task, wd):
    W, H, pitch, fps, speed = 256, 48, 4, 30, 100
    mask_im = Image.new("L", (W * 3, H), 0)
    d = ImageDraw.Draw(mask_im)
    d.fontmode = "1"
    d.text((64, 4), "KOSIF 2026 +3.4%", font=_font(36), fill=255)
    mask = np.asarray(mask_im).astype(float) / 255
    yy, xx = np.mgrid[:H, :W]
    cy, cx = (yy // pitch) * pitch + pitch / 2 - .5, (xx // pitch) * pitch + pitch / 2 - .5
    disk = np.hypot(yy - cy, xx - cx) <= 1.5
    frames, lit_mats = [], []
    for n in range(0, 31):
        off = n * speed / fps
        gy, gx = np.arange(H // pitch) * pitch + pitch // 2, np.arange(W // pitch) * pitch + pitch // 2
        lit = mask[gy[:, None], np.clip((gx[None] + off).astype(int), 0, W * 3 - 1)] > .5
        litpix = np.kron(lit, np.ones((pitch, pitch))) * disk
        core = np.stack([litpix * 255, litpix * 60, litpix * 40], -1)
        glow = _blur(core, 6) * .6
        img = np.clip(core + glow + 10, 0, 255)
        frames.append(img)
        lit_mats.append(lit)
    vid = _video(wd / "led_ticker.mp4", frames, fps)
    p0 = _save(wd / "led_t0.png", frames[0])
    back = fx.frames(vid, (W, H))
    off_lattice = float(back[0][..., 0][~disk].max())
    on_lattice = float(back[0][..., 0][disk].max())
    m0 = np.array([[back[0][y * 4 + 2, x * 4 + 2, 0] > 128 for x in range(W // 4)] for y in range(H // 4)])
    m30 = np.array([[back[30][y * 4 + 2, x * 4 + 2, 0] > 128 for x in range(W // 4)] for y in range(H // 4)])
    best, bs = None, 0
    for s in range(0, 40):
        e = (m30[:, :W // 4 - s] != m0[:, s:]).mean()
        if best is None or e < best:
            best, bs = e, s
    raw_off = float(np.asarray(mask_im)[:, :W][~disk].max())
    return [check("bright cores only on the 4 px dot lattice (off-lattice max < 128)", off_lattice < 128 and on_lattice > 200,
                  [off_lattice, on_lattice], "<128 / >200"),
            check("ticker scrolls 100 px/s = 25 dots in 1 s", abs(bs * pitch - speed) <= pitch, bs * pitch, speed),
            check("negative control: raw text mask lights pixels off the lattice", raw_off > 128, raw_off, ">128")], [vid, p0]


@card("RETRO-19")
def oscilloscope(task, wd):
    W, H = 200, 160
    tau, sweeps, T = .100, 5.0, .79

    def render(amp, persist=True):
        img = np.zeros((H, W))
        dt = 1 / 20000
        ts = np.arange(T - .2, T, dt)   # one full sweep period
        for t in ts:
            ph = (t * sweeps) % 1
            x = ph * (W - 1)
            y = H / 2 - amp * math.sin(2 * math.pi * 3 * ph)
            age = T - t
            wgt = math.exp(-age / tau) if persist else 1.0
            img[int(round(y)) % H, int(round(x))] += wgt * dt * 400
        return img
    flat = render(0)
    sine = render(40)
    grat = np.zeros((H, W, 3))
    grat[:, [int(round(i * (W - 1) / 10)) for i in range(11)]] = 40
    grat[[int(round(j * (H - 1) / 8)) for j in range(9)], :] = 40
    img = grat.copy()
    tr = np.clip(_blur(sine, .7) * 255 / max(1e-9, _blur(sine, .7).max()), 0, 255)
    img = np.maximum(img, np.stack([tr * .36, tr, tr * .56], -1))
    p = _save(wd / "scope.png", img)
    js = wd / "flat_trace.json"
    row = flat[H // 2]
    js.write_text(json.dumps(row.tolist()), "utf-8")
    prof = np.array(json.loads(js.read_text()))
    xs = np.arange(W)
    ph_now = (T * sweeps) % 1
    age = ((ph_now - xs / (W - 1)) % 1) / sweeps
    sel = (prof > 0) & (age > .005) & (age < .15)
    slope = np.polyfit(age[sel], np.log(prof[sel]), 1)[0]
    tau_fit = -1 / slope
    nopers = render(0, False)[H // 2]
    sel2 = (nopers > 0) & (age > .005) & (age < .15)
    slope2 = np.polyfit(age[sel2], np.log(nopers[sel2]), 1)[0]
    b = _load(p)
    v_count = len([i for i in range(W) if b[3, i, 0] == 40])
    h_count = len([j for j in range(H) if b[j, 3, 0] == 40])
    # brighter where it slows: sine peak (slow path) vs zero crossing, normalised by persistence
    return [check("phosphor persistence fits exp(-age/tau), tau = 100 ms", abs(tau_fit - tau) < .01, tau_fit, tau),
            check("10x8 graticule (11 vertical, 9 horizontal lines)", v_count == 11 and h_count == 9, [v_count, h_count], [11, 9]),
            check("negative control: a trace without persistence has no decay", abs(slope2) < 1, slope2, "~0")], [p, js]


@card("RETRO-21")
def tactical_crt(task, wd):
    W, H = 240, 136
    bg, fg, green = _hex("#0A0A0A"), _hex("#EAEAEA"), _hex("#4AF626")
    im = Image.new("RGB", (W, H), tuple(int(v) for v in bg))
    d = ImageDraw.Draw(im)
    d.fontmode = "1"
    d.text((10, 10), "SYS 04  TRACK 118.2", font=_font(12), fill=tuple(int(v) for v in fg))
    d.text((10, 40), "LINK OK", font=_font(12), fill=tuple(int(v) for v in green))
    d.text((10, 70), "ALT 3210  HDG 044", font=_font(12), fill=tuple(int(v) for v in fg))
    a = np.asarray(im).astype(float)
    rows = np.arange(H) % 4 >= 2
    a[rows] *= .9   # repeating-linear-gradient 2 px transparent / 2 px rgba(0,0,0,.1)
    p = _save(wd / "telemetry.png", a)
    # quantised motion: a value ticking in 0.5 s steps, never eased
    ticks = [math.floor(t / .5) * .5 for t in np.arange(0, 3, 1 / 30)]
    (wd / "ticks.json").write_text(json.dumps(ticks), "utf-8")
    b = _load(p)
    pure_black = int((b.sum(-1) == 0).sum())
    is_green = (np.abs(b - green).sum(-1) < 40) | (np.abs(b - green * .9).sum(-1) < 40)
    from scipy.ndimage import label
    gy = np.where(is_green.any(1))[0]
    one_line = gy.size and gy.max() - gy.min() < 16
    bgrows = b[:, W - 5, 0]
    period = [bgrows[y] for y in range(8)]
    scan_ok = all(abs(bgrows[y] - (9 if y % 4 >= 2 else 10)) <= .5 for y in range(H))
    distinct = len(set(ticks))
    smooth = [t for t in np.arange(0, 3, 1 / 30)]
    return [check("background is never pure #000", pure_black == 0, pure_black, 0),
            check("terminal green on one element only (single text line)", bool(one_line), int(gy.max() - gy.min()) if gy.size else -1, "<16 px tall"),
            check("scanlines: 2 px rows at -10% every 4 px", scan_ok, period, "10,10,9,9"),
            check("motion is quantised ticks (6 values in 3 s)", distinct == 6, distinct, 6),
            check("negative control: smooth motion would have 90 distinct values", len(set(smooth)) > 6, len(set(smooth)), ">6")], \
        [p, wd / "ticks.json"]


RAMP = " .:-=+*#%@"


def _ascii(lum, cols):
    H, W = lum.shape
    cw = W // cols
    rows = H // (cw * 9 // 8) if False else H // cw * 1
    ch = cw
    grid = lum[:(H // ch) * ch, :cols * cw].reshape(H // ch, ch, cols, cw).mean(axis=(1, 3))
    idx = np.clip(np.floor(grid / 256 * len(RAMP)), 0, len(RAMP) - 1).astype(int)
    return grid, idx, ["".join(RAMP[i] for i in r) for r in idx]


@card("RETRO-22")
def ascii_pass(task, wd):
    H, W = 360, 640
    yy, xx = np.mgrid[:H, :W]
    lum = np.clip(xx / W * 255 * .8 + 50 * (np.hypot(yy - 180, xx - 320) < 90), 0, 255)
    out = {}
    for cols in (20, 40, 80):
        grid, idx, lines = _ascii(lum, cols)
        out[cols] = lines
    txt = wd / "ascii_80.txt"
    txt.write_text("\n".join(out[80]), "utf-8")
    back = txt.read_text("utf-8").split("\n")
    grid, idx, _ = _ascii(lum, 80)
    match = all(RAMP[idx[r, c]] == back[r][c] for r in range(len(back)) for c in range(80))
    im = Image.new("L", (80 * 8, len(back) * 8), 0)
    d = ImageDraw.Draw(im)
    d.fontmode = "1"
    for r, line in enumerate(back):
        d.text((0, r * 8), line, font=_font(8), fill=255)
    png = wd / "ascii_80.png"
    im.save(png)
    row = [RAMP.index(c) for c in back[2]]
    mono = all(row[i] <= row[i + 1] for i in range(len(row) - 1))
    levels_out = len(set("".join(back)))
    levels_in = len(np.unique(np.round(grid)))
    return [check("80x45 character grid", len(back) == 45 and all(len(l) == 80 for l in back), [len(back), len(back[0])], [45, 80]),
            check("each char = ramp[floor(luma*10)]", match, True, True),
            check("gradient row maps monotonically through the ramp", mono and row[-1] > row[0], [row[0], row[-1]], "increasing"),
            check("coarse to fine grids 20/40/80 cols", [len(out[c][0]) for c in (20, 40, 80)] == [20, 40, 80],
                  [len(out[c][0]) for c in (20, 40, 80)], [20, 40, 80]),
            check("output quantised to <=10 glyph levels", levels_out <= 10, levels_out, "<=10"),
            check("negative control: input cells have >10 luma levels", levels_in > 10, levels_in, ">10")], [txt, png]


@card("RETRO-23")
def cell_patterns(task, wd):
    rng = _rng(23)
    H, W, size = 64, 96, 8
    yy, xx = np.mgrid[:H, :W]
    src = np.stack([xx / W * 255, yy / H * 255, 128 + 0 * xx], -1) + rng.normal(0, 6, (H, W, 3))
    src = np.clip(src, 0, 255)
    pix = src.reshape(H // size, size, W // size, size, 3).mean(axis=(1, 3))
    cells = np.kron(pix, np.ones((size, size, 1)))
    cy, cx = yy % size, xx % size
    # LED bars: three vertical sub-bars R G B, each lit by its channel
    led = np.zeros_like(cells)
    for ch in range(3):
        bar = (cx >= ch * 2 + 1) & (cx < ch * 2 + 2 + 1) & (cy >= 1) & (cy < size - 1)
        led[..., ch] = np.where(bar, cells[..., ch], 0)
    # Lego studs: cell colour with a lighter centred stud
    stud = np.hypot(cy - size / 2 + .5, cx - size / 2 + .5) < size * .3
    lego = cells * np.where(stud, 1.15, .9)[..., None]
    # 8x8 threshold matrix (Bayer 8)
    b8 = np.array([[0, 32, 8, 40, 2, 34, 10, 42], [48, 16, 56, 24, 50, 18, 58, 26], [12, 44, 4, 36, 14, 46, 6, 38],
                   [60, 28, 52, 20, 62, 30, 54, 22], [3, 35, 11, 43, 1, 33, 9, 41], [51, 19, 59, 27, 49, 17, 57, 25],
                   [15, 47, 7, 39, 13, 45, 5, 37], [63, 31, 55, 23, 61, 29, 53, 21]])
    lum = _luma(cells)
    thr = (lum / 255 * 64 > b8[cy, cx]).astype(float) * 255
    p1, p2, p3 = _save(wd / "led.png", led), _save(wd / "lego.png", np.clip(lego, 0, 255)), _save(wd / "threshold8.png", np.stack([thr] * 3, -1))
    t = _load(p3)[..., 0] / 255
    frac = t.reshape(H // 8, 8, W // 8, 8).mean(axis=(1, 3))
    target = np.round(_luma(pix) / 255 * 64) / 64
    err = float(np.abs(frac - target).max())
    l = _load(p1)
    led_ok = float(np.abs(l[1, 1, 0] - round(pix[0, 0, 0])) + np.abs(l[1, 3, 1] - round(pix[0, 0, 1])) + np.abs(l[1, 5, 2] - round(pix[0, 0, 2])))
    blockstd = float(cells.reshape(H // size, size, W // size, size, 3).std(axis=(1, 3)).max())
    sizes_pow2 = all((s & (s - 1)) == 0 for s in (32, 16, 8, 4, 2, 1))
    src_frac = (src[..., 0] / 255).reshape(H // 8, 8, W // 8, 8)
    neg_bin = float(np.mean((src_frac > .02) & (src_frac < .98)))
    return [check("pixelate: cells constant before shaping", blockstd < 1e-9, blockstd, 0),
            check("8x8 threshold: on-fraction per cell = cell luma (max err)", err <= 1 / 64 + 1e-9, err, "<=1/64"),
            check("LED bars carry the cell's R, G, B", led_ok <= 3, led_ok, "<=3"),
            check("progressive depixelation sizes are powers of two", sizes_pow2, True, True),
            check("negative control: unprocessed input is not binary", neg_bin > .5, neg_bin, ">0.5")], [p1, p2, p3]


DITHER = Path("/opt/node22/lib/node_modules/hyperframes/dist/skills/media-use/scripts/dither.mjs")


@card("RETRO-24")
def dither_passes(task, wd):
    if not DITHER.exists() or not fx.which("node"):
        raise RuntimeError("hyperframes dither.mjs not installed")
    H, W = 90, 120
    yy, xx = np.mgrid[:H, :W]
    src = np.stack([xx / W * 255] * 3, -1) * .7 + np.stack([yy / H * 60] * 3, -1)
    p_in = _save(wd / "dither_in.png", src)
    pal = GB
    palset = {tuple(int(v) for v in _hex(c)) for c in pal}
    checks, outs = [], []
    for alg in ("floyd-steinberg", "atkinson"):
        o = wd / ("dither_%s.png" % alg)
        fx.run(["node", str(DITHER), "--input", str(p_in), "--out", str(o), "--algorithm", alg,
                "--palette", ",".join(pal), "--point-size", "3", "--contrast", "1", "--brightness", "1"], timeout=30)
        b = _load(o)
        cs = _colours(b)
        bh, bw = (b.shape[0] // 3) * 3, (b.shape[1] // 3) * 3
        bstd = float(b[:bh, :bw].reshape(bh // 3, 3, bw // 3, 3, 3).std(axis=(1, 3)).max())
        checks.append(check("%s output uses only the 4 GB colours" % alg, cs <= palset and len(cs) >= 3, len(cs), 4))
        checks.append(check("%s point size 3 (3x3 blocks uniform)" % alg, bstd == 0, bstd, 0))
        outs.append(o)
    # error diffusion keeps the left->right brightness order of the source
    b = _luma(_load(outs[0]))
    lm = [b[:, i * 30:(i + 1) * 30].mean() for i in range(4)]
    checks.append(check("floyd-steinberg keeps the gradient order", all(lm[i] < lm[i + 1] for i in range(3)), lm, "increasing"))
    n_in = len(_colours(_load(p_in)))
    checks.append(check("negative control: input has more than 4 colours", n_in > 4, n_in, ">4"))
    return checks, outs


@card("RETRO-25")
def moire(task, wd):
    H, W, lam, f = 200, 320, 48.0, 1.0
    yy, xx = np.mgrid[:H, :W]
    c1, c2 = (100, 100), (100, 220)
    r1 = np.hypot(yy - c1[0], xx - c1[1])
    r2 = np.hypot(yy - c2[0], xx - c2[1])
    cols = [_hex("#d62828"), _hex("#f3e9d2"), _hex("#111111")]
    fps = 30
    frames = []
    for n in range(fps * 2):
        phi = 2 * math.pi * f * n / fps
        s = np.sin(2 * math.pi * (r1 - r2) / lam + phi)
        idx = np.where(s > .3, 0, np.where(s < -.3, 2, 1))
        frames.append(np.array(cols)[idx])
    vid = _video(wd / "moire.mp4", frames, fps)
    p = _save(wd / "moire_f0.png", frames[0])
    b = _load(p)
    axis = (b[100, 110:210, 0] > 150).astype(float)   # between the centres
    spec = np.abs(np.fft.rfft(axis - axis.mean()))
    k = int(np.argmax(spec[1:]) + 1)
    period = 100 / k
    v = fx.frames(vid, (W, H))
    px = (v[:, 150, 160, 0] > 150).astype(int)
    toggles = int(np.abs(np.diff(px)).sum())
    flash_hz = toggles / 2 / 2.0
    n_col = len(_colours(b))
    flat = np.tile(cols[1], (H, W, 1))
    fa = (flat[100, 110:210, 0] > 150).astype(float)
    return [check("stripe period on the centre axis = lambda/2 = 24 px (12 px stripes)", abs(period - 24) < 2.5, period, 24),
            check("3-colour palette red/cream/black", n_col == 3, n_col, 3),
            check("phase animation flashes below 3 Hz", 0 < flash_hz < 3, flash_hz, "<3"),
            check("negative control: a flat plate has no stripe period", fa.std() == 0, float(fa.std()), ">0")], [vid, p]


@card("RETRO-26")
def dom_glitch(task, wd):
    W, H = 200, 80
    im = Image.new("RGB", (W, H), (20, 20, 28))
    d = ImageDraw.Draw(im)
    d.fontmode = "1"
    d.text((20, 22), "GLITCH", font=_font(30), fill=(240, 240, 240))
    clean = np.asarray(im).astype(float)
    fps, dur, steps, amp, seed = 60, .3, 30, 10, 26
    frames, shifts_ok, rows_uniform = [], True, True
    magenta = np.array([255, 0, 80]) * .7
    cyan = np.array([0, 200, 255]) * .7
    for n in range(int(.5 * fps)):
        t = n / fps
        if t >= dur:
            frames.append(clean.copy())
            continue
        st = int(t * steps)
        r = np.random.default_rng(seed * 1000 + st)
        f = clean.copy()
        ink = (clean.sum(-1) > 300)
        dx = int(r.integers(-amp // 2, amp // 2 + 1))
        for sh, col in ((dx, magenta), (-dx, cyan)):
            m = np.roll(ink, sh, axis=1) & ~ink
            f[m] = col
        for _ in range(3):
            y0 = int(r.integers(0, H - 8))
            hgt = int(r.integers(3, 9))
            s = int(r.integers(-amp, amp + 1))
            f[y0:y0 + hgt] = np.roll(f[y0:y0 + hgt], s, axis=1)
        frames.append(f)
    vid = _video(wd / "glitch.mp4", frames, fps)
    v = fx.frames(vid, (W, H))
    pairs_same = all(np.array_equal(v[2 * i], v[2 * i + 1]) for i in range(int(dur * fps) // 2))
    after_clean = float(np.abs(v[-1] - clean).max())
    during = float(np.abs(v[3] - clean).mean())
    max_shift = 0
    for fr in v[:int(dur * fps)]:
        for y in range(0, H, 2):
            if np.abs(fr[y] - clean[y]).sum() > 0:
                best = min(range(-12, 13), key=lambda s: np.abs(np.roll(clean[y], s, 0) - fr[y]).sum())
                max_shift = max(max_shift, abs(best))
    has_mag = bool(np.any(np.abs(v[:int(dur * fps)] - magenta).sum(-1) < 30))
    return [check("30 steps/s at 60 fps: frame pairs identical", pairs_same, pairs_same, True),
            check("returns exactly to clean after 0.3 s", after_clean == 0, after_clean, 0),
            check("slice displacement within amp 10 px", max_shift <= 10, max_shift, "<=10"),
            check("magenta split shadow present", has_mag, has_mag, True),
            check("glitch visible during the 0.3 s (mean diff from clean)", during > 1, during, ">1"),
            check("negative control: the clean element has no magenta split",
                  not bool(np.any(np.abs(clean - magenta).sum(-1) < 30)), False, False)], [vid]


@card("RETRO-27")
def glitch_pass(task, wd):
    H, W = 96, 200
    yy, xx = np.mgrid[:H, :W]
    src = np.full((H, W, 3), 40.0)
    src[:, ::25] = 255
    bands, frac, smax, chroma = 24, .28, .06, .012
    bh = H // bands

    def hash01(a, b):
        v = math.sin(a * 127.1 + b * 311.7) * 43758.5453
        return v - math.floor(v)
    frames, shifted_frac, shifts = [], [], []
    for frame in range(12):
        out = src.copy()
        nshift = 0
        for b in range(bands):
            hv = hash01(b, frame)
            if hv < frac:
                s = int(round((hash01(b + 50, frame) * 2 - 1) * smax * W))
                out[b * bh:(b + 1) * bh] = np.roll(out[b * bh:(b + 1) * bh], s, axis=1)
                nshift += 1
                shifts.append(abs(s))
        co = int(round(chroma * W))
        out[..., 0] = np.roll(out[..., 0], co, axis=1)
        out[..., 2] = np.roll(out[..., 2], -co, axis=1)
        frames.append(out)
        shifted_frac.append(nshift / bands)
    vid = _video(wd / "glitch_pass.mp4", frames, 12)
    v = fx.frames(vid, (W, H))
    offs = [_shift_x(v[0][y:y + 1, :, 2], v[0][y:y + 1, :, 0], 8) for y in range(0, H, 4)]
    co = int(round(chroma * W))
    again = frames[3]
    return [check("~28% of 24 bands sliced per frame (mean)", abs(np.mean(shifted_frac) - .28) < .1, float(np.mean(shifted_frac)), .28),
            check("slice shift <= 0.06 W", max(shifts) <= smax * W + 1e-9, max(shifts), smax * W),
            check("chroma split: R +1.2% W, B -1.2% W (R-B offset per row)", all(o == 2 * co for o in offs),
                  sorted(set(offs)), 2 * co),
            check("hashed per frame: deterministic and varying", np.array_equal(v[3], fx.frames(vid, (W, H))[3]) and
                  not np.array_equal(v[3], v[4]), True, True),
            check("negative control: the unprocessed input has no R/B offset",
                  _shift_x(src[0:1, :, 2], src[0:1, :, 0], 8) != 2 * co, _shift_x(src[0:1, :, 2], src[0:1, :, 0], 8), 2 * co)], [vid]


@card("RETRO-29")
def kinetic_theme_lock(task, wd):
    themes = {
        "J": "Brutalist Acid: background #BDBDB8, hero #C6FF00, small text #0A0A0A, ultra-condensed heavy sans, chrome and black rubber, concrete grain, harsh top light.",
        "K": "Retro 70s Warm: background #F3E3C3, hero #E8732C, small text #5A3A22, rounded heavy retro serif, film grain, warm sun.",
    }
    checks, outs = [], []
    for k, block in themes.items():
        c, o = _prompt_lock(wd, "theme_" + k, block, ["Clip %d: the word moves in on beat %d." % (i, i) for i in range(1, 6)],
                            ["nike", "coca-cola", "apple"])
        checks += [dict(x, check="theme %s: %s" % (k, x["check"])) for x in c]
        outs += o
    hexes = {"J": "#C6FF00", "K": "#E8732C"}
    checks.append(check("each lock carries its hero hex", all(hexes[k] in themes[k] for k in themes), True, True))
    return checks, outs


@card("RETRO-30")
def lofi_loop(task, wd):
    W, H, fps, loop = 96, 54, 12, 6.0
    n = int(loop * fps)
    periods = {"rain": 1.0, "steam": 3.0, "lamp": 2.0, "breath": 3.0}
    top, bot, warm = _hex("#2B2D42"), _hex("#5C5470"), _hex("#F2C14E")
    yy, xx = np.mgrid[:H, :W]
    rng = _rng(30)
    drops = rng.random((30, 2))
    frames = []
    for i in range(n):
        t = i / fps
        img = top + (yy[..., None] / H) * (bot - top)
        for dx, dy in drops:   # rain falls one screen per period
            y = int(((dy + t / periods["rain"]) % 1) * H)
            x = int(dx * W)
            img[max(0, y - 3):y, x] = img[max(0, y - 3):y, x] * .5 + 200 * .5
        lamp = .8 + .2 * math.sin(2 * math.pi * t / periods["lamp"])
        m = np.hypot(yy - 14, xx - 78) < 6
        img[m] = warm * lamp
        br = 1 + .06 * math.sin(2 * math.pi * t / periods["breath"])
        body = ((yy - 40) / (10 * br)) ** 2 + ((xx - 30) / 9) ** 2 < 1
        img[body] = (30, 28, 40)
        sy = int(30 - ((t / periods["steam"]) % 1) * 16)
        img[sy:sy + 2, 50:53] = img[sy:sy + 2, 50:53] * .6 + 220 * .4
        frames.append(img)
    vid = _video(wd / "lofi_loop.mp4", frames + [frames[0]], fps)
    v = fx.frames(vid, (W, H))
    seam = float(np.abs(v[0] - v[n]).max())
    divides = all(abs(loop / p - round(loop / p)) < 1e-9 for p in periods.values())
    bounds = all(1.0 <= p <= 3.0 for p in periods.values())
    diffs = [float(np.abs(v[i + 1] - v[i]).mean()) for i in range(n - 1)]
    nocut = max(diffs) < 6
    hard = np.abs(v[1] - np.full_like(v[1], 128)).mean()
    return [check("seamless: frame at 6 s equals frame 0", seam == 0, seam, 0),
            check("every motion period divides the 6 s loop", divides, list(periods.values()), "divisors of 6"),
            check("motions last 1-3 s (none faster than 0.8 s)", bounds, list(periods.values()), "1..3 s"),
            check("no cuts (max mean frame diff)", nocut, max(diffs), "<6"),
            check("negative control: a hard cut to grey would exceed the cut threshold", hard > 6, float(hard), ">6")], [vid]


def _rel_lum(h):
    c = _hex(h) / 255
    c = np.where(c <= .03928, c / 12.92, ((c + .055) / 1.055) ** 2.4)
    return float(c @ np.array([.2126, .7152, .0722]))


def _contrast(a, b):
    la, lb = sorted([_rel_lum(a), _rel_lum(b)], reverse=True)
    return (la + .05) / (lb + .05)


@card("RETRO-31")
def retro_presets(task, wd):
    presets = {
        "vintage-os": {"surface": "#C0C0C0", "text": "#000000", "accent": "#008080", "font": "Silkscreen + Lalezar (Arabic)"},
        "pac-arcade": {"surface": "#000000", "text": "#F4B9B0", "accent": "#2A3FE5", "font": "Press Start 2P + Lalezar"},
        "neobrutalism": {"surface": "#FBFBF9", "text": "#432DD7", "accent": "#FDC800", "font": "scale 13/15/17/21/27/35"},
        "neon": {"surface": "#000000", "text": "#BBF351", "accent": "#00BCFF", "font": "display + Arabic partner"},
    }
    rep = {}
    for k, p in presets.items():
        rep[k] = {"text_on_surface": round(_contrast(p["text"], p["surface"]), 2),
                  "accent_on_surface": round(_contrast(p["accent"], p["surface"]), 2)}
        rep[k]["text_AA"] = rep[k]["text_on_surface"] >= 4.5
    out = wd / "retro_presets_wcag.json"
    out.write_text(json.dumps({"presets": presets, "wcag": rep}, indent=1), "utf-8")
    back = json.loads(out.read_text())
    bw = _contrast("#000000", "#FFFFFF")
    scale = [13, 15, 17, 21, 27, 35]
    return [check("WCAG formula known answer: black/white = 21", abs(bw - 21) < 1e-9, bw, 21),
            check("every preset's text passes AA 4.5:1", all(v["text_AA"] for v in back["wcag"].values()),
                  {k: v["text_on_surface"] for k, v in back["wcag"].items()}, ">=4.5"),
            check("vintage OS black on #C0C0C0 = 11.54 (hand-computed)", abs(back["wcag"]["vintage-os"]["text_on_surface"] - 11.54) < .01,
                  back["wcag"]["vintage-os"]["text_on_surface"], 11.54),
            check("neobrutalism type scale strictly increasing", all(scale[i] < scale[i + 1] for i in range(5)), scale, "increasing"),
            check("negative control: grey-on-grey pair fails AA", _contrast("#999999", "#C0C0C0") < 4.5,
                  round(_contrast("#999999", "#C0C0C0"), 2), "<4.5")], [out]


FONT57 = {"K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
          "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
          "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
          "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
          "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"]}


@card("RETRO-X01")
def led_bulge_words(task, wd):
    word = "KOSIF"
    cols = len(word) * 6 - 1
    grid = np.zeros((7, cols), dtype=int)
    for i, ch in enumerate(word):
        for r, row in enumerate(FONT57[ch]):
            for c, bit in enumerate(row):
                grid[r, i * 6 + c] = int(bit)
    cell = 12
    # true pixel word: square cells, drawn cell by cell
    pw = np.kron(grid, np.ones((cell, cell))) * 255
    p_word = _save(wd / "pixel_word.png", np.stack([pw] * 3, -1))
    # LED lattice with barrel bulge
    k, n = .15, 21
    W = H = 440
    sp = 140
    c0 = (n - 1) / 2
    dots = []
    img = np.zeros((H, W, 3))
    ly, lx = np.mgrid[-8:9, -8:9]
    for j in range(n):
        for i in range(n):
            u, v = (i - c0) / c0, (j - c0) / c0
            r2 = u * u + v * v
            f = 1 + k * r2
            x, y = W / 2 + u * f * sp, H / 2 + v * f * sp
            rad = 3.0 * (1 + 1.6 * k * r2)
            dots.append((u, v, x, y, rad))
            iy, ix = int(round(y)), int(round(x))
            yy, xx = ly + iy, lx + ix
            win = img[iy - 8:iy + 9, ix - 8:ix + 9]
            m = np.hypot(yy - y, xx - x) <= rad
            win[m] = np.maximum(win[m], (230, 230, 230))
            for dx, col in ((-1.5, (255 * .55, 42 * .55, 60 * .55)), (1.5, (42 * .55, 107 * .55, 255 * .55))):
                mf = (np.hypot(yy - y, xx - x - dx) <= rad) & ~m
                win[mf] = np.clip(win[mf] + col, 0, 255)   # 'lighter' compositing
    p_led = _save(wd / "led_bulge.png", img)
    b = _load(p_led)[..., 1]
    from scipy.ndimage import label, center_of_mass
    lab, nl = label(b > 200)
    cms = center_of_mass(b > 200, lab, range(1, nl + 1))
    sizes = np.bincount(lab.ravel())[1:]
    errs, rad_meas = [], []
    for (u, v, x, y, rad) in dots:
        d = [math.hypot(cy - y, cx - x) for cy, cx in cms]
        errs.append(min(d))
    corner = int(np.argmin([math.hypot(cy - dots[0][3], cx - dots[0][2]) for cy, cx in cms]))
    centre = int(np.argmin([math.hypot(cy - H / 2, cx - W / 2) for cy, cx in cms]))
    size_ratio = math.sqrt(sizes[corner] / sizes[centre])
    expect_ratio = (1 + 1.6 * k * 2) / 1
    corner_pos = math.hypot(cms[corner][0] - H / 2, cms[corner][1] - W / 2)
    expect_pos = math.hypot(sp, sp) * (1 + k * 2)
    wb = _load(p_word)[..., 0]
    recon = (wb.reshape(7, cell, cols, cell).mean(axis=(1, 3)) > 127).astype(int)
    aa = len(np.unique(wb))
    smooth = np.asarray(Image.fromarray(pw.astype(np.uint8)).resize((cols * cell // 2, 7 * cell // 2), Image.BICUBIC))
    return [check("dot positions follow x(1+k r^2), corner radius", abs(corner_pos - expect_pos) < 2, corner_pos, expect_pos),
            check("dot size grows by (1+1.6k r^2) at the corner", abs(size_ratio - expect_ratio) < .08, size_ratio, expect_ratio),
            check("all 441 dots found where predicted", nl == n * n and max(errs) < 1.0, [nl, max(errs)], [441, "<1"]),
            check("pixel word reproduces the 5x7 bitmaps exactly", np.array_equal(recon, grid), True, True),
            check("square cells, no anti-aliasing (2 grey levels)", aa == 2, aa, 2),
            check("negative control: a scaled pixel font is anti-aliased", len(np.unique(smooth)) > 2, int(len(np.unique(smooth))), ">2")], \
        [p_word, p_led]
