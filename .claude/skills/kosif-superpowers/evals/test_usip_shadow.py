#!/usr/bin/env python3
"""USIP v5.3 shadow evals: the deterministic rows of references/protocol/A9-shadow-evals.md.

Each test names the protocol case IDs it checks (R01…R30, -1.11#NN, -1.16#NN, -1.32#NN, -1.38#N and the hard gates
H01…H09) and runs them against this checkout's own scripts and catalog: skill_intelligence.build_brief in process,
scripts/fusionforge.py as a subprocess with --root in a temporary folder (never the real out/fusionforge),
tools/verify_video.py, and the protocol files. Nothing is executed for real, published or sent.

When the module ends it prints a Shadow report to stderr with every row of the A9 merged table plus H01…H09, each
PASS, FAIL or NOT_RUN. NOT_RUN means there is no deterministic check here (behaviour that needs a live host, a human,
a bridge or an external service) or the test did not run (skipped or filtered). A row checked only in part shows its
scope. expectedFailure marks an honest gap this release did not fix; the report lists it as FAIL (known gap).
USIP_SHADOW_REPORT=<file.json> also writes the report as JSON.

Run: python3 -m unittest discover -s .claude/skills/kosif-superpowers/evals -p 'test_usip_shadow.py' -v
"""
from __future__ import annotations

import functools
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
REPO = SKILL.parents[2] if SKILL.parent.name == "skills" else SKILL.parent  # repo root when the skill sits in .claude/skills
SCRIPTS = SKILL / "scripts"
FF = SCRIPTS / "fusionforge.py"
A9 = SKILL / "references" / "protocol" / "A9-shadow-evals.md"
NOW = "2026-10-21T12:00:00Z"
sys.path.insert(0, str(SCRIPTS))
import _secrets  # noqa: E402
import check_skill as C  # noqa: E402
import skill_intelligence as S  # noqa: E402

GATES = [f"H{n:02d}" for n in range(1, 10)]
RESULTS: dict = {}  # case id -> {"status", "tests", "scope", "known_gap"}


def case(*ids, scope=""):
    """Tie a test to protocol case IDs; its outcome becomes their PASS/FAIL row in the Shadow report."""
    def deco(fn):
        @functools.wraps(fn)
        def wrapper(self, *a, **kw):
            try:
                fn(self, *a, **kw)
            except unittest.SkipTest:
                raise
            except BaseException:
                _mark(ids, "FAIL", fn.__name__, scope, getattr(wrapper, "__unittest_expecting_failure__", False))
                raise
            _mark(ids, "PASS", fn.__name__, scope, False)
        wrapper.case_ids = ids
        return wrapper
    return deco


def _mark(ids, status, test, scope, known):
    for cid in ids:
        row = RESULTS.setdefault(cid, {"status": status, "tests": [], "scope": [], "known_gap": False})
        if status == "FAIL":
            row["status"] = "FAIL"
            row["known_gap"] = row["known_gap"] or known
        row["tests"].append(test)
        if scope and scope not in row["scope"]:
            row["scope"].append(scope)


def a9_rows() -> list:
    """(id, topic) for every row of the A9 merged table, in table order."""
    rows = []
    for line in A9.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*(-1\.\d+#\d+|R\d{2})\s*\|\s*([^|]*)\|", line)
        if m:
            rows.append((m.group(1), m.group(2).strip()))
    return rows


def tearDownModule():
    try:
        order = [r[0] for r in a9_rows()] + GATES
    except OSError:
        order = list(GATES)
    order += sorted(cid for cid in RESULTS if cid not in order)
    report = []
    for cid in order:
        row = RESULTS.get(cid)
        report.append({"id": cid, "status": row["status"] if row else "NOT_RUN", "tests": row["tests"] if row else [],
                       "scope": "; ".join(row["scope"]) if row else "", "known_gap": bool(row and row["known_gap"])})
    counts = Counter(r["status"] for r in report)
    known = sum(1 for r in report if r["known_gap"])
    out = [f"\nUSIP v5.3 shadow report (A9 merged table + H01-H09): {len(report)} cases · PASS {counts['PASS']} · "
           f"FAIL {counts['FAIL']} ({known} known gap{'s' if known != 1 else ''}) · NOT_RUN {counts['NOT_RUN']}"]
    for r in report:
        if r["status"] != "NOT_RUN":
            tail = (" [" + r["scope"] + "]" if r["scope"] else "") + (" (known gap)" if r["known_gap"] else "")
            out.append(f"  {r['status']:<4} {r['id']:<9} {', '.join(dict.fromkeys(r['tests']))}{tail}")
    out.append("  NOT_RUN (no deterministic check here, or not run): " + " ".join(r["id"] for r in report if r["status"] == "NOT_RUN"))
    print("\n".join(out), file=sys.stderr)
    dest = os.environ.get("USIP_SHADOW_REPORT")
    if dest:
        Path(dest).write_text(json.dumps({"schema": "kosif.usip-shadow-report.v1", "protocol": S.PROTOCOL_VERSION,
                                          "counts": dict(counts), "cases": report}, ensure_ascii=False, indent=1) + "\n",
                              encoding="utf-8")


@functools.lru_cache(maxsize=None)
def brief(q: str) -> dict:
    return S.build_brief(q)


def plan_ids(b: dict, k: str) -> set:
    return {sp["id"] for sp in b["plans"].get(k, {}).get("superpowers", [])}


def needs(b: dict) -> dict:
    return {m["need"]: m["status"] for m in b["must_have_coverage"]}


def verifier_families(b: dict) -> set:
    return {v.get("via_family") for v in b.get("verifiers", [])}


def top_families(b: dict, n: int = 5) -> set:
    return {f for x in b["shortlist"][:n] for f in x.get("families", [])}


# ---------------------------------------------------------------------------------------------------- routing
class Routing(unittest.TestCase):
    @case("R01", "-1.11#01", "-1.32#08", scope="level, plans, must-haves and questions; not the Stage-0 card wording")
    def test_R01_simple_questions_are_L0_without_plans_or_questions(self):
        for q in ("ما معنى الاستحقاق؟", "وش معنى الاستحقاق؟", "what is MCP?"):
            with self.subTest(q=q):
                b = brief(q)
                self.assertEqual(b["analysis"]["level"], "L0")
                self.assertEqual(b["plans"], {})
                self.assertIsNone(b["approval_question"])
                self.assertEqual(b["must_have_coverage"], [])
                self.assertEqual(b["analysis"].get("questions") or [], [])

    @case("-1.11#07", "-1.16#09", scope="routing")
    def test_1_11_07_image_request_is_not_hijacked_to_video(self):
        for q in ("صمم صورة", "صورة فقط"):
            with self.subTest(q=q):
                a = brief(q)["analysis"]
                self.assertEqual(a["primary"], "image")
                self.assertNotIn("video", a["deliverables"])

    @case("-1.11#08", "-1.16#10", scope="routing")
    def test_1_11_08_suno_lyrics_stay_audio_without_a_storyboard(self):
        for q in ("اكتب أغنية Suno", "اكتب كلمات أغنية Suno فقط", "كلمات Suno فقط"):
            with self.subTest(q=q):
                b = brief(q)
                self.assertEqual(b["analysis"]["primary"], "audio")
                self.assertNotIn("video", b["analysis"]["deliverables"])
                names = [sp["name_en"].lower() for p in b["plans"].values() for sp in p["superpowers"]]
                self.assertFalse([n for n in names if "storyboard" in n], names)

    @case("-1.11#11", "-1.16#11", scope="routing only; no live REA or Ghidra run")
    def test_1_11_11_binary_analysis_routes_to_REA(self):
        for q in ("حلل REA للملف الثنائي app.exe", "حلل binary في REA/Ghidra"):
            with self.subTest(q=q):
                b = brief(q)
                self.assertIn("reverse", b["analysis"]["deliverables"])
                self.assertIn("software-investigation", verifier_families(b))

    @case("-1.11#12", scope="routing")
    def test_1_11_12_source_repo_architecture_is_not_REA(self):
        a = brief("حلل معمارية هذا المستودع source repo")["analysis"]
        self.assertNotIn("reverse", a["deliverables"])
        self.assertEqual(a["primary"], "code")

    @case("-1.11#02", scope="routing and code verifiers; proving the cause is the agent's job")
    def test_1_11_02_bug_fix_routes_to_engineering_with_code_checks(self):
        b = brief("أصلح خطأ في كود")
        self.assertEqual(b["analysis"]["primary"], "code")
        self.assertTrue(verifier_families(b) & {"code-engineering", "verification-evals", "api-testing", "atlas-code"}, b["verifiers"])

    @case("-1.11#13", scope="routing only; nothing is uploaded by the brief")
    def test_1_11_13_graphify_dependency_map(self):
        b = brief("Graphify اعمل خريطة الاعتماديات للمستودع")
        self.assertEqual(b["analysis"]["primary"], "code")
        self.assertTrue(any("graphify" in sp["name_en"].lower() for sp in b["plans"]["A"]["superpowers"]), b["plans"]["A"])

    @case("-1.11#10", scope="routing only")
    def test_1_11_10_prompt_improvement_reaches_prompt_craft(self):
        self.assertIn("prompt-craft", top_families(brief("حسّن البرومبت")))

    @case("-1.11#04", scope="routing only; reading the source is the agent's job")
    def test_1_11_04_source_lookup_is_research(self):
        b = brief("ابحث عن مصدر لمعلومة")
        self.assertEqual(b["analysis"]["primary"], "research")
        self.assertIn("web-research", verifier_families(b))

    @case("-1.11#05", scope="routing only")
    def test_1_11_05_prd_with_options_reaches_strategy(self):
        self.assertIn("strategy-finance", top_families(brief("اكتب PRD بخيارات")))

    @case("-1.11#09", scope="routing only; no video is watched or copied")
    def test_1_11_09_imitating_a_montage_uses_reference_tools(self):
        b = brief("قلّد مونتاج الفيديو")
        self.assertEqual(b["analysis"]["primary"], "video")
        self.assertTrue({t["id"] for t in b["tools"]} & {"reference-edit-engine", "motion-reference-probe"}, b["tools"])

    @case("-1.16#03", scope="routing, sound checks and a verify stage; nothing is rendered")
    def test_1_16_03_video_from_my_voice_keeps_sound_checks(self):
        b = brief("أنتج فيديو من صوتي")
        self.assertEqual(b["analysis"]["primary"], "video")
        self.assertFalse(b["analysis"].get("silent"))
        self.assertTrue(any("loudness" in (v.get("name_en") or "").lower() for v in b["verifiers"]), b["verifiers"])
        for k, p in b["plans"].items():
            if p.get("superpowers"):
                self.assertIn("verify", p["stages"], k)

    @case("-1.16#04", scope="routing only")
    def test_1_16_04_draw_and_animate_a_character(self):
        b = brief("ارسم شخصية وحركها")
        self.assertEqual(needs(b).get("شخصية متحركة"), "covered", b["must_have_coverage"])
        self.assertTrue({t["id"] for t in b["tools"]} & {"code-drawing-master", "character-fullbody", "character-ik", "smart-draw"}, b["tools"])

    @case("-1.16#07", scope="routing only; glyph shaping is checked at render time")
    def test_1_16_07_arabic_kinetic_words_need_rtl(self):
        b = brief("موشن كلمات عربية")
        self.assertEqual(needs(b).get("نص عربي صحيح RTL"), "covered", b["must_have_coverage"])
        self.assertTrue(any("arabic" in (v.get("name_en") or "").lower() for v in b["verifiers"]), b["verifiers"])

    @case("-1.16#01", "-1.32#06", scope="plans differ by method (B/C rule); the decision itself is the user's")
    def test_1_16_01_plans_are_three_methods_not_three_sizes(self):
        for q in ("اعمل عصف ذهني لبناء تطبيق", "طوّر البروتوكول وارفعه", "مونتاج فيديو على صوتي بترجمة عربية"):
            with self.subTest(q=q):
                b = brief(q)
                A, B, Cc = plan_ids(b, "A"), plan_ids(b, "B"), plan_ids(b, "C")
                self.assertTrue(A and B)
                self.assertNotEqual(A, B)
                if b["plans"]["C"].get("unavailable"):
                    self.assertFalse(Cc)
                    self.assertNotEqual(b["recommended"], "C")
                else:
                    self.assertNotEqual(B, Cc)
                    self.assertFalse(B <= Cc, "C is B plus extras")
                    self.assertTrue(Cc - B, "C has no picks of its own")

    @case("-1.11#03", "-1.16#13", scope="an eval gate is planned; baseline and candidate runs are not executed here")
    def test_1_11_03_protocol_evolution_plans_an_eval_gate(self):
        for q in ("طوّر بروتوكول KOSIF SEE", "طوّر البروتوكول"):
            with self.subTest(q=q):
                b = brief(q)
                self.assertNotEqual(b["analysis"]["level"], "L0")
                self.assertTrue(b["plans"])
                self.assertIn("verification-evals", verifier_families(b), b["verifiers"])

    @case("-1.32#13", scope="routing only; debits = credits is not computed here")
    def test_1_32_13_accounting_entry_has_the_accounting_need(self):
        self.assertEqual(needs(brief("قيد محاسبي")).get("محاسبة ومخزون بأرقام صحيحة"), "covered")

    @unittest.expectedFailure
    @case("-1.11#06", scope="routing only")
    def test_1_11_06_statement_reconciliation_has_the_accounting_need(self):
        # Known gap: the Arabic reconciliation words (مطابقة كشف، فروقات) do not trigger the accounting need and the
        # shortlist is unrelated; the English "reconcile a bank statement against the ledger" does trigger it.
        self.assertIn("محاسبة ومخزون بأرقام صحيحة", needs(brief("احسب مطابقة كشف حساب بنكي")))

    @unittest.expectedFailure
    @case("-1.16#14", scope="routing only")
    def test_1_16_14_financial_figures_have_a_deterministic_numbers_need(self):
        # Known gap: «أرقام مالية» alone reaches number-typography picks, not a finance or accounting need.
        self.assertIn("محاسبة ومخزون بأرقام صحيحة", needs(brief("احسب أرقام مالية")))

    @unittest.expectedFailure
    @case("-1.11#15", "-1.16#12", scope="routing only")
    def test_1_11_15_merging_to_main_is_a_git_release_job(self):
        # Known gap: the GitHub need fires on push verbs next to a git target and on "pull request"; a bare merge to
        # main («ادمج إلى main», «ادمج ونشّر main») is still read as an unspecified request.
        for q in ("ادمج إلى main", "ادمج ونشّر main"):
            self.assertTrue(any("GitHub" in n for n in needs(brief(q))), q)

    @case("R22", "-1.32#04", "-1.38#5", scope="indexed 100% scan with a bounded shortlist, and FusionForge caps")
    def test_R22_the_catalog_is_indexed_not_preloaded(self):
        b = brief("مونتاج فيديو على صوتي بترجمة عربية")
        cov = b["coverage"]
        self.assertTrue(cov["complete"])
        self.assertEqual(cov["records_scanned"], cov["records_on_disk"])
        self.assertLessEqual(len(b["shortlist"]), 60)
        self.assertLess(len(b["shortlist"]) * 10, cov["records_scanned"])
        r = subprocess.run([sys.executable, str(SCRIPTS / "skill_intelligence.py"), "verify"], capture_output=True, text=True, timeout=600)
        self.assertEqual(r.returncode, 0, r.stderr[-400:])
        self.assertTrue(json.loads(r.stdout)["coverage"]["complete"])
        with tempfile.TemporaryDirectory() as d:
            for n in ("61", "300"):
                r = subprocess.run([sys.executable, str(FF), "--root", str(Path(d) / "ff"), "propose", "مونتاج فيديو",
                                    "--project", "caps", "--max-capabilities", n], capture_output=True, text=True, timeout=120, cwd=d)
                self.assertEqual(r.returncode, 2, r.stderr)
                self.assertIn("fusionforge: error: USAGE:", r.stderr)
                self.assertFalse((Path(d) / "ff" / "caps" / "recipes").exists())


# ---------------------------------------------------------------------------------------------------- FusionForge
def secret_samples() -> list:
    """Built at runtime so this file never holds a credential-shaped literal."""
    a = "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6"
    return ["sk-" + "ant-api03-" + a, "github" + "_pat_" + "11ABCDEFG0" + a, "AK" + "IAIOSFODNN7EXAMPLE",
            "AI" + "za" + "Sy" + a + "abc", "Bear" + "er " + a]


class FusionForge(unittest.TestCase):
    GOAL = "مونتاج فيديو على صوتي بترجمة عربية"

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.tmp = Path(cls._tmp.name).resolve()
        cls.root = cls.tmp / "ff"
        cls.brief_file = cls.tmp / "brief.json"
        cls.brief_file.write_text(json.dumps(brief(cls.GOAL), ensure_ascii=False), encoding="utf-8")
        cls.n_ev = 0

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def ff(self, *args, rc=0, code=None):
        env = {k: v for k, v in os.environ.items() if k != "KOSIF_FUSIONFORGE_ROOT"}
        r = subprocess.run([sys.executable, str(FF), "--root", str(self.root), "--now", NOW, *args, "--json"],
                           cwd=str(self.tmp), capture_output=True, text=True, timeout=300, env=env)
        self.assertNotIn("Traceback", r.stderr)
        self.assertEqual(r.returncode, rc, f"{args[:1]}: {r.stderr}")
        if code:
            self.assertIn(f"fusionforge: error: {code}:", r.stderr)
        return json.loads(r.stdout) if rc == 0 else r

    def evidence(self, text=None) -> str:
        type(self).n_ev += 1
        p = self.tmp / f"qa-{type(self).n_ev}.json"
        p.write_text(text or json.dumps({"check": type(self).n_ev, "measured": True}), encoding="utf-8")
        return str(p)

    def propose(self, project, goal=None) -> dict:
        return self.ff("propose", goal or self.GOAL, "--project", project, "--from-brief", str(self.brief_file))["recipe"]

    def run_chosen_plan(self, project, rid, plan="A"):
        self.ff("choose", "--project", project, "--id", rid, "--plan", plan, "--why", "smallest plan that meets every must-have")
        rec = self.ff("show", "--project", project, "--id", rid)["recipe"]
        stage = {n["id"]: n["stage"] for n in rec["nodes"]}
        for nid in rec["plan_choice"]["nodes"]:
            self.ff("trace", "--project", project, "--id", rid, "--stage", stage[nid], "--node", nid, "--result", "passed",
                    "--action", f"ran {nid}", "--tool", "human", "--output", f"{nid}.out", "--observed", f"{nid} measured",
                    "--evidence", self.evidence())

    def verified(self, project) -> str:
        rid = self.propose(project)["id"]
        self.run_chosen_plan(project, rid)
        self.ff("record", "--project", project, "--id", rid, "--status", "tested", "--evidence", self.evidence())
        self.ff("record", "--project", project, "--id", rid, "--status", "verified", "--evidence", self.evidence(), "--qa-pass")
        return rid

    @case("-1.38#1", scope="real catalog brief; local index written, nothing executed")
    def test_1_38_1_new_request_is_a_candidate_with_nothing_executed(self):
        out = self.ff("propose", self.GOAL, "--project", "p1", "--from-brief", str(self.brief_file))
        rec = out["recipe"]
        self.assertEqual((rec["schema"], rec["status"], rec["traces"], rec["plan_choice"]), ("kosif.fusionforge.recipe.v2", "candidate", [], None))
        self.assertEqual({n["status"] for n in rec["nodes"]}, {"pending"})
        self.assertTrue(any(n["stage"] == "verify" for n in rec["nodes"]))
        self.assertEqual(out["validate"]["errors"], [])
        self.assertTrue((self.root / "p1" / "index.json").is_file())
        self.assertEqual(self.ff("catalog", "--project", "p1")["by_status"].get("verified", 0), 0)

    @case("-1.38#4", scope="engine gate: transitions, evidence, --qa-pass, self-evidence")
    def test_1_38_4_verified_needs_a_run_evidence_and_qa_pass(self):
        rid = self.propose("p4")["id"]
        base = ("record", "--project", "p4", "--id", rid, "--status")
        self.ff(*base, "verified", "--evidence", self.evidence(), "--qa-pass", rc=2, code="ILLEGAL_TRANSITION")
        self.ff("choose", "--project", "p4", "--id", rid, "--plan", "A", "--why", "lean")
        self.ff(*base, "tested", rc=2)
        self.ff(*base, "tested", "--evidence", self.evidence(), rc=2, code="NO_RUN")
        rid2 = self.propose("p4b")["id"]
        self.run_chosen_plan("p4b", rid2)
        self.ff("record", "--project", "p4b", "--id", rid2, "--status", "tested", "--evidence", self.evidence())
        vbase = ("record", "--project", "p4b", "--id", rid2, "--status", "verified")
        self.ff(*vbase, "--evidence", self.evidence(), rc=2, code="QA_PASS_REQUIRED")
        self.ff(*vbase, "--qa-pass", rc=2)
        own = self.root / "p4b" / "recipes" / f"{rid2}.json"
        self.ff(*vbase, "--evidence", str(own), "--qa-pass", rc=2, code="SELF_EVIDENCE")
        self.ff(*vbase, "--evidence", str(self.root / "p4b" / "index.json"), "--qa-pass", rc=2, code="SELF_EVIDENCE")
        self.assertEqual(self.ff("show", "--project", "p4b", "--id", rid2)["recipe"]["status"], "tested")
        self.assertEqual(self.ff("show", "--project", "p4", "--id", rid)["recipe"]["status"], "planned")

    @case("-1.38#9", scope="engine: a failed recipe is final, teaches RECIPE_FAILED and is never verified")
    def test_1_38_9_failed_experiment_teaches_but_never_counts(self):
        rid = self.propose("p9")["id"]
        self.ff("record", "--project", "p9", "--id", rid, "--status", "failed", "--evidence", self.evidence(), rc=2, code="NOTE_REQUIRED")
        self.ff("record", "--project", "p9", "--id", rid, "--status", "failed", "--evidence", self.evidence(), "--note", "fonts missing here")
        self.ff("trace", "--project", "p9", "--id", rid, "--stage", "verify", "--action", "late", rc=2, code="TERMINAL_RECIPE")
        self.assertEqual(self.ff("catalog", "--project", "p9")["by_status"].get("verified", 0), 0)
        self.assertIn("RECIPE_FAILED", self.ff("lessons", "--project", "p9")["counts"])
        reuse = self.ff("reuse", self.GOAL, "--project", "p9", "--from-brief", str(self.brief_file))
        self.assertEqual(reuse["matches"], [])
        self.assertEqual([a["id"] for a in reuse["avoid"]], [rid])

    @case("-1.38#2", "-1.38#3", "R19", "-1.16#16", "-1.32#16",
          scope="FusionForge memory only: same-project recall, nothing reaches another project")
    def test_1_38_2_similar_goal_recalls_the_verified_recipe_only_in_its_project(self):
        rid = self.verified("pa")
        reuse = self.ff("reuse", "مونتاج فيديو بترجمة عربية على صوتي", "--project", "pa", "--from-brief", str(self.brief_file))
        self.assertEqual(reuse["matches"][0]["id"], rid)
        self.assertEqual(reuse["matches"][0]["status"], "verified")
        again = self.propose("pa")
        self.assertEqual(again["recall"]["template"], rid)
        self.assertTrue(again["recall"]["matches"])
        other = self.ff("reuse", "مونتاج فيديو بترجمة عربية على صوتي", "--project", "pb", "--from-brief", str(self.brief_file))
        self.assertEqual((other["matches"], other["avoid"]), ([], []))
        fresh = self.propose("pb")
        self.assertEqual((fresh["recall"]["matches"], fresh["recall"]["avoid"], fresh["recall"]["template"]), ([], [], None))
        self.assertNotIn(rid, json.dumps(fresh, ensure_ascii=False))

    @case("-1.38#6", scope="engine: a graph of names without typed handoffs and a final verify is refused")
    def test_1_38_6_names_without_handoffs_or_a_test_stay_candidate(self):
        rec = self.propose("p6")
        caps = [c for n in rec["nodes"] for c in n["capability_ids"]][:3]
        graph = {"nodes": [{"id": f"X{i}", "stage": "create", "capability_ids": [c], "inputs": [], "outputs": [], "executor": "human"}
                           for i, c in enumerate(caps, 1)],
                 "edges": [{"from": "X1", "to": "X2", "kind": "video"}, {"from": "X2", "to": "X3", "kind": "audio"}],
                 "plans": {"A": {"idea": "names only", "nodes": ["X1", "X2", "X3"]}}}
        gf = self.tmp / "names-only.json"
        gf.write_text(json.dumps(graph), encoding="utf-8")
        self.ff("set-graph", "--project", "p6", "--id", rec["id"], "--file", str(gf), rc=2, code="GRAPH_INVALID")
        self.assertEqual(self.ff("show", "--project", "p6", "--id", rec["id"])["recipe"]["status"], "candidate")

    @case("-1.32#05", scope="FusionForge draft contracts (default_unconfirmed): typed I/O and a check per node; picks not judged")
    def test_1_32_05_every_node_has_input_output_and_a_check(self):
        goal = "توليفة محاسبة و Graphify: خريطة اعتماديات لنظام القيود المحاسبية"
        bf = self.tmp / "brief-acc.json"
        bf.write_text(json.dumps(brief(goal), ensure_ascii=False), encoding="utf-8")
        out = self.ff("propose", goal, "--project", "p5", "--from-brief", str(bf))
        self.assertEqual(out["validate"]["errors"], [])
        rec = out["recipe"]
        nodes = {n["id"]: n for n in rec["nodes"]}
        for n in rec["nodes"]:
            with self.subTest(node=n["id"]):
                self.assertTrue(n["inputs"] and n["outputs"] and n["acceptance"] and n["executor"]["ref"])
        for e in rec["edges"]:
            produced = {o["kind"] for o in nodes[e["from"]]["outputs"]}
            accepted = {i["kind"] for i in nodes[e["to"]]["inputs"]}
            self.assertTrue(e["kind"] == "any" or (e["kind"] in produced and (e["kind"] in accepted or "any" in accepted)), e)
        for k, p in rec["plans"].items():
            with self.subTest(plan=k):
                self.assertTrue(any(nodes[nid]["stage"] == "verify" for nid in p["nodes"]))

    @case("R24", scope="FusionForge gate only: a failed verify node keeps the candidate from verified")
    def test_R24_a_failed_check_rejects_the_candidate(self):
        rid = self.propose("p24")["id"]
        self.ff("choose", "--project", "p24", "--id", rid, "--plan", "A", "--why", "lean")
        rec = self.ff("show", "--project", "p24", "--id", rid)["recipe"]
        stage = {n["id"]: n["stage"] for n in rec["nodes"]}
        for nid in rec["plan_choice"]["nodes"]:
            failed = stage[nid] == "verify"
            self.ff("trace", "--project", "p24", "--id", rid, "--stage", stage[nid], "--node", nid,
                    "--result", "failed" if failed else "passed", "--action", f"ran {nid}", "--observed", "regression" if failed else "ok",
                    "--evidence", self.evidence(), *(["--error-class", "quality_below_threshold"] if failed else []))
        self.ff("record", "--project", "p24", "--id", rid, "--status", "tested", "--evidence", self.evidence())
        self.ff("record", "--project", "p24", "--id", rid, "--status", "verified", "--evidence", self.evidence(), "--qa-pass",
                rc=2, code="GATE_NODE_NOT_PASSED")
        self.assertEqual(self.ff("show", "--project", "p24", "--id", rid)["recipe"]["status"], "tested")

    @case("-1.38#7", "H05", scope="credential patterns only (not licences or permissions)")
    def test_1_38_7_credentials_are_refused_in_written_fields(self):
        rid = self.propose("p7")["id"]
        for s in secret_samples():
            with self.subTest(kind=s[:4]):
                self.ff("trace", "--project", "p7", "--id", rid, "--stage", "create", "--action", "used " + s, rc=2, code="SECRET")
        self.ff("choose", "--project", "p7", "--id", rid, "--plan", "A", "--why", "token " + secret_samples()[0], rc=2, code="SECRET")
        self.ff("propose", "مونتاج فيديو " + secret_samples()[1], "--project", "p7", rc=2, code="SECRET")
        text = (self.root / "p7" / "recipes" / f"{rid}.json").read_text(encoding="utf-8")
        self.assertEqual(_secrets.find_secrets(text), [])

    @case("-1.38#10", scope="promotion stays a pending_human proposal; the catalog is untouched")
    def test_1_38_10_promotion_is_a_pending_human_proposal(self):
        cand = self.propose("p10")["id"]
        self.ff("promote", "--project", "p10", "--id", cand, rc=2)
        cat = SKILL / "data" / "superpowers.json"
        before = hashlib.sha256(cat.read_bytes()).hexdigest()
        rid = self.verified("p10")
        out = self.ff("promote", "--project", "p10", "--id", rid)
        self.assertEqual(out["approval"]["state"], "pending_human")
        prop = json.loads(Path(out["path"]).read_text(encoding="utf-8"))
        self.assertIsNone(prop["approval"]["approved_by"])
        self.assertNotIn(self.GOAL, json.dumps(prop, ensure_ascii=False))
        self.assertEqual(hashlib.sha256(cat.read_bytes()).hexdigest(), before)

    @case("-1.38#8", scope="engine refuses to save without a root; the no-shell card fallback is documented")
    def test_1_38_8_no_runtime_means_no_saved_memory_claim(self):
        for doc in ("PROTOCOL.md", "SESSION_PROMPT.md"):
            self.assertIn("MEMORY_RUNTIME_UNAVAILABLE", (SKILL / doc).read_text(encoding="utf-8"), doc)
        if subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=str(self.tmp), capture_output=True).returncode == 0:
            self.skipTest("the temporary directory is inside a git checkout")
        scripts = self.tmp / "nogit" / ".claude" / "skills" / "kosif-superpowers" / "scripts"
        scripts.mkdir(parents=True)
        for name in ("fusionforge.py", "_secrets.py"):
            shutil.copy2(SCRIPTS / name, scripts / name)
        work = self.tmp / "nogit-work"
        work.mkdir()
        env = {k: v for k, v in os.environ.items() if k != "KOSIF_FUSIONFORGE_ROOT"}
        r = subprocess.run([sys.executable, str(scripts / "fusionforge.py"), "catalog", "--project", "p"], cwd=str(work),
                           capture_output=True, text=True, timeout=60, env=env)
        self.assertEqual(r.returncode, 2, r.stderr)
        self.assertIn("fusionforge: error: NO_ROOT:", r.stderr)

    @case("-1.32#22", scope="FusionForge records: git-ignored, project-scoped, exported only on request")
    def test_1_32_22_memory_is_project_scoped_and_opt_in(self):
        if not shutil.which("git"):
            self.skipTest("git is not installed")
        r = subprocess.run(["git", "-C", str(REPO), "check-ignore", "-q", "out/fusionforge/anyproject/index.json"], capture_output=True)
        if r.returncode == 128:
            self.skipTest("not a git checkout")
        self.assertEqual(r.returncode, 0, "out/fusionforge is not git-ignored")
        rid = self.propose("p22")["id"]
        self.assertTrue((self.root / "p22" / "recipes" / f"{rid}.json").is_file())
        self.assertFalse((self.root / "p22" / "exports").exists(), "propose exported without being asked")


# ---------------------------------------------------------------------------------------------------- media and docs
class MediaAndDocs(unittest.TestCase):
    @case("R26", "-1.32#17", scope="tools/verify_video.py refuses a JSON timeline as a video")
    def test_R26_a_json_timeline_is_not_a_video(self):
        if not (REPO / "tools" / "verify_video.py").is_file():
            self.skipTest("tools/verify_video.py is not in this checkout (packaged skill)")
        if not (shutil.which("ffprobe") and shutil.which("ffmpeg")):
            self.skipTest("ffprobe/ffmpeg are not installed")
        with tempfile.TemporaryDirectory() as d:
            for name in ("timeline.json", "film.mp4"):
                p = Path(d) / name
                p.write_text('{"scenes": [{"text": "hello"}]}', encoding="utf-8")
                r = subprocess.run([sys.executable, str(REPO / "tools" / "verify_video.py"), str(p), "--fps", "30", "--duration", "5"],
                                   capture_output=True, text=True, timeout=120)
                self.assertNotEqual(r.returncode, 0, name)
                self.assertNotIn("Traceback", r.stderr)

    @case("H01", "H02", scope="headings: each -1.1…-1.48 once in the appendices, phases 0-11 once in the core")
    def test_H01_H02_every_old_section_has_exactly_one_home(self):
        heads = Counter()
        for p in sorted((SKILL / "references" / "protocol").glob("A*.md")):
            heads.update(re.findall(r"^#{2,4} (-1\.\d+)\s", p.read_text(encoding="utf-8"), re.M))
        for n in range(1, 49):
            self.assertEqual(heads[f"-1.{n}"], 1, f"-1.{n}")
        core = (SKILL / "PROTOCOL.md").read_text(encoding="utf-8")
        for n in range(12):
            self.assertEqual(len(re.findall(rf"^## المرحلة {n} —", core, re.M)), 1, f"phase {n}")

    @case("H03", "R28", scope="one current version everywhere and none newer in the CHANGELOG")
    def test_H03_R28_one_version_everywhere_and_no_downgrade(self):
        v = S.PROTOCOL_VERSION
        self.assertRegex(v, r"^USIP v\d+\.\d+$")
        title = (SKILL / "PROTOCOL.md").read_text(encoding="utf-8").splitlines()[0]
        self.assertIn(v, title)
        for doc in (SKILL / "SESSION_PROMPT.md", SKILL / "SKILL.md", REPO / "CLAUDE.md"):
            if not doc.is_file():
                continue  # CLAUDE.md is absent from a packaged skill
            text = doc.read_text(encoding="utf-8")
            self.assertIn(v, text, doc.name)
            older = re.search(r"USIP v(\d+\.\d+)", text)
            self.assertEqual("USIP v" + older.group(1), v, f"{doc.name}: first version named is not the current one")
        src = (SCRIPTS / "fusionforge.py").read_text(encoding="utf-8")
        self.assertIn(f'PROTOCOL = "{v}"', src)
        self.assertEqual(brief("مونتاج فيديو على صوتي بترجمة عربية")["protocol"], v)
        log = (SKILL / "references" / "protocol" / "CHANGELOG.md").read_text(encoding="utf-8")
        versions = [tuple(int(x) for x in m.split(".")) for m in re.findall(r"^## v(\d+\.\d+)", log, re.M)]
        self.assertEqual(max(versions), tuple(int(x) for x in v.split("v")[1].split(".")))

    @case("H04", scope="every schema file and a fresh brief parse (enum parity: evals/test_fusionforge.py)")
    def test_H04_contracts_parse(self):
        for p in sorted((SKILL / "schemas").glob("*.json")):
            with self.subTest(schema=p.name):
                json.loads(p.read_text(encoding="utf-8"))
        rec = json.loads((SKILL / "schemas" / "fusionforge.recipe.v2.json").read_text(encoding="utf-8"))
        self.assertIn("2020-12", rec.get("$schema", ""))
        b = json.loads(json.dumps(brief("مونتاج فيديو على صوتي بترجمة عربية"), ensure_ascii=False))
        self.assertTrue(b["schema"].startswith("kosif.skill-intelligence"))
        self.assertEqual(set(b["plans"]), {"A", "B", "C"})

    @case("H05", scope="credential patterns in the protocol, prompts and entry docs")
    def test_H05_no_credentials_in_protocol_files(self):
        files = [SKILL / "PROTOCOL.md", SKILL / "SESSION_PROMPT.md", SKILL / "SKILL.md"]
        files += [REPO / "CLAUDE.md"] if (REPO / "CLAUDE.md").is_file() else []
        files += sorted((SKILL / "references" / "protocol").glob("*.md"))
        for p in files:
            with self.subTest(doc=p.name):
                self.assertIsNone(C.SECRET_RE.search(p.read_text(encoding="utf-8")), p.name)

    @case("H06", scope="this report: every A9 row and H gate gets PASS, FAIL or NOT_RUN; every case ID used here exists")
    def test_H06_the_shadow_report_is_complete_and_honest(self):
        rows = a9_rows()
        ids = [r[0] for r in rows]
        self.assertEqual(len(ids), len(set(ids)), "duplicate A9 ids")
        self.assertEqual(len(ids), 101)
        used = set()
        for cls in (Routing, FusionForge, MediaAndDocs):
            for name in dir(cls):
                used.update(getattr(getattr(cls, name), "case_ids", ()))
        self.assertFalse(used - set(ids) - set(GATES), "case IDs missing from the A9 table")
        self.assertIn("NOT_RUN", A9.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
