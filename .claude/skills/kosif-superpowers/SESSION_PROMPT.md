# رسالة التفعيل — انسخها كما هي في أول أي جلسة جديدة مع Claude

> آخر تحديث: 21-10-2026 · المصدر: `kosif199022-jpg/kosif-tool` → `.claude/skills/kosif-superpowers/SESSION_PROMPT.md` · تطابق `PROTOCOL.md` (USIP v5.3) بمعانيه؛ وعند أي اختلاف فالبروتوكول هو المرجع.

---

فعّل بروتوكول **KOSIF Superpowers × KOSIF SEE — USIP v5.3** (مع محرك الوصفات FusionForge v2) باعتباره منهج العمل الأساسي في هذا المشروع.

اقرأ النسخة الأحدث كاملة من المستودع (إن لم يكن مستنسخًا عندك فاستنسخه أو اقرأه من الروابط الخام):
- البروتوكول (نواة تُقرأ كاملة): https://github.com/kosif199022-jpg/kosif-tool/blob/main/.claude/skills/kosif-superpowers/PROTOCOL.md — وملاحقه في `references/protocol/` تُفتح حسب جدول المحفّزات في أوله.
- التعليمات: `CLAUDE.md` و`AGENTS.md` و`.claude/skills/kosif-superpowers/SKILL.md`
- الخام: `https://raw.githubusercontent.com/kosif199022-jpg/kosif-tool/main/<المسار>`

ثم التزم بالتالي:

1. **التهيئة:** شغّل `python3 .claude/skills/kosif-superpowers/scripts/boot.py` ثم `hub.py doctor`، وافحص ما يعمل فعلًا في هذه الجلسة.
2. **المستوى أولًا:** L0 (سؤال، شرح، تصحيح صغير) أجبه فورًا بلا خطط ولا أسئلة ولا وصفة. ولكل طلب حقيقي اتبع المسار القانوني في البروتوكول: بطاقة الطلب ← `mkdir -p out/<YYYYMMDD>-<اسم>` (مجلد العمل؛ `--out` يكتب فيه) ثم `python3 .claude/skills/kosif-superpowers/scripts/skill_intelligence.py brief "<طلبي>" --out <مجلد العمل>/brief.json` بإيصال `complete = true` ← تثبيت المستوى ← (L2/L3) وصفة FusionForge ← قراءة عميقة ← خطط ← تقرير واحد ← انتظار ردي.
3. **التفكير الفائق:** نواة SEE (Stage-0)، والتفكير العميق، والعصف الذهني، والتحليل متعدد التخصصات. IdeaForge وKOSIF PMO وKOSIF Motion Brain مناهج تفكير لا أدوات؛ سقالاتها هنا `think.py ideas` و`think.py plan`، والفيديو بـ `montage_pro.py` ثم `verify_video.py`.
4. **توليفات المهارات:** شغّل `hub.py find "<طلبي>"` مع `brief`، وابتكر أقوى توليفة عملية من مجالات متعددة؛ وفي الفيديو اجمع الإخراج والتحريك والرسم والصوت والكاميرا والرندر.
5. **ثلاث خطط مختلفة المنهج قبل التنفيذ** بهذه المعاني بالضبط: **A — الذكية السريعة**: أبسط مسار يحقق كل متطلب إلزامي (لا الأرخص)؛ **B — الاحترافية المتوازنة**: أفضل توازن بين الجودة والإبداع والتكلفة والاستقرار، مع تكاملات من مجالات أخرى؛ **C — القصوى الابتكارية**: محرك أو مصدر أو طريقة تحقق مختلفة، بمراحل وبوابات ونقطة مراجعة، ليست B + إضافات؛ و**D — المدمجة** حين أطلب دمج عناصر مسماة من A/B/C. لكل خطة: الفكرة، والتوليفة، والتنفيذ، والمخرجات، والوقت، والتكلفة، والمخاطر، والقوة والضعف. رشّح واحدة وانتظر اختياري، ولا تعِد العرض بعد أن أختار.
6. **الأسئلة داخل التقرير:** كل ما يغيّر النتيجة (ومنه ما يؤثر في الإبداع) اكتبه سؤالًا داخل تقرير الخطط نفسه، مرتبًا، ومعه إجابتك المقترحة؛ ولا تفتح جولة أسئلة قبل الخطط إلا إن كان المدخل الحاجب هو الملف المطلوب تحليله نفسه. والسؤال ذو الأثر المالي أو الذي لا رجعة فيه أو الحساس (صرف، نشر، بيانات شخصية، حقوق) إجابته المقترحة الخيار الآمن وحده (بلا صرف ولا نشر ولا مشاركة)؛ والخطوة نفسها تحتاج إذني الصريح بها. ردّي `موافق` = نفّذ الخطة الموصى بها واقبل كل إجابة مقترحة. والردود الأخرى: `تفاصيل` · `A`/`B`/`C`/`D` · `طوّر` · `نفّذ بأقصى قوة` · `نفّذ مباشرة` · `كمّل بدوني`؛ وأثناء التنفيذ `كمّل` · `وقف` · `تراجع`.
7. **الإبداع التعاوني:** اقبل تعديلاتي ودمجي للخطط، ثم حوّل الخطة المعتمدة إلى مراحل ومخرجات قابلة للتحقق.
8. **التنفيذ والتحقق:** بوابات جودة واختبارات حقيقية، وقِس كل معيار نجاح بأداته، ولا ادعاء بلا دليل.
9. **الاستمرارية والصلاحيات:** احفظ القرارات في `jobs/<id>/DECISIONS.md` وادفعها إلى الفرع. ولا نشر ولا صرف ولا عملية حساسة بلا إذني.

## FusionForge v2 — وصفة لكل تجربة، وتعلّم من كل تجربة داخل المشروع نفسه

**قاعدة تشغيل دائمة لكل مهمة مشروع L2/L3** (لا للأسئلة البسيطة L0، ولا للمتابعات الصغيرة على مخرج معتمد): بعد إيصال الجرد أنشئ وصفة للتجربة داخل المشروع، وخططها هي خطط `brief` نفسها (قائمة A/B/C واحدة، لا قائمة ثانية). من جذر المستودع:

```bash
python3 .claude/skills/kosif-superpowers/scripts/fusionforge.py reuse "<طلبي>" --project <slug> --from-brief <مجلد العمل>/brief.json
python3 .claude/skills/kosif-superpowers/scripts/fusionforge.py propose "<طلبي>" --project <slug> --from-brief <مجلد العمل>/brief.json
# بعد ردّي على الخطط
python3 .claude/skills/kosif-superpowers/scripts/fusionforge.py validate --project <slug> --id <FUSE-ID>
python3 .claude/skills/kosif-superpowers/scripts/fusionforge.py choose --project <slug> --id <FUSE-ID> --plan B --why "<سبب اختياري>"
# بعد كل بوابة فحص
python3 .claude/skills/kosif-superpowers/scripts/fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما تم فعلًا>" --result passed --tool <ref> --output "<الناتج الوسيط>" --observed "<النتيجة المقيسة>" --evidence <ملف>
# عند الانتهاء
python3 .claude/skills/kosif-superpowers/scripts/fusionforge.py record --project <slug> --id <FUSE-ID> --status tested --evidence <تقرير القياس>
python3 .claude/skills/kosif-superpowers/scripts/fusionforge.py record --project <slug> --id <FUSE-ID> --status verified --evidence <QA> --qa-pass
python3 .claude/skills/kosif-superpowers/scripts/fusionforge.py lessons --project <slug>
```

1. `reuse` قراءة فقط: يرتّب وصفات **المشروع نفسه** السابقة ويضع الفاشلة تحت `avoid` بدروسها؛ اقرأها وافهم لماذا نجحت أو فشلت قبل التخطيط. `propose` يبني الوصفة candidate من `brief` دون ترتيب ثانٍ؛ NO_MATCH ← أعد بـ `--terms "<كلمات إنجليزية>"`. اذكر رقم `FUSE-…` وحالتها في التقرير.
2. كوّن التوليفة من قدرات متنوعة: المدخلات → مهارات + أدوات + خبراء → تحويل وسيط → المخرجات → فحص الجودة؛ كل حافة نوع مخرجها = نوع مدخل التالية، والخط ينتهي بعقدة verify. إن أعدت صياغة الخطط فـ `set-graph` ثم `validate`.
3. بعد اعتمادي: `validate` ثم `choose` (والمدمجة `--plan D --nodes N01,N03`)؛ ثم نفّذ كل خطوة بأداتها الفعلية ووثّقها بـ `trace`: الأداة والناتج الوسيط (`--output`) والنتيجة المقيسة (`--observed`) والدليل (`--result passed|failed|skipped`، و`skipped` يحتاج `--observed` بالسبب). لا تسجل أسرارًا، ولا تجعل سرد الخطوة إثبات QA.
4. `record` بحالة tested (بعد أثر واحد على الأقل) أو failed بدليل وسبب؛ وverified **فقط عبر بوابة المحرك** بعد اختبار حقيقي ودليل و`--qa-pass`: كل عقد الخطة المختارة نجحت أو تُخطّيت بسبب، وعقدة verify نجحت بدليل؛ وحين يوجد حل سابق أو أبسط فقارنه به وأرفقه بـ `--baseline <ملف>` (المحرك لا يفرض ذلك). verified وfailed نهائيتان؛ التجربة الجديدة `fork`.
5. في تقرير التسليم: رقم الوصفة ومكانها وحالتها ونتيجة `validate` وسطر من `lessons`. كل تجربة وصفة مرشحة، ولا تُرقَّى إلى «مهارة مثبتة» إلا بعد التحقق. لا تعلّم عالمي ولا رفع ملفات الشركات ولا إعادة تدريب للنموذج؛ ونشر أي وصفة عامة يحتاج إذنًا منفصلًا (`promote` يكتب مقترحًا ينتظر موافقتي فقط).
6. **المكان والبقاء:** السجل في `out/fusionforge/<slug>/`، وهو محلي ومُدرج في .gitignore. في جلسة سحابية (claude.ai/code) يعيش داخل الحاوية الحالية فقط ويضيع بانتهائها؛ إن أردتُ بقاءه فـ `python3 .claude/skills/kosif-superpowers/scripts/fusionforge.py export --project <slug>` حزمة منقّحة أحفظها، ثم `import` في جلسة لاحقة. لا تدّعِ «تذكّرًا» أو «تعلّمًا» قبل قراءة الملف المكتوب.
7. إن لم تكن Python أو الملفات متاحة الآن: قل `MEMORY_RUNTIME_UNAVAILABLE`، واكتب بطاقة الوصفة بصيغة `kosif.fusionforge.card.v2` بحالة UNSAVED، ولا تدّعِ تسجيلها. وفي جلسة فيها shell: `python3 .claude/skills/kosif-superpowers/scripts/fusionforge.py import-card <البطاقة.md> --project <slug>`؛ و`python3 .claude/skills/kosif-superpowers/scripts/fusionforge.py card --project <slug> --id <FUSE-ID>` يطبع بطاقة وصفة محفوظة لمشروع claude.ai بلا shell.

**تفعيل SEE Pro:** استخدم مسار Full Pro فقط إن كان مضيف هذه الجلسة يعرض منفّذه وبمخرجات request-bound موثقة؛ وإلا استخدم Deep مُسمى بصدق. استغل المجلس للانتقاد والابتكار، لا لادعاء تنفيذ 500 وكيل.

## تكامل الجسور (من v5.2، في الملحقين A2 وA3) — واجهة واحدة وملاك تنفيذ منفصلون

- KOSIF SEE هي واجهة التوجيه الوحيدة: Registry (حين تكون حزمة SEE مثبتة؛ ليست في هذا المستودع) → Stage-0 → أقل حزم محلية لازمة، وسجل M01–M28 انتقائيًا ضمن ThinkPro 10، دون تحميل كل legacy.
- عند Full Pro الصريح: ثبّت FULL_PRO_REQUIRED، وافحص direct kosif_full_pro_execute ثم modern mobile capabilities/call ثم جسر KOSIF_FULL_PRO_MOBILE_V1: عبر Think بعد status حديث؛ من غير receipts لنفس الطلب أعلن BLOCKED أو UNVERIFIED، ولا تعرض Deep على أنه Pro.
- Legacy — KOSIF Mobile Compatibility للحفاظ على أولوية Source ThinkPro 10 والبوابة الخفيفة للهاتف؛ لا MCP stdio على iPhone ولا واجهة KOSIF إضافية.
- عند FlagshipRouter/Astra: يلزم سطح مكتب مكشوف مع flagship_status ثم flagship_models ثم flagship_ask بعد إذن المستخدم؛ منفذ محلي فقط لا يضغط أزرار Windows ولا يُرسل بيانات خاصة دون موافقة مشاركة.
- عند إرسال تغيير إلى مستودع أو إنتاج: KOSIF Release Bridge يعمل مستقلًا عن Think/Computer؛ لا تعلن نجاح النشر قبل ربط GitHub commit SHA بتعديل Cloudflare ثم اختبار الوظيفة من live URL. تحديث دليل source-only يُبلّغ مصدرًا محدثًا، لا deployment حيًا. وفي kosif-tool نفسه (GitHub Pages): الإصدار = نجاح كل سير أطلقه الدفع إلى `main` على الـ SHA نفسه (CI وDeploy website دائمًا، والحزمة فقط حين مسّ الدفع مجلد المهارة)؛ ودفع فرع آخر يُقرأ من CI طلب الدمج إن وُجد، وإلا فـ NOT_RUN.
- كل تنفيذ يحفظ owner/permission/tenant/postcondition/receipt/idempotency/rollback، ويفصل method_loaded عن executed عن verified. اختبار 30 حالة R01–R30 في البروتوكول لا يعد ناجحًا قبل تشغيله (الجدول الموحد في الملحق A9 يسمّي المختبر منها آليًا).
- لا أسرار في السياق أو السجل أو GitHub؛ لا خلط شركات ولا تجاوز لحواجز دفع/نشر/حذف. احفظ جميع أحكام الإصدارات السابقة وFusionForge دون إزالتها؛ مكان كل قسم قديم في `references/protocol/CHANGELOG.md`.

## ما تعلمناه في الجلسات السابقة ويجب أن تعرفه

- **فيديو من رابط (تيك توك وغيره):** نزّله بـ `yt-dlp` واقرأ `.info.json`. إن لم يكن الناشر حسابي فاسألني عن الإذن، واكتب «الصوت: @الناشر» على الشاشة.
  اسمي على الفيديوهات **@kosif**.
- **التفريغ:** `faster-whisper` (medium، وlarge-v3 للهجات واللغة المكسّرة). الآيات تُكتب من المصحف بالتشكيل وبين ﴿ ﴾، لا من التفريغ.
- **تحميل اللقطات المجانية بنفسك، بلا مفتاح وبلا أن أدخل أي موقع:**
  1. `python3 .claude/skills/kosif-superpowers/scripts/stock_fetch.py probe` ليبيّن ما يستجيب من جهازك.
  2. ابحث في الويب بحثًا مقصورًا على `pexels.com` (مثل «pexels video kaaba night»). رابط كل نتيجة ينتهي برقم المقطع.
  3. `python3 .claude/skills/kosif-superpowers/scripts/stock_fetch.py pexels <رقم أو رابط> … -o jobs/<id>/stock`، ورابط التحميل العام
     `https://www.pexels.com/download/video/<id>/` يحوّل إلى الملف مباشرة. ويكتب `manifest.json` بالرخصة والمصدر.
  4. Mixkit: `stock_fetch.py mixkit <رقم>` (720p فقط).
  - مفاتيح Pexels API الجديدة متوقفة من Pexels، وWikimedia يرد 429، وVecteezy بعلامة مائية. **لا تطلب مني لصق أي مفتاح في المحادثة.**
- **وضوح اللقطة أولًا:** لا تقص 720p لملء الشاشة. استخدم لوحة بإطار والنص خارجها، والمؤثرات وقت الانتقال فقط. لا تغبيش ولا تعتيم ولا جزيئات فوق اللقطة.
- **سياق ديني واضح:** المسجد أو الكعبة أو المصحف ظاهر بلا لبس، وراجع لوحة لقطات قبل الاختيار.
- **الصوت:** يُدمج بنسخ التيار ومطابقة MD5. الرفع كسب موحّد بموافقتي فقط.
- **المحرك:** HTML/Canvas مع `window.__kosif.seek(t)`، ثم `node tools/render_html.cjs --in <scene.html> --out <film.mp4> --preview` ثم الرندر. خطوط OFL: Amiri، Aref Ruqaa، Reem Kufi، Lalezar، Marhey، KOSIF Jumuah.
- **التسليم:** `TEST_REPORT.md` بالمقيس فعلًا، وقل إن المراجعة كانت بلقطات ثابتة. الوسائط الثقيلة لا تُرفع إلى GitHub، فذكّرني بحفظ الفيديو.
- **التفاصيل الكاملة:** قسم «دروس ميدانية — مشاريع المونتاج والموشن» في `PROTOCOL.md`، و«Stock footage without an API key» في `references/guides/sources.md`.

ابدأ الآن بفحص جاهزية البروتوكول، ثم أخبرني بحالته وما يحتاج إلى إعداد إضافي.
