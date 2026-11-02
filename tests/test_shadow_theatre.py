"""Tests for the KOSIF Shadow Theatre skill: grammar checks, body kinematics, depth, iris and a tiny real render."""
import copy
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".claude/skills/kosif-shadow-theatre"
sys.path.insert(0, str(SKILL / "scripts"))
import shadow_engine as E  # noqa: E402
import shadow_theatre as ST  # noqa: E402

DEMO = SKILL / "scenes/lantern-keeper.json"


def tiny(spec):
    s = copy.deepcopy(spec)
    s.update(width=216, height=384, fps=6)
    return s


class Grammar(unittest.TestCase):
    def test_demo_passes(self):
        self.assertEqual(ST.check_spec(ST.load_spec(DEMO)), [])

    def test_gap_and_missing_body_build_fail(self):
        s = ST.load_spec(DEMO)
        s["scenes"][1]["start"] += 0.5
        for sc in s["scenes"]:
            sc["techniques"] = [t for t in sc.get("techniques", []) if t != "body-build"]
        errs = " | ".join(ST.check_spec(s))
        self.assertIn("gap or overlap", errs)
        self.assertIn("no body-build", errs)

    def test_unknown_pose_is_reported(self):
        s = ST.load_spec(DEMO)
        s["scenes"][0]["actors"][1]["keys"][0]["pose"] = "moonwalk"
        self.assertTrue(any("moonwalk" in e for e in ST.check_spec(s)))


class Body(unittest.TestCase):
    def test_arms_up_puts_wrists_above_head(self):
        j, _ = E.body_skeleton(E.resolve_pose("arms_up"), "plain", 100, 1)
        self.assertLess(j["wr_a"][1], j["head"][1])
        self.assertLess(j["wr_b"][1], j["head"][1])

    def test_facing_mirrors(self):
        a, _ = E.body_skeleton(E.resolve_pose("lunge"), "plain", 100, 1)
        b, _ = E.body_skeleton(E.resolve_pose("lunge"), "plain", 100, -1)
        self.assertAlmostEqual(a["ft_a"][0], -b["ft_a"][0], places=6)

    def test_pose_blend_is_halfway(self):
        p = E.mix_pose(("stand", "arms_up", 0.5))
        self.assertAlmostEqual(p["arm_a"], (E.POSES["stand"]["arm_a"] + E.POSES["arms_up"]["arm_a"]) / 2)


class Render(unittest.TestCase):
    def setUp(self):
        self.r = E.ShadowRenderer(tiny(ST.load_spec(DEMO)))

    def test_deterministic_and_has_shadow(self):
        a, b = self.r.render(8.0).rgb, self.r.render(8.0).rgb
        self.assertTrue(np.array_equal(a, b))
        inside = a[60:320, 20:196].mean(2)
        self.assertGreater((inside < 30).mean(), 0.03)  # silhouettes present
        self.assertGreater((inside > 80).mean(), 0.2)   # lit sky present

    def test_depth_grows_and_softens(self):
        actor = {"type": "human", "keys": [{"t": 0, "x": 0.5, "y": 0.9, "pose": "stand"}]}
        near = copy.deepcopy(actor)
        near["keys"][0]["depth"] = 0.8
        m0, _, _ = self.r.actor_layer(actor, 0)
        m1, _, _ = self.r.actor_layer(near, 0)
        self.assertGreater((m1 > 0.5).sum(), 2 * (m0 > 0.5).sum())
        soft = lambda m: ((m > 0.05) & (m < 0.95)).sum() / max(1, (m > 0.5).sum())
        self.assertGreater(soft(m1), soft(m0))

    def test_iris_closed_is_dark(self):
        f = self.r.render(21.99).rgb  # arch iris fully closed at the end
        self.assertLess(f[60:320, 20:196].mean(), 25)


@unittest.skipUnless(shutil.which("ffmpeg"), "ffmpeg missing")
class Film(unittest.TestCase):
    def test_tiny_render_with_score(self):
        s = tiny(ST.load_spec(DEMO))
        for sc in s["scenes"]:
            sc["start"], sc["end"] = sc["start"] / 11, sc["end"] / 11
            for a in sc.get("actors", []):
                for k in a.get("keys", []):
                    k["t"] /= 11
            for key in ("iris", "spot"):
                for k in (sc.get(key) or {}).get("keys", []) + (sc.get(key) or {}).get("r_keys", []):
                    k["t"] /= 11
            sc.pop("cues", None)
        s["duration"] = 2.0
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "s.json"
            p.write_text(json.dumps(s))
            out = Path(d) / "f.mp4"
            rc = ST.main(["render", str(p), "--out", str(out), "--force"])
            self.assertEqual(rc, 0)
            info = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height",
                                              "-of", "json", str(out)], capture_output=True, text=True).stdout)
            kinds = sorted(x["codec_type"] for x in info["streams"])
            self.assertEqual(kinds, ["audio", "video"])
            self.assertEqual(info["streams"][0].get("width") or info["streams"][1].get("width"), 216)


if __name__ == "__main__":
    unittest.main()
