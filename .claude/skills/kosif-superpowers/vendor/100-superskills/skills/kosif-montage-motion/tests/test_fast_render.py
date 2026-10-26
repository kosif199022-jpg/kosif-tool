"""The parallel renderer (film.film_animate, v1.3): chunks rendered by several browser pages, each its own H.264
segment, joined without re-encoding — the frames must come out complete and in time order."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import film  # noqa: E402

PAGE = """<!doctype html><html><body style="margin:0;background:#000"><canvas id="c" width="64" height="64"></canvas>
<script>const x = document.getElementById('c').getContext('2d');
window.seek = (t) => { const v = Math.round(Math.min(1, t / 2) * 255); x.fillStyle = `rgb(${v},${v},${v})`; x.fillRect(0, 0, 64, 64); };
window.seek(0);</script></body></html>"""


def _can_render() -> bool:
    try:
        import html_render
        from playwright.sync_api import sync_playwright  # noqa: F401
        return bool(shutil.which("ffmpeg")) and html_render.browser_path() is not None
    except Exception:  # noqa: BLE001
        return False


class ChunkingTests(unittest.TestCase):
    def test_auto_workers_bounds(self):
        self.assertEqual(film.auto_workers(10), 1)          # too few frames to pay for a second page
        self.assertGreaterEqual(film.auto_workers(600), 1)
        self.assertLessEqual(film.auto_workers(600), 6)


@unittest.skipUnless(_can_render(), "needs FFmpeg, Playwright and a Chromium")
class ParallelRenderTests(unittest.TestCase):
    def test_two_workers_keep_every_frame_in_order(self):
        d = Path(tempfile.mkdtemp(prefix="kosif_fast_"))
        try:
            page = d / "ramp.html"
            page.write_text(PAGE, encoding="utf-8")
            rep = film.film_animate(str(page), d / "ramp.mp4", fps=30, seconds=2.0, size=(64, 64), workers=2)
            self.assertEqual(rep["workers"], 2)
            probe = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                                    "stream=nb_read_frames", "-of", "json", str(d / "ramp.mp4")], capture_output=True, text=True)
            self.assertEqual(int(json.loads(probe.stdout)["streams"][0]["nb_read_frames"]), 60)
            raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(d / "ramp.mp4"), "-f", "rawvideo", "-pix_fmt", "gray", "-"],
                                 capture_output=True).stdout
            lum = [raw[i * 64 * 64 + 32 * 64 + 32] for i in range(60)]
            self.assertLess(lum[0], 20)
            self.assertGreater(lum[-1], 230)
            self.assertTrue(all(b >= a - 3 for a, b in zip(lum, lum[1:])), lum)    # monotonic: chunks joined in order
        finally:
            shutil.rmtree(d, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
