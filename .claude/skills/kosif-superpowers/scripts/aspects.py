"""Flexible aspect ratios / أي مقاس فيديو — shared by kosif.py, import_briefs.py and verify_video.py.

Accepts any of:
  * a ratio "W:H" with integers or decimals: 9:16, 16:9, 1:1, 4:5, 4:3, 3:4, 2:3, 21:9, 2.35:1, 2.39:1, 1.85:1
  * explicit pixels "WxH": 1920x816, 1080x1350, 3840x2160 (kept exactly, rounded to even)
  * a platform or shape name: reel, story, tiktok, shorts, youtube, square, portrait, feed, landscape,
    cinema, scope, ultrawide, classic, vertical, horizontal (Arabic names work too)

resolve(spec) -> (label, width, height). Pixels for a bare ratio follow one rule: ratios between
9:16 and 16:9 get a 1080 px short side (1080x1920, 1440x1080, 1080x1350…); wider or taller ratios get
a 1920 px long side (2.35:1 -> 1920x818). Every dimension is even, as H.264 4:2:0 requires.
Only the standard library is used (Python 3.8+).
"""
from __future__ import annotations

import re
from fractions import Fraction

# Classic presets keep their historical pixel sizes.
PRESETS = {"9:16": (1080, 1920), "16:9": (1920, 1080), "1:1": (1080, 1080), "4:5": (1080, 1350)}

NAMES = {
    "reel": "9:16", "reels": "9:16", "story": "9:16", "stories": "9:16", "tiktok": "9:16", "shorts": "9:16",
    "vertical": "9:16", "portrait-full": "9:16", "ريلز": "9:16", "ستوري": "9:16", "طولي": "9:16", "تيك توك": "9:16",
    "youtube": "16:9", "landscape": "16:9", "horizontal": "16:9", "hd": "16:9", "عرضي": "16:9", "يوتيوب": "16:9",
    "square": "1:1", "مربع": "1:1",
    "feed": "4:5", "portrait": "4:5", "instagram": "4:5", "انستجرام": "4:5",
    "classic": "4:3", "tv": "4:3", "كلاسيكي": "4:3",
    "cinema": "2.39:1", "scope": "2.39:1", "anamorphic": "2.39:1", "سينما": "2.39:1", "سينمائي": "2.39:1",
    "ultrawide": "21:9", "wide": "21:9", "flat": "1.85:1",
}

_RATIO = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*[:/]\s*(\d+(?:\.\d+)?)\s*$")
_PIXELS = re.compile(r"^\s*(\d{2,5})\s*[x×*]\s*(\d{2,5})\s*$", re.I)


def _even(n: float) -> int:
    n = int(round(n))
    return n if n % 2 == 0 else n + 1


def _label(w: float, h: float) -> str:
    """Short human label: 1920x818 -> 2.35:1, 1440x1080 -> 4:3."""
    f = Fraction(w / h).limit_denominator(32)
    if abs(float(f) - w / h) < 0.004 and f.numerator <= 64:
        return f"{f.numerator}:{f.denominator}"
    return f"{w / h:.2f}:1"


def ratio_of(spec: str) -> float:
    """Width/height of any accepted spec (raises ValueError)."""
    return (lambda r: r[1] / r[2])(resolve(spec))


def resolve(spec) -> tuple[str, int, int]:
    """Return (label, width, height) for any ratio, pixel size or name; ValueError if unreadable."""
    if spec is None or str(spec).strip() == "":
        raise ValueError("empty aspect")
    s = str(spec).strip().lower()
    s = NAMES.get(s, s)
    if s in PRESETS:
        w, h = PRESETS[s]
        return s, w, h
    m = _PIXELS.match(s)
    if m:
        w, h = _even(float(m.group(1))), _even(float(m.group(2)))
        return _label(w, h), w, h
    m = _RATIO.match(s)
    if not m:
        raise ValueError(f"unreadable aspect {spec!r}: use W:H (e.g. 21:9, 2.35:1), WxH (1920x816) or a name ({', '.join(sorted(set(NAMES)))})")
    a, b = float(m.group(1)), float(m.group(2))
    if a <= 0 or b <= 0:
        raise ValueError(f"aspect {spec!r} must be positive")
    r = a / b
    if not 0.2 <= r <= 5:
        raise ValueError(f"aspect {spec!r} is outside 1:5 … 5:1")
    if 9 / 16 - 1e-9 <= r <= 16 / 9 + 1e-9:
        w, h = (_even(1080 * r), 1080) if r >= 1 else (1080, _even(1080 / r))
    else:
        w, h = (1920, _even(1920 / r)) if r > 1 else (_even(1920 * r), 1920)
    label = s.replace(" ", "") if _RATIO.match(s) else _label(w, h)
    return label, w, h


def resolution(spec) -> str:
    """'WxH' string for any spec."""
    _, w, h = resolve(spec)
    return f"{w}x{h}"


def is_valid(spec) -> bool:
    try:
        resolve(spec)
        return True
    except ValueError:
        return False
