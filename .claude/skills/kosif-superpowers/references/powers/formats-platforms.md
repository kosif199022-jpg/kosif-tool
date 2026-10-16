# المقاسات والمنصات — Formats & platforms

> **قوتك هنا:** تسلّم فيلمًا واحدًا كأنه عشرة: كل منصة بمقاسها وحدودها ومنطقتها الآمنة، مُعاد تأطيره حول الوجه لا مقصوصًا من المنتصف، بغلاف ليس أسود، وبعلوّ −14 LUFS، ومعه نص النشر مفحوصًا بحدود كل منصة — دون أن تنشر شيئًا بنفسك.
> **أقوى دليل:** شغّلتَ هنا `kmotion.py platforms` على فيديو اختبار فخرجت نسخ tiktok/whatsapp/youtube مع تقرير حدود، و`kmotion.py export` أخرج 9:16 و1:1 وغلافًا وGIF، واختبارا `test_platforms_table` و`test_poster_pick_and_bake` نجحا (`100-superskills/skills/kosif-montage-motion/tests/test_v6.py:180`, `100-superskills/skills/kosif-montage-motion/tests/test_launch.py:89`).
> **You can:** pick the canvas from the destination, keep text out of platform chrome, reframe any ratio, encode web-safe masters, HLS ladders and alpha overlays, and ship per-platform files + post packs.
> **69 powers follow** — ✅ 17 · 🟢 15 · 📦 6 · 🔑 3 · 👁 2 · 📄 26 · 💡 0.

**الحالة / status:** ✅ مُثبت هنا (كود + اختبار أو رندر في هذه الحاوية) · 🟢 جاهز (كود المالك يعمل بلا إضافات) · 📦 بأمر تثبيت · 🔑 مفتاح أو خدمة · 👁 شوهد في فيديو أنتجتَه (وصفة البناء مرفقة) · 📄 موصوف فقط · 💡 فكرة.
مسارات الدليل نسبية إلى `/home/user/`؛ `style:<id>` = فيديو مرجعي أنتجتَه سابقًا (ملاحظاته في `kosif-tool/styles/<id>/`).

**فحص هذه الحاوية (2026-10-16):** على مصدر `testsrc2` 1920×1080/30: تعبئة ضبابية 9:16 ✔ · ماستر H.264 بعلامات BT.709 و`moov` قبل `mdat` ✔ · أشرطة 2.39:1 بـ drawbox ✔ · GIF بلوحة 128 لونًا (6 ث، 480 بكسل ≈ 1.0 MB) ✔ · سلم HLS بثلاث جودات ✔ (يلزم ربط الصوت ثلاث مرات) · فصول بعناوين عربية ✔ · WebM VP9 بقناة ألفا (alpha_mode=1) ✔ · ProRes 4444 ✔ (prores_ks يخرج yuva444p12le) · `kmotion platforms/export/aspect` ✔ · `social.py pack/check` ✔ · `build_studio_cloud.py` بنى صفحة 78,544 بايت ✔.

## الفهرس / contents
- **المقاسات والنسب — Canvases & aspect ratios** — FMT-01 … FMT-07 (7)
- **المناطق الآمنة والمقروئية — Safe zones & legibility** — FMT-08 … FMT-12 (5)
- **إعادة التأطير والتحويل — Reframing & conversion** — FMT-13 … FMT-19 (7)
- **الترميز والماستر والتسليم التقني — Encoding, masters & technical delivery** — FMT-20 … FMT-30 (11)
- **التصدير لكل منصة وحزم النشر — Per-platform exports & post packs** — FMT-31 … FMT-43 (13)
- **الأغلفة والصور المصغرة والأصول الثابتة — Thumbnails, covers & static assets** — FMT-44 … FMT-54 (11)
- **قوالب السوشيال وإيقاع الإعلانات — Social formats, ad slots & platform blocks** — FMT-55 … FMT-69 (15)
- توليفات قوية / power combos · أخطاء ممنوعة / never do · أقوى 5 حركات توقيع / 5 signature moves

## المقاسات والنسب — Canvases & aspect ratios

_اختر الإطار من مكان العرض، ثم ثبّت المقاس قبل أول بكسل._

#### FMT-01 · المقاس من الوجهة · Derive the canvas from the destination · 🟢 جاهز / ready
- **ماذا / what:** لا تسأل «أي مقاس؟» بل «أين سيُعرض؟» واشتق الإطار وسجّل الاشتقاق في البريف. — Derive the canvas from where it plays and record the derivation in the brief.
- **متى أستخدمها / when:** أول سؤال في كل بريف — first decision of every brief.
- **كيف / how:** Reels/TikTok/Shorts/Snapchat/WhatsApp status → 9:16 1080×1920; YouTube/site/desktop → 16:9 1920×1080; feed reach → 4:5 1080×1350; square feed → 1:1 1080×1080; link preview → 1.91:1 1200×630; Pinterest → 2:3 1000×1500; cinema → 2.39:1. Fastify planner sets 9:16 by default and render.py forces even widths (width=round(h*ratio)); beware `--height 1920` on 16:9 gives 3413×1920, so pass `--height 1080`. KOSIF scaffolds declare the target per composition. **أرقام / params:** 9:16 1080×1920 · 16:9 1920×1080 · 4:5 1080×1350 · 1:1 1080×1080 · 1.91:1 1200×630 · 2:3 1000×1500.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes/references/brief-contract.md` · `kosif-atlas/skills/2976-pwdev-social-media/12587-format-specs/SKILL.md` · `fastify-motion-bro/scripts/render.py:29-33` · `fastify-motion-bro/scripts/planner.mjs:10`

#### FMT-02 · جدول المقاسات الموحد في أدواتك · Aspect presets across the owner tools · ✅ مُثبت هنا / proven here
- **ماذا / what:** كل أدواتك تتفق على نفس الجدول: 9:16 و16:9 و1:1 و4:5، مع 4:3 و21:9 في التحقق والمونتاج. — All owner tools share one ratio table; verify_video also accepts 4:3 and 21:9.
- **متى أستخدمها / when:** عند scaffold أو montage أو التحقق — any scaffold, montage or verify call.
- **كيف / how:** `kosif.py scaffold <id> <dir>` and `verify_video.py --aspect`; kosif-studio RATIOS add 4:3 1440×1080 and 21:9 2520×1080; claude-animation-studio `new_scene.py --ratio 9:16 --dur 10 --fps 30 --kind 2d|3d`; studio forms offer fps 24/25/30/50/60. Basma editor works at 720p (9:16 720×1280, 1:1 900×900, 16:9 1280×720, 4:5 864×1080) and exports with short side 1080; it auto-picks the aspect from the source ratio (>1.2 → 16:9, <0.7 → 9:16, <0.9 → 4:5, else 1:1). Verified here: verify_video passed 11/12 on a 9:16 platform file (loudness check failed on a sine tone, as expected). **أرقام / params:** 4:3 1440×1080 · 21:9 2520×1080 · Basma 720p working size, 1080 export.
- **الدليل / proof:** `kosif-tool/tools/kosif.py:35` · `kosif-tool/tools/verify_video.py:24` · `kosif-studio/motion/tools.py:44` · `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:15` · `app/public/js/00_editor.js:72`

#### FMT-03 · الإطار السينمائي العريض والأشرطة · Cinematic 2.35/2.39:1 and letterbox bars · ✅ مُثبت هنا / proven here
- **ماذا / what:** إما ترندر مباشرة بإطار عريض (1920×816) أو تضع أشرطة سوداء داخل 16:9، وأحيانًا تنفتح الأشرطة في أول اللقطة. — Render a native 1920×816 frame, or burn black bars inside 16:9; optionally animate the bars open.
- **متى أستخدمها / when:** تريلر، سرد سينمائي، افتتاح فاخر — trailers, cinematic stories, premium openers.
- **كيف / how:** Bar height = (H − W/2.39)/2 → 138 px at 1080p, 92 px at 720p (≈12–12.5% each). Burn with two drawbox fills; place subtitles inside the lower bar. Animated reveal (scene3d template): #letterbox-top/bottom from 70 px → 0 over 2.2 s power4.inOut, starting at min(2.4 s, 15% of D). Compose subjects on thirds with wide negative space. Verified here with drawbox on 1920×1080. **أرقام / params:** bars 138 px @1080p · 92 px @720p · reveal 70→0 px / 2.2 s.

```bash
ffmpeg -i in.mp4 -vf "drawbox=y=0:w=iw:h=(ih-iw/2.39)/2:c=black:t=fill,\
  drawbox=y=ih-(ih-iw/2.39)/2:w=iw:h=(ih-iw/2.39)/2:c=black:t=fill" -c:a copy out.mp4
```

- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/templates/scene3d/index.html:36` · `style:pm-theparuchh-6e08c3` · `style:pm-rebutonepress-810f78` · `style:pm-kamstudiolabs-0b0824`

#### FMT-04 · مسرح ثابت يُكبَّر ككتلة · Fixed stage scaled as one block · 📄 موصوف / documented only
- **ماذا / what:** صمّم كل إطار على 1920×1080 ثابت وكبّر المسرح كله للنافذة بدل إعادة التدفق. — Author on a fixed 1920×1080 stage and scale the whole stage to the viewport instead of reflowing.
- **متى أستخدمها / when:** عروض HTML ومعاينات داخل iframe — HTML decks and iframe previews.
- **كيف / how:** .stage{width:1920px;height:1080px;transform:scale(min(vw/1920, vh/1080))} with letter/pillarbox; keep all chrome inside the stage; switch slides with opacity/visibility not display; no breakpoints inside the stage. For video renders this equals fixed px layout per data-width/height on #root. **أرقام / params:** stage 1920×1080; scale = min(vw/1920, vh/1080).
- **الدليل / proof:** `kosif-atlas/skills/880-superloopy/1944-superloopy-slides/viewport-base.css` · `kosif-atlas/skills/880-superloopy/1944-superloopy-slides/html-template.md` · `100-superskills/skills/kosif-montage-motion/scripts/projects/five_sec/index.html:33`

#### FMT-05 · خط متجاوب بين المقاسات · Fluid type tokens per aspect · 📄 موصوف / documented only
- **ماذا / what:** تكوين واحد يُصدَّر إلى 16:9 و9:16 و1:1 بأحجام خط مشتقة من عرض الإطار. — One composition exports to 16:9, 9:16 and 1:1 with type sized from the frame width.
- **متى أستخدمها / when:** عند تصدير نفس المشهد بعدة نسب — same scene in several ratios.
- **كيف / how:** Size tokens per aspect, or clamp()/vw against the composition width (not the browser). Minimums at 1080 wide: body/caption ≥ 48–64 px on 9:16, smallest legible 36 px; split content rather than shrinking it. **أرقام / params:** captions ≥48–64 px @1080 w; floor 36 px.
- **الدليل / proof:** `kosif-atlas/skills/3438-ux-design/14126-web-typography/references/responsive-typography.md` · `kosif-atlas/skills/3438-ux-design/14126-web-typography/SKILL.md`

#### FMT-06 · نسختان مقصودتان لمشاهد البيانات · Deliberate vertical vs horizontal data layouts · 📄 موصوف / documented only
- **ماذا / what:** لا تضغط رسمًا أفقيًا في إطار عمودي؛ صمّم نسخة رأسية بعلامات أقل وعناوين أقصر. — Design vertical and horizontal versions of a data scene instead of squeezing the desktop chart.
- **متى أستخدمها / when:** أي رسم بيانات أو خريطة ستُسلَّم بنسبتين — any chart/map delivered in two ratios.
- **كيف / how:** 9:16: fewer markers, shorter labels, stacked small multiples, legend below, 3–5 ticks. 16:9: side-by-side panels, 4–7 ticks. Map plates 3840×2160 for 16:9 and ≈2700×3840 for 9:16. Inspect rendered pixels at every ratio (see DATA, MAP families). **أرقام / params:** ticks 3–5 vertical · 4–7 horizontal · map plate 3840×2160 / 2700×3840.
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10320-d3-data-visualization/SKILL.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/mapbox/references/render-stability.md`

#### FMT-07 · أبعاد تناسب نماذج التوليد · Latent-friendly sizes and frame counts · 📄 موصوف / documented only
- **ماذا / what:** نماذج الانتشار تريد أبعادًا تقبل القسمة على 8 أو 16 أو 32، وLTX يريد 8k+1 إطارًا. — Diffusion models need sizes divisible by 8/16/32 and LTX needs 8k+1 frames.
- **متى أستخدمها / when:** قبل إرسال أي طلب توليد صورة أو فيديو — before any image/video generation call (GEN).
- **كيف / how:** Round W/H to ÷8 (SD), ÷16 (Wan, Krea 2), ÷32 (LTX); LTX common 768×512, 1216×704, 704×480 with 121/161/257 frames; frames = round_to_8k+1(duration×fps). Then upscale/reframe to the delivery canvas, never stretch. AI clip slot lengths used by Fastify profiles: 6 s (fitness, viral), 7 s (stickman), 8 s Veo / 10 s Flow (kinetic), 10 s (vox, food) — re-verify model availability. **أرقام / params:** ÷8/÷16/÷32 · frames 8k+1 · clips 6/7/8/10 s.
- **الدليل / proof:** `kosif-atlas/skills/2142-comfyui-plugin/7651-comfy-image-utils` · `fastify-motion-bro/scripts/profiles/kinetic-flow.mjs:41,116` · `fastify-motion-bro/docs/PROFILE_CATALOG.md:19`

## المناطق الآمنة والمقروئية — Safe zones & legibility

_واجهة المنصة تغطي الحواف؛ ارسم الخطوط الإرشادية قبل التصميم._

#### FMT-08 · المنطقة الآمنة في الإطار العمودي · 9:16 UI safe zone · ✅ مُثبت هنا / proven here
- **ماذا / what:** في 1080×1920 تغطي أزرار المنصة الأعلى والأسفل والجانب الأيمن؛ ضع النص والوجوه والدعوة داخل ≈900×1350 مزاحة للأعلى. — On 1080×1920 platform chrome covers top, bottom and right rail; keep critical content in a ~900×1350 zone nudged upward.
- **متى أستخدمها / when:** كل ريل/شورت/ستوري — every vertical deliverable.
- **كيف / how:** Conservative margins: top 250, bottom 320, right 120, left 60 px (IG story/reel covers: avoid 250 top / 400 bottom; rule of thumb: UI covers bottom 20% and right 12%). Owner variants: kosif-tool starter safe overlay inset 120/60/220 px (checkbox #safe, verified in the canvas starter), Basma review rule top 14% / bottom 18% (25–35% in its director KB) / sides 6% with captions ≈70% down; tool-briefs use 120 px top/bottom. Values drift with app updates — draw guides first, screenshot-check. **أرقام / params:** T250 B320 R120 L60 · trusted ≈900×1350 · starter inset 120/60/220.
- **الدليل / proof:** `kosif-tool/starters/html-canvas/index.html:47` · `kosif-tool/playbooks/kinetic-type.md:19` · `kosif-atlas/skills/2976-pwdev-social-media/12592-story-reels/SKILL.md` · `app/public/js/00_editor.js:1491`

#### FMT-09 · جدول هوامش المنصات للصور · Social canvas + text-safe margin table · 📄 موصوف / documented only
- **ماذا / what:** مقاسات الصور الثابتة والأغلفة مع الهامش الآمن لكل سطح. — Still/cover sizes with text-safe margins per surface.
- **متى أستخدمها / when:** أغلفة، بانرات، بطاقات روابط — covers, banners, link cards.
- **كيف / how:** LinkedIn post 1200×627 (100 px) · X card 1200×675 (80 px) · IG square 1080×1080 (108 px = 10%) · IG landscape 1080×566 (80 px) · FB post 1200×630 (100 px) · YouTube thumbnail 1280×720 (72 px) · channel art 2560×1440 (safe 1546×423 centred) · LinkedIn cover 1584×396 · X header 1500×500 · GitHub preview 1280×640 ≤1 MB · display 300×250, 728×90, 160×600. Keep key content 10–15% from edges. **أرقام / params:** see table; general 10–15% margin.
- **الدليل / proof:** `kosif-atlas/skills/1567-tonone/4428-form-social/SKILL.md` · `kosif-atlas/skills/1446-marketing-skills/3504-image` · `kosif-atlas/skills/2153-github-actions-plugin/7759-github-social-preview`

#### FMT-10 · منطقة الترجمة الآمنة · Caption safe area · 📄 موصوف / documented only
- **ماذا / what:** الترجمة داخل title-safe 90% وبعيدة عن واجهة المنصة، سطران كحد أقصى. — Captions inside 90% title-safe, clear of platform UI, max two lines.
- **متى أستخدمها / when:** كل ترجمة محروقة — every burned caption (pairs with ARAB-64).
- **كيف / how:** 5% margins; on 9:16 keep out of bottom ≈20% and right ≈12%; position ≈70% down; ≤2 lines; contrast ≥4.5:1 (≥7:1 for small mobile text). **أرقام / params:** 2 lines · 5% margins · contrast ≥4.5:1.
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-typography/references/quality-and-editors.md` · `kosif-atlas/skills/1503-universal-design-principles/3825-legibility-contrast-and-spacing/SKILL.md`

#### FMT-11 · قواعد المقروئية على الهاتف · Phone legibility gate · 🟢 جاهز / ready
- **ماذا / what:** أصغر نص 36 بكسل على عرض 1080، فحص على معاينة 360 بكسل، تباين ≥4.5:1. — Smallest text 36 px at 1080 wide, checked on a 360 px preview, contrast ≥4.5:1.
- **متى أستخدمها / when:** قبل الرندر النهائي — before final render (TEST_REPORT checks 8, 12, 13).
- **كيف / how:** kosif-tool STYLE.md §6 + TEST_REPORT: sides 5%, top/bottom 12% on 9:16; Basma wraps every agent run on 9:16 so caption.size < 9 becomes 9.5 and missing stroke becomes 6; montage-motion readable() rule passes its test (`test_launch.Rules.test_readable`). **أرقام / params:** min 36 px @1080 · preview 360 px · Basma caption ≥9.5, stroke 6.
- **الدليل / proof:** `kosif-tool/templates/STYLE.md` · `kosif-tool/templates/TEST_REPORT.md` · `app/public/js/10_studio.js:4614`

#### FMT-12 · كثافة العرض: متحدث أم قراءة · Density mode: narrated vs read-first · 📄 موصوف / documented only
- **ماذا / what:** المحتوى المروي فكرة واحدة في الإطار بخط ضخم، والمقروء صامتًا يحتمل بنية أكثر؛ قسّم بدل أن تصغّر. — Narrated pieces carry one idea per frame; silent read-first pieces can hold more — split rather than shrink.
- **متى أستخدمها / when:** عند تحديد عدد النقاط في المشهد — sizing each scene.
- **كيف / how:** Ask: narrated or silent? Speaker-led: 1–3 bullets; reading-first: 4–8 bullets or 4–6 cards. Social autoplays muted, so burn the key words or ship captions.vtt. **أرقام / params:** speaker-led 1–3 · read-first 4–8 bullets / 4–6 cards.
- **الدليل / proof:** `kosif-atlas/skills/880-superloopy/1944-superloopy-slides` · `kosif-atlas/skills/1511-homie/3903-video/references/DELIVERY.md`

## إعادة التأطير والتحويل — Reframing & conversion

_قصّ المنتصف الأعمى ممنوع: إما تتبّع الموضوع، أو صورة كاملة فوق نسختها الضبابية._

#### FMT-13 · إعادة تأطير ذكية حول الوجوه · Smart reframe around faces · ✅ مُثبت هنا / proven here
- **ماذا / what:** تحويل أي لقطة لنسبة أخرى يتبع الوجوه (ومركز الحركة عند غيابها)، أو قص المنتصف، أو صورة فوق خلفية ضبابية. — Reframe to another ratio following faces (motion-centroid fallback), centre crop, or fit over a blurred fill.
- **متى أستخدمها / when:** تحويل مقطع 16:9 لريل أو 4:5 — turning landscape footage into vertical/feed.
- **كيف / how:** `python3 scripts/kmotion.py aspect CLIP --to 9:16|16:9|1:1|4:5 --mode smart|crop|blur --out v.mp4` (same tool in kosif-studio `motion/tools.py aspect`, studio recipe "aspect", MCP kosif_run). Blur mode: gblur sigma 40, brightness −0.12, saturation 0.85. Verified here: 1920×1080 → 4:5 smart gave 1080×1350. Heavier subject tracking (YOLO/mediapipe) is an install away; Resolve Smart Reframe needs Resolve Studio. **أرقام / params:** modes smart|crop|blur · blur σ40, −0.12 brightness, 0.85 sat.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md` · `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:70` · `kosif-studio/motion/tools.py:219` · `kosif-one/tools/kosif-studio/motion/tools.py:219`

#### FMT-14 · الصورة الكاملة فوق نسختها الضبابية · Full frame over its blurred fill · ✅ مُثبت هنا / proven here
- **ماذا / what:** اصنع 9:16 من 16:9 بوضع الإطار كاملًا في المنتصف فوق نسخة مكبّرة مموّهة ومعتمة منه. — Make 9:16 from 16:9 by laying the full frame over a scaled, blurred, darkened copy of itself.
- **متى أستخدمها / when:** لقطات لا تحتمل القص: شاشات، نصوص، مجموعات — footage that cannot be cropped.
- **كيف / how:** Verified here on 1920×1080 → 1080×1920. Variants: gblur sigma 30 instead of boxblur; HyperFrames yt-vertical-fill block does the reverse (portrait inside 16:9 with blurred/mirror/copy side fills, grid texture, contrast lift; `npx hyperframes add yt-vertical-fill`). **أرقام / params:** boxblur 20 · brightness −0.15 · fg 1080 wide.

```bash
ffmpeg -i in.mp4 -filter_complex "[0:v]split[a][b];\
 [a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20,eq=brightness=-0.15[bg];\
 [b]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2" -c:a copy v.mp4
```

- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3903-video/references/TRAILER.md` · `100-superskills/skills/pro-video-editor-ffmpeg/references/ffmpeg-recipes.md` · `kosif-one/vendor/hyperframes/registry/blocks/yt-vertical-fill/yt-vertical-fill.html`

#### FMT-15 · تحجيم مع حشو لأي إطار · Scale + pad / centre crop · 🟢 جاهز / ready
- **ماذا / what:** أدخل أي مصدر في إطار الهدف بلا تشويه: تصغير وحشو (letter/pillarbox)، أو قص المنتصف عندما يكون الموضوع في الوسط فعلًا. — Fit any source without distortion: scale down and pad, or centre-crop only when the subject really is centred.
- **متى أستخدمها / when:** شرائح، لقطات شاشة، مصادر غير متوقعة — slides, screenshots, odd sources.
- **كيف / how:** Pad: scale=W:H:force_original_aspect_ratio=decrease,pad=W:H:(ow-iw)/2:(oh-ih)/2. Centre crop: crop=ih*9/16:ih,scale=1080:1920 (pro-video-editor edl_render `--ratios 9:16,1:1`). Never pad with plain black for social — prefer the blurred fill. **أرقام / params:** targets 1080×1920 · 1080×1350 · 1080×1080 · 1920×1080.
- **الدليل / proof:** `kosif-atlas/skills/235-mas-video-lab/754-ffmpeg/SKILL.md` · `100-superskills/skills/pro-video-editor-ffmpeg/scripts/edl_render.py:126`

#### FMT-16 · أوضاع ملاءمة اللقطة: cover / contain / blur · Clip fit modes cover · contain · blur · 🟢 جاهز / ready
- **ماذا / what:** اللقطات البديلة تُقص وتُطابق سرعتها وتثبّت إطاراتها ثم تُلائم الإطار بالتغطية أو الاحتواء أو الخلفية الضبابية بعدد إطارات اللقطة بالضبط. — Replacement clips are trimmed, speed-matched, set to CFR and fitted by cover/contain/blur to the exact shot frame count.
- **متى أستخدمها / when:** تايملاين JSON أو محاكاة فيديو مرجعي — timeline JSON builds and mimic replacements.
- **كيف / how:** Timeline JSON `clips[].fit = cover|contain|blur`; mimic `shots[i].replacement.fit` → mm_build._fit_filter / prep_shot. Found-footage normaliser (Ghorba): -ss 0 -t DUR -an, scale=W:H:force_original_aspect_ratio=increase:flags=bicubic,crop=W:H,setsar=1,fps=24,<grade>,format=yuv420p, libx264 crf 24 -threads 2, -stream_loop -1 for clips shorter than the slot. **أرقام / params:** Ghorba 540×960 or 720×1280 @24 · crf 24 · threads 2.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/timeline-schema.md` · `kosif-one/tools/kosif-mimic/scripts/mm_build.py` · `kosif-one/projects/KOSIF_Motion_Ghorba/KOSIF_Ghorba_Render.py:146-148`

#### FMT-17 · دفعة شورتس من مونتاج طويل · Batch vertical shorts from a long edit · 📄 موصوف / documented only
- **ماذا / what:** من تايملاين طويل اقترح ≈20 مرشحًا بخطافات مختلفة وتوقيتات دخول وخروج دقيقة، ثم نسخ عمودية بتأطير يتبع الموضوع. — Propose ~20 short candidates with distinct hooks and exact in/out from a long timeline, then reframe each to portrait.
- **متى أستخدمها / when:** بودكاست، محاضرة، بث طويل — podcasts, talks, long streams.
- **كيف / how:** Feasibility: a 60 s short with two 15 s handles needs ≥90 s of source. Local path: per candidate ffmpeg trim + kmotion aspect --mode smart (or blur), inspect frames; never pad black or silently shorten. Resolve path: duplicate timeline, custom 2160×3840 before switching to portrait, Smart Reframe per clip (Resolve Studio scripting), verify the render really is 2160×3840 — API success ≠ good framing. **أرقام / params:** 20 candidates · 60 s + 2×15 s handles · 2160×3840.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2466-davinciresolve-youtube-shorts/SKILL.md`

#### FMT-18 · إعادة التكوين لا القص الأعمى · Recompose per platform, never blind-crop · 📄 موصوف / documented only
- **ماذا / what:** رندر الماستر بأكبر نسبة ثم أعد تكوين كل منصة (مواضع النص والعناصر) ويمر كل ملف من بوابة الفحص. — Render the master at the largest aspect, recompose each platform version and gate each file.
- **متى أستخدمها / when:** أي تسليم متعدد النسب لموشن مصمم — multi-ratio delivery of designed motion.
- **كيف / how:** For HTML motion, re-render each ratio from the same composition with ratio-specific layout tokens (text blocks, legends) instead of cropping pixels; for product/feature videos reframe each ratio against the real UI and make one poster per ratio. Native portrait renders of every AI clip cost ≈2× (scroll-world clipMobile chain, 720 w, -g 4); a focus-x % per stop can steer a cheaper 16:9→9:16 crop. **أرقام / params:** 16:9 · 4:5 · 9:16 · 1:1; native portrait ≈2× cost.
- **رخصة / license:** mcp-higgsfield-landing has no licence file — read for ideas, do not copy code.
- **الدليل / proof:** `kosif-tool/playbooks/render-pipeline.md:57` · `kosif-atlas/skills/101-video-skills/215-feature-video` · `kosif-one/vendor/scroll-world/skills/scroll-world/SKILL.md` · `kosif-one/vendor/mcp-higgsfield-landing/src/scripts/world.ts:86`

#### FMT-19 · نسخ الصور متعددة المقاسات بخدمة Adobe · Multi-ratio still variations via Adobe · 🔑 مفتاح أو خدمة / needs key or paid service
- **ماذا / what:** من صورة واحدة نسخ لكل منصة بقص يتبع الموضوع أو توسيع بالذكاء، بمعاينة 3 قصّات أولًا. — Platform crops from one image with subject-aware crop or generative expand, previewing 3 crops first.
- **متى أستخدمها / when:** عندما يكون حساب Adobe متصلًا — only with an Adobe connector/account.
- **كيف / how:** Adobe Firefly connector: image_crop_and_resize / video_resize (video is resize only, no auto-reframe), focus subject|face|upper_body|{prompt}|{x,y}. Local equivalent: saliency/face box → crop, or blurred/mirrored fill. **أرقام / params:** 3-crop preview · focus modes.
- **الدليل / proof:** `kosif-atlas/skills/103-adobe-for-creativity/232-adobe-create-social-variations/SKILL.md` · `kosif-atlas/skills/103-adobe-for-creativity/238-adobe-resize-photos-and-videos/SKILL.md`

## الترميز والماستر والتسليم التقني — Encoding, masters & technical delivery

_كل MP4 يخرج 4:2:0 بعلامات BT.709 و faststart وصوت 48 kHz — ثم يُقاس._

#### FMT-20 · ماستر H.264 آمن للويب · Web-safe H.264 master · ✅ مُثبت هنا / proven here
- **ماذا / what:** كل MP4 للويب 8-bit 4:2:0، وذرة moov في المقدمة ليبدأ التشغيل قبل اكتمال التحميل، وعلامات BT.709 حتى لا يبهت اللون على iOS. — Every web/social MP4 is 8-bit 4:2:0, moov-first and tagged BT.709 so iOS/QuickTime do not wash colours out.
- **متى أستخدمها / when:** كل تسليم نهائي — every final file.
- **كيف / how:** Verified here: bt709 tags read back by ffprobe and moov before mdat. Owner encoders: kosif-studio film.Encoder pipes RGB into libx264 and raises if ffmpeg exits non-zero (draft ultrafast/crf 23, delivery medium/crf 18, GOP 2×fps); fastify render.py CRF 19; kosif-tool render-pipeline H.264 High CRF 18–20; kosif-studio tools gate: even dimensions, AAC 48 kHz 192–256k. **أرقام / params:** crf 17–18 final / 23 web · AAC 160–320k 48 kHz · GOP 2×fps.

```bash
ffmpeg -i in.mov -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 \
  -movflags +faststart -c:a aac -b:a 192k -ar 48000 out.mp4
```

- **الدليل / proof:** `kosif-atlas/skills/235-mas-video-lab/754-ffmpeg/SKILL.md` · `kosif-studio/film.py:38` · `kosif-studio/motion/tools.py:42` · `kosif-tool/playbooks/render-pipeline.md:65`

#### FMT-21 · ماستر يوتيوب 4K · YouTube 4K delivery spec · 📄 موصوف / documented only
- **ماذا / what:** 3840×2160 بإطارات التايملاين، H.264 بـ 45 Mbps (≤30 fps) أو 68 Mbps (60 fps)، وصوت AAC 320k. — 3840×2160 at timeline fps, H.264 45/68 Mbps or H.265 30/45, AAC 48 kHz 320 kbps, −14 LUFS.
- **متى أستخدمها / when:** تسليم يوتيوب عالي الجودة — premium YouTube uploads.
- **كيف / how:** ffmpeg -c:v libx264 -b:v 45M -maxrate 50M -bufsize 90M; if the NLE lacks AAC, render PCM then -c:v copy -c:a aac -b:a 320k; verify frame count within 1 frame of the timeline; −14 LUFS ±1, TP ≤ −1 dBTP. Vector scenes can be re-rendered at 4K (HyperFrames `--resolution landscape-4k` via deviceScaleFactor; kosif-studio `studio.py SCENE --render out.png --scale 3.2` = 3840×2560, raster results enlarged by integer Lanczos with unsharp 1.35/−0.35). **أرقام / params:** 45/68 Mbps · AAC 320k · frame count ±1.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2450-davinciresolve-audio-delivery/SKILL.md` · `kosif-one/vendor/hyperframes/docs/guides/4k-rendering.mdx` · `kosif-studio/studio.py:141` · `kosif-one/tools/kosif-studio/studio.py:342`

#### FMT-22 · فيديو بقناة شفافة · Alpha video: WebM VP9 & ProRes 4444 · ✅ مُثبت هنا / proven here
- **ماذا / what:** صدّر الطبقات (شريط اسم، ملصق، شعار) بشفافية لتركيبها في محرر آخر أو على صفحة. — Export overlays with alpha for NLEs (ProRes 4444 .mov) or the web (VP9 .webm).
- **متى أستخدمها / when:** عندما يطلب المستخدم «ملف أركّبه على فيديوهاتي» — overlays for other editors.
- **كيف / how:** Verified here: VP9 yuva420p reports alpha_mode=1; prores_ks -profile:v 4444 writes yuva444p12le. Remotion: --image-format=png --pixel-format=yuva444p10le --codec=prores --prores-profile=4444, or yuva420p + vp9. HyperFrames: render --format webm|mov|png-sequence. The page background must be transparent. **أرقام / params:** yuva420p (web) · yuva444p10le (NLE).

```bash
ffmpeg -framerate 30 -i f_%05d.png -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 0 -crf 30 out.webm
ffmpeg -framerate 30 -i f_%05d.png -c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le out.mov
```

- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10438-remotion-render/transparent-videos.md` · `kosif-one/vendor/hyperframes/docs/packages/cli.mdx`

#### FMT-23 · HDR بعشرة بت · HDR 10-bit HEVC · 📦 بأمر تثبيت / one install
- **ماذا / what:** حافظ على مصادر BT.2020 PQ/HLG في HEVC بعشرة بت. — Keep BT.2020 PQ/HLG sources in 10-bit HEVC MP4.
- **متى أستخدمها / when:** فقط عندما تكون المصادر HDR فعلًا — only with real HDR sources.
- **كيف / how:** HyperFrames render --hdr (auto when sources are HDR; not combinable with --resolution); verify transfer/primaries with ffprobe. Social defaults stay SDR BT.709.
- **تثبيت / install:** `npm i -D hyperframes@0.8.164`
- **رخصة / license:** Apache-2.0
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/guides/hdr.mdx`

#### FMT-24 · سلم جودات HLS · Multi-rendition HLS ladder · ✅ مُثبت هنا / proven here
- **ماذا / what:** ماستر واحد ← 1080/720/480 بإطارات مفتاحية متطابقة للبث التكيّفي. — One master packaged into 1080/720/480 renditions with aligned keyframes.
- **متى أستخدمها / when:** استضافة فيديو على موقع أو منصة تعليمية — self-hosted streaming.
- **كيف / how:** Verified here: 3 variant playlists + master.m3u8 with 3 STREAM-INF. Gotcha found here: with var_stream_map each rendition needs its own audio map (-map 0:a three times), otherwise ffmpeg fails with "Invalid argument". Choose HLS (widest), DASH, CMAF (one set for both) or LL-HLS/WebRTC for live; DRM and CDN are external. **أرقام / params:** 5000/2800/1400k · GOP 60 @30 fps · 4 s segments.

```bash
ffmpeg -i m.mp4 -filter_complex "[0:v]split=3[a][b][c];[a]scale=-2:1080[o1];[b]scale=-2:720[o2];[c]scale=-2:480[o3]" \
 -map [o1] -map [o2] -map [o3] -map 0:a -map 0:a -map 0:a -c:v libx264 -b:v:0 5000k -b:v:1 2800k -b:v:2 1400k \
 -g 60 -keyint_min 60 -sc_threshold 0 -c:a aac -b:a 128k -f hls -hls_time 4 -hls_playlist_type vod \
 -hls_flags independent_segments -var_stream_map "v:0,a:0 v:1,a:1 v:2,a:2" -master_pl_name master.m3u8 h_%v.m3u8
```

- **الدليل / proof:** `kosif-atlas/skills/235-mas-video-lab/754-ffmpeg/SKILL.md` · `kosif-atlas/skills/2387-streaming-media-engineering/9243-transcoding-and-abr-ladder/SKILL.md` · `kosif-atlas/skills/2387-streaming-media-engineering/9242-streaming-architecture-and-protocol-sele/SKILL.md`

#### FMT-25 · ترميز GPU بـ NVENC · NVENC GPU encode · 📄 موصوف / documented only
- **ماذا / what:** ترميز سريع على كرت NVIDIA بإعدادات جودة عالية. — Fast NVIDIA encode with quality flags.
- **متى أستخدمها / when:** على جهاز المستخدم بكرت NVIDIA فقط — user machines with NVIDIA (not this container).
- **كيف / how:** -c:v h264_nvenc -preset p7 -tune hq -rc vbr -cq 19; HyperFrames --gpu. This container has no GPU — use libx264. **أرقام / params:** cq 19 · preset p7.
- **الدليل / proof:** `kosif-atlas/skills/235-mas-video-lab/754-ffmpeg/SKILL.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-cli/SKILL.md`

#### FMT-26 · أهداف العلوّ لكل وجهة · Loudness targets per destination · 🟢 جاهز / ready
- **ماذا / what:** قِس ثم اضبط الكسب إلى الهدف وحدّ القمة الحقيقية. — Measure, gain to the destination target, limit true peak.
- **متى أستخدمها / when:** آخر خطوة صوتية قبل التسليم — last audio step (see BEAT, VOICE).
- **كيف / how:** Web/YouTube/Spotify/Apple −14 LUFS ±1, TP ≤ −1 dBTP; calm pieces −16 to −18; podcast −16 (mono −19); broadcast EBU R128 −23; club −9 to −6 (script −8); music bed under SFX −18 to −20. Two-pass loudnorm I=-14:TP=-1:LRA=11, then confirm with ebur128=peak=true on the encoded file; kosif-tool verify_video prints LUFS and TP (the proof films measured −14.0 LUFS / −2.1 dBFS). Preserve user audio untouched unless asked. **أرقام / params:** −14 LUFS · TP −1 dBTP · podcast −16 · R128 −23.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-audio/scripts/audio_analyze.py:30` · `kosif-atlas/skills/1526-gamegen/4163-game-audio-procedural/references/mixing-and-loops.md` · `kosif-tool/tools/verify_video.py` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/glass-luxury-logo/README.md`

#### FMT-27 · صيغ الصوت للحلقات وتراخيص الموسيقى · Loop audio formats & music licence receipts · 📄 موصوف / documented only
- **ماذا / what:** MP3 يضيف صمتًا في الطرفين فيكسر الحلقات؛ سلّم WAV/OGG/Opus، وسجّل ترخيص الموسيقى في إيصال الرندر. — MP3 pads silence and breaks loops — ship WAV/OGG/Opus; record music rights in the render receipt.
- **متى أستخدمها / when:** GIF/فيديو متكرر بصوت، أو موسيقى مولدة — loops and generated music.
- **كيف / how:** ffmpeg -c:a libopus or pcm_s16le; browsers need Web Audio buffer loop. ElevenLabs free plan has no commercial licence and needs "Eleven Music" credit; paid plan licence counts at render time — store plan/rights in the receipt.
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3901-sound/references/TRAPS.md` · `kosif-atlas/skills/1511-homie/3892-music/references/RIGHTS.md`

#### FMT-28 · مواصفات معاينة متجر التطبيقات · App-store preview video spec · 📄 موصوف / documented only
- **ماذا / what:** معاينات iOS: حتى 3، من 15 إلى 30 ث، ≤500 MB، لقطات التطبيق الحقيقية فقط، وأول 5 ث تحسم. — iOS previews: up to 3, 15–30 s, ≤500 MB, real app footage only; the first 5 s decide.
- **متى أستخدمها / when:** إعلان تطبيق للمتجر — app store listings.
- **كيف / how:** H.264 10–12 Mbps up to 30 fps (or ProRes 422 HQ), stereo AAC 256 kbps at 44.1/48 kHz, .mov/.m4v/.mp4, autoplays muted; average watch 4–6.5 s. Google Play takes a YouTube URL. ffmpeg -c:v libx264 -b:v 11M -maxrate 12M -r 30 -c:a aac -b:a 256k -ar 48000 -ac 2; verify with ffprobe. **أرقام / params:** 15–30 s · 10–12 Mbps · ≤30 fps · AAC 256k.
- **الدليل / proof:** `kosif-atlas/skills/1446-marketing-skills/3488-aso/references/apple-specs.md` · `kosif-atlas/skills/1446-marketing-skills/3488-aso/references/google-play-specs.md`

#### FMT-29 · تضمين الموشن في صفحات الويب · Web embedding of motion & media · 📄 موصوف / documented only
- **ماذا / what:** فيديو الويب muted autoplay playsinline loop بصورة poster، وWebM مع بديل H.264، وفرع لمن يفضل تقليل الحركة. — Ship web video muted/playsinline/loop with a poster, WebM + H.264 fallback and a prefers-reduced-motion branch.
- **متى أستخدمها / when:** فيديو بطل في موقع أو صفحة هبوط — hero video on a site.
- **كيف / how:** Poster via -frames:v 1 is the LCP image; explicit width/height or aspect-ratio; stills as <picture> AVIF → WebP → JPEG at 3–5 widths; fetchpriority high on 1–2 hero images. Owner light profile (earth): WebP q80 at 1600/1200/900 widths, silent H.264 1280 w crf 27 -an +faststart (~1.8 MB of brand art, tested). **أرقام / params:** LCP ≤2.5 s · CLS <0.1 · INP <200 ms · WebP q80 · crf 27.
- **الدليل / proof:** `kosif-atlas/skills/2306-generative-web-media/8855-web-optimization-pipeline/SKILL.md` · `kosif-earth-ci-fork/tools/brand_art.test.mjs` · `kosif-earth-ci-fork/docs/design/HIGGSFIELD_VISUALS_ar.md`

#### FMT-30 · تسجيل المتصفح إلى MP4 وGIF بمرورين · Browser clip → MP4 + two-pass GIF · 🟢 جاهز / ready
- **ماذا / what:** سجّل حركة الواجهة بمقاس فيديو صريح، احتفظ بالـ WebM، حوّل إلى MP4، ولا تصنع GIF إلا إذا بقي التوقيت مفهومًا. — Record UI motion at an explicit video size, keep the WebM, convert to MP4, GIF only when timing survives.
- **متى أستخدمها / when:** ديمو واجهة سريع أو README — quick UI demos and READMEs (see UI).
- **كيف / how:** Playwright video:{mode:"on", size:{width:1280,height:820}} (Playwright + Chromium installed here); ffmpeg -vf scale=1280:-2 -c:v libx264 -pix_fmt yuv420p -crf 26 -preset veryfast -movflags +faststart -an; GIF fps=12,scale=960:-1:flags=lanczos,palettegen → paletteuse. **أرقام / params:** crf 26 · GIF 12 fps / 960 w.
- **الدليل / proof:** `kosif-atlas/skills/1530-webcraft/4196-ui-screenshots/references/clips.md`

## التصدير لكل منصة وحزم النشر — Per-platform exports & post packs

_ملف مفحوص لكل منصة، والحدود تُبلَّغ ولا تُقص بصمت — وأنت لا تنشر أبدًا بنفسك._

#### FMT-31 · ملف مفحوص لكل منصة · Checked per-platform delivery (8 platforms) · ✅ مُثبت هنا / proven here
- **ماذا / what:** ملف لكل منصة بنسبتها ومقاسها وسقف معدل البت، مع تقرير المدة والحجم دون قص صامت. — One checked file per platform at its ratio, size and bitrate ceiling; duration/size limits reported, never trimmed.
- **متى أستخدمها / when:** «جهزه لتيك توك وريلز وواتساب» — any multi-platform hand-off.
- **كيف / how:** `python3 scripts/kmotion.py platforms FILM.mp4 --out deliver --platforms tiktok,reels,shorts,youtube,x,whatsapp,linkedin,snapchat --mode smart|crop|blur --title …` → FILM_<platform>.mp4 + FILM.platforms.json (libx264 high, CRF 20, maxrate, faststart, AAC 48k). Verified here on a 6 s clip (tiktok/whatsapp/youtube + JSON with warnings) and by test_platforms_table. Limits are "as commonly published; verify at use". **أرقام / params:** tiktok 9:16 1080×1920 ≤600 s ≤287 MB 12000k/192k · reels ≤180 s ≤250 MB · shorts ≤180 s ≤256 MB · youtube 16:9 ≤2000 MB 16000k/256k · x 1280×720 ≤140 s ≤512 MB 8000k/160k · whatsapp 720×1280 ≤30 s ≤16 MB 2200k/96k · linkedin 1:1 1080 ≤600 s ≤200 MB 8000k · snapchat ≤60 s ≤32 MB 6000k/128k.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/platforms.py:28` · `100-superskills/skills/kosif-montage-motion/tests/test_v6.py:180` · `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:87`

#### FMT-32 · حزمة التسليم: كل النسب وغلاف وGIF · Delivery pack: all ratios + poster + GIF/WebP · ✅ مُثبت هنا / proven here
- **ماذا / what:** من ماستر واحد: نسخة لكل نسبة (بتأطير ذكي ومتوازي)، غلاف JPG بعنوان عربي اختياري، ومعاينة GIF وWebP، وملف export.json. — From one master: a reframed variant per ratio, a titled poster JPG, GIF/WebP previews and export.json.
- **متى أستخدمها / when:** نهاية كل مشروع — end of every job.
- **كيف / how:** `python3 scripts/kmotion.py export FILM.mp4 --out deliver --aspects 9:16,1:1,16:9 --title "…" --gif --webp` (kosif-studio `tools.py export … --poster 2.0 --mode smart --parallel 2`). Verified here: produced _9x16.mp4, _1x1.mp4, _poster.jpg, .gif and .export.json. **أرقام / params:** GIF 12 fps / 480 px / 160 colours / bayer scale 4 / 8 s · WebP 15 fps / 540 px / q70 / 8 s.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md` · `kosif-studio/motion/tools.py:378` · `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:84`

#### FMT-33 · حزمة نشر مفحوصة لكل منصة · Post pack + linter per platform · ✅ مُثبت هنا / proven here
- **ماذا / what:** يكتب الكابشن والوسوم وعنوان يوتيوب ووصفه والدعوة وأول تعليق ونص الغلاف والنص البديل، ثم يفحصها بحدود كل منصة وملاءمة الفيديو. لا ينشر. — Writes caption, hashtags, YouTube title/description, CTA, first comment, cover text and alt text, then lints them against each platform and the video fit. Never posts.
- **متى أستخدمها / when:** مع كل تسليم للسوشيال — with every social delivery.
- **كيف / how:** `python3 social.py pack FILM.mp4 --platforms tiktok,reels,shorts --topic "…" --out X.post.json` then `social.py check X.post.json` (exit 0 = ready). Lints: X weighted length (emoji 2, URL 23), YT title ≤100 (warn >70), hashtag caps (IG 5, YT >60 voids all, Threads 1), Arabic-normalised duplicate tags, hook before "more", dead links, CTA, alt text. Verified here: pack + check ran on a TikTok file (it flagged items as not ready — a draft to fill, not a final caption). Basma has the in-app version (5 Arabic hook titles ≤6 words, postPack JSON, POST_LIMITS) — needs its key-backed agent. **أرقام / params:** X 280 weighted · YT title ≤100 · IG 5 tags · Threads 1.
- **الدليل / proof:** `100-superskills/skills/kosif-social/scripts/social.py:165` · `kosif-one/tools/kosif-social/scripts/social.py:39` · `app/public/js/00_editor.js:2079`

#### FMT-34 · جدول حدود المنصات (2026-10) · Platform limits table (as of 2026-10) · ✅ مُثبت هنا / proven here
- **ماذا / what:** حدود الحروف والوسوم وما يظهر قبل «المزيد» والمدة والنسبة والكاروسيل لتسع منصات. — Caption, hashtag, visible-before-more, duration, ratio, size and carousel limits for nine platforms.
- **متى أستخدمها / when:** قبل كتابة أي نص نشر أو اختيار مدة — before writing copy or choosing length.
- **كيف / how:** `python3 social.py limits [--platform tiktok|reels|instagram|shorts|youtube|facebook|x|linkedin|threads]` (ran here; WhatsApp is not in this table — use platforms.py). Default posting slots (heuristic local time): tiktok 21:00, reels 20:00, instagram 13:00, shorts 18:00, youtube 17:00, facebook 19:00, x 12:00, linkedin 09:00, threads 12:00 — overridden by besttime. **أرقام / params:** tiktok 4000 chars/600 s/35 photos · reels 2200/5 tags/125 visible/180 s · IG 4:5 carousel 20 · FB 63206 · X 280/140 s/4 images · LinkedIn 3000/210 visible.
- **الدليل / proof:** `100-superskills/skills/kosif-social/scripts/social.py:39` · `100-superskills/skills/kosif-social/scripts/social.py:67` · `kosif-one/tools/kosif-social/scripts/social.py:35`

#### FMT-35 · خلطة الوسوم والخطاف · Hashtag mix & hook rules · 📄 موصوف / documented only
- **ماذا / what:** وسوم إنستغرام: عام + اثنان متخصصان + مكان + علامة؛ والعربية بلا تشكيل ولا تطويل وبشرطة سفلية؛ والخطاف يطابق أول ثانيتين. — IG tags 1 general + 2 niche + 1 place + 1 brand; Arabic tags without tashkeel/tatweel; hook matches the first 2 s.
- **متى أستخدمها / when:** كتابة نص النشر — writing the caption.
- **كيف / how:** Hook = number / result / question / contradiction that the first 2 s of video actually show; one CTA (save / share / comment word / follow); one punchy non-corporate share line for X/LinkedIn/Discord drafted in planning, finalised at delivery (brag). **أرقام / params:** max 5 tags · 1 CTA.
- **الدليل / proof:** `100-superskills/skills/kosif-social/references/copy-guide.md` · `kosif-one/vendor/brag/skills/brag/references/step-2-plan.md`

#### FMT-36 · خط إنتاج النسخ المترجمة · Localized versions pipeline · 📄 موصوف / documented only
- **ماذا / what:** نصوص الشاشة في كتالوج منفصل عن التايملاين، ورندر لكل لغة مع تبديل الاتجاه. — On-screen strings in a catalogue separate from the timeline; one render per locale with RTL/LTR switching.
- **متى أستخدمها / when:** نسخة عربية وإنجليزية من نفس الفيلم — the same film in ar + en.
- **كيف / how:** Scene JSON with string keys → per-locale renders; lock brand names in a glossary; validate placeholders/ICU before import; translation memory fuzzy 75–100% via XLIFF; re-fit text after translation (Arabic vs English length differs); pair with ARAB-08 content-language switch. **أرقام / params:** TM fuzzy 75–100%.
- **الدليل / proof:** `kosif-atlas/skills/2329-localization-i18n-engineering/8941-l10n-pipeline-and-tms/SKILL.md` · `kosif-atlas/skills/1802-content-multiplier/4838-channel-formats/SKILL.md`

#### FMT-37 · رندر دفعي بالمتغيرات · Variable-driven batch render · 📦 بأمر تثبيت / one install
- **ماذا / what:** مئات النسخ المخصصة (اسم، سعر، مدينة) من قالب واحد بصفوف متغيرات. — Many personalised outputs from one template, one row of variables each.
- **متى أستخدمها / when:** إعلانات مخصصة، شهادات، بطاقات تهنئة — personalised ads, certificates, greetings.
- **كيف / how:** `npx hyperframes render --batch rows.json --output "renders/{name}.mp4"` (cloud/lambda variants take JSONL); KOSIF equivalent: loop mtemplates.py `--set key=value` per row and render each.
- **تثبيت / install:** `npm i -D hyperframes@0.8.164`
- **رخصة / license:** Apache-2.0
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-cli/references/compare-and-batch.md` · `kosif-one/vendor/hyperframes/packages/cli/src/commands/batchRender.ts` · `100-superskills/skills/kosif-montage-motion/scripts/mtemplates.py:55`

#### FMT-38 · HyperFrames: صيغ وجودات الرندر · HyperFrames render formats & quality tiers · 📦 بأمر تثبيت / one install
- **ماذا / what:** التقاط حتمي للإطارات ثم ترميز ffmpeg إلى MP4/WebM/MOV/GIF/PNG/HLS بدرجات جودة. — Deterministic capture + ffmpeg encode to MP4/WebM/MOV/GIF/PNG/HLS with quality tiers.
- **متى أستخدمها / when:** مشاريع HyperFrames — HyperFrames compositions (see ENG).
- **كيف / how:** npx hyperframes render [--quality draft|looks|delivery] [--fps 24|30|60] [--format mp4|webm|mov|gif|png-sequence|hls] [--crf 0-51 | --video-bitrate 10M] [--workers auto] [--docker] [--strict]. Defaults 30 fps; looks = CRF 16; GIF ≤30 fps (15 preferred); HLS 4 s; ≈256 MB RAM per worker. For KOSIF HTML pages the in-repo path is `node tools/render_html.cjs` (proven by the proof films). **أرقام / params:** looks CRF 16 · GIF 15 fps · worker ≈256 MB.
- **تثبيت / install:** `npm i -D hyperframes@0.8.164`
- **رخصة / license:** Apache-2.0
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-cli/references/preview-render.md` · `kosif-one/vendor/hyperframes/packages/cli/src/commands/render.ts` · `kosif-tool/tools/render_html.cjs`

#### FMT-39 · مشاركة ورفع بلا نشر تلقائي · Share sheet & upload shortcuts (never auto-post) · 📦 بأمر تثبيت / one install
- **ماذا / what:** يشارك الملف عبر قائمة مشاركة النظام مع الكابشن، أو يفتح صفحات الرفع في تيك توك ويوتيوب وإنستغرام وفيسبوك؛ لا ينشر وحده. — Shares the file through the system share sheet with caption, or opens upload pages; never posts by itself.
- **متى أستخدمها / when:** المستخدم على الهاتف ويريد الرفع فورًا — user on phone ready to upload.
- **كيف / how:** Basma share(): navigator.share({files,title,text}); links tiktok.com/upload, youtube.com/upload, instagram.com, facebook.com/reels/create.
- **تثبيت / install:** `cd app && npm install`
- **الدليل / proof:** `app/public/js/50_autoedit.js:1336`

#### FMT-40 · إرسال الفيلم على واتساب · WhatsApp media delivery container · 🔑 مفتاح أو خدمة / needs key or paid service
- **ماذا / what:** خدمة Node تربط حساب واتساب وترسل نصًا أو صورًا أو فيديو أو صوتًا أو مستندًا لرقم. — Node service that links a WhatsApp account and sends text, images, video, audio or documents to a number.
- **متى أستخدمها / when:** عندما يريد المستخدم استلام الريل على واتساب ويربط حسابه — only with the user’s linked account.
- **كيف / how:** kosif-audit-studio/whatsapp-container-v2: `npm install` then routes /connect (QR link), /status, /send, /send-media, /send-bundle; mimetype prefix picks message type; audio goes with ptt false. Needs the owner to scan the link QR — a personal account, not an API key. **أرقام / params:** max media 25 MB · ptt false.
- **الدليل / proof:** `kosif-audit-studio/whatsapp-container-v2/server.mjs:9` · `kosif-audit-studio/whatsapp-container-v2/server.mjs:147`

#### FMT-41 · روابط خاصة مستضافة وعمليات Cloudinary · Hosted private links & Cloudinary URL ops · 🔑 مفتاح أو خدمة / needs key or paid service
- **ماذا / what:** رفع المشروع إلى رابط خاص ثابت، أو اشتقاق نسخ الفيديو من الرابط (قص، كتم، حد مقاس، WebP متحرك) في Cloudinary. — Publish a project to a stable private URL, or derive video variants by URL in Cloudinary.
- **متى أستخدمها / when:** عندما يملك المستخدم الحساب — only with the account.
- **كيف / how:** `npx hyperframes publish [dir]` (hosted, republish updates the same link). Cloudinary: so_/eo_/du_ trim, ac_none for autoplay, c_limit,h_720, fps_, fl_splice, f_auto:animated previews — e.g. du_5/vc_auto/f_auto:video/q_auto. Both need accounts; locally use ffmpeg and the claude.ai artifact (FMT studio cloud) instead.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-cli/references/preview-render.md` · `kosif-atlas/skills/1119-cloudinary/2560-cloudinary-transformations/references/video-transformations.md`

#### FMT-42 · استوديو كامل كصفحة claude.ai واحدة · KOSIF Studio Cloud — one-page artifact · ✅ مُثبت هنا / proven here
- **ماذا / what:** يحزم محرر الاستوديو كله في صفحة HTML مستقلة تعمل كـ artifact بلا خادم، والحفظ عبر قدرة التنزيل. — Bundles the whole Studio editor into one self-contained HTML page that runs as a claude.ai artifact; saves go through the downloads capability.
- **متى أستخدمها / when:** المستخدم بلا حاسوب ويريد محررًا يصدّر MP4 من المتصفح — user on claude.ai only.
- **كيف / how:** `python3 scripts/web/build_studio_cloud.py --out studio-cloud.html --home-url URL`: modules wrapped in IIFEs, imports rewritten, mp4-muxer@5.2.1 from cdn.jsdelivr.net, download() → window.claude.use("downloads").save(); save errors mapped (declined, too_large, rate_limited, rejected_extension). Verified here: built a 78,544-byte page. **أرقام / params:** ≈78.5 KB page · mp4-muxer 5.2.1.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/build_studio_cloud.py:1` · `100-superskills/skills/kosif-montage-motion/scripts/web/build_studio_cloud.py:45`

#### FMT-43 · حزم المساعدات الأخرى وغلاف JSON · Custom GPT / Claude Project packs & JSON envelope · 📄 موصوف / documented only
- **ماذا / what:** تعليمات جاهزة و12 ملف معرفة وبدايات محادثة عربية وOpenAPI، وشكل JSON لتطبيقات AI Studio الخاصة بالمستخدم. — Ready instructions, 12 knowledge files, Arabic conversation starters and OpenAPI; a JSON answer envelope for the user’s own AI Studio apps.
- **متى أستخدمها / when:** المستخدم يريد نقل القدرات إلى GPT أو مشروع Claude — exporting the toolkit to other assistants.
- **كيف / how:** Paste chatgpt/custom-gpt/instructions.md (3,999/8,000 chars), upload knowledge/*.md, import openapi.json with a Bearer token (29 action tools; MCP 65); Claude Project uses claude/project-instructions.md. JSON envelope only when the app parses JSON: {title, analysis, confidence, sources, json:{tool_output,prompts,imageSpecs}, nextSteps, qualityScore{…}} with per-platform {platform, prompt, negativePrompt, params{aspect}, audioDirection}.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/chatgpt/custom-gpt/SETUP.md` · `kosif-one/tools/kosif-omni/skills/kosif-cinema-director/references/response-formats.md`

## الأغلفة والصور المصغرة والأصول الثابتة — Thumbnails, covers & static assets

_الغلاف ليس أسود أبدًا، والنص فوقه حقيقي ومشكّل — لا يكتبه مولّد الصور._

#### FMT-44 · الغلاف كإطار أول · Poster picked and baked as frame 0 · ✅ مُثبت هنا / proven here
- **ماذا / what:** يُختار إطار قوي مستقر (لا الرأس أو الذيل الأسود) ويُثبَّت كإطار أول حتى لا تظهر الصورة المصغرة سوداء، مع بقاء عدد الإطارات والصوت. — Pick a strong settled still (never the black head/tail) and bake it into frame 0 so thumbnails are not black; frame count and audio unchanged.
- **متى أستخدمها / when:** كل فيلم يبدأ بإظلام أو دخول تدريجي — every film that fades in.
- **كيف / how:** `python3 scripts/poster.py FILM --at 3.2 --bake` or poster.pick → extract → bake; brag recipe: overlay on the first frame only, -c:a copy (1/30 s at 30 fps). Verified by test_poster_pick_and_bake here. **أرقام / params:** 1 frame · audio copied · frame count unchanged.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_launch.py:89` · `100-superskills/skills/kosif-montage-motion/scripts/poster.py` · `kosif-one/vendor/brag/skills/brag/references/step-4-deliver.md`

#### FMT-45 · اختيار إطار الغلاف آليًا · Thumbnail candidate picking · 🟢 جاهز / ready
- **ماذا / what:** اسحب عينات من الفيديو كله، استبعد الفارغ والضبابي والانتقالات، ورشّح لحظات مختلفة تُظهر الموضوع أو النتيجة. — Sample the whole video, drop blank/blurred/transition frames, shortlist distinct moments showing subject or result.
- **متى أستخدمها / when:** فيديو خام بلا تصميم غلاف — raw footage that needs a cover.
- **كيف / how:** ffmpeg -vf "select='gt(scene,0.3)',scale=640:-1" -vsync vfr, or thumbnail=n=100; score with numpy Laplacian variance (sharpness), face presence, contrast, placement; tile a contact sheet; when the piece is a composition, render the chosen moment natively. Animated cover = gentle loop with matching ends. YouTube bulk custom thumbnails ≲100 per channel per 24 h. **أرقام / params:** scene > 0.3 · thumbnail n=100 · ≤~100 uploads/24 h.
- **الدليل / proof:** `kosif-atlas/skills/101-video-skills/222-video-thumbnails/SKILL.md` · `kosif-atlas/skills/932-vidseeds/2178-vidseeds/skills/vidseeds-local-video/SKILL.md`

#### FMT-46 · غلاف بعنوان عربي من الفيلم · Arabic-titled cover from a film frame · 🟢 جاهز / ready
- **ماذا / what:** يلتقط إطارًا عند ثانية محددة ويكتب عليه عنوانًا عربيًا مشكّلًا كصورة غلاف. — Grab a frame at a chosen second and write a shaped Arabic title on it.
- **متى أستخدمها / when:** غلاف ريل أو يوتيوب سريع — quick reel/YouTube cover (shaping per ARAB-59).
- **كيف / how:** `python3 scripts/kmotion.py thumb FILM --at 2 --text "…" --out cover.jpg` (studio recipe "thumb"); text is shaped by Pillow RAQM here. For designed thumbnails compose HTML/CSS and screenshot with Playwright at 1280×720. **أرقام / params:** --at seconds · 1280×720 for YouTube.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:90`

#### FMT-47 · بريف الصورة المصغرة: 3 أفكار واختبار A/B · Thumbnail brief: 3 concepts + A/B · 📄 موصوف / documented only
- **ماذا / what:** ثلاثة مفاهيم (تخطيط، تعبير، موضع النص، اللون، عناصر العلامة) مع توصية وخطة اختبار. — Three concepts with a recommendation, background-only image prompts, shooting notes and an A/B plan.
- **متى أستخدمها / when:** قناة يوتيوب أو حملة — channels and campaigns.
- **كيف / how:** Shooting notes: slightly below eye level, medium close-up, one off-axis key light. Generate backgrounds without text (prompt template: subject with exaggerated emotion, high contrast, bold rim light, clean background, space on the right for title, 16:9) and composite the real face and the Arabic title as layers. A/B: vary one element, judge after 48 h by CTR vs channel average. **أرقام / params:** 3 concepts · 1280×720 · 48 h test.
- **الدليل / proof:** `kosif-atlas/skills/3067-youtube/13228-creator-thumbnail-agent/SKILL.md` · `kosif-one/tools/kosif-omni/skills/kosif-image-studio/references/prompt-library.md`

#### FMT-48 · كلمات الغلاف وتكامله مع العنوان · Thumbnail word limits & title pairing · 📄 موصوف / documented only
- **ماذا / what:** نص الغلاف 1–3 كلمات (4 حد أقصى)، ولون إبراز واحد، ولا تكرر أي كلمة من العنوان. — Thumbnail copy 1–3 words (4 max), one accent colour, and zero words shared with the title.
- **متى أستخدمها / when:** كتابة نص الغلاف والعنوان — writing cover text + title.
- **كيف / how:** Must read in under 1 s at 150–200 px width; for Arabic count words not letters, heavy weights, no tracking. Title ≤60 chars with the key words in the first ~40; check overlap with a set intersection; produce 3 pairs at different angles (curiosity / benefit / identity). Basma cover text 2–4 words. **أرقام / params:** 1–3 words · title ≤60 chars · 0 shared words.
- **الدليل / proof:** `kosif-atlas/skills/1520-digital-marketing-pro/4132-video-packaging/SKILL.md` · `kosif-atlas/skills/1817-youtube-strategy/4868-yt-packaging/SKILL.md`

#### FMT-49 · غلاف طباعي للروابط OG · Typography-first OG / cover image · 📄 موصوف / documented only
- **ماذا / what:** أغلفة وبطاقات روابط HTML+CSS تُصوَّر بالضبط 1200×630، بعنوان ≈40 حرفًا وخطين كحد أقصى. — Covers and link previews as HTML+CSS screenshots at exactly 1200×630, title ≈40 chars, ≤2 fonts.
- **متى أستخدمها / when:** مقالات، صفحات هبوط، منشورات لينكدإن — articles and link posts.
- **كيف / how:** Playwright screenshot of a fixed-size body with overflow hidden; direction by topic (technical = dark + accent gradients, tutorial = light and structured, conceptual = centred gradient type). Same approach yields 1280×720 thumbnails and 1080×1350 posts. **أرقام / params:** 1200×630 · ≤40 chars · ≤2 fonts.
- **رخصة / license:** WTFPL folder in the atlas x* area — permissive, idea only.
- **الدليل / proof:** `kosif-atlas/skills/x4919-visual-gen/x20318-cover-image/SKILL.md`

#### FMT-50 · حزمة أصول الهوية الرقمية · Identity export set: favicon, PWA, OG · 🟢 جاهز / ready
- **ماذا / what:** أقل مجموعة تصدير للهوية: favicon.svg وico، أيقونات التثبيت، وصور OG وX. — Minimum identity export: favicon.svg/ico, install icons, OG and X cards.
- **متى أستخدمها / when:** تسليم شعار أو هوية — logo/identity hand-off (see BRAND).
- **كيف / how:** favicon.svg (dark via media query), favicon.ico 16/32/48, apple-touch 180×180, PWA 192/512, OG 1200×630, X 1200×675; render with headless Chromium or Pillow. Owner examples: earth tools/brand/make_marks.py renders icons from the SVG mark with theme_color #1d1814 (identity_unity test); audit-studio Arabic RTL manifest (lang ar, dir rtl, standalone, SVG any/maskable icons, theme #24113f). **أرقام / params:** 16/32/48 · 180 · 192/512 · 1200×630 · 1200×675.
- **الدليل / proof:** `kosif-atlas/skills/2248-brand-identity-studio/8557-brand-book-assembly` · `kosif-earth-ci-fork/tools/brand/make_marks.py` · `kosif-earth-ci-fork/tools/identity_unity.test.mjs` · `kosif-audit-studio/manifest.webmanifest`

#### FMT-51 · تصدير الرسوم PNG@2x وSVG · Chart export PNG@2x / SVG + data-table toggle · 🟢 جاهز / ready
- **ماذا / what:** كل رسم ينزّل نفسه SVG أو PNG مضاعف الدقة بالعنوان والمفتاح، ويتحول لجدول بيانات. — Every chart downloads itself as SVG or 2× PNG with legend/title baked in and toggles to its data table.
- **متى أستخدمها / when:** تسليم صور ثابتة من مشهد بيانات — stills from a data scene (DATA).
- **كيف / how:** exportFig(fig, fmt): resolve CSS var colours with getComputedStyle, serialise SVG, draw into a canvas at k=2, canvas.toBlob("image/png"); fall back to SVG on error; PRINT_CSS hides tools. **أرقام / params:** scale 2×.
- **الدليل / proof:** `kosif-earth-ci-fork/ui/components/charts.js:184` · `kosif-earth-ci-fork/ui/components/charts.js:247`

#### FMT-52 · تصدير SVG وأوضاع الاستوديو الرسام · Painter studio export modes (PNG · 4K · SVG · MP4) · 🟢 جاهز / ready
- **ماذا / what:** من صورة واحدة: PNG، نسخة مطابقة، 3840×2560، SVG متتبَّع بطبقات اللون، برنامج بايثون، وفيلم MP4 للرسم. — From one picture: PNG, exact copy, 3840×2560 render or Lanczos enlargement, traced SVG, a Python program and an MP4 of the drawing.
- **متى أستخدمها / when:** تحويل رسم أو شعار نقطي إلى أصول قابلة للتحرير — vectorising art/logos.
- **كيف / how:** Toolbar التصدير: 💾 PNG (Ctrl+S), ⤢ high-res (3840×2560, scale 3.2, ss=2), 📤 image code, 🎬 film (30 fps H.264); vectorize.to_svg(data, path, scale) writes one even-odd path per colour (scale 2 from the window, 4 from --trace). **أرقام / params:** 3840×2560 · SVG scale 2/4 · MP4 30 fps.
- **الدليل / proof:** `kosif-studio/studio.py:1275` · `kosif-studio/vectorize.py:247` · `kosif-studio/out/aghnam_logo.svg`

#### FMT-53 · مخرجات الطباعة والمستندات · Print & document outputs · 🟢 جاهز / ready
- **ماذا / what:** الطباعة تخفي الأدوات وتفرض خلفية بيضاء ولوحة تراثية فاتحة، وتقارير بشكل ورقة، وإيصالات حرارية 80 مم بـ QR. — Print hides chrome and forces a light heritage palette; paper-style report previews; 80 mm thermal receipts and 60×40 mm labels with QR.
- **متى أستخدمها / when:** المستخدم يريد نسخة مطبوعة أو PDF من مشروع — print/PDF deliverables.
- **كيف / how:** @media print: hide topbar/rails, panels break-inside:avoid, no shadows, body 11pt/1.6; earth print lock: ink #2b1a0f, brand #8a5a2b, Amiri / Noto Naskh / Aref Ruqaa. Paper preview: .paper bg #fcfbf7, padding 64px clamp(28px,6vw,78px), shadow 0 22px 60px #0008, brand header 800 weight / 3px tracking (Latin only) #5b376d. Receipts: qrcode.js with CorrectLevel.M, TLV invoice data. **أرقام / params:** 11pt/1.6 · 80 mm receipt · 60×40 mm label · QR ECC M.
- **الدليل / proof:** `kosif-earth-ci-fork/ui/ds/tokens.css:446` · `kosif-audit-pro/app/globals.css:3133` · `kosif-audit-studio/continuous-review.css:1` · `kosif-earth-ci-fork/ui/features/enterprise.js:246`

#### FMT-54 · المستند إلى عرض شرائح · Document → slideshow / interactive deck · 🟢 جاهز / ready
- **ماذا / what:** أي تقرير يتحول لشرائح ملء الشاشة: شريحة عنوان متدرجة ثم شريحة لكل قسم، بتنقل بالكيبورد. — Any generated report becomes full-screen slides: gradient title slide, one slide per h1/h2, keyboard navigation.
- **متى أستخدمها / when:** «اعمله عرض» من نص موجود — turning a document into a deck.
- **كيف / how:** earth SK.output present(): slidesOf(doc) splits at headings; title slide linear-gradient(135deg,#0b1030 0%,#2a3fae 60%,#2340c4 100%); title clamp(22px,4vw,44px) 800. HyperFrames slideshow skill adds fragments, hotspots, branching sequences and presenter notes (npm install needed). **أرقام / params:** padding clamp(12px,3vw,40px) clamp(12px,4vw,56px).
- **الدليل / proof:** `kosif-earth-ci-fork/ui/core/output.js:228` · `kosif-one/vendor/hyperframes/skills/slideshow/SKILL.md`

## قوالب السوشيال وإيقاع الإعلانات — Social formats, ad slots & platform blocks

_كل خانة إعلانية تفرض هيكلًا؛ وكل مقطع قصير يمر باختبار «هل يقف وحده؟»._

#### FMT-55 · فيزياء خانات الإعلان · Ad-slot structure physics · 📄 موصوف / documented only
- **ماذا / what:** 6 ث = رسالة واحدة والعلامة ظاهرة بالثانية 2؛ 15 ث قابل للتخطي = الخطاف قبل زر التخطي عند 5 ث؛ 30 ث = قوس واحد يدفع مبكرًا ومتأخرًا. — 6 s bumper: one message, brand by 2 s; 15 s skippable: hook + core before the 5 s skip; 30 s: one arc, pay off early and late.
- **متى أستخدمها / when:** أي إعلان مدفوع — any paid ad.
- **كيف / how:** Template each length as a fixed timeline grid (markers at 2 s, 5 s, end card) and verify message placement on rendered stills at those times. Platform pacing (kosif-tool ads playbook): TikTok/Reels 9:16 15–30 s with cuts every 1–2 s; YouTube pre-roll key message before 5 s; feeds 1:1/4:5; ad structure hook 0–1.5 s, features 2–3 s each, CTA 2–3 s, logo 1–1.5 s. **أرقام / params:** 6 / 15 / 30 s · markers 2 s, 5 s · cuts 1–2 s.
- **الدليل / proof:** `kosif-atlas/skills/1520-digital-marketing-pro/4133-video-script/SKILL.md` · `kosif-tool/playbooks/ads.md:30`

#### FMT-56 · نسخ مختصرة ومطولة من نص واحد · Alternate cut-downs (60/30/15 s) · 📄 موصوف / documented only
- **ماذا / what:** علّم كل نبضة بأولوية (أساسي/اختياري) لتتولد النسخ القصيرة بالتصفية وإعادة التدفق. — Tag each beat core/optional so cut-downs are generated by filtering beats and re-flowing the timeline.
- **متى أستخدمها / when:** حملة تحتاج 60 و30 و15 ثانية — campaigns in several lengths.
- **كيف / how:** Timeline/storyboard JSON beats with priority; regenerate 30 s and 15 s by dropping optional beats and re-timing to the same audio grid; re-check each version’s hook and CTA.
- **الدليل / proof:** `kosif-atlas/skills/1520-digital-marketing-pro/4133-video-script/SKILL.md`

#### FMT-57 · تفتيت المحتوى الطويل · Content atomisation map · 📄 موصوف / documented only
- **ماذا / what:** مصدر طويل واحد ← فيديو كامل + 3–5 مقاطع قصيرة + نسخ أصلية لكل منصة، بإصدار متدرج. — One long source → full video + 3–5 shorts + platform-native variants, released staggered.
- **متى أستخدمها / when:** بودكاست، ويبينار، مقال — podcast, webinar, article (see STORY).
- **كيف / how:** Blog→video: H2s → chapters, stats/quotes → pull-quote overlays on B-roll, steps → tutorial segments, conclusion → short. Every derivative passes the standalone test (own hook and payoff, no "as discussed…"); list what was cut and why; channel specs: short video = 80–150 spoken words for 20–45 s, 3–5 beats each with an on-screen text cue, one CTA; YouTube description 200–500 words, first ~100 chars above the fold. **أرقام / params:** 3–5 clips per long piece · 80–150 words / 20–45 s.
- **الدليل / proof:** `kosif-atlas/skills/1520-digital-marketing-pro/4013-content-repurpose/SKILL.md` · `kosif-atlas/skills/1802-content-multiplier/4838-channel-formats/channels/short-video.md`

#### FMT-58 · مواصفات التريلر حسب المنصة · Trailer platform targets · 📄 موصوف / documented only
- **ماذا / what:** أطوال ومقاسات التريلر لكل منصة، والصامت يحمل رسالته بالترجمة. — Trailer lengths/specs per platform; muted autoplay means captions carry the message.
- **متى أستخدمها / when:** تريلر لعبة أو منتج أو فيلم — trailers.
- **كيف / how:** X/Bluesky/Mastodon 30–45 s 16:9 1080p60, hook within 2 s; YouTube 30–90 s; Shorts/TikTok/Reels 15–45 s native 9:16 with a big subject; README/Discord GIF loops 4–8 s at 640 px, 20 fps, <15 MB; store pages 60–120 s. Render native 9:16 rather than cropping when possible. **أرقام / params:** 30–45 · 30–90 · 15–45 s · GIF 4–8 s 640 w 20 fps <15 MB.
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4173-game-trailer/references/concept-and-music.md`

#### FMT-59 · فصول يوتيوب من العلامات · YouTube chapters from markers · ✅ مُثبت هنا / proven here
- **ماذا / what:** أول فصل عند 00:00، ثلاثة فصول على الأقل بفارق ≥10 ث، بأسماء أماكن أو أحداث قابلة للبحث. — First chapter at 00:00, ≥3 chapters ≥10 s apart, searchable names; also muxed as MP4 chapters.
- **متى أستخدمها / when:** فيديو يوتيوب طويل أو درس — long YouTube videos, lessons.
- **كيف / how:** Write the "mm:ss Name" list (hh:mm:ss past 60 min) for the description; mood words belong in captions, not chapters. To embed: ffmetadata [CHAPTER] blocks (TIMEBASE=1/1000, START, END, title=…) then ffmpeg -i in -i ch.txt -map_metadata 1 -map_chapters 1 -c copy. Verified here with Arabic titles read back by ffprobe -show_chapters. **أرقام / params:** ≥3 chapters · ≥10 s apart · first 00:00.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2465-davinciresolve-subtitle-travelnote/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2445-akbun-davinciresolve-workflow/SKILL.md`

#### FMT-60 · بنية الكاروسيل وحدوده · Carousel structure & limits · 🟢 جاهز / ready
- **ماذا / what:** الشريحة الأولى خطاف يعمل وحده، الثانية جسر، فكرة لكل شريحة، والأخيرة ملخص ودعوة؛ أقل من 5 = منشور واحد. — Slide 1 hooks alone, slide 2 bridges, one point per slide, last slide recap + CTA; under 5 slides → single post.
- **متى أستخدمها / when:** كاروسيل إنستغرام/لينكدإن أو تحويله لريل — carousels, or a carousel animated into a reel.
- **كيف / how:** Instagram 5 min / 8–10 ideal, LinkedIn PDF 7–12, Facebook 5–8, all 1080×1350; title ≤8 words, body ≤30 words; reserve 80 px outer edge for pager; one progress signal (counter, bar or colour progression); one slide component with variants (cover, content, data, contrast, closing). Render with the Arabic carousel tool (ARAB-60: `social.py carousel spec.json --out DIR` → PNG + PDF + contact sheet). The same slide system animates into a 9:16 reel, one slide per beat. **أرقام / params:** 1080×1350 · title ≤8 w · body ≤30 w · 80 px edge.
- **الدليل / proof:** `kosif-atlas/skills/2976-pwdev-social-media/12581-carousel-builder/SKILL.md` · `kosif-one/tools/kosif-social/SKILL.md` · `kosif-one/tools/kosif-social/examples/carousel.json`

#### FMT-61 · افتتاحيات وخواتيم سوشيال عربية (MG-061…070) · Arabic social openers & closers (MG-061…070) · 📄 موصوف / documented only
- **ماذا / what:** وصفات موقوتة: ثلاث بطاقات سريعة، سؤال يشق الشاشة، ثلاث نصائح بشريط تقدم، النتيجة أولًا، مقارنة بنصفين عادلين، ودعوة واحدة. — Timed recipes: three quick cards, question that splits the screen, three tips with progress, result-first, fair vertical split, one clear CTA.
- **متى أستخدمها / when:** ريلز تعليمية وترويجية قصيرة — short explainer/promo reels.
- **كيف / how:** MG-061: cards 0–0.9 / 0.9–1.8 / 1.8–2.7 s, topic 2.7–4 s, mask reveal per word. MG-062: question 0–1.5, split 1.5–2.5, answer 2.5–5 s (two masked frame copies move vertically). MG-063: tips 0–4/4–8/8–12 s, corner number, real progress bar. MG-066: result 0–2, shrink 2–3, steps 3–8, back 8–10 s. MG-067: labels 0–1, compare 1–6, summary 6–8 s with equal area, light and speed. MG-070: last shot shrinks 0–1 s, one CTA 1–4 s, never a fake tappable button. **أرقام / params:** 4 · 5 · 12 · 10 · 8 · 4 s.
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-social-clips.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### FMT-62 · حلقة متصلة بلا قطع · Seamless loop (video + GIF) · ✅ مُثبت هنا / proven here
- **ماذا / what:** العنصر الخارج في النهاية يدخل في البداية بنفس الموضع والسرعة، أو تذوب النهاية في البداية، ثم GIF بلوحة متكيفة. — The exiting element re-enters at the same position and speed, or the tail cross-fades into the head; then an adaptive-palette GIF.
- **متى أستخدمها / when:** خلفيات، ملصقات، GIF للـ README أو ديسكورد — loops, stickers, README GIFs.
- **كيف / how:** Author a timeline where t=D equals t=0 and export frames 0..N−1 only; check with ffmpeg -stream_loop and a frame diff (brief: first/last identical, final hold only a 2% opacity breathe). Cross-fade variant: xfade=fade:duration=0.4:offset=D−0.8. GIF: palettegen=stats_mode=diff:max_colors=192, paletteuse=dither=sierra2_4a:diff_mode=rectangle, -loop 0; over budget → width 480 → fps 15 → 128 colours → shorter. Verified here: 6 s, 480 px, 15 fps, 128 colours ≈1.0 MB. **أرقام / params:** ≈6 s · <15 MB (X/Discord) · 128–192 colours.
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4173-game-trailer/references/assembly-and-review.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-loops-backgrounds.md` · `kosif-tool/styles/pm-listudio-820c7b/BRIEF.md`

#### FMT-63 · قالب بطاقة الختام · End-card template · ✅ مُثبت هنا / proven here
- **ماذا / what:** دعوة ومعرّف حساب وثلاث أيقونات تفاعل متتابعة وزر اشتراك ينضغط مرتين وشريط تقدم. — CTA, handle, three staggered social icons, subscribe pill that squashes twice and a linear progress bar.
- **متى أستخدمها / when:** آخر 4–6 ثوانٍ في أي ريل — the last seconds of any reel.
- **كيف / how:** `python3 scripts/mtemplates.py new NAME --template end-card --set cta="تابعنا للمزيد" --set handle=@kosif [--seconds 6 --size 1080x1920]` → projects/NAME/index.html (+fonts, gsap, motion-kit); render with motion.py. Verified by test_every_template_generates_and_lints. **أرقام / params:** 6 s · accent #E7B65A · bg #1b2a49 → #0d1b2a · bar linear over D−0.4 s.
- **رخصة / license:** Uses GSAP — standard "no charge" licence, not MIT.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/templates/motion/end-card.html` · `100-superskills/skills/kosif-montage-motion/scripts/mtemplates.py:55` · `100-superskills/skills/kosif-montage-motion/tests/test_v6.py`

#### FMT-64 · ختام تحميل التطبيق وشارات المتاجر · App end card & store badges · 📦 بأمر تثبيت / one install
- **ماذا / what:** أيقونة واسم وسطر وصف وزر دعوة داكن مستدير وصف مزايا؛ أو عنوان قصير فوق شارتي App Store وGoogle Play. — Icon, wordmark, descriptor, dark rounded CTA pill and feature row; or a headline over equal App Store / Google Play badges.
- **متى أستخدمها / when:** إعلان تطبيق — app promos.
- **كيف / how:** Seen in style:pm-mehul4795-4a7007 (9:16, pale lavender #eceffa, CTA pill radius 24 px, features separated by red dots, small "BY …" credit). Registry block: `npx hyperframes add store-badge-lockup`, mount on a .clip div with data-composition-src/data-start/data-duration and data-variable-values (headline, showApple, showGoogle); extra duration becomes hold, never time-stretch. Square muted app ad brief: icon + name fully visible by 300 ms, last 500 ms frozen for the thumbnail, 80 px margin, text ≥48 px, headline ≥96 px. **أرقام / params:** pill r 24 px · visible by 300 ms · hold last 500 ms.
- **تثبيت / install:** `npm i -D hyperframes@0.8.164`
- **رخصة / license:** Apache-2.0
- **الدليل / proof:** `style:pm-mehul4795-4a7007` · `kosif-one/vendor/hyperframes/registry/components/store-badge-lockup/store-badge-lockup.html` · `kosif-tool/styles/pm-cansincengiz-me-cf68dd/BRIEF.md`

#### FMT-65 · بطاقات المنصات المتحركة · Animated platform cards (follow, post, comment, now-playing) · 📦 بأمر تثبيت / one install
- **ماذا / what:** بطاقات بشكل المنصات: متابعة تيك توك وإنستغرام وإكس، منشور إكس وريديت، تعليقات يوتيوب، شريط اشتراك، إشعار ماك، وبطاقة «يُشغَّل الآن». — Platform-style overlays: TikTok/Instagram/X follow, X and Reddit posts, YouTube comments, subscribe lower third, macOS notification, now-playing card.
- **متى أستخدمها / when:** ريل يذكر حسابًا أو تعليقًا أو أغنية — reels quoting accounts, comments or songs.
- **كيف / how:** `npx hyperframes add tiktok-follow | instagram-follow | x-follow-card | x-post | reddit-post | yt-comment-card | yt-lower-third | macos-notification | spotify-card` → compositions/<name>.html (inline SVG + paused GSAP 3.14.2 timeline). Sizes: follow cards 1080×1920 4.5 s, posts/notification 1920×1080 5 s, comments 8 s, lower third elastic.out(1,0.4) 4.5 s. Swap DM Sans/Inter for an Arabic face (ARAB-11) and set text direction per element. Use fictional handles or the user’s own — never impersonate real accounts. **أرقام / params:** 4.5–8 s · 1080×1920 / 1920×1080.
- **تثبيت / install:** `npm i -D hyperframes@0.8.164`
- **رخصة / license:** Apache-2.0 registry; GSAP inside uses its standard licence.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/tiktok-follow/tiktok-follow.html` · `kosif-one/vendor/hyperframes/registry/blocks/x-post/x-post.html` · `kosif-one/vendor/hyperframes/registry/blocks/yt-comment-card/yt-comment-card.html` · `kosif-one/vendor/hyperframes/registry/blocks/spotify-card/spotify-card.html`

#### FMT-66 · سؤال خطاف مع عدّاد حي · Hook question + live counter overlay · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** سؤال ثابت عريض في الثلث الآمن العلوي، تحته عدّاد يتحدث مع الأحداث، وتعليمة صغيرة في الأسفل الآمن، وكبسولة «شغّل الصوت» أول 3 ث. — Fixed bold question in the top safe zone, a counter beneath that updates on events, tiny instruction at the bottom, a "sound on" pill for 3 s.
- **متى أستخدمها / when:** تحديات، ألعاب، تجارب «كم مرة…» — challenge and counting reels.
- **كيف / how:** Question in the top 12–20% of 9:16; counter as tabular digits updated on event times (ARAB-73); "sound on" pill fades at 3 s; vertical ad variant puts the headline in the top third. **أرقام / params:** top 12–20% · pill 0–3 s.
- **الدليل / proof:** `style:pm-kantamk-61f410` · `style:pm-francoxavier33-d2dfd2`

#### FMT-67 · إعلان مربع للخلاصة · Square feed promo · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** إعلان 1:1 مقروء بلا صوت، الكلام في الأعلى أو كتلة نص أعلى اليسار. — 1:1 promo legible without sound, captions on top or a top-left text block.
- **متى أستخدمها / when:** منشورات الخلاصة ولينكدإن — feed and LinkedIn posts.
- **كيف / how:** 1080×1080 (or 720×720 draft), captions top, text block top-left (top-right for Arabic), 80 px margins, product/hero bottom two-thirds; e-commerce ad structure: hook 0–1.5 s, promise, 2–4 feature beats 2–3 s, price card spring (damping 14, stiffness 180), CTA 2–3 s, logo 1–1.5 s, product ≥40% of frame height (`kosif.py scaffold ecommerce-ad <dir>`). **أرقام / params:** 1080×1080 · 80 px · product ≥40% height.
- **الدليل / proof:** `style:pm-cansincengiz-me-cf68dd` · `style:pm-rammanq-f5a90f` · `kosif-tool/styles/ecommerce-ad/SKILL.md` · `kosif-tool/playbooks/ads.md`

#### FMT-68 · أمثلة بريفات جاهزة · Ready example briefs · 🟢 جاهز / ready
- **ماذا / what:** ثلاث بريفات جاهزة: «رحلة الإبداع» دودل 9:16 30 ث، إطلاق منتج 16:9 20 ث، «الشرح بطريقة الرسم» سبورة 9:16 45 ث. — Three ready briefs: doodle 9:16 30 s (ar-EG), product launch 16:9 20 s (en), whiteboard 9:16 45 s (ar).
- **متى أستخدمها / when:** بداية سريعة لمشروع Fastify — fast start in Fastify Motion Bro.
- **كيف / how:** Copy into project/brief.json and run `npm run plan`; deliverable = H.264 yuv420p +faststart CRF 19 MP4 + editable source, brief, storyboard and QA receipt (AGENTS.md step 9).
- **الدليل / proof:** `fastify-motion-bro/examples/demo-9x16.json` · `fastify-motion-bro/examples/whiteboard-ar.json` · `fastify-motion-bro/AGENTS.md:17-18`

#### FMT-69 · مهارات تسويق مساندة · Supporting marketing skills (store, newsletter, SEO) · 📄 موصوف / documented only
- **ماذا / what:** مهارات المالك للمتاجر والنشرات البريدية وهيكلة المحتوى للبحث — تخطيط مساند للفيديو لا أكثر. — Owner skills for e-commerce listings, newsletters and SEO architecture — planning support only.
- **متى أستخدمها / when:** الفيديو جزء من حملة أوسع — the video is part of a wider campaign.
- **كيف / how:** Load the skill (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/ecommerce-store-listings/SKILL.md` · `100-superskills/skills/newsletter-email-marketing/SKILL.md` · `100-superskills/skills/seo-content-architecture/SKILL.md`

## توليفات قوية / power combos

- **ريل من فيديو أفقي / landscape → reel:** FMT-13 (smart) + FMT-14 (blur fill للقطات الشاشة) + FMT-01 + ARAB-62 (كاريوكي) + FMT-31 (ملف لكل منصة) — الوجه يبقى في الكادر، والترجمة في المنطقة الآمنة، ثم نسخ tiktok/reels/shorts بتقرير حدود.
- **تسليم كامل لعميل / full client hand-off:** FMT-32 + FMT-33 + FMT-44 (غلاف كإطار أول) + FMT-26 (−14 LUFS) + QA (verify_video) — كل النسب، غلاف، GIF، حزمة نشر مفحوصة، وإيصال قياس.
- **بودكاست إلى 20 شورت / podcast to shorts:** FMT-17 + FMT-57 (تفتيت) + SYNC (words.json) + FMT-13 + FMT-33 — اختيار المقاطع بخطافات مستقلة، تأطير يتبع المتكلم، وحزمة نشر لكل مقطع.
- **إعلان تطبيق / app ad:** FMT-55 (فيزياء الخانة) + UI (واجهة حية) + FMT-64 (ختام المتجر) + FMT-28 (مواصفة المتجر) + FMT-62 (حلقة) — الرسالة قبل 5 ث، ختام بالأيقونة، ونسخة معاينة للمتجر.
- **فيلم سينمائي عريض / cinematic short:** FMT-03 (أشرطة 2.39) + CAM (حركة كاميرا بطيئة) + COLOR (تدرج) + FMT-21 (ماستر 4K) + FMT-59 (فصول) — أشرطة تنفتح في 2.2 ث وترجمة داخل الشريط السفلي.
- **طبقة لمحرر آخر / overlay for another editor:** FMT-22 (ألفا) + ARAB-50 (شريط اسم) + BRAND — شريط اسم عربي بشفافية ProRes 4444 أو WebM.
- **حملة بلغتين / bilingual campaign:** FMT-36 + ARAB-08 + FMT-56 (نسخ مختصرة) + FMT-31 — كتالوج نصوص، رندر عربي وإنجليزي، ونسخ 30/15 ث لكل منصة.
- **محرر بلا حاسوب / no-computer editor:** FMT-42 (Studio Cloud artifact) + FMT-30 (تسجيل/تحويل) — المستخدم يحرر ويصدّر MP4 من claude.ai مباشرة.

## أخطاء ممنوعة / never do

1. **لا قصّ منتصف أعمى من 16:9 إلى 9:16** — يقطع الوجوه والنصوص؛ استخدم smart أو blur (FMT-13/FMT-14).
2. **لا نص أو دعوة في أسفل 20% أو يمين 12% من الريل** — تغطيه أزرار المنصة؛ ارسم الخطوط أولًا (FMT-08).
3. **لا MP4 بدون yuv420p و+faststart وعلامات BT.709** — لا يعمل على بعض الهواتف، يتأخر التشغيل، ويبهت اللون على iOS (FMT-20).
4. **لا قص صامت لمدة أو حجم يتجاوز حد المنصة** — بلّغ المستخدم واقترح نسخة مختصرة؛ أدواتك تُبلغ ولا تقص (FMT-31/FMT-56).
5. **لا غلاف أسود** — الأفلام التي تبدأ بإظلام تظهر سوداء في المعاينة؛ ثبّت الغلاف كإطار أول (FMT-44).
6. **لا تنشر نيابة عن المستخدم ولا ترسل لرقم بدون ربطه وموافقته** — أدواتك تعد الحزمة والروابط فقط (FMT-33/FMT-39/FMT-40).
7. **لا تكتب العنوان العربي داخل مولد الصور للغلاف** — يشوه الحروف؛ ولّد خلفية بلا نص وركّب العنوان (FMT-46, ARAB-09).
8. **لا MP3 للحلقات** — يضيف صمتًا يكسر الاتصال؛ WAV/Opus (FMT-27).
9. **لا تفترض أن حدود المنصات ثابتة** — الجداول «حتى 2026-10، راجعها عند الاستخدام»؛ قل ذلك للمستخدم قبل حملة مهمة (FMT-34).
10. **لا var_stream_map في HLS مع صوت واحد مربوط مرة واحدة** — جربتها هنا: ffmpeg يفشل؛ اربط الصوت لكل جودة (FMT-24).
11. **لا انتحال حسابات حقيقية في بطاقات المنصات** — استخدم حساب المستخدم أو حسابًا متخيلًا واضحًا (FMT-65).
12. **لا تكبير نقطي بمعامل كسري لتسليم 4K** — أعد رندر المتجهات بالدقة الأعلى، والنقطي بمعامل صحيح Lanczos (FMT-21/FMT-52).

## أقوى 5 حركات توقيع / 5 signature moves

1. **FMT-31 — ملف مفحوص لكل منصة:** `kmotion platforms` بثماني منصات وتقرير حدود — أول ما تعرضه بعد أي فيلم.
2. **FMT-13 — تأطير ذكي حول الوجه:** 16:9 → 9:16 أو 4:5 بلا قص للوجوه، مجرَّب هنا.
3. **FMT-44 — الغلاف كإطار أول:** يختفي «المربع الأسود» في كل معاينات السوشيال.
4. **FMT-33 — حزمة النشر المفحوصة:** كابشن، وسوم، عنوان، نص غلاف وبديل — بحدود كل منصة وبلا نشر تلقائي.
5. **FMT-32 — حزمة التسليم الكاملة:** كل النسب + غلاف بعنوان عربي + GIF/WebP في أمر واحد.
