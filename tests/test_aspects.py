"""Any-aspect support: tools/aspects.py, the CLI and the request generator agree."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from aspects import resolve, ratio_of, is_valid  # noqa: E402

CASES = {
    "9:16": (1080, 1920), "16:9": (1920, 1080), "1:1": (1080, 1080), "4:5": (1080, 1350),
    "4:3": (1440, 1080), "3:4": (1080, 1440), "2:3": (1080, 1620), "21:9": (1920, 824),
    "2.35:1": (1920, 818), "2.39:1": (1920, 804), "1920x816": (1920, 816), "3840x2160": (3840, 2160),
    "reel": (1080, 1920), "cinema": (1920, 804), "مربع": (1080, 1080),
}


class AspectsTest(unittest.TestCase):
    def test_resolve_sizes_are_even_and_match(self):
        for spec, size in CASES.items():
            _, w, h = resolve(spec)
            self.assertEqual((w, h), size, spec)
            self.assertEqual((w % 2, h % 2), (0, 0), spec)

    def test_ratio_and_validation(self):
        self.assertAlmostEqual(ratio_of("2.35:1"), 1920 / 818, places=3)
        for bad in ("", "abc", "0:1", "10:1", "1x1", "10x00"):
            self.assertFalse(is_valid(bad), bad)

    def test_cli_prompt_accepts_any_aspect(self):
        rec = json.loads((ROOT / "catalog" / "styles.json").read_text(encoding="utf-8"))[0]["id"]
        for spec, res in (("2.35:1", "1920x818"), ("3:4", "1080x1440"), ("cinema", "1920x804")):
            p = subprocess.run([sys.executable, str(ROOT / "tools" / "kosif.py"), "prompt", rec, "--aspect", spec, "--lang", "en"],
                               capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertIn(res, p.stdout, spec)
        for spec in ("junk", "1x1", "10x00"):  # pixel specs are validated too: argparse error, no traceback
            bad = subprocess.run([sys.executable, str(ROOT / "tools" / "kosif.py"), "prompt", rec, "--aspect", spec], capture_output=True, text=True)
            self.assertEqual(bad.returncode, 2, spec)
            self.assertIn("argument --aspect", bad.stderr, spec)
            self.assertNotIn("Traceback", bad.stderr, spec)

    def test_generator_mirrors_python(self):
        js = ("import('./web/generator.js').then(g=>{const o={};for(const s of %s){const r=g.resolveAspect(s);o[s]=[r.w,r.h]}"
              "console.log(JSON.stringify(o))})") % json.dumps(list(CASES))
        p = subprocess.run(["node", "--input-type=module", "-e", js], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        if p.returncode != 0:
            self.skipTest(f"node unavailable: {p.stderr[:200]}")
        got = json.loads(p.stdout)
        for spec, size in CASES.items():
            self.assertEqual(tuple(got[spec]), size, spec)


if __name__ == "__main__":
    unittest.main()
