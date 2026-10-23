"""Caption lines: reading rules, suspect-phrase screening, every input shape, SRT/VTT/JSON round trips and lint."""
import json, sys, tempfile, unittest
from pathlib import Path
SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import caption_lines as C  # noqa: E402


def W(*rows):
    return [{"text": t, "start": s, "end": e} for t, s, e in rows]


class CaptionLinesTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def test_rules_break_lines(self):
        words = W(("a", 0, .2), ("b", .25, .4), ("c", .45, .6), ("d", .65, .8), ("e", .85, 1.0),   # max-words 4
                  ("f", 2.0, 2.2),                                                                  # pause
                  ("قال؟", 2.3, 2.6), ("نعم", 2.7, 2.9))                                            # Arabic ? ends
        lines = C.group(words, max_words=4)
        self.assertEqual([l["text"] for l in lines], ["a b c d", "e", "f قال؟", "نعم"])
        self.assertEqual([l["break"] for l in lines], ["max-words", "pause", "sentence-end", "end"])

    def test_max_chars_and_duration(self):
        long = W(("abcdefghij", 0, .5), ("klmnopqrst", .5, 1), ("uvwxyz1234", 1, 1.5), ("x", 1.5, 1.6))
        self.assertEqual(len(C.group(long, max_words=9, max_chars=21)), 2)
        slow = W(("a", 0, 1.5), ("b", 1.5, 3.0), ("c", 3.0, 4.5))
        self.assertEqual(len(C.group(slow, max_words=9, max_dur=3.2)), 2)

    def test_comma_needs_two_words(self):
        self.assertEqual(len(C.group(W(("نعم،", 0, .3), ("طبعا", .35, .6)))), 1)
        self.assertEqual(len(C.group(W(("نعم", 0, .3), ("طبعا،", .35, .6), ("هيا", .65, .9)))), 2)

    def test_bridge_and_min_duration_never_overlap(self):
        lines = C.group(W(("a.", 0, .1), ("b.", .3, .35), ("c", 2, 2.05)), min_dur=0.4, bridge=0.3)
        self.assertAlmostEqual(lines[0]["end"], 0.3)        # hole of 0.2 closed, capped by the next start
        self.assertAlmostEqual(lines[1]["end"], 0.7)        # extended into silence
        self.assertAlmostEqual(lines[2]["end"], 2.4)
        for a, b in zip(lines, lines[1:]):
            self.assertLessEqual(a["end"], b["start"])

    def test_screen_drops_inventions_and_loops(self):
        lines = [{"text": t, "start": i, "end": i + .5, "n": 1} for i, t in enumerate(
            ["أهلا", "ترجمة نانسي قنقر", "Thanks for watching!", "...", "نعم", "نعم", "نعم", "تمام"])]
        kept, dropped = C.screen(lines)
        self.assertEqual([l["text"] for l in kept], ["أهلا", "نعم", "نعم", "تمام"])
        self.assertEqual([d["suspect"] for d in dropped], ["subtitle-credit", "outro", "punctuation-only", "repeat-loop"])
        kept2, _ = C.screen([dict(l) for l in lines], keep_suspect=True)
        self.assertEqual(len(kept2), len(lines))

    def test_input_shapes(self):
        shapes = {
            "atlas.json": [{"word": "مرحبا", "start": 0.5, "end": 0.9}],
            "wrapped.json": {"words": [{"text": "مرحبا", "start": 0.5, "end": 0.9}]},
            "whispercpp.json": {"transcription": [{"text": " مرحبا", "offsets": {"from": 500, "to": 900}}]},
            "faster.json": {"segments": [{"words": [{"word": " مرحبا", "start": 0.5, "end": 0.9}]}]},
        }
        for name, data in shapes.items():
            p = self.tmp / name
            p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            self.assertEqual(C.load_words(p), [{"text": "مرحبا", "start": 0.5, "end": 0.9}], name)

    def test_cli_round_trip_and_lint(self):
        src = self.tmp / "w.json"
        src.write_text(json.dumps([{"word": w, "start": i * .5, "end": i * .5 + .4} for i, w in
                                   enumerate("بسم الله الرحمن الرحيم الحمد لله رب العالمين".split())], ensure_ascii=False), encoding="utf-8")
        for ext in (".srt", ".vtt", ".json"):
            out = self.tmp / f"c{ext}"
            self.assertEqual(C.main(["group", str(src), "-o", str(out), "--rlm"]), 0)
            caps = C.parse_captions(out)
            self.assertEqual(" ".join(c["text"] for c in caps), "بسم الله الرحمن الرحيم الحمد لله رب العالمين")
            self.assertEqual(C.lint(caps), [])
        self.assertTrue((self.tmp / "c.srt").read_text(encoding="utf-8").split("\n")[2].startswith(C.RLM))
        self.assertTrue((self.tmp / "c.vtt").read_text(encoding="utf-8").startswith("WEBVTT"))

    def test_lint_flags_problems(self):
        caps = [{"start": 0, "end": 0.2, "text": "هذا سطر طويل جدا جدا جدا"}, {"start": 0.1, "end": 1, "text": "اشتركوا في القناة"}]
        issues = " | ".join(i["issue"] for i in C.lint(caps))
        for needle in ("shorter than", "reading speed", "overlaps", "outro"):
            self.assertIn(needle, issues)


if __name__ == "__main__":
    unittest.main()
