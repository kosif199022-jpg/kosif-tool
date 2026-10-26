"""Turn an image (a logo, an icon, flat artwork) into a vector picture program.

1. Pick the image's pure colours. Antialiased in-between colours along edges are recognised as mixtures and
   skipped.
2. Enlarge the image 8x smoothly and give every fine pixel its nearest pure colour. Because the source's
   antialiasing becomes smooth boundaries, the edges come out as curves, not stair steps.
3. Trace each colour region's outline, holes included, with OpenCV, and simplify it into polygons.
4. Stack the layers largest first, each grown by a hair, so neighbours overlap and no seams show between them.

The result is pure vector data: it renders crisp at any size and is also written out as an SVG.
"""
from __future__ import annotations

import colorsys
import json
import math
from pathlib import Path

import cv2
import numpy as np
from PIL import Image


def _edge_blends(rgb: np.ndarray) -> np.ndarray:
    """True where a pixel is antialiasing: its colour lies between two OPPOSITE neighbours of clearly different
    colours. A grey letter on white is not a blend (no black next to it); a grey pixel between black and white is."""
    c = rgb.astype(np.float32)
    H, W = c.shape[:2]
    R = 1                                   # 3-colour blends in sub-pixel gaps are caught later, in _palette
    pad = np.pad(c, ((R, R), (R, R), (0, 0)), mode="edge")
    out = np.zeros((H, W), bool)
    dirs = [((-1, 0), (1, 0)), ((0, -1), (0, 1)), ((-1, -1), (1, 1)), ((-1, 1), (1, -1))]
    for k in range(1, R + 1):
        for (y1, x1), (y2, x2) in dirs:
            p = pad[R + k * y1:R + k * y1 + H, R + k * x1:R + k * x1 + W]
            q = pad[R + k * y2:R + k * y2 + H, R + k * x2:R + k * x2 + W]
            d = q - p
            dd = (d * d).sum(-1)
            t = ((c - p) * d).sum(-1) / np.maximum(dd, 1e-6)
            dist = np.sqrt(((c - (p + t[..., None] * d)) ** 2).sum(-1))
            out |= (dd > 40 ** 2) & (t > .08) & (t < .92) & (dist < 18)
    return out


def _palette(rgba: np.ndarray, max_colors: int = 16, min_share: float = 0.001) -> list[np.ndarray]:
    """The image's real colours: most frequent first, from fully opaque pixels that are not edge blends; each
    colour is the mean of the pixels it stands for (not a bin centre), so flat areas come back exact."""
    opaque = rgba[..., 3] >= 200
    rgb = rgba[..., :3]
    pure = rgb[opaque & ~_edge_blends(rgb)].astype(np.float32)
    if not len(pure):
        pure = rgb[opaque].astype(np.float32)
    q = (pure // 8).astype(np.int32)
    keys, inv, counts = np.unique(q, axis=0, return_inverse=True, return_counts=True)
    inv = inv.ravel()
    total, cands = opaque.sum(), []
    for i in np.argsort(-counts):
        if counts[i] < total * min_share or len(cands) >= max_colors + 8:
            break
        c = pure[inv == i].mean(0)
        if all(np.linalg.norm(c - p) >= 30 for p in cands):
            near = pure[np.linalg.norm(pure - c, axis=1) < 22]    # mean of everything close to the pick
            cands.append(near.mean(0) if len(near) else c)

    # A candidate that can be mixed from 2-3 stronger colours, and whose pixels mostly sit right next to those very
    # colours, is an edge blend (e.g. pink in a sub-pixel gap between red and white). Grey letters on white survive:
    # grey mixes from black and white, but there is no black beside them.
    img = rgb.astype(np.float32)
    kernel = np.ones((5, 5), np.uint8)
    near_mask = lambda c: (np.linalg.norm(img - c, axis=-1) < 26) & opaque  # noqa: E731
    accepted: list[np.ndarray] = []
    for c in cands:
        parents = _mixture(c, accepted)
        if parents is not None:
            own = near_mask(c)
            close = np.ones_like(own)
            for p in parents:
                close &= cv2.dilate(near_mask(accepted[p]).astype(np.uint8), kernel).astype(bool)
            if own.sum() and (own & close).sum() / own.sum() > 0.5:
                continue
        accepted.append(c)
        if len(accepted) >= max_colors:
            break
    return accepted


def _mixture(c: np.ndarray, cols: list[np.ndarray], tol: float = 16.0):
    """Indices of 2 or 3 colours whose blend reproduces c (weights 6-94%), or None."""
    from itertools import combinations
    best = None
    for r in (2, 3):
        for idx in combinations(range(len(cols)), r):
            A = np.stack([cols[i] for i in idx], 1)            # 3 x r
            M = np.vstack([A, np.full((1, r), 255.0)])         # weights must sum to 1 (weighted row)
            w, *_ = np.linalg.lstsq(M, np.append(c, 255.0), rcond=None)
            if np.all(w > .06) and np.all(w < .94):
                err = np.linalg.norm(A @ w - c)
                if err < tol and (best is None or err < best[0]):
                    best = (err, idx)
        if best:
            return best[1]
    return None


def name_ar(c) -> str:
    """A rough Arabic colour name, for the step labels."""
    r, g, b = (float(v) / 255 for v in c)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    h *= 360
    if s < .14 or v < .12:
        return "الأبيض" if v > .9 else "الرمادي الفاتح" if v > .65 else "الرمادي" if v > .3 else "الأسود"
    if v > .85 and s < .3:
        return "الكريمي" if 20 < h < 90 else "الوردي الفاتح" if h < 20 or h > 300 else "الفاتح"
    if h < 15 or h >= 340:
        return "الأحمر" if v > .55 else "الأحمر الداكن"
    if h < 45:
        return "البرتقالي" if v > .6 else "البني"
    if h < 62:
        return "الأصفر" if v > .7 else "الزيتي"
    if h < 165:
        return "الأخضر الفاتح" if v > .65 and h < 95 else "الأخضر الزيتي" if h < 95 else "الأخضر" if v > .5 else "الأخضر الداكن"
    if h < 260:
        return "الأزرق"
    return "البنفسجي" if h < 300 else "الوردي"


def _memberships(rgba: np.ndarray, P: np.ndarray, margin: float = 14.0) -> np.ndarray:
    """How much of each palette colour every source pixel holds. A pixel close to one colour is that colour; an
    edge pixel is split between the two colours it blends (red/white 40:60), never handed to a third colour that
    merely sits nearby in colour space (grey between red and white). The last channel is transparency."""
    c = rgba[..., :3].astype(np.float32)
    alpha = rgba[..., 3].astype(np.float32) / 255
    H, W = alpha.shape
    K = len(P)
    d1 = np.linalg.norm(c[..., None, :] - P[None, None], axis=-1)
    best1, dist1 = d1.argmin(-1), d1.min(-1)
    dist2 = np.full((H, W), np.inf, np.float32)
    bi, bj, bt = np.zeros((H, W), int), np.zeros((H, W), int), np.zeros((H, W), np.float32)
    for i in range(K):
        for j in range(i + 1, K):
            d = P[j] - P[i]
            t = np.clip(((c - P[i]) @ d) / float(d @ d), 0, 1)
            dist = np.linalg.norm(c - (P[i] + t[..., None] * d), axis=-1)
            better = dist < dist2
            dist2[better], bi[better], bj[better], bt[better] = dist[better], i, j, t[better]
    m = np.zeros((K + 1, H, W), np.float32)
    yy, xx = np.mgrid[:H, :W]
    pure = dist1 <= dist2 + margin
    m[best1[pure], yy[pure], xx[pure]] = 1
    b = ~pure
    np.add.at(m, (bi[b], yy[b], xx[b]), 1 - bt[b])
    np.add.at(m, (bj[b], yy[b], xx[b]), bt[b])
    m[:K] *= alpha
    m[K] = 1 - alpha
    return m


def looks_like_photo(rgba: np.ndarray) -> bool:
    """Photos and paintings have thousands of distinct colours; logos, icons and flat art have a few hundred."""
    small = np.asarray(Image.fromarray(rgba).convert("RGB").resize((200, 200), Image.BILINEAR))
    return len(np.unique((small // 8).reshape(-1, 3), axis=0)) > 1200


def _photo_memberships(rgba: np.ndarray, k: int):
    """For photos: smooth the texture but keep the edges, then group the colours into k (k-means in Lab)."""
    rgb = np.ascontiguousarray(rgba[..., :3])
    alpha = rgba[..., 3].astype(np.float32) / 255
    H, W = alpha.shape
    flat = cv2.bilateralFilter(rgb, 9, 40, 9)
    lab = cv2.cvtColor(flat, cv2.COLOR_RGB2LAB).reshape(-1, 3).astype(np.float32)
    opaque = (rgba[..., 3] >= 128).reshape(-1)
    sample = lab[opaque]
    if len(sample) > 60000:
        sample = sample[np.random.default_rng(0).choice(len(sample), 60000, replace=False)]
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 40, 0.3)
    _, _, centres = cv2.kmeans(sample, k, None, crit, 3, cv2.KMEANS_PP_CENTERS)
    labels = np.concatenate([((lab[i:i + 50000, None] - centres[None]) ** 2).sum(-1).argmin(1)
                             for i in range(0, len(lab), 50000)]).reshape(H, W)
    pal = cv2.cvtColor(np.clip(centres, 0, 255).astype(np.uint8)[None], cv2.COLOR_LAB2RGB)[0].astype(np.float32)
    m = np.zeros((k + 1, H, W), np.float32)
    yy, xx = np.mgrid[:H, :W]
    m[labels, yy, xx] = 1
    m[:k] *= alpha
    m[k] = 1 - alpha
    return list(pal), m


def trace(path: str | Path, up: int = 8, simplify: float = 0.85, grow: int = 2, sharpen: float = 0.9,
          min_area: float = 0.9, colors: int | None = None, max_side: int = 520) -> dict:
    """Any image -> vector colour layers. Logos and flat art keep their exact colours; photos (auto-detected, or
    colors=k) are grouped into k colours, like a poster or a painting in flat paint."""
    im = Image.open(path).convert("RGBA")
    if max(im.size) > max_side:                    # the result is vector: tracing a big photo larger adds only noise
        f = max_side / max(im.size)
        im = im.resize((max(1, round(im.width * f)), max(1, round(im.height * f))), Image.LANCZOS)
    w, h = im.size
    a0 = np.asarray(im)
    photo = colors is not None or looks_like_photo(a0)
    if photo:
        pal, mem = _photo_memberships(a0, colors or 24)
        up, simplify, min_area, sharpen = (4 if max(w, h) > 260 else 6), 1.1, max(min_area, 2.5), 0.4
    else:
        pal = _palette(a0)
        mem = _memberships(a0, np.array(pal, np.float32))
    P = np.array(pal, np.float32)
    # unsharp the shares first: a line thinner than a pixel never reaches 50% at its core and would break into beads
    # when enlarged; sharpening lifts such peaks while a straight edge keeps its 50% midpoint where it was
    mem = np.stack([cv2.GaussianBlur(m, (0, 0), .55) for m in mem])      # even out pixel-to-pixel flicker
    mem = np.stack([m + sharpen * (m - cv2.GaussianBlur(m, (0, 0), 1.0)) for m in mem])
    mem = np.stack([cv2.resize(m, (w * up, h * up), interpolation=cv2.INTER_CUBIC) for m in mem])
    lab = mem.argmax(0)
    alpha = lab != len(P)
    lab[~alpha] = -1
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * grow + 1, 2 * grow + 1))

    def contours(mask) -> list[dict]:
        cs, hier = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
        if hier is None:
            return []
        hier = hier[0]
        outers = sorted([i for i in range(len(cs)) if hier[i][3] < 0], key=lambda i: -cv2.contourArea(cs[i]))
        out = []
        for i in outers:
            groups = [(i, False)] + [(j, True) for j in range(len(cs)) if hier[j][3] == i]
            for j, hole in groups:
                c = cv2.approxPolyDP(cs[j], simplify, True)[:, 0, :].astype(np.float32)
                if len(c) >= 3 and abs(cv2.contourArea(c)) > up * up * min_area:
                    out.append({"hole": hole, "pts": np.round((c + .5) / up, 3).tolist()})
        return out

    layers = []
    areas = [(int((lab == k).sum()), k) for k in range(len(pal))]
    for area, k in sorted(areas, reverse=True):
        if area < up * up * 2:
            continue
        mask = cv2.dilate(((lab == k) * 255).astype(np.uint8), kernel)
        ys, xs = np.nonzero(lab == k)
        col = P[k]
        layers.append({"color": "#%02x%02x%02x" % tuple(int(round(v)) for v in col), "name": name_ar(col),
                       "area": round(area / up / up, 1), "centre": [round(xs.mean() / up, 1), round(ys.mean() / up, 1)],
                       "polys": contours(mask)})
    silhouette = contours((alpha * 255).astype(np.uint8))
    return {"source": Path(path).name, "size": [w, h], "photo": bool(photo), "layers": layers,
            "silhouette": silhouette}


def to_svg(data: dict, path: str | Path, scale: float = 1.0):
    """Write the traced picture as an SVG (one even-odd path per colour, stacked like the program)."""
    w, h = data["size"]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w * scale:g}" height="{h * scale:g}">']
    for L in data["layers"]:
        d = " ".join("M" + " L".join(f"{x:g} {y:g}" for x, y in p["pts"]) + " Z" for p in L["polys"])
        out.append(f'<path fill="{L["color"]}" fill-rule="evenodd" d="{d}"/>')
    out.append("</svg>")
    Path(path).write_text("\n".join(out), encoding="utf-8")


def save(data: dict, path: str | Path):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


if __name__ == "__main__":
    import sys
    src = sys.argv[1]
    data = trace(src)
    n = sum(len(L["polys"]) for L in data["layers"])
    pts = sum(len(p["pts"]) for L in data["layers"] for p in L["polys"])
    print(f"{src}: {data['size']} -> {len(data['layers'])} colour layers, {n} outlines, {pts} points")
    for L in data["layers"]:
        print(f"  {L['color']} {L['name']:<16} area {L['area']:>8} px  outlines {len(L['polys'])}")
    stem = Path(src).stem
    save(data, Path(__file__).parent / "scenes" / f"{stem}.json")
    to_svg(data, Path(__file__).parent / "out" / f"{stem}.svg", scale=4)
