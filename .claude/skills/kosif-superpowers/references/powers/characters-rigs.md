# الشخصيات والتحريك الهيكلي — Characters & rigs

> **قوتك هنا:** أنت تصمم شخصية أصلية وتثبّت هويتها، وتبني لها هيكلًا بمفاصل (SVG أو Canvas أو three.js)، وتمشّيها بدورة إجرائية لا تنزلق قدماها، وتجعلها تقفز وتنضغط وتتنفس وترمش وتتكلم — وتجعلها «حيّة» حتى وهي ساكنة.
> **أقوى دليل:** صوّرتُ هنا إطارات من مشهد القطة السينمائي (`cinematic-cat.html`) عند 0 و2 و5.5 ث بـ Playwright: القطة في منتصف القفزة فوق البركة والفراشة المرشدة ترفرف — هيكل بأربع أرجل وآلة وضعيات تعمل كدالة للزمن؛ ومرّت هنا اختبارات الأرنب القطيفة المنحوت (`test_shape_kit` 4/4، أكثر من 50 ألف مثلث) وأقفال شخصيات fastify (15/15) ومشهد الحوت في `kosif-studio` (Judge 2/2).
> **You can:** design, lock, rig, walk, act and idle original characters in 2D and 3D, and route to avatar/AI services only when the user has a key. **50 powers follow** — ✅ 6 · 🟢 14 · 📦 2 · 🔑 4 · 👁 11 · 📄 13 · 💡 0.

**الحالة / status:** ✅ مُثبت هنا (كود + اختبار أو رندر في هذه الحاوية) · 🟢 جاهز (كود المالك يعمل بلا إضافات) · 📦 بأمر تثبيت · 🔑 مفتاح أو خدمة · 👁 شوهد في فيديو أنتجتَه (وصفة البناء مرفقة) · 📄 موصوف فقط · 💡 فكرة.
مسارات الدليل نسبية إلى `/home/user/`؛ `style:<id>` = فيديو مرجعي أنتجتَه سابقًا (ملاحظاته في `kosif-tool/styles/<id>/`).

**قاعدتان قبل أي شخصية:** تصاميم أصلية فقط (لا شخصيات محمية بحقوق)، وفي الأفلام العربية تدخل الشخصية من اليمين وتنظر يسارًا وفقاعات كلامها جمل عربية كاملة (`kosif-tool/playbooks/characters.md`).

## الفهرس / contents
- **التصميم والثبات — Design, model sheets & identity locks** — CHAR-01 … CHAR-09 (9)
- **هياكل ثنائية الأبعاد — 2D rigs** — CHAR-10 … CHAR-23 (14)
- **المشي والقفز والتمثيل — Locomotion & acting** — CHAR-24 … CHAR-35 (12)
- **حياة الشخصية والحركة الثانوية — Idle life & secondary motion** — CHAR-36 … CHAR-39 (4)
- **شخصيات ثلاثية الأبعاد — 3D characters** — CHAR-40 … CHAR-46 (7)
- **محركات ومكونات وأساليب جاهزة — Engines, components & catalog styles** — CHAR-47 … CHAR-50 (4)
- توليفات قوية / power combos · أخطاء ممنوعة / never do · أقوى 5 حركات توقيع / 5 signature moves

## التصميم والثبات — Design, model sheets & identity locks

_الشخصية تُصمم وتُقفل قبل أن تتحرك._

#### CHAR-01 · ورقة تصميم الشخصية واختبار الظل · Model sheet & silhouette test · 📄 موصوف / documented only
- **ماذا / what:** اكتب النسب واللوحة وسماكة الخط والزوايا قبل التحريك، وكل وضعية مفتاحية يجب أن تُقرأ كظل أسود مصمت. — Lock proportions, palette, line weight and views before animating; every key pose must read as a solid black shape.
- **متى أستخدمها / when:** قبل أول إطار لأي شخصية متكررة — before the first frame of any recurring character.
- **كيف / how:** STYLE.md: 3–5 colours, outline weight and colour, views front / side / three-quarter (+ rear and the in-video camera view) on one ground line and scale, 3–5 key expressions; one canonical spec per character kept apart from style skills (silhouette, fixed features, proportions, default palette, e.g. whale mascot #FFFFFF belly, #D9D9D9 back, #F0F0F0 cheek, #1A1A1A outline); build the SVG rig with grouped parts and pivots so every video reuses the same character; fill the pose with black to check readability. **أرقام / params:** 3–5 colours; 3–5 views.
- **الدليل / proof:** `kosif-tool/playbooks/characters.md:15` · `kosif-atlas/skills/1094-akbun-draw/2427-akbun-mascot-whale/SKILL.md` · `kosif-atlas/skills/1526-gamegen/4166-game-concept-art/SKILL.md`

#### CHAR-02 · وصفة اللطافة · Cute character recipe · 📄 موصوف / documented only
- **ماذا / what:** نسب وقواعد شكل جعلت الأرنب يُقرأ لطيفًا: الرأس أعرض من الجسم، عيون منخفضة متباعدة، خدود، أنف صغير، أطراف قصيرة، باستيل مع لون تأكيد واحد. — Proportion and look rules that made the bunny read as cute.
- **متى أستخدمها / when:** أي تميمة أو شخصية أطفال — any mascot or kids' character.
- **كيف / how:** head width ≥ body (.16 vs .14); eyes at ~45% of head height, spacing 0.4 × head width, tall 1.12, two catch-lights; cheeks k ≈ .02; nose ≤ 1/8 head width; soft blends 10–30 mm; short limbs, big feet; pastel + one accent; warm key front-left-top with mint + pink rims, neutral tone curve, bloom threshold ≥ .9; alive acting: breathing ±0.6%, blinks, ear flop. **أرقام / params:** head .16 vs torso .14; eyes 45% / 0.4×.
- **الدليل / proof:** `kosif-studio/motion/references/shape-kit.md` · `100-superskills/skills/kosif-montage-motion/references/shape-kit.md`

#### CHAR-03 · أقفال الهوية النصية · Identity lock text (CHR/LOC sheets) · 📄 موصوف / documented only
- **ماذا / what:** فقرة قفل واحدة لكل شخصية ومكان تُلصق حرفيًا في كل وصف لاحق، مع صحائف 360° للزوايا والتعابير. — One lock paragraph per character and location pasted verbatim into every later prompt, with 360° sheets.
- **متى أستخدمها / when:** أي سلسلة مشاهد مولدة لنفس الشخصية — any generated series with a recurring character.
- **كيف / how:** CHR-001: name · age · skin tone · face shape · eyes · brows · nose · lips · hair · build/height · signature outfit · accessories · marks · MUST NOT CHANGE: …; views front, 3/4 left, profile, back, full-body contrapposto; expressions neutral, joy, anger, fear, determination; LOC-001: era, scale, left/right/centre landmarks, time-of-day variants. Models have no memory: copy the CHARACTER sentence byte-for-byte, keep background tone and the 3–5 colour palette identical, vary only the SCENE line. identity_reference.py checks 5 views (front, left, right, back, three_quarter). **أرقام / params:** 5 views; 5 expressions.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-cinema-director/references/continuity-protocols.md` · `kosif-one/tools/kosif-omni/skills/kosif-image-studio/references/prompt-library.md` · `100-superskills/skills/kosif-montage-motion/references/continuity-protocols.md` · `kosif-atlas/skills/2976-pwdev-social-media/12595-visual-consistency`

#### CHAR-04 · قفل الشخصية النفسي · Personality lock · 📄 موصوف / documented only
- **ماذا / what:** تحويل سمات شخصية خيالية إلى وقفة ونظرة وملبس ثابتة حتى يبقى تمثيلها متسقًا عبر اللقطات. — Map a fictional character's personality facets to posture, gaze and styling cues.
- **متى أستخدمها / when:** شخصيات قصصية بأكثر من مشهد — story characters across scenes.
- **كيف / how:** pick 4–6 Big-Five facets and map to cues (assertive: squared shoulders, direct gaze, centre frame; anxious: guarded arms, off-camera glance, tense jaw; ordered: pressed clothes, symmetrical workspace…); add 3 if-then behaviour signatures and the driving need (autonomy / competence / relatedness). Fictional characters only. **أرقام / params:** 4–6 facets; 3 if-then rules.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-image-studio/references/character-psychology.md`

#### CHAR-05 · بايبلات شخصيات fastify · Fastify character bibles & reference locks · ✅ مُثبت هنا / proven here
- **ماذا / what:** مواصفات ثابتة مختبرة تُلصق في كل وصف: رجل عصوي أصلي، شخصيتان أصليتان ثلاثيتا الأبعاد، ورياضي بلا وجه — مع قفل الصورة المرجعية للمستخدم. — Tested fixed specs pasted into every prompt, plus the user's reference-image lock.
- **متى أستخدمها / when:** ملفات الإنتاج المرحلية stickman / character-romance / fitness — the staged production profiles.
- **كيف / how:** Stickman BIBLE: charcoal-black 5 px brush strokes at 1080 px width, circular head = 1/4 of height, slim straight torso, single-line limbs each half a torso long, two dot eyes + one mouth stroke, tiny teal scarf at the left of the neck, palette black/teal + one muted warm accent. If the user has their own figure, prompts reference the attached image unchanged and text-only tools are refused (referenceTool 'text-only' throws). Romance: A = young woman (warm brown skin, curly dark shoulder hair with pale-blue ribbon, emerald jacket, cream boots), B = waist-high doll (porcelain face, lilac bob, coral/turquoise patchwork, amber buttons, teal boots) in all 10 prompts. Fitness: faceless muscular sculpt-render, black cap and shorts, dark gym, one overhead teal-blue rim light, shallow DOF. Profile tests 15/15 passed here. **أرقام / params:** stroke 5 px @1080; head 25% height; limb 0.5 torso.
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/stickman.mjs` · `fastify-motion-bro/scripts/profiles/character-romance.mjs` · `fastify-motion-bro/scripts/profiles/fitness.mjs` · `fastify-motion-bro/tests/production-profiles.test.mjs`

#### CHAR-06 · ثبات الشخصية في التوليد بالمراجع · Reference-based consistency in generators · 🔑 مفتاح أو خدمة / needs key
- **ماذا / what:** مراجع متعددة مسماة لكل شخصية، تعديل صورة الأفاتار الموجودة بدل توليد شخص جديد، وIP-Adapter لنقل الهوية أو الأسلوب، وأوراق الشخصيات كمراسٍ قبل الفيديو. — Named multi-reference inputs, editing the supplied avatar, IP-Adapter conditioning and character sheets as anchors.
- **متى أستخدمها / when:** حين يملك المستخدم مفتاح خدمة صور/فيديو — when the user has an image/video service.
- **كيف / how:** 4–5 references per character from different angles, labelled ('Character A: the red-haired knight'), repeat 2–3 identifiers every turn; when the setting does not change say 'Edit @Image1: …' keeping face/hair/light; ComfyUI IPAdapterAdvanced weight 0.55–0.65 for characters (> 0.75 copies pose, < 0.4 drifts), FaceID 0.7–0.85, plus ControlNet for pose; one image call per sheet (front, 3/4, profile on plain ground with one telling prop) — redo off-style sheets before animating (an image costs cents, a clip dollars). Needs Gemini/OpenAI image API keys, or a GPU ComfyUI host. **أرقام / params:** 4–5 refs; IPA 0.55–0.65; FaceID 0.7–0.85.
- **الدليل / proof:** `kosif-atlas/skills/2173-tools-plugin/7917-generate-image` · `kosif-atlas/skills/259-quickdesign/865-quickdesign` · `kosif-atlas/skills/2819-comfyui/11445-comfyui-workflow-design` · `kosif-atlas/skills/1511-homie/3889-art`

#### CHAR-07 · شريط حركة كامل من إطار واحد · Whole-strip sprite from one seed frame · 🔑 مفتاح أو خدمة / needs key
- **ماذا / what:** ولّد شريط حركة التميمة كاملًا في طلب تعديل واحد حول إطار معتمد، لأن التوليد إطارًا إطارًا ينجرف. — Generate the whole animation strip in one edit request around an approved frame.
- **متى أستخدمها / when:** سبرايتات ألعاب أو تميمة بكسل — game sprites, pixel mascots.
- **كيف / how:** place the seed on a transparent 1024 canvas with 4 slots of 256; prompt invariants (same character, facing, palette, silhouette, outfit, transparent background, exact frame count, no scenery); normalise to fixed frames (e.g. 64 px) with one shared scale and bottom-centre anchor; optionally lock frame 1 to the seed; review a preview sheet. Needs an image-edit model key. **أرقام / params:** 1024 canvas; 4 × 256 slots; 64 px frames.
- **الدليل / proof:** `kosif-atlas/skills/2696-game-studio/10368-sprite-pipeline`

#### CHAR-08 · الأفاتار الناطق · AI talking avatars · 🔑 مفتاح أو خدمة / needs key
- **ماذا / what:** فيديو مقدّم بمزامنة شفاه من نص دون تصوير، ثم يُركّب تحت رسوم متحركة مكتوبة بالكود. — Script-driven lip-synced presenters composited under coded motion graphics.
- **متى أستخدمها / when:** مقدم بلا تصوير — a presenter without filming.
- **كيف / how:** HeyGen (MCP/API: script, avatar, language; 230+ avatars, 140+ languages; personal twin from a 2–5 min recording) or Synthesia for full-body corporate presenters; keep the presenter clip as project media and lay editable scenes and Arabic captions on top. Needs a HeyGen/Synthesia account key; check Arabic lip-sync on a still before committing. **أرقام / params:** twin from 2–5 min video.
- **الدليل / proof:** `kosif-atlas/skills/1446-marketing-skills/3531-video` · `kosif-one/vendor/hyperframes/docs/guides/avatar-presenter.mdx`

#### CHAR-09 · شخصية ذكاء اصطناعي بالحالات · Stateful AI persona orb · 📦 بأمر تثبيت / one install
- **ماذا / what:** مقدم على شكل كرة بخمس حالات: سكون، استماع، تفكير، كلام، نوم — تقودها حالة الصوت. — A narrator orb with five states driven by audio state.
- **متى أستخدمها / when:** شرح منتجات الذكاء الاصطناعي — AI product explainers.
- **كيف / how:** Vercel ai-elements Persona (Rive WebGL2) via npx ai-elements add persona; local stand-in with no install: SVG/CSS state classes switched from words.json speaking segments (speaking while a word is active, thinking in gaps > 0.7 s, idle otherwise), rendered with render_html.cjs. **أرقام / params:** 5 states.
- **تثبيت / install:** `npx ai-elements add persona`
- **الدليل / proof:** `kosif-atlas/skills/2722-vercel/10522-ai-elements/SKILL.md`

## هياكل ثنائية الأبعاد — 2D rigs

_قصاصات بمفاصل، IK بعظمتين، وجوه تُبدَّل._

#### CHAR-10 · هيكل SVG بنقاط دوران · SVG cut-out rig with pivots · 🟢 جاهز / ready
- **ماذا / what:** مجموعات SVG منفصلة لكل طرف بنقاط دوران صريحة ودورانات متداخلة، والكوع يتأخر إطارين ليصنع المتابعة. — Separate SVG groups per limb with explicit pivots and nested rotations; the elbow lags 2 frames.
- **متى أستخدمها / when:** أي شخصية مسطحة تتحرك — any flat character.
- **كيف / how:** python3 tools/kosif.py scaffold character-rig <dir>; parts head, torso, upper/lower arm, hand, upper/lower leg, foot; transform rotate(θ px py) in nested <g>; Remotion arm: shoulder interpolate(frame, [0,6,14,24], [0,8,−55,−48]), elbow ([2,10,18,26] → [0,5,−30,−24]) with Easing.inOut(Easing.sin); walk 12 frames/step at 24 fps; 5–7 mouth shapes; moving hold 1–2%. **أرقام / params:** elbow +2 f; 12 f/step.
- **الدليل / proof:** `kosif-tool/playbooks/characters.md:54` · `kosif-tool/styles/character-rig/SKILL.md` · `100-superskills/skills/character-animation-2d/SKILL.md`

#### CHAR-11 · أطراف بـ IK بعظمتين · Two-bone IK limbs · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** تُعطى الوركَ وأهداف اليدين والقدمين في العالم، فيُحل الكوع والركبة بـ IK بعظمتين، ويُرسم الطرف منحنى يمر بالمفصل. — Give hip and world targets; solve elbow/knee with 2-bone IK and draw each limb as a curve through the joint.
- **متى أستخدمها / when:** رجل عصوي، دراجة بدواسات، شخصية تمسك أشياء — stickmen, pedalling, grabbing.
- **كيف / how:** bend direction from facing (elbows back, knees forward); quadratic control point = 2J − (S + E)/2 so the curve passes through the joint J; stroke ~3 px round caps. Bicycle: crank θ = ω·t (ω ≈ 2π·1 Hz), pedals at θ and θ + π, legs solved hip → pedal, wheels at gear ratio ~2.5 × ω, wheel radius 0.33 m. **أرقام / params:** ω ≈ 2π rad/s; gear 2.5.

```js
function ik2(S, T, l1, l2, bend = 1) {            // shoulder/hip S → target T
  const dx = T.x - S.x, dy = T.y - S.y, d = Math.min(Math.hypot(dx, dy), l1 + l2 - 1e-3);
  const a = Math.atan2(dy, dx), c = (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d);
  const t = a - bend * Math.acos(Math.max(-1, Math.min(1, c)));
  const J = { x: S.x + l1 * Math.cos(t), y: S.y + l1 * Math.sin(t) };   // elbow / knee
  const E = { x: S.x + d * Math.cos(a), y: S.y + d * Math.sin(a) };
  return { J, E, ctrl: { x: 2 * J.x - (S.x + E.x) / 2, y: 2 * J.y - (S.y + E.y) / 2 } };
}
```

- **الدليل / proof:** `kosif-tool/styles/stickman` · `kosif-tool/styles/pm-axtonliu-0b861d`

#### CHAR-12 · انحناء الجسم والمط حسب السرعة · Velocity-driven body bend & squash · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** الجذع أنبوب منحنٍ يُرسم مرتين، انحناؤه من سرعة الميل، ومطه وضغطه من سرعة الورك وصدمات الهبوط، والرأس يتأخر قليلًا. — Torso as a bent tube; bend from tilt velocity, squash/stretch from hip velocity and landings; head lags.
- **متى أستخدمها / when:** شخصيات خطية مرنة كوميدية — rubbery comic characters.
- **كيف / how:** torso = quadratic bezier hip → neck drawn wide black then thinner white on top (~38 px); bend = k·d(tilt)/dt computed from seek(t) and seek(t − 1/fps) (never accumulated); stretch/squash 0.85–1.15 from vertical hip velocity plus landing impulses; head follows 1–2 frames late. **أرقام / params:** tube ~38 px; squash 0.85–1.15.
- **الدليل / proof:** `kosif-tool/styles/stickman`

#### CHAR-13 · وجوه بتبديل الأشكال · Swap-shape faces, mouths & expressions · 📄 موصوف / documented only
- **ماذا / what:** العيون والفم أشكال تُبدَّل لا مسارات تُشوَّه: 5–7 أفواه، فم مغلق على م/ب، رمش، حواجب بزاوية لكل عاطفة. — Eyes and mouth are swapped shapes, not distorted paths.
- **متى أستخدمها / when:** كل شخصية تتكلم أو تتفاعل — every talking or reacting character.
- **كيف / how:** mouth index from phoneme/word timing (words.json), switch within 1 frame, closed on M/B/P (م ب ف in Arabic); eyes as dots blinking scaleY → 0.1 for 80 ms every 2.5–4 s; brows as short strokes angled per emotion; mouth per emotion (smile, flat, O + sweat drop, grit, content); up to 8 expression states (dots, ^ ^ joy, angry brows, hearts, wink + tongue) swapped on beats with a 6 px bounce, sweat-drop and sparkle overlays; screen-face robots swap glyph eyes per emotion. **أرقام / params:** 5–7 mouths; switch ≤1 f; blink 80 ms / 2.5–4 s.
- **الدليل / proof:** `kosif-tool/playbooks/characters.md:18` · `kosif-tool/styles/stickman` · `kosif-tool/styles/pm-jake11moran-a269c4`

#### CHAR-14 · شخصية قصاصات بمؤشر اتجاه · Cut-out rig with facing dial · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** قيمة اتجاه واحدة من −1 إلى 1 تزيح ملامح الوجه وتبدّل الذراع القريبة والبعيدة، وطور المشي مشتق من المسافة المقطوعة فلا تنزلق القدمان. — One facing value shifts features and swaps near/far arm; walk phase from distance so feet never slide.
- **متى أستخدمها / when:** دودل وقصص بشخصية تتجول — doodle stories with a walking character.
- **كيف / how:** parts head, near/far arm, legs, body around pivots; phase = distance / stepLength (~40 px) so speed changes never slide feet; arm swing ±20°, head bob 2–3 px; at facing 0 show both eyes centred. **أرقام / params:** step ~40 px; arm ±20°; bob 2–3 px.
- **الدليل / proof:** `kosif-tool/styles/doodle`

#### CHAR-15 · الشخصية في إطارها المحلي · Character built in its own local frame · ✅ مُثبت هنا / proven here
- **ماذا / what:** ارسم الجسم حول أصله الخاص (قدميه أو رأسه) ثم ضعه وأدره وكبّره كمجموعة واحدة، فيسهل إعادة وضعه وتحريكه. — Design a body around its own origin, then place/rotate/scale it as one group.
- **متى أستخدمها / when:** كل شخصية تُعاد في لقطات مختلفة — every character reused across shots.
- **كيف / how:** SVG: collect parts then wrap <g transform="translate(560 392) rotate(-16) scale(1.3)"> with a blurred warm rim-glow ellipse behind (#fb923c rx 80 ry 54 at .55); Pillow scenes: whale W(x,y)/WS(shape) rotate along HEAD (700,290) → TAIL (1200,760); dragon girl xf() scales 1.4× around her feet (380,619). The whale scene passes the studio judge gate (test run here). **أرقام / params:** translate/rotate/scale as one group.
- **الدليل / proof:** `kosif-one/projects/duck-vs-dragon/duck_dragon.py` · `kosif-studio/scenes/whale_dragon.py:46` · `kosif-studio/scenes/dragon_girl.py:288` · `kosif-studio/tests/test_studio.py:227`

#### CHAR-16 · أدوات تفاصيل المخلوقات · Creature detail builders · 🟢 جاهز / ready
- **ماذا / what:** جناح خفاش من عظام وغشاء متدلٍّ بين الأطراف، أشواك ظهر، صفائح بطن، وريشة منحنية — تشريح فوري للتنانين والطيور. — Bat wing, dorsal spikes, belly plates and feather leaves.
- **متى أستخدمها / when:** تنانين، طيور، كائنات خيالية — dragons, birds, fantasy creatures.
- **كيف / how:** wing(shoulder, elbow, wrist, tips, attach, sag=0.28) → (membrane, bones, veins): bone tubes 8/6/4.5, fingers 3.4 → 0.7, scallops of 12 samples, wrist claw; spikes(spine, radii, every, size) with height (4 + r·.45)·size; belly_plates(spine, radii) ribbed every 4th sample; leaf(base, tip, width, bend, n=10) for each feather of a spread wing. **أرقام / params:** sag 0.28; scallop 12.
- **الدليل / proof:** `kosif-studio/scenes/dragon_girl.py:88` · `kosif-studio/scenes/dragon_girl.py:46` · `kosif-studio/scenes/duck_dragon.py:34` · `100-superskills/skills/pixel-studio-painter/scripts/scenes/dragon_girl.py`

#### CHAR-17 · الرجل العصوي الكوميدي · Stickman comic style · 🟢 جاهز / ready
- **ماذا / what:** رجل عصوي مرن، بطاقات تسقط وتتكدس، وضربة كوميدية لنصيحة بمفارقة. — A flexible stick figure, cards that drop and stack, a comic beat with a twist.
- **متى أستخدمها / when:** نصائح ومواقف ساخرة — tips and comic situations.
- **كيف / how:** python3 tools/kosif.py scaffold stickman <dir> (SVG line rig with pivots, arcs, squash; on twos optional). Basma STY.stickman: 16:9, bright, 2.1 wps, Readex Pro, bg #FBF9F4, ink #1F2328, accent #F2C94C, floor #EFEAE0, colours #EB5757 / #F2C94C / #5B8DEF / #9B51E0 / #27AE60; sfx pop/hit/tick/shimmer; question lines end with ؟. style:stickman: pose keys with Easing.inOut(cubic) + procedural layers (breath 0.3 Hz 2 px, thumb scroll, leg kicks, 2-step walk); card flies to hand, flips at mid (250 ms), thrown 500 ms with ghosts, box squash, counter +1. **أرقام / params:** 2.1 wps; breath 0.3 Hz.
- **الدليل / proof:** `kosif-tool/styles/stickman/SKILL.md` · `app/public/js/10_studio.js:504` · `kosif-tool/styles/stickman`

#### CHAR-18 · تحريك رسمة واحدة بعظام · 2D mesh bone rig from one image · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** تُقسم الرسمة إلى أجزاء وتُشوَّه شبكتها بنحو 16 عظمة، مع دورات رقص جيبية على الإيقاع. — Split an illustration into parts and deform its mesh with ~16 bones, sine dance cycles on the beat.
- **متى أستخدمها / when:** تحريك رسمة المستخدم أو شخصية ثابتة — animating a user's drawing.
- **كيف / how:** parts on separate layers with pivots; per-bone rotation = A·sin(2π·(BPM/60)·t + φ) (150 BPM in the reference); mesh deform via a skinned plane (three.js SkinnedMesh or PIXI mesh) or per-part rotation if the drawing is flat; keep amplitudes small at joints to avoid tearing. **أرقام / params:** ~16 bones; 150 BPM.
- **الدليل / proof:** `kosif-tool/styles/pm-topi-003-b0e12c`

#### CHAR-19 · أشياء بوجوه وتمائم · Object-as-character faces & mascots · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** حوّل أي شيء إلى شخصية بعينين لامعتين وحاجبين: بلاطة، كرة، فقاعة كلام، كتلة شوكية — مع رمش وانضغاط وتمايل. — Turn any object into a character with glossy eyes and brows.
- **متى أستخدمها / when:** تمائم العلامات، شرح ودود — brand mascots, friendly explainers.
- **كيف / how:** two glossy black spheres (metalness .6, roughness .15, radius ~8% of the tile width) slightly protruding + capsule brows animated in y/rotation; blink scaleY 100 ms every 2–4 s; egg sphere scale (1, 1.25, 1) with emissive orange and a headlamp point light, landing squash y .75 for 80 ms; speech-bubble blob with kawaii eyes, blush, bounce 1.1/0.9; spiky SVG blob idle wobble ±4° and scale .97–1.03 in a 1.2 s loop, 8–15% of frame, hopping between corners and reacting; googly eyes on everyday props. **أرقام / params:** eye r ~8% tile; blink 100 ms.
- **الدليل / proof:** `kosif-tool/styles/pm-anilraok-eff262` · `kosif-tool/styles/pm-gorden-sun-041f56` · `kosif-tool/styles/pm-anthonyriera-9b1b2a` · `kosif-tool/styles/pm-anas0ra-e57aea`

#### CHAR-20 · مسرح شخصية بديكور واحد · Single-set character stage · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** غرفة واحدة مرسومة كطبقات SVG، والشخصية بين ظهر المكتب وواجهته فتختفي ذراعاها خلفه طبيعيًا. — One illustrated room as SVG layers with the character between desk back and desk front.
- **متى أستخدمها / when:** سلسلة حلقات بنفس المكان — episodic series in one place.
- **كيف / how:** ~6 layers (wall, window, props, desk back, character, desk front); character pivot at the desk line; characters on twos while UI elements stay smooth — never mix the two cadences on one element (steps(12) per second). **أرقام / params:** ~6 layers; 2-frame holds.
- **الدليل / proof:** `kosif-tool/styles/pm-jake11moran-a269c4` · `kosif-tool/styles/pm-jake11moran-a269c4/BRIEF.md`

#### CHAR-21 · شخصيات ظلية مسطحة · Flat silhouette characters · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** شخصية بتعبئة داكنة واحدة ومفصلين أو ثلاثة، تُقرأ بالمحيط فقط أمام خلفية مضيئة. — A single dark-fill character with 2–3 joints, read only by outline.
- **متى أستخدمها / when:** قصص هادئة وأجواء ليلية — quiet stories, night moods.
- **كيف / how:** fill ~#0d0c0b, no internal detail, side profile (cap, long coat); walk 12 frames per step at 24 fps cadence; galloping silhouettes loop over speed lines; glowing stroke figures (lime with blur glow) for logos. **أرقام / params:** #0d0c0b; 12 f/step.
- **الدليل / proof:** `kosif-tool/styles/pm-kamstudiolabs-0b0824` · `kosif-tool/styles/pm-kamstudiolabs-0b0824/BRIEF.md` · `kosif-tool/styles/pm-utopyaszx-1b2f94`

#### CHAR-22 · تمائم البكسل والسبرايت · Pixel & sprite mascots · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** تميمة بكسل تمشي بتبديل رجلين وإطارين، وساحر بكسل يرفع عصاه بست خطوات، وتبديل الشخصية بنفخة دخان. — Pixel mascots with 2-frame leg swaps, stepped staff raises and smoke-puff swaps.
- **متى أستخدمها / when:** ألعاب، تقنية، حنين ريترو — games, tech, retro nostalgia.
- **كيف / how:** walking brick sprite: two eyes, four legs, 2-frame leg swap + 2 px bob at ~6 fps, colour #d17c55, slides with the camera; wizard: walk, staff raise in 6 stepped frames, 2-frame hat overshoot, rune circle at 8 fps; class swap wizard → knight → rogue behind a 6–8 frame pixel smoke puff; index = floor(frame·fps_target/30) % n. **أرقام / params:** 6–8 fps; puff 6–8 f.
- **الدليل / proof:** `kosif-tool/styles/pm-lemomo-ai-0d9cff` · `kosif-tool/styles/pm-0xevinho-3777d8` · `kosif-tool/styles/pm-0xevinho-3777d8/BRIEF.md`

#### CHAR-23 · تحولات الشخصية · Character transformations & variants · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** نفس الشخصية تكبر عبر مراحل بنفس الألوان، أو أجزاؤها تنفصل وتتركب في مواضعها مع اهتزاز الكاميرا عند التلامس. — The same character ages through variants, or its parts dock into slots with a contact shake.
- **متى أستخدمها / when:** قصص النمو، روبوتات تتجمع — growth stories, assembling robots.
- **كيف / how:** swap rig variants per stage keeping palette and silhouette cues; transform & dock: parts tween rotation/position into slots, camera shake 6 px for 150 ms on each contact (EASE-51 hitPulse). **أرقام / params:** shake 6 px / 150 ms.
- **الدليل / proof:** `kosif-tool/styles/pm-loicrambo-ad6830` · `kosif-tool/styles/pm-allforbigfire-86ff3c`

## المشي والقفز والتمثيل — Locomotion & acting

_دورة مشي بلا انزلاق، قفزة بقوس، ورد فعل يُقرأ._

#### CHAR-24 · دورة المشي · Walk cycle · 📄 موصوف / documented only
- **ماذا / what:** تلامس ← نزول ← عبور ← صعود، مع اهتزاز الجسم، والمشي في المكان مع خلفية تتحرك بسرعة الخطوة. — Contact-down-passing-up with body bob; walk in place with background parallax at stride speed.
- **متى أستخدمها / when:** كل شخصية تمشي — every walking character.
- **كيف / how:** 24 frames per two steps at 24 fps (12 per step); bob 3–5% of height; background speed = stride / 0.5 s; clip names, durations, loop flag and event markers (contact, footsteps); check body bob and limb separation; phase = f(t) so any frame renders directly; walk/idle/talk as functions of phase returning limb angles and body height with distinct contact and passing poses. **أرقام / params:** 12 f/step; bob 3–5%.
- **الدليل / proof:** `kosif-tool/playbooks/characters.md:27` · `kosif-atlas/skills/1526-gamegen/4162-game-animation/SKILL.md` · `100-superskills/skills/character-animation-2d/SKILL.md`

#### CHAR-25 · ساق مشي إجرائية · Procedural walk-cycle leg · ✅ مُثبت هنا / proven here
- **ماذا / what:** ساق مرسومة كضربة منحنية، قدمها تتأرجح بجيب الطور وترتفع في النصف الأمامي فقط، والأرجل البعيدة أغمق، وأربع أرجل بإزاحة π تعطي مشية طبيعية. — A curved-stroke leg whose foot swings with sin(phase) and lifts only on the forward half.
- **متى أستخدمها / when:** حيوانات رباعية مسطحة — flat quadrupeds.
- **كيف / how:** leg(x, phase, far): foot = x + 22·sin(phase), knee = x + 12·sin(phase), lift = max(0, cos(phase))·15; quadratic path stroke 23, round caps, paw stroke 15; step 1.5 Hz, bob cos(2p)·2 px, tail ±9° at half step rate, blink 0.095 s every 4 s; the 8 s loop walks right→left (x = 680 − 145t with a copy 1160 px behind). Captured frames here at 0 / 2 / 5.5 s with Playwright (window.render(t)) show the gait advancing. **أرقام / params:** swing ±22 px; lift 15 px; 1.5 Hz.

```js
function leg(x, phase, far) {
  const foot = x + 22 * Math.sin(phase), knee = x + 12 * Math.sin(phase);
  const lift = Math.max(0, Math.cos(phase)) * 15;          // lift only while swinging forward
  return `<path d="M${x} 300 Q${knee} 330 ${foot} ${360 - lift}"
    stroke="${far ? '#c46f2a' : '#e5953c'}" stroke-width="23" fill="none" stroke-linecap="round"/>`;
}
// four legs: phases p, p + π, p + π/2, p + 3π/2 with p = 2π·1.5·t
```

- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cat.html` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cat.mp4`

#### CHAR-26 · آلة حالات الوضعية · Keyframed pose state machine · ✅ مُثبت هنا / proven here
- **ماذا / what:** تمثيل الشخصية كمقاطع زمنية: مشي، انحناء تمهيدي، قفزة بقوس، ضغط هبوط، مشي، ثم نظرة للأعلى — والأطراف تعاد وضعيتها لكل مقطع. — Character action as time segments with limbs re-posed per segment.
- **متى أستخدمها / when:** مشهد قصير بقصة حركية — a short scene with a physical story.
- **كيف / how:** pose(t): walk x = 430 + 59t (gait 1.12 Hz) until 4.1 s; crouch 14·smoothstep((t − 4.65)/0.55); jump u ∈ [5.2, 6.9] s: x 671.9 → 1050, height 147·4u(1 − u), body angle −14° → +12°; land crouch 18·sin; walk 48 px/s at 0.98 Hz; tail 12 sin 2.2t + 3 sin 5t; look = smoothstep((t − 9.7)/0.7) with a 3/4 look-back. Four legs separately articulated (stance 60% of cycle, swing lift 21·sin(πv)). Frame captured here at 5.5 s shows the cat mid-leap over the puddle. **أرقام / params:** apex 147 px; flight 1.7 s; 1.12 → 0.98 Hz.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cinematic-cat.html` · `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/assets/scene.js:59` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/midnight-cat.mp4`

#### CHAR-27 · مولد المشي للسبرايت · Procedural sprite walk generator · 📄 موصوف / documented only
- **ماذا / what:** دالة رسم واحدة بمعاملات زوايا الأطراف وطور الخطوة واهتزاز الجسم وأرجحة الذراع والضغط تبقي كل إطار على النموذج. — One draw(direction, pose) function keeps every frame on-model.
- **متى أستخدمها / when:** شخصيات بكسل وألعاب — pixel characters, games.
- **كيف / how:** Python/Pillow or canvas; proportion presets chibi / standard / tall; walk 4–8 frames, bob 1 px; RPG-style 3 patterns 0-1-2-1; mirror the side view only if symmetric and shade after mirroring with light from top-left. **أرقام / params:** 4–8 frames; bob 1 px.
- **الدليل / proof:** `kosif-atlas/skills/2460-pixel-art/9525-animate`

#### CHAR-28 · الوضعيات المفتاحية أولًا · Pose-to-pose blocking · 📄 موصوف / documented only
- **ماذا / what:** ضع الوضعيات المفتاحية ثم الوسيطة، كل 8–16 إطارًا. — Block keys, then breakdowns.
- **متى أستخدمها / when:** كل تمثيل شخصية — all character acting.
- **كيف / how:** keys every 8–16 frames at 24–30 fps; stick rig: joint angles per pose interpolated easeInOut over 400 ms, hold 1 s; follow-through 2–4 frames, anticipation 4–8 frames (EASE-49). **أرقام / params:** keys 8–16 f; 400 ms + 1 s hold.
- **الدليل / proof:** `kosif-tool/playbooks/characters.md:24` · `kosif-tool/styles/pm-chrisjdimarco-f068db`

#### CHAR-29 · لحظة رد الفعل · Reaction beat recipe · 📄 موصوف / documented only
- **ماذا / what:** هبوط، قفزة، هبوط بانضغاط، متابعة للشعر، ثبات متنفس. — Sink, jump, land with squash, hair follow-through, breathing hold.
- **متى أستخدمها / when:** دهشة، فرح، اكتشاف — surprise, joy, discovery.
- **كيف / how:** 0–200 ms sink 4% ease-in sine; 200–450 ms jump ease-out cubic; 450–700 ms land squash 8% on a spring (damping 12, stiffness 200); 450–800 ms follow-through; 800–2000 ms breathing hold. Hop with anticipation: 120 ms crouch, squash .80–.85 / stretch 1.15, landing cubic-bezier(.34,1.56,.64,1) 450 ms, limbs overlap 60 ms, area preserved (sx·sy = 1). **أرقام / params:** 0/200/450/700/800/2000 ms.
- **الدليل / proof:** `kosif-tool/playbooks/characters.md:36` · `kosif-tool/styles/pm-abderrahmen-g-9e8ed0/BRIEF.md` · `kosif-tool/styles/pm-paulo-kombucha-96431c/BRIEF.md`

#### CHAR-30 · الإشارة والكشف · Point and reveal · 📄 موصوف / documented only
- **ماذا / what:** الذراع تمتد على قوس، والهدف يقفز بعد توقف الإصبع بـ 80 ملّي ثانية. — The arm extends on an arc; the target pops 80 ms after the finger stops.
- **متى أستخدمها / when:** شخصية تقدم بطاقات أو ميزات — a character presenting cards.
- **كيف / how:** arm 350 ms on an arc; target pops at +80 ms; Basma 'character' template: hop in, point at 3 cards, react, wave (circle body, dot eyes, squash & stretch, anticipation, blinking, reacting to on-screen text). **أرقام / params:** arm 350 ms; +80 ms.
- **الدليل / proof:** `kosif-tool/playbooks/characters.md:50` · `app/public/js/00_editor.js:2007`

#### CHAR-31 · الحديث للكاميرا · Talk-to-camera behaviours · 📄 موصوف / documented only
- **ماذا / what:** ميل الرأس على النبر، رمش دوري، والفم من توقيت الأصوات. — Head tilts on stress, periodic blinks, mouth from phoneme timing.
- **متى أستخدمها / when:** شخصية تشرح بصوت المستخدم — a character narrating the user's voice.
- **كيف / how:** tilt ±3° on stressed words (from the emphasis picker ARAB-68 / words.json), blink every 2.5–4 s with a 3-frame blink, mouth index from word timing (CHAR-13); add a small head nod on sentence ends. **أرقام / params:** ±3°; blink 2.5–4 s, 3 f.
- **الدليل / proof:** `kosif-tool/playbooks/characters.md:48`

#### CHAR-32 · ظهور التمائم وقفزاتها · Mascot pop-ins & hop arcs · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** الشخصيات تصعد من خلف الأفق بتجاوز، أو تقفز بداخل دائرة ملونة، أو تقفز على قوس منقط. — Characters rise from behind a hill, pop in on a colour disc, or hop along a dotted parabola.
- **متى أستخدمها / when:** تقديم شخصيات أو فريق — introducing characters or a team.
- **كيف / how:** horizon rise: masked below the hill line, 350 ms easeOutBack(1.6), stagger 150–250 ms left→right (start right for Arabic), then idle bob ±3 px; disc pop: cut-out PNG 0.8 → 1.05 → 1 in 300 ms while a pastel circle grows 400 ms, name pill 'الاسم: الدور' below; hop arc ~1 s along a dotted parabola drawn trailing behind, landing squash. **أرقام / params:** 350 ms backOut 1.6; pop 300 / disc 400 ms.
- **الدليل / proof:** `kosif-tool/styles/pm-abderrahmen-g-9e8ed0` · `kosif-tool/styles/pm-paulo-kombucha-96431c` · `kosif-tool/styles/pm-kangaroohere-b10f8d`

#### CHAR-33 · لمسات تمثيل · Acting accents: celebrate, sleep, run · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** مزج من وضعية الركوب إلى بسط الجناحين بتجاوز، حروف Z طافية للنوم، وعدّاء بتمويه حركة يقفز الحواجز. — Celebration blends, floating Z glyphs, a motion-blurred hurdler.
- **متى أستخدمها / when:** ختام فرح، شخصية نائمة، رياضة — happy endings, sleepy characters, sports.
- **كيف / how:** celebration: blend riding → wings-spread over ~0.8 s back.out (wing rotation ~70°), hold, return; sleep: Z glyphs rise, scale up and fade, stagger 250 ms; runner: 8-frame cycle along a baseline, jump arc 400 ms, directional blur (EASE-61). **أرقام / params:** 0.8 s; Z stagger 250 ms; cycle 8 f.
- **الدليل / proof:** `kosif-tool/styles/pm-axtonliu-0b861d` · `kosif-tool/styles/pm-cansincengiz-me-cf68dd` · `kosif-tool/styles/pm-fionntobin-97b7af`

#### CHAR-34 · مبادئ التحريك للهياكل · Animation principles for rigs · 📄 موصوف / documented only
- **ماذا / what:** تمهيد، ضغط عند الهبوط، متابعة للشعر والقماش، أقواس، وحجم ثابت — ولحظة الاصطدام تُثبَّت. — Anticipation, landing squash, hair/cloth follow-through, arcs, constant volume; hold impact frames.
- **متى أستخدمها / when:** مراجعة أي حركة شخصية — reviewing any character motion.
- **كيف / how:** locomotion needs contact / passing / extreme poses with planted feet; actions need readable anticipation, contact and recovery (player-facing attacks avoid long anticipation); hold the impact frame; keep volumes constant; verify encoded frame count, fps and duration after render.
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4162-game-animation/SKILL.md` · `100-superskills/skills/character-animation-2d/SKILL.md`

#### CHAR-35 · الشخصية العربية تدخل من اليمين · RTL character staging · 📄 موصوف / documented only
- **ماذا / what:** في الأفلام العربية تدخل الشخصيات من اليمين وتنظر يسارًا، وفقاعات الكلام تحمل جملًا عربية كاملة من اليمين. — In Arabic films characters enter from the right and look left; bubbles hold whole RTL phrases.
- **متى أستخدمها / when:** كل فيلم شخصيات عربي — every Arabic character film.
- **كيف / how:** mirror the staging plan (entrances, look direction, reading path); balloons pop with a spring and contain whole shaped phrases (never per letter); stagger group entrances right → left.
- **الدليل / proof:** `kosif-tool/playbooks/characters.md:75`

## حياة الشخصية والحركة الثانوية — Idle life & secondary motion

_الشخصية لا تتجمد أبدًا._

#### CHAR-36 · حياة الخمول · Idle life (breath, blink, glances) · 🟢 جاهز / ready
- **ماذا / what:** تنفس صغير، تمايل الرأس على عدة موجات، رمش مجدول، أذنان وذيل — كلها دالة للزمن. — Breathing, head sway, scheduled blinks, ears and tail as a pure function of t.
- **متى أستخدمها / when:** أي ثبات للشخصية — any character hold.
- **كيف / how:** K3.idle(root, t, {amount, phase}): breath ±1.2% at 2.2 rad/s, blink every 3.7 s lasting 0.3 s, ears ±.12 rad at 2.6, tail ±.35 rad at 3.1; bunny project: breath .006·sin(2π·0.9t), head (.05 sin 1.7t, .12 sin(1.1t + .5), .05 sin 1.3t), blink windows 1.18–1.34 s and 4.62–4.76 s with eye scaleY 1 − .85·bl, a 0.25 rad head turn toward camera at its stop; 2D moving hold: torso scale 1–2% over 2 s. **أرقام / params:** breath 0.6–1.2%; blink /3.7 s.
- **الدليل / proof:** `kosif-studio/motion/kit/lab-kit.js:280` · `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js:118` · `kosif-tool/playbooks/characters.md:28`

#### CHAR-37 · حركة ثانوية بالنوابض · Spring-rig secondary motion · 🟢 جاهز / ready
- **ماذا / what:** مجموعات مفاصل تقودها نوابض (تردد وتخميد) لارتخاء الأذن وارتداد الذيل، تحت حد سرعة. — Pivot groups driven by frequency/ζ springs under a speed gate.
- **متى أستخدمها / when:** آذان، ذيول، شعر، إكسسوارات متدلية — ears, tails, hair, dangling props.
- **كيف / how:** angle = A·(1 − spring(t, t0, f, ζ)) on each pivot (EASE-25); ear flop f 1.5 Hz ζ 0.42 passes; f 2.2 Hz ζ 0.28 failed the 80 px/frame gate at 1080×1920 — measure with motion.py speed (EASE-60). **أرقام / params:** 1.5 Hz ζ .42 ok; 2.2/.28 fails.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/shape-kit.md` · `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js`

#### CHAR-38 · فراشة ويراعة مرافقة · Winged companions (butterfly, firefly) · ✅ مُثبت هنا / proven here
- **ماذا / what:** فراشة متوهجة ترشد البطل: جناحاها يرفرفان بتحجيم أفقي وتتمايل على مسار جيبي بهالة سماوية. — A glowing butterfly leads the hero, flapping by horizontal scale on a sine path.
- **متى أستخدمها / when:** مرشد صغير في مشهد ليلي — a small guide in night scenes.
- **كيف / how:** wing scaleX = |sin(2π·4.5t)|·0.85 + 0.13; y = 348 − 20 sin 1.8t − 48·smooth((t − 4.2)/1.8) + 55·smooth((t − 7)/2); fill #86fff0 at .87, halo r 28; firefly: oval body, big eyes, flap 8 Hz, radial-gradient glow on the tail. Visible in the frame captured here at 5.5 s. **أرقام / params:** 4.5 Hz (butterfly), 8 Hz (firefly).
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cinematic-cat.html` · `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/assets/scene.js:107` · `kosif-tool/styles/pm-kamstudiolabs-c9bb28`

#### CHAR-39 · سرب طيور · Flock of birds · 🟢 جاهز / ready
- **ماذا / what:** طيور على شكل V مكررة بالمثيلات ترفرف في الشيدر وتتبع مسارًا مفتاحيًا. — Instanced V-shaped birds flapping in a shader along a keyed path.
- **متى أستخدمها / when:** سماء حية، غروب، رحلة — living skies, sunsets, journeys.
- **كيف / how:** K3.makeFlock({n:18, path:[[t,x,y,z],…], t0, t1, spread:120, size:9, color:'#1a1d22', seed}); mesh.userData.set(t); flap sin(t·9). **أرقام / params:** n 18; spread 120; flap sin 9t.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:203`

## شخصيات ثلاثية الأبعاد — 3D characters

_شخصيات منحوتة إجرائيًا بمفاصل مسماة._

#### CHAR-40 · الأرنب القطيفة المنحوت · SDF plush bunny (rigged) · ✅ مُثبت هنا / proven here
- **ماذا / what:** أرنب لطيف منحوت إجرائيًا بأجزاء مفصلية مسماة (جسم، رأس، أذنان، ذيل، عينان، فم، وشاح) وعيون موضوعة بإصابة الأشعة. — A procedurally sculpted plush bunny with named rig parts.
- **متى أستخدمها / when:** تميمة ثلاثية الأبعاد، قصص أطفال، إعلانات لطيفة — 3D mascots, kids' stories.
- **كيف / how:** const b = K3S.bunny({fur:'#f2e4d8', belly:'#fbf3ea', pink:'#ff9fb8', nose:'#ff7c9c', scarf:'#7fe7b4', cells:132}); animate b.parts.head / earL / earR / tail rotations (neck pivot [0, .152, .004], ears pivot from the skull); ~0.33 m tall; stage disc (r .24, #9dffb4, shadow .5) and studio backdrop (#22504a / #0d2627 / #040b0c); 'w' mouth and stitches as Catmull-Rom tubes (32 segments, r 1.1 mm). test_shape_kit passed here (96 cells > 50,000 triangles; 183,752 triangles at full res, ~4.6 s mesh time). **أرقام / params:** ~0.33 m; 132 cells.
- **الدليل / proof:** `kosif-studio/motion/kit/shape-kit.js:453` · `100-superskills/skills/kosif-montage-motion/tests/test_shape_kit.py:40` · `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js:29`

#### CHAR-41 · عيون لامعة وعيون برمش · Glossy & blinking eyes · 🟢 جاهز / ready
- **ماذا / what:** مقلة لامعة بحلقة قزحية دافئة ونقطتي ضوء، أو عين بطبقات (صلبة، قزحية مضيئة، بؤبؤ، قرنية) برمش. — Glossy eyeballs with two catch-lights, or layered eyes with a blink.
- **متى أستخدمها / when:** كل شخصية ثلاثية الأبعاد — every 3D character.
- **كيف / how:** K3S.eye({r:.012, tall:1.12, color, iris:'#5a3a2c'}) — iris at 55%, catch-lights .3r and .14r upper-outer, gloss roughness .08, clearcoat 1, ior 1.5, env 1.6; K3.makeEye(r, {iris}): sclera #f4f6f2, iris #8fe02a (emissive 12%), pupil #05070a, cornea opacity .22; eye.userData.blink(k) scales y by 1 − .92k. **أرقام / params:** r .012; catch-lights .3/.14 r.
- **الدليل / proof:** `kosif-studio/motion/kit/shape-kit.js:311` · `kosif-studio/motion/kit/lab-kit.js:56`

#### CHAR-42 · أرنب وأسد المختبر · Lab rabbit & lion characters · 🟢 جاهز / ready
- **ماذا / what:** حيوانان قطيفة بمفاصل مسماة وفرو بطبقات قشرية على أرضية استوديو كريمية، مع HUD يسمي الأجزاء ومبادلة أجزاء. — Two plush animals with named joints and shell fur on a cream sweep, with a part-naming HUD.
- **متى أستخدمها / when:** شرح «كيف صُنع»، مقارنة، علوم للأطفال — 'how it's made', comparisons, kids' science.
- **كيف / how:** K3.makeRabbit({color:'#f1f0ea', inner:'#f3b6c0', iris:'#3a7bd5', furLength:.09, layers:7}); K3.makeLion({color:'#e3b05a', mane:'#8a4a1c', iris:'#d9a21b', muzzle:'#f5e2b8', furLength:.07, layers:8, mane ×2.6, gravity .5}); root.userData.joints; studio(scene); labPost(renderer, …, {bloom:0}); six HUD beats SHAPE → JOINT → LOAD → BREAK → SWAP → RANK; swap: rabbit tail colour lerps to 0x8a4a1c and scales 1 + .45·sw over 16.4–17.2 s; materials leather 0x15171a, metal 0xd8dde3; motion.py new NAME --lab scaffolds it (960×540, 24 fps, 20 s). **أرقام / params:** fur .07–.09; 7–8 layers.
- **الدليل / proof:** `kosif-studio/motion/kit/lab-kit.js:74` · `kosif-studio/motion/kit/lab-kit.js:101` · `kosif-studio/motion/projects/lab_rabbit_lion/README.md`

#### CHAR-43 · سمكة كوي إجرائية · Procedural koi · 🟢 جاهز / ready
- **ماذا / what:** سمكة كوي بجسم مرفوع وزعانف وجلد بنقوش حراشف ببذرة في أربعة أنواع، وانحناء سباحة يميل في المنعطفات. — A lofted koi with seeded scale skin in four varieties and a swim bend that leans into turns.
- **متى أستخدمها / when:** برك، حدائق يابانية، هدوء — ponds, calm scenes.
- **كيف / how:** const k = K3.makeKoi({length:.62, seed, kind:'kohaku'|'sanke'|'showa'|'ogon', amp:.11, caustics}); k.userData.set(t, path(t, out), 1.6); 28 rings × 18 segments, skin 256 px, clearcoat .6; base #f4eee4 (ogon #e8be5a), red #e25620 (showa #c4341c), black #181618. **أرقام / params:** .62 m; swim 1.6 Hz; amp .11.
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:629` · `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:613`

#### CHAR-44 · شخصيات من أشكال أولية · Primitive toon figures · 🟢 جاهز / ready
- **ماذا / what:** شخصيات كرتونية من كرات وكبسولات بعيون كبيرة ومفاصل هرمية، أو صياد من الخلف يكفي ليُقرأ إنسانًا. — Toon characters from spheres and capsules with hierarchical joints.
- **متى أستخدمها / when:** مشاهد ثلاثية الأبعاد سريعة تحتاج إنسانًا — quick 3D scenes needing a figure.
- **كيف / how:** fisherman: torso Capsule(.2, .42) rotated −.18, head sphere .13 + half-sphere cap 0xcfc6b2, leg capsules, rod cylinder .008 → .02 oriented by a quaternion base → tip, Line to the water; toon material + big eyes for cartoon figures; keep pivots at joints for rotation. **أرقام / params:** capsule .2/.42; head .13.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:96` · `kosif-tool/styles/pm-ryzoft-4f85bd`

#### CHAR-45 · دوران 360 لورقة الشخصية · Turntable character sheet · 🟢 جاهز / ready
- **ماذا / what:** الكاميرا تتوقف أمام وجانب وظهر وجانب الشخصية بثبات، كورقة دوران قبل التحريك. — Camera steps front, side, back, side with holds, like a turnaround sheet.
- **متى أستخدمها / when:** اعتماد الشخصية مع المستخدم قبل الفيلم — approving a character before the film.
- **كيف / how:** K3.shot('turntable', {subject, size, t0, t1}): 4 quarter turns, each holding 70% of its quarter and turning in the last 30%; frame at 80% of height; render once and show the user as a contact sheet. **أرقام / params:** 4 holds; turn in last 30%.
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:1066` · `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:1067`

#### CHAR-46 · جسد من الجسيمات بحركة حقيقية · Particle body from real motion (mocap) · 🟢 جاهز / ready
- **ماذا / what:** مؤدٍّ مصوّر بكاميرا ثابتة يصبح جسيمات متوهجة داخل ظله مع أشباح متتبعة. — A performer on a fixed camera becomes glowing particles inside the silhouette, with tracer ghosts.
- **متى أستخدمها / when:** رقص، رياضة، لحظة سحرية — dance, sport, magical moments.
- **كيف / how:** python motion.py mocap VIDEO --out body.json [--points 1200] (background difference, threshold 28, coords 0..1000; OpenCV 5.0 is installed here) → K3.makeParticleBody(json, {height:4, depth:.35, ghosts:3, ghostStep:3, color:'#ffb36b', size:26}); userData.set(t, pulse); ghost alpha .35/k. **أرقام / params:** 1200 pts; 3 ghosts every 3 f.
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:938` · `kosif-studio/motion/motion.py` · `100-superskills/skills/kosif-montage-motion/scripts/qa.py:605`

## محركات ومكونات وأساليب جاهزة — Engines, components & catalog styles

_ما يُستدعى بأمر واحد._

#### CHAR-47 · تمثيل الشخصيات بلوتي · Lottie character acting · 📦 بأمر تثبيت / one install
- **ماذا / what:** تمثيل الشخصية (مشي، توقف، إشارة، سكون) في ملف Lottie واحد، وGSAP يملك البطاقات والكاميرا موقوتة على علامات الملف. — The character's acting lives in one Lottie; GSAP owns cards and camera timed to its markers.
- **متى أستخدمها / when:** شخصية مصممة في After Effects أو مرخصة — AE-made or licensed characters.
- **كيف / how:** lottie-web or dotLottie player registered for seeking (goToAndStop(frame, true) from seek(t)); read beat times from markers (tm frames / fr); 1 s walk cycle loop:true moved with GSAP x matched to stride; offset actions inside the file; HyperFrames block lottie-character-walk (planted feet, stops and points at a card, 7.5 s); license the character. **أرقام / params:** walk loop 1 s; block 7.5 s.
- **تثبيت / install:** `npm i lottie-web`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/adapters/lottie.md` · `kosif-one/vendor/hyperframes/registry/blocks/lottie-character-walk/lottie-character-walk.html`

#### CHAR-48 · لوحات الكوميكس · Comics panels · 🟢 جاهز / ready
- **ماذا / what:** قصة في لوحات بفواصل وفقاعات كلام، والكاميرا تتنقل بين اللوحات. — A story in comic panels with gutters and balloons; the camera travels panel to panel.
- **متى أستخدمها / when:** قصص قصيرة وحكايات تعليمية — short stories, lessons.
- **كيف / how:** python3 tools/kosif.py scaffold comics-panels <dir>; Canvas/SVG panel grid, each panel a scene with a pose-to-pose rig (keys every 8–16 frames, anticipation 4–8 frames); camera rig pans between panels; balloons pop with a spring and hold whole Arabic phrases; ink outlines. Panels generated without text, bubbles drawn in code (ARAB-09). **أرقام / params:** keys 8–16 f.
- **الدليل / proof:** `kosif-tool/styles/comics-panels/SKILL.md` · `kosif-tool/styles/comics-panels/STYLE.json` · `kosif-atlas/skills/1094-akbun-draw/2423-akbun-draw-webtoon-b`

#### CHAR-49 · أنمي أكشن · Anime action · 🟢 جاهز / ready
- **ماذا / what:** أكشن مستوحى من الأنمي: خطوط سرعة، إطارات اصطدام، لطخات حركة. — Speed lines, impact frames and smears.
- **متى أستخدمها / when:** لحظات قتال أو انطلاق رياضي — fights, sports bursts.
- **كيف / how:** python3 tools/kosif.py scaffold anime-action <dir>; 2D rig + smear frames, speed-line overlays, camera shake; anticipation 4–8 frames, overshoot 5–10%; hold impact frames 2–3 frames with an inverted flash; original designs only. **أرقام / params:** anticipation 4–8 f; overshoot 5–10%.
- **الدليل / proof:** `kosif-tool/styles/anime-action/SKILL.md` · `kosif-tool/styles/anime-action/STYLE.json`

#### CHAR-50 · صفحات ويبتون بشخصيات حيوانية · Webtoon pages with Arabic overlay · 🔑 مفتاح أو خدمة / needs key
- **ماذا / what:** أوصاف شخصيات حيوانية ثابتة تُكرر حرفيًا في كل وصف، خلفية بيضاء، والحوار طبقة SVG قابلة للتحرير بعربية صحيحة. — Fixed animal character descriptions repeated verbatim, white background, dialogue as an editable SVG overlay.
- **متى أستخدمها / when:** قصص أطفال مصورة — illustrated kids' stories.
- **كيف / how:** art from an image model (needs a key) with no text; dialogue balloons and Arabic lettering drawn in SVG over the panels; animate panels with gentle push-ins and balloon pops.
- **الدليل / proof:** `kosif-atlas/skills/1094-akbun-draw/2423-akbun-draw-webtoon-b`

## توليفات قوية / power combos

- **قصة أطفال عربية / Arabic kids' story:** CHAR-40 + CHAR-36 + CHAR-29 + CHAR-35 + VOICE + ARAB-62 — أرنب قطيفة يتنفس ويرمش، يدخل من اليمين، يقفز فرحًا عند الكلمة المنبورة، والترجمة كاريوكي.
- **شرح بتميمة العلامة / brand mascot explainer:** CHAR-19 + CHAR-30 + CHAR-13 + EASE-30 + UI — تميمة بعينين لامعتين تشير إلى ثلاث بطاقات تقفز بعد توقف الإصبع، وفمها يتبع الصوت.
- **ستيكمان نصائح / stickman tips reel:** CHAR-17 + CHAR-11 + CHAR-12 + EASE-55 + DRAW-26 — أطراف IK، جذع مرن بالسرعة، بطاقة تطير لليد وتُرمى بأشباح.
- **مشهد ليلي سينمائي / cinematic night scene:** CHAR-26 + CHAR-38 + CHAR-25 + GLOW + PART (مطر) — قطة بآلة وضعيات تقفز البركة، فراشة متوهجة ترشدها.
- **فيلم المختبر / lab explainer:** CHAR-42 + CHAR-45 + 3D + CAM — أرنب وأسد بمفاصل مسماة، HUD يسمي الأجزاء، دوران 360 قبل الحركة.
- **رقص من فيديو حقيقي / particle dance:** CHAR-46 + BEAT + GLOW + PART — جسد من 1200 جسيم يرقص كالمؤدي ونبضه على الإيقاع.
- **سلسلة شخصية مولدة / generated character series:** CHAR-03 + CHAR-06 + CHAR-05 + GEN + ARAB-09 — قفل نصي وصور مرجعية، بلا نص داخل الصور، والعربية طبقة فوقها.

## أخطاء ممنوعة / never do

1. **لا شخصيات محمية بحقوق ولا تقليد شخصيات مشهورة** — تصاميم أصلية فقط، ورخّص أي شخصية Lottie جاهزة (CHAR-01/47).
2. **لا انزلاق للقدمين** — اشتق طور المشي من المسافة المقطوعة لا من الزمن وحده (CHAR-14/24).
3. **لا تشوّه مسار الفم والعينين** — بدّل أشكالًا جاهزة خلال إطار واحد، والفم مغلق على م/ب (CHAR-13).
4. **لا شخصية متجمدة** — تنفس 0.6–2%، رمش كل 2.5–4 ث، حتى في الثبات (CHAR-36).
5. **لا تراكم الفيزياء إطارًا بإطار في الرندر** — الانحناء من الفرق بين seek(t) وseek(t − 1/fps)، والنوابض بصيغة مغلقة (CHAR-12/37).
6. **لا نوابض أذن سريعة بلا قياس** — 2.2 هرتز بتخميد 0.28 تجاوز حد 80 بكسل/إطار؛ قِس السرعة (CHAR-37).
7. **لا تولّد شخصًا جديدًا حين يكون للمستخدم صورة** — عدّل صورته؛ التوليد الجديد يعطي شخصًا آخر (CHAR-06).
8. **لا تخلط إيقاع «على اثنين» مع حركة ناعمة على العنصر نفسه** — الشخصية متقطعة والواجهة ناعمة، كلٌّ في طبقته (CHAR-20).
9. **لا تُدخل الشخصية من اليسار في فيلم عربي بلا سبب** — اتجاه القراءة من اليمين (CHAR-35).
10. **لا تعرض أفاتارًا ناطقًا بالعربية دون فحص مزامنة الشفاه على لقطة** — الخدمات تتفاوت في العربية (CHAR-08).

## أقوى 5 حركات توقيع / 5 signature moves

1. **CHAR-26 — آلة حالات الوضعية:** مشي ← انحناء ← قفزة بقوس 147 بكسل ← هبوط ← نظرة — قصة حركية كاملة في 10 ث، مصورة هنا.
2. **CHAR-40 — الأرنب القطيفة:** تميمة ثلاثية الأبعاد بمفاصل مسماة جاهزة للتمثيل، مختبرة هنا.
3. **CHAR-36 — حياة الخمول:** تنفس ورمش ونظرة للكاميرا — ما يجعل أي شخصية حيّة.
4. **CHAR-11 — IK بعظمتين:** أطراف ترسم نفسها نحو أهداف في العالم — ستيكمان يمسك ويرمي ويركب دراجة.
5. **CHAR-29 — لحظة رد الفعل:** هبوط 4%، قفزة، ضغط 8% بنابض، متابعة — دهشة تُقرأ في ثانيتين.
