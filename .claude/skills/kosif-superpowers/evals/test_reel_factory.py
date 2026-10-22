"""reel_factory.py: advisory rights record, --out refusal, audio codec and words-vs-audio checks, plan math, manifest mapping,
phrase overrides, style determinism and --transcribe forwarding.
Plan tests use a stdlib WAV standing in for an AAC voice (the codec rule is patched for them and tested on its own) and
empty placeholder shot files, so they run without ffmpeg; the codec-probe and plate tests need ffmpeg, and the build
smoke test also needs node + Playwright's Chromium. Each skips cleanly when its tools are missing."""
import contextlib, io, json, math, os, shutil, struct, subprocess, sys, tempfile, unittest, wave
from pathlib import Path
from unittest import mock
SK = Path(__file__).resolve().parents[1]
REPO = SK.parents[2]  # <repo>/.claude/skills/kosif-superpowers
sys.path.insert(0, str(SK / "scripts"))
import reel_factory as RF  # noqa: E402

HAVE_FFMPEG = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))
HAVE_GIT_BIN = bool(shutil.which("git"))
HAVE_GIT = HAVE_GIT_BIN and (REPO / ".git").exists()
HAVE_FAKE_TRANSCRIBE = "KOSIF_TRANSCRIBE_FAKE" in (SK / "scripts" / "montage_pro.py").read_text(encoding="utf-8")


def has_encoder(name: str) -> bool:
    if not HAVE_FFMPEG:
        return False
    r = subprocess.run(["ffmpeg", "-hide_banner", "-encoders"], capture_output=True, text=True)
    return any(line.split()[1:2] == [name] for line in r.stdout.splitlines())


HAVE_X264 = has_encoder("libx264")


def have_chromium() -> bool:
    """The factory's own pre-check: Playwright's Chromium found the way tools/render_html.cjs looks for it."""
    return bool(shutil.which("node") and (REPO / "tools" / "render_html.cjs").is_file()) and RF.chromium_problem() is None


def ffmpeg(*args):
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", *[str(a) for a in args]], check=True)


def gray_diffs(video: Path, crop, lo: int, hi: int):
    """Mean absolute luma difference of frame i → i+1 for i in [lo, hi) inside crop (w, h, x, y): raw bytes, no filters."""
    w, h, x, y = crop
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(video), "-vf", f"crop={w}:{h}:{x}:{y},format=gray",
                          "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    n = w * h
    frames = [raw[i * n:(i + 1) * n] for i in range(lo, hi + 1)]
    return [sum(abs(a - b) for a, b in zip(f0, f1)) / n for f0, f1 in zip(frames, frames[1:])]


def write_wav(path: Path, seconds: float, sr: int = 8000):
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr)
        wf.writeframes(b"".join(struct.pack("<h", int(3000 * math.sin(2 * math.pi * 220 * n / sr))) for n in range(int(sr * seconds))))


def call(argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = RF.main([str(a) for a in argv])
        except SystemExit as exc:  # argparse
            code = exc.code
    return code, out.getvalue(), err.getvalue()


WORDS = [("اللهم", 0.10, 0.50), ("في", 0.55, 0.70), ("يوم", 0.75, 1.00), ("الخميس", 1.05, 1.40),   # pause 0.6
         ("ارزقنا", 2.00, 2.40), ("بركة", 2.45, 2.80),                                              # pause 0.4
         ("آمين", 3.20, 3.80)]


def words_doc(rows=WORDS, **extra):
    return dict({"schema": "kosif-words/1", "words": [{"word": w, "start": s, "end": e} for w, s, e in rows]}, **extra)


def fake_segments(path: Path):
    path.write_text(json.dumps({"language": "ar", "segments": [
        {"text": "اللهم في يوم الخميس", "words": [{"word": w, "start": s, "end": e} for w, s, e in WORDS[:4]]},
        {"text": "ارزقنا بركة آمين", "words": [{"word": w, "start": s, "end": e} for w, s, e in WORDS[4:]]}]}, ensure_ascii=False),
        encoding="utf-8")
    return path


class PlanMathTests(unittest.TestCase):
    def words(self):
        return [{"w": w, "s": s, "e": e} for w, s, e in WORDS]

    def test_group_by_pause_and_max_words(self):
        ph = RF.group_by_pause(self.words())
        self.assertEqual([p["text"] for p in ph], ["اللهم في يوم الخميس", "ارزقنا بركة", "آمين"])
        self.assertEqual((ph[1]["start"], ph[1]["end"]), (2.0, 2.8))
        many = [{"w": f"w{i}", "s": i * 0.3, "e": i * 0.3 + 0.25} for i in range(14)]  # no pause at all
        self.assertEqual([len(p["words"]) for p in RF.group_by_pause(many)], [6, 6, 2])

    def test_cuts_match_hand_made_plate_and_cycle_shots(self):
        # the hand-made reel (jobs/20261022-tiktok-reel/build/make_plate.sh): 7 shots, 0.4 s xfades centred on the cuts
        starts, dur = [0.0, 1.90, 4.18, 6.86, 8.20, 9.74, 13.10], 15.7
        shots = [{"file": f"s{i}.mp4", "start": 2.0} for i in range(3)]
        cuts = RF.plan_cuts(starts, dur, shots, ["fade", "circleopen"])
        self.assertEqual([c["dur"] for c in cuts], [2.1, 2.68, 3.08, 1.74, 1.94, 3.76, 2.8])
        self.assertEqual([c["offset"] for c in cuts[1:]], [1.7, 3.98, 6.66, 8.0, 9.54, 12.9])
        self.assertEqual([c["shot"] for c in cuts], [0, 1, 2, 0, 1, 2, 0])
        self.assertEqual(cuts[3]["in"], 2.0 + 2.1)  # a cycled shot continues where it left off
        self.assertIsNone(cuts[0]["transition"])
        self.assertEqual([c["transition"] for c in cuts[1:3]], ["fade", "circleopen"])
        self.assertAlmostEqual(RF.plate_length(cuts), dur, places=6)

    def test_plate_length_equals_duration_for_any_layout(self):
        for starts, dur, n in (([0.3, 1.7, 2.9, 5.0], 6.2, 2), ([0.0], 3.0, 1), ([0.0, 2.0, 4.5], 7.25, 5)):
            cuts = RF.plan_cuts(starts, dur, [{"file": "a", "start": 0.0}] * n, ["fade"])
            self.assertAlmostEqual(RF.plate_length(cuts), dur, places=6)
            self.assertAlmostEqual(cuts[-1]["dur"], dur - cuts[-1]["at"] + (RF.XFADE / 2 if len(cuts) > 1 else 0), places=6)

    def test_one_shot_per_phrase_unless_too_close(self):
        two = [{"file": "a", "start": 0.0}, {"file": "b", "start": 0.0}]
        cuts = RF.plan_cuts([0.0, 0.5, 2.0, 3.6], 4.0, two, ["fade"], min_shot=1.0)
        self.assertEqual([c["at"] for c in cuts], [0.0, 2.0])  # 0.5 is too soon after 0, 3.6 too close to the end
        self.assertEqual([c["phrase"] for c in cuts], [0, 2])
        self.assertEqual([c["merged"] for c in cuts], [[1], [3]])
        # default: every phrase gets its own shot down to the technical minimum (the 0.4 s xfade + 0.1 s)
        self.assertEqual(RF.MIN_SHOT, 0.5)
        cuts = RF.plan_cuts([0.0, 0.3, 0.8, 2.0, 3.6], 4.0, two, ["fade"])
        self.assertEqual([c["at"] for c in cuts], [0.0, 0.8, 2.0])
        self.assertEqual([c["merged"] for c in cuts], [[1], [], [4]])  # 0.3 s after the start; 0.4 s before the end
        for a, b in zip(cuts[1:], cuts[2:]):  # xfade windows never overlap
            self.assertGreaterEqual(round(b["offset"] - (a["offset"] + RF.XFADE), 6), 0.1)

    def test_short_shot_is_clamped(self):
        cuts = RF.plan_cuts([0.0, 2.0], 4.0, [{"file": "a", "start": 3.0, "duration": 4.0}], ["fade"])
        self.assertLessEqual(cuts[0]["in"] + cuts[0]["dur"], 4.0)

    def test_parse_words_formats(self):
        k1 = {"schema": "kosif-words/1", "words": [{"word": w, "start": s, "end": e, "prob": 0.9} for w, s, e in WORDS],
              "phrases": [{"text": "اللهم في يوم الخميس ارزقنا", "start": 0.1, "end": 2.4, "words": [0, 4]},
                          {"text": "بركة آمين", "start": 2.45, "end": 3.8, "words": [5, 6]}]}
        words, phrases, src = RF.parse_words(k1)
        self.assertEqual(src, "words.json phrases")
        self.assertEqual([len(p["words"]) for p in phrases], [5, 2])
        self.assertEqual(words[0]["p"], 0.9)
        for doc in ({"words": k1["words"]}, k1["words"]):
            words, phrases, src = RF.parse_words(doc)
            self.assertEqual(len(words), 7)
            self.assertIsNone(phrases)
        segs = [{"start": 0.0, "end": 1.4, "text": " اللهم في يوم الخميس", "words": [{"w": " " + w, "s": s, "e": e} for w, s, e in WORDS[:4]]},
                {"start": 2.0, "end": 3.8, "text": " ارزقنا بركة آمين", "words": [{"w": w, "s": s, "e": e} for w, s, e in WORDS[4:]]}]
        words, phrases, src = RF.parse_words(segs)
        self.assertEqual(src, "whisper segments")
        self.assertEqual([p["text"] for p in phrases], ["اللهم في يوم الخميس", "ارزقنا بركة آمين"])
        self.assertEqual(words[0]["w"], "اللهم")
        self.assertNotIn("p", words[0])
        self.assertEqual(RF.parse_words({"segments": segs})[2], "whisper segments")
        overlap = RF.parse_words([{"word": "a", "start": 0.0, "end": 0.9}, {"word": "b", "start": 0.5, "end": 1.0}])[0]
        self.assertEqual(overlap[0]["e"], 0.5)  # clamped to the next start
        with self.assertRaises(RF.Fail):
            RF.parse_words({"words": []})
        by_time = RF.parse_words(dict(k1, phrases=[{"text": "x", "start": "0.1", "end": 1.5}]))[1]
        self.assertEqual(len(by_time[0]["words"]), 4)
        for bad in ({"text": "a b", "start": None, "end": None, "words": None}, {"text": "a b"}, {"start": "soon", "end": 1}):
            with self.assertRaises(RF.Fail) as cm:  # was a TypeError traceback (exit 1)
                RF.parse_words(dict(k1, phrases=[bad]))
            self.assertEqual(cm.exception.code, 2)
            self.assertIn("phrase 1 has neither", str(cm.exception))

    def test_check_words_ties_timings_to_the_audio(self):
        words = self.words()
        mine = "ab" * 32
        bad, rec = RF.check_words({"source": {"sha256": mine.upper()}}, words, mine, 4.0)
        self.assertEqual((bad, rec["status"], rec["sha256_match"], rec["fits_audio"]), ([], "ok", True, True))
        self.assertIn("not measured", rec["timing_accuracy"])
        bad, rec = RF.check_words({"source": {"sha256": "0" * 64, "file": "other.m4a"}}, words, mine, 4.0)
        self.assertEqual(len(bad), 1)
        self.assertIn("other.m4a", bad[0])
        self.assertFalse(rec["sha256_match"])
        bad, rec = RF.check_words(words, words, mine, 3.0)  # bare list: nothing declared; 3.8 > 3.0 + 0.25
        self.assertIsNone(rec["sha256_match"])
        self.assertEqual(rec["words_starting_after_audio"], 1)
        self.assertIn("the last word ends at 3.8 s but --audio lasts 3.0 s", bad[0])
        self.assertEqual(RF.check_words(words, words, mine, 3.6)[0], [])  # within the 0.25 s slack

    def test_display_words_override(self):
        ph = RF.group_by_pause(self.words())[0]
        exact, how = RF.display_words(ph, "اللَّهُمَّ في يومِ الخميس")
        self.assertEqual(how, "words")
        self.assertEqual([w[1] for w in exact], [0.1, 0.55, 0.75, 1.05])
        est, how = RF.display_words(ph, "اللَّهُمَّ في يومِ الخميسِ المبارك")
        self.assertEqual(how, "estimated")
        starts = [w[1] for w in est]
        self.assertEqual(starts, sorted(starts))
        self.assertTrue(ph["start"] <= starts[0] and est[-1][2] <= ph["end"] + 1e-9)

    def test_style_determinism(self):
        self.assertEqual(RF.resolve_style("7"), RF.resolve_style("7"))
        self.assertEqual(RF.resolve_style("gold-night")["palette"], "gold-night")
        looks = {(s["palette"], s["transitions"], s["frame"]) for s in (RF.resolve_style(str(i)) for i in range(12))}
        self.assertGreater(len(looks), 3)
        custom = RF.resolve_style("ivory:glide:arch")
        self.assertEqual((custom["palette"], custom["transitions"], custom["frame"]), ("ivory", "glide", "arch"))
        for bad in ("neon", "ivory:zoom", "ivory:soft:circle"):
            with self.assertRaises(RF.Fail) as cm:
                RF.resolve_style(bad)
            self.assertEqual(cm.exception.code, 2)

    def test_slug_credit_and_inline(self):
        self.assertRegex(RF.slugify("دعاء يوم الخميس", "a.m4a"), r"^reel-[0-9a-f]{8}$")
        self.assertEqual(RF.slugify("Dua — Thursday!", "a.m4a"), "dua-thursday")
        self.assertEqual(RF.split_credit("الصوت: @roouf44"), {"text": "الصوت: @roouf44", "label": "الصوت:", "latin": "@roouf44"})
        self.assertIsNone(RF.split_credit(""))
        tpl = RF.TEMPLATE.read_text(encoding="utf-8")
        self.assertEqual(tpl.count(RF.DATA_TOKEN), 1)
        self.assertIn("window.__kosif", tpl)
        for banned in ("Date.now", "Math.random", "requestAnimationFrame", "new Date"):
            self.assertNotIn(banned, tpl)
        html = RF.inline_scene(tpl, {"title": "</script><b>", "duration": 3})
        self.assertNotIn("</script><b>", html)
        hostile = {"title": "<!--<script>", "handle": "</script><img src=x>", "credit": "a\u2028b", "duration": 3}
        html = RF.inline_scene(tpl, hostile)
        self.assertNotIn("<", html.split("/*KOSIF_SCENE_DATA*/", 1)[1].split("\n", 1)[0])  # no raw "<" in the data at all
        self.assertEqual(json.loads(html.split("/*KOSIF_SCENE_DATA*/", 1)[1].split("\n", 1)[0].rstrip(";"))["title"],
                         "<!--<script>")  # and it reads back unchanged
        self.assertIn('"duration": 3', html)

    def test_layout_inside_safe_zone(self):
        L, S = RF.LAYOUT, RF.SAFE
        self.assertGreaterEqual(L["title_y"] - 62, S["top"])          # 58 px title, ascent + rise
        self.assertLessEqual(L["credit_y"] + 12, S["bottom"])         # 26 px credit, descent
        self.assertLessEqual(L["handle_y"] + 16, L["credit_y"])
        for size, n in ((80, 3), (112, 2)):  # the scene's caption block: baselines around text_cy, lh = 1.3 × size
            first = L["text_cy"] - (n - 1) * size * 1.3 / 2 + size * 0.3
            last = first + (n - 1) * size * 1.3
            self.assertGreater(first - size, L["panel"][1] + L["panel"][3] * 0.42)  # tashkeel ascent stays on the scrim
            self.assertLess(last + size * 0.4, L["handle_y"] - 64 * 0.72)           # descent clears the grown outro handle
        x, y, w, h = L["panel"]
        self.assertAlmostEqual(w / h, 0.8)                             # the 4:5 plate fills the panel
        self.assertLessEqual(x + w, RF.W)

    def test_plate_command_pads_every_input_and_the_end(self):
        cuts = RF.plan_cuts([0.0, 1.2], 2.554, [{"file": "a.mp4", "start": 0.3}, {"file": "b.mp4", "start": 1.0}], ["fade"])
        cmd = RF.plate_cmd(cuts, 77, Path("p/%04d.jpg"))
        self.assertEqual([cmd[i + 1] for i, v in enumerate(cmd) if v == "-t"], ["1.467", "1.621"])  # +2 frames each
        graph = cmd[cmd.index("-filter_complex") + 1]
        self.assertTrue(graph.endswith("[x1]tpad=stop_mode=clone:stop_duration=0.5[plate]"), graph)
        self.assertEqual(cmd[cmd.index("-frames:v") + 1], "77")


class CliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.audio = self.tmp / "voice.wav"
        write_wav(self.audio, 4.0)
        # The stdlib WAV stands in for an AAC voice so these tests need no ffmpeg; the codec rule has its own tests.
        codecs = mock.patch.object(RF, "DELIVERY_CODECS", RF.DELIVERY_CODECS + ("pcm", "pcm_s16le"))
        codecs.start()
        self.addCleanup(codecs.stop)
        self.words = self.tmp / "words.json"
        self.words.write_text(json.dumps(words_doc(), ensure_ascii=False), encoding="utf-8")
        self.files = []
        for i in range(2):  # placeholders: plan only checks they exist (no ffprobe duration for them)
            p = self.tmp / f"shot{i}.mp4"
            p.write_bytes(b"placeholder")
            self.files.append(p)
        self.out = self.tmp / "out"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def shots(self, **over):
        rows = [{"file": str(f), "start": 0.5, "rights": "stock-license", "licence_url": "https://www.pexels.com/license/",
                 "credit": f"Pexels #{i}"} for i, f in enumerate(self.files)]
        rows[1].update(over)
        p = self.tmp / "shots.json"
        p.write_text(json.dumps(rows), encoding="utf-8")
        return p

    def base(self, rights="owned", *extra, shots=None):
        return ["plan", "--audio", self.audio, "--audio-rights", rights, "--words", self.words,
                "--shots", shots or self.shots(), "--out", self.out, *extra]

    def plan(self, out=None):
        return json.loads(((out or self.out) / "plan.json").read_text(encoding="utf-8"))

    def rights(self):
        return json.loads((self.out / "rights.json").read_text(encoding="utf-8"))

    def test_non_owned_audio_without_evidence_is_recorded_not_blocked(self):
        code, out, err = call(self.base("direct-permission"))
        self.assertEqual(code, 0, err)                                 # the owner's rule: rights never block
        self.assertIn("RIGHTS_NOTE", err)
        self.assertIn("--audio-rights-evidence", err)
        self.assertNotIn("RIGHTS_BLOCKED", err)
        rec = self.rights()
        self.assertEqual(rec["status"], "incomplete")
        self.assertEqual(len(rec["gaps"]), 1)
        self.assertTrue((self.out / "plan.json").exists())
        self.assertEqual(json.loads(out)["rights_status"], "incomplete")

    def test_missing_or_unknown_audio_rights_is_recorded(self):
        argv = [a for a in self.base() if a not in ("--audio-rights", "owned")]
        code, _, err = call(argv)
        self.assertEqual(code, 0, err)
        self.assertIn("rights not declared", err)
        self.assertIsNone(self.rights()["audio"]["rights"])
        code, _, err = call(self.base("mine"))
        self.assertEqual(code, 0, err)
        self.assertIn("'mine' is not one of", err)
        self.assertEqual(self.rights()["audio"]["rights"], "mine")

    def test_evidence_url_or_file_completes_the_record(self):
        code, _, err = call(self.base("direct-permission", "--audio-rights-evidence", "http://example.com/permission"))
        self.assertEqual(code, 0, err)
        self.assertEqual(self.rights()["status"], "incomplete")        # plain http is noted as a gap, nothing more
        ev = self.tmp / "permission.txt"
        ev.write_text("written permission", encoding="utf-8")
        code, _, err = call(self.base("direct-permission", "--audio-rights-evidence", ev))
        self.assertEqual(code, 0, err)
        self.assertNotIn("RIGHTS_NOTE", err)
        rec = self.rights()
        self.assertEqual((rec["status"], rec["gaps"]), ("complete", []))
        self.assertEqual(len(rec["audio"]["evidence"]["sha256"]), 64)

    def test_shot_licence_gaps_are_recorded_not_blocked(self):
        for over, gap in ((dict(licence_url="http://www.pexels.com/license/"), "shot 2 (shot1.mp4): licence_url must be an https URL"),
                          (dict(credit=""), "'stock-license' needs a credit"),
                          (dict(rights=None), "rights missing")):
            code, _, err = call(self.base(shots=self.shots(**over)))
            self.assertEqual(code, 0, err)
            self.assertIn(gap, err)
            self.assertTrue(any(gap in g for g in self.rights()["gaps"]), gap)
            self.assertTrue((self.out / "plan.json").exists())

    def test_owned_plan_math(self):
        code, out, err = call(self.base("owned", "--style", "11", "--title", "دعاء", "--credit", "الصوت: @x"))
        self.assertEqual(code, 0, err)
        res = json.loads(out)
        self.assertEqual((res["status"], res["words_check"], res["merged_phrases"]), ("planned", "ok", 0))
        plan = self.plan()
        self.assertAlmostEqual(plan["audio"]["duration"], 4.0, places=2)
        self.assertAlmostEqual(plan["duration"], plan["audio"]["duration"] + 1.0, places=6)
        self.assertAlmostEqual(plan["plate"]["length"], plan["duration"], places=6)
        self.assertAlmostEqual(sum(c["dur"] for c in plan["cuts"]) - RF.XFADE * (len(plan["cuts"]) - 1), plan["duration"], places=6)
        self.assertEqual([p["text"] for p in plan["phrases"]], ["اللهم في يوم الخميس", "ارزقنا بركة", "آمين"])
        self.assertEqual([c["at"] for c in plan["cuts"]], [0.0, 2.0, 3.2])
        self.assertEqual([c["shot"] for c in plan["cuts"]], [0, 1, 0])  # cycled
        self.assertEqual(len(plan["transitions"]), 2)
        self.assertEqual(plan["style"], RF.resolve_style("11"))
        self.assertEqual(plan["credit"]["latin"], "@x")
        self.assertEqual(plan["audio"]["sha256"], RF.sha256(self.audio))
        self.assertEqual(plan["cut_rule"], {"rule": "one shot per phrase, cut at each phrase start", "min_shot": 0.5,
                                            "phrases": 3, "cuts": 3, "merged": []})
        self.assertEqual(plan["words"]["check"]["status"], "ok")
        self.assertIsNone(plan["words"]["check"]["sha256_match"])  # this words.json declares no source

    def test_min_shot_option_records_merged_phrases(self):
        code, _, err = call(self.base("owned", "--min-shot", "0.3"))
        self.assertEqual(code, 2)
        self.assertIn("--min-shot must be at least 0.5", err)
        code, _, err = call(self.base("owned", "--min-shot", "1.5"))
        self.assertEqual(code, 0, err)
        rule = self.plan()["cut_rule"]
        self.assertEqual((rule["min_shot"], rule["cuts"]), (1.5, 2))
        self.assertEqual(rule["merged"], [{"phrase": 2, "start": 3.2, "text": "آمين", "shown_on_cut": 1,
                                           "reason": "starts 1.2 s after the cut at 2.0 s (< 1.5 s)"}])

    def test_phrases_override(self):
        bad = self.tmp / "two.json"
        bad.write_text(json.dumps(["اللَّهُمَّ", "آمين"], ensure_ascii=False), encoding="utf-8")
        code, _, err = call(self.base("owned", "--phrases", bad))
        self.assertEqual(code, 2)
        self.assertIn("--phrases has 2 texts but the words give 3 phrases", err)
        good = self.tmp / "three.json"
        good.write_text(json.dumps(["اللَّهُمَّ في يومِ الخميس", "ارزقنا بركةً", "آمين"], ensure_ascii=False), encoding="utf-8")
        code, _, err = call(self.base("owned", "--phrases", good))
        self.assertEqual(code, 0, err)
        plan = self.plan()
        self.assertEqual(plan["phrases"][1]["text"], "ارزقنا بركةً")
        self.assertEqual(plan["phrases"][1]["words"][1], ["بركةً", 2.45, 2.8])  # timing stays from words

    def test_shots_manifest_mapping(self):
        man = self.tmp / "manifest.json"
        rows = [{"id": "111", "source": "pexels", "page": "https://www.pexels.com/video/111/", "licence": "Pexels License",
                 "licence_url": "https://www.pexels.com/license/", "file": "shot0.mp4", "duration": 10.0},
                {"id": "222", "source": "pexels", "licence": "Pexels License", "licence_url": "https://www.pexels.com/license/",
                 "file": "shot1.mp4", "duration": 6.0},
                {"id": "333", "source": "pexels", "licence_url": "https://www.pexels.com/license/", "file": None, "skipped": "too big"},
                {"id": "444", "source": "elsewhere", "licence_url": "http://example.com/licence", "file": "shot1.mp4"}]
        man.write_text(json.dumps(rows), encoding="utf-8")
        argv = ["plan", "--audio", self.audio, "--audio-rights", "owned", "--words", self.words, "--shots-manifest", man, "--out", self.out]
        code, _, err = call(argv + ["--shot-ids", "111@3,222"])
        self.assertEqual(code, 0, err)
        rec = json.loads((self.out / "rights.json").read_text(encoding="utf-8"))
        self.assertEqual([s["rights"] for s in rec["shots"]], ["stock-license", "stock-license"])
        self.assertEqual(rec["shots"][0]["credit"], "Pexels #111 — https://www.pexels.com/video/111/")
        plan = self.plan()
        self.assertEqual([s["start"] for s in plan["shots"]], [3.0, 1.0])
        self.assertTrue(plan["shots"][0]["file"].endswith("shot0.mp4"))
        code, _, err = call(argv + ["--shot-ids", "111,999"])
        self.assertEqual(code, 2)
        self.assertIn("id 999 is not in", err)
        code, _, err = call(argv + ["--shot-ids", "333"])
        self.assertEqual(code, 2)
        self.assertIn("no downloaded file", err)
        shutil.rmtree(self.out)
        code, _, err = call(argv + ["--shot-ids", "111,444"])
        self.assertEqual(code, 0, err)  # unknown source → no rights, and an http licence: both recorded as gaps
        self.assertIn("shot 2 (444): rights missing", err)
        self.assertIn("licence_url must be an https URL", err)
        self.assertEqual(json.loads((self.out / "rights.json").read_text(encoding="utf-8"))["status"], "incomplete")
        code, _, err = call(argv)
        self.assertEqual(code, 2)
        self.assertIn("--shot-ids", err)

    def test_usage_errors(self):
        code, _, _ = call(["plan", "--audio", self.audio, "--audio-rights", "owned", "--shots", self.shots(), "--out", self.out])
        self.assertEqual(code, 2)  # neither --words nor --transcribe
        code, _, err = call(self.base("owned", "--style", "neon"))
        self.assertEqual(code, 2)
        code, _, err = call(["plan", "--audio", self.tmp / "nope.wav", "--audio-rights", "owned", "--words", self.words,
                             "--shots", self.shots(), "--out", self.out])
        self.assertEqual(code, 2)
        self.assertIn("file not found", err)
        code, _, err = call(self.base("owned", "--retranscribe"))
        self.assertEqual(code, 2)
        self.assertIn("--retranscribe only applies with --transcribe", err)

    def test_malformed_phrase_and_out_file_are_usage_errors(self):
        nullp = self.tmp / "nullphrase.json"
        nullp.write_text(json.dumps(words_doc(phrases=[{"text": "a b", "start": None, "end": None, "words": None}])), encoding="utf-8")
        code, _, err = call(["plan", "--audio", self.audio, "--audio-rights", "owned", "--words", nullp, "--shots", self.shots(),
                             "--out", self.out])
        self.assertEqual(code, 2, err)  # was a TypeError traceback (exit 1)
        self.assertIn("phrase 1 has neither", err)
        afile = self.tmp / "afile"
        afile.write_text("", encoding="utf-8")
        code, _, err = call(self.base("owned")[:-1] + [afile])
        self.assertEqual(code, 2, err)  # was FileExistsError (exit 1)
        self.assertIn("exists and is not a folder", err)

    def test_undeliverable_codec_is_refused_before_anything_is_written(self):
        # the audio is muxed with -c copy and verify_video accepts only AAC/MP3: plan must say so, not a 4 after the render
        with mock.patch.object(RF, "DELIVERY_CODECS", ("aac", "mp3")):
            code, _, err = call(self.base("owned"))
        self.assertEqual(code, 2)
        self.assertRegex(err, r"--audio codec pcm(_s16le)? cannot be delivered untouched")
        self.assertIn("Supply AAC (.m4a) or MP3", err)
        self.assertFalse(self.out.exists())

    def test_words_from_another_recording_are_refused(self):
        other = self.tmp / "other.json"
        other.write_text(json.dumps(words_doc(source={"file": "other.m4a", "sha256": "0" * 64, "duration": 20.0}), ensure_ascii=False),
                         encoding="utf-8")
        argv = ["plan", "--audio", self.audio, "--audio-rights", "owned", "--words", other, "--shots", self.shots(), "--out", self.out]
        code, _, err = call(argv)
        self.assertEqual(code, 2)
        self.assertIn("is not the sha256 of --audio", err)
        self.assertIn("--allow-words-mismatch", err)
        self.assertFalse((self.out / "plan.json").exists())
        code, _, err = call(argv + ["--allow-words-mismatch"])
        self.assertEqual(code, 0, err)
        self.assertIn("warning: --allow-words-mismatch", err)
        chk = self.plan()["words"]["check"]
        self.assertEqual((chk["status"], chk["sha256_match"], chk["overridden"]), ("mismatch", False, True))
        # the timings of a longer recording: ten words up to 18.5 s on a 4 s voice
        longer = self.tmp / "longer.json"
        longer.write_text(json.dumps(words_doc([(f"w{i}", 2.0 * i, 2.0 * i + 0.5) for i in range(10)])), encoding="utf-8")
        code, _, err = call(argv[:6] + [longer] + argv[7:-1] + [self.tmp / "out2"])
        self.assertEqual(code, 2)
        self.assertIn("the last word ends at 18.5 s but --audio lasts 4.0 s (8 word(s) start after it)", err)
        # the same timings declared for this very file pass
        same = self.tmp / "same.json"
        same.write_text(json.dumps(words_doc(source={"file": "voice.wav", "sha256": RF.sha256(self.audio)}), ensure_ascii=False),
                        encoding="utf-8")
        code, _, err = call(argv[:6] + [same] + argv[7:-1] + [self.tmp / "out3"])
        self.assertEqual(code, 0, err)
        chk = self.plan(self.tmp / "out3")["words"]["check"]
        self.assertEqual((chk["status"], chk["sha256_match"]), ("ok", True))

    def test_build_checks_its_tools_before_anything(self):
        argv = ["build"] + self.base("owned")[1:]
        with mock.patch.dict(os.environ), mock.patch.object(RF.shutil, "which", lambda name: "/usr/bin/" + name), \
                mock.patch.object(RF, "render_script", return_value=Path(__file__)), \
                mock.patch.object(RF, "chromium_problem", return_value="Playwright's Chromium not found (simulated)"):
            os.environ.pop("KOSIF_RENDER_HTML", None)
            code, _, err = call(argv)
        self.assertEqual(code, 2)  # was exit 4 BUILD_FAILED at the render step
        self.assertIn("Chromium not found", err)
        self.assertFalse(self.out.exists())
        with mock.patch.object(RF.shutil, "which", lambda name: None if name == "node" else "/usr/bin/" + name):
            code, _, err = call(argv)
        self.assertEqual(code, 2)
        self.assertIn("node not found on PATH", err)
        self.assertFalse(self.out.exists())

    @unittest.skipUnless(HAVE_FAKE_TRANSCRIBE, "montage_pro.py transcribe (fake-model hook) not present")
    def test_transcribe_runs_after_the_rights_record_and_propagates_failure(self):
        fake = fake_segments(self.tmp / "segments.json")
        argv = ["plan", "--audio", self.audio, "--transcribe", "--shots", self.shots(), "--out", self.out]
        with mock.patch.dict(os.environ, {"KOSIF_TRANSCRIBE_FAKE": str(fake)}):
            code, _, err = call(argv + ["--audio-rights", "cc-by"])
            self.assertEqual(code, 0, err)                             # a rights gap is noted, the transcription still runs
            self.assertIn("RIGHTS_NOTE", err)
            self.assertTrue((self.out / "rights.json").exists())
            self.assertTrue((self.out / "words.json").exists())
            shutil.rmtree(self.out)
            code, _, err = call(argv + ["--audio-rights", "owned"])
            self.assertEqual(code, 0, err)
        plan = self.plan()
        w = plan["words"]
        self.assertEqual(w["source"], "transcribe")
        self.assertEqual([p["text"] for p in plan["phrases"]], ["اللهم في يوم الخميس", "ارزقنا بركة آمين"])
        # measured and recorded: engine, its own elapsed time, the wall time of the call, and the tie to the audio
        self.assertEqual((w["engine"]["name"], w["engine"]["version"]), ("fake", "fake"))
        self.assertEqual(w["transcribe"]["status"], "written")
        self.assertIsInstance(w["transcribe"]["elapsed_s"], float)
        self.assertGreaterEqual(w["transcribe"]["wall_s"], w["transcribe"]["elapsed_s"])
        self.assertEqual((w["check"]["status"], w["check"]["sha256_match"]), ("ok", True))
        broken = self.tmp / "broken.json"
        broken.write_text("{}", encoding="utf-8")
        with mock.patch.dict(os.environ, {"KOSIF_TRANSCRIBE_FAKE": str(broken)}):  # fresh out: an up-to-date words.json is reused
            code, _, err = call(argv[:-1] + [self.tmp / "out2", "--audio-rights", "owned"])
        self.assertEqual(code, 2)
        self.assertIn("--transcribe failed", err)

    @unittest.skipUnless(HAVE_FAKE_TRANSCRIBE and HAVE_GIT_BIN, "needs git and montage_pro.py transcribe (fake-model hook)")
    def test_transcribe_gets_allow_tracked_and_retranscribe(self):
        fake = fake_segments(self.tmp / "segments.json")
        repo = self.tmp / "gi"
        subprocess.run(["git", "init", "-q", str(repo)], check=True, capture_output=True)
        argv = ["plan", "--audio", self.audio, "--audio-rights", "owned", "--transcribe", "--shots", self.shots(), "--out", repo / "reel"]
        with mock.patch.dict(os.environ, {"KOSIF_TRANSCRIBE_FAKE": str(fake)}):
            code, _, err = call(argv)
            self.assertEqual(code, 2)
            self.assertIn("not git-ignored", err)
            code, _, err = call(argv + ["--allow-tracked"])  # was refused again by transcribe (flag not passed on)
            self.assertEqual(code, 0, err)
            self.assertIn("--allow-tracked", self.plan(repo / "reel")["words"]["transcribe"]["command"])
            hand = self.tmp / "hand"
            hand.mkdir()
            (hand / "words.json").write_text(json.dumps(words_doc(), ensure_ascii=False), encoding="utf-8")
            code, _, err = call(argv[:-1] + [hand])
            self.assertEqual(code, 2)  # a hand-made words.json is never replaced silently...
            self.assertIn("pass --retranscribe to replace it", err)
            self.assertNotIn("--force", err)  # ...and the hint names this tool's flag
            code, _, err = call(argv[:-1] + [hand, "--retranscribe"])
            self.assertEqual(code, 0, err)
        self.assertEqual(json.loads((hand / "words.json").read_text(encoding="utf-8"))["engine"]["name"], "fake")

    @unittest.skipUnless(HAVE_GIT, "git checkout needed")
    def test_out_refuses_tracked_and_jobs(self):
        for bad, why in ((REPO / "tools", "tracked by git"), (REPO / "jobs" / "reel-factory-test", "inside jobs/"),
                         (REPO / "reel-factory-not-ignored", "not git-ignored")):
            code, _, err = call(self.base("owned")[:-2] + ["--out", bad])
            self.assertEqual(code, 2, bad)
            self.assertIn(why, err)
            self.assertFalse((Path(bad) / "rights.json").exists())
        self.assertFalse((REPO / "jobs" / "reel-factory-test").exists())
        self.assertIsNone(RF.out_problem(REPO / "out" / "reels" / "x"))
        self.assertIsNone(RF.out_problem(self.tmp / "elsewhere"))

    @unittest.skipUnless(hasattr(os, "symlink"), "needs symlinks")
    def test_writes_never_follow_a_symlink_out_of_out(self):
        elsewhere = self.tmp / "elsewhere"
        elsewhere.mkdir()
        self.out.mkdir()
        os.symlink(elsewhere, self.out / "build")            # OUT/build -> somewhere else
        (self.out / "rights.json").symlink_to(elsewhere / "rights.json")
        code, _, err = call(self.base("owned"))
        self.assertEqual(code, 2, err)
        self.assertIn("symlink", err)
        self.assertFalse((elsewhere / "rights.json").exists())
        self.assertEqual(list(elsewhere.iterdir()), [])

    def test_out_inside_the_skill_is_always_refused(self):
        target = SK / "out" / "reels" / "reel-factory-test"  # git-ignored by the root out/ pattern, but ships with the skill
        existed = (SK / "out").exists()
        for extra in ([], ["--allow-tracked"]):
            code, _, err = call(self.base("owned")[:-2] + ["--out", target] + extra)
            self.assertEqual(code, 2)
            self.assertIn("inside the skill folder", err)
        self.assertFalse(target.exists())
        self.assertEqual((SK / "out").exists(), existed)
        self.assertIn("inside the skill folder", RF.out_problem(SK / "proofs" / "x"))
        if (REPO / ".git").exists():  # the default no longer depends on the current folder
            here = os.getcwd()
            try:
                os.chdir(str(SK))
                self.assertEqual(RF.default_out("x"), REPO / "out" / "reels" / "x")
            finally:
                os.chdir(here)


@unittest.skipUnless(HAVE_FFMPEG, "needs ffmpeg/ffprobe")
class AudioCodecTests(unittest.TestCase):
    def test_only_aac_or_mp3_is_planned(self):
        with tempfile.TemporaryDirectory() as td:
            t = Path(td)
            (t / "s.mp4").write_bytes(b"placeholder")
            (t / "shots.json").write_text(json.dumps([{"file": "s.mp4", "rights": "owned", "licence_url": "https://example.com/mine"}]),
                                          encoding="utf-8")
            (t / "words.json").write_text(json.dumps(words_doc(WORDS[:4]), ensure_ascii=False), encoding="utf-8")
            sine = ["-f", "lavfi", "-i", "sine=frequency=330:sample_rate=48000:duration=1.5"]
            cases = [("voice.flac", ["-c:a", "flac"])]
            if has_encoder("libopus"):
                cases.append(("voice.opus", ["-c:a", "libopus"]))  # WhatsApp-style voice note
            for name, enc in cases + [("voice.m4a", ["-c:a", "aac"])]:
                ffmpeg(*sine, *enc, t / name)
                out = t / ("out-" + name)
                code, _, err = call(["plan", "--audio", t / name, "--audio-rights", "owned", "--words", t / "words.json",
                                     "--shots", t / "shots.json", "--out", out])
                if name.endswith(".m4a"):
                    self.assertEqual(code, 0, err)
                else:  # was exit 0 here and exit 4 VERIFY_FAILED only after the plate and the render
                    self.assertEqual(code, 2, name)
                    self.assertIn("Supply AAC (.m4a) or MP3", err)
                    self.assertFalse(out.exists())


@unittest.skipUnless(HAVE_FFMPEG and HAVE_X264, "needs ffmpeg/ffprobe with libx264")
class PlateTests(unittest.TestCase):
    def test_plate_has_exactly_duration_times_fps_frames(self):
        # measured before the padding: this chain wrote 76 of 77 frames (a 50 fps shot read up to its end ran short)
        with tempfile.TemporaryDirectory() as td:
            t = Path(td)
            ffmpeg("-f", "lavfi", "-i", "testsrc2=size=160x120:rate=30000/1001:duration=3.3", "-c:v", "libx264", "-pix_fmt", "yuv420p", t / "a.mp4")
            ffmpeg("-f", "lavfi", "-i", "smptebars=size=120x160:rate=50:duration=2.7", "-c:v", "libx264", "-pix_fmt", "yuv420p", t / "b.mp4")
            shots = [{"file": str(t / "a.mp4"), "start": 0.3, "duration": 3.3}, {"file": str(t / "b.mp4"), "start": 1.121, "duration": 2.7}]
            for at, dur in ((1.2, 2.554), (1.212, 2.591)):
                cuts = RF.plan_cuts([0.0, at], dur, shots, ["fade"])
                want = int(round(dur * RF.FPS))
                pdir = t / f"p{at}"
                pdir.mkdir()
                r = subprocess.run(RF.plate_cmd(cuts, want, pdir / "%04d.jpg"), capture_output=True, text=True)
                self.assertEqual(r.returncode, 0, r.stderr)
                self.assertEqual(len(list(pdir.glob("*.jpg"))), want, (at, dur))


@unittest.skipUnless(HAVE_FFMPEG and HAVE_X264 and have_chromium(), "needs ffmpeg/ffprobe (libx264), node and Playwright's Chromium")
class BuildSmokeTest(unittest.TestCase):
    def test_tiny_build_is_verified_and_smooth_at_the_cut(self):
        with tempfile.TemporaryDirectory() as td:
            t = Path(td)
            ffmpeg("-f", "lavfi", "-i", "sine=frequency=330:sample_rate=48000:duration=2.5", "-c:a", "aac", t / "a.m4a")
            # shots 1 and 2 are the same still (landscape), so the first cut fades between identical frames and any
            # change there comes from the scene; shot 3 is portrait (the other crop branch)
            ffmpeg("-f", "lavfi", "-i", "testsrc=size=320x240:rate=25", "-frames:v", "1", t / "still.png")
            ffmpeg("-loop", "1", "-i", t / "still.png", "-t", "4", "-r", "25", "-c:v", "libx264", "-pix_fmt", "yuv420p", t / "still.mp4")
            ffmpeg("-f", "lavfi", "-i", "smptebars=size=240x320:rate=25:duration=3", "-c:v", "libx264", "-pix_fmt", "yuv420p", t / "bars.mp4")
            (t / "words.json").write_text(json.dumps([{"word": "اللهم", "start": 0.1, "end": 0.6}, {"word": "في", "start": 1.2, "end": 1.5},
                                                      {"word": "آمين", "start": 2.0, "end": 2.4}], ensure_ascii=False), encoding="utf-8")
            (t / "shots.json").write_text(json.dumps([{"file": n, "rights": "owned", "licence_url": "https://example.com/mine"}
                                                      for n in ("still.mp4", "still.mp4", "bars.mp4")]), encoding="utf-8")
            out = t / "reel"
            code, stdout, err = call(["build", "--audio", t / "a.m4a", "--audio-rights", "owned", "--words", t / "words.json",
                                      "--shots", t / "shots.json", "--title", "تجربة", "--style", "gold-night:soft",
                                      "--out", out, "--draft"])
            self.assertEqual(code, 0, err + stdout)
            b = json.loads((out / "build.json").read_text(encoding="utf-8"))
            self.assertEqual(b["status"], "verified")
            self.assertTrue(b["results"]["verify"]["report"]["source_audio"]["md5_match"])
            self.assertTrue(b["results"]["audio_untouched"])
            self.assertEqual([s["step"] for s in b["commands"]][:4], ["plate", "render", "mux", "verify"])
            self.assertTrue((out / "build" / "fonts" / "OFL-ArefRuqaa.txt").is_file())
            self.assertEqual((b["results"]["plate_frames"], b["results"]["plate_frames_target"]), (105, 105))
            report = (out / "TEST_REPORT.md").read_text(encoding="utf-8")
            self.assertIn("audio identical to source", report)
            self.assertIn("word-timing accuracy: **not measured**", report)
            plan = json.loads((out / "plan.json").read_text(encoding="utf-8"))
            self.assertEqual([c["at"] for c in plan["cuts"]], [0.0, 1.2, 2.0])
            self.assertEqual(plan["cuts"][1]["transition"], "fade")
            # Panel interior of the 540x960 draft (clear of the frame stroke, its light sweep, the title and the
            # captions): only the plate's slow push-in moves it. The old per-shot push-in reset at the cut and
            # measured 1.52 mean-abs at frame 35 → 36 on exactly this crop; ≤ 0.06 once it is continuous.
            k = int(round(1.2 * RF.FPS))
            near = gray_diffs(out / "reel.mp4", (340, 180, 100, 220), k - 4, k + 3)
            self.assertLess(max(near), 0.5, [round(v, 2) for v in near])


if __name__ == "__main__":
    unittest.main()
