"""Preview before render: `plan` stops with a storyboard and a movement matrix, `go` renders after the yes."""
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

DM = SCRIPTS / "dragon_montage.py"


@unittest.skipUnless(C.have("ffmpeg") and C.have("ffprobe"), "ffmpeg needed")
class PreviewBeforeRender(unittest.TestCase):
    def test_plan_stops_then_go_renders(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            a = C.make_test_clip(tmp / "a.mp4", 8.0, tone=440)
            job = tmp / "job"
            res = subprocess.run([sys.executable, str(DM), "plan", "ريل قصير", "--clip", str(a), "--job", str(job),
                                  "--seconds", "6", "--no-transcribe", "--preview", "--rounds", "1"],
                                 capture_output=True, text=True, timeout=900)
            self.assertEqual(res.returncode, 0, res.stderr[-2000:])
            out = json.loads(res.stdout.strip().splitlines()[-1])
            self.assertEqual(out["status"], "awaiting_owner_approval")
            self.assertFalse((job / "render").exists(), "plan must not render")
            plan = json.loads((job / "preview" / "plan.json").read_text(encoding="utf-8"))
            edl = C.read(job, "edl")
            self.assertEqual([r["id"] for r in plan["rows"]], [e["id"] for e in edl["events"]])
            self.assertTrue(all(r["camera"] and r["transition"] and r["reason"] for r in plan["rows"]))
            md = (job / "preview" / "PLAN_AR.md").read_text(encoding="utf-8")
            self.assertIn("مصفوفة التحركات", md)
            self.assertIn("موافق", md)
            self.assertEqual(md.count("\n| ") - 1, len(plan["rows"]))   # one matrix row per cut (+ header)
            try:
                import PIL  # noqa: F401
                self.assertTrue((job / "preview" / "storyboard.jpg").stat().st_size > 1000)
            except ImportError:
                pass

            res = subprocess.run([sys.executable, str(DM), "go", "--job", str(job)],
                                 capture_output=True, text=True, timeout=900)
            self.assertEqual(res.returncode, 0, res.stderr[-2000:])
            self.assertTrue(Path(json.loads(res.stdout.strip().splitlines()[-1])["final"]).is_file())
            meta = json.loads((job / "job.json").read_text(encoding="utf-8"))
            self.assertEqual(meta["status"], "approved")

    def test_go_without_plan_refuses(self):
        with tempfile.TemporaryDirectory() as tmp:
            res = subprocess.run([sys.executable, str(DM), "go", "--job", tmp], capture_output=True, text=True)
            self.assertNotEqual(res.returncode, 0)
            self.assertIn("plan", res.stderr)


if __name__ == "__main__":
    unittest.main()
