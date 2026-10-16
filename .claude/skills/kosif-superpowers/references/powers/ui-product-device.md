# الواجهات والمنتجات والأجهزة — UI, product & devices

> **قوتك هنا:** تصنع عرض منتج يبدو كتسجيل حقيقي لكنه مُخرج إطارًا بإطار — مؤشر بفيزياء يضع رأسه على الهدف، ضغطة تستجيب بعد 60–120 ms، هاتف بمنظور صحيح وواجهة عربية معكوسة كما ينبغي، ووكيل ذكاء اصطناعي يشطب مهامه أمام المشاهد.
> **أقوى دليل:** رندرتُ هنا مؤشر motion-kit مع الضغط والكتابة (`kosif-studio/motion/projects/kit_v3_demo`، 180 إطارًا، VERIFY OK) ووصفة واجهة Canvas من `kosif-tool/playbooks/product-ui.md` (120 إطارًا 9:16)، واختبار مشغل HTML المستقل نجح؛ وبطاقات الزجاج مثبتة في فيلم `proofs/glass-luxury-logo`.
> **You can:** direct silent demos, cursors, typing/agent theater, micro-interactions, phones and browsers, scroll tours and launch films from a URL. **89 powers follow** — ✅ 5 · 🟢 15 · 📦 23 · 🔑 1 · 👁 16 · 📄 27 · 💡 2.

**الحالة / status:** ✅ مُثبت هنا (كود + اختبار أو رندر في هذه الحاوية) · 🟢 جاهز (كود المالك يعمل بلا إضافات) · 📦 بأمر تثبيت · 🔑 مفتاح أو خدمة · 👁 شوهد في فيديو أنتجتَه (وصفة البناء مرفقة) · 📄 موصوف فقط · 💡 فكرة.
مسارات الدليل نسبية إلى `/home/user/`؛ `style:<id>` = فيديو مرجعي أنتجتَه سابقًا (ملاحظاته في `kosif-tool/styles/<id>/`).

**فحص سريع لهذه الحاوية (2026-10-16):** Playwright + Chromium ✔ · `render_html.cjs` يرندر صفحات `__kosif.seek` وصفحات motion-kit (بسطر جسر واحد) ✔ · مكوّنات HyperFrames موجودة محليًا للقراءة لكن رندرها يحتاج `npx hyperframes` (جرّبتُ demo.html بالوضع الافتراضي فخرج إطار ثابت) · `starters/remotion` بلا node_modules → `npm install` أولًا.

## الفهرس / contents
- **قوانين إخراج عرض المنتج — Product-demo direction laws** — UI-01 … UI-10 (10)
- **المؤشر واللمس — Cursor & touch** — UI-11 … UI-24 (14)
- **الكتابة والطلبات ومسرح الذكاء — Typing, prompts & AI-agent theater** — UI-25 … UI-32 (8)
- **حركات الواجهة الدقيقة — Micro-interactions & UI components** — UI-33 … UI-46 (14)
- **الأجهزة والإطارات — Devices & frames** — UI-47 … UI-57 (11)
- **الشاشات والتمرير والكاميرا على الواجهة — Screens, scroll & camera on UI** — UI-58 … UI-71 (14)
- **التقاط المواقع والتسجيل وأفلام الإطلاق — Capture, recording & launch films** — UI-72 … UI-78 (7)
- **أنظمة التصميم والقوالب والأدوات — Design tokens, templates & tooling** — UI-79 … UI-89 (11)
- توليفات قوية / power combos · أخطاء ممنوعة / never do · أقوى 5 حركات توقيع / 5 signature moves

## قوانين إخراج عرض المنتج — Product-demo direction laws

_قبل أي مؤشر أو هاتف: من يتكلم في اللقطة، وماذا يرى المشاهد أولًا، ومتى تحدث الاستجابة._

#### UI-01 · العرض الصامت: الواجهة تحكي · Silent product demo — the UI tells the story · 📄 موصوف / documented only
- **ماذا / what:** الواجهة والمؤشر والكاميرا يحملون القصة، والكلمات تسمّي الخطوة أو النتيجة فقط. — Interface, cursor and camera carry the story; words only name a beat or an outcome.
- **متى أستخدمها / when:** أي فيلم منتج أو ميزة بلا تعليق صوتي — any feature film without narration.
- **كيف / how:** Storyboard five columns: time · screen state · pointer action · camera focus · text. Frame 1 must already be legible. The camera moves toward the current action, then settles before the next one; one subject per beat; clear old props before the next beat. Animate from time only (deterministic). Before the full export render stills at: frame 0, each action, every transition midpoint, last frame — and watch it once muted. **أرقام / params:** stills: first · per action · transition midpoints · last
- **الدليل / proof:** `kosif-atlas/skills/101-video-skills/217-silent-product-demo/SKILL.md` · `kosif-atlas/skills/101-video-skills/215-feature-video/SKILL.md` · `kosif-atlas/skills/101-video-skills/220-ui-tutorial-video`

#### UI-02 · ثلاثية النية والفعل والاستجابة · Intent → action → response with real latency · 📄 موصوف / documented only
- **ماذا / what:** المؤشر يصل، يضغط، ثم تستجيب الواجهة بعد زمن استجابة واقعي. — The pointer arrives, presses, and the UI answers after a believable latency.
- **متى أستخدمها / when:** كل نقرة أو لمسة في أي عرض — every click or tap beat.
- **كيف / how:** Response starts 60–120 ms after the press frame. 0 ms reads as a slideshow, more than 200 ms reads as a bug. Never animate success before the action completes. Direct-manipulation feedback lands within 100 ms; UI animations stay under 500 ms and look interruptible. **أرقام / params:** latency 60–120 ms; >200 ms = bug; feedback <100 ms; anim <500 ms
- **الدليل / proof:** `kosif-tool/playbooks/product-ui.md:29` · `kosif-tool/playbooks/product-ui.md:58` · `kosif-atlas/skills/3438-ux-design/14121-microinteractions`

#### UI-03 · محتوى واجهة حقيقي ومحلي · Real, locale-correct UI content · 📄 موصوف / documented only
- **ماذا / what:** أسماء ومبالغ وتواريخ معقولة بلغة المشاهد؛ لا lorem ولا مؤشرات متناقضة ولا ميزة مخترعة. — Plausible locale-correct names, amounts and dates; no lorem, no contradictory KPIs, no invented features.
- **متى أستخدمها / when:** كل شاشة تظهر في الفيلم — every screen in the film.
- **كيف / how:** Write the strings first (Arabic UI labels ≥ 28 px at 1080 wide, line-height 1.6–1.8, letter-spacing 0). Use disposable test data when capturing a real app. Prices, countdowns and claims must be confirmed by the user — a fake price or countdown is forbidden. Saudi/Gulf money: SAR with tabular digits from one numeral system. **أرقام / params:** Arabic UI text ≥ 28 px; lh 1.6–1.8
- **الدليل / proof:** `kosif-tool/playbooks/product-ui.md:19` · `kosif-tool/playbooks/product-ui.md:209-214` · `kosif-atlas/skills/101-video-skills/215-feature-video/SKILL.md`

#### UI-04 · إعادة بناء الشاشة كطبقات · Layered screen rebuild · 🟢 جاهز / ready
- **ماذا / what:** الشاشة تُبنى طبقات: خلفية ← إطار ← محتوى ← أدوات ← طبقات عائمة ← مؤشر ← شروح، ولكل طبقة جدولها الزمني. — Build the screen as background → chrome → content → controls → overlays → pointer → callouts, each with its own timeline.
- **متى أستخدمها / when:** عندما تحتاج زوومًا شديدًا أو حركة داخل الواجهة — whenever you need deep zoom or motion inside the UI.
- **كيف / how:** Rebuild the UI as live DOM/SVG/Canvas with real strings at 2× density; keep a flattened screenshot only as the reference to match. If zoom makes a screenshot unreadable, re-capture at higher resolution or rebuild it as DOM. Depth comes from elevation tiers and overlap, plus 2–4% chrome/content parallax — not from tilt or glass. **أرقام / params:** 2× density; parallax 2–4%
- **الدليل / proof:** `kosif-tool/playbooks/product-ui.md:17` · `kosif-tool/playbooks/product-ui.md:23` · `kosif-atlas/skills/101-video-skills/220-ui-tutorial-video/SKILL.md`

#### UI-05 · حقيبة أصول من أجزاء حقيقية · Animation kit from real parts · 🟢 جاهز / ready
- **ماذا / what:** قبل التحريك: أعد بناء الواجهة كـ DOM، صوّرها بدقة 3–5×، واقطع كل زر وأيقونة وشريحة كقطعة شفافة ≥ 1600 بكسل. — Before animating, rebuild the UI as DOM, shoot it at 3–5× and cut every button, chip and icon into a transparent part ≥ 1600 px.
- **متى أستخدمها / when:** إعلان منتج يحتاج قطعًا تتطاير وتتركب — product ads where parts fly and assemble.
- **كيف / how:** Playwright element screenshots with omitBackground:true for transparent parts (Playwright + Chromium are installed here). Split the official SVG mark into layers and re-stack them; a PIL difference check must stay ≤ 1/255. Watch aspect: rendering 1200×800 parts into a 224×160 slot stretches 7%. **أرقام / params:** parts ≥ 1600 px; capture 3–5×; layer diff ≤ 1/255
- **الدليل / proof:** `kosif-atlas/skills/2681-emulo/10272-video/SKILL.md`

#### UI-06 · عكس الواجهة للعربية · RTL product-UI mirroring · 📄 موصوف / documented only
- **ماذا / what:** اعكس التفاعل لا العتاد: الشريط الجانبي يمين، الزر الأساسي يسار، الأسهم مقلوبة، والتقدم يمتلئ من اليمين. — Mirror interaction, not hardware: sidebar right, primary action left, chevrons flipped, progress fills right-to-left.
- **متى أستخدمها / when:** أي واجهة أو هاتف عربي في الفيلم — any Arabic UI or phone.
- **كيف / how:** Use dir=rtl on the UI container only (not <html> in renders) with logical CSS (margin-inline-start, inset-inline-end). The cursor starts bottom-right; forward navigation pushes the new screen in from the left; toasts enter top-left (top-end). Phones: back chevron on the right, toggles 'on' at the left, tab order RTL; the island, camera and hardware buttons are NOT mirrored; hero copy sits right of the device with positive yaw. Phone numbers and times get unicode-bidi:plaintext. Cut typed text at graphemes with Intl.Segmenter. Narrow tab rows: 44 px fade on the inline-start edge plus proximity scroll-snap. **أرقام / params:** Arabic compact rows +10% line height; tab fade 44 px
- **الدليل / proof:** `kosif-tool/playbooks/product-ui.md:209-214` · `kosif-tool/playbooks/phone.md:187-192` · `kosif-audit-pro/patch/kosif-v17.css`

#### UI-07 · لوحة البيانات داخل الإطار · Dashboard composition for a frame · 📄 موصوف / documented only
- **ماذا / what:** سؤال واحد يسيطر واللوحة كلها تتراجع خلفه. — One question dominates; everything else recedes.
- **متى أستخدمها / when:** مشاهد لوحات تحكم أو تقارير — dashboard or report scenes.
- **كيف / how:** One focal view + subordinate context; 5–7 KPIs max (4–6 for an executive summary); legends next to the evidence; no wall of equal tiles. Animate the headline tile first, then the rest. Operations scenes show live/stale states explicitly (status dot with halo, see UI-45). **أرقام / params:** 5–7 KPIs; headline first
- **الدليل / proof:** `kosif-atlas/skills/3455-business-analytics/14162-kpi-dashboard-design/SKILL.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10335-visualization-strategy-and-critique/SKILL.md`

#### UI-08 · تشريح التفاعل الدقيق كوحدة مشهد · Microinteraction anatomy as a beat · 📄 موصوف / documented only
- **ماذا / what:** كل لحظة واجهة = مُطلِق ← قاعدة ← تغذية راجعة ← حالة مستقرة. — Every UI moment is trigger → rule → feedback → settled state.
- **متى أستخدمها / when:** تقطيع أي عرض واجهة إلى نبضات — breaking any UI demo into beats.
- **كيف / how:** Storyboard each UI beat as trigger → visible change → settled state, and score it with an 8-row checklist (score = passed/8 × 10). Physical metaphors stay shortened: drawers slide from their side, modals rise like cards, momentum scroll settles on a spring. Standard ranges: 150 ms micro, 250–300 ms transitions, 400–500 ms larger moves; whole-UI motion ≤ 700 ms, ≤ 3 flashes per second. **أرقام / params:** 150 / 250–300 / 400–500 ms; ≤ 700 ms; ≤ 3 flashes/s
- **الدليل / proof:** `kosif-atlas/skills/3438-ux-design/14121-microinteractions` · `kosif-atlas/skills/1503-universal-design-principles/3766-mimicry-behavioral` · `100-superskills/skills/ui-motion-microinteractions/SKILL.md`

#### UI-09 · مقطع حلقة لمكوّن واحد · Seamless UI component loop (3–6 s) · 📄 موصوف / documented only
- **ماذا / what:** مكوّن حقيقي واحد يؤدي فعلًا واحدًا ويعود لبدايته بلا قفزة. — One real component performs one action and loops without a jump.
- **متى أستخدمها / when:** ردود سوشيال، صفحات منتج، عرض زر أو مفتاح — social replies, product pages, a single control.
- **كيف / how:** Use the component's real size, colours, shadows and timing; fit whole periodic cycles into the duration; one-shot actions return via a plausible reverse. Locked camera or one subtle push. Compare the first and last frames and watch several repeats for jumps or double triggers. **أرقام / params:** 3–6 s; one action; first frame == last frame
- **الدليل / proof:** `kosif-atlas/skills/101-video-skills/219-ui-component-clip/SKILL.md`

#### UI-10 · عناوين أفعال بسيطة في الشروحات · Plain action labels in tutorials · 📄 موصوف / documented only
- **ماذا / what:** التسمية تقول الفعل («اختر ملفًا»، «اضغط تسجيل») لا رقم الخطوة. — Captions name the action ('CHOOSE A FILE', 'PRESS RECORD'), not decorative step numbers.
- **متى أستخدمها / when:** فيديوهات تعليم الاستخدام — how-to and onboarding videos.
- **كيف / how:** Open with the payoff, then explain steps over the action. One short line per decision; the pointer reaches the exact target and holds through the press; keep menus and overlays where the app places them.
- **الدليل / proof:** `kosif-atlas/skills/101-video-skills/220-ui-tutorial-video/SKILL.md`

## المؤشر واللمس — Cursor & touch

_المؤشر ممثل: يظهر عند القرار فقط، يتحرك على منحنى بسرعة شبه ثابتة، ويضع رأسه على الهدف قبل الضغط._

#### UI-11 · مؤشر بفيزياء في motion-kit · motion-kit physics cursor + press + typeOn · ✅ مُثبت هنا / proven here
- **ماذا / what:** سهم مرسوم يمر بمحطات زمنية على منحنى Hermite ويتوقف بسرعة صفر، ويضغط مع انضغاط الهدف. — A drawn arrow travels timed stops on a Hermite curve (zero velocity at holds) and presses with the target dipping.
- **متى أستخدمها / when:** أي عرض واجهة في HTML/GSAP — any HTML/GSAP UI demo.
- **كيف / how:** c = M.cursor(stage,{size:30}); M.moveCursor(tl, c, [{t,x,y},…], {hold:[t…]}) samples the path at 60 fps into keyframes; M.press(tl, c, at, {target, down:.97}); M.typeOn(tl, el, text, at, {cps:46, hold:.6}). Rendered here: kit_v3_demo through render_html.cjs (6 s, 180 frames, VERIFY OK) after adding one bridge line, because the kit exposes window.__kosifSeek, not window.__kosif. **أرقام / params:** size 28–34 px (h ×1.22), drop-shadow 0 6px 8px rgba(0,0,0,.28); travel 36–48 f, arc 15–25% of the path; press 0.88 over 4 f, recover 8 f; target 0.97

```html
<!-- render any motion-kit page with tools/render_html.cjs -->
<script>window.__kosif = { duration: 6, seek: (t) => window.__kosifSeek(t) };</script>
```

- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:403` · `kosif-studio/motion/kit/motion-kit.js:426` · `kosif-studio/motion/projects/kit_v3_demo/index.html:39` · `kosif-studio/tests/test_studio.py:637`

#### UI-12 · واجهة منتج على Canvas بدالة draw(t) · Canvas product UI draw(t) recipe · ✅ مُثبت هنا / proven here
- **ماذا / what:** شاشة تصعد، بطاقات تتتابع كل 50 ms، مؤشر يقطع 560 ms بقوس، وزر ينضغط 80 ms ويتحرر 140 ms — كله دالة نقية للزمن. — Screen rises, cards stagger 50 ms apart, a cursor arcs in 560 ms, the button presses 80 ms and releases 140 ms — all a pure function of time.
- **متى أستخدمها / when:** عرض واجهة سريع بلا مكتبات، أو 9:16 للريلز — a dependency-free UI demo, also 9:16.
- **كيف / how:** Copy the playbook block into starters/html-canvas and render: node tools/render_html.cjs --in index.html --out film.mp4 --width 1080 --height 1920 --fps 30 --mode seek. Rendered here: 120 frames, VERIFY OK. Lesson from the frames: the 23 px arrow is tiny at 1080 wide — scale the cursor ×1.5–2 for phone-sized output. **أرقام / params:** bg #0b0d12, panel #161a23, cards #1f2430, button #19c37d; push 1.00→1.05 over 4 s; screen rise 48 px in 0.52 s expoOut
- **الدليل / proof:** `kosif-tool/playbooks/product-ui.md:163-203` · `kosif-tool/tools/render_html.cjs` · `kosif-tool/starters/html-canvas/index.html`

#### UI-13 · تصميم حركة المؤشر · Cursor choreography rules · 📄 موصوف / documented only
- **ماذا / what:** يظهر عند القرار، يسير بسرعة شبه ثابتة على منحنى ناعم، يستقر على الهدف 200–400 ms ثم يضغط. — Appears only for decisions, glides at near-constant speed on a smooth curve, dwells 200–400 ms on target, then presses.
- **متى أستخدمها / when:** تخطيط مسار أي مؤشر — planning any cursor path.
- **كيف / how:** Plan waypoints per beat; interpolate with Catmull-Rom + arc-length so speed is constant; the tip (not the arrow's centre) lands on the hit target; hold through the pressed state; the UI response is visible before the cursor moves on. First appearance glides in from a short offset (−140, +90 px). Check tip-on-target in stills. Arrow for desktop scenes, translucent tap circle on phones — never an arrow on a phone. **أرقام / params:** glide ~450 ms per hop (380–700 ms cubic-bezier(.2,.8,.2,1)); dwell 200–400 ms; arrow 22–26 px with 1.5 px outline; tap circle 40–48 px at 25–35% opacity
- **الدليل / proof:** `kosif-atlas/skills/101-video-skills/217-silent-product-demo` · `kosif-tool/playbooks/product-ui.md:20` · `kosif-tool/playbooks/product-ui.md:152` · `kosif-tool/styles/saas-demo/SKILL.md`

#### UI-14 · حلقة الضغط والتموج · Press ring & click ripple · 🟢 جاهز / ready
- **ماذا / what:** عند النقرة تنكمش الحلقة من المؤشر وتتلاشى، أو تنطلق موجتان صغيرتان. — On click a ring scales out from the tip and fades, or two small ripples release.
- **متى أستخدمها / when:** كل نقرة تحتاج تأكيدًا مرئيًا — every click that needs a visible confirmation.
- **كيف / how:** Inject a fixed-position div so the ring is captured in frames; element.animate keyframes scale 0.45→1.25, opacity 1→0, 420 ms ease-out. The ripple element exists in the DOM from t=0 at opacity 0 (no creation mid-render). Product-UI style: ripple 0→48 px in 320–400 ms; phone tap ripple 0→64 px, opacity 0.6→0 over 300 ms. **أرقام / params:** ring 0.45→1.25 / 420 ms; ripple 48 px desktop, 64 px phone
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3903-video/scripts/record-page.mjs` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/cursor-click-ripple.md` · `kosif-tool/styles/ui-micro/SKILL.md` · `kosif-tool/playbooks/phone.md:36`

#### UI-15 · مؤشر ماك معبّر يتجه مع حركته · Expressive directional macOS cursor · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** سهم أسود بحد أبيض يدور نحو اتجاه السرعة، يكبر عند المرور وينكمش عند الضغط، والكاميرا تقترب من النقرة. — Black arrow with white outline that rotates toward its velocity, grows on hover, shrinks on press while the camera zooms toward the click.
- **متى أستخدمها / when:** عروض ماك/ويب فاخرة — premium Mac/web demos.
- **كيف / how:** Rotation lerps toward atan2(vy, vx); decelerating glide; hover scale 1.55; press −15% for 3 frames; 32×39 px arrow with soft shadow. The 'oversized cursor' variant draws a 3.5× macOS arrow that lands, clicks and settles below the control. **أرقام / params:** hover ×1.55; press −15% / 3 f; arrow 32×39 px
- **الدليل / proof:** `style:pm-notdwd-7de38a` · `style:pm-notdwd-c2037d` · `kosif-one/vendor/hyperframes/registry/components/oversized-cursor/oversized-cursor.html`

#### UI-16 · مؤشر بهالة لونية يلاحق هدفًا متحركًا · Cursor with accent halo homing on a live target · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** المؤشر يعيد حساب موضع الهدف كل إطار والكاميرا تنجرف، مع دائرة شفافة خلفه تنبض عند النقر. — The arrow re-reads the live element position every frame while the camera drifts; a translucent accent halo pulses on click.
- **متى أستخدمها / when:** عندما تتحرك الكاميرا أثناء النقر — when the camera keeps moving during clicks.
- **كيف / how:** Every frame read the target's transformed rect and steer toward it (no stale coordinates). Halo #f0442c at 40% alpha, 36 px; on click it shrinks and pulses 150 ms while the target shows its pressed state. **أرقام / params:** halo 36 px 40% alpha; pulse 150 ms
- **الدليل / proof:** `style:pm-antonio-kodheli-490109`

#### UI-17 · المؤشر المغناطيسي · Magnetic cursor & magnetic buttons · 📦 بأمر تثبيت / one install
- **ماذا / what:** نقطة ناعمة تنجذب إلى الأزرار وتتحول إلى لوحة التمرير، والأيقونات تميل نحوها. — A soft dot is pulled into buttons, morphing into their hover plate while icons lean toward it.
- **متى أستخدمها / when:** عروض أدوات وتطبيقات حديثة — modern tool and app demos.
- **كيف / how:** HyperFrames component magnetic-cursor (vars visits '0,3', press 2, accent #3b82f6, tone light|dark). Hand-built rule: element offset = (cursor − centre) × factor, tween 0.3 s power2.out; leave → elastic.out(1,0.5) 0.5 s. Drive it from the scripted cursor path, never from a real mouse. **أرقام / params:** buttons factor 0.3, cards 0.1; return 0.5 s elastic.out(1,0.5)
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/magnetic-cursor/magnetic-cursor.html` · `kosif-atlas/skills/3438-ux-design/14124-top-design/references/animation-patterns.md`
- **📦 تثبيت / install:** `npx hyperframes add magnetic-cursor`
- **⚖️ ترخيص / license:** مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT).

#### UI-18 · سحب وإفلات · Cursor drag & drop · 📦 بأمر تثبيت / one install
- **ماذا / what:** المؤشر يمسك بطاقة، يرفعها ويميلها، يحملها لعمود فارغ، يفلتها فتستقر وتغلق القائمة الفجوة. — The cursor grabs a card, lifts and tilts it, carries it to an empty column and drops it while the list closes the gap.
- **متى أستخدمها / when:** كانبان، ترتيب مهام، رفع ملفات — kanban, task ordering, uploads.
- **كيف / how:** Grab = press dip + lift; the ghost travels on tweens matched to the cursor (same position, duration, ease; immediateRender:false); drop = snap with selection chrome. Variants: fill-handle and corner-resize. HyperFrames component cursor-drag-drop (card_label, accent #0a84ff, tone light|dark). **أرقام / params:** matched tweens; drop settle spring
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/cursor-drag.md` · `kosif-one/vendor/hyperframes/registry/components/cursor-drag-drop/cursor-drag-drop.html`
- **📦 تثبيت / install:** `npx hyperframes add cursor-drag-drop`
- **⚖️ ترخيص / license:** مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT).

#### UI-19 · تحديد نص ومستطيل وقائمة يمين · Text select, marquee select & context menu · 📦 بأمر تثبيت / one install
- **ماذا / what:** السهم يصير I-beam ويحدد نصًا ثم يضغط Bold؛ أو يسحب مستطيل تحديد على شبكة صور؛ أو يفتح قائمة نقر أيمن. — The arrow becomes an I-beam and selects text then clicks Bold; or drags a marquee over a photo grid; or blooms a right-click menu.
- **متى أستخدمها / when:** عروض محررات ومديري ملفات — editor and file-manager demos.
- **كيف / how:** HyperFrames components: cursor-text-select (title, text, phrase, accent), cursor-marquee-select (start/end x,y in %, each touched tile rings and checks while a pill counts), cursor-context-menu (items list, pick index, the menu blooms from the cursor tip). For Arabic text select by whole words, never split letters. **أرقام / params:** positions in % of frame
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/cursor-text-select/cursor-text-select.html` · `kosif-one/vendor/hyperframes/registry/components/cursor-marquee-select/cursor-marquee-select.html` · `kosif-one/vendor/hyperframes/registry/components/cursor-context-menu/cursor-context-menu.html`
- **📦 تثبيت / install:** `npx hyperframes add cursor-text-select`
- **⚖️ ترخيص / license:** مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT).

#### UI-20 · مؤشرات متعاونين بأسمائها · Named multiplayer cursors · 📦 بأمر تثبيت / one install
- **ماذا / what:** 2–4 مؤشرات ملونة بأسماء تعمل على لوحة واحدة بنبضات متناوبة. — 2–4 coloured, named cursors work one canvas on alternating beats.
- **متى أستخدمها / when:** إظهار التعاون الحي — showing live collaboration.
- **كيف / how:** Partition the canvas into zones so paths never cross; actions on alternating beats (~1.2 / 2.6 / 4.0 s); legs power2.inOut; press scale 0.88 for 0.07 s yoyo; one payoff at a time. Name tags are pills (radius 999) in each user's colour. Components: multiplayer-cursors (cursorCount 2–6, labels). **أرقام / params:** beats 1.2/2.6/4.0 s; press 0.88 / 0.07 s
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/multi-cursor-choreography.md` · `kosif-one/vendor/hyperframes/registry/components/multiplayer-cursors/multiplayer-cursors.html` · `style:pm-kikelopezdesign-7cc9e8` · `style:pm-sachaarbonel-8f14f4`
- **📦 تثبيت / install:** `npx hyperframes add multiplayer-cursors`
- **⚖️ ترخيص / license:** مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT).

#### UI-21 · مؤشر وكيل ذكي · AI agent cursor · 📦 بأمر تثبيت / one install
- **ماذا / what:** مؤشر يحمل اسم وكيل يمر على قائمة خطوات، يكتب اسم كل خطوة، يحلّق حول كل هدف وينتهي بعلامة صح. — A named agent pointer walks a list of steps, types each step label, rings each click target and ends on a check.
- **متى أستخدمها / when:** عروض وكلاء الذكاء الاصطناعي — AI-agent product films.
- **كيف / how:** Component agent-cursor: agent_name, steps 'Reading the page,Opening Settings,…', targets 'x,y;x,y' in %, accent #0a84ff; extra duration becomes hold, never time-stretch. Render with npx hyperframes render — tested here: rendering its demo.html with render_html --mode virtual gives a frozen frame, because the paused window.__timelines and data-composition-src need the HyperFrames runtime. **أرقام / params:** targets as % pairs
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/agent-cursor/agent-cursor.html` · `kosif-one/vendor/hyperframes/registry/components/agent-cursor/demo.html`
- **📦 تثبيت / install:** `npx hyperframes add agent-cursor`
- **⚖️ ترخيص / license:** مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT).

#### UI-22 · مؤشر اللمس على الهاتف · Touch indicator: tap & swipe · 📦 بأمر تثبيت / one install
- **ماذا / what:** دائرة تلامس شفافة تلمس الزجاج على إطار الاستجابة، نقرًا أو سحبًا. — A translucent contact circle touches the glass on the response frame, as tap or swipe.
- **متى أستخدمها / when:** كل تفاعل داخل هاتف — every phone interaction.
- **كيف / how:** Cue 60 ms before the press; press 90 ms cubic-bezier(0.4,0,1,1) with device 0.96 and button 0.92; release spring {stiffness 240, damping 14}; ripple 0→64 px, 0.6→0 opacity over 300 ms. Components: touch-indicator (gesture tap|swipe, polarity), gesture-tap (Follow → Following), swipe-rail (momentum carry, snap), pull-to-refresh (rubber band, pullDistance 120). **أرقام / params:** circle 40–48 px; press 90 ms; ripple 64 px / 300 ms
- **الدليل / proof:** `kosif-tool/playbooks/phone.md:36` · `kosif-tool/playbooks/phone.md:59-68` · `kosif-one/vendor/hyperframes/registry/components/touch-indicator/touch-indicator.html` · `kosif-one/vendor/hyperframes/registry/components/swipe-rail/swipe-rail.html`
- **📦 تثبيت / install:** `npx hyperframes add touch-indicator`
- **⚖️ ترخيص / license:** مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT).

#### UI-23 · ضغط اختصار لوحة المفاتيح · Keycap shortcut trigger · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** ثلاثة أزرار مفاتيح تنضغط بالتتابع، والأخير يمتلئ بلون التمييز ويطلق الحركة التالية. — Three rounded keycaps press in sequence; the last fills with the accent and triggers the next animation.
- **متى أستخدمها / when:** إظهار اختصار أو أمر سريع — showing a shortcut or quick command.
- **كيف / how:** Each key: translateY 3 px + shadow shrink for 120 ms, 80 ms gap; last key fill accent then cut. Pair with a command palette (UI-30). **أرقام / params:** 120 ms per key; 80 ms gap
- **الدليل / proof:** `style:pm-agonaliu-466a8f`

#### UI-24 · تحكم وهدف يتغيران معًا · Control ↔ target live sync · 📄 موصوف / documented only
- **ماذا / what:** منزلق أو حقل يتغير والسطح المرتبط به يتغير في النبضة نفسها. — A scrubbed or typed control and its bound target change in the same beat.
- **متى أستخدمها / when:** محررات الإعدادات والألوان — inspector, settings and colour editors.
- **كيف / how:** Readout tween and target transform share one label, duration and ease (tl.addLabel('edit1'), shared SCRUB_DUR/SCRUB_EASE). While dragging, the control value is derived from cursor x; on release it springs to rest. Seen variants: settings sliders that move when the narration names them (knob 500 ms ease-in-out, inactive label 40% grey) and an accent swatch ring hopping every 350 ms while the whole UI recolours. **أرقام / params:** knob 500 ms; swatch hop 350 ms
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/control-target-sync.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints/panel-edit-live-sync.md` · `style:pm-rossaxbt-3085b7` · `style:pm-iammxfschr-d68f90`

## الكتابة والطلبات ومسرح الذكاء — Typing, prompts & AI-agent theater

_أكثر مشهد مطلوب في 2026: طلب يُكتب، زر يُضغط، ووكيل يعمل أمامك خطوة بخطوة._

#### UI-25 · كتابة بإيقاع بشري · Human-rhythm typing with caret · 🟢 جاهز / ready
- **ماذا / what:** حروف تظهر بإيقاع شبه بشري مع مؤشر كتابة يومض، ومُحددة بالبذرة لا بالعشوائية. — Characters appear on a near-human rhythm with a blinking caret, seeded rather than random.
- **متى أستخدمها / when:** أي حقل بحث أو دردشة أو طرفية — any search, chat or terminal field.
- **كيف / how:** reveal = text.slice(0, floor(t·cps)) with a 1-frame hold every 2–3 chars from a seeded pattern (no Math.random in renders). Caret blink 500–530 ms (2 Hz), always visible while typing. Speeds: prompts 35–50 ms/char, terminals 35–45, human forms 70 ms ±20, search ~12 cps. Arabic: cut at grapheme clusters with Intl.Segmenter. motion-kit typeOn (cps 46) is rendered and proven in UI-11. **أرقام / params:** 35–50 ms/char prompts; 70 ±20 ms forms; caret 500–530 ms

```js
// seeded human typing: ~1 char/frame, a 1-frame pause every 2–3 chars
function typed(text, t, fps = 30, seed = 7) {
  const segs = [...new Intl.Segmenter('ar', {granularity: 'grapheme'}).segment(text)].map(s => s.segment);
  let f = Math.floor(t * fps), n = 0, s = seed;
  while (f-- > 0 && n < segs.length) { s = (s * 16807) % 2147483647; if (s % 3) n++; }
  return segs.slice(0, n).join('');
}
```

- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:193` · `kosif-tool/playbooks/product-ui.md:104-116` · `style:pm-notdwd-c2037d` · `style:product`

#### UI-26 · طلب يُكتب ثم يُرسل ثم يولّد · Prompt type → submit → generate · 📄 موصوف / documented only
- **ماذا / what:** طلب يُكتب في حقل حقيقي، المؤشر يضغط إرسال، ثم تجيب الآلة: حالة تحميل ← إجابة متدفقة أو ناتج. — A prompt types into a real input, the cursor presses send, and the machine answers: status theater → streaming answer or artifact.
- **متى أستخدمها / when:** إعلانات أدوات الذكاء الاصطناعي — AI-tool ads and intros.
- **كيف / how:** Blueprint prompt-type-submit-generate (5.2–12 s). Type ~35–50 ms/char with caret, send = button scale 0.9 + accent ring pulse 300 ms, then a thin progress bar fills ~1 s while a tile grid resolves tile by tile, or the result fades/scales in full-frame. Seen: centred 600×48 px pill on a dark frame; gradient-rim glowing search pill (1.5 px conic pink→violet→blue border + blurred copy below, blur 24 px at 0.35). **أرقام / params:** blueprint 5.2–12 s; ring 300 ms; progress ~1 s
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints/prompt-type-submit-generate.md` · `style:pm-listudio-820c7b` · `style:pm-influencer-seo-ce8c33` · `style:pm-lester-tyy-f897f7`

#### UI-27 · وكيل ينجز قائمة مهام · Agent progress theater & tool-call checklist · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** رسالة المستخدم ← خطة الوكيل ← صفوف أدوات تدور ثم تتحول لعلامة صح بالتتابع ← بطاقة جاهزة. — User bubble → agent plan → tool-call rows spin then turn into checks in sequence → 'Ready' card.
- **متى أستخدمها / when:** عروض الوكلاء والأتمتة — agent and automation films.
- **كيف / how:** Rows (mono 11–13 px, 'namespace · function') appear 250–600 ms apart; each spinner becomes a green check #2bb673 with a 0.6→1 scale pop; footer counters tick; optional terminal pane types output alongside. Status words can swap first (Queued → Reading → Drafting → Done) with HyperFrames state-chip-rail. Blueprint agent-progress-theater (4.2–11.6 s). **أرقام / params:** ticks 250–600 ms apart; check pop 250 ms
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints/agent-progress-theater.md` · `style:pm-ddryo-loos-300829` · `style:pm-majorbaguette-fb11d7` · `style:pm-bizibeast-10f264` · `style:pm-listudio-820c7b`

#### UI-28 · محادثة: فقاعات وكتابة جارية · Chat thread, bubbles & typing dots · 📦 بأمر تثبيت / one install
- **ماذا / what:** مشهد مراسلة كامل: شريط حالة، اسم جهة الاتصال، فقاعات بذيل، علامة استلام، رموز، بطاقة رابط ونقاط كتابة. — A full messaging scene: status bar, contact pill, tailed bubbles, receipt, emoji, link card and typing dots.
- **متى أستخدمها / when:** إعلانات قصص المحادثة وQ&A — chat-story ads and Q&A beats.
- **كيف / how:** Components chat-thread (messages 'recv:…|sent:…|card:title~domain|emoji:…', beat 1.7 s), chat-message (entry scale 0.75 in 0.12 s from the sender corner), typing-indicator (three dots, vanish when the message lands). Hand-built: bubbles slide y+12 and fade, alternate sides, stagger 500 ms; Q&A answer bubble 300 ms back.out. Arabic: received bubbles on the left, sent on the right in RTL apps — mirror the tail. **أرقام / params:** beat 1.7 s; bubble 0.12 s from 0.75
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/chat-thread/chat-thread.html` · `kosif-one/vendor/hyperframes/registry/components/chat-message/chat-message.html` · `kosif-one/vendor/hyperframes/registry/components/typing-indicator/typing-indicator.html` · `style:pm-fractadev-149adc`
- **📦 تثبيت / install:** `npx hyperframes add chat-thread`
- **⚖️ ترخيص / license:** مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT).

#### UI-29 · طرفية ومحرر كود · Terminal & IDE scenes (24 theme blocks) · 📦 بأمر تثبيت / one install
- **ماذا / what:** نافذة طرفية بأضواء المرور وموجه ~ $ وحروف تُكتب ومؤشر كتلة، أو محرر VS Code كامل بثيماته. — A terminal window with traffic lights, a '~ $' prompt, typed characters and a block cursor — or a full VS Code workbench in its themes.
- **متى أستخدمها / when:** افتتاح بأمر، عروض مطورين، فرق الكود — cold opens, developer demos, code diffs.
- **كيف / how:** 24 ready ~11–12 s blocks: VS Code (12 themes: dark-plus, light-plus, dark-modern, monokai, solarized-light…) with per-char typing and a pytest terminal, or macOS Terminal.app (12 profiles). Edit codeLines. Hand-built: 35–45 ms/char, block cursor in the accent colour, blink 500 ms. Diff rows: old line struck through grey (strike draw 250 ms), new line types in orange, rows 1.2 s apart. **أرقام / params:** 24 themes; 35–45 ms/char
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/code-snippet-dark-modern` · `kosif-one/vendor/hyperframes/skills/pr-to-video/references/code-vocabulary.md` · `style:pm-viktoroddy-98c1d8` · `style:plotter`
- **📦 تثبيت / install:** `npx hyperframes add code-snippet-dark-modern`
- **⚖️ ترخيص / license:** مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT).

#### UI-30 · لوحة أوامر وبحث يصفّي النتائج · Command palette & search filter · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** حقل بحث يُكتب فيه، صفوف النتائج تنزلق، الصف الأول مميز، وEnter يتحول لإشعار. — Characters type into a search field, result rows slide in, the first row highlights and Enter collapses into a toast.
- **متى أستخدمها / when:** إظهار السرعة والبحث — speed and search features.
- **كيف / how:** ~70 ms per char (or one char per beat subdivision on music); rows fade/slide 12 px in 250 ms; non-matching rows fade to 30% and collapse in 400 ms; matches move up with a yellow keyword highlight and a '1 result' label. **أرقام / params:** 70 ms/char; filter 400 ms
- **الدليل / proof:** `style:pm-twoclipping-5cba86` · `style:pm-mehul4795-4a7007` · `style:pm-brainextends-e19ac3` · `style:pm-agonaliu-466a8f`

#### UI-31 · إجابة متدفقة وسجل حي · Streaming answer & live log · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** الإجابة تظهر سطرًا سطرًا، أو سجل أحادي الخط تُضاف إليه سطور بوسوم ملونة. — The answer appears line by line, or a mono log appends rows with coloured verb tags.
- **متى أستخدمها / when:** إظهار العمل الجاري — showing work in progress.
- **كيف / how:** Bullet lines every ~120 ms after the question bubble. Live log: dark card radius 16 px, green live dot, mono endpoint rows with ✓ and '200' appended every ~120 ms; verb tags OBSERVE/CLICK/SCROLL. Skeleton reply: 3 grey bars (30 px high, 40–70% wide) grow to imply loading. **أرقام / params:** lines ~120 ms; card radius 16 px
- **الدليل / proof:** `style:pm-wani-shola-16ca7a` · `style:pm-0xfemyn-e114d3` · `style:pm-hqmank-7c61f1` · `style:pm-kloss-xyz-15182a`

#### UI-32 · كتابة في تطبيق الملاحظات · Notes-app typing story · 📦 بأمر تثبيت / one install
- **ماذا / what:** عنوان عريض ثم سطور تُكتب بإيقاع ضربات مقاس، والصفحة تتمرر لكل سطر ثم قطع إلى بطاقة ورقية. — A bold title then body lines typed on a measured keystroke rhythm, the page scrolling per line, then a cut to a paper card.
- **متى أستخدمها / when:** قصص «أشياء لم يخبرني بها أحد» — confessional / list stories.
- **كيف / how:** Component notes-typing (lines 'a|b|c', speed 0.5–2) and the 24.85 s 1080×1920 block notes-reveal (Courier Prime + Permanent Marker). Arabic version: swap the fonts for Arabic faces and type by grapheme. **أرقام / params:** speed 0.5–2; block 24.85 s 9:16
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/notes-typing/notes-typing.html` · `kosif-one/vendor/hyperframes/registry/blocks/notes-reveal/notes-reveal.html`
- **📦 تثبيت / install:** `npx hyperframes add notes-reveal`
- **⚖️ ترخيص / license:** مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT).

## حركات الواجهة الدقيقة — Micro-interactions & UI components

_جدول الأزمنة الذي يجعل الواجهة تبدو حقيقية: ضغط، تبديل، نجاح، خطأ، تحميل، إشعار._

#### UI-33 · جدول ردود الفعل الدقيقة · Micro-feedback timing table · 📄 موصوف / documented only
- **ماذا / what:** أزمنة دقيقة لكل لحظة: ضغط، مرور، تبديل، فتح، إشعار، درج، هيكل، علامة صح، اهتزاز خطأ. — Exact timings for press, hover, toggle, expand, toast, drawer, skeleton, success check, error shake.
- **متى أستخدمها / when:** مرجعك قبل تحريك أي عنصر واجهة — your reference before animating any control.
- **كيف / how:** CSS transitions or WAAPI; the error shake is keyframes on x. Animate only transform and opacity (plus colour), never width/height in renders. **أرقام / params:** press scale 0.97–0.98 in 50–100 ms; hover 1.02; toggle 150–250 ms; expand 200–300 ms; fade 150–300 ms; drawer in 300 / out 250; modal 250 ms .95→1 (out 200); skeleton→content 200–400 ms; check draw 300–500 ms; shake x [0,−10,10,−10,10,0] 0.4 s; arrival bounce spring 200–400 ms
- **الدليل / proof:** `kosif-atlas/skills/3438-ux-design/14121-microinteractions/references/feedback-patterns.md` · `kosif-atlas/skills/3529-ui-design/14308-interaction-design/references/microinteraction-patterns.md` · `kosif-tool/styles/ui-micro/SKILL.md`

#### UI-34 · ضغط ومرور بمنطق القراءة · Press & hover with reading-direction nudges · 🟢 جاهز / ready
- **ماذا / what:** الأزرار تنخفض وتنكمش قليلًا عند الضغط وترتفع عند المرور، والأيقونات تدفع باتجاه القراءة. — Buttons press down and shrink, lift on hover, and inline icons nudge in the reading direction.
- **متى أستخدمها / when:** واجهات عربية مصقولة — polished Arabic UIs.
- **كيف / how:** active: translateY(1px) scale(.985), svg scale(.92); hover (only under @media (hover:hover) and (pointer:fine)): translateY(−1px); inline-end icon translateX(−3px), inline-start 2px; icon action rotate(−7deg) scale(1.06); metric cards lift −2px with icon rotate(−4deg). Transition only colour, background, border, shadow, transform, opacity at 150 ms ease-out. Touch targets ≥ 44 px. **أرقام / params:** 150 ms ease-out; press .985; touch ≥ 44 px
- **الدليل / proof:** `kosif-audit-pro/app/globals.css:215` · `kosif-audit-pro/app/globals.css:223` · `kosif-audit-pro/app/globals.css:1256`

#### UI-35 · ضغط وتحرير زر نابض · Press-release spring button · 📄 موصوف / documented only
- **ماذا / what:** انضغاط خطي ثم ارتداد نابض على الخاصية نفسها، مع انكماش الظل ودفقة وتوهج خلفي. — Linear compression then spring recovery on the same property, with shadow shrink, release burst and background glow.
- **متى أستخدمها / when:** زر الـ CTA البطل — the hero CTA press.
- **كيف / how:** Press linear scale 1 → PRESS_SCALE (~0.9) power1.in while the cursor compresses with it; release back.out(BOUNCE). Product-UI tokens: press 80 ms, release 140 ms spring k300 d20; the showreel pill flattens into a progress bar (scaleX 2.0 / scaleY .24 in .34 s) that fills linearly 1.1 s while a counter climbs. **أرقام / params:** press 80 ms; release 140 ms spring 300/20
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/press-release-spring.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/physics-press-reaction.md` · `kosif-studio/motion/projects/showreel/index.html:78`

#### UI-36 · قلب المفتاح وتبديل الثيم · Toggle flip & theme switch · 📦 بأمر تثبيت / one install
- **ماذا / what:** مفتاح كبير يقلب مع تجاوز الإبهام وتلاشي لون المسار؛ أو تبديل الثيم يصبح حدثًا بصريًا. — An oversized toggle flips with thumb overshoot and a track-colour crossfade; or a theme switch becomes the event.
- **متى أستخدمها / when:** إظهار إعداد أو وضع داكن — showing a setting or dark mode.
- **كيف / how:** Component toggle-flip (direction on|off, label, size 20–70). Theme switch: segmented thumb slides 300 ms easeOutCubic then the whole palette crosses cream → chocolate; sun/moon icon orbits in from 75° at .72 scale over 260 ms spring. Gag variant: 'FULL BODY MODE ON' toggle 250 ms while the frame zooms out 400 ms. **أرقام / params:** thumb 300 ms; icon orbit 260 ms from 75°
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/toggle-flip/toggle-flip.html` · `kosif-audit-pro/app/globals.css:403` · `style:pm-thilina-a-891c09` · `style:pm-sab8a-364a5a`
- **📦 تثبيت / install:** `npx hyperframes add toggle-flip`
- **⚖️ ترخيص / license:** مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT).

#### UI-37 · من التحميل إلى علامة صح · Spinner → success check · 📦 بأمر تثبيت / one install
- **ماذا / what:** قوس يدور ثم ينكمش لدائرة وترسم علامة صح بخطها، مع نبضة حلقة. — A rotating arc collapses into a circle and a check draws by its stroke, with a ring pop.
- **متى أستخدمها / when:** نهاية أي فعل ناجح — the end of any successful action.
- **كيف / how:** Arc rotation 0.8 s → collapse → stroke-dashoffset check draw 250 ms (300–500 ms for hero checks). Component success-check (tint, ring subtle|standard|bold, spin). Pair with a toast or a 'Saved' label swap. **أرقام / params:** spinner 0.8 s; check 250–500 ms
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/success-check/success-check.html` · `style:pm-demonugc-4c5753`
- **📦 تثبيت / install:** `npx hyperframes add success-check`
- **⚖️ ترخيص / license:** مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT).

#### UI-38 · حقل إدخال: خطأ واهتزاز ونجاح · Input feedback: error shake & valid state · 📦 بأمر تثبيت / one install
- **ماذا / what:** حقل يهتز عند الخطأ، يعرض اقتراح تصحيح، ثم يتحول حده للأخضر. — A field shakes on error, offers a 'Did you mean…?' pill, then its border turns green.
- **متى أستخدمها / when:** عروض النماذج والتحقق — form and validation demos.
- **كيف / how:** Form recipe: focus ring, type 16 chars at 70 ms ±20, tick 240 ms, focus jumps on spring 170/20, submit, spinner crossfade 120 ms, toast spring 200/22 held ~2 s. Component input-feedback (status valid|error). Suggestion flow: type 45 ms/char, cursor clicks the pill, border colour change 200 ms. **أرقام / params:** shake 0.4 s; tick 240 ms; toast hold ~2 s
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/input-feedback/input-feedback.html` · `kosif-tool/playbooks/product-ui.md:104-116` · `style:pm-kmasiff-cc72cb`
- **📦 تثبيت / install:** `npx hyperframes add input-feedback`
- **⚖️ ترخيص / license:** مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT).

#### UI-39 · هيكل لامع يتحول إلى محتوى · Skeleton shimmer → content · 📦 بأمر تثبيت / one install
- **ماذا / what:** عناصر رمادية يمر عليها ضوء مائل ثم تتلاشى إلى المحتوى الحقيقي. — Grey placeholders with a diagonal light sweep crossfade into real content.
- **متى أستخدمها / when:** لحظة التحميل الصادقة — an honest loading beat.
- **كيف / how:** Shimmer = moving linear-gradient 30% wide, 1.2–1.5 s loop; reveal crossfade + slight scale-in 200–400 ms per block. Loading ladder by wait: < 0.3 s nothing; 0.3–1 s inline spinner; 1–5 s skeleton; 5–30 s determinate bar; > 30 s bar + % + ETA; a blank 600–800 ms reads as broken. Component skeleton-reveal. **أرقام / params:** shimmer 1.2–1.5 s; reveal 200–400 ms
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/skeleton-reveal/skeleton-reveal.html` · `kosif-atlas/skills/3438-ux-design/14121-microinteractions/references/feedback-patterns.md` · `style:pm-justincooperman-e7bbc4`
- **📦 تثبيت / install:** `npx hyperframes add skeleton-reveal`
- **⚖️ ترخيص / license:** مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT).

#### UI-40 · إشعارات: نظام وجزيرة ورصّة · Notifications: native pop, dynamic island, stacks · 📦 بأمر تثبيت / one install
- **ماذا / what:** إشعار iOS/macOS يسقط بنابض، جزيرة ديناميكية تتمدد، أو رصّة إشعارات تتسارع حتى برج قلق. — An iOS/macOS banner drops on a spring, a dynamic island expands, or notifications pile faster into an anxious tower.
- **متى أستخدمها / when:** خطّاف البداية أو لحظة «تم» — the hook or the 'done' moment.
- **كيف / how:** Island: 120×36 → 300×80 on spring {stiffness 180, damping 16} ≈ 260 ms; content from 180 ms with 60 ms stagger; hold to 2.4 s; collapse 300 ms. Components native-notification-pop (os ios|macos, at 0.3 s), notification-stack (1–5 cards, newest on top, one grows as focus), notification-pileup (count 4–10, speed), badge-pop (elastic count). Blocks notification-cascade (14 s, 9:16) and slack-notification-ad (12 s). **أرقام / params:** island 260 ms spring 180/16; hold 2.4 s
- **الدليل / proof:** `kosif-tool/playbooks/phone.md:41` · `kosif-tool/playbooks/phone.md:89-96` · `kosif-one/vendor/hyperframes/registry/components/native-notification-pop/native-notification-pop.html` · `kosif-one/vendor/hyperframes/registry/components/notification-stack/notification-stack.html` · `kosif-one/vendor/hyperframes/registry/blocks/notification-cascade/notification-cascade.html`
- **📦 تثبيت / install:** `npx hyperframes add native-notification-pop`
- **⚖️ ترخيص / license:** مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT).

#### UI-41 · تحول بطاقة إلى لوحة (FLIP) · Shared-element morph: card → panel (FLIP) · 📦 بأمر تثبيت / one install
- **ماذا / what:** بطاقة صغيرة تصبح لوحة كاملة بالتحويل وحده، وأبناؤها يعوّضون المقياس ويعاد ترتيبهم. — A small card becomes a full panel by transform only; children counter-scale and reflow onto measured targets.
- **متى أستخدمها / when:** فتح تفاصيل، انتقال بين حالتين — opening details, moving between two states.
- **كيف / how:** Measure both layouts, animate transform (never width/height in renders), counter-scale children, crossfade content in 150 ms. Component modal-morph (expand_at 1.2 s, register calm|snappy), card-resize, panel-reveal, menu-morph (hamburger → menu). Single-element morph chain: one container whose width/height/radius/fill are springs retargeted every beat (stiffness ~300, damping ratio ~0.8). Edge-pinned growth uses mask + sheet slide or proxy scaleY with inverse counter-scale. **أرقام / params:** 400–700 ms easeInOutCubic; spring ~300 / ζ 0.8
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/modal-morph/modal-morph.html` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/anchored-layout-expand.md` · `style:pm-twoclipping-5cba86` · `style:pm-en-ra-81c6dd` · `style:pm-antonio-kodheli-490109`
- **📦 تثبيت / install:** `npx hyperframes add modal-morph`
- **⚖️ ترخيص / license:** مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT).

#### UI-42 · إعادة ترتيب قائمة وسطور · FLIP list reorder & self-reordering lines · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** البطاقات تنزلق لأماكنها الجديدة، أو سطور مستند تعيد ترتيب نفسها. — Cards slide to new slots, or document lines re-order themselves.
- **متى أستخدمها / when:** إظهار الترتيب الذكي أو الفرز — smart sorting or prioritising.
- **كيف / how:** FLIP 450 ms cubic-bezier(0.2,0.8,0.2,1), stagger 40–60 ms (45 ms cascade). Lines: spring 160/20 with 50 ms offsets; highlight wipe 180 ms with the colour switch at 50%. **أرقام / params:** 450 ms; stagger 40–60 ms
- **الدليل / proof:** `kosif-tool/styles/pm-melvynx-6cde6c/BRIEF.md` · `style:pm-thayto-dev-44b911`

#### UI-43 · مؤشرات التبويب والشريط النشط · Tab slide indicator & active rail bar · 🟢 جاهز / ready
- **ماذا / what:** كبسولة تنزلق بين التبويبات، وشريط رفيع ينمو بجانب العنصر النشط. — A pill slides between tabs; a thin bar grows beside the active nav item.
- **متى أستخدمها / when:** التنقل داخل التطبيق — in-app navigation beats.
- **كيف / how:** Rail: ::after 3 px bar scaleY(0.2)→1 on a 260 ms spring, opacity 160 ms; mobile bottom nav uses a top bar scaleX .25→1; icon lifts translateY(−2px) scale(1.06). Component tabs-slide-indicator (labels, shape pill|rounded|square). **أرقام / params:** spring 260 ms; opacity 160 ms
- **الدليل / proof:** `kosif-audit-pro/app/globals.css:527` · `kosif-audit-pro/app/globals.css:2765` · `kosif-one/vendor/hyperframes/registry/components/tabs-slide-indicator/tabs-slide-indicator.html`

#### UI-44 · شريط المراحل والحلقة والتقدم · Stepper, progress ring & progress bars · ✅ مُثبت هنا / proven here
- **ماذا / what:** عقد على خط يمتلئ وتتحول لعلامات صح، حلقة تقدم تدور، وشريط تقدم يساوي t/المدة. — Nodes on a line fill and turn into checks, a progress ring sweeps, and a progress bar equals t/duration.
- **متى أستخدمها / when:** خطوات عملية، رفع ملفات، شريط تقدم الفيلم نفسه — process steps, uploads, the film's own progress.
- **كيف / how:** Film progress bar in the tested starter: #progress width = t/DURATION × 100%, 14 px, #7ee8d2 (rendered in every proof film). Stepper: 5 circles (18 px) on a 3 px line that fills accent node to node, each node pops into a filled check ~150 ms; mono labels under each. Ring: SVG stroke-dashoffset 1200 ms with Arabic status labels crossfading 150 ms (expand 400 ms easeOutQuint). Segmented step bar: N thin 3 px rounded bars, active one fills linearly. Chips: Mono 21 px/700, radius 14, done = mint text, on = lime #d0ff6a with 34 px glow, bad = coral #ff907a. **أرقام / params:** bar 14 px #7ee8d2; node pop ~150 ms; ring 1200 ms
- **الدليل / proof:** `kosif-tool/starters/html-canvas/index.html:46` · `kosif-tool/starters/html-canvas/index.html:211` · `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/index.html:30` · `style:pm-kmasiff-cc72cb` · `style:isometric`

#### UI-45 · نقطة حالة بهالة وشارة مباشرة · Status dot with halo & live pill · 🟢 جاهز / ready
- **ماذا / what:** نقطة 8–9 بكسل بلون الحالة مع هالة ناعمة 4 بكسل، أو كبسولة «متصل» بنقطة نابضة. — An 8–9 px state-coloured dot with a soft 4 px halo, or an 'online' pill with a pulsing dot.
- **متى أستخدمها / when:** حالات مباشر/متوقف وبطاقات الأنظمة — live/stale states and system cards.
- **كيف / how:** ::before circle + box-shadow 0 0 0 4px <soft colour>; studio green #54d89c with rgba(84,216,156,.12) halo; verified teal, attention amber, default muted. Live pill: pale-green pill with dot pulse 1.2 s loop. **أرقام / params:** dot 8–9 px; halo 4 px; pulse 1.2 s
- **الدليل / proof:** `kosif-audit-pro/app/globals.css:855` · `kosif-audit-studio/styles.css:116` · `style:pm-jhylee95-e1152f`

#### UI-46 · لحظة احتفال توقيعية · Signature celebration moment · 💡 فكرة / idea
- **ماذا / what:** رد فعل مميز للعلامة (انفجار إعجاب، علامة صح مع قصاصات) على الفعل الأكثر ظهورًا. — A distinctive branded reaction (like-burst, check with confetti) on the most visible action.
- **متى أستخدمها / when:** لحظة «السحر» في فيلم المنتج — the magic-moment beat of a product film.
- **كيف / how:** One or two per product, always skippable; removal test: if nobody misses it, it is decoration. Build with seeded canvas particles (see PART) — canvas-confetti/tsparticles are installable but use your own seeded burst in renders. **أرقام / params:** 1–2 per product
- **الدليل / proof:** `kosif-atlas/skills/3438-ux-design/14121-microinteractions/references/signature-moments.md`

## الأجهزة والإطارات — Devices & frames

_هاتف واحد بارامتري يكفي أغلب الأفلام؛ المهم المنظور الصحيح وواجهة حية داخل الشاشة._

#### UI-47 · ثوابت الهاتف البارامتري · Parametric phone constants · 📄 موصوف / documented only
- **ماذا / what:** هاتف واحد بمقاس شاشة وزوايا متحدة المركز وإطار وجزيرة أو نوتش. — One parametric phone: screen size, concentric radii, bezel, island or notch.
- **متى أستخدمها / when:** كل مشهد هاتف — every phone scene.
- **كيف / how:** Screen 390×844 (19.5:9); screen radius 12–14% of width; bezel 2–3%; frame radius = screen radius + bezel; island 120×36 at 12 px from top; notch 210×34 r 20. The screen is clipped live DOM/SVG/Canvas at 2× density; island and home indicator painted after the UI; in-screen text ≥ 30 px, callouts ≥ 36 px; message text lives outside the device. **أرقام / params:** 390×844; radius 12–14% W; bezel 2–3%; island 120×36
- **الدليل / proof:** `kosif-tool/playbooks/phone.md:17` · `kosif-tool/playbooks/phone.md:19` · `kosif-tool/playbooks/phone.md:110`

#### UI-48 · منظور الجهاز وسرعة دورانه · Device perspective, rotation caps & idle hover · 📄 موصوف / documented only
- **ماذا / what:** مسافة منظور وحدود دوران، والهاتف لا يستقر أبدًا على 0°. — Perspective distance and yaw/pitch caps; the rest pose is never 0°.
- **متى أستخدمها / when:** أي ميل أو دوران للجهاز — any device tilt or turn.
- **كيف / how:** perspective 1200–1600 px (~1.3× width); yaw ±28°, pitch ±8°; rest yaw −6° to −10°. Rotation ≤ 40°/s for reveals, ≤ 4°/s idle; settle overshoot 1–2°; idle hover 6·sin(2πt/3.2) px (≤ 6 px, period ≥ 3.2 s). **أرقام / params:** yaw ±28°; pitch ±8°; ≤ 40°/s; hover ≤ 6 px / 3.2 s
- **الدليل / proof:** `kosif-tool/playbooks/phone.md:21` · `kosif-tool/playbooks/phone.md:34-35`

#### UI-49 · دخول الجهاز وكشف البطل · Device entrance & hero reveal · 📄 موصوف / documented only
- **ماذا / what:** الهاتف يصعد وزاويته تستقر، يمر انعكاس، تتتابع الواجهة، ثم العنوان ودفعة كاميرا. — The phone rises while yaw settles, a reflection passes, UI rows stagger in, then the headline and a slow push.
- **متى أستخدمها / when:** افتتاح فيلم تطبيق — opening an app film.
- **كيف / how:** Entrance 700–900 ms: rise 120–160 px, yaw −22°→−8°, opacity done by 250 ms; Remotion spring {damping 18, stiffness 90, mass 1.1} or cubic-bezier(0.16,1,0.3,1). Hero recipe (ms): 0–900 rise 140 px; 350–1550 reflection pass; 600–1300 UI rows 70 ms apart; 1200–1800 headline spring 14/120; 900–4000 push to 1.04 with yaw drift ±1.5°. Seen variants: rise from 40% below on black in 600 ms ease-out cubic; overshoot 1.08 in 700 ms with a 2 px squash land. **أرقام / params:** 700–900 ms; rise 120–160 px; yaw −22→−8°
- **الدليل / proof:** `kosif-tool/playbooks/phone.md:33` · `kosif-tool/playbooks/phone.md:49-57` · `style:pm-gautam-mer1-2ae354` · `kosif-tool/styles/pm-l3d1c-0e35a3/BRIEF.md`

#### UI-50 · هاتف 2.5D على Canvas · Canvas 2.5D phone (drawPhone) · 🟢 جاهز / ready
- **ماذا / what:** Canvas ثنائي الأبعاد يزيّف دوران الهاتف بضغط العرض cos(yaw) مع ميل خفيف، وظل وقص وجزيرة ولمعة. — 2D canvas fakes yaw by cos(yaw) width squash plus slight shear, with shadow, clip, screen canvas, island and glare.
- **متى أستخدمها / when:** هاتف بلا Three.js داخل starters/html-canvas — a phone without Three.js.
- **كيف / how:** ctx.transform(cos(rad), sin(rad)·0.12, 0, 1, 0, 0); roundRect clip; drawImage(screenCanvas); glare as a moving linear gradient. Valid below 28° yaw; above that use CSS 3D or a GLTF model. **أرقام / params:** PHONE 420×900 r 60 bezel 12; shadowBlur 90; yaw < 28°
- **الدليل / proof:** `kosif-tool/playbooks/phone.md:146-179` · `kosif-tool/starters/html-canvas/index.html`

#### UI-51 · مكوّن Device في Remotion · Remotion Device component · 📦 بأمر تثبيت / one install
- **ماذا / what:** هاتف React بنابض دخول وضغط ولمعة وظل معاكس للدوران وجزيرة. — A React phone with spring entrance, tap press, glare pass, yaw-opposed shadow and island overlay.
- **متى أستخدمها / when:** أفلام Remotion في starters/remotion — Remotion films.
- **كيف / how:** Inside CameraRig; uses easing.ts progress / easeOutExpo; perspective 1400; rotateX 4deg; glare progress over frames 10–36; R 52, BEZEL 12, frame #15171c. **أرقام / params:** perspective 1400; glare f10–36
- **الدليل / proof:** `kosif-tool/playbooks/phone.md:106-143` · `kosif-tool/starters/remotion/package.json`
- **📦 تثبيت / install:** `cd kosif-tool/starters/remotion && npm install`
- **⚖️ ترخيص / license:** Remotion برخصة الشركة: مجانية للأفراد والفرق الصغيرة، وتحتاج ترخيصًا للشركات الأكبر / Remotion company license — free for individuals and small teams, paid above that.

#### UI-52 · تسليم بين جهازين · Two-device turntable handoff · 📄 موصوف / documented only
- **ماذا / what:** الجهاز الأول يستدير وينزلق، الثاني يدخل، وعنصر مشترك يطير بينهما على قوس. — Device A turns away and slides, B enters, a shared element flies between them on an arc.
- **متى أستخدمها / when:** من الهاتف إلى الحاسوب، أو بين تطبيقين — phone → desktop, or app → app.
- **كيف / how:** A yaw −8°→+28° and slide 220 px; B +30°→+8°, scale 0.9→1 over 1400 ms cubic-bezier(0.65,0,0.35,1); specular pass 500–700 ms; shared element 700–1000 ms; settle with a 1.5° overshoot spring 16/100. Browser→phone morph alternative: one tween of width/height/radius in 600 ms with content reflowing, not scaling. **أرقام / params:** 1400 ms; shared element 700–1000 ms
- **الدليل / proof:** `kosif-tool/playbooks/phone.md:79-87` · `kosif-tool/styles/pm-deifosv-04e4d3/BRIEF.md`

#### UI-53 · نافذة متصفح أو ماك وهمية · Browser chrome & macOS frame mock · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** نافذة مستديرة بأضواء المرور وشريط رابط، أو شريط قوائم ماك بأيقوناته وخلفية متدرجة. — A rounded window with traffic-light dots and a URL pill, or a macOS menu bar with status icons over a gradient wallpaper.
- **متى أستخدمها / when:** عرض موقع أو تطبيق سطح مكتب — showing a website or desktop app.
- **كيف / how:** Window radius 12 px, shadow 0 20–30px 60px rgba(0,0,0,.12), slide up 20 px + fade 500 ms; inner grid scrolls 600 px over 3 s ease-in-out. macOS frame: black bezel band, navy menu bar ~60 px on a 1080 stage, three coloured dots, date/time. Component browser-device-stage (chrome browser|window|phone, screen slot with skeleton default, optional crossfade to a second screen at swap_at). **أرقام / params:** radius 12 px; slide 20 px / 500 ms
- **الدليل / proof:** `style:pm-ai-baymax-0ef9dd` · `style:pm-wani-shola-16ca7a` · `style:pm-notdwd-c2037d` · `kosif-one/vendor/hyperframes/registry/components/browser-device-stage/browser-device-stage.html`

#### UI-54 · مروحة أجهزة وانفراد الهواتف · Multi-device splay & phone fan-out · 📦 بأمر تثبيت / one install
- **ماذا / what:** هاتف وجهاز لوحي وحاسوب تنفرد من رصّة مركزية، أو هاتف واحد يتكاثر لخمسة كالمروحة. — Phone, tablet and desktop fan out from a centred stack, or one phone multiplies into five like a fan.
- **متى أستخدمها / when:** إظهار التوفر على كل المنصات — 'works everywhere' beats.
- **كيف / how:** Fan-out: duplicate into 5 phones translating outward with rotation ±6°/±12°, outer ones slightly lower and smaller, soft shadow, 600 ms spring, 40 ms stagger from the centre. Components multi-device-splay and device-frame-stage (phone|tablet, cutout none|island|notch, body graphite|silver, idle float). **أرقام / params:** rotate ±6/±12°; 600 ms; 40 ms stagger
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/multi-device-splay/multi-device-splay.html` · `kosif-one/vendor/hyperframes/registry/components/device-frame-stage/device-frame-stage.html` · `style:pm-samuel-yostt-891f87`
- **📦 تثبيت / install:** `npx hyperframes add multi-device-splay`
- **⚖️ ترخيص / license:** مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT).

#### UI-55 · آيفون وماك بوك ثلاثيا الأبعاد بشاشات حية · 3D GLTF iPhone & MacBook with live screens · 📦 بأمر تثبيت / one install
- **ماذا / what:** نماذج GLTF لآيفون وماك بوك مع شاشات HTML حية وعدسة زجاج وكاميرا مراجعة منتج ودوران 360. — GLTF iPhone 15 Pro Max and MacBook Pro with live HTML-in-Canvas screens, a glass lens, review-style camera moves and a 360 turntable.
- **متى أستخدمها / when:** إطلاق تطبيق فاخر — premium app launches.
- **كيف / how:** Blocks vfx-iphone-device (15 s), ios26-liquid-glass (15 s home screen with liquid-glass icons), macos-tahoe-liquid-glass (15 s). Engine: Three.js 0.147 from CDN + HTML-in-Canvas (canvas layoutsubtree + ctx.drawElementImage — an experimental Chromium API: verify it in this Chromium before promising) + GSAP paused timeline. **أرقام / params:** 15 s; 1920×1080
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/vfx-iphone-device/vfx-iphone-device.html` · `kosif-one/vendor/hyperframes/registry/blocks/ios26-liquid-glass/ios26-liquid-glass.html` · `kosif-one/vendor/hyperframes/registry/blocks/macos-tahoe-liquid-glass/macos-tahoe-liquid-glass.html`
- **📦 تثبيت / install:** `npx hyperframes add vfx-iphone-device`
- **⚖️ ترخيص / license:** مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT). Apple-style device models are look-alikes — never imply Apple endorsement.

#### UI-56 · موك أب HTML بلقطة 2× · HTML/CSS device & package mockup screenshot · 🟢 جاهز / ready
- **ماذا / what:** ضع الصورة داخل جهاز أو عبوة بظلال CSS والتقط بكثافة 2×. — Place an image inside a device or package with CSS shadows and capture at 2× DPR.
- **متى أستخدمها / when:** صور ثابتة للغلاف أو بطاقة نهاية — covers and end cards.
- **كيف / how:** Playwright page.screenshot with deviceScaleFactor 2 (Playwright + Chromium installed here). The KOSIF approved mockups (iMac dashboard, four iPhones on a stone plinth, audit laptop, 1448×1086 WebP) are the visual reference for Arabic RTL product composites: navy rail, white cards, blue/green bars. **أرقام / params:** 2× DPR; reference 1448×1086
- **الدليل / proof:** `100-superskills/skills/product-photo-mockups/SKILL.md:24` · `kosif-earth-ci-fork/docs/design/mockups/kosif-iphone.webp` · `kosif-earth-ci-fork/docs/design/mockups/kosif-laptop-dashboard.webp`

#### UI-57 · قلب الهاتف وتبديل الشاشة · Phone flip with mid-swap · 💡 فكرة / idea
- **ماذا / what:** الهاتف ينقلب 180° وتتبدل الشاشة عند 90°. — The phone flips 180° and swaps its screen at 90°.
- **متى أستخدمها / when:** قبل/بعد على الجهاز نفسه — before/after on the same device.
- **كيف / how:** CSS 3D rotateY 700 ms; swap content exactly at the 90° frame (backface hidden); keep tilt ≤ ±8° on the other axis. **أرقام / params:** 700 ms; swap at 90°
- **الدليل / proof:** `kosif-tool/styles/pm-cansincengiz-me-cf68dd/BRIEF.md`

## الشاشات والتمرير والكاميرا على الواجهة — Screens, scroll & camera on UI

_الكاميرا تتحرك نحو الفعل ثم تستقر؛ التمرير بخطوات؛ والشرح يخرج من العنصر لا من الفراغ._

#### UI-58 · جولة تمرير مع شروحات · Scroll tour with callouts · 📄 موصوف / documented only
- **ماذا / what:** شرح يُرسم، توقف، ثم يتمرر المحتوى بينما يبقى الإطار ثابتًا والخلفية تتحرك قليلًا. — A callout draws, dwells, then content scrolls while the chrome stays fixed and the background parallaxes.
- **متى أستخدمها / when:** شرح صفحة أو تطبيق طويل — touring a long page or app.
- **كيف / how:** Scroll −720 px in 800 ms cubic-bezier(0.45,0,0.15,1), bg parallax −24 px; callouts appear only after the scroll ends (+150 ms). Phone version: card-per-beat steps of 450 ms ≈ 62% of the screen height, hold ≥ 600 ms, device counter-rotates 2°, ≤ 5 cards, never linear scroll over 2 s. **أرقام / params:** −720 px / 800 ms; hold ≥ 600 ms
- **الدليل / proof:** `kosif-tool/playbooks/product-ui.md:91-102` · `kosif-tool/playbooks/phone.md:38` · `kosif-tool/playbooks/phone.md:72-77` · `kosif-tool/styles/pm-cansincengiz-me-cf68dd/BRIEF.md`

#### UI-59 · خطوط شرح قائدة · Callout leader lines · 📄 موصوف / documented only
- **ماذا / what:** الشروح خارج الجهاز تتبع عنصرها، وخطوطها تُرسم. — Callouts outside the device follow their element and their leader lines draw on.
- **متى أستخدمها / when:** تسمية أجزاء الواجهة — labelling UI parts.
- **كيف / how:** Rows 60–90 ms stagger; callout +120 ms; leader 260 ms cubic-bezier(0.16,1,0.3,1); mono caps labels; dotted variant dash 2/4 drawn in 400 ms, 120 ms stagger from input chips into the phone UI. **أرقام / params:** leader 260 ms; stagger 60–90 ms
- **الدليل / proof:** `kosif-tool/playbooks/phone.md:39` · `style:pm-jesscaroline7-1ff7cb` · `style:pm-gabrielbuzziv-4ff0c6`

#### UI-60 · اقتراب يقوده المؤشر · Cursor-led push-in & focus zoom · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** الكاميرا تقترب نحو موضع النقرة ثم تتوقف لحظة. — The camera pushes toward the click point and holds.
- **متى أستخدمها / when:** إظهار تفصيلة صغيرة في الواجهة — showing a small UI detail.
- **كيف / how:** Push cubic-bezier(0.22,1,0.36,1) 900 ms, max 1.6×, 300 ms hold; focus zoom up to 1.4× needs a 2× render of the UI (1→1.3 in the modal recipe). Cursor 24 px quad-bezier 350–450 ms, click squash 0.9 in 90 ms. **أرقام / params:** 900 ms; ≤ 1.6×; render 2× for zoom
- **الدليل / proof:** `kosif-tool/styles/pm-techyoutbe-945b56/BRIEF.md` · `kosif-tool/styles/ui-micro/SKILL.md` · `kosif-tool/playbooks/product-ui.md:77-89`

#### UI-61 · وصفة النقر وفتح نافذة · Click → modal recipe · 📄 موصوف / documented only
- **ماذا / what:** قوس المؤشر، مرور، ضغط، تحرير، خلفية معتمة، لوحة بنابض، حقول متتابعة، اقتراب، توقف. — Cursor arc, hover, press, release, backdrop, panel spring, field stagger, focus zoom, dwell.
- **متى أستخدمها / when:** أي نقرة تفتح شيئًا — any click that opens something.
- **كيف / how:** Times (ms): 0 / 560 / 700 / 780 / 860 / 880 / 1000 / 1600 / 2200. Remotion CursorPress: travel 17 frames, pressAt 21, ripple 48 px, accent #19c37d; modal at pressAt+5; focus 1→1.3. Arrival recipe before it: 0–520 rise, chrome 400–900 with 60 ms stagger, 6 cards 700–1300 at 50 ms, push 1.05 over 4 s. **أرقام / params:** press at 700–780 ms; modal +5 frames
- **الدليل / proof:** `kosif-tool/playbooks/product-ui.md:77-89` · `kosif-tool/playbooks/product-ui.md:124-158` · `kosif-tool/playbooks/product-ui.md:66-75`

#### UI-62 · صفحة ويب مائلة تتمرر · 3D tilted webpage scroll & perspective pan · 📄 موصوف / documented only
- **ماذا / what:** صفحة كاملة كبطاقة مائلة في المنظور يتمرر محتواها بنابض. — A full webpage as a tilted 3D card whose content scrolls with spring easing.
- **متى أستخدمها / when:** عرض موقع كامل في ثوانٍ — a whole site in seconds.
- **كيف / how:** perspective + rotateX/rotateY; radius 24 px; shadow 40px 30px 80px rgba(0,0,0,.45); one paused GSAP timeline with fromTo explicit states, transforms/opacity only. Pan variant: rotateX 20° rotateY −15°, translate the parent across in 3 s ease-in-out. Use as a contrast moment, not the main idea — tilt cards are a tired default. **أرقام / params:** rotateX 20° / rotateY −15°; 3 s pan
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/3d-page-scroll.md` · `style:pm-daniel-haida-8691d4` · `style:pm-jayscambler-3f8889`

#### UI-63 · جدار بطاقات واجهة يطفو بعمق · Floating UI card wall in depth · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** شبكة بطاقات بمستويات Z مختلفة والكاميرا تتقدم، والضبابية تتبع بعد البطاقة عن مستوى التركيز. — A grid of cards at varied translateZ; the camera dollies in; blur follows distance from the focal plane.
- **متى أستخدمها / when:** افتتاح «كم المحتوى» — 'so much content' openers.
- **كيف / how:** perspective 1200 px; 3–5 columns of skeleton post cards; blur 0–8 px by |z − focus|; dolly 2 s. Wall-of-thumbnails variant: dim all but the chosen to 0.3 opacity and scale it 1.05. **أرقام / params:** perspective 1200; blur 0–8 px; dolly 2 s
- **الدليل / proof:** `style:pm-robj3d3-b18fad` · `style:pm-reyzostyle-b55864` · `style:pm-aistocksavvy-3fb9f5`

#### UI-64 · عدسة تكبير التفاصيل · Magnifier lens pass · 📄 موصوف / documented only
- **ماذا / what:** دائرة مكبرة تنزلق على سطح المنتج فتكشف الملمس مع تسمية. — A magnified circle glides over the product surface revealing texture with a label.
- **متى أستخدمها / when:** تفاصيل منتج أو نص صغير في واجهة — product details or small UI text.
- **كيف / how:** 0–1 s product, 1–4 s lens pass, 4–6 s detail hold. Enlarged copy inside clip-path:circle() whose centre follows the lens path, with compensating background-position. Never present invented detail as real photography. **أرقام / params:** 6 s; lens pass 3 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-product-ads.md`

#### UI-65 · نقطة ساخنة مع فقاعة إرشاد · Hotspot tooltip walkthrough · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** نقطة بلون العلامة تنبض على الهدف، المؤشر يصل، وتظهر فقاعة إرشاد بعدّاد «1 من 4». — A pulsing brand dot marks the target, the cursor arrives, and a tooltip card with an 'n of 4' counter pops below.
- **متى أستخدمها / when:** جولات التهيئة — onboarding tours.
- **كيف / how:** Pulse 1 s loop; tooltip pop 200 ms with Back/Next buttons. Split variant: chat bubbles on the left (40%) drive the product UI on the right (60%), bubble stagger ~600 ms. Component onboarding-stepper-flow (milestone rail + step card). **أرقام / params:** pulse 1 s; pop 200 ms; split 40/60
- **الدليل / proof:** `style:pm-jhylee95-e1152f` · `kosif-one/vendor/hyperframes/registry/components/onboarding-stepper-flow/onboarding-stepper-flow.html`

#### UI-66 · مقارنة قبل وبعد · Before/after wipe & comparison split · 📦 بأمر تثبيت / one install
- **ماذا / what:** طبقتان كاملتان وخط فاصل يمسح الطبقة الثانية ويستقر عند نسبة. — Two full-bleed layers; a divider wipes the 'after' across and rests at a split.
- **متى أستخدمها / when:** تحسين، تعديل، فلتر، إعادة تصميم — improvements, edits, redesigns.
- **كيف / how:** clip-path: inset() on the top layer, divider x 0→100% ease-in-out 1.2 s, rest at 50%. Components before-after-wipe (rest_split, wipe_at 0.25 s, labels) and comparison-split (muted before vs vivid after, horizontal|vertical). Arabic: the 'after' enters from the right. **أرقام / params:** wipe 1.2 s; rest 50%
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/before-after-wipe/before-after-wipe.html` · `kosif-one/vendor/hyperframes/registry/components/comparison-split/comparison-split.html` · `style:pm-oliahmed205-3e31c4`
- **📦 تثبيت / install:** `npx hyperframes add before-after-wipe`
- **⚖️ ترخيص / license:** مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT).

#### UI-67 · دوار الشاشات والموكاب الثابت · Screen-flow carousel & sticky mock swap · 📦 بأمر تثبيت / one install
- **ماذا / what:** 2–5 شاشات على سكة، الوسطى أساسية والجيران يتراجعون؛ أو موكاب ثابت تتبدل ميزاته مع العناوين. — 2–5 app screens ride a rail with the centre primary and neighbours receding; or a pinned mock crossfades through features while captions rise.
- **متى أستخدمها / when:** عرض 3 ميزات في فيلم قصير — three features in a short film.
- **كيف / how:** Advance on cues with a velocity-matched throw and long-tail catch; caption swaps with each stop. Seen: covers sliding x with 80 ms stagger and slight 3D tilt; cropped-edge strip moving ~120 px/s; slot-reel portrait scroller decelerating onto one card in 1.0 s (blur 0→30→0 px, overshoot 1.1). Components screen-flow-carousel, sticky-mock-swap; block app-showcase (three floating phone screens, 5.5 s). **أرقام / params:** strip ~120 px/s; slot reel 1.0 s
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/screen-flow-carousel/screen-flow-carousel.html` · `kosif-one/vendor/hyperframes/registry/components/sticky-mock-swap/sticky-mock-swap.html` · `kosif-one/vendor/hyperframes/registry/blocks/app-showcase/app-showcase.html` · `style:pm-brainextends-e19ac3` · `style:pm-samuel-yostt-891f87`
- **📦 تثبيت / install:** `npx hyperframes add screen-flow-carousel`
- **⚖️ ترخيص / license:** مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT).

#### UI-68 · شبكة بنتو للميزات · Bento feature grid · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** بطاقات مستديرة بواجهات مصغرة متحركة تظهر بالتتابع. — Rounded cards with mini animated UIs pop in staggered.
- **متى أستخدمها / when:** ملخص الميزات أو نظام التصميم — feature summaries or a design-system reel.
- **كيف / how:** Stagger 80–100 ms, radius 20 px. Design-system bento: 12-column grid, 24 px gutter; modules = frame counter 'f 047/900' with progress, palette swatches, 'Aa' type specimen, easing plots (expo.out, power3.inOut, back.out(1.7)), BPM meter. **أرقام / params:** stagger 80–100 ms; radius 20 px
- **الدليل / proof:** `style:pm-sudo-kiran-4f8b59` · `style:pm-grace-sunnyy-29bc61` · `style:pm-thayto-dev-44b911`

#### UI-69 · لوحة قياس HUD وشروح مسقطة من 3D · Instrument-panel HUD & projected callouts · 🟢 جاهز / ready
- **ماذا / what:** شريط عنوان وساعة وأشرطة زمنية وثلاث لوحات رسوم حية، وشروح بحلقات منقطة مسقطة من نقاط ثلاثية الأبعاد. — Title strip, clock, timeline bars, three live chart panels and dashed-ring callouts projected from 3D anchors.
- **متى أستخدمها / when:** أفلام مختبر/تحليل تقنية — lab or technical analysis films.
- **كيف / how:** H = K3.hud(root, W, H, {title, subtitle, panels, accent, ink, paper, font, seed}); H.addCallout({anchor, label, title, text, side, measure}); H.update(t, camera, {stage, side, duration}) — call camera.updateMatrixWorld() first. Floor: K3S.stageDisc({radius .32, color #9dffb4}) with grid, rings, 36 ticks and a uScan sweep. Lighter version: component telemetry-hud (mono label:value lines, corner brackets). **أرقام / params:** lime #a8ff3c, ink #0f1512, paper #f4f2ec; IBM Plex Mono; top 8.5% H, bottom 20% H
- **الدليل / proof:** `kosif-studio/motion/kit/lab-kit.js:207` · `kosif-studio/motion/kit/shape-kit.js:343` · `100-superskills/skills/kosif-montage-motion/scripts/kit/lab-kit.js:207` · `kosif-one/vendor/hyperframes/registry/components/telemetry-hud/telemetry-hud.html`

#### UI-70 · مربع تتبع وماسح ضوئي · AI tracking box & scanner brackets · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** زوايا L صفراء تتبع هدفًا مع نسبة ثقة متذبذبة، أو أربع زوايا تنقفل على بطاقة وخط مسح يكتسحها. — Yellow L-bracket corners follow a target with a fluctuating confidence label, or four corners snap onto a card while a scan line sweeps.
- **متى أستخدمها / when:** رؤية حاسوبية، مسح QR، OCR — computer vision, QR scan, OCR beats.
- **كيف / how:** Tracking box: #facc15, corners 48×48 px with 6 px border, confidence 95–99% (seeded), box derived from the target each frame. Scanner: corners 14 px stroke r12 snap in 250 ms back-out, green glowing line sweeps 900 ms, then lavender line highlights #c9cdf5 @0.6 with 70 ms stagger. Beat lock: an outlined box with 0 0 24px #e8501f glow hops cards per beat, overshoots, locks, dims the rest to 30%. Component camera-scan-gate ends on 'Verified'. **أرقام / params:** corners 48 px / 6 px; sweep 900 ms
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/ai-tracking-box.md` · `style:pm-mehul4795-4a7007` · `style:pm-tankazunori0914-0fc886` · `kosif-one/vendor/hyperframes/registry/components/camera-scan-gate/camera-scan-gate.html`

#### UI-71 · مسرح أداة تصميم ومقابض تحديد · Design-tool canvas, selection handles & size tags · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** كل العمل كإطارات على لوحة فاتحة بشبكة نقاط، وكاميرا افتراضية تتنقل، ومستطيل تحديد بمقابض ووسم مقاس. — All work as labelled frames on a light dotted canvas with a virtual camera, plus selection boxes with handles and a 'W × H' tag.
- **متى أستخدمها / when:** قصص التصميم والإبداع — design and creative-process stories.
- **كيف / how:** Dot grid 24 px on #e8e7e3; file chip top-right, zoom % badge bottom-left; move a container (scale + translate) instead of cutting. Selection: 1.5 px accent rect, 4 (or 8) square handles, filled tag below, appear 120–150 ms. Blueprint overlay: duplicate the UI as 1 px cyan #3fb6d2 strokes with 8% fill and crossfade 400 ms. Component vector-editor-rig (pen path, anchors, bezier handles). **أرقام / params:** dot grid 24 px; handles appear 120–150 ms
- **الدليل / proof:** `style:pm-kikelopezdesign-7cc9e8` · `style:pm-moguzbulbul-6311b6` · `style:pm-arjunsh1607-93005d` · `kosif-one/vendor/hyperframes/registry/components/vector-editor-rig/vector-editor-rig.html`

## التقاط المواقع والتسجيل وأفلام الإطلاق — Capture, recording & launch films

_من رابط أو تطبيق حقيقي إلى فيلم: التقط، ابنِ، ولا تخترع صفحة لم تُلتقط._

#### UI-72 · تسجيل صفحة بخطوات مبرمجة · Scripted page recording (Playwright) · 🟢 جاهز / ready
- **ماذا / what:** ملف خطوات JSON يقود صفحة حقيقية: انتظار، نقر بمؤشر منزلق، سحب، كتابة، تمرير، مع ترجمة لكل خطوة. — A JSON steps file drives a real page — wait, click with a gliding cursor, drag, type, wheel scroll, captions per step.
- **متى أستخدمها / when:** عرض ميزة من منتج حقيقي — a feature demo from a real product.
- **كيف / how:** Write your own Playwright script (Playwright + Chromium are installed here) mirroring the step grammar: wait, waitFor selector/text/js, click, tap, drag (hold), hover, held keys, type, wheel scroll over time, goto, caption → captions.vtt. Frames the page did not repaint are held and counted, never interpolated; warn under 20 fps. The atlas record-page.mjs is reference only (needs puppeteer-core; do not run unreviewed). Prep: native resolution, enlarged cursor, editor font ≥ 16 pt, notifications off, disposable data, lead-in and lead-out. **أرقام / params:** settle 1.5 s; glide 450 ms; type 70 ms/key; caption 3 s; step timeout 20 s; max 600 s; phone = 360×640 at 3×
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3903-video/references/RECORD.md` · `kosif-atlas/skills/1511-homie/3903-video/references/examples/site-walkthrough.json` · `kosif-atlas/skills/1096-akbun-editvideo/2447-akbun-vlog-shootplan/SKILL.md`

#### UI-73 · التقاط موقع إلى فيديو · Website capture → video · 📦 بأمر تثبيت / one install
- **ماذا / what:** زحف متصفح بلا واجهة على رابط يخرج لقطات وألوان وخطوط ونصوص وأصول، ثم فيلم من مرئيات الموقع نفسه. — A headless crawl of a URL yields screenshots, brand tokens (colours, fonts), text and assets; the film is built from the site's own visuals.
- **متى أستخدمها / when:** «اعمل فيديو لموقعي» — 'make a video of my site'.
- **كيف / how:** npx hyperframes capture https://site -o ./capture --json [--skip-vision] [--max-screenshots 12] [--timeout 60000]; gate on ok:true and no capture/BLOCKED.md — a failed capture is a hard stop, never invent a page. Then capture → design → script → storyboard → voice → build → validate (product-launch-video skill, 30–90 s sweet spot, up to ~3 min). Tone mixes: high impact = per-word type + velocity cuts + counters; premium = variable font + Lottie + slow cuts. Vision captions need an external service. **أرقام / params:** sweet spot 30–90 s
- **الدليل / proof:** `kosif-one/vendor/hyperframes/packages/cli/src/commands/capture.ts` · `kosif-one/vendor/hyperframes/skills/product-launch-video/SKILL.md` · `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/SKILL.md`
- **📦 تثبيت / install:** `npx hyperframes capture <url> -o ./capture --json`
- **⚖️ ترخيص / license:** Apache-2.0

#### UI-74 · فيلم إطلاق kmotion brag · kmotion brag launch film · 🟢 جاهز / ready
- **ماذا / what:** من مجلد أو رابط إلى خطة ثم بناء ثم تسليم لفيلم إطلاق موقع أو تطبيق. — From a folder or URL to plan → build → deliver for a site/app launch film.
- **متى أستخدمها / when:** إطلاق منتج من مستودع أو موقع — launches from a repo or site.
- **كيف / how:** kmotion brag init DIR|URL → plan → build → deliver (scripts/launch.py, covered by tests/test_launch.py). Basma studio alternative: AGENT.TOOLS.launch_film {product, pitch, duration} writes hook → pain → reveal → 3 features → CTA and cuts uploaded recordings on the beat under big kinetic titles (needs the app's AI service). **أرقام / params:** story: hook · pain · reveal · 3 features · CTA
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/launch.py` · `100-superskills/skills/kosif-montage-motion/tests/test_launch.py` · `app/public/js/10_studio.js:4306`

#### UI-75 · وصفة فيديو ميزة حقيقية · Real-feature video recipe · 📄 موصوف / documented only
- **ماذا / what:** «المستخدم يفعل كذا، والمنتج يفعل كذا بوضوح» — التقط التطبيق الحقيقي لا موك أب. — 'The user does X; the product visibly does Y' — capture the real app, not a mockup.
- **متى أستخدمها / when:** إعلان ميزة جديدة — announcing a new feature.
- **كيف / how:** Leave a little time before/after the action; cut waits only where it does not misrepresent the experience; one visual focus at a time; words only when the picture can't say it. Capture with Playwright recordVideo, edit/reframe with ffmpeg, overlays with render_html.cjs. Deliver 16:9, 4:5, 9:16 and 1:1. **أرقام / params:** formats 16:9 · 4:5 · 9:16 · 1:1
- **الدليل / proof:** `kosif-atlas/skills/101-video-skills/215-feature-video/SKILL.md`

#### UI-76 · من فيجما إلى طبقات متحركة · Figma frame → animatable layers · 🔑 مفتاح أو خدمة / needs key or service
- **ماذا / what:** اسحب بنية الإطار وألوانه وظلاله وخطوطه ومسافاته من فيجما وأعد بناءه HTML/CSS جاهزًا للتحريك. — Pull a frame's structure, fills, shadows, type, auto-layout spacing and variables from Figma and rebuild it as animatable HTML/CSS.
- **متى أستخدمها / when:** عندما يرسل المستخدم رابط فيجما — when the user sends a Figma link.
- **كيف / how:** File key after /design/ or /file/; node-id 123-456 == 123:456; auto-layout → flexbox; RGBA floats 0–1 → hex; REST /v1/images/:key?ids=…&format=png&scale=2. Needs a Figma token or the Figma MCP (external service). **أرقام / params:** PNG export scale 2; variables per light/dark
- **الدليل / proof:** `kosif-atlas/skills/1381-figma/3252-figma-implementing` · `kosif-atlas/skills/1381-figma/3252-figma-implementing/references/figma-mcp-tools.md`

#### UI-77 · تسجيل المتصفح بمؤشر ولوحة لقطات · Browser recording CLI with cursor & contact sheet · 📦 بأمر تثبيت / one install
- **ماذا / what:** سجّل التبويب النشط إلى webm/mp4 بـ 1–60 إطارًا مع مؤشر متحرك ولوحة لقطات تلقائية. — Record the active tab to webm/mp4 at 1–60 fps with an animated pointer and an automatic contact sheet.
- **متى أستخدمها / when:** تسجيل سريع بلا كتابة سكربت — quick recordings without a script.
- **كيف / how:** agent-browser record start demo.webm --cursor --contact-sheet --fps 60 (needs the agent-browser install + ffmpeg). Default 30 fps; 60 for motion studies; 1–15 for long timelines. In this container prefer your own Playwright script (UI-72); desktop recorders (wf-recorder on Wayland, OBS, x11grab) are not usable headless here. **أرقام / params:** 30 fps default; 60 motion; 1–15 long
- **الدليل / proof:** `kosif-atlas/skills/1412-agent-browser/3350-agent-browser/references/video-recording.md`
- **📦 تثبيت / install:** `npm i -g agent-browser`

#### UI-78 · فيديو تعليمي من ملف YAML · YAML-defined tutorial video · 📄 موصوف / documented only
- **ماذا / what:** صف الشرائح وخطوات الشاشة والتعليق في YAML ثم يُرندر مع صوت وترجمة. — Describe slides, screencast steps and narration in YAML, then render with TTS narration and subtitles.
- **متى أستخدمها / when:** شروح متكررة بعلامة ثابتة — repeatable branded tutorials.
- **كيف / how:** docker compose run video-guide-creator validate|generate guides/<slug>.yml (Edge TTS voices; edge-tts looks blocked from this container). Rule worth keeping: narration describes the action before it happens; brand presets hold colours, voice and logo.
- **الدليل / proof:** `kosif-atlas/skills/2836-video-guide/11537-video-guide-creator/SKILL.md`

## أنظمة التصميم والقوالب والأدوات — Design tokens, templates & tooling

_ما تحتاجه لتبدو الواجهة احترافية من أول إطار، ومكتبات مكوّنات جاهزة._

#### UI-79 · رموز تصميم الواجهة وسلالمها · UI tokens & Refactoring-UI scales · 📄 موصوف / documented only
- **ماذا / what:** شبكة 8 بكسل، زوايا 8/16/24، خط عنوان + مقاسان، وأربعة مستويات ظل. — 8 px grid, radii 8/16/24, one headline + two UI sizes, four elevation tiers.
- **متى أستخدمها / when:** أي واجهة وهمية داخل فيلم — any mock UI inside a film.
- **كيف / how:** Write them into STYLE.md first. Spacing 4, 8, 16, 24, 32, 48, 64; type 12–36 on a ~1.2 scale (hero 36 px lh 1.1, body 16 px lh 1.75); measure 45–75ch. Shadows: sm 0 1px 2px .05 · md 0 4px 6px .1 · lg 0 10px 15px .1 · xl 0 20px 25px .15; product tiers 0 2px 8px rgba(0,0,0,.12) → 0 24px 64px rgba(0,0,0,.35). **أرقام / params:** 8 px grid; radii 8/16/24; 4 shadow tiers
- **الدليل / proof:** `kosif-tool/playbooks/product-ui.md:18` · `kosif-atlas/skills/3438-ux-design/14122-refactoring-ui`

#### UI-80 · سطح زجاجي للواجهات · Glass surface stack · ✅ مُثبت هنا / proven here
- **ماذا / what:** لوحة ضبابية بطبقات فوق خلفيات داكنة: ضبابية خلفية، تعبئة 5%، حد متدرج 1 بكسل، وظل محيطي كبير. — Layered frosted panels on dark scenes: backdrop blur, 5% fill, 1 px gradient border, large soft ambient shadow.
- **متى أستخدمها / when:** بطاقات فاخرة وإشعارات زجاجية — luxury cards and glass notifications.
- **كيف / how:** backdrop-filter blur(22–28px) saturate(150%) (40 px for modals); fill rgba(255,255,255,.05–.08); 1 px border gradient .12→.02 plus a 1 px inner highlight; box-shadow 0 24px 80px rgba(0,0,0,.25). Dark backgrounds only, max 3 cards, cards rise y 40→0 and unblur 12→0 with 80 ms stagger. Proven here: four glass cards on three parallax depths in the glass-luxury-logo film (13/13 checks). Needs Chromium's backdrop-filter. HyperFrames liquid-glass blocks need WebGPU/HTML-in-Canvas — unverified here. **أرقام / params:** blur 22–28 px (40 modals); fill 5–8%; shadow 0 24px 80px .25
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/proofs/glass-luxury-logo/README.md` · `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md` · `100-superskills/skills/trend-animation-styles/references/styles.md` · `kosif-tool/styles/glass-ui/SKILL.md`

#### UI-81 · معمارية الثيمات: الشكل × الوضع × العلامة · Look × theme × brand token architecture · 🟢 جاهز / ready
- **ماذا / what:** مجموعة رموز واحدة تُعاد كسوتها بـ 14 شكلًا ووضعين وعلامات، مع استوديو للخط واللون والزوايا والتباين. — One token set re-skinned by 14 looks, light/dark and brand variants, plus a studio for font, accent, radius, scale and contrast.
- **متى أستخدمها / when:** واجهات عربية بعدة هويات في فيلم واحد — Arabic UIs with several identities in one film.
- **كيف / how:** html[data-look] × [data-theme] × [data-brand]; looks: kosif, cobalt, navygold, najd, heritage, executive, audit, midnight, notebook, aurora, vivid, oasis, graphite, onyx (+ night pairs, auto); radii sharp 4/6/8 or round 12/16/22; --sk-zoom; data-contrast; screens never hard-code colour. KPI tile: white on mist, soft shadow, 4 px tone edge on the reading side, radius 18 px. **أرقام / params:** 14 looks; radii 4/6/8 or 12/16/22
- **الدليل / proof:** `kosif-earth-ci-fork/ui/layouts/shell.js:29` · `kosif-earth-ci-fork/ui/ds/tokens.css` · `kosif-earth-ci-fork/ui/ds/surfaces.css`

#### UI-82 · ستايل برومو المنتج · Product promo style (neon prompt + glass orb) · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** تايبوغرافي حركي لإطلاق منتج مع صندوق طلب نيون وكرة زجاجية وتقلب فاتح/داكن. — Launch-promo kinetic type with a neon prompt box, a glass orb and light/dark flips.
- **متى أستخدمها / when:** إطلاق أداة ذكاء اصطناعي — AI-tool launches.
- **كيف / how:** 16:9, 2.2 words/s, Readex Pro; bg #05050A, light #F8F7FF, ink #F5F3FF, grey #8B88A6, violet #A88BFF/#6C3BFF, blue #2F5BFF, pink #D946EF, orange #FF6A1A. Modes cycle big → prompt → orb → capsule → end; typing + click SFX on prompt lines, impact on the end card. Typewriter with a 3 px purple caret at ~18 chars/s while the parent scales 2.5→1 from the first character (camera pull-back synced to typing). **أرقام / params:** 2.2 wps; ~18 cps; pull-back 2.5→1
- **الدليل / proof:** `app/public/js/10_studio.js:794` · `style:product`

#### UI-83 · واجهة ملصقات بظل صلب · Sticker UI with hard offset shadow · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** بطاقات وأزرار بحد داكن سميك وزوايا كبيرة وظل صلب مزاح بلا ضبابية. — Cards, pills and buttons with a thick dark outline, big radii and a solid offset shadow with no blur.
- **متى أستخدمها / when:** أفلام مرحة أو نيو-بروتاليست — playful or neo-brutalist films.
- **كيف / how:** 4–6 px outline #2a1711, radius 24–40 px, same-hue shadow offset y 6 px; brutalist variant: 2 px black border, header strip, mono label. **أرقام / params:** outline 4–6 px; shadow offset 6 px
- **الدليل / proof:** `style:pm-thilina-a-891c09` · `style:pm-polydao-7a572b`

#### UI-84 · مكتبة مكوّنات HyperFrames للواجهات · HyperFrames UI component registry · 📦 بأمر تثبيت / one install
- **ماذا / what:** أكثر من 40 مكوّن واجهة جاهزًا (مؤشرات، إشعارات، أجهزة، محادثات، تبويبات…) تُركّب في أي مشهد. — 40+ ready UI components (cursors, notifications, devices, chats, tabs…) that mount into any scene.
- **متى أستخدمها / when:** عندما يكفي مكوّن جاهز بدل البناء من الصفر — when a ready component beats building from scratch.
- **كيف / how:** npx hyperframes add <name> copies compositions/components/<name>.html; mount on a class='clip' div with data-composition-src + data-start/data-duration/data-track-index; overrides as JSON in data-variable-values; colours come from 18 theme tokens (accent green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch. Preview npx hyperframes preview, render npx hyperframes render. The vendored copies are readable locally for study. Table below.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/agent-cursor/registry-item.json` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints-index.md`
- **📦 تثبيت / install:** `npx hyperframes add <component>`
- **⚖️ ترخيص / license:** مكوّنات HyperFrames برخصة Apache-2.0، لكنها تحمّل GSAP 3.14 من CDN — GSAP برخصة «بلا مقابل» القياسية، ليست MIT / HyperFrames components are Apache-2.0 but load GSAP 3.14 from a CDN under GSAP's standard no-charge license (not MIT).

#### UI-85 · مخططات مشاهد الواجهة · UI scene blueprints · 📄 موصوف / documented only
- **ماذا / what:** وصفات متعددة المراحل لمشاهد الواجهة الشائعة، تُختار حسب الدور وتُذكر في الستوري بورد. — Multi-phase recipes for common UI scenes, picked by role and cited per beat in the storyboard.
- **متى أستخدمها / when:** تخطيط فيلم منتج كامل بسرعة — planning a whole product film fast.
- **كيف / how:** Pick from blueprints-index.md by role: cursor-ui-demo (4.0–12.9 s), device-surface-showcase (5–11.3 s), prompt-type-submit-generate (5.2–12 s), agent-progress-theater (4.2–11.6 s), panel-edit-live-sync (5.3–11.9 s), transcript-scroll-artifact-reveal (5–11.8 s), zoom-out-workspace-reveal, cta-morph-press. 13 runnable 1920×1080 examples (hook-counter-burst 3.5 s … demo-page-scroll-spotlight 9 s) are the ground truth. **أرقام / params:** durations 3.5–12.9 s
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints/cursor-ui-demo.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints/device-surface-showcase.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/examples/hook-counter-burst.html`

#### UI-86 · أساليب KOSIF للواجهات · KOSIF UI styles to scaffold · 🟢 جاهز / ready
- **ماذا / what:** ثلاثة أساليب جاهزة للبناء: عرض SaaS، تفاعلات دقيقة، وواجهة زجاجية — مع كتيبي product-ui وphone. — Three ready styles — SaaS demo, UI micro-interactions, glass UI — backed by the product-ui and phone playbooks.
- **متى أستخدمها / when:** بداية أي فيلم واجهة في kosif-tool — starting any UI film in kosif-tool.
- **كيف / how:** python3 tools/kosif.py scaffold saas-demo <dir> (or ui-micro, glass-ui); python3 tools/kosif.py list --category product-ui (82 entries) / --category phone (8). saas-demo: cursor 380–700 ms cubic-bezier(.2,.8,.2,1), press 80/140 ms, 8 px grid. ui-micro: hover 120–160 ms, press 0.96, ripple 0→48 px in 320–400 ms, focus zoom ≤ 1.4× with a 2× render.
- **الدليل / proof:** `kosif-tool/styles/saas-demo/STYLE.json` · `kosif-tool/styles/ui-micro/STYLE.json` · `kosif-tool/styles/glass-ui/STYLE.json` · `kosif-tool/playbooks/product-ui.md` · `kosif-tool/playbooks/phone.md`

#### UI-87 · مشغّل HTML مستقل بشريط تقديم · Standalone HTML player with seek & reduced motion · ✅ مُثبت هنا / proven here
- **ماذا / what:** الفيلم يُسلَّم صفحة ويب offline بتشغيل/إيقاف وإعادة ومنزلق 0.01 ث ورابط تحميل MP4 واحترام الحركة المخفضة. — The film ships as an offline web page with play/pause, restart, a 0.01 s range slider, an MP4 download link and prefers-reduced-motion support.
- **متى أستخدمها / when:** تسليم تفاعلي أو معاينة للعميل — interactive deliverables or client previews.
- **كيف / how:** build.cjs templates an Arabic RTL page; rAF advances by min(dt, 0.1 s) and auto-stops at the end; window.render(t) clamps; window.setPlaying(bool); ?capture hides the chrome for rendering. Ran here: node player-test.cjs → PASS (initialisation, reduced motion, seek, deterministic frame, play/pause, restart, automatic stop, bounds). **أرقام / params:** theme #060d17/#08121c, focus ring #ffb769, accent #71e5d2
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/build.cjs:6` · `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/player-test.cjs:1`

#### UI-88 · مراجعة على الإطار: سحب وتحجيم واختصارات · Frame review: drag, resize & Arabic-safe shortcuts · 🟢 جاهز / ready
- **ماذا / what:** في وضع التحرير يُسحب العنصر ويُحجّم من زاويته وتُحفظ القيم كنسب من الإطار، والاختصارات تعمل بلوحة مفاتيح عربية. — In edit mode elements drag and corner-resize with values saved as % of frame; shortcuts work on an Arabic keyboard layout.
- **متى أستخدمها / when:** جولات التعديل مع المستخدم — revision rounds with the user.
- **كيف / how:** Edits stored as '<id>.@box' = [x,y,w,h] in % (one decimal), 14 px corner grab radius, uniform scale ≥ 0.1. Keys bound to ev.code (KeyE, KeyN, BracketLeft/Right) so they survive the Arabic layout: Space play, ←/→ one frame, Shift+←/→ one second, [ ] scene, E edit, N note; speeds ½×/1×/2×; studio app keeps 60-step undo/redo. **أرقام / params:** box in % of frame; undo depth 60
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/index.html:600` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/index.html:954` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:159`
- **⚖️ ترخيص / license:** MIT (Motion OS)

#### UI-89 · قواعد صفحات الويب المسلَّمة · Web deliverable rules (landing, perf, hover gating) · 📄 موصوف / documented only
- **ماذا / what:** عندما يكون الناتج صفحة: أنماط هبوط، ميزانية أداء، والمرور فقط على مؤشر دقيق. — When the deliverable is a page: landing patterns, a performance budget, and hover only on fine pointers.
- **متى أستخدمها / when:** صفحة منتج متحركة أو ترويج يُسجّل لاحقًا — animated product pages or promos recorded later.
- **كيف / how:** Hero (≤ 10-word outcome headline, one CTA, product in use) → social proof → 3–6 benefits → 3 steps → offer → FAQ → final CTA; container max 72rem; H1 clamp(28px,5vw,44px); breakpoints 360/768/1024/1280; 375 px without sideways scroll. Budget: LCP ≤ 2.5 s, CLS ≤ 0.1, INP ≤ 200 ms, JS ≤ 170 KB gz. @media (hover:hover) and (pointer:fine) for hover lifts; touch targets ≥ 44 px; respect prefers-reduced-motion. **أرقام / params:** LCP ≤ 2.5 s; CLS ≤ 0.1; INP ≤ 200 ms
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-web-design/references/web-playbook.md` · `100-superskills/skills/landing-page-premium/SKILL.md` · `kosif-audit-pro/app/globals.css:223`

**مكوّنات HyperFrames للواجهات / UI component quick table** (كلها 📦 `npx hyperframes add <name>`؛ المصدر في `kosif-one/vendor/hyperframes/registry/components/`):

| المجموعة / group | المكوّنات / components |
|---|---|
| مؤشرات / cursors | agent-cursor · magnetic-cursor · oversized-cursor · dart-cursor · cursor-drag-drop · cursor-text-select · cursor-marquee-select · cursor-context-menu · cursor-glyph-trail · multiplayer-cursors · press-ripple |
| لمس / touch | touch-indicator · gesture-tap · swipe-rail · pull-to-refresh · sheet-spring-up |
| محادثة / chat | chat-thread · chat-message · typing-indicator · notes-typing |
| إشعارات / notifications | native-notification-pop · notification-stack · notification-pileup · badge-pop |
| حالات / states | toggle-flip · success-check · input-feedback · skeleton-reveal · state-chip-rail · icon-morph-beat · icon-swap · micro-transitions |
| تحولات / morphs | modal-morph · card-resize · panel-reveal · menu-morph · focus-swap · tabs-slide-indicator |
| أجهزة وشاشات / devices & screens | browser-device-stage · device-frame-stage · multi-device-splay · screen-flow-carousel · sticky-mock-swap |
| تدفقات / flows | onboarding-stepper-flow · settings-toggle-flow · signup-flow · avatar-group-hover |
| تقنية / tech | telemetry-hud · camera-scan-gate · vector-editor-rig · before-after-wipe · comparison-split |

**كتل كاملة / full blocks:** app-showcase (5.5 s) · message-thread-reveal (25.8 s, 9:16) · notes-reveal (24.9 s, 9:16) · notification-cascade (14 s, 9:16) · share-sheet-carousel (7.2 s, 9:16) · slack-notification-ad (12 s, 9:16) · thread-message-stack (8 s) · ui-3d-reveal (13 s) · vfx-iphone-device · ios26-liquid-glass · macos-tahoe-liquid-glass (15 s) · liquid-glass-notification / -widgets (8 s, WebGPU) · vpn-youtube-spot (7 s; its SFX file is missing locally) · 24 code-snippet IDE/terminal themes.

## توليفات قوية / power combos

- **إطلاق أداة ذكاء اصطناعي / AI-tool launch:** UI-26 + UI-27 + UI-11 + UI-82 + ARAB (كلمة وعد ضخمة) + BEAT (نقرات وكتابة على الإيقاع) — طلب يُكتب، زر يُضغط، وكيل يشطب خطواته، ثم بطاقة نهاية — كما في style:product.
- **ريل تطبيق عربي 9:16 / Arabic app reel:** UI-47 + UI-49 + UI-06 + UI-22 + UI-40 + SYNC (ترجمة من words.json) — هاتف يصعد بزاوية −8°، واجهة معكوسة، لمسات بدوائر شفافة، وجزيرة ديناميكية لحظة النجاح.
- **فيلم موقعي من رابط / site film from a URL:** UI-73 + UI-62 + UI-58 + UI-59 + TRANS (قطعات سرعة) + VOICE (تعليق) — مرئيات الموقع نفسه، جولة تمرير بشروح، ولا صفحة مخترعة.
- **شرح تعليمي لميزة / feature tutorial:** UI-72 + UI-10 + UI-60 + UI-14 + CAM (اقتراب واستقرار) + QA (لقطات عند كل فعل) — تسجيل حقيقي، أفعال بالعربي، اقتراب على كل نقرة.
- **لوحة بيانات حية / live dashboard story:** UI-07 + UI-44 + UI-45 + DATA (عدّادات وأعمدة) + COLOR (لوحة الهوية) — سؤال واحد يسيطر، والأرقام تعد بأرقام جدولية.
- **قبل/بعد لمنتج تصميم / design-tool before/after:** UI-71 + UI-66 + UI-24 + SHAPE (تحول الأشكال) — مقابض تحديد، منزلق يغيّر السطح حيًا، ومسح يكشف النتيجة.
- **إعلان فاخر بزجاج / luxury glass promo:** UI-80 + UI-55 + GLOW (توهج الحواف) + CAM (دوران 360) + BRAND (شعار يُرسم) — بطاقات زجاج بثلاثة أعماق وجهاز ثلاثي الأبعاد بشاشة حية.
- **قصة محادثة إعلانية / chat-story ad:** UI-28 + UI-40 + UI-25 + BEAT (فقاعة على كل نبضة) + FORMAT (9:16) — محادثة تتصاعد ثم بطاقة دعوة.

## أخطاء ممنوعة / never do

1. **لا مؤشر سهم داخل هاتف** — الهواتف تُلمس؛ استخدم دائرة لمس شفافة 40–48 px (UI-22).
2. **لا استجابة في 0 ms ولا بعد 200 ms** — الأولى عرض شرائح والثانية تبدو عطلًا؛ 60–120 ms (UI-02).
3. **لا lorem ولا سعر أو عدّاد تنازلي غير مؤكد ولا ميزة مخترعة** — يكسر الثقة ويخالف قواعد الإعلان (UI-03).
4. **لا تحرك width/height في الرندر** — يعيد التخطيط كل إطار ويرتعش؛ حرّك transform وopacity وعوّض مقياس الأبناء (UI-41).
5. **لا تقلب <html dir=rtl> في صفحة تُرندر** — ضع الاتجاه على حاوية الواجهة فقط؛ واعكس التفاعل لا العتاد (UI-06).
6. **لا تكبّر لقطة شاشة حتى تتكسر** — أعد الالتقاط بدقة أعلى أو أعد البناء DOM بكثافة 2× (UI-04).
7. **لا تجعل الميل الثلاثي والزجاج والتوهج هي الفكرة** — العمق من الارتفاع والتداخل وبارالاكس 2–4%؛ الميل لحظة تباين فقط (UI-62).
8. **لا Math.random في الكتابة أو الثقة أو الجسيمات** — الرندر يجب أن يتكرر بالإطار نفسه؛ استخدم بذرة (UI-25).
9. **لا ترندر مكوّن HyperFrames بالوضع الافتراضي لـ render_html** — جرّبتها هنا: إطار ثابت، لأن الجدول متوقف والمكوّن الفرعي لا يُركّب؛ استخدم npx hyperframes render (UI-21).
10. **لا تخترع صفحة عندما يفشل الالتقاط** — توقف واطلب لقطات أو رابطًا آخر (UI-73).
11. **لا مؤشر بحجم 23 px في إطار 1080 عرضًا** — رأيته في رندر الوصفة: يكاد لا يُرى على الهاتف؛ كبّره ×1.5–2 (UI-12).

## أقوى 5 حركات توقيع / 5 signature moves

1. **UI-11 — مؤشر Hermite بضغطة وكتابة:** محطات زمنية، توقف بسرعة صفر، ضغط 0.88 في 4 إطارات، والهدف ينخفض 0.97 — مُرندر هنا.
2. **UI-26 + UI-27 — طلب يُكتب ووكيل يشطب:** 40 ms للحرف، حلقة إرسال 300 ms، ثم علامات صح كل 250–600 ms.
3. **UI-49 — كشف الهاتف البطل:** صعود 140 px مع yaw −22°→−8°، لمعة تعبر، صفوف كل 70 ms، ودفعة 1.04.
4. **UI-41 — بطاقة تصبح لوحة:** تحويل فقط، أبناء يعوضون المقياس، نابض ~300 بنسبة إخماد 0.8.
5. **UI-58 + UI-59 — جولة تمرير بشروح مرسومة:** −720 px في 800 ms، توقف ≥ 600 ms، وخط قائد 260 ms.
