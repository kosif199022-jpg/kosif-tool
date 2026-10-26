# خريطة الدمج — كل المهارات القديمة وأين ذهبت

كل المهارات بقيت في أماكنها (لم يُحذف شيء)، لكن المستخدم يطلب من باب واحد: **kosif-one**.
المهارات المتشابهة اندمجت في «أقسام»؛ كل قسم له مهارة رئيسية وأدلة مساعدة.

## 1. التحميل والمواد — `reel_from_web`, `analyze_reference`
- رئيسي: `kosif-montage-motion` → `kmotion fetch` (yt-dlp؛ بنترست، تيك توك، إنستجرام، يوتيوب)
- بنترست بالبحث: لوحة المتصفح المدمجة، والمستخدم يسجّل الدخول بنفسه

## 2. المونتاج والريلز — `edit_my_footage`, `talking_reel`
- رئيسي: `kosif-montage-motion` (montage، timeline، reel، تلوين، قص الصمت، 9:16 ذكي، تمويه الوجوه)
- مدموج فيه: `pro-video-editor-ffmpeg`، `video-editing-captions`، `reels-shorts-factory`،
  `audio-reactive-captions-studio`، ومونتاج `ultra-motion-montage`

## 3. الموشن والأنيميشن 2D — `motion_2d`
- رئيسي: `hyperframes-animation-studio` (مسطّح SVG/GSAP)
- مدموج فيه: `motion-director-pro`، `kinetic-typography-arabic`، `data-in-motion`، `explainer-edu-animation`،
  `character-animation-2d`، `trend-animation-styles`، `claude-animation-studio`

## 4. السينما ثلاثية الأبعاد — `cinematic_3d`
- رئيسي: `hyperframes-animation-studio` (three-kit)
- مدموج فيه: `ultra-motion-montage`، `cinematic-3d-scene`

## 5. فيديو الإطلاق والإعلان — `launch_video`
- رئيسي: `kosif-montage-motion` → `kmotion brag` + `kmotion final`
- المراجعة: `motion-os` (صفحة مشهد بمشهد) ← `kmotion review`

## 6. فيلم من الصوت — `sound_to_film`
- رئيسي: `kosif-montage-motion` (verse، Voice2Motion/audio2motion)
- مدموج فيه: `audio-reactive-captions-studio`

## 7. البرومبتات والسينما — `ai_video_prompts`
- رئيسي: `kosif-omni:kosif-cinema-director` (7 طبقات)
- مدموج فيه: `cinema-director-7layers`، `video-prompt-director`، `kmotion aiprompts/omniprompt`،
  `kosif-omni:kosif-lighting`، `photo-lighting-plan`

## 8. الصور والجرافيك — `image_graphics`, `pixel_redraw`
- رئيسي: `image-prompt-forge` + `kosif-omni:kosif-image-studio`
- مدموج فيه: `thumbnail-social-graphics`، `brand-identity-logo`، `product-photo-mockups`، `pixel-art-game-assets`،
  `image-critique-reverse-prompt`
- رسم بيكسل ببيكسل / إعادة رسم مطابقة / تعديل لون: `pixel-studio-painter`

## 9. الصوت — `audio_only`
- رئيسي: `kmotion audiolab` + `audio-mastering-analysis`
- مدموج فيه: `kosif-omni:kosif-audio`، `kosif-omni:kosif-voice`

## 10. حركة المواقع — `ui_web_motion`
- `ui-motion-microinteractions`، `website-design-system`، `kosif-omni:kosif-web-design`

## 11. السوشيال ميديا — `social_content` (+ خطوة `post_pack` بعد كل فيديو)
- رئيسي: `kosif-social` — بوست لكل منصة (كابشن، وسوم، عنوان ووصف يوتيوب) يتفحص على حدود المنصة، كاروسيل PNG + PDF،
  خطة محتوى (CSV/Excel/تقويم)، أحسن وقت نشر من تحليلات الحساب نفسه، تجارب A/B بحجم عينة واختبار دلالة. **مفيش نشر.**
- مدموج فيه: `arabic-copywriting`، `storytelling-scripts`، `youtube-channel-strategy`، `market-competitor-research`،
  `ideation-100-ideas`، `seo-content-architecture`، `ecommerce-store-listings`، `newsletter-email-marketing`،
  `ab-testing-experiments`، `reels-shorts-factory`، `thumbnail-social-graphics`

## إضافات اتوصلت بأقسام موجودة (2026-10-09)
- المونتاج: `davinci-resolve-pipeline` · الإخراج: `storyboard-shotlist`، `storytelling-scripts`
- فيديو الإعلان: `ad-creative-30s` · البرومبتات: `storyboard-shotlist`
- الصوت: `voiceover-tts-direction`، `music-song-brief`، `podcast-production` (وكمان في ريل الكلام)
- الصور: `ai-art-style-library`، `svg-illustration-icons`

## 12. أغنية → ريل من بنترست — `song_reel`
- رئيسي: `kmotion songreel` (analyze → بحث بنترست لكل مقطع حسب المعنى → cut على البيت → build: كلمات متحركة فوق الفيديو)
- مبني على: `verse` (بقى يقبل فيديو تحت الكلمات) + `transcribe` (الغناء تحت الموسيقى) + `fetch`

## 13. المحاكاة — `mimic_reel`
- `kmotion mimic` (study / match / build) + مهارة `kosif-mimic` للدقة: إعادة تركيب الانتقالات بمنحنى تقدّمها المقاس،
  منحنيات حركة النص، مطابقة الخط من ~80 خط عربي، LUT لكل لقطة، الصوت الأصلي منسوخ كما هو
- من Cinema C (c32): طريقة التحميل بإعادة المحاولة، ومختبر الصوت (audiolab)

## مهارات خارجية متثبتة (2026-10-09) ومربوطة بالخطوات
- `brag` + `brag-slim` (github.com/latent-spaces/brag): فيديو إطلاق 15–25 ث من كود المشروع أو رابط موقع، 7 نبرات، موسيقى ومؤثرات مرفقة
- HyperFrames الرسمية (github.com/heygen-com/hyperframes): `hyperframes` (نقطة الدخول) · `-core` · `-animation` (24 تأثير نص + Three.js)
  · `-creative` · `-keyframes` (عمق 3D وحركة كاميرا) · `-cli` · `-audio` · `-registry` (~400 تأثير جاهز: حبيبات فيلم، غلتش، لمعة، رسوم بيانية)
  · `music-to-video` (فيديو كلمات على الإيقاع) · `motion-graphics` · `product-launch-video` · `embedded-captions` (ترجمة سينمائية ورا الشخص، 35 ستايل)
  · `talking-head-recut` · `faceless-explainer` · `general-video` · `media-use`
- `kosif-mimic`: المحاكاة الدقيقة · `motion-os`: صفحة المراجعة

## الجملة اللي تضيفها لأي طلب عشان كل القدرات تشتغل
> **بالعربي:** «استخدم كل قدراتك: افهم المادة الأول، واقترح 2–3 أفكار، واجمع من بنترست لو محتاج، واعمل مونتاج على
> الإيقاع والمعنى، وموشن وكتابة عربي متحركة و3D لو تفيد، وصوت مظبوط، وراجع الفريمات بنفسك، وسلّم 1080 مع الغلاف
> والحقوق والبوست لكل منصة.»
>
> **English:** "Full power: understand the material first, propose 2–3 directions, pull footage from Pinterest if it
> helps, cut on the beat and the meaning, add motion, kinetic Arabic type and 3D where they add something, master the
> sound, review the frames yourself, and deliver 1080p with a poster, credits and a post pack per platform."

## 14. أي شيء آخر — `not_media`
- `kosif-omni:kosif-omni` (كود، محاسبة، بحث، قرارات، إكسل، واتساب، GitHub…)

## نسخ مكررة يُفضّل تجاهلها
- `anthropic-skills:kosif-montage-motion` = نسخة 6.1 قديمة مرفوعة على claude.ai؛ الأحدث هي 6.2 في
  `~/.claude/skills/kosif-montage-motion`. على claude.ai ارفع ملف `KOSIF-Montage-Motion-v6.2-claude-ai.zip` بدلها.
- الأمر `/kosif-video` باقٍ ويعمل، لكنه للفيديو فقط؛ `kosif-one` يشمله.
