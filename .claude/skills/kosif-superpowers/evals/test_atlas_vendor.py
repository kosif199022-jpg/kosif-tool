"""Vendored Atlas skills: every file matches its manifest hash, only safe skills are copied, and cards point at real folders."""
import hashlib
import json
import sys
import unittest
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
V = SK / "vendor" / "kosif-atlas"
sys.path.insert(0, str(SK / "scripts"))
import atlas_5000  # noqa: E402


class AtlasVendorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.man = json.loads((V / "KOSIF_INTEGRATION.json").read_text(encoding="utf-8"))
        cls.idx = {str(s["id"]): s for s in atlas_5000.load_index()["skills"]}

    def test_manifest_hashes_match_files(self):
        self.assertEqual(self.man["skills_count"], len(self.man["skills"]))
        for s in self.man["skills"]:
            for f in s["files"]:
                data = (V / s["path"] / f["path"]).read_bytes()
                self.assertEqual(hashlib.sha256(data).hexdigest(), f["sha256"], (s["path"], f["path"]))

    def test_only_safe_permissive_skills_are_copied(self):
        for s in self.man["skills"]:
            self.assertTrue(atlas_5000.is_safe(self.idx[str(s["atlas_id"])]), s["atlas_id"])
            self.assertTrue((V / s["path"]).parent.joinpath("SOURCE.md").is_file(), s["path"])
            self.assertTrue((V / s["path"] / "SKILL.md").is_file() or (V / s["path"] / "skill.md").is_file(), s["path"])

    def test_no_executable_or_binary_files(self):
        text = {".md", ".txt", ".json", ".yaml", ".yml", ".csv", ".toml"}
        for p in V.rglob("*"):
            if p.is_file() and p.name not in ("LICENSE", "NOTICE"):
                self.assertIn(p.suffix.lower(), text, p)
                self.assertFalse(p.stat().st_mode & 0o111, p)

    def test_cards_point_at_vendored_folders(self):
        paths = {f"vendor/kosif-atlas/{s['path']}" for s in self.man["skills"]}
        seen = 0
        for f in (SK / "data" / "powers").glob("atlas-*.json"):
            for r in json.loads(f.read_text(encoding="utf-8")):
                for p in (r.get("atlas") or {}).get("vendored") or []:
                    self.assertIn(p, paths, r["id"])
                    self.assertIn(p, r["install"], r["id"])
                    seen += 1
        self.assertGreater(seen, 0)


if __name__ == "__main__":
    unittest.main()
