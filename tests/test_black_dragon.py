"""Black Dragon tests: full inventory coverage, truthful parallel adapter execution, safety."""
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".claude/skills/kosif-superpowers/scripts"
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location("black_dragon", SCRIPTS / "black_dragon.py")
dragon = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dragon)


class BlackDragonTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.old_repo = dragon.REPO
        dragon.REPO = self.root
        self.addCleanup(setattr, dragon, "REPO", self.old_repo)
        (self.root / "scripts").mkdir()
        self.job = self.root / "out" / "dragon"
        self.inventory = {
            "skill:editor": {"kind": "skill", "source": "editor/SKILL.md"},
            "power:THINK-A": {"kind": "power", "source": "powers.json"},
            "power:RENDER-A": {"kind": "power", "source": "powers.json"},
            "tool:render": {"kind": "tool", "source": "tools.json"},
        }
        (self.root / "scripts" / "safe_adapter.py").write_text(
            "import pathlib,sys\n"
            "pathlib.Path(sys.argv[1]).write_text('real output: ' + sys.argv[2])\n",
            encoding="utf-8",
        )

    def adapter(self):
        return {"script": "scripts/safe_adapter.py",
                "args": ["{artifact}", "{task}"]}

    def test_all_items_dispatched_even_with_no_adapters(self):
        result = dragon.run("full test", self.job, {}, workers=4,
                            allow_execution=False, timeout=5, entries=self.inventory)
        self.assertEqual(result["scheduled"], 4)
        self.assertEqual(result["blocked"], 4)
        self.assertFalse(result["full_coverage"])
        ledger = json.loads((self.job / "all_skills_ledger.json").read_text())
        self.assertEqual(set(ledger["items"]), set(self.inventory))
        self.assertTrue(all(x["attempts"] == 1 for x in ledger["items"].values()))

    def test_registered_adapters_require_explicit_execute_flag(self):
        adapters = {key: self.adapter() for key in self.inventory}
        result = dragon.run("test", self.job, adapters, workers=4,
                            allow_execution=False, timeout=5, entries=self.inventory)
        self.assertEqual(result["executed"], 0)
        self.assertEqual(result["blocked"], 4)
        self.assertEqual(list((self.job / "artifacts").iterdir()), [])

    def test_every_real_adapter_runs_and_has_verified_receipt(self):
        adapters = {key: self.adapter() for key in self.inventory}
        result = dragon.run("all at once", self.job, adapters, workers=4,
                            allow_execution=True, timeout=5, entries=self.inventory)
        self.assertEqual(result["executed"], 4)
        self.assertEqual(result["failed"], 0)
        self.assertTrue(result["full_coverage"])
        ledger = dragon.audit.load(self.job, self.inventory)
        self.assertTrue(all(x["status"] == "executed" for x in ledger["items"].values()))
        for key in self.inventory:
            self.assertEqual(ledger["items"][key]["receipt"]["command"][0], sys.executable)
        self.assertTrue(dragon.audit.report(self.job, self.inventory)["fully_executed"])

    def test_unregistered_entries_prevent_full_coverage(self):
        adapters = {"tool:render": self.adapter()}
        result = dragon.run("partial", self.job, adapters, workers=8,
                            allow_execution=True, timeout=5, entries=self.inventory)
        self.assertEqual(result["executed"], 1)
        self.assertEqual(result["blocked"], 3)
        self.assertFalse(result["full_coverage"])

    def test_invalid_adapter_script_fails_not_silent_success(self):
        adapters = {"tool:render": {"script": "../unsafe.py", "args": []}}
        result = dragon.run("unsafe", self.job, adapters, workers=2,
                            allow_execution=True, timeout=5, entries=self.inventory)
        self.assertEqual(result["failed"], 1)
        self.assertEqual(result["blocked"], 3)

    def test_unknown_adapter_rejected_before_initializing(self):
        with self.assertRaisesRegex(ValueError, "Unknown adapter"):
            dragon.run("unknown", self.job, {"tool:not-known": self.adapter()},
                       workers=2, allow_execution=True, timeout=5, entries=self.inventory)
        self.assertFalse(self.job.exists())

    def test_reject_overwrite_and_bad_parallelism(self):
        dragon.run("once", self.job, {}, workers=1,
                   allow_execution=False, timeout=5, entries=self.inventory)
        with self.assertRaises(ValueError):
            dragon.run("again", self.job, {}, workers=1,
                       allow_execution=False, timeout=5, entries=self.inventory)
        with self.assertRaises(ValueError):
            dragon.run("invalid", self.root / "out" / "other", {}, workers=0,
                       allow_execution=False, timeout=5, entries=self.inventory)
        with self.assertRaises(ValueError):
            dragon.run("invalid", self.root / "out" / "other", {}, workers=1000,
                       allow_execution=False, timeout=5, entries=self.inventory)


if __name__ == "__main__":
    unittest.main()
