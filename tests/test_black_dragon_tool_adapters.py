"""Black Dragon tool adapters: every program in the tool registry has a runner, and the runner is honest."""
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".claude/skills/kosif-superpowers/scripts"
RUNNER = SCRIPTS / "_black_dragon_tool.py"
sys.path.insert(0, str(SCRIPTS))
_spec = importlib.util.spec_from_file_location("black_dragon", SCRIPTS / "black_dragon.py")
dragon = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dragon)
_tspec = importlib.util.spec_from_file_location("bd_tool", RUNNER)
tool = importlib.util.module_from_spec(_tspec)
_tspec.loader.exec_module(tool)


def run(tool_id, artifact):
    return subprocess.run([sys.executable, "-B", str(RUNNER), tool_id, str(artifact)],
                          capture_output=True, text=True, timeout=600, cwd=ROOT)


class Registry(unittest.TestCase):
    def test_every_tool_has_a_runner_or_a_named_blocker(self):
        adapters = dragon._load_adapters(dragon.REVIEWED_ADAPTERS)
        tools = sorted(k for k, v in dragon.full_inventory().items() if v["kind"] == "tool")
        left = [k for k in tools if k not in adapters]
        self.assertEqual(sorted(left), sorted(dragon.TOOL_BLOCKERS), "a tool with no runner needs a named reason")
        for key in dragon.TOOL_BLOCKERS:
            self.assertNotIn(key, adapters, "a blocked tool must not also have a runner")

    def test_tool_runner_entries_name_real_registry_tools(self):
        adapters = dragon._load_adapters(dragon.REVIEWED_ADAPTERS)
        rows = {k: v for k, v in adapters.items() if v.get("tool_suite")}
        self.assertGreater(len(rows), 100)
        for key, spec in rows.items():
            t = tool.load_tool(spec["args"][0])
            self.assertTrue(tool.script_path(t).exists(), key)
            if spec["args"][0] not in tool.RECIPES:
                self.assertTrue(t.get("tests"), f"{key}: a test-suite runner needs registered tests")


class Honesty(unittest.TestCase):
    """The runner refuses or fails instead of handing out an empty pass."""

    def setUp(self):
        # The fake tool must live inside the repository (the runner resolves paths against it); out/ is gitignored.
        (ROOT / "out").mkdir(exist_ok=True)
        self.tmp = Path(tempfile.mkdtemp(dir=ROOT / "out"))
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.registry = self.tmp / "tools.json"
        self.saved = tool.TOOLS
        self.addCleanup(setattr, tool, "TOOLS", self.saved)
        tool.TOOLS = self.registry

    def fake(self, test_body, name="fake_tool"):
        script = self.tmp / f"{name}.py"
        script.write_text("print('hi')\n")
        test = self.tmp / f"test_{name}.py"
        test.write_text(test_body)
        rel = lambda p: str(p.relative_to(ROOT))
        self.registry.write_text(json.dumps({"tools": [
            {"id": "fake", "root": "repo", "path": rel(script), "tests": [rel(test)], "commands": []}]}))
        out = self.tmp / "a" / "fake.json"
        out.parent.mkdir()
        code = tool.main(["fake", str(out)])
        return code, json.loads(out.read_text())

    def test_tool_with_no_tests_and_no_recipe_is_refused(self):
        tool.TOOLS = self.saved
        out = self.tmp / "r.json"
        self.assertEqual(tool.main(["rea-owned-repo-batch", str(out)]), 2)
        self.assertEqual(json.loads(out.read_text())["verdict"], "refused")

    def test_passing_suite_passes(self):
        code, rep = self.fake("import unittest\n# fake_tool\nclass T(unittest.TestCase):\n    def test_ok(self):\n        self.assertTrue(True)\n")
        self.assertEqual((code, rep["verdict"], rep["tests_ran"]), (0, "passed", 1))

    def test_failing_suite_fails(self):
        code, rep = self.fake("import unittest\n# fake_tool\nclass T(unittest.TestCase):\n    def test_bad(self):\n        self.assertEqual(1, 2)\n")
        self.assertEqual((code, rep["verdict"]), (1, "failed"))

    def test_all_skipped_suite_fails(self):
        code, rep = self.fake("import unittest\n# fake_tool\n@unittest.skip('no app')\nclass T(unittest.TestCase):\n    def test_x(self):\n        pass\n")
        self.assertEqual((code, rep["verdict"]), (1, "failed"))

    def test_test_file_that_never_names_the_tool_is_not_counted(self):
        code, rep = self.fake("import unittest\nclass T(unittest.TestCase):\n    def test_ok(self):\n        pass\n")
        self.assertEqual((code, rep["verdict"]), (1, "failed"))
        self.assertEqual(len(rep["unrelated_tests_not_run"]), 1)
        self.assertEqual(rep["steps"], [])


class Recipes(unittest.TestCase):
    def test_fast_recipes_pass_with_known_answers(self):
        with tempfile.TemporaryDirectory() as tmp:
            for tid in ("atlas-transfer", "atlas-review-summary", "protocol-lint", "relabel-proofs", "repo-build"):
                with self.subTest(tool=tid):
                    art = Path(tmp) / f"{tid}.json"
                    done = run(tid, art)
                    rep = json.loads(art.read_text(encoding="utf-8"))
                    self.assertEqual(done.returncode, 0, json.dumps(rep, ensure_ascii=False)[:1500])
                    self.assertEqual(rep["mode"], "known-answer-recipe")
                    self.assertTrue(rep["checks"] and all(c["pass"] for c in rep["checks"]))

    def test_protocol_lint_recipe_needs_the_planted_drifts_caught(self):
        names = [c for c in tool.RECIPES]
        self.assertIn("protocol-lint", names)
        import _black_dragon_tool_recipes as R
        with tempfile.TemporaryDirectory() as tmp:
            bad = R._release(Path(tmp) / "r", broken=True)
            done = subprocess.run([sys.executable, "-B", str(SCRIPTS / "protocol_lint.py"), str(bad), "--version", "9.9", "--json"],
                                  capture_output=True, text=True, timeout=60)
            codes = sorted({f.split()[0] for f in json.loads(done.stdout)["fails"]})
            self.assertEqual((done.returncode, codes), (1, ["C", "S", "T"]))


class FormerlyBlocked(unittest.TestCase):
    """Blender and Remotion were unblocked by real engines; only the owner's GitHub/phone tools stay blocked."""

    def test_only_the_owner_bound_tools_stay_blocked(self):
        adapters = dragon._load_adapters(dragon.REVIEWED_ADAPTERS)
        self.assertEqual(sorted(dragon.TOOL_BLOCKERS), ["tool:rea-owned-repo-batch", "tool:rebalance-creative-repos",
                                                        "tool:repo-ashell-cinema"])
        for key in ("tool:blender-rescue-scene", "tool:blender-cat-fur-upgrade", "tool:starter-remotion"):
            self.assertTrue(adapters[key].get("tool_suite"), key)
        self.assertIn("starter-remotion", tool.RECIPES)

    def test_recipe_fails_without_node_modules(self):
        import _black_dragon_tool_recipes as R
        with tempfile.TemporaryDirectory() as tmp:
            empty = Path(tmp) / "remotion"
            empty.mkdir()
            checks = []
            R.starter_remotion(R.Ctx(tool={}, script=empty, work=Path(tmp), env=dict(), timeout=30, task="",
                                     steps=[], check=lambda n, ok, v=None: checks.append(ok)))
            self.assertEqual(checks, [False])


BLENDER_ENGINE = shutil.which("blender") or importlib.util.find_spec("bpy")


@unittest.skipUnless(BLENDER_ENGINE, "neither the Blender app nor the bpy module (pip install bpy) is installed")
class BlenderToolsRunTheirRealTests(unittest.TestCase):
    """The 10 Blender tests really run (under the app, or the bpy module from PyPI) and none is skipped."""

    def test_both_blender_tools_pass_with_no_skips(self):
        with tempfile.TemporaryDirectory() as tmp:
            for tid, script in (("blender-rescue-scene", "blender_rescue_scene.py"),
                                ("blender-cat-fur-upgrade", "blender_cat_fur_upgrade.py")):
                with self.subTest(tool=tid):
                    art = Path(tmp) / f"{tid}.json"
                    done = run(tid, art)
                    rep = json.loads(art.read_text(encoding="utf-8"))
                    self.assertEqual(done.returncode, 0, json.dumps(rep, ensure_ascii=False)[:1500])
                    self.assertEqual((rep["verdict"], rep["mode"]), ("passed", "own-test-suite"))
                    self.assertTrue(rep["script"].endswith(script))
                    self.assertGreaterEqual(rep["tests_ran"], 10)
                    self.assertEqual(rep["tests_skipped"], 0)


REMOTION_CLI = ROOT / "starters/remotion/node_modules/.bin/remotion"


@unittest.skipUnless(REMOTION_CLI.is_file() and shutil.which("node"),
                     "starters/remotion has no node_modules (run npm ci there)")
class RemotionStarterRenders(unittest.TestCase):
    def test_known_answers_and_planted_flaw(self):
        with tempfile.TemporaryDirectory() as tmp:
            art = Path(tmp) / "starter-remotion.json"
            done = run("starter-remotion", art)
            rep = json.loads(art.read_text(encoding="utf-8"))
            self.assertEqual(done.returncode, 0, json.dumps(rep, ensure_ascii=False)[:2000])
            self.assertEqual((rep["verdict"], rep["mode"]), ("passed", "known-answer-recipe"))
            checks = {c["check"]: c for c in rep["checks"]}
            self.assertEqual(checks["composition KosifFilm: 30 fps, 1080x1920, 360 frames"]["value"], [30, 1080, 1920, 360])
            self.assertEqual(checks["frame 60: 1080x1920 PNG with real, non-blank pixels"]["value"]["size"], [1080, 1920])
            self.assertTrue(checks["planted flaw caught: unknown composition refused, no file written"]["pass"])
            self.assertEqual(len(rep["checks"]), 7)



@unittest.skipUnless(shutil.which("node"), "node is not installed")
class CollectLinksRunsInsideTheRepo(unittest.TestCase):
    """The repository's package.json says "type": "module"; collect_links.js must still start (it used require())."""

    def test_starts_as_an_es_module(self):
        done = subprocess.run(["node", str(SCRIPTS / "collect_links.js")], capture_output=True, text=True, timeout=60, cwd=ROOT)
        self.assertEqual(done.returncode, 2, done.stderr)  # usage error, not "require is not defined"
        self.assertNotIn("require is not defined", done.stderr)


if __name__ == "__main__":
    unittest.main()
