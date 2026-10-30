"""The front door (scripts/hub.py), the tool registry (data/tools.json) and the catalog MCP server (scripts/kosif_mcp.py).

    python3 -m unittest discover -s .claude/skills/kosif-superpowers/evals -p test_hub.py -v
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
SCRIPTS = SKILL / "scripts"
REPO = SKILL.parents[2]
sys.path.insert(0, str(SCRIPTS))
import hub  # noqa: E402
import powers as P  # noqa: E402

# A request in the user's words → a tool that must appear in the top 3 of `hub.py find`.
ROUTING = [
    ("ارسم قطة وإنسان يمشوا في الشارع بالكود", "code-drawing-master"),
    ("render a spinning cube to mp4 without installing blender", "native-3d"),
    ("export an animated glb file without blender", "native-glb"),
    ("حلل فيديو مرجعي وطلّع توقيت القطعات", "motion-reference-probe"),
    ("rebuild the edit of this reference video as a remotion project with my clips", "reference-edit-engine"),
    ("شيل الضباب وقلل النويز من صوري", "app-studio"),
    ("inspect this windows installer setup.exe before running it", "installer-triage"),
    ("BPM and beat hypotheses from my song wav", "music-rhythm-engine"),
    ("check the final mp4 duration fps and audio track before delivery", "verify-video"),
    ("connect claude desktop to files in a folder on my computer", "kosif-remote-commander"),
    ("حرّك ذراع الشخصية عند كلمة معينة في التسجيل", "character-ik"),
    ("رندر سينمائي بسايكلز في بلندر", "blender-cycles-render"),
    ("find a whiteboard motion style and scaffold a project", "repo-kosif"),
    ("convert my srt captions to words.json", "repo-words-convert"),
    ("ايش اللي تقدر تعمله على الجهاز ده", "probe-env"),
    ("نص آيات القرآن وتوقيت الكلمات مع صوت القارئ", "quran-text"),
    ("هات نص الآيات بالتشكيل واعمل توقيت كل كلمة في التلاوة", "quran-text"),
    ("اعرضها على المجلس بشرط لا ترجمة للآيات", "llm-council"),
]


def run(*args, cwd=SKILL, env=None, inp=None, timeout=120):
    return subprocess.run([sys.executable, *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8",
                          timeout=timeout, env=env, input=inp)


class RegistryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reg = json.loads(hub.TOOLS_JSON.read_text(encoding="utf-8"))

    def test_registry_is_valid(self):
        self.assertEqual(hub.validate_registry(self.reg), [])

    def test_every_script_and_repo_tool_is_registered(self):
        registered = {(t["root"], t["path"].rstrip("/")) for t in self.reg["tools"]}
        missing = [f"scripts/{f.name}" for f in sorted(SCRIPTS.iterdir())
                   if f.suffix in (".py", ".cjs", ".mjs") and not f.name.startswith(("test_", "_"))
                   and ("skill", f"scripts/{f.name}") not in registered]
        missing += [f"tools/{f.name} (repo)" for f in sorted((REPO / "tools").iterdir())
                    if f.suffix in (".py", ".cjs") and ("repo", f"tools/{f.name}") not in registered]
        self.assertEqual(missing, [], "add these to data/tools.json (references/guides/maintain.md)")

    def test_examples_name_files_that_exist(self):
        for t in self.reg["tools"]:
            base = SKILL if t["root"] == "skill" else REPO
            for c in t["commands"]:
                for ref in re.findall(r"(?<![\w./-])((?:scripts|tools|resources|assets|starters|templates)/[\w./-]+\.(?:json|py|cjs|mjs|js|sh))(?![\w])", c["example"]):
                    with self.subTest(tool=t["id"], ref=ref):
                        self.assertTrue((base / ref).exists() or (SKILL / ref).exists() or (REPO / ref).exists(), f"{t['id']}: {ref}")

    def test_cli_help_works_without_optional_dependencies(self):
        """`--help` must never crash: heavy imports belong inside the commands that need them."""
        for t in self.reg["tools"]:
            path = (SKILL if t["root"] == "skill" else REPO) / t["path"]
            if t["kind"] != "cli" or path.suffix not in (".py", ".cjs"):
                continue
            if path.suffix == ".cjs" and not shutil.which("node"):
                continue
            with self.subTest(tool=t["id"]):
                cwd = SKILL if t["root"] == "skill" else REPO
                if path.suffix == ".py":
                    proc = run(str(path), "--help", cwd=cwd, timeout=60)
                else:
                    proc = subprocess.run(["node", str(path), "--help"], cwd=cwd, capture_output=True, text=True, timeout=60)
                self.assertEqual(proc.returncode, 0, f"{t['id']} --help failed: {proc.stderr[-400:]}")

    def test_schema_enums_match_the_code(self):
        schema = json.loads((SKILL / "schemas" / "tools.schema.json").read_text(encoding="utf-8"))
        tool = schema["$defs"]["tool"]["properties"]
        self.assertEqual(tuple(tool["area"]["enum"]), hub.AREAS)
        self.assertEqual(tuple(tool["kind"]["enum"]), hub.KINDS)
        self.assertEqual(set(tool["safety"]["enum"]), set(hub.SAFETY))
        self.assertEqual(tuple(tool["evidence"]["enum"]), hub.EVIDENCE)
        self.assertEqual(set(schema["$defs"]["tool"]["required"]) - set(self.reg["tools"][0]), set())

    def test_power_schema_describes_every_record(self):
        schema = json.loads((SKILL / "schemas" / "power.schema.json").read_text(encoding="utf-8"))
        pat = re.compile(schema["properties"]["id"]["pattern"])
        statuses = set(schema["properties"]["status"]["enum"])
        scopes = set(schema["properties"]["proof_scope"]["enum"])
        for p in P.load_powers():
            self.assertTrue(pat.match(p["id"]), p["id"])
            self.assertIn(p["status"], statuses, p["id"])
            self.assertIn(p["proof_scope"], scopes, p["id"])
            missing = [k for k in schema["required"] if k not in p]
            self.assertEqual(missing, [], p["id"])


class BundledCopiesTest(unittest.TestCase):
    """The skill ships copies of three repo tools so it works without the repository; they must not drift."""
    PAIRS = (("tools/render_html.cjs", "resources/motion-runtime/render_html.cjs"),
             ("tools/verify_video.py", "scripts/verify_video.py"),
             ("tools/aspects.py", "scripts/aspects.py"))

    def test_bundled_copies_match_the_repo_tools(self):
        for repo_rel, skill_rel in self.PAIRS:
            with self.subTest(tool=repo_rel):
                self.assertEqual((REPO / repo_rel).read_bytes(), (SKILL / skill_rel).read_bytes(),
                                 f"{skill_rel} differs from {repo_rel}: copy the repo version over it")


class FindTest(unittest.TestCase):
    def test_routing_cases(self):
        reg = hub.load_registry()
        misses = []
        for brief, want in ROUTING:
            got = [t["id"] for t in hub.find(brief, limit_tools=3, reg=reg)["tools"]]
            if want not in got:
                misses.append(f"{brief!r}: wanted {want}, got {got}")
        self.assertEqual(misses, [])

    def test_find_json_shape(self):
        proc = run("scripts/hub.py", "find", "اعمل فيديو موشن عربي متزامن مع صوتي 9:16", "--json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        for key in ("tools", "execution_plan", "powers", "guides", "family_chapters", "styles", "next"):
            self.assertIn(key, data)
        self.assertTrue(data["tools"] and data["powers"])
        self.assertIn(data["tools"][0]["readiness"]["state"], ("ready", "missing", "unavailable"))
        self.assertIn("matched_terms", data["tools"][0])
        self.assertIn("strong_terms", data["tools"][0])
        self.assertEqual(data["execution_plan"]["primary"], data["execution_plan"]["ready_now"][0])

    def test_execution_plan_separates_ready_tools_and_aggregates_unlocks(self):
        cards = [
            {"id": "ready", "readiness": {"state": "ready", "missing": []}},
            {"id": "blocked-a", "readiness": {"state": "missing", "missing": ["bin:ffmpeg", "pip:cv2"]}},
            {"id": "blocked-b", "readiness": {"state": "missing", "missing": ["bin:ffmpeg"]}},
        ]
        plan = hub.execution_plan(cards)
        self.assertEqual(plan["primary"], "ready")
        self.assertEqual(plan["ready_now"], ["ready"])
        self.assertEqual(plan["best_unlocks"][0], {"requirement": "bin:ffmpeg", "tools_unlocked": 2})

    def test_match_explanation_uses_the_same_fields_as_ranking(self):
        tool = hub.load_registry()["tools"][0]
        phrase = tool["keywords"][0]
        explanation = hub.explain_tool_match(tool, hub.terms_of(phrase))
        self.assertTrue(explanation["matched_terms"], (tool["id"], phrase, explanation))
        self.assertTrue(set(explanation["strong_terms"]) <= set(explanation["matched_terms"]))

    def test_human_output_from_repo_root_rewrites_paths(self):
        proc = run(".claude/skills/kosif-superpowers/scripts/hub.py", "find", "render a 3D cube without blender", cwd=REPO)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("$ python3 .claude/skills/kosif-superpowers/scripts/", proc.stdout)

    def test_tool_list_doctor_docs_power(self):
        for args in (("tool", "native-3d"), ("tool", "native-3d", "--json"), ("list",), ("list", "--area", "3d", "--json"),
                     ("areas",), ("doctor",), ("doctor", "--json"), ("docs", "blender"), ("power", "3D-01"), ("mcp-config", "--json")):
            with self.subTest(args=args):
                proc = run("scripts/hub.py", *args)
                self.assertEqual(proc.returncode, 0, proc.stderr)
                self.assertTrue(proc.stdout.strip())
        self.assertNotEqual(run("scripts/hub.py", "tool", "no-such-tool").returncode, 0)

    def test_generated_files_are_current(self):
        proc = run("scripts/hub.py", "build", "--check")
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_manifest_counts_match_the_catalog(self):
        m = json.loads((SKILL / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(m["counts"]["powers"], len(P.load_powers()))
        self.assertEqual(m["counts"]["tools"], len(hub.load_registry()["tools"]))
        self.assertEqual(len(m["families"]), len(list((SKILL / "data" / "powers").glob("*.json"))))

    def test_run_asks_for_consent_first(self):
        reg = hub.load_registry()
        gated = next(t for t in reg["tools"] if t["consent"] and t["kind"] == "cli" and t["path"].endswith(".py") and t["root"] == "skill")
        proc = run("scripts/hub.py", "run", gated["id"], "--definitely-not-a-flag")
        self.assertEqual(proc.returncode, 3, proc.stderr)
        self.assertIn("--yes", proc.stderr)
        ok = run("scripts/hub.py", "run", "powers", "stats")  # listed in the tool's safe_commands
        self.assertEqual(ok.returncode, 0, ok.stderr)
        risky = run("scripts/hub.py", "run", "powers", "env", "--json")  # not listed: still gated
        self.assertEqual(risky.returncode, 3, risky.stderr)
        bare = run("scripts/hub.py", "run", gated["id"])  # a bare run is not exempt
        self.assertEqual(bare.returncode, 3, bare.stderr)

    def test_run_passes_a_late_separator_to_the_tool(self):
        proc = run("scripts/hub.py", "run", "invention-lab", "invent", "--", "-captions")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout)["problem"], "-captions")

    def test_tool_lookup_needs_a_whole_id_or_file_name(self):
        for bad in ("", "py", "s"):
            self.assertEqual(run("scripts/hub.py", "tool", bad).returncode, 1, bad)
        self.assertEqual(run("scripts/hub.py", "tool", "hub.py").returncode, 0)

    def test_shown_rewrites_paths_once_and_quotes_odd_roots(self):
        tool = {"root": "skill"}
        out = hub.shown("node -e \"import x from './resources/a.mjs'\" ../../../proofs/p.blend scripts/x.py", tool, cwd=Path("/"))
        prefix = os.path.relpath(SKILL, "/").replace(os.sep, "/")
        self.assertEqual(out, f"node -e \"import x from '{prefix}/resources/a.mjs'\" {prefix}/../../../proofs/p.blend {prefix}/scripts/x.py")


class ArabicSearchTest(unittest.TestCase):
    def test_imperatives_and_clitics_gain_a_matchable_stem(self):
        stems = P.arabic_stems(["ارسم", "وارسم", "احذف", "والخلفية", "ايه", "render"])
        for want in ("رسم", "حذف", "خلفيه"):
            self.assertIn(want, stems)
        self.assertNotIn("render", stems)

    def test_drawing_request_reaches_drawing_powers(self):
        picked = P.suggest(P.load_powers(), P.load_styles(), "ارسم قطة بالكود")["picked"]
        fams = {p["family"] for _s, p in picked}
        self.assertTrue(fams & {"hand-drawn-draw-on", "characters-rigs", "runnable-tools", "ai-generation"}, fams)


class McpServerTest(unittest.TestCase):
    def test_selftest(self):
        proc = run("scripts/kosif_mcp.py", "--selftest")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_stdio_session(self):
        msgs = [
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-03-26", "capabilities": {}}},
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
            {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "kosif_find", "arguments": {"task": "ارسم شخصية كرتونية بالكود"}}},
            {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "kosif_read_guide", "arguments": {"path": "/etc/passwd"}}},
        ]
        proc = run(str(SCRIPTS / "kosif_mcp.py"), inp="\n".join(json.dumps(m) for m in msgs) + "\n", cwd=REPO)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        lines = proc.stdout.strip().splitlines()
        self.assertEqual(len(lines), 4, "one reply per request, none for the notification, nothing else on stdout")
        replies = {r["id"]: r for r in map(json.loads, lines)}
        self.assertEqual(replies[1]["result"]["protocolVersion"], "2025-03-26")
        names = {t["name"] for t in replies[2]["result"]["tools"]}
        self.assertTrue({"kosif_find", "kosif_tool", "kosif_power", "kosif_doctor"} <= names)
        found = json.loads(replies[3]["result"]["content"][0]["text"])
        self.assertIn("code-drawing-master", [t["id"] for t in found["tools"]])
        self.assertTrue(replies[4]["result"]["isError"])

    def test_bad_input_never_stops_the_server(self):
        lines = [
            "not json",
            "[1, 2]",
            json.dumps([{"jsonrpc": "2.0", "id": 7, "method": "ping"}, {"jsonrpc": "2.0", "method": "notifications/x"}]),
            json.dumps({"jsonrpc": "2.0", "id": 8, "method": "resources/read", "params": {"uri": "kosif://nope"}}),
            json.dumps({"jsonrpc": "2.0", "id": 9, "result": {}}),  # a client response: no reply
            json.dumps({"jsonrpc": "2.0", "id": 10, "method": "tools/call",
                        "params": {"name": "kosif_search_powers", "arguments": {"query": "kinetic", "limit": -1}}}),
            json.dumps({"jsonrpc": "2.0", "id": 11, "method": "ping"}),
        ]
        proc = subprocess.run([sys.executable, str(SCRIPTS / "kosif_mcp.py")], input=("\n".join(lines) + "\n").encode() + b"\xff\xfe{\n",
                              capture_output=True, timeout=120)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = proc.stdout.decode("ascii")  # replies are pure ASCII JSON
        replies = [json.loads(x) for x in out.strip().splitlines()]
        self.assertEqual(replies[0]["error"]["code"], -32700)
        self.assertEqual([r["error"]["code"] for r in replies[1]], [-32600, -32600])
        self.assertEqual(replies[2], [{"jsonrpc": "2.0", "id": 7, "result": {}}])
        self.assertEqual(replies[3]["error"]["code"], -32002)
        self.assertEqual(len(json.loads(replies[4]["result"]["content"][0]["text"])), 1, "limit is clamped to 1..50")
        self.assertEqual(replies[5]["id"], 11)
        self.assertEqual(replies[6]["error"]["code"], -32700)
        self.assertEqual(len(replies), 7)

    def test_standalone_install_works_without_the_repo(self):
        import shutil
        with tempfile.TemporaryDirectory() as tmp:
            dst = Path(tmp) / ".claude" / "skills" / "kosif-superpowers"
            shutil.copytree(SKILL, dst, ignore=shutil.ignore_patterns("__pycache__", "node_modules", "*.mp4", "*.mov", "*.png", "*.jpg", "*.webm"))
            proc = run(str(dst / "scripts" / "kosif_mcp.py"), "--selftest", cwd=dst)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            proc = run(str(dst / "scripts" / "hub.py"), "find", "ارسم شخصية كرتونية بالكود", "--json", cwd=dst)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertTrue(json.loads(proc.stdout)["tools"])

    def test_find_next_command_quotes_the_task(self):
        res = hub.find('شعار $(touch /tmp/x) "مقتبس"', reg=hub.load_registry())
        plan = [n for n in res["next"] if "requirements.py plan" in n][0]
        self.assertIn("'شعار $(touch /tmp/x) \"مقتبس\"'", plan)

    def test_project_mcp_config_points_at_the_server(self):
        cfg = json.loads((REPO / ".mcp.json").read_text(encoding="utf-8"))
        args = cfg["mcpServers"]["kosif-superpowers"]["args"]
        self.assertTrue((REPO / args[0]).is_file())


if __name__ == "__main__":
    unittest.main()
