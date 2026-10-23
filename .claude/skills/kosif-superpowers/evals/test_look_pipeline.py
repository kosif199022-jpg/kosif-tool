"""Look pipeline: one set of numbers for ffmpeg, SVG and GLSL; measured ffmpeg parity on a test frame."""
import shutil, subprocess, sys, tempfile, unittest
import xml.etree.ElementTree as ET
from pathlib import Path
SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import look_pipeline as L  # noqa: E402

HAVE = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))


class LookMathTests(unittest.TestCase):
    def test_natural_is_identity(self):
        c = L.pipeline(L.params_for("natural"))
        self.assertEqual(L._is_identity(c), (True, True))
        self.assertEqual(L.to_ffmpeg(c), "format=rgb24")
        self.assertEqual(L.apply_pixel(c, [10, 128, 250]), [10, 128, 250])

    def test_mono_is_grey_and_amount_scales(self):
        c = L.pipeline(L.params_for("mono"))
        r, g, b = L.apply_pixel(c, [220, 40, 40])
        self.assertTrue(abs(r - g) <= 1 and abs(g - b) <= 1)
        half = L.params_for("vivid", 0.5)
        self.assertAlmostEqual(half["saturation"], L.PRESETS["vivid"][2]["saturation"] / 2)

    def test_overrides_are_clamped_and_checked(self):
        p = L.params_for("natural", overrides={"fade": 3, "contrast": -4})
        self.assertEqual((p["fade"], p["contrast"]), (1.0, -1.0))
        with self.assertRaises(SystemExit):
            L.params_for("natural", overrides={"glow": 1})

    def test_svg_and_glsl_carry_the_same_numbers(self):
        c = L.pipeline(L.params_for("cinematic"))
        root = ET.fromstring(L.to_svg(c).split("\n")[0])
        ns = "{http://www.w3.org/2000/svg}"
        f = root.find(f"{ns}filter")
        self.assertEqual(f.get("color-interpolation-filters"), "sRGB")
        funcs = f.find(f"{ns}feComponentTransfer")
        self.assertEqual([float(x.get("slope")) for x in funcs], c["slope"])
        vals = [float(v) for v in f.find(f"{ns}feColorMatrix").get("values").split()]
        self.assertEqual([vals[i * 5 + j] for i in range(3) for j in range(3)], [x for row in c["matrix"] for x in row])
        glsl = L.to_glsl(c)
        self.assertIn("M * clamp(", glsl)
        self.assertIn(f"{c['matrix'][1][0]:.6f}", glsl)      # column 0 holds M[0][0], M[1][0], M[2][0]


@unittest.skipUnless(HAVE, "ffmpeg not installed")
class LookFfmpegTests(unittest.TestCase):
    def test_every_preset_matches_reference_maths(self):
        for name in L.PRESETS:
            r = L.verify(name)
            self.assertTrue(r["ok"], r)
            self.assertLessEqual(r["max_abs_error"], 2, r)

    def test_apply_writes_new_file_and_refuses_overwrite(self):
        tmp = Path(tempfile.mkdtemp())
        src = tmp / "in.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "testsrc2=size=160x90:rate=10:duration=1",
                        "-pix_fmt", "yuv420p", str(src)], check=True)
        out = tmp / "out.mp4"
        self.assertEqual(L.main(["apply", str(src), str(out), "--preset", "warm"]), 0)
        self.assertGreater(out.stat().st_size, 0)
        with self.assertRaises(SystemExit):
            L.main(["apply", str(src), str(out), "--preset", "warm"])


if __name__ == "__main__":
    unittest.main()
