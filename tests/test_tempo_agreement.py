"""The two tempo tools must agree: a steady beat gets ~the same BPM from both,
irregular onsets get "no steady beat" from both, and silence/noise never crash.

music_rhythm_engine.py (via audio_cue_mapper.py) and the vendored
pro-video-editor-ffmpeg beat_cuts.py share one steadiness rule
(match >= max(0.60, chance_match + 0.10)). Before that rule, beat_cuts
returned the modal inter-onset gap as a BPM for any input, noise included.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".claude" / "skills" / "kosif-superpowers"
CUE_MAPPER = SKILL / "scripts" / "audio_cue_mapper.py"
RHYTHM = SKILL / "scripts" / "music_rhythm_engine.py"
BEAT_CUTS = (SKILL / "vendor" / "100-superskills" / "skills" / "pro-video-editor-ffmpeg"
             / "scripts" / "beat_cuts.py")
SR = 44100


def write_wav(path: Path, x: np.ndarray) -> Path:
    data = (np.clip(x, -1, 1) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())
    return path


def clicks(times, seconds: float) -> np.ndarray:
    """880 Hz 60 ms clicks over a quiet 110 Hz hum, like the Black Dragon self-test clip."""
    t = np.arange(int(seconds * SR)) / SR
    x = 0.03 * np.sin(2 * np.pi * 110 * t)
    for c in times:
        a = int(c * SR)
        b = min(len(x), a + int(0.06 * SR))
        x[a:b] += 0.5 * np.sin(2 * np.pi * 880 * t[a:b])
    return x


@unittest.skipUnless(shutil.which("ffmpeg"), "beat_cuts.py decodes through ffmpeg")
class TempoAgreementTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="tempo-agreement-")
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def run_tool(self, *args):
        r = subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True, timeout=120)
        self.assertEqual(r.returncode, 0, r.stderr[-800:])

    def both(self, wav: Path):
        cues, grid, beats = (self.dir / f"{wav.stem}.{n}.json" for n in ("cues", "rhythm", "beats"))
        self.run_tool(CUE_MAPPER, wav, "--out", cues)
        self.run_tool(RHYTHM, cues, "--out", grid)
        self.run_tool(BEAT_CUTS, wav, "--out", beats)
        return (json.loads(grid.read_text(encoding="utf-8")),
                json.loads(beats.read_text(encoding="utf-8")))

    def assert_no_steady_beat(self, rhythm, beats):
        self.assertFalse(rhythm["steady_beat"])
        self.assertIsNone(rhythm["candidate_tempo_bpm"])
        self.assertEqual(rhythm["estimated_grid_seconds"], [])
        self.assertFalse(beats["steady_beat"])
        self.assertIsNone(beats["bpm"])
        self.assertIsNone(beats["beat_period_s"])
        for out in (rhythm, beats):
            self.assertGreaterEqual(out["tempo_confidence"], 0.0)
            self.assertLessEqual(out["tempo_confidence"], 1.0)

    def test_120_bpm_clicks_agree_and_are_steady(self):
        for seconds in (6.0, 20.0):
            with self.subTest(seconds=seconds):
                wav = write_wav(self.dir / f"click120_{int(seconds)}.wav",
                                clicks(np.arange(0, seconds, 0.5), seconds))
                rhythm, beats = self.both(wav)
                self.assertTrue(rhythm["steady_beat"])
                self.assertTrue(beats["steady_beat"])
                self.assertAlmostEqual(rhythm["candidate_tempo_bpm"], 120, delta=2)
                self.assertAlmostEqual(beats["bpm"], 120, delta=2)
                self.assertAlmostEqual(rhythm["candidate_tempo_bpm"], beats["bpm"], delta=2)
                self.assertGreater(rhythm["tempo_confidence"], 0.5)
                self.assertGreater(beats["tempo_confidence"], 0.5)
                self.assertTrue(rhythm["estimated_grid_seconds"])
                # Existing output keys stay in place for callers.
                for key in ("bpm", "beats_s", "cut_points_s", "beat_period_s", "energy_fps", "energy"):
                    self.assertIn(key, beats)
                for key in ("tempo_hypotheses", "verified_bpm", "measured_transients_seconds"):
                    self.assertIn(key, rhythm)

    def test_irregular_onsets_report_no_steady_beat_in_both(self):
        for seed in (1, 2, 3):
            with self.subTest(seed=seed):
                rng = np.random.default_rng(seed)
                times = np.cumsum(rng.uniform(0.18, 1.3, 60))
                times = times[times < 19.5]
                wav = write_wav(self.dir / f"irregular_{seed}.wav", clicks(times, 20.0))
                rhythm, beats = self.both(wav)
                self.assertGreater(len(beats["beats_s"]), 10, "onsets are still detected")
                self.assert_no_steady_beat(rhythm, beats)

    def test_silence_and_noise_do_not_crash_or_invent_a_beat(self):
        rng = np.random.default_rng(7)
        signals = {
            "silence": np.zeros(SR * 3),
            "white_noise": rng.normal(0, 0.2, SR * 8),
            # Low-frequency random walk: with the old 0.3 s refractory it produced a fake ~165 BPM.
            "brown_noise": np.cumsum(rng.normal(0, 0.02, SR * 8)) * 0.02,
        }
        for name, x in signals.items():
            with self.subTest(signal=name):
                rhythm, beats = self.both(write_wav(self.dir / f"{name}.wav", x))
                self.assert_no_steady_beat(rhythm, beats)


if __name__ == "__main__":
    unittest.main()
