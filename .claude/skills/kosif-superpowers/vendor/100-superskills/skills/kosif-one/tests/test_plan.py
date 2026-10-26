"""Offline tests for the KOSIF One planner: python tests/test_plan.py"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import plan  # noqa: E402

CASES = {
    "اعمل ريل من بنترست عن البحر بالليل": "reel_from_web",
    "نزّل الفيديو ده من تيك توك https://www.tiktok.com/x واعمله مونتاج": "reel_from_web",
    "عايز موشن جرافيك لكلمات متحركة عن النجاح": "motion_2d",
    "مشهد 3D واقعي لمركب في البحر تحت القمر": "cinematic_3d",
    "اعمل فيديو اعلان لمنتج جديد": "launch_video",
    "عندي فيديو بتكلم فيه عايز اقص الصمت واحط سبتايتل": "talking_reel",
    "حلل الفيديو ده واستخرج البرومبت": "analyze_reference",
    "اكتب لي برومبت فيديو لـ Veo عن صحراء": "ai_video_prompts",
    "اعمل لي لوجو لمتجري": "image_graphics",
    "ارسم الصورة دي بيكسل ببيكسل": "pixel_redraw",
    "نضّف الصوت من الضوضاء وماستر على -14": "audio_only",
    "صلح الكود ده فيه خطأ": "not_media",
    "اعمل فيلم على القصيدة دي": "sound_to_film",
    "اكتب كابشن وهاشتاجات للفيديو ده لتيك توك": "social_content",
    "اعمل لي كاروسيل انستجرام عن اخطاء الريلز": "social_content",
    "اعمل خطة محتوى شهر للسوشيال": "social_content",
    "امتى احسن وقت للنشر على حسابي": "social_content",
    "اعمل ريل من بنترست وجهزه للنشر بالهاشتاج": "reel_from_web",
    "عايز فيديو شبهه بالظبط بنفس الانتقالات ونفس الكتابة بس بفيديوهات من بنترست": "mimic_reel",
    "مهارة المحاكاة: قلد الريل ده": "mimic_reel",
}


class PlanTests(unittest.TestCase):
    def test_routes(self):
        for req, want in CASES.items():
            with self.subTest(req=req):
                self.assertEqual(plan.plan(req)["fallback_route"], want)

    def test_every_step_resolves(self):
        for rid, r in plan.ROUTES.items():
            for st in r["steps"]:
                self.assertIn(st.rstrip("?"), plan.STEP_SKILLS, f"{rid}: {st}")

    def test_every_step_has_a_phase(self):
        self.assertEqual(set(plan.STEP_SKILLS) - set(plan.PHASE), set())

    def test_combine_merges_and_orders(self):
        steps = plan.combine(["reel_from_web", "motion_2d", "sound_to_film"])
        names = [s["step"] for s in steps]
        self.assertEqual(len(names), len(set(names)))          # no duplicate steps
        self.assertEqual(names[0], "fetch")                    # gather first
        required = [s["step"] for s in steps if not s["optional"]]
        self.assertEqual(required[-1], "gate")                 # gate is the last required step
        self.assertEqual(names[-1], "post_pack")               # the optional social pack follows the gate
        self.assertLess(names.index("motion_build_2d"), names.index("captions"))
        gate = next(s for s in steps if s["step"] == "gate")
        self.assertEqual(gate["from"], ["reel_from_web", "motion_2d", "sound_to_film"])
        captions = next(s for s in steps if s["step"] == "captions")
        self.assertTrue(captions["optional"])                  # optional in reel_from_web only

    def test_combo_packets(self):
        req = "عايز فيديو للعيد فيه الكلمات بتتحرك والدنيا بتمطر بشكل واقعي"
        out = plan.plan(req, main="cinematic_3d", extra=["sound_to_film"])
        routes = [c["route"] for c in out["combo_packets"]]
        self.assertIn("motion_2d", routes)
        self.assertIn("sound_to_film", routes)                 # Claude's own suggestion is checked too
        self.assertNotIn("cinematic_3d", routes)
        self.assertTrue(all(c["mode"] == "noul" and c["question"].endswith("?") for c in out["combo_packets"]))

    def test_jev_packet_shape(self):
        p = plan.plan("اعمل ريل من بنترست مع ترجمة")["jev_packet"]
        self.assertEqual(p["mode"], "choice")
        self.assertTrue(p["question"].endswith("?"))
        self.assertGreaterEqual(len(p["options"]), 2)
        self.assertIn("reel_from_web", p["options"])
        self.assertEqual(p["evidence"]["requested_addons"], ["captions", "vertical"])

    def test_social_pack_addon_and_step(self):
        out = plan.plan("اعمل ريل من بنترست وجهزه للنشر بالهاشتاج")
        self.assertIn("social_pack", [a["addon"] for a in out["addons"]])
        pack = next(s for s in out["steps"] if s["step"] == "post_pack")
        self.assertTrue(pack["optional"])
        self.assertEqual(pack["use"][0]["how"], "Skill tool")
        self.assertTrue(pack["use"][0]["exists"])               # kosif-social is installed

    def test_empty_falls_to_not_media(self):
        self.assertEqual(plan.plan("مرحبا")["fallback_route"], "not_media")

    def test_installed_skills_exist(self):
        for name in ("kosif-montage-motion", "hyperframes-animation-studio", "pixel-studio-painter", "kosif-social"):
            self.assertTrue(plan.resolve(name)["exists"], name)
        for name in ("ultra-motion-montage", "motion-os"):   # separate packages, optional here
            if not plan.resolve(name)["exists"]:
                print(f"skip: {name} is not installed")

    def test_superskill_playbooks_exist(self):
        missing = [u["path"] for refs in plan.STEP_SKILLS.values() for u in map(plan.resolve, refs)
                   if u["how"] == "Read playbook file" and not u["exists"]]
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main(verbosity=1)
