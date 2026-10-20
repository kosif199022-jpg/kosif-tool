"""Capability graph (scripts/capability_graph.py): every family is connected, code edges are real files."""
from __future__ import annotations

import json
import os
import subprocess
import tempfile
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / ".claude" / "skills" / "kosif-superpowers"


class CapabilityGraphTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Build into a temporary folder: tests must never rewrite tracked files.
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.tmp.name)
        proc = subprocess.run([sys.executable, str(SKILL / "scripts" / "capability_graph.py"), "build", "--out-dir", str(cls.out)],
                              capture_output=True, text=True, timeout=180)
        assert proc.returncode == 0, proc.stderr
        cls.g = json.loads((cls.out / "capability_graph.json").read_text(encoding="utf-8"))

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_build_is_deterministic_and_committed_files_are_current(self):
        again = Path(self.tmp.name) / "again"
        proc = subprocess.run([sys.executable, str(SKILL / "scripts" / "capability_graph.py"), "build", "--out-dir", str(again)],
                              capture_output=True, text=True, timeout=180, env={**os.environ, "PYTHONHASHSEED": "12345"})
        self.assertEqual(proc.returncode, 0, proc.stderr)
        for name in ("capability_graph.json", "capability-graph.html"):
            self.assertEqual((self.out / name).read_bytes(), (again / name).read_bytes(), f"{name} differs between two builds")
        check = subprocess.run([sys.executable, str(SKILL / "scripts" / "capability_graph.py"), "build", "--check"],
                               capture_output=True, text=True, timeout=180)
        self.assertEqual(check.returncode, 0, check.stderr)

    def test_every_family_hangs_off_a_domain(self):
        fams = {n["id"] for n in self.g["nodes"] if n["kind"] == "family"}
        linked = {e["to"] for e in self.g["edges"] if e["rel"] == "has" and e["from"].startswith("dom:")}
        self.assertEqual(fams, linked)
        self.assertEqual(len(fams), len(list((SKILL / "data" / "powers").glob("*.json"))))

    def test_script_and_test_nodes_exist_on_disk(self):
        for n in self.g["nodes"]:
            if n["kind"] == "script":
                self.assertTrue((SKILL / n["label"]).exists(), n["label"])
            if n["kind"] == "test":
                self.assertTrue((ROOT / n["label"]).exists() or (SKILL / "evals" / n["label"]).exists(), n["label"])

    def test_graphify_layer_is_cross_checked(self):
        self.assertGreaterEqual(self.g["graphify_import_edges_confirmed_locally"], 1)
        self.assertTrue(self.g["graphify"]["commit"])

    def test_html_is_offline(self):
        html = (self.out / "capability-graph.html").read_text(encoding="utf-8")
        self.assertNotIn("<script src=", html)
        self.assertIn("prefers-color-scheme", html)


if __name__ == "__main__":
    unittest.main()
