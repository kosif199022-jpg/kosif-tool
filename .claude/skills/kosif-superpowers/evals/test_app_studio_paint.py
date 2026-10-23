"""The painting batch of app_studio.py (scripts/app_studio_paint.py: Paint.NET effects, Photoshop blend modes, layers,
LUTs, sky replacement, liquify and lens blur, MS Paint brushes, fill, coloring book and stickers) run on synthetic files in
a folder with an Arabic name, each with a measured postcondition. Proof behind APPX-99…APPX-113."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

try:
    import numpy as np
    import cv2
    MISSING_EXTRAS = None
except ImportError as exc:  # optional extras: pip install numpy opencv-python-headless pillow
    np = cv2 = None
    MISSING_EXTRAS = str(exc)


def setUpModule():
    # a skip raised here (not at import time) keeps `python3 evals/<this file>` and `-m unittest <file>` at exit 0
    if MISSING_EXTRAS:
        raise unittest.SkipTest(f"App Studio tests need numpy and opencv-python-headless ({MISSING_EXTRAS})")


PATH = Path(__file__).resolve().parents[1] / "scripts" / "app_studio.py"
spec = importlib.util.spec_from_file_location("app_studio_paint_test", PATH)
st = importlib.util.module_from_spec(spec)
spec.loader.exec_module(st)  # stdlib-only at import time; numpy/cv2 load inside the operations


def scene(w=320, h=240, seed=3):
    rng = np.random.default_rng(seed)
    img = np.zeros((h, w, 3), np.uint8)
    for y in range(h // 2):
        img[y] = (235, 170 + y // 4, 120 + y // 3)
    img[h // 2:] = (60, 130, 70)
    for k in range(5):
        cv2.rectangle(img, (10 + k * 62, 60 + k * 7), (50 + k * 62, h // 2 + 30), (40, 60 + k * 30, 200 - k * 30), -1)
        for wy in range(70 + k * 7, h // 2 + 20, 14):
            cv2.rectangle(img, (16 + k * 62, wy), (26 + k * 62, wy + 6), (200, 240, 250), -1)
    return cv2.add(img, rng.integers(0, 6, img.shape, dtype=np.uint8))


class PaintBatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.d = Path(cls.tmp.name) / "رسم واختبار"
        cls.d.mkdir()
        cls.img = scene()
        cls.src = cls.d / "مدينة.png"
        st.write(cls.src, cls.img)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def run_op(self, name, inputs, out, **params):
        r = st.OPS[name]["fn"]([str(x) for x in inputs], str(self.d / out), {k: str(v) for k, v in params.items()})
        self.assertEqual(r["op"], name)
        self.assertTrue(Path(r["output"]).exists(), name)
        return r

    def test_registered(self):
        for name in st.PAINT_BATCH["effects"] + ["julia", "mandelbrot", "blend", "layers", "lut", "lut-make", "sky-replace",
                                                  "liquify", "lens-blur", "paint", "fill", "coloring-book", "sticker"]:
            self.assertIn(name, st.OPS)
        self.assertGreaterEqual(len(st.PAINT_BATCH["effects"]), 30)

    def test_every_effect_runs_and_changes_the_image(self):
        for name in st.PAINT_BATCH["effects"]:
            with self.subTest(effect=name):
                r = self.run_op(name, [self.src], f"{name}.png")
                o = st.read(r["output"])
                self.assertEqual(o.shape, self.img.shape)
                if name != "levels":   # default levels is the identity on purpose
                    self.assertGreater(r["metrics"]["mean_abs_change"], 0.5, name)

    def test_measured_effects(self):
        for name in ["oil-paint", "pencil-sketch", "twist", "bulge", "zoom-blur", "radial-blur", "motion-blur",
                     "surface-blur", "unfocus", "median", "pixelate", "crystallize", "glow", "posterize", "sepia",
                     "invert", "auto-level"]:
            with self.subTest(effect=name):
                self.assertTrue(self.run_op(name, [self.src], f"m_{name}.png")["verified"], name)
        r = self.run_op("posterize", [self.src], "post3.png", levels=3)
        self.assertLessEqual(r["metrics"]["max_distinct_per_channel"], 3)
        r = self.run_op("levels", [self.src], "lev.png", in_black=40, in_white=200, out_black=10, out_white=240)
        self.assertTrue(r["verified"])
        self.assertEqual((r["metrics"]["lut_0"], r["metrics"]["lut_255"]), (10, 240))

    def test_fractals(self):
        for name in ("julia", "mandelbrot"):
            r = self.run_op(name, ["-"], f"{name}.png", w=200, h=150, iterations=50)
            self.assertTrue(r["verified"])
            self.assertEqual(st.read(r["output"]).shape[:2], (150, 200))

    def test_blend_modes(self):
        top = self.d / "top.png"
        t = np.zeros_like(self.img)
        cv2.circle(t, (160, 120), 80, (40, 90, 220), -1)
        st.write(top, t)
        for mode in st.PAINT_BATCH["blend_modes"]:
            with self.subTest(mode=mode):
                r = self.run_op("blend", [self.src, top], f"blend_{mode}.png", mode=mode)
                if mode != "hard-mix":
                    self.assertTrue(r["verified"], mode)
        # multiply with white is the identity, screen with black is the identity
        white = self.d / "white.png"
        st.write(white, np.full_like(self.img, 255))
        o = st.read(self.run_op("blend", [self.src, white], "mul_white.png", mode="multiply")["output"])
        self.assertLessEqual(int(np.abs(o.astype(int) - self.img.astype(int)).max()), 1)

    def test_layers_png_and_openraster(self):
        top = self.d / "top.png"
        if not top.exists():
            st.write(top, np.zeros_like(self.img))
        spec_ = {"width": 320, "height": 240, "background": "#ffffff", "layers": [
            {"name": "صورة", "image": "مدينة.png"}, {"name": "دائرة", "image": "top.png", "mode": "screen", "opacity": 0.6},
            {"name": "شريط", "color": "#ffcc00", "size": [320, 40], "y": 200, "mode": "multiply"},
            {"name": "مخفي", "color": "#000000", "visible": False}]}
        (self.d / "stack.json").write_text(json.dumps(spec_, ensure_ascii=False), encoding="utf-8")
        r = self.run_op("layers", [self.d / "stack.json"], "art.ora")
        self.assertTrue(r["verified"])
        with zipfile.ZipFile(r["output"]) as z:
            self.assertEqual(z.infolist()[0].filename, "mimetype")
            xml = z.read("stack.xml").decode("utf-8")
            self.assertIn('visibility="hidden"', xml)
            self.assertIn("svg:screen", xml)
            self.assertIn("mergedimage.png", z.namelist())
        png = st.read(self.run_op("layers", [self.d / "stack.json"], "art.png")["output"])
        self.assertEqual(png.shape, self.img.shape)

    def test_luts(self):
        r = self.run_op("lut-make", ["-"], "id.cube", look="identity", size=17)
        self.assertTrue(r["verified"])
        o = st.read(self.run_op("lut", [self.src], "id.png", cube=self.d / "id.cube")["output"])
        self.assertLessEqual(int(np.abs(o.astype(int) - self.img.astype(int)).max()), 1)
        for look in ("teal-orange", "bleach-bypass", "noir", "golden-hour"):
            self.assertTrue(self.run_op("lut-make", ["-"], f"{look}.cube", look=look, size=17)["verified"])
            r = self.run_op("lut", [self.src], f"{look}.png", cube=self.d / f"{look}.cube")
            self.assertTrue(r["verified"])
            self.assertGreater(r["metrics"]["mean_abs_change"], 2)
        noir = st.read(self.d / "noir.png")
        self.assertLessEqual(int(np.abs(noir[..., 0].astype(int) - noir[..., 2].astype(int)).max()), 2)

    def test_sky_replace(self):
        r = self.run_op("sky-replace", [self.src], "sky.png", sky="sunset")
        self.assertTrue(r["verified"])
        self.assertGreater(r["metrics"]["sky_fraction"], 0.25)
        self.assertLess(r["metrics"]["sky_fraction"], 0.6)
        o = st.read(r["output"])
        self.assertLess(float(np.abs(o[200:].astype(int) - self.img[200:].astype(int)).mean()), 25)   # land kept

    def test_liquify_and_lens_blur(self):
        r = self.run_op("liquify", [self.src], "liq.png", mode="bloat", strength=0.6)
        self.assertGreater(r["metrics"]["mean_abs_change"], 0.5)
        r = self.run_op("lens-blur", [self.src], "lens.png", focus=0.9, radius=10, blades=6)
        self.assertTrue(r["verified"])

    def test_paint_brushes(self):
        strokes = [{"brush": b, "color": "#1f5fd1", "size": 12, "points": [[20, 20 + 25 * i], [300, 25 + 25 * i]]}
                   for i, b in enumerate(st.PAINT_BATCH["brushes"]) if b != "eraser"]
        strokes.append({"brush": "eraser", "size": 20, "points": [[160, 0], [160, 300]]})
        (self.d / "strokes.json").write_text(json.dumps({"width": 320, "height": 300, "background": "#ffffff",
                                                          "strokes": strokes}), encoding="utf-8")
        r = self.run_op("paint", [self.d / "strokes.json"], "brushes.png")
        self.assertTrue(r["verified"])
        o = st.read(r["output"])
        self.assertTrue((o[:, 158:162] > 245).all())   # the eraser restored the paper

    def test_fill(self):
        r = self.run_op("fill", [self.src], "fill.png", x=5, y=200, color="#ff00ff", tolerance=12)
        self.assertTrue(r["verified"])
        o = st.read(r["output"])
        self.assertEqual(tuple(int(v) for v in o[5, 5]), tuple(int(v) for v in self.img[5, 5]))   # sky untouched

    def test_coloring_book_and_sticker(self):
        r = self.run_op("coloring-book", [self.src], "color.png")
        self.assertTrue(r["verified"])
        r = self.run_op("sticker", [self.src], "sticker.png", box="10,50,300,110", border=10)
        self.assertTrue(r["verified"])
        from PIL import Image
        self.assertEqual(Image.open(r["output"]).mode, "RGBA")


if __name__ == "__main__":
    unittest.main()
