"""Tests for the Black Dragon repo fusion registry and its stdlib-only native modules."""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".claude/skills/kosif-black-dragon"
SCRIPTS = SKILL / "scripts"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


rf = _load("bd_repo_fusion", SCRIPTS / "repo_fusion.py")


class RepoFusionData(unittest.TestCase):
    def setUp(self):
        self.data = rf.load()

    def test_counts_and_schema(self):
        repos = self.data["repos"]
        self.assertEqual(len(repos), 10)
        caps = [c for r in repos for c in r["capabilities"]]
        self.assertEqual(len(caps), 101)
        self.assertEqual(sum(c["status"] == "native-implemented" for c in caps), 47)
        ids = [c["id"] for c in caps]
        self.assertEqual(len(ids), len(set(ids)), "capability ids must be unique")
        for c in caps:
            self.assertIn(c["status"], ("source-linked", "native-implemented"))
            self.assertIn(c["dragon_stage"], rf.STAGES)

    def test_every_repo_has_report_and_module_file(self):
        for r in self.data["repos"]:
            self.assertTrue((SKILL / r["report"]).is_file(), r["report"])
            self.assertIn("@", r["verified_from"])
            if r["module"]:
                self.assertTrue((SCRIPTS / "fusion" / r["module"]).is_file(), r["module"])
            else:
                self.assertFalse(any(c["status"] == "native-implemented" for c in r["capabilities"]))
        self.assertEqual(len(self.data["modules"]), 9)

    def test_no_personal_paths_in_fusion(self):
        for p in list((SCRIPTS / "fusion").glob("*.py")) + [SKILL / "data/repo_fusion.json"]:
            text = p.read_text(encoding="utf-8")
            self.assertNotIn("C:\\Users\\cinde", text, p.name)
            self.assertNotIn("C:/Users/cinde", text, p.name)

    def test_find_arabic_and_english(self):
        hits = rf.find(self.data, "تقسيم الأغنية دروب")
        self.assertTrue(hits and hits[0]["repo"] == "librosa/librosa")
        hits = rf.find(self.data, "jianying draft", stage="deliver")
        self.assertTrue(hits and all(h["dragon_stage"] == "deliver" for h in hits))
        self.assertEqual(rf.find(self.data, "zzzz-no-such-thing"), [])

    def test_show(self):
        self.assertEqual(rf.show(self.data, "pixelfx")["license"], "MIT")
        self.assertIsNone(rf.show(self.data, "nope"))

    def test_prompt_index_has_no_prompt_text(self):
        idx = json.loads((SKILL / "data/opus_video_cases_index.json").read_text(encoding="utf-8"))
        self.assertEqual(len(idx["items"]), 703)
        self.assertFalse(any("prompt" in x for x in idx["items"]))


class StdlibModuleSelfTests(unittest.TestCase):
    """Run the self-tests of the modules that need only the standard library."""

    def _run(self, name):
        res = rf.run_self_tests(rf.load(), name)
        self.assertEqual(len(res), 1)
        self.assertTrue(res[0]["ok"], res[0]["tail"])

    def test_promptlib(self):
        self._run("promptlib")

    def test_rapier_bake(self):
        self._run("rapier_bake")

    @unittest.skipUnless(shutil.which("node"), "node not installed")
    def test_three(self):
        self._run("three")


class MediaHunter(unittest.TestCase):
    MH = SKILL / "tools/media_hunter/mh.py"

    def test_files_and_offline_sites(self):
        self.assertTrue((SKILL / "tools/media_hunter/data/media_sites_615.csv").is_file())
        self.assertFalse((SKILL / "tools/media_hunter/keys.json").exists())
        try:
            import httpx  # noqa: F401
        except ImportError:
            self.skipTest("httpx not installed")
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ, MH_CACHE=tmp, MH_OUT=tmp)
            out = subprocess.run([sys.executable, "-I", str(self.MH), "sites", "camel desert", "--json"],
                                 capture_output=True, text=True, encoding="utf-8", env=env, timeout=120)
            self.assertEqual(out.returncode, 0, out.stderr[-500:])
            sites = json.loads(out.stdout)
            self.assertGreater(len(sites), 5)
            self.assertTrue(all(s["url"].startswith("http") for s in sites))


if __name__ == "__main__":
    unittest.main()
