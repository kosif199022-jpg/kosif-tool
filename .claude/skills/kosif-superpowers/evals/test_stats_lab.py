"""Offline known-answer tests for scripts/stats_lab.py (abtest, samplesize, describe, lots)."""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import stats_lab as S  # noqa: E402


def run(args):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            rc = S.main(args)
        except SystemExit as e:
            rc = e.code
    return rc, out.getvalue(), err.getvalue()


class StatsLabTests(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.d = Path(self.t.name)

    def tearDown(self):
        self.t.cleanup()

    def w(self, name, text):
        p = self.d / name
        p.write_text(text, encoding="utf-8")
        return str(p)

    def test_abtest_known_answer(self):
        # pooled p=0.115, SE0=sqrt(.115*.885*.002)=0.0142671 -> z=0.03/SE0=2.10274, p=0.035488
        r = S.abtest((1000, 100), (1000, 130))
        self.assertAlmostEqual(r["z"], 2.1027, places=4)
        self.assertAlmostEqual(r["p_value"], 0.035488, places=5)
        # Wald: SE1=sqrt(.09/1000+.1131/1000)=0.0142513 -> 0.03 +- 0.027932
        self.assertAlmostEqual(r["ci_difference"][0], 0.002068, places=5)
        self.assertAlmostEqual(r["ci_difference"][1], 0.057932, places=5)
        # log RR: ln 1.3 +- 1.96*sqrt(.9/100+.87/130) -> exp(...) - 1
        self.assertAlmostEqual(r["lift"], 0.3, places=6)
        self.assertAlmostEqual(r["ci_lift"][0], 0.016984, places=5)
        self.assertAlmostEqual(r["ci_lift"][1], 0.661776, places=5)
        self.assertEqual(r["verdict"], "B_BETTER")
        same = S.abtest((500, 50), (500, 50))
        self.assertEqual(same["p_value"], 1.0)
        self.assertEqual(same["verdict"], "NO_SIGNIFICANT_DIFFERENCE")

    def test_samplesize_known_answer(self):
        # 10% -> 12%: (1.959964*sqrt(2*.11*.89) + 0.841621*sqrt(.09+.1056))^2 / .02^2 = 3840.9 -> 3841
        r = S.samplesize(0.10, 0.20)
        self.assertEqual(r["n_per_arm"], 3841)
        self.assertEqual(r["n_total"], 7682)
        self.assertEqual(S.samplesize(0.10, 0.02, absolute=True)["n_per_arm"], 3841)
        self.assertGreater(S.samplesize(0.10, 0.20, power=0.9)["n_per_arm"], 3841)

    def test_describe_known_answer(self):
        f = self.w("d.csv", "x,label\n1,a\n2,b\n3,c\n4,d\n100,e\nn/a,f\n")
        r = S.describe(f, "x")
        self.assertEqual((r["n"], r["skipped_non_numeric"]), (5, 1))
        self.assertEqual((r["mean"], r["median"], r["q1"], r["q3"], r["iqr"]), (22.0, 3.0, 2.0, 4.0, 2.0))
        self.assertAlmostEqual(r["sd"], 43.617657, places=5)  # sqrt(7610/4)
        self.assertEqual(r["fences"], [-1.0, 7.0])
        self.assertEqual(r["outliers"], [{"row": 6, "value": 100.0}])
        g = self.w("t.csv", 'v\n"1,000"\n2000\n')
        self.assertEqual(S.describe(g, "v")["mean"], 1500.0)

    def test_lots_methods(self):
        f = self.w("t.csv", "date,side,qty,price,fee\n2024-01-01,buy,10,100,10\n2024-02-01,buy,10,200,0\n"
                            "2024-03-01,sell,15,300,5\n")
        # fifo basis = 10*101 + 5*200 = 2010; proceeds 4500-5 = 4495
        self.assertEqual(S.lots(f, "fifo")["realized_total"], "2485")
        # lifo/hifo basis = 10*200 + 5*101 = 2505
        self.assertEqual(S.lots(f, "lifo")["realized_total"], "1990")
        r = S.lots(f, "hifo")
        self.assertEqual(r["realized_total"], "1990")
        self.assertEqual(r["open_lots"], [{"asset": "-", "lot_row": 2, "date": "2024-01-01", "qty": "5", "unit_cost": "101"}])

    def test_lots_assets_and_oversell(self):
        f = self.w("t.csv", "date,side,qty,price,asset\n2024-01-02,sell,1,50,BTC\n2024-01-01,buy,2,10,BTC\n"
                            "2024-01-01,buy,1,5,ETH\n")
        r = S.lots(f, "fifo")  # rows are sorted by date, so the buy comes first
        self.assertEqual(r["realized_by_asset"], {"BTC": "40"})
        bad = self.w("b.csv", "date,side,qty,price\n2024-01-01,buy,1,10\n2024-01-02,sell,2,10\n")
        rc, out, err = run(["lots", bad])
        self.assertEqual(rc, 2)
        self.assertEqual(out, "")
        self.assertEqual(len(err.strip().splitlines()), 1)

    def test_cli_bad_input_one_line(self):
        for args in (["abtest", "--a", "10,20", "--b", "10,1"], ["samplesize", "--base", "1.5", "--mde", "0.1"],
                     ["describe", str(self.d / "missing.csv"), "--col", "x"], ["nope"], ["lots", "x", "--method", "avg"]):
            rc, out, err = run(args)
            self.assertEqual(rc, 2, args)
            self.assertEqual(len(err.strip().splitlines()), 1, (args, err))

    def test_cli_json_text_and_determinism(self):
        a = run(["abtest", "--a", "1000,100", "--b", "1000,130"])
        b = run(["abtest", "--a", "1000,100", "--b", "1000,130"])
        self.assertEqual(a, b)
        self.assertEqual(json.loads(a[1])["verdict"], "B_BETTER")
        rc, out, _ = run(["samplesize", "--base", "0.1", "--mde", "0.2", "--text"])
        self.assertEqual(rc, 0)
        self.assertIn("3841", out)
        self.assertEqual(run(["--self-test"])[0], 0)

    def test_stdin_csv(self):
        from unittest import mock
        with mock.patch("sys.stdin", io.StringIO("date,side,qty,price,fee\n2024-01-05,buy,10,100,5\n"
                                                 "2024-03-01,buy,10,150,5\n2024-06-01,sell,12,200,4\n")):
            rc, out, _ = run(["lots", "-", "--method", "fifo"])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out)["realized_total"], "1090")  # 2400-4 - (10*100.5 + 2*150.5)


if __name__ == "__main__":
    unittest.main()
