# القصة والإخراج — Story & direction

> **قوتك هنا:** أنت المخرج قبل أن تكون المحرّك: تسأل رسالة واحدة قصيرة بالعربية، تقترح 2–3 اتجاهات مختلفة فعلًا، تختار خطافًا يُفهم في ثانية، تبني القصة على صراع وقرار، تحمل الفيلم بشيء واحد يعبر كل اللقطات، وتختم عن قصد — وكل نبضة تضيف معلومة جديدة أو تُحذف.
> **أقوى دليل:** خطط حتمية مجرَّبة هنا: `kmotion proplan` قسّم فيلم 11 ث إلى hook/setup/contrast/payoff/end_card عند الإطارات 0/40/119/205/277، و`story_lint.py` أعطى درجة 72 مع تحذيرات حقيقية، وموجّه `plan.py` حوّل «عايز ريل من فيديو كلام مع ترجمة وموسيقى» إلى talking_reel، واختبارات Fastify (24 اختبارًا) واختبار `test_direct_plans_like_an_editor` نجحت كلها.
> **You can:** route any Arabic request, write the brief/plan/storyboard as data, pick hooks and arcs with second budgets, direct taste (one signature, one device, no AI-look), and run ready genre engines (talking edit, launch film, stickman, romance, dua, montage).
> **94 powers follow** — ✅ 14 · 🟢 20 · 📦 2 · 🔑 1 · 👁 11 · 📄 46 · 💡 0.

**الحالة / status:** ✅ مُثبت هنا (كود + اختبار أو رندر في هذه الحاوية) · 🟢 جاهز (كود المالك يعمل بلا إضافات) · 📦 بأمر تثبيت · 🔑 مفتاح أو خدمة · 👁 شوهد في فيديو أنتجتَه (وصفة البناء مرفقة) · 📄 موصوف فقط · 💡 فكرة.
مسارات الدليل نسبية إلى `/home/user/`؛ `style:<id>` = فيديو مرجعي أنتجتَه سابقًا (ملاحظاته في `kosif-tool/styles/<id>/`).

**فحص هذه الحاوية (2026-10-16):** `kosif.py prompt` + اختبارات test_cli/test_templates/test_generator ✔ · `kmotion proplan` ✔ · `story_lint.py` ✔ · `kosif-one plan.py` ✔ · `social.py calendar` (CSV/XLSX/MD/ICS) ✔ · Fastify: planner 5 + cli 2 + profiles 10 + viral 7 = 24 نجاح ✔ (تشغيل `node --test tests/` دفعة واحدة يفشل بخطأ تشغيل؛ شغّل كل ملف منفردًا) · kosif-studio: direct/verse/audio2motion ✔.

## الفهرس / contents
- **الاستقبال والتوجيه — Intake & routing** — STORY-01 … STORY-07 (7)
- **وثائق ما قبل الإنتاج — Pre-production documents** — STORY-08 … STORY-15 (8)
- **الخطاف والافتتاحية — Hooks & openings** — STORY-16 … STORY-20 (5)
- **هياكل القصة والأقواس الموقوتة — Story structures & timed arcs** — STORY-21 … STORY-34 (14)
- **الذوق والإخراج البصري — Direction & taste** — STORY-35 … STORY-46 (12)
- **أدوات السرد والنقوش — Story devices & motifs** — STORY-47 … STORY-58 (12)
- **محركات الأنواع والأفلام الجاهزة — Genre engines & ready films** — STORY-59 … STORY-77 (19)
- **الأفكار والتغليف والتخطيط — Ideation, packaging & planning** — STORY-78 … STORY-85 (8)
- توليفات قوية / power combos · أخطاء ممنوعة / never do · أقوى 5 حركات توقيع / 5 signature moves
- **إضافات v2 — v2 additions** — STORY-X01 … STORY-X06 (6)

## الاستقبال والتوجيه — Intake & routing

_سؤال واحد قصير، افتراضات معلنة، ثم مسار واضح — لا استجواب ولا إطلاق خمس أدوات معًا._

#### STORY-01 · استقبال عربي بجولة واحدة · One-round Arabic intake with defaults · 🟢 جاهز / ready
- **ماذا / what:** رسالة عربية واحدة قصيرة فيها الأسئلة الناقصة فقط، كل سؤال باقتراح افتراضي، ثم انتظار. — One short Arabic message with only the missing questions, each with a default, then wait.
- **متى أستخدمها / when:** أول ردّ على أي طلب فيديو — first reply to any video request.
- **كيف / how:** Diff the request against what the user already gave (audio, references, timing, style); ask only from the seven: message/audience/script, production type, duration + platform, language/dialect (فصحى/مصري/سعودي/English), supplied assets, realism/rhythm/likes-dislikes, preview-vs-final. Unanswered non-blocking items take your stated default (9:16, 30 s). For novices offer only 2–3 decision surfaces (where it plays, how long, how it should feel) with 2–4 options each; for data/map jobs infer then ask 1–3 either/or questions. Interactive CLI: `npm run intake` writes project/brief.json (defaults kinetic, 9:16, 30 s, ar-EG). Never re-ask known facts; a BRIEF.md or STORYBOARD.md already in the project means resume, not interview. **أرقام / params:** 1 message · ≤7 questions · defaults offered.
- **الدليل / proof:** `fastify-motion-bro/docs/QUESTIONS.md:1-10` · `fastify-motion-bro/scripts/cli.mjs:9-19` · `kosif-one/vendor/hyperframes/skills/hyperframes/references/pitch-round.md` · `kosif-one/vendor/hyperframes/skills/hyperframes/SKILL.md`

#### STORY-02 · موجّه الطلب الواحد (16 مسارًا) · One-request router (16 routes + add-ons) · ✅ مُثبت هنا / proven here
- **ماذا / what:** يطبّع الطلب العربي/الإنجليزي، يرتب المسارات بالكلمات، يلتقط الإضافات (ترجمة، صوت، موسيقى، 9:16، غلاف، خصوصية…) ويدمج حتى 4 مسارات في خط إنتاج واحد. — Normalises an Arabic/English request, ranks 16 routes by keyword evidence, detects add-ons and merges up to 4 routes into one pipeline.
- **متى أستخدمها / when:** تحديد ما سيُبنى فعلًا قبل أي كود — deciding what to build.
- **كيف / how:** `python3 plan.py --json "عايز ريل من فيديو كلام مع ترجمة وموسيقى"` → main_route talking_reel (ran here). Routes: reel_from_web, edit_my_footage, talking_reel, motion_2d, cinematic_3d, launch_video, sound_to_film, song_reel, mimic_reel, analyze_reference, ai_video_prompts, image_graphics, pixel_redraw … ; `--combine MAIN A B` runs shared steps once with one ratio/palette/font set; Jev keeps an extra route at p_yes ≥ 0.6, 0.4–0.6 only with a stated reason, < 0.4 dropped; explicit user words always win. Basma has the no-AI equivalent (KIT.guess regex votes: تقني→plotter, قصة→doodle, درس→whiteboard, رياض→chalkboard) and a local content classifier (music: silence < 6% + beat conf ≥ 1.35; screen: ≥ 55% still frames; edited: ≥ 2.5 cuts/10 s). Fastify asks which of nine profile modes to run and loads only that skill. **أرقام / params:** max 4 routes · p_yes 0.6/0.4 · ~0.1 s.
- **الدليل / proof:** `100-superskills/skills/kosif-one/scripts/plan.py:37` · `kosif-one/tools/kosif-one/scripts/plan.py:39` · `app/public/js/10_studio.js:928` · `fastify-motion-bro/docs/PROFILE_CATALOG.md:5-17`

#### STORY-03 · مخطط اللقطات الحتمي ProPlan · Deterministic shot planner (ProPlan) · ✅ مُثبت هنا / proven here
- **ماذا / what:** جملة المهمة ← خطة قراءة فقط: النية، الأوامر، القيود، و5 نبضات بإطارات دقيقة وحركة كاميرا لكل لقطة ونية صوت. — A task sentence becomes a read-only plan: intent, commands, limits and a 5-beat frame-exact storyboard with a camera move per shot.
- **متى أستخدمها / when:** قبل أي بناء، أو لشرح الخطة للمستخدم — before building, or to show the plan.
- **كيف / how:** `python3 scripts/kmotion.py proplan --task "…" --seconds 12 --fps 30 --aspect 9:16 --out plan.json` (also POST /api/plan, MCP motion_plan). Cuts at 0/.12/.36/.62/.84/1 of frames: hook, setup, contrast, payoff, end_card; 2D moves fast_reveal/slow_push/match_cut/focus_lift/still_hold; 3D dolly_in/orbit/side_track…; audio_intent "impact" on beats 1 and 4; text safe area 15–80% on 9:16, 8% inset otherwise; `--require-full-pro` exits 3 without verified receipts. Ran here: 11 s 3D → frames 0/40/119/205/277, intent 3d_motion, side_effects_performed false. Simpler 3-shot scaffold (ultra_animator): 30/40/30% wide dolly-in → medium orbit 45° → payoff. **أرقام / params:** seconds 2–600 · fps 24/25/30/50/60 · cuts 0/12/36/62/84/100%.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/proplan.py` · `100-superskills/skills/kosif-montage-motion/tests/test_core.py:54` · `kosif-studio/motion/proplan.py:84` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/scripts/ultra_animator.py:104`

#### STORY-04 · مولّد طلب Claude من الأسلوب · Style → Claude request generator · ✅ مُثبت هنا / proven here
- **ماذا / what:** يملأ قالب طلب ثنائي اللغة من سجل الأسلوب: المستودع، الأسلوب، الكتيبات، المصدر، المقاس، المحرك، اللغة، الصوت. — Fills a bilingual request template from a style record and options.
- **متى أستخدمها / when:** تسليم مهمة لجلسة Claude أخرى أو للموقع — handing a job to another session.
- **كيف / how:** `python3 tools/kosif.py prompt <id> --lang ar --aspect 9:16 --fps 30 --duration 15 --source "audio voice.mp3"|"video x.mp4"|"text s.md"|none --stack auto|remotion|canvas|svg|three --audio keep|music|sfx|silent --content-lang ar|en|both` (ran here for whiteboard). Source phrases: audio = master clock, transcribe and sync; video = study cuts/motion/speech; text = script supplied; none = write original narration + timed plan. web/generator.js mirrors it (buildRequest, cliCommand). Basma buildMotionPrompt adds a second-by-second timeline, spring 0.42/16 rad/s or ease-out 0.25–0.5 s, exits 0.2–0.3 s, stagger 0.06–0.12 s. **أرقام / params:** 15 placeholders · 5-step workflow.
- **الدليل / proof:** `kosif-tool/tools/kosif.py:425` · `kosif-tool/templates/claude_request.ar.txt` · `kosif-tool/web/generator.js` · `kosif-tool/tests/test_generator.mjs`

#### STORY-05 · بوابة اختيار الأسلوب قبل التخطيط · Style-choice gate: 3–5 directions, max 2 blended · 🟢 جاهز / ready
- **ماذا / what:** قبل أي ستوريبورد اعرض 3–5 اتجاهات مختلفة حقًا (صورة النتيجة، لماذا تناسب، الكلفة) وانتهِ بـ «أي أسلوب؟»؛ والمزج = أساس + لمسة واحدة بنطاق محدد. — Before any storyboard offer 3–5 genuinely different directions and end with "which style?"; blending = one base + one scoped accent.
- **متى أستخدمها / when:** طلب مفتوح أو «اعمل حاجة حلوة» — open briefs.
- **كيف / how:** Map the brief to the S01–S14 menu or the 288-style catalogue (`python3 tools/kosif.py search <words>`); mark one as recommended. For unformed asks sample five concepts with ≥2 from the unusual tail before recommending (pitch round); each pitch names the capability it rides. Record base=S02, accent=S03 (titles only); never blend more than two; a described look outside the menu is labelled CUSTOM. When the user cannot describe a look, show 2–4 quick variant stills/3 s loops and revise only from marked ones. **أرقام / params:** 3–5 options · 1 recommended · ≤2 blended.
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/styles.md` · `kosif-one/vendor/hyperframes/skills/hyperframes/references/pitch-round.md` · `kosif-atlas/skills/1995-hypotyposis/7163-sketch` · `kosif-tool/STYLE_INDEX.md`

#### STORY-06 · جدول الرد قبل البناء · Talk-before-build response table · 📄 موصوف / documented only
- **ماذا / what:** تغيير مسمّى = نفّذه؛ ملاحظة شعورية = اعثر على السبب القابل للقياس وغيّره واشرح؛ سؤال = أجب فقط؛ «ثبّت» = لا تغيّر شيئًا؛ فكرة = اقترح وأضف للخطة؛ موافقة = ابنِ. — Named change → do it; felt note → find the measurable cause; question → answer only; hold → change nothing; approval → build.
- **متى أستخدمها / when:** كل جولة مراجعة — every revision round.
- **كيف / how:** Translate felt notes ("مش فخم كفاية") into numbers: durations, easing, contrast, type weight, hold length. The review page composes all unsent edits/notes into one prompt with sections Edits (apply exactly), Notes (timecode/scene/element), Links, Scenes, Do; motion requests go to notes because only Claude changes motion. **أرقام / params:** 7 response types.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-studio/SKILL.md` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/index.html:883`

#### STORY-07 · قائمة القوة الكاملة وفرصة الوسائط · Full-power checklist & media-opportunity pass · 📄 موصوف / documented only
- **ماذا / what:** قبل البناء مُرّ على: المادة، الفهم، الصورة، الصوت، التشطيب، الأفكار — ومرة واحدة اعرض كل التحسينات الممكنة في طلب واحد. — Walk material, understanding, picture, sound, finish and ideas; make one consolidated media-upgrade ask.
- **متى أستخدمها / when:** كل مشروع متوسط أو كبير — mid/large jobs.
- **كيف / how:** Checklist: 2–3 directions, hook ≤2 s, one carried device, payoff, deliberate end, poster, credits, post pack, deliver ≥1080p. Media pass (one grounded scan): script without voice → TTS; emoji icons → real icons; placeholder image → better image; silent cuts → transition SFX; >10 s without music → bed; user approves all/some/none. **أرقام / params:** ≥1080p · one consolidated ask.
- **الدليل / proof:** `kosif-one/tools/kosif-one/SKILL.md` · `kosif-one/vendor/hyperframes/skills/media-use/SKILL.md`

## وثائق ما قبل الإنتاج — Pre-production documents

_الخطة بيانات قبل أن تكون كودًا: نفس الملف يقود الرندر وفحص اللقطات._

#### STORY-08 · STYLE.md وPLAN.md: المرصود والمفترض والجدول الموقوت · STYLE.md + PLAN.md: observed vs assumed + timed scene table · ✅ مُثبت هنا / proven here
- **ماذا / what:** ورقة أسلوب تفصل ما رُصد (بدليل زمني) عما افتُرض، وجدول مشاهد بلا فجوات ينتهي بالضبط عند المدة. — A style sheet separating observed (timestamped) from assumed, and a gap-free scene table ending exactly at duration.
- **متى أستخدمها / when:** كل مشروع kosif-tool قبل الكود — every scaffolded project.
- **كيف / how:** `python3 tools/kosif.py scaffold <id> <dir>` fills both. STYLE: tokens for colour, type, line weights, easing, camera, Arabic rules, do-nots. PLAN: start/end, action, camera, transition, audio cue, assets; one clear motion per scene; word-timing table; licence checklist. Timing defaults: entrances 250–600 ms, accents 120–300 ms, transitions 300–800 ms. Fastify `npm run plan` writes storyboard.json, STYLE.md and a PLAN.md checklist (the agent must then rewrite it creatively). **أرقام / params:** entrances 250–600 ms · accents 120–300 · transitions 300–800.
- **الدليل / proof:** `kosif-tool/templates/STYLE.md` · `kosif-tool/templates/PLAN.md` · `kosif-tool/tests/test_templates.py` · `fastify-motion-bro/scripts/planner.mjs:25-35`

#### STORY-09 · عقد المشهد كبيانات · Scene contract as data (scene cards) · 📄 موصوف / documented only
- **ماذا / what:** كل مشهد سجل JSON: النص، الخلاصة، طبقات البيانات، الوسائط، الكاميرا، المدى الزمني أو كلمات words.json، فعل الحركة، وإطار ثابت للفحص. — Every scene is a JSON record: text, takeaway, layers, media, camera, time range or word ids, motion verb, static QA frame.
- **متى أستخدمها / when:** أي فيلم شرح أو بيانات أو توليد — explainers, data stories, generated scenes.
- **كيف / how:** Fields: id, viewer text/VO line, takeaway, dataLayers (visible/dimmed/highlighted), media, annotations, cameraOrTransform, triggerRange (s or word ids), motionVerb (reveal, compare, accumulate, transform, move, zoom, pan, highlight, play), reducedMotion/static key frame. Generated-scene cards add base image, camera (static/pan/dolly/orbital), on-screen text + safe position, caption, motion prompt; mark "SPECIFIED, NOT GENERATED" when no key exists. The renderer reads durations and text from the same JSON so storyboard and film never drift; brief.json per-beat fields (time, composition, camera, subjects, text, typography, icons_ui, lighting_texture, motion, transition_out, audio) follow the same idea. **أرقام / params:** 9 motion verbs.
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10329-scrollytelling-and-parallax-data-visuali/references/story-patterns-and-scene-contracts.md` · `kosif-atlas/skills/2976-pwdev-social-media/12594-video-gen/SKILL.md` · `100-superskills/skills/kosif-montage-motion/references/video-breakdown.md`

#### STORY-10 · اللوحات قبل الرندر · Boards-first production gate · 📄 موصوف / documented only
- **ماذا / what:** لا رندر قبل موافقة المستخدم على البريف ودليل الأسلوب واللوحة وأوراق الشخصيات ولوحات الستوريبورد. — No render until the user approves brief, style guide, palette, character sheets and storyboard panels.
- **متى أستخدمها / when:** أفلام الشخصيات والرسوم والأعمال الطويلة — character/illustrated or long films.
- **كيف / how:** brief.md → boards/(style-guide, palette.json {ink, paper, tones}, models, storyboard.json panels {shot, panel, t, png, action, camera}) → approval → shots.json {fps, size, shots[t0,t1]} (shot1 t0=0; each t1 = next t0) → render → review. An approval digest invalidates when boards change; scene modules expose renderFrame(t)/renderDrawing(k); audio muxed afterwards. Lighter version: DESIGN.md (style prompt, colour roles, type, motion rules, don’ts) + STORYBOARD.md beat table; storyboard.html cells drawn as static sketches at the key moment. **أرقام / params:** approval digest · contiguous shots.
- **الدليل / proof:** `kosif-atlas/skills/2414-animation/9356-produce/SKILL.md` · `kosif-one/projects/water-cycle-animation/DESIGN.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-creative/references/storyboard-recipe.md`

#### STORY-11 · جدول النبضات بعمود «المعلومة الجديدة» · Timed beat sheet with a “new information” column · 📄 موصوف / documented only
- **ماذا / what:** الوقت | الكلام بالضبط | ما على الشاشة | ما الجديد الذي عرفه المشاهد؛ النبضة التي لا تضيف شيئًا تُحذف. — Time | exact words | screen action | new information; a beat that adds nothing is cut.
- **متى أستخدمها / when:** كل ريل أو شرح أو إعلان — every short.
- **كيف / how:** Write before animating; change framing or add evidence as soon as the image has made its point; proof before long explanation; one CTA that follows from what was shown. Convert rows to timeline cues (words.json timings when audio exists). Shot-list variant: # · time · shot type · lens · move · action · lighting · sound · text · transition; reels ≤ one shot per 2.5 s, hook ≤1.5 s. Pencil storyboard frames: grey sketch, thin red lines for camera axis, dashed frame rectangle. **أرقام / params:** 10 shot-list columns · ≤1 shot / 2.5 s.
- **الدليل / proof:** `kosif-atlas/skills/101-video-skills/218-social-video-hooks/SKILL.md` · `100-superskills/skills/storyboard-shotlist/SKILL.md:23` · `kosif-atlas/skills/1096-akbun-editvideo/2449-akbun-vlog-storyboard`

#### STORY-12 · نوتة الحركة · Motion score table · 📄 موصوف / documented only
- **ماذا / what:** لكل نبضة: العنصر والغرض، البداية والنهاية، المدة والتأخير، المنحنى، المحفّز، البديل، وسلوك المقاطعة — قبل الكود. — Per beat: subject/purpose, start/end state, duration/delay, ease, trigger, fallback, interruption — before code.
- **متى أستخدمها / when:** موشن مصمم بدقة (واجهات، هوية، مالية) — precise designed motion.
- **كيف / how:** Stagger by semantic grouping; define reduced-motion and interruption. Example (Arabic finance "ledger finding its structure"): warm paper, charcoal Arabic type, restrained blue rules; the selected account’s rule grows inline-start in 280 ms decelerating; the detail panel follows +80 ms with a 12 px translate settling in 360 ms; reduced motion = instant update. Product example: "aperture discovers the object", 700 ms mask. **أرقام / params:** rule 280 ms · panel +80 ms / 12 px / 360 ms.
- **الدليل / proof:** `kosif-studio/motion/references/motion-director.md` · `100-superskills/skills/kosif-montage-motion/references/motion-director.md`

#### STORY-13 · حزمة المخرج السينمائي ومواصفة المشهد بسبع طبقات · Cinema deliverable package & 7-layer scene spec · 📄 موصوف / documented only
- **ماذا / what:** العنوان والـ logline وخطة المنصة، أوراق مرجعية مقفلة، قائمة لقطات، أوامر لكل لقطة، خطة إضاءة وتدرج، قائمة استمرارية ومخاطر. — Title, logline, platform plan, locked reference sheets, shot list, per-shot prompts, lighting plan + grade, continuity checklist, risks.
- **متى أستخدمها / when:** أفلام توليد بالذكاء أو إنتاج تصوير — AI-generated or shot productions (GEN).
- **كيف / how:** Seven layers written before any prompt: identity, world, action & physics, camera & lens, lighting, materials & atmosphere, colour & story. Shot list # size angle lens motion duration purpose; lighting setup/ratio/Kelvin; English prompts, Arabic explanations; per-shot clips 5–10 s; edit plan cuts on 60/BPM. Continuity: fixed light direction per scene, fixed wardrobe/props, lens matches stated distance. Hand-off folder for another engine: PROMPT.md, START-HERE.md, ATTACH/ parts ≥1600 px, frames/, missing assets named not invented. **أرقام / params:** 7 layers · clips 5–10 s · parts ≥1600 px.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-cinema-director/SKILL.md` · `100-superskills/skills/cinema-director-7layers/SKILL.md:12` · `kosif-one/tools/kosif-omni/skills/kosif-video/SKILL.md` · `kosif-atlas/skills/2681-emulo/10272-video/SKILL.md`

#### STORY-14 · كتل القفل الحرفية للاستمرارية · Verbatim lock-block continuity · ✅ مُثبت هنا / proven here
- **ماذا / what:** أوصاف الشخصية والخلفية والعالم والكاميرا والإضاءة والأسلوب تُجمَّد نصًا ثابتًا يُلصق كما هو في كل أمر، والكود يتأكد من وجودها. — Character, world, camera, light and style descriptions are frozen text pasted unchanged into every prompt; code asserts their presence.
- **متى أستخدمها / when:** أي سلسلة أوامر توليد لنفس الشخصية — multi-shot generated stories.
- **كيف / how:** core.repeated(piece, prompts) / lockCheck(text, lock) + ensure() throw if a lock is missing; used by stickman, romance, fitness, vox, food and kinetic profiles. Proven by the Fastify production-profile tests here (10/10). **أرقام / params:** lock blocks per prompt.
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/core.mjs:6,12` · `fastify-motion-bro/tests/production-profiles.test.mjs` · `fastify-motion-bro/docs/PRODUCTION-GATES.md:5`

#### STORY-15 · ذاكرة الذوق والوصفات · Taste memory & recipe freeze · 📦 بأمر تثبيت / one install
- **ماذا / what:** تتذكر اختيارات المستخدم المتكررة (أنيميشن الترجمة، الإبراز، اللوك، الانتقال) وتجمّد التشغيل المعتمد كوصفة مسماة. — Remembers repeated choices and freezes an approved run as a named recipe.
- **متى أستخدمها / when:** عميل متكرر أو سلسلة حلقات — recurring clients and series.
- **كيف / how:** Basma tasteKeep on export: a value counts when ≥2 times and ≥60% of the last 12 exports, appended to the brief as an Arabic line. HyperFrames media-use: `node scripts/recipe.mjs freeze --name <n>`, `recipe.mjs list`, `prefs.mjs get --json` promote preset/voice/caption identity to defaults. **أرقام / params:** last 12 exports · ≥60%.
- **تثبيت / install:** `cd app && npm install`
- **الدليل / proof:** `app/public/js/00_editor.js:2839` · `kosif-one/vendor/hyperframes/skills/media-use/scripts/recipe.mjs` · `kosif-one/vendor/hyperframes/skills/media-use/references/memory.md`

## الخطاف والافتتاحية — Hooks & openings

_الإطار الأول يتحرك ويُظهر الموضوع؛ الثانية الأولى تُفهم بلا صوت؛ ولا تبدأ بالشعار._

#### STORY-16 · قانون الثانية الأولى · One-second hook law (0–1–3 s) · 📄 موصوف / documented only
- **ماذا / what:** الثانية الأولى تُفهم وحدها: فعل أو نتيجة، والصورة والكلام والعنوان يخدمون فكرة واحدة دون تكرار نفس الكلمات. — The first second stands alone: an action or result; picture, line and title support one idea without repeating words.
- **متى أستخدمها / when:** كل ريل وشورت وإعلان — every short.
- **كيف / how:** Something moves on frame 1 (motion within the first 3 frames: zoom-in, hand move, falling object, light shift); major change before 1.5 s; never open on the logo; hook text ≤4–5 words, bold, high contrast; develop 1–3 s, deliver after 3 s. Pattern interrupt ≤0.5 s for viral formats. Validate by watching the first second muted and with sound. Expectation cue: lock one timing/easing system — inconsistent timing reads as cobbled together. **أرقام / params:** hook 0–1 s (short) / 0–3 s (general) · ≤4–5 words.
- **الدليل / proof:** `kosif-atlas/skills/101-video-skills/218-social-video-hooks/SKILL.md` · `kosif-tool/playbooks/ads.md:25` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/references/montage_grammar.md` · `kosif-atlas/skills/1503-universal-design-principles/3791-expectation-effect-design-cues`

#### STORY-17 · مكتبة الخطافات المسماة · Named hook library · 📄 موصوف / documented only
- **ماذا / what:** أنماط افتتاح بشروط نجاحها: نتيجة أولًا، اختبار مرئي، مشكلة محددة، فعل مفاجئ، سؤال مباشر، رقم دقيق غريب، اعتراف، قبل/بعد، ادعاء مخالف، رقم صادم، استعارة حسية. — Named openers with conditions: result-first, visible test, specific problem, surprising action, direct question, odd-precision number, confession, before/after, contrarian, shocking stat, visceral metaphor.
- **متى أستخدمها / when:** كتابة أول سطر/أول لقطة — writing the opening.
- **كيف / how:** Generate 5–7 variants in different patterns (never five of one kind), label each, recommend one; use verbatim audience language. Viral-opener classifier: 11 shapes (flat contrarian one-liner, odd-precision number, build-in-public confession, quote reframe, mini-list, relatable cold open, listicle promise, story at the tension…). PR/launch extras: concept announcement, before/after teaser, stakes. Ship three distinct 3 s hooks per script as alternate first scenes of the same composition (props switch) for A/B without re-editing the body. **أرقام / params:** 5–7 variants · 3 hooks × 3 s · 11 formulas.
- **الدليل / proof:** `kosif-atlas/skills/2964-pwdev-copy/12448-copy-hooks/SKILL.md` · `kosif-atlas/skills/3035-x-skills/13065-x-hook-extractor/references/classification-rules.md` · `kosif-one/vendor/hyperframes/skills/faceless-explainer/references/story-design.md` · `kosif-atlas/skills/1520-digital-marketing-pro/4133-video-script/SKILL.md`

#### STORY-18 · خطاف الفلوج الصامت · Silent-vlog hook anatomy · 📄 موصوف / documented only
- **ماذا / what:** خطاف بلا كلام قبل فلوج جاهز: افتتاح بارد 5–7 ث، سياق 3–6، فضول 8–12، لقطة فريدة، تشويق — الكل ≤45 ث. — A speech-free hook before a finished vlog: cold open 5–7 s, context 3–6, curiosity 8–12, unique 5–8, teaser 3–5; ≤45 s.
- **متى أستخدمها / when:** فلوجات سفر ويوميات بلا تعليق — travel/diary vlogs.
- **كيف / how:** First cut shows the thumbnail subject, title within the first second; cuts 1.5–4 s (no run of sub-1 s cuts in calm films); last intro cut matches motion/direction of the first main-body cut; hook scenes stay in the body; if no material creates curiosity, propose a cold open only rather than faking tension. Candidate types: result-first, contrast (ordinary vs peak, day vs night), interruption (cut before completion), list. Implement as a hook segment list prepended via ffmpeg concat or composition. **أرقام / params:** cold 5–7 · context 3–6 · curiosity 8–12 · total ≤45 s.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2441-akbun-davinciresolve-searchhook/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2441-akbun-davinciresolve-searchhook/references/hook-principles.md`

#### STORY-19 · الإطار الأول دليل لا تدرّج · Product-proof first frame · 📄 موصوف / documented only
- **ماذا / what:** الافتتاح يُظهر المنتج أو الدليل أو الأطروحة، لا خلفية متدرجة عامة؛ ومشهد المنتج = مُدخل + فعل + نتيجة مرئية. — Open on the product, evidence or thesis, never a generic gradient; product scenes need input, action and a visible consequence.
- **متى أستخدمها / when:** إعلانات وأفلام منتجات وشرح — product films.
- **كيف / how:** Check frame 0 of every film against this rule; label fictional data and never invent metrics. Do-it-first demo: open on the compelling "after", then peel back only the layers the audience needs; map every beat to a pain and cut beats without one. Result-first social recipe (MG-066) lives in FMT. **أرقام / params:** frame 0 check.
- **الدليل / proof:** `kosif-atlas/skills/97-frontend-design-director/206-frontend-design-director` · `kosif-atlas/skills/2375-sales-engineering/9185-demo-design/SKILL.md`

#### STORY-20 · افتتاحيات مرصودة: سؤال، سطران متعاكسان، إشعارات الألم · Observed openers: question, two-line reversal, pain notifications · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** سؤال من سطرين بكلمة ملونة ثم المنتج؛ سطر حقيقة عام ثم سطر بلون مميز يعكسه؛ ثلاث إشعارات مائلة تحكي الألم ثم تطير أيقونة المنتج للمنتصف. — Centred two-line question with one coloured word; neutral fact line then an accent line that reverses it; three tilted OS notifications voicing the pain, then the product icon flies in.
- **متى أستخدمها / when:** افتتاح إعلان أو شرح — ad/explainer openers.
- **كيف / how:** Question: hold ~2 s, accent green on the key word, then move into the product. Reversal: same size, line 2 enters ~1 s later in the accent colour only. Notifications: radius 18 px, shadow 0 12px 30px rgba(0,0,0,.08), tilt ±4°, stagger 300 ms. Ironic cold open: sterile white compliance UI held 2.3 s with a hovering cursor, then hard cut to loud visuals. Space-to-earth opener: starfield + planet with title, then cut to the world. One dot to thought swarm: lone dot + typewriter caption, ripple rings, word count doubling every 0.5 s. **أرقام / params:** hold 2 s · line 2 +1 s · stagger 300 ms.
- **الدليل / proof:** `style:pm-justincooperman-e7bbc4` · `style:pm-kloss-xyz-b9b3f6` · `style:pm-wozu-co-242285` · `style:pm-spearwtf-3c1fd1` · `style:pm-gizakdag-b8c59e`

## هياكل القصة والأقواس الموقوتة — Story structures & timed arcs

_صراع واحد، قرار من البطل، تصعيد، ثم دفعة — بميزانية ثوانٍ لكل قسم._

#### STORY-21 · محرك الصراع وstory_lint · Conflict engine + story_lint (GMC+S) · ✅ مُثبت هنا / proven here
- **ماذا / what:** كل نبضة لها هدف ودافع وصراع ورهان، والبطل يقرر، والرهان يتصاعد، والتأمل ≈20%، والذروة تحل الصراع الخارجي عبر الداخلي. — Every beat has goal, motivation, conflict and stakes; the hero chooses; stakes escalate; ~20% introspection; the climax resolves outer through inner conflict.
- **متى أستخدمها / when:** أي قصة أو إعلان بشخصيات — any narrative piece.
- **كيف / how:** Pipe JSON to `python3 scripts/omni/story_lint.py` (exit 1 on issues): {central_conflict, protagonist, beats[{goal, motivation, conflict, stakes, stakes_level, choice, mode, level, stage}], climax{outer, inner}, plot}. central_conflict must be one of "character vs character|society|nature|technology|supernatural|self". Ran here: a 3-beat Arabic sample scored 72 (flagged a non-canonical conflict label, choices that do not name the protagonist, missing inner-conflict beat). Escalation levers: uncertain outcome, withheld need, personal stakes, no-win choice, no safe haven, team shake-up, tighter clock; four levels (central, story, scene, inner); ~80% action / 20% reflection. **أرقام / params:** score = 100 − 12·issues − 4·warnings · ≥3 beats · introspection warn >30%.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/omni/story_lint.py:32` · `kosif-one/tools/kosif-omni/skills/kosif-video/scripts/story_lint.py:32` · `kosif-one/tools/kosif-omni/skills/kosif-video/references/story-conflict.md`

#### STORY-22 · منتقي الإطار السردي · Story framework chooser · 📄 موصوف / documented only
- **ماذا / what:** رحلة البطل المضغوطة، StoryBrand، PAS للإعلانات القصيرة، BAB للمزايا، ABT للشرح، قوس التحول، دراسة الحالة، وحبكات بوكر السبع. — Compressed hero’s journey, StoryBrand, PAS, BAB, ABT, transformation arc, case study and Booker’s seven plots.
- **متى أستخدمها / when:** اختيار عمود القصة — choosing the spine.
- **كيف / how:** Pick by job: recognition → transformation arc; clarity → ABT (And-But-Therefore); proof → case study; short ad → PAS; feature → Before-After-Bridge; brand story → hero’s journey in 8 stages (ordinary world, call, hesitation, mentor, threshold, trials, reward, return) with the viewer as hero and the product as mentor; never skip the trials. Booker plots: Overcoming the Monster (stages checked by story_lint), Rags to Riches, Quest, Voyage and Return, Comedy, Tragedy, Rebirth. Scene outcomes yes / no / yes-but / no-and — prefer complicating ones in the middle. Run a 3-second "who is the protagonist?" check. **أرقام / params:** hero 8 stages · StoryBrand 7 · plots 7.
- **الدليل / proof:** `kosif-atlas/skills/1503-universal-design-principles/3732-archetypes-storytelling-arcs/references/narrative-frameworks.md` · `kosif-atlas/skills/1164-leaderize-storytelling-framework/2746-leaderize-storytelling-framework/instructions.md` · `100-superskills/skills/kosif-montage-motion/scripts/omni/story_lint.py:24` · `kosif-atlas/skills/1213-story-skills/2883-scene-craft/SKILL.md`

#### STORY-23 · قوس القطعة القصيرة · Short-piece arc (hook → development → pressure → lift → payoff → end) · 🟢 جاهز / ready
- **ماذا / what:** إطار أول مكوَّن ومتحرك، تطوير، ضغط، انفراج، دفعة، ونهاية مقصودة؛ 4–7 نبضات وشيء واحد محمول. — Frame 0 composed and moving, development, pressure, lift, payoff, deliberate end; 4–7 beats, one carried device.
- **متى أستخدمها / when:** أي فيلم 10–60 ث — any 10–60 s film.
- **كيف / how:** Choreography acts: anticipation 10–20%, action 30–50%, reaction 10–20%, resolution 20–30%; something new every 2–4 s. Reel story formula: conflict hook ≤2 s → one escalation → protagonist choice → payoff/CTA, product as the tool of the choice, 15–60 s, ~80% action. kosif-montage-motion lint warns on banned defaults. **أرقام / params:** 4–7 beats · new thing every 2–4 s.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md` · `kosif-one/tools/kosif-studio/motion/references/motion-craft.md` · `kosif-one/tools/kosif-omni/skills/kosif-video/references/story-conflict.md`

#### STORY-24 · وصفة فيلم الخمس ثوانٍ · Five-second film recipe · 🟢 جاهز / ready
- **ماذا / what:** فكرة واحدة، ≤3 نبضات، حامل واحد مرسوم، حركة كاميرا واحدة، ≤8 كلمات، ثم قزحية تغمر إلى العلامة. — One idea, ≤3 beats, one drawn carrier, one camera move, ≤8 words, an iris flood to the brand.
- **متى أستخدمها / when:** سْتينغ علامة أو أسرع تسليم — brand stings, fastest delivery.
- **كيف / how:** Beat 1 0–1.2 s: ring draws in 0.9 s + halo + lines rise; beat 2 1.2–3.6 s: push 1→1.09 and slow ring rotation; beat 3 3.6–5 s: words leave, ring → iris, gold flood + flash, brand words reveal. 1080×1920 30 fps; reference project five_sec. **أرقام / params:** entrance 0–1.2 · hold 1.2–3.8 · payoff 3.8–5 s · ≤8 words.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/five_sec/index.html:31` · `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md`

#### STORY-25 · هيكل الإعلان ووصفة إعلان التطبيق 15 ث · Ad beat skeleton & 15 s app-ad recipe · 🟢 جاهز / ready
- **ماذا / what:** خطاف، وعد، 2–4 مزايا، دليل، دعوة، شعار — ووصفة تطبيق من سبع نبضات بالإطار. — Hook, promise, 2–4 features, proof, CTA, logo — and a seven-beat app ad timed to frames.
- **متى أستخدمها / when:** إعلانات المنتجات والتطبيقات — product/app ads (with FMT ad-slot physics).
- **كيف / how:** Skeleton: hook 0–1.5 s, problem/promise 1.5–4 s, 2–4 features × 2–3 s, proof, CTA 2–3 s, logo 1–1.5 s. 15 s app ad at 30 fps: Sequences at 0/45/120/195/270/345/405 frames with durations 45/75/75/75/75/60/45 — hook ease-out quint, tap spring 14/160, chart 4–6.5 s, notification 6.5–9 s, rating 4.8 counting 9–11.5 s ease-out cubic, CTA 11.5–13.5 s. 30 s spot: 0–3 hook, 3–10 problem, 10–22 solution + proof, 22–30 CTA, VO ≤70 words. Store product: drops on a coloured plinth, turns 30°, three benefit tags pop, price lands. Observed 10 s: 0–1.6 title, 1.6–4.8 day 1, 4.8–7.4 day 2, 7.4–10 title + CTA, each beat holds 0.8 s. Locked shouty lines: hook, thesis, twist, proof, command, handle — ≤4 words each, one per 4 s. **أرقام / params:** frames 0/45/120/195/270/345/405 · VO ≤70 words.
- **الدليل / proof:** `kosif-tool/playbooks/ads.md:36-70` · `kosif-tool/playbooks/ads.md:15-19` · `100-superskills/skills/ad-creative-30s/SKILL.md:23` · `style:pm-gonzalomacagno-2de1a9` · `style:pm-techhalla-7acbc2`

#### STORY-26 · أقواس العروض والإطلاق · Demo & launch arcs with second budgets · 📄 موصوف / documented only
- **ماذا / what:** كلاسيكي 30–60 ث، مشكلة-حل 20–40 ث، تشويق 15 ث، وخمسة أقواس إطلاق (PAS، Future Pacing، Demo Loop…). — Classic 30–60 s, problem-solution 20–40 s, 15 s teaser, and five launch arcs.
- **متى أستخدمها / when:** فيلم منتج أو SaaS — product/SaaS films.
- **كيف / how:** Classic: hook 3, problem 5, magic moment 5, proof 15, social proof 4, invite 4 s. Problem-solution: before 6, after 6, how 10, CTA 4. Teaser: hook 2, demo 8, logo 3, tagline 2. Launch arcs: PAS (hook → pain → agitation → tease → product → proof → CTA), Future Pacing (imagine → name → remove pain → mechanism → outcome → CTA), Demo Loop (question → intro → demo 1 → demo 2 → trust → CTA)… Problem scenes chaotic/red, solution scenes spacious/green; vary durations (short hooks, long proof). Observed SaaS arc 6/6/7/6/5 s (why, tangled UI fragments, snap into real UI, outcomes, logo); problem → obvious fix (show its flaw) → real fix with chapter pills, 8–10 scenes of 5–6 s; promo from a codebase: hook question → logo → N features ×≈4.6 s → social proof → CTA. **أرقام / params:** classic 3/5/5/15/4/4 s · PS 6/6/10/4 · teaser 2/8/3/2.
- **الدليل / proof:** `kosif-atlas/skills/166-demo-video/535-demo-video/SKILL.md` · `kosif-one/vendor/hyperframes/skills/product-launch-video/references/story-design.md` · `kosif-tool/styles/pm-aschapmann-131210/BRIEF.md` · `style:pm-0xnfrith-5be616` · `style:pm-ai-baymax-0ef9dd`

#### STORY-27 · فيلم العلامة: من المشكلة إلى الكشف · Brand film arc: problem → reveal (6 beats) · 📄 موصوف / documented only
- **ماذا / what:** مشكلة، تصعيد، منعطف، كشف، دليل، هبوط — ادعاء واحد لكل نبضة، واستعارة بصرية تحمل المشكلة، والمنتج الحقيقي هو الدليل. — Problem, escalation, turn, reveal, proof, landing — one claim per beat; a metaphor carries the problem; the real product is the proof.
- **متى أستخدمها / when:** أفلام العلامات والهوية — brand films (BRAND).
- **كيف / how:** Storyboard major frames and one motivated transition from "problem world" to "product world"; recurring limited shape set; never redraw the logo from memory; rough-cut for clarity before polish; must still read muted. Metaphor chapters (observed): frame the product as a scientific metaphor (fission → fusion), 2 chapters of 15–18 s, climax at ~60% of runtime; overload beats via HyperFrames overwhelm-surround / scroll-feed blocks (6–9 s). **أرقام / params:** 6 beats · 1 claim per beat · climax ≈60%.
- **الدليل / proof:** `kosif-atlas/skills/101-video-skills/212-brand-film/SKILL.md` · `style:pm-ajith-io-4c248f` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints/overwhelm-surround.md`

#### STORY-28 · هياكل الشرح · Explainer structures · 📄 موصوف / documented only
- **ماذا / what:** شرح مفهوم (طبقة بعد طبقة)، كيف تُعمل (3–6 خطوات على مسرح واحد)، قائمة، قصة شارحة؛ وخمسة أسطر سردية للشرح القصير. — Concept, how-to (3–6 steps on one stage), listicle, story explainer; plus a five-line narration arc for short explainers.
- **متى أستخدمها / when:** دروس وشروحات بلا وجه — faceless explainers (DIAG).
- **كيف / how:** Five-line arc for 15–30 s: hook → misconception → hidden mechanism → example/contrast → memorable truth, second person, longest line ≤14 words, one sentence per 6 s scene (Fastify viral profile, tested). Essay explainer 5–7 min: hook 0:15 (question + personal line), why it matters 0:30, 3–5 principles × 0:35–0:45, my take 0:40, evidence 0:45, misconceptions 0:30, conclusion 0:20, next action 0:15. Observed: 12 chapters × 12 s (establishing move → headline → one visual proof → data panel, hard cuts); question → scan (suspense) → flash lock → big answer → data → restate (30 s: 4/9/6/6/5 s); calm silent 30 s: question → 3 numbered steps ≈8 s each → logo, works muted. **أرقام / params:** ≤14 words/line · 5 lines/30 s · 12×12 s chapters.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/faceless-explainer/references/story-design.md` · `fastify-motion-bro/skills/viral-editorial/SKILL.md:8` · `kosif-atlas/skills/1096-akbun-editvideo/2461-davinciresolve-style-essay/SKILL.md` · `style:pm-blueoctopusai-dd17bd` · `style:pm-tankazunori0914-0fc886` · `style:pm-majorbaguette-fb11d7`

#### STORY-29 · مقاييس أساليب المونتاج الطويل · Long-form edit style metrics (essay · diary · reflection) · 📄 موصوف / documented only
- **ماذا / what:** متوسط طول اللقطة وعدد القطعات في الدقيقة الأولى وحد البقاء على نفس الشاشة لكل نوع. — Average shot length, first-minute cuts and max same-screen time per long-form style.
- **متى أستخدمها / when:** مونتاج فيديو يوتيوب طويل — long YouTube edits (PHOTO/FOOT).
- **كيف / how:** Essay: ASL 3.3 s (2.5–4), 20 cuts in minute one, max same screen 8 s, cards 40% (principles 15, source docs 10, tables 10, logos 5), cuts only. Diary/project: ASL 8 s, 3 cuts in minute one, max 40 s, B-roll 30%, 12-frame dissolves only around timelapses, never hide what got stuck. Reflection: ASL 3.8 s, 15 cuts/min, voice 70% of runtime, 12–20 frame dissolves at beat changes, subtitles bottom-centre 8% margin, 5.5% glyph height, ~18 chars/line. Talking-head cadence: return to the face within 30–45 s of B-roll. **أرقام / params:** ASL 3.3 / 8 / 3.8 s.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2461-davinciresolve-style-essay/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2462-davinciresolve-style-project/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2463-davinciresolve-style-reflection/SKILL.md` · `kosif-atlas/skills/3067-youtube/13229-creator-visual-director`

#### STORY-30 · هيكل يوتيوب الطويل والاحتفاظ · Long-form YouTube skeleton & retention holds · 📄 موصوف / documented only
- **ماذا / what:** خطاف 3 ث بلا لقطات مساندة، افتتاح بارد بوعد صريح، أقسام موسومة، وعلامات خطر انسحاب مع «إمساك» عند كل منها. — Hook in 3 s, cold open with an explicit promise, labelled segments, and 2–3 named drop points each with a hold.
- **متى أستخدمها / when:** سكربت يوتيوب أو بودكاست مصور — YouTube scripts.
- **كيف / how:** Spoken sentences tagged [CHAPTER: name ~m:s], [B-ROLL: …], [IMPROVISE: …] become timeline markers and motion-graphics cue lists. ~150 wpm (15 min ≈2250 words). Retention: hook 0–30 s, context 30–90 s, body = Problem → Solution → Example → Result per point, CTA in the final 60 s, chapters past 6–8 min, promise in 15 s and a re-hook every 2 min; drop points (setup stretch, mid sag, pre-CTA fade) get a re-hook, open loop or pattern interrupt (scene-style switch, camera jolt, kinetic stat card). Tutorial types: feature 15–30 min, update 10–20, use-case 15–30, reaching the first "wow" fast. Six-stage creator pipeline: research → script → SEO → visual brief → editor brief → thumbnail brief, missing inputs marked [MISSING: …]. **أرقام / params:** ~150 wpm · 2–3 risk points · re-hook /2 min.
- **الدليل / proof:** `kosif-atlas/skills/3067-youtube/13226-creator-script-agent/SKILL.md` · `kosif-atlas/skills/192-marketing-skills/617-video-content-strategist/SKILL.md` · `kosif-atlas/skills/1520-digital-marketing-pro/4133-video-script/SKILL.md` · `kosif-atlas/skills/1817-youtube-strategy/4867-yt-outline/SKILL.md`

#### STORY-31 · التريلر بالمازورات وقوس الطاقة · Trailer beat sheet in bars & energy arc · 📄 موصوف / documented only
- **ماذا / what:** تريلر 35–45 ث مكتوب بالمازورات: افتتاح بارد 1–2، سْتينغ اختياري، هبوط 6–8 بلقطة لكل مازورة، جولة، ذروة، نهاية مع إمساك ≥1.5 ث. — A 35–45 s trailer written in bars: cold open 1–2, optional sting, drop 6–8 (one shot per bar), tour, climax, end holding ≥1.5 s.
- **متى أستخدمها / when:** تريلر لعبة أو منتج أو فيلم — trailers (BEAT).
- **كيف / how:** Cold open = most striking moment already in motion, ending on a downbeat hit with flash/hit-stop, no logo first; captions 1–3 words, at most one per bar, nothing that must be read in under a beat; half-bar cuts in the last bars; timeline.json tiling the bar grid; render native 16:9 and 9:16. Energy arc (observed): quiet wides 0–8 s → build with day-night shift 8–20 → fast beat-cut climax 20–32 → silence → title card 32–38. Darkness beat: near-black frame (mean luminance <3%) with one warm ember for 2–3 s before the climax. **أرقام / params:** bars: cold 1–2 · drop 6–8 · tour 3–4 · climax 4–6 · end 2–3.
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4173-game-trailer/references/concept-and-music.md` · `style:pm-theparuchh-6e08c3` · `style:pm-kamstudiolabs-0b0824`

#### STORY-32 · قوس قصة البيانات · Data story arc & progressive layering · 📄 موصوف / documented only
- **ماذا / what:** افتح على الرقم المفاجئ، ضع خط الأساس، 2–3 أدلة، استبصار واحد، ثم التوصية — وكل نبضة تضيف طبقة واحدة. — Open on the surprising number, set the baseline, 2–3 evidence beats, one insight, end on the recommendation — one new layer per beat.
- **متى أستخدمها / when:** أي فيلم أرقام — data films (DATA).
- **كيف / how:** Insight-first title: [number] + [impact] + [context] ("الصادرات +23% بعد الميناء الجديد"), subtitle carries unit, dates, source — if it cannot be written the scene is not ready. Same axes across beats; dim previous layers to 30–40%; before/after panels with identical row order, after values counting from before values, delta in accent only. Every chart must answer a question in the script; a beat that only adds drama is cut; pause any frame and the claim still reads. **أرقام / params:** 3 evidence beats · prior layers 30–40%.
- **الدليل / proof:** `kosif-atlas/skills/3455-business-analytics/14161-data-storytelling/SKILL.md` · `kosif-atlas/skills/3455-business-analytics/14161-data-storytelling/references/details.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10329-scrollytelling-and-parallax-data-visuali/SKILL.md`

#### STORY-33 · أقواس العروض التقديمية كهياكل فيديو · Deck & pitch arcs as video skeletons · 📄 موصوف / documented only
- **ماذا / what:** مستثمر، مبيعات، مؤتمر، SCQA داخلي — بعناوين ادعاء لا عناوين موضوع. — Investor, sales, conference and internal SCQA arcs with claim headlines.
- **متى أستخدمها / when:** فيديو عرض أو pitch مدته 60–90 ث — pitch videos.
- **كيف / how:** Investor: problem, solution, market, product, traction, model, competition, team, numbers, ask (10–12 slides → 60–90 s). Sales: problem, solution, proof, offer, next step. Conference: hook ~30 s, context, insight, evidence, takeaway. SCQA: situation, complication, question, answer. Landing frameworks PAS / AIDA / BAB with alternating proof modes (demonstration, metric, customer, mechanism). Lock the narrative before visuals. **أرقام / params:** 10–12 slides → 60–90 s.
- **الدليل / proof:** `kosif-atlas/skills/1567-tonone/4422-form-deck/SKILL.md` · `100-superskills/skills/pitch-deck-investor/SKILL.md` · `kosif-atlas/skills/198-product-skills/634-landing-page-generator`

#### STORY-34 · قصص الأطفال: كتاب مصور ويوم كامل · Kids stories: picture book & day-to-night arc · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** مشكلة، ثلاث محاولات، حل، درس ضمني؛ أو فيلم ينظم كيوم من الصباح إلى ليل القرية المضيء. — Problem, three attempts, resolution, implicit lesson; or a film structured as one day from morning to a glowing night village.
- **متى أستخدمها / when:** قصة أطفال أو أنشودة — children’s stories (CHAR).
- **كيف / how:** Picture book: 12–32 pages, ≤25 words per page, cliffhanger at the end of each right page. Day arc (observed, 60–80 s, ~6 acts): morning greeting → play → nature → sunset wash with a typewriter line → night village with lit windows and a goodnight line → finale gathering every character. Time-of-day icons (moon + Zzz → sun + coffee steam) signal passing time without text. **أرقام / params:** ≤25 words/page · 6 acts / 60–80 s.
- **الدليل / proof:** `100-superskills/skills/comics-picture-books/SKILL.md:21` · `style:pm-abderrahmen-g-9e8ed0` · `style:pm-nikolajankovic-ce4ff4`

## الذوق والإخراج البصري — Direction & taste

_اختر أطروحة ولغة واحدة، أنفق الجرأة في مكان واحد، واحذف كل ما يبدو «مولّدًا»._

#### STORY-35 · منهج المخرج: أطروحة ونقش ونوتة · Motion-director method: thesis, motif, score · 📄 موصوف / documented only
- **ماذا / what:** قِس حجم المهمة، اقترح 2–3 اتجاهات باستعارة وتكوين وسلوك توقيع ومقايضة، ثم التزم بأطروحة ونقش ومادة وحركة. — Size the job, propose 2–3 directions (metaphor, composition, signature behaviour, trade-off), then commit to thesis, motif, material and movement.
- **متى أستخدمها / when:** بداية أي فيلم مصمم — start of any designed film.
- **كيف / how:** Strong still frame first, then animate to reveal relationships; choose the smallest capable engine; write the motion score (STORY motion score) before code; answer in the user’s language. Visual-argument test: remove the image — if nothing is lost it only decorates; write one sentence of what the viewer must understand in 2 s; define what repeats across a campaign vs what varies; avoid literal illustration (arrow up for growth). **أرقام / params:** 2–3 directions · 2 s comprehension.
- **الدليل / proof:** `kosif-studio/motion/references/motion-director.md` · `kosif-atlas/skills/2976-pwdev-social-media/12583-creative-concept/SKILL.md`

#### STORY-36 · جرأة في مكان واحد · Spend boldness in one place · 📄 موصوف / documented only
- **ماذا / what:** لحظة توقيع واحدة لكل فيلم (كشف منسّق أو تفاعل)، وكل ما حولها هادئ؛ التأثيرات المبعثرة تبدو قالبًا. — One signature moment per film; everything else quiet — scattered effects read as template.
- **متى أستخدمها / when:** مراجعة الستوريبورد — storyboard review.
- **كيف / how:** Mark one "signature beat" in the storyboard; other beats use utility motion. Brand-moment flags in creator videos: return with the find, reveal of what was built, verdict — hold on the face, colour push, longer hold or sting. **أرقام / params:** 1 signature / film · 1–2 per product.
- **الدليل / proof:** `kosif-atlas/skills/1420-frontend-design-skills/3376-anthropic-frontend-design` · `kosif-atlas/skills/3438-ux-design/14121-microinteractions/references/signature-moments.md` · `kosif-atlas/skills/3067-youtube/13229-creator-visual-director/SKILL.md`

#### STORY-37 · قائمة «المظهر المولَّد» الممنوعة · Generated-look blacklist (anti-slop) · 🟢 جاهز / ready
- **ماذا / what:** عنوان في المنتصف على تدرج، كل شيء يظهر بتلاشٍ، نص يظهر من الضبابية، تلاشيات متقاطعة، مشهد داكن بتوهج أخضر/بنفسجي، جسيمات ووميض عدسة بلا سبب، Inter/Roboto للعناوين، #6366f1، ثلاث بطاقات متساوية. — Centred title on gradient, everything fading in, blur-in text, crossfades, dark scene with green/purple glow, gratuitous particles/flares, Inter/Roboto display, indigo #6366f1, three equal cards.
- **متى أستخدمها / when:** فحص ذاتي لكل إطار ستوريبورد — self-check every board.
- **كيف / how:** If a choice would appear for any similar brief, replace it with one specific to the subject. Also flagged: gradient text, left accent stripes, cyan-on-dark, pure #000/#fff (tint toward the accent), cream ~#F4F1EA + clay ~#D97757, everything centred, Syne; uppercase eyebrows ≤ ceil(sections/3); ≤2 zigzag rows; grain >3%, uniform chromatic aberration, glass on light backgrounds, springs without overshoot read cheap. `motion.py lint` warns on several of these unless the brand owns them. **أرقام / params:** grain ≤3% · eyebrows ≤ ceil(sections/3).
- **الدليل / proof:** `kosif-studio/motion/references/motion-craft.md` · `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md` · `kosif-atlas/skills/880-superloopy/1941-superloopy-frontend/references/anti-slop.md` · `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### STORY-38 · شخصية حركة واحدة لكل فيلم · One motion personality per film · 📄 موصوف / documented only
- **ماذا / what:** اختر شخصية واحدة واستخرج كل حركة من مسموحاتها ومحظوراتها: حقل المؤشر، الجولة الكبرى، الآلة المسكونة، النَفَس المحبوس، التايب الحركي، المادة السائلة، السطح الواحد، الوزن الحقيقي. — Pick one personality and derive every move from its allowed moves and bans.
- **متى أستخدمها / when:** تحديد «إحساس» الحركة — setting the motion feel.
- **كيف / how:** cursor-field: nothing moves until the pointer does, instant response, long settle. grand-tour: film in ≤6 acts, one evolving background world, 2–3 depth layers. haunted-machine: decode/glitch, scanline/dither, split-flap, quantised ticks, no smooth easing. held-breath: one near-imperceptible drift, instant cuts, never two moving things, no springs. kinetic-type: only letterforms move, one text behaviour per view. liquid-material: one viscous substance, recovery slower than disturbance. one-surface: shared-element morphs, no entrance choreography. real-weight: overshoot, 1–2 bounces, one gravity, arrive by moving never fading. Render any of them with kosif-tool render_html.cjs. **أرقام / params:** 8 personalities.
- **الدليل / proof:** `kosif-atlas/skills/342-kernel/1223-frontend/motion/held-breath.md` · `kosif-atlas/skills/342-kernel/1223-frontend/motion/real-weight.md` · `kosif-atlas/skills/342-kernel/1223-frontend/motion/haunted-machine.md` · `kosif-tool/tools/render_html.cjs`

#### STORY-39 · من الشعور إلى الأرقام · Feeling → motion vocabulary map · 📄 موصوف / documented only
- **ماذا / what:** حين يقول المستخدم فخم/تقني/مرح/رسمي/هادئ/صحفي ترجمها إلى مدد ومؤثرات وطابع حركة حسب نوع العميل. — Translate فخم/تقني/مرح/رسمي/هادئ/صحفي into durations, effects and a motion character by client archetype.
- **متى أستخدمها / when:** كل طلب يصف إحساسًا — every mood word.
- **كيف / how:** Dramatic: 1–1.5 s fades, scale 0.9→1, spotlight. Techy: neon glow, scramble, grid reveals, particles. Playful: spring bounce, bobbing. Corporate: clean slides. Archetypes: product-led SaaS crisp state changes (120–250 ms feedback); developer tools instrument-like terminal/data progressions; fintech calm, no overshoot; commerce tactile material. Typography by mood: high impact = per-word type + velocity transitions + counters; premium = variable-font + slow transitions; technical = typing + canvas + motion path. Brand archetype (hero, sage, jester…) sets palette temperature and motion energy. **أرقام / params:** feedback 120–250 ms · dramatic fades 1–1.5 s.
- **الدليل / proof:** `kosif-atlas/skills/880-superloopy/1944-superloopy-slides/animation-patterns.md` · `kosif-atlas/skills/97-frontend-design-director/206-frontend-design-director/references/motion.md` · `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md` · `kosif-atlas/skills/1503-universal-design-principles/3731-archetypes-brand-voice`

#### STORY-40 · الأساليب المسماة الثمانية · Eight named visual styles (Swiss Pulse …) · 📄 موصوف / documented only
- **ماذا / what:** Swiss Pulse، Velvet Standard، Deconstructed، Maximalist Type، Data Drift، Soft Signal، Folk Frequency، Shadow Cut — لكل منها لوحة وخط ومنحنى وانتقال. — Eight designer-inspired styles, each with palette, type, ease signature and transition.
- **متى أستخدمها / when:** اختيار لوك جاهز بسرعة — fast look selection.
- **كيف / how:** Swiss Pulse: #1a1a1a + one accent #0066FF or #FFB300, 12-column grid, numbers 80–120 px counting up, expo.out/power4.out, hard cut or iris/zoom. Velvet Standard: navy #1a237e or gold #c9a84c, ALL CAPS tracking ≥0.15em (Latin only), long holds, sine.inOut glide, cross-warp morph. Data Drift: #0a0a0a, #7c3aed, #06b6d4, particles settle into the readable figure, warp transitions. Maximalist Type: loud launches, ridged burn. Deconstructed: raw industrial, glitch/whip pan. Map a mood to a style with the mood→style table. **أرقام / params:** 8 styles.
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/visual-styles.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-creative/references/visual-styles.md`

#### STORY-41 · أنظمة جمالية جاهزة ولا تخلطها · Aesthetic systems & presets — never mix · 📄 موصوف / documented only
- **ماذا / what:** تحريري بسيط، سويسري صناعي، تليمتري CRT، زجاج أثيري، فخامة تحريرية، هيكلية ناعمة، تقييد معايَر — وكل فيلم يتكلم لغة واحدة. — Editorial minimal, Swiss industrial, CRT telemetry, ethereal glass, editorial luxury, soft structuralism, calibrated restraint — one language per film.
- **متى أستخدمها / when:** تثبيت اللوك قبل التصميم — locking the look (COLOR, TEX).
- **كيف / how:** Editorial: bone #F7F6F3, ink #111111, border #EAEAEA, pastel pairs FDEBEC/9F2F2D, E1F3FE/1F6C9F; motion translateY 12 px + fade 600 ms cubic-bezier(0.16,1,0.3,1). Swiss industrial: paper #F4F4F0, ink #050505, one red #E61919, radius 0. CRT: bg #0A0A0A, green #4AF626 on one element, scanlines 2 px period 4 px. Ethereal glass: #050505, backdrop blur ~40 px, white/10 hairlines, rise 64 px + blur over ~800 ms cubic-bezier(0.32,0.72,0,1). Calibrated restraint: #F9FAFB/#18181B, one accent (emerald #10B981, blue #3B82F6, rose #E11D48, amber #F59E0B), spring 100/20, stagger index×100 ms. Seed presets (run WCAG checks): neobrutalism #FDC800/#432DD7, neon #BBF351/#00BCFF, vintage OS #008080/#C0C0C0, arcade #2A3FE5 on black, luxury mono #000/#FAFAFA, dramatic #8B5CF6/#F43F5E. Colour dosage: restrained ≤10% accent, committed 30–60%, full palette 3–4 roles, drenched 100%. Decide dark vs light from one sentence about who watches, where, under what light. **أرقام / params:** dosage ≤10 / 30–60 / 100%.
- **الدليل / proof:** `kosif-atlas/skills/2981-designer-skill/12625-designer-skill/reference/aesthetic-systems.md` · `kosif-atlas/skills/3593-bespoke-design-system/14409-bespoke-design-system/source-design-systems/neobrutalism/DESIGN.md` · `kosif-atlas/skills/342-kernel/1223-frontend/variants/abyss.md` · `kosif-atlas/skills/1394-stark/3329-web-design`

#### STORY-42 · قواعد تصميم الحركة · Choreography rules (build · breathe · resolve, 1/3 rules) · 🟢 جاهز / ready
- **ماذا / what:** كل مشهد: بناء متتابع 0–30%، تنفّس بحركة محيطية واحدة 30–70%، حسم 70–100%؛ البطل يقود، حركة مضادة، العمق بالسرعة. — Every scene: staggered build 0–30%, one ambient motion 30–70%, decisive resolve 70–100%; hero leads, counter-motion, depth by speed.
- **متى أستخدمها / when:** كتابة توقيت كل مشهد — timing every scene (EASE).
- **كيف / how:** Enter ~0.4 s, exit ~0.25 s (exits ≈40% faster); total stagger <500 ms regardless of count; slowest scene ≈3× slower than fastest. Counter-motion 20–30%; depth speeds 1× / 0.5× / 0.2×; no move over 1/3 of the frame without an intermediate key; with 3+ elements ≤1/3 move at once (observed cap: ≤3 independently moving groups); something new every 2–4 s; one origin per group. Anti-slideshow rule: every meaningful shot carries continuous time-driven motion — verify with frame-hash differences across a scene. Object test per beat: on-screen phrase, a weighted body doing a named verb, the surface — a word is not a body. **أرقام / params:** 30/40/30% · enter 0.4 / exit 0.25 s · stagger <500 ms.
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/motion-principles.md` · `kosif-studio/motion/references/motion-craft.md` · `fastify-motion-bro/AGENTS.md:13` · `100-superskills/skills/motion-director-pro/references/motion-floor.md`

#### STORY-43 · إخراج النبضة بأفعال الطاقة · Beat direction with energy verbs · 📄 موصوف / documented only
- **ماذا / what:** كل نبضة تجربة: مفهوم، إشارة الصوت، وصف سينمائي بخمسة عناصر على الأقل في المقدمة والوسط والخلفية، وكل عنصر له فعل. — Each beat is an experience: concept, VO cue, ≥5 elements across FG/MG/BG, and a verb for every element.
- **متى أستخدمها / when:** كتابة الستوريبورد التفصيلي — detailed storyboards.
- **كيف / how:** Energy verbs: high SLAMS/CRASHES/PUNCHES/STAMPS/SHATTERS; medium CASCADES/SLIDES/DROPS/FILLS/DRAWS; low types on/FLOATS/morphs/COUNTS UP. 8–10 visual elements per beat, 2–3 techniques per beat, ≥2 depth layers, slow push 1→1.04 per beat; declare rhythm up front (fast-fast-SLOW-fast-SHADER-hold). Technique combos by energy: high impact = per-word type + velocity transitions + counters; cinematic = path drawing + video compositing + CSS 3D; technical = typing + procedural canvas. Website films: use ≥50% of captured screenshots, logo in first and last beat, ≤2 consecutive text-only beats; print an asset table first. **أرقام / params:** 8–10 elements · 2–3 techniques · push 1→1.04.
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/step-4-storyboard.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-creative/references/beat-direction.md` · `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md`

#### STORY-44 · عدسات النقد قبل الرندر · Creative review lenses & aesthetics council · 📄 موصوف / documented only
- **ماذا / what:** مروران: اطرح حتى يقول كل إطار نية واحدة (سبعة صفوف ← درجة من 10)، ثم 12 عدسة فنية تتحدى المشهد. — Two passes: subtract until each frame states one intent (7 rows → score /10), then 12 art-direction lenses challenge the scene.
- **متى أستخدمها / when:** قبل الرندر النهائي — before final render (QA).
- **كيف / how:** Score: 7/7 → 10, 6/7 → 9, 5/7 → 7. Lenses VA01–VA12: spatial worldbuilder, character designer, action choreographer, cinematographer, lighting artist, colourist, VFX designer, atmosphere & weather, materials & texture, production designer, composition director, beauty critic. Basma autopilot critique: a 6-frame contact sheet (3 columns, 264 px tiles, timestamps) scored on hook, readability, motion, variety, safe zones, brief, sound sync, identity, then fixes the three worst problems (needs its AI key). **أرقام / params:** 7 rows → /10 · 12 lenses · 6-frame sheet.
- **الدليل / proof:** `kosif-atlas/skills/3438-ux-design/14123-steve-jobs-design-review/SKILL.md` · `kosif-one/tools/kosif-omni/skills/kosif-visual-aesthetics-council/SKILL.md` · `app/public/js/00_editor.js:2394`

#### STORY-45 · التعلم من المرجع دون نسخه · Learn from references without cloning · ✅ مُثبت هنا / proven here
- **ماذا / what:** لكل مرجع وظيفة واحدة (حركة، كاميرا وإيقاع، أو هوية) مع قائمة «لا تنسخ»، واستعر القواعد لا المحتوى. — Give each reference one job with a do-not-copy list; borrow grammar, never content.
- **متى أستخدمها / when:** «اعمل زي الفيديو ده» — "make it like this".
- **كيف / how:** `python3 motion.py study REFERENCE.mp4 --out DIR` measures cuts, shot lengths, first change, motion energy, stillness and palette into style_guide.md (verified here on a 6 s test clip: wrote style_guide.md, study.json, contact.png, first_frame.png, review.md). Keep only what is constant across ≥3 films; anything unique to one is its costume; state "do not average the references". Never copy scripts, logos, characters, footage or people; if you cannot open the frames, say so and ask for 5–8 screenshots. For famous infographics, redesign so it could not be mistaken for the reference (palette, type, layout, cadence). Basma DNA.toStyle turns a measured fingerprint into caption, zoom, transition and grade settings without a model. **أرقام / params:** constant across ≥3 refs · 5–8 screenshots.
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/qa.py:1` · `kosif-atlas/skills/2681-emulo/10272-video/SKILL.md` · `fastify-motion-bro/AGENTS.md:8` · `kosif-atlas/skills/2690-build-web-data-visualization/10335-visualization-strategy-and-critique/SKILL.md`

#### STORY-46 · قواعد الصدق في الوعود · Honesty rules for claims · 📄 موصوف / documented only
- **ماذا / what:** «واقعي» = لوحة رقمية مضاءة بواقعية لا صورة فوتوغرافية؛ الأرقام من المصدر فقط؛ لا تدّعي رؤية ما لم تفتحه. — "Realistic" means a realistically lit painting, not a photo; numbers only from the source; never claim to have seen what you did not open.
- **متى أستخدمها / when:** كل وعد للمستخدم — every promise.
- **كيف / how:** State limits up front (code from a description never matches a photo; exact match only via image code or exact mode). Facts only from the cue: scene headline is the number the cue said, else its longest word — never a demo value (audio2motion.head, tested). Document → film: summarise faithfully, never invent facts; image-only PDFs are rejected with an OCR hint. Label fictional data.
- **الدليل / proof:** `kosif-studio/references/drawing-guide.md:93` · `kosif-studio/motion/audio2motion.py:49` · `kosif-studio/tests/test_audio2motion.py:43` · `app/public/js/10_studio.js:2787`

## أدوات السرد والنقوش — Story devices & motifs

_شيء واحد يعبر اللقطات، فصول مرقمة، ونهاية تُغلق الدائرة — هذه أدوات المخرج الصغيرة._

#### STORY-47 · الشيء المحمول عبر الفيلم · Travelling device / hero-object thread · 🟢 جاهز / ready
- **ماذا / what:** جسم واحد (نقطة، كرة، شمس) يعيش في كل لقطة: يهبط، ينبض على الإيقاع، يصير زرًا ثم نقطة الجملة ثم نقطة الشعار. — One object survives every cut — lands, pulses on beats, becomes a button, a full stop, the logo dot.
- **متى أستخدمها / when:** ريلز العروض والهوية — showreels, identity films (BRAND, TRANS).
- **كيف / how:** KOSIF showreel: dot #E4342F on #0F1211, rides a sampled path (60 samples) on a 120 BPM clock, pulses 1.25/1.2 scale (0.06 s out, 0.22 s settle), squashes on landing, opens the iris onto footage, ends as the lockup’s full stop (15 s 1080p60, rendered kosif_motion_showreel.mp4). Observed: coral dot ≈2.5–3% of height reused as i-dot, full stop and decimal with squash 0.7/1.3; orange ball #ff5a1f at the same screen position at each cut for a match. Dua film variant: the sun climbs and on the key line lifts with a heavy spring into the rosette (flash peak .55, scale 1→1.18→1). Evolution chain: each scene’s object is born from the previous (point → line → circle → sphere → lens → ball → world → full stop), 2.5–3 s per step, no cuts. **أرقام / params:** pulse 1.25 / 0.06 + 0.22 s · squash 0.7/1.3 · 120 BPM.
- **الدليل / proof:** `kosif-studio/motion/projects/showreel/index.html:66` · `kosif-studio/out/kosif_motion_showreel.mp4` · `kosif-one/projects/thursday-dua-animation/source/index.html:153-161` · `style:pm-1littlecoder-9fef89` · `style:pm-leonkohli-6dc01b` · `style:pm-hbcoop-de365c`

#### STORY-48 · كشف جملة الذروة · Payoff-line detection · ✅ مُثبت هنا / proven here
- **ماذا / what:** يجد سطر الذروة: بعد سطر قصير متكرر (كافح… كافح) الجملة التالية تحسمه؛ في الأغاني آخر عودة للازمة؛ وإلا أكثر جملة منبورة في آخر 40%. — Finds the climax line: after a repeated short line the next sentence resolves it; in songs the last refrain return; else the most stressed sentence in the last 40%.
- **متى أستخدمها / when:** تعليق صوتي، أغنية، دعاء — voice, song or dua films (SYNC, ARAB).
- **كيف / how:** direct.plan / verse.plan: refrain = line heard ≥2×; payoff line size ×1.22, light sweep, flare, held +2.2 s, then dip to black. Tested here (test_direct_plans_like_an_editor, test_verse_reads_a_text_like_a_lyricist). **أرقام / params:** size ×1.22 · hold +2.2 s · last 40%.
- **الدليل / proof:** `kosif-studio/motion/direct.py:116` · `kosif-studio/motion/verse.py:280` · `kosif-studio/tests/test_studio.py:910`

#### STORY-49 · من المعنى إلى الرمز · Concept-to-symbol motifs · 🟢 جاهز / ready
- **ماذا / what:** معنى الكلمة المفتاحية يختار رمزًا يُرسم بجوار السطر، والأرقام المنطوقة تصير عدّادًا، والرموز مقننة كي لا تصير ورق حائط. — A keyword’s meaning picks a symbol drawn beside the line; spoken numbers become a counter; symbols are rationed.
- **متى أستخدمها / when:** أفلام الكلمات من الصوت — verse/voice films.
- **كيف / how:** verse.concept_of: 12 concepts (sun, moon, heart, clock, money, trophy, road, question, check, home, rain, light) matched by Arabic roots + English prefixes, stripping و ف ب ل ال. Hero metaphor objects for kinetic beats (Fastify, tested): rocket, chess piece, hourglass, blank glass cube, magnifying glass, paper staircase, generic interface — "no text on the object". **أرقام / params:** 12 concepts · 7 metaphor objects.
- **الدليل / proof:** `kosif-studio/motion/verse.py:173` · `kosif-studio/motion/verse.py:322` · `fastify-motion-bro/scripts/profiles/kinetic-flow.mjs:103,110-111`

#### STORY-50 · أنظمة الفصول المرقّمة · Chapter label systems · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** رقم الفصل + اسم بأحرف كبيرة + عنوان فرعي مائل، أو «• 0N / فعل الاسم» فوق العنوان، أو دائرة سوداء برقم أبيض. — Chapter number + caps label + italic subtitle, "• 0N / VERB THE NOUN" eyebrow, or a black circle with a white number.
- **متى أستخدمها / when:** شروحات وعروض متعددة الأجزاء — multi-part explainers/promos.
- **كيف / how:** Variants seen: mono label at 1.2% frame height with accent dot; "[0N] WORD" heavy caps top-left; 14 px numbered chip; yellow numbered title top-left, FadeOut all, short empty beat (12–14 sections for a 7 min lesson, fade 0.5–1 s); per-unit framing that resets an "elapsed 0 → 1.000 s" bar each chapter; showreel chapters named by skill, 8 × 1.6 s + 2 s end. For Arabic use Arabic-Indic or Latin digits consistently (ARAB-73). **أرقام / params:** eyebrow 1.2% h · 8 × 1.6 s showreel.
- **الدليل / proof:** `style:pm-codestackr-c071bf` · `style:pm-elliot-garreffa-f334bc` · `style:pm-moguzbulbul-6311b6` · `style:pm-linearuncle-5d2bae` · `style:pm-nolkeeg-bf062e` · `style:pm-shinskinakamoto-20190b`

#### STORY-51 · خواتيم الملخص · Recap endings (grid · collage · board · progress) · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** شبكة من عمودين لكل العناصر، أو كولاج للمشاهد السابقة يطير إلى شبكة 3×3، أو لوحة خلاصات ملونة، أو عداد رندر وهمي يملأ شريط الفصول. — Two-column summary grid, collage of earlier scenes flying into a 3×3, colour-coded takeaway board, or a fake render-progress recap.
- **متى أستخدمها / when:** نهاية شرح أو قائمة أو ريل عرض — recap before the logo.
- **كيف / how:** Grid: index in accent, title, one-line hook, rating, recommendation bar, row stagger 120 ms. Collage: tilted thumbnails rotate ±4°, stagger 50 ms, 500 ms easeOutBack. Board: 5 one-line takeaways each in its chapter colour + boxed footnote, one line per narration sentence. Progress: blue screen, spinner + filename, rolling percent 0 → 99 in ≈1.5 s with digit motion blur, filmstrip of chapters filling left-to-right (RTL for Arabic). Reflective ending: 2–3 numbered open questions held ~8–10 s each. **أرقام / params:** row 120 ms · collage 50 ms / ±4° / 500 ms.
- **الدليل / proof:** `style:pm-gigabit-million-16b3a0` · `style:pm-motiondsgnr-9dcfa6` · `style:pm-tak3sh8-be5012` · `style:pm-levabashidze-2d713a` · `style:pm-linearuncle-5d2bae`

#### STORY-52 · الإطار المغلق والحلقة · Bookends & loop endings · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** افتح وأغلق على نفس البطاقة أو العنوان أو الإطار الهادئ، أو عُد لنفس الفيلم ليتكرر الفيديو بلا نهاية. — Open and close on the same card/title/calm frame, or return to the opening so the video loops.
- **متى أستخدمها / when:** ريلز تعاد، سير ذاتية، أفلام هادئة — loops, CVs, calm films.
- **كيف / how:** Title bookend: same tracked title + subtitle, ending version over the darkened final image, fade 1.5 s (Latin tracking only). Control → escape → chaos → control: acts named in a HUD, bookended by the same calm frame (5 acts / 30 s). Loop bookend: open on rapid output previews (~0.5 s cuts), explain, end on the same film. Code-loop outro: only a blinking cursor remains. Calm porthole ending: circle mask with slow loop, italic word, title. Seamless technical loop: FMT seamless loop. **أرقام / params:** fade 1.5 s · intro cuts ~0.5 s.
- **الدليل / proof:** `style:pm-rebutonepress-810f78` · `style:pm-pankajkumar-dev-0bee87` · `style:pm-lemomo-ai-0d9cff` · `style:pm-web3wesley-7bb108` · `kosif-tool/styles/pm-jake11moran-a269c4/BRIEF.md`

#### STORY-53 · بطاقات الجملة والصمت · Statement cards, caption beats & silence · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** قطع إلى أسود بجملة واحدة عريضة لتغيير الفصل، أو سطر قصير على أسود يتلاشى ويثبت، أو صمت في ظلام قبل الذروة. — Hard cut to black with one bold sentence to change chapter; short line on black; silence in darkness before the climax.
- **متى أستخدمها / when:** تغيير الفصول وبناء التوتر — chapter turns and tension.
- **كيف / how:** Statement card: white weight 800, hold 1.5–2 s, then cut back to UI. Narrative caption beat: fade 400 ms, hold 2 s. Darkness beat: mean luminance <3% with one ember for 2–3 s. Calm lock-up outro after a frenzy: black, centred wordmark, 3-line tagline, handles, hold 3–4 s, fade 400 ms. Made-with-code end card: three short bold lines + muted credits row, hold 3–5 s. Arabic: no tracking on the tagline. **أرقام / params:** hold 1.5–2 s · fade 400 ms · luminance <3%.
- **الدليل / proof:** `style:pm-lester-tyy-f897f7` · `style:pm-marklaunches-3b9492` · `style:pm-kamstudiolabs-0b0824` · `style:pm-micheleharmonic-77628e` · `style:pm-kantamk-61f410`

#### STORY-54 · تبدّل المزاج: ظلام/نور، نهار/ليل · Mood shifts: dark↔light acts, day/night interludes · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** بدّل الثيم في منتصف الفيلم ليعلن انتقال المشكلة إلى الحل، أو أدخل مشهدًا نيليًا واحدًا «بينما تنام» ثم عد للنور. — Switch theme mid-film to mark problem → solution, or insert one indigo "while you sleep" scene.
- **متى أستخدمها / when:** أفلام المنتجات والقصص — product/story films (COLOR).
- **كيف / how:** Crossfade 600 ms into the interlude; 3D world moods (earth crystal world, tested): locked glow .25 speed .55, open glow .6 speed 1, unlock glow 1.6 speed 1.6, lerp k=.04 per frame, pulse adds up to 3 and decays ×0.92 per frame. Genre-hop: keep one message but re-skin each beat in a distinct genre (palette, font, texture, framing) for 6–8 s each; climax gag: hold a browser-default page (Times, white) for 3–5 s. **أرقام / params:** crossfade 600 ms · lerp .04 · genre 6–8 s.
- **الدليل / proof:** `style:pm-sudo-kiran-b055de` · `style:pm-sachaarbonel-8f14f4` · `kosif-earth-ci-fork/ui/art/crystal-world.js:96` · `kosif-earth-ci-fork/tools/crystal_world.test.mjs` · `style:pm-emollick-8661a8`

#### STORY-55 · نبضات كوميدية وعاطفية · Comic & emotional beats · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** فقاعة كلام مضحكة، ختم ميم، مؤشر عملاق خصم، اعتراف بالكليشيه، انقلاب شخصية لتختبئ، نقل التوهج من الشخصية للشيء. — Speech-bubble gag, meme stamp, giant cursor antagonist, self-aware cliché, character flip to hide, glow transferred from character to object.
- **متى أستخدمها / when:** ريلز ترفيهية وقصص شخصيات — entertainment and character reels (CHAR).
- **كيف / how:** Bubble: anchored to the projected character position, pop 0→1.1→1 back-out, hold 1.5 s, white fill, 2 px black stroke, radius 10 px, tail triangle. Stamp: scale 1.4→1 in 3 frames, hold 2 s after escalating damage. Flip: rotate 180° to a blank back face in 600 ms easeInOut, then return. Paper airplane: bezier flight 800 ms, unfold scaleX 0→1 in 300 ms with crease lines. Accumulating props: each compliment adds a persistent prop (text-on-path sash, clips), drop-in 400 ms back-out. Question-mark twist: assumption 1.5 s → scramble + strike 1.5 s → "?" hold 1 s → promise. **أرقام / params:** pop 0→1.1→1 · stamp 3 frames · flip 600 ms.
- **الدليل / proof:** `style:pm-gorden-sun-041f56` · `style:pm-0xevinho-3777d8` · `style:pm-kamstudiolabs-c9bb28` · `style:pm-anilraok-eff262` · `style:pm-jake11moran-a269c4` · `style:pm-robj3d3-b18fad`

#### STORY-56 · نبضات الحجة · Argument beats (pain triptych · THE FIX bar · cost reframing · paper-form) · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** ثلاثة أعمدة ألم بأمثلة واجهة صغيرة، شريط «الحل» بقاعدة واحدة وإحصاء تكرار، رقم خسارة كبير أمام سعر يومي صغير، واستمارة ورقية تمثل الطريقة القديمة تُشطب بالأحمر. — Three pain columns with mini-UI proof, a "THE FIX" bar with a frequency stat, big loss vs tiny daily price, and an old-way paper form struck in red.
- **متى أستخدمها / when:** إعلانات وشروح مقنعة — persuasive explainers and ads.
- **كيف / how:** Triptych: icon chip, short title, mini UI, one-line caption, built right-to-left for Arabic, stagger 300 ms, radius 12 px. FIX bar: cream full-width card, green pill, one-sentence rule, divider, "≈1 in N" stat, slide-up 400 ms easeOutCubic. Paper form: hard cut from the dark world to an off-white form (black header bar, numbered fields), red marker strike drawn in 400 ms. Phase captions: steady / burst / recovery with a final takeaway in accent. **أرقام / params:** stagger 300 ms · slide-up 400 ms · strike 400 ms.
- **الدليل / proof:** `style:pm-aschapmann-131210` · `style:pm-henkvaness-0e06af` · `style:pm-thayto-dev-44b911` · `style:plotter` · `style:pm-parkerrex-1a54fe`

#### STORY-57 · جسر الوميض والسحب للخلف إلى ملصق · Flash bridge + poster pull-back reveal · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** ادفع داخل الضوء حتى يملأ الإطار، وميض بلونه، ثم ابدأ المشهد التالي مكبَّرًا داخل ملصق صغير لنفس المشهد وارجع لتكشف الحائط والعنوان. — Push into light until full frame, flash to its colour, start the next scene zoomed inside a small poster of itself and pull back to reveal wall + headline.
- **متى أستخدمها / when:** الانتقال بين عالمين أو خاتمة — world transitions and endings (TRANS, CAM).
- **كيف / how:** Flash ~200 ms; pull-back ~2 s easeOutCubic from inside a small <svg viewBox> poster. Step-out-of-painting outro: the 3D scene flattens back into a framed canvas on a wall. **أرقام / params:** flash 200 ms · pull-back 2 s.
- **الدليل / proof:** `style:fake3d` · `kosif-tool/styles/pm-mandelduck-95fd08/BRIEF.md`

#### STORY-58 · نبضات العالم والحالة · World beats: surreal props, overload, one-take, beacon · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** أشياء قديمة تطفو في السماء، كل شيء يتسارع حول مركز هادئ، لقطة واحدة بلا قطع يقودها قسم الموسيقى، ومنارة تنبض لتصوير مفهوم مجرد. — Floating vintage props, overload closing in on a calm centre, a cut-free single take driven by music sections, a beacon visualising an abstract concept.
- **متى أستخدمها / when:** أفلام فنية وشروحات علمية — art films, science explainers.
- **كيف / how:** Drift 10–30 px/s, rotation 2–8 °/s. Overwhelm surround (HyperFrames block, count 16 (8–24), intensity 0.5–2). Single take: density of launches rises toward the climax, HUD shows state names. Beacon: proper interval 1 s × 1/√(1−r_s/r) — observed interval grows and redshifts near the horizon. Life-as-a-game metaphor: skills as levels, progress as score, end card "Player 1". **أرقام / params:** drift 10–30 px/s · 2–8 °/s.
- **الدليل / proof:** `style:pm-koldo2k-5cff87` · `kosif-one/vendor/hyperframes/registry/components/overwhelm-surround/overwhelm-surround.html` · `style:pm-kamstudiolabs-447565` · `style:pm-rebutonepress-810f78` · `style:pm-ibrahimwasim240-809370`

## محركات الأنواع والأفلام الجاهزة — Genre engines & ready films

_قوالب قصة تعمل فعلًا: من مقطع كلام إلى ريل مُخرَج، ومن موقع إلى فيلم إطلاق، ومن نوع إلى خمس نبضات._

#### STORY-59 · مونتاج مُخرَج لمقطع كلام · Directed edit of a talking clip · ✅ مُثبت هنا / proven here
- **ماذا / what:** يبني تكوينًا قابلًا للتحرير من مقطع كلام: لوحة نظيفة، سلسلة صوت، دفع نحو المتكلم، كلمة مفتاحية لكل جملة بخط كبير وضربة، أرقام كحلقات ساعة، كلمة القطع كسطح انتقال، ودفعة ثم إظلام. — Builds an editable composition: clean plate, voice chain, subject push, a stressed keyword per sentence with a punch, numbers as clock rings, the cut word as a transition plane, payoff then dip.
- **متى أستخدمها / when:** المستخدم أرسل فيديو يتكلم فيه — a talking-head upload (with SYNC, ARAB-62).
- **كيف / how:** `python3 direct.py CLIP.mp4 --name NAME --size 1080x1920 --words X.words.json --accent "#E7B65A" --credit "…" [--fix "a=b"] [--render]` → projects/NAME/edit.js (also `kmotion direct`). Plate libx264 slow crf 15 -g 1; keyword 190 px; captions 54 px ≤6 words; hook releases at the second word; end = last word + 0.35 s; stress = loudness × length. Planning is tested here; full render needs faster-whisper (pip install faster-whisper) and the clip. **أرقام / params:** keyword 190 px · captions 54 px ≤6 w · end +0.35 s.
- **الدليل / proof:** `kosif-studio/motion/direct.py:231` · `kosif-studio/tests/test_studio.py:910` · `100-superskills/skills/kosif-montage-motion/scripts/direct.py`

#### STORY-60 · قوس الريل التحفيزي (FINAL_EDIT) · Motivational talking-reel arc (FINAL_EDIT) · 🟢 جاهز / ready
- **ماذا / what:** قوس مثبت 20 ث: تجميد خطاف ← رسم الإدراك ← دفء الحلم ← أمثلة دقيقة ≈1.2 ث ← ضربات ضغط ← انفراج بلون مميز ← كلمة ضخمة كانتقال ← دفعة ← إظلام. — A proven 20 s arc: hook freeze → realisation graphic → dream warmth → micro examples ≈1.2 s → pressure punches → lift in accent → giant-word transition → payoff → dip.
- **متى أستخدمها / when:** تعليق صوتي تحفيزي أو نصيحة — motivational voice clips.
- **كيف / how:** Time map: 0 hook, 1.56 clock, 3.28 dream, 5.22 weight, 7.24 car, 9.5 pressure, 11.3 lift, 13.14 word transition, 14.62 time drain, 16.02 build, 17.26 payoff, 18.42 close, 20.06 dip. Delivered at 20.57 s 1080×1920 30 fps, −14.4 LUFS, TP −2.7 dBTP. Premium edit by hand: decaption, Lanczos restore, push 100→108%, 3 text levels, micro-graphics ≤1.5 s, payoff alone, two reviewers P0/P1/P2. **أرقام / params:** 20.57 s · −14.4 LUFS · push 100→108%.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:188` · `kosif-studio/out/FINAL_EDIT/EDIT_NOTES.txt` · `100-superskills/skills/kosif-montage-motion/SKILL.md`

#### STORY-61 · فيلم الإطلاق من الموقع أو الكود · Launch video from a site or codebase (/brag) · 🟢 جاهز / ready
- **ماذا / what:** اجمع مادة المنتج، أجب عن 9 أسئلة فحص، ابنِ ستوريبورد من رحلة المستخدم الحقيقية، ثم سلّم بغلاف ونص مشاركة — 15–25 ث. — Gather product material, answer a 9-question rubric, storyboard the real user flow, deliver with poster and share copy — 15–25 s.
- **متى أستخدمها / when:** إطلاق تطبيق أو موقع — app/site launches (UI).
- **كيف / how:** `python3 scripts/kmotion.py brag init DIR|URL --tone default|polished|yc-parody|chaotic|deadpan|cinematic|app-store --format landscape|vertical|square --duration 20` → storyboard; `brag deliver OUT --film film.mp4` (poster + gate; share copy ≤280 chars tested by test_launch). Shape: hook 2–3 s, reveal 2–4 s, 2–3 highlights (entry → action → result), outro 2–4 s, 18–22 s ideal. Tones: default 4–5 scenes soft; polished 3–4 long holds, crossfade 0.6–0.8 s; yc-parody deadpan hard cuts; chaotic 6–8 scenes some <2 s, flash/zoom cut 1.2→1.0; deadpan 3–4 scenes, 0.8–1.0 s fades; cinematic big type, dramatic wipes, 0.95→1.0; app-store 4–6 feature cards, 0.35–0.45 s slides. Website 7-step variant: capture → brand cheat sheet → narration → beat storyboard → VO + timestamps → compositions → validate. **أرقام / params:** 15–25 s · share ≤280 chars · 7 tones.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/launch.py:29` · `100-superskills/skills/kosif-montage-motion/references/launch-video.md` · `100-superskills/skills/kosif-montage-motion/tests/test_launch.py` · `kosif-one/vendor/brag/skills/brag/references/step-1-inspect.md`

#### STORY-62 · بنية ريل العرض 15 ث · Showreel beat structure (120 BPM) · 🟢 جاهز / ready
- **ماذا / what:** ادعاء خطاف، ضغطة زر، عدّاد تقدم، منحنى نابض يُرسم بالقلم، قانون يُكتب، قزحية تسقط إلى لقطات حقيقية، بطاقة حقائق، انهيار للداخل، شعار. — Hook claim, button press, progress counter, pen-drawn spring curve, typed law, iris to real footage, fact card, implode, lockup.
- **متى أستخدمها / when:** ريل الاستوديو أو المنتج — studio/product reels.
- **كيف / how:** 1920×1080 60 fps on beats b4, b6, b9, b12, b15.8, b21, b24.6, b26 of a 120 BPM grid; Arabic claims «كل إطار برنامج», «نابض، لا منحنى», «الإطار دالة في الزمن». Project files projects/showreel + score.json + cues.json; rendered mp4 kept in kosif-studio/out. **أرقام / params:** 15 s · 60 fps · 8 beat cues.
- **الدليل / proof:** `kosif-studio/motion/projects/showreel/index.html:66` · `100-superskills/skills/kosif-montage-motion/scripts/projects/showreel/index.html:38` · `kosif-studio/out/kosif_motion_showreel.mp4`

#### STORY-63 · فيلم المختبر SHAPE→RANK · Product-lab film (SHAPE → JOINT → LOAD → BREAK → SWAP → RANK) · 🟢 جاهز / ready
- **ماذا / what:** فيلم تعليمي بنطاقات مراحل مسماة تقود الرقائق والترجمة والكاميرا والمؤثرات معًا، بعدسة تتوقف عند كل جزء. — An educational film cut into named stage bands that drive chips, captions, camera and effects together.
- **متى أستخدمها / when:** شرح منتج أو هندسة أو مقارنة — product/structure explainers (3D, DIAG).
- **كيف / how:** Bands B = {joint .85, load 1.65, brk 2.55, swap 3.35, rank 4.15, end 5.0} (5 s twin), T_BREAK 2.66; load ramps easeInOut to 3.0× then back; 20 s lab: lens stops at 0/3/6.5/9.5/13/16/18 s, fov 30, bilingual callouts, deliberate dip #0f1512 for .6 s. Animation illustrates, it is not proof. **أرقام / params:** stops 0/3/6.5/9.5/13/16/18 s · fov 30.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js:8` · `100-superskills/skills/kosif-montage-motion/scripts/projects/lab_rabbit_lion/src/main.js:40` · `100-superskills/skills/kosif-montage-motion/references/STRUCTURAL_TWIN.md`

#### STORY-64 · قصة بلا كلام: مرشد وقفزة · Wordless short: a guide and a leap · 🟢 جاهز / ready
- **ماذا / what:** بطل يتبع ضوءًا (فراشة) في عالم معادٍ وجميل، يتوقع العقبة، يقفز، يهبط، ويلتفت للجمهور؛ العنوان يتلاشى مبكرًا والشعار في النهاية. — Hero follows a light through a hostile-but-beautiful world, anticipates, leaps, lands, looks back; title early, tagline last.
- **متى أستخدمها / when:** أفلام قصيرة صامتة أو إعلانات عاطفية — silent shorts.
- **كيف / how:** Beats: walk 0–4.1 s, notice/crouch 4.1–5.2, leap 5.2–6.9, land 6.9–7.35, walk 7.35–9.7, look back 9.7–12; end line from 10.4 s. MIDNIGHT vector short: CinematicCat.sceneSVG(t) per frame, 1280×720, 12 s, 24 fps (288 frames), title fades 2.2–3.2 s, window.render(t) contract. **أرقام / params:** 12 s · 24 fps · 6 beats.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/README.txt:12` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cinematic-cat.html:124`

#### STORY-65 · ستة أقواس لأنواع الستيكمان · Stickman six genre arcs · ✅ مُثبت هنا / proven here
- **ماذا / what:** مضحك، حب، مؤثر، مفاجأة حبكة، كوميديا سوداء، انقلاب الواقع — كل منها بخمس نبضات. — Funny, love, heart-touching, plot twist, dark comedy, surprise — five beats each.
- **متى أستخدمها / when:** ريلز ستيكمان — stickman reels (CHAR).
- **كيف / how:** genre 1–6 → arcs[genre−1]; beats map to setup/build/turn/peak/payoff (commute misunderstanding, shy small gesture, unseen kindness, bad luck helps, shortcut backfires, reality flips); clips 7 s; lock blocks enforced. Tested by production-profiles tests here. **أرقام / params:** 6 genres × 5 beats · 7 s clips.
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/stickman.mjs:9-17` · `fastify-motion-bro/tests/production-profiles.test.mjs`

#### STORY-66 · قوس الحب بخمس نبضات وإطارين · Five-beat love arc with paired frames · ✅ مُثبت هنا / proven here
- **ماذا / what:** لقاء، ثقة، بُعد، عودة، وعد حول طائر ورقي؛ لكل نبضة لقطة 35 مم واسعة ولقطة 85 مم عاطفية وسطر سرد. — Meeting, trust, distance, return, promise around a paper-crane motif; each beat a 35 mm wide + 85 mm close-up + one narration line.
- **متى أستخدمها / when:** قصص رومانسية أو عائلية مولدة — generated romance/family stories (GEN).
- **كيف / how:** `npm run profile -- start character-romance`; answer "<emotion/setting or DEFAULT>" → 5 scenes × 2 frames = 10 prompts, 9:16. Tested here. **أرقام / params:** 5 × 2 frames · 35 + 85 mm.
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/character-romance.mjs:10-29` · `fastify-motion-bro/skills/character-romance/SKILL.md:12`

#### STORY-67 · ملاءمة عدد المقاطع لخطوات الطبخ · Clip-count fitting (food flow) · ✅ مُثبت هنا / proven here
- **ماذا / what:** يوزع N مقطعًا على خطوات التحضير الحقيقية: يدمج الخطوات عندما المقاطع قليلة، ويضيف لقطات ماكرو (لمعان، بخار، دوران الطبق، تزيين) عندما كثيرة. — Maps N requested clips onto real preparation steps, merging or adding macro inserts; never repeats an action.
- **متى أستخدمها / when:** ريلز طبخ — food reels.
- **كيف / how:** pickStages(food, n): assembly = n−1; chunk or extend; the last clip is always the plated result; 1–200 clips; 10 s clips. Tested (production-profiles). **أرقام / params:** 1–200 clips · 10 s each.
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/food-flow.mjs:62-80` · `fastify-motion-bro/tests/production-profiles.test.mjs:48-55`

#### STORY-68 · مخرج الفيرال بخمس بوابات · Viral five-stage gated director · ✅ مُثبت هنا / proven here
- **ماذا / what:** 5 عناوين ← سكربت 5 أسطر ← 3 لوحات ← 5 أوامر ملصقات ← 5 أوامر حركة، وكل مرحلة تنتظر رد المستخدم. — 5 titles → 5-line script → 3 palettes → 5 poster prompts → 5 motion prompts, each waiting for the user.
- **متى أستخدمها / when:** ريلز تعليمية فيرال 9:16 — viral explainer reels.
- **كيف / how:** `npm run viral -- start | reply 1..5 | reply NEXT | status | compile | preview-project | approve-render`; session projects/viral-editorial/session.json; schema fmb.viral-editorial.v1; 1080×1920 30 fps; 5 ready topics (Attention Trap, Why Saving Money Feels So Hard, Stop Learning Technology the Wrong Way, Real Reason Some Ideas Spread, Motivation Myth). Tested (7/7). **أرقام / params:** 5 stages · 1080×1920 30 fps.
- **الدليل / proof:** `fastify-motion-bro/scripts/viral-editorial.mjs:35-46` · `fastify-motion-bro/tests/viral-editorial.test.mjs` · `fastify-motion-bro/skills/viral-editorial/SKILL.md:7-13`

#### STORY-69 · أفلام الدعاء والجمعة · Dua & Friday reels · 🟢 جاهز / ready
- **ماذا / what:** ريل جمعة بلقطات هادئة وسطر ديواني لكل لقطة، وفيلم دعاء الخميس بقلم ذهبي يرسم المحراب وسماء من الليل إلى الفجر. — A Friday reel with calm B-roll and one Diwani line per shot; a Thursday dua film where a gold pen draws a mihrab while the sky turns night to dawn.
- **متى أستخدمها / when:** محتوى ديني هادئ — calm religious content (ARAB, GLOW). No music under Quran recitation unless asked.
- **كيف / how:** Friday (mimic rebuild): 28.2 s, 1080×1920 30 fps, 11 shots, 10 fade-black transitions 0.70–0.80 s, text 135 px #fdfbf3 with 7 px #000 stroke. Thursday: 24.7 s, gold pen draws arch + eight-point rosette, mosque silhouette with lit windows, two swaying lanterns, petals and gold dust; AmiriB 84/104/130 px in #fff6e2/#ffd77a/#ffe39a, Aldhabi 170 px day name, sky #0b1033 → #34509a/#f2a079/#ffd890; key line on downbeat 10.987 s with the sun carrier. **أرقام / params:** 28.2 s / 24.7 s · fades 0.7–0.8 s.
- **الدليل / proof:** `kosif-one/projects/mimic-jumuah/study/mimic.json` · `kosif-one/projects/thursday-dua-animation/source/index.html` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/arabic-voice-kinetic/README.md`

#### STORY-70 · مونتاج الغربة بمعنى الأغنية · Meaning-matched song montage (Ghorba) · 🟢 جاهز / ready
- **ماذا / what:** مونتاج عمودي 48 ث عن الغربة: سبعة مقاطع بترتيب عاطفي تحت الأغنية الأصلية، تدرج باهت، وعنوان ASS لكل لقطة. — A 48 s vertical montage about living abroad: seven clips in emotional order under the untouched song, muted grade, per-shot ASS titles.
- **متى أستخدمها / when:** أغنية أو قصيدة يريد لها المستخدم مونتاجًا — songs/poems to montage (BEAT, FOOT).
- **كيف / how:** Exile order: departure (plane window 6.8 s) → goodbye (airport 5.2) → foreign streets (night drive 7.0) → memory (rain on glass 5.0) → loneliness (walking in rain 7.6) → family voices (6.8) → hope (sunrise from plane 9.6). 540×960 or 720×1280, 24 fps, contrast 1.06–1.08, saturation 0.86–0.95; concat demuxer, song muxed untouched. 18-step reuse runbook: inspect, transcribe with review, pitch 2–3 ideas, source footage (20–35 clean vertical shots for a full song), triage, beat/meaning shot list, Arabic motion type, export 9:16 and 16:9 on request. **أرقام / params:** 7 shots / 48 s · 24 fps · sat 0.86–0.95.
- **الدليل / proof:** `kosif-one/projects/KOSIF_Motion_Ghorba/KOSIF_Ghorba_Render.py:19-27` · `kosif-one/projects/KOSIF_Motion_Ghorba/MONTAGE_REUSE_RUNBOOK_AR.md`

#### STORY-71 · مستقبل مصر 2120: خطاف وقاعدة تراث · Egypt 2120: one-second concept + heritage rule · 🟢 جاهز / ready
- **ماذا / what:** افتح على المفهوم في ثانية بسؤال، وكل لقطة تضيف حقيقة برقاقة مرقمة، وختام بسطر وإخلاء «تصور فني تخيلي»؛ والأهرامات الحقيقية لا تُمس. — Open on the concept in a second, each shot adds one fact with a numbered chip, end with one line + disclaimer; real monuments stay untouched.
- **متى أستخدمها / when:** أفلام تخيلية عن أماكن حقيقية — speculative films about real places (3D, MAP).
- **كيف / how:** Hook 0–2.6 s («مصر ٢١٢٠» + «كيف سنعيش بعد مئة عام؟»), chips «٠١ · الجيزة» …, captions start 0.25 s after each cut and leave 0.3 s before the next, 18 s total. Heritage: Khufu, Khafre, Menkaure at 1:5 in their real diagonal (ConeGeometry(base/√2, h, 4) rotated 45°, stone #E3BC86) — futurism around them, never on them. **أرقام / params:** 18 s · captions +0.25 s / −0.3 s · scale 1:5.
- **الدليل / proof:** `kosif-one/projects/egypt-2120-animation/index.html:448-453` · `kosif-one/projects/egypt-2120-animation/index.html:218-221`

#### STORY-72 · شرح «تعريفان للنجاح» على لوحات مولدة · Two-definitions-of-success voice explainer · 🟢 جاهز / ready
- **ماذا / what:** شرح صوتي 47 ث: سؤال بعلامة استفهام ضخمة، قاعة ألف شخص، عالم المال البارد يبهت للرمادي عند «غير سعيد»، وعالم ذهبي دافئ. — A 47 s voice explainer on generated plates: giant outlined question mark, a hall of 1,000 people, a cold money world draining to grey, a warm golden world.
- **متى أستخدمها / when:** فلسفة أو تنمية ذاتية بصوت — reflective voice explainers.
- **كيف / how:** GSAP + Motion Kit composition with three text levels; base #05070b, gold #f5c97a, cold #7fd0ff, alarm #ff6b6b, cream #e9dcc4; synthesised 90 BPM D-minor score (vol .42) under the voice with designed SFX cues; 1080×1920 30 fps. **أرقام / params:** 47 s · 90 BPM · 3 text levels.
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/index.html`

#### STORY-73 · أشكال فيديو صانع المحتوى · Creator-video shapes & faceless VO · 📄 موصوف / documented only
- **ماذا / what:** الاختبار (نفس المهمة بطريقتين)، المهمة الحقيقية، اليوم، الشاشة الموجّهة — ومونتاج صوتي بلا وجه يُفحص بكاشف وجوه. — The Test, The Real Task, The Day, The Guided Screen — and faceless VO edits verified by a face detector.
- **متى أستخدمها / when:** مؤسس أو صانع محتوى يصوّر نفسه — founders/creators (FOOT).
- **كيف / how:** Choose the shape the footage can actually prove; never stage results; record each beat twice (precise + natural), lens near eye level, leave caption/UI space. Faceless: V1 screen recordings and face-free B-roll, voice A1, cards V2, captions V3; sample 1 fps frames through a face detector and replace flagged segments. Transcript-first assembly: inventory (file, camera, face flag, length, sentence count, gist) → beat sheet from what was actually said (voice clip = speech >50%) → approval → timeline. **أرقام / params:** 2 takes / beat · 1 fps face check.
- **الدليل / proof:** `kosif-atlas/skills/101-video-skills/214-creator-video/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2460-davinciresolve-story-devtalk/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2451-davinciresolve-beats-devtalk/SKILL.md`

#### STORY-74 · قواعد مونتاج المدينة · City montage shot grammar · 📄 موصوف / documented only
- **ماذا / what:** افتح على شارع/مرور/لافتات/ضوء، بدّل بين الواسع والمتوسط والتفاصيل، واربط اتجاه الحركة عبر القطعات على ضربات الإيقاع. — Open on establishing street/traffic/signage/light, alternate wide, mid and detail, chain motion direction across cuts on downbeats.
- **متى أستخدمها / when:** مونتاج سفر أو مدينة — travel/city montages (BEAT, TRANS).
- **كيف / how:** Shot list tagged wide/medium/detail with motion vectors (train passes, camera moves, water); cut to downbeats from a beat map. Travel-note captions: place, time and mood ("9 AM, market alley"), commas only, chapter title bottom-left 0.5 s after scene start for 3 s, ≤2 lines, ≈18 chars/line, bottom margin 8%. **أرقام / params:** captions ≤2 lines · 18 chars · margin 8%.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2433-akbun-davinciresolve-cut-new-york/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2465-davinciresolve-subtitle-travelnote/SKILL.md`

#### STORY-75 · معرض قوالب الأفلام (52) وقوالب البداية · Film template gallery (52) & starter briefs · 📦 بأمر تثبيت / one install
- **ماذا / what:** 52 بريفًا أصليًا في 7 أنواع عربية بخانات للموضوع والسطر والرقم — والملء لا يخترع أرقامًا؛ وثلاثة قوالب بداية في Workbench. — 52 original brief templates in 7 Arabic genres with slots for subject, line and figure; three Workbench starter briefs.
- **متى أستخدمها / when:** المستخدم لا يعرف من أين يبدأ — users without a brief.
- **كيف / how:** Basma TPL: showreels (reel-designer 15 s, reel-type 12, logo-sting 5 …), launch (app-launch 15, saas-promo 15, pricing 12, milestone 8, dashboard-reveal 12 …), explainers and more; per-style script contracts (plotter 4–7 lines of 2–5 words; doodle 4–8 sentences with «dialogue»; whiteboard 4–6 steps; stickman 4–7 lines with a twist; infographic 3–6 lines with one real figure each). Workbench GET /api/templates: kinetic «حروف وحركة» #a7e8d0, cinematic «لقطة سينمائية» #d3c0fa, montage «مونتاج بإيقاع» #f5ce91. **أرقام / params:** 52 templates · 7 genres.
- **تثبيت / install:** `cd app && npm install`
- **الدليل / proof:** `app/public/js/00_editor.js:1777` · `app/public/js/10_studio.js:913` · `100-superskills/skills/kosif-montage-motion/scripts/web/wbcompat.py:24`

#### STORY-76 · لوحات المشهد المرسوم وموجّه الرسم · Painted-scene showcases & drawing request router · 🟢 جاهز / ready
- **ماذا / what:** برامج لوحات خيالية (فتاة وتنين، حوت وتنين في عاصفة، بطة تهاجم تنينًا) وموجّه يحدد أي كود لأي طلب رسم. — Fantasy painting programs and a router mapping each drawing ask to a pipeline.
- **متى أستخدمها / when:** طلب رسم/لوحة سينمائية أو «ارسم الصورة دي» — painting requests (TEX, LIGHT).
- **كيف / how:** Router: "draw this image as is / give me its code" → to_python; cinematic painting from a prompt → KOSIF scene + judge; realistic 3D/reflections → Three.js page; film of the drawing → painter film. Recipe: value before colour (range >150/255), three lights (cool key, warm key, dim ambient) each with rim, aerial depth (screen fill blur 30 at 0.2), then grade/vignette/grain; brief as must-show elements + light sources + prohibitions, built back to front. whale_dragon passes its judge test (letterbox 62/738); dragon_girl sky #05071a → #8c3a2e, 280 stars. **أرقام / params:** value range >150 · 3 lights + rims.
- **الدليل / proof:** `kosif-studio/references/drawing-guide.md:6` · `kosif-studio/scenes/whale_dragon.py:1` · `kosif-studio/scenes/dragon_girl.py:129`

#### STORY-77 · كتاب العالم والكائنات الأصلية · Creature & world-bible kit · 📄 موصوف / documented only
- **ماذا / what:** قوالب لكائنات وعوالم أصلية: بطاقة كائن (الندرة، البيئة، الصورة الظلية، الحركة المميزة، التطور، نقطة الضعف) وكتاب عالم. — Templates for original creatures and world bibles — no trademarked characters.
- **متى أستخدمها / when:** ألعاب، سلاسل خيالية، شخصيات علامة — games, fantasy series, mascots (CHAR).
- **كيف / how:** 19 element types; rarity Common 60 / Uncommon 25 / Rare 10 / Epic 4 / Legendary 0.9 / Mythical 0.1 %; 8 biomes; creature card: name, type, rarity, biome, silhouette + 3 features, palette, signature move + VFX, evolution trigger, weakness, lore hook, 7-layer prompt + CHR code; world bible: premise, map zones, factions, magic/tech limits, economy, conflicts, 5 LOC + 5 CHR. Anime shot grammar (observed): intro each unit → launch → transform → close-ups → pose. **أرقام / params:** rarity 60/25/10/4/0.9/0.1 % · 8 biomes.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-cinema-director/references/creative-worlds.md` · `style:pm-allforbigfire-86ff3c`

## الأفكار والتغليف والتخطيط — Ideation, packaging & planning

_أفكار من محفزات حقيقية، عناوين بتوتر صادق، وتقويم نشر يصنع سلسلة._

#### STORY-78 · توليد أفكار بعشوائية حقيقية · Lateral ideation with real randomness · 🟢 جاهز / ready
- **ماذا / what:** كلمات محفزة عشوائية فعلًا وأوامر استفزاز لتفلت من الأفكار المتوقعة؛ أو 100 فكرة عبر 10 اتجاهات ثم تصفية. — Genuinely random stimulus words and provocation prompts; or 100 ideas across 10 directions, then filter.
- **متى أستخدمها / when:** عندما تكون الأفكار الأولى مكررة — when first ideas are generic.
- **كيف / how:** kosif_ideate {problem, concepts[], n ≤30, seed} → definition checklist, n stimuli with contiguity/similarity/contrast prompts, concept challenges, provocation operators, stage-2 filter (reproducible seed). 100-ideas skill: reverse, combine, constrain, exaggerate, swap audience… Idea tiering: 15–20 raw ideas via gap analysis, trend riding, format innovation, audience questions; 60–70% growth tier; each with working title, angle, timeliness. Discovery intent per idea: search (front-load the answer, real query phrasing) vs browse (opening + thumbnail pattern-break) — no discovery logic, no idea yet. **أرقام / params:** n ≤30 · 15–20 ideas · 60–70% tier 1.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-think-pro/scripts/ideate.py` · `100-superskills/skills/ideation-100-ideas/SKILL.md` · `kosif-atlas/skills/1817-youtube-strategy/4866-yt-ideation/SKILL.md` · `kosif-atlas/skills/1520-digital-marketing-pro/4132-video-packaging/SKILL.md`

#### STORY-79 · استخراج القصص والنُّقَط من النص · Story-mine & transcript nuggets · 📄 موصوف / documented only
- **ماذا / what:** القصة المعاشة تخفي: الدرس، الرأي المخالف، الإطار، الدليل، اللحظة القريبة؛ والتفريغ يعطي 15–25 نقطة بثلاثة مرشحات. — A lived story hides lesson, contrarian take, framework, proof and relatable moment; a transcript yields 15–25 nuggets via three filters.
- **متى أستخدمها / when:** بودكاست، محاضرة، قصة شخصية — podcasts, talks, personal stories (SYNC).
- **كيف / how:** Filters: what surprised, what challenged an assumption, what you would repeat over coffee; provisional headline + signal per nugget; pick 2–4 for clips and animated quote cards. Lead drafts with the surprise, number or reversal — never chronology ("بدأ الأمر عندما…"); never improve facts; anonymise client details by default. **أرقام / params:** 15–25 nuggets · pick 2–4 · 5 angle types.
- **الدليل / proof:** `kosif-atlas/skills/1181-transcript-to-content-pipeline/2789-transcript-to-content-pipeline/instructions.md` · `kosif-atlas/skills/1520-digital-marketing-pro/4122-story-mine/SKILL.md`

#### STORY-80 · العناوين: التوتر الصادق وخمسة اختبارات · Titles: honest charge & five tests · 📄 موصوف / documented only
- **ماذا / what:** العنوان القوي يعبّر عن توتر حقيقي (متوقع مقابل فعلي، وعد مقابل كلفة)، ويمر بخمسة اختبارات: يكمل «أريد ___»، وضوح فوري، طاقة إيجابية، لغة الجمهور، يُعاد شفهيًا. — Strong titles express a true tension and pass five tests.
- **متى أستخدمها / when:** عنوان فيديو أو عنوان على الشاشة — titles and on-screen headlines.
- **كيف / how:** State 2–4 charges plainly, generate 10–20 raw candidates, keep 3–5 with the supporting fact; cut words until cutting removes truth. Strategy families: direct benefit, honest curiosity gap, authority, trending/urgency; 5–10 titles <60 chars labelled by strategy. Weak priors only: numbers, concreteness and individual stories lift clicks; ≈2.3% CTR per negative word is not a licence for fear. Arabic copy: PAS / AIDA / 4U, 10 headlines → pick 3, one CTA, consistent dialect, Arabic punctuation. **أرقام / params:** 10–20 raw → 3–5 · <60 chars.
- **الدليل / proof:** `kosif-atlas/skills/2218-majestic-writing/8393-headline-generator/SKILL.md` · `kosif-atlas/skills/3067-youtube/13227-creator-seo-agent/SKILL.md` · `kosif-atlas/skills/1817-youtube-strategy/4868-yt-packaging/SKILL.md` · `100-superskills/skills/arabic-copywriting/SKILL.md`

#### STORY-81 · خريطة الدعوة للفعل · CTA placement map · 📄 موصوف / documented only
- **ماذا / what:** القصير: دعوة واحدة عند الذروة الطبيعية؛ الطويل: دعوة ناعمة في المنتصف وقوية في آخر 60 ث، عبر الكلام والشاشة وبطاقة النهاية والتعليق المثبت. — Short: one CTA at the climax; long: soft mid-roll + strong end within the last 60 s.
- **متى أستخدمها / when:** تحديد مكان الدعوة — placing the call to action (FMT end card).
- **كيف / how:** Mark CTA cues on the timeline with rationale; the end card is a reusable component held long enough to read; one offer, one audience, one action. **أرقام / params:** short 1 CTA · long mid + end ≤60 s.
- **الدليل / proof:** `kosif-atlas/skills/1520-digital-marketing-pro/4133-video-script/SKILL.md` · `kosif-one/vendor/ai-design-skills/skills/landing-page-design/SKILL.md`

#### STORY-82 · الغلاف يبدأ من النفس لا من الصورة · Psychology-first thumbnail brainstorm · 📄 موصوف / documented only
- **ماذا / what:** ابدأ بما يجب أن يتساءل عنه المشاهد ويشعر به: 2–3 أسئلة، 1–2 عاطفة، مشكلة في عبارة واحدة كبطل، ثم 2–3 اتجاهات. — Start from what the viewer should wonder and feel: 2–3 questions, 1–2 emotions, the problem as hero, then 2–3 directions.
- **متى أستخدمها / when:** قبل تصميم الغلاف — before designing a thumbnail (FMT thumbnails).
- **كيف / how:** Emotions: curiosity, unease, trust, vulnerability, surprise; turn each direction into an HTML/CSS layout and render variants with Playwright at 1280×720. **أرقام / params:** 2–3 questions · 1–2 emotions · 1280×720.
- **الدليل / proof:** `kosif-atlas/skills/1101-akbun-writing/2486-akbun-thumbnail-review/SKILL.md`

#### STORY-83 · أعمدة المحتوى والتقويم · Content pillars & publishing calendar · ✅ مُثبت هنا / proven here
- **ماذا / what:** خليط أعمدة (رؤى 30%، كواليس 25%، تعليم 25%، شخصي 15%، ترويج 5%) يوزَّع بالأوزان على المنصات والأيام إلى تقويم يُستورد كتذكيرات. — A pillar mix spread by weight across platforms and allowed days into an importable calendar.
- **متى أستخدمها / when:** سلسلة محتوى أو خطة شهر — series and monthly plans.
- **كيف / how:** `python3 social.py calendar plan.json --out DIR` → calendar.csv/.xlsx/.md/.ics (ran here on the example plan). Promotion above ~20% reduces reach; 3–5 pillars each tied to a metric; plan one motion template series per pillar so cost per post drops. **أرقام / params:** 30/25/25/15/5 % · CSV/XLSX/MD/ICS.
- **الدليل / proof:** `100-superskills/skills/kosif-social/scripts/social.py:471` · `kosif-one/tools/kosif-social/examples/plan.json` · `kosif-atlas/skills/192-marketing-skills/611-social-content/SKILL.md`

#### STORY-84 · موجة الموشن 2026: أنماط الطلب والميزانيات · Motion-wave prompt patterns & effort budgets · 📄 موصوف / documented only
- **ماذا / what:** خمسة أنماط طلب نجحت: ريل بسطر واحد، أشِر إلى رابط علامة، سمِّ لوكًا ومرجعًا، مواصفة XML، بريف مخرج طويل ببوابات — مع توقعات واقعية للوقت والكلفة. — Five prompt patterns that worked, with realistic time/cost expectations.
- **متى أستخدمها / when:** تحديد التوقعات وقوالب الاستقبال — setting expectations.
- **كيف / how:** Corpus 3,984 posts / 203M views: 3D 487 posts 52.0M, seek(t) 70 / 34.9M, UI 217 / 16.3M, Arabic only 11 / 0.13M — Arabic motion done right is open ground. Patterns: one-liner showreel (~15 s); brand URL with real assets + music; name a look + reference (frame every 0.5 s → style_guide.md); XML spec (<inputs> <direction> <structure> at 120 BPM <build> <gotchas> <start>); long brief 9.5k–19k chars with a payoff every 3–5 s and gates plan → stills → animatic → pass → polish → audio → render. Budgets: median 20 min (p90 57) for a short clip from one prompt; median 4 h for celebrated pieces; median $10 in tokens (p90 $200). **أرقام / params:** 3,984 posts · 20 min / 4 h medians.
- **الدليل / proof:** `kosif-studio/motion/references/x-trend-2026.md` · `100-superskills/skills/kosif-montage-motion/references/x-trend-2026.md`

#### STORY-85 · وكلاء الإبداع الفرعيون وقرارات Jev · Creative sub-agents & Jev decisions · 🔑 مفتاح أو خدمة / needs key or paid service
- **ماذا / what:** شخصيات وكلاء جاهزة (مخرج سينمائي، منتج فيديو بفحص إطار بإطار، مصمم إضاءة، مهندس صوت، ناقد بصري، راوي) ومحرك قرار يعطي احتمالًا لكل خيار. — Ready sub-agent personas and a decision engine that gives each option a probability.
- **متى أستخدمها / when:** مشاريع كبيرة تحتاج أدوارًا — large multi-role jobs.
- **كيف / how:** Launch via the Agent tool as kosif-omni:<agent>; each delegates to inner roles (prompt engineer, camera-move expert, rhythm expert, frame consistency, edit director, Arabic captions engineer). Jev (owner service) scored design choices, e.g. IBM Plex Sans Arabic p=0.99, ram emblem 0.97; combine-route thresholds 0.6/0.4. Owner-built planning skills (curriculum, research with citations, red-team pre-mortem, market research, decks) support the video job as instruction-only playbooks. **أرقام / params:** p_yes 0.6 / 0.4.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/agents/kosif-video-producer.md` · `kosif-one/tools/kosif-omni/agents/kosif-cinema-director.md` · `kosif-earth-ci-fork/docs/design/KOSIF-LUXE.md` · `100-superskills/skills/red-team-premortem/SKILL.md`

## توليفات قوية / power combos

- **ريل من مقطع كلام / talking clip → reel:** STORY-01 + STORY-59 + STORY-48 + ARAB-62 + FMT (ملف لكل منصة) — رسالة واحدة، ثم مونتاج مُخرَج بكلمة مفتاحية لكل جملة، وذروة تُكتشف وتُمسك 2.2 ث.
- **إطلاق منتج / product launch:** STORY-02 + STORY-61 + STORY-26 + STORY-19 + UI + FMT (ختام المتجر) — أول إطار هو المنتج يعمل، 18–22 ث، ونص مشاركة ≤280 حرفًا.
- **فيلم من أغنية أو قصيدة / song or poem film:** STORY-70 + STORY-48 + STORY-49 + BEAT + ARAB-66 — ترتيب عاطفي للقطات، ورمز لكل معنى، والذروة على آخر عودة للازمة.
- **شرح بيانات / data explainer:** STORY-32 + STORY-09 + STORY-50 + DATA + ARAB-77 — عنوان استبصار برقم، طبقة لكل نبضة، وفصول مرقمة.
- **ريل عرض الاستوديو / studio showreel:** STORY-62 + STORY-47 + STORY-36 + BEAT + TRANS — نقطة حمراء تعبر كل لقطة على شبكة 120 BPM.
- **إعلان 15 ث / 15 s ad:** STORY-16 + STORY-17 (3 خطافات) + STORY-25 + FMT ad-slot + EASE — الرسالة قبل 5 ث، وثلاث افتتاحيات لاختبار A/B.
- **قصة بشخصيات مولدة / generated character story:** STORY-21 + STORY-13 + STORY-14 + STORY-66 + GEN — قصة تمر بفحص الصراع، أوامر مقفلة الاستمرارية، ولقطتان لكل نبضة.
- **دعاء ليلي / night dua:** STORY-69 + STORY-47 (الشمس) + ARAB-28 + GLOW + VOICE (بلا موسيقى) — الشمس تصعد وترتطم بالوردة على السطر المفتاحي.
- **«اعمل زي ده» / match a reference:** STORY-45 + STORY-05 + STORY-44 + QA — قواعد المرجع لا محتواه، ثم ورقة لقطات قبل/بعد.

## أخطاء ممنوعة / never do

1. **لا تستجوب المستخدم في جولات متعددة** — رسالة واحدة بالأسئلة الناقصة مع افتراضات؛ ولا تسأل عما أعطاه (STORY-01).
2. **لا تبدأ بالشعار ولا بإطار ساكن** — الإطار الأول يتحرك ويُظهر الموضوع؛ الشعار في النهاية (STORY-16).
3. **لا «سلايد شو» يسمى موشن** — صور بتلاشٍ ليست موشن جرافيك؛ كل لقطة دالة في الزمن وتتحقق بفروق الإطارات (STORY-42).
4. **لا مظهر «مولّد»** — عنوان في المنتصف على تدرج، توهج بنفسجي، جسيمات ووميض بلا فكرة، ثلاث بطاقات متساوية (STORY-37).
5. **لا تخلط أكثر من اتجاهين ولا نظامين جماليين** — زجاج على شبكة سويسرية يلغي كل منهما الآخر (STORY-05, STORY-41).
6. **لا أرقام أو حقائق مخترعة** — العنوان هو الرقم الذي قيل أو أطول كلمة، والبيانات التخيلية تُوسم (STORY-46).
7. **لا نبضة بلا معلومة جديدة** — احذفها أو بسّطها؛ الدراما وحدها لا تكفي (STORY-11, STORY-32).
8. **لا تنسخ المرجع** — لا سكربت ولا شعار ولا شخصيات ولا لقطات؛ ولا تدّعي أنك شاهدت فيديو لم تفتحه (STORY-45).
9. **لا قصة بلا قرار من البطل ولا وسط يُحل بسهولة** — story_lint يحذّر؛ فضّل yes-but وno-and (STORY-21).
10. **لا جرأة مبعثرة** — لحظة توقيع واحدة، والباقي هادئ (STORY-36).
11. **لا موسيقى تحت تلاوة القرآن ولا عبث بالمعالم الحقيقية** — الدعاء بلا مرافقة إلا بطلب، والأهرامات تبقى بنسبها (STORY-69, STORY-71).
12. **لا وعود زمنية غير واقعية** — قطعة مشهورة تأخذ ساعات؛ قل التقدير بصدق (STORY-84).

## أقوى 5 حركات توقيع / 5 signature moves

1. **STORY-02 + STORY-03 — من جملة عربية إلى خطة إطارات:** موجّه 16 مسارًا ثم خمس نبضات بإطارات دقيقة؛ مُجرَّب هنا.
2. **STORY-59 — مونتاج مُخرَج لمقطع كلام:** كلمة مفتاحية لكل جملة، أرقام كحلقات، كلمة القطع كانتقال، وذروة ممسوكة.
3. **STORY-47 — الشيء المحمول:** نقطة أو شمس أو كرة تعبر كل لقطة وتنتهي في الشعار — أسرع طريق لفيلم «مُخرَج».
4. **STORY-17 — ثلاثة خطافات لنفس الجسم:** افتتاحيات بديلة بأنماط مختلفة لاختبار A/B دون إعادة المونتاج.
5. **STORY-21 — فحص الصراع:** هدف ودافع وصراع ورهان لكل نبضة، وقرار من البطل، ودرجة من 100 قبل أي رندر.

## إضافات من Cinematic Director PRO v5

_مستخلصة من حزمة المالك KOSIF Claude Cinematic Director PRO v5 (انظر [cinematic-director-pro.md](../cinematic-director-pro.md)). مسارات الدليل `owner-upload:` تشير إلى ملفات داخل أرشيف المالك، لا إلى هذا المستودع._

#### STORY-P01 · عشرون وصفة أسلوب موشن بمحركاتها · 20 motion style recipes (S01–S20) with engine candidates · 📄 موصوف / documented only
- **ماذا / what:** قائمة أصلية بعشرين أسلوبًا، لكل واحد هدف بصري ومحركات مرشحة ومعاينة مفهومية مربوطة؛ للاختيار السريع لا كإثبات تنفيذ. / An original list of 20 styles, each with a visual goal, candidate engines and a linked concept preview — for quick choice, not proof of execution.
- **كيف / how:** S01 particles (Pixi/Three/Canvas, A24) · S02 liquid-morph (Flubber/GLSL/SVG, A13) · S03 holographic (Three/OGL/Blender, A36) · S04 neon-glow (SVG/Canvas/FFmpeg, A03) · S05 wireframe-3d exploded parts (Three/Blender, A31) · S06 glassmorphism (CSS/Three, A34) · S07 kinetic-type word by word, Arabic shaped (Remotion/SVG/HarfBuzz, A08) · S08 isometric process (SVG/Three, A32) · S09 clay-3d (Blender/Three, A35) · S10 ascii terminal (Canvas/SVG, A10) · S11 gradient-mesh (GLSL/OGL, A28) · S12 comic-book panels with camera moves (SVG/Remotion, A41) · S13 split-flap stats (Canvas/Remotion, A19) · S14 retro-vhs (FFmpeg/GLSL, A49) · S15 halftone (Canvas/GLSL, A25) · S16 bauhaus primitives (D3/SVG/Motion Canvas, A17) · S17 pixel-art grid (Canvas/Pixi, A51) · S18 blueprint (SVG/Manim/Blender, A02) · S19 art-deco metallic ornament (SVG/Canvas, A23) · S20 neo-brutalism blocks (HTML/CSS/Remotion, A09). Every linked preview is flagged example_is_exact_style=false. Source: distilled from the owner-supplied Google Doc (Tyler Mommsen, motion-graphics prompts). For build numbers open the matching existing powers (e.g. TYPE-35 split-flap, SHAPE-73 bauhaus, RETRO-33 ascii, 3D-106 isometric). **أرقام / params:** 20 presets · fields id, slug, name_ar, visual_goal, engine_candidates, example_reference_id
- **الرخصة / license:** owner package (own work)
- **الدليل / proof:** `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/references/STYLE_PRESETS_20.json` · `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/integrations/kosif-see/style_gallery.html` · `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/references/GOOGLE_DOC_DISTILLATION.md`

#### STORY-P02 · الإحاطة السينمائية بثماني خانات · Eight-slot cinematic brief (PRODUCT → … → OUTPUT) · 📄 موصوف / documented only
- **ماذا / what:** قبل أي كود اكتب الإحاطة في ثماني خانات ثابتة حتى لا يبقى قرار بصري أو صوتي مفتوحًا. / Before any code, fill eight fixed slots so no visual or sound decision stays open.
- **كيف / how:** PRODUCT/TOPIC → STORY → FORMAT (aspect, duration, fps) → LOOK (hex colours, fonts, camera angle) → MOTION (easing family, transitions, the one continuous thread object — see STORY-175) → SOUND (who is the master clock: the voice if there is speech; real beat map, never an assumed 120 BPM) → QUALITY (acceptance list) → OUTPUT (files, codecs, editable source). Then choose the engine: UI/logo/type in React → Remotion; DOM-seekable → HyperFrames; diagrams/maths → Motion Canvas or Manim; real 3D camera → Three.js/Blender after a GPU check; existing footage → FFmpeg + ffprobe + scene detect/ASR; photoreal generated shots → an external generator that is actually available. **أرقام / params:** 8 slots · hex colours required · voice = master clock
- **الرخصة / license:** owner package (own work)
- **الدليل / proof:** `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/references/GOOGLE_DOC_DISTILLATION.md`

#### STORY-P03 · قاموس تحويل وصف الهواة إلى أوامر حركة · Amateur → pro motion lexicon (adjective → code direction) · 📄 موصوف / documented only
- **ماذا / what:** يحوّل كلمات مثل «ناعم» و«متتابع» و«مع الإيقاع» إلى تعليمات قابلة للبرمجة، مع متى لا تُستخدم. / Turns words like "smooth", "staggered" or "on the beat" into programmable instructions, with when not to use them.
- **كيف / how:** smooth → closed-form damped spring or cubic-bezier(0.16,1,0.3,1), bounded overshoot (not everything needs a spring) · staggered → overlapping timeline with measured offsets synced to voice/beat, not a hard-coded 125 ms · alive hold → bounded micro-motion that never hurts reading · on the beat → detected onsets from the real audio · motion blur → sub-frame sampling (tmix over whole adjacent frames is not shutter blur) · Arabic writing → word/run spring + clip-path, never split("") · glyph scramble → seeded, Latin or unjoined glyphs only · line draw → getTotalLength + dashoffset + tip at getPointAtLength · elastic transition → shared geometry into the next scene (a cut is sometimes better) · mask wipe → clipPath/canvas compositing · gooey → feGaussianBlur + feColorMatrix · liquid glass → background distortion + rim light only if GPU justifies it · camera move → deterministic matrix, text inside safe zones · UI demo → rebuilt layered components, not a zoomed screenshot · seamless loop → every animated state incl. velocities periodic at the seam · deterministic seek → frame = f(t, seed, assets), verified by shuffled frame order · voice to motion → forced alignment → events → meaning → keys, ±100 ms only once measured · 3D trailer → camera spline, light rig, verified hardware. **أرقام / params:** 18 mappings
- **الرخصة / license:** owner package (own work)
- **الدليل / proof:** `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/references/MOTION_TECHNIQUE_LEXICON.md`

## إضافات v2 — v2 additions

_قدرات أُضيفت في الإصدار الثاني من حزم المالك (higgsfield-motion-saas وhiggsfield-motion-claude ومهارة المونتاج التحريرية وفيلم الأغنية وKOSIF SEE) ومن مهارات ECC (رخصة MIT)، مكتوبة بكلماتنا. ✅ هنا = شُغّلت في جلسة 2026-10-16 وسجلها في [external-skills.md](../external-skills.md)؛ مسارات `owner-upload:` تشير إلى أرشيفات المالك لا إلى هذا المستودع. — v2 additions from the owner's packages and ECC skills (MIT), in our own words; ✅ = run in this session, log in external-skills.md; `owner-upload:` paths point into the owner's archives, not this repo._

#### STORY-X01 · السيناريو أولًا وخريطة المحفزات · Scenario first: beat-grid shot table and trigger map · 📄 موصوف / documented only
- **ماذا / what:** قبل البناء: جدول لقطات على شبكة الإيقاع وخريطة محفزات (زمن · سبب · نتيجة · كاميرا) وسؤالان على الأكثر، ثم معايرة نحو خمسة إطارات مفتاحية قبل التوسع. — Before building: a shot table on the beat grid, a trigger map (time · cause · effect · camera), at most two questions, then calibrate about five key frames before fanning out.
- **متى أستخدمها / when:** بداية أي فيلم حركة أو إعلان — the start of any motion film or ad.
- **كيف / how:** Show something visible within 10–15 minutes; the trigger map makes every transition motivated (TRANS-X01); key frames are approved before scenes are built in parallel; status answers give clock time, what changed, the stage, an image and a clock-time ETA, and offer to stop. 'Stop' halts everything, including credit spend. **أرقام / params:** first visible result ≤ 10–15 min; ≤ 2 questions; ~5 calibration frames.
- **الرخصة / license:** owner (no LICENSE file)
- **المصدر / source:** `owner-upload:motion-skill-claude/higgsfield-motion-claude/references/production-lessons.md`
- **الدليل / proof:** `owner-upload:motion-skill-claude/higgsfield-motion-claude/references/production-lessons.md` · `owner-upload:motion-skill-claude/higgsfield-motion-claude/SKILL.md`

#### STORY-X02 · ذوق العميل: من الرفض إلى قاعدة · Client taste: from rejection to rule · 📄 موصوف / documented only
- **ماذا / what:** كل رفض من العميل يتحول إلى قاعدة مكتوبة تُطبق في الأفلام التالية. — Every client rejection becomes a written rule applied to later films.
- **متى أستخدمها / when:** مشروع مع عميل يتكرر أو مراجعات متعددة — repeat clients or multi-round reviews.
- **كيف / how:** Rules that transferred: flat clean vector reads cheap → add a photographed pass (GLOW-X01) and tint bloom cores; write 'differences from the references' on the storyboard (palette, shape, type, story); an era palette may be borrowed, a brand identity never; one world per film with 6–12 small true details near the hero; the single accent colour and the frame centre are reserved for the story event; 'as in the reference' = sample that range every 0.08 s and copy the motion grammar beat by beat in your own palette and type; 'code-based' means no 3D app at all, so state the toolchain in the first reply; characters idle at about 2× the amplitude that looks right in a still. **أرقام / params:** ref sampling every 0.08 s; 6–12 true details.
- **الرخصة / license:** owner (no LICENSE file)
- **المصدر / source:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/client-taste.md`
- **الدليل / proof:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/client-taste.md` · `owner-upload:motion-skill-claude/higgsfield-motion-claude/references/client-taste.md`

#### STORY-X03 · انضباط التكرار والنسخ · Iteration and version discipline · 📄 موصوف / documented only
- **ماذا / what:** رقّم النسخ ولا تكتب فوقها، وغيّر فقط ما سُمّي، وإذا قيل «النسخة السابقة أفضل» انسخ كودها وأرقامها حرفيًا. — Number versions and never overwrite; change only named items; if told 'vN was better', copy vN's code and numbers verbatim.
- **متى أستخدمها / when:** كل جولة تعديل — every revision round.
- **كيف / how:** Back up the approved version; a new reference mid-project → merge its beats into the approved cut with a beat → reference table; patch-render only the changed ranges; never ship silent and never ship without frame-level QA (QA-X01 plus stills every 2 frames ±0.5 s around each cut); fix diagnosed defects before new ideas.
- **الرخصة / license:** owner (no LICENSE file)
- **المصدر / source:** `owner-upload:motion-skill-claude/higgsfield-motion-claude/references/production-lessons.md`
- **الدليل / proof:** `owner-upload:motion-skill-claude/higgsfield-motion-claude/references/production-lessons.md` · `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/client-taste.md`

#### STORY-X04 · تقديرات وقت واقعية · Realistic time estimates · 📄 موصوف / documented only
- **ماذا / what:** قدّر وقت العمل من أرقام فعلية لا من حدس؛ التقديرات السابقة كانت أعلى من الواقع بثلاث إلى أربع مرات. — Estimate from measured actuals, not intuition; past estimates were 3–4× too high.
- **متى أستخدمها / when:** حين يسأل المستخدم «كم سيستغرق؟» أو عند التخطيط — when the user asks how long, or when planning.
- **كيف / how:** Storyboard 15–25 min; film 25–45 min after the go for 4–7 scene files; revision 15–40 min; an agent round 30–60 min. Actuals on four owner films: 39 min (estimated 1.5–2 h), 63 min, 1 h 53 min (two rounds), 4 h 50 min (four versions). Masters with 8 sub-frames and a 0.5 shutter take about 20 s of render per film second. **أرقام / params:** storyboard 15–25 min; film 25–45 min; revision 15–40 min.
- **الرخصة / license:** owner (no LICENSE file)
- **المصدر / source:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/launch-film.md`
- **الدليل / proof:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/client-taste.md` · `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/launch-film.md` · `owner-upload:motion-skill-claude/higgsfield-motion-claude/references/production-lessons.md`

#### STORY-X05 · استعارات بصرية من فيلم الأغنية · Visual metaphors from the owner's song film · 📄 موصوف / documented only
- **ماذا / what:** أدوات سرد مرسومة بالكود: وجهان متقابلان بينهما ضوء، ونجوم ترسم وجهًا، وبورتريه مصنوع من كلمات الأغنية، وسماء تمر عليها ساعات اليوم. — Code-drawn story devices: two facing profiles with light between them, stars that draw a face, a portrait made of the lyric's words, and a time-lapse sky.
- **متى أستخدمها / when:** فيلم أغنية رومانسية أو قصة بلا لقطات حقيقية — a love-song film or a story without real footage.
- **كيف / how:** Rubin-vase profiles: his profile fills bottom → top with her words (portrait made of text). Constellation profile: chosen profile points become stars that draw her face before they meet and complete in the finale. Time-lapse sky colour keys with sun and moon, a blossoming tree, a moon ring pulsing with the audio, meteors on the climactic word. The README traces which catalog styles inspired each idea: keep that catalog → film traceability. The whole 56.92 s 9:16 film is one deterministic canvas file with seek(t) plus three small Python tools; the song stays untouched.
- **الرخصة / license:** owner (song audio and lyrics are third-party; not included)
- **المصدر / source:** `owner-upload:film_project/film/README_AR.md`
- **الدليل / proof:** `owner-upload:film_project/film/README_AR.md` · `owner-upload:film_project/film/film.js`

#### STORY-X06 · اعرض ثلاث معاينات بدل الأسئلة · Show three previews instead of a questionnaire · 📄 موصوف / documented only
- **ماذا / what:** لاكتشاف الذوق ابنِ ثلاثة إطارات معاينة مختلفة فعلًا ودع المستخدم يختار، بدل قائمة أسئلة. — To discover taste, build three genuinely different single-frame previews and let the user pick, instead of a questionnaire.
- **متى أستخدمها / when:** بداية مشروع والمستخدم لا يعرف ما يريد — the start of a project when the user cannot describe the look.
- **كيف / how:** Each preview is small (under ~100 lines) and shows one direction: palette, type and motion feel. Then build the chosen one with tokens. Works for decks, title cards and film looks alike. **أرقام / params:** 3 previews; < ~100 lines each.
- **الرخصة / license:** MIT (ECC, (c) 2026 Affaan Mustafa)
- **المصدر / source:** `https://github.com/affaan-m/ECC/tree/main/skills/frontend-slides/SKILL.md`
- **الدليل / proof:** `https://github.com/affaan-m/ECC/tree/main/skills/frontend-slides/SKILL.md`

## إضافات مرفقات 2026-10-23 — 2026-10-23 upload additions

_من مراجعة مرفقات المالك: [owner-uploads-review-20261023.md](../owner-uploads-review-20261023.md). — From the owner-upload review._


#### STORY-U01 · خط فيلم الأغنية الكرتوني · Cartoon music-video pipeline · 📄 موصوف / documented
- **ماذا / what:** أغنية ~40 ث (مقطع بين شخصيتين ولازمة واحدة معًا، سطور حرفية بسيطة) ← صفحة شخصيات وبيئات 2×2 ومؤثرات 5×2 مولّدة ← تُعاد رسمها بالكود ولا تُلصق ← رندر بقطع متداخلة قابلة للاستئناف ← لقطات ثابتة بأفواه مغلقة لمزامنة الشفاه. — Song → sheets → repaint in code → resumable render → lip-sync plates.
- **متى أستخدمها / when:** فيديو أغنية كرتوني من الصفر / a cartoon music video from nothing
- **كيف / how:** لكل قسم من الأغنية بيئة؛ كلمات بأسلوب «كود» متوهج؛ كاميرا مدارية. **أرقام / params:** ~40 s; env sheet 2×2; props 5×2
- **الرخصة / license:** Claude AI Motion Graphics (Tao Prompts) — ideas and numbers only, code not copied
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/references/owner-uploads-review-20261023.md`
