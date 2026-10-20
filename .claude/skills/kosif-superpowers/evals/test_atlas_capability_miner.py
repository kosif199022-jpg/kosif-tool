"""Atlas capability miner: fixture-only tests. No network, no Atlas code executed, no REA required."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import atlas_capability_miner as m  # noqa: E402


def make_atlas(root: Path) -> Path:
    atlas = root / "atlas"
    skills = [
        {"id": 1, "plugin": "p-git", "skill": "commit", "description": "Derive a conventional commit message from the staged diff and commit safely.",
         "license": "MIT", "source": "https://github.com/o/r/tree/abc/plugins/p-git", "path": "skills/1-p-git/1-commit",
         "files": ["SKILL.md", "scripts/commit.sh"], "complete": True, "risk_flags": ["scripts"], "verdict": "REVIEW_BEFORE_INSTALL"},
        {"id": 2, "plugin": "p-sec", "skill": "security-audit", "description": "Run a security audit for OWASP vulnerabilities and secrets.",
         "license": "Apache-2.0", "source": "https://github.com/o/r/tree/abc/plugins/p-sec", "path": "skills/2-p-sec/2-security-audit",
         "files": ["SKILL.md"], "complete": True, "risk_flags": [], "verdict": "READ_ONLY_OK"},
        {"id": 3, "plugin": "p-sec-mirror", "skill": "security-audit", "description": "Run a security audit for OWASP vulnerabilities and secrets.",
         "license": "MIT", "source": "https://github.com/o/r2/tree/abc/plugins/p-sec", "path": "skills/3-p-sec-mirror/3-security-audit",
         "files": ["SKILL.md"], "complete": True, "risk_flags": [], "verdict": "READ_ONLY_OK"},
        {"id": 4, "plugin": "p-video", "skill": "remotion-render", "description": "Render a Remotion video composition with ffmpeg and animation keyframes.",
         "license": "MIT", "source": "https://github.com/o/r/tree/abc/plugins/p-video", "path": "skills/4-p-video/4-remotion-render",
         "files": ["SKILL.md", "render.mjs", "lib/util.ts"], "complete": True, "risk_flags": ["scripts"], "verdict": "REVIEW_BEFORE_INSTALL"},
    ]
    copyleft = [{"id": "x1", "plugin": "gpl-tool", "skill": "gpl-thing", "description": "A GPL licensed data pipeline with airflow and dbt.",
                 "license": "GPL-3.0", "source": "https://github.com/o/g/tree/abc", "path": "skills/x1-gpl-tool/x1-gpl-thing",
                 "files": ["SKILL.md"], "complete": True, "risk_flags": [], "verdict": "READ_ONLY_OK"}]
    atlas.mkdir()
    (atlas / "index.json").write_text(json.dumps({"count": 4, "skills": skills}), encoding="utf-8")
    (atlas / "index-copyleft.json").write_text(json.dumps({"count": 1, "skills": copyleft}), encoding="utf-8")
    for s in skills + copyleft:
        d = atlas / s["path"]
        d.mkdir(parents=True)
        (d / "SKILL.md").write_text("---\nname: %s\ndescription: \"%s\"\ntags: [a, b]\nallowed-tools: Bash(git:*)\n---\n# body\n"
                                    % (s["skill"], s["description"]), encoding="utf-8")
    return atlas


class ClassifyTests(unittest.TestCase):
    def test_keyword_taxonomy_is_deterministic(self):
        a = m.classify("commit", "Derive a conventional commit message from the staged diff", [])
        b = m.classify("commit", "Derive a conventional commit message from the staged diff", [])
        self.assertEqual(a, b)
        self.assertEqual(a["theme"], "git-release")
        self.assertEqual(a["domain"], "code")

    def test_fallback_when_nothing_matches(self):
        c = m.classify("zzz", "qqq www", [])
        self.assertEqual(c["theme"], m.FALLBACK_THEME)

    def test_every_theme_has_a_known_domain(self):
        for theme, (dom, ar, en, kws) in m.THEMES.items():
            self.assertIn(dom, m.DOMAINS, theme)
            self.assertTrue(kws, theme)
            self.assertTrue(ar and en, theme)


class IndexTests(unittest.TestCase):
    def test_index_stats_search_batches(self):
        with tempfile.TemporaryDirectory() as d:
            atlas = make_atlas(Path(d))
            idx = m.build_index(atlas)
            self.assertEqual(idx["count"], 5)
            by_id = {str(s["id"]): s for s in idx["skills"]}
            self.assertEqual(by_id["1"]["sh"], 1)
            self.assertEqual(by_id["4"]["js"], 2)
            self.assertEqual(by_id["4"]["domain"], "motion")
            self.assertTrue(by_id["x1"]["copyleft"])
            self.assertEqual(by_id["2"]["desc_dupes"], 1)   # mirrored description
            self.assertEqual(by_id["1"]["tools"], "Bash(git:*)")
            st = m.stats(idx)
            self.assertEqual(st["skills"], 5)
            self.assertEqual(st["copyleft"], 1)
            self.assertEqual(st["unique_descriptions"], 4)
            hits = m.search(idx, "security audit owasp", top=3)
            self.assertEqual(str(hits[0]["id"]), "2")
            self.assertTrue(hits[0]["online_url"].startswith(m.ATLAS_REPO))
            ar = m.search(idx, "فيديو موشن", top=2)
            self.assertEqual(str(ar[0]["id"]), "4")
            out = Path(d) / "batches"
            r = m.write_batches(idx, out, size=2)
            self.assertEqual(r["themes"], len({s["theme"] for s in idx["skills"]}))
            manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(sum(b["records"] for b in manifest), 4)   # mirror collapsed
            gz = Path(d) / "idx.json.gz"
            m.save_index(idx, gz)
            self.assertEqual(m.load_index(gz)["count"], 5)


class ReaTests(unittest.TestCase):
    def test_batch_refuses_without_authorization(self):
        with tempfile.TemporaryDirectory() as d:
            r = m.rea_batch(Path(d), Path(d) / "none.json", Path(d) / "out", authorized=False, limit=1, timeout=1, keep=False)
            self.assertEqual(r["status"], "authorization_required")
            self.assertFalse(r["analysis_executed"])

    def test_summarize_evidence_is_compact_and_path_free(self):
        ev = {"evidence_id": "ev_x", "provider": {"id": "rea-javascript-application"}, "predicate_type": "rea.javascript-application-analysis",
              "normalized_result": {"root_artifact_sha256": "abc", "statistics": {"parsed_javascript_files": 2, "relevant_files": 3},
                                    "graph": {"nodes": [{"kind": "javascript-module", "observations": [{"properties": {"declared_specifier": "react", "resolution_status": "external"}}]},
                                                        {"kind": "javascript-module", "observations": [{"properties": {"declared_specifier": "./x", "resolution_status": "not-found"}}]},
                                                        {"kind": "unknown", "observations": [{"properties": {"inline_script_count": 2, "path": "/secret/local/path.html"}}]}],
                                              "edges": [{"relation": "imports"}]},
                                    "semantic_graph": {"nodes": [{"kind": "boundary", "properties": {"boundary_kind": "child-process"}}], "unknowns": [1, 2]},
                                    "limitations": ["static only"], "summary": {"ipc": {}}, "integrity_contradictions": []}}
        s = m.summarize_evidence(ev)
        self.assertEqual(s["external_packages"], {"react": 1})
        self.assertEqual(s["unresolved_local_imports"], 1)
        self.assertEqual(s["inline_html_scripts_not_analyzed"], 2)
        self.assertEqual(s["boundaries"], {"child-process": 1})
        self.assertEqual(s["unknowns"], 2)
        self.assertNotIn("/secret/local/path.html", json.dumps(s))

    def test_receipts_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            runs = [{"id": 1, "plugin": "p", "skill": "s", "path": "skills/1", "status": "evidence", "rea_version": "6.7.0", "exit": 0, "seconds": 1.0,
                     "summary": {"evidence_id": "ev", "root_sha256": "r", "statistics": {"parsed_javascript_files": 1}, "graph_nodes": 2, "graph_edges": 1,
                                 "external_packages": {"react": 1}, "boundaries": {}, "unresolved_local_imports": 0, "inline_html_scripts_not_analyzed": 0,
                                 "unknowns": 0, "limitations": ["x"]}},
                    {"id": 2, "status": "timeout_10s", "exit": None}]
            p = Path(d) / "runs.json"
            p.write_text(json.dumps(runs), encoding="utf-8")
            r = m.rea_receipts(p)
            self.assertEqual(r["evidence_records"], 1)
            self.assertEqual(r["runs"], 2)
            self.assertEqual(r["packages_by_skill_count"][0][0], "react")

    def test_script_never_executes_atlas_code(self):
        src = (SK / "scripts" / "atlas_capability_miner.py").read_text(encoding="utf-8")
        for bad in ("os.system", "eval(", "exec(", "importlib", "requests.", "urllib.request"):
            self.assertNotIn(bad, src)
        # the only subprocess targets are the REA launcher (rea --version / analyze-javascript-application)
        self.assertEqual(src.count("subprocess.run("), 2)


if __name__ == "__main__":
    unittest.main()
