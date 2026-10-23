# أطلس مناهج كتب الرسم — Drawing Methods Atlas

ملخص أصلي لطرق التعليم في أشهر كتب الرسم، مربوط بأداة تنفيذية ترسم وتفحص. الهدف أن يعرف Claude **كيف يفكر الرسام** قبل أن يرسم شخصية أو وجهًا أو جسمًا أو شكلًا، سواء رسم بالكود (SVG) أو كتب برومبت لنموذج صور.

An original summary of how the best-known drawing books teach, tied to a tool that draws and checks. It gives Claude the artist's order of thinking before it draws a character, face, figure or shape, whether in code (SVG) or as a prompt for an image model.

السجل: [`data/drawing_methods_atlas.json`](../data/drawing_methods_atlas.json) · الأداة: `scripts/drawing_methods.py` · الاختبار: `evals/test_drawing_methods.py` · الأكاديمية الأم: [A14](protocol/A14-drawing-cinematic-academy.md) · العودة للبروتوكول: [PROTOCOL.md](../PROTOCOL.md)

## الفهرس / contents

1. [حدود الصدق / honesty limits](#حدود-الصدق--honesty-limits)
2. [ترتيب التفكير عند الرسم / the drawing pipeline](#ترتيب-التفكير-عند-الرسم--the-drawing-pipeline)
3. [الكتب والمناهج / books and their methods](#الكتب-والمناهج--books-and-their-methods)
4. [الأوامر / commands](#الأوامر--commands)
5. [كيف يرسم Claude فعليًا / how Claude actually draws](#كيف-يرسم-claude-فعليًا--how-claude-actually-draws)
6. [ما يفحصه check / what check measures](#ما-يفحصه-check--what-check-measures)

## حدود الصدق / honesty limits

- كل بطاقة (DM-01…DM-26) **إعادة صياغة أصلية** لطريقة تعليم معروفة ارتبطت بالكتاب؛ لم يُنسخ نص أو صفحة أو رسم من أي كتاب، ولم تُقرأ النصوص الكاملة للكتب الحديثة في هذه الجلسة. حقل `review_status` يقول ذلك صراحة لكل بطاقة.
- الكتب مرقّمة بمعرّفات فهرس الـ200 (`data/creative_books_200_index.json`، مثل ART-021)، وما ليس فيه له معرّف `EXT-…` ببيانات ببليوغرافية فقط.
- هذا **ليس تدريبًا لأوزان النموذج** ولا دليل احتراف. الدليل الوحيد على الجودة هو رسم فعلي يُفحص مقابل بنود `checks` في البطاقات، ثم مراجعة بصرية.
- عند كتابة برومبت صور: اذكر **الطريقة** (لغة أشكال، خط فعل، ضوء دافئ وظل بارد) لا أسماء فنانين أحياء، ولا تنسخ رسوم كتب.

Each card restates a widely taught method in original words; no book text, page or illustration is copied and the full texts of modern books were not read here (`review_status` says so per card). This is not model training and not proof of mastery: only drawings checked against the cards' `checks`, then reviewed visually, show quality.

## ترتيب التفكير عند الرسم / the drawing pipeline

| المرحلة | ماذا تفعل | البطاقات |
|---|---|---|
| intent النية | ماذا يحكي الرسم ولمن | DM-22, DM-23 |
| thumbnail المصغرات | 3–6 تكوينات صغيرة بثلاث قيم | DM-21, DM-22 |
| gesture الإيماءة | خط الفعل والإيقاع قبل أي تفصيل | DM-06 |
| construction البناء | كتل ثلاثية الأبعاد ونسب ومنظور | DM-03, DM-04, DM-05, DM-07, DM-08, DM-09 |
| design التصميم | لغة الأشكال والسيلويت والمبالغة | DM-13, DM-14, DM-15 |
| line الخط | أوزان خط تفصل القريب عن البعيد | DM-24 |
| value/colour الضوء واللون | عائلة ضوء وعائلة ظل وحرارة لون | DM-19, DM-20, DM-21 |
| verify التحقق | اقلب الصورة، صغّرها، افحص السيلويت والنسب | DM-02, DM-14 |

القاعدة الذهبية المشتركة بين الكتب كلها: **من العام إلى الخاص** — الحركة ثم الكتلة ثم الحافة ثم التفصيل ثم الضوء، ولا تفصيل قبل أن تقرأ الوضعية من الظل الخارجي.

The rule all these books share: general to specific — action, then mass, then edge, then detail, then light; no detail before the pose reads in silhouette.

## الكتب والمناهج / books and their methods

| المجال | الكتب الأشهر (المعرّف) | الطريقة المستخلصة | البطاقة |
|---|---|---|---|
| الملاحظة | Betty Edwards — *Drawing on the Right Side of the Brain* (ART-001)، Kimon Nicolaides — *The Natural Way to Draw* (ART-006) | ارسم ما تراه لا الرمز الذهني؛ الخط الكفافي البطيء والفراغ السالب | DM-01 |
| القياس | Bert Dodson — *Keys to Drawing* (ART-004) | وحدة قياس واحدة وخطوط شاقول | DM-02 |
| البناء | E. G. Lutz (ART-010)، Scott Robertson — *How to Draw* (ART-047) | كل شيء كرات وعلب وأسطوانات؛ قطوع تتسع بعيدًا عن مستوى العين | DM-03, DM-04 |
| المنظور | Storey (ART-055)، Norling (ART-046)، Mateu-Mestre — *Framed Perspective* (ART-049) | الأفق = عين المشاهد؛ نقاط التلاشي تصنع إحساس اللقطة | DM-05 |
| الإيماءة | Nicolaides، Mike Mattesi — *FORCE* (ART-038)، Walt Stanchfield — *Drawn to Life* (ART-097)، Glenn Vilppu (EXT-004) | خط فعل واحد منحنٍ، مستقيم مقابل منحنى | DM-06 |
| النسب | Andrew Loomis — *Figure Drawing for All It's Worth* (ART-021)، Jack Hamm (ART-086) | الجسم بوحدة الرأس: 8 بطولي، 7.5 واقعي، 3 طفل كرتوني | DM-07 |
| المانيكان | Michael Hampton — *Figure Drawing: Design and Invention* (ART-030)، George Bridgman — *Constructive Anatomy* (ART-027) | قفص صدري وحوض صلبان ووسط مرن (الفاصوليا)، كتل متعاشقة | DM-08 |
| الرأس | Loomis — *Drawing the Head and Hands* (ART-022)، Hogarth (ART-044) | كرة بمستويين جانبيين وفك؛ الوجه أثلاث؛ العينان في منتصف الرأس | DM-09 |
| اليدان | Bridgman — *The Book of a Hundred Hands* (ART-029)، Hogarth — *Drawing Dynamic Hands* (ART-042) | كف علبة، إبهام كتلة مستقلة، مفاصل على أقواس | DM-10 |
| القماش | Hogarth — *Dynamic Wrinkles and Drapery* (ART-043) | تصنيف الطيات (أنبوبية، حلزونية، نصف قفل، متعرجة، متساقطة…) حسب نقاط الارتكاز والشد | DM-11 |
| الاتزان | Loomis، Robert Beverly Hale (ART-013) | خط الجاذبية فوق القدم الحاملة؛ كتف وحوض متعاكسان | DM-12 |
| تصميم الشخصيات | Tom Bancroft — *Creating Characters with Personality* (EXT-001)، Molly Bang — *Picture This* (ART-091)، Jack Hamm (ART-085) | لغة الأشكال: دائرة لطف، مربع ثبات، مثلث خطر؛ تنويع الأحجام | DM-13 |
| السيلويت والجاذبية | Thomas & Johnston — *The Illusion of Life* (ART-093)، Richard Williams (ART-092) | الشخصية تُقرأ من الظل الأسود وحده؛ مبالغة مقصودة في سمة واحدة | DM-14, DM-15 |
| التعبير | Gary Faigin (EXT-003)، Preston Blair (ART-094) | حاجب + جفن + فم يتفقون على عاطفة واحدة | DM-16 |
| الكرتون | Preston Blair — *Cartoon Animation* (ART-094) | كرات مرنة تحفظ حجمها عند الانضغاط والتمدد | DM-17 |
| ثبات الشخصية | Eric Goldberg (ART-095)، Bancroft — *Character Mentor* (EXT-002) | ورقة تدوير على خطوط أفقية مشتركة ولوحة ألوان مثبتة | DM-18 |
| الضوء | Robertson — *How to Render* (ART-048)، James Gurney — *Color and Light* (ART-061) | خط انتهاء واضح، ظل ذاتي وملقى، ضوء منعكس خافت | DM-19 |
| القيم | Arthur Wesley Dow — *Composition* (ART-071)، Harold Speed (ART-012) | نوتان: 3 قيم في كتل كبيرة، أعلى تباين عند نقطة التركيز | DM-20 |
| اللون | Gurney (ART-061/063)، Josef Albers (ART-069)، Itten (ART-073) | ضوء دافئ وظل بارد؛ لوحة محدودة بأدوار | DM-21 |
| التكوين | Mateu-Mestre — *Framed Ink* (ART-081)، Bruce Block — *The Visual Story* (ART-100) | مصغرات، نقطة تركيز واحدة، خطوط قائدة | DM-22, DM-23 |
| التحبير | Guptill — *Rendering in Pen and Ink* (ART-059)، Gary Martin (ART-088) | خط خارجي أسمك، داخلي أنحف، نهايات مستدقة | DM-24 |
| الحيوانات | Ken Hultgren (ART-084)، Jack Hamm — *How to Draw Animals* (ART-087) | العمود الفقري وكتلتا الصدر والحوض، الكعب المرتفع | DM-25 |
| السرد المصور | Scott McCloud — *Understanding Comics* (ART-089) | الإغلاق بين اللوحات، أنواع الانتقال، خط المحور | DM-26 |

## الأوامر / commands

Typed from the skill folder (`.claude/skills/kosif-superpowers/`):

```bash
python3 scripts/drawing_methods.py list --domain character            # البطاقات حسب المجال
python3 scripts/drawing_methods.py find "ارسم وش شخصية بتضحك"          # أنسب البطاقات للطلب
python3 scripts/drawing_methods.py show --id DM-09                     # بطاقة كاملة
python3 scripts/drawing_methods.py plan "ارسم شخصية كرتونية طفل سعيد"  # خطة من النية إلى التحقق
python3 scripts/drawing_methods.py prompt "a brave girl explorer" --methods DM-13,DM-16   # برومبت صور بلا استدعاء نموذج
python3 scripts/drawing_methods.py draw head --yaw 30 --pitch -10 --out out/head.svg
python3 scripts/drawing_methods.py draw figure --heads 8 --pose contrapposto --out out/figure.svg   # stand|contrapposto|walk|action
python3 scripts/drawing_methods.py draw character --shape triangle --age adult --expression angry --out out/villain.svg
python3 scripts/drawing_methods.py draw forms --eye-level 0.45 --out out/forms.svg
python3 scripts/drawing_methods.py check --svg out/villain.svg         # يخرج 1 عند فشل أي بند
python3 -m unittest discover -s evals -p 'test_drawing_methods.py' -v
```

`draw` writes four groups: `stage-guide` (head units, eye level), `stage-construction` (line of action, ball and planes, rib cage and pelvis, joints, landmarks), `stage-final` (the drawing) and `stage-silhouette` (a solid-black thumbnail inset). Every element is plain SVG with `data-part` names, so a later step can recolour, animate or hand it to `creative_paint.py`, `unified_draw.py` or the motion pipeline. Output is deterministic and never overwrites without `--force`.

## كيف يرسم Claude فعليًا / how Claude actually draws

1. **حلّل الطلب:** `plan` يعطي البطاقات والمراحل وبنود الفحص؛ اكتب النية في سطر (مَن الشخصية؟ ماذا تشعر؟ أين؟).
2. **ابدأ من هيكل حقيقي:** `draw` للرأس أو الجسم أو الشخصية يعطي بناءً صحيح النسب؛ عدّل عليه أو اكتب SVG خاصًا بنفس الترتيب (guide → construction → final).
3. **للمشاهد المتحركة:** شخصيات `code_drawing_master.py` و`character_fullbody.py` تتبع نفس القواعد (خط فعل، كتل، مفاصل)؛ استعمل البطاقات لاختيار الوضعيات والتعابير.
4. **لنموذج صور:** `prompt` يجمع مصطلحات البطاقات المختارة ويعطي بنود مراجعة؛ لا يُصرف رصيد ولا يُستدعى نموذج من هنا، والتوليد خطوة منفصلة بموافقة.
5. **افحص قبل التسليم:** `check` ثم ارسم PNG وانظر إليه فعليًا (اقلب الصورة أفقيًا، صغّرها لحجم أيقونة)؛ لا تقل «رسمت باحتراف» من نجاح الفحص الهندسي وحده.

Plan with `plan`, start from a correct structure with `draw`, keep the stage order when writing your own SVG, reuse the cards when posing `code_drawing_master.py` or `character_fullbody.py` actors, build image prompts with `prompt` (no model is called), then `check` and look at a rendered PNG before delivery.

## ما يفحصه check / what check measures

| kind | checks | card |
|---|---|---|
| all | the four stage groups exist and are not empty | DM-03 |
| head | face thirds equal within 10%; eye line at half the full head height; hairline → brow → nose → chin in screen order | DM-09 |
| figure | measured heads-tall within 0.2 of the plan; pelvis near the midpoint (canon ≥ 7); neck over the support foot within 0.3 head; rib cage and pelvis tilt in opposite directions; a line of action exists | DM-06, DM-07, DM-12 |
| character | dominant shape on head/body; a contrasting secondary shape on hands/feet; heads-tall matches the age; brows, eyes and mouth carry one emotion | DM-13, DM-15, DM-16 |
| forms | ellipse openness (ry/rx) grows with distance from eye level; one declared light | DM-04, DM-19 |

These are geometric and structural checks only. They do not judge beauty, likeness or professional quality.
