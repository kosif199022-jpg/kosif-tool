"""KOSIF faces — one face detector for the whole kit (smart reframe, privacy blur, text placement), with honest fallbacks.

Detectors, best first:
  yunet   OpenCV FaceDetectorYN (DNN). Needs the model file `face_detection_yunet_2023mar.onnx` in scripts/kit/models/
          (or KOSIF_YUNET=path). It is not downloaded automatically: fetch it from the OpenCV Zoo
          (https://github.com/opencv/opencv_zoo/tree/main/models/face_detection_yunet) and drop it there.
  haar    OpenCV CascadeClassifier with haarcascade_frontalface_default.xml (builds that ship cv2.data).
  skin    A measured skin-colour heuristic (YCrCb thresholds → connected blobs of a face-like size and aspect). Works
          without any model; finds skin, not identity — hands and necks count — so it over-protects rather than misses.

    faces.detect(rgb) → [(x, y, w, h, score)]     faces.which() → the detector name
"""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
MODEL = Path(os.environ.get("KOSIF_YUNET") or HERE / "kit" / "models" / "face_detection_yunet_2023mar.onnx")
_DET: dict | None = None


def _load() -> dict:
    global _DET
    if _DET is not None:
        return _DET
    det: dict = {"name": "skin", "cv2": None}
    try:
        import cv2
        det["cv2"] = cv2
        if MODEL.exists() and hasattr(cv2, "FaceDetectorYN"):
            det["name"], det["yn"], det["yn_size"] = "yunet", cv2.FaceDetectorYN.create(str(MODEL), "", (320, 320), 0.7, 0.3, 5000), (320, 320)
        elif hasattr(cv2, "CascadeClassifier") and hasattr(cv2, "data"):
            xml = Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml"
            if xml.exists():
                c = cv2.CascadeClassifier(str(xml))
                if not c.empty():
                    det["name"], det["haar"] = "haar", c
    except ImportError:
        pass
    _DET = det
    return det


def which() -> str:
    return _load()["name"]


def detect(rgb: np.ndarray, min_frac: float = 0.004) -> list[tuple[int, int, int, int, float]]:
    """Faces in an RGB frame as (x, y, w, h, score). `min_frac`: smallest face area as a share of the frame."""
    det = _load()
    h, w = rgb.shape[:2]
    if det["name"] == "yunet":
        cv2 = det["cv2"]
        if det["yn_size"] != (w, h):
            det["yn"].setInputSize((w, h)); det["yn_size"] = (w, h)
        _, faces = det["yn"].detect(cv2.cvtColor(np.ascontiguousarray(rgb), cv2.COLOR_RGB2BGR))
        out = []
        for f in (faces if faces is not None else []):
            x, y, fw, fh, score = float(f[0]), float(f[1]), float(f[2]), float(f[3]), float(f[-1])
            if fw * fh >= min_frac * w * h:
                out.append((int(max(0, x)), int(max(0, y)), int(fw), int(fh), round(score, 3)))
        return out
    if det["name"] == "haar":
        cv2 = det["cv2"]
        g = cv2.cvtColor(np.ascontiguousarray(rgb), cv2.COLOR_RGB2GRAY)
        side = int((min_frac * w * h) ** 0.5)
        return [(int(x), int(y), int(fw), int(fh), 1.0) for (x, y, fw, fh) in det["haar"].detectMultiScale(g, 1.15, 5, minSize=(max(20, side), max(20, side)))]
    return skin_boxes(rgb, min_frac)


def skin_boxes(rgb: np.ndarray, min_frac: float = 0.004) -> list[tuple[int, int, int, int, float]]:
    """Skin-coloured blobs with a face-like aspect, on a 1/4-size copy; the score is the blob's fill ratio."""
    from scipy import ndimage
    h, w = rgb.shape[:2]
    s = 4 if min(h, w) >= 480 else 2 if min(h, w) >= 200 else 1
    small = rgb[::s, ::s].astype(np.float32)
    r, g, b = small[..., 0], small[..., 1], small[..., 2]
    y = 0.299 * r + 0.587 * g + 0.114 * b
    cr = 128 + 0.5 * r - 0.4187 * g - 0.0813 * b
    cb = 128 - 0.1687 * r - 0.3313 * g + 0.5 * b
    mask = (cr > 135) & (cr < 175) & (cb > 80) & (cb < 128) & (y > 50) & (r > g) & (r > b)
    mask = ndimage.binary_opening(mask, iterations=1)
    mask = ndimage.binary_closing(mask, iterations=2)
    lab, n = ndimage.label(mask)
    out = []
    if n == 0:
        return out
    sl = ndimage.find_objects(lab)
    area_min = min_frac * (h // s) * (w // s)
    for i, obj in enumerate(sl, start=1):
        if obj is None:
            continue
        ys, xs = obj
        bw, bh = xs.stop - xs.start, ys.stop - ys.start
        area = int((lab[obj] == i).sum())
        if area < area_min or bw < 6 or bh < 6:
            continue
        aspect = bw / bh
        if not (0.45 <= aspect <= 1.6):
            continue
        fill = area / (bw * bh)
        if fill < 0.35:
            continue
        out.append((int(xs.start * s), int(ys.start * s), int(bw * s), int(bh * s), round(float(fill), 3)))
    out.sort(key=lambda t: -(t[2] * t[3]))
    return out[:12]


def centre(rgb: np.ndarray) -> tuple[float, float] | None:
    """The area-weighted centre of the faces as a share of the frame, or None."""
    f = detect(rgb)
    if not f:
        return None
    h, w = rgb.shape[:2]
    wts = np.array([b[2] * b[3] for b in f], np.float32)
    xs = np.array([(b[0] + b[2] / 2) / w for b in f]); ys = np.array([(b[1] + b[3] / 2) / h for b in f])
    return float(np.average(xs, weights=wts)), float(np.average(ys, weights=wts))
