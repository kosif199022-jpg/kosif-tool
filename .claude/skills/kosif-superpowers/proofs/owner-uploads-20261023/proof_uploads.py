#!/usr/bin/env python3
"""Proof run for the 2026-10-23 owner-upload review (references/owner-uploads-review-20261023.md).

Re-implements, in our own code, three numeric recipes distilled from the owner-supplied
"Claude AI Motion Graphics" skill (Tao Prompts; ideas and numbers only, no code copied) and
renders specimens of the two OFL font families added to proofs/_shared/fonts:

  1. before/after slider progress curve: glide -> slow crawl -> reveal       (TRANS-U01)
  2. noise + centre-distance reveal field dissolve                           (PART-U01)
  3. graphics-only RGBA layer recovered from two aligned renders             (QA-U01)
  4. El Messiri (Arabic) and Poppins (Latin) specimens via Pillow + raqm      (ARAB-U01, TYPE-U01)

Writes sheet.jpg and receipt.json next to this file. Needs numpy and Pillow (raqm for Arabic).
    python3 proofs/owner-uploads-20261023/proof_uploads.py
"""
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, features

HERE = Path(__file__).resolve().parent
FONTS = HERE.parent / "_shared" / "fonts"
W, H = 480, 270


def ease_out(x):
    x = np.clip(x, 0.0, 1.0)
    return 1 - (1 - x) ** 3


def ease_in_out(x):
    x = np.clip(x, 0.0, 1.0)
    return np.where(x < 0.5, 4 * x ** 3, 1 - (-2 * x + 2) ** 3 / 2)


def smoothstep(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3 - 2 * x)


def slider_progress(t, t0=0.0):
    """Glide in fast to ~0.46, crawl (never stop) for ~2 s, then accelerate to a full reveal."""
    return (0.46 * ease_out((t - t0) / 0.8)
            + 0.10 * smoothstep((t - t0 - 0.5) / 2.05)
            + 0.44 * ease_in_out((t - t0 - 2.3) / 0.95))


def smooth_noise(w, h, seed=7, cells=12):
    rng = np.random.default_rng(seed)
    coarse = rng.random((cells + 1, cells + 1)).astype(np.float32)
    img = Image.fromarray((coarse * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    return np.asarray(img, np.float32) / 255.0


def reveal_alpha(p, w=W, h=H):
    """alpha = clip((p*1.15 - field)/0.12), field = 0.55*noise + 0.45*|x-0.5|*2 (centre reveals first)."""
    x = np.linspace(0, 1, w, dtype=np.float32)[None, :].repeat(h, 0)
    field = 0.55 * smooth_noise(w, h) + 0.45 * np.abs(x - 0.5) * 2
    return np.clip((p * 1.15 - field) / 0.12, 0, 1)


def plates():
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    original = np.stack([0.25 + 0.3 * x / W, 0.3 + 0.2 * y / H, 0.45 + 0 * x], -1)
    graphics = original.copy()
    graphics[60:120, 40:300] = [0.95, 0.95, 0.92]          # a caption bar
    graphics[150:230, 330:440] = [0.85, 0.35, 0.25]        # an illustration block
    return original, graphics


def graphics_layer(original, graphics):
    """diff = max_channel|g - o|; alpha = clip((diff - 0.10)/0.12); RGBA of the graphics only."""
    diff = np.abs(graphics - original).max(-1)
    alpha = np.clip((diff - 0.10) / 0.12, 0, 1)
    return np.dstack([graphics, alpha])


def to_img(a):
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    receipt = {"schema": "kosif.proof.receipt.v1", "run": "owner-uploads-20261023", "checks": {}}

    ts = np.linspace(0, 3.5, 351)
    prog = slider_progress(ts)
    mono = bool(np.all(np.diff(prog) >= -1e-9))
    crawl = prog[(ts >= 0.9) & (ts <= 2.2)]
    receipt["checks"]["slider_curve"] = {
        "monotone": mono, "p_at_0.8s": round(float(slider_progress(0.8)), 3),
        "crawl_span_0.9_2.2s": [round(float(crawl.min()), 3), round(float(crawl.max()), 3)],
        "crawl_never_stops": bool(np.all(np.diff(crawl) > 0)), "p_end": round(float(prog[-1]), 3),
        "pass": mono and bool(np.all(np.diff(crawl) > 0)) and abs(float(prog[-1]) - 1) < 1e-6}

    covered = [float(reveal_alpha(p).mean()) for p in (0.0, 0.25, 0.5, 0.75, 1.0)]
    receipt["checks"]["reveal_field"] = {
        "coverage_at_p": [round(c, 3) for c in covered],
        "pass": covered[0] == 0.0 and covered[-1] == 1.0 and all(b >= a for a, b in zip(covered, covered[1:]))}

    o, g = plates()
    layer = graphics_layer(o, g)
    truth = np.zeros((H, W), bool)
    truth[60:120, 40:300] = True
    truth[150:230, 330:440] = True
    got = layer[..., 3] > 0.5
    iou = float((got & truth).sum() / (got | truth).sum())
    receipt["checks"]["graphics_layer"] = {"iou_vs_truth": round(iou, 4), "pass": iou > 0.99}

    sheet = Image.new("RGB", (W * 2, H * 3), (18, 18, 20))
    # row 1: slider frames at t=0.8 s and t=2.0 s (left = graphics, right = original)
    for i, t in enumerate((0.8, 2.0)):
        cut = int(W * float(slider_progress(t)))
        frame = o.copy()
        frame[:, :cut] = g[:, :cut]
        im = to_img(frame)
        ImageDraw.Draw(im).line([(cut, 0), (cut, H)], fill=(255, 255, 255), width=2)
        sheet.paste(im, (i * W, 0))
    # row 2: reveal at p=0.45 and recovered graphics layer over a checkerboard
    a = reveal_alpha(0.45)[..., None]
    sheet.paste(to_img(o * (1 - a) + g * a), (0, H))
    checker = ((np.indices((H, W)).sum(0) // 16) % 2 * 0.15 + 0.35)[..., None].repeat(3, -1)
    sheet.paste(to_img(checker * (1 - layer[..., 3:]) + layer[..., :3] * layer[..., 3:]), (W, H))
    # row 3: font specimens
    d = ImageDraw.Draw(sheet)
    arab = ImageFont.truetype(str(FONTS / "ElMessiri[wght].ttf"), 46)
    lat = ImageFont.truetype(str(FONTS / "Poppins-Bold.ttf"), 46)
    lat_r = ImageFont.truetype(str(FONTS / "Poppins-Regular.ttf"), 26)
    raqm = features.check("raqm")
    kw = {"direction": "rtl", "language": "ar"} if raqm else {}
    d.text((W - 30, H * 2 + 60), "قدرات خارقة للمونتاج", font=arab, fill=(240, 236, 226), anchor="ra", **kw)
    d.text((W + 30, H * 2 + 60), "Motion Graphics", font=lat, fill=(240, 236, 226))
    d.text((W + 30, H * 2 + 130), "Poppins Regular · OFL 1.1", font=lat_r, fill=(170, 170, 170))
    bbox = d.textbbox((W - 30, H * 2 + 60), "قدرات خارقة للمونتاج", font=arab, anchor="ra", **kw)
    receipt["checks"]["fonts"] = {"raqm": raqm, "el_messiri_ink_bbox": list(bbox),
                                  "pass": raqm and bbox[2] - bbox[0] > 200}

    out = HERE / "sheet.jpg"
    sheet.save(out, quality=85, optimize=True)
    receipt["outputs"] = {"sheet.jpg": sha(out)}
    receipt["fonts_sha256"] = {f: sha(FONTS / f) for f in ("ElMessiri[wght].ttf", "Poppins-Regular.ttf", "Poppins-Bold.ttf")}
    receipt["pass"] = all(c["pass"] for c in receipt["checks"].values())
    (HERE / "receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=1) + "\n")
    print(json.dumps({k: v["pass"] for k, v in receipt["checks"].items()}), "->", "PASS" if receipt["pass"] else "FAIL")
    return 0 if receipt["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
