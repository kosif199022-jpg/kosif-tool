"""pixel-studio-painter: `studio.py --code FILE --render PNG` draws the code in FILE, not the default scene."""
import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STUDIO = (ROOT / ".claude/skills/kosif-superpowers/vendor/100-superskills/skills/pixel-studio-painter"
          / "scripts" / "studio.py")
NEEDS = ("numpy", "PIL", "cv2")
MISSING = [m for m in NEEDS if importlib.util.find_spec(m) is None]

PIL_CODE = """from PIL import Image, ImageDraw
img = Image.new("RGB", (1200, 800), (255, 0, 0))
draw = ImageDraw.Draw(img)
draw.rectangle((0, 0, 99, 99), fill=(0, 0, 255))
img.save("out.png")
"""
SVG_CODE = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800">'
            '<rect width="1200" height="800" fill="#00ff00"/></svg>')


@unittest.skipIf(MISSING, f"missing modules: {MISSING}")
class PixelStudioCodeRender(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="pixel_studio_code_")
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def render(self, *args):
        env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}     # no __pycache__ inside vendor/
        return subprocess.run([sys.executable, "-B", str(STUDIO), *args], cwd=self.tmp, env=env,
                              capture_output=True, text=True, timeout=180)

    def pixels(self, png):
        from PIL import Image
        with Image.open(png) as im:
            return im.convert("RGB"), im.size

    def test_pil_code_is_rendered_not_the_default_scene(self):
        code, png = self.tmp / "red.py", self.tmp / "out.png"
        code.write_text(PIL_CODE, encoding="utf-8")
        p = self.render("--code", str(code), "--render", str(png))
        self.assertEqual(p.returncode, 0, p.stderr)
        im, size = self.pixels(png)
        self.assertEqual(size, (1200, 800))
        self.assertEqual(im.getpixel((600, 400)), (255, 0, 0))          # the red canvas
        self.assertEqual(im.getpixel((1150, 750)), (255, 0, 0))
        self.assertEqual(im.getpixel((10, 10)), (0, 0, 255))            # the blue square in the corner
        self.assertEqual(im.getpixel((150, 150)), (255, 0, 0))

    def test_svg_code_is_rendered_at_scale(self):
        code, png = self.tmp / "green.svg", self.tmp / "green.png"
        code.write_text(SVG_CODE, encoding="utf-8")
        p = self.render("--code", str(code), "--render", str(png), "--scale", "0.5")
        self.assertEqual(p.returncode, 0, p.stderr)
        im, size = self.pixels(png)
        self.assertEqual(size, (600, 400))
        for xy in ((300, 200), (20, 20), (580, 380)):
            self.assertEqual(im.getpixel(xy), (0, 255, 0))

    def test_risky_code_is_refused_without_allow_risky(self):
        code, png = self.tmp / "risky.py", self.tmp / "risky.png"
        code.write_text("import subprocess\n" + PIL_CODE, encoding="utf-8")
        p = self.render("--code", str(code), "--render", str(png))
        self.assertNotEqual(p.returncode, 0)
        self.assertFalse(png.exists())

    def test_render_without_code_still_draws_a_scene(self):
        png = self.tmp / "scene.png"
        p = self.render("--render", str(png), "--scale", "0.25")
        self.assertEqual(p.returncode, 0, p.stderr)
        _, size = self.pixels(png)
        self.assertEqual(size, (300, 200))


if __name__ == "__main__":
    unittest.main()
