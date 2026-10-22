# A4 — FusionForge v2 وتركيب المهارات / composition and project memory (USIP v5.3)

> **متى تقرأه / when to read:** في كل طلب L2/L3 (المسار القانوني يستدعي FusionForge)، أو حين تركّب مهارات في توليفة، أو تسجّل تجربة، أو تستعيد دروس المشروع. · [العودة إلى النواة / back to the core](../../PROTOCOL.md#متى-تفتح-الملاحق--appendix-triggers)

> **الحالة هنا / backing:** قابل للتنفيذ ومختبر: `scripts/fusionforge.py` (FusionForge v2، stdlib) مع `evals/test_fusionforge.py`، ومخططات [fusionforge.recipe.v2](../../schemas/fusionforge.recipe.v2.json) و[card.v2](../../schemas/fusionforge.card.v2.json) و[bundle.v2](../../schemas/fusionforge.bundle.v2.json). HyperFusion (-1.22) منهج موثَّق: توليد خمس توليفات ومصفوفة التوافق وPareto يجريها Claude، لا السكربت.

نُقلت أقسام «المرحلة -1» هنا من `PROTOCOL.md` (v5.2) بنصها وبأرقامها؛ كل تعديل موسوم `(v5.3: …)`. معاني الخطط وكلمات الرد وسلالم الحالة المعتمدة في [مسرد النواة](../../PROTOCOL.md#المسرد--glossary)، وعند أي تعارض تغلب النواة. خريطة كل قسم قديم: [CHANGELOG](CHANGELOG.md).

## الفهرس / contents

- [FusionForge v2 — الأوامر والحالات (v5.3)](#fusionforge-v2--الأوامر-والحالات-v53)
- [الأقسام المنقولة / moved sections](#الأقسام-المنقولة--moved-sections)
  - [-1.22 مختبر توليف المهارات HyperFusion — ابتكار تركيبات قبل التنفيذ](#-122-مختبر-توليف-المهارات-hyperfusion--ابتكار-تركيبات-قبل-التنفيذ)
  - [-1.35 FusionForge — اختراع قدرات مركبة من مجموعات كبيرة من المهارات](#-135-fusionforge--اختراع-قدرات-مركبة-من-مجموعات-كبيرة-من-المهارات)
  - [-1.36 التعلم الذاتي التراكمي Self-Learning Workflow Memory](#-136-التعلم-الذاتي-التراكمي-self-learning-workflow-memory)
  - [-1.37 قوانين تسجيل المهارة المكتشفة](#-137-قوانين-تسجيل-المهارة-المكتشفة)
  - [-1.45 HyperFusion + FusionForge — دمج عميق دون تضخيم التنفيذ](#-145-hyperfusion--fusionforge--دمج-عميق-دون-تضخيم-التنفيذ)

## FusionForge v2 — الأوامر والحالات (v5.3)

FusionForge لا يرتّب القدرات بنفسه ولا ينفّذ شيئًا: يحوّل `brief` (المرتّب الوحيد) إلى وصفة `kosif.fusionforge.recipe.v2` بعقد typed (مرحلة، قدرات ببصمة ذرّاتها، مدخلات ومخرجات بأنواع أصول، منفّذ) وحواف handoff، وخطط A/B/C هي خطط `brief` نفسها؛ ثم يسجّل ما حدث فعلًا: الخطة المختارة وسببها، وأثر كل عقدة بدليل مُهشَّم، وتغيّر الحالة عبر آلة حالات مفروضة.

**التشغيل** من جذر المستودع: `python3 .claude/skills/kosif-superpowers/scripts/fusionforge.py [--root DIR] [--catalog-file F] [--tools-file F] [--now ISO8601] <cmd> …`. كل أمر يقبل `--json` (JSON كامل فيه `"root"`)؛ والافتراضي ملخص قصير (≤ 25 سطرًا). الخطأ سطر واحد على stderr: `fusionforge: error: <CODE>: <message>`، بلا traceback. رمز الخروج 2 = استعمال/تحقق/حالة، و3 = NO_MATCH في propose (أعد بـ `--terms`)، و4 = validate وجد أخطاء.

**الجذر:** `--root` ثم `$KOSIF_FUSIONFORGE_ROOT` ثم `<جذر git للمجلد الحالي>/out/fusionforge` ثم `<المستودع الذي يحوي المهارة>/out/fusionforge`. مساحة المشروع `<root>/<project>/`: `recipes/` (الوصفات و`.brief.json` بجانب كل وصفة)، و`evidence/`، و`index.json`، و`lessons.json`، و`exports/`، و`promotions/`، و`legacy/`. `out/` مُدرج في `.gitignore`: لا يُرفع إلى git، ولا يبقى في جلسة سحابية جديدة أو جهاز آخر إلا بـ `export` ثم `import` بموافقة المستخدم.

| الأمر | ماذا يفعل |
|---|---|
| `propose "<goal>" --project P [--from-brief brief.json] [--terms "…"] [--max-capabilities N] [--id FUSE-…]` | وصفة candidate من `brief` (يبنيه داخليًا إن غاب `--from-brief` ويحفظه بجانب الوصفة)؛ يشترط `coverage.complete=true`؛ العقد من مراحل خطط A/B/C، وعقود I/O typed، وحواف، و`similar_unverified`، واستدعاء من وصفات المشروع نفسه |
| `reuse "<goal>" --project P [--top N] [--no-brief] [--from-brief brief.json] [--terms "…"]` | قراءة فقط: ترتيب وصفات المشروع السابقة بالتشابه × القوة × الحداثة × الصلاحية؛ الفاشلة تحت `avoid` بدروسها |
| `show --project P --id ID` · `catalog --project P` | قراءة فقط؛ `catalog` لا ينشئ مجلدات ويسرد الملفات التالفة بدل الانهيار |
| `set-graph --project P --id ID --file graph.json` | candidate فقط: يستبدل العقد والحواف بعد التحقق |
| `bind --project P --id ID --node N --executor REF` | candidate أو planned: `REF` = `tool:<id في tools.json>` أو `bin:<name>` أو `mcp:<server/tool>` أو `method:<atom id>` أو `human` |
| `validate --project P --id ID` | الفحوص V01–V12؛ الخروج 4 عند أي خطأ |
| `choose --project P --id ID --plan A\|B\|C\|D --why "…" [--nodes N01,N02]` | candidate → planned؛ يشترط validate بلا أخطاء؛ D يحتاج `--nodes` |
| `trace --project P --id ID --stage S --action "…" [--node N] [--result passed\|failed\|skipped] [--tool REF] [--input] [--output] [--observed] [--capabilities ID…] [--evidence FILE] [--error-class C]` | خطوة نُفذت فعلًا؛ يحدّث حالة العقدة؛ `skipped` يحتاج `--observed`؛ يسجّل استبدال الأداة؛ يرفض الأسرار ومعرفات القدرات المجهولة؛ مرفوض على الوصفة النهائية |
| `record --project P --id ID --status planned\|tested\|verified\|failed [--evidence FILE] [--qa-pass] [--note] [--baseline FILE]` | انتقال مفروض وسجل حالة؛ بوابة verified أدناه؛ planned عبر `choose` وحده (`USE_CHOOSE`) |
| `fork --project P --id ID [--new-id FUSE-…]` | candidate جديدة بنفس الهدف والرسم وحالات مصفّرة و`forked_from` |
| `lessons --project P` | يعيد بناء `lessons.json`: WORKED وFAILED وREPLACED وHANDOFF وRECIPE_FAILED (الفشل داخل) |
| `card --project P --id ID [--out FILE]` · `import-card FILE --project P [--new-id FUSE-…]` | بطاقة Markdown فيها كتلة JSON `kosif.fusionforge.card.v2` منقّحة (بلا مسارات مطلقة، والأدلة ببصمتها) لجلسة بلا shell؛ الاستيراد ينشئ candidate دائمًا |
| `export --project P [--out FILE] [--include-candidates]` · `import FILE --project P` | حزمة منقّحة `kosif.fusionforge.bundle.v2` للحفظ الاختياري (الافتراضي `<space>/exports/<project>-<YYYYMMDD>.json`)، لا تُرفع آليًا؛ الاستيراد يحفظ الحالة مع `imported: true`، والدليل غير المحلي تحذير ووزنه في reuse ×0.8 |
| `migrate --project P` | v1 → v2 مع نسخ احتياطية في `legacy/`؛ وصفة v1 verified بلا أثر تُوسم `legacy_unproven` (وزنها ×0.3) |
| `promote --project P --id ID` | يكتب `promotions/<id>.proposal.json` بحالة `pending_human`؛ لا يعدّل الكتالوج أبدًا |

**الانتقالات:** candidate → planned أو failed؛ planned → tested أو failed؛ tested → tested أو verified أو failed؛ وغير ذلك `ILLEGAL_TRANSITION`. verified وfailed نهائيتان: تجربة جديدة = `fork`. tested وfailed وverified تحتاج `--evidence`، وtested تحتاج أثرًا واحدًا على الأقل نتيجته passed أو failed.

**بوابة verified:** الحالة tested + `--qa-pass` + خطة مختارة + كل عقدة في الخطة المختارة آخر نتيجتها passed أو skipped + عقدة واحدة على الأقل في مرحلة verify نجحت بدليل + بصمة الدليل تختلف عن أي دليل سُجّل مع فشل + validate بلا أخطاء. المحرك يفحص السجلات لا جودة العمل، ولا يشترط `--baseline`: مقارنة خط الأساس التي يطلبها -1.37 و-1.45 قبل VERIFIED (حين يوجد حل سابق أو أبسط) حكمك أنت.

**سياسة الدليل:** ملف عادي غير فارغ وليس رابطًا رمزيًا، داخل المجلد الحالي أو جذر git له أو جذر FusionForge أو مستودع المهارة؛ وليس داخل `recipes/` أو `index.json` أو `lessons.json`؛ يُهشَّم على دفعات، وتُنسخ الملفات حتى 5 MB إلى `evidence/<sha256><suffix>`، وتحفظ السجلات `source` نسبيًا و`sha256` و`size` و`stored`، بلا مسارات مطلقة. **الأسرار:** `scripts/_secrets.py` يفحص كل حقل نصي في كل أمر كاتب ويرفضه. **الكتابة:** ذرّية (ملف مؤقت ثم `os.replace`) تحت قفل `<space>/.lock`؛ والملف التالف بجانبها لا يكسر الأوامر الأخرى.

**رموز validate:** V01 SCHEMA · V02 STATE_LOG_INVALID · V03 HANDOFF_KIND_MISMATCH · V04 NO_FINAL_VERIFY · V05 EXECUTOR_UNKNOWN · V06 EVIDENCE_MISSING · V07 EVIDENCE_HASH_MISMATCH · V08 SECRET · V09 SELF_EVIDENCE · V10 VERIFIED_WITHOUT_RUN · V11 CATALOG_DRIFT (تحذير) · V12 UNKNOWN_CAPABILITY (تحذير)؛ وللمستورد EVIDENCE_NOT_LOCAL (تحذير). **المراحل:** understand, research, plan, build, create, refine, assemble, verify, deliver. **أنواع الأصول:** brief, spec, plan, sources, code, dataset, report, document, image, audio, video, model3d, font, prompt, evidence, package, any (`prompt` = حزمة مطالبات قابلة للنسخ من `scripts/prompt_pack.py`، مثال حافة: A(output:prompt)→adapter(prompt:prompt@engine)→المستخدم؛ لا تُنفَّذ هنا). **العلاقات:** sequence, parallel, complement, substitute, verify, refine, fallback (الحلقة لـ refine وحدها).

**بلا shell:** لا تدّعِ حفظًا. اكتب بطاقة الوصفة بيدك بصيغة `kosif.fusionforge.card.v2` (جدول العقد + كتلة JSON)، وعنوانها بحالة UNSAVED، ومعها سطر `MEMORY_RUNTIME_UNAVAILABLE`؛ وفي جلسة لاحقة فيها shell: `import-card` ينشئ منها candidate.

**ما يزيده المحرك على هذا العقد / engine rules beyond the table (v5.3):**
- **الحالات:** `record --status planned` يرفضه المحرك بـ `USE_CHOOSE` (planned لا يضبطه إلا `choose`)؛ و`failed` يحتاج `--note` غير فارغ (`NOTE_REQUIRED`)؛ و`--qa-pass` لا يُقبل إلا مع `verified`. `trace --result` قبل `choose` يُرفض بـ `PLAN_NOT_CHOSEN` (أثر بلا `--result` مسموح)، و`choose` يعيد كل العقد إلى pending. خارج مستودع git بلا `--root` ولا `$KOSIF_FUSIONFORGE_ROOT` يتوقف كل أمر بـ `NO_ROOT`، وجذر داخل المستودع غير مستثنى من git يطبع التحذير `ROOT_NOT_GITIGNORED`.
- **البوابة:** إلى جانب `QA_PASS_REQUIRED` و`GATE_NODE_NOT_PASSED` و`GATE_NO_VERIFY_EVIDENCE` و`GATE_VALIDATE_ERRORS`: `GATE_FAILURE_EVIDENCE_REUSED` يشمل كل دليل سُجّل مع فشل في المشروع كله (الفروع والوصفات الشقيقة)، و`GATE_EVIDENCE_REUSED` يرفض دليل QA أو دليل أثر verify سبق أن وثّق وصفة أخرى، و`GATE_EVIDENCE_NOT_LOCAL` يطلب لوصفة مستوردة أثر verify جديدًا بدليل على هذا الجهاز.
- **الدليل والمخرجات:** `SELF_EVIDENCE` يشمل أيضًا `cards/` و`legacy/` و`exports/` و`promotions/` والروابط الصلبة ونسخ أي سجل `kosif.fusionforge.*`؛ وملفات الاعتماد (`.env` و`.npmrc` و`.netrc` و`id_rsa` ومخازن المفاتيح و`.ssh/` و`.aws/` و`.gnupg/`) تُرفض بـ `EVIDENCE_SENSITIVE`؛ وملف نصي فيه نمط اعتماد يُرفض بـ `SECRET`، كما تُفحص المسارات و`--project`. `card --out` يجب أن ينتهي بـ `.md` و`export --out` بـ `.json`، ولا يكتبان داخل `recipes/` أو `legacy/` أو `evidence/` ولا فوق سجل (`OUT_REFUSED`). `promote` يرفض غير المتحقق (`NOT_VERIFIED`) والمرحَّلة و`legacy_unproven` وأي تحذير V10 والمستوردة غير المتحقق منها هنا (`NOT_PROVEN`).
- **التقرير والذاكرة:** معرّف في `brief` لا يطابق الكتالوج يُعاد ربطه بالاسم حين يطابق عنصرًا واحدًا (تحذير `BRIEF_ID_REMAPPED`) وإلا يتوقف بـ `BRIEF_CATALOG_MISMATCH`؛ و`NO_MATCH` (خروج 3) أيضًا حين لا تحمل الخطط إلا تحققًا أو تسليمًا. الوصفات السابقة التي فيها أخطاء validate لا تعطي ذاكرة (تحذير `MEMORY_SKIPPED_INVALID_PRIORS:n`). خيارات زائدة: `reuse --from-brief/--terms`، و`fork`/`import-card --new-id`.
- **حقول إضافية:** الأثر `tool_reported`؛ والدليل فوق 5 MB `root_rel`؛ والمستورد `import_receipt`؛ وذاكرة العقدة `ran_in` و`stage_worked` و`stage_failed` و`stage_replacements`؛ والاستدعاء `template_executors`؛ وreuse `sim_basis` و`reusable` (في validate وcatalog وreuse، لا في `index.json`)؛ والدروس `assumed_executor` و`node_capabilities` وعدّادا `assumed_passed`/`assumed_failed` في `by_executor`.
- **أرقام reuse:** التشابه = 0.5 للهدف + 0.5 لتداخل القدرات حين يتاح `brief` (وصفة بلا قدرة مشتركة ليست مشابهة)، وحدّه الأدنى 0.15 للنص وحده و0.2 مع القدرات، والقالب في propose يحتاج 0.05 على الأقل؛ القوة لوصفة v1 verified بلا أثر 0.3 ومع آثار v1 0.5؛ والمستوردة ×0.8. **الحتمية:** `--now` مع `--id` يعطيان ملفات وصفة و`brief` وفهرس وبطاقة متطابقة بايتًا ببايت، بشرط `brief` حتمي (`--from-brief`).

## الأقسام المنقولة / moved sections

### -1.22 مختبر توليف المهارات HyperFusion — ابتكار تركيبات قبل التنفيذ

حوّل كل طلب مركب إلى **رسم بياني للقدرات**. لكل عقدة: معرف، فائدة، مدخل، مخرج، حالة توفر، صاحب تشغيل، تكلفة، حقوق، اختبار. وصِل العقد بعلاقات: sequence وparallel وcomplement وsubstitute وvalidate وcritique وrefine وrollback. (v5.3: حواف الوصفة في FusionForge v2 typed: لكل حافة `kind` من أنواع الأصول وعلاقة من sequence/parallel/complement/substitute/verify/refine/fallback؛ validate تقابل verify، والنقد عقدة verify، وrollback حقل في العقدة.) لا تستخدم الرسم لإثبات أن أداة نصبت.

**خوارزمية التوليف:**
1. فكّك الهدف إلى قدرات ضرورية ونوعية وتجريبية، وميز بين مهارة منهجية ومنفذ حقيقي.
2. ابحث في الفهرس الذري والخارق، أضف حزم SEE المناسبة وفق سقفها، وسجّل فجوات التغطية.
3. ولّد خمس توليفات متنوعة، منها توليفتان عابرتان للمجالات؛ لا تجمع أسماءً بلا تبادل مخرجات.
4. لكل توليفة حدّد لماذا يضيف كل عنصر نتيجة قابلة للقياس؛ احذف التكرار. طبّق Pareto على الجودة والوقت والتكلفة والمخاطرة.
5. اصنع مصفوفة توافق: صيغ الملفات، واجهات الإدخال/الإخراج، الأذونات، عزل الشركات، جودة المصدر، وطول السياق.
6. اعرض أفضل ثلاث خطط A/B/C؛ اسمح بدمج عناصرها في D، ثم ثبّت قرار المستخدم. (v5.3: بمعاني المسرد، والقرار يُسجَّل بـ `fusionforge.py choose`.)
7. بعد الموافقة، نفّذ خطاً واحداً أولاً مع اختبار end-to-end قصير؛ توازِ فقط بين خطوات مستقلة لا تتصارع على ملف أو حساب.
8. عند نجاح كل مرحلة، جمد نجاحها كأثر مقيَّس، وأعد تخطيط المتعثر فقط.

**أمثلة تركيب إبداعي:**
- فيديو الدعاء: Speech alignment + Storyboard + footage/rights + Arabic font QA + deterministic render + ffprobe. استيراد الصوت وحده ليس فيلماً مكتملاً.
- تدقيق مالي: مصادر وأدلة + محاسبة IFRS + مطابقة حسابية مستقلة + anomalous-GL + مراجعة تفسيرية + عزل شركة.
- تطوير برمجيات: Graphify + عزل السبب + ADR + إصلاح صغير + اختبارات خاصية/انحدار + إطلاق ومراقبة.
- تعليمات وكيل: Prompt Architecture + Agent Contracts + Eval Trust + حراسة المصدر + سجل اختبارات تصادم.

### -1.35 FusionForge — اختراع قدرات مركبة من مجموعات كبيرة من المهارات

هذا هو القلب التنفيذي الجديد لفكرة المستخدم: لا تكتفِ بترشيح مهارات موجودة؛ ابحث في المرشحات الكثيرة عن تآزر مفيد، وصمّم توليفة ذات مدخلات ومخرجات وصيغ تحويل واختبار محدد، ثم جرّبها لتصبح مهارة مركبة قابلة لإعادة الاستخدام.

1. (v5.3: الترتيب الملزم في [المسار القانوني](../../PROTOCOL.md#المسار-القانوني-الواحد--canonical-pipeline): reuse ثم propose --from-brief بعد الإيصال، ثم validate وchoose بعد الموافقة، ثم trace وrecord.) المسار: Stage-0 → brief بإيصال جرد كامل → FusionForge propose → القراءة العميقة للمرشحات → خريطة dependencies → A/B/C → اعتماد → prototype → تنفيذ → QA → حفظ وصفة → استدعاء في المهمة التالية.
2. يشمل البحث مجموعة كبيرة من Superpowers المفهرسة: shortlist حتى 90 افتراضياً أو 300 عند الحاجة، وترشيح حتى 24 Superpower متنوعة افتراضياً أو 60 إذا كان كل مكوّن له دور مقاس. (v5.3: هذه أرقام محرك v1؛ في v2 لا يرتّب FusionForge بنفسه: عقده تأتي من خطط `brief` الذي فحص 100% من السجلات، و`--max-capabilities N` يقصّ الخطط اللاحقة أولًا.) **لا تخلط هذا بعدد حزم SEE المحمّلة**: تبقى قيود الحزم ≤2 Standard و≤4 Deep، والتخصصات الديناميكية ≤1 أو ≤2.
3. لكل عقدة: معرف القدرة، سبب اختيارها، المدخل، المخرج، حالة توفر المنفذ، الاعتماديات، صاحب التنفيذ، الصلاحية، الكلفة، اختبار القبول، البديل. الروابط sequence / parallel / complement / substitute / verify / refine.
4. صمّم أفكاراً عابرة للمجالات: مهارة تنتج X، وأخرى تحول X إلى Y، وثالثة تتحقق من Y، ثم Z جديد يمكن إثبات فائدته مقارنة بأبسط حل. جرّب تباينات الترتيب والواجهات وأدوات القياس. لا تكدّس الأسماء للزينة.
5. أنتج 3 توليفات بمعاني المسرد (v5.3: صُحّحت لتطابق المرحلة 6): A أبسط مسار يحقق كل متطلب إلزامي، B احترافية متوازنة بتكاملات من مجالات أخرى، C محرك أو مصدر أو طريقة تحقق مختلفة (ليست B + إضافات). اسمح للمستخدم بجمعها في D (دمج عقد مسماة يوافق عليه). وهي خطط `brief` نفسها داخل الوصفة: قائمة واحدة لكل طلب. لا تعيد الأسئلة أو الخطط بعد اعتماد خطة قائمة.
6. قارِن Baseline مقابل Candidate بمدخلات ومعايير متطابقة؛ جدوى أعلى أو دقة/جودة أحسن/وقت أقل بوثيقة قياس، وإلا تُرفض الترقية. أفضل أفكار على الورق لا تعني قدرات تم تنفيذها. (v5.3: خط الأساس يُرفق بـ `record … --baseline <ملف>`، والمحرك لا يشترطه لـ verified: المقارنة حكمك أنت.)

### -1.36 التعلم الذاتي التراكمي Self-Learning Workflow Memory

بناء على إذن المستخدم، لكل طلب إنتاجي L2/L3 عند توفر shell وملفات المشروع: **أنشئ وصفة تجربة جديدة تلقائياً داخل المشروع المحلي**. هذه ذاكرة مهارات تنفيذية قابلة للاستدعاء وليست تدريباً أو تعديلاً لأوزان Claude. لا مراقبة خفية ولا نسخ للمحادثات كاملة ولا تعميم لبيانات الشركات.

- قبل الاقتراح، اقرأ سجل نجاحات المشروع نفسه واستفد من التركيبات المتحققة السابقة، ولا تستدع ذاكرة شركة أخرى دون موافقة وعزل.
- شغّل من جذر المستودع: python3 .claude/skills/kosif-superpowers/scripts/fusionforge.py propose "<goal>" --project <project-slug> (v5.3: ومعه `--from-brief <مجلد العمل>/brief.json`، وقبله `reuse`؛ الأوامر كلها في القسم الأول من هذا الملف.)
- المكان المحلي: out/fusionforge/<project>/index.json وout/fusionforge/<project>/recipes/FUSE-<date>-<id>.json. مجلد out/ مُدرج في .gitignore فلا يُرفع إلى git (v5.3: صُحّحت عبارة كانت تقول العكس). (v5.3: الجذر يحدده `--root` ثم `$KOSIF_FUSIONFORGE_ROOT`، وفي جلسة سحابية يعيش داخل الحاوية فقط: احفظه بـ `export` إن أراد المستخدم.) حفظ هذا الفهرس محلياً **ليس** نشراً على GitHub ولا ضماناً ببقائه على أجهزة أخرى؛ النسخ الاحتياطي أو مزامنته يحتاج موافقة ومساراً خاصاً.
- كل وصفة تحتوي: الهدف، المكونات ومعرفاتها، الأدوار والاعتماديات، ترتيب Workflow، 3 مناهج، مصادر الكتالوج، المفروض/المجهول، اختبار القيمة، والأدلة والنتائج. هي مرشح جديد حتى لو أُنشئت بعد كل مهمة.
- بعد تجربة فعلية سجّل tested/failed بمستند قياس؛ بعد اختبار نجاح حقيقي سجل verified مع ملف دليل موجود وخيار qa-pass. مثال: python3 .claude/skills/kosif-superpowers/scripts/fusionforge.py record --project <project> --id <FUSE-ID> --status verified --evidence <QA.json> --qa-pass
- حالة verified هي تصريح من المنفذ أنه راجع دليلاً حقيقياً، لا ضمان من سكربت أن محتوى QA صحيح. (v5.3: في v2 يفرض المحرك بوابة على السجلات قبل verified — tested أولًا، و`--qa-pass`، وكل عقدة في الخطة المختارة passed أو skipped، وعقدة verify نجحت بدليل، ودليل لا يطابق دليل فشل، وvalidate نظيف — لكنه لا يحكم على جودة العمل نفسه، ولا يشترط خط الأساس الذي يطلبه -1.37.) لو فشل التنفيذ، احتفظ بالوصفة والحالة failed وسجل سبب الفشل ووسيلة تفاديه؛ لا تحذف خبرات صحيحة.
- (v5.3: في v2: `reuse` يرتّب وصفات المشروع نفسه بـ التشابه × القوة × الحداثة × الصلاحية ويضع الفاشلة تحت `avoid` بدروسها، و`propose` يستدعي أقواها قالبًا.) عند طلب مشابه مستقبلاً يرفع FusionForge أولوية المكونات التي نجحت في **المشروع ذاته** ويعيد معرفات الوصفات السابقة. ثم يصمم نسخة أحدث ويختبر التحسّن لا يكررها بلا تفكير.
- لا ترفع التجربة إلى مكتبة مهارات عامة أو data/powers أو data/superpowers.json دون تجريد الأسرار وعزل المستأجرين، واختبار نجاح عبر مشروعين مستقلين، واختبار تصادم/عدم تشغيل، وموافقة المستخدم، ثم تشغيل سلسلة صيانة الفهرس الحتمي. (v5.3: `promote` يكتب مقترحًا بحالة pending_human فقط ولا يلمس الكتالوج.)

### -1.37 قوانين تسجيل المهارة المكتشفة

ميّز بوضوح:
- IDEA: توليفة مقترحة لم تُنفذ.
- CANDIDATE: وصفة محفوظة ومترابطة بمدخلات ومخرجات.
- TESTED: تجربة حدثت بدليل سواء نجحت أو أخفقت؛ لا تساوي نجاحاً.
- VERIFIED: اجتياز بوابة QA بدليل قابل للفحص ومقارنة مع خط أساس.
- REUSABLE: يمكن استدعاؤها داخل المشروع بعد التحقق من حداثة الأدوات والسياق.
- GENERALIZED: قابلة للانتقال عبر مشروعات فقط بقرار وموافقة منفصلين.

(v5.3: مقابلها في حالات المحرك: IDEA = لا وصفة بعد · CANDIDATE = `candidate` أو `planned` · TESTED = `tested` · VERIFIED = `verified` · REUSABLE = علامة مشتقة: verified وvalidate نظيف · GENERALIZED = ترقية يوافق عليها إنسان، لا تحدث آليًا أبدًا · و`failed` حالة نهائية تحفظ الدرس. التفاصيل في [المسرد](../../PROTOCOL.md#المسرد--glossary).)

**كل تجربة = وصفة جديدة في فهرس التجارب، وليس كل تجربة = قدرة ناجحة.** هذه نقطة صدق أساسية. عند كتابة تقرير نهائي اذكر ماذا اكتشفت وكيف ركبت الأدوات، وما الذي نُفّذ واختُبر، وما الذي لم يثبت، ورقم وصفة FusionForge ومكانها. حافظ على المخرجات الناجحة عند فشل أداة أخرى، وكرر المسار الفاشل وحده ضمن حدود الصلاحيات.

### -1.45 HyperFusion + FusionForge — دمج عميق دون تضخيم التنفيذ

يبقى سجل FusionForge الأساسي في -1.35…-1.38 هو المرجع للذاكرة والتراكم؛ أضف لكل عقدة capability_origin وmethod_or_executor وtenant_scope وrequired_permission وexpected_postcondition وevidence_status وcost_known وrollback. (v5.3: في مخطط v2 تقابلها: `executor.ref` (tool:/bin:/mcp:/method:/human) و`owner` و`permission` و`outputs[].check` و`status` و`rollback`؛ ونطاق المستأجر هو `--project`، والكلفة تبقى في الخطة.) مصادر origin المسموحة: local_superpowers، see_method_pack، think_live_provider، atlas_public_reference، computer_executor، flagship_local، release_bridge.

ابنِ Workflow بأطراف قابلة للتوصيل: إدخال → معالجة → نقد مستقل → تحقق حتمي → منفذ مرخص → فحص أثر → تعلّم مشروع اختياري. توليد 5 مسارات واختيار A/B/C مختلفة المنهج مفيد في L2/L3 لكنه لا يوجب تشغيل آلاف الأدوات؛ عدد الوكلاء لا يقيس الدقة. لا تُرقِّ IDEA أو CANDIDATE إلى VERIFIED قبل خط أساس واختبار فعلي وإيصال مخرج. (v5.3: المحرك يمنع القفز: candidate → planned → tested → verified؛ أما خط الأساس فيُرفق بـ `record … --baseline <ملف>` لكن المحرك **لا يشترطه** لـ verified، فهذا الشرط حكمك أنت قبل `--qa-pass`.) عزل ملفات الشركات قبل توحيد الخبرة؛ لا تعميم صامت إلى مشروع آخر. يدير KOSIF PMO الحالة والاعتماديات/المخاطر؛ لا ينشر ذاتيًا.

(v5.3: اختبارات القبول -1.38 صارت في [A9](A9-shadow-evals.md) مع بقية مواصفات الاختبار، ولكل بند فيها اسم الاختبار الآلي الذي يغطيه.)
