"""Mind map & audit: every superpower has one stage, task maps follow stage order, fresh build."""
import json, sys, unittest
from pathlib import Path
SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import capability_mindmap as M  # noqa: E402


class MindmapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = json.loads((SK / "data" / "capability_mindmap.json").read_text(encoding="utf-8"))

    def test_fresh(self):
        fresh = json.loads(json.dumps(M.build(), ensure_ascii=False))
        self.assertEqual(fresh["tasks"], self.d["tasks"], "capability_mindmap.json is stale: run capability_mindmap.py build")

    def test_stage_order_and_coverage(self):
        order = [s["id"] for s in self.d["stages"]]
        sps = self.d["superpowers"]
        self.assertTrue(all(s["stage"] in order for s in sps.values()))
        for tm in self.d["tasks"]:
            keys = list(tm["plan"])
            self.assertEqual(keys, sorted(keys, key=order.index), tm["id"])
            self.assertIn("create", keys, tm["id"])
        hub_sp = sum(len(v) for h in self.d["hubs"] for v in h["stages"].values())
        self.assertEqual(hub_sp, len(sps))


if __name__ == "__main__":
    unittest.main()
