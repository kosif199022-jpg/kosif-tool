# المقاسات والمنصات — Formats & platforms

> فصل مُجمَّع آليًا من 185 ملاحظة حصاد (مستودعات KOSIF + أطلس المهارات + 253 فيديو مرجعي)، مدموجة إلى **183 قدرة** مرتبة من الأقوى دليلًا. لم يُحرَّر يدويًا بعد — تحقّق من الدليل قبل الادعاء.
> Auto-compiled chapter: 183 powers deduplicated by name from 185 harvested atoms; strongest evidence first.

**الحالة:** ✅ مُثبت هنا 17 · 🟢 جاهز 41 · 📦 بأمر تثبيت 36 · 🔑 مفتاح/خدمة 7 · 👁 شوهد في فيديو 9 · 📄 موصوف 70 · 💡 فكرة 3

#### FMT-01 · تصدير ماستر H.264 آمن للويب · Web-safe H.264 master export · ✅ مُثبت هنا
- **ماذا / what:** Every MP4 for web/social is encoded 4:2:0 8-bit with the moov atom moved to the front so it starts playing before download finishes, and tagged BT.709 so iOS/QuickTime do not wash colours out.
- **كيف / how:** ffmpeg -i in -c:v libx264 -preset slow -crf 17..23 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 -movflags +faststart -c:a aac -b:a 160k..320k out.mp4
- **أرقام / params:** crf 17 (final) / 23 (web); aac 160-320k 48kHz
- **الدليل / proof:** `kosif-atlas/skills/235-mas-video-lab/754-ffmpeg/SKILL.md` · `kosif-atlas/skills/1526-gamegen/4173-game-trailer/references/assembly-and-review.md`

#### FMT-02 · GIF متكرر بلا قطع · Seamless looping GIF · ✅ مُثبت هنا
- **ماذا / what:** Make a short loop whose seam is invisible by cross-fading the tail into the head, then build an adaptive palette for small, clean GIFs.
- **كيف / how:** fps=F,scale=W:-2:flags=lanczos,split; trim tail/head; xfade=transition=fade:duration=0.4:offset=dur-0.8 ; palettegen=stats_mode=diff:max_colors=192 ; paletteuse=dither=sierra2_4a:diff_mode=rectangle ; -loop 0. Over budget: width 480 -> fps 15 -> 128 colours -> shorter shot.
- **أرقام / params:** ~6 s, <15 MB (X/Discord)
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4173-game-trailer/references/assembly-and-review.md` · `kosif-atlas/skills/1526-gamegen/4173-game-trailer/assets/marketing/render.py`

#### FMT-03 · بيان تطبيق ويب تقدمي عربي · Arabic RTL PWA manifest · ✅ مُثبت هنا
- **ماذا / what:** Installable standalone app manifest in Arabic RTL with SVG any/maskable icons and shortcuts.
- **كيف / how:** manifest.webmanifest: lang ar, dir rtl, display standalone, icons svg sizes any; service worker caches shell assets.
- **أرقام / params:** background/theme #f8fafc; shell theme-color #24113f (index) / #211830 (legacy)
- **الدليل / proof:** `kosif-audit-studio/manifest.webmanifest` · `kosif-audit-studio/sw.js`

#### FMT-04 · ملف ترميز الويب للصور والمقاطع · Web delivery encode profile (stills + clips) · ✅ مُثبت هنا
- **ماذا / what:** Lightweight delivery: WebP stills at fixed widths and silent H.264 clips with faststart; total brand art ~1.8 MB.
- **كيف / how:** WebP quality 80; H.264 width 1280 -crf 27 -an -movflags +faststart; sectors cropped 3:2 to 720x480.
- **أرقام / params:** widths 1600 / 1200 / 900 / 720x480; crf 27
- **الدليل / proof:** `kosif-earth-ci-fork/docs/design/HIGGSFIELD_VISUALS_ar.md` · `kosif-earth-ci-fork/tools/brand_art.test.mjs`

#### FMT-05 · أيقونات التثبيت ولون السمة · PWA install icons + theme colour · ✅ مُثبت هنا
- **ماذا / what:** Installable app icons rendered from the SVG mark and manifest colours matched to the ledger ink.
- **كيف / how:** payload/icon-192.png.b64, icon-512.png.b64, apple-touch-icon.png.b64; manifest theme_color/background_color #1d1814; <meta name=theme-color content=#1d1814>.
- **أرقام / params:** 192 / 512 / 180 px
- **الدليل / proof:** `kosif-earth-ci-fork/tools/identity_unity.test.mjs` · `kosif-earth-ci-fork/tools/brand/make_marks.py`

#### FMT-06 · أطوال مقاطع Flow/Veo · Flow/Veo clip length presets · ✅ مُثبت هنا
- **ماذا / what:** AI clip lengths used: 6 s (fitness, viral), 7 s (stickman), 8 s Veo or 10 s Flow (kinetic), 10 s (vox, food); model availability must be re-verified.
- **كيف / how:** Set in each profile; kinetic labels model capability 'verify availability'.
- **أرقام / params:** 6/7/8/10 s
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/kinetic-flow.mjs:41,116` · `fastify-motion-bro/scripts/profiles/stickman.mjs:29` · `fastify-motion-bro/docs/PROFILE_CATALOG.md:19`

#### FMT-07 · التسليم لكل منصة · Platform deliveries · ✅ مُثبت هنا
- **ماذا / what:** One checked file per platform (ratio, size, bitrate ceiling, limits reported, never trimmed).
- **كيف / how:** python scripts/kmotion.py platforms FILM.mp4 --out deliver --platforms tiktok,shorts,whatsapp --title …
- **أرقام / params:** limits 'verify at use'
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md`

#### FMT-08 · قالب بطاقة الختام · Template: end-card · ✅ مُثبت هنا
- **ماذا / what:** Call to action, handle, three social icons (heart, comment, share) staggered, subscribe pill squashing twice, linear progress bar.
- **كيف / how:** python scripts/mtemplates.py new NAME --template end-card --set key=value ... [--seconds S --size WxH --fps F] -> projects/NAME/index.html (+ fonts, gsap, motion-kit); preview in a browser; render with motion.py render.
- **أرقام / params:** 6 s; cta 'تابعنا للمزيد', handle '@kosif', accent #E7B65A, bg1 #1b2a49, bg2 #0d1b2a; button text 'اشترك'; bar 1u tall, linear over D-0.4 s
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/templates/motion/end-card.html` · `100-superskills/skills/kosif-montage-motion/scripts/mtemplates.py:55`

#### FMT-09 · اختيار الغلاف وتثبيته كإطار أول · Poster pick and bake as frame 0 · ✅ مُثبت هنا
- **ماذا / what:** A good still is picked (never the black head or tail) and baked as the first frame so social thumbnails are not black, keeping frame count and AAC audio.
- **كيف / how:** poster.pick(film) → {t}; poster.extract(film, t, jpg); poster.bake(film, jpg, out) → frames unchanged.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_launch.py:89`

#### FMT-10 · جدول التسليم حسب المنصة · Platform delivery table · ✅ مُثبت هنا
- **ماذا / what:** Per-platform aspect, size, max duration, max MB and bitrates; e.g. WhatsApp status 720×1280 ≤30 s ≤16 MB.
- **كيف / how:** platforms.PLATFORMS: tiktok 9:16 1080×1920 600 s 287 MB; reels 180 s 250 MB; shorts 180 s 256 MB; youtube 16:9 1920×1080 2000 MB; x 16:9 1280×720 140 s 512 MB; whatsapp 9:16 720×1280 30 s 16 MB; linkedin 1:1 1080×1080 600 s 200 MB; snapchat 60 s 32 MB; kmotion platforms FILM --platforms tiktok,reels,shorts.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_v6.py:180`

#### FMT-11 · توحيد المقاطع على 9:16 بالقص · 9:16 cover-crop normaliser for found footage · ✅ مُثبت هنا
- **ماذا / what:** Turns any downloaded clip into an exact vertical segment: cover scale, centre crop, constant fps, SAR 1, yuv420p, no audio.
- **كيف / how:** ffmpeg -ss 0 -i clip -t DUR -an -vf scale=W:H:force_original_aspect_ratio=increase:flags=bicubic,crop=W:H,setsar=1,fps=24,<grade>,format=yuv420p -c:v libx264 -preset ultrafast|veryfast -crf 24 -threads 2 -r 24; optionally -stream_loop -1 to loop clips shorter than the slot.
- **أرقام / params:** W,H = 540x960 or 720x1280; fps 24; crf 24; threads 2 (low-RAM laptop)
- **الدليل / proof:** `kosif-one/projects/KOSIF_Motion_Ghorba/KOSIF_Ghorba_Render.py:146-148` · `kosif-one/projects/KOSIF_Motion_Ghorba/tools/render_ghorba_preview.py:137-145`

#### FMT-12 · حزمة نشر لكل منصة مع فحص · Per-platform post pack + linter · ✅ مُثبت هنا
- **ماذا / what:** Writes a post pack per platform (caption, hashtags, YouTube title/description, CTA, first comment, cover text, alt text) and checks it against each platform's limits and the video's fit. Never posts.
- **كيف / how:** python social.py pack FILM.mp4 --platforms tiktok,reels,shorts --topic ... --out X.post.json; python social.py check X.post.json (exit 0 = ready).
- **أرقام / params:** X weighted (emoji 2, URL 23); YouTube title <= 100 (warn > 70); Instagram 5 hashtags; YouTube > 60 voids all; Threads 1
- **الدليل / proof:** `kosif-one/tools/kosif-social/SKILL.md` · `kosif-one/tools/kosif-social/scripts/social.py:39`

#### FMT-13 · حدود المنصات · Platform limits table (as of 2026-10) · ✅ مُثبت هنا
- **ماذا / what:** Caption, hashtag, visible-before-more, max seconds, ratio, size and carousel limits for nine platforms.
- **كيف / how:** python social.py limits [--platform X].
- **أرقام / params:** tiktok 4000 chars/600 s/9:16 1080x1920/35 photos; reels 2200/5 tags/125 visible/180 s; instagram 4:5 1080x1350 carousel 20; shorts title 100/180 s; youtube 16:9 thumb 1280x720; facebook 63206 chars/carousel 10; x 280 weighted/140 s/4 images; linkedin 3000/210 visible/600 s/PDF carousel; threads 500/…
- **الدليل / proof:** `kosif-one/tools/kosif-social/scripts/social.py:35` · `kosif-one/tools/kosif-social/scripts/social.py:39`

#### FMT-14 · حزمة بوست لكل منصة · Per-platform post pack + check · ✅ مُثبت هنا
- **ماذا / what:** Probes the film, reports fit per platform, then lints captions: length (X weighted emoji 2/URL 23), YT title <=100 warn >70, hashtag max (IG 5, YT >60 voids, Threads 1), hashtag form, Arabic-normalised duplicates, hook before 'more', dead links, CTA, alt text.
- **كيف / how:** python3 social.py pack FILM.mp4 --platforms tiktok,reels,shorts --topic ... ; social.py check post.json (exit 0 ready)
- **أرقام / params:** see platform table
- **الدليل / proof:** `100-superskills/skills/kosif-social/scripts/social.py:165` · `100-superskills/skills/kosif-social/SKILL.md`

#### FMT-15 · جدول مواصفات المنصات · Platform spec table · ✅ مُثبت هنا
- **ماذا / what:** TikTok 4000 chars 600 s 9:16 1080x1920 carousel 35; Reels 2200, 5 tags, 125 visible, 180 s; Instagram 4:5 1080x1350 carousel 20; Shorts title 100, 180 s; YouTube 16:9 1920x1080 thumb 1280x720; Facebook 63206; X 280 weighted 140 s 1280x720 carousel 4; LinkedIn 3000, 210 visible, 1:1, PDF carousel; Th…
- **كيف / how:** python3 social.py limits [--platform]
- **أرقام / params:** see what
- **الدليل / proof:** `100-superskills/skills/kosif-social/scripts/social.py:39`

#### FMT-16 · مواصفات التسليم للمنصات · Platform delivery spec · ✅ مُثبت هنا
- **ماذا / what:** Every MP4: H.264 yuv420p, even dimensions, +faststart, AAC 48 kHz, integrated −14 LUFS, true peak ≤ −1 dBTP.
- **كيف / how:** tools.V/A constants + inspect gate
- **أرقام / params:** crf 18 preset medium; AAC 192-256 kb/s
- **الدليل / proof:** `kosif-studio/motion/tools.py:42` · `kosif-studio/motion/qa.py:173`

#### FMT-17 · جدول النسب والدقات · Aspect/resolution table · ✅ مُثبت هنا
- **ماذا / what:** 9:16=1080x1920, 16:9=1920x1080, 1:1=1080x1080, 4:5=1080x1350 (CLI/web); verify_video also accepts 4:3 and 21:9.
- **كيف / how:** --aspect
- **الدليل / proof:** `kosif-tool/tools/kosif.py:35` · `kosif-tool/tools/verify_video.py:24`

#### FMT-18 · مسرح ثابت 16:9 يُكبَّر ككتلة واحدة · Fixed 16:9 stage scaled as a whole · 🟢 جاهز
- **ماذا / what:** Author every frame on a fixed 1920x1080 canvas and scale the whole stage to the viewport (letterbox/pillarbox) instead of reflowing; works standalone and inside iframes.
- **كيف / how:** Wrapper + .deck-stage with transform: scale(min(vw/1920, vh/1080)); keep all chrome inside the stage; switch slides with visibility/opacity, not display. Negate clamp with calc(-1*clamp()).
- **أرقام / params:** canvas 1920x1080; no responsive breakpoints inside the stage
- **الدليل / proof:** `kosif-atlas/skills/880-superloopy/1944-superloopy-slides` · `kosif-atlas/skills/880-superloopy/1944-superloopy-slides/viewport-base.css` · `kosif-atlas/skills/880-superloopy/1944-superloopy-slides/html-template.md`

#### FMT-19 · تسجيل المتصفح إلى MP4 وGIF بمرورين · Browser clip to MP4 and two-pass GIF · 🟢 جاهز
- **ماذا / what:** Record UI motion at an explicit video size so it isn't downscaled, keep the original WebM, convert to H.264 MP4 for players and only make a GIF when its lower fidelity still communicates timing.
- **كيف / how:** Playwright video:{mode:'on', size:{width:1280,height:820}}; ffmpeg -i in.webm -vf scale=1280:-2 -c:v libx264 -pix_fmt yuv420p -crf 26 -preset veryfast -movflags +faststart -an out.mp4; GIF: fps=12,scale=960:-1:flags=lanczos,palettegen then [x][1:v]paletteuse.
- **أرقام / params:** crf 26; GIF fps 12, width 960, lanczos
- **الدليل / proof:** `kosif-atlas/skills/1530-webcraft/4196-ui-screenshots/references/clips.md`

#### FMT-20 · تحجيم مع حشو لأي مقاس · Scale + pad letterbox to any frame · 🟢 جاهز
- **ماذا / what:** Fit any source into a target canvas without distortion by scaling down to fit and padding the rest (letter/pillar box), e.g. landscape into 1080x1920 with blurred or flat bars.
- **كيف / how:** scale=W:H:force_original_aspect_ratio=decrease,pad=W:H:(ow-iw)/2:(oh-ih)/2 ; blurred-bars variant: split; [bg]scale=W:H:force_original_aspect_ratio=increase,crop=W:H,gblur=sigma=30[bg]; [bg][fg]overlay=(W-w)/2:(H-h)/2
- **أرقام / params:** 1080x1920, 1080x1350, 1080x1080, 1920x1080
- **الدليل / proof:** `kosif-atlas/skills/235-mas-video-lab/754-ffmpeg/SKILL.md`

#### FMT-21 · سلم جودات HLS · Multi-rendition HLS ladder · 🟢 جاهز
- **ماذا / what:** Package one master into 1080/720/480 renditions with aligned keyframes for adaptive streaming.
- **كيف / how:** split=3 + scale/pad per rung; libx264 5000k/2800k/1400k with maxrate≈1.07x and bufsize 1.5x; -g 60 -keyint_min 60 -sc_threshold 0 ; -f hls -hls_time 4 -hls_playlist_type vod -hls_flags independent_segments -var_stream_map 'v:0,a:0 v:1,a:0 v:2,a:0' -master_pl_name master.m3u8. Prefer per-title ladders and CMAF once for HLS+DASH.
- **أرقام / params:** GOP 2 s @30fps; 4 s segments
- **الدليل / proof:** `kosif-atlas/skills/235-mas-video-lab/754-ffmpeg/SKILL.md` · `kosif-atlas/skills/2387-streaming-media-engineering/9243-transcoding-and-abr-ladder/SKILL.md`

#### FMT-22 · تنسيق صفحة التقرير الورقية · Report 'paper' page styling · 🟢 جاهز
- **ماذا / what:** On-screen report preview styled as a printed sheet with a letter-spaced brand header rule.
- **كيف / how:** .paper min-height 720px, background #fcfbf7 (editorial #fffdf8), padding 64px clamp(28px,6vw,78px), shadow 0 22px 60px #0008; .paper-brand weight 800 ls 3px #5b376d 2px underline.
- **أرقام / params:** h1 34px; h2 18px with 1px #ddd3df rule; body lh 1.9; mobile padding 38x22, min-height 580
- **الدليل / proof:** `kosif-audit-studio/continuous-review.css:1` · `kosif-audit-studio/kosif-one-editorial-theme.css`

#### FMT-23 · أنماط الطباعة · Print stylesheets · 🟢 جاهز
- **ماذا / what:** Print hides chrome/buttons, forces white background and black text, avoids breaking panels, and uses 11pt body.
- **كيف / how:** @media print { .topbar,.primary-rail,... {display:none!important}; panels break-inside: avoid; box-shadow none }.
- **أرقام / params:** border #b8b8b8; v17 body 11pt / 1.6
- **الدليل / proof:** `kosif-audit-pro/app/globals.css:3133` · `kosif-audit-pro/patch/kosif-v17.css` · `kosif-audit-studio/styles.css:851`

#### FMT-24 · قفل لوحة الطباعة · Print palette lock (always light heritage) · 🟢 جاهز
- **ماذا / what:** Whatever theme is on screen, print media switches to a light heritage palette with Amiri / Aref Ruqaa and the default categorical chart colours.
- **كيف / how:** @media print block in tokens.css overriding all looks; body background #fff.
- **أرقام / params:** ink #2b1a0f; brand #8a5a2b; fonts Amiri, Noto Naskh Arabic, Aref Ruqaa
- **الدليل / proof:** `kosif-earth-ci-fork/ui/ds/tokens.css:446`

#### FMT-25 · تصدير الرسم PNG/SVG وعرض جدول · Chart export PNG@2x / SVG + table toggle · 🟢 جاهز
- **ماذا / what:** Every chart can switch to its data table and download itself as SVG or a 2x PNG with legend and title baked in, with a print stylesheet that hides tools.
- **كيف / how:** exportFig(fig,fmt): resolve CSS var colours via getComputedStyle, serialise SVG, draw into canvas at k=2, canvas.toBlob('image/png'); fallback to SVG on error; PRINT_CSS for print windows.
- **أرقام / params:** scale 2x
- **الدليل / proof:** `kosif-earth-ci-fork/ui/components/charts.js:184` · `kosif-earth-ci-fork/ui/components/charts.js:247`

#### FMT-26 · تحويل المستند إلى عرض شرائح · Document -> slideshow presentation mode · 🟢 جاهز
- **ماذا / what:** Turns any generated report into full-screen slides: a gradient title slide, then one slide per h1/h2 section under the brand mark, keyboard navigation, keeping the document's own table styles.
- **كيف / how:** SK.output present(): slidesOf(doc) splits at headings; short preface becomes subtitle; PRES_CSS (branded via brandCSS); title slide linear-gradient(135deg,#0b1030 0%,#2a3fae 60%,#2340c4 100%); header border-bottom 3px; title clamp(22px,4vw,44px) 800.
- **أرقام / params:** slide padding clamp(12px,3vw,40px) clamp(12px,4vw,56px); 100vh
- **الدليل / proof:** `kosif-earth-ci-fork/ui/core/output.js:228`

#### FMT-27 · صيغ الإيصال الحراري والملصقات مع QR · Thermal receipt / label print formats + QR · 🟢 جاهز
- **ماذا / what:** Print layouts for 80mm thermal receipts with ZATCA QR and 60x40mm scale/packaging labels; QR drawn with an embedded qrcode.js.
- **كيف / how:** new QRCode(box,{...,correctLevel:QRCode.CorrectLevel.M}); TLV-encoded invoice data.
- **أرقام / params:** 80mm receipt; 60x40mm label; QR ECC M
- **الدليل / proof:** `kosif-earth-ci-fork/ui/features/enterprise.js:1` · `kosif-earth-ci-fork/ui/features/enterprise.js:246`

#### FMT-28 · مقاسات الإخراج · Aspect & resolution presets · 🟢 جاهز
- **ماذا / what:** Three aspect ratios with derived pixel sizes: 9:16 for TikTok/Reels (default), 16:9 YouTube, 1:1; final suggested 1920 px tall at 30 fps.
- **كيف / how:** brief.aspect -> player canvas size; render.py width=round(h*ratio) forced even.
- **أرقام / params:** 9:16 1080x1920; 16:9 3413x1920 if h=1920 (use --height 1080 for 1920x1080); 1:1; fps 30
- **الدليل / proof:** `fastify-motion-bro/scripts/planner.mjs:10` · `fastify-motion-bro/scripts/render.py:29-33` · `fastify-motion-bro/web/player.js:20-22`

#### FMT-29 · أمثلة ملخصات · Example briefs · 🟢 جاهز
- **ماذا / what:** Three ready briefs: رحلة الإبداع doodle 9:16 30 s ar-EG; Product Launch brag 16:9 20 s en; الشرح بطريقة الرسم whiteboard 9:16 45 s ar.
- **كيف / how:** Copy into project/brief.json and run npm run plan.
- **الدليل / proof:** `fastify-motion-bro/examples/demo-9x16.json` · `fastify-motion-bro/examples/launch-16x9.json` · `fastify-motion-bro/examples/whiteboard-ar.json`

#### FMT-30 · إعادة التأطير الذكي · Smart aspect reframe · 🟢 جاهز
- **ماذا / what:** 9:16 around faces (motion centroid fallback), crop or blurred pad.
- **كيف / how:** python scripts/kmotion.py aspect CLIP.mp4 --to 9:16 --mode smart|crop|blur
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md`

#### FMT-31 · تصدير متعدد النسب · Multi-aspect export + poster + GIF/WebP · 🟢 جاهز
- **ماذا / what:** Every aspect variant + poster in parallel.
- **كيف / how:** python scripts/kmotion.py export FILM.mp4 --out deliver --aspects 9:16,1:1,16:9 --title … --gif --webp
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md`

#### FMT-32 · أشرطة سينمائية · Letterbox reveal · 🟢 جاهز
- **ماذا / what:** Black bars that open at the start of a cinematic shot.
- **كيف / how:** scene3d index.html: tween #letterbox-top/bottom height.
- **أرقام / params:** 70 px -> 0 over 2.2 s power4.inOut at min(2.4 s, 15% of D)
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/templates/scene3d/index.html:36`

#### FMT-33 · مقاسات وإطارات مستخدمة في المشاريع · Format presets demonstrated by the projects · 🟢 جاهز
- **ماذا / what:** The example films cover the common deliverables: vertical 1080×1920 30 fps (5 s, 20.6 s), 1920×1080 at 30 and 60 fps (5–17 s), 1280×720 24 fps (12 s), 960×540 24 fps lab previews, 720×1280 30 fps voice pieces.
- **كيف / how:** Set data-width/height/fps/duration on #root; keep fonts and layout absolute in px for that size.
- **أرقام / params:** five_sec/bunny 1080×1920@30 5 s; premium_edit 1080×1920@30 20.566 s; showreel 1920×1080@60 15 s; night_boat 5 s, blue_hour 8 s, koi/sound_ground 10 s, water 17 s @30; midnight 1280×720@24 12 s; lab 960×540@24 20 s
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/five_sec/index.html:33` · `100-superskills/skills/kosif-montage-motion/scripts/projects/showreel/index.html:38` · `100-superskills/skills/kosif-montage-motion/scripts/projects/lab_rabbit_lion/index.html:22`

#### FMT-34 · تصدير tiktok · Platform export tiktok · 🟢 جاهز
- **ماذا / what:** Checked delivery file for tiktok: reframed, bitrate-capped, limits reported not trimmed.
- **كيف / how:** platforms.py FILM --platforms tiktok --mode smart|crop|blur ; libx264 high, CRF 20, maxrate, faststart, AAC 48k
- **أرقام / params:** 9:16 1080x1920, 600s, 287MB, 12000k/192k
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/platforms.py:28`

#### FMT-35 · تصدير reels · Platform export reels · 🟢 جاهز
- **ماذا / what:** Checked delivery file for reels: reframed, bitrate-capped, limits reported not trimmed.
- **كيف / how:** platforms.py FILM --platforms reels --mode smart|crop|blur ; libx264 high, CRF 20, maxrate, faststart, AAC 48k
- **أرقام / params:** 9:16 1080x1920 180s 250MB 12000k
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/platforms.py:28`

#### FMT-36 · تصدير shorts · Platform export shorts · 🟢 جاهز
- **ماذا / what:** Checked delivery file for shorts: reframed, bitrate-capped, limits reported not trimmed.
- **كيف / how:** platforms.py FILM --platforms shorts --mode smart|crop|blur ; libx264 high, CRF 20, maxrate, faststart, AAC 48k
- **أرقام / params:** 9:16 180s 256MB 12000k
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/platforms.py:28`

#### FMT-37 · تصدير youtube · Platform export youtube · 🟢 جاهز
- **ماذا / what:** Checked delivery file for youtube: reframed, bitrate-capped, limits reported not trimmed.
- **كيف / how:** platforms.py FILM --platforms youtube --mode smart|crop|blur ; libx264 high, CRF 20, maxrate, faststart, AAC 48k
- **أرقام / params:** 16:9 1920x1080 2000MB 16000k/256k
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/platforms.py:28`

#### FMT-38 · تصدير x · Platform export x · 🟢 جاهز
- **ماذا / what:** Checked delivery file for x: reframed, bitrate-capped, limits reported not trimmed.
- **كيف / how:** platforms.py FILM --platforms x --mode smart|crop|blur ; libx264 high, CRF 20, maxrate, faststart, AAC 48k
- **أرقام / params:** 16:9 1280x720 140s 512MB 8000k
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/platforms.py:28`

#### FMT-39 · تصدير whatsapp · Platform export whatsapp · 🟢 جاهز
- **ماذا / what:** Checked delivery file for whatsapp: reframed, bitrate-capped, limits reported not trimmed.
- **كيف / how:** platforms.py FILM --platforms whatsapp --mode smart|crop|blur ; libx264 high, CRF 20, maxrate, faststart, AAC 48k
- **أرقام / params:** 9:16 720x1280 30s 16MB 2200k/96k
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/platforms.py:28`

#### FMT-40 · تصدير linkedin · Platform export linkedin · 🟢 جاهز
- **ماذا / what:** Checked delivery file for linkedin: reframed, bitrate-capped, limits reported not trimmed.
- **كيف / how:** platforms.py FILM --platforms linkedin --mode smart|crop|blur ; libx264 high, CRF 20, maxrate, faststart, AAC 48k
- **أرقام / params:** 1:1 1080 600s 200MB 8000k
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/platforms.py:28`

#### FMT-41 · تصدير snapchat · Platform export snapchat · 🟢 جاهز
- **ماذا / what:** Checked delivery file for snapchat: reframed, bitrate-capped, limits reported not trimmed.
- **كيف / how:** platforms.py FILM --platforms snapchat --mode smart|crop|blur ; libx264 high, CRF 20, maxrate, faststart, AAC 48k
- **أرقام / params:** 9:16 60s 32MB 6000k/128k
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/platforms.py:28`

#### FMT-42 · ريل بأمر واحد · One-command reel · 🟢 جاهز
- **ماذا / what:** Transcribe → decaption → restore → voice chain → music → captions → gate.
- **كيف / how:** reel.py CLIP --out F --style reels --music auto
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/reel.py`

#### FMT-43 · صورة الغلاف · Poster frame bake · 🟢 جاهز
- **ماذا / what:** Strongest settled frame as JPEG, baked into frame 0.
- **كيف / how:** poster.py FILM --at 3.2 --bake
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/poster.py`

#### FMT-44 · مقاسات ونسب الاستوديو · Studio size and ratio presets · 🟢 جاهز
- **ماذا / what:** The canvas sizes and ratios offered across the studio forms.
- **كيف / how:** recipes SIZES / RATIOS; Workbench ASPECTS.
- **أرقام / params:** sizes 1080x1920, 1920x1080, 1080x1080, 1080x1350; ratios 9:16, 16:9, 1:1, 4:5; fps 24/25/30/50/60
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:15` · `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:16` · `100-superskills/skills/kosif-montage-motion/scripts/web/wbcompat.py:22`

#### FMT-45 · KOSIF Studio Cloud كصفحة واحدة · KOSIF Studio Cloud (one-page claude.ai artifact) · 🟢 جاهز
- **ماذا / what:** Bundles the whole Studio editor into one self-contained HTML page that runs as a claude.ai artifact with no server; file saves go through the artifact's downloads capability.
- **كيف / how:** python scripts/web/build_studio_cloud.py --out studio-cloud.html --home-url URL; modules wrapped in IIFE scopes, imports rewritten, mp4-muxer@5.2.1 loaded from cdn.jsdelivr.net, download() routed to __kosifSave → window.claude.use('downloads').save().
- **أرقام / params:** verified here: builds a 78,588-byte page; save errors mapped (declined, too_large, rate_limited, rejected_extension)
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/build_studio_cloud.py:1` · `100-superskills/skills/kosif-montage-motion/scripts/web/build_studio_cloud.py:21` · `100-superskills/skills/kosif-montage-motion/scripts/web/build_studio_cloud.py:45`

#### FMT-46 · مقاسات الإخراج · Output aspect presets · 🟢 جاهز
- **ماذا / what:** Named frame sizes used by montage and reel.
- **كيف / how:** --ratio 9:16|16:9|1:1|4:5.
- **أرقام / params:** 9:16 1080x1920; 16:9 1920x1080; 1:1 1080x1080; 4:5 1080x1350
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/montage.py:57`

#### FMT-47 · إعادة التأطير · Reframe: smart / crop / blurred pad · 🟢 جاهز
- **ماذا / what:** Converts aspect: face-aware crop (motion centroid fallback), centre crop, or fitted picture over a blurred darkened copy.
- **كيف / how:** python tools.py aspect CLIP --to 9:16 --mode smart|crop|blur --out v.mp4.
- **أرقام / params:** blur pad gblur sigma 40, brightness -0.12, saturation 0.85
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/tools.py:219`

#### FMT-48 · تصدير كل المقاسات مع غلاف · Multi-format export + poster + GIF/WebP · 🟢 جاهز
- **ماذا / what:** From one master: a face-aware variant per aspect, a poster JPG with optional Arabic title, optional GIF and WebP.
- **كيف / how:** python tools.py export FILM --out DIR [--aspects 9:16,1:1,16:9] [--poster 2.0] [--gif] [--webp].
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/tools.py:378`

#### FMT-49 · تصدير عالي الدقة · High-resolution export 3840x2560 · 🟢 جاهز
- **ماذا / what:** Re-renders vector scenes and logos at 3840x2560 without loss; photos get a faithful enlargement.
- **كيف / how:** python studio.py SCENE --render out.png --scale 3.2; menu export_big.
- **أرقام / params:** scale 3.2 of 1200x800
- **الدليل / proof:** `kosif-one/tools/kosif-studio/studio.py:16` · `kosif-one/tools/kosif-studio/studio.py:342`

#### FMT-50 · ملاءمة اللقطة للإطار · Footage fit modes cover/contain/blur · 🟢 جاهز
- **ماذا / what:** Replacement clips are trimmed, speed-matched, set to constant fps and fitted by cover, contain or blurred background, to exactly the shot's frame count.
- **كيف / how:** shots[i].replacement.fit = 'cover'|'contain'|'blur'; mm_build._fit_filter / prep_shot.
- **الدليل / proof:** `kosif-one/tools/kosif-mimic/scripts/mm_build.py`

#### FMT-51 · قص 9:16 من المنتصف · Centre crop to 9:16 · 🟢 جاهز
- **ماذا / what:** Reframe 16:9 to vertical.
- **كيف / how:** -vf crop=ih*9/16:ih,scale=1080:1920; edl_render --ratios 9:16,1:1
- **أرقام / params:** 1080x1920
- **الدليل / proof:** `100-superskills/skills/pro-video-editor-ffmpeg/references/ffmpeg-recipes.md` · `100-superskills/skills/pro-video-editor-ffmpeg/scripts/edl_render.py:126`

#### FMT-52 · مواعيد نشر مبدئية · Default posting slots · 🟢 جاهز
- **ماذا / what:** Heuristic local times: tiktok 21:00, reels 20:00, instagram 13:00, shorts 18:00, youtube 17:00, facebook 19:00, x 12:00, linkedin 09:00, threads 12:00.
- **كيف / how:** Overridden by besttime
- **الدليل / proof:** `100-superskills/skills/kosif-social/scripts/social.py:67`

#### FMT-53 · مولّد مشروع مشهد · Scene scaffolder (2D/3D, 4 ratios) · 🟢 جاهز
- **ماذا / what:** Creates project folder with index.html (2d or 3d), DESIGN.md, STORYBOARD.md, run.md.
- **كيف / how:** python new_scene.py --name N --ratio 9:16 --dur 10 --fps 30 --kind 2d|3d
- **أرقام / params:** 9:16=1080x1920, 16:9=1920x1080, 1:1=1080x1080, 4:5=1080x1350
- **الدليل / proof:** `100-superskills/skills/claude-animation-studio/scripts/new_scene.py:14`

#### FMT-54 · مُرمّز H.264 · H.264 encoder wrapper · 🟢 جاهز
- **ماذا / what:** Pipes raw RGB frames into libx264 and fails loudly if FFmpeg exits non-zero so a broken encode never passes as a film.
- **كيف / how:** film.Encoder(out, w, h, fps, preset, crf).frame(rgb) ... close().
- **أرقام / params:** draft ultrafast/crf 23; delivery medium/crf 18; yuv420p; GOP 2*fps; +faststart
- **الدليل / proof:** `kosif-studio/film.py:38`

#### FMT-55 · تصدير SVG للرسم المتتبَّع · Vector SVG export of traced art · 🟢 جاهز
- **ماذا / what:** Writes the traced layers as one even-odd path per colour, stacked like the program, for use in any vector tool.
- **كيف / how:** vectorize.to_svg(data, path, scale).
- **أرقام / params:** scale 2 from the window, 4 from --trace
- **الدليل / proof:** `kosif-studio/vectorize.py:247` · `kosif-studio/out/aghnam_logo.svg`

#### FMT-56 · نسب العرض الجاهزة · Aspect presets · 🟢 جاهز
- **ماذا / what:** Named output sizes used across montage, tools and proplan.
- **كيف / how:** RATIOS dicts
- **أرقام / params:** 9:16 1080x1920; 16:9 1920x1080; 1:1 1080x1080; 4:5 1080x1350; 4:3 1440x1080; 21:9 2520x1080
- **الدليل / proof:** `kosif-studio/motion/tools.py:44` · `kosif-studio/motion/montage.py:57`

#### FMT-57 · حزمة التسليم · Delivery export pack · 🟢 جاهز
- **ماذا / what:** From one master: a variant per aspect (reframed in parallel), a poster JPG with optional Arabic title, optional GIF and WebP previews, and an export.json.
- **كيف / how:** python tools.py export FILM --out DIR [--aspects 9:16,1:1,16:9 --poster 2.0 --gif --webp --title '...' --mode smart --parallel 2]
- **أرقام / params:** GIF fps 12, 480 px, palettegen 160 colours, bayer dither scale 4, 8 s; WebP fps 15, 540 px, q 70, 8 s
- **الدليل / proof:** `kosif-studio/motion/tools.py:378`

#### FMT-58 · إظهار المنطقة الآمنة · Safe-area overlay toggle · 🟢 جاهز
- **ماذا / what:** Dashed overlay marks a 9:16 safe zone (inset 120/60/220 px) for platform UI bars; toggled from live controls.
- **كيف / how:** #safe checkbox
- **أرقام / params:** inset 120px 60px 220px
- **الدليل / proof:** `kosif-tool/starters/html-canvas/index.html:47`

#### FMT-59 · مواصفات المنصات · Platform encoding specs · 📦 بأمر تثبيت
- **ماذا / what:** Per-platform resolution/fps/codec table.
- **كيف / how:** Default 9:16 1080x1920 30fps H.264 High yuv420p CRF 18-20; 16:9 YouTube; 1:1/4:5 feeds.
- **أرقام / params:** AAC 48kHz 192kbps -14 LUFS
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/playbooks/render-pipeline.md:65` · `kosif-tool/playbooks/render-pipeline.md:63-67`

#### FMT-60 · إعادة تأطير ذكية للشورتس في ريزولف · Smart Reframe shorts batch (Resolve) · 📦 بأمر تثبيت
- **ماذا / what:** From a finished timeline, propose 20 short candidates with distinct hooks and exact in/out, duplicate per candidate, set custom 2160x3840 timeline before switching to portrait, run Smart Reframe per clip and inspect frames (API success ≠ good framing).
- **كيف / how:** DaVinci Resolve Studio scripting: duplicate timeline, timeline settings, TimelineItem Smart Reframe, duration marker; feasibility: 60 s short + two 15 s handles needs ≥90 s of source; verify render is truly 2160x3840.
- **أرقام / params:** 20 candidates; 60 s + 2x15 s handles
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2466-davinciresolve-youtube-shorts/SKILL.md`

#### FMT-61 · نشر الوسائط المولدة على الويب · Web delivery of generated media · 📦 بأمر تثبيت
- **ماذا / what:** Never ship raw PNG/JPEG or raw video tags.
- **كيف / how:** <picture> AVIF → WebP → JPEG, 3-5 widths, explicit width/height; LCP hero eager with fetchpriority high on 1-2 images; video muted autoplay playsinline loop with poster, WebM + H.264 fallback and a prefers-reduced-motion guard; optimizer npx sharp@0.33.5.
- **أرقام / params:** LCP ≤2.5 s; CLS <0.1; INP <200 ms
- **تثبيت / install:** `npx sharp@0`
- **الدليل / proof:** `kosif-atlas/skills/2306-generative-web-media/8855-web-optimization-pipeline` · `kosif-atlas/skills/881-codex-seo/1954-seo-image-gen`

#### FMT-62 · حاوية إرسال الوسائط عبر واتساب · WhatsApp media delivery container · 📦 بأمر تثبيت
- **ماذا / what:** Node HTTP service that links a WhatsApp account and sends text, images, videos, audio or documents (e.g. a rendered reel) to a number.
- **كيف / how:** server.mjs routes /connect, /status, /send, /send-media, /send-bundle; mimetype prefix chooses image/video/audio/document message type.
- **أرقام / params:** max media 25 MB; audio sent with ptt false (not as voice note)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-audit-studio/whatsapp-container-v2/server.mjs:9` · `kosif-audit-studio/whatsapp-container-v2/server.mjs:147` · `kosif-audit-studio/whatsapp-container-v2/package.json`

#### FMT-63 · قاعدة الكابشن المقروء على الطولي · Readable caption rule for vertical video · 📦 بأمر تثبيت
- **ماذا / what:** After any agent run on a 9:16 project, captions are forced to a phone-readable minimum.
- **كيف / how:** Wrapped AGENT.run: if aspect 9:16 and caption.size < 9 set 9.5; if no stroke set 6.
- **أرقام / params:** size >= 9.5; stroke 6
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:4614`

#### FMT-64 · مقاسات الفيديو · Aspect presets and canvas sizes · 📦 بأمر تثبيت
- **ماذا / what:** Four delivery aspects with fixed canvas sizes and an optional 1080p export scale.
- **كيف / how:** DIMS: 9:16 720x1280, 1:1 900x900, 16:9 1280x720, 4:5 864x1080; export 'res 1080' scales so the short side is 1080 (e.g. 1080x1920); auto aspect from source ratio (>1.2 -> 16:9, <0.7 -> 9:16, <0.9 -> 4:5, else 1:1).
- **أرقام / params:** 720p default; 1080p option
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:72` · `app/public/js/00_editor.js:933` · `app/public/js/60_unify.js:108`

#### FMT-65 · مشاركة ورفع للمنصات · Share sheet and upload shortcuts · 📦 بأمر تثبيت
- **ماذا / what:** Shares the rendered file through the system share sheet with caption and hashtags, or opens the TikTok, YouTube, Instagram and Facebook Reels upload pages; never posts by itself.
- **كيف / how:** share(): navigator.share({files,title,text}); upload links tiktok.com/upload, youtube.com/upload, instagram.com, facebook.com/reels/create.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/50_autoedit.js:1336`

#### FMT-66 · مواصفات التسليم MP4 · H.264 MP4 delivery spec · 📦 بأمر تثبيت
- **ماذا / what:** Final deliverable is H.264 yuv420p MP4 with faststart plus editable source, brief, storyboard and QA receipt.
- **كيف / how:** render.py flags + qa.py check; deliver per AGENTS.md step 9.
- **أرقام / params:** libx264, yuv420p, +faststart, CRF 19
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `fastify-motion-bro/scripts/render.py:42` · `fastify-motion-bro/AGENTS.md:17-18` · `fastify-motion-bro/docs/REVIEW_CHECKLIST.md:9-11`

#### FMT-67 · إخراج HDR · HDR 10-bit H.265 output · 📦 بأمر تثبيت
- **ماذا / what:** Preserve BT.2020 PQ/HLG sources into 10-bit HEVC MP4; verify with ffprobe.
- **كيف / how:** render --hdr (auto when sources HDR); not combinable with --resolution.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/guides/hdr.mdx`

#### FMT-68 · تصيير 4K · 4K supersampling · 📦 بأمر تثبيت
- **ماذا / what:** Render existing 1080p comp at 4K via deviceScaleFactor whole multiple.
- **كيف / how:** render --resolution landscape-4k; aspect must match.
- **أرقام / params:** 3840x2160
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/guides/4k-rendering.mdx`

#### FMT-69 · مخرجات شفافة · Alpha outputs · 📦 بأمر تثبيت
- **ماذا / what:** Transparent WebM (VP9) and MOV ProRes 4444; png-sequence RGBA.
- **كيف / how:** render --format webm|mov|png-sequence; --vp9-cpu-used -8..8.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/packages/cli.mdx`

#### FMT-70 · شارات المتاجر · Store Badge Lockup · 📦 بأمر تثبيت
- **ماذا / what:** Short headline above equal-size App Store and Google Play badges as a mobile end card.
- **كيف / how:** Install with `npx hyperframes add store-badge-lockup` (copies to compositions/components/store-badge-lockup.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless C…
- **أرقام / params:** showApple/showGoogle yes|no; vars: headline=Get the app; showApple=yes[yes|no]; showGoogle=yes[yes|no]
- **تثبيت / install:** `npx hyperframes add store-badge-lockup` (copies to compositions/components/store-badge-lockup`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/store-badge-lockup/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/store-badge-lockup/store-badge-lockup.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/store-badge-lockup.mdx`

#### FMT-71 · بطاقة متابعة · X Follow Card · 📦 بأمر تثبيت
- **ماذا / what:** Social follow card with avatar, handle and follower count motion.
- **كيف / how:** Install with `npx hyperframes add x-follow-card` (copies to compositions/components/x-follow-card.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium fr…
- **تثبيت / install:** `npx hyperframes add x-follow-card` (copies to compositions/components/x-follow-card`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/x-follow-card/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/x-follow-card/x-follow-card.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/x-follow-card.mdx`

#### FMT-72 · متابعة إنستغرام · Instagram Follow · 📦 بأمر تثبيت
- **ماذا / what:** Animated Instagram-style follow overlay with profile card and follow button.
- **كيف / how:** Install with `npx hyperframes add instagram-follow` (copies the full composition to compositions/instagram-follow.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: inline SVG, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 1080x1920; 4.5 s; Google Fonts: DM Sans; 1080x1920; duration 4.5 s
- **تثبيت / install:** `npx hyperframes add instagram-follow` (copies the full composition to compositions/instagram-follow`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/instagram-follow/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/instagram-follow/instagram-follow.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/instagram-follow.mdx`

#### FMT-73 · إشعار ماك · macOS Notification · 📦 بأمر تثبيت
- **ماذا / what:** Animated macOS-style notification banner with app icon and message.
- **كيف / how:** Install with `npx hyperframes add macos-notification` (copies the full composition to compositions/macos-notification.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: inline SVG, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 5 s; Google Fonts: Inter; 1920x1080; duration 5 s
- **تثبيت / install:** `npx hyperframes add macos-notification` (copies the full composition to compositions/macos-notification`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/macos-notification/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/macos-notification/macos-notification.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/macos-notification.mdx`

#### FMT-74 · منشور ريديت · Reddit Post Card · 📦 بأمر تثبيت
- **ماذا / what:** Animated Reddit-style post card overlay with upvotes and comments.
- **كيف / how:** Install with `npx hyperframes add reddit-post` (copies the full composition to compositions/reddit-post.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: inline SVG, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 5 s; Google Fonts: DM Sans; 1920x1080; duration 5 s
- **تثبيت / install:** `npx hyperframes add reddit-post` (copies the full composition to compositions/reddit-post`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/reddit-post/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/reddit-post/reddit-post.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/reddit-post.mdx`

#### FMT-75 · بطاقة سبوتيفاي · Spotify Now Playing · 📦 بأمر تثبيت
- **ماذا / what:** Animated Spotify-style now-playing card with album art and progress bar.
- **كيف / how:** Install with `npx hyperframes add spotify-card` (copies the full composition to compositions/spotify-card.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: inline SVG, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 1080x1920; 5 s; Google Fonts: Inter; 1080x1920; duration 5 s
- **تثبيت / install:** `npx hyperframes add spotify-card` (copies the full composition to compositions/spotify-card`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/spotify-card/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/spotify-card/spotify-card.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/spotify-card.mdx`

#### FMT-76 · متابعة تيك توك · TikTok Follow · 📦 بأمر تثبيت
- **ماذا / what:** Animated TikTok-style follow overlay with profile card and follow button.
- **كيف / how:** Install with `npx hyperframes add tiktok-follow` (copies the full composition to compositions/tiktok-follow.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: inline SVG, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 1080x1920; 4.5 s; Google Fonts: DM Sans; 1080x1920; duration 4.5 s
- **تثبيت / install:** `npx hyperframes add tiktok-follow` (copies the full composition to compositions/tiktok-follow`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/tiktok-follow/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/tiktok-follow/tiktok-follow.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/tiktok-follow.mdx`

#### FMT-77 · منشور إكس · X Post Card · 📦 بأمر تثبيت
- **ماذا / what:** Animated X/Twitter-style post card with engagement metrics.
- **كيف / how:** Install with `npx hyperframes add x-post` (copies the full composition to compositions/x-post.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: inline SVG, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 5 s; Google Fonts: Inter; 1920x1080; duration 5 s
- **تثبيت / install:** `npx hyperframes add x-post` (copies the full composition to compositions/x-post`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/x-post/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/x-post/x-post.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/x-post.mdx`

#### FMT-78 · تعليقات يوتيوب · Comment Cards · 📦 بأمر تثبيت
- **ماذا / what:** Social comments typing over footage: avatar pop, username/time, per-character typewriter, likes row.
- **كيف / how:** Install with `npx hyperframes add yt-comment-card` (copies the full composition to compositions/yt-comment-card.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: inline SVG, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 8 s; 1920x1080; duration 8 s
- **تثبيت / install:** `npx hyperframes add yt-comment-card` (copies the full composition to compositions/yt-comment-card`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/yt-comment-card/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/yt-comment-card/yt-comment-card.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/yt-comment-card.mdx`

#### FMT-79 · شريط اشتراك يوتيوب · YouTube Lower Third · 📦 بأمر تثبيت
- **ماذا / what:** YouTube-style subscribe lower third with avatar and channel info.
- **كيف / how:** Install with `npx hyperframes add yt-lower-third` (copies the full composition to compositions/yt-lower-third.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: inline SVG, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** DM Sans; elastic.out(1, 0.4); 4.5 s; Google Fonts: DM Sans; 1920x1080; duration 4.5 s
- **تثبيت / install:** `npx hyperframes add yt-lower-third` (copies the full composition to compositions/yt-lower-third`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/yt-lower-third/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/yt-lower-third/yt-lower-third.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/yt-lower-third.mdx`

#### FMT-80 · تعبئة الفيديو العمودي · Vertical Media Filler · 📦 بأمر تثبيت
- **ماذا / what:** Portrait media in a 16:9 frame via blurred-scale, mirror or copy side fills, grid texture and contrast lift.
- **كيف / how:** Install with `npx hyperframes add yt-vertical-fill` (copies the full composition to compositions/yt-vertical-fill.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** images inside block; live footage stays in host; 1920x1080; duration 8 s
- **تثبيت / install:** `npx hyperframes add yt-vertical-fill` (copies the full composition to compositions/yt-vertical-fill`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/yt-vertical-fill/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/yt-vertical-fill/yt-vertical-fill.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/yt-vertical-fill.mdx`

#### FMT-81 · اشتقاق أبعاد الإطار من منصة النشر · Aspect derivation from destination · 📦 بأمر تثبيت
- **ماذا / what:** Canvas size is derived from where the video plays rather than asked directly.
- **كيف / how:** In the brief: social feed -> 1080x1080; TikTok/Reels/Shorts -> 1080x1920; YouTube/website/desktop -> 1920x1080; state the derivation as a receipt.
- **أرقام / params:** 1080x1080 | 1080x1920 | 1920x1080
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes/references/brief-contract.md`

#### FMT-82 · التصيير إلى صيغ متعددة · Render to MP4/WebM/MOV/GIF/PNG/HLS · 📦 بأمر تثبيت
- **ماذا / what:** Deterministic frame capture + FFmpeg encode with quality tiers and formats; WebM/MOV keep transparency; GIF two-pass palette; HLS segments; supersampled 4K via deviceScaleFactor; HDR/SDR forcing; GPU encode; Docker reproducible mode.
- **كيف / how:** npx hyperframes render [--quality draft|looks|delivery] [--fps 24|30|60] [--format mp4|webm|mov|gif|png-sequence|hls] [--resolution landscape-4k] [--crf 0-51 | --video-bitrate 10M] [--hdr|--sdr] [--workers auto] [--docker] [--gpu] [--variables JSON] [--strict].
- **أرقام / params:** default 30 fps; looks = CRF 16 standard preset; delivery = high; gif fps <= 30 (15 preferred); hls 4 s segments; worker ~256 MB each
- **تثبيت / install:** `npx hyperframes render [--quality draft|looks|delivery] [--fps 24|30|60] [--format mp4|webm|mov|gif|png-sequence|hls] [--resolution landscape-4k] [--crf 0-51 | --video-bitrate 10M] [--hdr|--sdr] [--workers auto] [--docker] [--gpu] [--variables JSON] [--strict]`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-cli/references/preview-render.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-cli/SKILL.md` · `kosif-one/vendor/hyperframes/packages/cli/src/commands/render.ts`

#### FMT-83 · تصيير دفعي بالمتغيرات · Variable-driven batch render · 📦 بأمر تثبيت
- **ماذا / what:** Render many personalized outputs from one template by rows of variable values.
- **كيف / how:** npx hyperframes render --batch rows.json --output 'renders/{name}.mp4'; cloud/lambda/cloudrun render-batch with JSONL.
- **تثبيت / install:** `npx hyperframes render --batch rows`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-cli/references/compare-and-batch.md` · `kosif-one/vendor/hyperframes/packages/cli/src/commands/batchRender.ts`

#### FMT-84 · عرض تقديمي تفاعلي · Slideshow / interactive deck · 📦 بأمر تثبيت
- **ماذا / what:** Navigable deck (not an MP4) from scene compositions + one JSON island manifest per composition: SlideRef, fragments (reveal hold points), hotspots and slide sequences for branching, presenter mode with editable speaker notes, media cleanup on slide exit, global mute, Three.js optional, page-to-deck …
- **كيف / how:** slideshow/SKILL.md schema (SlideshowManifest, SlideRef, SlideHotspot, SlideSequence) + references/standalone-harness.md parent wrapper and postMessage bootstrap.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/slideshow/SKILL.md` · `kosif-one/vendor/hyperframes/skills/slideshow/references/standalone-harness.md`

#### FMT-85 · تصدير المنصات · Per-platform export · 📦 بأمر تثبيت
- **ماذا / what:** Platform copies.
- **كيف / how:** kmotion platforms FILM --to tiktok,reels,...
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/operating-manual.md` · `100-superskills/skills/kosif-montage-motion/scripts/platforms.py`

#### FMT-86 · أنماط الملاءمة · Clip fit modes · 📦 بأمر تثبيت
- **ماذا / what:** cover / contain / blur background.
- **كيف / how:** clips[].fit
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/timeline-schema.md`

#### FMT-87 · تكامل: slack-gif-creator skill · Integration: slack-gif-creator skill · 📦 بأمر تثبيت
- **ماذا / what:** Catalogued skill/MCP/library (link only; not installed here).
- **كيف / how:** see official setup
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog-2.md`

#### FMT-88 · كاروسيل عربي · Arabic carousel renderer (PNG + PDF) · 📦 بأمر تثبيت
- **ماذا / what:** Renders Instagram/TikTok/LinkedIn carousels with correct Arabic shaping and wrap, fallback fonts for Latin/@handles, a PDF and a contact sheet.
- **كيف / how:** python social.py carousel spec.json --out DIR; spec {platform, size, brand{bg,fg,accent,handle,font,font_bold}, slides[{title, body, kicker, image}]}.
- **أرقام / params:** titles <= 4 lines; size 1080x1350 (or 1080x1440 3:4 grid)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-social/SKILL.md` · `kosif-one/tools/kosif-social/examples/carousel.json`

#### FMT-89 · تصدير 4K وتكبير أمين للصور النقطية · 4K export and faithful raster enlargement · 📦 بأمر تثبيت
- **ماذا / what:** Vector pictures (scenes, SVG, traced logos) are re-rendered at 3840x2560; raster results are kept exact and also enlarged by an integer Lanczos factor with a gentle unsharp mask, colours untouched.
- **كيف / how:** Studio ⤢ button / export_big(); enlarge(im, target=3840) uses cv2.resize INTER_LANCZOS4 then addWeighted(1.35, blur, -0.35); runner --export at --scale 3.2.
- **أرقام / params:** 3840x2560 (scale 3.2, ss=2); integer k = round(3840/max side); unsharp sigma 0.6*k
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/studio.py:141` · `kosif-studio/studio.py:1287` · `kosif-studio/out/dragon_girl_3840x2560.png`

#### FMT-90 · أوضاع التصدير · Export modes · 📦 بأمر تثبيت
- **ماذا / what:** From one picture the studio delivers: PNG at window size, <name>_exact.png identical to the source, 3840x2560 vector render or integer Lanczos enlargement, traced SVG, a standalone Python program, the data-only image code, and an MP4 of the drawing.
- **كيف / how:** Toolbar التصدير group: 💾 PNG (Ctrl+S), ⤢ دقة عالية, 📤 كود الصورة, 🎬 فيلم; CLI equivalents in studio.py/film.py/to_python.py.
- **أرقام / params:** 3840x2560; MP4 30 fps H.264
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/studio.py:1275` · `kosif-studio/studio.py:1287` · `kosif-studio/studio.py:1245`

#### FMT-91 · إعلان متجر · Style: E-commerce ad (ecommerce-ad) · 📦 بأمر تثبيت
- **ماذا / what:** Store product ad: hero product, price card, feature beats and one CTA.
- **كيف / how:** Ad structure hook 0-1.5s, promise, 2-4 feature beats 2-3s, price card spring d14 s180, CTA 2-3s, logo 1-1.5s. Scaffold: python3 tools/kosif.py scaffold ecommerce-ad <dir>.
- **أرقام / params:** product >=40% frame height
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `style:ecommerce-ad` · `kosif-tool/playbooks/ads.md`

#### FMT-92 · إعلان إطلاق منتج · Style: Product launch (product) · 📦 بأمر تثبيت
- **ماذا / what:** Tech product launch promo: huge words, product hero, features, CTA.
- **كيف / how:** Ads structure; product push 3-5%, light sweep 800ms; feature beats 300-450ms ease-out quint. Scaffold: python3 tools/kosif.py scaffold product <dir>.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `style:product` · `kosif-tool/playbooks/ads.md`

#### FMT-93 · إعلانات · Category: Ads · 📦 بأمر تثبيت
- **ماذا / what:** Capability family 'ads' (6 catalog entries) with a dedicated bilingual playbook of timings and recipes.
- **كيف / how:** Read playbooks/ads.md (visual grammar, motion mechanics, scene recipes, QA); build in starters/html-canvas or starters/remotion; filter catalog with python3 tools/kosif.py list --category ads.
- **أرقام / params:** hook 0-1.5s; features 2-3s each; CTA 2-3s; logo 1-1.5s; TikTok 15-30s cuts 1-2s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/playbooks/ads.md` · `kosif-tool/catalog/categories.json` · `kosif-tool/catalog/meta.json`

#### FMT-94 · قص التركيز للجوال · Mobile focus crop · 📦 بأمر تثبيت
- **ماذا / what:** 16:9 clips cropped vertical; per-stop focus % interpolated into --focus-x.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/mcp-higgsfield-landing/src/scripts/world.ts:86`

#### FMT-95 · نسخ متعددة المقاسات للمنصات · Multi-ratio social variations · 🔑 مفتاح/خدمة
- **ماذا / what:** From one source image produce platform ratios with subject-aware cropping or AI canvas expansion, showing a 3-crop preview before the full set and reusing those crops; video is resized only (no smart reframe) in that connector.
- **كيف / how:** Locally: compute subject box (saliency/face detection) and crop or extend with blurred/mirrored fill per ratio; the Adobe Firefly connector path needs an Adobe account.
- **أرقام / params:** 3-crop preview
- **الدليل / proof:** `kosif-atlas/skills/103-adobe-for-creativity/232-adobe-create-social-variations/SKILL.md`

#### FMT-96 · عمليات الفيديو عبر روابط Cloudinary · Cloudinary video URL operations · 🔑 مفتاح/خدمة
- **ماذا / what:** Server-side video derivatives addressed by URL: trim with so_/eo_/du_, remove audio (ac_none) for autoplay, cap size (c_limit,h_720), set fps_, concatenate clips or images (fl_splice, image duration du_), animated WebP previews (f_auto:animated, or fl_animated,fl_awebp with a WebP signal, e_loop); a…
- **كيف / how:** Needs a Cloudinary account; e.g. du_5/vc_auto/f_auto:video/q_auto for a 5 s preview, ac_none/vc_h264/f_mp4/q_auto for silent autoplay.
- **الدليل / proof:** `kosif-atlas/skills/1119-cloudinary/2560-cloudinary-transformations/SKILL.md` · `kosif-atlas/skills/1119-cloudinary/2560-cloudinary-transformations/references/video-transformations.md`

#### FMT-97 · إعدادات جاهزة لكل استخدام · Use-case presets for Gemini still generation · 🔑 مفتاح/خدمة
- **ماذا / what:** Pre-mapped ratio/size per asset type.
- **كيف / how:** OG/social 16:9 at 1K; blog hero 16:9 at 2K; schema/product 4:3 at 1K-2K; social square 1:1 at 1K; infographic 2:3 at 4K; favicon 1:1 at 512; Pinterest 2:3 at 2K; drafts gemini-2.5-flash-image at 512.
- **الدليل / proof:** `kosif-atlas/skills/881-codex-seo/1954-seo-image-gen`

#### FMT-98 · عناوين خطاف وبوست النشر · Hook titles and social post pack · 🔑 مفتاح/خدمة
- **ماذا / what:** Suggests 5 Arabic hook titles (<= 6 words, no clickbait lies) and writes TikTok/Instagram/YouTube Shorts text with hashtags, cover text and alt text, checking platform limits.
- **كيف / how:** btnHooks (quick task); postPack JSON {tiktok{caption<=150, 3-5 tags}, instagram{2-4 lines CTA, 5-8 tags, firstComment}, youtube{title<=70, 2-3 lines, 5-8 tags}, coverText 2-4 words, altText}; POST_LIMITS tiktok 2200, instagram 2200, ytTitle 100, igTags 30.
- **الدليل / proof:** `app/public/js/00_editor.js:1500` · `app/public/js/00_editor.js:2079` · `app/public/js/00_editor.js:2080`

#### FMT-99 · النشر برابط ثابت خاص · Publish to a stable private link · 🔑 مفتاح/خدمة
- **ماذا / what:** Uploads the project to a hosted, private-by-default URL; republishing updates the same link.
- **كيف / how:** npx hyperframes publish [dir].
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-cli/references/preview-render.md`

#### FMT-100 · حزم Custom GPT ومشروع Claude · Custom GPT / Claude Project packs · 🔑 مفتاح/خدمة
- **ماذا / what:** Ready instructions (3,999/8,000 chars), 12 knowledge files (concatenated skill docs), 4 Arabic conversation starters (one asks for a full cinematic package), OpenAPI for Actions.
- **كيف / how:** Paste chatgpt/custom-gpt/instructions.md; upload knowledge/*.md; import openapi.json with Bearer token; Claude Project uses claude/project-instructions.md.
- **أرقام / params:** Actions profile 29 tools; MCP 65
- **الدليل / proof:** `kosif-one/tools/kosif-omni/chatgpt/custom-gpt/instructions.md` · `kosif-one/tools/kosif-omni/chatgpt/custom-gpt/SETUP.md` · `kosif-one/tools/kosif-omni/chatgpt/custom-gpt/conversation-starters.md`

#### FMT-101 · سلسلة عمودية 9:16 · Native 9:16 portrait chain · 🔑 مفتاح/خدمة
- **ماذا / what:** Optional portrait renders of every clip wired as clipMobile/connectorsMobile (~2x cost).
- **كيف / how:** Pipeline 6b.
- **أرقام / params:** 720w, -g 4
- **الدليل / proof:** `kosif-one/vendor/scroll-world/skills/scroll-world/SKILL.md`

#### FMT-102 · تنسيق مربع للخلاصة · Square feed format · 👁 شوهد في فيديو
- **ماذا / what:** 1080x1080, captions top, readable without sound
- **الدليل / proof:** `style:pm-cansincengiz-me-cf68dd`

#### FMT-103 · صيغة إعلان عمودي · Vertical ad format · 👁 شوهد في فيديو
- **ماذا / what:** 9:16 with headline in top third
- **الدليل / proof:** `style:pm-francoxavier33-d2dfd2`

#### FMT-104 · إطار سينمائي عريض · Cinematic 2.35:1 canvas · 👁 شوهد في فيديو
- **ماذا / what:** render at 1920x816 directly (or letterbox inside 16:9); compose with subjects on thirds and large negative space
- **أرقام / params:** 1920x816 @60fps
- **الدليل / proof:** `style:pm-kamstudiolabs-0b0824`

#### FMT-105 · سؤال جذب مع عدّاد حي · Hook question + live counter overlay · 👁 شوهد في فيديو
- **ماذا / what:** fixed bold question in top safe zone, uppercase counter beneath updating on events, tiny instruction caption in bottom safe zone, 'sound on' pill for first 3 s
- **أرقام / params:** top 12-20% of 9:16 frame
- **الدليل / proof:** `style:pm-kantamk-61f410`

#### FMT-106 · أشرطة سينمائية سوداء · Letterbox bars · 👁 شوهد في فيديو
- **ماذا / what:** black bars top and bottom to get ~2.35:1 within 16:9
- **أرقام / params:** bars ≈ 12% h each
- **الدليل / proof:** `style:pm-maxalexweber-67688b`

#### FMT-107 · بطاقة ختام بزر التحميل · App-store end card · 👁 شوهد في فيديو
- **ماذا / what:** app icon, wordmark, descriptor line, dark rounded CTA pill and a row of features separated by red dots; small 'BY …' credit at bottom
- **أرقام / params:** 9:16, CTA pill 24 px radius
- **الدليل / proof:** `style:pm-mehul4795-4a7007`

#### FMT-108 · إعلان بصيغة مربعة · Square format promo · 👁 شوهد في فيديو
- **ماذا / what:** 1:1 layout with top-left text block for social feeds
- **أرقام / params:** 720x720
- **الدليل / proof:** `style:pm-rammanq-f5a90f`

#### FMT-109 · إطار سينمائي بأشرطة سوداء · Cinematic letterbox · 👁 شوهد في فيديو
- **ماذا / what:** Render a 2.35:1 picture inside 16:9 with pure black bars; place subtitles inside the lower bar
- **أرقام / params:** bar height ~12.5% each at 1080p
- **الدليل / proof:** `style:pm-rebutonepress-810f78`

#### FMT-110 · أشرطة سينمائية 2.39:1 · Cinematic letterbox 2.39:1 · 👁 شوهد في فيديو
- **ماذا / what:** render 16:9 then ffmpeg drawbox top/bottom black bars height = (H - W/2.39)/2
- **أرقام / params:** 720p -> 92px bars
- **الدليل / proof:** `style:pm-theparuchh-6e08c3`

#### FMT-111 · المنطقة الآمنة العمودية · Vertical safe area · 📄 موصوف
- **ماذا / what:** 1080x1920 canvas with ~900x1350 usable area for platform UI.
- **كيف / how:** layout guides
- **أرقام / params:** 1080x1920; usable ~900x1350
- **الدليل / proof:** `100-superskills/skills/reels-shorts-factory/references/sources.md:19` · `kosif-tool/playbooks/kinetic-type.md:19`

#### FMT-112 · تصدير فيديو شفاف · Transparent video export · 📄 موصوف
- **ماذا / what:** Render overlays with alpha for use in other editors or browsers.
- **كيف / how:** ProRes 4444: --image-format=png --pixel-format=yuva444p10le --codec=prores --prores-profile=4444 (.mov, for NLEs); WebM VP9: --image-format=png --pixel-format=yuva420p --codec=vp9 (.webm, for web). HyperFrames: render --format webm.
- **أرقام / params:** yuva444p10le / yuva420p
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10438-remotion-render/transparent-videos.md` · `kosif-atlas/skills/2702-hyperframes/10379-hyperframes-cli/SKILL.md`

#### FMT-113 · نسخة عمودية فوق خلفية ضبابية · Vertical cut over blurred fill · 📄 موصوف
- **ماذا / what:** Make 9:16 from 16:9 by placing the full frame across the middle over a blurred, darkened, scaled copy of itself (or an action-following crop), never a fixed center crop.
- **كيف / how:** ffmpeg filter: split; [bg] scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20,eq=brightness=-0.15; [fg] scale=1080:-2; overlay=(W-w)/2:(H-h)/2.
- **أرقام / params:** 1080x1920
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3903-video/references/TRAILER.md` · `kosif-atlas/skills/1511-homie/3903-video/references/DELIVERY.md`

#### FMT-114 · قاعدة الترجمة للتشغيل الصامت · Muted-autoplay captions rule · 📄 موصوف
- **ماذا / what:** Social feeds autoplay muted, so key words must be burned into the picture or shipped as a VTT track.
- **كيف / how:** Kinetic type for key phrases or captions.vtt sidecar; keep under platform size caps.
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3903-video/references/DELIVERY.md`

#### FMT-115 · إعدادات ترميز FFmpeg · FFmpeg encoding presets & HLS · 📄 موصوف
- **ماذا / what:** Encoding recipes: GPU NVENC quality flags, aligned keyframes for streaming, multi-rendition HLS, loudness normalization.
- **كيف / how:** NVENC: -c:v h264_nvenc -preset p7 -tune hq -rc vbr -cq 19; HLS: split to 1080/720/480 at 5000k/2800k/1400k, -g 60 -keyint_min 60 -sc_threshold 0, -hls_time 4; audio aac 128k.
- **أرقام / params:** cq 19; GOP 60; 5000/2800/1400k
- **الدليل / proof:** `kosif-atlas/skills/235-mas-video-lab/754-ffmpeg/SKILL.md`

#### FMT-116 · وضعا كثافة العرض · Presentation density modes · 📄 موصوف
- **ماذا / what:** Speaker-led content wants one idea per frame with huge type; reading-first content can hold more structure. Split rather than shrink.
- **كيف / how:** Ask whether the piece is narrated (low density) or read silently (higher density) and size type accordingly.
- **أرقام / params:** speaker-led 1-3 bullets; reading-first 4-8 bullets or 4-6 cards
- **الدليل / proof:** `kosif-atlas/skills/880-superloopy/1944-superloopy-slides`

#### FMT-117 · وصفة فيديو الميزة وإعادة التأطير · Feature video recipe and multi-ratio reframing · 📄 موصوف
- **ماذا / what:** Write 'the user does X; the product visibly does Y'; capture with clean test data and pre/post roll; cut waiting only if honest; end on the finished state; reframe each ratio against the real UI and make a poster per ratio.
- **كيف / how:** Playwright capture or designed port; ffmpeg crops/scales per ratio; never rely on automatic centre crop.
- **أرقام / params:** 16:9, 4:5, 9:16, 1:1
- **الدليل / proof:** `kosif-atlas/skills/101-video-skills/215-feature-video`

#### FMT-118 · بريف الثمبنيل: ثلاث أفكار واختبار A/B · Thumbnail creative brief (3 concepts + A/B) · 📄 موصوف
- **ماذا / what:** Thumbnail work delivers three concepts (layout, expression direction, text placement, colour treatment, brand elements), a recommended one, background-only image prompts (real face composited later), shooting notes and an optional A/B plan.
- **كيف / how:** Shooting notes: slightly below eye level, medium close-up, single key light off-axis; A/B winner after 48 h by CTR vs channel average; vary one element per test. Compose final in HTML/CSS and screenshot with Playwright at 1280x720.
- **أرقام / params:** 3 concepts; 1280x720; 48 h test window
- **الدليل / proof:** `kosif-atlas/skills/3067-youtube/13228-creator-thumbnail-agent/SKILL.md` · `kosif-atlas/skills/1817-youtube-strategy/4868-yt-packaging/SKILL.md`

#### FMT-119 · حدود كلمات نص الثمبنيل · Thumbnail text word limits · 📄 موصوف
- **ماذا / what:** Thumbnail copy is extremely short: 1-3 words is the packaging norm, 4 is a hard ceiling in most sources (one source allows 7 as absolute maximum); one accent colour per thumbnail; must read in under 1 s at mobile size.
- **كيف / how:** Typeset in the composition with the brand display face; test at 150-200 px width; for Arabic count words, not letters, and prefer heavy weights with generous tracking-free shaping.
- **أرقام / params:** 1-3 words ideal; 4 max (7 absolute in one source); 1 accent colour
- **الدليل / proof:** `kosif-atlas/skills/1520-digital-marketing-pro/4132-video-packaging/SKILL.md` · `kosif-atlas/skills/3067-youtube/13228-creator-thumbnail-agent/SKILL.md` · `kosif-atlas/skills/1817-youtube-strategy/4868-yt-packaging/SKILL.md`

#### FMT-120 · قاعدة تكامل العنوان والغلاف · Title/thumbnail pairing rule · 📄 موصوف
- **ماذا / what:** Title and thumbnail do different jobs: the title carries context and searchable keywords, the thumbnail carries the tension a human reacts to; any thumbnail word that also appears in the title is wasted and rejected.
- **كيف / how:** Check word-by-word overlap programmatically (simple set intersection); titles <=60 characters with the important words in the first ~40; generate 3 pairs at different angles (curiosity/benefit/identity) and vary only one element when A/B testing.
- **أرقام / params:** title <=60 chars; key words in first 40; 0 shared words
- **الدليل / proof:** `kosif-atlas/skills/1520-digital-marketing-pro/4132-video-packaging/SKILL.md` · `kosif-atlas/skills/1817-youtube-strategy/4868-yt-packaging/SKILL.md`

#### FMT-121 · فيزياء هيكلة الإعلانات حسب الخانة · Ad-slot structure physics · 📄 موصوف
- **ماذا / what:** Paid video slots impose structure: 6 s bumper carries ONE message with the brand visible by second 2; 15 s skippable must land hook and core message before the skip button at 5 s; 30 s spot has room for one arc but pays off early and again late; UGC-style looks native yet is disclosed as an ad.
- **كيف / how:** Template each ad length as a fixed timeline grid in the composition (markers at 2 s, 5 s, end card) and verify message placement in rendered stills at those timestamps.
- **أرقام / params:** bumper 6 s (brand by 2 s); skippable 15 s (skip at 5 s); spot 30 s
- **الدليل / proof:** `kosif-atlas/skills/1520-digital-marketing-pro/4133-video-script/SKILL.md`

#### FMT-122 · تخطيط نسخ مختصرة ومطولة · Alternate-cut planning · 📄 موصوف
- **ماذا / what:** From one shoot/script, specify which sections to drop or expand for shorter and longer versions (e.g. 60 s, 30 s, 15 s cut-downs).
- **كيف / how:** Tag each beat with priority (core/optional) in the timeline data so cut-downs are generated by filtering beats and re-flowing the timeline.
- **الدليل / proof:** `kosif-atlas/skills/1520-digital-marketing-pro/4133-video-script/SKILL.md`

#### FMT-123 · المناطق الآمنة للفيديو العمودي · Vertical 9:16 safe zones · 📄 موصوف
- **ماذا / what:** On 1080x1920 the app UI covers the edges: keep critical content inside roughly 900x1350 centered and shifted upward.
- **كيف / how:** Conservative margins: top 250 px, bottom 320 px, right 120 px, left 60 px (one source: avoid 250 top + 400 bottom for IG story/reel covers; another: UI covers bottom 20% and right 12%). Draw guides first in the composition and screenshot-check that nothing critical falls outside. Values change with app updates.
- **أرقام / params:** 1080x1920; safe ~900x1350; margins T250 B320 R120 L60
- **الدليل / proof:** `kosif-atlas/skills/2976-pwdev-social-media/12592-story-reels/SKILL.md` · `kosif-atlas/skills/2976-pwdev-social-media/12587-format-specs/SKILL.md` · `kosif-atlas/skills/1567-tonone/4428-form-social/SKILL.md`

#### FMT-124 · بنية الكاروسيل وحدوده · Carousel structure and limits · 📄 موصوف
- **ماذا / what:** Slide 1 is the only slide everyone sees and must work alone as the hook; slide 2 bridges hook to value; one point per slide; last slide recaps + CTA; under 5 slides it should be a single post.
- **كيف / how:** Instagram 5 min / 8-10 ideal, LinkedIn PDF 7-12, Facebook 5-8, all 1080x1350; title <=8 words, body <=30 words; reserve 80 px outer edge for swipe/pager; keep one progress signal (counter, bar, or colour progression); build one slide component with variants (cover, content, data, contrast, closing). The same slide system can be animated into a 9:16 reel, one slide per beat.
- **أرقام / params:** 1080x1350; title<=8w; body<=30w; 80 px edge
- **الدليل / proof:** `kosif-atlas/skills/2976-pwdev-social-media/12581-carousel-builder/SKILL.md`

#### FMT-125 · اختيار المقاس حسب الهدف · Format-by-goal chooser · 📄 موصوف
- **ماذا / what:** Pick canvas by objective: maximum feed surface 4:5 (1080x1350); sequential teaching carousel 4:5; short-video reach 9:16 (1080x1920); link preview 1.91:1 (1200x630); Pinterest search 2:3 (1000x1500).
- **كيف / how:** Encode as presets in the scaffold so each composition declares its target; dimensions are stable while safe zones are not.
- **أرقام / params:** 4:5 1080x1350; 9:16 1080x1920; 1.91:1 1200x630; 2:3 1000x1500
- **الدليل / proof:** `kosif-atlas/skills/2976-pwdev-social-media/12587-format-specs/SKILL.md`

#### FMT-126 · جدول مقاسات المنصات وهوامشها · Social canvas and safe-margin table · 📄 موصوف
- **ماذا / what:** Reference sizes with text-safe margins for common surfaces.
- **كيف / how:** LinkedIn post 1200x627 (100 px margins); X card 1200x675 (80 px); IG square 1080x1080 (108 px, 10%); IG landscape 1080x566 (80 px); story/reel cover 1080x1920 (avoid 250 top/400 bottom); FB post 1200x630 (100 px); YouTube thumbnail 1280x720 (72 px); channel art 2560x1440 (safe 1546x423 centered); display 300x250, 728x90, 160x600.
- **أرقام / params:** see how
- **الدليل / proof:** `kosif-atlas/skills/1567-tonone/4428-form-social/SKILL.md`

#### FMT-127 · خريطة تفتيت المحتوى · Content atomization map · 📄 موصوف
- **ماذا / what:** One long source (video, podcast, webinar, article) becomes a full video plus 3-5 short clips and platform-native variants; releases are staggered, never same-day everywhere.
- **كيف / how:** Blog-to-video mapping: H2s -> chapters, stats/quotes -> pull-quote overlays on B-roll, step sections -> tutorial segments, conclusion -> short clip. Every derivative must pass a standalone test: its own hook and payoff, no 'as discussed in...' context debt; list what was cut and why.
- **أرقام / params:** 3-5 clips per long piece; 10+ derivatives target
- **الدليل / proof:** `kosif-atlas/skills/192-marketing-skills/617-video-content-strategist/SKILL.md` · `kosif-atlas/skills/1520-digital-marketing-pro/4013-content-repurpose/SKILL.md` · `kosif-atlas/skills/2264-creator-economy-operations/8628-plan-content-and-audience-growth/SKILL.md`

#### FMT-128 · استخراج دفعة شورتس عمودية من مونتاج طويل · Batch vertical shorts from a long edit · 📄 موصوف
- **ماذا / what:** Propose ~20 short candidates with distinct hooks and exact in/out timecodes from a finished long timeline, check feasibility (a 60 s short with two 15 s handles needs >=90 s), then create portrait versions with subject-aware reframing and inspect frames.
- **كيف / how:** Resolve: duplicate timeline, custom 2160x3840, Smart Reframe, duration marker, render private. Local: ffmpeg crop/scale per candidate with face/subject tracking (or full frame over blurred fill), never pad with black or silently shorten.
- **أرقام / params:** 20 candidates; 2160x3840; handles 2x15 s
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2466-davinciresolve-youtube-shorts/SKILL.md`

#### FMT-129 · مواصفات التريلر حسب المنصة · Trailer platform targets · 📄 موصوف
- **ماذا / what:** X/Bluesky/Mastodon 30-45 s, 16:9 1080p60, autoplays muted so hook within 2 s and captions carry the message; YouTube 30-90 s; Shorts/TikTok/Reels 15-45 s native 9:16 with big subject; README/Discord GIF loops 4-8 s at 640 px, 20 fps, under 15 MB; store pages 60-120 s.
- **كيف / how:** Render native 9:16 rather than cropping 16:9 when possible.
- **أرقام / params:** 30-45 s; 30-90 s; 15-45 s; GIF 4-8 s 640w 20 fps <15 MB
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4173-game-trailer/references/concept-and-music.md`

#### FMT-130 · صورة غلاف تعتمد على الطباعة · Typography-first OG/cover image · 📄 موصوف
- **ماذا / what:** Covers and link previews as self-contained HTML+CSS screenshots at exactly 1200x630: title shortened to about 40 characters, at most two fonts, decorative shapes in CSS only, direction by topic (technical = dark with accent gradients; tutorial = light and structured; conceptual = gradient centred ty…
- **كيف / how:** Playwright screenshot of a fixed-size body with overflow hidden; same approach produces 1280x720 thumbnails and 1080x1350 posts.
- **أرقام / params:** 1200x630; title <=40 chars; <=2 fonts
- **الدليل / proof:** `kosif-atlas/skills/x4919-visual-gen/x20318-cover-image/SKILL.md`

#### FMT-131 · بطاقات مواصفات القنوات · Channel spec cards · 📄 موصوف
- **ماذا / what:** Per-channel specs with format, length, structure, do/avoid: short video = 80-150 spoken words for 20-45 s, hook line on screen and spoken, 3-5 beats each with an [on-screen text] cue, one CTA; YouTube description 200-500 words with the first ~100 characters above the fold and chapters that must star…
- **كيف / how:** Load the spec, draft, enforce counts; re-fit after translation since text expands or contracts (Arabic vs English).
- **أرقام / params:** 80-150 words; 20-45 s; chapters from 0:00
- **الدليل / proof:** `kosif-atlas/skills/1802-content-multiplier/4838-channel-formats/SKILL.md` · `kosif-atlas/skills/1802-content-multiplier/4838-channel-formats/channels/short-video.md` · `kosif-atlas/skills/1802-content-multiplier/4838-channel-formats/channels/youtube.md`

#### FMT-132 · MG-061 افتتاح بثلاث بطاقات سريعة · MG-061 Three quick cards opener · 📄 موصوف
- **ماذا / what:** Three words over three shots summarise the value of a short video, then the topic shot settles.
- **كيف / how:** 0-0.9 / 0.9-1.8 / 1.8-2.7 s cards, 2.7-4 s topic; steady rhythm cuts with a mask reveal per word; never longer than the words can be read.
- **أرقام / params:** 4 s; 0.9 s per card
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-social-clips.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### FMT-133 · MG-062 سؤال يشق الشاشة · MG-062 Question that splits the screen · 📄 موصوف
- **ماذا / what:** A centred question splits into top and bottom halves revealing the filmed answer - vertical explainer opener.
- **كيف / how:** 0-1.5 s question, 1.5-2.5 s split, 2.5-5 s answer; two masked frame copies moving vertically with the text. Keep faces and key titles away from platform buttons.
- **أرقام / params:** 5 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-social-clips.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### FMT-134 · MG-063 تسلسل ثلاث نصائح · MG-063 Three-tip sequence with progress · 📄 موصوف
- **ماذا / what:** A tip number sits in a corner while the paragraph changes every few seconds with a simple progress bar.
- **كيف / how:** 0-4 / 4-8 / 8-12 s tips; one text template, markers, content swaps without excess motion; the bar is part of the video, not a fake app UI.
- **أرقام / params:** 12 s; 3 x 4 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-social-clips.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### FMT-135 · MG-066/067 النتيجة أولاً ومقارنة بنصفين · MG-066/067 Result-first and fair vertical split · 📄 موصوف
- **ماذا / what:** Show the result, shrink it to a thumbnail kept on screen while the steps play, then return to it (MG-066); a vertical screen split into two labelled halves to compare alternatives (MG-067).
- **كيف / how:** MG-066: 0-2 result, 2-3 shrink, 3-8 steps, 8-10 back to result; the result must match the steps shown. MG-067: 0-1 labels, 1-6 compare, 6-8 summary; equal area, light and speed so the comparison is fair.
- **أرقام / params:** 10 s / 8 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-social-clips.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### FMT-136 · MG-069 نهاية تتصل بالبداية · MG-069 Seamless end-to-start loop · 📄 موصوف
- **ماذا / what:** The element leaving the last shot enters at the same position and speed at the start, so the clip loops naturally.
- **كيف / how:** 0-1 s enter, 1-4 s main action, 4-6 s matching exit; match pose and speed at both ends; actually play the last-to-first transition. Local: author a timeline where t=duration equals t=0 and export frames 0..N-1 only; check with ffmpeg -stream_loop.
- **أرقام / params:** 6 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-social-clips.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-loops-backgrounds.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### FMT-137 · MG-070 خاتمة بدعوة واحدة واضحة · MG-070 Single clear CTA end card · 📄 موصوف
- **ماذا / what:** The final shot scales down slightly and one short call to action appears beside it.
- **كيف / how:** 0-1 s shrink, 1-4 s read; scale/position with static text; choose one action and never design a fake tappable button.
- **أرقام / params:** 4 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-social-clips.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### FMT-138 · اختيار إطار الصورة المصغرة محلياً · Local thumbnail frame picking · 📄 موصوف
- **ماذا / what:** Probe the video, extract candidate frames at scene changes, score them (sharpness, face presence, contrast, subject placement), then compose short overlay copy; the hosted service generates thumbnails in ~70-100 s per job, and YouTube bulk custom-thumbnail uploads should stay under about 100 per cha…
- **كيف / how:** ffprobe; ffmpeg -vf "select='gt(scene,0.3)',scale=640:-1" -vsync vfr; numpy Laplacian variance for sharpness; text overlay built in HTML and rendered to 1280x720 PNG.
- **أرقام / params:** <=~100 uploads/24 h/channel
- **الدليل / proof:** `kosif-atlas/skills/932-vidseeds/2178-vidseeds/skills/vidseeds-thumbnails/SKILL.md` · `kosif-atlas/skills/932-vidseeds/2178-vidseeds/skills/vidseeds-local-video/SKILL.md`

#### FMT-139 · إعادة التأطير حسب الموضوع · Subject-aware reframing · 📄 موصوف
- **ماذا / what:** Resize to a target aspect by reframing (largest crop at the target ratio, no distortion) with a focus mode: subject, face, upper body, a named object prompt, or explicit x/y; for video, reframing is per shot (the Adobe tool resizes video but has no auto-reframe).
- **كيف / how:** Local: ffmpeg crop=w:h:x:y with x/y from a smoothed per-frame detector centre (OpenCV/YOLO - needs install) or manual keyframes; Adobe image_crop_and_resize/video_resize need the Adobe connector.
- **أرقام / params:** focus: subject | face | upper_body | {prompt} | {x,y}
- **الدليل / proof:** `kosif-atlas/skills/103-adobe-for-creativity/238-adobe-resize-photos-and-videos/SKILL.md`

#### FMT-140 · تضمين الفيديو المتحرك في الويب · Web embedding of motion pieces · 📄 موصوف
- **ماذا / what:** Ship web video as muted autoplay + playsinline + loop with a poster frame (the LCP image), WebM plus H.264 MP4 fallback, explicit width/height or aspect-ratio, and a prefers-reduced-motion branch that shows the poster with a play control; stills as AVIF -> WebP -> JPEG/PNG in <picture> at 3-5 widths…
- **كيف / how:** ffmpeg encodes (libvpx-vp9 and libx264), poster via -frames:v 1; HTML snippet.
- **أرقام / params:** LCP <=2.5 s; CLS <0.1; INP <200 ms; 3-5 widths
- **الدليل / proof:** `kosif-atlas/skills/2306-generative-web-media/8855-web-optimization-pipeline/SKILL.md`

#### FMT-141 · اختيار بروتوكول البث وجودة التجربة · Streaming protocol choice and QoE · 📄 موصوف
- **ماذا / what:** Pick delivery by latency and reach: HLS (widest, Apple-native), DASH (open), CMAF (shared fragments for both), LL-HLS/LL-DASH (few-second live, needs CDN chunked transfer), WebRTC (sub-second interactive, harder to scale); decide DRM (Widevine/FairPlay/PlayReady) and packaging early; judge by startu…
- **كيف / how:** ffmpeg packages HLS locally (-f hls -hls_time 4 -hls_playlist_type vod) and DASH (-f dash); CDN/DRM are external.
- **الدليل / proof:** `kosif-atlas/skills/2387-streaming-media-engineering/9242-streaming-architecture-and-protocol-sele/SKILL.md` · `kosif-atlas/skills/2387-streaming-media-engineering/9241-playback-qoe-and-delivery/SKILL.md` · `kosif-atlas/skills/2387-streaming-media-engineering/9240-low-latency-live-streaming/SKILL.md`

#### FMT-142 · مواصفات فيديو معاينة المتجر · App-store preview video spec · 📄 موصوف
- **ماذا / what:** iOS app previews: up to 3, 15-30 s, <=500 MB, H.264 at 10-12 Mbps up to 30 fps or ProRes 422 HQ, stereo AAC 256 kbps or PCM at 44.1/48 kHz, .mov/.m4v/.mp4, autoplays muted, real app footage only; first 5 s decide (average watch 4-6.5 s; reported +20-40% conversion). Google Play: a YouTube URL, 30 s-…
- **كيف / how:** ffmpeg -c:v libx264 -b:v 11M -maxrate 12M -r 30 -c:a aac -b:a 256k -ar 48000 -ac 2; verify with ffprobe.
- **أرقام / params:** 15-30 s; 10-12 Mbps; <=30 fps; AAC 256 kbps
- **الدليل / proof:** `kosif-atlas/skills/1446-marketing-skills/3488-aso/SKILL.md` · `kosif-atlas/skills/1446-marketing-skills/3488-aso/references/apple-specs.md` · `kosif-atlas/skills/1446-marketing-skills/3488-aso/references/google-play-specs.md`

#### FMT-143 · خط إنتاج النسخ المترجمة · Localized versions pipeline · 📄 موصوف
- **ماذا / what:** For multi-language versions of one motion piece keep on-screen strings in a catalog separate from the timeline, exchange with a TMS via XLIFF, use translation memory (fuzzy matches 75-100%), lock brand/product names in a glossary, validate placeholders/ICU before import and pick a fallback policy (s…
- **كيف / how:** KOSIF scene JSON with string keys -> per-locale renders with RTL/LTR switching; Python check for missing keys/placeholders.
- **أرقام / params:** TM fuzzy 75-100%
- **الدليل / proof:** `kosif-atlas/skills/2329-localization-i18n-engineering/8941-l10n-pipeline-and-tms/SKILL.md`

#### FMT-144 · مناطق الأمان في الفيديو العمودي · 9:16 UI safe zones · 📄 موصوف
- **ماذا / what:** Platform chrome covers the top, bottom and right rail of vertical video; keep critical text/CTA inside a central zone shifted upward.
- **كيف / how:** On 1080x1920: top 250 px, bottom 320 px, right 120 px, left 60 px reserved -> trusted area ≈ 900x1350 centred, nudged up. Alt rule of thumb: UI covers bottom 20% and right 12%. Draw guides first, then lay out.
- **أرقام / params:** trusted 900x1350; text ≥32 px
- **الدليل / proof:** `kosif-atlas/skills/2976-pwdev-social-media/12592-story-reels/SKILL.md` · `kosif-atlas/skills/1526-gamegen/4173-game-trailer/references/gotchas.md`

#### FMT-145 · مصفوفة المقاسات للمنصات · Platform size matrix · 📄 موصوف
- **ماذا / what:** Canonical output sizes for social variants from one master.
- **كيف / how:** IG feed 1080x1080 / 1080x1350, IG story/reel 1080x1920, TikTok 1080x1920 only, LinkedIn 1200x627 + 1080x1080, Facebook 1200x630 / 1080x1080 / 1080x1920, X 1200x675 / 1080x1080, Snapchat 1080x1920, Threads 1080x1350; YouTube 4K 3840x2160, Shorts 2160x3840.
- **الدليل / proof:** `kosif-atlas/skills/103-adobe-for-creativity/232-adobe-create-social-variations/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2466-davinciresolve-youtube-shorts/SKILL.md`

#### FMT-146 · مواصفات تسليم يوتيوب 4K · Delivery spec YouTube 4K · 📄 موصوف
- **ماذا / what:** YouTube 4K master: 3840x2160 at timeline fps; H.264 45 Mbps (≤30 fps) / 68 Mbps (60 fps) or H.265 30/45 Mbps; AAC 48 kHz 320 kbps stereo; -14 LUFS ±1, TP ≤ -1 dBTP; verify frame count within 1 frame of timeline.
- **كيف / how:** Resolve render preset or ffmpeg -c:v libx264 -b:v 45M -maxrate 50M -bufsize 90M ; if NLE lacks AAC, render PCM then ffmpeg -c:v copy -c:a aac -b:a 320k
- **أرقام / params:** 45/68 Mbps; 320k AAC
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2450-davinciresolve-audio-delivery/SKILL.md`

#### FMT-147 · فصول يوتيوب من العلامات · YouTube chapters from markers · 📄 موصوف
- **ماذا / what:** First chapter at 00:00, at least 3 chapters, ≥10 s apart, searchable place/event names (mood words go in captions, not chapters); output 'mm:ss Name' list (hh:mm:ss past 60 min) for the description.
- **كيف / how:** Export timeline markers; or write ffmetadata [CHAPTER] blocks and mux with -map_metadata
- **أرقام / params:** ≥3 chapters, ≥10 s
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2465-davinciresolve-subtitle-travelnote/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2445-akbun-davinciresolve-workflow/SKILL.md`

#### FMT-148 · اختيار صورة الغلاف · Thumbnail candidate picking · 📄 موصوف
- **ماذا / what:** Sample across the whole video, drop blank/transition/blurred and first/last frames, shortlist visually distinct moments that show subject/action/result, reframe each aspect separately; animated cover = gentle-motion short loop with similar start/end frames.
- **كيف / how:** ffmpeg select by scene + thumbnail filter (thumbnail=n=100) ; tile contact sheet ; render chosen frame natively from composition when possible
- **الدليل / proof:** `kosif-atlas/skills/101-video-skills/222-video-thumbnails/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2441-akbun-davinciresolve-searchhook/SKILL.md`

#### FMT-149 · ترخيص الموسيقى حسب الباقة · Music licence by plan · 📄 موصوف
- **ماذا / what:** ElevenLabs free plan has no commercial licence and needs 'Eleven Music' credit; paid plan licence counts at render time; record receipts.
- **كيف / how:** Store plan/rights in render receipt.
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3892-music/references/RIGHTS.md`

#### FMT-150 · لا MP3 للحلقات · Loop formats: no MP3 · 📄 موصوف
- **ماذا / what:** MP3 pads silence at both ends; loops/effects ship as WAV/OGG/Opus; mp3 only for page players; browsers need Web Audio buffer loop.
- **كيف / how:** ffmpeg -c:a libopus or pcm_s16le.
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3901-sound/references/TRAPS.md` · `kosif-atlas/skills/1526-gamegen/4163-game-audio-procedural`

#### FMT-151 · أهداف العلو للتسليم · Loudness delivery targets · 📄 موصوف
- **ماذا / what:** Web/YouTube/trailer -14 LUFS integrated ±1, true peak <= -1 dBTP; calm -16 to -18; bed under SFX -18 to -20.
- **كيف / how:** ffmpeg loudnorm I=-14:TP=-1:LRA=11 two-pass; verify with ebur128=peak=true on final encoded file.
- **أرقام / params:** -14 LUFS, -1 dBTP
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2450-davinciresolve-audio-delivery` · `kosif-atlas/skills/1511-homie/3901-sound` · `kosif-atlas/skills/1526-gamegen/4163-game-audio-procedural/references/mixing-and-loops.md`

#### FMT-152 · مواصفة صوت الفيديو للتسليم · Video audio delivery spec · 📄 موصوف
- **ماذا / what:** YouTube 4K: AAC 48kHz 320kbps stereo; H.264 45Mbps (<=30fps) / 68Mbps (60fps); H.265 30/45.
- **كيف / how:** ffmpeg -c:a aac -b:a 320k -ar 48000; ffprobe check duration within 1 frame.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2450-davinciresolve-audio-delivery`

#### FMT-153 · حجم خط متجاوب · Fluid responsive type · 📄 موصوف
- **ماذا / what:** Scale type with canvas size so one composition exports to 16:9, 9:16 and 1:1.
- **كيف / how:** CSS clamp()/vw units against composition width; or size tokens per aspect.
- **الدليل / proof:** `kosif-atlas/skills/3438-ux-design/14126-web-typography/references/responsive-typography.md`

#### FMT-154 · تكبير للهاتف · Mobile reading boost · 📄 موصوف
- **ماذا / what:** Small screens and outdoor light demand larger, higher-contrast text.
- **كيف / how:** Body 17-18px web; in 1080x1920 video keep captions ≥ 48-64px and contrast ≥7:1.
- **الدليل / proof:** `kosif-atlas/skills/3438-ux-design/14126-web-typography/SKILL.md`

#### FMT-155 · المنطقة الآمنة للترجمة · Caption safe area · 📄 موصوف
- **ماذا / what:** Keep captions inside title-safe area and away from platform UI.
- **كيف / how:** Title safe 90% (5% margins); for 9:16 Reels/TikTok keep text out of bottom ~20% and right ~12% UI zones; max 2 lines.
- **أرقام / params:** 2 lines; 5% margins
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-typography/references/quality-and-editors.md` · `kosif-atlas/skills/1503-universal-design-principles/3825-legibility-contrast-and-spacing/SKILL.md`

#### FMT-156 · مقاسات أصول الهوية الرقمية · Favicon/OG/social asset sizes · 📄 موصوف
- **ماذا / what:** Minimum identity export set for 2026.
- **كيف / how:** favicon.svg (dark via media query), favicon.ico 16/32/48, apple-touch 180×180, PWA 192/512, OG 1200×630, X card 1200×675. Render with headless Chromium/Pillow.
- **أرقام / params:** see how
- **الدليل / proof:** `kosif-atlas/skills/2248-brand-identity-studio/8557-brand-book-assembly`

#### FMT-157 · خطط نسب الأبعاد لمشاهد البيانات · Aspect-ratio plans for data scenes · 📄 موصوف
- **ماذا / what:** Design horizontal and vertical versions deliberately instead of squeezing a desktop chart.
- **كيف / how:** Vertical 1080x1920: fewer markers, shorter labels, stacked small multiples, legend/key below, 3-5 ticks; horizontal 1920x1080: side-by-side panels. Map plates: 3840x2160 for 16:9, ~2700x3840 for 9:16. Inspect rendered pixels at every delivered ratio.
- **أرقام / params:** ticks 3-5 vertical, 4-7 horizontal
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/SKILL.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10320-d3-data-visualization/SKILL.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/mapbox/references/render-stability.md`

#### FMT-158 · أبعاد وعدد إطارات متوافقة مع الفضاء الكامن · Latent-friendly dimensions and frame counts · 📄 موصوف
- **ماذا / what:** Diffusion models need sizes divisible by 8 (16 for WanVideo and Krea 2, 32 for LTX) and LTX needs 8k+1 frames.
- **كيف / how:** Round sizes before sending (ImageResizeKJv2 divisible_by); LTX common 768x512, 1216x704, 704x480 with 121/161/257 frames; compute frames from duration × fps and round to 8k+1.
- **أرقام / params:** ÷8 / ÷16 / ÷32; frames 8k+1
- **الدليل / proof:** `kosif-atlas/skills/2142-comfyui-plugin/7651-comfy-image-utils` · `kosif-atlas/skills/1514-huggingface-skills/3937-huggingface-lora-space-builder`

#### FMT-159 · مقاسات المنصات والمناطق الآمنة · Platform sizes and safe zones for generated assets · 📄 موصوف
- **ماذا / what:** Target dimensions for stills and clips by placement.
- **كيف / how:** OG 1200x630; YouTube 16:9 1920x1080 / thumbnail 1280x720; Reels/TikTok/Shorts 1080x1920; IG feed 1080x1080 or 1080x1350 (4:5); LinkedIn cover 1584x396; X header 1500x500; GitHub preview 1280x640 ≤1 MB (min 640x320); keep key content 10-15% from edges.
- **أرقام / params:** safe margin 10-15%
- **الدليل / proof:** `kosif-atlas/skills/1446-marketing-skills/3504-image` · `kosif-atlas/skills/1446-marketing-skills/3531-video` · `kosif-atlas/skills/2153-github-actions-plugin/7759-github-social-preview`

#### FMT-160 · المناطق الآمنة للريلز · 9:16 platform safe zones · 📄 موصوف
- **ماذا / what:** Keep faces and text out of the top 14%, bottom 18-35% and the right edge where platform buttons sit; captions about 70% down.
- **كيف / how:** Used in frame review prompt (bottom 18%, right side), autopilot rule 6, critique rubric and DIRECTOR_KB composition list.
- **أرقام / params:** top 14%; bottom 18% (UI) / 25-35% (KB); sides 6%
- **الدليل / proof:** `app/public/js/00_editor.js:1491` · `app/public/js/10_studio.js:8`

#### FMT-161 · حزمة النشر · Post pack (kosif-social) · 📄 موصوف
- **ماذا / what:** Caption/hashtags/CTA per platform, carousel, calendar, A/B.
- **كيف / how:** social.py pack FILM --platforms; check; carousel; calendar; besttime; abplan/abread
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/operating-manual.md`

#### FMT-162 · تحويل النسبة بقص ذكي · Smart aspect conversion around faces · 📄 موصوف
- **ماذا / what:** Reframes footage to another ratio, following faces (smart), centre-cropping, or placing it over a blurred fill.
- **كيف / how:** From the studio: recipe 'aspect' (form in the الوصفات tab, POST /api/jobs {recipe:'aspect', args} or MCP kosif_run); equivalent CLI `python scripts/kmotion.py aspect …`.
- **أرقام / params:** clip; --to 9:16|16:9|1:1|4:5 (default 9:16); --mode smart|crop|blur (default smart); --out out/vertical.mp4
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:70`

#### FMT-163 · تصدير كل النسب مع بوستر · All-ratio export + poster + GIF · 📄 موصوف
- **ماذا / what:** Exports a film in several aspect ratios plus a titled poster and optionally a GIF.
- **كيف / how:** From the studio: recipe 'export' (form in the الوصفات tab, POST /api/jobs {recipe:'export', args} or MCP kosif_run); equivalent CLI `python scripts/kmotion.py export …`.
- **أرقام / params:** film; --out out/deliver; --aspects 9:16,1:1,16:9; --title; --gif
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:84`

#### FMT-164 · غلاف بعنوان عربي · Arabic-titled cover / thumbnail · 📄 موصوف
- **ماذا / what:** Grabs a frame at a chosen second and writes an Arabic title on it as a cover image.
- **كيف / how:** From the studio: recipe 'thumb' (form in the الوصفات tab, POST /api/jobs {recipe:'thumb', args} or MCP kosif_run); equivalent CLI `python scripts/kmotion.py thumb …`.
- **أرقام / params:** film; --at 2; --text; --out out/cover.jpg
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:90`

#### FMT-165 · تصدير لكل منصة مع فحص الحدود · Per-platform export with limit checks (8 platforms) · 📄 موصوف
- **ماذا / what:** One checked file per platform at its ratio and size with a video bitrate ceiling; duration and file-size limits are reported, never silently trimmed.
- **كيف / how:** Recipe 'platforms' (film; --out out/deliver; --platforms tiktok,reels,shorts,…; --title) or kmotion platforms.
- **أرقام / params:** tiktok 9:16 1080×1920 ≤600 s ≤287 MB 12000k/192k · reels 9:16 1080×1920 ≤180 s ≤250 MB 12000k/192k · shorts 9:16 1080×1920 ≤180 s ≤256 MB 12000k/192k · youtube 16:9 1920×1080 ≤2000 MB 16000k/256k · x 16:9 1280×720 ≤140 s ≤512 MB 8000k/160k · whatsapp 9:16 720×1280 ≤30 s ≤16 MB 2200k/96k · linkedin 1…
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:87` · `100-superskills/skills/kosif-montage-motion/scripts/platforms.py:28`

#### FMT-166 · غلاف JSON لتطبيقات الاستوديو · AI-Studio JSON envelope + platform prompt object · 📄 موصوف
- **ماذا / what:** Machine-readable answer shape for the user's own AI Studio apps.
- **كيف / how:** Only when the user's app parses JSON: {title, analysis, confidence, sources, json:{tool_output,prompts,imageSpecs}, nextSteps, qualityScore{detail,consistency,cinematic,lighting,colorTheory}, colorAnalysis{kelvin,mood}}; per-platform object {platform, prompt, negativePrompt, params{aspect}, audioDirection}.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-cinema-director/references/response-formats.md`

#### FMT-167 · برومبت صورة مصغرة · YouTube thumbnail prompt · 📄 موصوف
- **ماذا / what:** Template for click-worthy thumbnails with room for a title.
- **كيف / how:** 'YouTube thumbnail, [subject] with exaggerated [emotion], high contrast, bold rim light, clean background, space on the right for title, 16:9'; add Arabic title as an overlay layer, not in the generator.
- **أرقام / params:** 16:9; title space right
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-image-studio/references/prompt-library.md`

#### FMT-168 · أهداف علو الصوت لكل منصة · Loudness targets per platform · 📄 موصوف
- **ماذا / what:** Delivery loudness for each destination.
- **كيف / how:** Measure, then gain to target and limit to the true-peak ceiling.
- **أرقام / params:** Spotify/YouTube/Apple ~ -14 LUFS TP <= -1 dBTP; podcast -16 LUFS (mono -19); broadcast EBU R128 -23 LUFS TP -1; club -9 to -6 LUFS TP -0.3 (script uses -8)
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-audio/SKILL.md` · `kosif-one/tools/kosif-omni/skills/kosif-audio/scripts/audio_analyze.py:30`

#### FMT-169 · مواصفات التصدير · Export spec for social/cinema · 📄 موصوف
- **ماذا / what:** Default delivery formats.
- **كيف / how:** Reels/TikTok 9:16, YouTube 16:9, cinema 2.39:1; H.264/H.265, 1080x1920 or 3840x2160, 24/30 fps, -14 LUFS, yuv420p.
- **أرقام / params:** 9:16, 16:9, 2.39:1; 1080x1920 / 3840x2160; 24/30 fps
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-video/SKILL.md` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/SKILL.md`

#### FMT-170 · تعبئة بخلفية ضبابية · Blurred-fill vertical · 📄 موصوف
- **ماذا / what:** Fit wide footage in 9:16 over a blurred, scaled copy.
- **كيف / how:** [0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20[bg];[0:v]scale=1080:-2[fg];overlay centred
- **أرقام / params:** boxblur 20
- **الدليل / proof:** `100-superskills/skills/pro-video-editor-ffmpeg/references/ffmpeg-recipes.md`

#### FMT-171 · خلطة الوسوم والخطاف · Hashtag mix and hook rules · 📄 موصوف
- **ماذا / what:** IG: 1 general + 2 niche + 1 place + 1 brand; Arabic tags no tashkeel/tatweel with underscores; hook = number/result/question/contradiction matching first 2 s of video; one CTA (save/share/comment word/follow).
- **كيف / how:** copy-guide
- **أرقام / params:** max 5
- **الدليل / proof:** `100-superskills/skills/kosif-social/references/copy-guide.md`

#### FMT-172 · متجر يبيع · E-commerce Store & Listings · 📄 موصوف
- **ماذا / what:** Owner-built skill "E-commerce Store & Listings" (own words): workflow guidance for e-commerce store & listings; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill ecommerce-store-listings (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/ecommerce-store-listings/SKILL.md`

#### FMT-173 · رسائل تُفتح وتُقرأ · Newsletters & Email Marketing · 📄 موصوف
- **ماذا / what:** Owner-built skill "Newsletters & Email Marketing" (own words): workflow guidance for newsletters & email marketing; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill newsletter-email-marketing (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/newsletter-email-marketing/SKILL.md`

#### FMT-174 · ظهور في البحث بلا خدع · SEO & Content Architecture · 📄 موصوف
- **ماذا / what:** Owner-built skill "SEO & Content Architecture" (own words): workflow guidance for seo & content architecture; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill seo-content-architecture (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/seo-content-architecture/SKILL.md`

#### FMT-175 · تصدير فافيكون · Favicon + manifest export · 📄 موصوف
- **ماذا / what:** PNG via PIL/browser, favicon.ico, manifest, sprite.svg, SVG optimisation.
- **كيف / how:** PIL
- **الدليل / proof:** `100-superskills/skills/svg-illustration-icons/SKILL.md:24`

#### FMT-176 · قواعد المقروئية والتباين على الهاتف · Phone legibility and contrast rules · 📄 موصوف
- **ماذا / what:** Smallest readable text 36 px at 1080 width, verify on 360 px preview, contrast ≥ 4.5:1, safe margins 5% sides and 12% top/bottom for 9:16.
- **كيف / how:** STYLE.md §6 / TEST_REPORT checks 8,12,13
- **الدليل / proof:** `kosif-tool/templates/STYLE.md` · `kosif-tool/templates/TEST_REPORT.md`

#### FMT-177 · إيقاع المنصات للإعلانات · Platform pacing table (ads) · 📄 موصوف
- **ماذا / what:** Aspect, length and cut rate per platform for ads.
- **أرقام / params:** TikTok/Reels 9:16 15–30 s cuts every 1–2 s; YouTube pre-roll 16:9 key message before 5 s; feed 1:1 or 4:5
- **الدليل / proof:** `kosif-tool/playbooks/ads.md:30`

#### FMT-178 · إعادة التكوين لكل منصة · Multi-platform recompose · 📄 موصوف
- **ماذا / what:** Render master at largest aspect, recompose (not blind-crop) per platform; each passes gate.
- **الدليل / proof:** `kosif-tool/playbooks/render-pipeline.md:57`

#### FMT-179 · الغلاف كإطار أول · Bake poster as frame 0 · 📄 موصوف
- **ماذا / what:** Replace only frame 0 with the poster so Slack/X/Discord thumbnails show it; duration and audio unchanged.
- **كيف / how:** ffmpeg filter_complex overlay on first frame, -c:a copy.
- **أرقام / params:** 1/30 s at 30fps
- **الدليل / proof:** `kosif-one/vendor/brag/skills/brag/references/step-4-deliver.md`

#### FMT-180 · نص المشاركة · Share copy line · 📄 موصوف
- **ماذا / what:** One punchy non-corporate sentence for X/LinkedIn/Discord delivered with the video.
- **كيف / how:** Draft in plan, finalize at delivery.
- **الدليل / proof:** `kosif-one/vendor/brag/skills/brag/references/step-2-plan.md`

#### FMT-181 · إعلان تطبيق مربع صامت · Muted-autoplay square app ad · 💡 فكرة
- **ماذا / what:** 1:1 ad legible without sound; icon+name fully visible by 300 ms; last 500 ms frozen for thumbnail.
- **كيف / how:** 1080x1080 composition.
- **أرقام / params:** 80 px safe margin; text ≥48 px; headline ≥96 px
- **الدليل / proof:** `style:pm-cansincengiz-me-cf68dd`

#### FMT-182 · منطقة آمنة · 9:16 safe area & exits 40% faster · 💡 فكرة
- **ماذا / what:** 120 px top/bottom margins in 1080x1920; exits 40% faster than entrances.
- **أرقام / params:** spring 180/18; 350-700 ms
- **الدليل / proof:** `style:pm-l3d1c-0e35a3`

#### FMT-183 · حلقة متصلة · Pixel-identical seamless loop · 💡 فكرة
- **ماذا / what:** First and last frames identical; final hold only 2% opacity breathe.
- **كيف / how:** Verify frame diff.
- **أرقام / params:** 20 s; hold 1.5 s
- **الدليل / proof:** `style:pm-listudio-820c7b`
