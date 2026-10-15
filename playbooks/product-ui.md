# Product UI motion — حركة واجهات المنتج

This playbook covers films whose subject is an app or SaaS interface: feature launches, onboarding explainers, "how it works" clips and release notes in motion. It tells Claude how to rebuild screens as layered components, choreograph cursor, tap, scroll, modal and focus events with believable timings, and frame the screen with or without a device. It sits under the style's `SKILL.md` and `BRIEF.md`: when they state a number, theirs wins.

هذا الدليل يخص الأفلام التي بطلها واجهة تطبيق أو منتج SaaS: إطلاق ميزة، شرح أول استخدام، مقطع «كيف يعمل»، أو ملاحظات إصدار متحركة. يشرح كيف تُعاد بناء الشاشة كطبقات مستقلة، وكيف تُنسَّق حركة المؤشر والنقر والتمرير والنوافذ المنبثقة والتركيز بتوقيتات واقعية، وكيف تُؤطَّر الشاشة داخل جهاز أو بدونه. يأتي تحت `SKILL.md` و`BRIEF.md` الخاصين بالاستايل، وعند تعارض رقم محدد فالأولوية لهما.

## 1. When to use — متى تستخدمه

Use it when the message is "this is what the product does" and the proof is the interface doing it: a 20–45 s launch film, a 10–15 s feature teaser, a vertical reel walking through one flow, a changelog clip, a before/after inside the same screen. Do not reach for it when the film is brand mood only (`playbooks/ads.md`), when a chart is the hero (`playbooks/charts.md`) or when the piece is pure typography (`playbooks/kinetic-type.md`); those films may borrow one UI scene from here.

Decide the framing before the plan. Device-free framing (a floating, rounded screen with its own shadow) suits desktop SaaS, dashboards and anything that must crop to several aspect ratios. In-device framing (phone or laptop bezel) suits mobile apps where thumb reach and status bar matter; `playbooks/phone.md` adds the bezel rules, this playbook keeps the interaction rules.

**بالعربية:** استخدمه عندما تكون الرسالة «هذا ما يفعله المنتج» والدليل هو الواجهة نفسها وهي تعمل: فيلم إطلاق 20–45 ثانية، تشويقة ميزة 10–15 ثانية، ريل عمودي لمسار واحد، أو مقطع تحديثات. لا تستخدمه لفيلم هوية بلا واجهة، ولا عندما يكون الرسم البياني هو البطل، ولا للتايبوغرافي الصرف. حدّد الإطار قبل الخطة: شاشة طافية بلا جهاز للمنتجات المكتبية ولكل ما يحتاج قصًّا لعدة نسب، وجهاز حقيقي للتطبيقات الجوالة حيث يهم الإبهام وشريط الحالة.

## 2. Visual grammar — القواعد البصرية

- **Layers, not screenshots.** Build every screen as: background → chrome (sidebar, top bar, tab bar) → content blocks (cards, rows, fields) → controls (buttons, toggles, inputs) → overlays (modal, dropdown, toast) → pointer layer → callout layer. Each layer owns its timeline so it can enter, change state and leave on its own. A flattened PNG may sit behind the rebuilt layers as a reference, never as the thing that animates.
- **Tokens first.** One 8 px grid; three radii (8, 16, 24); one headline size plus two UI sizes; four elevation tiers whose shadow grows with the tier, from `0 2px 8px rgba(0,0,0,.12)` to `0 24px 64px rgba(0,0,0,.35)` for a modal. Write the tokens in `STYLE.md` and reuse them in code.
- **Real content.** Plausible names, amounts, dates and statuses in the viewer's locale and script. No lorem ipsum, no "Item 1, Item 2", no KPI tile that disagrees with the chart beside it.
- **Pointer design.** Device-free: a 22–26 px arrow with a 1.5 px outline in the opposite tone of the UI. In-device mobile: a 40–48 px translucent circle at 25–35 % opacity, visible only during the tap; never draw an arrow on a phone.
- **Framing numbers.** On 16:9 the device-free screen fills 72–84 % of frame width, with up to 6° of rotation during its arrival move only. On 9:16 keep the screen full width and travel vertically instead of shrinking it. Callouts sit outside the screen edge, never over the control they describe.
- **Camera.** One group transform (`CameraRig` in `starters/remotion`, a single `setTransform` in Canvas) drives push, pan and focus for the whole scene. When a focus zoom exceeds 1.4×, build the screen at 2× or render with `--scale 2`.
- **Depth without gimmicks.** Depth comes from elevation tiers, overlap and a 2–4 % parallax between chrome and content during pans; not from 3D tilts, glass blur on every card or a perpetual glow.

**بالعربية:** الشاشة طبقات لا لقطة: خلفية ← هيكل (شريط جانبي/علوي) ← محتوى (بطاقات وصفوف وحقول) ← عناصر تحكم ← طبقات فوقية (نافذة، قائمة، تنبيه) ← طبقة المؤشر ← طبقة الشروحات، ولكل طبقة خطها الزمني. شبكة 8 بكسل، ثلاثة أنصاف أقطار (8/16/24)، أربع درجات ارتفاع بظلال تكبر مع الدرجة. محتوى حقيقي بلغة المشاهد وأرقام متسقة، لا نص وهمي. المؤشر سهم 22–26 بكسل بلا جهاز، ودائرة لمس شفافة 40–48 بكسل داخل الهاتف ولا سهم أبدًا. الشاشة الطافية تملأ 72–84% من عرض الكادر الأفقي، وفي العمودي تبقى بكامل العرض ونتحرك رأسيًا. كاميرا واحدة لكل مشهد عبر تحويل مجموعة واحد؛ أي تقريب فوق 1.4× يتطلب بناء الشاشة بدقة مضاعفة.

## 3. Motion mechanics — ميكانيكا الحركة

Every interaction is a triad: **intent** (pointer arrives) → **action** (press) → **response** (the UI answers after a short latency). Skip one and the film reads as fake. The numbers are first estimates at 30 fps; refine against the reference.

| Event | Duration | Curve | Notes |
|---|---|---|---|
| Cursor travel | 380–700 ms for 200–900 px | `cubic-bezier(0.2, 0.8, 0.2, 1)` | path lifts 2–4 % of distance mid-way (a wrist arc); settle 80–120 ms before pressing |
| Hover state | 120–160 ms | `cubic-bezier(0.4, 0, 0.2, 1)` | background and elevation only, no scale |
| Press / release | 80 ms down, 140 ms up | down linear; up spring k=300 d=20 m=1 | button scale 1→0.96; cursor 1→0.88 |
| Tap ripple (mobile) | 320–400 ms | `cubic-bezier(0.16, 1, 0.3, 1)` | 0→48 px, alpha 0.35→0 |
| Response latency | 60–120 ms | — | gap between release and the first UI change |
| Modal open | backdrop 200 ms; panel 280–320 ms | panel spring k=170 d=18 m=1 | scale 0.96→1, y 12→0 px |
| Modal close | 160–200 ms | `cubic-bezier(0.4, 0, 1, 1)` | always faster than open |
| Dropdown / popover | 180–220 ms | expo-out | transform origin at the trigger |
| Toggle / checkbox | 180 ms | spring k=400 d=28 | knob travel and colour together |
| Tab switch | content cross-fade ≤150 ms; indicator 240 ms | indicator expo-out | content never slides and fades at once |
| List stagger | 40–60 ms per item, whole list ≤400 ms | item 260 ms expo-out | y 16→0, alpha 0→1; cap at 8 visible items |
| Typing | 55–90 ms per character, ±20 ms seeded jitter | — | caret blinks every 530 ms; 1 fake typo per 40 chars at most |
| Scroll | 600–900 ms per screen height | `cubic-bezier(0.45, 0, 0.15, 1)` | 1.2–2.0 s pause between moves |
| Toast | in 240 ms, hold 1.6–2.4 s, out 200 ms | in spring k=200 d=22 | one toast on screen at a time |
| Screen arrival | 520–640 ms | expo-out | y 48→0, alpha 0→1, scale 0.98→1 |
| Focus zoom | 500–700 ms | `cubic-bezier(0.65, 0, 0.35, 1)` | 1→1.4–1.6×, hold ≥1.5 s, release in 600 ms |
| Camera push | 1.00→1.06 across 2–5 s | in-out-sine | pan ≤120 px per scene |
| Shared-element move | 320–420 ms | spring k=170 d=20 | the element travels, everything else fades |

Rules that hold across the table:

- **Dwell.** After a state settles, give 1.2–2.0 s of reading time before the next intent (0.8 s minimum in reels). The dwell is where the voice-over lands.
- **Speed hierarchy.** Chrome slowest, content medium, pointer and micro-feedback fastest. A sidebar and a button moving at the same speed flatten the scene.
- **One overshoot per scene.** At most one spring with visible bounce (damping < 16); every other move is expo-out or ease-in-out.
- **Floors and ceilings.** Nothing visible is shorter than 80 ms; nothing stays frozen longer than 1.2 s unless a caret, progress bar or slow camera keeps the frame alive.
- **Latency is content.** 60–120 ms between release and response feels real; 0 ms is a slideshow, >200 ms is a bug.

**بالعربية:** كل تفاعل ثلاثية: نية (وصول المؤشر) ← فعل (ضغط) ← استجابة بعد كمون 60–120 مللي ثانية؛ الاستجابة الفورية تبدو مزيفة وفوق 200 تبدو عطلًا. انتقال المؤشر 380–700 مللي ثانية بقوس خفيف وتوقف 80–120 قبل الضغط؛ الضغط 80 نزولًا و140 صعودًا؛ النافذة تفتح 280–320 بنابض k=170 d=18 وتغلق أسرع 160–200؛ تدرّج القوائم 40–60 لكل عنصر بسقف 400 للمجموعة؛ الكتابة 55–90 لكل حرف مع تذبذب مثبّت بالبذرة؛ التمرير 600–900 لكل ارتفاع شاشة مع وقفة 1.2–2 ثانية؛ تقريب التركيز 500–700 ثم ثبات 1.5 ثانية. وقفة قراءة 1.2–2 ثانية بعد كل حالة، الهيكل أبطأ من المحتوى والمؤشر أسرع الجميع، ونابض واحد مرتد لكل مشهد.

## 4. Scene recipes — وصفات المشاهد

Times in ms from the start of the scene; each recipe assumes 30 fps and a 1080-wide screen.

### A. Arrival and first look (device-free)

| Start | End | Action | Easing |
|---|---|---|---|
| 0 | 520 | screen rises y 48→0, alpha 0→1, scale 0.98→1 | expo-out |
| 120 | 520 | shadow grows tier 1→2 | ease-out |
| 400 | 900 | chrome paints: sidebar then top bar (60 ms stagger) | 260 ms expo-out each |
| 700 | 1300 | 6 content cards stagger up, 50 ms apart | expo-out |
| 0 | 4000 | camera push 1.00→1.05 | in-out-sine |
| 1300 | 2800 | dwell; caret blinks in the search field | — |

### B. Click opens a modal

| Start | End | Action | Easing |
|---|---|---|---|
| 0 | 560 | cursor travels to the primary button, 3 % arc | `cubic-bezier(0.2, 0.8, 0.2, 1)` |
| 560 | 700 | settle; button hover state | `cubic-bezier(0.4, 0, 0.2, 1)` |
| 700 | 780 | press: button 0.96, cursor 0.88 | linear |
| 780 | 920 | release | spring k=300 d=20 |
| 860 | 1060 | backdrop alpha 0→0.5 | ease-out |
| 880 | 1200 | panel scale 0.96→1, y 12→0 | spring k=170 d=18 |
| 1000 | 1400 | panel fields stagger in, 50 ms apart | 260 ms expo-out |
| 1600 | 2200 | focus zoom 1→1.3 on the panel | `cubic-bezier(0.65, 0, 0.35, 1)` |
| 2200 | 3600 | dwell | — |

### C. Scroll-through tour with callouts

| Start | End | Action | Easing |
|---|---|---|---|
| 0 | 320 | callout 1 leader line draws (stroke-dashoffset) | expo-out |
| 240 | 480 | callout 1 label fades and rises 8 px | expo-out |
| 480 | 1800 | dwell on section 1 | — |
| 1800 | 2000 | callout 1 fades out | ease-in |
| 1800 | 2600 | content scrolls −720 px; chrome stays | `cubic-bezier(0.45, 0, 0.15, 1)` |
| 1800 | 2600 | background parallax −24 px | same |
| 2600 | 3100 | callout 2 draws | expo-out |
| 3100 | 4500 | dwell | — |

### D. Form fill, validation, success

| Start | End | Action | Easing |
|---|---|---|---|
| 0 | 480 | cursor to first field, press, focus ring 160 ms | travel curve; ring expo-out |
| 560 | 1700 | type 16 characters at 70 ms ±20 | — |
| 1700 | 1940 | validation tick draws next to the field | expo-out |
| 1940 | 2300 | focus jumps to the next field (ring moves, 240 ms) | spring k=170 d=20 |
| 2300 | 3200 | type 12 characters | — |
| 3400 | 3900 | cursor to Submit, press, release | as recipe B |
| 3980 | 4600 | button label swaps to a spinner (cross-fade 120 ms), spinner runs | linear rotation |
| 4600 | 4840 | toast slides in from the top-end corner | spring k=200 d=22 |
| 4840 | 6800 | hold, then toast leaves in 200 ms | ease-in |

**بالعربية:** أربع وصفات جاهزة: (أ) وصول الشاشة ثم رسم الهيكل ثم تدرّج البطاقات مع دفعة كاميرا بطيئة ووقفة؛ (ب) المؤشر يصل ويستقر ويضغط، ثم خلفية معتمة ولوحة تفتح بنابض وحقول متدرجة وتقريب تركيز؛ (ج) شرح يُرسم بخط قائد، وقفة، تمرير 720 بكسل والهيكل ثابت مع بارالاكسس خفيف، ثم شرح ثانٍ؛ (د) تعبئة نموذج بكتابة حرفية مع علامة تحقق، انتقال التركيز، إرسال، مؤشر تحميل، ثم تنبيه نجاح يدخل من الزاوية العلوية ناحية نهاية السطر. الأزمنة بالمللي ثانية من بداية المشهد والجداول أعلاه هي المرجع.

## 5. Implementation — التنفيذ

Two paths, same plan. In `starters/remotion`, `Film.tsx` already wraps scenes in `CameraRig`; add a `Screen` component that stacks the layers from section 2 as absolutely positioned divs and drive each from `useCurrentFrame()` with `progress` and `staggerStart` from `easing.ts`. Convert the millisecond tables to frames in one place (`Math.round(ms / 1000 * fps)`) so retiming is a single edit. The snippet is the cursor and press feedback of recipe B:

```tsx
import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { easeInOutCubic } from "./easing";

type Pt = { x: number; y: number };
/** Cursor travels on a wrist-like arc, presses at `pressAt` and releases. Frames. */
export const CursorPress: React.FC<{ from: Pt; to: Pt; travel: number; pressAt: number; accent: string }> =
  ({ from, to, travel, pressAt, accent }) => {
    const frame = useCurrentFrame();
    const { fps } = useVideoConfig();
    const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
    const t = interpolate(frame, [0, travel], [0, 1], { ...clamp, easing: easeInOutCubic });
    const dist = Math.hypot(to.x - from.x, to.y - from.y);
    const lift = Math.sin(t * Math.PI) * dist * 0.03;
    const x = from.x + (to.x - from.x) * t;
    const y = from.y + (to.y - from.y) * t - lift;
    const down = interpolate(frame, [pressAt, pressAt + 2], [0, 1], clamp);
    const up = spring({ frame: frame - pressAt - 2, fps, config: { stiffness: 300, damping: 20 } });
    const scale = 1 - 0.12 * down * (1 - up);
    const ripple = interpolate(frame, [pressAt + 3, pressAt + 13], [0, 1], clamp);
    return (
      <>
        <div style={{ position: "absolute", left: to.x - 24 * ripple, top: to.y - 24 * ripple,
          width: 48 * ripple, height: 48 * ripple, borderRadius: 999,
          background: accent, opacity: 0.35 * (1 - ripple) }} />
        <svg width={24} height={28} viewBox="0 0 24 28" style={{ position: "absolute", left: x, top: y,
          transform: `scale(${scale})`, transformOrigin: "4px 2px" }}>
          <path d="M4 2 L20 15 L12 16 L16 25 L12 26.5 L8 17.5 L4 21 Z" fill="#fff" stroke="#0b0d12" strokeWidth={1.5} />
        </svg>
      </>
    );
  };
// Usage inside a scene: <CursorPress from={{x:300,y:1400}} to={{x:540,y:980}} travel={17} pressAt={21} accent="#19c37d" />
// The modal then opens from frame pressAt + 5: spring({ frame: frame - (pressAt + 5), fps, config: { stiffness: 170, damping: 18 } }).
```

In `starters/html-canvas` the page exposes `window.__kosif = { duration, seek(t) }` and `tools/render_html.cjs` calls `seek` once per frame, so `draw(t)` must be a pure function of time with no state carried between frames. The arrival and press beats in Canvas:

```js
// product-ui.js — deterministic timeline for tools/render_html.cjs (seek mode)
const cv = document.querySelector("canvas"), g = cv.getContext("2d");
const expoOut = (t) => (t >= 1 ? 1 : 1 - Math.pow(2, -10 * t));
const inOut = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
const seg = (t, a, b, e = expoOut) => e(Math.min(1, Math.max(0, (t - a) / (b - a))));
const FROM = { x: 300, y: 1400 }, TO = { x: 540, y: 980 };          // cursor path, px
const BTN = { x: 440, y: 950, w: 200, h: 60 };                      // primary button

function draw(t) {                                                   // t in seconds
  g.setTransform(1, 0, 0, 1, 0, 0);
  g.fillStyle = "#0b0d12"; g.fillRect(0, 0, cv.width, cv.height);
  const push = 1 + 0.05 * (t / 4);                                   // camera push 1.00 -> 1.05 over 4 s
  g.translate(cv.width / 2, cv.height / 2); g.scale(push, push); g.translate(-cv.width / 2, -cv.height / 2);
  const arrive = seg(t, 0, 0.52);                                    // screen rises 48 px, fades in
  g.globalAlpha = arrive;
  g.shadowColor = "rgba(0,0,0,.25)"; g.shadowBlur = 28 * arrive; g.shadowOffsetY = 10 * arrive;
  g.fillStyle = "#161a23"; g.beginPath(); g.roundRect(90, 300 + 48 * (1 - arrive), 900, 1320, 24); g.fill();
  g.shadowBlur = 0; g.shadowOffsetY = 0; g.globalAlpha = 1;
  for (let i = 0; i < 6; i++) {                                      // cards stagger 50 ms apart
    const k = seg(t, 0.7 + i * 0.05, 0.96 + i * 0.05);
    g.globalAlpha = k; g.fillStyle = "#1f2430";
    g.beginPath(); g.roundRect(130, 420 + i * 120 + 16 * (1 - k), 820, 96, 16); g.fill();
  }
  g.globalAlpha = 1;
  const down = seg(t, 1.9, 1.98, (x) => x), up = seg(t, 1.98, 2.12);  // press 80 ms, release 140 ms
  const btnScale = 1 - 0.04 * down * (1 - up);
  g.translate(BTN.x + BTN.w / 2, BTN.y + BTN.h / 2); g.scale(btnScale, btnScale);
  g.fillStyle = "#19c37d"; g.beginPath(); g.roundRect(-BTN.w / 2, -BTN.h / 2, BTN.w, BTN.h, 12); g.fill();
  g.setTransform(push, 0, 0, push, (1 - push) * cv.width / 2, (1 - push) * cv.height / 2);
  const m = seg(t, 1.2, 1.76, inOut), lift = Math.sin(m * Math.PI) * 14;   // cursor travel 560 ms
  const cx = FROM.x + (TO.x - FROM.x) * m, cy = FROM.y + (TO.y - FROM.y) * m - lift;
  const cs = 1 - 0.12 * down * (1 - up);
  g.translate(cx, cy); g.scale(cs, cs); g.fillStyle = "#fff"; g.strokeStyle = "#0b0d12"; g.lineWidth = 1.5;
  g.beginPath(); g.moveTo(0, 0); g.lineTo(16, 13); g.lineTo(8, 14); g.lineTo(12, 23); g.lineTo(8, 24.5);
  g.lineTo(4, 15.5); g.lineTo(0, 19); g.closePath(); g.fill(); g.stroke();
}
window.__kosif = { duration: 4, seek: draw };
```

Render with `node tools/render_html.cjs --in index.html --out film.mp4 --mode seek --fps 30 --seed 7`; the seed matters when typing jitter uses `Math.random`. If the interface is real DOM with CSS transitions, keep the seek contract by pausing every animation and setting its time inside `seek` (`document.getAnimations().forEach(a => { a.pause(); a.currentTime = t * 1000; })`), or render with `--mode virtual`, which advances Chromium's clock exactly one frame at a time.

**بالعربية:** مساران لنفس الخطة. في `starters/remotion` تُضاف مكوّنة `Screen` تكدّس الطبقات كعناصر `absolute` داخل `CameraRig`، وتُقاد كل طبقة من `useCurrentFrame()` مع `progress` و`staggerStart` من `easing.ts`، وتُحوَّل أزمنة الجداول إلى إطارات في مكان واحد. في `starters/html-canvas` الصفحة تكشف `window.__kosif = { duration, seek(t) }` ودالة الرسم تابع نقي للزمن بلا حالة بين الإطارات، والرندر عبر `tools/render_html.cjs --mode seek`. إذا كانت الواجهة DOM حقيقي بانتقالات CSS، أوقف كل `getAnimations()` واضبط `currentTime` داخل `seek`، أو استخدم `--mode virtual`.

## 6. Arabic and RTL notes — ملاحظات العربية

- Mirror the layout, not just the text: sidebar on the right, primary action at the end of the row (left in RTL), chevrons and checkmarks flipped, progress bars filling right-to-left. The cursor's natural start is the bottom-right, so recipe B's travel runs from the right.
- Forward navigation pushes the new screen in from the left edge and the old one out to the right; scroll stays vertical. Toasts enter from the top-left ("top-end") corner.
- Never split an Arabic word into letters to animate it. Typing is fine because the browser reshapes the whole prefix each frame; the last glyph switching from final to medial form as the next letter lands is what real typing looks like. Cut typing at grapheme boundaries (`Intl.Segmenter`), never inside a base+mark pair.
- Set `dir="rtl"` on the screen root and `unicode-bidi: plaintext` on mixed lines; wrap Latin product names, emails and codes in `<bdi>`. Choose one digit system per film (Western or Arabic-Indic) for UI numbers, charts and captions alike.
- UI labels at a minimum of 28 px on a 1080-wide frame, line-height 1.6–1.8, letter-spacing 0; readable families are Cairo, Tajawal, IBM Plex Sans Arabic and Noto Sans Arabic. The full rules live in `playbooks/arabic-typography.md`.
- Callout leader lines start at the right edge of the label; arrows keep their semantic direction (toward the result), not a mirrored copy of the LTR film.

**بالعربية:** اعكس التخطيط لا النص فقط: الشريط الجانبي يمينًا، الزر الرئيسي في نهاية السطر، الأسهم والعلامات مقلوبة، وأشرطة التقدم تمتلئ من اليمين. التنقل للأمام يدفع الشاشة الجديدة من اليسار. لا تفكك الكلمة إلى حروف لتحريكها؛ الكتابة الحرفية مقبولة لأن المتصفح يعيد تشكيل النص كاملًا كل إطار، والقص على حدود الحروف المركّبة فقط. `dir="rtl"` على جذر الشاشة، و`<bdi>` للأسماء اللاتينية والأرقام، ونظام أرقام واحد للفيلم كله. حجم نص الواجهة لا يقل عن 28 بكسل على عرض 1080 وتباعد الأحرف صفر. التفاصيل في `playbooks/arabic-typography.md`.

## 7. Audio sync — المزامنة مع الصوت

When the user supplies a voice, `words.json` (`{word, start, end}` in seconds) is the master clock and the audio file is never trimmed, stretched or re-encoded. Map each interaction to the verb that names it: the press lands within ±100 ms of the verb's `start`, the response begins before the sentence ends, and the dwell sits on the clause that explains the result. If the sentence outlasts the dwell, let the camera push cover the remainder rather than adding an action. Arrival moves sit on the breath before the first word.

Sound design is sparse: one short click per press (10–30 ms transient, 12–18 dB below the voice), one soft swish per modal or screen change, nothing on list items, hovers or carets. A film without SFX is acceptable; a sound on every stagger item is not. In Remotion add `<Audio src={staticFile("voice.mp3")} />` at frame 0 and read `public/words.json`; with `render_html.cjs` pass `--audio voice.mp3` so the muxed track keeps its timing. Verify with the probe in `templates/TEST_REPORT.md` and by scrubbing three key words against the frames they trigger. See `playbooks/audio-sync.md` for transcription and alignment.

**بالعربية:** عند وجود صوت فإن `words.json` هو الساعة الرئيسية والملف الصوتي لا يُقص ولا يُمدّ ولا يُعاد ترميزه. اربط كل تفاعل بالفعل الذي يسميه: الضغط خلال ±100 مللي ثانية من بداية الكلمة، والاستجابة تبدأ قبل نهاية الجملة، ووقفة القراءة على العبارة التي تشرح النتيجة. المؤثرات شحيحة: نقرة قصيرة لكل ضغط، وسويش ناعم لكل نافذة أو شاشة، ولا صوت على عناصر القوائم أو التمرير أو المؤشر. في Remotion يوضع `<Audio>` عند الإطار صفر، ومع `render_html.cjs` يُمرَّر `--audio`، ثم يُتحقق من المدة والمسار الصوتي وثلاث كلمات مفتاحية.

## 8. Quality checklist — قائمة الفحص

1. Does every interaction show intent, action and response, with 60–120 ms latency before the response?
2. Is every screen built from individually retimable layers, with no flattened screenshot animating?
3. Does each settled state hold at least 1.2 s (0.8 s in reels) before the next intent?
4. Is there at most one bouncing spring per scene, everything else expo-out or ease-in-out?
5. Does the pointer match the framing (arrow device-free, tap circle in a phone) and never teleport?
6. Is all UI copy real, locale-correct and consistent, with one digit system throughout?
7. In Arabic, is the layout mirrored (sidebar, buttons, chevrons, toasts) with no joined letters split?
8. Does any focus zoom above 1.4× use a 2× screen or `--scale 2`?
9. With supplied voice, does each press land within ±100 ms of its verb and the audio stay untouched?
10. Did a contact-sheet preview go to the user before the final render, and did the MP4 pass the duration, fps, frame-count and audio-stream checks in `TEST_REPORT.md`?

**بالعربية:** عشر أسئلة نعم/لا: ثلاثية نية/فعل/استجابة بكمون 60–120؟ شاشات من طبقات لا لقطة مسطحة؟ وقفة 1.2 ثانية بعد كل حالة؟ نابض مرتد واحد لكل مشهد؟ مؤشر مناسب للإطار ولا ينتقل قفزًا؟ نص حقيقي متسق بنظام أرقام واحد؟ تخطيط عربي معكوس وحروف غير مفككة؟ دقة مضاعفة لأي تقريب فوق 1.4×؟ ضغط خلال ±100 مللي ثانية من الفعل المنطوق وصوت غير معدّل؟ فحص المدة والإطارات والصوت في `TEST_REPORT.md` ومعاينة قبل الرندر؟

## 9. Anti-patterns — أخطاء شائعة

The tells of a generated-looking product film; each one is a reason to reject a preview.

- **The teleporting cursor.** A pointer that appears over the button, moves in a straight line at constant speed, or presses with no settle. Real hands arc, slow down and pause.
- **Zero-latency UI.** The modal appears on the same frame as the click. The 60–120 ms gap is what makes it feel like software instead of a slideshow.
- **Bounce on everything.** Every card, label and toast overshooting on the same spring. Overshoot is a highlight, not a default.
- **The glass-and-glow stack.** Purple-to-blue gradient, blurred glass cards with no content, floating orbs, a glow on every edge. Depth comes from elevation tiers and overlap.
- **Lorem UI.** "Item 1", "John Doe", "$1,234", charts with no axis, grey-circle avatars. Viewers pause product films; the content must survive a pause.
- **Uniform 300 ms.** One duration and one curve for chrome, content and pointer alike.
- **Infinite stagger.** Twelve rows entering 100 ms apart so the list takes 1.2 s to arrive. Cap at 400 ms total and 8 items.
- **Blur-in text.** Every label arriving from a Gaussian blur. Inside a UI, text fades and rises 8–16 px; blur belongs to camera focus only.
- **3D wobble.** Screens tilting in perspective and drifting forever. Rotation is for the arrival move only.
- **Mismatched density.** A 1× screenshot zoomed to 1.8× next to crisp vector callouts.
- **Fake scroll.** Chrome moving with the content, or scroll without a pause. Chrome stays, content moves, then everything stops to be read.
- **Sound on everything.** A whoosh per list item. One click per press, one swish per screen.

**بالعربية:** علامات الفيلم المولَّد التي تستوجب رفض المعاينة: مؤشر ينتقل قفزًا أو بخط مستقيم بسرعة ثابتة؛ واجهة بلا كمون تستجيب في نفس إطار النقر؛ ارتداد على كل عنصر؛ خلفية بنفسجية متدرجة مع بطاقات زجاجية فارغة وتوهج على كل حافة؛ محتوى وهمي لا يصمد عند الإيقاف؛ مدة واحدة ومنحنى واحد لكل شيء؛ تدرّج لا ينتهي؛ ضبابية دخول على كل نص؛ شاشات تميل وتهتز في منظور ثلاثي الأبعاد؛ لقطة بدقة منخفضة مكبّرة بجانب شروحات حادة؛ تمرير يحرّك الهيكل مع المحتوى بلا وقفة؛ مؤثر صوتي على كل عنصر.

## 10. Related styles — استايلات ذات صلة

- saas-demo — استعراض SaaS
- ui-micro — واجهات دقيقة
- glass-ui — واجهة زجاجية
- scroll-world — عالم تمرير
- pm-aschapmann-131210 — SaaS launch video
- pm-demonugc-4c5753 — Morphing UI states loop
- pm-jhylee95-e1152f — Supademo launch video
- pm-visheshbaghell-3aba37 — Tally product demo
