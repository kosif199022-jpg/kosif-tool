# A14 — KOSIF Drawing & Cinematic Learning Academy

> **متى تقرأه / when to read:** تعليم Claude الرسم، تحسين جودة التصميم واللقطات، دراسة الكتب، تشريح، منظور، تكوين، إضاءة، مونتاج، تحريك.
>
> **العودة للنواة:** [PROTOCOL.md](../../PROTOCOL.md). هذا ملحق مستقل، ولا يغيّر القواعد الأعلى، ومنها قانون Katana التحليلي فقط في [A8](A8-motion-brain.md).

## هدف الميزة وحالة العمل

**المطلوب ليس فهرس كتب فقط.** المسار: مصدر مشروع ومراجع محددة → استخراج مبدأ قابل للفحص → تمرين أصلي → تنفيذ محرك → قياس بصري مستقل → نقد وإعادة رسم → حفظ درس مشروع ورفع مستواه بناء على أدلة. لا تدّعِ أن جمع أسماء الكتب، أو قراءة مقتطف، يغيّر أوزان Claude أو يثبت تحوّله إلى رسام محترف. «قدرة مبرمجة» ≠ «جودة فنية بشرية معتمدة».

الفهرس المقصود `data/creative_books_200_index.json` يحتوي **100 مرشح للرسم و100 مرشح للمونتاج/التصوير/الإضاءة/الصوت/المؤثرات**. معظمها ببينة ببليوغرافية غير كافية لقول «دُرس المحتوى». `review_status` و`full_text_ingested` و`method_extracted` جزء من الحقيقة الدائمة. لا تُقتبس أو تُنسخ كتب حديثة محمية بلا ترخيص مناسب. تُقرأ النسخ المصرح بها محلياً أو المصادر العامة قانونياً؛ افحص حقوق النشر حسب الدولة والطبعة.

## مراجع أصلية تحققت مبادئها نصياً

| المؤلف/المصدر | مكان المبدأ في النص | فكرة أصلية قابلة للتطبيق | التنفيذ هنا |
|---|---|---|---|
| E. G. Lutz — *What to Draw and How to Draw It* | [Project Gutenberg #74518، INSTRUCTIONS](https://www.gutenberg.org/cache/epub/74518/pg74518-images.html) | تتابع الضربات؛ خطوط إنشاء خفيفة قبل التفاصيل، ثم حذف خطوط المساعدة | `creative_principles.py construct` يولد 4 إطارات SVG لأشكال يحددها المستخدم |
| Harold Speed — *The Practice and Science of Drawing* | [#14264، الفصلان V وIX](https://www.gutenberg.org/cache/epub/14264/pg14264-images.html) | تدريب مستقل على رسم الخط والكتل اللونية؛ تلخيص الضوء والنصف ظل والظل إلى ثلاث كتل | `creative_principles.py values` يقسّم بيانات PGM ذات التدرج الرمادي إلى ثلاث قيم |
| Arthur Wesley Dow — *Composition* | [#45410، الفصل I وNOTAN والفصل XII](https://www.gutenberg.org/cache/epub/45410/pg45410-images.html) | تنظيم الخط والكتل الفاتحة والداكنة واللون، ودراسة نوتان ثنائية/ثلاثية | `values` مع `cut-tones` لقياس اختلاف توزيع الكتل بين الإطارات |

**حد التحليل:** اطلعنا على الفصول/المقاطع الداعمة المذكورة، لا نفترض قراءة وتحليل 200 كتاب بالكامل. ترجمة الفكرة إلى مخطط خوارزمي **تطوير أصلي** لا نقل لشيفرة أو لوحات الكتاب. دليل قيمة التمرين يحتاج صور إنتاج واقعية ومراجع بصرية معتمدة، لا يثبته النجاح البرمجي فقط.

## ثلاث قدرات فعلية داخل KOSIF

1. **C-DRAW-01 — الرسم المتدرج:** `construct` يأخذ ملف JSON بأبعاد `width,height` وقائمة `shapes` (دائرة / مستطيل / خط) ولكل عنصر `stage=guide|mass|outline|detail`. يخرج أربعة ملفات SVG قابلة للفحص: مساعدات الإنشاء، الكتل، المحيط، الصورة النهائية. يمكن تغذيتها إلى Storyboard وMotion Brain بالتتابع. لا يدعي أنه يرسم أي شيء من نص حر وحده.
2. **C-DRAW-02 — درس الضوء والظل:** `values` يأخذ صورة تدرج رمادي `P2` بحد أقصى مليون بكسل ويخرج `PGM` مقسّمًا إلى ثلاث قيم `0,127,255`، مع إحصاءات توزيع السواد ومقياس توازن يمين/يسار. النتيجة قياس هندسي، **وليست حكماً آلياً بالجمال**؛ تحتاج مراجعة بشرية أو رؤيوية منفصلة.
3. **C-MOTION-01 — استمرارية كتل الإضاءة في القطع:** `cut-tones` يقارن توزيعات القيم في لقطات زمنية مأخوذة من التحليل. يرصد تغيرًا كبيرًا ليفتح مراجعة المخرج؛ **القطع المتباين قد يكون مقصودًا**، فلا تمنعه آلياً. لا يشاهد الفيديو ولا يفك ضغطه، ويُغذى ببيانات فعلية من أداة تحليل صور مصرح بها.

### أوامر التشغيل من جذر المستودع

```bash
SK=.claude/skills/kosif-superpowers
python3 "$SK/scripts/drawing_academy.py" index
python3 "$SK/scripts/drawing_academy.py" lesson --id build_shapes --out out/draw-lesson.json
python3 "$SK/scripts/drawing_academy.py" scan-book --book-id lutz-how --input authorized-book.txt --rights own_copy_private --out out/lutz-audit.json
python3 "$SK/scripts/creative_principles.py" construct --input original-shapes.json --out-prefix out/stage
python3 "$SK/scripts/creative_principles.py" values --input gray-reference.pgm --out out/notan.pgm
python3 "$SK/scripts/creative_principles.py" cut-tones --input frame-tone-ratios.json --out out/tonal-cuts.json
python3 -m unittest discover -s "$SK/evals" -p 'test_creative_principles.py' -v
```

تنسيق `original-shapes.json` مثال أصلي لا منقول من كتاب:

```json
{"width":300,"height":300,"shapes":[
  {"kind":"circle","x":150,"y":80,"r":38,"stage":"guide"},
  {"kind":"rect","x":110,"y":118,"w":80,"h":100,"stage":"mass"},
  {"kind":"circle","x":150,"y":80,"r":38,"stage":"outline"},
  {"kind":"line","x1":138,"y1":82,"x2":162,"y2":82,"stage":"detail"}
]}
```

تنسيق `frame-tone-ratios.json` هو قائمة كائنات `[{"time_seconds":0,"tone_ratio":{"0":0.2,"127":0.3,"255":0.5}},...]`، ويجب أن يكون مجموع القيم 1، والأزمنة متزايدة. إذا لم تتوفر العينات الفعلية من الفيديو فلا يصح تقديم التحليل كأنه مراجعة مقطع.

## C-SPACE-01 و C-COLOR-01 — قدرات المصدر العملية

**C-SPACE-01: Two-point perspective.** Original, geometric two-point SVG perspective from user-defined horizon, vanishing points, front edge and receding depths. Every receding edge is generated as a collinear interpolation toward its source vanishing point and checked with numeric tests. Based on public-domain G. A. Storey's discussion of sightline, horizon, and angular perspective: https://www.gutenberg.org/ebooks/20165. This is a constrained 2D schematic, not a general 3D modeler.

**C-COLOR-01: palette contrast analysis.** Input 2–16 distinct hex colors, output hue angle, HSV value/saturation, WCAG relative luminance and pairwise ratios. Influenced by the **principle** of separating hue/value/chroma from A. H. Munsell, https://www.gutenberg.org/ebooks/26054; mathematically **NOT the Munsell system**. Do not claim aesthetic quality or exact Munsell chroma.

    python scripts/perspective_color_lab.py perspective --input perspective-scene.json --out perspective.svg
    python scripts/perspective_color_lab.py palette --input brand-colors.json --out palette.json
    python -m unittest discover -s evals -p test_perspective_color_lab.py -v

Perspective input example: {"width":800,"height":800,"horizon_y":300,"left_vp_x":30,"right_vp_x":760,"front_bottom":[400,650],"front_height":240,"depth_left":0.4,"depth_right":0.5}

Palette input example: {"colors":["#18392E","#F5E5C4","#AC8136"]}

**Verification state as of 22-10-2026:** 7 construction/tonal tests + 7 source-aware academy tests + 8 projection/color tests passed on authorized Windows laptop (22 total). The wider legacy v5.2 fixture-reproduction test had a preexisting hash-parsing drift: manual retention report showed 0 missing v5.2 units, but historic fixture hashes did not reproduce. Do not count this as a clean complete protocol run. Fetching all 8 public-domain source texts to the laptop hit SSL CERTIFICATE_VERIFY_FAILED; TLS checks were not bypassed. Source anchors from verified texts and selected sections are not a full-text review of 200 books.
## حلقة التعليم للفن الإبداعي

**A: مصادر موثوقة** → B: محضر مصادر مع مقاطع/صفحات وحقوق → C: قدرة `method card` أصلية بمدخلات ومخرجات محددة → D: تمارين رسم أو إعداد لقطة → E: معاينة حقيقية وأدلة بصريّة → F: نقد على النسب والتكوين والقيم الضوئية والاتساق عبر الإطارات → G: تحسين ثم مقارنة مسار قديم/جديد وإيصال نتائج. اربط بالمحركات المثبتة، ولا تُسند لها وظيفة خارج نطاقها: `code_drawing_master.py` للشخصيات الأصلية، `unified_draw.py` للرسم الحركي، `montage_pro.py` للمونتاج، `verify_video.py` لفحص MP4. قبل الإدعاء بأن Claude «تعلّم» طبّق تمارين غير موجودة في المصادر، وحكماً مستقلاً، وقارن المخرجات بطريقة عادلة.

**التعلّم المقصود هنا:** ذاكرة معرفة ومهارات قابلة للاستدعاء وتوجيه أدوات وتحسين حلول بناء على قياسات؛ **لا** fine-tuning أو تعديل أوزان النموذج. تقارير حقوق المصدر أو مقاطع الكتب الخاصة تبقى داخل نطاق المستخدم، ولا تُنسخ إلى المكتبة المشتركة أو GitHub دون إذن. طبّق قواعد عزل الشركات ومشاركة FusionForge والبوابات العامة.
