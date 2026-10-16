# الألوان واللوحات والتلوين — Colour, palettes & grading

> **قوتك هنا:** أنت تقرر اللون كمخرج لا كمزيّن — تقيس اللقطة ثم تصححها، تطابقها مع مرجع بأرقام محدودة، تلبسها لوكًا بسطر FFmpeg أو بفلتر متصفح أو بـLUT مخبوز، وتبني هوية كاملة من لون واحد مع تباين مضمون، ثم تحرّك اللون نفسه كأداة سرد: قلب قطبية، فصول بحقول لونية، سماء تتحول من الليل إلى الفجر.
> **أقوى دليل:** الأحد عشر تلوينًا في `kosif-studio/motion/montage.py:42` نُفذت كلها في هذه الحاوية يوم 2026-10-16 (rc=0، واختبار `kosif-studio/tests/test_studio.py:818` يثبت blue_hour وsodium_night)، وخبزتُ teal_orange في Hald/‏.cube وأعدت تطبيقه بدقة 51.9/47.9 dB PSNR، ونقل رينهارد إلى LUT واختبارات المطابقة (`test_mimic.py` 10/10، `test_analyze.py` 5/5) واختبارات الهوية (`identity_unity`، `palette`، `dashboard-theme` 5/5 لكل منها) مرّت هنا.
> **You can:** measure, correct, match, grade, palette-build, contrast-check and animate colour across FFmpeg, HTML/Canvas, three.js, Pillow and HyperFrames. **86 powers follow** — ✅ 38 · 🟢 15 · 📦 8 · 🔑 0 · 👁 13 · 📄 11 · 💡 1.

**الحالة / status:** ✅ مُثبت هنا (كود + اختبار أو رندر في هذه الحاوية) · 🟢 جاهز (كود المالك يعمل بلا إضافات) · 📦 بأمر تثبيت · 🔑 مفتاح أو خدمة · 👁 شوهد في فيديو أنتجتَه (وصفة البناء مرفقة) · 📄 موصوف فقط · 💡 فكرة.
مسارات الدليل نسبية إلى `/home/user/`؛ `style:<id>` = فيديو مرجعي أنتجتَه سابقًا (ملاحظاته في `kosif-tool/styles/<id>/`). `app/` = محرر «بصمة» (Basma).

**فحص سريع لهذه الحاوية (2026-10-16):** ffmpeg 6.1.1 فيه lut3d وhaldclut وcolortemperature وhuesaturation وselectivecolor وcolorbalance وcurves وvibrance وgrayworld وsignalstats وcas وvignette ✔ · Chromium (Playwright) رسم لوكات Canvas/CSS ✔ · NumPy + Pillow ✔ · OpenCV غير مثبت (vectorize وqa.study وملف اختبارات kosif-studio يحتاجونه) · HyperFrames CLI غير مثبت (`npm i -D hyperframes@0.8.164`) · DaVinci Resolve غير موجود — أرقام سكربتات Resolve تُطبق هنا بـFFmpeg.

## الفهرس / contents
- **اللوكات الجاهزة للفوتيج — Ready footage looks** — COLOR-01 … COLOR-12 (12)
- **التصحيح المقاس والتحليل والمطابقة — Measured correction, analysis & matching** — COLOR-13 … COLOR-30 (18)
- **اللوحات والهويات وأنظمة الرموز — Palettes, identities & token systems** — COLOR-31 … COLOR-49 (19)
- **نظرية اللون والإتاحة وقواعد الإخراج — Colour theory, access & direction rules** — COLOR-50 … COLOR-56 (7)
- **اللون في الضوء والفضاء واللمسة الأخيرة — Colour in light, atmosphere & finish** — COLOR-57 … COLOR-65 (9)
- **اللون عبر الزمن — Colour over time** — COLOR-66 … COLOR-77 (12)
- **الخلفيات والتدرجات والمعالجات — Grounds, gradients & treatments** — COLOR-78 … COLOR-86 (9)
- توليفات قوية / power combos · أخطاء ممنوعة / never do · أقوى 5 حركات توقيع / 5 signature moves

## اللوكات الجاهزة للفوتيج — Ready footage looks

_لوكات تعمل الآن على أي فيديو: FFmpeg في سطر، أو فلاتر المتصفح، أو LUT مخبوز، أو محرك HyperFrames عند تثبيته._

#### COLOR-01 · أحد عشر لوكًا جاهزًا بـFFmpeg · Eleven FFmpeg grade presets · ✅ مُثبت هنا / proven here
- **ماذا / what:** جدول GRADES في montage.py: أحد عشر تلوينًا مسمّى (curves/colorbalance/eq) تطبّقه على مقطع أو على كل لقطة في المونتاج، والحبيبات مبذورة فتتكرر النتيجة نفسها. — The montage.py GRADES table: eleven named curves/colorbalance/eq grades for one clip or per cut, with seeded grain so re-renders are identical.
- **متى أستخدمها / when:** أي فوتيج حقيقي يحتاج مزاجًا بسرعة — ريلز، مونتاج، فيلم كلمات فوق لقطات. — any real footage that needs a mood fast — reels, montages, lyric films over clips.
- **كيف / how:** CLI: `python montage.py grade CLIP.mp4 --preset teal_orange [--out X.mp4]` (also `kmotion grade`, `montage cut --grade`, timeline JSON `clips[].grade`, `smart_montage.py grade`). Output libx264 -preset medium -crf 17, format=yuv420p, audio stream copied untouched. The same chain can be pasted into any `-vf`. Verified in this container on 2026-10-16: all 11 chains ran on testsrc2 with rc=0 (blue_hour pulls YAVG 121.6→108.2 and V 127→133.7; teal_orange pushes U to 135.6), and kosif-studio's test asserts blue_hour + sodium_night run through ffmpeg. The kosif-studio, 100-superskills and kosif-one/tools tables match value for value (only line endings differ); kosif-omni's smart_montage carries the first six at CRF 18 with unseeded vintage grain alls=12 — prefer the seeded table. **أرقام / params:** 11 presets; CRF 17 (smart_montage CRF 18); grain all_seed=7; audio -c:a copy.

| preset | المزاج / mood | سلسلة FFmpeg المختصرة / chain (exact values) | متى / when |
|---|---|---|---|
| `teal_orange` | بلوكبستر: بشرة دافئة وظلال فيروزية | curves r `0/0 .2/.1 .7/.8 1/1`, b `0/.05 .3/.38 .7/.65 1/.95` + colorbalance rs .08 gs −.02 bs −.08 rh −.04 gh .02 bh .08 | إعلان، سفر، بشر |
| `golden_hour` | غروب دافئ مشبع | curves r .5→.58, b .5→.42 1→.92 + eq saturation 1.25 contrast 1.08 brightness .02 | ذكريات، طعام، طبيعة |
| `cyberpunk` | نيون سماوي/أرجواني | curves r 0→.05 .5→.45, b 0→.08 .5→.62 + colorbalance rs −.1 gs −.05 bs .15 rh .12 gh −.05 bh .08 + eq sat 1.35 contrast 1.2 | ليل المدن، تقنية، ألعاب |
| `vintage_film` | فيلم باهت بحبيبات | curves all `0/.06 .5/.5 1/.94` (+ r .5→.52, b 0→.04 .5→.48 1→.96) + noise alls=10 allf=t+u all_seed=7 + eq contrast 1.05 sat .9 | حنين، أرشيف |
| `matrix_tech` | أخضر تقني | curves g 0→.04 .5→.54, b .5→.46 1→.92 + colorbalance rs −.08 gs .1 bs −.05 + eq contrast 1.15 sat .85 | أمن، برمجة، غموض |
| `clean_commercial` | إعلاني نظيف حاد | eq contrast 1.12 sat 1.18 brightness .01 + unsharp 5:5:0.8 | منتجات، متاجر |
| `blue_hour` | توازن تنجستن: سماء زرقاء عميقة ومصابيح دافئة | colortemperature 4300 mix .85 + curves b 0→.06 .5→.56, r .5→.47 + eq sat 1.08 contrast 1.06 | ليل هادئ، أدعية ليلية |
| `sodium_night` | مصابيح شارع برتقالية وظلال زرقاء | curves r .4→.46, g .5→.47 1→.96, b 0→.05 .3→.3 1→.86 + colorbalance bs .10 gs .02 rh .06 bh −.08 + eq contrast 1.12 | شوارع ليلية |
| `restore` | ترميم الفوتيج القديم | انظر COLOR-02 | لقطات هاتف قديمة |
| `magma_night` | ليل أحمر حار | curves r 0→.02 .5→.56, g .5→.44 1→.95, b 0→.05 .5→.42 1→.88 + eq contrast 1.1 sat 1.1 | عوالم صوتية، نار |
| `none` | بلا تلوين | `null` | مقارنة قبل/بعد |

```bash
# one clip, audio untouched
python3 kosif-studio/motion/montage.py grade in.mp4 --preset blue_hour --out out.mp4
# or paste the chain yourself (exact owner values)
ffmpeg -i in.mp4 -vf "colortemperature=temperature=4300:mix=0.85,curves=b='0/0.06 0.5/0.56 1/1':r='0/0 0.5/0.47 1/1',eq=saturation=1.08:contrast=1.06,format=yuv420p" \
  -c:v libx264 -crf 17 -c:a copy out.mp4
```

- **الدليل / proof:** `kosif-studio/motion/montage.py:42` · `kosif-studio/tests/test_studio.py:818` · `100-superskills/skills/kosif-montage-motion/scripts/montage.py:42` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/scripts/smart_montage.py:29`

#### COLOR-02 · ترميم الفوتيج القديم · Restore grade for old or soft footage · ✅ مُثبت هنا / proven here
- **ماذا / what:** تلوين إنقاذ: إزالة ضوضاء زمنية خفيفة، سواد أنظف، انضغاط للإضاءات، دفء خفيف في المنتصف، وشحذ متكيف — ونسخة FINAL_EDIT المضبوطة يدويًا التي شُحنت. — A rescue grade: light temporal denoise, cleaner blacks, highlight roll-off, warmer mids and contrast-adaptive sharpening — plus the hand-tuned FINAL_EDIT variant that shipped.
- **متى أستخدمها / when:** لقطات هاتف قديمة أو مضغوطة أو باهتة قبل أي لوك إبداعي. — old, soft or over-compressed phone clips, before any creative look.
- **كيف / how:** `montage.py grade CLIP --preset restore`. Chain: hqdn3d=1.2:1.2:3:3 → eq contrast 1.12 brightness −0.015 saturation 1.07 gamma 0.97 → curves all `0/0 .06/.035 .25/.22 .5/.5 .8/.82 .94/.93 1/.97` → colorbalance rs .012 bs −.01 rm .025 gm .005 bm −.02 → cas 0.3. FINAL_EDIT (talking head, Lanczos 720×1280→1080×1920): eq contrast 1.12 brightness −0.02 saturation 1.10 gamma 0.96, same curves, colorbalance rs .015 bs −.01 rm .01, cas 0.32. Ran here on testsrc2 (rc=0). Upscale before CAS, never after. **أرقام / params:** hqdn3d 1.2:1.2:3:3; gamma .97/.96; cas .3/.32; whites capped at .97.
- **الدليل / proof:** `kosif-studio/motion/montage.py:42` · `100-superskills/skills/kosif-montage-motion/scripts/montage.py:53` · `kosif-studio/out/FINAL_EDIT/project/grade.txt` · `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:12`

#### COLOR-03 · تلوينات مشاريع بسطر واحد · One-line project grades (muted Ghorba, navy door + RTL mirror) · ✅ مُثبت هنا / proven here
- **ماذا / what:** تلوينات صغيرة شُحنت في مشاريع حقيقية: «الغربة» الهادئ المعتم قليلًا بنسختين، وتلوين colorbalance يسحب لقطة رمادية نحو الكحلي مع عكس أفقي ليفرغ اليمين للنص العربي. — Small grades shipped in real projects: the quiet, slightly darker Ghorba look in two calibrations, and a colorbalance pull from charcoal toward brand navy with an hflip so empty space sits on the right for Arabic text.
- **متى أستخدمها / when:** مشاهد حزينة أو تأملية؛ أو لقطة مولّدة تحتاج لون الهوية وجهة القراءة العربية. — melancholic or reflective shots; a generated clip that needs the brand hue and Arabic reading side.
- **كيف / how:** Ghorba v1 `eq=contrast=1.08:saturation=0.86:brightness=-0.023`, v2 `eq=contrast=1.06:saturation=0.95:brightness=-0.009` inside the per-shot -vf. Navy door: `-vf "hflip,colorbalance=rs=-.10:gs=-.03:bs=.25:rm=-.05:bm=.10"` then H.264 width 1280 crf 27 -an +faststart. All three ran here on testsrc2 (rc=0). **أرقام / params:** sat .86/.95; brightness −.023/−.009; bs +.25 navy pull.
- **الدليل / proof:** `kosif-one/projects/KOSIF_Motion_Ghorba/KOSIF_Ghorba_Render.py:146` · `kosif-one/projects/KOSIF_Motion_Ghorba/tools/render_ghorba_preview.py:139` · `kosif-earth-ci-fork/docs/design/HIGGSFIELD_VISUALS_ar.md`

#### COLOR-04 · خَبز أي تلوين في LUT · Bake any grade into a Hald CLUT / .cube and apply LUTs · ✅ مُثبت هنا / proven here
- **ماذا / what:** تحوّل أي سلسلة FFmpeg إلى صورة Hald أو ملف .cube بحجم 33 نقطة، ثم تطبقها بـlut3d أو haldclut بنتيجة شبه مطابقة — وتطبق LUT التحويل أو LUT الإبداعي من الكاميرا بالطريقة نفسها. — Turn any FFmpeg chain into a Hald image or a 33-point .cube and re-apply it with lut3d/haldclut almost identically; camera conversion and creative LUTs go in the same way.
- **متى أستخدمها / when:** لوك تريد إعادة استخدامه في Resolve أو Premiere أو مشاريع أخرى، أو تسليم LUT للعميل. — a look to reuse in other tools or projects, or to hand a client a LUT.
- **كيف / how:** haldclutsrc=8 (64³ entries) → run the grade chain on that one frame → apply with `[v][hald]haldclut=interp=tetrahedral`, or resample the Hald to a 33³ .cube (NumPy, R fastest) and use `lut3d=file=look.cube:interp=tetrahedral`. Verified here with teal_orange on 640×360 testsrc2: Hald vs direct grade PSNR 51.9 dB, 33³ cube vs direct 47.9 dB. Spatial or temporal parts (noise, unsharp, cas, vignette) do not bake — re-add them after the LUT. Use 33- or 65-point cubes and tetrahedral interpolation on 10-bit sources to avoid banding; never apply a conversion LUT twice. **أرقام / params:** haldclutsrc level 8; cube 33³ (or 65³); PSNR 51.9 / 47.9 dB measured.

```bash
G="curves=r='0/0 0.2/0.1 0.7/0.8 1/1':b='0/0.05 0.3/0.38 0.7/0.65 1/0.95',colorbalance=rs=0.08:gs=-0.02:bs=-0.08:rh=-0.04:gh=0.02:bh=0.08"
ffmpeg -f lavfi -i haldclutsrc=8 -vf "$G" -frames:v 1 teal_orange_hald.png
ffmpeg -i in.mp4 -i teal_orange_hald.png -filter_complex "[0][1]haldclut=interp=tetrahedral" -c:a copy out.mp4
ffmpeg -i in.mp4 -vf "lut3d=file=look.cube:interp=tetrahedral" -c:a copy out_cube.mp4
```

- **الدليل / proof:** `kosif-studio/motion/montage.py:42` · `kosif-atlas/skills/1096-akbun-editvideo/2445-akbun-davinciresolve-workflow/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2435-akbun-davinciresolve-logconvert/SKILL.md` · `100-superskills/skills/pro-video-editor-ffmpeg/references/ffmpeg-recipes.md`

#### COLOR-05 · لوكات المتصفح بالفلاتر وطبقات الدمج · Browser looks: CSS filter + blend-mode tint layers · ✅ مُثبت هنا / proven here
- **ماذا / what:** أحد عشر لوكًا من محرر «بصمة» تُبنى من فلتر CSS واحد وطبقات صبغة بأنماط دمج، مع منزلقات تباين وتشبع وإضاءة، وتلوين «الحبر والزعفران» الذي يعيد تلوين فيديو بلا إعادة ترميز. — Basma's eleven looks built from one CSS filter plus blended tint layers, with contrast/saturation/brightness sliders, and the 'ink & saffron' re-tone that recolours a clip at runtime without re-encoding.
- **متى أستخدمها / when:** مشاهد HTML/Canvas/Remotion تحتاج لوكًا فوريًا، أو معاينة قبل خبز تلوين FFmpeg. — HTML/Canvas/Remotion scenes that need an instant look, or a preview before baking an FFmpeg grade.
- **كيف / how:** Canvas: ctx.filter = look.f, drawImage, then for each tint [hex, alpha, mode] set globalAlpha + globalCompositeOperation and fillRect; then gradeFilter adds contrast() saturate() brightness() from sliders (contrast 0.8–1.4, saturate 0.5–1.6, brightness 0.8–1.2, vignette 0–0.8, optional soft-light tint alpha 0.16). Ink & saffron (video element): grayscale(1) sepia(.5) saturate(1.35) hue-rotate(-8deg) contrast(1.05) brightness(.82); banner wash linear-gradient(160deg, rgba(217,83,14,.55), rgba(29,24,20,.9)) with background-blend-mode:color. All 12 rendered in Chromium (Playwright) in this container on 2026-10-16. **أرقام / params:** 11 looks + ink_saffron; slider ranges c .8–1.4 / s .5–1.6 / b .8–1.2.

| look | CSS filter | طبقات الصبغة / tint layers |
|---|---|---|
| teal_orange | contrast(1.06) saturate(1.1) | #0b7285 20% soft-light + #ff9a3c 10% overlay |
| golden | sepia(.2) saturate(1.18) brightness(1.03) | #ffb347 18% soft-light |
| cyber | saturate(1.3) contrast(1.12) hue-rotate(-10deg) | #ff2bd6 10% screen + #16c7ff 12% soft-light |
| film | contrast(.94) saturate(.82) sepia(.12) | #161a22 100% lighten + #f4d9a8 8% soft-light |
| bw | grayscale(1) contrast(1.18) | — |
| cool / warm | saturate(1.02) / saturate(1.06) | #3a78ff 14% / #ff7a3a 13% soft-light |
| matrix | contrast(1.15) saturate(.85) | #1fa35a 20% soft-light + #06140b lighten |
| blue_hour | contrast(1.06) saturate(1.08) | #2f5fd0 20% soft-light + #ffb070 6% overlay |
| clean | contrast(1.12) saturate(1.18) brightness(1.01) | — |
| ink_saffron | grayscale(1) sepia(.5) saturate(1.35) hue-rotate(-8deg) contrast(1.05) brightness(.82) | banner wash, blend color |

```js
function applyLook(ctx, img, look, x, y, w, h) {
  ctx.save(); ctx.filter = look.f || 'none';
  ctx.drawImage(img, x, y, w, h); ctx.filter = 'none';
  for (const [hex, a, mode] of look.tint || []) {
    ctx.globalAlpha = a; ctx.globalCompositeOperation = mode;
    ctx.fillStyle = hex; ctx.fillRect(x, y, w, h);
  }
  ctx.restore();                      // alpha + composite reset
}
```

- **الدليل / proof:** `app/public/js/00_editor.js:204` · `app/public/js/00_editor.js:217` · `kosif-earth-ci-fork/unlock.html:85` · `kosif-earth-ci-fork/ui/ds/sqc.css:308`

#### COLOR-06 · سلسلة FFmpeg المُصدّرة من «بصمة» · Basma fingerprint grade chain export · 🟢 جاهز / ready
- **ماذا / what:** سكربت بايثون مُصدَّر من استوديو «بصمة» يعيد إنتاج التلوين بفلاتر FFmpeg عادية: eq وcolorbalance وفينيت وحبيبات وأشرطة سينما. — The Python script Basma exports reproduces a look with plain FFmpeg: eq, colorbalance, vignette, grain and letterbox bars.
- **متى أستخدمها / when:** حين تصمم اللوك في المتصفح وتريد رندرًا نهائيًا بـFFmpeg بنفس الروح. — design the look in the browser, render the final with FFmpeg.
- **كيف / how:** grade_chain(): eq=contrast:saturation:brightness=(b−1)·0.5; teal_orange → colorbalance rs=−0.08:bs=0.10:rh=0.08:bh=−0.06; bw → hue=s=0; warm/cool → colorbalance rm/bm ±0.6·k; vignette=PI/5 when strength > 0.3; grain → noise=alls=6+40·g:allf=t; letterbox → drawbox 10.5% top and bottom. Pure FFmpeg, nothing to install. **أرقام / params:** vignette PI/5 if >0.3; grain alls 6+40g; letterbox 10.5%.
- **الدليل / proof:** `app/public/js/10_studio.js:1683`

#### COLOR-07 · أمزجة فيلم الكلمات وتلوينها · Verse moods: palette plus matching footage grade · 🟢 جاهز / ready
- **ماذا / what:** خمسة أمزجة (ليل، فجر، ذهب، بحر، حبر) لكل منها لوحة سماء/هالة/ذرات، وكل مزاج يختار تلوين الفوتيج المناسب تلقائيًا، والفيلم يزداد إضاءة على طول قوسه. — Five moods (night, dawn, gold, sea, ink), each a sky/halo/mote palette that also picks the matching footage grade; the film brightens along its arc.
- **متى أستخدمها / when:** فيلم دعاء أو قصيدة أو أغنية من الصوت، بخلفية مرسومة أو فوق لقطات. — dua, poem or song films from sound, over painted skies or footage.
- **كيف / how:** `verse.py AUDIO --mood night|dawn|gold|sea|ink --accent '#E7B65A'`; songreel MOOD_GRADE maps night→blue_hour, dawn/gold→golden_hour, sea→teal_orange, ink→vintage_film (COLOR-01). Each section shifts hue +7°/−5° and brightness rises 0.9→1.15 over the film. **أرقام / params:** night #0B0F1E/#221C3B glow #ECBD51 mote #F9E094; dawn #12142B/#994329/#FAA442/#FFDDA3; gold #110D09/#372715/#EEAD2B/#FBD774; sea #07131D/#16444B/#3CDDD2/#ACF6F6; ink #0A0A0A/#1C1C1C/#B2B2B2/#EBEBEB.

| mood | sky top → bottom | glow · mote | footage grade |
|---|---|---|---|
| night | #0B0F1E → #221C3B | #ECBD51 · #F9E094 | blue_hour |
| dawn | #12142B → #994329 | #FAA442 · #FFDDA3 | golden_hour |
| gold | #110D09 → #372715 | #EEAD2B · #FBD774 | golden_hour |
| sea | #07131D → #16444B | #3CDDD2 · #ACF6F6 | teal_orange |
| ink | #0A0A0A → #1C1C1C | #B2B2B2 · #EBEBEB | vintage_film |

- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/verse.py:49` · `100-superskills/skills/kosif-montage-motion/scripts/songreel.py:78` · `100-superskills/skills/kosif-montage-motion/templates/verse.html:79` · `kosif-one/tools/kosif-studio/motion/templates/verse.html:64`

#### COLOR-08 · مكتبة اللوكات المسماة · Named film-stock and photo looks library · 📄 موصوف / documented only
- **ماذا / what:** قاموس لوكات بأسماء يفهمها العميل: أفلام كوداك وفوجي وسينستيل، و«بليتش بايباس» و«ويس أندرسون» الباستيل، وسبعة لوكات صور بوحدات أدوبي. — A vocabulary of looks a client recognises: Kodak/Fuji/CineStill stocks, bleach bypass, pastel Wes, and seven photo-set looks in Adobe units.
- **متى أستخدمها / when:** حين يقول العميل «أبغاه سينمائي/دافئ/قديم» وتحتاج اسمًا ونقطة بداية رقمية. — a client says 'cinematic / warm / old' and you need a name plus a numeric start.
- **كيف / how:** Director KB (CSS base + mood): teal_orange (blockbuster, contrast 1.12 sat 1.15), bleach_bypass (gritty, contrast 1.3 sat .6), cold_desat (sad, sat .6 brightness .96), warm_vintage (nostalgia, sepia .25 contrast .95), kodak_portra (intimate, contrast .95 brightness 1.04), vision3_500t (filmic night, contrast 1.1), cinestill_800t (dreamy neon, contrast 1.08 sat 1.1), fuji_velvia (vivid travel, contrast 1.2 sat 1.45), noir_bw (grayscale, contrast 1.4), neon_cyber (contrast 1.15 sat 1.35), pastel_wes (contrast .88). Film shorthand: Portra 400, Ektar 100, CineStill 800T split tone #D4A050 highlights / #1A3040 shadows, Velvia. Photo looks (Adobe units — exact needs the Adobe connector; approximate locally with colortemperature/vibrance/eq or a numpy .cube): Warm & Golden temp 32/120 lum 67 vibrance +15; Bright & Airy 20/60/62 sat −10 vibrance +10 brightness +15; Moody & Cinematic 20/−50/45 sat −20 contrast +25; Cool & Fresh 18/−123/45 vibrance +10. Translate to COLOR-01/05 chains; never promise an exact stock emulation. **أرقام / params:** 11 KB grades; CineStill split #D4A050/#1A3040; 7 photo looks.
- **الدليل / proof:** `app/public/js/10_studio.js:8` · `kosif-one/tools/kosif-omni/skills/kosif-image-studio/references/prompt-library.md` · `kosif-atlas/skills/103-adobe-for-creativity/230-adobe-batch-edit-photos/SKILL.md`

#### COLOR-09 · نموذج تلوين HyperFrames · HyperFrames WebGL grade model, 17 presets and media-treatment CLI · 📦 بأمر تثبيت / one install
- **ماذا / what:** محرك تلوين WebGL كامل: تعريض وتباين وإضاءات وظلال وأبيض وأسود وحرارة وصبغة وحيوية وتشبع، وعجلات وثلاثة منحنيات وحتى أربع تحديدات HSL وحبيبات وفينيت وLUT، مع 17 إعدادًا جاهزًا وأداة تحفظ المعالجة على العنصر. — A full WebGL grade: exposure/contrast/highlights/shadows/whites/blacks/temperature/tint/vibrance/saturation, wheels, curves, up to 4 HSL selections, grain, vignette, custom .cube, 17 presets, and a CLI that persists the treatment on an element.
- **متى أستخدمها / when:** تركيبات HyperFrames أو صور/فيديو داخل HTML تحتاج تلوينًا قابلًا للقياس والمقارنة. — HyperFrames compositions or HTML media that need measurable, comparable grading.
- **كيف / how:** Grade object `{preset, intensity, adjust:{exposure −2..2, others −1..1}, details:{vignette, vignetteFeather, grain, grainSize}, colorSpace:'rec709'}`. Persist: `npx hyperframes media-treatment --selector '#hero' --grading '<json>' --apply --json`; measure with `--analyze --json`; list controls with `--capabilities --json`. Presets: neutral, warm-daylight (exposure .06 contrast .07 temperature .18 sat .08), clean-studio, skin-soft, food-pop (contrast .1 temperature .14 sat .18), night-lift, muted-editorial (sat −.12 vignette .1), vintage-wash, mono-clean (sat −1), mono-fade, soft-boost, bright-pop, deep-contrast (contrast .2), creator-camcorder, vhs-playback, editorial-halftone, two-ink-print. grade-compare renders a 16-cell A/B sheet. Vendored source in kosif-one/vendor/hyperframes; the CLI is not installed here. **أرقام / params:** 17 presets; HSL selections ≤4; exposure −2..2; grade-compare 16 cells.
- **التثبيت / install:** `npm i -D hyperframes@0.8.164   # then: npx hyperframes media-treatment --capabilities --json`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/packages/core/src/colorGrading.ts:448` · `kosif-one/vendor/hyperframes/packages/cli/src/commands/media-treatment.ts` · `kosif-one/vendor/hyperframes/docs/guides/color-grading.mdx` · `kosif-one/vendor/hyperframes/skills/media-use/references/grading.md`

#### COLOR-10 · وصفات المعالجة وممرات الملاحظات · HyperFrames treatment recipes and feedback lanes · 📦 بأمر تثبيت / one install
- **ماذا / what:** 19 بذرة معالجة مختبرة (بورتريه طبيعي، صقل منتج، VHS، 8 ملم، هافتون، طباعة بلونين...) وقاعدة تحوّل ملاحظة العميل الغامضة إلى «ممر» معالجة محدد. — 19 tested treatment seeds (natural portrait, product polish, VHS, 8mm, halftone, two-ink print…) plus a rule that maps vague client feedback to one treatment lane.
- **متى أستخدمها / when:** «خلّه أدفأ» أو «أبغاه قديم» أو «سوّه مثل الطباعة» — تحتاج قرارًا صحيحًا لا تخمينًا. — 'make it warmer', 'make it old', 'make it look printed' — decide, don't guess.
- **كيف / how:** Lanes: correction (too dark/flat/warm) → wheels/curves/HSL secondary → preset or custom treatment (premium, cinematic) → shader effect (retro, print, ASCII, glitch, camcorder) → privacy blur/pixelate → framing/motion → seek-safe treatment keyframes. First inspect an early/middle/late contact sheet (`hyperframes snapshot <p> --frames 3`), then start from a seed and tune only inside its bounded ranges; adjust values are absolute, not deltas. **أرقام / params:** Natural Portrait {preset:'skin-soft', intensity:0.6}; VHS grain .16 tapeDamage .82 tapeTracking .85 chromaBleed .5 CA .18 scanlines .35 glitch .32.

| seed | الاستخدام / use | المفتاح / key |
|---|---|---|
| Natural Portrait | متحدث، مقابلة | skin-soft @0.6 — ليس تنعيم بشرة |
| Product Polish | منتج ولايف ستايل | احمِ لون المنتج والملصق، فينيت خفيف فقط |
| UI Fidelity | تسجيل شاشة | بكسلات الواجهة كما هي |
| Film Memory | حنين دافئ مقيد | قاعدة ثابتة + طابع زمني |
| Creator Camcorder | UGC محمول | بكسل + HUD اختياري |
| VHS Playback | شريط تناظري | grain .16, tapeDamage .82, scanlines .35 |
| 8mm Home Movie | فيلم منزلي | weave + flicker |
| Editorial Halftone / Two-Ink Print / Mono Screen Print | طباعة تحريرية | halftone / twoInkPrint / monoScreen |
| Engraved / Crosshatched | رسم محفور ومظلل | engraving / crosshatch |
| CRT Display / Procedural ASCII | شاشة قديمة، فن حروف | crtCurvature+scanlines / ascii |
| Ordered Dither / Error Diffusion | تقليل ألوان | Bayer / dither.mjs offline |
| Organic Light Leak / Social Flash / Freeze-Frame | انتقالات معالجة | registry overlays |

- **التثبيت / install:** `npm i -D hyperframes@0.8.164`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/media-use/references/media-treatment-recipes.md` · `kosif-one/vendor/hyperframes/skills/media-use/references/media-treatments.md`

#### COLOR-11 · لوكات LUT مع بديل حتمي · LUT looks with deterministic buildCube fallback · 📦 بأمر تثبيت / one install
- **ماذا / what:** ثلاثة لوكات LUT مفهرسة تُجلب عند الطلب، ومع غياب الشبكة تُبنى محليًا من معاملاتها بمكعب 33³ — فلا تعتمد على ملف مجهول. — Three indexed LUT looks fetched on demand; offline they are rebuilt locally from parameters as a 33³ cube.
- **متى أستخدمها / when:** تريد لوك LUT معروفًا بنتيجة قابلة للتكرار حتى بلا إنترنت. — a known LUT look with reproducible output, even offline.
- **كيف / how:** `npx hyperframes media-use resolve --type lut …` (add `--local-only` to force buildCube). teal-orange-blockbuster (intensity .85; contrast .18; split tone shadows [−.04,.05,.09] highlights [.1,.04,−.03]); bleach-bypass (.8; contrast .55, saturation −.72); film-fade (.75; blacks +.35, contrast −.28, temperature +.16). Never paste a .cube into context — reference the file. **أرقام / params:** cube 33³ default; 3 looks.
- **التثبيت / install:** `npm i -D hyperframes@0.8.164`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/media-use/luts/index.json` · `kosif-one/vendor/hyperframes/skills/media-use/luts/README.md` · `kosif-one/vendor/hyperframes/skills/media-use/references/grading.md`

#### COLOR-12 · كشف التلوين بالمقارنة · Grade Split Reveal (flat → graded sweep) · 📦 بأمر تثبيت / one install
- **ماذا / what:** الصورة نفسها مرتين — خام ومُلوّنة — بحافة صلبة تمسح الإطار، تتوقف للمقارنة، ثم تستقر على النسخة الملوّنة؛ والتلوينان حقيقيان بـWebGL. — The same picture twice — flat and graded — with a hard edge that sweeps, pauses for comparison, then commits to the grade; both are real WebGL grades.
- **متى أستخدمها / when:** ريل «قبل/بعد» لخدمة تلوين أو تعليم المونتاج. — before/after reels for grading services or editing lessons.
- **كيف / how:** `npx hyperframes add grade-split-reveal` → mount on a `.clip` div with data-composition-src/data-start/data-duration/data-track-index and JSON data-variable-values. Looks: warm-cinematic (deep-contrast, contrast .28, temp .18, vibrance .26, vignette .3, grain .1) | cool-teal (contrast .32, temp −.26, tint .08) | bleach-bypass (contrast .54, sat −.46, grain .18); split 62% (25–85); edge hairline 2 px | bold 6 px | hidden. Extra duration becomes hold, never time-stretch. Pure-HTML alternative: two stacked layers, top one clip-path inset animated left→right. **أرقام / params:** split 62% (25–85); edge 2/6 px; 3 looks.
- **التثبيت / install:** `npm i -D hyperframes@0.8.164 && npx hyperframes add grade-split-reveal`
- **الرخصة / license:** registry compositions are timed with GSAP — GSAP 'Standard no-charge' license (gsap.com/standard-license), not MIT.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/grade-split-reveal/grade-split-reveal.html` · `kosif-one/vendor/hyperframes/registry/components/grade-split-reveal/registry-item.json` · `kosif-one/vendor/hyperframes/docs/catalog/components/grade-split-reveal.mdx`

## التصحيح المقاس والتحليل والمطابقة — Measured correction, analysis & matching

_التصحيح التقني قبل الإبداعي: تقيس ثم تصحح، وتطابق لقطاتك مع مرجع بأرقام محدودة لا تنفلت._

#### COLOR-13 · ترتيب عقد التلوين · Grade order: technical before creative · 📄 موصوف / documented only
- **ماذا / what:** التصحيح التقني أولًا لكل لقطة ثم عقدة «لوك» إبداعية منفصلة؛ لا تخلطهما أبدًا. — Per-clip technical correction first, then a separate creative LOOK node; never mix the two.
- **متى أستخدمها / when:** كل مشروع فيه أكثر من لقطة حقيقية. — every project with more than one real clip.
- **كيف / how:** Resolve: EXPOSURE → WB (before the Log→Rec.709 transform) → CST/LUT → CONTRAST → SAT (ceiling ~1.25 with shadow/highlight roll-off) → LOOK as a new serial node; LUT/CST runs first in time and everything is measured on its output. DWG/Intermediate path: input CST → global exposure → WB → contrast 1.3 pivot 0.336 → colour-slice sat → selective → output CST → creative LUT, tetrahedral. FFmpeg analogue: eq/exposure → colorbalance/colortemperature → lut3d → eq=contrast → hue=s → look LUT/curves, each its own filter. Phone footage needs less. **أرقام / params:** SAT ≤1.25; DWG contrast 1.3 pivot 0.336.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2445-akbun-davinciresolve-workflow/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2445-akbun-davinciresolve-workflow/references/look-scopes.md` · `100-superskills/skills/davinci-resolve-pipeline/references/color-grading-order.md`

#### COLOR-14 · كشف اللوج قبل LUT · Log detection before a conversion LUT · ✅ مُثبت هنا / proven here
- **ماذا / what:** لا تطبق LUT تحويل Log إلا على لقطة ثبت أنها Log؛ وسم bt709 والمظهر الباهت ليسا دليلًا. — Apply a Log→Rec.709 LUT only to clips proven Log; a bt709 tag or a flat look is not evidence.
- **متى أستخدمها / when:** لقطات كاميرا أو آيفون مختلطة المصادر. — mixed camera/iPhone sources.
- **كيف / how:** Priority: user profile > NLE input colour space/gamma containing 'log' > `ffprobe -show_streams -of json` color_transfer containing 'log' > 8-bit yuv420p ⇒ not Log (Apple Log / I-Log are 10-bit). Some Log files are tagged bt709. Then `lut3d=Log_to_Rec709.cube` (65-point), once only. `--selftest` passed in this container on 2026-10-16 (PYTHONPATH = the exposure skill's scripts). Live CDL writes need DaVinci Resolve Studio (paid app, not here); in this container apply the same numbers with FFmpeg. **أرقام / params:** 10-bit required for Apple Log / I-Log; 65-point cube.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2435-akbun-davinciresolve-logconvert/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2435-akbun-davinciresolve-logconvert/scripts/logconvert.py`

#### COLOR-15 · التعريض حسب وقت اليوم · Exposure bands by time of day + cut jump caps · ✅ مُثبت هنا / proven here
- **ماذا / what:** لا تساوِ إضاءة كل اللقطات: الليل أغمق والساعة الذهبية الأسطع، وحدّ أقصى لقفزة الإضاءة بين لقطتين متتاليتين حتى لا تتعب العين. — Don't normalise everything: night darker, golden hour brightest, and cap the brightness jump between adjacent cuts to avoid flicker fatigue.
- **متى أستخدمها / when:** مونتاج سفر أو فلوج يمتد عبر اليوم. — travel montages and vlogs spanning a day.
- **كيف / how:** Measure median luma (10-bit 0–1023): night 120–280, morning 320–460, day 420–560, golden 440–600, blue hour 310–485. Adjacent tail→head difference ≤60 same period / ≤120 across periods; per-clip shift ≤±120; >0.5% pixels clipped lowers target by 40; tolerance 15; sunrise/sunset windows ±30 min / 1.5 h. FFmpeg: `signalstats` YAVG → `eq=brightness/gamma`. `--selftest` passed in this container on 2026-10-16 (PYTHONPATH = the exposure skill's scripts). Live CDL writes need DaVinci Resolve Studio (paid app, not here); in this container apply the same numbers with FFmpeg. **أرقام / params:** bands 120–280 / 320–460 / 420–560 / 440–600 / 310–485; jump ≤60/≤120.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2434-akbun-davinciresolve-exposure/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2434-akbun-davinciresolve-exposure/scripts/exposure_scope.py`

#### COLOR-16 · توازن الأبيض بالبكسلات المحايدة · Neutral-pixel white balance · ✅ مُثبت هنا / proven here
- **ماذا / what:** تقدير الصبغة من البكسلات الرمادية متوسطة الإضاءة، وتثبيت الأخضر وتحريك الأحمر والأزرق — مع خيار إبقاء دفء أو برودة مقصودة. — Estimate the cast from low-saturation mid-brightness pixels, hold G and move R/B, optionally keeping a deliberate warm or cool bias.
- **متى أستخدمها / when:** لقطة مصفرة أو مزرقة بلا قصد. — an unintended yellow or blue cast.
- **كيف / how:** Downscale to 320 px; neutral = max channel 25–85% and saturation ≤20%; need ≥0.5% of pixels; target R−B = 0 (or +30 warm / −20 cool on request); CDL Offset ±0.10, Slope 1±0.20, ≤3 secant iterations. FFmpeg: colorbalance / colortemperature / colorchannelmixer, or `grayworld` (built in here). `--selftest` passed in this container on 2026-10-16 (PYTHONPATH = the exposure skill's scripts). Live CDL writes need DaVinci Resolve Studio (paid app, not here); in this container apply the same numbers with FFmpeg. **أرقام / params:** R−B 0/+30/−20; offset ±.10; slope 1±.20.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2444-akbun-davinciresolve-whitebalance/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2444-akbun-davinciresolve-whitebalance/scripts/whitebalance.py`

#### COLOR-17 · تباين حول محور مع حماية القص · Pivot contrast with clip guard · ✅ مُثبت هنا / proven here
- **ماذا / what:** تباين S حول نقطة ارتكاز تناسب فضاء العقدة، ويتراجع تلقائيًا إذا بدأ السواد أو البياض بالقص. — S-contrast around a pivot matched to the node space that backs off automatically if blacks or whites clip.
- **متى أستخدمها / when:** فوتيج مسطح يحتاج «عمقًا» دون فقد تفاصيل. — flat footage that needs depth without losing detail.
- **كيف / how:** Default 1.15 (range 0.5–1.5), pivot 0.435 on the LUT path, 0.336 for DaVinci Intermediate; clipping if p1 < 16 or p99 > 1008 (10-bit) or >0.5% clipped → reduce, max 3 retries, stop at 1.0. FFmpeg: curves S or eq=contrast with a pivoted lutyuv. `--selftest` passed in this container on 2026-10-16 (PYTHONPATH = the exposure skill's scripts). Live CDL writes need DaVinci Resolve Studio (paid app, not here); in this container apply the same numbers with FFmpeg. **أرقام / params:** 1.15; pivot .435/.336; p1<16, p99>1008.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2432-akbun-davinciresolve-contrast/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2432-akbun-davinciresolve-contrast/scripts/contrast.py`

#### COLOR-18 · أرضية تشبع وانحدار سينمائي · Saturation floor with film roll-off · ✅ مُثبت هنا / proven here
- **ماذا / what:** أضف تشبعًا فقط للقطات الباهتة عن نطاق وقتها (لا تنقص أبدًا)، بحد 1.25، واخفض التشبع في الظلال والإضاءات العالية كما يفعل الفيلم. — Only add saturation to clips below their time-of-day band (never remove), capped at 1.25, rolling saturation off in shadows and highlights like film.
- **متى أستخدمها / when:** لقطات هاتف رمادية أو ضبابية. — grey or hazy phone shots.
- **كيف / how:** Bands (mean max−min, 10-bit): morning 50–110, day 60–120, afternoon 60–130, evening 45–100, night 30–80; Sat = floor/measured ≤1.25; roll-off below 15% and above 85% luma down to 60%. FFmpeg: eq=saturation / hue=s plus a luma-selective lutyuv. `--selftest` passed in this container on 2026-10-16 (PYTHONPATH = the exposure skill's scripts). Live CDL writes need DaVinci Resolve Studio (paid app, not here); in this container apply the same numbers with FFmpeg. **أرقام / params:** cap 1.25; roll-off 15%/85% → 60%.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2440-akbun-davinciresolve-saturation/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2440-akbun-davinciresolve-saturation/scripts/saturation.py`

#### COLOR-19 · تعزيز السماء فقط · Sky hue-window boost · ✅ مُثبت هنا / proven here
- **ماذا / what:** تعميق السماء الزرقاء وحدها بنافذة لونية ناعمة حول 215°، دون لمس العشب أو البشرة. — Deepen blue skies only, with a soft hue window around 215°, leaving grass and skin alone.
- **متى أستخدمها / when:** لقطات خارجية بسماء باهتة. — exteriors with washed-out skies.
- **كيف / how:** Resolve DCTL: weight w falls off outside 215° ±20°, sat × (1 + 0.25w), lum × (1 − 0.1w), measured on the upper half. FFmpeg 6.1 here: `huesaturation=colors=b+c:saturation=0.25:intensity=-0.04:strength=5` — tested on a synthetic frame: sky #7fa8d8→#70a0da while grass #6b8a3c and skin #d9a27a stayed identical. `--selftest` passed in this container on 2026-10-16 (PYTHONPATH = the exposure skill's scripts). Live CDL writes need DaVinci Resolve Studio (paid app, not here); in this container apply the same numbers with FFmpeg. **أرقام / params:** hue 215° width 40° sat 1.25 lum 0.9; ffmpeg strength 5.

```bash
ffmpeg -i in.mp4 -vf "huesaturation=colors=b+c:saturation=0.25:intensity=-0.04:strength=5" -c:a copy sky.mp4
```

- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2442-akbun-davinciresolve-sky/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2442-akbun-davinciresolve-sky/scripts/sky.py`

#### COLOR-20 · لوكات مقاسة بأهداف السكوب · Scope-target looks (Japan summer, New York, Still, Tokyo night) · 📄 موصوف / documented only
- **ماذا / what:** لوكات إبداعية مكتوبة كأهداف قياس على مخرج Rec.709: نسب IRE لـP10/P50/P95 ونصف قطر عناقيد اللون على الفكتورسكوب. — Creative looks written as measurable targets on the Rec.709 output: P10/P50/P95 in IRE and colour-cluster radius on a normalised vectorscope.
- **متى أستخدمها / when:** تريد لوكًا تتحقق منه بالأرقام لا بالعين فقط. — a look you can verify by numbers, not only by eye.
- **كيف / how:** Y'=0.2126R'+0.7152G'+0.0722B', IRE=100·Y'; Cb=(B'−Y')/1.8556, Cr=(R'−Y')/1.5748; radius normalised to the 100% colour-bar hexagon. Build with curves/colorbalance/lut3d, compare +0/+1/+2 stop variants, then measure. **أرقام / params:** see table.

| look | P10 / P50 / P95 IRE | >99 IRE | عناقيد اللون / clusters |
|---|---|---|---|
| Japan summer | 8±4 / 46±8 / 91±7 | ≤0.2% | foliage 32%±8, sun orange 36%±8 |
| New York golden | 7±4 / 48±8 / 93±6 | ≤0.3% | red/orange 48%±10, blue/teal 42%±10 |
| Still (muted urban) | 8±3 / 39±6 / 84±7 | ≤0.1% | grey ≤8%, green/teal 29%±6 |
| Tokyo night | 4±4 / 20±8 / 78±12 | ≤0.5% | teal ambient 35%±12, warm practicals 70%±15 — لا ترفع الظلال المشوشة |

- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2436-akbun-davinciresolve-look-japan-summer/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2437-akbun-davinciresolve-look-new-york/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2438-akbun-davinciresolve-look-still/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2439-akbun-davinciresolve-look-tokyo-night`

#### COLOR-21 · توجيه التلوين حسب اللقطة وأرضية الإضاءة · Per-shot-type direction, one light floor, value before colour · 📄 موصوف / documented only
- **ماذا / what:** جدول تلوين لكل نوع لقطة، وأرضية إضاءة واحدة وسقف واحد للفيلم كله، والقيمة (الفاتح/الغامق) تُقرر قبل اللون. — A grade table per shot type, one luminance floor and ceiling per film, and value (light/dark) decided before hue.
- **متى أستخدمها / when:** أي فيلم يجمع متحدثًا وتسجيل شاشة وجرافيك. — any film mixing talking head, screen recording and graphics.
- **كيف / how:** Table shot type | colour direction | notes: talking head = base grade with warm ambient pull; screen recordings crisp, high-contrast on text; graphics on the brand background; animation free palette; drifting scenes get a correction note. Name one floor (deepest black) and the brightest section's ceiling — no jumps dark→white. Realistic tonal range > 150 of 255; peak saturation only in fire and eyes. **أرقام / params:** tonal range >150/255; one floor per film.
- **الدليل / proof:** `kosif-atlas/skills/3067-youtube/13229-creator-visual-director/SKILL.md` · `100-superskills/skills/motion-director-pro/references/motion-floor.md` · `kosif-studio/references/drawing-guide.md:62`

#### COLOR-22 · تحليل حرارة اللون والميل والتشبع · Colour analysis: CCT, cast, colourfulness, 6-colour palette · ✅ مُثبت هنا / proven here
- **ماذا / what:** أداة تقرأ صورة أو إطارًا وتعطيك: حرارة اللون بالكلفن، وميله الدافئ/البارد، ومقدار الألوان، وتوزيع الإضاءة، وستة ألوان سائدة بحصصها. — Reads an image or frame and returns CCT in kelvin, warm/cool cast, colourfulness, tonal zones and six dominant colours with shares.
- **متى أستخدمها / when:** قبل التلوين لتعرف أين أنت، وبعده لتثبت ما تغير. — before grading to know where you are, after to prove what changed.
- **كيف / how:** `python3 kosif-one/tools/kosif-omni/skills/kosif-vision/scripts/image_analyze.py FRAME.png` → JSON: exposure (p1/median/p99, clipped %, zones, verdict), colour (McCamy CCT via sRGB→linear→XYZ, valid 1000–25000 K; cast warm if R̄−B̄ > 12, cool if < −12; colourfulness = hypot(σrg, σyb) + 0.3·hypot(μrg, μyb) labelled <15 not … >82 highly) and palette (median-cut to 6 on a 256 px thumbnail). Ran here on a graded frame. **أرقام / params:** cast ±12; CCT 1000–25000 K; palette k=6 @256 px.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-vision/scripts/image_analyze.py:100` · `100-superskills/skills/kosif-montage-motion/scripts/omni/image_analyze.py:59` · `100-superskills/skills/kosif-montage-motion/scripts/omni/image_analyze.py:120`

#### COLOR-23 · إزاحة الميرد واختيار الجل · Mired shift → CTO/CTB gel · ✅ مُثبت هنا / proven here
- **ماذا / what:** حساب حتمي: من حرارة إلى حرارة كم «ميرد» وأي جل يقرّبك — لتخطيط إضاءة لقطة أو برومبت أو مشهد ثلاثي الأبعاد مقنع. — Deterministic maths: mired shift between two colour temperatures and the nearest gel, for believable lighting in shots, prompts and 3D.
- **متى أستخدمها / when:** مزج ضوء تنجستن مع نهار، أو وصف إضاءة واقعية لمولد صور. — mixing tungsten and daylight, or describing real lighting to a generator.
- **كيف / how:** `echo '{"op":"mired","from_k":3200,"to_k":5600}' | python3 light_calc.py` → shift = 1e6/to − 1e6/from. Ran here: −133.9 → Full CTB, 'cooler (blue)'. Gels: Full CTB −159, ½ CTB −68, ¼ CTB −30, ⅛ CTB −12, ⅛ CTO +20, ¼ CTO +42, ½ CTO +81, Full CTO +159. **أرقام / params:** 3200→5600 K = −133.9 mired → Full CTB.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-lighting/scripts/light_calc.py:69` · `kosif-one/tools/kosif-omni/skills/kosif-lighting/scripts/light_calc.py:22` · `100-superskills/skills/kosif-montage-motion/scripts/omni/light_calc.py:69`

#### COLOR-24 · استخراج الباليت وتسمية الألوان · Palette extraction, colour naming and ΔE · ✅ مُثبت هنا / proven here
- **ماذا / what:** يسحب الألوان السائدة من أي مرجع ويسمّيها بأقرب اسم من 20 اسمًا بمسافة Lab، ويقيس الفرق ΔE — لبناء قفل أسلوب أو جملة يفهمها العميل. — Pulls dominant colours from any reference, names them by nearest Lab distance among 20 names, and measures ΔE — for a style lock or a client-readable sentence.
- **متى أستخدمها / when:** «أبغى ألوان هذا الفيديو» أو مقارنة لونين بالأرقام. — 'I want this video's colours', or comparing two colours numerically.
- **كيف / how:** mm_color.palette(img, k=5) → [{hex, share, name}], color_name(rgb), delta_e(c1,c2) — ran here (testsrc → #9DFE77 green 49.7%, #A300FC purple 31.3%). Studio qa.study → k-means k=6 (KMEANS_PP, 30 iters, eps 0.5, 3 attempts) into style_guide.md (needs OpenCV). Basma analyzeRef: 16–72 samples every 0.25 s at 40×40, 512-bucket RGB histogram weighted 0.25+saturation, keep colours with L1 > 90; darkest → bg, most saturated → accent. **أرقام / params:** 20 names; k 5–6; Basma L1 > 90.
- **الدليل / proof:** `kosif-one/tools/kosif-mimic/scripts/mm_color.py:134` · `kosif-studio/motion/qa.py:383` · `app/public/js/00_editor.js:1299`

#### COLOR-25 · باليت وخلفية لكل نبضة من المرجع · Reference palette + background per beat · ✅ مُثبت هنا / proven here
- **ماذا / what:** يقسم فيديو مرجعيًا إلى نبضات (قطع، ذوبان، دخول) ويعطي كل نبضة لون خلفية وباليت، بدقة ±8 لكل قناة في الاختبار. — Splits a reference video into beats (cuts, dissolves, entrances) and gives each beat a background hex and palette, within ±8 per channel on synthetic tests.
- **متى أستخدمها / when:** تحليل ريل مرجعي قبل إعادة بنائه بلغة KOSIF. — analysing a reference reel before rebuilding it.
- **كيف / how:** `analyze.analyze(film, out)` → analysis.json {width, height, aspect, duration, beats:[{t0,t1,background,palette:[{hex}]}], scenes, audio:{lufs}} + overview.jpg, timeline.jpg, brief.json and 3 frames per beat; beats ≤3.05 s. tests/test_analyze.py ran here: 5 tests OK. **أرقام / params:** ±8/channel; beats ≤3.05 s; 3 frames per beat.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_analyze.py:50` · `100-superskills/skills/kosif-montage-motion/tests/test_analyze.py:39`

#### COLOR-26 · نقل رينهارد إلى LUT لكل لقطة · Reinhard Lab transfer → per-shot .cube · ✅ مُثبت هنا / proven here
- **ماذا / what:** يطابق إحصاءات Lab للقطة جديدة مع لقطة مرجعية ويخبزها في LUT بحجم 33³ يُطبق لكل لقطة على حدة. — Matches a new shot's Lab statistics to a reference shot and bakes it into a 33³ LUT applied per shot.
- **متى أستخدمها / when:** «خلّ لقطاتي بنفس ألوان هذا الفيلم». — 'make my shots look like this film'.
- **كيف / how:** lab_stats(src) / lab_stats(ref) → reinhard_lut(src, dst, size=33, strength=0.85, max_gain=2.2) → write_cube → apply_lut or FFmpeg lut3d. Ran here: mean Lab (69.0, 14.8, 10.3) moved toward the sodium_night reference (62.7, 11.7, 17.1) → (64.4, 10.4, 16.1); the written .cube also applied with ffmpeg lut3d (rc=0). Gains clamped so flat sources cannot explode. **أرقام / params:** size 33; strength .85; max_gain 2.2.

```python
import mm_color as C   # kosif-one/tools/kosif-mimic/scripts
lut = C.reinhard_lut(C.lab_stats(src_rgb), C.lab_stats(ref_rgb), size=33, strength=0.85)
C.write_cube('shot03.cube', lut, 33)      # ffmpeg -vf lut3d=file=shot03.cube
```

- **الدليل / proof:** `kosif-one/tools/kosif-mimic/scripts/mm_color.py` · `100-superskills/skills/kosif-mimic/scripts/mm_color.py:1` · `100-superskills/skills/kosif-mimic/scripts/mm_build.py:105`

#### COLOR-27 · مطابقة اللقطات بنقل لوني محدود · Bounded colour transfer + Hungarian shot match · ✅ مُثبت هنا / proven here
- **ماذا / what:** يختار لكل لقطة مرجعية أنسب مقطع ونقطة بداية من مكتبتك (لون، تباين، تشبع، حركة) بالتعيين المجري، ثم ينقل اللون بمكسب وإزاحة محدودين لا ينفلتان. — Picks, for every reference shot, the best pool clip and in-point (colour, contrast, saturation, motion) by Hungarian assignment, then transfers colour with clamped gain/offset.
- **متى أستخدمها / when:** إعادة بناء مونتاج مرجعي من لقطاتك أنت. — rebuilding a reference montage from your own footage.
- **كيف / how:** `mimic match PROJECT/study --pool POOL [--set N=file@sec] [--strength 0.7]`; colour_transfer(look{mean,std}, mean, std, strength) → per channel (gain, offset) with 0.6 ≤ gain ≤ 1.6 and −120 ≤ offset ≤ 120; windows containing source cuts are rejected. Real study: costs 0.356–0.602, gains .82–1.6, offsets −73…+113. tests/test_mimic.py ran here: 10 tests OK. **أرقام / params:** gain .6–1.6; offset ±120; strength .7.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_mimic.py:91` · `100-superskills/skills/kosif-montage-motion/references/mimic.md` · `kosif-one/projects/mimic-jumuah/study/match.json`

#### COLOR-28 · إصلاح تلقائي ومطابقة مرجع في «بصمة» · Basma measured auto-fix, reference match and look classifier · 📦 بأمر تثبيت / one install
- **ماذا / what:** يصلح الفيديو المعتم أو المسطح أو المصبوغ من بكسلاته بلا ذكاء اصطناعي ويشرح الإصلاح بالعربية، ويطابق مقطعك مع مرجع، ويسمّي لوك المرجع. — Fixes dark/flat/cast footage from its own pixels without AI and explains the fix in Arabic, matches a clip to a reference, and labels the reference's look.
- **متى أستخدمها / when:** مستخدم يرفع مقطعًا «مو حلو» أو يقول «سوّه مثل هذا». — a user uploads a 'not nice' clip or says 'make it like this'.
- **كيف / how:** measureFix(): luma percentiles p02/p50/p98; contrast = clamp(200/range, 0.9, 1.3) when range < 200; brightness toward mid 118 (0.85–1.3) when mid outside 112–150; saturation clamp(0.24/s, 1, 1.25) when 0.05 < s < 0.18; grey-world on near-neutral pixels (s < 0.22, 50 < l < 215, ≥6% of pixels) → per-channel gains 0.82–1.18 as a multiply colour. Match: contrast ratio clamp 0.8–1.4, saturate 0.5–1.6, brightness 0.8–1.2, tint = reference mean hex, bw when ref saturation < 0.08, letterbox copied. DNA classifier: sat < 0.07 → bw; blue shadows > 6 with red highlights > 10 → teal_orange; warmth > 0.1 → golden (sat > 0.3) or warm; warmth < −0.05 → blue_hour (mean L < 90) or cool; contrast > 0.26 & sat > 0.32 → clean; sat > 0.45 & dark → cyber. Runs inside the Basma editor (Vite app). **أرقام / params:** contrast .9–1.3; gains .82–1.18; mid 118.
- **التثبيت / install:** `cd /home/user/app && npm install && npm run dev`
- **الدليل / proof:** `app/public/js/00_editor.js:2976` · `app/public/js/00_editor.js:2364` · `app/public/js/10_studio.js:1213`

#### COLOR-29 · تغيير لون بلون مع الحفاظ على الظل · Local recolour A→B keeping shading (Arabic requests) · ✅ مُثبت هنا / proven here
- **ماذا / what:** «غيّر الأحمر إلى أزرق» تُنفذ محليًا: قناع لوني بتسامح، ثم استبدال الصبغة مع إبقاء الطيات والظلال، وفهم طلبات العربية والإنجليزية. — 'Change red to blue' done locally: a tolerant colour mask, hue replacement that keeps folds and shading, and parsing of Arabic or English requests.
- **متى أستخدمها / when:** تعديل لون قميص أو منتج أو خلفية في صورة أو إطار. — recolouring a shirt, product or background in a still or frame.
- **كيف / how:** edit_pack TOOLS: recolor(img, src_hex, dst_hex, tolerance=40, region=None, keep_shading=True) via HSV (V scaled by dst/src, S scaled), plus adjust(brightness/contrast/saturation/sharpness), tint(hex, 0.3), erase(softness 14). parse_colour_request('غيّر الأحمر إلى أزرق') → ('#d62828', '#2f6fd6'). Ran here: gold #c9a227 → #1ac5d9 (target #19c3d9) while a red block stayed #b5432c. **أرقام / params:** tolerance 40–42; tint .3; Pillow only.
- **الدليل / proof:** `100-superskills/skills/pixel-studio-painter/scripts/edit_pack.py:50` · `100-superskills/skills/pixel-studio-painter/references/drawing-guide.md`

#### COLOR-30 · ألوان الشعار الحقيقية · Logo true colours + antialias-blend detection · 📦 بأمر تثبيت / one install
- **ماذا / what:** يستخرج ألوان الشعار الفعلية كمتوسطات للبكسلات النقية، ويتعرف على بكسلات التنعيم عند الحواف فلا يحسبها ألوانًا جديدة. — Finds a logo's true colours as means of pure pixels and recognises antialias edge blends so they are not mistaken for palette colours.
- **متى أستخدمها / when:** تحريك شعار عميل بألوانه الدقيقة أو تحويله لفيكتور. — animating a client logo in exact colours or vectorising it.
- **كيف / how:** vectorize._palette(rgba, max_colors=16, min_share=.001): quantise /8 to rank, keep candidates ≥30 apart, average everything within 22. _edge_blends tests 4 neighbour directions (neighbour contrast > 40, t in 0.08–0.92, distance < 18); _mixture least-squares 2–3 colour weights 6–94% within tol 16. vectorize.py imports OpenCV, which is not installed here. **أرقام / params:** max 16 colours; ≥30 apart; blend tol 16.
- **التثبيت / install:** `pip install opencv-python-headless`
- **الدليل / proof:** `kosif-studio/vectorize.py:45` · `kosif-studio/vectorize.py:24` · `kosif-studio/scenes/aghnam_logo.json`

## اللوحات والهويات وأنظمة الرموز — Palettes, identities & token systems

_لوحات المالك المختبرة، وهويات KOSIF، ومكتبات جاهزة، وتوليد هوية كاملة من لون واحد._

#### COLOR-31 · هوية كاملة من لون واحد · One hex → full WCAG token set (+ 9 accent presets) · ✅ مُثبت هنا / proven here
- **ماذا / what:** تعطي لونًا واحدًا فتحصل على ثيم فاتح وداكن وألوان حالات ومسافات وأحجام خط وتوقيتات حركة — كل زوج يمر اختبار التباين — مع كتلة CSS جاهزة. — Give one colour and get light + dark themes, status colours, spacing, type scale and motion tokens — every pair contrast-checked — plus a ready CSS block.
- **متى أستخدمها / when:** عميل بلا هوية أو بلون شعار فقط؛ أول خطوة قبل أي مشهد. — a client with only a logo colour; the first step before any scene.
- **كيف / how:** `echo '{"brand":"#8a5a2b","name":"k"}' | python3 design_tokens.py` (also MCP kosif_design_tokens): lightness is walked until text pairs reach 4.6:1 and UI pairs 3:1; CSS has :root, prefers-color-scheme dark guarded by :not([data-theme=light]), [data-theme=dark] and reduced-motion 0 ms. Ran here: #8a5a2b → dark brand #d4985e, light ink #221911 on #faf9f7 = 16.42:1, all 22 checked pairs pass. Runtime twin in EARTH: accentTokens(hex, dark, surface) mixes toward black (light) until 3:1 or toward white (dark) until 4:1 in steps of .08 (max .9), on-brand white if ≥3.2 else #06101f, brand-2 = 32% white mix, deep = 55% toward #0b1f3a, soft = 11% (22% dark), gradient 135° b2 0% / c 55% / deep 100%. Nine accent presets feed it: كوبالت #2340c4, زمردي #0f9d6c, أخضر وطني #006c35, فيروزي #0e8a9a, ملكي #6b4ee6, عنبري #c2410c, ذهبي #b8862b, قرمزي #d0343f, فحمي #3b4a5e. **أرقام / params:** text 4.6:1, UI 3:1; status hues ok 140° warn 35° bad 4° info 200° (s .65); space 4–64 px; type ratio 1.25; t-fast 120 ms, t 180 ms; ease cubic-bezier(.2,.8,.2,1).

```bash
echo '{"brand":"#8a5a2b","name":"k"}' \
  | python3 kosif-one/tools/kosif-omni/skills/kosif-web-design/scripts/design_tokens.py > tokens.json
# tokens.json → .tokens.light / .tokens.dark / .contrast[] / .css  (paste .css into the composition)
```

- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-web-design/scripts/design_tokens.py:62` · `kosif-earth-ci-fork/ui/layouts/shell.js:76` · `kosif-earth-ci-fork/ui/layouts/shell.js:69` · `kosif-atlas/skills/196-landing/621-landing/scripts/brand_palette_validator.py`

#### COLOR-32 · هوية «دفتر KOSIF» · Dafter KOSIF ledger identity (default, light + night) · ✅ مُثبت هنا / proven here
- **ماذا / what:** الهوية الافتراضية: ورق دفاتر كريمي، بطاقات بيضاء دافئة، حبر فحمي للعناوين والأزرار، ولون زعفران واحد للعلامات والحالة النشطة — ونسخة ليلية. — The default identity: cream ledger paper, warm white cards, charcoal ink for rails/headings/buttons and a single saffron accent — with a night twin.
- **متى أستخدمها / when:** أي فيلم لـKOSIF نفسها أو عميل يريد دفئًا مهنيًا عربيًا. — KOSIF's own films or clients wanting warm Arabic professionalism.
- **كيف / how:** html[data-look=kosif][data-brand=ledger] (+ [data-theme=dark]); map bg/ink/accent to scene background, type and highlight. Saffron text uses the darker step #a53e07 (5.9:1); ink #1d1814 is 17:1. identity_unity.test.mjs ran here (5/5 pass). **أرقام / params:** light: bg #fbf8f3 surface #fffdf9 line #e3d9cc ink #1d1814 ink-2 #4b4139 saffron #d9530e text #a53e07 soft #fbe9dc ok #2c7a4b warn #a76a10 bad #b3261e info #2f5f8f; night: bg #161310 surface #1c1814 ink #f5ede3 brand #f2732d gold-ink #ff9a5f grad 135° #ff9a5f→#f2732d 45%→#a53e07.
- **الدليل / proof:** `kosif-earth-ci-fork/ui/ds/tokens.css:263` · `kosif-earth-ci-fork/ui/ds/tokens.css:284` · `kosif-earth-ci-fork/docs/design/SQC-IDENTITY-ar.md` · `kosif-earth-ci-fork/tools/identity_unity.test.mjs`

#### COLOR-33 · مظاهر KOSIF EARTH · KOSIF EARTH identity looks (14) · 🟢 جاهز / ready
- **ماذا / what:** أربعة عشر مظهرًا مختبرًا في واجهة المالك، منها عربية الروح (تراث الوادي، نجد الفاخر، الواحة، الدفتر المسطر) — كلها رموز CSS تنقلها مباشرة إلى مشهد. — Fourteen identity looks from the owner's app, several with Arabic character (Heritage Valley, Najd luxe, Oasis, Notebook) — CSS tokens you lift straight into a scene.
- **متى أستخدمها / when:** تحتاج لوحة كاملة مجربة بنسخة فاتحة وداكنة في دقيقة. — a complete light/dark palette in a minute.
- **كيف / how:** Select with [data-look=…] / [data-brand=…] (+ [data-theme=dark]); copy --sk-* values into :root of the composition. Cobalt & Ice is covered by identity_unity.test.mjs (ran here); the rest are owner CSS. Earth-office door forbids a full-image green tint or hue-rotate; intro amber is a title-card palette over space footage. **أرقام / params:** see table.

| look | light (bg · ink · brand · accent) | night / notes |
|---|---|---|
| Cobalt & Ice | #f4f6fb · #111827 · cobalt #2340c4 (8.1:1) · ice #19c3d9 (text #076f80) | #070a1e · brand #3fd3e6 · #9fb0ff |
| Navy & Gold (luxe) | ivory #f7f4ec · navy #0b1f3a · button #13305a · gold #c9a227 (text #8a6a0e) | #0a1424 · gold #d4af37 · #8fb3e8 |
| تراث الوادي Heritage Valley | parchment #f4ead8 · #2b1a0f · #8a5a2b · #b8864e | #16110c · #d09a5e — Amiri / Aref Ruqaa |
| نجد الفاخر Najd luxe | #f7faf7 · #11281a · green #006c35 · gold #d4af37 | #09150e · #2ecc71 · #f1c40f — Aref Ruqaa |
| الواحة Oasis | sand #f6f1e7 · #23261f · sage #3b6a4e · terracotta #c2703d | #141915 · #86b896 · #e59a63 — Readex Pro |
| الدفتر Notebook | #f7f3e8 · #23252b · ink blue #2c5aa0 · margin red #c0392b | Aref Ruqaa headings |
| Executive | #f5f6fb · #1d2340 · #5b4ee6 · #3d7bf5 | radius 14/20 |
| Professional Audit | #f3f4f6 · #161b26 · #1f3b68 · #2f5d9e | radius 4/6/8 |
| Midnight analysis | #0d1117 · #e8edf5 · #7c8cff · #4fd1c5 | dark only |
| الشفق Aurora glass | #eef2f9 · brand #0a66ff · #7b61ff · grad #7b61ff→#0a66ff→#00b3ff | #0a0c13 · #5b95ff |
| النابض Vivid | #f8fafc · #1e293b · #6366f1 · #06b6d4 · grad →#8b5cf6→#ec4899 | #0f1124 · Tajawal |
| Graphite | #0e0f12 · #eceef2 · #8183ff · mint #5ee0c4 | radius 6/9/12 |
| العقيق Onyx | #0b0b0c · #f4efe4 · gold #d4af5a · #b8893a | Noto Naskh display |
| Earth office door / intro amber | forest #176b4b · mint #b9f3cd | veil rgba(4,9,17,.78) · amber #e8bd76 · CTA #f9f1e8 |

- **الدليل / proof:** `kosif-earth-ci-fork/ui/ds/tokens.css:162` · `kosif-earth-ci-fork/ui/ds/tokens.css:378` · `kosif-earth-ci-fork/ui/ds/tokens.css:7` · `kosif-earth-ci-fork/ui/art/brand/earth-office-door.css`

#### COLOR-34 · إعادة تلوين حسب الدور · Role-based palette remap (brandCSS) · ✅ مُثبت هنا / proven here
- **ماذا / what:** يعيد كتابة أوراق أنماط مصممة بالكوبالت إلى هوية الدفتر حسب الدور: النص زعفران مقروء، الخلفيات المعبأة حبر، والخطوط زعفران — مع الحفاظ على الشفافية. — Rewrites cobalt-authored stylesheets into the ledger identity by role: text → readable saffron, filled backgrounds → ink, strokes → saffron, alpha suffixes kept.
- **متى أستخدمها / when:** تحويل قالب أو رسم بياني جاهز إلى هوية عميل دون إعادة رسمه. — re-branding a ready template or chart without redrawing it.
- **كيف / how:** brandCSS(css): three role regexes for #2340c4 (color: → #a53e07, background: → #1d1814, else → #d9530e), then a 44-pair hex table and an rgba() triplet table (e.g. #0b1030→#1d1814, #19c3d9→#f2732d, #f4f6fb→#fbf8f3, rgba(35,64,196,…)→rgba(217,83,14,…)). Used for print, letterhead, charts print CSS and presentations. identity_unity.test.mjs ran here (5/5). **أرقام / params:** 3 role rules + 44 hex pairs + rgba table.
- **الدليل / proof:** `kosif-earth-ci-fork/ui/core/sk.js:348` · `kosif-earth-ci-fork/tools/identity_unity.test.mjs`

#### COLOR-35 · تحويل انتقائي ذهبي→جليدي · Selective gold→ice hue rotation (image and video) · ✅ مُثبت هنا / proven here
- **ماذا / what:** يدير نطاق الذهبي فقط إلى سماوي جليدي بأوزان ناعمة، ويقرّب الكحلي نحو الكوبالت، ويترك الخشب والبشرة والأحمر كما هي — للصور وللفيديو إطارًا بإطار. — Rotates only the gold hue band to ice cyan with smooth weights, nudges navy to cobalt and leaves wood, skin and reds untouched — stills or MP4 frame by frame.
- **متى أستخدمها / when:** أصل مولّد أو صورة بهوية قديمة تحتاج لون الهوية الجديدة. — a generated asset or old-brand image that needs the new brand hue.
- **كيف / how:** `python3 tools/brand/recolor_ice.py IN OUT` (webp/png/jpg or mp4). NumPy HSV: w = smooth(h,18,30)·(1−smooth(h,62,74))·smooth(s,.08,.22); target hue 190+(h−45)·.35; blue band 196–248 pulled half-way to 228; s·(1−.1w), v·(1−.06w). Video: rawvideo rgb24 pipe → libx264 -preset slow -crf 24 yuv420p +faststart (audio dropped — re-mux the original audio). Ran here: #c9a227 → #34a6bd, red #b5432c unchanged, navy #0b1f3a → #0b1a3a. **أرقام / params:** gold ~22–68° → ice ~185–195°; crf 24; webp q82.
- **الدليل / proof:** `kosif-earth-ci-fork/tools/brand/recolor_ice.py` · `kosif-earth-ci-fork/docs/design/HIGGSFIELD_VISUALS_ar.md`

#### COLOR-36 · باليتات الشيدر كمتغيرات · Shader palettes as uniforms (Crystal World) · ✅ مُثبت هنا / proven here
- **ماذا / what:** عالم بلوري ثلاثي الأبعاد بلوحتين (كوبالت وجليد / حبر وزعفران كهرماني) تُمرَّر كمتغيرات، ولا لون مثبت داخل الشيدر — والاختبار يفرض ذلك. — A crystal-world shader with two palettes (cobalt ice / ledger amber) passed as uniforms; no colour is hard-coded in the shader and a test enforces it.
- **متى أستخدمها / when:** مشهد شيدر يجب أن يتبع هوية العميل. — any shader scene that must follow a client identity.
- **كيف / how:** PALETTES.cobalt / PALETTES.ledger chosen from data-brand or an explicit option. cobalt iceA (.043,.063,.19) iceB (.10,.76,.85) skyB (.86,.95,1) rim (.60,.93,.97); ledger iceA (.114,.094,.078) iceB (.85,.33,.055) skyB (.98,.95,.90) rim (.98,.76,.55) snow (1,.9,.78). identity_unity.test.mjs ran here (5/5). **أرقام / params:** 2 palettes × iceA/iceB/skyB/rim/snow uniforms.
- **الدليل / proof:** `kosif-earth-ci-fork/ui/art/crystal-world.js:102` · `kosif-earth-ci-fork/tools/identity_unity.test.mjs`

#### COLOR-37 · باليتات منتجات التدقيق · KOSIF audit palettes + cascade-order theming · ✅ مُثبت هنا / proven here
- **ماذا / what:** لوحات «ريش الطيور» الفاتحة والداكنة، ولوحة القيادة النيلية، والثيم التحريري البنفسجي الذهبي الكريمي، ولوحات التراث والليل — مقفلة باختبارات، وطبقات ثيم تُرتب بالتحميل. — Feather light/dark, the indigo dashboard, the purple-gold-cream editorial theme, heritage and night palettes — locked by tests, themes layered by cascade order.
- **متى أستخدمها / when:** مشاهد واجهات مالية/تدقيق أو فيلم إطلاق لمنتجات KOSIF. — finance/audit UI scenes or KOSIF product launch films.
- **كيف / how:** Copy the :root block; switch html[data-theme=dark]; status hues: primary violet focus, teal done, amber attention, coral risk. Cascade: continuous-review.css → dashboard-theme.css → product-model.css → kosif-one-editorial-theme.css; the test asserts that order and that meta theme-color (#24113f) is a colour the final theme paints. palette.test.mjs (5/5) and dashboard-theme.test.js (5/5) ran here. **أرقام / params:** see table.

| palette | key hex |
|---|---|
| Feather light | bg #f7f7fb · fg #22183f · primary #5b2acb · teal #087f86 · amber #ad6700 · coral #c93343 · aubergine #2f1b68 |
| Feather dark | bg #12101a · fg #f4f1fb · primary #9a7cff · teal #5cc3c5 · amber #f0b652 · coral #ff7b86 |
| V5 dashboard | bg #f8fafc · text #1e293b · brand #6366f1→#a855f7 · hero #6366f1→#8b5cf6 55%→#ec4899 |
| KOSIF One editorial | purple #24113f · #4b2377 · gold #c8a35d · cream #fbfaf6 · heritage green #216753 · hero 125° #24113f→#43206b→#6d3a87 |
| Heritage AI | paper #f6efe3 · purple #241332 · gold #c59a3b · AI core radial #c59a3b→#241332 + glow 45px #c59a3b66 |
| Studio 4 mint on plum | sidebar #211830 · primary #6544a7 · accent #216753 · mint #dbf6cd |
| Continuous review / research lab | #100c16 · #8b5cf6 · mint #5eead4 / #100b18 · lilac #b691ff · good #8de4b4 |
| Deep-space cinema | #050914 · glass rgba(15,23,42,.78) blur 18px radius 24px |

- **الدليل / proof:** `kosif-audit-pro/app/globals.css:21` · `kosif-audit-pro/tests/palette.test.mjs` · `kosif-audit-studio/kosif-one-editorial-theme.css` · `kosif-audit-studio/tests/dashboard-theme.test.js`

#### COLOR-38 · ثيمات Kinetic Flow السبعة عشر · Kinetic-flow locked themes A–Q + custom R · ✅ مُثبت هنا / proven here
- **ماذا / what:** سبعة عشر ثيمًا مقفلًا لفيديوهات التايبوغرافي الحركي: خلفية ولون بطل ولون صغير وخط وخامة وانتقال ونهاية — تُكرر حرفيًا في كل برومبت مقطع، مع ثيم R مخصص يتحقق من الـhex. — Seventeen locked kinetic-type themes (background, hero, small colour, font, finish, transition, end card) repeated verbatim in every clip prompt, plus a custom theme R with hex validation.
- **متى أستخدمها / when:** سلسلة مقاطع مولدة أو متحركة يجب أن تبدو كفيلم واحد. — a series of generated or animated clips that must read as one film.
- **كيف / how:** kinetic-flow setup {"theme":"A"} → STYLE LOCK paragraph repeated in every clip; R requires background, accent (^#[0-9a-f]{6}$), font, finish, overlay, animation, transition (small defaults #333333, end card 'fade to black'); S copies a reference (COLOR-56). production-profiles.test.mjs ran here (10/10). **أرقام / params:** 17 themes; 7 required keys for R.

| theme | bg · hero · small | theme | bg · hero · small |
|---|---|---|---|
| A Cream Minimal Luxe | #ECEAE3 · #3A3A3A · #8A8A8A | J Brutalist Acid | #BDBDB8 · #C6FF00 · #0A0A0A |
| B Lavender Editorial | #E6D8F6 · #6A1BD1 · #6A1BD1 | K Retro 70s Warm | #F3E3C3 · #E8732C · #5A3A22 |
| C Monochrome Agency | #F4F3EF · #111111 · #2B2B2B | L Cinematic Dark Doc | #141414 · #E0A100 · #BDBDBD |
| D Midnight Neon | #0B0D17 · #00E5FF · #DDE6F0 | M Blueprint Technical | #0F3B6E · #FFFFFF · #A9C8EE |
| E Gold Noir Luxury | #0A0A0A · #C9A24B · #EDE6D6 | N Paper Craft Cutout | #F2EBDD · #D94032 · #1A1A1A |
| F Swiss Bold Red | #FFFFFF · #E30613 · #000000 | O Aurora Glass | #0E0E1A · #FFFFFF · #C9CBE0 |
| G Candy Clay Pop | #FFE8DC · #2D2A4A · #2D2A4A | P Sports Energy | #0B0B0B · #FFD400 · #FFFFFF |
| H Sage Organic | #DDE3D3 · #2F4A3A · #2F4A3A | Q Y2K Chrome Iridescent | #E9ECF2 · #141414 · #5A5F6E |
| I Corporate Blue Trust | #F7F9FC · #0B2A5B · #4A5A78 | R Custom | your validated hex |

- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/kinetic-flow.mjs:4` · `fastify-motion-bro/scripts/profiles/kinetic-flow.mjs:24-30,44-54` · `fastify-motion-bro/tests/production-profiles.test.mjs:67-74`

#### COLOR-39 · باليتات الافتتاحي الفيروسي · Viral-editorial palettes 1–3 + 80/20 rule · ✅ مُثبت هنا / proven here
- **ماذا / what:** ثلاث لوحات للمحرك التحريري: توقيع تحريري (أوف وايت + بنفسجي)، تقني داكن (رمادي أردوازي + فيروزي)، أكاديمي عالي التباين (كريمي + طوبي) — وكل تسلسل 80% محايد و20% لون واحد. — Three palettes for the editorial renderer — Signature Editorial, Dark Technical, High-Contrast Academic — and each sequence is ~80% neutral, ~20% one accent.
- **متى أستخدمها / when:** فيديوهات شرح «فيروسية» بشبكة وأشكال تحريرية. — viral editorial explainers with grid and shapes.
- **كيف / how:** PALETTES['1'|'2'|'3'] → compileStoryboard.palette → editorial renderer. viral-editorial.test.mjs (7/7) and production-profiles.test.mjs (10/10) ran here. **أرقام / params:** 1: bg #F4F1EC grid #D7D4D0 accent #6134B9 text #24212A line #D5CFD9 shape #E6DFF5; 2: #1B252C / #36414A / #24DAD1 / #EFF8F7 / #364B50 / #24373B; 3: #F1E9DD / #D8CAB8 / #BC5935 / #2C2928 / #DFCEBD / #E9D1C0; 80/20.
- **الدليل / proof:** `fastify-motion-bro/scripts/viral-editorial.mjs:6` · `fastify-motion-bro/docs/VIRAL-EDITORIAL-DNA.md:19` · `fastify-motion-bro/tests/viral-editorial.test.mjs`

#### COLOR-40 · باليتات أفلام المالك · Owner film palettes from shipped projects · 🟢 جاهز / ready
- **ماذا / what:** لوحات خرجت من أفلام ومشاريع حقيقية — كحلي وذهبي، عاجي وحبر وذهبي، نيون مختبري، مدينة ممطرة، بحر ليلي، نقطة حمراء — جاهزة للنسخ. — Palettes lifted from real shipped films and projects — navy/gold, ivory/ink/gold, lab neon, rainy neon city, night sea, red dot — ready to copy.
- **متى أستخدمها / when:** تحتاج لوحة «مجربة على الشاشة» بدل اختراع جديدة. — you want a screen-proven palette instead of inventing one.
- **كيف / how:** Copy the :root tokens or the hex roles; keep one carrier/accent per palette (COLOR-54). midnight_cat and duck-vs-dragon are tested-code; the rest are owner code. **أرقام / params:** see table.

| palette | hex roles | source |
|---|---|---|
| Navy & gold (5 s brand) | bg #1b2a49→#0b1626 · carrier #E7B65A · sparkle #ffe9b8 · flood #E7B65A→#c9953f→#a9772a | five_sec |
| Ivory, ink & gold (premium reel) | ivory #F5F0E6 · ink #121417 · accent #E7B65A · accent2 #F3D9A4 · scrim rgba(10,11,13,.74) | premium_edit |
| Lab HUD neon | mint #9dffb4 · lime #d0ff6a · ink #eaffed · warn #ffda77 · fail #ff907a · bg #040b0c | bunny_twin |
| Rainy neon city | sky #030915→#11293a→#3d4561 · cyan #28eee5 · rose #ff4566 · lamp #ffe3a4 · warm hero #ffbb66 | midnight_cat ✅ |
| Night sea | moon 4100 K vs lantern 1900 K #ff9a3c · fog #0d1626 · sea #061525 · title #f3ead8 | night_boat |
| Showreel red dot | bg #0f1211 · ink #f2f1ec · red #e4342f · secondary #9aa29d | showreel |
| Dusk lava | sky #070d18→#16233b→#3b2238→#7c2d12→#c2410c · lava #fde047→#f97316→#991b1b | duck-vs-dragon ✅ |
| Flat science | sky #BFE6FF · sea #2B86E0 · sun #FFC233 · text #0B2545 · accent #FF7A00 (current stage only) | water-cycle |
| Amber-sky on zinc | #09090b · #fafafa · amber #f59e0b · sky #38bdf8 · red #ef4444 | kinetic_2d |
| Midnight / sky / rose / gold (3D) | #030712 · key #38bdf8 · rim #f43f5e · accent #fbbf24 | cinematic_3d |
| Lime & turquoise on navy | #0c1728/#132337→#090d1d · #9fece2 · #d5f375 · violet #e995ff | fastify native |
| Workbench pastel accents | mint #a7e8d0 · lavender #d3c0fa · apricot #f5ce91 on #11171b (cycled per scene) | wbcompat |

- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/five_sec/index.html:23` · `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/assets/scene.js:14` · `kosif-one/projects/duck-vs-dragon/duck_dragon.py:13-56` · `fastify-motion-bro/web/motion.js:9-21`

#### COLOR-41 · باليتات القوالب وخاناتها · Starter palettes and palette slots · ✅ مُثبت هنا / proven here
- **ماذا / what:** قالب Canvas المختبر يبدأ بلوحة «كحلي وتركوازي» وخلفية شعاعية وشبكة 90 بكسل؛ وSTYLE.md فيه خانات الألوان؛ وقالب Remotion يأخذ لون التمييز كخاصية. — The tested canvas starter opens on 'midnight teal' with a radial backdrop and a 90 px grid; STYLE.md carries the colour slots; the Remotion starter takes the accent as a prop.
- **متى أستخدمها / when:** بداية كل مشروع من `kosif.py scaffold` قبل تبديل الألوان بلوحة العميل. — the start of every scaffolded project, before swapping in the client palette.
- **كيف / how:** html-canvas: --bg #0b1020 --ink #f3f7ff --muted #9fb0cc --accent #7ee8d2 --accent-2 #ffb86b; stage radial-gradient(#182446 → #0b1020 55%); grid rgba(255,255,255,.045) every 90 px at opacity .6. templates/STYLE.md §4.1 defaults (marked estimated): bg #0B0F19 fg #F5F7FA accent #FFB020 muted #8A93A6 line #2A3346. Remotion: ink #0b0d12, paper #f4f1ea, accent prop (default #ff7a1a, example #19c37d) + withAlpha(color, a) (appends hex byte or uses color-mix) — Remotion needs `npm i` in starters/remotion and is under the Remotion company license. **أرقام / params:** midnight teal; grid 90 px @ .045; STYLE.md 5 tokens; accent prop.
- **الدليل / proof:** `kosif-tool/starters/html-canvas/index.html:9` · `kosif-tool/templates/STYLE.md` · `kosif-tool/starters/remotion/src/Film.tsx:49` · `kosif-tool/starters/remotion/props.example.json`

#### COLOR-42 · ثيمات HyperFrames وعقد الرموز · HyperFrames themes + 18-token contract · 🟢 جاهز / ready
- **ماذا / what:** ملف ثيم واحد يعيد تلوين كل المكونات لأنها تقرأ 18 متغير CSS نفسها (لوحة، خط، شكل، حركة) — وثلاثة ثيمات جاهزة: محايد، جريء، تحريري. — One theme file restyles every component because all read the same 18 CSS custom properties (palette, type, shape, motion); three ready themes: neutral, bold, editorial.
- **متى أستخدمها / when:** قوالب HTML متعددة يجب أن تتبدل هويتها بملف واحد. — many HTML components whose identity must switch with one file.
- **كيف / how:** One :root defines --bg --fg --muted --surface --border --brand --accent --accent-2 --font-display --font-body --font-mono --radius --space-1..3 --dur-beat --ease-standard --ease-emphasis; primitives use var(--fg, #f8fafc) and never declare tokens in :root. Link themes/*.css before compositions (plain CSS, nothing to install). **أرقام / params:** neutral: #f3f4f6 / #111318 / brand #1d4ed8 / #0284c7 / #60a5fa, Inter, beat .4 s; bold: #080611 / #fff8ff / #ff3d81 / #7c5cff / #00d4ff, Impact, beat .32 s, overshoot cubic-bezier(.34,1.56,.64,1); editorial: #e9e1d2 / #202725 / #246b63 / #31776f / #8a6549, Georgia, beat .48 s.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/themes/CONTRACT.md` · `kosif-one/vendor/hyperframes/themes/neutral.css` · `kosif-one/vendor/hyperframes/themes/bold.css` · `kosif-one/vendor/hyperframes/themes/editorial.css`

#### COLOR-43 · مكتبات باليتات جاهزة · Ready palette libraries (families, deck presets, recut themes, demo kit, dark ladders) · 📄 موصوف / documented only
- **ماذا / what:** مئات الألوان مرتبة حسب الغرض: 9 عائلات × 8 صفوف، و12 ستايل عروض بخطوطها، و6 ثيمات بطاقات، وطقم ديمو داكن دلالي، وسلالم خلفيات داكنة. — Hundreds of colours sorted by purpose: 9 families × 8 rows, 12 deck presets with fonts, 6 recut card themes, a semantic dark demo kit and dark-ground ladders.
- **متى أستخدمها / when:** بداية سريعة حين لا يعطيك العميل أي لون. — a fast start when the client gives no colour.
- **كيف / how:** Pick ONE row and declare one bg, one fg, one accent before writing HTML; never mix rows. Demo kit timing: entrances 0.5–0.8 s cubic-bezier(0.16,1,0.3,1), gaps 0.2–0.4 s, crossfade 0.3–0.5 s, hold 1–2 s. Heading text gradient #FFFFFF→#9B9B9B on dark / #000000→#666666 on light. The Arko sushi palette (#131209 / #f3eadb / #d0703a) sits in vendor code with no licence — look, don't copy. **أرقام / params:** 9×8 rows (~360 hex); 12 deck presets; 6 recut themes.

| library | first row / sample |
|---|---|
| Bold/Energetic | #FFBE0B #FB5607 #FF006E #8338EC #3A86FF |
| Clean/Corporate | #FFFCF2 #CCC5B9 #403D39 #252422 #EB5E28 |
| Dark/Premium | #000000 #14213D #FCA311 #E5E5E5 #FFFFFF |
| Jewel/Rich | #5F0F40 #9A031E #FB8B24 #E36414 #0F4C5C |
| Monochrome | #F8F9FA #DEE2E6 #ADB5BD #495057 #212529 |
| Nature/Earth | #606C38 #283618 #FEFAE0 #DDA15E #BC6C25 |
| Neon/Electric | #F72585 #B5179E #7209B7 #560BAD #3A0CA3 |
| Pastel/Soft | #CDB4DB #FFC8DD #FFAFCC #BDE0FE #A2D2FF |
| Warm/Editorial | #264653 #2A9D8F #E9C46A #F4A261 #E76F51 |
| Deck presets | Bold Signal #1a1a1a/#FF5722 · Electric Studio #0a0a0a/#4361ee · Creative Voltage #0066ff/#d4ff00 · Dark Botanical #0f0f0f/#d4a574/#e8b4b8 … (12) |
| Recut themes | classic on #FFF9E3 · noir on #1a1a1a · mint on #e8faf0 · craft on #f6efe1 · slate on #1e293b · mono |
| Demo dark kit | trust #c5d5ff · premium #7c6af5 · success #4ade80 · problem #f28b82 · energy #fbbf24 · bg #0d0e12 |
| Dark-ground ladder | #000000 #131209 #181818 #1F1F1F #272727 #313131 |

- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-creative/palettes/dark-premium.md` · `kosif-atlas/skills/880-superloopy/1944-superloopy-slides/STYLE_PRESETS.md` · `kosif-one/vendor/hyperframes/skills/talking-head-recut/SKILL.md` · `kosif-atlas/skills/166-demo-video/535-demo-video/references/scene-design-system.md`

#### COLOR-44 · اللون حسب العاطفة والقطاع والثقافة · Brand colour by emotion, sector and culture · 📄 موصوف / documented only
- **ماذا / what:** جدول يقترح لونًا أساسيًا حسب الشعور المطلوب، وأعراف القطاعات، وتنبيه لمعاني الألوان عند الجمهور العربي والخليجي والمصري. — A table proposing a primary by desired emotion, sector conventions, and a watch-list for colour meanings with Arabic, Gulf and Egyptian audiences.
- **متى أستخدمها / when:** عميل بلا هوية يسأل «أي لون يناسبني؟». — a client without a brand asks 'which colour suits me?'.
- **كيف / how:** Pick one primary, derive light/dark/alpha in HSL (lighten 15%, darken 8%, glow rgba(primary,.12)) and validate 4.5:1. Never use the same hue for primary and destructive; finance blue/green trust, health calm teal; run a competitive audit and decide fit vs break. Before locking, list what each colour means to the target audience (red, white, green, yellow differ by culture) and add text cues. **أرقام / params:** trust #1E40AF; navy #1E3A5F; energy #DC2626; warm #EA580C; growth #16A34A; teal #0D9488; premium #7C3AED; developer #4F46E5; heritage amber #D97706; neutral #374151.
- **الدليل / proof:** `kosif-atlas/skills/3454-brand-landingpage/14160-brand-landingpage/references/stitch-architecture.md` · `kosif-atlas/skills/1567-tonone/4427-form-palette` · `kosif-atlas/skills/1503-universal-design-principles/3813-color`

#### COLOR-45 · ألوان الحالات الدلالية · Semantic status colours (soft-tint chips, 5-stop ladder) · ✅ مُثبت هنا / proven here
- **ماذا / what:** كل حالة (نجاح، تحذير، خطر، معلومة) لها صبغة خفيفة خلفية ولون قوي أمامي وأيقونة، وسلّم من خمس درجات لكل لون — فالمعنى لا يحمله اللون وحده. — Each status gets a pale tint background, a strong foreground and an icon, plus a five-stop ladder per hue — meaning never rides on colour alone.
- **متى أستخدمها / when:** بطاقات حكم، شارات، مخططات قرار، مقارنات قبل/بعد. — verdict cards, badges, decision diagrams, before/after.
- **كيف / how:** Chip: 36×36 rounded tile, bg = soft token, fg = strong token, icon 18 px (violet #f0edfa/#5b2acb, teal #e4f4f3/#087f86, amber #fff1d7/#ad6700, coral #fbe8ea/#c93343) — palette.test.mjs ran here. Ladder: 50 tinted bg, 300 border/icon, 500 fill, 700 text on tint, 900 text on dark (50+700 passes AA body; 50+500 large text only). Default hues HSL success 142 (70%), warning 38 (90%), destructive 0 (75%), info 220 (90%). Diagram pairs light fill + dark stroke: start #fed7aa/#c2410c, success #a7f3d0/#047857, decision #fef3c7/#b45309, AI #ddd6fe/#6d28d9, error #fecaca/#b91c1c; inactive dashed. Seen: 2×3 dark glass verdict cards with corner glow radius 120 px α .35, stagger 80 ms. **أرقام / params:** tile 36 px icon 18 px; stops 50/300/500/700/900.
- **الدليل / proof:** `kosif-audit-pro/app/globals.css:1297` · `kosif-audit-pro/tests/palette.test.mjs` · `kosif-atlas/skills/1503-universal-design-principles/3815-color-semantic-systems` · `kosif-atlas/skills/2790-work/11181-draw-excalidraw`
- **شوهد أيضًا في / also seen in:** `style:pm-kmasiff-cc72cb` · `style:pm-parkerrex-1a54fe`

#### COLOR-46 · باليتات آمنة لعمى الألوان · Colour-blind-safe categorical palettes · 🟢 جاهز / ready
- **ماذا / what:** أوكابي-إيتو وبول تول ولوحة الفئات السبع بإضاءة متساوية — ومع كل لون شكل أو تسمية، لأن 8% من الرجال لا يميزون الأحمر من الأخضر. — Okabe-Ito, Paul Tol and a matched-lightness 7-hue set — always paired with shape or label, because ~8% of men miss red/green.
- **متى أستخدمها / when:** أي رسم بياني أو خريطة أو مخطط فيه فئات. — any chart, map or diagram with categories.
- **كيف / how:** Okabe-Ito #E69F00 #56B4E9 #009E73 #F0E442 #0072B2 #D55E00 #CC79A7 #000000 (on white use #0072B2 #D55E00 #009E73 #CC79A7 #000000 for 3:1). Tol Bright #4477AA #EE6677 #228833 #CCBB44 #66CCEE #AA3377 #BBBBBB (7); High-contrast #004488 #DDAA33 #BB5566 (3, best in greyscale); Vibrant #EE7733 #0077BB #33BBEE #EE3377 #CC3311 #009988 #BBBBBB. 7-hue: hsl(220 70% 55%) (160 60% 45%) (40 90% 55%) (310 60% 55%) (10 70% 55%) (270 50% 55%) (85 50% 45%). Never interpolate these; ≤5–7 categories; add icons, direct labels, dashes; simulate with Chrome 'Emulate vision deficiencies'. **أرقام / params:** Okabe-Ito 8 (5 on white); Tol 7/3/7/9/6; ≤7 hues.
- **الدليل / proof:** `kosif-atlas/skills/3202-quantitative-sciences/13564-scientific-visualization/assets/color_palettes.py` · `kosif-atlas/skills/3202-quantitative-sciences/13564-scientific-visualization/references/color_palettes.md` · `kosif-atlas/skills/1503-universal-design-principles/3815-color-semantic-systems` · `kosif-atlas/skills/1503-universal-design-principles/3814-color-accessibility-and-mode`

#### COLOR-47 · خرائط الألوان وتسلسل الرسم البياني · Colormap semantics and chart colour hierarchy · 📄 موصوف / documented only
- **ماذا / what:** اختر نوع الخريطة اللونية حسب معنى البيانات، ولون تمييز واحد يحمل الاستنتاج والباقي رمادي، ولكل لون معنى واحد في الفيلم كله. — Pick the colormap by what the data means; one accent carries the insight, context stays grey; each hue has exactly one meaning per film.
- **متى أستخدمها / when:** كل مشهد بيانات أو إنفوغراف. — every data or infographic scene.
- **كيف / how:** Sequential = monotonic lightness (viridis, plasma, inferno, magma, cividis); diverging only around a meaningful centre (RdBu_r, PuOr, BrBG) with a centred norm (e.g. vmin −2, centre 0, vmax 5), no-data in neutral grey; cyclic for angles/hours; ColorBrewer at its exact class count; no rainbow for ordered values. Chart hierarchy: ≤4 hues, chrome at 20–30% contrast, highlight 100% vs others 35–45%, no gradients/shadows/perspective on data. Write a role→hex ledger before animating; accent on ≤2 marks; never let red/green or blue/purple alone carry a distinction. **أرقام / params:** ≤4 hues; chrome 20–30%; others 35–45%; accent ≤2 marks.
- **الدليل / proof:** `kosif-tool/playbooks/charts.md:19-20` · `kosif-atlas/skills/3202-quantitative-sciences/13564-scientific-visualization/references/color_palettes.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10318-accessibility-and-inclusive-visualizatio/references/color-contrast-and-redundant-encoding.md` · `kosif-atlas/skills/317-data/942-data-visualization/SKILL.md`

#### COLOR-48 · التدرج الحراري بسبع محطات · Thermal 7-stop heat ramp · ✅ مُثبت هنا / proven here
- **ماذا / what:** تدرج كاميرا حرارية (بارد، عميق، أخضر، أصفر، برتقالي، أحمر، أبيض) لحقول الحرارة وخرائط الشدة، مع سقف يمنعه من الاحتراق للأبيض. — A heat-camera ramp (cold, deep, green, yellow, orange, red, white) for heat fields and intensity maps, capped so it never blows to white.
- **متى أستخدمها / when:** خرائط حرارة، طاقة، كثافة، أو أثر إصبع حراري. — heat, energy or density maps, thermal trails.
- **كيف / how:** Map heat 0–1 through seven stops blended with smoothstep at 0, .12, .30, .45, .60, .78, 1; cap heat at 0.75; background heat 0.34–0.66; keep dark→light so heat reads as brightness when you swap in a brand ramp. Full-screen fragment shader: fbm 5 octaves warp-the-warp, melt cycle 6 s, blob 0.37, flow 0.26, rim 0.6, halo 0.45; trail 24 points fading over 1.6 s. **أرقام / params:** stops 0/.12/.30/.45/.60/.78/1; cap .75.
- **الدليل / proof:** `kosif-atlas/skills/100-ui-motion/211-thermal-finger-trail/SKILL.md` · `kosif-atlas/skills/100-ui-motion/211-thermal-finger-trail/references/thermal-finger-trail.html`

#### COLOR-49 · تدرجا ماغما والجبل · Magma colormap and alpine terrain ramp · 🟢 جاهز / ready
- **ماذا / what:** تدرج ماغما مضغوط (أسود → بنفسجي → أرجواني → مرجاني → برتقالي → ذهبي باهت) للطيف الصوتي، وتدرج جبلي يلون التضاريس بالارتفاع والميل. — A compact magma ramp (black→violet→magenta→coral→orange→pale gold) for spectrograms, and an alpine ramp that colours terrain by height and slope.
- **متى أستخدمها / when:** عوالم يقودها الصوت، أو تضاريس ثلاثية الأبعاد وخرائط. — sound-driven worlds, or 3D terrain and maps.
- **كيف / how:** qa._magma(v) stops 0 (0,0,4) · .2 (40,11,84) · .4 (120,28,109) · .6 (192,58,118) · .75 (236,105,89) · .88 (251,165,74) · 1 (252,253,191). K3.alpineColour as makeTerrain colour: deep #2f4a3a (<−5 m), sand #b9a77a → grass #4e6e34 (5–25 m), grass2 #6b8a3c, rock #5d5a58/#7a6f66 (120–420 m, slope .28–.6), snow #f4f7fb above 520–700 m. **أرقام / params:** magma 7 stops; alpine 6 bands.
- **الدليل / proof:** `kosif-studio/motion/qa.py:439` · `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:135`

## نظرية اللون والإتاحة وقواعد الإخراج — Colour theory, access & direction rules

_قوانين تمنع الفوضى اللونية: تناغم، تباين مقاس، لون تمييز واحد، وقفل أسلوب السلسلة._

#### COLOR-50 · مولّد التناغم اللوني · Harmony generator 2D/3D + harmony detector · ✅ مُثبت هنا / proven here
- **ماذا / what:** يبني ألوانًا متكاملة أو متجاورة أو ثلاثية أو منقسمة أو رباعية من درجة أساس واحدة، كنصوص CSS أو ألوان three.js — ويصنّف لوحة موجودة. — Builds complementary/analogous/triadic/split/tetradic hues from one base as CSS strings or THREE.Color, and classifies an existing palette.
- **متى أستخدمها / when:** تحتاج لونًا مرافقًا لشعار العميل أو لوحة لمشهد ثلاثي الأبعاد. — a companion colour for a client logo, or a 3D scene palette.
- **كيف / how:** MOTION.palette(scheme, baseHue, {sat, light:[…]}) → {hues, css}; K3.harmony(scheme, hue, {sat .6, light .5}) → THREE.Color. Offsets: complementary 0/180, analogous −30/0/30, triadic 0/120/240, split 0/150/210, tetradic 0/60/180/240; defaults S 60% L 50%. blue_hour uses harmony('complementary', 222) → [222, 42] (blue sky vs orange lamps). Keep one family dominant, the complement only as accent. Detector: take chromatic colours (OKLCH C ≥ 0.04), test mono (±15°), analogous (±30°), complementary, split (±150°), triadic (±120°), square — tolerance ±15°; free combinations allowed but flagged. Ran here in Chromium (vendored kit/gsap.min.js + motion-kit.js): MOTION.palette('split', 210) → hues [210, 0, 60] as hsl(… 60% 50%), ('complementary', 222) → [222, 42]. **أرقام / params:** offsets as listed; tolerance ±15°; C ≥ .04.
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:113` · `kosif-studio/motion/kit/three-kit.js:1176` · `100-superskills/skills/kosif-montage-motion/scripts/projects/blue_hour/src/main.js:24` · `kosif-atlas/skills/3593-bespoke-design-system/14409-bespoke-design-system/references/color-harmony-math.md`

#### COLOR-51 · تدرجات إدراكية OKLCH وظلال بإزاحة الصبغة · Perceptual OKLCH ramps and hue-shifted shading · 📄 موصوف / documented only
- **ماذا / what:** ابنِ السلالم في OKLCH حتى تبدو الخطوات متساوية فعلًا، وحرّك الصبغة: الظلال تبرد والإضاءات تدفأ بدل التغميق فقط؛ ولا أبيض نقي ولا رمادي محايد في لوحة فنية. — Build ramps in OKLCH so steps look even, and shift hue — shadows cooler, highlights warmer — instead of just darkening; no pure white or neutral grey in a painterly palette.
- **متى أستخدمها / when:** سلالم رمادي، تدرجات مواد، رسم وإضاءة شخصيات. — grey ramps, material ramps, illustration shading.
- **كيف / how:** sRGB → linear → OKLab → OKLCH (Ottosson 2020); keep H within ±10° per family, vary L and C; Chromium renders oklch() natively in HTML/Remotion. Neutral ramp check: OKLCH L per stop, deltas d, uniformity = 1 − (max|d| − min|d|)/mean|d| ≥ 0.7. Material ramps 3–5 steps rotating hue 10–20° and raising saturation in darks. Painting family: deep blues, pale yellows, a green touch, warm ochre. **أرقام / params:** hue drift ≤10°; uniformity ≥0.7; shift 10–20°/step.
- **الدليل / proof:** `kosif-atlas/skills/3593-bespoke-design-system/14409-bespoke-design-system/references/color-harmony-math.md` · `kosif-atlas/skills/2460-pixel-art/9527-sprite` · `kosif-atlas/skills/2981-designer-skill/12625-designer-skill/reference/css-techniques.md` · `kosif-tool/styles/pm-mandelduck-95fd08/BRIEF.md`

#### COLOR-52 · حساب التباين WCAG · WCAG contrast math, role tiers and alpha flattening · ✅ مُثبت هنا / proven here
- **ماذا / what:** احسب الإضاءة النسبية ونسبة التباين لكل نص فوق خلفيته قبل الرندر، بعتبة حسب دور النص، وادمج الشفافية أولًا لأن اللوحة الزجاجية فوق الفيديو تتغير. — Compute relative luminance and contrast for every caption/background pair before render, with thresholds by role, flattening alpha first because a glass plate over video changes.
- **متى أستخدمها / when:** كل ترجمة وعنوان ولوحة سفلية، خاصة فوق فيديو أو تدرج. — every caption, title and lower third, especially over video or gradients.
- **كيف / how:** Decode sRGB (c/12.92 if c ≤ 0.04045 else ((c+0.055)/1.055)^2.4), L = 0.2126R + 0.7152G + 0.0722B, ratio = (Lmax+0.05)/(Lmin+0.05). Body 4.5:1 (AAA 7:1); large text/UI/brand/links 3:1; disabled/hover optional — only body failures block delivery. Translucent plates: out = fg·α + bg·(1−α) per channel, sampling the darkest and brightest frames under the plate. Accessibility cut: AAA pairs, solid borders, no text over gradients (@media (prefers-contrast: more)). design_tokens.py implements this and ran here (22 pairs pass). **أرقام / params:** 4.5 / 3.0 / none; AAA 7:1.

```python
def lum(hex_):
    c = [int(hex_[i:i+2], 16) / 255 for i in (1, 3, 5)]
    c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)      # ratio('#a53e07', '#fbf8f3') ≈ 6.0
```

- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-web-design/scripts/design_tokens.py:92` · `kosif-atlas/skills/3593-bespoke-design-system/14409-bespoke-design-system/references/color-harmony-math.md` · `kosif-atlas/skills/2199-lvtd-skills/8013-color-math-accessibility` · `100-superskills/skills/brand-identity-logo/SKILL.md:23`

#### COLOR-53 · الوضع الداكن بلا قلب · Dark variant without inversion · 📄 موصوف / documented only
- **ماذا / what:** لا تقلب الألوان: خلفية قريبة من الأسود بصبغة الهوية، نص أوف وايت، وألوان الهوية أقل تشبعًا وأفتح قليلًا — وتجنب الأسود والأبيض النقيين. — Don't invert: a brand-tinted near-black ground, off-white text, brand colours desaturated and lifted — and avoid pure #000/#fff.
- **متى أستخدمها / when:** نسخة ليلية لفيلم أو مشهد داكن لنفس الهوية. — a night version of a film or a dark scene in the same identity.
- **كيف / how:** bg hsl(220 10% 8%), text ~hsl(0 0% 90%); brand hsl(220 90% 50%) → hsl(220 70% 60%) (sat −20 pts, L +10 pts); darkest ~#111827 to avoid halation; use #0a0a0a and #fafaf9 instead of black/white; text tiers by opacity 100/60/40%, borders 10%. Re-run contrast in both modes. **أرقام / params:** sat −20, L +10; tiers 100/60/40/10%.
- **الدليل / proof:** `kosif-atlas/skills/1503-universal-design-principles/3814-color-accessibility-and-mode` · `kosif-atlas/skills/3438-ux-design/14124-top-design`

#### COLOR-54 · لون تمييز واحد بمعنى واحد · One accent, one meaning (~5% of the frame) · 🟢 جاهز / ready
- **ماذا / what:** لون تمييز واحد بمعنى واحد يغطي نحو 5% من البكسلات، ولحظة واحدة يملأ فيها الإطار؛ الوصول يُصبغ ثم يرتاح إلى المحايد؛ والمحايدات تميل لصبغة الهوية لا للرمادي. — One accent with one meaning on ~5% of pixels and one full-bleed beat; arrivals tint then relax to neutral; neutrals lean toward the brand hue instead of pure grey.
- **متى أستخدمها / when:** دائمًا — أول قرار لوني في أي فيلم. — always — the first colour decision of any film.
- **كيف / how:** Lock roles before animating: one primary, a ~9-stop neutral ramp, success/warning/destructive as a separate axis (≈5 roles). Sequences ~80% neutral / ~20% accent; accent marks exactly one element per composition and never a placeholder (stand-in cards, avatars and series are alpha steps of the ink). Arrival tints relax to neutral over 12–50 frames. premium_edit takes --ivory/--ink/--accent/--accent2 (#F5F0E6 / #121417 / #E7B65A / #F3D9A4). Seen as ink black #090909, bone #f4f1ea and one signal orange #f27525 used only for the active element; light canvas with one #ff4c2d for selection, cursor and impact numbers. **أرقام / params:** accent ≈5% pixels; 80/20; tint relax 12–50 f; 5 roles.
- **الدليل / proof:** `kosif-studio/motion/direct.py:288` · `kosif-studio/motion/references/craft-numbers.md` · `kosif-earth-ci-fork/docs/design/SQC-IDENTITY-ar.md` · `kosif-one/vendor/hyperframes/registry/components/CATALOG.md`
- **شوهد أيضًا في / also seen in:** `style:plotter` · `style:pm-kikelopezdesign-7cc9e8` · `style:pm-majorbaguette-fb11d7` · `style:pm-manuelogomigo-f33ca9`

#### COLOR-55 · أنظمة لونين أو ثلاثة صارمة · Strict two- and three-colour systems · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** أنت أنتجت أفلامًا بلونين أو ثلاثة فقط حيث التباين نفسه يصنع الإيقاع: حبر وورق ولون إشارة، تُقلب الأدوار بين الفصول. — You have produced films with only two or three colours where contrast itself makes the rhythm: ink, paper and one signal colour, roles swapped between chapters.
- **متى أستخدمها / when:** ريلز تايبوغرافي جريئة، إعلانات أدوات، شوريلات. — bold type reels, tool ads, showreels.
- **كيف / how:** Choose ink + paper + one signal; every element must use one of them (no tints except alpha of ink); flip ground per chapter or bar (COLOR-66/67); max 3 hues, white type on a saturated single ground for heroes; avoid multi-gradients, sparkles and purple 'AI' clichés. Build: CSS vars --ink/--paper/--signal, scenes swap which is ground. **أرقام / params:** 2–3 hues only; flip per chapter/bar.

| style | ink · paper · signal |
|---|---|
| style:pm-fionntobin-97b7af | cobalt #2a24c6 on #eeecdf (and inverse) |
| style:pm-grace-sunnyy-29bc61 | #141311 · #e7e2da · vermilion #e93e24 (ground changes every bar) |
| style:pm-leadnotifi-e83f94 | #161616 · #f0f1ec · acid lime #e4fb34 (flip every 3.5–4 s on downbeat) |
| style:plotter | #090909 · #f4f1ea · orange #f27525 |
| style:pm-majorbaguette-fb11d7 | #191816 · #f7f7f5 · lime #d6f04a (steps, checks, key phrases only) |
| style:pm-levabashidze-2d713a | #100e0c · #f2eee5 · #e8502e + electric blue #3134f0 |

- **الدليل / proof:** `style:pm-fionntobin-97b7af` · `style:pm-grace-sunnyy-29bc61` · `style:pm-leadnotifi-e83f94` · `kosif-atlas/skills/100-ui-motion/209-kinetic-inflated-hero/SKILL.md`
- **شوهد أيضًا في / also seen in:** `style:plotter` · `style:pm-majorbaguette-fb11d7` · `style:pm-levabashidze-2d713a` · `style:pm-micheleharmonic-77628e`

#### COLOR-56 · قفل الأسلوب وبصمة المرجع · Style lock and reference style-DNA (+ exact hex after generation) · ✅ مُثبت هنا / proven here
- **ماذا / what:** قفل أسلوب يُنسخ حرفيًا في كل لقطة (5 ألوان hex، إضاءة، عدسة، تلوين، حبيبات، حقبة، 3 كلمات مزاج)، ووضع S ينسخ لوك مرجع بعد فحص 5–8 لقطات فعلًا — والهوية الدقيقة تُطبق في طبقة الحركة لا تُترك لمولد الصور. — A style lock copied verbatim into every shot (5 hex, lighting, lens, grade, grain, era, 3 mood words); mode S copies a reference look only after inspecting 5–8 frames; exact brand hex is applied in the motion layer, not trusted to the generator.
- **متى أستخدمها / when:** سلسلة مشاهد مولدة، أو «سوّه مثل هذا الفيديو». — a series of generated shots, or 'make it like this video'.
- **كيف / how:** Intake 4–6 named hex (one bg = lightest, one accent). kinetic-flow theme S → REFERENCE stage demands DNA (palette hex, typography, objects, transitions, timing) → SCRIPT, label 'Reference: <name>'; never copy words, logos or people. Generators: 3–10 style references, then grade or overlay the true hex (e.g. a #8B2635 band) in HTML/SVG/Remotion — seeds do not transfer across models. production-profiles.test.mjs ran here (10/10). **أرقام / params:** 5 HEX + 3 mood words; 5–8 screenshots; 3–10 refs.
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/kinetic-flow.mjs:22,46` · `fastify-motion-bro/tests/production-profiles.test.mjs:67-74` · `kosif-one/tools/kosif-omni/skills/kosif-image-studio/references/prompt-library.md` · `kosif-atlas/skills/2306-generative-web-media/8850-brand-conditioned-generation`

## اللون في الضوء والفضاء واللمسة الأخيرة — Colour in light, atmosphere & finish

_ما يحدث للون داخل المشهد: تحويل النغمات، الضباب الجوي، الرؤية الليلية، وتشطيب الرسام._

#### COLOR-57 · تحويل النغمات ACES وAgX وNeutral · Tone-mapping choice: ACES, AgX or Neutral · 🟢 جاهز / ready
- **ماذا / what:** اختيار منحنى تحويل النغمات لكل لقطة: ACES قوي، AgX يحفظ صبغة الإضاءات الساطعة (نيون ونار)، وNeutral أمين لألوان المنتجات. — Pick the tone curve per shot: ACES punchy, AgX keeps hue in bright highlights (neon, fire), PBR Neutral faithful for products.
- **متى أستخدمها / when:** كل مشهد three.js — قبل أي تلوين بعده. — every three.js scene, before any post grade.
- **كيف / how:** K3.makeRenderer(canvas, W, H, {tone:'aces'|'agx'|'neutral', exposure}) — pixelRatio 1, PCFShadowMap, preserveDrawingBuffer. Shipped exposures: blue_hour agx 1.05, night_boat agx .95, bunny neutral .9, lab neutral 1.0, koi .62, sound_ground .7; omni cinematic template uses ACESFilmic exposure 1.25 with FogExp2(#030712, .035). Runs in Chromium with no npm install through the pre-built `kit/three-kit.bundle.js` (904 KB IIFE with three.js inside); the ES-module `three-kit.js` needs `three` resolvable. **أرقام / params:** exposure .5–1.25; agx for lamps/neon, neutral for products.
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:76` · `100-superskills/skills/kosif-montage-motion/scripts/projects/blue_hour/src/main.js:17` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/cinematic_3d.html:102` · `kosif-studio/motion/references/book-lessons.md`

#### COLOR-58 · تمريرة المظهر · Look pass: gamut mask, Purkinje night vision, split toning · 🟢 جاهز / ready
- **ماذا / what:** تمريرة بعد الرندر: قناع طيف يخفض تشبع الألوان خارج إسفين مختار فتتماسك اللوحة، ورؤية ليلية تُزرّق الظلال وتغرق الأحمر أولًا، وتقسيم لوني دافئ/بارد. — A post pass: a gamut mask that desaturates hues outside a chosen wedge, Purkinje night vision that turns darks rod-blue and sinks reds first, and warm-light / cool-shadow split toning.
- **متى أستخدمها / when:** ليل مقنع، أو لوحة مشتتة تحتاج توحيدًا. — believable night, or a scattered palette that needs unity.
- **كيف / how:** const look = K3.makeLookPass({warm, cool}); composer.addPass(look); look.userData.set({gamut:[centreHueDeg, widthDeg, strength], night:0..1, split:0..1}) before OutputPass. Gamut edge feather 25° beyond half-width; night rod weights (.05,.55,.40), tint (.72,.86,1.12) on luma .02–.35, darken 25%; split warm #ffc98a / cool #5a7fb8, luma ramp .1–.7, strength ×0.35. Shipped: blue_hour {night .55, split .45, warm #ffb36a, cool #4a6aa8}; night_boat {night .35, split .55, warm #ffa860, cool #4f6fa8}. Runs in Chromium with no npm install through the pre-built `kit/three-kit.bundle.js` (904 KB IIFE with three.js inside); the ES-module `three-kit.js` needs `three` resolvable. **أرقام / params:** gamut feather 25°; split ×.35; night darken 25%.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:1148` · `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:1164` · `100-superskills/skills/kosif-montage-motion/scripts/projects/blue_hour/src/main.js:124` · `kosif-studio/motion/kit/three-kit.js:1147`

#### COLOR-59 · المنظور الجوي · Aerial perspective: 3-channel fog, fog toward the sun, sky bounce · 🟢 جاهز / ready
- **ماذا / what:** ضباب بثلاث قنوات (الأزرق يتشتت أكثر) فيصبح البعيد أزرق وأقل تباينًا؛ والضباب يدفأ حين تنظر نحو شمس منخفضة ويبقى باردًا بعيدًا عنها — قواعد غورني في الكود. — Per-channel fog (blue scatters most) so distance turns bluer and flatter; haze warms toward a low sun and stays cool away from it — Gurney's rules in code.
- **متى أستخدمها / when:** مناظر طبيعية، جبال، مدن عند الغروب أو الساعة الزرقاء. — landscapes, ridges, cities at sunset or blue hour.
- **كيف / how:** K3.aerialPerspective({scatter:[0.62, 0.85, 1.25]}) before the first render (patches the fog chunk), scene.fog colour = horizon sky (FogExp2). Per frame K3.fogTowardSun(scene, camera, sunDir, cool, warm, amount) with weight = max(0, dot(view, sun))³ × amount; skyBounce({sky, ground}) cool from above, warm from below. blue_hour: four identical dark ridges 0x2b2420 at 0.7/1.4/2.6/4.5 km, FogExp2(0x8790b0, 0.00062), cool 0x8790b0, warm 0xc49a8a, amount .9, scatter [.55,.8,1.3]. Seen: exponential fog tinted to sky #90b5ca. Runs in Chromium with no npm install through the pre-built `kit/three-kit.bundle.js` (904 KB IIFE with three.js inside); the ES-module `three-kit.js` needs `three` resolvable. **أرقام / params:** scatter [.62,.85,1.25]; weight dot³; ridges .7/1.4/2.6/4.5 km.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:1131` · `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:1201` · `100-superskills/skills/kosif-montage-motion/scripts/projects/blue_hour/src/main.js:54` · `kosif-studio/motion/references/book-lessons.md`
- **شوهد أيضًا في / also seen in:** `style:pm-ivanfioravanti-bd9261`

#### COLOR-60 · تمريرة تلوين الشيدر · Shader grade pass driven by story or music · 🟢 جاهز / ready
- **ماذا / what:** تلوين نهائي على مستوى الشيدر: ظلال باردة وإضاءات دافئة، دفء، رفع للسواد، انحراف لوني عند الحواف، فينيت وحبيبات — والمفاتيح تتغير كل إطار مع القصة أو الموسيقى. — A shader finish: cool shadows / warm highlights, warmth, black lift, edge chromatic aberration, vignette and grain — uniforms change per frame with story or music.
- **متى أستخدمها / when:** كل فيلم ثلاثي الأبعاد يحتاج «لمسة فيلم» موحدة. — any 3D film that needs one cohesive filmic finish.
- **كيف / how:** post.grade.uniforms uWarm / uLift / uVig / uCA: shadows (0.92,0.98,1.08), highlights (1.08,1.0,0.92), warm tint (1.05,.98,.9) × uWarm .5, vignette .42 smoothstep .35–.95, CA 1.2 px at 1920 scaled by radius. Shipped: koi warm .55 lift .02; sound_ground lift .08 ('no pure black') and warm .45 + .3·bass; water_cycle warm .75→.2 over 5 s, lift .08·overcast. Egypt-2120 pass after OutputPass: CA dot(d,d)·.006, saturation mix 1.08, oval vignette .38 smoothstep(.25,.85,|d·(1.1,.82)|), grain (hash−.5)·.028 stepped at 1/30 s. Runs in Chromium with no npm install through the pre-built `kit/three-kit.bundle.js` (904 KB IIFE with three.js inside); the ES-module `three-kit.js` needs `three` resolvable. **أرقام / params:** vig .38–.42; CA .006 / 1.2 px; grain .028; lift .02–.08.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:389` · `100-superskills/skills/kosif-montage-motion/scripts/projects/sound_ground/src/main.js:69` · `100-superskills/skills/kosif-montage-motion/scripts/projects/water_cycle_3d/src/main.js:104` · `kosif-one/projects/egypt-2120-animation/index.html:436-444`

#### COLOR-61 · ألوان مصادر الضوء العملية · Named practical light colours (sodium, mercury, moon, flame) · 🟢 جاهز / ready
- **ماذا / what:** ألوان مسماة لمصادر حقيقية — صوديوم، زئبق، قمر، لهب — وحرارات متباينة (قمر 4100K مقابل فانوس 1900K) تجعل الليل مقنعًا. — Named real-source colours — sodium, mercury, moon, flame — and contrasting temperatures (4100 K moon vs 1900 K lantern) that make night believable.
- **متى أستخدمها / when:** مشاهد ليلية بمصابيح أو نار أو قمر. — night scenes with lamps, fire or moon.
- **كيف / how:** K3.lightColor('sodium'|'mercury'|'moon'|'flame') from LIGHT_SOURCES. night_boat: sky zenith (0.004,0.008,0.024), horizon (0.035,0.058,0.105), fog #0d1626, sea #061525, lantern #ff9a3c, title #f3ead8, rule #e0a35a — one ember source against navy and silver. Plan the gel with COLOR-23. Runs in Chromium with no npm install through the pre-built `kit/three-kit.bundle.js` (904 KB IIFE with three.js inside); the ES-module `three-kit.js` needs `three` resolvable. **أرقام / params:** moon 4100 K; lantern 1900 K #ff9a3c.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:106` · `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:137` · `kosif-studio/motion/references/book-lessons.md`

#### COLOR-62 · تشطيب الرسام الفيلمي · Painter filmic curve, split-tone grade and grain · ✅ مُثبت هنا / proven here
- **ماذا / what:** في مشاهد الرسم بالكود: منحنى ACES فيلمي بتعريض وتباين وتشبع ورفع، وتلوين يرفع الظلال نحو لون والإضاءات نحو آخر، وحبيبات مبذورة. — For code-painted scenes: an ACES-fitted filmic curve with exposure/contrast/saturation/lift, a shadows→colour / highlights→colour grade, and seeded grain.
- **متى أستخدمها / when:** لوحات Pillow/NumPy ومشاهد KOSIF Studio المرسومة. — Pillow/NumPy paintings and KOSIF Studio painted scenes.
- **كيف / how:** filmic(exposure, contrast, saturation, lift) with y = x(2.51x+.03)/(x(2.43x+.59)+.14) — scenes that use it set ROLLOFF = 1.0; grade(shadows, highlights, amount, contrast); grain(amount, seed). Shipped: whale (1.0, 1.14, 1.04); dragon night grade #0b0820 / #ffe9cf .45 c1.06; duck storm #0a1426 / #ffe2c4 .4 c1.08. Ran here via render.py on a gradient plate: mean abs change filmic 26.7, grade 2.1, grain 4.1 (the module imports without OpenCV; its unittest file needs OpenCV). **أرقام / params:** ACES fit; grade amount .4–.45; grain .02.
- **الدليل / proof:** `kosif-studio/render.py:769` · `kosif-studio/render.py:797` · `kosif-studio/scenes/whale_dragon.py:287` · `kosif-studio/scenes/dragon_girl.py:414`

#### COLOR-63 · انضغاط الإضاءات العالية · Highlight roll-off quantiser · ✅ مُثبت هنا / proven here
- **ماذا / what:** يحوّل اللوحة العائمة إلى 8 بت بكتف tanh فوق نقطة ركبة، فتبقى النار والتوهج غنية بدل القص — وركبة 1.0 تحفظ ألوان الشعار بدقة. — Converts the float canvas to 8-bit with a tanh shoulder above a knee so fire and glows stay rich instead of clipping; knee 1.0 keeps logo colours exact.
- **متى أستخدمها / when:** كل مشهد فيه نار أو توهج أو شمس؛ وknee 1.0 لكل شعار. — any scene with fire, glow or sun; knee 1.0 for logos.
- **كيف / how:** to_uint8(rolloff=k): x > k → k + (1−k)·tanh((x−k)/(1−k)); default 0.82, filmic scenes 1.0. Ran here: a pure white fill renders (244,244,244) at the default knee and (255,255,255) at 1.0. **أرقام / params:** knee .82 default; 1.0 exact colours.

```python
import numpy as np
def rolloff(x, k=0.82):                    # x: float image, 1.0 = white
    y = x.copy(); m = x > k
    y[m] = k + (1 - k) * np.tanh((x[m] - k) / (1 - k))
    return (np.clip(y, 0, 1) * 255 + 0.5).astype(np.uint8)
```

- **الدليل / proof:** `kosif-studio/render.py:820` · `kosif-studio/scenes/whale_dragon.py:30` · `kosif-studio/tests/test_studio.py:99`

#### COLOR-64 · التعتيم الطرفي في كل محرك · Vignette in every engine · ✅ مُثبت هنا / proven here
- **ماذا / what:** تعتيم الأطراف لتركيز العين في المركز — بنفس الروح في Canvas وthree.js وFFmpeg وCSS ومشاهد الرسام. — Edge darkening that focuses the centre — the same intent in Canvas, three.js, FFmpeg, CSS and painter scenes.
- **متى أستخدمها / when:** معظم اللقطات الإبداعية؛ خفيف 10–15% في الشرح. — most creative shots; light 10–15% in explainers.
- **كيف / how:** 2D motion-kit: MOTION.vignette(stage, {inner:55%, strength:.42, z:89}) = transparent to 55% → rgba(0,0,0,.42). Painter: vignette(strength) smoothstep from 35% of the half-diagonal, typical .45–.6 (ran here). TSL/WebGPU: v = clamp(1 − dist·1.5, 0, 1); color.rgb *= v. FFmpeg: vignette=PI/5 (Basma uses it when strength > 0.3; I used PI/4.5 in tests). CSS: radial-gradient overlay. Photo stacks 10–15% (COLOR-82). **أرقام / params:** inner 55% / .42; painter .45–.6; TSL falloff 1.5; ffmpeg PI/5.
- **الدليل / proof:** `kosif-studio/render.py:782` · `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:457` · `kosif-atlas/skills/2221-webgpu-threejs-tsl/8405-webgpu-threejs-tsl/docs/post-processing.md` · `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:457`

#### COLOR-65 · تدرجات بشفافية وأنماط دمج · Gradient paints with alpha stops and blend modes · ✅ مُثبت هنا / proven here
- **ماذا / what:** تعبئة أي شكل أو نص بتدرج خطي أو شعاعي بمحطات تحمل شفافية (#rrggbbaa)، مع تنعيم ودمج normal/add/screen/multiply. — Fill any shape or text with linear/radial gradients whose stops carry alpha (#rrggbbaa), softened by blur, with normal/add/screen/multiply blending.
- **متى أستخدمها / when:** سماوات، هالات، أرضيات، وإضاءات مرسومة. — skies, halos, grounds and painted light.
- **كيف / how:** lin((x1,y1),(x2,y2),[(0,c0),…,(1,cn)]) / rad((cx,cy), r, stops), evaluated per pixel by Ctx.paint; fill(shape, paint, alpha, blur, mode). Ran here with a #0b1020→#ffb86b plate. **أرقام / params:** stops with alpha; modes normal/add/screen/multiply.
- **الدليل / proof:** `kosif-studio/render.py:46` · `kosif-studio/render.py:346` · `kosif-one/tools/kosif-studio/render.py:397`

## اللون عبر الزمن — Colour over time

_اللون كحركة وكقصة: قلب القطبية، فصول بحقول لونية، سماء تتحول، وتلوين يحكي المعنى._

#### COLOR-66 · قلب القطبية بين الفصول · Polarity flip ink↔paper at act boundaries · ✅ مُثبت هنا / proven here
- **ماذا / what:** المسرح يبدّل الخلفية والمقدمة (حبر↔ورق) عند حدود الفصل راكبًا القطع — من الفوضى المظلمة إلى الحل المضيء، أو من الفاتح إلى «الصورة الأكبر». — The stage swaps background and foreground (ink↔paper) at an act boundary, riding a cut — dark chaos to airy solution, or light to the 'bigger picture'.
- **متى أستخدمها / when:** منعطف السرد، الإسقاط الموسيقي، أو بداية فصل جديد. — the story turn, a music drop, or a new chapter.
- **كيف / how:** MOTION.polarity(tl, stage, at, bg, fg) = one tl.to on backgroundColor + color, 0.1 s (6 f) E.smooth, only at act boundaries, never on a static frame. Ran here in Chromium with the vendored gsap: at t=0.9 s bg rgb(11,13,18), at 1.05 s mid-grey rgb(128,127,126), at 1.2 s rgb(244,241,234) with ink inverted. Observed variants: instant 0-frame switch on a drop with the hero held in place; e-ink style 2–4-frame invert flash then swap (<150 ms); #fafcf9→#0e271e over ~500 ms keeping white cards; charcoal #201f1a→cream #f6efe7 over ~300 ms at ~⅓ of the film; same hue family 90%→25% lightness for act 2. **أرقام / params:** 0.1 s E.smooth; 0–500 ms variants.
- **الرخصة / license:** motion-kit runs on GSAP — GSAP 'Standard no-charge' license (gsap.com/standard-license), not MIT.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:368` · `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:368` · `style:pm-ik-builds-b8bdcf` · `style:pm-xelandre-363f00`
- **شوهد أيضًا في / also seen in:** `style:pm-bogdandragomir-35e024` · `style:pm-elliot-garreffa-f334bc` · `style:pm-gabrielbuzziv-4ff0c6` · `style:pm-deebeeeff-50fcd0` · `style:pm-twoclipping-6dd14e` · `style:pm-micheleharmonic-77628e`

#### COLOR-67 · فصول وضربات بحقول لونية · Colour-field chapter and beat flips · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** كل فصل أو ضربة يملك خلفية مسطحة مشبعة من 3–4 ألوان للهوية، والقطع نفسه يصبح تغيير لون، ولون النص ينقلب ليبقى مقروءًا. — Each chapter or beat owns one flat saturated ground from a 3–4-colour brand set; every cut is also a colour change and text inverts to stay legible.
- **متى أستخدمها / when:** إعلانات منتجات مرحة، ريلز إيقاعية، شرح بفصول. — playful product ads, beat reels, chaptered explainers.
- **كيف / how:** Keep ink colours constant, rotate grounds; flood the next colour across the frame (~400 ms) or hard-cut on the beat (≤1 flip per bar, never tweened when the brief says instant). Owner base: MOTION.polarity for two colours; HyperFrames palette-flip primitive re-skins via 0 ms variable flips anchored to section changes (needs gsap on the page — vendored as kit/gsap.min.js). **أرقام / params:** 3–4 grounds; flood ~400 ms or 0 ms on beat; ≤1 flip/bar.

| style | grounds |
|---|---|
| style:pm-bizibeast-10f264 | blue #2481fa · coral #fc504e · yellow #ffc21a · navy #141a34 (flood ~400 ms) |
| style:pm-jhylee95-e1152f | #434ce5 · #f6f7fa · #0b0b14 · surprise lime #d4f59a (every cut) |
| style:pm-roundtablespace-d3a1be | #0f0f11 · #f1eee5 · #f04a35 · #302ff5 (per bar) |
| style:pm-1littlecoder-9fef89 | #201da8 ↔ #d7dcfc ↔ #ffffff |
| style:pm-sudeepsd-1a3485 | navy #0c3247 ↔ cream #f6f2e9, yellow #f5c400, rare red #e8392b |
| style:pm-agonaliu-466a8f | #0f142d problem / #f7f8f2 features, blue #2f4be0 across both |

```js
// hard colour-field flips on beat times (seconds), text inverts with the ground
const GROUNDS = ['#2481fa', '#fc504e', '#ffc21a', '#141a34'];
const INK = { '#ffc21a': '#141a34' };               // dark ink only on yellow
beats.forEach((t, i) => {
  const g = GROUNDS[i % GROUNDS.length];
  tl.set(stage, { backgroundColor: g }, t);           // 0 ms — a set, not a tween
  tl.set(words, { color: INK[g] || '#ffffff' }, t);
});
```

- **الدليل / proof:** `style:pm-bizibeast-10f264` · `style:pm-jhylee95-e1152f` · `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/palette-flip/scene.html` · `kosif-tool/styles/pm-reflex-cloud-72ffe5/BRIEF.md`
- **شوهد أيضًا في / also seen in:** `style:pm-roundtablespace-d3a1be` · `style:pm-1littlecoder-9fef89` · `style:pm-sudeepsd-1a3485` · `style:pm-agonaliu-466a8f` · `style:pm-levabashidze-2d713a` · `style:pm-buildfastwithai-53234e` · `style:pm-techyoutbe-945b56` · `style:pm-souravbhar871-61f424` · `style:pm-leadnotifi-e83f94`

#### COLOR-68 · ضربة لون كامل للإطار · Full-bleed accent beat / brand flash fill · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** لحظة واحدة يمتلئ فيها الإطار كله بلون الهوية أو لون صادم — للنكتة أو الوعد أو الشعار — ثم يعود المسرح. — One moment where the whole frame floods with the brand or a shock colour — for the punchline, promise or logo — then the stage returns.
- **متى أستخدمها / when:** ذروة الإعلان، كشف الاسم، أو «الحل الواضح» المضلل. — the ad's peak, the name reveal, or the misleading 'obvious fix'.
- **كيف / how:** Tween the stage background to the brand for ~0.8 s while the hero shrinks to a tile (#1ed760 → darker #18a04a), or hard-cut to a flat accent frame with tone-on-tone serif text 15% darker and hold ~0.7 s, then collapse to a centre dash; or switch to lime for one scene with a hard cut or 200 ms fade, then back to cream; or one white punchline card in a dark film, cut in/out on the beat (~1 s). This is the one full-bleed beat COLOR-54 allows. **أرقام / params:** hold .7–1 s; fade ≤200 ms; tone-on-tone −15%.
- **الدليل / proof:** `style:pm-brainextends-e19ac3` · `style:pm-marouanegazouzi-6071d5` · `style:pm-0xnfrith-5be616` · `style:pm-robvjourney-ce3e1a`
- **شوهد أيضًا في / also seen in:** `style:pm-manuelogomigo-f33ca9`

#### COLOR-69 · تحريك تدرج السماء ووقت اليوم · Sky-stop tweening: time of day and seasons · 🟢 جاهز / ready
- **ماذا / what:** لوحة الفيلم كلها تنجرف بتحريك محطات تدرج السماء: ليل → فجر → صباح، أو غروب → شفق → ليل في لقطة واحدة، أو دورة الفصول — مع إضاءة المصابيح حين يعتم. — The whole film palette drifts by tweening sky-gradient stops: night→dawn→morning, sunset→dusk→night in one take, or a season cycle — lamps switch on as it darkens.
- **متى أستخدمها / when:** أدعية الفجر، قصص يوم كامل، تقدم زمني بلا قطع. — dawn duas, day-in-a-life stories, time passing without cuts.
- **كيف / how:** GSAP on SVG stop-color: tl.to('#s0', {attr:{'stop-color':…}, duration:11, ease:'sine.inOut'}, 0) then a 13.7 s second leg; silhouette fill #1d0f2c→#3a1d3c; veil opacity .38→.22 linear; stars fade out from 2 s over 9 s. Thursday-dua stops: night #0b1033/#3b1f5e/#b9507a → dawn #2b3d86/#c4677a/#ffb066 → morning #34509a/#f2a079/#ffd890. Observed: sunset #f0bd9f/#e58c8c → dusk #9f6986 → night #292142 over ~25 s; day→night with a cool grey multiply 0→35% #6a6f86 and a 300 px lamp glow; 3D: sun elevation + exposure −2 EV over 4–6 s, fog to teal-black; season parameter 0..4 (~7 s each, 1–2 s crossfades) swapping tree fill and particle emitter. gsap is vendored as kit/gsap.min.js. **أرقام / params:** legs 11 s + 13.7 s; ~25 s single take; seasons 7 s.

```js
const stops = { night: ['#0b1033', '#3b1f5e', '#b9507a'],
                dawn:  ['#2b3d86', '#c4677a', '#ffb066'],
                morning: ['#34509a', '#f2a079', '#ffd890'] };
['#s0', '#s1', '#s2'].forEach((id, i) => {
  tl.to(id, { attr: { 'stop-color': stops.dawn[i] }, duration: 11, ease: 'sine.inOut' }, 0)
    .to(id, { attr: { 'stop-color': stops.morning[i] }, duration: 13.7, ease: 'sine.inOut' }, 11);
});
```

- **الرخصة / license:** GSAP 'Standard no-charge' license (gsap.com/standard-license), not MIT.
- **الدليل / proof:** `kosif-one/projects/thursday-dua-animation/source/index.html:142-151` · `style:pm-demitiyageekzen-7770ad` · `style:pm-itsolelehmann-e47532` · `kosif-tool/styles/pm-kamstudiolabs-0b0824/BRIEF.md`
- **شوهد أيضًا في / also seen in:** `style:pm-jake11moran-a269c4` · `style:pm-theparuchh-6e08c3` · `style:pm-anas0ra-e57aea` · `style:pm-marklaunches-3b9492` · `style:pm-x4b47x-9cc84f` · `style:doodle` · `style:fake3d`

#### COLOR-70 · التلوين كقصة · Grade change as story (drain, bloom, freeze to grey) · 🟢 جاهز / ready
- **ماذا / what:** اللون يحكي المغزى: صورة المال تنطفئ للرمادي بصبغة حمراء عند «غير سعيد»، وصورة الفرح تومض ثم تستقر دافئة مشبعة، واللحظة تزداد غنى — أو يتجمد اللون للرمادي لمدة مقطع موسيقي ثم يعود. — Colour carries the moral: the money plate drains to grey with a red cast on 'unhappy', the joy plate flashes over-bright and settles warm and saturated, the moment keeps getting richer — or colour freezes to grey for one bar and snaps back.
- **متى أستخدمها / when:** قصص عاطفية، إعلانات «قبل/بعد» في المشاعر، كسرات موسيقية. — emotional stories, feeling-based before/after, musical breaks.
- **كيف / how:** GSAP on img CSS filter: drain grayscale(.9) brightness(.7) contrast(1.15) in 0.6 s + tint rgba(80,0,0,.22); joy brightness(1.6) saturate(.6) → brightness(1) saturate(1.15) in 0.9 s; moment saturate(.9) → saturate(1.25) brightness(1.05) over 8 s; tints rgba(10,30,45,.25), rgba(20,60,110,.18), rgba(255,170,60,.08). Freeze: saturate(0) + a slight contrast drop switched in 1 frame, held one bar, snapped back on the downbeat. **أرقام / params:** drain .6 s; bloom .9 s; enrich 8 s; freeze = 1 bar.
- **الرخصة / license:** GSAP 'Standard no-charge' license when timed with GSAP.
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/index.html:52-59` · `kosif-one/projects/whatsapp-motion/projects/success/index.html:146-150` · `style:pm-samaote-5e2fc2`

#### COLOR-71 · منطق الألوان السردي · Narrative colour logic (problem → solution) · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** لون واحد لكل فصل سردي: أحمر متوهج لنقاط الألم وسماوي للعرض، وبطاقة يقلب توهجها ونصها من الأحمر للسماوي لتظهر المشكلة وهي تُحل؛ ولكل مرحلة حياة أرضيتها. — One accent per narrative act: red glow for pain points, cyan for the offer, a card whose glow and text flip red→cyan as the problem is solved; each life stage owns its ground.
- **متى أستخدمها / when:** إعلانات B2B، قصص تحول، شرح مشكلة/حل. — B2B pitches, transformation stories, problem/solution explainers.
- **كيف / how:** Ground #0a1822→#10374b radial, red #e8333f for the problem (glow + second headline line), cyan #1fb3e6 for the offer, green #2ee6a0 for proof; flip a card's glow + text over ~300 ms at the turn. Red reserved for mistakes, green for fixes (#c9463d / #1f7a4f on cream #eee8dc). Navy base, white type, orange ≤15% of the frame; red/green only in charts. **أرقام / params:** 1 accent per act; orange ≤15%.
- **الدليل / proof:** `style:pm-ceowinkz-7c776b` · `style:pm-henkvaness-0e06af` · `style:pm-loicrambo-ad6830` · `kosif-tool/styles/pm-ceowinkz-7c776b/BRIEF.md`
- **شوهد أيضًا في / also seen in:** `style:pm-ismailfahmi-557268`

#### COLOR-72 · لون لكل عنصر · Per-item hue coding at equal luminance · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** كل عنصر أو صوت أو فئة يحصل على صبغة واحدة تتكرر في شارته ونقطته وإطاره وتوهجه، بإضاءة متقاربة على خلفية ثابتة — والعين تتبع العنصر بلونه. — Each item, voice or class gets one hue reused on its pill, bullet, brackets and glow, at similar luminance on a constant ground — the eye tracks it by colour.
- **متى أستخدمها / when:** قوائم أدوات، آلات موسيقية، فئات بيانات، مقارنات. — tool lists, instruments, data classes, comparisons.
- **كيف / how:** Hues at ~70% saturation and similar lightness (check with COLOR-46/52); keep the base constant (navy); reuse the same colours in the recap list. Observed sets: items orange/blue/purple/amber/green/pink; instruments cyan glock, amber marimba, violet bass, red drums, yellow cymbals on navy; skills lime #c6f432 primary + #7b4fe8 / #ff2e88 / #3fd0e6 on #0a0815; multi-ink black #1c1c1c structure, red #c42d3f errors, blue #2b4a9b definitions, green #2f8a5b conclusions; hot #e8665a / cold #3ec7c0; one solid colour column per faction; sentiment classes teal/pink/yellow crossfaded. **أرقام / params:** ~70% saturation; equal luminance; ≤7 hues.
- **الدليل / proof:** `style:pm-gigabit-million-16b3a0` · `style:pm-kamstudiolabs-447565` · `style:pm-tak3sh8-be5012` · `style:pm-ibrahimwasim240-809370`
- **شوهد أيضًا في / also seen in:** `style:pm-mdaman010-e7226a` · `style:pm-triglyceee-bd5b08` · `style:pm-ismailfahmi-557268`

#### COLOR-73 · صبغة الإطار للحدث · Full-frame event tint and flash · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** يُصبغ الإطار كله بلون الحدث طوال مدته (تعويذة زرقاء، قرمزية، حمراء) ويقوى للحظة الاصطدام؛ وحالة الخطأ تصبغ حتى 15% عنبري. — Multiply/overlay the whole frame with the event colour for its duration (blue, crimson, red spell), flashing stronger on impact; an error state tints up to 15% amber.
- **متى أستخدمها / when:** ألعاب، أكشن، حالات خطأ أو تحذير في واجهة. — games, action, error or warning states in UI films.
- **كيف / how:** Overlay div or Canvas fillRect with mix-blend-mode multiply/overlay at 30–60% for the cast, 2–3 frames stronger on impact, then release; for UI errors cap at 15%. Keep text contrast checked (COLOR-52). **أرقام / params:** tint 30–60%; flash 2–3 frames; error ≤15%.
- **الدليل / proof:** `style:pm-0xevinho-3777d8` · `kosif-tool/styles/pm-jake11moran-a269c4/BRIEF.md`
- **شوهد أيضًا في / also seen in:** `style:pm-tstfully-0aa6b4`

#### COLOR-74 · حلقات بتدرج الصبغة ودوران اللون · Hue-indexed rings and slow hue rotation · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** صبغة كل حلقة تُشتق من ترتيبها (وردي في الداخل حتى فيروزي في الخارج)، والعداد يأخذ لون الحلقة الداخلية؛ أو خلفية تدور صبغتها 360° كل 10 ثوانٍ بدل القطع. — Each ring's hue comes from its index (pink inside to teal outside) and the counter takes the innermost hue; or a background that rotates 360° per 10 s instead of cutting.
- **متى أستخدمها / when:** عدادات، مؤقتات، بصريات موسيقية، شاشات انتظار. — counters, timers, music visuals, holding screens.
- **كيف / how:** hue = 330° → 185° across ring index, HSL L ~65% S ~80% on near-black; or step 30° per ring around the wheel. Rotation: CSS filter hue-rotate or a shader uniform 360°/10 s while keeping text ≥4.5:1 (check at the worst hue). **أرقام / params:** 330°→185°; L 65% S 80%; 360°/10 s.
- **الدليل / proof:** `style:pm-kantamk-61f410` · `kosif-tool/styles/pm-kantamk-61f410/BRIEF.md` · `kosif-tool/styles/pm-monokern-ade5b6/BRIEF.md`
- **شوهد أيضًا في / also seen in:** `style:pm-monokern-ade5b6`

#### COLOR-75 · عنوان بلونين وكلمة مميزة · Two-tone headline and accent word · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** أول العبارة بلون والنكتة بلون الهوية، أو كلمة واحدة لكل ضربة تأخذ تعبئة ليمونية وخطًا سميكًا تحتها — واللون نفسه لكل الأزرار التفاعلية. — First phrase in one colour, punchline in the brand colour, or one word per beat gets a lime fill and thick underline — the same colour reused on interactive pills.
- **متى أستخدمها / when:** عناوين ريلز، إعلانات، شرائح شرح. — reel headlines, ads, explainer cards.
- **كيف / how:** Cream #f3f0e4 + lime #d8f24a on navy #07131f; black heavy grotesk #111 with the last 1–2 words in brand orange #ef5a0c and an orange dot bullet on the kicker; strict black/white + lime #c5fc34 for the beat word, magenta #ff2bd6 only for bars and bullets. For Arabic apply the colour to whole words (see ARAB powers). **أرقام / params:** 1 accent word per beat; underline thick.
- **الدليل / proof:** `style:pm-deifosv-04e4d3` · `style:pm-paulo-kombucha-96431c` · `style:pm-techhalla-7acbc2`

#### COLOR-76 · شريط عينات الألوان · Swatch-strip reveal · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** صف من ستة مربعات ألوان بأسماء hex تحتها يظهر من اليسار لليمين كدليل «كتاب الأسلوب». — A row of six colour squares with hex labels pops in left to right as a 'style book' proof.
- **متى أستخدمها / when:** فيديوهات هوية، عروض تصميم، كواليس. — identity films, design showcases, behind the scenes.
- **كيف / how:** 40 px squares, mono hex labels 8 px under each, stagger 50 ms, scale 0→1 with a small overshoot; feed it the palette from COLOR-24 or COLOR-31 (RTL layouts reverse the order). **أرقام / params:** 40 px; mono 8 px; stagger 50 ms.
- **الدليل / proof:** `style:pm-kyonax-on-tech-aabc1d`

#### COLOR-77 · باليت مفهرسة من 16 لونًا · Indexed 16-colour palette with alternating accent flash · 💡 فكرة / idea
- **ماذا / what:** فكرة: سقف 16 لونًا للفيلم كله، ولونا تمييز يتبادلان على الإطارات الفردية والزوجية لثلاثة إطارات عند كل تعويذة، وومضة أخيرة بأربعة ألوان. — Idea: cap the whole film at 16 colours; two accents alternate on odd/even frames for 3 frames per spell, and a final 4-colour flash.
- **متى أستخدمها / when:** ألعاب ريترو وبكسل آرت. — retro games and pixel art.
- **كيف / how:** Untested: keep an indexed palette array, quantise every frame to it (Pillow quantize with a fixed palette or HyperFrames ordered dither), swap the two accent indices on frame parity for 3 frames. **أرقام / params:** 16 colours; 2 accents; 3-frame flash.
- **الدليل / proof:** `kosif-tool/styles/pm-0xevinho-3777d8/BRIEF.md`

## الخلفيات والتدرجات والمعالجات — Grounds, gradients & treatments

_أرضيات المشهد: داكنة شعاعية، ورقية كريمية، بقع ضبابية متحركة، ولوحات شيدر، وسلالم المعالجة._

#### COLOR-78 · أرضيات داكنة شعاعية · Radial dark grounds · ✅ مُثبت هنا / proven here
- **ماذا / what:** خلفية داكنة بمركز أفتح قليلًا — كحلي تقني، جمر دافئ، توهج أحمر، HUD دافئ — وهي بداية القالب المختبر. — A dark ground with a slightly lighter centre — tech navy, ember, red glow, warm HUD — and the tested starter's default.
- **متى أستخدمها / when:** شرح تقني، إعلانات فاخرة، واجهات HUD. — tech explainers, premium ads, HUD scenes.
- **كيف / how:** Canvas starter: radial-gradient(#182446 → #0b1020 55%) + 90 px grid at .045 (tested). Fastify: createLinearGradient(0,0,w,h) stop0 #0c1728 on even scenes / #132337 on odd → #090d1d, so consecutive scenes breathe. 3D: K3S.studioBackdrop({inner #1e4a44, mid #0c2224 at 55%, outer #050c0d, cy .42}) as scene.background (512 px canvas). Observed: navy #131e35 → #0a121f; ember: black + off-centre #43211a at 40%; warm HUD #3a1a0e → #0e0e0b + 40 px grid at 4% + vignette; dark + radial red 15%; navy + gold accent. **أرقام / params:** centre→edge 55%; grid 90 px @ .045; alt start per scene.
- **الدليل / proof:** `kosif-tool/starters/html-canvas/index.html:14` · `fastify-motion-bro/web/motion.js:9` · `100-superskills/skills/kosif-montage-motion/scripts/kit/shape-kit.js:336` · `style:pm-tankazunori0914-0fc886`
- **شوهد أيضًا في / also seen in:** `style:pm-yunn260414-60d996` · `style:pm-astrodevil-3f2054` · `style:pm-tstfully-0aa6b4` · `style:pm-ezshine-c90d73` · `style:pm-kamstudiolabs-c9bb28`

#### COLOR-79 · أرضية ورقية كريمية · Warm paper editorial ground · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** ورق كريمي دافئ بحبر شبه أسود ولون واحد للفعل، مع فينيت شعاعي خفيف — للفصول الهادئة والخاتمات العاطفية والشرح التحريري. — Warm cream paper with near-black ink and one action colour, under a faint radial vignette — for calm chapters, emotional outros and editorial explainers.
- **متى أستخدمها / when:** قصص، شرح هادئ، خاتمة بعد فصول داكنة. — stories, calm explainers, an outro after dark chapters.
- **كيف / how:** Base #f4eee0 / ink #1f1b17 / highlight #f6cf9a / action #d9472b; radial #fcf7ed → #f2ebe1 with rust #c0502e; #efefe5 with an 8% vignette behind dark UI cards; #e6e1d2 with a 35% edge vignette and coral accent words in italic serif; split variant: two close grounds #f6f2e9 / #ebdcc7 with a soft shadow seam, coffee ink #3e2a20, terracotta #b0643a. Owner equivalents: ledger #fbf8f3 (COLOR-32), viral-editorial palettes 1/3 (COLOR-39). **أرقام / params:** vignette 8–35%; one action colour.
- **الدليل / proof:** `style:pm-1stnoel-c20a89` · `style:pm-ho-ba-f3f0e9` · `style:pm-kloss-xyz-15182a` · `style:pm-sarut0bisasuke-cefa43`
- **شوهد أيضًا في / also seen in:** `style:pm-iammxfschr-d68f90` · `style:pm-wani-shola-16ca7a` · `style:pm-amitsingha89-150378` · `style:pm-henkvaness-0e06af`

#### COLOR-80 · خلفية بقع ضبابية متحركة · Drifting blob / mesh-gradient ambient ground · 📦 بأمر تثبيت / one install
- **ماذا / what:** 3–4 بقع لونية ضخمة شديدة الضبابية تنجرف ببطء على أساس فاتح أو داكن — شفق بنفسجي برتقالي أسفل الإطار، أو باستيل خوخي ولافندر، أو تدرج خطي باستيل مع شبكة نقاط. — 3–4 huge, heavily blurred colour blobs drifting slowly over a light or dark base — violet/orange aurora along the bottom, peach/lavender pastels, or a pastel linear gradient with a dot grid.
- **متى أستخدمها / when:** إطلاق منتج، SaaS، خلفية هادئة خلف نص. — product launches, SaaS, calm backgrounds behind type.
- **كيف / how:** Pure CSS (works now): absolutely positioned divs with radial-gradient(closest-side, colour, transparent), size 60–80% of width, opacity .15–.9, blur 120–300 px, sine drift period 8–12 s (10–40 px per 10 s); warm one blob up on a key event. Pastel linear: linear-gradient(180deg, #c4a4ed, #f3daed) with #1c1838 text (>7:1), or 30° peach #f6eada → lavender #dfe4f2 with 1 px dots every 24 px at 8%. Shader: noise(uv·k + t·0.05) mixing #00F0FF / #7000FF / #000000. HyperFrames ready blocks: mesh-gradient-bg, mk-background (10 s, 1920×1080, GSAP). **أرقام / params:** blur 120–300 px; period 8–12 s; dots 1 px / 24 px @ 8%.

```html
<div class="blob" style="--c:#2f5bff; left:-10%; bottom:-30%"></div>
<div class="blob" style="--c:#6c3bff; left:30%;  bottom:-35%"></div>
<div class="blob" style="--c:#ff6a1a; right:-15%; bottom:-30%"></div>
<style>
.blob{position:absolute;width:70vw;aspect-ratio:1;opacity:.75;filter:blur(120px);
  background:radial-gradient(closest-side,var(--c),transparent);
  animation:drift 10s ease-in-out infinite alternate}
@keyframes drift{to{transform:translate(4%,-6%) scale(1.08)}}
</style>
```

- **التثبيت / install:** `npm i -D hyperframes@0.8.164 && npx hyperframes add mesh-gradient-bg`
- **الرخصة / license:** the HyperFrames blocks are timed with GSAP — GSAP 'Standard no-charge' license; the pure-CSS recipe needs no licence.
- **الدليل / proof:** `style:product` · `kosif-one/vendor/hyperframes/registry/components/mesh-gradient-bg/mesh-gradient-bg.html` · `kosif-one/vendor/hyperframes/registry/blocks/mk-background/mk-background.html` · `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`
- **شوهد أيضًا في / also seen in:** `style:pm-justincooperman-e7bbc4` · `style:pm-mehul4795-4a7007` · `style:pm-sachaarbonel-8f14f4` · `style:pm-samuel-yostt-891f87` · `style:pm-sudo-kiran-4f8b59` · `style:pm-francoxavier33-d2dfd2` · `style:pm-gonzalomacagno-2de1a9` · `style:pm-ai-baymax-0ef9dd`

#### COLOR-81 · لوحات شيدر WebGPU · WebGPU shader colour plates · 📦 بأمر تثبيت / one install
- **ماذا / what:** سبع خلفيات شيدر جاهزة مدة كل منها ثانيتان: بقعة مرجانية، عجلة ألوان، تدرج متدفق، خريطة حرارية، تدرج شبكي، بلازما، دوامة. — Seven ready 2 s shader plates: coral Blob, ColorWheel, FlowingGradient, Heatmap orb, MeshGradient, Plasma, Swirl.
- **متى أستخدمها / when:** طبقة خلفية تحت العناوين في إعلانات تقنية. — a background plate under titles in tech ads.
- **كيف / how:** `npx hyperframes add blob|color-wheel|flowing-gradient|heatmap|mesh-gradient|plasma|swirl`, or place lib/shaders.iife.js (1,444,793 bytes, shaders 4.0.0) beside the HTML and declare <canvas data-shader="Plasma" width=1920 height=1080> in a root marked data-requires-webgpu data-no-timeline. Rendering needs a WebGPU-capable Chromium — headless WebGPU is not verified here; fall back to COLOR-80's CSS blobs if it fails. **أرقام / params:** 7 shaders; 1920×1080; 2 s loops.
- **التثبيت / install:** `npm i -D hyperframes@0.8.164 && npx hyperframes add plasma`
- **الرخصة / license:** Apache-2.0 AND MIT (see lib/shaders.THIRD-PARTY-LICENSES.txt).
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/plasma/plasma.html` · `kosif-one/vendor/hyperframes/registry/blocks/mesh-gradient/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/blob/lib/shaders.THIRD-PARTY-LICENSES.txt`

#### COLOR-82 · توحيد الطبقات · Unify the stack: one grade, grain, vignette · 📄 موصوف / documented only
- **ماذا / what:** تلوين واحد فوق التركيب كله، وحبيبات 2–4%، وفينيت 10–15%، وظل تلامس لكل قصاصة — حتى تُقرأ الطبقات كصورة واحدة. — One grade over the whole composition, 2–4% grain, a 10–15% vignette and a contact shadow for every cut-out, so layers read as one photograph.
- **متى أستخدمها / when:** كولاج صور، قصاصات، منتجات فوق خلفيات. — photo collages, cut-outs, products over plates.
- **كيف / how:** Grade the final composite, not each layer (a per-layer warm over-sharpened HDR grade never fuses); grain 2–4%; vignette 10–15%; contact shadow blur 24 px, offset 0, opacity .35. Check question before render: is one grade plus grain applied to the whole stack? **أرقام / params:** grain 2–4%; vignette 10–15%; shadow 24 px @ .35.
- **الدليل / proof:** `kosif-tool/playbooks/photos.md:21`

#### COLOR-83 · سلم المعالجة · Treatment ladder: colour → duotone → halftone → vector · 📄 موصوف / documented only
- **ماذا / what:** الصورة تنزل درجات الأسلوب على الإيقاع أو الكلمات: لون كامل، ثنائي اللون، هافتون، ثم فيكتور مسطح — ونسخ بوب آرت ثنائية اللون بتوقيت متتابع. — A photo steps down stylisations on beats or words: full colour, duotone, halftone, flat vector — plus pop-art duotone clones with offset timing.
- **متى أستخدمها / when:** انتقال من صورة واقعية إلى جرافيك، أو تكرار بوب آرت. — photo-to-graphic transitions, pop-art repeats.
- **كيف / how:** duotone 300 ms → halftone 300 ms → flat vector 400 ms, each on a beat or word boundary; luma threshold 0.5; dot pitch 8–12 px at 1080 width. Duotone = map luma between two hex (CSS: grayscale + two blended layers; FFmpeg: format=gray then lut/colorize; HyperFrames two-ink-print). Tiles: one duotone shader per tile with staggered starts. **أرقام / params:** 300/300/400 ms; threshold .5; pitch 8–12 px.
- **الدليل / proof:** `kosif-tool/playbooks/photos.md:42` · `style:pm-topi-003-b0e12c`

#### COLOR-84 · تشطيب الكولاج العتيق مع الوميض · Vintage collage finish with exposure flicker · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** عوالم كولاج فوتوغرافي بتلوين عتيق باهت: نزع 40% من التشبع، صبغة سيبيا، فينيت داكن، حبيبات متحركة، ووميض تعريض خفيف. — Photo-collage worlds under a muted vintage grade: ~40% desaturation, sepia tint, dark vignette, animated grain and a slight exposure flicker.
- **متى أستخدمها / when:** زووم لا نهائي، ذكريات، سريالية عتيقة. — infinite zooms, memories, vintage surrealism.
- **كيف / how:** Observed numbers: vignette 0.6, grain 8%, flicker ±3% luminance; palette #221d17 / #332b22 / #6b746d / #a09b89 / #c4c2b3 / #928573. FFmpeg recipe (this exact chain ran here; YAVG swung 89.3–99.3 across 30 frames): hue=s=0.6 → a 50% sepia colorchannelmixer → eq brightness 0.03·sin(2π·6t) with eval=frame → vignette → noise alls=8 allf=t+u. **أرقام / params:** desat 40%; vignette .6; grain 8%; flicker ±3% at ~6 Hz.

```bash
ffmpeg -i in.mp4 -vf "hue=s=0.6,colorchannelmixer=.697:.385:.095:0:.175:.843:.084:0:.136:.267:.566,\
eq=brightness='0.03*sin(2*PI*t*6)':eval=frame,vignette=angle=PI/4.5,noise=alls=8:allf=t+u,format=yuv420p" -c:a copy vintage.mp4
```

- **الدليل / proof:** `style:pm-koldo2k-5cff87`

#### COLOR-85 · لوحات الغروب والسايكدلك والدفع الأحادي · Sunset/synthwave, psychedelic and monohue-push palettes · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** سماء خوخية وردية نيلية مع ظلال بنفسجية وإضاءات برتقالية، وشمس عملاقة مخططة، ولوحة سايكدلك نيلية برتقالية وردية ليمونية، ودفع كل الصور نحو بنفسجي واحد بسواد مسحوق. — Peach→pink→indigo skies with purple shadows and orange highlights, a giant striped sun, an indigo/orange/pink/lemon psychedelic palette, and pushing all imagery toward one violet with crushed blacks.
- **متى أستخدمها / when:** ريلز موسيقية، ريترو، توحيد صور مولدة متباينة. — music reels, retro, unifying mismatched generated images.
- **كيف / how:** Sunset: sky #f5c798 → #e5a880 → #9a6766 → #170926, lift shadows to purple, highlights to orange, slight vignette. Synthwave sun: radial red gradient disc with horizontal dark bands in its bottom third. Monohue push: base #0c0b10, accent #9a6cf0, crush blacks, lift highlights, grain 4% + vignette for cohesion (FFmpeg: hue=s=0.4 then colorbalance toward violet, or a Reinhard transfer to a violet reference, COLOR-26). **أرقام / params:** sunset 4 stops; violet push grain 4%.
- **الدليل / proof:** `style:pm-axtonliu-0b861d` · `style:pm-chrisjdimarco-f068db` · `style:pm-gizakdag-cf4ae6` · `style:pm-influencer-seo-ce8c33`

#### COLOR-86 · طين أبيض ولون للبيانات فقط · White clay render with colour only for data · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** مشهد ثلاثي الأبعاد كله رمادي فاتح كالطين، بإضاءة نصف كروية وضباب أبيض، واللون محجوز فقط لتدفق البيانات. — A 3D scene entirely in light-grey clay under hemisphere light and white fog, with colour reserved only for data flows.
- **متى أستخدمها / when:** شرح أنظمة وبنية تحتية ومعمارية برمجيات. — system, infrastructure and architecture explainers.
- **كيف / how:** MeshStandardMaterial light grey (roughness high), HemisphereLight, white FogExp2; tone mapping neutral (COLOR-57); the only saturated colour is the moving data (one hue per flow, COLOR-72). **أرقام / params:** 1 data hue per flow; everything else grey.
- **الدليل / proof:** `style:pm-sayan-shanky-f850d8`

## توليفات قوية / power combos

- **فيلم دعاء الفجر / dawn dua film:** COLOR-07 + COLOR-69 + COLOR-54 + COLOR-64 + ARAB (كلمات بقناع) + GLOW (أشعة ضوء) + VOICE (التلاوة بلا موسيقى) — مزاج dawn يرسم السماء، والسماء تنتقل ليل←فجر←صباح على 24.7 s، والإضاءة ترتفع 0.9→1.15 مع القوس، ولون ذهبي واحد للكلمة المفتاحية.
- **ريل مونتاج من لقطات العميل / client montage reel:** COLOR-02 + COLOR-14 + COLOR-15 + COLOR-01 + BEAT (قص على الإيقاع) + TRANS — ترميم ثم كشف اللوج ثم موازنة الإضاءة بين القطعات (قفزة ≤60) ثم لوك واحد للكل، والصوت الأصلي يُنسخ كما هو.
- **«سوّه مثل هذا الفيديو» / match a reference:** COLOR-25 + COLOR-24 + COLOR-26 + COLOR-27 + COLOR-56 + FOOT + QA (ورقة قبل/بعد) — باليت وخلفية لكل نبضة، ثم نقل رينهارد إلى LUT لكل لقطة بقوة 0.85، وقفل الأسلوب يحفظ الـhex للسلسلة كلها.
- **هوية عميل من لون الشعار / brand from a logo colour:** COLOR-30 + COLOR-31 + COLOR-52 + COLOR-54 + BRAND (كشف الشعار) + TYPE — ألوان الشعار الحقيقية، ثم ثيم فاتح وداكن يمر 4.6:1، ولون تمييز واحد على 5% من الإطار.
- **إعلان منتج مرح / playful product ad:** COLOR-67 + COLOR-68 + COLOR-80 + COLOR-75 + UI + EASE — فصول بحقول لونية تُقلب على الإيقاع، ضربة لون الهوية عند الكشف، وبقع شفق خلف الواجهة، وكلمة الوعد بلون الهوية.
- **شرح بيانات / data explainer:** COLOR-46 + COLOR-47 + COLOR-45 + COLOR-52 + DATA + EXPL — أوكابي-إيتو للفئات، رمادي للسياق ولون واحد للاستنتاج، وشارات حالة بصبغة وأيقونة، وكل تسمية تمر اختبار التباين.
- **ليل ثلاثي الأبعاد مقنع / believable 3D night:** COLOR-57 + COLOR-58 + COLOR-59 + COLOR-61 + COLOR-60 + 3D + GLOW — AgX للمصابيح، رؤية ليلية 0.35–0.55 وتقسيم لوني، ضباب بثلاث قنوات، فانوس 1900K مقابل قمر 4100K، ورفع خفيف للسواد.
- **قصة عاطفية قبل/بعد / emotional before-after:** COLOR-70 + COLOR-66 + COLOR-71 + STORY + SYNC — اللون ينطفئ للرمادي عند الكلمة الحزينة، والقطبية تنقلب عند المنعطف، والحل يأخذ لونه الخاص.
- **غلاف أو لقطة مولّدة بهوية دقيقة / generated plate on brand:** GEN + COLOR-35 + COLOR-03 + COLOR-56 + ARAB — ولّد بلا نص، حوّل الذهبي إلى لون الهوية انتقائيًا أو اسحب الرمادي نحو الكحلي مع عكس أفقي ليفرغ اليمين للعربية، وطبّق الـhex الحقيقي في طبقة الحركة.

## أخطاء ممنوعة / never do

1. **لا تخلط التصحيح التقني باللوك الإبداعي في خطوة واحدة** — يصبح كل تعديل لاحق مستحيل القياس؛ تعريض ← توازن أبيض ← LUT ← تباين ← تشبع ← لوك منفصل (COLOR-13).
2. **لا تطبق LUT تحويل Log على لقطة لم يثبت أنها Log، ولا تطبقه مرتين** — وسم bt709 والمظهر الباهت ليسا دليلًا؛ 8-bit yuv420p ليس Log؛ النتيجة ألوان محروقة (COLOR-14).
3. **لا تلمس صوت المستخدم أثناء التلوين** — كل سلاسل المالك تنسخ الصوت `-c:a copy`؛ و`recolor_ice.py` يسقط الصوت في الفيديو — أعد دمج الصوت الأصلي دائمًا.
4. **لا تعتمد على Hald/‏.cube لنقل الحبيبات أو الشحذ أو الفينيت** — الـLUT لوني فقط؛ noise وunsharp وcas وvignette تضيع عند الخبز — أضفها بعد LUT (COLOR-04).
5. **لا ترفع التشبع فوق 1.25 ولا تشبّع الظلال والإضاءات بقدر المنتصف** — البشرة تتشوه والإضاءات تحترق؛ ارفع فقط اللقطات التي تحت أرضيتها، واخفض التشبع تحت 15% وفوق 85% من الإضاءة حتى 60% (COLOR-18).
6. **لا تزد على لون تمييز واحد بمعنى واحد** — العين لا تعرف أين تنظر؛ ≈5% من الإطار، ولحظة واحدة تملأ الكادر، والمحايدات تميل لصبغة الهوية (COLOR-54).
7. **لا تضع نصًا فوق تدرج أو فيديو دون حساب التباين بعد دمج الشفافية** — الإطار الأفتح تحت اللوحة يقتل القراءة؛ 4.5:1 للنص و3:1 للعناصر الكبيرة (COLOR-52).
8. **لا تجعل اللون الإشارة الوحيدة للمعنى، ولا تستخدم قوس قزح لقيم مرتبة** — 8% من الرجال لا يميزون الأحمر من الأخضر، وقوس قزح يكذب على الترتيب؛ أضف شكلًا أو تسمية واستخدم تدرجًا أحادي الإضاءة (COLOR-46/47).
9. **لا تقلب الألوان لصنع الوضع الداكن ولا تستخدم الأسود والأبيض النقيين** — الهوية تفقد روحها ويظهر توهج الشاشات؛ خلفية شبه سوداء بصبغة الهوية وتشبع أقل (COLOR-53).
10. **لا تثق بمولد الصور في لون الهوية** — النماذج لا تحفظ الـhex والبذور لا تنتقل بين النماذج؛ طبّق اللون الحقيقي في طبقة الحركة (COLOR-56).
11. **لا تدرّج قلب الألوان على الإيقاع حين يطلب الأسلوب ضربة حادة، ولا تقلب القطبية على إطار ساكن** — الانتقال البطيء يقتل الضربة؛ tl.set عند زمن الإيقاع، و0.1 s فقط عند حدود الفصل (COLOR-66/67).
12. **لا تنسخ لوحة أو ملفًا من كود بائع بلا رخصة** — Arko في vendor بلا رخصة: انظر وتعلم ولا تنسخ؛ مكونات HyperFrames الموقوتة بـGSAP تخضع لرخصة GSAP القياسية.

## أقوى 5 حركات توقيع / 5 signature moves

1. **COLOR-01 — الأحد عشر لوكًا:** سطر واحد يعطي الفوتيج مزاجه: blue_hour لليل الهادئ، golden_hour للذكرى، teal_orange للإعلان — مُثبتة هنا والصوت لا يُمس.
2. **COLOR-31 — هوية من لون واحد:** لون شعار العميل ← ثيم فاتح وداكن وحالات وحركة، كل زوج ≥4.6:1 — قبل أول مشهد.
3. **COLOR-26 — رينهارد إلى LUT لكل لقطة:** «خلّه مثل هذا الفيلم» بأرقام: Lab mean/std بقوة 0.85 في مكعب 33³ يعمل في FFmpeg.
4. **COLOR-66 — قلب القطبية:** حبر↔ورق عند منعطف القصة في 0.1 s — أبسط حركة لونية وأقواها سرديًا، وشوهدت في ثمانية من أفلامك.
5. **COLOR-69 — سماء تتحول:** ليل ← فجر ← صباح بتحريك ثلاث محطات تدرج على 24.7 s — توقيع أفلام الدعاء والقصائد.
