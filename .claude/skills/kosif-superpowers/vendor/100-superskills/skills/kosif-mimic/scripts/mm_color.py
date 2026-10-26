"""Colour science helpers: sRGB↔Lab, statistics, Reinhard colour transfer as a 3D LUT (.cube), colour names."""
from __future__ import annotations

from pathlib import Path

import numpy as np

_M = np.array([[0.4124564, 0.3575761, 0.1804375],
               [0.2126729, 0.7151522, 0.0721750],
               [0.0193339, 0.1191920, 0.9503041]], np.float32)
_MI = np.linalg.inv(_M).astype(np.float32)
_WHITE = np.array([0.95047, 1.0, 1.08883], np.float32)


def srgb_to_linear(c):
    c = np.asarray(c, np.float32)
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def linear_to_srgb(c):
    c = np.clip(np.asarray(c, np.float32), 0, None)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * np.power(c, 1 / 2.4) - 0.055)


def rgb_to_lab(rgb):
    """rgb: float in [0,1] (…x3) → Lab (L 0..100)."""
    lin = srgb_to_linear(rgb)
    xyz = lin @ _M.T / _WHITE
    eps = 216 / 24389
    k = 24389 / 27
    f = np.where(xyz > eps, np.cbrt(xyz), (k * xyz + 16) / 116)
    L = 116 * f[..., 1] - 16
    a = 500 * (f[..., 0] - f[..., 1])
    b = 200 * (f[..., 1] - f[..., 2])
    return np.stack([L, a, b], -1).astype(np.float32)


def lab_to_rgb(lab):
    lab = np.asarray(lab, np.float32)
    fy = (lab[..., 0] + 16) / 116
    fx = fy + lab[..., 1] / 500
    fz = fy - lab[..., 2] / 200
    eps = 216 / 24389
    k = 24389 / 27
    fx3, fz3 = fx ** 3, fz ** 3
    x = np.where(fx3 > eps, fx3, (116 * fx - 16) / k)
    y = np.where(lab[..., 0] > k * eps, fy ** 3, lab[..., 0] / k)
    z = np.where(fz3 > eps, fz3, (116 * fz - 16) / k)
    xyz = np.stack([x, y, z], -1) * _WHITE
    lin = xyz @ _MI.T
    return np.clip(linear_to_srgb(lin), 0, 1)


def lab_stats(rgb_u8: np.ndarray, mask: np.ndarray | None = None) -> dict:
    """Mean/std of Lab over (optionally masked-in) pixels. rgb_u8 HxWx3 or Nx3."""
    px = rgb_u8.reshape(-1, 3).astype(np.float32) / 255.0
    if mask is not None:
        m = mask.reshape(-1).astype(bool)
        if m.sum() > 50:
            px = px[m]
    if len(px) > 60000:
        idx = np.random.default_rng(7).choice(len(px), 60000, replace=False)
        px = px[idx]
    lab = rgb_to_lab(px)
    return {"mean": lab.mean(0).round(3).tolist(), "std": (lab.std(0) + 1e-3).round(3).tolist(),
            "p05": np.percentile(lab[:, 0], 5).round(2), "p95": np.percentile(lab[:, 0], 95).round(2)}


def merge_stats(stats: list[dict]) -> dict:
    if not stats:
        return {"mean": [50, 0, 0], "std": [20, 10, 10], "p05": 5, "p95": 95}
    m = np.mean([s["mean"] for s in stats], 0)
    # pooled std: mean of variances + variance of means
    var = np.mean([np.square(s["std"]) for s in stats], 0) + np.var([s["mean"] for s in stats], 0)
    return {"mean": m.round(3).tolist(), "std": np.sqrt(var).round(3).tolist(),
            "p05": float(np.mean([s.get("p05", 5) for s in stats])), "p95": float(np.mean([s.get("p95", 95) for s in stats]))}


def reinhard_lut(src: dict, dst: dict, size: int = 33, strength: float = 0.85,
                 max_gain: float = 2.2, chroma_strength: float | None = None) -> np.ndarray:
    """3D LUT (size³×3, R fastest when flattened in .cube order) mapping src stats → dst stats in Lab.

    strength blends the transfer with identity; gains are clamped so a flat source cannot explode."""
    chroma_strength = strength if chroma_strength is None else chroma_strength
    g = np.linspace(0, 1, size, dtype=np.float32)
    b, gg, r = np.meshgrid(g, g, g, indexing="ij")  # b slowest, r fastest
    rgb = np.stack([r, gg, b], -1).reshape(-1, 3)
    lab = rgb_to_lab(rgb)
    sm, ss = np.array(src["mean"], np.float32), np.array(src["std"], np.float32)
    dm, ds = np.array(dst["mean"], np.float32), np.array(dst["std"], np.float32)
    gain = np.clip(ds / np.maximum(ss, 1e-3), 1 / max_gain, max_gain)
    out = (lab - sm) * gain + dm
    w = np.array([strength, chroma_strength, chroma_strength], np.float32)
    lab2 = lab * (1 - w) + out * w
    lab2[:, 0] = np.clip(lab2[:, 0], 0, 100)
    return lab_to_rgb(lab2).astype(np.float32)


def write_cube(path: str | Path, lut: np.ndarray, size: int, title: str = "mimic"):
    lines = [f'TITLE "{title}"', f"LUT_3D_SIZE {size}", "DOMAIN_MIN 0.0 0.0 0.0", "DOMAIN_MAX 1.0 1.0 1.0"]
    lines += [f"{v[0]:.6f} {v[1]:.6f} {v[2]:.6f}" for v in lut.reshape(-1, 3)]
    Path(path).write_text("\n".join(lines) + "\n", encoding="ascii")


def apply_lut(rgb_u8: np.ndarray, lut: np.ndarray, size: int) -> np.ndarray:
    """Trilinear LUT application in NumPy (for previews/stats; the build uses ffmpeg lut3d)."""
    cube = lut.reshape(size, size, size, 3)  # [b][g][r]
    x = rgb_u8.astype(np.float32) / 255.0 * (size - 1)
    i0 = np.clip(np.floor(x).astype(np.int32), 0, size - 2)
    f = x - i0
    r0, g0, b0 = i0[..., 0], i0[..., 1], i0[..., 2]
    fr, fg, fb = f[..., 0:1], f[..., 1:2], f[..., 2:3]
    out = np.zeros(rgb_u8.shape, np.float32)
    for db in (0, 1):
        wb = fb if db else 1 - fb
        for dg in (0, 1):
            wg = fg if dg else 1 - fg
            for dr in (0, 1):
                wr = fr if dr else 1 - fr
                out += cube[b0 + db, g0 + dg, r0 + dr] * (wb * wg * wr)
    return np.clip(out * 255 + 0.5, 0, 255).astype(np.uint8)


def hex_of(rgb) -> str:
    r, g, b = [int(max(0, min(255, round(float(v))))) for v in rgb[:3]]
    return f"#{r:02X}{g:02X}{b:02X}"


def rgb_of(hexs: str) -> tuple[int, int, int]:
    h = hexs.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


_NAMES = {
    "black": (15, 15, 15), "white": (245, 245, 245), "gray": (128, 128, 128), "red": (200, 40, 40),
    "orange": (235, 140, 40), "gold": (212, 175, 80), "yellow": (240, 220, 60), "green": (60, 160, 70),
    "teal": (40, 150, 150), "blue": (50, 90, 200), "navy": (25, 35, 80), "purple": (120, 60, 160),
    "pink": (235, 150, 180), "brown": (120, 80, 50), "beige": (225, 205, 170), "cream": (245, 235, 210),
    "sky blue": (130, 180, 230), "lavender": (190, 170, 225), "peach": (245, 190, 150), "olive": (120, 120, 50),
}


def color_name(rgb) -> str:
    lab = rgb_to_lab(np.array(rgb, np.float32) / 255.0)
    best, bd = "gray", 1e9
    for n, c in _NAMES.items():
        d = float(np.linalg.norm(rgb_to_lab(np.array(c, np.float32) / 255.0) - lab))
        if d < bd:
            best, bd = n, d
    return best


def palette(rgb_u8: np.ndarray, k: int = 5, mask=None, seed: int = 3) -> list[dict]:
    """Small k-means palette in Lab → [{'hex','share','name'}] sorted by share."""
    px = rgb_u8.reshape(-1, 3).astype(np.float32)
    if mask is not None:
        m = mask.reshape(-1).astype(bool)
        if m.sum() > 100:
            px = px[m]
    rng = np.random.default_rng(seed)
    if len(px) > 20000:
        px = px[rng.choice(len(px), 20000, replace=False)]
    lab = rgb_to_lab(px / 255.0)
    k = min(k, max(1, len(lab) // 50))
    cent = lab[rng.choice(len(lab), k, replace=False)]
    for _ in range(12):
        d = ((lab[:, None, :] - cent[None]) ** 2).sum(-1)
        a = d.argmin(1)
        for j in range(k):
            sel = lab[a == j]
            if len(sel):
                cent[j] = sel.mean(0)
    d = ((lab[:, None, :] - cent[None]) ** 2).sum(-1)
    a = d.argmin(1)
    out = []
    for j in range(k):
        share = float((a == j).mean())
        if share <= 0:
            continue
        rgb = (lab_to_rgb(cent[j]) * 255).round()
        out.append({"hex": hex_of(rgb), "share": round(share, 3), "name": color_name(rgb)})
    return sorted(out, key=lambda d: -d["share"])


def delta_e(c1, c2) -> float:
    a = rgb_to_lab(np.array(c1, np.float32) / 255.0)
    b = rgb_to_lab(np.array(c2, np.float32) / 255.0)
    return float(np.linalg.norm(a - b))
