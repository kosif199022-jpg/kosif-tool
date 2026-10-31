"""Truthful planning and delivery gates for Cinema Pro; runs without FFmpeg."""
import tempfile
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))
import cinematic_pro_conductor as c


class CinemaProTests(unittest.TestCase):
    def test_all_pro_roles_discovered_but_not_claimed_executed(self):
        for kind in ("audio", "video"):
            plan = c.plan(kind)
            self.assertGreaterEqual(len(plan["team"]), 10)
            self.assertTrue(all(x["state"] == "candidate" for x in plan["team"]))
            self.assertTrue(plan["chosen_roles"])
            self.assertEqual(len(plan["stages"]), 4)

    def test_incompatible_option_fails(self):
        with self.assertRaises(ValueError):
            c.plan("audio", "reframe")
        with self.assertRaises(ValueError):
            c.plan("video", "not-a-real-option")

    def test_existing_tools_are_candidates_not_proof(self):
        with patch.object(c.m, "doctor", return_value={"tools": {}, "ready_options": []}):
            result = c.doctor()
        self.assertIn("cinema-pro.doctor", result["schema"])
        self.assertTrue(result["optional_modules"])
        self.assertTrue(all(v["executed"] is False for v in result["optional_modules"].values()))

    def test_gate_refuses_unverified_and_folders(self):
        with tempfile.TemporaryDirectory() as d:
            folder = Path(d)
            src = folder / "voice.mp3"; src.write_bytes(b"source")
            target = folder / "out.mp4"; target.write_bytes(b"placeholder")
            good = {"status": "rendered", "output": str(target), "verify": {"exit": 0},
                    "master_unchanged": True}
            with patch.object(c.m, "sha256", return_value="hash"):
                self.assertTrue(c.gate(good, src, "hash")["passed"])
                self.assertFalse(c.gate({**good, "verify": {"exit": 1}}, src, "hash")["passed"])
                self.assertFalse(c.gate({**good, "master_unchanged": False}, src, "hash")["passed"])
                self.assertFalse(c.gate({**good, "output": str(folder)}, src, "hash")["passed"])
                self.assertFalse(c.gate({**good, "status": "needs-inputs"}, src, "hash")["passed"])
                self.assertFalse(c.gate({**good, "delivery_mix": {"status": "failed"}}, src, "hash")["passed"])

    def test_run_writes_evidence_receipt_not_success_on_failed_verify(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d); src = path / "source.mp3"; src.write_bytes(b"source")
            job = path / "job"
            with patch.object(c.m, "probe", return_value={"video": None, "audio": {"codec": "mp3"}}), \
                 patch.object(c.m, "doctor", return_value={"tools": {"ffmpeg": {"present": True},
                     "node": {"present": True}}, "ready_options": []}), \
                 patch.object(c.m, "sha256", return_value="original"), \
                 patch.object(c.m, "intake", return_value={"kind": "audio"}), \
                 patch.object(c.m, "options", return_value={"menu": [{"id": "kinetic-film"}]}), \
                 patch.object(c.m, "build", return_value={"status": "rendered", "output": str(path / "absent.mp4"),
                     "master_unchanged": True, "verify": {"exit": 0}}):
                result = c.run(src, job)
            self.assertEqual(result["status"], "failed")
            self.assertEqual(result["executed"][-1]["stage"], "verify")
            self.assertFalse(result["executed"][-1]["passed"])
            saved = __import__("json").loads((job / "cinema_pro_receipt.json").read_text())
            self.assertEqual(saved["status"], "failed")


    def test_cinematic_recipes_select_chain_and_reject_wrong_kind(self):
        self.assertEqual(c.plan("video", recipe="cinematic-reel")["render_chain"],
                         ["highlight-reel", "reframe", "look"])
        self.assertEqual(c.plan("audio", recipe="cinematic-audio")["render_chain"],
                         ["kinetic-film", "look"])
        with self.assertRaises(ValueError):
            c.plan("audio", recipe="cinematic-reel")
        with self.assertRaises(ValueError):
            c.plan("video", option="look", recipe="cinematic-reel")

    def test_three_pass_recipe_verifies_each_stage_and_preserves_original(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            src = root / "source.mp4"
            src.write_bytes(b"original")
            outputs = []
            def mock_build(stage_job, option, style, title):
                f = stage_job / "out" / (option + ".mp4")
                f.parent.mkdir(parents=True, exist_ok=True)
                f.write_bytes(option.encode())
                outputs.append((option, style))
                return {"status": "rendered", "output": str(f),
                        "verify": {"exit": 0}, "master_unchanged": True}
            with patch.object(c.m, "probe", return_value={"video": {"width": 640}, "audio": {}}), \
                 patch.object(c.m, "doctor", return_value={"tools": {"ffmpeg": {"present": True},
                     "ffprobe": {"present": True}}, "ready_options": []}), \
                 patch.object(c.m, "sha256", return_value="immutable"), \
                 patch.object(c.m, "intake", return_value={"kind": "video"}), \
                 patch.object(c.m, "options", return_value={"menu": [{"id": "highlight-reel"}]}), \
                 patch.object(c.m, "build", side_effect=mock_build):
                receipt = c.run(src, root / "job", recipe="cinematic-reel", style="15")
            self.assertEqual(receipt["status"], "verified", receipt)
            self.assertEqual(outputs, [("highlight-reel", "15"), ("reframe", "9:16"), ("look", "film")])
            self.assertEqual(len(receipt["passes"]), 3)
            self.assertTrue(Path(receipt["output"]).is_file())
            self.assertEqual(len([s for s in receipt["executed"] if s["stage"] == "verify"]), 3)

    def test_recipe_stops_if_intermediate_verification_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); src = root / "source.mp4"; src.write_bytes(b"original")
            def failed_build(*_args):
                return {"status": "rendered", "output": str(root / "missing.mp4"),
                        "verify": {"exit": 0}, "master_unchanged": True}
            with patch.object(c.m, "probe", return_value={"video": {"width": 640}, "audio": {}}), \
                 patch.object(c.m, "doctor", return_value={"tools": {"ffmpeg": {"present": True},
                     "ffprobe": {"present": True}}, "ready_options": []}), \
                 patch.object(c.m, "sha256", return_value="immutable"), \
                 patch.object(c.m, "intake", return_value={"kind": "video"}), \
                 patch.object(c.m, "options", return_value={"menu": [{"id": "highlight-reel"}]}), \
                 patch.object(c.m, "build", side_effect=failed_build) as execute:
                receipt = c.run(src, root / "job", recipe="cinematic-reel")
            self.assertEqual(receipt["status"], "failed")
            self.assertEqual(execute.call_count, 1)
            self.assertEqual(len(receipt["passes"]), 1)


if __name__ == "__main__":
    unittest.main()
