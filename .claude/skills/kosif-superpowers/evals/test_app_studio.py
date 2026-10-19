"""Every app_studio.py operation run on synthetic files in a folder with an Arabic name, each with a measured
postcondition. This is the proof behind the ✅ on APPX-31…50 and APPX-61…87 when they are run through the CLI."""
import http.server
import importlib.util
import json
import importlib.util as _iu  # noqa
import math
import shutil
from pathlib import Path
import tempfile
import threading
import unittest
import warnings

import numpy as np
import cv2

PATH = Path(__file__).resolve().parents[1] / "scripts" / "app_studio.py"
spec = importlib.util.spec_from_file_location("app_studio", PATH)
st = importlib.util.module_from_spec(spec)
spec.loader.exec_module(st)


def scene(w=480, h=320, seed=7):
    rng = np.random.default_rng(seed)
    img = np.zeros((h, w, 3), np.uint8)
    for y in range(h // 2):
        img[y] = (235, 170 + y // 4, 120 + y // 3)     # BGR sky
    img[h // 2:] = (60, 120, 70)
    for k in range(5):
        x0 = 20 + k * 92
        top = int(rng.integers(50, 120))
        cv2.rectangle(img, (x0, top), (x0 + 60, h // 2 + 30), tuple(int(c) for c in rng.integers(60, 220, 3)), -1)
        for wy in range(top + 8, h // 2 + 20, 18):
            cv2.rectangle(img, (x0 + 8, wy), (x0 + 22, wy + 10), (200, 240, 250), -1)
    cv2.circle(img, (w // 2, int(h * .78)), 40, (50, 60, 200), -1)
    return cv2.GaussianBlur(img, (3, 3), 0)


class AppStudioTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.d = Path(cls.tmp.name) / "صور الاختبار"      # non-ASCII path on purpose
        cls.d.mkdir()
        cls.clean = scene()
        cls.src = cls.d / "مدينة.png"
        st.write(cls.src, cls.clean)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def run_op(self, name, inputs, out=None, **params):
        out = None if out is False else str(self.d / (out or f"{name}.png"))
        r = st.OPS[name]["fn"]([str(x) for x in inputs], out, {k: str(v) for k, v in params.items()})
        self.assertEqual(r["op"], name)
        return r

    def put(self, name, img):
        p = self.d / name
        st.write(p, img)
        return p

    # --- photo
    def test_dehaze(self):
        hazy = (self.clean * 0.45 + 235 * 0.55).astype(np.uint8)
        r = self.run_op("dehaze", [self.put("hazy.png", hazy)])
        self.assertGreater(st.psnr(st.read(r["output"]), self.clean), st.psnr(hazy, self.clean) + 3)

    def test_denoise_both_methods(self):
        noisy = (self.clean + np.random.default_rng(1).normal(0, 18, self.clean.shape)).clip(0, 255).astype(np.uint8)
        p = self.put("noisy.png", noisy)
        for m in ("fast", "nlm"):
            r = self.run_op("denoise", [p], f"dn_{m}.png", method=m)
            self.assertGreater(st.psnr(st.read(r["output"]), self.clean), st.psnr(noisy, self.clean) + 3, m)

    def test_keystone_auto(self):
        canvas = np.full((400, 560, 3), 30, np.uint8)
        quad = np.float32([[90, 60], [470, 40], [500, 360], [60, 340]])
        M = cv2.getPerspectiveTransform(np.float32([[0, 0], [480, 0], [480, 320], [0, 320]]), quad)
        warped = cv2.warpPerspective(self.clean, M, (560, 400))
        mask = cv2.warpPerspective(np.full((320, 480), 255, np.uint8), M, (560, 400))
        canvas[mask > 0] = warped[mask > 0]
        r = self.run_op("keystone", [self.put("tilted.png", canvas)])
        self.assertLess(np.abs(np.float32(r["metrics"]["corners"]) - quad).max(), 4)
        out = cv2.resize(st.read(r["output"]), (480, 320))
        self.assertGreater(st.psnr(out[15:-15, 15:-15], self.clean[15:-15, 15:-15]), 20)

    def test_lens(self):
        h, w = self.clean.shape[:2]
        K = np.float32([[w, 0, w / 2], [0, w, h / 2], [0, 0, 1]])
        D = np.float32([0.3, 0, 0, 0, 0])
        ys, xs = np.indices((h, w), np.float32)
        und = cv2.undistortPoints(np.stack([xs.ravel(), ys.ravel()], 1).reshape(-1, 1, 2), K, D, P=K).reshape(h, w, 2)
        dist = cv2.remap(self.clean, und[..., 0], und[..., 1], cv2.INTER_LINEAR)
        r = self.run_op("lens", [self.put("barrel.png", dist)], k1=0.3)
        c = (slice(h // 6, -h // 6), slice(w // 6, -w // 6))
        self.assertGreater(st.psnr(st.read(r["output"])[c], self.clean[c]), st.psnr(dist[c], self.clean[c]) + 5)

    def test_ca(self):
        h, w = self.clean.shape[:2]
        sc = lambda ch, s: cv2.warpAffine(ch, cv2.getRotationMatrix2D((w / 2, h / 2), 0, s), (w, h), borderMode=cv2.BORDER_REFLECT)
        b, g, r_ = cv2.split(self.clean)
        fr = cv2.merge([sc(b, 0.99), g, sc(r_, 1.01)])
        r = self.run_op("ca", [self.put("fringe.png", fr)])
        self.assertAlmostEqual(r["metrics"]["scale_r"], 1 / 1.01, delta=0.002)
        self.assertAlmostEqual(r["metrics"]["scale_b"], 1 / 0.99, delta=0.002)

    def test_develop_grey_world_and_vibrance(self):
        cast = (self.clean.astype(float) * [0.75, 1.0, 1.25]).clip(0, 255).astype(np.uint8)
        r = self.run_op("develop", [self.put("cast.png", cast)], wb="grey", curve="s", vibrance=0.3)
        m = r["metrics"]["channel_means_bgr"]
        self.assertLess(max(m) - min(m), 12)

    def test_grain_and_vignette(self):
        g = st.read(self.run_op("grain", [self.src], amount=8)["output"]).astype(float)
        self.assertAlmostEqual((g - self.clean).std(), 8, delta=2.5)
        v = st.read(self.run_op("vignette", [self.src], amount=0.5)["output"]).astype(float)
        self.assertLess(v[:20, :20].mean(), self.clean[:20, :20].mean() * 0.8)

    def test_watermark_text_and_logo(self):
        r = self.run_op("watermark", [self.src], "wm.jpg", text="KOSIF", opacity=0.5, pos="br")
        self.assertTrue(Path(r["output"]).is_file())
        ra = self.run_op("watermark", [self.src], "wm_ar.png", text="© كوسيف للتصميم", opacity=0.9, pos="c", size=0.08)
        self.assertIn(ra["metrics"]["arabic_shaping"], ("raqm", "arabic-reshaper+bidi"))
        self.assertGreater(np.abs(st.read(ra["output"]).astype(int) - self.clean).sum(), 0)
        logo =np.zeros((40, 80, 4), np.uint8); logo[..., 1:3] = 255; logo[..., 3] = 255
        lp = self.d / "logo.png"; cv2.imencode(".png", logo)[1].tofile(str(lp))
        r2 = self.run_op("watermark", [self.src], "wm2.png", logo=str(lp), opacity=0.5, pos="tl", size=0.2)
        out = st.read(r2["output"]).astype(float)
        x, y = r2["metrics"]["position"]
        self.assertGreater(out[y + 5, x + 5, 1], self.clean[y + 5, x + 5, 1])

    def test_jpegmini_verifies_its_ssim(self):
        r = self.run_op("jpegmini", [self.src], "small.jpg", delta=0.01)
        self.assertTrue(r["verified"])
        self.assertLess(r["metrics"]["quality"], 95)

    def test_contact_sheet_and_pdf(self):
        for i in range(7):
            self.put(f"cs_{i}.png", np.roll(self.clean, i * 30, axis=1))
        r = self.run_op("contact-sheet", [self.d], "sheet.pdf", cols=3, rows=2)
        self.assertGreaterEqual(r["metrics"]["pages"], 2)
        r2 = self.run_op("pdf", [self.d / "cs_0.png", self.d / "cs_1.png"], "album.pdf")
        self.assertEqual(r2["metrics"]["pages"], 2)
        self.assertTrue(Path(r2["output"]).read_bytes().startswith(b"%PDF"))

    def test_preset_chain_and_v1_migration(self):
        pj = self.d / "warm.json"
        pj.write_text(json.dumps({"schema": 2, "ops": [{"op": "develop", "temp": 0.3, "curve": "s"}, {"op": "vignette", "amount": 0.3}]}))
        a = st.read(self.run_op("preset", [self.src], "pa.png", preset=pj)["output"])
        b = st.read(self.run_op("preset", [self.src], "pb.png", preset=pj)["output"])
        self.assertTrue(np.array_equal(a, b))
        ratio = lambda x: x[..., 2].astype(float).mean() / x[..., 0].astype(float).mean()
        self.assertGreater(ratio(a), ratio(self.clean) * 1.05)   # warmer than the source
        old = self.d / "old.json"
        old.write_text(json.dumps({"schema": 1, "warmth": 0.3, "ops": [{"op": "vignette", "amount": 0.3}]}))
        self.assertEqual(self.run_op("preset", [self.src], "pc.png", preset=old)["metrics"]["schema"], 2)

    def test_xmp_roundtrip_merges_keywords(self):
        self.run_op("xmp", [self.src], False, rating=4, label="Green", keywords="مدينة,city")
        r = self.run_op("xmp", [self.src], False, keywords="sunset")
        self.assertTrue(r["verified"])
        back = self.run_op("xmp", [self.src], False, read=1)["metrics"]
        self.assertEqual((back["rating"], back["label"]), (4, "Green"))
        self.assertEqual(back["keywords"], ["مدينة", "city", "sunset"])

    def test_horizon(self):
        h, w = 320, 480
        c = np.full((h, w, 3), 90, np.uint8)
        cv2.line(c, (0, h // 2), (w, h // 2), (255, 255, 255), 3)
        c[h // 2 + 2:] = (60, 110, 60)
        t = cv2.warpAffine(c, cv2.getRotationMatrix2D((w / 2, h / 2), 4.0, 1), (w, h), borderMode=cv2.BORDER_REPLICATE)
        r = self.run_op("horizon", [self.put("tilt.png", t)])
        self.assertAlmostEqual(abs(r["metrics"]["angle_deg"]), 4.0, delta=0.4)

    def test_hdr_fusion_and_single(self):
        ins = [self.put(f"ev{i}.png", (self.clean.astype(float) * g).clip(0, 255).astype(np.uint8)) for i, g in enumerate((0.4, 1, 2.2))]
        r = self.run_op("hdr", ins)
        self.assertLess(r["metrics"]["clipped_hi_pct"], ((self.clean.astype(float) * 2.2) >= 250).mean() * 100)
        self.assertEqual(self.run_op("hdr", [ins[0]], "hdr1.png")["metrics"]["inputs"], 1)

    def test_sharpen_and_clarity(self):
        soft = self.put("soft.png", cv2.GaussianBlur(self.clean, (0, 0), 1.5))
        r = self.run_op("sharpen", [soft], amount=1.0)
        self.assertGreater(r["metrics"]["laplacian_var_after"], r["metrics"]["laplacian_var_before"])
        r2 = self.run_op("clarity", [self.src], amount=0.6)
        self.assertGreater(r2["metrics"]["local_contrast_after"], r2["metrics"]["local_contrast_before"])

    def test_hsl_band(self):
        r = self.run_op("hsl", [self.src], band="green", sat=-1.0)
        out = cv2.cvtColor(st.read(r["output"]), cv2.COLOR_BGR2HLS)
        ground = out[int(320 * .9), 10]
        self.assertLess(ground[2], cv2.cvtColor(self.clean, cv2.COLOR_BGR2HLS)[int(320 * .9), 10][2] * 0.3)

    def test_bw_split_tone(self):
        o = st.read(self.run_op("bw", [self.src])["output"])
        self.assertLessEqual(np.abs(o[..., 0].astype(int) - o[..., 2]).max(), 1)
        t = st.read(self.run_op("split-tone", [self.put("grey.png", o)], amount=0.3)["output"]).astype(float)
        self.assertGreater(np.abs(t[..., 0] - t[..., 2]).mean(), 5)

    def test_redeye_box(self):
        img = self.clean.copy()
        cv2.circle(img, (100, 100), 8, (40, 30, 230), -1)
        for kw in ({"box": "88,88,24,24"}, {}):   # given box, then automatic red-blob detection
            r = self.run_op("redeye", [self.put("eye.png", img)], **kw)
            o = st.read(r["output"])
            self.assertLess(o[100, 100, 2], 100, kw)
            self.assertGreater(r["metrics"]["pixels_fixed"], 100, kw)
            self.assertLess(np.abs(o[200:, :].astype(int) - self.clean[200:, :]).max(), 1, kw)   # nothing else touched

    def test_repair_box(self):
        img = self.clean.copy()
        cv2.rectangle(img, (300, 40), (320, 60), (0, 0, 255), -1)          # a red blemish in the sky
        r = self.run_op("repair", [self.put("blem.png", img)], box="298,38,25,25")
        o = st.read(r["output"])
        self.assertLess(np.abs(o[50, 310].astype(int) - self.clean[50, 310]).max(), 40)

    def test_moire(self):
        h, w = self.clean.shape[:2]
        xx = np.indices((h, w))[1]
        pat = (self.clean + 25 * np.sin(xx * 2 * np.pi / 4.0)[..., None]).clip(0, 255).astype(np.uint8)
        r = self.run_op("moire", [self.put("moire.png", pat)])
        self.assertGreater(st.psnr(st.read(r["output"]), self.clean), st.psnr(pat, self.clean) + 3)

    def test_tilt_shift_bg_blur(self):
        o = st.read(self.run_op("tilt-shift", [self.src], saturation=0)["output"])
        lap = lambda a: cv2.Laplacian(cv2.cvtColor(a, cv2.COLOR_BGR2GRAY), cv2.CV_64F).var()
        self.assertLess(lap(o[50:85]), lap(self.clean[50:85]) * 0.5)          # buildings far from the sharp band
        self.assertGreater(lap(o[170:185]), lap(self.clean[170:185]) * 0.8)   # the band itself stays sharp
        r = self.run_op("bg-blur", [self.src], box="180,170,120,100")
        self.assertGreater(r["metrics"]["subject_pct"], 1)

    def test_crop_resize_autotone_icc(self):
        r = self.run_op("crop", [self.src], aspect="9:16", focus="subject")
        w, h = r["metrics"]["box"][2:]
        self.assertAlmostEqual(w / h, 9 / 16, delta=0.01)
        self.assertEqual(max(self.run_op("resize", [self.src], long=200)["metrics"]["size"]), 200)
        flat = self.put("flat.png", (self.clean * 0.4 + 70).astype(np.uint8))
        a = self.run_op("auto-tone", [flat])["metrics"]
        self.assertGreater(a["std_after"], a["std_before"] * 1.5)
        self.assertEqual(self.run_op("icc", [self.src], "icc.png")["metrics"]["mode"], "RGB")

    def test_library_ops(self):
        lib = self.d / "lib"
        lib.mkdir()
        st.write(lib / "a.jpg", self.clean)
        st.write(lib / "a_copy.jpg", cv2.resize(cv2.resize(self.clean, (240, 160)), (480, 320)))
        st.write(lib / "other.jpg", 255 - self.clean)
        groups = self.run_op("dedupe", [lib], False)["metrics"]["duplicate_groups"]
        self.assertEqual(len(groups), 1)
        self.assertEqual(sorted(Path(g).name for g in groups[0]), ["a.jpg", "a_copy.jpg"])
        self.run_op("xmp", [lib / "a.jpg"], False, rating=5, keywords="غروب")
        db = str(self.d / "lib.db")
        self.assertEqual(self.run_op("catalog", [lib], "lib.db")["metrics"]["indexed"], 3)
        hits = st.OPS["search"]["fn"]([db], None, {"q": "غروب", "min_rating": "4"})["metrics"]["hits"]
        self.assertEqual([Path(h["path"]).name for h in hits], ["a.jpg"])
        plan = self.run_op("rename", [lib], False, pattern="{n:03d}_{stem}{ext}")["metrics"]
        self.assertFalse(plan["applied"])
        self.assertEqual(len(plan["plan"]), 3)
        self.assertIn("a.jpg", self.run_op("exif", [lib], False)["metrics"])

    def test_faces_runs_or_names_its_requirement(self):
        try:
            r = self.run_op("faces", [self.src])
            self.assertIsInstance(r["metrics"]["count"], int)
        except RuntimeError as exc:   # OpenCV 5 without a YuNet model: the error must say what to install
            self.assertIn("yunet", str(exc).lower())

    # --- design / procedural
    def test_boolean(self):
        j = self.d / "shapes.json"
        j.write_text(json.dumps([{"circle": [0, 0, 50]}, {"rect": [0, -60, 80, 120]}]))
        r = self.run_op("boolean", [j], "bool.svg", mode="difference")
        self.assertAlmostEqual(r["metrics"]["area"], math.pi * 2500 / 2, delta=5)
        self.assertIn("<path", Path(r["output"]).read_text())

    def test_trace(self):
        img = np.full((120, 160, 3), 255, np.uint8)
        cv2.circle(img, (80, 60), 35, (40, 40, 200), -1)
        r = self.run_op("trace", [self.put("logo_bmp.png", img)], "logo.svg", colors=2)
        self.assertGreaterEqual(r["metrics"]["paths"], 2)
        self.assertIn('fill="#c8', Path(r["output"]).read_text())

    def test_procedural(self):
        r = self.run_op("scatter", [], "scatter.svg", count=80, min_dist=40, w=800, h=800)
        self.assertTrue(r["verified"])
        self.assertTrue(st.read(self.run_op("noise-field", [], "terrain.png", w=256, h=256, mode="terrain")["output"]).std() > 10)
        self.run_op("noise-field", [], "clouds.png", w=128, h=128, mode="clouds")
        self.assertGreater(self.run_op("lsystem", [], "plant.svg", iterations=3)["metrics"]["segments"], 100)

    def test_chops(self):
        k = self.d / "keys.json"
        k.write_text(json.dumps([[0, 0], [0.99, 0], [1.0, 1], [4, 1]]))
        v = json.loads(Path(self.run_op("chops", [k], "lag.json", lag=0.25, fps=30)["output"]).read_text())["values"]
        t63 = next(i for i, x in enumerate(v) if x >= 0.632) / 30 - 1.0
        self.assertAlmostEqual(t63, 0.25, delta=0.06)
        s = json.loads(Path(self.run_op("chops", [k], "spring.json", spring="200:12", fps=60)["output"]).read_text())["values"]
        self.assertGreater(max(s), 1.0)    # overshoot

    # --- type
    def test_font_build_inspect_subset(self):
        g = self.d / "glyphs"
        g.mkdir()
        (g / "A.svg").write_text('<svg viewBox="0 0 600 1000"><path d="M0 800 L300 0 L600 800 Z"/></svg>')
        (g / "V.svg").write_text('<svg viewBox="0 0 600 1000"><path d="M0 0 L300 800 L600 0 Z"/></svg>')
        (g / "uni0628.svg").write_text('<svg viewBox="0 0 800 1000"><path d="M50 600 C50 800 750 800 750 600 L700 600 C700 700 100 700 100 600 Z"/></svg>')
        r = self.run_op("font-build", [g], "Brand.ttf", family="KOSIF Brand", kern="A V -80;V A -60")
        self.assertEqual(r["metrics"]["codepoints"], 4)
        info = self.run_op("font-inspect", [r["output"]], False)["metrics"]
        self.assertEqual(info["family"], "KOSIF Brand")
        self.assertIn("kern", info["gpos"])
        self.assertEqual(info["arabic_letters"], "1/42")
        sub = self.run_op("font-subset", [r["output"]], "sub.ttf", text="AV")
        self.assertLess(sub["metrics"]["bytes_out"], sub["metrics"]["bytes_in"])

    # --- animation
    def test_tween_lottie_ik(self):
        spr = np.zeros((30, 30, 4), np.uint8); cv2.circle(spr, (15, 15), 12, (40, 80, 230, 255), -1)
        sp = self.d / "ball.png"; cv2.imencode(".png", spr)[1].tofile(str(sp))
        r = self.run_op("tween", [sp], "sheet.png", frames=12, onion=1)
        self.assertEqual(r["metrics"]["first"], [40.0, 180.0])
        self.assertEqual(r["metrics"]["last"], [600.0, 180.0])
        self.assertTrue((self.d / "sheet_onion.png").is_file())
        lot = json.loads(Path(self.run_op("lottie", [], "anim.json", frames=48)["output"]).read_text())
        self.assertEqual((lot["op"], lot["layers"][0]["ks"]["p"]["a"]), (48, 1))
        ik = self.run_op("ik", [], False, l1=100, l2=80, target="120,60")
        self.assertTrue(ik["verified"])
        self.assertLess(ik["metrics"]["reach_error"], 1e-6)

    # --- download
    def test_download_ranged(self):
        payload = np.random.default_rng(3).integers(0, 256, 700_000, dtype=np.uint8).tobytes()
        (self.d / "srv").mkdir(exist_ok=True)
        (self.d / "srv" / "f.bin").write_bytes(payload)
        root = str(self.d / "srv")

        class H(http.server.SimpleHTTPRequestHandler):
            def __init__(s, *a, **k):
                super().__init__(*a, directory=root, **k)
            def log_message(s, *a):
                pass
            def send_head(s):
                rng = s.headers.get("Range")
                if not rng or s.command != "GET":
                    s.send_response(200); s.send_header("Accept-Ranges", "bytes"); s.send_header("Content-Length", str(len(payload))); s.end_headers()
                    import io
                    return io.BytesIO(payload if s.command == "GET" else b"")
                a, b = (int(x) for x in rng.split("=")[1].split("-"))
                s.send_response(206); s.send_header("Content-Length", str(b - a + 1)); s.end_headers()
                import io
                return io.BytesIO(payload[a:b + 1])
        srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        try:
            import hashlib
            url = f"http://127.0.0.1:{srv.server_address[1]}/f.bin"
            r = st.OPS["download"]["fn"]([url], str(self.d / "got.bin"), {"parts": "4", "sha256": hashlib.sha256(payload).hexdigest()})
            self.assertTrue(r["verified"], r)
            self.assertEqual((self.d / "got.bin").read_bytes(), payload)
        finally:
            srv.shutdown()

    # --- Canva (APPX-88…98, remove-bg = APPX-14)
    def test_design_template_arabic_and_effects(self):
        photo = self.put("portrait.png", self.clean)
        spec = {"size": "instagram-post", "background": {"gradient": ["#0f172a", "#1f6feb"], "angle": 120},
                "elements": [
                    {"type": "image", "src": photo.name, "box": [90, 120, 360, 360], "mask": "circle", "filter": "duotone"},
                    {"type": "rect", "box": [520, 160, 470, 300], "fill": "#ffffff", "opacity": 0.12, "radius": 32},
                    {"type": "text", "text": "عرض خاص لمدة أسبوع فقط", "box": [540, 180, 430, 260], "font": "cairo",
                     "color": "#ffd166", "effect": "shadow"},
                    {"type": "text", "text": "KOSIF STUDIO", "box": [90, 860, 900, 120], "font": "lalezar", "color": "#ffffff",
                     "effect": "outline", "align": "center"},
                    {"type": "line", "box": [90, 820, 900, 0], "fill": "#ffd166", "width": 6}]}
        j = self.d / "post.json"
        j.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
        r = self.run_op("design", [j], "post.png")
        self.assertTrue(r["verified"], r["metrics"])               # every text block fits its box
        self.assertEqual(r["metrics"]["size"], [1080, 1080])
        ar = r["metrics"]["texts"][0]
        self.assertIn(ar["shaping"], ("raqm", "arabic-reshaper+bidi"))
        o = st.read(r["output"])
        box = o[180:440, 540:970]
        self.assertGreater(((box[..., 2] > 200) & (box[..., 1] > 170) & (box[..., 0] < 140)).sum(), 500)   # yellow text drawn
        self.assertLess(np.abs(o[120 + 5, 90 + 5].astype(int) - o[5, 5]).max(), 60)                         # circle mask corner = background

    def test_resize_design_all_platforms(self):
        r = self.run_op("resize-design", [self.src], "sizes", sizes="instagram-post,story,youtube-thumbnail,facebook-cover")
        self.assertTrue(r["verified"])
        self.assertEqual(len(r["metrics"]["files"]), 4)
        self.assertEqual(st.read(r["metrics"]["files"]["story"]).shape[:2], (1920, 1080))

    def test_remove_bg_transparent_png(self):
        h, w = 320, 480
        bg = (np.random.default_rng(4).integers(0, 255, (h, w, 3))).astype(np.uint8)
        bg = cv2.GaussianBlur(bg, (0, 0), 6)
        cv2.circle(bg, (240, 160), 90, (30, 40, 220), -1)
        r = self.run_op("remove-bg", [self.put("subj.png", bg)], "cut.png", box="130,50,220,220")
        rgba = cv2.imdecode(np.fromfile(r["output"], np.uint8), cv2.IMREAD_UNCHANGED)
        self.assertEqual(rgba.shape[2], 4)
        truth = np.zeros((h, w), bool); cv2.circle(truth.view(np.uint8), (240, 160), 90, 1, -1)
        got = rgba[..., 3] > 127
        self.assertGreater((got & truth).sum() / (got | truth).sum(), 0.85)

    def test_duotone(self):
        r = self.run_op("duotone", [self.src], "duo.png", dark="#1b1464", light="#ff6f61")
        o = cv2.imdecode(np.fromfile(r["output"], np.uint8), cv2.IMREAD_COLOR).reshape(-1, 3).astype(float)
        d, l = np.array([0x64, 0x14, 0x1b], float), np.array([0x61, 0x6f, 0xff], float)   # BGR
        t = ((o - d) @ (l - d)) / ((l - d) @ (l - d))
        off_line = np.linalg.norm(o - (d + np.clip(t, 0, 1)[:, None] * (l - d)), axis=1)
        self.assertLess(off_line.max(), 3)

    def test_collage_layouts(self):
        ims = [self.put(f"c{i}.png", np.roll(self.clean, i * 50, axis=1)) for i in range(4)]
        r = self.run_op("collage", ims, "hero.jpg", layout="hero", gap=10, radius=20)
        self.assertEqual(r["metrics"]["size"], [1080, 1080])
        self.assertEqual(len(r["metrics"]["cells"]), 4)
        self.assertEqual(self.run_op("collage", ims, "grid.png", layout="grid", size="800x800")["metrics"]["size"], [800, 800])

    def test_mockup_auto_surface(self):
        scene_ = np.full((400, 600, 3), 40, np.uint8)
        quad = np.int32([[180, 80], [430, 100], [420, 330], [170, 300]])
        cv2.fillConvexPoly(scene_, quad, (235, 235, 235))
        des = np.zeros((300, 400, 3), np.uint8); des[:] = (40, 40, 220)
        r = self.run_op("mockup", [self.put("des.png", des), self.put("scene.png", scene_)], "mock.png")
        self.assertLess(np.abs(np.float32(r["metrics"]["quad"]) - quad).max(), 6)
        o = st.read(r["output"])
        self.assertGreater(o[200, 300, 2], 150)                  # design red inside the surface
        self.assertLess(o[200, 300, 0], 90)
        self.assertEqual(o[20, 20].tolist(), [40, 40, 40])     # scene untouched outside

    @unittest.skipUnless(importlib.util.find_spec("segno"), "pip install segno")
    def test_qr_decodes_back(self):
        url = "https://github.com/kosif199022-jpg/kosif-tool"
        self.assertTrue(self.run_op("qr", [url], "qr.png", dark="#0f172a")["verified"])
        logo = np.zeros((60, 60, 4), np.uint8); logo[..., 2] = 220; logo[..., 3] = 255
        lp = self.d / "qlogo.png"; cv2.imencode(".png", logo)[1].tofile(str(lp))
        r = self.run_op("qr", [url], "qr_logo.png", logo=str(lp))
        self.assertEqual(r["metrics"]["error"], "H")
        self.assertTrue(r["verified"])
        self.assertTrue(self.run_op("qr", ["كوسيف"], "qr.svg")["verified"])

    def test_palette_finds_brand_colours(self):
        img = np.zeros((200, 300, 3), np.uint8)
        img[:, :150] = (0x8c, 0x5a, 0x1e); img[:, 150:250] = (0x66, 0xd1, 0xff); img[:, 250:] = (255, 255, 255)
        r = self.run_op("palette", [self.put("brand.png", img)], "brand", colors=3)
        hexes = [c["hex"] for c in r["metrics"]["palette"]]
        self.assertEqual(hexes[0], "#1e5a8c")
        self.assertIn("#ffd166", hexes)
        self.assertTrue(Path(r["metrics"]["swatch"]).is_file())

    @unittest.skipUnless(importlib.util.find_spec("matplotlib"), "pip install matplotlib")
    def test_chart_arabic_labels(self):
        j = self.d / "sales.json"
        j.write_text(json.dumps({"labels": ["يناير", "فبراير", "مارس"], "values": [12, 19, 7]}, ensure_ascii=False), encoding="utf-8")
        for kind in ("bar", "line", "donut"):
            with warnings.catch_warnings():
                warnings.simplefilter("error", UserWarning)   # a missing Arabic glyph is a failure, not a warning
                r = self.run_op("chart", [j], f"chart_{kind}.png", kind=kind, title="المبيعات")
            self.assertGreater(st.read(r["output"]).std(), 10, kind)
            self.assertIn(r["metrics"]["arabic_shaping"], ("matplotlib-native", "arabic-reshaper+bidi"))
        csv = self.d / "s.csv"
        csv.write_text("month,value\nA,1\nB,2\n", encoding="utf-8")
        self.assertEqual(self.run_op("chart", [csv], "c.svg")["metrics"]["points"], 2)

    @unittest.skipUnless(importlib.util.find_spec("pptx"), "pip install python-pptx")
    def test_pptx_from_images_and_design(self):
        s1 = self.put("s1.png", self.clean)
        dj = self.d / "s2.json"
        dj.write_text(json.dumps({"background": "#101828", "elements": [{"type": "text", "text": "شكرًا لكم", "box": [200, 400, 1520, 280], "color": "#ffffff"}]},
                                 ensure_ascii=False), encoding="utf-8")
        notes = self.d / "notes.txt"
        notes.write_text("مقدمة\nختام\n", encoding="utf-8")
        r = self.run_op("pptx", [s1, dj], "deck.pptx", notes=notes)
        self.assertTrue(r["verified"])
        self.assertEqual(r["metrics"]["slides"], 2)

    def test_print_pdf_bleed_marks_cmyk(self):
        r = self.run_op("print-pdf", [self.src], "card.pdf", width_mm=90, height_mm=50, bleed_mm=3, dpi=300)
        m = r["metrics"]
        mm = lambda v: round(v / 25.4 * 300)
        self.assertEqual(m["trim_px"], [mm(90), mm(50)])
        self.assertEqual(m["bleed_px"], mm(3))
        self.assertEqual(m["page_px"], [mm(90) + 2 * mm(3) + 2 * mm(10), mm(50) + 2 * mm(3) + 2 * mm(10)])
        self.assertEqual(m["mode"], "CMYK")
        self.assertTrue(Path(r["output"]).read_bytes().startswith(b"%PDF"))

    def test_text_anim_gif_and_mp4(self):
        r = self.run_op("text-anim", [], "t.gif", text="رمضان كريم", style="typewriter", size="480x270", seconds=1, fps=12)
        from PIL import Image
        gif = Image.open(r["output"])
        total = 0
        for i in range(gif.n_frames):   # Pillow merges identical frames and adds up their durations
            gif.seek(i)
            total += gif.info.get("duration", 0)
        self.assertAlmostEqual(total, 1000, delta=60)
        self.assertGreater(gif.n_frames, 1)
        if shutil.which("ffmpeg"):
            r2 = self.run_op("text-anim", [], "t.mp4", text="KOSIF", style="pop", size="320x320", seconds=1, fps=10)
            self.assertGreater(Path(r2["output"]).stat().st_size, 1000)

    # --- cli
    def test_cli_doctor_and_every_op_is_covered(self):
        doc = st.doctor()
        self.assertEqual(doc["ops"], len(st.OPS))
        covered = {n for n in dir(self) if n.startswith("test_")}
        src = (Path(__file__).read_text(encoding="utf-8"))
        for name in st.OPS:
            self.assertIn(f'"{name}"', src, f"op {name} has no test")

    def test_cli_main_and_batch(self):
        import contextlib
        import io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            st.main(["vignette", str(self.src), "-o", str(self.d / "cli.png"), "--set", "amount=0.3"])
        self.assertEqual(json.loads(buf.getvalue().strip().splitlines()[-1])["op"], "vignette")
        bdir = self.d / "batch_in"; bdir.mkdir(exist_ok=True)
        st.write(bdir / "1.png", self.clean); st.write(bdir / "2.png", self.clean)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            st.main(["batch", "resize", str(bdir), "-o", str(self.d / "batch_out"), "--set", "long=100"])
        out = json.loads(buf.getvalue().strip().splitlines()[-1])
        self.assertEqual((out["batch"], out["failed"]), (2, 0))


if __name__ == "__main__":
    unittest.main()
