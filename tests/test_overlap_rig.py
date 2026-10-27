"""Overlapping camera rig (tools/overlap_rig.py, playbooks/overlap-camera.md)."""
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("overlap_rig", ROOT / "tools" / "overlap_rig.py")
rig = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rig)


class EaseTests(unittest.TestCase):
    def test_endpoints_and_monotonic(self):
        for o, i, _ in rig.GRAPHS.values():
            vals = [rig.ae_ease(o, i, k / 100) for k in range(101)]
            self.assertEqual(vals[0], 0.0)
            self.assertEqual(vals[-1], 1.0)
            self.assertTrue(all(b >= a - 1e-9 for a, b in zip(vals, vals[1:])))

    def test_peak_position_matches_name(self):
        def peak(o, i):
            return max(range(100), key=lambda k: rig.ae_ease(o, i, (k + 1) / 100) - rig.ae_ease(o, i, k / 100)) / 100

        self.assertLess(peak(*rig.GRAPHS["sharpStartHard"][:2]), 0.05)
        self.assertGreater(peak(*rig.GRAPHS["sharpEndHard"][:2]), 0.95)
        self.assertAlmostEqual(peak(*rig.GRAPHS["sharpMid"][:2]), 0.5, delta=0.1)

    def test_css(self):
        self.assertEqual(rig.css(0.7, 0.75), "cubic-bezier(0.7, 0, 0.25, 1)")


class RigTests(unittest.TestCase):
    def test_reference_rig_passes(self):
        rep = rig.check(rig.REFERENCE_RIG)
        self.assertTrue(rep["ok"], rep["issues"])
        self.assertEqual([h["overlap_frames"] for h in rep["handoffs"]], [20, 13, 20])
        self.assertGreater(rep["min_speed"], 5)

    def test_camera_ends_at_sum_of_offsets(self):
        end = rig.cam_at(rig.REFERENCE_RIG, 200)
        self.assertAlmostEqual(end[0], sum(n["d"] for n in rig.REFERENCE_RIG))

    def test_back_to_back_moves_are_a_stop(self):
        bad = [
            {"axis": "x", "d": -500, "f0": 0, "f1": 30, "graph": [0.7, 0.75]},
            {"axis": "x", "d": -500, "f0": 30, "f1": 60, "graph": [0.7, 0.75]},
        ]
        rep = rig.check(bad)
        self.assertFalse(rep["ok"])

    def test_long_move_covering_a_gap_is_not_a_stop(self):
        nested = [
            {"axis": "x", "d": -2000, "f0": 0, "f1": 100, "graph": [0.7, 0.75]},
            {"axis": "y", "d": -300, "f0": 10, "f1": 30, "graph": [0.7, 0.75]},
            {"axis": "y", "d": -300, "f0": 40, "f1": 60, "graph": [0.7, 0.75]},
        ]
        rep = rig.check(nested)
        self.assertFalse(any("camera stops" in s for s in rep["issues"]), rep["issues"])
        self.assertEqual([h["from"] for h in rep["handoffs"]], [1, 1])

    def test_bad_axis(self):
        rep = rig.check([{"axis": "w", "d": 1, "f0": 0, "f1": 10, "graph": [0.5, 0.5]}])
        self.assertFalse(rep["ok"])


if __name__ == "__main__":
    unittest.main()
