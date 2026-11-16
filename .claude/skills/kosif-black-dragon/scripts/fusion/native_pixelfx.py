#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""native_pixelfx - pixel-art frame effects for the Black Dragon, in numpy/OpenCV.

Ideas ported (re-written, not copied) from patch-gg/pixelfx (MIT, Copyright (c) 2026 Patch and Hugo Duprez;
sim.js adapts Sprite Fusion's pixel art VFX, act.js adapts Hollow Crown, both MIT):
  * two buffers per frame: COLOR (opaque pixels faded by 4x4 Bayer ordered dither, or soft alpha-blended discs)
    and LIGHT (additive glow), composited over footage; over transparency light becomes colour with
    alpha = its brightest channel (premultiplied), so sprite sheets read as additive on dark scenes;
  * a 120 Hz-substepped particle sim with pixel-art kinds: SPARK (streaks, bounces off the floor), FIRE
    (puffs that cool down a hue-shifted ramp and leave SMOKE), SMOKE (three soft discs), EMBER (drifting);
  * hue-shifted palette ramps (dark -> bright) and ramp mapping with no blending (pixel art picks a step);
  * hit-stop choreography: freeze on contact, decaying shake (sin/cos jitter on 60 Hz steps), poses held on
    12 fps steps, plus the anime "impact frame" (2 frames ink-on-paper, 2 inverted).

Subcommands
  palettes                         list ramps
  ramp-map IN OUT                  pixelate an image/video and map its luma onto a ramp with ordered dither
  fx PRESET OUT                    render explosion|sparks|campfire|embers over footage, an image, or a colour
                                   (OUT .mp4 / .png sequence dir); --sheet writes an RGBA sprite sheet + JSON
  hitstop IN OUT --hits 1.2,2.0    retime a clip: freeze + shake (+ --impact frames, + --step 12 on-twos look)
  self-test                        builds its own inputs in a temp dir and asserts real results
All subcommands accept --json for machine-readable output.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import sys
import tempfile
from pathlib import Path

import cv2
import numpy as np

# ----------------------------------------------------------------------------------------------- palettes
PAL = {
    "fire": ["#1f0b10", "#4a1118", "#8c1d1c", "#cc3a1a", "#f2701f", "#ffae35", "#ffe27a", "#fff8d6"],
    "ember": ["#1a0a0e", "#3d1012", "#701a14", "#a8301a", "#e0561e", "#ff8a2a", "#ffc46a"],
    "smoke": ["#0e0c12", "#1d1a22", "#2e2a35", "#433e4b", "#5c5664", "#7b7484", "#a39cab"],
    "ice": ["#0c1430", "#162c5c", "#1f4f94", "#2f7fcc", "#58b4ec", "#9bdcff", "#d8f4ff", "#ffffff"],
    "water": ["#081830", "#0e2e5a", "#14508c", "#1c76bc", "#36a2e0", "#78ccf4", "#c4ecff", "#ffffff"],
    "electric": ["#0a0f2e", "#172a78", "#2550d0", "#3f8cff", "#7cc8ff", "#c8f0ff", "#ffffff"],
    "poison": ["#0d1a0c", "#173a14", "#265e18", "#3f8a1e", "#6cb82a", "#a8e04a", "#e0ff8a"],
    "holy": ["#2a1c08", "#5a3e10", "#9a6c18", "#d8a428", "#ffd84a", "#fff09a", "#fffbe6", "#ffffff"],
    "arcane": ["#140a26", "#2b1252", "#481c88", "#6b2cc0", "#9a48ec", "#c684ff", "#ecc8ff", "#ffffff"],
    "shadow": ["#050308", "#0f0a18", "#1c1230", "#2c1a4a", "#432468", "#5e3290", "#8048b8", "#a970e0"],
    "gold": ["#1e1206", "#4a2c08", "#86520c", "#c48412", "#f0b424", "#ffe066", "#fff6c4", "#ffffff"],
    "neon": ["#1a0516", "#3d0a33", "#701560", "#b0228f", "#f53cd1", "#ff86e6", "#ffd2f6", "#ffffff"],
    "cyber": ["#041418", "#08303a", "#0c5260", "#108088", "#18b4b0", "#4ce8d8", "#b4fff0", "#ffffff"],
    "matrix": ["#020a04", "#05200c", "#0a3c16", "#106624", "#1a9a34", "#3cd650", "#a4ffa8", "#e8ffe8"],
    "night": ["#07060d", "#0c0a18", "#131026", "#1b1734", "#241f44", "#2f2956"],
}
HOT = ["#fff3a6", "#ffe26b", "#ff8a2a", "#f2561d"]
SMOKE_RAMP = ["#7b6f72", "#5d5660", "#433d48", "#2b2630", "#1a171e"]  # fresh -> thin
FIRE_HOT_TO_COLD = ["#ffffff", "#fff3a6", "#ffe26b", "#ffc23d", "#ff8a2a", "#f2561d", "#c9281f", "#8a1f17", "#4a1712"]

BAYER4 = (np.array([0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5], np.float32).reshape(4, 4) + 0.5) / 16.0


def hexrgb(h: str) -> np.ndarray:
    s = h.lstrip("#")
    if len(s) == 3:
        s = "".join(ch * 2 for ch in s)
    return np.array([int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)], np.float32)


def ramp(name_or_list) -> np.ndarray:
    lst = PAL[name_or_list] if isinstance(name_or_list, str) and name_or_list in PAL else (
        name_or_list.split(",") if isinstance(name_or_list, str) else name_or_list)
    return np.stack([hexrgb(c) for c in lst])


def fit_ramp(r: np.ndarray, n: int) -> np.ndarray:
    """Resample a ramp to n steps keeping both ends (nearest step, never blended)."""
    if len(r) == n:
        return r
    idx = [round(i * (len(r) - 1) / max(1, n - 1)) for i in range(n)]
    return r[idx]


# ----------------------------------------------------------------------------------------------- frame + painter
class Frame:
    """color: HxWx4 float (rgb 0..255, a 0..1); light: HxWx3 float additive."""

    def __init__(self, w: int, h: int):
        self.w, self.h = w, h
        self.color = np.zeros((h, w, 4), np.float32)
        self.light = np.zeros((h, w, 3), np.float32)

    # opaque pixel, faded by ordered dither (alpha a)
    def dot(self, x, y, c, a=1.0):
        sx, sy = int(math.floor(x)), int(math.floor(y))
        if a <= 0 or sx < 0 or sy < 0 or sx >= self.w or sy >= self.h:
            return
        if a < 1 and a <= BAYER4[sy & 3, sx & 3]:
            return
        self.color[sy, sx, :3] = c
        self.color[sy, sx, 3] = 1.0

    def line(self, x0, y0, x1, y1, c, a=1.0):
        sx, sy, ex, ey = int(math.floor(x0)), int(math.floor(y0)), int(math.floor(x1)), int(math.floor(y1))
        dx, dy = abs(ex - sx), -abs(ey - sy)
        stx, sty = (1 if sx < ex else -1), (1 if sy < ey else -1)
        err = dx + dy
        for _ in range(dx - dy + 2):
            self.dot(sx + 0.5, sy + 0.5, c, a)
            if sx == ex and sy == ey:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy; sx += stx
            if e2 <= dx:
                err += dx; sy += sty

    def _box(self, cx, cy, r):
        x0, x1 = max(0, int(math.floor(cx - r))), min(self.w - 1, int(math.ceil(cx + r)))
        y0, y1 = max(0, int(math.floor(cy - r))), min(self.h - 1, int(math.ceil(cy + r)))
        if x1 < x0 or y1 < y0:
            return None
        ys, xs = np.mgrid[y0:y1 + 1, x0:x1 + 1].astype(np.float32)
        return x0, y0, x1, y1, (xs + 0.5 - cx), (ys + 0.5 - cy)

    def circle(self, cx, cy, r, c):
        """Opaque filled disc (hard pixel edge)."""
        if r < 0.6:
            return self.dot(cx, cy, c)
        b = self._box(cx, cy, r)
        if b is None:
            return
        x0, y0, x1, y1, dx, dy = b
        m = dx * dx + dy * dy <= r * r
        reg = self.color[y0:y1 + 1, x0:x1 + 1]
        reg[m, :3] = c
        reg[m, 3] = 1.0

    def disc(self, cx, cy, r, c, a):
        """Soft translucent disc blended over what is there (smoke, vapour)."""
        if a <= 0.004:
            return
        b = self._box(cx, cy, max(r, 0.5))
        if b is None:
            return
        x0, y0, x1, y1, dx, dy = b
        m = dx * dx + dy * dy <= max(r, 0.5) ** 2
        reg = self.color[y0:y1 + 1, x0:x1 + 1]
        da = reg[..., 3]
        oa = a + da * (1 - a)
        k = np.where(oa > 0, a / np.maximum(oa, 1e-6), 0)[..., None]
        newc = np.asarray(c, np.float32) * k + reg[..., :3] * (1 - k)
        reg[..., :3] = np.where(m[..., None], newc, reg[..., :3])
        reg[..., 3] = np.where(m, oa, da)

    def glow(self, cx, cy, r, c, k=0.5):
        """Radial additive light: (1 - d)^2 * k, zero at radius r."""
        if r < 1 or k <= 0.004:
            return
        b = self._box(cx, cy, r)
        if b is None:
            return
        x0, y0, x1, y1, dx, dy = b
        d = np.sqrt((dx * dx + dy * dy)) / r
        f = np.clip(1 - d, 0, 1) ** 2 * k
        reg = self.light[y0:y1 + 1, x0:x1 + 1]
        np.minimum(reg + f[..., None] * np.asarray(c, np.float32), 255, out=reg)


def composite(fr: Frame, bg: np.ndarray | None, light_k=1.0, scale=1) -> np.ndarray:
    """Colour over background plus light. bg: HxWx3 uint8 at scale*frame size, or None for RGBA over nothing."""
    col, lit = fr.color, fr.light * light_k
    if scale != 1:
        col = np.repeat(np.repeat(col, scale, 0), scale, 1)
        lit = np.repeat(np.repeat(lit, scale, 0), scale, 1)
    rgb, a = col[..., :3], col[..., 3:4]
    if bg is not None:
        h, w = rgb.shape[:2]
        base = bg[:h, :w].astype(np.float32)
        out = rgb * a + base * (1 - a) + lit
        return np.clip(out, 0, 255).astype(np.uint8)
    # over transparency: premultiply, add light, divide by the new alpha (alpha >= brightest light channel)
    pr = rgb * a + lit
    na = np.clip(np.maximum(a, lit.max(axis=2, keepdims=True) / 255.0), 0, 1)
    outc = np.where(na > 0, np.minimum(255, pr / np.maximum(na, 1e-6)), 0)
    return np.concatenate([outc, na * 255], axis=2).clip(0, 255).astype(np.uint8)


# ----------------------------------------------------------------------------------------------- particles
SPARK, MOTE, FIRE, SMOKE, EMBER = range(5)
GRAVITY = 950.0


class Particles:
    def __init__(self, seed=1, ground=float("inf"), fire_ramp=None, sparks=None):
        self.R = random.Random(seed)
        self.list: list[dict] = []
        self.t = 0.0
        self.ground = ground
        self.fire = [hexrgb(c) for c in FIRE_HOT_TO_COLD] if fire_ramp is None else list(fire_ramp)
        self.sparks = [hexrgb(c) for c in (sparks or HOT)]
        self.smoke = [hexrgb(c) for c in SMOKE_RAMP]

    def spawn(self, k, x, y, vx, vy, life, size=1.0, smokes=False, big=False, delay=0.0, col=None):
        self.list.append(dict(k=k, x=x, y=y, vx=vx, vy=vy, life=life, max=life, size=size, smokes=smokes,
                              big=big, delay=delay, col=col, seed=self.R.random() * 100))

    def update(self, dt):
        n = max(1, math.ceil(dt * 120 - 1e-9))  # fixed fine step: same look at any output fps
        for _ in range(n):
            self._step(dt / n)

    def _step(self, dt):
        self.t += dt
        t, R = self.t, self.R
        keep = []
        for p in self.list:
            if p["delay"] > 0:
                p["delay"] -= dt; keep.append(p); continue
            p["life"] -= dt
            if p["life"] <= 0:
                if p["k"] == FIRE and p["smokes"]:
                    big = p["big"]
                    self.spawn(SMOKE, p["x"], p["y"], p["vx"] * 0.6, p["vy"] * 0.6 - 6,
                               R.uniform(1.3, 2.3) if big else R.uniform(0.8, 1.4), p["size"] * (0.85 if big else 0.7), big=big)
                continue
            k = p["k"]
            if k == FIRE:
                p["vy"] -= 95 * dt
                p["vx"] += math.sin(t * 17 + p["seed"]) * 30 * dt
                p["vx"] -= p["vx"] * 5 * dt
                p["vy"] -= p["vy"] * 3.2 * dt
            elif k == SPARK:
                p["vy"] += GRAVITY * 0.45 * dt
                p["vx"] -= p["vx"] * 2.2 * dt
                p["vy"] -= p["vy"] * 2.2 * dt
                ny = p["y"] + p["vy"] * dt
                p["x"] += p["vx"] * dt
                if p["vy"] > 0 and p["y"] <= self.ground <= ny:  # bounce, losing energy
                    p["vy"] = -p["vy"] * 0.45; p["vx"] *= 0.7; p["y"] = self.ground - 0.25
                else:
                    p["y"] = ny
                keep.append(p); continue
            elif k == EMBER:
                p["vy"] += (-30 + math.sin(t * 3 + p["seed"]) * 20) * dt
                p["vx"] += math.cos(t * 2.3 + p["seed"]) * 45 * dt
                p["vx"] -= p["vx"] * 1.6 * dt
                p["vy"] -= p["vy"] * 1.6 * dt
            elif k == SMOKE:
                p["vy"] -= (23 if p["big"] else 16) * dt
                p["vx"] += math.sin(t * 1.3 + p["seed"]) * 8 * dt
                p["vx"] -= p["vx"] * 1.6 * dt
                p["vy"] -= p["vy"] * 1.2 * dt
            elif k == MOTE:
                p["vx"] -= p["vx"] * 0.6 * dt; p["vy"] -= p["vy"] * 0.6 * dt
            p["x"] += p["vx"] * dt
            p["y"] += p["vy"] * dt
            keep.append(p)
        self.list = keep

    def draw(self, fr: Frame):
        # soft kinds first (behind), hard pixels and light on top
        order = sorted((q for q in self.list if q["delay"] <= 0), key=lambda q: 0 if q["k"] == SMOKE else 1)
        S, F, SM = self.sparks, self.fire, self.smoke
        for q in order:
            k = q["life"] / q["max"]
            x, y = q["x"], q["y"]
            sp = math.hypot(q["vx"], q["vy"]) or 1.0
            ux, uy = q["vx"] / sp, q["vy"] / sp
            if q["k"] == SPARK:
                head = S[0] if k > 0.6 else S[1] if k > 0.3 else S[2]
                ln = min(9.0, 1 + sp * 0.022)
                fr.line(x - ux * ln, y - uy * ln, x - ux * ln * 0.4, y - uy * ln * 0.4, head if k > 0.5 else S[-1])
                fr.line(x - ux * ln * 0.45, y - uy * ln * 0.45, x, y, head)
                fr.glow(x, y, 3, head, 0.45 * k)
            elif q["k"] == EMBER:
                c = S[0] if k > 0.6 else S[1] if k > 0.3 else S[2]
                if k < 0.25 and math.sin(self.t * 40 + q["seed"]) < 0:
                    continue  # dying embers flicker
                fr.dot(x, y, c)
                fr.glow(x, y, 3 + q["size"], c, 0.35 * k)
            elif q["k"] == MOTE:
                c = q["col"] if q["col"] is not None else S[1]
                fr.line(x - ux * 3, y - uy * 3, x, y, c, 1 if k > 0.35 else k / 0.35)
                fr.glow(x, y, 3, c, 0.4 * k)
            elif q["k"] == SMOKE:
                age = 1 - k
                r = q["size"] * (0.65 + min(1, age * 2.5) * 0.45 + age * (0.5 if q["big"] else 0.4))
                a = min(1, age * 12) * min(1, k * 2.4) * (0.7 if q["big"] else 0.58)
                c = SM[min(len(SM) - 1, int(age * 1.05 * len(SM)))]
                fr.disc(x, y, r, c, a * 0.45)
                fr.disc(x + r * 0.05, y + r * 0.06, r * 0.74, c, a * 0.62)
                if age < 0.5:
                    fr.disc(x - r * 0.22, y - r * 0.3, r * 0.5, c * 0.88 + 255 * 0.12, a * 0.4 * (1 - age * 2))
            elif q["k"] == FIRE:
                # a ball that cools down the ramp as it rises: dark rim, lit core, tongue on top
                age = 1 - k
                n = len(F)
                heat = min(0.999, age ** 0.62 + (q["seed"] % 1) * 0.1)
                idx = min(n - 2, int(heat * (n - 1)))
                r = q["size"] * (0.55 + 0.45 * min(1, age * 7)) * (1 - age * 0.55)
                c = F[idx]
                if idx >= n - 2:
                    fr.disc(x, y, r, c, min(1, k * 3) * 0.85)
                else:
                    fr.circle(x, y, r, F[min(n - 1, idx + 2)])
                    fr.circle(x - r * 0.16, y - r * 0.22, r * 0.78, c)
                    if r > 1.6:
                        fr.circle(x, y - r * 0.9, r * 0.42, c)
                    if idx <= 3 and r > 1.8:
                        fr.circle(x - r * 0.28, y - r * 0.34, r * 0.36, F[max(0, idx - 1)])
                    if idx < 6:
                        fr.glow(x, y, r * 2.4 + 2, c, 0.18 * k)


class Flashes:
    """Lights that flare and die (k * life^2)."""

    def __init__(self):
        self.list = []

    def add(self, x, y, r, c, k, life):
        self.list.append([x, y, r, hexrgb(c) if isinstance(c, str) else c, k, life, life])

    def update(self, dt):
        for l in self.list:
            l[5] -= dt
        self.list = [l for l in self.list if l[5] > 0]

    def draw(self, fr):
        for x, y, r, c, k, life, mx in self.list:
            u = life / mx
            fr.glow(x, y, r * (0.55 + 0.45 * u), c, k * u * u)


# ----------------------------------------------------------------------------------------------- presets
def make_preset(name, x, y, seed, palette=None, ground=None):
    fire_ramp = None
    if palette:
        rp = ramp(palette)  # dark -> bright; fire walks bright -> dark, and tops out white
        fire_ramp = [np.array([255, 255, 255], np.float32)] + list(fit_ramp(rp, 8)[::-1])
    ps = Particles(seed=seed, ground=ground if ground is not None else y + 6, fire_ramp=fire_ramp)
    fl = Flashes()
    R = ps.R
    state = {"t": 0.0, "acc": 0.0}
    hot = ps.fire[3] if len(ps.fire) > 3 else hexrgb(HOT[1])

    def burst_explosion():
        fl.add(x, y, 60, hot, 0.9, 0.35)
        fl.add(x, y, 22, "#ffffff", 1.0, 0.1)
        for _ in range(26):
            a, v = R.uniform(0, math.tau), R.uniform(20, 70)
            ps.spawn(FIRE, x + math.cos(a) * 3, y + math.sin(a) * 3, math.cos(a) * v, math.sin(a) * v - 20,
                     R.uniform(0.35, 0.8), R.uniform(2.5, 5.5), smokes=R.random() < 0.7, big=R.random() < 0.5)
        for _ in range(30):
            a, v = R.uniform(math.pi * 1.05, math.pi * 1.95), R.uniform(120, 320)
            ps.spawn(SPARK, x, y, math.cos(a) * v, math.sin(a) * v, R.uniform(0.3, 0.8))
        for _ in range(10):
            ps.spawn(EMBER, x + R.uniform(-6, 6), y + R.uniform(-4, 4), R.uniform(-30, 30), R.uniform(-60, -20), R.uniform(0.8, 1.6), R.uniform(1, 2))

    def burst_sparks():
        fl.add(x, y, 26, "#fff3a6", 0.8, 0.15)
        for _ in range(40):
            a, v = R.uniform(math.pi * 1.1, math.pi * 1.9), R.uniform(150, 380)
            ps.spawn(SPARK, x, y, math.cos(a) * v, math.sin(a) * v, R.uniform(0.25, 0.7))

    def tick_campfire(dt):
        state["acc"] += dt * 30
        while state["acc"] > 1:
            state["acc"] -= 1
            s = R.uniform(1.6, 3.4)
            ps.spawn(FIRE, x + R.uniform(-4, 4), y - s * 0.6, R.uniform(-6, 6), R.uniform(-34, -14), R.uniform(0.3, 0.65), s, smokes=R.random() < 0.3)
            if R.random() < 0.08:
                ps.spawn(EMBER, x, y - 2, R.uniform(-15, 15), R.uniform(-45, -15), R.uniform(0.6, 1.4), 1)
        fr_flick = 0.25 + 0.08 * math.sin(state["t"] * 23)
        fl.list = [l for l in fl.list if l[6] != 0.05]
        fl.add(x, y - 4, 30, hot, fr_flick, 0.05)

    def tick_embers(dt):
        state["acc"] += dt * 14
        while state["acc"] > 1:
            state["acc"] -= 1
            ps.spawn(EMBER, x + R.uniform(-40, 40), y + R.uniform(-4, 4), R.uniform(-10, 10), R.uniform(-40, -10), R.uniform(1.0, 2.2), R.uniform(1, 2))

    started = {"v": False}

    def update(dt):
        if not started["v"]:
            started["v"] = True
            if name == "explosion":
                burst_explosion()
            elif name == "sparks":
                burst_sparks()
        state["t"] += dt
        if name == "campfire":
            tick_campfire(dt)
        elif name == "embers":
            tick_embers(dt)
        ps.update(dt)
        fl.update(dt)

    def draw(fr):
        fl.draw(fr)
        ps.draw(fr)

    return update, draw, ps


PRESETS = ("explosion", "sparks", "campfire", "embers")


# ----------------------------------------------------------------------------------------------- media io
def read_frames(path, max_frames=None):
    cap = cv2.VideoCapture(str(path))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    out = []
    while True:
        ok, f = cap.read()
        if not ok:
            break
        out.append(f)
        if max_frames and len(out) >= max_frames:
            break
    cap.release()
    return out, fps


def write_video(path, frames, fps):
    path = Path(path)
    if path.suffix.lower() in (".mp4", ".avi", ".mov"):
        h, w = frames[0].shape[:2]
        vw = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*("mp4v" if path.suffix.lower() != ".avi" else "MJPG")), fps, (w, h))
        for f in frames:
            vw.write(f)
        vw.release()
    else:
        path.mkdir(parents=True, exist_ok=True)
        for i, f in enumerate(frames):
            cv2.imencode(".png", f)[1].tofile(str(path / f"frame_{i:05d}.png"))
    return str(path)


def imread(path):
    return cv2.imdecode(np.fromfile(str(path), np.uint8), cv2.IMREAD_COLOR)


def imwrite(path, img):
    cv2.imencode(Path(path).suffix or ".png", img)[1].tofile(str(path))


IMG_EXT = {".png", ".jpg", ".jpeg", ".bmp", ".webp"}


# ----------------------------------------------------------------------------------------------- ramp-map
def ramp_map_image(bgr, palette="fire", pixel=4, dither=True):
    h, w = bgr.shape[:2]
    sw, sh = max(1, w // pixel), max(1, h // pixel)
    small = cv2.resize(bgr, (sw, sh), interpolation=cv2.INTER_AREA).astype(np.float32)
    luma = (0.299 * small[..., 2] + 0.587 * small[..., 1] + 0.114 * small[..., 0]) / 255.0
    rp = ramp(palette)
    n = len(rp)
    x = np.clip(luma, 0, 1) * (n - 1)
    lo = np.floor(x).astype(int)
    frac = x - lo
    if dither:
        th = np.tile(BAYER4, (sh // 4 + 1, sw // 4 + 1))[:sh, :sw]
        idx = np.where(frac > th, lo + 1, lo)
    else:
        idx = np.rint(x).astype(int)
    idx = np.clip(idx, 0, n - 1)
    rgb = rp[idx]
    out = rgb[..., ::-1].astype(np.uint8)
    return cv2.resize(out, (sw * pixel, sh * pixel), interpolation=cv2.INTER_NEAREST)


def cmd_ramp_map(a):
    src = Path(a.input)
    if src.suffix.lower() in IMG_EXT:
        out = ramp_map_image(imread(src), a.palette, a.pixel, not a.no_dither)
        imwrite(a.output, out)
        res = {"output": a.output, "size": [out.shape[1], out.shape[0]], "colors": int(len(np.unique(out.reshape(-1, 3), axis=0)))}
    else:
        frames, fps = read_frames(src)
        outs = [ramp_map_image(f, a.palette, a.pixel, not a.no_dither) for f in frames]
        write_video(a.output, outs, fps)
        res = {"output": a.output, "frames": len(outs), "fps": fps}
    return res


# ----------------------------------------------------------------------------------------------- fx
def parse_bg(spec, W, H, n):
    """Returns a function i -> HxWx3 BGR uint8 (or None for transparent)."""
    if spec in (None, "", "none", "transparent"):
        return lambda i: None, None
    p = Path(spec)
    if p.exists() and p.suffix.lower() in IMG_EXT:
        img = cv2.resize(imread(p), (W, H), interpolation=cv2.INTER_AREA)
        return lambda i: img, None
    if p.exists():
        frames, fps = read_frames(p, n)
        frames = [cv2.resize(f, (W, H), interpolation=cv2.INTER_AREA) for f in frames]
        return (lambda i: frames[min(i, len(frames) - 1)]), fps
    c = hexrgb(spec)[::-1].astype(np.uint8)
    img = np.empty((H, W, 3), np.uint8); img[:] = c
    return lambda i: img, None


def render_fx(preset, W, H, pixel, seconds, fps, x=None, y=None, seed=1, palette=None, bg=None, light=1.0):
    pw, ph = W // pixel, H // pixel
    x = pw / 2 if x is None else x / pixel
    y = ph * 0.7 if y is None else y / pixel
    n = int(round(seconds * fps))
    bgf, bgfps = parse_bg(bg, pw * pixel, ph * pixel, n)
    update, draw, ps = make_preset(preset, x, y, seed, palette)
    frames, rgba = [], []
    for i in range(n):
        update(1.0 / fps)
        fr = Frame(pw, ph)
        draw(fr)
        b = bgf(i)
        rgba.append(composite(fr, None, light, 1))
        if b is None:
            frames.append(cv2.cvtColor(composite(fr, None, light, pixel), cv2.COLOR_RGBA2BGRA))
        else:
            rgb = composite(fr, b[..., ::-1].copy(), light, pixel)
            frames.append(rgb[..., ::-1].copy())
    return frames, rgba, (pw, ph, x, y)


def write_sheet(rgba_frames, path, fps, pivot, name):
    n = len(rgba_frames)
    h, w = rgba_frames[0].shape[:2]
    cols = max(1, math.ceil(math.sqrt(n)))
    rows = math.ceil(n / cols)
    sheet = np.zeros((rows * h, cols * w, 4), np.uint8)
    frames = []
    for i, f in enumerate(rgba_frames):
        r, c = divmod(i, cols)
        sheet[r * h:(r + 1) * h, c * w:(c + 1) * w] = f
        frames.append({"filename": f"{name}_{i}", "frame": {"x": c * w, "y": r * h, "w": w, "h": h}, "duration": round(1000 / fps)})
    imwrite(path, cv2.cvtColor(sheet, cv2.COLOR_RGBA2BGRA))
    meta = {"frames": frames, "meta": {"image": Path(path).name, "size": {"w": cols * w, "h": rows * h},
            "frameTags": [{"name": name, "from": 0, "to": n - 1, "direction": "forward"}],
            "pixelfx": {"fps": fps, "frames": n, "frameSize": [w, h], "columns": cols, "pivot": [round(pivot[0], 2), round(pivot[1], 2)]}}}
    jp = Path(path).with_suffix(".json")
    jp.write_text(json.dumps(meta, indent=1), encoding="utf-8")
    return str(jp)


def cmd_fx(a):
    W, H = map(int, a.size.lower().split("x"))
    frames, rgba, (pw, ph, px, py) = render_fx(a.preset, W, H, a.pixel, a.seconds, a.fps, a.x, a.y, a.seed, a.palette, a.bg, a.light)
    res = {"preset": a.preset, "frames": len(frames), "pixel_canvas": [pw, ph], "scale": a.pixel}
    if a.output:
        if a.bg in (None, "", "none", "transparent") and Path(a.output).suffix.lower() in (".mp4", ".avi", ".mov"):
            frames = [f[..., :3] for f in frames]
        res["output"] = write_video(a.output, frames, a.fps)
    if a.sheet:
        res["sheet"] = a.sheet
        res["sheet_json"] = write_sheet(rgba, a.sheet, a.fps, (px, py), a.preset)
    return res


# ----------------------------------------------------------------------------------------------- hitstop
def two_tone(f, invert=False, thr=None):
    g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    thr = float(np.median(g)) if thr is None else thr
    paper = g > thr
    if invert:
        paper = ~paper
    out = np.where(paper[..., None], 255, 0).astype(np.uint8)
    return np.repeat(out, 3, axis=2) if out.shape[2] == 1 else out


def shake_offset(shake_left, shake0, amp):
    if shake_left <= 0:
        return 0, 0
    k = amp * (shake_left / shake0)
    f = math.floor(shake_left * 60)
    return round(math.sin(f * 2.4) * k), round(math.cos(f * 3.7) * k * 0.7)


def hitstop_frames(frames, fps, hits, stop=0.1, shake=0.25, amp=6.0, impact=False, step=0.0):
    """Returns (out_frames, timeline). Source time stands still for round(stop*fps) frames at each hit; shake decays over `shake` s."""
    hits = sorted(hits)
    dt = 1.0 / fps
    dur = len(frames) / fps
    out, timeline = [], []
    src_t, freeze_left, shake_left, hi, impact_i = 0.0, 0, 0.0, 0, -1
    while src_t < dur - 1e-9:
        while hi < len(hits) and hits[hi] <= src_t + 1e-9:
            freeze_left = max(freeze_left, int(round(stop * fps)))
            shake_left = shake
            impact_i = 0 if impact else -1
            hi += 1
        ts = src_t
        if step > 0:
            ts = math.floor(src_t * step + 1e-6) / step  # held drawings on step-fps beats
        idx = min(len(frames) - 1, int(round(ts * fps)))
        f = frames[idx]
        if 0 <= impact_i < 4:
            f = two_tone(f, invert=impact_i >= 2)
            impact_i += 1
        ox, oy = shake_offset(shake_left, shake, amp)
        if ox or oy:
            M = np.float32([[1, 0, ox], [0, 1, oy]])
            f = cv2.warpAffine(f, M, (f.shape[1], f.shape[0]), borderMode=cv2.BORDER_REPLICATE)
        out.append(f)
        timeline.append({"out": len(out) - 1, "src": idx, "frozen": freeze_left > 0, "shake": [ox, oy]})
        if shake_left > 0:
            shake_left -= dt
        if freeze_left > 0:
            freeze_left -= 1
        else:
            src_t += dt
    return out, timeline


def cmd_hitstop(a):
    frames, fps = read_frames(a.input)
    if not frames:
        raise SystemExit("no frames read from input")
    hits = [float(v) for v in a.hits.split(",") if v.strip()]
    out, tl = hitstop_frames(frames, fps, hits, a.stop, a.shake, a.amp, a.impact, a.step)
    write_video(a.output, out, fps)
    return {"output": a.output, "in_frames": len(frames), "out_frames": len(out), "fps": fps,
            "frozen_frames": sum(1 for r in tl if r["frozen"]), "hits": hits}


# ----------------------------------------------------------------------------------------------- self-test
def self_test():
    results = []

    def check(name, cond, detail=""):
        results.append({"check": name, "ok": bool(cond), "detail": detail})
        if not cond:
            raise AssertionError(f"{name}: {detail}")

    with tempfile.TemporaryDirectory(prefix="pixelfx_st_") as td:
        td = Path(td)
        # 1. ramp-map: a horizontal gradient maps only onto ramp colours, with dither mixing in mid-tones
        grad = np.tile(np.linspace(0, 255, 128, dtype=np.uint8)[None, :, None], (64, 1, 3))
        gp = td / "grad.png"; imwrite(gp, grad)
        out = ramp_map_image(imread(gp), "ice", 4, True)
        cols = {tuple(c) for c in np.unique(out.reshape(-1, 3), axis=0)}
        allowed = {tuple(c[::-1].astype(np.uint8)) for c in ramp("ice")}
        check("ramp-map uses only ramp colours", cols <= allowed, f"{len(cols)} colours")
        check("ramp-map spans the ramp", len(cols) >= 6, f"{len(cols)} of {len(allowed)}")
        blk = out[0:16, 40:56].reshape(-1, 3)
        check("ordered dither mixes neighbouring steps inside a mid-tone block", len(np.unique(blk, axis=0)) >= 2)
        check("pixelation keeps 4x4 blocks", bool(np.all(out[0:4, 0:4] == out[0, 0])))

        # 2. composite over transparency: light alone becomes colour with alpha = brightest channel
        fr = Frame(8, 8); fr.glow(4, 4, 4, hexrgb("#ff8000"), 1.0)
        rgba = composite(fr, None)
        c = rgba[4, 4]
        check("light over nothing -> alpha from brightest channel", c[3] > 100 and c[0] >= c[1] >= c[2], str(c.tolist()))

        # 3. explosion preset over a dark plate, deterministic per seed
        f1, rg1, _ = render_fx("explosion", 320, 180, 2, 1.2, 30, seed=7, bg="#0b0a10")
        f2, _, _ = render_fx("explosion", 320, 180, 2, 1.2, 30, seed=7, bg="#0b0a10")
        f3, _, _ = render_fx("explosion", 320, 180, 2, 1.2, 30, seed=8, bg="#0b0a10")
        h = lambda fs: hashlib.sha1(b"".join(x.tobytes() for x in fs)).hexdigest()
        check("same seed renders identical frames", h(f1) == h(f2))
        check("other seed renders a different take", h(f1) != h(f3))
        bright = [float(x.mean()) for x in f1]
        peak = int(np.argmax(bright))
        check("explosion flares early then dies down", peak < 8 and bright[-1] < bright[peak] * 0.6,
              f"peak frame {peak} mean {bright[peak]:.1f}, last {bright[-1]:.1f}")
        check("pixel scale 2 gives 2x2 blocks", bool(np.all(f1[5][90:92, 160:162] == f1[5][90, 160])))
        sh = td / "explosion.png"
        jp = write_sheet(rg1, sh, 30, (80, 63), "explosion")
        meta = json.loads(Path(jp).read_text(encoding="utf-8"))
        sheet = cv2.imdecode(np.fromfile(str(sh), np.uint8), cv2.IMREAD_UNCHANGED)
        check("sprite sheet is RGBA with transparent and opaque pixels",
              sheet.shape[2] == 4 and (sheet[..., 3] == 0).any() and (sheet[..., 3] == 255).any())
        check("sheet json lists every frame", len(meta["frames"]) == len(rg1) == 36, str(len(meta["frames"])))

        # 4. sparks bounce off the floor (none end up far below it)
        upd, drw, ps = make_preset("sparks", 80, 60, 3, ground=66)
        maxy = 0.0
        for _ in range(18):
            upd(1 / 30)
            maxy = max([maxy] + [p["y"] for p in ps.list if p["k"] == SPARK])
        check("sparks bounce on the ground line", maxy < 66 + 4, f"max y {maxy:.2f}")

        # 5. hitstop on a synthetic clip with a moving square
        frames = []
        for i in range(30):
            f = np.full((72, 128, 3), 40, np.uint8)
            cv2.rectangle(f, (4 + i * 3, 30), (14 + i * 3, 40), (255, 255, 255), -1)
            frames.append(f)
        vp = td / "clip.avi"; write_video(vp, frames, 30)
        back, fps = read_frames(vp)
        check("synthetic clip round-trips", len(back) == 30, str(len(back)))
        out, tl = hitstop_frames(back, 30, [0.5], stop=0.2, shake=0.2, amp=4, impact=True)
        check("freeze inserts stop*fps frames", len(out) == 36, str(len(out)))
        frozen_src = {r["src"] for r in tl if r["frozen"]}
        check("source frame holds during the freeze", len(frozen_src) == 1, str(frozen_src))
        imp = out[15:19]
        check("impact frames are two-tone ink/paper", all(set(np.unique(x).tolist()) <= {0, 255} for x in imp))
        check("frames 3-4 of the impact are inverted", bool((imp[2] == 255 - imp[0]).mean() > 0.95))
        check("shake moves the picture then settles", any(r["shake"] != [0, 0] for r in tl) and tl[-1]["shake"] == [0, 0])
        out12, tl12 = hitstop_frames(back, 30, [], step=12)
        srcs = [r["src"] for r in tl12]
        check("step=12 holds drawings (fewer unique source frames)", len(set(srcs)) <= 13, str(len(set(srcs))))
    return {"ok": all(r["ok"] for r in results), "passed": sum(r["ok"] for r in results), "total": len(results), "checks": results}


# ----------------------------------------------------------------------------------------------- cli
def main(argv=None):
    ap = argparse.ArgumentParser(description="Pixel-art frame effects (ported ideas from patch-gg/pixelfx, MIT).")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("palettes", help="list palette ramps")

    r = sub.add_parser("ramp-map", help="pixelate + map luma onto a palette ramp with Bayer dither")
    r.add_argument("input"); r.add_argument("output")
    r.add_argument("--palette", default="fire", help="ramp name or comma list of hex, dark to bright")
    r.add_argument("--pixel", type=int, default=4)
    r.add_argument("--no-dither", action="store_true")

    f = sub.add_parser("fx", help="render a pixel VFX preset over footage/image/colour")
    f.add_argument("preset", choices=PRESETS)
    f.add_argument("output", nargs="?", help=".mp4/.avi or a directory for a PNG sequence")
    f.add_argument("--size", default="640x360"); f.add_argument("--pixel", type=int, default=3)
    f.add_argument("--seconds", type=float, default=1.5); f.add_argument("--fps", type=float, default=30)
    f.add_argument("--x", type=float); f.add_argument("--y", type=float)
    f.add_argument("--seed", type=int, default=1); f.add_argument("--palette")
    f.add_argument("--bg", default="#0b0a10", help="video, image, #hex colour, or 'transparent'")
    f.add_argument("--light", type=float, default=1.0)
    f.add_argument("--sheet", help="also write an RGBA sprite sheet PNG (+ .json) at pixel resolution")

    h = sub.add_parser("hitstop", help="freeze + shake (+impact frames, +on-twos) at hit times")
    h.add_argument("input"); h.add_argument("output")
    h.add_argument("--hits", required=True, help="comma list of seconds in the source")
    h.add_argument("--stop", type=float, default=0.1); h.add_argument("--shake", type=float, default=0.25)
    h.add_argument("--amp", type=float, default=6.0); h.add_argument("--impact", action="store_true")
    h.add_argument("--step", type=float, default=0.0, help="hold frames on N fps beats (12 = animated-on-twos)")

    sub.add_parser("self-test")
    a = ap.parse_args(argv)
    if a.cmd == "palettes":
        res = {k: v for k, v in PAL.items()}
    elif a.cmd == "ramp-map":
        res = cmd_ramp_map(a)
    elif a.cmd == "fx":
        res = cmd_fx(a)
    elif a.cmd == "hitstop":
        res = cmd_hitstop(a)
    else:
        try:
            res = self_test()
        except AssertionError as e:
            res = {"ok": False, "error": str(e)}
            print(json.dumps(res, ensure_ascii=False, indent=1))
            return 1
    if a.json or a.cmd == "self-test":
        print(json.dumps(res, ensure_ascii=False, indent=1))
    else:
        for k, v in res.items():
            print(f"{k}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
