"""Transition renderer shared by the analyser (classify by re-synthesis) and the builder (replay).

render(kind, A, B, P, **params) → frame
  A, B   float32 HxWx3 in 0..255 (outgoing / incoming frames at this output instant)
  P      FFmpeg xfade 'progress': 1.0 = all A … 0.0 = all B   (q = 1 - P is the share of B)

The xfade formulas are ported 1:1 from FFmpeg's libavfilter/vf_xfade.c so a detected 'wipeleft'
replays exactly like ffmpeg's. Custom kinds model what phone editors (CapCut/InShot) do:
zoomblur, blurcross, flash, dipblack, dipwhite, whip*, spin.
"""
from __future__ import annotations

import math

import numpy as np

import mm_img

XFADE = ["fade", "wipeleft", "wiperight", "wipeup", "wipedown", "slideleft", "slideright", "slideup", "slidedown",
         "circlecrop", "rectcrop", "distance", "fadeblack", "fadewhite", "radial", "smoothleft", "smoothright",
         "smoothup", "smoothdown", "circleopen", "circleclose", "vertopen", "vertclose", "horzopen", "horzclose",
         "dissolve", "pixelize", "diagtl", "diagtr", "diagbl", "diagbr", "hlslice", "hrslice", "vuslice", "vdslice",
         "hblur", "fadegrays", "wipetl", "wipetr", "wipebl", "wipebr", "squeezeh", "squeezev", "zoomin",
         "fadefast", "fadeslow", "coverleft", "coverright", "coverup", "coverdown", "revealleft", "revealright",
         "revealup", "revealdown"]
CUSTOM = ["dipblack", "dipwhite", "flash", "blurcross", "zoomblur", "zoomblurout", "whipleft", "whipright",
          "whipup", "whipdown", "spin"]
ALL = XFADE + CUSTOM

# Plain-language Arabic names for reports
AR = {"cut": "قطع مباشر", "fade": "تلاشي متداخل (Crossfade)", "fadeblack": "تلاشي عبر الأسود", "dipblack": "غمس للأسود",
      "fadewhite": "تلاشي عبر الأبيض", "dipwhite": "غمس للأبيض", "flash": "فلاش أبيض", "blurcross": "تمويه متداخل",
      "zoomblur": "زووم + تمويه (CapCut Zoom)", "zoomblurout": "زووم للخارج + تمويه", "zoomin": "زووم للداخل",
      "wipeleft": "مسح لليسار", "wiperight": "مسح لليمين", "wipeup": "مسح لأعلى", "wipedown": "مسح لأسفل",
      "slideleft": "سحب لليسار", "slideright": "سحب لليمين", "slideup": "سحب لأعلى", "slidedown": "سحب لأسفل",
      "smoothleft": "مسح ناعم لليسار", "smoothright": "مسح ناعم لليمين", "smoothup": "مسح ناعم لأعلى",
      "smoothdown": "مسح ناعم لأسفل", "circleopen": "دائرة تفتح", "circleclose": "دائرة تقفل", "dissolve": "ذوبان نقطي",
      "whipleft": "سوايب سريع لليسار", "whipright": "سوايب سريع لليمين", "whipup": "سوايب سريع لأعلى",
      "whipdown": "سوايب سريع لأسفل", "spin": "دوران", "pixelize": "بكسلة", "hblur": "تمويه أفقي",
      "coverleft": "تغطية من اليمين", "coverright": "تغطية من اليسار", "coverup": "تغطية من أسفل",
      "coverdown": "تغطية من أعلى", "revealleft": "كشف لليسار", "revealright": "كشف لليمين",
      "revealup": "كشف لأعلى", "revealdown": "كشف لأسفل"}

# A small prior: prefer the common, simple explanations when two kinds fit about equally well
COMPLEXITY = {k: 0.0 for k in ALL}
COMPLEXITY.update({"fade": 0.0, "fadeblack": 0.01, "dipblack": 0.01, "fadewhite": 0.01, "dipwhite": 0.01,
                   "wipeleft": 0.01, "wiperight": 0.01, "wipeup": 0.01, "wipedown": 0.01, "slideleft": 0.01,
                   "slideright": 0.01, "slideup": 0.01, "slidedown": 0.01, "zoomblur": 0.015, "blurcross": 0.015,
                   "flash": 0.015, "fadefast": 0.03, "fadeslow": 0.03, "distance": 0.05, "fadegrays": 0.03,
                   "dissolve": 0.03, "pixelize": 0.04, "squeezeh": 0.05, "squeezev": 0.05, "radial": 0.04,
                   "hlslice": 0.05, "hrslice": 0.05, "vuslice": 0.05, "vdslice": 0.05, "spin": 0.04,
                   "zoomblurout": 0.03, "circlecrop": 0.05, "rectcrop": 0.05,
                   "whipleft": 0.02, "whipright": 0.02, "whipup": 0.02, "whipdown": 0.02, "cut": 0.0,
                   "coverleft": 0.012, "coverright": 0.012, "coverup": 0.012, "coverdown": 0.012,
                   "revealleft": 0.012, "revealright": 0.012, "revealup": 0.012, "revealdown": 0.012})


def _smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def _mix(a, b, m):
    """FFmpeg's mix(a, b, m) = a*m + b*(1-m)."""
    if isinstance(m, np.ndarray) and m.ndim == 2:
        m = m[..., None]
    return a * m + b * (1.0 - m)


_GRID_CACHE: dict = {}


def _grid(h, w):
    key = (h, w)
    if key not in _GRID_CACHE:
        y, x = np.mgrid[0:h, 0:w].astype(np.float32)
        _GRID_CACHE[key] = (x, y)
    return _GRID_CACHE[key]


def _frand(x, y):
    r = np.sin(x * 12.9898 + y * 78.233) * 43758.545
    return r - np.floor(r)


def _shift_rows(img, z):
    """out[y] = img[(y + z) mod H]."""
    return np.roll(img, -z, axis=0)


def _shift_cols(img, z):
    return np.roll(img, -z, axis=1)


def _zoom(img, z, cx=0.5, cy=0.5, border="reflect"):
    if abs(z - 1.0) < 1e-4:
        return img
    h, w = img.shape[:2]
    M = np.array([[z, 0, (1 - z) * cx * w], [0, z, (1 - z) * cy * h]], np.float32)
    return mm_img.warp_affine(img, M, (w, h), border=border)


def _rotate_zoom(img, deg, z):
    h, w = img.shape[:2]
    a = math.radians(deg)
    c, s = math.cos(a) * z, math.sin(a) * z
    cx, cy = w / 2, h / 2
    M = np.array([[c, -s, cx - c * cx + s * cy], [s, c, cy - s * cx - c * cy]], np.float32)
    return mm_img.warp_affine(img, M, (w, h), border="reflect")


def _motion_blur(img, length, axis):
    length = int(round(length))
    if length < 2:
        return img
    k = np.ones(length, np.float32) / length
    if mm_img.HAVE_CV2:
        ker = k[None, :] if axis == 1 else k[:, None]
        return mm_img.cv2.filter2D(img, -1, ker, borderType=mm_img.cv2.BORDER_REFLECT)
    from scipy.ndimage import convolve1d
    return convolve1d(img, k, axis=axis, mode="reflect")


def render(kind: str, A: np.ndarray, B: np.ndarray, P: float, **prm) -> np.ndarray:
    A = A.astype(np.float32, copy=False)
    B = B.astype(np.float32, copy=False)
    P = float(min(1.0, max(0.0, P)))
    h, w = A.shape[:2]
    x, y = _grid(h, w)
    k = kind
    if k == "cut":
        return A if P >= 0.5 else B
    if k == "fade":
        return _mix(A, B, P)
    if k == "wipeleft":
        z = int(w * P)
        return np.where((x > z)[..., None], B, A)
    if k == "wiperight":
        z = int(w * (1 - P))
        return np.where((x > z)[..., None], A, B)
    if k == "wipeup":
        z = int(h * P)
        return np.where((y > z)[..., None], B, A)
    if k == "wipedown":
        z = int(h * (1 - P))
        return np.where((y > z)[..., None], A, B)
    if k in ("slideleft", "slideright"):
        z = int(-P * w) if k == "slideleft" else int(P * w)
        zx = (z + x).astype(np.int64)
        zz = np.mod(zx, w)
        inside = (zx >= 0) & (zx < w)
        Bs = B[:, zz[0]]
        As = A[:, zz[0]]
        return np.where(inside[..., None], Bs, As)
    if k in ("slideup", "slidedown"):
        z = int(-P * h) if k == "slideup" else int(P * h)
        zy = (z + np.arange(h)).astype(np.int64)
        zz = np.mod(zy, h)
        inside = (zy >= 0) & (zy < h)
        return np.where(inside[:, None, None], B[zz], A[zz])
    if k == "circlecrop":
        z = (2 * abs(P - 0.5)) ** 3 * math.hypot(w / 2, h / 2)
        dist = np.hypot(x - w / 2, y - h / 2)
        val = B if P < 0.5 else A
        return np.where((z < dist)[..., None], 0.0, val)
    if k == "rectcrop":
        zh, zw = int(abs(P - 0.5) * h), int(abs(P - 0.5) * w)
        inside = (np.abs(x - w / 2) < zw) & (np.abs(y - h / 2) < zh)
        val = B if P < 0.5 else A
        return np.where(inside[..., None], val, 0.0)
    if k == "distance":
        d = np.sqrt((((A - B) / 255.0) ** 2).sum(-1)) <= P
        inner = _mix(A, B, d.astype(np.float32))
        return _mix(inner, B, P)
    if k in ("fadeblack", "fadewhite"):
        bg = 0.0 if k == "fadeblack" else 255.0
        ph = 0.2
        return _mix(_mix(A, bg, _smoothstep(1 - ph, 1.0, P)), _mix(bg, B, _smoothstep(ph, 1.0, P)), P)
    if k == "radial":
        smooth = np.arctan2(x - w / 2, y - h / 2) - (P - 0.5) * (math.pi * 2.5)
        return _mix(B, A, _smoothstep(0, 1, smooth))
    if k == "smoothleft":
        return _mix(B, A, _smoothstep(0, 1, 1 + x / w - P * 2))
    if k == "smoothright":
        return _mix(B, A, _smoothstep(0, 1, 1 + (w - 1 - x) / w - P * 2))
    if k == "smoothup":
        return _mix(B, A, _smoothstep(0, 1, 1 + y / h - P * 2))
    if k == "smoothdown":
        return _mix(B, A, _smoothstep(0, 1, 1 + (h - 1 - y) / h - P * 2))
    if k == "circleopen":
        z = math.hypot(w / 2, h / 2)
        return _mix(A, B, _smoothstep(0, 1, np.hypot(x - w / 2, y - h / 2) / z + (P - 0.5) * 3))
    if k == "circleclose":
        z = math.hypot(w / 2, h / 2)
        return _mix(B, A, _smoothstep(0, 1, np.hypot(x - w / 2, y - h / 2) / z + (1 - P - 0.5) * 3))
    if k == "vertopen":
        w2 = w / 2
        return _mix(B, A, _smoothstep(0, 1, 2 - np.abs((x - w2) / w2) - P * 2))
    if k == "vertclose":
        w2 = w / 2
        return _mix(B, A, _smoothstep(0, 1, 1 + np.abs((x - w2) / w2) - P * 2))
    if k == "horzopen":
        h2 = h / 2
        return _mix(B, A, _smoothstep(0, 1, 2 - np.abs((y - h2) / h2) - P * 2))
    if k == "horzclose":
        h2 = h / 2
        return _mix(B, A, _smoothstep(0, 1, 1 + np.abs((y - h2) / h2) - P * 2))
    if k == "dissolve":
        smooth = _frand(x, y) * 2 + P * 2 - 1.5
        return np.where((smooth >= 0.5)[..., None], A, B)
    if k == "pixelize":
        d = min(P, 1 - P)
        dist = math.ceil(d * 50) / 50
        if dist <= 0:
            return _mix(A, B, P)
        sq = 2 * dist * min(w, h) / 20
        sx = np.minimum((np.floor(x / sq) + 0.5) * sq, w - 1).astype(np.int64)
        sy = np.minimum((np.floor(y / sq) + 0.5) * sq, h - 1).astype(np.int64)
        return _mix(A[sy, sx], B[sy, sx], P)
    if k in ("diagtl", "diagtr", "diagbl", "diagbr"):
        xx = x / w if k in ("diagtl", "diagbl") else (w - 1 - x) / w
        yy = y / h if k in ("diagtl", "diagtr") else (h - 1 - y) / h
        return _mix(B, A, _smoothstep(0, 1, 1 + xx * yy - P * 2))
    if k in ("hlslice", "hrslice"):
        xx = x / w if k == "hlslice" else (w - 1 - x) / w
        smooth = _smoothstep(-0.5, 0, xx - P * 1.5)
        ss = np.where(smooth <= (10 * xx - np.floor(10 * xx)), 0.0, 1.0)
        return _mix(B, A, ss)
    if k in ("vuslice", "vdslice"):
        yy = y / h if k == "vuslice" else (h - 1 - y) / h
        smooth = _smoothstep(-0.5, 0, yy - P * 1.5)
        ss = np.where(smooth <= (10 * yy - np.floor(10 * yy)), 0.0, 1.0)
        return _mix(B, A, ss)
    if k == "hblur":
        prog = P * 2 if P <= 0.5 else (1 - P) * 2
        size = 1 + int((w // 2) * prog)
        if size > 1:  # FFmpeg: forward window mean(src[x : x+size]), shrinking at the right edge
            def fwd(img):
                cs = np.concatenate([np.zeros_like(img[:, :1]), np.cumsum(img, axis=1)], axis=1)
                hi = np.minimum(np.arange(w) + size, w)
                return (cs[:, hi] - cs[:, np.arange(w)]) / (hi - np.arange(w))[None, :, None]
            A2, B2 = fwd(A), fwd(B)
        else:
            A2, B2 = A, B
        return _mix(A2, B2, P)
    if k == "fadegrays":
        ga = A.mean(-1, keepdims=True).repeat(3, -1)
        gb = B.mean(-1, keepdims=True).repeat(3, -1)
        return _mix(_mix(A, ga, _smoothstep(0.8, 1, P)), _mix(gb, B, _smoothstep(0.2, 1, P)), P)
    if k in ("wipetl", "wipetr", "wipebl", "wipebr"):
        if k == "wipetl":
            zw, zh = int(w * P), int(h * P)
            mA = (y <= zh) & (x <= zw)
        elif k == "wipetr":
            zw, zh = int(w * (1 - P)), int(h * P)
            mA = (y <= zh) & (x > zw)
        elif k == "wipebl":
            zw, zh = int(w * P), int(h * (1 - P))
            mA = (y > zh) & (x <= zw)
        else:
            zw, zh = int(w * (1 - P)), int(h * (1 - P))
            mA = (y > zh) & (x > zw)
        return np.where(mA[..., None], A, B)
    if k == "squeezeh":
        if P <= 0:
            return B
        z = 0.5 + (np.arange(h) / h - 0.5) / P
        ok = (z >= 0) & (z <= 1)
        yy = np.clip(np.rint(z * (h - 1)), 0, h - 1).astype(np.int64)
        return np.where(ok[:, None, None], A[yy], B)
    if k == "squeezev":
        if P <= 0:
            return B
        z = 0.5 + (np.arange(w) / w - 0.5) / P
        ok = (z >= 0) & (z <= 1)
        xx = np.clip(np.rint(z * (w - 1)), 0, w - 1).astype(np.int64)
        return np.where(ok[None, :, None], A[:, xx], B)
    if k == "zoomin":
        zf = float(_smoothstep(0.5, 1, P))
        u = 0.5 + (x / w - 0.5) * zf
        v = 0.5 + (y / h - 0.5) * zf
        iu = np.clip(np.ceil(u * (w - 1)), 0, w - 1).astype(np.int64)
        iv = np.clip(np.ceil(v * (h - 1)), 0, h - 1).astype(np.int64)
        zv = A[iv, iu]
        return _mix(zv, B, float(_smoothstep(0, 0.5, P)))
    if k in ("fadefast", "fadeslow"):
        d = np.abs(A - B) / 255.0
        ex = 1 + np.log(1 + d) if k == "fadefast" else 1 + np.log(2 - d)
        return _mix(A, B, np.power(P, ex))
    if k in ("coverleft", "coverright"):
        z = int((-P if k == "coverleft" else P) * w)
        zx = z + np.arange(w)
        zz = np.where(zx < 0, zx + w, np.where(zx >= w, zx - w, zx))
        inside = (zx >= 0) & (zx < w)
        return np.where(inside[None, :, None], B[:, zz], A)
    if k in ("coverup", "coverdown"):
        z = int((-P if k == "coverup" else P) * h)
        zy = z + np.arange(h)
        zz = np.where(zy < 0, zy + h, np.where(zy >= h, zy - h, zy))
        inside = (zy >= 0) & (zy < h)
        return np.where(inside[:, None, None], B[zz], A)
    if k in ("revealleft", "revealright"):
        z = int((-P if k == "revealleft" else P) * w)
        zx = z + np.arange(w)
        zz = np.where(zx < 0, zx + w, np.where(zx >= w, zx - w, zx))
        inside = (zx >= 0) & (zx < w)
        return np.where(inside[None, :, None], B, A[:, zz])
    if k in ("revealup", "revealdown"):
        z = int((-P if k == "revealup" else P) * h)
        zy = z + np.arange(h)
        zz = np.where(zy < 0, zy + h, np.where(zy >= h, zy - h, zy))
        inside = (zy >= 0) & (zy < h)
        return np.where(inside[:, None, None], B, A[zz])
    # ------------------------------------------------------------------ custom (phone-editor) kinds
    q = 1.0 - P
    if k in ("dipblack", "dipwhite"):
        bg = 0.0 if k == "dipblack" else 255.0
        mid = prm.get("mid", 0.5)
        if q < mid:
            u = q / mid
            return A * (1 - u) + bg * u
        u = (q - mid) / (1 - mid)
        return bg * (1 - u) + B * u
    if k == "flash":
        peak = prm.get("peak", 0.5)
        width = prm.get("width", 0.5)
        flash = max(0.0, 1 - abs(q - peak) / max(1e-3, width))
        base = _mix(A, B, P)
        return base * (1 - flash) + 255.0 * flash
    if k == "blurcross":
        sig = prm.get("blur", 0.035) * max(h, w)
        s = sig * math.sin(math.pi * q)
        Ab = mm_img.gaussian_blur(A, s) if s > 0.3 else A
        Bb = mm_img.gaussian_blur(B, s) if s > 0.3 else B
        return _mix(Ab, Bb, P)
    if k in ("zoomblur", "zoomblurout"):
        zmax = prm.get("zoom", 0.4)
        bmax = prm.get("blur", 0.02) * max(h, w)
        xmix = prm.get("xmix", 0.12)
        sign = 1 if k == "zoomblur" else -1
        zA = 1 + sign * zmax * _ease_in(min(1.0, q / 0.5))
        zB = 1 + sign * zmax * _ease_in(min(1.0, (1 - q) / 0.5))
        bA = bmax * min(1.0, q / 0.5)
        bB = bmax * min(1.0, (1 - q) / 0.5)
        fa = _zoom(A, zA) if q < 0.5 + xmix else None
        fb = _zoom(B, zB) if q > 0.5 - xmix else None
        if fa is not None and bA > 0.3:
            fa = mm_img.gaussian_blur(fa, bA)
        if fb is not None and bB > 0.3:
            fb = mm_img.gaussian_blur(fb, bB)
        if fa is None:
            return fb
        if fb is None:
            return fa
        m = float(_smoothstep(0.5 - xmix, 0.5 + xmix, q))
        return fa * (1 - m) + fb * m
    if k in ("whipleft", "whipright", "whipup", "whipdown"):
        horiz = k in ("whipleft", "whipright")
        base = render({"whipleft": "slideleft", "whipright": "slideright", "whipup": "slideup",
                       "whipdown": "slidedown"}[k], A, B, P)
        blur = prm.get("blur", 0.08) * (w if horiz else h) * math.sin(math.pi * q)
        return _motion_blur(base, blur, 1 if horiz else 0)
    if k == "spin":
        deg = prm.get("deg", 90.0)
        if q < 0.5:
            u = q / 0.5
            fr = _rotate_zoom(A, deg * u * u, 1 + 0.3 * u)
        else:
            u = (1 - q) / 0.5
            fr = _rotate_zoom(B, -deg * u * u, 1 + 0.3 * u)
        bl = 0.02 * max(h, w) * math.sin(math.pi * q)
        return mm_img.gaussian_blur(fr, bl) if bl > 0.3 else fr
    raise ValueError(f"unknown transition '{kind}'")


def _ease_in(u):
    return u * u


def default_params(kind: str) -> dict:
    return {"zoomblur": {"zoom": 0.4, "blur": 0.02, "xmix": 0.12}, "zoomblurout": {"zoom": 0.3, "blur": 0.02, "xmix": 0.12},
            "blurcross": {"blur": 0.035}, "flash": {"peak": 0.5, "width": 0.5}, "dipblack": {"mid": 0.5},
            "dipwhite": {"mid": 0.5}, "spin": {"deg": 90.0}}.get(kind, {})


PARAM_GRID = {
    "zoomblur": [{"zoom": z, "blur": b, "xmix": 0.12} for z in (0.2, 0.4, 0.7) for b in (0.0, 0.01, 0.025, 0.045)],
    "zoomblurout": [{"zoom": z, "blur": b, "xmix": 0.12} for z in (0.2, 0.35) for b in (0.0, 0.02)],
    "blurcross": [{"blur": b} for b in (0.015, 0.035, 0.06)],
    "flash": [{"peak": 0.5, "width": wd} for wd in (0.25, 0.5)],
    "dipblack": [{"mid": 0.5}], "dipwhite": [{"mid": 0.5}],
    "whipleft": [{"blur": 0.08}], "whipright": [{"blur": 0.08}], "whipup": [{"blur": 0.08}], "whipdown": [{"blur": 0.08}],
    "spin": [{"deg": d} for d in (90.0, 180.0)],
}
