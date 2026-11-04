"""Tests for suno_bridge.py (A46): offline, no network, no credits."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))
import suno_bridge as sb  # noqa: E402

SCRIPT = SKILL / "scripts" / "suno_bridge.py"


class PlanTests(unittest.TestCase):
    def test_egyptian_ad(self):
        p = sb.build_plan("عايز أغنية مهرجان مصري لإعلان 30 ثانية صوت رجالي")
        pr = p["prompt"]
        self.assertIn("mahraganat", pr["style"])
        self.assertIn("male vocals", pr["style"])
        self.assertEqual(pr["duration_seconds"], 30)
        self.assertEqual(pr["dialect"], "Egyptian Arabic")
        self.assertEqual(pr["structure"], ["Hook", "Chorus", "Tag"])
        self.assertTrue(p["approval_required"] and p["credits_spend"])
        self.assertFalse(p["generated"])
        self.assertLessEqual(len(pr["style"]), sb.STYLE_LIMIT)

    def test_dua_is_vocals_only(self):
        pr = sb.build_plan("دعاء ليلة الجمعة بدون موسيقى")["prompt"]
        self.assertIn("a cappella", pr["style"])
        self.assertFalse(pr["instrumental"])

    def test_instrumental_has_no_lyrics(self):
        pr = sb.build_plan("cinematic epic trailer, instrumental, 2 min")["prompt"]
        self.assertTrue(pr["instrumental"])
        self.assertIsNone(pr["lyrics_scaffold"])
        self.assertEqual(pr["duration_seconds"], 120)
        self.assertEqual(pr["language"], "English")

    def test_digest_is_deterministic_and_prompt_bound(self):
        a = sb.build_plan("lofi calm study beat")
        b = sb.build_plan("lofi calm study beat")
        c = sb.build_plan("lofi calm study beat", duration=60)
        self.assertEqual(a["approval_digest"], b["approval_digest"])
        self.assertNotEqual(a["approval_digest"], c["approval_digest"])
        self.assertRegex(a["approval_digest"], r"^[0-9a-f]{64}$")


class ReceiptTests(unittest.TestCase):
    def setUp(self):
        self.plan = sb.build_plan("أغنية أطفال مرحة")
        self.result = {"clips": [{"id": "abc-123", "audio_url": "https://cdn1.suno.ai/abc-123.mp3",
                                  "duration": 118.4}]}

    def test_verified_with_matching_digest(self):
        r, errors = sb.build_receipt(self.plan, self.result, self.plan["approval_digest"])
        self.assertEqual(errors, [])
        self.assertEqual(r["status"], "VERIFIED")
        self.assertEqual(r["song_id"], "abc-123")
        self.assertEqual(r["duration_seconds"], 118.4)

    def test_refuses_other_digest(self):
        r, errors = sb.build_receipt(self.plan, self.result, "0" * 64)
        self.assertEqual(r["status"], "REFUSED")
        self.assertTrue(any("does not match" in e for e in errors))

    def test_refuses_edited_plan(self):
        edited = json.loads(json.dumps(self.plan))
        edited["prompt"]["style"] = "heavy metal"
        _, errors = sb.build_receipt(edited, self.result, self.plan["approval_digest"])
        self.assertTrue(any("edited" in e for e in errors))

    def test_refuses_result_without_song(self):
        _, errors = sb.build_receipt(self.plan, {"status": "queued"}, self.plan["approval_digest"])
        self.assertTrue(any("no song id" in e for e in errors))

    def test_audio_file_hashed(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "song.mp3"
            f.write_bytes(b"ID3fake")
            r, errors = sb.build_receipt(self.plan, {"id": "x1"}, self.plan["approval_digest"], f)
            self.assertEqual(errors, [])
            self.assertEqual(r["audio_file"]["bytes"], 7)


class CliTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True,
                              timeout=60)

    def test_help_and_doctor(self):
        self.assertEqual(self.run_cli("--help").returncode, 0)
        d = self.run_cli("doctor")
        self.assertEqual(d.returncode, 0)
        doc = json.loads(d.stdout)
        self.assertIn("credits:spend", doc["resource_scopes"])
        self.assertEqual(doc["network_requests"], 0)

    def test_plan_then_receipt_round_trip(self):
        with tempfile.TemporaryDirectory() as d:
            plan_f, res_f, rec_f = Path(d, "plan.json"), Path(d, "res.json"), Path(d, "rec.json")
            self.assertEqual(self.run_cli("plan", "نشيد رمضان", "--out", str(plan_f)).returncode, 0)
            digest = json.loads(plan_f.read_text(encoding="utf-8"))["approval_digest"]
            res_f.write_text(json.dumps({"id": "s1", "url": "https://suno.com/song/s1"}), encoding="utf-8")
            ok = self.run_cli("receipt", "--plan", str(plan_f), "--result", str(res_f),
                              "--approved-digest", digest, "--out", str(rec_f))
            self.assertEqual(ok.returncode, 0, ok.stderr)
            bad = self.run_cli("receipt", "--plan", str(plan_f), "--result", str(res_f),
                               "--approved-digest", "f" * 64)
            self.assertEqual(bad.returncode, 1)

    def test_probe_network_blocked_is_exit_3(self):
        with mock.patch.object(sb.urllib.request, "urlopen", side_effect=sb.urllib.error.URLError("blocked")):
            out, code = sb.probe(1)
        self.assertEqual(code, 3)
        self.assertFalse(out["credentials_sent"])


if __name__ == "__main__":
    unittest.main()
