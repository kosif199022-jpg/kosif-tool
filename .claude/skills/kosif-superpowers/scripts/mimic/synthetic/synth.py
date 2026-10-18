"""Procedural 'Pinterest-style' ambient clips for tests: clouds, bokeh, rain, sunset, blossoms, candle.

Each generator returns a function frame(i) -> HxWx3 uint8. Deterministic per seed.
"""
from __future__ import annotations

import math

import numpy as np

try:
    import cv2
except Exception:  # pragma: no cover
    cv2 = None


def _blur(a, s):
    k = int(s * 3) * 2 + 1
    return cv2.GaussianBlur(a, (k, k), s)


def _noise_tex(h, w, seed, scale=40.0, octaves=3):
    rng = np.random.default_rng(seed)
    tex = np.zeros((h, w), np.float32)
    amp = 1.0
    for o in range(octaves):
        n = rng.standard_normal((h, w)).astype(np.float32)
        n = _blur(n, scale / (2 ** o))
        n /= (n.std() + 1e-6)
        tex += amp * n
        amp *= 0.5
    tex = (tex - tex.min()) / (tex.max() - tex.min() + 1e-6)
    return tex


def _vgrad(h, w, top, bottom, mid=None, midpos=0.5):
    y = np.linspace(0, 1, h, dtype=np.float32)[:, None, None]
    top = np.array(top, np.float32)[None, None]
    bottom = np.array(bottom, np.float32)[None, None]
    if mid is None:
        g = top * (1 - y) + bottom * y
    else:
        mid = np.array(mid, np.float32)[None, None]
        g = np.where(y < midpos, top * (1 - y / midpos) + mid * (y / midpos),
                     mid * (1 - (y - midpos) / (1 - midpos)) + bottom * ((y - midpos) / (1 - midpos)))
    return np.broadcast_to(g, (h, w, 3)).copy()


def clouds(w, h, seed=1, hue=(70, 130, 210), speed=1.2):
    tex = _noise_tex(h * 2, w * 2, seed, scale=60)
    sky = _vgrad(h, w, hue, (200, 220, 245))

    def frame(i):
        ox = int(20 + i * speed) % w
        oy = int(h * 0.5 + 6 * math.sin(i / 50))
        c = tex[oy:oy + h, ox:ox + w]
        c = np.clip((c - 0.45) * 2.6, 0, 1)[..., None]
        img = sky * (1 - c) + np.array([250, 250, 252], np.float32) * c
        return np.clip(img, 0, 255).astype(np.uint8)
    return frame


def bokeh(w, h, seed=2, base=(30, 18, 10), col=(255, 190, 90), n=36, speed=0.8):
    rng = np.random.default_rng(seed)
    xs = rng.uniform(0, w, n)
    ys = rng.uniform(0, h, n)
    rs = rng.uniform(w * 0.03, w * 0.11, n)
    vs = rng.uniform(0.3, 1.0, n) * speed
    a = rng.uniform(0.25, 0.8, n)
    bg = _vgrad(h, w, base, tuple(min(255, c * 2) for c in base))

    def frame(i):
        layer = np.zeros((h, w), np.float32)
        for k in range(n):
            y = (ys[k] - i * vs[k]) % (h + 2 * rs[k]) - rs[k]
            x = xs[k] + 8 * math.sin(i / 40 + k)
            cv2.circle(layer, (int(x), int(y)), int(rs[k]), float(a[k]), -1, lineType=cv2.LINE_AA)
        layer = _blur(layer, 3.0)
        img = bg + layer[..., None] * np.array(col, np.float32)[None, None]
        return np.clip(img, 0, 255).astype(np.uint8)
    return frame


def rain(w, h, seed=3, top=(8, 14, 35), bottom=(20, 40, 80), n=260, speed=24):
    rng = np.random.default_rng(seed)
    xs = rng.uniform(0, w, n)
    ys = rng.uniform(0, h, n)
    ln = rng.uniform(18, 46, n)
    br = rng.uniform(70, 170, n)
    bg = _vgrad(h, w, top, bottom)
    glow = np.zeros((h, w), np.float32)
    cv2.circle(glow, (int(w * 0.7), int(h * 0.3)), int(w * 0.2), 1.0, -1)
    glow = _blur(glow, w * 0.12)
    bg = bg + glow[..., None] * np.array([90, 80, 40], np.float32)

    def frame(i):
        layer = np.zeros((h, w), np.float32)
        for k in range(n):
            y = (ys[k] + i * speed * (0.6 + 0.4 * (k % 3) / 2)) % (h + 60) - 30
            x = xs[k] + 0.25 * (y - ys[k])
            cv2.line(layer, (int(x), int(y)), (int(x + ln[k] * 0.25), int(y + ln[k])), float(br[k]), 1, cv2.LINE_AA)
        img = bg + layer[..., None] * np.array([0.85, 0.9, 1.0], np.float32)[None, None]
        return np.clip(img, 0, 255).astype(np.uint8)
    return frame


def sunset(w, h, seed=4, top=(70, 40, 110), mid=(240, 120, 90), bottom=(40, 30, 60)):
    rng = np.random.default_rng(seed)
    bg = _vgrad(h, w, top, bottom, mid=mid, midpos=0.55)
    tex = _noise_tex(h, w * 2, seed + 10, scale=12)

    def frame(i):
        img = bg.copy()
        sx, sy = int(w * 0.5 + i * 0.3), int(h * 0.52 - i * 0.15)
        sun = np.zeros((h, w), np.float32)
        cv2.circle(sun, (sx, sy), int(w * 0.07), 1.0, -1, cv2.LINE_AA)
        halo = _blur(sun, w * 0.08)
        img += halo[..., None] * np.array([255, 170, 90], np.float32) * 0.9
        img = img * (1 - sun[..., None]) + sun[..., None] * np.array([255, 235, 190], np.float32)
        # water shimmer under the horizon
        wy = int(h * 0.62)
        sh = tex[wy:h, (i * 3) % w:(i * 3) % w + w]
        shimmer = np.clip((sh - 0.5) * 3, 0, 1)
        img[wy:h] = img[wy:h] * (0.55 + 0.25 * shimmer[..., None]) + shimmer[..., None] * np.array([120, 70, 50], np.float32) * 0.5
        return np.clip(img, 0, 255).astype(np.uint8)
    return frame


def blossoms(w, h, seed=5, base=(245, 205, 215), petal=(230, 110, 150), n=70):
    rng = np.random.default_rng(seed)
    xs = rng.uniform(0, w, n)
    ys = rng.uniform(0, h, n)
    rs = rng.uniform(w * 0.02, w * 0.06, n)
    ph = rng.uniform(0, 6.28, n)
    bg = _vgrad(h, w, base, (base[0] - 40, base[1] - 30, base[2] - 10))
    tex = _noise_tex(h, w, seed + 5, scale=50)
    bg = bg * (0.85 + 0.3 * tex[..., None])

    def frame(i):
        layer = np.zeros((h, w), np.float32)
        for k in range(n):
            x = xs[k] + 14 * math.sin(i / 25 + ph[k])
            y = (ys[k] + i * 0.9) % h
            cv2.ellipse(layer, (int(x), int(y)), (int(rs[k]), int(rs[k] * 0.6)), (i * 2 + k * 20) % 180, 0, 360, 1.0, -1, cv2.LINE_AA)
        layer = _blur(layer, 1.2)
        img = bg * (1 - 0.85 * layer[..., None]) + layer[..., None] * np.array(petal, np.float32) * 0.85
        return np.clip(img, 0, 255).astype(np.uint8)
    return frame


def candle(w, h, seed=6, warm=(255, 160, 60)):
    rng = np.random.default_rng(seed)
    fl = rng.uniform(0.85, 1.15, 4000)
    bg = _vgrad(h, w, (12, 8, 6), (30, 18, 10))

    def frame(i):
        f = float(np.convolve(fl, np.ones(5) / 5, mode="same")[i % 4000])
        glow = np.zeros((h, w), np.float32)
        cv2.circle(glow, (w // 2, int(h * 0.55)), int(w * 0.06 * f), 1.0, -1)
        g2 = _blur(glow, w * 0.18 * f)
        flame = np.zeros((h, w), np.float32)
        cv2.ellipse(flame, (w // 2 + int(3 * math.sin(i / 7)), int(h * 0.5)), (int(w * 0.018), int(w * 0.05 * f)), 0, 0, 360, 1.0, -1, cv2.LINE_AA)
        flame = _blur(flame, 2)
        img = bg + g2[..., None] * np.array(warm, np.float32) * 1.4 * f
        img = img * (1 - flame[..., None]) + flame[..., None] * np.array([255, 240, 200], np.float32)
        body = (slice(int(h * 0.56), int(h * 0.85)), slice(w // 2 - int(w * 0.07), w // 2 + int(w * 0.07)))
        img[body] = img[body] * 0.3 + np.array([230, 220, 205], np.float32) * 0.7 * (0.6 + 0.4 * f)
        return np.clip(img, 0, 255).astype(np.uint8)
    return frame


GENERATORS = {"clouds": clouds, "bokeh": bokeh, "rain": rain, "sunset": sunset, "blossoms": blossoms, "candle": candle}
