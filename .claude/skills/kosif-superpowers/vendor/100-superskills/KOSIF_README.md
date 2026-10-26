# 100 Super Skills داخل KOSIF Superpowers

مستودعك [`kosif199022-jpg/100-superskills`](https://github.com/kosif199022-jpg/100-superskills) (رخصة MIT) منسوخ هنا كاملًا: **114 مهارة** في 10 مجالات، 682 ملفًا، منها 143 سكربتًا. قبل كده كان سوبر باور بيستشهد بـ 72 مهارة منها كمراجع لبطاقات القدرات بس، و42 مهارة ماكانتش موجودة خالص. وبعدها PR #153 ربط المستودع كـ Git submodule مع فهرس `data/100-superskills-index.json` وأداة `superskills_bridge.py`، بس جلسات Claude السحابية بتستنسخ المستودع من غير submodules، فالملفات ماكانتش بتوصل. النسخة دي بتحط الملفات نفسها في نفس المسار، فالفهرس والجسر بتوع #153 شغالين زي ما هم. دلوقتي كل مهارة موجودة بمنهجها وسكربتاتها واختباراتها، ويقدر Claude يلاقيها من الباب الأمامي.

The owner's repository is copied here whole: 114 skills in 10 domains, 682 files, 143 scripts. Before this, Superpowers cited 72 of them only as evidence for power cards and did not have the other 42 at all.

## الاستخدام / Use

من فولدر المهارة `.claude/skills/kosif-superpowers/`:

```bash
python3 scripts/hub.py find "عايز نموذج مالي في إكسل"          # الباب الأمامي بيعرض المهارات الخارقة المناسبة كمان
python3 scripts/superskills.py find "تايبوغرافي عربي متحرك"      # ترتيب الـ114 مهارة للطلب
python3 scripts/superskills.py list                              # كلها حسب المجال
python3 scripts/superskills.py show kosif-mimic --full           # المنهج كامل والسكربتات والاختبارات والمصادر
python3 scripts/superskills.py install genius-council-decision   # نسخها في ~/.claude/skills
python3 scripts/superskills.py verify                            # كل ملف مطابق لبصمته
python3 scripts/superskills.py selftest                          # اختبارات المهارات نفسها في نسخة مؤقتة
```

بعد ما تلاقي المهارة: اقرأ `skills/<slug>/SKILL.md` ونفّذ منهجها. السكربتات بتتشغل من فولدر المهارة نفسه زي ما الـ SKILL.md بيقول.

## المجالات / Domains

| المجال | العدد |
|---|---|
| الحركة والأنيميشن (motion) | 8 |
| الصورة والفيديو والسينما (image-video) | 17 |
| البرومبتات والذكاء الاصطناعي (prompts-ai) | 10 |
| أدوات Office والبيانات (office-data) | 15 |
| تصميم المواقع والبرمجة (web-code) | 25 |
| الكتابة والصوت والأعمال والتعليم والقرار (business) | 25 |
| الدفعة المتقدمة جدًا (ultra) | 8 |
| استوديو الرسم بالبيكسل (pixel) | 1 |
| استوديو HyperFrames (hyperframes) | 1 |
| مهارات KOSIF الأساسية: kosif-one وkosif-social وkosif-mimic وkosif-montage-motion (kosif-core) | 4 |

## ما اتنسخ وما فضل برّه / What was copied

- كل الملفات النصية لحد 1 ميجا، والملفات الثنائية الصغيرة لحد 500 كيلو (خطوط OFL ومؤثرات صوتية وصور).
- 9 ملفات وسائط كبيرة فضلت في المستودع الأصلي (فيديو الأمثلة، صورتين PNG كبار، نموذج tessdata العربي، ملفات WAV للأمثلة). كل مهارة بتقول اللي ناقصها في `left_upstream` داخل `KOSIF_INTEGRATION.json`، وتتجاب من GitHub لو احتجتها.
- الملفات مش قابلة للتنفيذ، وKOSIF مابيشغلش منها حاجة لوحده غير اختبارات المهارات تحت `selftest`، وفي نسخة مؤقتة.
- `vendor/` بيتساب برّه ملف claude.ai المضغوط زي باقي المجموعات المنسوخة، فهناك بيوصل الفهرس والوصف بس.

## تعديلات KOSIF / KOSIF patches

خمس تعديلات صغيرة علشان المهارات تشتغل في مكانها الجديد، ومتسجلة في `kosif_patches` وبتتطبق تاني مع كل `sync`:

1. `kosif-one/scripts/plan.py`: بيلاقي المهارات اللي جنبه في الفولدر ده بدل مسار سطح المكتب على ويندوز بس.
2. `kosif-one/scripts/plan.py`: المهارة اللي مش متثبتة في `~/.claude/skills` بس موجودة جنبه بتتحسب موجودة ومعاها مسارها.
3. `kosif-one/tests/test_plan.py`: فحص المهارات المثبتة بيقبل الفولدر المجاور، والمهارات اللي من حزم تانية (ultra-motion-montage وmotion-os) بتتعدّى لو مش موجودة.
4. `pixel-studio-painter/scripts/tests/test_studio.py`: اختبارات Motion محتاجة فولدر `scripts/motion/` اللي الحزمة الأصلية ماشحنتهوش، فبتتعدّى بالسبب ده بدل 5 أخطاء.
5. `kosif-montage-motion/scripts/ffprobe_shim.py`: ffmpeg 6 ومابعده مابيطبعش عدد الإطارات في التمرير بالنسخ، فكان `nb_frames` ناقص. بقى يعدّ بفك الترميز لو احتاج.

## الإثبات / Evidence (2026-10-26)

- `verify`: 682 من 682 ملف مطابقين.
- `selftest`: كل فولدرات الاختبار الست للأربع مهارات اللي فيها اختبارات نجحت، 215 اختبار (pixel-studio-painter 43، kosif-montage-motion 8+112+31، kosif-one 10، kosif-social 11). محتاجة ffmpeg وopencv-python-headless وscipy وpillow وnumpy.
- 115 من 129 سكربت بايثون بيردّوا على `--help`. الباقي محتاج ملف دخل أو playwright أو matplotlib، أو هو موديول مشهد مش أمر.
- اختبار المستودع: `evals/test_superskills.py`.

للتحديث من المستودع الأصلي: `git clone https://github.com/kosif199022-jpg/100-superskills ../100-superskills` ثم `python3 scripts/superskills.py sync --src ../100-superskills`.
