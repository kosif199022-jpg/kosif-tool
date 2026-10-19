"""Regression checks for KOSIF Capability Atlas (read-only, no network)."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKILL = REPO / ".claude" / "skills" / "kosif-superpowers"
sys.path.insert(0, str(SKILL / "scripts"))
import capability_atlas as atlas


class TestCapabilityAtlas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index, cls.fresh = atlas.load()

    def test_generated_index_is_fresh_and_uses_real_counts(self):
        self.assertTrue(self.fresh)
        self.assertEqual(self.index["schema"], atlas.VERSION)
        self.assertEqual(self.index["source_sha256"], atlas.signature())
        self.assertEqual(self.index["catalog"]["total"], len(self.index["powers"]))
        self.assertGreater(self.index["catalog"]["total"], 4000)

    def test_unique_source_ids_and_trace(self):
        ids = [row["id"] for row in self.index["powers"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(row["source"].startswith("data/powers/") for row in self.index["powers"]))

    def test_bilingual_discovery(self):
        english = atlas.search(self.index, "Arabic PDF", top=10)
        arabic = atlas.search(self.index, "جرد مخزون", top=10)
        self.assertTrue(english)
        self.assertTrue(arabic)
        self.assertTrue(all(row["score"] > 0 for row in english + arabic))

    def test_unknown_query_does_not_fabricate_results(self):
        self.assertEqual(atlas.search(self.index, "zzzzunknownwordzzzz"), [])

    def test_plan_links_canonical_process_router(self):
        result = atlas.plan(self.index, "Build a software app with tests")
        self.assertEqual(result["master"], "kosif-superpowers")
        self.assertIn("test-driven-development", result["process_skills"])
        self.assertIn("verification-before-completion", result["process_skills"])
        self.assertTrue(result["capabilities"])
        self.assertIn("No catalog capability was executed", result["notice"])

    def test_unverified_api_and_dependencies(self):
        for item in ("key:SECRET_KEY", "npm:nonexistent-package", "service:cloud", "model:weights"):
            self.assertEqual(atlas.requirement_state(item)["state"], "unverified")

    def test_proof_is_not_session_receipt(self):
        p = atlas.show("DOC-05")
        self.assertIsNotNone(p)
        self.assertIn("not a receipt", p["notice"])
        self.assertIn("proof", p)

    def test_cli_json_and_doctor(self):
        script = str(SKILL / "scripts" / "capability_atlas.py")
        run = subprocess.run([sys.executable, script, "doctor", "--json"],
                             text=True, capture_output=True, timeout=60)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout)["status"], "ready")

    def test_no_credential_leak_in_plan(self):
        result = atlas.plan(self.index, "Write a program to edit a video", top=3)
        self.assertNotIn("api_key_value", json.dumps(result).lower())
        self.assertTrue(all("source" in c for c in result["capabilities"]))


if __name__ == "__main__":
    unittest.main()
