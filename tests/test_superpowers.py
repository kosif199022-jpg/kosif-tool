"""Integrity tests for the kosif-superpowers skill (.claude/skills/kosif-superpowers).

The skill is Claude's capability catalog: power chapters, machine-readable
power data, reference files, a stdlib search script and rendered proofs.
These tests keep the data well-formed, the links alive and the repository
free of rendered video.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / ".claude" / "skills" / "kosif-superpowers"
POWERS = SKILL / "data" / "powers"
SCRIPT = SKILL / "scripts" / "powers.py"
STATUSES = {"proven", "ready", "install", "key", "seen", "documented", "idea"}
REQUIRED = ("id", "family", "name_ar", "name_en", "status", "what", "how")
MAX_SHEET = 400_000


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


@unittest.skipUnless(SKILL.is_dir(), "kosif-superpowers skill not present")
class SuperpowersTest(unittest.TestCase):
    def test_skill_frontmatter(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        m = re.match(r"---\n(.*?)\n---\n", text, re.S)
        self.assertIsNotNone(m, "SKILL.md needs YAML frontmatter")
        self.assertRegex(m.group(1), r"(?m)^name: kosif-superpowers$")
        self.assertRegex(m.group(1), r"(?m)^description: .{40,}")

    def test_relative_links_resolve(self):
        broken = []
        for md in [SKILL / "SKILL.md", *sorted((SKILL / "references").rglob("*.md")), *sorted((SKILL / "proofs").glob("*/README.md"))]:
            for target in re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", md.read_text(encoding="utf-8")):
                if re.match(r"^[a-z]+:", target):
                    continue
                if not (md.parent / target).resolve().exists():
                    broken.append(f"{md.relative_to(SKILL)} -> {target}")
        self.assertEqual(broken, [], "broken relative links")

    def test_power_files_are_well_formed(self):
        files = sorted(POWERS.glob("*.json"))
        self.assertGreaterEqual(len(files), 20, "expected one power file per family")
        seen = {}
        for f in files:
            rows = load(f)
            self.assertIsInstance(rows, list, f.name)
            self.assertTrue(rows, f"{f.name} is empty")
            for r in rows:
                for k in REQUIRED:
                    self.assertTrue(r.get(k), f"{f.name}: {r.get('id')} lacks {k}")
                self.assertEqual(r["family"], f.stem, f"{r['id']} filed under {f.name}")
                self.assertIn(r["status"], STATUSES, f"{r['id']} status {r['status']}")
                self.assertNotIn(r["id"], seen, f"duplicate id {r['id']} ({f.name}, {seen.get(r['id'])})")
                seen[r["id"]] = f.name
                if r["status"] == "install":
                    self.assertTrue(r.get("install"), f"{r['id']} is 'install' but has no install command")

    def test_local_proof_paths_exist(self):
        missing = []
        for f in sorted(POWERS.glob("*.json")):
            for r in load(f):
                for p in r.get("proof") or []:
                    p = str(p).split(":", 1)[0] if re.match(r"^kosif-tool/[^:]+:\d", str(p)) else str(p)
                    if p.startswith("kosif-tool/"):
                        if not (ROOT / p[len("kosif-tool/"):]).exists():
                            missing.append(f"{r['id']}: {p}")
        self.assertEqual(missing, [], "power proofs pointing at missing kosif-tool files")

    def test_styles_data_matches_catalog(self):
        p = SKILL / "data" / "styles.json"
        if not p.is_file():
            self.skipTest("styles.json not generated")
        catalog = {r["id"] for r in load(ROOT / "catalog" / "styles.json")}
        rows = load(p)
        unknown = [r.get("id") for r in rows if r.get("id") not in catalog]
        self.assertEqual(unknown, [], "styles.json ids not in catalog/styles.json")

    def test_proofs_have_readme_and_small_sheet(self):
        for d in sorted(x for x in (SKILL / "proofs").iterdir() if x.is_dir() and not x.name.startswith("_")):
            self.assertTrue((d / "README.md").is_file(), f"{d.name} lacks README.md")
            self.assertNotIn("VERIFY_LINE", (d / "README.md").read_text(encoding="utf-8"), f"{d.name}/README.md still has the VERIFY_LINE placeholder")
            sheet = d / "sheet.jpg"
            self.assertTrue(sheet.is_file(), f"{d.name} lacks sheet.jpg")
            self.assertLessEqual(sheet.stat().st_size, MAX_SHEET, f"{d.name}/sheet.jpg too large")
        videos = [p for p in SKILL.rglob("*") if p.suffix.lower() in {".mp4", ".mov", ".webm", ".wav", ".mp3"}]
        self.assertEqual(videos, [], "rendered media must stay out of the repository")

    def run_script(self, *args):
        proc = subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, encoding="utf-8")
        return proc

    def test_script_stats_search_show(self):
        st = self.run_script("stats")
        self.assertEqual(st.returncode, 0, st.stderr)
        self.assertRegex(st.stdout, r"powers: \d+")
        se = self.run_script("search", "glow")
        self.assertEqual(se.returncode, 0, se.stdout + se.stderr)
        first_id = se.stdout.split()[0]
        sh = self.run_script("show", first_id)
        self.assertEqual(sh.returncode, 0, sh.stdout + sh.stderr)
        self.assertIn(f"id: {first_id}", sh.stdout)

    def test_script_arabic_suggest(self):
        proc = self.run_script("suggest", "دعاء", "هادئ", "9:16")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("9:16", proc.stdout)


if __name__ == "__main__":
    unittest.main()
