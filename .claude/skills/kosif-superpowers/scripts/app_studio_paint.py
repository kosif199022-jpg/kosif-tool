"""KOSIF App Studio, painting batch: the effects, adjustments, compositing and brush features found with REA in
Paint.NET 4.2.13 (PaintDotNet.Effects.dll: 64 *Effect types), the Adobe Photoshop 2025 offline package (Filters,
3DLUTs, Sky_Presets, sensei_models) and Microsoft Paint 11.2605 (PaintUI.winmd AIFeature/ToolKind, PaintTools.dll
brush tools, ProjectFile.dll layer stack). Original code on numpy/OpenCV/Pillow; no vendor code, models or assets.

Loaded by app_studio.py (`register(globals())`), so every op here runs through the same CLI:
    python scripts/app_studio.py oil-paint photo.jpg -o oil.jpg --set brush=4 coarseness=24
    python scripts/app_studio.py blend base.jpg top.png -o out.png --set mode=soft-light opacity=0.8
    python scripts/app_studio.py layers stack.json -o art.ora          # OpenRaster (GIMP/Krita open it) or .png
    python scripts/app_studio.py lut-make - -o teal.cube --set look=teal-orange ; app_studio.py lut a.jpg -o b.jpg --set cube=teal.cube
    python scripts/app_studio.py paint strokes.json -o drawing.png     # MS Paint brushes: crayon, watercolor, oil…
"""
import json
import math
from pathlib import Path
import zipfile

PDN = "Paint.NET 4.2.13 (REA: PaintDotNet.Effects.dll)"
PS = "Photoshop 2025 (package listing)"
MSP = "Microsoft Paint 11.2605 (REA: PaintUI.winmd, PaintTools.dll)"


def register(g):
    op, read, write, f, res, np_cv, BASE = g["op"], g["read"], g["write"], g["f"], g["res"], g["np_cv"], g["BASE"]
    PIL = BASE + ["pip:pillow"]

    def num(p, key, default):
        return float(p.get(key, default))

    def hexcol(c, default=(0, 0, 0)):
        """'#rrggbb' → BGR tuple."""
        c = str(c or "").lstrip("#")
        if len(c) != 6:
            return default
        r, gg, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
        return (b, gg, r)

    def remap(img, mx, my, border=None):
        np, cv2 = np_cv()
        border = cv2.BORDER_REFLECT if border is None else border
        return cv2.remap(img, mx.astype(np.float32), my.astype(np.float32), cv2.INTER_LINEAR, borderMode=border)

    def grid(img):
        np, _ = np_cv()
        h, w = img.shape[:2]
        y, x = np.mgrid[0:h, 0:w].astype(np.float32)
        return x, y, w, h

    def local_std(a):
        np, cv2 = np_cv()
        g = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY).astype(np.float32)
        m = cv2.blur(g, (5, 5))
        return float(np.sqrt(np.maximum(cv2.blur(g * g, (5, 5)) - m * m, 0)).mean())

    def changed(a, b):
        np, _ = np_cv()
        return float(np.mean(np.abs(a.astype(np.int16) - b.astype(np.int16))))

    # ============================================================== Paint.NET effects (APPX-99 … APPX-104)
    FX = {}

    def fx(name, appx, ar, en, params):
        def deco(fn):
            FX[name] = fn

            @op(name, f"{PDN}: {fn.__doc__.split(':')[0]}", appx, BASE, ar, f"{en} ; {params}")
            def run(inp, out, p, _fn=fn, _name=name):
                src = read(inp[0])
                o, checks = _fn(src, p)
                metrics = {"mean_abs_change": changed(src, o) if o.shape == src.shape else None, **checks}
                ok = bool(checks.pop("_ok", None)) if "_ok" in checks else None
                metrics.pop("_ok", None)
                return res(_name, write(out, o), metrics, verified=bool(ok))
            return fn
        return deco

    # ---- artistic
    @fx("oil-paint", "APPX-99", "رسم زيتي", "oil painting (most-frequent intensity bin per brush window)", "brush=3 coarseness=20")
    def oil_paint(img, p):
        """OilPaintingEffect: BrushSize, Coarseness"""
        np, cv2 = np_cv()
        r, L = int(num(p, "brush", 3)), int(num(p, "coarseness", 20))
        k = (2 * r + 1, 2 * r + 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        q = (gray.astype(np.int32) * L // 256)
        best = np.full(gray.shape, -1.0, np.float32)
        out = np.zeros(img.shape, np.float32)
        for lvl in range(L):
            m = (q == lvl).astype(np.float32)
            if not m.any():
                continue
            cnt = cv2.boxFilter(m, -1, k, normalize=False)
            upd = cnt > best
            if upd.any():
                s = cv2.boxFilter(img.astype(np.float32) * m[..., None], -1, k, normalize=False)
                out[upd] = s[upd] / np.maximum(cnt[upd], 1)[..., None]
                best[upd] = cnt[upd]
        o = out.clip(0, 255).astype(np.uint8)
        # oil painting flattens texture inside each stroke: mean 5×5 local deviation must drop
        return o, {"local_std_before": local_std(img), "local_std_after": local_std(o), "_ok": local_std(o) < local_std(img)}

    @fx("ink-sketch", "APPX-99", "رسم بالحبر", "ink sketch: inked outlines over washed colour", "ink=50 coloring=50")
    def ink_sketch(img, p):
        """InkSketchEffect: InkOutline, Coloring"""
        np, cv2 = np_cv()
        ink, col = num(p, "ink", 50) / 100, num(p, "coloring", 50) / 100
        g = cv2.GaussianBlur(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), (3, 3), 0).astype(np.float32)
        mag = cv2.magnitude(cv2.Sobel(g, cv2.CV_32F, 1, 0), cv2.Sobel(g, cv2.CV_32F, 0, 1))
        a = (mag / (mag.max() + 1e-6) * (0.5 + 2.5 * ink)).clip(0, 1)
        gray3 = cv2.cvtColor(g.astype(np.uint8), cv2.COLOR_GRAY2BGR).astype(np.float32)
        base = gray3 * (1 - col) + img.astype(np.float32) * col
        base = 255 - (255 - base) * 0.7               # washed paper
        o = (base * (1 - a[..., None])).clip(0, 255).astype(np.uint8)
        return o, {"ink_coverage": float((a > 0.5).mean())}

    @fx("pencil-sketch", "APPX-99", "رسم بالرصاص", "pencil sketch (colour-dodge of inverted blur)", "tip=2 range=0")
    def pencil_sketch(img, p):
        """PencilSketchEffect: PencilTipSize, ColorRange"""
        np, cv2 = np_cv()
        tip, rng = num(p, "tip", 2), num(p, "range", 0)
        g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
        b = cv2.GaussianBlur(255 - g, (0, 0), 1 + tip * 2)
        d = (g * 255 / (255 - b + 1)).clip(0, 255)
        d = 255 * (d / 255) ** (1 + rng / 50)
        o = cv2.cvtColor(d.astype(np.uint8), cv2.COLOR_GRAY2BGR)
        return o, {"white_fraction": float((d > 230).mean()), "_ok": float((d > 230).mean()) > 0.3}

    # ---- distort
    def polar(img, p):
        np, _ = np_cv()
        x, y, w, h = grid(img)
        cx, cy = num(p, "cx", 0.5) * w, num(p, "cy", 0.5) * h
        return x - cx, y - cy, cx, cy, w, h

    @fx("twist", "APPX-100", "التواء دوّامي", "twist around the centre, strongest at the middle", "angle=90 radius=0.5 cx cy")
    def twist(img, p):
        """TwistEffect: Angle, Radius"""
        np, _ = np_cv()
        dx, dy, cx, cy, w, h = polar(img, p)
        R = num(p, "radius", 0.5) * min(w, h)
        r = np.hypot(dx, dy)
        t = np.where(r < R, (1 - r / R) ** 2, 0) * math.radians(num(p, "angle", 90))
        c, s = np.cos(t), np.sin(t)
        o = remap(img, cx + dx * c - dy * s, cy + dx * s + dy * c)
        outside = r > R + 1
        err = float(np.abs(o[outside].astype(int) - img[outside].astype(int)).max()) if outside.any() else 0.0
        return o, {"radius_px": float(R), "outside_max_error": err, "_ok": err <= 1}

    @fx("bulge", "APPX-100", "انتفاخ/انقباض", "bulge (amount>0) or pinch (amount<0)", "amount=0.6 radius=0.5 cx cy")
    def bulge(img, p):
        """BulgeEffect: Amount, Offset"""
        np, _ = np_cv()
        dx, dy, cx, cy, w, h = polar(img, p)
        R, a = num(p, "radius", 0.5) * min(w, h), max(-0.95, min(0.95, num(p, "amount", 0.6)))
        r = np.hypot(dx, dy)
        k = np.where(r < R, 1 - a * (1 - (r / R) ** 2), 1.0)
        o = remap(img, cx + dx * k, cy + dy * k)
        outside = r > R + 1
        err = float(np.abs(o[outside].astype(int) - img[outside].astype(int)).max()) if outside.any() else 0.0
        return o, {"amount": a, "outside_max_error": err, "_ok": err <= 1}

    @fx("polar-inversion", "APPX-100", "انعكاس قطبي", "polar inversion z → a·z/|z|²", "amount=1 edge=reflect|wrap")
    def polar_inversion(img, p):
        """PolarInversionEffect: Amount, EdgeBehavior"""
        np, cv2 = np_cv()
        dx, dy, cx, cy, w, h = polar(img, p)
        s = min(w, h) / 2
        zx, zy = dx / s, dy / s
        r2 = np.maximum(zx * zx + zy * zy, 1e-4)
        a = num(p, "amount", 1)
        border = cv2.BORDER_WRAP if p.get("edge") == "wrap" else cv2.BORDER_REFLECT
        return remap(img, cx + s * a * zx / r2, cy + s * a * zy / r2, border), {}

    def smooth_field(h, w, scale, seed):
        np, cv2 = np_cv()
        rng = np.random.default_rng(seed)
        gh, gw = max(2, int(h / scale) + 2), max(2, int(w / scale) + 2)
        return cv2.resize(rng.standard_normal((gh, gw)).astype(np.float32), (w, h), interpolation=cv2.INTER_CUBIC)

    @fx("dents", "APPX-100", "تموجات وانبعاجات", "dents: smooth random displacement", "scale=40 strength=8 seed=1")
    def dents(img, p):
        """DentsEffect: Scale, Refraction, Roughness, Tension, Seed"""
        x, y, w, h = grid(img)
        sc, st, sd = num(p, "scale", 40), num(p, "strength", 8), int(num(p, "seed", 1))
        fx_ = smooth_field(h, w, sc, sd) + 0.5 * smooth_field(h, w, sc / 2, sd + 1)
        fy_ = smooth_field(h, w, sc, sd + 2) + 0.5 * smooth_field(h, w, sc / 2, sd + 3)
        return remap(img, x + st * fx_, y + st * fy_), {"seed": sd}

    @fx("frosted-glass", "APPX-100", "زجاج مصنفر", "frosted glass: random scatter within a radius", "amount=4 seed=1")
    def frosted_glass(img, p):
        """FrostedGlassEffect: MaxScatterRadius, MinScatterRadius, NumSamples"""
        np, cv2 = np_cv()
        x, y, w, h = grid(img)
        a, rng = num(p, "amount", 4), np.random.default_rng(int(num(p, "seed", 1)))
        mx = x + rng.uniform(-a, a, x.shape).astype(np.float32)
        my = y + rng.uniform(-a, a, y.shape).astype(np.float32)
        return cv2.remap(img, mx, my, cv2.INTER_NEAREST, borderMode=cv2.BORDER_REFLECT), {}

    @fx("tile-reflection", "APPX-100", "بلاط عاكس", "tile reflection: lens-distorted rotated tiles", "size=40 angle=30 curvature=1")
    def tile_reflection(img, p):
        """TileEffect: Rotation, SquareSize, Curvature"""
        np, _ = np_cv()
        x, y, w, h = grid(img)
        s, A, c = num(p, "size", 40), math.radians(num(p, "angle", 30)), num(p, "curvature", 1)
        cx, cy = w / 2, h / 2
        xr = math.cos(A) * (x - cx) + math.sin(A) * (y - cy)
        yr = -math.sin(A) * (x - cx) + math.cos(A) * (y - cy)
        tx, ty = np.floor(xr / s), np.floor(yr / s)
        u, v = (xr - (tx + .5) * s) / (s / 2), (yr - (ty + .5) * s) / (s / 2)
        lens = lambda q: np.sign(q) * np.abs(q) ** (1 + c) * (1 - 0.25 * c)   # each tile is its own lens: seams at edges
        u2, v2 = lens(u), lens(v)
        xr2, yr2 = (tx + .5) * s + u2 * s / 2, (ty + .5) * s + v2 * s / 2
        return remap(img, cx + math.cos(A) * xr2 - math.sin(A) * yr2, cy + math.sin(A) * xr2 + math.cos(A) * yr2), {}

    # ---- blurs
    def sharp(a):
        np, cv2 = np_cv()
        return float(cv2.Laplacian(cv2.cvtColor(a, cv2.COLOR_BGR2GRAY), cv2.CV_32F).var())

    def blur_ok(img, o):
        return {"sharpness_before": sharp(img), "sharpness_after": sharp(o), "_ok": sharp(o) < sharp(img)}

    @fx("zoom-blur", "APPX-101", "تغبيش تقريب", "zoom blur toward a centre", "amount=0.25 samples=16 cx cy")
    def zoom_blur(img, p):
        """ZoomBlurEffect: Amount, Offset"""
        np, cv2 = np_cv()
        h, w = img.shape[:2]
        cx, cy, a, n = num(p, "cx", .5) * w, num(p, "cy", .5) * h, num(p, "amount", .25), int(num(p, "samples", 16))
        acc = np.zeros(img.shape, np.float32)
        for k in range(n):
            M = cv2.getRotationMatrix2D((cx, cy), 0, 1 + a * k / max(1, n - 1))
            acc += cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REFLECT)
        o = (acc / n).astype(np.uint8)
        return o, blur_ok(img, o)

    @fx("radial-blur", "APPX-101", "تغبيش دوراني", "radial (spin) blur around a centre", "angle=12 samples=16 cx cy")
    def radial_blur(img, p):
        """RadialBlurEffect: Angle, Offset, Quality"""
        np, cv2 = np_cv()
        h, w = img.shape[:2]
        cx, cy, A, n = num(p, "cx", .5) * w, num(p, "cy", .5) * h, num(p, "angle", 12), int(num(p, "samples", 16))
        acc = np.zeros(img.shape, np.float32)
        for k in range(n):
            M = cv2.getRotationMatrix2D((cx, cy), -A / 2 + A * k / max(1, n - 1), 1)
            acc += cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REFLECT)
        o = (acc / n).astype(np.uint8)
        return o, blur_ok(img, o)

    @fx("motion-blur", "APPX-101", "تغبيش حركة", "directional motion blur", "angle=25 distance=20 centered=1")
    def motion_blur(img, p):
        """MotionBlurEffect: Angle, Distance, Centered"""
        np, cv2 = np_cv()
        d, A = max(1, int(num(p, "distance", 20))), math.radians(num(p, "angle", 25))
        size = 2 * d + 1
        k = np.zeros((size, size), np.float32)
        c = d
        start = -d if str(p.get("centered", "1")) != "0" else 0
        for t in np.linspace(start, d, 4 * d + 1):
            k[int(round(c + t * math.sin(A))), int(round(c + t * math.cos(A)))] = 1
        o = cv2.filter2D(img, -1, k / k.sum(), borderType=cv2.BORDER_REFLECT)
        return o, blur_ok(img, o)

    @fx("surface-blur", "APPX-101", "تنعيم السطح مع حفظ الحواف", "surface blur (edge-preserving)", "radius=6 threshold=40")
    def surface_blur(img, p):
        """SurfaceBlurEffect: Radius, Threshold"""
        _, cv2 = np_cv()
        r, t = int(num(p, "radius", 6)), num(p, "threshold", 40)
        o = cv2.bilateralFilter(img, 2 * r + 1, t * 2, r)
        return o, blur_ok(img, o)

    @fx("unfocus", "APPX-101", "عدم تركيز (قرصي)", "unfocus: disc (lens) blur", "radius=4")
    def unfocus(img, p):
        """UnfocusEffect: Radius"""
        np, cv2 = np_cv()
        r = max(1, int(num(p, "radius", 4)))
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1)).astype(np.float32)
        o = cv2.filter2D(img, -1, k / k.sum(), borderType=cv2.BORDER_REFLECT)
        return o, blur_ok(img, o)

    @fx("fragment", "APPX-101", "تشظّي (نسخ مزاحة)", "fragment: average of shifted copies", "fragments=4 distance=8 rotation=0")
    def fragment(img, p):
        """FragmentEffect: Fragments, Distance, Rotation"""
        np, cv2 = np_cv()
        h, w = img.shape[:2]
        n, d, rot = max(2, int(num(p, "fragments", 4))), num(p, "distance", 8), math.radians(num(p, "rotation", 0))
        acc = np.zeros(img.shape, np.float32)
        for k in range(n):
            t = rot + 2 * math.pi * k / n
            M = np.float32([[1, 0, d * math.cos(t)], [0, 1, d * math.sin(t)]])
            acc += cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REFLECT)
        return (acc / n).astype(np.uint8), {}

    @fx("median", "APPX-101", "وسيط (إزالة نقاط)", "median filter", "radius=3")
    def median(img, p):
        """MedianEffect: Radius, Percentile"""
        _, cv2 = np_cv()
        o = cv2.medianBlur(img, 2 * max(1, int(num(p, "radius", 3))) + 1)
        return o, {"local_std_before": local_std(img), "local_std_after": local_std(o), "_ok": local_std(o) < local_std(img)}

    # ---- stylize
    def directional(img, A, gray=True):
        np, cv2 = np_cv()
        src = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if gray else img
        s = src.astype(np.float32)
        return math.cos(A) * cv2.Sobel(s, cv2.CV_32F, 1, 0) + math.sin(A) * cv2.Sobel(s, cv2.CV_32F, 0, 1)

    @fx("emboss", "APPX-102", "نقش بارز رمادي", "emboss (grey relief at an angle)", "angle=45 strength=1")
    def emboss(img, p):
        """EmbossEffect: Angle"""
        np, cv2 = np_cv()
        e = (128 + directional(img, math.radians(num(p, "angle", 45))) * 0.5 * num(p, "strength", 1)).clip(0, 255)
        return cv2.cvtColor(e.astype(np.uint8), cv2.COLOR_GRAY2BGR), {}

    @fx("relief", "APPX-102", "نقش بارز ملوّن", "relief: colour image with embossed edges", "angle=45 strength=0.6")
    def relief(img, p):
        """ReliefEffect: Angle"""
        np, _ = np_cv()
        e = directional(img, math.radians(num(p, "angle", 45))) * 0.25 * num(p, "strength", 0.6)
        return (img.astype(np.float32) + e[..., None]).clip(0, 255).astype(np.uint8), {}

    @fx("edge-detect", "APPX-102", "كشف الحواف", "edge detect (Paint.NET-style grey relief of colour edges)", "angle=45")
    def edge_detect(img, p):
        """EdgeDetectEffect: Angle"""
        np, _ = np_cv()
        e = directional(img, math.radians(num(p, "angle", 45)), gray=False)
        return (128 + e * 0.5).clip(0, 255).astype(np.uint8), {}

    @fx("outline", "APPX-102", "تحديد بخط", "outline: thicken dark edges", "thickness=3 intensity=50")
    def outline(img, p):
        """OutlineEffect: Thickness, Intensity"""
        np, cv2 = np_cv()
        t, it = max(1, int(num(p, "thickness", 3))), num(p, "intensity", 50) / 100
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * t + 1, 2 * t + 1))
        er = cv2.erode(img, k)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        grad = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, k).astype(np.float32)
        a = (grad / (grad.max() + 1e-6) * (0.5 + it)).clip(0, 1)[..., None]
        return (img * (1 - a) + er * a).astype(np.uint8), {}

    @fx("pixelate", "APPX-102", "بكسلة", "pixelate into square cells", "cell=12")
    def pixelate(img, p):
        """PixelateEffect: CellSize"""
        np, cv2 = np_cv()
        c = max(2, int(num(p, "cell", 12)))
        h, w = img.shape[:2]
        small = cv2.resize(img, (max(1, w // c), max(1, h // c)), interpolation=cv2.INTER_AREA)
        big = cv2.resize(small, (small.shape[1] * c, small.shape[0] * c), interpolation=cv2.INTER_NEAREST)
        o = img.copy()
        o[:big.shape[0], :big.shape[1]] = big
        block = big[:c, :c].reshape(-1, 3)
        return o, {"cell": c, "_ok": bool((block == block[0]).all())}

    @fx("crystallize", "APPX-102", "بلورات (فورونوي)", "crystallize: Voronoi cells filled with their mean colour", "size=16 seed=1")
    def crystallize(img, p):
        """CrystalizeEffect: Size, Seed"""
        np, cv2 = np_cv()
        h, w = img.shape[:2]
        s, rng = max(3, int(num(p, "size", 16))), np.random.default_rng(int(num(p, "seed", 1)))
        ys, xs = np.mgrid[s // 2:h:s, s // 2:w:s]
        xs = (xs + rng.uniform(-s / 2.5, s / 2.5, xs.shape)).clip(0, w - 1).astype(int).ravel()
        ys = (ys + rng.uniform(-s / 2.5, s / 2.5, ys.shape)).clip(0, h - 1).astype(int).ravel()
        mask = np.ones((h, w), np.uint8)
        mask[ys, xs] = 0
        _, lab = cv2.distanceTransformWithLabels(mask, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
        lab = lab.ravel()
        n = lab.max() + 1
        cnt = np.bincount(lab, minlength=n).astype(np.float64)
        flat = img.reshape(-1, 3).astype(np.float64)
        means = np.stack([np.bincount(lab, flat[:, c], n) for c in range(3)], 1) / np.maximum(cnt, 1)[:, None]
        o = means[lab].reshape(img.shape).astype(np.uint8)
        cells = len(np.unique(o.reshape(-1, 3), axis=0))
        return o, {"seeds": int(len(xs)), "distinct_colours": cells, "_ok": cells <= len(xs)}

    @fx("glow", "APPX-102", "توهج", "glow: screen a blurred copy", "radius=6 brightness=10 contrast=10")
    def glow(img, p):
        """GlowEffect: Radius, Brightness, Contrast"""
        np, cv2 = np_cv()
        a = img.astype(np.float32) / 255
        b = cv2.GaussianBlur(a, (0, 0), max(1, num(p, "radius", 6)))
        b = ((b - .5) * (1 + num(p, "contrast", 10) / 100) + .5 + num(p, "brightness", 10) / 100).clip(0, 1)
        o = 1 - (1 - a) * (1 - b * 0.6)
        o = (o * 255).astype(np.uint8)
        return o, {"mean_before": float(img.mean()), "mean_after": float(o.mean()), "_ok": o.mean() > img.mean()}

    @fx("soften-portrait", "APPX-102", "تنعيم البورتريه", "soften portrait: smooth skin, lift light, warm", "softness=5 lighting=5 warmth=10")
    def soften_portrait(img, p):
        """SoftenPortraitEffect: Softness, Lighting, Warmth"""
        np, cv2 = np_cv()
        s = max(1, int(num(p, "softness", 5)))
        o = cv2.bilateralFilter(img, 2 * s + 1, 30 + 6 * s, s * 2).astype(np.float32)
        o += num(p, "lighting", 5) * 1.5
        wm = num(p, "warmth", 10) / 100 * 25
        o[..., 2] += wm
        o[..., 0] -= wm
        return o.clip(0, 255).astype(np.uint8), {}

    # ---- render
    def fractal(p, julia):
        np, cv2 = np_cv()
        W, H = int(num(p, "w", 800)), int(num(p, "h", 600))
        it, zoom, A = int(num(p, "iterations", 120)), num(p, "zoom", 1), math.radians(num(p, "angle", 0))
        y, x = np.mgrid[0:H, 0:W].astype(np.float64)
        s = 3.0 / (zoom * min(W, H))
        u, v = (x - W / 2) * s, (y - H / 2) * s
        u, v = u * math.cos(A) - v * math.sin(A), u * math.sin(A) + v * math.cos(A)
        if julia:
            z, c = u + 1j * v, complex(num(p, "cr", -0.8), num(p, "ci", 0.156))
        else:
            z, c = np.zeros_like(u, complex), (u - 0.6) + 1j * v
        n = np.zeros(z.shape, np.float64)
        alive = np.ones(z.shape, bool)
        for k in range(it):
            z[alive] = z[alive] ** 2 + (c if julia else c[alive])
            esc = alive & (np.abs(z) > 4)
            n[esc] = k + 1 - np.log2(np.log(np.abs(z[esc]) + 1e-9) + 1e-9)
            alive &= ~esc
        t = (n / it) ** 0.5
        hue = ((t * 360 * num(p, "factor", 1.5)) % 180).astype(np.uint8)
        hsv = np.dstack([hue, np.full_like(hue, 220), (np.where(alive, 0, 255 * np.clip(t * 3, 0, 1))).astype(np.uint8)])
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR), {"size": [W, H], "iterations": it, "inside_fraction": float(alive.mean())}

    for nm, jul, ar, en in (("julia", True, "كسيريات جوليا", "Julia set fractal"), ("mandelbrot", False, "كسيريات ماندلبروت", "Mandelbrot fractal")):
        def mk(julia=jul, name=nm):
            def run(inp, out, p):
                o, m = fractal(p, julia)
                return res(name, write(out, o), m, verified=0.0 < m["inside_fraction"] < 1.0 and float(o.std()) > 5)
            return run
        op(nm, f"{PDN}: {'Julia' if jul else 'Mandelbrot'}FractalEffect", "APPX-103", BASE, ar,
           f"{en} → PNG ; IN = - ; w h iterations zoom angle factor" + (" cr ci" if jul else ""))(mk())

    # ---- adjustments
    @fx("posterize", "APPX-104", "تقليل مستويات الألوان", "posterize to N levels per channel", "levels=6")
    def posterize(img, p):
        """PosterizeAdjustment: RedLevels, GreenLevels, BlueLevels, LinkLevels"""
        np, _ = np_cv()
        L = max(2, min(64, int(num(p, "levels", 6))))
        o = (np.round(img / 255 * (L - 1)) * (255 / (L - 1))).astype(np.uint8)
        u = max(len(np.unique(o[..., c])) for c in range(3))
        return o, {"levels": L, "max_distinct_per_channel": u, "_ok": u <= L}

    @fx("sepia", "APPX-104", "سيبيا", "sepia tone", "")
    def sepia(img, p):
        """SepiaEffect: none"""
        np, cv2 = np_cv()
        g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
        o = np.dstack([g * 0.78, g * 0.96, g * 1.12]).clip(0, 255).astype(np.uint8)
        ok = bool((o[..., 2] >= o[..., 1]).all() and (o[..., 1] >= o[..., 0]).all())
        return o, {"_ok": ok}

    @fx("invert", "APPX-104", "عكس الألوان", "invert colours", "")
    def invert(img, p):
        """InvertColorsEffect: none"""
        o = 255 - img
        return o, {"_ok": bool(((255 - o) == img).all())}

    @fx("auto-level", "APPX-104", "مستويات تلقائية", "auto level: per-channel 0.5–99.5 % stretch", "clip=0.5")
    def auto_level(img, p):
        """AutoLevelEffect: none"""
        np, _ = np_cv()
        c = num(p, "clip", 0.5)
        o = np.empty_like(img)
        for k in range(3):
            lo, hi = np.percentile(img[..., k], [c, 100 - c])
            o[..., k] = ((img[..., k].astype(np.float32) - lo) / max(1, hi - lo) * 255).clip(0, 255)
        return o, {"std_before": float(img.std()), "std_after": float(o.std()), "_ok": o.std() >= img.std() - 0.5}

    @fx("levels", "APPX-104", "المستويات (Levels)", "levels: input black/white, gamma, output black/white", "in_black=0 in_white=255 gamma=1 out_black=0 out_white=255")
    def levels(img, p):
        """LevelsEffect: input/output levels and gamma"""
        np, cv2 = np_cv()
        ib, iw, gm = num(p, "in_black", 0), num(p, "in_white", 255), num(p, "gamma", 1)
        ob, ow = num(p, "out_black", 0), num(p, "out_white", 255)
        x = np.arange(256, dtype=np.float32)
        t = ((x - ib) / max(1, iw - ib)).clip(0, 1) ** (1 / max(gm, 1e-3))
        lut = (ob + t * (ow - ob)).clip(0, 255).astype(np.uint8)
        o = cv2.LUT(img, lut)
        return o, {"lut_0": int(lut[0]), "lut_255": int(lut[255]), "_ok": int(lut[int(ib)]) == int(round(ob)) and int(lut[int(iw)]) == int(round(ow))}

    @fx("add-noise", "APPX-104", "إضافة ضوضاء/حبيبات", "add noise with intensity, colour saturation and coverage", "intensity=40 saturation=50 coverage=100 seed=1")
    def add_noise(img, p):
        """AddNoiseEffect: Intensity, Saturation, Coverage, Seed"""
        np, _ = np_cv()
        rng = np.random.default_rng(int(num(p, "seed", 1)))
        it, sat, cov = num(p, "intensity", 40), num(p, "saturation", 50) / 100, num(p, "coverage", 100) / 100
        lum = rng.normal(0, it / 2, img.shape[:2])[..., None]
        col = rng.normal(0, it / 2, img.shape)
        n = lum * (1 - sat) + col * sat
        n *= (rng.random(img.shape[:2]) < cov)[..., None]
        return (img + n).clip(0, 255).astype(np.uint8), {}

    # ============================================================== Photoshop: blend modes and layers (APPX-105)
    def lum(c):
        return 0.3 * c[..., 0] + 0.59 * c[..., 1] + 0.11 * c[..., 2]

    def clip_color(c):
        np, _ = np_cv()
        L = lum(c)[..., None]
        n, x = c.min(-1, keepdims=True), c.max(-1, keepdims=True)
        c = np.where(n < 0, L + (c - L) * L / np.maximum(L - n, 1e-6), c)
        return np.where(x > 1, L + (c - L) * (1 - L) / np.maximum(x - L, 1e-6), c)

    def set_lum(c, l):
        return clip_color(c + (l - lum(c))[..., None])

    def sat(c):
        return c.max(-1) - c.min(-1)

    def set_sat(c, s):
        np, _ = np_cv()
        mx, mn = c.max(-1, keepdims=True), c.min(-1, keepdims=True)
        rng = mx - mn
        return np.where(rng > 1e-6, (c - mn) * s[..., None] / np.maximum(rng, 1e-6), 0.0)

    def blend_rgb(cb, cs, mode):
        """W3C Compositing Level 1 blend functions on RGB floats in 0..1 (+ Photoshop's linear/vivid/pin/hard-mix)."""
        np, _ = np_cv()

        def dodge(b, s):
            return np.where(b <= 0, 0, np.where(s >= 1, 1, np.minimum(1, b / np.maximum(1 - s, 1e-6))))

        def burn(b, s):
            return np.where(b >= 1, 1, np.where(s <= 0, 0, 1 - np.minimum(1, (1 - b) / np.maximum(s, 1e-6))))

        def hard(b, s):
            return np.where(s <= .5, b * 2 * s, b + (2 * s - 1) - b * (2 * s - 1))

        def soft(b, s):
            d = np.where(b <= .25, ((16 * b - 12) * b + 4) * b, np.sqrt(b))
            return np.where(s <= .5, b - (1 - 2 * s) * b * (1 - b), b + (2 * s - 1) * (d - b))

        def vivid(b, s):
            return np.where(s <= .5, burn(b, 2 * s), dodge(b, 2 * (s - .5)))

        sep = {
            "normal": lambda b, s: s, "multiply": lambda b, s: b * s, "screen": lambda b, s: b + s - b * s,
            "overlay": lambda b, s: hard(s, b), "darken": np.minimum, "lighten": np.maximum,
            "color-dodge": dodge, "color-burn": burn, "hard-light": hard, "soft-light": soft,
            "difference": lambda b, s: np.abs(b - s), "exclusion": lambda b, s: b + s - 2 * b * s,
            "linear-burn": lambda b, s: np.maximum(0, b + s - 1), "linear-dodge": lambda b, s: np.minimum(1, b + s),
            "vivid-light": vivid, "linear-light": lambda b, s: np.clip(b + 2 * s - 1, 0, 1),
            "pin-light": lambda b, s: np.where(s <= .5, np.minimum(b, 2 * s), np.maximum(b, 2 * s - 1)),
            "hard-mix": lambda b, s: (vivid(b, s) >= .5).astype(b.dtype),
            "subtract": lambda b, s: np.maximum(0, b - s), "divide": lambda b, s: np.where(s <= 0, 1, np.minimum(1, b / np.maximum(s, 1e-6))),
        }
        if mode in sep:
            return np.clip(sep[mode](cb, cs), 0, 1)
        if mode == "hue":
            return set_lum(set_sat(cs, sat(cb)), lum(cb))
        if mode == "saturation":
            return set_lum(set_sat(cb, sat(cs)), lum(cb))
        if mode == "color":
            return set_lum(cs, lum(cb))
        if mode == "luminosity":
            return set_lum(cb, lum(cs))
        raise ValueError(f"unknown blend mode {mode!r}")

    MODES = ["normal", "multiply", "screen", "overlay", "darken", "lighten", "color-dodge", "color-burn", "hard-light",
             "soft-light", "difference", "exclusion", "linear-burn", "linear-dodge", "vivid-light", "linear-light",
             "pin-light", "hard-mix", "subtract", "divide", "hue", "saturation", "color", "luminosity"]
    NEUTRAL = {"multiply": 1.0, "screen": 0.0, "darken": 1.0, "lighten": 0.0, "linear-dodge": 0.0, "difference": 0.0,
               "exclusion": 0.0, "subtract": 0.0, "divide": 1.0, "overlay": 0.5, "soft-light": 0.5, "hard-light": 0.5,
               "linear-light": 0.5, "color-dodge": 0.0, "color-burn": 1.0, "linear-burn": 1.0, "vivid-light": 0.5}
    SELF = {"normal", "darken", "lighten", "pin-light", "hue", "saturation", "color", "luminosity"}   # B(c, c) == c

    def composite(base_rgb, top_rgb, top_a, mode, opacity):
        """Porter-Duff source-over with a blend function, opaque backdrop (RGB floats, alpha 0..1)."""
        a = (top_a * opacity)[..., None]
        return base_rgb * (1 - a) + blend_rgb(base_rgb, top_rgb, mode) * a

    def load_rgba(path, size=None):
        np, _ = np_cv()
        from PIL import Image
        im = Image.open(path).convert("RGBA")
        if size and im.size != tuple(size):
            im = im.resize(tuple(size), Image.LANCZOS)
        a = np.asarray(im).astype(np.float32) / 255
        return a[..., :3], a[..., 3]

    def save_rgb(path, rgb, alpha=None):
        np, _ = np_cv()
        from PIL import Image
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        arr = (np.clip(rgb, 0, 1) * 255 + .5).astype(np.uint8)
        if alpha is not None:
            arr = np.dstack([arr, (np.clip(alpha, 0, 1) * 255 + .5).astype(np.uint8)])
            Image.fromarray(arr, "RGBA").save(path)
        else:
            Image.fromarray(arr, "RGB").save(path)
        return str(path)

    @op("blend", PS + ": layer blend modes; Paint.NET BlendMode", "APPX-105", PIL, "دمج طبقتين بوضع مزج",
        "IN = base top ; mode=" + "|".join(MODES) + " ; opacity=1 ; x y offset of top")
    def blend(inp, out, p):
        np, _ = np_cv()
        mode = p.get("mode", "normal")
        cb, _ = load_rgba(inp[0])
        H, W = cb.shape[:2]
        ts, ta = load_rgba(inp[1])
        top, alpha = np.zeros_like(cb), np.zeros((H, W), np.float32)
        x, y = int(num(p, "x", 0)), int(num(p, "y", 0))
        h, w = min(ts.shape[0], H - y), min(ts.shape[1], W - x)
        top[y:y + h, x:x + w], alpha[y:y + h, x:x + w] = ts[:h, :w], ta[:h, :w]
        o = composite(cb, top, alpha, mode, num(p, "opacity", 1))
        m = {"mode": mode}
        ok = None
        if mode in NEUTRAL:   # measured postcondition: the neutral colour leaves the backdrop unchanged
            nt = blend_rgb(cb, np.full_like(cb, NEUTRAL[mode]), mode)
            m["neutral_max_error"] = float(np.abs(nt - cb).max())
            ok = m["neutral_max_error"] < 1e-4 or mode in ("color-dodge", "color-burn")
        elif mode in SELF:    # measured postcondition: blending an image onto itself returns it
            m["self_max_error"] = float(np.abs(blend_rgb(cb, cb, mode) - cb).max())
            ok = m["self_max_error"] < 1e-4
        return res("blend", save_rgb(out, o), m, verified=bool(ok))

    @op("layers", PS + " layers; " + MSP + " LayerStack/.paint", "APPX-105", PIL, "مشروع طبقات → PNG أو OpenRaster",
        "IN = layers.json {width,height,background:'#fff'|null,layers:[{name,image|color,x,y,opacity,mode,visible}]} → .png or .ora")
    def layers(inp, out, p):
        np, _ = np_cv()
        from PIL import Image
        spec_path = Path(inp[0])
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        W, H = int(spec["width"]), int(spec["height"])
        bg = spec.get("background", "#ffffff")
        base = np.zeros((H, W, 3), np.float32)
        base_a = np.zeros((H, W), np.float32)
        if bg:
            b, gg, r = hexcol(bg, (255, 255, 255))
            base[:], base_a[:] = (r / 255, gg / 255, b / 255), 1
        stack = []
        for i, L in enumerate(spec.get("layers", [])):
            rgb, a = np.zeros((H, W, 3), np.float32), np.zeros((H, W), np.float32)
            x, y = int(L.get("x", 0)), int(L.get("y", 0))
            if L.get("image"):
                ip = Path(L["image"])
                ip = ip if ip.is_absolute() else spec_path.parent / ip
                s, sa = load_rgba(ip, L.get("size"))
            else:
                b, gg, r = hexcol(L.get("color", "#000000"))
                lw, lh = L.get("size", [W, H])
                s = np.zeros((int(lh), int(lw), 3), np.float32) + (r / 255, gg / 255, b / 255)
                sa = np.ones((int(lh), int(lw)), np.float32)
            x0, y0 = max(0, x), max(0, y)
            x1, y1 = min(W, x + s.shape[1]), min(H, y + s.shape[0])
            if x1 > x0 and y1 > y0:
                rgb[y0:y1, x0:x1] = s[y0 - y:y1 - y, x0 - x:x1 - x]
                a[y0:y1, x0:x1] = sa[y0 - y:y1 - y, x0 - x:x1 - x]
            stack.append({"name": L.get("name", f"Layer {i + 1}"), "rgb": rgb, "a": a, "x": x, "y": y,
                          "opacity": float(L.get("opacity", 1)), "mode": L.get("mode", "normal"),
                          "visible": bool(L.get("visible", True))})
        merged, merged_a = base.copy(), base_a.copy()
        for L in stack:
            if L["visible"]:
                aa = L["a"] * L["opacity"]
                merged = composite(merged, L["rgb"], L["a"], L["mode"], L["opacity"])
                merged_a = merged_a + aa * (1 - merged_a)
        out = Path(out)
        if out.suffix.lower() != ".ora":
            return res("layers", save_rgb(out, merged, None if bg else merged_a), {"layers": len(stack)}, verified=True)
        # OpenRaster: mimetype first and stored, stack.xml top-first, PNG per layer, merged image and thumbnail
        import io
        from xml.sax.saxutils import quoteattr
        out.parent.mkdir(parents=True, exist_ok=True)
        ora_mode = {"normal": "svg:src-over", "multiply": "svg:multiply", "screen": "svg:screen", "overlay": "svg:overlay",
                    "darken": "svg:darken", "lighten": "svg:lighten", "color-dodge": "svg:color-dodge",
                    "color-burn": "svg:color-burn", "hard-light": "svg:hard-light", "soft-light": "svg:soft-light",
                    "difference": "svg:difference", "exclusion": "svg:exclusion", "hue": "svg:hue",
                    "saturation": "svg:saturation", "color": "svg:color", "luminosity": "svg:luminosity",
                    "linear-dodge": "svg:plus"}

        def png_bytes(rgb, a):
            arr = np.dstack([(np.clip(rgb, 0, 1) * 255 + .5).astype(np.uint8), (np.clip(a, 0, 1) * 255 + .5).astype(np.uint8)])
            bio = io.BytesIO()
            Image.fromarray(arr, "RGBA").save(bio, "PNG")
            return bio.getvalue()

        entries = ['<?xml version="1.0" encoding="UTF-8"?>', f'<image version="0.0.5" w="{W}" h="{H}">', "<stack>"]
        with zipfile.ZipFile(out, "w") as z:
            z.writestr(zipfile.ZipInfo("mimetype"), "image/openraster", compress_type=zipfile.ZIP_STORED)
            for i, L in reversed(list(enumerate(stack))):
                name = f"data/layer{i}.png"
                z.writestr(name, png_bytes(L["rgb"], L["a"]), compress_type=zipfile.ZIP_DEFLATED)
                entries.append(f'<layer name={quoteattr(L["name"])} src="{name}" x="0" y="0" opacity="{L["opacity"]:.3f}" '
                               f'visibility="{"visible" if L["visible"] else "hidden"}" composite-op="{ora_mode.get(L["mode"], "svg:src-over")}"/>')
            if bg:
                z.writestr("data/background.png", png_bytes(base, base_a), compress_type=zipfile.ZIP_DEFLATED)
                entries.append('<layer name="Background" src="data/background.png" x="0" y="0"/>')
            entries += ["</stack>", "</image>"]
            z.writestr("stack.xml", "\n".join(entries), compress_type=zipfile.ZIP_DEFLATED)
            z.writestr("mergedimage.png", png_bytes(merged, merged_a), compress_type=zipfile.ZIP_DEFLATED)
            thumb = Image.open(io.BytesIO(png_bytes(merged, merged_a)))
            thumb.thumbnail((256, 256))
            bio = io.BytesIO()
            thumb.save(bio, "PNG")
            z.writestr("Thumbnails/thumbnail.png", bio.getvalue(), compress_type=zipfile.ZIP_DEFLATED)
        with zipfile.ZipFile(out) as z:     # measured postcondition: valid OpenRaster container
            first = z.infolist()[0]
            n_layers = z.read("stack.xml").decode("utf-8").count("<layer ")
            ok = (first.filename == "mimetype" and first.compress_type == zipfile.ZIP_STORED
                  and z.read("mimetype") == b"image/openraster" and n_layers == len(stack) + (1 if bg else 0))
        return res("layers", str(out), {"layers": len(stack), "ora_layers": n_layers}, verified=ok)

    # ============================================================== Photoshop: 3D LUTs (APPX-106)
    def parse_cube(path):
        np, _ = np_cv()
        size, rows, dmin, dmax = None, [], [0, 0, 0], [1, 1, 1]
        for line in Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
            t = line.strip()
            if not t or t.startswith("#") or t.upper().startswith("TITLE"):
                continue
            up = t.upper()
            if up.startswith("LUT_3D_SIZE"):
                size = int(t.split()[1])
            elif up.startswith("LUT_1D_SIZE"):
                raise ValueError("1D LUTs are not supported; use a 3D .cube")
            elif up.startswith("DOMAIN_MIN"):
                dmin = [float(v) for v in t.split()[1:4]]
            elif up.startswith("DOMAIN_MAX"):
                dmax = [float(v) for v in t.split()[1:4]]
            elif t[0] in "-.0123456789":
                rows.append([float(v) for v in t.split()[:3]])
        if not size or len(rows) != size ** 3:
            raise ValueError(f"bad .cube: size {size}, {len(rows)} rows")
        # .cube order: red changes fastest → table[b, g, r]
        return np.asarray(rows, np.float32).reshape(size, size, size, 3), np.asarray(dmin), np.asarray(dmax)

    def apply_lut(rgb, table, dmin=None, dmax=None):
        """Trilinear lookup; rgb float 0..1 (…,3) RGB order, table[b,g,r] → RGB."""
        np, _ = np_cv()
        n = table.shape[0]
        if dmin is not None:
            rgb = (rgb - dmin) / np.maximum(dmax - dmin, 1e-6)
        x = np.clip(rgb, 0, 1) * (n - 1)
        i0 = np.floor(x).astype(int).clip(0, n - 2)
        fr = x - i0
        r0, g0, b0 = i0[..., 0], i0[..., 1], i0[..., 2]
        fr_, fg, fb = fr[..., 0:1], fr[..., 1:2], fr[..., 2:3]
        out = 0
        for db in (0, 1):
            for dg in (0, 1):
                for dr in (0, 1):
                    w = (fb if db else 1 - fb) * (fg if dg else 1 - fg) * (fr_ if dr else 1 - fr_)
                    out = out + w * table[b0 + db, g0 + dg, r0 + dr]
        return out

    def look_fn(name):
        np, _ = np_cv()

        def smooth(x):
            return x * x * (3 - 2 * x)

        def teal_orange(c):
            L = lum(c)[..., None]
            warm, teal = np.array([1.0, .62, .32]), np.array([.15, .45, .55])
            tint = teal * (1 - smooth(L)) + warm * smooth(L)
            return np.clip(c * 0.75 + tint * L * 0.35 + (c - L) * 0.15, 0, 1)

        def bleach(c):
            L = lum(c)[..., None]
            ov = np.where(L <= .5, 2 * c * L, 1 - 2 * (1 - c) * (1 - L))
            return np.clip(c * 0.4 + ov * 0.6, 0, 1)

        looks = {
            "identity": lambda c: c,
            "teal-orange": teal_orange,
            "bleach-bypass": bleach,
            "film-fade": lambda c: np.clip(0.08 + c * 0.86, 0, 1) ** 1.05,
            "warm": lambda c: np.clip(c * np.array([1.08, 1.0, 0.86]), 0, 1),
            "cool": lambda c: np.clip(c * np.array([0.9, 1.0, 1.1]), 0, 1),
            "noir": lambda c: np.repeat(smooth(np.clip(lum(c), 0, 1))[..., None], 3, -1),
            "cross-process": lambda c: np.clip(np.stack([smooth(c[..., 0]), c[..., 1] ** 0.85, c[..., 2] * 0.7 + 0.15], -1), 0, 1),
            "matrix-green": lambda c: np.clip(c * np.array([0.82, 1.06, 0.8]) + np.array([0, 0.02, 0]), 0, 1),
            "golden-hour": lambda c: np.clip(c ** np.array([0.9, 1.0, 1.15]) * np.array([1.05, 0.98, 0.85]), 0, 1),
        }
        if name not in looks:
            raise ValueError(f"look must be one of {sorted(looks)}")
        return looks[name]

    @op("lut-make", PS + ": Presets/3DLUTs (28 film looks)", "APPX-106", BASE, "صناعة LUT سينمائي (.cube)",
        "IN = - ; look=teal-orange|bleach-bypass|film-fade|warm|cool|noir|cross-process|matrix-green|golden-hour|identity ; size=33 → .cube")
    def lut_make(inp, out, p):
        np, _ = np_cv()
        look, n = p.get("look", "teal-orange"), int(num(p, "size", 33))
        fn = look_fn(look)
        b, gg, r = np.meshgrid(*(np.linspace(0, 1, n),) * 3, indexing="ij")
        table = fn(np.stack([r, gg, b], -1).astype(np.float64)).astype(np.float32)
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        lines = [f'TITLE "KOSIF {look}"', f"LUT_3D_SIZE {n}", "DOMAIN_MIN 0 0 0", "DOMAIN_MAX 1 1 1"]
        lines += [f"{v[0]:.6f} {v[1]:.6f} {v[2]:.6f}" for v in table.reshape(-1, 3)]
        Path(out).write_text("\n".join(lines) + "\n", encoding="utf-8")
        back, _, _ = parse_cube(out)    # measured: the file re-parses to the same table
        err = float(np.abs(back - table).max())
        return res("lut-make", str(out), {"look": look, "size": n, "roundtrip_max_error": err}, verified=err < 1e-5)

    @op("lut", PS + ": Color Lookup adjustment (.cube/3DLUTs)", "APPX-106", BASE, "تطبيق LUT على صورة",
        "cube=file.cube (any 3D .cube, e.g. from lut-make or a camera vendor) ; amount=1")
    def lut(inp, out, p):
        np, _ = np_cv()
        if not p.get("cube"):
            raise ValueError("--set cube=path/to/look.cube is required")
        table, dmin, dmax = parse_cube(p["cube"])
        img = read(inp[0])
        rgb = img[..., ::-1].astype(np.float32) / 255
        o = apply_lut(rgb, table, dmin, dmax)
        amt = num(p, "amount", 1)
        o = rgb * (1 - amt) + o * amt
        n = table.shape[0]   # measured: trilinear lookup reproduces the lattice exactly
        k = np.array([[0, 0, 0], [n - 1, n - 1, n - 1], [n // 2, 1, n - 2]])
        lat = apply_lut(k / (n - 1), table)
        exp = table[k[:, 2], k[:, 1], k[:, 0]]
        err = float(np.abs(lat - exp).max())
        return res("lut", write(out, (o[..., ::-1] * 255 + .5).clip(0, 255).astype(np.uint8)),
                   {"lut_size": n, "lattice_max_error": err, "mean_abs_change": float(np.abs(o - rgb).mean() * 255)},
                   verified=err < 1e-5)

    # ============================================================== Photoshop: sky replacement (APPX-107)
    SKIES = {"blue": ("#2f6fd6", "#bfe0ff"), "sunset": ("#2b1d5c", "#ffb36b"), "dusk": ("#0f1b3d", "#d2668a"),
             "golden": ("#5d8fd8", "#ffd58a"), "storm": ("#2a2f38", "#8a939e")}

    @op("sky-replace", PS + ": Edit › Sky Replacement (Sky_Presets)", "APPX-107", BASE, "استبدال السماء",
        "sky=blue|sunset|dusk|golden|storm or an image path ; feather=1.5 ; harmonize=0.25 ; show_mask=0")
    def sky_replace(inp, out, p):
        np, cv2 = np_cv()
        img = read(inp[0])
        h, w = img.shape[:2]
        f32 = img.astype(np.float32)
        b, gg, r = f32[..., 0], f32[..., 1], f32[..., 2]
        bright = (b + gg + r) / 3
        tex = np.abs(cv2.Laplacian(cv2.GaussianBlur(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), (5, 5), 0), cv2.CV_32F))
        tex = cv2.blur(tex, (9, 9))
        cand = (((b > r + 8) & (bright > 90)) | (bright > 200)) & (tex < 6)
        cand = cv2.morphologyEx(cand.astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
        n, lab = cv2.connectedComponents(cand)
        top = set(np.unique(lab[0][cand[0] > 0])) - {0}
        mask = np.isin(lab, list(top)).astype(np.uint8)
        # grow into sky-coloured pixels next to edges that the texture test excluded (geodesic dilation)
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).astype(np.float32)
        if mask.any():
            mu, sd = lab[mask > 0].mean(0), lab[mask > 0].std(0)
            colour = (np.abs(lab - mu) <= np.maximum(10, 2.5 * sd)).all(-1).astype(np.uint8)
        else:
            colour = mask
        k3 = np.ones((3, 3), np.uint8)
        for _ in range(64):
            grown = cv2.dilate(mask, k3) & colour
            if (grown == mask).all():
                break
            mask = grown
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
        fe = max(0.5, num(p, "feather", 1.5))
        a = cv2.GaussianBlur(mask.astype(np.float32), (0, 0), fe)[..., None]   # anti-aliased edge, no halo
        sky = p.get("sky", "sunset")
        if sky in SKIES:
            c1, c2 = (np.array(hexcol(c), np.float32) for c in SKIES[sky])
            ys = np.linspace(0, 1, h, dtype=np.float32)[:, None, None]
            yb = max(1, int(np.nonzero(mask.any(1))[0].max()) if mask.any() else h // 2)
            t = np.clip(np.linspace(0, 1, h)[:, None, None] * h / yb, 0, 1).astype(np.float32)
            sky_img = np.broadcast_to(c1 * (1 - t) + c2 * t, (h, w, 3)).astype(np.float32)
            del ys
        else:
            sky_img = cv2.resize(read(sky), (w, h), interpolation=cv2.INTER_AREA).astype(np.float32)
        hz = num(p, "harmonize", 0.25)
        fg_mean = f32[mask == 0].mean(0) if (mask == 0).any() else f32.mean((0, 1))
        sky_mean = sky_img[mask > 0].mean(0) if mask.any() else sky_img.mean((0, 1))
        fg = f32 * (1 - hz) + f32 * (sky_mean / np.maximum(fg_mean, 1)) * hz      # light the land with the new sky
        o = (fg * (1 - a) + sky_img * a).clip(0, 255).astype(np.uint8)
        if str(p.get("show_mask", "0")) == "1":
            o = (mask * 255).astype(np.uint8)
        frac = float(mask.mean())
        top_row = float(mask[0].mean())
        return res("sky-replace", write(out, o), {"sky_fraction": frac, "top_row_sky": top_row, "sky": sky},
                   verified=0.03 < frac < 0.9 and top_row > 0.5)

    # ============================================================== Photoshop: Liquify (APPX-108)
    @op("liquify", PS + ": Filters/Liquify.8bf", "APPX-108", BASE, "تسييل (دفع/قرص/نفخ/لف)",
        "mode=push|pinch|bloat|twirl ; cx cy (0..1) ; radius=0.2 ; strength=0.5 ; dx dy (push, px) ; or ops=liquify.json [{mode,cx,cy,…}]")
    def liquify(inp, out, p):
        np, _ = np_cv()
        img = read(inp[0])
        steps = json.loads(Path(p["ops"]).read_text(encoding="utf-8")) if p.get("ops") else [p]
        o = img
        for s in steps:
            x, y, w, h = grid(o)
            cx, cy = float(s.get("cx", .5)) * w, float(s.get("cy", .5)) * h
            R, k = float(s.get("radius", .2)) * min(w, h), float(s.get("strength", .5))
            dx, dy = x - cx, y - cy
            r = np.hypot(dx, dy)
            fall = np.where(r < R, (1 - (r / R) ** 2) ** 2, 0).astype(np.float32)
            mode = s.get("mode", "push")
            if mode == "push":
                mx, my = x - float(s.get("dx", 40)) * fall, y - float(s.get("dy", 0)) * fall
            elif mode in ("pinch", "bloat"):
                sc = 1 + (k if mode == "pinch" else -k) * fall
                mx, my = cx + dx * sc, cy + dy * sc
            elif mode == "twirl":
                t = k * math.pi * fall
                mx, my = cx + dx * np.cos(t) - dy * np.sin(t), cy + dx * np.sin(t) + dy * np.cos(t)
            else:
                raise ValueError("mode must be push|pinch|bloat|twirl")
            o = remap(o, mx, my)
        return res("liquify", write(out, o), {"steps": len(steps), "mean_abs_change": changed(img, o)})

    # ============================================================== Photoshop: Lens Blur with depth and bokeh (APPX-109)
    def aperture(r, blades, rot):
        np, cv2 = np_cv()
        r = max(1, int(r))
        k = np.zeros((2 * r + 1, 2 * r + 1), np.uint8)
        if blades < 3:
            cv2.circle(k, (r, r), r, 1, -1, cv2.LINE_AA)
        else:
            pts = [(r + r * math.cos(rot + 2 * math.pi * i / blades), r + r * math.sin(rot + 2 * math.pi * i / blades)) for i in range(blades)]
            cv2.fillConvexPoly(k, np.int32(np.round(pts)), 1, cv2.LINE_AA)
        k = k.astype(np.float32)
        return k / k.sum()

    @op("lens-blur", PS + ": Filters/Lens Blur.8bf + DepthPrediction", "APPX-109", BASE, "تغبيش عدسة بعمق وبوكيه",
        "depth=map.png (white = near) or auto (bottom = near) ; focus=0.8 (depth in focus) ; radius=14 ; blades=6 ; rotation=0 ; highlights=0.6 ; slices=8")
    def lens_blur(inp, out, p):
        np, cv2 = np_cv()
        img = read(inp[0])
        h, w = img.shape[:2]
        if p.get("depth") and p["depth"] != "auto":
            d = cv2.resize(cv2.cvtColor(read(p["depth"]), cv2.COLOR_BGR2GRAY), (w, h)).astype(np.float32) / 255
        else:
            d = np.repeat(np.linspace(0, 1, h, dtype=np.float32)[:, None], w, 1)
        focus, R, blades = num(p, "focus", .8), num(p, "radius", 14), int(num(p, "blades", 6))
        rot, hl, K = math.radians(num(p, "rotation", 0)), num(p, "highlights", .6), max(2, int(num(p, "slices", 8)))
        lin = (img.astype(np.float32) / 255) ** 2.2
        lum_ = lin.mean(-1, keepdims=True)
        lin = lin * (1 + 4 * hl * np.clip((lum_ - 0.7) / 0.3, 0, 1))      # bright points bloom into bokeh shapes
        acc, wsum = np.zeros_like(lin), np.zeros((h, w), np.float32)
        centers = np.linspace(0, 1, K)
        for c in centers:
            m = np.clip(1 - np.abs(d - c) * (K - 1), 0, 1)
            if not m.any():
                continue
            rad = R * abs(c - focus)
            if rad < 0.75:
                acc += lin * m[..., None]
                wsum += m
                continue
            k = aperture(rad, blades, rot)
            acc += cv2.filter2D(lin * m[..., None], -1, k, borderType=cv2.BORDER_REFLECT)
            wsum += cv2.filter2D(m, -1, k, borderType=cv2.BORDER_REFLECT)
        o = acc / np.maximum(wsum, 1e-6)[..., None]
        o = o / (1 + 4 * hl * np.clip((o.mean(-1, keepdims=True) - 0.7) / 0.3, 0, 1) * 0.5)
        o = (np.clip(o, 0, 1) ** (1 / 2.2) * 255 + .5).astype(np.float32)
        coc = R * np.abs(d - focus)                     # circle of confusion per pixel: keep the focal plane crisp
        wb = np.clip((coc - 0.5) / 1.5, 0, 1)[..., None]
        o = (img.astype(np.float32) * (1 - wb) + o * wb + .5).astype(np.uint8)
        infocus = np.abs(d - focus) < 0.1
        far = np.abs(d - focus) > 0.5

        def region_sharp(a, m):
            lap = cv2.Laplacian(cv2.cvtColor(a, cv2.COLOR_BGR2GRAY), cv2.CV_32F)
            return float(lap[m].var()) if m.any() else 0.0
        s_in = (region_sharp(img, infocus), region_sharp(o, infocus))
        s_far = (region_sharp(img, far), region_sharp(o, far))
        ok = s_far[0] > 0 and s_far[1] < 0.5 * s_far[0] and s_in[1] >= 0.6 * s_in[0]
        return res("lens-blur", write(out, o), {"focus_sharpness_before_after": s_in, "far_sharpness_before_after": s_far,
                                                "blades": blades}, verified=bool(ok))

    # ============================================================== MS Paint: brushes (APPX-110)
    BRUSHES = ["pencil", "brush", "calligraphy-45", "calligraphy-135", "airbrush", "oil", "crayon", "marker",
               "natural-pencil", "watercolor", "eraser"]

    def dense(points, step=1.0):
        np, _ = np_cv()
        pts = np.asarray(points, np.float32)
        if len(pts) == 1:
            return pts
        out = [pts[0]]
        for a, b in zip(pts[:-1], pts[1:]):
            n = max(1, int(np.hypot(*(b - a)) / step))
            out += [a + (b - a) * t for t in np.linspace(0, 1, n + 1)[1:]]
        return np.asarray(out)

    def stroke_mask(shape, s, rng):
        np, cv2 = np_cv()
        h, w = shape
        kind, size = s.get("brush", "brush"), float(s.get("size", 8))
        pts = dense(s["points"])
        ipts = np.int32(np.round(pts)).reshape(-1, 1, 2)
        m = np.zeros((h, w), np.float32)
        if kind == "pencil":
            mm = np.zeros((h, w), np.uint8)
            cv2.polylines(mm, [ipts], False, 255, max(1, int(size / 4)), cv2.LINE_8)
            return mm / 255.0, "normal"
        if kind in ("brush", "eraser", "watercolor", "marker", "crayon", "natural-pencil"):
            mm = np.zeros((h, w), np.uint8)
            th = max(1, int(size if kind != "natural-pencil" else max(1, size / 3)))
            if kind == "marker":
                for (x, y) in pts:        # chisel marker: flat square nib
                    cv2.rectangle(mm, (int(x - size / 2), int(y - size / 4)), (int(x + size / 2), int(y + size / 4)), 255, -1)
            else:
                cv2.polylines(mm, [ipts], False, 255, th, cv2.LINE_AA)
            m = mm / 255.0
            if kind == "crayon":       # wax skips the paper grain
                grain = smooth_field(h, w, 1.5, int(rng.integers(1 << 30)))
                m = m * (grain > -0.35) * 0.9
            elif kind == "natural-pencil":
                m = m * np.clip(0.55 + 0.25 * rng.standard_normal((h, w)), 0, 1)
            elif kind == "watercolor":
                soft = cv2.GaussianBlur(m, (0, 0), max(1, size / 5))
                rim = np.clip(soft - cv2.GaussianBlur(soft, (0, 0), max(1, size / 4)), 0, 1) * 2.5
                m = np.clip(soft * 0.35 + rim * 0.5, 0, 0.85)
            return m.astype(np.float32), ("multiply" if kind == "marker" else "erase" if kind == "eraser" else "normal")
        if kind in ("calligraphy-45", "calligraphy-135"):
            ang = math.radians(45 if kind.endswith("45") else 135)
            ux, uy = math.cos(ang) * size / 2, -math.sin(ang) * size / 2
            mm = np.zeros((h, w), np.uint8)
            for a, b in zip(pts[:-1], pts[1:]):
                quad = np.int32(np.round([a + (ux, uy), a - (ux, uy), b - (ux, uy), b + (ux, uy)]))
                cv2.fillConvexPoly(mm, quad, 255, cv2.LINE_AA)
            return mm / 255.0, "normal"
        if kind == "airbrush":
            mm = np.zeros((h, w), np.float32)
            for (x, y) in pts[::2]:
                dots = rng.normal(0, size / 2.5, (int(max(4, size)), 2)) + (x, y)
                ok = (dots[:, 0] >= 0) & (dots[:, 0] < w) & (dots[:, 1] >= 0) & (dots[:, 1] < h)
                d = dots[ok].astype(int)
                mm[d[:, 1], d[:, 0]] += 0.35
            return np.clip(mm, 0, 1), "normal"
        if kind == "oil":
            nb = max(3, int(size / 2))
            mm = np.zeros((h, w), np.float32)
            tang = np.gradient(pts, axis=0)
            nrm = np.stack([-tang[:, 1], tang[:, 0]], 1)
            nrm /= np.maximum(np.linalg.norm(nrm, axis=1, keepdims=True), 1e-6)
            for i in range(nb):
                off = (i / (nb - 1) - .5) * size
                bp = pts + nrm * off + rng.normal(0, 0.3, pts.shape)
                layer = np.zeros((h, w), np.uint8)
                cv2.polylines(layer, [np.int32(np.round(bp)).reshape(-1, 1, 2)], False, 255, 2, cv2.LINE_AA)
                mm = np.maximum(mm, layer / 255.0 * float(rng.uniform(0.55, 1.0)))
            return mm, "normal"
        raise ValueError(f"brush must be one of {BRUSHES}")

    @op("paint", MSP + ": Brush/Calligraphic/AirBrush/Pencil/Eraser tools", "APPX-110", BASE, "رسم بفرش الرسّام",
        "IN = strokes.json {width,height,background:'#fff' | image, strokes:[{brush:" + "|".join(BRUSHES) + ",color,size,opacity,points:[[x,y],…]}]}")
    def paint(inp, out, p):
        np, cv2 = np_cv()
        spec_path = Path(inp[0])
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        if spec.get("image"):
            ip = Path(spec["image"])
            canvas = read(ip if ip.is_absolute() else spec_path.parent / ip).astype(np.float32)
        else:
            canvas = np.zeros((int(spec["height"]), int(spec["width"]), 3), np.float32) + hexcol(spec.get("background", "#ffffff"), (255, 255, 255))
        paper = canvas.copy()
        rng = np.random.default_rng(int(spec.get("seed", 7)))
        report = []
        for s in spec.get("strokes", []):
            m, how = stroke_mask(canvas.shape[:2], s, rng)
            a = (m * float(s.get("opacity", 1)))[..., None]
            col = np.array(hexcol(s.get("color", "#000000")), np.float32)
            if s.get("brush") == "oil":
                col = col * float(rng.uniform(0.92, 1.08))
            before = canvas.copy()
            if how == "multiply":
                canvas = canvas * (1 - a) + canvas * (col / 255) * a
            elif how == "erase":
                canvas = canvas * (1 - a) + paper * a
            else:
                canvas = canvas * (1 - a) + col * a
            report.append({"brush": s.get("brush", "brush"), "coverage_px": int((np.abs(canvas - before).sum(-1) > 3).sum())})
        o = canvas.clip(0, 255).astype(np.uint8)
        ok = bool(report) and all(r["coverage_px"] > 0 or r["brush"] == "eraser" for r in report)
        return res("paint", write(out, o), {"strokes": report}, verified=ok)

    # ============================================================== MS Paint / Paint.NET: bucket fill (APPX-111)
    @op("fill", MSP + ": FloodFillOperation; Paint.NET Paint Bucket", "APPX-111", BASE, "سطل التعبئة",
        "x y (px) ; color=#ff0000 ; tolerance=10 (0..100) ; mode=contiguous|global")
    def fill(inp, out, p):
        np, cv2 = np_cv()
        img = read(inp[0])
        h, w = img.shape[:2]
        x, y = int(num(p, "x", w // 2)), int(num(p, "y", h // 2))
        col = hexcol(p.get("color", "#ff0000"), (0, 0, 255))
        t = int(num(p, "tolerance", 10) / 100 * 255)
        o = img.copy()
        if p.get("mode") == "global":
            seed = img[y, x].astype(np.int16)
            sel = (np.abs(img.astype(np.int16) - seed).max(-1) <= t)
            o[sel] = col
            area = int(sel.sum())
        else:
            mask = np.zeros((h + 2, w + 2), np.uint8)
            area, *_ = cv2.floodFill(o, mask, (x, y), col, (t,) * 3, (t,) * 3, 4 | cv2.FLOODFILL_FIXED_RANGE | (255 << 8))
        ok = tuple(int(v) for v in o[y, x]) == tuple(col) and area > 0
        return res("fill", write(out, o), {"filled_px": int(area), "seed": [x, y]}, verified=ok)

    # ============================================================== MS Paint: Coloring Book (APPX-112)
    @op("coloring-book", MSP + ": AIFeature.ColoringBook", "APPX-112", BASE, "صفحة تلوين من صورة",
        "lines=2 (thickness) ; detail=7 (lower = more lines) ; min_area=40 (speck cleanup)")
    def coloring_book(inp, out, p):
        np, cv2 = np_cv()
        img = read(inp[0])
        g = cv2.cvtColor(cv2.bilateralFilter(img, 9, 60, 7), cv2.COLOR_BGR2GRAY)
        g = cv2.medianBlur(g, 5)
        th = cv2.adaptiveThreshold(g, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, int(num(p, "detail", 7)))
        ed = cv2.Canny(g, 40, 120)
        ink = ((th == 0) | (ed > 0)).astype(np.uint8)
        n, lab, stats, _ = cv2.connectedComponentsWithStats(ink, connectivity=8)
        keep = np.zeros(n, bool)
        keep[1:] = stats[1:, cv2.CC_STAT_AREA] >= int(num(p, "min_area", 40))
        ink = keep[lab].astype(np.uint8)
        t = max(1, int(num(p, "lines", 2)))
        ink = cv2.dilate(ink, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (t, t)))
        o = np.where(ink[..., None] > 0, 0, 255).astype(np.uint8).repeat(3, 2)
        white = float((o[..., 0] == 255).mean())
        binary = bool(np.isin(np.unique(o), [0, 255]).all())
        return res("coloring-book", write(out, o), {"white_fraction": white, "binary": binary}, verified=binary and white > 0.55)

    # ============================================================== MS Paint: stickers (APPX-113)
    @op("sticker", MSP + ": AIFeature.StickerGenerator, Remove background", "APPX-113", PIL, "ملصق بحد أبيض وظل",
        "IN = PNG with transparency (or any image: background removed first with remove-bg box=…) ; border=12 ; shadow=0.35")
    def sticker(inp, out, p):
        np, cv2 = np_cv()
        from PIL import Image
        im = Image.open(inp[0]).convert("RGBA")
        arr = np.asarray(im).astype(np.float32) / 255
        if arr[..., 3].min() > 0.99:          # opaque input: cut the subject out first
            tmp = Path(out).with_name(Path(out).stem + "_cutout.png")
            g["OPS"]["remove-bg"]["fn"]([inp[0]], str(tmp), {k: v for k, v in p.items() if k in ("box", "feather")})
            arr = np.asarray(Image.open(tmp).convert("RGBA")).astype(np.float32) / 255
            tmp.unlink(missing_ok=True)
        bd, sh = max(1, int(num(p, "border", 12))), num(p, "shadow", 0.35)
        pad = bd * 3
        h, w = arr.shape[:2]
        big = np.zeros((h + 2 * pad, w + 2 * pad, 4), np.float32)
        big[pad:pad + h, pad:pad + w] = arr
        a = big[..., 3]
        ring = cv2.dilate((a > 0.5).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * bd + 1,) * 2)).astype(np.float32)
        ring = cv2.GaussianBlur(ring, (3, 3), 0)
        shadow = cv2.GaussianBlur(ring, (0, 0), bd / 1.5)
        M = np.float32([[1, 0, bd / 3], [0, 1, bd / 2]])
        shadow = cv2.warpAffine(shadow, M, (shadow.shape[1], shadow.shape[0])) * sh
        rgb = np.zeros(big.shape[:2] + (3,), np.float32)
        alpha = shadow.copy()
        rgb = rgb * (1 - ring[..., None]) + 1.0 * ring[..., None]
        alpha = ring + alpha * (1 - ring)
        rgb = rgb * (1 - a[..., None]) + big[..., :3] * a[..., None]
        alpha = a + alpha * (1 - a)
        o = np.dstack([np.clip(rgb, 0, 1), np.clip(alpha, 0, 1)])
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        Image.fromarray((o * 255 + .5).astype(np.uint8), "RGBA").save(out)
        border_px = (ring > 0.999) & (cv2.dilate(a, np.ones((3, 3), np.uint8)) < 0.01)
        ok = bool(border_px.any()) and float(o[border_px][:, :3].min()) > 0.95 and float(o[0, 0, 3]) < 0.05
        return res("sticker", str(out), {"border_px": int(border_px.sum()), "size": [o.shape[1], o.shape[0]]}, verified=ok)

    return {"effects": sorted(FX), "blend_modes": MODES, "brushes": BRUSHES}
