"""The two automatic directors decide like editors: direct (a talking clip) and verse (sound alone)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))


class Directors(unittest.TestCase):
    def test_direct_plans_like_an_editor(self):
        import direct
        def seg(t, text, step=0.4):
            ws = [{"text": w, "start": round(t + i * step, 3), "end": round(t + (i + 1) * step, 3)} for i, w in enumerate(text.split())]
            return {"start": t, "end": ws[-1]["end"], "text": text, "words": ws}
        segs = [seg(0.0, "محدش معاك 24 ساعة"), seg(1.8, "إنت مع نفسك 24 ساعة"), seg(3.8, "محدش ممكن يعيش لك حلمك"),
                seg(6.4, "محدش ممكن ينزل لك وزنك"), seg(9.0, "كافح"), seg(9.6, "كافح"), seg(10.4, "محدش يقدر إطلاقا"),
                seg(12.0, "كافح"), seg(12.8, "حط نفسك في الفعل"), seg(14.6, "اللحظة دي ممكن تكون آخر لحظة")]
        words = [w for sg in segs for w in sg["words"]]
        stress = [0.0] * len(words)
        shots = [{"start": 0.0, "end": 9.4, "box": (0.3, 0.15, 0.4, 0.33), "cx": 540, "cy": 600},
                 {"start": 9.4, "end": 17.5, "box": (0.45, 0.25, 0.1, 0.2), "cx": 540, "cy": 700}]
        P = direct.plan(segs, shots, stress, 1080, 1920, 17.5)
        self.assertEqual(P["payoff"]["lines"][0] + " " + P["payoff"]["lines"][1], "حط نفسك في الفعل")   # the line after the refrain
        keys = [k["text"] for k in P["keys"]]
        for kw in ("حلمك", "وزنك"):
            self.assertIn(kw, keys)                                               # end-focus picks the content word
        self.assertNotIn("ساعة", keys)                                            # the unit after a number belongs to the ring
        self.assertNotIn("ممكن", keys)                                            # filler words never become keywords
        self.assertEqual([m["text"] for m in P["motifs"]], ["24"])                 # one ring, on the repetition
        self.assertAlmostEqual(P["motifs"][0]["t"], 1.8 + 3 * 0.4, places=2)
        face_bottom = (0.15 + 0.33) * 1920
        for k in P["keys"]:
            if k["t"] < 9.4:
                self.assertGreater(k["y"], face_bottom)                          # never over the face
        for c in P["captions"]:
            self.assertLessEqual(c["y"], 0.80 * 1920)                             # inside the 9:16 safe area
        self.assertEqual([c["text"] for c in P["chapters"]], ["كافح"])          # the cut's word becomes the transition plane
        fixed = direct.apply_fixes([seg(0.0, "ما حدش معاك")], "ما حدش=محدش")
        self.assertEqual(fixed[0]["text"], "محدش معاك")
        self.assertAlmostEqual(fixed[0]["words"][0]["start"], 0.0); self.assertAlmostEqual(fixed[0]["words"][0]["end"], 0.8)

    def test_verse_reads_a_text_like_a_lyricist(self):
        import verse
        # the true text (with diacritics and hamza) onto ASR words (plain, one misheard, one missed)
        asr = [{"text": t, "start": i * 0.5, "end": i * 0.5 + 0.45} for i, t in enumerate("اللهم اجعل هذا اليوم مفتاح لكل خير".split())]
        lines = verse.align([["اللّهُمَّ", "اجْعَلْ", "هذا", "اليومَ"], ["مِفتاحاً", "لكلِّ", "خيرٍ", "وسرور"]], asr)
        self.assertEqual([w["start"] for w in lines[0]], [0.0, 0.5, 1.0, 1.5])               # matched through the diacritics
        self.assertAlmostEqual(lines[1][0]["start"], 2.0)                                    # a misheard word keeps its slot
        self.assertGreater(lines[1][3]["start"], lines[1][2]["start"])                       # a missed word sits after its neighbour
        # phrasing: no pauses (stretched words) → cut before phrase openers, keep "يا حي يا قيوم" whole, ≤ 7 words
        flat = [{"text": t, "start": i * 0.32, "end": (i + 1) * 0.32} for i, t in
                enumerate("اللهم في يوم الخميس اجعل هذا اليوم مفتاحا لكل خير وقضيت حوائجنا يا حي يا قيوم بك أستجير".split())]
        segs = verse.segment(flat)
        texts = [" ".join(w["text"] for w in s) for s in segs]
        self.assertTrue(all(len(s) <= 7 for s in segs))
        self.assertTrue(any(t.startswith("اجعل") for t in texts), texts)
        self.assertTrue(any("يا حي يا قيوم" in t for t in texts), texts)
        self.assertFalse(any(t.split()[-1] in ("في", "لكل", "يا") for t in texts), texts)  # no line ends on a particle
        # plan: the refrain's last return is the payoff, keywords are sparse and never fillers, sections per picture
        def ln(t, text, step=0.45):
            return [{"text": w, "start": round(t + i * step, 3), "end": round(t + (i + 1) * step, 3)} for i, w in enumerate(text.split())]
        song = [ln(0.5, "ليل المدينة بارد"), ln(3.0, "والقلب يسأل عن بيته"), ln(5.6, "يا غربة الروح"), ln(8.0, "والدرب طويل وبعيد"),
                ln(10.6, "يا غربة الروح"), ln(13.0, "متى نرجع للوطن"), ln(15.6, "يا غربة الروح")]
        n = sum(len(x) for x in song)
        P = verse.plan(song, [0.4] * n, 20.0, 1080, 1920, "غربة", n_images=3)
        self.assertTrue(P["lines"][P["payoff"]]["payoff"]); self.assertEqual(P["payoff"], 6)  # the last return of the refrain
        self.assertEqual(P["refrain"], "يا غربة الروح")
        keys = [w["text"] for l in P["lines"] for w in l["words"] if w["key"]]
        self.assertEqual(len(keys), len(set(keys)))                                       # each keyword once
        self.assertNotIn("يا", keys)
        self.assertGreaterEqual(len(P["sections"]), 3)                                    # one section per picture
        for l in P["lines"]:
            self.assertLess(l["t"], l["end"])
        for a, b in zip(P["lines"], P["lines"][1:]):
            self.assertLessEqual(a["end"], b["t"])                                         # lines never overlap
        self.assertIsNotNone(P["cards"]["header"])                                        # no intro: the title as a header


if __name__ == "__main__":
    unittest.main()
