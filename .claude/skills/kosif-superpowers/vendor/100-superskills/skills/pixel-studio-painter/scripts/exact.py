"""Exact redraw: an image is painted from nothing, the way a painter works, and ends identical to the original,
pixel for pixel (red, green, blue and transparency).

  1. blocking in    - the big shapes in a few flat colours (a logo's own colours; a photo's main tones)
  2. refining       - photos only: more tones, painted shadows -> mid-tones -> lights
  3. final touches  - every pixel that still differs gets its exact original value, the most visible first:
                      visible details, then fine corrections, then changes the eye cannot see (almost no time)

For photos the plan (how many colours to block in, how many tones to refine) is chosen by Jev from measured
candidates; if Jev cannot be reached a deterministic rule chooses. Everything happens at the image's own
resolution; nothing is resampled.
"""
from __future__ import annotations

import cv2
import numpy as np
from PIL import Image

import render as R
import vectorize as V

PLANS = {"A": (6, 32), "B": (10, 64), "C": (16, 96), "D": (24, 128)}      # block-in colours, refining tones
DEFAULT = "B"


def load_rgba(path) -> np.ndarray:
    im = Image.open(path)
    im.load()
    return np.ascontiguousarray(np.asarray(im.convert("RGBA")))


def _kmeans(lab: np.ndarray, k: int, seed: int = 0, attempts: int = 2, cap: int = 60000):
    sample = lab
    if len(sample) > cap:
        sample = sample[np.random.default_rng(seed).choice(len(sample), cap, replace=False)]
    k = max(1, min(k, len(np.unique(sample, axis=0))))
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 40, 0.3)
    _, _, centres = cv2.kmeans(sample.astype(np.float32), k, None, crit, attempts, cv2.KMEANS_PP_CENTERS)
    labels = np.concatenate([((lab[i:i + 60000, None] - centres[None]) ** 2).sum(-1).argmin(1)
                             for i in range(0, len(lab), 60000)])
    return centres, labels


def _lab(rgb: np.ndarray) -> np.ndarray:
    """8-bit OpenCV Lab (for clustering)."""
    return cv2.cvtColor(np.ascontiguousarray(rgb), cv2.COLOR_RGB2LAB).reshape(-1, 3).astype(np.float32)


def _lab_true(rgb: np.ndarray) -> np.ndarray:
    """CIE Lab in real units (L 0..100), for colour differences the eye can judge (ΔE)."""
    f = np.ascontiguousarray(rgb.reshape(-1, 1, 3)).astype(np.float32) / 255
    return cv2.cvtColor(f, cv2.COLOR_RGB2LAB).reshape(-1, 3)


def _rgb_of_lab(centres: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(np.clip(centres, 0, 255).astype(np.uint8)[None], cv2.COLOR_LAB2RGB)[0]


def delta_e(a_rgba: np.ndarray, b_rgba: np.ndarray) -> np.ndarray:
    """Visible difference per pixel: CIE76 ΔE on colour, plus a transparency difference counted the same way."""
    a, b = a_rgba.reshape(-1, 4), b_rgba.reshape(-1, 4)
    de = np.linalg.norm(_lab_true(a[:, :3]) - _lab_true(b[:, :3]), axis=1)
    return de + np.abs(a[:, 3].astype(np.float32) - b[:, 3]) / 2.55


def _stages(rgba: np.ndarray, block_k: int, fine_k: int, quick: bool = False):
    """The blocking-in map and the refined picture, shared by the plan and by its measured candidates."""
    H, W = rgba.shape[:2]
    visible = rgba.reshape(-1, 4)[:, 3] > 0
    photo = V.looks_like_photo(rgba)
    if photo:
        smooth = cv2.bilateralFilter(np.ascontiguousarray(rgba[..., :3]), 9, 40, 9)
        centres, labels = _kmeans(_lab(smooth)[visible], block_k, attempts=1 if quick else 2)
        lab_map = np.full(H * W, 255, np.uint8)
        lab_map[visible] = labels
        lab_map = cv2.medianBlur(lab_map.reshape(H, W), 5).reshape(-1).astype(np.int32)
        lab_map[(lab_map == 255) | ~visible] = -1
        pal = _rgb_of_lab(centres)
    else:
        P = np.array(V._palette(rgba), np.float32)
        lab_map = V._memberships(rgba, P).argmax(0).reshape(-1).astype(np.int32)
        lab_map[(lab_map == len(P)) | ~visible] = -1
        pal = np.clip(np.round(P), 0, 255).astype(np.uint8)
    fine = None
    if photo:
        lab_all = _lab(rgba[..., :3])
        centres, labels = _kmeans(lab_all[visible], fine_k, seed=1, attempts=1 if quick else 2,
                                  cap=15000 if quick else 60000)
        fine = np.zeros((H * W, 4), np.uint8)
        fine[visible, :3] = _rgb_of_lab(centres)[labels]
        fine[visible, 3] = 255
    return {"photo": photo, "lab_map": lab_map, "pal": pal, "fine": fine, "visible": visible}


def candidates(rgba: np.ndarray, side: int = 240) -> dict:
    """Measure every plan on a reduced copy: how close the first impression is, how close refining gets, and how
    many pixels would still be visibly off before the exact pass."""
    im = Image.fromarray(rgba, "RGBA")
    if max(im.size) > side:
        f = side / max(im.size)
        im = im.resize((max(1, round(im.width * f)), max(1, round(im.height * f))), Image.LANCZOS)
    small = np.asarray(im).copy()
    target = small.reshape(-1, 4)
    out = {}
    for name, (bk, fk) in PLANS.items():
        st = _stages(small, bk, fk, quick=True)
        block = np.zeros_like(target)
        ok = st["lab_map"] >= 0
        block[ok, :3] = st["pal"][st["lab_map"][ok]]
        block[ok, 3] = 255
        de_block = delta_e(block, target)[st["visible"]]
        refined = block.copy()
        if st["fine"] is not None:
            move = np.abs(st["fine"].astype(np.int16) - block.astype(np.int16)).sum(1) > 12
            refined[move] = st["fine"][move]
        de_fine = delta_e(refined, target)[st["visible"]]
        layers = int(len(np.unique(st["lab_map"][ok])))
        out[name] = {"block_colours": bk, "refine_tones": fk, "first_impression_dE": round(float(de_block.mean()), 1),
                     "refined_dE": round(float(de_fine.mean()), 1),
                     "visibly_off_pct": round(float((de_fine > 10).mean() * 100), 1), "steps": layers + 3 + 3}
    return out


def choose_plan(rgba: np.ndarray):
    """(block_k, fine_k, info). Photos: Jev picks among measured plans (two orderings, averaged); logos keep their
    own colours, so there is nothing to choose."""
    if not V.looks_like_photo(rgba):
        return 12, 64, None
    import jev_client
    cands = candidates(rgba)
    h, w = rgba.shape[:2]
    options = {f"plan_{n}": (f"{c['block_colours']} colours to block in (first impression ΔE {c['first_impression_dE']}), "
                             f"{c['refine_tones']} tones to refine (ΔE {c['refined_dE']}), {c['visibly_off_pct']}% of "
                             f"pixels still visibly off before the exact pass, about {c['steps']} steps")
               for n, c in cands.items()}
    state = {"image": f"{w}x{h} photograph", "goal": "redraw it from a blank canvas so that it ends identical to the "
             "original; the drawing should read like a painter's progress", **options}
    q = ("Which painting plan redraws this image most like a skilled painter - recognisable big shapes first, then "
         "steady refinement - and leaves the fewest visible corrections for the final exact pass?")
    res = jev_client.choose(q, state, options)
    # the rule used when Jev is unreachable: fewest visible corrections, each extra step costing a little
    rule = min(cands, key=lambda n: cands[n]["visibly_off_pct"] + 0.4 * cands[n]["steps"])
    pick = res["choice"].removeprefix("plan_") if res else rule
    info = {"by": "jev" if res else "rule", "choice": pick, "rule_choice": rule, "candidates": cands,
            "probabilities": {k.removeprefix("plan_"): v for k, v in res["probabilities"].items()} if res else None,
            "stable": res["stable"] if res else None, "latency_s": res["latency_s"] if res else None}
    bk, fk = PLANS[pick]
    return bk, fk, info


def plan(rgba: np.ndarray, block_k: int = 10, fine_k: int = 64):
    """Yield paint jobs (label, order, origin, weight, idx, cols RGBA). idx are flat pixel indices sorted in painting
    order. After the last job the canvas equals rgba exactly."""
    H, W = rgba.shape[:2]
    target = rgba.reshape(-1, 4)
    cur = np.zeros_like(target)                       # a blank, transparent sheet
    count = 0

    def order(label: str, idx: np.ndarray, kind: str):
        nonlocal count
        origin = (float((idx % W).mean()), float((idx // W).mean())) if kind == "grow" else None
        o = R.reveal_order(idx.astype(np.int32), W, R.Step(label, [], kind, origin), 1.0, seed=count)
        count += 1
        return o, origin

    st = _stages(rgba, block_k, fine_k)
    lab_map, pal, visible = st["lab_map"], st["pal"], st["visible"]
    # 1. blocking in
    for area, k in sorted(((int((lab_map == k).sum()), k) for k in range(len(pal))), reverse=True):
        if not area:
            continue
        label = f"الكتلة: اللون {V.name_ar(pal[k])}"
        o, origin = order(label, np.flatnonzero(lab_map == k), "grow")
        cols = np.repeat(np.append(pal[k], 255).astype(np.uint8)[None], o.size, 0)
        cur[o] = cols
        yield label, "grow", origin, .9, o, cols

    # 2. refining (photos): shadows, mid-tones, lights
    fine = st["fine"]
    if fine is not None:
        diff = visible & (np.abs(fine.astype(np.int16) - cur.astype(np.int16)).sum(1) > 12)
        if diff.any():
            lum = _lab(rgba[..., :3])[:, 0]
            cut = np.quantile(lum[diff], [1 / 3, 2 / 3])
            for b, label in enumerate(("الظلال", "الألوان المتوسطة", "الأضواء")):
                sel = diff & (lum >= (cut[b - 1] if b else -1)) & (lum < (cut[b] if b < 2 else 999))
                idx = np.flatnonzero(sel)
                if idx.size:
                    o, origin = order(label, idx, "sparkle")
                    cur[o] = fine[o]
                    yield label, "sparkle", origin, .7, o, fine[o]

    # 3. final touches, the most visible first; time follows visibility
    diff = np.flatnonzero(np.any(cur != target, axis=1))
    if diff.size:
        de = delta_e(cur[diff], target[diff])
        for lo, hi, label, kind, weight in ((12, 1e9, "اللمسات الدقيقة: التفاصيل الظاهرة", "sweep", 1.2),
                                            (4, 12, "اللمسات الدقيقة: تصحيحات خفيفة", "sparkle", .4),
                                            (-1, 4, "اللمسات الدقيقة: فروق لا تراها العين", "sparkle", .12)):
            idx = diff[(de >= lo) & (de < hi)]
            if idx.size:
                o, origin = order(label, idx, kind)
                cur[o] = target[o]
                yield label, kind, origin, weight, o, target[o]
    assert np.array_equal(cur, target), "exact redraw did not reach the original"


def mismatches(canvas: np.ndarray, rgba: np.ndarray) -> int:
    """How many pixels differ (any of R, G, B, A)."""
    return int(np.any(canvas.reshape(-1, 4) != rgba.reshape(-1, 4), axis=1).sum())
