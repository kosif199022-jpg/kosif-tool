#!/usr/bin/env python3
"""English on-screen captions for the Einstein season (toonkit surface).

    import captions as cap
    cap.title(g, "Moving clocks tick slower.", t, t0=3.0, t1=6.0)            # big top caption, pops in and out
    cap.note(g, "Einstein, 1905", (540, 1700), t, t0=8, t1=12, size=40)      # small caption anywhere
    cap.clock(g, (200, 400), 60, t * 0.5)                                     # clock face, hands from a time in hours

Text is drawn with PIL on the 1.5x canvas, white fill with a thick dark outline, and a soft rounded backing card.
Keep captions short (2 to 8 words) and leave them on screen at least 1.5 s.
"""
import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import toonkit as tk

FONT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "20261115-s79", "fonts")
_CANDIDATES = [
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fonts", "Cairo-900.ttf"),
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
_cache = {}


def _font(size):
    if size not in _cache:
        for p in _CANDIDATES:
            if os.path.exists(p):
                _cache[size] = ImageFont.truetype(p, int(size * tk.S)); break
        else:
            _cache[size] = ImageFont.load_default()
    return _cache[size]


def _draw(g, text, c, size, alpha, col, ink, card, scale=1.0):
    if alpha <= 0.01: return
    f = _font(max(8, int(size * scale)))
    d0 = ImageDraw.Draw(Image.new("L", (4, 4)))
    bb = d0.textbbox((0, 0), text, font=f, stroke_width=int(6 * tk.S))
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    pad = int(26 * tk.S * scale)
    im = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if card:
        d.rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=int(28 * tk.S * scale), fill=card + (200,))
    d.text((pad - bb[0], pad - bb[1]), text, font=f, fill=col[::-1] + (255,), stroke_width=int(6 * tk.S * scale), stroke_fill=ink[::-1] + (255,))
    a = np.asarray(im).astype(np.float32)
    x0, y0 = int(c[0] * tk.S - im.width / 2), int(c[1] * tk.S - im.height / 2)
    H, W = g.img.shape[:2]
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + im.width), min(H, y0 + im.height)
    if xb <= xa or yb <= ya: return
    L = a[ya - y0:yb - y0, xa - x0:xb - x0]
    al = L[..., 3:4] / 255.0 * alpha
    reg = g.img[ya:yb, xa:xb].astype(np.float32)
    g.img[ya:yb, xa:xb] = (reg * (1 - al) + L[..., 2::-1] * al).astype(np.uint8)


def _env(t, t0, t1, fade=0.25):
    if t < t0 or t > t1: return 0.0, 0.0
    a = min(1.0, (t - t0) / fade, (t1 - t) / fade)
    pop = tk.out_back((t - t0) / 0.35)
    return max(0.0, a), 0.85 + 0.15 * pop


def title(g, text, t, t0, t1, y=230, size=64, col=(255, 255, 255), ink=(30, 30, 34), card=(40, 40, 46)):
    """Big caption near the top of the frame; pops in with overshoot, fades out."""
    a, s = _env(t, t0, t1)
    _draw(g, text, (540, y), size, a, col, ink, card, s)


def note(g, text, c, t, t0, t1, size=44, col=(255, 255, 255), ink=(30, 30, 34), card=None):
    """Small caption at any world position (labels, years, values)."""
    a, s = _env(t, t0, t1, 0.2)
    _draw(g, text, c, size, a, col, ink, card, s)


def clock(g, c, r, hours, face=(250, 250, 248), rim=(60, 60, 66)):
    """Analogue clock face. hours = elapsed time in hours (float); hands turn accordingly."""
    g.disc(c, r, face, 7, rim)
    for i in range(12):
        a = i * math.tau / 12
        g.line((c[0] + r * .78 * math.sin(a), c[1] - r * .78 * math.cos(a)), (c[0] + r * .9 * math.sin(a), c[1] - r * .9 * math.cos(a)), tk.INK, 5)
    am = (hours % 1) * math.tau; ah = (hours % 12) / 12 * math.tau
    g.line(c, (c[0] + r * .48 * math.sin(ah), c[1] - r * .48 * math.cos(ah)), tk.INK, 10)
    g.line(c, (c[0] + r * .72 * math.sin(am), c[1] - r * .72 * math.cos(am)), (40, 40, 200), 6)
    g.disc(c, 8, tk.INK, 0)
