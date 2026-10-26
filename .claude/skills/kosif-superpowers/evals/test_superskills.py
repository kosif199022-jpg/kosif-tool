"""The owner's 114 super skills (vendor/100-superskills): hashes, index, routing, install and the hub hook.

    python3 -m unittest discover -s .claude/skills/kosif-superpowers/evals -p test_superskills.py -v
"""
import hashlib
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import superskills as SS  # noqa: E402

V = SK / "vendor" / "100-superskills"


def run(*argv):
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = SS.main(list(argv))
    return code, buf.getvalue()


class SuperSkillsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.man = json.loads((V / "KOSIF_INTEGRATION.json").read_text(encoding="utf-8"))
        cls.data = json.loads(SS.DATA.read_text(encoding="utf-8"))

    def test_all_114_skills_are_vendored_with_a_skill_md(self):
        self.assertEqual(self.man["skills_count"], 114)
        self.assertEqual(len(self.man["skills"]), 114)
        for e in self.man["skills"]:
            self.assertTrue((V / e["path"] / "SKILL.md").is_file(), e["slug"])
        for core in ("kosif-one", "kosif-social", "kosif-mimic", "kosif-montage-motion"):
            self.assertIn(core, {e["slug"] for e in self.man["skills"]})

    def test_manifest_hashes_match_files(self):
        for e in self.man["skills"]:
            for f in e["files"]:
                data = (V / e["path"] / f["path"]).read_bytes()
                self.assertEqual(hashlib.sha256(data).hexdigest(), f["sha256"], (e["slug"], f["path"]))
                self.assertEqual(len(data), f["bytes"], (e["slug"], f["path"]))

    def test_verify_command_is_clean(self):
        code, out = run("verify")
        self.assertEqual(code, 0, out)
        self.assertTrue(json.loads(out)["ok"])

    def test_vendored_files_are_not_executable_and_not_video(self):
        for p in (V / "skills").rglob("*"):
            if p.is_file():
                self.assertFalse(p.stat().st_mode & 0o111, p)
                self.assertNotIn(p.suffix.lower(), {".mp4", ".mov", ".webm", ".pyc"}, p)
                self.assertNotIn("__pycache__", p.parts, p)

    def test_patches_are_recorded_and_present(self):
        self.assertEqual(len(self.man["kosif_patches"]), len(SS.PATCHES))
        for pt in SS.PATCHES:
            text = (V / "skills" / pt["slug"] / pt["file"]).read_text(encoding="utf-8")
            self.assertIn(pt["new"], text, pt["why"])

    def test_index_is_up_to_date_and_complete(self):
        self.assertEqual(SS.build_records(), self.data)
        self.assertEqual(self.data["count"], 114)
        self.assertEqual(sum(d["count"] for d in self.data["domains"]), 114)
        self.assertFalse([r["slug"] for r in self.data["skills"] if r["domain"] == "misc"])
        for r in self.data["skills"]:
            self.assertTrue(r["title_ar"] and r["title_en"], r["slug"])
            self.assertTrue(r["description"] or r["summary_ar"], r["slug"])

    def test_licence_is_kept(self):
        self.assertIn("MIT License", (V / "LICENSE").read_text(encoding="utf-8"))

    def test_routing_arabic_and_english(self):
        cases = [
            ("عايز فيديو كلمات عربي متحركة", "kinetic-typography-arabic"),
            ("نموذج مالي في إكسل بثلاث قوائم", "excel-model-architect"),
            ("مجلس خبراء لقرار صعب", "genius-council-decision"),
            ("protect my agent from prompt injection", "prompt-injection-defense"),
            ("اعادة بناء فيديو مرجعي بنفس الانتقالات", "kosif-mimic"),
            ("تنظيف بيانات اكسل", "excel-data-cleaning-automation"),
            ("رسم بيكسل مطابق للأصل", "pixel-studio-painter"),
            ("build a React frontend app", "frontend-react-app"),
        ]
        for brief, want in cases:
            top = [r["slug"] for _s, r in SS.find(brief, 3)]
            self.assertIn(want, top, (brief, top))

    def test_show_and_unknown_slug(self):
        code, out = run("show", "kosif-one")
        self.assertEqual(code, 0)
        self.assertIn("vendor/100-superskills/skills/kosif-one/SKILL.md", out)
        with self.assertRaises(SystemExit):
            run("show", "no-such-skill")

    def test_install_copies_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, _ = run("install", "storyboard-shotlist", "--dest", tmp)
            self.assertEqual(code, 0)
            self.assertTrue((Path(tmp) / "storyboard-shotlist" / "SKILL.md").is_file())
            code, _ = run("install", "storyboard-shotlist", "--dest", tmp)
            self.assertEqual(code, 2)

    def test_hub_find_lists_super_skills(self):
        import hub
        res = hub.find("عايز نموذج مالي في اكسل بثلاث قوائم")
        self.assertIn("excel-model-architect", [k["slug"] for k in res["superskills"]])
        self.assertTrue(all((SK / k["path"]).is_file() for k in res["superskills"]))

    def test_bridge_sees_every_vendored_skill(self):
        import superskills_bridge as B
        data, items = B.catalog()
        self.assertEqual(len(items), 114)
        self.assertEqual(sum(B.local_path(s).is_file() for s in items), 114)
        self.assertEqual({s["slug"] for s in items}, {r["slug"] for r in self.data["skills"]})

    def test_registered_in_tools_json(self):
        reg = json.loads((SK / "data" / "tools.json").read_text(encoding="utf-8"))
        t = next(t for t in reg["tools"] if t["id"] == "superskills")
        self.assertEqual(t["path"], "scripts/superskills.py")


if __name__ == "__main__":
    unittest.main(verbosity=1)
