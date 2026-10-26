"""Contact sheets for review (shots, transitions, text events) — images Claude and the user look at."""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import mm_img
from mm_common import ASSETS, tc

_FONT_CACHE = {}


def font(size: int, arabic: bool = False):
    key = (size, arabic)
    if key in _FONT_CACHE:
        return _FONT_CACHE[key]
    cands = [ASSETS / "fonts" / "Cairo-700.ttf", ASSETS / "fonts" / "Tajawal-Bold.ttf"]
    f = None
    for c in cands:
        if c.exists():
            try:
                f = ImageFont.truetype(str(c), size, layout_engine=ImageFont.Layout.RAQM)
                break
            except Exception:
                try:
                    f = ImageFont.truetype(str(c), size)
                    break
                except Exception:
                    pass
    if f is None:
        f = ImageFont.load_default()
    _FONT_CACHE[key] = f
    return f


def draw_text(d: ImageDraw.ImageDraw, xy, text, size=16, fill=(255, 255, 255), anchor="la"):
    f = font(size)
    kw = {}
    if any("؀" <= c <= "ۿ" for c in text):
        kw = {"direction": "rtl", "language": "ar"}
    try:
        d.text(xy, text, font=f, fill=fill, anchor=anchor, **kw)
    except Exception:
        d.text(xy, text, font=f, fill=fill, anchor=anchor)


def _fit(img: np.ndarray, w: int) -> Image.Image:
    im = Image.fromarray(img.astype(np.uint8))
    h = int(round(im.height * w / im.width))
    return im.resize((w, h), Image.LANCZOS)


def grid(tiles: list[Image.Image], labels: list[str], cols: int, pad: int = 8, label_h: int = 44,
         bg=(18, 18, 22)) -> Image.Image:
    if not tiles:
        return Image.new("RGB", (200, 80), bg)
    tw = max(t.width for t in tiles)
    th = max(t.height for t in tiles)
    rows = (len(tiles) + cols - 1) // cols
    W = cols * (tw + pad) + pad
    H = rows * (th + label_h + pad) + pad
    sheet = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(sheet)
    for i, (t, lab) in enumerate(zip(tiles, labels)):
        r, c = divmod(i, cols)
        x = pad + c * (tw + pad)
        y = pad + r * (th + label_h + pad)
        sheet.paste(t, (x, y))
        for k, line in enumerate(lab.split("\n")[:2]):
            draw_text(d, (x + 2, y + th + 4 + k * 19), line, size=15, fill=(235, 235, 240))
    return sheet


def shots_sheet(spec: dict, P: dict) -> Path:
    tiles, labels = [], []
    for s in spec["shots"]:
        kf = next((k for k in s.get("keyframes", []) if k["tag"] == "mid"), None)
        if not kf:
            continue
        im = np.asarray(Image.open(P["root"] / kf["clean"]).convert("RGB"))
        tiles.append(_fit(im, 220))
        labels.append(f"#{s['id']}  {tc(s['start_s'])}–{tc(s['end_s'])}\n{s['dur_s']:.2f}s  speed {s['motion']['speed']}")
    out = P["sheets"] / "shots.png"
    grid(tiles, labels, cols=min(6, max(1, len(tiles)))).save(out)
    return out


def transitions_sheet(spec: dict, P: dict, feats: dict) -> Path:
    S = feats["small"]
    N = len(S)
    rows = []
    for t in spec["transitions"]:
        a, b = t["ts"], t["te"] - 1
        if t["frames"] == 0:
            idx = [t["ts"] - 2, t["ts"] - 1, t["ts"], t["ts"] + 1]
        else:
            mid = (a + b) // 2
            idx = [a - 1, a, (a + mid) // 2, mid, (mid + b) // 2, b, b + 1]
        idx = [int(np.clip(i, 0, N - 1)) for i in idx]
        strip = [_fit(S[i], 110) for i in idx]
        lab = f"T{t['id']} {t['type']} ({t['frames']}f) @ {tc(t['ts_s'])} conf {t['confidence']}"
        rows.append((strip, lab))
    if not rows:
        img = Image.new("RGB", (400, 60), (18, 18, 22))
        draw_text(ImageDraw.Draw(img), (10, 18), "no transitions detected (single shot)", 16)
        out = P["sheets"] / "transitions.png"
        img.save(out)
        return out
    tw = max(s.width for strip, _ in rows for s in strip)
    th = max(s.height for strip, _ in rows for s in strip)
    W = 7 * (tw + 4) + 12
    H = len(rows) * (th + 30) + 10
    sheet = Image.new("RGB", (W, H), (18, 18, 22))
    d = ImageDraw.Draw(sheet)
    for r, (strip, lab) in enumerate(rows):
        y = 6 + r * (th + 30)
        draw_text(d, (8, y), lab, 15, (255, 220, 140))
        for c, im in enumerate(strip):
            sheet.paste(im, (8 + c * (tw + 4), y + 22))
    out = P["sheets"] / "transitions.png"
    sheet.save(out)
    return out


def text_sheet(spec: dict, P: dict) -> Path:
    tiles, labels = [], []
    for e in spec["texts"]:
        zp = P["root"] / e["crops"]["zone"]
        im = np.asarray(Image.open(zp).convert("RGB"))
        tiles.append(_fit(im, 420))
        t = e["time"]
        ocr = " | ".join(l.get("ocr", "") for l in e["lines"])
        labels.append(f"E{e['id']} {tc(t['in_start_s'])} - {tc(t['out_end_s'])} in:{e['anim_in']['type']} out:{e['anim_out']['type']}"
                      f" fill {e['style'].get('fill')}\nOCR: {ocr[:60]}")
    out = P["sheets"] / "texts.png"
    grid(tiles, labels, cols=2 if len(tiles) > 1 else 1, label_h=46).save(out)
    return out


def all_sheets(spec: dict, P: dict, feats: dict) -> list[Path]:
    out = [shots_sheet(spec, P), transitions_sheet(spec, P, feats)]
    if spec.get("texts"):
        out.append(text_sheet(spec, P))
    return out


def side_by_side(a: np.ndarray, b: np.ndarray, la: str = "REFERENCE", lb: str = "REMAKE", w: int = 300) -> Image.Image:
    A, B = _fit(a, w), _fit(b, w)
    sheet = Image.new("RGB", (2 * w + 12, max(A.height, B.height) + 30), (18, 18, 22))
    sheet.paste(A, (4, 26))
    sheet.paste(B, (w + 8, 26))
    d = ImageDraw.Draw(sheet)
    draw_text(d, (6, 4), la, 15, (200, 200, 210))
    draw_text(d, (w + 10, 4), lb, 15, (255, 220, 140))
    return sheet
