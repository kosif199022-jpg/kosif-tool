"""End-to-end tests for tools/kosif.py through subprocess.

Deterministic tests run against a synthetic fixture repository built in a
temporary directory (``--root``); smoke tests run against the real catalog and
skip with a clear reason when it is being regenerated.
"""
from __future__ import annotations

import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _fixture import BASE, PM_A, PM_B, REAL_ROOT, build_repo, real_catalog, run_kosif  # noqa: E402

PLACEHOLDER = re.compile(r"\{[A-Za-z_]\w*\}")


class FixtureCliTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory(prefix="kosif-cli-")
        cls.root = build_repo(Path(cls._tmp.name) / "repo")
        cls.work = Path(cls._tmp.name) / "elsewhere"
        cls.work.mkdir()

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def kosif(self, *args, expect=0):
        proc = run_kosif(*args, root=self.root, cwd=self.work)
        self.assertEqual(proc.returncode, expect, f"args={args}\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}")
        return proc

    # -- help / errors ---------------------------------------------------
    def test_no_arguments_prints_bilingual_help(self):
        proc = run_kosif(root=self.root, cwd=self.work)
        self.assertEqual(proc.returncode, 2)
        self.assertIn("الاستخدام / Usage", proc.stdout)
        self.assertIn("scaffold", proc.stdout)
        proc = self.kosif("--help")
        self.assertIn("Commands", proc.stdout)

    def test_unknown_id_suggests_close_matches(self):
        proc = self.kosif("show", "pm-demo-aaaaab", expect=1)
        self.assertIn("unknown style id", proc.stderr)
        self.assertIn("Did you mean", proc.stderr)
        self.assertIn(PM_A, proc.stderr)
        self.assertEqual(proc.stdout, "")

    def test_unknown_category_is_a_clean_error(self):
        proc = self.kosif("list", "--category", "nope", expect=1)
        self.assertIn("unknown category", proc.stderr)
        self.assertIn("charts", proc.stderr)

    # -- list --------------------------------------------------------------
    def test_list_table_sorted_by_rank(self):
        out = self.kosif("list").stdout
        self.assertIn("id", out.splitlines()[0])
        self.assertLess(out.index(PM_A), out.index(PM_B))
        self.assertLess(out.index(PM_B), out.index(BASE))  # unranked last
        self.assertIn("3 ", out.splitlines()[-1])

    def test_list_json_and_filters(self):
        rows = json.loads(self.kosif("list", "--json").stdout)
        self.assertEqual([r["id"] for r in rows], [PM_A, PM_B, BASE])
        rows = json.loads(self.kosif("list", "--category", "charts", "--json").stdout)
        self.assertEqual({r["id"] for r in rows}, {PM_A, BASE})
        rows = json.loads(self.kosif("list", "--category", "بيانات", "--json").stdout)  # legacy label works too
        self.assertEqual({r["id"] for r in rows}, {PM_A, BASE})
        rows = json.loads(self.kosif("list", "--origin", "KOSIF", "--json").stdout)
        self.assertEqual([r["id"] for r in rows], [BASE])
        rows = json.loads(self.kosif("list", "--origin", "PromptsMotion", "--type", "Skill", "--json").stdout)
        self.assertEqual([r["id"] for r in rows], [PM_B])
        rows = json.loads(self.kosif("list", "--sort", "published", "--json").stdout)
        self.assertEqual([r["id"] for r in rows], [PM_B, PM_A, BASE])
        rows = json.loads(self.kosif("list", "--sort", "name", "--limit", "1", "--json").stdout)
        self.assertEqual([r["id"] for r in rows], [PM_A])

    # -- search ------------------------------------------------------------
    def test_search_is_case_insensitive_over_many_fields(self):
        out = self.kosif("search", "CHART", "showreel").stdout
        self.assertIn(PM_A, out)
        self.assertNotIn(PM_B, out)
        out = self.kosif("search", "@beta").stdout  # creator
        self.assertIn(PM_B, out)
        out = self.kosif("search", "رسوم بيانية").stdout  # Arabic category label
        self.assertIn(PM_A, out)
        self.assertIn(BASE, out)
        out = self.kosif("search", "أعمدة").stdout  # Arabic keyword
        self.assertIn(PM_A, out)
        rows = json.loads(self.kosif("search", "hand-drawn", "--json").stdout)
        self.assertEqual([r["id"] for r in rows], [PM_B])
        out = self.kosif("search", "zzz-nothing").stdout
        self.assertIn("no results", out)
        header = self.kosif("search", "demo").stdout.splitlines()[0]
        for col in ("id", "name", "categories", "type"):
            self.assertIn(col, header)

    # -- show --------------------------------------------------------------
    def test_show_prints_record_brief_and_playbooks(self):
        out = self.kosif("show", PM_A).stdout
        self.assertIn(f"styles/{PM_A}/STYLE.json", out)
        self.assertIn('"aspect_label": "16:9"', out)
        self.assertIn(f"BRIEF — styles/{PM_A}/BRIEF.md", out)
        self.assertIn("مقترح إبداعي تجريبي", out)
        self.assertIn("playbooks/charts.md", out)
        self.assertIn("playbooks/kinetic-type.md", out)
        out = self.kosif("show", PM_B).stdout
        self.assertIn("no BRIEF.md", out)

    # -- prompt ------------------------------------------------------------
    def test_prompt_fills_every_placeholder_ar_and_en(self):
        for lang in ("ar", "en"):
            out = self.kosif("prompt", PM_A, "--lang", lang).stdout
            self.assertIn(PM_A, out)
            self.assertIn(f"https://www.promptsmotion.com/{PM_A}", out)
            self.assertIn("https://github.com/kosif199022-jpg/kosif-tool", out)
            self.assertIsNone(PLACEHOLDER.search(out), f"unfilled placeholder in {lang} prompt:\n{out}")
            self.assertIn(f"styles/{PM_A}/BRIEF.md", out)  # brief_line present
            self.assertIn("playbooks/charts.md", out)
            self.assertIn("1920x1080", out)  # default aspect from the record (16:9)
            self.assertIn("12", out)  # default duration from the record
        out = self.kosif("prompt", PM_B, "--lang", "en").stdout
        self.assertNotIn("BRIEF.md", out)  # no brief → empty brief_line
        self.assertIn("1080x1920", out)
        self.assertIn("15 seconds", out)

    def test_prompt_options_and_out_file(self):
        out_file = self.work / "nested" / "request.txt"
        proc = self.kosif(
            "prompt", BASE, "--lang", "en", "--aspect", "1:1", "--fps", "25", "--duration", "9.5",
            "--source", "audio voice.mp3", "--stack", "canvas", "--brand", "navy + gold", "--audio", "music",
            "--content-lang", "both", "--notes", "fast opening", "--out", str(out_file),
        )
        self.assertIn(str(out_file), proc.stdout)
        text = out_file.read_text(encoding="utf-8")
        self.assertIn("1:1 at 1080x1080, 25 fps, 9.5 seconds", text)
        self.assertIn("attached audio file: voice.mp3", text)
        self.assertIn("HTML Canvas", text)
        self.assertIn("navy + gold", text)
        self.assertIn("-14 LUFS", text)
        self.assertIn("Arabic and English together", text)
        self.assertIn("fast opening", text)
        self.assertIsNone(PLACEHOLDER.search(text))
        text = self.kosif("prompt", BASE, "--aspect", "4:5", "--source", "none", "--audio", "silent").stdout
        self.assertIn("1080x1350", text)
        self.assertIn("بدون صوت", text)
        text = self.kosif("prompt", BASE, "--lang", "en", "--source", "a hand-written script on paper", "--audio", "voice over only").stdout
        self.assertIn("Source material: a hand-written script on paper", text)  # free text passes through
        self.assertIn("Audio and music: voice over only", text)

    # -- scaffold ----------------------------------------------------------
    def test_scaffold_creates_project_and_copies_starter(self):
        dest = self.work / "proj-a"
        proc = self.kosif("scaffold", PM_A, str(dest), "--starter", "html-canvas", "--source", "audio voice.mp3")
        self.assertIn(str(dest), proc.stdout)
        for name in ("STYLE.md", "PLAN.md", "TEST_REPORT.md", "words.json", "REQUEST.md"):
            self.assertTrue((dest / name).is_file(), name)
            text = (dest / name).read_text(encoding="utf-8")
            self.assertIsNone(PLACEHOLDER.search(text), f"unfilled placeholder in {name}")
        style = (dest / "STYLE.md").read_text(encoding="utf-8")
        self.assertIn(PM_A, style)
        self.assertIn("Demo chart showreel / عرض رسوم تجريبي", style)
        self.assertIn(f"https://www.promptsmotion.com/{PM_A}", style)
        self.assertIn("Charts / رسوم بيانية (charts)", style)
        self.assertIn("playbooks/charts.md, playbooks/kinetic-type.md", style)
        self.assertIn(f"styles/{PM_A}/BRIEF.md", style)
        plan = (dest / "PLAN.md").read_text(encoding="utf-8")
        self.assertIn("16:9 · 1920x1080 · 30 fps · 12 s (360", plan)
        report = (dest / "TEST_REPORT.md").read_text(encoding="utf-8")
        self.assertIn("-14 LUFS", report)
        self.assertIn("100 ms", report)
        words = json.loads((dest / "words.json").read_text(encoding="utf-8"))
        self.assertEqual(words["language"], "ar")
        request = (dest / "REQUEST.md").read_text(encoding="utf-8")
        self.assertIn(PM_A, request)
        self.assertIn("voice.mp3", request)
        self.assertTrue((dest / "html-canvas" / "index.html").is_file())
        self.assertFalse((dest / "html-canvas" / "node_modules").exists(), "node_modules must not be copied")

    def test_scaffold_refuses_non_empty_dir_without_force(self):
        dest = self.work / "proj-b"
        dest.mkdir()
        (dest / "keep.txt").write_text("mine\n", encoding="utf-8")
        proc = self.kosif("scaffold", PM_B, str(dest), expect=1)
        self.assertIn("not empty", proc.stderr)
        self.assertIn("--force", proc.stderr)
        self.assertFalse((dest / "STYLE.md").exists())
        self.kosif("scaffold", PM_B, str(dest), "--force")
        self.assertTrue((dest / "STYLE.md").is_file())
        self.assertEqual((dest / "keep.txt").read_text(encoding="utf-8"), "mine\n")

    def test_scaffold_missing_starter_is_reported_not_fatal(self):
        dest = self.work / "proj-c"
        proc = self.kosif("scaffold", BASE, str(dest), "--starter", "remotion")  # fixture has no remotion starter
        self.assertIn("starters/remotion/", proc.stdout)
        self.assertIn("does not exist", proc.stdout)
        self.assertIn("html-canvas", proc.stdout)  # lists what is available
        self.assertTrue((dest / "REQUEST.md").is_file())
        self.assertFalse((dest / "remotion").exists())

    # -- stats / validate --------------------------------------------------
    def test_stats_text_and_json(self):
        out = self.kosif("stats").stdout
        self.assertIn("total styles: 3", out)
        self.assertIn("charts", out)
        data = json.loads(self.kosif("stats", "--json").stdout)
        self.assertEqual(data["total"], 3)
        self.assertEqual(data["origin"], {"PromptsMotion": 2, "KOSIF original style": 1})
        self.assertEqual(data["type"], {"Prompt": 1, "Skill": 1, "Style": 1})
        self.assertEqual(data["category"]["charts"], 2)
        self.assertEqual(data["aspect_label"]["16:9"], 1)
        self.assertEqual(data["with_brief_files"], 1)
        self.assertEqual(data["playbooks_present"], 3)
        self.assertEqual(data["top_creators"][0][1], 1)

    def test_validate_passes_through_exit_code(self):
        proc = self.kosif("validate", "--quiet")
        self.assertIn("result: OK", proc.stdout)
        (self.root / "styles" / PM_B / "SKILL.md").rename(self.root / "styles" / PM_B / "SKILL.md.bak")
        try:
            proc = self.kosif("validate", expect=1)
            self.assertIn("SKILL.md missing", proc.stdout)
        finally:
            (self.root / "styles" / PM_B / "SKILL.md.bak").rename(self.root / "styles" / PM_B / "SKILL.md")


class RealRepoCliTest(unittest.TestCase):
    """Smoke tests on the real catalog; skipped while it is being regenerated."""

    @classmethod
    def setUpClass(cls):
        data, reason = real_catalog()
        if data is None:
            raise unittest.SkipTest(reason)
        cls.records = data[0]
        cls.first = cls.records[0]

    def kosif(self, *args):
        proc = run_kosif(*args, cwd=Path(tempfile.gettempdir()))  # no --root: resolved from __file__
        self.assertEqual(proc.returncode, 0, f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}")
        return proc.stdout

    def test_list_and_stats_agree_with_catalog(self):
        rows = json.loads(self.kosif("list", "--json"))
        self.assertEqual(len(rows), len(self.records))
        stats = json.loads(self.kosif("stats", "--json"))
        self.assertEqual(stats["total"], len(self.records))

    def test_search_show_prompt_on_first_record(self):
        rid = self.first["id"]
        self.assertIn(rid, self.kosif("search", rid))
        self.assertIn(f"styles/{rid}/STYLE.json", self.kosif("show", rid))
        for lang in ("ar", "en"):
            out = self.kosif("prompt", rid, "--lang", lang)
            self.assertIn(rid, out)
            self.assertIn(self.first["page"], out)
            self.assertIsNone(PLACEHOLDER.search(out), out)

    def test_scaffold_into_temp_dir(self):
        with tempfile.TemporaryDirectory(prefix="kosif-scaffold-") as tmp:
            dest = Path(tmp) / "project"
            self.kosif("scaffold", self.first["id"], str(dest))
            for name in ("STYLE.md", "PLAN.md", "TEST_REPORT.md", "words.json", "REQUEST.md"):
                self.assertTrue((dest / name).is_file(), name)
                self.assertIsNone(PLACEHOLDER.search((dest / name).read_text(encoding="utf-8")), name)


if __name__ == "__main__":
    unittest.main()
