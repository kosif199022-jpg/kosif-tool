"""Arabic-correct text rendering for the remake.

Engines
  pil  Pillow + libraqm (HarfBuzz/FriBiDi shaping) — default when available
  ass  ffmpeg/libass rendered on black and on white, alpha recovered by two-background matting
       (works on machines whose Pillow has no raqm, e.g. stock Windows wheels)

render_line(text, font_path, size) → Line(alpha HxW float32, ink bbox, per-word alphas in reading order)
compose(alpha, style) → RGBA float32 layer with fill / outline / shadow / glow / box
"""
from __future__ import annotations

import os
import subprocess
import tempfile
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, features

import mm_color
import mm_img
from mm_common import ffmpeg, has_arabic, is_ltr_word, log

HAVE_RAQM = bool(features.check("raqm"))
PAD = 8


@dataclass
class Line:
    text: str
    alpha: np.ndarray                     # H×W float32 0..1
    ink: tuple[int, int, int, int]        # x0, y0, x1, y1 in alpha coords
    words: list[np.ndarray] = field(default_factory=list)
    word_boxes: list[tuple[int, int, int, int]] = field(default_factory=list)

    @property
    def ink_h(self):
        return self.ink[3] - self.ink[1]

    @property
    def ink_w(self):
        return self.ink[2] - self.ink[0]


def engine_name(pref: str = "auto") -> str:
    if pref in ("pil", "ass"):
        return pref
    return "pil" if HAVE_RAQM else "ass"


@lru_cache(maxsize=256)
def _font(path: str, size: int):
    if HAVE_RAQM:
        return ImageFont.truetype(path, size, layout_engine=ImageFont.Layout.RAQM)
    return ImageFont.truetype(path, size)


def _ink_bbox(a: np.ndarray, thr: float = 0.08):
    ys, xs = np.nonzero(a > thr)
    if len(xs) == 0:
        return (0, 0, 1, 1)
    return (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)


def _pil_draw(text, font, W, H, anchor_xy, anchor, direction, lang):
    im = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(im)
    kw = {}
    if HAVE_RAQM:
        kw = {"direction": direction}
        if lang:
            kw["language"] = lang
    d.text(anchor_xy, text, font=font, fill=255, anchor=anchor, **kw)
    return np.asarray(im, np.float32) / 255.0


def render_line_pil(text: str, font_path: str, size: int) -> Line:
    font = _font(str(font_path), int(size))
    rtl = has_arabic(text)
    direction = "rtl" if rtl else "ltr"
    lang = "ar" if rtl else None
    anchor = "rs" if rtl else "ls"  # baseline anchor at the reading start (right edge for Arabic)
    kw = {"direction": direction}
    if lang:
        kw["language"] = lang
    if not HAVE_RAQM:
        kw = {}
    l, t, r, b = font.getbbox(text, anchor=anchor, **kw)
    W = int(np.ceil(r - l)) + 2 * PAD + 4
    H = int(np.ceil(b - t)) + 2 * PAD + 4
    ax, ay = PAD + 2 - l, PAD + 2 - t
    full = _pil_draw(text, font, W, H, (ax, ay), anchor, direction, lang)
    # make sure nothing is clipped; if so, grow the canvas and redraw
    ink = _ink_bbox(full)
    if ink[0] <= 1 or ink[2] >= W - 1 or ink[1] <= 1 or ink[3] >= H - 1:
        W2, H2 = W + 2 * size, H + size
        ax += size
        ay += size // 2
        full = _pil_draw(text, font, W2, H2, (ax, ay), anchor, direction, lang)
        W, H = W2, H2
    words = text.split()
    word_alphas = []
    if len(words) > 1:
        prev = np.zeros_like(full)
        for k in range(1, len(words) + 1):
            pre = " ".join(words[:k])
            cur = _pil_draw(pre, font, W, H, (ax, ay), anchor, direction, lang)
            word_alphas.append(np.clip(cur - prev, 0, 1))
            prev = np.maximum(prev, cur)
        # residual (kerning differences) goes to the last word so the sum equals the full line
        resid = np.clip(full - np.clip(sum(word_alphas), 0, 1), 0, 1)
        word_alphas[-1] = np.clip(word_alphas[-1] + resid, 0, 1)
    else:
        word_alphas = [full]
    return _crop_line(Line(text, full, _ink_bbox(full), word_alphas))


def _crop_line(L: Line, margin: int = PAD) -> Line:
    x0, y0, x1, y1 = L.ink
    H, W = L.alpha.shape
    cx0, cy0 = max(0, x0 - margin), max(0, y0 - margin)
    cx1, cy1 = min(W, x1 + margin), min(H, y1 + margin)
    sl = (slice(cy0, cy1), slice(cx0, cx1))
    words = [w[sl] for w in L.words]
    a = L.alpha[sl]
    return Line(L.text, np.ascontiguousarray(a), _ink_bbox(a), [np.ascontiguousarray(w) for w in words],
                [_ink_bbox(w) for w in words])


# ----------------------------------------------------------------------------- libass engine

def _font_family(path: str) -> str:
    try:
        from fontTools.ttLib import TTFont
        f = TTFont(path, lazy=True, fontNumber=0)
        return f["name"].getDebugName(1) or Path(path).stem
    except Exception:
        return Path(path).stem


def _ass_render(text_tagged: str, font_path: str, size: int, W: int, H: int, bg: str) -> np.ndarray:
    fam = _font_family(font_path)
    tmp = Path(tempfile.mkdtemp(prefix="mm-ass-"))
    fontsdir = Path(font_path).parent
    ass = tmp / "t.ass"
    ass.write_text(
        "[Script Info]\nScriptType: v4.00+\nPlayResX: %d\nPlayResY: %d\nScaledBorderAndShadow: yes\n\n"
        "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
        "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
        "Alignment, MarginL, MarginR, MarginV, Encoding\n"
        "Style: T,%s,%d,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,-1\n\n"
        "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
        "Dialogue: 0,0:00:00.00,0:00:05.00,T,,0,0,0,,{\\an5\\pos(%d,%d)}%s\n" % (W, H, fam, size, W // 2, H // 2, text_tagged),
        encoding="utf-8")
    out = tmp / "o.png"
    vf = f"ass='{ass.as_posix()}':fontsdir='{fontsdir.as_posix()}'"
    subprocess.run([ffmpeg(), "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c={bg}:s={W}x{H}:d=0.04",
                    "-vf", vf, "-frames:v", "1", str(out)], check=True, capture_output=True)
    arr = np.asarray(Image.open(out).convert("RGB"), np.float32) / 255.0
    for p in (ass, out):
        p.unlink(missing_ok=True)
    tmp.rmdir()
    return arr


def _ass_alpha(tagged: str, font_path: str, size: int, W: int, H: int) -> np.ndarray:
    blk = _ass_render(tagged, font_path, size, W, H, "black")
    wht = _ass_render(tagged, font_path, size, W, H, "white")
    # white text: on black → a ; on white → 1 → alpha = blk (any channel), sanity via matting
    a = 1.0 - (wht - blk).mean(-1)
    return np.clip(a, 0, 1).astype(np.float32)


def render_line_ass(text: str, font_path: str, size: int) -> Line:
    W = int(size * (len(text) * 0.75 + 4))
    H = int(size * 2.6)
    esc = text.replace("{", "(").replace("}", ")")
    full = _ass_alpha(esc, font_path, size, W, H)
    words = text.split()
    word_alphas = []
    if len(words) > 1:
        for k in range(len(words)):
            parts = []
            for j, wd in enumerate(words):
                tag = "{\\alpha&H00&}" if j == k else "{\\alpha&HFF&}"
                parts.append(tag + wd)
            word_alphas.append(_ass_alpha(" ".join(parts), font_path, size, W, H))
    else:
        word_alphas = [full]
    return _crop_line(Line(text, full, _ink_bbox(full), word_alphas))


def render_line(text: str, font_path: str, size: int, engine: str = "auto") -> Line:
    eng = engine_name(engine)
    if eng == "pil":
        return render_line_pil(text, font_path, size)
    return render_line_ass(text, font_path, size)


# ----------------------------------------------------------------------------- fitting

def fit_size(text: str, font_path: str, target_ink_h: float, engine: str = "auto", guess: int | None = None) -> tuple[int, Line]:
    """Font size (px) whose rendered ink height matches target_ink_h."""
    size = int(guess or max(8, round(target_ink_h * 1.05)))
    best = None
    for _ in range(5):
        L = render_line(text, font_path, size, engine)
        h = max(1, L.ink_h)
        err = abs(h - target_ink_h)
        if best is None or err < best[0]:
            best = (err, size, L)
        if err <= 0.6:
            break
        size = max(6, int(round(size * target_ink_h / h)))
        if best and size == best[1]:
            break
    return best[1], best[2]


# ----------------------------------------------------------------------------- styling

def _dilate_alpha(a: np.ndarray, r: float) -> np.ndarray:
    if r <= 0.25:
        return a
    ri = int(np.ceil(r))
    if mm_img.HAVE_CV2:
        k = mm_img.cv2.getStructuringElement(mm_img.cv2.MORPH_ELLIPSE, (2 * ri + 1, 2 * ri + 1))
        return mm_img.cv2.dilate(a, k)
    from scipy.ndimage import grey_dilation
    y, x = np.ogrid[-ri:ri + 1, -ri:ri + 1]
    return grey_dilation(a, footprint=(x * x + y * y <= ri * ri))


def compose(alpha: np.ndarray, style: dict, scale: float = 1.0) -> tuple[np.ndarray, tuple[int, int]]:
    """RGBA (premultiplied, float 0..1) of the styled text and the offset of `alpha` inside it.

    style keys: fill '#RRGGBB', opacity, outline{color,width_px}, shadow{dx_px,dy_px,blur_px,opacity,color},
    glow{radius_px,strength,color}, box{color,opacity,pad_px,radius_px}. Pixel sizes are at source
    resolution; `scale` converts them when rendering at another resolution."""
    sh = style.get("shadow") or None
    gl = style.get("glow") or None
    ol = style.get("outline") or None
    bx = style.get("box") or None
    m = 2
    if sh:
        m = max(m, int(abs(sh.get("dx_px", 0)) * scale + abs(sh.get("dy_px", 0)) * scale + 3 * sh.get("blur_px", 0) * scale + 4))
    if gl:
        m = max(m, int(3 * gl.get("radius_px", 4) * scale + 4))
    if ol:
        m = max(m, int(ol.get("width_px", 1) * scale + 3))
    if bx:
        m = max(m, int(bx.get("pad_px", 12) * scale + 4))
    H, W = alpha.shape
    A = np.zeros((H + 2 * m, W + 2 * m), np.float32)
    A[m:m + H, m:m + W] = alpha
    out = np.zeros((H + 2 * m, W + 2 * m, 4), np.float32)

    def over(rgb, a):
        a = np.clip(a, 0, 1)[..., None]
        out[..., :3] = rgb[None, None, :] * a + out[..., :3] * (1 - a)
        out[..., 3:4] = a + out[..., 3:4] * (1 - a)

    if bx:
        ys, xs = np.nonzero(A > 0.05)
        if len(xs):
            pad = int(bx.get("pad_px", 12) * scale)
            box = np.zeros_like(A)
            box[max(0, ys.min() - pad):ys.max() + pad, max(0, xs.min() - pad):xs.max() + pad] = 1.0
            r = bx.get("radius_px", 0) * scale
            if r > 1:
                box = mm_img.gaussian_blur(box, r / 2.5)
                box = np.clip((box - 0.5) * 4 + 0.5, 0, 1)
            over(np.array(mm_color.rgb_of(bx.get("color", "#000000")), np.float32) / 255, box * bx.get("opacity", 0.6))
    base = A
    if ol and ol.get("width_px", 0) > 0:
        base = _dilate_alpha(A, ol["width_px"] * scale)
    if sh:
        dx, dy = int(round(sh.get("dx_px", 0) * scale)), int(round(sh.get("dy_px", 0) * scale))
        S = np.roll(np.roll(base, dy, 0), dx, 1)
        b = sh.get("blur_px", 0) * scale
        if b > 0.3:
            S = mm_img.gaussian_blur(S, b)
        over(np.array(mm_color.rgb_of(sh.get("color", "#000000")), np.float32) / 255, S * sh.get("opacity", 0.5))
    if gl:
        Gl = mm_img.gaussian_blur(_dilate_alpha(A, gl.get("radius_px", 4) * scale * 0.5), gl.get("radius_px", 4) * scale)
        over(np.array(mm_color.rgb_of(gl.get("color", "#FFFFFF")), np.float32) / 255, Gl * gl.get("strength", 0.4) * 2)
    if ol and ol.get("width_px", 0) > 0:
        over(np.array(mm_color.rgb_of(ol.get("color", "#000000")), np.float32) / 255, base)
    fill = np.array(mm_color.rgb_of(style.get("fill", "#FFFFFF")), np.float32) / 255
    over(fill, A * style.get("opacity", 1.0))
    # to premultiplied
    out[..., :3] *= 1.0  # 'over' above already accumulates premultiplied colour
    return out, (m, m)


def composite(frame: np.ndarray, layer: np.ndarray, x: float, y: float, alpha_mul: float = 1.0) -> np.ndarray:
    """Alpha-composite a premultiplied RGBA layer (float 0..1) onto an RGB uint8/float frame at (x, y)."""
    H, W = frame.shape[:2]
    h, w = layer.shape[:2]
    xi, yi = int(np.floor(x)), int(np.floor(y))
    fx, fy = x - xi, y - yi
    if abs(fx) > 1e-3 or abs(fy) > 1e-3:  # sub-pixel placement
        M = np.array([[1, 0, fx], [0, 1, fy]], np.float32)
        layer = mm_img.warp_affine(layer, M, (w + 1, h + 1), border="constant")
        h, w = layer.shape[:2]
    x0, y0 = max(0, xi), max(0, yi)
    x1, y1 = min(W, xi + w), min(H, yi + h)
    if x1 <= x0 or y1 <= y0:
        return frame
    L = layer[y0 - yi:y1 - yi, x0 - xi:x1 - xi]
    a = L[..., 3:4] * alpha_mul
    region = frame[y0:y1, x0:x1].astype(np.float32)
    region = L[..., :3] * 255.0 * alpha_mul + region * (1 - a)
    frame[y0:y1, x0:x1] = np.clip(region, 0, 255).astype(frame.dtype) if frame.dtype == np.uint8 else region
    return frame
