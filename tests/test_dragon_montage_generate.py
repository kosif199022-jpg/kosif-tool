"""Optional station «التوليد والمحاكاة» of Dragon Montage: dm_generate.py (gaps/attach) and dm_mimic.py.

No network: proposals are text only, attach copies a local synthetic clip, mimic runs mm_analyze locally.
"""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".claude/skills/kosif-dragon-montage/scripts"
sys.path.insert(0, str(SCRIPTS))
import dm_common as C  # noqa: E402

GEN = SCRIPTS / "dm_generate.py"
MIM = SCRIPTS / "dm_mimic.py"
LINT = ROOT / ".claude/skills/living-site/tools/kling_lint.py"
HAVE_FF = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))


def run(*argv):
    res = subprocess.run([sys.executable, *map(str, argv)], capture_output=True, text=True, timeout=900)
    if res.returncode:
        raise AssertionError(f"rc={res.returncode}\n{res.stderr[-2000:]}\n{res.stdout[-500:]}")
    return res


def fixture_job(job: Path) -> None:
    """Brief wants 60 s; the owner gave 20 s of footage (2 clips x 10 s); no music; weak hook shot."""
    def clip(cid, path, q_first):
        return {"id": cid, "path": str(path), "duration": 10.0, "width": 1920, "height": 1080, "fps": 30.0,
                "has_audio": True, "loudness_lufs": -20.0,
                "shots": [{"id": f"{cid}-s001", "start": 0.0, "end": 5.0, "quality": {"score": q_first},
                           "faces": 0, "thumb": f"analysis/{cid}-s001.jpg"},
                          {"id": f"{cid}-s002", "start": 5.0, "end": 10.0, "quality": {"score": 0.7}, "faces": 0}],
                "words": [], "silences": [], "energy": []}
    C.write(job, "analysis", C.new("analysis", clips=[clip("c01", "/x/a.mp4", 0.3), clip("c02", "/x/b.mp4", 0.6)],
                                   music={"path": None, "bpm": None, "beats": [], "downbeats": []},
                                   tools_used=["ffprobe"], missing=[]))
    C.write(job, "brief", C.new("brief", task="مونتاج لرحلة في سيوة: الهدوء والمية والنخل", one_truth="Siwa is calm water and palms",
                                platform="reel", aspect="9:16", target_seconds=60, feeling="calm",
                                content_type="travel", energy=0.4))
    C.write(job, "concepts", C.new("concepts", concepts=[{"id": "A", "title": "t", "logline": "l",
                                                          "arc": ["hook", "setup", "turn", "payoff", "cta"]}],
                                   decision={"chosen": "A"}))
    C.write(job, "look", C.new("look", style_id="calm", grade={"id": "warm"}, transitions=[{"id": "cut"}],
                               captions={"style": "clean"}, music={"mood": "calm", "bpm_range": [70, 90]}))
    C.write(job, "edl", C.new("edl", width=1080, height=1920, fps=30, duration=18.0, captions={"enabled": False},
                              audio={"music": {"path": None}},
                              events=[{"id": "e001", "clip": "c01", "src_in": 0.0, "src_out": 3.0, "rec_in": 0.0,
                                       "shot": "c01-s001", "reason": "hook: first image"},
                                      {"id": "e002", "clip": "c02", "src_in": 5.0, "src_out": 10.0, "rec_in": 3.0,
                                       "shot": "c02-s002", "reason": "setup: the place"},
                                      {"id": "e003", "clip": "c01", "src_in": 5.0, "src_out": 10.0, "rec_in": 8.0,
                                       "role": "payoff", "reason": "the palms at sunset"}]))


class GenerateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.job = self.tmp / "job"
        self.job.mkdir()
        fixture_job(self.job)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_gaps_proposals(self):
        run(GEN, "gaps", "--job", self.job)
        doc = json.loads((self.job / "generate.json").read_text(encoding="utf-8"))
        self.assertEqual(doc["schema"], "kosif.dm.generate.v1")
        self.assertEqual(doc["credits_spent"], 0)
        kinds = {g["kind"] for g in doc["gaps"]}
        self.assertTrue({"short-footage", "missing-role", "weak-hook", "no-music"} <= kinds, kinds)
        props = doc["proposals"]
        self.assertTrue(props)
        self.assertTrue(all(p["consent_required"] is True for p in props))
        for p in props:
            for k in ("id", "kind", "role", "seconds", "prompt", "negative", "model_suggestion", "tool", "est_credits"):
                self.assertIn(k, p)
        roles = {p["role"] for p in props}
        self.assertTrue({"turn", "cta", "hook", "music", "broll"} <= roles, roles)
        video = [p for p in props if p["kind"] == "video"]
        self.assertGreaterEqual(sum(p["seconds"] for p in video if p["role"] == "broll"), 40)
        self.assertTrue(all(3 <= p["seconds"] <= 30 for p in video))
        music = [p for p in props if p["kind"] == "music"]
        self.assertEqual(music[0]["tool"], "suno.audio-create")
        self.assertIn("70-90 BPM", music[0]["prompt"])
        if LINT.is_file():
            for p in video:
                self.assertEqual(p["lint"]["result"], "PASS", (p["id"], p["lint"]))
        ar = (self.job / "GENERATE_AR.md").read_text(encoding="utf-8")
        self.assertIn("أيوه", ar)
        self.assertIn("mcp__Higgsfield__generate_video", ar)

    def test_no_gaps_when_footage_is_enough(self):
        b = C.read(self.job, "brief")
        b["target_seconds"] = 10
        C.write(self.job, "brief", b)
        (self.job / "edl.json").unlink()
        (self.job / "look.json").unlink()
        run(GEN, "gaps", "--job", self.job)
        doc = json.loads((self.job / "generate.json").read_text(encoding="utf-8"))
        self.assertNotIn("short-footage", {g["kind"] for g in doc["gaps"]})

    @unittest.skipUnless(HAVE_FF, "ffmpeg missing")
    def test_attach_adds_clip(self):
        run(GEN, "gaps", "--job", self.job)
        doc = json.loads((self.job / "generate.json").read_text(encoding="utf-8"))
        pid = next(p["id"] for p in doc["proposals"] if p["kind"] == "video")
        f = C.make_test_clip(self.tmp / "generated.mp4", 4.0, size="320x568")
        out = json.loads(run(GEN, "attach", "--job", self.job, "--proposal", pid, "--file", f).stdout)
        self.assertEqual(out["clip"], "c03")
        an = C.read(self.job, "analysis")
        new = an["clips"][-1]
        self.assertEqual(new["id"], "c03")
        self.assertTrue(new["generated"])
        self.assertTrue((self.job / new["path"]).is_file() or Path(new["path"]).is_file())
        self.assertAlmostEqual(new["duration"], 4.0, delta=0.3)
        doc = json.loads((self.job / "generate.json").read_text(encoding="utf-8"))
        self.assertEqual(next(p for p in doc["proposals"] if p["id"] == pid)["status"], "attached")


@unittest.skipUnless(HAVE_FF, "ffmpeg missing")
class MimicTest(unittest.TestCase):
    def test_mimic_rhythm(self):
        with tempfile.TemporaryDirectory() as tmp:
            job = Path(tmp) / "job"
            ref = C.make_test_clip(Path(tmp) / "ref.mp4", 6.0, size="320x180")
            run(MIM, "mimic", "--job", job, "--reference", ref, "--skip-text")
            rh = json.loads((job / "reference_rhythm.json").read_text(encoding="utf-8"))
            self.assertEqual(rh["schema"], "kosif.dm.reference_rhythm.v1")
            self.assertGreaterEqual(len(rh["shots"]), 2)
            self.assertAlmostEqual(rh["shots"][1]["start"], 3.0, delta=0.2)
            self.assertTrue(rh["pacing"]["shot_lengths_s"])
            lk = C.validate("look", json.loads((job / "look_override.json").read_text(encoding="utf-8")))
            self.assertEqual(lk["transitions"][0]["id"], "cut")
            self.assertTrue(any(r["tool"] == "mm_analyze" and r["rc"] == 0 for r in C.receipts(job)))


if __name__ == "__main__":
    unittest.main()
