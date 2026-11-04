"""Tests for the Dragon Mind super-skill: full coverage, honest tiers, deterministic thinking."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIND = ROOT / ".claude/skills/kosif-dragon-mind"
sys.path.insert(0, str(MIND / "scripts"))
import dragon_mind as dm  # noqa: E402
import _mind_vocab as V  # noqa: E402

TIERS = {t for t, _ in V.TIERS}


class DragonMindTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inv, cls.desc, cls.adapters, cls.tools = dm.load_inventory()
        cls.dec = dm.decompose(cls.inv, cls.desc)
        cls.ready = dm.readiness(cls.inv, cls.desc, cls.adapters, cls.tools)

    def test_every_entry_is_decomposed(self):
        self.assertEqual(set(self.dec), set(self.inv))
        for row in self.dec.values():
            self.assertIn(row["primary"], V.FACULTY_IDS)
            self.assertEqual(row["faculties"][0], row["primary"])
            self.assertLessEqual(len(row["faculties"]), 4)

    def test_every_entry_has_a_known_tier(self):
        rows = self.ready["rows"]
        self.assertEqual(set(rows), set(self.inv))
        self.assertTrue(all(r["tier"] in TIERS for r in rows.values()))
        self.assertEqual(sum(self.ready["tiers"].values()), len(self.inv))

    def test_executable_tier_only_for_reviewed_adapters(self):
        for key, row in self.ready["rows"].items():
            if row["tier"] == "T4-executable":
                self.assertIn(key, self.adapters)
            if key.startswith(("power:", "superpower:", "style:")):
                self.assertNotIn(row["tier"], ("T3-runnable",))

    def test_fuse_has_all_faculties_and_champions_are_members(self):
        fused = dm.fuse(self.dec, self.ready["rows"], self.desc)
        self.assertEqual(list(fused), V.FACULTY_IDS)
        for fid, info in fused.items():
            for champ in info["champions"]:
                self.assertIn(fid, self.dec[champ["id"]]["faculties"])
            if info["executors"] == 0:
                self.assertTrue(info["gap"])

    def test_think_is_deterministic_and_covers_the_cycle(self):
        task = "اعمل فيديو موشن عربي لإطلاق منتج وانشره على تيك توك"
        a, b = dm.think(task), dm.think(task)
        self.assertEqual(a["digest"], b["digest"])
        self.assertEqual({f["stage"] for f in a["frameworks"]} if a["frameworks"] else set(),
                         {s["id"] for s in V.CYCLE} if a["frameworks"] else set())
        names = {n["faculty"] for n in a["graph"]["nodes"]}
        self.assertTrue(set(dm.ALWAYS) <= names)
        self.assertIn("animate-motion", names)
        self.assertEqual(len(a["graph"]["edges"]), len(a["graph"]["nodes"]))
        self.assertTrue(a["consent_required"])
        self.assertTrue(any(i["kind"] == "consent" for i in a["critic"]))
        self.assertIn("executed", a["evidence_rule"])

    def test_think_rejects_empty_task(self):
        with self.assertRaises(ValueError):
            dm.think("  ")

    def test_report_is_markdown_with_sections(self):
        md = dm.report_md(dm.think("research a pricing strategy for a new app"))
        for head in ("## 1.", "## 2.", "## 3.", "## 4.", "## 5."):
            self.assertIn(head, md)

    def test_frameworks_library_is_valid(self):
        lib = json.loads((MIND / "data" / "frameworks.json").read_text(encoding="utf-8"))["frameworks"]
        self.assertGreaterEqual(len(lib), 100)
        self.assertEqual(len({f["id"] for f in lib}), len(lib))
        stages = {s["id"] for s in V.CYCLE}
        for f in lib:
            self.assertIn(f["stage"], stages)
            self.assertTrue(f["source_books"] and f["check"] and f["questions_ar"])
        for st, dflt in dm.STAGE_DEFAULTS.items():
            self.assertIn(dflt, {f["id"] for f in lib if f["stage"] == st}, st)

    def test_research_receipt_matches_data(self):
        rec = json.loads((MIND / "data" / "research_receipt.json").read_text(encoding="utf-8"))
        gh = json.loads((MIND / "data" / "github_patterns.json").read_text(encoding="utf-8"))
        bk = json.loads((MIND / "data" / "books_thinking.json").read_text(encoding="utf-8"))
        self.assertEqual(rec["github"]["repos_measured"], gh["repos_measured"])
        self.assertEqual(rec["books"]["kept"], len(bk["books"]))
        self.assertEqual(bk["screened"], 10000)
        for p in gh["patterns"]:
            self.assertLessEqual(p["repos"], gh["repos_measured"])

    def test_mind_adapter_runs_through_the_dragon_runner(self):
        bd, _ = dm._dragon()
        self.assertIn(V.MIND_ADAPTER_KEY, self.inv)
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "adapters.json"
            self.assertEqual(dm.main(["adapters", "--out", str(out)]), 0)
            loaded = bd._load_adapters(out)
            self.assertIn(V.MIND_ADAPTER_KEY, loaded)
            self.assertTrue(set(loaded) <= set(self.inv))
            artifact = Path(tmp) / "mind.txt"
            spec = loaded[V.MIND_ADAPTER_KEY]
            args = [a.replace("{artifact}", str(artifact)).replace("{task}", "قص فيديو وتلوينه") for a in spec["args"]]
            done = subprocess.run([sys.executable, str(ROOT / spec["script"]), *args], cwd=ROOT,
                                  capture_output=True, text=True, timeout=120)
            self.assertEqual(done.returncode, 0, done.stderr[-500:])
            body = artifact.read_text(encoding="utf-8")
            # the mind's own adapter writes its report; a reviewed skill adapter (PR #214) writes a JSON verdict
            self.assertTrue("عقل التنين" in body or '"verdict": "passed"' in body, body[:300])


class DragonMindLinkAndApplyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.links = json.loads((MIND / "data" / "mind_links.json").read_text(encoding="utf-8"))
        cls.inv, *_ = dm.load_inventory()

    def test_graph_is_one_connected_network_over_valid_ids(self):
        nodes, edges = self.links["nodes"], self.links["edges"]
        self.assertEqual(self.links["stats"]["components_all_links"], 1)
        self.assertEqual(set(nodes), set(edges))
        for k, e in edges.items():
            for kind in ("peers", "next", "prev", "specialist", "hub_chain"):
                for o in e.get(kind, []):
                    self.assertIn(o, nodes, (k, kind))
            for kind in ("owner", "hub"):
                if e.get(kind):
                    self.assertIn(e[kind], nodes)

    def test_every_live_entry_is_linked_or_resolvable(self):
        missing = set(self.inv) - set(self.links["nodes"])
        self.assertLessEqual(len(missing), 25, "run dragon_mind.py link --write")

    def test_applier_works_for_every_kind(self):
        import card_apply as ca
        by_kind = {}
        for k, n in sorted(self.links["nodes"].items()):
            by_kind.setdefault(n["kind"], k)
        self.assertEqual(set(by_kind), {"power", "superpower", "style", "skill", "playbook", "protocol", "tool"})
        with tempfile.TemporaryDirectory() as tmp:
            for kind, key in by_kind.items():
                out = Path(tmp) / (kind + ".json")
                self.assertEqual(ca.main([str(out), key, "اعمل فيديو موشن عربي"]), 0, key)
                res = json.loads(out.read_text(encoding="utf-8"))
                self.assertTrue(res["steps"], key)
                self.assertTrue(res["status"].startswith("applied-"))
                src = ca.source_path(res["kind"], res["source"])
                self.assertEqual(res["source_sha256"], ca.sha(src))
            self.assertEqual(ca.main([str(Path(tmp) / "x.json"), "power:NO-SUCH-CARD", "task"]), 3)

    def test_audit_splits_receipts_and_catches_tampering(self):
        import hashlib
        with tempfile.TemporaryDirectory() as tmp:
            job = Path(tmp)
            (job / "receipts").mkdir()
            (job / "artifacts").mkdir()
            rows = [("power:A", V.APPLIER_SCRIPT, '{"status": "applied-ready-here"}'),
                    ("tool:b", ".claude/skills/kosif-superpowers/scripts/_black_dragon_exec.py x tool.py", "ran"),
                    ("tool:c", "_black_dragon_exec.py", "ran")]
            for i, (entry, script, body) in enumerate(rows):
                art = job / "artifacts" / ("%d.txt" % i)
                art.write_text(body, encoding="utf-8")
                rec = {"entry": entry, "command": ["python3", script], "artifact": str(art),
                       "artifact_sha256": hashlib.sha256(art.read_bytes()).hexdigest()}
                (job / "receipts" / ("%d.json" % i)).write_text(json.dumps(rec), encoding="utf-8")
            (job / "artifacts" / "2.txt").write_text("tampered", encoding="utf-8")
            res = dm.audit_job(job)
        self.assertEqual(res["tiers"], {"method_applied": 1, "tool_adapter_executed": 1})
        self.assertEqual(res["method_status"], {"applied-ready-here": 1})
        self.assertEqual(res["hash_mismatch"], ["tool:c"])
        self.assertEqual(res["real_executed"], 1)

    def test_all_adapters_cover_every_entry_and_keep_reviewed_ones(self):
        bd, _ = dm._dragon()
        reviewed = bd._load_adapters(bd.REVIEWED_ADAPTERS)
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "all.json"
            self.assertEqual(dm.main(["adapters", "--all", "--out", str(out)]), 0)
            allad = bd._load_adapters(out)
        self.assertEqual(set(allad), set(self.inv))
        for k, spec in reviewed.items():
            self.assertEqual(allad[k], spec)
        real = dm.reviewed_adapters(bd)  # reviewed + generated real runners
        for k, spec in real.items():
            self.assertEqual(allad[k], spec)
        for k, spec in allad.items():
            bd._safe_script(spec["script"])
            if k not in real and k != V.MIND_ADAPTER_KEY:
                self.assertIs(spec.get("method_applier"), True, k)

    def test_generated_real_runners_merge_and_reviewed_wins(self):
        bd, _ = dm._dragon()
        reviewed = bd._load_adapters(bd.REVIEWED_ADAPTERS)
        some = sorted(reviewed)[0]
        power = next(k for k in sorted(self.inv) if k.startswith("power:") and k not in reviewed)
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / bd.REVIEWED_ADAPTERS.name).write_text(bd.REVIEWED_ADAPTERS.read_text(encoding="utf-8"),
                                                      encoding="utf-8")
            runner = {"script": V.APPLIER_SCRIPT, "args": ["{artifact}"], "why": "proof runner"}
            (d / V.GENERATED_ADAPTER_FILES[0]).write_text(
                json.dumps({"adapters": {power: runner, some: runner}}), encoding="utf-8")
            merged = dm.reviewed_adapters(bd, d)
        self.assertEqual(merged[power], runner)
        self.assertEqual(merged[some], reviewed[some])
        self.assertNotIn("method_applier", merged[power])

    def test_superpower_chain_executes_only_when_every_member_runs(self):
        import superpower_run as spr
        sps = spr.load_superpowers()
        self.assertEqual(len(sps), sum(1 for k in self.inv if k.startswith("superpower:")))
        sp_id = min(sps, key=lambda i: (len(sps[i]["pipeline"]), i))
        members = ["power:" + s["id"] for s in sps[sp_id]["pipeline"]]
        with tempfile.TemporaryDirectory() as tmp:
            ok = Path(tmp) / "ok.py"
            ok.write_text("import sys,pathlib; pathlib.Path(sys.argv[1]).write_text('ran ' + sys.argv[2])\n")
            bad = Path(tmp) / "bad.py"
            bad.write_text("import sys; sys.exit(1)\n")
            rel_ok = ".claude/skills/kosif-dragon-mind/scripts/_t_ok.py"
            rel_bad = ".claude/skills/kosif-dragon-mind/scripts/_t_bad.py"
            (ROOT / rel_ok).write_text(ok.read_text())
            (ROOT / rel_bad).write_text(bad.read_text())
            try:
                full = {m: {"script": rel_ok, "args": ["{artifact}", "{task}"]} for m in members}
                adapters, counts = spr.registry(full)
                self.assertIn("superpower:" + sp_id, adapters)
                art = Path(tmp) / "a.json"
                self.assertEqual(spr.execute(art, sp_id, "t", runners=full), 0)
                res = json.loads(art.read_text(encoding="utf-8"))
                self.assertEqual(res["verdict"], "executed")
                self.assertEqual(res["members_executed"], len(members))
                for st in res["steps"]:
                    self.assertEqual(st["artifact_sha256"], spr.sha(Path(st["artifact"])))
                broken = dict(full, **{members[0]: {"script": rel_bad, "args": []}})
                self.assertEqual(spr.execute(Path(tmp) / "b.json", sp_id, "t", runners=broken), 3)
                none = spr.execute(Path(tmp) / "c.json", sp_id, "t", runners={})
                self.assertEqual(none, 3)
                self.assertEqual(json.loads((Path(tmp) / "c.json").read_text())["verdict"], "none")
            finally:
                (ROOT / rel_ok).unlink()
                (ROOT / rel_bad).unlink()


if __name__ == "__main__":
    unittest.main()
