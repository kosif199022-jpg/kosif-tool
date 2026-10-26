"""songreel: the parts that need no audio or video — sections, the excerpt, the shot grid, the clip choice, queries."""
import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import songreel as SR  # noqa: E402


def line(t, words, step=0.5):
    return [{"text": w, "start": round(t + k * step, 3), "end": round(t + k * step + 0.4, 3)} for k, w in enumerate(words)]


LINES = [line(26.5, "مدينة لا تعرف اسمي".split()), line(34, "وباب أفتحه ولا يعرفني".split()),
         line(41.5, "المفتاح في يدي".split()), line(85, "ما أقسى من الغربة".split()), line(93.5, "أن تشتاق لمن لا يراك".split()),
         line(101.5, "ما أقسى من الغربة".split()), line(130, "سأعود سأعود".split())]
DUR = 140.0


class SongreelTests(unittest.TestCase):
    def setUp(self):
        self.lv = np.full(int(DUR / 0.5), 0.3)
        self.lv[int(84 / 0.5):int(110 / 0.5)] = 0.85                 # the loud chorus

    def test_sections(self):
        secs = SR.sections_of(LINES, DUR, self.lv)
        kinds = [s["kind"] for s in secs]
        self.assertEqual(kinds[0], "instrumental")                    # 26.5 s of intro
        self.assertIn("instrumental", kinds[2:])                       # the 41.5 → 85 gap
        chorus = next(s for s in secs if 3 in s["lines"])
        self.assertGreater(chorus["energy"], 0.7)
        self.assertEqual([s["i"] for s in secs], list(range(len(secs))))

    def test_excerpt_prefers_loud_refrain(self):
        secs = SR.sections_of(LINES, DUR, self.lv)
        bt = {"beats": list(np.arange(0, DUR, 0.5)), "downbeats": list(np.arange(0, DUR, 2.0))}
        c = SR.choose_excerpt(LINES, secs, bt, self.lv, 30, DUR, {3, 5}, 3)
        best = c[0]
        self.assertLessEqual(best["start"], 85.0)
        self.assertGreaterEqual(best["end"], 101.5)
        self.assertIn(best["start"], bt["downbeats"])                  # starts on a downbeat
        self.assertLessEqual(best["seconds"], 32.5)
        self.assertLessEqual(len(c), 3)

    def _spec(self):
        secs = SR.sections_of(LINES, DUR, self.lv)
        return {"excerpt": {"start": 82.0, "end": 112.0}, "beats": list(np.arange(0, DUR, 0.5)),
                "loudness": list(self.lv), "sections": secs,
                "lines": [{"t": ln[0]["start"], "end": ln[-1]["end"], "refrain": i in (3, 5)} for i, ln in enumerate(LINES)]}

    def test_shot_grid(self):
        shots = SR.shot_grid(self._spec(), 30)
        self.assertAlmostEqual(sum(s["dur"] for s in shots), 30.0, places=2)
        self.assertTrue(all(0.9 <= s["dur"] <= 4.5 for s in shots[:-1]))
        self.assertIn(round(101.5 - 82.0, 3), [s["t"] for s in shots])  # the payoff (last refrain) is a cut
        loud = [s["dur"] for s in shots if s["energy"] > 0.7]
        quiet = [s["dur"] for s in shots if s["energy"] < 0.5]
        self.assertTrue(loud and float(np.median(loud)) <= 1.6)          # ≈1.4 s target where loud
        self.assertTrue(quiet and float(np.median(quiet)) > float(np.median(loud)))
        self.assertTrue(all(abs(s["dur"] * 30 - round(s["dur"] * 30)) < 0.02 for s in shots))   # whole frames

    def test_assign(self):
        shots = SR.shot_grid(self._spec(), 30)
        clips = [{"file": f"m/s0{k % 3}/c{k}.mp4", "image": False, "seconds": 20.0, "w": 1080, "h": 1920, "luma": 0.3 + 0.01 * k,
                  "warmth": 0.0, "sat": 0.3, "motion": float(k)} for k in range(6)]
        out = SR.assign(shots, clips)
        picks = [s["clip"] for s in out]
        self.assertTrue(all(a != b for a, b in zip(picks, picks[1:])))   # never the same clip twice in a row
        self.assertGreaterEqual(len(set(picks)), 4)                        # the set is used, not one favourite
        short = [{**clips[0], "seconds": 0.5}] + clips[1:]
        self.assertTrue(all(s["clip"] != 0 for s in SR.assign(SR.shot_grid(self._spec(), 30), short)))

    def test_assign_keeps_section_clips_home(self):
        shots = SR.shot_grid(self._spec(), 30)
        secs = sorted({s["section"] for s in shots})
        clips = [{"file": f"m/s{secs[k % len(secs)]:02d}/c{k}.mp4", "image": False, "seconds": 20.0, "w": 720, "h": 1280,
                  "luma": 0.3, "warmth": 0.0, "sat": 0.3, "motion": float(k)} for k in range(3 * len(secs))]
        for s in SR.assign(shots, clips):
            self.assertEqual(Path(clips[s["clip"]]["file"]).parent.name, f"s{s['section']:02d}")

    def test_concepts_and_queries(self):
        c = SR.concepts_of("وظلي وحده يمشي بجانبي والدار لغيري".split())
        self.assertIn("alone", c)
        self.assertIn("home", c)
        for k in c:
            self.assertIn(k, SR.SCENES)

    def test_media_files_prefers_edit_copy(self):
        import tempfile
        d = Path(tempfile.mkdtemp())
        (d / "s01").mkdir()
        for n in ("a.mp4", "a.edit.mp4", "b.mp4", "notes.txt"):
            (d / "s01" / n).write_bytes(b"x")
        names = [p.name for p in SR.media_files(d)]
        self.assertEqual(names, ["a.edit.mp4", "b.mp4"])


if __name__ == "__main__":
    unittest.main(verbosity=1)
