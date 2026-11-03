"""Real programs for the media-image-audio power cards (Pillow/raqm, OpenCV, codecs, audio DSP).

Each builds its own fixture, performs the card's technique with the card's numbers and returns
known answers. Library substitutes are named in the observed values (e.g. a numpy YIN where the
card names librosa, which is not installed here); paid, ML-model and missing-binary cards are skipped.
"""
from __future__ import annotations

import io
import json
import math
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, features

from .photo_video_footage import (REPO, chk, decode_audio, ff, ffstderr, jwrite, near, probe, read_wav,
                                  tone, write_wav, dom_freq)

FONT = REPO / ".claude/skills/kosif-superpowers/proofs/_shared/fonts/Amiri-Bold.ttf"


def _ink_bbox(img):
    a = np.asarray(img.convert("L")) < 128
    ys, xs = np.nonzero(a)
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def media_01(work):
    text = "السلام عليكم"
    f = ImageFont.truetype(str(FONT), 64, layout_engine=ImageFont.Layout.RAQM)
    img = Image.new("L", (640, 140), 255)
    right_x = 600
    ImageDraw.Draw(img).text((right_x, 30), text, font=f, fill=0, direction="rtl", language="ar", anchor="ra")
    img.save(work / "arabic.png")
    x0, y0, x1, y1 = _ink_bbox(img)
    basic = ImageFont.truetype(str(FONT), 64, layout_engine=ImageFont.Layout.BASIC)
    w_raqm = f.getlength(text, direction="rtl", language="ar")
    w_basic = basic.getlength(text)
    return [chk("raqm available", features.check("raqm"), features.version("raqm")),
            chk("anchor 'ra': ink ends within 8 px left of x=600, never past it", right_x - 8 <= x1 <= right_x, x1),
            chk("text sits below the ascender line y=30", y0 >= 30, y0),
            chk("raqm shapes (joined width differs from unshaped isolated forms)", abs(w_raqm - w_basic) > 5,
                (round(w_raqm), round(w_basic)))]


def media_02(work):
    import arabic_reshaper
    from bidi.algorithm import get_display
    text = "مرحبا بالعالم"
    raqm = ImageFont.truetype(str(FONT), 48, layout_engine=ImageFont.Layout.RAQM)
    basic = ImageFont.truetype(str(FONT), 48, layout_engine=ImageFont.Layout.BASIC)

    def render(t, font, **kw):
        im = Image.new("L", (520, 100), 255)
        ImageDraw.Draw(im).text((500, 20), t, font=font, fill=0, anchor="ra", **kw)
        return np.asarray(im) < 128

    good = render(text, raqm, direction="rtl", language="ar")
    pre = get_display(arabic_reshaper.reshape(text))
    legacy = render(pre, basic)  # reshape + bidi for a non-shaping engine: correct
    double = render(pre, raqm, direction="rtl", language="ar")  # shaped twice: reversed
    import cv2
    blur = lambda a: cv2.GaussianBlur(a.astype(np.float32), (0, 0), 3)
    dist = lambda a, b: float(np.abs(blur(a) - blur(b)).mean())
    sheet = np.concatenate([good, legacy, double]).astype(np.uint8) * 255
    Image.fromarray(255 - sheet).save(work / "panel.png")
    pres = sum(0xFE70 <= ord(c) <= 0xFEFF for c in pre)
    return [chk("reshaper emits presentation forms for the non-shaping path", pres >= 10, pres),
            chk("correct pipelines look closer than the double-shaped one", dist(good, legacy) < 0.7 * dist(good, double),
                (round(dist(good, legacy), 4), round(dist(good, double), 4))),
            chk("double-shaped string is the visual reversal", pre[::-1] != text and get_display(pre) != pre, pre[:6])]


def media_04(work):
    """Mitigation for weak Arabic-Indic digit OCR: normalise digits and validate every number."""
    trans = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789")

    def check_phone(s):
        d = s.translate(trans).replace(" ", "").replace("-", "")
        if d.startswith("+966"):
            d = "0" + d[4:]
        return d if (d.isdigit() and len(d) == 10 and d.startswith("05")) else None

    def luhn(n):
        n = n.translate(trans)
        if not n.isdigit():
            return False
        tot = 0
        for i, ch in enumerate(reversed(n)):
            k = int(ch) * (2 if i % 2 else 1)
            tot += k - 9 if k > 9 else k
        return tot % 10 == 0

    ocr = {"phone_ok": "٠٥٥١٢٣٤٥٦٧", "phone_garbage": "٠٥٥l٢3٤ه٦٧", "card_ok": "٤٥٣٩١٤٨٨٠٣٤٣٦٤٦٧",
           "card_bad": "٤٥٣٩١٤٨٨٠٣٤٣٦٤٦٨"}
    res = {"phone_ok": check_phone(ocr["phone_ok"]), "phone_garbage": check_phone(ocr["phone_garbage"]),
           "card_ok": luhn(ocr["card_ok"]), "card_bad": luhn(ocr["card_bad"])}
    jwrite(work, "number_checks.json", {"ocr": ocr, "result": res,
                                        "ask_user_to_confirm": [k for k, v in res.items() if not v]})
    return [chk("Arabic-Indic phone normalised and valid", res["phone_ok"] == "0551234567", res["phone_ok"]),
            chk("garbled OCR phone rejected", res["phone_garbage"] is None, res["phone_garbage"]),
            chk("Luhn passes the true number", res["card_ok"], res["card_ok"]),
            chk("one-digit OCR error caught by checksum", not res["card_bad"], res["card_bad"])]


def deskew_angle(gray):
    import cv2
    g = cv2.medianBlur(gray, 3)
    _, b = cv2.threshold(g, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    b = cv2.morphologyEx(b, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    b = cv2.dilate(b, np.ones((5, 60), np.uint8))
    cs, _ = cv2.findContours(b, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    angs = []
    for c in cs:
        if cv2.contourArea(c) <= 5000:
            continue
        (cx, cy), (w, h), a = cv2.minAreaRect(c)
        if w < h:
            a -= 90
        angs.append(a)
    return float(np.median(angs)), len(angs)


def media_05(work):
    import cv2
    img = np.full((600, 800), 255, np.uint8)
    for k in range(6):
        cv2.putText(img, "Lorem ipsum dolor sit amet", (60, 120 + 70 * k), cv2.FONT_HERSHEY_SIMPLEX, 1.4, 0, 3)
    M = cv2.getRotationMatrix2D((400, 300), 12, 1.0)
    skew = cv2.warpAffine(img, M, (800, 600), borderValue=255)
    est, n = deskew_angle(skew)
    back = cv2.warpAffine(skew, cv2.getRotationMatrix2D((400, 300), est, 1.0), (800, 600), borderValue=255)
    cv2.imwrite(str(work / "deskewed.png"), back)
    est2, _ = deskew_angle(back)
    return [chk("true 12 deg estimated within 0.5", near(abs(est), 12, 0.5), round(est, 2)),
            chk("lines found as blobs > 5000 px", n >= 4, n),
            chk("after rotation the skew is ~0 (mod 90)", min(abs(est2) % 90, 90 - abs(est2) % 90) < 0.6, round(est2, 2))]


def media_08(work):
    import cv2
    img = np.full((120, 160), 255, np.uint8)
    cv2.rectangle(img, (30, 30), (90, 80), 0, -1)
    cv2.circle(img, (125, 60), 18, 0, -1)
    noisy = cv2.add(img, np.random.default_rng(0).integers(0, 30, img.shape, dtype=np.uint8))
    t, bw = cv2.threshold(noisy, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    edges = cv2.Canny(img, 80, 160)
    cs, _ = cv2.findContours(255 - bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    shapes = sorted(len(cv2.approxPolyDP(c, 0.02 * cv2.arcLength(c, True), True)) for c in cs)
    rot = cv2.warpAffine(img, cv2.getRotationMatrix2D((80, 60), 90, 1.0), (160, 120), borderValue=255)
    cv2.imwrite(str(work / "edges.png"), edges)
    ink = img == 0
    return [chk("Otsu separates noisy ink from paper", (bw[ink] == 0).all() and (bw[~ink] == 255).all(), t),
            chk("two contours: rectangle (4 vertices) and circle (many)", len(cs) == 2 and shapes[0] == 4 and shapes[1] > 6,
                shapes),
            chk("Canny finds the rectangle border", edges[30:81, 30].max() == 255 and edges[55, 60] == 0, "edge"),
            chk("warpAffine borderValue=255 fills white corners", rot[0, 0] == 255, int(rot[0, 0]))]


def ssim(a, b):
    import cv2
    a, b = a.astype(np.float64), b.astype(np.float64)
    C1, C2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2
    vals = []
    for ch in range(3):
        x, y = a[..., ch], b[..., ch]
        mx, my = cv2.GaussianBlur(x, (11, 11), 1.5), cv2.GaussianBlur(y, (11, 11), 1.5)
        sx = cv2.GaussianBlur(x * x, (11, 11), 1.5) - mx * mx
        sy = cv2.GaussianBlur(y * y, (11, 11), 1.5) - my * my
        sxy = cv2.GaussianBlur(x * y, (11, 11), 1.5) - mx * my
        vals.append((((2 * mx * my + C1) * (2 * sxy + C2)) / ((mx * mx + my * my + C1) * (sx + sy + C2))).mean())
    return float(np.mean(vals))


def media_09(work):
    import cv2
    yy, xx = np.mgrid[:240, :320]
    img = np.dstack([xx * 255 // 320, yy * 255 // 240, (xx + yy) % 256]).astype(np.uint8)
    cv2.circle(img, (160, 120), 60, (250, 250, 250), -1)
    img = cv2.GaussianBlur(np.clip(img + np.random.default_rng(0).normal(0, 6, img.shape), 0, 255).astype(np.uint8),
                           (0, 0), 1.5)
    src = Image.fromarray(img)
    res = {}
    for fmt, kw, ext in [("PNG", {"optimize": True}, "png"), ("WEBP", {"quality": 80}, "webp"),
                         ("AVIF", {"quality": 50}, "avif"), ("JPEG", {"quality": 85}, "jpg")]:
        p = work / f"img.{ext}"
        src.save(p, fmt, **kw)
        back = np.asarray(Image.open(p).convert("RGB"))
        res[fmt] = {"kb": round(p.stat().st_size / 1024, 1), "psnr": round(float(cv2.PSNR(img, back)), 2),
                    "ssim": round(ssim(img, back), 4)}
    jwrite(work, "compression.json", res)
    return [chk("PNG lossless (PSNR inf/high)", res["PNG"]["psnr"] >= 99 or res["PNG"]["ssim"] == 1.0, res["PNG"]),
            chk("WebP q80 smaller than PNG with SSIM >= 0.95", res["WEBP"]["kb"] < res["PNG"]["kb"] and res["WEBP"]["ssim"] >= 0.95,
                res["WEBP"]),
            chk("AVIF q50 smaller than PNG with SSIM >= 0.95", res["AVIF"]["kb"] < res["PNG"]["kb"] and res["AVIF"]["ssim"] >= 0.95,
                res["AVIF"]),
            chk("JPEG q85 PSNR > 30 dB", res["JPEG"]["psnr"] > 30, res["JPEG"])]


def media_10(work):
    import cv2
    img = np.full((120, 120, 3), (240, 240, 240), np.uint8)
    cols = [(200, 30, 40), (30, 120, 200), (40, 180, 70)]
    for (cx, r), c in zip([(30, 22), (60, 18), (92, 14)], cols):
        cv2.circle(img, (cx, 60), r, c, -1)
    Z = img.reshape(-1, 3).astype(np.float32)
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.5)
    cv2.setRNGSeed(1)
    _, lab, cen = cv2.kmeans(Z, 4, None, crit, 4, cv2.KMEANS_PP_CENTERS)
    counts = np.bincount(lab.ravel(), minlength=4)
    order = np.argsort(-counts)
    pal = [tuple(int(round(v)) for v in cen[i]) for i in order]
    jwrite(work, "palette.json", ["#%02x%02x%02x" % p for p in pal])
    errs = [min(np.abs(np.array(p) - c).max() for p in pal) for c in cols]
    return [chk("background is the largest cluster", np.abs(np.array(pal[0]) - 240).max() <= 2, pal[0]),
            chk("three disc colours recovered within 3 RGB units", max(errs) <= 3, errs),
            chk("disc clusters sorted by size (red r22 before green r14)", pal.index(min(pal, key=lambda p: abs(p[0] - 200)))
                < pal.index(min(pal, key=lambda p: abs(p[1] - 180))), pal)]


EAN_L = ["0001101", "0011001", "0010011", "0111101", "0100011", "0110001", "0101111", "0111011", "0110111", "0001011"]
EAN_G = ["".join("1" if c == "0" else "0" for c in s)[::-1] for s in EAN_L]
EAN_R = ["".join("1" if c == "0" else "0" for c in s) for s in EAN_L]
EAN_P = ["LLLLLL", "LLGLGG", "LLGGLG", "LLGGGL", "LGLLGG", "LGGLLG", "LGGGLL", "LGLGLG", "LGLGGL", "LGGLGL"]


def ean_check(d12):
    s = sum(int(c) * (3 if i % 2 else 1) for i, c in enumerate(d12))
    return str((10 - s % 10) % 10)


def ean_bits(d13):
    par = EAN_P[int(d13[0])]
    left = "".join((EAN_L if p == "L" else EAN_G)[int(c)] for p, c in zip(par, d13[1:7]))
    right = "".join(EAN_R[int(c)] for c in d13[7:])
    return "101" + left + "01010" + right + "101"


def ean_decode(bits):
    left, right = bits[3:45], bits[50:92]
    digs, par = "", ""
    for k in range(6):
        s = left[7 * k:7 * k + 7]
        if s in EAN_L:
            digs, par = digs + str(EAN_L.index(s)), par + "L"
        else:
            digs, par = digs + str(EAN_G.index(s)), par + "G"
    for k in range(6):
        digs += str(EAN_R.index(right[7 * k:7 * k + 7]))
    return str(EAN_P.index(par)) + digs


def media_11(work):
    import cv2
    import segno
    payload = "https://example.com/مرحبا?x=1"
    q = segno.make(payload, error="m")
    p = work / "qr.png"
    q.save(str(p), scale=8, border=4)
    dec, pts, _ = cv2.QRCodeDetector().detectAndDecode(cv2.imread(str(p)))
    d12 = "590123412345"
    d13 = d12 + ean_check(d12)
    bits = ean_bits(d13)
    mod = 3
    row = np.array([0 if b == "1" else 255 for b in "0" * 9 + bits + "0" * 9], np.uint8)
    img = np.repeat(np.repeat(row[None], 60, 0), mod, 1)
    Image.fromarray(img).save(work / "ean13.png")
    scan = (np.asarray(Image.open(work / "ean13.png"))[30] < 128).astype(int)
    xs = np.nonzero(scan)[0]
    width = (xs.max() - xs.min() + 1) / 95
    rd = "".join(str(scan[int(xs.min() + (i + 0.5) * width)]) for i in range(95))
    return [chk("QR with Arabic URL decodes back to the payload", dec == payload, dec),
            chk("EAN-13 check digit of 590123412345 is 7", d13[-1] == "7", d13),
            chk("barcode is 95 modules", len(bits) == 95, len(bits)),
            chk("scanned bars decode to the same 13 digits", ean_decode(rd) == d13, ean_decode(rd))]


def media_14(work):
    rng = np.random.default_rng(3)
    outs = []
    for i in range(6):
        im = Image.fromarray(rng.integers(0, 255, (480, 640, 3)).astype(np.uint8))
        p = work / f"out_{i}.png"
        im.save(p)
        outs.append(p)
    tw, th, cols = 320, 240, 3
    sheet = Image.new("RGB", (tw * cols, th * 2), "white")
    for i, p in enumerate(outs):
        sheet.paste(Image.open(p).resize((tw, th)), ((i % cols) * tw, (i // cols) * th))
    q = sheet.quantize(64)
    buf = io.BytesIO()
    q.save(buf, "PNG", optimize=True)
    colors = 64
    while buf.tell() > 300 * 1024 and colors > 8:
        colors //= 2
        buf = io.BytesIO()
        sheet.quantize(colors).save(buf, "PNG", optimize=True)
    (work / "contact.png").write_bytes(buf.getvalue())
    back = Image.open(work / "contact.png").convert("RGB")
    tile3 = np.asarray(back.crop((0, th, tw, 2 * th))).astype(float)
    ref3 = np.asarray(Image.open(outs[3]).resize((tw, th))).astype(float)
    return [chk("contact sheet under 300 KB", buf.tell() <= 300 * 1024, buf.tell()),
            chk("6 tiles in a 3x2 grid", back.size == (960, 480), back.size),
            chk("tile 4 is output 3 (closest source)", min(range(6), key=lambda k: np.abs(
                np.asarray(Image.open(outs[k]).resize((tw, th))).astype(float) - tile3).mean()) == 3, "tile->source")]


def media_15(work):
    sr = 48000
    t = np.arange(2 * sr) / sr
    tone_ = 0.2 * np.sin(2 * np.pi * 440 * t)
    sil = np.zeros(sr)
    clicks = np.zeros(3 * sr)
    for k in range(6):
        i = int(k * 0.5 * sr)
        n = 480
        clicks[i:i + n] += np.sin(2 * np.pi * 1000 * np.arange(n) / sr) * np.exp(-np.arange(n) / 80)
    sig = np.concatenate([tone_, sil, clicks])
    p = write_wav(work / "test.wav", sig, sr)
    x, r = read_wav(p)
    seg = x[3 * sr:]
    env = np.abs(seg)
    hits = [i for i in range(1, len(env)) if env[i] > 0.3 and env[i - 1] <= 0.3]
    hits = [h for k, h in enumerate(hits) if k == 0 or h - hits[k - 1] > 2000]
    gaps = np.diff(hits) / sr
    pr = probe(p)["streams"][0]
    return [chk("48 kHz PCM_16", pr["sample_rate"] == "48000" and pr["bits_per_sample"] == 16, pr["sample_rate"]),
            chk("tone is 440 Hz at 0.2", near(dom_freq(x[:sr], sr), 440, 1) and near(np.abs(x[:sr]).max(), 0.2, 0.01),
                dom_freq(x[:sr], sr)),
            chk("1 s of digital silence", np.abs(x[2 * sr:3 * sr]).max() == 0, "zeros"),
            chk("6 clicks 0.5 s apart (120 BPM)", len(hits) == 6 and np.allclose(gaps, 0.5, atol=0.002), gaps.tolist())]


def yin(x, sr, fmin=100, fmax=1000, frame=2048, hop=512, thresh=0.1):
    tmin, tmax = int(sr / fmax), int(sr / fmin)
    f0 = []
    for s in range(0, len(x) - frame - tmax, hop):
        w = x[s:s + frame + tmax]
        d = np.array([np.sum((w[:frame] - w[t:t + frame]) ** 2) for t in range(tmax + 1)])
        cmnd = np.ones_like(d)
        cmnd[1:] = d[1:] * np.arange(1, tmax + 1) / np.maximum(np.cumsum(d[1:]), 1e-12)
        cand = np.nonzero(cmnd[tmin:] < thresh)[0]
        t = (cand[0] + tmin) if len(cand) else int(np.argmin(cmnd[tmin:]) + tmin)
        while t + 1 <= tmax and cmnd[t + 1] < cmnd[t]:
            t += 1
        if 1 <= t < tmax:  # parabolic interpolation
            a, b, c = cmnd[t - 1], cmnd[t], cmnd[t + 1]
            t = t + 0.5 * (a - c) / (a - 2 * b + c) if (a - 2 * b + c) else t
        f0.append(sr / t)
    return np.array(f0)


def media_16(work):
    sr = 16000
    out = {}
    for f in (440.0, 220.0):
        x = tone(0.5, f, sr)
        out[f] = float(np.median(yin(x, sr, fmin=100, fmax=1000)))
    jwrite(work, "f0.json", {"engine": "numpy YIN (librosa not installed)", "f0": out})
    return [chk("440 Hz tone -> 440 +-1 Hz", near(out[440.0], 440, 1), out[440.0]),
            chk("220 Hz tone -> 220 +-1 Hz", near(out[220.0], 220, 1), out[220.0])]


def onsets(x, sr, hop=128):
    env = np.array([np.sqrt((x[i:i + hop] ** 2).mean()) for i in range(0, len(x) - hop, hop)])
    flux = np.maximum(np.diff(env, prepend=env[0]), 0)
    thr = 0.3 * flux.max()
    on, last = [], -1e9
    for i in range(1, len(flux) - 1):
        if flux[i] > thr and flux[i] >= flux[i - 1] and flux[i] > flux[i + 1] and i - last > 0.1 * sr / hop:
            on.append(i * hop / sr)
            last = i
    return np.array(on)


def media_17(work):
    sr = 16000
    hits = np.zeros(int(3.2 * sr))
    for k in range(6):
        i = int(k * 0.5 * sr)
        hits[i:i + 300] += np.sin(2 * np.pi * 900 * np.arange(300) / sr) * np.exp(-np.arange(300) / 60)
    lead = int(0.1 * sr)
    on_no_lead = onsets(hits, sr)
    padded = np.concatenate([np.zeros(lead), hits])
    on = onsets(padded, sr) - 0.1
    bpm = 60 / np.median(np.diff(on))
    jwrite(work, "onsets.json", {"onsets": on.round(3).tolist(), "bpm": float(bpm)})
    return [chk("window from 0.1 s before the first hit finds all 6", len(on) == 6, len(on)),
            chk("onset at sample 0 missed without the lead-in", len(on_no_lead) == 5, len(on_no_lead)),
            chk("tempo 120 +-1 BPM", near(bpm, 120, 1), round(float(bpm), 2))]


def k_weight_lufs(x, sr):
    """ITU-R BS.1770-4 integrated loudness (mono), gated."""
    from scipy.signal import lfilter
    f0, G, Q = 1681.974450955533, 3.999843853973347, 0.7071752369554196
    K = math.tan(math.pi * f0 / sr)
    Vh = 10 ** (G / 20)
    Vb = Vh ** 0.4996667741545416
    a0 = 1 + K / Q + K * K
    b1 = [(Vh + Vb * K / Q + K * K) / a0, 2 * (K * K - Vh) / a0, (Vh - Vb * K / Q + K * K) / a0]
    a1 = [1, 2 * (K * K - 1) / a0, (1 - K / Q + K * K) / a0]
    f0, Q = 38.13547087602444, 0.5003270373238773
    K = math.tan(math.pi * f0 / sr)
    a2 = [1, 2 * (K * K - 1) / (1 + K / Q + K * K), (1 - K / Q + K * K) / (1 + K / Q + K * K)]
    b2 = [1, -2, 1]
    y = lfilter(b2, a2, lfilter(b1, a1, x))
    blk, step = int(0.4 * sr), int(0.1 * sr)
    z = np.array([np.mean(y[i:i + blk] ** 2) for i in range(0, len(y) - blk + 1, step)])
    l = -0.691 + 10 * np.log10(z + 1e-20)
    z1 = z[l > -70]
    rel = -0.691 + 10 * np.log10(z1.mean()) - 10
    z2 = z1[(-0.691 + 10 * np.log10(z1 + 1e-20)) > rel]
    return float(-0.691 + 10 * np.log10(z2.mean()))


def ebur128_I(path):
    err = ffstderr("-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-")
    return float([l for l in err.splitlines() if l.strip().startswith("I:")][-1].split()[1])


def media_18(work):
    sr = 48000
    rng = np.random.default_rng(0)
    x = 0.1 * np.sin(2 * np.pi * 1000 * np.arange(3 * sr) / sr) + 0.02 * rng.standard_normal(3 * sr)
    p = write_wav(work / "a.wav", x, sr)
    a = k_weight_lufs(read_wav(p)[0], sr)
    b = ebur128_I(p)
    jwrite(work, "lufs.json", {"numpy_bs1770": a, "ffmpeg_ebur128": b})
    sine = write_wav(work / "ref.wav", 10 ** (-20 / 20) * np.sin(2 * np.pi * 1000 * np.arange(3 * sr) / sr), sr)
    ref = k_weight_lufs(read_wav(sine)[0], sr)
    return [chk("two independent meters agree within 0.3 LU", abs(a - b) <= 0.3, (round(a, 2), b)),
            chk("1 kHz sine at -20 dBFS mono reads ~-23 LUFS", near(ref, -23.0, 0.3), round(ref, 2))]


def loudnorm_two_pass(src, dst, I=-14, TP=-1.0, LRA=11, lra_rule=True):
    err = ffstderr("-nostats", "-i", src, "-af", f"loudnorm=I={I}:TP={TP}:LRA={LRA}:print_format=json", "-f", "null", "-")
    m = json.loads(err[err.rindex("{"):err.rindex("}") + 1])
    lra = max(LRA, float(m["input_lra"]) + 1) if lra_rule else LRA
    af = (f"loudnorm=I={I}:TP={TP}:LRA={lra}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:"
          "linear=true:print_format=json")
    err2 = ffstderr("-nostats", "-i", src, "-af", af, "-ar", "48000", dst)
    return m, json.loads(err2[err2.rindex("{"):err2.rindex("}") + 1])


def media_19(work):
    sr = 48000
    t = np.arange(6 * sr) / sr
    x = 0.08 * np.sin(2 * np.pi * 330 * t) * (1 + 0.2 * np.sin(2 * np.pi * 0.5 * t))
    src = write_wav(work / "in.wav", x, sr)
    m, r = loudnorm_two_pass(src, work / "out.wav")
    I = ebur128_I(work / "out.wav")
    # wide-range input with LRA 11: ffmpeg falls back to dynamic
    y = np.concatenate([10 ** (-d / 20) * 0.5 * np.sin(2 * np.pi * 330 * t[:sr]) for d in (0, 4, 8, 12, 16, 20, 24)])
    wide = write_wav(work / "wide.wav", y, sr)
    _, r2 = loudnorm_two_pass(wide, work / "wide_out.wav", lra_rule=False)
    _, r3 = loudnorm_two_pass(wide, work / "wide_ok.wav", lra_rule=True)
    jwrite(work, "loudnorm.json", {"pass1": m, "pass2": r, "wide_lra11": r2["normalization_type"],
                                   "wide_rule": r3["normalization_type"]})
    return [chk("pass 2 is linear", r["normalization_type"] == "linear", r["normalization_type"]),
            chk("output -14 +-0.5 LUFS", near(I, -14, 0.5), I),
            chk("wide input with LRA=11 goes dynamic (detected)", r2["normalization_type"] == "dynamic",
                r2["normalization_type"]),
            chk("LRA = max(11, input_lra + 1) keeps it linear", r3["normalization_type"] == "linear", r3["normalization_type"])]


def media_20(work):
    sr = 16000
    x = np.concatenate([tone(2.0, 440, sr, 0.3), np.zeros(sr), tone(2.0, 440, sr, 0.3)])
    p = write_wav(work / "a.wav", x, sr)
    err = ffstderr("-i", p, "-af", "silencedetect=noise=-50dB:d=0.5", "-f", "null", "-")
    s = [float(l.split("silence_start: ")[1]) for l in err.splitlines() if "silence_start" in l]
    e = [float(l.split("silence_end: ")[1].split()[0]) for l in err.splitlines() if "silence_end" in l]
    jwrite(work, "silence.json", {"start": s, "end": e})
    return [chk("one silence 2.0 -> 3.0 s", len(s) == 1 and near(s[0], 2.0, 0.01) and near(e[0], 3.0, 0.01), (s, e))]


def media_21(work):
    sr = 16000
    x = np.concatenate([tone(1.0, 440, sr, 0.8), np.zeros(sr)])
    p = write_wav(work / "a.wav", x, sr)
    ff("-i", p, "-filter_complex", "showwavespic=s=1200x200:colors=#2a78d6", "-frames:v", "1", work / "w.png")
    ff("-i", p, "-lavfi", "showspectrumpic=s=1200x300:legend=0", work / "s.png")
    w = np.asarray(Image.open(work / "w.png").convert("RGB")).astype(int)
    s = np.asarray(Image.open(work / "s.png").convert("RGB")).astype(int)
    blue = (np.abs(w - np.array([0x2a, 0x78, 0xd6])).sum(-1) < 60)
    left, right = blue[:, :600].mean(), blue[:, 610:].mean()
    rowe = s[:, :580].sum(axis=(1, 2))
    peak_row = int(np.argmax(rowe))
    want_row = int(round((1 - 440 / 8000) * (s.shape[0] - 1)))
    return [chk("waveform 1200x200", w.shape[:2] == (200, 1200), w.shape),
            chk("wave drawn in #2a78d6 for the tone, flat for silence", left > 0.5 and right < 0.02, (round(left, 3), round(right, 3))),
            chk("spectrum 1200x300 peaks at 440 Hz row", s.shape[:2] == (300, 1200) and abs(peak_row - want_row) <= 4,
                (peak_row, want_row))]


def media_22(work):
    sr = 44100
    p = write_wav(work / "in.wav", tone(3.0, 440, sr, 0.5), sr)
    ff("-i", p, "-af", "atrim=0:2,afade=t=in:d=0.2,afade=t=out:st=1.6:d=0.4", work / "edit.wav")
    ff("-i", work / "edit.wav", "-c:a", "libmp3lame", "-b:a", "128k", work / "o.mp3")
    y, _ = read_wav(work / "edit.wav")
    d = float(probe(work / "o.mp3")["format"]["duration"])
    rms = lambda a, b: float(np.sqrt((y[int(a * sr):int(b * sr)] ** 2).mean()))
    return [chk("slice to 2000 ms", len(y) == 2 * sr, len(y)),
            chk("fade in 200 ms: first 10 ms near silent, 0.5-1.0 s full", rms(0, 0.01) < 0.02 and near(rms(0.5, 1.0), 0.354, 0.01),
                (round(rms(0, 0.01), 4), round(rms(0.5, 1.0), 3))),
            chk("fade out 400 ms ends near silent", rms(1.99, 2.0) < 0.02, round(rms(1.99, 2.0), 4)),
            chk("mp3 128k duration 2.0-2.1 s (encoder padding)", 2.0 <= d <= 2.1, d)]


def media_23(work):
    sr = 48000
    p = write_wav(work / "in.wav", tone(6.0, 440, sr, 0.3), sr)
    before = p.read_bytes()
    ff("-i", p, "-c:a", "aac", "-b:a", "96k", work / "out.m4a")
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                        str(work / "out.m4a")], capture_output=True, text=True)
    d = float(r.stdout)
    st = probe(work / "out.m4a")["streams"][0]
    return [chk("duration still 6.000 s +-0.03", near(d, 6.0, 0.03), d),
            chk("AAC ~96 kb/s", st["codec_name"] == "aac" and 70_000 <= int(st["bit_rate"]) <= 110_000, st.get("bit_rate")),
            chk("original untouched", p.read_bytes() == before, "same bytes")]


def media_24(work):
    sr = 16000

    def compressor(x, thr_db=-20, ratio=4):
        # RMS detector (one-pole mean square over 20 ms), level referenced to sine peak dBFS
        from scipy.signal import lfilter
        k = math.exp(-1 / (0.02 * sr))
        ms = lfilter([1 - k], [1, -k], x * x)
        db = 10 * np.log10(np.maximum(2 * ms, 1e-18))
        over = np.maximum(0.0, db - thr_db)
        out = x * 10 ** (-(over - over / ratio) / 20)
        return out

    def reverb(x, rt60=0.4):
        rng = np.random.default_rng(1)
        n = int(rt60 * sr)
        ir = rng.standard_normal(n) * np.exp(-6.91 * np.arange(n) / n)
        ir[0] = 1.0
        y = np.convolve(x, ir * 0.3)
        return y / np.abs(y).max() * np.abs(x).max()

    x = tone(1.0, 440, sr, 10 ** (-6 / 20))
    orig = write_wav(work / "orig.wav", x, sr)
    c = compressor(x)
    write_wav(work / "comp.wav", c, sr)
    lvl = 20 * math.log10(np.sqrt((c[sr // 2:] ** 2).mean()) * math.sqrt(2))
    r = reverb(np.concatenate([x[:sr // 4], np.zeros(sr // 2)]))
    write_wav(work / "verb.wav", r, sr)
    tail = float(np.sqrt((r[sr // 4 + 800:sr // 4 + 2400] ** 2).mean()))
    return [chk("-6 dB tone, threshold -20, ratio 4 -> -16.5 dB", near(lvl, -16.5, 0.5), round(lvl, 2)),
            chk("reverb leaves a tail after the dry signal stops", tail > 0.01, round(tail, 4)),
            chk("original kept untouched", np.allclose(read_wav(orig)[0], x, atol=1e-4), "orig.wav")]


def media_28(work):
    img = Image.new("RGB", (32, 24), (120, 80, 40))
    exif = Image.Exif()
    exif[0x010F] = "PhoneMaker"  # Make
    exif[0x0110] = "Model X"
    gps = {1: "N", 2: (24.0, 42.0, 30.0), 3: "E", 4: (46.0, 40.0, 10.0)}
    exif[0x8825] = gps
    p = work / "photo.jpg"
    img.save(p, exif=exif.tobytes())
    read = Image.open(p).getexif()
    gps_read = read.get_ifd(0x8825)
    clean = work / "photo_clean.jpg"
    im = Image.open(p)
    Image.frombytes(im.mode, im.size, im.tobytes()).save(clean, quality=95)
    after = Image.open(clean).getexif()
    return [chk("camera make read", read.get(0x010F) == "PhoneMaker", read.get(0x010F)),
            chk("GPS latitude read", tuple(float(v) for v in gps_read.get(2, ())) == (24.0, 42.0, 30.0), gps_read.get(2)),
            chk("re-saved copy has no EXIF and no GPS", len(after) == 0 and b"PhoneMaker" not in clean.read_bytes(), len(after)),
            chk("original kept", p.is_file() and b"PhoneMaker" in p.read_bytes(), "kept")]


def media_41(work):
    """W3C compositing blend formulas (the spec Mosamem's core tests against)."""
    def multiply(b, s): return b * s
    def screen(b, s): return b + s - b * s
    def hard_light(b, s): return np.where(s <= .5, multiply(b, 2 * s), screen(b, 2 * s - 1))
    def overlay(b, s): return hard_light(s, b)

    def soft_light(b, s):
        d = np.where(b <= .25, ((16 * b - 12) * b + 4) * b, np.sqrt(b))
        return np.where(s <= .5, b - (1 - 2 * s) * b * (1 - b), b + (2 * s - 1) * (d - b))

    def difference(b, s): return np.abs(b - s)
    def color_dodge(b, s): return np.where(b == 0, 0, np.where(s >= 1, 1, np.minimum(1, b / np.maximum(1 - s, 1e-12))))

    b, s = np.array(0.5), np.array(0.25)
    res = {"multiply": float(multiply(b, s)), "screen": float(screen(b, s)), "overlay": float(overlay(b, s)),
           "soft_light": float(soft_light(np.array(0.2), np.array(0.8))), "difference": float(difference(b, s)),
           "color_dodge": float(color_dodge(np.array(0.4), np.array(0.5)))}
    grad = np.linspace(0, 1, 256)
    img = (np.stack([multiply(grad, grad[::-1]), screen(grad, grad[::-1]), overlay(grad, grad[::-1])]) * 255).astype(np.uint8)
    Image.fromarray(np.repeat(img, 20, 0)).save(work / "blends.png")
    jwrite(work, "blends.json", res)
    sl = 0.2 + (2 * 0.8 - 1) * ((((16 * 0.2 - 12) * 0.2 + 4) * 0.2) - 0.2)
    return [chk("multiply 0.5*0.25 = 0.125", res["multiply"] == 0.125, res["multiply"]),
            chk("screen = 0.625", res["screen"] == 0.625, res["screen"]),
            chk("overlay(0.5, 0.25) = hardlight(0.25, 0.5) = 0.25", res["overlay"] == 0.25, res["overlay"]),
            chk("soft-light W3C branch b<=.25", near(res["soft_light"], sl, 1e-12), res["soft_light"]),
            chk("color-dodge 0.4/(1-0.5) = 0.8", near(res["color_dodge"], 0.8, 1e-12), res["color_dodge"]),
            chk("screen of white is white, multiply by black is black", float(screen(np.array(1.0), np.array(0.3))) == 1.0
                and float(multiply(np.array(0.7), np.array(0.0))) == 0.0, "identities")]


PROGRAMS = {
    "MEDIA-01": media_01, "MEDIA-02": media_02, "MEDIA-04": media_04, "MEDIA-05": media_05, "MEDIA-08": media_08,
    "MEDIA-09": media_09, "MEDIA-10": media_10, "MEDIA-11": media_11, "MEDIA-14": media_14, "MEDIA-15": media_15,
    "MEDIA-16": media_16, "MEDIA-17": media_17, "MEDIA-18": media_18, "MEDIA-19": media_19, "MEDIA-20": media_20,
    "MEDIA-21": media_21, "MEDIA-22": media_22, "MEDIA-23": media_23, "MEDIA-24": media_24, "MEDIA-28": media_28,
    "MEDIA-41": media_41,
}
