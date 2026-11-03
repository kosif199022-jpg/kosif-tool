"""Black Dragon structural card validation: planted flaws are caught, and it is never execution."""
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".claude/skills/kosif-superpowers/scripts"
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location("black_dragon", SCRIPTS / "black_dragon.py")
dragon = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dragon)
import _black_dragon_validate as validate  # noqa: E402


def _w(path: Path, text) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text if isinstance(text, str) else json.dumps(text, ensure_ascii=False), encoding="utf-8")


def _power(pid, family, proof, **extra):
    row = {"id": pid, "family": family, "domain": "motion", "name_ar": "قدرة", "name_en": "A power",
           "status": "proven", "what": "does a thing", "how": "like this", "params": "", "install": "",
           "requires": ["ffmpeg"], "license": "", "proof": proof, "proof_scope": "repo",
           "styles": [], "tags": ["t"], "when": "always"}
    row.update(extra)
    return row


class MiniCatalog:
    """A small but complete catalog of every kind, valid unless a test plants a flaw."""

    def __init__(self, base: Path):
        self.repo = base / "kosif-tool"
        self.skill = self.repo / ".claude" / "skills" / "kosif-superpowers"
        r, s = self.repo, self.skill
        _w(r / "playbooks" / "motion.md", "# Motion\n\nSee [the other](diagrams.md).\n")
        _w(r / "playbooks" / "diagrams.md", "# Diagrams\n\nText.\n")
        _w(r / "catalog" / "categories.json", [{"key": "motion", "en": "Motion", "ar": "موشن",
                                                "playbook": "playbooks/motion.md"}])
        self.style = {"id": "calm", "name": "Calm", "name_ar": "", "origin": "KOSIF original style",
                      "type": "Style", "category": ["motion"], "page": "https://example.org/calm",
                      "video": None, "poster": None, "creator_url": None, "tech": [],
                      "skill": "styles/calm/SKILL.md", "playbooks": ["playbooks/motion.md"]}
        _w(r / "catalog" / "styles.json", [self.style])
        _w(r / "styles" / "calm" / "SKILL.md", "---\nname: calm\ndescription: calm style\n---\n# Calm\n")
        _w(r / "styles" / "calm" / "STYLE.json", self.style)
        _w(r / "tools" / "render.py", "print('render')\n")
        _w(r / "tests" / "test_render.py", "import unittest\n")
        _w(s / "SKILL.md", "---\nname: kosif-superpowers\ndescription: master skill\n---\n"
                           "# Master\n\nRead [the protocol](PROTOCOL.md).\n")
        _w(s / "PROTOCOL.md", "# Protocol\n\n| appendix | trigger |\n|---|---|\n"
                              "| [A1 thinking](references/protocol/A1-think.md) | always |\n")
        _w(s / "references" / "protocol" / "A1-think.md", "# A1\n\nBack to [core](../../PROTOCOL.md).\n")
        _w(s / "data" / "requirements.json", {"_note": "x", "ffmpeg": {}, "python3": {}})
        self.powers = [_power("MOT-01", "motion", ["kosif-tool/playbooks/motion.md:2"]),
                       _power("MOT-02", "motion", ["https://example.org/x", "kosif-one/elsewhere.md"],
                              status="documented", proof_scope="sibling")]
        _w(s / "data" / "powers" / "motion.json", self.powers)
        self.superpower = {"id": "SP-0001", "domain": "motion", "family": "motion", "name_ar": "خارقة",
                           "name_en": "Fused", "best": "proven", "size": 2,
                           "status_mix": {"proven": 1, "documented": 1}, "families": {"motion": 2},
                           "requires": ["ffmpeg"], "proof": [], "twins": [["MOT-01", "MOT-02"]], "links": [],
                           "pipeline": [{"id": "MOT-01", "status": "proven"},
                                        {"id": "MOT-02", "status": "documented"}]}
        _w(s / "data" / "superpowers.json", {"schema": "x", "items": [self.superpower]})
        self.tool = {"id": "render", "path": "tools/render.py", "root": "repo", "kind": "cli",
                     "area": "make", "title_en": "Render", "title_ar": "رندر", "summary_en": "renders",
                     "safety": "read-only", "commands": [{"name": "run"}], "requires": {},
                     "tests": ["tests/test_render.py"], "docs": ["playbooks/motion.md"],
                     "families": ["motion"], "power_id": "MOT-01"}
        _w(s / "data" / "tools.json", {"tools": [self.tool]})
        _w(r / ".claude" / "skills" / "editor" / "SKILL.md",
           "---\nname: editor\ndescription: >-\n  edits video\n---\n# Editor\n\n[guide](guide.md)\n")
        _w(r / ".claude" / "skills" / "editor" / "guide.md", "# Guide\n")

    def save_powers(self):
        _w(self.skill / "data" / "powers" / "motion.json", self.powers)

    def inventory(self):
        return dragon.full_inventory(self.skill, self.repo)

    def results(self):
        inv = self.inventory()
        return {r["entry"]: r for r in validate.validate_catalog(inv, self.skill, self.repo)}, inv


class CardValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.cat = MiniCatalog(Path(self.temp.name))

    def problems(self, key):
        rows, _ = self.cat.results()
        return rows[key]["status"], rows[key]["problems"]

    def test_clean_catalog_validates_every_kind_with_receipts(self):
        rows, inv = self.cat.results()
        self.assertEqual(set(rows), set(inv))
        self.assertEqual({r["kind"] for r in rows.values()},
                         {"skill", "power", "tool", "superpower", "style", "playbook", "protocol"})
        bad = {k: r["problems"] for k, r in rows.items() if r["status"] != "validated"}
        self.assertEqual(bad, {})
        for row in rows.values():
            self.assertRegex(row["source_sha256"], r"^[0-9a-f]{64}$")
            self.assertTrue(row["checks"])
        # sibling-repo and URL proofs are counted, never treated as verified files
        self.assertEqual(rows["power:MOT-02"]["external_refs_not_checkable"], {"sibling_repo": 1, "url": 1})

    def test_missing_evidence_file_is_invalid(self):
        self.cat.powers[0]["proof"] = ["kosif-tool/playbooks/gone.md"]
        self.cat.save_powers()
        status, problems = self.problems("power:MOT-01")
        self.assertEqual(status, "invalid")
        self.assertIn("proof_path_missing: kosif-tool/playbooks/gone.md", problems)

    def test_proof_line_beyond_end_of_file_is_invalid(self):
        self.cat.powers[0]["proof"] = ["kosif-tool/playbooks/motion.md:400"]
        self.cat.save_powers()
        status, problems = self.problems("power:MOT-01")
        self.assertEqual(status, "invalid")
        self.assertTrue(any(p.startswith("proof_line_out_of_range") for p in problems))

    def test_power_fields_requirements_and_family(self):
        self.cat.powers[0].update(what="", requires=["warp-drive"], family="other", status="magic")
        del self.cat.powers[0]["tags"]
        self.cat.save_powers()
        _, problems = self.problems("power:MOT-01")
        cats = {p.split(":", 1)[0] for p in problems}
        self.assertTrue({"empty_field", "missing_field", "unknown_requirement",
                         "family_mismatch", "bad_status"} <= cats, problems)

    def test_superpower_pointing_at_nonexistent_power_is_invalid(self):
        self.cat.superpower["pipeline"].append({"id": "GHOST-99", "status": "proven"})
        self.cat.superpower["size"] = 3
        _w(self.cat.skill / "data" / "superpowers.json", {"items": [self.cat.superpower]})
        status, problems = self.problems("superpower:SP-0001")
        self.assertEqual(status, "invalid")
        self.assertIn("component_missing: power GHOST-99 does not exist", problems)

    def test_superpower_drift_from_its_components_is_invalid(self):
        self.cat.superpower["pipeline"][1]["status"] = "proven"
        self.cat.superpower["links"] = [{"id": "SP-9999"}]
        _w(self.cat.skill / "data" / "superpowers.json", {"items": [self.cat.superpower]})
        _, problems = self.problems("superpower:SP-0001")
        cats = {p.split(":", 1)[0] for p in problems}
        self.assertTrue({"component_status_drift", "link_missing"} <= cats, problems)

    def test_skill_without_frontmatter_is_invalid(self):
        _w(self.cat.repo / ".claude" / "skills" / "editor" / "SKILL.md", "# Editor\n\nNo frontmatter.\n")
        status, problems = self.problems("skill:editor")
        self.assertEqual(status, "invalid")
        self.assertIn("no_frontmatter: SKILL.md has no YAML frontmatter block", problems)

    def test_skill_missing_description_and_broken_link(self):
        _w(self.cat.repo / ".claude" / "skills" / "editor" / "SKILL.md",
           "---\nname: editor\n---\n# Editor\n\n[gone](references/gone.md) `[code](ignored.md)`\n")
        _, problems = self.problems("skill:editor")
        self.assertIn("frontmatter_missing: description", problems)
        self.assertIn("broken_link: references/gone.md", problems)
        self.assertFalse(any("ignored.md" in p for p in problems))

    def test_tool_missing_path_and_tests(self):
        (self.cat.repo / "tools" / "render.py").unlink()
        (self.cat.repo / "tests" / "test_render.py").unlink()
        status, problems = self.problems("tool:render")
        self.assertEqual(status, "invalid")
        self.assertIn("tool_path_missing: tools/render.py", problems)
        self.assertIn("test_missing: tests/test_render.py", problems)

    def test_style_json_drift_and_missing_playbook(self):
        changed = dict(self.cat.style, name="Changed", playbooks=["playbooks/none.md"])
        _w(self.cat.repo / "styles" / "calm" / "STYLE.json", dict(changed, playbooks=self.cat.style["playbooks"]))
        _w(self.cat.repo / "catalog" / "styles.json", [changed])
        _, problems = self.problems("style:calm")
        cats = {p.split(":", 1)[0] for p in problems}
        self.assertTrue({"style_json_drift", "playbook_missing"} <= cats, problems)

    def test_broken_style_json_is_invalid(self):
        _w(self.cat.repo / "styles" / "calm" / "STYLE.json", "{not json")
        _, problems = self.problems("style:calm")
        self.assertTrue(any(p.startswith("style_json_invalid") for p in problems))

    def test_playbook_without_heading_and_protocol_missing_appendix(self):
        _w(self.cat.repo / "playbooks" / "diagrams.md", "just text\n")
        (self.cat.skill / "references" / "protocol" / "A1-think.md").rename(
            self.cat.skill / "references" / "protocol" / "A2-moved.md")
        rows, _ = self.cat.results()
        self.assertIn("no_heading: no markdown heading", rows["playbook:diagrams"]["problems"])
        self.assertIn("appendix_missing: references/protocol/A1-think.md", rows["protocol:PROTOCOL"]["problems"])

    def test_receipts_are_written_and_tampering_is_detected(self):
        inv = self.cat.inventory()
        job = Path(self.temp.name) / "job"
        job.mkdir()
        summary = validate.write(job, validate.validate_catalog(inv, self.cat.skill, self.cat.repo), inv)
        self.assertEqual(summary["validated"] + summary["invalid"], len(inv))
        self.assertFalse(summary["counts_as_executed"])
        ok = validate.verify_job(job, inv, self.cat.skill, self.cat.repo)
        self.assertTrue(ok["integrity_passed"], ok)
        with self.assertRaises(ValueError):
            validate.write(job, [], inv)
        # a source edited after validation is caught on re-hash
        _w(self.cat.repo / "playbooks" / "diagrams.md", "# Diagrams\n\nEdited later.\n")
        changed = validate.verify_job(job, inv, self.cat.skill, self.cat.repo)
        self.assertFalse(changed["integrity_passed"])
        self.assertEqual(changed["sources_changed"], 1)
        # a forged receipt line is caught by the file hash
        path = job / validate.VALIDATION_FILE
        path.write_text(path.read_text(encoding="utf-8").replace('"checks"', '"checks_x"', 1), encoding="utf-8")
        self.assertIn("validation.jsonl SHA-256 differs from the summary",
                      validate.verify_job(job, inv, self.cat.skill, self.cat.repo)["errors"])


class ValidationIsNotExecutionTests(unittest.TestCase):
    """Wired into run(): a separate tier that never changes executed or full_coverage."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.cat = MiniCatalog(Path(self.temp.name))
        self.old_repo = dragon.REPO
        dragon.REPO = self.cat.repo
        self.addCleanup(setattr, dragon, "REPO", self.old_repo)
        self.inv = self.cat.inventory()

    def go(self, name, validate_cards, **kw):
        return dragon.run("validate every card", self.cat.repo / "out" / name, {}, workers=2,
                          allow_execution=False, timeout=5, entries=self.inv,
                          validate_cards=validate_cards, catalog_roots=(self.cat.skill, self.cat.repo), **kw)

    def test_all_validated_but_nothing_executed_and_no_full_coverage(self):
        plain = self.go("plain", False)
        checked = self.go("checked", True)
        self.assertEqual(checked["validated"], len(self.inv))
        self.assertEqual(checked["validation_invalid"], 0)
        self.assertEqual(checked["executed"], plain["executed"])
        self.assertEqual(checked["executed"], 0)
        self.assertEqual(checked["blocked"], plain["blocked"])
        self.assertFalse(checked["full_coverage"])
        self.assertFalse(checked["validation"]["counts_as_executed"])
        job = self.cat.repo / "out" / "checked"
        ledger = json.loads((job / "all_skills_ledger.json").read_text(encoding="utf-8"))
        self.assertNotIn("validated", {x["status"] for x in ledger["items"].values()})
        md = (job / "black_dragon_report.md").read_text(encoding="utf-8")
        self.assertIn(f"validated: **{len(self.inv)}/{len(self.inv)}** (invalid: 0)", md)
        self.assertIn("NOT execution", md)
        self.assertEqual(len((job / "validation.jsonl").read_text(encoding="utf-8").splitlines()), len(self.inv))
        self.assertNotIn("validated", plain)

    def test_invalid_cards_are_counted_without_failing_the_run(self):
        (self.cat.repo / "tools" / "render.py").unlink()
        report = self.go("broken", True)
        self.assertEqual(report["validation_invalid"], 1)
        self.assertEqual(report["validated"] + report["validation_invalid"], report["scheduled"])
        self.assertEqual(report["failed"], 0)


class RealCatalogValidationTests(unittest.TestCase):
    def test_every_real_card_gets_exactly_one_receipt(self):
        inv = dragon.full_inventory()
        rows = validate.validate_catalog(inv, dragon.audit.SKILL, dragon.REPO)
        summary = validate.summarize(rows, inv)
        self.assertTrue(summary["covered_all"])
        self.assertEqual(summary["validated"] + summary["invalid"], summary["total"])
        self.assertEqual(summary["total"], len(inv))
        self.assertGreater(summary["validated"], 0.9 * len(inv))
        for row in rows:
            self.assertEqual(row["status"] == "invalid", bool(row["problems"]), row["entry"])


if __name__ == "__main__":
    unittest.main()
