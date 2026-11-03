"""Black Dragon power adapters: a power counts as executed only when the code it cites as proof ran green."""
import importlib.util
import io
import json
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".claude/skills/kosif-superpowers/scripts"
sys.path.insert(0, str(SCRIPTS))


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


power = _load("bd_power", "_black_dragon_power.py")
builder = _load("bd_power_build", "build_black_dragon_power_adapters.py")
dragon = _load("black_dragon", "black_dragon.py")

GOOD = """import unittest

class Good(unittest.TestCase):
    def test_adds(self):
        self.assertEqual(2 + 2, 4)
"""
BAD = """import unittest

class Planted(unittest.TestCase):
    def test_wrong_answer(self):
        self.assertEqual(2 + 2, 5)
"""
SKIPPED = """import unittest

class AllSkipped(unittest.TestCase):
    @unittest.skip("environment missing")
    def test_needs_gpu(self):
        pass
"""


class Fixture(unittest.TestCase):
    """A tiny power catalog whose proofs live in a gitignored out/ folder inside the repository."""

    def setUp(self):
        (ROOT / "out").mkdir(exist_ok=True)
        self.tmp = Path(tempfile.mkdtemp(dir=ROOT / "out", prefix="power-adapter-test-"))
        self.addCleanup(shutil.rmtree, self.tmp, True)
        rel = self.tmp.relative_to(ROOT).as_posix()
        (self.tmp / "test_good_fixture.py").write_text(GOOD, encoding="utf-8")
        (self.tmp / "test_planted_failure.py").write_text(BAD, encoding="utf-8")
        (self.tmp / "test_all_skipped.py").write_text(SKIPPED, encoding="utf-8")
        # A name made at run time, so no test file in the repository (this one included) can name it.
        lonely = "untested_" + self.tmp.name.rsplit("-", 1)[-1].replace("_", "") + ".py"
        (self.tmp / lonely).write_text("import argparse\nargparse.ArgumentParser().parse_args()\n", encoding="utf-8")
        cat = self.tmp / "powers"
        cat.mkdir()
        rows = [
            {"id": "FIX-GOOD", "proof": [f"kosif-tool/{rel}/test_good_fixture.py:3", "https://example.org"]},
            {"id": "FIX-GOOD-TWIN", "proof": [f"kosif-tool/{rel}/test_good_fixture.py"]},
            {"id": "FIX-BAD", "proof": [f"kosif-tool/{rel}/test_planted_failure.py"]},
            {"id": "FIX-MIXED", "proof": [f"kosif-tool/{rel}/test_good_fixture.py",
                                          f"kosif-tool/{rel}/test_planted_failure.py"]},
            {"id": "FIX-SKIP", "proof": [f"kosif-tool/{rel}/test_all_skipped.py"]},
            {"id": "FIX-HELP-ONLY", "proof": [f"kosif-tool/{rel}/{lonely}"]},
        ]
        (cat / "fixture.json").write_text(json.dumps({"powers": rows}), encoding="utf-8")
        self.addCleanup(setattr, power, "POWERS", power.POWERS)
        power.POWERS = cat
        self.job = self.tmp / "job"
        (self.job / "artifacts").mkdir(parents=True)

    def run_power(self, pid):
        artifact = self.job / "artifacts" / f"{pid}.txt"
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            code = power.main([f"power:{pid}", str(artifact), "--task=ignored", "--timeout=120"])
        return code, json.loads(artifact.read_text(encoding="utf-8"))


class Honesty(Fixture):
    def test_passing_proof_is_executed_with_a_full_receipt(self):
        code, body = self.run_power("FIX-GOOD")
        self.assertEqual(code, 0)
        self.assertEqual(body["verdict"], "passed")
        self.assertEqual(body["power"], "power:FIX-GOOD")
        (proof,) = body["proofs"]
        self.assertTrue(proof["path"].endswith("test_good_fixture.py"))
        self.assertEqual(proof["sha256"], power.sha256(ROOT / proof["path"]))
        self.assertEqual(proof["runner"], "test-file")
        self.assertEqual(proof["tests_ran"], 1)
        self.assertFalse(proof["cache_hit"])
        self.assertIn("unittest", proof["commands"][0])

    def test_shared_proof_runs_once_per_job_but_each_power_gets_its_artifact(self):
        self.run_power("FIX-GOOD")
        code, twin = self.run_power("FIX-GOOD-TWIN")
        self.assertEqual(code, 0)
        self.assertEqual(twin["power"], "power:FIX-GOOD-TWIN")
        self.assertTrue(twin["proofs"][0]["cache_hit"])
        self.assertEqual(len(list((self.job / "power-proof-cache").glob("*/result.json"))), 1)

    def test_planted_failing_test_gives_nonzero_and_no_pass(self):
        code, body = self.run_power("FIX-BAD")
        self.assertNotEqual(code, 0)
        self.assertEqual(body["verdict"], "failed")
        self.assertNotIn("passed", [p["verdict"] for p in body["proofs"]])

    def test_one_failing_proof_fails_the_whole_power(self):
        code, body = self.run_power("FIX-MIXED")
        self.assertNotEqual(code, 0)
        self.assertEqual(body["verdict"], "failed")

    def test_all_skipped_tests_are_not_a_pass(self):
        code, body = self.run_power("FIX-SKIP")
        self.assertNotEqual(code, 0)
        self.assertEqual(body["verdict"], "failed")

    def test_script_with_only_help_is_refused(self):
        code, body = self.run_power("FIX-HELP-ONLY")
        self.assertEqual(code, 2)
        self.assertEqual(body["verdict"], "refused")
        self.assertEqual(body["proofs"][0]["runner"], "none")

    def test_proof_reference_parsing(self):
        self.assertEqual(power.local_proof("kosif-tool/tools/kosif.py:12-14"), "tools/kosif.py")
        self.assertIsNone(power.local_proof("kosif-tool/../etc/passwd.py"))
        self.assertIsNone(power.local_proof("kosif-one/tools/kosif.py"))
        self.assertIsNone(power.local_proof("kosif-tool/README.md"))


class GeneratedRegistry(unittest.TestCase):
    def test_file_is_current_and_loads_into_black_dragon(self):
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()) as err:
            self.assertEqual(builder.check(), 0, err.getvalue())
        self.assertIn(builder.OUT, dragon.generated_adapter_files())
        doc = json.loads(builder.OUT.read_text(encoding="utf-8"))
        loaded = dragon._load_one_adapter_file(builder.OUT)
        inventory = dragon.full_inventory()
        self.assertGreater(len(loaded), 100)
        for key, spec in loaded.items():
            self.assertTrue(key.startswith("power:") and key in inventory, key)
            self.assertEqual(inventory[key]["kind"], "power")
            self.assertEqual(spec["args"], [key, "{artifact}", "--task={task}"])
            self.assertTrue(spec["proof_sha256"], key)
            dragon._safe_script(spec["script"])
        self.assertFalse(set(doc["adapters"]) & set(doc["excluded"]))
        for key, why in doc["excluded"].items():
            self.assertTrue(why.split(":")[0] in ("refused", "failed", "slow", "timeout"), (key, why))

    def test_check_catches_a_tampered_pin(self):
        doc = json.loads(builder.OUT.read_text(encoding="utf-8"))
        key = sorted(doc["adapters"])[0]
        path = sorted(doc["adapters"][key]["proof_sha256"])[0]
        doc["adapters"][key]["proof_sha256"][path] = "0" * 64
        with tempfile.TemporaryDirectory() as d:
            fake = Path(d) / "powers.json"
            fake.write_text(builder.render(doc["adapters"], doc["excluded"]), encoding="utf-8")
            saved = builder.OUT
            builder.OUT = fake
            try:
                with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()) as err:
                    self.assertEqual(builder.check(), 1)
            finally:
                builder.OUT = saved
        self.assertIn("proof changed since verification", err.getvalue())


if __name__ == "__main__":
    unittest.main()
