# أطلس مناهج كتب الرسم — Drawing Methods Atlas

ملخص أصلي لطرق التعليم في أشهر كتب الرسم، ومنها 41 كتابًا من مكتبة المستخدم نفسه قُرئت في 2026-10-23، مربوط بأداة تنفيذية ترسم وتفحص. الهدف أن يعرف Claude **كيف يفكر الرسام** قبل أن يرسم شخصية أو وجهًا أو جسمًا أو شكلًا، سواء رسم بالكود (SVG) أو كتب برومبت لنموذج صور.

An original summary of how the best-known drawing books teach, including 41 books from the user's own library read on 2026-10-23, tied to a tool that draws and checks. It gives Claude the artist's order of thinking before it draws a character, face, figure or shape, whether in code (SVG) or as a prompt for an image model.

السجل: [`data/drawing_methods_atlas.json`](../data/drawing_methods_atlas.json) · الأداة: `scripts/drawing_methods.py` · الاختبار: `evals/test_drawing_methods.py` · الأكاديمية الأم: [A14](protocol/A14-drawing-cinematic-academy.md) · العودة للبروتوكول: [PROTOCOL.md](../PROTOCOL.md)

## الفهرس / contents

1. [حدود الصدق / honesty limits](#حدود-الصدق--honesty-limits)
2. [ترتيب التفكير عند الرسم / the drawing pipeline](#ترتيب-التفكير-عند-الرسم--the-drawing-pipeline)
3. [الكتب والمناهج / books and their methods](#الكتب-والمناهج--books-and-their-methods)
4. [مكتبة المستخدم / the user's library](#مكتبة-المستخدم--the-users-library)
5. [الأوامر / commands](#الأوامر--commands)
6. [كيف يرسم Claude فعليًا / how Claude actually draws](#كيف-يرسم-claude-فعليًا--how-claude-actually-draws)
7. [ما يفحصه check / what check measures](#ما-يفحصه-check--what-check-measures)

## حدود الصدق / honesty limits

- كل بطاقة (DM-01…DM-48) **إعادة صياغة أصلية** بكلماتنا؛ لم يُنسخ نص أو صفحة أو رسم من أي كتاب ولا يُوزَّع شيء منها. حقل `review_status` يقول لكل بطاقة كم قُرئ فعلًا:
  - `user_copy_read_paraphrased`: قُرئت نسخة المستخدم في 2026-10-23 (طبقة النص، أو OCR، أو صفحات عينة مرسومة لكتب الصور) ثم أُعيدت صياغة الطريقة. هذا لا يعني دراسة كل صفحة سطرًا بسطر، وبعض الكتب كان OCR فيها مشوّهًا (مذكور في الجدول).
  - `general_teaching_knowledge`: طريقة معروفة ارتبطت بالكتاب دون قراءة نصه هنا.
- الكتب مرقّمة بمعرّفات فهرس الـ200 (`data/creative_books_200_index.json`، مثل ART-021)، ومكتبة المستخدم `UBK-01…UBK-41` (العنوان والمؤلف وطريقة القراءة فقط، مع `index_id` إن كان الكتاب في الفهرس)، وما عدا ذلك `EXT-…` ببيانات ببليوغرافية فقط.
- هذا **ليس تدريبًا لأوزان النموذج** ولا دليل احتراف. الدليل الوحيد على الجودة هو رسم فعلي يُفحص مقابل بنود `checks` في البطاقات، ثم مراجعة بصرية.
- عند كتابة برومبت صور: اذكر **الطريقة** (لغة أشكال، خط فعل، ضوء دافئ وظل بارد) لا أسماء فنانين أحياء، ولا تنسخ رسوم كتب.

Each card restates a method in original words; no book text, page or illustration is copied or redistributed. `review_status` says per card whether the user's own copy was read on 2026-10-23 (text layer, OCR or rendered sample pages) or the card rests on widely taught knowledge only. This is not model training and not proof of mastery: only drawings checked against the cards' `checks`, then reviewed visually, show quality.

## ترتيب التفكير عند الرسم / the drawing pipeline

| المرحلة | ماذا تفعل | البطاقات |
|---|---|---|
| intent النية | ماذا يحكي الرسم ولمن | DM-22, DM-23 |
| thumbnail المصغرات | 3–6 تكوينات صغيرة بثلاث قيم | DM-21, DM-22 |
| gesture الإيماءة | خط الفعل والإيقاع وخط التوازن والشد قبل أي تفصيل | DM-06, DM-29, DM-30 |
| construction البناء | كتل ثلاثية الأبعاد ونسب ومنظور ورأس الأنمي والأفق والمدن والنبات والمنتجات | DM-03, DM-04, DM-05, DM-07, DM-08, DM-09, DM-31, DM-34, DM-37, DM-38, DM-39, DM-42 |
| design التصميم | لغة الأشكال والسيلويت والمبالغة وأنماط الأنمي والشعر ورموز الكرتون والمخلوقات | DM-13, DM-14, DM-15, DM-35, DM-40, DM-43, DM-46 |
| line الخط | أوزان خط، تهشير وتنقيط، ملمس الرصاص، التراكب والخط الواثق | DM-24, DM-33, DM-47, DM-48 |
| value/colour الضوء واللون | عائلة ضوء وعائلة ظل، ظل ساقط مبني، بشرة الأنمي، رصاص واقعي | DM-19, DM-20, DM-21, DM-32, DM-36, DM-44 |
| motion الحركة الزمنية | انضغاط وتمدد وتحضير، توقيت وتباعد وأقواس، مشي وجري (للتحريك فقط) | DM-27, DM-28, DM-45 |
| verify التحقق | اقلب الصورة، صغّرها، افحص السيلويت والنسب، وراجع بنظام التمرين | DM-02, DM-14, DM-41 |

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
| التحريك | Thomas & Johnston (ART-093)، Richard Williams (ART-092)، Stanchfield (ART-097) | كيس الدقيق يحفظ حجمه، تحضير عكسي، أجزاء تتوقف في أوقات مختلفة؛ تباعد متقارب عند الأطراف وأقواس | DM-27, DM-28 |
| الحركة للأمام | Loomis (ART-021)، Debt-Free Art Degree (UBK-37) | أعلى الجسم يسبق قاعدته، القدم الدافعة خلف خط التوازن | DM-29 |
| ارسم الفعل | Stanchfield (ART-097/098) | الجانب المشدود مستقيم والمنضغط منحنٍ، شريط مطاطي بين الأطراف | DM-30 |
| الأشخاص في العمق | Loomis، Brehm (UBK-13) | الأفق يقطع كل الأشخاص المتماثلين عند النقطة نفسها | DM-31 |
| الظل الساقط | David Brody (UBK-04)، Kistler (ART-009) | قدم المصباح نقطة تلاشي الظلال؛ تقاطع شعاعين | DM-32 |
| التهشير | Brody، Borgman (UBK-03)، Brehm، Gair (UBK-41) | القيمة من كثافة العلامات؛ ترجمة 3–5 درجات رمادي إلى حبر | DM-33 |
| رأس الأنمي والشعر | Ozawa (UBK-02)، Sketching Manga-Style (UBK-10)، Studio Hard (UBK-26) | خطا التقاطع يقرران التصميم؛ الشعر كتلة ثم خصلات، والجاذبية تشد الأطراف | DM-34, DM-35 |
| تلوين الأنمي | كتاب البشرة اليابانية (UBK-22)، ImagineFX (UBK-21) | ظل أكثر تشبعًا يميل للأحمر ثم للبنفسجي، بلا أسود | DM-36 |
| المدن | Brehm (UBK-13)، Gair | خطوط إعداد ثم ظلال مضخّمة عند حافتها | DM-37 |
| النبات | How to Draw Flowers (UBK-20)، Baid (UBK-40) | أشكال بسيطة ثم حواف ثم عروق ثم تظليل يتبع السطح | DM-38 |
| المنتجات والسيارات | Robertson (ART-047) | مساقط ثم صندوق منظور؛ المحور الأصغر للقطع الناقص على المحور | DM-39 |
| رموز الكرتون | Franklin Bishop — *The Cartoonist's Bible* (UBK-15) | خطوط سرعة واهتزاز واختصارات تعبير | DM-40 |
| التمرين | Scobey (UBK-31)، Lemon (UBK-08)، Date Naoto (UBK-30)، Hammond (UBK-05) | عشر دقائق يوميًا، أيام ملاحظة وأيام ذاكرة، شبكة للنقل | DM-41 |
| البناء للمبتدئ | Kistler (ART-008/009)، Baid، Big Book of Drawing Animals (UBK-11) | مخطط، تشكيل، مسح، تظليل، ظل ساقط | DM-42 |
| أنماط الأنمي | Ozawa، Date Naoto | SD وعادي وبطولي؛ هوية ثابتة من العين والشعر والنسبة والملابس | DM-43 |
| الرصاص الواقعي | Lee Hammond (UBK-05)، Karen Reed (UBK-19) | الشكل أولًا، دمج بطبقات، إضاءة بالممحاة | DM-44 |
| المشي والجري | Richard Williams (ART-092)، Thomas & Johnston | تلامس، هبوط، عبور، صعود؛ الذراعان عكس الساقين | DM-45 |
| المخلوقات والألعاب | Lee Dae-hoon — *Game Creature Design* (UBK-36) | عشرات السيلويتات ثم هيكل معقول ثم تجسيد خامة خامة | DM-46 |
| ملمس الرصاص | Trudy Friend (UBK-34)، Hammond، Borgman | ضربة عريضة، ضع وادفع واسحب، تعرج لأوراق الشجر | DM-47 |
| التراكب والخط الواثق | Tom Fox (UBK-25)، Bert Dodson (UBK-17)، Stanchfield | خطوط أقل وأوثق؛ التراكب يصنع العمق؛ فحص الخط الأوسط والسيلويت | DM-48 |

## مكتبة المستخدم / the user's library

41 كتابًا من مجلد المستخدم قُرئت في 2026-10-23. لا يُحفظ من أي كتاب إلا العنوان والمؤلف وعدد الصفحات وطريقة القراءة (`user_library` في السجل)؛ النصوص والصور لا تُنسخ ولا تُرفع. «صفحات عينة» تعني كتبًا مصوّرة بلا نص كافٍ، فُهمت طريقتها من صفحات مرسومة مختارة.

Forty-one books from the user's folder, read on 2026-10-23. Only title, author, page count and how it was read are stored (`user_library`); no text or image is copied or uploaded. "Sample pages" means a picture book whose method was read from selected rendered pages.

| المعرّف | الكتاب | صفحات | القراءة | البطاقات |
|---|---|---|---|---|
| UBK-01 | *Figure Drawing for All It's Worth* — Andrew Loomis (ART-021) | 198 | OCR | DM-07, DM-09, DM-12, DM-19, DM-29, DM-31, DM-40 |
| UBK-02 | *How to Draw Anime & Game Characters Vol. 1* — Tadashi Ozawa | 155 | OCR | DM-07, DM-10, DM-11, DM-15, DM-16, DM-34, DM-35, DM-43 |
| UBK-03 | *Pen & Pencil Drawing Techniques* — Harry Borgman | 220 | OCR جزئي + صفحات | DM-20, DM-33, DM-44, DM-47 |
| UBK-04 | *How to Draw (The Great Courses, 36 lectures)* — David Brody | 676 | نص | DM-19, DM-20, DM-22, DM-31, DM-32, DM-33, DM-39 |
| UBK-05 | *Lee Hammond's Big Book of Drawing* — Lee Hammond | 208 | OCR | DM-25, DM-41, DM-44, DM-47 |
| UBK-06 | *Draw and Color Sea Creatures* — Russell Farrell (Walter Foster) | 42 | OCR | DM-42 |
| UBK-07 | *The Animator's Survival Kit* — Richard Williams (ART-092) | 346 | OCR | DM-14, DM-17, DM-27, DM-28, DM-45 |
| UBK-08 | *Fearless Drawing* — Kerry Lemon | 131 | نص | DM-33, DM-41, DM-47 |
| UBK-09 | *You Can Draw in Just 30 Minutes* — Mark Kistler (ART-009) | 405 | نص | DM-32, DM-42 |
| UBK-10 | *How to Draw Manga: Sketching Manga-Style Vol. 3 — Unforgettable Characters* — Kazuaki Morita et al. | 184 | نص | DM-14, DM-34, DM-36, DM-43 |
| UBK-11 | *Big Book of Drawing Animals* — Rodriguez & Beaudenon | 194 | صفحات عينة | DM-25, DM-42 |
| UBK-12 | *You Can Draw in 30 Days* — Mark Kistler (ART-008) | 257 | OCR | DM-03, DM-42 |
| UBK-13 | *Draw Buildings and Cities in 15 Minutes* — Matthew Brehm | 201 | نص | DM-31, DM-32, DM-33, DM-37 |
| UBK-14 | *Cartoons: Drawing Funny* — not printed in the pages read | 162 | OCR | DM-26, DM-40 |
| UBK-15 | *The Cartoonist's Bible* — Franklin Bishop | 195 | نص | DM-16, DM-17, DM-25, DM-27, DM-40 |
| UBK-16 | *How to Draw Cool Stuff: The 5-Minute Workbook* — Catherine V. Holmes | 287 | OCR | DM-42 |
| UBK-17 | *Keys to Drawing* — Bert Dodson (ART-004) | 226 | OCR | DM-01, DM-02, DM-04, DM-19, DM-48 |
| UBK-18 | *The Illusion of Life: Disney Animation* — Frank Thomas & Ollie Johnston (ART-093) | 546 | نص | DM-14, DM-15, DM-16, DM-17, DM-27, DM-28, DM-45 |
| UBK-19 | *Sketching People: Basics of Drawing the Human* — Karen Reed | 74 | نص | DM-44 |
| UBK-20 | *How to Draw Flowers and Plants* — unknown (workbook) | 133 | نص | DM-38 |
| UBK-21 | *Ultimate Guide to Manga Art (2022)* — ImagineFX (anthology) | 134 | نص | DM-21, DM-24, DM-34, DM-35, DM-36, DM-46 |
| UBK-22 | *How to Paint Realistic Skin of a Beautiful Girl* — Japanese anthology (machine translation) | 148 | نص | DM-36 |
| UBK-23 | *How to Draw Clothing for Manga* — unknown (Japanese) | 348 | نص | DM-11, DM-32 |
| UBK-24 | *Cartoons Drawing Worksheets* — howtodrawforkids.com | 216 | صفحات عينة | DM-42 |
| UBK-25 | *Anatomy for Artists: Drawing Form & Pose* — Tom Fox | 297 | OCR | DM-04, DM-08, DM-09, DM-10, DM-48 |
| UBK-26 | *How to Draw Hairstyles for Manga* — Studio Hard Deluxe | 391 | نص | DM-35 |
| UBK-27 | *How to Draw Animals: A Visual Reference Guide to Sketching 100 Animals* — Japanese anatomist | 178 | نص | DM-25 |
| UBK-28 | *Anime Academy: How to Draw Manga* — unknown | 134 | OCR | DM-07, DM-08, DM-11, DM-19, DM-21, DM-22, DM-34, DM-35, DM-36, DM-43 |
| UBK-29 | *Drawn to Life Vol. 1 (Portuguese translation)* — Walt Stanchfield (ART-097) | 493 | نص | DM-06, DM-12, DM-14, DM-18, DM-27, DM-29, DM-30, DM-45, DM-48 |
| UBK-30 | *A Comprehensive 13-Week Art Course (65 daily lessons)* — Date Naoto | 194 | نص | DM-07, DM-21, DM-22, DM-24, DM-34, DM-36, DM-41, DM-43 |
| UBK-31 | *365 Days of Drawing* — Lorna Scobey | 322 | نص | DM-01, DM-02, DM-21, DM-41 |
| UBK-32 | *How to Draw Disney Characters for Kids* — unknown | 234 | صفحات عينة | DM-42 |
| UBK-33 | *Point Character Drawing Vol. 2 (Chinese edition)* — Taco | 223 | OCR | DM-07, DM-10, DM-12, DM-34, DM-35 |
| UBK-34 | *Drawing: The Complete Question Handbook* — Trudy Friend | 131 | OCR | DM-01, DM-32, DM-47 |
| UBK-35 | *Drawn to Life Vol. 2 (Chinese edition)* — Walt Stanchfield (ART-098) | 346 | OCR | DM-15, DM-30, DM-48 |
| UBK-36 | *Game Creature Design (Chinese edition)* — Lee Dae-hoon | 276 | OCR | DM-46 |
| UBK-37 | *Debt-Free Art Degree: Foundations in Drawing* — Quarry Books | 332 | نص | DM-02, DM-09, DM-12, DM-19, DM-29, DM-30 |
| UBK-38 | *Human Anatomy for Artists* — Xiao Weichun | 328 | نص | DM-04, DM-08, DM-09, DM-35, DM-39, DM-46 |
| UBK-39 | *How to Draw (Portuguese edition)* — Scott Robertson & Thomas Bertling (ART-047) | 211 | نص | DM-03, DM-04, DM-24, DM-37, DM-39 |
| UBK-40 | *How to Draw: Easy Techniques and Step-by-Step* — Aaria Baid | 374 | نص | DM-38, DM-40, DM-42 |
| UBK-41 | *How to Draw Anything* — Angela Gair | 168 | OCR | DM-02, DM-22, DM-33, DM-37, DM-38, DM-41 |

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
python3 scripts/drawing_methods.py draw bounce --frames 13 --bounce-height 0.55 --out out/bounce.svg   # كرة تنط: أقواس وتباعد وانضغاط
python3 scripts/drawing_methods.py draw shadow --light-x 0.15 --light-height 0.4 --out out/shadow.svg   # ظل ساقط مبني من مصباح
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
| bounce | every drawing keeps the ball's area within 3%; spacing near the apex smaller than near contact; the contact frame is squashed and touches the ground; stretched frames near contact | DM-27, DM-28 |
| shadow | every shadow point lies on both its ground ray (from the light's foot) and its light ray within 1 px; the light stands over its foot; a cast-shadow shape exists | DM-32, DM-19 |

These are geometric and structural checks only. They do not judge beauty, likeness or professional quality.
