#!/usr/bin/env python3
"""Regression suite for FusionForge v2 (scripts/fusionforge.py) and the shared secret detector (scripts/_secrets.py).

Every CLI call runs in a subprocess with --root inside a temporary directory and cwd set to that directory, so
nothing touches the real out/fusionforge. Most tests use a small fixture catalog, brief.json and tools.json;
two tests run propose against the real catalog (smoke, determinism without a brief file). Beyond the happy path the
suite covers: typed-garbage sibling records and an in-process type fuzz (no INTERNAL errors), secrets in every
written field (paths, --project, quoted JSON keys, evidence file contents), the verified gate across forks, siblings
and imports, self-evidence by copy or hard link, path redaction, output-path guards, lessons that credit only what a
trace reported, stage memory, stale briefs, and the NO_ROOT rule. Run: python3 -m unittest evals/test_fusionforge.py
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
SCRIPT = SKILL / "scripts" / "fusionforge.py"
sys.path.insert(0, str(SKILL / "scripts"))
import _secrets  # noqa: E402

NOW = "2026-10-21T12:00:00Z"
GOAL = "مونتاج فيديو بترجمة عربية وصوت"
FIXED_ID = "FUSE-20261021-0123456789"


def item(sid, name_en, name_ar, domain, fams, atoms, links=()):
    return {"id": sid, "name_en": name_en, "name_ar": name_ar, "domain": domain, "families": {f: 1 for f in fams},
            "focus": name_en.lower().split(), "size": len(atoms),
            "pipeline": [{"id": a, "status": "proven" if i == 0 else "documented", "name_en": f"{name_en} step {i}", "name_ar": name_ar}
                         for i, a in enumerate(atoms)],
            "links": [{"id": l, "sim": s} for l, s in links]}


CATALOG = {"schema": "kosif.superpowers.v1", "items": [
    item("SP-0001", "Video montage cut", "مونتاج فيديو", "motion", ["video-edit"], ["VID-01", "VID-02", "VID-03"], [("SP-0006", 0.5)]),
    item("SP-0002", "Arabic kinetic captions", "ترجمة عربية متحركة", "motion", ["arabic-type"], ["ARB-01", "ARB-02"], [("SP-0001", 0.4)]),
    item("SP-0003", "Audio loudness master", "صوت ماستر", "media", ["audio"], ["AUD-01", "AUD-02"]),
    item("SP-0004", "Frame QA scan", "فحص الاطارات", "data", ["qa-verification"], ["QA-01", "QA-02"], [("SP-0007", 0.3)]),
    item("SP-0005", "Request card analysis", "تحليل الطلب", "mind", ["planning-execution"], ["PLN-01", "PLN-02"]),
    item("SP-0006", "Export package delivery", "تسليم الحزمة", "docs", ["delivery"], ["DEL-01", "DEL-02"]),
    item("SP-0007", "Financial reconciliation invariant", "تسوية مالية", "data", ["finance"], ["FIN-01"]),
    item("SP-0008", "Beat-synced cut planner", "قص على الايقاع", "motion", ["video-edit", "audio"], ["BEAT-01", "BEAT-02", "BEAT-03"]),
]}
TOOLS = {"schema": "kosif.tools.v1", "tools": [
    {"id": "fixture-render", "area": "motion", "families": ["video-edit"]},
    {"id": "fixture-qa", "area": "maintain", "families": ["qa-verification"]},
    {"id": "fixture-pack", "area": "maintain", "families": ["delivery", "packaging"]},
]}


def sp(sid, stage):
    it = next(i for i in CATALOG["items"] if i["id"] == sid)
    return {"id": sid, "name_ar": it["name_ar"], "name_en": it["name_en"], "stage": stage, "role": "core", "local_badge": "✅"}


def tool(tid, state="ready"):
    t = next(x for x in TOOLS["tools"] if x["id"] == tid)
    return {"id": tid, "area": t["area"], "state": state, "command": f"python3 {tid}.py", "families": t["families"]}


def plan(name, idea, stages, tools):
    return {"name": name, "idea": idea, "stages": stages,
            "superpowers": [sp(s, st) for st, ids in stages.items() for s in ids], "tools": tools}


BRIEF = {
    "schema": "kosif.skill-intelligence.v2",
    "coverage": {"complete": True, "catalog_sha256": "f" * 64, "records_scanned": 22, "records_on_disk": 22},
    "analysis": {"request": GOAL, "level": "L2", "primary": "video", "deliverables": ["video"]},
    "shortlist": [dict(sp(i["id"], "create"), families=list(i["families"]), score=50.0) for i in CATALOG["items"]],
    "must_have_coverage": [{"need": "نص عربي صحيح RTL", "superpowers": ["SP-0002"], "status": "covered"}],
    "plans": {
        "A": plan("A", "shortest path", {"understand": ["SP-0005"], "create": ["SP-0001"], "verify": ["SP-0004"], "deliver": ["SP-0006"]},
                  [tool("fixture-render")]),
        "B": plan("B", "balanced", {"understand": ["SP-0005"], "create": ["SP-0001", "SP-0002"], "refine": ["SP-0003"],
                                    "verify": ["SP-0004"], "deliver": ["SP-0006"]}, [tool("fixture-render"), tool("fixture-qa")]),
        "C": plan("C", "different engine", {"understand": ["SP-0005"], "create": ["SP-0008", "SP-0002"], "refine": ["SP-0003"],
                                            "verify": ["SP-0004"], "deliver": ["SP-0006"]}, [tool("fixture-qa"), tool("fixture-pack", "missing")]),
    },
    "recommended": "B",
    "tools": [tool("fixture-render"), tool("fixture-qa"), tool("fixture-pack", "missing")],
}


def secret_samples() -> dict:
    """Built at runtime so this file never contains a credential-shaped literal."""
    a = "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6"
    return {
        "anthropic_api_key": "sk-" + "ant-api03-" + a,
        "openai_api_key": "sk-" + "proj-" + a,
        "aws_access_key_id": "AK" + "IAIOSFODNN7EXAMPLE",
        "aws_secret_access_key": "aws_secret_" + "access_key=" + "wJalrXUtnFEMIK7MDENGbPxRfiCYEXAMPLEKEY",
        "github_token": "gh" + "p_" + a,
        "github_fine_grained_pat": "github" + "_pat_" + "11ABCDEFG0" + a,
        "gitlab_token": "gl" + "pat-" + a[:24],
        "google_api_key": "AI" + "za" + "Sy" + a + "abc",
        "slack_token": "xo" + "xb-" + "1234567890-" + a[:12],
        "stripe_secret_key": "sk" + "_live_" + a,
        "huggingface_token": "hf" + "_" + a + "xy",
        "bearer_token": "Bear" + "er " + a,
        "jwt": "eyJ" + "hbGciOiJIUzI1NiJ9" + "." + "eyJzdWIiOiIxMjM0NTY3ODkwIn0" + "." + "SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
        "private_key_block": "-----BEGIN " + "OPENSSH PRIVATE " + "KEY-----",
        "url_credentials": "postgres://admin:" + "s3cretP4ss" + "@db.example.com/x",
        "credential_assignment": "pass" + "word=" + "hunter2hunter2",
        "google_oauth_client_secret": "GOC" + "SPX-" + a,
        "google_oauth_access_token": "ya2" + "9." + a,
        "digitalocean_token": "do" + "p_v1_" + "ab12" * 16,
        "shopify_token": "shp" + "at_" + "abcdef0123456789" * 2,
        "pypi_token": "pyp" + "i-AgEIcHlwaS5vcmc" + a,
        "mailgun_key": "ke" + "y-" + "0123456789abcdef" * 2,
        "basic_auth_header": "Authorization: Basic " + "dXNlcjpwYXNzd29yZA==",
        "credential_cli_flag": "--pass" + "word " + "hunter2hunter2",
        "credential_assignment_ar": "كلمة المرور: " + "hunter2hunter2",
    }


def quoted_samples() -> list:
    """Credential shapes the plain key=value rule used to miss (quoted JSON/YAML/Python keys, empty URL user, app tokens)."""
    a = "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6"
    return ['{"api_' + 'key": "' + a + '"}', '{"pass' + 'word": "' + "hunter2hunter2" + '"}', "{'tok" + "en': '" + a + "'}",
            "redis://:" + "s3cretP4ss" + "@cache.example.com:6379", "xa" + "pp-1-A0123456789-" + a, "DB_P" + "WD=" + "s3cr3tpass99",
            "client_" + "secret: " + a, "--api" + "-key=" + a]


class Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name).resolve()
        self.root = self.tmp / "ff"
        self.catalog = self.tmp / "catalog.json"
        self.tools = self.tmp / "tools.json"
        self.brief = self.tmp / "brief.json"
        self.catalog.write_text(json.dumps(CATALOG, ensure_ascii=False), encoding="utf-8")
        self.tools.write_text(json.dumps(TOOLS), encoding="utf-8")
        self.brief.write_text(json.dumps(BRIEF, ensure_ascii=False, indent=1), encoding="utf-8")
        self.n_ev = 0

    # ------------------------------------------------------------ helpers
    def run_cli(self, *args, root=None, now=NOW, catalog=None, fixtures=True, json_out=True, cwd=None, env_extra=None):
        cmd = [sys.executable, str(SCRIPT), "--root", str(root or self.root)]
        if fixtures:
            cmd += ["--catalog-file", str(catalog or self.catalog), "--tools-file", str(self.tools)]
        if now:
            cmd += ["--now", now]
        cmd += list(args) + (["--json"] if json_out else [])
        env = dict(os.environ)
        env.pop("KOSIF_FUSIONFORGE_ROOT", None)
        env.update(env_extra or {})
        return subprocess.run(cmd, cwd=str(cwd or self.tmp), capture_output=True, text=True, timeout=180, env=env)

    def ok(self, *args, **kw):
        r = self.run_cli(*args, **kw)
        self.assertEqual(r.returncode, 0, f"{args}: {r.stderr}")
        self.assertNotIn("Traceback", r.stderr)
        return json.loads(r.stdout) if kw.get("json_out", True) else r.stdout

    def refused(self, code, *args, rc=2, **kw):
        r = self.run_cli(*args, **kw)
        self.assertEqual(r.returncode, rc, f"{args}: expected rc {rc} got {r.returncode}: {r.stderr}")
        self.assertNotIn("Traceback", r.stderr)
        line = [l for l in r.stderr.splitlines() if l.startswith("fusionforge: error:")]
        self.assertTrue(line, r.stderr)
        self.assertIn(f"fusionforge: error: {code}:", line[-1], r.stderr)
        return r

    def evidence(self, text=None, name=None):
        self.n_ev += 1
        p = self.tmp / (name or f"qa-{self.n_ev}.json")
        p.write_text(text or json.dumps({"check": self.n_ev, "pass": True}), encoding="utf-8")
        return str(p)

    def propose(self, project="alpha", goal=GOAL, now=NOW, rid=None, brief=None, **kw):
        args = ["propose", goal, "--project", project, "--from-brief", str(brief or self.brief)]
        if rid:
            args += ["--id", rid]
        return self.ok(*args, now=now, **kw)["recipe"]

    def show(self, rid, project="alpha", **kw):
        return self.ok("show", "--project", project, "--id", rid, **kw)["recipe"]

    def path_of(self, rid, project="alpha", root=None):
        return (root or self.root) / project / "recipes" / f"{rid}.json"

    def edit(self, rid, fn, project="alpha"):
        p = self.path_of(rid, project)
        r = json.loads(p.read_text(encoding="utf-8"))
        fn(r)
        p.write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")

    def choose(self, rid, plan="A", project="alpha", now=NOW, **kw):
        return self.ok("choose", "--project", project, "--id", rid, "--plan", plan, "--why", "smallest plan that covers every must-have", now=now, **kw)

    def trace(self, rid, node, stage, result="passed", project="alpha", now=NOW, evidence=True, extra=()):
        args = ["trace", "--project", project, "--id", rid, "--stage", stage, "--node", node, "--result", result,
                "--action", f"ran {node}", "--observed", f"{node} {result}"] + list(extra)
        if evidence:
            args += ["--evidence", self.evidence() if evidence is True else evidence]
        return self.ok(*args, now=now)

    def run_plan(self, rid, project="alpha", now=NOW, skip=()):
        r = self.show(rid, project)
        nodes = {n["id"]: n for n in r["nodes"]}
        for nid in r["plan_choice"]["nodes"]:
            if nid in skip:
                continue
            self.trace(rid, nid, nodes[nid]["stage"], project=project, now=now)
        return r

    def to_tested(self, project="alpha", goal=GOAL, now=NOW, plan="A"):
        rid = self.propose(project, goal, now=now)["id"]
        self.choose(rid, plan, project, now=now)
        self.run_plan(rid, project, now=now)
        self.ok("record", "--project", project, "--id", rid, "--status", "tested", "--evidence", self.evidence(), now=now)
        return rid

    def to_verified(self, project="alpha", goal=GOAL, now=NOW, plan="A"):
        rid = self.to_tested(project, goal, now, plan)
        self.ok("record", "--project", project, "--id", rid, "--status", "verified", "--evidence", self.evidence(), "--qa-pass", now=now)
        return rid

    def codes(self, out):
        return {e["name"] for e in out["errors"]}, {w["name"] for w in out["warnings"]}


class ProposeTests(Base):
    def test_from_brief_builds_typed_nodes_plans_and_edges(self):
        out = self.ok("propose", GOAL, "--project", "alpha", "--from-brief", str(self.brief), "--id", FIXED_ID)
        r = out["recipe"]
        self.assertEqual(out["root"], str(self.root))
        self.assertEqual((r["schema"], r["status"], r["id"]), ("kosif.fusionforge.recipe.v2", "candidate", FIXED_ID))
        self.assertEqual(len(r["status_log"]), 1)
        nodes = {n["id"]: n for n in r["nodes"]}
        self.assertEqual(r["plans"]["A"]["nodes"], ["N01", "N02", "N03", "N04"])
        self.assertEqual(r["plans"]["B"]["nodes"], ["N01", "N05", "N06", "N03", "N04"])
        self.assertEqual(r["plans"]["C"]["nodes"], ["N01", "N07", "N06", "N03", "N04"])
        self.assertEqual(r["plans"]["A"]["label"], "simplest path that meets every must-have")
        self.assertEqual([nodes[n]["stage"] for n in r["plans"]["B"]["nodes"]], ["understand", "create", "refine", "verify", "deliver"])
        brief_caps = {c for p in BRIEF["plans"].values() for ids in p["stages"].values() for c in ids}
        self.assertEqual({c for n in r["nodes"] for c in n["capability_ids"]}, brief_caps)
        self.assertEqual(nodes["N02"]["outputs"][0]["kind"], "video")
        self.assertEqual(nodes["N02"]["executor"]["ref"], "tool:fixture-render")
        self.assertEqual(nodes["N03"]["executor"]["ref"], "tool:fixture-qa")
        self.assertEqual(nodes["N04"]["executor"], {"ref": "tool:fixture-pack", "runnable": "missing", "source": "brief_tool_family_match"})
        self.assertEqual(nodes["N01"]["executor"]["ref"], "method:PLN-01")
        self.assertTrue(all(n["contract_source"] == "default_unconfirmed" and n["status"] == "pending" for n in r["nodes"]))
        kinds = {(e["from"], e["to"]): e["kind"] for e in r["edges"]}
        self.assertEqual(kinds[("N01", "N02")], "spec")
        self.assertEqual(kinds[("N02", "N03")], "video")
        self.assertEqual(kinds[("N03", "N04")], "evidence")
        self.assertEqual(len(r["edges"]), 8)
        self.assertEqual(r["suggested_plan"], "B")
        self.assertIsNone(r["plan_choice"])
        fp = r["capabilities"]["SP-0001"]
        self.assertEqual(fp["atoms"], ["VID-01", "VID-02", "VID-03"])
        self.assertEqual(fp["atoms_sha256"], hashlib.sha256(b"VID-01,VID-02,VID-03").hexdigest())
        self.assertEqual([s["to"] for s in r["similar_unverified"]], ["SP-0007"])
        self.assertNotIn("SP-0007", {c for n in r["nodes"] for c in n["capability_ids"]})
        saved = self.root / "alpha" / "recipes" / f"{FIXED_ID}.brief.json"
        self.assertEqual(saved.read_bytes(), self.brief.read_bytes())
        self.assertEqual(r["brief"]["sha256"], hashlib.sha256(self.brief.read_bytes()).hexdigest())
        self.assertIn("LEARNING_INDEX_EMPTY", r["warnings"])
        self.assertTrue(out["validate"]["ok"], out["validate"])

    def test_max_capabilities_trims_later_plans_first(self):
        r = self.ok("propose", GOAL, "--project", "alpha", "--from-brief", str(self.brief), "--max-capabilities", "4")["recipe"]
        self.assertEqual(sorted(r["capabilities"]), ["SP-0001", "SP-0004", "SP-0005", "SP-0006"])
        self.assertEqual(r["plans"]["A"]["nodes"], ["N01", "N02", "N03", "N04"])
        self.refused("USAGE", "propose", GOAL, "--project", "alpha", "--from-brief", str(self.brief), "--max-capabilities", "0")

    def test_root_resolution_env_then_git(self):
        env_root = self.tmp / "env-root"
        cmd = [sys.executable, str(SCRIPT), "catalog", "--project", "alpha", "--json"]
        env = dict(os.environ, KOSIF_FUSIONFORGE_ROOT=str(env_root))
        out = subprocess.run(cmd, cwd=str(self.tmp), capture_output=True, text=True, timeout=60, env=env)
        self.assertEqual(json.loads(out.stdout)["root"], str(env_root))
        repo = self.tmp / "repo"
        repo.mkdir()
        if subprocess.run(["git", "init", "-q", str(repo)], capture_output=True).returncode != 0:
            self.skipTest("git is not available")
        env.pop("KOSIF_FUSIONFORGE_ROOT")
        out = subprocess.run(cmd, cwd=str(repo), capture_output=True, text=True, timeout=60, env=env)
        self.assertEqual(json.loads(out.stdout)["root"], str(repo / "out" / "fusionforge"))
        self.assertFalse((repo / "out").exists())
        prop = [sys.executable, str(SCRIPT), "--catalog-file", str(self.catalog), "--tools-file", str(self.tools), "--now", NOW,
                "propose", GOAL, "--project", "alpha", "--from-brief", str(self.brief)]
        out = subprocess.run(prop, cwd=str(repo), capture_output=True, text=True, timeout=60, env=env)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("fusionforge: warning: ROOT_NOT_GITIGNORED", out.stderr)
        (repo / ".gitignore").write_text("out/\n", encoding="utf-8")
        out = subprocess.run(prop, cwd=str(repo), capture_output=True, text=True, timeout=60, env=env)
        self.assertEqual((out.returncode, out.stderr), (0, ""))

    def test_default_output_is_compact(self):
        text = self.ok("propose", GOAL, "--project", "alpha", "--from-brief", str(self.brief), json_out=False)
        self.assertLessEqual(len(text.strip().splitlines()), 25)
        self.assertIn("FUSE-", text)

    def test_no_match_and_incomplete_brief_and_usage_errors(self):
        b = dict(BRIEF, plans={}, analysis=dict(BRIEF["analysis"], level="L0"))
        nb = self.tmp / "l0.json"
        nb.write_text(json.dumps(b, ensure_ascii=False), encoding="utf-8")
        r = self.refused("NO_MATCH", "propose", "اشرح كلمة", "--project", "alpha", "--from-brief", str(nb), rc=3)
        self.assertIn("--terms", r.stderr)
        self.assertFalse((self.root / "alpha" / "recipes").exists())
        nb.write_text(json.dumps(dict(BRIEF, coverage={"complete": False}), ensure_ascii=False), encoding="utf-8")
        self.refused("BRIEF_INCOMPLETE", "propose", GOAL, "--project", "alpha", "--from-brief", str(nb))
        self.refused("BAD_PROJECT", "propose", GOAL, "--project", "../x", "--from-brief", str(self.brief))
        self.refused("USAGE", "no-such-command")
        self.refused("BAD_ID", "show", "--project", "alpha", "--id", "../../etc")

    def test_real_catalog_smoke_never_tracebacks(self):
        r = self.run_cli("propose", "طور البرتكول وارفعه", "--project", "smoke", fixtures=False, now=None)
        self.assertNotIn("Traceback", r.stderr)
        self.assertIn(r.returncode, (0, 3), r.stderr)
        if r.returncode == 0:
            rec = json.loads(r.stdout)["recipe"]
            self.assertTrue(rec["nodes"])
            self.assertTrue(any(n["stage"] == "verify" for n in rec["nodes"]))
            v = self.run_cli("validate", "--project", "smoke", "--id", rec["id"], fixtures=False, now=None)
            self.assertIn(v.returncode, (0, 4), v.stderr)
            self.assertNotIn("Traceback", v.stderr)
        else:
            self.assertIn("NO_MATCH", r.stderr)

    def test_determinism_without_a_brief_file(self):
        roots, env = [self.tmp / "d1", self.tmp / "d2"], {"PYTHONHASHSEED": "0"}  # the brief's own tie order is the router's job
        for root in roots:
            r = self.run_cli("propose", "طور البرتكول وارفعه", "--project", "det", "--id", FIXED_ID, root=root, fixtures=False, env_extra=env)
            if r.returncode == 3:
                self.skipTest("the real catalog has no match for the smoke goal")
            self.assertEqual(r.returncode, 0, r.stderr)
        for rel in (f"det/recipes/{FIXED_ID}.json", f"det/recipes/{FIXED_ID}.brief.json", "det/index.json"):
            self.assertEqual((roots[0] / rel).read_bytes(), (roots[1] / rel).read_bytes(), rel)
        brief = json.loads((roots[0] / f"det/recipes/{FIXED_ID}.brief.json").read_text(encoding="utf-8"))
        self.assertEqual((brief["elapsed_s"], brief["coverage"]["scanned_at"]), (None, NOW))

    def test_determinism_with_now_and_id(self):
        roots = [self.tmp / "r1", self.tmp / "r2"]
        for root in roots:
            self.ok("propose", GOAL, "--project", "alpha", "--from-brief", str(self.brief), "--id", FIXED_ID, root=root)
            self.ok("card", "--project", "alpha", "--id", FIXED_ID, root=root)
        for rel in (f"alpha/recipes/{FIXED_ID}.json", f"alpha/recipes/{FIXED_ID}.brief.json", "alpha/index.json", f"alpha/cards/{FIXED_ID}.md"):
            self.assertEqual((roots[0] / rel).read_bytes(), (roots[1] / rel).read_bytes(), rel)


class ValidateChooseTests(Base):
    def test_validate_codes(self):
        rid = self.propose()["id"]
        clean = self.ok("validate", "--project", "alpha", "--id", rid)
        self.assertTrue(clean["ok"])
        self.edit(rid, lambda r: r["edges"][0].update(kind="audio"))
        out = json.loads(self.refused("VALIDATE_ERRORS", "validate", "--project", "alpha", "--id", rid, rc=4).stdout)
        err = {(e["code"], e["name"]) for e in out["errors"]}
        self.assertIn(("V03", "HANDOFF_KIND_MISMATCH"), err)
        self.edit(rid, lambda r: (r["edges"][0].update(kind="spec"), r["nodes"][1]["executor"].update(ref="tool:does-not-exist")))
        out = json.loads(self.refused("VALIDATE_ERRORS", "validate", "--project", "alpha", "--id", rid, rc=4).stdout)
        self.assertEqual({(e["code"], e["name"]) for e in out["errors"]}, {("V05", "EXECUTOR_UNKNOWN")})
        self.edit(rid, lambda r: (r["nodes"][1]["executor"].update(ref="tool:fixture-render"), r["plans"]["A"].update(nodes=["N01", "N02"])))
        out = json.loads(self.refused("VALIDATE_ERRORS", "validate", "--project", "alpha", "--id", rid, rc=4).stdout)
        self.assertIn("NO_FINAL_VERIFY", self.codes(out)[0])
        self.edit(rid, lambda r: (r["plans"]["A"].update(nodes=["N01", "N02", "N03", "N04"]), r.update(status="tested")))
        out = json.loads(self.refused("VALIDATE_ERRORS", "validate", "--project", "alpha", "--id", rid, rc=4).stdout)
        self.assertIn("STATE_LOG_INVALID", self.codes(out)[0])
        token = secret_samples()["github_token"]
        self.edit(rid, lambda r: r.update(status="candidate", goal=GOAL + " " + token))
        r = self.refused("VALIDATE_ERRORS", "validate", "--project", "alpha", "--id", rid, rc=4)
        self.assertIn("SECRET", self.codes(json.loads(r.stdout))[0])
        self.assertNotIn(token, r.stdout + r.stderr)

    def test_choose_records_plan_and_rejects_bad_choices(self):
        rid = self.propose()["id"]
        self.refused("USAGE", "choose", "--project", "alpha", "--id", rid, "--plan", "D", "--why", "merge")
        self.refused("USAGE", "choose", "--project", "alpha", "--id", rid, "--plan", "B", "--why", "x", "--nodes", "N01")
        self.refused("UNKNOWN_NODE", "choose", "--project", "alpha", "--id", rid, "--plan", "D", "--why", "merge", "--nodes", "N01,N99")
        out = self.ok("choose", "--project", "alpha", "--id", rid, "--plan", "B", "--why", "best balance for captions")
        self.assertEqual(out["status"], "planned")
        r = self.show(rid)
        self.assertEqual(r["plan_choice"]["plan"], "B")
        self.assertEqual(r["plan_choice"]["why"], "best balance for captions")
        self.assertEqual(r["plan_choice"]["nodes"], r["plans"]["B"]["nodes"])
        self.assertEqual([(s["from"], s["to"], s["cmd"]) for s in r["status_log"]], [(None, "candidate", "propose"), ("candidate", "planned", "choose")])
        self.refused("ILLEGAL_TRANSITION", "choose", "--project", "alpha", "--id", rid, "--plan", "A", "--why", "again")
        rid2 = self.propose()["id"]
        self.edit(rid2, lambda r: r["nodes"][1]["executor"].update(ref="tool:nope"))
        self.refused("VALIDATE_ERRORS", "choose", "--project", "alpha", "--id", rid2, "--plan", "A", "--why", "x")
        rid3 = self.propose()["id"]
        out = self.ok("choose", "--project", "alpha", "--id", rid3, "--plan", "D", "--why", "A's cut with C's verify", "--nodes", "N01,N02,N07,N03,N04")
        r3 = self.show(rid3)
        self.assertEqual(r3["plan_choice"]["nodes"], ["N01", "N02", "N07", "N03", "N04"])
        pairs = {(e["from"], e["to"]) for e in r3["edges"]}
        self.assertTrue({("N02", "N03"), ("N07", "N03"), ("N01", "N07")} <= pairs)

    def test_set_graph_and_bind(self):
        rid = self.propose()["id"]
        graph = {"nodes": [
            {"id": "U1", "stage": "understand", "capability_ids": ["SP-0005"], "inputs": [{"name": "req", "kind": "brief"}],
             "outputs": [{"name": "card", "kind": "spec"}], "executor": "human"},
            {"id": "C1", "stage": "create", "capability_ids": ["SP-0001"], "inputs": [{"name": "card", "kind": "spec"}],
             "outputs": [{"name": "cut", "kind": "video"}], "executor": "tool:fixture-render"},
            {"id": "V1", "stage": "verify", "capability_ids": ["SP-0004"], "inputs": [{"name": "cut", "kind": "video"}],
             "outputs": [{"name": "qa", "kind": "evidence"}], "executor": {"ref": "tool:fixture-qa"}}],
            "edges": [{"from": "U1", "to": "C1", "kind": "spec"}, {"from": "C1", "to": "V1", "kind": "video", "relation": "verify"}],
            "plans": {"A": {"idea": "lean", "nodes": ["U1", "C1", "V1"]}}}
        bad = json.loads(json.dumps(graph))
        bad["edges"][1]["kind"] = "audio"
        gf = self.tmp / "graph.json"
        gf.write_text(json.dumps(bad), encoding="utf-8")
        r = self.refused("GRAPH_INVALID", "set-graph", "--project", "alpha", "--id", rid, "--file", str(gf))
        self.assertIn("V03", r.stderr)
        gf.write_text(json.dumps(graph), encoding="utf-8")
        out = self.ok("set-graph", "--project", "alpha", "--id", rid, "--file", str(gf))
        self.assertEqual((out["nodes"], out["edges"], out["plans"]), (3, 2, ["A"]))
        rec = self.show(rid)
        self.assertEqual({n["contract_source"] for n in rec["nodes"]}, {"model"})
        self.refused("EXECUTOR_UNKNOWN", "bind", "--project", "alpha", "--id", rid, "--node", "C1", "--executor", "tool:nope")
        self.refused("UNKNOWN_NODE", "bind", "--project", "alpha", "--id", rid, "--node", "Z9", "--executor", "human")
        out = self.ok("bind", "--project", "alpha", "--id", rid, "--node", "C1", "--executor", "bin:ffmpeg")
        self.assertEqual(out["executor"]["ref"], "bin:ffmpeg")
        self.ok("choose", "--project", "alpha", "--id", rid, "--plan", "A", "--why", "lean")
        self.refused("ILLEGAL_STATE", "set-graph", "--project", "alpha", "--id", rid, "--file", str(gf))


class StateMachineTests(Base):
    def test_every_illegal_transition_is_refused(self):
        ev = self.evidence()
        cand = self.propose()["id"]
        planned = self.propose()["id"]
        self.choose(planned)
        tested = self.to_tested()
        verified = self.to_verified()
        failed = self.propose()["id"]
        self.ok("record", "--project", "alpha", "--id", failed, "--status", "failed", "--evidence", self.evidence(), "--note", "brief was wrong")
        illegal = {cand: ["tested", "verified"], planned: ["planned", "verified"], tested: ["planned"],
                   verified: ["planned", "tested", "verified", "failed"], failed: ["planned", "tested", "verified", "failed"]}
        for rid, targets in illegal.items():
            for st in targets:
                with self.subTest(rid=rid, to=st):
                    extra = ["--qa-pass"] if st == "verified" else []
                    self.refused("USE_CHOOSE" if st == "planned" else "ILLEGAL_TRANSITION", "record", "--project", "alpha", "--id", rid, "--status", st, "--evidence", ev, *extra)
        self.refused("USE_CHOOSE", "record", "--project", "alpha", "--id", cand, "--status", "planned")
        self.refused("USAGE", "record", "--project", "alpha", "--id", cand, "--status", "candidate")
        for rid in (verified, failed):
            self.refused("TERMINAL_RECIPE", "trace", "--project", "alpha", "--id", rid, "--stage", "create", "--action", "late")
        self.refused("ILLEGAL_TRANSITION", "choose", "--project", "alpha", "--id", planned, "--plan", "B", "--why", "again")
        log = self.show(verified)["status_log"]
        self.assertEqual([s["to"] for s in log], ["candidate", "planned", "tested", "verified"])
        self.assertTrue(all(s["evidence_sha256"] for s in log[2:]))

    def test_tested_needs_a_run_and_evidence(self):
        rid = self.propose()["id"]
        self.choose(rid)
        self.refused("EVIDENCE_REQUIRED", "record", "--project", "alpha", "--id", rid, "--status", "tested")
        self.refused("NO_RUN", "record", "--project", "alpha", "--id", rid, "--status", "tested", "--evidence", self.evidence())
        self.ok("trace", "--project", "alpha", "--id", rid, "--stage", "create", "--action", "note without result")
        self.refused("NO_RUN", "record", "--project", "alpha", "--id", rid, "--status", "tested", "--evidence", self.evidence())
        self.refused("USAGE", "record", "--project", "alpha", "--id", rid, "--status", "failed", "--evidence", self.evidence(), "--qa-pass")


class TraceTests(Base):
    def test_trace_updates_node_and_records_substitution(self):
        rid = self.propose()["id"]
        self.choose(rid)
        out = self.trace(rid, "N02", "create", "failed", evidence=True, extra=("--error-class", "missing_dependency"))
        self.assertEqual(out["node_status"], "failed")
        self.assertEqual(out["trace"]["tool"], "tool:fixture-render")
        self.assertIsNone(out["trace"]["substitution"])
        out = self.trace(rid, "N02", "create", "passed", extra=("--tool", "bin:ffmpeg", "--capabilities", "SP-0001"))
        self.assertEqual(out["trace"]["substitution"], {"planned": "tool:fixture-render", "used": "bin:ffmpeg"})
        r = self.show(rid)
        n02 = next(n for n in r["nodes"] if n["id"] == "N02")
        self.assertEqual((n02["status"], n02["last_trace"]), ("passed", 2))
        ev = r["traces"][0]["evidence"]
        self.assertEqual(len(ev["sha256"]), 64)
        self.assertTrue((self.root / "alpha" / ev["stored"]).is_file())
        self.assertFalse(ev["source"].startswith("/"))
        self.assertNotIn(str(self.tmp), json.dumps(r, ensure_ascii=False))
        self.refused("UNKNOWN_CAPABILITY", "trace", "--project", "alpha", "--id", rid, "--stage", "create", "--node", "N02",
                  "--result", "passed", "--action", "x", "--capabilities", "SP-9999")
        self.refused("SKIP_NEEDS_OBSERVED", "trace", "--project", "alpha", "--id", rid, "--stage", "deliver", "--node", "N04",
                  "--result", "skipped", "--action", "not needed")
        self.ok("trace", "--project", "alpha", "--id", rid, "--stage", "deliver", "--node", "N04", "--result", "skipped",
                "--action", "not needed", "--observed", "the user downloads the file directly")
        self.refused("UNKNOWN_NODE", "trace", "--project", "alpha", "--id", rid, "--stage", "create", "--node", "N99", "--result", "passed", "--action", "x")
        self.refused("STAGE_MISMATCH", "trace", "--project", "alpha", "--id", rid, "--stage", "verify", "--node", "N02", "--result", "passed", "--action", "x")
        self.refused("NODE_NOT_IN_PLAN", "trace", "--project", "alpha", "--id", rid, "--stage", "refine", "--node", "N06", "--result", "passed", "--action", "x")
        self.refused("EXECUTOR_UNKNOWN", "trace", "--project", "alpha", "--id", rid, "--stage", "create", "--node", "N02", "--result", "passed",
                  "--action", "x", "--tool", "tool:not-registered")
        self.refused("USAGE", "trace", "--project", "alpha", "--id", rid, "--stage", "create", "--node", "N02", "--result", "passed",
                  "--action", "x", "--error-class", "timeout")
        v1 = self.ok("trace", "--project", "alpha", "--id", rid, "--stage", "create", "--action", "Executed renderer", "--tool", "mock-render")
        self.assertEqual(v1["trace"]["tool"], "bin:mock-render")
        self.assertIsNone(v1["node_status"])

    def test_parallel_traces_store_every_entry(self):
        rid = self.propose()["id"]
        base = [sys.executable, str(SCRIPT), "--root", str(self.root), "--catalog-file", str(self.catalog), "--tools-file", str(self.tools),
                "--now", NOW, "trace", "--project", "alpha", "--id", rid, "--stage", "create"]
        procs = [subprocess.Popen(base + ["--action", f"parallel step {i}"], cwd=str(self.tmp), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                 for i in range(10)]
        results = [(p.wait(timeout=120), p.stdout.read(), p.stderr.read()) for p in procs]
        for p in procs:
            p.stdout.close()
            p.stderr.close()
        self.assertEqual([rc for rc, _o, _e in results], [0] * 10, [e for _rc, _o, e in results])
        traces = self.show(rid)["traces"]
        self.assertEqual(len(traces), 10)
        self.assertEqual(sorted(t["seq"] for t in traces), list(range(1, 11)))
        self.assertEqual(sorted(t["action"] for t in traces), sorted(f"parallel step {i}" for i in range(10)))


class VerifiedGateTests(Base):
    def make_tested(self, skip=()):
        rid = self.propose()["id"]
        self.choose(rid)
        self.run_plan(rid, skip=skip)
        self.ok("record", "--project", "alpha", "--id", rid, "--status", "tested", "--evidence", self.evidence())
        return rid

    def verify(self, rid, ev=None, qa=True, code=None):
        args = ["record", "--project", "alpha", "--id", rid, "--status", "verified", "--evidence", ev or self.evidence()] + (["--qa-pass"] if qa else [])
        return self.refused(code, *args) if code else self.ok(*args)

    def test_gate_negatives(self):
        rid = self.make_tested(skip=("N04",))
        self.verify(rid, code="GATE_NODE_NOT_PASSED")
        self.verify(rid, qa=False, code="QA_PASS_REQUIRED")
        rid2 = self.propose()["id"]
        self.choose(rid2)
        r = self.show(rid2)
        for nid in r["plan_choice"]["nodes"]:
            st = next(n["stage"] for n in r["nodes"] if n["id"] == nid)
            self.trace(rid2, nid, st, evidence=(st != "verify"))
        self.ok("record", "--project", "alpha", "--id", rid2, "--status", "tested", "--evidence", self.evidence())
        self.verify(rid2, code="GATE_NO_VERIFY_EVIDENCE")
        rid3 = self.make_tested()
        own = self.path_of(rid3)
        self.verify(rid3, ev=str(own), code="SELF_EVIDENCE")
        self.verify(rid3, ev=str(self.root / "alpha" / "index.json"), code="SELF_EVIDENCE")
        link = self.tmp / "innocent_qa.json"
        os.symlink(self.evidence(), link)
        self.verify(rid3, ev=str(link), code="EVIDENCE_SYMLINK")
        system = next((p for p in ("/etc/hostname", "/etc/passwd", "/etc/hosts") if Path(p).is_file() and Path(p).stat().st_size), None)
        if system:
            self.verify(rid3, ev=system, code="EVIDENCE_OUTSIDE_ALLOWED")
        empty = self.tmp / "empty.json"
        empty.write_text("", encoding="utf-8")
        self.verify(rid3, ev=str(empty), code="EVIDENCE_EMPTY")
        self.assertEqual(self.show(rid3)["status"], "tested")

    def test_failure_evidence_cannot_be_reused(self):
        rid = self.propose()["id"]
        self.choose(rid)
        bad = self.evidence('{"frames_black": 12}', name="fail.json")
        self.trace(rid, "N03", "verify", "failed", evidence=bad, extra=("--error-class", "quality_below_threshold"))
        self.run_plan(rid)
        self.ok("record", "--project", "alpha", "--id", rid, "--status", "tested", "--evidence", self.evidence())
        self.verify(rid, ev=bad, code="GATE_FAILURE_EVIDENCE_REUSED")
        rid2 = self.propose()["id"]
        self.choose(rid2)
        bad2 = self.evidence('{"loudness": -9}', name="fail2.json")
        self.trace(rid2, "N03", "verify", "failed", evidence=bad2)
        self.run_plan(rid2, skip=("N03",))
        self.trace(rid2, "N03", "verify", "passed", evidence=bad2)
        self.ok("record", "--project", "alpha", "--id", rid2, "--status", "tested", "--evidence", self.evidence())
        self.verify(rid2, code="GATE_FAILURE_EVIDENCE_REUSED")

    def test_qa_evidence_cannot_verify_two_recipes_and_baseline_is_kept(self):
        qa = self.evidence('{"qa": "pass", "lufs": -14}', name="shared-qa.json")
        first = self.make_tested()
        base = self.evidence('{"lufs": -9}', name="baseline.json")
        self.refused("BASELINE_SAME_AS_EVIDENCE", "record", "--project", "alpha", "--id", first, "--status", "verified",
                     "--evidence", qa, "--qa-pass", "--baseline", qa)
        self.ok("record", "--project", "alpha", "--id", first, "--status", "verified", "--evidence", qa, "--qa-pass", "--baseline", base)
        self.assertEqual(self.show(first)["baseline"]["sha256"], hashlib.sha256(Path(base).read_bytes()).hexdigest())
        second = self.make_tested()
        self.verify(second, ev=qa, code="GATE_EVIDENCE_REUSED")
        self.verify(second)

    def test_results_count_only_after_choose_and_failure_needs_a_note(self):
        rid = self.propose()["id"]
        self.refused("PLAN_NOT_CHOSEN", "trace", "--project", "alpha", "--id", rid, "--stage", "create", "--node", "N02",
                     "--result", "passed", "--action", "ran before approval")
        self.ok("trace", "--project", "alpha", "--id", rid, "--stage", "create", "--action", "prepared footage")
        self.edit(rid, lambda r: [n.update(status="passed") for n in r["nodes"]])
        self.choose(rid)
        self.assertEqual({n["status"] for n in self.show(rid)["nodes"]}, {"pending"})
        self.refused("NOTE_REQUIRED", "record", "--project", "alpha", "--id", rid, "--status", "failed", "--evidence", self.evidence())
        self.refused("NOTE_REQUIRED", "record", "--project", "alpha", "--id", rid, "--status", "failed", "--evidence", self.evidence(), "--note", "  ")

    def test_failure_evidence_of_a_parent_or_sibling_cannot_verify_a_fork(self):
        parent = self.propose()["id"]
        fail = self.evidence('{"errors": 12}', name="qa_fail.json")
        self.ok("record", "--project", "alpha", "--id", parent, "--status", "failed", "--evidence", fail, "--note", "QA failed: 12 errors")
        fork = self.ok("fork", "--project", "alpha", "--id", parent)["recipe"]["id"]
        self.choose(fork)
        r = self.show(fork)
        nodes = {n["id"]: n for n in r["nodes"]}
        for nid in r["plan_choice"]["nodes"]:
            self.trace(fork, nid, nodes[nid]["stage"], evidence=fail if nodes[nid]["stage"] == "verify" else True)
        self.ok("record", "--project", "alpha", "--id", fork, "--status", "tested", "--evidence", self.evidence())
        self.verify(fork, ev=fail, code="GATE_FAILURE_EVIDENCE_REUSED")
        self.verify(fork, code="GATE_FAILURE_EVIDENCE_REUSED")  # the verify node's own QA is the failed one

    def test_verify_trace_evidence_cannot_verify_two_recipes(self):
        qa = self.evidence('{"qa": "pass", "frames": 300}', name="qa.json")
        recs = []
        for _ in range(2):
            rid = self.propose()["id"]
            self.choose(rid)
            r = self.show(rid)
            nodes = {n["id"]: n for n in r["nodes"]}
            for nid in r["plan_choice"]["nodes"]:
                self.trace(rid, nid, nodes[nid]["stage"], evidence=qa if nodes[nid]["stage"] == "verify" else True)
            self.ok("record", "--project", "alpha", "--id", rid, "--status", "tested", "--evidence", self.evidence())
            recs.append(rid)
        self.verify(recs[0])
        r = self.verify(recs[1], code="GATE_EVIDENCE_REUSED")
        self.assertIn(recs[0], r.stderr)

    def test_imported_results_need_a_local_verify_run_before_verified_or_promote(self):
        rid = self.make_tested()
        bundle = self.tmp / "tested.json"
        self.ok("export", "--project", "alpha", "--out", str(bundle))
        root2 = self.tmp / "machine2"
        self.ok("import", str(bundle), "--project", "alpha", root=root2)
        args = ["record", "--project", "alpha", "--id", rid, "--status", "verified", "--evidence", self.evidence(), "--qa-pass"]
        self.refused("GATE_EVIDENCE_NOT_LOCAL", *args, root=root2)
        imp = self.show(rid, root=root2)
        self.assertEqual(imp["import_receipt"]["trace_seq"], max(t["seq"] for t in imp["traces"]))
        self.ok("trace", "--project", "alpha", "--id", rid, "--stage", "verify", "--node", "N03", "--result", "passed",
                "--action", "re-ran the QA here", "--evidence", self.evidence(), root=root2)
        self.ok(*args, root=root2)
        self.ok("promote", "--project", "alpha", "--id", rid, root=root2)
        verified = self.to_verified()
        self.ok("export", "--project", "alpha", "--out", str(bundle))
        root3 = self.tmp / "machine3"
        self.ok("import", str(bundle), "--project", "alpha", root=root3)
        self.refused("NOT_PROVEN", "promote", "--project", "alpha", "--id", verified, root=root3)

    def test_copies_and_hard_links_of_records_are_not_evidence(self):
        rid = self.make_tested()
        own = self.path_of(rid)
        copy = self.tmp / "copy.json"
        copy.write_bytes(own.read_bytes())
        self.verify(rid, ev=str(copy), code="SELF_EVIDENCE")
        link = self.tmp / "hl.json"
        try:
            os.link(own, link)
        except OSError:
            link = None
        if link:
            self.verify(rid, ev=str(link), code="SELF_EVIDENCE")
        card = self.ok("card", "--project", "alpha", "--id", rid, "--out", str(self.tmp / "card.md"))
        self.verify(rid, ev=card["path"], code="SELF_EVIDENCE")
        self.assertEqual(self.show(rid)["status"], "tested")

    def test_positive_path_then_tamper_is_detected(self):
        rid = self.make_tested()
        out = self.verify(rid)
        self.assertEqual(out["status"], "verified")
        clean = self.ok("validate", "--project", "alpha", "--id", rid)
        self.assertTrue(clean["ok"], clean)
        self.assertTrue(clean["reusable"])
        self.assertTrue(next(x for x in self.ok("catalog", "--project", "alpha")["recipes"] if x["id"] == rid)["reusable"])
        r = self.show(rid)
        verify_trace = next(t for t in r["traces"] if t["node"] == "N03")
        stored = self.root / "alpha" / verify_trace["evidence"]["stored"]
        stored.write_text('{"pass": false}', encoding="utf-8")
        before = self.path_of(rid).read_bytes()
        out = json.loads(self.refused("VALIDATE_ERRORS", "validate", "--project", "alpha", "--id", rid, rc=4).stdout)
        self.assertIn(("V07", "EVIDENCE_HASH_MISMATCH"), {(e["code"], e["name"]) for e in out["errors"]})
        self.assertFalse(out["reusable"])
        self.assertEqual(self.path_of(rid).read_bytes(), before)
        reuse = self.ok("reuse", GOAL, "--project", "alpha", "--no-brief")
        m = next(x for x in reuse["matches"] if x["id"] == rid)
        self.assertEqual((m["factors"]["freshness"], m["score"], m["reusable"]), (0.0, 0.0, False))
        again = self.propose()
        self.assertIsNone(again["recall"]["template"])  # revoked evidence teaches nothing
        self.assertFalse(any(n.get("memory") for n in again["nodes"]))
        self.assertIn("MEMORY_SKIPPED_INVALID_PRIORS:1", again["warnings"])


class SecretTests(Base):
    def test_detector_formats_and_clean_texts(self):
        samples = secret_samples()
        self.assertGreaterEqual(len(samples), 12)
        for name, value in samples.items():
            with self.subTest(name=name):
                self.assertIn(name, _secrets.find_secrets(f"note: {value} end"))
        for text in quoted_samples():
            with self.subTest(quoted=text[:12]):
                self.assertTrue(_secrets.find_secrets(text), text[:12])
        for clean in ("مونتاج فيديو بترجمة عربية", "tokens: 12 per line", "use the secret manager", "N01→N02 (spec)",
                      "sha256 " + "ab" * 32, "task-skills-and-more-things-for-video", "https://example.com/a/b",
                      "FUSE-20261021-0123456789", "tool:fixture-render method:PLN-01", "pwd: /home/user/kosif-tool",
                      "explain the token: lifecycle and refresh", "context token: 128000 used", "token=placeholder",
                      "password: <your-password>", "set API_KEY=$OPENAI_API_KEY in env", "api_key: ${API_KEY}", "ran in pwd=/tmp/job",
                      "the --token option is required", "Basic introduction to video", "bearer authentication flow",
                      "ssh://git@host:22/x", "password: ********", "كلمة المرور: <سرية>", "secret: manager"):
            self.assertEqual(_secrets.find_secrets(clean), [], clean)
        a = "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6"
        self.assertEqual(_secrets.scan_object({"cfg": {"api_" + "key": a}, "n": 3}), [("$.cfg.api_" + "key", ["credential_assignment"])])
        with self.assertRaises(_secrets.SecretError) as cm:
            _secrets.refuse_secrets(goal="ok", note=samples["jwt"])
        self.assertEqual(cm.exception.field, "note")
        self.assertNotIn(samples["jwt"], str(cm.exception))

    def test_cli_refuses_secrets_in_every_written_field(self):
        samples = secret_samples()
        values = list(samples.values())
        self.refused("SECRET", "propose", GOAL + " " + samples["github_token"], "--project", "alpha", "--from-brief", str(self.brief))
        self.refused("SECRET", "propose", GOAL, "--project", "alpha", "--from-brief", str(self.brief), "--terms", samples["openai_api_key"])
        self.assertFalse((self.root / "alpha" / "recipes").exists())
        rid = self.propose()["id"]
        self.choose(rid)
        base = ["trace", "--project", "alpha", "--id", rid, "--stage", "create"]
        for i, field in enumerate(("--action", "--tool", "--input", "--output", "--observed")):
            args = base + (["--action", "x"] if field != "--action" else []) + [field, values[i]]
            with self.subTest(field=field):
                r = self.refused("SECRET", *args)
                self.assertNotIn(values[i], r.stderr + r.stdout)
        for name, value in samples.items():
            with self.subTest(observed=name):
                self.refused("SECRET", *(base + ["--action", "x", "--observed", f"saw {value}"]))
        self.refused("SECRET", "record", "--project", "alpha", "--id", rid, "--status", "failed", "--evidence", self.evidence(),
                  "--note", "leaked " + samples["aws_access_key_id"])
        self.refused("SECRET", "choose", "--project", "alpha", "--id", self.propose()["id"], "--plan", "A", "--why", samples["slack_token"])
        for text in quoted_samples():
            with self.subTest(quoted=text[:12]):
                self.refused("SECRET", *(base + ["--action", "x", "--observed=" + text]))
        r = self.show(rid)
        self.assertEqual((len(r["traces"]), r["status"]), (0, "planned"))
        text = "".join(p.read_text(encoding="utf-8") for p in (self.root / "alpha").rglob("*.json"))
        for v in values + quoted_samples():
            self.assertNotIn(v, text)

    def test_project_paths_and_evidence_files_are_scanned(self):
        samples = secret_samples()
        self.refused("SECRET", "propose", GOAL, "--project", samples["github_token"], "--from-brief", str(self.brief))
        self.assertFalse(self.root.exists())
        rid = self.propose()["id"]
        sub = self.tmp / "job"
        sub.mkdir()
        named = sub / (samples["aws_access_key_id"] + ".json")
        named.write_text('{"qa": "fail"}', encoding="utf-8")
        assigned = sub / ("api_" + "key=abcdef123456.txt")
        assigned.write_text("report", encoding="utf-8")
        for flag, path in (("--evidence", named), ("--evidence", assigned), ("--baseline", named)):
            with self.subTest(flag=flag, path=path.name[:8]):
                extra = ["--evidence", self.evidence()] if flag == "--baseline" else []
                self.refused("SECRET", "record", "--project", "alpha", "--id", rid, "--status", "failed", "--note", "broke", flag, str(path), *extra)
        self.refused("SECRET", "trace", "--project", "alpha", "--id", rid, "--stage", "create", "--action", "x", "--evidence", str(named))
        leaky = self.evidence("render ok\nGITHUB_TOKEN=" + samples["github_token"] + "\n", name="render.log")
        self.refused("SECRET", "trace", "--project", "alpha", "--id", rid, "--stage", "create", "--action", "x", "--evidence", leaky)
        dotenv = self.evidence("MODE=prod", name=".env")
        self.refused("EVIDENCE_SENSITIVE", "trace", "--project", "alpha", "--id", rid, "--stage", "create", "--action", "x", "--evidence", dotenv)
        (self.tmp / ".ssh").mkdir()
        (self.tmp / ".ssh" / "notes.txt").write_text("harmless", encoding="utf-8")
        self.refused("EVIDENCE_SENSITIVE", "trace", "--project", "alpha", "--id", rid, "--stage", "create", "--action", "x",
                     "--evidence", str(self.tmp / ".ssh" / "notes.txt"))
        r = self.show(rid)
        self.assertEqual((r["status"], r["traces"]), ("candidate", []))
        stored = b"".join(p.read_bytes() for p in (self.root / "alpha").rglob("*") if p.is_file())
        self.assertNotIn(samples["github_token"].encode(), stored)
        self.assertNotIn(samples["aws_access_key_id"].encode(), stored)


class RobustnessTests(Base):
    def test_corrupt_siblings_do_not_break_commands(self):
        rid = self.propose()["id"]
        rdir = self.root / "alpha" / "recipes"
        (rdir / "FUSE-20261021-ffffffffff.json").write_text("{not json", encoding="utf-8")
        (rdir / "FUSE-20261021-eeeeeeeeee.json").write_bytes(b"\xff\xfe\x00\x81")
        (rdir / "FUSE-20261021-dddddddddd.json").write_text('{"status": "verified"}', encoding="utf-8")
        cat = self.ok("catalog", "--project", "alpha")
        self.assertEqual(cat["total"], 1)
        self.assertEqual(len(cat["invalid_files"]), 3)
        self.assertEqual(self.show(rid)["id"], rid)
        self.ok("reuse", GOAL, "--project", "alpha", "--no-brief")
        self.ok("trace", "--project", "alpha", "--id", rid, "--stage", "create", "--action", "still works")
        self.ok("lessons", "--project", "alpha")
        index = json.loads((self.root / "alpha" / "index.json").read_text(encoding="utf-8"))
        self.assertEqual(len(index["invalid_files"]), 3)
        self.refused("RECIPE_UNREADABLE", "show", "--project", "alpha", "--id", "FUSE-20261021-ffffffffff")

    def test_malformed_record_gives_validate_errors_not_a_crash(self):
        rid = self.propose()["id"]

        def junk(r):
            r["edges"] += ["x", {"from": ["N01"], "to": "N02", "id": "E99"}, {"id": "E98", "from": "N01", "to": "N09"}]
            r["nodes"].append("junk")
            r["capabilities"]["SP-0001"] = "junk"
            r["plans"]["B"] = "junk"
            r["plan_choice"] = {"plan": "A", "why": 3, "nodes": [["N01"]], "at": None}
            r["traces"] += ["junk", {"seq": "x"}]
            r["evidence"].append("junk")
            r["status_log"].append(5)
        self.edit(rid, junk)
        for cmd in (("validate", "--project", "alpha", "--id", rid), ("reuse", GOAL, "--project", "alpha", "--no-brief"),
                    ("lessons", "--project", "alpha"), ("catalog", "--project", "alpha"), ("card", "--project", "alpha", "--id", rid),
                    ("export", "--project", "alpha", "--include-candidates"), ("fork", "--project", "alpha", "--id", rid)):
            r = self.run_cli(*cmd)
            self.assertNotIn("INTERNAL", r.stderr, cmd)
            self.assertNotIn("Traceback", r.stderr, cmd)
        out = json.loads(self.refused("VALIDATE_ERRORS", "validate", "--project", "alpha", "--id", rid, rc=4).stdout)
        self.assertTrue({"SCHEMA", "STATE_LOG_INVALID"} <= self.codes(out)[0])
        self.refused("RECIPE_INVALID", "trace", "--project", "alpha", "--id", rid, "--stage", "create", "--action", "x")
        self.refused("RECIPE_INVALID", "card", "--project", "alpha", "--id", rid)
        self.assertEqual(self.show(rid)["id"], rid)

    def test_typed_garbage_siblings_never_break_commands(self):
        good = self.to_tested()
        tested = json.loads(self.path_of(good).read_text(encoding="utf-8"))

        def nodes(fn):
            return lambda r: [fn(n) for n in r["nodes"]]

        def traces(fn):
            return lambda r: [fn(t) for t in r["traces"]]
        mutations = [lambda r: r.update(plan_choice="B"), nodes(lambda n: n.update(executor="human")), lambda r: r.update(evidence=[1, 2]),
                     lambda r: [x.update(at=5) for x in r["status_log"]], traces(lambda t: t.update(node=["N01"])),
                     traces(lambda t: t.update(capabilities=["SP-0001", 3])), lambda r: r.update(edges="N01->N02"),
                     nodes(lambda n: n.update(inputs=["video"])), lambda r: r.update(capabilities=["SP-0001"]),
                     nodes(lambda n: n.update(executor={})), lambda r: [e.update(source_base=[]) for e in r["evidence"]],
                     lambda r: r.update(goal=42), lambda r: r.update(warnings=[1]), lambda r: r.update(tool_states=[]),
                     lambda r: r.update(suggested_plan=["A"]), lambda r: r.update(status="verified", nodes=[{"id": "N01", "stage": "create", "executor": "tool:x"}])]
        rdir = self.root / "alpha" / "recipes"
        for i, mut in enumerate(mutations):
            x = json.loads(json.dumps(tested))
            x["id"] = f"FUSE-20261021-{i:010x}"
            mut(x)
            (rdir / f"{x['id']}.json").write_text(json.dumps(x), encoding="utf-8")
        cat = self.ok("catalog", "--project", "alpha")
        self.assertEqual((cat["total"], len(cat["invalid_files"])), (1, len(mutations)))
        self.propose()
        self.ok("reuse", GOAL, "--project", "alpha", "--no-brief")
        self.ok("lessons", "--project", "alpha")
        self.ok("export", "--project", "alpha")
        self.trace(good, "N03", "verify")
        self.ok("record", "--project", "alpha", "--id", good, "--status", "verified", "--evidence", self.evidence(), "--qa-pass")
        bad = f"FUSE-20261021-{1:010x}"
        for cmd in (("validate", "--project", "alpha", "--id", bad), ("show", "--project", "alpha", "--id", bad)):
            for js in (True, False):
                r = self.run_cli(*cmd, json_out=js)
                self.assertNotIn("INTERNAL", r.stderr, (cmd, js))
                self.assertNotIn("Traceback", r.stderr, (cmd, js))
        out = json.loads(self.refused("VALIDATE_ERRORS", "validate", "--project", "alpha", "--id", bad, rc=4).stdout)
        self.assertIn("SCHEMA", self.codes(out)[0])
        self.refused("RECIPE_INVALID", "trace", "--project", "alpha", "--id", bad, "--stage", "create", "--action", "x")
        card = self.ok("card", "--project", "alpha", "--id", good, "--out", str(self.tmp / "c.md"))["markdown"]
        broken = card.replace('"executor":{"ref":"method:PLN-01"', '"executor":"human","x":{"ref":"method:PLN-01"', 1)
        self.assertNotEqual(broken, card)
        (self.tmp / "broken.md").write_text(broken, encoding="utf-8")
        self.refused("CARD_INVALID", "import-card", str(self.tmp / "broken.md"), "--project", "alpha")

    def test_fuzzed_field_types_never_crash_the_engine(self):
        import argparse
        import importlib.util
        rid = self.to_tested()
        rec = json.loads(self.path_of(rid).read_text(encoding="utf-8"))
        spec = importlib.util.spec_from_file_location("ff_fuzz", SCRIPT)
        F = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(F)
        ctx = F.Ctx(argparse.Namespace(root=str(self.root), catalog_file=str(self.catalog), tools_file=str(self.tools), now=NOW))
        space = self.root / "alpha"
        paths = []

        def walk(o, p=()):
            paths.append(p)
            if isinstance(o, dict):
                for k, v in o.items():
                    walk(v, p + (k,))
            elif isinstance(o, list) and o:
                walk(o[0], p + (0,))
        walk(rec)
        consumers = {"lessons": F.extract_lessons, "strength": F.recipe_strength, "recency": lambda r: F.recency(ctx, r),
                     "drift": lambda r: F.drift(ctx, r), "card": lambda r: F.render_card(F.card_payload(ctx, r)), "export": F.export_recipe,
                     "verified_shas": F.verified_shas, "template": F.template_executors,
                     "memory": lambda r: F.annotate_memory(ctx, json.loads(json.dumps(rec["nodes"])), [r])}
        crashes = []
        for p in paths[1:]:
            for junk in (None, 1, "x", [], {}, [1]):
                r = json.loads(json.dumps(rec))
                o = r
                for k in p[:-1]:
                    o = o[k]
                o[p[-1]] = junk
                fns = {"validate": lambda r: F.validate_recipe(ctx, space, r), "index_row": F.index_row,
                       "summary": lambda r: F.summary("show", {"recipe": r}, ctx)}
                if not F.malformed(r):
                    fns.update(consumers)
                for name, fn in fns.items():
                    try:
                        fn(r)
                    except F.FFError:
                        pass
                    except Exception as exc:  # noqa: BLE001
                        crashes.append((name, "/".join(map(str, p)), repr(junk), type(exc).__name__))
        self.assertEqual(crashes[:5], [])

    def test_set_graph_and_out_paths_check_types_and_places(self):
        rid = self.propose()["id"]
        r = self.show(rid)
        gf = self.tmp / "g.json"
        for bad in ({"nodes": [dict(r["nodes"][0], capability_ids="SP-0005")], "edges": []},
                    {"nodes": r["nodes"], "edges": r["edges"], "plans": {"A": ["N01", "N02"]}},
                    {"nodes": [dict(r["nodes"][0], inputs=["brief"])], "edges": []},
                    {"nodes": r["nodes"], "edges": [{"from": "N01", "to": ["N02"], "kind": "spec"}]}):
            gf.write_text(json.dumps(bad), encoding="utf-8")
            self.refused("GRAPH_INVALID", "set-graph", "--project", "alpha", "--id", rid, "--file", str(gf))
        recipe = self.path_of(rid)
        before = recipe.read_bytes()
        self.refused("OUT_REFUSED", "card", "--project", "alpha", "--id", rid, "--out", str(recipe))
        self.refused("OUT_REFUSED", "card", "--project", "alpha", "--id", rid, "--out", str(recipe.parent / "x.md"))
        self.refused("OUT_REFUSED", "export", "--project", "alpha", "--include-candidates", "--out", str(self.root / "alpha" / "lessons.json"))
        self.refused("OUT_REFUSED", "export", "--project", "alpha", "--include-candidates", "--out", str(self.tmp / "bundle.md"))
        copy = self.tmp / "copy.json"
        copy.write_bytes(before)
        self.refused("OUT_REFUSED", "export", "--project", "alpha", "--include-candidates", "--out", str(copy))
        self.assertEqual((recipe.read_bytes(), copy.read_bytes()), (before, before))
        out = self.tmp / "bundle.json"
        self.ok("export", "--project", "alpha", "--include-candidates", "--out", str(out))
        self.ok("export", "--project", "alpha", "--include-candidates", "--out", str(out))  # a previous bundle may be replaced

    def test_read_only_commands_create_no_directories(self):
        fresh = self.tmp / "fresh" / "ff"
        cat = self.ok("catalog", "--project", "ghost", root=fresh)
        self.assertEqual((cat["exists"], cat["total"]), (False, 0))
        self.refused("NOT_FOUND", "show", "--project", "ghost", "--id", FIXED_ID, root=fresh)
        self.refused("NOT_FOUND", "validate", "--project", "ghost", "--id", FIXED_ID, root=fresh)
        self.ok("reuse", GOAL, "--project", "ghost", "--no-brief", root=fresh)
        self.assertFalse((self.tmp / "fresh").exists())
        rid = self.propose()["id"]
        before = sorted(p.relative_to(self.root).as_posix() for p in self.root.rglob("*"))
        self.ok("catalog", "--project", "alpha")
        self.show(rid)
        self.ok("validate", "--project", "alpha", "--id", rid)
        self.ok("reuse", GOAL, "--project", "alpha", "--no-brief")
        self.assertEqual(sorted(p.relative_to(self.root).as_posix() for p in self.root.rglob("*")), before)


class LearningTests(Base):
    def test_lessons_include_failed_replaced_worked_and_recipe_failed(self):
        rid = self.propose()["id"]
        self.choose(rid)
        self.trace(rid, "N02", "create", "failed", extra=("--error-class", "missing_dependency"))
        self.trace(rid, "N02", "create", "passed", extra=("--tool", "bin:ffmpeg"))
        self.trace(rid, "N01", "understand", "passed")
        rid2 = self.propose()["id"]
        self.ok("record", "--project", "alpha", "--id", rid2, "--status", "failed", "--evidence", self.evidence(), "--note", "font shaping broke")
        out = self.ok("lessons", "--project", "alpha")
        types = {l["type"] for l in out["lessons"]}
        self.assertTrue({"FAILED", "REPLACED", "WORKED", "HANDOFF", "RECIPE_FAILED"} <= types, types)
        repl = next(l for l in out["lessons"] if l["type"] == "REPLACED")
        self.assertEqual((repl["executor"], repl["replaced_by"]), ("tool:fixture-render", "bin:ffmpeg"))
        failed = next(l for l in out["lessons"] if l["type"] == "FAILED")
        self.assertEqual(failed["error_class"], "missing_dependency")
        self.assertEqual(next(l for l in out["lessons"] if l["type"] == "RECIPE_FAILED")["note"], "font shaping broke")
        self.assertEqual(out["by_executor"]["tool:fixture-render"]["replaced_by"], {"bin:ffmpeg": 1})
        doc = json.loads((self.root / "alpha" / "lessons.json").read_text(encoding="utf-8"))
        self.assertEqual(len(doc["lessons"]), len(out["lessons"]))
        again = self.ok("lessons", "--project", "alpha")
        self.assertEqual([l["id"] for l in again["lessons"]], [l["id"] for l in out["lessons"]])

    def test_lessons_credit_the_executor_and_capabilities_that_ran(self):
        rid = self.propose()["id"]
        self.choose(rid)
        self.trace(rid, "N01", "understand")
        self.trace(rid, "N02", "create", "failed", extra=("--error-class", "tool_error"))
        self.trace(rid, "N02", "create", "passed", extra=("--tool", "bin:ffmpeg", "--capabilities", "SP-0001"))
        out = self.ok("lessons", "--project", "alpha")
        by = {(l["type"], l["node"]): l for l in out["lessons"]}
        handoff = next(l for l in out["lessons"] if l["type"] == "HANDOFF" and l["node"] == "N02")
        self.assertEqual((handoff["from_executor"], handoff["to_executor"]), ("method:PLN-01", "bin:ffmpeg"))
        w2, w1 = by[("WORKED", "N02")], by[("WORKED", "N01")]
        self.assertEqual((w2["capabilities"], w2["node_capabilities"], w2["assumed_executor"]), (["SP-0001"], ["SP-0001"], False))
        self.assertEqual((w1["capabilities"], w1["node_capabilities"], w1["assumed_executor"]), ([], ["SP-0005"], True))
        self.assertTrue(by[("FAILED", "N02")]["assumed_executor"])
        self.assertEqual(out["by_executor"]["method:PLN-01"]["passed"], 0)
        self.assertEqual(out["by_executor"]["method:PLN-01"]["assumed_passed"], 1)
        self.assertEqual(out["by_executor"]["bin:ffmpeg"]["passed"], 1)
        nxt = {n["id"]: n for n in self.propose()["nodes"]}
        self.assertEqual(nxt["N01"]["memory"], {"ran_in": [rid]})  # ran, but neither its tool nor capabilities were reported
        self.assertEqual(nxt["N02"]["memory"]["failed_in"], [rid])
        self.assertEqual(nxt["N02"]["memory"]["replacement_hint"], "bin:ffmpeg")
        self.assertEqual(nxt["N02"]["memory"]["proven_capabilities"], ["SP-0001"])
        self.assertEqual(nxt["N05"]["memory"]["proven_capabilities"], ["SP-0001"])  # SP-0002 never reported running

    def test_stage_memory_reaches_a_node_with_another_executor(self):
        rid = self.propose()["id"]
        self.choose(rid)
        self.trace(rid, "N02", "create", "failed", extra=("--error-class", "missing_dependency"))
        self.trace(rid, "N02", "create", "passed", extra=("--tool", "bin:ffmpeg"))
        plain = json.loads(json.dumps(BRIEF))
        plain["tools"] = []
        for p in plain["plans"].values():
            p["tools"] = []
        nb = self.tmp / "no-tools.json"
        nb.write_text(json.dumps(plain, ensure_ascii=False), encoding="utf-8")
        r = self.propose(goal="مونتاج قصير بخط عربي", brief=nb)
        n02 = next(n for n in r["nodes"] if n["id"] == "N02")
        self.assertEqual(n02["executor"]["ref"], "method:VID-01")
        self.assertEqual(n02["memory"]["stage_failed"], ["tool:fixture-render"])
        self.assertEqual(n02["memory"]["stage_worked"], ["bin:ffmpeg"])
        self.assertEqual(n02["memory"]["stage_replacements"], ["tool:fixture-render -> bin:ffmpeg"])
        self.assertNotIn("worked_in", n02["memory"])

    def test_stale_brief_is_remapped_by_name_or_refused(self):
        swapped = json.loads(json.dumps(CATALOG))
        a, b = swapped["items"][0], swapped["items"][1]
        swapped["items"][0], swapped["items"][1] = dict(b, id="SP-0001"), dict(a, id="SP-0002")
        cat2 = self.tmp / "catalog-swapped.json"
        cat2.write_text(json.dumps(swapped, ensure_ascii=False), encoding="utf-8")
        r = self.ok("propose", GOAL, "--project", "alpha", "--from-brief", str(self.brief), catalog=cat2)["recipe"]
        self.assertTrue({"BRIEF_ID_REMAPPED:SP-0001->SP-0002", "BRIEF_ID_REMAPPED:SP-0002->SP-0001"} <= set(r["warnings"]))
        n02 = next(n for n in r["nodes"] if n["id"] == "N02")
        self.assertEqual((n02["capability_ids"], r["capabilities"]["SP-0002"]["name_en"]), (["SP-0002"], "Video montage cut"))
        renamed = json.loads(json.dumps(CATALOG))
        renamed["items"][0]["name_en"] = "Something else entirely"
        cat3 = self.tmp / "catalog-renamed.json"
        cat3.write_text(json.dumps(renamed, ensure_ascii=False), encoding="utf-8")
        self.refused("BRIEF_CATALOG_MISMATCH", "propose", GOAL, "--project", "alpha", "--from-brief", str(self.brief), catalog=cat3)

    def test_generic_only_brief_is_no_match(self):
        generic = dict(BRIEF, shortlist=[], plans={k: plan(k, "checks only", {"verify": ["SP-0004"]}, []) for k in "ABC"})
        nb = self.tmp / "generic.json"
        nb.write_text(json.dumps(generic, ensure_ascii=False), encoding="utf-8")
        r = self.refused("NO_MATCH", "propose", "xqzv blorf", "--project", "alpha", "--from-brief", str(nb), rc=3)
        self.assertIn("--terms", r.stderr)
        self.assertFalse((self.root / "alpha" / "recipes").exists())

    def test_reuse_ordering_isolation_and_avoid(self):
        older = self.to_verified(goal=GOAL, now="2026-09-01T10:00:00Z")
        newer = self.to_tested(goal="مونتاج فيديو بترجمة عربية", now="2026-10-01T10:00:00Z")
        bad = self.propose(goal="مونتاج فيديو عربي بصوت", now="2026-10-10T10:00:00Z")["id"]
        self.ok("record", "--project", "alpha", "--id", bad, "--status", "failed", "--evidence", self.evidence(), "--note", "captions drifted", now="2026-10-10T10:00:00Z")
        other = self.to_verified(project="beta", goal=GOAL)
        res = self.ok("reuse", GOAL, "--project", "alpha", "--no-brief")
        ids = [m["id"] for m in res["matches"]]
        self.assertEqual(ids[:2], [older, newer])
        self.assertNotIn(other, ids)
        for m in res["matches"]:
            f = m["factors"]
            self.assertAlmostEqual(m["score"], round(f["sim"] * f["strength"] * f["recency"] * f["freshness"], 4), places=4)
        self.assertEqual(res["matches"][0]["factors"]["strength"], 1.0)
        self.assertEqual(res["matches"][1]["factors"]["strength"], 0.4)
        self.assertGreater(res["matches"][1]["factors"]["recency"], res["matches"][0]["factors"]["recency"])
        self.assertEqual([a["id"] for a in res["avoid"]], [bad])
        self.assertIn("captions drifted", json.dumps(res["avoid"], ensure_ascii=False))
        english = self.ok("reuse", "video montage with arabic captions", "--project", "alpha", "--from-brief", str(self.brief))
        self.assertEqual(english["brief"], "file")
        self.assertIn(older, [m["id"] for m in english["matches"]])
        text_only = self.ok("reuse", "video montage with arabic captions", "--project", "alpha", "--no-brief")
        sim = lambda res: next(m["factors"]["sim"] for m in res["matches"] if m["id"] == older)  # noqa: E731
        self.assertGreater(sim(english), sim(text_only))
        beta = self.ok("reuse", GOAL, "--project", "beta", "--no-brief")
        self.assertEqual([m["id"] for m in beta["matches"]], [other])
        r = self.propose(goal=GOAL)
        self.assertEqual(r["recall"]["template"], older)
        self.assertEqual(r["recall"]["avoid"][0]["id"], bad)
        n02 = next(n for n in r["nodes"] if n["id"] == "N02")
        self.assertIn(older, n02["memory"]["ran_in"])  # no --tool was reported: the planned executor is only assumed
        self.assertNotIn("worked_in", n02["memory"])
        self.assertNotIn("LEARNING_INDEX_EMPTY", r["warnings"])
        gamma = self.propose(project="gamma", goal=GOAL)
        self.assertEqual((gamma["recall"]["matches"], gamma["recall"]["template"]), ([], None))
        self.assertIn("LEARNING_INDEX_EMPTY", gamma["warnings"])

    def test_catalog_drift_is_remapped_by_atoms(self):
        rid = self.to_verified()
        swapped = json.loads(json.dumps(CATALOG))
        a, b = swapped["items"][0], swapped["items"][1]
        a_new, b_new = dict(b, id="SP-0001"), dict(a, id="SP-0002")
        swapped["items"][0], swapped["items"][1] = a_new, b_new
        cat2 = self.tmp / "catalog-v2.json"
        cat2.write_text(json.dumps(swapped, ensure_ascii=False), encoding="utf-8")
        out = self.ok("validate", "--project", "alpha", "--id", rid, catalog=cat2)
        self.assertTrue(out["ok"])
        self.assertIn("CATALOG_DRIFT", {w["name"] for w in out["warnings"]})
        self.assertEqual(out["drift"]["remapped"], {"SP-0001": "SP-0002", "SP-0002": "SP-0001"})
        res = self.ok("reuse", GOAL, "--project", "alpha", "--no-brief", catalog=cat2)
        m = next(x for x in res["matches"] if x["id"] == rid)
        self.assertEqual(m["drift"]["remapped"], {"SP-0001": "SP-0002", "SP-0002": "SP-0001"})
        self.assertEqual(m["factors"]["freshness"], 0.75)
        stale = json.loads(json.dumps(CATALOG))
        stale["items"] = [i for i in stale["items"] if i["id"] != "SP-0003"]
        cat3 = self.tmp / "catalog-v3.json"
        cat3.write_text(json.dumps(stale, ensure_ascii=False), encoding="utf-8")
        out = self.run_cli("validate", "--project", "alpha", "--id", rid, catalog=cat3)
        warns = json.loads(out.stdout)["warnings"]
        self.assertTrue(any(w["name"] == "CATALOG_DRIFT" and w["where"] == "SP-0003" for w in warns))


class PortabilityTests(Base):
    def test_card_round_trip_forces_candidate(self):
        rid = self.to_verified()
        card = self.tmp / "card.md"
        out = self.ok("card", "--project", "alpha", "--id", rid, "--out", str(card))
        text = card.read_text(encoding="utf-8")
        self.assertIn("```json fusionforge-card-v2", text)
        self.assertIn("kosif.fusionforge.card.v2", text)
        self.assertNotIn(str(self.tmp), text)
        self.assertEqual(out["status_at_export"], "verified")
        imp = self.ok("import-card", str(card), "--project", "alpha")["recipe"]
        src = self.show(rid)
        self.assertEqual(imp["status"], "candidate")
        self.assertEqual(imp["provenance"]["kind"], "card")
        self.assertEqual(imp["provenance"]["status_at_export"], "verified")
        self.assertEqual((imp["traces"], imp["evidence"], imp["plan_choice"]), ([], [], None))
        self.assertTrue(imp["self_reported"])
        shape = lambda r: [(n["id"], n["stage"], n["capability_ids"], [p["kind"] for p in n["inputs"]],  # noqa: E731
                            [p["kind"] for p in n["outputs"]], n["executor"]["ref"]) for n in r["nodes"]]
        self.assertEqual(shape(imp), shape(src))
        self.assertEqual(imp["edges"], src["edges"])
        self.assertEqual({n["status"] for n in imp["nodes"]}, {"pending"})
        self.ok("validate", "--project", "alpha", "--id", imp["id"])
        card.write_text(text.replace("Results below", "Results " + secret_samples()["jwt"] + " below"), encoding="utf-8")
        self.refused("SECRET", "import-card", str(card), "--project", "alpha")
        (self.tmp / "nocard.md").write_text("# nothing here", encoding="utf-8")
        self.refused("CARD_INVALID", "import-card", str(self.tmp / "nocard.md"), "--project", "alpha")

    def test_export_redacts_and_import_keeps_status(self):
        rid = self.to_verified()
        cand = self.propose()["id"]
        bundle = self.tmp / "bundle.json"
        out = self.ok("export", "--project", "alpha", "--out", str(bundle))
        self.assertEqual(out["recipes"], 1)
        text = bundle.read_text(encoding="utf-8")
        self.assertNotIn(str(self.tmp), text)
        data = json.loads(text)
        recs = [e for r in data["recipes"] for e in r["evidence"] + [t["evidence"] for t in r["traces"] if t["evidence"]]]
        self.assertTrue(recs)
        self.assertEqual({(e["source"], e["source_base"]) for e in recs}, {(None, None)})
        self.assertEqual(data["schema"], "kosif.fusionforge.bundle.v2")
        self.assertEqual([r["id"] for r in data["recipes"]], [rid])
        default = self.ok("export", "--project", "alpha", "--include-candidates")
        self.assertEqual(default["recipes"], 2)
        self.assertTrue(default["path"].endswith("alpha/exports/alpha-20261021.json"))
        root2 = self.tmp / "other-machine"
        res = self.ok("import", str(bundle), "--project", "alpha", root=root2)
        self.assertEqual(res["imported"], [rid])
        r = self.show(rid, root=root2)
        self.assertEqual((r["status"], r["imported"]), ("verified", True))
        v = self.ok("validate", "--project", "alpha", "--id", rid, root=root2)
        self.assertTrue(v["ok"])
        self.assertIn("EVIDENCE_NOT_LOCAL", {w["name"] for w in v["warnings"]})
        reuse = self.ok("reuse", GOAL, "--project", "alpha", "--no-brief", root=root2)
        self.assertEqual(reuse["matches"][0]["factors"]["strength"], 0.8)
        again = self.ok("import", str(bundle), "--project", "alpha", root=root2)
        self.assertEqual(again["skipped_existing"], [rid])
        self.refused("PROJECT_MISMATCH", "import", str(bundle), "--project", "beta", root=root2)
        self.assertNotIn(cand, [x["id"] for x in data["recipes"]])

    def test_migrate_keeps_backup_and_flags_legacy_unproven(self):
        space = self.root / "alpha" / "recipes"
        space.mkdir(parents=True)
        cat_sha = hashlib.sha256(self.catalog.read_bytes()).hexdigest()
        v1 = {"schema": "kosif.fusionforge.recipe.v1", "id": "FUSE-20261001-aaaaaaaaaa", "project": "alpha", "status": "verified",
              "created_at": "2026-10-01T00:00:00+00:00", "updated_at": "2026-10-02T00:00:00+00:00", "goal": GOAL,
              "catalog_sha256": cat_sha, "capabilities": [{"id": "SP-0001", "name": "مونتاج فيديو"}, {"id": "SP-0004", "name": "فحص"}, {"id": "SP-0008", "name": "ايقاع"}],
              "workflow": [{"stage": "build", "capability_ids": ["SP-0008"], "status": "not_run"},
                           {"stage": "create", "capability_ids": ["SP-0001"], "status": "not_run"},
                           {"stage": "verify", "capability_ids": ["SP-0004"], "status": "not_run"},
                           {"stage": "deliver", "capability_ids": [], "status": "not_run"}],
              "evidence": [{"file_local": "/nowhere/QA.json", "sha256": "c" * 64, "status": "verified", "qa_pass_asserted": True,
                            "comment": "", "recorded_at": "2026-10-02T00:00:00+00:00"}]}
        raw = (json.dumps(v1, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        (space / f"{v1['id']}.json").write_bytes(raw)
        self.refused("LEGACY_RECIPE", "validate", "--project", "alpha", "--id", v1["id"])
        self.assertIn(v1["id"], self.ok("catalog", "--project", "alpha")["legacy_v1"])
        out = self.ok("migrate", "--project", "alpha")
        self.assertEqual([m["id"] for m in out["migrated"]], [v1["id"]])
        self.assertEqual((self.root / "alpha" / "legacy" / f"{v1['id']}.v1.json").read_bytes(), raw)
        r = self.show(v1["id"])
        self.assertEqual((r["schema"], r["status"], r["legacy_unproven"]), ("kosif.fusionforge.recipe.v2", "verified", True))
        self.assertEqual([s["to"] for s in r["status_log"]], ["candidate", "planned", "tested", "verified"])
        self.assertEqual([n["stage"] for n in r["nodes"]], ["build", "create", "verify"])
        self.assertEqual(r["nodes"][0]["executor"]["ref"], "method:BEAT-01")
        self.assertNotIn("/nowhere", json.dumps(r))
        v = self.ok("validate", "--project", "alpha", "--id", v1["id"])
        self.assertTrue(v["ok"], v)
        self.assertIn("VERIFIED_WITHOUT_RUN", {w["name"] for w in v["warnings"]})
        res = self.ok("reuse", GOAL, "--project", "alpha", "--no-brief")
        self.assertEqual(res["matches"][0]["factors"]["strength"], 0.3)
        self.assertEqual(self.ok("migrate", "--project", "alpha")["already_v2"], [v1["id"]])
        self.refused("NOT_PROVEN", "promote", "--project", "alpha", "--id", v1["id"])
        self.assertFalse((self.root / "alpha" / "promotions").exists())

    def test_card_and_bundle_hide_every_absolute_path_form(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("ff_redact", SCRIPT)
        F = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(F)
        cases = {"file:///home/kosif/clients/acme/final.mp4": "<abs-path>", "log:/home/kosif/x/render.log": "log:<abs-path>",
                 "C:/Users/kosif/Desktop/a.mp4": "<abs-path>", "(/var/lib/x/y)": "(<abs-path>)", "\\\\server\\share\\a.mp4": "<abs-path>",
                 "https://example.com/a/b": "https://example.com/a/b", "~/clients/a.mp4": "<home-path>", "N01→N02 and/or 1/2": "N01→N02 and/or 1/2"}
        for raw, want in cases.items():
            self.assertEqual(F.redact_text(raw), want, raw)
        rid = self.propose()["id"]
        self.choose(rid)
        self.trace(rid, "N02", "create", extra=("--output", "file:///home/kosif/clients/acme/final.mp4",
                                                "--input", "C:/Users/kosif/acme/a.mp4 and \\\\nas\\share\\b.mov"))
        self.ok("trace", "--project", "alpha", "--id", rid, "--stage", "create", "--action", "log",
                "--observed", "log:/home/kosif/clients/acme/render.log; (/Users/kosif/x/y)")
        bundle = self.tmp / "b.json"
        self.ok("export", "--project", "alpha", "--include-candidates", "--out", str(bundle))
        card = self.ok("card", "--project", "alpha", "--id", rid, "--out", str(self.tmp / "c.md"))["markdown"]
        leak = re.compile(r"/(?:home|Users|root|tmp|var)/|[A-Za-z]:[\\/]Users|\\\\nas")
        for name, text in (("bundle", bundle.read_text(encoding="utf-8")), ("card", card)):
            self.assertIsNone(leak.search(text), (name, leak.search(text)))

    def test_large_evidence_is_found_from_another_directory(self):
        rid = self.propose()["id"]
        big = self.tmp / "big.bin"
        big.write_bytes(b"\x01" * (5 * 1024 * 1024 + 10))
        out = self.ok("trace", "--project", "alpha", "--id", rid, "--stage", "create", "--action", "rendered", "--evidence", "big.bin")
        ev = out["trace"]["evidence"]
        self.assertEqual((ev["stored"], ev["source"]), (None, "big.bin"))
        self.assertFalse(ev["root_rel"].startswith("/"))
        sub = self.tmp / "sub"
        sub.mkdir()
        self.ok("validate", "--project", "alpha", "--id", rid, cwd=sub)
        bundle = self.tmp / "b.json"
        self.ok("export", "--project", "alpha", "--include-candidates", "--out", str(bundle))
        self.assertNotIn("root_rel", bundle.read_text(encoding="utf-8"))

    def test_skill_outside_a_checkout_needs_an_explicit_root(self):
        if subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=str(self.tmp), capture_output=True).returncode == 0:
            self.skipTest("the temporary directory is inside a git checkout")
        scripts = self.tmp / "home" / ".claude" / "skills" / "kosif-superpowers" / "scripts"
        scripts.mkdir(parents=True)
        for name in ("fusionforge.py", "_secrets.py"):
            (scripts / name).write_bytes((SCRIPT.parent / name).read_bytes())
        work = self.tmp / "work"
        work.mkdir()
        env = {k: v for k, v in os.environ.items() if k != "KOSIF_FUSIONFORGE_ROOT"}
        r = subprocess.run([sys.executable, str(scripts / "fusionforge.py"), "catalog", "--project", "p"], cwd=str(work),
                           capture_output=True, text=True, timeout=60, env=env)
        self.assertEqual(r.returncode, 2, r.stderr)
        self.assertIn("fusionforge: error: NO_ROOT:", r.stderr)
        self.assertFalse((self.tmp / "home" / "out").exists())

    def test_promote_and_fork(self):
        cat_sha = hashlib.sha256(self.catalog.read_bytes()).hexdigest()
        cand = self.propose()["id"]
        self.refused("NOT_VERIFIED", "promote", "--project", "alpha", "--id", cand)
        rid = self.to_verified()
        out = self.ok("promote", "--project", "alpha", "--id", rid)
        self.assertEqual(out["approval"]["state"], "pending_human")
        prop = json.loads(Path(out["path"]).read_text(encoding="utf-8"))
        self.assertEqual(prop["schema"], "kosif.fusionforge.promotion.v2")
        self.assertIsNone(prop["approval"]["approved_by"])
        self.assertNotIn(GOAL, json.dumps(prop, ensure_ascii=False))
        self.assertEqual(hashlib.sha256(self.catalog.read_bytes()).hexdigest(), cat_sha)
        self.assertTrue(out["path"].endswith(f"alpha/promotions/{rid}.proposal.json"))
        fork = self.ok("fork", "--project", "alpha", "--id", rid)["recipe"]
        self.assertEqual((fork["status"], fork["forked_from"], fork["traces"], fork["plan_choice"]), ("candidate", rid, [], None))
        self.assertEqual({n["status"] for n in fork["nodes"]}, {"pending"})
        self.assertEqual(self.show(rid)["status"], "verified")
        self.ok("validate", "--project", "alpha", "--id", fork["id"])


class SchemaFileTests(unittest.TestCase):
    def test_schema_files_match_engine_constants(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("fusionforge_mod", SCRIPT)
        ff = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ff)
        sdir = SKILL / "schemas"
        recipe = json.loads((sdir / "fusionforge.recipe.v2.json").read_text(encoding="utf-8"))
        card = json.loads((sdir / "fusionforge.card.v2.json").read_text(encoding="utf-8"))
        bundle = json.loads((sdir / "fusionforge.bundle.v2.json").read_text(encoding="utf-8"))
        defs = recipe["$defs"]
        self.assertEqual(recipe["properties"]["schema"]["const"], ff.SCHEMA)
        self.assertEqual(card["properties"]["schema"]["const"], ff.CARD_SCHEMA)
        self.assertEqual(bundle["properties"]["schema"]["const"], ff.BUNDLE_SCHEMA)
        self.assertEqual(tuple(defs["stage"]["enum"]), ff.STAGES)
        self.assertEqual(tuple(defs["kind"]["enum"]), ff.KINDS)
        self.assertEqual(tuple(recipe["properties"]["status"]["enum"]), ff.STATUSES)
        self.assertEqual(tuple(defs["edge"]["properties"]["relation"]["enum"]), ff.RELATIONS)
        self.assertEqual(tuple(defs["node"]["properties"]["status"]["enum"]), ff.NODE_STATUSES)


class DocstringTests(unittest.TestCase):
    def test_docstring_lists_every_subcommand_with_an_example(self):
        import argparse
        import importlib.util
        spec = importlib.util.spec_from_file_location("fusionforge_doc", SCRIPT)
        ff = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ff)
        parser = ff.build_parser()
        sub = next(a for a in parser._actions if isinstance(a, argparse._SubParsersAction))
        doc = ff.__doc__
        for name in sub.choices:
            self.assertRegex(doc, r"scripts/fusionforge\.py " + re.escape(name) + r"\s", name)


if __name__ == "__main__":
    unittest.main(verbosity=2)
