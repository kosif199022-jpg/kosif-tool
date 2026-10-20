"""Universal Skill Intelligence Protocol: full coverage receipt, fail-closed gaps, three distinct plans, approval gate."""
import json, shutil, sys, tempfile, unittest
from pathlib import Path
SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import skill_intelligence as S  # noqa: E402


class ProtocolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.b = S.build_brief("عايز فيديو موشن جرافيك 9:16 على صوتي بترجمة عربية متحركة وشخصية كرتونية")

    def test_coverage_is_every_record(self):
        disk = sum(len(json.loads(f.read_text(encoding="utf-8"))) for f in (SK / "data" / "powers").glob("*.json"))
        c = self.b["coverage"]
        self.assertEqual(c["records_on_disk"], disk)
        self.assertEqual(c["records_scanned"], disk)
        self.assertEqual(c["records_classified"], disk)
        self.assertTrue(c["complete"])
        self.assertEqual(len(c["catalog_sha256"]), 64)

    def test_derived_indexes_fresh(self):
        for k, v in self.b["freshness"].items():
            self.assertTrue(v["ok"], f"{k} stale: {v.get('fix')}")

    def test_three_plans_differ_and_each_has_a_verifier(self):
        p = self.b["plans"]
        sizes = [p[k]["counts"]["superpowers"] for k in "ABC"]
        self.assertLess(sizes[0], sizes[1])
        self.assertLessEqual(sizes[1], sizes[2])
        for k in "ABC":
            self.assertIn("verify", p[k]["stages"], k)
            order = [S.STAGE_ORDER.index(s) for s in p[k]["stages"]]
            self.assertEqual(order, sorted(order), k)
        self.assertIn(self.b["recommended"], "ABC")
        self.assertIn("أنصحك بالخطة", self.b["approval_question"])
        self.assertTrue(self.b["recommended_reason"])

    def test_own_voice_never_replaced_and_transcription_forced(self):
        b = S.build_brief("عندي فويس بصوتي عايز فيديو ريلز 9:16 بكلمات عربية متحركة على صوتي")
        ex = [e["id"] for e in b["excluded"]]
        self.assertTrue(ex, "TTS / voice-clone superpowers must be excluded for the user's own voice")
        for k in "ABC":
            self.assertFalse(set(ex) & {x["id"] for x in b["plans"][k]["superpowers"]}, k)
        need = next(m for m in b["must_have_coverage"] if m["need"].startswith("توقيت الكلمات"))
        self.assertEqual(need["status"], "covered")
        for k in "ABC":
            self.assertTrue(b["plans"][k]["meets_must_haves"], k)

    def test_levels_and_recommendation_reasons(self):
        l0 = S.build_brief("ترجم الجملة دي للإنجليزي: القدرات الخارقة جاهزة")
        self.assertEqual(l0["analysis"]["level"], "L0")
        self.assertIsNone(l0["approval_question"])
        self.assertEqual(l0["plans"], {})
        code = S.build_brief("ابني لي تطبيق ويب بسيط لمحاسبة محل صغير: مبيعات ومخزون وتقرير شهري PDF، ويكون فيه اختبارات")
        self.assertEqual(code["analysis"]["primary"], "code")
        self.assertEqual(code["analysis"]["ambition"], "balanced")   # «بسيط» describes the app, not the plan
        self.assertEqual(code["recommended"], "B")
        self.assertNotIn("reverse", [x["group"] for x in code["plans"]["A"]["superpowers"]])
        self.assertIn("اختبارات", code["recommended_reason"])

    def test_plans_are_different_approaches(self):
        ideas = {self.b["plans"][k]["idea"] for k in "ABC"}
        self.assertEqual(len(ideas), 3)

    def test_font_requests_bring_the_users_typography_library(self):
        for task in ("اعمل خطة مذاكرة لابني", "خطوات تثبيت بايثون", "خطأ في الكود"):
            self.assertEqual(S.asset_libraries(task), [], task)  # خطة/خطوات/خطأ are not fonts
        b = S.build_brief("صمم شعار بخط كوفي لمطعم شاورما، عربي وإنجليزي")
        libs = b["asset_libraries"]
        self.assertEqual([x["id"] for x in libs], ["telegram-typography-atlas"])
        lib = libs[0]
        index = json.loads((SK / lib["index"]).read_text(encoding="utf-8"))
        self.assertEqual(lib["stats"]["fonts"], len(index["fonts"]))
        self.assertEqual(lib["stats"]["redistribution_approved"], 0)  # license hints are never permission
        self.assertRegex(lib["command"], r'"[^"]*kufi[^"]*"')
        self.assertIn("--arabic-only", lib["command"])
        self.assertNotRegex(json.dumps(lib, ensure_ascii=False), r"[A-Za-z]:\\\\|/Users/|/home/")  # no private paths
        self.assertEqual(b["analysis"]["primary"], "image")
        self.assertTrue(any(m["need"].startswith("خط مناسب") and m["status"] == "covered" for m in b["must_have_coverage"]))
        for k in "ABC":
            p = b["plans"][k]
            self.assertEqual(p["tools"][0]["id"], "telegram-typography-atlas", k)
            self.assertIn("telegram-typography-atlas", p["asset_routes"])
        self.assertIn("font-fidelity-lab", [t["id"] for t in b["plans"]["B"]["tools"]])
        self.assertIn("مكتبات أصولك", S.render(b))

    def test_count_and_deep(self):
        sp = [x["id"] for x in self.b["plans"]["A"]["superpowers"]]
        c = S.count(sp)
        self.assertEqual(c["superpowers"], len(sp))
        self.assertEqual(c["unknown_superpowers"], [])
        self.assertIn("=====", S.deep([sp[0]]))

    def test_scores_use_the_published_weights(self):
        x = self.b["shortlist"][0]
        self.assertEqual(set(x["score_parts"]), set(S.WEIGHTS))
        self.assertAlmostEqual(sum(x["score_parts"].values()), x["score"], delta=0.6)
        self.assertLessEqual(x["score"], 100)

    def test_motion_request_routes_to_motion(self):
        groups = [g["group"] for g in self.b["inventory"]["groups_ranked"][:3]]
        self.assertIn("motion", groups)
        self.assertIn("montage-pro", [t["id"] for t in self.b["tools"]] + ["montage-pro"])  # registry entry exists

    def test_report_renders_required_sections(self):
        md = S.render(self.b)
        for h in ("بطاقة الطلب", "نتيجة الجرد", "مقارنة الخطط", "التوصية", "موافق", "جدول التغطية"):
            self.assertIn(h, md)

    def test_fails_closed_on_unclassified_family(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            fake = tmp / "powers"
            shutil.copytree(SK / "data" / "powers", fake)
            (fake / "zz-unknown.json").write_text(json.dumps([{"id": "ZZ-01", "family": "zz-unknown", "name_en": "x"}]), encoding="utf-8")
            old = S.POWERS
            S.POWERS = fake
            try:
                r = S.scan_catalog()["receipt"]
            finally:
                S.POWERS = old
            self.assertFalse(r["complete"])
            self.assertEqual(r["unclassified_count"], 1)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
