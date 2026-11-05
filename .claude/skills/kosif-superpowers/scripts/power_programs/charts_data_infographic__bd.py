"""DATA-91 Data-in-Motion dark style: render bar-chart frames from clean CSV with the card's tokens."""
from __future__ import annotations
import csv
import io
from pathlib import Path
from ._mind_common import save, eq, truth

BG = (0x0D, 0x1B, 0x2A)
CARD_SERIES = ("#3B82F6", "#F59E0B", "#10B981", "#EF4444", "#A855F7")  # the card's tokens (the known answer)
CARD_BG = (0x0D, 0x1B, 0x2A)
SERIES = list(CARD_SERIES)  # what the renderer uses
STAGGER = 0.060


def hexrgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def ease_out(t):
    t = min(1.0, max(0.0, t))
    return 1 - (1 - t) ** 3


def frame(values, t, dur=0.6, W=540, H=960):
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    vmax = max(values)
    base, top, n = H - 120, 160, len(values)
    bw = (W - 80) // n - 20
    heights = []
    for i, v in enumerate(values):
        p = ease_out((t - i * STAGGER) / dur)
        hgt = int((base - top) * (v / vmax) * p)
        x = 40 + i * (bw + 20)
        d.rectangle([x, base - hgt, x + bw, base], fill=hexrgb(SERIES[i % 5]))
        heights.append(hgt)
    d.line([30, base, W - 30, base], fill=(200, 210, 220), width=2)  # fixed axis
    return img, heights


def data91(work):
    work = Path(work)
    src = "region,value\nA,40\nB,75\nC,55\nD,90\nE,30\n"
    rows = list(csv.DictReader(io.StringIO(src)))
    vals = [int(r["value"]) for r in rows]
    shots = {}
    for t in (0.0, 0.03, 0.3, 1.2):
        img, hs = frame(vals, t)
        img.save(work / f"t{t:.2f}.png")
        shots[t] = (img, hs)
    img, hs = shots[1.2]
    px_bg = img.getpixel((5, 5))
    px_bar = [img.getpixel((40 + i * ((540 - 80) // 5) + 5, 960 - 125)) for i in range(5)]
    save(work, "tokens.json", {"bg": "#0D1B2A", "series": SERIES, "stagger_ms": 60, "values": vals,
                               "final_heights": hs})
    order = sorted(range(5), key=lambda i: vals[i])
    return [eq("background token", px_bg, CARD_BG),
            eq("bar colours are the CVD-safe series", px_bar, [hexrgb(c) for c in CARD_SERIES]),
            eq("frame 0 is empty", sum(shots[0.0][1]), 0),
            truth("stagger: at 30 ms only bar 1 has started", shots[0.03][1][0] > 0 and all(h == 0 for h in shots[0.03][1][1:]),
                  shots[0.03][1]),
            eq("final heights rank like the data", sorted(range(5), key=lambda i: hs[i]), order)]


PROGRAMS = {"DATA-91": data91}
