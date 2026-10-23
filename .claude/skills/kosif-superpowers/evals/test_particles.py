"""Offline tests for particles.py (closed-form seekable bursts, budget rules, SVG frame)."""
import json
import math
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
SCRIPT = SK / "scripts" / "particles.py"
sys.path.insert(0, str(SK / "scripts"))
import particles as P  # noqa: E402


def cfg(**kw):
    return P.make_cfg(P._ns(**kw))


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)


class ParticleTests(unittest.TestCase):
    def test_hash_rng_stateless_and_uniform(self):
        self.assertEqual(P.lowbias32(0), 0)
        self.assertEqual(P.rand01(7, 3, 2), P.rand01(7, 3, 2))
        self.assertNotEqual(P.rand01(7, 3, 2), P.rand01(8, 3, 2))
        xs = [P.rand01(1, i, 0) for i in range(5000)]
        self.assertTrue(all(0 <= x < 1 for x in xs))
        self.assertAlmostEqual(sum(xs) / len(xs), 0.5, delta=0.02)

    def test_t0_all_at_origin(self):
        r = P.burst(cfg(t=0.0, count=30))
        self.assertTrue(all((p["x"], p["y"], p["opacity"]) == (540, 540, 1) for p in r["particles"]))

    def test_ballistic_radius(self):
        # no drag, no gravity, speed exactly 100 px/s: radius at t=0.5 is 50 px
        c = cfg(t=0.5, speed="100,100", drag=0.0, gravity=0.0, life="2,2")
        for p in P.burst(c)["particles"]:
            self.assertAlmostEqual(math.hypot(p["x"] - 540, p["y"] - 540), 50, delta=0.01)

    def test_closed_form_drag(self):
        c = cfg(t=0.5, speed="100,100", drag=1.0, gravity=0.0, life="2,2")
        want = 100 * (1 - math.exp(-0.5))  # 39.3469
        for p in P.burst(c)["particles"]:
            self.assertAlmostEqual(math.hypot(p["x"] - 540, p["y"] - 540), want, delta=0.01)

    def test_gravity_with_and_without_drag(self):
        p = P.particle(cfg(t=1.0, speed="0,0", drag=0.0, gravity=300.0, life="5,5"), 0, 1.0)
        self.assertAlmostEqual(p["y"] - 540, 150, places=3)  # g t^2 / 2
        p = P.particle(cfg(t=1.0, speed="0,0", drag=2.0, gravity=300.0, life="5,5"), 0, 1.0)
        self.assertAlmostEqual(p["y"] - 540, 150 * (1 - (1 - math.exp(-2)) / 2), places=2)  # 85.15

    def test_opacity_curve(self):
        c = cfg(speed="0,0", life="1,1")
        self.assertAlmostEqual(P.particle(c, 0, 0.5)["opacity"], 0.5)
        self.assertAlmostEqual(P.particle(c, 0, 0.25)["opacity"], 0.9375)  # 1 - 4*(0.25^3)
        self.assertEqual(P.particle(c, 0, 1.0)["opacity"], 0)

    def test_seekable_any_order(self):
        c = cfg(count=60, t=0.9, stagger=0.3)
        frame = P.burst(c)["particles"]
        for i in (59, 0, 31):
            self.assertEqual(P.particle(c, i, 0.9), frame[i])
        a = run("burst", "--seed", "4", "--count", "25", "--t", "0.6")
        b = run("burst", "--seed", "4", "--count", "25", "--t", "0.6")
        self.assertEqual(a.returncode, 0, a.stderr)
        self.assertEqual(a.stdout, b.stdout)
        self.assertEqual(json.loads(a.stdout)["count"], 25)

    def test_stagger_hides_unstarted(self):
        c = cfg(count=200, t=0.05, stagger=1.0)
        vis = [p for p in P.burst(c)["particles"] if p["opacity"] > 0]
        self.assertTrue(all(p["delay"] <= 0.05 for p in vis))
        self.assertLess(len(vis), 40)

    def test_budget(self):
        ok = P.budget({"engine": "canvas2d", "kind": "ambient", "count": 300, "sizes": [4, 8, 14],
                       "colors": ["#fff", "#fc0"], "behind_text": True, "seeded": True, "density": "uneven"})
        self.assertEqual((ok["verdict"], ok["violations"], ok["warnings"]), ("pass", [], []))
        bad = P.budget({"engine": "canvas2d", "kind": "burst", "count": 900, "sizes": [2, 4, 8, 14],
                        "colors": ["#fff", "#f00", "#0f0"], "behind_text": False, "seeded": False})
        rules = {v["rule"] for v in bad["violations"]}
        self.assertEqual(rules, {"sizes.max3", "colors.max2", "count.engine", "burst.max40", "seeded", "layer.behind_text"})
        self.assertEqual(P.budget({"engine": "webgl", "count": 20000, "seeded": True})["verdict"], "pass")
        self.assertEqual(P.budget({"engine": "webgl", "count": 20001, "seeded": True})["verdict"], "fail")
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "s.json"
            f.write_text(json.dumps({"engine": "lasers", "count": 1}))
            p = run("budget", str(f))
            self.assertEqual(p.returncode, 2)
            self.assertEqual(len(p.stderr.strip().splitlines()), 1)

    def test_svg_frame(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "f.svg"
            p = run("svg", "--seed", "7", "--count", "12", "--t", "0.3", "--out", str(out))
            self.assertEqual(p.returncode, 0, p.stderr)
            info = json.loads(p.stdout)
            text = out.read_text()
            self.assertTrue(text.startswith("<svg"))
            self.assertEqual(text.count("<circle"), info["visible"])
            self.assertEqual(sorted(Path(d).iterdir()), [out])
        s = run("svg", "--seed", "7", "--count", "12", "--t", "0.3")
        self.assertEqual(s.stdout, text)

    def test_bad_input(self):
        for args in (["burst", "--t", "0.5", "--size", "big"], ["burst", "--t", "-1"],
                     ["burst", "--t", "0.5", "--colors", "red"], ["svg", "--t", "0.1", "--bg", "black"]):
            p = run(*args)
            self.assertEqual(p.returncode, 2, args)
            self.assertEqual(p.stdout, "")

    def test_stdin_spec(self):
        p = subprocess.run([sys.executable, str(SCRIPT), "budget", "-"], input='{"engine": "svg", "count": 301}',
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(json.loads(p.stdout)["verdict"], "fail")

    def test_self_test(self):
        p = run("--self-test")
        self.assertEqual(p.returncode, 0, p.stderr)


if __name__ == "__main__":
    unittest.main()
