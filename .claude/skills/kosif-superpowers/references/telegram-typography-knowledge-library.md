# KOSIF Typography Knowledge Library — مكتبة الإلهام الطباعي

**الهدف:** يبحث Claude وKOSIF Superpowers في مكتبة الخطوط والأفكار الطباعية المستخرجة من صادرات Telegram الخاصة بالمستخدم، ليختار خطوطًا ويقترح اتجاهات تصميم عربية ولاتينية. لا تُنشر الخطوط نفسها، ولا الصور، ولا الرسائل، ولا المسارات المحلية.

- **الفهرس العام (آمن للنشر):** `data/telegram-typography-catalog-complete-20261020.json` (المخطط `kosif.telegram-typography-index.v3`)
- **المحرك:** `scripts/telegram_typography_atlas.py`، بالأوامر `find` و`doctor` و`refresh` و`scan` و`enrich-zips`. الاختبارات في `scripts/test_telegram_typography_atlas.py`.
- **ملف المواقع الخاص:** يبقى على جهاز المستخدم فقط، وفيه المسارات الحقيقية ومواقع الملفات داخل ZIP. **لا ترفعه إلى GitHub، ولا تكتب مساره في رد عام.** ضعه في مجلد خاص بحسابك مثل `%LOCALAPPDATA%\KOSIF\typography-private\`. لا تضعه في `C:\Users\Public`، فهذا المجلد يقرؤه كل حساب على الجهاز.

## نتائج الجرد (2026-10-20، بعد `refresh`)

| البند | العدد |
|---|---|
| مجلدات التصدير · الملفات · الرسائل المقروءة | 4 · 4,370 · 2,766 (من 4 ملفات HTML) |
| ملفات خطوط مباشرة TTF/OTF ← المختلف منها بالبصمة | 1,269 ← 1,246 |
| أرشيفات ZIP · إدخالات خطوط داخلها ← جديد مختلف · مكرر | 89 · 5,283 ← 4,268 · 1,015 |
| **خطوط مختلفة بالبصمة SHA-256 (الإجمالي)** | **5,514** |
| تدعم العربية (20 حرفًا أساسيًا على الأقل) · تدعم اللاتينية | 4,634 · 3,932 |
| أسماء عائلات مختلفة (بلا تمييز حالة الأحرف) · أزواج عائلة/وزن | 2,412 · 4,058 |
| حالة الرخصة من بيانات الخط نفسه | 1,066 OFL مُدّعاة · 3 Apache · 11 GPL · 534 مقيدة أو تحتاج مراجعة (منها 402 تقول أسماؤها Trial أو Demo أو Personal Use أو Unlicensed) · 3,864 بلا دليل · 36 لم تُحلل |
| معتمد لإعادة التوزيع | **0**: الحقل `redistribution_approved=false` لكل خط |
| الصور | 2,981 صورة قُرئت أبعادها فقط، و80 عينة رُئيت مرة واحدة بشكل خاص |

5,514 هو عدد **ملفات خطوط مختلفة**، لا عدد عائلات مستقلة: «Somar Rounded» وحدها لها 270 ملفًا. البحث يجمع النتائج في صف واحد لكل عائلة.

## تعليمات إلزامية لـClaude عند أي طلب متعلق بالخطوط

1. افهم الاستخدام: بوستر، شعار، هوية، نص طويل، خط عربي أصلي، بطاقات، واجهة، موشن جرافيك، عنوان 3D، خط أطفال أو تصميم دعائي.
2. ابحث في الفهرس قبل الاختيار، وبالعربي أو الإنجليزي. البحث يفهم كلمات الأنماط بأي إملاء (كوفي، رقعة/رقعه/الرقعة، ديواني، ثلث، نسخ، نستعليق، أطفال، شعار، مقروء…) وأسماء مثل DecoTypeThuluthII، ويضع اسم العائلة المطابق تمامًا أولًا، ويعيد صفًا واحدًا لكل عائلة مع أوزانها وعدد نسخها وحالة رخصتها. `--latin` يبقي الخطوط التي تغطي اللاتينية أيضًا.
3. قارن 5–20 مرشحًا، واعتبرها **مراجع إلهام أو اقتراحات اختيار**، لا تصاريح استخدام أو تعديل أو نسخ لحدود الحروف.
4. قدّم ثلاثة مسارات: حل سريع مقروء بخط رخصته مؤكدة، وحل احترافي يقيس المرشحات ويقارنها، وحل تجريبي بحروف أصلية من الصفر.
5. للتنفيذ استعمل **خطًا تأكدت رخصته من مصدره الرسمي**، أو اصنع حروفًا أصلية من الصفر. ملفات الخطوط على جهاز المستخدم: للرندر في جلسة سحابية حمّل الخط المفتوح من مصدره الرسمي، أو اعمل على الجهاز عبر Remote Desktop Commander بإذن المستخدم.
6. راجع وصل الحروف العربية والأرقام والتشكيل وGSUB وGPOS وRTL وأحجام الهاتف وتباين الخلفية. قِس بـ `font_fidelity_lab.py`، وقارن بصريًا بـ `render_text.cjs`.
7. اختبر القراءة بالمقاسات 16 و24 و48 و96، عربيًا ولاتينيًا، وسجّل الخط المختار ومصدر رخصته وأسباب الاختيار. للتحريك أو التجسيم انتقل إلى KOSIF Motion أو Blender أو Timeline.
8. **رخص name table مثل OFL أو Apache تلميح، لا تصريح قانوني.** فلتر `--license open` يضيّق المرشحات فقط؛ التأكيد من المصدر واجب قبل أي تسليم.

## أوامر جاهزة

من مجلد المهارة `.claude/skills/kosif-superpowers/`:

```bash
python3 scripts/telegram_typography_atlas.py doctor                      # أي الأوامر تعمل هنا (find وrefresh لا يحتاجان مكتبات)
python3 scripts/telegram_typography_atlas.py find --index data/telegram-typography-catalog-complete-20261020.json "خط رقعة" --arabic-only --limit 15
python3 scripts/telegram_typography_atlas.py find --index data/telegram-typography-catalog-complete-20261020.json "kufi logo" --arabic-only --latin --license open   # شعار ثنائي اللغة
python3 scripts/telegram_typography_atlas.py find --index data/telegram-typography-catalog-complete-20261020.json "Cairo"
python3 scripts/telegram_typography_atlas.py refresh --index data/telegram-typography-catalog-complete-20261020.json --out ./refreshed.json
```

إعادة الفحص على جهاز المستخدم فقط. المخرجات ملفات جديدة خارج مجلد التصدير. الأمر يرفض أن يكتب فوق ملف موجود، ويرفض أن يضع ملف المواقع الخاص داخل أي مستودع git. `enrich-zips` يعمل على فحص جديد فقط، لا على فهرس أُثري من قبل.

في cmd:

```cmd
mkdir "%LOCALAPPDATA%\KOSIF\typography-private"
python scripts\telegram_typography_atlas.py scan --root "C:\Users\USERNAME\Downloads\Telegram Desktop" --public-out NEW-public.json --private-out "%LOCALAPPDATA%\KOSIF\typography-private\private-new.json"
python scripts\telegram_typography_atlas.py enrich-zips --root "C:\Users\USERNAME\Downloads\Telegram Desktop" --public NEW-public.json --private "%LOCALAPPDATA%\KOSIF\typography-private\private-new.json" --new-public NEW-complete.json --new-private "%LOCALAPPDATA%\KOSIF\typography-private\private-complete.json"
python scripts\telegram_typography_atlas.py refresh --index NEW-complete.json --out NEW-final.json
```

في PowerShell:

```powershell
$P = "$env:LOCALAPPDATA\KOSIF\typography-private"; New-Item -ItemType Directory -Force $P | Out-Null
python scripts\telegram_typography_atlas.py scan --root "$env:USERPROFILE\Downloads\Telegram Desktop" --public-out NEW-public.json --private-out "$P\private-new.json"
python scripts\telegram_typography_atlas.py enrich-zips --root "$env:USERPROFILE\Downloads\Telegram Desktop" --public NEW-public.json --private "$P\private-new.json" --new-public NEW-complete.json --new-private "$P\private-complete.json"
```

`scan` يحتاج beautifulsoup4 وfonttools وPillow. الخطوط بصيغة WOFF2 داخل ZIP تحتاج أيضًا brotli، ويثبتها `pip install fonttools[woff]`.

## 16 اتجاهًا تصميميًا (من الفهرس)

كل اتجاه في الفهرس معه حتى 12 خطًا مرتبطًا من عائلات مختلفة، تتقدمها الخطوط ذات الرخص المفتوحة المُدّعاة والأغنى بالحروف العربية. يُعاد بناء هذه القائمة على كل الخطوط، بما فيها خطوط ZIP.

| المعرّف | الاتجاه | فكرة تطبيقية أصلية |
|---|---|---|
| kufi-grid | شبكة كوفية هندسية | وحدات مربعة متساوية مع فراغ سلبي، وحروف تُبنى من الصفر |
| naskh-editorial | نسخ للتحرير | عناوين ونصوص طويلة مقروءة بتوازن جيد للتشكيل والوصل |
| ruqah-personal | رقعة شخصية | إيقاع قلم سريع لدعوات وهوية غير رسمية |
| diwani-ceremony | ديواني فاخر | حروف زخرفية متداخلة لشهادات وتغليف فاخر |
| thuluth-poster | ثلث للبوسترات | صعودات طويلة وتراكيب تراثية |
| arabic-latin-pair | تزاوج عربي لاتيني | خطوط تغطي النظامين، مع مواءمة الارتفاعات والأوزان والأرقام |
| geometric-logo | شعار هندسي | بناء حروف متفردة دون تتبّع خط آخر |
| bold-sale | خط دعائي عريض | أرقام أسعار واضحة وتباين وزن للموبايل |
| calligraphy-motion | الخط المتحرك | كشف الحروف بترتيب الرسم مع حفظ الوصل وتوقيت RTL |
| decorative-ornament | زخرفة حروف | وحدات زخرفية أصلية متكررة |
| brush-doodle | قلم حر وفرشاة | ملمس حبر وحركة قلم أصلية |
| 3d-glyph | حروف مجسمة | بروز وحواف وإضاءة Blender لحروف مسموح بها |
| display-editorial | عناوين تحريرية | عنوان عربي قوي مع متن مقروء |
| light-product | خط رفيع للمنتجات | ملصقات رقيقة مقروءة بتباين WCAG |
| identity-system | نظام هوية طباعية | نظام أحجام ومسافات قابل لإعادة الاستخدام |
| kids-rounded | خط أطفال دائري | حروف واسعة دائرية وفراغات داخلية كبيرة |

## أمثلة للدمج داخل KOSIF

- **بوستر عرض سعودي:** ابحث `"بوستر" --arabic-only`، ثم قارن نمطين للعناوين والأرقام. صمّم العناصر في Creative Paint أو Unified Draw، ثم قِس الخط بـ font-fidelity-lab.
- **لوحة موشن 9:16:** اختر خطًا يدويًا برخصة مؤكدة، أو صمّم مسارات حروف أصلية، واربطها بتوقيت كلمات **مقاس فعلًا** في Motion؛ لا تستنتج التوقيت من شدة الصوت وحدها.
- **خط عربي أصلي:** اكتب موجزًا لكل حرف وأشكال اتصاله، ثم ابنه بـ FontForge أو Fontra، وتحقق بـ fontTools وHarfBuzz، وأخرج عينات حروف وكلمات وأرقام، وسجّل حقوق النسخة الجديدة.

## الحدود وحقوق النشر

يحتوي الفهرس العام على:
- أسماء العائلات والأوزان من بيانات OpenType، بعد حذف الروابط (بما فيها t.me والنطاقات بلا https) و@الحسابات والبريد والأرقام منها؛
- تغطية العربية واللاتينية؛
- تلميحات الرخص؛
- أوصاف إبداعية مجردة؛
- عدّاد موضوعات الرسائل.

**لا يحتوي على** أي خط قابل للتحميل، ولا صورة، ولا رسالة، ولا اسم مرسل، ولا رابط تيليجرام، ولا مسار محلي.

**وجود خط في الصادرات لا يعني أنه مجاني أو قابل للنسخ أو لإعادة التوزيع.**

ما لم يُفحص:
- محتوى كل الصور؛
- ملفات PDF وRAR والأرشيفات المتداخلة؛
- خطوط EOT (118) وملفات .glyphs (8) داخل ZIP؛
- أرشيف ZIP واحد تعذرت قراءته، و36 خطًا داخل ZIP لم يُحلل.

لذلك لا يجوز وصف الفحص بأنه استوعب كل البيانات.

عدّاد موضوعات الرسائل جاء من الفحص الأصلي على الجهاز بأداة وسوم قديمة كانت تطابق أجزاء الكلمات، فقد يزيد عن الواقع؛ إعادة `scan` تعيد حسابه. أما `refresh` فيعيد اشتقاق ما يحدده الفهرس العام وحده:
- الوسوم بالكلمة الكاملة؛
- علامات الرخص من الأسماء؛
- الاتجاهات والأعداد؛
- الحدود.

انظر أيضًا: references/font-matching.md وreferences/font-innovation-50.md وscripts/font_fidelity_lab.py.
