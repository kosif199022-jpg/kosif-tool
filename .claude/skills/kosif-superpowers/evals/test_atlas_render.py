"""Real-browser tests for the original A15 explainer engine (skipped without Playwright/Chromium)."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import atlas_render as R  # noqa: E402

try:
    import playwright  # noqa: F401
    HAVE_PW = True
except ImportError:
    HAVE_PW = False


class EngineStaticTests(unittest.TestCase):
    def test_assets_are_original_and_complete(self):
        h = (SK / "assets" / "atlas_harness.js").read_text(encoding="utf-8")
        s = (SK / "assets" / "atlas_sound.js").read_text(encoding="utf-8")
        for name in ("KH.rng", "KH.noise", "KH.drawOn", "KH.roughStroke", "KH.grain", "KH.paper", "KH.camAt", "KH.counter", "KH.project"):
            self.assertIn(name, h)
        for name in ("KS.kit", "KS.live", "KS.renderOffline", "function bed", "function music", "withMinor"):
            self.assertIn(name, s)
        self.assertNotIn("Math.random(", "\n".join(l for l in (h + s).splitlines() if not l.strip().startswith("//")))
        page = (SK / "templates" / "atlas_explainer.html").read_text(encoding="utf-8")
        for name in ("window.seek", "window.DURATION", "window.scoreSound", "storyboard=1", "const BEATS"):
            self.assertIn(name, page)

    def test_cli_help_without_browser(self):
        r = subprocess.run([sys.executable, str(SK / "scripts" / "atlas_render.py"), "--help"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)
        self.assertIn("storyboard", r.stdout)


@unittest.skipUnless(HAVE_PW, "playwright not installed")
class EngineBrowserTests(unittest.TestCase):
    def test_check_is_deterministic_and_fast(self):
        r = subprocess.run([sys.executable, str(SK / "scripts" / "atlas_render.py"), "check"], capture_output=True, text=True, timeout=180)
        self.assertEqual(r.returncode, 0, r.stderr)
        rep = json.loads(r.stdout.strip().splitlines()[-1])
        self.assertTrue(rep["deterministic"])
        self.assertTrue(rep["has_scoreSound"])
        self.assertEqual(rep["beats"], 6)

    def test_short_render_has_video_and_audio(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "clip.mp4"
            self.assertEqual(R.main(["render", "--out", str(out), "--fps", "10", "--start", "6", "--end", "7.5"]), 0)
            probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type", "-of", "csv=p=0", str(out)], capture_output=True, text=True)
            self.assertEqual(sorted(probe.stdout.split()), ["audio", "video"])
            with self.assertRaises(SystemExit):
                R.main(["render", "--out", str(out), "--fps", "10", "--end", "1"])


if __name__ == "__main__":
    unittest.main()
