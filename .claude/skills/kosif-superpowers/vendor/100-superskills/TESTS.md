# سجل الاختبارات (2026-10-05 و2026-10-06، Windows 11، Python 3.13، ffmpeg 9.0، Edge headless عبر Playwright)

| # | ما اختُبر | الأمر | النتيجة |
|---|---|---|---|
| 1 | فهرسة الأطلس | `python tools/catalog.py` | 15,122 مهارة من 3,691 إضافة؛ 12,914 MIT و2,064 Apache |
| 2 | بناء المئة مهارة | `python tools/build.py` | 100 مجلد SKILL.md + references/sources.md، كل مهارة بـ 8 مصادر مطابقة |
| 3 | أنيميشن 2D كامل | `new_scene.py --ratio 9:16 --dur 6` ثم `capture.py` ثم `encode.py` ثم `qa.py` | 180 إطاراً في 1080×1920، MP4 h264 yuv420p، لوحة تحقق، QA = PASS (المثال في `examples/demo2d/`) |
| 4 | أنيميشن 3D (Three.js) | نفس المسار بـ `--kind 3d --ratio 16:9 --dur 4` | 120 إطاراً في 1920×1080 عبر Edge headless (WebGL + Bloom)، MP4، QA = PASS بعد جعل الإيقاعات نسبية وإضاءة الافتتاح أعلى |
| 5 | باني البرومبت | `prompt_build.py brief.json` | ولّد البرومبت + 3 حالات اختبار + نسختي A/B + أسئلة النقاط العمياء (148 كلمة) |
| 6 | فاحص البرومبت | `prompt_lint.py p1.md --kind task --untrusted` | PASS بدرجة 100/100 |
| 7 | فاحص البرومبت على برومبت رديء | `prompt_lint.py bad.md` | BLOCK بدرجة 20/100: مدخل غير مسوّر، لغة غير محددة، لا صيغة إخراج (كما هو متوقع) |
| 8 | مصنع برومبتات الصور | `image_prompt_forge.py spec.json` | 6 صيغ (Midjourney، Flux، SDXL، ChatGPT، Ideogram، NanoBanana) + تنبيه النص العربي؛ خروج 0 |
| 9 | مخرج برومبتات الفيديو | `video_prompt_forge.py shots.json --platforms veo,sora` | لقطتان × منصتان، قصّ المدة الزائدة إلى حد المنصة؛ خروج 0 |
| 10 | فاحص الإكسل | `xlsx_check.py t.xlsx` على ملف مولّد بـ openpyxl | كشف رقماً كنص (F3)، وقيمة ثابتة وسط عمود صيغ (F5)، وVLOOKUP قديمة؛ REVISE كما هو متوقع |

| 11 | الفهرس العميق | `python tools/deep_index.py` | قرأ نص كل SKILL.md (15,122 مهارة، 15.1 مليون كلمة) في 18.6 دقيقة (1116 ث)؛ وسوم بكثافة الذكر؛ SQLite FTS5 + JSON + `DEEP-INDEX.md` |
| 12 | 101 فحص الوسائط | `probe.py clipA.mp4 --keyframes` | كودك/دقة/fps/إطارات مفتاحية + تحذيرات VFR |
| 13 | 101 قصّ الصمت والإيقاع | `silence_cut.py` و`beat_cuts.py` على صوت مُصنَّع | كشف صمت 1.5 ث وحذفه بهامش؛ BPM 120.8 من نبضات كل 0.5 ث (الصحيح 120) |
| 14 | 101 تجميع EDL | `edl_render.py edl.json --ratios 1:1` | مقطعان + xfade + J-cut + سرعة 1.5× + موسيقى −18 dB + loudnorm بمرورين؛ المدة 4.000 = المتوقعة؛ القياس اللاحق −14.0 LUFS و−2.1 dBTP؛ نسخة 1:1 |
| 15 | 102 خط DaVinci | `resolve_pipeline.py doctor` / `verify` | بلا Resolve: وضع يدوي بخروج 2 (لا ادعاء تنفيذ)؛ verify يقرأ ffprobe |
| 16 | 103 جبهة البرومبت | `prompt_frontier.py p.md --model claude` | اكتشف سقالة التفكير، وأمثلة بآثار تفكير، والصراخ، وترتيب answer قبل reason، وعدّ القيود؛ فئة Gemma 3 تعطي درجة إلزام 2→3 |
| 17 | 103 درع الحقن | `injection_shield.py scan/wrap/check/suite` | فحص مسبق FLAG، تسوير + كناري، كشف الكناري في المخرج (خروج 3)، 20 حالة هجوم |
| 18 | 104 مختبر التقييم | `eval_runner.py score/gate/kappa/bench` | σ، فجوة خصومي 2.8 → ترجيح 0.6/0.4، بوابة انحدار تخرج 3، κ لكل معيار، pass@3/pass^3 |
| 19 | 105 طاقة الحركة والبوابة | `motion_energy.py demo2d.mp4 --ref demo3d.mp4` / `storyboard_gate.py` | كشف 84% شبه ساكن وتجميد 1.8 ث في المثال؛ البوابة أمسكت الوصف المزاجي و11 كلمة وتغطية 18% وغياب الجسم الحامل |
| 20 | 106 الصوت والترجمة | `extract_audio_data.py` + `captions_pages.py` + رندر القالبين | 180 إطار بيانات (16 حزمة)، 3 صفحات ترجمة + SRT/VTT/ASS، وقالب الترجمة بإبراز الكلمة وقالب الصوت التفاعلي صُوّرا وجُمّعا إلى mp4 |
| 21 | 107 النموذج المالي | `model_builder.py` → `xlsx_recalc.py` → `model_audit.py` | 8 أوراق و248 صيغة؛ LibreOffice أعاد الحساب (موجود على الجهاز) بلا أخطاء؛ Checks = OK وBS_check/CF_check صفر في كل الفترات؛ التدقيق PASS بلا أرقام مدفونة |
| 22 | 108 أتمتة إكسل | `lambda_library.py`, `formula_translate.py` | 18 دالة LAMBDA مسمّاة مع Docs؛ الترجمة لفّت ARRAYFORMULA وحذّرت من المراجع الهيكلية وDAY(b−a) وLET في Lark |
| 23 | الفهرس الموحّد | `python tools/advanced_index.py` | درّج 15,122 مهارة بمُدرِّج أدلة v2 (توزيع الجودة 5:533 · 4:3,008 · 3:5,569 · 2:5,999 · 1:13)، و70,662 صفاً (مهارة، وسم) بدرجة مركبة؛ الست بطاقات اليدوية تتقدّم على المُدرِّج؛ view `advanced_skill` وجدول `skill_tag` في SQLite يعملان بالاستعلامات المذكورة في التقرير |
| 24 | ضبط الترتيب | `python tools/advanced_index.py --from-cache` | إعادة الترتيب من البطاقات المخبّأة بلا قراءة الأطلس؛ بوابة صلة 3/k أزالت الدخلاء (zoom-sdk، markitdown) من قوائم الوسوم |

## ما لم يُختبر هنا (قل «not-executed» حتى يُشغَّل)
- السكربتات داخل claude.ai أو ChatGPT (المهارات هناك منهجيات؛ السكربتات تحتاج بيئة تنفيذ).
- `resolve_pipeline.py` ضد DaVinci Resolve Studio حقيقي (الوضع اليدوي فقط هو المختبر).
- مُدرِّج الأدلة يقيس الملموسية لا صحة المحتوى؛ ملف مفصّل خاطئ قد ينال 4/5.
- `capture.py` على Linux/macOS بلا Edge (المسار البديل: `python -m playwright install chromium`).
- دقة البرومبتات على المولّدات نفسها (Midjourney وVeo…) تحتاج توليداً فعلياً ومراجعة بصرية.

## إعادة التشغيل
```text
python tools/build.py
cd examples/demo2d && python ../../skills/claude-animation-studio/scripts/capture.py --html index.html
```
| 25 | 109 استوديو الرسم: الاختبارات | `cd skills/pixel-studio-painter/scripts` ثم `python -m unittest discover -s tests` | 18/18: الثقوب وeven-odd، وأقواس SVG، والتدرّج الشفاف، والنص العربي، وترتيب الرسم، واستيراد SVG، والتتبّع (شعار وصورة)، والمطابقة التامة (صفر بيكسل مختلف)، وكود PIL بدقته الأصلية مطابقاً لناتجه، والكود المعطوب يُرجع الخطأ الحقيقي |
| 26 | 109 النافذة الحية | `studio.py --image` و`--code` و`dragon_girl` مع لقطات للنافذة أثناء الرسم | مشهد الفتاة والتنين 15.3 ث (4.97 مليون بيكسل)؛ شعار في الوضع المطابق 6.3 ث و«✅ مطابقة للأصل 100%»؛ صورة 1254×1254 مطابقة؛ كود PIL في 25 خطوة بترتيب الكود |
