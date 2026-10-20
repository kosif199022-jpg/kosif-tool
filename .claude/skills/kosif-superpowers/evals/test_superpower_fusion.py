"""Fused superpowers: every atomic power in exactly one superpower, fewer superpowers, one connected graph."""
import json, sys, unittest
from pathlib import Path
SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import powers as P  # noqa: E402
import superpower_fusion as F  # noqa: E402


class FusionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((SK / "data" / "superpowers.json").read_text(encoding="utf-8"))
        cls.atoms = P.load_powers()

    def test_partition_is_exact(self):
        ids = [m["id"] for s in self.data["items"] for m in s["pipeline"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(set(ids), {p["id"] for p in self.atoms}, "superpowers.json is stale: run superpower_fusion.py build")

    def test_fewer_and_connected(self):
        self.assertLess(self.data["superpowers"], len(self.atoms) / 5)
        self.assertEqual(F.connected(self.data["items"]), 1)
        for s in self.data["items"]:
            self.assertTrue(s["links"])

    def test_badge_honesty(self):
        for s in self.data["items"]:
            self.assertEqual(sum(s["status_mix"].values()), s["size"])
            self.assertEqual(s["best"], min(s["status_mix"], key=lambda k: P.STATUSES.index(k)))

    def test_suggest_routes_arabic_brief(self):
        res = F.suggest(self.data, "مونتاج ريلز بإيقاع الموسيقى", 5)
        self.assertTrue(res)
        self.assertEqual(res[0]["domain"], "motion")


if __name__ == "__main__":
    unittest.main()
