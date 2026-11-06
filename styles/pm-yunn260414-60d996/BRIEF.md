# شرح مبسط لـ Git بثمانية فصول ومخططات وطرفية — What is Git explainer

> فيديو شرح طويل (نحو 6 دقائق و48 ثانية) يعرّف المبتدئين بـ Git بالصينية على خلفية كحلية متدرجة: مجلد يمتلئ بنسخ ملف مكررة، تعارض بين شخصين، تشبيه حفظ الألعاب، بطاقة تعريف بـ Git، شبكة حواسيب موزعة، Git مقابل GitHub كالكاميرا والألبوم، المناطق الثلاث كصورة جماعية بإطارات ملونة، طرفية تكتب الأوامر بجوار بطاقة شرح لكل أمر، خطوط فروع تتشعب وتندمج، مزامنة حاسوب مع مستودع بعيد، ثم جدول أوامر سريع وبطاقة ختام، وترجمة أسفل كل مشهد.
>
> A 6 min 48 s beginner Git explainer in Chinese on a navy gradient: duplicate file copies, a game-save analogy, Git facts, a distributed network, the three areas as coloured frames, a terminal typing each command beside an explainer card, branch lines splitting and merging, remote sync, and a cheat-sheet ending, with a caption under every scene.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/yunn260414-60d996
- التصنيفات / Categories: diagrams, code
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 408 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: Remotion, React, SVG, Web Audio

## الفكرة
الفكرة شرح Git كأنه نظام حفظ للملفات مثل حفظ الألعاب، بتشبيهات يومية واضحة: المناطق الثلاث كمسرح ثم الوقوف أمام الكاميرا ثم الألبوم. ثمانية فصول مرقمة بوسم أحمر صغير في الزاوية، كل فصل يبني مخططاً بسيطاً من بطاقات داكنة بحواف ملونة وإيموجي، والتعليق الصوتي يظهر ترجمة في كبسولة داكنة أسفل الشاشة. الطابع واجهة مطور هادئة: كحلي، أحمر Git، أزرق وأصفر وأخضر للمناطق.

## Concept
The idea is to explain Git as a save system for files, like saving a game, with clear everyday analogies: the three areas as a stage, then standing in front of the camera, then the album. Eight chapters are numbered with a small red tag in the corner, each building a simple diagram from dark cards with coloured borders and emoji, while the narration shows as a caption in a dark pill at the bottom. The look is a calm developer UI: navy, Git red, and blue, yellow and green for the areas.

## المشاهد المقترحة
- 0-34 ث: المشكلة: نافذة سطح مكتب فيها مستند واحد، ثم تتكدس نسخ بأسماء «نهائي» تطول؛ سطر بوجه حائر يسأل أين ذهبت فقرة قديمة؛ وشخصان يعدلان نفس الفصل فيظهر انفجار أحمر «تعارض».
- 34-68 ث: التحكم في النسخ: بطاقة عنوان، ثم ثلاث خانات حفظ لعبة مع ختم «انتهت اللعبة» وسطر استعادة، تقابلها ثلاث نسخ ملف v1 إلى v3 بالمؤلف والوقت.
- 68-113 ث: ما هو Git: شعار Git أحمر بجوار صفوف حقائق (السنة، المبتكر، كُتب في أيام)؛ شبكة ماسية من حواسيب يحمل كل منها التاريخ كاملاً؛ وبطاقتا Git وGitHub بعلامة «لا يساوي» وتشبيه الكاميرا والألبوم.
- 113-170 ث: المناطق الثلاث: إطارات زرقاء للعمل وصفراء للتجهيز وخضراء للمستودع؛ شخصيات تنتقل من المسرح إلى إطار التجهيز، وصورة تستقر في المستودع، وشارات ملفات تنتقل على وسمي add وcommit.
- 170-260 ث: الأوامر الأساسية: طرفية يساراً تكتب كل أمر ومخرجاته سطراً سطراً، وبطاقة يميناً باسم الأمر ومعناه ونصيحة؛ تغطي init وstatus وadd وcommit وlog وdiff وrestore.
- 260-305 ث: الفروع: خط رئيسي أزرق بنقاط حفظ، وفرع ميزة أخضر ينحني جانباً، ومؤشر «أنت هنا» ينتقل بينهما، ثم يندمج الفرع عائداً بعقدة دمج حمراء.
- 305-350 ث: العمل عن بُعد: بطاقة حاسوب وبطاقة مستودع سحابي؛ أسهم متقطعة تتحرك للاستنساخ (تنزيل) والدفع (رفع)، ثم دورة العمل اليومية سحب-تعديل-إضافة-حفظ-دفع كشارات.
- 350-408 ث: الخلاصة: عنوان جدول مرجعي، تدفق المناطق الثلاث، ثم شبكة شارات أوامر بالأحمر والأخضر والبنفسجي؛ وبطاقة ختام بشعار Git ودعوة لحفظ أول مشروع وتلميح للتنزيل.

## Proposed scenes
- 0-34s: The problem: a desktop window shows one document, then copies with ever longer 'final' names pile up; a confused-emoji line asks where an old paragraph went; two people edit the same chapter and a red 'conflict' burst appears.
- 34-68s: Version control: a title card, then three game-save slots with a 'game over' stamp and a reload line, mapped to three file versions v1-v3 with author and time.
- 68-113s: What Git is: a red Git logo beside fact rows (year, creator, written in days); a diamond network of laptops each holding a full history; Git versus GitHub cards with a 'not equal' sign and camera/album analogy.
- 113-170s: Three areas: blue working, yellow staging and green repository frames; figures move from the stage into the staging frame, a photo lands in the repository, and file chips travel along add and commit labels.
- 170-260s: Basic commands: a terminal on the left types each command and its output line by line while a card on the right names the command, its meaning and a tip; covers init, status, add, commit, log, diff and restore.
- 260-305s: Branches: a blue main line with save points, a green feature branch curving off, a 'you are here' marker switching between them, then the branch merging back with a red merge node.
- 305-350s: Remote: a laptop card and a cloud repository card; dashed arrows animate clone (download) and push (upload), then the daily pull-edit-add-commit-push loop as chips.
- 350-408s: Summary: a cheat-sheet title, the three-area flow, then a grid of command chips in red, green and purple; final card with the Git logo, a call to save your first project and a download hint.

## قواعد الحركة
- إيقاع درس: جملة تعليق واحدة لكل ترجمة (نحو 5-12 ثانية)، وكل جملة تضيف عنصراً واحداً إلى المخطط الحالي؛ والمشاهد تتلاشى تقاطعياً بين الخطوات.
- وسم الفصل «n / 08» في كبسولة حمراء صغيرة مع اسم الفصل أعلى اليسار في كل شاشة؛ والترجمات في كبسولة داكنة دائرية في وسط الأسفل.
- اللوحة: تدرج كحلي من #0e1a33 إلى #0a1020، بطاقة #121b30، أحمر Git #f05a3c، أزرق العمل #3b82f6، أصفر التجهيز #f5c542، أخضر المستودع #34d399، بنفسجي البعيد #a78bfa، نص #e6ebf5.
- البطاقات داكنة بحواف ملونة 1-2 بكسل وتوهج ناعم حين تنشط؛ والإيموجي والشخصيات البسيطة تحمل التشبيهات.
- أقسام الطرفية تكتب الأوامر حرفاً حرفاً وتظهر المخرجات بعد توقف قصير؛ مع أسطر فروقات ملونة (أحمر للمحذوف وأخضر للمضاف).
- مخططات الفروع تُرسم خطوطها بضربات متباطئة؛ ووسم «أنت هنا» يقفز بين العقد. (للنسخة العربية: الترجمة والبطاقات من اليمين لليسار، والأوامر تبقى بالإنجليزية من اليسار لليمين.)

## Motion rules
- Lecture pace: one narration sentence per caption (about 5-12 s), and each sentence adds one element to the current diagram; scenes cross-fade between steps.
- Chapter tag 'n / 08' in a small red pill plus chapter name top-left on every screen; captions in a dark rounded pill centred at the bottom.
- Palette: navy gradient #0e1a33 to #0a1020, card #121b30, Git red #f05a3c, working blue #3b82f6, staging yellow #f5c542, repository green #34d399, remote purple #a78bfa, text #e6ebf5.
- Cards are dark with 1-2 px coloured borders and a soft glow when active; emoji and simple figures carry the analogies.
- Terminal sections type commands character by character with output appearing after a short pause; coloured diff lines (red removed, green added).
- Branch diagrams draw their lines on with eased strokes; the 'you are here' tag hops between nodes.

## Facts stated by the source (rewritten in our words)
- The subject is a beginner explainer about what Git is.
- The page tags it as diagrams and music; no duration or stack is stated.

## Assumptions
Observed from 36 frames sampled every ~11.3 s across about 408 s: the problem setup, version-control analogy, Git facts and distribution, the three areas, the terminal command walkthrough, branching, remote sync and the cheat-sheet ending, with Chinese captions. Chapter boundaries are estimated between samples. Assumed: that captions follow a narration voice (an audio track exists but was not listened to); no music content was analysed, so the 'music' tag is unverified.

## Keywords
git explainer, version control, beginner tutorial, terminal, branch diagram, three areas, cheat sheet, narration captions, Chinese, شرح Git, التحكم في النسخ, درس للمبتدئين, طرفية, مخطط الفروع
