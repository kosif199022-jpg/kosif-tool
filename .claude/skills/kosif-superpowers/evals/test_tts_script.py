"""Offline known-answer tests for scripts/tts_script.py (chunk, estimate, ssml)."""
import contextlib
import io
import json
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import tts_script as T  # noqa: E402

NS = "{http://www.w3.org/2001/10/synthesis}"


def run(args):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            rc = T.main(args)
        except SystemExit as e:
            rc = e.code
    return rc, out.getvalue(), err.getvalue()


class TtsScriptTests(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.d = Path(self.t.name)

    def tearDown(self):
        self.t.cleanup()

    def w(self, text):
        p = self.d / "s.txt"
        p.write_text(text, encoding="utf-8")
        return str(p)

    def test_chunk_sentences_and_paragraphs(self):
        t = "مرحبا بكم في KOSIF Studio. هذا اختبار، قصير جدا!\n\nفقرة ثانية؟ نعم."
        c = T.chunk(t, 30)
        self.assertEqual([i["text"] for i in c["items"]],
                         ["مرحبا بكم في KOSIF Studio.", "هذا اختبار، قصير جدا!", "فقرة ثانية؟ نعم."])
        self.assertEqual([i["ends_at"] for i in c["items"]], ["sentence", "paragraph", "paragraph"])
        self.assertEqual(c["paragraphs"], 2)
        # paragraphs are never merged, even when they would fit
        self.assertEqual(T.chunk(t, 250)["chunks"], 2)

    def test_chunk_never_splits_words(self):
        t = "واحد اثنان ثلاثة أربعة خمسة ستة سبعة ثمانية تسعة عشرة."
        c = T.chunk(t, 20)
        self.assertTrue(c["all_within_limit"])
        self.assertEqual(" ".join(i["text"] for i in c["items"]).split(), t.split())
        for i in c["items"]:
            self.assertLessEqual(i["chars"], 20)
        # clause marks are preferred over plain word breaks
        c2 = T.chunk("الجملة الأولى طويلة، والثانية أطول منها، والثالثة هنا.", 25)
        self.assertEqual(c2["items"][0]["text"], "الجملة الأولى طويلة،")
        self.assertEqual(c2["items"][0]["ends_at"], "clause")
        long = T.chunk("short " + "x" * 50 + " end", 20)
        self.assertFalse(long["all_within_limit"])
        self.assertTrue(any(i.get("overlong_word") for i in long["items"]))
        # a decimal point is not a sentence end
        self.assertEqual(T.sentences("السعر 3.5 جنيه. تمام."), ["السعر 3.5 جنيه.", "تمام."])

    def test_word_count_arabic(self):
        self.assertEqual(T.count_words("وبالكتاب ، نقرأ 2026"), 3)
        self.assertEqual(T.count_words("— - ! ،"), 0)
        self.assertEqual(T.count_words("مَرْحَبًا بِكُم"), 2)

    def test_estimate_known_answer(self):
        e = T.estimate("كلمة " * 130, wpm=130)  # 60 s of speech + one paragraph pause
        self.assertAlmostEqual(e["total_seconds"], 60.8, places=6)
        self.assertEqual(e["total_mmss"], "1:01")
        e2 = T.estimate("أ، ب، ج.", wpm=60)  # 3 s + 2 clauses*0.2 + paragraph 0.8 (sentence mark not double-counted)
        self.assertAlmostEqual(e2["total_seconds"], 4.2, places=6)
        self.assertEqual(e2["items"][0]["clause_marks"], 2)

    def test_ssml_structure_and_lang_runs(self):
        t = "مرحبا بكم في KOSIF Studio. هذا اختبار، قصير جدا!\n\nفقرة & ثانية؟"
        r = T.ssml(t, "ar-EG")
        root = ET.fromstring(r["ssml"])
        self.assertEqual(root.get("{http://www.w3.org/XML/1998/namespace}lang"), "ar-EG")
        self.assertEqual(len(root.findall(NS + "p")), 2)
        self.assertEqual(r["sentences"], 3)
        self.assertEqual(r["other_script_runs"], 1)
        self.assertIn('<lang xml:lang="en-US">KOSIF Studio</lang>.', r["ssml"])
        self.assertIn('اختبار،<break time="200ms"/>', r["ssml"])
        self.assertIn("&amp;", r["ssml"])
        en = T.ssml("Hello world, this is KOSIF. أهلا بكم.", "en-US")
        self.assertIn('<lang xml:lang="ar-SA">أهلا بكم</lang>.', en["ssml"])
        ET.fromstring(en["ssml"])

    def test_cli_bad_input_and_determinism(self):
        f = self.w("نص قصير. ثم نص آخر، وهكذا.")
        a, b = run(["estimate", f]), run(["estimate", f])
        self.assertEqual(a, b)
        self.assertEqual(a[0], 0)
        self.assertEqual(json.loads(a[1])["words"], 6)
        rc, out, _ = run(["ssml", f, "--xml"])
        self.assertTrue(out.startswith("<speak"))
        empty = self.w("   \n")
        for args in (["chunk", empty], ["chunk", f, "--max-chars", "5"], ["estimate", f, "--wpm", "5"],
                     ["ssml", f, "--lang", "not a tag"], ["chunk", str(self.d / "nope.txt")], ["unknown"]):
            rc, out, err = run(args)
            self.assertEqual(rc, 2, args)
            self.assertEqual(out, "")
            self.assertEqual(len(err.strip().splitlines()), 1, (args, err))
        self.assertEqual(run(["--self-test"])[0], 0)


if __name__ == "__main__":
    unittest.main()
