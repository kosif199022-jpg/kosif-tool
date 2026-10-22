#!/usr/bin/env python3
"""Regression tests for scripts/prompt_pack.py (copyable prompt packs, warn-only lint). Temp dirs only."""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
SCRIPT = SK / "scripts" / "prompt_pack.py"
FAKE_KEY = "AI" + "za" + "SyD" + "q7Xk2LmN9pR4sT6vW8yZ0aB3cE5fH1jK"  # built at run time: no key literal in this file


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], text=True, capture_output=True, timeout=120)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROMPTS = [
    {"id": "P1", "engine": "midjourney", "text": "A lone fisherman on a wooden boat at dawn, mist over the river, 35mm lens",
     "negative": ["blurry"], "params": {"ar": "16:9", "stylize": 150}, "explain_ar": "افتتاحية هادئة"},
    {"id": "P2", "engine": "veo", "text": "A man and a woman in a Pixar style street at day and night, 8k, a sign that reads \"OPEN\"",
     "params": {"ar": "9:16", "duration": 8}, "explain_ar": "مشهد للاختبار"},
    {"id": "P3", "engine": "generic-image", "text": "Macro shot of dew on a green leaf, soft morning light", "negative": "text, watermark"},
]


class PromptPackTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def put(self, obj):
        p = self.root / "prompts.json"
        p.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")
        return str(p)

    def build(self, obj, *extra):
        out = self.root / "pack"
        r = run("build", self.put(obj), "--out", str(out), *extra)
        return r, out

    def test_one_fence_per_prompt_and_text_byte_identical(self):
        r, out = self.build(PROMPTS)
        self.assertEqual(r.returncode, 0, r.stderr)
        md = (out / "PACK.md").read_text(encoding="utf-8")
        self.assertEqual(md.count("```text\n"), len(PROMPTS))
        pack = json.loads((out / "pack.json").read_text(encoding="utf-8"))
        for src, it in zip(PROMPTS, pack["prompts"]):
            self.assertTrue(it["block"].startswith(src["text"]), "prompt words must be copied unchanged")
            self.assertIn("```text\n" + it["block"] + "\n```", md)
        self.assertIn('<div dir="ltr">', md)

    def test_arabic_explanation_outside_fence(self):
        _r, out = self.build(PROMPTS)
        md = (out / "PACK.md").read_text(encoding="utf-8")
        inside = "".join(part for i, part in enumerate(md.split("```")) if i % 2 == 1)
        self.assertNotIn("افتتاحية هادئة", inside)
        self.assertIn("**الشرح:** افتتاحية هادئة", md)

    def test_engine_suffix_applied_once(self):
        _r, out = self.build(PROMPTS)
        pack = json.loads((out / "pack.json").read_text(encoding="utf-8"))
        mj, vid, img = pack["prompts"]
        self.assertTrue(mj["block"].endswith("--no blurry --ar 16:9 --stylize 150 --v 7"))
        self.assertEqual(mj["block"].count("--v 7"), 1)
        self.assertTrue(mj["version_sensitive"])
        self.assertEqual(mj["engine_version"], "7")
        self.assertEqual(vid["block"].count("No subtitles or on-screen text."), 1)
        self.assertIn("Negative prompt: text, watermark", img["block"])

    def test_lint_warns_but_never_rewrites(self):
        spec = self.put(PROMPTS)
        before = Path(spec).read_bytes()
        r = run("lint", spec)
        self.assertEqual(r.returncode, 2, r.stderr)
        codes = {(w["id"], w["code"]) for w in json.loads(r.stdout)["warnings"]}
        for code in ("CONTRADICTION", "SUBJECTS_UNSEPARATED", "NAMED_STYLE", "HYPE_TOKENS", "TEXT_IN_IMAGE", "NO_NEGATIVE_BASELINE"):
            self.assertIn(("P2", code), codes)
        self.assertFalse(any(i == "P1" for i, _c in codes), codes)
        self.assertEqual(Path(spec).read_bytes(), before, "lint must not touch the input file")
        _r, out = self.build(PROMPTS)
        pack = json.loads((out / "pack.json").read_text(encoding="utf-8"))
        self.assertEqual(pack["prompts"][1]["text"].encode("utf-8"), PROMPTS[1]["text"].encode("utf-8"))
        self.assertIn("Pixar", pack["prompts"][1]["block"])
        self.assertIn("8k", pack["prompts"][1]["block"])

    def test_no_word_swap_dictionary(self):
        src = SCRIPT.read_text(encoding="utf-8").lower()
        for banned in ("sanitizeprompt", "euphemism_map", "replacements = {", "word_swap"):
            self.assertNotIn(banned, src)

    def test_secret_refused_and_never_echoed(self):
        bad = [{"id": "K1", "text": "A city at dusk " + FAKE_KEY}]
        r, out = self.build(bad)
        self.assertEqual(r.returncode, 3)
        self.assertNotIn(FAKE_KEY, r.stdout + r.stderr)
        self.assertFalse((out / "PACK.md").exists())
        r = run("lint", self.put(bad))
        self.assertEqual(r.returncode, 3)
        self.assertNotIn(FAKE_KEY, r.stdout + r.stderr)

    def test_scene_spec_refs_write_start_here(self):
        spec = {"title": "قصة", "engine": "midjourney",
                "scenes": [{"scene": "S1", "prompt_en": "A red kite over dunes, wide shot", "negatives": ["text"], "refs": ["kite.png"]}]}
        r, out = self.build(spec)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("kite.png", (out / "START-HERE.md").read_text(encoding="utf-8"))

    def test_jobs_folder_refused(self):
        repo = SK.parents[2]
        r = run("build", self.put(PROMPTS), "--out", str(repo / "jobs" / "_prompt_pack_test"))
        self.assertEqual(r.returncode, 1)
        self.assertIn("jobs/", r.stderr)
        self.assertFalse((repo / "jobs" / "_prompt_pack_test").exists())

    def test_fusionforge_accepts_prompt_kind(self):
        ff = load("fusionforge_for_prompt_pack", SK / "scripts" / "fusionforge.py")
        self.assertIn("prompt", ff.KINDS)
        a4 = (SK / "references" / "protocol" / "A4-fusionforge-composition.md").read_text(encoding="utf-8")
        self.assertIn("font, prompt, evidence", a4)


if __name__ == "__main__":
    unittest.main(verbosity=2)
