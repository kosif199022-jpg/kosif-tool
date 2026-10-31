"""Tests for the KOSIF Web Film skill («التنين الأسود»): plan, scaffold, check, and a real seek render."""
import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".claude/skills/kosif-web-film/scripts/web_film.py"
spec = importlib.util.spec_from_file_location("web_film", SCRIPT)
wf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wf)


def filled(duration=8.0):
    p = wf.default_plan("فيديو التنين الأسود", duration, "9:16", ["اسم: التنين الأسود"])
    p["concept"] = "التنين بيصحى ويكتب اسمه"
    for s, t in zip(p["shots"], ["في الضلمة", "حاجة بتصحى", "", "نار ونور", "التنين الأسود"]):
        s["text"] = t
    p["shots"][0]["covers"], p["shots"][-1]["covers"] = [], [0]
    return p


class PlanChecks(unittest.TestCase):
    def test_default_plan_needs_a_concept(self):
        errs = wf.check_plan(wf.default_plan("x"))
        self.assertEqual(errs, ["concept is empty: write the one idea the film serves"])

    def test_filled_plan_passes(self):
        self.assertEqual(wf.check_plan(filled()), [])

    def test_gap_same_length_same_transition_and_uncovered_requirement(self):
        p = filled()
        p["shots"][1]["start"] += 0.5
        self.assertTrue(any("gap or overlap" in e for e in wf.check_plan(p)))
        p = filled()
        n = len(p["shots"])
        for i, s in enumerate(p["shots"]):
            s["start"], s["end"] = i * p["duration"] / n, (i + 1) * p["duration"] / n
        self.assertIn("every shot has the same length: vary the pacing", wf.check_plan(p))
        p = filled()
        p["shots"][1]["transition_in"] = p["shots"][0]["transition_in"]
        self.assertTrue(any("same transition" in e for e in wf.check_plan(p)))
        p = filled()
        p["shots"][-1]["covers"] = []
        self.assertTrue(any("requirement 0" in e for e in wf.check_plan(p)))
        p = filled()
        for s in p["shots"]:
            s["memorable"] = False
        self.assertIn("no shot is marked memorable", wf.check_plan(p))


class HtmlChecks(unittest.TestCase):
    def test_scaffold_passes_its_own_check(self):
        p = filled()
        page = wf.scaffold(p)
        self.assertEqual(wf.check_html(page, p), [])
        self.assertIn('dir="rtl"', page)
        self.assertNotIn(">shape<", page, "an empty shot must not show its kind as text")

    def test_html_rules(self):
        p = filled()
        ok = wf.scaffold(p)
        bad = {
            "network": ok.replace("</head>", '<link href="https://fonts.googleapis.com/css2?family=Cairo"></head>'),
            "wall clock": ok.replace("window.__kosif.seek(0);", "window.__kosif.seek(Date.now()%1);"),
            "Math.random": ok.replace("rng(PLAN.seed||7)", "Math.random"),
            "setInterval": ok.replace("window.__kosif.seek(0);", "setInterval(()=>0,10);"),
            "duration": ok.replace(f"\"duration\": {p['duration']}", "\"duration\": 9.5"),
        }
        for name, page in bad.items():
            self.assertTrue(wf.check_html(page, p), name)


@unittest.skipUnless(shutil.which("node"), "node not installed")
class RealRender(unittest.TestCase):
    def test_scaffold_renders_and_moves(self):
        probe = subprocess.run(["node", "-e", "require('playwright')"], capture_output=True)
        if probe.returncode:
            self.skipTest("playwright not available")
        with tempfile.TemporaryDirectory() as d:
            p = filled(4.0)
            plan, page = Path(d, "film.plan.json"), Path(d, "film.html")
            plan.write_text(json.dumps(p, ensure_ascii=False), encoding="utf-8")
            self.assertEqual(wf.main(["scaffold", str(plan), "--out", str(page)]), 0)
            self.assertEqual(wf.main(["check", str(plan), "--html", str(page)]), 0)
            js = """const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();
            const pg=await b.newPage();const errs=[];pg.on('pageerror',e=>errs.push(e.message));
            await pg.goto(process.argv[1]);const r=await pg.evaluate(()=>{const s=document.querySelector('.shape');
            window.__kosif.seek(%s);const a=s.style.transform;window.__kosif.seek(%s);const z=s.style.transform;
            return {a,z,d:window.__kosif.duration};});console.log(JSON.stringify({...r,errs}));await b.close();})();"""
            sh = p["shots"][2]
            out = subprocess.run(["node", "-e", js % (sh["start"] + 0.05, sh["end"] - 0.05), page.as_uri()],
                                 capture_output=True, text=True, timeout=120, cwd=ROOT)
            r = json.loads(out.stdout.strip().splitlines()[-1])
            self.assertEqual(r["errs"], [])
            self.assertEqual(r["d"], 4.0)
            self.assertNotEqual(r["a"], r["z"], "the shape must move between the start and end of its shot")


if __name__ == "__main__":
    unittest.main()
