"""Image operations with OpenCV when present and NumPy/SciPy/Pillow fallbacks otherwise.

All functions take/return NumPy arrays. Grey images are HxW, colour images HxWx3 (RGB order).
"""
from __future__ import annotations

import numpy as np

try:  # OpenCV is optional but much faster
    import cv2  # type: ignore
    cv2.setNumThreads(max(1, (cv2.getNumberOfCPUs() or 2)))
except Exception:  # pragma: no cover
    cv2 = None

try:
    from scipy import ndimage as ndi  # type: ignore
except Exception:  # pragma: no cover
    ndi = None

from PIL import Image, ImageFilter

HAVE_CV2 = cv2 is not None


def to_gray(rgb: np.ndarray) -> np.ndarray:
    rgb = rgb.astype(np.float32)
    return rgb[..., 0] * 0.299 + rgb[..., 1] * 0.587 + rgb[..., 2] * 0.114


def resize(img: np.ndarray, size: tuple[int, int], interp: str = "area") -> np.ndarray:
    """size = (w, h)."""
    w, h = int(size[0]), int(size[1])
    if img.shape[1] == w and img.shape[0] == h:
        return img
    if HAVE_CV2:
        flag = {"area": cv2.INTER_AREA, "linear": cv2.INTER_LINEAR, "cubic": cv2.INTER_CUBIC,
                "nearest": cv2.INTER_NEAREST, "lanczos": cv2.INTER_LANCZOS4}[interp]
        return cv2.resize(img, (w, h), interpolation=flag)
    dtype = img.dtype
    mode = {"area": Image.BOX, "linear": Image.BILINEAR, "cubic": Image.BICUBIC,
            "nearest": Image.NEAREST, "lanczos": Image.LANCZOS}[interp]
    if img.dtype == np.bool_:
        out = np.asarray(Image.fromarray(img.astype(np.uint8) * 255).resize((w, h), mode)) > 127
        return out
    if img.dtype != np.uint8:
        chans = [np.asarray(Image.fromarray(img[..., c].astype(np.float32), "F").resize((w, h), mode))
                 for c in range(img.shape[2])] if img.ndim == 3 else \
            [np.asarray(Image.fromarray(img.astype(np.float32), "F").resize((w, h), mode))]
        out = np.stack(chans, -1) if img.ndim == 3 else chans[0]
        return out.astype(dtype)
    return np.asarray(Image.fromarray(img).resize((w, h), mode))


def gaussian_blur(img: np.ndarray, sigma: float) -> np.ndarray:
    if sigma <= 0.05:
        return img
    if HAVE_CV2:
        k = int(max(3, round(sigma * 3) * 2 + 1))
        return cv2.GaussianBlur(img, (k, k), sigma, borderType=cv2.BORDER_REFLECT)
    if ndi is not None:
        if img.ndim == 3:
            return ndi.gaussian_filter(img, sigma=(sigma, sigma, 0), mode="reflect")
        return ndi.gaussian_filter(img, sigma=sigma, mode="reflect")
    dtype = img.dtype
    if img.ndim == 2:
        return np.asarray(Image.fromarray(img.astype(np.float32), "F").filter(ImageFilter.GaussianBlur(sigma))).astype(dtype)
    return np.stack([gaussian_blur(img[..., c], sigma) for c in range(img.shape[2])], -1)


def box_blur(img: np.ndarray, k: int) -> np.ndarray:
    k = max(1, int(k))
    if HAVE_CV2:
        return cv2.blur(img, (k, k), borderType=cv2.BORDER_REFLECT)
    if ndi is not None:
        size = (k, k, 1) if img.ndim == 3 else (k, k)
        return ndi.uniform_filter(img.astype(np.float32), size=size, mode="reflect").astype(img.dtype)
    return gaussian_blur(img, k / 2.5)


def _disk(r: int) -> np.ndarray:
    r = max(0, int(r))
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return (x * x + y * y <= r * r + r * 0.5).astype(np.uint8)


def _rect(kw: int, kh: int) -> np.ndarray:
    return np.ones((max(1, int(kh)), max(1, int(kw))), np.uint8)


def _morph_src(mask: np.ndarray) -> np.ndarray:
    if mask.dtype in (np.bool_, np.uint8, np.float32):
        return mask
    if np.issubdtype(mask.dtype, np.integer) and mask.min() >= 0 and mask.max() <= 255:
        return mask.astype(np.uint8)
    return mask.astype(np.float32)


def dilate(mask: np.ndarray, r: int = 1, shape: str = "disk", kw: int | None = None, kh: int | None = None) -> np.ndarray:
    if r <= 0 and kw is None:
        return mask
    mask = _morph_src(mask)
    k = _rect(kw, kh) if kw is not None else (_disk(r) if shape == "disk" else _rect(2 * r + 1, 2 * r + 1))
    if HAVE_CV2:
        src = mask.astype(np.uint8) if mask.dtype == np.bool_ else mask
        out = cv2.dilate(src, k)
        return out.astype(bool) if mask.dtype == np.bool_ else out
    if ndi is not None:
        if mask.dtype == np.bool_:
            return ndi.binary_dilation(mask, structure=k.astype(bool))
        return ndi.grey_dilation(mask, footprint=k.astype(bool))
    raise RuntimeError("dilate needs OpenCV or SciPy")


def erode(mask: np.ndarray, r: int = 1, shape: str = "disk", kw: int | None = None, kh: int | None = None) -> np.ndarray:
    if r <= 0 and kw is None:
        return mask
    mask = _morph_src(mask)
    k = _rect(kw, kh) if kw is not None else (_disk(r) if shape == "disk" else _rect(2 * r + 1, 2 * r + 1))
    if HAVE_CV2:
        src = mask.astype(np.uint8) if mask.dtype == np.bool_ else mask
        out = cv2.erode(src, k)
        return out.astype(bool) if mask.dtype == np.bool_ else out
    if ndi is not None:
        if mask.dtype == np.bool_:
            return ndi.binary_erosion(mask, structure=k.astype(bool))
        return ndi.grey_erosion(mask, footprint=k.astype(bool))
    raise RuntimeError("erode needs OpenCV or SciPy")


def close(mask, r=1, **kw):
    return erode(dilate(mask, r, **kw), r, **kw)


def open_(mask, r=1, **kw):
    return dilate(erode(mask, r, **kw), r, **kw)


def tophat(gray: np.ndarray, k: int, dark: bool = False) -> np.ndarray:
    """White (bright thin structures) or black top-hat with a square k×k kernel. gray float32 0..255."""
    g = gray.astype(np.float32)
    if HAVE_CV2:
        ker = cv2.getStructuringElement(cv2.MORPH_RECT, (k, k))
        op = cv2.MORPH_BLACKHAT if dark else cv2.MORPH_TOPHAT
        return cv2.morphologyEx(g, op, ker)
    if ndi is not None:
        if dark:
            return ndi.grey_closing(g, size=(k, k)) - g
        return g - ndi.grey_opening(g, size=(k, k))
    raise RuntimeError("tophat needs OpenCV or SciPy")


def label(mask: np.ndarray):
    """Connected components (8-connectivity). Returns (n, labels, stats) where stats rows are
    [x, y, w, h, area] for labels 1..n-1 (row 0 = background), like OpenCV."""
    m = mask.astype(np.uint8)
    if HAVE_CV2:
        n, lab, stats, _ = cv2.connectedComponentsWithStats(m, connectivity=8)
        return n, lab, stats
    if ndi is None:
        raise RuntimeError("label needs OpenCV or SciPy")
    lab, n = ndi.label(m, structure=np.ones((3, 3)))
    stats = np.zeros((n + 1, 5), np.int64)
    objs = ndi.find_objects(lab)
    for i, sl in enumerate(objs, start=1):
        if sl is None:
            continue
        ys, xs = sl
        stats[i] = [xs.start, ys.start, xs.stop - xs.start, ys.stop - ys.start, int((lab[sl] == i).sum())]
    stats[0, 4] = int((lab == 0).sum())
    return n + 1, lab, stats


def warp_affine(img: np.ndarray, M: np.ndarray, size: tuple[int, int], border: str = "reflect",
                interp: str = "linear") -> np.ndarray:
    w, h = size
    if HAVE_CV2:
        b = {"reflect": cv2.BORDER_REFLECT101, "constant": cv2.BORDER_CONSTANT,
             "replicate": cv2.BORDER_REPLICATE}[border]
        flag = {"linear": cv2.INTER_LINEAR, "cubic": cv2.INTER_CUBIC, "nearest": cv2.INTER_NEAREST}[interp]
        return cv2.warpAffine(img, M.astype(np.float32), (w, h), flags=flag, borderMode=b)
    # Pillow wants the inverse map (output → input)
    A = np.vstack([M, [0, 0, 1]])
    inv = np.linalg.inv(A)
    coeffs = (inv[0, 0], inv[0, 1], inv[0, 2], inv[1, 0], inv[1, 1], inv[1, 2])
    im = Image.fromarray(img)
    return np.asarray(im.transform((w, h), Image.AFFINE, coeffs, resample=Image.BILINEAR))


def laplacian_abs(gray: np.ndarray) -> np.ndarray:
    g = gray.astype(np.float32)
    if HAVE_CV2:
        return np.abs(cv2.Laplacian(g, cv2.CV_32F, ksize=3))
    out = np.zeros_like(g)
    out[1:-1, 1:-1] = np.abs(g[:-2, 1:-1] + g[2:, 1:-1] + g[1:-1, :-2] + g[1:-1, 2:] - 4 * g[1:-1, 1:-1])
    return out


def sobel_mag(gray: np.ndarray) -> np.ndarray:
    g = gray.astype(np.float32)
    if HAVE_CV2:
        gx = cv2.Sobel(g, cv2.CV_32F, 1, 0, ksize=3)
        gy = cv2.Sobel(g, cv2.CV_32F, 0, 1, ksize=3)
        return np.sqrt(gx * gx + gy * gy)
    gx = np.zeros_like(g)
    gy = np.zeros_like(g)
    gx[:, 1:-1] = g[:, 2:] - g[:, :-2]
    gy[1:-1, :] = g[2:, :] - g[:-2, :]
    return np.sqrt(gx * gx + gy * gy) * 2


def block_reduce_mean(a: np.ndarray, gy: int, gx: int) -> np.ndarray:
    """Mean over a gy×gx grid of equal blocks (crops the remainder). a: HxW (or HxWxC)."""
    h, w = a.shape[:2]
    bh, bw = h // gy, w // gx
    a = a[: bh * gy, : bw * gx]
    if a.ndim == 2:
        return a.reshape(gy, bh, gx, bw).mean(axis=(1, 3))
    return a.reshape(gy, bh, gx, bw, a.shape[2]).mean(axis=(1, 3))


def inpaint(rgb: np.ndarray, mask: np.ndarray, radius: int = 5) -> np.ndarray:
    """Fill masked pixels from their surroundings (for clean reference frames without the overlay text)."""
    if HAVE_CV2:
        return cv2.inpaint(rgb.astype(np.uint8), mask.astype(np.uint8) * 255, radius, cv2.INPAINT_TELEA)
    # Fallback: iterative blur fill
    out = rgb.astype(np.float32).copy()
    m = mask.astype(bool)
    known = (~m).astype(np.float32)
    for s in (2, 4, 8, 16, 32):
        num = gaussian_blur(out * known[..., None], s)
        den = gaussian_blur(known, s)[..., None]
        fill = num / np.maximum(den, 1e-4)
        out[m] = fill[m]
    return np.clip(out, 0, 255).astype(np.uint8)


def phase_shift(a: np.ndarray, b: np.ndarray) -> tuple[float, float, float]:
    """Translation (dx, dy) that maps a onto b, plus peak strength. Grey float arrays of equal size."""
    a = a.astype(np.float32) - a.mean()
    b = b.astype(np.float32) - b.mean()
    h, w = a.shape
    win = np.outer(np.hanning(h), np.hanning(w)).astype(np.float32)
    A = np.fft.rfft2(a * win)
    B = np.fft.rfft2(b * win)
    R = B * np.conj(A)
    R /= np.maximum(np.abs(R), 1e-6)
    r = np.fft.irfft2(R, s=(h, w))
    idx = np.unravel_index(int(np.argmax(r)), r.shape)
    peak = float(r[idx])
    dy, dx = idx
    if dy > h // 2:
        dy -= h
    if dx > w // 2:
        dx -= w
    return float(dx), float(dy), peak


def save_png(path, arr):
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(str(path))


def save_jpg(path, arr, q=90):
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGB").save(str(path), quality=q)
