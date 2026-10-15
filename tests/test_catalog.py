"""Schema invariants over the real catalog (catalog/SCHEMA.md).

Skips with a clear reason when catalog/styles.json cannot be read, which
happens while another process regenerates it.
"""
from __future__ import annotations

import json
import re
import sys
import unittest
from collections import Counter
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _fixture import REAL_ROOT, TOOLS, real_catalog  # noqa: E402

sys.path.insert(0, str(TOOLS))
import validate  # noqa: E402  (tools/validate.py — pure functions reused here)

ORIGINS = {"PromptsMotion", "KOSIF original style"}
TYPES = {"Prompt", "Skill", "Style"}
ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]*$")


class RealCatalogTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        data, reason = real_catalog()
        if data is None:
            raise unittest.SkipTest(reason)
        cls.records, cls.categories = data
        cls.cat_keys = {c["key"] for c in cls.categories}
        cls.legacy = {label for c in cls.categories for label in (c.get("legacy") or [])}

    def test_ids_unique_and_slug_shaped(self):
        ids = [r["id"] for r in self.records]
        dups = [k for k, n in Counter(ids).items() if n > 1]
        self.assertEqual(dups, [], f"duplicate ids: {dups}")
        bad = [i for i in ids if not ID_RE.match(i)]
        self.assertEqual(bad, [], f"ids that are not lowercase slugs: {bad[:10]}")

    def test_required_fields_and_enums(self):
        for r in self.records:
            with self.subTest(id=r["id"]):
                self.assertIsInstance(r["name"], str)
                self.assertTrue(r["name"])
                self.assertIn(r["origin"], ORIGINS)
                self.assertIn(r["type"], TYPES)
                self.assertIsInstance(r["category"], list)
                self.assertIsInstance(r["creator"], str)
                self.assertEqual(r["skill"], f"styles/{r['id']}/SKILL.md")
                if r["origin"] == "PromptsMotion":
                    self.assertTrue(r["id"].startswith("pm-"), "PromptsMotion ids are pm-<slug>")
                    self.assertIn(r["type"], {"Prompt", "Skill"})
                else:
                    self.assertEqual(r["type"], "Style")

    def test_urls_are_https_or_null(self):
        for r in self.records:
            with self.subTest(id=r["id"]):
                self.assertTrue(r["page"].startswith("https://"), r["page"])
                for field in ("video", "poster", "creator_url"):
                    v = r.get(field)
                    self.assertTrue(v is None or v.startswith("https://"), f"{field}={v!r}")

    def test_optional_fields_tolerate_null_but_keep_types(self):
        for r in self.records:
            with self.subTest(id=r["id"]):
                a = r.get("aspect")
                if a is not None:
                    self.assertIsInstance(a, dict)
                    self.assertIsInstance(a.get("w"), int)
                    self.assertIsInstance(a.get("h"), int)
                    self.assertGreater(a["w"] * a["h"], 0)
                rank = r.get("rank")
                self.assertTrue(rank is None or (isinstance(rank, int) and rank >= 1), rank)
                pub = r.get("published")
                if pub is not None:
                    date.fromisoformat(pub[:10])
                for field in ("tech", "stack", "keywords", "playbooks"):
                    v = r.get(field)
                    self.assertTrue(v is None or all(isinstance(x, str) for x in v), field)
                d = r.get("difficulty")
                self.assertTrue(d is None or (isinstance(d, int) and 1 <= d <= 5), d)
                spw = r.get("source_prompt_words")
                self.assertTrue(spw is None or isinstance(spw, int), "prompt length is stored as a number only")

    def test_categories_are_known_keys_or_legacy_labels(self):
        for r in self.records:
            for c in r["category"]:
                with self.subTest(id=r["id"], category=c):
                    self.assertTrue(c in self.cat_keys or c in self.legacy, f"unknown category {c!r}")

    def test_aspect_label_matches_aspect(self):
        for r in self.records:
            a, label = r.get("aspect"), r.get("aspect_label")
            if not a or label is None:
                continue
            with self.subTest(id=r["id"]):
                self.assertRegex(label, r"^\d+:\d+$|^other$")
                lr = validate.label_ratio(label)
                if lr is None:
                    self.assertEqual(validate.ratio_label(a["w"], a["h"]), "other")
                else:
                    self.assertLess(abs(lr - a["w"] / a["h"]), validate.RATIO_TOLERANCE)

    def test_prompts_motion_subset(self):
        pm_path = REAL_ROOT / "catalog" / "prompts_motion.json"
        if not pm_path.exists():
            self.skipTest("catalog/prompts_motion.json not present")
        try:
            pm = json.loads(pm_path.read_text(encoding="utf-8"))
        except ValueError as exc:
            self.skipTest(f"prompts_motion.json unreadable (mid-regeneration): {exc}")
        ids = {r["id"] for r in self.records}
        stray = [r["id"] for r in pm if r["id"] not in ids]
        self.assertEqual(stray, [])
        for r in pm:
            self.assertEqual(r["origin"], "PromptsMotion", r["id"])

    def test_categories_json_shape(self):
        keys = [c["key"] for c in self.categories]
        self.assertEqual(len(keys), len(set(keys)), "duplicate category keys")
        for c in self.categories:
            with self.subTest(key=c["key"]):
                for field in ("en", "ar", "playbook"):
                    self.assertIsInstance(c.get(field), str)
                    self.assertTrue(c[field])
                self.assertTrue(c["playbook"].startswith("playbooks/"))
                self.assertIsInstance(c.get("legacy", []), list)

    def test_no_rehosted_media_in_repo(self):
        media = {".mp4", ".webm", ".mov", ".webp", ".png", ".jpg", ".jpeg", ".gif", ".mp3", ".wav"}
        found = [p for base in ("styles", "catalog") for p in (REAL_ROOT / base).rglob("*") if p.suffix.lower() in media]
        self.assertEqual(found, [], f"media binaries must not be rehosted: {found[:5]}")


if __name__ == "__main__":
    unittest.main()
