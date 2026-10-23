"""REA-approach superpowers map: synthetic self-test plus read-only checks on the real tree. Nothing is executed."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import rea_superpowers_map as rm  # noqa: E402


class ReaSuperpowersMapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = rm.build(atlas=False)

    def test_self_test_passes(self):
        r = subprocess.run([sys.executable, str(SK / "scripts/rea_superpowers_map.py"), "--self-test"],
                           capture_output=True, text=True, timeout=120)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(json.loads(r.stdout)["self_test"], "pass")

    def test_real_tree_is_mapped(self):
        c = self.m["counts"]
        self.assertGreater(c["scripts"], 100)
        self.assertGreater(c["py_edges"], 50)
        self.assertEqual(self.m["parse_failures"], [])
        ids = {s["id"] for s in self.m["scripts"]}
        self.assertIn("rea_superpowers_map", ids)
        self.assertTrue(set(rm.GAP_KINDS) >= set(c["gaps"]))

    def test_registered_and_linked(self):
        node = rm.find_node(self.m, "rea_superpowers_map")
        self.assertEqual(node["role"], "registered")
        self.assertIn("rea-superpowers-map", node["tools"])
        self.assertTrue(node["tests"])

    def test_receipt_is_trimmed_rea_output(self):
        rec = json.loads((SK / rm.RECEIPT).read_text(encoding="utf-8"))
        self.assertEqual(rec["schema"], "kosif.rea-receipt.v1")
        self.assertEqual(rec["tool"], "rea import-reference-source")
        self.assertEqual(rec["authority"], "historical-reference")
        for r in rec["relationships"]:
            self.assertFalse(r["from"].startswith(("/", "..")))

    def test_ingest_rejects_foreign_json(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "x.json"
            p.write_text('{"schema": "Other"}')
            with self.assertRaises(SystemExit):
                rm.ingest_rea(p, p, root=Path(d))

    def test_outputs_deterministic(self):
        self.assertEqual(rm.outputs(self.m), rm.outputs(rm.build(atlas=False)))

    def test_ci_detection_covers_scripts_and_repo_tests(self):
        ci = ("run: python3 -m unittest discover -s .claude/skills/kosif-superpowers/evals -p 'test_*.py'\n"
              "run: python3 -m unittest discover -s tests -v\n"
              "run: python3 .claude/skills/kosif-superpowers/proofs/x/test_writing.py\n")
        d, f = rm.ci_patterns(ci)
        self.assertIn(("tests", "test*.py"), d)                       # unittest's default pattern
        self.assertTrue(rm.in_ci(".claude/skills/kosif-superpowers/evals/test_a.py", d, f))
        self.assertTrue(rm.in_ci("tests/test_repo.py", d, f))
        self.assertTrue(rm.in_ci(".claude/skills/kosif-superpowers/proofs/x/test_writing.py", d, f))
        # a test kept beside its tool is NOT covered by the evals pattern: its folder must be discovered too
        self.assertFalse(rm.in_ci(".claude/skills/kosif-superpowers/scripts/test_tool.py", d, f))
        d2, f2 = rm.ci_patterns(ci + "run: python3 -m unittest discover -s .claude/skills/kosif-superpowers/scripts -p 'test_*.py' -v\n")
        self.assertTrue(rm.in_ci(".claude/skills/kosif-superpowers/scripts/test_tool.py", d2, f2))

    def test_real_tree_gap_ids_include_scripts_tests_when_uncovered(self):
        ci_file = rm.REPO / ".github/workflows/ci.yml"
        if not ci_file.is_file():
            self.skipTest("skill is not inside its repository checkout")
        d, f = rm.ci_patterns(ci_file.read_text(encoding="utf-8"))
        uncovered = {g["id"] for g in self.m["gaps"] if g["kind"] == "test_not_in_ci"}
        for t in sorted((SK / "scripts").glob("test_*.py")):
            rel = ".claude/skills/kosif-superpowers/scripts/" + t.name
            self.assertEqual(rm.in_ci(rel, d, f), "scripts/" + t.name not in uncovered, t.name)

    def test_html_is_self_contained(self):
        page = rm.outputs(self.m)[rm.OUT_HTML]
        self.assertNotIn("<script src", page)
        self.assertNotIn("<link", page)
        self.assertIn("prefers-color-scheme", page)


if __name__ == "__main__":
    unittest.main()
