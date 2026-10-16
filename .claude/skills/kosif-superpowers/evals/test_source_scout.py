"""Regression coverage for source_scout: routing, license guards, and no side effects."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

PATH=Path(__file__).resolve().parents[1]/"scripts"/"source_scout.py"
spec=importlib.util.spec_from_file_location("source_scout",PATH)
scout=importlib.util.module_from_spec(spec)
spec.loader.exec_module(scout)


class SourceScoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry=json.loads(scout.DATA.read_text(encoding="utf-8"))
        cls.rows=scout.load()

    def top(self, query):
        results=scout.suggest(query,self.rows,5)
        return results[0]["repo"] if results else ""

    def test_catalog_has_all_reviewed_sources(self):
        self.assertEqual(len(self.rows),31)
        self.assertEqual(len({r["repo"] for r in self.rows}),31)
        self.assertEqual(len({r["domain"] for r in self.rows}),13)
        self.assertTrue(scout.validate(self.registry))

    def test_domain_specific_routing(self):
        queries={
            "keyframes timeline masking animation":"alyssaxuu/motionity",
            "procedural vector graphics svg node":"GraphiteEditor/Graphite",
            "portfolio risk market analyst trader":"TauricResearch/TradingAgents",
            "transformer attention pretraining pytorch":"rasbt/LLMs-from-scratch",
            "javascript data structures big o":"trekhleb/javascript-algorithms",
            "استضافة ذاتية سيرفر":"awesome-selfhosted/awesome-selfhosted",
            "نظام تشغيل شبكات قواعد بيانات":"CyC2018/CS-Notes",
            "برومبتات قوالب تعليمات":"f/prompts.chat",
            "agent memory persistent self improve":"NousResearch/hermes-agent",
        }
        for q,expected in queries.items():
            with self.subTest(query=q):
                self.assertEqual(self.top(q),expected)

    def test_explicit_repo_reference_wins(self):
        self.assertEqual(self.top("inspect obra/superpowers methods"),"obra/superpowers")
        self.assertEqual(self.top("OpenClaw integration"),"openclaw/openclaw")

    def test_unicode_arabic_normalization(self):
        self.assertIn("استضافه",scout.words("إستضافة"))
        self.assertIn("خوارزميات",scout.words("خوارزميات"))

    def test_empty_or_irrelevant_query_has_no_auto_discovery(self):
        for q in ("","مرحبا", "في من على"):
            self.assertEqual(scout.suggest(q,self.rows),[])

    def test_code_copy_guard_for_unverified_license(self):
        x=scout.suggest("awesome-selfhosted",self.rows,code_reuse=True)[0]
        self.assertEqual(x["reuse_gate"],"check_rights_first")
        self.assertEqual(x["execution"],"not_installed_or_executed")

    def test_permissive_license_still_checks_dependency(self):
        x=scout.suggest("GraphiteEditor/Graphite",self.rows,code_reuse=True)[0]
        self.assertEqual(x["reuse_gate"],"check_file_and_dependency_licenses")

    def test_domain_filter_and_response_cap(self):
        items=scout.suggest("tools code system prompt",self.rows,limit=100,domain="prompts")
        self.assertLessEqual(len(items),10)
        self.assertTrue(all(z["domain"]=="prompts" for z in items))

    def test_cannot_upgrade_evidence_through_registry(self):
        self.assertTrue(all(z["status"]=="reference_only" for z in self.rows))
        self.assertFalse(any("verified"==z["status"] for z in self.rows))

    def test_untrusted_catalog_mutations_are_rejected(self):
        altered=json.loads(json.dumps(self.registry))
        altered["sources"][0]["status"]="executor_exposed"
        with self.assertRaises(ValueError):
            scout.validate(altered)
        altered=json.loads(json.dumps({"schema":"kosif.community-sources.v1","sources":self.rows}))
        altered["sources"][0]["url"]="https://evil.invalid/payload"
        with self.assertRaises(ValueError):
            scout.validate(altered)

    def test_two_user_repos_get_correct_routes(self):
        self.assertEqual(self.top("scalability load balancing cache sharding consistency"), "donnemartin/system-design-primer")
        self.assertEqual(self.top("choose python libraries packages pip uv"), "vinta/awesome-python")
        self.assertEqual(self.top("convert docx pptx xlsx markdown"), "microsoft/markitdown")

    def test_snapshot_ranking_has_ten_valid_unique_repos(self):
        ranking=self.registry["python_top10"]["items"]
        self.assertEqual(len(ranking),10)
        self.assertEqual([x["rank"] for x in ranking],list(range(1,11)))
        self.assertEqual([x["repo"] for x in ranking[:2]],
                         ["public-apis/public-apis","EbookFoundation/free-programming-books"])
        self.assertEqual(ranking[-1]["repo"],"Significant-Gravitas/AutoGPT")
        self.assertTrue(all(a["stars"] > b["stars"] for a,b in zip(ranking,ranking[1:])))
        self.assertTrue(scout.validate(self.registry))

    def test_snapshot_tamper_is_rejected(self):
        tampered=json.loads(json.dumps(self.registry))
        tampered["python_top10"]["items"][0]["stars"]=0
        with self.assertRaises(ValueError):
            scout.validate(tampered)
        tampered=json.loads(json.dumps(self.registry))
        tampered["python_top10"]["items"][0]["repo"]="unknown/repository"
        with self.assertRaises(ValueError):
            scout.validate(tampered)

    def test_python_ranking_cli_reports_snapshot_not_live(self):
        run=subprocess.run([sys.executable,str(PATH),"python-top"],text=True,
                           capture_output=True,check=False,timeout=5)
        self.assertEqual(run.returncode,0,run.stderr)
        data=json.loads(run.stdout)
        self.assertEqual(len(data["items"]),10)
        self.assertFalse(data["live_star_counts"])

    def test_noncode_cc_by_reuse_gated(self):
        for repo in ("donnemartin/system-design-primer","vinta/awesome-python"):
            with self.subTest(repo=repo):
                self.assertEqual(scout.suggest(repo,self.rows,code_reuse=True)[0]["reuse_gate"],
                                 "check_rights_first")

    def test_cli_runs_without_network_or_install(self):
        run=subprocess.run([sys.executable,str(PATH),"check"],text=True,
                           capture_output=True,check=False,timeout=5)
        self.assertEqual(run.returncode,0,run.stderr)
        obj=json.loads(run.stdout)
        self.assertEqual(obj["source_count"],31)
        self.assertEqual(obj["python_rank_count"],10)
        self.assertFalse(obj["runtime_proven"])


if __name__=="__main__":
    unittest.main()
