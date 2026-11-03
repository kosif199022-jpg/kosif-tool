"""Black Dragon style adapters: a catalog style really scaffolds and renders checked frames."""
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".claude/skills/kosif-superpowers/scripts"
ADAPTER = SCRIPTS / "_black_dragon_style.py"
DATA = ROOT / ".claude/skills/kosif-superpowers/data/black_dragon_adapters_styles.json"
sys.path.insert(0, str(SCRIPTS))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


dragon = load("black_dragon", SCRIPTS / "black_dragon.py")
style = load("bd_style", ADAPTER)
builder = load("bd_style_build", SCRIPTS / "build_black_dragon_style_adapters.py")


def have_browser():
    if not shutil.which("node"):
        return False
    probe = subprocess.run(["node", "-e", "require(require.resolve('playwright',{paths:[process.cwd(),"
                            "'/opt/node-tools/node_modules']}))"], capture_output=True, cwd=ROOT)
    return probe.returncode == 0


HAVE_BROWSER = have_browser()
STYLE_ID = "anime-action"
PLANT_HEAD = "<!doctype html><html><head><meta charset='utf-8'></head>"


class KnownAnswers(unittest.TestCase):
    def test_counter_formula(self):
        self.assertEqual(style.expected_counter(5.0), 126)
        self.assertEqual(style.expected_counter(3.5), 0)
        self.assertEqual(style.expected_counter(7.0), 128)

    def test_frame_size_from_style_aspect(self):
        self.assertEqual(style.frame_size({"aspect": {"w": 1920, "h": 1080}}), (1920, 1080))
        self.assertEqual(style.frame_size({"aspect": None}), (1080, 1920))

    def test_unknown_style_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            art = Path(tmp) / "a.txt"
            done = subprocess.run([sys.executable, str(ADAPTER), "no-such-style", str(art)],
                                  capture_output=True, text=True, timeout=60)
            self.assertEqual(done.returncode, 1)
            self.assertFalse(json.loads(art.read_text(encoding="utf-8"))["passed"])


class Registry(unittest.TestCase):
    def test_generated_file_is_current_and_loaded(self):
        self.assertTrue(DATA.is_file(), "run build_black_dragon_style_adapters.py")
        self.assertEqual(builder.static_check(DATA), [])
        adapters = dragon._load_adapters(dragon.REVIEWED_ADAPTERS)
        inventory = dragon.full_inventory()
        doc = json.loads(DATA.read_text(encoding="utf-8"))
        self.assertTrue(doc["adapters"])
        for key, spec in doc["adapters"].items():
            self.assertEqual(inventory[key]["kind"], "style", key)
            self.assertIn(key, adapters)
            dragon._safe_script(spec["script"])
        self.assertEqual(doc["counts"]["verified"] + doc["counts"]["excluded"], doc["counts"]["catalog_styles"])
        self.assertEqual(doc["counts"]["catalog_styles"],
                         sum(1 for k, v in inventory.items() if v.get("kind") == "style"))


@unittest.skipUnless(HAVE_BROWSER, "node + playwright needed")
class EndToEnd(unittest.TestCase):
    def test_one_style_through_black_dragon_attempt(self):
        doc = json.loads(DATA.read_text(encoding="utf-8")) if DATA.is_file() else {}
        spec = doc.get("adapters", {}).get("style:" + STYLE_ID) or {
            "script": ADAPTER.relative_to(ROOT).as_posix(), "args": [STYLE_ID, "{artifact}", "--task={task}"]}
        with tempfile.TemporaryDirectory(dir=ROOT / "out" if (ROOT / "out").is_dir() else None) as tmp:
            job = Path(tmp)
            (job / "receipts").mkdir()
            result = dragon._attempt("style:" + STYLE_ID, spec, "test task", job, True, 120, kind="style")
            self.assertEqual(result["status"], "executed", result)
            receipt = json.loads(Path(result["receipt"]).read_text(encoding="utf-8"))
            art = json.loads(Path(receipt["artifact"]).read_text(encoding="utf-8"))
            self.assertTrue(art["passed"], art["failed_checks"])
            self.assertEqual(art["entry"], "style:" + STYLE_ID)
            self.assertEqual(art["known_answers"]["counter"], 126)
            self.assertEqual(len(art["frames"]), 3)
            self.assertNotEqual(art["frames"][0]["sha256"], art["frames"][1]["sha256"])
            self.assertEqual(art["frames"][0]["sha256"], art["frames"][2]["sha256"])
            self.assertEqual(art["frames"][0]["dom"]["title_words"], style.title_words(
                json.loads((ROOT / "styles" / STYLE_ID / "STYLE.json").read_text(encoding="utf-8"))))
            for row in art["frames"][:2]:
                self.assertTrue(Path(row["thumbnail"]["path"]).is_file())

    def planted(self, body):
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp, True)
        page = tmp / "page.html"
        page.write_text(PLANT_HEAD + body + "</html>", encoding="utf-8")
        rep = style.Report()
        out = style.render_frames(page, tmp, (320, 568), style.TIMES, rep)
        self.assertIsNotNone(out, rep.checks)
        style.frame_checks(out, (320, 568), rep, None)
        return rep

    def failed(self, rep, words):
        return [c["check"] for c in rep.checks if not c["pass"] and words in c["check"]]

    def test_blank_page_is_rejected(self):
        rep = self.planted("<body style='margin:0;background:#000'><script>"
                           "window.__kosif={duration:12,fps:30,seek(){}};</script></body>")
        self.assertFalse(rep.passed)
        self.assertTrue(self.failed(rep, "not blank"))
        self.assertTrue(self.failed(rep, "differ (motion"))

    def test_static_slide_is_rejected(self):
        stripes = "".join(f"<div style='height:40px;background:hsl({i*37},70%,50%)'></div>" for i in range(14))
        rep = self.planted("<body style='margin:0'>" + stripes + "<script>"
                           "window.__kosif={duration:12,fps:30,seek(){}};</script></body>")
        self.assertFalse(rep.passed)
        self.assertFalse(self.failed(rep, "not blank"), rep.checks)
        self.assertEqual(self.failed(rep, "differ (motion"), [c["check"] for c in rep.checks
                                                              if not c["pass"]])

    def test_moving_page_passes_pixel_checks_but_js_error_fails(self):
        moving = ("<body style='margin:0;background:#123'><div id='b' style='position:absolute;width:120px;"
                  "height:120px;background:#fc6'></div><script>window.__kosif={duration:12,fps:30,"
                  "seek(t){document.getElementById('b').style.left=(t*40)+'px';"
                  "document.getElementById('b').style.top=(t*60)+'px';}};</script></body>")
        self.assertTrue(self.planted(moving).passed)
        rep = self.planted(moving.replace("</script>", "</script><script>undefinedThing();</script>"))
        self.assertEqual([c["check"] for c in rep.checks if not c["pass"]],
                         ["page loaded with no JavaScript or console error"])


if __name__ == "__main__":
    unittest.main()
