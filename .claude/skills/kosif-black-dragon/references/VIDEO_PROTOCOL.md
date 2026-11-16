# بروتوكول التنين الأسود الإلزامي لأي منتج فيديو (الإصدار ٢)

**القاعدة:** أي طلب فيه فيديو (ريل، إعلان، برومو، مونتاج، موشن، فيلم، انترو، شورتس) بيمشي في **مسار واحد بسبع مراحل بنفس الترتيب**، و**كل مرحلة ليها مهارات أساسية من التنين الأسود لازم تشتغل فعلًا قبلها**. مفيش مرحلة تتخطى، ومفيش مهارة تتقال إنها "اتستخدمت" من غير إيصال تشغيل، ومفيش تسليم قبل ما `check` يعدّي (exit 0).

الأداة: `.claude/skills/kosif-black-dragon/scripts/video_protocol.py`.

- `core <id> --job J -- <args>` بيشغّل المهارة الأساسية بجد، ويحفظ اللوج وإيصال مختوم (الأمر، كود الخروج، بصمة اللوج). المهارة اللي تخرج بفشل (زي هوك ضعيف) **مش بتتحسب**.
- `record` و`color` بيرفضوا أي مرحلة لحد ما مهاراتها الأساسية كلها يبقى ليها إيصال ناجح.
- مهارة تبع مرحلة جاية مينفعش تشتغل بدري، عشان الترتيب يفضل واحد.
- `check` بيراجع كل الختوم والإيصالات واللوجات، وبيرفض لو أي حاجة ناقصة أو اتعدلت.

## المراحل والمهارات الإلزامية

| # | المرحلة | المهارات الأساسية الإلزامية (لازم كلها، و"أو" = واحدة منهم تكفي) | الحقول |
|---|---|---|---|
| 1 | `brief` بطاقة الطلب | `mind-think` عقل التنين **+** `tool-matrix` مصفوفة الأدوات | goal, audience, platform, aspect, duration_s, message, hero |
| 2 | `concept` الفكرة | `matrices` المصفوفات اللانهائية **+** `style-atlas` أطلس الـ٨٦ أسلوب **+** `reel-hooks` تقييم الهوك (لازم ميطلعش WEAK) | idea, metaphor, hook (+ emotion اختياري) |
| 3 | `color-design` تحليل الألوان | مدمج: قياس ٦٠/٣٠/١٠ ولون تمييز واحد على البطل | يتقاس من البكسلات |
| 4 | `shots` خطة اللقطات | `motion-repos` مستودعات الموشن **+** (`web-film-plan` أو `montage-options` أو `kmx-recipe` أو `shadow-check`) | shots[].duration_s, what, accent_on |
| 5 | `produce` الإنتاج | محرك رندر واحد على الأقل: `web-film-render` أو `motion-director` أو `motion-runtime` أو `montage-build` أو `cinema-run` أو `kmx-experiment` أو `shadow-render` | outputs, tool, paid, spend_approved |
| 6 | `qa-color` الفحص | (`media-verify` بوابة التسليم أو `web-film-check`) **+** فحص الألوان على الناتج الحقيقي | يتقاس من البكسلات |
| 7 | `deliver` التسليم | `check` بيطلع قايمة `cores_used` تلقائي | summary, executed, not_executed |

## خريطة المهارات الأساسية (اللي البروتوكول بيشغّلها)

| المعرّف | البرنامج | بيعمل إيه |
|---|---|---|
| `mind-think` | `kosif-dragon-mind/scripts/dragon_mind.py think` | عقل التنين: ٢٦ ملكة، ست مراحل تفكير، ١٢٠ إطار من الكتب، وفجوات صريحة |
| `tool-matrix` | `kosif-superpowers/scripts/hub.py find` | مصفوفة الأدوات: ٢١٠ أداة (١٩٣ جاهزة على الجهاز ده) + كتالوج ٥٨٠٠+ قدرة، مرتبة للمهمة |
| `matrices` | `kosif-infinite-matrices/scripts/kmx.py ideate` | أنظمة بصرية وحركية جديدة من طوب سببي (حالة، عملية، قانون، زمن، ذاكرة، تغذية راجعة) من ٨٦ أسلوب |
| `kmx-recipe` / `kmx-experiment` | `kmx.py recipe validate` / `kmx.py experiment --render --mp4` | وصفة المصفوفات وتجربة A/B/C برندر حقيقي |
| `style-atlas` | `kosif-superpowers/scripts/style_atlas_bridge.py` | أطلس الأساليب الـ٨٦: `search`، أو `plan` لدمج ٨٥/١٥ |
| `reel-hooks` | `kosif-reel-hooks/scripts/reel_tools.py hook` | تقييم الهوك؛ لو WEAK بيخرج بفشل والمرحلة متتقفلش |
| `motion-repos` | `video_protocol.py repos` | ترتيب ٢٥ محرك موشن (three.js, GSAP, Remotion, Lottie, Manim, motion-canvas ...) + ٢٥ مصدر + مستودعاتك (kosif-one, fastify-motion-bro, kosif-studio ...) للمهمة، مع ملاحظة الترخيص |
| `web-film-plan` / `web-film-render` / `web-film-check` | `kosif-web-film/scripts/web_film.py` + `tools/render_html.cjs` | فيلم الويب (التنين الأسود): خطة ← HTML بـ seek(t) ← MP4، وفحص البنية |
| `montage-options` / `montage-build` | `kosif-superpowers/scripts/montage_pro.py` | فريق مونتاج برو (١٣ دور) على مادة مرفوعة |
| `motion-director` | `kosif-superpowers/scripts/motion_director.py` | سكريبت متوقت على الصوت ← أنيميشن SVG ← MP4 |
| `motion-runtime` | `kosif-superpowers/scripts/motion_runtime.py` | فيلم SVG أصلي + رندر |
| `cinema-run` | `kosif-superpowers/scripts/cinematic_pro_conductor.py run` | سينما برو: من المادة للرندر بفحص مستقل |
| `shadow-check` / `shadow-render` | `kosif-shadow-theatre/scripts/shadow_theatre.py` | مسرح الظل |
| `media-verify` | `kosif-superpowers/scripts/verify_video.py` | بوابة التسليم: كودك، مقاس، فريمات، مدة، صوت، loudness |

اعرض الجدول ده من الأداة نفسها: `python3 $T cores` (أو `--stage shots`).

## قاعدة الألوان (اللون العاشر)

من تحليل ريلزين يوسف رحاب: البوستر بيبقى شيك بلونين، بس الهوية بتيجي من **لون تالت واحد (~١٠٪) بيتحط على البطل**.

- **لون أساسي ~٦٠٪ + لون مساعد ~٣٠٪ + لون تمييز ~١٠٪.** اللون التمييزي على البطل والكلمة المفتاحية بس.
- تلات طرق تختار بيها (`--rule`):
  - `contrast`: عايز الحاجة تتشاف؟ لوّنها بعكس لون خلفيتها.
  - `emotion`: اختار لون إحساسه هو نفسه فكرتك (غضب = أحمر، قوة/طاقة = برتقالي، جيمنج = أخضر نيون، فخامة = موف ...). محتاج `emotion` في الفكرة، أو `--accent`.
  - `neon`: ألوانك مطفية؟ ضيف نيون.
- في فيلم الويب: حط اللون المختار في `visual_language.palette` = `[خلفية، نص، لون التمييز]` قبل `scaffold`.

**شروط النجاح:** في التصميم، فرق اللون (ΔE) بين التمييزي والخلفية ≥ ٤٠. وفي الفحص، الملف لازم يكون نفس ملف الإنتاج، وفيه لون تمييز نسبته بين ٠٫٥٪ و١٨٪، وبيبان (ΔE ≥ ٤٠)، ومن نفس عيلة اللون المخطط (فرق الدرجة ≤ ٢٠° وΔE ≤ ٤٥).

## مثال كامل (اتجرب فعلًا: ريل قهوة ٨ ثواني)

```bash
T=.claude/skills/kosif-black-dragon/scripts/video_protocol.py
J=out/black-dragon/demo-coffee
TASK="ريل ٨ ثواني لمنتج قهوة: فنجان واحد يصحّيك"

python3 $T start "$TASK" --job $J
# 1 brief
python3 $T core mind-think  --job $J -- "$TASK" --out $J/mind
python3 $T core tool-matrix --job $J -- "$TASK" --limit 6
python3 $T record brief --job $J --data brief.json
# 2 concept
python3 $T core matrices    --job $J -- --count 3
python3 $T core style-atlas --job $J -- search "warm product glow"
python3 $T core reel-hooks  --job $J -- hook --hook "إنت لسه نايم وعينك مفتوحة؟ فنجان واحد ٨ الصبح يصحّيك" --screen "٣ ساعات نوم؟"
python3 $T record concept --job $J --data concept.json
# 3 color
python3 $T color color-design keyframe.png --job $J --rule emotion
# 4 shots
python3 $T core motion-repos  --job $J -- "$TASK kinetic typography"
python3 $T core web-film-plan --job $J -- "$TASK" --out $J/film.plan.json --duration 8 --ratio 9:16
python3 $T record shots --job $J --data shots.json
# 5 produce (بعد scaffold بالباليت)
python3 $T core web-film-render --job $J -- --in $J/film.html --out $J/final.mp4 --mode seek --offline --aspect 9:16
python3 $T record produce --job $J --data produce.json
# 6 qa
python3 $T core media-verify --job $J -- $J/final.mp4 --aspect 9:16 --fps 30 --duration 8 --no-audio
python3 $T color qa-color $J/final.mp4 --job $J
# 7 deliver
python3 $T record deliver --job $J --data deliver.json
python3 $T check --job $J      # exit 0 = يتسلم، exit 5 = مينفعش يتسلم
```

في التجربة دي الهوك الأول ("فنجان واحد يصحّيك") أخد ٣٠ من ١٠٠ (WEAK)، فالبروتوكول رفض يقفل مرحلة الفكرة لحد ما اتكتب هوك أقوى أخد ٨٠٫١. والفحص الأخير: ٨/٨ في بوابة التسليم، واللون البرتقالي المخطط ظهر في الناتج بفرق درجة ٠٫٥° بس.

## حدود صريحة

- الأداة بتثبت إن المهارات اشتغلت وخرجت بنجاح، وبتقيس الألوان والترتيب، لكنها **مش بتحكم على جودة الفكرة أو الإخراج**. ده لسه شغل العين والمراجعة.
- أدوات محتاجة حاجات مش متسطبة على الجهاز (Blender، opencv، Remotion) بتفضل اختيارية جوه مجموعة "أو". الجهاز ده فيه ١٩٣ من ٢١٠ أداة جاهزة (`hub.py doctor`).
- مفيش صرف كريدت، ولا نشر، ولا رفع، ولا تسطيب من غير موافقة صريحة. أداة مدفوعة في الإنتاج لازم `spend_approved: true`.
- الختم فحص محلي إن محدش عدّل حاجة بعد تسجيلها، مش توقيع خارجي.

## إضافة محركات ريل ١٢ أداة (2026-11-12)

أصبح للتنين الأسود مساحة مستقلة لتجهيز Remotion وHyperFrames وMotion Canvas وThree.js وManim وRough.js وGSAP وAnime.js وMo.js وWhisperX وAuto-Editor وFFmpeg:

`.claude/skills/kosif-black-dragon/integrations/instagram-video-12/README.md`

الأداة `toolchain.py` توفر `plan` لاختيار البرامج، `doctor` للتحقق من وجود التبعيات فعليًا، `install --all --yes` لتنزيلها على جهاز التشغيل بموافقة، و`run` لتنفيذ CLI متاح. لا يتغير ترتيب المراحل السبعة ولا شروط `core` و`check` القديمة. وجود تبعية في registry أو نجاح `doctor` لا يعتبر إيصال رندر ولا يثبت جودة الفيديو. يُراعى هامش سكتات الكلام في `auto-editor` وترخيص Remotion.
