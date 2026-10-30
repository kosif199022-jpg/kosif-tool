"""workflows/dua-daily: config checks, page build (no browser), fonts with their OFL texts, seek hook."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WF = ROOT / "workflows" / "dua-daily"
spec = importlib.util.spec_from_file_location("dua_daily", WF / "scripts" / "dua_daily.py")
dua = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dua)


class DuaDailyTest(unittest.TestCase):
    def write(self, d, cfg):
        p = Path(d) / "c.json"
        p.write_text(json.dumps(cfg, ensure_ascii=False), encoding="utf-8")
        return p

    def test_build_injects_config_and_fonts(self):
        with tempfile.TemporaryDirectory() as d:
            page = dua.build(WF / "config_example.json", Path(d) / "job")
            html = page.read_text(encoding="utf-8")
            self.assertIn("window.__DUA_CFG=", html)
            self.assertLess(html.index("window.__DUA_CFG="), html.index("const W=720"))
            self.assertIn("يا أرحم الراحمين", html)
            self.assertTrue((Path(d) / "job" / "fonts" / "ArefRuqaa-Bold.ttf").exists())

    def test_script_close_tag_is_escaped(self):
        with tempfile.TemporaryDirectory() as d:
            cfg = {"date": "2026-10-20", "segments": [{"start": 0, "end": 2, "text": "</script><b>x"}]}
            html = dua.build(self.write(d, cfg), Path(d) / "job").read_text(encoding="utf-8")
            self.assertNotIn("</script><b>x", html)

    def test_rejects_bad_configs(self):
        bad = [
            {"date": "2026-10-20", "segments": []},
            {"date": "2026-10-20", "segments": [{"start": 0, "end": 2, "text": " "}]},
            {"date": "2026-10-20", "segments": [{"start": 2, "end": 1, "text": "a"}]},
            {"date": "2026-10-20", "segments": [{"start": 0, "end": 3, "text": "a"}, {"start": 1, "end": 4, "text": "b"}]},
            {"date": "20/10/2026", "segments": [{"start": 0, "end": 2, "text": "a"}]},
            {"date": "2026-10-20", "audio": "missing.m4a", "segments": [{"start": 0, "end": 2, "text": "a"}]},
        ]
        for cfg in bad:
            with self.subTest(cfg=cfg), tempfile.TemporaryDirectory() as d:
                with self.assertRaises(SystemExit):
                    dua.build(self.write(d, cfg), Path(d) / "job")

    def test_seek_hook_matches_renderer(self):
        html = (WF / "template.html").read_text(encoding="utf-8")
        renderer = (ROOT / "tools" / "render_html.cjs").read_text(encoding="utf-8")
        for hook in ("__kosifReady", "__kosif"):
            self.assertIn(hook, renderer)
            self.assertIn("window." + hook + "=", html)
        self.assertIn("devicePixelRatio", html)

    def test_every_font_has_its_licence(self):
        fonts = WF / "fonts"
        credits = (WF / "CREDITS.md").read_text(encoding="utf-8")
        ttfs = sorted(fonts.glob("*.ttf"))
        self.assertEqual(len(ttfs), 5)
        for f in ttfs:
            self.assertIn(f.name, credits)
        for lic in fonts.glob("OFL-*.txt"):
            self.assertIn("SIL OPEN FONT LICENSE", lic.read_text(encoding="utf-8").upper())
            self.assertIn(lic.name, credits)


if __name__ == "__main__":
    unittest.main()
