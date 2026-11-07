"""Dragon Montage station 5 «يكتب المونتاج»: the director (dm_direct.py) and EDL converters (dm_edl.py)."""
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DM = ROOT / ".claude/skills/kosif-dragon-montage/scripts"
sys.path.insert(0, str(DM))


def _load(name):
    spec = importlib.util.spec_from_file_location(name, DM / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


dm = _load("dm_common")
dm_edl = _load("dm_edl")
direct = _load("dm_direct")

SENTENCES = [
    "اهلا بيكم في رحلة جديدة",
    "النهارده هنروح مكان محدش يعرفه",
    "ليه الناس كلها بتسافر نفس الأماكن؟",
    "السر إن أحلى الأماكن مستخبية",
    "المكان ده غير حياتي جدا",
    "تخيل تصحى على البحر ده كل يوم",
    "الرحلة كلها كلفتني 3000 جنيه بس",
    "لو عايز تعرف الطريق تابعني واشترك",
    "خلينا نكمل المشي ناحية الجبل",
    "الأكل هنا طعمه مختلف خالص",
]
FILLERS = ["اممم", "يعني", "آآ"]


def talking_clip(path):
    """10 minutes, 10 shots of 60 s with a face, sentences with fillers and long pauses."""
    words, silences, t, k = [], [], 0.5, 0
    while t < 595:
        sent = SENTENCES[k % len(SENTENCES)].split()
        if k % 3 == 1:                                   # a filler before every third sentence
            words.append({"w": FILLERS[k % 3], "start": round(t, 3), "end": round(t + 0.45, 3), "conf": 0.6})
            t += 0.55
        for j, w in enumerate(sent):
            d = 0.22 + 0.04 * len(w)
            words.append({"w": w + ("." if j == len(sent) - 1 and "؟" not in w else ""), "start": round(t, 3),
                          "end": round(t + d, 3), "conf": 0.9})
            t += d + 0.08
        pause = 0.9 if k % 4 == 0 else 0.5
        if pause > 0.8:
            silences.append({"start": round(t, 3), "end": round(t + pause, 3)})
        t += pause
        k += 1
    shots = [{"id": f"c01-s{i + 1:03d}", "start": i * 60.0, "end": (i + 1) * 60.0,
              "quality": {"sharpness": 0.7, "exposure": 0.55, "shake": 0.05, "score": 0.6 + 0.03 * (i % 4)},
              "faces": 1, "motion_energy": 0.1, "color": {"mean_rgb": [0.4, 0.4, 0.4], "saturation": 0.3}}
             for i in range(10)]
    energy = [{"t": float(s), "rms": 0.1 + 0.15 * ((s // 7) % 3) / 2} for s in range(600)]
    return {"id": "c01", "path": path, "duration": 600.0, "width": 1920, "height": 1080, "fps": 30, "has_audio": True,
            "loudness_lufs": -19, "shots": shots, "words": words, "silences": silences, "energy": energy}


def travel_clip(n, path):
    shots, t = [], 0.0
    for i in range(5):
        d = 3.0 + (i + n) % 3
        shots.append({"id": f"c{n:02d}-s{i + 1:03d}", "start": round(t, 3), "end": round(t + d, 3),
                      "quality": {"sharpness": 0.8, "exposure": 0.6, "shake": 0.1 * ((i + n) % 2),
                                  "score": round(0.5 + 0.08 * ((i * n) % 5), 2)},
                      "faces": 1 if (i + n) % 4 == 0 else 0, "motion_energy": round(0.2 + 0.15 * ((i + 2 * n) % 5), 2),
                      "color": {"mean_rgb": [0.5, 0.4, 0.3], "saturation": 0.5}})
        t += d
    return {"id": f"c{n:02d}", "path": path, "duration": round(t, 3), "width": 1920, "height": 1080, "fps": 30,
            "has_audio": True, "shots": shots, "words": [], "silences": [], "energy": []}


def fixture(job, target=45):
    media = job / "media"
    media.mkdir(parents=True)
    paths = {}
    for n in range(1, 6):
        p = media / f"clip{n}.mp4"
        p.write_bytes(b"\0" * 64)
        paths[n] = str(p)
    mp = media / "music.mp3"
    mp.write_bytes(b"\0" * 64)
    beats = [round(0.25 + 0.5 * i, 3) for i in range(400)]           # 120 bpm
    analysis = dm.new("analysis", clips=[talking_clip(paths[1])] + [travel_clip(n, paths[n]) for n in range(2, 6)],
                      music={"path": str(mp), "bpm": 120, "beats": beats, "downbeats": beats[::4]},
                      contact_sheet=None, tools_used=["fixture"], missing=[])
    brief = dm.new("brief", task="التنين الأسود، مونتاج", one_truth="أحلى الأماكن مستخبية", audience="شباب",
                   platform="reel", aspect="9:16", target_seconds=target, feeling="inspiring", energy=0.7,
                   language="ar-eg", content_type="travel", must_keep=[], avoid=[], frameworks=[])
    concepts = dm.new("concepts", concepts=[
        {"id": "A", "title": "speech", "arc": ["hook", "setup", "payoff", "cta"], "rhythm": "speech-led",
         "hook": {"text": "ليه الناس كلها بتسافر نفس الأماكن", "first_seconds": 3}},
        {"id": "B", "title": "beat", "arc": ["hook", "setup", "turn", "payoff", "cta"], "rhythm": "on-beat",
         "hook": {"text": "ليه الناس كلها بتسافر نفس الأماكن", "first_seconds": 3}}],
        decision={"chosen": "B", "matrix": [], "why": "fixture"}, premortem=[])
    look = dm.new("look", style_id="warm-travel", style_source="catalog", grade={"id": "cinematic", "engine": "look_pipeline"},
                  transitions=[{"id": "cut"}, {"id": "xfade-fade", "seconds": 0.25}],
                  camera=[{"id": "punch-in", "scale": 1.08}],
                  captions={"style": "karaoke", "font": "Cairo", "position": "lower"}, music={"mood": "warm"}, why="fixture")
    for kind, data in (("analysis", analysis), ("brief", brief), ("concepts", concepts), ("look", look)):
        dm.write(job, kind, data)
    return analysis


class DirectorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.job = Path(cls.tmp.name) / "job"
        cls.analysis = fixture(cls.job)
        cls.edl = direct.direct(cls.job)
        cls.clips = {c["id"]: c for c in cls.analysis["clips"]}

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_contract_and_duration(self):
        dm.validate("edl", self.edl)
        self.assertEqual(dm_edl.check(self.edl), [])
        self.assertEqual((self.edl["width"], self.edl["height"]), (1080, 1920))
        self.assertLessEqual(abs(self.edl["duration"] - 45) / 45, 0.10, self.edl["duration"])
        self.assertGreaterEqual(len(self.edl["events"]), 8)

    def test_hook_first_with_reason(self):
        first = self.edl["events"][0]
        self.assertEqual(first["role"], "hook")
        self.assertEqual(first["rec_in"], 0.0)
        self.assertTrue(first["reason"].startswith("hook:"))
        self.assertIn("خطّاف", first["reason"])
        self.assertLessEqual(dm_edl.event_seconds(first), 3 * 1.6 + 0.5)
        for ev in self.edl["events"]:
            self.assertIn("|", ev["reason"])                  # English | Arabic
            self.assertTrue(ev["reason"].startswith(ev["role"] + ":"))

    def test_arc_order_and_mix(self):
        roles = [e["role"] for e in self.edl["events"]]
        arc = ["hook", "setup", "turn", "payoff", "cta"]
        self.assertEqual([r for i, r in enumerate(roles) if i == 0 or roles[i - 1] != r],
                         [r for r in arc if r in roles])
        kinds = {e["kind"] for e in self.edl["events"]}
        self.assertEqual(kinds, {"speech", "broll"})

    def test_never_cuts_inside_a_word_and_drops_fillers(self):
        for ev in self.edl["events"]:
            for w in self.clips[ev["clip"]]["words"]:
                for t in (ev["src_in"], ev["src_out"]):
                    self.assertFalse(w["start"] + 1e-6 < t < w["end"] - 1e-6, (ev["id"], t, w))
                if ev["src_in"] <= w["start"] and w["end"] <= ev["src_out"]:
                    self.assertNotIn(w["w"], ("اممم", "يعني", "آآ"), ev["id"])

    def test_no_long_silence_kept(self):
        for ev in self.edl["events"]:
            if ev["kind"] != "speech":
                continue
            ws = [w for w in self.clips[ev["clip"]]["words"] if ev["src_in"] <= w["start"] and w["end"] <= ev["src_out"]]
            for a, b in zip(ws, ws[1:]):
                self.assertLessEqual(b["start"] - a["end"], 0.4 + 1e-6)

    def test_broll_cuts_snapped_to_beats(self):
        beats = self.analysis["music"]["beats"]
        evs = self.edl["events"]
        checked = 0
        for ev, nxt in zip(evs, evs[1:]):
            if ev["kind"] != "broll":
                continue
            cut = nxt["rec_in"]
            self.assertLessEqual(min(abs(b - cut) for b in beats), 0.15 + 1e-3, (ev["id"], cut))
            checked += 1
        self.assertGreater(checked, 2)
        self.assertGreater(self.edl["meta"]["snapped_cuts"], 2)

    def test_no_duplicate_shots_or_source_overlap(self):
        broll = [e["shot"] for e in self.edl["events"] if e["kind"] == "broll"]
        self.assertEqual(len(broll), len(set(broll)))
        evs = self.edl["events"]
        for i, a in enumerate(evs):
            for b in evs[i + 1:]:
                if a["clip"] == b["clip"]:
                    self.assertFalse(a["src_in"] < b["src_out"] and b["src_in"] < a["src_out"], (a["id"], b["id"]))
        for ev in evs:
            if ev["kind"] == "broll":
                shot = next(s for s in self.clips[ev["clip"]]["shots"] if s["id"] == ev["shot"])
                self.assertGreaterEqual(ev["src_in"], shot["start"] - 1e-6)
                self.assertLessEqual(ev["src_out"], shot["end"] + 1e-6)

    def test_look_applied(self):
        evs = self.edl["events"]
        self.assertEqual(self.edl["grade"]["id"], "cinematic")
        self.assertTrue(self.edl["captions"]["enabled"])
        self.assertEqual(self.edl["captions"]["style"], "karaoke")
        self.assertEqual(evs[0]["transition_in"]["id"], "cut")
        for i, ev in enumerate(evs):
            if ev["transition_in"]["id"] != "cut":       # xfade only on a b-roll section change
                self.assertNotEqual(evs[i - 1]["role"], ev["role"])
        self.assertTrue(any(e["camera"]["id"] == "punch-in" for e in evs if e["kind"] == "speech"))

    def test_deterministic(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        job = Path(tmp.name) / "job"
        fixture(job)
        again = direct.direct(job)
        strip = lambda e: [(x["clip"], x["src_in"], x["src_out"], x["rec_in"]) for x in e["events"]]
        self.assertEqual(strip(again), strip(self.edl))

    # ------------------------------------------------------------------ converters
    def test_timeline_round_trip(self):
        tl = dm_edl.to_timeline(self.edl, self.analysis)
        self.assertEqual(tl["schema"], "kosif.timeline.v1")
        self.assertEqual(len(tl["tracks"][0]["clips"]), len(self.edl["events"]))
        self.assertEqual(tl["tracks"][1]["kind"], "audio")
        sys.path.insert(0, str(dm.SP))
        tlmod = _load_sp("kosif_timeline")
        doc = json.loads(json.dumps(tl))
        doc["duration"] = min(doc["duration"], 60)
        doc["width"], doc["height"] = 270, 480          # its own preview pixel budget
        tlmod.validate(doc, do_probe=False)              # the timeline tool accepts it
        back = dm_edl.from_timeline(json.loads(json.dumps(tl)), self.analysis)
        self.assertEqual(len(back["events"]), len(self.edl["events"]))
        for a, b in zip(self.edl["events"], back["events"]):
            for k in ("clip", "src_in", "src_out", "rec_in", "reason", "role"):
                self.assertEqual(a[k], b[k], k)
        self.assertAlmostEqual(back["duration"], self.edl["duration"], places=2)

    def test_pve_dry_run(self):
        pve = dm_edl.to_pve(self.edl, self.analysis)
        self.assertEqual(pve["size"], [1080, 1920])
        self.assertEqual(len(pve["clips"]), len(self.edl["events"]))
        self.assertIn("music", pve["sources"])
        f = self.job / "pve.json"
        f.write_text(json.dumps(pve, ensure_ascii=False), encoding="utf-8")
        res = subprocess.run([sys.executable, str(dm.PVE / "edl_render.py"), str(f), "--out", str(self.job / "x.mp4"),
                              "--dry-run"], capture_output=True, text=True, timeout=60)
        self.assertEqual(res.returncode, 0, res.stderr)
        rep = json.loads(res.stdout.strip().splitlines()[-1])
        self.assertAlmostEqual(rep["expected_duration_s"], self.edl["duration"], delta=0.05)

    def test_nle_export(self):
        out = self.job / "render"
        res = dm_edl.to_nle(self.edl, self.analysis, out)
        words = json.loads(Path(res["words"]).read_text(encoding="utf-8"))["words"]
        self.assertTrue(words)
        self.assertTrue(all(0 <= w["start"] < w["end"] <= self.edl["duration"] + 0.01 for w in words))
        run = subprocess.run(res["argv"] + ["--allow-missing"], capture_output=True, text=True, timeout=120)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        files = json.loads(run.stdout)["files"]
        self.assertTrue(any(f.endswith(".fcpxml") for f in files))
        self.assertTrue(any(f.endswith(".srt") for f in files))

    def test_from_cut_plan(self):
        plan = {"schema": "kosif.edl.v1", "video": {"fps": 30, "width": 1080, "height": 1920, "frame_count": 180},
                "scenes": [{"id": "SCENE-001", "start_frame": 0, "end_frame_exclusive": 90, "spoken_text": "اهلا",
                            "footage_path": self.clips["c02"]["path"], "video_trim": {"in": 0.0, "out": 3.0},
                            "camera": {"move": "slow_push_in"}},
                           {"id": "SCENE-002", "start_frame": 90, "end_frame_exclusive": 180, "spoken_text": "يلا",
                            "footage_path": self.clips["c03"]["path"], "video_trim": {"in": 1.0, "out": 4.0},
                            "camera": {"move": "gentle_pan_left"}}]}
        edl = dm_edl.from_cut_plan(plan, self.analysis)
        dm.validate("edl", edl)
        self.assertEqual([e["clip"] for e in edl["events"]], ["c02", "c03"])
        self.assertEqual(edl["events"][1]["rec_in"], 3.0)
        self.assertEqual(edl["duration"], 6.0)


class ReviewTests(unittest.TestCase):
    def test_apply_review_drop_trim_swap(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        job = Path(tmp.name) / "job"
        analysis = fixture(job)
        edl = direct.direct(job)
        evs = edl["events"]
        speech = next(e for e in evs[1:] if e["kind"] == "speech")
        broll = [e for e in evs if e["kind"] == "broll"]
        drop_id, swap_ev = broll[0]["id"], broll[1]
        dm.write(job, "review", dm.new("review", round=1, checks=[], verdict="fix", score=0.6, fixes=[
            {"event": drop_id, "action": "drop", "detail": "weak shot"},
            {"event": speech["id"], "action": "trim", "detail": "tail 0.6", "check": "dead-air"},
            {"event": swap_ev["id"], "action": "swap", "detail": "repeats colour"},
            {"event": "*", "action": "regrade", "target": "grade", "grade": "warm", "detail": "too cold"}]))
        res = subprocess.run([sys.executable, str(DM / "dm_direct.py"), "direct", "--job", str(job), "--apply-review"],
                             capture_output=True, text=True, timeout=120)
        self.assertEqual(res.returncode, 0, res.stderr)
        new = dm.read(job, "edl")
        self.assertTrue((job / "edl.r0.json").exists())
        self.assertEqual(new["revision"], 1)
        ids = [e["id"] for e in new["events"]]
        self.assertNotIn(drop_id, ids)
        self.assertEqual(len(new["events"]), len(evs) - 1)
        t = next(e for e in new["events"] if e["id"] == speech["id"])
        self.assertLess(t["src_out"], speech["src_out"])
        words = analysis["clips"][0]["words"]
        self.assertFalse(any(w["start"] < t["src_out"] < w["end"] for w in words))
        self.assertIn("review r1", t["reason"])
        s = next(e for e in new["events"] if e["id"] == swap_ev["id"])
        self.assertNotEqual(s["shot"], swap_ev["shot"])
        self.assertEqual(new["grade"]["id"], "warm")
        self.assertEqual(dm_edl.check(new), [])
        self.assertLess(new["duration"], edl["duration"])


def _load_sp(name):
    spec = importlib.util.spec_from_file_location(name, dm.SP / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


if __name__ == "__main__":
    unittest.main()
