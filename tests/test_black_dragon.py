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

    def test_method_applier_receipts_are_applied_not_executed(self):
        # A generic applier that writes a procedure for every card must not inflate "executed".
        applier = self.root / ".claude/skills/kosif-dragon-mind/scripts"
        applier.mkdir(parents=True)
        (applier / "card_apply.py").write_text(
            "import pathlib,sys\npathlib.Path(sys.argv[1]).write_text('procedure for ' + sys.argv[2])\n",
            encoding="utf-8")
        card = {"script": ".claude/skills/kosif-dragon-mind/scripts/card_apply.py", "args": ["{artifact}", "{task}"]}
        adapters = {k: dict(card) for k in self.inventory if k != "tool:render"}
        adapters["power:RENDER-A"]["script"] = "scripts/safe_adapter.py"
        adapters["power:RENDER-A"]["method_applier"] = True  # the explicit flag works for any script too
        adapters["tool:render"] = self.adapter()
        result = dragon.run("apply all", self.job, adapters, workers=4,
                            allow_execution=True, timeout=5, entries=self.inventory)
        self.assertEqual(result["executed"], 1)
        self.assertEqual(result["applied"], 3)
        self.assertEqual(result["blocked_why"]["method_applied"], 3)
        self.assertEqual(sum(result["blocked_why"].values()), result["blocked"])
        self.assertFalse(result["full_coverage"])
        ledger = dragon.audit.load(self.job, self.inventory)
        for key in ("skill:editor", "power:THINK-A", "power:RENDER-A"):
            self.assertNotEqual(ledger["items"][key]["status"], "executed")
            self.assertTrue(Path(ledger["items"][key]["applied_receipt"]["receipt_path"]).is_file())
        self.assertFalse(dragon.audit.report(self.job, self.inventory)["fully_executed"])

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

    def test_diagnosis_separates_knowledge_from_executable_tools(self):
        result = dragon.run("diagnose", self.job, {}, workers=2,
                            allow_execution=False, timeout=5, entries=self.inventory)
        readiness = result["adapter_readiness"]
        self.assertEqual(readiness["catalog_entries"], 4)
        self.assertEqual(readiness["catalog_tools"], 1)
        self.assertEqual(readiness["tools_missing_reviewed_adapter"], 1)
        self.assertEqual(readiness["knowledge_entries_without_adapter"], 3)
        self.assertFalse(result["reviewed_execution_complete"])
        ledger = json.loads((self.job / "all_skills_ledger.json").read_text())
        self.assertIn("Tool has no reviewed", ledger["items"]["tool:render"]["reason"])
        self.assertIn("Knowledge-only", ledger["items"]["skill:editor"]["reason"])

    def test_approved_adapter_completion_does_not_claim_whole_catalog(self):
        result = dragon.run("selective", self.job, {"tool:render": self.adapter()},
                            workers=2, allow_execution=True, timeout=5,
                            entries=self.inventory)
        self.assertTrue(result["reviewed_execution_complete"])
        self.assertEqual(result["registered_tool_executed"], 1)
        self.assertEqual(result["adapter_readiness"]["reviewed_tool_adapters"], 1)
        self.assertEqual(result["adapter_readiness"]["knowledge_entries_without_adapter"], 3)
        self.assertFalse(result["full_coverage"])


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


    def test_real_full_tool_activation_cli(self):
        """Production catalog is inspected without executing its programs."""
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "full-tools.json"
            completed = subprocess.run([
                sys.executable, str(SCRIPTS / "black_dragon.py"), "activate",
                "اعمل فيديو موشن", "--selection", "all", "--out", str(output),
            ], cwd=ROOT, capture_output=True, text=True, timeout=120)
            self.assertEqual(completed.returncode, 0, completed.stderr[-1600:])
            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(report["status"], "planned_not_executed")
            self.assertEqual(report["catalog"]["examined"], len(self.entries))
            self.assertEqual(report["catalog"]["assigned"], len(self.entries))
            self.assertEqual(report["counts"]["catalog_tools"],
                             sum(x["kind"] == "tool" for x in self.entries.values()))
            self.assertEqual(len(report["tools"]), report["counts"]["catalog_tools"])
            self.assertGreater(report["counts"]["statically_inspected"], 0)
            self.assertEqual(report["counts"]["execution_attempts"], 0)
            self.assertFalse(report["approval_gate"]["approved"])
            self.assertEqual(len(report["council"]["members"]), 5)

    def test_default_cli_registry_is_reviewed_but_does_not_auto_execute(self):
        built_in = dragon._cli_adapters(None)
        self.assertGreaterEqual(len(built_in), 20)
        self.assertEqual(built_in, dragon._load_adapters(dragon.REVIEWED_ADAPTERS))
        with tempfile.TemporaryDirectory() as tmp:
            custom = Path(tmp) / "custom.json"
            custom.write_text('{"adapters": {}}', encoding="utf-8")
            self.assertEqual(dragon._cli_adapters(custom), {})

    def test_doctor_reports_missing_adapters_without_fake_success(self):
        completed = subprocess.run(
            [sys.executable, str(SCRIPTS / "black_dragon.py"), "doctor"],
            cwd=ROOT, capture_output=True, text=True, timeout=120)
        self.assertEqual(completed.returncode, 0, completed.stderr[-1600:])
        diagnosis = json.loads(completed.stdout)
        self.assertGreater(diagnosis["catalog_entries"], 1000)
        self.assertGreater(diagnosis["catalog_tools"], 0)
        self.assertEqual(diagnosis["unknown_adapters"], [])
        self.assertEqual(diagnosis["invalid_adapter_scripts"], {})
        self.assertGreater(diagnosis["tools_missing_reviewed_adapter"], 0)
        self.assertGreater(diagnosis["knowledge_entries_without_adapter"], 0)

    def test_reviewed_adapters_point_at_real_entries_and_scripts(self):
        adapters = dragon._load_adapters(dragon.REVIEWED_ADAPTERS)
        self.assertGreaterEqual(len(adapters), 20)
        for key, spec in adapters.items():
            self.assertIn(key, self.entries)
            self.assertTrue(dragon._safe_script(spec["script"]).is_file())
            if spec.get("skill_program"):  # skill adapters: RECIPE {artifact} --task={task} [--media={media}]
                self.assertTrue(spec["script"].endswith("_black_dragon_skill.py"), key)
                self.assertEqual(spec["args"][1:3], ["{artifact}", "--task={task}"], key)
                continue
            if spec.get("tool_suite"):  # tool adapters: TOOL_ID {artifact} --task={task}
                self.assertTrue(spec["script"].endswith("_black_dragon_tool.py"), key)
                self.assertEqual(spec["args"][1:], ["{artifact}", "--task={task}"], key)
                self.assertEqual(key, "tool:" + spec["args"][0])
                continue
            if spec.get("media"):  # media adapters: RECIPE {artifact} --media={media}
                self.assertTrue(spec["script"].endswith("_black_dragon_media.py"), key)
                self.assertEqual(spec["args"][1:], ["{artifact}", "--media={media}"], key)
                continue
            if spec.get("style_render"):  # style adapters: STYLE_ID {artifact} --task={task}
                self.assertTrue(spec["script"].endswith("_black_dragon_style.py"), key)
                self.assertEqual(spec["args"][1:], ["{artifact}", "--task={task}"], key)
                self.assertEqual(key, "style:" + spec["args"][0])
                continue
            if spec.get("power_proof"):  # power adapters: power:ID {artifact} --task={task}
                self.assertTrue(spec["script"].endswith("_black_dragon_power.py"), key)
                self.assertEqual(spec["args"], [key, "{artifact}", "--task={task}"], key)
                continue
            if spec.get("power_program"):  # power programs: ID {artifact} --task={task}
                self.assertTrue(spec["script"].endswith("_black_dragon_power_program.py"), key)
                self.assertEqual(spec["args"], [key.split(":", 1)[1], "{artifact}", "--task={task}"], key)
                continue
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

    def test_probe_staticaly_discovers_cli_without_executing_help(self):
        with tempfile.TemporaryDirectory() as tmp:
            job = Path(tmp)
            record = {"id": "micro-index", "kind": "cli", "root": "skill",
                      "path": "scripts/micro_index.py", "safety": "read-only"}
            probe = dragon._probe("tool:micro-index", record, job)
            self.assertEqual(probe["status"], "static-only", probe)
            self.assertNotIn("command", probe)
            self.assertEqual(json.loads(Path(probe["output"]).read_text())["executed"], False)
            self.assertEqual(dragon._probe("tool:x", dict(record, kind="library"), job)["status"],
                             "not-probeable")
            self.assertEqual(dragon._probe("tool:x", None, job)["status"], "not-probeable")


if __name__ == "__main__":
    unittest.main()


class GeneratedRegistryMergeTests(unittest.TestCase):
    def test_generated_files_add_entries_and_reviewed_wins(self):
        with tempfile.TemporaryDirectory() as tmp:
            reviewed = Path(tmp) / "black_dragon_adapters.json"
            reviewed.write_text(json.dumps({"adapters": {"a": {"script": "r.py", "args": []}}}))
            (Path(tmp) / "black_dragon_adapters_powers.json").write_text(json.dumps(
                {"adapters": {"a": {"script": "gen.py", "args": []}, "b": {"script": "gen.py", "args": []}}}))
            old = dragon.REVIEWED_ADAPTERS
            dragon.REVIEWED_ADAPTERS = reviewed
            try:
                merged = dragon._load_adapters(reviewed)
            finally:
                dragon.REVIEWED_ADAPTERS = old
            self.assertEqual(merged["a"]["script"], "r.py")
            self.assertEqual(merged["b"]["script"], "gen.py")
            # A custom path is loaded alone, without generated files.
            self.assertEqual(set(dragon._load_adapters(Path(tmp) / "black_dragon_adapters_powers.json")), {"a", "b"})
