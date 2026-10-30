#!/usr/bin/env python3
"""Tests for scripts/fusionforge_hub_runner.py (FusionForge recipe -> hub.py run bridge).

Most tests use a fake hub.py and a fake fusionforge.py in a temporary folder that log their arguments, so they
check ordering, fail-closed stops, approvals and receipts without running real tools. Two integration tests use
the real hub.py and fusionforge.py: one runs four real read-only tools of a fixture recipe and checks the
recipe's traces; one checks that a registry other than hub.py's own is refused.
Run: python3 -m unittest discover -s .claude/skills/kosif-superpowers/evals -p 'test_fusionforge_hub_runner.py' -v
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
SCRIPT = SKILL / "scripts" / "fusionforge_hub_runner.py"
REAL_HUB = SKILL / "scripts" / "hub.py"
REAL_FF = SKILL / "scripts" / "fusionforge.py"

FAKE_HUB = '''import json, sys, time, subprocess
from pathlib import Path
args = sys.argv[1:]
here = Path(__file__)
if args[:1] == ["doctor"]:  # readiness, as hub.py doctor --json reports it
    states = json.loads(here.with_suffix(".states").read_text()) if here.with_suffix(".states").exists() else {}
    print(json.dumps({"tools": [{"id": t, "state": s, "missing": [] if s == "ready" else ["bin:x"]}
                                for t, s in {"alpha": "ready", "beta": "ready", **states}.items()]}))
    sys.exit(0)
with here.with_suffix(".calls").open("a") as f:
    f.write(" ".join(args) + "\\n")
tool_args = args[args.index("--") + 1:]
if "--fail" in tool_args:
    sys.exit(5)
if "--slow" in tool_args:
    time.sleep(5)
if "--orphan" in tool_args:  # like hub.py: the tool is a child process
    marker = tool_args[tool_args.index("--orphan") + 1]
    subprocess.call([sys.executable, "-c", "import time,sys; time.sleep(2); open(sys.argv[1],'w').write('x')", marker])
if "--write" in tool_args:  # --write PATH TEXT
    i = tool_args.index("--write")
    Path(tool_args[i + 1]).write_text(tool_args[i + 2])
sys.exit(0)
'''
FAKE_FF = '''import json, sys
from pathlib import Path
here = Path(__file__)
args = sys.argv[1:]
if "show" in args:
    print(json.dumps({"recipe": json.loads((here.parent / "recipe.json").read_text())}))
    sys.exit(0)
with here.with_suffix(".calls").open("a") as f:
    f.write(" ".join(args) + "\\n")
if here.with_suffix(".mode").exists():
    print("fusionforge: error: NODE_NOT_IN_PLAN: the trace was refused", file=sys.stderr)
    sys.exit(2)
sys.exit(0)
'''


class Base(unittest.TestCase):
    def setUp(self):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        self.base = Path(d.name).resolve()
        self.recipe, self.registry = self.base / "recipe.json", self.base / "tools.json"
        self.hub, self.ff = self.base / "hub.py", self.base / "forge.py"
        self.hub.write_text(FAKE_HUB, encoding="utf-8")
        self.ff.write_text(FAKE_FF, encoding="utf-8")
        self.n = 0
        self.data = {
            "schema": "kosif.fusionforge.recipe.v2", "id": "FUSE-20261030-abcde12345", "project": "sample",
            "status": "planned", "plan_choice": {"plan": "A", "nodes": ["N01", "N02"]},
            "plans": {"A": {"nodes": ["N01", "N02"]}},
            "nodes": [{"id": "N01", "stage": "build", "status": "pending", "executor": {"ref": "tool:alpha"}},
                      {"id": "N02", "stage": "verify", "status": "pending", "executor": {"ref": "tool:beta"}}],
            "edges": [{"id": "E01", "from": "N01", "to": "N02", "kind": "code", "relation": "sequence"}]}
        self.tools = {"tools": [{"id": "alpha", "kind": "cli", "safety": "read-only", "consent": ""},
                                {"id": "beta", "kind": "cli", "safety": "writes-files", "consent": ""}]}

    def calls(self, p):
        f = p.with_suffix(".calls")
        return f.read_text().splitlines() if f.exists() else []

    def runs(self):
        return [c for c in self.calls(self.hub) if c.startswith("run ")]

    def invoke(self, *, execute=False, extra=(), plan=None, report=None):
        self.n += 1
        report = report or self.base / "out" / f"receipt-{self.n}.json"
        self.recipe.write_text(json.dumps(self.data), encoding="utf-8")
        self.registry.write_text(json.dumps(self.tools), encoding="utf-8")
        cmd = [sys.executable, str(SCRIPT), "--recipe", str(self.recipe), "--registry", str(self.registry),
               "--hub", str(self.hub), "--fusionforge", str(self.ff), "--report", str(report)]
        cmd += ["--execute"] if execute else []
        if plan is not None:
            p = self.base / f"plan-{self.n}.json"
            p.write_text(json.dumps(plan), encoding="utf-8")
            cmd += ["--plan-file", str(p)]
        proc = subprocess.run(cmd + list(extra), text=True, capture_output=True, timeout=60, cwd=str(self.base))
        self.assertNotIn("Traceback", proc.stderr)
        return proc, json.loads(Path(report).read_text(encoding="utf-8"))


class BridgeTests(Base):
    def test_dry_run_launches_nothing(self):
        proc, r = self.invoke()
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(r["status"], "DRY_RUN_READY")
        self.assertEqual([n["status"] for n in r["nodes"]], ["READY", "READY"])
        self.assertEqual(self.runs(), [])
        self.assertEqual(self.calls(self.ff), [])

    def test_runs_in_edge_order_and_traces_every_node(self):
        self.data["plan_choice"]["nodes"] = self.data["plans"]["A"]["nodes"] = ["N02", "N01"]  # listed backwards
        proc, r = self.invoke(execute=True, plan={"N01": ["--in", "a b.json"]})
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(r["status"], "EXECUTED")
        self.assertEqual([n["node"] for n in r["nodes"]], ["N01", "N02"])
        self.assertEqual(self.runs(), ["run alpha -- --in a b.json", "run beta --"])
        tr = self.calls(self.ff)
        self.assertEqual(len(tr), 2)
        self.assertIn("--node N01", tr[0])
        self.assertIn("--result passed", tr[0])
        self.assertIn("--tools-file " + str(self.registry), tr[0])
        self.assertTrue((self.base / "out" / "receipt-1.N01.json").is_file())
        self.assertEqual(len(r["nodes"][0]["execution"]["stdout_sha256"]), 64)
        self.assertFalse(r["schema"].startswith("kosif.fusionforge."))  # fusionforge refuses its own records as evidence

    def test_fusionforge_node_ids_like_u1_c1_v1(self):
        ren = {"N01": "C1", "N02": "V1"}
        for n in self.data["nodes"]:
            n["id"] = ren[n["id"]]
        self.data["plan_choice"]["nodes"] = self.data["plans"]["A"]["nodes"] = ["C1", "V1"]
        self.data["edges"] = [{"from": "C1", "to": "V1", "relation": "verify"}]
        proc, r = self.invoke(execute=True, plan={"C1": ["x"]})
        self.assertEqual(proc.returncode, 0, r)
        self.assertEqual([n["node"] for n in r["nodes"]], ["C1", "V1"])

    def test_failure_stops_the_chain_and_is_traced(self):
        proc, r = self.invoke(execute=True, plan={"N01": ["--fail"]})
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(r["status"], "FAILED")
        self.assertEqual((r["covered_nodes"], r["selected_nodes"]), (1, 2))
        self.assertEqual(r["nodes"][0]["execution"]["returncode"], 5)
        self.assertEqual(len(self.runs()), 1)
        self.assertIn("--result failed", self.calls(self.ff)[0])
        self.assertIn("--error-class tool_error", self.calls(self.ff)[0])

    def test_trace_is_mandatory(self):
        self.ff.with_suffix(".mode").write_text("refuse")
        proc, r = self.invoke(execute=True)
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(r["nodes"][0]["status"], "FAIL")
        self.assertIn("NODE_NOT_IN_PLAN", r["nodes"][0]["fusionforge_trace"]["error_line"])
        self.assertEqual(len(self.runs()), 1)  # the next node never runs on an unrecorded result

    def test_outputs_are_passed_downstream_and_checked(self):
        out1, out2 = self.base / "w" / "a.json", self.base / "w" / "b.txt"
        plan = {"N01": {"args": ["--write", "{out.data}", '{"ok": true}'], "outputs": {"data": str(out1)}, "make_dirs": [str(out1.parent)]},
                "N02": {"args": ["--src", "{N01.data}", "--write", "{out.rep}", "fine"], "outputs": {"rep": str(out2)}}}
        proc, r = self.invoke(execute=True, plan=plan)
        self.assertEqual(proc.returncode, 0, r)
        self.assertEqual(self.runs()[1], f"run beta -- --src {out1} --write {out2} fine")
        self.assertEqual(r["nodes"][0]["outputs"]["data"]["bytes"], len('{"ok": true}'))
        self.assertIn("--output data=", self.calls(self.ff)[0])

    def test_missing_empty_or_broken_output_fails_and_is_quarantined(self):
        out1 = self.base / "a.json"
        for args, code in ((["x"], "OUTPUT_MISSING"), (["--write", str(out1), ""], "OUTPUT_EMPTY"),
                           (["--write", str(out1), "{broken"], "OUTPUT_INVALID_JSON")):
            proc, r = self.invoke(execute=True, plan={"N01": {"args": args, "outputs": {"data": str(out1)}}})
            self.assertEqual((proc.returncode, r["nodes"][0]["status"]), (1, "FAIL"), code)
            self.assertIn(code, r["nodes"][0]["reason"])
            self.assertFalse(out1.exists(), "a failed node's output must not stay where the next node reads it")
            self.assertEqual(len(r["nodes"]), 1)
        self.assertTrue(any((self.base / "out").glob("*.quarantine/N01/a.json")))

    def test_existing_output_is_never_overwritten(self):
        out1 = self.base / "a.json"
        out1.write_text("{}")
        proc, r = self.invoke(execute=True, plan={"N01": {"args": [], "outputs": {"data": str(out1)}}})
        self.assertEqual(proc.returncode, 2)
        self.assertIn("already exist", r["nodes"][0]["reason"])
        self.assertEqual(self.runs(), [])

    def test_missing_input_blocks(self):
        proc, r = self.invoke(execute=True, plan={"N01": {"inputs": [str(self.base / "nope.wav")]}})
        self.assertEqual(proc.returncode, 2)
        self.assertIn("input files missing", r["nodes"][0]["reason"])
        self.assertEqual(self.runs(), [])

    def test_plan_file_references_are_checked_up_front(self):
        for bad in ({"N01": "--in x"}, {"N01": [1]}, {"N09": ["x"]}, ["N01"], {"N01": {"args": [], "extra": 1}},
                    {"N01": {"args": ["{N02.rep}"]}, "N02": {"outputs": {"rep": "r.txt"}}},  # N02 runs after N01
                    {"N02": {"args": ["{N01.nothing}"]}}, {"N01": {"args": ["{out.x}"]}},
                    {"N01": {"outputs": {"a": "same.txt"}}, "N02": {"outputs": {"b": "same.txt"}}},
                    {"N01": {"outputs": {"a": "/etc/passwd-copy"}}}):
            proc, r = self.invoke(execute=True, plan=bad)
            self.assertEqual((proc.returncode, r["status"]), (2, "BLOCKED"), bad)
        self.assertEqual(self.runs(), [])

    def test_network_needs_explicit_flag(self):
        self.tools["tools"][0]["safety"] = "network"
        proc, r = self.invoke(execute=True)
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(r["nodes"][0]["status"], "BLOCKED")
        self.assertEqual(self.runs(), [])
        self.assertIn("BLOCKED: network", self.calls(self.ff)[0])  # the block itself is noted in the recipe
        self.assertNotIn("--result", self.calls(self.ff)[0])
        proc, r = self.invoke(execute=True, extra=["--allow-network"])
        self.assertEqual(proc.returncode, 0, r)
        self.assertEqual(self.runs()[0], "run --yes alpha --")

    def test_requires_network_flag_counts_too(self):
        self.tools["tools"][1]["requires"] = {"network": True}
        proc, r = self.invoke(execute=True)
        self.assertEqual(proc.returncode, 2)
        self.assertEqual([n["status"] for n in r["nodes"]], ["PASS", "BLOCKED"])

    def test_external_and_consent_need_their_own_flags(self):
        self.tools["tools"][0]["safety"] = "runs-external-programs"
        proc, r = self.invoke(execute=True, extra=["--allow-network", "--allow-consent"])
        self.assertEqual(proc.returncode, 2)
        self.assertIn("--allow-external", r["nodes"][0]["reason"])
        self.tools["tools"][0].update(safety="read-only", consent="uploads to a third-party site")
        proc, r = self.invoke(execute=True, extra=["--allow-network", "--allow-external"])
        self.assertEqual(proc.returncode, 2)
        self.assertIn("consent", r["nodes"][0]["reason"])
        proc, r = self.invoke(execute=True, extra=["--allow-consent"])
        self.assertEqual(proc.returncode, 0, r)

    def test_tool_not_ready_blocks(self):
        self.hub.with_suffix(".states").write_text(json.dumps({"alpha": "missing"}))
        proc, r = self.invoke(execute=True, extra=["--allow-network", "--allow-external", "--allow-consent"])
        self.assertEqual(proc.returncode, 2)
        self.assertIn("hub.py doctor: tool is missing", r["nodes"][0]["reason"])
        self.assertEqual(self.runs(), [])

    def test_unknown_safety_is_never_safe(self):
        self.tools["tools"][0]["safety"] = "paid"
        proc, r = self.invoke(execute=True, extra=["--allow-network", "--allow-external", "--allow-consent"])
        self.assertEqual(proc.returncode, 2)
        self.assertIn("unknown safety", r["nodes"][0]["reason"])

    def test_non_tool_executors_and_non_cli_entries_block(self):
        for ref in ("bin:ffmpeg", "mcp:server/tool", "tool:not-there", "tool:../x"):
            self.data["nodes"][0]["executor"]["ref"] = ref
            proc, r = self.invoke(execute=True)
            self.assertEqual((proc.returncode, r["nodes"][0]["status"]), (2, "BLOCKED"), ref)
        self.data["nodes"][0]["executor"]["ref"] = "tool:alpha"
        self.tools["tools"][0]["kind"] = "library"
        proc, r = self.invoke(execute=True)
        self.assertEqual(r["nodes"][0]["status"], "BLOCKED")
        self.assertEqual(self.runs(), [])

    def test_manual_node_blocks_then_resumes_after_its_trace(self):
        self.data["nodes"][0]["executor"]["ref"] = "human"
        proc, r = self.invoke(execute=True)
        self.assertEqual(proc.returncode, 2)
        self.assertIn("MANUAL", r["nodes"][0]["reason"])
        self.assertEqual(self.runs(), [])
        self.data["nodes"][0]["status"] = "passed"  # what fusionforge.py trace --result passed leaves behind
        proc, r = self.invoke(execute=True)
        self.assertEqual(proc.returncode, 0, r)
        self.assertEqual([n["status"] for n in r["nodes"]], ["ALREADY_DONE", "PASS"])
        self.assertEqual(self.runs(), ["run beta --"])

    def test_unplanned_or_edited_plan_is_refused(self):
        self.data["status"] = "candidate"
        proc, r = self.invoke(execute=True)
        self.assertEqual((proc.returncode, r["status"]), (2, "BLOCKED"))
        self.assertIn("choose", r["error"])
        self.data["status"] = "planned"
        self.data["plan_choice"]["nodes"] = ["N02", "N01"]  # differs from plans.A
        proc, r = self.invoke(execute=True)
        self.assertIn("differ", r["error"])
        self.data["plan_choice"] = {"plan": "D", "nodes": ["N01"]}  # plan D must be stored by choose
        proc, r = self.invoke(execute=True)
        self.assertIn("differ", r["error"])
        self.assertEqual(self.runs(), [])

    def test_cycle_is_refused_refine_edges_ignored(self):
        self.data["edges"].append({"id": "E02", "from": "N02", "to": "N01", "relation": "refine"})
        proc, r = self.invoke(execute=True)
        self.assertEqual(proc.returncode, 0, r)
        self.data["edges"][-1]["relation"] = "sequence"
        proc, r = self.invoke(execute=True)
        self.assertEqual(proc.returncode, 2)
        self.assertIn("cycle", r["error"])

    def test_timeout_kills_the_tool_too(self):
        marker = self.base / "orphan-wrote-this"
        proc, r = self.invoke(execute=True, extra=["--timeout", "1"], plan={"N01": ["--orphan", str(marker)]})
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(r["nodes"][0]["execution"]["error"], "TIMEOUT")
        self.assertIn("--error-class timeout", self.calls(self.ff)[0])
        time.sleep(2.5)
        self.assertFalse(marker.exists(), "the tool kept running after the timeout")

    def test_never_overwrites_a_receipt(self):
        report = self.base / "out" / "fixed.json"
        self.invoke(report=report)
        before = report.read_bytes()
        proc = subprocess.run([sys.executable, str(SCRIPT), "--recipe", str(self.recipe), "--registry", str(self.registry),
                               "--hub", str(self.hub), "--report", str(report)], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(report.read_bytes(), before)

    def test_report_outside_allowed_dirs_blocks_before_running(self):
        with tempfile.TemporaryDirectory() as other:
            proc, r = self.invoke(execute=True, report=Path(other) / "r.json")
        self.assertEqual(proc.returncode, 2)
        self.assertIn("EVIDENCE_OUTSIDE_ALLOWED", r["error"])
        self.assertEqual(self.runs(), [])


class RealHubTests(unittest.TestCase):
    """Real hub.py, real fusionforge.py, real tools from data/tools.json."""

    def test_registry_must_be_the_hubs_own(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "recipe.json").write_text("{}", encoding="utf-8")
            (d / "tools.json").write_text('{"tools": []}', encoding="utf-8")
            proc = subprocess.run([sys.executable, str(SCRIPT), "--recipe", str(d / "recipe.json"), "--registry", str(d / "tools.json"),
                                   "--report", str(d / "r.json")], capture_output=True, text=True, cwd=str(d))
            self.assertEqual(proc.returncode, 2)
            self.assertIn("tools.json this hub runs from", json.loads((d / "r.json").read_text())["error"])

    def test_two_tool_recipe_end_to_end(self):
        """U1 manual -> C1 reference-edit-engine (consent) -> V1 creative-quality-gate reading C1's plan.json."""
        sys.path.insert(0, str(SKILL / "evals"))
        from test_fusionforge import BRIEF, CATALOG  # fixture catalog and brief
        with tempfile.TemporaryDirectory() as d:
            d = Path(d).resolve()
            (d / "catalog.json").write_text(json.dumps(CATALOG, ensure_ascii=False), encoding="utf-8")
            (d / "brief.json").write_text(json.dumps(BRIEF, ensure_ascii=False), encoding="utf-8")
            (d / "probe.json").write_text(json.dumps({"status": "reference_timing_observed_not_animation_reconstructed",
                                                      "duration_seconds": 5, "cut_candidates_seconds": [1, 2, 4]}), encoding="utf-8")
            (d / "card.md").write_text("request card written by hand\n", encoding="utf-8")
            rid, root = "FUSE-20261030-0123456789", d / "ff"
            env = {k: v for k, v in os.environ.items() if k != "KOSIF_FUSIONFORGE_ROOT"}

            def ff(*args):
                p = subprocess.run([sys.executable, str(REAL_FF), "--root", str(root), "--catalog-file", str(d / "catalog.json"),
                                    "--now", "2026-10-30T12:00:00Z", *args], capture_output=True, text=True, cwd=str(d), env=env, timeout=180)
                self.assertEqual(p.returncode, 0, p.stderr)
                return p.stdout

            def bridge(name, *extra):
                rep = d / "out" / f"{name}.json"
                p = subprocess.run([sys.executable, str(SCRIPT), "--recipe", str(root / "e2e" / "recipes" / f"{rid}.json"),
                                    "--plan-file", str(d / "io.json"), "--fusionforge-root", str(root), "--report", str(rep), *extra],
                                   capture_output=True, text=True, cwd=str(d), env=env, timeout=300)
                return p.returncode, json.loads(rep.read_text(encoding="utf-8"))

            graph = {"nodes": [
                {"id": "U1", "stage": "understand", "capability_ids": ["SP-0005"], "inputs": [{"name": "req", "kind": "brief"}],
                 "outputs": [{"name": "card", "kind": "spec"}], "executor": "human"},
                {"id": "C1", "stage": "create", "capability_ids": ["SP-0001"], "inputs": [{"name": "card", "kind": "spec"}],
                 "outputs": [{"name": "cut", "kind": "video"}], "executor": "tool:reference-edit-engine"},
                {"id": "V1", "stage": "verify", "capability_ids": ["SP-0004"], "inputs": [{"name": "cut", "kind": "video"}],
                 "outputs": [{"name": "qa", "kind": "evidence"}], "executor": "tool:creative-quality-gate"}],
                "edges": [{"from": "U1", "to": "C1", "kind": "spec"}, {"from": "C1", "to": "V1", "kind": "video", "relation": "verify"}],
                "plans": {"A": {"idea": "lean", "nodes": ["U1", "C1", "V1"]}}}
            (d / "graph.json").write_text(json.dumps(graph), encoding="utf-8")
            (d / "io.json").write_text(json.dumps({
                "C1": {"args": ["--probe", str(d / "probe.json"), "--fps", "30", "--out", str(d / "edit")],
                       "inputs": [str(d / "probe.json")], "outputs": {"plan": str(d / "edit" / "src" / "plan.json")}},
                "V1": {"args": ["{C1.plan}", "--out", "{out.audit}"], "outputs": {"audit": str(d / "qa" / "audit.json")},
                       "make_dirs": [str(d / "qa")]}}), encoding="utf-8")
            ff("propose", "bridge e2e", "--project", "e2e", "--from-brief", str(d / "brief.json"), "--id", rid)
            ff("set-graph", "--project", "e2e", "--id", rid, "--file", str(d / "graph.json"))
            ff("choose", "--project", "e2e", "--id", rid, "--plan", "A", "--why", "bridge e2e")

            rc, r = bridge("1")
            self.assertEqual((rc, [n["status"] for n in r["nodes"]]), (2, ["BLOCKED", "BLOCKED", "READY"]))
            rc, r = bridge("2", "--execute")
            self.assertEqual((rc, [n["status"] for n in r["nodes"]]), (2, ["BLOCKED"]))  # U1 is manual
            ff("trace", "--project", "e2e", "--id", rid, "--stage", "understand", "--node", "U1", "--action", "wrote the card",
               "--result", "passed", "--tool", "human", "--evidence", str(d / "card.md"))
            rc, r = bridge("3", "--execute")
            self.assertEqual((rc, [n["status"] for n in r["nodes"]]), (2, ["ALREADY_DONE", "BLOCKED"]))
            self.assertIn("consent", r["nodes"][1]["reason"])
            # no user clips or audio are supplied, so the consent note (copying user media) is satisfied here
            rc, r = bridge("4", "--execute", "--allow-consent")
            self.assertEqual(rc, 0, json.dumps(r, indent=1))
            self.assertEqual([n["status"] for n in r["nodes"]], ["ALREADY_DONE", "PASS", "PASS"])
            audit = json.loads((d / "qa" / "audit.json").read_text(encoding="utf-8"))
            self.assertEqual(audit["status"], "structurally_verified_render_pending")
            self.assertEqual(audit["failures"], [])

            rec = json.loads(ff("show", "--project", "e2e", "--id", rid, "--json"))["recipe"]
            self.assertEqual([n["status"] for n in rec["nodes"]], ["passed", "passed", "passed"])
            results = [(t["node"], t["result"], t["tool"]) for t in rec["traces"] if t["result"]]
            self.assertEqual(results, [("U1", "passed", "human"), ("C1", "passed", "tool:reference-edit-engine"),
                                       ("V1", "passed", "tool:creative-quality-gate")])
            self.assertIn("plan=", next(t for t in rec["traces"] if t["node"] == "C1" and t["result"])["output"])
            self.assertEqual(rec["status"], "planned")  # the bridge never records tested or verified


if __name__ == "__main__":
    unittest.main()
