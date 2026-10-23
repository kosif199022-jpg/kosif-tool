"""Smoke tests for scripts the REA map (scripts/rea_superpowers_map.py) found with no test at all.

Each script must parse its arguments and print usage without touching the network, git or Atlas
sources; the offline Atlas method router also gets a behavioural check on its shipped manifest."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import atlas_task_method_router as router  # noqa: E402

HELP_ONLY = [
    "scripts/atlas_bulk_source_audit.py",
    "scripts/atlas_deep_fusion.py",
    "scripts/atlas_review_summary.py",
    "scripts/atlas_task_method_router.py",
    "scripts/atlas_transfer.py",
    "scripts/probe_env.py",
    "scripts/rea_owned_repo_batch.py",
    "scripts/rebalance_creative_repos.py",
]


class ScriptSmokeTests(unittest.TestCase):
    def test_help_exits_zero(self):
        for rel in HELP_ONLY:
            with self.subTest(script=rel):
                r = subprocess.run([sys.executable, str(SK / rel), "--help"], capture_output=True, text=True,
                                   timeout=60, cwd=str(SK))
                self.assertEqual(r.returncode, 0, r.stderr[-400:])
                self.assertIn("usage:", r.stdout)

    def test_method_router_on_shipped_manifest(self):
        data = json.loads((SK / "data/atlas-method-provenance-20261020.json").read_text(encoding="utf-8-sig"))
        out = router.route("run a pre-mortem on the launch plan: what could fail", data)
        self.assertEqual(out["schema"], "kosif.superpowers.atlas.method-route.v1")
        self.assertLessEqual(out["selected_count"], 2)
        for row in out["selected"]:
            self.assertFalse(row["third_party_code_executed"])
            self.assertFalse(row["executor_exposed"])
        none = router.route("bake a sourdough loaf", data)
        self.assertEqual((none["selected_count"], none["fallback"]), (0, "native_kosif_superpowers"))
        with self.assertRaises(ValueError):
            router.route("x", data, max_methods=3)


if __name__ == "__main__":
    unittest.main()
