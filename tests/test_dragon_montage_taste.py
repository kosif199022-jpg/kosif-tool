"""Dragon Montage station 4 «يختار الذوق»: vocabularies are executable, the taste index is complete,
and pick writes a valid look.json whose ids exist."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1] / ".claude" / "skills" / "kosif-dragon-montage"
sys.path.insert(0, str(SKILL / "scripts"))
import dm_common as C  # noqa: E402
import dm_taste as T  # noqa: E402

DATA = SKILL / "data"
FF = shutil.which("ffmpeg")
W, H, FPS = 180, 320, 30


def _ff(args: list[str]):
    res = subprocess.run([FF, "-y", "-v", "error", *args], capture_output=True, text=True, timeout=120)
    assert res.returncode == 0, res.stderr[-800:]


def _ok(out: Path):
    info = C.probe(out)
    v = [s for s in info["streams"] if s["codec_type"] == "video"][0]
    assert float(info["format"]["duration"]) > 0.5
    return v


@unittest.skipIf(FF is None, "ffmpeg not installed")
class FiltersRun(unittest.TestCase):
    """Every grade / transition / camera / caption style runs with ffmpeg on a 2 s test clip."""

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.d = Path(cls._tmp.name)
        cls.a = C.make_test_clip(cls.d / "a.mp4", seconds=2.0, size="320x180")
        cls.b = C.make_test_clip(cls.d / "b.mp4", seconds=2.0, size="320x180", color="rgbtestsrc", tone=660)

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def test_grades(self):
        for gid in T.vocab("grade"):
            with self.subTest(grade=gid):
                out = self.d / f"g_{gid}.mp4"
                _ff(["-i", str(self.a), "-vf", T.grade_filter(gid) + ",format=yuv420p", "-an", "-c:v", "libx264",
                     "-preset", "ultrafast", str(out)])
                _ok(out)

    def test_transitions(self):
        for tid, t in T.vocab("transition").items():
            with self.subTest(transition=tid):
                out = self.d / f"t_{tid}.mp4"
                f = T.transition_filter(tid, offset=1.5)
                if f is None:   # cut / jump-cut / match-cut render as a concat
                    fc, want = "[0:v][1:v]concat=n=2:v=1:a=0,format=yuv420p[v]", 4.0
                else:
                    self.assertTrue(0 < t["seconds"] <= 1.0)
                    fc = f"[0:v]settb=AVTB,fps=30[a];[1:v]settb=AVTB,fps=30[b];[a][b]{f},format=yuv420p[v]"
                    want = 1.5 + 2.0
                _ff(["-i", str(self.a), "-i", str(self.b), "-filter_complex", fc, "-map", "[v]", "-c:v", "libx264",
                     "-preset", "ultrafast", str(out)])
                _ok(out)
                self.assertLess(abs(float(C.probe(out)["format"]["duration"]) - want), 0.2)

    def test_cameras(self):
        for cid in T.vocab("camera"):
            with self.subTest(camera=cid):
                out = self.d / f"c_{cid}.mp4"
                vf = f"scale={W}:{H},setsar=1," + T.camera_filter(cid, W, H, FPS, 2.0) + ",format=yuv420p"
                _ff(["-i", str(self.a), "-vf", vf, "-an", "-c:v", "libx264", "-preset", "ultrafast", str(out)])
                v = _ok(out)
                self.assertEqual((v["width"], v["height"]), (W, H))

    def test_caption_styles_burn_arabic(self):
        keys = ["Fontname", "Fontsize", "PrimaryColour", "SecondaryColour", "OutlineColour", "BackColour", "Bold",
                "BorderStyle", "Outline", "Shadow", "Alignment", "MarginV", "Encoding"]
        for sid, cs in T.vocab("caption").items():
            if sid == "none":
                continue
            with self.subTest(caption=sid):
                st = cs["ass"]
                self.assertTrue(all(k in st for k in keys))
                self.assertEqual(st["Encoding"], -1)
                ass = self.d / f"{sid}.ass"
                ass.write_text("[Script Info]\nScriptType: v4.00+\nPlayResX: 320\nPlayResY: 180\n\n[V4+ Styles]\n"
                               "Format: Name, " + ", ".join(keys) + "\n"
                               "Style: Cap," + ",".join(str(st[k]) for k in keys) + "\n\n[Events]\n"
                               "Format: Layer, Start, End, Style, Text\n"
                               "Dialogue: 0,0:00:00.00,0:00:01.50,Cap,اهلا بيكم في التنين\n", encoding="utf-8")
                out = self.d / f"cap_{sid}.mp4"
                _ff(["-i", str(self.a), "-vf", f"ass={ass}", "-an", "-c:v", "libx264", "-preset", "ultrafast", str(out)])
                _ok(out)


class TasteData(unittest.TestCase):
    def test_vocab_shapes_and_links(self):
        grades = T.vocab("grade")
        assert {"natural", "cinematic", "night-dua", "teal-orange", "restore"} <= set(grades)
        assert len(grades) == 21
        assert T.resolve("grade", "teal_orange") == "teal-orange" and T.resolve("grade", "none") == "natural"
        tr = T.vocab("transition")
        assert {"cut", "jump-cut", "match-cut", "xfade-fade"} <= set(tr)
        assert T.resolve("transition", "fade") == "xfade-fade" and T.resolve("transition", "wipeleft") == "xfade-wipeleft"
        atoms = {a["id"] for a in json.loads((C.MATRICES / "data" / "197_mechanism_atoms.json").read_text())["atoms"]}
        linked = [a for x in list(tr.values()) + list(T.vocab("camera").values()) for a in x.get("matrix_atoms", [])]
        assert linked and set(linked) <= atoms
        cams = T.vocab("camera")
        assert {"punch-in", "slow-push", "ken-burns-left", "shake-in", "speed-ramp"} <= set(cams)
        assert all(c["kling"] for c in cams.values())
        assert set(T.vocab("caption")) == {"karaoke", "punchy", "clean", "none"}

    def test_taste_index_covers_all_styles(self):
        idx = json.loads((DATA / "taste_index.json").read_text(encoding="utf-8"))
        assert idx["count"] >= 800 and idx["counts"] == {"catalog": 311, "library500": 500, "atlas86": 86}
        g, t, c, cap = set(T.vocab("grade")), set(T.vocab("transition")), set(T.vocab("camera")), set(T.vocab("caption"))
        for r in idx["styles"]:
            assert r["moods"] and set(r["moods"]) <= set(T.FEEL_AR)
            assert 0 <= r["energy"] <= 1 and r["grade_id"] in g and r["caption_style"] in cap
            assert r["transition_ids"] and set(r["transition_ids"]) <= t
            assert r["camera_ids"] and set(r["camera_ids"]) <= c
            assert r["platforms"] and r["content_types"]

    def test_build_is_deterministic(self):
        import build_taste_index as B
        a, b = B.build(), B.build()
        assert a == b

    @staticmethod
    def _fixture_job(tmp_path: Path, **over) -> Path:
        job = C.job_dir(tmp_path / "job")
        brief = C.new("brief", task="التنين الأسود، مونتاج: ريل متوتر عن تحدي الصبح", one_truth="الصبح بيكسب اللي بيقوم",
                      audience="شباب", platform="reel", aspect="9:16", target_seconds=30, feeling="tense", energy=0.75,
                      language="ar-eg", content_type="talking-head", must_keep=[], avoid=["pastel"], frameworks=[])
        brief.update(over)
        C.write(job, "brief", brief)
        C.write(job, "concepts", C.new("concepts", concepts=[
            {"id": "A", "title": "عد تنازلي", "logline": "…", "arc": ["hook", "turn", "payoff"], "rhythm": "on-beat",
             "style_hint": "neon glitch countdown", "risks": []}], decision={"chosen": "A", "why": "…"}))
        return job

    @staticmethod
    def _check_look(look: dict):
        C.validate("look", look)
        assert look["grade"]["id"] in T.vocab("grade")
        assert look["transitions"] and all(t["id"] in T.vocab("transition") for t in look["transitions"])
        assert look["camera"] and all(c["id"] in T.vocab("camera") for c in look["camera"])
        assert look["captions"]["style"] in T.vocab("caption")
        assert look["style_source"] in ("catalog", "library500", "atlas86", "kmx")
        assert look["why"] and any("؀" <= ch <= "ۿ" for ch in look["why"])

    def test_pick_fixture_brief(self):
        tmp_path = Path(self._tmp())
        job = self._fixture_job(tmp_path)
        look = T.pick(job)
        self._check_look(look)
        on_disk = C.read(job, "look")
        assert on_disk["style_id"] == look["style_id"]
        assert "tense" in look["fit"]["parts"] or look["fit"]["parts"].get("feeling", 0) > 0
        assert look["music"]["bpm_range"][0] >= 100       # energy 0.75 + on-beat rhythm

    def test_pick_forced_style_and_cli(self):
        tmp_path = Path(self._tmp())
        job = self._fixture_job(tmp_path)
        res = subprocess.run([sys.executable, str(SKILL / "scripts" / "dm_taste.py"), "pick", "--job", str(job),
                              "--style", "FA-08"], capture_output=True, text=True, timeout=120)
        assert res.returncode == 0, res.stderr
        look = C.read(job, "look")
        self._check_look(look)
        assert look["style_id"] == "FA-08" and look["style_source"] == "atlas86"

    def test_pick_invent(self):
        tmp_path = Path(self._tmp())
        job = self._fixture_job(tmp_path)
        look = T.pick(job, do_invent=True, seed=7)
        self._check_look(look)
        assert look["style_source"] == "kmx" and len(look["kmx"]["parents"]) >= 2

    def test_look_override_from_mimic(self):
        tmp_path = Path(self._tmp())
        job = self._fixture_job(tmp_path)
        (job / "look_override.json").write_text(json.dumps(C.new(
            "look", style_id="ref", style_source="mimic", grade={"id": "vintage", "engine": "look_pipeline", "lut": None},
            transitions=[{"id": "fade", "seconds": 0.4}, {"id": "cut"}], camera=[{"id": "punch-in", "scale": 1.1}],
            captions={"style": "clean"})), encoding="utf-8")
        look = T.pick(job)
        self._check_look(look)
        assert look["grade"]["id"] == "vintage" and look["transitions"][0] == {"id": "xfade-fade", "seconds": 0.4}
        assert look["override"]["keys"] == ["grade", "transitions", "camera"]

    def test_query_cli(self):
        res = subprocess.run([sys.executable, str(SKILL / "scripts" / "dm_taste.py"), "query", "--feeling", "tense",
                              "--platform", "reel", "--content", "talking-head"], capture_output=True, text=True, timeout=120)
        assert res.returncode == 0, res.stderr
        assert len(res.stdout.strip().splitlines()) == 5

    def _tmp(self) -> str:
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        return t.name


if __name__ == "__main__":
    unittest.main()
