#!/usr/bin/env python3
"""Proof run for APPX-31…APPX-50: features found in the second batch of analysed desktop apps
(DxO PhotoLab 4, Capture One 21, JPEGmini Pro, FontLab 7, Affinity Designer 1.10, Houdini 18.5,
Internet Download Manager 6.43, Adobe Animate 2024) rebuilt with open tools on synthetic data.
Every recipe is original code; nothing here comes from the vendors' binaries. Each check has a
measurable postcondition. Writes results_studio.json next to this file.

    python smoke_studio.py     # needs numpy, opencv-python, pillow, fontTools, shapely; stdlib for the rest
"""
import hashlib
import http.server
import io
import json
from pathlib import Path
import platform
import shutil
import sys
import tempfile
import threading
import time
import urllib.request

HERE = Path(__file__).resolve().parent
RESULTS = []


def check(pid, name, fn):
    t0 = time.time()
    try:
        ok, detail = fn()
    except Exception as exc:  # a failed recipe is recorded, never hidden
        ok, detail = False, f"{type(exc).__name__}: {str(exc)[:300]}"
    RESULTS.append({"id": pid, "check": name, "ok": bool(ok), "detail": detail, "seconds": round(time.time() - t0, 2)})
    print(("PASS " if ok else "FAIL ") + pid + "  " + name + "  — " + str(detail)[:150])


def psnr(a, b):
    import numpy as np
    mse = np.mean((a.astype(float) - b.astype(float)) ** 2)
    return 99.0 if mse == 0 else 10 * np.log10(255.0 ** 2 / mse)


def ssim(a, b):
    """Single-scale SSIM on luma (Wang et al. 2004), Gaussian window 11, sigma 1.5."""
    import cv2
    import numpy as np
    if a.ndim == 3:
        a, b = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY), cv2.cvtColor(b, cv2.COLOR_RGB2GRAY)
    a, b = a.astype(float), b.astype(float)
    c1, c2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2
    blur = lambda x: cv2.GaussianBlur(x, (11, 11), 1.5)
    ma, mb = blur(a), blur(b)
    va, vb, cov = blur(a * a) - ma * ma, blur(b * b) - mb * mb, blur(a * b) - ma * mb
    m = ((2 * ma * mb + c1) * (2 * cov + c2)) / ((ma * ma + mb * mb + c1) * (va + vb + c2))
    return float(np.mean(m))


def scene(w=640, h=426, seed=7):
    """A synthetic 'photo': sky gradient, ground, buildings with straight edges, a textured disc."""
    import cv2
    import numpy as np
    rng = np.random.default_rng(seed)
    img = np.zeros((h, w, 3), np.uint8)
    for y in range(h // 2):
        img[y] = (120 + y // 3, 170 + y // 4, 235)
    img[h // 2:] = (70, 120, 60)
    for k in range(6):
        x0 = 30 + k * 100
        top = int(rng.integers(60, 170))
        cv2.rectangle(img, (x0, top), (x0 + 70, h // 2 + 40), tuple(int(c) for c in rng.integers(60, 220, 3)), -1)
        for wy in range(top + 10, h // 2 + 30, 22):
            cv2.rectangle(img, (x0 + 10, wy), (x0 + 25, wy + 12), (250, 240, 200), -1)
            cv2.rectangle(img, (x0 + 45, wy), (x0 + 60, wy + 12), (250, 240, 200), -1)
    cv2.circle(img, (w // 2, int(h * 0.78)), 50, (200, 60, 50), -1)
    tex = rng.integers(0, 40, (h, w, 1)).astype(np.uint8)
    img = cv2.add(img, np.repeat(tex, 3, axis=2) // 4)
    return img


def main():
    import cv2
    import numpy as np
    W = Path(tempfile.mkdtemp(prefix="appx_studio_"))
    clean = scene()

    def dehaze():   # DxO ClearView → dark channel prior (He et al. 2009) + guided refinement by box filter
        t_true = 0.45
        A = np.array([235, 235, 235], float)
        hazy = (clean.astype(float) * t_true + A * (1 - t_true)).clip(0, 255).astype(np.uint8)
        I = hazy.astype(float) / 255
        dark = cv2.erode(I.min(axis=2), np.ones((15, 15)))
        n = max(1, dark.size // 1000)
        idx = np.argsort(dark.ravel())[-n:]
        Aest = I.reshape(-1, 3)[idx].max(axis=0)
        t = 1 - 0.95 * cv2.erode((I / Aest).min(axis=2), np.ones((15, 15)))
        t = cv2.blur(t, (31, 31)).clip(0.1, 1)
        J = ((I - Aest) / t[..., None] + Aest).clip(0, 1)
        out = (J * 255).astype(np.uint8)
        before, after = psnr(hazy, clean), psnr(out, clean)
        c0, c1 = hazy.std(), out.std()
        return after > before + 3 and c1 > c0 * 1.3, f"PSNR vs haze-free {before:.1f} → {after:.1f} dB; contrast σ {c0:.1f} → {c1:.1f}"
    check("APPX-31", "dehaze (ClearView-style) by dark channel prior", dehaze)

    def denoise():  # DxO Noise: NoiseRemovalMethod {High, Prime, DeepPrime} → tiered open denoisers
        rng = np.random.default_rng(1)
        noisy = (clean.astype(float) + rng.normal(0, 18, clean.shape)).clip(0, 255).astype(np.uint8)
        fast = cv2.bilateralFilter(noisy, 7, 40, 7)                        # tier 1 "High"
        best = cv2.fastNlMeansDenoisingColored(noisy, None, 12, 12, 7, 21)  # tier 2 "Prime"-class
        p0, p1, p2 = psnr(noisy, clean), psnr(fast, clean), psnr(best, clean)
        return p2 > p0 + 4 and p1 > p0, f"PSNR noisy {p0:.1f} → bilateral {p1:.1f} → NL-means {p2:.1f} dB (AI tier = 📦 model)"
    check("APPX-32", "tiered noise reduction", denoise)

    def keystone():  # DxO Perspective (KeystoningAutoMode, 4/8 points) → homography from a detected quad
        h, w = clean.shape[:2]
        src = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
        tilted = np.float32([[60, 30], [w - 40, 0], [w - 10, h], [20, h - 25]])
        M = cv2.getPerspectiveTransform(src, tilted)
        warped = cv2.warpPerspective(clean, M, (w, h), borderValue=(0, 0, 0))
        # auto: find the quad of the non-black content, order corners, map back to the frame
        mask = (warped.max(axis=2) > 0).astype(np.uint8)
        cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        quad = cv2.approxPolyDP(max(cnts, key=cv2.contourArea), 8, True).reshape(-1, 2).astype(np.float32)
        s, d = quad.sum(1), np.diff(quad, axis=1).ravel()
        ordered = np.float32([quad[s.argmin()], quad[d.argmin()], quad[s.argmax()], quad[d.argmax()]])
        back = cv2.warpPerspective(warped, cv2.getPerspectiveTransform(ordered, src), (w, h))
        err = np.abs(ordered - tilted).max()
        inner = (slice(20, h - 20), slice(20, w - 20))
        return err < 3 and psnr(back[inner], clean[inner]) > 22, f"corner error {err:.1f}px; restored PSNR {psnr(back[inner], clean[inner]):.1f} dB"
    check("APPX-33", "automatic keystone / perspective correction", keystone)

    def lens():      # DxO Distortion, Affinity lens_correction_data → Brown radial model + cv2.undistort
        h, w = clean.shape[:2]
        K = np.float32([[w, 0, w / 2], [0, w, h / 2], [0, 0, 1]])
        dist = np.float32([0.35, 0, 0, 0, 0])   # barrel distortion simulated by inverse remap
        ys, xs = np.indices((h, w), np.float32)
        pts = np.stack([xs.ravel(), ys.ravel()], 1).reshape(-1, 1, 2)
        und = cv2.undistortPoints(pts, K, dist, P=K).reshape(h, w, 2)
        distorted = cv2.remap(clean, und[..., 0], und[..., 1], cv2.INTER_LINEAR)
        fixed = cv2.undistort(distorted, K, dist)
        c = (slice(h // 6, -h // 6), slice(w // 6, -w // 6))
        p0, p1 = psnr(distorted[c], clean[c]), psnr(fixed[c], clean[c])
        return p1 > p0 + 5, f"PSNR distorted {p0:.1f} → corrected {p1:.1f} dB (k1=0.35)"
    check("APPX-34", "lens distortion correction", lens)

    def chroma_ab():  # DxO ChromaticAberration → register R and B to G by radial scale search
        h, w = clean.shape[:2]
        def scale_ch(ch, s):
            M = cv2.getRotationMatrix2D((w / 2, h / 2), 0, s)
            return cv2.warpAffine(ch, M, (w, h), borderMode=cv2.BORDER_REFLECT)
        r, g, b = cv2.split(clean)
        fringed = cv2.merge([scale_ch(r, 1.012), g, scale_ch(b, 0.988)])
        def best(ch):
            cands = np.linspace(0.97, 1.03, 61)
            errs = [np.abs(scale_ch(ch, s).astype(float) - cv2.split(fringed)[1].astype(float))[40:-40, 40:-40].mean() for s in cands]
            return cands[int(np.argmin(errs))]
        sr, sb = best(cv2.split(fringed)[0]), best(cv2.split(fringed)[2])
        fixed = cv2.merge([scale_ch(cv2.split(fringed)[0], sr), cv2.split(fringed)[1], scale_ch(cv2.split(fringed)[2], sb)])
        c = (slice(40, -40), slice(40, -40))
        p0, p1 = psnr(fringed[c], clean[c]), psnr(fixed[c], clean[c])
        return p1 > p0 + 4, f"R×{sr:.3f} B×{sb:.3f} found (true 1/1.012, 1/0.988); PSNR {p0:.1f} → {p1:.1f} dB"
    check("APPX-35", "lateral chromatic aberration removal", chroma_ab)

    def develop():   # DxO WhiteBalance/ToneCurve/HSL, Capture One Presets60 (Curve, Color Balance)
        cast = (clean.astype(float) * [1.25, 1.0, 0.75]).clip(0, 255)
        gains = cast.reshape(-1, 3).mean(0).mean() / cast.reshape(-1, 3).mean(0)   # grey world
        wb = (cast * gains).clip(0, 255)
        x = np.array([0, 64, 128, 192, 255], float); y = np.array([0, 50, 128, 210, 255], float)   # S-curve
        lut = np.interp(np.arange(256), x, y).astype(np.uint8)
        toned = cv2.LUT(wb.astype(np.uint8), lut)
        hsv = cv2.cvtColor(toned, cv2.COLOR_RGB2HSV)
        hsv[..., 1] = (hsv[..., 1].astype(float) * 1.2).clip(0, 255)            # global saturation (HSL)
        out = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
        means = cast.reshape(-1, 3).mean(0); m2 = wb.reshape(-1, 3).mean(0)
        spread0, spread1 = means.max() - means.min(), m2.max() - m2.min()
        return spread1 < 2 and out.std() > wb.std(), f"channel-mean spread {spread0:.1f} → {spread1:.2f} after grey-world WB; S-curve σ {wb.std():.1f} → {out.std():.1f}"
    check("APPX-36", "white balance + tone curve + HSL develop", develop)

    def grain_vignette():  # Capture One Presets60/Film Grain, DxO Grain + CreativeVignetting
        h, w = clean.shape[:2]
        rng = np.random.default_rng(3)
        g = cv2.GaussianBlur(rng.normal(0, 1, (h, w)).astype(np.float32), (0, 0), 0.8)
        g = g / g.std() * 8
        yy, xx = np.indices((h, w)); r = np.hypot((xx - w / 2) / (w / 2), (yy - h / 2) / (h / 2))
        vig = 1 - 0.45 * np.clip(r - 0.4, 0, None) ** 1.5
        out = ((clean.astype(float) + g[..., None]) * vig[..., None]).clip(0, 255).astype(np.uint8)
        corner, centre = out[:30, :30].mean() / clean[:30, :30].mean(), out[h // 2 - 15:h // 2 + 15, w // 2 - 15:w // 2 + 15].mean() / clean[h // 2 - 15:h // 2 + 15, w // 2 - 15:w // 2 + 15].mean()
        grain = (out.astype(float) - (clean.astype(float) * vig[..., None])).std()
        return corner < 0.85 and centre > 0.97 and 5 < grain < 12, f"corner ×{corner:.2f}, centre ×{centre:.2f}, grain σ {grain:.1f}"
    check("APPX-37", "film grain + vignette look", grain_vignette)

    def watermark():  # DxO Correction.Watermark → alpha-composited mark with exact opacity
        from PIL import Image, ImageDraw
        base = Image.fromarray(clean).convert("RGBA")
        mark = Image.new("RGBA", base.size, (0, 0, 0, 0))
        ImageDraw.Draw(mark).rectangle([440, 360, 620, 410], fill=(255, 255, 255, int(255 * 0.4)))
        out = np.array(Image.alpha_composite(base, mark).convert("RGB")).astype(float)
        expect = clean[385, 530].astype(float) * 0.6 + 255 * 0.4
        err = np.abs(out[385, 530] - expect).max()
        untouched = np.abs(out[10, 10] - clean[10, 10]).max()
        return err <= 1.5 and untouched == 0, f"40% mark pixel error {err:.1f}, outside the mark unchanged"
    check("APPX-38", "watermark with exact opacity", watermark)

    def smart_jpeg():  # JPEGmini → smallest JPEG quality whose SSIM stays ≥ 0.985 (binary search)
        from PIL import Image
        src = Image.fromarray(cv2.GaussianBlur(clean, (3, 3), 0))   # a photo-like, not per-pixel-noise, source
        srcarr = np.array(src)
        def enc(q):
            b = io.BytesIO(); src.save(b, "JPEG", quality=q, optimize=True, progressive=True); return b.getvalue()
        def score(data):
            return ssim(np.array(Image.open(io.BytesIO(data)).convert("RGB")), srcarr)
        ref = enc(95)
        target = score(ref) - 0.01            # "visually the same as q95" within 0.01 SSIM
        lo, hi, best = 30, 95, 95
        while lo <= hi:
            mid = (lo + hi) // 2
            if score(enc(mid)) >= target:
                best, hi = mid, mid - 1
            else:
                lo = mid + 1
        out = enc(best)
        s = score(out)
        return len(out) < len(ref) * 0.75 and s >= target, f"q95 {len(ref)//1024} KB → q{best} {len(out)//1024} KB ({100 - 100*len(out)//len(ref)}% smaller) at SSIM {s:.4f} (target {target:.4f})"
    check("APPX-39", "perceptual JPEG recompression (JPEGmini-style)", smart_jpeg)

    def contact_sheet():  # Capture One PrintTemplates / WebContactSheet → grid pages + PDF
        from PIL import Image, ImageDraw
        thumbs = [Image.fromarray(np.roll(clean, k * 37, axis=1)) for k in range(14)]
        cols, rows, cell = 4, 3, (300, 220)
        pages = []
        for p in range(0, len(thumbs), cols * rows):
            page = Image.new("RGB", (cols * cell[0] + 40, rows * cell[1] + 80), "white")
            d = ImageDraw.Draw(page)
            for i, t in enumerate(thumbs[p:p + cols * rows]):
                t = t.copy(); t.thumbnail((cell[0] - 20, cell[1] - 40))
                x, y = 20 + (i % cols) * cell[0], 60 + (i // cols) * cell[1]
                page.paste(t, (x, y)); d.text((x, y + t.height + 4), f"IMG_{p + i + 1:04d}", fill="black")
            pages.append(page)
        pdf = W / "sheet.pdf"
        pages[0].save(pdf, save_all=True, append_images=pages[1:])
        n = pdf.read_bytes().count(b"/Type /Page\n") or pdf.read_bytes().count(b"/Type /Page")
        return len(pages) == 2 and pdf.stat().st_size > 20000, f"14 images → {len(pages)} pages of 4×3, PDF {pdf.stat().st_size//1024} KB"
    check("APPX-40", "contact sheet / print template to PDF", contact_sheet)

    def presets():   # Capture One .costyle / DxO preset files (+ versioned settings, Compatibility.V7…V15)
        preset = {"schema": 2, "name": "warm-contrast", "ops": [{"op": "wb", "gains": [1.05, 1.0, 0.95]},
                                                                {"op": "curve", "x": [0, 128, 255], "y": [0, 120, 255]}]}
        def migrate(p):   # v1 had a single "warmth" number; old files keep opening
            if p.get("schema", 1) == 1:
                w = p.pop("warmth", 0.0)
                p["ops"] = [{"op": "wb", "gains": [1 + w, 1.0, 1 - w]}] + p.get("ops", []); p["schema"] = 2
            return p
        def apply(img, p):
            x = img.astype(float)
            for o in p["ops"]:
                if o["op"] == "wb":
                    x = x * o["gains"]
                elif o["op"] == "curve":
                    x = np.interp(x, o["x"], o["y"])
            return x.clip(0, 255).astype(np.uint8)
        path = W / "warm.preset.json"; path.write_text(json.dumps(preset))
        a = apply(clean, json.loads(path.read_text())); b = apply(clean, json.loads(path.read_text()))
        old = migrate({"schema": 1, "warmth": 0.05, "ops": [{"op": "curve", "x": [0, 128, 255], "y": [0, 120, 255]}]})
        c = apply(clean, old)
        return np.array_equal(a, b) and np.abs(a.astype(int) - c.astype(int)).max() <= 1, "preset file applies deterministically; schema-1 file migrates to the same result"
    check("APPX-41", "versioned preset / style files", presets)

    def xmp():       # Lightroom/ACDSee/DxO Search.Metadata, Affinity libxmp → XMP sidecar with rating + keywords
        import xml.etree.ElementTree as ET
        img = W / "IMG_0001.jpg"; cv2.imwrite(str(img), cv2.cvtColor(clean, cv2.COLOR_RGB2BGR))
        ns = {"x": "adobe:ns:meta/", "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
              "xmp": "http://ns.adobe.com/xap/1.0/", "dc": "http://purl.org/dc/elements/1.1/"}
        for k, v in ns.items():
            ET.register_namespace(k, v)
        root = ET.Element(f"{{{ns['x']}}}xmpmeta"); rdf = ET.SubElement(root, f"{{{ns['rdf']}}}RDF")
        desc = ET.SubElement(rdf, f"{{{ns['rdf']}}}Description", {f"{{{ns['xmp']}}}Rating": "4", f"{{{ns['xmp']}}}Label": "Green"})
        bag = ET.SubElement(ET.SubElement(desc, f"{{{ns['dc']}}}subject"), f"{{{ns['rdf']}}}Bag")
        for kw in ("مدينة", "city", "sunset"):
            ET.SubElement(bag, f"{{{ns['rdf']}}}li").text = kw
        side = img.with_suffix(".xmp"); ET.ElementTree(root).write(side, encoding="utf-8", xml_declaration=True)
        back = ET.parse(side).getroot()
        d = back.find(f".//{{{ns['rdf']}}}Description")
        kws = [li.text for li in back.iter(f"{{{ns['rdf']}}}li")]
        return d.get(f"{{{ns['xmp']}}}Rating") == "4" and "مدينة" in kws, f"sidecar {side.name}: rating 4, label Green, keywords {kws}"
    check("APPX-42", "XMP sidecar: rating, label, keywords", xmp)

    def horizon():   # DxO Horizon, Capture One AutoCrop → Hough dominant angle, rotate, crop to the largest inner rect
        h, w = clean.shape[:2]
        canvas = np.full((h, w, 3), 90, np.uint8)
        cv2.line(canvas, (0, h // 2), (w, h // 2), (255, 255, 255), 3)
        canvas[h // 2 + 2:] = (60, 110, 60)
        M = cv2.getRotationMatrix2D((w / 2, h / 2), 3.5, 1.0)
        tilted = cv2.warpAffine(canvas, M, (w, h), borderMode=cv2.BORDER_REPLICATE)
        edges = cv2.Canny(cv2.cvtColor(tilted, cv2.COLOR_RGB2GRAY), 50, 150)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 720, 120, minLineLength=w // 3, maxLineGap=10)
        angs = [np.degrees(np.arctan2(y2 - y1, x2 - x1)) for x1, y1, x2, y2 in lines.reshape(-1, 4)]
        ang = float(np.median([a for a in angs if abs(a) < 20]))
        fixed = cv2.warpAffine(tilted, cv2.getRotationMatrix2D((w / 2, h / 2), ang, 1.0), (w, h), borderMode=cv2.BORDER_REPLICATE)
        e2 = cv2.Canny(cv2.cvtColor(fixed, cv2.COLOR_RGB2GRAY), 50, 150)
        l2 = cv2.HoughLinesP(e2, 1, np.pi / 720, 120, minLineLength=w // 3, maxLineGap=10)
        resid = float(np.median([abs(np.degrees(np.arctan2(y2 - y1, x2 - x1))) for x1, y1, x2, y2 in l2.reshape(-1, 4)]))
        return abs(abs(ang) - 3.5) < 0.4 and resid < 0.4, f"horizon tilt found {ang:.2f}° (true ±3.5°), residual {resid:.2f}°"
    check("APPX-43", "auto horizon straighten", horizon)

    def font():      # FontLab 7 (freetype, harfbuzz, kerning pair data, standard.nam) → fontTools FontBuilder
        from fontTools.fontBuilder import FontBuilder
        from fontTools.pens.ttGlyphPen import TTGlyphPen
        from fontTools.ttLib import TTFont
        from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
        def box(x0, y0, x1, y1, pen):
            pen.moveTo((x0, y0)); pen.lineTo((x0, y1)); pen.lineTo((x1, y1)); pen.lineTo((x1, y0)); pen.closePath()
        glyphs = {}
        for name, rects in {".notdef": [(50, 0, 450, 700)], "space": [], "A": [(0, 0, 120, 700), (380, 0, 500, 700), (0, 600, 500, 700), (0, 300, 500, 400)],
                            "V": [(0, 100, 120, 700), (380, 100, 500, 700), (0, 0, 500, 120)]}.items():
            pen = TTGlyphPen(None)
            for r in rects:
                box(*r, pen)
            glyphs[name] = pen.glyph()
        fb = FontBuilder(1000, isTTF=True)
        order = list(glyphs)
        fb.setupGlyphOrder(order); fb.setupCharacterMap({0x20: "space", 0x41: "A", 0x56: "V"})
        fb.setupGlyf(glyphs); fb.setupHorizontalMetrics({n: (560 if n != "space" else 250, 0) for n in order})
        fb.setupHorizontalHeader(ascent=800, descent=-200)
        fb.setupNameTable({"familyName": "KOSIF Test", "styleName": "Regular"}); fb.setupOS2(); fb.setupPost()
        addOpenTypeFeaturesFromString(fb.font, "feature kern { pos A V -80; pos V A -80; } kern;")
        path = W / "kosif-test.ttf"; fb.save(str(path))
        f = TTFont(str(path))
        pp = f["GPOS"].table.LookupList.Lookup[0].SubTable[0]
        val = pp.PairSet[0].PairValueRecord[0].Value1.XAdvance
        return f["maxp"].numGlyphs == 4 and val == -80, f"TTF built: {f['maxp'].numGlyphs} glyphs, kern A/V {val} in GPOS, {path.stat().st_size} bytes"
    check("APPX-44", "build a font with kerning (FontLab-style)", font)

    def booleans():  # Affinity libgeometry, Houdini he_boolean → shapely boolean ops → SVG path
        from shapely.geometry import Point, box as sbox
        a, b = Point(0, 0).buffer(50, quad_segs=64), sbox(0, -60, 80, 60)
        uni, diff, inter = a.union(b), a.difference(b), a.intersection(b)
        ok = abs(uni.area - (a.area + b.area - inter.area)) < 1e-6 and abs(diff.area - (a.area - inter.area)) < 1e-6
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-60 -70 150 140">{diff.svg()}</svg>'
        (W / "bool.svg").write_text(svg)
        return ok and abs(diff.area - np.pi * 2500 / 2) < 5, f"circle − box = {diff.area:.0f} (half disc {np.pi*1250:.0f}); union/intersection areas consistent; SVG written"
    check("APPX-45", "vector boolean operations to SVG", booleans)

    def chops():     # Houdini CHOPs (Lag, Noise, Envelope, Cycle) → channel ops for motion curves
        fps, n = 30, 120
        t = np.arange(n) / fps
        step = (t >= 1).astype(float)                         # a hard key at 1 s
        lag = np.zeros(n); a = 1 - np.exp(-1 / (0.25 * fps))  # Lag CHOP: one-pole smoothing, τ = 0.25 s
        for i in range(1, n):
            lag[i] = lag[i - 1] + a * (step[i] - lag[i - 1])
        rng = np.random.default_rng(5)
        noise = np.interp(t, np.linspace(0, t[-1], 9), rng.uniform(-1, 1, 9))   # Noise CHOP: smooth value noise
        cycle = np.tile(np.sin(np.linspace(0, 2 * np.pi, fps, endpoint=False)), n // fps)   # Cycle CHOP
        env = np.convolve(np.abs(cycle), np.ones(5) / 5, mode="same")              # Envelope CHOP
        t63 = t[np.argmax(lag >= 0.632)] - 1.0
        return abs(t63 - 0.25) < 0.05 and np.abs(np.diff(noise)).max() < 0.2 and abs(cycle[:fps].sum()) < 1e-9, \
            f"lag reaches 63% in {t63:.2f}s (τ 0.25); noise max step {np.abs(np.diff(noise)).max():.3f}; cycle loops seamlessly; envelope peak {env.max():.2f}"
    check("APPX-46", "motion channel ops: lag, noise, cycle, envelope", chops)

    def pdg():       # Houdini PDG / TOPs → dependency graph with content-hash caching
        ran = []
        graph = {"fetch": [], "denoise": ["fetch"], "grade": ["denoise"], "thumb": ["fetch"], "sheet": ["grade", "thumb"]}
        cache = {}
        def run_graph(params):
            done, order = set(), []
            def visit(n):
                if n in done:
                    return
                for d in graph[n]:
                    visit(d)
                key = hashlib.sha256(json.dumps([n, params.get(n), [cache.get(d) for d in graph[n]]]).encode()).hexdigest()
                if cache.get(n) != key:
                    ran.append(n); cache[n] = key
                done.add(n); order.append(n)
            for n in graph:
                visit(n)
            return order
        order = run_graph({"grade": 1}); first = list(ran); ran.clear()
        run_graph({"grade": 1}); second = list(ran); ran.clear()
        run_graph({"grade": 2}); third = list(ran)
        topo = all(order.index(d) < order.index(n) for n in graph for d in graph[n])
        return topo and len(first) == 5 and second == [] and third == ["grade", "sheet"], \
            f"first run {first}; rerun cached {second}; after a grade change only {third}"
    check("APPX-47", "task graph with dependency order and caching (PDG-style)", pdg)

    def segmented_download():   # IDM → N parallel HTTP Range parts, resume after interruption, SHA-256 verify
        payload = np.random.default_rng(9).integers(0, 256, 3_000_000, dtype=np.uint8).tobytes()
        srv_dir = W / "srv"; srv_dir.mkdir(); (srv_dir / "big.bin").write_bytes(payload)

        class H(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *a, **k):
                super().__init__(*a, directory=str(srv_dir), **k)
            def log_message(self, *a):
                pass
            def do_GET(self):
                rng = self.headers.get("Range")
                data = (srv_dir / "big.bin").read_bytes()
                if rng:
                    s, e = rng.split("=")[1].split("-"); s, e = int(s), int(e)
                    self.send_response(206); self.send_header("Content-Range", f"bytes {s}-{e}/{len(data)}")
                    body = data[s:e + 1]
                else:
                    self.send_response(200); body = data
                self.send_header("Accept-Ranges", "bytes"); self.send_header("Content-Length", str(len(body))); self.end_headers()
                self.wfile.write(body)
            def do_HEAD(self):
                self.send_response(200); self.send_header("Accept-Ranges", "bytes")
                self.send_header("Content-Length", str(len(payload))); self.end_headers()
        srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        url = f"http://127.0.0.1:{srv.server_address[1]}/big.bin"
        try:
            req = urllib.request.Request(url, method="HEAD")
            size = int(urllib.request.urlopen(req, timeout=10).headers["Content-Length"])
            parts, n = W / "parts", 6
            parts.mkdir()
            bounds = [(i * size // n, (i + 1) * size // n - 1) for i in range(n)]
            def fetch(i, limit=None):
                s, e = bounds[i]; p = parts / f"{i}.part"
                have = p.stat().st_size if p.exists() else 0      # resume from what is already on disk
                if s + have > e:
                    return
                r = urllib.request.Request(url, headers={"Range": f"bytes={s + have}-{e}"})
                with urllib.request.urlopen(r, timeout=10) as resp, open(p, "ab") as out:
                    while True:
                        chunk = resp.read(65536 if limit is None else min(65536, limit))
                        if not chunk:
                            break
                        out.write(chunk)
                        if limit is not None:
                            limit -= len(chunk)
                            if limit <= 0:
                                return            # simulated interruption
            fetch(2, limit=100_000)              # part 2 is cut off mid-way
            threads = [threading.Thread(target=fetch, args=(i,)) for i in range(n)]
            [t.start() for t in threads]; [t.join() for t in threads]
            out = W / "big.bin"
            with open(out, "wb") as o:
                for i in range(n):
                    o.write((parts / f"{i}.part").read_bytes())
            ok = hashlib.sha256(out.read_bytes()).hexdigest() == hashlib.sha256(payload).hexdigest()
            return ok, f"{size} bytes in {n} ranged parts, part 2 resumed after a cut at 100000 bytes, SHA-256 match {ok}"
        finally:
            srv.shutdown()
    check("APPX-48", "segmented, resumable download (IDM-style)", segmented_download)

    def tween():     # Adobe Animate classic/motion tween, onion skin, sprite-sheet export
        from PIL import Image, ImageDraw
        ease = lambda u: u * u * (3 - 2 * u)   # smoothstep ease in-out
        k0, k1, frames = (40, 100), (360, 60), 24
        pos = [(k0[0] + (k1[0] - k0[0]) * ease(i / (frames - 1)), k0[1] + (k1[1] - k0[1]) * ease(i / (frames - 1))) for i in range(frames)]
        def draw(p, alpha=255):
            im = Image.new("RGBA", (420, 160), (0, 0, 0, 0)); ImageDraw.Draw(im).ellipse([p[0] - 15, p[1] - 15, p[0] + 15, p[1] + 15], fill=(230, 80, 40, alpha)); return im
        onion = Image.new("RGBA", (420, 160), (255, 255, 255, 255))
        for k, a in ((9, 60), (10, 120), (11, 255)):
            onion = Image.alpha_composite(onion, draw(pos[k], a))
        sheet = Image.new("RGBA", (420 * 6, 160 * 4), (0, 0, 0, 0))
        for i, p in enumerate(pos):
            sheet.paste(draw(p), ((i % 6) * 420, (i // 6) * 160))
        meta = {"frames": [{"x": (i % 6) * 420, "y": (i // 6) * 160, "w": 420, "h": 160} for i in range(frames)], "fps": 24}
        sheet.save(W / "sheet.png"); (W / "sheet.json").write_text(json.dumps(meta))
        v = np.diff(np.array(pos)[:, 0])
        return pos[0] == k0 and np.allclose(pos[-1], k1) and v[0] < v[frames // 2] and v[-1] < v[frames // 2], \
            f"{frames} tween frames hit both keys, eased (speed {v[0]:.1f} → {v[frames//2]:.1f} → {v[-1]:.1f} px/frame); onion skin + 6×4 sprite sheet + JSON"
    check("APPX-49", "eased tween, onion skin, sprite sheet (Animate-style)", tween)

    def tone_map():  # DxO SelectiveTonalControl / Smart Lighting, Capture One HDR sliders → exposure fusion
        stack = [(clean.astype(float) * g).clip(0, 255).astype(np.uint8) for g in (0.35, 1.0, 2.2)]
        fused = cv2.createMergeMertens().process(stack)   # 8-bit in, float 0..1 out
        fused = (fused.clip(0, 1) * 255).astype(np.uint8)
        clip_hi = lambda x: (x >= 250).mean(); clip_lo = lambda x: (x <= 5).mean()
        return clip_hi(fused) < clip_hi(stack[2]) and clip_lo(fused) <= clip_lo(stack[0]) and ssim(fused, clean) > 0.6, \
            f"clipped highlights {clip_hi(stack[2]):.1%} → {clip_hi(fused):.1%}, crushed shadows {clip_lo(stack[0]):.1%} → {clip_lo(fused):.1%}"
    check("APPX-50", "exposure fusion / selective tonal control", tone_map)

    out = {"date": time.strftime("%Y-%m-%d"), "host": f"{platform.system()} {platform.machine()}",
           "python": platform.python_version(), "opencv": cv2.__version__, "numpy": np.__version__,
           "passed": sum(r["ok"] for r in RESULTS), "total": len(RESULTS), "results": RESULTS}
    (HERE / "results_studio.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    shutil.rmtree(W, ignore_errors=True)
    print(f"{out['passed']}/{out['total']} passed")
    return 0 if out["passed"] == out["total"] else 1


if __name__ == "__main__":
    sys.exit(main())
