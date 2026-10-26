"""Offline tests for kmotion mimic (scripts/mimic.py): frame-exact boundaries on synthetic frames, shot lengths, the
timeline-plan reader, the gate's plan fallback, colour transfer limits. python tests/test_mimic.py"""
import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import mimic as M  # noqa: E402

FPS = 30.0
H, W = 48, 27


def scene(seed: int, n: int, drift: float = 0.0) -> np.ndarray:
    """n frames of a textured random picture that moves a little (a 'shot')."""
    rng = np.random.default_rng(seed)
    base = rng.integers(0, 120, (H, W * 2, 3)).astype(np.float32)
    base = (base + np.roll(base, 1, 0) + np.roll(base, 1, 1)) / 3
    base += rng.integers(30, 130, 3).astype(np.float32)               # every shot has its own colour cast, like real scenes
    out = []
    for i in range(n):                                                # sensor-like noise instead of whole-pixel jumps
        x = int(i * drift) % W
        out.append(base[:, x:x + W] + rng.normal(0, 1.5, (H, W, 3)).astype(np.float32))
    return np.stack(out)


def film() -> np.ndarray:
    """shot A 60f | cut | B 45f, dissolve 15f into C 60f | dip to black 18f | D 60f."""
    a, b, c, d = scene(1, 60), scene(2, 60), scene(3, 75), scene(4, 60)
    parts = [a, b[:45]]
    k = 15
    mix = np.stack([b[45 + j] * (1 - (j + 1) / (k + 1)) + c[j] * ((j + 1) / (k + 1)) for j in range(k)])
    parts += [mix, c[k:]]
    dip = np.stack([c[-1] * (1 - j / 8) for j in range(9)] + [d[0] * (j / 8) for j in range(9)])
    parts += [dip, d]
    return np.clip(np.concatenate(parts), 0, 255).astype(np.uint8)


class Boundaries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fr = film()
        cls.bd = M.boundaries(cls.fr, FPS)

    def test_three_boundaries_with_types(self):
        types = [b["type"] for b in self.bd["boundaries"]]
        self.assertEqual(types, ["cut", "dissolve", "fadeblack"], self.bd["boundaries"])

    def test_cut_is_frame_exact(self):
        self.assertEqual(self.bd["boundaries"][0]["frame"], 60)

    def test_dissolve_place_and_length(self):
        b = self.bd["boundaries"][1]
        self.assertLessEqual(abs(b["frame"] - 104), 2)               # the last pure-B frame is 104
        self.assertLessEqual(abs(b["dur"] * FPS - 16), 2)            # 15 mixed frames → 16 frame steps

    def test_dip_found(self):
        b = self.bd["boundaries"][2]
        self.assertLessEqual(abs(b["start"] * FPS - 180), 3)
        self.assertLessEqual(abs(b["dur"] * FPS - 17), 4)

    def test_no_suspects_or_flashes(self):
        self.assertEqual(self.bd["flashes"], [])

    def test_shots_cover_the_film(self):
        dur = len(self.fr) / FPS
        shots = M.shots_from(self.bd["boundaries"], dur)
        self.assertEqual(len(shots), 4)
        self.assertEqual(shots[0]["start"], 0.0)
        self.assertAlmostEqual(shots[-1]["end"], dur, places=3)
        for s in shots:                                               # a rebuilt clip spans both of its transitions
            self.assertAlmostEqual(s["clip"], s["end"] - s["start"], places=3)

    def test_exposure_fade_inside_a_shot_is_not_a_cut(self):
        a = scene(7, 90, 0.1)
        ramp = np.stack([a[i] * (0.35 + 0.65 * min(1, i / 40)) for i in range(90)]).astype(np.uint8)
        bd = M.boundaries(np.concatenate([scene(8, 45, 0.1).astype(np.uint8), ramp]), FPS)
        self.assertEqual([b["type"] for b in bd["boundaries"]], ["cut"], bd["boundaries"])


class PlanAndGate(unittest.TestCase):
    def test_planned_boundaries_from_timeline_report(self):
        rep = {"clips": [{"dur": 3.0}, {"dur": 3.0}, {"dur": 3.0}, {"dur": 3.0}],
               "transitions": [{"after_clip": 1, "type": "fade", "dur": 0.5, "at": 5.5},
                               {"after_clip": 2, "type": "fadeblack", "dur": 0.6, "at": 7.9}]}
        plan = M.planned_boundaries(rep)
        self.assertEqual([(p["start"], p["type"]) for p in plan], [(3.0, "cut"), (5.5, "dissolve"), (7.9, "fadeblack")])

    def test_colour_transfer_is_bounded(self):
        look = {"mean": [200, 180, 160], "std": [60, 50, 40]}
        m = M.colour_transfer(look, np.array([20.0, 20, 20]), np.array([2.0, 2, 2]), 1.0)
        for g, o in m.values():
            self.assertTrue(0.6 <= g <= 1.6 and -120 <= o <= 120)

    def test_match_features_flag_source_cuts_and_black(self):
        fr = np.concatenate([scene(1, 10), scene(2, 10), np.zeros((3, H, W, 3), np.float32)]).astype(np.uint8)
        F = M._features(fr)
        self.assertTrue(F["brk"][10])                                 # the source's own cut
        self.assertTrue(F["brk"][-1])                                 # a black frame
        self.assertFalse(F["brk"][1:10].any())


if __name__ == "__main__":
    unittest.main(verbosity=1)
