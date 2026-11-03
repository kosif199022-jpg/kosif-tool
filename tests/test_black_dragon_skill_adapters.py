"""Black Dragon skill adapters: the scripts that skills ship really run and are checked."""
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
WRAPPER = SCRIPTS / "_black_dragon_skill.py"
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location("black_dragon", SCRIPTS / "black_dragon.py")
dragon = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dragon)
sspec = importlib.util.spec_from_file_location("bd_skill", WRAPPER)
skill = importlib.util.module_from_spec(sspec)
sspec.loader.exec_module(skill)

HAVE_FFMPEG = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))


def missing_module(recipe):
    name = skill.NEEDS_MODULE.get(recipe)
    return bool(name) and importlib.util.find_spec(name) is None
TASK = "اعمل مونتاج فيديو موشن جرافيك بصوت"


def run(recipe, artifact, *extra):
    return subprocess.run([sys.executable, str(WRAPPER), recipe, str(artifact), *extra],
                          capture_output=True, text=True, timeout=600)


class SkillAdapterRegistry(unittest.TestCase):
    def test_every_skill_adapter_is_a_skill_entry_whose_scripts_exist(self):
        adapters = dragon._load_adapters(dragon.REVIEWED_ADAPTERS)
        inventory = dragon.full_inventory()
        rows = {k: v for k, v in adapters.items() if v.get("skill_program")}
        self.assertEqual(sorted(v["args"][0] for v in rows.values()), sorted(skill.RECIPES))
        for key, spec in rows.items():
            self.assertEqual(inventory[key]["kind"], "skill", key)
            self.assertTrue(skill.SCRIPT[spec["args"][0]].is_dir(), key)
            self.assertEqual(bool(spec.get("media")), spec["args"][0] in skill.NEEDS_MEDIA, key)


class SkillAdapterRuns(unittest.TestCase):
    def test_every_recipe_runs_and_passes_its_checks(self):
        with tempfile.TemporaryDirectory() as tmp:
            for recipe in skill.RECIPES:
                if (recipe in skill.NEEDS_MEDIA and not HAVE_FFMPEG) or missing_module(recipe):
                    continue  # its prerequisite is absent here; the Black Dragon checks job installs them
                with self.subTest(recipe=recipe):
                    art = Path(tmp) / f"{recipe}.txt"
                    done = run(recipe, art, "--task=" + TASK, "--media=")
                    report = json.loads(art.read_text(encoding="utf-8"))
                    self.assertEqual(done.returncode, 0, json.dumps(report, ensure_ascii=False)[:1500])
                    self.assertEqual(report["verdict"], "passed")
                    for row in report["outputs"]:
                        out = Path(row["path"])
                        self.assertTrue(out.is_relative_to(art.with_name(art.stem + ".work")))
                        self.assertEqual(skill.media.sha256(out), row["sha256"])

    def test_empty_task_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            art = Path(tmp) / "x.txt"
            self.assertEqual(run("reel-hooks", art, "--task=").returncode, 1)
            self.assertEqual(json.loads(art.read_text())["verdict"], "failed")

    def test_a_checker_that_misses_the_planted_flaw_earns_no_receipt(self):
        # A fake image_prompt_forge that writes prompts but never reports a problem.
        with tempfile.TemporaryDirectory() as tmp:
            fake = Path(tmp) / "fake"
            fake.mkdir()
            (fake / "image_prompt_forge.py").write_text(
                "import sys\nopen(sys.argv[sys.argv.index('--out') + 1], 'w').write("
                "''.join(f'## {p}\\n' for p in ['midjourney','flux','sdxl','chatgpt','ideogram','nanobanana']) + "
                "open(sys.argv[1], encoding='utf-8').read())\n", encoding="utf-8")
            saved = skill.SCRIPT["image-prompts"]
            skill.SCRIPT["image-prompts"] = fake
            try:
                art = Path(tmp) / "art.json"
                code = skill.main(["image-prompts", str(art), "--task=" + TASK])
            finally:
                skill.SCRIPT["image-prompts"] = saved
            self.assertEqual(code, 1)
            self.assertEqual(json.loads(art.read_text(encoding="utf-8"))["verdict"], "failed")


class SkillProgramsLeft(unittest.TestCase):
    def test_every_skill_program_is_connected_or_has_a_named_blocker(self):
        adapters = dragon._load_adapters(dragon.REVIEWED_ADAPTERS)
        inventory = dragon.full_inventory()
        left = sorted(k for k, v in inventory.items() if v["kind"] == "skill" and k not in adapters
                      and dragon._skill_has_cli(v.get("source")))
        self.assertEqual(left, sorted(dragon.SKILL_PROGRAM_BLOCKERS))


if __name__ == "__main__":
    unittest.main()
