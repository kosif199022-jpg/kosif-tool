# الاختبارات والجودة والأمان — QA & security (`quality`)

> مكتبة بروتوكول USIP v5.6، مولّدة بـ `scripts/smart_capabilities.py library` من `data/powers/*.json` و`data/tools.json`؛ لا تُحرَّر يدويًا. الدليل: [A28 اختيار القدرات](../protocol/A28-capability-routing.md) · [الفهرس](INDEX.md) · [النواة](../../PROTOCOL.md#متى-تفتح-الملاحق--appendix-triggers)

## الفهرس / contents

- [متى تستخدم هذه المجموعة / when](#متى-تستخدم-هذه-المجموعة--when)
- [الحالة بالأرقام / status](#الحالة-بالأرقام--status)
- [الأدوات القابلة للتشغيل / runnable tools](#الأدوات-القابلة-للتشغيل--runnable-tools)
- [العائلات / families](#العائلات--families)
- [كل القدرات / every power](#كل-القدرات--every-power)

## متى تستخدم هذه المجموعة / when

كلمات التوجيه: test verify validation audit qa security eval اختبار مراجعة توثيق أمان

خط العمل المقترح (هدف تصميم، لم يُختبر كوحدة واحدة): الجرد → التقييم → اختبارات الانحدار → إثبات النتائج

العضوية في المجموعة تصنيف للتوجيه، لا دليل على أن القدرات تعمل معًا: اربطها بخط عمل مختبر فقط.

## الحالة بالأرقام / status

| الحالة | العدد | المعنى |
|---|---:|---|
| `proven` | 94 | ✅ proven: a proof exists in the catalog; still check its requirements here before calling it ready |
| `ready` | 58 | 🟢 ready: runnable without setup according to the catalog |
| `documented` | 195 | 📄 documented: a described method; needs building or wiring before it runs |
| `seen` | 3 | 👁 seen: observed in a reference or demo, not executed here |
| `install` | 94 | 📦 install: needs a package, binary or model first |
| `key` | 15 | 🔑 key: needs an account, key or paid service (ask before any spend) |
| `idea` | 5 | 💡 idea: not built |
| **المجموع** | **464** | |

## الأدوات القابلة للتشغيل / runnable tools

| الأداة | ما تفعله | ابدأ بـ | الدليل |
|---|---|---|---|
| `agent-guard` | حارس الوكيل: فحص الأوامر قبل تشغيلها وكشف الأسرار وخطة فروع متوازية | `python3 scripts/agent_guard.py rules` | tested-here |
| `anchor-gate` | بوابة حفظ الحقائق عند إعادة الصياغة | `python3 scripts/anchor_gate.py --before proofs/general-writing/pairs/en_before.txt --after proofs/general-writing/pairs/en_after_drift.txt --text` | tested-here |
| `atlas-audit-synthesis` | تحويل مراجعة الأطلس إلى بيان مُراجَع | `python3 scripts/atlas_audit_synthesis.py --records ./out/atlas-audit-private/records.json --rea-dir ./out/rea --manifest-out ./out/manifest.json --report-out ./out/atlas-reviewed-audit.md` | untested |
| `atlas-body-audit` | مراجعة ساكنة لنصوص مهارات الأطلس | `python3 scripts/atlas_body_audit.py --index ./atlas-index.json --out ./out/atlas-audit-private --limit 200` | tested-here |
| `atlas-external-bridge` | بحث مهارات أطلس الخارجية | `python3 scripts/atlas_external_bridge.py stats --index ./atlas_index.json --copyleft-index ./atlas_copyleft_index.json` | tested-here |
| `atlas-metadata-audit` | تدقيق بيانات أطلس الوصفية | `python3 scripts/atlas_metadata_audit.py --index ./atlas_index.json --copyleft ./atlas_copyleft_index.json --output ./out/atlas_audit.json` | tested-here |
| `blender-cycles-render` | رندر Cycles إلى فيديو مُتحقَّق منه | `python3 scripts/blender_cycles_render.py doctor` | tested-here |
| `book-methods` | مناهج مستخلصة من الكتب: التفكير الجانبي والهندسة العملية والأدلة البايزية والشخصية وفحوص المحاسبة ووضوح البرومنت | `python3 scripts/book_methods.py search "شخصية حوار"` | tested-here |
| `build-chapters` | مولّد فصول العائلات | `python3 scripts/build_chapters.py` | untested |
| `capability-runtime-router` | موجّه القدرات التنفيذية | `python3 scripts/capability_runtime_router.py --task "حلل فيديو مرجعي وأنتج مونتاج مشابه بأصولي" --limit 5 --json` | tested-here |
| `catalog-evidence-audit` | تدقيق أدلة الكتالوج | `python3 scripts/catalog_evidence_audit.py` | tested-elsewhere |
| `charter-ingest` | إدخال قائمة الميثاق: مجلس الخبراء 500 فهرسًا للاستشارة | `python3 scripts/charter_ingest.py roster.txt --out data/experts_500.json` | tested-here |
| `check-skill` | فحص سلامة المهارة | `python3 scripts/check_skill.py` | untested |
| `cinematic-broll-render` | تصيير لقطات B-roll بحركة كاميرا | `python3 scripts/cinematic_broll_render.py --edl ./edl.json --manifest ./clips.json --audio ./voice.wav --out ./out/master.mkv --width 1080 --height 1920` | tested-here |
| `council` | مجلس البرو: خمسة متعارضين أو مجلس مناسب من 100 شخصية، ثلاث جولات وحكم بالدرجات | `python3 scripts/council.py plan "اعمل ريلز دعاء" --dir out/demo/council --options A,B,C` | tested-here |
| `creative-quality-gate` | بوابة جودة خطة المونتاج | `python3 scripts/creative_quality_gate.py ./my-project/src/plan.json --out ./out/quality-audit.json` | tested-here |
| `differential-exam` | مصحّح الامتحان الخفي التفاضلي | `python3 scripts/differential_exam.py seal ./exam --out ./exam-seal.json` | tested-here |
| `kosif-remote-commander` | خادم KOSIF Remote Commander | `python3 scripts/kosif_remote_superpowers.py doctor` | tested-here |
| `local-project-audit` | فحص المشروع المحلي دون تشغيل | `python3 scripts/local_project_audit.py ./my-project` | tested-here |
| `package-skill` | تحزيم المهارة للرفع إلى claude.ai | `python3 scripts/package_skill.py` | tested-here |
| `prompt-lab` | مختبر البرومبت | `python3 scripts/prompt_lab.py kinds` | tested-here |
| `prompt-pack` | حزمة المطالبات: كل مطالبة في كتلة كود قابلة للنسخ مع فحص يحذّر فقط | `python3 scripts/prompt_pack.py build prompts.json --out out/demo/prompts --engine midjourney` | tested-here |
| `reel-factory` | مصنع الريلز: صوت وتوقيت كلمات ولقطات مرخصة ← ريلز 9:16 مفحوص | `python3 scripts/reel_factory.py plan --audio ./voice.m4a --audio-rights owned --words ./words.json --shots-manifest ./stock/manifest.json --shot-ids 17928486,8165467,20382699 --title "دعاء يوم الخميس" --handle @kosif` | tested-here |
| `relabel-proofs` | إعادة تصنيف نطاق الأدلة | `python3 scripts/relabel_proofs.py` | untested |
| `render-html` | محوّل HTML إلى فيديو MP4 | `node resources/motion-runtime/render_html.cjs --in ./film.html --out ./out/film.mp4 --fps 30 --audio ./voice.wav` | tested-elsewhere |
| `repo-check-originality` | فاحص أصالة الملفات الإبداعية | `python3 tools/check_originality.py --briefs ./briefs/ --texts ./source-texts/` | untested |
| `repo-import-briefs` | استيراد الملفات الإبداعية | `python3 tools/import_briefs.py ./briefs/` | untested |
| `repo-render-html` | محوّل حتمي من HTML إلى فيديو MP4 | `node tools/render_html.cjs --in starters/html-canvas/index.html --out ./out/film.mp4 --fps 30 --audio ./voice.mp3` | tested-elsewhere |
| `repo-validate` | فاحص سلامة أطلس الأنماط | `python3 tools/validate.py` | tested-here |
| `repo-verify-video` | بوابة فحص تسليم الفيديو | `python3 tools/verify_video.py ./out/film.mp4 --aspect 9:16 --fps 30 --duration 12 --audio ./voice.mp3 --json ./out/report.json` | tested-here |
| `skill-layout` | خريطة ترتيب المهارة | `python3 scripts/skill_layout.py build` | tested-here |
| `source-scout` | مستكشف مصادر المجتمع | `python3 scripts/source_scout.py check` | tested-here |
| `sources-index` | فهرس المصادر: الذاكرة الفهرسية لمرفقات المستخدم داخل مجلد العمل | `python3 -I scripts/sources_index.py add charter.txt --dir ../../../out/demo` | tested-here |
| `tell-scan` | فاحص العبارات الكتابية النمطية | `python3 scripts/tell_scan.py proofs/general-writing/samples/en_ai.txt` | tested-here |
| `verify-video` | بوابة فحص تسليم الفيديو | `python3 scripts/verify_video.py ./in.mp4 --aspect 9:16 --fps 30 --duration 15 --json ./out/report.json` | tested-here |
| `video-workflow-bridge` | جسر سير عمل الفيديو | `python3 scripts/video_workflow_bridge.py paper-edit templates/ik-wave-words.json --keep "1-3,5" --fps 30 --out ./out/paper-edit.json` | tested-here |

الأوامر نسبية إلى مجلد المهارة (أو جذر المستودع لأدوات `tools/`)؛ `python3 scripts/hub.py tool <id>` يعطي كل الأوامر والمتطلبات والحدود.

## العائلات / families

| العائلة | القدرات | الفصل |
|---|---:|---|
| `api-testing` | 22 | [api-testing.md](../powers/api-testing.md) |
| `qa-verification` | 384 | [qa-verification.md](../powers/qa-verification.md) |
| `security-safety` | 23 | [security-safety.md](../powers/security-safety.md) |
| `verification-evals` | 35 | [verification-evals.md](../powers/verification-evals.md) |

## كل القدرات / every power

مرتبة بالحالة ثم العائلة ثم المعرّف. `hub.py` و`skill_intelligence.py deep <ID>` يعطيان بطاقة القدرة كاملة بدليلها.

| المعرّف | الاسم | English | الحالة | المتطلبات |
|---|---|---|---|---|
| `API-01` | مجموعة طلبات كملفات نصية في git | Author an API collection as git-tracked Bru files | proven | npm:bruno |
| `API-02` | تشغيل المجموعة كاختبارات قبول | Run a collection as automated acceptance tests | proven | npm:bruno |
| `API-03` | تأكيدات تعريفية على الاستجابة | Declarative response assertions | proven | npm:bruno |
| `API-04` | اختبارات Chai على الاستجابة | Chai-style tests on the response | proven | npm:bruno |
| `API-05` | تسلسل الطلبات بحفظ المتغيرات | Request chaining via saved variables | proven | npm:bruno |
| `API-06` | المصادقة: Bearer وBasic وOAuth2 | Auth: Bearer, Basic, OAuth 2.0 and more | proven | key:unspecified, npm:bruno |
| `API-07` | متغيرات على مستويات متعددة | Variables at every scope | proven | npm:bruno |
| `API-08` | الأسرار خارج الملفات | Secrets kept out of the files | proven | npm:bruno |
| `API-09` | سكربتات ما قبل وبعد الطلب | Pre-request and post-response scripts | proven | npm:bruno |
| `API-10` | تشغيل مدفوع بالبيانات من CSV/JSON | Data-driven runs from CSV/JSON | proven | npm:bruno |
| `API-11` | تقارير JSON وJUnit وHTML | JSON, JUnit and HTML reports | proven | npm:bruno |
| `API-12` | بوابة فشل لخط CI | CI failure gate | proven | npm:bruno |
| `API-13` | استيراد OpenAPI إلى مجموعة | Import OpenAPI into a collection | proven | npm:bruno |
| `API-14` | توليد توثيق HTML للـAPI | Generate standalone HTML API docs | proven | npm:bruno |
| `API-15` | تحويل Postman وInsomnia | Convert Postman and Insomnia collections | proven | npm:bruno |
| `QA-01` | بوابة التسليم | Delivery gate (inspect) | proven | python3 |
| `QA-02` | فحص الحلقة بلا درزة | Seamless loop check | proven | python3 |
| `QA-03` | بوابة فحص التسليم | verify_video delivery gate | proven | ffmpeg, python3 |
| `QA-04` | فحص التسليم من الملف نفسه | Delivery QA from the decoded file | proven | ffmpeg |
| `QA-05` | سياسة الإطارات الصادقة | Honest-frame capture policy | proven | ffmpeg, node, chromium |
| `QA-06` | كشف تغير المشهد | Scene-change detection | proven | ffmpeg |
| `QA-07` | تدقيق القص على الإيقاع | Cut-to-beat audit | proven |  |
| `QA-08` | إصلاح انزياح التوقيت عند الدمج | Concat drift fix: encode once | proven | ffmpeg |
| `QA-09` | عتبات التباين وتدقيق اللوحة | Contrast thresholds and palette audit | proven | python3, npm:axe |
| `QA-10` | عقد تباين الألوان والمسافة الإدراكية | Palette contrast + perceptual-distance contract | proven | npm:axe |
| `QA-11` | عقد الحركة المخفضة | Reduced-motion contract | proven |  |
| `QA-12` | اختبار عقد الحركة | Motion contract test | proven | node |
| `QA-13` | اختبار عقد التجاوب | Responsive layout contract test | proven | node |
| `QA-14` | فحص الأصول والصياغة الثابت | Static asset and syntax check | proven | node |
| `QA-15` | اختبار تثبيت الثيم | Theme lock test (dashboard/editorial) | proven | node, fonts:arabic |
| `QA-16` | محاكاة حركة المناطق من المرجع | Regional motion clone (4x4 block motion) | proven |  |
| `QA-17` | اختبارات CI | CI and regression tests | proven | python3, npm:esbuild |
| `QA-18` | سياسة تقليل الحركة | Reduced-motion policy | proven |  |
| `QA-19` | اختبارات توحيد الهوية | Single-identity enforcement tests | proven | node |
| `QA-20` | مقياس انحراف الهوية | Identity drift ratchet (identity_audit) | proven | node |
| `QA-21` | اختبارات وجود أصول الهوية وخفتها | Brand art presence & weight tests | proven | node |
| `QA-22` | اختبار محرك ثلاثي الأبعاد دون متصفح | 3D engine unit test without a browser | proven | chromium, npm:three |
| `QA-23` | مدقق ملخص المشروع | Brief validator | proven |  |
| `QA-24` | عبارة اعتماد التصدير النهائي | Typed final-render approval phrase | proven | node, python3 |
| `QA-25` | حزمة الاختبارات | Unit test suite (24 tests) | proven | node |
| `QA-26` | علم التحقق التاريخي | Historical fact-check flag | proven |  |
| `QA-27` | خصائص قابلة للتعديل وملف مشاهد داخل التركيب | Editable props + reel JSON inside the composition | proven |  |
| `QA-28` | كشف الانتقالات: قطع وذوبان وغطس | Transition detection: cut, dissolve, dip | proven |  |
| `QA-29` | حلّال إنشائي بتحقق يدوي وبوابات ثقة | Structural solver with hand-calc and trust gates | proven |  |
| `QA-30` | اختبارات حتمية لهندسة الفيلم | Deterministic geometry tests for a film function | proven | node |
| `QA-31` | اختبار المشغل بمحاكاة DOM | Mocked-DOM player test harness | proven | node |
| `QA-32` | بوابة قابلية قراءة النص | Readability gate for on-screen text | proven |  |
| `QA-33` | قواعد نص المشاركة | Share-copy rules | proven |  |
| `QA-34` | توليد القوالب مع فحص | Template generation + lint gate | proven |  |
| `QA-35` | حلقة مراجعة مشهد بمشهد مع الكتابة للمصدر | Scene-by-scene review loop with write-back | proven |  |
| `QA-36` | عميل التصيير البعيد وبوابات الأمان | Remote render client and bridge safety gates | proven |  |
| `QA-37` | مدقق الخطة | Plan validator | proven |  |
| `QA-38` | قواعد التحقق من manifest | Manifest validation rules | proven |  |
| `QA-39` | حماية الواجهة المحلية من المواقع الأخرى | Cross-origin guard for the local API | proven |  |
| `QA-40` | صفحة المراجعة مشهدًا بمشهد | Scene-by-scene review page (KOSIF Review / Motion OS player) | proven |  |
| `QA-41` | منظف مشروع Studio | Studio project sanitiser | proven | node |
| `QA-42` | مدقق مواصفة المشهد الصارم | Strict SceneSpec validator (25 fields) | proven | python3 |
| `QA-43` | مدقق برومبت الصور والفيديو | Image/video prompt linter | proven | python3 |
| `QA-44` | عقد التنفيذ البصري | Visual execution contract (build/verify/repair/jev) | proven |  |
| `QA-45` | تدقيق صفحات الويب | Static web/HTML audit | proven | python3, chromium |
| `QA-46` | بوابة فحص الجودة وإيصال الإنتاج | ffprobe delivery gate + receipt | proven | ffmpeg |
| `QA-47` | اختبارات A/B | A/B test plan and read | proven | python3 |
| `QA-48` | أفضل وقت نشر | Best time from own analytics | proven | python3 |
| `QA-49` | تجارب A/B | A/B plan and read | proven | python3 |
| `QA-50` | فحص الإطارات الآلي | Frame QA: black/white/freeze/cut scan | proven | python3 |
| `QA-51` | بوابة الستوري بورد | Storyboard gate | proven | python3 |
| `QA-52` | دليل رندر demo2d | demo2d proof render | proven |  |
| `QA-53` | فحص البرومبت | Image prompt lint | proven |  |
| `QA-54` | فحص الفيديو المولد | Post-generation video QA | proven |  |
| `QA-55` | فحص أمان الكود قبل التشغيل | Code safety gate before running pasted code | proven | python3 |
| `QA-56` | تمييز الصورة الفوتوغرافية عن الرسم المسطح | Photo vs flat-art classifier | proven |  |
| `QA-57` | فحص الحتمية والذوق | Composition lint (determinism + contract + taste) | proven | python3 |
| `QA-58` | لوحات النقد | Critique contact sheets | proven | python3 |
| `QA-59` | قاعدة الصدق في التوقيت | Truthful-timing rule | proven |  |
| `QA-60` | مجموعة اختبارات الموشن | Motion test suite | proven | chromium, imagemagick, pip:opencv |
| `QA-61` | أفلام مرجعية مقاسة | Shipped-film benchmark (measured) | proven |  |
| `QA-62` | فحص الأصالة | Originality check | proven | python3 |
| `QA-63` | لوحة معاينة 8 إطارات | Contact-sheet preview (--preview) | proven | ffmpeg, node, chromium |
| `QA-64` | سطر التحقق بعد الرندر | Post-render ffprobe VERIFY line | proven | ffmpeg |
| `QA-65` | تقرير الفحص بـ 16 بندًا | TEST_REPORT 16-check QA template | proven | ffmpeg |
| `QA-66` | فحص المستودع والإحصاءات | kosif.py validate / stats | proven | python3 |
| `QA-67` | مجموعة الاختبارات | Test suite (node --test + unittest) | proven | ffmpeg, node, python3 |
| `QA-U01` | طبقة الرسوم وحدها من رندرين | Graphics-only layer from two aligned renders | proven |  |
| `QA-X01` | مسح الإطارات بعد الترميز | Frame-diff scan of the encoded file (OUTLIER · JUMP · FREEZE · DEAD AIR · TIMING) | proven | ffmpeg, pip:numpy |
| `QA-X02` | مقياس الهواء الميت | Dead-air meter (block maximum) | proven | chromium |
| `QA-X03` | الحجم الفعلي وأسوأ بكسل تباين | Effective text size and worst-pixel contrast by double render | proven | pip:pillow, npm:axe |
| `QA-X04` | فحص اتجاه الزوم عبر القطع | Zoom-direction check across cuts (log velocity) | proven |  |
| `QA-X08` | فحص المطابقة المرئي: الرندر مقابل إطارات المرجع | Fidelity check: composite the render against the reference frames | proven | node, chromium, pip:pillow, fonts:arabic |
| `QA-X09` | بطاقة نتائج اصطناعية بحقيقة أرضية لخط أنابيب المحاكاة | Synthetic ground-truth scorecard for the mimic pipeline | proven | ffmpeg, chromium, pip:numpy, pip:pillow |
| `SEC-14` | تشغيل أدوات غريبة في بيئة نظيفة | Run foreign tools in a scrubbed sandbox | proven | python3, key:graphify |
| `CHECK-02` | بوابة ما بعد الرندر | Postcondition gate on the delivered file (ffprobe / verify_video.py / measured sync) | proven | ffmpeg, pip:office |
| `CHECK-03` | انظر إلى المخرَج بعينك | Look at the output: contact sheets, frames, screenshots | proven | ffmpeg, python3, chromium |
| `CHECK-22` | لقطة الفهرس والمدقِّق | Catalog snapshot: powers.py stats + repo validator | proven | python3 |
| `CHECK-23` | بوابة السجلات الحتمية | Deterministic record gate for the power catalog (mutation-tested) | proven |  |
| `QA-100` | مراجعة المشاهد | Review loop | ready |  |
| `QA-101` | فحص البيئة | Environment check | ready | python3 |
| `QA-102` | شارات حالة البيئة | Environment status pills | ready | ffmpeg, pip:faster-whisper |
| `QA-103` | المراجعة: معاينة شبحية للعناصر المنقولة | Review: ghost preview of moved elements | ready |  |
| `QA-104` | المراجعة: ملاحظات مثبتة على الإطار | Review: pinned frame notes | ready |  |
| `QA-105` | المراجعة: إعادة التحميل التلقائي والروابط العميقة | Review: auto-reload on new version and deep links | ready |  |
| `QA-106` | تقرير التصدير | Export report object | ready |  |
| `QA-107` | قياس الحدة والضجيج | Sharpness and noise measurement | ready |  |
| `QA-108` | مقارنة صورتين لاستمرارية اللقطات | A/B image comparison for shot continuity | ready | python3 |
| `QA-109` | لوحة فحص 4×4 من الإطارات | Contact sheet 4x4 (every 15th frame) | ready | ffmpeg |
| `QA-110` | فاحص جودة الفيديو | Video QA inspector (black/freeze/loudness) | ready | ffmpeg, python3 |
| `QA-111` | تحليل صوتي مقاس | Measured audio analysis (BS.1770 loudness, true peak, BPM, spectrum) | ready | ffmpeg, pip:matplotlib |
| `QA-112` | تحليل صورة مقاس | Measured image analysis | ready | pip:numpy, pip:pillow |
| `QA-113` | مقارنة إطارين | A/B frame comparison | ready | python3 |
| `QA-114` | لوحة معاينة المصادر | Source contact sheet for footage triage | ready | ffmpeg, pip:pillow |
| `QA-115` | أوراق المراجعة | Critique sheets: contact, phone, strip + review.md | ready | python3 |
| `QA-116` | فحص مسبق لمهمة الوسائط | Media job preflight (proplan) | ready | python3 |
| `QA-117` | فحص الملفات والدفعات والخطوط | Probe, batch and Arabic font scan | ready | python3 |
| `QA-118` | فحص أمان الكود الملصوق | Pasted-code safety scan + sandbox | ready |  |
| `QA-119` | أوراق مراجعة المحاكاة | Review contact sheets (shots, transitions, texts, side by side) | ready |  |
| `QA-120` | فحص المصدر بـ ffprobe | ffprobe source inspection | ready | ffmpeg, python3 |
| `QA-121` | مشغل الكود الآمن | Sandboxed AI code runner | ready | python3 |
| `QA-122` | مقياس طاقة الحركة | Motion energy meter vs reference | ready | python3 |
| `QA-123` | فحص الملف | Probe media | ready | python3 |
| `QA-124` | أدوات المعاينة الحية | Live preview controls (play/scrub/?t=) | ready |  |
| `QA-125` | فاحص أصالة النصوص | Brief originality n-gram checker | ready | python3 |
| `QA-68` | فحص إزاحة مزامنة الشفاه بالارتباط المتقاطع | Lip-sync offset check by cross-correlation | ready |  |
| `QA-69` | حارس القيم الشاذة | NaN/Inf guard pass | ready |  |
| `QA-70` | فحص التركيب | Composition lint rules | ready | python3 |
| `QA-71` | قياس طاقة الحركة | Motion energy measure | ready | python3 |
| `QA-72` | كشف مكتبات الحركة ونموذج التفاعل | Motion-library and interaction-model detection | ready | npm:three, npm:gsap, npm:lottie, npm:animejs |
| `QA-73` | مقارنة صور بدون اعتمادات | Dependency-free PNG visual diff | ready | node, pip:numpy, pip:pillow |
| `QA-74` | إعدادات التقاط واجهة قابلة للتكرار | Reproducible UI capture settings | ready | chromium |
| `QA-75` | التقاط إطارات مرجعية لمطابقة الأسلوب | Reference capture for style matching | ready | ffmpeg |
| `QA-76` | ورقة إطارات الكلمات وبوابة تزامن الضربات | Word-frame sheet and hit-sync gate | ready |  |
| `QA-77` | قراءة بيانات التوليد المضمنة | Embedded generation metadata readback | ready | pip:pillow |
| `QA-78` | وثيقة الهوية المولدة من الرموز | Identity doc generated from tokens | ready | python3 |
| `QA-79` | مسح بصري بـ Playwright | Playwright visual sweeps (desktop + 390/320px phones) | ready | node, chromium |
| `QA-80` | بوابة المعاينة قبل التصدير | Preview-before-final-render gate | ready | python3 |
| `QA-81` | إيصال الفحص الفني | ffprobe QA receipt | ready | ffmpeg, python3 |
| `QA-82` | إثبات التغير الزمني بالبصمة | Temporal-change frame-hash proof | ready | ffmpeg |
| `QA-83` | تعليم المقاطع الخطرة نصياً | Text-risk clip flagging | ready |  |
| `QA-84` | تحديد موقع عنصر في صورة بشبكة مرقمة | Grid-index visual grounding (locate X in an image) | ready | node |
| `QA-85` | كوسف: بوابة التسليم وقياسات الحركة | KOSIF: delivery inspect gate and motion measures | ready | python3 |
| `QA-86` | فحص الملفات والخطوط | probe / fonts | ready | python3 |
| `QA-87` | بوابة التسليم | inspect delivery gate | ready | python3 |
| `QA-88` | ورقة المراجعة | sheet contact review | ready | python3 |
| `QA-89` | فحص التركيب | lint composition | ready | python3 |
| `QA-90` | دراسة مرجع | study reference | ready | python3 |
| `QA-91` | فحص الحلقة | loopcheck | ready | python3 |
| `QA-92` | فحص المقروئية | readable | ready | python3 |
| `QA-93` | تثبيت الغلاف | poster bake | ready | python3 |
| `QA-94` | بوابة العربية | Arabic delivery gate | ready | python3 |
| `QA-95` | صفحة المراجعة | Review page (Motion OS) | ready | python3 |
| `QA-96` | مشغل المعاينة | Self-playing preview player | ready | npm:hyperframes |
| `QA-97` | وسوم الأمانة للمحاكاة التوضيحية | Honesty labels for illustrative simulations | ready |  |
| `QA-98` | ورقة لقطات وفحص السرعة | Contact sheet + speed check | ready |  |
| `QA-99` | دراسة فيلم مرجعي | Reference study | ready |  |
| `API-19` | تعاون عبر git بلا سحابة | Git-native collaboration, no cloud | documented | npm:bruno |
| `API-20` | مكتبات مدمجة في السكربتات | Built-in libraries in scripts | documented | npm:bruno |
| `API-21` | إرسال طلب فرعي من سكربت | Send a sub-request from a script | documented | npm:bruno |
| `API-22` | صيغة OpenCollection وBru Lang | OpenCollection YAML and Bru Lang | documented | npm:bruno |
| `QA-231` | حلقة النقد ثلاث جولات | Critique loop ≥3 rounds | documented |  |
| `QA-232` | قياس إزاحة مزامنة الشفاه | GCC-PHAT lip-sync lag check | documented |  |
| `QA-233` | قواعد الأمانة في اللقطات | Honest capture rules | documented |  |
| `QA-234` | ورقة لقطات للمراجعة | Contact sheet review | documented | ffmpeg |
| `QA-235` | إطار مرجعي للمقارنة | Golden still regression | documented | chromium, npm:remotion |
| `QA-236` | إخفاء البيانات الحساسة في لقطات الواجهة | Privacy masking for UI footage | documented | ffmpeg |
| `QA-237` | فحص التسليم للفيديو | Delivery QA for web/social video | documented | ffmpeg, python3 |
| `QA-238` | مراجعة اللقطات الثابتة قبل الرندر | Stills-before-render review | documented | node, chromium |
| `QA-239` | بديل الحركة المخففة والإطار الثابت | Reduced-motion and static-frame fallback | documented | npm:gsap |
| `QA-240` | لا تخترع الرقم الذي يصنع الخطاف | Never invent the hook statistic | documented |  |
| `QA-241` | ترجمة مدمجة وحدود الوميض | Burned captions and photosensitivity limits | documented |  |
| `QA-242` | فحص تباين النص فوق الصورة | Text-over-photo contrast check | documented | pip:numpy, pip:pillow, npm:axe |
| `QA-243` | بوابات وضوح الإعلان الثابت | Static-ad legibility gates | documented | npm:axe |
| `QA-244` | انضباط اختبار الإبداعات | Creative testing discipline | documented | pip:hypothesis |
| `QA-245` | سلم تقييم مشاهد الخطاف | Hook scene scoring rubric | documented | ffmpeg |
| `QA-246` | بوابة فحص الملف المسلّم | Delivered-file QA gate | documented | ffmpeg |
| `QA-247` | مقياس الالتصاق SUCCESs | SUCCESs stickiness score | documented |  |
| `QA-248` | مراجعة الثمبنيل بست نقاط | Six-check thumbnail review | documented | pip:pillow |
| `QA-249` | اختيار ذكي للإطارات لمشاهدة الفيديو | Smart frame selection for watching videos | documented | ffmpeg, pip:numpy |
| `QA-250` | بحث تغليف نزيه | Honest packaging research | documented |  |
| `QA-251` | قائمة فحص قبل اعتماد الموشن | Pre-delivery motion QA checklist | documented | ffmpeg, python3 |
| `QA-252` | ضوابط الصدق لكل فئة موشن | Category truth guardrails | documented |  |
| `QA-253` | تراكب شفاف 50/50 لكشف الفروق الدقيقة | Onion-skin overlay for subtle visual diffs | documented | ffmpeg, pip:pillow |
| `QA-254` | ترتيب استبعاد النسخ المولدة | Elimination order for generated variants | documented | pip:pillow |
| `QA-255` | اختبار القوالب بمحتوى متطرف | Content-stress testing of templates | documented | chromium |
| `QA-256` | قياس الجهارة والذروة | Loudness / true-peak verification | documented | ffmpeg |
| `QA-257` | تحويل معدل إطارات متغير إلى ثابت | VFR to CFR fix for sync drift | documented | ffmpeg |
| `QA-258` | حد أمان الوميض | Flash-safety cap | documented |  |
| `QA-259` | حد أدنى لحجم الترجمة | Readable caption size floor | documented |  |
| `QA-260` | فحص جودة التفريغ | Transcript quality gate | documented | pip:faster-whisper |
| `QA-261` | قياس التلوين بالمقاييس | Scope-based grade measurement | documented | ffmpeg, pip:numpy |
| `QA-262` | تحديث العناصر بعد إعادة القص | Recut propagation | documented |  |
| `QA-263` | جدول التحقق من الرندر النهائي | Final render verification table | documented | ffmpeg |
| `QA-264` | قاعدة المشاهدة مرتين | Watch twice rule | documented |  |
| `QA-265` | فحص جودة التفريغ وإعادة المحاولة | Transcript quality gate + retry | documented |  |
| `QA-266` | قياس دقة التفريغ وضبط الصمت | ASR WER and endpointing discipline | documented | ffmpeg |
| `QA-267` | صورة طيف وموجة للمراجعة | Spectrogram + waveform review image | documented | ffmpeg |
| `QA-268` | ترتيب الميكس والفحص | Mix order & listening checks | documented | ffmpeg |
| `QA-269` | تنبيه علو المؤثرات القصيرة | Short-SFX loudness caveat | documented |  |
| `QA-270` | حفظ الصوت الأصلي بنسخة | Preserve original audio via duplicate | documented |  |
| `QA-271` | علامات مراجعة للأحكام الذوقية | Review markers for subjective calls | documented |  |
| `QA-272` | فخ إعادة الإسناد في TSL | TSL reassignment pitfall | documented |  |
| `QA-273` | ميزانية أداء الشيدر | Shader cost budget | documented |  |
| `QA-274` | قائمة تحقق الريندر الأسود | Blender black-render checklist | documented | blender |
| `QA-275` | حدود التباين | WCAG contrast floors | documented | python3, npm:axe |
| `QA-276` | احترام تقليل الحركة | Reduced-motion respect | documented |  |
| `QA-277` | اختبار ثنائي الاتجاه | Bidi pseudo-locale stress test | documented |  |
| `QA-278` | لا تخترع رموزا | No invented glyphs | documented | pip:fonttools |
| `QA-279` | فحص النقط عند حافة القناع | Mask-edge dot check | documented |  |
| `QA-280` | التحقق من اللوك بالمقاييس | Scope-target look verification | documented | ffmpeg, pip:numpy |
| `QA-281` | قائمة مراجعة التحريك | Animation review checklist (contact/passing) | documented |  |
| `QA-282` | فحص الشفافية والهالات | Real alpha and halo checks | documented | pip:pillow |
| `QA-283` | تعليق الإشارة مقابل الضجيج | Signal-vs-noise annotation | documented |  |
| `QA-284` | حلقة فحص: قياس ثم حكم | Measure-then-judge figure QA loop | documented |  |
| `QA-285` | حالات ثابتة لاختبار الصور | Stable visual regression states | documented |  |
| `QA-286` | التحقق من تصيير الخرائط | Map render verification | documented |  |
| `QA-287` | تحقق من واجهات البيانات | Trust-but-verify data APIs | documented |  |
| `QA-288` | فحص عمى الألوان والرمادي | Colorblind and grayscale check | documented |  |
| `QA-289` | سجل المصدر والإفصاح عن الذكاء الاصطناعي | Provenance ledger and AI disclosure | documented |  |
| `QA-290` | منهج تدقيق الكثافة قبل وبعد | Before/after visual density audit method | documented |  |
| `QA-291` | سجل مصدر الأصول | Asset provenance ledger | documented |  |
| `QA-292` | قياس جهارة صوت المقدمة | Intro audio loudness (measured) | documented | ffmpeg |
| `QA-293` | ميزانية أداء الطبقة الزخرفية | Decorative-layer perf budget | documented |  |
| `QA-294` | ميثاق عدم الادعاء | No-false-claims honesty contract | documented | pip:higgsfield |
| `QA-295` | قائمة مراجعة الرندر | Render review checklist | documented |  |
| `QA-296` | فحص بوابات المحرر في CI | CI editorial gate check | documented | ffmpeg, node, python3, chromium |
| `QA-297` | مراجعة الإطار الأول والأوسط والأخير | First/middle/last frame review | documented | ffmpeg |
| `QA-298` | تصيير حتمي بدوكر | Docker deterministic render | documented | ffmpeg, chromium, docker, npm:hyperframes |
| `QA-299` | تشخيص صوت لا يمكن سماعه | Diagnose audio you cannot hear | documented | ffmpeg |
| `QA-300` | فخاخ HyperFrames | HyperFrames traps | documented | npm:gsap, npm:hyperframes |
| `QA-301` | حدود السرعة | Speed limits | documented |  |
| `QA-302` | طاقة اختلاف الإطارات | Frame-difference energy | documented |  |
| `QA-303` | قاعدة الصدق | Honesty rule | documented |  |
| `QA-304` | تقرير فحص التسليم لفيديو صوتي | Delivery QA report for a voice-driven render | documented |  |
| `QA-305` | حلقة النقد الثمانية | 8-criterion critique loop | documented |  |
| `QA-306` | قائمة جودة الحركة | LottieFiles quality checklist | documented | npm:lottie |
| `QA-307` | مراجعة بثلاث عدسات | Three-lens review receipt | documented |  |
| `QA-308` | إطارات المراجعة | Review frames (eight-second gate) | documented | python3 |
| `QA-309` | فحص الحتمية والذوق | Determinism and taste lint | documented | python3 |
| `QA-310` | بوابة التسليم | Delivery gate (black, freeze, LUFS, peak, exposure) | documented | python3 |
| `QA-311` | لوحة النقد | Critique sheet (frames + phone view) | documented | python3 |
| `QA-312` | معلومات الملف | File probe | documented | ffmpeg, python3 |
| `QA-313` | فحص البيئة | Environment doctor | documented | ffmpeg, pip:faster-whisper |
| `QA-314` | مخطط reel.json ومدققه | reel.json schema and checker | documented | ffmpeg, node |
| `QA-315` | بوابات جودة التسليم | Delivery quality gates (montage) | documented | imagemagick |
| `QA-316` | قائمة منع أخطاء التوليد | Generator failure-prevention checklist | documented |  |
| `QA-317` | أتمتة المتصفح ولقطات الفحص | Browser automation & screenshot QA (Playwright patterns) | documented | chromium |
| `QA-318` | مستويات القدرة وقواعد الصدق | Capability tiers & truth rules | documented |  |
| `QA-319` | قاعدة نظافة المصادر | Source hygiene rule (no burned-in text, logos, screen recordings) | documented |  |
| `QA-320` | حلقة النقد الذاتي | Critique loop rubric (8 criteria, >= 3 rounds) | documented | python3 |
| `QA-321` | تشخيص أعطال ffmpeg | ffmpeg troubleshooting table | documented | ffmpeg |
| `QA-322` | بوابات تسليم المونتاج | Editor delivery gates | documented | ffmpeg |
| `QA-323` | قياس بالـ Scopes عبر لقطات | Scope measurement via stills | documented | pip:pillow |
| `QA-324` | سجل العلامات الملوّنة | Resolve marker registry | documented |  |
| `QA-325` | كشف اللقطات الرديئة | Bad-segment detection | documented | ffmpeg |
| `QA-326` | فحص ما قبل الرندر | Pre-render checklist (Resolve) | documented |  |
| `QA-327` | بوابة الخطوط والألوان المحظورة | Banned-font / default-colour gate | documented | key:openai, fonts:arabic |
| `QA-328` | بوابة المقروئية | Readability gate | documented |  |
| `QA-329` | علامات التصميم الآلي | AI-design tells blacklist | documented |  |
| `QA-330` | بوابة الثماني ثوانٍ | Eight-second gate + weakest-beat gate | documented |  |
| `QA-331` | اختبار التجميد | Freeze test for fake motion | documented |  |
| `QA-332` | 2). تدقيق وإصلاح الإتاحة | Accessibility (WCAG 2 | documented | npm:axe |
| `QA-333` | فحص الادعاءات والأرقام والاقتباسات والاس | Fact-Checker & Verifier | documented |  |
| `QA-334` | تقييم مخرجات الذكاء الاصطناعي بأرقام تصم | LLM Judge & Eval Lab | documented |  |
| `QA-335` | تقييم أي ميزة ذكاء اصطناعي بأرقام | LLM Judge & Eval Suites | documented |  |
| `QA-336` | اختبارات تثبت أن الكود يعمل | Complete Testing Suite | documented |  |
| `QA-337` | اختبار الفهم بلا صوت | Silent-readability test | documented |  |
| `QA-338` | نسختان A/B | A/B thumbnail single-variable | documented | chromium |
| `QA-339` | قياسات الصورة | Image metrics by code | documented | pip:numpy, pip:pillow |
| `QA-340` | تقييم بخمس معايير | 5x20 critique score | documented |  |
| `QA-341` | حدّ نابض الأذن | Ear spring speed limit | documented |  |
| `QA-342` | قائمة جودة الحركة | Motion quality checklist | documented | npm:lottie |
| `QA-343` | الدقة وإتاحة الوصول | Meaning, data truth and accessibility | documented |  |
| `QA-344` | قائمة الفيديو القابل للتكرار | Reproducible video checklist | documented | python3 |
| `QA-345` | بوابة التسليم | Delivery inspect gate | documented | python3 |
| `QA-346` | معيار النقد بمراجعين | Two-reviewer critique rubric | documented |  |
| `QA-347` | العدسات الجمالية الاثنتا عشرة | Twelve aesthetic lenses | documented |  |
| `QA-348` | قائمة صيد العيوب | Failure hunt list | documented |  |
| `QA-349` | معاينة قبل الرندر النهائي | Preview-before-render approval gate | documented |  |
| `QA-350` | أخطاء الـ3D الشائعة | 3D anti-patterns | documented |  |
| `QA-351` | قائمة فحص الإعلان | Ad QA checklist | documented |  |
| `QA-352` | فحص الطباعة العربية | Arabic typography QA | documented |  |
| `QA-353` | فحص التزامن في ثلاث لحظات | Three-point sync spot check | documented |  |
| `QA-354` | أخطاء تحريك الشخصيات | Character anti-patterns | documented |  |
| `QA-355` | أخطاء الرسوم البيانية | Chart anti-patterns | documented |  |
| `QA-356` | أخطاء مشاهد الكود | Code anti-patterns | documented |  |
| `QA-357` | أخطاء التايبوغرافي الحركي | Kinetic-type anti-patterns | documented |  |
| `QA-358` | حد الوميض الآمن | Flash safety limit | documented |  |
| `QA-359` | أخطاء الجسيمات | Particle anti-patterns | documented |  |
| `QA-360` | قائمة فحص الرندر | Render QA checklist | documented |  |
| `QA-361` | أخطاء أفلام الهاتف | Phone anti-patterns | documented |  |
| `QA-362` | أخطاء أفلام الصور | Photo anti-patterns | documented | imagemagick |
| `QA-363` | أخطاء أفلام المنتج | Product UI anti-patterns | documented |  |
| `QA-364` | تقييم حدة المؤثرات | SFX high-frequency risk scoring | documented |  |
| `QA-365` | اختيار إطار الغلاف | Settled poster frame pick | documented | ffmpeg |
| `QA-366` | قاعدة الوصلة المتطابقة | Frame-identical seam rule | documented | ffmpeg |
| `QA-367` | فحص الوصلات | Seam QA pass | documented |  |
| `QA-P01` | إيصال تنفيذ مُتحقَّق منه: لا نجاح بلا دليل | Evidence receipt validator (no verified success without evidence) | documented | ffmpeg, python3 |
| `QA-P02` | حلقة مراجعة الرندر المحدودة | Bounded iterative render review (½-second frames, 2–4 rounds) | documented |  |
| `QA-X05` | ناقد بعين العميل | Client-proxy critic instead of a generic creative director | documented |  |
| `QA-X06` | لا قياسات مختلقة | Never fabricate measurements | documented | pip:librosa |
| `QA-X07` | سلم حالات مهمة الوسائط | Media-job status ladder and preflight classes | documented | ffmpeg, python3 |
| `SEC-01` | المحتوى الخارجي بيانات لا أوامر | Untrusted content is data, not instructions | documented |  |
| `SEC-02` | فحص النص المخفي | Hidden-text and payload scan | documented | network |
| `SEC-03` | تغليف المدخلات غير الموثوقة للنموذج | Wrap untrusted input before a model reads it | documented | claude:tools |
| `SEC-04` | افصل القارئ عن المنفّذ | Split the reader from the actor | documented |  |
| `SEC-05` | نظافة الأسرار | Secrets hygiene | documented | key:unspecified |
| `SEC-06` | البحث عن الأسرار المسرّبة | Leaked-secret scanning | documented | git, mcp:github, gitleaks |
| `SEC-07` | عند تسرّب سر | When a secret leaks | documented |  |
| `SEC-08` | مراجعة أمان للتغييرات | Security review of a change | documented | node |
| `SEC-10` | المهارات والإضافات سلسلة توريد | Skills, plugins and MCP servers are supply chain | documented |  |
| `SEC-11` | لا تثق بإعدادات مستودع غريب | Do not trust a foreign repo's agent config | documented |  |
| `SEC-12` | قواعد منع أساسية | Baseline deny rules | documented | network |
| `SEC-13` | أقل قدر من الصلاحية | Least agency | documented |  |
| `SEC-15` | حارس الأوامر المدمّرة | Destructive-command guard | documented |  |
| `SEC-16` | حلقة الموافقة على الرسائل الصادرة | Outbound approval loop | documented |  |
| `SEC-20` | سلّم الموافقة وأقل تصعيد | Approval ladder and least escalation | documented |  |
| `SEC-21` | تقطيع الأوامر وقواعد بادئة مختبرة | Command segmentation and tested prefix rules | documented |  |
| `SEC-22` | تصنيف مخاطر الحارس قبل الفعل | Guardian risk taxonomy before acting | documented |  |
| `SEC-23` | صدق تدهور العزل | Honest sandbox degradation | documented | python3 |
| `CHECK-01` | حلقة التحقق الثمانية | Verification loop (8 steps until done-criteria pass) | documented | ffmpeg |
| `CHECK-04` | التقييم الذاتي بخمسة محاور | Five-axis self-evaluation (accuracy, completeness, clarity, actionability, concision) | documented |  |
| `CHECK-05` | هاجم مخرَجك بنفسك | Red-team your own output (edge inputs + sceptical expert) | documented |  |
| `CHECK-06` | حلقة تحقق الكود | Code verification loop: build → types → lint → tests → secrets → diff | documented | node, python3, git, key:unspecified |
| `CHECK-07` | قاعدة التوقف | Stop rule: done means checks pass, or the budget ends with risks stated | documented |  |
| `CHECK-08` | سُلَّم الأدلة للادعاءات | Evidence ladder for claims (badges are earned, leased and downgraded) | documented |  |
| `CHECK-09` | الإيصال المنمَّط | Typed receipt after consequential actions | documented | ffmpeg |
| `CHECK-10` | كلمات الحالة الصادقة | Honest status words (stage by stage) | documented |  |
| `CHECK-11` | التقييم أولًا | Eval-first: capability evals + regression evals | documented |  |
| `CHECK-12` | pass@k مقابل pass^k | pass@k vs pass^k (any success vs always success) | documented |  |
| `CHECK-13` | بوابة الفشل القاطع | Hard-fail gate: one must-never-happen failure blocks release | documented |  |
| `CHECK-14` | انضباط المحكِّم | Judge discipline: assertions first, one criterion per judgement, cited evidence | documented | ffmpeg |
| `CHECK-15` | طريقة سانتا: مراجعان معزولان | Santa method: two isolated reviewers, both must pass | documented | claude:tools |
| `CHECK-16` | حلقة المولِّد والمقيِّم | Generator–evaluator loop (weighted rubric, threshold, iteration cap) | documented | chromium |
| `CHECK-17` | المتحقق العدائي | Adversarial verifier that defaults to 'refuted' | documented |  |
| `CHECK-18` | حلقة تحسين الأداء بالقياس | Benchmark-optimisation loop (one hypothesis per variant) | documented | pip:hypothesis |
| `CHECK-19` | فحص تصميم الحلقة | Loop design check before automating anything | documented |  |
| `CHECK-20` | اختبار الطفرات للمدقِّق | Mutation-test your validator (seed defects, count catches) | documented |  |
| `CHECK-21` | مصفوفة اختبار التفعيل | Trigger eval matrix for a skill (+ with/without A/B) | documented | claude:tools |
| `CHECK-24` | حلقة التطوير الذاتي للمهارة | Self-evolution loop for this skill (evolve with evidence) | documented | python3 |
| `CHECK-25` | دروس بموافقة ونطاق مشروع | Consent-scoped lessons (growth log) | documented |  |
| `CHECK-26` | سجل القرارات المتكرر | Decision ledger for repeated rollouts | documented |  |
| `CHECK-27` | تصنيف الأعطال وأصغر إصلاح | Failure taxonomy → smallest repair | documented | key:unspecified |
| `CHECK-28` | سجل الحادثة | Incident record: expected vs actual vs evidence | documented | ffmpeg, pip:pillow |
| `CHECK-29` | قواعد الإصلاح الذاتي | Self-repair rules: retry once, narrower; never relax a safety gate | documented |  |
| `CHECK-30` | حَكَم مغلق الخيارات مرتين بترتيب معكوس | Closed-set judge asked twice with reversed options, a 'none' option and a declared fallback | documented |  |
| `CHECK-31` | امتحان مختوم قبل العمل | Exam sealed before the work | documented | python3 |
| `CHECK-32` | خادم نموذج وهمي مسجِّل | Recording mock model server | documented | python3 |
| `CHECK-33` | قائمة سطح الملاحظة | Observable-surface checklist | documented |  |
| `CHECK-34` | المصحّح يعطي 100% على نفسه أولًا | Scorer must score 100% on itself first | documented | python3 |
| `CHECK-35` | ملاحظات استرداد صادقة وخط أساس | Honest recovery notes and a measured baseline | documented | npm:rea |
| `QA-228` | تعاقب حلقات تشغيل المعاينات في الشبكة | Staggered loop phases for live grids | seen |  |
| `QA-229` | مقارنة إعادة بناء لقطة بلقطة | Shot-for-shot remake comparison | seen | ffmpeg |
| `QA-230` | إغلاق حلقة بلا تقطيع | Seamless loop closure | seen |  |
| `API-16` | بروتوكولات متعددة | REST, GraphQL, gRPC, WebSocket, SOAP | install | npm:bruno |
| `API-17` | استيراد WSDL | Import a WSDL (SOAP) definition | install | npm:bruno |
| `QA-126` | فحص التباين عبر الزمن | WCAG contrast audit over time | install | chromium, npm:hyperframes, npm:axe |
| `QA-127` | فحص تجاوز النصوص على الخط الزمني | Layout inspect sweep | install | chromium, npm:hyperframes |
| `QA-128` | خريطة الحركة لتدقيق الكوريغرافيا | Animation map (choreography audit) | install | npm:gsap |
| `QA-129` | حزمة أسلوب بنطاقات إحصائية | Style pack with statistical bands | install |  |
| `QA-130` | قالب تحليل فيديو مرجعي | Reference-video breakdown template | install | ffmpeg, pip:faster-whisper |
| `QA-131` | اختبار الإطارات الذهبية بأداة odiff | Golden-frame regression with odiff | install | ffmpeg, node, pip:numpy, pip:pillow |
| `QA-132` | سجل ألوان العلامات | Marker colour registry | install |  |
| `QA-133` | مشاهدة فيديو مرجعي بالإطارات والتفريغ | Watch a reference video (frames + transcript) | install | ffmpeg, yt-dlp, pip:faster-whisper |
| `QA-134` | التحقق من تزامن القطع مع الضربة | Onset-sync verification | install | ffmpeg, pip:numpy, pip:librosa |
| `QA-135` | التعامل مع فقد جهاز GPU | WebGPU device-loss handling | install | chromium |
| `QA-136` | بوابات جودة الروتوسكوب | Rotoscope fidelity gates | install |  |
| `QA-137` | نظافة البيانات المكانية | Spatial data hygiene | install |  |
| `QA-138` | قياس مستوى الكلام والضوضاء | Speech level and noise-floor measurement | install |  |
| `QA-139` | اكتشاف القطعات في الفيديو | Footage shot/cut detection (reference probe) | install |  |
| `QA-140` | تحليل بصمة المرجع العميق | Style DNA deep reference study | install |  |
| `QA-141` | درجة التشابه مع المرجع وتصليحها | Fingerprint similarity score and auto-fix | install |  |
| `QA-142` | تقدير التكلفة وحد الصرف | Cost estimate and spending limit | install | key:video-gen |
| `QA-143` | نصايح الكوتش بضغطة | Coach tips with one-tap fixes (no AI) | install |  |
| `QA-144` | بوابة التسليم | Delivery gate | install |  |
| `QA-145` | صفحة فحص الربط | Integration health check page | install |  |
| `QA-146` | عرض المرجع والأصل والمنتج | Multi-monitor compare view | install |  |
| `QA-147` | رندر تجريبي سريع | Smoke render mode | install | python3 |
| `QA-148` | أمر: فحص ثابت | CLI: lint | install | npm:hyperframes |
| `QA-149` | أمر: فحص بصري | CLI: check | install | npm:hyperframes, npm:axe |
| `QA-150` | أمر: لقطات | CLI: snapshot | install | npm:hyperframes |
| `QA-151` | أمر: إطارات مفتاحية | CLI: keyframes | install | npm:hyperframes |
| `QA-152` | أمر: مقارنة | CLI: compare / grade-compare | install | npm:hyperframes |
| `QA-153` | قواعد الأداء | Performance rules | install |  |
| `QA-154` | حلقة المراجعة: خطة ثم رسومات ثم بناء ثم معاينة | Review loop: plan -> sketch sheet -> build -> final look | install | node |
| `QA-155` | تثبيت وترقية إصدار الأداة في المشروع | Pin and upgrade the project CLI | install | npm:hyperframes |
| `QA-156` | محظورات الحتمية | Determinism bans | install |  |
| `QA-157` | أخطاء الفحص الأولى الشائعة | Lint first-pass gotchas | install |  |
| `QA-158` | أمر فحص الخط الزمني | Timeline inspection command | install | npm:hyperframes |
| `QA-159` | انتقالات CSS محظورة | Banned CSS transitions | install |  |
| `QA-160` | سكربت خريطة الحركة للتدقيق | Animation map audit script | install | npm:gsap, npm:hyperframes |
| `QA-161` | أدوات تشخيص الحركة | Keyframe diagnostics CLI (keyframes / --shot / --ghost / strip) | install | npm:three, npm:hyperframes |
| `QA-162` | التحقق من الالتزام بالتصميم | Design adherence verification | install |  |
| `QA-163` | تقرير التباين من الإطارات | Contrast report from rendered frames | install | npm:axe |
| `QA-164` | فحص البنية الثابت | Lint (static) gate | install | npm:hyperframes |
| `QA-165` | الفحص في المتصفح: الأخطاء والتخطيط والحركة والتباين | Check (browser gate: runtime, layout, motion, WCAG contrast) | install | chromium, npm:hyperframes, npm:axe |
| `QA-166` | تأكيدات الحركة الجانبية | Motion sidecar assertions (*.motion.json) | install |  |
| `QA-167` | لقطات ثابتة لورقة الاتصال | Snapshot contact sheets | install | npm:hyperframes |
| `QA-168` | سطر تشخيص التصيير | Render diagnostics line (capture path) | install | ffmpeg |
| `QA-169` | مقارنة النسخ ودرجات اللون | Compare variants and color grades | install | npm:hyperframes |
| `QA-170` | سجل المشروع والتراجع لكل دورة | Project history undo per agent turn | install | npm:hyperframes |
| `QA-171` | معيار جودة المكونات والمساهمة | Component quality bar and contribution | install | npm:hyperframes |
| `QA-172` | فحص جودة النص المفرغ وتنظيفه | Transcript quality check and cleaning | install |  |
| `QA-173` | بوابة قرار الترجمة | Caption decision gate (refuse bad clips) | install | ffmpeg, pip:faster-whisper |
| `QA-174` | معاينة سريعة للإطارات المركبة | Fast composite preview frames (no render) | install | node |
| `QA-175` | بوابات فحص الترجمة | Caption render gates (timing / occlusion / overflow / hand-off) | install | chromium, npm:gsap |
| `QA-176` | أخطاء الترجمة المعروفة | Caption failure modes (learned) | install | chromium |
| `QA-177` | بوابة دقة حركة فيجما | Figma motion fidelity gate (motion-energy PSNR) | install | npm:hyperframes |
| `QA-178` | بوابة الإطارات المفتاحية | Keyframe gate frames | install | python3 |
| `QA-179` | مفاتيح إخفاء العناصر لتصحيح المشهد | Debug visibility toggles for heavy 3D scenes | install |  |
| `QA-180` | بناء المحاكاة وبوابة المقارنة | Mimic build + compare gate | install |  |
| `QA-181` | فخاخ المحاكاة | Mimic traps rules | install | ffmpeg |
| `QA-182` | معاينة وفحص القراءة | Preview + readability check | install |  |
| `QA-183` | مراجعة المستخدم | Review site markup | install |  |
| `QA-184` | التصيير النهائي والبوابة | Final render + inspect gate | install |  |
| `QA-185` | تحليل الفيديو | Video analyze breakdown | install |  |
| `QA-186` | مكتبة الأساليب | Batch style library | install |  |
| `QA-187` | رسم الموجة والطيف | Waveform + spectrum plot | install | pip:matplotlib |
| `QA-188` | شريط تقدم حقيقي من FFmpeg | Live render progress from ffmpeg -progress | install | ffmpeg |
| `QA-189` | تتبع أخطاء الشيدر بالعزل | Shader isolation debugging | install | chromium |
| `QA-190` | دراسة الفيديو المرجعي | Reference film study (boundaries, looks, text zones) | install |  |
| `QA-191` | فحص المطابقة بالإطارات والصوت | Mimic comparison QA (frames + audio correlation) | install |  |
| `QA-192` | مشغل معاينة داخل المتصفح | Built-in browser preview player | install | claude:browser |
| `QA-193` | بوابة الإطارات المفتاحية | Key frames gate | install | python3 |
| `QA-194` | قياس سرعة الحركة على الشاشة | On-screen speed gate (optical flow) | install | python3 |
| `QA-195` | حكم الواقعية للصور | Realism judge for still renders | install | python3 |
| `QA-196` | تحليل حدود اللقطات والمظهر | Shot boundary and look analysis | install |  |
| `QA-197` | اختبار المحاكاة بفيديو اصطناعي | Synthetic regression harness for mimic | install | python3 |
| `QA-198` | محلل الفيديو المرجعي | Reference video analyser | install | python3 |
| `QA-199` | اختبار المحاكاة الاصطناعي | Synthetic regression for mimic | install | python3 |
| `QA-200` | حكم الواقعية | Realism judge metric | install | python3 |
| `QA-201` | مشغّل المعاينة | In-browser preview player | install | npm:hyperframes |
| `QA-202` | اللمسات الأخيرة حسب وضوح الفرق | Final-touch passes ordered by visibility (Delta E bands) | install |  |
| `QA-203` | خطط رسم مقاسة يختار بينها حَكَم | Measured painting plans chosen by a judge | install |  |
| `QA-204` | التحقق من المطابقة التامة | Exact-match verification badge | install |  |
| `QA-205` | كود الصورة كبيانات تُقرأ دون تنفيذ | Image code as pure data (read without executing) | install |  |
| `QA-206` | بوابة الواقعية | Realism gate (judge.py) | install | python3 |
| `QA-207` | حلقة المراجعة بالقياس | Measured review loop for painted scenes | install | python3 |
| `QA-208` | مجموعة اختبارات الاستوديو | KOSIF Studio regression suite | install | ffmpeg, python3 |
| `QA-209` | لقطات مراجعة مفتاحية | Key-frame review grabs | install | python3 |
| `QA-210` | سرعة الحركة على الشاشة | On-screen speed by optical flow | install | python3 |
| `QA-211` | دراسة فيلم مرجعي | Reference film study | install | python3 |
| `QA-212` | فحص التسليم | Delivery verification | install | python3 |
| `QA-213` | بوابة الفحص قبل الرندر | hyperframes check gate | install | npm:hyperframes, npm:axe |
| `SEC-09` | فحص الحزام بـAgentShield | Harness scan with AgentShield | install | node |
| `SEC-17` | Semgrep CE: تشغيل قواعد تحليل ثابت على مستودع وفرز | Semgrep CE: Run pattern-based SAST rules over a repo and triage findings | install | pip:semgrep |
| `SEC-18` | Gitleaks: كشف الأسرار المسرّبة في تاريخ git | Gitleaks: Detect committed secrets across git history | install | gitleaks |
| `SEC-19` | Trivy: فحص ملفات القفل والحاويات والبنية ككود بحثًا | Trivy: Scan lockfiles, containers and IaC for CVEs and misconfigurations | install | trivy |
| `API-18` | خوادم محاكاة من مواصفة أو أمثلة | Mock servers from a spec or saved examples | key | npm:bruno, key:unspecified |
| `QA-214` | صورة مفهوم أولاً ثم تنفيذ مطابق | Concept-image first, then faithful build | key | key:unspecified |
| `QA-215` | رندر مدفوع بسقف ميزانية | Budget-capped paid render | key | key:unspecified |
| `QA-216` | التحقق من الكلمات المغناة بتحويل الكلام لنص | Sung-lyric verification by speech-to-text | key | pip:faster-whisper, key:elevenlabs |
| `QA-217` | دليل الأسلوب وحلقة التوليد والفحص | Theme bible + generate/QA loop for figure sets | key | tesseract, key:unspecified |
| `QA-218` | حكم Jev المغلق | Jev closed-set judge | key | key:unspecified |
| `QA-219` | ترتيب خطوات الإنتاج وسد الفراغات | Production step ordering + gap filling + auto review | key | imagemagick, key:unspecified |
| `QA-220` | مراجعة الفريم الحالي | Single-frame director review | key | key:unspecified |
| `QA-221` | مطابقة النص مع الكلام | Transcript verification against speech | key | key:unspecified |
| `QA-222` | سد فراغات المونتاج قبل الريندر | Gap filling before render | key | imagemagick, key:unspecified |
| `QA-223` | فحص الاستهلاك المتبقي | Usage and plan-window check | key | npm:hyperframes, key:unspecified |
| `QA-224` | الحكم جيف | Jev order-robust judge | key | key:unspecified |
| `QA-225` | رندر من دافنشي مع تحقق | Resolve render + verify | key | ffmpeg, python3, key:unspecified |
| `QA-226` | حَكَم Jev المقاوم للترتيب | Jev order-robust judge client | key | key:unspecified |
| `QA-227` | مقارنة ثلاثة نماذج | Three-model transition bake-off | key | key:video-gen |
| `QA-368` | حد أدنى للقراءة | Readability hold & 400 ms floor | idea |  |
| `QA-369` | قاعدة العلامات التجارية | Trademark safety rule | idea |  |
| `QA-370` | تشغيل قابل للتكرار | Reproducible seeded runs | idea |  |
| `QA-371` | منع النص فوق الوجه | Face-region text ban | idea |  |
| `QA-372` | حد الوميض الآمن | Flash photosensitivity cap | idea |  |
