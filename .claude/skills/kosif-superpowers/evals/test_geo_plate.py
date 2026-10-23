"""Offline tests for geo_plate.py (projection to pixels, choropleth classing, coordinate ledger)."""
import json
import math
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
SCRIPT = SK / "scripts" / "geo_plate.py"
sys.path.insert(0, str(SK / "scripts"))
import geo_plate as G  # noqa: E402


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)


def xy(r):
    return [(p["x"], p["y"]) for p in r["points"]]


class GeoPlateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_equirect_world(self):
        r = G.project("equirect", "2000x1000", ["0,0", "-180,90", "180,-90", "90,45"])
        self.assertEqual(xy(r), [(1000, 500), (0, 0), (2000, 1000), (1500, 250)])

    def test_equirect_ref_lat_squash(self):
        # cos(60) = 0.5 makes the world square: lon 90 -> 3/4 of a 1000 px plate
        r = G.project("equirect", "1000x1000", ["90,0", "180,90"], ref_lat=60)
        self.assertEqual(xy(r), [(750, 500), (1000, 0)])

    def test_mercator(self):
        r = G.project("mercator", "1024x1024", ["0,0", "180,85.05112878", "0,45", "0,89"])
        self.assertAlmostEqual(r["points"][0]["x"], 512, places=3)
        self.assertAlmostEqual(r["points"][0]["y"], 512, places=3)
        self.assertAlmostEqual(r["points"][1]["y"], 0, places=2)
        # y = (1 - ln(tan(67.5 deg))/pi)/2 * 1024 = 368.36
        self.assertAlmostEqual(r["points"][2]["y"], 368.36, delta=0.01)
        self.assertTrue(r["points"][3].get("clamped_lat"))

    def test_bbox_fit_and_negative_cli(self):
        p = run("project", "--proj", "equirect", "--size", "400x200", "--bbox", "-10,-5,10,5", "-10,5", "10,-5", "0,0")
        self.assertEqual(p.returncode, 0, p.stderr)
        r = json.loads(p.stdout)
        self.assertEqual(xy(r), [(0, 0), (400, 200), (200, 100)])
        self.assertEqual(run("project", "--proj", "equirect", "--size", "10x10", "10,95").returncode, 2)
        self.assertEqual(run("project", "--proj", "mercator", "--size", "10x10", "--ref-lat", "30", "0,0").returncode, 2)

    def test_breaks_known(self):
        self.assertEqual(G.breaks_jenks([1, 2, 3, 10, 11, 12, 20, 21, 22], 3), [1, 3, 12, 22])
        self.assertEqual(G.breaks_jenks([10, 20, 300, 1100, 1200, 2000], 3), [10, 300, 1200, 2000])
        self.assertEqual(G.breaks_quantile([1, 2, 3, 4, 5], 2), [1, 3, 5])
        self.assertEqual(G.breaks_equal([0, 3, 10], 5), [0, 2, 4, 6, 8, 10])
        self.assertAlmostEqual(G.gvf([1, 2, 3, 10, 11, 12, 20, 21, 22], [1, 3, 12, 22]), 1 - 6 / 548.0, places=9)

    def test_classify_raw_counts_warning(self):
        f = self.d / "r.csv"
        f.write_text("region,cases,pop\nA,10,1000\nB,20,1000\nC,300,1000\nD,1100,1000\nE,1200,1000\nF,2000,1000\n")
        r = G.classify(str(f), "cases", "jenks", 3)
        self.assertEqual((r["breaks"], r["class_counts"]), ([10, 300, 1200, 2000], [3, 2, 1]))
        self.assertTrue(r["normalization"]["looks_like_raw_counts"])
        self.assertEqual(len(r["warnings"]), 1)
        self.assertEqual([x["class"] for x in r["rows"]], [1, 1, 1, 2, 2, 3])

    def test_classify_per_capita(self):
        f = self.d / "r.csv"
        f.write_text("region,cases,pop\nA,10,100\nB,10,1000\nC,50,1000\nD,30,100\n")
        r = G.classify(str(f), "cases", "equal", 2, per_capita="pop", scale=1000)
        self.assertEqual([x["value"] for x in r["rows"]], [100, 10, 50, 300])
        self.assertEqual(r["breaks"], [10, 155, 300])
        self.assertTrue(r["normalization"]["normalized"])
        self.assertEqual(r["warnings"], [])
        g = self.d / "g.csv"
        g.write_text("region,rate\nA,1\nB,2\nC,3\n")
        self.assertEqual(G.classify(str(g), "rate", "quantile", 2)["warnings"], [])

    def test_classify_refusals(self):
        f = self.d / "r.csv"
        f.write_text("region,v,pop\nA,1,0\nB,2,10\n")
        for args in (["--value", "missing", "--method", "equal", "--classes", "2"],
                     ["--value", "v", "--method", "equal", "--classes", "2", "--per-capita", "pop"],
                     ["--value", "v", "--method", "equal", "--classes", "3"]):
            p = run("classify", str(f), *args)
            self.assertEqual(p.returncode, 2, args)
            self.assertEqual(len(p.stderr.strip().splitlines()), 1)

    def test_ledger(self):
        good = {"crs": "EPSG:4326", "source": "Natural Earth", "licence": "public domain", "date": "2024-01",
                "kind": "measured", "points": [{"id": "cairo", "lon": 31.2357, "lat": 30.0444},
                                               {"id": "london", "lon": -0.1276, "lat": 51.5072}]}
        r = G.ledger(good)
        self.assertEqual((r["verdict"], r["points_ok"], r["warnings"]), ("pass", 2, []))
        bad = {"points": [{"id": 1, "lon": 30.04, "lat": 131.2, "source": "x"},
                          {"id": 1, "lon": 0, "lat": 0, "source": "x", "licence": "CC-BY-4.0"}]}
        r = G.ledger(bad)
        rules = {e["rule"] for e in r["errors"]}
        self.assertEqual(rules, {"crs.missing", "coord.range", "licence.missing", "id.duplicate"})
        self.assertIn("swapped", [e for e in r["errors"] if e["rule"] == "coord.range"][0]["message"])
        self.assertIn("coord.null_island", {w["rule"] for w in r["warnings"]})
        merc = G.ledger({"crs": "EPSG:3857", "source": "s", "licence": "l",
                         "points": [{"id": 1, "x": 3.0e7, "y": 0}, {"id": 2, "x": 31.2, "y": 30.0}]})
        self.assertEqual([e["rule"] for e in merc["errors"]], ["coord.range"])
        self.assertIn("coord.units", {w["rule"] for w in merc["warnings"]})

    def test_ledger_cli_and_determinism(self):
        f = self.d / "p.json"
        f.write_text(json.dumps({"crs": "EPSG:4326", "points": [{"id": 1, "lon": 1, "lat": 2}]}))
        a, b = run("ledger", str(f)), run("ledger", str(f))
        self.assertEqual(a.returncode, 0)
        self.assertEqual(a.stdout, b.stdout)
        self.assertEqual(json.loads(a.stdout)["verdict"], "fail")
        f.write_text("[oops")
        self.assertEqual(run("ledger", str(f)).returncode, 2)
        self.assertEqual(sorted(p.name for p in self.d.iterdir()), ["p.json"])

    def test_stdin_csv(self):
        p = subprocess.run([sys.executable, str(SCRIPT), "classify", "-", "--value", "v", "--method", "quantile",
                            "--classes", "2"], input="n,v\na,1\nb,2\nc,3\nd,4\ne,5\n", capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(json.loads(p.stdout)["breaks"], [1, 3, 5])

    def test_self_test(self):
        p = run("--self-test")
        self.assertEqual(p.returncode, 0, p.stderr)


if __name__ == "__main__":
    unittest.main()
