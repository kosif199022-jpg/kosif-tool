"""Offline known-answer tests for scripts/brand_tokens.py (palette, tokens, contrast)."""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import brand_tokens as B  # noqa: E402

SVG = """<svg xmlns="http://www.w3.org/2000/svg"><style>.a{fill:red}.b{stroke-width:2;color:#222}</style>
<defs><linearGradient id="g"><stop offset="0" stop-color="#00f"/>
<stop offset="1" style="stop-color:hsl(240,100%,50%)"/></linearGradient></defs>
<rect fill="#F00"/><path style="fill:#ff0000;stroke:rgb(0, 0, 255)"/><circle fill="none" stroke="url(#g)"/>
<path fill="#3366cc80"/><path fill="weird"/><text fill="currentColor">x</text></svg>"""


def run(args):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            rc = B.main(args)
        except SystemExit as e:
            rc = e.code
    return rc, out.getvalue(), err.getvalue()


class BrandTokensTests(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.d = Path(self.t.name)

    def tearDown(self):
        self.t.cleanup()

    def w(self, name, obj):
        p = self.d / name
        p.write_text(obj if isinstance(obj, str) else json.dumps(obj), encoding="utf-8")
        return str(p)

    def test_parse_and_wcag_math(self):
        self.assertEqual(B.parse_color("#F00"), ("#ff0000", 1.0))
        self.assertEqual(B.parse_color("rgb(100%, 0%, 0%)"), ("#ff0000", 1.0))
        self.assertEqual(B.parse_color("rgba(0 0 255 / 50%)"), ("#0000ff", 0.5))
        self.assertEqual(B.parse_color("hsl(120, 100%, 25%)"), ("#008000", 1.0))
        self.assertEqual(B.parse_color("#3366cc80"), ("#3366cc", 0.502))
        self.assertIsNone(B.parse_color("url(#g)"))
        self.assertEqual(round(B.ratio("#000000", "#ffffff"), 2), 21.0)
        self.assertEqual(round(B.ratio("#777777", "#ffffff"), 2), 4.48)  # the classic just-fails grey
        self.assertEqual(round(B.ratio("#767676", "#ffffff"), 2), 4.54)
        self.assertEqual(B.scale("#3366cc")["100"], "#d6e0f5")  # 51*.2+255*.8=214.2 ...
        self.assertEqual(B.scale("#3366cc")["900"], "#0a1429")  # 51*.2=10.2, 102*.2=20.4, 204*.2=40.8

    def test_palette_counts(self):
        r = B.palette(self.w("l.svg", SVG))
        got = {c["hex"]: c["count"] for c in r["colors"]}
        self.assertEqual(got, {"#0000ff": 3, "#ff0000": 3, "#222222": 1, "#3366cc": 1})
        self.assertEqual(r["total_uses"], 8)
        self.assertEqual(r["colors"][0]["hex"], "#0000ff")  # tie broken by hex
        self.assertEqual(r["colors"][0]["roles"], {"stop-color": 2, "stroke": 1})
        self.assertEqual(next(c for c in r["colors"] if c["hex"] == "#3366cc")["alpha_values"], [0.502])
        self.assertEqual(r["unparsed"], ["weird"])

    def test_tokens_three_tiers(self):
        r = B.tokens(self.w("p.json", {"primary": "#3366cc"}))
        self.assertTrue(r["neutral_synthesized"])
        self.assertEqual(r["core"]["color"]["primary"]["500"], {"$value": "#3366cc", "$type": "color"})
        self.assertEqual(r["semantic"]["color"]["action"]["primary"]["$value"], "{core.color.primary.500}")
        self.assertEqual(r["component"]["button"]["primary"]["bg"]["$value"], "{semantic.color.action.primary}")
        self.assertEqual(r["resolved"]["component.button.primary.bg"], "#3366cc")
        self.assertEqual(r["resolved"]["component.button.primary.bg-hover"], "#2952a3")
        self.assertIn("--button-primary-bg: var(--color-action-primary);", r["css"])
        self.assertIn("--core-color-primary-500: #3366cc;", r["css"])
        # pure red fails white text (4.0), so the action colour steps to 600 (#cc0000, 5.89)
        r2 = B.tokens(self.w("l.json", ["#ffffff", "#ff0000", "#808080"]))
        self.assertEqual(r2["sources"], {"neutral": "#808080", "primary": "#ff0000"})
        self.assertEqual(r2["resolved"]["semantic.color.action.primary"], "#cc0000")
        # palette output feeds tokens directly
        pal = self.w("pal.json", B.palette(self.w("l.svg", SVG)))
        self.assertEqual(B.tokens(pal)["sources"]["primary"], "#0000ff")

    def test_contrast_matrix(self):
        tk = self.w("t.json", B.tokens(self.w("p.json", {"primary": "#3366cc"})))
        r = B.contrast(tk)
        self.assertEqual(r["mode"], "intended-pairs")
        self.assertEqual(r["fail_AA"], [])
        flat = B.contrast(self.w("f.json", {"text": "#777777", "bg": "#ffffff"}))
        self.assertEqual(flat["mode"], "text-on-background")
        row = flat["matrix"][0]
        self.assertEqual((row["ratio"], row["AA"], row["AA_large"], row["AAA"]), (4.48, False, True, False))
        dtcg = {"color": {"base": {"$value": "#000000"}, "text": {"$value": "{color.base}"}, "bg": {"$value": "#ffffff"}}}
        self.assertEqual(B.contrast(self.w("d.json", dtcg))["matrix"][0]["ratio"], 21.0)
        allp = B.contrast(self.w("a.json", {"a": "#000000", "b": "#ffffff", "c": "#000000"}))
        self.assertEqual((allp["mode"], allp["pairs"]), ("all-pairs", 2))

    def test_bad_input_and_determinism(self):
        svg = self.w("l.svg", SVG)
        self.assertEqual(run(["palette", svg]), run(["palette", svg]))
        circ = self.w("c.json", {"x": {"text": {"$value": "{x.bg}"}, "bg": {"$value": "{x.text}"}}})
        for args in (["palette", self.w("n.svg", "<html></html>")], ["palette", str(self.d / "missing.svg")],
                     ["tokens", self.w("b.json", {"primary": "blue-ish"})], ["tokens", self.w("e.json", [])],
                     ["contrast", circ], ["contrast", self.w("one.json", {"a": "#000"})], ["paint"]):
            rc, out, err = run(args)
            self.assertEqual(rc, 2, args)
            self.assertEqual(out, "")
            self.assertEqual(len(err.strip().splitlines()), 1, (args, err))
        rc, out, _ = run(["tokens", self.w("p.json", {"primary": "#3366cc"}), "--css"])
        self.assertTrue(out.startswith(":root {"))
        self.assertEqual(run(["--self-test"])[0], 0)
        from unittest import mock
        with mock.patch("sys.stdin", io.StringIO('<svg><rect fill="#1D4ED8"/><circle fill="#1d4ed8"/></svg>')):
            rc, out, _ = run(["palette", "-"])
        self.assertEqual((rc, json.loads(out)["colors"][0]["count"]), (0, 2))


if __name__ == "__main__":
    unittest.main()
