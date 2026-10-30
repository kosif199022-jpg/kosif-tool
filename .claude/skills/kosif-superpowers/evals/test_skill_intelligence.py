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

    def test_font_detection_styles_and_own_voice(self):
        for task in ("اعمل خط زمني للمشروع", "عايز شعار اعلاني للحملة", "خطوات تثبيت بايثون"):
            self.assertEqual(S.asset_libraries(task), [], task)     # a timeline, a slogan, steps: not fonts
        cases = {"صمم بطاقة بالرقعة": "ruqah", "خط للأطفال لكتاب قصص": "kids", "عايز الخطوط الكوفية لبوستر": "kufi",
                 "اختار لي خط عربي مقروء لتطبيق موبايل": "sans"}
        for task, style in cases.items():
            libs = S.asset_libraries(task)
            self.assertTrue(libs and style in libs[0]["styles_detected"], (task, libs and libs[0]["styles_detected"]))
            self.assertIn(".claude/skills/kosif-superpowers/scripts/telegram_typography_atlas.py", libs[0]["command"])  # runs from the repo root
        self.assertEqual(S.analyse("اختار لي خط عربي مقروء لتطبيق موبايل")["primary"], "image")
        bi = S.asset_libraries("صمم شعار بخط كوفي عربي وإنجليزي")[0]
        self.assertTrue(bi["bilingual"])
        self.assertIn("--latin", bi["command"])
        self.assertTrue(any(m["need"].startswith("زوج خطوط") for m in S.analyse("صمم شعار بخط كوفي عربي وإنجليزي")["must_haves"]))
        diwani = S.asset_libraries("اعمل بوستر رمضان بخط ديواني")[0]
        if not diwani["open_license_candidates"]:
            self.assertIn("لا يوجد في مكتبتك خط مفتوح", diwani["routes"]["A"])
        b = S.build_brief("حرك كلمات أغنيتي بخط يدوي على صوتي 9:16")
        self.assertEqual(b["analysis"]["primary"], "video")
        self.assertEqual(b["analysis"]["level"], "L2")
        for k in "ABC":
            ids = [t["id"] for t in b["plans"][k]["tools"]]
            self.assertIn("montage-pro", ids, k)
            self.assertIn("telegram-typography-atlas", ids, k)

    def test_specialised_tools_only_when_asked(self):
        import hub
        three = {"id": "x", "area": "3d"}; audio = {"id": "y", "area": "audio"}; draw = {"id": "z", "area": "draw"}
        self.assertFalse(hub.off_request(three, "اعمل فيديو ثري دي لمنتج"))
        self.assertFalse(hub.off_request(three, "build a webgl low poly scene"))
        self.assertTrue(hub.off_request(three, "موديل عمل جديد للشركة"))          # a business model, not a 3D model
        self.assertFalse(hub.off_request(audio, "اعمل نشيد بصوتي"))
        self.assertFalse(hub.off_request(audio, "convert my srt captions to words.json"))
        self.assertTrue(hub.off_request(audio, "اعمل فاتورة ومخزون لمحل"))      # nothing about sound
        self.assertTrue(hub.off_request(audio, "a soundness proof for the parser"))  # 'sound' only as a whole word
        self.assertFalse(hub.off_request(draw, "ارسم ماسكوت كرتون"))
        self.assertTrue(hub.off_request({"id": "web-app-study", "area": "investigate"}, "ابني تطبيق ويب بـ three.js"))
        self.assertFalse(hub.off_request({"id": "web-app-study", "area": "investigate"}, "حلل موقع منافس مبني بإيه"))

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


class V53RoutingFixes(unittest.TestCase):
    """USIP v5.3 routing fixes (audit lens routing: RQ-06..RQ-10 and the missed items)."""

    @classmethod
    def setUpClass(cls):
        cls.meta = S.build_brief("طوّر بروتوكول USIP ومحرك FusionForge للتوليف الذاتي للمهارات وتعلم الـworkflows المركبة، واختبره وارفعه على GitHub")
        cls.inv = S.build_brief("ابني تطبيق ويب صغير لإدارة المخزون مع اختبارات")
        cls.article = S.build_brief("اكتب مقال عربي طويل عن الذكاء الاصطناعي في التعليم")
        cls.walk = S.build_brief("حرّك شخصية ثلاثية الأبعاد تمشي في مشهد سينمائي")
        cls.asr = S.build_brief("ابحث عن أفضل مكتبات تفريغ صوتي عربية وقارن بينها")
        cls.all = [cls.meta, cls.inv, cls.article, cls.walk, cls.asr]

    def test_protocol_version_and_contract_fields(self):
        b = self.meta
        self.assertEqual(b["protocol"], "USIP v6.0")
        self.assertTrue(b["schema"].startswith("kosif.skill-intelligence"))
        self.assertTrue(b["coverage"]["complete"])
        self.assertEqual(set(b["plan_definitions"]), set("ABCD"))
        for w in ("موافق", "تفاصيل", "D", "طوّر", "كمّل بدوني"):
            self.assertIn(w, b["reply_words"])
        for w in ("كمّل", "وقف", "تراجع"):
            self.assertIn(w, b["execution_words"])
        for k in "ABC":   # the FusionForge contract: plans keep their keys
            p = b["plans"][k]
            for key in ("name", "idea", "stages", "superpowers", "tools"):
                self.assertIn(key, p)
            self.assertEqual(p["definition"], S.PLAN_DEFINITIONS[k])
            for x in p["superpowers"]:
                self.assertTrue({"id", "name_ar", "name_en", "stage", "role", "local_badge"} <= set(x))
        self.assertIsInstance(S.expand("تفريغ صوتي", S.build_df(S.scan_catalog()["records"])[0]), list)

    def test_repo_is_a_whole_word_not_report(self):
        a = S.analyse("write a monthly sales report from my spreadsheet")
        self.assertNotIn("code", a["deliverables"])
        self.assertEqual(S.analyse("summarize this report")["level"], "L0")
        self.assertEqual(S.analyse("fix the bug in my repo")["primary"], "code")
        self.assertEqual(S.analyse("create a dashboard from a CSV file with charts and a summary report")["primary"], "data")

    def test_lyrics_and_suno_are_audio_a_lyric_video_is_video(self):
        self.assertEqual(S.analyse("اكتب كلمات أغنية عن الوطن لـ Suno")["primary"], "audio")
        self.assertEqual(S.analyse("write song lyrics for a Suno track")["primary"], "audio")
        self.assertEqual(S.analyse("make a lyric video for my song")["primary"], "video")

    def test_cinematic_is_a_style_not_maximum_effort(self):
        a = S.analyse("حرّك شخصية ثلاثية الأبعاد تمشي في مشهد سينمائي")
        self.assertEqual(a["ambition"], "balanced")
        self.assertNotEqual(a["level"], "L3")
        self.assertEqual(a["style"], ["cinematic"])
        self.assertNotIn("أقصى", self.walk["recommended_reason"])
        self.assertEqual(S.analyse("اعمل فيديو باقصى قوة")["level"], "L3")   # an explicit «بأقصى قوة» still is
        self.assertFalse([v for v in self.walk["verifiers"] if "loudness" in v["name_en"].lower()])   # a silent walk

    def test_tests_must_have_clitics_and_whole_words(self):
        for task in ("ابني سكربت صغير واختبره", "اختبر الكود ده", "add pytest coverage", "write unit tests"):
            self.assertTrue(any(m["need"].startswith("اختبارات") for m in S.analyse(task)["must_haves"]), task)
        for task in ("show me the latest news about AI", "enter the contest"):
            self.assertFalse(any(m["need"].startswith("اختبارات") for m in S.analyse(task)["must_haves"]), task)
        need = next(m for m in self.inv["must_have_coverage"] if m["need"].startswith("اختبارات"))
        names = {x["id"]: x["name_en"] for x in self.inv["shortlist"]}
        self.assertFalse([i for i in need["superpowers"] if "golden still" in names.get(i, "").lower()])   # not a motion suite

    def test_github_push_must_have_and_its_question(self):
        push = lambda a: any(m["need"].startswith("رفع على GitHub") for m in a["must_haves"])
        a = S.analyse("عدّل السكربت وارفعه على GitHub")
        self.assertTrue(push(a))
        self.assertTrue(any("فرع" in q["question"] and q["suggested_default"] for q in a["questions"]))
        named = S.analyse("عدّل السكربت وارفعه على GitHub في فرع جديد")   # the branch is named: no question (RR1-10)
        self.assertTrue(push(named))
        self.assertFalse([q for q in named["questions"] if "فرع" in q["question"]])
        self.assertFalse(push(S.analyse("ارفع الصورة دي على درايف")))
        for task in ("find the best GitHub repos for Arabic OCR", "اكتب مقال عن GitHub Copilot", "قارن بين GitHub و GitLab للفرق الصغيرة",
                     "commit to a daily writing habit plan", "explain what a git rebase does"):   # a mention is not a push (RR-01/RR-02)
            a = S.analyse(task)
            self.assertFalse(push(a), task)
            self.assertFalse([q for q in a["questions"] if "فرع" in q["question"]], task)
        self.assertTrue(push(S.analyse("push my changes to GitHub and open a pull request")))
        need = next(m for m in self.meta["must_have_coverage"] if m["need"].startswith("رفع على GitHub"))
        self.assertEqual(need["status"], "covered")

    def test_meta_engineering_is_code(self):
        self.assertEqual(self.meta["analysis"]["primary"], "code")
        self.assertEqual(self.meta["recommended"], "B")
        self.assertEqual(S.analyse("حسّن بروتوكول المراجعة في المهارة وأضف له اختبارات")["primary"], "code")
        v = S.analyse("اعمل فيديو موشن بمحرك Remotion")
        self.assertEqual(v["primary"], "video")          # a stronger deliverable keeps primary; code is secondary
        self.assertIn("code", v["deliverables"])

    def test_fit_floor_for_core_role_and_plan_picks(self):
        for b in self.all:
            short = {x["id"]: x for x in b["shortlist"]}
            for x in b["shortlist"]:
                if x["role"] == "core":
                    self.assertGreaterEqual(x["fit_share"], S.MIN_FIT, x["id"])
            ver = {v["id"] for v in b["verifiers"]}
            for p in b["plans"].values():
                for x in p["superpowers"]:
                    if x["role"] in ("must-have", "verifier") or x["id"] in ver:
                        continue
                    self.assertGreaterEqual(short[x["id"]]["fit_share"], S.MIN_FIT, (b["analysis"]["request"], x["id"], x["name_en"]))

    def test_verifiers_normalised_and_from_the_right_families(self):
        for b in self.all:
            prim = b["analysis"]["primary"]
            fams = S.VERIFY_FAMILIES.get(prim, S.VERIFY_FAMILIES["unspecified"])
            for v in b["verifiers"]:
                self.assertTrue(v["via"], v)
                self.assertIn(v["via_family"], fams, (prim, v["name_en"], v["via"]))   # the atom that qualified it judges this deliverable
                self.assertNotIn("github actions runner-cost", v["name_en"].lower(), prim)
        names = [v["name_en"] for v in self.article["verifiers"]]
        self.assertFalse([n for n in names if "GitHub Actions" in n or "Systems map" in n], names)
        self.assertFalse([v for v in self.meta["verifiers"] if "Language Coach" in v["name_en"]])
        for v in self.walk["verifiers"] + self.inv["verifiers"]:   # no Arabic-typography check where no Arabic text is produced
            self.assertNotIn(v["via_family"], {"typography-arabic", "arabic-language"}, v["name_en"])

    def test_must_have_terms_do_not_collide_across_senses(self):
        short = {x["id"]: x for x in self.inv["shortlist"]}
        for m in self.inv["must_have_coverage"]:
            for i in m["superpowers"]:
                self.assertNotIn("software-investigation", short[i]["families"], (m["need"], i))
        for k in "ABC":
            self.assertNotIn("reverse", [x["group"] for x in self.inv["plans"][k]["superpowers"]], k)
        self.assertFalse(any(m["need"].startswith("نص عربي") for m in self.asr["analysis"]["must_haves"]))   # Arabic ASR, not RTL text
        self.assertFalse(any(m["need"].startswith("محاسبة") for m in S.analyse("make an inventory of the classes in this APK")["must_haves"]))
        pick = next(m for m in self.article["must_have_coverage"] if m["need"].startswith("نص عربي"))["superpowers"]
        self.assertFalse([i for i in pick if "PlantUML" in short.get(i, {}).get("name_en", "") or i == "SP-0094"])

    def test_aliases_sense_and_concepts(self):
        df = S.build_df(S.scan_catalog()["records"])[0]
        flat = lambda q: S.expand(q, df)
        self.assertIn("transcription", flat("تفريغ صوتي"))
        self.assertIn("article", flat("مقال"))
        self.assertIn("protocol", flat("بروتوكول"))
        self.assertIn("github", flat("وارفعه على GitHub"))
        self.assertIn("upload", flat("ارفع الصورة"))
        self.assertNotIn("github", flat("ارفع الصورة"))
        self.assertIn("test", flat("واختبره"))
        self.assertNotIn("workflows", flat("تعلم الـworkflows المركبة"))              # not GitHub Actions here
        self.assertIn("orchestration", flat("تعلم الـworkflows المركبة"))
        self.assertIn("workflows", flat("optimize our github actions workflows"))
        # every SENSE entry, in its other sense (RR1-04, RR0-07, RR0-11)
        for q in ("ابني محرك ألعاب بسيط", "ابني محرك بحث للمستندات", "محرك قواعد للخصومات"):
            self.assertIn("engine", flat(q), q)
            self.assertNotIn("orchestration", flat(q), q)
        self.assertIn("orchestration", flat("طوّر بروتوكول USIP ومحرك FusionForge للتوليف الذاتي للمهارات"))
        self.assertIn("upscale", flat("ارفع جودة الصورة"))
        self.assertNotIn("upload", flat("ارفع جودة الصورة"))
        self.assertIn("push", flat("slow camera push in on the hero"))
        self.assertIn("git", flat("push my changes to GitHub"))
        self.assertNotIn("push", flat("push my changes to GitHub"))
        self.assertIn("login", flat("صفحة تسجيل الدخول"))
        self.assertIn("recording", flat("تسجيل شاشة فيديو"))
        self.assertIn("expense", flat("تطبيق لتسجيل المصاريف اليومية"))
        self.assertNotIn("recording", flat("تطبيق لتسجيل المصاريف اليومية"))
        for word in S.SENSE:
            rules, default = S.SENSE[word]
            self.assertTrue(rules and isinstance(default, tuple), word)
        cq = S.concepts("شعار عربي", df)
        self.assertTrue(any({"عربي", "arabic"} <= set(g) for g in cq))               # a word and its alias are one concept
        recs = S.scan_catalog()["records"]
        _, toks = S.build_df(recs)
        once = S.score_records(recs[:300], toks[:300], df, [["عربي", "arabic"]])
        twice = S.score_records(recs[:300], toks[:300], df, ["عربي", "arabic"])
        self.assertTrue(all(a <= b + 1e-9 for a, b in zip(once, twice)))
        self.assertTrue(any(a < b for a, b in zip(once, twice)))

    def test_dialect_questions_are_l0_production_is_not(self):
        self.assertEqual(S.analyse("وش معنى كلمة الاستحقاق؟")["level"], "L0")
        self.assertEqual(S.analyse("صلّح خطأ إملائي في الجملة دي")["level"], "L0")
        self.assertNotEqual(S.analyse("لخص التقرير ده واعمل منه عرض تقديمي PDF وانشره")["level"], "L0")
        self.assertNotEqual(S.analyse("اشرح الذكاء الاصطناعي في مقال للمدونة")["level"], "L0")
        self.assertEqual(S.analyse("اشرح لي الفرق بين التعلم الآلي والعميق")["level"], "L0")
        g = S.analyse("explain what a git rebase does")   # git makes code a deliverable only for real work
        self.assertEqual(g["level"], "L0")
        self.assertEqual(g["questions"], [])

    def test_plans_b_and_c_are_not_the_same_plan(self):
        """Contract §1: C is another method, never B plus extras (RR-01/RR-06): C has picks of its own, keeps at most half
        of B's own picks (must-haves and listed checks aside) and never contains the whole of B, unless it is honestly
        labelled a depth level of B (and then differs from B) or marked unavailable."""
        for b in self.all:
            p = b["plans"]
            ids = {k: {x["id"] for x in v["superpowers"]} for k, v in p.items()}
            if p["C"].get("unavailable"):
                self.assertFalse(ids["C"])
                continue
            self.assertNotEqual(ids["B"], ids["C"], b["analysis"]["request"])
            if p["C"].get("depth_of") == "B":
                continue
            fixed = {i for m in b["must_have_coverage"] for i in m["superpowers"]} | {v["id"] for v in b["verifiers"]}
            b_core, c_core = ids["B"] - fixed, ids["C"] - fixed
            self.assertTrue(c_core - ids["B"], "C has no pick of its own")
            self.assertLessEqual(2 * len(b_core & c_core), len(b_core), (b["analysis"]["request"], "C keeps most of B"))
            self.assertFalse(ids["B"] <= ids["C"], (b["analysis"]["request"], "C is B plus extras"))

    def test_named_platform_gate_and_cross_domain_rule(self):
        """A superpower built around a platform the request does not name never enters a plan (RR1-11, RR0-11), and a
        cross-domain integration never comes from a group that is off-domain for the deliverable."""
        names = [x["name_en"] for p in self.inv["plans"].values() for x in p["superpowers"]]
        for k in ("Godot", "Shopify", "GitHub Actions runner-cost", "Typed EVM", "App-store preview"):
            self.assertFalse([n for n in names if k in n], k)
        self.assertTrue(any(x["gated"] for x in self.inv["shortlist"]))
        for b in self.all:
            pen = S.AFFINITY.get(b["analysis"]["primary"], {})
            home = {g for d in b["analysis"]["deliverables"] for g in S.HOME_GROUPS.get(d, [])} | set(b["analysis"]["topics"])
            for x in b["shortlist"]:
                if x["role"] == "cross-domain":
                    self.assertTrue(pen.get(x["group"], 1.0) >= 1.0 or x["group"] in home, (b["analysis"]["request"], x["name_en"]))

    def test_c_is_marked_unavailable_rather_than_a_copy_of_b(self):
        """When the catalog offers neither another method nor a deeper level, C is marked unavailable (never B twice),
        never recommended (not even for a maximum-effort request), and the report says so. Forced with a one-tool request,
        no verifier families and a maximum-effort card."""
        old_fams, old_an = S.VERIFY_FAMILIES, S.analyse
        S.VERIFY_FAMILIES = {k: set() for k in old_fams}
        S.analyse = lambda t: {**old_an(t), "ambition": "max", "level": "L3"}
        try:
            b = S.build_brief("trafilatura")   # one superpower in the whole catalog matches
        finally:
            S.VERIFY_FAMILIES, S.analyse = old_fams, old_an
        c = b["plans"]["C"]
        self.assertTrue(c.get("unavailable"), [x["name_en"] for x in c["superpowers"]])
        self.assertEqual((c["superpowers"], c["stages"], c["tools"], c["meets_must_haves"]), ([], {}, [], False))
        self.assertNotEqual(b["recommended"], "C")   # even though the request asked for maximum effort
        self.assertIn(c["unavailable"], S.render(b))

    def test_shortlist_scores_scale_below_the_fit_floor(self):
        """RR0-15: below MIN_FIT, readiness, evidence, cost and links cannot lift an off-target pick up the shortlist."""
        for b in self.all:
            for x in b["shortlist"]:
                g = min(1.0, (x["fit_share"] + 0.0005) / S.MIN_FIT)   # fit_share is rounded to 3 places
                for part in ("integration", "feasibility", "evidence", "cost"):
                    self.assertLessEqual(x["score_parts"][part], S.WEIGHTS[part] * g + 0.06, (x["name_en"], part))

    def test_data_document_research_have_their_own_archetypes(self):
        self.assertIn("research", S.ARCHETYPES)
        self.assertIn("data", S.ARCHETYPES)
        self.assertIn("document", S.ARCHETYPES)
        self.assertNotEqual(self.article["plans"]["A"]["idea"], S.ARCHETYPES["_generic"]["A"][0])
        rec = self.asr["plans"][self.asr["recommended"]]
        self.assertTrue({"research"} & {x["group"] for x in rec["superpowers"]})


class V53ReviewFixes(unittest.TestCase):
    """Request-card fixes from the adversarial reviews of the v5.3 routing pass (RR-xx); analyse() only, so cheap."""

    def test_questions_and_definitions_are_l0_with_nothing_listed(self):
        for task in ("يعني ايه API؟", "what does API mean?", "ما معنى موشن جرافيك؟", "explain how to make a video", "what is MCP?",
                     "ما هو بروتوكول HTTP؟", "what is the difference between TCP and UDP?", "what's the capital of France?",
                     "مين اخترع الكهرباء؟", "شو يعني الاستحقاق؟", "اشرح لي حول الذكاء الاصطناعي", "لخص الأفكار الرئيسية في التقرير ده"):
            a = S.analyse(task)
            self.assertEqual(a["level"], "L0", task)
            self.assertEqual((a["must_haves"], a["questions"]), ([], []), task)
        for task in ("explain how transformers work in a short animated video", "why does my app crash when I click save",
                     "اشرح الذكاء الاصطناعي في مقال للمدونة", "لخص الكتاب ده وحوله الى عرض تقديمي"):
            self.assertNotEqual(S.analyse(task)["level"], "L0", task)

    def test_ambiguous_meta_words_need_a_software_context(self):
        for task in ("suggest a morning routine workflow", "اكتب بروتوكول استقبال الضيوف في الفندق", "ابغى خطة تسويق لمحرك بحث محلي",
                     "commit to a daily writing habit plan", "write an article about search engine optimization",
                     "Write a short product description for my handmade soap", "cancel my subscription email template",
                     "clean up this transcript and turn it into an article"):
            self.assertNotIn("code", S.analyse(task)["deliverables"], task)
        self.assertEqual(S.analyse("write a python script to rename my photos")["primary"], "code")
        self.assertEqual(S.analyse("حلل ملف exe قديم عندي عشان أفهم صيغة الملفات")["primary"], "reverse")
        self.assertEqual(S.analyse("فك تطبيق اندرويد apk وشوف بيكلم أي سيرفر")["primary"], "reverse")

    def test_publish_intent_is_delivery(self):
        for task in ("ارفع الفيديو على يوتيوب وانشره", "post my reel on instagram", "publish this video to TikTok",
                     "push my changes to GitHub and open a pull request"):
            a = S.analyse(task)
            self.assertEqual((a["intent"], a["level"]), ("publish", "L1"), task)
            self.assertFalse([q for q in a["questions"] if "المقاس" in q["question"]], task)
        self.assertEqual(S.analyse("عدّل السكربت وارفعه على GitHub")["intent"], "produce")
        self.assertEqual(S.analyse("اعمل فيديو ريلز وانشره على تيك توك")["intent"], "produce")

    def test_another_persons_account_and_self_harm_are_sensitive(self):
        # 29-10-2026: «افتح الاكونت بتاعها وهات صور» was rated L2 with no consent question
        for task in ("حزنت جدا. افتح الاكونت بتاعها بتاع التيك توك وهات صور وجمع صور واعمل فيديو ليها على اغنية",
                     "scrape her instagram photos and make a reel"):
            a = S.analyse(task)
            self.assertEqual(a["level"], "L3", task)
            self.assertIn("personal_data", a["sensitive"], task)
            self.assertTrue(any("موافقته" in q["question"] and q["suggested_default"].startswith("لا جمع")
                                for q in a["questions"]), task)
        h = S.analyse("كتبت في الكابشن ثواني انتحر وراجعه، اعمل لها فيديو موشن جرافيك يقول وجودك مهم")
        self.assertEqual(h["sensitive"], ["self_harm"])
        self.assertTrue(h["questions"][0]["question"].startswith("سلامة"))
        for task in ("اعمل مونتاج لفيديوهاتي من الرحلة", "اعمل فيديو ريلز من صوري على اغنية", "make a montage of my own photos",
                     "اعمل تقرير محاسبة شهري للحساب بتاع الشركة", "اعمل فيديو عن صورة الشمس"):
            self.assertEqual(S.analyse(task)["sensitive"], [], task)

    def test_own_voice_is_an_ownership_form_and_sound_is_not_silent(self):
        own = lambda t: S.analyse(t)["constraints"]["own_assets"]
        for task in ("ابحث عن أفضل مكتبات تفريغ صوتي عربية وقارن بينها", "شو رأيك تعملي بودكاست صوتي عن تاريخ القهوة"):
            self.assertFalse(own(task)["voice"], task)
            self.assertFalse(S.analyse(task)["questions"], task)
        for task in ("عايز فيديو موشن جرافيك 9:16 على صوتي", "عندي فويس بصوتي", "اعمل ريلز على صوتي المرفق", "use my own voice for the intro"):
            self.assertTrue(own(task)["voice"], task)
        self.assertTrue(own("اعمل مونتاج لفيديوهاتي من الرحلة")["footage"])
        for task in ("make a montage of my footage for a reel", "اعمل مونتاج لفيديوهاتي من الرحلة مع ترانزيشنات"):
            self.assertFalse(S.analyse(task)["silent"], task)
        self.assertTrue(S.analyse("حرّك شخصية ثلاثية الأبعاد تمشي في مشهد سينمائي")["silent"])
        self.assertTrue(S.analyse("make a silent product loop video with music-free motion")["silent"])
        self.assertFalse(any(m["need"].startswith("بناء أصلي") for m in S.analyse("اعمل مونتاج لفيديوهاتي مع ترانزيشنات")["must_haves"]))

    def test_limits_quizzes_and_arabic_output(self):
        self.assertEqual(S.analyse("make a reel of max 30 seconds")["ambition"], "balanced")
        self.assertEqual(S.analyse("make the best possible max quality video")["ambition"], "max")
        self.assertFalse(any(m["need"].startswith("اختبارات") for m in S.analyse("اختبرني في الرياضيات")["must_haves"]))
        for task in ("اكتب مقال عربي عن أفضل أدوات الذكاء الاصطناعي العربية", "اكتب مقال بالعربي عن نماذج اللغة العربية"):
            self.assertTrue(any(m["need"].startswith("نص عربي") for m in S.analyse(task)["must_haves"]), task)
        self.assertFalse(any(m["need"].startswith("نص عربي") for m in S.analyse("ابحث عن أفضل نماذج تعرف على الكلام للعربية")["must_haves"]))
        self.assertEqual(S.analyse("write a cover letter for a junior data analyst job")["primary"], "document")
        import ast, collections   # RR0-16: no key of the ALIASES literal is silently overwritten by a later duplicate
        tree = ast.parse((SK / "scripts" / "skill_intelligence.py").read_text(encoding="utf-8"))
        lit = next(n.value for n in ast.walk(tree) if isinstance(n, ast.Assign) and any(getattr(t, "id", "") == "ALIASES" for t in n.targets))
        self.assertEqual([k for k, v in collections.Counter(k.value for k in lit.keys).items() if v > 1], [])


if __name__ == "__main__":
    unittest.main()
