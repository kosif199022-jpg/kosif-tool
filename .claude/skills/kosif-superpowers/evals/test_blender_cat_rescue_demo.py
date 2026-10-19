"""Static and file-format proofs for the original five-second Blender demo."""
import json
from pathlib import Path
import shutil
import subprocess
import unittest

SK = Path(__file__).resolve().parents[1]
REPO = SK.parents[2]
SCRIPT = SK / "examples" / "blender_cat_rescue_5s.py"
MOVIE = REPO / "proofs" / "blender-cat-rescue-advanced-20261019" / "KOSIF_CAT_RESCUE_5_SECONDS.mp4"

class RescueDemoProof(unittest.TestCase):
    def test_source_compiles_without_importing_blender(self):
        source = SCRIPT.read_text(encoding="utf-8-sig")
        compile(source, str(SCRIPT), "exec")
        self.assertIn("scene.frame_end=120", source)
        self.assertIn("scene.render.fps=24", source)
        self.assertIn("bpy.ops.render.render(animation=True)", source)

    def test_public_rendered_proof_is_mp4(self):
        self.assertTrue(MOVIE.is_file())
        raw = MOVIE.read_bytes()
        self.assertGreater(len(raw), 10000)
        self.assertEqual(raw[4:8], b"ftyp")

    @unittest.skipUnless(shutil.which("ffprobe"), "ffprobe unavailable")
    def test_exact_five_seconds_120_frames(self):
        proc = subprocess.run([
            "ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
            "-show_entries", "stream=codec_name,nb_read_frames",
            "-show_entries", "format=duration", "-of", "json", str(MOVIE)
        ], capture_output=True, text=True, check=True)
        data = json.loads(proc.stdout)
        self.assertEqual(data["streams"][0]["codec_name"], "h264")
        self.assertEqual(int(data["streams"][0]["nb_read_frames"]), 120)
        self.assertAlmostEqual(float(data["format"]["duration"]), 5.0, delta=.01)

if __name__ == "__main__":
    unittest.main()
