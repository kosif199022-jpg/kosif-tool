# التوهج والإضاءة — Glow, light & bloom

> **قوتك هنا:** أنت تصنع ضوءًا يُصدَّق لا «توهج ذكاء اصطناعي»: انبعاث نقي يُضاف فوق المشهد بأنصاف أقطار متدرجة، هالة بلون مصدرها، إضاءة بالوقفات والكلفن، وأشعة وفلير ووميض في توقيتها — في المتصفح وthree.js والرسم بالكود وlibass. التوهج حاضر في 162 من 253 فيديو مرجعيًا أنتجتَه (بلوم في 54، تعتيم أطراف في 54، هالات في 29).
> **أقوى دليل:** لافتة النيون العربية «قهوة» التي رُندرت في هذه الحاوية — 10.000 ث، 300 إطار، 1080×1920، ‎−14.1 LUFS، و13/13 فحصًا ناجحًا (`kosif-tool/.claude/skills/kosif-superpowers/proofs/neon-glow/README.md`). وفي هذه الجلسة (2026-10-16) شغّلتُ أيضًا: سلسلة makePost ببلوم K3 على WebGL2 (SwiftShader)، ومكدس توهج/حافة/فلير في render.py، وفيلم CSS عربي (نيون لكل كلمة + مسحة ضوء + أشعة + وميض) عبر render_html.cjs بنتيجة VERIFY OK، وترجمة ASS بتوهج مزدوج، وحاسبة الضوء.
> **You can:** light, glow, bloom, flare, sweep and reflect — in HTML/CSS/SVG, Canvas, three.js (window.K3), the Python painter and ffmpeg/libass. **87 powers follow** — ✅ 31 · 🟢 20 · 📦 21 · 🔑 1 · 👁 9 · 📄 5 · 💡 0.

**الحالة / status:** ✅ مُثبت هنا (كود + اختبار أو رندر في هذه الحاوية) · 🟢 جاهز (كود المالك يعمل بلا إضافات) · 📦 بأمر تثبيت · 🔑 مفتاح أو خدمة · 👁 شوهد في فيديو أنتجتَه (وصفة البناء مرفقة) · 📄 موصوف فقط · 💡 فكرة.
مسارات الدليل نسبية إلى `/home/user/`؛ `style:<id>` = فيديو مرجعي أنتجتَه سابقًا (ملاحظاته في `kosif-tool/styles/<id>/`).

**فحص سريع لهذه الحاوية (2026-10-16):** Chromium (Playwright) يعطي WebGL 2.0 عبر SwiftShader بالأعلام `--use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader` ✔ · WebGPU: لا محوّل افتراضيًا، ومحوّل متاح فقط مع `--enable-unsafe-webgpu --enable-features=Vulkan --use-angle=swiftshader --enable-unsafe-swiftshader` (لم يُرندر لوح WebGPU بعد) · `three-kit.bundle.js` جاهز (three r186 بداخله، بلا npm) ✔ · OpenCV غير مثبت → bloom/chroma/relief في render.py تحتاج `pip install opencv-python-headless` · libass: مرّر `shaping=complex` دائمًا، فالوضع الافتراضي أظهر «ا» المنفصلة مربعًا فارغًا مع Cairo وTajawal.

## الفهرس / contents
- **النيون وتوهج الخطوط — Neon & line glow** — GLOW-01 … GLOW-15 (15)
- **التوهج المحيطي والهالات والخلفيات — Ambient glow, halos & backdrops** — GLOW-16 … GLOW-25 (10)
- **البلوم وما بعد المعالجة — Bloom & post** — GLOW-26 … GLOW-40 (15)
- **اللمعات والمسح الضوئي — Sheens, sweeps & glints** — GLOW-41 … GLOW-46 (6)
- **الأشعة والفلير والتسريب والوميض — Rays, flares, leaks & flashes** — GLOW-47 … GLOW-56 (10)
- **إضاءة الاستوديو والحافة وحسابات الضوء — Studio light, rim & light maths** — GLOW-57 … GLOW-72 (16)
- **ضوء الطبيعة والمصادر العملية والانعكاس — Natural light, practicals & reflections** — GLOW-73 … GLOW-84 (12)
- توليفات قوية / power combos · أخطاء ممنوعة / never do · أقوى 5 حركات توقيع / 5 signature moves
- **إضافات v2 — v2 additions** — GLOW-X01 … GLOW-X02 (2)

## النيون وتوهج الخطوط — Neon & line glow

_أنابيب وخطوط ونصوص تشع: طبقة انبعاث نقية تُضاف فوق المشهد عدة مرات بأنصاف أقطار متزايدة، وقلب أبيض ساخن._

#### GLOW-01 · لافتة نيون عربية حيّة · Living Arabic neon sign (ignition · wall light · wet reflection · synced hum) · ✅ مُثبت هنا / proven here
- **ماذا / what:** لافتة «قهوة» تشتعل على جدار طوب مبلل، و«OPEN LATE» حرفًا حرفًا بحرف T معطوب، وفنجان يُرسم بضوء يسري، وكل ذلك ينعكس على الأرض والصوت من الجدول نفسه. — A 10 s 9:16 neon-sign film: «قهوة» ignites on wet bricks, OPEN LATE lights letter by letter with a faulty T, a cup draws on with a travelling hot spot, the floor reflects it all and the sound comes from the same schedule.
- **متى أستخدمها / when:** لافتات، افتتاحيات ليلية، شعارات مقاهٍ ومتاجر، أي عنوان عربي يجب أن «يُضاء» — signs, night openers, shop/café logos, any Arabic title that must light up.
- **كيف / how:** Seek-driven Canvas page (window.__kosif.seek) rendered with render_html.cjs. Emission layer E = pure tube colour × level, then composited 5× with globalCompositeOperation 'lighter', each copy blurred; radii ≥26 px are blurred at ½ or ¼ resolution and scaled up (cheap and identical-looking). Wall light = ¼-res light map (ambient #1b1f30 + 40 px blur ×1.0 + 140 px blur ×1.95) multiplied onto a seeded brick albedo, so bricks take the sign colour and mortar stays dark. White-hot core from a distance field of the glyph mask (edge colour → mid at d1 → core at d2; Arabic 5/12 px, Latin 4/9 px) — never strokeText, because variable-font outlines overlap and the stroke draws seams through joined Arabic letters. Arabic word stays whole (browser-shaped); Latin letters are separate tubes. Camera push 1.0→1.075 + ±2 px handheld; reflection = 3 px flipped strips with ripple, sharp in puddles + 16 px blur film, Fresnel fade .9→.25; 90 rain streaks lit by the sign; grain + vignette. Sound: 120 Hz hum ∝ lit level, crackle on each rising edge, wet car pass panned with the headlight, normalised to −14 LUFS. **أرقام / params:** glow stack [3 px α.95, 10 α.75, 26 α.55 @½, 64 α.42 @¼, 140 α.30 @¼]; pink #ff2d95/#ff8fc8/#fff1f8, cyan #17d9ff/#93f0ff/#f0fdff, amber #ff9a1a/#ffc77a/#fff7e8, unlit glass #2a1820 rim #6a3a52; Cairo variable wght 420 @270 px (Arabic), 640 @100 px +22 px tracking (Latin), tube ≈20 px; verify 13/13: 1080×1920, 30 fps, 300 frames, 10.000 s, −14.1 LUFS, TP −1.4 dBFS; ≈13 min render on 4 cores.

```js
const GLOW = [[3,.95],[10,.75],[26,.55],[64,.42],[140,.30]];   // [blur px @1080 w, alpha]
function addGlow(ctx, E) {                       // E = emission canvas (tube colour × level)
  ctx.globalCompositeOperation = 'lighter';
  for (const [r, a] of GLOW) {
    const k = r >= 64 ? 4 : r >= 26 ? 2 : 1;      // big radii blurred at ¼–½ res (reuse canvases)
    const c = new OffscreenCanvas(W / k, H / k), g = c.getContext('2d');
    g.filter = `blur(${r / k}px)`; g.drawImage(E, 0, 0, W / k, H / k);
    ctx.globalAlpha = a; ctx.drawImage(c, 0, 0, W, H);
  }
  ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over';
}
```

- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/proofs/neon-glow/README.md` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/neon-glow/index.html` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/neon-glow/schedule.js` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/neon-glow/sound.py`
- **فيديوهات مرجعية / reference videos:** `style:product` · `style:pm-sudo-kiran-b055de`

#### GLOW-02 · جدول الاشتعال والوميض المعطوب · Ignition & faulty-tube flicker schedule · ✅ مُثبت هنا / proven here
- **ماذا / what:** الأنابيب تشتعل من جدول JSON واحد من مقاطع [بداية، نهاية، شدة] يقرأه الرسم والصوت معًا: توهج مسبق، ضربات بإطار واحد، انقطاعات، ثم تسخين. — Tubes light from one JSON schedule of [start, end, level] segments read by both picture and sound: pre-glow, one-frame strikes, dropouts, then a warm-up ramp.
- **متى أستخدمها / when:** كل لحظة «تشغيل» لافتة أو مصباح أو شاشة، ومزامنة الطقطقة مع الضوء — any switch-on moment; crackle synced to light.
- **كيف / how:** schedule.js holds plain JSON after 'window.NEON_SCHEDULE ='; segLevel(segs,t) returns the level of the active segment (0 outside), the last segment ends at 99 (stays lit) with a warm-up; hum = 1 − 0.035·sin(2π·4.7·t) − 0.03·noise per tube. Latin letters start at 2.3 + 0.1·i with their own 3-segment pattern; one 'faulty' tube gets extra dropouts. sound.py parses the same JSON (regex) → crackle on every rising edge, 120 Hz hum (+harmonics) ∝ lit level, buzz on the faulty tube. Alternatives: SVG sign flicker opacity .45 + .25·sin(1.4t); HyperFrames neon-flicker primitive anchored to hold/texture events (best span 0.5–2.5 s). **أرقام / params:** arabic [[.50,.70,.12],[.70,.733,.9],[.80,.833,.35],[.967,1,1],[1.10,1.233,.6],[1.30,1.333,.95],[1.40,1.433,.45],[1.50,99,1]]; warm-up 0.5 s outCubic; latin pattern [[0,.034,.85],[.10,.134,.45],[.20,99,1]]; faulty dropouts 7.80–7.967 s; one frame at 30 fps = 0.033 s.
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/proofs/neon-glow/schedule.js` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/neon-glow/sound.py` · `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/neon-flicker/scene.html` · `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/assets/scene.js:124`

#### GLOW-03 · أنبوب نيون SVG بأربع طبقات · SVG neon tube (4-stroke stack) · ✅ مُثبت هنا / proven here
- **ماذا / what:** خط لافتة نيون من أربع ضربات للمسار نفسه: هالتان عريضتان باهتتان، والأنبوب الملون، وقلب رفيع شبه أبيض. — A neon line drawn as four stacked strokes of one path: two wide faint halos, the coloured tube and a thin near-white core.
- **متى أستخدمها / when:** رسوم خطية ليلية، أيقونات نيون، مدن مرسومة بـ SVG — night line art, neon icons, SVG cityscapes.
- **كيف / how:** Same path four times, round caps/joins; animate group opacity for flicker. Cheap (no filters), crisp at any scale, and the tested midnight-cat scene uses it for signs. **أرقام / params:** w 1.7–3 px; 7w @ .045, 3w @ .12, w @ 1, 0.24w #f2ffff @ .85; flicker .45 + .25·sin(1.4t).

```js
function neon(d, c, w = 3) {           // halo, halo, tube, hot core
  return [[7*w,.045,c],[3*w,.12,c],[w,1,c],[.24*w,.85,'#f2ffff']].map(([sw,o,col]) =>
    `<path d="${d}" fill="none" stroke="${col}" stroke-width="${sw}" stroke-opacity="${o}"
       stroke-linecap="round" stroke-linejoin="round"/>`).join('');
}
// seek(t): sign.style.opacity = .45 + .25*Math.sin(1.4*t)
```

- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/assets/scene.js:13` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cinematic-cat.html:13`

#### GLOW-04 · توهج النص النيوني بثلاثة ظلال لكل كلمة · Neon text glow (triple shadow, per word) · ✅ مُثبت هنا / proven here
- **ماذا / what:** ثلاثة ظلال متراكبة 8 و24 و64 بكسل بلون واحد تجعل النص أنبوب نيون، تُطبَّق على كل كلمة لا على الحاوية. — Three stacked text-shadows (8, 24, 64 px) in one colour make type read as neon — applied per word span, never on the parent.
- **متى أستخدمها / when:** شعار أو عنوان قصير نيون، أسلوب neon-tech، كلمة واحدة بطلة — short neon titles/logos, the neon-tech style; never body text.
- **كيف / how:** text-shadow: 0 0 8px C, 0 0 24px C, 0 0 64px rgba(C,.6); fill a near-white tint (#eafcff) so the core reads hot. Arabic: one inline-block span per whole word inside direction:rtl. Glow on a parent with translucent children draws a visible rectangle — put it on the active word only. Style rules from the neon sheets: near-black #05060A, max 2 neon colours (#39FF14 / #FF2BD6 / #00E5FF), ≤3 flashes/s, RGB split only 2 frames. Scaffold the house style with `python3 tools/kosif.py scaffold neon-tech <dir>` (seeded particle bursts 400–1300 px/s, 150–600 particles). Verified in this container 2026-10-16: Arabic «نور الليل» with per-word spans rendered through render_html.cjs (VERIFY OK 2.4 s, 30 fps). **أرقام / params:** C = #00E5FF; blur 8/24/64 px, last at α .6; ≤2 colours; ≤3 flashes/s.
- **الدليل / proof:** `100-superskills/skills/trend-animation-styles/references/styles.md` · `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/audio-reactive.md` · `kosif-tool/styles/neon-tech/SKILL.md` · `kosif-tool/tools/render_html.cjs`
- **فيديوهات مرجعية / reference videos:** `style:pm-monokern-ade5b6` · `style:pm-sudo-kiran-b055de` · `style:pm-ceowinkz-7c776b`

#### GLOW-05 · توهج الكلمة النشطة في الترجمة · Active caption-word glow · 📦 بأمر تثبيت / one install
- **ماذا / what:** الكلمة المنطوقة أو المميزة بنجمة تتوهج بلون التمييز داخل الترجمة. — The spoken (or starred) caption word glows in the accent colour.
- **متى أستخدمها / when:** ريلز كاريوكي، ترجمة نيون، تمييز كلمة مفتاحية — karaoke reels, neon captions, keyword emphasis.
- **كيف / how:** Canvas: shadowColor = accent, shadowBlur = 0.5 × fontSize, offset 0, on the active word only (Basma 'glow' highlight; AutoEdit caption style 'neon'). HyperFrames caption-neon-glow component for HTML films. Keep the glow on the word, not the line box. **أرقام / params:** shadowBlur 0.5·fontSize; neon pair #FF0099 / #00FFF0; accent set #FCFF00 #53FF01 #FF0002.
- **الدليل / proof:** `app/public/js/00_editor.js:403` · `app/public/js/00_editor.js:2352` · `kosif-one/vendor/hyperframes/registry/components/caption-neon-glow/caption-neon-glow.html`
- **📦 تثبيت / install:** `cd /home/user/app && npm install   # Basma Studio (Vite) — or: npx hyperframes@0.8.164 add caption-neon-glow`
- **ترخيص / license:** HyperFrames (Apache-2.0) components animate with GSAP 3.14 — GSAP standard 'no charge' license (gsap.com/standard-license), not OSI.

#### GLOW-06 · ترجمة عربية بتوهج ASS مزدوج الطبقة · Two-layer ASS glow for Arabic captions · ✅ مُثبت هنا / proven here
- **ماذا / what:** توهج تحت الترجمة العربية برسم السطر نفسه مرتين: طبقة خلفية بحد سميك شبه شفاف وطبقة أمامية بحد رفيع حاد، وكلاهما يكبر قليلًا وهو يصعد. — A glow under Arabic captions by drawing the same line twice: a back layer with a thick semi-transparent outline and a crisp front layer, both scaling up slightly as they rise.
- **متى أستخدمها / when:** حرق ترجمة عربية بـ ffmpeg بلا متصفح، مونتاج أغانٍ وريلز — ffmpeg-burned Arabic captions, song montages, reels.
- **كيف / how:** Two ASS styles: 'Glow' on Layer 0 (outline 9, primary alpha &H80, optional \blur6) and 'Main' on Layer 1 (outline 3, shadow 2) with identical override tags \move(360,1060,360,1020,0,650)\fad(230,400)\fscx94\fscy94\t(0,650,\fscx100\fscy100); opening title \move(360,1030,360,950,0,950)\fad(300,650) \fscx88→107 over 950 ms. Swap ',' for the Arabic comma '،'. Verified here 2026-10-16 with Tajawal Bold: the default libass shaping turned the isolated ا of «القلب» into an empty box (with Cairo too) — pass shaping=complex and ship the font via fontsdir. **أرقام / params:** Noto Kufi Arabic (or Tajawal/Cairo) 57 px glow/main, 79 px title; Glow outline 9 α 0x80 (#DFF2FF / outline #8B5D3E); Main outline 3 shadow 2; MarginV 205–210; PlayRes 720×1280.

```ini
Style: Glow,Tajawal,57,&H80FFF2DF,&H80FFF2DF,&H803E5D8B,&H00000000,-1,0,0,0,100,100,0,0,1,9,0,2,40,40,210,1
Style: Main,Tajawal,57,&H00F8F7F3,&H00F8F7F3,&H00101B2E,&H64000000,-1,0,0,0,100,100,0,0,1,3,2,2,40,40,210,1
Dialogue: 0,0:00:00.00,0:00:02.00,Glow,,0,0,0,,{\blur6\move(360,1060,360,1020,0,650)\fad(230,400)}غربةٌ تسكن القلب
Dialogue: 1,0:00:00.00,0:00:02.00,Main,,0,0,0,,{\move(360,1060,360,1020,0,650)\fad(230,400)}غربةٌ تسكن القلب
# ffmpeg -i in.mp4 -vf "ass=cap.ass:fontsdir=fonts:shaping=complex" out.mp4
```

- **الدليل / proof:** `kosif-one/projects/KOSIF_Motion_Ghorba/tools/render_ghorba_preview.py:52-77` · `kosif-one/projects/KOSIF_Motion_Ghorba/KOSIF_Ghorba_Render.py:52-54` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/_shared/fonts/Tajawal-Bold.ttf`

#### GLOW-07 · مرشح توهج SVG ونسخة مموهة · SVG blur-merge glow & blurred duplicate · ✅ مُثبت هنا / proven here
- **ماذا / what:** مسار أو شكل يتوهج بدمج نسخة مموهة منه تحت الشكل الحاد. — A path or shape glows by merging a Gaussian-blurred copy under the crisp original.
- **متى أستخدمها / when:** خطوط ذهبية مرسومة، برق، عيون وحمم، موجة ختامية — drawn gold lines, lightning, eyes/lava rims, end-card waves.
- **كيف / how:** <filter x=-50% y=-50% width=200% height=200%> feGaussianBlur stdDeviation 6 → feMerge(blur, SourceGraphic). For light sources draw the blurred copy (filters blur3/blur8/blur20, opacity .9) then the sharp shape on top; a big impact light is a full-frame radialGradient rect. Without filters: duplicate layer, blur, 30% opacity. Verified here in the render_html test (gold arc, stdDeviation 6). **أرقام / params:** stdDeviation 3 / 6 / 8 / 20; region −50%..200%; impact glow r 560 #fdba74 .75 → #f97316 0; end-card wave blur 12 px.
- **الدليل / proof:** `kosif-one/projects/duck-vs-dragon/duck_dragon.py:61-63` · `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:56` · `kosif-studio/motion/projects/premium_edit/index.html:56` · `kosif-tool/styles/pm-aschapmann-131210/BRIEF.md`
- **فيديوهات مرجعية / reference videos:** `style:pm-heyiammallik-e72d17` · `style:pm-aschapmann-131210`

#### GLOW-08 · رأس ضوئي يسري على الخط وشطب متوهج · Travelling light head on a stroke (glint, comet, glowing strike) · ✅ مُثبت هنا / proven here
- **ماذا / what:** نقطة ساخنة تجري على مسار وهو يُرسم، أو وميض قصير يجري على حواف حرف، أو خط أحمر متوهج يشطب كلمة. — A hot spot rides a stroke as it draws, a short glint runs along an outlined glyph, or a glowing red line strikes a word out.
- **متى أستخدمها / when:** رسم أيقونة أو شعار، تتبع مسار، مذنّب، «خطأ ← صواب» — icon/logo draw-on, path tracing, comets, wrong→right edits.
- **كيف / how:** SVG path pathLength=1, stroke-dashoffset 1→0 (~1 s); head = getPointAtLength(L·p) drawn as a 4–6 px white dot with a 12 px glow; or a second dash of length 0.04 (≈8% of length) at the same offset in the accent with drop-shadow 6–12 px; fade the head over 0.5 s after arrival. Pulses travel at constant speed (2400 px/s) and the target blooms .6→1 with 5% overshoot in 400 ms. Strike: 4 px red #e8322a scaleX 0→1 from the reading start, 400 ms power3.out, 10 px glow, then swap the word. Arabic: start the head on the right. Verified here (neon cup head; render_html arc with head). **أرقام / params:** draw ~1 s; head dash .04; glow 6–12 px; pulse 2400 px/s, 40 px glow; strike 400 ms; Basma pen head r .07·m α .42 + 8 sparks.
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/proofs/neon-glow/index.html` · `kosif-one/vendor/hyperframes/registry/components/tracing-beam/tracing-beam.html` · `app/public/js/10_studio.js:292` · `kosif-tool/styles/pm-influencer-seo-ce8c33/BRIEF.md`
- **فيديوهات مرجعية / reference videos:** `style:product` · `style:pm-robj3d3-b18fad` · `style:pm-manuelogomigo-f33ca9` · `style:pm-ajith-io-ea7f2d` · `style:pm-oliahmed205-3e31c4`

#### GLOW-09 · خط كهربائي متوهج برأس أبيض · Electric draw-head route line · 📦 بأمر تثبيت / one install
- **ماذا / what:** مسار أو نهر يُرسم وآخر 3% منه أبيض ساخن فوق قلب ثلجي وتوهج أزرق، ثم يخبو الرأس بعد الوصول. — A route or river whose leading 3% glows white-hot over an icy core and blue glow, the head fading after arrival.
- **متى أستخدمها / when:** خرائط الرحلات والأنهار والكابلات — map routes, rivers, cables.
- **كيف / how:** Four stacked line layers bottom→top: glow #49C6FF width 11 opacity .32 blur 6; core #E8F7FF width 3; head-glow rgba(120,225,255,.95) width 16 blur 9; head #FFFFFF width 4.5. Head source = slice from (drawn − 3%) to drawn; head opacity 1 while drawing, 0 over 0.5 s after. No dark casing under it. The same stack ports 1:1 to SVG in render_html. **أرقام / params:** head = last 3%; widths 11/3/16/4.5; blur 6/9; fade 0.5 s; bg #101315.
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/references/map-explainer-architecture.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/assets/tokens.ts`
- **📦 تثبيت / install:** `npm i remotion@4.0.536 @remotion/cli@4.0.536 maplibre-gl@6.14.0`
- **ترخيص / license:** Remotion company license (free for individuals and small teams; companies above the threshold need a paid license — remotion.dev/license).

#### GLOW-10 · توهج فوسفوري وخطوط نيون على Canvas · Phosphor / canvas neon stroke glow · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** خطوط راسم إشارات خضراء تتوهج وتترك أثرًا باهتًا، وحلقة نشطة أقوى من البقية. — Oscilloscope-green strokes glow and leave a fading afterglow; the active ring outshines the rest.
- **متى أستخدمها / when:** موسيقى مرئية، شاشات علمية، حلقات تقدم — music viz, scope/lab looks, progress rings.
- **كيف / how:** Build recipe: Canvas globalCompositeOperation 'lighter', strokeStyle #4dff9a at α .6, shadowBlur 10–14 with shadowColor = stroke; two passes per path (wide faint + thin bright 1.5–2 px) on #030706; persistence = redraw last frame at ~.85 before drawing the new one; additive overlaps brighten. Rings: shadowBlur 12–20, active α 1, others .6. **أرقام / params:** core 1.5–2 px; blur 10–14 px; bg #030706; persistence ≈ .85/frame.
- **الدليل / proof:** `style:pm-rneayan-ea6129` · `style:pm-kantamk-61f410`

#### GLOW-11 · حافة متدرجة متوهجة وظل بلون العنصر · Gradient rim-glow border & hue-matched glow shadow · 📦 بأمر تثبيت / one install
- **ماذا / what:** كبسولة أو بطاقة أو هاتف بحافة متدرجة تتوهج من نسخة مموهة خلفها، وأيقونة بظل ملون من لونها. — A pill, card or phone with a gradient rim glowing from a blurred duplicate behind it; icons with a shadow in their own hue.
- **متى أستخدمها / when:** خانة الأوامر، البطاقة النشطة، أيقونة التطبيق، شارات وأقفال — prompt boxes, focused cards, app icons, badges, locks.
- **كيف / how:** Rim: black rounded rect (radius 999 px), 2 px conic-gradient border (green→yellow→red or #d946ef→#6c3bff), blurred duplicate 20–40 px behind. Focus: box-shadow 0 0 24px accent@40%. Drawn version: HyperFrames outline-draw (conic border drawn clockwise, clean closure). Hue shadow: 0 20px 50px rgba(hue,.35) under a glossy squircle; hex badge = gradient stroke + drop-shadow 0 0 12px gold; padlock keyhole glow blur 20 px as the shackle drops in 250 ms. **أرقام / params:** border 2 px; blur 30 px; focus 24 px @40%; outline-draw thickness 6 (1–20) radius 24 (0–80) progress 0–100.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/outline-draw/outline-draw.html` · `style:product` · `style:pm-jazzen-chen-4542ae` · `style:pm-wozu-co-242285`
- **فيديوهات مرجعية / reference videos:** `style:pm-ultimaxbt-2ddf1e` · `style:pm-yunn260414-60d996` · `style:pm-bthreeagency-b9b8d9` · `style:pm-agonaliu-466a8f`
- **📦 تثبيت / install:** `npx hyperframes@0.8.164 add outline-draw`
- **ترخيص / license:** HyperFrames (Apache-2.0) components animate with GSAP 3.14 — GSAP standard 'no charge' license (gsap.com/standard-license), not OSI.

#### GLOW-12 · كلمة من نقاط مضيئة · Dot-matrix glowing word · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** كلمة تُبنى من شبكة نقاط مضيئة تتوهج مع وميض في وسطها. — A word built from a grid of glowing dots, with a flare at the centre.
- **متى أستخدمها / when:** شاشات LED، عدّادات، عناوين تقنية — LED boards, counters, tech titles.
- **كيف / how:** Build recipe: render the shaped WHOLE word to an offscreen canvas (Arabic stays joined), sample its alpha on a grid, draw a 4 px dot where alpha > .5 with additive blending, then a 20 px bloom pass and a soft flare at the centre; reveal dots by distance from centre. **أرقام / params:** dot 4 px; bloom 20 px.
- **الدليل / proof:** `style:pm-lukasersil-0ed38e`

#### GLOW-13 · نفق نيون واندفاع للأمام · Neon tunnel / streak zoom-through · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** حلقات نيون مستطيلة أو قضبان ضوء تندفع نحو الكاميرا مع خطوط سرعة وتوهج. — Neon rounded-rect rings or light bars rush toward camera with speed lines and bloom.
- **متى أستخدمها / when:** انتقال طاقة عالية، افتتاحية ألعاب أو تقنية — high-energy transitions, gaming/tech openers.
- **كيف / how:** Build recipe: 20–30 rounded-rect rings (red/blue/white) with scale = 1/z as z decreases each frame, additive blend; radial speed lines; 2–3 frames of horizontal slice glitch at the peak. Bar variant: bright coloured bars stretch toward camera over 500 ms, bloom 1.5, sparks. **أرقام / params:** 20–30 rings; 500 ms; bloom strength 1.5.
- **الدليل / proof:** `style:pm-prasenx-8d9323` · `style:pm-spearwtf-3c1fd1`

#### GLOW-14 · توهج مضاف متدرج في الرسم بالكود · Painter additive glow stack (blades, magic, embers) · ✅ مُثبت هنا / proven here
- **ماذا / what:** ضوء يفيض من شكل: الشكل نفسه يُملأ بالإضافة ويموَّه بنصف قطر، ويتكرر بأنصاف أقطار متناقصة. — Light spilling from a shape: the shape filled additively and blurred, repeated at shrinking radii.
- **متى أستخدمها / when:** مشاهد KOSIF Studio المرسومة: سيوف، سحر، جمر، عيون — code-painted scenes: blades, magic, embers, eyes.
- **كيف / how:** glow(shape, colour, radius, alpha) == fill(shape, colour, alpha, blur=radius, mode='add') on the float canvas; stack 2–3 glows of decreasing radius, then the solid near-white fill. Ran here 2026-10-16: render.py rendered the blade stack + shade + rim + flare at 600×400 in 0.12 s. **أرقام / params:** blade: glow 40 #1a8cff .5 → 14 #3fd0ff .95 → 4 #b8f2ff 1 → fill #f2fdff; spill example glow(ellipse(900,200,90), '#8a7ad0', 40, .5).

```python
import render as R                       # kosif-studio/render.py
blade = R.ellipse(600, 400, 30, 240)
step = R.Step('blade', [R.glow(blade, '#1a8cff', 40, .5), R.glow(blade, '#3fd0ff', 14, .95),
                        R.glow(blade, '#b8f2ff', 4, 1), R.fill(blade, '#f2fdff')])
R.render_image([step], scale=.5).save('blade.png')
```

- **الدليل / proof:** `kosif-studio/render.py:407` · `kosif-studio/scenes/dragon_girl.py:377` · `kosif-one/tools/kosif-studio/render.py:407` · `100-superskills/skills/pixel-studio-painter/scripts/render.py`

#### GLOW-15 · وصفة البرق والقوس الكهربائي · Lightning bolt, electric arc & 3D double flash · 🟢 جاهز / ready
- **ماذا / what:** برق متعرج بفرع وتوهج أزرق عريض وقلب أبيض رفيع وغسلة سماء، أو ومضتان قصيرتان تضيئان مشهدًا ثلاثي الأبعاد. — A jagged branching bolt with a wide blue glow, thin white core and sky wash — or two short pulses lighting a 3D scene.
- **متى أستخدمها / when:** عواصف، صدمات، لحظات «فكرة»، ضربات إيقاع — storms, impacts, 'idea' moments, accent hits.
- **كيف / how:** 2D (render.py, seeded): random walk x += U(−30,18), y += U(18,34) until y 430, one branch; glow(stroke(bolt,10), '#8fb4ff', 30, .7) + fill(stroke(bolt,2.6), '#f6f9ff') + radial screen wash .18 (#9fbcf0). 3D: flash = max(0,1−|t−10.6|/.09) + .55·max(0,1−|t−10.82|/.07) drives a 9000-intensity point light, exposure +.05·flash and cloud colour ×(1+1.6·flash) — rule: lightning = a 2-frame spike of light + exposure. Music: HyperFrames electric-arc primitive on accent/glitch events (0.1–0.6 s). **أرقام / params:** pulses 90 ms + 70 ms (2nd at 55%); bolt #8fb4ff / #f6f9ff / wash #9fbcf0.
- **الدليل / proof:** `kosif-studio/scenes/whale_dragon.py:107` · `kosif-studio/scenes/duck_dragon.py:114` · `100-superskills/skills/kosif-montage-motion/scripts/projects/water_cycle_3d/src/main.js:70` · `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/electric-arc/scene.html`
- **فيديوهات مرجعية / reference videos:** `style:pm-nolkeeg-bf062e`

## التوهج المحيطي والهالات والخلفيات — Ambient glow, halos & backdrops

_ضوء لا يُرى مصدره: برك شعاعية خلف البطل، خلفيات حية تتنفس، هالات تلفت الانتباه ثم تهدأ._

#### GLOW-16 · بركة ضوء شعاعية خلف العنوان · Hero radial glow pool (bloom-in, bounded breathe, point origin) · ✅ مُثبت هنا / proven here
- **ماذا / what:** بركة ضوء ناعمة بلون العلامة خلف العنوان أو الشعار تجذب العين بلا شكل صلب، تتفتح ثم تتنفس بحدود. — A soft brand-tinted pool of light behind the title or logo pulls the eye without a hard shape; it blooms in, then breathes within bounds.
- **متى أستخدمها / when:** بطاقات العنوان والشعار والدعوة، خلفيات داكنة — title/logo/CTA cards on dark grounds.
- **كيف / how:** UI: radial-gradient(circle, rgba(accent,.12) 0%, transparent 70%). Film: bloom in with power2.out to peak opacity ≤ .45, then a linear-driven breathe ±6%. Logo: #0645e2 at 40% to black, radius ≈50% W, mark scales .9→1 with blur 8→0, wordmark staggers in. Point origin: 1 px #ffd2a8 dot, halo #ff7a2a α .5→0 growing 4→40 px over 3 s with a ±10% pulse every 1.2 s; swell = dot scale + halo 2× radius at .6 in 600 ms. Remotion starter: radial-gradient(120% 80% at 50% 18%, accent@.3, #0b0d12 62%) + 44 px dot grid drifting .35/.21 px per frame. Verified here (render_html test: cyan pool .45 + breathe). **أرقام / params:** alpha .12 (UI) / ≤ .45 (film); fade to 0 at 70%; breathe ±6%; point halo 4→40 px / 3 s.
- **الدليل / proof:** `kosif-atlas/skills/196-landing/621-landing` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/ambient-glow-bloom.md` · `kosif-tool/starters/remotion/src/Film.tsx:77`
- **فيديوهات مرجعية / reference videos:** `style:pm-arjunsh1607-93005d` · `style:pm-imthatcarlos-e04bfe` · `style:pm-l3d1c-0e35a3` · `style:pm-tdinh-me-815acb` · `style:pm-kloss-xyz-b9b3f6` · `style:pm-leonkohli-6dc01b`

#### GLOW-17 · غسيل خلفية بعدة توهجات وقاعدة الخلفية الحية · Multi-blob wash, corner glows & the living-backdrop rule · 🟢 جاهز / ready
- **ماذا / what:** بقع لونية ناعمة كبيرة في زوايا الخلفية، و2–5 عناصر محيطية بطيئة تُبقي المشهد حيًا. — Large soft colour blobs in the background corners, plus 2–5 slow ambient decoratives that keep a scene alive.
- **متى أستخدمها / when:** واجهات ولوحات تحكم وخلفيات مشاهد شرح — dashboards, UI films, explainer backdrops.
- **كيف / how:** Fixed ::before layer (z-index −1, pointer-events none) with two radial-gradients via color-mix: violet 7% at 58% 0% (solid 0–18%, fade 46%) + teal 5% at 18% 42% (0–12%, fade 38%). Page wash: radial-gradient(600px 400px at 95% −5%, rgba(99,102,241,.08)), (500px 380px at −5% 40%, rgba(6,182,212,.07)), (500px 380px at 100% 85%, rgba(236,72,153,.06)); editorial: 700×420 at 96% −8% rgba(75,35,119,.10) + 520×380 at −10% 45% rgba(200,163,93,.08). Living layer: pick 2–5 of breathing accent glow, ghost text at 3–8% drifting, pulsing hairlines, grain, thematic shapes. On dark grounds never a full-screen linear gradient (H.264 banding) — radial or solid + local glow + grain. **أرقام / params:** blob alphas .05–.10; ghost text 3–8%; 2–5 decoratives.
- **الدليل / proof:** `kosif-audit-pro/app/globals.css:271` · `kosif-audit-studio/dashboard-theme.css` · `kosif-audit-studio/kosif-one-editorial-theme.css` · `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/house-style.md`

#### GLOW-18 · خلفيات الاستوديو الإجرائية: شفق وغروب ومدار · Studio procedural glow backdrops (aurora · sunset · grid) · ✅ مُثبت هنا / proven here
- **ماذا / what:** مشاهد خلفية مرسومة حيًا: شبكة مائلة تنجرف، توهج شعاعي يدور على مسار ليساجو، ثلاث حلقات بيضاوية، و38 جسيمًا. — Live-drawn backdrop scenes: drifting diagonal grid, a radial glow wandering on a Lissajous path, three rotating ellipse rings and 38 particles.
- **متى أستخدمها / when:** خلفية سريعة لمقطع، شاشة انتظار، مقدمة — quick clip backgrounds, holding screens, intros.
- **كيف / how:** Click the preset (data-preset='aurora'|'sunset'|'grid') or set clip {type:'demo', preset}; drawDemo() paints from t. Wandering glow: createRadialGradient at x = w/2 + sin(.32t)·.13w, y = .48h + cos(.38t)·.08h, inner r·.08, outer r = .39·min(w,h); stops 0 preset colour α 0x55, .68 #77cfc017, 1 transparent. **أرقام / params:** aurora #071520→#12343a (60%)→#22584d, line #83c8cf, glow #57d2ba55, rings #65c6bb66 · sunset #22121e→#512823→#c6773c, line #ffc08b, glow #ecaa6155 · grid #101225→#272244→#41466b, glow #9985ed55; clip 6 s.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:65` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:67` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/index.html`

#### GLOW-19 · ستارة الشفق · Aurora drift / aurora curtains · 📦 بأمر تثبيت / one install
- **ماذا / what:** ثلاث بقع شفق بلون التمييز تنجرف في حلقة متصلة فوق قاعدة داكنة، أو ستائر شفق خضراء وبنفسجية بمظلل WebGPU. — Three accent-tinted aurora blobs drift in a seamless loop over a dark base — or green/violet curtains from a WebGPU shader.
- **متى أستخدمها / when:** خلفيات إطلاق منتجات وفواصل هادئة — product-launch backdrops, calm interludes.
- **كيف / how:** CSS: `npx hyperframes@0.8.164 add aurora-drift`, mount on a class='clip' div (data-start/duration/track-index, data-variable-values JSON); colours from the 18 theme tokens; extra duration becomes hold, never time-stretch. Shader: data-shader='Aurora' canvas in a root marked data-requires-webgpu (see GLOW-52). Seen in style:product: blurred blue-violet-purple blobs + orange at right along the bottom third of #06050a. **أرقام / params:** accent green|blue|violet; mood deep|bright; faint vignette.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/aurora-drift/aurora-drift.html` · `kosif-one/vendor/hyperframes/registry/blocks/aurora/aurora.html` · `style:product`
- **📦 تثبيت / install:** `npx hyperframes@0.8.164 add aurora-drift`
- **ترخيص / license:** HyperFrames (Apache-2.0) components animate with GSAP 3.14 — GSAP standard 'no charge' license (gsap.com/standard-license), not OSI.

#### GLOW-20 · بقعة ضوء تتبع العنصر · Follow-spot & feathered spotlight · 📦 بأمر تثبيت / one install
- **ماذا / what:** توهج خلفي كبير ينتقل مركزه إلى العنصر النشط، أو تعتيم كل الإطار إلا بيضاوي ناعم ينزلق بين الأهداف. — A big backdrop glow whose centre glides to the active element, or a dimmed frame except a feathered ellipse gliding between targets.
- **متى أستخدمها / when:** إنفوغرافيك بأسلوب أبل، شرح واجهات، منتج على منصة — Apple-style infographics, UI walkthroughs, pedestal products.
- **كيف / how:** Follow: black bg + one radial (#0a3d91 ≈25%, radius ≈60% W) whose centre lerps to the active object per scene. Feather: HyperFrames yt-feather-highlight — ellipse position/size are CSS vars, so it glides. Spotlight card: scripted cursor-following spot + lit border. Pedestal: radial ellipse under the object. Paper spot: radius 15% W travelling over 3 s. **أرقام / params:** radius ≈60% W @25%; paper spot 15% W / 3 s.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/yt-feather-highlight/yt-feather-highlight.html` · `kosif-one/vendor/hyperframes/registry/components/spotlight-card/spotlight-card.html` · `style:infographic`
- **فيديوهات مرجعية / reference videos:** `style:pm-bthreeagency-b9b8d9` · `style:pm-ajith-io-4c248f`
- **📦 تثبيت / install:** `npx hyperframes@0.8.164 add yt-feather-highlight`
- **ترخيص / license:** HyperFrames (Apache-2.0) components animate with GSAP 3.14 — GSAP standard 'no charge' license (gsap.com/standard-license), not OSI.

#### GLOW-21 · حلقات هالة متحدة المركز · Concentric halo rings · 🟢 جاهز / ready
- **ماذا / what:** دوائر زخرفية من ظلال box-shadow منتشرة بشفافية ضئيلة تعطي هالة رادار خلف المحتوى. — Decorative circles from stacked spread box-shadows at very low alpha give a radar/atmosphere halo behind content.
- **متى أستخدمها / when:** خلفية بطل، شعار، رمز مركزي — hero backdrops, logos, central symbols.
- **كيف / how:** box-shadow: 0 0 0 45px rgba(255,255,255,.025), 0 0 0 95px rgba(255,255,255,.018) on a 420 px circle (studio4: #bdd1c004/#bdd1c005 at 50/100 px). Ember variant: brown-orange radial behind the mark (radius ≈35% H) + 2–3 thin 1 px rings at 20% + orbiting flare dots, rotating 10°/s. **أرقام / params:** circle 420–470 px; spreads 24/45/50/95/100 px; alpha .018–.04.
- **الدليل / proof:** `kosif-audit-studio/styles.css:167` · `kosif-audit-studio/studio.css:57` · `style:pm-robj3d3-b18fad`

#### GLOW-22 · نبضة وهالة لفت الانتباه · Pulse ring, halo & the attention set · 🟢 جاهز / ready
- **ماذا / what:** حلقة تتسع وتخبو عددًا محددًا من المرات لتأكيد حالة، ومفردات قليلة للفت الانتباه لكل منها معنى. — An outline ring scales out and fades a fixed number of times to confirm a state, plus a small vocabulary of focus effects, each with a meaning.
- **متى أستخدمها / when:** قيمة جديدة، حالة «يعمل»، مدينة نشطة على خريطة — new values, live/healthy states, the active city.
- **كيف / how:** Ring ::after with border, keyframes, iteration-count 2, then stop. Menu: pulse (new/alert, low amplitude, 1–2 cycles); halo (current focus without changing the mark); sparkle (positive discovery only); ember/fire (heat/overload — never human tragedy); glow trail (active route); shockwave (when distance from an origin matters: 1–3 circles .2→3, opacity .6→0, stroke thinning, 600–900 ms expo.out + 4 px shake for 150 ms). Progress head: 8 px #d9f3c7 dot with box-shadow 0 0 16px #d9f3c7bb at the top of the ring. Let the mark settle static. **أرقام / params:** health .55→2.4, 900 ms, delay 320 ms, ×2 (8 px teal dot + 4 px halo); current stage .85→1.45, 900 ms, delay 480 ms, ×2.
- **الدليل / proof:** `kosif-audit-pro/app/globals.css:576` · `kosif-audit-studio/studio.css:73` · `kosif-atlas/skills/2690-build-web-data-visualization/10332-threejs-data-visualization/references/particle-effects-and-flow.md` · `style:pm-maxalexweber-67688b`

#### GLOW-23 · كلمة تنفجر بتوهج وحلقة · Burst word with glow & expanding ring · ✅ مُثبت هنا / proven here
- **ماذا / what:** كلمة بطلة تقفز من 0.55 إلى 1 بنابض مع توهج ناعم بينما تتسع حلقة لون التمييز حتى 1500 بكسل وتخبو. — A hero word pops 0.55→1 on a spring with a soft glow while a 6 px accent ring expands to 1500 px and fades.
- **متى أستخدمها / when:** ضربة الكلمة الأولى، كشف رقم، ذروة ريل — first-beat words, number reveals, reel peaks.
- **كيف / how:** Tested html-canvas starter: pop prog(local, .2, .75, spring 150/14); ring prog(local, .25, 1.3, outExpo), width 10 + r·1500; text-shadow 0 0 60px rgba(126,232,210,.55). **أرقام / params:** 220 px weight 900 #fff; glow 60 px rgba(126,232,210,.55); ring 6 px #7ee8d2.
- **الدليل / proof:** `kosif-tool/starters/html-canvas/index.html:28` · `kosif-tool/starters/html-canvas/index.html:168`

#### GLOW-24 · هالة تتنفس مع الصوت وأشعة وغبار القصيدة · Voice/beat-breathing halo, shafts & dust (verse light) · 📦 بأمر تثبيت / one install
- **ماذا / what:** هالة مركزية تتضخم مع علو الصوت والضربات، وأشعة ضوء بطيئة وغبار يطير نحو العدسة، ووميض على الجملة الختامية. — A central halo swells with loudness and kicks, slow light shafts and dust fly toward the lens, and a flare marks the payoff.
- **متى أستخدمها / when:** قصيدة، دعاء، أغنية، تعليق صوتي — poems, duas, songs, voice-overs.
- **كيف / how:** verse.html draw(t) reads window.SOUND channels (rms, bass, kick) and state.flare. Halo radius and alpha below; drawDepth(): 9 light shafts from above, spread .13 rad, length 1.35 H, alpha .05 + .04·rms + .05·kick; 140 dust points flying at z-speed .025–.075 (near ones ×3.2 softer); payoff flare 0→1 in .5 s, back over 2.2 s; kicks send rings, onsets lift motes. Keep it subtle: no EQ bars, no strobing, no beat claim without a detector. The halo maths alone runs in any seek page (render_html verified). **أرقام / params:** R = .62·min(W,H)·(1 + .05 rms + .06 kick + .25 flare); inner α .20 + .16 rms + .14 kick + .35 flare; drum bloom 200 px / 400 ms decay.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/templates/verse.html:130` · `100-superskills/skills/kosif-montage-motion/templates/verse.html:99` · `kosif-studio/motion/verse.py:382` · `kosif-one/vendor/brag/skills/brag/references/audio.md`
- **فيديوهات مرجعية / reference videos:** `style:pm-kamstudiolabs-447565`
- **📦 تثبيت / install:** `pip install faster-whisper   # measured word times for verse.py; without it timings are reported as 'estimated'`

#### GLOW-25 · دائرة سحرية بكسل بتوهج منقّط · Pixel magic circle (dithered glow) · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** حلقة رونية تحت الساحر تدور بإطارات متقطعة بتوهج منقط بلون التعويذة. — A rune ring under the caster rotating in stepped frames with a dithered glow in the spell colour.
- **متى أستخدمها / when:** ألعاب بكسل، سحر، أسلوب ريترو — pixel games, magic, retro looks.
- **كيف / how:** Build recipe: ellipse ring + rune dots on a low-res canvas, rotate in steps at 8 fps (not smooth), glow as an ordered-dither halo (Bayer 4×4) instead of blur so it stays pixel-crisp; alternate two colours on the flash; upscale nearest-neighbour. **أرقام / params:** 8 fps rotation; 2-colour alternating flash.
- **الدليل / proof:** `style:pm-0xevinho-3777d8`

## البلوم وما بعد المعالجة — Bloom & post

_الضوء الذي يتجاوز 1.0 ينسكب كالعدسة: بلوم بعتبة، هالة بلون المصدر، تعتيم أطراف، وانحراف لوني محسوب — بأرقام لقطات حقيقية._

#### GLOW-26 · سلسلة ما بعد المعالجة السينمائية (makePost) · Three-kit cinematic post stack (makePost) · ✅ مُثبت هنا / proven here
- **ماذا / what:** حارس NaN، ثم بلوم Unreal، ثم أشعة من الشمس، ثم عمق مجال، ثم تلوين وتعتيم وانحراف لوني، ثم حبيبات — في استدعاء واحد. — NaN/firefly guard → Unreal bloom → screen-space sun rays → bokeh DOF → grade (split tone, vignette, CA) → film grain → output, in one call.
- **متى أستخدمها / when:** كل مشهد three.js في KOSIF: طبيعة، مدن، منتجات — every three.js scene: nature, cities, products.
- **كيف / how:** Load the prebuilt bundle (three r186 inside, no npm): <script src=three-kit.bundle.js> → window.K3. post = K3.makePost(renderer, scene, camera, W, H, {bloom, bloomThreshold, aperture, maxblur, vignette, ca, grain, clampMax}); per frame post.sunOnScreen(sunDir) then post.composer.render(0). Verified here 2026-10-16 (Playwright Chromium, --use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader, WebGL 2.0): emissive torus K3.kelvin(1900) + cyan orb with the defaults gave a clean corona in each source colour; bloom .9 / threshold .6 washed the whole frame orange. Realism rules: exposure .5–.62, bloom threshold ≥ .9, sun in front of lens only at sunrise; ≈1–1.5 s/frame at 1080p. **أرقام / params:** guard clamp 48; bloom .22 radius .6 threshold .9; rays 64 samples decay .972 ×.55; bokeh focus 900 aperture 4e-5 maxblur .0035; vignette .42; CA 1.2; grain .16; shadows tint (.92,.98,1.08) highs (1.08,1,.92).

```js
// <script src="kit/three-kit.bundle.js"></script>  → window.K3 (three r186 bundled)
const T = K3.THREE, r = new T.WebGLRenderer({antialias: true, preserveDrawingBuffer: true});
r.toneMapping = T.ACESFilmicToneMapping;
const lamp = new T.MeshStandardMaterial({color: 0x111111, emissive: K3.kelvin(1900), emissiveIntensity: 3});
const post = K3.makePost(r, scene, cam, W, H, {bloom: .22, bloomThreshold: .9, grain: .05});
function seek(t) { update(t); post.sunOnScreen(sunDir); post.composer.render(0); }
```

- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:361` · `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.bundle.js` · `kosif-studio/tests/test_studio.py:606` · `kosif-studio/motion/references/hyperframes-authoring.md`
- **فيديوهات مرجعية / reference videos:** `style:pm-axtonliu-0b861d`

#### GLOW-27 · بلوم بلون مصدره على المواد المشعة · Emissive colour-corona bloom (and hit-lit rings) · ✅ مُثبت هنا / proven here
- **ماذا / what:** كل مصدر ساطع يلبس هالة بلونه هو، والسطوح المضاءة لا تتوهج؛ الألوان تأتي من الانبعاث فوق مشهد داكن. — Every bright source wears a halo in its own colour while lit surfaces stay clean; colour comes from emission over a dark scene.
- **متى أستخدمها / when:** مصابيح، نيون ثلاثي الأبعاد، محركات، حلقات تضيء مع الإيقاع — lamps, 3D neon, engines, beat-lit rings.
- **كيف / how:** Keep albedo dark (value < .2) and drive colour through emissive materials; threshold below the lamps but above lit surfaces (≥ .9 for realism, .2–.5 only for stylised neon caves); generous radius .6–.75, corona in the source colour, never grey. White objects that must not glow → selective bloom: render emissive into a separate MRT target, bloom it at threshold 0 (strength 1.5, radius .5), add to colour. Beat ring: emissive torus, on hit emissiveIntensity 4 decaying exponentially (τ ≈ 250 ms), random neon hue, bloom 1.2–1.8 at threshold .2. Verified in the K3 render above. **أرقام / params:** realism threshold ≥ .9; corona radius .6–.75; selective MRT 0 / 1.5 / .5; hit decay τ ≈ 250 ms.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/book-lessons.md` · `kosif-atlas/skills/2221-webgpu-threejs-tsl/8405-webgpu-threejs-tsl/docs/post-processing.md` · `kosif-studio/motion/kit/three-kit.js:361` · `style:pm-gorden-sun-041f56`
- **فيديوهات مرجعية / reference videos:** `style:pm-ivanfioravanti-bd9261`

#### GLOW-28 · جدول البلوم والتعريض لكل لقطة · Per-shot bloom & exposure presets (cinematic · lite · lab) · 🟢 جاهز / ready
- **ماذا / what:** كل لقطة تحمل قيم البلوم والعتبة ونصف القطر والتعريض الخاصة بها، فيتغير المزاج مع القطع فورًا. — Each shot carries its own bloom strength/threshold/radius and exposure, so a cut changes mood instantly.
- **متى أستخدمها / when:** أفلام ثلاثية الأبعاد متعددة اللقطات؛ اختيار نقطة بداية مجربة — multi-shot 3D films; a tested starting point.
- **كيف / how:** Plug the numbers into makePost / K3S.makeLitePost / K3.labPost (all inside the verified bundle). Exposure fades in over 0–0.35 s and drops 10% in the last 0.6 s of each shot. labPost is tuned for software GL (rays off, DOF optional). The source projects themselves bundle 'three' from npm (rebuild with the install line), but the numbers need nothing new. **أرقام / params:** الجدول أدناه / see the table below.

| لقطة / shot | bloom | threshold | radius | other |
|---|---|---|---|---|
| makePost default | .22 | .90 | .60 | vignette .42 · CA 1.2 · grain .16 |
| K3S.makeLitePost | .55 | .82 | .50 | vignette .38 · grain .025 |
| lite, character (bunny_twin) | .32 | .93 | .40 | vignette .45 · grain .018 |
| K3.labPost (software GL) | .08 | .95 | — | grain .05 · vignette .18 · CA .4 · warm .25 · rays off |
| blue_hour | .75 | .72 | .70 | aperture 2e-5 · vignette .5 · grain .10 · CA 1.2 |
| night_boat | .60 | .78 | .75 | vignette .55 · grain .11 |
| koi_pond | .32 | .86 | — | aperture 2.2e-4 · maxblur .006 |
| sound_ground | .60 | .78 | — | CA 1.4 · grain .12 |
| cinematic-3d-scene | .70 | .82 | .60 | ACES · vignette · light grain |
| Egypt orbit | 1.25 | .12 | .75 | exposure 1.10 |
| Egypt Giza | .42 | .95 | .50 | exposure .82 |
| Egypt Nile | .50 | .90 | .55 | exposure .82 |
| Egypt Cairo night | .95 | .78 | .60 | exposure .90 |
| Egypt Alexandria | .85 | .80 | .60 | exposure .92 |

- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/blue_hour/src/main.js:122` · `kosif-one/projects/egypt-2120-animation/index.html:190` · `kosif-studio/motion/kit/shape-kit.js:365` · `kosif-studio/motion/kit/lab-kit.js:272`

#### GLOW-29 · بلوم TSL وWebGPU · TSL / WebGPU bloom, selective MRT & lens nodes · 📦 بأمر تثبيت / one install
- **ماذا / what:** بلوم بعتبة وبلوم انتقائي وضبابية حركة وانحراف لوني كعُقد TSL في WebGPURenderer. — Threshold bloom, selective bloom, velocity motion blur and chromatic aberration as TSL nodes on WebGPURenderer.
- **متى أستخدمها / when:** مشاهد three.js حديثة على WebGPU — modern three.js scenes on WebGPU.
- **كيف / how:** bloom(scenePassColor) from three/addons/tsl/display/BloomNode.js, output = color.add(bloomPass); selective: emissive → MRT target, bloom at threshold 0; motionBlur(color, scenePass.getTextureNode('velocity')); chromaticAberration(color, {offset: vec2(.002)}). WebGPU in headless Chromium here needs --enable-unsafe-webgpu --enable-features=Vulkan --use-angle=swiftshader --enable-unsafe-swiftshader (adapter verified 2026-10-16; no TSL scene rendered yet). **أرقام / params:** bloom threshold .5 strength 1 radius .5; selective 0 / 1.5 / .5; CA offset .002.
- **الدليل / proof:** `kosif-atlas/skills/2221-webgpu-threejs-tsl/8405-webgpu-threejs-tsl/docs/post-processing.md` · `kosif-atlas/skills/2221-webgpu-threejs-tsl/8405-webgpu-threejs-tsl/SKILL.md` · `100-superskills/skills/kosif-montage-motion/references/tools-catalog-2.md`
- **📦 تثبيت / install:** `npm i three@0.186.1`

#### GLOW-30 · بلوم الرسم الثابت · Painter highlight bloom (stills & painted films) · 📦 بأمر تثبيت / one install
- **ماذا / what:** الضوء فوق العتبة ينسكب حوله بنصفي قطر كالعدسة على لوحة الرسم بالكود. — Light above a threshold spills into its surroundings at two radii, like a lens, on the code-painted canvas.
- **متى أستخدمها / when:** لمسة أخيرة لمشاهد KOSIF Studio وصور الأغلفة — finishing pass for painted scenes and covers.
- **كيف / how:** bloom(threshold, radius, strength, tint) adds blur(hi, r)·strength·tint + blur(hi, 3r)·strength·.5·tint, where hi = max(canvas − threshold, 0). Checked here: glow/shade/rim/flare run, but bloom() and chroma() stop with ModuleNotFoundError: cv2 until OpenCV is installed. **أرقام / params:** default .75 / 30 / .6; whale .8 / 24 / .32 tint #ffe6d0; AI-plate recipe .72 / 26 / .5.
- **الدليل / proof:** `kosif-studio/render.py:732` · `kosif-studio/scenes/whale_dragon.py:287` · `kosif-one/tools/kosif-studio/render.py:732`
- **📦 تثبيت / install:** `pip install opencv-python-headless`

#### GLOW-31 · الدمج المضاف على لوحة عائمة · Float-canvas light compositing (add / screen above 1.0) · ✅ مُثبت هنا / proven here
- **ماذا / what:** أربعة أوضاع دمج على لوحة float32 بلا قص، فيتجاوز الضوء المضاف 1.0 ثم ينحدر بنعومة بدل أن يُقص. — Four blend modes on an unclipped float32 canvas, so additive light can exceed 1.0 and roll off later instead of clipping.
- **متى أستخدمها / when:** أي تراكب توهجات في الرسم بالكود؛ ونفس الفكرة في المتصفح بـ lighter/screen — stacking glows in the painter; same idea in browsers.
- **كيف / how:** Pass mode= to fill()/text()/noise(); screen is reg += col·a·(1 − min(reg, 1)) so glows over 1.0 are not clipped; multiply darkens for shadows/texture; render_image(rolloff .82) or filmic() (ACES-style curve) maps >1 back. Browser equivalents: Canvas globalCompositeOperation 'lighter' (add) / 'screen', CSS mix-blend-mode: screen. **أرقام / params:** mode ∈ {normal, add, screen, multiply}; alpha 0..1; paint '#rrggbbaa'; rolloff .82.
- **الدليل / proof:** `kosif-studio/render.py:366` · `kosif-studio/render.py:397` · `100-superskills/skills/pixel-studio-painter/scripts/render.py`

#### GLOW-32 · تعتيم الأطراف · Vignette (CSS · canvas · kit · painter) · ✅ مُثبت هنا / proven here
- **ماذا / what:** تعتيم الحواف لتركيز العين في الوسط، بأربع طرق جاهزة. — Darkens the frame edges to focus the centre, four ready ways.
- **متى أستخدمها / when:** تقريبًا كل لقطة سينمائية، وتحت الترجمة — nearly every cinematic shot.
- **كيف / how:** CSS: full-frame div box-shadow inset 0 0 160px rgba(0,0,0,.85), pointer-events none (verified in the render_html test). Canvas: radial from .3·min(W,H) transparent to .75·max(W,H) rgba(0,0,0,v). motion-kit: MOTION.vignette(stage, {inner, strength, z}). Painter: vignette(strength .5), smoothstep from d .35. Over footage: 72% × 58% ellipse to .55. HyperFrames vignette component as a drop-in. **أرقام / params:** inset 160 px α .85; canvas v 0–.8 (MK .32–.78); kit inner 55% strength .42; footage .55.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/cinematic_3d.html:68` · `kosif-studio/motion/kit/motion-kit.js:457` · `app/public/js/00_editor.js:289` · `kosif-studio/render.py`

#### GLOW-33 · الانحراف اللوني للعدسة · Lens chromatic aberration (edge-weighted) · ✅ مُثبت هنا / proven here
- **ماذا / what:** الأحمر والأزرق يتباعدان قليلًا نحو أطراف الإطار كما في عدسة حقيقية. — Red and blue drift apart toward the frame edges, as in a real lens.
- **متى أستخدمها / when:** لمسة سينمائية خفيفة على مشهد كامل — a subtle lens finish on whole frames, never on body text.
- **كيف / how:** Shader: sample R/G/B at offsets scaled by distance from centre (≈0.002 UV at the edge, zero at the centre). makePost grade pass: off = d·(ca/1920)·|d|·4 with d = uv − .5, so the split grows quadratically toward the edges (ca 1.2–1.4; ran in the verified K3 render); TSL chromaticAberration(color, {offset: vec2(.002)}); painter chroma(1.5) scales R/B by 1 ± amount·2/max(W,H) about the centre (needs OpenCV). **أرقام / params:** offset .002 at edges; makePost ca 1.2 (sound_ground 1.4); labPost .4.
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:361` · `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md` · `kosif-studio/render.py:756`

#### GLOW-34 · انقسام RGB على الضربة · RGB-split hit jitter · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** نسخ حمراء وسماوية مزاحة ترتجف إطارين أو ثلاثة عند الضربة ثم يعود السكون. — Red and cyan offset copies jitter for 2–3 frames on a hit, then stillness returns.
- **متى أستخدمها / when:** ضربات الإيقاع، الغليتش، حركة سريعة ممتدة — beat hits, glitch accents, fast stretches.
- **كيف / how:** Build recipe: draw the layer three times with R +3 px and B −3 px in screen blend (idle 2–4 px), spike to 8–12 px on hits for 2–3 frames; text: red/cyan duplicates offset 4 px, mix-blend screen, jitter 3–5 frames; onion-skin: previous 3 frames tinted cyan/pink at 40%; add horizontal slice displacement only on heavy beats. Owner glitch pass (makeGlitchPass) exists in the trend notes but has not run here. **أرقام / params:** idle 2–4 px; hits 8–12 px for 2–3 frames; text offset 4 px.
- **الدليل / proof:** `style:pm-gizakdag-b8c59e` · `style:pm-micheleharmonic-77628e` · `style:pm-majin-appsheet-2d3c1a` · `100-superskills/skills/kosif-montage-motion/references/x-trend-2026.md`
- **فيديوهات مرجعية / reference videos:** `style:pm-zheke-38deff` · `style:pm-lukasersil-0ed38e` · `style:pm-topi-003-b0e12c`

#### GLOW-35 · تمويه السرعة وتلطيخ التكبير وكشف التركيز · Velocity blur, zoom-smear title & focus-pull glow · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** تمويه اتجاهي يتبع السرعة ويختفي عند السكون، وعنوان ختامي يدخل بخطوط تكبير ثم يتوهج، وشعار يظهر من ضبابية مع توهج. — Directional blur proportional to velocity (zero at rest), an end title that enters as zoom streaks then glows, and a logo pulled into focus with a glow.
- **متى أستخدمها / when:** دخول سريع، ختام أبل، كشف شعار — fast entrances, keynote end cards, logo reveals.
- **كيف / how:** Build recipe: per layer compute velocity; SVG feGaussianBlur stdDeviation on the motion axis ≈ .25 · px/frame (cap 24 px), filter region x −50% width 200%, same ease as the move; or an echo trail collapsing into the lead. End title: 20–30 scaled faded copies of the wordmark on a black radial bg, then one white word with tight 8 px glow + 60 px halo shrinking ≈1 px/frame (1650→500 px wide), ease-in collapse. Focus pull: blur 20→0 + glow fade over 600 ms; radial zoom-blur spin ≈ .3. HyperFrames' shutter motion-blur component (shutterAngle 360–720, 16 samples, +3.38 dB PSNR vs AE) is documented but not installed. **أرقام / params:** blur ≈ .25·px/frame, cap 24 px; glow 8 px + halo 60 px; focus 600 ms.
- **الدليل / proof:** `style:pm-notdwd-7de38a` · `style:pm-reflex-cloud-72ffe5` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/references/motion-blur.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/motion-blur-streak.md`
- **فيديوهات مرجعية / reference videos:** `style:pm-ultimaxbt-bbebf5`

#### GLOW-36 · مؤثرات وسائط HyperFrames وسلسلة VFX · HyperFrames media effects & per-pixel VFX chain · 📦 بأمر تثبيت / one install
- **ماذا / what:** معالجات غير هدّامة للصور والفيديو (Bloom وBlur وPixelate) وسلسلة نواة WebGL تُعاد رسمها حتميًا عند كل seek. — Non-destructive image/video treatments (Bloom, Blur, Pixelate) and a WebGL2 kernel chain repainted deterministically on every seek.
- **متى أستخدمها / when:** لقطات داخل أفلام HyperFrames تحتاج بلوم أو تشويه — footage inside HyperFrames films.
- **كيف / how:** `hyperframes media-treatment --selector <css> --apply` writes data attributes (source untouched); VFX chain: data-vfx-chain='{"version":1,"nodes":[{"type":"displacement-map"},{"type":"wave-warp"}]}' with an explicit pixel box on .hf-vfx-in; animate params through CSS custom properties. **أرقام / params:** families Bloom · Blur · Pixelate; nodes displacement-map · wave-warp · noise.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/guides/media-effects.mdx` · `kosif-one/vendor/hyperframes/docs/guides/vfx-chain.mdx`
- **📦 تثبيت / install:** `npm i -D hyperframes@0.8.164   # then: npx hyperframes media-treatment --selector '#clip' --apply`

#### GLOW-37 · مكتبة مؤثرات ريموشن · Remotion @remotion/effects (glow · lightLeak · starburst · shine) · 📄 موصوف / documented only
- **ماذا / what:** قرابة 55 مؤثر WebGL2/Canvas تُطبَّق كمصفوفة effects على الفيديو أو الصورة، منها glow وlightLeak وstarburst وshine. — About 55 WebGL2/canvas effects applied as an effects array on Video/Solid/CanvasImage, including glow, lightLeak, starburst and shine.
- **متى أستخدمها / when:** مشاريع Remotion فقط — Remotion projects only.
- **كيف / how:** npx remotion add @remotion/effects; Config.setChromiumOpenGlRenderer('angle'); lightLeak({progress, seed, hueShift}) inside TransitionSeries.Overlay (hueShift 120 green, 240 blue); custom createEffect({type, backend: '2d'|'webgl2'|'webgpu', apply, schema}). @remotion/effects is NOT in this container's probe list — run `npm view @remotion/effects version` before promising it. **أرقام / params:** ~55 effects; hueShift 120 / 240.
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10436-remotion-markup/effects.md` · `kosif-atlas/skills/2712-remotion/10436-remotion-markup/light-leaks.md`
- **ترخيص / license:** Remotion company license (free for individuals and small teams; companies above the threshold need a paid license — remotion.dev/license).

#### GLOW-38 · تأثيرات ما بعد المعالجة على عناصر HTML · HTML-in-canvas post-FX & TypeGPU liquid glass · 📄 موصوف / documented only
- **ماذا / what:** التقاط عنصر HTML حي كنسيج ومعالجته بـ GLSL أو WGSL: بلوم ثلاثي الأبعاد، زجاج سائل، CRT، تموج، تفتت. — Capture live DOM as a texture and post-process it with GLSL/WGSL: 3D rotation with bloom, liquid glass, CRT, ripples, shatter.
- **متى أستخدمها / when:** عندما يجب أن يتوهج أو يتشوه نص HTML حقيقي — when real HTML type must bloom or distort.
- **كيف / how:** Effect catalogue (10): 3D rotation with bloom, magnetic cursor distortion, shatter, liquid surface, portal reveal, noise dissolve, holographic/iridescent, scan lines + CRT, frosted glass, pixel sort. TypeGPU: video-backed liquid glass, rounded-rect SDF pill, frosted blur via a downsample pass. Needs drawElementImage (html-in-canvas flag) + WebGPU in the render environment — not verified here; prefer the K3 or Canvas routes. **أرقام / params:** 10 named effects.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/adapters/html-in-canvas-patterns.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/adapters/typegpu.md`

#### GLOW-39 · مظهر الهولوجرام · Hologram look · 📦 بأمر تثبيت / one install
- **ماذا / what:** إضاءة حافة فرينل وخطوط مسح وإضافة ووميض خفيف وبلوم بعتبة منخفضة تصنع هولوجرامًا. — Fresnel rim + scanlines + additive blending + slight flicker + low-threshold bloom make a hologram.
- **متى أستخدمها / when:** واجهات خيال علمي، رسائل مستقبلية — sci-fi UI, future messages.
- **كيف / how:** three.js: emissive += rimColor·pow(1 − |dot(eye, normal)|, 2–4); fragment scanline term sin(y·k + t) with ≈300–800 lines over the screen height; AdditiveBlending, depthWrite false; a slight opacity flicker (a few %, never a strobe); bloom threshold low. Or the WebGPU 'Hologram' plate (pale blue orb with scan rings, GLOW-52). **أرقام / params:** fresnel power 2–4; 300–800 scanlines/screen.
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md` · `kosif-one/vendor/hyperframes/registry/blocks/hologram/hologram.html`
- **📦 تثبيت / install:** `npm i three@0.186.1   # or: npx hyperframes@0.8.164 add hologram (WebGPU)`

#### GLOW-40 · التوهج على النص علامة توليد · QA: glow on type is a tell · ✅ مُثبت هنا / proven here
- **ماذا / what:** فحص الجودة يحذّر من ظل نص كبير أو ملون لأنه علامة سريعة على عمل مولَّد؛ الظل الداكن الناعم أفضل. — The QA linter flags large or coloured text-shadow as a quick tell of generated work; prefer dark soft shadows.
- **متى أستخدمها / when:** قبل كل رندر نهائي فيه نص — before every final render with type.
- **كيف / how:** qa.py lint warns when text-shadow blur ≥ 20 px or the shadow colour is not black. Glow belongs on one hero word or a neon sign (GLOW-01/04), never on captions or body text — the owner playbooks list 'glow and chromatic aberration on body text' as a do-not. **أرقام / params:** warn: text-shadow blur ≥ 20 px or non-black.
- **الدليل / proof:** `kosif-studio/motion/qa.py:68` · `kosif-tool/playbooks/kinetic-type.md:104`

## اللمعات والمسح الضوئي — Sheens, sweeps & glints

_شريط ضوء يعبر مرة واحدة ثم يسكن: داخل الحروف، على الزجاج، على المنتج، أو كخط مسح._

#### GLOW-41 · مسحة ضوء على جملة الذروة · Payoff light sweep through letterforms · ✅ مُثبت هنا / proven here
- **ماذا / what:** شريط ساطع يعبر الكلمة عبر تدرج مقصوص على النص، فيعطي لمعة معدنية على كلمة الختام. — A bright band travels through the word via a gradient clipped to the text — a metallic glint on the payoff word.
- **متى أستخدمها / when:** الجملة الختامية، اسم المنتج، الكلمة المكررة في الأغنية — payoff lines, product names, refrains.
- **كيف / how:** background-clip:text with an oversized gradient (background-size 300% 100%) and tween background-position. Set the gradient with background-image (the 'background' shorthand placed after background-clip resets the clip and paints a solid block). LTR sweep 100%→0% travels left→right; for Arabic run 0%→100% so the light moves with the reading (the vendored shimmer utility auto-reverses for RTL). Payoff mode: dim everything else to .3, the line slams from scale 1.08 + blur 16. Variants: HyperFrames text-shimmer (sweep_at 1.2 s), shimmer-sweep, chrome-sweep / spotlight-sweep primitives on downbeats (0.6–2 s). Verified here: Arabic «القمّة» swept in the render_html test. **أرقام / params:** gradient 100°: ivory 0–40%, #fff7e2 47%, #fff 50%, #fff7e2 53%, ivory 60–100%; 0.75 s power2.inOut (verse 1.0 s); drop-shadow 0 4px 18px rgba(0,0,0,.5); shimmer util 2 s linear, spread calc(3ch + 40px).

```css
.payoff { color: transparent; -webkit-background-clip: text; background-clip: text;
  background-image: linear-gradient(100deg, #e9dfc8 40%, #fff7e2 47%, #fff 50%, #fff7e2 53%, #e9dfc8 60%);
  background-size: 300% 100%; filter: drop-shadow(0 4px 18px rgba(0,0,0,.5)); }
/* seek(t): s = ease(clamp01((t - t0) / .75));
   el.style.backgroundPosition = (rtl ? 100*s : 100 - 100*s) + '% 50%'; */
```

- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:35` · `100-superskills/skills/kosif-montage-motion/templates/directed.html:120` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/gradient-text-sweep.md` · `kosif-audit-pro/vendor/shadcn-tailwind-4.13.0.css:536`

#### GLOW-42 · لمعة البطاقة والزر وانعكاس الزجاج · UI sheen family: card scan, button glint, one-pass glass band · 🟢 جاهز / ready
- **ماذا / what:** شريط ضوء قطري يعبر البطاقة مرة، ولمعة بيضاء على الزر، وشريط انعكاس يعبر زجاج الهاتف مرة لكل دوران — ولا شيء يتكرر. — A diagonal band crosses the card once, a white glint crosses the button, a reflection band crosses phone glass once per rotation — nothing loops.
- **متى أستخدمها / when:** الإجراء التالي في واجهة، زر الدعوة، دوران هاتف — next-action cards, CTAs, phone turns.
- **كيف / how:** Card: ::before inset −65% −18%, linear-gradient(112deg, transparent 42%, primary 10% at 50%, transparent 58%), translate 42%→−42% with rotate 6deg. Button: ::after 24% wide, rotate(14deg), transparent → rgba(255,255,255,.55) → transparent, translateX 0→520% (fine pointers only). Glass: linear-gradient(115deg, transparent 40%, rgba(255,255,255,.14) 50%, transparent 60%) once per rotation; emerging-from-dark variant 1800 ms at 25%. HyperFrames gloss-sweep: card lands with a restrained slam and catches one specular sweep (angle 25°, −60..60). **أرقام / params:** card 950 ms ease-cinematic, delay 260 ms, peak 35%; button 720 ms, opacity 0→.9 at 24%→0; glass 1.2 s cubic-bezier(.33,1,.68,1) peak .12–.16.
- **الدليل / proof:** `kosif-audit-pro/app/globals.css:1142` · `kosif-audit-pro/app/globals.css:412` · `kosif-tool/playbooks/phone.md:42` · `kosif-one/vendor/hyperframes/registry/components/gloss-sweep/gloss-sweep.html`

#### GLOW-43 · مرور الضوء المفتاحي على المنتج · Travelling key-light pass (product hero, light-thread reveal) · 📦 بأمر تثبيت / one install
- **ماذا / what:** ضوء مفتاحي يعبر المشهد مرة فيتغير كل بريق وظل معه، أو خيط ضوء يكشف حواف منتج داكن قبل إضاءته كاملًا. — A key light crosses the scene once and every highlight and shadow shifts with it, or a thin light thread traces a dark product's outline before it is fully lit.
- **متى أستخدمها / when:** لقطة المنتج البطل، منتجات داكنة، إعلانات فاخرة هادئة — hero product shots, dark products, quiet-premium ads.
- **كيف / how:** HyperFrames light-sweep-pass: one --light-x custom property drives the soft diagonal band and all slotted highlights/shadows in lockstep. Ads playbook: push 3–5% per beat or a 15–30° turn + a light sweep of 800 ms, product ≥ 40% of frame height. MG-037 (dark product): 0–1 s partial dark, 1–3 s sweep, 3–5 s full reveal via a moving light mask over differently exposed copies — fake light cannot recover missing detail. S02 Quiet premium: slow scale 1.00→1.04, few transitions. **أرقام / params:** angle 115° (60–160); sweep_at .9 s; strength subtle|standard; sweep 800 ms.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/light-sweep-pass/light-sweep-pass.html` · `kosif-tool/playbooks/ads.md:18` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-product-ads.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/styles.md`
- **📦 تثبيت / install:** `npx hyperframes@0.8.164 add light-sweep-pass`
- **ترخيص / license:** HyperFrames (Apache-2.0) components animate with GSAP 3.14 — GSAP standard 'no charge' license (gsap.com/standard-license), not OSI.

#### GLOW-44 · لمعة تدور مع الجسم · Rotation-locked specular sheen (fake 3D, chrome) · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** وجه الجسم يُضاء حسب زاوية دورانه، ولمعة متدرجة تنزلق عليه بقدر الدوران. — The object's face brightens by its rotation angle and a gradient highlight slides across it in proportion.
- **متى أستخدمها / when:** مفاتيح وعملات وشعارات معدنية بثلاثي أبعاد مزيف — keys, coins, metal logos in fake 3D.
- **كيف / how:** Build recipe: fixed light from top-left; face brightness = max(0, dot(normal, lightDir)); move a linear-gradient highlight stop across the face ∝ rotation angle; extruded edge one shade darker. Music cue: HyperFrames chrome-sweep primitive on downbeat/reveal (0.6–1.4 s). **أرقام / params:** light fixed top-left; sweep ∝ angle.
- **الدليل / proof:** `style:fake3d` · `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/chrome-sweep/scene.html`

#### GLOW-45 · خط مسح ليزري وشريط إضاءة يمسح الكود · Laser scan line & scanning highlight bar · 🟢 جاهز / ready
- **ماذا / what:** خط أحمر متوهج يصعد وينزل داخل إطار مسح، أو شريط ضوء يمسح الكود فتبيض الأسطر التي يعبرها. — A glowing red line sweeps up and down inside a scan frame, or a light bar travels down code and the lines it passes turn white.
- **متى أستخدمها / when:** مسح باركود، تحليل، قراءة كود — barcode scans, analysis beats, code walkthroughs.
- **كيف / how:** Laser: height 2 px, background var(--sk-bad), box-shadow 0 0 8px; @keyframes top 10%→90%→10% 2 s ease-in-out infinite; frame 2 px dashed rgba(255,255,255,.85) + box-shadow 0 0 0 4000px rgba(0,0,0,.45) to darken the surround. Code bar: 2 px core + 40 px soft gradient above, ≈1 line per 80 ms, yellow #f2c230 at α .6, passed lines grey→white. **أرقام / params:** 2 s cycle; glow 8 px; surround .45; code bar 1 line / 80 ms.
- **الدليل / proof:** `kosif-earth-ci-fork/ui/features/enterprise.css:348` · `style:pm-kyonax-on-tech-aabc1d` · `style:pm-tstfully-0aa6b4`

#### GLOW-46 · بريق نجمي وشرر القلم · Twinkle sparkles & pen sparks · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** نجوم رباعية تكبر وتدور وتختفي حول العنوان، وشرر صغير حتمي حول رأس القلم. — 4-point stars scale up, spin and vanish around a headline; small deterministic sparks around a pen head.
- **متى أستخدمها / when:** اكتشاف إيجابي، كلمة «جديد»، كتابة يدوية — positive discoveries, 'new', handwriting heads.
- **كيف / how:** Build recipe: star path scale 0→1→0 with rotation over 600 ms at seeded positions, 6–10 alive at once; pen head: radial glow r .07·m α .42 + 8 deterministic 2 px sparks within .01–.045·m redrawn each frame from a per-frame seed (Basma). Sparkle means good news only (attention menu). **أرقام / params:** life 600 ms; 6–10 concurrent; 8 sparks 2 px.
- **الدليل / proof:** `style:pm-deebeeeff-50fcd0` · `app/public/js/10_studio.js:267`

## الأشعة والفلير والتسريب والوميض — Rays, flares, leaks & flashes

_الضوء الذي يُرى في الهواء أو في العدسة: أشعة، فلير، تسريب ضوء، ووميض يقطع._

#### GLOW-47 · أشعة إلهية وبلوم فوق اللقطة بـ CSS · CSS god rays & bloom layer over footage · ✅ مُثبت هنا / proven here
- **ماذا / what:** أشعة مخروطية متكررة مقنّعة لتتلاشى للأسفل، وبلوم شعاعي دافئ بوضع screen قرب البطل، فوق لقطة حقيقية أو رسم. — Repeating conic rays masked to fade downward and a warm radial bloom in screen mode near the subject, over real footage or drawings.
- **متى أستخدمها / when:** أبواب تنفتح، دعاء، لحظة كشف، إعلان فاخر — doors opening, duas, reveals, premium edits.
- **كيف / how:** #rays repeating-conic-gradient(from 168deg at 590px −260px, 0° → α .13 at 2.2° → 0 at 5° → 0 at 9°), mix-blend screen, mask linear 0 → .6 → transparent at 75%; #bloom radial ellipse 380×520 at 60px 300px rgba(255,214,150,.5) → .16 → 0, screen; bottom scrim 52%→100% to .74 for captions; deliberate dip to black .32 s power2.in. 2D variant: warm trapezoids #ffc76a at 20–35% with linear fade + 30–60 twinkling motes. Verified here (render_html test: rays + pool + vignette). **أرقام / params:** rays 2.2°/5°/9° α .13; bloom .5→.16→0; cues bloom .85 at 3.6 s, 1.0 at 11.55 s, rays .45→1 at 16 s.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:20` · `kosif-studio/motion/projects/premium_edit/index.html:20` · `style:fake3d`
- **فيديوهات مرجعية / reference videos:** `style:pm-abderrahmen-g-9e8ed0`

#### GLOW-48 · أشعة الشمس في المشهد ثلاثي الأبعاد · Screen-space god rays (3D sun) · 🟢 جاهز / ready
- **ماذا / what:** ضبابية شعاعية بـ 64 عينة من موضع الشمس على الشاشة، مقصورة على البكسلات الساطعة ومنطقة السماء. — A 64-tap radial blur from the on-screen sun, limited to bright pixels and the sky region.
- **متى أستخدمها / when:** شروق، غابة، ماء، عاصفة تنقشع — sunrises, forests, water, clearing storms.
- **كيف / how:** Inside makePost: post.rays.uniforms.uAmount.value = k only while post.sunOnScreen(sun) is true; dithered and masked above the sun height to avoid water-glitter lattices. Time it: amount = inFront ? .9·(1 − smooth(2.5, 5, t)) + .3 + .35·overcast : 0; music: .35 + .45·kick toward an eclipse. **أرقام / params:** 64 samples; stride .55 of sun distance; decay .972/sample; luma threshold .7; output ×.55.
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:378` · `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:372` · `100-superskills/skills/kosif-montage-motion/scripts/projects/water_cycle_3d/src/main.js:99` · `100-superskills/skills/kosif-montage-motion/scripts/projects/sound_ground/src/main.js:129`

#### GLOW-49 · انفجار أشعة شمسي دوّار · Rotating sunburst / ray-burst backdrop · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** أشعة رفيعة من مركز تدور ببطء خلف شعار أو بطل أو كلمة «ترقية»، بشعاع مركزي أبيض وحافة قوس قزح أحيانًا. — Thin rays from a centre rotate slowly behind a logo, hero or LEVEL UP stamp, sometimes with a white central beam and rainbow fringe.
- **متى أستخدمها / when:** احتفال، ترقية، تمائم، عنوان تريلر — celebrations, level-ups, mascots, trailer titles.
- **كيف / how:** Build recipe: repeating-conic-gradient wedges (24–48 thin rays, or 12–16 alternating purple/magenta for level-ups), radial mask, screen blend, rotate 2–20°/s; golden backdrop = radial + conic rays + rings at .4; trailer: radial streaks behind a bevelled gold serif (#f1d38a→#8a5a1a), frame within frame. WebGPU 'SunBurst' plate as an alternative (GLOW-52). **أرقام / params:** 24–48 rays (12–16 for level-up); rotate 20°/s; opacity .4.

```css
.burst { position:absolute; inset:-50%; mix-blend-mode:screen;
  background: repeating-conic-gradient(from 0deg at 50% 50%,
    rgba(255,214,150,.22) 0deg 7.5deg, transparent 7.5deg 15deg);      /* 24 rays */
  -webkit-mask-image: radial-gradient(circle, #000 10%, transparent 60%); }
/* seek(t): burst.style.transform = `rotate(${20 * t}deg)` */
```

- **الدليل / proof:** `style:pm-gizakdag-b8c59e` · `style:pm-ibrahimwasim240-809370` · `style:pm-kentcdodds-6fa8cf` · `style:pm-emollick-8661a8`

#### GLOW-50 · وهج العدسة ثلاثي الأبعاد · 3D lens flare that follows the sun · 🟢 جاهز / ready
- **ماذا / what:** فلير من خمسة عناصر مولّدة (أقراص وحلقات) مثبت باتجاه الشمس ويختفي حين تُحجب. — A five-element flare from generated soft and ring sprites, placed along the sun direction and hidden when the sun is occluded.
- **متى أستخدمها / when:** شروق وغروب ولقطات سماء في three.js — sunrise/sunset and sky shots in three.js.
- **كيف / how:** const f = K3.makeLensflare({color}); place at sunDir × 9000 + camera.position; f.visible = post.sunOnScreen(sun) (e.g. && t < 7.5); fade it with overcast and lightning. **أرقام / params:** soft 420 px @0 #ffe2b0; ring 90 @.35 #ffd0a0; soft 60 @.55 #aad4ff; ring 140 @.75 #ffc8a0; soft 40 @.95 #ffffff.
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:312` · `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:312` · `100-superskills/skills/kosif-montage-motion/scripts/projects/water_cycle_3d/src/main.js:99`

#### GLOW-51 · فلير أنامورفي بأشباح · Anamorphic flare with ghosts (painter + streak field) · ✅ مُثبت هنا / proven here
- **ماذا / what:** قلب ناعم وخط أفقي طويل بداخله خط أبيض، وأقراص أشباح باهتة معكوسة عبر مركز الإطار. — A soft core glow, a long horizontal streak with a white inner streak, and faint ghost discs mirrored through the frame centre.
- **متى أستخدمها / when:** مصابيح سيارات، شمس منخفضة، نقطة ضوء بطلة، لقطات خيال علمي — headlights, low suns, hero light points, sci-fi.
- **كيف / how:** Painter: flare(centre, colour, size, streak, strength, ghosts=3) = glow(core) + additive streak ellipse (streak × .09·size) + white inner streak (.55·streak × .04·size) + ghosts at t = 1 + .55k mirrored through the centre — ran here 2026-10-16. Screen-space version: 3–5 ghost rings along the sun→centre axis + bloom on highlights > .9. Many-point field: HyperFrames vfx-anamorphic-flare (140 drifting emitters, high-pass .3, 80 horizontal taps at ¼ res, tint #7a8aff). **أرقام / params:** default #ffb070, size 120, streak 420, strength .6 (whale 100/360/.38); field intensity 5, streakLength 1 (0.1–6), timeScale .5, backdrop #04040a.
- **الدليل / proof:** `kosif-studio/render.py:741` · `kosif-studio/scenes/whale_dragon.py:287` · `kosif-one/vendor/hyperframes/registry/blocks/vfx-anamorphic-flare/vfx-anamorphic-flare.html` · `style:pm-axtonliu-0b861d`
- **فيديوهات مرجعية / reference videos:** `style:pm-nft-chen-5f8bb0` · `style:pm-justincooperman-e7bbc4`

#### GLOW-52 · ألواح ضوء WebGPU جاهزة · WebGPU shader light plates (Godrays · LensFlare · LightEdge · Prism …) · 📦 بأمر تثبيت / one install
- **ماذا / what:** لوحات خلفية بمظللات WebGPU لمدة ثانيتين: أشعة إلهية، فلير، حافة مضيئة، منشور، خيوط ضوء، شفق وغيرها. — 2-second WebGPU shader backgrounds: god rays, lens flare, light edge, prism, light strands, aurora and more.
- **متى أستخدمها / when:** خلفية تحت العناوين حين يتوفر WebGPU — background plates under titles when WebGPU is available.
- **كيف / how:** `npx hyperframes@0.8.164 add <id>` or put lib/shaders.iife.js beside the HTML and declare <canvas data-shader='Godrays' width=1920 height=1080> in a root marked data-requires-webgpu data-no-timeline. A WebGPU adapter exists here only with --enable-unsafe-webgpu --enable-features=Vulkan --use-angle=swiftshader --enable-unsafe-swiftshader (checked 2026-10-16); no plate has been rendered yet — preview one frame first. The library has 36 looks; the light ones are in the table below. **أرقام / params:** 1920×1080; 2 s; shaders.iife.js 1,444,793 bytes (shaders 4.0.0).

| data-shader | look |
|---|---|
| Godrays | light rays fan from a corner across a deep blue field |
| LensFlare | star-burst flare with a faint rainbow halo shimmering on black |
| LightEdge | purple and cyan light racing around an orb edge |
| Prism | a white beam splitting into a slowly turning rainbow |
| SunBurst | cream and black rays fanning from centre, slowly turning |
| Strands | thin pink and blue light ribbons weaving across black |
| SineWave | a glowing white sine wave travelling across black |
| FallingLines | white lines falling at varied speeds, leaving fading trails |
| Hologram | pale blue holographic orb with scan rings and flicker |
| Aurora | green/violet aurora curtains rippling over a night sky |

- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/godrays/godrays.html` · `kosif-one/vendor/hyperframes/registry/blocks/lens-flare/lens-flare.html` · `kosif-one/vendor/hyperframes/registry/blocks/aurora/lib/shaders.THIRD-PARTY-LICENSES.txt`
- **📦 تثبيت / install:** `npx hyperframes@0.8.164 add godrays`
- **ترخيص / license:** Shader library MIT (Shader Effects Inc., shaders 4.0.0) + HyperFrames Apache-2.0 — ship lib/shaders.THIRD-PARTY-LICENSES.txt with the film.

#### GLOW-53 · تسريب ضوء وحرق فيلم · Light leak, overexposure & film-burn transition · 📦 بأمر تثبيت / one install
- **ماذا / what:** ضوء دافئ يغسل القطع، أو تحترق اللقطة إلى الأبيض، أو بقع حرق تعبر الإطار. — Warm light washes over the cut, the outgoing shot blows out to white, or burn blobs sweep across.
- **متى أستخدمها / when:** ذكريات، انتقال مُبرَّر، مونتاج دافئ — memory beats, motivated transitions, warm montages.
- **كيف / how:** CSS: oversized (≥2400 px) blurred warm blobs moving x 300–600 px at opacity .4–.9 over ≈.5 s; overexposure: filter brightness(1.5)→(3) + scale 1.03→1.06, then a white overlay 0→1→0 over ≈.9 s. Drifting canvas leak (Basma): radial at x = W·(.5 + .65 sin .31t), y = H·(.12 + .1 cos .23t), r = .75·max(W,H), rgba(255,170,90,leak) → rgba(255,80,60,.35·leak) at 45% → 0, globalCompositeOperation 'screen'. Rainbow wash: full-frame blurred gradient pass 600 ms. Ready-made: HyperFrames organic-light-leak-overlay (4 s), the 'light-leak' WebGL transition. **أرقام / params:** leak 0–.6 (AutoEdit up to .9); blobs ≥2400 px; brightness 1.5→3; burn ≈.9 s.
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/transitions/css-light.md` · `app/public/js/00_editor.js:287` · `kosif-one/vendor/hyperframes/registry/blocks/organic-light-leak-overlay/organic-light-leak-overlay.html` · `style:pm-gizakdag-cf4ae6`
- **فيديوهات مرجعية / reference videos:** `style:fake3d`
- **📦 تثبيت / install:** `npx hyperframes@0.8.164 add organic-light-leak-overlay   # or: cd /home/user/app && npm install (Basma)`
- **ترخيص / license:** HyperFrames (Apache-2.0) components animate with GSAP 3.14 — GSAP standard 'no charge' license (gsap.com/standard-license), not OSI.

#### GLOW-54 · ومضة الإطار وانفجار الضوء · Flash frame, double strike & light-burst transition · ✅ مُثبت هنا / proven here
- **ماذا / what:** ومضة بيضاء أو بلون التمييز مع ضربة ثانية اختيارية، أو كرة ضوء بحلقة وخط أنامورفي تكبر ثم يقطع المشهد. — A white/accent flash with an optional second strike, or a light orb with a ring and anamorphic streak that scales up before the cut.
- **متى أستخدمها / when:** الاصطدام، بداية قسم، ذروة عاطفية، انتقال شوريل — impacts, section starts, emotional peaks, showreel cuts.
- **كيف / how:** MOTION.flash(tl, el, at, {peak, dur, again}) on a full-frame div. Warm accent version: radial-gradient(circle at 50% 55%, #fff1c8, #ffbf6b 45%, transparent 80%) with mix-blend screen on the three emotional peaks only. Light-burst transition: white-core/blue-halo orb + thin ring + full-width anamorphic streak (4–6 px, 20 px blur) + short radial sparks, scale .3→1.2 over ≈300 ms additive, then cut. Hit flash 80 ms linear + 8 ghosts over 120 ms. Respect ≤3 flashes/s. Verified here (render_html test: .06 s attack, cubic decay .35 s). **أرقام / params:** attack .06 s to .85; decay .35 s power4.out; again 50% at +.16 s; dua peaks 10.99 s .55/.9 · 18.75 s .35/.6 · 22.95 s .6/1.1.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:325` · `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:325` · `kosif-one/projects/thursday-dua-animation/source/index.html:212-217` · `style:pm-marouanegazouzi-6071d5`
- **فيديوهات مرجعية / reference videos:** `style:pm-notdwd-7de38a` · `style:pm-kantamk-61f410`

#### GLOW-55 · أشعة يلقيها النص ونص بشعاع المؤشر · Volumetric rays cast by a wordmark / cursor-light text · 📦 بأمر تثبيت / one install
- **ماذا / what:** كلمة تُلقي أشعة ضوء حجمية نحو مؤشر ضوء يتحرك، أو نص يُكشف بتوهج المؤشر وظلال لونية. — A wordmark casts volumetric light rays toward a sweeping light cursor, or text is revealed by a cursor glow with chromatic shadow rays.
- **متى أستخدمها / when:** كشف اسم علامة، ذروة موسيقية طويلة — brand-name reveals, long musical phrases.
- **كيف / how:** HyperFrames text-spectral-rays primitive (the shader owns the wordmark; anchor to phrase/sweep events, best span 2.5–5 s) or the vfx-text-cursor block (WebGL + Canvas 2D + SVG, 8 s). Arabic: render the shaped whole word to a texture first; the block's default font (Big Shoulders Display) is Latin-only. **أرقام / params:** spectral rays 2.5–5 s; text-cursor 8 s 1920×1080.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/text-spectral-rays/scene.html` · `kosif-one/vendor/hyperframes/registry/blocks/vfx-text-cursor/vfx-text-cursor.html`
- **📦 تثبيت / install:** `npx hyperframes@0.8.164 add vfx-text-cursor`
- **ترخيص / license:** HyperFrames (Apache-2.0) components animate with GSAP 3.14 — GSAP standard 'no charge' license (gsap.com/standard-license), not OSI.

#### GLOW-56 · الشمس والهالة والكسوف · Blooming sun, corona & eclipse (2D and 3D) · 📦 بأمر تثبيت / one install
- **ماذا / what:** شمس بثلاث طبقات توهج وأشعة دوارة، وشروق خلف الأفق، وقرص قمر أسود بهالة برتقالية تتسع مع الباص. — A sun with three stacked glows and slowly turning rays, a sunrise behind the horizon, and a black moon disc whose orange corona widens with the bass.
- **متى أستخدمها / when:** قصص الزمن والأمل، أغانٍ، ختام علامة — time/hope stories, songs, brand finales.
- **كيف / how:** 2D: noise-textured disc core #fcfaca → mid #f7b54a → outer #c0461c, additive outer glow as 3 stacked blurs 40/120/300 px, ray sprites rotating ≈2°/s, intensity ramps per section; finale: brand-colour radial (radius 60% of frame) rising behind the horizon over 2 s easeOut. 3D shader: disc = 1 − smoothstep(.072, .075, r); corona = exp(−max(0, r − .074)·(46 − 12·uBass))·(.55 + 1.1·uBass), colour (1, .42, .16), uBass = clamp(bass·1.1 + kick·.35). Black sun: dark disc + thin emissive annulus (≈2% of radius, strength 20–40, #f2d7a8), bloom threshold .8, jagged edge noise. **أرقام / params:** blurs 40/120/300 px; rays 2°/s; corona falloff 46 − 12·bass.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/sound_ground/src/main.js:23` · `style:pm-samaote-5e2fc2` · `style:pm-aschapmann-131210` · `style:pm-theparuchh-6e08c3`
- **فيديوهات مرجعية / reference videos:** `style:pm-nolkeeg-bf062e`
- **📦 تثبيت / install:** `npm i three@0.186.1 esbuild   # rebuild sound_ground as-is; or port the shader to window.K3`

## إضاءة الاستوديو والحافة وحسابات الضوء — Studio light, rim & light maths

_إضاءة كما في موقع التصوير: نسب بالوقفات، حرارة لون بالكلفن، نعومة من حجم المصدر — وحاسبة تثبت الأرقام._

#### GLOW-57 · إضاءة ثلاثية بالوقفات والكلفن · Three-point rig in stops & Kelvin (K3.lightRig) · ✅ مُثبت هنا / proven here
- **ماذا / what:** مفتاح وتعبئة وحافة تُحدَّد كما في موقع التصوير: التعبئة N وقفات تحت المفتاح، والحافة M وقفات، ولكل ضوء حرارته. — Key, fill and rim set as on a real set: fill N stops under key, rim M stops over/under, each light with its own Kelvin.
- **متى أستخدمها / when:** كل مشهد ثلاثي الأبعاد — وإعداد واحد للفيلم كله لا إضاءة رمادية افتراضية — every 3D scene; one rig per film.
- **كيف / how:** rig = K3.lightRig(scene, {...}); rig.set({...}) per shot; rig.ratio() reports the lighting ratio. Playbook rule: one rig per film, never default grey lighting; minimal three.js sample Hemisphere(0xffffff, 0x223344, .6) + Directional(0xffffff, 1.2) at (3,4,2). Verified here: ratio() = 5 with the defaults (K3 bundle in Chromium). **أرقام / params:** key 3.0 @5600 K az −40 el 35 (shadows); fill 6500 K az 45 el 10, −2 stops (5:1); rim 4300 K az 160 el 40, +.5 stop; distance 10.

```js
const rig = K3.lightRig(scene, {key: 3, keyK: 5600, keyAz: -40, keyEl: 35,
  fillK: 6500, fillStops: 2, rimK: 4300, rimStops: 0.5});
rig.ratio();              // 5  → 5:1 'dramatic' (verified here)
rig.set({fillStops: 1});  // softer shot → 3:1
```

- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:1009` · `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:1009` · `kosif-tool/playbooks/3d.md:15` · `kosif-tool/playbooks/3d.md:60-61`

#### GLOW-58 · قوالب البورتريه السبعة · Seven portrait rig presets (K3.lightPreset) · 🟢 جاهز / ready
- **ماذا / what:** إعدادات مصوري البورتريه كتركيبات جاهزة، ونعومة الظل محسوبة من حجم المصدر ومسافته. — Photographers' portrait setups as ready rigs, with shadow softness derived from source size and distance.
- **متى أستخدمها / when:** شخصيات ثلاثية الأبعاد، رؤوس، منتجات على هيئة شخصية — 3D characters, busts, character-like products.
- **كيف / how:** const rig = K3.lightPreset(scene, name, {target, distance, key}); rig.softness gives the apparent size in degrees (shadow.radius = deg/3). Table below. **أرقام / params:** الجدول أدناه / see the table below.

| preset | key (az / el) | fill | rim | source size |
|---|---|---|---|---|
| rembrandt | −75 / 40 | −2.5 stops | −0.5 at az 150 | 1.0 m |
| clamshell | 0 / 55 | below (el −25) −1 | −1.5 | 0.9 m |
| edgy | overhead 0 / 60 | −4 | two rims +0.8 at az ±140 | 0.6 m |
| ultrasoft | −35 / 30 | −0.8 | −0.3 | 2.1 m |
| short | 55 / 30 | −2.5 | 0 | 0.9 m |
| broad | −55 / 30 | −2.0 | −1 | 0.9 m |
| sun | hard low sun 3600 K, −60 / 18 | sky fill 9000 K −2.3 | −1 | 0.05 m |

- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:1108` · `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:1110` · `kosif-studio/motion/references/book-lessons.md`

#### GLOW-59 · ثمانية عشر إعداد إضاءة وخطة الطاقم · 18 named lighting setups & the /lightplan deliverable · 📄 موصوف / documented only
- **ماذا / what:** جدول إعدادات بالزاوية والنسبة والكلفن والمزاج وجملة برومبت، وخطة إضاءة كاملة يمكن تسليمها لطاقم أو إعادة بنائها ثلاثيًا. — A preset table with angle, ratio, Kelvin, mood and a prompt fragment, plus a full lighting plan a crew can execute or 3D can rebuild.
- **متى أستخدمها / when:** قبل التصوير، أو لوصف إضاءة لمولّد صور، أو لمطابقة مزاج — pre-shoot plans, prompt lighting, mood matching.
- **كيف / how:** Pick a setup → compute ratios/gels with light_calc (GLOW-60) → /lightplan: mood line → ASCII top view (12 = behind, 6 = camera) → per-light table (role, fixture, modifier, power/stops, height, angle, distance, gel) → computed ratios & exposure → camera ISO/shutter/aperture/WB → budget version (window + lamp + foam board + phone light) → common mistakes → English prompt fragment. /relight freezes identity/pose. Product: big soft key + fill + rim to edge glass/metal, one consistent shadow; Kelvin per source, avoid unintended mixing. **أرقام / params:** الجدول أدناه / see the table below.

| setup | key / numbers | mood |
|---|---|---|
| Rembrandt | 45° side, cheek triangle, 4:1 (catalog: ~3:1), 5600 K (catalog: ~3200 K) | classic drama |
| Loop | 30°, 3:1 | natural portrait |
| Butterfly / Paramount | front-high beauty dish, clamshell fill, 2:1 | beauty |
| Clamshell | 1.5:1 | soft beauty |
| Split | 90°, 8:1+ | conflict, duality |
| Broad · Short | 3:1 · 4:1 | widen · slim the face |
| Chiaroscuro | one hard source, no fill | painterly noir |
| High-key | background +1.5 stops, 1.5:1 | clean, commercial |
| Low-key | 8:1+, 3200–5600 K | noir |
| Cinematic teal-orange | 3200 K key vs 6500 K ambient, 4:1 | blockbuster |
| Neon noir / neon practical | magenta + cyan on wet surfaces | night city |
| Golden-hour backlight | sun 10–20° (≈15°), 3200–3500 K, 3:1, rim | warmth, nostalgia |
| Blue hour | 9000 K sky (7500–9000) / 2700 K lamps, ≈20 min after sunset | melancholy |
| Moonlight | 7000 K, 6:1 (catalog: 4100–6500 K silver) | night calm |
| Candle / firelight | 1800–2200 K (1900), 6:1, flicker | intimacy |
| Volumetric god rays | haze, 5600 K, shafts through fog/dust | awe, faith |
| Product rim + gradient | 2 strip boxes at 45° | premium product |
| Window light | 90°, 3:1, 5600–6500 K | documentary |
| Silhouette · Joel-Grimes edgy | rim only · two softboxes behind + beauty dish | mystery · sports hero |

Ratios: 2:1 commercial · 3:1 natural portrait · 4–8:1 dramatic · 8:1+ noir. Bigger/closer source = softer; doubling distance = −2 stops.

- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-lighting/references/lighting-presets.md` · `kosif-one/tools/kosif-omni/skills/kosif-lighting/SKILL.md` · `100-superskills/skills/kosif-montage-motion/references/visual-catalog.md` · `100-superskills/skills/photo-lighting-plan/SKILL.md:22`

#### GLOW-60 · حاسبة الضوء · Light calculator (ratio · softness · falloff · EV · guide number · shutter angle · mired) · ✅ مُثبت هنا / proven here
- **ماذا / what:** حسابات تصوير حتمية: نسبة الإضاءة ومزاجها، نعومة المصدر، سقوط الضوء بالمسافة، قيمة التعريض، وزاوية الغالق. — Deterministic photo/cinema maths: lighting ratio and mood, source softness, distance falloff, exposure value, shutter angle.
- **متى أستخدمها / when:** كل خطة إضاءة أو مشهد ثلاثي يجب أن يُصدَّق — any plan or 3D scene that must read as believable.
- **كيف / how:** echo '[{"op":"ratio","key_stops_over_fill":2}, ...]' | python3 scripts/omni/light_calc.py (or the MCP kosif_light_calc, list via ops=[…]); JS twins K3.softnessDeg(size, dist) = 2·atan(size/2d), K3.falloffStops(d1, d2) = 2·log2(d2/d1). Ran here 2026-10-16, results in params. **أرقام / params:** ratio 2 stops → 5:1 'dramatic' (≤2.5 flat, ≤4.5 natural, ≤9 dramatic, else noir); 4:1 → fill 1.58 stops; softness 1.2 m @1.5 m → 43.6° 'soft' (>45 very soft, >20 soft, >8 medium); falloff 2 m→4 m = 2 stops; EV f/2.8 1/125 ISO100 = 9.94; 24 fps @180° = 1/48 s; GN 60 ISO100 5 m → f/12; mired 5600→3200 = +133.9 Full CTO.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/omni/light_calc.py:40` · `kosif-one/tools/kosif-omni/skills/kosif-lighting/scripts/light_calc.py:45` · `kosif-one/tools/kosif-omni/mcp-server/tests/test_server.py:198` · `kosif-studio/motion/kit/three-kit.js:1026`

#### GLOW-61 · حرارة اللون والجيلاتين ومصادر مسماة · Kelvin → RGB, gels & 19 named light sources · ✅ مُثبت هنا / proven here
- **ماذا / what:** تحويل الكلفن إلى لون RGB، وحساب إزاحة المايرد وأقرب جيلاتين CTO/CTB، وجدول 19 مصدر ضوء حقيقي. — Kelvin → linear RGB, the mired shift and nearest CTO/CTB gel, and a table of 19 real light sources.
- **متى أستخدمها / when:** القمر والفوانيس ومصابيح الصوديوم والنيون — أي ضوء يجب أن «يُقرأ» فيزيائيًا — moons, lanterns, sodium lamps, neon.
- **كيف / how:** K3.kelvin(K) → THREE.Color (Tanner Helland Planckian fit, 1000–40000 K); K3.gel(fromK, toK) → {mired, gel}; K3.lightColor(name) from K3.LIGHT_SOURCES. Verified here: kelvin(1900) = #ff8400, kelvin(3200) = #ffb87b, gel(5600, 3200) = {mired 134, 'Full CTO'}. Shore lights kelvin(2200–3100) at 70% / kelvin(5200). **أرقام / params:** candle 1850 K, firelight 1900, sodium #ffa040, tungsten 2700, halogen 3200, sunrise 3000, golden_hour 3500, led_warm 3000, led_neutral 4000, mercury #bff0dc, metal_halide 4300, fluorescent #e8f5e6, moonlight #9fb4d9, daylight 5600, overcast 6500, open_shade 8000, blue_sky 11000, neon_red #ff2a3a, neon_blue #3a7bff; gels Full CTB −159 · ½ −68 · ¼ −30 · ⅛ −12 · ⅛ CTO +20 · ¼ +42 · ½ +81 · Full +159.
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:992` · `kosif-studio/motion/kit/three-kit.js:1001` · `kosif-studio/motion/kit/three-kit.js:1183` · `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:137`

#### GLOW-62 · ارتداد السماء وضباب نحو الشمس · Sky bounce, fog toward the sun & blue-hour painting · 🟢 جاهز / ready
- **ماذا / what:** السطوح المظللة المواجهة للأعلى تبرد من السماء والمواجهة للأسفل تدفأ من الأرض، والضباب يدفأ فقط حين تواجه الكاميرا شمسًا منخفضة. — Up-facing shadow planes go cool from the sky, down-facing ones warm from the ground, and haze warms only when the camera faces a low sun.
- **متى أستخدمها / when:** الغروب والساعة الزرقاء والطبيعة — sunsets, blue hour, landscapes.
- **كيف / how:** K3.skyBounce(scene, {sky, ground, intensity}); K3.fogTowardSun(scene, camera, sunDir, cool, warm, amount) each frame (alignment³). Blue-hour recipe (Gurney lessons in 3D): aerialPerspective scatter [.55, .8, 1.3], AgX tone mapping exposure 1.05, FogExp2 #8790B0 .00062, fov 32, ridges at .7/1.4/2.6/4.5 km, sodium lamps with colour corona against the blue sky, weak sunrise-coloured directional .35 for the afterglow, 1600 stars on a rotating pole. **أرقام / params:** sky = blue_sky 11000 K, ground #b07a4a, intensity .6; blue_hour sky 0x5a7ab8 ground 0x6a4a36 1.25.
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:1194` · `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:1201` · `kosif-studio/motion/projects/blue_hour/src/main.js:1` · `100-superskills/skills/kosif-montage-motion/scripts/projects/blue_hour/src/main.js:93`

#### GLOW-63 · إضاءة الحافة في الرسم · Painter rim light & two-colour wet rims · ✅ مُثبت هنا / proven here
- **ماذا / what:** الحافة المواجهة لاتجاه الضوء تأخذ شريطًا ناعمًا من لونه — الحيلة التي تفصل الظلال عن الخلفية. — The edge band facing the light direction gets a soft band of its colour — the trick that separates silhouettes from the background.
- **متى أستخدمها / when:** شخصيات وصخور ومخلوقات في مشاهد مرسومة، أسطح مبللة — painted characters, rocks, creatures, wet surfaces.
- **كيف / how:** rim(shape, toward=(dx,dy), width, colour, alpha, soft=.6, mode='add') = shape mask minus a copy shifted away from the light, softened. Three-light cinematic setup: a cool key (moon/lightning), a warm key (fire/sunset) and a dim ambient; every body gets a rim from each key in its true direction, the warm one stronger near its source. Wet surfaces: two opposing rims. Ran here 2026-10-16. **أرقام / params:** width 2–4 (+ wide soft pass 8–10, soft 2–2.4, α .3); wet: rim((.7,−1), 2.6, '#ff9a4a', .8) + rim((−.4,−1), 1.8, '#9fb5da', .55); whale lights COLD (1010,120,520,#cfe0ff,1.0) · WARM (684,356,150,#ff8a3a,1.7) · AMBIENT (600,−400,900,#5a6c88,.35).
- **الدليل / proof:** `kosif-studio/render.py:412` · `kosif-studio/scenes/duck_dragon.py:229` · `kosif-studio/references/drawing-guide.md:62` · `kosif-studio/scenes/whale_dragon.py:30`

#### GLOW-64 · تظليل الحجم نحو الضوء · Form shading toward a light point · ✅ مُثبت هنا / proven here
- **ماذا / what:** تدرج شعاعي من اللون المضاء إلى الداكن مزاح نحو الضوء يجعل الشكل المسطح يبدو مستديرًا. — A radial gradient from lit to dark, offset toward the light, makes a flat shape read as rounded.
- **متى أستخدمها / when:** كرات، فواكه، رؤوس، أي حجم سريع في الرسم بالكود — orbs, fruit, heads, any quick volume.
- **كيف / how:** shade(shape, light_xy, lit, dark, core=.35, soft=0): hotspot offset = r·core toward the light, gradient radius r·(1 + core). Tested (test_studio.py:71) and ran here in the smoke render. **أرقام / params:** core .35; radius r·(1 + core).
- **الدليل / proof:** `kosif-studio/render.py:524` · `kosif-studio/tests/test_studio.py:71` · `kosif-one/tools/kosif-studio/render.py:524`

#### GLOW-65 · جسم مضاء فيزيائيًا وسحب مجسمة · Physically lit relief bodies & cloud decks · 📦 بأمر تثبيت / one install
- **ماذا / what:** يحوّل الشكل المسطح إلى حجم مضاء: حقل ارتفاع، نتوءات متعددة المقاييس، إضاءة نقطية حقيقية مع لمعة وفرينل وتشتت تحت السطح. — Turns a flat silhouette into a lit volume: height field, multi-scale bumps, real point lights with Blinn specular, Fresnel and subsurface scattering.
- **متى أستخدمها / when:** مخلوقات وجلود وسحب في المشاهد المرسومة — creatures, skins and clouds in painted scenes.
- **كيف / how:** relief(shape, lights, base, ambient, bulge, plateau, shininess, spec, bump, bump_cell, seed, fresnel, fres_col, soft, bumps=[(amp, cell)], sss, sss_col, roughness); clouds = relief(deck, [COLD, fire, AMBIENT], '#1c2430', .25, .9, .7, 8, .08, bumps=[(14,46),(5,14)], seed=12, soft=5, sss=8) between dark blurred fills. Needs OpenCV (Sobel normals) — not installed here. **أرقام / params:** ambient .22, bulge .6, plateau .5, shininess 30, spec .5; whale bumps [(2,40),(.9,12),(.3,3.5)], sss 2.5 #e8d8d0, roughness .55.
- **الدليل / proof:** `kosif-studio/render.py:573` · `kosif-studio/render.py:618` · `kosif-studio/scenes/whale_dragon.py:93`
- **📦 تثبيت / install:** `pip install opencv-python-headless`

#### GLOW-66 · مظلل البلورة: فرينل ولمعة وانعكاس سماء · Fresnel + Blinn glass/crystal shader · ✅ مُثبت هنا / proven here
- **ماذا / what:** مظلل يجعل البلورات المضلعة تُقرأ زجاجًا: لون بحسب الاتجاه، سماء منعكسة، حافة فرينل، لمعة حادة، وضباب. — A fragment shader that makes faceted crystals read as glass: body colour by normal, reflected sky, Fresnel rim, sharp Blinn highlight, fog.
- **متى أستخدمها / when:** بلورات، جليد، زجاج، هولوجرام، أغلفة جوية — crystals, ice, glass, holograms, atmospheres.
- **كيف / how:** Tested in the earth crystal world. Fresnel power 2–4 sells glass/atmospheres; Blinn-Phong half = normalize(eye + light), spec = pow(dot(n, h), shininess). **أرقام / params:** fresnel exp 2.6; spec exp 64; rim .9; fog near 6 far 24; key light dir (.5, .9, .6).

```glsl
vec3 ice = mix(iceA, iceB, N.y*.5 + .5);
vec3 sky = mix(skyA, skyB, smoothstep(-.6, .9, reflect(-V, N).y));
float ndl = max(dot(N, L), 0.), fres = pow(1. - max(dot(N, V), 0.), 2.6);
float spec = pow(max(dot(N, normalize(L + V)), 0.), 64.);
vec3 c = ice*(.35 + .65*ndl) + sky*.35 + rim*fres*.9 + spec*.8;
c = mix(c, c*tint, .6) + tint*glow*.35*fres;
c = mix(c, fogCol, smoothstep(6., 24., depth));
```

- **الدليل / proof:** `kosif-earth-ci-fork/ui/art/crystal-world.js:46` · `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md` · `kosif-atlas/skills/2221-webgpu-threejs-tsl/8405-webgpu-threejs-tsl/SKILL.md`

#### GLOW-67 · زجاج بانكسار وتشتت وكرات زجاجية · Refraction, dispersion & glass orbs · 📦 بأمر تثبيت / one install
- **ماذا / what:** أجسام زجاجية تكسر ما خلفها بمعامل انكسار، وتشتت لوني لكل قناة، وكرة زجاجية بلمعة علوية وهالات. — Glass that bends what is behind it by IOR, per-channel dispersion, and glass orbs with a top highlight and halos.
- **متى أستخدمها / when:** عدسة فوق كود أو نص، كرة بنفسجية لامعة، كوكب كوني — a lens over code/text, a glossy orb, a cosmic planet.
- **كيف / how:** three.js: refract(view, normal, 1/IOR); per-channel IOR for dispersion; Fresnel rim; backside FBO trick. CSS orb: radial-gradient circle + backdrop-filter blur + an inner highlight crescent (+ 3–4 faint concentric halo rings, inner orange hotspot as in style:product). HyperFrames cosmic-orb block: iridescent soap-bubble planet with nebula bands and edge chromatic aberration. **أرقام / params:** IOR 1/1.31 (ice) … 1.45–1.5 (glass); cosmic-orb hue 268, accent 196, spin .035, size .86, backdrop #04040a, 10 s.
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion` · `kosif-one/vendor/hyperframes/registry/blocks/cosmic-orb/cosmic-orb.html` · `style:pm-hbcoop-de365c` · `style:product`
- **فيديوهات مرجعية / reference videos:** `style:pm-twoclipping-221cab`
- **📦 تثبيت / install:** `npm i three@0.186.1   # or: npx hyperframes@0.8.164 add cosmic-orb`

#### GLOW-68 · حافة نيون من ألوان الواجهة وإضاءة نابضة · Accent rim rig from the UI palette (pulsing) · 📦 بأمر تثبيت / one install
- **ماذا / what:** شخصية أو جسم يُضاء كمنتج: مفتاح دافئ ناعم وتعبئة باردة وحافتان ملونتان من ألوان الواجهة، وأضواء تنبض فيتنفس الجسم. — A character or object lit like a product: soft warm key, cool fill and two coloured rims from the overlay palette, with pulsing accents so it breathes.
- **متى أستخدمها / when:** شخصيات تقنية، توائم رقمية، أبطال ثلاثية مع HUD — tech characters, digital twins, 3D heroes with HUDs.
- **كيف / how:** bunny_twin: DirectionalLight 0xfff3ea 2.3 (shadow 1024, radius 6, bias −.0004); Hemisphere 0xd8fff2/0x1a2624 .32; SpotLight 0x9dffb4 2.4 and 0xffb8d0 1.5 (dist 3, angle .7, penumbra .6); envFromGradient top 0x8fd6c4 sunPower 2.5, environmentIntensity .5. cinematic_3d: ambient #0f172a 1.5; dir #38bdf8 3.5 at (5,8,5); rim point #f43f5e 5.0 range 50 at (−6,−2,−4); gold point #fbbf24 4.0 range 40 at (4,−4,3); per frame gold = 3.5 + 1.2·sin(3t), rim = 4.0 + 1.5·cos(2.5t). **أرقام / params:** pulse 3 rad/s & 2.5 rad/s, amplitude 1.2 & 1.5.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js:30` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/cinematic_3d.html:112` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/cinematic_3d.html:206`
- **📦 تثبيت / install:** `npm i three@0.186.1 esbuild`

#### GLOW-69 · استوديو كريمي بثلاث إضاءات · Cream studio sweep with a soft 3-light rig · 🟢 جاهز / ready
- **ماذا / what:** خلفية سويب كريمية وظل تلامس وشبكة باهتة وإضاءة ناعمة ثلاثية لأفلام المختبر والمنتج. — A cream sweep background, contact shadow, faint grid and a soft three-light rig for product-lab films.
- **متى أستخدمها / when:** شرح منتج، تشريح، أفلام «مختبر» نظيفة — product explainers, exploded views, clean lab films.
- **كيف / how:** K3.studio(scene, {bg, grid}) from lab-kit; pair with labPost (rays off, tuned for software GL). **أرقام / params:** bg #f1efe8; key 2.6 at (3,6,4); fill 0xdfe8ff .9; rim 1.4; hemisphere .9; shadow opacity .22; grid #c9d8c2.
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/lab-kit.js:194` · `100-superskills/skills/kosif-montage-motion/SKILL.md:101`

#### GLOW-70 · ظل وانعكاس متسقان مع مفتاح واحد · One-key consistency: shadow, lit edge & reflection · 🟢 جاهز / ready
- **ماذا / what:** إزاحة الظل وحافة الإضاءة وشريط الانعكاس كلها تتفق مع مفتاح واحد أعلى اليسار، وتُعاد حسابها مع الدوران والارتفاع. — Shadow offset, lit-edge highlight and reflection band all agree with one top-left key and are recomputed with yaw and lift.
- **متى أستخدمها / when:** هواتف وبطاقات ومنتجات تدور أو تطفو — phones, cards and products that turn or float.
- **كيف / how:** box-shadow `${-yaw*1.6}px 48px 90px rgba(0,0,0,.55)`, inset 1px rgba(255,255,255,.09); reflection linear-gradient(115deg, transparent 40%, rgba(255,255,255,.14) 50%, transparent 60%); recompute per frame from yaw and lift. MG-034 shadow-first: 0–1 s a separate shadow layer slides in, 1–2 s the product lands into it, 2–5 s benefit; its size/blur follow the product's Y and its direction matches the photo's light. **أرقام / params:** shadow down 40–60 px, x ≈ −yaw×1.6; ambient blur 60–100 px @50%; contact 8–12 px @35%; reflection 10–16% white; 140 px rise → blur +30%, opacity −20%.
- **الدليل / proof:** `kosif-tool/playbooks/phone.md:23` · `kosif-tool/playbooks/phone.md:43` · `kosif-tool/playbooks/phone.md:128-138` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-product-ads.md`

#### GLOW-71 · قراءة إضاءة صورة مرجعية · Read the light of a reference image · 🟢 جاهز / ready
- **ماذا / what:** يخمّن أي جانب أسطع وكم وقفة بين المضاء والظل من متوسطات الإضاءة، كتقدير صريح. — Guesses which side is brighter and the lit-to-shadow ratio in stops from luminance halves — reported as a heuristic.
- **متى أستخدمها / when:** مطابقة إضاءة لقطة مع صورة مرجعية أو منتج مصوَّر — matching a 3D/2D light to a photo.
- **كيف / how:** image_analyze.py analyze(): mean luma of left/right/top/bottom halves; side_ratio_stops = log2(lit/shade); lighting_ratio = 2^stops : 1; then feed K3.lightRig / lightPreset and keep shadows pointing the same way (GLOW-70). **أرقام / params:** side threshold 8 luma levels.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/omni/image_analyze.py:120`

#### GLOW-72 · وصفات إضاءة مقفلة لمولدات الصور والفيديو · Locked lighting phrases for AI plates · 🔑 مفتاح أو خدمة / needs key or paid service
- **ماذا / what:** جمل إضاءة قصيرة تغيّر المزاج بثبات، ووصفات مقفلة لكل نوع إنتاج تُنسخ كما هي في كل مقطع. — Short lighting phrases that reliably change mood, and locked per-genre recipes copied verbatim into every clip.
- **متى أستخدمها / when:** لقطات مولدة بالذكاء الاصطناعي تحتاج اتساقًا بين المقاطع — AI-generated plates that must match across clips.
- **كيف / how:** One key-light phrase + direction + temperature (e.g. warm directional light from a high window camera-left, soft Rembrandt triangle); rim/volumetric for hero and abstract plates, flat/even for icons and diagrams. Locks: car = large softbox key front-left + thin right rim + soft floor reflection; food = golden overhead practical + left softbox + gentle counter shadows; fitness = single overhead teal-blue rim fading to black, close shot 4–6 s with a localised red/orange heat-map glow on the target muscle (labels in post); documentary L = amber top spotlight with smoke haze. The prompt builders are tested here; the picture itself needs a generation service — the profiles target Google Flow / Veo (food-flow.mjs:98), so that account (or another image/video API key) is required. **أرقام / params:** vocabulary: natural, studio, rim, soft directional, volumetric rays, flat/even, golden hour, high key, Rembrandt, chiaroscuro.
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/car-exploded.mjs:56` · `fastify-motion-bro/scripts/profiles/fitness.mjs:32` · `fastify-motion-bro/tests/production-profiles.test.mjs:29-32` · `kosif-atlas/skills/1446-marketing-skills/3504-image`

## ضوء الطبيعة والمصادر العملية والانعكاس — Natural light, practicals & reflections

_ضوء يأتي من داخل العالم: سماء وشمس، أوراق، ماء، فوانيس ومصابيح ومنارات — وانعكاسها على الأرض المبللة._

#### GLOW-73 · سماء فيزيائية وشمس وبيئة من تدرج · Physical sky, sun, fill & gradient environment · 🟢 جاهز / ready
- **ماذا / what:** قبة سماء بتشتت جوي وشمس بالارتفاع والسمت، وضوء شمس يلقي ظلًا مع تعبئة من جهة الكاميرا، وبيئة انعكاس من تدرج محدود. — An atmospheric-scattering sky with the sun placed by elevation/azimuth, a shadow-casting sun with a camera-side fill, and a bounded gradient environment for reflections.
- **متى أستخدمها / when:** أفلام من الشروق إلى الظهر، مناظر طبيعية، منتجات لامعة في الخارج — sunrise-to-noon films, landscapes, glossy outdoor products.
- **كيف / how:** sky = K3.makeSky(scene, {turbidity, rayleigh, mie, mieG}); sky.setSun(elevDeg, azimDeg); K3.makeSunLight(scene, {intensity, shadowSize, bounds, far}); K3.makeFill(scene, 0xcfe0ff) (intensity set per frame); K3.envFromGradient(renderer, scene, {top, horizon, ground, sun, sunColor, sunPower}) — PMREM from a bounded gradient avoids the Sky shader's sun-disk Inf/NaN black rectangles (envFromSky is the risky alternative). Procedural dome alternative: back-faced sphere shader with a 3-colour gradient, sun = pow(s,1800/size)·30 + pow(s,40)·.8 + pow(s,6)·.25, hashed twinkling stars. **أرقام / params:** turbidity 3, rayleigh 1.6, mie .004, mieG .85, scale 45000; sun 3.0, shadow map 4096, bounds 2300, bias −.0005, normalBias 2; env top #7da2cc horizon #f0cfa0 ground #3a3a2a sun #ffd29a power 6; domes: dawn #1C4C98/#F0A878, golden #2E4A7A/#FFB067, night #03061A/#1A1F54, blue hour #081433/#D9806A.
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:86` · `kosif-studio/motion/kit/three-kit.js:98` · `kosif-studio/motion/kit/three-kit.js:480` · `kosif-one/projects/egypt-2120-animation/index.html:80-98`

#### GLOW-74 · ضوء متسلل بين الأوراق · Dappled sunlight (komorebi gobo) · 🟢 جاهز / ready
- **ماذا / what:** كشاف بنسيج أوراق مولّد ينزلق قليلًا مع الزمن فتتحرك ظلال الأوراق على الأرض والماء. — A spotlight projecting a generated leafy cookie that slides slightly over time, so leaf shadows move on ground and water.
- **متى أستخدمها / when:** حدائق، برك، دعاء صباحي، هدوء — gardens, ponds, calm mornings.
- **كيف / how:** const d = K3.makeDappledSun(scene, {intensity, angle, color, density, floor, seed, shadowSize}); d.place(sunDir, target, dist); per frame d.setDapple(t); feed d.matrix() + texture to water (uDapple). SpotLight decay 0 makes it sun-like. **أرقام / params:** colour #ffd9a6 (koi #ffcf96); intensity 4 (3–5; koi 4.2); angle .24 rad (koi .19); penumbra .35; tex 512; floor .16; density .15; shadow 4096.
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:765` · `100-superskills/skills/kosif-montage-motion/scripts/projects/koi_pond/src/main.js:35` · `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:765`

#### GLOW-75 · كاوستكس تحت الماء · Underwater caustics & absorption · 🟢 جاهز / ready
- **ماذا / what:** شبكة ضوء متحركة على السطوح تحت الماء من الشمس المباشرة فقط، مع امتصاص لوني بالعمق. — A moving caustic light network on surfaces below the waterline from direct sun only, plus per-channel absorption with depth.
- **متى أستخدمها / when:** برك، بحار، أحواض سمك — ponds, seas, aquariums.
- **كيف / how:** K3.addCaustics(material, {level, strength, scale, absorb, sun, time}) patches any Standard/Physical material. **أرقام / params:** strength 1.6; scale 1.6 (≈5.5 for 5–15 cm garden-pond cells); absorb RGB [1.6, .55, .42]/m; fades in 0–.12 m, gone by 1.2–3 m.
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:561` · `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:561` · `kosif-studio/motion/references/hyperframes-authoring.md`

#### GLOW-76 · التعريض الطويل وخطوط الضوء · Long-exposure lighten stack & continuous light trails · 🟢 جاهز / ready
- **ماذا / what:** تراكم عينات داخل الإطار: وضع «الأسطع» لمسارات النجوم والسيارات والرسم بالضوء، والمتوسط لماء حريري. — Sub-frame accumulation: 'lighten' keeps each pixel's brightest sample for star trails, car trails and light painting; 'average' gives silky water.
- **متى أستخدمها / when:** ليل المدن، نجوم، شلالات، سيوف وكرات بذيول — city nights, stars, waterfalls, blades and balls with tails.
- **كيف / how:** render --blur 16 --shutter 30 --stack lighten|average (window.__stack='lighten' with __blur > 1; MaxEquation blending). A light that moves farther than its size between sub-samples leaves dots — stretch it: mesh.scale.z = 1 + K3.trailLength(speed)/(2·radius), gap = speed·(shutter/fps)/k. 2D trails: keep the last 8–10 positions and draw them additively with decreasing alpha (tail ≈150 ms; orbit arcs with a 40% tail and a hot head sprite). **أرقام / params:** 1 s exposure per frame at 30 fps; 16 sub-samples; shutter 30; 2D tail 8–10 positions.
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:1221` · `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:442` · `kosif-studio/tests/test_studio.py:793` · `100-superskills/skills/kosif-montage-motion/references/book-lessons.md`
- **فيديوهات مرجعية / reference videos:** `style:pm-chrisjdimarco-f068db` · `style:pm-kamstudiolabs-447565` · `style:pm-nolkeeg-bf062e`

#### GLOW-77 · هالات ومخاريط المصابيح ثنائية الأبعاد · 2D practical halos, lamp cones, lit windows & fireflies · ✅ مُثبت هنا / proven here
- **ماذا / what:** برك ضوء من تدرجات شعاعية للقمر واللافتات والمصابيح، ومخاريط شفافة تحت أعمدة الإنارة، ونوافذ تضاء ويراعات. — Soft light pools from radial gradients (moon, signs, lamps), translucent cones under street lamps, windows switching on and fireflies.
- **متى أستخدمها / when:** مدن ليلية مرسومة، غرف دافئة، شتاء، قرى — drawn night cities, cosy rooms, winter, villages.
- **كيف / how:** SVG radialGradient defs layered over the scene with transparent edges (tested in midnight_cat). Practical pool: warm amber core → transparent in screen blend over a darkened scene, brightness falling off with distance from the lantern. Windows: switch on in sequence with warm fill + additive radial bloom 30–60 px; winter lamps fade pink → warm cream with a radial halo (80 px, 1 s) and slight room darkening; fireflies = small yellow dots with blurred halos on noise paths pulsing 1–2 Hz. **أرقام / params:** moon #a9d7ce .33 → #509eac .12 → 0; cyanHalo #28eee5 .2; roseHalo #ff4566 .23 pulsing .76 + .07·sin 5t; lampHalo #ffe3a4 .45 → #ffd378 .10 at 17%; beam #ffe4a3 .06 → 0; pool core #fff1cf, mid #f2b25a 40%, radius 200–400 px.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/assets/scene.js:14` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cinematic-cat.html:16` · `style:pm-kamstudiolabs-0b0824` · `style:pm-abderrahmen-g-9e8ed0`
- **فيديوهات مرجعية / reference videos:** `style:pm-itsolelehmann-e47532` · `style:pm-x4b47x-9cc84f`

#### GLOW-78 · أضواء المدينة الليلية ثلاثية الأبعاد · 3D night practicals: sodium lamps, additive point sprites & bokeh · 📦 بأمر تثبيت / one install
- **ماذا / what:** صف مصابيح صوديوم يُقرأ ضوءًا حقيقيًا بثمن رخيص، ونقاط ضوء مضافة لأضواء المدن والطائرات المسيّرة، وكرات بوكيه في الخلفية. — A row of sodium lamps that reads as real light cheaply, additive point sprites for city lights and drones, and bokeh orbs far behind.
- **متى أستخدمها / when:** شوارع ليلية، مدن من الأعلى، خلفيات بوكيه — night streets, aerial cities, bokeh backdrops.
- **كيف / how:** Lamps: 24 lamps every 45 m — emissive sodium×9 sphere r .22 (blooms), additive soft pool plane 16×16 m in sodium×.55 on wet asphalt (roughness .32), only the nearest 6 as true PointLight(sodium, 70, 45, 2). Points: BufferGeometry with position/color/aSize/aAlpha, ShaderMaterial transparent, depthWrite false, AdditiveBlending; gl_PointSize = clamp(aSize·1100/−mv.z, 1.5, 90); fragment a = smoothstep(.5, 0, d)², rgb·a·alpha·2.2; 5000 typical, FBO ping-pong for 100k+. Bokeh: 3–5 emissive spheres far behind (blue + warm orange, radius 3–6% of frame) through DOF, or soft sprite discs. **أرقام / params:** sodium #ffa040; 6 real lights; point size 1.5–90 px; 5000 points.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/blue_hour/src/main.js:96` · `kosif-one/projects/egypt-2120-animation/index.html:142-158` · `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion` · `style:pm-anilraok-eff262`
- **📦 تثبيت / install:** `npm i three@0.186.1 esbuild`

#### GLOW-79 · ارتعاش الفانوس والشمعة · Lantern & candle flicker (organic) · 📦 بأمر تثبيت / one install
- **ماذا / what:** فانوس يرتعش بموجتين من الضوضاء ولا يهبط تحت 80%، فيقود الضوء النقطي واللهب والتوهج وبركة الماء معًا. — A lantern flickers with two octaves of noise and never drops below ~80%, driving point light, flame, glow sprite and water pool together.
- **متى أستخدمها / when:** قوارب ليلية، خيام، شموع، دعاء — night boats, tents, candles, duas.
- **كيف / how:** fl = .9 + .07·perlin(7t, 1.3) + .04·perlin(19t, 4.1); lamp.intensity = 9·fl (range 26, decay 1.6); flame colour LANTERN×13·fl; glow opacity .32·fl; pool .85·fl; lantern swings .06·sin(1.1t + 1.3). Candle/fire presets: 1800–2200 K (candle 1850, firelight 1900), 6:1 ratio. Neon is different: it strikes and drops out (GLOW-02), it does not wobble. **أرقام / params:** floor ≈80%; octaves 7 Hz & 19 Hz; intensity 9, range 26, decay 1.6.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:230` · `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:84` · `100-superskills/skills/kosif-montage-motion/references/lighting-presets.md`
- **📦 تثبيت / install:** `npm i three@0.186.1 esbuild`

#### GLOW-80 · شعاع منارة دوّار · Rotating lighthouse / beacon beam · 📦 بأمر تثبيت / one install
- **ماذا / what:** شعاع ضوء حجمي مزيف: مخروطان مفتوحان بمظلل مضاف تتلاشى شفافيته على الطول، يدور حول المصباح. — A fake volumetric beam: two open cones with an additive shader whose alpha fades along the length, rotating around the lamp.
- **متى أستخدمها / when:** منارات، حراس، بحر ليلي، قصص صامتة — lighthouses, keepers, night seas, silent shorts.
- **كيف / how:** 3D: ConeGeometry(55, 900, 32, 1, true) translated −450, rotated ±90° inside a pivot; fragment a = pow(1 − v, 1.6)·.55·(.6 + .4·sin(u·2π·3)); beamPivot.rotation.y = 1.25t + 1.2; bloom at the source (≈1.5). 2D: two opposite triangular wedges (10–14°) from the lamp, linear alpha .35 → 0, 'lighter' blend, one revolution ≈6 s; failure beat: 3 flicker pulses of 400 ms, then cut to dark. **أرقام / params:** beam #FFE7B8; 1.25 rad/s (3D) or 6 s/rev (2D); wedge 10–14°.
- **الدليل / proof:** `kosif-one/projects/egypt-2120-animation/index.html:412-418` · `kosif-tool/styles/pm-kamstudiolabs-0b0824/BRIEF.md` · `style:pm-kamstudiolabs-0b0824` · `style:pm-ryzoft-4f85bd`
- **فيديوهات مرجعية / reference videos:** `style:pm-faroukzy-9ff23e`
- **📦 تثبيت / install:** `npm i three@0.186.1   # 3D cone; the 2D wedge needs nothing`

#### GLOW-81 · قمر مرسوم بهالة · Painted moon with halo · 🟢 جاهز / ready
- **ماذا / what:** قمر كامل: هالة بنفسجية واسعة، قرص كريمي مضاء من أعلى اليسار، فوهات ناعمة، وهالة داخلية دافئة. — A full moon: wide purple halo, cream-to-tan disc lit from upper left, soft crater blotches and a warm inner halo.
- **متى أستخدمها / when:** ليالي القصص والأدعية والمشاهد المرسومة — story nights, duas, painted scenes.
- **كيف / how:** glow(ellipse r·2.4, '#4f3f86', 70, .55); fill(ellipse, rad(offset, r·1.55, ['#fffaf0', '#f7e6c2', '#dcb47e'])); crater ellipses #b99467 α .2–.3 blur 4–9; glow #f1d29a 26 .32. Uses only glow/fill (verified here). **أرقام / params:** radius 150 at (845, 232).
- **الدليل / proof:** `kosif-studio/scenes/dragon_girl.py:150` · `kosif-studio/render.py:407`

#### GLOW-82 · انعكاس الضوء على الأرض المبللة والماء · Wet-floor & water reflections of light and titles · ✅ مُثبت هنا / proven here
- **ماذا / what:** الأرض المبللة تعكس اللافتة بشرائح مقلوبة متموجة وخفوت فرينل، والعناوين تطفو فوق انعكاس مكسور، وعمود ضوء ذهبي على النهر. — Wet ground mirrors the sign as rippled flipped strips with Fresnel fade; titles float over a broken reflection; a golden column of light lies on the river.
- **متى أستخدمها / when:** ليل ممطر، أنهار، أرضيات لامعة، عنوان فوق ماء — rainy nights, rivers, glossy floors, titles over water.
- **كيف / how:** Neon proof: mirror around the wall/floor junction in 3 px strips with ripple, a sharp layer inside puddle masks (2 px blur + short streaks) and a 16 px half-res film on the rest of the asphalt, × Fresnel fade .9 (far) → .25 (near), rain-drop ripples in puddles, junction AO — rendered here. Titles: MG-057 vertically flipped copy + gradient mask + perspective skew (CSS scaleY(−1) + mask-image); MG-079 reflection distorted by a displacement map from the water texture (SVG feDisplacementMap + animated feTurbulence). Sunset sea: animated normal-map ripples (scale .02), spec power 200 toward the sun, fog .0015. Lit pavilion: thin warm-gold edge strokes #f6e2b0 (1–2 px), bloom 12–20 px ramping on over 2 s, long reflection column on the water. A dark far bank sells water. **أرقام / params:** strips 3 px; puddle blur 2 px, film 16 px @½; Fresnel .9→.25; MG-057 5 s, MG-079 7 s.
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/proofs/neon-glow/index.html` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-tracking-compositing.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-cinematic-titles.md` · `style:pm-demitiyageekzen-7770ad`
- **فيديوهات مرجعية / reference videos:** `style:pm-nft-chen-5f8bb0`

#### GLOW-83 · حقل حراري وتلوين دوبلر · Thermal heat-ramp field & Doppler-beamed glow · 🟢 جاهز / ready
- **ماذا / what:** مظلل واحد: كتلة FBM مشوهة مرتين تُلوَّن بمنحدر حرارة من سبع درجات وتُلطَّخ بأثر إصبع؛ وقرص يضيء ويزرق من جهة الاقتراب. — One shader: a double domain-warped FBM blob mapped through a 7-stop heat ramp and smeared by a finger trail; and a disk brightened and blue-shifted on its approaching side.
- **متى أستخدمها / when:** خرائط حرارة، تحميل زائد، ثقوب سوداء وعلوم — heat maps, overload beats, black holes and science.
- **كيف / how:** Heat stops at 0/.12/.30/.45/.60/.78/1 via smoothstep, heat capped .75; 24 trail points (life 1.6 s, smudge 9, radius .17, follow .3), melt cycle 6 s, blob .37, press ripple .18 / bloom .55 / .9 s. For video, script the 'finger' as keyframed points. Doppler (seen): intensity ∝ δ^3–4 — brighten/blue-shift the approaching side, dim/red-shift the receding one, then heavy bloom (20–40 px, threshold .7). Ember/fire means heat or overload, never human tragedy. **أرقام / params:** 7 stops; 24 pts / 1.6 s / smudge 9; Doppler δ^3–4, bloom 20–40 px.
- **الدليل / proof:** `kosif-atlas/skills/100-ui-motion/211-thermal-finger-trail/SKILL.md` · `kosif-atlas/skills/100-ui-motion/211-thermal-finger-trail/references/thermal-finger-trail.html` · `style:pm-rebutonepress-810f78`

#### GLOW-84 · عناوين الضباب وشق الضوء وكشف الفخامة الهادئة · Fog-layer & light-slit titles (quiet premium) · 📄 موصوف / documented only
- **ماذا / what:** عنوان ثابت بين طبقتي ضباب تتحركان بسرعتين، أو خط ضوء رفيع يتسع ليكشف عنوان فصل ثم يخفت. — A title holds between two fog layers moving at different speeds, or a thin line of light widens to reveal a chapter title, then dims.
- **متى أستخدمها / when:** فصول الأفلام الوثائقية، افتتاحيات هادئة فاخرة — documentary chapters, calm premium openers.
- **كيف / how:** MG-071: 0–2 s atmosphere, 2–4 s appear, 4–8 s read; screen/alpha layering with graded fog depth; haze must never block reading (local: procedural canvas-noise fog with mix-blend-mode screen). MG-072: 0–1 s line, 1–3 s widen, 3–6 s hold; horizontal moving mask + limited glow; avoid fast flashes and white that eats the letters. S02 Quiet premium: measured contrast, restrained shadows, a little sheen, slow 1.00→1.04 drifts, few transitions — gloss cannot rescue a weak source. **أرقام / params:** MG-071 8 s; MG-072 6 s; drift 1.00→1.04.
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-cinematic-titles.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/styles.md`

## توليفات قوية / power combos

- **لافتة ليلية عربية / Arabic night sign:** GLOW-01 + GLOW-02 + GLOW-82 + ARAB (الكلمة كاملة مشكّلة) + BEAT (طنين 120 هرتز وطقطقة على كل اشتعال) + QA (verify_video) — كما في `proofs/neon-glow`؛ استبدل «قهوة» باسم المتجر واحتفظ بجدول الاشتعال.
- **فيلم دعاء أو قصيدة / dua or poem film:** GLOW-24 + GLOW-47 + GLOW-41 + GLOW-74 + ARAB (كلمات من الصوت) + SYNC (words.json) + VOICE (بلا موسيقى) — الهالة تتنفس مع الصوت، والأشعة تبطئ، ومسحة الضوء تقع على جملة الختام فقط.
- **إطلاق منتج تقني / tech product launch:** GLOW-42 + GLOW-43 + GLOW-16 + GLOW-70 + UI (نافذة مائلة) + CAM (دفع 3–5%) — مثل style:product: حافة نيون لخانة الأوامر، شفق في الثلث السفلي، كرة زجاجية، ولمعة واحدة لا تتكرر.
- **مشهد ثلاثي سينمائي / cinematic 3D shot:** GLOW-26 + GLOW-57 + GLOW-61 + GLOW-73 + GLOW-48 + GLOW-50 + 3D + COLOR (درجة لونية) — إضاءة بالوقفات وحرارة لون حقيقية، ثم بلوم بعتبة .9 وأشعة لا تظهر إلا والشمس في الكادر.
- **مدينة ليلية مرسومة / painted night city:** GLOW-77 + GLOW-03 + GLOW-63 + GLOW-79 + TEX (حبيبات ومطر) + DRAW — هالات SVG ملونة، لافتات نيون بأربع ضربات، حواف مبللة بلونين، وفانوس لا يهبط تحت 80%.
- **ريل بإيقاع / beat-cut reel:** GLOW-54 + GLOW-34 + GLOW-27 + GLOW-23 + BEAT (كشف الضربات) + TRANS — ومضة وانقسام RGB على الضربات القوية فقط (≤3 ومضات/ث)، وحلقات تضيء مع كل ضربة ثم تسكن.
- **رحلة على خريطة / map journey:** GLOW-09 + GLOW-22 + MAP + DATA (عدّاد المسافة) + ARAB (أسماء مُسقطة) — خط كهربائي برأس أبيض 3% وموجة صدمة حيث تهم المسافة من نقطة البداية.
- **ترجمة متوهجة بلا متصفح / browserless glowing captions:** GLOW-06 + SYNC (كاريوكي ASS) + FOOT (مونتاج) + QA — طبقتا Glow/Main بـ shaping=complex وخط ثابت داخل fontsdir، فوق لقطات حقيقية.
- **غلاف أو مشهد مرسوم بالكود / painted cover:** GLOW-14 + GLOW-51 + GLOW-81 + GLOW-63 + GLOW-30 + GEN (لوحة بلا نص) — مكدس توهج متدرج، فلير أنامورفي بأشباح، ثم بلوم بعد تثبيت OpenCV.
- **صورة مولدة بإضاءة متسقة / consistent AI plates:** GLOW-72 + GLOW-59 + GLOW-60 + GEN — جملة إضاءة مقفلة واحدة لكل المقاطع، وأرقامها محسوبة قبل أن تُكتب.

## أخطاء ممنوعة / never do

1. **لا توهج على نص الترجمة أو المتن ولا انحراف لوني عليه** — علامة توليد يرصدها qa.py (ظل ≥20 بكسل أو ملوّن)، وكتيبات المالك تمنعه؛ التوهج لكلمة بطلة أو لافتة فقط (GLOW-40).
2. **لا بلوم على كل شيء ولا «غبار متوهج» خلف كل مشهد** — أكثر مظهر مولَّد شيوعًا (`kosif-tool/playbooks/particles.md:97`)، وفي الواجهات «حزمة الزجاج والتوهج» بلا محتوى (`kosif-tool/playbooks/product-ui.md:248`).
3. **لا عتبة بلوم منخفضة على مشهد واقعي** — جرّبتُ هنا bloom .9 بعتبة .6 فغسل الإطار كله بالبرتقالي؛ الافتراضي .22 بعتبة .9، والألوان من الانبعاث فوق ألبيدو داكن (GLOW-26/GLOW-27).
4. **لا strokeText لقلب أنبوب نيون عربي بخط متغيّر** — حدود الخط المتداخلة ترسم ندوبًا داخل الحروف المتصلة؛ احسب القلب من حقل مسافة لقناع الكلمة كاملة (GLOW-01).
5. **لا ترجمة ASS عربية بلا shaping=complex** — جرّبتُ هنا: الوضع الافتراضي أظهر «ا» في «القلب» مربعًا فارغًا مع Cairo وTajawal (GLOW-06).
6. **لا اختصار background بعد background-clip:text** — يعيد القص إلى الحدود فيُرسم مستطيل تدرج مصمت مكان الحروف؛ استخدم background-image (GLOW-41).
7. **لا تدرج خطي يملأ الشاشة على خلفية داكنة** — تشرّط H.264 (banding)؛ استخدم توهجًا شعاعيًا محليًا + حبيبات (`kosif-atlas/skills/2702-hyperframes/10378-hyperframes/house-style.md`).
8. **لا لمعة أو نبضة تتكرر للأبد** — مسح البطاقة مرة، وانعكاس الزجاج مرة لكل دوران، والنبضة مرتين ثم تسكن (GLOW-42, GLOW-22).
9. **لا ومضات أسرع من 3 في الثانية ولا أبيض يأكل الحروف** — خطر صحي وقراءة ضائعة؛ قمة الومضة .55–.85 ثم انحدار power4.out (`100-superskills/skills/trend-animation-styles/references/styles.md`).
10. **لا فلير مبالغ فيه ولا شمس داخل العدسة طوال الفيلم** — الشمس أمام العدسة عند الشروق فقط ثم مفتاح جانبي، والفلير يظهر فقط والشمس في الكادر (GLOW-50; `kosif-studio/motion/references/hyperframes-authoring.md`; المبالغة مقبولة فقط حين تكون نكتة مقصودة كما في style:pm-henkpoley-3d3407).
11. **لا ظل يخالف اتجاه الضوء ولا إضاءة رمادية افتراضية** — مفتاح واحد للفيلم، والظل والانعكاس يتبعانه (GLOW-70, GLOW-57).
12. **لا تخلط حرارات لون بلا قصد ولا توهج «جمر» على مأساة إنسانية** — لكل مصدر كلفنه، والجمر يعني حرارة أو حملًا زائدًا فقط (GLOW-61, GLOW-22).

## أقوى 5 حركات توقيع / 5 signature moves

1. **GLOW-01 — لافتة النيون العربية الحية:** مكدس 3/10/26/64/140 بكسل بـ lighter، جدول اشتعال يقرأه الصوت، جدار يأخذ لون اللافتة، وانعكاس على أرض مبللة — مُثبت هنا بـ 13/13.
2. **GLOW-41 — مسحة الضوء على جملة الذروة:** تدرج 300% مقصوص على الكلمة في 0.75 ث، من اليمين لليسار في العربية، والباقي يخفت إلى .3.
3. **GLOW-16 — بركة الضوء خلف البطل:** تتفتح إلى ≤ .45 ثم تتنفس ±6% — أول ما تضعه خلف أي عنوان أو شعار على خلفية داكنة.
4. **GLOW-26 — makePost ببلوم بلون المصدر:** bundle واحد بلا npm، بلوم .22 بعتبة .9، أشعة وفلير مع الشمس، وحارس NaN — كل مشهد ثلاثي يبدو مصوَّرًا.
5. **GLOW-47 — أشعة إلهية فوق اللقطة:** repeating-conic مقنّع يتلاشى للأسفل + بلوم دافئ بـ screen + ومضة على الذروة — توقيع الدعاء والكشف والأبواب التي تنفتح.

## إضافات من Cinematic Director PRO v5

_مستخلصة من حزمة المالك KOSIF Claude Cinematic Director PRO v5 (انظر [cinematic-director-pro.md](../cinematic-director-pro.md)). مسارات الدليل `owner-upload:` تشير إلى ملفات داخل أرشيف المالك، لا إلى هذا المستودع._

#### GLOW-P01 · كتابة مسار نيون نقطية بطبقتي توهج في Pillow · Raster neon path-write in Pillow (blurred halo + hot core) · 📄 موصوف / documented only
- **ماذا / what:** خط نيون يُرسم تدريجيًا بلا متصفح: هالة مموهة مدموجة ثم قلب ساطع ونقطة رأس بيضاء. / A neon line writes on without a browser: a blurred halo blended in, then a bright core and a white tip dot.
- **كيف / how:** Path = 321 points of a decaying sine (amplitude 95 px, 3 half-waves, e^(−i/600)). Visible count = len·min(1, t/2.6). Halo: draw the partial path 17 px wide in (0,150,195) on a black layer, GaussianBlur(21), Image.blend(base, halo, 0.44). Core: 6 px (31,200,245) then 2 px (204,254,255), joint="curve"; tip = 10 px white ellipse. Dark ground (8,11,23) with faint 48 px scan lines; Arabic caption with direction="rtl". frame(t) is pure — re-rendering t=2.5 gives identical bytes. Re-ran here: 4 s 480×854 24 fps MP4 + still PNG; frame looked clean. Raster cousin of GLOW-03 (SVG 4-stroke tube) for Pillow/ffmpeg-only pipelines. Status note: the code is owner material that is not vendored in this skill; the numbers above are from one run on the owner's copy on 2026-10-16 and cannot be re-run from here, so this is 📄 documented, not ✅. **أرقام / params:** halo 17 px · blur 21 · blend 0.44 · core 6 px + 2 px · write-on 2.6 s
- **الرخصة / license:** owner package (own work)
- **الدليل / proof:** `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/tools/render_neon.py` · `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/examples/Neon_Path_Draw.mp4` · `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/examples/Neon_Path_Draw.png`

## إضافات v2 — v2 additions

_قدرات أُضيفت في الإصدار الثاني من حزم المالك (higgsfield-motion-saas وhiggsfield-motion-claude ومهارة المونتاج التحريرية وفيلم الأغنية وKOSIF SEE) ومن مهارات ECC (رخصة MIT)، مكتوبة بكلماتنا. ✅ هنا = شُغّلت في جلسة 2026-10-16 وسجلها في [external-skills.md](../external-skills.md)؛ مسارات `owner-upload:` تشير إلى أرشيفات المالك لا إلى هذا المستودع. — v2 additions from the owner's packages and ECC skills (MIT), in our own words; ✅ = run in this session, log in external-skills.md; `owner-upload:` paths point into the owner's archives, not this repo._

#### GLOW-X01 · مرور العدسة «مصوَّر لا مرسوم» · Photographed lens pass (barrel, fringes, bloom, vignette, grain) · 📄 موصوف / documented only
- **ماذا / what:** مرور أخير على الإطارات يضيف ما تفعله عدسة حقيقية: انتفاخ برميلي، حواف لونية شعاعية، توهج للمناطق المضيئة على ثلاث درجات، تعتيم أطراف، وحبيبات خفيفة. — A final pass over rendered frames adding what a real lens does: barrel bulge, radial colour fringes, three-scale bloom on highlights, vignette and fine grain.
- **متى أستخدمها / when:** فيلم متجهي نظيف يبدو رخيصًا أو مسطحًا — a clean vector film that looks cheap or flat.
- **كيف / how:** Owner script lens.py (numpy + Pillow; not vendored): `python3 lens.py frames_dir out_dir --fps 30 [--k .04 --ca 1.5 --bloom .35 --thr .72 --vig .35 --grain .02] [--sched sched.json]`. Bloom from highlights above thr at three radii (h·0.006 / 0.02 / 0.06, weights 0.7 / 1 / 0.45, screen blend, auto-off on bright frames); barrel k with R/B sampled slightly apart (radial fringes); vignette smoothstep(0.35 → 1.25 r); luma grain seeded per frame, strongest in mid-tones. Per-scene overrides via --sched. Ran here (V7) on 960×540 test frames: corner −27 % (65.3 → 47.8), a halo +6.1 next to a white disc, grain std 0 → 4.1 and re-seeded every frame, ±1 px R/B fringe near the edge; 1.2 s for 3 frames. WebGL equivalents that worked: CA 0.0032·r (0.012 was far too much), CRT barrel 0.2, paper 0.035–0.05, scanlines 0.32, vignette 0.3–0.7. Status note: the code is owner material that is not vendored in this skill; the numbers above are from one run on the owner's copy on 2026-10-16 and cannot be re-run from here, so this is 📄 documented, not ✅. **أرقام / params:** k .04; CA 1.5 px; bloom .35 @ thr .72; vignette .35; grain .02.
- **الرخصة / license:** owner (no LICENSE file)
- **المصدر / source:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/scripts/code/lens.py`
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/references/external-skills.md` · `owner-upload:motion-saas_skill/higgsfield-motion-saas/scripts/code/lens.py`

#### GLOW-X02 · نواة توهج ملوّنة وحدود الوميض · Tinted bloom cores and flash limits · 📄 موصوف / documented only
- **ماذا / what:** التوهج الأبيض النقي يبدو رخيصًا؛ لوّن نواته، وأطلق الوميض من نقطة الفعل، ولا تتجاوز حدود الأمان. — Pure white bloom reads cheap: tint its core, bloom flashes from the action point, and stay inside safety limits.
- **متى أستخدمها / when:** ضربات وكشف شعار وتوهجات نيون — hits, logo reveals and neon glows.
- **كيف / how:** Tint the bloom core toward the light's colour; a flash blooms from the action point; at most one big flash per second; accessibility: ≤ 3 flashes per second and a full white frame ≤ 2 frames. **أرقام / params:** ≤ 1 big flash/s; ≤ 3 flashes/s; white ≤ 2 frames.
- **الرخصة / license:** owner (no LICENSE file)
- **المصدر / source:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/client-taste.md`
- **الدليل / proof:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/client-taste.md` · `owner-upload:motion-skill-claude/higgsfield-motion-claude/references/production-lessons.md`
