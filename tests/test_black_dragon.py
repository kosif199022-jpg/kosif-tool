"""Black Dragon tests: full inventory coverage, truthful parallel adapter execution, safety."""
import importlib.util
import json
import subprocess
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

    def test_every_entry_gets_a_brief_line_and_assignment(self):
        result = dragon.run("montage video", self.job, {}, workers=2,
                            allow_execution=False, timeout=5, entries=self.inventory)
        self.assertEqual(result["assigned"], 4)
        self.assertTrue(result["assignment_complete"])
        lines = [json.loads(x) for x in (self.job / "briefs.jsonl").read_text().splitlines()]
        self.assertEqual({x["entry"] for x in lines}, set(self.inventory))
        self.assertTrue(all(x["part"] and x["mode"] and x["application"] for x in lines))
        ledger = json.loads((self.job / "all_skills_ledger.json").read_text())
        for item in ledger["items"].values():
            self.assertEqual(len(item["assignment"]["brief_sha256"]), 64)
            self.assertEqual(item["status"], "blocked")  # assigned is never "executed"
        self.assertIn("Black Dragon", (self.job / "black_dragon_report.md").read_text())

    def test_failing_adapter_is_failed_and_dependents_blocked(self):
        (self.root / "scripts" / "bad.py").write_text("import sys\nsys.exit(3)\n")
        adapters = {"power:THINK-A": {"script": "scripts/bad.py", "args": []},
                    "tool:render": dict(self.adapter(), depends_on=["power:THINK-A"])}
        result = dragon.run("x", self.job, adapters, workers=2,
                            allow_execution=True, timeout=5, entries=self.inventory)
        ledger = dragon.audit.load(self.job, self.inventory)
        self.assertEqual(ledger["items"]["power:THINK-A"]["status"], "failed")
        self.assertEqual(ledger["items"]["tool:render"]["status"], "blocked")
        self.assertIn("Prerequisites", ledger["items"]["tool:render"]["reason"])
        self.assertEqual(result["executed"], 0)


class FullInventoryTests(unittest.TestCase):
    """The real repository inventory: every capability type, no duplicates."""

    @classmethod
    def setUpClass(cls):
        cls.entries = dragon.full_inventory()

    def test_every_kind_is_present(self):
        kinds = {v["kind"] for v in self.entries.values()}
        self.assertEqual(kinds, {"skill", "power", "tool", "superpower", "style", "playbook", "protocol"})
        base = dragon.audit.catalog()
        self.assertTrue(set(base) <= set(self.entries))

    def test_counts_match_their_sources(self):
        skill = dragon.audit.SKILL
        tools = json.loads((skill / "data/tools.json").read_text(encoding="utf-8"))["tools"]
        sps = json.loads((skill / "data/superpowers.json").read_text(encoding="utf-8"))["items"]
        styles = json.loads((ROOT / "catalog/styles.json").read_text(encoding="utf-8"))
        count = lambda k: sum(1 for v in self.entries.values() if v["kind"] == k)
        self.assertEqual(count("tool"), len(tools))
        self.assertEqual(count("superpower"), len(sps))
        self.assertEqual(count("style"), len(styles))
        self.assertEqual(count("playbook"), len(list((ROOT / "playbooks").glob("*.md"))))

    def test_brain_assigns_every_real_entry(self):
        plan = dragon.brain.plan("اعمل مونتاج فيديو بصوت", self.entries, {},
                                 skill_root=dragon.audit.SKILL)
        self.assertEqual(plan["assigned"], len(self.entries))
        self.assertEqual(plan["selected_out"], 0)
        self.assertEqual(sum(p["assigned"] for p in plan["parts"].values()), len(self.entries))
        self.assertEqual(sum(plan["modes"].values()), len(self.entries))
        self.assertTrue(any(p["leads"] for p in plan["parts"].values()))

    def test_reviewed_adapters_point_at_real_entries_and_scripts(self):
        adapters = dragon._load_adapters(dragon.REVIEWED_ADAPTERS)
        self.assertGreaterEqual(len(adapters), 20)
        for key, spec in adapters.items():
            self.assertIn(key, self.entries)
            self.assertTrue(dragon._safe_script(spec["script"]).is_file())
            tool = spec["args"][1]
            self.assertTrue((ROOT / tool).is_file(), tool)
            self.assertEqual(spec["args"][0], "{artifact}")


class RealExecutionTests(unittest.TestCase):
    """Integration: real repo tools run through reviewed adapters with verified receipts."""

    def test_reviewed_adapters_execute_with_receipts_on_full_inventory(self):
        adapters = dragon._load_adapters(dragon.REVIEWED_ADAPTERS)
        keep = {k: adapters[k] for k in ("tool:export-profile", "tool:agent-guard", "tool:micro-index")}
        with tempfile.TemporaryDirectory() as tmp:
            job = Path(tmp) / "job"
            result = dragon.run("مونتاج ريلز", job, keep, workers=3, allow_execution=True,
                                timeout=120, probe_tools=False)
            self.assertEqual(result["executed"], 3, result)
            self.assertEqual(result["failed"], 0)
            self.assertEqual(result["assigned"], result["scheduled"])
            self.assertFalse(result["full_coverage"])
            ledger = json.loads((job / "all_skills_ledger.json").read_text())
            for key in keep:
                receipt = ledger["items"][key]["receipt"]
                artifact = Path(receipt["artifact"])
                self.assertGreater(artifact.stat().st_size, 0)
                self.assertEqual(dragon.audit.sha256(artifact), receipt["artifact_sha256"])

    def test_exec_wrapper_keeps_the_tool_exit_code(self):
        wrapper = SCRIPTS / "_black_dragon_exec.py"
        with tempfile.TemporaryDirectory() as tmp:
            art = Path(tmp) / "a.txt"
            bad = subprocess.run([sys.executable, str(wrapper), str(art), "../x.py"],
                                 capture_output=True, text=True)
            self.assertEqual(bad.returncode, 2)
            ok = subprocess.run([sys.executable, str(wrapper), str(art),
                                 ".claude/skills/kosif-superpowers/scripts/export_profile.py"],
                                capture_output=True, text=True)
            self.assertEqual(ok.returncode, 0, ok.stderr)
            self.assertGreater(art.stat().st_size, 0)

    def test_probe_runs_help_only_for_argparse_cli_tools(self):
        with tempfile.TemporaryDirectory() as tmp:
            job = Path(tmp)
            record = {"id": "micro-index", "kind": "cli", "root": "skill",
                      "path": "scripts/micro_index.py", "safety": "read-only"}
            probe = dragon._probe("tool:micro-index", record, job)
            self.assertEqual(probe["status"], "passed", probe)
            self.assertEqual(probe["command"][-1], "--help")
            self.assertEqual(dragon._probe("tool:x", dict(record, kind="library"), job)["status"],
                             "not-probeable")
            self.assertEqual(dragon._probe("tool:x", None, job)["status"], "not-probeable")


if __name__ == "__main__":
    unittest.main()
