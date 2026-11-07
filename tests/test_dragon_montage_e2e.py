"""End-to-end: «التنين الأسود، مونتاج» runs all eight stations on synthetic footage."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".claude/skills/kosif-dragon-montage/scripts"
sys.path.insert(0, str(SCRIPTS))
import dm_common as C  # noqa: E402


class DragonMontageE2E(unittest.TestCase):
    def test_edit_through_black_dragon(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            a = C.make_test_clip(tmp / "a clip.mp4", 8.0, tone=440)
            b = C.make_test_clip(tmp / "b.mp4", 6.0, tone=660, color="rgbtestsrc")
            job = tmp / "job"
            res = subprocess.run([
                sys.executable, str(ROOT / ".claude/skills/kosif-superpowers/scripts/black_dragon.py"),
                "montage", "edit", "اعمل ريل قصير حماسي", "--clip", str(a), "--clip", str(b),
                "--job", str(job), "--platform", "reel", "--seconds", "8", "--no-transcribe",
                "--preview", "--rounds", "2"], capture_output=True, text=True, timeout=900)
            self.assertEqual(res.returncode, 0, res.stderr[-3000:])
            out = json.loads(res.stdout.strip().splitlines()[-1])
            self.assertTrue(Path(out["final"]).is_file())
            for kind in ("analysis", "brief", "concepts", "look", "edl", "render", "review"):
                C.read(job, kind)
            edl = C.read(job, "edl")
            self.assertTrue(all(ev["reason"].strip() for ev in edl["events"]))
            report = (job / "report.md").read_text(encoding="utf-8")
            self.assertIn("الأرقام بأمانة", report)
            self.assertTrue(any(r["owner_media"] for r in C.receipts(job)))
            job_meta = json.loads((job / "job.json").read_text(encoding="utf-8"))
            self.assertIn("rounds", job_meta)


if __name__ == "__main__":
    unittest.main()
