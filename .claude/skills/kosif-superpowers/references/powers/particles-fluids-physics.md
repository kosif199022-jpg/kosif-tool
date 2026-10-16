# الجسيمات والسوائل والفيزياء — Particles, fluids & physics

> **قوتك هنا:** آلاف النقاط التي تعني شيئًا — غبار يعطي الهواء عمقًا، شرر يقع على الضربة، مطر بطبقتين وبرك تتموج، قصاصات احتفال، سحابة تتجمع كلمةً عربية متصلة ثم تنفجر جمرًا، مجرات وكرات فيبوناتشي، ماء وبحر وسحب حجمية في 3D، وكرات ترتد بمعامل ارتداد حقيقي — وكلها دالة خالصة للزمن فيتطابق كل رندر.
> **أقوى دليل:** فيلم `proofs/particles-to-arabic` (6000 جسيم في حقل curl خالٍ من التباعد بتكامل RK2 مخزّن مسبقًا، تتجمع «إبداع» من اليمين ثم تنفجر بسحب مغلق الصيغة — 13/13)؛ ومختبر جسيمات رندرتُه هنا (2026-10-16، 90 إطارًا): `MOTION.rain/vapour/sparkle` من motion-kit، انفجار ببذرة وجاذبية، قصاصات تنقلب، خطوط حقل تدفق، كرة فيبوناتشي، قفزة فضائية، كرة ترتد بـ e=0.75، ومجرة ω∝1/r — وإطارات 3D من `night_boat` (بحر وقفزة سمكة بحلقات) و`midnight_cat` (مطر بطبقتين وبرك).
> **You can:** burst, rain, snow, dust, confetti, gather and dissolve words, flow fields, galaxies, water, clouds, fire, sparks and rigid-body-feeling drops — in Canvas, SVG/GSAP, three.js and Pillow. **75 powers follow** — ✅ 17 · 🟢 13 · 📦 13 · 🔑 1 · 👁 20 · 📄 10 · 💡 1.

**الحالة / status:** ✅ مُثبت هنا (كود + اختبار أو رندر في هذه الحاوية) · 🟢 جاهز (كود المالك يعمل بلا إضافات) · 📦 بأمر تثبيت · 🔑 مفتاح أو خدمة · 👁 شوهد في فيديو أنتجتَه (وصفة البناء مرفقة) · 📄 موصوف فقط · 💡 فكرة.
مسارات الدليل نسبية إلى `/home/user/`؛ `style:<id>` = فيديو مرجعي أنتجتَه سابقًا (ملاحظاته في `kosif-tool/styles/<id>/`).

**فحص سريع لهذه الحاوية (2026-10-16):** مختبر الجسيمات (Canvas + motion-kit + GSAP المضمّن) رُندر في وضع seek ✔ · مشاريع three-kit تُرندر إطاراتها عبر `window.seek` من motion-kit وWebGL SwiftShader ✔ (night_boat, midnight_cat) — لكن `render_html.cjs` في وضع virtual انتهت مهلته على صفحات WebGL · لم تُثبّت هنا: matter-js, cannon-es, @dimforge/rapier3d-compat, @tsparticles/engine, canvas-confetti, simplex-noise (كلها على npm) · Houdini وEmberGen غير متاحين.

## الفهرس / contents
- **قوانين الحتمية والمعنى — Determinism & meaning laws** — PART-01 … PART-05 (5)
- **الانفجارات والاحتفالات — Bursts & celebrations** — PART-06 … PART-14 (9)
- **تجمّع وتفكك الكلمات والأشكال — Gather & dissolve: words, icons, data** — PART-15 … PART-21 (7)
- **الحقول والتدفق والضوضاء — Flow fields, noise & trails** — PART-22 … PART-31 (10)
- **الأجواء: غبار ونجوم ومطر وثلج — Atmosphere: dust, stars, rain & snow** — PART-32 … PART-45 (14)
- **الفضاء والكرات الجسيمية — Space & 3D point clouds** — PART-46 … PART-52 (7)
- **النار والدخان والماء والطقس — Fire, smoke, water & weather** — PART-53 … PART-67 (15)
- **الفيزياء والأجسام — Physics & bodies** — PART-68 … PART-75 (8)
- توليفات قوية / power combos · أخطاء ممنوعة / never do · أقوى 5 حركات توقيع / 5 signature moves

## قوانين الحتمية والمعنى — Determinism & meaning laws

_جسيم بلا معنى ضوضاء، وجسيم بلا بذرة يكسر الرندر. هذه القواعد قبل أي انفجار._

#### PART-01 · ضجيج حتمي بالهاش وmulberry32 · Deterministic hash / seeded RNG · ✅ مُثبت هنا / proven here
- **ماذا / what:** استبدل Math.random بدالة هاش أو مولد ببذرة، فكل إطار يُرسم مطابقًا في كل رندر وبأي ترتيب. — Replace Math.random with an integer hash or a seeded PRNG so every frame renders identically, in any order.
- **متى أستخدمها / when:** كل نظام جسيمات أو نمط توليدي يُرندر إلى فيديو — بلا استثناء.
- **كيف / how:** rnd(i) = fract(sin(i·127.1 + 311.7)·43758.5453) for per-index values; KOSIF.rng(seed) = mulberry32 for sequences; motion-kit MOTION.rng(seed); flicker = hash(i, floor(t·10)). Everything in the lab and the proof films uses this (seed 20261016/20261015). **أرقام / params:** e.g. 200 points, brightness = hash(i, floor(t·10)).

```js
function mulberry32(a){return()=>{a|=0;a=a+0x6D2B79F5|0;
  let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;
  return((t^t>>>14)>>>0)/4294967296}}
const rnd = i => { const s = Math.sin(i*127.1+311.7)*43758.5453; return s - Math.floor(s); };
```

- **الدليل / proof:** `kosif-tool/starters/html-canvas/timeline.js:40` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cinematic-cat.html:9` · `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/particles-to-arabic/README.md`

#### PART-02 · الجسيم دالة للزمن لا حالة · Closed-form particles (state-free seek) · ✅ مُثبت هنا / proven here
- **ماذا / what:** موقع كل جسيم يُحسب من t مباشرة (بالستي، سحب مغلق، دوري)، أو تُخزّن خطوات المحاكاة مسبقًا ثم يُبحث فيها — فلا حالة تتراكم بين الإطارات. — Compute each particle from t (ballistic, closed-form drag, periodic wrap) or pre-bake simulation steps and look them up — no state carried between frames.
- **متى أستخدمها / when:** أي محاكاة تتطلب seek(t) دقيقًا (render_html.cjs, HyperFrames).
- **كيف / how:** Ballistic: p = p0 + v·τ + ½g·τ²; drag: p = p0 + v·(1 − e^(−kτ))/k; wrap: y = (y0 + v·t) mod H; stateful fields (curl advection) integrated once at 60 Hz with RK2 and stored, seek = linear interpolation between stored steps (particles-to-arabic). Bake Blender/Houdini sims to sequences — GLB does not carry them. **أرقام / params:** RK2 @ 60 Hz pre-baked; drag k 2.4/s.
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/proofs/particles-to-arabic/README.md` · `kosif-atlas/skills/1526-gamegen/4164-game-audio-vfx/SKILL.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/particle-burst.md`

#### PART-03 · الجسيم يعني شيئًا · Particle meaning rule · 📄 موصوف / documented only
- **ماذا / what:** الجسيمات تُظهر كمية→بنية أو طاقة أو تدفقًا أو تفككًا؛ احذف الغبار الزخرفي. في الفيديو التحليلي كل جسيم كيان أو عينة أو حامل اتجاه أو مؤشر تركيز. — Particles show quantity→structure, energy, flow or dissolution; remove decorative dust. In analytic video each particle is an entity, sample, direction carrier or focus cue.
- **متى أستخدمها / when:** قبل إضافة أي جسيمات، خصوصًا في البيانات.
- **كيف / how:** State the unit on screen or in VO; cap counts; sample instead of drawing every edge; pair with static width/labels for quantity; end on a static frame; avoid for aggregated or uncertain human harm.
- **الدليل / proof:** `kosif-tool/playbooks/particles.md:9` · `kosif-atlas/skills/2690-build-web-data-visualization/10332-threejs-data-visualization/references/particle-effects-and-flow.md`

#### PART-04 · ميزانية الأحجام والألوان والعدد · Size / colour / count budget · 📄 موصوف / documented only
- **ماذا / what:** ثلاثة أحجام 4/8/14px، لونان كحد أقصى، 150–600 جسيم في Canvas و≤ 20,000 في WebGL، خلف النص وبكثافة غير متساوية. — Sizes 4/8/14 px, ≤ 2 colours, 150–600 on Canvas 2D, ≤ 20,000 WebGL points, behind type, uneven density.
- **متى أستخدمها / when:** تصميم أي طبقة جسيمات.
- **كيف / how:** Burst speeds 400–1300 px/s, gravity 60–150 px/s², flow-field noise scale .0025; go GPU (instanced/FBO) beyond ~5k. **أرقام / params:** 4/8/14 px; 150–600 Canvas; ≤ 20k WebGL.
- **الدليل / proof:** `kosif-tool/playbooks/particles.md:15-18` · `kosif-tool/playbooks/particles.md`

#### PART-05 · المؤثر على إطار التلامس · Impact on the contact frame · 📄 موصوف / documented only
- **ماذا / what:** الانفجار والمؤثر الصوتي يقعان على إطار التلامس أو القمة الفعلي لا على بداية المقطع. — Bursts and hit SFX land on the actual contact/apex frame, not the clip start.
- **متى أستخدمها / when:** كل ضربة، هبوط، كسر، ركلة طبل.
- **كيف / how:** One event list drives both audio and particles (e.g. SOUND.kicks, makeSparks event times); respect reduced-motion and flashing limits.
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4164-game-audio-vfx`

## الانفجارات والاحتفالات — Bursts & celebrations

_الانفجار يخرج بـ expo.out ويسقط بجاذبية ويخبو بـ inOutCubic — والكلمة البطلة تدخل قبله بـ 250ms._

#### PART-06 · انفجار ببذرة وجاذبية · Seeded analytic burst · ✅ مُثبت هنا / proven here
- **ماذا / what:** 160 جسيمًا ببذرة ثابتة تنفجر من المركز بمسافة expo.out وتمايل وجاذبية خفيفة وتلاشٍ inOutCubic — دالة خالصة للزمن. — 160 seeded particles explode from the centre with expo.out distance, wobble, slight gravity and an inOutCubic fade — a pure function of t.
- **متى أستخدمها / when:** كشف كلمة، إنجاز، ضربة إيقاع، ختام.
- **كيف / how:** rng(20261015): angle, speed 400–1300 px (420–1320 in the starter), size 4–14, 70% #7ee8d2 / 30% #ffb86b; d = outExpo(life)·sp; alpha = 1 − inOutCubic(life); y += life·120; r shrinks 60%. Rendered here twice: the lab panel and the html-canvas starter itself (render_html.cjs, 7–10.5 s, burst + ring around «الفكرة»). **أرقام / params:** 160 parts; 400–1300 px/s; gravity 60–150 px/s²; life .7–1.0.
- **الدليل / proof:** `kosif-tool/starters/html-canvas/index.html:118` · `kosif-tool/playbooks/particles.md:52-66`

#### PART-07 · وصفة انفجار الكشف · Reveal-burst recipe · 📄 موصوف / documented only
- **ماذا / what:** الكلمة البطلة تكبر بنابض، ثم ينطلق 160 جسيمًا وحلقة تتسع وتخبو. — Hero word springs in, seeded particles burst, a ring expands and fades.
- **متى أستخدمها / when:** بطاقة عنوان، كشف رقم، كلمة مفتاحية.
- **كيف / how:** Word 0–250 ms spring (damping 14, stiffness 150); 160 particles 50–3000 ms; ring 100–1100 ms outExpo (SHAPE shockwave). **أرقام / params:** word 250 ms; ring 1 s outExpo.
- **الدليل / proof:** `kosif-tool/playbooks/particles.md:38-40`

#### PART-08 · قصاصات احتفال تنقلب · Confetti burst / rain with 3D flip · ✅ مُثبت هنا / proven here
- **ماذا / what:** مستطيلات صغيرة بألوان العلامة تنطلق للأعلى وتسقط بجاذبية وتتمايل وتنقلب (scaleY = cos). — Small brand-coloured rectangles launch up, fall with gravity, sway and flip in 3D (scaleY = cos).
- **متى أستخدمها / when:** نجاح، إطلاق، بطاقة نهاية، احتفال.
- **كيف / how:** Per piece: x = x0 + vx·t + sin(3t + ph)·20, y = y0 + vy·t + ½g·t², rotate spin·t, scale(1, cos(8t + ph)); 20–300 pieces, g 600–900 px/s², life 1–2.5 s. Rendered here (70 pieces, closed form). HyperFrames confetti component is the seeded drop-in. **أرقام / params:** 40–150 pcs; g 600–900 px/s²; sway 20 px; life 1.5–2.5 s.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/confetti/confetti.html` · `kosif-tool/styles/isometric` · `kosif-tool/styles/pm-deebeeeff-50fcd0`
- **أساليب / styles:** `style:isometric` · `style:pm-deebeeeff-50fcd0` · `style:pm-anilraok-eff262` · `style:pm-viktoroddy-98c1d8` · `style:pm-sudo-kiran-6609ed` · `style:pm-devius-maximus-beab45`

#### PART-09 · انفجارات HyperFrames الجاهزة · HyperFrames burst primitives (particle-burst, radial-burst-lines) · 📦 بأمر تثبيت / one install
- **ماذا / what:** انفجار جسيمات وانفجار خطوط سرعة شعاعية مثبتان على أحداث الموسيقى (drop / crash / surge)، وقاعدة انفجار حتمي ≤ 40 جسيمًا. — Particle explosion and radial speed-line bursts anchored to music events, plus the deterministic burst rule (≤ ~40 particles, closed-form gravity).
- **متى أستخدمها / when:** ريل موسيقي داخل HyperFrames.
- **كيف / how:** Copy music-to-video/references/motion-primitives/particle-burst/scene.html or radial-burst-lines/scene.html; anchor to audiomap events; best span .2–1.2 s / .2–.8 s. **أرقام / params:** ≤ ~40 particles; chips radius 2 px.
- **📦 تثبيت / install:** `npm i -D hyperframes`
- **⚖️ ترخيص / license:** Apache-2.0 (+ GSAP standard license).
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/particle-burst/scene.html` · `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/radial-burst-lines/scene.html` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/particle-burst.md`

#### PART-10 · شرطات وشرارات الاصطدام · Radial dash burst & impact spark lines · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** 80–150 شرطة قصيرة من المركز بسرعة متباطئة تدور مع اتجاهها وتخبو بثلاثة ألوان؛ أو 4–6 خطوط قصيرة عند نقطة الاصطدام. — 80–150 short segments from the centre, decelerating, rotated along velocity, fading in a 3-colour mix; or 4–6 short radial lines at an impact point.
- **متى أستخدمها / when:** ضربة، لكمة، فتح، انطلاق.
- **كيف / how:** White 70% / yellow 20% / red 10%; life 600–900 ms; impact lines life 200 ms at 200 px/s; tracer variant: bursts of 6–10 additive streaks at ~3000 u/s, life .3 s, #fff2d0. **أرقام / params:** 80–150 dashes, 600–900 ms; impact 4–6 lines, 200 ms.
- **الدليل / proof:** `kosif-tool/styles/pm-sudeepsd-1a3485` · `kosif-tool/styles/pm-kamstudiolabs-447565` · `kosif-tool/styles/pm-nft-chen-5f8bb0`
- **أساليب / styles:** `style:pm-sudeepsd-1a3485` · `style:pm-kamstudiolabs-447565` · `style:pm-nft-chen-5f8bb0`

#### PART-11 · تحطم إلى مربعات أو شظايا · Shatter to squares / shards / ring shards · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** الجسم يُستبدل بمربعات تحمل ألوانه وتُقذف على حلزون مع انحراف لوني، أو مثلثات تنفجر من نواة متوهجة، أو حلقة تتشظى أقواسًا. — Replace the object with coloured square particles flung on a spiral with RGB split, triangles exploding from a glowing core, or a ring splitting into arc shards.
- **متى أستخدمها / when:** تدمير، تحول، «كسر القاعدة».
- **كيف / how:** 300–600 squares, 600 ms, R/B offset 4–8 px + motion blur; shards 600 ms easeOutExpo with spin; ring: 24 shards 400–600 px/s fading 500 ms, or ~60 glowing dots sampled on the ring drifting 40–120 px/s for 2 s. **أرقام / params:** 300–600 squares; 24 ring shards.
- **الدليل / proof:** `kosif-tool/styles/pm-teslachartz-c58b32` · `kosif-tool/styles/pm-zaqailo-212ad3` · `kosif-tool/styles/pm-kantamk-61f410`
- **أساليب / styles:** `style:pm-teslachartz-c58b32` · `style:pm-zaqailo-212ad3` · `style:pm-kantamk-61f410`

#### PART-12 · انفجار سحابة صور أو بطاقات · Image-card burst cloud · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** ~120 بطاقة صور مستديرة تنطلق شعاعيًا بأعماق مختلفة وتبطؤ إلى سحابة طافية حول كبسولة نص. — ~120 rounded image cards fly radially at varied depth (scale .4–1.2), slowing to a drifting cloud around a caption pill.
- **متى أستخدمها / when:** «آلاف المستخدمين»، معرض، مجتمع.
- **كيف / how:** Burst 700 ms expo-out then drift 10 px/s; soft shadows; slight rotation; depth blur by scale. **أرقام / params:** ~120 cards; 700 ms; drift 10 px/s.
- **الدليل / proof:** `kosif-tool/styles/pm-rossaxbt-3085b7` · `kosif-tool/styles/pm-macrohou-33959d`
- **أساليب / styles:** `style:pm-rossaxbt-3085b7` · `style:pm-macrohou-33959d`

#### PART-13 · انفجار فتح إنجاز ونجوم ذهبية · Achievement unlock star burst · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** 80 نجمة ذهبية تنطلق شعاعيًا بجاذبية خفيفة وتخبو في 2 ث. — 80 gold star particles radial with light gravity, fading over 2 s.
- **متى أستخدمها / when:** ألعاب، شارات، مستويات.
- **كيف / how:** Gravity .05 per frame-unit, colours #e3b75a / #fff; star sprite 4-point sparkle. **أرقام / params:** 80 stars; fade 2 s.
- **الدليل / proof:** `kosif-tool/styles/pm-bthreeagency-b9b8d9`
- **أساليب / styles:** `style:pm-bthreeagency-b9b8d9`

#### PART-14 · مؤثرات بكسل بخطوات اللوحة · Pixel VFX by palette-step fades · 📄 موصوف / documented only
- **ماذا / what:** شرر وضربات وانفجارات وتعاويذ تكبر وتنفجر وتخبو بالنزول على سلم لوني من الساطع إلى الداكن، لا بالشفافية؛ أو تموت بفقد بكسل كل إطار. — Sparks, slashes, explosions and spells grow, burst and fade by stepping down a bright→dark ramp — never alpha; or die by losing 1 px per frame.
- **متى أستخدمها / when:** بكسل آرت وألعاب ريترو.
- **كيف / how:** Procedural draw(frame) in Pillow; hold the impact frame 2–3 frames; ramp 4–6 colours; shrink-to-die: 24 particles, 3–5 frame life. **أرقام / params:** ramp 4–6 colours; hold 2–3 frames.
- **الدليل / proof:** `kosif-atlas/skills/2460-pixel-art/9530-vfx` · `kosif-tool/styles/pm-0xevinho-3777d8/BRIEF.md`

## تجمّع وتفكك الكلمات والأشكال — Gather & dissolve: words, icons, data

_العربية تُؤخذ عيناتها من الكلمة المشكّلة كاملة — فتتجمع الجسيمات حروفًا متصلة لا حروفًا معزولة._

#### PART-15 · جسيمات تتجمع كلمة عربية · Particles gather into a shaped Arabic word · ✅ مُثبت هنا / proven here
- **ماذا / what:** 6000 جسيم تسبح في حقل curl ثم تنجذب من اليمين إلى نقاط مأخوذة من صورة الكلمة المشكّلة كاملة، فتبقى الحروف متصلة. — 6,000 particles swim in a curl field, then attract right-to-left to points sampled from the whole shaped word, so letters stay joined.
- **متى أستخدمها / when:** عنوان، شعار، كلمة مفتاحية في أغنية أو دعاء.
- **كيف / how:** Render the word once with the shaper on a hidden canvas, take alpha > 150 pixels on a 2 px step, Fisher–Yates shuffle with the seed; start_i = 2.2 + 1.1·(.72·(1−u) + .28·rand) s (u = x position, right first), duration 1.75 s inOutCubic, curved path ±.18–.50; then breathe, light sweep, and explode (drag k 2.4/s, buoyancy −46τ²). Proven in proofs/particles-to-arabic (13/13). **أرقام / params:** N 6000; seed 20261016; step 2 px; travel 1.75 s; shockwave 3200 px/s.
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/proofs/particles-to-arabic/README.md` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/particles-to-arabic/index.html` · `kosif-tool/playbooks/particles.md:27`
- **أساليب / styles:** `style:pm-grace-sunnyy-29bc61` · `style:pm-jasonzhou1993-8595e0` · `style:pm-ndhabarde11-f155b4` · `style:pm-topi-003-9ca6b5`

#### PART-16 · تفكك النص إلى جسيمات أو جمر · Text dissolve / disintegrate to embers · 📄 موصوف / documented only
- **ماذا / what:** بكسلات الكلمة تُستبدل بجسيمات تصعد وتخبو، أو تتحرر من اليسار لليمين بعتبة ضوضاء وتتحول من الأبيض إلى البرتقالي كجمر. — Word pixels become particles that drift up and fade, or are released by a sweeping noise threshold and turn white→orange like embers.
- **متى أستخدمها / when:** نهاية فكرة، «تلاشى»، انتقال.
- **كيف / how:** Arabic: sample the whole shaped word and keep it readable ≥ 1 s first; drift 200 px over 1.5 s; ember variant 20–60k points (GPU), release sweep 1.2 s (for Arabic sweep right→left), curl velocity, additive, life 2 s. HyperFrames particle-text-dissolve does in/out with one painter (no per-particle tweens). **أرقام / params:** drift 200 px / 1.5 s; hold ≥ 1 s; sweep 1.2 s.
- **الدليل / proof:** `kosif-tool/playbooks/particles.md:44` · `kosif-tool/playbooks/particles.md:72` · `kosif-one/vendor/hyperframes/registry/components/particle-text-dissolve/particle-text-dissolve.html`
- **أساليب / styles:** `style:pm-ajith-io-4c248f` · `style:pm-robvjourney-ce3e1a`

#### PART-17 · أيقونة أو شعار يتكون من سحابة نقاط · Icon / logo coalescing from a point cloud · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** نقاط تُؤخذ على مسار الأيقونة تبدأ مبعثرة في سحابة دمعية وتقفز بنابض إلى أهدافها، مع توهج نقطة البؤرة. — Points sampled along an icon path start scattered in a teardrop cloud and spring to their targets, with a glowing focal point.
- **متى أستخدمها / when:** كشف شعار، أمان (قفل)، علامة تجارية.
- **كيف / how:** 300–6000 points, spring stiffness 120 damping 18 (~600 ms), additive + bloom 1.5; X-glyph variant: 80–150 glyph particles scatter .6 s then converge .8 s and crossfade to the real logo; pixel-logo variant eases to bitmap grid cells over 1.5 s. **أرقام / params:** 300–6000 pts; spring 120/18; ~600 ms.
- **الدليل / proof:** `kosif-tool/styles/pm-bogdandragomir-35e024` · `kosif-tool/styles/pm-madhav-xo-f97f20` · `kosif-tool/styles/pm-robj3d3-b18fad`
- **أساليب / styles:** `style:pm-bogdandragomir-35e024` · `style:pm-madhav-xo-f97f20` · `style:pm-robj3d3-b18fad` · `style:pm-jayscambler-3f8889`

#### PART-18 · جسيمات تتحول إلى بيانات أو واجهة · Particles → chart / grid / UI · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** كل جسيم ينتقل إلى نقطة هدف (عناقيد، صناديق مدرج تكراري، خلايا شبكة) ثم تخبو النقاط وتظهر الواجهة مكانها. — Each particle lerps to a target set (clusters, histogram bins, snapped grid cells), then the dots fade while UI layers fade up.
- **متى أستخدمها / when:** «من الفوضى إلى البيانات»، عرض منتج تحليلي.
- **كيف / how:** Targets from chart geometry; 1.2 s easeInOut; grid pitch ~24 px, 600 ms easeInOutCubic stagger 0–300 ms by distance; prompt→particles→chart morph 700 ms (idea). **أرقام / params:** 1.2 s; grid 24 px; stagger ≤ 300 ms.
- **الدليل / proof:** `kosif-tool/styles/pm-ismailfahmi-557268` · `kosif-tool/styles/pm-bogdandragomir-35e024` · `kosif-tool/styles/pm-listudio-820c7b/BRIEF.md`
- **أساليب / styles:** `style:pm-ismailfahmi-557268` · `style:pm-bogdandragomir-35e024`

#### PART-19 · كشف صورة بالجسيمات · Particle image reveal (HyperFrames) · 📦 بأمر تثبيت / one install
- **ماذا / what:** حقل جسيمات ببذرة يتقارب بينما تنكشف صورة تحته، والآثار ترق حتى تصفو. — A seeded particle field converges while an image reveals beneath, trails thinning until clean.
- **متى أستخدمها / when:** كشف صورة منتج أو شخص.
- **كيف / how:** npx hyperframes add particle-image-reveal; density low|med|high; direction ltr|center (use center or mirror for Arabic layouts).
- **📦 تثبيت / install:** `npx hyperframes add particle-image-reveal`
- **⚖️ ترخيص / license:** Apache-2.0.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/particle-image-reveal/particle-image-reveal.html`

#### PART-20 · سحابة تتحول من حلقة إلى كرة · Point-cloud shape morph (torus ↔ sphere, helix → strands) · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** N نقطة لكل منها هدفان (سطح طارة وسطح كرة) تُستوفى مع خطوط قصيرة باتجاه السرعة وتدرج برتقالي→أزرق؛ أو لولب مزدوج يصير خيوطًا. — N points with two targets (torus surface, sphere surface) lerped with velocity streaks and an orange→blue ramp; or a double helix whose points become strands.
- **متى أستخدمها / when:** تحول مفاهيم، علوم، شعارات تقنية.
- **كيف / how:** N 5–10k, morph 1.5 s, slow y-rotation; pair targets by sorting both sets by (θ, φ) to avoid crossing chaos. **أرقام / params:** 5–10k pts; 1.5 s.
- **الدليل / proof:** `kosif-tool/styles/pm-tequilafunks-97f6c9` · `kosif-tool/styles/pm-madebyjmayala-b9204d`
- **أساليب / styles:** `style:pm-tequilafunks-97f6c9` · `style:pm-madebyjmayala-b9204d`

#### PART-21 · من فيديو إلى جسم جسيمي · Mocap: performer silhouette → particle body · 🟢 جاهز / ready
- **ماذا / what:** من فيديو بكاميرا ثابتة: خلفية وسيطة، فرق، تنظيف بالمورفولوجيا، ونقاط ثابتة لكل إطار تغذي جسمًا جسيميًا في three-kit. — From a fixed-camera video: median background, difference, morphology cleanup and a stable seeded point set per frame for a three-kit particle body.
- **متى أستخدمها / when:** راقص أو رياضي يتحول إلى غبار ضوئي.
- **كيف / how:** python motion.py mocap VIDEO --out body.json [--fps 30 --points 1200 --from 0 --dur D] → makeParticleBody. **أرقام / params:** 480 px; threshold 28; Gaussian 5×5; open/close 5×5; 30× candidates seed 7; coords 0–1000.
- **الدليل / proof:** `kosif-studio/motion/qa.py:598` · `100-superskills/skills/kosif-montage-motion/references/x-trend-2026.md`

## الحقول والتدفق والضوضاء — Flow fields, noise & trails

_curl يعطي حركة سائلة بلا تجمّع، وfbm يعطي غيمًا وتضاريس؛ والتدفق على المسار يحمل الاتجاه لا الكمية._

#### PART-22 · صندوق الضوضاء · Noise toolbox (Perlin / Simplex / curl / fBm / warp) · 📄 موصوف / documented only
- **ماذا / what:** Perlin للكتل، Simplex للتدرجات، curl لحركة سائلة بلا تباعد، fBm للغيم والتضاريس، وتشويه المجال (warp the warp) للتدفق الملتف. — Perlin for blobs, Simplex for gradients, curl for divergence-free fluid motion, fBm for clouds/terrain, domain warping for curling flow.
- **متى أستخدمها / when:** أي حركة عضوية.
- **كيف / how:** GLSL noise in shaders or JS (three-kit K3.fbm, simplex-noise); fBm 4–6 octaves; drive time uniform from frame/fps, never clock.elapsedTime. Analytic fallback: 3–4 summed prime-frequency sines scrolled .1–.3 units/s. **أرقام / params:** fBm 5 oct; freq 1.5; speed .5.
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md` · `kosif-tool/playbooks/code.md:28`

#### PART-23 · حقل curl تحليلي خالٍ من التباعد · Analytic curl field (stream-function) · ✅ مُثبت هنا / proven here
- **ماذا / what:** دالة تيار ψ من سبع موجات جيبية، والسرعة = (∂ψ/∂y, −∂ψ/∂x) بمشتقات تحليلية — جسيمات تدور ولا تتكدس. — A stream function ψ of 7 sine waves; velocity = (∂ψ/∂y, −∂ψ/∂x) with analytic derivatives — particles swirl and never clump.
- **متى أستخدمها / when:** سحب جسيمات سابحة، دخان، سائل ملون، سماء دوامية.
- **كيف / how:** Wavelengths 260–1020 px, speeds 38–84 px/s, +18 px/s updraft; integrate RK2 at 60 Hz and pre-store (see PART-02). Proven in proofs/particles-to-arabic. **أرقام / params:** 7 waves; λ 260–1020 px; RK2 60 Hz.
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/proofs/particles-to-arabic/README.md`
- **أساليب / styles:** `style:pm-mandelduck-95fd08`

#### PART-24 · خطوط حقل التدفق · Flow-field streak lines · ✅ مُثبت هنا / proven here
- **ماذا / what:** آلاف الجسيمات تتبع زاوية من ضوضاء تحليلية وتُرسم خطوطًا قصيرة بمزج جمعي — شعر أو ريح أو مغناطيس. — Particles follow an angle from analytic noise and are drawn as short additive streaks — hair, wind, magnetism.
- **متى أستخدمها / when:** خلفيات توليدية خلف العناوين، طاقة، ريح.
- **كيف / how:** angle = noise(x·.0025, y·.0025, t·.2)·2π, speed 40–120 px/s; draw 14-step polylines at alpha .25 with "lighter". Rendered here (500 seeds). Carpet variant: grid of 24×5 px segments rotated to noise(x,y,t)·2π (scale .004); backdrop at 15% opacity, .2 units/s behind titles. **أرقام / params:** noise scale .0025–.004; 40–120 px/s; alpha .1–.25.
- **الدليل / proof:** `kosif-tool/playbooks/particles.md:26` · `kosif-tool/playbooks/code.md:47` · `kosif-tool/styles/pm-ismailfahmi-557268`
- **أساليب / styles:** `style:pm-ismailfahmi-557268` · `style:pm-vanshwtfff-db0466` · `style:pm-rendesr-86be44`

#### PART-25 · سرير تدفق ولزوجة على الإيقاع · Beat-anchored flow-field bed & gooey metaball (HyperFrames) · 📦 بأمر تثبيت / one install
- **ماذا / what:** خلفية curl توليدية تمتد على المقطع كله، وحقل كرات لزجة على البناء والإسقاط. — A generative curl-noise background bed for the whole span, and a gooey metaball field anchored to build/drop.
- **متى أستخدمها / when:** فيديو موسيقي في HyperFrames.
- **كيف / how:** Copy motion-primitives/bg-flow-field/scene.html (best span 4–12 s) or gooey-metaball/scene.html (1.5–3 s); anchor to audiomap events.
- **📦 تثبيت / install:** `npm i -D hyperframes`
- **⚖️ ترخيص / license:** Apache-2.0.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/bg-flow-field/scene.html` · `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/gooey-metaball/scene.html`

#### PART-26 · تدفق الجسيمات على المسارات · Particle flow along routes & network edges · 📄 موصوف / documented only
- **ماذا / what:** نقاط تسافر على طرق أو أنابيب أو حواف شبكة لتظهر الاتجاه والنشاط بآثار تخبو. — Dots travelling along routes, pipes or network edges to show direction and activity, with fading trails.
- **متى أستخدمها / when:** لوجستيات، بيانات شبكية، أنابيب، دورة دموية.
- **كيف / how:** Precompute paths; each particle phase + speed; pos = pointAt((t·speed + phase) % 1); trail = last 8–20 samples with decaying opacity; never all edges at once — filter to the focus neighbourhood. Canvas for a few hundred, Pixi ParticleContainer/three Points for many. Playbook: 600 ms per traversal. **أرقام / params:** trail 8–20 samples; 600 ms per traversal.
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10332-threejs-data-visualization/references/particle-effects-and-flow.md` · `kosif-tool/playbooks/particles.md:46`
- **أساليب / styles:** `style:pm-sayan-shanky-f850d8`

#### PART-27 · طبقات التدفق في deck.gl · deck.gl flow layers (trips, arcs, hex) · 📦 بأمر تثبيت / one install
- **ماذا / what:** طبقات GPU لحركة على الخرائط: رحلات بآثار تخبو، أقواس منشأ-وجهة، مسارات، وتجميع سداسي. — GPU map layers: timestamped trips with fading trails, OD arcs, paths, hex aggregation.
- **متى أستخدمها / when:** تدفقات جغرافية كبيرة (MAP).
- **كيف / how:** TripsLayer currentTime = frame time; ArcLayer (state geodesic vs schematic); HexagonLayer for density; over MapLibre.
- **📦 تثبيت / install:** `npm i deck.gl maplibre-gl`
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/references/deckgl-d3-geo-stack-selection.md`

#### PART-28 · حقل حراري يُلطخ بالإصبع · Thermal finger-trail smear field · 📄 موصوف / documented only
- **ماذا / what:** كتلة حرارية من ضوضاء مشوهة المجال عبر سلم حراري بسبع وقفات، وأثر مؤشر يسحبها كطلاء مبلل ثم تلتئم، وضغطة ترسل حلقة. — A heat-camera blob of domain-warped noise through a seven-stop ramp; a pointer trail drags it like wet paint and heals; a press sends a ripple ring.
- **متى أستخدمها / when:** عرض تفاعل، تقنية حيوية، خلفيات «حرارة».
- **كيف / how:** Single WebGL1 fragment shader; 24 trail points (pos, velocity, age; life 1.6 s) as uniforms; disp += vel·smoothstep(r,0,d)·age; uv += disp·9. In video, script the finger as a Catmull-Rom path. Atlas reference HTML (needs a CDN panel) not rendered here. **أرقام / params:** fbm 5 oct; ramp 0/.12/.30/.45/.60/.78/1; smudge 9 (>14 tears); radius .17; ripple .18, bloom .55, .9 s.
- **الدليل / proof:** `kosif-atlas/skills/100-ui-motion/211-thermal-finger-trail/SKILL.md` · `kosif-atlas/skills/100-ui-motion/211-thermal-finger-trail/references/thermal-finger-trail.html`

#### PART-29 · شبكة نقاط تتأثر بجاذب · Dot-grid displacement around an attractor · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** شبكة نقاط تُزاح بعيدًا عن جسم متحرك وتتلون بالمسافة، وسلسلة كرات تتبع القائد بتأخر. — Grid dots pushed away from a moving attractor and tinted by distance; a chain of balls follows the leader with lag.
- **متى أستخدمها / when:** تفاعل مؤشر مكتوب مسبقًا، فيزياء مرحة.
- **كيف / how:** grid 24–28 px, falloff radius 160–200 px, spring back to rest; chain 15 balls lagging 2 frames each; inverse-square attraction (clamped) for hero pulls. **أرقام / params:** grid 24–28 px; radius 160–200 px; chain lag 2 frames.
- **الدليل / proof:** `kosif-tool/styles/pm-chatgptastra-0d95c7` · `kosif-tool/styles/pm-himanshutwtxs-5f4b43` · `kosif-tool/playbooks/particles.md:28` · `kosif-atlas/skills/342-kernel/1223-frontend/motion/cursor-field.md`
- **أساليب / styles:** `style:pm-chatgptastra-0d95c7` · `style:pm-himanshutwtxs-5f4b43`

#### PART-30 · حزم موجات وشرائط خطوط · Noisy multi-trace waveform & line-ribbon waves · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** 15 خطًا عبر العرض = مجموع 3 جيوب + ضوضاء بمزج جمعي؛ أو 100–200 منحنى رفيع بتدرج برتقالي→أرجواني→أزرق. — 15 polylines = sum of 3 sines + simplex noise, additive; or 100–200 thin sine curves with an orange→magenta→blue gradient.
- **متى أستخدمها / when:** صوت، بيانات، خلفيات تقنية.
- **كيف / how:** Trace: amp 20–60 px, 200 points, alpha .25; ribbons: lineWidth .6, alpha .3, 3–4 bands; parallax wave layers 1 : .6 : .3, amp 10–30 px. **أرقام / params:** 15 traces; 100–200 ribbons.
- **الدليل / proof:** `kosif-tool/styles/pm-rneayan-ea6129` · `kosif-tool/styles/pm-jasonzhou1993-8595e0` · `kosif-tool/styles/pm-faroukzy-9ff23e`
- **أساليب / styles:** `style:pm-rneayan-ea6129` · `style:pm-jasonzhou1993-8595e0` · `style:pm-faroukzy-9ff23e`

#### PART-31 · آثار الحركة والضوء · Motion trails from time-sampled history · 🟢 جاهز / ready
- **ماذا / what:** كل متحرك يُرسم K مرة في أزمنة أسبق بحجم وشفافية متناقصين؛ أو ذيل مدبب يقل عرضه نحو الطرف. — Each mover is drawn K times at slightly earlier times with shrinking size and alpha; or a tapered tail whose width falls toward the end.
- **متى أستخدمها / when:** درونات، سيارات طائرة، مذنبات، كرة ترتد.
- **كيف / how:** for k < K: position at t − k·dt; head size 3.4–4.2, tail 2.2–2.6·(1 − k/K), alpha .55–.7·(1 − k/K); egypt-2120: 36 drones × 16 samples (dt .045), 9 lanes × 30 taxis × 14 (dt .03); tapered trail ~.3 s, width 6→0 px; ribbons: last 60 wingtip positions, alpha .8→0. **أرقام / params:** K 12–16; dt .03–.045 s.
- **الدليل / proof:** `kosif-one/projects/egypt-2120-animation/index.html`
- **أساليب / styles:** `style:pm-kantamk-61f410` · `style:pm-nft-chen-5f8bb0`

## الأجواء: غبار ونجوم ومطر وثلج — Atmosphere: dust, stars, rain & snow

_الهواء يحتاج طبقتين: بعيدة كثيفة بطيئة، وقريبة قليلة سريعة — هكذا يُصنع العمق بجسيمات._

#### PART-32 · مطر motion-kit · MOTION.rain (seeded SVG/DOM rain) · ✅ مُثبت هنا / proven here
- **ماذا / what:** خطوط مطر مائلة ببذرة بطول وعرض وسرعة لكل قطرة، تظهر وتخبو مع الحاوية. — Seeded slanted rain streaks (SVG lines or divs) with per-drop length/width/speed and container fades.
- **متى أستخدمها / when:** أي مشهد ممطر ثنائي الأبعاد.
- **كيف / how:** MOTION.rain(tl, container, {n, x0..y1, fall, len, angle, color, at, dur, seed}). Rendered here. Gotcha found here: each drop starts at at − dur + delay, so use at ≥ fall (~.6 s) or the first drops sit above the frame. **أرقام / params:** n 240; fall .55 s; len 46 px (×.6–1.4); width 1–2.6 px; angle −8°; rgba(220,235,255,.75); fade .6/.8 s.
- **⚖️ ترخيص / license:** GSAP standard no-charge license (vendored).
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:265` · `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:265`

#### PART-33 · بخار motion-kit · MOTION.vapour (steam puffs) · ✅ مُثبت هنا / proven here
- **ماذا / what:** دوائر ببذرة تصعد وتكبر وتنجرف وتخبو كبخار أو دخان أو نفَس. — Seeded circles that rise, grow, drift and fade like steam, smoke or breath.
- **متى أستخدمها / when:** قهوة، تبخر في شرح، دخان خفيف.
- **كيف / how:** MOTION.vapour(tl, svgGroup, {n, r, rise, height, drift, spread, color, at, dur, x0, x1, y0, seed}); rendered here over #2b3a55. Wisp variant: 9-point polylines x + 14 sin(y/60 + 5t + x) rising 420 px, opacity sin(πp)·.9; coffee curls: 3 thin bezier strokes rising 40 px/s fading .4→0, loop 3 s. **أرقام / params:** n 70; r 18 px; rise 2.6 s; height 320 px; drift 120 px; scale .5→1.4.
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:283` · `kosif-one/projects/water-cycle-animation/index.html`
- **أساليب / styles:** `style:pm-itsolelehmann-e47532`

#### PART-34 · تلألؤ ونجوم · MOTION.sparkle & star twinkle · ✅ مُثبت هنا / proven here
- **ماذا / what:** نقاط ببذرة تتلألأ (شفافية ذهاب وإياب) عبر منطقة: نجوم، غبار، سحر. — Seeded dots twinkling (yoyo opacity) across a region: stars, dust, magic.
- **متى أستخدمها / when:** سماء ليلية، لمسة سحرية، خلفيات أدعية.
- **كيف / how:** MOTION.sparkle(tl, group, {n, x0..y1, color, at, seed}); rendered here (#ffe9b8). Canvas variant: alpha = .5 + .5 sin(t·(3 + .2f) + f), cross sparkles for the brightest, washed out near the moon. **أرقام / params:** n 40; r 1–3.2 px; opacity .15↔1 over .6–1.8 s; 40 repeats; sine.inOut.
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:300` · `100-superskills/skills/kosif-montage-motion/scripts/projects/five_sec/index.html:66`
- **أساليب / styles:** `style:pm-hoyoyoda-3a5c08`

#### PART-35 · غبار طافٍ وحقل عمق · Drifting dust motes & depth field · ✅ مُثبت هنا / proven here
- **ماذا / what:** نقاط صغيرة مضيئة تنجرف وتتمايل بسرعات وشفافيات متفاوتة — تعطي الهواء جسمًا خلف الواجهات والنصوص. — Small luminous dots drifting and bobbing at staggered speeds/opacities — body for the air behind UI and text.
- **متى أستخدمها / when:** كل خلفية «فارغة»، دعاء، تقديم هادئ.
- **كيف / how:** Proof: 110 dust motes in proofs/arabic-voice-kinetic. Recipes: studio 38 motes x = (137.3i + t·(5 + i%3)) mod w, y = (sin(2.71i + .18t)·.42 + .5)·h; fastify 26 golden-ratio dots (k·.618 mod 1) ±15/±20 px; depth: 40–80 dots, size 2–6 px, 5–15 px/s, varied blur; over footage: warm radial dots screen-blended, rising and fading in 1.6 s. **أرقام / params:** 26–110 motes; 5–15 px/s; alpha .07–.48.
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/proofs/arabic-voice-kinetic/README.md` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:69` · `fastify-motion-bro/web/motion.js:11` · `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:157`
- **أساليب / styles:** `style:pm-ceowinkz-7c776b`

#### PART-36 · أنظمة Basma الخمسة · Basma particle overlays (dust, bokeh, sparks, snow, confetti) · 📦 بأمر تثبيت / one install
- **ماذا / what:** طبقات جسيمات حتمية في محرر Basma كدالة للزمن: غبار صاعد، بوكيه، شرر، ثلج، قصاصات. — Deterministic overlays in the Basma editor: rising dust, bokeh, sparks, snow, confetti — pure functions of time.
- **متى أستخدمها / when:** ريلز سريعة داخل محرر Basma.
- **كيف / how:** drawParticles(): dust 54 dots rising 1.8%/s twinkle .18–.48; bokeh 16 screen discs 3–10% m alpha .08–.15; sparks 54 accent dots rising 12%/s "lighter"; snow 54 falling 6%/s; confetti 46 flips falling 16%/s; rnd(i) = frac(sin(127.1i + 311.7)·43758.5453). **أرقام / params:** dust|bokeh|sparks|confetti|snow.
- **📦 تثبيت / install:** `cd app && npm install`
- **الدليل / proof:** `app/public/js/00_editor.js:234`

#### PART-37 · مطر بطبقتين وبرك ورذاذ · Two-layer parallax rain, puddle ripples & splashes · ✅ مُثبت هنا / proven here
- **ماذا / what:** مطر بعيد رفيع كثير بطيء، وقريب سميك قليل سريع بإزاحة بارالاكس، وحلقات برك إهليلجية ورذاذ بالستي عند كل خطوة. — Far rain (many, thin, slow) and near rain (few, thick, fast) with parallax; elliptical puddle ripples and ballistic splash droplets at each footfall.
- **متى أستخدمها / when:** مشاهد ليلية ممطرة، شخصيات تمشي في المطر.
- **كيف / how:** far 152 drops 340–600 px/s, 11–25 px, #86b7c9 .8 px α .13, parallax .03; near 32 drops 630 px/s 37 px #95d6df 1.3 px α .17 parallax .1; wrap 1450×850; 20 ripples rx 5→29 ry 1→5; 11 droplets/event vx ±105, vy −45…−129, g 145 px/s², life .63 s. midnight_cat frame rendered here via window.seek; proofs/neon-glow adds 90 streaks + puddle rings. **أرقام / params:** 152 + 32 drops; 11 droplets × .63 s.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/assets/scene.js:108` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/examples/cinematic-cat.html:108` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/neon-glow/README.md`
- **أساليب / styles:** `style:pm-faroukzy-9ff23e` · `style:pm-kamstudiolabs-0b0824`

#### PART-38 · مطر الرسام بطبقات وضوء نار · Painted rain with exposure smear (Studio) · 🟢 جاهز / ready
- **ماذا / what:** خطوط مائلة بطبقتي عمق وطبقة دافئة مضاءة بالنار ثم تمويه حركي اتجاهي. — Slanted strokes in two depth layers, a warm fire-lit layer, then directional motion blur.
- **متى أستخدمها / when:** لوحات ثابتة/مرسومة بـ render.py.
- **كيف / how:** rain(seed, n, x0, x1, y0, y1, length, width, slant=−.25) → stroke(); colours #a8bbd4/.15, #cddcef/.2, fire-lit #ffb066 add; then motion_blur. **أرقام / params:** 520 + 150 + 160 streaks; lengths 24/60/36.
- **الدليل / proof:** `kosif-studio/scenes/whale_dragon.py:55` · `kosif-studio/scenes/duck_dragon.py:24`

#### PART-39 · مطر وضباب ومطر الغيمة · Rain + fog bands; cloud rain with splash rings · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** 300–500 خط مطر مائل 10–15° مع 2–3 أشرطة ضباب مموهة تنجرف؛ أو شرطات زرقاء تسقط من بصمة الغيمة وتولد حلقات عند الأرض. — 300–500 streaks at 10–15° with 2–3 blurred fog bands drifting; or blue dashes falling from a cloud footprint spawning ground rings.
- **متى أستخدمها / when:** جو ضبابي، شرح دورة الماء، دودل.
- **كيف / how:** Streak alpha .25–.4, length 12–24 px; doodle: 40–60 streaks, fall 600–900 ms, ring 300 ms; loop 38 drops at 950 px/s below the cloud base (water-cycle). **أرقام / params:** 300–500 streaks; fog 2–3 bands.
- **الدليل / proof:** `kosif-tool/styles/pm-kamstudiolabs-0b0824` · `kosif-tool/styles/doodle` · `kosif-one/projects/water-cycle-animation/index.html`
- **أساليب / styles:** `style:pm-kamstudiolabs-0b0824` · `style:doodle`

#### PART-40 · جسيمات موسمية وبتلات · Seasonal particles & falling petals · 🟢 جاهز / ready
- **ماذا / what:** بتلات وأوراق وثلج تنجرف قطريًا مع الريح؛ وبتلات ورد تسقط وتتمايل وتدور كدالة للزمن وحده. — Blossoms, leaves and snow drifting diagonally with the wind; rose petals falling, swaying and spinning as a function of t alone.
- **متى أستخدمها / when:** مواسم، أعراس، أدعية، ربيع.
- **كيف / how:** 22 petals from M.rng(11): period 7–12 s, y = −60 + 2050·((t/dur + ph) % 1), x += drift·u (±170) + sin(1.3t + 9ph)·(20–50), rotate ±300–700°·u, #e8436a/#f27b93 .9; seasonal: 60–150 particles, vx −100…−300 px/s, sway 10 px; chalk dust: dots from the drawing tip fall with g ~400 px/s² fading .5 s. **أرقام / params:** 22 petals; 7–12 s periods.
- **الدليل / proof:** `kosif-one/projects/thursday-dua-animation/source/index.html`
- **أساليب / styles:** `style:pm-itsolelehmann-e47532` · `style:chalkboard`

#### PART-41 · ثلج وحقل نجوم HyperFrames · HyperFrames snow & starfield blocks · 📦 بأمر تثبيت / one install
- **ماذا / what:** ثلج آمن للبحث بحجم وسرعة وشفافية مترابطة للعمق وقناع يبقي المركز صافيًا؛ وسماء بثلاث طبقات أحجام تتلألأ في طبقتي بارالاكس. — Seek-safe snow with size/speed/opacity correlated for depth and a radial mask keeping the centre clear; a night sky with three size tiers twinkling in two parallax layers.
- **متى أستخدمها / when:** خلفيات جاهزة خلف عنوان.
- **كيف / how:** npx hyperframes add snow (density sparse|dense, speed calm|gust, 6 s) | starfield (tone warm|cool|white, speed slow|fast).
- **📦 تثبيت / install:** `npx hyperframes add snow`
- **⚖️ ترخيص / license:** Apache-2.0.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/snow/snow.html` · `kosif-one/vendor/hyperframes/registry/blocks/starfield/starfield.html`

#### PART-42 · ثلج وجمر على المعالج الرسومي · GPU snow / ember point sprites · 🟢 جاهز / ready
- **ماذا / what:** نقاط تسقط وتتمايل وتخبو مع العمق بمزج جمعي — ثلج للأزرق وجمر دافئ للبني. — Point sprites that fall, sway and fade with depth, additively blended — snow for cobalt, embers for ledger.
- **متى أستخدمها / when:** خلفيات WebGL للهوية، شتاء، دفء.
- **كيف / how:** Vertex: y = mod(y − t·(.25 + .15 size), 16) − 8; x += .25 sin(.6t + 3.1z + 7 size); pointSize = (1.5 + 3.5 size)·dpr·clamp(10/d, .2, 2.5); alpha clamp(1.2 − d/22, .05, .8); fragment round sprite, smoothstep; blend ONE,ONE, depthMask false. Pass t from the frame. **أرقام / params:** 160 (phone) / 360 (desktop); field 24×16×(2..20).
- **الدليل / proof:** `kosif-earth-ci-fork/ui/art/crystal-world.js:65` · `kosif-earth-ci-fork/ui/art/crystal-world.js:149`

#### PART-43 · ذرات صاعدة وحلقات الركلة · Rising motes + kick rings (verse) · 🟢 جاهز / ready
- **ماذا / what:** 72 ذرة ضوء تصعد وتتلألأ وترتفع مع البدايات الصوتية، وكل ركلة طبل ترسل حلقة تتسع 1.3 ث. — 72 light motes rise and twinkle, lifted by onsets; each kick sends an expanding ring for 1.3 s.
- **متى أستخدمها / when:** أفلام الأغاني والشعر من الصوت.
- **كيف / how:** verse.html draw(t) with SOUND.kicks; "lighter"; motes r 2–9 px, speed .006–.026/s; ring radius (.16 + .42·dt)·min(W,H), alpha .22·(1 − dt/1.3)². Audio-driven variant proven in proofs/audio-reactive-spectrum (90 seeded particles, onset shockwaves .7 s). **أرقام / params:** 72 motes; ring 1.3 s.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/templates/verse.html:153` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/audio-reactive-spectrum/README.md`

#### PART-44 · هالة شعاعية وجسيمات صاعدة · Radial aura + drifting particle canvas · 🟢 جاهز / ready
- **ماذا / what:** خلفية Canvas بتوهج شعاعي كهرماني/سماوي وعشرات النقاط تصعد وتلتف. — A Canvas background with a soft amber/sky radial glow and dozens of dots drifting upward and wrapping.
- **متى أستخدمها / when:** قوالب حركية ثنائية سريعة (omni).
- **كيف / how:** createRadialGradient(W/2,H/2,50,W/2,H/2,.7W) amber .15 / sky .08 / transparent; 60 particles y = (y0 − 40·speed·t) mod H at alpha .4; seed the RNG (mulberry32) — the template uses Math.random as shipped. **أرقام / params:** 60 particles r 2–6 px, 40–120 px/s, #f59e0b / #38bdf8.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/kinetic_2d.html:128`

#### PART-45 · خلفيات هادئة حلقية · Ambient background loops (MG-111/113/114) · 📄 موصوف / documented only
- **ماذا / what:** كتلتان مموهتان تتباعدان وتعودان، ثلاثة خطوط موجية خلف عنوان بودكاست، وذرات ضوء تنجرف بأعماق مختلفة. — Two blurred blobs drift apart and back; three wavy lines behind a podcast title; light specks drifting at varied depth.
- **متى أستخدمها / when:** خلفيات حلقية للبودكاست والتنبيهات.
- **كيف / how:** 8 s / 8 s / 10 s loops; every speck cycle must divide the loop length; t mod period; tiny dither noise against banding; test gradients for banding after compression. **أرقام / params:** 8 / 8 / 10 s.
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-loops-backgrounds.md`

## الفضاء والكرات الجسيمية — Space & 3D point clouds

_الكرة من نقاط فيبوناتشي، والمجرة سرعتها ∝ 1/r، والقفزة الفضائية خط من الإسقاط السابق إلى الحالي._

#### PART-46 · كرة جسيمات فيبوناتشي · Fibonacci particle sphere · ✅ مُثبت هنا / proven here
- **ماذا / what:** N نقطة بالزاوية الذهبية على كرة، تدور وتُسقط بمنظور وتُرتب بالعمق، حجمها وشفافيتها بالعمق، وبعضها نقاط لهجة حمراء. — N golden-angle points on a sphere, rotated, perspective-projected, depth-sorted, size/alpha by z, a few red accent points.
- **متى أستخدمها / when:** «عالمي»، ذكاء اصطناعي، شبكة لغات، كوكب.
- **كيف / how:** y = 1 − 2(i+.5)/N, r = √(1−y²), θ = 2.39996·i; rotate in y; f = 2.6/(3.2 − z); alpha .25 + .6·(z+1)/2. Rendered here (900 points). Gather/collapse: radius 0→R ease-out 1.5 s, R→0 ease-in .6 s into an origin dot; chips can pop at projected points. **أرقام / params:** N 600–3000; FOV ~42°; alpha by depth.
- **الدليل / proof:** `kosif-tool/styles/pm-ayushunleashed-ece3e3` · `kosif-tool/styles/pm-kloss-xyz-b9b3f6` · `kosif-tool/styles/pm-crazyalphaaa-bc7e75`
- **أساليب / styles:** `style:pm-ayushunleashed-ece3e3` · `style:pm-kloss-xyz-b9b3f6` · `style:pm-crazyalphaaa-bc7e75` · `style:pm-zaqailo-212ad3` · `style:pm-sudo-kiran-6609ed` · `style:pm-motiondsgnr-9dcfa6`

#### PART-47 · مجرة حلزونية · Spiral galaxy (differential rotation) · ✅ مُثبت هنا / proven here
- **ماذا / what:** نقاط على أذرع حلزونية لوغاريتمية ملونة حسب الذراع، تدور بسرعة زاوية ∝ 1/r فيلتف الداخل أسرع. — Points on log-spiral arms coloured by arm, rotating with angular speed ∝ 1/r so the core winds faster.
- **متى أستخدمها / when:** فضاء، ختام، «كون من الأفكار».
- **كيف / how:** arm = i % 3, d = rand^.6, a = arm·2.094 + 4d + jitter; angle += t·.9/(d + .15); y squashed .55; additive. Rendered here (2500 points). HyperFrames spiral-galaxy: 20,000 GPU sprites, 3 arms, rate .25, glow 1.9, core #ffa575, rim #311599. **أرقام / params:** 2.5k–20k points; 2–3 arms; ω ∝ 1/r.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/spiral-galaxy/spiral-galaxy.html` · `kosif-tool/styles/pm-shneural-2abdfa` · `kosif-tool/styles/pm-tolgayhickiran-e90799`
- **أساليب / styles:** `style:pm-shneural-2abdfa` · `style:pm-tolgayhickiran-e90799` · `style:pm-kloss-xyz-fe0c31` · `style:pm-sudiyasa-f48ac9`

#### PART-48 · قفزة فضائية وخطوط سرعة · Hyperspace warp starfield · ✅ مُثبت هنا / proven here
- **ماذا / what:** ~600 نقطة بعمق z تُسقط x/z وy/z ويُرسم خط من الموضع السابق للحالي، والسرعة تقفز على الإسقاط الموسيقي. — ~600 points with depth; project x/z, y/z and draw a line from the previous to the current projection; speed ramps up on drops.
- **متى أستخدمها / when:** انتقال «انطلاق»، سرعة، فضاء، ذروة موسيقية.
- **كيف / how:** Speed 2→30 units/frame; stroke 1 px #9db4ff α .6 (cap line width ~2.5 px); rendered here. Tunnel variant: 3000 points on a cylinder moving to camera as streaks with a dark centre; warp-star transition between scenes .8 s, streak 50–200 px. **أرقام / params:** ~600 stars; speed 2→30.
- **الدليل / proof:** `kosif-tool/styles/pm-maxalexweber-67688b` · `kosif-tool/styles/pm-leonkohli-6dc01b` · `kosif-tool/styles/pm-nolkeeg-bf062e`
- **أساليب / styles:** `style:pm-maxalexweber-67688b` · `style:pm-leonkohli-6dc01b` · `style:pm-nolkeeg-bf062e` · `style:pm-apoorvjain25-d24184` · `style:pm-lukasersil-0ed38e`

#### PART-49 · حلقة جسيمات وكوكبة · Particle torus & constellation · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** نقاط على سطح طارة تدور على محورين بشفافية بالعمق؛ أو نجوم عشوائية تتصل خطوطها بالأقرب تحت هالة بنفسجية. — Points on a torus rotating on two axes with depth alpha; or random stars linked to near neighbours under a violet haze.
- **متى أستخدمها / when:** تقنية، شبكات، فواصل.
- **كيف / how:** Torus R 1, r .35, 2000 points, red accent subset; constellation: connect pairs with d < 90 px, line alpha ∝ 1 − d/90. **أرقام / params:** 2000 pts; link < 90 px.
- **الدليل / proof:** `kosif-tool/styles/pm-roundtablespace-d3a1be` · `kosif-tool/styles/pm-codestackr-c071bf` · `kosif-tool/styles/pm-dale-vaz-cc612a`
- **أساليب / styles:** `style:pm-roundtablespace-d3a1be` · `style:pm-codestackr-c071bf` · `style:pm-dale-vaz-cc612a`

#### PART-50 · نقاط مضيئة ثلاثية جمعية · Additive glowing point sprites (three.js) · 🟢 جاهز / ready
- **ماذا / what:** مئات النقاط المضيئة في حجم تدور ببطء حول البطل، بتلاشٍ ناعم من gl_PointCoord. — Hundreds of glowing points scattered in a volume, slowly rotating around the hero, with a gl_PointCoord falloff.
- **متى أستخدمها / when:** عمق وبريق حول منتج أو شعار ثلاثي.
- **كيف / how:** cinematic_3d: 400 positions in a 20×25×20 box; PointsMaterial #38bdf8 size .08 opacity .75 AdditiveBlending; rotation.y = .08t. Shader version: s = pow(1 − distance(gl_PointCoord, .5), 3), depthWrite false, 5000 points ±2. **أرقام / params:** 400–5000 points; falloff power 3.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/cinematic_3d.html:165` · `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### PART-51 · جسيمات GPU بمئة ألف · GPU particles: FBO ping-pong & TSL compute (100k+) · 📦 بأمر تثبيت / one install
- **ماذا / what:** خزّن مواقع الجسيمات في خامة عائمة وحدّثها في تمريرة محاكاة (FBO)، أو بمخازن حوسبة في WebGPU TSL — لمئة ألف جسيم وأكثر. — Store positions in a float texture updated in a simulation pass (FBO ping-pong), or in WebGPU TSL storage buffers — 100k+ particles.
- **متى أستخدمها / when:** سحب كثيفة، نص من 60 ألف نقطة، مجرات.
- **كيف / how:** DataTexture RGBA float → SimulationMaterial → WebGLRenderTarget (two, ping-pong) → points read uPositions; TSL: instancedArray(N,"vec3"), Fn(…)().compute(N), renderer.compute(update). Seed initial positions; for video advance exactly one step per frame. WebGPU unverified here — FBO on WebGL is the safe path. **أرقام / params:** N 100k; gravity −9.8, bounce .7, friction .98.
- **📦 تثبيت / install:** `npm i three`
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md` · `kosif-atlas/skills/2221-webgpu-threejs-tsl/8405-webgpu-threejs-tsl/examples/particle-system.js`

#### PART-52 · دوامة وشفط وشظايا طافية · Particle vortex, suck-in & floating shards · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** 3000 نقطة على حلزون زاويتها تزيد k/r، أو بطاقات تلتف نحو البطل وهي تصغر، أو شظايا نيون تطفو وتدور في المقدمة. — 3k points on a spiral with angle += k/r; cards spiralling into the hero while shrinking; neon shards drifting and spinning in the foreground.
- **متى أستخدمها / when:** جذب، «كل شيء يصب في…»، عمق.
- **كيف / how:** Suck-in 300–500 ms easeInCubic, rotation 90–180°, radial scribble lines; shards ~40 instanced, .5 rad/s, size for depth of field. **أرقام / params:** 3k pts; suck 300–500 ms; 40 shards.
- **الدليل / proof:** `kosif-tool/styles/pm-3xtihor-0f6911` · `kosif-tool/styles/pm-ik-builds-b8bdcf` · `kosif-tool/styles/pm-gorden-sun-041f56`
- **أساليب / styles:** `style:pm-3xtihor-0f6911` · `style:pm-ik-builds-b8bdcf` · `style:pm-gorden-sun-041f56`

## النار والدخان والماء والطقس — Fire, smoke, water & weather

_النار طبقات جمع من الأحمر للأبيض، والدخان عناقيد مموهة، والماء انعكاس فرينل ولمعة — كلها بأرقام لا صور._

#### PART-53 · نفث النار بطبقات · Layered fire breath · 🟢 جاهز / ready
- **ماذا / what:** نار من أنابيب لهب جمعية من الأحمر إلى الأبيض بتمايل ببذرة وانحناء، مع مخروط توهج وألسنة ملتفة ورذاذ اصطدام. — Fire as stacked additive flame tubes red→white with seeded wobble and bend, a wide glow cone, curling tongues and an impact splash.
- **متى أستخدمها / when:** تنانين، لهب، طاقة، ملصقات ملحمية.
- **كيف / how:** Studio: flame(seed, a, b, r0, r1, wob, bend) — 7 red #ff3d0a (.5, blur 3), 5 orange #ff9326 (.65, 2.4), 3 yellow #ffe7a2 (.85), 1 white (.75), all mode "add", radius tapers t^.75·(1 − .55t^6). SVG (duck_dragon.py): outer #dc2626 + blur20 #f97316, mid #f97316, core #fde68a, hot #fffbeb blur 8, 12 tongues, splash fan every 20°. **أرقام / params:** 16 tubes in 4 colours; splash ±80° every 20°.
- **الدليل / proof:** `kosif-studio/scenes/dragon_girl.py:108` · `kosif-studio/scenes/whale_dragon.py:247` · `kosif-one/projects/duck-vs-dragon/duck_dragon.py`

#### PART-54 · جمر ودخان وتعتيم · Embers, sparks & smoke atmosphere · 🟢 جاهز / ready
- **ماذا / what:** شرر ببذرة بأربعة ألوان نار، ودخان من قطوع مموهة كبيرة، وجمر على مسار النار يطفو للأعلى بعيدًا عن وجه البطل. — Seeded embers in four fire colours, large blurred smoke ellipses, and sparks scattered along the fire path drifting up, kept off the hero’s face.
- **متى أستخدمها / when:** تشطيب مشهد ناري أو ملحمي.
- **كيف / how:** duck_dragon: 110 embers r ∈ {1.2…3.8}, #fde047 #fbbf24 #fb923c #f97316 .55–1; 9 smoke ellipses rx 120–260 ry 18–40 .16 blur 20; vignette r 950 to black .6. Studio: dots(emb) #ffd27a .9 add + halos ×3 #ff7a2a .45 blur 2.4, order "sparkle"; Gaussian σ 36–44 px along the path, lift ≤ 100. **أرقام / params:** 110–440 embers; smoke .16 blur 20.
- **الدليل / proof:** `kosif-one/projects/duck-vs-dragon/duck_dragon.py` · `kosif-studio/scenes/dragon_girl.py:408` · `kosif-studio/scenes/whale_dragon.py:282`
- **أساليب / styles:** `style:pm-theparuchh-6e08c3`

#### PART-55 · شرر على ساعة الشريط · Event sparks on the tape clock (three-kit) · 📦 بأمر تثبيت / one install
- **ماذا / what:** شرر جمعي يُقذف عند الأحداث الصوتية ويتحرك على ساعة الشريط، فيعلق في الهواء حين يتوقف المسار. — Additive sparks thrown at sound events that move on the tape clock, so they hang in the air when the track stops.
- **متى أستخدمها / when:** ريل موسيقي ثلاثي، «توقف الشريط».
- **كيف / how:** K3.makeSparks([{t,x,y,z}], {per, speed, gravity, drift, color, size, seed}); userData.set(t, tapeFn). sound_ground: per 90, speed 6.5, gravity 7, drift 15 m/s, 2400 slow embers 0xff9a5a. Break variant: 26 sparks ballistic from a midpoint + torus flash ring red→green on repair. The demo project loads assets/main.bundle.js, which is not built in this checkout (koi_pond threw a load error here) — install esbuild and bundle first; the kit functions themselves ship in the prebuilt three-kit.bundle.js. **أرقام / params:** per 60; speed 5; gravity 6; life .5–1.6 s; #ffa040.
- **📦 تثبيت / install:** `cd 100-superskills/skills/kosif-montage-motion/scripts && npm install three@0.186.1 esbuild && python3 motion.py bundle sound_ground`
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:886` · `100-superskills/skills/kosif-montage-motion/scripts/projects/sound_ground/src/main.js:56` · `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js:93`

#### PART-56 · بخار وغيوم من عناقيد بيضاوية · Ellipse-cluster clouds, smoke & steam (Studio) · 🟢 جاهز / ready
- **ماذا / what:** عناقيد قطوع ببذرة مستدقة الأطراف تُقرأ غيمًا حين تموّه، ونسخ مزاحة بمزج screen/add لقمم مقمرة وبطون مضاءة بالنار، وبخار عند تصادم نار وماء. — Seeded tapered ellipse clusters read as clouds when blurred; offset screen/add copies give moonlit tops and fire-lit bellies; steam where fire meets water.
- **متى أستخدمها / when:** سماء مرسومة، دخان، بخار.
- **كيف / how:** cloud(cx, cy, w, h, n, seed) + fill(blur 12–20) + translated fill(mode "screen"|"add"); steam: #d6dde6 .45 blur 12 screen + noise .5 cell 20 + translate 14 #ff8a3a .32 add + glow #fff0c0 26 .7 + 6 tongues. **أرقام / params:** ellipse w .07–.16, h .3–.6; blur 13–17.
- **الدليل / proof:** `kosif-studio/scenes/dragon_girl.py:36` · `kosif-studio/scenes/whale_dragon.py:257`

#### PART-57 · رذاذ وزبد وانهمار ماء · Spray, foam & water sheeting · 🟢 جاهز / ready
- **ماذا / what:** رذاذ نقاط غاوسية أبيض ودافئ، وزبد على قمم الأمواج، وصفائح ماء تنهمر من الجسم ثم تمويه حركي. — Gaussian spray dots in white and warm add, foam along wave crests, water sheets running off a body, then motion blur.
- **متى أستخدمها / when:** حيتان، أمواج، اصطدام بالماء.
- **كيف / how:** spray(seed, cx, cy, n, sx, sy, up, sizes) + foam(seed, y, amp, n) + motion_blur; 3D fish jump: 60 spray points y = .05 + vy·u − 4.9u² (u ≤ .7 s) + two additive rings .9·e^(−.9u), scale .6 + 3.4u, second .35 s later. **أرقام / params:** 460 dots σ 160×70; 5 foam rows.
- **الدليل / proof:** `kosif-studio/scenes/whale_dragon.py:65` · `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js:205`

#### PART-58 · بحر عاكس وماء ضحل شفاف · Reflective sea & shallow see-through water (three-kit) · ✅ مُثبت هنا / proven here
- **ماذا / what:** سطح three.js Water بخرائط موج مولدة وانعكاس الشمس؛ وماء ضحل بمجموع جيوب وحلقات تموج وفرينل ولمعة GGX وشفافية ملونة بالعمق. — three.js Water plane with generated wave normals and sun reflection; shallow water with sum-of-sines swell, ripple rings, Fresnel, GGX glint and depth-tinted transmission.
- **متى أستخدمها / when:** بحر ليلي، بِرك، أنهار.
- **كيف / how:** K3.makeSea({size 30000, res 768, color #0e4a63, distortion 2.4, waveSize 3}) — night_boat frames rendered here (moon glitter, fish-jump rings). K3.makeShallowWater({width 30, depth 30, seg 256, ripples 24, amp .012, clarity .62, deep #0d3b3a, shallow #2f6f62, skyTop #6f9cc8, horizon #f2d6b0, bank #26301c}); w.userData.ripple(x,z,t0,amp); addCaustics scale ≈5.5. **أرقام / params:** sea res 768; shallow 256 seg, 24 rings, life 3.5 s, front .34 m/s.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:245` · `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/src/main.js` · `kosif-studio/motion/kit/three-kit.js:506`

#### PART-59 · شيدر ماء منمّط ورسام الماء · Stylised water shader / flat sea path · 🟢 جاهز / ready
- **ماذا / what:** ماء بثلاثة جيوب مجموعة ومشتقات تحليلية وانعكاس فرينل ولمعة شمس ولمعات مهشّرة وضباب؛ أو سطح بحر مسطح بجيب ورغوة على القمة. — Three summed sine waves with analytic normals, Fresnel sky, hot sun specular, hashed glints and fog; or a flat sea path rebuilt per frame with crest foam.
- **متى أستخدمها / when:** النيل، بحر كرتوني، شرح دورة الماء.
- **كيف / how:** fres = pow(1 − N·V, 4); spec = pow(R·L, 400)·14 + pow(R·L, 24)·.5; sparkle step(.9965, hash(floor(xz·1.6) + floor(9t))); fog 1 − exp(−(d·den)²). Flat: y = 790 + 9 sin(2πx/180 + 2.2t), gradient #2B86E0→#1559A8, foam #CFE9FF 5 px .8. **أرقام / params:** Nile deep #0A3A66 sky #7FB2E0 amp .12; flat amp 9 px λ 180 px.
- **الدليل / proof:** `kosif-one/projects/egypt-2120-animation/index.html` · `kosif-one/projects/water-cycle-animation/index.html`
- **أساليب / styles:** `style:pm-demitiyageekzen-7770ad`

#### PART-60 · أنظمة الطقس ثلاثية الأبعاد · 3D weather: vapour, cloud slab, rain, flocks · 📦 بأمر تثبيت / one install
- **ماذا / what:** بخار نقطي يصعد، طبقة سحب حجمية بالأشعة تتغير تغطيتها ولونها مع القصة، مطر آلاف الخطوط، وأسراب طيور تعبر قرب مستوى التركيز. — Rising vapour points, a raymarched volumetric cloud slab whose cover and colour follow the story, thousands of rain streaks, and bird flocks crossing near focus.
- **متى أستخدمها / when:** شرح دورة الماء، طقس، طبيعة.
- **كيف / how:** K3.makeVapour({n 1400, life 6–10 s, additive, alpha ×.16}); K3.makeCloudSlab({size [7000,520,4200], centre [0,1240,−900]}) 36 view steps × 3 light taps, powder term; K3.makeRain({n 9000, 900–1400 u/s, slant 120}); K3.makeFlock({n 16–18, path, t0, t1, flap sin 9t}); all driven by userData.set(t, …) ramps (water_cycle_3d). The demo project loads assets/main.bundle.js, which is not built in this checkout (koi_pond threw a load error here) — install esbuild and bundle first; the kit functions themselves ship in the prebuilt three-kit.bundle.js. **أرقام / params:** vapour 1400; rain 9000; cloud 36×3 steps.
- **📦 تثبيت / install:** `cd 100-superskills/skills/kosif-montage-motion/scripts && npm install three@0.186.1 esbuild && python3 motion.py bundle water_cycle_3d`
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:273` · `kosif-studio/motion/kit/three-kit.js:325` · `kosif-studio/motion/kit/three-kit.js:203` · `100-superskills/skills/kosif-montage-motion/scripts/projects/water_cycle_3d/src/main.js:34`

#### PART-61 · حياة البركة: كوي وبتلات وقصب · Pond life: koi, petals, lily pads, reeds, sway · 📦 بأمر تثبيت / one install
- **ماذا / what:** سبع أسماك كوي تنثني على مسارات ليساجو بأعماق مختلفة، 170 بتلة تسقط وتطفو وتصنع حلقات، زنابق تتمايل، وآلاف أعواد القصب والعشب تميل مع الريح. — Seven koi bend along Lissajous paths at depths, 170 petals fall and float (ringing the water), lily pads bob, thousands of reeds and grass blades sway.
- **متى أستخدمها / when:** هدوء، تأمل، يابان، طبيعة.
- **كيف / how:** makeKoi({length .62–.92, amp .10–.14}); x = cx + ax sin(dir·w·t + ph), z = cz + az sin(2·dir·w·t + ph2), depth −.22…−.52; K3.makePetals({n 120–170, fall 2.4–4.6 s, ripple amp .0016–.0024}); makeBlades 2200 (tall .95, amp .07, 1.2 Hz) + 6000 (tall .22, amp .25, 1.7 Hz); K3.addSway(mat, {amp .06, freq 1.3 Hz}) bend ∝ height²; flags K3.addWave(amp .08, 2.4 Hz, λ .9). The demo project loads assets/main.bundle.js, which is not built in this checkout (koi_pond threw a load error here) — install esbuild and bundle first; the kit functions themselves ship in the prebuilt three-kit.bundle.js. **أرقام / params:** 7 koi; 170 petals; 8200 blades.
- **📦 تثبيت / install:** `cd 100-superskills/skills/kosif-montage-motion/scripts && npm install three@0.186.1 esbuild && python3 motion.py bundle koi_pond`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/koi_pond/src/main.js:50` · `kosif-studio/motion/kit/three-kit.js:685` · `kosif-studio/motion/kit/three-kit.js:591` · `kosif-studio/motion/kit/three-kit.js:977`

#### PART-62 · مسارات ضوء السيارات · Long-exposure car light trails · 📦 بأمر تثبيت / one install
- **ماذا / what:** أضواء خلفية تبتعد وأمامية تقترب تصير خطوطًا متصلة بمط كل ضوء على اتجاه حركته. — Tail lights going away and headlights coming in become continuous streaks by stretching each light along its motion.
- **متى أستخدمها / when:** مدن ليلية، طرق، زمن يمر.
- **كيف / how:** 18 cars, 22–27 m/s, wrap 1560 m; tail 0xff1e1e ×6, head 0xfff1d8 ×6 spheres r .16; scale.z = 1 + trailLength(v)/(2·.16)·1.2, offset forward so the streak never sits inside the body. Studio also has a long-exposure "lighten" pass for light trails; its test errored in this container, so treat that path as unverified. The demo project loads assets/main.bundle.js, which is not built in this checkout (koi_pond threw a load error here) — install esbuild and bundle first; the kit functions themselves ship in the prebuilt three-kit.bundle.js. **أرقام / params:** 18 cars; ×6 emissive.
- **📦 تثبيت / install:** `cd 100-superskills/skills/kosif-montage-motion/scripts && npm install three@0.186.1 esbuild && python3 motion.py bundle blue_hour`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/blue_hour/src/main.js:107`

#### PART-63 · سكب وارتفاع السائل · Pour stream & liquid fill with wobble · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** زجاجة تميل وتسكب خيطًا من عنقها، والمنسوب يرتفع بقص مستطيل مع تموج سطح مخمد، وسحب قشدة تنتشر داخل السائل. — A bottle tilts and pours a stream from its neck; the level rises via a clip rect with a damped surface wobble; cream clouds diffuse inside the liquid.
- **متى أستخدمها / when:** مشروبات، وصفات، «امتلاء» كمؤشر.
- **كيف / how:** Enter 500 ms easeOutBack, rotate ~−45° about the neck, 4–6 px stream grows then retracts, exit 400 ms; level cubic-bezier(.33,0,.2,1) 2.5–3 s, wobble 2–4 px @ 1.5 Hz damped 600 ms; cream: 6–10 blobs blur 12–20 px drifting with noise, clipped to the liquid, ~3 s; ice cubes easeOutBounce 700 ms, 12 px bounce, 180 ms stagger. **أرقام / params:** pour 2.5–3 s; wobble 2–4 px @ 1.5 Hz.
- **الدليل / proof:** `kosif-tool/styles/pm-ror-fly-9950f1` · `kosif-tool/styles/pm-sarut0bisasuke-cefa43`
- **أساليب / styles:** `style:pm-ror-fly-9950f1` · `style:pm-sarut0bisasuke-cefa43`

#### PART-64 · سائل ملون ومعدن سائل · Fluid sim backdrop & chrome metaballs · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** سوائل مستقرة على GPU بحقن صبغة خلف نص محدد؛ أو 3–5 كرات SDF تدور وتلتحم بمادة كروم؛ أو كرات بخطوط كنتور. — GPU stable fluids with dye injection behind outlined text; 3–5 raymarched SDF spheres orbiting and merging in chrome; or metaballs with marching-squares iso-contours.
- **متى أستخدمها / when:** أغلفة جريئة، موسيقى إلكترونية، شعارات سائلة.
- **كيف / how:** Chrome: smooth k .4, orbit .5 Hz, env-map; contours: sum of 7 radial fields, 4–6 iso levels; HyperFrames vfx-liquid-background (vertex displacement plane, 12 s) is the installable option. **أرقام / params:** k .4; 7 balls; 4–6 contours.
- **الدليل / proof:** `kosif-tool/styles/pm-lukasersil-0ed38e` · `kosif-tool/styles/pm-sahildesigner23-ee3155` · `kosif-tool/styles/pm-teslachartz-c58b32` · `kosif-one/vendor/hyperframes/registry/blocks/vfx-liquid-background/vfx-liquid-background.html`
- **أساليب / styles:** `style:pm-lukasersil-0ed38e` · `style:pm-sahildesigner23-ee3155` · `style:pm-teslachartz-c58b32`

#### PART-65 · لهب عادم وشعلة · Exhaust plume & canvas fire emitter · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** مخروط جمعي بضوضاء وأشرطة ماسية ساطعة (بنفسجي→أبيض)، أو باعث يولد 30–60 جسيمًا في الإطار تصعد بسلم أبيض→أصفر→أحمر. — Additive noisy cone with bright shock-diamond bands (violet→white core), or an emitter spawning 30–60 particles/frame rising white→yellow→red→transparent.
- **متى أستخدمها / when:** صواريخ، محركات، شموع، مشاعل.
- **كيف / how:** Emitter as closed form: particle i born at floor(t·rate) with hash-seeded velocity, age = t − birth, colour ramp by age, "lighter"; cube exhaust: emissive cubes ~1 s life, 40/s; heat streaks: red line sprites rising and fading. **أرقام / params:** 30–60 / frame; life ~1 s.
- **الدليل / proof:** `kosif-tool/styles/pm-konstantinsaifo-96fc89` · `kosif-tool/styles/pm-chrisjdimarco-f068db` · `kosif-tool/styles/pm-ivanfioravanti-bd9261`
- **أساليب / styles:** `style:pm-konstantinsaifo-96fc89` · `style:pm-chrisjdimarco-f068db` · `style:pm-ivanfioravanti-bd9261`

#### PART-66 · أشعة تحت الماء وفوانيس عائمة · Underwater rays & floating lanterns · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** تدرج أزرق بأشعة ضوء قطرية شفافة، قناديل تتمايل وفقاعات تصعد؛ أو فوانيس لوتس مضيئة تطفو على الماء بوميض وانعكاس قصير. — Blue gradient with translucent diagonal light shafts, bobbing jellyfish and rising bubbles; or glowing lotus lanterns drifting on water with flicker and a short reflection streak.
- **متى أستخدمها / when:** بحر، أطفال، مهرجانات فوانيس.
- **كيف / how:** Bob 10 px @ .4 Hz; bubbles 20–40 px/s with wobble; lanterns 8–15, flicker .85–1.0 @ 3–6 Hz, drift 5–10 px/s. **أرقام / params:** bob 10 px/.4 Hz; 8–15 lanterns.
- **الدليل / proof:** `kosif-tool/styles/pm-abderrahmen-g-9e8ed0` · `kosif-tool/styles/pm-demitiyageekzen-7770ad`
- **أساليب / styles:** `style:pm-abderrahmen-g-9e8ed0` · `style:pm-demitiyageekzen-7770ad`

#### PART-67 · محاكاة هوديني · Houdini FLIP / Pyro / Vellum / RBD + Karma · 🔑 مفتاح أو خدمة / needs key or service
- **ماذا / what:** محاليل احترافية للسوائل والدخان والقماش والأجسام الصلبة، وجسيمات curl بـ VEX، تتطلب ترخيصًا تجاريًا. — Pro fluid, smoke, cloth and rigid-body solvers and VEX curl-flow particles — commercial licence required.
- **متى أستخدمها / when:** فقط إن وفّر المستخدم Houdini وترخيصه.
- **كيف / how:** hython headless baking; VEX: @v = lerp(@v, noise·speed, blend); orient to velocity; @pscale shrinks from 70% of life. Not available here — use PART-23 / PART-51 instead.
- **⚖️ ترخيص / license:** Houdini تجاري (SideFX) / commercial SideFX licence.
- **الدليل / proof:** `kosif-atlas/skills/228-mas-3d-games/708-houdini/SKILL.md`

## الفيزياء والأجسام — Physics & bodies

_الفيزياء في الفيديو تُحسب بخطوة ثابتة 1/fps (أو أجزاء منها) وتُخبز — وإلا يختلف الرندر الثاني عن الأول._

#### PART-68 · كرة ترتد بمعامل ارتداد · Gravity bounce with restitution & dotted trail · ✅ مُثبت هنا / proven here
- **ماذا / what:** y″ = −g مع عكس السرعة × e عند التلامس، ونقطة كل N إطارات تترك أثر قطع مكافئ منقط مع تسمية «e = 0.75». — Integrate y″ = −g, reflect velocity ×e on contact, stamp a dot every N frames to leave a dotted parabola, annotated “e = 0.75”.
- **متى أستخدمها / when:** شرح فيزياء، شعارات تقفز، «الطاقة تُفقد».
- **كيف / how:** Fixed dt = 1/60 replayed from frame 0 inside seek (deterministic); e .75–.85; g 900 px/s²; dot 4 px #c9452c every 2–4 frames. Rendered here. Add squash 20% on impact and stretch 10% in flight (SHAPE squash). **أرقام / params:** e .75–.85; dt 1/60; dot every 2–4 frames.
- **الدليل / proof:** `kosif-tool/styles/pm-hbcoop-de365c` · `kosif-tool/styles/pm-deifosv-04e4d3/BRIEF.md`
- **أساليب / styles:** `style:pm-hbcoop-de365c` · `style:pm-web3wesley-7bb108`

#### PART-69 · كرة داخل حلقات دوارة · Ball in rotating gapped rings (escape sim) · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** كرة ترتد داخل 12 حلقة دوارة بفجوات؛ تنعكس السرعة حول العمودي وتمر من الفجوة فتختفي الحلقة متشظية. — A ball ricochets inside 12 rotating gapped rings; velocity reflects about the normal and passes through the gap, the ring then shatters.
- **متى أستخدمها / when:** ريلز «مرضية» (satisfying)، ألعاب.
- **كيف / how:** Fixed sub-steps (120 Hz at 60 fps or 4/frame); when |p − c| ≥ R − r: v −= 2(v·n)n, restitution 1; gap test via atan2 within the rotating window (gap 28–40°); rings ω .3 + .08i alternating; tapered trail .3 s. **أرقام / params:** 12 rings; gap 28–40°; speed ~600 px/s.
- **الدليل / proof:** `kosif-tool/styles/pm-kantamk-61f410` · `kosif-tool/styles/pm-kantamk-61f410/BRIEF.md`
- **أساليب / styles:** `style:pm-kantamk-61f410`

#### PART-70 · سقوط وتكدس الأجسام · Drops, piles & toppling stacks · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** بطاقات تسقط بارتداد وتتكدس ثم يتمايل البرج وينهار؛ أيقونات تسقط في وعاء؛ ملصقات تتكوم أسفل الشاشة؛ برطمان يمتلئ بعداد. — Cards drop with bounce and stack, the tower sways and topples; icons fall into a bowl; posters pile along the bottom; a jar fills with a counter.
- **متى أستخدمها / when:** «تراكم»، كمية، إحصاءات مرحة.
- **كيف / how:** Each item as phases of t: drop ~300 ms easeOutBounce (stagger 400 ms), shared sway growing to 6°, topple about base, settle; icons 500 ms easeInQuad + 15% bounce, ±15°; jar g ~2500 px/s², restitution .3, 1 item / 120 ms; posters 40–60, ±30°, stagger 30 ms (or pre-baked rigid bodies). **أرقام / params:** drop 300 ms; restitution .3; 1 item / 120 ms.
- **الدليل / proof:** `kosif-tool/styles/stickman` · `kosif-tool/styles/pm-wozu-co-242285` · `kosif-tool/styles/pm-thilina-a-891c09` · `kosif-tool/styles/pm-lester-tyy-f897f7`
- **أساليب / styles:** `style:stickman` · `style:pm-wozu-co-242285` · `style:pm-thilina-a-891c09` · `style:pm-lester-tyy-f897f7` · `style:pm-lexnlin-6161a6`

#### PART-71 · محركات الأجسام الصلبة · Rigid-body engines (Rapier / cannon-es / matter-js) · 📦 بأمر تثبيت / one install
- **ماذا / what:** شعارات ومكعبات تسقط وتتكدس بفيزياء حقيقية في 2D أو 3D. — Logos and voxels falling and stacking with real physics in 2D or 3D.
- **متى أستخدمها / when:** حين لا تكفي المنحنيات المكتوبة (عشرات الأجسام المتصادمة).
- **كيف / how:** Step a fixed dt = 1/fps per frame from a seeded initial state and bake positions to JSON, then render frames from the bake (never real-time). @react-three/rapier for R3F; matter-js for 2D. **أرقام / params:** dt 1/fps; bake first.
- **📦 تثبيت / install:** `npm i @dimforge/rapier3d-compat matter-js cannon-es`
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md` · `kosif-atlas/skills/2696-game-studio/10367-react-three-fiber-game/SKILL.md`

#### PART-72 · حركات فيزيائية جاهزة · HyperFrames physical motions (pendulum, physical exit, stack shuffle) · 📦 بأمر تثبيت / one install
- **ماذا / what:** محتوى معلق يتأرجح بندوليًا ويستقر، بطاقة تخرج بزخم حقيقي (رمي، سقوط، انزلاق) بلا تلاشٍ، ورصة بطاقات تُخلط بكتلة. — Content swings into rest like a damped pendulum, a card exits with real momentum (toss/drop/slide), and a 3–5 card stack reshuffles with mass.
- **متى أستخدمها / when:** بطاقات وواجهات بحس مادي.
- **كيف / how:** npx hyperframes add pendulum-swing (pivot top-center|left|right, amplitude gentle|standard|wide) | physical-exit (mode toss|drop|slide) | spring-stack-shuffle (cues "0.9, 1.7, 1.95"). Reactive displacement rule: the intruder tween drives the victim, victim durations 40–50% of the intruder.
- **📦 تثبيت / install:** `npx hyperframes add pendulum-swing`
- **⚖️ ترخيص / license:** Apache-2.0.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/pendulum-swing/pendulum-swing.html` · `kosif-one/vendor/hyperframes/registry/components/physical-exit/physical-exit.html` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/reactive-displacement.md`

#### PART-73 · أوتار تهتز عند الاصطدام · Vibrating strings on impact · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** خمسة منحنيات أفقية؛ عند الاصطدام تأخذ نقطة التحكم سعة A تخمد بجيب مخمد. — Five horizontal quadratics; on impact the control point gets amplitude A decaying as a damped sine.
- **متى أستخدمها / when:** موسيقى، ضربة، وتر.
- **كيف / how:** offset = A·e^(−6t)·sin(30t), A ≈ 4% of height, 400 ms. **أرقام / params:** A 4% h; e^(−6t) sin 30t.
- **الدليل / proof:** `kosif-tool/styles/pm-1littlecoder-9fef89`
- **أساليب / styles:** `style:pm-1littlecoder-9fef89`

#### PART-74 · أسراب الطيور والحروف (boids) · Flocks & boids (birds, letters, stipple) · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** سرب V يرفرف على مسار، أو 8192 نقطة بفصل ومحاذاة وتماسك، أو حروف تطير كسرب فوق سماء متدرجة. — Flapping V-birds on a path, 8,192 boids with separation/alignment/cohesion, or glyph sprites flocking over a gradient sky.
- **متى أستخدمها / when:** طبيعة، حرية، «الأفكار تطير».
- **كيف / how:** three-kit makeFlock n 18 (ready, see PART-60); boids: precompute on CPU with fixed dt and bake, draw 1–2 px dots with a soft projected shadow; gulls 3–5 flapping 3 Hz on slow paths. For Arabic letter flocks fly whole words, not letters. **أرقام / params:** n 18 / 8192; flap 3 Hz.
- **الدليل / proof:** `kosif-tool/styles/pm-hbcoop-de365c` · `kosif-tool/styles/pm-ajith-io-ea7f2d` · `kosif-tool/styles/pm-axtonliu-0b861d` · `kosif-studio/motion/kit/three-kit.js:203`
- **أساليب / styles:** `style:pm-hbcoop-de365c` · `style:pm-ajith-io-ea7f2d` · `style:pm-axtonliu-0b861d`

#### PART-75 · رمية قوسية بأشباح · Parabolic toss with ghost trail · 💡 فكرة / idea
- **ماذا / what:** رمز يُقذف على قطع مكافئ ويترك 12 نسخة شبحية تخبو. — A token thrown on a parabola leaving 12 fading ghost copies.
- **متى أستخدمها / when:** «أرسل»، دفع، تحويل نقاط.
- **كيف / how:** Untested brief idea: sample the arc at 12 earlier times (PART-31), 900 ms total, trail fade 200 ms. **أرقام / params:** 900 ms; 12 ghosts.
- **الدليل / proof:** `kosif-tool/styles/pm-paulo-kombucha-96431c/BRIEF.md`

## توليفات قوية / power combos

- **كلمة من الفوضى / word from chaos:** PART-15 + PART-23 + PART-02 + GLOW (توهج بنصف وربع الدقة) + CAM (اقتراب واهتزاز يخمد) + BEAT (ضربة 70→38Hz على الانفجار) — كما في proofs/particles-to-arabic.
- **ليل ممطر حي / living rainy night:** PART-37 + TEX (طوب يتلوّن وأرض مبتلة) + GLOW (نيون) + PART-35 + CAM (اهتزاز يدوي ±2px) — كما في proofs/neon-glow وmidnight_cat.
- **ريل موسيقي يتنفس / breathing music reel:** PART-43 + PART-06 (على كل onset) + BEAT (features.json لكل إطار) + SHAPE (حلقة صدمة) + SYNC (كاريوكي) — كما في proofs/audio-reactive-spectrum.
- **دعاء ليلي هادئ / calm night dua:** PART-34 + PART-35 + PART-40 (بتلات) + SHAPE (وردة ثمانية) + TEX (قمر إجرائي) + VOICE (بلا موسيقى) — جسيمات قليلة بطيئة لا تنافس الكلمة.
- **احتفال إطلاق / launch celebration:** PART-08 + PART-07 + PART-13 + BRAND (الشعار) + EASE (back.out للكلمة) + BEAT (whoosh + pop).
- **قصة بيانات من نقاط / data from dots:** PART-03 + PART-18 + PART-26 + DATA (القيم والمحاور) + MAP (PART-27 للتدفقات الجغرافية) — كل نقطة كيان والوحدة مكتوبة.
- **كوكب أفكار / planet of ideas:** PART-46 + PART-47 + PART-48 + 3D (كاميرا مدارية) + GLOW (bloom) + TYPE/ARAB (رقائق كلمات تنبثق على النقاط).
- **شرح دورة الماء / water-cycle explainer:** PART-60 + PART-58 + PART-33 + EXPL (تسميات) + CAM (رحلة كاميرا) — بخار يصعد، سحب تعتم، مطر، نهر.

## أخطاء ممنوعة / never do

1. **لا Math.random ولا Date.now داخل الرندر** — كل رندر يختلف وseek يكسر الحالة؛ هاش أو mulberry32 ببذرة (PART-01).
2. **لا محاكاة بحالة متراكمة تُقدَّم مع الساعة** — القفز إلى إطار يعطي نتيجة مختلفة؛ صيغة مغلقة أو خبز مسبق بخطوة ثابتة (PART-02).
3. **لا تجمع جسيمات على حروف عربية مفصولة** — خذ العينات من الكلمة المشكّلة كاملة فتبقى الحروف متصلة، واجعل الكشف من اليمين (PART-15).
4. **لا غبار زخرفي في مشهد بيانات** — كل جسيم يجب أن يعني كيانًا أو تدفقًا؛ الزينة تكذب على الأرقام (PART-03).
5. **لا جسيمات فوق النص المقروء** — خلف الطباعة وبكثافة غير متساوية، والكلمة مقروءة ≥ 1 ث قبل أن تتفكك (PART-04، PART-16).
6. **لا MOTION.rain بـ at أقل من مدة السقوط** — جربتها هنا: القطرات الأولى تبقى فوق الكادر؛ ابدأ at ≥ 0.6 ث (PART-32).
7. **لا تعتمد على وضع virtual لصفحات WebGL في render_html.cjs** — انتهت مهلته هنا؛ قُد مشاريع three-kit عبر window.seek / render(t) (PART-58).
8. **لا انفجار متأخر أو مبكر عن التلامس** — يقع على إطار الاصطدام أو onset بالضبط، وإلا يبدو الصوت والصورة منفصلين (PART-05).
9. **لا عشرات آلاف النقاط على Canvas 2D** — 150–600 هو السقف المريح؛ انتقل إلى WebGL Points/FBO (PART-04، PART-51).
10. **لا وعود Houdini أو محاكاة سوائل حقيقية هنا** — غير متاحة؛ اعرض curl وFBO والماء الإجرائي بدلًا منها (PART-67).
11. **لا وميض سريع متكرر بعد الانفجار** — احترم حدود الوميض وreduced-motion، خصوصًا في المحتوى العام.

## أقوى 5 حركات توقيع / 5 signature moves

1. **PART-15 — الكلمة العربية من 6000 جسيم:** curl ثم انجذاب من اليمين إلى عينات الكلمة المشكلة ثم انفجار جمر — مُثبت في فيلم كامل.
2. **PART-06 — الانفجار ببذرة:** 160 جسيمًا، expo.out، جاذبية 120px، تلاشٍ inOutCubic — في الـstarter ومُثبت هنا.
3. **PART-37 — مطر بطبقتين وبرك:** 152 بعيدة + 32 قريبة وحلقات ورذاذ — أسرع طريق لليل سينمائي.
4. **PART-46 — كرة فيبوناتشي:** 900 نقطة بالزاوية الذهبية وشفافية بالعمق — «عالمي/ذكاء اصطناعي» في 15 سطرًا.
5. **PART-43 — ذرات تصعد مع الصوت:** onset يرفعها وكل ركلة حلقة — الجسيمات تسمع الموسيقى.
