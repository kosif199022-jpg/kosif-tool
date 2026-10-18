"""The «الدعاء» style kit: measured spec, example project, fonts and builder stay consistent."""
import importlib.util
import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DUA = ROOT / "styles" / "dua"
HEX = re.compile(r"^#[0-9A-F]{6}$")


class DuaSpec(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = json.loads((DUA / "dua.style.json").read_text(encoding="utf-8"))
        cls.example = json.loads((DUA / "kit" / "example" / "project.json").read_text(encoding="utf-8"))

    def test_structure_matches_cuts_and_transitions(self):
        s = self.spec
        self.assertEqual(s["structure"]["shots"], len(s["cuts_s"]) + 1)
        self.assertEqual(len(s["transitions"]["sequence_reference"]), len(s["cuts_s"]))
        self.assertEqual(len(s["dua_lines_reference"]), s["structure"]["shots"])
        self.assertEqual(s["cuts_s"], sorted(s["cuts_s"]))
        for kind in s["transitions"]["sequence_reference"]:
            self.assertIn(kind, s["transitions"]["kinds"])

    def test_text_colours_are_hex(self):
        for name, value in self.spec["palette"]["text"].items():
            self.assertRegex(value, HEX, name)
        self.assertEqual(self.spec["layers"]["subtitle_gold"]["fill"], self.spec["palette"]["text"]["gold"])

    def test_layer_boxes_inside_frame(self):
        w, h = self.spec["output"]["w"], self.spec["output"]["h"]
        for name in ("title", "date", "subtitle_gold"):
            x0, y0, x1, y1 = self.spec["layers"][name]["bbox_px"]
            self.assertTrue(0 <= x0 < x1 <= w and 0 <= y0 < y1 <= h, name)

    def test_audio_rule_is_copy(self):
        self.assertIn("-c:a copy", self.spec["output"]["audio"])

    def test_example_project_follows_the_reference_timing(self):
        lines = self.example["lines"]
        self.assertEqual(len(lines), self.spec["structure"]["shots"])
        for a, b in zip(lines, lines[1:]):
            self.assertAlmostEqual(a["end"], b["start"], places=3)
        onsets = [l["start"] for l in lines[1:]]
        for onset, cut in zip(onsets, self.spec["cuts_s"]):
            self.assertLessEqual(abs(onset - cut), 0.2)

    def test_fonts_ship_with_licences(self):
        fonts = DUA / "kit" / "fonts"
        for ttf, lic in (("Marhey-VF.ttf", "OFL-Marhey.txt"), ("ScheherazadeNew-Bold.ttf", "OFL-ScheherazadeNew.txt")):
            self.assertTrue((fonts / ttf).read_bytes()[:4] in (b"\x00\x01\x00\x00", b"true", b"OTTO"), ttf)
            self.assertIn("SIL OPEN FONT LICENSE", (fonts / lic).read_text(encoding="utf-8").upper())

    def test_catalog_record_and_skill_power(self):
        recs = {r["id"]: r for r in json.loads((ROOT / "catalog" / "styles.json").read_text(encoding="utf-8"))}
        self.assertIn("dua", recs)
        self.assertIn("Ready-made kit", (DUA / "SKILL.md").read_text(encoding="utf-8"))
        powers = json.loads((ROOT / ".claude/skills/kosif-superpowers/data/powers/photo-video-footage.json").read_text(encoding="utf-8"))
        ids = {p["id"] for p in powers if "dua" in p.get("styles", [])}
        self.assertTrue({"FOOT-D01", "FOOT-D02", "FOOT-D03"} <= ids)
        sheet = ROOT / ".claude/skills/kosif-superpowers/proofs/dua-style/sheet.jpg"
        self.assertLessEqual(sheet.stat().st_size, 400_000)

    @unittest.skipUnless(shutil.which("node"), "node not installed")
    def test_layers_script_parses(self):
        subprocess.run(["node", "--check", str(DUA / "kit" / "layers.cjs")], check=True)

    @unittest.skipUnless(importlib.util.find_spec("numpy") and importlib.util.find_spec("PIL"), "numpy/Pillow not installed")
    def test_builder_loads_project(self):
        spec = importlib.util.spec_from_file_location("build_dua", DUA / "kit" / "build_dua.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "project.json"
            p.write_text(json.dumps(self.example, ensure_ascii=False), encoding="utf-8")
            proj = mod.load_project(p)
        self.assertEqual(proj["fps"], 30)
        self.assertEqual(len(proj["lines"]), 8)
        self.assertEqual(proj["lines"][0]["start"], 0.0)


if __name__ == "__main__":
    unittest.main()
