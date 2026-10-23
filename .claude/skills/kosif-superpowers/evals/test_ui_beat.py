"""Offline tests for ui_beat.py (cursor keyframes, RTL mirror, loop check)."""
import json
import math
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
SCRIPT = SK / "scripts" / "ui_beat.py"
sys.path.insert(0, str(SK / "scripts"))
import ui_beat as U  # noqa: E402


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)


class UiBeatTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, obj, name="x.json"):
        p = self.d / name
        p.write_text(obj if isinstance(obj, str) else json.dumps(obj), encoding="utf-8")
        return str(p)

    def test_ease_known_values(self):
        e = U.EASES["ease-in-out"]
        self.assertAlmostEqual(U.ease_value(e, 0.5), 0.5, places=9)  # symmetric curve
        self.assertAlmostEqual(U.ease_value(U.EASES["linear"], 0.3), 0.3, places=9)
        self.assertEqual(U.ease_value(e, 0), 0.0)
        self.assertEqual(U.ease_value(e, 1), 1.0)
        self.assertLess(U.ease_value(U.EASES["ease-in"], 0.25), 0.25)
        self.assertGreater(U.ease_value(U.EASES["ease-out"], 0.25), 0.25)
        self.assertEqual(U.parse_ease("cubic-bezier:0.4,0,0.2,1"), (0.4, 0.0, 0.2, 1.0))

    def test_cursor_linear_straight(self):
        c = U.cursor((0, 0), (300, 0), 1, 30, "linear", 0)
        self.assertEqual(c["frames"], 31)
        self.assertEqual([k["x"] for k in c["keyframes"][:3]], [0.0, 10.0, 20.0])
        self.assertEqual(c["keyframes"][15]["x"], 150.0)
        self.assertEqual(c["keyframes"][-1]["x"], 300)
        self.assertTrue(all(k["y"] == 0 for k in c["keyframes"]))

    def test_cursor_arc_control_point_and_click(self):
        c = U.cursor((900, 1700), (540, 960), 0.8, 30)
        # dx=-360, dy=-740; perpendicular (-dy, dx) * 0.12 = (88.8, -43.2) added to midpoint (720, 1330)
        self.assertEqual(c["control_point"], [808.8, 1286.8])
        mid = c["keyframes"][12]
        self.assertEqual(mid["progress"], 0.5)
        # quadratic Bezier at s=0.5: .25*900 + .5*808.8 + .25*540
        self.assertEqual((mid["x"], mid["y"]), (764.4, 1308.4))
        k = c["click"]
        self.assertEqual((k["press_frame"], k["release_frame"], k["ui_response_frame"]), (24, 27, 26))
        self.assertEqual(k["ripple"]["end_frame"], 33)
        self.assertEqual(k["ripple"]["radius_px"], [0, 64])
        self.assertAlmostEqual(c["distance_px"], round(math.hypot(360, 740), 3))

    def test_cursor_cli_and_refusals(self):
        r = run("cursor", "--from", "0,0", "--to", "10,10", "--dur", "0.5", "--fps", "60", "--no-click",
                "--ease", "cubic-bezier:0.65,0,0.35,1")
        self.assertEqual(r.returncode, 0, r.stderr)
        d = json.loads(r.stdout)
        self.assertEqual(d["frames"], 31)
        self.assertNotIn("click", d)
        w = json.loads(run("cursor", "--from", "0,0", "--to", "1,1", "--dur", "1", "--fps", "30",
                           "--response-ms", "250").stdout)
        self.assertIn("warning", w["click"])
        for args in (["--from", "0", "--to", "1,1"], ["--from", "0,0", "--to", "1,1", "--ease", "bounce"],
                     ["--from", "0,0", "--to", "1,1", "--ease", "cubic-bezier:2,0,0,1"]):
            r = run("cursor", *args, "--dur", "1", "--fps", "30")
            self.assertEqual(r.returncode, 2, args)
            self.assertEqual(len(r.stderr.strip().splitlines()), 1)
        self.assertEqual(run("cursor", "--from", "0,0", "--to", "1,1", "--dur", "0", "--fps", "30").returncode, 2)

    def test_rtl_mirror(self):
        lay = {"elements": [{"id": "back", "x": 24, "w": 48, "icon": "chevron-left", "align": "left"},
                            {"id": "title", "x": 100, "w": 400, "text": "الإعدادات", "text_align": "start"},
                            {"id": "play", "x": 980, "w": 76, "icon": "play", "anchor": "right"},
                            {"id": "send", "x": 0, "w": 1080, "icon": "send", "justify": "flex-start"}]}
        r = U.rtl_mirror(lay, 1080)
        e = {x["id"]: x for x in r["elements"]}
        self.assertEqual(e["back"]["x"], 1008)
        self.assertEqual(e["back"]["align"], "right")
        self.assertEqual(e["back"]["icon_transform"], "scaleX(-1)")
        self.assertEqual(e["title"]["x"], 580)
        self.assertEqual(e["title"]["text_align"], "start")
        self.assertEqual(e["title"]["dir"], "rtl")
        self.assertEqual(e["play"]["x"], 24)
        self.assertEqual(e["play"]["anchor"], "left")
        self.assertNotIn("icon_transform", e["play"])
        self.assertEqual(e["send"]["x"], 0)
        self.assertEqual([i["id"] for i in r["icons_flip"]], ["back", "send"])
        self.assertEqual([i["id"] for i in r["icons_keep"]], ["play"])
        self.assertEqual(r["warnings"], [])
        self.assertEqual(U.rtl_mirror([{"x": 1000, "w": 200}], 1080)["warnings"], ["el1 lies outside 0..1080"])

    def test_rtl_cli_and_refusals(self):
        p = self.write({"elements": [{"id": "a", "x": 10, "w": 20}]})
        self.assertEqual(json.loads(run("rtl-mirror", p, "--width", "100").stdout)["elements"][0]["x"], 70)
        self.assertEqual(run("rtl-mirror", self.write({"elements": [{"id": "a"}]}, "b.json"),
                             "--width", "100").returncode, 2)
        self.assertEqual(run("rtl-mirror", self.write({"elements": [{"x": 1, "w": 1, "align": "diagonal"}]},
                                                      "c.json"), "--width", "100").returncode, 2)
        self.assertEqual(run("rtl-mirror", p, "--width", "0").returncode, 2)

    def test_loop_check(self):
        same = U.loop_check({"start": {"card": {"y": 0, "opacity": 1}, "tab": "home"},
                             "end": {"card": {"opacity": 1.0000000001, "y": 0}, "tab": "home"}, "duration": 4})
        self.assertTrue(same["seamless"])
        self.assertEqual(same["keys_compared"], 3)
        self.assertEqual(same["warnings"], [])
        diff = U.loop_check({"states": [{"a": 1, "b": [1, 2], "c": "x"}, {"a": 1}, {"a": 1.5, "b": [1, 3], "d": True}],
                             "duration": 8})
        self.assertFalse(diff["seamless"])
        got = {x["key"]: x["reason"] for x in diff["differing"]}
        self.assertEqual(got, {"a": "delta 0.5", "b[1]": "delta 1", "c": "missing at end", "d": "missing at start"})
        self.assertEqual(len(diff["warnings"]), 1)
        t = U.loop_check([{"v": 1}, {"v": "1"}])
        self.assertEqual(t["differing"][0]["reason"], "type differs")

    def test_loop_cli_and_refusals(self):
        r = run("loop-check", self.write([{"x": 0}, {"x": 0}]))
        self.assertEqual(r.returncode, 0)
        self.assertTrue(json.loads(r.stdout)["seamless"])
        self.assertEqual(run("loop-check", self.write([{"x": 0}], "one.json")).returncode, 2)
        self.assertEqual(run("loop-check", self.write("not json", "nj.json")).returncode, 2)

    def test_deterministic_and_self_test(self):
        a = run("cursor", "--from", "5,5", "--to", "500,300", "--dur", "1.2", "--fps", "30").stdout
        self.assertEqual(a, run("cursor", "--from", "5,5", "--to", "500,300", "--dur", "1.2", "--fps", "30").stdout)
        self.assertEqual(run("--self-test").returncode, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
