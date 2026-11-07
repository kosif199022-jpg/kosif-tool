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


class CaptionSafeAreaAndFaceCrop(unittest.TestCase):
    """Platform UI covers the lower band: 9:16 captions ≥ 0.22·H from the bottom, 16:9 ≥ 0.08·H."""

    def _style(self, style="karaoke"):
        import dm_render
        return dm_render, dm_render.caption_style(style, None)

    def test_safe_area_table_in_caption_styles(self):
        sa = json.loads((SCRIPTS.parent / "data" / "caption_styles.json").read_text(encoding="utf-8"))["safe_area"]
        self.assertGreaterEqual(sa["9:16"]["bottom"], 0.22)
        self.assertGreaterEqual(sa["16:9"]["bottom"], 0.08)

    def test_margin_floor_per_aspect(self):
        R, st = self._style()
        for W, H, need in ((1080, 1920, 0.22), (720, 1280, 0.22), (1920, 1080, 0.08), (1080, 1350, 0.14)):
            with self.subTest(size=f"{W}x{H}"):
                self.assertGreaterEqual(R.caption_margin_v(st, W, H) / H, need)
        R, clean = self._style("clean")
        self.assertGreaterEqual(R.caption_margin_v(clean, 1080, 1920) / 1920, 0.22)
        self.assertGreaterEqual(R.caption_margin_v(st, 1080, 1920, 0.30) / 1920, 0.30)   # review fix wins
        R, punchy = self._style("punchy")
        self.assertEqual(int(punchy["ass"]["Alignment"]), 5)                            # centre: no floor needed

    def test_written_ass_honours_safe_area(self):
        import re
        R, st = self._style()
        st["font"] = "Cairo"
        with tempfile.TemporaryDirectory() as td:
            for W, H, need in ((1080, 1920, 0.22), (1920, 1080, 0.08)):
                f = Path(td) / f"c{W}.ass"
                R.write_ass(f, [{"word": "اهلا", "start": 0.1, "end": 0.5}], st, W, H)
                txt = f.read_text(encoding="utf-8")
                res_y = int(re.search(r"PlayResY: (\d+)", txt).group(1))
                mv = int(re.search(r"^Style: Cap,.*,(\d+),-?\d+$", txt, re.M).group(1))
                self.assertGreaterEqual(mv / res_y, need, txt.splitlines()[11])

    def test_face_center_hook(self):
        import dm_render as R
        clip = {"shots": [{"id": "c01-s001", "start": 0, "end": 3, "face_center": [0.8, 0.3]},
                          {"id": "c01-s002", "start": 3, "end": 6, "faces_box": [0.1, 0.2, 0.2, 0.2]}]}
        self.assertEqual(R.face_center({"shot": "c01-s001", "src_in": 0.5}, clip), (0.8, 0.3))
        self.assertAlmostEqual(R.face_center({"src_in": 4.0}, clip)[0], 0.2)
        self.assertEqual(R.face_center({"src_in": 9.0}, clip), (0.5, 0.5))


@unittest.skipUnless(dm.have("ffmpeg") and dm.have("ffprobe"), "ffmpeg missing")
class FaceCenteredCrop(unittest.TestCase):
    """A bright square at x=0.8 of a 16:9 source must land in the middle of the 9:16 output."""

    def test_crop_centres_on_face(self):
        import dm_render
        with tempfile.TemporaryDirectory(prefix="dm_crop_") as td:
            j = Path(td)
            src = j / "wide.mp4"
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "color=c=black:s=640x360:d=2:r=30",
                            "-f", "lavfi", "-i", "sine=frequency=300:duration=2", "-vf",
                            "drawbox=x=492:y=60:w=40:h=40:color=white:t=fill", "-c:v", "libx264", "-preset",
                            "ultrafast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(src)], check=True)
            dm.write(j, "analysis", dm.new("analysis", clips=[
                {"id": "c01", "path": str(src), "duration": 2.0, "width": 640, "height": 360, "fps": 30,
                 "has_audio": True, "shots": [{"id": "c01-s001", "start": 0, "end": 2, "faces": 1,
                                               "face_center": [0.8, 0.222]}], "words": []}],
                music={"path": None, "bpm": None, "beats": [], "downbeats": []}, tools_used=[], missing=[]))
            dm.write(j, "edl", dm.new("edl", width=360, height=640, fps=30, events=[
                {"id": "e001", "clip": "c01", "src_in": 0.0, "src_out": 1.5, "rec_in": 0.0, "speed": 1.0,
                 "transition_in": {"id": "cut"}, "camera": {"id": "none"}, "reason": "t", "shot": "c01-s001"}],
                audio={"music": {"path": None}, "voice_from": "events", "target_lufs": -14},
                captions={"enabled": False}, grade={"id": "none"}, duration=1.5))
            doc = dm_render.render(j, [], fast=True, do_verify=False, do_export=False)
            raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", "0.5", "-i", str(j / doc["final"]), "-frames:v", "1",
                                  "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True, check=True).stdout
            W, H = 360, 640
            cols = [x for x in range(W) if max(raw[y * W + x] for y in range(0, 300, 4)) > 128]
            self.assertTrue(cols, "box not in frame")
            cx = (cols[0] + cols[-1]) / 2 / W
            self.assertAlmostEqual(cx, 0.5, delta=0.08)


@unittest.skipUnless(dm.have("ffmpeg") and dm.have("ffprobe"), "ffmpeg missing")
class TruePeakLimiter(unittest.TestCase):
    """A hot, clipped source must come out under edl.audio.limiter_tp (set by the review fix loop)."""

    def test_limiter_tp_honoured(self):
        import dm_render
        with tempfile.TemporaryDirectory(prefix="dm_tp_") as td:
            j = Path(td)
            src = j / "hot.mp4"
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "color=c=gray:s=320x180:d=4:r=30",
                            "-f", "lavfi", "-i", "aevalsrc='0.99*sgn(sin(2*PI*180*t))*(0.3+0.7*mod(floor(t*6),2))':s=48000:d=4",
                            "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-c:a", "aac",
                            "-shortest", str(src)], check=True)
            dm.write(j, "analysis", dm.new("analysis", clips=[
                {"id": "c01", "path": str(src), "duration": 4.0, "width": 320, "height": 180, "fps": 30,
                 "has_audio": True, "shots": [], "words": []}],
                music={"path": None, "bpm": None, "beats": [], "downbeats": []}, tools_used=[], missing=[]))
            dm.write(j, "edl", dm.new("edl", width=180, height=320, fps=30, events=[
                {"id": "e001", "clip": "c01", "src_in": 0.0, "src_out": 3.5, "rec_in": 0.0, "speed": 1.0,
                 "transition_in": {"id": "cut"}, "camera": {"id": "none"}, "reason": "t"}],
                audio={"music": {"path": None}, "voice_from": "events", "target_lufs": -14, "limiter_tp": -1.5},
                captions={"enabled": False}, grade={"id": "none"}, duration=3.5))
            doc = dm_render.render(j, [], fast=True, do_verify=False, do_export=False)
            peak = dm_render.measure_true_peak(j, j / doc["final"])
            self.assertLessEqual(peak, -1.5)
            self.assertEqual(doc["loudness"]["true_peak_ceiling"], -1.5)


# ----------------------------------------------------------------------------- regression: reviewer findings
def _ramp_clip(path: Path, seconds: float = 10.0) -> Path:
    """Grey level = 20·t (so a frame tells which source second it came from) + a steady 440 Hz tone."""
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i",
                    f"color=c=black:s=64x64:r=30:d={seconds},format=gray,geq=lum='20*T',format=yuv420p",
                    "-f", "lavfi", "-i", f"sine=frequency=440:duration={seconds}", "-c:v", "libx264",
                    "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(path)],
                   check=True, timeout=120)
    return path


def _pcm(path: Path) -> list[float]:
    """Mono 8 kHz samples of a file's audio."""
    import array
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", "8000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    a = array.array("h")
    a.frombytes(raw)
    return [x / 32768.0 for x in a]


def _rms(xs) -> float:
    return (sum(x * x for x in xs) / max(1, len(xs))) ** 0.5


def _luma_at(path: Path, t: float, w: int, h: int) -> float:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(path), "-frames:v", "1",
                          "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True, check=True).stdout
    return sum(raw[:w * h]) / (w * h)


def _job(j: Path, clip: Path, events: list[dict], *, W=64, H=112, duration=60.0, grade="none", music=None) -> None:
    dm.write(j, "analysis", dm.new("analysis", clips=[
        {"id": "c01", "path": str(clip), "duration": duration, "width": 64, "height": 64, "fps": 30,
         "has_audio": True, "shots": [], "words": []}],
        music={"path": None, "bpm": None, "beats": [], "downbeats": []}, tools_used=[], missing=[]))
    for ev in events:
        ev.setdefault("rec_in", 0.0)
        ev.setdefault("reason", "t")
        ev.setdefault("camera", {"id": "none"})
        ev.setdefault("transition_in", {"id": "cut"})
    edl = dm.new("edl", width=W, height=H, fps=30, events=events,
                 audio={"music": {"path": music}, "voice_from": "events", "target_lufs": -14},
                 captions={"enabled": False}, grade={"id": grade}, duration=0.0)
    import dm_edl
    dm_edl.reflow(edl)
    dm.write(j, "edl", edl)


@unittest.skipUnless(dm.have("ffmpeg") and dm.have("ffprobe"), "ffmpeg missing")
class OutOfOrderSingleSource(unittest.TestCase):
    """One source, events out of source order, joined by crossfades: acrossfade used to output nothing
    (shared [0:a] → silence hidden by apad). Each event is now its own -ss/-t input."""

    @classmethod
    def setUpClass(cls):
        import dm_render
        cls._tmp = tempfile.TemporaryDirectory(prefix="dm_ooo_")
        cls.j = Path(cls._tmp.name)
        clip = _ramp_clip(cls.j / "src.mp4", 10.0)
        cls.src = [(4.3, 8.0), (0.3, 4.0), (6.0, 9.0), (1.0, 3.0)]
        xf = {"id": "xfade-fade", "seconds": 0.3}
        _job(cls.j, clip, [
            {"id": f"e{i + 1:03d}", "clip": "c01", "src_in": a, "src_out": b,
             "transition_in": dict(xf) if i in (1, 3) else {"id": "cut"}} for i, (a, b) in enumerate(cls.src)],
            duration=10.0)
        cls.doc = dm_render.render(cls.j, [], fast=True, do_verify=False, do_export=False)
        cls.final = cls.j / cls.doc["final"]

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def test_audio_never_silent(self):
        pcm = _pcm(self.final)
        win = 800                                    # 0.1 s windows
        quiet = [i * 0.1 for i in range(len(pcm) // win) if _rms(pcm[i * win:(i + 1) * win]) < 0.02]
        self.assertGreater(len(pcm) / 8000, 11.0)
        self.assertEqual(quiet, [], f"silent windows at {quiet[:10]}")

    def test_video_frames_come_from_the_right_source_time(self):
        for ev, (a, b) in zip(self.doc["events_out"], self.src):
            mid_out = (ev["out_in"] + ev["out_out"]) / 2
            src_t = a + (mid_out - ev["out_in"])
            with self.subTest(ev=ev["id"]):
                self.assertAlmostEqual(_luma_at(self.final, mid_out, 64, 112), 20 * src_t, delta=4)

    def test_events_out_match_reflow_and_file(self):
        import dm_edl
        edl = dm_edl.reflow(dm.read(self.j, "edl"))
        eo = self.doc["events_out"]
        self.assertEqual([e["id"] for e in eo], [e["id"] for e in edl["events"]])
        for e, ev in zip(eo, edl["events"]):
            self.assertAlmostEqual(e["out_in"], ev["rec_in"], delta=1 / 30 + 1e-6)
        self.assertAlmostEqual(eo[-1]["out_out"], edl["duration"], delta=1 / 30 + 1e-6)
        self.assertAlmostEqual(eo[-1]["out_out"], self.doc["duration"], delta=1e-3)
        dur = float(dm.probe(self.final)["format"]["duration"])
        self.assertAlmostEqual(dur, self.doc["duration"], delta=0.1)


class TimingSingleSourceOfTruth(unittest.TestCase):
    """dm_render.plan_timeline follows dm_edl.reflow exactly (40 events, mixed xfades: was 19.5 vs 19.33 s)."""

    def test_forty_events(self):
        import random
        import dm_edl
        import dm_render
        rnd = random.Random(7)
        evs, t = [], 0.0
        for i in range(40):
            ln = rnd.choice([0.2, 0.33, 0.41, 0.5, 0.77, 1.0])
            tr = {"id": "xfade-fade", "seconds": rnd.choice([0.1, 0.25, 0.4, 0.6])} if i % 3 == 1 else {"id": "cut"}
            evs.append({"id": f"e{i + 1:03d}", "clip": "c01", "src_in": round(t, 3), "src_out": round(t + ln, 3),
                        "rec_in": 0.0, "speed": rnd.choice([1.0, 1.0, 1.25]), "transition_in": tr, "reason": "t"})
            t += ln
        edl = dm.new("edl", width=64, height=64, fps=30, events=evs, audio={}, captions={}, duration=0.0)
        ref = dm_edl.reflow(json.loads(json.dumps(edl)))
        plan = dm_render.plan_timeline(edl, 30.0)
        self.assertAlmostEqual(plan[-1]["end_f"] / 30, ref["duration"], delta=1 / 30)
        for p, ev in zip(plan, ref["events"]):
            self.assertAlmostEqual(p["start"], ev["rec_in"], delta=1 / 30 + 1e-6)
            self.assertEqual(p["trans"] != "cut", dm_edl.overlap(ev) * 30 >= 0.5 and p["td_f"] >= 1)
        for a, b in zip(plan, plan[1:]):            # contiguous: next start = previous end − overlap
            self.assertEqual(b["start_f"], a["end_f"] - b["td_f"])


@unittest.skipUnless(dm.have("ffmpeg") and dm.have("ffprobe"), "ffmpeg missing")
class DirectorFieldsAndClamp(unittest.TestCase):
    """ev.mute → silence, ev.grade → that event only, src_out past the media → clamped + warned."""

    def test_mute_grade_and_clamp(self):
        import dm_render
        with tempfile.TemporaryDirectory(prefix="dm_fields_") as td:
            j = Path(td)
            clip = dm.make_test_clip(j / "c.mp4", 4.0, size="160x90")
            _job(j, clip, [
                {"id": "e001", "clip": "c01", "src_in": 0.0, "src_out": 1.5},
                {"id": "e002", "clip": "c01", "src_in": 0.2, "src_out": 1.7, "mute": True, "grade": {"id": "mono"}},
                {"id": "e003", "clip": "c01", "src_in": 3.0, "src_out": 6.0}],      # past the 4 s clip
                W=96, H=96, duration=4.0)
            doc = dm_render.render(j, [], fast=True, do_verify=False, do_export=False)
            final = j / doc["final"]
            eo = {e["id"]: e for e in doc["events_out"]}
            self.assertAlmostEqual(eo["e003"]["out_out"] - eo["e003"]["out_in"], 1.0, delta=1 / 30 + 1e-6)
            self.assertTrue(any("e003" in w and "clamped" in w for w in doc["warnings"]), doc["warnings"])
            self.assertAlmostEqual(doc["duration"], 4.0, delta=0.05)
            pcm = _pcm(final)

            def span_rms(e):
                a, b = eo[e]["out_in"] + 0.1, eo[e]["out_out"] - 0.1
                return _rms(pcm[int(a * 8000):int(b * 8000)])
            self.assertGreater(span_rms("e001"), 0.05)
            self.assertLess(span_rms("e002"), 0.01)
            self.assertGreater(span_rms("e003"), 0.05)
            self.assertEqual(doc["muted"], ["e002"])
            self.assertEqual(doc["grade"]["per_event"], {"e002": "mono"})

            def chroma(t):
                raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(final), "-frames:v", "1",
                                      "-f", "rawvideo", "-pix_fmt", "yuv444p", "-"], capture_output=True,
                                     check=True).stdout
                n = 96 * 96
                return sum(abs(v - 128) for v in raw[n:3 * n]) / (2 * n)     # mean |U−128|,|V−128|
            self.assertLess(chroma((eo["e002"]["out_in"] + eo["e002"]["out_out"]) / 2), 3)
            self.assertGreater(chroma((eo["e001"]["out_in"] + eo["e001"]["out_out"]) / 2), 15)


@unittest.skipUnless(dm.have("ffmpeg") and dm.have("ffprobe"), "ffmpeg missing")
class WindowsSafePathsAndEncoding(unittest.TestCase):
    """Filtergraph never carries an absolute path (C:\\… breaks it on Windows): ffmpeg runs in render/
    with relative names. Stations print Arabic on a cp1252 console without crashing."""

    def test_arabic_colon_job_dir_cp1252_console(self):
        import os
        with tempfile.TemporaryDirectory(prefix="dm_win_") as td:
            j = Path(td) / "مونتاج: تجربة"
            j.mkdir()
            clip = dm.make_test_clip(j / "فيديو.mp4", 2.0, size="160x90")
            dm.write(j, "analysis", dm.new("analysis", clips=[
                {"id": "c01", "path": str(clip), "duration": 2.0, "width": 160, "height": 90, "fps": 30,
                 "has_audio": True, "shots": [], "words": _words([("اهلا", 0.2, 0.6), ("بيكم", 0.7, 1.2)])}],
                music={"path": None, "bpm": None, "beats": [], "downbeats": []}, tools_used=[], missing=[]))
            dm.write(j, "edl", dm.new("edl", width=180, height=320, fps=30, events=[
                {"id": "e001", "clip": "c01", "src_in": 0.0, "src_out": 1.8, "rec_in": 0.0, "speed": 1.0,
                 "transition_in": {"id": "cut"}, "camera": {"id": "none"}, "reason": "t"}],
                audio={"music": {"path": None}, "voice_from": "events", "target_lufs": -14},
                captions={"enabled": True, "style": "karaoke"}, grade={"id": "none"}, duration=1.8))
            env = {**os.environ, "PYTHONIOENCODING": "cp1252"}
            res = subprocess.run([sys.executable, str(SCRIPTS / "dm_render.py"), "render", "--job", str(j),
                                  "--no-verify", "--no-export"], capture_output=True, timeout=300, env=env)
            out = res.stdout.decode("utf-8", "replace")
            self.assertEqual(res.returncode, 0, out + res.stderr.decode("utf-8", "replace"))
            self.assertIn("render/final.mp4", out)
            graph = (j / "render" / "graph.txt").read_text(encoding="utf-8")
            self.assertIn("ass=filename='captions.ass'", graph)
            self.assertNotIn(str(j), graph)
            self.assertNotIn(td, graph)
            # error path prints the Arabic job path too
            res = subprocess.run([sys.executable, str(SCRIPTS / "dm_render.py"), "render", "--job",
                                  str(Path(td) / "مفيش")], capture_output=True, timeout=60, env=env)
            self.assertEqual(res.returncode, 2, res.stderr.decode("utf-8", "replace"))
            self.assertIn("مفيش", res.stdout.decode("utf-8"))

    def test_other_stations_print_arabic_on_cp1252(self):
        import os
        env = {**os.environ, "PYTHONIOENCODING": "cp1252"}
        for argv in (["dm_doctor.py", "doctor", "--tier", "required"],
                     ["dm_taste.py", "query", "--feeling", "warm", "--json"],
                     ["dm_doctor.py", "install-plan", "--os", "windows"]):
            with self.subTest(argv=argv[:2]):
                res = subprocess.run([sys.executable, str(SCRIPTS / argv[0]), *argv[1:]], capture_output=True,
                                     timeout=120, env=env)
                err = res.stderr.decode("utf-8", "replace")
                self.assertNotIn("UnicodeEncodeError", err)
                self.assertIn(res.returncode, (0, 1), err)

    def test_install_ps1_is_ascii(self):
        raw = (SCRIPTS / "install_tools.ps1").read_bytes()
        bad = sorted({b for b in raw if b > 0x7F})
        self.assertTrue(raw.startswith(b"\xef\xbb\xbf") or not bad, f"non-ASCII bytes {bad[:8]} without a BOM")


if __name__ == "__main__":
    unittest.main()
