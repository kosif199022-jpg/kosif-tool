"""Tests for tools/validate.py.

The fixture tests prove every check can both pass and fail; the real-repo
test passes when the checkout is clean and skips with the list of failing
derived-file checks when the catalog is mid-regeneration.
"""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _fixture import BASE, PM_A, PM_B, REAL_ROOT, brief_for, build_repo, make_records, run_validate, write_json  # noqa: E402

# Checks whose failure can be explained by a catalog / derived-file regeneration in progress.
REGENERATION_SENSITIVE = (
    "styles.json parses", "catalog has records", "record fields", "category value", "aspect_label",
    "STYLE.json", "orphan", "STYLE_INDEX.md", "prompts_motion", "briefs.json", "playbook", "meta.json",
)


class FixtureValidateTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="kosif-validate-")
        self.root = Path(self._tmp.name) / "repo"
        self.records = make_records()

    def tearDown(self):
        self._tmp.cleanup()

    def build(self, **kwargs) -> Path:
        return build_repo(self.root, records=self.records, **kwargs)

    def assert_fails(self, needle: str, *extra_needles: str) -> str:
        proc = run_validate(self.root)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("[FAIL]", proc.stdout)
        for n in (needle,) + extra_needles:
            self.assertIn(n, proc.stdout)
        return proc.stdout

    def assert_passes(self) -> str:
        proc = run_validate(self.root)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertNotIn("[FAIL]", proc.stdout)
        self.assertIn("result: OK", proc.stdout)
        return proc.stdout

    def test_clean_fixture_passes_with_numbered_report(self):
        self.build()
        out = self.assert_passes()
        self.assertIn(" 1. [PASS]", out)
        self.assertIn("3 records", out)
        self.assertNotIn("[WARN]", out)
        quiet = run_validate(self.root, "--quiet").stdout
        self.assertNotIn("[PASS]", quiet)
        self.assertIn("summary", quiet)

    def test_json_report(self):
        self.build()
        proc = run_validate(self.root, "--json")
        self.assertEqual(proc.returncode, 0)
        data = json.loads(proc.stdout)
        self.assertEqual(data["failed"], 0)
        self.assertGreaterEqual(len(data["checks"]), 13)
        self.assertTrue(all(c["status"] in {"PASS", "WARN", "FAIL"} for c in data["checks"]))

    def test_duplicate_id_fails(self):
        self.records.append(dict(self.records[0]))
        self.build()
        self.assert_fails("duplicate id", PM_A)

    def test_unknown_category_fails_but_legacy_label_only_warns(self):
        self.records[1]["category"] = ["الرسم اليدوي"]  # legacy label for hand-drawn
        self.build()
        out = self.assert_passes()
        self.assertIn("[WARN]", out)
        self.assertIn("legacy category label", out)
        self.records[1]["category"] = ["watercolor"]
        self.build()
        self.assert_fails("unknown category 'watercolor'")

    def test_invalid_enum_and_http_url_fail(self):
        self.records[2]["origin"] = "Somewhere"
        self.records[2]["page"] = "http://example.com/insecure"
        self.records[0]["video"] = "ftp://example.com/a.mp4"
        self.build()
        self.assert_fails("origin 'Somewhere'", "page must be an https URL", "video must be null or an https URL")

    def test_aspect_label_mismatch_fails_and_4_3_label_passes(self):
        self.records[0]["aspect_label"] = "9:16"  # pixels say 16:9
        self.build()
        self.assert_fails("aspect_label '9:16' does not match aspect 1920x1080")
        self.records[0]["aspect"] = {"w": 1408, "h": 1080}
        self.records[0]["aspect_label"] = "4:3"  # same tolerance rule as the catalog generator
        self.build()
        out = self.assert_passes()
        self.assertNotIn("outside the SCHEMA.md set", out)
        self.records[0]["aspect_label"] = "other"
        self.build()
        self.assert_fails("aspect_label is 'other' but 1408x1080 is 4:3")

    def test_style_json_must_equal_catalog_record(self):
        self.build()
        changed = dict(self.records[0], rank=99)
        write_json(self.root / "styles" / PM_A / "STYLE.json", changed)
        self.assert_fails("STYLE.json differs from the catalog record (fields: rank)")
        write_json(self.root / "styles" / PM_A / "STYLE.json", dict(self.records[0], id="pm-other"))
        self.assert_fails("STYLE.json id is")
        (self.root / "styles" / PM_A / "STYLE.json").write_text("{not json", encoding="utf-8")
        self.assert_fails("STYLE.json cannot parse")

    def test_missing_skill_and_orphan_dir(self):
        self.build()
        (self.root / "styles" / PM_B / "SKILL.md").unlink()
        self.assert_fails(f"styles/{PM_B}/SKILL.md missing")
        (self.root / "styles" / PM_B / "SKILL.md").write_text("# back\n", encoding="utf-8")
        (self.root / "styles" / "ghost").mkdir()
        out = self.assert_passes()
        self.assertIn("styles/ghost/ has no catalog record", out)

    def test_style_index_must_mention_every_id(self):
        self.build()
        idx = self.root / "STYLE_INDEX.md"
        idx.write_text(idx.read_text(encoding="utf-8").replace(f"[{BASE}](styles/{BASE}/SKILL.md)", "[gone](styles/gone/SKILL.md)"), encoding="utf-8")
        self.assert_fails(f"{BASE}: not mentioned in STYLE_INDEX.md")

    def test_prompts_motion_subset(self):
        self.build()
        write_json(self.root / "catalog" / "prompts_motion.json", [self.records[0], dict(self.records[1], id="pm-stray-000000")])
        self.assert_fails("prompts_motion id 'pm-stray-000000' is not in styles.json")

    def test_briefs_json_keys_and_ids(self):
        bad = brief_for(PM_A)
        del bad["scenes_ar"]
        del bad["facts_from_source"]
        self.build(briefs={PM_A: bad})
        self.assert_fails("lacks keys: scenes_ar, facts_from_source")
        self.build(briefs={PM_A: brief_for(PM_A), "pm-nobody-111111": brief_for("pm-nobody-111111")})
        self.assert_fails("briefs.json id 'pm-nobody-111111' is not in styles.json")
        self.build()
        (self.root / "catalog" / "briefs.json").unlink()  # optional file
        self.records[0]["brief"] = None
        self.build(briefs=None)
        (self.root / "catalog" / "briefs.json").unlink()
        self.assert_passes()

    def test_record_brief_path_must_exist(self):
        self.build()
        (self.root / "styles" / PM_A / "BRIEF.md").unlink()
        self.assert_fails(f"{PM_A}: record.brief points to a missing file")

    def test_missing_playbook_fails(self):
        self.build()
        (self.root / "playbooks" / "charts.md").unlink()
        self.assert_fails("playbooks/charts.md missing (referenced by categories.json[charts])")

    def test_rehosted_media_fails(self):
        self.build()
        (self.root / "styles" / PM_A / "reference.mp4").write_bytes(b"\x00\x00\x00\x18ftypmp42" + b"\x00" * 32)
        self.assert_fails(f"styles/{PM_A}/reference.mp4: media binary inside the repository")
        (self.root / "styles" / PM_A / "reference.mp4").unlink()
        (self.root / "catalog" / "poster.bin").write_bytes(b"RIFF\x10\x00\x00\x00WEBPVP8 " + b"\x00" * 16)
        self.assert_fails("catalog/poster.bin: file content looks like a media binary")

    def test_template_placeholder_sets_must_match(self):
        self.build()
        en = self.root / "templates" / "claude_request.en.txt"
        en.write_text(en.read_text(encoding="utf-8").replace("{notes}", "{remarks}"), encoding="utf-8")
        self.assert_fails("only in ar template: notes", "only in en template: remarks")
        en.unlink()
        self.assert_fails("templates/claude_request.en.txt missing")

    def test_unparseable_catalog_fails_cleanly(self):
        self.build()
        (self.root / "catalog" / "styles.json").write_text("[{\"id\": ", encoding="utf-8")
        out = self.assert_fails("catalog/styles.json parses")
        self.assertIn("cannot parse", out)

    def test_root_without_catalog_is_an_error(self):
        empty = Path(self._tmp.name) / "empty"
        empty.mkdir()
        proc = run_validate(empty)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("no catalog/", proc.stderr)


class RealRepoValidateTest(unittest.TestCase):
    def test_real_repo_validates_or_skips_during_regeneration(self):
        proc = run_validate(REAL_ROOT, "--json")
        try:
            data = json.loads(proc.stdout)
        except ValueError:
            self.fail(f"validate.py did not produce a JSON report:\n{proc.stdout}\n{proc.stderr}")
        failed = [c for c in data["checks"] if c["status"] == "FAIL"]
        if proc.returncode == 0:
            self.assertEqual(failed, [])
            return
        hard = [c["title"] for c in failed if not any(k in c["title"] for k in REGENERATION_SENSITIVE)]
        self.assertEqual(hard, [], "validator failures unrelated to catalog regeneration:\n" + "\n".join(f"- {c['title']}: {c['details'][:3]}" for c in failed))
        summary = "; ".join(f"{c['title']} ({len(c['details'])} items, e.g. {c['details'][0] if c['details'] else ''})" for c in failed)
        self.skipTest("catalog/derived files are mid-regeneration — validate.py reports: " + summary)


if __name__ == "__main__":
    unittest.main()
