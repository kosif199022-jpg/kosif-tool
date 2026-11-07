"""Tests for the Black Dragon 3D build studio (planning only, nothing rendered)."""
import importlib.util
import io
import json
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".claude/skills/kosif-black-dragon/scripts"


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


studio = _load("build_studio", "build_studio.py")
dragon = _load("black_dragon_native", "black_dragon.py")


class BuildStudioTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = studio.load()

    def test_library_shape(self):
        self.assertEqual(len(self.data["recipes"]), 21)
        self.assertEqual(len(self.data["principles"]), 18)
        self.assertEqual(sorted(r["order"] for r in self.data["recipes"]), list(range(1, 22)))
        for r in self.data["recipes"]:
            self.assertTrue(r["inputs"] and r["steps_ar"] and r["gates_ar"] and r["variants_ar"], r["id"])

    def test_arabic_match_routes_to_expected_recipe(self):
        cases = {
            "عايز فيديو دوّار لزجاجة عطر للإعلان": "product-turntable",
            "شعار متحرك انترو للقناة": "logo-reveal",
            "حوّل ملف المبيعات csv لرسم بياني": "data-chart",
            "قطع شطرنج للطباعة ثلاثية الأبعاد stl": "printable-minis",
            "مخطط قاعة الفرح وعدد الضيوف": "event-layout",
        }
        for task, expected in cases.items():
            self.assertEqual(studio.match(task, self.data)[0]["id"], expected, task)

    def test_brief_keeps_unfilled_inputs_as_questions(self):
        b = studio.brief("product-turntable", self.data, {"product": "زجاجة عطر"})
        self.assertEqual(b["status"], "PLANNING_BRIEF_NOT_A_RENDER")
        self.assertEqual(len(b["open_questions"]), 2)
        self.assertIn("P02", [p["id"] for p in b["principles"]])
        self.assertTrue(b["gates"][0].startswith("رندر"))

    def test_big_builds_are_staged(self):
        b = studio.brief("venue-pitch", self.data)
        self.assertEqual(b["stages"][0], "خطة/مسقط للموافقة")
        self.assertIn("P03", [p["id"] for p in b["principles"]])

    def test_unknown_fill_key_is_rejected(self):
        with self.assertRaises(ValueError):
            studio.brief("logo-reveal", self.data, {"colour": "#000"})

    def test_lint_flags_missing_self_check_and_spec(self):
        weak = studio.lint("Make a game level in Unreal", self.data)
        missing = [m["check"] for m in weak["missing"]]
        self.assertEqual(missing[0], "staged")
        self.assertIn("self_check", missing)
        strong = studio.lint("Build it as a script in Blender from @[logo.svg], free assets only. "
                             "Show me 3 options first, render 1920x1080 at 30 fps and check the frames.",
                             self.data)
        self.assertEqual(strong["coverage"], "7/7")

    def test_dragon_cli_delegates_build3d(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = dragon.main(["build3d", "match", "جزيرة لو بولي طائرة"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(buf.getvalue())[0]["id"], "floating-island")

    def test_no_verbatim_source_prompt_text(self):
        raw = (SCRIPTS.parent / "data/build3d_recipes.json").read_text(encoding="utf-8")
        for phrase in ("Look at the frames yourself", "Make a premium product video",
                       "Check the loop point so there's no jump"):
            self.assertNotIn(phrase, raw)


if __name__ == "__main__":
    unittest.main()
