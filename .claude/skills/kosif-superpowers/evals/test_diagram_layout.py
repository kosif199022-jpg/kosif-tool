"""Offline tests for diagram_layout.py (lint, layered layout, SVG)."""
import json
import subprocess
import sys
import tempfile
import unittest
import xml.dom.minidom
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
SCRIPT = SK / "scripts" / "diagram_layout.py"
sys.path.insert(0, str(SK / "scripts"))
import diagram_layout as D  # noqa: E402

CHAIN = {"nodes": [{"id": "a", "label": "المستخدم", "role": "user"}, {"id": "b", "label": "API", "role": "backend"},
                   {"id": "c", "label": "DB", "role": "data"}],
         "edges": [{"from": "a", "to": "b", "label": "طلب"}, {"from": "b", "to": "c", "label": "query"},
                   {"from": "a", "to": "c", "label": "cache"}]}


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)


class DiagramLayoutTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, obj, name="g.json"):
        p = self.d / name
        p.write_text(obj if isinstance(obj, str) else json.dumps(obj, ensure_ascii=False), encoding="utf-8")
        return str(p)

    def test_lint_findings(self):
        g = {"nodes": [{"id": "a"}, {"id": "b"}, {"id": "c"}, {"id": "o"}, {"id": "a"},
                       {"id": "l", "label": "x" * 30}],
             "edges": [{"from": "a", "to": "b", "label": "go"}, {"from": "b", "to": "c", "label": "go"},
                       {"from": "c", "to": "a", "label": "back"}, {"from": "a", "to": "zz"},
                       {"from": "l", "to": "l"}]}
        r = D.lint(g)
        codes = sorted(f["code"] for f in r["findings"])
        self.assertIn("DUPLICATE_ID", codes)
        self.assertIn("DANGLING_EDGE", codes)
        self.assertIn("SELF_LOOP", codes)
        self.assertIn("LONG_LABEL", codes)
        self.assertEqual(r["cycles"], [["a", "b", "c"]])
        self.assertEqual([f["id"] for f in r["findings"] if f["code"] == "ORPHAN"], ["o"])
        self.assertEqual(r["errors"], 2)
        self.assertEqual(r["verdict"], "fail")

    def test_lint_clean_and_too_many(self):
        self.assertEqual(D.lint(CHAIN)["verdict"], "pass")
        self.assertEqual(D.lint(CHAIN)["findings"], [])
        big = {"nodes": [{"id": str(i)} for i in range(10)],
               "edges": [{"from": str(i), "to": str(i + 1), "label": "n"} for i in range(9)]}
        self.assertIn("TOO_MANY_NODES", [f["code"] for f in D.lint(big)["findings"]])

    def test_layout_longest_path_coordinates(self):
        L = D.layout(CHAIN)
        # c is at layer 2 (longest path a->b->c), not 1
        self.assertEqual({n["id"]: n["layer"] for n in L["nodes"]}, {"a": 0, "b": 1, "c": 2})
        # W = 2*40 + 3*180 + 2*90 = 800 ; H = 2*40 + 80 = 160
        self.assertEqual((L["width"], L["height"]), (800, 160))
        self.assertEqual([(n["x"], n["y"]) for n in L["nodes"]], [(40, 40), (310, 40), (580, 40)])
        e = L["edges"][0]
        self.assertEqual(e["points"], [[220, 80], [310, 80]])

    def test_layout_rtl_mirror(self):
        L, R = D.layout(CHAIN), D.layout(CHAIN, rtl=True)
        for a, b in zip(L["nodes"], R["nodes"]):
            self.assertEqual(b["x"], L["width"] - a["x"] - a["w"])
            self.assertEqual(b["y"], a["y"])
        self.assertEqual(R["nodes"][0]["x"], 580)
        # edge leaves the left side of a and enters the right side of b
        self.assertEqual(R["edges"][0]["points"], [[580, 80], [490, 80]])

    def test_layout_tb_and_cycle_and_ordering(self):
        g = {"nodes": [{"id": "s"}, {"id": "x"}, {"id": "y"}, {"id": "t"}],
             "edges": [{"from": "s", "to": "y"}, {"from": "s", "to": "x"}, {"from": "x", "to": "t"},
                       {"from": "y", "to": "t"}, {"from": "t", "to": "s"}]}
        L = D.layout(g, direction="tb")
        self.assertEqual(L["reversed_edges"], [["t", "s"]])
        layer = {n["id"]: n["layer"] for n in L["nodes"]}
        self.assertEqual(layer, {"s": 0, "x": 1, "y": 1, "t": 2})
        # TB: W = 80 + 2*180 + 40 = 480 ; H = 80 + 3*80 + 2*90 = 500 ; x, y in input order within layer 1
        self.assertEqual((L["width"], L["height"]), (480, 500))
        xs = {n["id"]: n["x"] for n in L["nodes"]}
        self.assertLess(xs["x"], xs["y"])
        self.assertEqual(xs["s"], 150)

    def test_layout_refuses_lint_errors(self):
        with self.assertRaises(D.Bad):
            D.layout({"nodes": [{"id": "a"}], "edges": [{"from": "a", "to": "q"}]})

    def test_svg_rtl_arabic(self):
        s = D.svg(CHAIN, rtl=True)
        doc = xml.dom.minidom.parseString(s.encode("utf-8"))
        groups = [g.getAttribute("id") for g in doc.getElementsByTagName("g")]
        self.assertEqual(groups, ["background", "connectors", "boxes", "labels"])
        texts = {t.firstChild.data: t for t in doc.getElementsByTagName("text")}
        self.assertEqual(texts["المستخدم"].getAttribute("direction"), "rtl")
        self.assertEqual(texts["API"].getAttribute("direction"), "ltr")
        self.assertEqual(texts["API"].getAttribute("unicode-bidi"), "isolate")
        rects = {r.getAttribute("id"): r for r in doc.getElementsByTagName("rect")}
        self.assertEqual(rects["n-b"].getAttribute("stroke"), "#34d399")
        self.assertEqual(rects["n-c"].getAttribute("stroke"), "#a78bfa")
        self.assertEqual(len(doc.getElementsByTagName("marker")), 1)
        self.assertEqual(len([p for p in doc.getElementsByTagName("path") if p.getAttribute("marker-end")]), 3)

    def test_cli_all_and_bad_input(self):
        p = self.write(CHAIN)
        self.assertEqual(json.loads(run("lint", p).stdout)["verdict"], "pass")
        self.assertEqual(json.loads(run("layout", p, "--rtl").stdout)["rtl"], True)
        out = self.d / "f.svg"
        r = run("svg", p, "--rtl", "--theme", "light", "--out", str(out))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("#ffffff", out.read_text(encoding="utf-8"))
        self.assertTrue(run("svg", p).stdout.startswith("<svg"))
        for bad in ("{", json.dumps({"edges": []}), json.dumps({"nodes": [{"label": "x"}]})):
            r = run("lint", self.write(bad, "bad.json"))
            self.assertEqual(r.returncode, 2)
            self.assertEqual(len(r.stderr.strip().splitlines()), 1)
        self.assertEqual(run("layout", self.write({"nodes": [{"id": "a"}], "edges": [{"from": "a", "to": "b"}]},
                                                  "d.json")).returncode, 2)

    def test_deterministic_and_self_test(self):
        p = self.write(CHAIN)
        self.assertEqual(run("svg", p, "--rtl").stdout, run("svg", p, "--rtl").stdout)
        self.assertEqual(run("--self-test").returncode, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
