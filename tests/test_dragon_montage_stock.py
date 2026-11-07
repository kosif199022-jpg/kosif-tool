"""Open-licence footage station: ranking and offline source listing (no network in tests)."""
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".claude/skills/kosif-dragon-montage/scripts"
sys.path.insert(0, str(SCRIPTS))
import dm_stock as S  # noqa: E402


class StockTests(unittest.TestCase):
    def test_rank_prefers_verified_commercial_no_credit_large(self):
        good = {"id": "a", "width": 1080, "height": 1920,
                "licence": {"verified": True, "commercial": True, "attribution_required": False}}
        credit = {"id": "b", "width": 1080, "height": 1920,
                  "licence": {"verified": True, "commercial": True, "attribution_required": True}}
        nc = {"id": "c", "width": 2160, "height": 3840,
              "licence": {"verified": True, "commercial": False, "attribution_required": False}}
        sus = {"id": "d", "width": 4000, "height": 4000, "flags": ["suspicious-licence"],
               "licence": {"verified": False, "commercial": None}}
        self.assertEqual([r["id"] for r in sorted([sus, nc, credit, good], key=S.rank)], ["a", "b", "c", "d"])

    def test_sources_lists_free_sites_offline(self):
        out = subprocess.run([sys.executable, str(SCRIPTS / "dm_stock.py"), "sources", "--find", "pexels"],
                             capture_output=True, text=True, encoding="utf-8", timeout=60)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("pexels", out.stdout.lower())


if __name__ == "__main__":
    unittest.main()
