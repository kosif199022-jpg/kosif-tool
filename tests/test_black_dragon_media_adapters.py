"""Black Dragon media adapters: real video/audio tools, known-answer self-test, honest failure."""
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
WRAPPER = SCRIPTS / "_black_dragon_media.py"
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location("black_dragon", SCRIPTS / "black_dragon.py")
dragon = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dragon)
mspec = importlib.util.spec_from_file_location("bd_media", WRAPPER)
media = importlib.util.module_from_spec(mspec)
mspec.loader.exec_module(media)

HAVE_FFMPEG = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))


def run(recipe, artifact, *extra):
    return subprocess.run([sys.executable, str(WRAPPER), recipe, str(artifact), *extra],
                          capture_output=True, text=True, timeout=600)


class MediaAdapterRegistry(unittest.TestCase):
    def test_every_media_adapter_names_a_real_recipe_and_catalog_tool(self):
        adapters = dragon._load_adapters(dragon.REVIEWED_ADAPTERS)
        inventory = dragon.full_inventory()
        rows = {k: v for k, v in adapters.items() if v.get("media")}
        self.assertGreaterEqual(len(rows), 8)
        self.assertEqual(sorted(v["args"][0] for v in rows.values()), sorted(media.RECIPES))
        for key in rows:
            self.assertIn(key, inventory)
            self.assertEqual(inventory[key]["kind"], "tool")

    def test_blocked_reasons_separate_methods_from_programs(self):
        self.assertEqual(dragon._why_blocked("tool"), "tool_without_adapter")
        for kind in ("power", "skill", "style", "playbook", "protocol", "superpower"):
            self.assertEqual(dragon._why_blocked(kind), "method_description")


@unittest.skipUnless(HAVE_FFMPEG, "ffmpeg/ffprobe not installed")
class MediaAdapterRuns(unittest.TestCase):
    def test_every_recipe_passes_its_known_answer_self_test(self):
        with tempfile.TemporaryDirectory() as tmp:
            for recipe in media.RECIPES:
                with self.subTest(recipe=recipe):
                    art = Path(tmp) / f"{recipe}.txt"
                    done = run(recipe, art)
                    report = json.loads(art.read_text(encoding="utf-8"))
                    self.assertEqual(done.returncode, 0, json.dumps(report, ensure_ascii=False)[:1500])
                    self.assertEqual(report["verdict"], "passed")
                    self.assertEqual(report["input"]["kind"], "self-test")
                    self.assertTrue(report["checks"])
                    for row in report["outputs"]:
                        out = Path(row["path"])
                        self.assertTrue(out.is_file())
                        self.assertEqual(media.sha256(out), row["sha256"])
                        self.assertTrue(out.is_relative_to(art.with_name(art.stem + ".work")))

    def test_missing_or_broken_media_fails_and_never_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            art = Path(tmp) / "missing.txt"
            self.assertEqual(run("cinema", art, "--media=" + str(Path(tmp) / "nope.mp4")).returncode, 1)
            self.assertEqual(json.loads(art.read_text())["verdict"], "failed")
            junk = Path(tmp) / "junk.mp4"
            junk.write_text("not a video", encoding="utf-8")
            art2 = Path(tmp) / "junk.txt"
            self.assertEqual(run("rhythm", art2, "--media=" + str(junk)).returncode, 1)

    def test_user_media_is_used_and_left_untouched(self):
        with tempfile.TemporaryDirectory() as tmp:
            clip = media.self_test_clip(Path(tmp))
            before = media.sha256(clip)
            art = Path(tmp) / "cut.txt"
            self.assertEqual(run("cut", art, "--media=" + str(clip)).returncode, 0)
            report = json.loads(art.read_text())
            self.assertEqual(report["input"]["kind"], "user-media")
            self.assertEqual(report["input"]["sha256"], before)
            self.assertEqual(media.sha256(clip), before)

    def test_black_dragon_passes_media_to_adapters_and_reports_it(self):
        adapters = dragon._load_adapters(dragon.REVIEWED_ADAPTERS)
        keep = {"tool:fast-edit": adapters["tool:fast-edit"],
                "tool:audio-cue-mapper": adapters["tool:audio-cue-mapper"]}
        with tempfile.TemporaryDirectory() as tmp:
            clip = media.self_test_clip(Path(tmp))
            job = Path(tmp) / "job"
            result = dragon.run("cut on the beat", job, keep, workers=2, allow_execution=True,
                                timeout=300, media=clip)
            self.assertEqual(result["executed"], 2, result)
            self.assertEqual(result["media"]["sha256"], media.sha256(clip))
            self.assertEqual(sum(result["blocked_why"].values()), result["blocked"])
            ledger = json.loads((job / "all_skills_ledger.json").read_text())
            art = json.loads(Path(ledger["items"]["tool:fast-edit"]["receipt"]["artifact"]).read_text())
            self.assertEqual(art["input"]["kind"], "user-media")


if __name__ == "__main__":
    unittest.main()
