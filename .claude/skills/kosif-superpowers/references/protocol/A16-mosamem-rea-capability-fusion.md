# A16 — Mosamem v0.1.0 × REA v6.7 × KOSIF Superpowers

> **النواة:** [PROTOCOL.md](../../PROTOCOL.md). لا يتجاوز هذا الملحق قواعد النواة.
>
> **متى تقرأه / when to read:** المستخدم يطلب دمج قدرات مصمم `motalim-ai/mosamem` أو REA `morluto/rea`، تحسين تعديل الصور العربية أو الطبقات وPSD، أو هندسة عكسية نظامية لبناء مهارات تصميم جديدة.
>
> **لا يستبدل** `PROTOCOL.md`؛ هو ملحق تكامل. حدود Katana في A8 ما زالت فعالة.

## المصدر ونطاق التحقق

- [Mosamem v0.1.0](https://github.com/motalim-ai/mosamem/releases/tag/v0.1.0) — اقرأ `README.md`, `docs/status.md`, `docs/psd-report.md`, `THIRD-PARTY-NOTICES.md`, `LICENSE` من نفس الوسم، وليس افتراض آخر إصدار. الرخصة **GPL-3.0-or-later**، وملف `package.json` يذكر Tauri/Svelte/ag-psd مع طبقة Rust مستقلة. هذه قدرات **موصوفة أو مختبرة من قِبل المصدر** لا تأكيد أنها مثبتة على جهاز KOSIF.
- [REA upstream](https://github.com/morluto/rea) — المستودع يذكر حزمة `rea-agents` وMIT، و`package.json` على main وقت المراجعة أعلن الإصدار 6.7.0، والنسخ الجديدة قد تختلف. يستخدم محللات JavaScript/Electron و.NET وحزم ومكونات native وCDP وGhidra/Hopper عند توفر مزود مخوّل. تحكمه الأدلة ونطاق الهدف المأذون فقط. مسار REA مثبت مسبقًا في KOSIF عبر `scripts/rea_bridge.py` وفهرس `data/powers/software-investigation.json`؛ **لا تكرر 153 أمرًا كقدرات جديدة**.
- تحت `data/mosamem_rea_capabilities.json`: **19 عقدة تكامل/طريقة** موثقة بالمصدر وحالة المنفذ — **ليست 19 محرّك صور جديدًا**. كتّابها أصلية ولا تحتوي كود أو أصول Mosamem GPL أو نماذج AI أو خطوط.
- [تقرير توافق PSD للمصدر](https://github.com/motalim-ai/mosamem/blob/v0.1.0/docs/psd-report.md): 87/90 ملفات اختبار فُتحت، 87/87 إعادة حفظ ذاتية حافظت على البنية والبكسل في اختبارات المشروع، 50 ملفًا اقترب مطابقته من flattened Photoshop بالمعيار الصارم، 8 قريبة، 20 مختلفة، 9 بلا مرجع قابل للمقارنة، و3 لم تُفتح (CMYK). لا تدّعِ أن PSD عالي التعقيد ينتقل بلا فقد؛ لا تسند اختبار المنتج إلى KOSIF.

## قدرات مُدمجة بالفعل في KOSIF كجسر أصلي

`scripts/mosamem_rea_fusion.py` يعتمد مكتبات Python القياسية، ويتكامل مع `rea_bridge.py` دون تثبيت إضافي أو دفع أو اتصال خارجي. استعمله على **جهاز مخوّل** وملفات يملكها المستخدم.

```bash
SK=.claude/skills/kosif-superpowers
python3 "$SK/scripts/mosamem_rea_fusion.py" doctor
python3 "$SK/scripts/mosamem_rea_fusion.py" catalog
python3 "$SK/scripts/mosamem_rea_fusion.py" plan "خلفية شفافة مع كتابة عربية" --domain image --out out/image-plan.json
python3 "$SK/scripts/mosamem_rea_fusion.py" plan "مونتاج ريلز بخط عربي" --domain motion
python3 "$SK/scripts/mosamem_rea_fusion.py" inspect "my-artwork.psd" --out out/psd-preflight.json
python3 "$SK/scripts/mosamem_rea_fusion.py" rea-plan javascript "path/to/authorized-js-app"
python3 -m unittest discover -s "$SK/evals" -p 'test_mosamem_rea_fusion.py' -v
```

حالات الأوامر: `doctor` يختبر البيئة ووجود REA في PATH ونسخة Node الملائمة، ويتفقد مسارات Mosamem المعروفة دون تشغيل. `catalog` يردّ بالعقد المقيدة المصدر. `plan` يولّد 5 عُقد مترابطة: جرد أصول مرخّصة → تحرير بواسطة أدوات KOSIF/واجهة Mosamem → تحليل REA اختياري بعد تصريح → QA → تسجيل وصفة FusionForge خاصة بالمشروع. `inspect` يقرأ **رأس** PSD/PSB/PNG/JPEG وبصمة SHA-256، ويحذر من CMYK أو 16/32-bit في ملفات PSD وغير المعروف في التوافق. لا يفتح طبقات PSD ولا يفحص التشابه البصري ولا ينفذ إزالة خلفية. `rea-plan` يستدعي **المخطط الموجود** فقط ولا يشغّل REA.

## تكاملات هجينة موصى بها

| مطلب | المصدر/أداة البداية | التسليم التالي | قيد قياس |
|---|---|---|---|
| صور إعلانية عربية | Mosamem: RTL editable type، styles، adjustments | KOSIF font fidelity → export QA | إعادة فتح النص، صلاحية الخطوط |
| إزالة خلفية | Mosamem (BiRefNet) محليًا بعد تنزيل النموذج بإذن | طبقات أصلية وأقنعة أو مصدر PNG مصرح به | فحص حواف الشعر والشفافية |
| تحديد كائن | Mosamem (SAM 2.1) GUI | mask → layers → controlled export | مراجعة الإنسان للقناع |
| ملء ذكي | Mosamem (MI-GAN) GUI | قبل/بعد + قياس تشوهات | ليس إنتاجًا مضمونًا |
| تحرير PSD | KOSIF preflight → Mosamem GUI | comparison against a flattened original | تحذير CMYK والأنماط المعقدة |
| رسومات لقطات فيديو | Mosamem طبقات → PNG مرخّص | KOSIF timeline/FFmpeg + audio-alignment | الزمن الأصلي يقود الحركة |
| البحث عن وظيفة برمجية | REA planner + existing `rea_bridge.py` | authorized static analysis → evidence packet | independent check, no automatic copying |

## فصل المصدر والتنفيذ والتحقق

1. لا تُنقل **أي ملفات Rust/TS/صور/خطوط** من Mosamem إلى KOSIF مباشرة. GPL تعطي حق استخدام المشروع وتعديله تحت شروطها، لكن الدمج داخل مشروع آخر قد ينشئ التزامات copyleft. استلهم **السلوك الموثق** أو شغّل التطبيق كأداة مستقلة. أي ضم مصدر يخضع لمراجعة قانونية مستقلة.
2. ليس لـMosamem `v0.1.0` API آلي موثق للتحكم في واجهته؛ لا تدّعِ إزالة خلفية تلقائية داخل KOSIF لمجرد ظهورها في كتالوج التكامل.
3. REA مصدر MIT مع مزودين وأدوات تجارية بشروط مستقلة. لا يثبت التنفيذ إلا `run_static` على هدف مأذون مع إيصال ونتيجة محفوظة محليًا؛ لا تستدعِ runtime/browser attach أو فك ثنائي بلا تفويض صريح مستقل. الأمر `npx rea-agents setup` ليس جزءًا من التخطيط أو doctor.
4. كل شركة ومحتوياتها تبقى منعزلة، لا تنشر ملفات PSD أو لقطات ونتائج تفكيك أو بصمات طريق خاصة في GitHub.
5. ليس هناك «تعليم أوزان Claude». المخرجات الجديدة تتحول إلى وصفة FusionForge مرشحة ثم اختبار فعلي وQA وأدلة وموافقة ترقية؛ لا يُرفع مجرد الشرح إلى «مهارة منفذة».
6. **Katana** يبقى للتحليل فقط إن أمكن إثبات وضع لا يستهلك رصيدًا، لا توليد أبدًا.

## اختبارات الجودة قبل الدمج

- `test_mosamem_rea_fusion.py` يشمل حفظ الملفات من التعديل، تشخيص PNG/JPEG/PSD وCMYK، التخطيط المقيّد، وفشل مغلق عند هدف REA مفقود، وسرية بيانات الشركات.
- أكمل فحوص `check_skill.py` الخاصة بالمستودع بعد التغييرات.
- يجب ألا يمنح نجاح هذه الاختبارات ادعاء تشغيل Mosamem فعليًا أو إصدار صورة PSD معدلة، أو نتيجة REA على التطبيق. الأجهزة والنماذج والنسخ المستهدفة تحتاج اختبارًا إضافيًا.
