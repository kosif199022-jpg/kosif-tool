"""Tests for scripts/self_council.py: inventory, plan, ingest validation, report ranking and ledger coverage (A37).

Every test builds a small fake repository in a temporary folder and points the script at it with --root, so the real
ledger and the real checkout are never touched."""
import contextlib
import io
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import self_council as sc  # noqa: E402

SKILL = ".claude/skills/kosif-superpowers"


def write(root: Path, rel: str, text: str) -> Path:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


def make_repo(root: Path) -> None:
    write(root, f"{SKILL}/SKILL.md", "---\nname: kosif-superpowers\ndescription: test skill\n---\n# x\n")
    write(root, f"{SKILL}/scripts/alpha.py", '#!/usr/bin/env python3\n"""Alpha.\n\n  python3 scripts/alpha.py run\n"""\nprint(1)\n')
    write(root, f"{SKILL}/scripts/beta.py", "import sys\n" + "x = 1\n" * 500)
    write(root, f"{SKILL}/scripts/gamma.py", '"""Gamma does a thing."""\n')
    write(root, f"{SKILL}/scripts/_helper.py", '"""Helper.\n\nusage: imported only\n"""\n')
    write(root, f"{SKILL}/evals/test_alpha.py", "import alpha\n")
    write(root, f"{SKILL}/evals/test_misc.py", "import json, gamma as g\n")  # an aliased import still counts
    write(root, f"{SKILL}/scripts/delta.py", '"""Delta.\n\nusage: python3 scripts/delta.py\n"""\n')
    write(root, "tests/test_through.py", "import subprocess  # drives delta through another script\n")
    write(root, "tools/shdir/run.sh", "#!/bin/sh\n# Run me: run --go\n")
    write(root, f"{SKILL}/data/tools.json", json.dumps({"tools": [
        {"root": "skill", "path": "scripts/alpha.py", "evidence": "tested-here"},
        {"root": "skill", "path": "scripts/gamma.py", "evidence": "untested"},
        {"root": "skill", "path": "scripts/delta.py", "evidence": "tested-here", "tests": ["tests/test_through.py"]},
        {"root": "repo", "path": "tools/shdir/run.sh", "evidence": "untested"}]}))
    write(root, f"{SKILL}/references/protocol/CHANGELOG.md",
          "# log\n\n## الفهرس / contents\n\n- x\n\n## v2 — 2026-10-24 (هذا الإصدار)\n\n- added `alpha.py`\n\n## v1 — 2026-10-01\n\n- old\n")
    write(root, ".claude/skills/other/SKILL.md", "---\nname: other\n---\n# no description\n")
    write(root, "apps/app1/main.js", "console.log(1)\n")
    write(root, "apps/app2/README.md", "# app2\n")
    write(root, "apps/app2/test_app2.py", "pass\n")
    write(root, "tools/tool1.py", '"""Tool one.\n\nusage: python3 tools/tool1.py\n"""\n')
    write(root, "playbooks/pb.md", "# Playbook\n\n## How\n\n```\nrun it\n```\n")
    write(root, "workflows/wf/README.md", "# wf\n")


def run(root: Path, *args, expect=0):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = sc.main(["--root", str(root), *args])
    if code != expect:
        raise AssertionError(f"exit {code} != {expect}: {err.getvalue()} {out.getvalue()[:400]}")
    return json.loads(out.getvalue()) if code == 0 else err.getvalue()


def finding(title, change, ev, sev="medium", effort="S", conf=0.8, cat="test"):
    return {"title": title, "proposed_change": change, "evidence": ev, "severity": sev, "effort": effort,
            "confidence": conf, "category": cat}


FIELDS = {"P1": {"test_verdict": {"status": "none", "ran": "python3 x --help"}},
          "P2": {"first_minute": {"clarity": 3, "would_say": "الأداة دي بتعمل ايه؟"}},
          "P3": {"keep_or_kill": {"decision": "keep", "why": "used"}},
          "P4": {"wiring": {"overlaps": [], "should_call": []}},
          "P5": {"ten_x": {"idea": "do more", "first_step": "add a flag"}}}


def review(pid, units, findings_for=None):
    revs = []
    for u in units:
        fs = findings_for(pid, u) if findings_for else []
        r = {"unit": u, "summary": f"{pid} on {u}", "findings": fs}
        r.update(json.loads(json.dumps(FIELDS[pid])))  # a copy: tests mutate it
        if not fs:
            r["no_findings_reason"] = "nothing found in my lens"
        revs.append(r)
    return {"persona": pid, "reviews": revs}


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="selfcouncil_"))
        self.root = self.tmp / "repo"
        make_repo(self.root)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def ingest(self, d, pid, obj, simulated=True, expect=0):
        f = self.tmp / f"{pid}_{abs(hash(json.dumps(obj, sort_keys=True)))}.json"
        f.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")
        return run(self.root, "ingest", "--dir", str(d), "--persona", pid, "--file", str(f),
                   *(["--simulated"] if simulated else []), expect=expect)

    def full_round(self, d, findings_for=None, simulated=True):
        batch = json.loads((d / "run.json").read_text(encoding="utf-8"))["batch"]
        for pid in sc.PERSONA_IDS:
            self.ingest(d, pid, review(pid, batch, findings_for), simulated=simulated)
        return batch


class InventoryTests(Base):
    def test_units_ids_and_signals(self):
        res = run(self.root, "inventory")
        self.assertEqual(res["counts"], {"skill": 2, "script": 5, "app": 2, "tool": 2, "playbook": 1, "workflow": 1})
        u = {x["id"]: x for x in res["units"]}
        a = u["script:alpha"]["signals"]
        self.assertEqual((a["has_test"], a["docstring"], a["usage"], a["registered"]), ("direct", True, True, True))
        self.assertEqual(a["changelog"], "v2 — 2026-10-24")
        b = u["script:beta"]
        self.assertEqual(b["signals"]["has_test"], "none")
        for r in ("NO_TEST", "LARGE_UNTESTED", "NO_DOCSTRING", "UNREGISTERED"):
            self.assertIn(r, b["reasons"])
        self.assertEqual(u["script:gamma"]["signals"]["has_test"], "indirect")
        self.assertIn("NO_USAGE", u["script:gamma"]["reasons"])
        self.assertNotIn("UNREGISTERED", u["script:_helper"]["reasons"])  # shared helpers are not hub tools
        self.assertIn("NO_DESCRIPTION", u["skill:other"]["reasons"])
        self.assertIn("NO_README", u["app:app1"]["reasons"])
        self.assertEqual(u["app:app2"]["signals"]["has_test"], "direct")
        self.assertIn("NO_TEST_REPORT", u["workflow:wf"]["reasons"])
        self.assertEqual(u["playbook:pb"]["signals"]["examples"], 1)
        d = u["script:delta"]  # a test named only in the registry still counts, as an indirect one
        self.assertEqual((d["signals"]["has_test"], d["signals"]["tests"]), ("registered", ["tests/test_through.py"]))
        self.assertNotIn("NO_TEST", d["reasons"])
        sh = u["tool:shdir"]["signals"]  # a folder tool is registered by a file inside it; "run --go" is a usage line
        self.assertEqual((sh["registered"], sh["usage"]), (True, True))
        self.assertEqual(run(self.root, "inventory")["units"], res["units"])  # deterministic

    def test_summary_and_kind_filter(self):
        res = run(self.root, "inventory", "--kind", "script", "--summary")
        self.assertNotIn("units", res)
        self.assertEqual(res["total"], 5)
        self.assertTrue(res["weakest"][0].startswith("script:beta"))


class PlanTests(Base):
    def test_plan_writes_prompts_and_claims(self):
        d1 = self.tmp / "out" / "r1"
        res = run(self.root, "plan", "--batch", "3", "--dir", str(d1))
        batch = [x.split()[0] for x in res["batch"]]
        self.assertEqual(batch[0], "script:beta")  # the weakest unit first
        for pid in sc.PERSONA_IDS:
            text = (d1 / "prompts" / f"{pid}.md").read_text(encoding="utf-8")
            for uid in batch:
                self.assertIn(uid, text)
        prompts = json.loads((d1 / "prompts.json").read_text(encoding="utf-8"))
        self.assertEqual(sorted(prompts), list(sc.PERSONA_IDS))
        self.assertEqual(sorted(prompts["P3"]), sorted(batch))
        self.assertIn("محامي الشيطان", prompts["P3"][batch[0]])
        led = json.loads((self.root / sc.LEDGER_REL).read_text(encoding="utf-8"))
        self.assertTrue(all(led["units"][u]["state"] == "planned" for u in batch))
        d2 = self.tmp / "out" / "r2"
        batch2 = [x.split()[0] for x in run(self.root, "plan", "--batch", "3", "--dir", str(d2))["batch"]]
        self.assertFalse(set(batch) & set(batch2))  # an open run's units are not planned twice
        self.assertIn("EXISTS", run(self.root, "plan", "--batch", "3", "--dir", str(d1), expect=2))
        self.assertIn("BATCH_RANGE", run(self.root, "plan", "--batch", "0", "--dir", str(self.tmp / "x"), expect=2))

    def test_deleted_run_releases_claims(self):
        d1 = self.tmp / "out" / "r1"
        b1 = [x.split()[0] for x in run(self.root, "plan", "--batch", "2", "--dir", str(d1))["batch"]]
        shutil.rmtree(d1)
        b2 = [x.split()[0] for x in run(self.root, "plan", "--batch", "2", "--dir", str(self.tmp / "out" / "r2"))["batch"]]
        self.assertEqual(b1, b2)


class IngestTests(Base):
    def setUp(self):
        super().setUp()
        self.d = self.tmp / "out" / "r1"
        run(self.root, "plan", "--batch", "2", "--dir", str(self.d))
        self.batch = json.loads((self.d / "run.json").read_text(encoding="utf-8"))["batch"]
        self.good_ev = f"{SKILL}/scripts/beta.py:1"

    def bad(self, pid, mutate, code="REVIEW_INVALID"):
        obj = review(pid, self.batch, lambda p, u: [finding("t", "c", self.good_ev)])
        mutate(obj)
        self.assertIn(code, self.ingest(self.d, pid, obj, expect=2))

    def test_rejects_bad_input(self):
        r0 = lambda o: o["reviews"][0]  # noqa: E731
        f0 = lambda o: o["reviews"][0]["findings"][0]  # noqa: E731
        self.bad("P1", lambda o: r0(o).update(unit="script:nope"))
        self.bad("P1", lambda o: f0(o).update(evidence="no/such/file.py"))
        self.bad("P1", lambda o: f0(o).update(evidence="/etc/passwd"))
        self.bad("P1", lambda o: f0(o).update(evidence="../outside.py"))
        self.bad("P1", lambda o: f0(o).update(severity="urgent"))
        self.bad("P1", lambda o: f0(o).update(effort="XL"))
        self.bad("P1", lambda o: f0(o).update(confidence=1.5))
        self.bad("P1", lambda o: f0(o).update(category="vibes"))
        self.bad("P1", lambda o: f0(o).pop("proposed_change"))
        self.bad("P1", lambda o: r0(o).pop("test_verdict"))
        self.bad("P2", lambda o: r0(o)["first_minute"].update(clarity=9))
        self.bad("P3", lambda o: r0(o)["keep_or_kill"].update(decision="maybe"))
        self.bad("P1", lambda o: r0(o).update(findings=[]))  # empty without a reason
        self.bad("P1", lambda o: o["reviews"].append(dict(o["reviews"][0])))  # a unit reviewed twice
        self.bad("P1", lambda o: o.update(persona="P2"), code="PERSONA_MISMATCH")
        self.bad("P1", lambda o: f0(o).update(proposed_change="set api_key=" + "sk-" + "ant-" + "abcdefghijklmnopqrstuvwx"), code="SECRET")  # key built at runtime: no literal in the file
        obj = review("P1", self.batch)
        self.assertIn("UNKNOWN_PERSONA", self.ingest(self.d, "P9", obj, expect=2))
        bad_json = self.tmp / "bad.json"
        bad_json.write_text("not json", encoding="utf-8")
        self.assertIn("BAD_JSON", run(self.root, "ingest", "--dir", str(self.d), "--persona", "P1", "--file", str(bad_json), expect=2))

    def test_accepts_valid_and_fenced(self):
        obj = review("P1", self.batch, lambda p, u: [finding("t", "c", self.good_ev)])
        f = self.tmp / "p1.json"
        f.write_text("```json\n" + json.dumps(obj) + "\n```", encoding="utf-8")
        res = run(self.root, "ingest", "--dir", str(self.d), "--persona", "p1", "--file", str(f), "--simulated")
        self.assertEqual((res["have"], res["of"], res["simulated"]), (2, 2, True))
        self.assertTrue((self.d / "reviews" / "P1.json").is_file())


class ReportTests(Base):
    def test_ranking_dedupe_and_status(self):
        d = self.tmp / "out" / "r1"
        run(self.root, "plan", "--batch", "2", "--dir", str(d))
        batch = json.loads((d / "run.json").read_text(encoding="utf-8"))["batch"]
        ev = f"{SKILL}/scripts/beta.py"
        target = batch[0]

        def fs(pid, u):
            if u != target:
                return []
            out = []
            if pid in ("P1", "P3", "P4"):  # three personas agree on the same missing test, worded slightly differently
                out.append(finding("Add a unit test for beta", "Add evals/test_beta.py covering beta main path", ev, sev="high", effort="S"))
            if pid == "P5":
                out.append(finding("Rewrite beta as a service", "Rewrite beta into a long-running web service", ev,
                                   sev="high", effort="L", conf=0.5, cat="feature"))
            if pid == "P2":
                out.append(finding("Docstring missing", "Write a docstring with a usage line", ev, sev="low", effort="S", cat="docs"))
            return out

        self.assertIn("INCOMPLETE", run(self.root, "report", "--dir", str(d), expect=2))
        self.full_round(d, fs)
        md, js = self.tmp / "docs" / "R.md", self.tmp / "docs" / "R.json"
        res = run(self.root, "report", "--dir", str(d), "--top", "2", "--out-md", str(md), "--out-json", str(js))
        self.assertEqual(res["status"], "SELF_COUNCIL_SIMULATED")
        rep = json.loads(js.read_text(encoding="utf-8"))
        self.assertEqual(len(rep["proposals"]), 3)  # the three test findings merged into one
        top = rep["implement_next"][0]
        self.assertEqual((top["title"], top["agree"], top["personas"]), ("Add a unit test for beta", 3, ["P1", "P3", "P4"]))
        self.assertEqual(len(rep["implement_next"]), 2)
        self.assertEqual(rep["proposals"][-1]["category"], "feature")  # high but L effort and low confidence ranks last
        self.assertIn("SIMULATED", md.read_text(encoding="utf-8"))
        self.assertEqual(rep["coverage"]["reviewed"], 2)

    def test_same_proposal_on_two_units_is_listed_once(self):
        d = self.tmp / "out" / "r2"
        run(self.root, "plan", "--batch", "2", "--dir", str(d))
        ev = f"{SKILL}/scripts/alpha.py"
        self.full_round(d, lambda p, u: [finding("Run the runner in CI", "Add one CI step for the shared runner", ev, sev="high")]
                        if p == "P1" else [])
        run(self.root, "report", "--dir", str(d))
        rep = json.loads((d / "report.json").read_text(encoding="utf-8"))
        self.assertEqual(len(rep["proposals"]), 1)
        self.assertEqual(len(rep["proposals"][0]["units"]), 2)


class LedgerCoverageTests(Base):
    def test_successive_runs_cover_everything_once(self):
        total = run(self.root, "inventory", "--summary")["total"]
        seen, n = [], 0
        while True:
            d = self.tmp / "out" / f"run{n}"
            code_err = io.StringIO()
            with contextlib.redirect_stdout(io.StringIO()) as o, contextlib.redirect_stderr(code_err):
                code = sc.main(["--root", str(self.root), "plan", "--batch", "4", "--dir", str(d)])
            if code != 0:
                self.assertIn("NOTHING_TO_PLAN", code_err.getvalue())
                break
            out = json.loads(o.getvalue())
            seen += [x.split()[0] for x in out["batch"]]
            self.full_round(d)
            cov = run(self.root, "report", "--dir", str(d))["coverage"]
            n += 1
            self.assertEqual(int(cov.split("/")[0]), len(seen))  # coverage grows by exactly the batch
            self.assertLess(n, 10)
        self.assertEqual(len(seen), total)
        self.assertEqual(len(set(seen)), total)  # no unit skipped, none twice
        st = run(self.root, "status")["coverage"]
        self.assertEqual((st["reviewed"], st["fresh"], st["percent"]), (total, total, 100.0))
        # a unit that changes after its review comes back as stale, and the next plan picks it up
        write(self.root, f"{SKILL}/scripts/alpha.py", '"""Alpha v2.\n\nusage: python3 alpha.py\n"""\n')
        self.assertEqual(run(self.root, "status")["coverage"]["stale"], 1)
        res = run(self.root, "plan", "--batch", "4", "--dir", str(self.tmp / "out" / "again"))
        self.assertEqual([x.split()[0] for x in res["batch"]], ["script:alpha"])
        res = run(self.root, "plan", "--batch", "2", "--dir", str(self.tmp / "out" / "revisit"), "--revisit")
        self.assertEqual(len(res["batch"]), 2)

    def test_partial_report_keeps_unit_pending(self):
        d = self.tmp / "out" / "p"
        run(self.root, "plan", "--batch", "1", "--dir", str(d))
        batch = json.loads((d / "run.json").read_text(encoding="utf-8"))["batch"]
        self.ingest(d, "P1", review("P1", batch))
        res = run(self.root, "report", "--dir", str(d), "--partial")
        self.assertEqual(res["status"], "SELF_COUNCIL_SIMULATED+PARTIAL")
        self.assertEqual(run(self.root, "status")["coverage"]["pending"], 1)
        again = run(self.root, "plan", "--batch", "1", "--dir", str(self.tmp / "out" / "p2"))
        self.assertEqual([x.split()[0] for x in again["batch"]], batch)  # the partial unit is first in line again


if __name__ == "__main__":
    unittest.main()
