"""Station 6 «ينفّذ» — dm_render.py end-to-end on synthetic clips (< 2 minutes)."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / ".claude" / "skills" / "kosif-dragon-montage" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import dm_common as dm  # noqa: E402


WORDS_C01 = [("اهلا", 0.3, 0.7), ("بيكم", 0.75, 1.1), ("في", 1.2, 1.35), ("التنين", 1.4, 1.9),
             ("الاسود", 1.95, 2.4), ("النهارده", 3.3, 3.9), ("هنعمل", 4.0, 4.5), ("مونتاج", 4.55, 5.2)]
WORDS_C02 = [("شوف", 1.1, 1.5), ("الفرق", 1.55, 2.1), ("بنفسك", 2.2, 2.8)]


def _words(ws):
    return [{"w": w, "start": a, "end": b, "conf": 0.9} for w, a, b in ws]


def make_job(j: Path):
    c1 = dm.make_test_clip(j / "media" / "c01.mp4", 6.0, tone=330, size="640x360")
    c2 = dm.make_test_clip(j / "media" / "c02.mp4", 6.0, tone=550, size="480x640", color="rgbtestsrc")
    music = j / "media" / "bed.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "sine=frequency=220:duration=4",
                    "-ac", "2", str(music)], check=True)
    analysis = dm.new("analysis", clips=[
        {"id": "c01", "path": str(c1), "duration": 6.0, "width": 640, "height": 360, "fps": 30, "has_audio": True,
         "shots": [{"id": "c01-s001", "start": 0, "end": 3, "face_center": [0.4, 0.5]}], "words": _words(WORDS_C01)},
        {"id": "c02", "path": str(c2), "duration": 6.0, "width": 480, "height": 640, "fps": 30, "has_audio": True,
         "shots": [], "words": _words(WORDS_C02)}],
        music={"path": None, "bpm": None, "beats": [], "downbeats": []}, tools_used=["ffprobe"], missing=[])
    dm.write(j, "analysis", analysis)
    # 4 events: cut, cut, xfade (0.4s), cut ; total = 2.5 + 2.0 + 2.0 + 1.5 - 0.4 = 7.6
    events = [
        {"id": "e001", "clip": "c01", "src_in": 0.2, "src_out": 2.7, "rec_in": 0.0, "speed": 1.0,
         "transition_in": {"id": "cut"}, "camera": {"id": "punch-in", "scale": 1.1}, "reason": "hook line",
         "shot": "c01-s001"},
        {"id": "e002", "clip": "c02", "src_in": 1.0, "src_out": 3.0, "rec_in": 2.5, "speed": 1.0,
         "transition_in": {"id": "cut"}, "camera": {"id": "slow-push"}, "reason": "reaction"},
        {"id": "e003", "clip": "c01", "src_in": 3.2, "src_out": 5.2, "rec_in": 4.1, "speed": 1.0,
         "transition_in": {"id": "xfade-fade", "seconds": 0.4}, "camera": {"id": "none"}, "reason": "payoff"},
        {"id": "e004", "clip": "c02", "src_in": 3.5, "src_out": 5.0, "rec_in": 6.1, "speed": 1.0,
         "transition_in": {"id": "cut"}, "camera": {"id": "ken-burns"}, "reason": "cta"},
    ]
    edl = dm.new("edl", width=1080, height=1920, fps=30, events=events,
                 audio={"music": {"path": "media/bed.wav", "gain_db": -18, "duck_under_speech_db": -10},
                        "voice_from": "events", "target_lufs": -14},
                 captions={"enabled": True, "style": "karaoke", "words_from": "analysis"},
                 grade={"id": "cinematic"}, duration=7.6)
    dm.write(j, "edl", edl)
    import dm_render
    doc = dm_render.render(j, [], preview=False, fast=True)
    return doc


def _probe(p):
    return dm.probe(p)


@unittest.skipUnless(dm.have("ffmpeg") and dm.have("ffprobe"), "ffmpeg missing")
class DragonMontageRender(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory(prefix="dm_render_")
        cls.j = Path(cls._tmp.name)
        cls.doc = make_job(cls.j)

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def test_final_video(self):
        j, doc = self.j, self.doc
        final = j / doc["final"]
        assert final.is_file()
        pr = _probe(final)
        v = next(s for s in pr["streams"] if s["codec_type"] == "video")
        assert (v["width"], v["height"]) == (1080, 1920)
        assert any(s["codec_type"] == "audio" for s in pr["streams"])
        assert abs(float(pr["format"]["duration"]) - 7.6) <= 0.3

    def test_loudness_and_verify(self):
        j, doc = self.j, self.doc
        ver = doc["verify"]
        assert ver["tool"] == "verify_video"
        assert ver["lufs"] is not None and abs(ver["lufs"] - (-14)) <= 1.5
        assert ver["true_peak"] is not None and ver["true_peak"] <= -1.0
        self.assertTrue(ver["pass"] is True, ver)

    def test_captions_and_project(self):
        j, doc = self.j, self.doc
        srt = j / doc["captions"]
        assert srt.is_file() and "-->" in srt.read_text(encoding="utf-8")
        assert "التنين" in srt.read_text(encoding="utf-8")
        ass = (j / doc["captions_ass"]).read_text(encoding="utf-8")
        assert "Dialogue:" in ass and "\\c&H" in ass
        words = json.loads((j / "render" / "words.json").read_text(encoding="utf-8"))["words"]
        # e003 starts at 4.1 (after the 0.4s xfade) at source 3.2: "النهارده" 3.3 → 4.2, but words in the
        w = next(x for x in words if x["word"] == "النهارده")
        assert abs(w["start"] - 4.3) < 0.15  # first half of an xfade are moved to its midpoint (4.3)
        assert doc["project"] == "render/project.fcpxml" and (j / doc["project"]).is_file()

    def test_render_json_and_receipts(self):
        j, doc = self.j, self.doc
        again = dm.read(j, "render")
        assert again["final"] == doc["final"] and "verify" in again
        rec = dm.receipts(j)
        tools = {r["tool"] for r in rec}
        assert {"ffmpeg.render", "ffmpeg.loudnorm-measure", "ffmpeg.loudnorm-apply", "verify_video", "nle_export"} <= tools
        assert all(r["rc"] == 0 for r in rec if r["tool"].startswith("ffmpeg"))
        assert [e["transition"] for e in doc["events"]] == ["cut", "cut", "fade", "cut"]

    def test_z_preview_cli(self):
        j = self.j
        res = subprocess.run([sys.executable, str(SCRIPTS / "dm_render.py"), "render", "--job", str(j), "--preview",
                              "--extra-ratios", "1:1", "--no-export"], capture_output=True, text=True, timeout=300)
        self.assertTrue(res.returncode == 0, res.stdout + res.stderr)
        out = json.loads(res.stdout.strip().splitlines()[-1])
        assert out["final"] == "render/preview.mp4"
        pr = _probe(j / "render" / "preview.mp4")
        v = next(s for s in pr["streams"] if s["codec_type"] == "video")
        assert (v["width"], v["height"]) == (360, 640)
        sq = _probe(j / "render" / "preview_1x1.mp4")
        v = next(s for s in sq["streams"] if s["codec_type"] == "video")
        assert v["width"] == v["height"]


if __name__ == "__main__":
    unittest.main()
