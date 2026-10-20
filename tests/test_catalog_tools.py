"""Tests for the catalog maintenance tools: sync_catalog.py, import_briefs.py,
check_originality.py and build.py.

Each tool resolves the repository from its own location, so the script is
copied into a synthetic fixture repository (tests/_fixture.py) and run there;
the real catalog is never touched.
"""
from __future__ import annotations

import html
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _fixture import BASE, PM_A, PM_B, TOOLS, _env, build_repo, write_json  # noqa: E402


def run(script: Path, *args, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(script), *map(str, args)], cwd=str(cwd) if cwd else None,
                          capture_output=True, text=True, encoding="utf-8", env=_env(), timeout=120)


def snapshot(root: Path) -> dict[str, bytes]:
    return {str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file() and "tools" not in p.parts}


class FixtureRepo(unittest.TestCase):
    tools: tuple[str, ...] = ()

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="kosif-catalog-tools-")
        self.tmp = Path(self._tmp.name)
        self.root = build_repo(self.tmp / "repo")
        (self.root / "tools").mkdir()
        for name in self.tools:
            shutil.copyfile(TOOLS / name, self.root / "tools" / name)

    def tearDown(self):
        self._tmp.cleanup()

    def records(self) -> dict[str, dict]:
        return {r["id"]: r for r in json.loads((self.root / "catalog" / "styles.json").read_text(encoding="utf-8"))}


class SyncCatalogTest(FixtureRepo):
    tools = ("sync_catalog.py",)

    def write_index(self, slugs: list[str]) -> None:
        arts = "".join(
            f'<article><a href="/{s}" aria-label="Open {html.escape(s)}"><video poster="/p/{s}.webp" '
            f'style="aspect-ratio:16 / 9"></video><span>@<!-- -->maker</span>'
            f'<span class="leading-[13px]">Prompt</span></a></article>' for s in slugs)
        p = self.root / ".cache" / "promptsmotion" / "home.html"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(f"<html><body>{arts}</body></html>", encoding="utf-8")

    def sync(self) -> subprocess.CompletedProcess:
        proc = run(self.root / "tools" / "sync_catalog.py", "--offline")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        return proc

    def test_keeps_kosif_styles_outside_base_and_flags_unlisted_entries(self):
        # PM_A stays on the index, PM_B left it; BASE ("kosif-demo") is a hand-added
        # KOSIF style that is not in the built-in BASE list (like 'dua').
        self.write_index([PM_A[3:]] + [f"new-{i:06x}" for i in range(55)])
        proc = self.sync()
        recs = self.records()
        self.assertIn(BASE, recs, "a KOSIF style outside BASE was dropped")
        self.assertEqual(recs[BASE]["name"], "استايل تجريبي")
        self.assertTrue(recs[BASE].get("listed", True))
        self.assertIn(PM_B, recs)
        self.assertIs(recs[PM_B]["listed"], False)
        self.assertIs(recs[PM_A]["listed"], True)
        self.assertEqual(recs[PM_A]["summary_en"], "Animated bar showreel", "brief fields must be carried over")
        self.assertIn("1 unlisted, 1 other styles kept", proc.stderr)
        self.assertTrue((self.root / "styles" / BASE / "STYLE.json").is_file())

    def test_no_op_sync_rewrites_identical_bytes(self):
        self.write_index([PM_A[3:], PM_B[3:]] + [f"new-{i:06x}" for i in range(50)])
        self.sync()
        first = snapshot(self.root)
        proc = self.sync()
        self.assertIn("(0 new, 0 changed, 0 unlisted, 1 other styles kept)", proc.stderr)
        self.assertEqual(first, snapshot(self.root))

    def test_retired_ids_are_the_only_ones_removed(self):
        script = self.root / "tools" / "sync_catalog.py"
        text = script.read_text(encoding="utf-8")
        self.assertIn("RETIRED: set[str] = set()", text)
        retired = {BASE, PM_A, "minimal"}  # a hand-added style, an entry still on the index, a BASE style
        script.write_text(text.replace("RETIRED: set[str] = set()", f"RETIRED: set[str] = {sorted(retired)!r}"), encoding="utf-8")
        self.write_index([PM_A[3:]] + [f"new-{i:06x}" for i in range(55)])
        self.sync()
        recs = self.records()
        for ident in retired:
            self.assertNotIn(ident, recs)
        self.assertIn(PM_B, recs)
        self.assertIn("brutalist", recs)


def good_brief(style_id: str, **overrides) -> dict:
    b = {
        "id": style_id, "title_ar": "عنوان", "summary_ar": "ملخص", "summary_en": "A short original summary.",
        "concept_ar": "فكرة", "concept_en": "An original concept.", "scenes_en": ["one", "two", "three"],
        "scenes_ar": ["١", "٢", "٣"], "motion_rules_en": ["ease out"], "motion_rules_ar": ["تباطؤ"], "stack": ["SVG"],
        "duration_s": 12, "aspect": "9:16", "difficulty": 3, "keywords": ["a", "b", "c", "d", "e", "f"],
        "facts_from_source": [], "assumptions_en": "None.",
    }
    b.update(overrides)
    return b


class ImportBriefsTest(FixtureRepo):
    tools = ("import_briefs.py", "aspects.py")

    def batch(self, name: str, content) -> Path:
        d = self.tmp / "briefs"
        d.mkdir(exist_ok=True)
        p = d / name
        p.write_text(content if isinstance(content, str) else json.dumps(content, ensure_ascii=False), encoding="utf-8")
        return d

    def importer(self, *args) -> subprocess.CompletedProcess:
        return run(self.root / "tools" / "import_briefs.py", *args)

    def test_strict_with_invalid_json_writes_nothing(self):
        self.batch("batch1.json", {"briefs": [good_brief(PM_B)]})
        d = self.batch("zz.json", "{bad")
        before = snapshot(self.root)
        proc = self.importer(d, "--strict")
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("zz.json: invalid JSON", proc.stderr)
        self.assertIn("nothing was written", proc.stderr)
        self.assertNotIn("Traceback", proc.stderr)
        self.assertEqual(before, snapshot(self.root))

    def test_without_strict_a_bad_file_is_skipped_and_the_rest_imported(self):
        self.batch("batch1.json", {"briefs": [good_brief(PM_B)]})
        d = self.batch("zz.json", "{bad")
        proc = self.importer(d)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("imported 1 briefs", proc.stdout)
        self.assertTrue((self.root / "styles" / PM_B / "BRIEF.md").is_file())
        self.assertEqual(self.records()[PM_B]["summary_en"], "A short original summary.")
        self.assertIn(PM_B, json.loads((self.root / "catalog" / "briefs.json").read_text(encoding="utf-8")))

    def test_top_level_list_gives_a_clear_message(self):
        d = self.batch("a.json", '[{"id": "x"}]')
        proc = self.importer(d)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn('a.json: expected an object {"briefs": [...]}, got a JSON list', proc.stderr)
        self.assertNotIn("Traceback", proc.stderr)
        strict = self.importer(d, "--strict")
        self.assertEqual(strict.returncode, 1)
        self.assertNotIn("Traceback", strict.stderr)

    def test_non_brief_items_and_bad_ids_do_not_crash(self):
        d = self.batch("b.json", {"briefs": ["text", 3, {"id": ["list"]}]})
        proc = self.importer(d)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("not a JSON object", proc.stderr)
        self.assertNotIn("Traceback", proc.stderr)

    def test_value_issues_import_anyway_but_type_issues_skip(self):
        d = self.batch("batch1.json", {"briefs": [good_brief(PM_B, difficulty=9), good_brief(BASE, concept_en=None)]})
        proc = self.importer(d)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn(f"issues in {PM_B} (imported anyway): difficulty must be an integer 1-5", proc.stderr)
        self.assertIn(f"issues in {BASE} (skipped): concept_en not a string", proc.stderr)
        self.assertTrue((self.root / "styles" / PM_B / "BRIEF.md").is_file())
        self.assertFalse((self.root / "styles" / BASE / "BRIEF.md").exists())
        strict = self.importer(d, "--strict")
        self.assertEqual(strict.returncode, 1)
        self.assertIn(f"issues in {PM_B} (skipped)", strict.stderr)


class CheckOriginalityTest(unittest.TestCase):
    SCRIPT = TOOLS / "check_originality.py"

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="kosif-originality-")
        self.tmp = Path(self._tmp.name)
        self.briefs, self.texts = self.tmp / "briefs", self.tmp / "texts"
        self.briefs.mkdir()
        self.texts.mkdir()
        (self.texts / "demo-aaaaaa.txt").write_text(
            "TITLE: Demo\nthe camera glides over a neon city while giant letters rise from the street\n", encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def check(self, summary: str, *extra) -> subprocess.CompletedProcess:
        write_json(self.briefs / "batch1.json", {"briefs": [{"id": "pm-demo-aaaaaa", "summary_en": summary}]})
        return run(self.SCRIPT, "--briefs", self.briefs, "--texts", self.texts, *extra)

    def test_copied_run_is_flagged_and_original_text_passes(self):
        copied = self.check("Giant letters rise from the street in a neon city.")
        self.assertEqual(copied.returncode, 1, copied.stdout + copied.stderr)
        self.assertIn("checked 1 briefs, flagged 1", copied.stdout)
        clean = self.check("Bold type climbs out of the pavement at night.")
        self.assertEqual(clean.returncode, 0, clean.stdout + clean.stderr)

    def test_missing_folders_fail_instead_of_passing(self):
        for args in (("--briefs", self.tmp / "nope", "--texts", self.texts),
                     ("--briefs", self.briefs, "--texts", self.tmp / "typo-texts")):
            proc = run(self.SCRIPT, *args)
            self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
            self.assertIn("is not a folder", proc.stderr)
        empty = run(self.SCRIPT, "--briefs", self.texts, "--texts", self.texts)
        self.assertEqual(empty.returncode, 2)
        self.assertIn("has no *.json files", empty.stderr)

    def test_invalid_json_is_an_input_error_without_traceback(self):
        (self.briefs / "zz.json").write_text("{oops", encoding="utf-8")
        proc = self.check("Bold type climbs out of the pavement at night.")
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        self.assertIn("zz.json: invalid JSON", proc.stderr)
        self.assertNotIn("Traceback", proc.stderr)

    def test_briefs_without_source_text_are_reported(self):
        write_json(self.briefs / "batch1.json", {"briefs": [{"id": "pm-other-bbbbbb", "summary_en": "x"}]})
        proc = run(self.SCRIPT, "--briefs", self.briefs, "--texts", self.texts)
        self.assertEqual(proc.returncode, 0)
        self.assertIn("checked 0 briefs", proc.stdout)
        self.assertIn("1 pm- brief(s) have no <slug>.txt", proc.stderr)


class BuildHelpTest(FixtureRepo):
    tools = ("build.py",)

    def test_help_names_every_file_a_build_writes(self):
        # Force every output to be rewritten: drop the derived files and re-serialise the input.
        for rel in ("STYLE_INDEX.md", "catalog/prompts_motion.json", "catalog/meta.json", "catalog/playbooks.json"):
            (self.root / rel).unlink()
        for p in (self.root / "styles").glob("*/STYLE.json"):
            p.unlink()
        recs = json.loads((self.root / "catalog" / "styles.json").read_text(encoding="utf-8"))
        (self.root / "catalog" / "styles.json").write_text(json.dumps(recs, ensure_ascii=False), encoding="utf-8")
        (self.root / "README.md").write_text("# Demo\n<!-- stats:start -->\nold\n<!-- stats:end -->\n", encoding="utf-8")
        before = snapshot(self.root)
        script = self.root / "tools" / "build.py"
        proc = run(script)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        after = snapshot(self.root)
        written = {p for p, data in after.items() if before.get(p) != data}
        help_text = " ".join(run(script, "--help").stdout.split())
        for rel in sorted(written):
            parts = Path(rel).parts
            name = f"styles/<id>/{parts[-1]}" if parts[0] == "styles" else rel
            self.assertIn(name, help_text, f"build.py writes {rel} but --help does not say so")
        self.assertEqual(run(script, "--check").returncode, 0)


if __name__ == "__main__":
    unittest.main()
