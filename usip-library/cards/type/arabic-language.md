# `arabic-language` — الخطوط والنصوص العربية واللاتينية (22 بطاقة)

> مكتبة بروتوكول USIP v5.5 الكاملة، مولّدة بـ `smart_capabilities.py cards` من `data/powers/arabic-language.json` وقواعد الملاحق A25–A29؛ لا تُحرَّر يدويًا. [الفهرس الرئيسي](../../README.md) · [فصل المجموعة](../../../.claude/skills/kosif-superpowers/references/library/type.md) · [النواة](../../../.claude/skills/kosif-superpowers/PROTOCOL.md)

## الفهرس / contents

- [`ARL-01` تطبيع العربية للبحث والمطابقة](#arl-01--تطبيع-العربية-للبحث-والمطابقة--normalize-arabic-for-search-and-matching)
- [`ARL-02` طابِق على نسخة مطبّعة واعرض بالإملاء الأصلي](#arl-02--طابِق-على-نسخة-مطبّعة-واعرض-بالإملاء-الأصلي--match-normalized-report-in-the-original-spelling)
- [`ARL-03` حدود الكلمة العربية مع السوابق](#arl-03--حدود-الكلمة-العربية-مع-السوابق--clitic-aware-arabic-word-boundaries)
- [`ARL-04` قراءة الأرقام العربية: هندية وفارسية وفواصل ونسبة](#arl-04--قراءة-الأرقام-العربية-هندية-وفارسية-وفواصل-ونسبة--parse-arabic-numerals-separators-and-percent)
- [`ARL-05` أسماء الشهور والأيام: ميلادية وشامية وهجرية](#arl-05--أسماء-الشهور-والأيام-ميلادية-وشامية-وهجرية--month-and-weekday-names-gregorian-levantine-hijri)
- [`ARL-06` تشكيل الحروف للعرض: محرك واحد فقط](#arl-06--تشكيل-الحروف-للعرض-محرك-واحد-فقط--shaping-arabic-for-display-exactly-one-engine)
- [`ARL-07` الاتجاه الثنائي في النصوص المختلطة](#arl-07--الاتجاه-الثنائي-في-النصوص-المختلطة--bidi-in-mixed-arabiclatin-text)
- [`ARL-08` خطوط عربية: فحص وتثبيت](#arl-08--خطوط-عربية-فحص-وتثبيت--arabic-fonts-check-and-install)
- [`ARL-09` سياسة التشكيل (الحركات)](#arl-09--سياسة-التشكيل-الحركات--tashkeel-policy)
- [`ARL-10` أدوات CAMeL Tools الخفيفة بلا نماذج](#arl-10--أدوات-camel-tools-الخفيفة-بلا-نماذج--camel-tools-character-utilities-without-models)
- [`ARL-11` تحليل صرفي وتعرّف اللهجة والكيانات (CAMeL Tools كاملة)](#arl-11--تحليل-صرفي-وتعرّف-اللهجة-والكيانات-camel-tools-كاملة--morphology-dialect-id-and-ner-with-full-camel-tools)
- [`ARL-12` PyArabic للتنظيف والتقطيع (رخصة GPL)](#arl-12--pyarabic-للتنظيف-والتقطيع-رخصة-gpl--pyarabic-for-cleanup-and-tokenizing-gpl)
- [`ARL-13` مقطّع Farasa عبر farasapy](#arl-13--مقطّع-farasa-عبر-farasapy--farasa-segmenter-via-farasapy)
- [`ARL-14` التعرف الضوئي على العربية (tesseract)](#arl-14--التعرف-الضوئي-على-العربية-tesseract--arabic-ocr-with-tesseract)
- [`ARL-15` تحقق من أرقام OCR ببوابة المراسي](#arl-15--تحقق-من-أرقام-ocr-ببوابة-المراسي--verify-ocr-numbers-with-the-anchor-gate)
- [`ARL-16` إصلاح الترميز المشوّه](#arl-16--إصلاح-الترميز-المشوّه--mojibake-repair)
- [`ARL-17` التعامل مع اللهجات وتحديد السجل](#arl-17--التعامل-مع-اللهجات-وتحديد-السجل--dialect-handling-and-register-choice)
- [`ARL-18` النقل الحرفي والرومنة](#arl-18--النقل-الحرفي-والرومنة--transliteration-and-romanization)
- [`ARL-19` مراجعة المطابقة النحوية بعد التعديل](#arl-19--مراجعة-المطابقة-النحوية-بعد-التعديل--agreement-check-after-editing)
- [`ARL-20` CAMeL Tools: تقطيع النص العربي واستخراج الجذور والتشكيل وتحديد](#arl-20--camel-tools-تقطيع-النص-العربي-واستخراج-الجذور-والتشكيل-وتحديد--camel-tools-tokenise-lemmatise-diacritise-and-dialect-identify-arabic-text)
- [`ARL-21` spaCy: تقطيع العربية ومطابقة القواعد؛ واستخراج الكيانات مع](#arl-21--spacy-تقطيع-العربية-ومطابقة-القواعد-واستخراج-الكيانات-مع--spacy-tokenise-arabic-and-match-rules-blank-ar-ner-with-downloaded-models)
- [`ARL-22` Argos Translate: ترجمة عربي-إنجليزي دون اتصال تمامًا](#arl-22--argos-translate-ترجمة-عربي-إنجليزي-دون-اتصال-تمامًا--argos-translate-translate-arabicenglish-fully-offline)

## البطاقات / cards

### `ARL-01` — تطبيع العربية للبحث والمطابقة / Normalize Arabic for search and matching

| الحقل | القيمة |
|---|---|
| العائلة | `arabic-language` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/arabic-language.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | ترجمة وتعريب (`translation`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | original (this skill) |

**ما هي:** نسخة مطبّعة للمطابقة فقط: بلا تشكيل ولا تطويل، ألف واحدة، ى→ي، ة→ه، وأرقام لاتينية؛ والنص الأصلي لا يُمس. — A matching-only copy without tashkeel or tatweel, one alef, ى→ي, ة→ه and ASCII digits; the original text is never changed.

**متى:** عند البحث في نص عربي أو إزالة تكراره أو مقارنته أو مطابقته بتعبير نمطي، وقبل المقارنة بين نسختين عربيتين / Searching, deduplicating, comparing or regex-matching Arabic text; before diffing two Arabic versions.

**كيف:** Python stdlib: unicodedata.normalize("NFKC", s); remove [\u064B-\u0652\u0670\u0640]; translate "أإآٱىة"→"اااايه"; translate ٠-٩ and ۰-۹ to 0-9. Ready code: tell_scan.norm_ar and anchor_gate.clean (scripts/). Tested: "ختامًا إلى مُستشفى المدينةِ" equals "ختاما الي مستشفي المدينه". Folding ة→ه and ى→ي is lossy: use it for keys, never for output. Motion-side alignment variant: ARAB-69.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** normalization · search · matching · tashkeel · alef · تطبيع · بحث · همزات

#### 1. الاستقبال (A25)

- اللغتان: افتراض مكتوب ← إلى لغة رسالة المستخدم
- المستوى اللغوي: افتراض مكتوب ← فصحى معاصرة بسيطة
- مصطلحات ثابتة: افتراض مكتوب ← المصطلح الشائع مع الإنجليزي بين قوسين عند أول ذكر
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `document` ← المخرج `document`، والمنفّذ `method:ARL-01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `anchor-gate` · `tell-scan`.
- مراحل النوع: المصطلحات الثابتة ← ترجمة ← مقابلة جملة بجملة ← مطابقة الأرقام والأسماء ← قراءة طبيعية ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المعنى كاملًا بلا حذف ولا إضافة ← مقابلة جملة بجملة
- إلزامي: الأرقام والأسماء والتواريخ مطابقة ← مقارنة آلية للأرقام
- جودة: تُقرأ طبيعية لا حرفية ← قراءة بصوت مسموع
- جودة: المصطلح الواحد مترجم بطريقة واحدة ← بحث المصطلحات
- أمر الحكم في الوضع 1: `think.py qa translation --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-writing/README.md`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-writing/arabic_probe.py`

#### 7. قدرات قريبة في العائلة

- `ARL-02` طابِق على نسخة مطبّعة واعرض بالإملاء الأصلي / Match normalized, report in the original spelling (proven)
- `ARL-03` حدود الكلمة العربية مع السوابق / Clitic-aware Arabic word boundaries (proven)

### `ARL-02` — طابِق على نسخة مطبّعة واعرض بالإملاء الأصلي / Match normalized, report in the original spelling

| الحقل | القيمة |
|---|---|
| العائلة | `arabic-language` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/arabic-language.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | ترجمة وتعريب (`translation`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | original (this skill) |

**ما هي:** خريطة مواضع حرفًا بحرف تربط النسخة المطبّعة بالأصل، فيظهر كل تطابق كما كتبه الكاتب بتشكيله. — A char-level offset map links the normalized copy to the source so every match is shown as written, tashkeel included.

**متى:** عند إبراز نتائج البحث أو نتائج الفحص أو التعديلات في نص عربي فيه تشكيل أو تطويل أو أشكال عرض / Highlighting search hits, lint results or edits in Arabic text that has tashkeel, tatweel or presentation forms.

**كيف:** Normalize one source char at a time, record the source index of every output char, match on the normalized string, map [start, end) back, then extend end over trailing harakat. Implemented in tell_scan.norm_with_map. Tested: matches on "وفي الختامِ، تُعزّز" display as "وفي الختامِ" and "تُعزّز" (not "تعزز").

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** offsets · highlight · display · original spelling · إملاء أصلي · تمييز

#### 1. الاستقبال (A25)

- اللغتان: افتراض مكتوب ← إلى لغة رسالة المستخدم
- المستوى اللغوي: افتراض مكتوب ← فصحى معاصرة بسيطة
- مصطلحات ثابتة: افتراض مكتوب ← المصطلح الشائع مع الإنجليزي بين قوسين عند أول ذكر
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `document` ← المخرج `document`، والمنفّذ `method:ARL-02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `anchor-gate` · `tell-scan`.
- مراحل النوع: المصطلحات الثابتة ← ترجمة ← مقابلة جملة بجملة ← مطابقة الأرقام والأسماء ← قراءة طبيعية ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المعنى كاملًا بلا حذف ولا إضافة ← مقابلة جملة بجملة
- إلزامي: الأرقام والأسماء والتواريخ مطابقة ← مقارنة آلية للأرقام
- جودة: تُقرأ طبيعية لا حرفية ← قراءة بصوت مسموع
- جودة: المصطلح الواحد مترجم بطريقة واحدة ← بحث المصطلحات
- أمر الحكم في الوضع 1: `think.py qa translation --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-writing/README.md`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-writing/arabic_probe.py`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-writing/test_writing.py`

#### 7. قدرات قريبة في العائلة

- `ARL-01` تطبيع العربية للبحث والمطابقة / Normalize Arabic for search and matching (proven)
- `ARL-03` حدود الكلمة العربية مع السوابق / Clitic-aware Arabic word boundaries (proven)
- `ARL-04` قراءة الأرقام العربية: هندية وفارسية وفواصل ونسبة / Parse Arabic numerals, separators and percent (proven)

### `ARL-03` — حدود الكلمة العربية مع السوابق / Clitic-aware Arabic word boundaries

| الحقل | القيمة |
|---|---|
| العائلة | `arabic-language` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/arabic-language.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | ترجمة وتعريب (`translation`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | original (this skill) |

**ما هي:** في بايثون \b و\w تعدّ الحروف العربية حروف كلمة، فيضيع "و٥" و"٢٠٢٤م" و"بالمصري"؛ استخدم حدودًا عربية صريحة مع سوابق اختيارية. — Python \b and \w treat Arabic letters as word chars, so clitic-glued forms are missed; use explicit Arabic boundaries with optional proclitics.

**متى:** عند كتابة أي تعبير نمطي على العربية: قوائم كلمات مفتاحية، استخراج أرقام، مطابقة أسماء / Writing any regex over Arabic: keyword lists, number extraction, name matching.

**كيف:** Word: (?<![\u0621-\u064A])(?:[وفبلك]?(?:ال)?\|لل)(?:WORD)(?![\u0621-\u064A]). Numbers: (?<![\d.,])\d+… with no letter lookarounds, so و٥ / بـ١٠٠ / ٢٠٢٤م are found. Names: not preceded or followed by a letter or digit, optional proclitic (so علي does not match inside عليها, but وأحمد matches أحمد). Tested: و٥→و٩ and ٢٠٢٤م→٢٠٢٥م flagged; يمارس is not the month مارس.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** regex · clitics · proclitic · word boundary · سوابق · تعبير نمطي

#### 1. الاستقبال (A25)

- اللغتان: افتراض مكتوب ← إلى لغة رسالة المستخدم
- المستوى اللغوي: افتراض مكتوب ← فصحى معاصرة بسيطة
- مصطلحات ثابتة: افتراض مكتوب ← المصطلح الشائع مع الإنجليزي بين قوسين عند أول ذكر
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `document` ← المخرج `document`، والمنفّذ `method:ARL-03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `anchor-gate` · `tell-scan`.
- مراحل النوع: المصطلحات الثابتة ← ترجمة ← مقابلة جملة بجملة ← مطابقة الأرقام والأسماء ← قراءة طبيعية ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المعنى كاملًا بلا حذف ولا إضافة ← مقابلة جملة بجملة
- إلزامي: الأرقام والأسماء والتواريخ مطابقة ← مقارنة آلية للأرقام
- جودة: تُقرأ طبيعية لا حرفية ← قراءة بصوت مسموع
- جودة: المصطلح الواحد مترجم بطريقة واحدة ← بحث المصطلحات
- أمر الحكم في الوضع 1: `think.py qa translation --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-writing/README.md`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-writing/test_writing.py`

#### 7. قدرات قريبة في العائلة

- `ARL-01` تطبيع العربية للبحث والمطابقة / Normalize Arabic for search and matching (proven)
- `ARL-02` طابِق على نسخة مطبّعة واعرض بالإملاء الأصلي / Match normalized, report in the original spelling (proven)
- `ARL-04` قراءة الأرقام العربية: هندية وفارسية وفواصل ونسبة / Parse Arabic numerals, separators and percent (proven)
- `ARL-05` أسماء الشهور والأيام: ميلادية وشامية وهجرية / Month and weekday names (Gregorian, Levantine, Hijri) (proven)

### `ARL-04` — قراءة الأرقام العربية: هندية وفارسية وفواصل ونسبة / Parse Arabic numerals, separators and percent

| الحقل | القيمة |
|---|---|
| العائلة | `arabic-language` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/arabic-language.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | ترجمة وتعريب (`translation`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | original (this skill) |

**ما هي:** ٣ = 3 = ۳، و١٬٥٠٠٬٠٠٠ = 1,500,000 = 1500000، و٪١٥ = %15 = 15%، والرقم الملتصق بحرف يُقرأ. — Arabic-Indic and Persian digits, ٫ ٬ ، separators, prefix or suffix percent and glued digits all fold to one canonical value.

**متى:** عند استخراج الأرقام أو مقارنتها في مستندات عربية أو فواتير أو مخرجات OCR أو ترجمات مرافقة / Extracting or comparing numbers in Arabic documents, invoices, OCR output or captions.

**كيف:** Translate digits; fold ٫→. ٬→, ،→, ٪→%; strip thousands separators only when they group by three; move a prefix percent to a suffix. Implemented in anchor_gate.fold_num. Tested: "في عام ٢٠٢٤م" = "في عام 2024"; "1,500,000 ريال" = "1500000 ريال"; "٪١٥" = "15%". Formatting the other way (money, tabular digits) is ARAB-73/ARAB-74.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** arabic digits · numbers · percent · separators · أرقام هندية · نسبة مئوية

#### 1. الاستقبال (A25)

- اللغتان: افتراض مكتوب ← إلى لغة رسالة المستخدم
- المستوى اللغوي: افتراض مكتوب ← فصحى معاصرة بسيطة
- مصطلحات ثابتة: افتراض مكتوب ← المصطلح الشائع مع الإنجليزي بين قوسين عند أول ذكر
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `document` ← المخرج `document`، والمنفّذ `method:ARL-04` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `anchor-gate` · `tell-scan`.
- مراحل النوع: المصطلحات الثابتة ← ترجمة ← مقابلة جملة بجملة ← مطابقة الأرقام والأسماء ← قراءة طبيعية ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المعنى كاملًا بلا حذف ولا إضافة ← مقابلة جملة بجملة
- إلزامي: الأرقام والأسماء والتواريخ مطابقة ← مقارنة آلية للأرقام
- جودة: تُقرأ طبيعية لا حرفية ← قراءة بصوت مسموع
- جودة: المصطلح الواحد مترجم بطريقة واحدة ← بحث المصطلحات
- أمر الحكم في الوضع 1: `think.py qa translation --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-writing/README.md`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-writing/arabic_probe.py`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-writing/test_writing.py`

#### 7. قدرات قريبة في العائلة

- `ARL-02` طابِق على نسخة مطبّعة واعرض بالإملاء الأصلي / Match normalized, report in the original spelling (proven)
- `ARL-03` حدود الكلمة العربية مع السوابق / Clitic-aware Arabic word boundaries (proven)
- `ARL-05` أسماء الشهور والأيام: ميلادية وشامية وهجرية / Month and weekday names (Gregorian, Levantine, Hijri) (proven)
- `ARL-06` تشكيل الحروف للعرض: محرك واحد فقط / Shaping Arabic for display: exactly one engine (proven)

### `ARL-05` — أسماء الشهور والأيام: ميلادية وشامية وهجرية / Month and weekday names (Gregorian, Levantine, Hijri)

| الحقل | القيمة |
|---|---|
| العائلة | `arabic-language` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/arabic-language.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | ترجمة وتعريب (`translation`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | original (this skill) |

**ما هي:** يتعرف على يناير/كانون الثاني/محرم وأيام الأسبوع بالعربية والإنجليزية ويقارنها بعد توحيد الهمزات. — Recognizes Gregorian, Levantine and Hijri month names and weekdays in Arabic and English, comparing after hamza folding.

**متى:** عند فحص التواريخ في نص عربي معاد كتابته أو مترجم أو ناتج عن OCR، وعند بناء محللات التواريخ / Checking dates in rewritten, translated or OCRed Arabic text; building date parsers.

**كيف:** Lists in anchor_gate.AR_WORDS: يناير…ديسمبر (with أبريل/ابريل/إبريل, يونيو/يونية), كانون، شباط، آذار، نيسان، أيار، حزيران، تموز، آب، أيلول، تشرين; محرم، صفر، ربيع، جمادى، رجب، شعبان، رمضان، شوال، القعدة، الحجة; weekdays with Egyptian forms (اتنين، تلات); الأحد only with ال. Never convert Hijri↔Gregorian unless asked. Ambiguous words left out on purpose (نص، ست، ضعف).

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** dates · hijri · months · weekdays · تاريخ هجري · شهور · أيام الأسبوع

#### 1. الاستقبال (A25)

- اللغتان: افتراض مكتوب ← إلى لغة رسالة المستخدم
- المستوى اللغوي: افتراض مكتوب ← فصحى معاصرة بسيطة
- مصطلحات ثابتة: افتراض مكتوب ← المصطلح الشائع مع الإنجليزي بين قوسين عند أول ذكر
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `document` ← المخرج `document`، والمنفّذ `method:ARL-05` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `anchor-gate` · `tell-scan`.
- مراحل النوع: المصطلحات الثابتة ← ترجمة ← مقابلة جملة بجملة ← مطابقة الأرقام والأسماء ← قراءة طبيعية ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المعنى كاملًا بلا حذف ولا إضافة ← مقابلة جملة بجملة
- إلزامي: الأرقام والأسماء والتواريخ مطابقة ← مقارنة آلية للأرقام
- جودة: تُقرأ طبيعية لا حرفية ← قراءة بصوت مسموع
- جودة: المصطلح الواحد مترجم بطريقة واحدة ← بحث المصطلحات
- أمر الحكم في الوضع 1: `think.py qa translation --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-writing/README.md`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-writing/test_writing.py`

#### 7. قدرات قريبة في العائلة

- `ARL-03` حدود الكلمة العربية مع السوابق / Clitic-aware Arabic word boundaries (proven)
- `ARL-04` قراءة الأرقام العربية: هندية وفارسية وفواصل ونسبة / Parse Arabic numerals, separators and percent (proven)
- `ARL-06` تشكيل الحروف للعرض: محرك واحد فقط / Shaping Arabic for display: exactly one engine (proven)
- `ARL-07` الاتجاه الثنائي في النصوص المختلطة / Bidi in mixed Arabic/Latin text (documented)

### `ARL-06` — تشكيل الحروف للعرض: محرك واحد فقط / Shaping Arabic for display: exactly one engine

| الحقل | القيمة |
|---|---|
| العائلة | `arabic-language` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/arabic-language.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | ترجمة وتعريب (`translation`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | arabic-reshaper MIT; python-bidi LGPL |

**ما هي:** المتصفح أو Pillow مع RAQM يشكّلان النص الخام مباشرة؛ arabic-reshaper مع python-bidi فقط للعارض الذي لا يشكّل؛ ولا تشكّل مرتين. — The browser or Pillow+RAQM shape raw text; reshaper+bidi only for renderers that do not shape; never shape twice.

**متى:** عند رسم العربية داخل صور أو رسوم بيانية أو ملفات PDF أو إطارات فيديو خارج المتصفح / Drawing Arabic into images, charts, PDFs or video frames outside a browser.

**كيف:** Check: PIL.features.check("raqm") (True here, Pillow 12.3.0) → ImageFont.truetype(font, size, layout_engine=ImageFont.Layout.RAQM) and draw raw logical text with direction="rtl". matplotlib 3.11 also bundles libraqm (check matplotlib.ft2font.__libraqm_version__): pass raw text there too; adding reshaper+bidi on top reverses it (proofs/general-data, mpl_arabic_modes.png). Only for reportlab, or a Pillow/matplotlib build without raqm: arabic_reshaper.reshape(t) then bidi.get_display(), with a font that has Presentation Forms-B (Amiri, Noto Naskh). Tested: reshaper gives U+FEB3 U+FEFC U+FEE1 for "سلام"; RAQM shaped "سلام" in Amiri at 82 px width. Full routing and failure modes: ARAB-06.

**التثبيت:** pip install arabic-reshaper python-bidi

**الوسوم:** shaping · raqm · arabic-reshaper · python-bidi · pillow · matplotlib · تشكيل الحروف · حروف مقطعة

#### 1. الاستقبال (A25)

- اللغتان: افتراض مكتوب ← إلى لغة رسالة المستخدم
- المستوى اللغوي: افتراض مكتوب ← فصحى معاصرة بسيطة
- مصطلحات ثابتة: افتراض مكتوب ← المصطلح الشائع مع الإنجليزي بين قوسين عند أول ذكر
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `pip:matplotlib` ← python3 -c "import matplotlib" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `pip:office` ← python3 -c "import office" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:arabic-reshaper` ← python3 -c "import arabic-reshaper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `document` ← المخرج `document`، والمنفّذ `method:ARL-06` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `anchor-gate` · `tell-scan`.
- مراحل النوع: المصطلحات الثابتة ← ترجمة ← مقابلة جملة بجملة ← مطابقة الأرقام والأسماء ← قراءة طبيعية ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المعنى كاملًا بلا حذف ولا إضافة ← مقابلة جملة بجملة
- إلزامي: الأرقام والأسماء والتواريخ مطابقة ← مقارنة آلية للأرقام
- جودة: تُقرأ طبيعية لا حرفية ← قراءة بصوت مسموع
- جودة: المصطلح الواحد مترجم بطريقة واحدة ← بحث المصطلحات
- أمر الحكم في الوضع 1: `think.py qa translation --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-writing/README.md`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-writing/arabic_probe.py`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-data/README.md`

#### 7. قدرات قريبة في العائلة

- `ARL-04` قراءة الأرقام العربية: هندية وفارسية وفواصل ونسبة / Parse Arabic numerals, separators and percent (proven)
- `ARL-05` أسماء الشهور والأيام: ميلادية وشامية وهجرية / Month and weekday names (Gregorian, Levantine, Hijri) (proven)
- `ARL-07` الاتجاه الثنائي في النصوص المختلطة / Bidi in mixed Arabic/Latin text (documented)
- `ARL-08` خطوط عربية: فحص وتثبيت / Arabic fonts: check and install (proven)

### `ARL-07` — الاتجاه الثنائي في النصوص المختلطة / Bidi in mixed Arabic/Latin text

| الحقل | القيمة |
|---|---|
| العائلة | `arabic-language` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/arabic-language.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | ترجمة وتعريب (`translation`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** علامات الاتجاه الخفية تُحذف قبل المعالجة وتُضاف عزلات الاتجاه عند العرض حول الكلمات اللاتينية والأرقام. — Strip invisible direction marks before processing; add direction isolates around Latin words and numbers when displaying.

**متى:** عند النصوص العربية/الإنجليزية المختلطة في واجهات المستخدم ورسائل الدردشة وملفات CSV المصدّرة والترجمات المرافقة التي فيها أسماء علامات أو أسعار / Mixed Arabic/English UI strings, chat messages, CSV exports, captions with brand names or prices.

**كيف:** Processing: remove LRM U+200E, RLM U+200F, ALM U+061C, embeddings U+202A–202E, isolates U+2066–2069 and BOM before matching (anchor_gate does this; tested on OCR output). Display: wrap embedded runs in FSI U+2068 … PDI U+2069 (or <bdi> / dir="auto" in HTML), keep % and currency with their number, never reverse strings by hand. Renderer-specific isolation for motion: ARAB-72.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** bidi · rtl · direction marks · isolates · اتجاه النص · نص مختلط

#### 1. الاستقبال (A25)

- اللغتان: افتراض مكتوب ← إلى لغة رسالة المستخدم
- المستوى اللغوي: افتراض مكتوب ← فصحى معاصرة بسيطة
- مصطلحات ثابتة: افتراض مكتوب ← المصطلح الشائع مع الإنجليزي بين قوسين عند أول ذكر
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `tesseract` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `document` ← المخرج `document`، والمنفّذ `method:ARL-07` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `anchor-gate` · `tell-scan`.
- مراحل النوع: المصطلحات الثابتة ← ترجمة ← مقابلة جملة بجملة ← مطابقة الأرقام والأسماء ← قراءة طبيعية ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المعنى كاملًا بلا حذف ولا إضافة ← مقابلة جملة بجملة
- إلزامي: الأرقام والأسماء والتواريخ مطابقة ← مقارنة آلية للأرقام
- جودة: تُقرأ طبيعية لا حرفية ← قراءة بصوت مسموع
- جودة: المصطلح الواحد مترجم بطريقة واحدة ← بحث المصطلحات
- أمر الحكم في الوضع 1: `think.py qa translation --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/scripts/anchor_gate.py`
- `kosif-tool/.claude/skills/kosif-superpowers/references/powers/typography-arabic.md`

#### 7. قدرات قريبة في العائلة

- `ARL-05` أسماء الشهور والأيام: ميلادية وشامية وهجرية / Month and weekday names (Gregorian, Levantine, Hijri) (proven)
- `ARL-06` تشكيل الحروف للعرض: محرك واحد فقط / Shaping Arabic for display: exactly one engine (proven)
- `ARL-08` خطوط عربية: فحص وتثبيت / Arabic fonts: check and install (proven)
- `ARL-09` سياسة التشكيل (الحركات) / Tashkeel policy (documented)

### `ARL-08` — خطوط عربية: فحص وتثبيت / Arabic fonts: check and install

| الحقل | القيمة |
|---|---|
| العائلة | `arabic-language` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/arabic-language.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | ترجمة وتعريب (`translation`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | OFL-1.1 (bundled fonts) |

**ما هي:** الحاوية لا تحمل خطًا عربيًا جيدًا افتراضيًا، لكن المهارة تحمل Amiri وCairo وTajawal وReem Kufi وAref Ruqaa وLalezar برخصة OFL. — The container has no good Arabic display face by default; the skill ships OFL Arabic fonts.

**متى:** قبل تصيير أي نص عربي إلى صورة أو PDF أو رسم بياني أو فيديو / Before rendering any Arabic text to an image, PDF, chart or video.

**كيف:** Check system coverage: fc-list :lang=ar family (here: only DejaVu, FreeSerif, FreeMono, Unifont). Use the bundled fonts in proofs/_shared/fonts (Amiri for Naskh and full tashkeel, Cairo/Tajawal for UI, Reem Kufi and Lalezar for display, Aref Ruqaa for calligraphic titles). System-wide install when root is available: apt-get install fonts-noto-core fonts-kacst fonts-arabeyes (from the environment probe; not run here). Font choice and fallback chains: ARAB-11, ARAB-13.

**التثبيت:** apt-get install -y fonts-noto-core fonts-kacst fonts-arabeyes (optional)

**الوسوم:** fonts · amiri · cairo · fc-list · خطوط عربية · خط

#### 1. الاستقبال (A25)

- اللغتان: افتراض مكتوب ← إلى لغة رسالة المستخدم
- المستوى اللغوي: افتراض مكتوب ← فصحى معاصرة بسيطة
- مصطلحات ثابتة: افتراض مكتوب ← المصطلح الشائع مع الإنجليزي بين قوسين عند أول ذكر
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `document` ← المخرج `document`، والمنفّذ `method:ARL-08` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `anchor-gate` · `tell-scan`.
- مراحل النوع: المصطلحات الثابتة ← ترجمة ← مقابلة جملة بجملة ← مطابقة الأرقام والأسماء ← قراءة طبيعية ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المعنى كاملًا بلا حذف ولا إضافة ← مقابلة جملة بجملة
- إلزامي: الأرقام والأسماء والتواريخ مطابقة ← مقارنة آلية للأرقام
- جودة: تُقرأ طبيعية لا حرفية ← قراءة بصوت مسموع
- جودة: المصطلح الواحد مترجم بطريقة واحدة ← بحث المصطلحات
- أمر الحكم في الوضع 1: `think.py qa translation --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-writing/README.md`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-writing/arabic_probe.py`

#### 7. قدرات قريبة في العائلة

- `ARL-06` تشكيل الحروف للعرض: محرك واحد فقط / Shaping Arabic for display: exactly one engine (proven)
- `ARL-07` الاتجاه الثنائي في النصوص المختلطة / Bidi in mixed Arabic/Latin text (documented)
- `ARL-09` سياسة التشكيل (الحركات) / Tashkeel policy (documented)
- `ARL-10` أدوات CAMeL Tools الخفيفة بلا نماذج / camel-tools character utilities without models (proven)

### `ARL-09` — سياسة التشكيل (الحركات) / Tashkeel policy

| الحقل | القيمة |
|---|---|
| العائلة | `arabic-language` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/arabic-language.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | ترجمة وتعريب (`translation`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** احذف التشكيل للمطابقة، واحفظه كما هو في القرآن والحديث والشعر، وأضفه فقط حيث يرفع لبسًا. — Strip harakat for matching, keep them untouched in sacred text and poetry, add them only to resolve ambiguity.

**متى:** عند تنظيف العربية المشكولة أو البحث فيها أو عرضها أو توليدها / Cleaning, searching, displaying or generating vowelled Arabic.

**كيف:** Matching: strip (ARL-01). Display: never "fix" or strip the diacritics of Quran, hadith or poetry; render full tashkeel with a font and engine that support it (Amiri + RAQM or a browser; leave headroom, ARAB-05). Writing: partial tashkeel only on words a reader could misread (عَلِم/عُلِم); random partial tashkeel on common words is a style tell. Automatic diacritization needs morphological models (ARL-11); review every result by eye and never auto-vowel sacred text. For speech alignment prefer vowelled source text over ASR output (ARAB-70).

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** tashkeel · harakat · diacritics · quran · تشكيل · حركات · ضبط بالشكل

#### 1. الاستقبال (A25)

- اللغتان: افتراض مكتوب ← إلى لغة رسالة المستخدم
- المستوى اللغوي: افتراض مكتوب ← فصحى معاصرة بسيطة
- مصطلحات ثابتة: افتراض مكتوب ← المصطلح الشائع مع الإنجليزي بين قوسين عند أول ذكر
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `document` ← المخرج `document`، والمنفّذ `method:ARL-09` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `anchor-gate` · `tell-scan`.
- مراحل النوع: المصطلحات الثابتة ← ترجمة ← مقابلة جملة بجملة ← مطابقة الأرقام والأسماء ← قراءة طبيعية ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المعنى كاملًا بلا حذف ولا إضافة ← مقابلة جملة بجملة
- إلزامي: الأرقام والأسماء والتواريخ مطابقة ← مقارنة آلية للأرقام
- جودة: تُقرأ طبيعية لا حرفية ← قراءة بصوت مسموع
- جودة: المصطلح الواحد مترجم بطريقة واحدة ← بحث المصطلحات
- أمر الحكم في الوضع 1: `think.py qa translation --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/references/humanizer.md`
- `kosif-tool/.claude/skills/kosif-superpowers/references/powers/typography-arabic.md`

#### 7. قدرات قريبة في العائلة

- `ARL-07` الاتجاه الثنائي في النصوص المختلطة / Bidi in mixed Arabic/Latin text (documented)
- `ARL-08` خطوط عربية: فحص وتثبيت / Arabic fonts: check and install (proven)
- `ARL-10` أدوات CAMeL Tools الخفيفة بلا نماذج / camel-tools character utilities without models (proven)
- `ARL-11` تحليل صرفي وتعرّف اللهجة والكيانات (CAMeL Tools كاملة) / Morphology, dialect ID and NER with full camel-tools (install)

### `ARL-10` — أدوات CAMeL Tools الخفيفة بلا نماذج / camel-tools character utilities without models

| الحقل | القيمة |
|---|---|
| العائلة | `arabic-language` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/arabic-language.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | ترجمة وتعريب (`translation`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | MIT |

**ما هي:** تحويل Buckwalter ذهابًا وإيابًا، وحذف التشكيل، وتوحيد الألف، من camel-tools دون تثبيت torch وtransformers. — Buckwalter round trip, dediacritization and alef normalization from camel-tools without installing torch and transformers.

**متى:** عند الحاجة إلى نقل حرفي ASCII دون فقدان لخطوط NLP، أو أدوات تطبيع موثوقة على جهاز بلا حزم تعلم آلي ثقيلة / Lossless ASCII transliteration for NLP pipelines, or reliable normalization helpers, on a machine without heavy ML packages.

**كيف:** pip install --no-deps camel-tools emoji (emoji is imported by camel_tools.utils.charsets). Then: CharMapper.builtin_mapper("ar2bw")(s) and "bw2ar" (round trip exact on "مُحَمَّدٌ يَقْرَأُ القُرْآنَ" → "muHama~dN yaqora>u Alquro\|na"), also ar2safebw and ar2hsb; camel_tools.utils.dediac.dediac_ar; normalize_alef_ar, normalize_alef_maksura_ar, normalize_teh_marbuta_ar. A plain pip install pulls transformers and torch.

**التثبيت:** pip install --no-deps camel-tools emoji

**الوسوم:** camel-tools · buckwalter · transliteration · dediac · nlp · معالجة اللغة · نقل حرفي

#### 1. الاستقبال (A25)

- اللغتان: افتراض مكتوب ← إلى لغة رسالة المستخدم
- المستوى اللغوي: افتراض مكتوب ← فصحى معاصرة بسيطة
- مصطلحات ثابتة: افتراض مكتوب ← المصطلح الشائع مع الإنجليزي بين قوسين عند أول ذكر
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:torch` ← python3 -c "import torch" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `pip:camel-tools` ← python3 -c "import camel-tools" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `document` ← المخرج `document`، والمنفّذ `method:ARL-10` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `anchor-gate` · `tell-scan`.
- مراحل النوع: المصطلحات الثابتة ← ترجمة ← مقابلة جملة بجملة ← مطابقة الأرقام والأسماء ← قراءة طبيعية ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المعنى كاملًا بلا حذف ولا إضافة ← مقابلة جملة بجملة
- إلزامي: الأرقام والأسماء والتواريخ مطابقة ← مقارنة آلية للأرقام
- جودة: تُقرأ طبيعية لا حرفية ← قراءة بصوت مسموع
- جودة: المصطلح الواحد مترجم بطريقة واحدة ← بحث المصطلحات
- أمر الحكم في الوضع 1: `think.py qa translation --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-writing/README.md`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-writing/arabic_probe.py`

#### 7. قدرات قريبة في العائلة

- `ARL-08` خطوط عربية: فحص وتثبيت / Arabic fonts: check and install (proven)
- `ARL-09` سياسة التشكيل (الحركات) / Tashkeel policy (documented)
- `ARL-11` تحليل صرفي وتعرّف اللهجة والكيانات (CAMeL Tools كاملة) / Morphology, dialect ID and NER with full camel-tools (install)
- `ARL-12` PyArabic للتنظيف والتقطيع (رخصة GPL) / PyArabic for cleanup and tokenizing (GPL) (proven)

### `ARL-11` — تحليل صرفي وتعرّف اللهجة والكيانات (CAMeL Tools كاملة) / Morphology, dialect ID and NER with full camel-tools

| الحقل | القيمة |
|---|---|
| العائلة | `arabic-language` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/arabic-language.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | ترجمة وتعريب (`translation`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `session` |
| الرخصة | MIT (code); data packages carry their own terms |

**ما هي:** التحليل الصرفي وفك اللبس وتعرّف اللهجة والكيانات المسماة تحتاج camel-tools كاملة مع حزم بيانات تُحمَّل. — Morphological analysis, disambiguation, dialect identification and NER need the full camel-tools install plus downloaded data packages.

**متى:** عند تحليل الجذوع وتقطيع اللواصق ووسم أقسام الكلام وتحديد لهجة مدونة واستخراج الأسماء والأماكن / Lemmatizing, segmenting clitics, tagging parts of speech, detecting the dialect of a corpus, extracting names and places.

**كيف:** pip install camel-tools (pulls transformers and torch; CPU torch installs in about 21 s, 769 MB here per the arsenal run), then download the data packages the task needs with the data tool camel-tools provides (list them first; sizes vary). Not run in this session: verify on the target machine and record the run before claiming it. For light character work use ARL-10 instead.

**التثبيت:** pip install camel-tools (+ its data packages)

**الوسوم:** camel-tools · morphology · dialect identification · ner · lemmatization · صرف · تعرف اللهجة · كيانات

#### 1. الاستقبال (A25)

- اللغتان: افتراض مكتوب ← إلى لغة رسالة المستخدم
- المستوى اللغوي: افتراض مكتوب ← فصحى معاصرة بسيطة
- مصطلحات ثابتة: افتراض مكتوب ← المصطلح الشائع مع الإنجليزي بين قوسين عند أول ذكر
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:torch` ← python3 -c "import torch" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `pip:camel-tools` ← python3 -c "import camel-tools" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `document` ← المخرج `document`، والمنفّذ `method:ARL-11` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `anchor-gate` · `tell-scan`.
- مراحل النوع: المصطلحات الثابتة ← ترجمة ← مقابلة جملة بجملة ← مطابقة الأرقام والأسماء ← قراءة طبيعية ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المعنى كاملًا بلا حذف ولا إضافة ← مقابلة جملة بجملة
- إلزامي: الأرقام والأسماء والتواريخ مطابقة ← مقارنة آلية للأرقام
- جودة: تُقرأ طبيعية لا حرفية ← قراءة بصوت مسموع
- جودة: المصطلح الواحد مترجم بطريقة واحدة ← بحث المصطلحات
- أمر الحكم في الوضع 1: `think.py qa translation --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `session-2026-10-16:general-arsenal.md#Full table`

#### 7. قدرات قريبة في العائلة

- `ARL-09` سياسة التشكيل (الحركات) / Tashkeel policy (documented)
- `ARL-10` أدوات CAMeL Tools الخفيفة بلا نماذج / camel-tools character utilities without models (proven)
- `ARL-12` PyArabic للتنظيف والتقطيع (رخصة GPL) / PyArabic for cleanup and tokenizing (GPL) (proven)
- `ARL-13` مقطّع Farasa عبر farasapy / Farasa segmenter via farasapy (install)

### `ARL-12` — PyArabic للتنظيف والتقطيع (رخصة GPL) / PyArabic for cleanup and tokenizing (GPL)

| الحقل | القيمة |
|---|---|
| العائلة | `arabic-language` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/arabic-language.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | ترجمة وتعريب (`translation`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | GPL |

**ما هي:** حذف التشكيل والتطويل وتقطيع بسيط، مع تنبيه: الرخصة GPL، فاستخدمها أداةً ولا تضمّن كودها في مشروع مغلق. — Strip tashkeel and tatweel and simple tokenization; GPL, so use it as a tool and do not bundle its code into closed projects.

**متى:** عند سكربتات التنظيف السريعة للعربية حيث يقبل ترخيص GPL / Quick Arabic cleanup scripts where GPL is acceptable.

**كيف:** pip install pyarabic; import pyarabic.araby as araby; araby.strip_tashkeel("مُحَمَّدٌ") → "محمد"; araby.strip_tatweel("عـــربي") → "عربي"; araby.tokenize(...) glues punctuation runs (":«", "»،"), so post-split punctuation if you count words. For MIT-only stacks use ARL-01 or ARL-10.

**التثبيت:** pip install pyarabic

**الوسوم:** pyarabic · tokenize · strip tashkeel · gpl · تقطيع · حذف التشكيل

#### 1. الاستقبال (A25)

- اللغتان: افتراض مكتوب ← إلى لغة رسالة المستخدم
- المستوى اللغوي: افتراض مكتوب ← فصحى معاصرة بسيطة
- مصطلحات ثابتة: افتراض مكتوب ← المصطلح الشائع مع الإنجليزي بين قوسين عند أول ذكر
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `document` ← المخرج `document`، والمنفّذ `method:ARL-12` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `anchor-gate` · `tell-scan`.
- مراحل النوع: المصطلحات الثابتة ← ترجمة ← مقابلة جملة بجملة ← مطابقة الأرقام والأسماء ← قراءة طبيعية ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المعنى كاملًا بلا حذف ولا إضافة ← مقابلة جملة بجملة
- إلزامي: الأرقام والأسماء والتواريخ مطابقة ← مقارنة آلية للأرقام
- جودة: تُقرأ طبيعية لا حرفية ← قراءة بصوت مسموع
- جودة: المصطلح الواحد مترجم بطريقة واحدة ← بحث المصطلحات
- أمر الحكم في الوضع 1: `think.py qa translation --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-writing/README.md`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-writing/arabic_probe.py`

#### 7. قدرات قريبة في العائلة

- `ARL-10` أدوات CAMeL Tools الخفيفة بلا نماذج / camel-tools character utilities without models (proven)
- `ARL-11` تحليل صرفي وتعرّف اللهجة والكيانات (CAMeL Tools كاملة) / Morphology, dialect ID and NER with full camel-tools (install)
- `ARL-13` مقطّع Farasa عبر farasapy / Farasa segmenter via farasapy (install)
- `ARL-14` التعرف الضوئي على العربية (tesseract) / Arabic OCR with tesseract (proven)

### `ARL-13` — مقطّع Farasa عبر farasapy / Farasa segmenter via farasapy

| الحقل | القيمة |
|---|---|
| العائلة | `arabic-language` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/arabic-language.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | ترجمة وتعريب (`translation`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `session` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مقطّع ومحلل عربي يعمل عبر Java؛ حزمة farasapy بلا رخصة معلنة على PyPI، فتحقق من الشروط قبل أي استخدام تجاري. — A Java-based Arabic segmenter; farasapy lists no license on PyPI, so check terms before commercial use.

**متى:** عند تقطيع اللواصق أو وسم أقسام الكلام حين لا يكون camel-tools خيارًا / Clitic segmentation or POS tagging when camel-tools is not an option.

**كيف:** pip install farasapy; needs a Java runtime (apt-get install default-jre if missing). Not run in this session. Compare its segmentation with camel-tools on a sample before choosing.

**التثبيت:** pip install farasapy (+ Java runtime)

**الوسوم:** farasa · segmentation · pos tagging · java · تقطيع صرفي

#### 1. الاستقبال (A25)

- اللغتان: افتراض مكتوب ← إلى لغة رسالة المستخدم
- المستوى اللغوي: افتراض مكتوب ← فصحى معاصرة بسيطة
- مصطلحات ثابتة: افتراض مكتوب ← المصطلح الشائع مع الإنجليزي بين قوسين عند أول ذكر
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:camel-tools` ← python3 -c "import camel-tools" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `document` ← المخرج `document`، والمنفّذ `method:ARL-13` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `anchor-gate` · `tell-scan`.
- مراحل النوع: المصطلحات الثابتة ← ترجمة ← مقابلة جملة بجملة ← مطابقة الأرقام والأسماء ← قراءة طبيعية ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المعنى كاملًا بلا حذف ولا إضافة ← مقابلة جملة بجملة
- إلزامي: الأرقام والأسماء والتواريخ مطابقة ← مقارنة آلية للأرقام
- جودة: تُقرأ طبيعية لا حرفية ← قراءة بصوت مسموع
- جودة: المصطلح الواحد مترجم بطريقة واحدة ← بحث المصطلحات
- أمر الحكم في الوضع 1: `think.py qa translation --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `session-2026-10-16:general-arsenal.md#Full table`

#### 7. قدرات قريبة في العائلة

- `ARL-11` تحليل صرفي وتعرّف اللهجة والكيانات (CAMeL Tools كاملة) / Morphology, dialect ID and NER with full camel-tools (install)
- `ARL-12` PyArabic للتنظيف والتقطيع (رخصة GPL) / PyArabic for cleanup and tokenizing (GPL) (proven)
- `ARL-14` التعرف الضوئي على العربية (tesseract) / Arabic OCR with tesseract (proven)
- `ARL-15` تحقق من أرقام OCR ببوابة المراسي / Verify OCR numbers with the anchor gate (proven)

### `ARL-14` — التعرف الضوئي على العربية (tesseract) / Arabic OCR with tesseract

| الحقل | القيمة |
|---|---|
| العائلة | `arabic-language` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/arabic-language.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | ترجمة وتعريب (`translation`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | tesseract Apache-2.0; pytesseract Apache-2.0 |

**ما هي:** tesseract مع حزمة ara يقرأ الكلمات العربية جيدًا لكنه يخطئ في الأرقام وعلامة % وقد يُسقط سطرًا كاملًا. — tesseract with ara reads Arabic words well but misreads digits and %, and can drop a whole line.

**متى:** عند استخراج نص عربي من مسوحات أو لقطات شاشة أو ملصقات أو إطارات فيديو / Extracting Arabic text from scans, screenshots, posters or video frames.

**كيف:** apt-get install -y tesseract-ocr tesseract-ocr-ara (root), then tesseract img.png out -l ara --psm 6 (add +eng for mixed text); Python: pytesseract (Apache-2.0). Tested on rendered lines: words right ("ارتفعت المبيعات … مارس", Cairo read الخميس, Amiri lost it), but ٢٥٪ → "ه5./" or "10", ٢٠٢٤ → "٠١74", 12 → ١١, and with Western digits the second line vanished; ×2 upscaling did not fix digits; output carries LRM/RLM marks. Always verify numbers (ARL-15) and look at the image. Scanned PDF pages: DOC-17. Pure-pip alternative: easyocr (Apache-2.0, needs torch, not run).

**المعاملات:** psm 3/4/6 gave identical text on single-column lines

**التثبيت:** apt-get install -y tesseract-ocr tesseract-ocr-ara && pip install pytesseract

**الوسوم:** ocr · tesseract · scan · arabic ocr · تعرف ضوئي · استخراج النص من الصور

#### 1. الاستقبال (A25)

- اللغتان: افتراض مكتوب ← إلى لغة رسالة المستخدم
- المستوى اللغوي: افتراض مكتوب ← فصحى معاصرة بسيطة
- مصطلحات ثابتة: افتراض مكتوب ← المصطلح الشائع مع الإنجليزي بين قوسين عند أول ذكر
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `tesseract` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:torch` ← python3 -c "import torch" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `document` ← المخرج `document`، والمنفّذ `method:ARL-14` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `anchor-gate` · `tell-scan`.
- مراحل النوع: المصطلحات الثابتة ← ترجمة ← مقابلة جملة بجملة ← مطابقة الأرقام والأسماء ← قراءة طبيعية ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المعنى كاملًا بلا حذف ولا إضافة ← مقابلة جملة بجملة
- إلزامي: الأرقام والأسماء والتواريخ مطابقة ← مقارنة آلية للأرقام
- جودة: تُقرأ طبيعية لا حرفية ← قراءة بصوت مسموع
- جودة: المصطلح الواحد مترجم بطريقة واحدة ← بحث المصطلحات
- أمر الحكم في الوضع 1: `think.py qa translation --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-writing/README.md`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-writing/arabic_probe.py`

#### 7. قدرات قريبة في العائلة

- `ARL-12` PyArabic للتنظيف والتقطيع (رخصة GPL) / PyArabic for cleanup and tokenizing (GPL) (proven)
- `ARL-13` مقطّع Farasa عبر farasapy / Farasa segmenter via farasapy (install)
- `ARL-15` تحقق من أرقام OCR ببوابة المراسي / Verify OCR numbers with the anchor gate (proven)
- `ARL-16` إصلاح الترميز المشوّه / Mojibake repair (proven)

### `ARL-15` — تحقق من أرقام OCR ببوابة المراسي / Verify OCR numbers with the anchor gate

| الحقل | القيمة |
|---|---|
| العائلة | `arabic-language` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/arabic-language.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | ترجمة وتعريب (`translation`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | original (this skill) |

**ما هي:** قارن ناتج OCR بنص مرجعي أو بقراءة ثانية عبر anchor_gate.py فيظهر كل رقم أو تاريخ أو نسبة قُرئت خطأ. — Diff OCR output against a reference or a second reading with anchor_gate.py to expose every misread number, date or percent.

**متى:** عند أي OCR لفواتير أو جداول أو إحصاءات أو تواريخ بالعربية / Any OCR of invoices, tables, statistics or dates in Arabic.

**كيف:** python3 -I scripts/anchor_gate.py --before truth_or_second_read.txt --after ocr.txt --text. Invisible bidi marks in OCR output are stripped, digit systems are equated. Tested: OCR of "٢٥٪ … ٢٠٢٤ … ١٢ مارس" → REVIEW_REQUIRED, dropped 12, 2024, 25%. With no reference, OCR twice (two fonts/scales or two engines) and diff the readings; disagreement marks the cells to check by eye.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ocr qa · numbers · verification · تحقق · أرقام

#### 1. الاستقبال (A25)

- اللغتان: افتراض مكتوب ← إلى لغة رسالة المستخدم
- المستوى اللغوي: افتراض مكتوب ← فصحى معاصرة بسيطة
- مصطلحات ثابتة: افتراض مكتوب ← المصطلح الشائع مع الإنجليزي بين قوسين عند أول ذكر
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `tesseract` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `document` ← المخرج `document`، والمنفّذ `method:ARL-15` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `anchor-gate` · `tell-scan`.
- مراحل النوع: المصطلحات الثابتة ← ترجمة ← مقابلة جملة بجملة ← مطابقة الأرقام والأسماء ← قراءة طبيعية ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المعنى كاملًا بلا حذف ولا إضافة ← مقابلة جملة بجملة
- إلزامي: الأرقام والأسماء والتواريخ مطابقة ← مقارنة آلية للأرقام
- جودة: تُقرأ طبيعية لا حرفية ← قراءة بصوت مسموع
- جودة: المصطلح الواحد مترجم بطريقة واحدة ← بحث المصطلحات
- أمر الحكم في الوضع 1: `think.py qa translation --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-writing/README.md`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-writing/arabic_probe.py`

#### 7. قدرات قريبة في العائلة

- `ARL-13` مقطّع Farasa عبر farasapy / Farasa segmenter via farasapy (install)
- `ARL-14` التعرف الضوئي على العربية (tesseract) / Arabic OCR with tesseract (proven)
- `ARL-16` إصلاح الترميز المشوّه / Mojibake repair (proven)
- `ARL-17` التعامل مع اللهجات وتحديد السجل / Dialect handling and register choice (documented)

### `ARL-16` — إصلاح الترميز المشوّه / Mojibake repair

| الحقل | القيمة |
|---|---|
| العائلة | `arabic-language` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/arabic-language.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | ترجمة وتعريب (`translation`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | original (this skill) |

**ما هي:** "Ø³Ù„Ø§Ù…" نص UTF-8 قُرئ على أنه cp1252، ويُصلح بعكس الخطوة؛ والملفات القديمة بترميز Windows-1256 تُفك به. — UTF-8 read as cp1252 is reversed by re-encoding; legacy Windows-1256 files decode with cp1256.

**متى:** عند ظهور العربية في ملفات CSV أو ترجمات أو رسائل بريد أو نسخ قواعد بيانات على شكل Ø³Ù„… أو «???» / CSV, subtitles, emails or database dumps where Arabic shows as Ø³Ù„… or as "???".

**كيف:** Python: garbled.encode("cp1252").decode("utf-8") (tested: "Ø³Ù„Ø§Ù… Ø¹Ù„ÙŠÙƒÙ…" → "سلام عليكم"). If bytes fail as UTF-8, try cp1256 (tested: d3e1c7e3 → "سلام"). Write CSV for spreadsheet apps as UTF-8 with BOM (encoding="utf-8-sig") so Arabic opens correctly. "???" means the text was already destroyed; go back to the source. File-name mojibake: ARAB-81.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** encoding · mojibake · cp1256 · utf-8 · csv · ترميز · حروف غريبة

#### 1. الاستقبال (A25)

- اللغتان: افتراض مكتوب ← إلى لغة رسالة المستخدم
- المستوى اللغوي: افتراض مكتوب ← فصحى معاصرة بسيطة
- مصطلحات ثابتة: افتراض مكتوب ← المصطلح الشائع مع الإنجليزي بين قوسين عند أول ذكر
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `document` ← المخرج `document`، والمنفّذ `method:ARL-16` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `anchor-gate` · `tell-scan`.
- مراحل النوع: المصطلحات الثابتة ← ترجمة ← مقابلة جملة بجملة ← مطابقة الأرقام والأسماء ← قراءة طبيعية ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المعنى كاملًا بلا حذف ولا إضافة ← مقابلة جملة بجملة
- إلزامي: الأرقام والأسماء والتواريخ مطابقة ← مقارنة آلية للأرقام
- جودة: تُقرأ طبيعية لا حرفية ← قراءة بصوت مسموع
- جودة: المصطلح الواحد مترجم بطريقة واحدة ← بحث المصطلحات
- أمر الحكم في الوضع 1: `think.py qa translation --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-writing/README.md`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-writing/arabic_probe.py`

#### 7. قدرات قريبة في العائلة

- `ARL-14` التعرف الضوئي على العربية (tesseract) / Arabic OCR with tesseract (proven)
- `ARL-15` تحقق من أرقام OCR ببوابة المراسي / Verify OCR numbers with the anchor gate (proven)
- `ARL-17` التعامل مع اللهجات وتحديد السجل / Dialect handling and register choice (documented)
- `ARL-18` النقل الحرفي والرومنة / Transliteration and romanization (proven)

### `ARL-17` — التعامل مع اللهجات وتحديد السجل / Dialect handling and register choice

| الحقل | القيمة |
|---|---|
| العائلة | `arabic-language` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/arabic-language.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | ترجمة وتعريب (`translation`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حدد السجل قبل الكتابة (فصحى رسمية، فصحى مبسطة، مصرية، خليجية، شامية، حجازية، مغاربية) والتزم به، ولا تعامل اللهجات كلهجة واحدة. — Choose the register before writing and keep it; do not treat Arabic dialects as one.

**متى:** عند أي مخرجات عربية: ترجمات مرافقة ومنشورات وسكربتات ونصوص واجهات وردود على مستخدم يكتب بلهجة / Any Arabic output: captions, posts, scripts, UI text, replies to a user who writes in dialect.

**كيف:** Reply in the user's register unless asked otherwise. Egyptian markers: مش، هـ/حـ (future)، اللي، ده/دي/دول، إزاي، دلوقتي. Levantine: شو، هلّق، كتير، منيح. Gulf: وايد، شلون، زين. Maghrebi: برشا، بزاف. Do not Egyptianize other dialects or judge them by MSA rules; keep one spelling convention; no fake dialect sprinkles. Automatic dialect ID exists in full camel-tools (ARL-11, not run here). Rewriting between registers: WRITE-19.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** dialect · register · egyptian · gulf · levantine · لهجة · عامية · فصحى · translate · translation · ترجم · ترجمة · عقد · contract

#### 1. الاستقبال (A25)

- اللغتان: افتراض مكتوب ← إلى لغة رسالة المستخدم
- المستوى اللغوي: افتراض مكتوب ← فصحى معاصرة بسيطة
- مصطلحات ثابتة: افتراض مكتوب ← المصطلح الشائع مع الإنجليزي بين قوسين عند أول ذكر
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:camel-tools` ← python3 -c "import camel-tools" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `document` ← المخرج `document`، والمنفّذ `method:ARL-17` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `anchor-gate` · `tell-scan`.
- مراحل النوع: المصطلحات الثابتة ← ترجمة ← مقابلة جملة بجملة ← مطابقة الأرقام والأسماء ← قراءة طبيعية ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المعنى كاملًا بلا حذف ولا إضافة ← مقابلة جملة بجملة
- إلزامي: الأرقام والأسماء والتواريخ مطابقة ← مقارنة آلية للأرقام
- جودة: تُقرأ طبيعية لا حرفية ← قراءة بصوت مسموع
- جودة: المصطلح الواحد مترجم بطريقة واحدة ← بحث المصطلحات
- أمر الحكم في الوضع 1: `think.py qa translation --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/references/humanizer.md`

#### 7. قدرات قريبة في العائلة

- `ARL-15` تحقق من أرقام OCR ببوابة المراسي / Verify OCR numbers with the anchor gate (proven)
- `ARL-16` إصلاح الترميز المشوّه / Mojibake repair (proven)
- `ARL-18` النقل الحرفي والرومنة / Transliteration and romanization (proven)
- `ARL-19` مراجعة المطابقة النحوية بعد التعديل / Agreement check after editing (documented)

### `ARL-18` — النقل الحرفي والرومنة / Transliteration and romanization

| الحقل | القيمة |
|---|---|
| العائلة | `arabic-language` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/arabic-language.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | ترجمة وتعريب (`translation`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | MIT |

**ما هي:** Buckwalter للتحويل الآلي بلا فقد بين العربية والـASCII، أما أسماء الناس فتُكتب كما يكتبها أصحابها (Mohamed أو Muhammad). — Buckwalter for lossless machine transliteration; people's names keep the Latin spelling they use themselves.

**متى:** عند تخزين العربية في أنظمة ASCII فقط، وبناء ميزات NLP، وكتابة الأسماء العربية داخل نص إنجليزي، وقراءة محادثات Arabizi / Storing Arabic in ASCII-only systems, building NLP features, writing Arabic names in English text, reading Arabizi chat.

**كيف:** Lossless: camel-tools ar2bw / bw2ar (round trip exact, ARL-10). Readers: use the spelling the person, brand or publication already uses; never "correct" a name's romanization; keep it in the anchor keep list (WRITE-08). Arabizi (Franco) chat uses digits for letters (3 for ع, 7 for ح, 2 for ء, 5 for خ); conventions vary by region, so confirm with the user and never auto-convert names.

**التثبيت:** pip install --no-deps camel-tools emoji

**الوسوم:** transliteration · romanization · buckwalter · arabizi · franco · نقل حرفي · فرانكو · عربيزي

#### 1. الاستقبال (A25)

- اللغتان: افتراض مكتوب ← إلى لغة رسالة المستخدم
- المستوى اللغوي: افتراض مكتوب ← فصحى معاصرة بسيطة
- مصطلحات ثابتة: افتراض مكتوب ← المصطلح الشائع مع الإنجليزي بين قوسين عند أول ذكر
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:camel-tools` ← python3 -c "import camel-tools" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `document` ← المخرج `document`، والمنفّذ `method:ARL-18` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `anchor-gate` · `tell-scan`.
- مراحل النوع: المصطلحات الثابتة ← ترجمة ← مقابلة جملة بجملة ← مطابقة الأرقام والأسماء ← قراءة طبيعية ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المعنى كاملًا بلا حذف ولا إضافة ← مقابلة جملة بجملة
- إلزامي: الأرقام والأسماء والتواريخ مطابقة ← مقارنة آلية للأرقام
- جودة: تُقرأ طبيعية لا حرفية ← قراءة بصوت مسموع
- جودة: المصطلح الواحد مترجم بطريقة واحدة ← بحث المصطلحات
- أمر الحكم في الوضع 1: `think.py qa translation --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-writing/README.md`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-writing/arabic_probe.py`

#### 7. قدرات قريبة في العائلة

- `ARL-16` إصلاح الترميز المشوّه / Mojibake repair (proven)
- `ARL-17` التعامل مع اللهجات وتحديد السجل / Dialect handling and register choice (documented)
- `ARL-19` مراجعة المطابقة النحوية بعد التعديل / Agreement check after editing (documented)
- `ARL-20` CAMeL Tools: تقطيع النص العربي واستخراج الجذور والتشكيل وتحديد / CAMeL Tools: Tokenise, lemmatise, diacritise and dialect-identify Arabic text (install)

### `ARL-19` — مراجعة المطابقة النحوية بعد التعديل / Agreement check after editing

| الحقل | القيمة |
|---|---|
| العائلة | `arabic-language` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/arabic-language.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | ترجمة وتعريب (`translation`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل نقل للفاعل أو تغيير للعدد يغيّر المطابقة: "قررت اللجنة" لكن "حضر الطلاب" ثم "الطلاب حضروا"، والعدد من 3 إلى 10 يخالف المعدود. — Moving the subject or changing a count changes agreement; numbers 3–10 take the opposite gender of the counted noun.

**متى:** بعد إعادة كتابة الجمل العربية أو إعادة هيكلتها أو قولبتها (فعلية ↔ اسمية، مفرد ↔ جمع، أرقام مُدرجة) / After rewriting, restructuring or templating Arabic sentences (verb-first ↔ subject-first, singular ↔ plural, inserted numbers).

**كيف:** Verb before a plural subject stays singular (حضر الطلاب); after it, it agrees in number (الطلاب حضروا). Feminine subjects take feminine verbs (أجّلت اللجنة). Numbers 3–10 reverse gender (ثلاثة أيام، ثلاث ساعات); 11–99 take a singular accusative noun; dual nouns take dual agreement. For generated templates with counts, use the plural rules in ARAB-76. Read the final text once only for agreement.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** grammar · agreement · gender · number · نحو · مطابقة · العدد والمعدود · translate · translation · ترجم · ترجمة · عقد · contract

#### 1. الاستقبال (A25)

- اللغتان: افتراض مكتوب ← إلى لغة رسالة المستخدم
- المستوى اللغوي: افتراض مكتوب ← فصحى معاصرة بسيطة
- مصطلحات ثابتة: افتراض مكتوب ← المصطلح الشائع مع الإنجليزي بين قوسين عند أول ذكر
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `document` ← المخرج `document`، والمنفّذ `method:ARL-19` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `anchor-gate` · `tell-scan`.
- مراحل النوع: المصطلحات الثابتة ← ترجمة ← مقابلة جملة بجملة ← مطابقة الأرقام والأسماء ← قراءة طبيعية ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المعنى كاملًا بلا حذف ولا إضافة ← مقابلة جملة بجملة
- إلزامي: الأرقام والأسماء والتواريخ مطابقة ← مقارنة آلية للأرقام
- جودة: تُقرأ طبيعية لا حرفية ← قراءة بصوت مسموع
- جودة: المصطلح الواحد مترجم بطريقة واحدة ← بحث المصطلحات
- أمر الحكم في الوضع 1: `think.py qa translation --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/references/humanizer.md`
- `kosif-tool/.claude/skills/kosif-superpowers/references/powers/typography-arabic.md`

#### 7. قدرات قريبة في العائلة

- `ARL-17` التعامل مع اللهجات وتحديد السجل / Dialect handling and register choice (documented)
- `ARL-18` النقل الحرفي والرومنة / Transliteration and romanization (proven)
- `ARL-20` CAMeL Tools: تقطيع النص العربي واستخراج الجذور والتشكيل وتحديد / CAMeL Tools: Tokenise, lemmatise, diacritise and dialect-identify Arabic text (install)
- `ARL-21` spaCy: تقطيع العربية ومطابقة القواعد؛ واستخراج الكيانات مع / spaCy: Tokenise Arabic and match rules (blank 'ar'); NER with downloaded models (proven)

### `ARL-20` — CAMeL Tools: تقطيع النص العربي واستخراج الجذور والتشكيل وتحديد / CAMeL Tools: Tokenise, lemmatise, diacritise and dialect-identify Arabic text

| الحقل | القيمة |
|---|---|
| العائلة | `arabic-language` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/arabic-language.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | ترجمة وتعريب (`translation`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** تقطيع النص العربي واستخراج الجذور والتشكيل وتحديد اللهجة. — Tokenise, lemmatise, diacritise and dialect-identify Arabic text. (CAMeL Tools, ★0.6k, MIT).

**متى:** عند مهام معالجة العربية الطبيعية التي يحق للمستخدم تشغيلها / arabic nlp tasks the user has the right to run

**كيف:** `pip install camel-tools && camel_data -i light`. Licence note: permissive.

**التثبيت:** pip install camel-tools && camel_data -i light

**الوسوم:** Arabic NLP · CAMeL Tools · toolbelt · توسعة

#### 1. الاستقبال (A25)

- اللغتان: افتراض مكتوب ← إلى لغة رسالة المستخدم
- المستوى اللغوي: افتراض مكتوب ← فصحى معاصرة بسيطة
- مصطلحات ثابتة: افتراض مكتوب ← المصطلح الشائع مع الإنجليزي بين قوسين عند أول ذكر
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:camel-tools` ← python3 -c "import camel-tools" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `document` ← المخرج `document`، والمنفّذ `method:ARL-20` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `anchor-gate` · `tell-scan`.
- مراحل النوع: المصطلحات الثابتة ← ترجمة ← مقابلة جملة بجملة ← مطابقة الأرقام والأسماء ← قراءة طبيعية ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المعنى كاملًا بلا حذف ولا إضافة ← مقابلة جملة بجملة
- إلزامي: الأرقام والأسماء والتواريخ مطابقة ← مقارنة آلية للأرقام
- جودة: تُقرأ طبيعية لا حرفية ← قراءة بصوت مسموع
- جودة: المصطلح الواحد مترجم بطريقة واحدة ← بحث المصطلحات
- أمر الحكم في الوضع 1: `think.py qa translation --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `ARL-18` النقل الحرفي والرومنة / Transliteration and romanization (proven)
- `ARL-19` مراجعة المطابقة النحوية بعد التعديل / Agreement check after editing (documented)
- `ARL-21` spaCy: تقطيع العربية ومطابقة القواعد؛ واستخراج الكيانات مع / spaCy: Tokenise Arabic and match rules (blank 'ar'); NER with downloaded models (proven)
- `ARL-22` Argos Translate: ترجمة عربي-إنجليزي دون اتصال تمامًا / Argos Translate: Translate Arabic↔English fully offline (install)

### `ARL-21` — spaCy: تقطيع العربية ومطابقة القواعد؛ واستخراج الكيانات مع / spaCy: Tokenise Arabic and match rules (blank 'ar'); NER with downloaded models

| الحقل | القيمة |
|---|---|
| العائلة | `arabic-language` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/arabic-language.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | ترجمة وتعريب (`translation`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | MIT |

**ما هي:** تقطيع العربية ومطابقة القواعد؛ واستخراج الكيانات مع النماذج. — Tokenise Arabic and match rules (blank 'ar'); NER with downloaded models. (spaCy, ★34.0k, MIT).

**متى:** عند مهام NLP التي يحق للمستخدم تشغيلها / nlp tasks the user has the right to run

**كيف:** `pip install spacy`. Verified here 2026-10-18: 8 Arabic tokens; matched 'يوم الجمعة' (spacy 3.8.16). Licence note: permissive.

**التثبيت:** pip install spacy

**الوسوم:** NLP · spaCy · toolbelt · توسعة

#### 1. الاستقبال (A25)

- اللغتان: افتراض مكتوب ← إلى لغة رسالة المستخدم
- المستوى اللغوي: افتراض مكتوب ← فصحى معاصرة بسيطة
- مصطلحات ثابتة: افتراض مكتوب ← المصطلح الشائع مع الإنجليزي بين قوسين عند أول ذكر
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:spacy` ← python3 -c "import spacy" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `document` ← المخرج `document`، والمنفّذ `method:ARL-21` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `anchor-gate` · `tell-scan`.
- مراحل النوع: المصطلحات الثابتة ← ترجمة ← مقابلة جملة بجملة ← مطابقة الأرقام والأسماء ← قراءة طبيعية ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المعنى كاملًا بلا حذف ولا إضافة ← مقابلة جملة بجملة
- إلزامي: الأرقام والأسماء والتواريخ مطابقة ← مقارنة آلية للأرقام
- جودة: تُقرأ طبيعية لا حرفية ← قراءة بصوت مسموع
- جودة: المصطلح الواحد مترجم بطريقة واحدة ← بحث المصطلحات
- أمر الحكم في الوضع 1: `think.py qa translation --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/toolbelt-smoke/README.md`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/toolbelt-smoke/smoke.py`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/toolbelt-smoke/results.json`

#### 7. قدرات قريبة في العائلة

- `ARL-19` مراجعة المطابقة النحوية بعد التعديل / Agreement check after editing (documented)
- `ARL-20` CAMeL Tools: تقطيع النص العربي واستخراج الجذور والتشكيل وتحديد / CAMeL Tools: Tokenise, lemmatise, diacritise and dialect-identify Arabic text (install)
- `ARL-22` Argos Translate: ترجمة عربي-إنجليزي دون اتصال تمامًا / Argos Translate: Translate Arabic↔English fully offline (install)

### `ARL-22` — Argos Translate: ترجمة عربي-إنجليزي دون اتصال تمامًا / Argos Translate: Translate Arabic↔English fully offline

| الحقل | القيمة |
|---|---|
| العائلة | `arabic-language` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/arabic-language.md)) |
| المجموعة | الخطوط والنصوص العربية واللاتينية (`type`) |
| نوع المخرج (A25، A27) | ترجمة وتعريب (`translation`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** ترجمة عربي-إنجليزي دون اتصال تمامًا. — Translate Arabic↔English fully offline. (Argos Translate, ★6.6k, MIT).

**متى:** عند مهام الترجمة التي يحق للمستخدم تشغيلها / translation tasks the user has the right to run

**كيف:** `pip install argostranslate (+ ar↔en package ~100 MB)`. Verified here 2026-10-18: import OK; install ar↔en package before translating (argostranslate ). Licence note: permissive.

**التثبيت:** pip install argostranslate (+ ar↔en package ~100 MB)

**الوسوم:** Translation · Argos Translate · toolbelt · توسعة

#### 1. الاستقبال (A25)

- اللغتان: افتراض مكتوب ← إلى لغة رسالة المستخدم
- المستوى اللغوي: افتراض مكتوب ← فصحى معاصرة بسيطة
- مصطلحات ثابتة: افتراض مكتوب ← المصطلح الشائع مع الإنجليزي بين قوسين عند أول ذكر
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:argos` ← python3 -c "import argos" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `document` ← المخرج `document`، والمنفّذ `method:ARL-22` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `anchor-gate` · `tell-scan`.
- مراحل النوع: المصطلحات الثابتة ← ترجمة ← مقابلة جملة بجملة ← مطابقة الأرقام والأسماء ← قراءة طبيعية ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المعنى كاملًا بلا حذف ولا إضافة ← مقابلة جملة بجملة
- إلزامي: الأرقام والأسماء والتواريخ مطابقة ← مقارنة آلية للأرقام
- جودة: تُقرأ طبيعية لا حرفية ← قراءة بصوت مسموع
- جودة: المصطلح الواحد مترجم بطريقة واحدة ← بحث المصطلحات
- أمر الحكم في الوضع 1: `think.py qa translation --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `ARL-20` CAMeL Tools: تقطيع النص العربي واستخراج الجذور والتشكيل وتحديد / CAMeL Tools: Tokenise, lemmatise, diacritise and dialect-identify Arabic text (install)
- `ARL-21` spaCy: تقطيع العربية ومطابقة القواعد؛ واستخراج الكيانات مع / spaCy: Tokenise Arabic and match rules (blank 'ar'); NER with downloaded models (proven)

