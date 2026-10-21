"""Hubs: every family in exactly one hub, every superpower in exactly one hub, routing and install plans work."""
import json, subprocess, sys, unittest
from pathlib import Path
SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import powers as P  # noqa: E402
import kosif_hubs as H  # noqa: E402


class HubTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.idx = json.loads((SK / "data" / "hubs_index.json").read_text(encoding="utf-8"))

    def test_families_partitioned(self):
        fams = [f for h in H.hubs() for f in h["families"]]
        self.assertEqual(len(fams), len(set(fams)))
        self.assertEqual(set(fams), {p["family"] for p in P.load_powers()})

    def test_index_fresh_and_complete(self):
        fresh = H.build_index()
        self.assertEqual(fresh["hubs"], self.idx["hubs"], "hubs_index.json is stale: run kosif_hubs.py build")
        sps = [s for h in self.idx["hubs"] for s in h["superpowers"]]
        self.assertEqual(len(sps), len(set(sps)))
        self.assertEqual(len(sps), self.idx["superpowers"])
        self.assertEqual(sum(h["powers"] for h in self.idx["hubs"]), self.idx["atoms"])

    def test_scripts_exist(self):
        for h in H.hubs():
            for s in h["scripts"]:
                self.assertTrue((SK / "scripts" / s).exists(), s)

    def test_routing(self):
        for task, hubs in (("مونتاج ريلز بانتقالات سريعة", {"motion"}), ("ارسم شعار بالكود", {"drawing"}),
                           ("analyze an electron app with rea", {"reverse"}), ("اكتب مقال عربي", {"documents", "type"})):
            res = H.route(self.idx, task, 3)
            self.assertTrue(hubs & {r["hub"]["id"] for r in res}, task)

    def test_install_plan_never_marks_keys_present_without_env(self):
        rows = H.install_plan(["key:elevenlabs"])
        self.assertNotIn("key:elevenlabs", rows["present"]) if not __import__("os").environ.get("ELEVENLABS_API_KEY") else None


if __name__ == "__main__":
    unittest.main()
